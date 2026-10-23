#!/usr/bin/env python3
"""PDF tarama planı — her ders yalnız kendi aday çıkmışlarını tarar (ICERIK_MOTORU_V3.md §15.2, §15.4).

Süzgeç (havuzu taramadan önce, betik):
  1. kapsam: Dönem 3 (dizin zaten yalnız Dönem 3); dersin BRANŞI ya da dersin KURULU (konular yıllar arasında kurul
     değiştirebilir → branş; branşı tutmayan ama aynı kuruldaki soru da aday). Başka dönem hiç aday olmaz.
  2. varlık kesişimi: dersin L0 varlıklarıyla ≥1 sözlük terimi (t:) ya da ≥2 varlık ortak — ya da konu adı eşleşmesi.
  3. KONU KİLİDİ: sorunun kayıtlı konusu (katlanmış) bir dersin defter konusuyla aynıysa soru YALNIZ o derse atanır
     (K1: 1.707 sorunun 1.463'ü, K2: 571/571 — ders kayıt defteri bu kuralla kuruldu). Konusu defterde başka bir derse
     ait olan soru, o dersin L0'ı henüz yoksa da başka derse ATANMAZ (bilinen konu = kN.json defterleri).
  4. TEK DERS kuralı (konusu tanınmayan sorular): puan = 0,6 × en iyi sayfa + 0,4 × en iyi 3 sayfa ortalaması (bge-m3)
     + 0,05 × derse özgü varlık örtüşmesi (idf); soru kapsamındaki dersler arasında EN yüksek puanlı derse (ya da en
     iyinin `PAY` içindekilere) ve `ESIK` üstündeyse bağlanır. Mutlak eşik tek başına yetmez: tıp metinleri arası bge-m3
     benzerliği 0,5–0,65 bandında yığılır (k1-12 akut inflamasyona transfüzyon ve SAAG soruları bağlanıyordu).
  5. sayfa: atanan dersin en iyi sayfası + en iyinin `KOMSU` katı üstündeki komşular (en çok 3).
Plan dosyası neden alındığını yazar; aynı PDF, aynı dizin ve aynı ders kümesiyle yeniden kurulmaz.
`--tam`: aynı kural kapsam/varlık süzgeci OLMADAN; hedefli planın kaçırdığı bağlar listelenir (ölçüt: 0).
`--olc`: Kurul 1 elle atamasıyla (bilgi deposu `yollar.cikmis`, müfredat konusuna göre) duyarlılık ve kesinlik.

Çıktı: meds_database_v2/ders_bilgi/<ders>/l1/tarama_plani.json
Kullanım (.venv-ocr): plan.py --kurul 1 [--tam] [--olc] [--zorla]   |   plan.py --ders k1-03 (tüm derslerin vektörleri önbellekten)
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kroki"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402

import dizin as D  # noqa: E402
from ortak import DEPO, KOK, dersler, katla, manifest, oku, sha, vektorle, yaz  # noqa: E402

SURUM = 3
ESIK = 0.55
PAY = 0.01
VARLIK_AGIRLIK = 0.05
KOMSU = 0.92


def sayfa_vektorleri(l0: dict) -> tuple[list[int], np.ndarray]:
    sayfalar, metin = [], []
    tekrar = set(l0.get("tekrar_satirlar") or [])
    for s in l0["sayfalar"]:
        t = " ".join(st["metin"] for st in s["satirlar"] if katla(st["metin"]).strip() not in tekrar)
        t += " " + " ".join(r.get("ocr", "") for r in s["resimler"])
        if len(t.split()) >= 5:
            sayfalar.append(s["sayfa"])
            metin.append(t[:2000])
    return sayfalar, vektorle(metin)


def _brans_eslesir(a: str, b: str) -> bool:
    a, b = katla(a).replace("tibbi ", "").strip(), katla(b).replace("tibbi ", "").strip()
    return bool(a) and bool(b) and (a == b or a in b or b in a)


def aday_mi(q: dict, ders: dict, ders_var: set[str]) -> str | None:
    """Aday ise nedeni, değilse None."""
    kapsam = _brans_eslesir(q["brans"], ders["brans"]) or (q["kurul"] == ders["kurul"])
    if not kapsam:
        return None
    ortak = set(q["varliklar"]) & ders_var
    if any(x.startswith("t:") for x in ortak):
        return "terim"
    if len(ortak) >= 2:
        return "varlik"
    if ders.get("konu") and katla(ders["konu"])[:12] and katla(ders["konu"])[:12] in katla(q.get("konu") or ""):
        return "konu"
    return None


class Evren:
    """Bilgi deposunda L0'ı olan TÜM derslerin sayfa vektörleri (küresel atama için; önbellekten hızlı)."""

    def __init__(self, dz, log=print):
        self.d, self.V = dz
        self.dersler, self.sayfa, self.sahip, satirlar, self.meta, self.var = [], [], [], [], {}, {}
        for p in sorted(DEPO.glob("k*-*/l0/sayfalar.json")):
            ders = p.parent.parent.name
            l0 = oku(p)
            sn, sv = sayfa_vektorleri(l0)
            if not sn:
                continue
            m = manifest(ders)
            self.meta[ders] = {"kurul": m.get("kurul"), "brans": m.get("brans") or "", "konu": m.get("konu") or "",
                               "pdf_sha": l0["pdf_sha"]}
            self.var[ders] = {v for s in l0["sayfalar"] for v in s.get("varliklar", [])}
            self.dersler.append(ders)
            self.sayfa += sn
            self.sahip += [len(self.dersler) - 1] * len(sn)
            satirlar.append(sv)
        self.SV = np.vstack(satirlar)
        self.sahip = np.array(self.sahip)
        self.kume_sha = sha("|".join(f"{x}:{self.meta[x]['pdf_sha']}" for x in self.dersler), 16)
        log(f"evren: {len(self.dersler)} ders, {len(self.sayfa)} sayfa")
        # soru × ders en iyi benzerlik (sayfaların en büyüğü) ve en iyi sayfa
        S = self.V @ self.SV.T
        n = len(self.dersler)
        self.en = np.full((S.shape[0], n), -1.0, dtype="float32")
        self.en_sayfa = np.zeros((S.shape[0], n), dtype=np.int64)
        for k in range(n):
            sut = np.flatnonzero(self.sahip == k)
            blok = S[:, sut]
            j = blok.argmax(1)
            self.en[:, k] = blok[np.arange(blok.shape[0]), j]
            self.en_sayfa[:, k] = sut[j]
        self.S = S
        # en iyi 3 sayfa ortalaması
        self.t3 = np.zeros_like(self.en)
        for k in range(n):
            sut = np.flatnonzero(self.sahip == k)
            self.t3[:, k] = np.sort(S[:, sut], 1)[:, -min(3, len(sut)):].mean(1)
        # derse özgü varlık örtüşmesi (yalnız sözlük terimleri; idf = log(ders sayısı / terimi içeren ders))
        import math
        from collections import Counter
        df = Counter(v for x in self.dersler for v in self.var[x] if v.startswith("t:"))
        idf = {v: math.log(n / c) for v, c in df.items()}
        self.vv = np.zeros_like(self.en)
        for i, q in enumerate(self.d["sorular"]):
            qv = [v for v in q["varliklar"] if v in idf]
            top = sum(idf[v] for v in qv)
            if top:
                for k, x in enumerate(self.dersler):
                    self.vv[i, k] = sum(idf[v] for v in qv if v in self.var[x]) / top
        self.puan = 0.6 * self.en + 0.4 * self.t3 + VARLIK_AGIRLIK * self.vv
        # konu kilidi
        konu_ders: dict[str, list[int]] = {}
        for k, x in enumerate(self.dersler):
            konu_ders.setdefault(katla(self.meta[x]["konu"]).strip(), []).append(k)
        bilinen = set(konu_ders) | bilinen_konular()
        self.kilit: dict[int, list[int]] = {}
        self.yabanci: set[int] = set()
        for i, q in enumerate(self.d["sorular"]):
            kq = katla(q.get("konu") or "").strip()
            if kq and kq in konu_ders:
                self.kilit[i] = konu_ders[kq]
            elif kq and kq in bilinen:
                self.yabanci.add(i)               # konusu L0'ı olmayan başka bir dersin: kimseye atanmaz

    def kapsam(self, filtreli: bool) -> np.ndarray:
        """soru × ders aday maskesi (filtreli=False: tam tarama, her soru her derse aday)."""
        n = len(self.dersler)
        M = np.ones((len(self.d["sorular"]), n), dtype=bool)
        if filtreli:
            for k, ders in enumerate(self.dersler):
                for i, q in enumerate(self.d["sorular"]):
                    M[i, k] = aday_mi(q, self.meta[ders], self.var[ders]) is not None
        return M

    def ata(self, M: np.ndarray, kilit: bool = True) -> dict[int, list[int]]:
        """ders sırası → atanan soru sıraları (konu kilidi, sonra TEK DERS kuralı). Neden `self.neden[(i, k)]`."""
        E = np.where(M, self.puan, -1.0)
        en_iyi = E.max(1)
        out: dict[int, list[int]] = {k: [] for k in range(len(self.dersler))}
        self.neden: dict[tuple, str] = {}
        for i in range(E.shape[0]):
            if kilit and i in self.kilit:
                for k in self.kilit[i]:
                    out[k].append(i); self.neden[(i, k)] = "konu"
                continue
            if kilit and i in self.yabanci:
                continue
            if en_iyi[i] < ESIK:
                continue
            for k in np.flatnonzero(E[i] >= en_iyi[i] - PAY):
                out[int(k)].append(i); self.neden[(i, int(k))] = "benzerlik"
        return out

    def bagli(self, k: int, sorular: list[int]) -> list[dict]:
        out = []
        sut = np.flatnonzero(self.sahip == k)
        for i in sorular:
            q = self.d["sorular"][i]
            satir = self.S[i, sut]
            en = float(satir.max())
            sec = [sut[j] for j in np.argsort(-satir)[:3] if satir[j] >= max(ESIK, KOMSU * en)]
            ikinci = np.sort(np.where(np.arange(len(self.dersler)) == k, -1, self.en[i]))[-1]
            out.append({"id": q["id"], "aile": q["aile"], "neden": getattr(self, "neden", {}).get((i, k), "benzerlik"),
                        "sayfalar": [self.sayfa[j] for j in sec], "benzerlik": round(en, 3),
                        "fark": round(en - float(ikinci), 3), "kez": q["kez"], "yillar": q["yillar"], "kurul": q["kurul"],
                        "brans": q["brans"]})
        return sorted(out, key=lambda x: -x["benzerlik"])


