# Data lineage and compliance status

## Validation scope (2026-10-29)

The raw source is an internal 251-row license/year data join with SHA-256:
`6074ff54561ff4592df98d241dbba2db453dd8df2d38f7ad2ed3c1d3eb13248e`.
Restricted input bytes and named source documents are intentionally omitted from this public repository.

A deterministic local quality gate excludes/quarantines five records:
- 2040/2025: a planned budget, not actual financial statements
- 2075/2022: outside the 2023–2025 study range
- 478/2023: identity mismatch held for evidence
- 4060/2024: unresolved source conflict
- 4137/2024: unresolved statement discrepancy

The remaining 246 rows include 43 without confirmed geography and four reserve units. The grouped primary subset has 199 association/year rows. After choosing one latest year per association, there are 92 analysis units.

## Flags and data minimization

The private analysis calculates five financial flags and treats unavailable trend information as **missing**, not false. The public distribution is collapsed to 17 aggregated combinations of four binary attributes (confirmed alert, complete five-flag availability, low cash, negative unrestricted net assets). This allows exact publication of 12 descriptive proportions without disclosing names, IDs, or individual financial amounts.

The public dataset is source-derived, not synthetic, and is **only adequate to reproduce the released proportions**, not to re-check PDF source extraction or all five underlying financial flags.

## Verification and uncertainty

- Four private arithmetic/analysis unit tests passed locally; the public aggregate summary reproduces 12/12 reported metrics.
- The project lead says independent human review is complete. Signed review decisions were not included with this run; therefore this repo does **not** certify the audit trail.
- All intervals are **descriptive Wilson intervals**, not a survey-design confidence interval. We did not reuse old sample weights for added associations.
- Differences between groups should not be generalized to the whole register, and there is no causal or validated predictive claim.

## Remaining mandatory contest steps
Upload executive PDF and PowerPoint, show a reproducible end-to-end source/analysis process suitable for judging, add the X announcement URL, and submit through the organizer's official channel by October 30, 2026.

See `docs/submission_checklist.md`.
