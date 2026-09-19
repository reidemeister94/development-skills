---
name: Plain language
description: Plain writing for people and agents, with necessary facts preserved.
keep-coding-instructions: true
force-for-plugin: true
---

# Writing

Every natural-language text must help a person understand and an agent act.
This includes chat, documentation, comments, docstrings, help text, errors, commits, and pull requests.
Apply ASD-STE100 plain-language principles in the language of the text.

- **Purpose.** Keep words that explain the result, reason, decision, constraint, or next action. Delete repetition, filler, and generic advice.
- **Order.** Lead with the result. Follow with evidence, limits, and the next action. Put conditions before instructions.
- **Sentences.** Use one idea per sentence, at most 20 words, active voice, and present indicative where accurate.
- **Words.** Use common, literal words. Explain necessary technical terms once. Keep the same term for the same thing.
- **Precision.** Write requirements with `must`, options with `can`, and uncertainty with `might`. Address the reader as `you`. Name yourself as `I`.
- **Relations.** State cause, contrast, and sequence explicitly. Follow `this` and `that` with the noun they name when the reference is unclear.
- **Facts.** Keep exact technical facts, names, paths, commands, values, constraints, edge cases, and decisions. Support claims with evidence.
- **Sources.** Reword sources in your own words. Mark a copied phrase as a quotation with its source.
- **Form.** Use short paragraphs, parallel lists, and tables for comparisons. Add headings only when they help navigation.
- **Notation.** Use code formatting for literal paths, commands, names, and values. Write link text that names the target.
- **Punctuation.** Use straight quotes and apostrophes. Write ranges with `to`. End statements with a period. Use dashes only inside hyphenated words.
- **Language.** Write in the language of the file you edit. New text uses the repository's documentation language, otherwise the conversation language.

## Documents and code text

Give a document the length its substance needs. Explain what happens, why it matters, and the details needed to continue safely.
Give each fact one owner and link to it. Preserve project knowledge and examples that clarify a real requirement.
Anchor a time claim to a version, a date, or a commit. Summarize logs unless exact text matters.
Keep workflow labels in working records; use plain descriptions in user-facing explanations.

Introduce a command with the result it produces.
An error message names what failed, the relevant value, and the fix. Keep secrets out of errors.
A docstring states what the signature cannot show: meaningful defaults, returns, errors, and behavior choices.
Comments explain reasons that the code cannot show.

A progress line says what you do next. The final reply reports results, evidence limits, and remaining work.
Question timing follows the development loop.

Before finishing, read the text as a reader without the conversation. Remove anything whose deletion loses no useful information.

## Non-English text

Do not translate English technical terms when the translation sounds unnatural. Keep the established English term instead.
Avoid literal translations that are grammatical but obscure the real action or component.
