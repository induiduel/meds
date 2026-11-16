#!/usr/bin/env python3
"""
Faz 14: cevabı belirsiz kalan (çözücüler uzlaşamayan) bekleyen kayıtları Gemini ile yeniden sorgular.

Her soru Gemini'ye kör sorulur (eski cevap ve diğer oylar gösterilmez; ücretsiz anahtarlar, Flash yoksa Lite) ve toplam
3 cevap şıkkı toplanır (phase14_cloud_question_editor.belirsizi_gemini_ile_tamamla). Kayıt "şüpheli" işaretlenir
(/test/cikmis → Şüpheli; cevaplar proposal.cevap_secenekleri). 3 cevaptan ikisi aynıysa o şık öneri olur, değilse boş kalır.

Güvenli yazım: her 10 soruda inceleme dosyası yeniden okunur, yalnız hâlâ 'review_required' olan kayıtlar güncellenir
(sayfadan aynı anda yapılan onay/ret kaybolmaz). Kullanım: phase14_belirsiz_gemini.py [--limit N]
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase14_cloud_question_editor as P14  # noqa: E402

F = P14.REVIEWS_FILE


def hedef_mi(r: dict) -> bool:
    p = r.get("proposal") or {}
    d = p.get("cevap_dogrulama") or {}
    return (r.get("status") == "review_required" and not p.get("cevap_secenekleri")
            and (bool(p.get("cevap_belirsiz")) or d.get("sonuc") in ("belirsiz", "ayni_model_iki_oy_gecersiz")))


def uygula(sonuclar: dict[str, dict]) -> int:
    """Dosyayı yeniden okuyup yalnız hâlâ bekleyen kayıtları günceller (kilitli, atomik)."""
    if not sonuclar:
        return 0
    with P14._KILIT, P14.dosya_kilidi():
        rows = [json.loads(l) for l in F.read_text(encoding="utf-8").splitlines() if l.strip()]
        n = 0
        for r in rows:
            yeni = sonuclar.get(str(r.get("question_id")))
            if yeni and r.get("status") == "review_required":
                r["proposal"] = yeni
                r["suspicious"] = True
                r["suspicious_at"] = datetime.utcnow().isoformat() + "Z"
                r["answer_doubtful"] = True
                n += 1
        tmp = F.with_suffix(".jsonl.tmp")
        tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        os.replace(tmp, F)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    rows = [json.loads(l) for l in F.read_text(encoding="utf-8").splitlines() if l.strip()]
    hedefler = [r for r in rows if hedef_mi(r)]
    if a.limit:
        hedefler = hedefler[: a.limit]
    logging.info(f"Belirsiz kayıt: {len(hedefler)} → Gemini ile yeniden sorgulanacak")
    bekleyen: dict[str, dict] = {}
    toplam = cogunluk = 0
    for i, r in enumerate(hedefler, 1):
        src, prop = dict(r.get("source") or {}), dict(r.get("proposal") or {})
        try:
            P14.belirsizi_gemini_ile_tamamla(src, prop)
        except Exception as e:  # noqa: BLE001
            logging.warning(f"#{r.get('question_id')} hata: {e}")
            continue
        if not prop.get("cevap_secenekleri"):
            continue
        cogunluk += bool(prop.get("dogru_secenek"))
        bekleyen[str(r["question_id"])] = prop
        if len(bekleyen) >= 10 or i == len(hedefler):
            toplam += uygula(bekleyen)
            bekleyen = {}
            logging.info(f"[{i}/{len(hedefler)}] yazıldı: {toplam} · çoğunluk bulunan: {cogunluk}")
    toplam += uygula(bekleyen)
    logging.info(f"Bitti: {toplam} kayıt şüpheli olarak işaretlendi; {cogunluk} soruda 3 cevaptan ikisi aynı şıkta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
