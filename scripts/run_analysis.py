#!/usr/bin/env python3
"""Exec Logic | XRay — privacy-minimized, deterministic descriptive analysis.

Inputs (aggregate counts only; no names, licences, amounts or PDFs):
  data_clean/indicator_totals.csv     two group rows of the released sample (S0)
  data_clean/sensitivity_totals.csv   the same six counts under documented robustness scenarios

Outputs:
  outputs/public_metrics.json         12 released metrics with descriptive Wilson 95% intervals
  outputs/group_comparison.json       major cities minus other governorates: difference,
                                      Newcombe 95% interval and two-sided Fisher exact p-value
  outputs/sensitivity_metrics.json    alert share per scenario (robustness of the headline)

It does NOT recreate source-statement extraction, survey weights or human sign-off.
Standard library only (Python 3.9+).
"""
import argparse
import csv
import json
import math
from pathlib import Path

REQUIRED = ("group", "associations", "confirmed_alert", "five_flags_evaluable",
            "alerts_among_five_evaluable", "critical_cash", "negative_unrestricted_net_assets")
GROUPS = ("المدن الكبرى", "المحافظات الأخرى")
Z = 1.959963984540054


def wilson(k, n):
    if n <= 0:
        return [None, None]
    p = k / n
    den = 1 + Z * Z / n
    mid = (p + Z * Z / (2 * n)) / den
    delta = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return [round(mid - delta, 6), round(mid + delta, 6)]


def _validate(r):
    for key in REQUIRED[1:]:
        try:
            v = int(r[key])
            assert str(v) == str(r[key]).strip() and v >= 0
        except (ValueError, AssertionError):
            raise ValueError("Invalid nonnegative integer: " + key)
        r[key] = v
    n, complete = r["associations"], r["five_flags_evaluable"]
    if any(r[k] > n for k in REQUIRED[2:]):
        raise ValueError("Subcount larger than total")
    if r["alerts_among_five_evaluable"] > complete or r["alerts_among_five_evaluable"] > r["confirmed_alert"]:
        raise ValueError("Inconsistent five-flag subcounts")
    if r["confirmed_alert"] > r["alerts_among_five_evaluable"] + (n - complete):
        raise ValueError("Impossible alert missingness")
    return r


def read_counts(filename):
    with open(filename, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 2 or not set(REQUIRED).issubset(rows[0]):
        raise ValueError("Expected exactly two rows and required columns")
    if {r["group"] for r in rows} != set(GROUPS):
        raise ValueError("Group coverage mismatch")
    return [_validate(r) for r in rows]


def produce(rows):
    output = []
    combined = {k: sum(row[k] for row in rows) for k in REQUIRED[1:]}
    combined["group"] = "الكل"
    for row in rows + [combined]:
        for metric, num, den in (
                ("confirmed_alert", "confirmed_alert", "associations"),
                ("full5_alert", "alerts_among_five_evaluable", "five_flags_evaluable"),
                ("critical_cash", "critical_cash", "associations"),
                ("negative_unrestricted_net_assets", "negative_unrestricted_net_assets", "associations")):
            n, k = row[den], row[num]
            output.append({"group": row["group"], "metric": metric, "n": n, "count": k,
                           "share": round(k / n, 6) if n else None, "wilson95": wilson(k, n)})
    return output


def fisher_two_sided(a, n1, c, n2):
    """Two-sided Fisher exact test for k1=a of n1 vs k2=c of n2 (sum of tables as or less likely)."""
    k = a + c
    N = n1 + n2
    denom = math.comb(N, k)

    def p(x):
        return math.comb(n1, x) * math.comb(n2, k - x) / denom
    lo, hi = max(0, k - n2), min(k, n1)
    p_obs = p(a)
    return min(1.0, sum(p(x) for x in range(lo, hi + 1) if p(x) <= p_obs * (1 + 1e-7)))


def newcombe(k1, n1, k2, n2):
    """Newcombe (1998) hybrid score interval for p1 - p2."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return [round(lo, 6), round(hi, 6)]


def compare_groups(rows):
    a, b = rows[0], rows[1]
    if a["group"] != GROUPS[0]:
        a, b = b, a
    out = []
    for metric, num, den in (("confirmed_alert", "confirmed_alert", "associations"),
                             ("critical_cash", "critical_cash", "associations"),
                             ("negative_unrestricted_net_assets", "negative_unrestricted_net_assets", "associations")):
        k1, n1, k2, n2 = a[num], a[den], b[num], b[den]
        out.append({"metric": metric, "major_cities": [k1, n1], "other_governorates": [k2, n2],
                    "difference": round(k1 / n1 - k2 / n2, 6), "newcombe95": newcombe(k1, n1, k2, n2),
                    "fisher_exact_p_two_sided": round(fisher_two_sided(k1, n1, k2, n2), 6),
                    "note": "Descriptive comparison of an unweighted sample; not causal, not population inference."})
    return out


def read_sensitivity(filename):
    with open(filename, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or not {"scenario", "description"}.issubset(rows[0]):
        raise ValueError("Sensitivity file needs scenario and description columns")
    scenarios = {}
    for r in rows:
        scenarios.setdefault(r["scenario"], {"description": r["description"], "rows": []})["rows"].append(_validate(dict(r)))
    for name, s in scenarios.items():
        if {r["group"] for r in s["rows"]} != set(GROUPS) or len(s["rows"]) != 2:
            raise ValueError("Scenario must have both groups exactly once: " + name)
    return scenarios


def sensitivity(scenarios):
    out = []
    for name, s in scenarios.items():
        tot_n = sum(r["associations"] for r in s["rows"])
        tot_k = sum(r["confirmed_alert"] for r in s["rows"])
        by = {r["group"]: r for r in s["rows"]}
        out.append({"scenario": name, "description": s["description"], "associations": tot_n, "alerts": tot_k,
                    "share": round(tot_k / tot_n, 6), "wilson95": wilson(tot_k, tot_n),
                    "major_cities": [by[GROUPS[0]]["confirmed_alert"], by[GROUPS[0]]["associations"]],
                    "other_governorates": [by[GROUPS[1]]["confirmed_alert"], by[GROUPS[1]]["associations"]],
                    "fisher_exact_p_two_sided": round(fisher_two_sided(by[GROUPS[0]]["confirmed_alert"], by[GROUPS[0]]["associations"],
                                                                       by[GROUPS[1]]["confirmed_alert"], by[GROUPS[1]]["associations"]), 6)})
    return out


def _write(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default="data_clean/indicator_totals.csv")
    ap.add_argument("--output", default="outputs/public_metrics.json")
    ap.add_argument("--sensitivity-input", default="data_clean/sensitivity_totals.csv")
    ap.add_argument("--comparison-output", default="outputs/group_comparison.json")
    ap.add_argument("--sensitivity-output", default="outputs/sensitivity_metrics.json")
    args = ap.parse_args()
    rows = read_counts(args.input)
    results = produce(rows)
    _write(args.output, results)
    comparison = compare_groups(rows)
    _write(args.comparison_output, comparison)
    sens = None
    if Path(args.sensitivity_input).exists():
        sens = sensitivity(read_sensitivity(args.sensitivity_input))
        _write(args.sensitivity_output, sens)
    print(json.dumps({"metrics": len(results), "all_alerts": results[8], "group_difference_alert": comparison[0],
                      "sensitivity_alert_share_range": [min(s["share"] for s in sens), max(s["share"] for s in sens)] if sens else None,
                      "notice": "Descriptive estimates only; no source-level verification or survey weights"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
