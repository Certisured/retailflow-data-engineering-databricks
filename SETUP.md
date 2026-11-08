# Learner setup

Use this starter repository with your trainer-provided Databricks Serverless workspace. No local Spark installation, API key or paid account purchase is part of these instructions.

## 1. Obtain your own copy

Fork the public Certisured course repository into your GitHub account. Download or clone your fork. Keep its root layout: README.md, notebooks/, retailflow-v1.0.0/, docs/, scripts/, and submissions/. Your fork is where Build Buddy will inspect the artifacts you push.

Before changing anything, you may run `python -B scripts/verify_repo.py --starter` from that root if Python 3.10+ is available. It requires no additional packages. This local check is optional for using Databricks; it is useful when verifying a download.

## 2. Obtain the assigned workspace names

Your trainer supplies an existing Unity Catalog catalog, schema and volume, plus a unique table prefix for you. Use lowercase letters, digits and underscores, beginning with a letter, because the notebooks validate that naming convention.

The trainer must arrange USE CATALOG, USE SCHEMA, READ VOLUME and CREATE TABLE. The person uploading files also needs WRITE VOLUME. Use your own table prefix so you write only your training tables. Workspace provisioning and instructor rehearsal occur before the teaching exercises.

## 3. Upload the dataset folder

In Databricks Catalog Explorer, open the assigned volume. Create a folder named exactly `retailflow-v1.0.0` and upload the **contents of the repository's retailflow-v1.0.0 folder**, preserving its subfolders. Do not upload a still-compressed ZIP as if Spark could read it directly.

The resulting paths must look like:

```text
/Volumes/<catalog>/<schema>/<volume>/retailflow-v1.0.0/manifest.json
/Volumes/<catalog>/<schema>/<volume>/retailflow-v1.0.0/data/sales_batch_01.csv
/Volumes/<catalog>/<schema>/<volume>/retailflow-v1.0.0/checks/expected/initial_sales.csv
```

Angle-bracket names are placeholders for the assigned real names. Upload the full dataset folder: its manifest, data/, docs/ and checks/. The preflight checks every listed file hash. This distribution uses checks/expected/, not the earlier instructor package's instructor/expected/ path.

Batch 02 remains at `data/sales_batch_02.csv` to preserve exact paths. Its presence does not mean it should be processed on Day 1. The notebooks name each input explicitly and introduce batch 02 only in notebook 05.

## 4. Import the notebooks

In Databricks Workspace, create your training notebook folder and use its Import action to import the seven .ipynb files from the repository's notebooks/ folder. Select Serverless in the notebook compute selector where needed.

In the configuration cell of **every** notebook, replace the example values for CATALOG, SCHEMA, VOLUME and TABLE_PREFIX with your assigned names. Keep those values identical across notebooks. Configuration contains workspace names, not credentials.

## 5. Run setup, then build through the lessons

Run the supplied `00_setup_and_preflight.ipynb` top to bottom. It verifies uploaded file hashes, source counts, a Spark read, and a small managed Delta table write/read. A successful run leaves a one-row table ending in `_preflight` as setup evidence.

The remaining notebooks are intentionally incomplete. Run configuration and supplied support cells first, then create the numbered exercise cells with Build Buddy. Follow docs/COURSE_GUIDE.md rather than using Run All on the blank scaffolds.

When returning to a notebook after its Python state is lost, rerun configuration, support cells and already-completed prerequisite steps. The reset setting in 03-05 should stay False unless deliberately restarting the exercise. At the normal final checkpoint, that guard must protect the completed 80-sale state.

## 6. Save learning evidence to GitHub

Export each edited Databricks notebook as .ipynb and replace its matching file in notebooks/ in your local fork. Commit and push your work, using GitHub Desktop or your usual Git workflow. Add the evidence described in submissions/README.md. Never include passwords, tokens or account secrets. An exported notebook file is an artifact; its actual outputs/checks are the evidence that the work ran.

If a setup check fails, share the exact error with your trainer or Build Buddy before continuing. Common causes are an extra folder level in the volume path, missing permissions, unchanged configuration placeholders, or importing files from the instructor distribution instead of this learner starter.

Official references: [Databricks Serverless notebooks](https://docs.databricks.com/aws/en/compute/serverless/notebooks), [volume file access](https://docs.databricks.com/aws/en/volumes/volume-files), and [notebook import/export](https://docs.databricks.com/aws/en/notebooks/notebook-export-import).
