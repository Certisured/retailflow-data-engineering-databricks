# The second delivery and repeat-safe processing

Batch 01 arrives on 4 January; batch 02 arrives on 6 January 2026. These are teaching arrival dates, not columns in the source files. Load dimension files once and keep them fixed.

`sales_batch_02.csv` has exactly 23 physical rows:
- B02-001 through B02-020: 20 new sale IDs S0061–S0080.
- B02-021 and B02-022: unchanged S0001 v1 and S0002 v1 replays. Ignore in current Silver.
- B02-023: S0003 v2, quantity 4 instead of 3. Update its Silver record; do not insert a second transaction.
- S0080 (B02-020) is one of the 20 new sales, dated 2 January. It is a late arrival, not a 21st new sale.

Process all valid arrivals by business key sale_id and version. Ignore lower versions and identical equal-version payloads; apply a higher version as an update; insert new IDs. Deduplicate a batch before a Delta MERGE, since multiple source candidates for a target key can be ambiguous. Equal-version conflicts follow QUALITY_RULES.md. Keep original provenance on ignored replays. The source-row identity is (file name, source_row_id); the business identity is sale_id.

Current Silver counts: 60 before batch 02, 80 after batch 02, 80 after replaying batch 02. For the first merge: 20 inserts, 1 update, 2 no-ops. On a full replay: 0 inserts, 0 updates, 23 no-ops. Replaying batch 01 after batch 02 must not revert S0003 v2.

Bronze may retain physical arrivals and ingestion metadata; reporting uses Silver current state. There are 83 arrivals across the two clean sales files, 81 distinct (sale_id, version) pairs, and 80 current sales. The dirty route has a different raw arrival count and the same final business state.

Enable returns R001–R003 initially and all six returns after batch 02. There is no incremental returns file: available_batch controls visibility. Do not use returns for S0065 or S0080 before those sales exist.

Rebuild Gold from current Silver for this tiny fixture. If updating partitions incrementally, recompute old affected sale dates as well: 1 January changes because of S0003 and 2 January because of S0080. Sale-date summaries attribute refunds back to the original sale date; cash-date summaries record refunds on return_date. Both expected views are supplied and must not be confused.
