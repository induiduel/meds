import unittest
from unittest import mock

from v2.core import match, vector


class _StubVectorIndex:
    def __init__(self, docs, model_name=None):
        self.docs = list(docs)

    def available(self):
        return False

    def search(self, query, k=5):
        return []


class TestTiers(unittest.TestCase):
    def test_high(self):
        self.assertEqual(match.guven_tier(0.8), "yuksek")

    def test_mid(self):
        self.assertEqual(match.guven_tier(0.4), "orta")

    def test_low(self):
        self.assertEqual(match.guven_tier(0.1), "dusuk")

    def test_margin_downgrades_high(self):
        self.assertEqual(match.guven_tier(0.9, margin=0.05), "orta")


class TestBuildIndex(unittest.TestCase):
    def test_bm25_when_vector_off(self):
        idx = vector.build_index([{"id": "a", "text": "x"}], use_vector=False)
        self.assertIsInstance(idx, match.Bm25Index)

    def test_hybrid_when_vector_on(self):
        with mock.patch.object(vector, "VectorIndex", _StubVectorIndex):
            idx = vector.build_index([{"id": "a", "text": "x"}], use_vector=True)
        self.assertIsInstance(idx, vector.HybridIndex)


class _FakeVector:
    def __init__(self, ranked_ids):
        self._ranked = ranked_ids

    def search(self, query, k=5):
        return [{"doc": {"id": i}, "skor": 1.0} for i in self._ranked[:k]]


class TestRrf(unittest.TestCase):
    def test_rrf_merges(self):
        docs = [{"id": "a", "text": "antifungal nistatin"}, {"id": "b", "text": "beta blokör"}]
        idx = vector.HybridIndex(docs, use_vector=False)
        idx.vector = _FakeVector(["b", "a"])  # bm25 a'yı öne koyar, vektör b'yi
        hits = idx.search("antifungal", k=2)
        ids = [h["doc"]["id"] for h in hits]
        self.assertEqual(set(ids), {"a", "b"})

    def test_vector_inactive_flag(self):
        idx = vector.HybridIndex([{"id": "a", "text": "x"}], use_vector=False)
        self.assertFalse(idx.vector_active)


if __name__ == "__main__":
    unittest.main()
