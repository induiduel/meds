import unittest

from v2.core import cluster, graph, validate


class TestCluster(unittest.TestCase):
    def test_merges_near_duplicates(self):
        a = {"question_id": "a", "stem": "Parenteral uygulama için çok toksik olan antifungal ilaç hangisidir?",
             "options": {"A": "Nistatin", "B": "Ketokonazol"}, "terimler": ["antifungal", "nistatin"]}
        b = {"question_id": "b", "stem": "Parenteral uygulama için toksik olan antifungal ilaç hangisidir",
             "options": {"A": "Nistatin", "C": "Vorikonazol", "D": "Flukonazol"}, "terimler": ["antifungal"]}
        res = cluster.cluster_and_merge([a, b], threshold=0.5)
        self.assertEqual(len(res.groups), 1)
        self.assertEqual(len(res.merged), 1)
        merged = res.merged[0]
        self.assertGreaterEqual(len(merged["options"]), 3)  # şıklar birleşti
        self.assertEqual(merged["birlesik_parca_sayisi"], 2)

    def test_distinct_kept_separate(self):
        a = {"question_id": "a", "stem": "Kalp kapak hastalıkları nelerdir?", "options": {}}
        b = {"question_id": "b", "stem": "Böbrek yetmezliği evreleri nelerdir?", "options": {}}
        res = cluster.cluster_and_merge([a, b], threshold=0.6)
        self.assertEqual(len(res.groups), 0)


class TestGraph(unittest.TestCase):
    def test_nodes_and_edges(self):
        recs = [
            {"ders": "Tıbbi Patoloji", "konu": "Akut Enflamasyon", "kazanim": "Akut Enflamasyon",
             "terimler": ["enflamasyon", "nötrofil"]},
            {"ders": "Tıbbi Patoloji", "konu": "Akut Enflamasyon", "kazanim": "Akut Enflamasyon",
             "terimler": ["enflamasyon", "makrofaj"]},
        ]
        g = graph.build(recs, min_edge=1)
        s = graph.summary(g)
        self.assertGreater(s["dugum"], 0)
        self.assertGreater(s["kenar"], 0)


class TestOpenEnded(unittest.TestCase):
    def test_open_ended_not_blocking(self):
        rec = {"question_id": "x", "stem": "Nistatin hangi yolla kullanılır?", "options": {},
               "acik_uclu": True, "answer": "Topikal", "status": "raw", "issues": [], "evidence": ["s:p1:c0"]}
        res = validate.inspect_question(rec)
        self.assertNotIn("options_lt4", res.blocking)
        self.assertIn("acik_uclu", res.review)

    def test_closed_without_options_blocking(self):
        rec = {"question_id": "y", "stem": "Antifungal hangisidir?", "options": {"A": "x"},
               "acik_uclu": False, "status": "raw", "issues": [], "evidence": ["s:p1:c0"]}
        res = validate.inspect_question(rec)
        self.assertIn("options_lt4", res.blocking)


if __name__ == "__main__":
    unittest.main()
