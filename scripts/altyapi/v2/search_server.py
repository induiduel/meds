"""v2 anlamsal arama servisi — CPU e5, 127.0.0.1:8092 (GPU YOK).

Site `/api/v2/search` bu servisi kullanır; model bir kez yüklenip bellekte tutulur. Servis kapalıysa
server BM25-lite'a düşer. Uçlar: `GET /health`, `GET /search?q=...&k=8`.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .core import cluster, embed

HOST = os.environ.get("MEDS_V2SEARCH_HOST", "127.0.0.1")
PORT = int(os.environ.get("MEDS_V2SEARCH_PORT", "8092"))


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
        if url.path == "/health":
            return self._json({"ok": True, "servis": "v2search", "vektor": embed.manifest().get("sayi", 0)})
        if url.path != "/search":
            return self._json({"error": "yol yok"}, 404)
        qs = parse_qs(url.query)
        q = (qs.get("q") or [""])[0]
        k = int((qs.get("k") or ["8"])[0])
        try:
            hits = embed.search(q, k=k) if q.strip() else []
            self._json({"sorgu": q, "sonuc": hits})
        except Exception as exc:  # noqa: BLE001
            self._json({"error": str(exc)}, 500)

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != "/merge":
            return self._json({"error": "yol yok"}, 404)
        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except Exception:  # noqa: BLE001
            payload = {}
        parcalar = [p for p in (payload.get("parcalar") or []) if isinstance(p, dict)]
        esik = float(payload.get("esik") or 0.55)
        try:
            res = cluster.cluster_and_merge(parcalar, threshold=esik)
            self._json({"giren": len(parcalar), "grup": len(res.groups), "birlesik": res.merged})
        except Exception as exc:  # noqa: BLE001
            self._json({"error": str(exc)}, 500)

    def log_message(self, *args):  # sessiz
        pass


def main() -> int:
    print(f"v2search {HOST}:{PORT} — vektör: {embed.manifest().get('sayi', 0)}", flush=True)
    try:
        embed.search("ısınma", k=1)  # model + vektörleri başlangıçta yükle (ilk istek hızlı olsun)
        print("v2search: model yüklendi (ısındı)", flush=True)
    except Exception as exc:  # noqa: BLE001
        print(f"v2search: ısınma hatası: {exc}", flush=True)
    HTTPServer((HOST, PORT), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
