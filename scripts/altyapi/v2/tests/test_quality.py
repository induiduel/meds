import unittest

from v2.core import quality


class TestQuestionGate(unittest.TestCase):
    def test_real_questions_pass(self):
        for s in [
            "Aşağıdakilerden hangisi parenteral uygulama için çok toksiktir?",
            "Antifungal hangisidir?",
            "Hangisi tromboz için yüksek risk grubundadır?",
            "Aşağıdakilerden hangisi AIDS ile ilişkili durumlardan değildir?",
            "Yaşlılıkta en sık görülen anemi tipi hangisidir?",
        ]:
            self.assertTrue(quality.is_question_stem(s), s)

    def test_headings_and_options_rejected(self):
        for s in ["KOMPLİKASYONLAR", "Bradikardi", "Nistatin", "FİBROEDENOM",
                  "Kaslar=", "✓Etki Mekanizması", "Giriş, Tanımlar Ve Temel İlkeler"]:
            self.assertFalse(quality.is_question_stem(s), s)

    def test_lecture_content_rejected(self):
        s = "3°C veya bir saat boyunca ≥38°C febril nötropeni (FN) en sık etken mikroorganizmalar E. coli"
        self.assertFalse(quality.is_question_stem(s))

    def test_merged_block_rejected(self):
        s = "Dokuda formol hangi işlem için uygulanır? A) Dehidratasyon B) Saydamlaştırma C) Fiksasyon D) Sertleştirme E) Boyama"
        self.assertFalse(quality.is_question_stem(s))

    def test_exam_header_rejected(self):
        s = "2025-2026 DÖNEM 3 FİNAL SINAVI acil tıp 97-Hangisi nabızsız ritimlerden değildir?"
        self.assertFalse(quality.is_question_stem(s))

    def test_too_long_rejected(self):
        self.assertFalse(quality.is_question_stem("Ne " + ("çok uzun bir metin " * 40) + "?"))


if __name__ == "__main__":
    unittest.main()
