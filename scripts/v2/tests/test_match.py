import unittest

from v2.core import match


class TestMatch(unittest.TestCase):
    def test_search_relevance(self):
        docs = [
            {"id": "a:p1:c0", "source_id": "a", "text": "Antifungal ilaçlar: nistatin topikal, sistemik için amfoterisin B."},
            {"id": "b:p1:c0", "source_id": "b", "text": "Beta blokörler hipertansiyonda kullanılır."},
        ]
        index = match.Bm25Index(docs)
        hits = index.search("antifungal nistatin", k=2)
        self.assertTrue(hits)
        self.assertEqual(hits[0]["doc"]["id"], "a:p1:c0")

    def test_match_question_adds_evidence(self):
        docs = [{"id": "a:p1:c0", "source_id": "a", "text": "Nistatin parenteral uygulama için toksiktir, sadece topikal kullanılır."}]
        index = match.Bm25Index(docs)
        q = {"stem": "Parenteral için toksik antifungal hangisidir?",
             "options": {"A": "Nistatin", "B": "Ketokonazol"}}
        hits = match.match_question(q, index, k=1)
        self.assertEqual(hits[0]["chunk_id"], "a:p1:c0")
        self.assertIn("support_ratio", hits[0])

    def test_empty_query(self):
        index = match.Bm25Index([{"id": "a", "text": "x"}])
        self.assertEqual(index.search("   ", k=3), [])


if __name__ == "__main__":
    unittest.main()
