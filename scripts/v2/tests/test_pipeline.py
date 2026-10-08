import tempfile
import unittest
from pathlib import Path
from unittest import mock

from v2 import config, pipeline

SAMPLE = """1. Aşağıdakilerden hangisi parenteral uygulama için çok toksik olan antifungaldir?
A) Kaspofungin
B) Ketokonazol
C) Nistatin
D) Vorikonazol
E) Flukonazol
Cevap: C

2. Glukozun hücre içine alınmasını sağlayan taşıyıcı hangisidir?
A) GLUT1
B) GLUT2
C) GLUT4
D) SGLT1
E) SGLT2
Cevap: C
"""


def _write_sample(d: str) -> Path:
    p = Path(d) / "cikmis_sorular.txt"
    p.write_text(SAMPLE, encoding="utf-8")
    return p


class TestPipelineNoPublish(unittest.TestCase):
    def test_parses_without_writing(self):
        with tempfile.TemporaryDirectory() as d:
            p = _write_sample(d)
            s = pipeline.run_ingest(p, publish=False, log=lambda *_: None)
            self.assertEqual(s["belge"], 1)
            self.assertEqual(s["ham_soru"], 2)
            self.assertEqual(s["tekil"], 2)


class TestPipelinePublishIdempotent(unittest.TestCase):
    def test_second_run_no_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            p = _write_sample(d)
            core = Path(d) / "core"
            patch = mock.patch.multiple(
                config,
                CORE_DIR=core, QUESTIONS_DIR=core / "questions", CHUNKS_DIR=core / "chunks",
                SOURCES_DIR=core / "sources", REPORTS_DIR=core / "reports",
                STATE_DIR=core / "_state", KATALOG_PATH=core / "KATALOG.json",
            )
            with patch:
                s1 = pipeline.run_ingest(p, dataset="test", publish=True, log=lambda *_: None)
                self.assertEqual(s1["soru_yayin"]["added"], 2)
                self.assertEqual(s1["soru_yayin"]["invalid"], 0)

                s2 = pipeline.run_ingest(p, dataset="test", publish=True, log=lambda *_: None)
                self.assertEqual(s2["soru_yayin"]["added"], 0)
                self.assertEqual(s2["soru_yayin"]["updated"], 2)
                self.assertEqual(s2["soru_yayin"]["total"], 2)

                qfiles = list((core / "questions").glob("*.jsonl"))
                self.assertEqual(len(qfiles), 1)
                self.assertGreaterEqual(len(list((core / "sources").glob("*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
