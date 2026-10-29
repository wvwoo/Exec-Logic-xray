"""Synthetic and expected aggregate checks; does not inspect private financial files."""
import csv,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_public_analysis import summarize,wilson
ROOT=Path(__file__).resolve().parents[1]
class PublicAnalysisTests(unittest.TestCase):
    def test_wilson(self):
        self.assertEqual(wilson(0,0),(None,None))
        a,b=wilson(22,92)
        self.assertAlmostEqual(a,0.163551,places=5)
        self.assertAlmostEqual(b,0.335621,places=5)
    def test_published_counts(self):
        out=summarize(ROOT/'data_clean/aggregated_indicator_counts.csv')
        by={(r['group'],r['metric']):r for r in out}
        self.assertEqual((by[('الكل','confirmed_red')]['n'],by[('الكل','confirmed_red')]['count']),(92,22))
        self.assertEqual((by[('المدن الكبرى','confirmed_red')]['n'],by[('المدن الكبرى','confirmed_red')]['count']),(49,12))
        self.assertEqual((by[('المحافظات الأخرى','confirmed_red')]['n'],by[('المحافظات الأخرى','confirmed_red')]['count']),(43,10))
        self.assertEqual((by[('الكل','full5_red')]['n'],by[('الكل','full5_red')]['count']),(88,21))
        self.assertEqual((by[('الكل','cash_crit')]['n'],by[('الكل','cash_crit')]['count']),(92,16))
        self.assertEqual((by[('الكل','unres_neg')]['n'],by[('الكل','unres_neg')]['count']),(92,17))
        self.assertEqual(len(out),12)
    def test_malformed_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.csv'
            path.write_text('group,confirmed_red,full5,cash_crit,unres_neg,count\nالمدن الكبرى,1,1,0,0,-2\n',encoding='utf-8')
            with self.assertRaises(ValueError):summarize(path)
if __name__=='__main__':unittest.main()
