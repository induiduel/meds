import unittest

from v2.core import llm


class TestParseJson(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(llm.parse_json('{"a": 1}'), {"a": 1})

    def test_fenced(self):
        self.assertEqual(llm.parse_json('```json\n{"a": 1}\n```'), {"a": 1})

    def test_with_think(self):
        self.assertEqual(llm.parse_json('<think>düşünce</think>{"a": 2}'), {"a": 2})

    def test_embedded(self):
        self.assertEqual(llm.parse_json('işte: {"a": 3} bitti'), {"a": 3})

    def test_invalid(self):
        self.assertIsNone(llm.parse_json("düz metin"))

    def test_strip_think(self):
        self.assertEqual(llm.strip_think("<think>x</think>y"), "y")


class TestChain(unittest.TestCase):
    def test_nonempty(self):
        chain = llm.chain()
        self.assertTrue(chain)
        for spec in chain:
            self.assertIn(":", spec)

    def test_keys_shape(self):
        pool = llm.keys()
        for provider in ("groq", "gemini", "zen", "openrouter"):
            self.assertIn(provider, pool)
            self.assertIsInstance(pool[provider], list)


if __name__ == "__main__":
    unittest.main()
