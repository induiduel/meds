#!/usr/bin/env python3
"""2026-27 ders checklist'i ve durum raporu.

Her ders programı konusu (tüm kurullar, tür = ders) için:
  - mevcut ders paketi/deste/not/örnek sorular (Kurul 1: s14 LESSONS listesi; kaynak PDF ve 'geçen yıl kaynağı' bayrağı)
  - 2026-27 Drive PDF'i (izlenen kök) ve PDF'in hangi sayfaları bu konuyu kapsıyor (bir PDF birden çok konu içerebilir)
  - ders işçisi taslak durumu
  → durum: tamam_2627 | onay_bekliyor | isleniyor | yenilenmeli | islenmeli | gecen_yil_kaynakli | pdf_bekleniyor

  checklist.py            → <durum>/checklist.json + durum_raporu.md (+ ekrana özet)
Kuyruğa alma kuralı (izle.py): bir PDF'in kapsadığı konulardan biri 'yenilenmeli' ya da 'islenmeli' ise PDF işlenir.
"""
from __future__ import annotations

import ast
import difflib
import re
import unicodedata
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ayarlar import APP, DATABASE, DOWNLOADS, IZLENEN_KOK, KAYIT, KUYRUK, STATE, TASLAK, oku, yaz  # noqa: E402

CHECKLIST = STATE / "checklist.json"
RAPOR = STATE / "durum_raporu.md"
KAPSAM = STATE / "kapsam.json"          # pdf yolu → [{konu, kurul, sayfa_bas, sayfa_bit, yontem, guven}]
# Kullanıcının elle verdiği eşleşme kararları (otomatik eşleşmeyi ezer): pdf yolu → {kurul, konu, not}
ESLESME_DUZELTME = STATE / "eslesme_duzeltme.json"
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")
ETIKET = {"tamam_2627": "✅ Tamam (2026-27)", "onay_bekliyor": "🟣 Onay bekliyor", "isleniyor": "🔵 İşleniyor",
          "kuyrukta": "🔵 Kuyrukta", "yenilenmeli": "🟠 Yenilenmeli (26-27 PDF geldi, ders geçen yıl kaynaklı)",
          "islenmeli": "🔴 İşlenmeli (26-27 PDF var, ders yok)", "gecen_yil_kaynakli": "🟡 Geçen yıl kaynaklı (26-27 PDF yok)",
          "pdf_bekleniyor": "⚪ PDF bekleniyor"}


def fold(s: str) -> str:
    s = str(s).replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))  # i̇ → i (nokta silinir, boşluk değil)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")[:50].strip("-")


SINONIM = [(r"\bovaryum\b|\bovaryan\b", "over"), (r"\bpatofizyoloji", "fizyopatoloji"),
           (r"\b(?:uro|nefro)litiyazis\b", "uriner sistem tas hastaliklari"),
           (r"cinsel yolla bulasan hastalik", "cinsel yolla bulasan enfeksiyon"), (r"\bsifiliz\b", "sifilis"),
           (r"\bglomeruler\b", "glomeruler")]
DURAK = {"ve", "ile", "icin", "bir", "veya", "de", "da", "in", "nin"}


def norm_konu(s: str) -> str:
    f = fold(re.sub(r"^[\s'\"“”‘’]+|[\s'\"“”‘’.]+$", "", str(s)))
    for a, b in SINONIM:
        f = re.sub(a, b, f)
    return f


def kokler(s: str) -> frozenset:
    # Kısa kelimeler atılır AMA bölüm numaraları korunur (Nekroz - I ≠ Nekroz - II; Ders 1 ≠ Ders 2)
    return frozenset(w[:5] for w in norm_konu(s).split()
                     if (len(w) >= 3 and w not in DURAK) or w.isdigit() or re.fullmatch(r"[ivx]{1,4}", w))


