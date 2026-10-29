#!/usr/bin/env python3
"""Regenerate the four public figures from the aggregate-only inputs (matplotlib required).

No identifying data is read. Colours: validated categorical pair (blue / orange);
text in neutral ink; Wilson 95% intervals drawn as thin whiskers.
"""
import argparse
import json
from pathlib import Path

from run_analysis import read_counts, read_sensitivity, sensitivity, wilson

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
NAMES = {"المدن الكبرى": "Major cities (Makkah, Jeddah, Taif)", "المحافظات الأخرى": "Other governorates"}


def _style(plt):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE})


def _finish(fig, ax, title, subtitle, path):
    ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold", pad=22)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, color=INK2, fontsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, dpi=180)


def generate(input_path, sens_path, output_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _style(plt)
    rows = read_counts(input_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 01 — confirmed alert share with Wilson intervals
    fig, ax = plt.subplots(figsize=(8, 4.6))
    xs = range(len(rows))
    for x, r in zip(xs, rows):
        k, n = r["confirmed_alert"], r["associations"]
        lo, hi = wilson(k, n)
        ax.bar(x, k / n * 100, width=0.5, color=BLUE)
        ax.plot([x, x], [lo * 100, hi * 100], color=INK2, linewidth=1.2)
        ax.text(x + 0.27, k / n * 100, f"{k/n*100:.1f}%  ({k}/{n})", va="center", color=INK, fontsize=10)
    ax.set_xticks(list(xs), [NAMES[r["group"]] for r in rows])
    ax.set_ylim(0, 45)
    ax.set_ylabel("Associations with a confirmed signal (%)")
    _finish(fig, ax, "Early-warning signals are similar in both groups",
            "Unweighted, latest year per association, n = 92. Whiskers: descriptive Wilson 95% interval.",
            out / "01_alert_prevalence.png")
    plt.close(fig)

    # 02 — two component indicators by group
    fig, ax = plt.subplots(figsize=(8, 4.6))
    fields = [("critical_cash", "Cash below one month of expenses", BLUE),
              ("negative_unrestricted_net_assets", "Negative unrestricted net assets", ORANGE)]
    w = 0.34
    for i, (f, label, col) in enumerate(fields):
        for x, r in zip(xs, rows):
            v = r[f] / r["associations"] * 100
            bx = x + (i - 0.5) * (w + 0.02)
            ax.bar(bx, v, width=w, color=col, label=label if x == 0 else None)
            ax.text(bx, v + 0.8, f"{v:.1f}%", ha="center", color=INK, fontsize=9)
    ax.set_xticks(list(xs), [NAMES[r["group"]] for r in rows])
    ax.set_ylim(0, 32)
    ax.set_ylabel("Share of associations (%)")
    ax.legend(frameon=False, loc="upper left", labelcolor=INK2)
    _finish(fig, ax, "Low cash appears more often outside the major cities",
            "Cash: 12.2% vs 23.3% (Fisher exact p = 0.18, not statistically distinguishable). Unweighted.",
            out / "02_indicator_comparison.png")
    plt.close(fig)

    # 03 — indicator completeness
    fig, ax = plt.subplots(figsize=(8, 4.2))
    total = sum(r["associations"] for r in rows)
    complete = sum(r["five_flags_evaluable"] for r in rows)
    ax.barh([1, 0], [complete, total - complete], height=0.5, color=[BLUE, "#b8b7b1"])
    for y, v, lab in [(1, complete, "All five indicators evaluable"), (0, total - complete, "At least one indicator missing (not treated as zero)")]:
        ax.text(v + 1, y, f"{v}", va="center", color=INK, fontsize=10)
    ax.set_yticks([1, 0], ["All five evaluable", "At least one missing"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Associations")
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Indicator completeness", loc="left", color=INK, fontsize=12, fontweight="bold", pad=22)
    ax.text(0, 1.02, f"n = {total}. Missing inputs are reported, never imputed as healthy.", transform=ax.transAxes, color=INK2, fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "03_coverage.png", dpi=180)
    plt.close(fig)

    # 04 — robustness of the headline across documented scenarios
    if sens_path and Path(sens_path).exists():
        sens = sensitivity(read_sensitivity(sens_path))
        labels = {"S0": "S0  Released sample", "S1": "S1  Merge gap repaired from sample file",
                  "S1b": "S1b S1 + one sign-inconsistent row held", "S3": "S3  Without 10 pending difference cases"}
        fig, ax = plt.subplots(figsize=(8, 4.2))
        for y, s in enumerate(reversed(sens)):
            lo, hi = s["wilson95"]
            ax.plot([lo * 100, hi * 100], [y, y], color=INK2, linewidth=1.2)
            ax.plot(s["share"] * 100, y, "o", color=BLUE if s["scenario"] == "S0" else ORANGE, markersize=8,
                    markeredgecolor=SURFACE, markeredgewidth=2)
            ax.text(hi * 100 + 0.8, y, f"{s['share']*100:.1f}%  ({s['alerts']}/{s['associations']})", va="center", color=INK, fontsize=9)
        ax.set_yticks(range(len(sens)), [labels.get(s["scenario"], s["scenario"]) for s in reversed(sens)])
        ax.set_xlim(10, 45)
        ax.set_xlabel("Associations with a confirmed signal (%) — Wilson 95% interval")
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_title("Headline is robust to documented data issues", loc="left", color=INK, fontsize=12, fontweight="bold", pad=22)
        ax.text(0, 1.02, "Share stays between 23.9% and 25.6% in every scenario.", transform=ax.transAxes, color=INK2, fontsize=9)
        fig.tight_layout()
        fig.savefig(out / "04_sensitivity.png", dpi=180)
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data_clean/indicator_totals.csv")
    parser.add_argument("--sensitivity-input", default="data_clean/sensitivity_totals.csv")
    parser.add_argument("--output-dir", default="outputs/figures")
    args = parser.parse_args()
    generate(args.input, args.sensitivity_input, args.output_dir)
