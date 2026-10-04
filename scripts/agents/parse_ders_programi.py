#!/usr/bin/env python3
"""
Ders programı ayrıştırıcı (tamamen yerel, token harcamaz).

Girdi : "2026-27 D3 ders programı.pdf"  (Kurul başlık sayfaları + haftalık tablolar)
Çıktı : kurul -> dersler (saat, öğretim üyeleri) -> işlenen konular (tarih, saat, hoca, hafta)
        + her konu için meds_downloads içindeki olası PDF eşleşmesi (skorlu ADAY; kesin değildir).

  parse_ders_programi.py [PDF] [--out JSON] [--downloads KLASÖR]

Varsayılan çıktı: meds_database/taxonomy/donem3_ders_programi.json
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[3]
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT / "meds_database")
DOWNLOADS = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or ROOT / "meds_downloads")
DEFAULT_PDF = DOWNLOADS / "drive_root" / "Ders Programı" / "2026-27 D3 ders programı.pdf"
DEFAULT_OUT = DB / "taxonomy" / "donem3_ders_programi.json"

MONTHS = {"ocak": 1, "şubat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "haziran": 6, "temmuz": 7,
          "ağustos": 8, "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12}
# Unvan; PDF'ten gelen metinde noktalar çoğu zaman düşmüş olur ("DR ÖĞR ÜYESİ ...")
TITLE_RE = re.compile(
    r"(?<![\wÇĞİÖŞÜçğıöşü])((?:PROF|DOÇ|UZ|ARŞ|DR)\.?\s*(?:DR\.?|ÖĞR\.?|GÖR\.?|)\s*(?:ÜYESİ|ÜYESI)?)(?![\wÇĞİÖŞÜçğıöşü])")
NON_LESSON = ["bağımsız öğrenme", "alan dışı seçmeli", "klinik ve mesleki", "kurul sınavı", "resmi tatil",
              "yarıyıl tatili", "final", "bütünleme", "tatil"]


def fold(s: str) -> str:
    """Eşleştirme için: küçük harf, Türkçe karakterleri ASCII'ye indir, noktalama at."""
    s = s.replace("İ", "i").replace("I", "ı").lower()
    s = s.translate(str.maketrans("çğıöşüâîû", "cgiosuaiu"))
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", s).split())


