#!/usr/bin/env python3
"""Conservative evidence gate for nonprofit license/year records.

This validates recorded approvals and preserves exclusions. It DOES NOT verify
that a signed review or the underlying PDF is authentic; people must do that.
Python >= 3.9; standard library only.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

HARD = {"استبعاد مثبت", "حجر هوية", "حجر تعارض المصدر"}
REQUIRED = {"الترخيص", "السنة", "حالة التقييم"}
REVIEW_REQUIRED = {
    "الترخيص", "السنة", "المراجع المستقل", "تاريخ المراجعة",
    "رابط أو ملف القائمة الأصلية", "رقم صفحة الدليل",
    "نتيجة المراجعة", "اعتماد قائد المشروع",
}


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        return list(reader), columns, list(reader.fieldnames or [])


def key(record):
    return record["الترخيص"].strip(), record["السنة"].strip()


def write_csv(path, rows, fields):
    with Path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def signed_decision(row):
    if not row:
        return False
    needed = [
        "المراجع المستقل", "تاريخ المراجعة",
        "رابط أو ملف القائمة الأصلية", "رقم صفحة الدليل",
    ]
    return (all(row.get(c, "").strip() not in ("", "لم يتم") for c in needed)
            and row.get("نتيجة المراجعة", "").strip() == "مقبول"
            and row.get("اعتماد قائد المشروع", "").strip() == "معتمد")


def run(source, decisions, output):
    source = Path(source)
    if not source.is_file():
        raise ValueError(f"Source CSV missing: {source}. Do not invent missing financial data.")
    records, fields, ordered = read_csv(source)
    if not REQUIRED.issubset(fields):
        raise ValueError("Missing required source columns: " + ", ".join(sorted(REQUIRED - fields)))
    if not records:
        raise ValueError("Source CSV has no rows")
    keys = [key(x) for x in records]
    if not all(a and b for a, b in keys):
        raise ValueError("Blank registration number or financial year")
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate registration number and financial year")

    review_map = {}
    if Path(decisions).is_file():
        review, review_fields, _ = read_csv(decisions)
        if not REVIEW_REQUIRED.issubset(review_fields):
            raise ValueError("Review decision file lacks mandatory columns")
        for row in review:
            k = key(row)
            if k in review_map:
                raise ValueError(f"Duplicate review for {k}")
            if k not in keys:
                raise ValueError(f"Review references unknown record {k}")
            review_map[k] = row

    approved, held, excluded = [], [], []
    for row in records:
        k = key(row)
        if row["حالة التقييم"].strip() in HARD:
            excluded.append(row)
        elif signed_decision(review_map.get(k)):
            approved.append(row)
        else:
            held.append(row)

    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    for basename, rows in (
        ("approved_panel.csv", approved),
        ("pending_evidence.csv", held),
        ("excluded_or_quarantined.csv", excluded),
    ):
        write_csv(out / basename, rows, ordered)
    summary = {
        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "total_records": len(records),
        "eligible_by_documented_decision_only": len(approved),
        "pending_independent_evidence": len(held),
        "excluded_or_quarantined": len(excluded),
        "source_pdf_authenticity_verified_by_script": False,
        "final_statistical_analysis_performed": False,
        "notice": "Human verification of original evidence, sampling and statistical estimates remains separate.",
    }
    (out / "quality_gate_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description="Audit-only evidence inclusion gate")
    parser.add_argument("--input", default="data_clean/consolidated_provisional.csv")
    parser.add_argument("--decisions", default="data_clean/review_decisions.csv")
    parser.add_argument("--out", default="outputs/qa")
    args = parser.parse_args()
    try:
        summary = run(args.input, args.decisions, args.out)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Quality gate stopped: {exc}\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
