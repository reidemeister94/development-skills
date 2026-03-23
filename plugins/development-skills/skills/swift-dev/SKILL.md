---
name: swift-dev
description: "Swift development. Use for Swift, SwiftUI, UIKit, Vapor, SPM, XCTest, Combine."
user-invocable: true
allowed-tools: Glob, Read, Grep, Bash, Task, Skill, Edit, Write, EnterPlanMode
---

# Swift Development

**Announce:** "I'm using the swift-dev skill. Following the mandatory 7-phase workflow."

## MANDATORY: Read and Follow the Shared Workflow

**You MUST read [workflow.md](../../shared/workflow.md) NOW** and follow ALL 7 phases defined there. The sections below provide Swift-specific inputs for each phase.

Read [patterns.md](patterns.md) during Phase 1.

**If you lost workflow.md from context:** Re-read `../../shared/workflow.md` NOW before continuing.

---

## Swift-Specific Configuration

### Verification Commands (Phase 2 + Phase 5)

WORKFLOW STATE Verification line: `swift build, swift test, swiftlint`

**Phase 5 Tier A — SPM projects:**
- `swift build` — compilation
- `swift test` — tests
- `swiftlint` — linting (if configured)
- Coverage target: 70-80%

**Phase 5 Tier C — Xcode projects:**
- `xcodebuild build` or `xcodebuild test`
- SwiftUI: `xcodebuild build -scheme [scheme] -destination 'platform=iOS Simulator,name=iPhone 16'`

### Implementation Rules (Phase 4)

- **Model structure** — Structs with Codable CRUD variants per entity (CreateRequest/UpdateRequest/Response), domain-driven file organization, composition over deep inheritance, prefer structs over classes
- **Minimize complexity** — lazy sequences for large collections, Dictionary lookups over array scans
- **Preserve compatibility** — CodingKeys for renamed fields, default values for new properties, preserve public API signatures, @available for deprecations

### Staff Review Configuration (Phase 6)

- **Patterns file path:** Path to this skill's `patterns.md`

---

## Anti-Rationalization (Swift-Specific)

Add these to the shared workflow's anti-rationalization check:

| Your thought | Reality |
|---|---|
| "The Swift compiler catches everything" | The compiler catches type errors, not logic bugs, architectural problems, or performance issues. Verification and review are still mandatory. |
| "SwiftUI previews are enough verification" | Previews only prove the view compiles. They do not test business logic, async flows, or edge cases. Run `swift test`. |
| "This is just a UI tweak, no need for the full workflow" | UI changes affect architecture (view/model boundaries), testability, and accessibility. Follow the workflow. |

### Red Flags (Swift-Specific)

- Expressing satisfaction before running `swift test` or `swift build`
- Assuming the compiler will catch the issue without running verification

---

## Quality Checklist (Swift-Specific)

Add these to the shared workflow's verification checklist:

- [ ] Using Swift 5.9+ / Swift 6 features where appropriate
- [ ] Structs preferred over classes (value semantics by default)
- [ ] Protocol-oriented design used
- [ ] async/await for asynchronous code
- [ ] No force unwraps outside tests
- [ ] Proper error handling with typed throws or do/catch
- [ ] `swift build` succeeds without warnings
- [ ] `swift test` passes (or `xcodebuild test`)
- [ ] `swiftlint` passes (if configured)
