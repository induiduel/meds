"""2026-27 Kurul 1 sınaması için ortak veri: ders notu satırları, altın kaynak satırlar, geliştirme/bekletilmiş ayrımı, metrikler.

Altın etiket: `eslesme.kanit` satırları (91 soru × 2 aday; 17'si elle). "Öğrenim Hedefleri" altındaki satırlar altına girmez (genel hedef cümlesi,
sorunun kaynağı değil); geriye altın kalmayan soru ilk adayı korur.
Ayrım: ders notları md5'e göre 3'te 1 BEKLETİLMİŞ (yalnız 0., 5., 10. turda ölçülür, ayarlama için asla bakılmaz), kalanı GELİŞTİRME.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import KOK, jetonlar, norm  # noqa: E402
from satir_model import dosya_satirlari, temizle  # noqa: E402

NOT = KOK.parent / "meds_database_v2/ders_notlari_k1"
SC = KOK.parent / "meds_temp/hoca_profili_sinama"


DERS_ESLE = {"Patoloji": "Tıbbi Patoloji", "Farmakoloji": "Tıbbi Farmakoloji"}  # 2026-27 dosyasındaki kısa adlar → çıkmış bankası adları (tur 1–5'te eksikti: profil/emb_ders genel kaldı)


def veri():
    d = json.loads((KOK / "data/cikmis_2627/kurul1_2627.json").read_text())
    idx = {x["id"]: x for x in json.loads((NOT / "index.json").read_text())}
    S = [q for q in d["sorular"] if q["durum"] in ("tam", "siklar_uretildi") and q.get("ders_notu_id") in idx]
    ders = {}
    for q in S:
        k = q["ders_notu_id"]
        if k not in ders:
            p = NOT / idx[k]["dosya"]
            sat = dosya_satirlari(p)
            ders[k] = dict(id=k, ders=DERS_ESLE.get(q["ders"], q["ders"]), konu=q["konu"], yol=p, satirlar=sat, sorular=[])
        q["dogru"] = q["siklar"]["ABCDE".find(q["cevap"])] if "ABCDE".find(q.get("cevap") or "") >= 0 and "ABCDE".find(q["cevap"]) < len(q["siklar"]) else ""
        ders[k]["sorular"].append(q)
    for k, dd in ders.items():
        no2i = {r["no"]: i for i, r in enumerate(dd["satirlar"])}
        for q in dd["sorular"]:
            kan = [x["satir"] for x in (q.get("eslesme") or {}).get("kanit", [])]
            ham = [no2i[n] for n in kan if n in no2i and not re.search(r"öğrenim hedef", norm(dd["satirlar"][no2i[n]]["baslik"]))]
            if not ham:
                ham = [no2i[n] for n in kan if n in no2i]
            q["altin"] = ham
        dd["bekletilmis"] = int(hashlib.md5(k.encode()).hexdigest(), 16) % 3 == 0
    return ders


def gelistirme(ders):
    return {k: v for k, v in ders.items() if not v["bekletilmis"]}


def bekletilmis(ders):
    return {k: v for k, v in ders.items() if v["bekletilmis"]}


def isabet(oneri: list[int], altin: list[int], tol: int = 0) -> bool:
    return any(abs(o - a) <= tol for o in oneri for a in altin)


def puanla(skorlar: dict[str, list[float]], ders: dict, ks=(5, 10, 20), oran=0.10) -> dict:
    """skorlar[ders_id] = satır puanları. Soru başına: doğru kaynak satırın en iyi sırası → ilk-K isabeti, ilk-%10, ±1 komşu isabeti, AUC benzeri yüzdelik."""
    sonuc = {f"ilk{k}": 0 for k in ks}
    sonuc.update(ilk10yuzde=0, komsu_ilk10=0, yuzdelik=0.0)
    n = 0
    for k, dd in ders.items():
        sk = skorlar[k]
        sira = sorted(range(len(sk)), key=lambda i: -sk[i])
        for q in dd["sorular"]:
            if not q["altin"]:
                continue
            n += 1
            rank = {i: r for r, i in enumerate(sira)}
            en = min(rank[a] for a in q["altin"])
            for K in ks:
                sonuc[f"ilk{K}"] += en < K
            kes = max(1, math.ceil(oran * len(sk)))
            sonuc["ilk10yuzde"] += en < kes
            sonuc["komsu_ilk10"] += isabet(sira[:kes], q["altin"], 1)
            sonuc["yuzdelik"] += en / max(1, len(sk) - 1)
    for a in list(sonuc):
        sonuc[a] = round(sonuc[a] / n, 3)
    sonuc["n_soru"] = n
    return sonuc
