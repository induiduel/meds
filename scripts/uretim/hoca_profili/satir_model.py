#!/usr/bin/env python3
"""Satır önem modeli: ders metninin hangi satırı sorulur? (LLM yok; saf Python lojistik regresyon + geriye dönük sınama)

  python3 scripts/uretim/hoca_profili/satir_model.py --cv        # 5 katlı dosya-bazlı sınama + temel çizgilerle kıyas
  python3 scripts/uretim/hoca_profili/satir_model.py --egit      # tüm veriyle eğit → src/data/hoca_profilleri/_model/satir_model.json
  python3 scripts/uretim/hoca_profili/satir_model.py --holdout   # 2026-27 Kurul 1 sınavı (modele hiç girmedi) üzerinde sınama

Sinyal aileleri (her biri ayrı temel çizgi olarak ölçülür, tam model hepsini birleştirir):
  BICIM      : madde derinliği, kalın/==vurgu==, tablo hücresi, sayı/yüzde, parantez, eponim, uzunluk, başlık altı ilk satır
  ISARET     : sınav-kuran söz kalıpları (en sık, tanı koydurucu, kontrendike, ancak/aksine, tanım, sınıflama …)
  TEKRAR     : satırdaki kavramların geçmiş sorularda (bu ders içinde) ne kadar sorulduğu (log-oran) ve ≥2 farklı yılda çıkmış kavramlar
  YAPI       : dosya içindeki bağıl konum, bölüm başlığı türü
Sızıntı önlemi: TEKRAR istatistiği, değerlendirilen dosyanın kat'ındaki soruları HİÇ görmeden hesaplanır (iç içe kat).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import CIKTI, KOK, jetonlar, norm, slug, soru_yukle  # noqa: E402

OZET = KOK.parent / "meds_temp/cikmis_check_solve/kaynak/ozetler"
NOTLAR_K1 = KOK.parent / "meds_database_v2/ders_notlari_k1"
MODEL = CIKTI / "_model/satir_model.json"

ISARET = {
    "en_sik": r"\ben (sık|önemli|yaygın|olası|tipik|karakteristik|belirgin|etkili)|\bsıklıkla|en çok",
    "tani_koydurucu": r"patognomonik|tanı koydurucu|altın standart|hallmark|pathognomonic|tanısal",
    "ilk_secim": r"ilk (basamak|seçenek|tercih|olarak)|tedavi(de)? seçilen|ilk seçilecek",
    "kontrendike": r"kontrendike|yan etki|advers|toksik|teratojen|dikkat|uyarı",
    "karsit": r"\bancak\b|\bfakat\b|aksine|oysa|farklı olarak|buna karşın|\bhariç\b|dışında|istisna",
    "tanim": r"\bdenir\b|olarak tanımlan|tanımı|anlamına gelir|olarak adlandırıl|tanımlanır",
    "siniflama": r"sınıflama|sınıflan|tip\s?[ivx0-9]|evre|grade|derece|alt tip|ikiye ayrıl|üçe ayrıl",
    "neden_sonuc": r"nedeniyle|sonucu|yol açar|neden olur|sonucunda|bağlı olarak|dolayı",
    "karsilastirma": r"karşılaştır|ayırıcı tanı|ayırt|farkı|aksine|\bvs\b",
    "klinik": r"klinik|bulgu|belirti|semptom|şikayet|muayene|görülür",
    "tedavi": r"tedavi|ilaç|doz|uygulan|kullanılır|endikasyon",
    "tablo_satiri": r"^\s*\|",
}
ISARET_RX = {k: re.compile(v) for k, v in ISARET.items()}
ILAC_EK = re.compile(r"\b\w+(mab|nib|pril|sartan|olol|dipin|statin|azol|misin|sillin|sefa\w+|floksasin|vir|kain|barbital|zepam|tidin|prazol|ksaban|parin)\b")


def temizle(s: str) -> str:
    s = re.sub(r"^\s*([-*•]|\d+[.)])\s+", "", s)
    s = re.sub(r"\*\*|==|__|`|<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip(" :|")


def dosya_satirlari(yol: Path) -> list[dict]:
    """Satır kaydı: ham, metin, derinlik, tablo mu, başlık altı ilk mi, bağıl konum, başlık türü."""
    ham = yol.read_text(errors="ignore").splitlines()
    out, baslik, ilk = [], "", True
    gov = [i for i, s in enumerate(ham) if s.strip() and not re.match(r"^\s*(\|?[-: |]+\|?)\s*$", s)]
    n = max(1, len(gov))
    for sira, i in enumerate(gov):
        s = ham[i]
        if re.match(r"^\s*#{1,6}\s", s):
            baslik, ilk = temizle(re.sub(r"^\s*#+\s*", "", s)), True
            continue
        m = re.match(r"^(\s*)", s)
        depth = len(m.group(1).replace("\t", "  ")) // 2
        t = temizle(s)
        if len(t.split()) < 3:
            continue
        out.append(dict(no=i + 1, ham=s, t=t, depth=depth, tablo=s.lstrip().startswith("|"), ilk=ilk, pos=sira / n, baslik=baslik,
                        kalin="**" in s, vurgu="==" in s, uzun=len(t.split())))
        ilk = False
    return out


def statik(r: dict) -> list[float]:
    t, tl = r["t"], norm(r["t"])
    eponim = len(re.findall(r"(?<=[a-zçğıöşü,;] )[A-ZÇĞİÖŞÜ][a-zçğıöşü]{3,}", t))
    f = [
        math.log1p(r["uzun"]), min(r["depth"], 4) / 4, float(r["tablo"]), float(r["ilk"]), float(r["kalin"]), float(r["vurgu"]),
        float(bool(re.search(r"\d", t))), float(bool(re.search(r"%|yüzde|oran", tl))), float("(" in t),
        min(eponim, 3) / 3, float(bool(ILAC_EK.search(tl))), float(t.endswith(":")), r["pos"],
        float(bool(re.search(r"öğrenim hedef|kaynak|kaynakça|özet|giriş", norm(r["baslik"])))),
    ]
    f += [float(bool(rx.search(tl) if k != "tablo_satiri" else r["tablo"])) for k, rx in ISARET_RX.items()]
    return f


STATIK_AD = ["log_uzunluk", "derinlik", "tablo", "baslik_alti_ilk", "kalin", "vurgu_==", "sayi", "yuzde_oran", "parantez", "eponim",
             "ilac_eki", "iki_nokta_sonlu", "bagil_konum", "giris_kaynak_bolumu"] + list(ISARET)
BICIM_IDX = list(range(0, 14))
ISARET_IDX = list(range(14, len(STATIK_AD)))


class Istatistik:
    """TEKRAR sinyali: jeton → (soruda geçme, metinde geçme) log-oranı; ders içi."""

    def __init__(self, sorular: list[dict], satir_df: Counter, n_satir: int):
        self.qc = Counter()
        self.yil2 = Counter()
        for q in sorular:
            js = set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]]))
            for j in js:
                self.qc[j] += 1
                if len(q["yil_set"]) >= 2 or q["kez"] >= 2:
                    self.yil2[j] += 1
        self.nq = max(1, len(sorular))
        self.df, self.nd = satir_df, max(1, n_satir)

    def w(self, j: str) -> float:
        return max(-2.0, min(4.0, math.log((self.qc[j] + 0.3) / self.nq) - math.log((self.df[j] + 1) / self.nd) - 0.5 * 0))

    def tekrar(self, t: str) -> list[float]:
        js = list(dict.fromkeys(jetonlar(t)))
        if not js:
            return [0.0, 0.0, 0.0, 0.0]
        ws = sorted((self.w(j) for j in js), reverse=True)
        top3 = sum(ws[:3]) / min(3, len(ws))
        sorulan = sum(1 for j in js if self.qc[j] >= 1) / len(js)
        yil2 = sum(1 for j in js if self.yil2[j] >= 1) / len(js)
        return [top3, ws[0], sorulan, yil2]


TEKRAR_AD = ["tekrar_ust3", "tekrar_max", "sorulmus_kavram_orani", "cok_yil_kavram_orani"]


# --------------------------------------------------------------- veri
def oz_dosyalari() -> dict[tuple[str, str], Path]:
    d = {}
    for p in OZET.glob("k*/*/*.md"):
        d[(p.parts[-3], slug(re.sub(r"\.md$", "", p.name)))] = p
    return d


def kurul_veri():
    Q = soru_yukle()
    idx = oz_dosyalari()
    dos: dict[Path, list[dict]] = {}
    sorular: list[dict] = []
    eslesen = 0
    for q in Q:
        oz = q["ozet"]
        if not oz or not oz.get("metin"):
            continue
        k = re.search(r"sum-(k\d)-", oz.get("ozetId", ""))
        p = idx.get((k.group(1) if k else "", slug(re.sub(r"^\d+\s*", "", oz.get("ozetBaslik", "")))))
        if not p:
            p = idx.get((k.group(1) if k else "", slug(oz.get("ozetBaslik", ""))))
        if not p:
            continue
        if p not in dos:
            dos[p] = dosya_satirlari(p)
        satirlar = dos[p]
        hedef = {temizle(x) for x in oz["metin"].splitlines() if len(temizle(x).split()) >= 3}
        pos = [i for i, r in enumerate(satirlar) if r["t"] in hedef]
        if not pos:
            continue
        # etiket keskinleştirme: kaynak aralığından soruyla en çok örtüşen satır(lar) pozitif (tüm aralık değil)
        qj = set(jetonlar(q["kok"] + " " + q["siklar"][q["dogru_i"]]))
        ov = {i: len(qj & set(jetonlar(satirlar[i]["t"]))) / math.sqrt(max(1, len(qj)) * max(1, len(set(jetonlar(satirlar[i]["t"]))))) for i in pos}
        en = max(ov.values())
        if en < 0.2:
            continue
        pos = [i for i, o in ov.items() if o >= en * 0.9]
        eslesen += 1
        q2 = dict(q, dosya=p, pos=pos)
        sorular.append(q2)
    return sorular, dos, eslesen, len(Q)


def lr_egit(X, y, w, ep=25, lr=0.15, l2=1e-3, seed=1):
    d = len(X[0])
    mu = [sum(r[j] for r in X) / len(X) for j in range(d)]
    sd = [max(1e-6, (sum((r[j] - mu[j]) ** 2 for r in X) / len(X)) ** 0.5) for j in range(d)]
    Z = [[(r[j] - mu[j]) / sd[j] for j in range(d)] for r in X]
    wt, b = [0.0] * d, 0.0
    rnd = random.Random(seed)
    idx = list(range(len(Z)))
    for e in range(ep):
        rnd.shuffle(idx)
        a = lr / (1 + 0.15 * e)
        for i in idx:
            z = b + sum(wt[j] * Z[i][j] for j in range(d))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            g = (p - y[i]) * w[i]
            for j in range(d):
                wt[j] -= a * (g * Z[i][j] + l2 * wt[j])
            b -= a * g
    return dict(mu=mu, sd=sd, w=wt, b=b)


def lr_skor(m, x):
    return m["b"] + sum(m["w"][j] * (x[j] - m["mu"][j]) / m["sd"][j] for j in range(len(x)))


def satir_df(dosyalar: dict[Path, list[dict]]):
    df, n = Counter(), 0
    for sat in dosyalar.values():
        for r in sat:
            n += 1
            for j in set(jetonlar(r["t"])):
                df[j] += 1
    return df, n


def ozellikler(satirlar, st: Istatistik):
    return [statik(r) + st.tekrar(r["t"]) for r in satirlar]


def rank_yuzdelik(skor: list[float], pos: list[int], en_iyi: bool = False) -> float:
    """1 - AUC (düşük iyi; rastgele 0.5): kaynak satırların, kaynak olmayan satırlardan düşük puan alma oranı.
    en_iyi=True (tek kaynak satırı belli olduğunda): en iyi pozitifin üstündeki satır oranı."""
    ps = set(pos)
    if en_iyi:
        en = max(skor[i] for i in pos)
        return sum(1 for s in skor if s > en) / max(1, len(skor) - 1)
    pv = [skor[i] for i in pos]
    nv = [s for i, s in enumerate(skor) if i not in ps]
    if not nv:
        return 0.5
    nv.sort()
    from bisect import bisect_left, bisect_right
    kaz = sum(bisect_left(nv, v) + 0.5 * (bisect_right(nv, v) - bisect_left(nv, v)) for v in pv)
    return 1 - kaz / (len(pv) * len(nv))


def sira_ort(*listeler, agirlik=None):
    """Sıra-ortalaması birleşimi: her bileşen dosya içinde 0..1 sıra yüzdesine çevrilip ağırlıklı ortalanır."""
    agirlik = agirlik or [1.0] * len(listeler)
    n = len(listeler[0])
    out = [0.0] * n
    for l, a in zip(listeler, agirlik):
        sirali = sorted(range(n), key=lambda i: l[i])
        for r, i in enumerate(sirali):
            out[i] += a * r / max(1, n - 1)
    return out


def ozet_metrik(yuz: list[float]) -> dict:
    n = len(yuz)
    return dict(n=n, ort_yuzdelik=round(sum(yuz) / n, 3), ilk10=round(sum(y <= .10 for y in yuz) / n, 3), auc=round(1 - sum(yuz) / n, 3),
                ilk20=round(sum(y <= .20 for y in yuz) / n, 3), ilk33=round(sum(y <= .33 for y in yuz) / n, 3))


def cv(K=5, seed=7):
    sorular, dos, es, toplam = kurul_veri()
    print(f"çıkmış {toplam} · özet satırına bağlanan {es} soru · {len(dos)} özet dosyası", file=sys.stderr)
    df, nd = satir_df(dos)
    dosyalar = sorted(dos, key=str)
    rnd = random.Random(seed)
    rnd.shuffle(dosyalar)
    kat = {p: i % K for i, p in enumerate(dosyalar)}
    sets = {f: [q for q in sorular if kat[q["dosya"]] == f] for f in range(K)}
    # kat çiftleri için istatistik
    def st_dis(dis: set[int]):
        return Istatistik([q for f, qs in sets.items() if f not in dis for q in qs], df, nd)
    sonuc = defaultdict(list)
    ad_tum = STATIK_AD + TEKRAR_AD
    for f in range(K):
        # eğitim satırları: g≠f, özellikler {f,g} dışı istatistikle
        X, y, w = [], [], []
        for g in range(K):
            if g == f:
                continue
            st = st_dis({f, g})
            gdos = [p for p in dosyalar if kat[p] == g]
            qpos = defaultdict(set)
            for q in sets[g]:
                qpos[q["dosya"]].update(q["pos"])
            for p in gdos:
                feats = ozellikler(dos[p], st)
                for i, fv in enumerate(feats):
                    pos = i in qpos.get(p, ())
                    if not pos and rnd.random() > 0.2:
                        continue
                    X.append(fv); y.append(1 if pos else 0); w.append(1.0 if pos else 5.0)
        m_tam = lr_egit(X, y, w)
        m_bicim = lr_egit([[r[j] for j in BICIM_IDX + ISARET_IDX] for r in X], y, w)
        m_rec = lr_egit([[r[j] for j in range(len(STATIK_AD), len(ad_tum))] for r in X], y, w)
        st_t = st_dis({f})
        for q in sets[f]:
            sat = dos[q["dosya"]]
            if len(sat) < 25:
                continue
            fe = ozellikler(sat, st_t)
            sk = {"tam": [lr_skor(m_tam, x) for x in fe],
                  "bicim+isaret": [lr_skor(m_bicim, [x[j] for j in BICIM_IDX + ISARET_IDX]) for x in fe],
                  "yalniz_tekrar": [lr_skor(m_rec, x[len(STATIK_AD):]) for x in fe],
                  "rastgele": [rnd.random() for _ in fe]}
            sk["birlesik_sira"] = sira_ort(sk["bicim+isaret"], sk["yalniz_tekrar"])
            for ad, s in sk.items():
                sonuc[ad].append(rank_yuzdelik(s, q["pos"], en_iyi=True))
            sonuc["_ders"].append(q["ders"])
            sonuc["_tam"].append(rank_yuzdelik(sk["tam"], q["pos"], en_iyi=True))
    cikti = {ad: ozet_metrik(v) for ad, v in sonuc.items() if not ad.startswith("_")}
    ders_yuz = defaultdict(list)
    for d, y in zip(sonuc["_ders"], sonuc["_tam"]):
        ders_yuz[d].append(y)
    cikti["ders_bazli_tam"] = {d: ozet_metrik(v) for d, v in sorted(ders_yuz.items(), key=lambda x: -len(x[1])) if len(v) >= 15}
    return cikti


def egit():
    sorular, dos, es, toplam = kurul_veri()
    df, nd = satir_df(dos)
    K = 5
    dosyalar = sorted(dos, key=str)
    random.Random(3).shuffle(dosyalar)
    kat = {p: i % K for i, p in enumerate(dosyalar)}
    X, y, w = [], [], []
    rnd = random.Random(5)
    for g in range(K):  # eğitim özelliklerinde sızıntı yok: kat g satırları g dışı istatistikle
        st = Istatistik([q for q in sorular if kat[q["dosya"]] != g], df, nd)
        qpos = defaultdict(set)
        for q in sorular:
            if kat[q["dosya"]] == g:
                qpos[q["dosya"]].update(q["pos"])
        for p in dosyalar:
            if kat[p] != g:
                continue
            for i, fv in enumerate(ozellikler(dos[p], st)):
                pos = i in qpos.get(p, ())
                if not pos and rnd.random() > 0.2:
                    continue
                X.append(fv); y.append(1 if pos else 0); w.append(1.0 if pos else 5.0)
    m = lr_egit(X, y, w, ep=35)
    m_b = lr_egit([[r[j] for j in BICIM_IDX + ISARET_IDX] for r in X], y, w, ep=35)
    m_t = lr_egit([[r[j] for j in range(len(STATIK_AD), len(STATIK_AD) + len(TEKRAR_AD))] for r in X], y, w, ep=35)
    st = Istatistik(sorular, df, nd)
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    cikti = dict(ozellik_adlari=STATIK_AD + TEKRAR_AD, model=m, model_bicim=m_b, model_tekrar=m_t, soru_sayisi=len(sorular), dosya_sayisi=len(dos),
                 tekrar_istatistigi=dict(nq=st.nq, nd=st.nd, qc={k: v for k, v in st.qc.items() if v >= 1},
                                         yil2={k: v for k, v in st.yil2.items() if v >= 1},
                                         df={k: v for k, v in df.items() if st.qc.get(k, 0) >= 1 or v >= 5}))
    MODEL.write_text(json.dumps(cikti, ensure_ascii=False))
    agirlik = sorted(zip(cikti["ozellik_adlari"], m["w"]), key=lambda x: -abs(x[1]))
    print("en etkili özellikler (standartlaşmış ağırlık):")
    for a, v in agirlik[:14]:
        print(f"  {v:+.2f}  {a}")
    return 0


def modeli_yukle():
    d = json.loads(MODEL.read_text())
    st = Istatistik([], Counter(d["tekrar_istatistigi"]["df"]), d["tekrar_istatistigi"]["nd"])
    st.qc, st.yil2, st.nq = Counter(d["tekrar_istatistigi"]["qc"]), Counter(d["tekrar_istatistigi"]["yil2"]), d["tekrar_istatistigi"]["nq"]
    return d, st


def skorla_dosya(yol: Path):
    d, st = modeli_yukle()
    sat = dosya_satirlari(yol)
    fe = ozellikler(sat, st)
    nS = len(STATIK_AD)
    b = [lr_skor(d["model_bicim"], [x[j] for j in BICIM_IDX + ISARET_IDX]) for x in fe]
    t = [lr_skor(d["model_tekrar"], x[nS:]) for x in fe]
    return sat, sira_ort(b, t), b, t, fe


def holdout():
    d = json.loads((KOK / "data/cikmis_2627/kurul1_2627.json").read_text())
    idx = json.loads((NOTLAR_K1 / "index.json").read_text())
    dosya = {x["id"]: NOTLAR_K1 / x["dosya"] for x in idx}
    cache, yuz, ayr = {}, [], defaultdict(list)
    for q in d["sorular"]:
        if q.get("durum") != "tam" or q.get("ders_notu_id") not in dosya:
            continue
        sik = q["siklar"]
        dogru = sik["ABCDE".index(q["cevap"])] if q.get("cevap") in list("ABCDE") and len(sik) > "ABCDE".index(q["cevap"]) else ""
        p = dosya[q["ders_notu_id"]]
        if p not in cache:
            cache[p] = skorla_dosya(p)
        sat, sk = cache[p][0], cache[p][1]
        if len(sat) < 25:
            continue
        qj = set(jetonlar(q["kok"] + " " + dogru))
        if len(qj) < 2:
            continue
        ov = []
        for r in sat:
            rj = set(jetonlar(r["t"]))
            ov.append(len(qj & rj) / math.sqrt(len(qj) * max(1, len(rj))))
        en = max(ov)
        if en < 0.28:
            continue
        pos = [i for i, o in enumerate(ov) if o >= en * 0.92]
        y = rank_yuzdelik(sk, pos, en_iyi=True)
        yuz.append(y)
        ayr[q["ders"]].append(y)
    print("2026-27 K1 holdout (model bu sınavı hiç görmedi; kaynak satır jeton-eşlemesiyle bulundu):")
    print(" ", ozet_metrik(yuz), "(rastgele beklenti: ilk10=0.10 ilk20=0.20 ilk33=0.33 ort=0.50)")
    for k, v in ayr.items():
        if len(v) >= 3:
            print(f"  {k}: {ozet_metrik(v)}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cv", action="store_true")
    ap.add_argument("--egit", action="store_true")
    ap.add_argument("--holdout", action="store_true")
    a = ap.parse_args()
    if a.cv:
        print(json.dumps(cv(), ensure_ascii=False, indent=1))
    if a.egit:
        egit()
    if a.holdout:
        holdout()
