import unittest

from v2.stages import s2_normalize

LECTURE = """1. Enflamasyonun kardinal bulguları
2. Vazodilatasyon ve artmış geçirgenlik
3. Nötrofil migrasyonu
"""

EXAM = """5. Antifungal hangisidir?
A) Nistatin
B) Ketokonazol
C) Vorikonazol
D) Flukonazol
E) Kaspofungin
Cevap: A
"""

SLIDE_WITH_Q = """Örnek soru:
1. Hücre zarındaki taşıyıcı hangisidir?
A) GLUT1
B) GLUT2
C) GLUT4
D) SGLT1
E) SGLT2
"""


def _doc(text, doc_type):
    return {"source": {"source_id": "s", "path": "p", "md5": "m", "name": "n", "donem": 3,
                       "doc_type": doc_type},
            "pages": [{"page": 1, "text": text}]}


class TestBuildQuestions(unittest.TestCase):
    def test_lecture_list_not_questions(self):
        qs = s2_normalize.build_questions(_doc(LECTURE, "lecture_slide"))
        self.assertEqual(qs, [])

    def test_lecture_real_question_kept(self):
        qs = s2_normalize.build_questions(_doc(SLIDE_WITH_Q, "lecture_slide"))
        self.assertEqual(len(qs), 1)
        self.assertEqual(set(qs[0]["options"]), {"A", "B", "C", "D", "E"})

    def test_exam_open_ended_kept(self):
        text = "1. Nistatin hangi yolla kullanılır?\nCevap: Topikal\n"
        qs = s2_normalize.build_questions(_doc(text, "past_question"))
        self.assertEqual(len(qs), 1)


if __name__ == "__main__":
    unittest.main()
