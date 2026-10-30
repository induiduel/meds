"""Öğrenci önem notları (geçmiş yıl öğrenci derlemeleri) — ortak yollar ve puanlama.

Kaynak: Dönem 3 Kurul 2 öğrenci derleme PDF'leri (psk3.2, nöro3.2, tbg3.2, ftr3.2; 2025-26 slaytlarından kesilmiş önemli
yerler + el yazısı + yapıştırılmış çıkmış sorular). Ham okuma: data/ogrenci_onem/ham/<pdf>_sNN.json (sayfa görüntüsünden,
iki geçişli). Yöntem ve sınırlar: docs/OGRENCI_ONEM_YONTEMI.md.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]  # meds/
HAM = KOK / "data/ogrenci_onem/ham"
CIKTI = KOK / "src/data/ogrenci_onem"
DOC = KOK / "docs/OGRENCI_ONEM"
PAST = KOK / "src/data/pastQuestions.json"
DERSLER = KOK / "src/data/dersler/k2.json"
Y25_PDF = KOK.parent / "meds_database_25_26/pdf/kurul2"

PDF_BRANS = {"psk": "Psikiyatri", "noro": "Nöroloji", "tbg": "Tıbbi Genetik", "ftr": "FTR"}

# Sinyal ağırlıkları (puan 0–100'e kırpılır). Gerekçe ve sınama: docs/OGRENCI_ONEM_YONTEMI.md §3.
AGIRLIK = {
    "cikmis": 40,        # öğrenci bu bloğa çıkmış soru yapıştırdı / blok çıkmış sorunun dayanağı
    "banka_cikmis": 30,  # bankadaki doğrulanmış bir çıkmış bu bloğa eşleşiyor (ilk eşleşme; her ek soru +5)
    "el_cikmis": 20,     # el yazısıyla "çıkmış" notu
    "el_sorarim": 20,    # hoca "sorarım/buraya çalışın" (el notu)
    "yildiz": 15, "unlem": 10,
    "tekrar": 10,        # aynı bilgi notta birden çok yerde
    "sari": 10, "yesil": 10, "pembe": 10,
    "el_onemli": 8,      # el yazısıyla açıklama/ek bilgi (öğrenci üstünde durmuş)
    "daire": 5, "kirmizi_cizgi": 5, "kutu": 5,
}
ESIK_A, ESIK_B = 55, 18  # A: çıkmış kanıtlı; B: vurgu + el notu; C: notta seçilmiş, az işaretli; (notta yok = D)


def norm(t: str) -> str:
    t = unicodedata.normalize("NFC", t or "").replace("İ", "i").replace("I", "ı").lower()
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-zçğıöşüâîû%/ ]", " ", t)).strip()


def jetonlar(t: str) -> set[str]:
    return {w for w in norm(t).split() if len(w) > 2}


def oku_json(p: Path, varsayilan=None):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return varsayilan


def ders_kaydi() -> dict[str, dict]:
    return {d["id"]: d for d in json.loads(DERSLER.read_text())["dersler"]}


def oncelik(puan: int, cikmis_kanit: bool = False, guclu_isaret: bool = False) -> str:
    """A: çıkmış kanıtı (notta yapıştırılmış ya da bankadaki çıkmış eşleşmesi) ya da puan ≥ ESIK_A.
    B: puan ≥ ESIK_B ya da yıldız/ünlem/"sorarım"/"çıkmış" el notu. C: geri kalan (yalnız kapsam)."""
    if cikmis_kanit or puan >= ESIK_A:
        return "A"
    return "B" if puan >= ESIK_B or guclu_isaret else "C"


ISARET_ACIKLAMA = re.compile(r"\s*\((?:[^()]*\b(?:kırmızı|pembe|sarı|yeşil|mavi|yıldız|çerçeve|daire|vurgu|altı çizili|ok)\b[^()]*)\)", re.I)
ISARET_TARIFI = re.compile(r"\b(satır\w*|tamamı|çerçeve\w*|maddenin|maddeler\w*|başlığı|altı çizili)\b", re.I)
_PAST: dict | None = None


def banka_dogru_metni(qid: str | None) -> str:
    global _PAST
    if not qid:
        return ""
    if _PAST is None:
        _PAST = {q["id"]: q for q in json.loads(PAST.read_text())}
    q = _PAST.get(qid) or {}
    return next((o.get("text", "") for o in q.get("options") or [] if o.get("isCorrect")), "")


def cikmis_cevap(c: dict) -> str:
    """Yapıştırılmış çıkmışın doğru cevabı METİN olarak: önce banka doğru şıkkının harfi notun şıklarında, sonra bankanın
    doğru şık metni, en son öğrencinin işareti."""
    harf = (c.get("banka_dogru") or c.get("ogrenci_cevap") or "").strip()
    h1 = harf[:1].upper()
    sik = next((s for s in c.get("siklar") or [] if re.match(rf"^\s*{re.escape(h1)}\s*[)\.\-]", s, re.I)), "") if h1 else ""
    if sik:
        return re.sub(r"^\s*\w\s*[)\.\-]\s*", "", sik).strip()
    return banka_dogru_metni(c.get("banka_id")) or harf


def bilgiler(b: dict, ders: dict | None = None) -> list[dict]:
    """Birimin tekil bilgi parçaları: el notu (hedef satırıyla), vurgulu satır, notta yapıştırılmış/bankadaki çıkmışın
    doğru önermesi. Kapı ve işçi özeti bunları cümle düzeyinde arar (konu benzerliği bilgi kapsamı değildir)."""
    out, gor = [], set()

    def ekle(tur: str, metin: str, cevap: str = ""):
        m = re.sub(r"\s+", " ", (metin or "")).strip(" -→=")
        if tur == "vurgu" and ISARET_TARIFI.search(m):
            return  # "üç satırın tamamı", "sarı çerçeveli" gibi işaret tarifi bilgi değildir
        if len(m) >= 6 and norm(m) not in gor:
            gor.add(norm(m)); out.append(dict(tur=tur, metin=m, **({"cevap": cevap} if cevap else {})))

    for e in b.get("el_yazisi") or []:
        if e.get("guven") == "dusuk":
            continue
        h = (e.get("hedef") or "").strip()
        ekle("el", f"{h}: {e.get('metin', '')}" if h and len(h) < 80 else e.get("metin", ""))
    for v in b.get("vurgulu") or []:
        ekle("vurgu", ISARET_ACIKLAMA.sub("", v))
    if ders:
        ogr = {c["id"]: c for c in ders.get("ogrenci_sorulari") or []}
        for cid in b.get("ogrenci_sorulari") or []:
            c = (ogr.get(cid) or {}).get("cikmis") or {}
            cevap = cikmis_cevap(c)
            if c.get("kok"):
                ekle("cikmis", f"{c['kok']} → {cevap}", cevap)
        bk = {r["id"]: r for r in ders.get("banka") or []}
        for qid in b.get("banka_cikmis") or []:
            r = bk.get(qid)
            if r:
                ekle("cikmis", f"{r['kok']} → {r['dogru']}", r["dogru"])
    return out


def cumleler(t: str) -> list[str]:
    t = re.sub(r"[#*>\[\]!]", " ", t or "")
    return [c.strip() for c in re.split(r"(?<=[.!?:])\s+|\n+", t) if len(c.strip()) > 15]
