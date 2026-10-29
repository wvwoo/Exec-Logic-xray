"""Synthetic-only test data; no financial statements or identifiable entities."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_quality_gate import run


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / "source.csv"
        self.decisions = self.root / "decisions.csv"
        self.out = self.root / "out"
        self.rows = [
            {"الترخيص": "101", "السنة": "2024", "حالة التقييم": "قابل للمراجعة"},
            {"الترخيص": "102", "السنة": "2024", "حالة التقييم": "استبعاد مثبت"},
            {"الترخيص": "103", "السنة": "2025", "حالة التقييم": "قابل للمراجعة"},
        ]
        self.write(self.src, self.rows)

    @staticmethod
    def write(path, rows):
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    def test_unsigned_rows_are_not_approved(self):
        results = run(self.src, self.decisions, self.out)
        self.assertEqual(results["eligible_by_documented_decision_only"], 0)
        self.assertEqual(results["pending_independent_evidence"], 2)
        self.assertEqual(results["excluded_or_quarantined"], 1)

    def test_complete_documented_review_unlocks_only_that_record(self):
        self.write(self.decisions, [{
            "الترخيص": "101", "السنة": "2024", "المراجع المستقل": "Test reviewer",
            "تاريخ المراجعة": "2026-10-29", "رابط أو ملف القائمة الأصلية": "mock.pdf",
            "رقم صفحة الدليل": "4", "نتيجة المراجعة": "مقبول",
            "اعتماد قائد المشروع": "معتمد",
        }])
        results = run(self.src, self.decisions, self.out)
        self.assertEqual(results["eligible_by_documented_decision_only"], 1)
        self.assertEqual(results["pending_independent_evidence"], 1)
        self.assertEqual(results["excluded_or_quarantined"], 1)
        self.assertFalse(results["source_pdf_authenticity_verified_by_script"])

    def test_duplicate_keys_fail_closed(self):
        self.write(self.src, [self.rows[0], self.rows[0]])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            run(self.src, self.decisions, self.out)

    def test_missing_input_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            run(self.root / "missing.csv", self.decisions, self.out)


if __name__ == "__main__":
    unittest.main()
