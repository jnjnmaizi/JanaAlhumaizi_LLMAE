# Murshid Mini | مرشد

**Jana Alhumaizi · LLM Application Engineering · SDA-AIE-213**

A course project exploring how to build, test, and explain a small service assistant. The core grows in one cumulative notebook across four labs; homework runs in separate notebooks, with actual outputs saved for each completed milestone.

This project follows instructor **Meaad Al-Marri’s** [course repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213). Supplied code is used with attribution and is not presented as an independently designed system.

## Project scope

| Track | How answers are produced | Runtime |
|---|---|---|
| Core labs | `FakeClient` selects fixed responses; later labs add tools, guards, tests, and caching. | Python standard library; CPU; no model download or API key |
| Day 1 homework | FLAN-T5 Small generates tokens from a supplied context and question. | Separate Python runtime; CPU; package and model downloads |
| Day 2 homework | A Python dispatcher validates manually supplied tool calls and checks ownership. | Separate notebook; standard library only; no model or API |

All examples are synthetic. The core is a deterministic simulation, while the homework uses a real pretrained model. Neither is a deployed government service.

## Progress and roadmap

Execution and GitHub submission are tracked separately. Future rows describe planned course work, not completed features.

| Milestone | Scope | Status |
|---|---|---|
| Lab 1 | Mock client, input validation, response contract, baseline checks | Executed; embedded and regression checks passed |
| Day 1 homework | One real-model answer on CPU | Executed; notebook uploaded; standalone JSON upload pending |
| Lab 2 | Structured ticket, read-only status lookup, ownership checks | Executed; 5/5 prescribed cases match the reference |
| Day 2 homework | Validate and dispatch allowed tool calls | Executed; 7/7 prescribed cases passed; records unchanged |
| Lab 3 | Prompt versioning, input/output checks, ten behavioral cases | Executed; C01–C10 passed; mode=mock |
| Day 3 homework | Catch deliberate validation errors and correct input | Executed; three expected rejections and accepted corrected input |
| Lab 4 | Public-answer cache, measurements, regression checks, final export | Not started |

Homework for Days 2 and 3 is complete in separate notebooks. Lab 4 and its homework have not been started. Execution status does not by itself confirm that every local file has been uploaded to GitHub.

## Day 1 results

### Core lab

The three examples produced the prescribed answers, and the notebook printed `"checks": "passed"`.

| Input | Answer |
|---|---|
| `كيف أتابع طلبي؟` | `يمكنك متابعة حالة طلبك باستخدام رقم المرجع.` |
| `How can I check my application status?` | `You can check your application status using its reference number.` |
| `ساعدني` | `ما الخدمة التي تحتاج مساعدة بشأنها؟` |

The response contract contains `trace_id`, `answer`, `model`, and `latency_ms`. The model is `training-mock`; the trace ID must be nonempty and latency nonnegative. Blank input returns a validation message without calling the client. Trace IDs and timings vary between runs.

### Real-model homework

