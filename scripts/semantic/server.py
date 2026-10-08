"""Semantik servis — CPU, ücretsiz, 127.0.0.1:8093. Site `/api/v2/semantic/*` bunu kullanır.

Uçlar:
  GET /health
  GET /classify?q=...     → ders/konu/kazanım + niyet + varlıklar + kanıt
  GET /retrieve?q=...&k=  → en iyi ders notu parçaları (kaynak/sayfa/skor)
Model başlangıçta bir kez yüklenir (ısınma).
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST = os.environ.get("MEDS_SEM_HOST", "127.0.0.1")
PORT = int(os.environ.get("MEDS_SEM_PORT", "8093"))

_ENGINE = None


def engine():
    global _ENGINE
    if _ENGINE is None:
        from . import pipeline

        _ENGINE = pipeline.Engine()
    return _ENGINE


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code: int = 200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        qs = parse_qs(url.query)
        if url.path == "/health":
            return self._json({"ok": True, "servis": "semantic"})
        if url.path == "/classify":
            q = (qs.get("q") or [""])[0]
            if not q.strip():
                return self._json({"error": "q gerekli"}, 400)
            try:
                return self._json(engine().classify(q))
            except Exception as exc:  # noqa: BLE001
                return self._json({"error": str(exc)}, 500)
        if url.path == "/retrieve":
            q = (qs.get("q") or [""])[0]
            k = int((qs.get("k") or ["10"])[0])
            if not q.strip():
                return self._json({"error": "q gerekli"}, 400)
            try:
                hits = engine().retrieve(q, k=k)
                return self._json({"sorgu": q, "sonuc": hits})
            except Exception as exc:  # noqa: BLE001
                return self._json({"error": str(exc)}, 500)
        self._json({"error": "yol yok"}, 404)

    def log_message(self, *args):
        pass


def main() -> int:
    print(f"semantic {HOST}:{PORT}", flush=True)
    try:
        engine().classify("ısınma")  # model/indeks ısınma
        print("semantic: hazır", flush=True)
    except Exception as exc:  # noqa: BLE001
        print(f"semantic ısınma hatası: {exc}", flush=True)
    HTTPServer((HOST, PORT), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
