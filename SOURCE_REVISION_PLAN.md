# Source based revision plan recorded before training

The September 22 class discussion emphasized adding independent teaching material rather than training on evaluation questions. The previous written assignment instructed students to read the fixed suite, and the assistant did read it before authoring the earlier synthetic extension. That history is retained and disclosed. This revision cannot undo prior exposure and is not claimed to be a blind or untouched final benchmark.

Primary comparison: a fresh classroom-only starter run versus classroom plus independently authored published English grammar and antonym material. Choose Graded Lessons in English by Alonzo Reed and Brainerd Kellogg (Project Gutenberg 7010) and English Synonyms and Antonyms by James Champlin Fernald (Project Gutenberg 28900) by subject, not by particular test items. Both predate this assignment.

Use the entire text bodies of both books, excluding Gutenberg front/end licensing wrappers, with deterministic paragraph reflow and the original maximum 47-token chunking. Do not select entries by test answers, alter the vocabulary directly, generate examples to fit cases, or tune the corpus after seeing scores. Apply the original automated reserved-prefix exclusion to candidate passages as a leakage guardrail; record excluded passage counts. This filter removes text and does not use answer keys to create or enrich training data. Keep untouched source downloads and their full notices outside corpus/.

Use fresh initialization, seed 42, 3000 steps, learning rate 0.001, original 2-block/4-head/64-dimensional architecture, and unchanged 48-case scoring. A separate 6000-step fresh run will test only the training-budget setting on the same expanded corpus, with the associated cosine-duration change disclosed. All runs and failures will be retained.

Prediction: independently authored material should add grammar and contrast contexts, but the 509-word-type cap and broad historical vocabulary may increase unknown-token rates, crowd out useful words, and reduce benchmark coverage or accuracy. Longer training cannot restore excluded vocabulary. We do not require the new version to outperform the earlier synthetic one.

AI prepares, executes and analyzes the experiments. Student comprehension will be documented only after the student supplies their own responses; no claim of demonstrated personal mastery is made from an AI-generated explanation alone.