def ayni_konu(a: str, b: str) -> bool:
    """Kesin konu eşitliği: normalize ad aynı ya da anlamlı kelime kökleri birebir aynı (Nefrotik ≠ Nefritik)."""
    if norm_konu(a) == norm_konu(b):
        return True
    ka, kb = kokler(a), kokler(b)
    return bool(ka) and ka == kb


def benzer(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, fold(a), fold(b)).ratio()


def k1_dersleri() -> list[dict]:
    """s14_notes.LESSONS + yayin_kaydi.json (Kurul 1): (ders, konu, hoca, tarih, kaynak_idleri, gecen_yil) → k1-NN-slug."""
    src = (APP / "scripts" / "v2" / "stages" / "s14_notes.py").read_text(encoding="utf-8")
    m = re.search(r"^LESSONS = (\[.*?^\])", src, re.S | re.M)
    if not m:
        return []
    liste = dict(enumerate(ast.literal_eval(m.group(1)), 1))
    for y in oku(APP / "scripts" / "ders_isci" / "yayin_kaydi.json", []):   # onaylanıp yayınlanan dersler
        if y.get("kurul") == 1:
            liste[y["numara"]] = (y["ders"], y["konu"], y["hoca"], y.get("tarih") or "", y["kaynak_idleri"], False)
    out = []
    for n, (ders, konu, hoca, tarih, kaynak, gecen) in sorted(liste.items()):
        s = re.sub(r"[^a-z0-9]+", "_", fold(konu)).strip("_")[:50].replace("_", "-")
        out.append({"kurul": 1, "numara": n, "id": f"k1-{n:02d}-{s}", "ders": ders, "konu": konu, "hoca": hoca,
                    "tarih": tarih, "kaynak_idleri": kaynak, "gecen_yil": bool(gecen)})
    return out


