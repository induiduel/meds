#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Faz 14: Bulut Tabanlı (Gemini Flash) Çıkmış Soru İyileştirme ve İnceleme Pipeline'ı.

Kullanıcının ilettiği Chunk/Batch mimarisine göre çalışır:
- /v1 üzerinden soruları ve müfredatı çeker.
- Google Gemini (gemini-2.5-flash / gemini-3.8-flash) ile soruyu analiz eder,
  tıbbi literatüre (Robbins, Guyton, Harrison vb.) göre eksik/hatalı kökleri ve açıklamaları düzeltir,
  müfredat ve YZV (Yapay Zeka Verisi) bloğunu üretir.
- Üretilen verileri 'meds_database_v2/phase14_past_question_editor/reviews.jsonl'
  inceleme katmanına ve nofrostlife.com.tr/test/cikmis arayüzüne sunar.
- Opsiyonel --direct-apply bayrağı verilirse X-API-Password ile /api uç noktasına canlı uygular.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Dizin tanımları
ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "scripts" / "agents"
sys.path.insert(0, str(AGENTS))

try:
    import lib
except ImportError:
    lib = None

# .env yükleme
ENV_FILE = ROOT / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip("'\"")
        os.environ.setdefault(k.strip(), v)

# Ayarlar
BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")
V1_CATALOG_URL = f"{BASE_URL}/v1"
API_WRITE_URL = f"{BASE_URL}/api"
API_PASSWORD = os.environ.get("MEDSORU_API_PASSWORD", "12345678")

# Gemini API Anahtarları (GEMINI_API_KEY, GEMINI_FREE_KEY_2, GEMINI_BACKUP_KEY)
GEMINI_KEYS = [
    os.environ.get("GEMINI_API_KEY", "").strip(),
    *[os.environ.get(n, "").strip() for n in sorted((n for n in os.environ if n.startswith("GEMINI_FREE_KEY_") and n[16:].isdigit()), key=lambda n: int(n[16:]))],
    os.environ.get("GEMINI_FALLBACK_KEY", "").strip(),
]
GEMINI_KEYS = [k for k in list(dict.fromkeys(GEMINI_KEYS)) if k and not k.startswith("BURAYA_") and not k.startswith("MY_")]


def _paid_key() -> str:
    """ÜCRETLİ anahtar — YALNIZ bu betik (Faz 14) kullanır; ücretsiz anahtarlar tükenince devreye girer.
    Aylık bütçe tavanı (record_cost_and_check_budget) bu anahtar için de geçerlidir."""
    v = os.environ.get("PHASE14_PAID_GEMINI_KEY", "").strip()
    if not v:
        try:
            for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
                if line.startswith("PHASE14_PAID_GEMINI_KEY="):
                    v = line.split("=", 1)[1].strip().strip('"')
        except OSError:
            pass
    return v


if _paid_key() and _paid_key() not in GEMINI_KEYS:
    GEMINI_KEYS.append(_paid_key())

OUT_DIR = ROOT.parent / "meds_database_v2" / "phase14_past_question_editor"
REVIEWS_FILE = OUT_DIR / "reviews.jsonl"
CHECKPOINT_FILE = OUT_DIR / "checkpoint_cloud.json"
REPORT_FILE = OUT_DIR / "report.json"
CURRICULUM_FILE = ROOT / "curriculum" / "kbu_tip_donem3_curriculum.json"

HEADERS_READ = {"Accept": "application/json"}
HEADERS_WRITE = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Password": API_PASSWORD,
}

# Ücret denetimi: YALNIZ ücretli anahtar (PHASE14_PAID_GEMINI_KEY) sayılır; ücretsiz anahtarlar 0 TL.
# Kullanıcı sınırları: ücretli anahtarla günde en fazla 100 istek, ayda en fazla 100 TL.
USD_TO_TRY = 42.0  # güvenli tavan kur
PAID_MAX_DAILY_REQUESTS = int(os.environ.get("PHASE14_PAID_MAX_DAILY", "100"))
PAID_MAX_MONTHLY_TL = float(os.environ.get("PHASE14_PAID_MAX_MONTHLY_TL", "100"))
MAX_MONTHLY_BUDGET_TL = PAID_MAX_MONTHLY_TL  # panel/sayfa uyumu
COST_TRACKING_FILE = OUT_DIR / "cost_tracking.json"

