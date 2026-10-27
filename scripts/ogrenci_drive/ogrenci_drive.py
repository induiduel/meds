#!/usr/bin/env python3
"""Öğrenci Drive klasörü izleme, indirme ve ders eşleştirme aracı.

Kullanıcının paylaştığı öğrenci notları ve ses kayıtları klasörü:
  Drive Kök: https://drive.google.com/drive/folders/17K7doMGg0xupQekTD5_Vz9xMXc5gd7BA
  Klasör ID: 17K7doMGg0xupQekTD5_Vz9xMXc5gd7BA

Klasör Şeması:
  /Kurullar/
    Kurul 2/
      Farmakoloji/
      Nöroloji/
      Tıbbi Patoloji/
    Kurul 3/ ... Kurul 6/
  /Ek notlar/
  /Çıkmış/
  /Yapay Zeka Çıktıları/

Kullanım:
  python3 scripts/ogrenci_drive/ogrenci_drive.py --tara
  python3 scripts/ogrenci_drive/ogrenci_drive.py --liste
  python3 scripts/ogrenci_drive/ogrenci_drive.py --esle [--kurul 2]
  python3 scripts/ogrenci_drive/ogrenci_drive.py --indir --id <drive_file_id> --hedef <hedef_yol>
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

KOK_ID = "17K7doMGg0xupQekTD5_Vz9xMXc5gd7BA"

APP_DIR = Path(__file__).resolve().parents[2]          # meds/
DATA_DIR = APP_DIR / "data"
DOWNLOADS_DIR = APP_DIR.parent / "meds_downloads"
DRIVE_ROOT_DIR = DOWNLOADS_DIR / "drive_root"
ENVANTER_DOSYASI = DATA_DIR / "ogrenci_drive_envanter.json"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

SES_UZANTILARI = {".m4a", ".mp3", ".wav", ".aac", ".ogg", ".opus", ".flac", ".wma"}
NOT_UZANTILARI = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".webp", ".heic", ".txt", ".md", ".pptx", ".ppt"}


def fold(s: str) -> str:
    """Türkçe karakterleri ve boşlukları normalize eder."""
    s = str(s).replace("İ", "i").replace("I", "ı").lower()
    _trans = str.maketrans("çğıöşüâîû", "cgiosuaiu")
    s = s.translate(_trans)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def drive_klasor_listele(folder_id: str) -> list[dict]:
    """Herkese açık Google Drive klasöründeki dosya ve alt klasörleri listeler."""
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "tr-TR,tr;q=0.9"})
    for deneme in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                text = resp.read().decode("utf-8", errors="replace")
            m = re.search(r"window\['_DRIVE_ivd'\]\s*=\s*'([^']+)'", text)
            if not m:
                return []
            raw = m.group(1)
            raw = re.sub(r"\\\\x([0-9a-fA-F]{2})", lambda h: chr(int(h.group(1), 16)), raw)
            raw = re.sub(r"\\x([0-9a-fA-F]{2})", lambda h: chr(int(h.group(1), 16)), raw)
            data = json.loads(raw)

            out = []
            seen = set()

            def _rec(v):
                if not isinstance(v, list):
                    return
                if (
                    len(v) >= 4
                    and isinstance(v[0], str)
                    and len(v[0]) >= 25
                    and isinstance(v[2], str)
                    and isinstance(v[3], str)
                    and v[0] not in seen
                ):
                    seen.add(v[0])
                    out.append({"id": v[0], "name": v[2], "mime": v[3]})
                for sub in v:
                    _rec(sub)

            _rec(data)
            return [o for o in out if o["id"] != folder_id]
        except Exception as e:
            if deneme == 2:
                print(f"[UYARI] Klasör listelenemedi: {folder_id} ({e})", file=sys.stderr)
            time.sleep(1.5 * (deneme + 1))
    return []


def tara_tum_agac(kok_id: str = KOK_ID) -> dict:
    """Tüm öğrenci Drive ağacını özyinelemeli tarar ve yapılandırılmış envanter döner."""
    print(">> Öğrenci Drive ağacı taranıyor...")
    kok_ogeleri = drive_klasor_listele(kok_id)
    envanter = {
        "taranma_zamani": time.strftime("%Y-%m-%d %H:%M:%S"),
        "kok_id": kok_id,
        "kurullar": {},
        "ek_notlar": [],
        "cikmis": [],
        "diger": [],
    }

    for oge in kok_ogeleri:
        ad = oge["name"]
        fid = oge["id"]
        is_folder = "folder" in oge["mime"]

        if is_folder and fold(ad) == "kurullar":
            kurul_klasorleri = drive_klasor_listele(fid)
            for k in kurul_klasorleri:
                k_ad = k["name"]
                k_id = k["id"]
                # Kurul no çıkar: "Kurul 2" -> 2
                km = re.search(r"kurul\s*(\d+)", fold(k_ad))
                kurul_no = int(km.group(1)) if km else k_ad
                envanter["kurullar"][str(kurul_no)] = {"klasor_adi": k_ad, "id": k_id, "branslar": {}}

                brans_klasorleri = drive_klasor_listele(k_id)
                for b in brans_klasorleri:
                    b_ad = b["name"]
                    b_id = b["id"]
                    b_ogeleri = drive_klasor_listele(b_id)
                    dosyalar = []
                    for d in b_ogeleri:
                        d_uz = Path(d["name"]).suffix.lower()
                        # Uzantısız Drive adları (ör. "Nöroloji 1 - …") MIME'den sınıflanır (2026-10-27)
                        mime = d.get("mime") or ""
                        tur = ("ses" if d_uz in SES_UZANTILARI or mime.startswith("audio/") else
                               "not" if d_uz in NOT_UZANTILARI or mime == "application/pdf" else "diger")
                        dosyalar.append({
                            "id": d["id"],
                            "name": d["name"],
                            "mime": d["mime"],
                            "uzanti": d_uz,
                            "tur": tur,
                            "path": f"Kurullar/{k_ad}/{b_ad}/{d['name']}",
                        })
                    envanter["kurullar"][str(kurul_no)]["branslar"][b_ad] = {
                        "id": b_id,
                        "dosyalar": dosyalar,
                    }

        elif is_folder and fold(ad) in ("ek notlar", "eknotlar"):
            ogeler = drive_klasor_listele(fid)
            for d in ogeler:
                envanter["ek_notlar"].append({
                    "id": d["id"],
                    "name": d["name"],
                    "mime": d["mime"],
                    "path": f"Ek notlar/{d['name']}",
                })
        elif is_folder and fold(ad) in ("cikmis", "cikmislar"):
            ogeler = drive_klasor_listele(fid)
            for d in ogeler:
                envanter["cikmis"].append({
                    "id": d["id"],
                    "name": d["name"],
                    "mime": d["mime"],
                    "path": f"Çıkmış/{d['name']}",
                })
        else:
            envanter["diger"].append(oge)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ENVANTER_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(envanter, f, ensure_ascii=False, indent=2)

    toplam_ses = 0
    toplam_not = 0
    for k_val in envanter["kurullar"].values():
        for b_val in k_val.get("branslar", {}).values():
            for d in b_val.get("dosyalar", []):
                if d["tur"] == "ses":
                    toplam_ses += 1
                elif d["tur"] == "not":
                    toplam_not += 1

    print(f"✓ Envanter güncellendi: {ENVANTER_DOSYASI}")
    print(f"  Kurullar: {list(envanter['kurullar'].keys())}")
    print(f"  Toplam ses: {toplam_ses} adet, Toplam not: {toplam_not} adet")
    return envanter


def envanter_yukle() -> dict:
    if ENVANTER_DOSYASI.exists():
        try:
            with open(ENVANTER_DOSYASI, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return tara_tum_agac()


def dosya_indir(drive_id: str, hedef_yol: Path | str, zorla: bool = False) -> bool:
    """Google Drive dosyasını doğrudan belirtilen yerel yola indirir."""
    hedef = Path(hedef_yol)
    if hedef.exists() and not zorla and hedef.stat().st_size > 0:
        return True

    hedef.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://drive.usercontent.google.com/download?id={drive_id}&export=download&authuser=0&confirm=t"
    req = urllib.request.Request(url, headers={"User-Agent": UA})

    try:
        print(f"İndiriliyor: {hedef.name} ({drive_id})...")
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(hedef, "wb") as out:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
        print(f"✓ İndirildi: {hedef} ({hedef.stat().st_size} bayt)")
        return True
    except Exception as e:
        print(f"[HATA] İndirilemedi {drive_id} -> {hedef}: {e}", file=sys.stderr)
        return False


def orjinal_pdf_bul(kurul_no: int | str, konu_veya_ders: str) -> Path | None:
    """Resmi hoca PDF'sini (drive_root veya ders_notlari altında) bulur."""
    kurul_str = f"Kurul {kurul_no}"
    hedef_klasor = DRIVE_ROOT_DIR / kurul_str
    if not hedef_klasor.exists():
        # Alternatif yollar
        for alt in DRIVE_ROOT_DIR.glob(f"*{kurul_no}*"):
            if alt.is_dir():
                hedef_klasor = alt
                break

    if not hedef_klasor.exists():
        return None

    norm_hedef = fold(konu_veya_ders)
    en_iyi_pdf = None
    en_yuksek_skor = 0.0

    for pdf in hedef_klasor.rglob("*.pdf"):
        ad_fold = fold(pdf.stem)
        skor = difflib.SequenceMatcher(None, norm_hedef, ad_fold).ratio()
        # Kelime kesişimi kontrolü
        kelimeler_hedef = set(norm_hedef.split())
        kelimeler_pdf = set(ad_fold.split())
        if kelimeler_hedef and kelimeler_pdf:
            kesisim = len(kelimeler_hedef & kelimeler_pdf) / len(kelimeler_hedef)
            skor = max(skor, kesisim)

        if skor > en_yuksek_skor:
            en_yuksek_skor = skor
            en_iyi_pdf = pdf

    if en_yuksek_skor >= 0.4:
        return en_iyi_pdf
    return None


