import tempfile
import unittest
from pathlib import Path
from unittest import mock

from v2 import config, pipeline

DOC = "1. Antifungal hangisidir? A) Nistatin B) Ketokonazol C) Vorikonazol D) Flukonazol E) Kaspofungin\nCevap: A\n"


def _patch(core: Path):
    return mock.patch.multiple(
        config,
        CORE_DIR=core, QUESTIONS_DIR=core / "questions", CHUNKS_DIR=core / "chunks",
        SOURCES_DIR=core / "sources", REPORTS_DIR=core / "reports",
        STATE_DIR=core / "_state", KATALOG_PATH=core / "KATALOG.json",
    )


class TestIngestAll(unittest.TestCase):
    def test_batch_and_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "arsiv"
            root.mkdir()
            (root / "a.txt").write_text(DOC, encoding="utf-8")
            (root / "b.txt").write_text(DOC.replace("Antifungal", "Antibiyotik"), encoding="utf-8")
            core = Path(d) / "core"
            with _patch(core):
                c1 = pipeline.run_ingest_all([root], dataset="test", log=lambda *_: None)
                self.assertEqual(c1["dosya"], 2)
                self.assertEqual(c1["islenen"], 2)
                self.assertEqual(c1["atlanan"], 0)

                c2 = pipeline.run_ingest_all([root], dataset="test", log=lambda *_: None)
                self.assertEqual(c2["islenen"], 0)
                self.assertEqual(c2["atlanan"], 2)


if __name__ == "__main__":
    unittest.main()
