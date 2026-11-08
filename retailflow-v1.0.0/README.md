# RetailFlow learner dataset distribution

Dataset version 1.0.0; learner distribution 1.0.0. Seven source CSVs are byte-identical to the original RetailFlow release. This distribution removes instructor-only documents and places 17 expected-result CSVs under checks/expected/. Its manifest is specific to these learner files.

Upload this folder's contents into the assigned /Volumes/<catalog>/<schema>/<volume>/retailflow-v1.0.0/ folder, preserving data/, docs/ and checks/. The root repository SETUP.md gives the full instructions.

Read data/ as source inputs and checks/expected/ only as verification outputs. The clean and dirty initial files are alternatives. The incremental file stays in data/ for exact path consistency and is introduced on Day 2. Currency is INR; blank customer fields mean guests.