def norm_space(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\n", " ")).strip()


def fix_name(s: str) -> str:
    return norm_space(s).replace("ÖČR", "ÖĞR").replace("ÜYESI", "ÜYESİ")


# --------------------------------------------------------------------------- kurul başlığı
def parse_kurul_header(page) -> dict | None:
    text = page.get_text()
    m = re.search(r"DÖNEM\s*(\d)\s*KURUL\s*(\d)", text)
    if not m:
        return None
    code = re.search(r"TIP\s*(\d{3})\s*-\s*([^\n]+)", text)
    info = {"donem": int(m.group(1)), "kurul": int(m.group(2)),
            "kod": f"TIP {code.group(1)}" if code else None,
            "ad": norm_space(code.group(2)) if code else None,
            "yetkililer": {}, "dersler": []}
    tabs = page.find_tables().tables
    if not tabs:
        return info
    cur = None
    pending = None  # satır bölünmüş hoca adı
    for row in tabs[0].extract():
        c = [norm_space(x) if x is not None else None for x in (row + [None] * 4)[:4]]
        c0, c1, c2, c3 = c
        if c0 in ("Dekan", "Dekan Yardımcıları", "Başkoordinatör", "Koordinatör", "Kurul Başkanı"):
            info["yetkililer"][c0] = fix_name(c1 or "")
            continue
        if c0 and c0.upper().startswith("DERSLER"):
            continue
        if c0 and c0.upper().startswith("TOPLAM"):
            tm = re.search(r"\d+", c1 or "")
            info["toplam_saat"] = int(tm.group()) if tm else None
            continue
        if c0:
            cur = {"ders": c0, "toplam_saat": int(re.sub(r"\D", "", c1)) if c1 and re.search(r"\d", c1) else None,
                   "ogretim_uyeleri": []}
            info["dersler"].append(cur)
        if cur is None:
            continue
        hours = re.search(r"(\d+)\s*$", c3 or "")
        name = fix_name(c2 or "")
        if name and hours:
            if pending:
                name, pending = pending + " " + name, None
            cur["ogretim_uyeleri"].append({"ad": name, "saat": int(hours.group(1))})
        elif name and not hours:
            pending = name
        elif not name and c0 is None and c1 and hours:
            pass
        # Bölünmüş soyad satırı: ad boş değil, başlıksız, saat var
    # Bölünmüş isim düzeltmesi: "…MEHMET MURAT" + "ŞAHİN" zaten birleştirildi
    return info


# --------------------------------------------------------------------------- haftalık tablo
def parse_date(cell: str) -> str | None:
    m = re.search(r"(\d{1,2})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(\d{4})", cell or "")
    if not m:
        return None
    mon = MONTHS.get(m.group(2).lower().replace("i̇", "i"))
    return f"{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}" if mon else None


ALIASES = {"dahiliye": "İç Hastalıkları", "anestezi": "Anestezi ve Reanimasyon",
           "iç hastalıkları (dahiliye)": "İç Hastalıkları"}


def _nospace(x: str) -> str:
    return fold(x).replace(" ", "")


def _find_ders(words: list[str], ders_names: list[str]):
    """Kelime dizisinde ilk geçen ders adı (boşluk/yazım farklarına toleranslı): (idx, ders, kelime_sayısı)."""
    cands = [(dn, dn) for dn in ders_names]
    cands += [(al, can) for al, can in ALIASES.items() if can in ders_names]
    best = None
    for alias, canon in sorted(cands, key=lambda c: len(c[0]), reverse=True):
        target = _nospace(alias)
        for i in range(len(words)):
            acc = ""
            for j in range(i, min(len(words), i + 8)):
                acc += _nospace(words[j])
                if acc == target:
                    if best is None or i < best[0]:
                        best = (i, canon, j - i + 1)
                    break
                if not target.startswith(acc):
                    break
    return best


def _complete_hoca(hoca: str, instructors: list[str]) -> str:
    hoca = fix_name(hoca)
    for ins in instructors:  # kesik hoca adını tamamla (önek)
        if fold(ins).startswith(fold(hoca)) and len(ins) >= len(hoca):
            return ins
    for ins in instructors:  # taşan soyad/ad parçası (sonek)
        if fold(ins).endswith(fold(hoca)) and len(fold(hoca)) >= 4:
            return ins
    return hoca


def split_cell(text: str, ders_names: list[str], instructors: list[str]):
    """Hücre -> (ders, konu, hoca, tür, başta_taşan_hoca).

    PDF tablosunda hoca adı bazen önceki satırın sonundan bu hücrenin başına taşar
    ("HOCA Ders Konu"); bu durumda başta_taşan_hoca döner ve çağıran taraf karar verir.
    """
    t = norm_space(text).replace("ÖČR", "ÖĞR").replace("ÜYESI", "ÜYESİ")
    low = fold(t)
    for k in NON_LESSON:
        if low.startswith(fold(k)):
            return None, t, None, "diger", None
    words = t.split()
    found = _find_ders(words, ders_names)
    lead = None
    if found:
        i, dn, n = found
        if i > 0:
            cand = _complete_hoca(" ".join(words[:i]), instructors)
            if cand in instructors or TITLE_RE.match(cand):
                lead = cand
        # Bağımsız Öğrenme gibi etkinlikler başta hoca taşmasıyla gelebilir
        rest_words = words[i + n:]
        ders = dn
        t = " ".join(rest_words)
    else:
        # "HOCA Bağımsız Öğrenme" gibi: hoca + etkinlik
        for k in NON_LESSON:
            idx = low.find(fold(k))
            if idx > 0:
                for j in range(1, len(words)):
                    if fold(" ".join(words[j:])).startswith(fold(k)):
                        cand = _complete_hoca(" ".join(words[:j]), instructors)
                        lead = cand if (cand in instructors or TITLE_RE.match(cand)) else None
                        return None, " ".join(words[j:]), None, "diger", lead
        return None, t, None, "diger", None
    hoca = None
    m = TITLE_RE.search(t)
    if m:
        hoca, t = _complete_hoca(t[m.start():], instructors), t[:m.start()].strip()
    topic = t.strip().rstrip(":").strip()
    return ders, topic, hoca, "ders", lead


def parse_week_page(page, kurul: dict):
    tabs = page.find_tables().tables
    if not tabs:
        return None
    rows = tabs[0].extract()
    head = rows[0]
    wk = re.match(r"(\d+)\.\s*HAFTA", norm_space(head[0]))
    if not wk:
        return None
    dates = [parse_date(h or "") for h in head[1:]]
    ders_names = [d["ders"] for d in kurul["dersler"]]
    instructors = [o["ad"] for d in kurul["dersler"] for o in d["ogretim_uyeleri"]]
    items = []
    for row in rows[1:]:
        slot = norm_space(row[0])
        if not re.match(r"\d{2}:\d{2}", slot or ""):
            continue
        for di, cell in enumerate(row[1:6]):
            date = dates[di] if di < len(dates) else None
            items.append({"tarih": date, "gun_no": di, "saat_dilimi": slot, "ham": norm_space(cell)})
    return int(wk.group(1)), dates, items


def merge_lessons(items, kurul, hafta, ders_names, instructors):
    """Ardışık dilimleri tek konuda birleştirir.

    - boş hücre (öğle arası hariç) = önceki dersin birleşik hücre devamı (+1 saat)
    - hücre başındaki taşan hoca adı, önceki ders hocasızsa ona, değilse bu derse aittir
    """
    by_day: dict[int, list] = {}
    for it in items:
        by_day.setdefault(it["gun_no"], []).append(it)
    out = []
    for day, slots in by_day.items():
        last = None
        for it in slots:
            raw = it["ham"]
            lunch = it["saat_dilimi"].replace(" ", "").startswith("12:10")
            if lunch:
                last = None
                continue
            if not raw:
                if last is not None:
                    last["saat"] += 1
                    last["saat_dilimleri"].append(it["saat_dilimi"])
                continue
            ders, topic, hoca, tur, lead = split_cell(raw, ders_names, instructors)
            if lead and hoca and hoca not in instructors:
                for ins in instructors:  # "PROF. DR. NURHAYAT ÖZKAN" + "SEVENCAN"
                    if fold(ins).startswith(fold(hoca)) and fold(ins).endswith(fold(lead.split()[-1])):
                        hoca, lead = ins, None
                        break
            if lead:
                if last is not None and last["tur"] == "ders" and not last["ogretim_uyesi"]:
                    last["ogretim_uyesi"] = lead
                elif hoca is None and tur == "ders":
                    hoca = lead
            key = (ders, topic, tur)
            if last and last["_key"] == key:
                last["saat"] += 1
                last["saat_dilimleri"].append(it["saat_dilimi"])
                if not last["ogretim_uyesi"]:
                    last["ogretim_uyesi"] = hoca
            else:
                last = {"_key": key, "kurul": kurul, "hafta": hafta, "tarih": it["tarih"], "tur": tur,
                        "ders": ders, "konu": topic, "ogretim_uyesi": hoca, "saat": 1,
                        "saat_dilimleri": [it["saat_dilimi"]], "ham_hucre": raw}
                out.append(last)
    for o in out:
        o.pop("_key", None)
    return out


# --------------------------------------------------------------------------- PDF eşleştirme (aday)
def index_pdfs(downloads: Path):
    idx = []
    for f in downloads.rglob("*.pdf"):
        if "Ders Programı" in str(f):
            continue
        parts = f.relative_to(downloads).parts
        kurul = next((int(m.group(1)) for p in parts if (m := re.match(r"Kurul\s*(\d)", p, re.I))), None)
        ders_klasoru = parts[-2] if len(parts) >= 2 else ""
        stem = re.sub(r"^\s*\d+\s*[\)\.\-]\s*", "", f.stem)
        idx.append({"path": str(f), "kurul": kurul, "ders_klasoru": ders_klasoru, "ad": f.stem, "fold": fold(stem)})
    return idx


def match_pdfs(lesson: dict, pdfs: list[dict]):
    if lesson["tur"] != "ders" or not lesson["konu"]:
        return []
    topic = fold(lesson["konu"])
    cand = []
    for p in pdfs:
        if p["kurul"] != lesson["kurul"]:
            continue
        same_ders = bool(lesson["ders"]) and fold(lesson["ders"]) == fold(p["ders_klasoru"])
        r = difflib.SequenceMatcher(None, topic, p["fold"]).ratio()
        tw, pw = set(topic.split()), set(p["fold"].split())
        jac = len(tw & pw) / max(1, len(tw | pw))
        score = 0.6 * r + 0.4 * jac + (0.1 if same_ders else 0)
        if score >= 0.45:
            cand.append({"pdf": p["path"], "skor": round(min(score, 1.0), 3), "ayni_ders_klasoru": same_ders})
    return sorted(cand, key=lambda x: -x["skor"])[:3]


# --------------------------------------------------------------------------- ana akış
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--downloads", type=Path, default=DOWNLOADS)
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    kurullar: dict[int, dict] = {}
    cur = None
    lessons: list[dict] = []
    final_info = {}
    for page in doc:
        hdr = parse_kurul_header(page)
        if hdr:
            cur = hdr
            kurullar[hdr["kurul"]] = hdr
            continue
        text = page.get_text()
        if "FİNAL TARİHİ" in text:
            m = re.search(r"FİNAL TARİHİ:\s*([\d.]+)", text)
            b = re.search(r"BÜTÜNLEME TARİHİ:\s*([\d.]+)", text)
            final_info = {"final": m.group(1) if m else None, "butunleme": b.group(1) if b else None}
            continue
        if not cur:
            continue
        res = parse_week_page(page, cur)
        if not res:
            continue
        hafta, dates, items = res
        names = [d["ders"] for d in cur["dersler"]]
        ins = [o["ad"] for d in cur["dersler"] for o in d["ogretim_uyeleri"]]
        lessons += merge_lessons(items, cur["kurul"], hafta, names, ins)

    pdfs = index_pdfs(a.downloads) if a.downloads.exists() else []
    for l in lessons:
        l["pdf_adaylari"] = match_pdfs(l, pdfs)
        l["pdf_eslesme_durumu"] = ("aday_yuksek" if l["pdf_adaylari"] and l["pdf_adaylari"][0]["skor"] >= 0.75
                                   else "aday_dusuk" if l["pdf_adaylari"] else "yok")

    result = {
        "stage": "curriculum",
        "kaynak": str(a.pdf),
        "donem": 3,
        "akademik_yil": "2026-2027",
        "dogrulandi": False,
        "dogrulama": "otomatik ayrıştırma (taslak); eşleşmeler ADAY'dır. Saat uyumsuzlukları saat_dogrulama alanında. Teyitten sonra meds_database'e alınır.",
        "final": final_info,
        "kurullar": [
            {**{k: v for k, v in k_.items()},
             "konular": [l for l in lessons if l["kurul"] == k_["kurul"] and l["tur"] == "ders"]}
            for k_ in sorted(kurullar.values(), key=lambda x: x["kurul"])
        ],
        "diger_etkinlikler": [l for l in lessons if l["tur"] != "ders"],
    }
    # Doğrulama: programdaki ders saatleri ile okunan saatler
    import collections
    for k_ in result["kurullar"]:
        got = collections.Counter()
        for l in k_["konular"]:
            got[l["ders"]] += l["saat"]
        k_["saat_dogrulama"] = [
            {"ders": d["ders"], "programdaki": d["toplam_saat"], "okunan": got[d["ders"]],
             "uyumlu": d["toplam_saat"] == got[d["ders"]]} for d in k_["dersler"]
        ]
        k_["tamamen_dogrulandi"] = all(x["uyumlu"] for x in k_["saat_dogrulama"])
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"Yazıldı: {a.out}")
    for k_ in result["kurullar"]:
        total = sum(l["saat"] for l in k_["konular"])
        declared = k_.get("toplam_saat")
        print(f"  Kurul {k_['kurul']} {k_['kod']} {k_['ad']}: {len(k_['dersler'])} ders, "
              f"{len(k_['konular'])} konu, {total} saat (programda toplam {declared})")


if __name__ == "__main__":
    main()