MODEL_PRICING = {  # USD / token (Google Gemini; flash-lite en ucuz)
    "gemini-flash-lite-latest": {"input": 0.10 / 1_000_000, "output": 0.40 / 1_000_000},
    "gemini-3.5-flash-lite":    {"input": 0.10 / 1_000_000, "output": 0.40 / 1_000_000},
    "gemini-3.1-flash-lite":    {"input": 0.10 / 1_000_000, "output": 0.40 / 1_000_000},
    "gemini-flash-latest":      {"input": 0.30 / 1_000_000, "output": 2.50 / 1_000_000},
    "gemini-3.5-flash":         {"input": 0.30 / 1_000_000, "output": 2.50 / 1_000_000},
}
# Cevap doğruluğu için önce düşünen (reasoning) Flash; Flash-Lite yalnız yedek. Flash-Lite düşünmeden cevap seçtiği için
# kayıttaki cevabı ~%25 oranında yanlış değiştiriyordu (2026-10-06/07 incelemesi). Ücretli tavanlar (100 istek/gün,
# 100 TL/ay) record_usage/paid_allowed ile aynen korunur.
# Ücretsiz Flash kotası günde model başına yalnız 20 istek → kota bitince Flash-Lite yedek. Lite'ın cevap değişikliği
# cevap_dogrula'da ancak güçlü bağımsız model (gpt-oss) + açıklama aynı şıkta birleşirse kabul edilir.
PAID_MODELS = ["gemini-flash-latest", "gemini-3.5-flash", "gemini-flash-lite-latest"]
FREE_MODELS = ["gemini-flash-latest", "gemini-3.5-flash", "gemini-flash-lite-latest", "gemini-3.5-flash-lite"]
STRONG_VERIFIER = "gpt-oss"                                    # cevap DEĞİŞİKLİĞİNİ yalnız bu doğrulayıcı onaylayabilir
# Bağımsız cevap doğrulayıcı (farklı model ailesi, ücretsiz Groq): soruyu kayıtlı cevabı görmeden çözer
VERIFY_MODELS = ["groq:openai/gpt-oss-120b", "groq:qwen/qwen3.8-27b"]


def load_monthly_cost() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    month = datetime.utcnow().strftime("%Y-%m")
    day = datetime.utcnow().strftime("%Y-%m-%d")
    data = {}
    if COST_TRACKING_FILE.exists():
        try:
            data = json.loads(COST_TRACKING_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    if data.get("month") != month:
        data = {"month": month, "total_requests": 0, "free_requests": 0, "paid_requests": 0, "input_tokens": 0,
                "output_tokens": 0, "cost_usd": 0.0, "cost_tl": 0.0}
    if data.get("paid_day") != day:
        data["paid_day"], data["paid_requests_today"] = day, 0
    data["max_budget_tl"] = PAID_MAX_MONTHLY_TL
    data["paid_max_daily"] = PAID_MAX_DAILY_REQUESTS
    return data


def _save_cost(state: dict):
    state["last_updated"] = datetime.utcnow().isoformat() + "Z"
    tmp = COST_TRACKING_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(COST_TRACKING_FILE)


def paid_allowed() -> tuple[bool, str]:
    st = load_monthly_cost()
    if st.get("paid_requests_today", 0) >= PAID_MAX_DAILY_REQUESTS:
        return False, f"ücretli günlük sınır doldu ({st['paid_requests_today']}/{PAID_MAX_DAILY_REQUESTS})"
    if st.get("cost_tl", 0) >= PAID_MAX_MONTHLY_TL:
        return False, f"ücretli aylık bütçe doldu ({st['cost_tl']:.2f}/{PAID_MAX_MONTHLY_TL:.0f} TL)"
    return True, ""


def record_usage(model_name: str, paid: bool, in_tokens: int, out_tokens: int, cached_tokens: int = 0) -> dict:
    st = load_monthly_cost()
    st["total_requests"] += 1
    st["input_tokens"] += in_tokens
    st["output_tokens"] += out_tokens
    cost_tl = 0.0
    if paid:
        pr = MODEL_PRICING.get(model_name, MODEL_PRICING["gemini-flash-latest"])
        # önbellekten okunan girdi tokenları %25 fiyatla (implicit caching)
        usd = (in_tokens - cached_tokens) * pr["input"] + cached_tokens * pr["input"] * 0.25 + out_tokens * pr["output"]
        cost_tl = usd * USD_TO_TRY
        st["paid_requests"] = st.get("paid_requests", 0) + 1
        st["paid_requests_today"] = st.get("paid_requests_today", 0) + 1
        st["cost_usd"] = round(st["cost_usd"] + usd, 6)
        st["cost_tl"] = round(st["cost_tl"] + cost_tl, 4)
    else:
        st["free_requests"] = st.get("free_requests", 0) + 1
    _save_cost(st)
    return {"cost_tl": cost_tl, **st}


LOG_FILE = ROOT.parent / "meds_temp" / "logs" / "phase14.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    # Tek işleyici: sunucu betiğin stdout/stderr'ini zaten phase14.log'a yönlendiriyor; StreamHandler + FileHandler
    # birlikte her satırı İKİ KEZ yazıyordu (istek tek). Çıktı terminale gidiyorsa (elle çalıştırma) ekrana da yazılır.
    handlers=[logging.FileHandler(str(LOG_FILE), encoding="utf-8")] + ([logging.StreamHandler(sys.stderr)] if sys.stderr.isatty() else [])
)


