import unittest

from v2.core import textnorm
from v2.stages import s1_extract


class TestPathMeta(unittest.TestCase):
    def test_kurul_ders_donem(self):
        p = "/x/donem3/3. Sınıf/Kurul 1/D3K1/Tıbbi Patoloji/neoplazi.pdf"
        meta = s1_extract.infer_path_meta(p)
        self.assertEqual(meta.get("kurul"), 1)
        self.assertEqual(meta.get("donem"), 3)
        self.assertEqual(meta.get("ders"), "Tıbbi Patoloji")

    def test_kurul_only(self):
        meta = s1_extract.infer_path_meta("/a/gecen_yil_d3/kurul 5/patoloji/x.pdf")
        self.assertEqual(meta.get("kurul"), 5)

    def test_no_match(self):
        self.assertEqual(s1_extract.infer_path_meta("/tmp/serbest.pdf"), {})


class TestBangOcr(unittest.TestCase):
    def test_bang_to_i(self):
        self.assertEqual(textnorm.repair_ocr("Kals!ton!n"), "Kalsitonin")

    def test_real_exclamation_preserved(self):
        self.assertEqual(textnorm.repair_ocr("Dikkat! Önemli"), "Dikkat! Önemli")


if __name__ == "__main__":
    unittest.main()
