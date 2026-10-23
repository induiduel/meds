"""Görev `parca_sorusu` — sesli dersin bir bölümü için 1–6 pekiştirme sorusu (ICERIK_MOTORU_V3.md §3.2).

Hedef: bölüm kimliği `kN-NN-bNN`. Girdi: o bölümün cümleleri (S1…, ekran yüzü) + bölümün slayt sayfalarının metni
(salt okunur dayanak). Bağlam: önceki bölüm başlıkları, sonraki bölümün başlığı (kronoloji: sorulmaz).
Model çıktısı (kısa etiketli JSON) → derleyici → `{surum, ders_id, bolum, sorular:[{id: <bolum>-ps<N>, …,
kanit_cumleler:[k…-cNNNN]}]}`. Uygulama: `meds_database_v2/ders_bilgi/<ders>/l2/parca_sorulari/<bolum>.json`.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .. import cekirdek as c
from . import _ortak as o

KURALLAR = ["kaynak_sadakati", "soru_yazimi", "sik_aciklama", "kronoloji", "turkce_uslup", "cikti_disiplini"]


def soru_sayisi(cumle_sayisi: int, cikmis_cumle: int) -> int:
    """Bölüm yoğunluğu: ~8 cümlede 1 soru + çıkmış bağlı her 2 cümleye 1; 1–6 arası."""
    return max(1, min(6, round(cumle_sayisi / 8) + (cikmis_cumle + 1) // 2))


def _bolum(hedef: str):
    m = re.fullmatch(r"(k\d-\d{2})-b\d{2,3}", hedef)
    if not m:
        raise SystemExit(f"parca_sorusu hedefi bölüm kimliği olmalı (kN-NN-bNN): {hedef}")
    ders_id = m.group(1)
    _, d = o.konusma_bul(ders_id)
    bolumler = d.get("bolumler") or []
    i = next((i for i, b in enumerate(bolumler) if b.get("id") == hedef), None)
    if i is None:
        raise SystemExit(f"bölüm yok: {hedef}")
    return ders_id, d, bolumler, i


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    ders_id, d, bolumler, i = _bolum(hedef)
    b = bolumler[i]
    et = c.Etiketler()
    satirlar, sayfalar, cikmisli = [], [], 0
    for p in b.get("paragraflar") or []:
        if p.get("sayfa") and p["sayfa"] not in sayfalar:
            sayfalar.append(p["sayfa"])
        for cm in p.get("cumleler") or []:
            metin = (cm.get("ekran") or cm.get("ses") or "").replace("**", "").strip()
            if not metin:
                continue
            cikmisli += bool(cm.get("cikmis"))
            satirlar.append(f"{et.ekle('S', cm['id'])}: {metin}")
    if len(satirlar) < 3:
        raise SystemExit(f"{hedef}: bölümde {len(satirlar)} cümle var — soru için yetersiz")
    n = int((ayar or {}).get("adet") or soru_sayisi(len(satirlar), cikmisli))
    kaynak = o.kaynak_sayfalar(ders_id)
    slayt = "\n".join(f"Sayfa {s}: {o.sade(kaynak[s], 900)}" for s in sayfalar if kaynak.get(s, "").strip())
    girdi = (f"Ders: {d.get('baslik', ders_id)}\nBölüm: {b.get('baslik', '')}\n\n## Bölümün anlatım cümleleri\n"
             + "\n".join(satirlar)
             + (f"\n\n## Bu bölümün slayt metni (dayanak, etiketsiz)\n{slayt}" if slayt else ""))
    onceki = [x.get("baslik", "") for x in bolumler[:i]][-6:]
    sonraki = bolumler[i + 1].get("baslik", "") if i + 1 < len(bolumler) else ""
    baglam = ("Önceki bölümler: " + ("; ".join(onceki) or "—") + f"\nSonraki bölüm (henüz anlatılmadı, sorma): {sonraki or '—'}")
    ornek = {"sorular": [{"kok": "…?", "secenekler": {h: "…" for h in o.HARFLER}, "dogru": "C",
                          "aciklama": "Doğru cevabın gerekçesi, 1–3 cümle.",
                          "sik_aciklamalari": {"A": "Yanlış. …", "B": "Yanlış. …", "C": "Doğru. …", "D": "Yanlış. …",
                                               "E": "Yanlış. …"},
                          "kanit": ["S2", "S5"]}]}
    return {
        "amac": (f"Aşağıdaki sesli ders bölümünü dinleyen öğrencinin bilgisini pekiştiren TAM OLARAK {n} çoktan seçmeli "
                 f"soru yaz. Her soru bu bölümde anlatılan bir bilgiyi ölçer ve o bilginin geçtiği cümleleri `kanit` "
                 f"alanında S etiketleriyle gösterir."),
        "kurallar": KURALLAR,
        "ek_kurallar": [
            "Her şık açıklaması 'Doğru.' ya da 'Yanlış.' ile başlar; doğru şıkkınki 'Doğru.' ile.",
            "`kanit` en az bir S etiketidir; doğru cevabın bilgisi bu cümlelerde açıkça geçer.",
            "Beş şıkkın HEPSİ GİRDİ'de (bölüm cümleleri ya da slayt metni) geçen kavramlardan seçilir; şık açıklamaları da "
            "yalnız GİRDİ'deki bilgiyle yazılır — ders dışı kavram ya da ders kitabı bilgisi ekleme.",
            f"Sorular birbirini tekrar etmez; {n} soru bölümün farklı bilgilerini ölçer.",
        ],
        "girdi": girdi, "baglam": baglam,
        "cikti_bicimi": "Yalnız şu JSON (sorular dizisinde tam " + str(n) + " öğe):\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": [f"tam {n} soru", "şıklar A–E, tek doğru", "kanıt etiketleri girdide var ve doğru şıkkı içeriyor",
                            "şık açıklaması 2–4 cümle, 20–65 kelime, ne / ne işe yarar / neden",
                            "kökte doğru şıkkın kelimeleri yok", "yasak kalıp ve süreç dili yok"],
        "esleme": et.esleme,
        "meta": {"ders_id": ders_id, "bolum": hedef, "adet": n, "kurul": int(ders_id[1]), "girdi_kok": sorted(c.kokler(girdi, en_az=3))},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("sorular"), list):
        return None, ["cevap JSON değil ya da 'sorular' dizisi yok"]
    et = c.Etiketler(esleme)
    e, sorular = [], []
    for i, q in enumerate(j["sorular"], 1):
        if not isinstance(q, dict):
            e.append(f"Q{i}: soru nesne değil"); continue
        kanit = q.get("kanit") or []
        if isinstance(kanit, str):
            kanit = re.findall(r"S\d+", kanit)
        uzun = [et.uzun(k) for k in kanit]
        if not kanit:
            e.append(f"Q{i}: kanit boş")
        bilinmeyen = [k for k, u in zip(kanit, uzun) if not u]
        if bilinmeyen:
            e.append(f"Q{i}: girdide olmayan etiket {bilinmeyen}")
        sec = {str(h).strip().upper()[:1]: str(t).strip() for h, t in (q.get("secenekler") or {}).items()}
        sorular.append({"id": f"{meta['bolum']}-ps{i}", "kok": str(q.get("kok") or "").strip(), "secenekler": sec,
                        "dogru": str(q.get("dogru") or "").strip().upper()[:1],
                        "aciklama": str(q.get("aciklama") or "").strip(),
                        "sik_aciklamalari": {str(h).strip().upper()[:1]: str(t).strip()
                                             for h, t in (q.get("sik_aciklamalari") or {}).items()},
                        "kanit_cumleler": [u for u in uzun if u]})
    return {"surum": 1, "ders_id": meta["ders_id"], "bolum": meta["bolum"], "sorular": sorular}, e


def _cumle_metinleri(ders_id: str) -> dict[str, str]:
    _, d = o.konusma_bul(ders_id)
    return {cm["id"]: (cm.get("ekran") or cm.get("ses") or "") for b in d.get("bolumler", [])
            for p in b.get("paragraflar", []) for cm in p.get("cumleler", [])}


def dogrula(cikti: dict, meta: dict) -> list[str]:
    e = []
    s = cikti.get("sorular") or []
    if len(s) != meta["adet"]:
        e.append(f"{len(s)} soru — tam {meta['adet']} olmalı")
    metin = _cumle_metinleri(meta["ders_id"])
    bolum_onek = meta["bolum"].rsplit("-b", 1)[0]
    gorulen = set()
    for q in s:
        yer = q["id"].rsplit("-", 1)[-1]
        for k in q["kanit_cumleler"]:
            if not k.startswith(bolum_onek):
                e.append(f"{yer}: kanıt başka dersten {k}")
        dayanak = " ".join(metin.get(k, "") for k in q["kanit_cumleler"])
        e += o.soru_denetle(q, yer, dayanak)
        # Kural 4: her şıkkın kavramı girdide geçmeli (ders dışı çeldirici yok)
        gk = set(meta.get("girdi_kok") or [])
        if gk:
            for h, t in q["secenekler"].items():
                kk = c.kokler(t, en_az=3)
                if kk and not (kk & gk):
                    e.append(f"{yer}.{h}: şık kavramı ({t[:40]!r}) bölümde/slaytta geçmiyor — çeldirici dersin kavramlarından seçilmeli")
        kk = c.katla(q["kok"])
        if kk in gorulen:
            e.append(f"{yer}: aynı soru kökü tekrar")
        gorulen.add(kk)
    return e


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    """Çözücü: derlenmiş çıktı → modelin yazacağı kısa etiketli JSON (gidiş-dönüş sınaması)."""
    et = c.Etiketler(esleme)
    return json.dumps({"sorular": [{"kok": q["kok"], "secenekler": q["secenekler"], "dogru": q["dogru"],
                                    "aciklama": q["aciklama"], "sik_aciklamalari": q["sik_aciklamalari"],
                                    "kanit": [et.kisa(k) for k in q["kanit_cumleler"]]} for q in cikti["sorular"]]},
                      ensure_ascii=False, indent=1)


def ozet(cikti: dict, esleme: dict, meta: dict) -> str:
    """Denetçiye gösterilecek okunur biçim (kısa etiketli)."""
    return tersine(cikti, esleme, meta)


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    if meta["kurul"] == 1 and cikis is None and not k1_izin:
        raise SystemExit("Kurul 1 verisine otomatik yazım yok (El kitabı §0.4): --cikis DİZİN ile sınama ya da --k1-izin")
    hedef = (cikis or c.DB2 / "ders_bilgi" / meta["ders_id"] / "l2" / "parca_sorulari") / f"{meta['bolum']}.json"
    c.yaz(hedef, cikti)
    return hedef
