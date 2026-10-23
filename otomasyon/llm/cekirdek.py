"""Görev sözleşmesinin ortak çekirdeği (ICERIK_MOTORU_V3.md §14).

Bir LLM işi = görev (gorevler.json kaydı + gorevler/<id>.py modülü) × hedef (kimlik). Çekirdek şunları sağlar:
  - iş klasörü `meds_temp/gorev/<is_id>/` (paket.md, paket.json, durum.json, cevap_N.txt, cikti.json, rapor.json),
  - modelden bağımsız paket biçimi (GÖREV · KURALLAR · GİRDİ · BAĞLAM · ÇIKTI BİÇİMİ · DENETİM LİSTESİ),
  - kısa etiket eşlemesi (S1 ↔ k2-07-c0142), JSON ayıklama, günlük.
Aynı görev + aynı girdi → bayt bayt aynı paket → aynı is_id (yeniden çalıştırma idempotent, önbellek anahtarı).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib
import json
import os
import re
import sys
from pathlib import Path

Path = Path  # yönlendirici c.Path kullanır

KOK = Path(__file__).resolve().parents[2]                     # meds/
LLM = KOK / "otomasyon" / "llm"
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or KOK.parent / "meds_temp")
IS_DIZIN = Path(os.environ.get("MEDS_GOREV_DIR") or TEMP / "gorev")
ONBELLEK = TEMP / "llm_onbellek"
DB2 = KOK.parent / "meds_database_v2"
for p in (KOK / "scripts", KOK / "scripts" / "agents"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

DURUMLAR = ("hazir", "cevap_var", "derlendi", "dogrulandi", "uygulandi", "reddedildi", "elle_bekliyor", "bekliyor_butce")


def oku(p: Path, varsayilan=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return varsayilan


def yaz(p: Path, veri):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    gecici = p.with_suffix(p.suffix + ".tmp")
    gecici.write_text(json.dumps(veri, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    gecici.replace(p)


def sha(s: str, n: int = 10) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]


def simdi() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


# ── defter ve modüller ────────────────────────────────────────────────────────────────────────────────────────────
def defter() -> dict:
    d = oku(LLM / "gorevler.json", {})
    return {g["id"]: g for g in d.get("gorevler", [])}


def kayit(gorev: str) -> dict:
    k = defter().get(gorev)
    if not k:
        raise SystemExit(f"tanımsız görev: {gorev} (otomasyon/llm/gorevler.json)")
    return k


def modul(gorev: str):
    kayit(gorev)
    return importlib.import_module(f"llm.gorevler.{gorev}")


def kurallar(adlar: list[str]) -> list[str]:
    """kurallar/<ad>.md parçaları; her satırı '- ' ile başlayan madde. Sıra korunur, tekrar atılır."""
    out: list[str] = []
    for ad in adlar:
        p = LLM / "kurallar" / f"{ad}.md"
        if not p.exists():
            raise SystemExit(f"kural parçası yok: {p}")
        for satir in p.read_text(encoding="utf-8").splitlines():
            satir = satir.strip()
            if satir.startswith("- ") and satir[2:] not in out:
                out.append(satir[2:])
    return out


# ── kısa etiketler ────────────────────────────────────────────────────────────────────────────────────────────────
class Etiketler:
    """Uzun kimlik ↔ kısa etiket (S1, R2, Q3 …). Model yalnız kısa etiket görür ve yazar."""

    def __init__(self, esleme: dict | None = None):
        self.esleme: dict[str, str] = dict(esleme or {})
        self._ters = {v: k for k, v in self.esleme.items()}

    def ekle(self, onek: str, uzun: str) -> str:
        if uzun in self._ters:
            return self._ters[uzun]
        n = sum(1 for k in self.esleme if re.fullmatch(rf"{onek}\d+", k)) + 1
        k = f"{onek}{n}"
        self.esleme[k] = uzun
        self._ters[uzun] = k
        return k

    def uzun(self, kisa: str) -> str | None:
        return self.esleme.get(kisa.strip())

    def kisa(self, uzun: str) -> str | None:
        return self._ters.get(uzun)


# ── paket ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def paket_md(p: dict) -> str:
    """p: amac, kurallar (ad listesi), ek_kurallar, girdi, baglam, cikti_bicimi, denetim_listesi."""
    kur = kurallar(p.get("kurallar", [])) + list(p.get("ek_kurallar", []))
    parca = [
        "# GÖREV", p["amac"].strip(), "",
        "# KURALLAR", *[f"{i}. {k}" for i, k in enumerate(kur, 1)], "",
        "# GİRDİ", p["girdi"].strip(), "",
    ]
    if p.get("baglam"):
        parca += ["# BAĞLAM (yalnız okumak için; buradan soru/bilgi üretme)", p["baglam"].strip(), ""]
    parca += ["# ÇIKTI BİÇİMİ", p["cikti_bicimi"].strip(), "",
              "# DENETİM LİSTESİ (cevabın betikle bunlara göre denetlenir; göndermeden önce kendin sına)",
              *[f"- {m}" for m in p.get("denetim_listesi", [])], "",
              "Yalnız istenen çıktıyı yaz; açıklama, selamlama ya da kod bloğu dışında metin ekleme."]
    return "\n".join(parca).rstrip() + "\n"


def kelime_say(s: str) -> int:
    return len(re.findall(r"\w+", s or ""))


# ── iş klasörü ────────────────────────────────────────────────────────────────────────────────────────────────────
def is_klasoru(is_id: str) -> Path:
    d = IS_DIZIN / is_id
    if not d.exists():
        raise SystemExit(f"iş yok: {is_id} ({d})")
    return d


def is_ac(gorev: str, hedef: str, hazir: dict) -> str:
    """Paketi yazar; aynı paket zaten varsa aynı işi döndürür (durumu korunur)."""
    md = paket_md(hazir)
    k = kayit(gorev)
    sinir = int(k.get("girdi_sinir_kelime", 6000))
    if kelime_say(md) > sinir:
        raise SystemExit(f"paket {kelime_say(md)} kelime > sınır {sinir} — hedefi böl ({gorev} {hedef})")
    guvenli = re.sub(r"[^0-9a-z-]+", "-", hedef.lower()).strip("-")[:60]
    is_id = f"{gorev}--{guvenli}--{sha(md, 8)}"
    d = IS_DIZIN / is_id
    if (d / "durum.json").exists():
        return is_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "paket.md").write_text(md, encoding="utf-8")
    yaz(d / "paket.json", {"gorev": gorev, "hedef": hedef, "esleme": hazir.get("esleme", {}),
                           "meta": hazir.get("meta", {}), "girdi_metni": hazir["girdi"], "paket_sha": sha(md, 16)})
    durum_yaz(is_id, durum="hazir", gorev=gorev, hedef=hedef, olusturuldu=simdi())
    return is_id


def paket(is_id: str) -> tuple[str, dict]:
    d = is_klasoru(is_id)
    return (d / "paket.md").read_text(encoding="utf-8"), oku(d / "paket.json", {})


def durum(is_id: str) -> dict:
    return oku(is_klasoru(is_id) / "durum.json", {})


def durum_yaz(is_id: str, **alan) -> dict:
    p = IS_DIZIN / is_id / "durum.json"
    d = oku(p, {}) or {}
    if "durum" in alan and alan["durum"] not in DURUMLAR:
        raise ValueError(alan["durum"])
    d.update(alan)
    d["guncellendi"] = simdi()
    yaz(p, d)
    return d


def gunluk(**kayit_):
    IS_DIZIN.mkdir(parents=True, exist_ok=True)
    with open(IS_DIZIN / "gunluk.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"zaman": simdi(), **kayit_}, ensure_ascii=False) + "\n")


# ── cevap ayıklama ────────────────────────────────────────────────────────────────────────────────────────────────
def json_cikar(cevap):
    """Model cevabından ilk dengeli JSON nesnesini çıkarır (kod bloğu, önsöz, <think> toleranslı). Bulamazsa None."""
    if isinstance(cevap, (dict, list)):
        return cevap
    s = re.sub(r"<think>.*?</think>", "", cevap or "", flags=re.S)
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", s, flags=re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except ValueError:
            pass
    bas = s.find("{")
    while bas != -1:
        derin, dizide, kac = 0, False, False
        for i in range(bas, len(s)):
            c = s[i]
            if dizide:
                if kac:
                    kac = False
                elif c == "\\":
                    kac = True
                elif c == '"':
                    dizide = False
            elif c == '"':
                dizide = True
            elif c == "{":
                derin += 1
            elif c == "}":
                derin -= 1
                if derin == 0:
                    try:
                        return json.loads(s[bas:i + 1])
                    except ValueError:
                        break
        bas = s.find("{", bas + 1)
    return None


# ── ortak metin yardımcıları (kapılar) ────────────────────────────────────────────────────────────────────────────
_KATLA = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")
DOLGU = set("aşağıdaki aşağıdakilerden hangisi hangisidir değildir olan olarak ile için veya gibi daha en çok az bir "
            "birlikte sonucu nedeniyle durumu durumunda özelliği yalnız".split())


def katla(s: str) -> str:
    return (s or "").replace("İ", "i").replace("I", "ı").lower().translate(_KATLA)


def kokler(s: str, en_az: int = 4) -> set[str]:
    """Türkçe katlanmış 5 harf kökler (≥ en_az harfli, dolgu ve sayı dışı) — sözcüksel dayanak denetimi için."""
    out = set()
    for w in re.findall(r"[0-9a-zçğıöşüâîû]+", (s or "").replace("İ", "i").replace("I", "ı").lower()):
        if len(w) < en_az or w.isdigit() or w in DOLGU:
            continue
        out.add(katla(w)[:5])
    return out


def sayilar(s: str) -> set[str]:
    return set(re.findall(r"\d+(?:[.,]\d+)?", s or ""))


# ── ortak kapı: iç etiket sızıntısı (H31) ──────────────────────────────────────────────────────────────────────────
ETIKET_MUAF_ALAN = {"yer", "not"}   # denetim bulgusu "yer", elenen çıkmış "not" (iç iz) etikete gönderme yapabilir


def etiket_sizintisi(cikti, esleme: dict, paket_md: str = "") -> list[str]:
    """Derlenmiş çıktının öğrenci metinlerinde kalmış kısa etiketler (Q3, L12 …). Derleyici etiket alanlarını uzun kimliğe
    çevirdiğinden metinde kalan etiket sızıntıdır. Yalnız bu pakette verilmiş etiketler sayılır; girdide satır başı dışında
    da geçen (S1 kalp sesi, L4 omur gibi tıbbi kullanım) etiketler muaftır. `_` ile başlayan iç alanlar ve "yer" atlanır."""
    kisa = set((esleme or {}).keys())
    if not kisa:
        return []
    tibbi = set()
    for t in kisa:
        hepsi = len(re.findall(rf"(?<![\w-]){re.escape(t)}(?![\w-])", paket_md))
        bas = len(re.findall(rf"(?m)^\s*(?:[-*]\s*)?{re.escape(t)}(?![\w-])", paket_md))
        if hepsi > bas + (paket_md.count(f"[{t}]")):
            tibbi.add(t)
    out = []

    def gez(x, yol):
        if isinstance(x, dict):
            for k, v in x.items():
                if not str(k).startswith("_") and k not in ETIKET_MUAF_ALAN:
                    gez(v, f"{yol}.{k}" if yol else str(k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                gez(v, f"{yol}[{i}]")
        elif isinstance(x, str):
            for t in re.findall(r"(?<![\w-])([A-Z]\d{1,3})(?![\w-])", x):
                if t in kisa and t not in tibbi:
                    out.append(f"{yol}: iç etiket ({t}) öğrenci metninde — etiketi kaldır, bilgiyi kendi cümlenle yaz")
                    break
    gez(cikti, "")
    return out


# ── betik onarımı: ses alanlarında kısaltma/Roma rakamı okunuşu (B katmanı; modelin uğraşmasına gerek yok) ─────────────
def ses_onar(cikti):
    """`ses`, `*_ses` ve `secenek_ses` altındaki metinlerde büyük harfli kısaltmaları ve Roma rakamlarını projenin EMA
    okunuşuna çevirir (scripts/sesli_anlatim/modul_okunus.donustur: "MSH" → "mee see haa", "tip II" → "tip iki").
    Yerinde değiştirir, değişen alan sayısını döndürür. Okunuşa çevrilmiş metinde büyük harf kalmadığından eş güçlüdür."""
    sys.path.insert(0, str(KOK / "scripts" / "sesli_anlatim"))
    import modul_okunus as MO
    say = 0

    def gez(x, ses_alt=False):
        nonlocal say
        if isinstance(x, dict):
            for k, v in x.items():
                sesli = ses_alt or k == "ses" or str(k).endswith("_ses")
                if isinstance(v, str) and sesli:
                    yeni = MO.donustur(v)
                    if yeni != v:
                        x[k] = yeni; say += 1
                else:
                    gez(v, sesli)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, str) and ses_alt:
                    yeni = MO.donustur(v)
                    if yeni != v:
                        x[i] = yeni; say += 1
                else:
                    gez(v, ses_alt)
    gez(cikti)
    return say


_KATLA = str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosuCGIOSUaiu")


def turkce_katlama(cikti, paket_md: str = "") -> list[str]:
    """Türkçe harfleri düşmüş metin ("dogum", "bagli", "oykusu"): 2026-10-23 K2 provasında ücretsiz model iki çözücü
    partisini baştan sona harfsiz yazdı ve partiler kabul edildi. Sözlük paketin kendi girdisinden kurulur: girdide Türkçe
    harfle geçen kelimelerin katlanmış biçimi çıktıda, girdide katlanmış biçimiyle hiç geçmeden yazılmışsa sayılır. Bir
    alanda (≥3 kelimelik metin) ≥2 farklı böyle kelime varsa HATA. İngilizce alıntıya ve kısa cümleye takılmaz."""
    # büyük harfli kelimeler (OCR, başlık: "FIZIK" → "fızık"?) sözlüğe alınmaz: küçük/baş harfli kelimeler yeterli
    kel = [w for w in re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşüâîû]{4,}", paket_md) if not w.isupper()]
    ham = {w.replace("İ", "i").replace("I", "ı").lower() for w in kel}
    katli = {w.translate(_KATLA) for w in ham if re.search(r"[çğıöşüâîû]", w)} - ham
    if not katli:
        return []
    out = []

    def gez(x, yol):
        if isinstance(x, dict):
            yol = x.get("_etiket") or yol
            for k, v in x.items():
                if not str(k).startswith("_") and k not in ETIKET_MUAF_ALAN:
                    gez(v, f"{yol}.{k}" if yol else str(k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                gez(v, f"{yol}[{i}]")
        elif isinstance(x, str) and len(x.split()) >= 3:      # kimlik/tür değerleri ("ornek", soru_id) tek kelimedir
            ws = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{4,}", x.replace("İ", "i").replace("I", "ı").lower())
            kotu = [w for w in ws if w in katli]
            if len(set(kotu)) >= 2:
                out.append(f"{yol}: Türkçe harfler düşmüş ({', '.join(sorted(set(kotu))[:4])}) — metni ç, ğ, ı, ö, ş, ü ile doğru yaz")
    gez(cikti, "")
    return out


# ── oturum kuyruğu (profil `oturum`, 2026-10-24) ─────────────────────────────────────────────────────────────────────
def kuyruk_yolu() -> Path:
    return IS_DIZIN / "kuyruk.json"


def kuyruk() -> dict:
    return oku(kuyruk_yolu(), {}) or {"isler": {}, "zincirler": {}}


def kuyruk_ekle(is_id: str | None = None, tip: str = "is", zincir: list[str] | None = None, cwd: str | None = None,
                ortam: dict | None = None) -> None:
    """Oturumun çözeceği paket (is_id; tip 'is' = paket.md → cevap.txt, 'duzeltme' = duzeltme_paket.md → duzeltme_cevap.txt)
    ya da kaldığı yerden sürdürülecek zincir komutu (argv)."""
    k = kuyruk()
    if is_id:
        k["isler"][is_id] = {"tip": tip, "zaman": simdi()}
    if zincir:
        k["zincirler"][sha(json.dumps(zincir), 12)] = {"argv": zincir, "cwd": cwd, "ortam": ortam or {}, "zaman": simdi()}
    yaz(kuyruk_yolu(), k)


def kuyruk_cikar(is_id: str | None = None, zincir_anahtar: str | None = None) -> None:
    k = kuyruk()
    k["isler"].pop(is_id, None)
    k["zincirler"].pop(zincir_anahtar, None)
    yaz(kuyruk_yolu(), k)
