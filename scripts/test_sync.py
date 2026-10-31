"""Check startup context and benchmark pricing selection."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class StartupContextTest(unittest.TestCase):
    def test_all_context_parts_are_registered(self):
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text())
        commands = hooks["hooks"]["SessionStart"][0]["hooks"]
        self.assertEqual(len(commands), 3)
        self.assertTrue(commands[1]["command"].endswith(" loop"))
        self.assertTrue(commands[2]["command"].endswith(" engineering"))

    def test_hooks_deliver_complete_contracts(self):
        for argument, tag, source in (
            (None, "WRITING-CONTRACT", "shared/writing.md"),
            ("loop", "DEVELOPMENT-LOOP", "shared/development-loop.md"),
            ("engineering", "ENGINEERING-CONTRACT", "shared/engineering.md"),
        ):
            with self.subTest(argument=argument):
                command = [str(ROOT / "hooks/session-start")]
                if argument:
                    command.append(argument)
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
                self.assertIn(f"<{tag}>", context)
                self.assertIn((ROOT / source).read_text().splitlines()[-1], context)
                self.assertLess(len(context), 10000)


class PricingTest(unittest.TestCase):
    def test_longest_model_prefix_wins(self):
        path = ROOT / "skills/ai-agent-bench/scripts/parse_transcript.py"
        spec = importlib.util.spec_from_file_location("parse_transcript", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def rates(value):
            return dict.fromkeys(
                ("input", "output", "cache_read", "cache_creation_5m", "cache_creation_1h"), value
            )

        pricing = {"model": rates(1), "model-pro": rates(2)}
        self.assertEqual(
            module.estimate_cost_usd("model-pro-dated", {"input": 1_000_000}, pricing), 2
        )


class LegacyDocumentTest(unittest.TestCase):
    def test_renamed_legacy_plan_keeps_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "docs/plans/archive"
            archive.mkdir(parents=True)
            plan = archive / "2020-01-01__example.md"
            plan.write_text("# Plan\n\n- [ ] Pending work\n")
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    str(ROOT / "scripts/check_docs.py"),
                    directory,
                    "--legacy-before",
                    "2021-01-01",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("WARNING", result.stdout)
            plan.rename(archive / "2022-01-01__example.md")
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    str(ROOT / "scripts/check_docs.py"),
                    directory,
                    "--legacy-before",
                    "2021-01-01",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ERROR", result.stdout)


class RenameDocumentsTest(unittest.TestCase):
    def test_apply_reports_unresolved_citation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            plan = root / "docs/plans/0001__2020-01-01__example.md"
            plan.parent.mkdir(parents=True)
            plan.write_text("# Example\n")
            (root / "README.md").write_text("See plan 0001.\n")
            subprocess.run(["git", "-C", directory, "add", "."], check=True)
            result = subprocess.run(
                ["uv", "run", str(ROOT / "scripts/rename_numbered_docs.py"), directory, "--apply"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("CITATION README.md", result.stdout)

    def test_preview_and_apply_preserve_references(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            plan = root / "docs/plans/0001__2020-01-01__example.md"
            plan.parent.mkdir(parents=True)
            plan.write_text("# Example\n")
            readme = root / "README.md"
            readme.write_text("See docs/plans/0001__2020-01-01__example.md\n")
            subprocess.run(["git", "-C", directory, "add", "."], check=True)
            command = ["uv", "run", str(ROOT / "scripts/rename_numbered_docs.py"), directory]
            preview = subprocess.run(command, capture_output=True, text=True, check=True)
            self.assertIn("RENAME", preview.stdout)
            self.assertTrue(plan.exists())
            subprocess.run(command + ["--apply"], capture_output=True, text=True, check=True)
            self.assertFalse(plan.exists())
            self.assertTrue((plan.parent / "2020-01-01__example.md").exists())
            self.assertIn("docs/plans/2020-01-01__example.md", readme.read_text())

    def test_untracked_nested_record_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "init", "-q", directory], check=True)
            path = Path(directory) / "docs/plans/0001__2020-01-01__folder/0002__nested.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Nested\n")
            result = subprocess.run(
                ["uv", "run", str(ROOT / "scripts/rename_numbered_docs.py"), directory],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("UNRESOLVED", result.stdout)


if __name__ == "__main__":
    unittest.main()
