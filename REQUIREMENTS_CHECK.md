# Assignment evidence checklist

This checklist maps the provided assignment to actual artifacts. It is an evidence audit, not a prediction of the instructor's score. All required experiments are complete; the only proposed experiment in the README is explicitly distinguished from the completed 6,000-step follow-up.

| Requirement | Evidence and review |
|---|---|
| Executed starter and expanded notebooks | [Starter](starter_custom_llm.ipynb), [expanded](expanded_custom_llm.ipynb); all 12 code cells in each have execution counts, no error outputs, and visible plot/inspection results |
| Settings and predictions before training | Notebook section 1 and prediction cell; [recorded plan](PRETRAINING_PLAN.md) |
| At least two extension categories | Grammar and opposites; [1,256 grammar passages](corpus/expanded/grammar.txt), [882 contrast passages](corpus/expanded/opposites.txt); rationale and permissions in README |
| Corpus inspection and extraction warnings | [Starter manifest](llm_runs/starter/corpus_manifest.json), [expanded manifest](llm_runs/expanded/corpus_manifest.json); TXT only, no extraction warnings, no PDF/OCR claim |
| Training-only vocabulary and both UNK rates | [Starter report](llm_runs/starter/vocabulary_report.json), [expanded report](llm_runs/expanded/vocabulary_report.json); both corpus UNK rates and separate benchmark coverage reported |
| Split and fixed panels | [Starter split](llm_runs/starter/split.json), [expanded split](llm_runs/expanded/split.json); disjoint passages, 20 documents per panel, limitations explicitly stated |
| Actual steps, time, hardware and parameters | Both config/training_summary files and README run table; interrupted setup attempt disclosed, all submitted training complete |
| Untrained, halfway and final samples | Every saved string appears in README; both samples directories retain complete files with fixed generation settings |
| Plot and full measured loss table | Both training_curves.svg files embedded in README; all three measurements per main run included; batch loss distinguished from fixed-panel loss |
| Word ID and full 64-number vectors before/after | Both inspection.json and tokenization.json files linked; all coordinates shown in README and notebooks |
| Real gradient and parameter update | Recorded customer coordinate 0 before/gradient/after and effective warmup learning rate; AdamW/clipping explanation |
| Next-token probabilities, attention and learning | Actual prefix probability change and saved first-head attention; corpus, IDs, vectors, embeddings, weights, loss and backpropagation explained |
| Temperature comparison without retraining | Both temperature_comparison.json files; all 0.3/0.8/1.2 strings shown with fixed BOS and seed; identical outputs not hidden |
| Four unchanged 48-case evaluations | 192 required case-stage records across starter/expanded untrained/final; complete CSV/JSON/summary links; original suite and scoring hashes checked |
| Scores, coverage, groups, categories and failures | Four-row main table, complete breakdowns, full result files, concrete incorrect and unscorable examples, paired common-case analysis |
| Free continuations distinct from choice scores | Actual strings and examples of correct choice/incoherent continuation, including empty output |
| Training/evaluation separation | [Detailed audit](evidence/detailed_audit.json), both separation reports, original runner protections; 160 reserved passages removed; no eval files or output folders used as corpus |
| Completed corpus comparison | Two original runs retained; comparison distinguishes vocabulary change, learned prediction change and confounds; calls suite a public development benchmark |
| Working interface on saved trained nanoGPT | Unchanged [chat.py](chat.py) loads expanded/model.pt and saved vocabulary; no API or canned replies |
| At least three interactions plus screenshot or recording | [Original terminal recording](evidence/chat.cast), [inline GIF](evidence/chat_recording.gif), [transcript](evidence/chat_transcript.json); includes failure, model hash, unknown-word warning and fresh-context description |
| Instructions and independently rerunnable evaluations | Exact README chat/eval commands; all six saved-model reruns match, and all three fresh training runs reproduce original numerical evidence |
| Proposed next experiment and limitation | README states a concrete future data-design experiment and limitations; actual [6,000-step follow-up](expanded_6000_custom_llm.ipynb) goes beyond the two required runs |
| Save both ZIPs and notebooks | [Starter ZIP](llm_runs/starter.zip), [expanded ZIP](llm_runs/expanded.zip), separate executed notebooks; audit verifies every archived file against the run folder |
| Public repository accessibility | Anonymous access verified and GitHub notebook preview inspected; final course-portal submission remains the student's action |

## Review findings that were addressed

- Re-running the submitted notebook originally required a manual folder edit. It now allocates a new timestamped folder automatically and was tested by completing all three notebooks again.
- The terminal recording originally required a downloaded player. A clearly labeled GIF replay and still frame now show the exact recorded text directly in GitHub.
- Verification reports originally lacked reusable checking code. The submission now includes verify_submission.py, reproduce.py and compare_reproductions.py, plus real execution reports.
- The learning comparison now includes all 48 paired case statuses and a fixed common-case denominator. The 7-case gain is separated into 3 common-case gains and 4 newly covered correct cases.
- The notebook interpretation cells now explain actual results locally instead of merely referring the reader to the README.

## Limits preserved in the explanation

No minimum eval score is required. Nineteen expanded cases are still unscorable, one known-vocabulary opposite case fails, and free responses can be incoherent. These results are retained and explained rather than optimized away. One seed and the small public suite do not establish statistical generalization. Exact prefix checks do not prove absence of every semantic leak. AI assistance is disclosed; the student should be able to explain the recorded learning evidence in their own words.
