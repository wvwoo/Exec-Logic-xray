# AI usage log | سجل استخدام الذكاء الاصطناعي

## 2026-10-29 — Preparation and public repository setup

- **Purpose:** Assist with financial-data quality auditing, identifying source conflicts, developing controlled inclusion/exclusion rules, drafting documentation and an initial Python evidence gate.
- **Tools:** ChatGPT assisted with code drafting, arithmetic checks, methodological notes, source review organization and publication preparation.
- **Human decisions:** The project lead approved excluding insufficiently substantiated records from certified findings while retaining their reasons in a private audit trail.
- **Verification boundary:** Passing synthetic tests cannot verify actual PDF financial statements, reviewers' identities, geographic sampling, or final v6 estimates.
- **Current limitation:** A complete independently certified financial panel and reproducible final v6 results have **not** been validated for this public release.
- **Privacy:** Original statement PDFs, sensitive sources, and internal audit files are omitted from the public repository pending authorization.

This log is **provisional** and must be expanded to document significant model-generated analyses, verification steps, and any modifications to the final pipeline before contest submission.


## 2026-10-29 — Source-derived exploratory reproduction

- ChatGPT wrote and tested a Python source-data analysis, including five financial flags and a strict missing-data policy.
- Removed 2 fixed exclusions and 3 quarantined records; used only primary sample entries with an identified geographic group.
- Recomputed descriptive alerts on 92 latest-year associations: 22 flagged, 88 five-flag-complete.
- Computed 95% Wilson descriptive intervals, checked all 12 publicly released summary counts, and produced PDF, PPTX and PNG outputs locally.
- Derived a **non-identifying 17-cell aggregate table** to permit public reproducibility without financial statements, organization names or reviewer identities.
- **Human oversight:** Lead attests human reviews finished, but this agent has not received signed final review decisions tied to each row and therefore does not certify source-level audit completeness.
- **Validation:** Four private-analysis automated tests passed; matching 12/12 aggregate stats was independently checked against the source-derived outputs.
- **Publication boundary:** AI did not publish an X post, submit the competition form, or confirm the final design weights.
