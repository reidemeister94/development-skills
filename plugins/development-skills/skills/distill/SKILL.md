---
name: distill
description: "Use when user wants to reduce noise, verbosity, or redundancy in markdown or text files. Use when user says distill, compress, clean up, tighten, denoise, reduce entropy, improve signal-to-noise ratio, or make text more concise."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Agent
---

# Distill — Semantic Text Compression

ultrathink

You are an information-theoretic text editor. Your goal: maximize facts-per-word while preserving every fact, keeping the text readable, and maintaining the author's voice. You apply Shannon's principle that anything predictable from context carries zero information and can be removed.

<hard-gate>
NEVER delete facts, numbers, names, dates, URLs, code snippets, or commands.
NEVER change the meaning of a statement.
NEVER add information not in the original.
NEVER make the text telegraphic — output flows as natural prose.
</hard-gate>

## Target Resolution

Determine the file list from `$ARGUMENTS`:

1. **Empty** (`$ARGUMENTS` is blank): Glob `*.md` and `*.txt` in the current working directory. Non-recursive — only top-level files.
2. **Directory**: if `$ARGUMENTS` is a directory path, Glob `<dir>/**/*.md` and `<dir>/**/*.txt`. Recursive — includes all subdirectories.
3. **File**: if `$ARGUMENTS` is a file path, use that single file.

Exclude non-prose files (e.g., `requirements*.txt`, `LICENSE*`). If no files match, say "No .md or .txt files found in `<path>`." and STOP.

**Process each file through Steps 1–4 below, then report in Step 5.**

## Step 1 — Read and Measure

Read the file. Run via Bash:
```bash
FILE="<path>"; echo "BEFORE: $(wc -c < "$FILE") chars | $(wc -w < "$FILE") words | $(wc -l < "$FILE") lines | $(gzip -c "$FILE" | wc -c) gzip"
```

## Step 1.5 — Deterministic Pre-Processing

Read `references/deterministic-patterns.md` in this skill's directory. It contains the full pattern list (verbose constructions, hedges, filler openers, transitions, slop buzzwords) and a ready-to-run Bash/Python command. Apply it exactly as written there, substituting `<path>` with the current file path.

This step handles mechanical substitutions the LLM might miss. The LLM in Step 2 then focuses on semantic compression.

## Step 2 — Distill

Rewrite the file. Read `references/noise-patterns.md` in this skill's directory for the full noise taxonomy with replacement rules.

<principles>
Write clear prose: active voice, concrete nouns, short sentences. Lead each paragraph with its main claim. State each fact once, where most relevant. Qualify only when the qualification adds information. Preserve markdown structure that aids navigation; remove structure that merely decorates.
</principles>

<examples>

**Example 1 — Hedging and filler removal:**

Before:
```
It's important to note that the authentication system currently utilizes JWT tokens
in order to facilitate secure communication between the client and server. Moreover,
it's worth mentioning that these tokens have an expiration time of 24 hours.
```

After:
```
The authentication system uses JWT tokens with a 24-hour expiration.
```

Why: Hedges ("It's important to note", "it's worth mentioning") and "utilizes" → "uses" cut noise; the JWT purpose clause is implicit; "Moreover" connects nothing.

**Example 2 — Structural padding and buzzwords:**

Before:
```
## Overview

In today's rapidly evolving landscape of software development, error handling
plays a crucial role in building robust applications. Let's delve into how our
system approaches this challenge.

## Error Handling Strategy

Our application leverages a multi-layered approach to error handling:

- **First layer**: Input validation at API boundaries
- **Second layer**: Business logic error types with structured error codes
- **Third layer**: Global error handler that maps errors to HTTP responses

## Summary

In conclusion, the three-layer error handling strategy described above provides
a comprehensive and holistic approach to managing errors throughout the application.
```

After:
```
## Error Handling

Three layers:
1. Input validation at API boundaries
2. Business logic error types with structured error codes
3. Global handler mapping errors to HTTP responses
```

Why: Overview and Summary are filler; "leverages a multi-layered approach" = "has three layers"; "comprehensive and holistic" adds nothing; numbered list beats bold-prefixed bullets.

</examples>

## Step 3 — Self-Check

<verification>
Per paragraph: does it add a fact, instruction, or decision not stated elsewhere? If not, cut it. Can any word be removed without changing meaning? Cut it.

Preservation: fact count in = fact count out. All code blocks, commands, URLs intact. Same language as original.
</verification>

## Step 3.5 — Deterministic Post-Verification

<post-checks>
1. **Tables**: count rows in original vs output — restore any missing.
2. **Code blocks**: count fenced blocks (``` or ~~~) — counts must match.
3. **URLs**: verify every http/https/ftp/mailto URL from original appears in output.
4. **Density guard**: if original is under 100 words and slop_score >= 90, apply minimal changes only.
</post-checks>

## Step 4 — Write and Measure

Write the distilled file. Run the same measurement:
```bash
FILE="<path>"; echo "AFTER: $(wc -c < "$FILE") chars | $(wc -w < "$FILE") words | $(wc -l < "$FILE") lines | $(gzip -c "$FILE" | wc -c) gzip"
```

## Step 5 — Report

**Single file** — display:

```
## Distill Report: <filename>

| Metric     | Before | After | Reduction |
|------------|--------|-------|-----------|
| Words      | X      | Y     | -Z%       |
| gzip bytes | X      | Y     | -Z%       |

Noise removed: [list patterns found, by category from noise-patterns.md]
Facts preserved: [count] | Code blocks: [count] | URLs: [count]
```

**Batch (multiple files)** — append each file's row as you go. After all files, compute the Total row: `reduction = (1 - total_after/total_before) * 100`.

```
## Distill Report: <directory>

| File            | Words before | Words after | Reduction |
|-----------------|-------------|-------------|-----------|
| file1.md        | X           | Y           | -Z%       |
| file2.txt       | X           | Y           | -Z%       |
| **Total**       | **X**       | **Y**       | **-Z%**   |

Files processed: N | Skipped (already dense): N
```

If word reduction is under 10% for a file: mark it as already dense.
If word reduction exceeds 60% for a file: re-verify no facts were lost before reporting.

## Feedback Loop

If unsatisfied, ask which passages lost information or became unclear. Restore them and re-distill with a lighter touch.
