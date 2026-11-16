#!/usr/bin/env python3
"""Ders başına hoca-üslup profili + konu başına kazanım haritası + geriye dönük sınama (LLM yok).

  python3 scripts/uretim/hoca_profili/uslup_analiz.py            # profilleri ve docs/HOCA_USLUBU/*.md üretir
  python3 scripts/uretim/hoca_profili/uslup_analiz.py --sinama   # yalnız geriye dönük sınama (üslup kayması + kavram tekrarı)

Çıktı: src/data/hoca_profilleri/<ders>/uslup.json, kazanim_haritasi.json, docs/HOCA_USLUBU/<ders>.md, _genel/uslup.json, _sinama.json
Algoritmalar: (1) kök kalıbı sınıflayıcı, (2) bilgi-türü sınıflayıcı ("neden sorulur"), (3) Bloom-türevi bilişsel düzey,
(4) şık/çeldirici ölçümü (NBME/Haladyna kusur ve strateji listeleri), (5) tekrar kümeleme (Jaccard, yıllar arası aynı kavram),
(6) dönem kayması (2023+ ↔ öncesi), (7) kaynak bağımlılığı (özet kanıtı benzerliği).
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import CIKTI, DOC, KOK, bilgi_turu, bilissel_duzey, celdirici_stratejisi, jetonlar, kok_kalibi, norm, sik_ozellik, slug, soru_yukle  # noqa: E402

DERS_ESLE = {"Patoloji": "Tıbbi Patoloji", "Farmakoloji": "Tıbbi Farmakoloji", "Anesteziyoloji ve Reanimasyon": "Anestezi ve Reanimasyon"}

NEDEN = {  # bilgi türü → hocanın o bilgiyi neden sorduğu (bilişsel/tıbbi gerekçe) + nasıl kurduğu
    "mekanizma": ("Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.",
                  "Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır."),
    "tani_ayirici": ("Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.",
                     "Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır."),
    "tanimlayici_bulgu": ("Patolojik/klinik imza bulgusu tanıyı koydurur; hastalığa özgü tek bulgu ödüllendirilir.",
                          "Bulgudan hastalığa ya da hastalıktan bulguya (ters yön); çeldirici komşu hastalığın bulgusudur."),
    "ilac_yan_etki": ("Hasta güvenliği: yan etki/kontrendikasyon bilmemek zarar demektir.", "İlaçtan yan etkiye ve yan etkiden ilaca; çeldirici aynı sınıfın başka üyesidir."),
    "ilac_endikasyon": ("Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.", "Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır."),
    "etiyoloji_risk": ("Neden ve risk faktörü önleme/tanıyı yönlendirir.", "En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir."),
    "siniflama_ad": ("Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.", "Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir."),
    "epidemiyoloji_sayi": ("Pre-test olasılık: sıklık ve yaş/cinsiyet dağılımı klinik şüpheyi belirler.", "Tek sayı ya da oran sorulur; çeldirici yakın değerlerdir."),
    "onleme_halk_sagligi": ("Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.", "Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir."),
    "prognoz_komplikasyon": ("Seyir ve komplikasyon izlem ve tedavi kararını belirler.", "Komplikasyon ya da prognoz belirleyicisi sorulur; çeldirici başka hastalığın komplikasyonudur."),
    "tanim_kavram": ("Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.", "Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir."),
}
DUZEY_ZORLUK = {"L1_hatirlama": "kolay-orta", "L2_anlama_iliski": "orta-zor", "L3_uygulama": "zor"}


def pay(c: Counter, n: int, nd=3) -> dict:
    return {k: round(v / n, nd) for k, v in c.most_common()} if n else {}


def yuzde_fark(a: dict, b: dict) -> float:
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b)) / 2


def jsd(p: dict, q: dict) -> float:
    ks = set(p) | set(q)
    m = {k: 0.5 * (p.get(k, 0) + q.get(k, 0)) for k in ks}
    def kl(a):
        return sum(a[k] * math.log2(a[k] / m[k]) for k in ks if a.get(k, 0) > 0)
    return 0.5 * kl({k: p.get(k, 0) for k in ks}) + 0.5 * kl({k: q.get(k, 0) for k in ks})


def yeni_2627() -> list[dict]:
    d = json.loads((KOK / "data/cikmis_2627/kurul1_2627.json").read_text())
    out = []
    for q in d["sorular"]:
        if q.get("durum") != "tam" or "ABCDE".find(q.get("cevap") or "") < 0:
            continue
        sik = q["siklar"]
        i = "ABCDE".index(q["cevap"])
        if len(sik) < 4 or i >= len(sik):
            continue
        kalip = kok_kalibi(q["kok"])
        tur = bilgi_turu(q["kok"], sik[i])
        sf = sik_ozellik(sik, i)
        out.append(dict(id="2627-" + str(q["sinav_no"]), ders=DERS_ESLE.get(q["ders"], q["ders"]), konu=q["konu"], kok=q["kok"], siklar=sik,
                        dogru_i=i, kalip=kalip, tur=tur, duzey=bilissel_duzey(kalip, tur, q["kok"]), sf=sf, strateji=celdirici_stratejisi(sf),
                        yillar=[2026], yil_set=[2026], kez=1, kurul=1, ozet={}, kok_kelime=len(q["kok"].split())))
    return out


def tum_sorular(yeni_dahil=True) -> list[dict]:
    Q = soru_yukle()
    for q in Q:
        q["ders"] = DERS_ESLE.get(q["ders"], q["ders"])
    return Q + (yeni_2627() if yeni_dahil else [])


def guven(n: int) -> str:
    return "yuksek" if n >= 120 else "orta" if n >= 40 else "dusuk"


def uslup(Q: list[dict], genel: dict | None = None) -> dict:
    n = len(Q)
    sf = [q["sf"] for q in Q]
    kw = sorted(q["kok_kelime"] for q in Q)
    konum = Counter("ABCDE"[q["dogru_i"]] for q in Q if q["dogru_i"] < 5)
    strat = Counter(s for q in Q for s in q["strateji"])
    eski = [q for q in Q if q["yil_set"] and max(q["yil_set"]) < 2023]
    yeni = [q for q in Q if q["yil_set"] and max(q["yil_set"]) >= 2023]
    kayma = {}
    if len(eski) >= 25 and len(yeni) >= 25:
        for alan in ("kalip", "duzey", "tur"):
            pe, py = pay(Counter(q[alan] for q in eski), len(eski)), pay(Counter(q[alan] for q in yeni), len(yeni))
            fark = {k: round(py.get(k, 0) - pe.get(k, 0), 3) for k in set(pe) | set(py) if abs(py.get(k, 0) - pe.get(k, 0)) >= 0.08}
            if fark:
                kayma[alan] = fark
    kez2 = sum(1 for q in Q if q["kez"] >= 2) / n
    yilli = [len(q["yil_set"]) for q in Q if q["yil_set"]]
    o = dict(
        n_soru=n, guven=guven(n), yillar=dict(sorted(Counter(y for q in Q for y in q["yil_set"]).items())),
        kok_kalibi=pay(Counter(q["kalip"] for q in Q), n), bilgi_turu=pay(Counter(q["tur"] for q in Q), n),
        bilissel_duzey=pay(Counter(q["duzey"] for q in Q), n),
        kok_kelime=dict(ort=round(statistics.mean(kw), 1), p25=kw[n // 4], medyan=kw[n // 2], p75=kw[3 * n // 4]),
        sik=dict(kelime_ort=round(statistics.mean(f["kelime_ort"] for f in sf), 1), kelime_cv=round(statistics.mean(f["kelime_cv"] for f in sf), 2),
                 dogru_en_uzun_orani=round(sum(f["dogru_en_uzun"] for f in sf) / n, 3), bilesik_sik_orani=round(statistics.mean(f["bilesik"] for f in sf), 3),
                 sayisal_sik_orani=round(sum(1 for f in sf if f["sayisal"] >= 0.8) / n, 3),
                 hepsi_hicbiri_orani=round(sum(f["hepsi_hicbiri"] for f in sf) / n, 3),
                 mutlak_ifade_celdirici_orani=round(sum(1 for f in sf if f["mutlak_celdirici"]) / n, 3),
                 dogru_sik_konumu=pay(konum, sum(konum.values())), celdirici_ortusme=round(statistics.mean(f["celdirici_ortusme"] for f in sf), 3)),
        celdirici_stratejisi=pay(strat, n), tekrar=dict(birden_cok_kez_cikan_soru_orani=round(kez2, 3),
                                                        ort_farkli_yil=round(statistics.mean(yilli), 2) if yilli else 0),
        donem_kaymasi_2023_sonrasi=kayma,
    )
    return o


def ortak_cekirdek(Q: list[dict]) -> list[dict]:
    """Tekrar kümeleme: aynı dersin sorularını doğru-şık+kök jetonu Jaccard'ıyla kümeler → çekirdek kavramlar."""
    js = [set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]])) for q in Q]
    kume: list[list[int]] = []
    for i in range(len(Q)):
        for k in kume:
            j0 = js[k[0]]
            if js[i] and j0 and len(js[i] & j0) / len(js[i] | j0) >= 0.5:
                k.append(i)
                break
        else:
            kume.append([i])
    out = []
    for k in kume:
        yil = sorted({y for i in k for y in Q[i]["yil_set"]})
        kez = sum(Q[i]["kez"] for i in k)
        if kez >= 2:
            q0 = max((Q[i] for i in k), key=lambda q: len(q["yil_set"]))
            out.append(dict(kavram=q0["siklar"][q0["dogru_i"]][:90], ornek_kok=q0["kok"][:200], kez=kez, farkli_kok=len(k), yillar=yil,
                            kaliplar=sorted({Q[i]["kalip"] for i in k}), tur=Counter(Q[i]["tur"] for i in k).most_common(1)[0][0]))
    out.sort(key=lambda x: (-x["kez"], -len(x["yillar"])))
    return out