def materyal_eslestir(kurul_no: int = 2) -> list[dict]:
    """Öğrenci materyalleri (ses/not) ile ders programı ve orijinal PDF'leri eşleştirir."""
    env = envanter_yukle()
    k_data = env.get("kurullar", {}).get(str(kurul_no))
    if not k_data:
        return []

    sonuclar = []
    branslar = k_data.get("branslar", {})

    for b_ad, b_val in branslar.items():
        for d in b_val.get("dosyalar", []):
            dosya_adi = d["name"]
            stem = Path(dosya_adi).stem
            # Temiz konu adı elde et: "Nöro 1 Nörolojik Hastaya Yaklaşım" -> "Nörolojik Hastaya Yaklaşım"
            temiz = re.sub(r"^(nöro|farma|patoloji|pat)\s*\d+[\s_-]*", "", stem, flags=re.IGNORECASE)
            temiz = re.sub(r"^(ders|k\d+[\s_-]*\d+)\s*", "", temiz, flags=re.IGNORECASE).strip()
            if not temiz:
                temiz = stem

            orj_pdf = orjinal_pdf_bul(kurul_no, temiz)

            sonuclar.append({
                "kurul": kurul_no,
                "brans": b_ad,
                "dosya_adi": dosya_adi,
                "dosya_id": d["id"],
                "tur": d["tur"],
                "path": d["path"],
                "arama_konusu": temiz,
                "orijinal_pdf": str(orj_pdf) if orj_pdf else None,
                "orijinal_pdf_adi": orj_pdf.name if orj_pdf else "Bulunamadı (henüz okul drive'ında yok ya da adı farklı)",
            })

    return sonuclar


