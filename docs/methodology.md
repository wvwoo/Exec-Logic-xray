# Methodology and limitations

**Period:** financial years 2023–2025. **Unit:** one association, latest eligible financial year (with the previous consecutive year where available). **Geography:** major cities (Makkah, Jeddah, Taif) vs other governorates of the Makkah region.

## Population, frame and sample
- Registry: 1,309 associations in the Makkah region (National Center for Non-Profit Sector listing). Licence numbers are unique, with no old/new-format collisions and no duplicate names after normalization (checked 29 Oct 2026).
- Frame: 453 associations that have both a governance score and a derived governorate (263 major cities / 190 other governorates). The 617 associations without a derived governorate and the 202 without a governance score are outside the frame, so results do not generalize to all 1,309.
- Design: 16 strata (group × sector), 120 primary units (60 + 60) and 58 ordered reserves. Base weights equal N_h/n_h in all 16 strata (verified). Strata with N_h ≤ 2 are take-all.
- Nonresponse: 24 of the 120 primary units have no usable published statements. The release analyses primary respondents only, with no nonresponse adjustment.

## Five flags and alert tier
1. Deficit in the latest and the previous consecutive year. 2. Negative unrestricted net assets. 3. Cash below one month of expenses. 4. Revenue down ≥25%. 5. Total net assets down ≥25% (nonzero baseline).
**Alert tier:** total net assets < 0, or two or more flags. Missing inputs are "not evaluable" and are never counted as zero. These thresholds are descriptive screening rules, not validated failure predictors.

## Statistics
- Shares with Wilson 95% intervals, treated as descriptive, not design-based.
- Group comparison: difference in proportions with a Newcombe hybrid-score interval and a two-sided Fisher exact test. Results were cross-checked against SciPy.
- Robustness: four scenarios (see `data_clean/README.md`). The overall alert share ranges from 23.9% to 25.6%.
- An indicative stratified estimate (N_h / respondents_h) computed internally gives about 25.7%, consistent with the unweighted result. It is **not published as a finding** because the records and the nonresponse treatment are not certified.
- No predictive model is fitted. The alert tier is defined from the same flags, so a classifier would be circular, and 92 units with no observed failure outcomes cannot support a validated forecast. This is a deliberate choice under guide item 7 ("if possible").

## Known data issues (documented, not silently fixed)
- **Merge gap:** 43 candidate rows (23 licences) reached the evidence gate without their group or role, although every licence exists in the sample file with both. Earlier documents described these as "missing geography"; that description is inaccurate. The release (S0) keeps them out, and scenario S1 shows the effect of restoring them.
- **Geography risk:** 26 sample units were assigned to Makkah city from a generic mention of "Makkah" in the name or address, which may refer to the region. These assignments are pending manual confirmation.
- **Accounting differences:** activity-statement and balance-sheet arithmetic flags are review prompts. They can come from prior-year adjustments, fair-value movements, restatements, signs or transcription. No source value was altered to make an equation balance.

## Ethics
Signals are not judgments on any named organization. Detailed records remain in the team's restricted package.
