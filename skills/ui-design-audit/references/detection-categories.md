# Code audit categories

Use only findings proved by the source. Project conventions override defaults.

| Category | Severity | Evidence | Cascade |
|---|---|---|---|
| Non-semantic interactive element, missing name or alt text, keyboard trap | CRITICAL | Element and handlers or attributes | Isolated |
| Confirmed contrast failure, color-only state, invisible focus, undersized target | CRITICAL | Resolved values or structural code | Cascading |
| Misleading action hierarchy, routine styling for destructive action, ambiguous label | HIGH | Control and nearby context | Cascading |
| Broken heading or landmark order, or an unnamed region | HIGH | Rendered structure in code | Cascading |
| Content hidden by fixed dimensions or overflow, or missing async state | HIGH | Layout and data branches | Cascading |
| The same role has inconsistent implementations | MEDIUM | Two or more concrete instances | Cascading |
| Value bypasses established project tokens or the component theme | MEDIUM | Exact style declaration | Isolated |
| One component mixes icon libraries or dark-mode strategies | MEDIUM | Imports and usage | Isolated |
| A data column uses a cryptic label | MEDIUM | Column declaration and domain context | Isolated |

Label estimated contrast or dimensions **Approximate**.
Do not report a raw value when the project has no token for that choice.
For repeated findings, show up to three anchors and the remaining count.
Code cannot confirm optical alignment, final responsive hierarchy, computed contrast in every theme, or interaction behavior.