def main():
    parser = argparse.ArgumentParser(description="Öğrenci Drive İzleme ve Eşleştirme")
    parser.add_argument("--tara", action="store_true", help="Öğrenci Drive klasörünü yeniden tara")
    parser.add_argument("--liste", action="store_true", help="Envanterdeki dosyaları listele")
    parser.add_argument("--esle", action="store_true", help="Materyalleri orijinal PDF'lerle eşleştir")
    parser.add_argument("--kurul", type=int, default=2, help="Kurul numarası (varsayılan: 2)")
    parser.add_argument("--indir", action="store_true", help="Dosya indir")
    parser.add_argument("--id", type=str, help="Drive dosya ID")
    parser.add_argument("--hedef", type=str, help="İndirilecek hedef dosya yolu")
    args = parser.parse_args()

    if args.tara:
        tara_tum_agac()
    elif args.liste:
        env = envanter_yukle()
        print(f"Tarama zamanı: {env.get('taranma_zamani')}")
        for k_no, k_val in env.get("kurullar", {}).items():
            print(f"\n📁 Kurul {k_no}: {k_val['klasor_adi']}")
            for b_ad, b_val in k_val.get("branslar", {}).items():
                print(f"  📂 {b_ad}")
                for d in b_val.get("dosyalar", []):
                    simge = "🎙️" if d["tur"] == "ses" else ("📄" if d["tur"] == "not" else "📎")
                    print(f"    {simge} {d['name']} (ID: {d['id']})")
    elif args.esle:
        eslesmeler = materyal_eslestir(args.kurul)
        print(f"\n=== Kurul {args.kurul} Öğrenci Materyali & Orijinal PDF Eşleşmeleri ===")
        for e in eslesmeler:
            simge = "🎙️" if e["tur"] == "ses" else "📄"
            print(f"\n{simge} Öğrenci Dosyası: [{e['brans']}] {e['dosya_adi']}")
            print(f"   Bulunan Orijinal PDF: {e['orijinal_pdf_adi']}")
            if e["orijinal_pdf"]:
                print(f"   Tam Yol: {e['orijinal_pdf']}")
    elif args.indir and args.id and args.hedef:
        dosya_indir(args.id, args.hedef)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
