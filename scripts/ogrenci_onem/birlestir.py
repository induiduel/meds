#!/usr/bin/env python3
"""Öğrenci önem notlarını ders başına önem birimlerine çevirir ve çıkmış bankasıyla eşler (LLM yok; bge-m3 CPU :8094).

  python3 scripts/ogrenci_onem/birlestir.py            # data/ogrenci_onem/ham → src/data/ogrenci_onem/<k2-xx>.json + index.json

Adımlar:
 1. Ham sayfa okumaları (iki geçişli, görüntüden) birleştirilir; `duzeltme` kayıtları metne uygulanır (ham → doğru).
 2. Birim = slayt / öğrenci özeti / el yazısı bloğu. Yapıştırılmış çıkmış soru blokları aynı dersin en yakın birimine bağlanır
    (birimin `cikmis` sinyali, soru metni `ogrenci_sorulari`'na).
 3. Bankadaki Kurul 2 çıkmışları (Psikiyatri, Nöroloji, Tıbbi Genetik, FTR; karantina dışı) konu adından derse bağlanır,
    soru kökü + doğru şık o dersin birimlerine bge-m3 ile eşlenir (eşik ESIK_BANKA); eşleşen birim `banka_cikmis` alır.
 4. Puan = sinyal ağırlıkları toplamı (ortak.AGIRLIK) → öncelik A/B/C. Puan bir YÖNLENDİRMEDİR, tıbbi kanıt değildir.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
from ortak import AGIRLIK, CIKTI, HAM, KOK, PAST, PDF_BRANS, ders_kaydi, norm, oku_json, oncelik  # noqa: E402

ESIK_BANKA = 0.60   # soru ↔ birim kosinüs (bge-m3); sınama: docs/OGRENCI_ONEM_YONTEMI.md §4
ESIK_YAPISTIR = 0.50


def karantina() -> set[str]:
    p = Path(KOK.parent / "meds_database/derived/quarantine/karantina.json")
    d = oku_json(p, {}) or {}
    return {k for k, v in (d.get("sorular") or {}).items()
            if any(n in (v.get("neden") or []) for n in ("kaynak_bulunamadi", "kurul2_disi"))}


def duzelt(metin: str, duz: list[dict]) -> str:
    for d in duz or []:
        h, y = (d.get("ham") or "").strip(), (d.get("dogru") or "").strip()
        if h and y and h in metin:
            metin = metin.replace(h, y)
    return metin


def birim_metni(b: dict) -> str:
    el = " ".join(e.get("metin", "") for e in b.get("el_yazisi") or [])
    return " ".join(x for x in [b.get("baslik") or "", b.get("metin") or "", el] if x).strip()


def soru_metni(c: dict) -> str:
    return (c.get("kok") or "") + " " + " ".join(c.get("siklar") or [])


def banka_sorulari(kayit: dict) -> list[dict]:
    konu2ders = {(d["brans"], norm(d["konu"])): d["id"] for d in kayit.values()}
    brans_esle = {"Psikiyatri": "Psikiyatri", "Nöroloji": "Nöroloji", "Tıbbi Genetik": "Tıbbi Genetik", "FTR": "FTR"}
    kar = karantina()
    out, gor = [], set()
    for q in json.loads(PAST.read_text()):
        if q.get("kurul") != 2 or q.get("discipline") not in brans_esle or q["id"] in kar or not q.get("stem"):
            continue
        ders = konu2ders.get((q["discipline"], norm(q.get("topic") or "")))
        if not ders:
            continue
        ops = q.get("options") or []
        dogru = next((o.get("text", "") for o in ops if o.get("isCorrect")), "")
        anah = norm(q["stem"])[:140] + "|" + norm(dogru)[:60]
        if anah in gor:  # aynı soru farklı yıl kaydı: ilk kayıt tutulur, yıllar birleşir
            next(x for x in out if x["anah"] == anah)["yillar"].append(str(q.get("examYear")))
            continue
        gor.add(anah)
        out.append(dict(id=q["id"], ders=ders, kok=q["stem"], dogru=dogru, yillar=[str(q.get("examYear"))], anah=anah,
                        isPastExam=bool(q.get("isPastExam"))))
    return out


def main() -> int:
    from lib import embed  # noqa: E402 — bge-m3 CPU servisi

    kayit = ders_kaydi()
    sayfalar = sorted(HAM.glob("*_s*.json"))
    if not sayfalar:
        sys.exit(f"ham okuma yok: {HAM}")
    birimler: dict[str, list[dict]] = defaultdict(list)
    yapistirilan: dict[str, list[dict]] = defaultdict(list)
    for f in sayfalar:
        d = json.loads(f.read_text())
        for b in d["bloklar"]:
            ders = b.get("ders") or "?"
            if ders not in kayit:
                continue
            duz = b.get("duzeltme") or []
            el = [dict(e, metin=duzelt(e.get("metin", ""), duz)) for e in b.get("el_yazisi") or []]
            kayitb = dict(id=b["id"], pdf=d["pdf"], sayfa=d["sayfa"], bolge=b.get("bolge"), tur=b["tur"],
                          baslik=b.get("baslik") or "", metin=duzelt(b.get("basili_metin") or "", duz), el_yazisi=el,
                          isaretler=b.get("isaretler") or [], sinyal=sorted(set(b.get("onem") or [])),
                          y25=b.get("y25"), y26=b.get("y26") or b.get("y26_ilgili"), duzeltme=duz, not_=b.get("not"))
            if b["tur"] == "cikmis_soru" and b.get("cikmis"):
                yapistirilan[ders].append(dict(kayitb, cikmis=b["cikmis"]))
            else:
                birimler[ders].append(kayitb)

    banka = banka_sorulari(kayit)
    # OCR/yazım varyantı aynı sorular (Distrofin/Distrofon…): aynı derste kosinüs ≥ 0.95 → tek kayıt, yıllar birleşir
    BV0 = embed([q["kok"] + " " + q["dogru"] for q in banka], model="bge-m3") if banka else []
    tekil, tv = [], []
    for q, v in zip(banka, BV0):
        es = next((j for j, (t, w) in enumerate(zip(tekil, tv)) if t["ders"] == q["ders"] and float(w @ v) >= 0.95), None)
        if es is None:
            tekil.append(q); tv.append(v)
        else:
            tekil[es]["yillar"] += q["yillar"]; tekil[es].setdefault("kopyalar", []).append(q["id"])
    banka = tekil
    # vektörler
    tum_birim = [(k, i, birim_metni(b)) for k, L in birimler.items() for i, b in enumerate(L)]
    V = embed([t for _, _, t in tum_birim], model="bge-m3")
    idx = {(k, i): n for n, (k, i, _) in enumerate(tum_birim)}

    def en_yakin(ders: str, vek) -> tuple[int, float]:
        L = birimler.get(ders) or []
        if not L:
            return -1, 0.0
        s = [(float(V[idx[(ders, i)]] @ vek), i) for i in range(len(L))]
        sk, i = max(s)
        return i, sk

    # 2) yapıştırılmış çıkmışlar → en yakın birim
    YV = embed([soru_metni(c["cikmis"]) for L in yapistirilan.values() for c in L], model="bge-m3") if yapistirilan else []
    n = 0
    for ders, L in yapistirilan.items():
        for c in L:
            i, sk = en_yakin(ders, YV[n]); n += 1
            c["bagli_birim"] = birimler[ders][i]["id"] if i >= 0 and sk >= ESIK_YAPISTIR else None
            c["benzerlik"] = round(sk, 3)
            if c["bagli_birim"]:
                b = birimler[ders][i]
                b.setdefault("ogrenci_sorulari", []).append(c["id"])
                b["sinyal"] = sorted(set(b["sinyal"]) | {"cikmis"})

    # 3) banka çıkmışları → birim
    yapistirilan_idler = {c["cikmis"].get("banka_id") for L in yapistirilan.values() for c in L if c["cikmis"].get("banka_id")}
    BV = tv
    banka_sonuc = []
    for q, v in zip(banka, BV):
        i, sk = en_yakin(q["ders"], v)
        eslesti = i >= 0 and sk >= ESIK_BANKA
        r = dict(id=q["id"], ders=q["ders"], yillar=q["yillar"], kok=q["kok"][:220], dogru=q["dogru"][:120],
                 kopyalar=q.get("kopyalar", []), birim=birimler[q["ders"]][i]["id"] if i >= 0 else None, benzerlik=round(sk, 3), kapsandi=eslesti,
                 notta_yapistirilmis=bool(({q["id"]} | set(q.get("kopyalar", []))) & yapistirilan_idler))
        banka_sonuc.append(r)
        if eslesti:
            b = birimler[q["ders"]][i]
            b.setdefault("banka_cikmis", []).append(q["id"])

    # 4) puan
    for ders, L in birimler.items():
        for b in L:
            p = sum(AGIRLIK.get(s, 0) for s in b["sinyal"] if s != "cikmis")
            if "cikmis" in b["sinyal"] or b.get("ogrenci_sorulari"):
                p += AGIRLIK["cikmis"]
            nb = len(b.get("banka_cikmis") or [])
            if nb:
                p += AGIRLIK["banka_cikmis"] + 5 * (nb - 1)
            if any(i.get("tur") == "yildiz" for i in b["isaretler"]) and "yildiz" not in b["sinyal"]:
                p += AGIRLIK["yildiz"]
            b["puan"] = min(100, p)
            b["oncelik"] = oncelik(b["puan"], bool(b.get("ogrenci_sorulari") or nb or "cikmis" in b["sinyal"]),
                                   bool(set(b["sinyal"]) & {"yildiz", "unlem", "el_sorarim", "el_cikmis"}))
            b["vurgulu"] = sorted({i.get("hedef", "").strip() for i in b["isaretler"]
                                   if i.get("hedef") and i.get("tur") in ("sari", "yesil", "pembe", "daire", "kirmizi_cizgi", "yildiz", "kutu")})

    CIKTI.mkdir(parents=True, exist_ok=True)
    indeks = []
    for ders in sorted(set(birimler) | set(yapistirilan)):
        L = sorted(birimler.get(ders, []), key=lambda b: (-b["puan"], b["pdf"], b["sayfa"]))
        bs = [r for r in banka_sonuc if r["ders"] == ders]
        y25_sayfa = sorted({(b["y25"] or {}).get("sayfa") for b in L if (b.get("y25") or {}).get("sayfa")})
        y25_key = next(((b["y25"] or {}).get("key") for b in L if (b.get("y25") or {}).get("key")), None)
        out = dict(ders=ders, kod=kayit[ders]["kod"], brans=kayit[ders]["brans"], konu=kayit[ders]["konu"],
                   kaynak="Geçmiş yıl (2025-26) öğrenci derleme notu: " + ", ".join(sorted({f"{b['pdf']}3.2" for b in L})),
                   y25=dict(key=y25_key, sayfalar=y25_sayfa),
                   sayac=dict(birim=len(L), A=sum(b["oncelik"] == "A" for b in L), B=sum(b["oncelik"] == "B" for b in L),
                              C=sum(b["oncelik"] == "C" for b in L), ogrenci_sorusu=len(yapistirilan.get(ders, [])),
                              banka=len(bs), banka_kapsandi=sum(r["kapsandi"] for r in bs)),
                   birimler=L, ogrenci_sorulari=yapistirilan.get(ders, []), banka=bs)
        (CIKTI / f"{ders}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
        indeks.append(dict(ders=ders, kod=out["kod"], brans=out["brans"], konu=out["konu"], **out["sayac"]))
    (CIKTI / "index.json").write_text(json.dumps(dict(surum=1, esik_banka=ESIK_BANKA, dersler=indeks), ensure_ascii=False, indent=1))
    for r in indeks:
        print(f"{r['ders']} {r['konu'][:34]:34} birim {r['birim']:3} A{r['A']:3} B{r['B']:3} C{r['C']:3}  "
              f"notta soru {r['ogrenci_sorusu']:2}  banka {r['banka_kapsandi']}/{r['banka']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
