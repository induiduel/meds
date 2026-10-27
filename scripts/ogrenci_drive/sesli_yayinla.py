#!/usr/bin/env python3
"""Elle üretilen Kurul 2+ sesli dersi canlıya ekler/günceller (KURUL2_DERS_STANDARDI §2 aşama 8; LLM yok).

Girdi: konusma_v2 çalışma klasörü (konusma_v2.json + --turet çıktıları konusma_metni.md, konusma_sayfalari.json,
konusma_capalari.json). Yapılanlar (yayinla._canli_ders_ekle ile aynı sözleşme):
  1. v2 → data/sesli_anlatim/v2/<key>.json (anahtar) + vurgu/<key>.json (konusma_v2.vurgu_turet) — yerel + Oracle
  2. POST /api/sesli-anlatim/ders-ekle (metin, sayfalar, capalar, deckId, dosya) → metin değiştiyse EMA işi kuyruğa
Kullanım:
  python3 scripts/ogrenci_drive/sesli_yayinla.py --key <key> --no N --baslik "…" --v2 <klasör> --deck <deckId> \\
      --pdf-yol "Kurul 2/…/x.pdf" --pdf-ad "x.pdf" --sayfa 62 --file-id <drive id> [--api http://127.0.0.1:3310]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
import konusma_v2 as KV  # noqa: E402

ORACLE = "medsor-oracle"
ORACLE_KOK = "/home/ubuntu/medsor/meds/data/sesli_anlatim"


def gizli() -> str:
    for s in (MEDS / ".env").read_text(encoding="utf-8").splitlines():
        if s.startswith("MEDS_PANEL_SECRET="):
            return s.split("=", 1)[1].strip()
    raise SystemExit("MEDS_PANEL_SECRET yok")


def main() -> int:
    ap = argparse.ArgumentParser()
    for a in ("key", "no", "baslik", "v2", "deck", "pdf-yol", "pdf-ad", "sayfa", "file-id"):
        ap.add_argument(f"--{a}", required=True)
    ap.add_argument("--api", default="http://127.0.0.1:3310")
    a = ap.parse_args()
    V, k = Path(a.v2), a.key
    v2 = json.loads((V / "konusma_v2.json").read_text(encoding="utf-8"))
    v2["anahtar"] = k
    yerel = MEDS / "data" / "sesli_anlatim"
    for alt, veri in (("v2", v2), ("vurgu", KV.vurgu_turet(v2))):
        p = yerel / alt / f"{k}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(veri, ensure_ascii=False, indent=1 if alt == "v2" else None), encoding="utf-8")
        subprocess.run(["scp", "-q", str(p), f"{ORACLE}:/tmp/{alt}_{k}.json"], check=True)
        subprocess.run(["ssh", ORACLE, f"sudo cp /tmp/{alt}_{k}.json {ORACLE_KOK}/{alt}/{k}.json"], check=True)
    metin = (V / "konusma_metni.md").read_text(encoding="utf-8")
    capa = V / "konusma_capalari.json"
    govde = {"key": k, "no": int(a.no), "baslik": a.baslik, "metin": metin,
             "sayfalar": json.loads((V / "konusma_sayfalari.json").read_text(encoding="utf-8")),
             "capalar": json.loads(capa.read_text(encoding="utf-8")) if capa.exists() else None,
             "deckId": a.deck,
             "dosya": {"path": a.pdf_yol, "name": a.pdf_ad, "pages": int(a.sayfa), "fileId": a.file_id}}
    req = urllib.request.Request(f"{a.api}/api/sesli-anlatim/ders-ekle", json.dumps(govde).encode(),
                                 {"Content-Type": "application/json", "x-panel-secret": gizli()})
    with urllib.request.urlopen(req, timeout=60) as r:
        print(r.read().decode())
    (yerel / "metin" / f"{k}.md").write_text(metin, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
