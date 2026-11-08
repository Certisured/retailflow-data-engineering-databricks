# The RetailFlow story

You have joined RetailFlow as its first data engineer. Manager Priya receives daily sales files from ten stores in India. She needs a report she can trust: which store sells most, which products never sell, how discounts affect sales, and how returns affect the money retained.

The first delivery contains 60 sales for 1–3 January 2026. An alternative store export has typing errors and repeated rows. The next delivery arrives on 6 January with sales for 4–5 January, one sale from 2 January that arrived late, two repeated sales, and one correction to an old sale.

Think of Bronze as an untouched inbox, Silver as checked business records, and Gold as answers to business questions. Keep rejected records in a quarantine table with reasons so a store can investigate them. An empty customer means a guest purchase, which still counts as a valid sale.

## Understand a record
S0001 is **one** Rice 1 kg at INR 80.00, no discount, bought at ST01 by C001 on 1 January. R001 returns that one unit the next day and refunds INR 80.00. Its contribution to lifetime net revenue is zero.

S0003 sells three Tea 250 g packs at INR 150.00 each with a 10% discount. Gross is 450.00, discount is 45.00, and net sales are 405.00. In batch 02 the store corrects quantity to four: the latest net sales become 540.00. Keep the old version in Bronze but replace it in Silver.

## Deliberate simplifications
One sale_id represents one product line and one transaction; there are no multi-line baskets. Units are whole numbers. All prices use INR and stay fixed in the product master. Historical sale price remains authoritative when supplied. There is no GST, shipping, cost of goods, inventory balance, profit, exchange rate, personal contact information, or customer age. Do not claim profit from revenue. P012 Desk Lamp has no sales: use a left join to show its zero.

All dates are store-local dates in Asia/Kolkata; no timestamp conversion is needed. Arrival is described by file/batch, separate from business sale date. Returns are positive events, never negative sale quantities.