def konu_haritasi(Q: list[dict]) -> list[dict]:
    by = defaultdict(list)
    for q in Q:
        by[norm(q["konu"])].append(q)
    out = []
    for konu, qs in by.items():
        if len(qs) < 3:
            continue
        n = len(qs)
        tur = Counter(q["tur"] for q in qs)
        kalip = Counter(q["kalip"] for q in qs)
        duzey = Counter(q["duzey"] for q in qs)
        ana_tur = [t for t, _ in tur.most_common(3)]
        cek = ortak_cekirdek(qs)
        yil = sorted({y for q in qs for y in q["yil_set"]})
        oz = [q["ozet"].get("benzerlik", 0) for q in qs if q["ozet"]]
        out.append(dict(
            konu=qs[0]["konu"], n_soru=n, yillar=yil, guven=guven(n),
            neden_sorulur=[dict(bilgi_turu=t, pay=round(tur[t] / n, 2), gerekce=NEDEN[t][0]) for t in ana_tur if tur[t] / n >= 0.15 or t == ana_tur[0]],
            nasil_sorulur=dict(kok_kalibi=pay(kalip, n), bilissel_duzey=pay(duzey, n), kurulus=NEDEN[ana_tur[0]][1]),
            hangi_bilgilerle=dict(celdirici=pay(Counter(s for q in qs for s in q["strateji"]), n), sik_kelime_ort=round(statistics.mean(q["sf"]["kelime_ort"] for q in qs), 1)),
            zorluk=DUZEY_ZORLUK[duzey.most_common(1)[0][0]] + (", tekrar eden" if cek else ""),
            kaynaga_bagimlilik=dict(ozet_kanitli_oran=round(len(oz) / n, 2), ort_benzerlik=round(statistics.mean(oz), 2) if oz else None),
            cekirdek_kavramlar=cek[:8], tekrar_eden_kavram_sayisi=len(cek),
            tipik_kok_ornekleri=[q["kok"][:180] for q in sorted(qs, key=lambda q: -q["kez"])[:3]],
        ))
    out.sort(key=lambda x: -x["n_soru"])
    return out


