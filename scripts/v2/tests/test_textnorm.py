import unittest

from v2.core import textnorm as tn


class TestMojibake(unittest.TestCase):
    def test_looks_mojibake(self):
        self.assertTrue(tn.looks_mojibake("bulgularÄ±ndan"))
        self.assertFalse(tn.looks_mojibake("bulgularından"))

    def test_fix_mojibake_latin1(self):
        self.assertEqual(tn.fix_mojibake("bulgularÄ±ndan"), "bulgularından")

    def test_fix_mojibake_cp1252(self):
        self.assertEqual(tn.fix_mojibake("yanlÄ±ÅŸ"), "yanlış")

    def test_fix_mojibake_noop_on_clean(self):
        self.assertEqual(tn.fix_mojibake("Kardiyoloji", ), "Kardiyoloji")


class TestClean(unittest.TestCase):
    def test_ligature(self):
        self.assertEqual(tn.clean_text("\ufb01nal"), "final")

    def test_strip_control_and_zero_width(self):
        self.assertEqual(tn.clean_text("a\u200bb\x07c"), "abc")

    def test_normalize_ws(self):
        self.assertEqual(tn.normalize_ws("a   b\t c"), "a b c")

    def test_multiple_newlines(self):
        self.assertEqual(tn.normalize_ws("a\n\n\n\nb"), "a\n\nb")


class TestHyphenBreak(unittest.TestCase):
    def test_join(self):
        self.assertEqual(tn.fix_hyphen_breaks("Send-\nromu"), "Sendromu")

    def test_not_join_real_hyphen(self):
        self.assertEqual(tn.fix_hyphen_breaks("e-posta"), "e-posta")


class TestRepairOcr(unittest.TestCase):
    def test_zero_between_letters(self):
        self.assertEqual(tn.repair_ocr("k0ntr0l"), "kontrol")

    def test_aggressive_one(self):
        self.assertEqual(tn.repair_ocr("k1r1k", aggressive=True), "klrlk")

    def test_non_aggressive_leaves_one(self):
        self.assertEqual(tn.repair_ocr("k1r1k"), "k1r1k")

    def test_bang_end_to_i(self):
        self.assertEqual(tn.repair_ocr("Hangis!"), "Hangisi")

    def test_real_exclamation_kept(self):
        self.assertEqual(tn.repair_ocr("Dikkat!"), "Dikkat!")


class TestFold(unittest.TestCase):
    def test_fold_tr(self):
        self.assertEqual(tn.fold_tr("ÇĞİÖŞÜ"), "cgiosu")

    def test_case(self):
        self.assertEqual(tn.fold_tr("İSTANBUL"), "istanbul")


class TestBrokenTurkish(unittest.TestCase):
    def test_replacement_char(self):
        self.assertTrue(tn.has_broken_turkish("bozuk \ufffd metin"))

    def test_mojibake(self):
        self.assertTrue(tn.has_broken_turkish("bulgularÄ±ndan"))


if __name__ == "__main__":
    unittest.main()
