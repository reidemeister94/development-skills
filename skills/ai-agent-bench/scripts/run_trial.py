"""Run a single agent-benchmark trial: worktree → baseline → agent → diff → post → gate → parse.

Task-agnostic. Reads configuration from a TOML file (convention:
`<repo>/.ai-agent-bench.toml`) written by the skill wizard. No hardcoded project-specific
knowledge — the task tells us which commands to run for measurement, gate, pre-hooks.

Output goes to `<repo>/eval-results/<task>/<agent>/run-<id>-<ts>/` and the agent's work is
preserved on a dedicated branch `eval-<agent>-run<id>-<ts>` (the worktree itself is cleaned
up at the end, but the branch survives for inspection via `git checkout`).

Usage:
    python run_trial.py --repo /abs/path --config /abs/path/.ai-agent-bench.toml \\
        --agent claude --run 1

Exit codes:
    0 — trial completed (gate may have failed; inspect gate_exit_code.txt)
    2 — bad arguments / preflight failure (missing CLI, dirty repo, invalid config)
    3 — gate preflight on HEAD failed (gate not usable as baseline)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------


def run(
    cmd: list[str] | str, *, cwd: Path | None = None, check: bool = True, **kwargs
) -> subprocess.CompletedProcess:
    """Thin wrapper around subprocess.run with sensible defaults."""
    shell = isinstance(cmd, str)
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check, shell=shell, **kwargs)


def run_capture(cmd: list[str] | str, *, cwd: Path | None = None) -> tuple[int, str, str]:
    """Run, capture stdout+stderr as text, return (exit_code, stdout, stderr)."""
    shell = isinstance(cmd, str)
    p = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, shell=shell, capture_output=True, text=True
    )
    return p.returncode, p.stdout, p.stderr


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def which(binary: str) -> str | None:
    return shutil.which(binary)


def expand_placeholders(s: str, *, repo: Path, worktree: Path, run_dir: Path) -> str:
    return (
        s.replace("{repo}", str(repo))
        .replace("{worktree}", str(worktree))
        .replace("{run_dir}", str(run_dir))
    )


def update_status(run_dir: Path, phase: str) -> None:
    """Append a phase transition to status.txt for the skill's heartbeat tailer."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with (run_dir / "status.txt").open("a") as f:
        f.write(f"{ts}\t{phase}\n")


def extract_command_basenames(cmd: str | None) -> list[str]:
    """Extract script/executable basenames from a shell pipeline.

    Splits on `&&`, `||`, `;`, `|`. For each sub-command skips env-var prefixes
    (`VAR=value`) and flag tokens (`-x`), then takes the first remaining token. If
    the first non-flag token is a known interpreter (python, python3, node, bash,
    sh), takes the FIRST non-flag arg after it instead (i.e. the script path).

    Examples:
        "pytest -q"                                          → ["pytest"]
        "ruff check . && mypy . && pytest -q"                → ["ruff", "mypy", "pytest"]
        "./gradlew check && ./scripts/full_regression.sh"    → ["gradlew", "full_regression.sh"]
        "python scripts/bench.py --runs 15"                  → ["bench.py"]
        "ASSIGNMENT_STEP_TIMER=/tmp/x python scripts/m.py"   → ["m.py"]
        ""                                                   → []
    """
    if not cmd:
        return []
    interpreters = {"python", "python3", "node", "bash", "sh", "uv", "poetry", "pipenv"}
    out: list[str] = []
    for sub in re.split(r"\s*(?:&&|\|\||;|\|)\s*", cmd):
        sub = sub.strip()
        if not sub:
            continue
        tokens = sub.split()
        # Skip leading env-var assignments (VAR=value) and flags (-x / --flag)
        primary: str | None = None
        rest_idx = 0
        for i, t in enumerate(tokens):
            if t.startswith("-"):
                continue
            if "=" in t and not t.startswith("./") and not t.startswith("/"):
                continue
            primary = t
            rest_idx = i + 1
            break
        if not primary:
            continue
        basename = Path(primary).name
        # If it's an interpreter, the script path is the first non-flag token after it
        if basename in interpreters:
            for t in tokens[rest_idx:]:
                if t.startswith("-"):
                    continue
                if "=" in t and not t.startswith("./") and not t.startswith("/"):
                    continue
                out.append(Path(t).name)
                break
        else:
            out.append(basename)
    # De-duplicate preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for bn in out:
        if bn and bn not in seen:
            seen.add(bn)
            unique.append(bn)
    return unique


