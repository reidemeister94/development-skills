# Writing

Every natural-language text written or edited must help a person understand and an agent act.

The rule covers:

- chat, documentation, plans, chronicles, research, reports, README files, and AGENTS files;
- comments, docstrings, help text, and error messages;
- changelogs, commit text, and pull request text.

And every other type of natural language text, written or spoken to the user.

## Serve both readers

Start with the explanation a teammate with little project knowledge needs:

- what is happening and why it matters;
- how the relevant part of the system works;
- what was learned or decided, with the reason;
- what changed and what that means.

Then give the working detail an agent needs:

- Keep exact technical facts, names, paths, commands, constraints, edge cases, and checks.
- Connect each piece of evidence to what it proves. Summarize raw logs unless their exact text matters.
- State uncertainty and remaining limits. Do not hide them behind process labels.

Human-first does not mean summary-only. Remove noise, not substance.

## Write naturally

- Use common, concrete words. Explain an uncommon technical or company term when it first matters.
- Prefer a direct explanation over labels such as “observable solved state”, “semantic boundary”, or “operative owner”.
- Workflow names are instructions for the agent, not explanations for the reader. Keep an exact workflow name only where a status field, command, or working record needs it. Everywhere else, translate `Full`, `Direct`, `RED`, and `GREEN` into ordinary language: say what work will happen, that a test fails before the fix, or that it passes afterward.
- Do the same for technical shorthand such as “truthy”, “fail closed”, or “boundary”. Use common words, or explain the term where it adds necessary precision.
- Keep one main idea in a sentence or list item. Split a sentence when its parts need different explanations.
- State what happened instead of narrating the agent’s process. Keep conversation history only when it records a decision that is not preserved elsewhere.
- Give each fact one owner. Link to that owner instead of repeating the same rule in several files.
- Keep an example only when it carries a real requirement or corrects an observed failure.

## Use formatting to aid reading

- Use paragraphs by default. Add headings when they help the reader navigate and lists when the content is truly a list.
- Do not use bold or italics only to add emphasis. Use code formatting only for literal names, values, paths, commands, or code.
- Use a table only for a real comparison or repeated mapping. Do not use one to make ordinary prose look structured.
- Remove empty sections, filler introductions, repeated conclusions, and template fields that add no information.

## Match the language

Keep the language already used by the file. For new text, follow the repository’s established documentation language. When none exists, use the language of the conversation. Preserve exact wording when it records a user, company, or domain decision.

## Check the result

Before finishing, read the text as a teammate who knows little about the project:

- Can they understand the subject, the reason, and the result without reconstructing the conversation?
- Can an agent find every detail needed to continue the work safely?
- Does each paragraph teach or record something useful?
- Would removing a sentence lose information, or only generated noise?
