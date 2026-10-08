import unittest
from unittest import mock

from v2.stages import s9_answer


class TestFillAnswers(unittest.TestCase):
    def _rec(self):
        return {
            "question_id": "q1", "stem": "Antifungal hangisidir?",
            "options": {"A": "Nistatin", "B": "Ketokonazol", "C": "Vorikonazol", "D": "Flukonazol", "E": "Kaspofungin"},
            "answer": None, "evidence": ["s:p1:c0"], "issues": ["answer_null"], "status": "needs_fix",
        }

    def test_fills_with_citation(self):
        rec = self._rec()
        kanit = "Parenteral uygulama için çok toksik olan ve sadece topikal kullanılan antifungal ilaç nistatindir."
        by_chunk = {"s:p1:c0": kanit}
        fake = {"answer": "A", "explanation": "Nistatin parenteral toksik topikal kullanılır",
                "alinti": "sadece topikal kullanılan antifungal ilaç nistatindir"}
        with mock.patch.object(s9_answer.faz14, "is_reviewed", return_value=False), \
             mock.patch.object(s9_answer.llm, "chat_json", return_value=fake):
            counts = s9_answer.fill_answers([rec], by_chunk=by_chunk, limit=1, log=lambda *_: None)
        self.assertEqual(counts["dolduruldu"], 1)
        self.assertEqual(rec["answer"], "A")
        self.assertIn("answer_kaynak", rec)
        self.assertNotIn("answer_null", rec["issues"])

    def test_rejects_without_support(self):
        rec = self._rec()
        by_chunk = {"s:p1:c0": "Tamamen alakasız bir metin; başka konular hakkında."}
        fake = {"answer": "A", "explanation": "uydurma gerekçe xyzabc", "alinti": "olmayan alıntı"}
        with mock.patch.object(s9_answer.faz14, "is_reviewed", return_value=False), \
             mock.patch.object(s9_answer.llm, "chat_json", return_value=fake):
            counts = s9_answer.fill_answers([rec], by_chunk=by_chunk, limit=1, log=lambda *_: None)
        self.assertEqual(counts["dolduruldu"], 0)
        self.assertIsNone(rec["answer"])

    def test_skips_faz14(self):
        rec = self._rec()
        with mock.patch.object(s9_answer.faz14, "is_reviewed", return_value=True):
            counts = s9_answer.fill_answers([rec], by_chunk={"s:p1:c0": "x"}, limit=1, log=lambda *_: None)
        self.assertEqual(counts["faz14_atlandi"], 1)


if __name__ == "__main__":
    unittest.main()