def build_harness_protocol_section(
    gate_basenames: list[str],
    measure_basenames: list[str],
    agent_cmds: list[str] | None = None,
) -> str:
    """Return a boilerplate block to append to the agent's prompt.

    Explicitly lists which commands the agent MUST NOT run (the ones the harness owns),
    plus the categories of checks it MAY run for fast in-session feedback. The agent
    sees this regardless of what the user's prompt says, so a user prompt that
    accidentally encourages iterative measurement is overridden here.

    When `agent_cmds` is non-empty (from `agent_test_commands` in the TOML), the
    repo-specific list appears under MAY run alongside the generic categories.
    """
    must_not = sorted({*gate_basenames, *measure_basenames})
    must_not_block = (
        "\n".join(f"  - {bn}" for bn in must_not) if must_not else "  (none configured)"
    )
    agent_cmds_block = ""
    if agent_cmds:
        agent_cmds_lines = "\n".join(f"  - `{c}`" for c in agent_cmds)
        agent_cmds_block = f"\nRepo-specific fast commands available to you:\n{agent_cmds_lines}\n"
    return f"""
---
HARNESS PROTOCOL (automatically appended by ai-agent-bench — follow strictly)

You MAY run (fast in-session feedback to self-correct while you work):
  - unit / integration tests targeting the specific files you are editing
  - type-check / lint (e.g. `tsc --noEmit`, `ruff check`, `mypy`, `eslint`)
{agent_cmds_block}
You MUST NOT run (the harness owns these; re-running them from your session
inflates wall time, contaminates measurement due to CPU contention, and
duplicates work the orchestrator will do with clean conditions):
{must_not_block}
  - any full regression / E2E / VP suite configured as the project gate
  - any profiling tool (cProfile, pyinstrument, hyperfine, STEP_TIMER / PROFILE env knobs)

These commands are the harness's `gate_cmd` and `measure_cmd`. The orchestrator will
execute them on HEAD before your session (baseline) and in your worktree after your
session (post). If the user's prompt above contradicts this section, follow this
section — it is the evaluation protocol.
"""


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_config(path: Path) -> dict:
    if not path.exists():
        die(f"config file not found: {path}")
    with path.open("rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# Agent invocation
# ---------------------------------------------------------------------------


def build_agent_command(agent: str, prompt: str, worktree: Path, run_dir: Path) -> list[str]:
    if agent == "claude":
        return [
            "claude",
            "-p",
            prompt,
            "--output-format",
            "stream-json",
            "--include-partial-messages",
            "--include-hook-events",
            "--verbose",
            "--dangerously-skip-permissions",
            "--add-dir",
            str(worktree),
        ]
    if agent == "codex":
        # `codex exec` is non-interactive by design (no approval prompts); --sandbox
        # workspace-write lets the agent edit files inside the worktree.
        return [
            "codex",
            "exec",
            "--json",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--output-last-message",
            str(run_dir / "last_message.txt"),
            "--cd",
            str(worktree),
            prompt,
        ]
    if agent == "opencode":
        # TODO: real OpenCode invocation. For now we capture nothing meaningful and emit a stub
        # session.jsonl so downstream aggregation still produces a report.
        return ["bash", "-c", 'echo \'{"type":"opencode_stub","note":"parser not implemented"}\'']
    raise ValueError(f"unknown agent: {agent}")


def run_agent_session(agent: str, prompt: str, worktree: Path, run_dir: Path) -> tuple[int, int]:
    """Run the agent CLI, writing session.jsonl. Returns (exit_code, wall_seconds)."""
    cmd = build_agent_command(agent, prompt, worktree, run_dir)
    session_path = run_dir / "session.jsonl"
    stderr_path = run_dir / "stderr.log"

    time_bin = "/usr/bin/time"
    use_time = os.access(time_bin, os.X_OK)
    if use_time:
        cmd = [time_bin, "-l", *cmd]

    start = time.time()
    with session_path.open("w") as out, stderr_path.open("w") as err:
        # Run with cwd=worktree for agents that don't accept an explicit --cd flag (claude uses
        # --add-dir; codex uses --cd). Extra cwd does not hurt.
        p = subprocess.run(cmd, cwd=str(worktree), stdout=out, stderr=err)
    wall = int(time.time() - start)
    return p.returncode, wall


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo", type=Path, required=True, help="target repository (absolute path)"
    )
    parser.add_argument("--config", type=Path, required=True, help="path to .ai-agent-bench.toml")
    parser.add_argument("--agent", choices=["claude", "codex", "opencode"], required=True)
    parser.add_argument("--run", required=True, help="run id/label (e.g. 1, 2, or a free label)")
    parser.add_argument(
        "--output-base", type=Path, help="override output base (default: <repo>/eval-results)"
    )
    parser.add_argument("--skip-baseline", action="store_true")
    parser.add_argument("--skip-post", action="store_true")
    parser.add_argument("--skip-gate", action="store_true")
    parser.add_argument("--skip-gate-preflight", action="store_true")
    parser.add_argument("--skip-agent", action="store_true", help="harness dry-run only")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not (repo / ".git").exists():
        die(f"not a git repository: {repo}")

    cfg = load_config(args.config.resolve())
    task_name = cfg.get("name") or "task"
    start_commit = cfg.get("start_commit") or "HEAD"
    prompt_file = cfg.get("prompt_file")
    if not prompt_file:
        die("config missing `prompt_file`")
    prompt_path = (
        (repo / prompt_file).resolve() if not Path(prompt_file).is_absolute() else Path(prompt_file)
    )
    if not prompt_path.exists():
        die(f"prompt file not found: {prompt_path}")
    prompt_text = prompt_path.read_text()

    measure_cmd = cfg.get("measure_cmd")
    gate_cmd = cfg.get("gate_cmd")
    pre_hooks = cfg.get("pre_hooks") or []
    agent_test_commands = cfg.get("agent_test_commands") or []

    # Resolve start_commit to a concrete SHA so the branch name and diff base are stable.
    rc, sha, err = run_capture(["git", "rev-parse", start_commit], cwd=repo)
    if rc != 0:
        die(f"could not resolve start_commit '{start_commit}': {err.strip()}")
    start_commit_sha = sha.strip()

    # Layout (dir creation deferred until after preflight checks so aborted runs don't leave
    # empty skeletons behind).
    output_base = (args.output_base or (repo / "eval-results")).resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_base / task_name / args.agent / f"run-{args.run}-{timestamp}"

    branch_name = f"eval-{args.agent}-run{args.run}-{timestamp}"
    worktree = repo / f".worktree-eval-{args.agent}-run{args.run}"

    print("=" * 72)
    print("  ai-agent-bench — trial")
    print("=" * 72)
    print(f"  Task:        {task_name}")
    print(f"  Agent:       {args.agent}")
    print(f"  Run ID:      {args.run}")
    print(f"  Repo:        {repo}")
    print(f"  Start:       {start_commit_sha[:12]} ({start_commit})")
    print(f"  Worktree:    {worktree}")
    print(f"  Branch:      {branch_name}")
    print(f"  Run dir:     {run_dir}")
    print(f"  Measure:     {measure_cmd or '(none)'}")
    print(f"  Gate:        {gate_cmd or '(none)'}")
    print("=" * 72)

    # ----------------------------- Preflight: CLI --------------------------
    if not args.skip_agent:
        cli_map = {"claude": "claude", "codex": "codex", "opencode": "opencode"}
        needed = cli_map[args.agent]
        if args.agent != "opencode" and which(needed) is None:
            die(
                f"{needed} CLI not found in PATH. Install it first or use --skip-agent for a harness dry-run."
            )

    # --------------------- Preflight: repo is clean ------------------------
    rc, stdout, _ = run_capture(["git", "status", "--porcelain"], cwd=repo)
    if stdout.strip():
        die(
            "target repo has uncommitted changes. Commit, stash, or clean the working tree "
            "first — the worktree is created from a specific commit and stray changes would "
            "pollute the trial."
        )

    # All preflight passed — now create the run dir and persist static metadata.
    run_dir.mkdir(parents=True, exist_ok=True)

    # Extract basenames from gate_cmd / measure_cmd so the agent's prompt can be
    # auto-annotated with a "MUST NOT run these" section, and so parse_transcript.py
    # can detect harness-duplication events in the agent's session.
    gate_basenames = extract_command_basenames(gate_cmd)
    measure_basenames = extract_command_basenames(measure_cmd)
    (run_dir / "harness_commands.json").write_text(
        json.dumps(
            {
                "gate_cmd": gate_cmd,
                "measure_cmd": measure_cmd,
                "gate_basenames": gate_basenames,
                "measure_basenames": measure_basenames,
            },
            indent=2,
        )
        + "\n"
    )

    resolved_prompt = prompt_text.replace("{{START_COMMIT}}", start_commit_sha)
    resolved_prompt += build_harness_protocol_section(
        gate_basenames, measure_basenames, agent_test_commands
    )
    (run_dir / "start_commit.txt").write_text(start_commit_sha + "\n")
    (run_dir / "branch_name.txt").write_text(branch_name + "\n")
    (run_dir / "prompt_resolved.md").write_text(resolved_prompt)
    update_status(run_dir, "init")

    # --------------------- Preflight: gate on HEAD -------------------------
    if gate_cmd and not args.skip_gate and not args.skip_gate_preflight:
        update_status(run_dir, "gate_preflight")
        print("\n[1/7] Gate preflight on HEAD — validating gate_cmd is usable as baseline...")
        preflight_log = run_dir / "gate_preflight.log"
        with preflight_log.open("w") as log:
            p = subprocess.run(gate_cmd, shell=True, cwd=str(repo), stdout=log, stderr=log)
        (run_dir / "gate_preflight_exit_code.txt").write_text(str(p.returncode) + "\n")
        if p.returncode != 0:
            print(f"  ✗ gate preflight FAILED (exit {p.returncode}). See {preflight_log}")
            print("  The trial cannot proceed: the gate must pass on HEAD to be a valid baseline.")
            return 3
        print(f"  ✓ gate preflight passed (exit 0). Log: {preflight_log.name}")

    # ----------------------------- Worktree --------------------------------
    update_status(run_dir, "worktree")
    print(f"\n[2/7] Creating worktree at {start_commit_sha[:12]}...")
    run_capture(["git", "worktree", "prune"], cwd=repo)
    if worktree.exists():
        run_capture(["git", "worktree", "remove", "--force", str(worktree)], cwd=repo)
        if worktree.exists():
            shutil.rmtree(worktree)
    rc, _, err = run_capture(
        ["git", "worktree", "add", "-b", branch_name, str(worktree), start_commit_sha], cwd=repo
    )
    if rc != 0:
        die(f"git worktree add failed: {err.strip()}")
    print(f"  ✓ worktree at {worktree}")
    print(f"  ✓ branch:    {branch_name}")

    # Trap cleanup: remove worktree dir but preserve branch (that's git's default behavior).
    def cleanup():
        if worktree.exists():
            print(f"\n  cleanup: removing worktree {worktree} (branch {branch_name} preserved)")
            rc, _, _ = run_capture(
                ["git", "worktree", "remove", "--force", str(worktree)], cwd=repo
            )
            if rc != 0 and worktree.exists():
                shutil.rmtree(worktree, ignore_errors=True)

    def handle_signal(signum, _frame):
        cleanup()
        sys.exit(128 + signum)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    exit_code = 0
    try:
        # --------------------------- Pre-hooks -----------------------------
        if pre_hooks:
            print(f"\n[3/7] Pre-hooks ({len(pre_hooks)})...")
            hook_log = run_dir / "pre_hooks.log"
            with hook_log.open("w") as log:
                for i, hook in enumerate(pre_hooks):
                    cmd = expand_placeholders(hook, repo=repo, worktree=worktree, run_dir=run_dir)
                    log.write(f"\n--- hook[{i}]: {cmd}\n")
                    log.flush()
                    p = subprocess.run(cmd, shell=True, cwd=str(worktree), stdout=log, stderr=log)
                    if p.returncode != 0:
                        print(f"  ✗ hook[{i}] failed (exit {p.returncode}): {cmd}")
                        print(f"    log: {hook_log}")
                        die("pre-hook failed — aborting trial")
            print(f"  ✓ {len(pre_hooks)} hooks executed")
        else:
            print("\n[3/7] No pre-hooks configured")

        # --------------------------- Baseline ------------------------------
        if measure_cmd and not args.skip_baseline:
            update_status(run_dir, "baseline")
            print("\n[4/7] Baseline measurement...")
            cmd = expand_placeholders(measure_cmd, repo=repo, worktree=worktree, run_dir=run_dir)
            baseline_path = run_dir / "baseline.json"
            stderr_path = run_dir / "baseline.stderr.log"
            with baseline_path.open("w") as out, stderr_path.open("w") as err:
                p = subprocess.run(cmd, shell=True, cwd=str(worktree), stdout=out, stderr=err)
            if p.returncode != 0:
                print(f"  ✗ baseline measure FAILED (exit {p.returncode}). See {stderr_path}")
                print("  Continuing — baseline JSON will be treated as missing downstream.")
            else:
                print(f"  ✓ baseline written to {baseline_path}")
        else:
            print("\n[4/7] Baseline skipped")

        # --------------------------- Agent session -------------------------
        agent_exit = 0
        if not args.skip_agent:
            update_status(run_dir, "agent:running")
            print(f"\n[5/7] Running agent: {args.agent}...")
            agent_exit, agent_wall = run_agent_session(
                args.agent, resolved_prompt, worktree, run_dir
            )
            (run_dir / "session_wall_seconds.txt").write_text(str(agent_wall) + "\n")
            (run_dir / "agent_exit_code.txt").write_text(str(agent_exit) + "\n")
            print(f"  ✓ agent exited {agent_exit}, wall {agent_wall}s")
        else:
            print("\n[5/7] Agent skipped")
            (run_dir / "session.jsonl").write_text("")  # empty so downstream doesn't complain

        # Fail-fast on non-zero agent exit: post-measurement and gate on unmodified code
        # would be misleading (they'd measure the baseline a second time and "pass" the gate).
        # Capture the diff (expected empty) so inspection is still possible, then abort.
        if agent_exit != 0:
            update_status(run_dir, "agent_failed")
            stderr_log = run_dir / "stderr.log"
            session_log = run_dir / "session.jsonl"
            (run_dir / "run_status.txt").write_text("failed_agent_session\n")
            (run_dir / "run_failure_summary.txt").write_text(
                "Agent session failed before downstream verification.\n"
                f"agent={args.agent}\n"
                f"exit_code={agent_exit}\n"
                f"wall_seconds={agent_wall}\n"
                f"stderr_log={stderr_log}\n"
                f"session_jsonl={session_log}\n"
            )
            run_capture(["git", "add", "-A"], cwd=worktree)
            _, diff_patch, _ = run_capture(
                ["git", "diff", start_commit_sha, "--staged"], cwd=worktree
            )
            (run_dir / "diff.patch").write_text(diff_patch)
            (run_dir / "gate_exit_code.txt").write_text("skipped_agent_failed\n")
            print("")
            print("=== Aborting after agent failure ===")
            print("  Skipping post measurement, gate, and parse.")
            print(f"  See: {stderr_log}")
            update_status(run_dir, "done")
            return agent_exit

        # --------------------------- Diff + snapshot commit ----------------
        update_status(run_dir, "diff")
        print("\n[6/7] Capturing diff + snapshot commit...")
        run_capture(["git", "add", "-A"], cwd=worktree)
        _, diff_patch, _ = run_capture(["git", "diff", start_commit_sha, "--staged"], cwd=worktree)
        (run_dir / "diff.patch").write_text(diff_patch)
        _, diff_stat, _ = run_capture(
            ["git", "diff", start_commit_sha, "--staged", "--stat"], cwd=worktree
        )
        (run_dir / "diff_stat.txt").write_text(diff_stat)
        _, commits, _ = run_capture(
            ["git", "log", "--oneline", f"{start_commit_sha}..HEAD"], cwd=worktree
        )
        (run_dir / "commits.txt").write_text(commits)

        rc, _, _ = run_capture(["git", "diff", "--cached", "--quiet"], cwd=worktree)
        if rc != 0:
            # There are staged changes to snapshot.
            run_capture(
                [
                    "git",
                    "-c",
                    "user.name=agent-eval",
                    "-c",
                    "user.email=agent-eval@local",
                    "-c",
                    "commit.gpgsign=false",
                    "commit",
                    "--no-verify",
                    "-m",
                    f"eval: {args.agent} run-{args.run} snapshot ({timestamp})",
                ],
                cwd=worktree,
            )
            print(f"  ✓ snapshot committed on branch {branch_name}")
        else:
            print("  - agent made no changes; no snapshot commit")

        # --------------------------- Post measurement ----------------------
        if measure_cmd and not args.skip_post:
            update_status(run_dir, "post")
            print("\n[7a/7] Post measurement...")
            cmd = expand_placeholders(measure_cmd, repo=repo, worktree=worktree, run_dir=run_dir)
            post_path = run_dir / "post.json"
            stderr_path = run_dir / "post.stderr.log"
            with post_path.open("w") as out, stderr_path.open("w") as err:
                p = subprocess.run(cmd, shell=True, cwd=str(worktree), stdout=out, stderr=err)
            if p.returncode != 0:
                print(f"  ✗ post measure FAILED (exit {p.returncode}). See {stderr_path}")
            else:
                print(f"  ✓ post written to {post_path}")
        else:
            print("\n[7a/7] Post skipped")

        # --------------------------- Gate ----------------------------------
        if gate_cmd and not args.skip_gate:
            update_status(run_dir, "gate")
            print("\n[7b/7] Gate...")
            cmd = expand_placeholders(gate_cmd, repo=repo, worktree=worktree, run_dir=run_dir)
            gate_log = run_dir / "gate.log"
            with gate_log.open("w") as log:
                p = subprocess.run(cmd, shell=True, cwd=str(worktree), stdout=log, stderr=log)
            (run_dir / "gate_exit_code.txt").write_text(str(p.returncode) + "\n")
            if p.returncode == 0:
                print("  ✓ gate PASSED")
            else:
                print(f"  ✗ gate FAILED (exit {p.returncode}). See {gate_log}")
        else:
            print("\n[7b/7] Gate skipped")
            (run_dir / "gate_exit_code.txt").write_text("skipped\n")

        # --------------------------- Parse + report ------------------------
        update_status(run_dir, "parse")
        print("\n[parse] Aggregating metrics + rendering report...")
        parse_script = SCRIPT_DIR / "parse_transcript.py"
        parse_cmd = [
            sys.executable,
            str(parse_script),
            "--agent",
            args.agent,
            "--run-dir",
            str(run_dir),
            "--output",
            str(run_dir / "metrics.json"),
            "--render-report",
            str(run_dir / "report.md"),
        ]
        p = subprocess.run(parse_cmd, capture_output=True, text=True)
        if p.returncode != 0:
            print(f"  ✗ parse failed: {p.stderr}")
            exit_code = 1
        else:
            print("  ✓ metrics.json + report.md written")

        update_status(run_dir, "done")

    finally:
        cleanup()

    # --------------------------- Summary --------------------------------
    print("\n" + "=" * 72)
    print("  TRIAL COMPLETE")
    print("=" * 72)
    print(f"  Run dir:  {run_dir}")
    print(f"  Report:   {run_dir / 'report.md'}")
    print(f"  Branch:   {branch_name}  ← preserved (not auto-deleted)")
    print(f"  Inspect:  git checkout {branch_name}")
    print(f"  Diff:     git diff {start_commit_sha[:12]} {branch_name}")
    gec = (
        (run_dir / "gate_exit_code.txt").read_text().strip()
        if (run_dir / "gate_exit_code.txt").exists()
        else "-"
    )
    print(f"  Gate:     exit={gec}")
    print("=" * 72)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
