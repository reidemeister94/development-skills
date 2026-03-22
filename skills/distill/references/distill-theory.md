# Distill — Theoretical Foundations

The `/distill` skill applies information theory, academic NLP research, and classical writing principles to semantic text compression. This document covers every foundation, with sources.

## 1. Shannon's Information Theory (1948)

**Source:** Claude Shannon, [*A Mathematical Theory of Communication*](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), Bell System Technical Journal, 1948.

Shannon defines the **entropy** H(X) of an information source:

```
H(X) = -Σ p(xᵢ) · log₂ p(xᵢ)
```

The **Source Coding Theorem** states that a source cannot be compressed below its entropy without information loss. Everything above entropy is eliminable redundancy.

In 1951 ([*Prediction and Entropy of Printed English*](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf)), Shannon estimated English at ~1.0–1.5 bits/character out of a theoretical maximum of ~4.7 bits/char for a 27-symbol alphabet. This means ~70–80% of English text is structurally redundant — predictable from context.

Modern LLMs (GPT-4 class, Claude) lower this estimate to ~0.7–0.8 bits/character, suggesting even more redundancy than Shannon measured with human predictors.

**Application to distill:** The skill treats Shannon entropy as the theoretical compression floor. Anything above it is a candidate for removal. The gzip compression ratio serves as a measurable proxy — gzip implements LZ77 + Huffman coding, which approximates entropy from above. If gzip size drops after distillation, real redundancy was removed.

## 2. Verbosity Compensation in LLMs (Sun et al., 2025)

