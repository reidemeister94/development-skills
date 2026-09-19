# Screenshot audit categories

Recognize common library defaults before reporting them.
An established library style is not a finding unless the view uses it inconsistently or weakly.

Inspect each region for:

- unreadable or approximately failing contrast, color-only meaning, and controls too small to perceive or target;
- unclear primary actions, competing destructive actions, missing hierarchy, cryptic labels, or content dominated by chrome;
- inconsistent spacing, alignment, typography, casing, icon weight, radii, elevation, or state treatment;
- empty async regions, skeletons unlike their content, clipped content, and visible responsive breaks;
- duplicated or conflicting implementations of the same role.

Label estimated contrast or dimensions **Approximate**.
One screenshot cannot prove semantics, keyboard behavior, responsive states, hidden states, DOM order, or accessible names.
It also cannot distinguish a deliberate project token from a coincidental pixel value.
