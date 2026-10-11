"""Ders işçisi iç API'si (yalnız compose iç ağı; dışarıya port açılmaz). Site (meds-app) /api/admin/ders-isci/* altında
yönetici yetkisiyle buraya vekil olur.

  GET  /saglik                         → {"ok": true}
  GET  /taslaklar                      → [{is_id, durum, ozet, ders_id, deste_id, mod, uyari, program, sayilar, karar, zaman}]
  GET  /taslak/<is_id>                 → {baglam özeti, rapor (md), denetim, karar}
  GET  /taslak/<is_id>/dosya/<ad>      → çıktı dosyası (deck.json, ornek_sorular.json, sozluk.json, hastaliklar.json,
                                          bilgi_havuzu.jsonl, cikmis_baglantilari.json, ders_notu.md, ders_paketi.json)
  POST /taslak/<is_id>/karar           ← {"karar": "onayla"|"reddet"|"duzelt", "not": "...", "kim": "..."}
  GET  /checklist                      → checklist.json (2026-27 durum raporu verisi)
  GET  /kuyruk                         → kuyruk.json özeti
Kararlar taslak/<is_id>/karar.json'a yazılır; birleştirme (yayın) ayrı adımdır.
"""
from __future__ import annotations

import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ayarlar import KUYRUK, STATE, TASLAK, log, oku, yaz

DOSYALAR = {"deck.json", "ornek_sorular.json", "sozluk.json", "hastaliklar.json", "bilgi_havuzu.jsonl",
            "cikmis_baglantilari.json", "ders_notu.md", "ders_paketi.json", "rapor.md", "denetim.json"}
GECERLI_ID = re.compile(r"^[0-9]{8}-[0-9a-f]{10}(?:-\d+)?$")


def taslak_ozeti(d) -> dict:
    b = oku(d / "baglam.json", {})
    du = oku(d / "durum.json", {})
    den = oku(d / "denetim.json", {})
    return {"is_id": d.name, "durum": du.get("durum") or "isleniyor", "ozet": du.get("ozet", ""),
            "ders_id": b.get("ders_id"), "deste_id": b.get("deste_id"), "mod": b.get("mod"), "uyari": b.get("uyari", ""),
            "pdf": b.get("pdf_adi"), "program": {k: (b.get("program") or {}).get(k) for k in
                                                  ("kurul", "ders", "konu", "ogretim_uyesi", "tarih", "guven", "skor")},
            "sayilar": den.get("sayilar", {}), "denetim_hata": den.get("hata"), "referans": len(den.get("referansla_tamamlanan", [])),
            "karar": oku(d / "karar.json", None), "zaman": du.get("zaman")}


class H(BaseHTTPRequestHandler):
    # HTTP/1.1 kalıcı bağlantı: varsayılan HTTP/1.0 her yanıttan sonra soketi kapatır; Node (undici) soketi havuzda canlı
    # sanıp yeniden kullanmaya çalışınca istek zaman aşımına kadar asılı kalıyordu (bekleme sonrası ilk istek 10–27 sn).
    protocol_version = "HTTP/1.1"
    timeout = 60  # boşta kalan bağlantıyı tutan iş parçacığı sonsuza dek beklemesin

    def log_message(self, *a):
        pass

    def _json(self, code: int, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _metin(self, code: int, txt: str, tur: str):
        b = txt.encode()
        self.send_response(code)
        self.send_header("Content-Type", f"{tur}; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _taslak(self, is_id: str):
        if not GECERLI_ID.match(is_id or ""):
            return None
        d = TASLAK / is_id
        return d if d.is_dir() else None

    def do_GET(self):  # noqa: N802
        yol = self.path.split("?")[0].rstrip("/")
        if yol == "/saglik":
            return self._json(200, {"ok": True})
        if yol == "/taslaklar":
            liste = [taslak_ozeti(d) for d in TASLAK.iterdir() if d.is_dir() and (d / "baglam.json").exists()]
            return self._json(200, sorted(liste, key=lambda x: x.get("zaman") or 0, reverse=True))
        if yol == "/checklist":
            return self._json(200, oku(STATE / "checklist.json", {}))
        if yol == "/kuyruk":
            return self._json(200, [{k: j.get(k) for k in ("is_id", "yol", "durum", "eklendi", "deneme", "son_mesaj")}
                                    | {"konular": [k.get("konu") for k in j.get("konular") or []]} for j in oku(KUYRUK, [])])
        m = re.match(r"^/taslak/([^/]+)(?:/dosya/([^/]+))?$", yol)
        if m:
            d = self._taslak(m.group(1))
            if not d:
                return self._json(404, {"hata": "taslak yok"})
            if m.group(2):
                ad = m.group(2)
                if ad not in DOSYALAR or not (d / ad).exists():
                    return self._json(404, {"hata": "dosya yok"})
                txt = (d / ad).read_text(encoding="utf-8")
                return self._metin(200, txt, "application/json" if ad.endswith(".json") else "text/plain")
            o = taslak_ozeti(d)
            o["rapor"] = (d / "rapor.md").read_text(encoding="utf-8") if (d / "rapor.md").exists() else ""
            o["denetim"] = oku(d / "denetim.json", {})
            o["dosyalar"] = sorted(x.name for x in d.iterdir() if x.name in DOSYALAR)
            return self._json(200, o)
        return self._json(404, {"hata": "yol yok"})

    def do_POST(self):  # noqa: N802
        m = re.match(r"^/taslak/([^/]+)/karar$", self.path.split("?")[0].rstrip("/"))
        d = self._taslak(m.group(1)) if m else None
        if not d:
            return self._json(404, {"hata": "taslak yok"})
        try:
            body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 20000)) or b"{}")
        except Exception:  # noqa: BLE001
            return self._json(400, {"hata": "geçersiz JSON"})
        karar = body.get("karar")
        if karar not in ("onayla", "reddet", "duzelt"):
            return self._json(400, {"hata": "karar onayla|reddet|duzelt olmalı"})
        if oku(d / "durum.json", {}).get("durum") != "onay_bekliyor":
            return self._json(409, {"hata": "taslak onay beklemiyor"})
        k = {"karar": karar, "not": str(body.get("not") or "")[:4000], "kim": str(body.get("kim") or "")[:200],
             "zaman": time.time()}
        yaz(d / "karar.json", k)
        log(f"karar: {d.name} → {karar}" + (f" ({k['not'][:80]})" if k["not"] else ""))
        return self._json(200, {"ok": True, "karar": k})


def baslat(port: int = 8095):
    srv = ThreadingHTTPServer(("0.0.0.0", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True, name="isci-api").start()
    log(f"iç API dinliyor: :{port}")
    return srv
