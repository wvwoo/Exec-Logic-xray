#!/usr/bin/env python3
"""Reproducible privacy-minimized Exec Logic XRay aggregate analysis.

Two grouped counts are sufficient for the twelve published descriptive metrics.
No member-level data, financial amounts, professional audit signoffs, or v6
weights are embedded or implied by this script.
"""
import argparse
import csv
import json
import math
from pathlib import Path

GROUPS = ("المدن الكبرى", "المحافظات الأخرى")
REQUIRED = (
    "group", "associations", "confirmed_alert", "five_flags_evaluable",
    "alerts_among_five_evaluable", "critical_cash",
    "negative_unrestricted_net_assets",
)

def wilson(k, n):
    if n <= 0:
        return [None, None]
    z = 1.959963984540054
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [round(center - radius, 6), round(center + radius, 6)]

def read_counts(filename):
    with open(filename, encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 2 or not set(REQUIRED).issubset(rows[0]):
        raise ValueError("Expected two aggregate records with required columns")
    if {row["group"] for row in rows} != set(GROUPS):
        raise ValueError("Missing/duplicate/unexpected group")
    for row in rows:
        for name in REQUIRED[1:]:
            try:
                value = int(row[name])
                if str(value) != row[name].strip() or value < 0:
                    raise ValueError()
            except ValueError:
                raise ValueError("Invalid integer: " + name)
            row[name] = value
        n = row["associations"]
        complete = row["five_flags_evaluable"]
        if any(row[name] > n for name in REQUIRED[2:]):
            raise ValueError("Subcount exceeds associations")
        if (row["alerts_among_five_evaluable"] > complete or
            row["alerts_among_five_evaluable"] > row["confirmed_alert"] or
            row["confirmed_alert"] > row["alerts_among_five_evaluable"] + n - complete):
            raise ValueError("Contradictory missingness/alert counts")
    return rows

def produce(rows):
    aggregate = {key: sum(row[key] for row in rows) for key in REQUIRED[1:]}
    aggregate["group"] = "الكل"
    output = []
    for row in rows + [aggregate]:
        for metric, numerator, denominator in (
            ("confirmed_alert", "confirmed_alert", "associations"),
            ("full5_alert", "alerts_among_five_evaluable", "five_flags_evaluable"),
            ("critical_cash", "critical_cash", "associations"),
            ("negative_unrestricted_net_assets", "negative_unrestricted_net_assets", "associations"),
        ):
            k, n = row[numerator], row[denominator]
            output.append({
                "group": row["group"], "metric": metric, "n": n, "count": k,
                "share": round(k / n, 6) if n else None,
                "wilson95": wilson(k, n),
            })
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data_clean/indicator_totals.csv")
    parser.add_argument("--output", default="outputs/public_metrics.json")
    args = parser.parse_args()
    results = produce(read_counts(args.input))
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"metrics": len(results), "overall": results[8],
                      "limitation": "Descriptive only; not certified v6"},
                     ensure_ascii=False))