def load_checkpoints() -> set[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if CHECKPOINT_FILE.exists():
        try:
            return set(json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8")).get("done_ids", []))
        except Exception:
            pass
    return set()


def save_checkpoint(islenmis_set: set[str], soru_id: str):
    islenmis_set.add(soru_id)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"done_ids": sorted(islenmis_set), "updated_at": datetime.utcnow().isoformat() + "Z"}
    CHECKPOINT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_curriculum_summary() -> str:
    if not CURRICULUM_FILE.exists():
        return ""
    try:
        data = json.loads(CURRICULUM_FILE.read_text(encoding="utf-8"))
        comms = data.get("committees", {})
        lines = []
        for code, info in comms.items():
            name = info.get("name", "")
            deps = ", ".join(info.get("departments", [])[:5])
            lines.append(f"- {code} ({name}): Branşlar: {deps}")
        return "\n".join(lines)
    except Exception:
        return ""


def _key_tiers() -> list[tuple[str, str, bool]]:
    """(etiket, anahtar, ücretli_mi) — önce ücretsizler, en son ücretli (yalnız Faz 14)."""
    tiers = []
    for name in ("GEMINI_API_KEY", *[f"GEMINI_FREE_KEY_{i}" for i in range(2, 51)], "GEMINI_FALLBACK_KEY"):
        v = os.environ.get(name, "").strip()
        if not v:
            try:
                for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
                    if line.startswith(name + "="):
                        v = line.split("=", 1)[1].split(" #")[0].strip().strip('"')
            except OSError:
                pass
        if v and not v.startswith(("BURAYA_", "MY_")) and v != _paid_key() and all(v != t[1] for t in tiers):
            tiers.append((f"ücretsiz:{name}", v, False))
    if _paid_key():
        tiers.append(("ÜCRETLİ:PHASE14_PAID_GEMINI_KEY", _paid_key(), True))
    return tiers


# Kip: ücretli anahtar yalnız elle başlatmada (ALLOW_PAID) ve ücretsizler tükenince. Otomatik kip yalnız ücretsiz.
ALLOW_PAID = False
FREE_RPM = int(os.environ.get("PHASE14_FREE_RPM", "6"))   # Flash ücretsiz katman dakikalık sınırı düşük
_last_call = [0.0]
_daily_exhausted: set[str] = set()                            # bu çalıştırmada günlük kotası biten (anahtar, model)


class QuotaExhausted(Exception):
    """Ücretsiz anahtarların günlük kotası bitti (ve ücretliye izin yok)."""


def call_gemini_json(prompt_text: str, system_text: str = "") -> tuple[dict | None, str]:
    """Gemini REST. system_text (kurallar + müfredat paketi) her istekte AYNI → otomatik önbellek (implicit caching).
    Her istekte hangi API/anahtar/model kullanıldığı ve ücretli sayaç günlüğe yazılır. Yerel model yok."""
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt_text}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1},
    }
    if system_text:
        payload["systemInstruction"] = {"parts": [{"text": system_text}]}
    data_bytes = json.dumps(payload).encode("utf-8")

    tried_any = False
    for label, key, paid in _key_tiers():
        if paid and not ALLOW_PAID:
            continue                                         # otomatik/ücretsiz kip: ücretli asla
        if paid:
            ok, why = paid_allowed()
            if not ok:
                logging.warning(f"[API] {label} kullanılmadı: {why}")
                continue
        for model in (PAID_MODELS if paid else FREE_MODELS):
            if (label, model) in _daily_exhausted:
                continue
            tried_any = True
            for _deneme in range(3):                         # 429/503/zaman aşımı: aynı modelle bekleyip yeniden dene
                r = _tek_istek(label, key, paid, model, data_bytes, prompt_text)
                if r == "tekrar":
                    time.sleep(20 * (_deneme + 1))
                    continue
                break
            if r in ("tekrar", "gec", "gunluk"):
                continue
            return r
    free_left = [1 for lb, _k, pd in _key_tiers() if not pd for m in FREE_MODELS if (lb, m) not in _daily_exhausted]
    if not free_left and not ALLOW_PAID:
        raise QuotaExhausted("ücretsiz günlük kotalar doldu")
    if not tried_any:
        raise QuotaExhausted("denenebilecek anahtar/model kalmadı")
    logging.error("[API] hiçbir anahtar/model yanıt vermedi; soru sonraki çalıştırmaya kaldı")
    return None, "none"


