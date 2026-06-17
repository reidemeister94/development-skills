# Adopting External Features

Before recommending or implementing ANY feature/pattern/tool from outside the project (library, plugin, framework, hook, convention copied from another repo):

1. **Overlap audit.** Existing mechanism covers >50% of the need → reject.
2. **Value assessment.** No named recurring pain point → reject.
3. **Fit analysis.** Forces new dependencies/patterns → reject or redesign.
4. **Maintenance cost.** Ongoing burden must be clearly less than value.
5. **Implementation form.** Edit existing > new file. Convention > hook. Configuration > code.
6. **Present before implementing.** Show the filtered shortlist with this analysis. User confirmation validates the decision to proceed, not the analysis — that stays the model's responsibility.
