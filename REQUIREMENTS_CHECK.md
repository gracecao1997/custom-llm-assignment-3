# Revised submission: requirement-to-evidence map

The current submission uses independent, complete published book bodies. Earlier synthetic experiments are retained in [SYNTHETIC_EXPERIMENTS.md](SYNTHETIC_EXPERIMENTS.md), with their [historical checklist](SYNTHETIC_REQUIREMENTS_CHECK.md). Earlier exposure to the public tests is disclosed; this revision is not a blind evaluation.

| Requirement | Current evidence |
|---|---|
| English report and two executed main notebooks | [README](README.md), [baseline](source_starter_custom_llm.ipynb), [source expansion](source_expanded_custom_llm.ipynb) |
| Predictions and settings before training | [Committed source revision plan](SOURCE_REVISION_PLAN.md), commit c924df9; notebook configuration cells |
| Two extension categories with sources | Grammar and synonyms/antonyms; [original sources](source_materials/sources.json), complete editions with notices in source_materials, source attribution in README |
| Inspect corpus and document preparation | [Deterministic preparation](prepare_source_corpus.py), [hashes and counts](source_materials/preparation_manifest.json), run corpus_manifest.json files; no PDF/OCR claim |
| Training-only vocabulary, UNK and data split | Each run’s vocabulary_report.json, tokenization.json and split.json; README reports train and validation UNK, passage-level split limitations and 20-document fixed panels |
| Actual training, hardware and time | Main runs each complete 3,000 steps at initial learning rate 0.001; config.json, training_summary.json and executed outputs |
| Learning explanation and weight evidence | README and notebook outputs show token IDs, full 64-dimensional before/after embeddings, actual gradient and parameter update, next-token probabilities and attention |
| Measured losses, plots and samples | All measured panel losses, training_curves.svg and complete untrained/halfway/final samples retained and shown in README |
| Temperature comparisons | Complete saved generations at 0.3, 0.8 and 1.2, with fixed prompts and seeds, in README and temperature_comparison.json |
| Four complete unchanged evaluations | Main runs’ language_evals/untrained and language_evals/final contain all 48 cases in CSV and JSON plus summaries; 192 required case-stage records |
| Coverage, accuracy, categories and failures | README distinguishes all-case from scorable accuracy, includes all groups/categories and real continuations; all 24 extension cases remain unscorable |
| Separation and reproducibility | [Audit](source_evidence/detailed_audit.json), original suite/runner hashes and reserved-prefix guardrail; no eval output used as corpus. Exact checks do not establish absence of semantic contamination |
| Saved checkpoint and working chat | Original [chat.py](chat.py), source_expanded/model.pt and saved vocabulary; README launch commands |
| Three real interactions and recording | [PTY recording](source_evidence/chat.cast), [transcript](source_evidence/chat_transcript.json), [GIF rendering of recorded text](source_evidence/chat_recording.gif). GIF is explicitly a replay, not a native screenshot |
| Independent saved-model evaluation reruns | [Six exact rerun comparisons](source_evidence/rerun_verification.json); all 288 case-stage records match the saved outputs |
| Executed follow-up and proposed next experiment | [6,000-step notebook](source_expanded_6000_custom_llm.ipynb), same corpus/split/vocabulary/initial weights; future vocabulary-cap change is clearly unexecuted |
| Saved run ZIPs and separate notebooks | [Baseline ZIP](llm_runs/source_starter.zip), [expanded ZIP](llm_runs/source_expanded.zip), [follow-up ZIP](llm_runs/source_expanded_6000.zip); audit compares archive bytes with saved files |
| Reproduction tools | [Audit code](verify_submission.py), [training reproduction helper](reproduce.py), [comparison helper](compare_reproductions.py); no claim of additional fresh retraining beyond the three executed revised notebooks |
| Transparent AI assistance and history | README discloses AI contributions and prior test exposure; old higher-scoring synthetic runs remain available. Technical prose is not presented as proof of personal mastery |

## Limits requiring honest interpretation

The revised scores are 20/48, 23/48 and 24/48. The follow-up's 100% scorable accuracy covers only half the suite. A 512-token cap and about 27% UNK in the expanded corpus prevent extension coverage. One seed, related passages across train/validation, and prior public-test exposure limit generalization claims. Extra training is real, but it does not fix missing vocabulary. The student must understand and explain the work personally; AI-generated explanations cannot substitute for that. The course-portal submission remains the student's action, and this checklist does not guarantee a grade or an instructor's academic-integrity determination.
