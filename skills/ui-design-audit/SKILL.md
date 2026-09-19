---
name: ui-design-audit
description: "Audit UI code or a screenshot for visual consistency and WCAG 2.2 AA issues; return a severity-ranked report without editing."
argument-hint: "[path | image]"
user-invocable: true
---

# UI design audit

State the target and report-only scope. Read the [audit contract](references/audit-contract.md) and applicable project design rules.

For code, skip generated and vendored paths.
Identify the project's design tokens, component library, and intentional exceptions before applying [code categories](references/detection-categories.md).
Anchor findings to `file:line`; cross-file claims need evidence from each file.

For PNG, JPG, WebP, or an attachment, inspect one frame with [render categories](references/render-categories.md) and named regions.
URLs and design tools need a saved screenshot. Ask for a local image when none is available.

Report only CRITICAL, HIGH, and MEDIUM findings, evidence limits, and isolated versus cascading fixes.
Do not edit. Offer a complementary code or screenshot pass only when it closes a real evidence gap.
