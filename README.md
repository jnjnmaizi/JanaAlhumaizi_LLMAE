# Murshid Mini | مرشد

**Jana Alhumaizi · SDA-AIE-213 · LLM Application Engineering**

Murshid Mini is my course project for building a small service assistant step by step. It answers a fixed set of service questions in Arabic and English, checks fictional application records, and validates requests before returning a response.

The project currently covers **Days 1–3**, with a cumulative lab notebook and separate homework exercises. Day 4 has not started.

[Open the main notebook in Colab](https://colab.research.google.com/github/jnjnmaizi/JanaAlhumaizi_LLMAE/blob/main/notebooks/murshid.ipynb) · [View saved lab results](murshid_outputs) · [Course reference](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213)

## What the project demonstrates

- Answering supported questions and asking for clarification when information is missing.
- Looking up application status using a reference number and checking record ownership.
- Rejecting malformed requests, unsupported actions, and selected unsafe inputs.
- Testing expected behavior and saving actual results for review.

The core labs use a deterministic `FakeClient` and fictional records. **Only Day 1 homework runs a real language model:** `google/flan-t5-small` on CPU. Day 2 and Day 3 homework use ordinary Python functions.

## Progress

| Day | Core lab | Separate homework | Recorded outcome |
|---|---|---|---|
| 1 | Mock responses, input validation, response fields | Run FLAN-T5 Small locally | Baseline checks passed; real answer generated |
| 2 | Structured tickets, status lookup, ownership checks | Validate and dispatch tool calls | 5 lab cases and 7 homework cases passed |
| 3 | Versioned prompt, input/output validation, evaluation | Raise and catch validation errors | 10 lab cases passed; 3 expected errors caught and corrected input accepted |
| 4 | Not started | Not started | — |

## Run the notebooks

### Core labs

Open [the cumulative notebook](https://colab.research.google.com/github/jnjnmaizi/JanaAlhumaizi_LLMAE/blob/main/notebooks/murshid.ipynb) in Google Colab with a Python 3 CPU runtime, then run the cells from the beginning.

| Milestone | Cells to run from a fresh runtime | Output |
|---|---|---|
| Day 1 | 1–3 | `murshid_outputs/baseline_results.json` |
| Day 2 | 1–6 | `murshid_outputs/day2_results.json` |
| Day 3 | 1–10 | `murshid_outputs/day3_results.json` |

Later lab cells depend on definitions from earlier days. The core requires only Python's standard library; no model download or API key is needed.

### Homework

Each homework notebook runs independently.

| Homework | Notebook | How to run |
|---|---|---|
| Day 1: real model | [Murshid_HW1.ipynb](Murshid_HW1.ipynb) | Run all four cells on CPU; allow time for dependencies and model weights to download |
| Day 2: tool calls | [homework/day2_tools.ipynb](homework/day2_tools.ipynb) | Run both cells; standard library only |
| Day 3: error handling | [homework/day3_errors.ipynb](homework/day3_errors.ipynb) | Run its single cell; standard library only |

Day 1 homework was run with Python 3.12 and pinned dependencies. Its setup installs `transformers==4.49.0` and `sentencepiece==0.2.0`, preserving existing PyTorch or installing `torch==2.6.0` if needed. The model runs inside the notebook runtime without an external inference API.

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

### Regression tests

The latest saved verification run passed **18/18 tests** across Days 1–3. See the [executed test log](results/day3_verification.txt) for the individual checks.

To run the tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

Tests compare results with the instructor-derived fixtures in [expected/](expected), check rejected requests and ownership, and verify repeat execution. The 18-test count belongs to the saved Day 3 run.

## Repository guide

| Location | Purpose |
|---|---|
| [notebooks/murshid.ipynb](notebooks/murshid.ipynb) | Current cumulative lab notebook: Days 1–3, ten code cells |
| [Murshid_HW1.ipynb](Murshid_HW1.ipynb) | Uploaded Day 1 real-model homework with outputs |
| [homework/](homework) | Current separate Day 2 and Day 3 homework notebooks |
| [murshid_outputs/](murshid_outputs) | Actual core lab reports |
| [results/](results) | Homework reports and executed test logs |
| [expected/](expected) | Instructor-derived expected results |
| [tests/](tests) | Regression tests for completed milestones |

Earlier uploads, `notebooks/murshid_Lap1.ipynb` and `Murshid_HW2.ipynb`, are retained. Use the notebook links above for the current cumulative lab and homework versions.

## Scope and learning goals

The practical focus is on the application around a model: validating input, deciding when a tool may run, checking access, handling errors, and measuring behavior with repeatable tests.

All service records are fictional. The session user is a teaching fixture, and keyword guards cover only selected examples. Passing these cases does not establish production security or general model accuracy. No model training, deployment, or Day 4 functionality is included at this checkpoint.

## Attribution

This course work follows instructor **Meaad Al-Marri's** [Murshid LLM Application Engineering repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213), the primary specification for SDA-AIE-213. Lab and homework code supplied by the instructor is credited as course material.

This repository documents my course implementation with AI assistance for coding, debugging, testing, and documentation. Project additions include result exports and regression coverage; saved outputs distinguish executed work from future milestones.
