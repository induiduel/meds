import tempfile
import unittest
from pathlib import Path

from v2 import config
from v2.core import store


class TestAtomicIO(unittest.TestCase):
    def test_roundtrip_text(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a" / "b.txt"
            store.atomic_write_text(p, "merhaba")
            self.assertEqual(p.read_text(encoding="utf-8"), "merhaba")

    def test_roundtrip_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            store.atomic_write_json(p, {"a": 1, "ü": "ş"})
            self.assertEqual(store.read_json(p), {"a": 1, "ü": "ş"})

    def test_no_leftover_tmp(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.txt"
            store.atomic_write_text(p, "veri")
            leftovers = [f.name for f in Path(d).iterdir() if f.name.startswith(".")]
            self.assertEqual(leftovers, [])


class TestJsonl(unittest.TestCase):
    def test_append_and_read(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.jsonl"
            store.append_jsonl(p, {"i": 1})
            store.append_jsonl(p, {"i": 2})
            self.assertEqual([r["i"] for r in store.read_jsonl(p)], [1, 2])

    def test_write_and_read(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.jsonl"
            store.write_jsonl(p, [{"i": 1}, {"i": 2}])
            self.assertEqual(len(store.read_jsonl(p)), 2)

    def test_guard_blocks_empty_over_nonempty(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.jsonl"
            store.write_jsonl(p, [{"i": 1}])
            with self.assertRaises(store.EmptyOverwriteError):
                store.write_jsonl(p, [])

    def test_guard_allows_when_disabled(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.jsonl"
            store.write_jsonl(p, [{"i": 1}])
            store.write_jsonl(p, [], guard=False)
            self.assertEqual(store.read_jsonl(p), [])

    def test_guard_allows_empty_when_file_absent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "yeni.jsonl"
            store.write_jsonl(p, [])
            self.assertTrue(p.exists())


class TestFileLock(unittest.TestCase):
    def test_acquire_release(self):
        with tempfile.TemporaryDirectory() as d:
            lock = Path(d) / "x.lock"
            with store.FileLock(lock):
                self.assertTrue(lock.exists())
            # ikinci kez alınabilmeli (bırakılmış)
            with store.FileLock(lock):
                pass


class TestState(unittest.TestCase):
    def test_mark_and_persist(self):
        with tempfile.TemporaryDirectory() as d:
            s1 = store.State("test", state_dir=d)
            self.assertFalse(s1.is_done("a"))
            s1.mark_done("a")
            s2 = store.State("test", state_dir=d)
            self.assertTrue(s2.is_done("a"))
            self.assertIn("guncelleme", s2.data)


class TestCoreBoundary(unittest.TestCase):
    def test_under_core_ok(self):
        self.assertTrue(config.is_under_core(config.CORE_DIR / "questions" / "1.jsonl"))

    def test_outside_core_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(PermissionError):
                store.assert_under_core(Path(d) / "kotu.jsonl")

    def test_database_dir_is_outside_core(self):
        self.assertFalse(config.is_under_core(config.DATABASE_DIR))


if __name__ == "__main__":
    unittest.main()