def kur_hepsi(liste: list[str], tam: bool = False, olc: bool = False, zorla: bool = False, dz=None, log=print) -> dict:
    t0 = time.time()
    E = Evren(dz or D.yukle(), log)
    M = E.kapsam(True)
    atama = E.ata(M)
    tam_atama = E.ata(E.kapsam(False), kilit=False) if tam else None
    if tam:
        E.ata(M)                                      # neden tablosu hedefli atamanınki olsun
    d = E.d
    olcum = {"gt": 0, "bulunan": 0, "plan_k1": 0, "plan_k1_dogru": 0}
    sonuc = {}
    for ders in liste:
        if ders not in E.dersler:
            log(f"{ders}: L0 yok — atlandı"); continue
        k = E.dersler.index(ders)
        hedef = DEPO / ders / "l1" / "tarama_plani.json"
        eski = oku(hedef) or {}
        if not (zorla or tam or olc) and eski.get("surum") == SURUM and eski.get("dizin_sha") == d["dizin_sha"] \
                and eski.get("kume_sha") == E.kume_sha:
            sonuc[ders] = eski; continue
        aday = int(M[:, k].sum())
        neden: dict = {}
        bagli = E.bagli(k, atama[k])
        plan = {"surum": SURUM, "ders_id": ders, "pdf_sha": E.meta[ders]["pdf_sha"], "dizin_sha": d["dizin_sha"],
                "kume_sha": E.kume_sha, "olusturuldu": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "suzgec": {"kurul": E.meta[ders]["kurul"], "brans": E.meta[ders]["brans"], "esik": ESIK, "pay": PAY,
                           "evren_ders": len(E.dersler)},
                "havuz": d["soru_sayisi"], "aday_sayisi": aday, "aday_orani": round(aday / max(d["soru_sayisi"], 1), 3),
                "bagli": bagli}
        if tam:
            P_ = set(atama[k])
            kacan = [i for i in tam_atama[k] if i not in P_]
            plan["tam_tarama"] = {"bagli": len(tam_atama[k]), "kacan": len(kacan),
                                  "kacan_ornek": [{"id": d["sorular"][i]["id"], "konu": d["sorular"][i]["konu"],
                                                   "benzerlik": round(float(E.en[i, k]), 3)} for i in kacan[:10]]}
        if olc:
            gt = gercek_atama(ders)
            if gt:
                plan_ids = {b["id"] for b in bagli}
                aile_gt = {x for x in gt}
                k1 = [b for b in bagli if b["kurul"] == E.meta[ders]["kurul"]]
                plan["olcum"] = {"gt": len(aile_gt), "bulunan": len(aile_gt & plan_ids),
                                 "plan_kurul": len(k1), "plan_kurul_gtde": sum(1 for b in k1 if b["id"] in aile_gt)}
                for a, b in (("gt", "gt"), ("bulunan", "bulunan"), ("plan_k1", "plan_kurul"), ("plan_k1_dogru", "plan_kurul_gtde")):
                    olcum[a] += plan["olcum"][b]
        yaz(hedef, plan, 1)
        sonuc[ders] = plan
        ek = f" | tam: {plan['tam_tarama']['bagli']} bağ, kaçan {plan['tam_tarama']['kacan']}" if tam else ""
        ek += f" | ölçüm {plan['olcum']}" if olc and plan.get("olcum") else ""
        log(f"{ders}: aday {aday} (%{100 * plan['aday_orani']:.1f}), bağlı {len(bagli)}{ek}")
    if olc and olcum["gt"]:
        log(f"ÖLÇÜM (elle atama): duyarlılık {olcum['bulunan']}/{olcum['gt']} = %{100 * olcum['bulunan'] / olcum['gt']:.1f};"
            f" kurul içi kesinlik {olcum['plan_k1_dogru']}/{olcum['plan_k1']} = %{100 * olcum['plan_k1_dogru'] / max(olcum['plan_k1'], 1):.1f}")
    if tam:
        kac = sum(p.get("tam_tarama", {}).get("kacan", 0) for p in sonuc.values())
        log(f"TAM TARAMA: toplam kaçan bağ {kac}")
    log(f"{time.time() - t0:.0f} sn")
    return sonuc


