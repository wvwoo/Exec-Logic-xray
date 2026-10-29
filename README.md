# Exec Logic | XRay Financial Early Warning

> **Release update (29 Oct 2026):** [Reproducible disclosure-safe release and review boundaries](docs/RELEASE_2026-10-29.md) now includes a two-row public dataset, a deterministic Python pipeline and tests. **The leader reports team human/financial/accounting review complete, but signed row-level certification is not independently shown; the updated Ritaj source contains unresolved differences.** PDF, deck and screenshot/video are prepared locally but are not yet uploaded here. Official organizer submission and X publication are not evidenced. The earlier status notes below document development history, not the current binary upload state.


**الفريق:** Exec Logic  
**المشروع:** أشعة إكس مالية — الإنذار المالي المبكر لجمعيات منطقة مكة المكرمة  
**Submission status:** Work in progress — **final v6 financial/statistical results are NOT certified**.

## السؤال البحثي | Research question

هل تختلف مؤشرات الصحة المالية والإفصاح للجمعيات الأهلية بين المدن الكبرى والمحافظات الأخرى في منطقة مكة المكرمة؟ وما الإشارات المالية المبكرة التي تستدعي المراجعة؟

This research evaluates nonprofit financial disclosure and financial-health indicators across geographic groups. An early-warning indicator is descriptive, **not** an established prediction of insolvency or an allegation against any specific association.

## Evidence, review and publication policy

- Technical extraction, reconciliation and QA have been performed, but the complete final panel is not independently certified.
- The project lead approved **documented methodological exclusion** of records with insufficient evidence; original sources and exclusion reasons are retained in the private audit trail.
- Original financial PDFs, private review records, and unpublished/sensitive datasets are **not** included in this public repository.
- Published final statistics, figures and reports must be reproducible from the approved release, never copied from an earlier version.

## Repository layout

- `scripts/run_quality_gate.py` — transparent inclusion/exclusion evidence gate (initial audit utility)
- `tests/test_quality_gate.py` — tests based exclusively on synthetic cases
- `docs/methodology.md` — methodology and limits
- `docs/submission_checklist.md` — deliverables against the official contest guide
- `data_clean/` — only appropriately authorized and certified cleaned data
- `outputs/figures/` — final figures once reproduced from the approved panel
- `report/` — executive summary once figures/results are approved
- `ai_usage_log.md` — declared AI assistance, verification and limitations

## Testing

The published quality-gate checks require Python 3.9+ (standard library only):

```bash
python -m unittest discover -s tests -v
```

To run the gate with a **local, authorized** source CSV (not published here):

```bash
python scripts/run_quality_gate.py --input data_clean/consolidated_provisional.csv --out outputs/qa
```

The gate checks logged decisions and duplicate license/year keys; it **cannot** authenticate original PDFs or provide a completed statistical v6 analysis.

## Outstanding contest deliverables

`analysis.ipynb` or `scripts/run_analysis.py`, certified data, reproducible final figures, `report/executive_summary.pdf`, the fully completed AI-use log, and publication/submission evidence are outstanding. **This repository is not yet a final competition submission.**

[دليل مسابقة تحليل البيانات للقطاع غير الربحي](https://drive.google.com/file/d/1XjBjiYW_UCdVuZqicMA3O23pdpHbqdte/view)

**Maintained by Exec Logic.**

## 29 October 2026 descriptive findings (reproduced)

**These are NOT finalized survey-weighted v6 estimates.** The project lead reports completion of human review; linking signed decisions to each included record and final sample weights is still an outstanding publication gate.

- 251 association-year source rows; 5 fixed exclusions / temporary quarantines
- 246 remaining candidate rows; 43 missing geographic group and 4 reserve-role records
- 199 grouped primary association-year rows, reduced to latest year for 92 associations
- 22/92 = **23.9%** confirmed early-warning signal in the available sample (descriptive Wilson interval 16.4–33.6%)
- Large cities: 12/49 = **24.5%**; other governorates: 10/43 = **23.3%**
- 88/92 have all five indicator inputs evaluable; four are incomplete

To reproduce **all 12 aggregate metrics** with Python standard library:

```sh
python scripts/run_public_analysis.py --input data_clean/aggregated_indicator_counts.csv --output outputs/public_metrics.json
python -m unittest discover -s tests -v
```

The 17-row aggregation intentionally excludes organization names, IDs, financial amounts and internal reviewer details. It reproduces released descriptive percentages only, not source-PDF extraction or design-based inference.

- [Arabic findings](report/executive_summary.md)
- [Data lineage and privacy limitations](docs/data_lineage.md)
- [X post draft / publication status](docs/X_post_draft.md)
- [Official delivery checklist](docs/submission_checklist.md)

**PDF executive report and PowerPoint deck are prepared outside GitHub and still need to be uploaded to this repository.** Neither an X post nor official competition form submission has been completed through this conversation.
