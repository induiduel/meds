#!/usr/bin/env python3
"""OpenDesign köprüsü — Claude masaüstü (3P geçit kipi) ve `claude -p` için model adı çevirici.

Sorun: Claude masaüstü/CLI, geçit kipinde model rotası adlarının Anthropic adı olmasını bekler
(`claude-sonnet-5`, `claude-opus-4-8` …). OpenDesign geçidi kendi kimliklerini sunar
(`deepseek-v4.1-flash`, `glm-5.3-flash` …). Bu köprü gelen `model` alanını eşleme tablosuna göre
geçit kimliğine çevirir, isteği geçide iletir ve yanıtı (SSE akışı dahil) olduğu gibi geri akıtır.

Tek kaynak: `meds/scripts/opendesign/rotalar.json` → `~/.claude/opendesign-kopru.json` (`kur.sh` yazar).
Anahtar: `MEDS_OPENDESIGN_KEY` > `~/.claude/settings.json` → env.ANTHROPIC_AUTH_TOKEN.
Kurulum/sağlık: `bash meds/scripts/opendesign/kur.sh` · `python3 …/kopru.py --doctor`

Dinler: 127.0.0.1:<port> (varsayılan 8787). Yalnız stdlib; /usr/bin/python3 ile çalışır.
Bu süreç kendi başına LLM işi başlatmaz: yalnız gelen isteği iletir (AGENTS kural 20).
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

SURUM = "2"
HOME = os.path.expanduser("~")
SETTINGS = os.path.join(HOME, ".claude", "settings.json")
MAPFILE = os.path.join(HOME, ".claude", "opendesign-kopru.json")
YEDEK_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rotalar.json")

# İstemciden geçide taşınmayan başlıklar. accept-encoding da düşer: geçit gzip'leseydi yanıtı
# sıkıştırılmış ama başlıksız akıtırdık (istemci çözemez).
HOP_HEADERS = {
    "host", "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "content-length", "authorization",
    "accept-encoding", "x-api-key",
}
# Geçitten istemciye aynen geçen yanıt başlıkları (yeniden deneme ve kota davranışı bunlara bağlı).
GECEN_BASLIKLAR = {"retry-after", "request-id", "anthropic-ratelimit-requests-limit",
                   "anthropic-ratelimit-requests-remaining", "anthropic-ratelimit-tokens-limit",
                   "anthropic-ratelimit-tokens-remaining", "anthropic-ratelimit-input-tokens-limit",
                   "anthropic-ratelimit-output-tokens-limit", "x-request-id"}


def _oku_yol(yol: str) -> dict:
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def _anahtar(env_settings: dict) -> str:
    return (os.environ.get("MEDS_OPENDESIGN_KEY") or os.environ.get("OPEN_DESIGN_API_KEY")
            or os.environ.get("ANTHROPIC_AUTH_TOKEN") or env_settings.get("ANTHROPIC_AUTH_TOKEN") or "")


def ayar_oku() -> dict:
    """Köprü ayarı: port, upstream, rotalar, takma adlar, anahtar. Eksikse anlaşılır hata."""
    ayar_env: dict = {}
    if os.path.exists(SETTINGS):
        try:
            ayar_env = (_oku_yol(SETTINGS).get("env") or {})
        except (OSError, json.JSONDecodeError) as e:
            raise SystemExit(f"kopru: {SETTINGS} okunamadı: {e}")
    if os.path.exists(MAPFILE):
        cfg = _oku_yol(MAPFILE)
    elif os.path.exists(YEDEK_MAP):
        cfg = _oku_yol(YEDEK_MAP)
        print(f"kopru: uyarı — {MAPFILE} yok, paketle gelen {YEDEK_MAP} kullanılıyor (kur.sh ile kurun)",
              file=sys.stderr)
    else:
        raise SystemExit(f"kopru: eşleme dosyası yok ({MAPFILE}) — `bash meds/scripts/opendesign/kur.sh`")
    # Geçit adresi eşleme dosyasından okunur: settings.json'daki ANTHROPIC_BASE_URL artık köprünün
    # kendisini gösterir, oradan okunursa köprü kendine istek atar (sonsuz döngü).
    base = (cfg.get("upstream") or ayar_env.get("ANTHROPIC_BASE_URL") or "").rstrip("/")
    if not base:
        raise SystemExit("kopru: upstream adresi yok (opendesign-kopru.json → upstream)")
    rotalar = {r["advertised"]: r["upstream"] for r in cfg["routes"] if not r.get("alias")}
    takma = {r["advertised"]: r["upstream"] for r in cfg["routes"] if r.get("alias")}
    return {"port": int(cfg.get("port", 8787)), "base": base, "anahtar": _anahtar(ayar_env),
            "rotalar": rotalar, "takma": takma, "cfg": cfg}


def esle(ad: str, AYAR: dict) -> str | None:
    """İstenen model adı → geçit kimliği. `[1m]` soneki (uzun bağlam) atılır; bilinmeyen ad None."""
    bare = ad.strip()
    if bare.endswith("[1m]"):
        bare = bare[:-4].strip()
    return AYAR["rotalar"].get(bare) or AYAR["takma"].get(bare)


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = f"opendesign-kopru/{SURUM}"
    AYAR: dict = {}

    def log_message(self, fmt, *args):  # journal'a yalnız özet yazılır
        pass

    # ---------- yardımcılar ----------
    def _json(self, code: int, obj: dict) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _upstream_conn(self):
        u = urlparse(self.AYAR["base"])
        if u.scheme == "https":
            return http.client.HTTPSConnection(u.hostname, u.port or 443, timeout=900)
        return http.client.HTTPConnection(u.hostname, u.port or 80, timeout=900)

    def _cevir(self, raw: bytes) -> bytes:
        if not raw:
            return raw
        try:
            govde = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return raw
        if isinstance(govde, dict) and isinstance(govde.get("model"), str):
            istenen = govde["model"]
            hedef = esle(istenen, self.AYAR)
            if hedef:
                govde["model"] = hedef
            else:
                log(f"uyarı: eşlenmemiş model '{istenen}' — olduğu gibi iletiliyor")
            return json.dumps(govde, ensure_ascii=False).encode()
        return raw

    def _forward(self, method: str) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if method in ("POST", "PUT", "PATCH"):
            raw = self._cevir(raw)

        basliklar = {k: v for k, v in self.headers.items() if k.lower() not in HOP_HEADERS}
        basliklar["Authorization"] = "Bearer " + self.AYAR["anahtar"]
        basliklar["Content-Type"] = "application/json"
        if not any(k.lower() == "anthropic-version" for k in basliklar):
            basliklar["anthropic-version"] = "2023-06-01"

        t0 = time.time()
        conn = self._upstream_conn()
        try:
            conn.request(method, self.path, body=raw if method in ("POST", "PUT", "PATCH") else None,
                         headers=basliklar)
            yanit = conn.getresponse()
        except Exception as exc:  # noqa: BLE001
            log(f"hata: geçide ulaşılamadı ({self.AYAR['base']}): {exc}")
            self._json(502, {"type": "error", "error": {"type": "api_error",
                                                        "message": f"kopru: geçide ulaşılamadı: {exc}"}})
            return

        log(f"{method} {self.path} -> {yanit.status} ({time.time() - t0:.1f} sn)")
        self.send_response(yanit.status)
        self.send_header("Content-Type", yanit.getheader("Content-Type", "application/json"))
        for k, v in yanit.getheaders():
            if k.lower() in GECEN_BASLIKLAR:
                self.send_header(k, v)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()

        try:
            while True:
                parca = yanit.read(65536)
                if not parca:
                    break
                self.wfile.write(b"%X\r\n" % len(parca))
                self.wfile.write(parca)
                self.wfile.write(b"\r\n")
                self.wfile.flush()
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass  # istemci akışı bıraktı (Esc) — geçit bağlantısı yine kapanır
        finally:
            conn.close()

    # ---------- uçlar ----------
    def do_GET(self):
        if self.path.rstrip("/") in ("", "/health"):
            self._json(200, {"ok": True, "surum": SURUM, "port": self.AYAR["port"],
                             "upstream": self.AYAR["base"], "rotalar": len(self.AYAR["rotalar"]),
                             "takma": len(self.AYAR["takma"]), "anahtar": bool(self.AYAR["anahtar"])})
            return
        if self.path.startswith("/v1/models"):
            data = [{"id": adv, "object": "model", "type": "model", "display_name": adv,
                     "created_at": "2026-01-01T00:00:00Z", "upstream": up}
                    for adv, up in self.AYAR["rotalar"].items()]
            self._json(200, {"data": data, "has_more": False,
                             "first_id": data[0]["id"] if data else None,
                             "last_id": data[-1]["id"] if data else None})
            return
        self._forward("GET")

    def do_POST(self):
        self._forward("POST")

    def do_DELETE(self):
        self._forward("DELETE")


# ── doktor ────────────────────────────────────────────────────────────────────────────────────────────────────
def doctor() -> int:
    """Kurulumu ve canlılığı denetler: eşleme, anahtar, port, geçit erişimi, depo model adları."""
    from urllib import error as urlerror
    from urllib import request as urlrequest

    sorun: list[str] = []
    try:
        AYAR = ayar_oku()
    except SystemExit as e:
        print(f"HATA {e}")
        return 1

    print(f"eşleme   : {MAPFILE if os.path.exists(MAPFILE) else YEDEK_MAP + ' (yedek)'}")
    print(f"upstream : {AYAR['base']}")
    print(f"port     : {AYAR['port']} · rotalar {len(AYAR['rotalar'])} · takma {len(AYAR['takma'])}")
    print(f"anahtar  : {'…' + AYAR['anahtar'][-4:] if AYAR['anahtar'] else 'YOK'} "
          f"({'ortam' if os.environ.get('MEDS_OPENDESIGN_KEY') else 'settings.json'})")
    if not AYAR["anahtar"]:
        sorun.append("anahtar yok")

    # Depoda geçen adların hepsi eşleniyor mu (eşlenmeyen ad geçide ham gider ve 400 alır)
    for ad in ("claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-4-5-20251001",
               "claude-opus-4-8", "claude-opus-4-7", "claude-opus-5", "claude-sonnet-5", "claude-haiku-5-5"):
        hedef = esle(ad, AYAR)
        print(f"  {ad:32} -> {hedef or 'EŞLENMEMİŞ'}")
        if not hedef:
            sorun.append(f"eşlenmemiş: {ad}")

    # Köprü ayakta mı
    try:
        with urlrequest.urlopen(f"http://127.0.0.1:{AYAR['port']}/health", timeout=3) as r:
            sag = json.loads(r.read() or b"{}")
        print(f"köprü    : ÇALIŞIYOR (sürüm {sag.get('surum')}, {sag.get('rotalar')} rota)")
    except Exception as e:  # noqa: BLE001
        print(f"köprü    : YOK ({type(e).__name__}) — `systemctl --user start opendesign-kopru`")
        sorun.append("köprü çalışmıyor")

    # Geçit erişimi ve model listesi (gerçek ağ denemesi, 20 sn)
    try:
        req = urlrequest.Request(AYAR["base"] + "/v1/models",
                                 headers={"Authorization": "Bearer " + AYAR["anahtar"],
                                          "anthropic-version": "2023-06-01"})
        with urlrequest.urlopen(req, timeout=20) as r:
            ms = [m.get("id") for m in json.loads(r.read()).get("data", [])]
        print(f"geçit    : erişilebilir, {len(ms)} model")
        eksik = sorted({u for u in AYAR["rotalar"].values()} - set(ms))
        if eksik:
            print(f"uyarı    : eşlemede olup geçitte görünmeyen model: {', '.join(eksik)}")
    except urlerror.HTTPError as e:
        print(f"geçit    : HTTP {e.code} — anahtar geçersiz ya da yetki yok")
        sorun.append(f"geçit HTTP {e.code}")
    except Exception as e:  # noqa: BLE001
        print(f"geçit    : erişilemedi ({type(e).__name__}: {str(e)[:120]})")
        sorun.append("geçit erişilemiyor")

    print("SONUÇ    :", "SORUN YOK" if not sorun else "SORUN — " + "; ".join(sorun))
    return 0 if not sorun else 1


def sunucu() -> int:
    AYAR = ayar_oku()
    u = urlparse(AYAR["base"])
    if u.hostname in ("127.0.0.1", "localhost") and (u.port or 0) == AYAR["port"]:
        log("hata: upstream köprünün kendisini gösteriyor — opendesign-kopru.json → 'upstream' alanını düzelt")
        return 1
    if not AYAR["anahtar"]:
        log("uyarı: anahtar yok — gelen istekler 401 alır")
    Handler.AYAR = AYAR
    srv = ThreadingHTTPServer(("127.0.0.1", AYAR["port"]), Handler)
    srv.daemon_threads = True
    log(f"opendesign-kopru v{SURUM} dinliyor: http://127.0.0.1:{AYAR['port']} -> {AYAR['base']} "
        f"({len(AYAR['rotalar'])} rota, {len(AYAR['takma'])} takma ad)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="OpenDesign köprüsü (model adı çevirici)")
    ap.add_argument("--doctor", action="store_true", help="kurulumu ve geçit erişimini denetle")
    ap.add_argument("--surum", action="store_true", help="sürümü yaz")
    a = ap.parse_args(argv)
    if a.surum:
        print(SURUM)
        return 0
    if a.doctor:
        return doctor()
    return sunucu()


if __name__ == "__main__":
    raise SystemExit(main())
