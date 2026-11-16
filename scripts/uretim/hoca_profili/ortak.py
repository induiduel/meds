"""Hoca üslubu hattı ortak işlevleri (LLM yok, yalnız standart kütüphane).

Soru → özellik: kök kalıbı, bilgi türü, bilişsel düzey, şık yapısı, çeldirici stratejisi.
Metin → ortak kök-jeton (Türkçe ek gürültüsünü 5 harf önekle törpüler).
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

KOK = _kok.MEDS
PAST = _kok.CIKMIS
CIKTI = KOK / "src/data/hoca_profilleri"
DOC = KOK / "docs/HOCA_USLUBU"

TR = str.maketrans("ÇĞİÖŞÜçğıöşü", "cgiosucgiosu")


def slug(s: str) -> str:
    s = (s or "").translate(TR).lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_") or "x"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().replace("İ", "i").replace("I", "ı")).strip()


DURAK = set("ve veya ile için bir bu şu o de da ki mi mı mu mü olan olarak daha çok en gibi ise ama fakat ancak hangi hangisi hangileri aşağıdakilerden aşağıdaki doğru yanlış değildir olduğu olan arasında sonra önce her tüm göre kadar nedeniyle sırasıyla ifade ifadelerden hasta hastada yaşında erkek kadın".split())


def jetonlar(s: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-zçğıöşüâîû0-9]+", norm(s)):
        if w in DURAK or len(w) < 3:
            continue
        out.append(w[:5])
    return out


def yil_no(y) -> int | None:
    m = re.match(r"(20\d\d)-(20\d\d)", str(y or ""))
    if not m or m.group(2) == "2026" and m.group(1) == "2021":  # '2021-2026' derleme etiketi, yıl değil
        return None
    return int(m.group(1))


# ---------------------------------------------------------------- kök kalıbı
KALIP_KURALLARI = [
    ("onculu", r"\bi{1,3}\.|\biv\.|öncül|ifadelerden hangileri|hangileri doğru|hangileri yanlış"),
    ("vaka", r"\d+\s*(yaşında|aylık|haftalık|günlük)|yaşındaki|başvur|kliniğe|acile|şikayet|şikâyet|muayenesinde|öyküsü"),
    ("eslestirme", r"eşleş|ilişkilendir|hangi .* hangi"),
    ("yanlis_bul", r"yanlış olan|doğru olmayan|söylenemez|yanlıştır\??$"),
    ("olumsuz", r"değildir|beklenmez|olamaz|dışında|görülmez|bulunmaz|yoktur|katkıda bulunmaz|etkilemez|yapmaz|değil\b"),
    ("en_tipik", r"\ben (sık|olası|karakteristik|tipik|önemli|yaygın|belirgin|sık neden|uygun|etkili|güvenilir|erken|geç)|ilk (basamak|seçenek|tercih|olarak)|en iyi"),
    ("dogru_ifade", r"doğru(dur)?\??$|ifade(si)? .*doğru|doğrudur"),
    ("tanim", r"nedir\??$|neye denir|tanımı|denir\??$|olarak adlandır"),
    ("sayi", r"kaç|yüzde|%|oranı|süre(si)?|dozu|kaç yıl"),
]


def kok_kalibi(kok: str) -> str:
    k = norm(kok)
    for ad, rx in KALIP_KURALLARI:
        if re.search(rx, k):
            return ad
    return "dogrudan"


# ---------------------------------------------------------------- bilgi türü ("neden sorulur")
BILGI_TURLERI = [
    ("tanimlayici_bulgu", r"patognomonik|tanı koydurucu|karakteristik|tipik bulgu|histopatolojik|mikroskop|görünüm|boyanma|inklüzyon|hücre(si|ler)?i? .*görül|morfolo"),
    ("mekanizma", r"mekanizma|nasıl|nedeniyle|yol açar|sonucu|neden olur|inhibe|bağlan|aktivasyon|sentez|yolak|reseptör|etki ederek|artış|azal"),
    ("ilac_yan_etki", r"yan etki|advers|toksisite|toksik|istenmeyen|kontrendike|teratojen"),
    ("ilac_endikasyon", r"endikasyon|tedavisinde|kullanılır|tercih edil|ilk seçenek|ilk basamak|tedavi"),
    ("tani_ayirici", r"tanı|ayırıcı|ayırt|tanısında|belirteç|marker|test|kriter|skor|görüntüleme"),
    ("etiyoloji_risk", r"etken|neden(i)?|risk faktör|etiyoloji|predispoz|sebep|bulaş|mikroorganizma|bakteri|virüs"),
    ("siniflama_ad", r"sınıf|tip(i)?\b|evre|derece|grade|gruba|alt tip|eponim|sendromu|hastalığı"),
    ("epidemiyoloji_sayi", r"sıklık|insidans|prevalans|yaş grubu|oran|%|yüzde|cinsiyet|epidemiyo"),
    ("onleme_halk_sagligi", r"önleme|koruma|tarama|aşı|korunma|sağlık eğitimi|birincil|ikincil|üçüncül"),
    ("prognoz_komplikasyon", r"komplikasyon|prognoz|metastaz|sonuç olarak|seyir|mortalite|ölüm"),
]


def bilgi_turu(kok: str, dogru: str) -> str:
    t = norm(kok + " " + dogru)
    skor = {ad: len(re.findall(rx, t)) for ad, rx in BILGI_TURLERI}
    ad, v = max(skor.items(), key=lambda x: x[1])
    return ad if v > 0 else "tanim_kavram"


def bilissel_duzey(kalip: str, tur: str, kok: str) -> str:
    """Bloom'dan türetilmiş 3 düzey: L1 hatırlama, L2 anlama/ilişki, L3 uygulama/klinik muhakeme."""
    if kalip == "vaka":
        return "L3_uygulama"
    if kalip in ("onculu", "eslestirme", "yanlis_bul") or tur in ("mekanizma", "tani_ayirici", "prognoz_komplikasyon"):
        return "L2_anlama_iliski"
    if kalip == "en_tipik" and tur in ("ilac_endikasyon", "etiyoloji_risk"):
        return "L2_anlama_iliski"
    return "L1_hatirlama"


