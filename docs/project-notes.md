# Project notes — Murshid Mini

## Design and execution

The cumulative notebook implements four course milestones using the Python standard library. Run all 14 code cells in order on CPU. Each code cell has an English Markdown explanation; these were requested by the learner in addition to the instructor's code-only layout. The first ten code-cell sources are preserved, and the four Day 4 blocks follow the instructor's `labs/day4.py` with attribution.

Request → cache eligibility check → cached public answer, or input guard → ticket extraction → schema validation → router → public mock response / authorized read-only status lookup → output validation → response and minimal metrics.

`FakeClient` selects fixed responses and counts calls. It is not a trained model. `build_prompt` exposes a versioned teaching template; the mock does not interpret it. `run_pipeline` manages guards and validation; `run_app` adds cache behavior and measurements. Homework stays separate. Days 1 and 4 download/load FLAN-T5 Small for real CPU inference, while Days 2 and 3 use standard-library exercises.

## Synthetic data and fields

The instructor's handwritten teaching fixtures are the data source. No real users, services, identifiers, or application records are used. See the executed export in [synthetic_data.json](../murshid_outputs/synthetic_data.json).

| Field | Meaning |
|---|---|
| `service_directory` | Fixed public answers indexed by `ar` and `en` |
| Record key | Fictional reference, such as `REF-1001` |
| `owner` | Fictional user allowed to view the record |
| `status` | Fictional application status |
| Ticket `service` | Selected service or out-of-scope route |
| Ticket `city` | Supported city value validated by the exercise |
| Ticket `request_id` | Reference number or `None` when missing |
| Ticket `needs_clarification` | Boolean consistent with the missing-reference state |

`REF-1001` belongs to `demo-user-1` and is `under_review`; `REF-1002` belongs to `demo-user-2` and is `approved`. These are public synthetic teaching fixtures. The default session is `demo-user-1`; a user writing another owner name inside a question does not change that session. This is an authorization exercise, not real authentication.

## Cache policy

Only the two exact directory FAQ questions, after trimming, are eligible. Keys include text, language, model label, prompt version, and directory version. Entries contain only answer text and creation time. A hit requires an age from zero inclusive to 300 seconds exclusive. A changed version, expired entry, or negative clock age causes a miss.

Status lookups, unknown questions, malformed ticket overrides, and guarded input bypass caching. The shared cache cannot return private status data. Records remain unchanged. Each response receives its own trace ID, including cache hits.

Metrics contain `trace_id`, `mode`, `code`, `cache_hit`, `mock_calls`, `tool_calls`, and `latency_ms`. They omit raw questions, answers, references, and owners. Synthetic data is exported separately for the course exercise.

## Evidence and repeatability

The executed outputs include the baseline, Day 2/3/4 reports, final report, metrics, and synthetic data. Cell 14 packages these JSON files into `murshid_submission.zip`; it does not package the notebook or separate homework.

The complete core notebook ran in two fresh local Python processes, then passed project regression tests. Existing daily tests select the relevant code cells so adding Markdown or later days does not weaken their behavior assertions. The instructor's test file was also run unchanged in a temporary code-only projection with daily script views extracted from the notebook. Its source-match test checks consistency of those views, not independent authorship.

Day 4 homework executed all three supplied code cells in an existing isolated Python 3.12 environment. Cached model weights were reused offline; no source data, package, or model output was invented. CPU package versions and measurements are saved with the report. The `expected/evaluation_result.json` file is the instructor's observation, while `murshid_live_outputs/evaluation_result.json` is this project's actual run.

## One decision to explain

Input `REF-1002` with the default session bypasses the public cache, becomes a status ticket, passes schema validation, and reaches the ownership check. The expected response is `access_denied` without exposing `approved`. Its limitation is that the session is a fixed fictional identity. This is a prepared explanation for the learner; no partner discussion has been performed by the agent.

The documented small change is adding English Text cells before code cells while preserving the supplied implementation. Result exports, fixture comparisons, and additional regression coverage make the behavior reviewable.

## References

- [Instructor's course repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213)
- [SDAIA Academy](https://github.com/SDAIAAcademy)
