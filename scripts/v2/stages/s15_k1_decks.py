"""Kurul 1 ders paketlerini (meds_database_v2/kurul1_ders_paketleri) Öğren sayfasının
etkileşimli deste biçimine (src/data/interactive_learning_decks.json) dönüştürür.

Her ders için bir deste: 1. slayt ders özeti, ardından paketteki öğrenim slaytları
(kartlar → flashcards, spotlar → spotPearls), sonda bilgi paketi (anlam → sonuç) ve
ders notundaki çıkmış sorular. Mevcut desteler korunur; yalnız `k1p-` önekli
desteler yenilenir. Yazmadan önce kaynak dosya yedeklenir.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime

from .. import config
from ..core import store

PAKET_DIR = config.PROJECT_ROOT / "meds_database_v2" / "kurul1_ders_paketleri"
NOT_DIR = config.TEMP_DIR / "study" / "k1"
DECKS_JSON = config.MEDS_DIR / "src" / "data" / "interactive_learning_decks.json"
PREFIX = "k1p-"
COMMITTEE = "Kurul 1 - Ürogenital ve Obstetrik Kurulu"
RENK = {"Tıbbi Patoloji": "rose", "Tıbbi Genetik": "violet", "Halk Sağlığı": "emerald",
        "Enfeksiyon Hastalıkları": "amber", "Üroloji": "sky", "Kadın Hastalıkları ve Doğum": "pink",
        "Tıbbi Farmakoloji": "indigo"}

_SORU = re.compile(r"^### Soru \d+:\s*\[(?P<etiket>[^\]]*)\]\s*\n(?P<govde>.*?)(?=^### Soru |^## |\Z)", re.S | re.M)


def _sorular(md: str, ders: str, konu: str) -> list[dict]:
    out = []
    for i, m in enumerate(_SORU.finditer(md), 1):
        g = m.group("govde")
        kok = re.search(r"\*\*Soru / Öncül:\*\*\s*(.+)", g)
        secenek = re.findall(r"^- \*\*([A-E])\)\*\*\s*(.+)$", g, flags=re.M)
        cevap = re.search(r"\*\*Doğru Cevap:\*\*\s*([A-E])\b", g)
        aciklama = re.search(r"Çözüm Notu:\*\*\s*(.+?)\s*(?:</details>|$)", g, flags=re.S)
        if not (kok and len(secenek) >= 2 and cevap):
            continue
        c = cevap.group(1)
        out.append({
            "id": f"q{i}", "examYear": m.group("etiket"), "committeeId": "kurul1", "discipline": ders,
            "topic": konu, "stem": kok.group(1).strip(),
            "options": [{"key": k, "text": t.strip(), "isCorrect": k == c} for k, t in secenek],
            "correctAnswer": c, "explanation": (aciklama.group(1).strip() if aciklama else ""),
        })
    return out


def _baslik_duzelt(md: str) -> str:
    """Deste görünümü yalnız `###` başlıkları tanır; `#`/`##` başlıkları `###` yapılır."""
    return re.sub(r"^#{1,2}\s+", "### ", md or "", flags=re.M)


def _slayt(no: int, baslik: str, alt: str, rozet: str, icerik: str, kartlar=None, spot=None, **extra) -> dict:
    icerik = _baslik_duzelt(icerik)
    return {
        "slideNumber": no, "title": baslik, "subtitle": alt, "badge": rozet, "badgeColor": extra.pop("renk", "sky"),
        "synthesisNarrative": icerik, "content": icerik,
        "flashcards": [{"id": f"s{no}-k{j}", "category": rozet, "front": k.get("on", ""), "hint": k.get("ipucu", ""),
                        "back": k.get("arka", ""), "question": k.get("on", ""), "answer": k.get("arka", "")}
                       for j, k in enumerate(kartlar or [], 1)],
        "coreContent": extra.pop("core", {}), "spotPearls": list(spot or []),
        "relatedQuestions": extra.pop("sorular", []), "aiPromptSuggestions": [], **extra,
    }


def deste(p: dict) -> dict:
    ders, konu = p["ders"], p["konu"]
    renk = RENK.get(ders, "sky")
    oz = p.get("ders_ozeti") or {}
    noktalar = list(oz.get("anahtar_noktalar") or [])
    slaytlar = [_slayt(1, oz.get("baslik") or konu, "Ders özeti", "Özet", oz.get("ozet", ""), spot=noktalar[:4], renk=renk)]
    for s in p.get("ogrenim_slaytlari") or []:
        slaytlar.append(_slayt(len(slaytlar) + 1, s.get("baslik", ""), s.get("altBaslik", ""), s.get("rozet", ""),
                               s.get("icerik", ""), s.get("kartlar"), s.get("spotlar"), renk=renk))
    bp = p.get("bilgi_paketi") or []
    if bp:
        satir = "\n".join(f"- **{b['bilgi']}:** {b['anlam']} → {b['sonuc']}" for b in bp)
        slaytlar.append(_slayt(len(slaytlar) + 1, "Bilgi Paketi", "Anlam → sonuç ilişkisi, kazanıma bağlı", "Bilgi paketi",
                               satir, renk=renk, core={"keyBullets": [
                                   {"title": b["bilgi"], "desc": f"{b['anlam']} → {b['sonuc']}", "isKey": b.get("onem") == "yuksek"}
                                   for b in bp]}))
    not_dosya = next(NOT_DIR.glob(f"{p['id'][3:5]}_*.md"), None)
    sorular = _sorular(not_dosya.read_text(encoding="utf-8"), ders, konu) if not_dosya else []
    if sorular:
        slaytlar.append(_slayt(len(slaytlar) + 1, "Çıkmış Sorular", f"{len(sorular)} Kurul 1 sorusu", "Çıkmış soru",
                               "Bu derse ait çıkmış Kurul 1 soruları.", renk=renk, sorular=sorular))
    ozet = oz.get("ozet", "")
    giris = re.sub(r"[#*=]", "", ozet.split("\n## ")[0] if ozet else "").strip()
    return {
        "deckId": PREFIX + p["id"], "id": PREFIX + p["id"], "title": konu, "shortTitle": konu[:40],
        "discipline": ders, "committee": COMMITTEE, "instructor": p.get("ogretim_uyesi", ""),
        "audioFile": "", "audioDuration": "", "confidence": "high", "themeColor": renk,
        "matchedNoteId": p["id"], "matchedNoteTitle": konu,
        "overview": (giris[:700] or konu) + (" (Kaynak: geçen yılın ders sunumu.)" if p.get("gecen_yil_kaynagi") else ""),
        "highYieldPearls": noktalar[:6], "slides": slaytlar, "totalSlides": len(slaytlar),
        "matchedPastQuestionsCount": len(sorular), "category": "Kurul 1 · 2026-2027 ders paketi",
        "programDate": p.get("tarih"), "kazanimlar": p.get("kazanimlar") or [],
    }


def run(log=print) -> dict:
    paketler = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(PAKET_DIR.glob("k1-*.json"))]
    yeni = [deste(p) for p in paketler]
    mevcut = store.read_json(DECKS_JSON, []) or []
    if not yeni:
        return {"deste": 0}
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = config.PROJECT_ROOT / "yedek" / "desteler" / stamp
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DECKS_JSON, dst / DECKS_JSON.name)
    korunan = [d for d in mevcut if not str(d.get("id", "")).startswith(PREFIX)]
    store.atomic_write_json(DECKS_JSON, korunan + yeni, indent=1)
    rapor = {"deste": len(yeni), "korunan": len(korunan), "slayt": sum(d["totalSlides"] for d in yeni),
             "soru": sum(d["matchedPastQuestionsCount"] for d in yeni), "yedek": str(dst)}
    log(json.dumps(rapor, ensure_ascii=False))
    return rapor