# ---------------------------------------------------------------- şık yapısı
MUTLAK = r"\b(her zaman|asla|hiçbir|tamamen|yalnızca|sadece|daima|mutlaka|kesinlikle|tümü)\b"


def sik_ozellik(siklar: list[str], dogru_i: int) -> dict:
    uz = [len(s.split()) for s in siklar]
    ort = sum(uz) / len(uz)
    sd = (sum((u - ort) ** 2 for u in uz) / len(uz)) ** 0.5
    dogru_uz = uz[dogru_i]
    en_uzun = dogru_uz == max(uz) and uz.count(max(uz)) == 1 and max(uz) >= 3
    bilesik = sum(1 for s in siklar if re.search(r"\+| ve | ile |→|;|,", s)) / len(siklar)
    sayisal = sum(1 for s in siklar if re.search(r"\d", s)) / len(siklar)
    mutlak_d = sum(1 for i, s in enumerate(siklar) if i != dogru_i and re.search(MUTLAK, norm(s)))
    mutlak_c = 1 if re.search(MUTLAK, norm(siklar[dogru_i])) else 0
    hep = any(re.search(r"hepsi|hiçbiri|yukarıdakilerin", norm(s)) for s in siklar)
    # çeldirici-doğru jeton örtüşmesi: komşu kavram yakınlığı
    jd = set(jetonlar(siklar[dogru_i]))
    ort_j = []
    for i, s in enumerate(siklar):
        if i == dogru_i:
            continue
        js = set(jetonlar(s))
        if jd and js:
            ort_j.append(len(jd & js) / len(jd | js))
    return dict(kelime_ort=ort, kelime_cv=(sd / ort if ort else 0), dogru_en_uzun=en_uzun, bilesik=bilesik, sayisal=sayisal,
                mutlak_celdirici=mutlak_d, mutlak_dogru=mutlak_c, hepsi_hicbiri=hep,
                celdirici_ortusme=(sum(ort_j) / len(ort_j) if ort_j else 0.0), dogru_oran=dogru_uz / ort if ort else 1.0)


def celdirici_stratejisi(f: dict) -> list[str]:
    s = []
    if f["sayisal"] >= 0.8:
        s.append("sayisal_yakin_deger")
    if f["bilesik"] >= 0.6:
        s.append("bilesik_yer_degistirmeli")
    if f["mutlak_celdirici"] >= 1:
        s.append("mutlak_ifade_tuzagi")
    if f["celdirici_ortusme"] >= 0.25:
        s.append("ayni_ailede_komsu_kavram")
    if not s:
        s.append("ayni_turden_ayri_kavram")
    return s


def soru_yukle() -> list[dict]:
    """Çıkmış sorular, tekilleştirilmiş (aynı kök+doğru şık = tek kayıt; kez + yıl listesi tutulur)."""
    ham = json.loads(PAST.read_text())
    tekil: dict[str, dict] = {}
    for q in ham:
        if not q.get("isPastExam") or not q.get("stem"):
            continue
        ops = q.get("options") or []
        if len(ops) < 4:
            continue
        dogru_i = next((i for i, o in enumerate(ops) if o.get("isCorrect")), None)
        if dogru_i is None:
            ca = (q.get("correctAnswer") or "").strip().upper()
            dogru_i = next((i for i, o in enumerate(ops) if (o.get("key") or "").upper() == ca), None)
        if dogru_i is None:
            continue
        siklar = [o.get("text") or "" for o in ops]
        anah = norm(q["stem"])[:160] + "|" + norm(siklar[dogru_i])[:80]
        yil = yil_no(q.get("examYear"))
        e = tekil.get(anah)
        if e is None:
            kalip = kok_kalibi(q["stem"])
            tur = bilgi_turu(q["stem"], siklar[dogru_i])
            sf = sik_ozellik(siklar, dogru_i)
            e = dict(id=q["id"], ders=q.get("discipline") or "?", konu=q.get("topic") or "?", kok=q["stem"], siklar=siklar,
                     dogru_i=dogru_i, kalip=kalip, tur=tur, duzey=bilissel_duzey(kalip, tur, q["stem"]), sf=sf,
                     strateji=celdirici_stratejisi(sf), yillar=[], kurul=q.get("kurul"),
                     ozet=(q.get("ozetKaniti") or {}), kok_kelime=len(q["stem"].split()))
            tekil[anah] = e
        e["yillar"].append(yil)
    for e in tekil.values():
        e["kez"] = len(e["yillar"])
        e["yil_set"] = sorted({y for y in e["yillar"] if y})
    return list(tekil.values())
