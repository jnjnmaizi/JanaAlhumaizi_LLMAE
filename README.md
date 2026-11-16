# Murshid Mini | مرشد

**Jana Alhumaizi · LLM Application Engineering · SDA-AIE-213**

A course project exploring how to build, test, and explain a small service assistant. The core grows in one cumulative notebook across four labs; homework runs in separate notebooks, with actual outputs saved for each completed milestone.

This project follows instructor **Meaad Al-Marri’s** [course repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213). Supplied code is used with attribution and is not presented as an independently designed system.

## Project scope

| Track | How answers are produced | Runtime |
|---|---|---|
| Core labs | `FakeClient` selects fixed responses; later labs add tools, guards, tests, and caching. | Python standard library; CPU; no model download or API key |
| Day 1 homework | FLAN-T5 Small generates tokens from a supplied context and question. | Separate Python runtime; CPU; package and model downloads |

All examples are synthetic. The core is a deterministic simulation, while the homework uses a real pretrained model. Neither is a deployed government service.

## Progress and roadmap

Execution and GitHub submission are tracked separately. Future rows describe planned course work, not completed features.

| Milestone | Scope | Status |
|---|---|---|
| Lab 1 | Mock client, input validation, response contract, baseline checks | Executed; embedded checks passed; upload paths need correction |
| Day 1 homework | One real-model answer on CPU | Executed; notebook uploaded; standalone JSON upload pending |
| Lab 2 | Structured ticket, read-only status lookup, ownership checks | Not started |
| Lab 3 | Prompt versioning, input guards, ten behavioral cases | Not started |
| Lab 4 | Public-answer cache, measurements, regression checks, final export | Not started |

Optional homework for Days 2–4 remains separate from the core and has not been started.

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

### Core labs

1. Open the cumulative `murshid.ipynb` in Google Colab using Python 3 and CPU / no accelerator. The core requires Python 3.9+ and only the standard library.
2. Run cells from the beginning in order. Day 1 contains three code cells.
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

Intended layout as the project progresses:

```text
README.md
notebooks/
  murshid.ipynb                  # One cumulative core notebook
murshid_outputs/
  baseline_results.json         # Actual Day 1 responses
  ...                           # Later outputs, added after execution
homework/
  day1_real_model.ipynb          # Separate real-model notebook
results/
  live_demo_result.json         # Actual real-model report
```

**Current upload notes:** the homework is currently stored as `Murshid_HW1.ipynb` at the root. The file named `murshid_outputs/baseline_results.json` contains the core notebook rather than a results array: save that notebook as `notebooks/murshid.ipynb`, then replace the JSON path with the actual downloaded results. The standalone homework JSON is still to be uploaded. These are file-organization tasks, not additional lab implementations.

## Verification through the final milestone

| Stage | Evidence to record |
|---|---|
| Day 1 | Three matching answers, correct response fields, nonnegative latency, and no client call for blank input |
| Day 2 — planned | Five prescribed scenarios, correct status and tool-call behavior, ownership checks, unchanged records |
| Day 3 — planned | Results for all ten supplied behavioral cases, including expected refusals |
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
