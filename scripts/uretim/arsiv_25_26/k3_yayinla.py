#!/usr/bin/env python3
"""2025-2026 Kurul 3 arşiv dersi yayını — ses + PDF metin takibi + terim/kısaltma + çıkmış chip + .medspak.

Öğren destesi ve canlı çizim ÜRETİLMEZ (kullanıcı kararı 2026-11-17). 2026-2027 veritabanına dokunmaz; her şey
meds_database_25_26/ ve meds/data/arsiv_25_26/ altına yazılır. Kapılar gevşetilmez: 0 HATA olmadan ses/paket çıkmaz.

  k3_yayinla.py <key> [--ses-zorla] [--kapi]      # --kapi: yalnız metin kapıları (ses üretmeden)
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

MEDS = _kok.MEDS
ROOT = MEDS.parent
DB = ROOT / "meds_database_25_26"
ARSIV_DATA = MEDS / "data" / "arsiv_25_26"
SA_KOK = ARSIV_DATA / "sesli_anlatim"
sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "arsiv_25_26"))
sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "ders_isci"))
sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts" / "hat" / "paket"))
sys.path.insert(0, str(MEDS / "scripts" / "altyapi" / "agents"))

import arsiv_yayinla as A  # noqa: E402  (cumle/kelime zamanı, pdf işareti, çıkmış konum, günlük)


# ── kapılar ──────────────────────────────────────────────────────────────────────────────────────
def kapsam(taslak: Path, v2: dict) -> list[str]:
    """Kullanıcı kapısı: her içerik sayfası anlatılır; görselli sayfada görsel ayrıca anlatılır (slayt.sekil)."""
    from pdf_isaret import Pdf
    baglam = json.loads((taslak / "baglam.json").read_text(encoding="utf-8"))
    pdf = Pdf(ROOT / baglam["pdf_yolu"])
    n = len(pdf.doc)
    cum = [c for b in v2["bolumler"] for p in b["paragraflar"] for c in p["cumleler"]]
    anlatilan, sekilli = set(), set()
    for c in cum:
        sl = c.get("slayt") or {}
        if sl.get("sayfa"):
            anlatilan.add(int(sl["sayfa"]))
            if sl.get("sekil"):
                sekilli.add(int(sl["sayfa"]))
        elif not (sl is None):
            pass
    h = []
    varl = {int(x["sayfa"]): x for x in json.loads((taslak / "sayfalar.json").read_text(encoding="utf-8"))} \
        if (taslak / "sayfalar.json").exists() else {}
    for s in range(1, n + 1):
        sy = pdf.sayfa(s)
        if not sy:
            continue
        if s == 1:
            continue          # kapak (başlık/hoca slaytı): anlatılmaz
        yazi = len(sy.kelimeler)
        v = varl.get(s) or {}
        gorsel = (v.get("gorsel_orani") or 0) >= 0.18 or (v.get("cizim") or 0) >= 25 or bool(v.get("tablolar"))
        if s not in anlatilan:
            h.append(f"s.{s}: anlatılmamış (yazı {yazi} kelime{', görsel var' if gorsel else ''})")
        elif gorsel and s not in sekilli:
            h.append(f"s.{s}: görselli sayfa, cümlede slayt.sekil yok (görsel anlatılmamış)")
    return h


def kapilar(taslak: Path, key: str) -> list[str]:
    h: list[str] = []
    import konusma_v2 as KV
    v2_yol = taslak / "konusma_v2.json"
    if not v2_yol.exists():
        return ["konusma_v2.json yok"]
    v2 = json.loads(v2_yol.read_text(encoding="utf-8"))
    h += [f"konusma_v2: {x}" for x in KV.dogrula(v2, KV.kaynak_sayfa(taslak), KV.kaynak_metin(taslak))[:20]]
    if h:
        return h
    md, sayfalar_l = KV.turet(v2)
    (taslak / "konusma_metni.md").write_text(md, encoding="utf-8")
    (taslak / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
    (taslak / "konusma_capalari.json").write_text(json.dumps(KV.capalar(v2), ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "uretim" / "sesli_anlatim" / "metin_denetle.py"), str(taslak / "konusma_metni.md")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        h += [f"metin_denetle: {x}" for x in (r.stdout or r.stderr).strip().splitlines()[:20]]
    h += [f"kapsam: {x}" for x in kapsam(taslak, v2)]
    return h


# ── medspak (destesiz) ──────────────────────────────────────────────────────────────────────────
def medspak(key: str, e: dict, v2: dict, metin: str, isr: dict, kz: dict, varyant: dict, gunluk: dict, pdf: Path) -> Path:
    import medspak_dogrula as MD
    out_dir = DB / "medspak" / "kurul3"
    out_dir.mkdir(parents=True, exist_ok=True)
    yol = out_dir / f"{key}.medspak"
    gecici = out_dir / f"{key}.{os.getpid()}.tmp.medspak"
    gecici.unlink(missing_ok=True)
    db = sqlite3.connect(str(gecici))
    db.executescript("""
      CREATE TABLE meta(anahtar TEXT PRIMARY KEY, deger TEXT);
      CREATE TABLE deste(id TEXT PRIMARY KEY, json TEXT);
      CREATE TABLE cumle(id TEXT PRIMARY KEY, paragraf INT, sira INT, ses TEXT, ekran TEXT, duzey INT, vurgu TEXT,
                         slayt_adim INT, cikmis TEXT, spot TEXT, isaret TEXT);
      CREATE TABLE cizim(cumle_id TEXT, sira INT, json TEXT);
      CREATE TABLE soru(id TEXT PRIMARY KEY, tur TEXT, json TEXT, bagli_cumle TEXT);
      CREATE TABLE ses_parca(varyant TEXT PRIMARY KEY, bicim TEXT, sure_sn REAL, metin_hash TEXT, veri BLOB, zamanlama TEXT, kelime_zaman TEXT);
      CREATE TABLE ek(ad TEXT PRIMARY KEY, tur TEXT, veri BLOB);
      CREATE TABLE gunluk(surum INT PRIMARY KEY, tarih TEXT, neden TEXT, hatali_bilgiler TEXT, degisiklikler TEXT);
    """)
    paragraflar = [p for b in v2.get("bolumler", []) for p in b.get("paragraflar", [])]
    for pi, p in enumerate(paragraflar):
        for ci, c in enumerate(p.get("cumleler", [])):
            i_list = (isr.get("c") or {}).get(str(pi)) or []
            db.execute("INSERT INTO cumle VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                c["id"], pi, ci, c.get("ses"), c.get("ekran"), c.get("duzey"),
                json.dumps(c.get("vurgu") or [], ensure_ascii=False), None,
                json.dumps(c.get("cikmis") or [], ensure_ascii=False), "null",
                json.dumps(i_list[ci] if ci < len(i_list) else None, ensure_ascii=False)))
    deste_id = e["deste_id"]
    deste = {"id": deste_id, "deckId": deste_id, "title": e["baslik"], "committee": "donem3-kurul3",
             "donem": "2025-2026", "arsiv": True, "slides": [],
             "sinama": {"etiket": "2025-2026 Arşiv", "aciklama": "Geçen yıl slaytlarından hazırlanmış arşiv sesli dersidir."}}
    db.execute("INSERT INTO deste VALUES (?,?)", (deste_id, json.dumps(deste, ensure_ascii=False)))
    cumle_by_cikmis = {}
    for p in paragraflar:
        for c in p.get("cumleler", []):
            for q in c.get("cikmis") or []:
                cumle_by_cikmis.setdefault(str(q), c["id"])
    for q, cid in cumle_by_cikmis.items():
        db.execute("INSERT OR IGNORE INTO soru VALUES (?,?,?,?)", (f"cikmis:{q}", "cikmis", json.dumps({"id": q}), cid))
    mp3 = SA_KOK / "ses" / key / f"{varyant['id']}.mp3"
    veri, bicim = mp3.read_bytes(), "mp3"
    opus = mp3.with_suffix(".opus")
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ac", "1", "-c:a", "libopus", "-b:a", "32k",
                        "-vbr", "on", "-application", "voip", str(opus)], capture_output=True, text=True)
    if r.returncode == 0 and opus.exists() and opus.stat().st_size:
        veri, bicim = opus.read_bytes(), "opus"
        opus.unlink(missing_ok=True)
    kz_v = (kz.get("varyantlar") or {}).get(varyant["id"]) or kz
    db.execute("INSERT INTO ses_parca VALUES (?,?,?,?,?,?,?)", (
        varyant["id"], bicim, varyant.get("sureSn"), A.fnv(metin), veri,
        json.dumps(varyant.get("zamanlama")), json.dumps(kz_v)))
    if pdf.exists():
        db.execute("INSERT OR REPLACE INTO ek VALUES (?,?,?)", (e["dosya"], "ders_pdf", pdf.read_bytes()))
    for g in gunluk.get("kayitlar") or []:
        db.execute("INSERT OR REPLACE INTO gunluk VALUES (?,?,?,?,?)", (
            int(g["surum"]), g["tarih"], g["neden"], json.dumps(g.get("hatali_bilgiler") or [], ensure_ascii=False),
            json.dumps(g.get("degisiklikler") or [], ensure_ascii=False)))
    meta = {"surum": 1, "donem": "2025-2026", "arsiv": "1", "ders_id": key, "deste_id": deste_id,
            "kurul": "donem3-kurul3", "baslik": e["baslik"], "metin_hash": A.fnv(metin),
            "isaret_metin_hash": isr.get("metinHash"), "cizim_metin_hash": isr.get("metinHash"),
            "kaynak_sha": hashlib.sha256(json.dumps(v2, sort_keys=True).encode()).hexdigest()[:16],
            "uretildi": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
            "ses_bicim": bicim, "ekler": 1 if pdf.exists() else 0}
    db.executemany("INSERT INTO meta VALUES (?,?)", [(k, v) for k, v in meta.items()])
    db.commit()
    db.close()
    os.replace(gecici, yol)
    hata = MD.denetle(yol)
    if hata:
        raise RuntimeError(f"medspak kapısı: {hata}")
    return yol


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--ses-zorla", action="store_true")
    ap.add_argument("--kapi", action="store_true", help="yalnız metin kapıları")
    a = ap.parse_args()
    key = a.key
    taslak = DB / "taslak" / key
    baglam_yol = taslak / "baglam.json"
    if not baglam_yol.exists():
        print(f"HATA: {baglam_yol} yok (k3_ders.py hazirla)", file=sys.stderr)
        return 2
    baglam = json.loads(baglam_yol.read_text(encoding="utf-8"))
    e = {"deste_id": baglam["deste_id"], "baslik": baglam["konu"], "dosya": baglam["pdf_adi"]}
    pdf = ROOT / baglam["pdf_yolu"]

    print(f"[{key}] 1/5 metin kapıları…")
    h = kapilar(taslak, key)
    if h:
        print(f"[{key}] KAPI HATALARI ({len(h)}):")
        for x in h[:40]:
            print("  -", x)
        return 1
    if a.kapi:
        print(f"[{key}] metin kapıları 0 HATA ✔")
        return 0

    v2 = json.loads((taslak / "konusma_v2.json").read_text(encoding="utf-8"))
    v2["anahtar"], v2["donem"] = key, "2025-2026"
    metin = (taslak / "konusma_metni.md").read_text(encoding="utf-8")
    pars = A.metin_paragraflari(metin)
    capalar = json.loads((taslak / "konusma_capalari.json").read_text(encoding="utf-8"))
    sayfalar_l = json.loads((taslak / "konusma_sayfalari.json").read_text(encoding="utf-8"))

    print(f"[{key}] 2/5 sesli anlatım dosyaları…")
    for alt in ("metin", "v2", "vurgu", "hizalama", "capa", "isaret", "cizim", "cikmis_konum", "cumle_zaman", "kelime_zaman", "ses", "terim", "kisaltma"):
        (SA_KOK / alt).mkdir(parents=True, exist_ok=True)
    (SA_KOK / "metin" / f"{key}.md").write_text(metin, encoding="utf-8")
    (SA_KOK / "v2" / f"{key}.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    import konusma_v2 as KV
    (SA_KOK / "vurgu" / f"{key}.json").write_text(json.dumps(KV.vurgu_turet(v2), ensure_ascii=False), encoding="utf-8")
    hz = {"deckId": e["deste_id"], "donem": "2025-2026",
          "dosyalar": [{"path": baglam["pdf_yolu"], "name": baglam["pdf_adi"], "fileId": baglam.get("file_id"),
                        "pages": int(baglam["sayfa"])}],
          "paragraflar": [{"dosya": 0, "sayfa": int(s), "guven": 1} for s in sayfalar_l],
          "kaynak": "arsiv-25-26-kurul3"}
    (SA_KOK / "hizalama" / f"{key}.json").write_text(json.dumps(hz, ensure_ascii=False, indent=1), encoding="utf-8")
    (SA_KOK / "capa" / f"{key}.json").write_text(json.dumps(
        {"mdSha1": hashlib.sha1(metin.encode("utf-8")).hexdigest(), "p": capalar}, ensure_ascii=False), encoding="utf-8")
    (SA_KOK / "cizim" / f"{key}.json").write_text(json.dumps(
        {"surum": 1, "metinHash": hashlib.sha1("\n".join(p["t"] for p in pars).encode()).hexdigest(), "p": {}}), encoding="utf-8")

    print(f"[{key}] 3/5 EMA GPU ses…")
    kilit = A.gpu_kilit_al()
    try:
        cmd = ["bash", str(MEDS / "scripts" / "uretim" / "patoloji_cozucu" / "cozucu_ses_gpu.sh"),
               str(MEDS / "scripts" / "uretim" / "arsiv_25_26" / "ema_yerel_uret.py"),
               "--key", key, "--metin", str(SA_KOK / "metin" / f"{key}.md"), "--kok", str(SA_KOK)]
        if a.ses_zorla:
            cmd.append("--zorla")
        r = subprocess.run(cmd, cwd=MEDS)
        if r.returncode != 0:
            print(f"HATA: EMA ses (kod {r.returncode})", file=sys.stderr)
            return r.returncode
        kayit = json.loads((SA_KOK / "kayit.json").read_text(encoding="utf-8"))
        varyant = kayit[key][0]
        mp3 = SA_KOK / "ses" / key / f"{varyant['id']}.mp3"

        print(f"[{key}] 4/5 cümle/kelime zamanı…")
        sha = hashlib.sha1("\n".join(p["t"] for p in pars).encode("utf-8")).hexdigest()
        cz = A.cumle_zaman_yerel(key, pars, mp3, varyant["zamanlama"], sha)
        (SA_KOK / "cumle_zaman" / f"{key}.json").write_text(json.dumps(cz, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        kz = A.kelime_zaman_yerel(key, pars, mp3, varyant["zamanlama"], sha)
    finally:
        kilit.close()

    print(f"[{key}] 5/5 PDF işareti, çıkmış, terim…")
    isr = A.pdf_isaret_yerel(key, pars, pdf, hz, capalar, sha, v2)
    ck = A.cikmis_konum_yerel(key, pars, v2, baglam, sha)
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "uretim" / "sesli_anlatim" / "takip_kapisi.py"), key,
                        "--kok", str(SA_KOK)], capture_output=True, text=True, cwd=MEDS)
    print((r.stdout or "").strip()[-1500:])
    if r.returncode != 0:
        print(f"HATA: takip kapısı (T1–T5) — {r.stdout.strip()[-400:]}", file=sys.stderr)
        return 1
    for betik, args in (("terim_sozlugu.py", ["otomatik", key, "--yaz"]),
                        ("kisaltma_sozlugu.py", ["otomatik", key, "--yaz"])):
        rr = subprocess.run([sys.executable, str(MEDS / "scripts" / "uretim" / "sesli_anlatim" / betik)] + args,
                            capture_output=True, text=True, cwd=MEDS)
        print(f"  {betik}: {(rr.stdout or rr.stderr).strip().splitlines()[-1][:160] if (rr.stdout or rr.stderr).strip() else rr.returncode}")

    # ders kaydı (dersler.json) — fcntl kilitli
    ders_kaydi = {"key": key, "donem": "2025-2026", "kurul": 3, "brans": baglam["brans"], "no": int(baglam["brans_no"]),
                  "kurulNo": int(baglam["numara"]), "baslik": baglam["konu"], "hoca": baglam.get("ogretim_uyesi") or "",
                  "sira": int(baglam["numara"]), "desteId": e["deste_id"], "sayfaSayisi": int(baglam["sayfa"])}
    A.json_kilitli_guncelle(SA_KOK / "dersler.json", [], lambda l: sorted(
        [d for d in (l or []) if d.get("key") != key] + [ders_kaydi],
        key=lambda x: (int(x.get("kurul") or 2), int(x.get("sira") or 0))))
    sayfa_haritasi = {"durum": "arsiv", "toplam_sayfa": int(baglam["sayfa"]), "sayfalar": []}
    (taslak / "sayfa_haritasi.json").write_text(json.dumps(sayfa_haritasi, ensure_ascii=False), encoding="utf-8")
    paket_dir = DB / "paketler" / "kurul3"
    paket_dir.mkdir(parents=True, exist_ok=True)
    (paket_dir / f"{key}.json").write_text(json.dumps({
        "ders_id": key, "donem": "2025-2026", "gecen_yil_kaynagi": True, "baslik": baglam["konu"],
        "brans": baglam["brans"], "hoca": baglam.get("ogretim_uyesi") or "", "program": baglam.get("program") or [],
        "pdf": baglam["pdf_yolu"], "sayfa": baglam["sayfa"],
        "ders_notu": "", "ornek_sorular": [], "sozluk": [],
        "medspak": "",
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    cumle_n = sum(len(p.get("cumleler") or []) for b in v2["bolumler"] for p in b.get("paragraflar", []))
    metrik = {"sureDk": round(varyant["sureSn"] / 60, 1), "sayfaSayisi": int(baglam["sayfa"]),
              "bolumSayisi": len(v2["bolumler"]), "paragrafSayisi": len(pars), "cumleSayisi": cumle_n,
              "cikmisEslesme": len(ck.get("q") or [])}
    gunluk = A.gunluk_guncelle(key, baglam["konu"], 3, baglam["brans"],
                              "2025-2026 Kurul 3 arşiv dersi (ses + PDF metin takibi; Öğren destesi ve çizim kullanıcı kararıyla üretilmedi)",
                              ["Öğren destesi, canlı çizim, ara resim ve ara soru üretilmedi — kullanıcı kararı 2026-11-17."],
                              [f"{baglam['pdf_adi']} ({baglam['sayfa']} sayfa) kaynağından {len(pars)} paragraf / {cumle_n} cümlelik sesli anlatım.",
                               "EMA Lightning GPU sesi, cümle/kelime zamanlaması, PDF işareti (takip kapısı T1–T5 0 HATA), terim/kısaltma, çıkmış chip ve .medspak üretildi."],
                              metrik)
    pak = medspak(key, e, v2, metin, isr, kz, varyant, gunluk, pdf)
    p = paket_dir / f"{key}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["medspak"] = str(pak.relative_to(ROOT))
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{key}] TAMAM ✔ {metrik['sureDk']} dk · {cumle_n} cümle · medspak {pak.stat().st_size // 1048576} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