[Executed homework notebook](Murshid_HW1.ipynb) · [Open in Colab](https://colab.research.google.com/github/jnjnmaizi/JanaAlhumaizi_LLMAE/blob/main/Murshid_HW1.ipynb)

The uploaded Colab run recorded:

| Field | Observed value |
|---|---|
| Model | `google/flan-t5-small` |
| Revision | `0fc9ddf78a1e988dac52e2dac162b0ede4fd74ab` |
| Device | CPU |
| Context | You can check your application status using its reference number. |
| Question | How can I check my application status? |
| Generated answer | **Use its reference number** |
| Generation and decoding time | **0.982 seconds** |
| Input tokens | **34** |
| Output tokens, including special tokens | **6** |
| External inference API calls | **0** |

The tokenizer converts the instructions, context, and question into token IDs that FLAN-T5 Small processes on CPU to generate output token IDs. Decoding converts those generated IDs into the answer, whereas `FakeClient` retrieves an answer from a fixed mapping.

The answer satisfies this example: it recommends the reference number without inventing fees, dates, or application status. The recorded time excludes installation and model loading; it is one observation, not a benchmark. The `review_required` field is a review reminder, not an automated correctness score.

## Run the project

### Day 2 evidence

The Day 2 milestone occupies cells 1–6 of the [cumulative notebook](notebooks/murshid.ipynb): three Day 1 cells followed by three Day 2 cells. Their source is preserved as Day 3 extends the notebook. The [actual Day 2 report](murshid_outputs/day2_results.json) matches the instructor's complete reference report.

| Case | Result | Status-tool calls |
|---|---|---:|
| Owned reference, `REF-1001` in Riyadh | `under_review` | 1 |
| Status request without a reference | `needs_clarification` | 0 |
| Missing reference, `REF-9999` | `not_found` | 1 |
| Cancel `REF-1001` | `unsupported_action` | 0 |
| Another user's reference, `REF-1002` | `access_denied` | 1 |

The [separate homework notebook](homework/day2_tools.ipynb) records seven passing cases in [results/tools_result.json](results/tools_result.json). Cases 2–7 are successful refusals, not crashes. It adapts the instructor's [tool homework](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213/blob/main/extensions/homework_tools.ipynb), preserving the dispatcher and its assertions; the documented addition exports the generated report to `results/tools_result.json`.

Validation checks the call's structure, allowed tool name, and argument types. Authorization separately checks whether the trusted session user owns the record: `REF-1002` is well-formed but unavailable to `demo-user-1`. The synthetic session is a teaching fixture, not production authentication.

The Day 2 verification run passed **12/12 tests**, including Day 1 regression, exact Day 2/homework fixture comparisons, repeat execution, schema rejection before tool calls, ownership, and unchanged records. The executed log is saved in [results/day2_verification.txt](results/day2_verification.txt). Run these milestone tests from the repository root with `python3 -m unittest discover -s tests -v`; the full four-day course suite is not claimed to pass.

### Day 3 evidence and decisions

The cumulative notebook now contains **ten code cells**. Cells 7–10 follow the instructor's [Day 3 source](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213/blob/main/labs/day3.py); earlier cell source is unchanged. The prompt template is a versioned teaching artifact: `FakeClient` does not execute it.

The actual [Day 3 report](murshid_outputs/day3_results.json) matches the full reference: `mode=mock`, `passed=10`, `total=10`, `pass_rate=100.0`. C01/C02 answer the FAQs; C03 returns an owned status; C04 reports a missing reference; C05 requests clarification; C06 rejects an out-of-scope question; C07 denies another user's record; C08 blocks the supplied instruction override; C09 rejects blank input; C10 rejects `BAD_TICKET` because its clarification flag is a string instead of a boolean.

C10 exercises `invalid_schema` for malformed structured ticket data. Separate tests deliberately make the router return malformed responses and verify that output validation returns `invalid_output`. The added tests also check that guards prevent routing, 500 characters are accepted while 501 are rejected, and evaluation reports diagnostic reasons for wrong results without weakening the supplied golden cases.

The [Day 3 homework](homework/day3_errors.ipynb) runs independently in **one code cell**, with only the standard library. It preserves the instructor's [error example](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213/blob/main/extensions/error_examples.ipynb) and adds an export to [results/errors_result.json](results/errors_result.json). `None` and blank input raise `ValueError: Enter a non-empty question string.`; 501 characters raises `ValueError: Use at most 500 characters.`. The corrected question is `How can I check my application status?`, accepted after surrounding whitespace is removed.

`raise` signals invalid input; `try` runs the operation that might fail; `except ValueError` catches and checks the intended rejection. A caught rejection is a successful test when the input was supposed to be refused; an unhandled traceback or failed assertion is not.

All **18 local tests passed**, including earlier milestones and both new notebooks; see [the executed log](results/day3_verification.txt). The documented additions are homework report export and regression coverage. Keyword filters are educational and do not cover every injection or personal-data pattern; ten selected mock cases do not establish general safety, live-model accuracy, or production authentication. No Day 4 caching is implemented.

### Core labs

1. Open the cumulative `murshid.ipynb` in Google Colab using Python 3 and CPU / no accelerator. The core requires Python 3.9+ and only the standard library.
2. Run cells from the beginning in order. Day 1 uses cells 1–3; Day 2 adds cells 4–6. Day 3 adds cells 7–10. Run all ten for this checkpoint.
3. Inspect the checks and download the generated files from `murshid_outputs/`.
4. Append each later lab to the same notebook after completing the previous milestone.

### Day 1 homework

1. Open the homework notebook separately with a CPU runtime.
2. Use Python 3.12 for the supplied pinned dependencies. A Python 3.13 Colab session encountered an installation failure during this project.
3. Run all four cells in order. Setup preserves existing PyTorch; if absent, it installs `torch==2.6.0` from the supplied CPU index. It installs `transformers==4.49.0` and `sentencepiece==0.2.0`.
4. Wait for package and model downloads. If a runtime restart is requested, restart and rerun from the first cell.
5. Review the answer, then download `results/live_demo_result.json` and the executed notebook.

Inference runs inside the notebook runtime after downloading the weights. No paid inference endpoint or API key is required. Use the instructor’s [setup and troubleshooting guide](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213/blob/main/extensions/README.md) for environment failures.

## Repository organization

For Day 2 homework, open `homework/day2_tools.ipynb` in a separate Python 3 / CPU notebook and run its two cells in order. It needs no package installation, model download, or API key. Download the executed notebook and its generated `results/tools_result.json`.

Intended layout as the project progresses:

```text
README.md
notebooks/
  murshid.ipynb                  # One cumulative core notebook
murshid_outputs/
  baseline_results.json         # Actual Day 1 responses
  day2_results.json             # Actual five-case Day 2 report
  day3_results.json             # Actual C01–C10 evaluation report
  ...                           # Later outputs, added after execution
homework/
  day1_real_model.ipynb          # Separate real-model notebook
  day2_tools.ipynb               # Separate two-cell dispatcher homework
  day3_errors.ipynb              # Separate one-cell error exercise
results/
  live_demo_result.json         # Actual real-model report
  tools_result.json             # Actual seven-case dispatcher report
  day2_verification.txt          # Day 2 test log
  errors_result.json            # Three caught errors and corrected input
  day3_verification.txt          # Executed 18-test regression log
```

**Upload notes:** the uploaded Day 1 homework remains available as `Murshid_HW1.ipynb` at the root. This checkpoint includes a freshly generated `murshid_outputs/baseline_results.json` containing actual response records; it should replace the incorrectly named notebook previously uploaded at that path. Save notebooks with `.ipynb` filenames and upload generated JSON separately. Local execution and remote publication remain separate steps.

## Verification through the final milestone

| Stage | Evidence to record |
|---|---|
| Day 1 | Three matching answers, correct response fields, nonnegative latency, and no client call for blank input |
| Day 2 — verified | Five prescribed scenarios, correct status and tool-call behavior, ownership checks, unchanged records; seven homework cases |
| Day 3 — verified | C01–C10 passed; guards, output contract, and three intentional homework rejections checked |
| Day 4 — planned | Cache-hit sequence, mock-call counts, regression results, and the final report |

Compare stable fields with the instructor’s [expected results](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213/tree/main/expected). Preserve actual outputs and failures; do not replace measurements with reference observations. Day 1 completion does not mean the full four-day test suite has passed.

## Engineering focus and limitations

- **Exact matching:** Day 1 removes surrounding whitespace, but punctuation or spelling changes can still lead to the fallback answer.
- **Application response versus client call:** invalid input receives a response even when the client is not called.
- **Generated answer versus verified answer:** nonempty text still needs review against the supplied context.
- **Reproducibility:** keep the model revision, settings, inputs, outputs, and measurement units visible.

This project does not train a model, use real application records, or establish production security. One English example does not demonstrate general accuracy or Arabic capability. Later mock caching measurements will describe the simulator, not measured savings from a paid API.

## Final submission checklist

- [ ] Complete and rerun all four core milestones in the same notebook.
- [ ] Correct repository paths and verify that JSON files contain reports rather than notebooks.
- [ ] Save actual outputs and the final report from the completed run.
- [ ] Keep completed homework notebooks separate, with their own results.
- [ ] Update the progress table and report only tests actually executed.
- [ ] Download the executed notebook separately from any generated results archive.
- [ ] Confirm that the instructor can open the repository and submission files.

## Acknowledgments

**LLM Application Engineering · SDA-AIE-213**, instructor **Meaad Al-Marri**, and [SDAIA Academy](https://github.com/SDAIAAcademy). The [instructor’s repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213) is the primary specification and source of the supplied examples.

This repository records Jana Alhumaizi’s course work with AI-assisted implementation, debugging, and documentation. Instructor-provided code is credited, and executed results are distinguished from planned work. No Academy endorsement or certification is claimed.
