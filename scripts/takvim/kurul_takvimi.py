#!/usr/bin/env python3
"""Ders programı PDF'inden kurul takvimini çıkarır → meds/src/data/kurul_takvimi.json

Her kurul için: ad, başlangıç (ilk haftanın pazartesisi), sınav tarihi (KURUL SINAVI
hücresinin sütunu), bitiş, ders listesi (tarih + saat + hücre metni). Modelsiz, yerel.
Ders programı Drive'da değişirse ders işçisi bunu yeniden çalıştırır; çıktı kararlıdır
(aynı PDF → aynı JSON), bu yüzden fark varsa takvim gerçekten değişmiştir.

Kullanım: python3 kurul_takvimi.py [--pdf YOL] [--yaz]
"""
import argparse, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
PDF = KOK / "meds_downloads/drive_root/Ders Programı/2026-27 D3 ders programı.pdf"
CIKTI = KOK / "meds/src/data/kurul_takvimi.json"
AYLAR = {a: i + 1 for i, a in enumerate(
    "ocak şubat mart nisan mayıs haziran temmuz ağustos eylül ekim kasım aralık".split())}
TARIH = re.compile(r"(\d{1,2})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(20\d\d)")


def tr_kucuk(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


def tarih(hucre):
    m = TARIH.search(hucre or "")
    if not m:
        return None
    ay = AYLAR.get(tr_kucuk(m.group(2)))
    return f"{m.group(3)}-{ay:02d}-{int(m.group(1)):02d}" if ay else None


def cikar(pdf):
    import pymupdf
    doc = pymupdf.open(pdf)
    kurullar, cur = [], None
    for sayfa in doc:
        metin = sayfa.get_text()
        m = re.search(r"KURUL\s+(\d)\s*\n\s*(TIP\s*\d+)\s*-\s*([^\n]+(?:\n[^\n]*KURULU)?)", metin)
        if m:
            ad = re.sub(r"\s+", " ", m.group(3)).strip()
            cur = {"kurul": int(m.group(1)), "kod": m.group(2), "ad": ad,
                   "baslangic": None, "sinav": None, "bitis": None, "dersler": []}
            kurullar.append(cur)
        if cur is None:
            continue
        for tablo in sayfa.find_tables().tables:
            satirlar = tablo.extract()
            if not satirlar:
                continue
            gunler = [tarih(h) for h in satirlar[0]]
            if not any(gunler):
                continue
            for g in gunler:
                if g:
                    cur["baslangic"] = min(filter(None, [cur["baslangic"], g]))
                    cur["bitis"] = max(filter(None, [cur["bitis"], g]))
            for satir in satirlar[1:]:
                saat = (satir[0] or "").strip()
                for j, h in enumerate(satir[1:], start=1):
                    h = re.sub(r"\s+", " ", (h or "").replace("Č", "Ğ").replace("č", "ğ")).strip()
                    h = re.sub(r"\s*Bağımsız Öğrenme$", "", h)
                    if not h or j >= len(gunler) or not gunler[j]:
                        continue
                    if "KURUL SINAVI" in h.upper():
                        cur["sinav"] = gunler[j]
                        continue
                    if re.match(r"(?i)^(bağımsız öğrenme|resmi tatil|alan dışı seçmeli|öğle)", h):
                        continue
                    cur["dersler"].append({"tarih": gunler[j], "saat": saat, "metin": h})
    son = doc[-1].get_text()
    f = re.search(r"FİNAL TARİHİ:\s*\|?\s*(\d\d)\.(\d\d)\.(\d{4})", son.replace("\n", " | "))
    b = re.search(r"BÜTÜNLEME TARİHİ:\s*\|?\s*(\d\d)\.(\d\d)\.(\d{4})", son.replace("\n", " | "))
    iso = lambda m: f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None
    for k in kurullar:  # aynı ders saatlerce sürebilir: tekrarı birleştir
        goruldu, tek = set(), []
        for d in k["dersler"]:
            a = (d["tarih"], d["metin"])
            if a not in goruldu:
                goruldu.add(a); tek.append(d)
        k["dersler"] = tek
    return {"surum": 1, "kaynak": str(Path(pdf).name), "egitimYili": "2026-2027", "donem": 3,
            "final": iso(f), "butunleme": iso(b), "kurullar": kurullar}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=str(PDF))
    ap.add_argument("--yaz", action="store_true")
    a = ap.parse_args()
    veri = cikar(a.pdf)
    for k in veri["kurullar"]:
        print(f"Kurul {k['kurul']} {k['ad'][:40]:40} {k['baslangic']} → sınav {k['sinav']} · {len(k['dersler'])} ders")
    eksik = [k["kurul"] for k in veri["kurullar"] if not (k["baslangic"] and k["sinav"])]
    if eksik:
        print("HATA: tarih çıkarılamadı:", eksik); sys.exit(1)
    if a.yaz:
        CIKTI.write_text(json.dumps(veri, ensure_ascii=False, indent=1) + "\n")
        ozet = {k: v for k, v in veri.items() if k != "kurullar"}
        ozet["kurullar"] = [{k: v for k, v in x.items() if k != "dersler"} for x in veri["kurullar"]]
        (CIKTI.parent / "kurul_takvimi_ozet.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=1) + "\n")
        print("yazıldı:", CIKTI, "+ kurul_takvimi_ozet.json")