**Source:** Jie Sun et al., [*Verbosity ≠ Veracity: Demystify Verbosity Compensation Behavior of Large Language Models*](https://arxiv.org/abs/2411.07858), UncertaiNLP Workshop, ACL 2025.

This paper identifies **Verbosity Compensation (VC)** — a systematic behavior where LLMs, when uncertain, compensate by producing more words. Analogous to human hesitation.

### The five VC categories

| Type | Description | Example |
|------|-------------|---------|
| Ambiguity | Vague answer instead of precise | "It's quite large" instead of "3,029 entries" |
| Question repetition | Restates the question before answering | Paraphrases the problem without giving the answer |
| Enumeration | Lists all possibilities instead of selecting | "Could be A, B, C, D" when the answer is B |
| Verbose details | Excessive context around a simple fact | 3 paragraphs of background for a one-line answer |
| Verbose format | Unnecessary formatting | Excessive markdown, quotation marks, emphasis on non-key terms |

### Quantitative findings

- GPT-4 exhibits VC in **50.4%** of responses
- VC frequency ranges from 13.6% (Llama-3-70B) to 74% (Mistral-7B)
- Verbose responses are **27.6% less accurate** than concise ones
- Higher model uncertainty correlates with higher verbosity
- This performance gap does **not diminish** with more capable models — it is structural, tied to RLHF training objectives (annotators rate longer responses higher)

**Application to distill:** All five VC categories map directly to noise patterns in the skill's taxonomy. The finding that verbosity correlates with lower accuracy justifies aggressive noise removal — it improves both density and correctness.

## 3. LLM Slop Taxonomy

**Sources:**
- [TinyComputers.io — *What Makes Something Slop*](https://tinycomputers.io/posts/llm-generated-content-what-makes-something-slop.html)
- [AI Phrase Finder — Words That Identify AI](https://aiphrasefinder.com/words-that-identify-ai/)
- [Embryo — List of Words AI Overuses](https://embryo.com/blog/list-words-ai-overuses/)
- [Slop Radar](https://github.com/renefichtmueller/slop-radar) — 245 English buzzwords + structural pattern matching

The TinyComputers analysis identifies the core mechanism: slop is "grammatically flawless and semantically empty." It demonstrates structural competence without substance. The fundamental issue is the **commitment problem** — slop refuses to make falsifiable claims, avoiding positions that "could be challenged or argued against" through relentless qualification.

### The 10 noise categories in the skill

1. **Hedging language** — "It's important to note", "It's worth mentioning"
2. **Empty transitions** — "Moreover", "Furthermore", "Additionally"
3. **Empty conclusions** — "In summary", "In conclusion", "In essence"
4. **Filler openers** — "Certainly!", "Great question!", "Let me explain"
5. **Buzzword inflation** — delve, tapestry, landscape, realm, leverage, harness, paradigm, cutting-edge, holistic, synergy
6. **Verbose constructions** — "in order to" → "to", "due to the fact that" → "because", "is able to" → "can"
7. **Structural padding** — unnecessary headers, rigid essay format, decorative formatting
8. **Non-committal language** — "X can be Y" when you mean "X is Y", excessive hedging
9. **Repetition and redundancy** — same idea in different words, echo sentences
10. **Verbosity compensation** — the five academic categories from Sun et al.

## 4. High-Entropy Writing (Miessler, 2024)

**Source:** Daniel Miessler, [*High-Entropy Writing*](https://danielmiessler.com/blog/high-entropy-writing), 2024. Creator of [Fabric](https://github.com/danielmiessler/Fabric), an open-source AI framework with 140+ prompt patterns.

Miessler applies Shannon's entropy to writing, building on Derek Sivers' observation: "People only really learn when they're surprised."

High-entropy content **surprises** the reader. If every sentence says something the reader could have predicted, the entropy is zero — the text adds nothing.

The practical rule: for every piece of content, ask *"What's surprising here? What makes the reader say 'wow'?"* If the answer is nothing, cut it.

**Exception:** Frameworks combining known elements into novel, useful structures qualify as high-entropy through elegance and practical usability, even if individual components are familiar.

**Application to distill:** This translates to the quality test: "Would a knowledgeable reader learn something from this paragraph?" If not, the paragraph is zero-entropy filler. The skill deletes paragraphs that fail both the factual-content check and the surprise check.

## 5. Orwell's Writing Rules (1946)

**Source:** George Orwell, *Politics and the English Language*, Horizon magazine, 1946.

Six rules:

1. Never use a metaphor, simile, or figure of speech you are used to seeing in print
2. Never use a long word where a short one will do
3. If it is possible to cut a word out, always cut it out
4. Never use the passive where you can use the active
5. Never use a foreign phrase, scientific term, or jargon if there is an everyday equivalent
6. Break any of these rules sooner than say anything outright barbarous

Orwell's thesis: sloppy language enables sloppy thinking. Clarity in language is clarity in thought.

**Application to distill:** Rules 1–4 are directly implemented. Rule 1 is especially relevant for LLM text — models produce conventional figures of speech at scale ("tapestry", "landscape", "delve into", "navigate the complexities of"). Rule 6 is the safety constraint: never compress to the point of incomprehensibility.

## 6. Strunk & White — The Elements of Style (1918/1959)

**Source:** William Strunk Jr., *The Elements of Style*, 1918. Revised by E.B. White, 1959.

Core principle:

> "Vigorous writing is concise. A sentence should contain no unnecessary words, a paragraph no unnecessary sentences, for the same reason that a drawing should have no unnecessary lines and a machine no unnecessary parts."

Key rules implemented in the skill:
- **Omit needless words** — every word must earn its place
- **Use definite, specific, concrete language** — "43 employees" not "a number of people"
- **Put statements in positive form** — "ignored" not "did not pay attention to"
- **Use nouns and verbs** — they carry information; adjectives and adverbs often dilute it

**Application to distill:** These rules inform the verbose constructions replacement list (20+ direct substitutions) and the general principle of preferring concrete words over abstract ones.

## 7. Factual Density (Horn & Zhila, 2013)

**Source:** Christian Horn and Alisa Zhila, [*Using Factual Density to Measure Informativeness of Web Documents*](https://aclanthology.org/W13-5621.pdf), ACL Workshop on Language Analysis in Social Media, 2013.

Factual density is defined as:

```
FD = number_of_extracted_facts / number_of_words
```

Uses Open Information Extraction (OIE) to extract facts — (subject, relation, object) triples — from text, then calculates facts per word. Validated with 13 human annotators on 50 web documents (Spearman ρ = 0.41, p < 0.01).

**Application to distill:** The "maximize facts-per-word ratio" principle. Distillation increases FD by shrinking the denominator (words) while keeping the numerator (facts) constant. The self-check step verifies the numerator is preserved.

## 8. Plain Language (ISO 24495, 2023)

**Sources:**
- [ISO 24495-1:2023 — *Plain Language: Governing Principles and Guidelines*](https://www.iso.org/standard/78907.html)
- [US National Archives — Top 10 Principles for Plain Language](https://www.archives.gov/open/plain-writing/10-principles.html)

ISO defines plain language as communication whose "wording, structure, and design are so clear that the intended audience can easily find what they need, understand what they find, and use that information."

Key principles:
- Main point first, details after
- Short sentences (under 20–25 words)
- One idea per paragraph
- Active voice
- Common words over jargon (unless audience is technical)
- Structure that aids scanning — but only when it serves navigation

**Application to distill:** These principles balance compression against readability. Plain language is not telegraphese. The distilled text must remain natural, readable prose — the `<hard-gate>` constraint "NEVER make the text telegraphic" enforces this.

## 9. Claude 4.6 Prompting Best Practices

**Sources:**
- [Anthropic — Prompting Best Practices for Claude 4.6](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Anthropic — Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [obra/superpowers](https://github.com/obra/superpowers) — agentic skills framework (42k+ stars, official Anthropic marketplace)

The skill's prompt architecture follows official Anthropic guidance for Claude Opus 4.6 and Sonnet 4.6:

| Technique | Why | Source |
|-----------|-----|--------|
| Role assignment (`<role>`) | Focuses behavior and tone | Anthropic prompting docs |
| XML tags for structure | Claude parses them unambiguously | Anthropic prompting docs |
| 3 before/after examples | "Most reliable way to steer output format, tone, structure" | Anthropic prompting docs |
| Motivation/WHY (`<why-this-matters>`) | "Claude generalizes from explanations" better than from rules | Anthropic prompting docs |
| Positive framing | "Tell Claude what to do instead of what not to do" | Anthropic prompting docs |
| Self-verification loop | "Before you finish, verify against criteria" | Anthropic prompting docs |
| `<hard-gate>` for inviolable constraints | Prevents rationalization of exceptions | superpowers pattern |
| Dense prompt style | "Prompt format influences output format" | Anthropic prompting docs |
| No over-explaining | "Claude is already very smart — only add context it doesn't have" | Anthropic skill best practices |
| Reference files for the model | "Be literal. Don't assume Claude will infer what you mean." | Anthropic skill best practices |
| SKILL.md under 500 lines | Optimal context performance | Anthropic skill best practices |
| Feedback loop | Self-correction: generate → review → refine | Anthropic prompting docs |

## 10. The Measurement: Why gzip

The gzip compression ratio is the skill's primary entropy proxy. Theoretical basis: the Source Coding Theorem guarantees that lossless compression output size is an upper bound on entropy.

gzip (LZ77 + Huffman coding) captures:
- **Exact string repetitions** — detects redundancy and repetition
- **Non-uniform character distributions** — detects statistical redundancy

If gzip size drops after distillation, the text lost real structural redundancy. If it stays the same despite fewer words, only decorative words were cut while the same repetitive patterns remain.

Word count alone is insufficient — it doesn't distinguish between removing a meaningful word and removing a filler word. The gzip metric catches structural redundancy that word count misses.

## How the Pieces Fit Together

```
Shannon (theory)           → The compression floor exists; above it is eliminable
    ↓
Sun et al. (diagnosis)     → LLMs produce ~50% VC; verbose = less accurate
    ↓
Slop taxonomy (symptoms)   → 10 categories of recognizable noise patterns
    ↓
Orwell + Strunk (therapy)  → Mechanical rules for sentence-level compression
    ↓
Miessler (quality gate)    → Every sentence must surprise; zero surprise = cut
    ↓
Plain Language (constraint) → Result must stay readable, not become telegraphic
    ↓
Claude 4.6 patterns (impl) → XML tags, examples, self-check, hard-gates
    ↓
gzip + word count (measure) → Objective verification that compression is real
```
