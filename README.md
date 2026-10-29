> **Judges | latest public release (29 October 2026):** [Final submission ZIP](https://drive.google.com/file/d/1lmeiSs69c-zh_-iC3tIOhOui67bKc4pe/view) · [Executive PDF](https://drive.google.com/file/d/1GHePlPwA8HrToeLsao-PtcuIvDZRLD2b/view) · [Presentation](https://docs.google.com/presentation/d/1NJmHH7dWFyqZyhiaFApOkql8IYf10IXz/edit) · [Full judges folder](https://drive.google.com/drive/folders/1-HjJpeF6G4X9wwha12VWV5Rbp5LWZvW9). **Public source is descriptive and unweighted; individual financial audit signoffs are not evidenced.** The X post and official competition form receipt are separate actions.

# Exec Logic | أشعة إكس مالية — XRay Financial Early Warning

**Team:** Exec Logic · **Project:** early financial-warning signals for nonprofit associations in the Makkah region · **Financial years:** 2023–2025
**Release:** competition release candidate, 29–30 October 2026 — *descriptive, unweighted, privacy-minimized; not an audit opinion and not a certified survey-weighted (v6) estimate.*

## السؤال | Question
هل تختلف مؤشرات الضغط المالي المبكر للجمعيات الأهلية بين المدن الكبرى (مكة المكرمة، جدة، الطائف) والمحافظات الأخرى في منطقة مكة المكرمة؟ وأي الإشارات تستحق أولوية المتابعة؟

## How to run (Python 3.9+, standard library only)

```bash
python scripts/run_analysis.py          # writes outputs/public_metrics.json, group_comparison.json, sensitivity_metrics.json
python -m unittest discover -s tests -v # 9 tests
python scripts/make_figures.py          # optional, needs matplotlib: regenerates outputs/figures/*.png
```

Run order: `data_clean/` → `scripts/run_analysis.py` → `outputs/` → `scripts/make_figures.py` → `outputs/figures/` → `report/`.

## Folder layout

| Path | Content |
|---|---|
| `README.md` | this file |
| `scripts/run_analysis.py` | the analysis: 12 released metrics, Wilson 95% intervals, group comparison (difference, Newcombe interval, Fisher exact test), robustness scenarios |
| `scripts/make_figures.py` | regenerates the four figures from the same inputs |
| `tests/test_analysis.py` | 9 unit tests (input validation, known statistical values, output reproduction) |
| `data_clean/indicator_totals.csv` | released aggregate counts (two group rows) |
| `data_clean/sensitivity_totals.csv` | the same counts under four documented scenarios |
| `data_clean/README.md` | data dictionary and how the counts were derived |
| `outputs/*.json` | generated results |
| `outputs/figures/` | `01_alert_prevalence.png`, `02_indicator_comparison.png`, `03_coverage.png`, `04_sensitivity.png`, `project_screenshot.png` |
| `report/executive_summary.pdf` | executive report (Arabic); `report/ExecLogic_XRay_Presentation.pptx` deck; `report/XRay_Demo_NoNarration.mp4` silent walkthrough |
| `ai_usage_log.md` | AI use, commands and what was verified |
| `docs/` | methodology, review and release status, submission status, X-post draft |

## Results (descriptive, unweighted)

| | Major cities | Other governorates | All |
|---|---|---|---|
| Associations | 49 | 43 | 92 |
| Confirmed early-warning signal | 12 (24.5%) | 10 (23.3%) | 22 (23.9%, Wilson 95%: 16.4–33.6%) |
| Cash below one month of expenses | 6 (12.2%) | 10 (23.3%) | 16 (17.4%) |
| Negative unrestricted net assets | 9 (18.4%) | 8 (18.6%) | 17 (18.5%) |

- **Group difference:** +1.2 points for major cities; Newcombe 95% interval −16.3 to +18.2 points; Fisher exact p = 1.00. The two groups are not distinguishable in this sample. Low cash is more frequent outside the major cities (23.3% vs 12.2%, p = 0.18), a monitoring lead, not a finding.
- **Completeness:** 88/92 associations have all five indicators evaluable; four are incomplete and are never treated as healthy.
- **Robustness:** the headline stays between 23.9% and 25.6% across four documented scenarios (`outputs/sensitivity_metrics.json`, figure 04), including repairing a data-merge gap and removing every association touched by the ten pending accounting differences.
- Signals are monitoring prompts, not predictions of failure and not allegations against any organization.

## Data, review and limitations

- **Source:** financial statements published by the associations (2023–2025), the National Center for Non-Profit Sector registry (1,309 associations), a stratified sampling frame of 453 (263 major cities / 190 other governorates), 120 primary + 58 reserve sample units.
- **Pipeline:** 251 association-year records → 5 documented exclusions or holds → 246 candidates → 199 grouped primary records → latest year per association → 92 units.
- **Review status:** according to the project lead, Exec Logic members completed the human, financial and accounting reviews. Additional automated checks were run, with exceptions and the limits of the available evidence documented. Individual signed record-level approvals are not part of this public release, and the evidence gate still lists the records as pending independent approval. The results are therefore released as descriptive and preliminary.
- **Not done:** design-weighted inference, nonresponse adjustment (24 of 120 primary units have no usable statements), causal claims, failure prediction.
- Full method and caveats: `docs/methodology.md`, `docs/review_and_release_status.md`.

## Privacy

Only aggregate counts are published: no association names, licence numbers, amounts, source PDFs, reviewer identities or exception lists. Detailed evidence stays in the team's restricted audit package, in line with the competition rule on confidential data.

## Submission

Repository: https://github.com/wvwoo/Exec-Logic-xray · Competition guide: https://drive.google.com/file/d/1XjBjiYW_UCdVuZqicMA3O23pdpHbqdte/view
The official submission is the X-post URL plus the repository URL entered through the organizer's channel. A commit or a ZIP is not proof of submission.
