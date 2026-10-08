import unittest

from v2.core import segment

SAMPLE = """12. Aşağıdakilerden hangisi parenteral uygulama için çok toksik olan antifungaldir?
A) Kaspofungin
B) Ketokonazol
C) Nistatin
D) Vorikonazol
E) Flukonazol
Cevap: C

13. Glukozun hücre içine alınmasını sağlayan taşıyıcı hangisidir?
A) GLUT1
B) GLUT2
C) GLUT4
D) SGLT1
E) SGLT2
Cevap: C
"""


class TestParseQuestions(unittest.TestCase):
    def test_two_questions(self):
        qs = segment.parse_questions(SAMPLE)
        self.assertEqual(len(qs), 2)
        self.assertEqual(qs[0]["no"], 12)
        self.assertEqual(set(qs[0]["options"]), {"A", "B", "C", "D", "E"})
        self.assertEqual(qs[0]["options"]["C"], "Nistatin")
        self.assertEqual(qs[0]["answer"], "C")

    def test_inline_options(self):
        text = "1. Enzim hangisidir? A) Amilaz B) Lipaz C) Pepsin D) Tripsin E) Renin"
        qs = segment.parse_questions(text)
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0]["options"]["B"], "Lipaz")

    def test_negative_flag(self):
        text = "1. Aşağıdakilerden hangisi yanlıştır? A) x B) y C) z D) t E) u"
        qs = segment.parse_questions(text)
        self.assertEqual(qs[0]["soru_tipi"], "negatif")

    def test_short_stem_dropped(self):
        self.assertEqual(segment.parse_questions("1. kısa A) x B) y C) z"), [])

    def test_dash_numbering(self):
        text = "97-Hangisi nabızsız ritimlerden değildir?\nA) Bradikardi\nB) Nabızsız elektriksel aktivite\nC) Ventriküler fibrilasyon\nD) Torsades de pointes\nE) Asistol\n"
        qs = segment.parse_questions(text)
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0]["no"], 97)
        self.assertEqual(set(qs[0]["options"]), {"A", "B", "C", "D", "E"})

    def test_dash_range_not_question(self):
        # "1-2" gibi aralıklar soru numarası olarak BÖLÜNMEMELİ (tek blok kalır)
        qs = segment.parse_questions("1-2 arası sayfa")
        self.assertTrue(all(q["no"] is None for q in qs))


if __name__ == "__main__":
    unittest.main()
