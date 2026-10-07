#!/usr/bin/env python3
"""
Sorgu vektörleme servisi (meds-embed): site aramasında sorguyu e5-small ile vektöre çevirir (CPU, ücretsiz, yerel).
Yalnız 127.0.0.1:8091 dinler. POST /embed {"texts": [...], "kind": "query"|"passage"} → {"vectors": [[...384]]}
Belge vektörleri rag_vector_build.py ile aynı model ve öneklerle üretilir.
"""
from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
from sentence_transformers import SentenceTransformer  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(4)
MODEL = SentenceTransformer("intfloat/multilingual-e5-small", device="cpu")
MODEL.max_seq_length = 256
LOCK = threading.Lock()
CACHE: dict[str, list[float]] = {}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code: int, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        self._send(200, {"ok": True, "model": "multilingual-e5-small", "boyut": 384})

    def do_POST(self):
        if self.path != "/embed":
            return self._send(404, {"error": "yok"})
        try:
            body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 200_000)) or b"{}")
            texts = [str(t)[:2000] for t in (body.get("texts") or [])][:64]
            prefix = "passage: " if body.get("kind") == "passage" else "query: "
            out, todo = [None] * len(texts), []
            for i, t in enumerate(texts):
                k = prefix + t
                if k in CACHE:
                    out[i] = CACHE[k]
                else:
                    todo.append(i)
            if todo:
                with LOCK:
                    v = MODEL.encode([prefix + texts[i] for i in todo], normalize_embeddings=True, show_progress_bar=False)
                for j, i in enumerate(todo):
                    out[i] = [round(float(x), 6) for x in v[j]]
                    if len(CACHE) < 5000:
                        CACHE[prefix + texts[i]] = out[i]
            self._send(200, {"vectors": out})
        except Exception as e:  # noqa: BLE001
            self._send(500, {"error": str(e)})


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(os.environ.get("MEDS_EMBED_PORT", "8091"))), H).serve_forever()
