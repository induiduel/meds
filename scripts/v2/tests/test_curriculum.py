import unittest
from unittest import mock

from v2.core import curriculum, faz14


class TestCurriculumSynthetic(unittest.TestCase):
    def _c(self):
        tax = {"kurullar": [{"kurul": 1, "konular": [
            {"ders": "Tıbbi Patoloji", "konu": "Akut Enflamasyon"},
            {"ders": "Tıbbi Farmakoloji", "konu": "Antifungal İlaçlar"},
        ]}]}
        cur = {"committees": {"TIP310": {"kurul": 1, "core_topics": ["Akut Enflamasyon", "Antifungal İlaçlar"]}}}
        return curriculum.Curriculum(tax, cur)

    def test_maps_konu(self):
        c = self._c()
        with mock.patch.object(curriculum, "MIN_KONU_SKOR", 0.0), mock.patch.object(curriculum, "MIN_KAZANIM_SKOR", 0.0):
            m = c.map({"stem": "Parenteral antifungal ilaç hangisidir?", "options": {"A": "Nistatin"}, "kurul": 1})
        self.assertEqual(m.get("konu"), "Antifungal İlaçlar")
        self.assertEqual(m.get("ders"), "Tıbbi Farmakoloji")

    def test_maps_kazanim(self):
        c = self._c()
        with mock.patch.object(curriculum, "MIN_KONU_SKOR", 0.0), mock.patch.object(curriculum, "MIN_KAZANIM_SKOR", 0.0):
            m = c.map({"stem": "Akut enflamasyon bulgusu", "options": {}, "kurul": 1})
        self.assertIsNotNone(m.get("kazanim"))

    def test_terms(self):
        c = self._c()
        m = c.map({"stem": "Antifungal ilaç", "options": {}, "kurul": 1})
        self.assertIn("antifungal", m.get("terimler", []))


class TestCurriculumReal(unittest.TestCase):
    def test_loads_real_files(self):
        cur = curriculum.load()
        self.assertIsNotNone(cur, "taxonomy/curriculum dosyaları okunamadı")
        m = curriculum.map_question({"stem": "Parenteral antifungal ilaç hangisidir?", "options": {"A": "Nistatin"}, "kurul": 1})
        self.assertIn("terimler", m)


class TestFaz14(unittest.TestCase):
    def test_content_key_stable(self):
        a = faz14.content_key("Soru?", {"A": "x", "B": "y"})
        b = faz14.content_key("Soru?", {"B": "y", "A": "x"})
        self.assertEqual(a, b)

    def test_known_reviewed(self):
        rec = {"stem": "Parenteral uygulama için çok toksik olan ve sadece topikal olarak kullanılan antifungal ilaç aşağıdakilerden hangisidir?",
               "options": {"A": "Kaspofungin", "B": "Ketokonazol", "C": "Nistatin", "D": "Vorikonazol", "E": "Flukonazol"}}
        self.assertTrue(faz14.is_reviewed(rec))

    def test_unknown_not_reviewed(self):
        rec = {"stem": "Bu tamamen uydurma bir soru köküdür zzz", "options": {"A": "q", "B": "w"}}
        self.assertFalse(faz14.is_reviewed(rec))


if __name__ == "__main__":
    unittest.main()
