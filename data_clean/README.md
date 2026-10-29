# data_clean — data dictionary

Both files contain **aggregate counts only** (no names, licences, amounts or documents).

## indicator_totals.csv (released sample, scenario S0)

| Column | Meaning |
|---|---|
| `group` | `المدن الكبرى` (Makkah, Jeddah and Taif cities) or `المحافظات الأخرى` (other governorates of the Makkah region) |
| `associations` | analysis units: one association, latest eligible financial year in 2023–2025 |
| `confirmed_alert` | units in the alert tier: total net assets < 0, **or** at least two of the five flags |
| `five_flags_evaluable` | units for which all five flags could be computed |
| `alerts_among_five_evaluable` | alert-tier units among those |
| `critical_cash` | cash and equivalents < one month of total expenses |
| `negative_unrestricted_net_assets` | unrestricted net assets < 0 |

The five flags: (1) deficit in the latest and the previous consecutive year; (2) negative unrestricted net assets; (3) cash below one month of expenses; (4) revenue down ≥25% on the previous year; (5) total net assets down ≥25% on the previous year. Missing inputs give "not evaluable", never zero.

## How the counts were built (cleaning steps, performed on the restricted panel)

1. Union of the team's extraction sources: 251 association-year records keyed by licence + year, with zero duplicate keys.
2. Five documented decisions: two fixed exclusions (an estimated budget, not actual statements; a year outside 2023–2025) and three precautionary holds (one identity conflict, two unresolved source conflicts). Result: 246 candidates.
3. Old and new licence formats are reconciled through an explicit, documented crosswalk. Names are never used to infer identity.
4. Keep primary sample units with a group assignment (199 records), then the latest year per association (92 units).
5. Compute the five flags and the tier, then aggregate by group.

## sensitivity_totals.csv

The same columns, plus `scenario` and `description`:

- **S0:** the release.
- **S1:** group and role restored from the approved sample file for 43 rows the evidence-gate merge had left blank. Every one of those licences is in the sample file. This adds 4 associations and corrects the latest or previous year of 3 more.
- **S1b:** S1, with one more row held because its reported change in net assets has the opposite sign to revenue minus expenses.
- **S3:** S0 without the associations whose latest or previous year is one of the ten pending accounting-difference cases.
