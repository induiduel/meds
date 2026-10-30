#!/usr/bin/env python3
"""Öğrenci önem verisinden ders başına okunur belge üretir (LLM yok): docs/OGRENCI_ONEM/<ders>.md + README.md.

  python3 scripts/ogrenci_onem/belge.py            # tüm dersler
  python3 scripts/ogrenci_onem/belge.py --ders k2-19

Belgeler ÜRETİLİR; elle düzenlenmez. Düzeltme kaynağı: ham okuma (data/ogrenci_onem/ham), analiz
(data/ogrenci_onem/analiz/<ders>.json) ya da betikler; sonra birlestir.py → basari.py --hesapla → belge.py.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import CIKTI, DOC, KOK, bilgiler, cikmis_cevap, oku_json  # noqa: E402

PDF_AD = {"psk": "psk3.2 (Psikiyatri)", "noro": "nöro3.2 (Nöroloji)", "tbg": "tbg3.2 (Tıbbi Genetik)", "ftr": "ftr3.2 (FTR)"}
SINYAL_AD = {"cikmis": "çıkmış", "sari": "sarı vurgu", "yesil": "yeşil vurgu", "pembe": "pembe vurgu", "yildiz": "yıldız",
             "unlem": "ünlem", "daire": "daire", "kirmizi_cizgi": "kırmızı alt çizgi", "kutu": "kutu", "tekrar": "tekrar",
             "el_onemli": "el notu", "el_cikmis": "el: çıkmış", "el_sorarim": "el: sorarım"}


def yuzde(x) -> str:
    return "—" if x is None else f"%{round(100 * x)}"


def sayfa_yeri(b: dict) -> str:
    y25, y26 = b.get("y25") or {}, b.get("y26") or {}
    p = [f"2025-26 s.{y25['sayfa']}" if y25.get("sayfa") else "", f"2026-27 s.{y26['sayfa']}" if isinstance(y26, dict) and y26.get("sayfa") else ""]
    return f"{PDF_AD.get(b['pdf'], b['pdf'])} sayfa {b['sayfa']}" + (" · " + " · ".join(x for x in p if x) if any(p) else "")


def soru_blogu(c: dict, numara: str) -> list[str]:
    k = c.get("cikmis") or {}
    out = [f"**{numara}** {k.get('kok', '').strip()}"]
    out += [f"- {s}" for s in k.get("siklar") or []]
    ek = []
    if k.get("ogrenci_cevap"):
        ek.append(f"öğrencinin cevabı: {k['ogrenci_cevap']}")
    if k.get("banka_id"):
        ek.append(f"bankada `{k['banka_id']}` ({k.get('banka_yil') or '?'}), doğru: {cikmis_cevap(k) or '?'}")
    else:
        ek.append("bankada bulunamadı")
    if k.get("tutarli") is False:
        ek.append("⚠ öğrenci cevabı/şık metni bankayla ya da tıbbi doğruyla UYUŞMUYOR")
    out.append(f"  - {' · '.join(ek)}" + (f" — {k['not']}" if k.get("not") else ""))
    return out


def ders_belgesi(d: dict, an: dict, bs: dict | None, kacan: list[dict]) -> str:
    L = [f"# {d['ders']} {d['konu']} — geçmiş yıl öğrenci önem notu",
         "",
         f"> {d['brans']} · ders kodu {d['kod']} · {d['kaynak']}. Belge `scripts/ogrenci_onem/belge.py` ile üretilir, elle düzenlenmez.",
         "> Amaç: tam içerik işçisi bu dersi yazarken neyi ne kadar vurgulayacağını, nerede ayrıntıya gireceğini ve örnek soruları",
         "> nereye yığacağını bilsin. Kullanım kuralları: `docs/OGRENCI_ONEM_YONTEMI.md` §5. Kısa özet: `python3 scripts/ogrenci_onem/oku.py --ders "
         + d["ders"] + "`.",
         "",
         "## 1. Özet ve isabet", ""]
    if an.get("ozet"):
        L += [an["ozet"], ""]
    s = d["sayac"]
    L += [f"- Birim: {s['birim']} (A {s['A']} · B {s['B']} · C {s['C']}); notta yapıştırılmış çıkmış: {s['ogrenci_sorusu']}; "
          f"bankadaki Kurul 2 çıkmışı: {s['banka']}.",
          f"- 2025-26 slaytından notta yer alan sayfalar: {', '.join(map(str, d['y25']['sayfalar'])) or '—'} (`{d['y25']['key']}`)."]
    if bs:
        L += [f"- **İsabet** (yargıçla ölçüldü, {bs['n']} çıkmış; bilgisi slayt metninde olan {bs['slaytta']['n']}): tam {yuzde(bs['isabet_tam'])}, geniş {yuzde(bs['isabet_genis'])}; "
              f"notta yapıştırılmamış {bs['yapistirilmamis_n']} soruda tam {yuzde(bs['yapistirilmamis_tam'])}, geniş {yuzde(bs['yapistirilmamis_genis'])}; "
              f"seçicilik {yuzde(bs['secicilik'])}" + (f", kaldıraç ×{bs['kaldirac']}" if bs.get("kaldirac") else "") + "."]
    L.append("")
    if an.get("temalar"):
        L += ["## 2. Öncelik haritası (anlatım ayrıntısı + örnek soru payı)", "",
              "| Öncelik | Tema | Soru payı | Kanıt | Nasıl anlatılmalı |", "|---|---|---|---|---|"]
        for t in an["temalar"]:
            L.append(f"| {t.get('oncelik', '')} | {t.get('tema', '')} | %{t.get('soru_payi', 0)} | {t.get('kanit', '')} | {t.get('anlatim', '')} |".replace("\n", " "))
        L.append("")
        tip = [(t["tema"], t.get("soru_tipleri") or []) for t in an["temalar"] if t.get("soru_tipleri")]
        if tip:
            L += ["Soru tipleri:", ""] + [f"- **{a}:** " + "; ".join(b) for a, b in tip] + [""]
    ogr = {c["id"]: c for c in d.get("ogrenci_sorulari") or []}
    bk = {r["id"]: r for r in d.get("banka") or []}
    for k, ad in (("A", "A birimleri — çıkmış kanıtlı, en ayrıntılı anlatılacak yerler"), ("B", "B birimleri — vurgulu ve el notlu yerler")):
        bl = [b for b in d["birimler"] if b["oncelik"] == k]
        if not bl:
            continue
        L += [f"## {3 if k == 'A' else 4}. {ad}", ""]
        for b in bl:
            sig = ", ".join(SINYAL_AD.get(x, x) for x in b["sinyal"])
            L += [f"### {b['baslik']}  ·  puan {b['puan']}", "", f"`{b['id']}` · {sayfa_yeri(b)} · işaret: {sig or '—'}", ""]
            if b.get("metin"):
                L += ["Slayt:", "", *[f"> {x}" for x in b["metin"].splitlines() if x.strip()][:18], ""]
            if b.get("vurgulu"):
                L += ["Öğrencinin işaretlediği: " + " · ".join(f"**{v}**" for v in b["vurgulu"][:8]), ""]
            el = [e for e in b.get("el_yazisi") or [] if e.get("metin")]
            if el:
                L += ["El notları (düzeltilmiş okuma):", ""]
                for e in el[:14]:
                    g = "" if e.get("guven") in (None, "yuksek") else f" _(okuma güveni: {e['guven']})_"
                    L.append(f"- {e.get('hedef', '')[:70] + ' → ' if e.get('hedef') else ''}{e['metin']}{g}")
                L.append("")
            ck = []
            for cid in b.get("ogrenci_sorulari") or []:
                c = (ogr.get(cid) or {}).get("cikmis") or {}
                ck.append(f"- Notta çıkmış: {c.get('kok', '')[:150]} → {cikmis_cevap(c) or '?'}")
            for qid in b.get("banka_cikmis") or []:
                r = bk.get(qid) or {}
                ck.append(f"- Bankada çıkmış ({', '.join(r.get('yillar') or [])}): {r.get('kok', '')[:150]} → {r.get('dogru', '')}")
            if ck:
                L += ["Çıkmış bağı:", "", *ck, ""]
            for x in b.get("duzeltme") or []:
                if x.get("gerekce"):
                    L.append(f"- ⚠ Düzeltme: «{x.get('ham', '')}» → «{x.get('dogru', '')}» — {x['gerekce']}")
            L.append("")
    cl = [b for b in d["birimler"] if b["oncelik"] == "C"]
    if cl:
        L += ["## 5. C birimleri — notta seçilmiş, az işaretli (kapsamda kalsın)", ""]
        L += [f"- {b['baslik']} ({sayfa_yeri(b)})" + (": " + " | ".join(x["metin"][:70] for x in bilgiler(b, d)[:2]) if bilgiler(b, d) else "") for b in cl]
        L.append("")
    if d.get("ogrenci_sorulari"):
        L += ["## 6. Notta yapıştırılmış çıkmış sorular", ""]
        for i, c in enumerate(d["ogrenci_sorulari"], 1):
            L += soru_blogu(c, f"S{i}.") + [""]
    if kacan:
        L += ["## 7. Notta olmayan ama sorulmuş çıkmışlar (öğrencinin kaçırdığı yer — bunlar da anlatılmalı)", ""]
        for r in kacan:
            L.append(f"- ({', '.join(r.get('yillar') or [])}) {r.get('kok', '')[:200]} → **{r.get('dogru', '')}**" + (f" — {r['gerekce']}" if r.get("gerekce") else ""))
        L.append("")
    if an.get("tuzaklar") or an.get("sayilar") or an.get("hoca_kaliplari"):
        L += ["## 8. Hoca kalıpları, tuzaklar, sayılar", ""]
        L += [f"- Kalıp: {x}" for x in an.get("hoca_kaliplari") or []]
        L += [f"- Tuzak: {t.get('tuzak', '')} — {t.get('neden', '')}" for t in an.get("tuzaklar") or []]
        L += [f"- Sayı: {x}" for x in an.get("sayilar") or []]
        L.append("")
    if an.get("duzeltmeler"):
        L += ["## 9. Notta yanlış olanlar — KULLANMA", "", "| Notta / slaytta | Doğrusu | Dayanak |", "|---|---|---|"]
        L += [f"| {x.get('yanlis', '')} | {x.get('dogru', '')} | {x.get('kaynak', '')} |".replace("\n", " ") for x in an["duzeltmeler"]]
        L.append("")
    L += ["## 10. İşçiye talimat", "",
          "- A birimleri anlatımda ayrıntılı yer alır (tanım → ayırt edici nokta → sayı/ölçüt → karıştırılan komşu kavram); önem listesinde "
          "`ogrenci: {oncelik: \"A\"}` etiketli madde; en az 2 örnek soru (farklı kalıp); hoca ara sorusu adayı.",
          "- B birimleri anlatımda açıkça geçer, en az 1 örnek soru. C birimleri kapsamda kalır.",
          "- Örnek soru dağılımı §2'deki soru payına ±10 puan uyar; §7'deki kaçan çıkmışların bilgisi de soruya çevrilir.",
          "- Bu yılın (2026-27) slaytında karşılığı olmayan birim anlatıma girmez; çıkmış kanıtlıysa önem listesine ve örnek soruya girebilir.",
          "- §9'daki yanlışlar kullanılmaz; okuma güveni düşük el notu tek başına dayanak olmaz.",
          f"- Kapı: `python3 scripts/ogrenci_onem/kapi.py {d['ders']}` → 0 HATA."]
    if an.get("ara_soru_adaylari"):
        L += ["", "Ara soru adayları:", ""] + [f"- `{x.get('birim', '')}`: {x.get('fikir', '')}" for x in an["ara_soru_adaylari"]]
    if an.get("kurul2627_notu"):
        L += ["", f"2026-27 notu: {an['kurul2627_notu']}"]
    return "\n".join(L).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders")
    a = ap.parse_args()
    DOC.mkdir(parents=True, exist_ok=True)
    idx = json.loads((CIKTI / "index.json").read_text())
    bs = oku_json(CIKTI / "basari.json", {}) or {}
    yargi = {}
    for f in sorted((KOK / "data/ogrenci_onem/yargi").glob("yargi_*.json")):
        for y in json.loads(f.read_text()):
            yargi[y["id"]] = y
    satir = []
    for r in idx["dersler"]:
        if a.ders and r["ders"] != a.ders:
            continue
        d = json.loads((CIKTI / f"{r['ders']}.json").read_text())
        an = oku_json(KOK / f"data/ogrenci_onem/analiz/{r['ders']}.json", {}) or {}
        if yargi:
            kacan = [dict(q, gerekce=yargi[q["id"]].get("gerekce") + ("" if yargi[q["id"]].get("slaytta", True) else " (yargıç: bilgisi 2025-26 slayt metninde de yok)"))
                     for q in d.get("banka") or [] if q["id"] in yargi and yargi[q["id"]]["karar"] == "yok"]
        else:
            kacan = [q for q in d.get("banka") or [] if not q.get("kapsandi") and not q.get("notta_yapistirilmis")]
        (DOC / f"{r['ders']}.md").write_text(ders_belgesi(d, an, (bs.get("ders") or {}).get(r["ders"]), kacan))
        satir.append((r, (bs.get("ders") or {}).get(r["ders"])))
    if not a.ders:
        g = bs.get("genel") or {}
        L = ["# Geçmiş yıl öğrenci önem notları — Kurul 2 (2025-26 derlemesi)", "",
             "Dört öğrenci derleme PDF'i (psk3.2, nöro3.2, tbg3.2, ftr3.2; 39 A3 sayfa) sayfa görüntüsünden iki geçişle okundu; her blok "
             "2025-26 slaytına, el yazısı ilgili satıra, yapıştırılmış çıkmışlar bankaya eşlendi. Yöntem, isabet ölçümü ve işçi kuralları: "
             "`docs/OGRENCI_ONEM_YONTEMI.md`. Veri: `src/data/ogrenci_onem/`.", ""]
        son = bs.get("son_sinav_2025_26") or {}
        if g:
            sl = g["slaytta"]
            L += ["**İsabet (yargıçla ölçüldü, `docs/OGRENCI_ONEM_YONTEMI.md` §4):**", "",
                  f"- Bilgisi 2025-26 slaytında olan {sl['n']} çıkmışta tam isabet {yuzde(sl['isabet_tam'])}, geniş (tam + kısmi) {yuzde(sl['isabet_genis'])}; "
                  f"notta yapıştırılmamış {sl['yapistirilmamis_n']} soruda tam {yuzde(sl['yapistirilmamis_tam'])}. Not slayt sayfalarının ortalama "
                  f"{yuzde(g['secicilik'])} kadarını içeriyor → rastgele sayfa seçimine göre ×{g['kaldirac_slaytta']} isabet.",
                  f"- En yeni sınav 2025-26 ({son.get('n', 0)} soru, yalnız {son.get('yapistirilan', 0)} tanesi notta yapıştırılmış): tam {yuzde(son.get('isabet_tam'))}, "
                  f"geniş {yuzde(son.get('isabet_genis'))}.",
                  f"- Tüm {g['n']} çıkmış (slayt dışı ve başka ders etiketli sorular dahil): tam {yuzde(g['isabet_tam'])}, geniş {yuzde(g['isabet_genis'])}.", ""]
        L += ["| Ders | Konu | A | B | C | Notta çıkmış | Banka | İsabet tam | Yapıştırılmamış tam | Seçicilik |", "|---|---|---|---|---|---|---|---|---|---|"]
        for r, b in satir:
            b = b or {}
            L.append(f"| [{r['ders']}]({r['ders']}.md) | {r['konu']} | {r['A']} | {r['B']} | {r['C']} | {r['ogrenci_sorusu']} | {r['banka']} | "
                     f"{yuzde(b.get('isabet_tam'))} | {yuzde(b.get('yapistirilmamis_tam'))} | {yuzde(b.get('secicilik'))} |")
        (DOC / "README.md").write_text("\n".join(L) + "\n")
    print(f"{len(satir)} belge → {DOC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
