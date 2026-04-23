# Trial monitoring — heartbeat, overrun, stream-disconnect

Invoked from `SKILL.md` Step 4, during and after the `run_trial.py` invocation.

The trial is opaque from outside. These are the signals that distinguish "slow but
healthy" from "stuck / failing / degraded".

---

## Heartbeat — use `status.txt`, not file existence

`run_trial.py` writes `${run_dir}/status.txt` at each phase transition. Each line is:

```
<ISO timestamp>\t<phase>
```

Phases in order: `init`, `gate_preflight`, `worktree`, `baseline`, `agent:running`,
`diff`, `post`, `gate`, `parse`, `done`.

Read the LAST line to know the current phase. Every 3–5 minutes during `agent:running`,
tail this file and report progress to the user. Do not poll aggressively — check every
few minutes only.

**Do NOT infer phase from file existence alone.** Shell redirection creates empty output
files (`baseline.json`, `post.json`, `session.jsonl`) the instant the phase starts, so
`-f $RUN_DIR/baseline.json` is true long before baseline completes. Either read
`status.txt` or check both existence AND non-zero size.

---

## Per-trial timeout expectation

- Nominal: **60–150 minutes** per trial, depending on task + agent. Surface this range
  to the user before launching.
- Warn threshold: **150 minutes** elapsed.
- Recommend-terminate threshold: **240 minutes** elapsed while phase is still
  `agent:running`.

Compute wall time as `now - timestamp_of_first_status_line`.

---

## Overrun detection

At each heartbeat check:

- **wall > 150 min** → print a prominent warning:

  ```
  OVERRUN: trial has been running <N> min, above the 60–150 min expectation.
  Options: (1) wait, (2) inspect session.jsonl to see if the agent is progressing,
  (3) SIGTERM the trial (artifacts are preserved).
  ```

- **wall > 240 min AND `status.txt` last phase is `agent:running`** → recommend
  terminating. A healthy agent session rarely exceeds 4 h on a well-scoped task.
- **`session.jsonl` has not grown in size for >10 min while `agent:running`** → surface
  as "possible stall / stream disconnect".

Log any of these events to `AI_AGENT_BENCH_ANOMALIES.md` per the anomaly-logging policy.

---

## Codex stream-disconnect signal

Codex `exec --json` can emit:

```json
{"type":"error","message":"Reconnecting... 2/5 (stream disconnected before completion: idle timeout waiting for websocket)"}
```

during WebSocket idle timeouts. Not itself fatal — the agent usually continues. But if
events stop arriving for >10 min after a reconnect warning, the session is likely stuck.
Combine with the session.jsonl byte-growth signal for a reliable stall detection.

---

## Post-trial summary

After each trial:
- Print the run dir path.
- Print the branch name (from `branch_name.txt` in the run dir) plus the `git checkout`
  command.
- Print the `gate_exit_code.txt` result prominently (PASS / FAIL).
- If the gate failed, ask: *"Trial <agent> run <id> gate FAILED. Continue with remaining
  trials or stop?"*
