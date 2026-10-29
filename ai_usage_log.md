# AI use disclosure | سجل استخدام الذكاء الاصطناعي

## Tools and roles
- **Claude (Anthropic)**, several sessions from 26 to 29 October 2026. It assisted with: extracting figures from published statements (every such row is flagged "needs review" at source), reading the v5 archive, writing the analysis and test code, cross-version arithmetic checks, figures, report and presentation drafts.
- **Humans:** according to the project lead, Exec Logic members completed the human, financial and accounting reviews. AI output is not an audit opinion.

## Session of 29 October 2026 (integrity and release check): what was run
| Step | Command / method | Result |
|---|---|---|
| Package integrity | `sha256sum -c SHA256SUMS.txt` | all files match |
| Public tests (before changes) | `python -m unittest discover -s tests -v` | 4/4 pass |
| Independent recomputation of the 12 metrics | re-implemented the five flags and tier from the candidate panel (restricted) | 22/92, 12/49, 10/43, 88 evaluable, 21 among evaluable, cash 6/10, unrestricted 9/8: **all match** |
| Registry and sample validation | uniqueness, licence-format collisions, frame = 453 (263/190), N_h/n_h weights in 16 strata, reserve order | consistent; merge gap of 43 rows found; reserve-order skips in 2 strata need a recorded reason |
| Contributor workbook re-check | arithmetic on workbook cells, key match to v5 | 29 / 13 flags reproduced; conflict counts depend on field scope |
| New statistics | Fisher exact, Newcombe interval; values cross-checked with SciPy | match |
| Public tests (after changes) | `python -m unittest discover -s tests -v` | 9/9 pass |

## What was not verified by AI
Original statement PDFs for every record (3 PDFs were inspected directly in earlier sessions); signed reviewer decisions; the original algorithm behind the sample fingerprint; the X post and official submission.

## Data handling
The confidential panel was processed only to produce aggregate counts. No names, licences, amounts or documents appear in the public release.
