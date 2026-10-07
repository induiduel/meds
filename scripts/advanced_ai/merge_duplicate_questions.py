#!/usr/bin/env python3
"""
Kopya çıkmış soruları birleştirir (veri dosyasına dokunmadan, okuma katmanı olarak).

Aynı soru farklı sınav dökümlerinden farklı kimliklerle birden çok kez girilmiş (başlık artığı, tarih, OCR farkı).
Bu betik data/pastQuestions.json'daki soruları Faz 14'ün kopya ölçütüyle (phase14_cloud_question_editor._ayni_soru:
kök+şık kelime örtüşmesi, vaka sayıları aynı olmalı, genel şıklarda temkinli) gruplar ve
$MEDS_DATABASE_DIR/../meds_database_v2/soru_birlestirme/birlestirmeler.json dosyasına yazar.

Site (src/services/questionMerge.ts) her gruptan yalnız "asil" soruyu gösterir; asil soruya mergedFrom (kopya kimlikleri)
eklenir, kullanıcıya gösterilmez. Yönetici /manage → "Birleştirilen sorular"dan asıl soruyu değiştirebilir, grubu
ayırabilir ya da onaylayabilir. Yönetici kararları (durum != "otomatik") yeniden çalıştırmada korunur.

Kullanım: merge_duplicate_questions.py [--kuru]   (--kuru: yazmadan say)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase14_cloud_question_editor as P14  # noqa: E402  (aynı kopya ölçütü)

DB_DIR = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
OUT = DB_DIR.parent / "meds_database_v2" / "soru_birlestirme" / "birlestirmeler.json"
SRC = ROOT / "data" / "pastQuestions.json"
REVIEWS = P14.REVIEWS_FILE


def kok(q: dict) -> str:
    return str(q.get("stem") or (q.get("reconstruction") or {}).get("stem") or "")


def siklar(q: dict) -> list[str]:
    o = q.get("options") or (q.get("reconstruction") or {}).get("options") or []
    if isinstance(o, dict):
        o = list(o.values())
    return [str(x.get("text") if isinstance(x, dict) else x) for x in o]


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", str(t or "").lower().replace("ı", "i"))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def birebir(a: dict, b: dict) -> bool:
    return norm(kok(a)) == norm(kok(b)) and sorted(map(norm, siklar(a))) == sorted(map(norm, siklar(b)))


def benzerlik(a: dict, b: dict) -> float:
    x = P14._kelimeler(kok(a) + " " + " ".join(siklar(a)))
    y = P14._kelimeler(kok(b) + " " + " ".join(siklar(b)))
    return round(len(x & y) / max(1, len(x | y)), 3)


ARTIK = re.compile(r"(\d{1,2}[./]\d{1,2}[./]\d{2,4}|sınav\.|\.edu\.tr|acil tıp acil tıp|^\s*no\b)", re.I)


def asil_puani(q: dict, onayli: set) -> tuple:
    """Asıl soru seçimi: Faz 14'te onaylanmış > başlık/tarih artığı olmayan > şıkları dolu > kökü uzun."""
    k = kok(q)
    dolu = sum(1 for s in siklar(q) if len(s.strip()) > 2)
    return (str(q.get("id")) in onayli, not ARTIK.search(k), dolu, len(k))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()

    raw = json.loads(SRC.read_text(encoding="utf-8"))
    qs = raw if isinstance(raw, list) else raw.get("questions", [])
    by_id = {str(q.get("id")): q for q in qs if q.get("id")}

    onayli = set()
    if REVIEWS.exists():
        for line in REVIEWS.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                if r.get("status") == "approved":
                    onayli.add(str(r.get("question_id")))
            except Exception:
                continue

    # Kopya çiftleri (Faz 14 ile aynı ölçüt) → birleşim-bul
    dizin = P14.KopyaDizini()
    ebeveyn: dict[str, str] = {}

    def bul(x):
        while ebeveyn.get(x, x) != x:
            x = ebeveyn[x]
        return x

    for qid, q in by_id.items():
        src = {"soru_koku": kok(q), "secenekler": {chr(65 + i): s for i, s in enumerate(siklar(q))}}
        esi = dizin.kopyasi_mi(qid, src)
        if esi:
            ebeveyn[bul(qid)] = bul(esi)
        dizin.ekle(qid, src)

    gruplar: dict[str, list[str]] = {}
    for qid in by_id:
        gruplar.setdefault(bul(qid), []).append(qid)
    gruplar = {k: v for k, v in gruplar.items() if len(v) > 1}

    # Önceki yönetici kararlarını koru
    eski = {}
    if OUT.exists():
        try:
            eski = {g["id"]: g for g in json.loads(OUT.read_text(encoding="utf-8")).get("gruplar", [])}
        except Exception:
            eski = {}
    karar_uyeleri = {u for g in eski.values() if g.get("durum") != "otomatik" for u in g.get("uyeler", [])}

    sonuc = [g for g in eski.values() if g.get("durum") != "otomatik"]   # onaylı / ayrıldı / elle seçilmiş
    for uyeler in gruplar.values():
        if any(u in karar_uyeleri for u in uyeler):
            continue                                                 # yönetici bu sorular için karar vermiş
        # temiz çekirdek: kökü diğer kopyaların içinde aynen geçen soru başına başlık/ders adı artığı almamıştır
        cekirdek = {u: sum(1 for v in uyeler if v != u and norm(kok(by_id[u])) and norm(kok(by_id[u])) in norm(kok(by_id[v])))
                    for u in uyeler}
        uyeler = sorted(uyeler, key=lambda u: (str(u) in onayli, cekirdek[u] > 0, *asil_puani(by_id[u], onayli)[1:]),
                        reverse=True)
        asil = uyeler[0]
        gid = "g-" + asil
        sonuc.append({
            "id": gid,
            "asil": asil,
            "uyeler": uyeler,
            "birebir_ayni": all(birebir(by_id[asil], by_id[u]) for u in uyeler[1:]),
            "benzerlik": min(benzerlik(by_id[asil], by_id[u]) for u in uyeler[1:]),
            "durum": "otomatik",              # otomatik | onayli | ayrildi (yönetici kararı)
            "olusturma": datetime.now().isoformat(timespec="seconds"),
        })

    aktif = [g for g in sonuc if g.get("durum") != "ayrildi"]
    gizlenen = sum(len(g["uyeler"]) - 1 for g in aktif)
    farkli = sum(1 for g in aktif if not g.get("birebir_ayni"))
    print(f"grup: {len(aktif)} · gizlenecek kopya: {gizlenen} · birebir aynı olmayan (incelenmeli): {farkli}")
    if a.kuru:
        for g in sorted(aktif, key=lambda g: g["benzerlik"])[:8]:
            print(" ", g["benzerlik"], g["uyeler"], "|", " ".join(kok(by_id[g["asil"]]).split())[:70])
        return 0
    if not aktif and OUT.exists():
        print("boş sonuç: mevcut dosya korunuyor")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"guncelleme": datetime.now().isoformat(timespec="seconds"), "gruplar": sonuc},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"yazıldı: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
