import unittest

from v2.core import schema


def _valid_question() -> dict:
    return {
        "question_id": "abc123abc123",
        "source_id": "c4259dc9087e",
        "donem": 3,
        "kurul": 1,
        "ders": "Tıbbi Farmakoloji",
        "konu": None,
        "stem": "Parenteral uygulama için çok toksik olan antifungal ilaç hangisidir?",
        "options": {"A": "Kaspofungin", "B": "Ketokonazol", "C": "Nistatin"},
        "answer": "C",
        "explanation": None,
        "status": "verified",
        "issues": [],
        "evidence": ["c4259dc9087e:p525:c0"],
        "pipeline_generation": "v2_core",
        "tags": ["deneme"],
        "created_at": "2026-10-07T00:00:00",
    }


class TestQuestionSchema(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate(_valid_question(), "question"), [])

    def test_missing_required(self):
        rec = _valid_question()
        del rec["stem"]
        errors = schema.validate(rec, "question")
        self.assertTrue(any("stem" in e for e in errors), errors)

    def test_bad_status(self):
        rec = _valid_question()
        rec["status"] = "saçma"
        errors = schema.validate(rec, "question")
        self.assertTrue(any("status" in e for e in errors), errors)

    def test_bad_type(self):
        rec = _valid_question()
        rec["donem"] = "üç"
        self.assertFalse(schema.is_valid(rec, "question"))


class TestChunkSchema(unittest.TestCase):
    def test_valid(self):
        rec = {
            "chunk_id": "00f441c79eb6:p1:c0",
            "source_id": "00f441c79eb6",
            "page": 1,
            "text": "MSS İlaçları Farmakolojisine Giriş",
            "doc_type": "lecture_slide",
            "hash": "1b8a900ca12e916b",
        }
        self.assertEqual(schema.validate(rec, "chunk"), [])

    def test_missing_text(self):
        rec = {"chunk_id": "a:p1:c0", "source_id": "a", "page": 1, "doc_type": "lecture_slide", "hash": "x"}
        errors = schema.validate(rec, "chunk")
        self.assertTrue(any("text" in e for e in errors), errors)


class TestSourceSchema(unittest.TestCase):
    def test_valid(self):
        rec = {
            "source_id": "00f441c79eb6",
            "drive_id": "1Ullkdi8IH6RA37H4mAH_z7hcjG2dfpT9",
            "name": "21 MSS İlaçları",
            "doc_type": "lecture_slide",
            "md5": "eb1639773c55271e579eb89813636d57",
            "donem": 3,
        }
        self.assertEqual(schema.validate(rec, "source"), [])

    def test_bad_doctype(self):
        rec = {
            "source_id": "a", "drive_id": "b", "name": "c", "doc_type": "video",
            "md5": "d", "donem": 3,
        }
        errors = schema.validate(rec, "source")
        self.assertTrue(any("doc_type" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
