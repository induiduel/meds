import unittest

from v2.core import ids


class TestDeterminism(unittest.TestCase):
    def test_question_id_stable(self):
        a = ids.question_id("Antifungal hangisidir?", {"A": "Nistatin", "B": "Ketokonazol"})
        b = ids.question_id("Antifungal hangisidir?", {"A": "Nistatin", "B": "Ketokonazol"})
        self.assertEqual(a, b)
        self.assertEqual(len(a), 12)

    def test_question_id_option_order_independent(self):
        a = ids.question_id("Soru?", {"A": "x", "B": "y"})
        b = ids.question_id("Soru?", {"B": "y", "A": "x"})
        self.assertEqual(a, b)

    def test_question_id_changes_with_content(self):
        a = ids.question_id("Soru bir?", ["x", "y"])
        b = ids.question_id("Soru iki?", ["x", "y"])
        self.assertNotEqual(a, b)

    def test_turkish_case_insensitive(self):
        self.assertEqual(ids.question_id("İLAÇ"), ids.question_id("ilaç"))


class TestIds(unittest.TestCase):
    def test_source_id_format(self):
        sid = ids.source_id("1Ullkdi8IH6RA37H4mAH_z7hcjG2dfpT9")
        self.assertEqual(len(sid), 12)
        int(sid, 16)  # hex olmalı

    def test_source_id_stable(self):
        self.assertEqual(ids.source_id("abc"), ids.source_id("abc"))

    def test_chunk_id_format(self):
        self.assertEqual(ids.chunk_id("00f441c79eb6", 3, 0), "00f441c79eb6:p3:c0")

    def test_content_hash(self):
        self.assertEqual(len(ids.content_hash("bir metin")), 16)
        self.assertEqual(ids.content_hash("Bir  METİN"), ids.content_hash("bir metin"))


if __name__ == "__main__":
    unittest.main()
