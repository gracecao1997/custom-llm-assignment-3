# Experiment plan recorded before execution

Two fresh 3000-step CPU models, learning rate 0.001, seed 42. Compare classroom-only versus classroom plus grammar and opposites files. Predict lower within-run panel loss and better grammatical/contrast vocabulary coverage after adding sources, without guaranteeing accuracy. Keep all 48 cases and scoring unchanged. No selection of a best seed or best checkpoint.

Sources are original synthetic teaching sentences prepared with AI assistance for this assignment, not copied from outside publications. The files may be shared with this project. They cover agreement, tense and contextual contrasts; they do not contain test stories, answer lists, or generated test outputs.

## Follow-up recorded after the two main experiments and before follow-up training

Expanded 3000 scored 27/48 with 29 scorable. Test 6000 fresh updates with the same expanded corpus, seed, split, panels and initial rate. Expect modest loss gains, unchanged coverage, and uncertain score change. Only TRAINING_STEPS changes; the cosine schedule duration is derived from this budget.
