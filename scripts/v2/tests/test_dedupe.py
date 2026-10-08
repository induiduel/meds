import unittest

from v2.core import dedupe


def _q(stem, opts):
    return {"stem": stem, "options": opts}


class TestDedupe(unittest.TestCase):
    def test_exact_duplicate(self):
        opts = {"A": "x", "B": "y", "C": "z", "D": "t", "E": "u"}
        recs = [_q("Antifungal ilaç hangisidir?", opts), _q("Antifungal ilaç hangisidir?", opts)]
        res = dedupe.deduplicate(recs)
        self.assertEqual(len(res.unique), 1)
        self.assertEqual(res.duplicate_count, 1)

    def test_near_duplicate(self):
        recs = [
            _q("Parenteral uygulama için çok toksik olan antifungal ilaç hangisidir?",
               {"A": "Nistatin", "B": "Ketokonazol", "C": "Vorikonazol", "D": "Kaspofungin", "E": "Flukonazol"}),
            _q("Parenteral uygulama için çok toksik olan antifungal ilaç hangisidir? ",
               {"A": "Nistatin", "B": "Ketokonazol", "C": "Vorikonazol", "D": "Kaspofungin", "E": "Flukonazol"}),
        ]
        res = dedupe.deduplicate(recs, near_threshold=0.9)
        # aynı normalize içerik → tam id eşitliği zaten yakalar
        self.assertEqual(len(res.unique), 1)

    def test_distinct_kept(self):
        recs = [
            _q("Kalp kapak hastalıkları nelerdir? A) x B) y C) z D) t E) u".split("?")[0], {"A": "x", "B": "y", "C": "z", "D": "t", "E": "u"}),
            _q("Böbrek yetmezliği evreleri nelerdir?", {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5"}),
        ]
        res = dedupe.deduplicate(recs, near_threshold=0.95)
        self.assertEqual(len(res.unique), 2)
        self.assertEqual(res.duplicate_count, 0)


if __name__ == "__main__":
    unittest.main()
