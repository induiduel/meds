import unittest

from v2.core.lectures import stems
from v2.stages import s13_study


class StudyHelpersTest(unittest.TestCase):
    def test_strip_answer_leak(self):
        cases = {
            "Tromboksan A2\nCevap: C": "Tromboksan A2",
            "Coronavirüs Cevap E": "Coronavirüs",
            "Klebsiella pneumoniae CEVAP: C": "Klebsiella pneumoniae",
            "Mortalite (Cevap anahtarı: B) 📌 Kaynak: 2018": "Mortalite",
            "Formalin --- [patoloji final.txt] Dokuda formol": "Formalin",
            "Faktör X -": "Faktör X",
            "Gram pozitif kok": "Gram pozitif kok",
        }
        for raw, want in cases.items():
            self.assertEqual(s13_study._strip_leak(raw), want, raw)

    def test_garbage_pearl(self):
        self.assertTrue(s13_study._GARBAGE_PEARL.match("S • ı"))
        self.assertTrue(s13_study._GARBAGE_PEARL.match("D • 1"))
        self.assertFalse(s13_study._GARBAGE_PEARL.match("VHL geni (3p25) defekti esastır."))

    def test_attribution_neutralized(self):
        note = "Prof. Dr. Hikmet Keleş amfide özellikle vurguladı: Korteksde yerleşir."
        self.assertEqual(s13_study._ATTRIBUTION.sub("Ders notu bağlamı: ", note),
                         "Ders notu bağlamı: Korteksde yerleşir.")
        self.assertIsNone(s13_study._ATTRIBUTION.match("Ders slaytlarında vurgulanan temel içerik"))

    def test_stems_fold_and_drop_stopwords(self):
        self.assertEqual(stems("Trombüsün ve fibrin ağı"), ["tromb", "fibri", "agi"])
        self.assertNotIn("ve", stems("trombüs ve emboli"))
        self.assertEqual(stems("Şizofreni"), ["sizof"])


if __name__ == "__main__":
    unittest.main()
