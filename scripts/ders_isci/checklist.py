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
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ayarlar import APP, DATABASE, DOWNLOADS, IZLENEN_KOK, KAYIT, KUYRUK, STATE, TASLAK, oku, yaz  # noqa: E402

CHECKLIST = STATE / "checklist.json"
RAPOR = STATE / "durum_raporu.md"
KAPSAM = STATE / "kapsam.json"          # pdf yolu → [{konu, kurul, sayfa_bas, sayfa_bit, yontem, guven}]
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")
ETIKET = {"tamam_2627": "✅ Tamam (2026-27)", "onay_bekliyor": "🟣 Onay bekliyor", "isleniyor": "🔵 İşleniyor",
          "kuyrukta": "🔵 Kuyrukta", "yenilenmeli": "🟠 Yenilenmeli (26-27 PDF geldi, ders geçen yıl kaynaklı)",
          "islenmeli": "🔴 İşlenmeli (26-27 PDF var, ders yok)", "gecen_yil_kaynakli": "🟡 Geçen yıl kaynaklı (26-27 PDF yok)",
          "pdf_bekleniyor": "⚪ PDF bekleniyor"}


def fold(s: str) -> str:
    s = str(s).replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")[:50].strip("-")


def benzer(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, fold(a), fold(b)).ratio()


def k1_dersleri() -> list[dict]:
    """s14_notes.LESSONS (Kurul 1): (ders, konu, hoca, tarih, kaynak_idleri, gecen_yil) → kimlik k1-NN-slug."""
    src = (APP / "scripts" / "v2" / "stages" / "s14_notes.py").read_text(encoding="utf-8")
    m = re.search(r"^LESSONS = (\[.*?^\])", src, re.S | re.M)
    if not m:
        return []
    out = []
    for n, (ders, konu, hoca, tarih, kaynak, gecen) in enumerate(ast.literal_eval(m.group(1)), 1):
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
        taslaklar.append(bg)

    # Satırlar = ders programı konuları ∪ programda olmayan ama işlenmiş dersler (s14) ∪ PDF kapaklarından bulunan konular
    hedefler = [(k.get("kurul"), t) for k in prog.get("kurullar") or [] for t in k.get("konular") or []
                if t.get("tur", "ders") == "ders" and t.get("konu")]

    def programda_var(kurul, konu):
        return any(kk == kurul and benzer(konu, t["konu"]) >= 0.85 for kk, t in hedefler)

    for d in dersler:
        if not programda_var(d["kurul"], d["konu"]):
            hedefler.append((d["kurul"], {"konu": d["konu"], "ders": d["ders"], "tarih": d["tarih"],
                                          "ogretim_uyesi": d["hoca"], "programda_degil": True}))
    for yol, xs in kapsam.items():
        for x in xs:
            if x.get("kurul") and not programda_var(x["kurul"], x["konu"]):
                hedefler.append((x["kurul"], {"konu": x["konu"], "ders": x.get("ders"), "tarih": None,
                                              "ogretim_uyesi": x.get("ogretim_uyesi"), "programda_degil": True}))
    satirlar = []
    gorulen = set()
    for kurul, t in hedefler:
        konu = t["konu"]
        anahtar = (kurul, fold(konu))
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        if True:
            ders = max((d for d in dersler if d["kurul"] == kurul), key=lambda d: benzer(konu, d["konu"]), default=None)
            if ders and benzer(konu, ders["konu"]) < 0.85:
                ders = None
            deste_id = f"k{kurul}p-{ders['id']}" if ders else None
            # Bu yılın PDF'leri: kapsam haritasında bu konuyu içeren izlenen-kök PDF'leri
            pdfler = [{"pdf": yol, "sayfa": f"{x.get('sayfa_bas', '?')}–{x.get('sayfa_bit', '?')}", "yontem": x.get("yontem")}
                      for yol, xs in kapsam.items() for x in xs
                      if x.get("kurul") == kurul and benzer(x.get("konu", ""), konu) >= 0.9]
            # s14 kaynağı izlenen kökten mi (= 2026-27 PDF)?
            ders_kaynak_2627 = bool(ders) and any((manifest.get(sid) or {}).get("root") == IZLENEN_KOK for sid in ders["kaynak_idleri"])
            taslak = next((x for x in taslaklar if x.get("kurul") == kurul
                           and benzer((x.get("program") or {}).get("konu") or "", konu) >= 0.9), None)
            bekleyen = any(j["durum"] in ("bekliyor", "isleniyor") and any(benzer(p["pdf"], j["yol"]) > 0.95 for p in pdfler)
                           for j in kuyruk)
            bilesen = {
                "deste": bool(deste_id and deste_id in deck_ids),
                "not": bool(ders) and any((ROOT_STUDY / f"k{kurul}").glob(f"{ders['numara']:02d}_*.md")) if ders else False,
                "ornek": bool(ders) and (APP / "src" / "data" / "ornek_sorular" / f"k{kurul}" / f"{ders['id']}.json").exists() if ders else False,
            }
            if taslak and taslak["_durum"] == "onay_bekliyor":
                durum = "onay_bekliyor"
            elif taslak:
                durum = "isleniyor"
            elif bekleyen:
                durum = "kuyrukta"
            elif ders and bilesen["deste"] and not ders["gecen_yil"] and (ders_kaynak_2627 or not pdfler):
                durum = "tamam_2627"
            elif ders and pdfler:
                durum = "yenilenmeli" if (ders["gecen_yil"] or not ders_kaynak_2627) else "tamam_2627"
            elif ders:
                durum = "gecen_yil_kaynakli" if ders["gecen_yil"] else "tamam_2627"
            elif pdfler:
                durum = "islenmeli"
            else:
                durum = "pdf_bekleniyor"
            satirlar.append({"kurul": kurul, "tarih": t.get("tarih"), "ders": t.get("ders"), "konu": konu,
                             "programda": not t.get("programda_degil"),
                             "hoca": t.get("ogretim_uyesi"), "durum": durum, "ders_id": ders["id"] if ders else None,
                             "deste_id": deste_id, "gecen_yil_kaynagi": ders["gecen_yil"] if ders else None,
                             "bilesenler": bilesen, "pdf_2627": pdfler,
                             "taslak": {"is_id": taslak.get("is_id"), "durum": taslak["_durum"]} if taslak else None})
    from collections import Counter
    sayim = Counter(s["durum"] for s in satirlar)
    veri = {"uretim": time.strftime("%Y-%m-%d %H:%M"), "akademik_yil": "2026-27", "sayim": dict(sayim), "konular": satirlar}
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
