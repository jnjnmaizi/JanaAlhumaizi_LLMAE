# Murshid Mini | مرشد

**Jana Alhumaizi · SDA-AIE-213 · LLM Application Engineering**

Murshid Mini is my course project for building a small service assistant step by step. It answers a fixed set of service questions in Arabic and English, checks fictional application records, and validates requests before returning a response.

The project covers **Days 1–4**, with one cumulative lab notebook and separate homework exercises. The core and Day 4 homework include English explanations before every code cell.

[Open the main notebook in Colab](https://colab.research.google.com/github/jnjnmaizi/JanaAlhumaizi_LLMAE/blob/main/notebooks/murshid.ipynb) · [View saved lab results](murshid_outputs) · [Course reference](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213)

## What the project demonstrates

- Answering supported questions and asking for clarification when information is missing.
- Looking up application status using a reference number and checking record ownership.
- Rejecting malformed requests, unsupported actions, and selected unsafe inputs.
- Testing expected behavior and saving actual results for review.

The core labs use a deterministic `FakeClient` and fictional records. **Day 1 and Day 4 homework run a real language model:** `google/flan-t5-small` on CPU. Day 2 and Day 3 homework use ordinary Python functions.

## Progress

| Day | Core lab | Separate homework | Recorded outcome |
|---|---|---|---|
| 1 | Mock responses, input validation, response fields | Run FLAN-T5 Small locally | Baseline checks passed; real answer generated |
| 2 | Structured tickets, status lookup, ownership checks | Validate and dispatch tool calls | 5 lab cases and 7 homework cases passed |
| 3 | Versioned prompt, input/output validation, evaluation | Raise and catch validation errors | 10 lab cases passed; 3 expected errors caught and corrected input accepted |
| 4 | Public FAQ cache, measurements, regression, final export | Evaluate three real-model FAQ answers | 3 → 1 mock calls; 10 golden cases passed; 3 actual answers reviewed |

## Run the notebooks

### Core labs

Open [the cumulative notebook](https://colab.research.google.com/github/jnjnmaizi/JanaAlhumaizi_LLMAE/blob/main/notebooks/murshid.ipynb) in Google Colab with a Python 3 CPU runtime, then run the cells from the beginning. Cell numbers below count **code cells only**; Text cells explain each step.

| Milestone | Cells to run from a fresh runtime | Output |
|---|---|---|
| Day 1 | 1–3 | `murshid_outputs/baseline_results.json` |
| Day 2 | 1–6 | `murshid_outputs/day2_results.json` |
| Day 3 | 1–10 | `murshid_outputs/day3_results.json` |
| Day 4 | 1–14 | `murshid_outputs/day4_results.json`, `final_report.json`, and supporting reports |

Later lab cells depend on definitions from earlier days. The core requires only Python's standard library; no model download or API key is needed.

### Homework

Each homework notebook runs independently.

| Homework | Notebook | How to run |
|---|---|---|
| Day 1: real model | [Murshid_HW1.ipynb](Murshid_HW1.ipynb) | Run all four cells on CPU; allow time for dependencies and model weights to download |
| Day 2: tool calls | [homework/day2_tools.ipynb](homework/day2_tools.ipynb) | Run both cells; standard library only |
| Day 3: error handling | [homework/day3_errors.ipynb](homework/day3_errors.ipynb) | Run its single code cell; standard library only |
| Day 4: real-model evaluation | [homework/day4_evaluation.ipynb](homework/day4_evaluation.ipynb) · [Colab](https://colab.research.google.com/github/jnjnmaizi/JanaAlhumaizi_LLMAE/blob/main/homework/day4_evaluation.ipynb) | Run all three code cells on CPU; read the explanations and review the generated answers |

The real-model homework was run locally with Python 3.12 and pinned dependencies. Its setup installs `transformers==4.49.0` and `sentencepiece==0.2.0`, preserving existing PyTorch or installing `torch==2.6.0` if needed. The model runs inside the notebook runtime without an external inference API.

To save your work from Colab, use **Save a copy in GitHub** for the `.ipynb` notebook. Download generated `.json` reports from the Files sidebar and upload them separately to the matching repository folder. `/content/` is a Colab runtime location, not part of a GitHub file path.

## Results and verification

### Day 1 — fixed responses and real generation

The core returns the prescribed Arabic and English answers, includes trace and timing fields, and rejects blank input without calling the client. Actual responses are saved in [the baseline report](murshid_outputs/baseline_results.json); trace IDs and timings vary between runs.

The uploaded [Day 1 homework notebook](Murshid_HW1.ipynb) contains this real-model observation:

| Field | Recorded value |
|---|---|
| Question | How can I check my application status? |
| Supplied context | You can check your application status using its reference number. |
| Answer | **Use its reference number** |
| Model / device | `google/flan-t5-small` / CPU |
| Input / output tokens | 34 / 6, including output special tokens |
| Generation and decoding time | 0.982 seconds; excludes setup and model loading |

The tokenizer converts the instructions, context, and question into token IDs, which the model uses to generate output token IDs. Decoding turns those IDs into the readable answer.

The answer matches the supplied context without adding fees, dates, or a status claim. This is one observed example, not a general accuracy benchmark. The standalone `results/live_demo_result.json` is not currently published in this repository; the output remains available inside the uploaded notebook.

### Day 2 — controlled tool access

The [lab report](murshid_outputs/day2_results.json) covers an owned record, a missing reference number, an unknown record, a cancellation request, and another user's record. The lookup is read-only, and ownership is checked before returning a status.

The [homework report](results/tools_result.json) records **7/7 passing cases**. These check the allowed tool name, argument structure, reference format, and ownership. A correctly rejected request counts as a passing test when rejection is the expected behavior.

### Day 3 — validation and evaluation

The [lab report](murshid_outputs/day3_results.json) records **10/10 passing cases** in `mock` mode. It covers FAQs, status lookups, clarification, out-of-scope questions, ownership, an instruction override, blank input, and a malformed ticket.

The versioned prompt is a teaching artifact; `FakeClient` does not execute it. Case C10 checks malformed ticket data (`invalid_schema`), while additional regression tests separately verify malformed responses (`invalid_output`).

The [homework report](results/errors_result.json) records three deliberate `ValueError` rejections: `None`, blank text, and a 501-character question. A valid question is accepted after trimming surrounding whitespace. This exercise demonstrates how `raise`, `try`, and `except` handle expected failures.

### Day 4 — caching and real-model evaluation

The [cache report](murshid_outputs/day4_results.json) matches the prescribed comparison: **3 mock calls without caching, 1 with caching**, hits `[false, true, true]`, and a **66.7% hit rate**. Only exact public FAQ answers are cached. Status requests remain subject to ownership checks; version changes and expiry after 300 seconds cause misses.

The [final core report](murshid_outputs/final_report.json) records 10/10 golden cases and zero external model API calls. [Metrics](murshid_outputs/metrics.json) contain measured Python latency in milliseconds. The USD 0.0036 cost example uses invented prices and is not an actual charge or saving.

Day 4 homework generated these actual CPU outputs:

| Case | Answer | Input / output tokens | Inference seconds |
|---|---|---|---:|
| E01 | Use its reference number | 34 / 6 | 2.444 |
| E02 | Reference number | 36 / 4 | 0.020 |
| E03 | Use its reference number | 37 / 6 | 0.026 |

Output counts include special tokens. All three answers convey the supplied context's reference-number requirement. The **3/3 keyword hits are a lexical indicator, not semantic accuracy**. Read the [actual evaluation report](murshid_live_outputs/evaluation_result.json), [AI-assisted meaning review](results/day4_manual_review.json), and [runtime details](results/day4_environment.json). Review the interpretation yourself before submission.

### Regression tests

The latest saved verification run passed **25/25 project tests** across Days 1–4. See the [executed test log](results/day4_verification.txt). The instructor's eight tests also passed against a temporary code-only view of the cumulative notebook; [the course-test log](results/day4_course_verification.txt) explains that projection. Markdown explanations are excluded from execution; behavior assertions remain unchanged.

To run the tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

Tests compare results with the instructor-derived fixtures in [expected/](expected), check rejected requests and ownership, and verify repeat execution. The real-model answers were generated separately; offline regression tests inspect their saved report rather than replacing generation with a mock. The cumulative notebook also ran successfully in two fresh local Python processes. Colab execution remains available through the links above.

## Repository guide

| Location | Purpose |
|---|---|
| [notebooks/murshid.ipynb](notebooks/murshid.ipynb) | Current cumulative lab notebook: Days 1–4, fourteen code cells plus explanations |
| [Murshid_HW1.ipynb](Murshid_HW1.ipynb) | Uploaded Day 1 real-model homework with outputs |
| [homework/](homework) | Current separate Day 2, Day 3, and Day 4 homework notebooks |
| [murshid_outputs/](murshid_outputs) | Actual core lab reports |
| [results/](results) | Homework reports and executed test logs |
| [murshid_live_outputs/](murshid_live_outputs) | Actual Day 4 real-model evaluation report |
| [docs/project-notes.md](docs/project-notes.md) | Technical design, synthetic data, and reproducibility |
| [docs/evaluation.md](docs/evaluation.md) | Final measurements, interpretation, and limitations |
| [expected/](expected) | Instructor-derived expected results; model observations are not forced targets |
| [tests/](tests) | Regression tests for completed milestones |

Earlier uploads, `notebooks/murshid_Lap1.ipynb` and `Murshid_HW2.ipynb`, are retained. Use the notebook links above for the current cumulative lab and homework versions.

## Scope and learning goals

The practical focus is on the application around a model: validating input, deciding when a tool may run, checking access, handling errors, and measuring behavior with repeatable tests.

All service records are fictional. The session user is a teaching fixture, and keyword guards cover only selected examples. Passing these cases does not establish production security or general model accuracy. No model training or production deployment is included. A feasible next improvement is a larger reviewed test set with ambiguous and adversarial examples, including keyword-containing answers with incorrect meaning.

## Save and submit

Run the cumulative notebook from a fresh runtime and download `murshid_submission.zip` from Colab's Files sidebar. This generated ZIP contains the seven core JSON reports only; download the executed notebook and homework reports separately.

The implementation and recorded local checks are complete through Day 4. Before submitting, review the three generated answers, explain one routing decision to your partner as requested by the course, and confirm the instructor can access your repository. No partner demonstration or instructor-access confirmation is claimed here.

## Attribution

Program reference: **[SDAIA Academy on GitHub](https://github.com/SDAIAAcademy)**.

This course work follows instructor **Meaad Al-Marri's** [Murshid LLM Application Engineering repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213), the primary specification for SDA-AIE-213. Lab and homework code supplied by the instructor is credited as course material.

This repository documents my course implementation with AI assistance for coding, debugging, testing, and documentation. Project additions include English explanations, result exports, and regression coverage. The academy link credits the training context and does not imply endorsement of this implementation.