def md_yaz(ders: str, u: dict, harita: list[dict], genel: dict) -> str:
    L = [f"# {ders} — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)", "",
         f"> {u['n_soru']} tekil çıkmış soru · güven: **{u['guven']}** · yıllar: {u['yillar']}", "",
         "## 1. Üslup özeti", ""]
    def sat(ad, d, g):
        return "\n".join(f"- **{k}**: %{round(v*100)} (genel ortalama %{round(g.get(k,0)*100)})" for k, v in list(d.items())[:7])
    L += ["### Kök kalıbı", sat("", u["kok_kalibi"], genel["kok_kalibi"]), "", "### Sorulan bilgi türü (neden sorulur)", sat("", u["bilgi_turu"], genel["bilgi_turu"]), "",
          "### Bilişsel düzey", sat("", u["bilissel_duzey"], genel["bilissel_duzey"]), ""]
    k = u["kok_kelime"]; s = u["sik"]
    L += ["### Biçim", f"- Kök uzunluğu: ort. {k['ort']} kelime (p25 {k['p25']} · medyan {k['medyan']} · p75 {k['p75']}).",
          f"- Şık: ort. {s['kelime_ort']} kelime; bileşik şık %{round(s['bilesik_sik_orani']*100)}; sayısal şık %{round(s['sayisal_sik_orani']*100)}; mutlak ifadeli çeldirici %{round(s['mutlak_ifade_celdirici_orani']*100)}.",
          f"- Doğru şık tek başına en uzun: %{round(s['dogru_en_uzun_orani']*100)} (genel %{round(genel['sik']['dogru_en_uzun_orani']*100)}). Doğru şık konumu: {s['dogru_sik_konumu']}.",
          f"- Çeldirici stratejisi: {u['celdirici_stratejisi']}", f"- Aynı bilginin yeniden sorulması: soruların %{round(u['tekrar']['birden_cok_kez_cikan_soru_orani']*100)}'i birden çok kez çıkmış.", ""]
    if u["donem_kaymasi_2023_sonrasi"]:
        L += ["### Dönem kayması (2023 sonrası − öncesi, puan farkı)", f"- {u['donem_kaymasi_2023_sonrasi']}", ""]
    L += ["## 2. Yazım kuralları (bu dersin soruları için)", ""]
    kp = list(u["kok_kalibi"].items())[:3]
    L += [f"- Kök kalıbı payları çıkmışa ±10 puan: {', '.join(f'{a} %{round(b*100)}' for a, b in kp)}.",
          f"- Kök {max(5, k['p25'])}–{k['p75']} kelime; şık ort. {s['kelime_ort']} kelime, uzunluklar birbirine yakın (CV≈{s['kelime_cv']}).",
          "- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.",
          f"- Bilişsel düzey hedefi: {', '.join(f'{a} %{round(b*100)}' for a, b in u['bilissel_duzey'].items())}.", ""]
    L += ["## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)", ""]
    for h in harita[:25]:
        nd = h["neden_sorulur"][0]
        L += [f"### {h['konu']} — {h['n_soru']} soru, yıllar {h['yillar']}, güven {h['guven']}",
              f"- **Neden:** {nd['bilgi_turu']} (%{round(nd['pay']*100)}) — {nd['gerekce']}",
              f"- **Nasıl:** {h['nasil_sorulur']['kok_kalibi']} · düzey {h['nasil_sorulur']['bilissel_duzey']} · {h['nasil_sorulur']['kurulus']}",
              f"- **Zorluk:** {h['zorluk']} · **kaynağa bağımlılık:** özet kanıtlı %{round(h['kaynaga_bagimlilik']['ozet_kanitli_oran']*100)}"]
        if h["cekirdek_kavramlar"]:
            L.append("- **Tekrar eden çekirdek kavramlar:** " + "; ".join(f"{c['kavram']} ({c['kez']}×, {len(c['yillar'])} yıl)" for c in h["cekirdek_kavramlar"][:4]))
        L.append("")
    return "\n".join(L)


