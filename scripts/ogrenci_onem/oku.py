#!/usr/bin/env python3
"""Tam içerik işçisinin okuyacağı öğrenci önem özeti (LLM yok).

  python3 scripts/ogrenci_onem/oku.py --ders k2-19                                # kısa özet (≤ 45 satır)
  python3 scripts/ogrenci_onem/oku.py --ders k2-19 --sayfalar <klasör>/sayfalar.json --yaz <klasör>/ogrenci_onem.json
        # 2026-27 PDF'i geldiyse: her A/B birimini bu yılın sayfasına eşler (bge-m3), eşleşmeyeni "bu yıl slaytta yok" işaretler

Kaynak: src/data/ogrenci_onem/<ders>.json (birimler) + data/ogrenci_onem/analiz/<ders>.json (temalar, tuzaklar, düzeltmeler)
+ src/data/ogrenci_onem/basari.json (dersin isabet ölçümü). Kullanım kuralları: docs/OGRENCI_ONEM_YONTEMI.md §5.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import CIKTI, KOK, bilgiler, oku_json  # noqa: E402

ESIK_SAYFA = 0.55
KURAL = [
    "A birimi: anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → karıştırılan komşu kavram), önem listesinde madde "
    "(`ogrenci: {oncelik: A}`), ≥2 örnek soru (farklı kalıp), ara soru adayı. B: anlatımda açık + ≥1 örnek soru. C: kapsamda kalır.",
    "Vurgu cümlesi yalnız kanıtla: 'çıkmış sınavda soruldu' yalnız doğrulanmış çıkmışta; öğrenci notu için 'geçen yılın öğrencileri "
    "bu bilgiyi en önemli yerler arasına aldı' türü cümle en çok derste 2 kez, yalnız A biriminde.",
    "2026-27 slaytında karşılığı olmayan birim anlatıma eklenmez (kaynak sadakati); çıkmış kanıtlıysa önem listesine 'geçen yıl "
    "sorulmuştu' notuyla ve örnek soruya girebilir. Notun 'duzeltmeler' listesindeki yanlışlar KULLANILMAZ.",
    "Kapı: python3 scripts/ogrenci_onem/kapi.py <ders> [--sayfalar …] → 0 HATA (A birimi eksik bilgisi listelenir; yalnız o bilgi eklenir).",
]


def sayfa_esle(birimler: list[dict], sayfalar: dict) -> dict[str, tuple[str, float]]:
    sys.path.insert(0, str(KOK / "scripts/agents"))
    from lib import embed  # noqa: E402
    sn = [k for k, v in sayfalar.items() if len((v or "").strip()) > 20]
    if not sn:
        return {}
    SV = embed([sayfalar[k][:1500] for k in sn], model="bge-m3")
    metin = [f"{b['baslik']}. {b['metin'][:900]}" for b in birimler]
    UV = embed(metin, model="bge-m3")
    out = {}
    for b, u in zip(birimler, UV):
        s = SV @ u; j = int(s.argmax())
        out[b["id"]] = (sn[j], round(float(s[j]), 3))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders", required=True)
    ap.add_argument("--sayfalar"); ap.add_argument("--yaz"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d = oku_json(CIKTI / f"{a.ders}.json")
    if not d:
        print(f"{a.ders}: öğrenci önem notu yok (bu ders 2025-26 öğrenci derlemesinde geçmiyor). Önem listesi yalnız çıkmış + hoca + profil ile kurulur.")
        return 0
    an = oku_json(KOK / f"data/ogrenci_onem/analiz/{a.ders}.json", {}) or {}
    bs = (oku_json(CIKTI / "basari.json", {}) or {}).get("ders", {}).get(a.ders)
    AB = [b for b in d["birimler"] if b["oncelik"] in ("A", "B")]
    es = sayfa_esle(AB, json.loads(Path(a.sayfalar).read_text())) if a.sayfalar else {}
    kayit = []
    for b in AB:
        bl = bilgiler(b, d)
        s = es.get(b["id"])
        kayit.append(dict(id=b["id"], oncelik=b["oncelik"], puan=b["puan"], baslik=b["baslik"], sinyal=b["sinyal"],
                          y25=b.get("y25"), y26=dict(sayfa=s[0], benzerlik=s[1], var=s[1] >= ESIK_SAYFA) if s else b.get("y26"),
                          bilgiler=[x["metin"] for x in bl][:8], cikmis=(b.get("ogrenci_sorulari") or []) + (b.get("banka_cikmis") or [])))
    ozet = dict(ders=a.ders, konu=d["konu"], kaynak=d["kaynak"], sayac=d["sayac"], basari=bs, analiz=an, birimler=kayit, kurallar=KURAL)
    if a.yaz:
        Path(a.yaz).write_text(json.dumps(ozet, ensure_ascii=False, indent=1))
    if a.json:
        print(json.dumps(ozet, ensure_ascii=False, indent=1)); return 0
    print(f"# Öğrenci önem özeti · {a.ders} {d['konu']}  (belge: docs/OGRENCI_ONEM/{a.ders}.md)")
    print(f"Kaynak: {d['kaynak']} · A {d['sayac']['A']} · B {d['sayac']['B']} · C {d['sayac']['C']} · notta çıkmış {d['sayac']['ogrenci_sorusu']}")
    if bs:
        print(f"İsabet (geçmiş çıkmışlar): tam %{round(100 * (bs.get('isabet_tam') or 0))}, geniş %{round(100 * (bs.get('isabet_genis') or 0))} "
              f"({bs.get('n')} soru; bilgisi slaytta olanlarda tam %{round(100 * ((bs.get('slaytta') or {}).get('isabet_tam') or 0))}) — "
              "isabet düşükse not tek başına yetmez, çıkmış + hoca profili ağırlığı artar.")
    if an.get("ozet"):
        print("Özet:", an["ozet"])
    for t in (an.get("temalar") or [])[:10]:
        print(f"- [{t.get('oncelik')}] %{t.get('soru_payi', 0)} {t.get('tema')} — {t.get('anlatim', '')[:160]}")
    print("A/B birimleri (en önemli bilgiler):")
    for k in kayit[:14]:
        y = k["y26"]
        yer = f" · 2026-27 s.{y['sayfa']}" + ("" if y.get("var", True) else " (BU YIL SLAYTTA YOK?)") if isinstance(y, dict) and y.get("sayfa") else ""
        print(f"  {k['oncelik']} {k['puan']:3} {k['baslik'][:60]}{yer}: " + " | ".join(x[:70] for x in k["bilgiler"][:3]))
    if an.get("tuzaklar"):
        print("Tuzaklar:", "; ".join(t.get("tuzak", "") for t in an["tuzaklar"][:6]))
    if an.get("duzeltmeler"):
        print("KULLANMA (notta yanlış):", "; ".join(f"{x.get('yanlis', '')} → {x.get('dogru', '')}" for x in an["duzeltmeler"][:6]))
    for r in KURAL:
        print("Kural:", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
