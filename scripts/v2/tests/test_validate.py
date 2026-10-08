import unittest

from v2.core import validate


def _q(**over):
    rec = {
        "question_id": "abc123abc123",
        "donem": 3, "kurul": 1, "ders": "Tıbbi Farmakoloji", "konu": None,
        "stem": "Parenteral uygulama için çok toksik olan antifungal ilaç hangisidir?",
        "options": {"A": "Kaspofungin", "B": "Ketokonazol", "C": "Nistatin", "D": "Vorikonazol", "E": "Flukonazol"},
        "answer": "C", "status": "verified", "issues": [], "evidence": ["x:p1:c0"],
    }
    rec.update(over)
    return rec


class TestQuestion(unittest.TestCase):
    def test_clean_is_ok(self):
        res = validate.inspect_question(_q())
        self.assertEqual(res.severity, validate.SEVERITY_OK, res.issues)

    def test_short_stem_blocking(self):
        res = validate.inspect_question(_q(stem="Prokaryottur?"))
        self.assertIn("stem_short", res.blocking)

    def test_answer_null_review(self):
        res = validate.inspect_question(_q(answer=None, status="fixed"))
        self.assertIn("answer_null", res.review)

    def test_answer_mismatch_blocking(self):
        res = validate.inspect_question(_q(answer="Z"))
        self.assertIn("answer_mismatch", res.blocking)

    def test_options_lt4_blocking(self):
        res = validate.inspect_question(_q(options={"A": "x", "B": "y"}))
        self.assertIn("options_lt4", res.blocking)

    def test_mojibake_blocking(self):
        res = validate.inspect_question(_q(stem="bulgularÄ±ndan yola çıkarak hangisi doğrudur?"))
        self.assertTrue(any(c.startswith("mojibake") for c in res.blocking), res.blocking)

    def test_status_inconsistent_review(self):
        res = validate.inspect_question(_q(stem="Kısa", status="verified"))
        self.assertIn("status_inconsistent", res.review)

    def test_ders_missing_review(self):
        res = validate.inspect_question(_q(ders=None))
        self.assertIn("ders_missing", res.review)


class TestChunkSource(unittest.TestCase):
    def test_chunk_empty_text(self):
        rec = {"chunk_id": "a:p1:c0", "source_id": "a", "page": 1, "text": "",
               "doc_type": "lecture_slide", "hash": "x"}
        res = validate.inspect_chunk(rec)
        self.assertIn("text_empty", res.blocking)

    def test_chunk_page_invalid(self):
        rec = {"chunk_id": "a:p0:c0", "source_id": "a", "page": 0, "text": "dolu metin",
               "doc_type": "lecture_slide", "hash": "x"}
        res = validate.inspect_chunk(rec)
        self.assertIn("page_invalid", res.blocking)

    def test_source_no_name(self):
        rec = {"source_id": "a", "drive_id": "b", "name": "", "doc_type": "lecture_slide",
               "md5": "d", "donem": 3}
        res = validate.inspect_source(rec)
        self.assertIn("name_empty", res.blocking)


class TestUnknownKind(unittest.TestCase):
    def test_raises(self):
        with self.assertRaises(ValueError):
            validate.inspect({}, "video")


if __name__ == "__main__":
    unittest.main()
