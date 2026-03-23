# Project Directives and Guidelines

These directives are injected into the project's CLAUDE.md on first plugin trigger. They establish universal principles for any project, any developer.

---

## MANDATORY: Read Before Any Task - Directives and guidelines for working on this project (v0.0.1)

You are building a growing understanding of this project across conversations. Every task you complete is an opportunity to make the next task faster, more accurate, and less ambiguous. **Treat documentation as a first-class output of every task, not an afterthought.**

Simplicity criterion: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome — that's a simplification win. When evaluating whether to keep a change, weigh the complexity cost against the improvement magnitude.

### What to do during every task

1. **Document as you go.** Don't wait until the end. As you discover something useful — a pattern, a gotcha, a data shape, a naming convention, a workaround — write it down immediately in the appropriate place. If you're unsure where, default to CLAUDE.md for project-wide knowledge and MEMORY.md for cross-session context.

2. **Remove ambiguity for your future self.** If you had to investigate something to figure it out (e.g., what columns a DataFrame has, how an endpoint's request body is shaped, what mock targets to use, which database schema is for writes), that investigation cost should be paid only once. Write the answer where you'll find it next time.

3. **Use the right document for the right purpose:**

   | Document | Purpose | When to update |
   |----------|---------|----------------|
   | **CLAUDE.md** | Project-wide knowledge, conventions, patterns, reference data, rules. This is your primary briefing document — it's loaded every conversation. | When you discover something any future task might need: architectural patterns, API shapes, DB schemas, testing conventions, common gotchas |
   | **MEMORY.md** | Cross-session memory. Stable facts confirmed across interactions, user preferences, solution patterns. | When a pattern is confirmed (not speculative), when the user corrects you, when a preference is expressed |
   | **docs/plans/** | Implementation plans with task checklists, approach decisions, implementation logs. Follow the existing naming convention: `NNNN__YYYY-MM-DD__implementation_plan__slug.md` | When starting a non-trivial task (create plan), during execution (update checklist + log), at completion (mark status) |
   | **docs/chronicles/** | Narrative records of significant discoveries, debugging sessions, design decisions. | When something surprising or non-obvious happened that would be valuable to remember |
   | **Other docs/** | Domain documentation (overview, data model, workflows, API reference, glossary, configuration) | When you learn something about the business domain, data model, or external systems |

4. **Make CLAUDE.md a cheat sheet, not a novel.** Favor tables, code snippets, and direct statements over prose. The goal is: when a new conversation starts, you should be able to read CLAUDE.md and immediately know how to be effective — what tools to use, what patterns to follow, what pitfalls to avoid, where to find things and the peculiarities of the project. CLAUDE.md file must be totally signal and zero noise, don't write in it things that are not immediately actionable or universally relevant across tasks. Maximize the information density while minimize the amount of text and complexity.

5. **Keep documents aligned.** After completing a task, ensure all affected documents reflect the final state. Plans should have updated checklists and verification results. Don't duplicate the same information across documents — each has its own purpose.

Before every change, ask yourself:
  - did I check all the sources below and this change is aligned with the best practices, tips, patterns, and techniques described in those sources? If not, adjust the change until it is aligned.
  - does this change really improve the final code quality for the developer? if not, don't do it.
  - does this change really simplify the workflow and the developer experience, keeping the maximum code quality while minimizing complexity? if not, don't do it.
  - is there a simpler way to achieve the same result? if yes, do that instead.
