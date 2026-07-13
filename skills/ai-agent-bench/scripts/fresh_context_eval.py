"""Run executable fresh-context agent checks with Pydantic Evals."""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

try:
    import logfire
except ImportError:  # logfire extra absent: tracing becomes a no-op
    import logfire_api as logfire
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.lifecycle import CaseLifecycle
from pydantic_evals.reporting import ReportCase, ReportCaseFailure


@dataclass(frozen=True)
class FileContains:
    path: str
    text: str


@dataclass(frozen=True)
class Scenario:
    identifier: str
    prompt: str
    files: dict[str, str]
    required_tools: tuple[str, ...]
    clean_worktree: bool | None
    changed_files: tuple[str, ...]
    file_contains: tuple[FileContains, ...] = ()


@dataclass(frozen=True)
class TrialResult:
    returncode: int
    transcript: str
    stderr: str = ""
    changed_files: tuple[str, ...] = ()
    file_contents: tuple[tuple[str, str], ...] = ()


def load_scenarios(path: Path) -> list[Scenario]:
    data = json.loads(path.read_text())
    if not isinstance(data.get("cases"), list):
        raise ValueError("cases must be a list")
    scenarios: list[Scenario] = []
    identifiers: set[str] = set()
    for item in data["cases"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise ValueError("every case needs a non-empty string id")
        if item["id"] in identifiers:
            raise ValueError(f"duplicate case id: {item['id']}")
        identifiers.add(item["id"])
        if not isinstance(item.get("prompt"), str) or not item["prompt"]:
            raise ValueError(f"{item['id']}: prompt must be a non-empty string")
        files = item.get("files", {})
        if not isinstance(files, dict) or not all(
            isinstance(relative, str) and isinstance(content, str)
            for relative, content in files.items()
        ):
            raise ValueError(f"{item['id']}: files must map string paths to string content")
        assertions = item.get("assertions", [])
        allowed = {"tool", "clean_worktree", "changed_file", "file_contains"}
        if not isinstance(assertions, list) or not all(
            isinstance(assertion, dict) and set(assertion) <= allowed and len(assertion) == 1
            for assertion in assertions
        ):
            raise ValueError(f"{item['id']}: each assertion must be one executable check")
        for assertion in assertions:
            if "clean_worktree" in assertion and not isinstance(assertion["clean_worktree"], bool):
                raise ValueError(f"{item['id']}: clean_worktree must be a boolean")
            if "tool" in assertion and not isinstance(assertion["tool"], str):
                raise ValueError(f"{item['id']}: tool must be a string")
            if "changed_file" in assertion and not isinstance(assertion["changed_file"], str):
                raise ValueError(f"{item['id']}: changed_file must be a string")
            if "file_contains" in assertion:
                check = assertion["file_contains"]
                if (
                    not isinstance(check, dict)
                    or set(check) != {"path", "text"}
                    or not all(isinstance(value, str) for value in check.values())
                ):
                    raise ValueError(f"{item['id']}: file_contains needs string path and text")
        scenarios.append(
            Scenario(
                identifier=item["id"],
                prompt=item["prompt"],
                files=files,
                required_tools=tuple(
                    assertion["tool"] for assertion in assertions if "tool" in assertion
                ),
                clean_worktree=next(
                    (
                        assertion["clean_worktree"]
                        for assertion in assertions
                        if "clean_worktree" in assertion
                    ),
                    None,
                ),
                changed_files=tuple(
                    assertion["changed_file"]
                    for assertion in assertions
                    if "changed_file" in assertion
                ),
                file_contains=tuple(
                    FileContains(**assertion["file_contains"])
                    for assertion in assertions
                    if "file_contains" in assertion
                ),
            )
        )
    return scenarios


def _plugin_dir(repository_root: Path) -> Path:
    candidate = repository_root / "plugins/development-skills"
    return candidate if candidate.is_dir() else repository_root


def build_command(
    agent: str, prompt: str, workdir: Path, transcript: Path, repository_root: Path
) -> list[str]:
    plugin_dir = _plugin_dir(repository_root)
    if agent == "claude":
        return [
            "claude",
            "-p",
            prompt,
            "--output-format",
            "stream-json",
            "--verbose",
            "--dangerously-skip-permissions",
            "--plugin-dir",
            str(plugin_dir),
        ]
    if agent == "codex":
        instructions = plugin_dir / "skills/using-development-skills/SKILL.md"
        if instructions.is_file():
            preload = f"Read {instructions} before your first decision."
        else:
            preload = (
                f"Inspect {plugin_dir / 'skills'} and read the relevant SKILL.md before your "
                "first decision."
            )
        prompt = f"{preload}\n\n{prompt}"
        return [
            "codex",
            "exec",
            "--json",
            "--sandbox",
            "workspace-write",
            "--add-dir",
            str(plugin_dir),
            "--output-last-message",
            str(transcript.with_name("last_message.txt")),
            "--cd",
            str(workdir),
            prompt,
        ]
    raise ValueError(f"unsupported agent: {agent}")


def run_agent(
    agent: str,
    prompt: str,
    workdir: Path,
    transcript: Path,
    repository_root: Path,
    timeout_seconds: int = 600,
) -> TrialResult:
    command = build_command(agent, prompt, workdir, transcript, repository_root)
    try:
        with logfire.span("fresh_context.agent", agent=agent, workdir=str(workdir)):
            process = subprocess.run(
                command,
                cwd=workdir,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds,
            )
    except subprocess.TimeoutExpired as error:
        stdout = (
            error.stdout.decode(errors="replace")
            if isinstance(error.stdout, bytes)
            else error.stdout
        )
        stderr = (
            error.stderr.decode(errors="replace")
            if isinstance(error.stderr, bytes)
            else error.stderr
        )
        transcript.write_text(stdout or "")
        return TrialResult(124, stdout or "", stderr or "timeout")
    transcript.write_text(process.stdout)
    changed = subprocess.run(
        ["git", "status", "--porcelain"], cwd=workdir, capture_output=True, text=True, check=True
    )
    changed_files = tuple(line[3:] for line in changed.stdout.splitlines())
    return TrialResult(process.returncode, process.stdout, process.stderr, changed_files)


def _tool_names(transcript: str) -> set[str]:
    names: set[str] = set()
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                for key in ("tool_name", "name"):
                    if isinstance(value.get(key), str):
                        names.add(value[key])
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(event)
    return names


@dataclass
class ObservableChecks(Evaluator[Scenario, TrialResult, None]):
    def evaluate(self, ctx: EvaluatorContext[Scenario, TrialResult, None]) -> dict[str, bool]:
        observed = _tool_names(ctx.output.transcript)
        results = {"agent_exit_zero": ctx.output.returncode == 0}
        if ctx.inputs.required_tools:
            results["required_tools"] = set(ctx.inputs.required_tools).issubset(observed)
        if ctx.inputs.clean_worktree is not None:
            results["clean_worktree"] = (not ctx.output.changed_files) == ctx.inputs.clean_worktree
        if ctx.inputs.changed_files:
            results["changed_files"] = set(ctx.inputs.changed_files).issubset(
                ctx.output.changed_files
            )
        contents = dict(ctx.output.file_contents)
        for index, check in enumerate(ctx.inputs.file_contains):
            name = (
                "file_contains" if len(ctx.inputs.file_contains) == 1 else f"file_contains_{index}"
            )
            results[name] = check.text in contents.get(check.path, "")
        return results


class FixtureManager:
    def __init__(self, workspace: Path, keep: bool):
        self.workspace = workspace
        self.keep = keep
        self.paths: dict[str, Path] = {}

    def create(self, scenario: Scenario) -> Path:
        path = Path(
            tempfile.mkdtemp(prefix=f"fresh-context-{scenario.identifier}-", dir=self.workspace)
        )
        root = path.resolve()
        try:
            for relative, content in scenario.files.items():
                target = (path / relative).resolve()
                if not target.is_relative_to(root):
                    raise ValueError(f"fixture file {relative!r} escapes outside the fixture")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            if not scenario.files:
                (path / ".gitkeep").touch()
            subprocess.run(["git", "init", "-q"], cwd=path, check=True)
            exclude = path / ".git/info/exclude"
            exclude.write_text(
                exclude.read_text() + "\nsession.jsonl\nlast_message.txt\n.eval-plugin/\n"
            )
            subprocess.run(["git", "add", "."], cwd=path, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.email=eval@example.local",
                    "-c",
                    "user.name=Eval",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                cwd=path,
                check=True,
            )
        except Exception:
            shutil.rmtree(path, ignore_errors=True)
            raise
        self.paths[scenario.identifier] = path
        return path

    def discard(self, scenario: Scenario) -> None:
        path = self.paths.pop(scenario.identifier, None)
        if path and not self.keep:
            shutil.rmtree(path)


class FixtureLifecycle(CaseLifecycle[Scenario, TrialResult, None]):
    def __init__(self, case: Case[Scenario, TrialResult, None], manager: FixtureManager):
        super().__init__(case)
        self.manager = manager

    async def setup(self) -> None:
        self.manager.create(self.case.inputs)

    async def teardown(
        self,
        _result: ReportCase[Scenario, TrialResult, None]
        | ReportCaseFailure[Scenario, TrialResult, None]
        | None,
    ) -> None:
        self.manager.discard(self.case.inputs)


def evaluate(
    scenarios: list[Scenario],
    *,
    agent: str,
    plugin_root: Path,
    repeat: int,
    workspace: Path,
    keep: bool = False,
    timeout_seconds: int = 600,
):
    manager = FixtureManager(workspace, keep)

    def task(scenario: Scenario) -> TrialResult:
        path = manager.paths[scenario.identifier]
        isolated_plugin = path / ".eval-plugin"
        shutil.copytree(_plugin_dir(plugin_root), isolated_plugin, symlinks=True)
        result = run_agent(
            agent,
            scenario.prompt,
            path,
            path / "session.jsonl",
            isolated_plugin,
            timeout_seconds,
        )
        contents: list[tuple[str, str]] = []
        root = path.resolve()
        for check in scenario.file_contains:
            target = (path / check.path).resolve()
            if not target.is_relative_to(root):
                raise ValueError(f"asserted file {check.path!r} escapes outside the fixture")
            contents.append((check.path, target.read_text() if target.is_file() else ""))
        return replace(result, file_contents=tuple(contents))

    dataset = Dataset(
        name="fresh-context",
        cases=[Case(name=scenario.identifier, inputs=scenario) for scenario in scenarios],
        evaluators=[ObservableChecks()],
    )
    return asyncio.run(
        dataset.evaluate(
            task,
            repeat=repeat,
            max_concurrency=1,
            progress=False,
            lifecycle=lambda case: FixtureLifecycle(case, manager),
        )
    )


def _report_json(report: Any) -> str:
    cases = []
    totals: dict[str, list[int]] = {}
    for case in report.cases:
        assertions = {name: result.value for name, result in case.assertions.items()}
        for name, value in assertions.items():
            passed, total = totals.setdefault(name, [0, 0])
            totals[name] = [passed + int(value is True), total + 1]
        cases.append(
            {
                "case": case.source_case_name or case.name,
                "run": case.name,
                "assertions": assertions,
            }
        )
    rates = {
        name: {"passed": passed, "total": total, "rate": passed / total}
        for name, (passed, total) in totals.items()
    }
    failures = [
        {
            "case": failure.source_case_name or failure.name,
            "run": failure.name,
            "error": failure.error_message,
        }
        for failure in report.failures
    ]
    return json.dumps({"cases": cases, "failures": failures, "rates": rates}, indent=2) + "\n"


def report_failed(report: Any) -> bool:
    return bool(report.failures) or any(
        result.value is not True for case in report.cases for result in case.assertions.values()
    )


def _report_results(report: dict[str, Any]) -> dict[tuple[str, str], list[bool]]:
    results: dict[tuple[str, str], list[bool]] = {}
    for case in report.get("cases", []):
        name = case["case"]
        results.setdefault((name, "task_succeeded"), []).append(True)
        for assertion, passed in case["assertions"].items():
            results.setdefault((name, assertion), []).append(passed is True)
    for failure in report.get("failures", []):
        results.setdefault((failure["case"], "task_succeeded"), []).append(False)
    return results


def _rate(values: list[bool]) -> dict[str, int | float]:
    passed = sum(values)
    return {"passed": passed, "total": len(values), "rate": passed / len(values)}


def compare_reports(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Compare identical Pydantic eval runs without hiding missing evidence."""
    old = _report_results(baseline)
    new = _report_results(candidate)
    comparisons: list[dict[str, Any]] = []
    counts = {"regressions": 0, "improvements": 0, "stable": 0, "inconclusive": 0}

    for case, assertion in sorted(old.keys() | new.keys()):
        old_values = old.get((case, assertion))
        new_values = new.get((case, assertion))
        old_rate = _rate(old_values) if old_values else None
        new_rate = _rate(new_values) if new_values else None
        if (
            not old_rate
            or not new_rate
            or old_rate["total"] != new_rate["total"]
            or (assertion == "task_succeeded" and old_rate["rate"] == new_rate["rate"] < 1)
        ):
            status = "INCONCLUSIVE"
            counts["inconclusive"] += 1
        elif new_rate["rate"] < old_rate["rate"]:
            status = "REGRESSION"
            counts["regressions"] += 1
        elif new_rate["rate"] > old_rate["rate"]:
            status = "IMPROVEMENT"
            counts["improvements"] += 1
        else:
            status = "STABLE"
            counts["stable"] += 1
        comparisons.append(
            {
                "case": case,
                "assertion": assertion,
                "baseline": old_rate,
                "candidate": new_rate,
                "status": status,
            }
        )

    if not comparisons:
        verdict = "INCONCLUSIVE"
    elif counts["regressions"]:
        verdict = "REGRESSION"
    elif counts["inconclusive"]:
        verdict = "INCONCLUSIVE"
    else:
        verdict = "NO_REGRESSION"
    return {"verdict": verdict, "summary": counts, "comparisons": comparisons}


def _write_output(rendered: str, output: Path | None) -> None:
    if output:
        output.write_text(rendered)
    else:
        print(rendered, end="")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--agent", choices=["claude", "codex"])
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--plugin-dir", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--compare",
        nargs=2,
        type=Path,
        metavar=("BASELINE_REPORT", "CANDIDATE_REPORT"),
    )
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    if args.compare:
        if args.cases or args.agent:
            parser.error("--compare cannot be combined with --cases or --agent")
        baseline, candidate = (json.loads(path.read_text()) for path in args.compare)
        comparison = compare_reports(baseline, candidate)
        _write_output(json.dumps(comparison, indent=2) + "\n", args.output)
        if comparison["verdict"] != "NO_REGRESSION":
            sys.exit(1)
        return
    if not args.cases or not args.agent:
        parser.error("--cases and --agent are required unless --compare is used")
    if args.repeat < 1:
        parser.error("--repeat must be positive")
    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be positive")
    logfire.configure(send_to_logfire="if-token-present", service_name="fresh-context-evals")
    report = evaluate(
        load_scenarios(args.cases),
        agent=args.agent,
        plugin_root=args.plugin_dir or args.repository_root,
        repeat=args.repeat,
        workspace=args.workspace,
        keep=args.keep,
        timeout_seconds=args.timeout_seconds,
    )
    rendered = _report_json(report)
    _write_output(rendered, args.output)
    if report_failed(report):
        sys.exit(1)


if __name__ == "__main__":
    main()
