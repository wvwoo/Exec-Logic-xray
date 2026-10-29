# Exec Logic | XRay Financial Early Warning

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