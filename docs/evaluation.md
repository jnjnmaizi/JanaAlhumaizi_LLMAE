# Final evaluation — Days 1–4

## Core run

Mode: **mock**. External model API calls: **0**. Actual model API spend: **USD 0**. The cumulative notebook was executed from the beginning in two fresh local Python processes, with all embedded assertions passing. These were local runs; no Colab restart is claimed.

The five Day 2 cases and ten Day 3 cases still match the reference. All ten golden cases also pass through `run_app`. Cache tests remain separate from those ten.

| Controlled comparison | Without cache | With initially empty cache |
|---|---:|---:|
| Requests | 3 | 3 |
| Mock calls | 3 | 1 |
| Cache hits | 0 | 2 |
| Hit rate | 0% | 66.7% |

Hit sequence: `false, true, true`. Tests check prompt and directory version changes, the 300-second TTL boundary, and status exclusion without weakening ownership checks.

The saved metrics contain **22 requests** from the cache experiment and regression checks. Measured local Python latency ranges from **0.0028 to 0.0183 ms**, with mean **0.0071 ms**. These observations are not model inference times or a reliable speed benchmark. The input/output token illustration computes `(1000 × 2 + 400 × 4) / 1,000,000 = USD 0.0036` using invented prices; it is not billed cost or measured savings.

## Real-model homework

All three actual cases E01–E03 were generated on CPU using FLAN-T5 Small and the pinned revision. Greedy settings: `do_sample=False`, `num_beams=1`, `max_new_tokens=48`. Actual outputs, token counts, and inference seconds are in [the evaluation report](../murshid_live_outputs/evaluation_result.json).

E01 and E03 returned “Use its reference number”; E02 returned “Reference number”. Inspection finds each supported by the supplied context without extra facts. The automated keyword count is 3/3; it is not semantic accuracy. The [AI-assisted review](../results/day4_manual_review.json) explains each judgment, and the learner should confirm or revise it before submission.

The environment is recorded in [day4_environment.json](../results/day4_environment.json). The first case took 2.444 seconds; later cases took 0.020 and 0.026 seconds. These are actual observations from one local run, excluding setup/loading, and should not be replaced with reference timings. No generation or setup failures occurred in this run. Pip emitted a nonfatal cache-permission warning and continued using the installed dependencies; the local cache path is redacted in the notebook output. External inference API calls and billed API cost were zero.

## Verification and limitations

- **25/25 project tests passed**, including prior milestones, cache behavior, report comparisons, and inspection of the saved model report: [log](../results/day4_verification.txt).
- **8/8 instructor tests passed** in the documented code-only projection: [log](../results/day4_course_verification.txt).
- Core Day 4 and final JSON reports match the reference exactly. Model report settings, schema, case coverage, and keyword calculation were checked without requiring reference timing or generated text.
- No failures were observed in these runs. The checks do not establish general accuracy, security, or production readiness.

A limitation is the finite mock routing and very small English evaluation set. A feasible future improvement is a larger independently reviewed set with ambiguous inputs and incorrect answers that still contain the keywords, keeping semantic review separate from lexical scoring.

Before submission, the learner should review the notebook, demonstrate one decision to a partner, and confirm instructor access. These human activities are not recorded as completed.
