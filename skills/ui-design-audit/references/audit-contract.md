# UI audit contract

Code and screenshot audits use the same severities:

- **CRITICAL:** accessibility blocker or confirmed WCAG 2.2 AA failure.
- **HIGH:** semantic or structural problem that misleads or excludes a user.
- **MEDIUM:** meaningful consistency problem. Drop anything lower.

Evidence is **Confirmed**, **Approximate**, or **Structural**.
Label approximate or structural evidence and name the browser, interaction, or measurement needed.

Each finding needs an anchor, defect, impact, and fix. Accessibility findings also cite WCAG.
Merge repeated findings with up to three examples and a count. Sort by severity and link shared root causes.

State evidence limits.
Code cannot prove final rendering or interaction. Screenshots cannot prove semantics, focus, responsiveness, or hidden states.

Audits never edit.
Fix later through the normal development workflow, grouping isolated findings and verifying cascading changes individually.
Suggest at most one complementary source that closes a real gap.
