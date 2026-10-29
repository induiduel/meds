#!/usr/bin/env python3
"""
Vektörleme servisi (meds-embed): yalnız CPU, ücretsiz, yerel. Yerel GPU YASAK (AGENTS.md).
Cihaz: meds-embed (:8091, e5-small) + meds-embed-bge (:8094, bge-m3). Oracle: aynı dosya Dockerfile.embed ile (:8094).

  GET  /       → {"ok", "model", "boyut", "yuklu"}  (modeli yüklemez)
  POST /embed {"texts": [...], "kind": "query"|"passage"|"raw"} → {"vectors": [[...]]}
       query/passage: "query: " / "passage: " öneki eklenir (site araması, rag_vector_build ile aynı);
       raw: metin olduğu gibi (scripts/agents/lib.py::embed — çağıran öneki kendisi ekler).

Yük ayarları (ortam):
  MEDS_EMBED_THREADS   torch iş parçacığı (varsayılan 2)
  MEDS_EMBED_IDLE_SEC  bu kadar saniye istek gelmezse model bellekten bırakılır (0 = hiç; varsayılan 0)
  MEDS_EMBED_CACHE     LRU önbellek kapasitesi (varsayılan 4000 vektör)
"""
from __future__ import annotations

import ctypes
import gc
import json
import os
import threading
import time
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # GPU asla görünmesin
THREADS = int(os.environ.get("MEDS_EMBED_THREADS", "2"))
os.environ.setdefault("OMP_NUM_THREADS", str(THREADS))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

EMBED_MODEL_NAME = os.environ.get("MEDS_EMBED_MODEL", "intfloat/multilingual-e5-small")
IS_BGE = "bge-m3" in EMBED_MODEL_NAME.lower()
DIM = 1024 if IS_BGE else 384
IDLE_SEC = int(os.environ.get("MEDS_EMBED_IDLE_SEC", "0"))
CACHE_MAX = int(os.environ.get("MEDS_EMBED_CACHE", "4000"))
PREFIX = {"query": "query: ", "passage": "passage: ", "raw": ""}

LOCK = threading.Lock()
CACHE: OrderedDict[str, list[float]] = OrderedDict()
_model = None
_last_use = time.monotonic()


def model():
    """Modeli ilk istekte yükler (açılışta RAM/CPU harcamaz)."""
    global _model
    if _model is None:
        import torch
        from sentence_transformers import SentenceTransformer

        torch.set_num_threads(THREADS)
        _model = SentenceTransformer(EMBED_MODEL_NAME, device="cpu")
        _model.max_seq_length = 512 if IS_BGE else 256
    return _model


def idle_reaper():
    global _model
    while True:
        time.sleep(max(30, IDLE_SEC // 4))
        with LOCK:
            if _model is not None and time.monotonic() - _last_use > IDLE_SEC:
                _model = None
                gc.collect()
                # Serbest kalan torch belleğini işletim sistemine geri ver: yoksa model bırakılsa da ~1–2 GB süreçte
                # kalıp takasa iniyordu (meds-embed-bge 1,3 GB, meds-embed 0,8 GB takas).
                try:
                    ctypes.CDLL("libc.so.6").malloc_trim(0)
                except Exception:  # noqa: BLE001
                    pass


def cache_put(k: str, v: list[float]):
    CACHE[k] = v
    CACHE.move_to_end(k)
    while len(CACHE) > CACHE_MAX:
        CACHE.popitem(last=False)


class H(BaseHTTPRequestHandler):
    # HTTP/1.1 kalıcı bağlantı: varsayılan HTTP/1.0 her yanıttan sonra soketi kapatır; Node (undici) soketi havuzda canlı
    # sanıp yeniden kullanmaya çalışınca istek zaman aşımına kadar asılı kalıyordu (bekleme sonrası ilk istek 10–27 sn).
    protocol_version = "HTTP/1.1"
    timeout = 60  # boşta kalan bağlantıyı tutan iş parçacığı sonsuza dek beklemesin

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
        self._send(200, {"ok": True, "model": EMBED_MODEL_NAME, "boyut": DIM, "yuklu": _model is not None})

    def do_POST(self):
        global _last_use
        if self.path != "/embed":
            return self._send(404, {"error": "yok"})
        try:
            body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 400_000)) or b"{}")
            texts = [str(t)[:2000] for t in (body.get("texts") or [])][:64]
            prefix = PREFIX.get(body.get("kind") or "query", "query: ")
            out: list = [None] * len(texts)
            todo = []
            with LOCK:
                for i, t in enumerate(texts):
                    hit = CACHE.get(prefix + t)
                    if hit is not None:
                        CACHE.move_to_end(prefix + t)
                        out[i] = hit
                    else:
                        todo.append(i)
                if todo:
                    v = model().encode([prefix + texts[i] for i in todo], normalize_embeddings=True,
                                       show_progress_bar=False, batch_size=16)
                    for j, i in enumerate(todo):
                        out[i] = [round(float(x), 6) for x in v[j]]
                        cache_put(prefix + texts[i], out[i])
                _last_use = time.monotonic()
            self._send(200, {"vectors": out})
        except Exception as e:  # noqa: BLE001
            self._send(500, {"error": str(e)})


if __name__ == "__main__":
    if IDLE_SEC > 0:
        threading.Thread(target=idle_reaper, daemon=True).start()
    if os.environ.get("MEDS_EMBED_PRELOAD") == "1":
        model()
    host = os.environ.get("MEDS_EMBED_HOST", "127.0.0.1")
    ThreadingHTTPServer((host, int(os.environ.get("MEDS_EMBED_PORT", "8091"))), H).serve_forever()