def sinama(Q: list[dict], yeni: list[dict]) -> dict:
    """(1) Üslup kayması: eski yıllardan çıkan ders profili, 2026-27'yi genel profilden daha iyi öngörüyor mu (JSD, küçük=iyi)?
    (2) Kavram tekrarı: 2025-26/2026-27 sorularının kaç %'si eski bir çıkmışla aynı kavram (Jaccard≥.5, aynı ders)?"""
    eski = [q for q in Q if q["yil_set"] and max(q["yil_set"]) < 2026 and q["id"][:4] != "2627"]
    gen_e = {a: pay(Counter(q[a] for q in eski), len(eski)) for a in ("kalip", "duzey", "tur")}
    r = dict(ders={}, ozet={})
    for ders in sorted({q["ders"] for q in yeni}):
        y = [q for q in yeni if q["ders"] == ders]
        e = [q for q in eski if q["ders"] == ders]
        if len(y) < 6 or len(e) < 30:
            continue
        d_ders, d_gen = [], []
        for a in ("kalip", "duzey", "tur"):
            py = pay(Counter(q[a] for q in y), len(y))
            d_ders.append(jsd(pay(Counter(q[a] for q in e), len(e)), py))
            d_gen.append(jsd(gen_e[a], py))
        ej = [set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]])) for q in e]
        hit = 0
        for q in y:
            s = set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]]))
            if s and any(x and len(s & x) / len(s | x) >= 0.5 for x in ej):
                hit += 1
        # taban çizgisi: aynı soru, başka dersin eski soruları
        diger = [set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]])) for q in eski if q["ders"] != ders][:len(e)]
        hit0 = sum(1 for q in y if (lambda s: s and any(x and len(s & x) / len(s | x) >= 0.5 for x in diger))(set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]]))))
        r["ders"][ders] = dict(n_yeni=len(y), n_eski=len(e), jsd_ders_profili=round(sum(d_ders) / 3, 4), jsd_genel_profil=round(sum(d_gen) / 3, 4),
                               ders_profili_daha_iyi=sum(d_ders) < sum(d_gen), eski_cikmisla_ayni_kavram=round(hit / len(y), 3), tabanda_ayni_kavram=round(hit0 / len(y), 3))
    v = list(r["ders"].values())
    if v:
        r["ozet"] = dict(ders_sayisi=len(v), ders_profili_daha_iyi=sum(x["ders_profili_daha_iyi"] for x in v),
                         ort_ayni_kavram=round(statistics.mean(x["eski_cikmisla_ayni_kavram"] for x in v), 3),
                         ort_taban=round(statistics.mean(x["tabanda_ayni_kavram"] for x in v), 3))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sinama", action="store_true")
    ap.add_argument("--yeni-haric", action="store_true", help="2026-27 sorularını profile KATMA (sızıntısız sınama için)")
    ap.add_argument("--cikti", type=Path, help="çıktı kökü (varsayılan src/data/hoca_profilleri)")
    a = ap.parse_args()
    global CIKTI, DOC
    if a.cikti:
        CIKTI = a.cikti
        DOC = a.cikti / "_doc"
    Q = tum_sorular(not a.yeni_haric)
    yeni = [q for q in Q if q["id"].startswith("2627-")]
    if a.sinama:
        print(json.dumps(sinama(Q, yeni), ensure_ascii=False, indent=1))
        return 0
    genel = uslup(Q)
    CIKTI.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    (CIKTI / "_genel").mkdir(exist_ok=True)
    (CIKTI / "_genel/uslup.json").write_text(json.dumps(genel, ensure_ascii=False, indent=1))
    sin = sinama(Q, yeni)
    (CIKTI / "_sinama.json").write_text(json.dumps(sin, ensure_ascii=False, indent=1))
    indeks = []
    for ders in sorted({q["ders"] for q in Q}):
        qs = [q for q in Q if q["ders"] == ders]
        if len(qs) < 8:
            continue
        u = uslup(qs, genel)
        h = konu_haritasi(qs)
        d = CIKTI / slug(ders)
        d.mkdir(exist_ok=True)
        (d / "uslup.json").write_text(json.dumps(dict(ders=ders, **u), ensure_ascii=False, indent=1))
        (d / "kazanim_haritasi.json").write_text(json.dumps(dict(ders=ders, konular=h), ensure_ascii=False, indent=1))
        (DOC / f"{slug(ders)}.md").write_text(md_yaz(ders, u, h, genel))
        indeks.append(dict(ders=ders, slug=slug(ders), n_soru=u["n_soru"], guven=u["guven"], konu_sayisi=len(h)))
        print(f"{ders}: {u['n_soru']} soru, {len(h)} konu haritası, güven {u['guven']}")
    (CIKTI / "index.json").write_text(json.dumps(indeks, ensure_ascii=False, indent=1))
    print(json.dumps(sin["ozet"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
