#!/usr/bin/env python3
"""2025-2026 arşiv dersi indirme + PDF/PPTX dönüşümü + cikar.py + L0 kroki + çıkmış soru bağlamı hazırlama.

Kullanım:
  /home/indu/medsor/meds/.venv-ocr/bin/python scripts/arsiv_25_26/indir_ve_cikar.py \
      --key y25-k2-01-norolojik-hastaya-yaklasim \
      --kurul 2 \
      --brans "Nöroloji" \
      --no 1 \
      --kurul-no 1 \
      --baslik "Nörolojik Hastaya Yaklaşım" \
      --file-id 1diqvLG4POBEMjKRJvtjhinpgeFV3AK7G \
      [--hoca "Dr. Öğr. Üyesi İrfan Yavaş"] \
      [--kaynak-taslak /home/indu/medsor/meds_temp/gercek_pdf/isci/taslak/20261024-b2a02c0f11]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
DB_25_26 = ROOT / "meds_database_25_26"
ARSIV_DATA = MEDS / "data" / "arsiv_25_26"
DOWNLOADS = ROOT / "meds_downloads" / "_downloads.json"

sys.path.insert(0, str(MEDS / "scripts" / "ders_isci"))
sys.path.insert(0, str(MEDS / "scripts" / "kroki"))
sys.path.insert(0, str(MEDS / "scripts" / "agents"))


def drive_indir(file_id: str, hedef: Path) -> Path:
    hedef.parent.mkdir(parents=True, exist_ok=True)
    if hedef.exists() and hedef.stat().st_size > 1024:
        return hedef
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0&confirm=t"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (medsor-arsiv-25-26)"})
    tmp = hedef.with_suffix(hedef.suffix + ".tmp")
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    if len(data) < 512 or data[:15].lower().startswith(b"<!doctype html"):
        raise RuntimeError(f"Drive indirme başarısız ({file_id}): {len(data)} bayt")
    tmp.write_bytes(data)
    tmp.replace(hedef)
    return hedef


def pptx_to_pdf(pptx: Path, pdf_hedef: Path) -> Path:
    if pdf_hedef.exists() and pdf_hedef.stat().st_size > 1024:
        return pdf_hedef
    pdf_hedef.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(pdf_hedef.parent), str(pptx)],
        capture_output=True, text=True, timeout=300
    )
    uretilen = pdf_hedef.parent / (pptx.stem + ".pdf")
    if r.returncode != 0 or not uretilen.exists():
        raise RuntimeError(f"PPTX → PDF dönüşümü başarısız: {r.stderr}")
    if uretilen != pdf_hedef:
        uretilen.replace(pdf_hedef)
    return pdf_hedef


def cikmis_esle(kurul: int, baslik: str, kaynak_md: str, limit: int = 35) -> list[dict]:
    pq_file = MEDS / "src" / "data" / "pastQuestions.json"
    if not pq_file.exists():
        return []
    tum = json.loads(pq_file.read_text(encoding="utf-8"))
    cid = f"donem3-kurul{kurul}"
    havuz = [q for q in tum if q.get("committeeId") == cid and not q.get("hidden") and not q.get("iptal")]
    if not havuz:
        return []
    try:
        from lib import embed, fold
        q_texts = []
        for q in havuz:
            r = q.get("reconstruction") or {}
            stem = r.get("stem") or q.get("stem") or ""
            ops = r.get("options") or q.get("options") or []
            ans = q.get("correctAnswer")
            ans_txt = next((o.get("text", "") for o in ops if isinstance(o, dict) and o.get("key") == ans), "")
            topic = q.get("topic") or ""
            q_texts.append(f"{topic} {stem} {ans_txt}".strip())
        # Sayfa bazlı parçalara böl
        parcalar = [p.strip()[:800] for p in re.split(r"^##\s+Sayfa\s+\d+", kaynak_md, flags=re.M) if p.strip()]
        if not parcalar:
            parcalar = [baslik]
        qv = embed(q_texts)
        pv = embed([f"{baslik}: {p}" for p in parcalar[:60]])
        sim = (qv @ pv.T).max(axis=1)
        secilen = sorted(range(len(havuz)), key=lambda i: float(sim[i]), reverse=True)[:limit]
        out = []
        for i in secilen:
            skor = float(sim[i])
            if skor < 0.48:
                continue
            q = havuz[i]
            r = q.get("reconstruction") or {}
            ops = r.get("options") or q.get("options") or []
            out.append({
                "id": q["id"],
                "yil": q.get("examYear"),
                "konu": q.get("topic"),
                "soru": r.get("stem") or q.get("stem"),
                "secenekler": {o.get("key"): o.get("text") for o in ops if isinstance(o, dict)},
                "cevap": q.get("correctAnswer"),
                "skor": round(skor, 3),
            })
        return out
    except Exception as e:
        print(f"Uyarı: embed ile çıkmış eşleme yapılamadı ({e}), kelime eşleşmesine düşülüyor", file=sys.stderr)
        return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="Ör. y25-k2-01-norolojik-hastaya-yaklasim")
    ap.add_argument("--kurul", type=int, required=True)
    ap.add_argument("--brans", required=True)
    ap.add_argument("--no", type=int, required=True, help="Branş içi numara")
    ap.add_argument("--kurul-no", type=int, required=True, help="Kurul içi sıra numarası")
    ap.add_argument("--baslik", required=True)
    ap.add_argument("--file-id", required=True)
    ap.add_argument("--hoca", default="")
    ap.add_argument("--kaynak-taslak", default="", help="Varsa mevcut taslaktan kopyala")
    a = ap.parse_args()

    dl = json.loads(DOWNLOADS.read_text(encoding="utf-8")) if DOWNLOADS.exists() else {}
    bilgi = dl.get(a.file_id) or {}
    orijinal_ad = Path(bilgi.get("path") or f"{a.key}.pdf").name
    uzanti = Path(orijinal_ad).suffix.lower() or ".pdf"

    pdf_dir = DB_25_26 / "pdf" / f"kurul{a.kurul}"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_yol = pdf_dir / f"{a.key}.pdf"

    if not pdf_yol.exists() or pdf_yol.stat().st_size < 1024:
        if uzanti in (".pptx", ".ppt"):
            ham = pdf_dir / f"{a.key}{uzanti}"
            print(f"[{a.key}] Drive'dan PPTX indiriliyor ({a.file_id})...")
            drive_indir(a.file_id, ham)
            print(f"[{a.key}] PPTX → PDF dönüştürülüyor...")
            pptx_to_pdf(ham, pdf_yol)
        else:
            print(f"[{a.key}] Drive'dan PDF indiriliyor ({a.file_id})...")
            drive_indir(a.file_id, pdf_yol)

    taslak = DB_25_26 / "taslak" / a.key
    taslak.mkdir(parents=True, exist_ok=True)

    if a.kaynak_taslak and Path(a.kaynak_taslak).is_dir():
        src = Path(a.kaynak_taslak)
        for item in src.iterdir():
            if item.name.startswith("oturum"):
                continue
            dst = taslak / item.name
            if item.is_dir():
                if not dst.exists():
                    shutil.copytree(item, dst)
            else:
                shutil.copy2(item, dst)

    # cikar.py ile kaynak.md, sayfalar.json, sayfa_goruntu/
    if not (taslak / "kaynak.md").exists() or not (taslak / "sayfalar.json").exists():
        print(f"[{a.key}] cikar.py çalıştırılıyor...")
        import cikar
        metin, bilgi_m = cikar.pdf_metni(pdf_yol)
        (taslak / "kaynak.md").write_text(metin, encoding="utf-8")
        bilgi_v = cikar.sayfa_varliklari(pdf_yol, taslak)
        ozet = {**bilgi_m, **bilgi_v}
        (taslak / "kaynak_bilgi.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        ozet = json.loads((taslak / "kaynak_bilgi.json").read_text(encoding="utf-8")) if (taslak / "kaynak_bilgi.json").exists() else {}

    sayfa_sayisi = int(ozet.get("sayfa") or len(json.loads((taslak / "sayfalar.json").read_text(encoding="utf-8"))))

    # L0 kroki üret (meds_database_v2 kirletilmeden MEDS_DB2_DIR=DB_25_26 ile)
    depo_ders = DB_25_26 / "ders_bilgi" / a.key
    depo_ders.mkdir(parents=True, exist_ok=True)
    manifest_obj = {
        "ders_id": a.key,
        "donem": "2025-2026",
        "kurul": a.kurul,
        "brans": a.brans,
        "baslik": a.baslik,
        "pdf": pdf_yol.name,
        "pdf_yolu": str(pdf_yol),
        "yollar": {"kaynak_md": str(taslak / "kaynak.md")},
    }
    (depo_ders / "manifest.json").write_text(json.dumps(manifest_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    l0_dir = depo_ders / "l0"
    if not (l0_dir / "sayfalar.json").exists():
        print(f"[{a.key}] L0 kroki çıkarılıyor...")
        env_l0 = dict(os.environ)
        env_l0["MEDS_DB2_DIR"] = str(DB_25_26)
        subprocess.run(
            [sys.executable, str(MEDS / "scripts" / "kroki" / "l0.py"), "--ders", a.key, "--pdf", str(pdf_yol), "--cikis", str(l0_dir)],
            env=env_l0,
            check=False
        )

    kaynak_md = (taslak / "kaynak.md").read_text(encoding="utf-8")
    aday_cikmis = cikmis_esle(a.kurul, a.baslik, kaynak_md)
    deste_id = f"k{a.kurul}p-{a.key}"

    baglam = {
        "is_id": a.key,
        "donem": "2025-2026",
        "arsiv": True,
        "kurul": a.kurul,
        "committeeId": f"donem3-kurul{a.kurul}",
        "numara": a.kurul_no,
        "brans_no": a.no,
        "ders_id": a.key,
        "deste_id": deste_id,
        "brans": a.brans,
        "konu": a.baslik,
        "ogretim_uyesi": a.hoca,
        "pdf_yolu": str(pdf_yol.relative_to(ROOT)),
        "pdf_adi": orijinal_ad if orijinal_ad.lower().endswith(".pdf") else (Path(orijinal_ad).stem + ".pdf"),
        "file_id": a.file_id,
        "sayfa": sayfa_sayisi,
        "sha256": hashlib.sha256(pdf_yol.read_bytes()).hexdigest(),
        "aday_cikmislar": aday_cikmis,
    }
    (taslak / "baglam.json").write_text(json.dumps(baglam, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{a.key}] Hazır: {sayfa_sayisi} sayfa, {len(aday_cikmis)} aday çıkmış soru → {taslak}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
