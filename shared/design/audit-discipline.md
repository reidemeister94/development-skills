# Design audit contract

Both code and screenshot audits use the same severities:

- **CRITICAL:** accessibility blocker or confirmed WCAG 2.2 AA failure.
- **HIGH:** semantic or structural problem that misleads or excludes a user.
- **MEDIUM:** meaningful consistency problem. Drop anything lower.

Mark evidence **Confirmed**, **Approximate**, or **Structural**. Show the label only for the latter two and name the needed browser, interaction, or measurement check. Never present an approximation as measured fact.

Each finding contains an anchor, what is wrong, user impact, and a concrete fix. Accessibility findings cite the WCAG success criterion. Collapse repeated instances into one finding with up to three examples and a count. Sort by severity and connect findings that share one root cause.

Every report states what the input cannot prove. Code cannot prove final rendering or interaction; a screenshot cannot prove semantics, focus, responsive behavior, or hidden states.

Audits report only. If asked to fix everything, explain that visual changes can cascade and apply one agreed finding at a time through the relevant UI skill. End with isolated findings that can be grouped and cascading findings that need individual verification.