def _tek_istek(label: str, key: str, paid: bool, model: str, data_bytes: bytes, prompt_text: str):
    """Tek Gemini isteği. Başarıda (json, model_etiketi); 'tekrar' (geçici hata), 'gunluk' (günlük kota), 'gec' (diğer)."""
    if not paid:                                     # ücretsiz katman: dakikalık sınırın altında kal
        wait = 60.0 / max(1, FREE_RPM) - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    req = urllib.request.Request(url, data=data_bytes, method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        text = "".join(p.get("text", "") for p in (body.get("candidates") or [{}])[0].get("content", {}).get("parts", [])).strip()
        usage = body.get("usageMetadata", {})
        in_t = usage.get("promptTokenCount", len(prompt_text) // 4)
        out_t = usage.get("candidatesTokenCount", len(text) // 4)
        cached = usage.get("cachedContentTokenCount", 0)
        st = record_usage(model, paid, in_t, out_t, cached)
        if paid:
            logging.info(f"[API] {label} · {model} · giriş {in_t} (önbellek {cached}) / çıkış {out_t} token · "
                         f"~{st['cost_tl']:.4f} TL · bugün {st['paid_requests_today']}/{PAID_MAX_DAILY_REQUESTS} · "
                         f"ay {st['cost_tl']:.2f}/{PAID_MAX_MONTHLY_TL:.0f} TL")
        else:
            logging.info(f"[API] {label} · {model} · giriş {in_t} (önbellek {cached}) / çıkış {out_t} token · ücretsiz")
        if text.startswith("```"):
            text = text.strip("`").split("\n", 1)[1] if "\n" in text else text
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text), f"{model} ({'ücretli' if paid else 'ücretsiz'})"
    except urllib.error.HTTPError as e:
        err_full = e.read().decode("utf-8", errors="ignore")
        err = err_full[:200]
        if e.code == 429:
            if any(t in err_full for t in ("PerDay", "per day", "RPD", "daily")):   # tam gövde: kısaltılınca günlük kota kaçıyordu
                _daily_exhausted.add((label, model))
                logging.warning(f"[API] {label} · {model}: GÜNLÜK kota doldu; bu çalıştırmada tekrar denenmez")
                return "gunluk"
            logging.warning(f"[API] {label} · {model}: dakikalık kota (429), beklenip yeniden denenecek")
            return "tekrar"
        logging.warning(f"[API] {label} · {model}: HTTP {e.code} {err}")
        return "tekrar" if e.code in (500, 503, 504) else "gec"
    except Exception as e:  # noqa: BLE001
        logging.warning(f"[API] {label} · {model}: {e}")
        return "tekrar"


def canonical_options(question: dict) -> dict[str, str]:
    raw = question.get("options") or (question.get("reconstruction") or {}).get("options") or {}
    if isinstance(raw, dict):
        return {str(k).upper(): str(v) for k, v in raw.items() if str(k).upper() in "ABCDE"}
    if isinstance(raw, list):
        result = {}
        for i, item in enumerate(raw[:5]):
            key = "ABCDE"[i]
            result[key] = str(item.get("text", "")) if isinstance(item, dict) else str(item)
        return result
    return {}


def source_view(question: dict) -> dict:
    rec = question.get("reconstruction") or {}
    return {
        "id": question.get("id"),
        "soru_koku": question.get("stem") or question.get("rawQuestion", {}).get("stem") or rec.get("stem") or "",
        "secenekler": canonical_options(question),
        "dogru_secenek": question.get("correctAnswer") or question.get("claimedAnswer") or rec.get("answer") or "",
        "aciklama": question.get("explanation") or rec.get("explanation") or "",
        "kurul_adi": question.get("committeeId") or "",
        "ders_adi": question.get("discipline") or "",
        "konu_adi": question.get("topic") or "",
    }


PHASE14_RULES = """Sen tıp fakültesi Dönem 3 kurul sınavı soru editörüsün. Görevin, öğrencilerin hatırlayarak ya da OCR ile
aktardığı ÇIKMIŞ bir soruyu, sorulmak isteneni değiştirmeden doğru, eksiksiz ve okunur hâle getirmektir.

TALİMATLARA HARFİYEN UY:
1. SORU KÖKÜ: Anlamını ve bağlamını mümkün olduğunca DEĞİŞTİRME. Yalnız imla, harf düşmesi, OCR bozukluğu, yapışık
   kelime ve eksik kalmış kısmı düzelt/tamamla. Eksik kökü ŞIKLARDAN yararlanarak tamamla (şıklar sorunun ne sorduğunu
   gösterir). Olumlu kökü olumsuza, olumsuzu olumluya ÇEVİRME. Sorunun ana hedefi neyse ona odaklan; başka bir konuya kaydırma.
2. ŞIKLAR: Aynı ilke — imla/OCR/yapışık kelime düzelt, eksik kalan şık metnini bağlamdan tamamla. Kaynakta hiç olmayan
   şıkları ancak 5'e tamamlamak için ekle ve harflerini "yapay_zeka_tamamlanan_siklar" listesine yaz.
3. CEVAP — ÇOK ÖNEMLİ: Kayıttaki cevap ("kayitli_cevap") YANLIŞ OLABİLİR (çoğu öğrencinin işaretlediği şıktır).
   Şıkları ASLA kayıttaki cevaba uysun diye değiştirme. Doğru cevabı soru kökü ve şıkların tıbbi içeriğine göre SEN belirle.
   Kayıttaki cevapla aynıysa "cevap_degisti": false; farklıysa "cevap_degisti": true ve "cevap_gerekcesi"nde nedenini yaz.
   Emin değilsen "cevap_emin": false yaz.
4. MÜFREDAT: Aşağıdaki DÖNEM 3 MÜFREDAT PAKETİ'ni kullan. Sorunun hangi kurul, ders ve KONU başlığına ait olduğunu
   paketteki adlarla birebir yaz (paketteki bir konu adını seç; uydurma ad yazma). Kurulu "TIP3N0" biçiminde yaz.
5. AÇIKLAMA: Maddeler hâlinde yaz ("aciklama_maddeleri" listesi, 3–6 madde, her madde tek cümle/kısa paragraf):
   doğru cevabın mekanizması, önemli çeldiricilerin neden yanlış olduğu, varsa klinik ipucu. Uydurma kaynak gösterme.
6. Yaptığın her değişikliği "degisen_alanlar" ve "degisiklik_ozeti"nde dürüstçe belirt. Değişiklik yoksa boş liste.
7. Yalnız istenen JSON şemasıyla yanıt ver."""


def system_text() -> str:
    """Kurallar + tüm müfredat paketi: her istekte birebir aynı (Gemini otomatik önbelleği için ön ek)."""
    global _SYSTEM_CACHE
    if _SYSTEM_CACHE is None:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import curriculum_package as CP
            pkg_text = CP.as_text(CP.load())
        except Exception as e:  # noqa: BLE001
            logging.warning(f"Müfredat paketi okunamadı ({e}); paketsiz devam")
            pkg_text = ""
        _SYSTEM_CACHE = PHASE14_RULES + "\n\n" + pkg_text
    return _SYSTEM_CACHE


_SYSTEM_CACHE = None

SCHEMA_HINT = """YANIT ŞEMASI (yalnız JSON):
{"soru_koku": "...", "secenekler": {"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."},
 "yapay_zeka_tamamlanan_siklar": [],
 "sik_analizi": {"A": "bu şık doğru mu yanlış mı, neden (1 cümle)", "B": "...", "C": "...", "D": "...", "E": "..."},
 "aciklama_maddeleri": ["...", "..."],
 "dogru_secenek": "A-E (YUKARIDAKİ şık analizi ve açıklamanın gösterdiği şık; onlarla çelişemez)",
 "cevap_degisti": false, "cevap_emin": true, "cevap_gerekcesi": "...",
 "kurul_adi": "TIP310", "ders_adi": "paketteki ders adı", "konu_adi": "paketteki konu adı",
 "degisen_alanlar": ["soru_koku"], "degisiklik_ozeti": "kısa ve somut",
 "YZV": {"degisiklik_ozeti": {"soru_koku_duzeltmesi": "...", "sik_duzeltmesi": "...", "aciklama_duzeltmesi": "...",
          "mufredat_atamasi": "...", "cevap_dogrulamasi": "..."}, "referans_literatur": "varsa standart kaynak"}}"""


def ai_ile_soruyu_duzelt(soru: dict, mufredat_ozeti: str = "") -> tuple[dict | None, str]:
    """Soruyu bulut modeline gönderir. Kayıttaki cevap 'kayitli_cevap' olarak verilir (doğru kabul edilmez)."""
    girdi = {k: v for k, v in soru.items() if k != "dogru_secenek"}
    girdi["kayitli_cevap"] = soru.get("dogru_secenek") or ""
    prompt = "İNCELENECEK SORU:\n" + json.dumps(girdi, ensure_ascii=False, indent=1) + "\n\n" + SCHEMA_HINT
    res, model = call_gemini_json(prompt, system_text())
    if isinstance(res, dict):
        maddeler = [str(m).strip() for m in (res.get("aciklama_maddeleri") or []) if str(m).strip()]
        if maddeler:
            res["aciklama"] = "\n".join(f"• {m}" for m in maddeler)   # site bu satırları madde olarak gösterir
        res.setdefault("review_required", True)
        anlam_koru(soru, res)
        cevap_dogrula(soru, res)
    return res, model


_OLUMSUZ = ("değildir", "degildir", "yanlıştır", "yanlistir", "olmaz", "hariç", "haric", "yoktur", "beklenmez",
            "görülmez", "gorulmez", "yapılmamalı", "yapilmamali", "doğru değil", "dogru degil", "yanlış", "en az")


def _olumsuz_mu(metin: str) -> bool:
    t = (metin or "").lower()
    return any(w in t for w in _OLUMSUZ)


def anlam_koru(soru: dict, res: dict) -> None:
    """Modelin soruyu kendi cevabına uydurmasını engeller (Flash-Lite 'doğru değildir'i 'doğrudur' yapıp şıkları
    yeniden yazıyordu). Kökün olumsuzluk yönü değiştiyse kök geri alınır; dolu bir şık anlamca çok değiştiyse
    (benzerlik < 0.55) o şık özgün haline döner. Boş/eksik şıkların tamamlanmasına izin verilir."""
    import difflib
    notlar = []
    ok, yk = soru.get("soru_koku") or "", res.get("soru_koku") or ""
    if ok and yk and _olumsuz_mu(ok) != _olumsuz_mu(yk):
        res["soru_koku"] = ok
        notlar.append("kökün olumlu/olumsuz yönü değiştirilmişti → özgün kök korundu")
    osec, ysec = soru.get("secenekler") or {}, res.get("secenekler") or {}
    if isinstance(osec, dict) and isinstance(ysec, dict):
        for k, ov in osec.items():
            ov = str(ov or "").strip()
            yv = str(ysec.get(k) or "").strip()
            if len(ov) >= 3 and yv and difflib.SequenceMatcher(None, ov.lower(), yv.lower()).ratio() < 0.55:
                ysec[k] = ov
                notlar.append(f"{k} şıkkı anlamca değiştirilmişti → özgün şık korundu")
        res["secenekler"] = ysec
    if notlar:
        res["review_required"] = True
        res["anlam_koruma"] = notlar
        logging.info("[KORUMA] " + "; ".join(notlar))


def _bagimsiz_cevap(soru_koku: str, secenekler: dict) -> tuple[str, str]:
    """Kayıtlı cevabı ve önerilen cevabı GÖRMEDEN soruyu çözer (ücretsiz Groq). (harf, model) ya da ("", "")."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
    try:
        import cloud_llm
    except Exception:
        return "", ""
    prompt = ("Tıp fakültesi sınav sorusu. Adım adım düşün, her şıkkı değerlendir, sonra tek doğru şıkkı seç.\n"
              "Soru kökündeki olumsuzluk ifadelerine (değildir, yanlıştır, olmaz, hariç) özellikle dikkat et.\n\n"
              f"SORU: {soru_koku}\n" + "\n".join(f"{k}) {v}" for k, v in sorted(secenekler.items()) if v) +
              '\n\nYalnız JSON: {"dogru_secenek": "A-E", "gerekce": "kısa"}')
    try:
        r = cloud_llm.chat(prompt, as_json=True, max_tokens=4000, temperature=0.0, models=VERIFY_MODELS, timeout=120)
    except Exception as e:
        logging.warning(f"[DOĞRULAMA] hata: {e}")
        return "", ""
    harf = str((r or {}).get("dogru_secenek") or "").strip().upper()[:1]
    return (harf if harf in secenekler else ""), (getattr(cloud_llm, "last_model", {}) or {}).get("ad") or "groq"


def _aciklamanin_cevabi(soru_koku: str, secenekler: dict, res: dict) -> str:
    """Modelin yazdığı şık analizi + açıklama hangi şıkkı doğru cevap olarak gösteriyor? (işaretlenen harf verilmez)"""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
    try:
        import cloud_llm
    except Exception:
        return ""
    analiz = res.get("sik_analizi") or {}
    maddeler = res.get("aciklama_maddeleri") or [res.get("aciklama") or ""]
    metin = ("\n".join(f"{k}: {v}" for k, v in sorted(analiz.items())) if isinstance(analiz, dict) else str(analiz))
    prompt = ("Aşağıda bir sınav sorusu ve bir öğrencinin yazdığı açıklama var. Tıbbi doğruluğu DEĞERLENDİRME; yalnız bu "
              "açıklamanın hangi şıkkı sorunun cevabı olarak gösterdiğini belirle. Soru kökündeki olumsuzluğa dikkat et "
              "(ör. 'hangisi yanlıştır' sorusunda cevap, açıklamanın YANLIŞ dediği şıktır).\n\n"
              f"SORU: {soru_koku}\n" + "\n".join(f"{k}) {v}" for k, v in sorted(secenekler.items()) if v) +
              f"\n\nŞIK ANALİZİ:\n{metin}\n\nAÇIKLAMA:\n" + "\n".join(str(m) for m in maddeler) +
              '\n\nYalnız JSON: {"aciklamanin_cevabi": "A-E" ya da "belirsiz"}')
    try:
        r = cloud_llm.chat(prompt, as_json=True, max_tokens=2000, temperature=0.0, models=VERIFY_MODELS, timeout=120)
    except Exception:
        return ""
    h = str((r or {}).get("aciklamanin_cevabi") or "").strip().upper()[:1]
    return h if h in secenekler else ""


def cevap_dogrula(soru: dict, res: dict) -> None:
    """Cevap kararını iki bağımsız modelle sağlamlaştırır:
    * Öneri kayıtlı cevapla aynı ve doğrulayıcı da aynı → değişiklik yok.
    * Öneri kayıtlıyı değiştiriyor → değişiklik yalnız doğrulayıcı YENİ cevapla hemfikirse kalır;
      doğrulayıcı kayıtlıyla hemfikirse kayıtlı cevaba dönülür; ikisi de değilse kayıtlı korunur, incelemeye düşer.
    * Öneri aynı ama doğrulayıcı farklı → cevap korunur, 'cevap şüpheli' olarak incelemeye düşer.
    Sonuç res['cevap_dogrulama'] alanında saklanır."""
    kayitli = str(soru.get("dogru_secenek") or "").strip().upper()[:1]
    oneri = str(res.get("dogru_secenek") or "").strip().upper()[:1]
    sec = res.get("secenekler") or soru.get("secenekler") or {}     # anlam_koru sonrası: özgün anlamda şıklar
    if not oneri or not isinstance(sec, dict):
        return
    harf, vmodel = _bagimsiz_cevap(res.get("soru_koku") or soru.get("soru_koku") or "", sec)
    ac_harf = _aciklamanin_cevabi(res.get("soru_koku") or soru.get("soru_koku") or "", sec, res)
    d = {"kayitli": kayitli, "oneri": oneri, "dogrulayici": harf, "dogrulayici_model": vmodel, "aciklama_gosterdigi": ac_harf}
    if ac_harf and ac_harf != oneri:
        # model açıklamada başka şıkkı savunup farklı harf işaretlemiş → önerinin cevabı güvenilmez
        logging.info(f"[DOĞRULAMA] açıklama {ac_harf} şıkkını gösteriyor, işaretlenen {oneri} → çelişki")
        d["aciklama_celiskisi"] = True
        if ac_harf == harf:
            oneri = ac_harf                                   # açıklama + bağımsız model aynı şıkta: o şık öneridir
            res["dogru_secenek"] = ac_harf
        res["review_required"] = True
    alanlar = list(res.get("degisen_alanlar") or [])
    if not harf:
        d["sonuc"] = "dogrulanamadi"
        if kayitli and oneri != kayitli:                     # doğrulanamayan değişiklik kabul edilmez
            res["dogru_secenek"] = kayitli
            res["cevap_degisti"] = False
            d["sonuc"] = "dogrulanamadi_kayitli_korundu"
        res["review_required"] = True
    elif not kayitli or oneri == kayitli:
        d["sonuc"] = "uzlasi" if harf == oneri else "suphe_kayitli_korundu"
        if harf != oneri:
            res["review_required"] = True
            res["cevap_emin"] = False
    elif harf == oneri and (STRONG_VERIFIER not in vmodel or (ac_harf and ac_harf != oneri)):
        res["dogru_secenek"] = kayitli                      # zayıf doğrulayıcı ya da açıklama çelişkisi: değişiklik yok
        res["cevap_degisti"] = False
        alanlar = [a for a in alanlar if a not in ("dogru_secenek", "cevap")]
        d["sonuc"] = "degisiklik_yeterince_dogrulanamadi_kayitli_korundu"
        res["review_required"] = True
    elif harf == oneri:
        d["sonuc"] = "degisiklik_iki_modelce_dogrulandi"
        res["cevap_degisti"] = True
        res["review_required"] = True                        # cevap değişikliği her zaman insan onayından geçer
    else:
        res["dogru_secenek"] = kayitli
        res["cevap_degisti"] = False
        alanlar = [a for a in alanlar if a not in ("dogru_secenek", "cevap")]
        d["sonuc"] = "degisiklik_reddedildi_kayitli_korundu" if harf == kayitli else "uzlasma_yok_kayitli_korundu"
        res["review_required"] = True
    son = str(res.get("dogru_secenek") or "").upper()[:1]
    if ac_harf and ac_harf != son:
        # kalan cevapla çelişen açıklama yayınlanmaz: incelemeye düşer, işaretlenir
        d["aciklama_son_cevapla_celisiyor"] = True
        res["review_required"] = True
    res["degisen_alanlar"] = alanlar
    res["cevap_dogrulama"] = d
    logging.info(f"[DOĞRULAMA] kayıtlı {kayitli or '-'} · öneri {oneri} · bağımsız {harf or '?'} ({vmodel}) → {d['sonuc']}")


def support_ratio(original: dict, proposal: dict) -> float:
    def get_tokens(text: str) -> set[str]:
        return set(text.lower().split())

    before = " ".join([original.get("soru_koku", ""), original.get("aciklama", ""), *original.get("secenekler", {}).values()])
    after = " ".join([str(proposal.get("soru_koku") or ""), str(proposal.get("aciklama") or ""),
                      *[str(v) for v in (proposal.get("secenekler") or {}).values()]])
    tok_after = get_tokens(after)
    if not tok_after:
        return 1.0
    new_tokens = tok_after - get_tokens(before)
    return round(max(0.0, 1.0 - (len(new_tokens) / len(tok_after))), 3)


def main() -> int:
    parser = argparse.ArgumentParser(description="Faz 14 Bulut Tabanlı Çıkmış Soru İyileştirme")
    parser.add_argument("--limit", type=int, default=10, help="Bu çalıştırmada incelenecek soru sayısı")
    parser.add_argument("--chunk-size", type=int, default=30, help="API'den bir seferde çekilecek soru sayısı")
    parser.add_argument("--direct-apply", action="store_true", help="İnceleme katmanına yazmanın yanı sıra /api üzerinden de doğrudan uygula")
    parser.add_argument("--ucretli-izin", action="store_true", help="ELLE başlatma: ücretsizler tükenince ücretli anahtara geç")
    parser.add_argument("--ucretsiz-otomatik", action="store_true", help="otomatik kip: yalnız ücretsiz, günlük kota bitene kadar")
    args = parser.parse_args()
    global ALLOW_PAID
    ALLOW_PAID = bool(args.ucretli_izin) and not args.ucretsiz_otomatik
    if args.ucretsiz_otomatik:
        args.limit = max(args.limit, 5000)                  # kota bitene kadar
    logging.info(f"Kip: {'ELLE (önce ücretsiz, sonra ücretli)' if ALLOW_PAID else 'YALNIZ ÜCRETSİZ' + (' · otomatik' if args.ucretsiz_otomatik else '')} · limit {args.limit}")

    islenmisler = load_checkpoints()
    curriculum_summary = ""  # müfredat paketi sistem metninde (system_text)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Soruları çek: Önce yerel veritabanı dosyasından veya /v1/past-exams endpointinden
    questions = []
    local_past = ROOT / "data" / "pastQuestions.json"
    if local_past.exists():
        try:
            raw = json.loads(local_past.read_text(encoding="utf-8"))
            questions = raw if isinstance(raw, list) else raw.get("questions", [])
            logging.info(f"Yerel çıkmış soru deposundan {len(questions)} soru yüklendi.")
        except Exception as e:
            logging.warning(f"Yerel dosya okunamadı: {e}")

    if not questions:
        try:
            req = urllib.request.Request(f"{V1_CATALOG_URL}/past-exams", headers=HEADERS_READ)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
                questions = data.get("questions", [])
                logging.info(f"/v1/past-exams üzerinden {len(questions)} soru çekildi.")
        except Exception as e:
            logging.error(f"Soru çekme hatası: {e}")
            return 1

    # Ders programı sırası: Dönem 3 Kurul 1'den başlayarak kurul → ders → konu (rastgele değil)
    import re as _re

    def _order(q: dict):
        c = str(q.get("contentCommitteeId") or q.get("committeeId") or "")
        m = _re.search(r"kurul\s*-?\s*(\d)", c, _re.I) or _re.match(r"^TIP\s*3(\d)0$", c, _re.I)
        k = int(m.group(1)) if m else (7 if "final" in c else 8 if "butunleme" in c else 9)
        return (k, str(q.get("discipline") or ""), str(q.get("topic") or ""), str(q.get("id") or ""))

    questions = sorted(questions, key=_order)
    stats = {"aday": len(questions), "islenen": 0, "degisiklik_onerisi": 0, "inceleme_gerekli": 0, "hata": 0}

    with REVIEWS_FILE.open("a", encoding="utf-8") as out_reviews:
        for q in questions:
            s_id = str(q.get("id") or "")
            if not s_id or s_id in islenmisler:
                continue
            if stats["islenen"] >= args.limit:
                break

            src = source_view(q)
            if len(src["soru_koku"].strip()) < 15 or len(src["secenekler"]) < 4:
                continue

            logging.info(f"Soru #{s_id} inceleniyor · {q.get('committeeId')} · {q.get('discipline')} · {q.get('topic')}")
            try:
                ai_sonuc, model_used = ai_ile_soruyu_duzelt(src, curriculum_summary)
            except QuotaExhausted as qe:
                logging.info(f"Durduruldu: {qe}. Yarın kota yenilenince kaldığı sorudan sürer.")
                break

            if not ai_sonuc or not isinstance(ai_sonuc, dict):
                logging.warning(f"Soru #{s_id} için AI yanıtı alınamadı.")
                stats["hata"] += 1
                continue

            ratio = support_ratio(src, ai_sonuc)
            changed = ai_sonuc.get("degisen_alanlar") or []
            if not changed and ai_sonuc.get("YZV", {}).get("degisiklik_yapildi_mi"):
                changed = ["soru_koku", "aciklama"]

            # İnceleme katmanı kaydı
            record = {
                "question_id": s_id,
                "source_hash": hashlib.sha256(json.dumps(src, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "model": model_used or "bilinmiyor",
                "source": src,
                "proposal": ai_sonuc,
                "support_ratio": ratio,
                "status": "review_required" if (ratio < 0.85 or ai_sonuc.get("review_required", True)) else "unchanged",
            }

            out_reviews.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_reviews.flush()

            stats["islenen"] += 1
            stats["degisiklik_onerisi"] += int(bool(changed))
            stats["inceleme_gerekli"] += int(record["status"] == "review_required")

            save_checkpoint(islenmisler, s_id)
            logging.info(f"✓ Soru #{s_id} inceleme katmanına yazıldı ({record['status']}, kanıt {ratio}).")

            # Eğer --direct-apply verilmişse canlı API'ye yaz
            if args.direct_apply:
                try:
                    update_body = dict(q)
                    update_body.update(ai_sonuc)
                    up_req = urllib.request.Request(
                        f"{API_WRITE_URL}/questions/{s_id}",
                        data=json.dumps(update_body).encode("utf-8"),
                        headers=HEADERS_WRITE,
                        method="PUT",
                    )
                    with urllib.request.urlopen(up_req, timeout=10) as up_res:
                        if up_res.status in [200, 204]:
                            logging.info(f"✓ Soru #{s_id} /api/questions üzerinden güncellendi.")
                except Exception as up_err:
                    logging.warning(f"Doğrudan güncelleme hatası (#{s_id}): {up_err}")

            time.sleep(1)

    REPORT_FILE.write_text(json.dumps({
        "zaman": datetime.utcnow().isoformat() + "Z",
        "motor": "Google Gemini Flash (Bulut)",
        **stats,
        "cikti": str(REVIEWS_FILE),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    logging.info(f"Faz 14 Bulut İşlemi Tamamlandı: {stats}")
    # Tüm sorular Faz 14'ten geçtiyse RAG + veritabanı yenilemesini kuyruğa al (bir kez)
    kalan = sum(1 for q in questions if str(q.get("id") or "") and str(q.get("id")) not in islenmisler
                and len(source_view(q)["soru_koku"].strip()) >= 15 and len(source_view(q)["secenekler"]) >= 4)
    if kalan == 0:
        flag = ROOT.parent / "meds_temp" / "state" / "faz14_bitti_rag.json"
        if not flag.exists():
            try:
                import fcntl
                qf = ROOT.parent / "meds_temp" / "state" / "phase_queue.json"
                with open(qf.with_suffix(".lock"), "w") as lk:
                    fcntl.flock(lk, fcntl.LOCK_EX)
                    q = json.loads(qf.read_text(encoding="utf-8")) if qf.exists() else []
                    if "rag_yenile" not in q:
                        q.append("rag_yenile")
                    qf.write_text(json.dumps(q), encoding="utf-8")
                flag.write_text(json.dumps({"zaman": datetime.utcnow().isoformat() + "Z"}), encoding="utf-8")
                logging.info("Tüm sorular Faz 14'ten geçti → RAG + veritabanı yenilemesi kuyruğa alındı (rag_yenile)")
            except Exception as e:  # noqa: BLE001
                logging.warning(f"RAG yenileme kuyruğa alınamadı: {e}")
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
