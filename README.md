# RetailFlow: Data Engineering from Zero to Pipeline

A two-day, 12-hour beginner course from Certisured using Python and Databricks Serverless. Start from zero, build a small retail data pipeline, and explain why its answers are trustworthy.

**Starter repository 1.0.0 · RetailFlow source data 1.0.0**

## How learning works

Core Vibes explain the ideas. Practical Vibes connect an idea to the next task. Build Buddy guides you as you create the numbered exercise cells in your own notebooks, run the code and inspect the actual results. Configuration and reusable support functions are supplied. Ask for a hint when needed; bring the actual output or error back to the guide.

Your goal is a small working pipeline and notebook results you can explain and reproduce. You will inspect 60 initial sales, clean deliberate quality problems, join shop data, account for refunds, apply a later delivery, and prove that replay does not double-count sales.

## Start here

1. Fork this public repository into your own GitHub account. Download or clone **your fork** so you have a place to save your work.
2. Read [the business story](retailflow-v1.0.0/docs/STORY.md) and [the course sequence](docs/COURSE_GUIDE.md).
3. Follow [SETUP.md](SETUP.md) to upload the dataset and import the notebooks into your assigned Databricks workspace.
4. Run the supplied `00_setup_and_preflight.ipynb`. Then follow Build Buddy to construct the empty exercise cells in notebooks 01–06.
5. Export your edited notebooks back into the `notebooks/` folder in your fork, preserving filenames and cell IDs. Record run evidence under `submissions/`; see its README. The repository copies do not update automatically when you edit a Databricks notebook.

If Python 3.10+ is available locally, verify the untouched starter with `python -B scripts/verify_repo.py --starter`. After you begin exercises, use `python -B scripts/verify_repo.py` to check the pinned dataset and notebook structure without requiring empty exercise cells. Neither command executes Spark or Delta.

## Repository layout

```text
README.md
SETUP.md
GITHUB_UPLOAD.md
LICENSE
VERSION
manifest.json
notebooks/                    # setup + six learner scaffolds
retailflow-v1.0.0/             # upload this folder's contents into the assigned volume folder
  manifest.json               # manifest for this learner distribution
  data/                       # seven source CSVs, byte-identical to dataset v1.0.0
  docs/                       # story, dictionary, quality and incremental rules
  checks/expected/            # machine-checking outputs, never source inputs
docs/COURSE_GUIDE.md
docs/CHECKPOINTS.md
scripts/verify_repo.py
submissions/README.md
VALIDATION_REPORT.md
```

## Source files and important rules

There are 10 stores, 12 products and 20 fictional customers. The initial sales file contains 60 sales. `sales_dirty.csv` is an **alternative** initial route: its 68 physical rows clean to 60 unique accepted sales, 2 duplicate drops and 6 quarantined rows. Six of the accepted rows require repair. Never append the clean and dirty initial files together.

Batch 02 contains 23 arrivals: 20 new sale IDs, 2 unchanged replays and 1 correction. It produces 80 current sales. S0003 becomes version 2 with quantity 4; S0080 arrives late but remains dated 2 January. Replaying either delivery must not change the final state.

All source dates are in January 2026 and store-local to Asia/Kolkata. All amounts are INR. Net sales is after discounts and before refunds; net revenue deducts refunds and is not profit. Blank customers are valid guests. Read paths explicitly: do not combine all CSVs or ingest the files under `checks/expected/` as sales.

## Reference outputs and starter status

Expected result CSVs are intentionally included for automatic comparisons. Completed instructor business notebooks, Vibe authoring scripts, facilitation answer keys and authentication files are excluded. The setup notebook is complete by design; its purpose is to establish access. The 32 business exercise cells in notebooks 01–06 are comments-only until you construct them.

This learner distribution has a new manifest because it excludes instructor materials and uses `checks/expected/`. The seven original data CSVs and 17 expected-result CSVs are unchanged. Notebook checks were adjusted to that learner-visible path; business logic and record identifiers are unchanged. Do not mix these scaffolds with a dataset folder from a different distribution.

Local checks have passed; Spark and Delta execution still need the instructor's rehearsal in the actual Databricks workspace. The course does not provision accounts or schedule jobs automatically. Course Vibes and the native Build Buddy project are being authored; this repository is their versioned starting point.

The materials are synthetic and distributed under the CC0 dedication in LICENSE. No purchase or real customer data is required.
