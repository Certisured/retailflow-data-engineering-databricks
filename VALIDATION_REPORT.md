# Starter repository validation

Prepared 8 November 2026. Seven source CSVs and all 17 expected-result CSVs were compared byte-for-byte with the previously validated RetailFlow release. The seven notebook files parse and their Python cells compile. The setup notebook is supplied complete; all 32 business exercise cells are comments-only. Check paths consistently use checks/expected/.

The supplied Python cleaner was executed locally against the actual dirty file and matched 60 accepted unique sales, 2 duplicate drops, 6 exact quarantined rows/reasons and 6 repairs. Accepted business records match the canonical initial file. Incremental reconstruction matches the final expected snapshot; reference metric arithmetic and source relationships were checked locally. Both manifests, every internal Markdown link, and archive extraction were verified.

The package contains no completed instructor business notebooks, authoring scripts, human facilitation answer keys, authentication files or pre-completed learner submissions. Expected CSV outputs and reusable support functions are intentionally public for checking the exercises.

Spark/Delta execution, notebook import, workspace permissions and GitHub-hosted/raw-download access have not been validated here. The public repository must be checked after upload. The instructor must rehearse in Databricks before teaching.

Before editing, run `python -B scripts/verify_repo.py --starter`; afterward, run `python -B scripts/verify_repo.py` to validate pinned data and notebook structure while allowing exercise changes.
