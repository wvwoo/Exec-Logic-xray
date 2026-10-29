import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_analysis import (compare_groups, fisher_two_sided, newcombe, produce, read_counts,
                                  read_sensitivity, sensitivity, wilson)

HEADER = ("group,associations,confirmed_alert,five_flags_evaluable,alerts_among_five_evaluable,"
          "critical_cash,negative_unrestricted_net_assets\n")


def _tmp(text):
    f = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".csv", delete=False)
    with f:
        f.write(text)
    return f.name


class PublicAnalysisTests(unittest.TestCase):
    def test_wilson_bounds(self):
        lo, hi = wilson(22, 92)
        self.assertLess(lo, 22 / 92)
        self.assertGreater(hi, 22 / 92)
        self.assertAlmostEqual(lo, 0.163551, places=5)
        self.assertAlmostEqual(hi, 0.335621, places=5)

    def test_public_sample(self):
        metrics = produce(read_counts("data_clean/indicator_totals.csv"))
        self.assertEqual(len(metrics), 12)
        self.assertEqual((metrics[8]["count"], metrics[8]["n"]), (22, 92))
        self.assertEqual((metrics[0]["count"], metrics[0]["n"]), (12, 49))
        self.assertEqual((metrics[4]["count"], metrics[4]["n"]), (10, 43))

    def test_released_json_matches_recomputation(self):
        released = json.loads(Path("outputs/public_metrics.json").read_text(encoding="utf-8"))
        self.assertEqual(released, produce(read_counts("data_clean/indicator_totals.csv")))

    def test_missingness_not_zero(self):
        d = read_counts("data_clean/indicator_totals.csv")
        self.assertEqual(sum(x["five_flags_evaluable"] for x in d), 88)
        self.assertEqual(sum(x["associations"] for x in d), 92)

    def test_bad_count(self):
        name = _tmp(HEADER + "المدن الكبرى,-1,0,0,0,0,0\nالمحافظات الأخرى,1,0,0,0,0,0\n")
        try:
            with self.assertRaises(ValueError):
                read_counts(name)
        finally:
            Path(name).unlink()

    def test_fisher_known_values(self):
        # Symmetric table must give p = 1; extreme table must be small.
        self.assertAlmostEqual(fisher_two_sided(5, 10, 5, 10), 1.0, places=9)
        self.assertLess(fisher_two_sided(10, 10, 0, 10), 0.001)
        # Classic tea-tasting table (3 of 4 vs 1 of 4): two-sided p = 0.485714
        self.assertAlmostEqual(fisher_two_sided(3, 4, 1, 4), 0.485714, places=5)

    def test_newcombe_contains_difference(self):
        lo, hi = newcombe(12, 49, 10, 43)
        self.assertLess(lo, 12 / 49 - 10 / 43)
        self.assertGreater(hi, 12 / 49 - 10 / 43)

    def test_group_difference_not_significant(self):
        alert = compare_groups(read_counts("data_clean/indicator_totals.csv"))[0]
        self.assertGreater(alert["fisher_exact_p_two_sided"], 0.05)
        self.assertLess(alert["newcombe95"][0], 0)
        self.assertGreater(alert["newcombe95"][1], 0)

    def test_sensitivity_consistent_with_release(self):
        sc = read_sensitivity("data_clean/sensitivity_totals.csv")
        base = read_counts("data_clean/indicator_totals.csv")
        s0 = sorted(sc["S0"]["rows"], key=lambda r: r["group"])
        self.assertEqual([r["confirmed_alert"] for r in s0], [r["confirmed_alert"] for r in sorted(base, key=lambda r: r["group"])])
        shares = [s["share"] for s in sensitivity(sc)]
        self.assertTrue(all(0.2 < s < 0.3 for s in shares))


if __name__ == "__main__":
    unittest.main()
