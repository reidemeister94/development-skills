# Noise Patterns Reference

Comprehensive taxonomy of noise in LLM-generated text, derived from academic research
(Verbosity != Veracity, ACL 2025) and empirical analysis of LLM output patterns.

## 1. Hedging Language

Phrases that signal uncertainty without adding information.

**Kill list:**
- "It's important to note that..."
- "It's worth mentioning that..."
- "It should be noted that..."
- "It bears mentioning..."
- "One could argue that..."
- "It goes without saying..."
- "Needless to say..."
- "As you may know..."
- "As we all know..."
- "As mentioned above/earlier..."
- "Keep in mind that..."

**Rule:** If removing the hedge doesn't change the meaning, remove it. The statement that follows is the actual content.

## 2. Empty Transitions

Connectives that add words without adding logical connection.

**Kill list:**
- "Moreover" / "Furthermore" / "Additionally" / "In addition"
- "That being said" / "With that in mind" / "Having said that"
- "On the other hand" (when not actually contrasting)
- "In terms of..."
- "When it comes to..."
- "With respect to..."
- "In the context of..."

**Rule:** If two sentences are logically connected, the connection should be evident from content. If they aren't, a transition word won't fix that.

## 3. Empty Conclusions

Phrases that restate what was already said.

**Kill list:**
- "In summary" / "In conclusion" / "In essence"
- "To summarize" / "To sum up" / "To recap"
- "Overall" / "All in all" / "At the end of the day"
- "The bottom line is..."
- Any final paragraph that restates previous paragraphs without new information

**Rule:** A conclusion should synthesize or add insight, not repeat.

## 4. Filler Openers

Performative acknowledgment that adds zero content.

**Kill list:**
- "Certainly!" / "Absolutely!" / "Of course!"
- "Great question!" / "That's a really good point!"
- "Sure, I'd be happy to help with that!"
- "Let me explain..." / "Let me break this down..."
- "Here's the thing..."

**Rule:** Delete entirely. Start with the actual content.

## 5. Buzzword Inflation

Words that sound impressive but carry less information than simpler alternatives.

**Replace or remove:**
- "delve" -> "examine" or just state the finding
- "leverage" -> "use"
- "utilize" -> "use"
- "facilitate" -> "help" or "enable"
- "implement" -> "build" or "add" (when appropriate)
- "tapestry" / "landscape" / "realm" / "paradigm" -> be specific about what you actually mean
- "cutting-edge" / "state-of-the-art" / "revolutionary" / "game-changer" -> state the specific advance
- "holistic" / "comprehensive" / "robust" -> what specifically does it cover?
- "synergy" / "alignment" / "empower" -> what specifically happens?
- "seamlessly" / "effortlessly" -> remove (if true, the reader will see it)
- "innovative" / "novel" -> state what's new specifically

**Rule:** If a word can be replaced by a more specific one, replace it. If it can be removed without loss, remove it.

## 6. Verbose Constructions

Multi-word phrases that have single-word equivalents.

**Replace:**
- "in order to" -> "to"
- "due to the fact that" -> "because"
- "at this point in time" -> "now"
- "in the event that" -> "if"
- "for the purpose of" -> "to" or "for"
- "on a daily basis" -> "daily"
- "a large number of" -> "many"
- "the vast majority of" -> "most"
- "in spite of the fact that" -> "although"
- "is able to" / "has the ability to" -> "can"
- "make use of" -> "use"
- "take into consideration" -> "consider"
- "prior to" -> "before"
- "subsequent to" -> "after"
- "in close proximity to" -> "near"
- "on the basis of" -> "based on" or "from"

## 7. Structural Padding

Document-level noise patterns.

**Patterns:**
- Unnecessary introductory paragraphs that don't contain information
- Rigid 5-paragraph essay structure forced on content that doesn't need it
- Headers for single-paragraph sections (the header repeats what the paragraph says)
- Bullet points where a single sentence would suffice
- Tables with only 2-3 rows (often clearer as prose)
- Decorative formatting (excessive bold, horizontal rules, emoji as bullets)

**Rule:** Structure should serve navigation. If a document is short enough to read linearly, minimize structural elements.

## 8. Non-Committal Language

Patterns that avoid making falsifiable claims.

**Patterns:**
- "X can be Y" when you mean "X is Y"
- "X may help with Y" when evidence shows it does
- "It depends on various factors" without stating which factors
- Presenting all sides as equally valid when evidence favors one
- "Some people think X, others think Y" without evaluating
- Excessive use of "might", "could", "possibly", "potentially"

**Rule:** Make the strongest claim the evidence supports. Qualify only when the qualification itself carries information (e.g., specifying conditions under which something is true).

## 9. Repetition and Redundancy

**Patterns:**
- Same idea expressed in different words within same section
- "X, which means Y" where Y is the obvious implication of X
- Echo sentences: "This is important. The importance of this cannot be overstated."
- List items that overlap in meaning
- Re-explaining a concept already explained earlier in the document

**Rule:** State each fact once, in the place where it's most relevant.

## 10. Verbosity Compensation (from academic research)

When uncertain, LLMs produce specific noise patterns:

- **Ambiguity**: vague answers ("it's quite large") instead of specific ones ("3,029 entries")
- **Question repetition**: restating the question before answering
- **Enumeration**: listing all possibilities instead of selecting the correct one
- **Verbose details**: excessive context around a simple fact
- **Verbose format**: unnecessary markdown formatting, quotation marks, emphasis on non-key terms