def kur(ders_id: str, tam: bool = False, zorla: bool = False, dz=None, log=print) -> dict:
    return kur_hepsi([ders_id], tam=tam, zorla=zorla, dz=dz, log=log)[ders_id]


def bilinen_konular() -> set[str]:
    """Ders kayıt defterlerindeki (src/data/dersler/kN.json) tüm konular — konusu tanınan soru başka derse atanmaz."""
    out = set()
    for p in sorted((KOK / "src" / "data" / "dersler").glob("k*.json")):
        for x in (oku(p, {}) or {}).get("dersler", []) if isinstance(oku(p, {}), dict) else []:
            if x.get("konu"):
                out.add(katla(x["konu"]).strip())
    return out


def gercek_atama(ders: str) -> set[str]:
    """Kurul 1 elle ataması: bilgi deposu `yollar.cikmis` ({kaynak_kod: [soru]}) — yalnız ölçüm için."""
    m = manifest(ders)
    p = (m.get("yollar") or {}).get("cikmis")
    d = oku(p) if p else None
    if not isinstance(d, dict):
        return set()
    return {q["id"] for q in d.get(str(m.get("kaynak_kod")), []) if isinstance(q, dict) and q.get("id")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders"); ap.add_argument("--kurul", type=int)
    ap.add_argument("--tam", action="store_true"); ap.add_argument("--olc", action="store_true")
    ap.add_argument("--zorla", action="store_true")
    a = ap.parse_args()
    liste = [a.ders] if a.ders else [x for x in dersler(a.kurul) if (DEPO / x / "l0" / "sayfalar.json").exists()]
    kur_hepsi(liste, a.tam, a.olc, a.zorla)
    return 0


if __name__ == "__main__":
    sys.exit(main())