def olustur() -> dict:
    prog = oku(DATABASE / "taxonomy" / "donem3_ders_programi.json", {})
    decks = oku(APP / "src" / "data" / "interactive_learning_decks.json", [])
    deck_ids = {d.get("id") for d in (decks if isinstance(decks, list) else [])}
    manifest = {i.get("source_id"): i for i in oku(DOWNLOADS / "_manifest.json", {}).get("items", [])}
    dersler = k1_dersleri()
    kapsam = oku(KAPSAM, {})
    kuyruk = oku(KUYRUK, [])
    taslaklar = []
    for b in TASLAK.glob("*/baglam.json"):
        bg = oku(b, {})
        bg["_durum"] = oku(b.parent / "durum.json", {}).get("durum") or "isleniyor"
        if bg["_durum"] not in ("yayinlandi", "reddedildi"):   # yayınlanan ders artık kaynaklarda (yayin_kaydi.json)
            taslaklar.append(bg)

    # ---- kaynak kimliği → yerel PDF yolu (s14 dersleri hangi Drive PDF'inden üretildi: kesin bağ)
    man_items = oku(DOWNLOADS / "_manifest.json", {}).get("items", [])
    indir = oku(DOWNLOADS / "_downloads.json", {})
    sid_yol = {}
    for it in man_items:
        if it.get("root") == IZLENEN_KOK and it.get("drive_id") in indir:
            yp = str(indir[it["drive_id"]].get("path") or "")
            if yp.startswith(IZLENEN_KOK + "/"):
                sid_yol[it["source_id"]] = yp[len(IZLENEN_KOK) + 1:]

    satirlar: list[dict] = []

    def satir_bul(kurul, konu):
        r = next((r for r in satirlar if r["kurul"] == kurul and ayni_konu(r["konu"], konu)), None)
        if r:
            return r
        # Alt küme kuralı: kısa ad uzun adın kelimelerinin alt kümesi (≥3 anlamlı kök) ve TEK aday varsa aynı konu
        # ("Ürogenital Sistem Tümörlerinde Genetik Belirteçler" ⊂ "... ve Kliniğe Yansımaları"); Nekroz I/II gibi çoklu adayda bağlanmaz.
        kk = kokler(konu)
        aday = [r for r in satirlar if r["kurul"] == kurul and len(kk) >= 3 and len(kokler(r["konu"])) >= 3
                and (kk <= kokler(r["konu"]) or kokler(r["konu"]) <= kk)]
        return aday[0] if len(aday) == 1 else None

    def satir_ekle(kurul, t, programda=True):
        r = {"kurul": kurul, "tarih": t.get("tarih"), "ders": t.get("ders"), "konu": t["konu"], "programda": programda,
             "hoca": t.get("ogretim_uyesi"), "_ders": None, "_pdf": []}
        satirlar.append(r)
        return r

    for k in prog.get("kurullar") or []:                       # a) ders programı
        for t in k.get("konular") or []:
            if t.get("tur", "ders") == "ders" and t.get("konu") and not satir_bul(k.get("kurul"), t["konu"]):
                satir_ekle(k.get("kurul"), t)
    for d in dersler:                                           # b) işlenmiş dersler (programda yoksa ek satır)
        r = satir_bul(d["kurul"], d["konu"]) or satir_ekle(d["kurul"], {"konu": d["konu"], "ders": d["ders"],
                                                                         "tarih": d["tarih"], "ogretim_uyesi": d["hoca"]}, False)
        r["_ders"] = d
        for sid in d["kaynak_idleri"]:                          #    dersin kendi kaynak PDF'i (kesin)
            if sid in sid_yol:
                r["_pdf"].append({"pdf": sid_yol[sid], "sayfa": "tümü", "yontem": "ders_kaynagi"})
    ders_kaynak_pdf = {x["pdf"] for r in satirlar for x in r["_pdf"]}
    pdf_konulari: dict[str, list] = {}
    duzeltme = oku(ESLESME_DUZELTME, {})
    for yol, xs in kapsam.items():                              # c) kapsam haritası (yeni / ders kaynağı olmayan PDF'ler)
        if yol in duzeltme:                                     #    kullanıcı kararı: tüm PDF bu konuya aittir
            dz = duzeltme[yol]
            x0 = xs[0] if xs else {}
            xs = [{**x0, "konu": dz["konu"], "kurul": dz.get("kurul", x0.get("kurul")), "programda": True,
                   "yontem": "kullanici", "guven": "kullanici", "kullanici_notu": dz.get("not", ""),
                   "sayfa_bas": 1, "sayfa_bit": max((x.get("sayfa_bit") or 1) for x in xs) if xs else None}]
        if yol in ders_kaynak_pdf:
            r = next(r for r in satirlar if any(x["pdf"] == yol for x in r["_pdf"]))
            pdf_konulari[yol] = [{**(xs[0] if xs else {}), "konu": r["konu"], "kurul": r["kurul"], "_satir": r}]
            continue
        for x in xs:
            kurul = x.get("kurul")
            if not kurul:
                continue
            r = satir_bul(kurul, x["konu"]) or satir_ekle(kurul, {"konu": x["konu"], "ders": x.get("ders"),
                                                                  "ogretim_uyesi": x.get("ogretim_uyesi")}, bool(x.get("programda")))
            r["_pdf"].append({"pdf": yol, "sayfa": f"{x.get('sayfa_bas', '?')}–{x.get('sayfa_bit', '?')}", "yontem": x.get("yontem")})
            pdf_konulari.setdefault(yol, []).append({**x, "_satir": r})

    for r in satirlar:
        kurul, konu, ders = r["kurul"], r["konu"], r["_ders"]
        pdfler = r["_pdf"]
        deste_id = f"k{kurul}p-{ders['id']}" if ders else None
        ders_kaynak_2627 = bool(ders) and any(sid in sid_yol for sid in ders["kaynak_idleri"])
        taslak = next((x for x in taslaklar if x.get("kurul") == kurul
                       and ayni_konu((x.get("program") or {}).get("konu") or "", konu)), None)
        bekleyen = any(j["durum"] in ("bekliyor", "isleniyor") and any(p["pdf"] == j["yol"] for p in pdfler) for j in kuyruk)
        bilesen = {
            "deste": bool(deste_id and deste_id in deck_ids),
            "not": bool(ders) and any((ROOT_STUDY / f"k{kurul}").glob(f"{ders['numara']:02d}_*.md")),
            "ornek": bool(ders) and (APP / "src" / "data" / "ornek_sorular" / f"k{kurul}" / f"{ders['id']}.json").exists(),
        }
        if taslak and taslak["_durum"] == "onay_bekliyor":
            durum = "onay_bekliyor"
        elif taslak:
            durum = "isleniyor"
        elif bekleyen:
            durum = "kuyrukta"
        elif ders and not ders["gecen_yil"] and bilesen["deste"]:
            durum = "tamam_2627"
        elif ders and pdfler:
            durum = "yenilenmeli"          # ders geçen yıl kaynağıyla hazırlanmış; bu yılın PDF'i geldi
        elif ders:
            durum = "gecen_yil_kaynakli"
        elif pdfler:
            durum = "islenmeli"
        else:
            durum = "pdf_bekleniyor"
        r.update({"durum": durum, "ders_id": ders["id"] if ders else None, "deste_id": deste_id,
                  "gecen_yil_kaynagi": ders["gecen_yil"] if ders else None, "ders_kaynagi_2627": ders_kaynak_2627,
                  "bilesenler": bilesen, "pdf_2627": pdfler,
                  "taslak": {"is_id": taslak.get("is_id"), "durum": taslak["_durum"]} if taslak else None})
    for r in satirlar:
        r.pop("_ders", None)
        r.pop("_pdf", None)
    pdf_konu_ozet = {yol: [{k: v for k, v in x.items() if k != "_satir"} | {"durum": x["_satir"]["durum"],
                            "satir_konu": x["_satir"]["konu"], "programda": x["_satir"]["programda"],
                            "tarih": x["_satir"]["tarih"], "ogretim_uyesi": x["_satir"]["hoca"]} for x in xs]
                     for yol, xs in pdf_konulari.items()}
    from collections import Counter
    sayim = Counter(x["durum"] for x in satirlar)
    veri = {"uretim": time.strftime("%Y-%m-%d %H:%M"), "akademik_yil": "2026-27", "sayim": dict(sayim), "konular": satirlar,
            "pdf_konulari": pdf_konu_ozet}
    yaz(CHECKLIST, veri)
    rapor_yaz(veri)
    return veri


