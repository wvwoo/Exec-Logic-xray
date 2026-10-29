import unittest
from scripts.run_analysis import read_counts, produce, wilson

class TestAnalysis(unittest.TestCase):
    def test_reproduce(self):
        summary = produce(read_counts("data_clean/indicator_totals.csv"))
        self.assertEqual(len(summary), 12)
        self.assertEqual((summary[8]["count"], summary[8]["n"]), (22, 92))
        self.assertEqual((summary[0]["count"], summary[0]["n"]), (12, 49))
        self.assertEqual((summary[4]["count"], summary[4]["n"]), (10, 43))

    def test_missing_indicators_not_zero(self):
        rows = read_counts("data_clean/indicator_totals.csv")
        self.assertEqual(sum(r["five_flags_evaluable"] for r in rows), 88)
        self.assertEqual(sum(r["associations"] for r in rows), 92)

    def test_wilson(self):
        low, high = wilson(22, 92)
        self.assertLess(low, 22 / 92)
        self.assertGreater(high, 22 / 92)

if __name__ == "__main__":
    unittest.main()
