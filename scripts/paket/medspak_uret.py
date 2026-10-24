#!/usr/bin/env python3
"""Tekil ders paketi `.medspak` (R7, ICERIK_MOTORU_V3.md §6): bir dersin bütün öğrenci içeriği tek SQLite dosyasında —
dışa aktarım ve çevrimdışı taşıma. Doğruluk kaynağı DEĞİLDİR (her yayından sonra betikle yeniden üretilir, elle yazılmaz).

Tablolar
  meta(anahtar, deger)          surum, ders_id, deste_id, kurul, baslik, metin_hash, kaynak_sha, uretildi, ses_bicim
  deste(id, json)               Öğren destesi (interactive_learning_decks.json'daki nesne)
  cumle(id, paragraf, sira, ses, ekran, duzey, vurgu, slayt_adim, cikmis, spot, isaret)   sesli metin v2 + PDF işareti
  cizim(cumle_id, sira, json)   canlı çizim komutları (cizim/<key>.json)
  soru(id, tur, json, bagli_cumle)  örnek sorular (deste) + çıkmış bağları
  ses_parca(varyant, bicim, sure_sn, metin_hash, veri, zamanlama, kelime_zaman)
  ek(ad, tur, veri)             yalnız --ekler (yönetici dışa aktarımı): ham PDF; öğrenci notu ve hoca kaydı öğrenci
                                indirmesine GİRMEZ (§6 gizlilik)
Kullanım: python3 scripts/paket/medspak_uret.py <ders anahtarı> [--ekler] [--cikti DİZİN]
          → meds_export/medspak/<anahtar>.medspak ; ardından medspak_dogrula.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
UZ = "medsor-oracle:/home/ubuntu/medsor/meds"
SURUM = 1


def fnv(s: str) -> str:
    """sesliAnlatim.ts hash(): FNV-1a 32 bit, JavaScript charCodeAt (UTF-16 birimleri) üzerinden."""
    h = 2166136261
    b = s.encode("utf-16-le")
    for i in range(0, len(b), 2):
        h = ((h ^ (b[i] | b[i + 1] << 8)) * 16777619) & 0xFFFFFFFF
    return format(h, "x")


def cek(goreli: str, hedef: Path) -> Path | None:
    hedef.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["rsync", "-az", f"{UZ}/{goreli}", str(hedef)], capture_output=True, text=True)
    return hedef if r.returncode == 0 and hedef.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("--ekler", action="store_true"); ap.add_argument("--cikti")
    a = ap.parse_args()
    key = a.key
    T = Path(tempfile.mkdtemp(prefix="medspak_"))
    S = "data/sesli_anlatim"
    dosya = {ad: cek(f"{S}/{alt}/{key}{uz}", T / alt / f"{key}{uz}") for ad, alt, uz in (
        ("v2", "v2", ".json"), ("metin", "metin", ".md"), ("hizalama", "hizalama", ".json"), ("isaret", "isaret", ".json"),
        ("cizim", "cizim", ".json"), ("kelime", "kelime_zaman", ".json"))}
    kayit = cek(f"{S}/kayit.json", T / "kayit.json")
    if not dosya["v2"] or not dosya["metin"]:
        print(f"{key}: sesli metin v2 / metin yok (Kurul 2+ dersi değil ya da yayımlanmamış)"); return 2
    v2 = json.loads(dosya["v2"].read_text())
    metin = dosya["metin"].read_text(encoding="utf-8")
    hz = json.loads(dosya["hizalama"].read_text()) if dosya["hizalama"] else {}
    deste_id = hz.get("deckId") or f"k2p-{key}"
    desteler = json.loads((MEDS / "src/data/interactive_learning_decks.json").read_text())
    deste = next((d for d in desteler if d.get("id") == deste_id), None)
    isr = json.loads(dosya["isaret"].read_text()) if dosya["isaret"] else {}
    cz = json.loads(dosya["cizim"].read_text()) if dosya["cizim"] else {}
    kz = json.loads(dosya["kelime"].read_text()) if dosya["kelime"] else {}
    varyantlar = (json.loads(kayit.read_text()).get(key) or []) if kayit else []

    out = Path(a.cikti or (MEDS.parent / "meds_export" / "medspak"))
    out.mkdir(parents=True, exist_ok=True)
    yol = out / f"{key}.medspak"
    yol.unlink(missing_ok=True)
    db = sqlite3.connect(yol)
    db.executescript("""
      CREATE TABLE meta(anahtar TEXT PRIMARY KEY, deger TEXT);
      CREATE TABLE deste(id TEXT PRIMARY KEY, json TEXT);
      CREATE TABLE cumle(id TEXT PRIMARY KEY, paragraf INT, sira INT, ses TEXT, ekran TEXT, duzey INT, vurgu TEXT,
                         slayt_adim INT, cikmis TEXT, spot TEXT, isaret TEXT);
      CREATE TABLE cizim(cumle_id TEXT, sira INT, json TEXT);
      CREATE TABLE soru(id TEXT PRIMARY KEY, tur TEXT, json TEXT, bagli_cumle TEXT);
      CREATE TABLE ses_parca(varyant TEXT PRIMARY KEY, bicim TEXT, sure_sn REAL, metin_hash TEXT, veri BLOB, zamanlama TEXT, kelime_zaman TEXT);
      CREATE TABLE ek(ad TEXT PRIMARY KEY, tur TEXT, veri BLOB);
    """)
    paragraflar = [p for b in v2.get("bolumler", []) for p in b.get("paragraflar", [])]
    n_cumle = 0
    import re as _re
    adim_no = lambda a: a if isinstance(a, int) else (int(m.group(1)) if (m := _re.search(r"-s(\d+)$", str(a or ""))) else None)  # noqa: E731
    for pi, p in enumerate(paragraflar):
        for ci, c in enumerate(p.get("cumleler", [])):
            i = (isr.get("c") or {}).get(str(pi)) or []
            db.execute("INSERT INTO cumle VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                c["id"], pi, ci, c.get("ses"), c.get("ekran"), c.get("duzey"), json.dumps(c.get("vurgu") or [], ensure_ascii=False),
                adim_no(c.get("slayt_adim")), json.dumps(c.get("cikmis") or [], ensure_ascii=False), json.dumps(c.get("spot"), ensure_ascii=False),
                json.dumps(i[ci] if ci < len(i) else None)))
            for si, z in enumerate(((cz.get("p") or {}).get(str(pi)) or {}).get(str(ci)) or []):
                db.execute("INSERT INTO cizim VALUES (?,?,?)", (c["id"], si, json.dumps(z, ensure_ascii=False)))
            n_cumle += 1
    if deste:
        db.execute("INSERT INTO deste VALUES (?,?)", (deste_id, json.dumps(deste, ensure_ascii=False)))
        for s in deste.get("slides") or []:
            for e in s.get("interactiveElements") or []:
                if e.get("type") == "micro_quiz":
                    db.execute("INSERT OR IGNORE INTO soru VALUES (?,?,?,?)", (f"{deste_id}:{s.get('slideNumber')}:{e.get('id')}", "deste",
                                                                              json.dumps(e, ensure_ascii=False), None))
    cumle_by_cikmis = {}
    for p in paragraflar:
        for c in p.get("cumleler", []):
            for q in c.get("cikmis") or []:
                cumle_by_cikmis.setdefault(str(q), c["id"])
    for q, cid in cumle_by_cikmis.items():
        db.execute("INSERT OR IGNORE INTO soru VALUES (?,?,?,?)", (f"cikmis:{q}", "cikmis", json.dumps({"id": q}), cid))
    mh = fnv(metin)
    for v in varyantlar:
        if v.get("metinHash") != mh:          # eski metnin sesi pakete girmez (ekranda metin, seste başka metin olur)
            continue
        mp3 = cek(f"{S}/ses/{key}/{v['id']}.mp3", T / "ses" / f"{v['id']}.mp3")
        if not mp3:
            continue
        db.execute("INSERT INTO ses_parca VALUES (?,?,?,?,?,?,?)", (v["id"], "mp3", v.get("sureSn"), v.get("metinHash"),
                                                                     mp3.read_bytes(), json.dumps(v.get("zamanlama")),
                                                                     json.dumps(kz.get(v["id"]) if isinstance(kz, dict) and v["id"] in kz else kz)))
    if a.ekler:
        for f in hz.get("dosyalar") or []:
            pdf = MEDS / "data/sesli_anlatim/.pdf_onbellek"
            aday = sorted(pdf.glob(f"{deste_id}_*.pdf"))
            if aday:
                db.execute("INSERT OR IGNORE INTO ek VALUES (?,?,?)", (f.get("name") or aday[-1].name, "pdf", aday[-1].read_bytes()))
    meta = {"surum": SURUM, "ders_id": key, "deste_id": deste_id, "kurul": (deste or {}).get("committee") or "",
            "baslik": v2.get("baslik") or (deste or {}).get("title") or key,
            "metin_hash": mh, "isaret_metin_hash": isr.get("metinHash"),
            "cizim_metin_hash": cz.get("metinHash"), "kaynak_sha": hashlib.sha256(json.dumps(v2, sort_keys=True).encode()).hexdigest()[:16],
            "uretildi": dt.datetime.now().isoformat(timespec="seconds"), "ses_bicim": "mp3", "ekler": int(a.ekler)}
    db.executemany("INSERT INTO meta VALUES (?,?)", [(k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v) for k, v in meta.items()])
    db.commit()
    say = {t: db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("cumle", "cizim", "soru", "ses_parca", "ek")}
    db.close()
    print(f"{yol} · {round(yol.stat().st_size / 1048576, 1)} MB · {say} · deste {'var' if deste else 'YOK'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
