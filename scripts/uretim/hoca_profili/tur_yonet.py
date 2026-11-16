#!/usr/bin/env python3
"""10 turluk kör ajan testi altyapısı. meds/.venv-ocr/bin/python ile çalışır.

  tur_yonet.py girdi  <tur> [--set gelistirme|bekletilmis]   → <SC>/tur<N>/girdi/<ders_id>/{not.md, adaylar.json, profil.md}
  tur_yonet.py puanla <tur> [--set ...]                      → ajan çıktılarını (<SC>/tur<N>/cikti/<ders_id>.json) 2026-27 ile puanlar

Ajan çıktısı biçimi (ders başına dosya): {"tahminler":[{"satir":<not.md satır no>,"olgu":"sorulabilecek bilgi, tam cümle","kalip":"...","bilgi_turu":"...","neden":"..."}]}
Puan: soru yakalandı = (a) tahmin satırı altın satırların ±1'inde VEYA (b) 'olgu' metni sorunun (kök+doğru şık) bge-m3 kosinüsü eşikten büyük.
Eşik: aynı tahminlerin BAŞKA derslerin sorularıyla kosinüsünün %97'lik dilimi (tur başına yeniden hesaplanır → şans düzeyi kontrolü).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algoritmalar import embed, hepsi, sira01  # noqa: E402
from sinama_ortak import SC, bekletilmis, gelistirme  # noqa: E402
from ortak import norm  # noqa: E402

PROFIL = SC / "profil_sizintisiz"


def adaylar(sig, dd, k, n=30, tur_filtre=False):
    """Aday satırlar: kararlı birleşim (ağırlıklar ayarlanabilir: sinama_agirlik.json)."""
    f = SC / "agirlik.json"
    ag = json.loads(f.read_text()) if f.exists() else dict(emb_ders=1, emb_konu=1, hedef=1, fmt=0.7, cue=0.5)
    s = sum(a * sira01(sig[k][ad]) for ad, a in ag.items())
    if tur_filtre:
        import re as _re
        for i, r in enumerate(dd["satirlar"]):
            if _re.search(r"çıkmış|soru \d+|öğrenim hedef", norm(r["baslik"])) or _re.match(r"(klinik & patofizyolojik|doğru cevap|soru / öncül)", norm(r["t"])) or r["no"] <= 6:
                s[i] = -9
    sira = np.argsort(-s)[:n]
    out = []
    for i in sira:
        r = dd["satirlar"][int(i)]
        ipucu = [ad for ad in ("hedef", "emb_konu", "emb_ders", "fmt", "cue") if sig[k][ad][int(i)] >= np.quantile(sig[k][ad], 0.85)]
        out.append(dict(satir=r["no"], metin=r["t"][:260], puan=round(float(s[int(i)]), 2), sinyal=ipucu))
    return out


def yapi_adaylari(dd, n_liste=5, n_ilac=6, n_kural=6):
    """Tur 2: genel puandan bağımsız yapısal aday sınıfları (olumsuz kök / ilaç-imza / kural sorularının hedefleri)."""
    import re as _re
    from satir_model import ILAC_EK
    sat = dd["satirlar"]
    bloklar, i = [], 0
    while i < len(sat):
        j = i
        while j + 1 < len(sat) and sat[j + 1]["depth"] == sat[i]["depth"] and sat[j + 1]["baslik"] == sat[i]["baslik"] and not sat[j + 1]["tablo"] == (not sat[i]["tablo"]):
            j += 1
        if j - i + 1 >= 4 and sat[i]["baslik"].strip() and sat[i]["no"] > 6 and not _re.search(r"çıkmış|soru \d+|spot|öğrenim|kaynak", norm(sat[i]["baslik"])):
            ort = sum(sat[x]["uzun"] for x in range(i, j + 1)) / (j - i + 1)
            if ort <= 16:
                bloklar.append((j - i + 1, i, j))
        i = j + 1
    bloklar.sort(reverse=True)
    liste = [dict(baslik=sat[a]["baslik"], satirlar=[sat[x]["no"] for x in range(a, b + 1)], uyeler=[sat[x]["t"][:90] for x in range(a, b + 1)][:14]) for _, a, b in bloklar[:n_liste]]
    ilac = [dict(satir=r["no"], metin=r["t"][:220]) for r in sat if ILAC_EK.search(norm(r["t"])) and _re.search(r"yan etki|toksik|kontrendike|endikasyon|kullanılır|izlem|doz|gebel|uyarı", norm(r["t"]))][:n_ilac]
    kural = [dict(satir=r["no"], metin=r["t"][:220]) for r in sat if _re.search(r"\bgerekir\b|verilmez|yapılmaz|önerilmez|kontrendike|\b\d+\s*(saat|gün|hafta|ay|yıl|mg|%)|eşik|en az|en fazla|yalnızca|asla|her zaman", norm(r["t"])) and not _re.search(r"çıkmış|soru \d+", norm(r["baslik"]))]
    kural = sorted(kural, key=lambda x: -len(x["metin"]))[:n_kural]
    yon_re = _re.compile(r"tedavi(?:de|si)? |ilk (?:seçenek|basamak|tercih)|seçilecek ilaç|tercih edilir|önerilir|aşı|profilaksi|izlem|takip|taranır|taramada|endike|kontrendike|empirik|perkütan|cerrahi|drenaj|antibiyotik|muayene|tetkik|tanıda|tanı için")
    yonetim = [dict(satir=r["no"], metin=r["t"][:220]) for r in sat if yon_re.search(norm(r["t"])) and not _re.search(r"çıkmış|soru \d+|öğrenim", norm(r["baslik"])) and 40 <= len(r["t"]) <= 400]
    yonetim = sorted(yonetim, key=lambda x: -len(x["metin"]))[:6]
    return dict(liste_bloklari=liste, ilac_satirlari=ilac, kural_esik_satirlari=kural, yonetim_satirlari=yonetim)


def adaylar_md(ad: dict) -> str:
    L = ["# Aday satırlar (not.md satır numarasıyla; ipucudur, kanıt değil)", "", "## A. Genel adaylar (algoritma sırası)"]
    L += [f"- s{c['satir']}: {c['metin'][:150]}" for c in ad["genel_adaylar"][:15]]
    L += ["", "## B. Liste/sınıf blokları (olumsuz kökün hedefi: tüm üyeleri bil)"]
    for b in ad.get("liste_bloklari", [])[:4]:
        L.append(f"- [{b['baslik'][:50]}] s{b['satirlar'][0]}–s{b['satirlar'][-1]}: " + "; ".join(u[:40] for u in b["uyeler"][:8]))
    L += ["", "## C. İlaç imza satırları"] + [f"- s{c['satir']}: {c['metin'][:140]}" for c in ad.get("ilac_satirlari", [])[:5]]
    L += ["", "## D. Kural/eşik/yapılmaz satırları"] + [f"- s{c['satir']}: {c['metin'][:140]}" for c in ad.get("kural_esik_satirlari", [])[:5]]
    if False:  # v7 denemesi: yarar kanıtlanmadı (TEST_TURLARI.md tur 10–11)
      L += ["", "## E. Klinik yönetim satırları (tedavi/aşı/izlem/tanı yaklaşımı; 'doğru yaklaşım' ve 'yanlıştır' kökleri)"] + [f"- s{c['satir']}: {c['metin'][:140]}" for c in ad.get("yonetim_satirlari", [])[:5]]
    return "\n".join(L)


def profil_md(dd, k, sig, Q, QE):
    from profil_oku import GUVEN_KURALI
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ortak
    ortak.CIKTI = PROFIL
    import profil_oku
    profil_oku.CIKTI = PROFIL
    u, harita = profil_oku.profil_yukle(dd["ders"])
    top = lambda d, kk=5: ", ".join(f"{x} %{round(v*100)}" for x, v in list(d.items())[:kk])
    L = [f"# Profil — {dd['ders']} / {dd['konu']}", f"Ders profili ({u['n_soru']} soru, güven {u['guven']}): kök kalıbı {top(u['kok_kalibi'])}; bilgi türü {top(u['bilgi_turu'])}; düzey {top(u['bilissel_duzey'])}; "
         f"çeldirici {top(u['celdirici_stratejisi'], 3)}."]
    # konu-bazlı yerel profil: dersin satır ortalamasına en yakın 40 geçmiş soru (konu adı eşleşmesinden bağımsız, hoca-agnostik)
    E = np.mean([1], axis=0)
    from algoritmalar import ders_gom
    c = ders_gom(dd).mean(0)
    idx = [j for j, q in enumerate(Q) if q["ders"] == dd["ders"]] or list(range(len(Q)))
    sc = QE[idx] @ c
    yak = [idx[j] for j in np.argsort(-sc)[:40]]
    from collections import Counter
    tur, kalip, duzey = Counter(Q[j]["tur"] for j in yak), Counter(Q[j]["kalip"] for j in yak), Counter(Q[j]["duzey"] for j in yak)
    n = len(yak)
    L += ["", f"## Bu konuya en yakın {n} geçmiş çıkmış (konu-bazlı yerel profil; farklı hocalar/yıllar karışabilir)",
          f"- Bilgi türü: {', '.join(f'{a} %{round(b/n*100)}' for a, b in tur.most_common(4))}",
          f"- Kök kalıbı: {', '.join(f'{a} %{round(b/n*100)}' for a, b in kalip.most_common(4))}",
          f"- Düzey: {', '.join(f'{a} %{round(b/n*100)}' for a, b in duzey.most_common(3))}", "", "### Yakın çıkmış örnekleri (kök → doğru şık)"]
    for j in yak[:10]:
        q = Q[j]
        L.append(f"- [{q['kalip']}/{q['tur']}/{sorted(q['yil_set'])[-1:] or '?'}] {q['kok'][:170]} → **{q['siklar'][q['dogru_i']][:90]}**")
    # tekrar eden çekirdek kavramlar (yakın sorular içinde)
    import uslup_analiz
    cek = uslup_analiz.ortak_cekirdek([Q[j] for j in yak])
    if cek:
        L += ["", "### Bu konuda tekrar eden çekirdek kavramlar (≥2 kez çıkmış)"]
        L += [f"- {c_['kavram']} ({c_['kez']}×, yıllar {c_['yillar']}, kalıplar {c_['kaliplar']})" for c_ in cek[:8]]
    return "\n".join(L)


def hedef_k(dd) -> int:
    """Tahmin sayısı: ders uzunluğuyla orantılı (10–18)."""
    return max(10, min(18, round(len(dd["satirlar"]) / 10)))


def girdi(tur: int, kume: str):
    ders, sig = hepsi()
    sec = gelistirme(ders) if kume == "gelistirme" else bekletilmis(ders)
    from algoritmalar import gecmis_gom
    Q, QE = gecmis_gom()
    kok = SC / f"tur{tur}"
    for k, dd in sec.items():
        d = kok / "girdi" / k
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(dd["yol"], d / "not.md")
        ad = dict(genel_adaylar=adaylar(sig, dd, k, n=20, tur_filtre=tur >= 3))
        if tur >= 2:
            ad.update(yapi_adaylari(dd))
        (d / "adaylar.json").write_text(json.dumps(ad if tur >= 2 else ad["genel_adaylar"], ensure_ascii=False, indent=1))
        if tur >= 3:
            (d / "adaylar.md").write_text(adaylar_md(ad))
        (d / "profil.md").write_text((f"**Bu ders için tam {hedef_k(dd)} tahmin yaz.**\n\n" if tur >= 4 else "") + profil_md(dd, k, sig, Q, QE))
        (kok / "cikti").mkdir(exist_ok=True)
    print(len(sec), "ders girdisi:", kok / "girdi")
    json.dump(sorted(sec), open(kok / "dersler.json", "w"))


def puanla(tur: int, kume: str):
    ders, sig = hepsi()
    sec = gelistirme(ders) if kume == "gelistirme" else bekletilmis(ders)
    kok = SC / f"tur{tur}"
    tahmin, ders_q = {}, {}
    for k in sec:
        f = kok / "cikti" / f"{k}.json"
        if f.exists():
            try:
                tahmin[k] = json.loads(f.read_text())["tahminler"]
            except Exception as e:  # bozuk çıktı = o ders yakalanamadı
                print("BOZUK", k, e)
    tum = [(k, i, t["olgu"]) for k, tl in tahmin.items() for i, t in enumerate(tl)]
    q_all = [(k, q) for k, dd in ders.items() for q in dd["sorular"]]
    TE = embed([t for _, _, t in tum]) if tum else np.zeros((0, 1024))
    QEv = embed([q["kok"] + " " + q["dogru"] for _, q in q_all])
    # eşik: tahminin başka dersin sorularıyla kosinüsü %97
    kos = []
    for a, (k, i, _) in enumerate(tum):
        for b, (kq, q) in enumerate(q_all):
            if kq != k:
                kos.append(float(TE[a] @ QEv[b]))
    esik = float(np.quantile(kos, 0.97)) if kos else 0.7
    res = dict(n_ders=len(sec), cevaplanan=len(tahmin), esik=round(esik, 3), soru=0, satir_isabet=0, anlam_isabet=0, ikisi=0, hic=[])
    ders_rapor = {}
    for k in sec:
        tl = tahmin.get(k, [])
        for q in ders[k]["sorular"]:
            if not q["altin"]:
                continue
            res["soru"] += 1
            sat = any(abs(t["satir"] - ders[k]["satirlar"][a]["no"]) <= 1 for t in tl for a in q["altin"] if isinstance(t.get("satir"), int))
            qi = [b for b, (kq, qq) in enumerate(q_all) if qq is q][0]
            an = max([float(TE[a] @ QEv[qi]) for a, (kk, i, _) in enumerate(tum) if kk == k] or [0])
            anlam = an >= esik
            res["satir_isabet"] += sat; res["anlam_isabet"] += anlam; res["ikisi"] += (sat or anlam)
            ders_rapor.setdefault(k, []).append(dict(kok=q["kok"][:90], dogru=q["dogru"][:60], satir=sat, anlam=round(an, 2), yakalandi=bool(sat or anlam), kalip=None))
            if not (sat or anlam):
                res["hic"].append(dict(ders=k, kok=q["kok"][:110], dogru=q["dogru"][:70]))
    n = max(1, res["soru"])
    ozet = dict(tur=tur, kume=kume, soru=res["soru"], satir_isabeti=round(res["satir_isabet"] / n, 3), anlam_isabeti=round(res["anlam_isabet"] / n, 3),
                yakalama=round(res["ikisi"] / n, 3), esik=res["esik"], cevaplanan_ders=f"{len(tahmin)}/{len(sec)}",
                tahmin_basina_ders=round(len(tum) / max(1, len(tahmin)), 1))
    (kok / f"sonuc_{kume}.json").write_text(json.dumps(dict(ozet=ozet, ders=ders_rapor, kacan=res["hic"]), ensure_ascii=False, indent=1))
    print(json.dumps(ozet, ensure_ascii=False))
    return ozet


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["girdi", "puanla"])
    ap.add_argument("tur", type=int)
    ap.add_argument("--set", default="gelistirme", choices=["gelistirme", "bekletilmis"])
    a = ap.parse_args()
    (girdi if a.komut == "girdi" else puanla)(a.tur, a.set)
