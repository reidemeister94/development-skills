# Definition of Done — lock the problem and the proof

Before any code, two things must be unambiguous. This is a HARD lock: no implementation until both are agreed (for a LIGHT / PASS_THROUGH task they're usually self-evident — state them in one line and move on).

1. **The problem / task + specs** — exactly what to solve or build, the acceptance criteria, and what is explicitly out of scope. Vague intent (*"make it better"*, *"fix the bug"*, *"handle errors"*) is not a spec.
2. **The verification procedure** — the definitive, 0-ambiguity check that says DONE or NOT-DONE. Name the concrete observation: the command that must pass, the endpoint that must return X, the query that must yield N rows, the log line that must (not) appear, the screenshot that must show Y. It must be reproducible, binary (pass/fail), runnable by YOU for fresh evidence (iron rule 8), and tied to the real problem — not a proxy ("the linter is green" rarely proves the behavior).

If the user cannot state either clearly, do NOT proceed on a fuzzy target — reach clarity via brainstorming + **analysis of reality**, then confirm:

- read the codebase + docs to see how it actually works;
- query the live state — database via MCP, logs, real request/response data — to see what is actually true, not what is assumed;
- turn what you find into a concrete spec and a concrete check.

The verification procedure is the **Success** line of the brainstorming restate and the **Verification strategy** of the plan; phase-3 executes it and reports against it (PASS / COULD-NOT-RUN / FAIL, never a faked pass). A task whose done-check you cannot name is a task you do not yet understand — keep interviewing or analysing until you can.
