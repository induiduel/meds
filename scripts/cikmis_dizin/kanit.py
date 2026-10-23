#!/usr/bin/env python3
"""Kanıt bölgeleri — her sorunun işaret ettiği bilginin slayttaki yeri + otomatik tekrar listesi (ICERIK_MOTORU_V3.md §16).

Sorular: dersin tarama planındaki bağlı çıkmışlar (l1/tarama_plani.json) + dersin örnek soruları (src/data/ornek_sorular).
Birim: L0 metin BLOĞU (uzun blok — >60 sözcük ya da >6 satır — ana madde işaretlerinden maddelere bölünür; tekrar eden başlık/altbilgi ve <3 sözcük atılır).
Slayt başlığı birimi (kısa + üst bant ya da numaralı) cevap terimini taşısa da `kesin` doğru bölgesi olamaz; gündem
sayfaları (hedefler, amaçlar, içerik, kazanımlar) hiç aday değildir.
Liste birimi (≥2 çeldirici de içinde geçiyor) ayırt etmez → anlamsal şart tutmaz. Olumsuz kök ("…değildir", "yanlıştır")
betikle en çok `olasi` (kanıt çeldiricilerin yeri). "Şekil/Tablo N.N'ye göre" kökü → o şeklin sayfası `kesin` (sekil_atfi).
Her soru için (betik; model yok):
  1. aday sayfalar: soru (kök + doğru) ↔ sayfa vektörü en iyi 3 sayfa (+ plandaki sayfalar);
  2. SÖZCÜKSEL şart: doğru şıkkın içerik köklerinin ≥ yarısı (en az 1) birimde geçer; sayı soruyorsa sayı birebir;
  3. ANLAMSAL şart: birimin sayfası soruyla bge-m3 ≥ BIRIM_ESIK (konu) ve birim içinde TF-IDF(birim, doğru şık) −
     en iyi TF-IDF(birim, çeldirici) > FARK (birim doğru cevabı AYIRT etmeli, yalnız konuyu değil). Birim düzeyinde sinir
     ağı vektörü yok: vektör servisleri CPU kotalı (2026-10-23 ölçümü 32 metin ≈ 8–18 sn) — TF-IDF dersin kendi
     birimlerinden kurulur, belirlenimci ve hızlıdır;
  4. ikisi tutarsa `kesin`, biri tutarsa `olasi` (R4'te `kanit_bagla` görevine), hiçbiri tutmazsa bağ YOK → `bagsiz`.
  Çeldirici bölgesi: yanlış şık derste ayrıca anlatılıyorsa (sözcüksel ≥ %60 + benzerlik ≥ BIRIM_ESIK) `celdirici`.
Kapı (`dogrula`): sayfa/satır geçerli; aynı birim, kökleri neredeyse aynı (≥0,92) ama doğru cevapları farklı iki sorunun
`kesin` kanıtı olamaz (çelişki → ikisi de `olasi`ya düşer).
Tekrar listesi (öğrenciye otomatik sunulan): yalnız TEKRAR katmanı = `kesin` + cevabın TÜM içerik kökleri birimde + birimin
sayfası bge-m3'e göre en benzer sayfa; çıkmış (kez, yıl) önce; aynı birim tek kart. K1 ölçümü (5.297 örnek soru, elle konan
kanıt sayfasıyla): kesin %69 → kabul %96,0; TEKRAR katmanı %33 → kabul %98,8 (kalan "yanlış"ların bir kısmı aynı bilginin
özet/tablo sayfası). Kesin-dışı ve olumsuz sorular R4 `kanit_bagla` görevine (modelle) gider.

Çıktı: meds_database_v2/ders_bilgi/<ders>/l1/kanit.json
Kullanım (.venv-ocr): kanit.py --ders k1-03 [--olc]   |   kanit.py --kurul 1 --olc    (örnek soru `kanit.sayfa` ile ölçüm)
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kroki"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402

import dizin as D  # noqa: E402
import plan as P  # noqa: E402
from ortak import DEPO, KOK, dersler, katla, kokler, oku, sayilar, vektorle, yaz  # noqa: E402

SURUM = 6
BIRIM_ESIK = 0.50     # sayfa (bge-m3) konu eşiği
FARK = 0.0           # birim: TF-IDF(doğru) − en iyi TF-IDF(çeldirici) > FARK
SOZ_ORAN = 0.5


GUNDEM = re.compile(r"\b(hedef(ler)?|öğrenim hedef\w*|amaç(lar)?|içerik|ders planı|sunum planı|konu başlıkları|"
                    r"kazanımlar|outline|objectives)\b", re.I)


def gundem_sayfasi(s: dict) -> bool:
    """Ders başı/sonu gündem sayfası (hedefler, amaçlar, içerik): bilgi değil başlık listesidir → kanıt adayı değil."""
    ilk = " ".join(st["metin"] for st in s["satirlar"][:2])
    return bool(GUNDEM.search(ilk)) and len(s["metin"].split()) < 120


def birimler(l0: dict) -> list[dict]:
    tekrar = set(l0.get("tekrar_satirlar") or [])
    out = []
    for s in l0["sayfalar"]:
        if gundem_sayfasi(s):
            continue
        gruplar: dict = {}
        for i, st in enumerate(s["satirlar"]):
            if katla(st["metin"]).strip() in tekrar:
                continue
            gruplar.setdefault(st.get("blok", i), []).append(i)
        for satirlar in gruplar.values():
            parcalar = [satirlar]
            metin = " ".join(s["satirlar"][i]["metin"] for i in satirlar)
            if len(metin.split()) > 60 or len(satirlar) > 6:
                parcalar = maddeler(satirlar, s["satirlar"])
            for p in parcalar:
                t = " ".join(s["satirlar"][i]["metin"] for i in p).strip()
                if len(t.split()) < 3:
                    continue
                bx = [min(s["satirlar"][i]["bbox"][0] for i in p), min(s["satirlar"][i]["bbox"][1] for i in p),
                      max(s["satirlar"][i]["bbox"][2] for i in p), max(s["satirlar"][i]["bbox"][3] for i in p)]
                out.append({"sayfa": s["sayfa"], "satirlar": p, "bbox": bx, "metin": t, "baslik": baslik_mi(t, bx)})
    return out


ANA_MADDE = re.compile(r"^\s*(?:[•●▪■➢◆✓]|\d+[.)]\s)")


def maddeler(satirlar: list[int], st: list[dict]) -> list[list[int]]:
    """Uzun blok → madde birimleri: ana madde işaretiyle (•, ●, ▪, ➢, "1.") başlayan satır yeni birim açar; alt madde
    (–, -, o) ve devam satırları ana maddeye bağlanır. Ana madde yoksa 3 satırlık pencereler. Birim ≤ 8 satır."""
    out: list[list[int]] = []
    for i in satirlar:
        if not out or ANA_MADDE.match(st[i]["metin"]) or len(out[-1]) >= 8:
            out.append([i])
        else:
            out[-1].append(i)
    if len(out) == 1 and len(satirlar) > 6:
        out = [satirlar[k:k + 3] for k in range(0, len(satirlar), 3)]
    return out


def baslik_mi(metin: str, bbox: list[float]) -> bool:
    """Slayt başlığı: kısa (≤ 8 sözcük) ve sayfanın üst bandında ya da numaralı ("4. …", "3) …"). Başlık cevap terimini
    taşısa da bilgiyi taşımaz → doğru cevap bölgesi `kesin` olamaz (2026-10-23 ölçümü: kesin ıskalarının çoğu başlıktı)."""
    w = metin.split()
    return len(w) <= 8 and (bbox[1] < 0.2 or bool(re.match(r"^\s*\d+\s*[.)]\s", metin)))


def ornek_sorulari(ders_id: str) -> list[dict]:
    m = re.match(r"k(\d)-", ders_id)
    out = []
    for p in sorted((KOK / "src" / "data" / "ornek_sorular" / f"k{m.group(1)}").glob(f"{ders_id}-*.json")):
        for kz in (oku(p, {}) or {}).get("kazanimlar", []):
            for q in kz.get("sorular", []):
                sec = q.get("secenekler") or {}
                if q.get("dogru") in sec:
                    out.append({"id": q["id"], "kaynak": "ornek", "kok": q.get("soru", ""), "secenekler": sec,
                                "dogru": q["dogru"], "dogru_metin": sec[q["dogru"]], "kez": 0, "yillar": [],
                                "_gercek_sayfa": (q.get("kanit") or {}).get("sayfa")})
    return out


class Tfidf:
    """Dersin kendi birimlerinden 5 harf kök TF-IDF (betik; servis yok). Birim içi ayırt etme için."""

    def __init__(self, metinler: list[str]):
        from collections import Counter
        self.df = Counter()
        belgeler = [Counter(self._k(t)) for t in metinler]
        for b in belgeler:
            self.df.update(b.keys())
        self.n = len(metinler)
        self.birim = [self._v(b) for b in belgeler]

    @staticmethod
    def _k(t: str) -> list[str]:
        return [katla(w)[:5] for w in re.findall(r"[0-9a-zçğıöşüâîû]+", (t or "").replace("İ", "i").replace("I", "ı").lower())
                if len(w) >= 3]

    def _v(self, sayac) -> dict:
        v = {k: (1 + math.log(c)) * math.log((self.n + 1) / (self.df.get(k, 0) + 1) + 1) for k, c in sayac.items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {k: x / n for k, x in v.items()}

    def vek(self, t: str) -> dict:
        from collections import Counter
        return self._v(Counter(self._k(t)))

    @staticmethod
    def cos(a: dict, b: dict) -> float:
        if len(a) > len(b):
            a, b = b, a
        return sum(x * b.get(k, 0.0) for k, x in a.items())


KURAL = {"liste": False, "olumsuz": True, "sekil": True, "baslik": True, "ust2": True}   # ablasyon sınaması için anahtarlar
OLUMSUZ = re.compile(r"\b(değil\w*|yanlış\w*|olama\w*|beklenme\w*|görülme\w*|bulunma\w*|sayılma\w*|içerme\w*|"
                     r"yer alma\w*|rastlanma\w*|dışında\w*|hariç)", re.I)
SEKIL = re.compile(r"(Şekil|ŞEKİL|Tablo|TABLO)\s*(\d+\.\d+)")


def sekil_sayfasi(kok: str, l0: dict) -> int | None:
    """Kök "Şekil 2.6'ya göre…" diyorsa o şekil/tablonun yazısının geçtiği sayfa (bilgi şekilde; metin birimi değil)."""
    m = SEKIL.search(kok or "")
    if not m:
        return None
    aranan = katla(f"{m.group(1)} {m.group(2)}")
    for s in l0["sayfalar"]:
        if aranan in katla(s["metin"]).replace("  ", " "):
            return s["sayfa"]
    return None


def sozcuksel(cevap: str, birim: str) -> bool:
    hedef = kokler(cevap)
    sy = sayilar(cevap)
    bk = kokler(birim)
    if sy and not sy <= sayilar(birim):
        return False
    if not hedef:
        return bool(sy)
    return len(hedef & bk) >= max(1, math.ceil(SOZ_ORAN * len(hedef)))


def kur(ders_id: str, olc: bool = False, dz=None, log=print) -> dict:
    t0 = time.time()
    l0 = oku(DEPO / ders_id / "l0" / "sayfalar.json")
    plan = oku(DEPO / ders_id / "l1" / "tarama_plani.json")
    if not l0 or not plan:
        raise SystemExit(f"{ders_id}: L0 ya da tarama planı yok")
    d, V = dz or D.yukle()
    dizin_id = {q["id"]: q for q in d["sorular"]}
    sorular = []
    for b in plan["bagli"]:
        q = dizin_id.get(b["id"])
        if q:
            sorular.append({**{k: q[k] for k in ("id", "kok", "secenekler", "dogru", "dogru_metin", "kez", "yillar")},
                            "kaynak": "cikmis", "_plan_sayfa": b["sayfalar"]})
    sorular += ornek_sorulari(ders_id)
    B = birimler(l0)
    if not B or not sorular:
        raise SystemExit(f"{ders_id}: birim ya da soru yok")
    T = Tfidf([b["metin"] for b in B])
    sayfa_no, SV = P.sayfa_vektorleri(l0)
    QK = vektorle([f"{q['kok']} {q['dogru_metin']}" for q in sorular])
    sonuc, bagsiz = [], []
    for qi, q in enumerate(sorular):
        ps = QK[qi] @ SV.T if len(sayfa_no) else np.zeros(0)
        en_sayfa = float(ps.max()) if len(ps) else 0.0
        aday_sayfa = {sayfa_no[k] for k in np.argsort(-ps)[:3]} | set(q.get("_plan_sayfa") or [])
        idx = [i for i, b in enumerate(B) if b["sayfa"] in aday_sayfa]
        if not idx:
            bagsiz.append(q["id"]); continue
        tq = T.vek(f"{q['kok']} {q['dogru_metin']}")
        td = T.vek(q["dogru_metin"])
        tc = [T.vek(t) for h, t in q["secenekler"].items() if h != q["dogru"] and t]
        sayfa_puan = {sayfa_no[k]: float(ps[k]) for k in range(len(sayfa_no))}
        olumsuz = KURAL["olumsuz"] and bool(OLUMSUZ.search(q["kok"]))
        cel_metin = [t for h, t in q["secenekler"].items() if h != q["dogru"] and t]
        sekil = sekil_sayfasi(q["kok"], l0) if KURAL["sekil"] else None
        if sekil:
            ust = [i for i, b in enumerate(B) if b["sayfa"] == sekil]
            if ust:
                i = max(ust, key=lambda j: T.cos(T.birim[j], tq))
                sonuc.append({"soru": q["id"], "kaynak": q["kaynak"], "kez": q["kez"], "yillar": q["yillar"],
                              "bolgeler": [{"rol": "dogru", "sayfa": sekil, "satirlar": B[i]["satirlar"], "bbox": B[i]["bbox"],
                                            "guven": "kesin", "yontem": "sekil_atfi", "metin": B[i]["metin"][:200]}],
                              "_gercek_sayfa": q.get("_gercek_sayfa"), "_vek": qi})
                continue
        en, en_puan = None, -9.0
        for i in idx:
            soz = sozcuksel(q["dogru_metin"], B[i]["metin"])
            # liste birimi: çeldiricilerden biri de aynı birimde geçiyorsa birim doğru cevabı AYIRT etmez
            cel_var = sum(1 for t in cel_metin if kokler(t) and sozcuksel(t, B[i]["metin"])) if (KURAL["liste"] or olumsuz) else 0
            s_kd = T.cos(T.birim[i], tq)
            s_d = T.cos(T.birim[i], td)
            s_c = max((T.cos(T.birim[i], c) for c in tc), default=0.0)
            # anlamsal: sayfa bge-m3 eşiği (konu) + birim doğru şıkkı çeldiricilerden AYIRT ediyor (TF-IDF)
            anl = sayfa_puan.get(B[i]["sayfa"], 0) >= BIRIM_ESIK and s_d - s_c > FARK and s_d > 0 and cel_var < 2
            if olumsuz:
                # olumsuz kök: kanıt çeldiricilerin anlatıldığı yer; birim seçimi çeldirici kapsamına göre
                soz, anl = cel_var >= 2, False
            puan = s_kd + (0.5 if soz else 0) + (0.25 if anl else 0) + 0.2 * sayfa_puan.get(B[i]["sayfa"], 0) \
                - (1.0 if B[i]["baslik"] and KURAL["baslik"] else 0)
            if puan > en_puan:
                en, en_puan = (i, soz, anl, s_kd, s_d - s_c), puan
        i, soz, anl, sk, fark = en
        # ikinci bağımsız sinyal: birimin sayfası sorunun bge-m3 ile en benzer iki sayfasından biri olmalı
        ust2 = {sayfa_no[k] for k in np.argsort(-ps)[:2]} if len(ps) else set()
        if KURAL["ust2"] and B[i]["sayfa"] not in ust2 and not (q.get("_plan_sayfa") and B[i]["sayfa"] in q["_plan_sayfa"][:1]):
            anl = False
        # olumsuz soru betikle en çok "olası" (R4 kanit_bagla görevi); başlık birimi kesin olamaz
        guven = "kesin" if soz and anl and not (B[i]["baslik"] and KURAL["baslik"]) and not olumsuz else ("olasi" if soz or anl else None)
        if not guven:
            bagsiz.append(q["id"]); continue
        # tekrar katmanı: kesin + cevabın TÜM içerik kökleri birimde + sayfa bge-m3'e göre en benzer sayfa
        ust1 = sayfa_no[int(np.argmax(ps))] if len(ps) else None
        hk = kokler(q["dogru_metin"])
        tam = bool(hk) and hk <= kokler(B[i]["metin"]) and sayilar(q["dogru_metin"]) <= sayilar(B[i]["metin"])
        tekrar_uygun = guven == "kesin" and tam and B[i]["sayfa"] == ust1
        bolgeler = [{"rol": "dogru", "sayfa": B[i]["sayfa"], "satirlar": B[i]["satirlar"], "bbox": B[i]["bbox"],
                     "guven": guven, "tekrar": tekrar_uygun, "benzerlik": round(sk, 3), "ayirt": round(fark, 3),
                     "sayfa_benzerlik": round(sayfa_puan.get(B[i]["sayfa"], 0), 3), "metin": B[i]["metin"][:200]}]
        for h, t in q["secenekler"].items():
            if h == q["dogru"] or not t or not kokler(t):
                continue
            tv = T.vek(t)
            ss = [T.cos(b, tv) for b in T.birim]
            k = int(np.argmax(ss))
            if k != i and ss[k] >= 0.3 and len(kokler(t) & kokler(B[k]["metin"])) >= max(1, math.ceil(0.6 * len(kokler(t)))):
                bolgeler.append({"rol": "celdirici", "sik": h, "sayfa": B[k]["sayfa"], "satirlar": B[k]["satirlar"],
                                 "bbox": B[k]["bbox"], "benzerlik": round(float(ss[k]), 3), "metin": B[k]["metin"][:200]})
        sonuc.append({"soru": q["id"], "kaynak": q["kaynak"], "kez": q["kez"], "yillar": q["yillar"], "bolgeler": bolgeler,
                      "_gercek_sayfa": q.get("_gercek_sayfa"), "_vek": qi})
    celiski = dogrula(sonuc, QK, sorular)
    model_kararlari_uygula(ders_id, sonuc, bagsiz, l0["pdf_sha"])
    tekrar = tekrar_listesi(sonuc)
    olcum = None
    if olc:
        g = [r for r in sonuc if r["_gercek_sayfa"]]
        kes = [r for r in g if r["bolgeler"][0]["guven"] == "kesin"]
        ola = [r for r in g if r["bolgeler"][0]["guven"] == "olasi"]
        def isabet(x): return sum(1 for r in x if abs(r["bolgeler"][0]["sayfa"] - r["_gercek_sayfa"]) <= 0) / max(len(x), 1)
        def yakin(x): return sum(1 for r in x if abs(r["bolgeler"][0]["sayfa"] - r["_gercek_sayfa"]) <= 1) / max(len(x), 1)
        ornek_toplam = sum(1 for q in sorular if q["kaynak"] == "ornek" and q.get("_gercek_sayfa"))
        olcum = {"ornek_soru": ornek_toplam, "kesin": len(kes), "olasi": len(ola),
                 "bagsiz": ornek_toplam - len(g), "kesin_sayfa_isabet": round(isabet(kes), 3),
                 "kesin_komsu_isabet": round(yakin(kes), 3), "olasi_sayfa_isabet": round(isabet(ola), 3)}
    for r in sonuc:
        r.pop("_vek", None); r.pop("_gercek_sayfa", None)
    cikti = {"surum": SURUM, "ders_id": ders_id, "pdf_sha": l0["pdf_sha"], "dizin_sha": plan["dizin_sha"],
             "kume_sha": plan.get("kume_sha"),
             "olusturuldu": time.strftime("%Y-%m-%dT%H:%M:%S"),
             "esik": {"birim": BIRIM_ESIK, "fark": FARK, "sozcuk_oran": SOZ_ORAN},
             "ozet": {"soru": len(sorular), "kesin": sum(1 for r in sonuc if r["bolgeler"][0]["guven"] == "kesin"),
                      "olasi": sum(1 for r in sonuc if r["bolgeler"][0]["guven"] == "olasi"), "bagsiz": len(bagsiz),
                      "celiski": len(celiski), "tekrar_karti": len(tekrar)},
             "sorular": sonuc, "bagsiz": bagsiz, "celiski": celiski, "tekrar": tekrar, "olcum": olcum,
             "model_bagsiz": sorted(k for k, v in ((oku(DEPO / ders_id / "l1" / "kanit_model.json") or {}).get("kararlar") or {}).items()
                                    if v.get("yok"))}
    yaz(DEPO / ders_id / "l1" / "kanit.json", cikti, 1)
    o = cikti["ozet"]
    log(f"{ders_id}: {o['soru']} soru → kesin {o['kesin']}, olası {o['olasi']}, bağsız {o['bagsiz']}, çelişki {o['celiski']}, "
        f"tekrar kartı {o['tekrar_karti']}" + (f" | ölçüm {olcum}" if olcum else "") + f" ({time.time() - t0:.0f} sn)")
    return cikti


def tekrar_listesi(sonuc: list[dict]) -> list[dict]:
    """Öğrenciye otomatik sunulan tekrar kartları: yalnız `tekrar: true` doğru bölgeleri; çıkmış (kez, yıl) önce."""
    tekrar, gorulen = [], set()
    for r in sorted((r for r in sonuc if r["bolgeler"][0].get("tekrar")),
                    key=lambda r: (r["kaynak"] != "cikmis", -r["kez"],
                                   -max([int(y[:4]) for y in r["yillar"] if y[:4].isdigit()] or [0]))):
        b = r["bolgeler"][0]
        anahtar = (b["sayfa"], tuple(b["satirlar"]))
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        tekrar.append({"sayfa": b["sayfa"], "satirlar": b["satirlar"], "bbox": b["bbox"], "soru": r["soru"],
                       "kaynak": r["kaynak"], "kez": r["kez"], "yontem": b.get("yontem", "betik"),
                       "celdirici": [x for x in r["bolgeler"][1:]][:2]})
    return tekrar


def model_kararlari_uygula(ders_id: str, sonuc: list[dict], bagsiz: list[str], pdf_sha: str) -> int:
    """`kanit_bagla` görevinin kararları (l1/kanit_model.json) betik yeniden koştuğunda kaybolmasın: aynı PDF için
    yeniden uygulanır; PDF değiştiyse yok sayılır (görev yeniden sorar)."""
    km = oku(DEPO / ders_id / "l1" / "kanit_model.json") or {}
    if km.get("pdf_sha") != pdf_sha:
        return 0
    sira = {r["soru"]: r for r in sonuc}
    n = 0
    for sid, k in (km.get("kararlar") or {}).items():
        if k.get("yok"):
            continue
        if sid in sira:
            sira[sid]["bolgeler"] = k["bolgeler"]
        else:
            sonuc.append({"soru": sid, "kaynak": k.get("kaynak", ""), "kez": k.get("kez", 0), "yillar": k.get("yillar", []),
                          "bolgeler": k["bolgeler"], "_gercek_sayfa": None, "_vek": None})
            if sid in bagsiz:
                bagsiz.remove(sid)
        n += 1
    return n


def dogrula(sonuc: list[dict], QK: np.ndarray, sorular: list[dict]) -> list[dict]:
    """Aynı birime kesin bağlı, kökleri neredeyse aynı ama doğru cevabı farklı sorular → çelişki; ikisi de `olasi`ya düşer."""
    celiski = []
    birime: dict = {}
    for r in sonuc:
        b = r["bolgeler"][0]
        if b["guven"] == "kesin":
            birime.setdefault((b["sayfa"], tuple(b["satirlar"])), []).append(r)
    for anahtar, rs in birime.items():
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, b = rs[i], rs[j]
                qa, qb = sorular[a["_vek"]], sorular[b["_vek"]]
                if float(QK[a["_vek"]] @ QK[b["_vek"]]) >= 0.92 and katla(qa["dogru_metin"]) != katla(qb["dogru_metin"]) \
                        and not (kokler(qa["dogru_metin"]) & kokler(qb["dogru_metin"])):
                    celiski.append({"birim": list(anahtar), "sorular": [a["soru"], b["soru"]]})
                    a["bolgeler"][0]["guven"] = b["bolgeler"][0]["guven"] = "olasi"
    return celiski


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders"); ap.add_argument("--kurul", type=int); ap.add_argument("--olc", action="store_true")
    a = ap.parse_args()
    liste = [a.ders] if a.ders else [x for x in dersler(a.kurul) if (DEPO / x / "l1" / "tarama_plani.json").exists()]
    dz = D.yukle()
    toplam = {"ornek_soru": 0, "kesin": 0, "olasi": 0, "isabet": 0, "komsu": 0}
    for x in liste:
        try:
            c = kur(x, a.olc, dz)
        except SystemExit as e:
            print(f"{x}: {e}"); continue
        if a.olc and c["olcum"]:
            o = c["olcum"]
            toplam["ornek_soru"] += o["ornek_soru"]; toplam["kesin"] += o["kesin"]; toplam["olasi"] += o["olasi"]
            toplam["isabet"] += round(o["kesin_sayfa_isabet"] * o["kesin"]); toplam["komsu"] += round(o["kesin_komsu_isabet"] * o["kesin"])
    if a.olc and len(liste) > 1:
        k = max(toplam["kesin"], 1)
        print(f"TOPLAM örnek soru {toplam['ornek_soru']}: kesin {toplam['kesin']} (%{100 * toplam['kesin'] / max(toplam['ornek_soru'], 1):.0f}),"
              f" olası {toplam['olasi']}; kesinde sayfa isabeti %{100 * toplam['isabet'] / k:.1f}, ±1 sayfa %{100 * toplam['komsu'] / k:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