ROOT_STUDY = Path(__import__("os").environ.get("MEDS_TEMP_DIR") or APP.parent / "meds_temp") / "study"


def rapor_yaz(v: dict):
    s = [f"# 2026-27 Ders Durum Raporu\n", f"_Üretim: {v['uretim']}_\n", "## Özet\n"]
    for d, et in ETIKET.items():
        if v["sayim"].get(d):
            s.append(f"- {et}: **{v['sayim'][d]}**")
    for kurul in sorted({x["kurul"] for x in v["konular"]}):
        s.append(f"\n## Kurul {kurul}\n")
        s.append("| Tarih | Ders | Konu | Durum | Deste | Not | Soru | 26-27 PDF (sayfa) |")
        s.append("|---|---|---|---|:-:|:-:|:-:|---|")
        for x in sorted((x for x in v["konular"] if x["kurul"] == kurul), key=lambda x: (x["tarih"] or "", x["ders"] or "")):
            b = x["bilesenler"]
            pdf = "; ".join(f"{Path(p['pdf']).name} ({p['sayfa']})" for p in x["pdf_2627"]) or "—"
            s.append(f"| {x['tarih'] or '—'} | {x['ders'] or ''} | {x['konu']}{'' if x.get('programda', True) else ' *(programda yok)*'} | {ETIKET[x['durum']]} | "
                     f"{'✓' if b['deste'] else '·'} | {'✓' if b['not'] else '·'} | {'✓' if b['ornek'] else '·'} | {pdf} |")
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")


if __name__ == "__main__":
    v = olustur()
    print(f"checklist: {len(v['konular'])} konu → {v['sayim']}\n  {CHECKLIST}\n  {RAPOR}")
