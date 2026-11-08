# Checkpoints you should be able to explain

| Stage | Expected result |
|---|---|
| S0001 | Asha, Rice 1 kg, RetailFlow Mumbai; quantity 1; INR 80.00 sales before returns |
| S0003 version 1 | Gross 450.00, discount 45.00, net sales 405.00 |
| Initial clean route | 60 sales |
| Alternative dirty route | 68 raw = 60 unique accepted + 2 duplicate drops + 6 quarantined; six accepted rows repaired |
| Enrichment | Still 60 sales; guest S0006 retained |
| Product coverage | P012 Desk Lamp remains visible with zero units |
| Initial report | Net sales 14,456.00; refunds 272.00; net revenue 14,184.00 |
| First incremental application | 20 inserts, 1 update, 2 no-ops; 80 current sales |
| S0003 version 2 | Quantity 4; net sales 540.00 |
| S0080 | Business date stays 2 January 2026, despite arriving in batch 02 |
| Replaying batch 02 | 23 no-ops; all current fields and provenance unchanged |
| Replaying batch 01 afterward | 60 no-ops; S0003 cannot revert to version 1 |
| Final report | Net sales 19,874.00; refunds 937.00; net revenue 18,937.00 |

Expected CSVs under retailflow-v1.0.0/checks/expected are reference outputs for comparison. They are not source inputs and not a substitute for building your own calculations. Initial returns are available_batch 01 only; final returns include both 01 and 02. Keep those markers as text with their leading zeroes.
