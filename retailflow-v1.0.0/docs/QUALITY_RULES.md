# Cleaning contract

Apply these rules in order to the alternative `sales_dirty.csv` route. Preserve raw strings and source_row_id in Bronze. Blank means null; do not treat null as numeric zero generally.

1. Trim surrounding whitespace from string columns. Uppercase store_id, product_id, customer_id and payment_method. Map the literal customer_id UNKNOWN to null. A null customer is an allowed guest. Unknown nonblank customers are rejected.
2. Parse dates as strict yyyy-MM-dd, or strict dd/MM/yyyy only when slashes are present. Thus D-003 is 1 January, never 1 March. Impossible calendar dates are rejected.
3. Parse integer quantity and record_version. Require both >= 1. Parse unit_price and discount_pct as decimals. Fill missing unit_price from the matching product list_price; fill missing discount_pct with 0. These two fill rules are explicit teaching assumptions, not general production advice. Never overwrite supplied prices.
4. Require sale_id, source_row_id, sale_date, store_id and product_id. Check store/product foreign keys, optional customer key, positive unit_price, discount_pct in [0,100], and payment_method in UPI/CARD/CASH. Reject failed records with reasons. Do not invent missing sale IDs or unknown products/stores.
5. After normalization, deduplicate by (sale_id, record_version). Identical business payloads are replays; keep the lowest source_row_id within this file. Exclude source_row_id from payload comparison. If the same key/version has conflicting business values, quarantine all conflicting candidates for investigation; do not silently choose one. This fixture has no such conflicts.
6. For current Silver, retain the highest valid record_version per sale_id. Carry the winning source_row_id as provenance. Differences in provenance do not change business equality.

## Exact row accounting
68 raw rows = 60 accepted unique sales + 2 dropped duplicates + 6 quarantined rows. Six of the 60 accepted rows require repair; they are not an extra six rows. D-061 and D-062 duplicate repaired D-001 and D-002 after normalization. Quarantine D-063 through D-068. The machine-readable rejected rows and reason codes are in `checks/expected/quarantine.csv`.

Expected clean business values equal sales_batch_01.csv after excluding source_row_id. The dirty route keeps D-* provenance while the clean route keeps B01-* provenance. Do not compare the provenance fields as business values.

## Returns validation and joins
return_id is unique, sale_id must exist in the current checkpoint, return_date must be on/after sale_date, and return_quantity must be positive. Cumulative returned quantity per sale cannot exceed sold quantity. refund_amount equals returned quantity times original discounted unit price, rounded to two decimals HALF_UP. This fixture has at most one return per sale, but aggregate returns by sale_id before joining them to sales in a reusable pipeline to avoid multiplying sales amounts. Never inner join sales to returns: that would remove sales with no returns.
