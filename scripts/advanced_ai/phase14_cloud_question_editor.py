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
import re
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
# Flash-Lite Faz 14'te HİÇ kullanılmaz (2026-10-07 testleri: çelişkili şık analizi, yanlış cevap). Güçlü model kotası
# bitince Faz 14 durur (QuotaExhausted) ve kota yenilenince kaldığı yerden sürer.
PAID_MODELS = ["gemini-flash-latest", "gemini-3.5-flash"]
FREE_MODELS = ["gemini-flash-latest", "gemini-3.5-flash"]
STRONG_GEMINI = ["gemini-flash-latest", "gemini-3.5-flash"]       # düşünen modeller: cevap oyu sayılır
LITE_MODELS = ["gemini-flash-lite-latest", "gemini-3.5-flash-lite"]
FAZ14_AYAR = ROOT.parent / "meds_temp" / "state" / "faz14_ayarlari.json"   # /test/cikmis sayfasından değiştirilir


def lite_acik() -> bool:
    """Flash kotası bitince Flash-Lite ile devam edilsin mi? (varsayılan açık; /test/cikmis → 'Lite yedeği')
    Lite yalnız soruyu düzeltir; cevap oyu SAYILMAZ (cevabı bağımsız çözücüler belirler)."""
    try:
        return bool(json.loads(FAZ14_AYAR.read_text(encoding="utf-8")).get("lite_kullan", True))
    except Exception:
        return True


WEAK_GEMINI = LITE_MODELS                                      # cevap oyu sayılmayan modeller
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
    with _KILIT:
        return _record_usage(model_name, paid, in_tokens, out_tokens, cached_tokens)


def _record_usage(model_name: str, paid: bool, in_tokens: int, out_tokens: int, cached_tokens: int = 0) -> dict:
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
    """İşlenmiş soru kimlikleri: checkpoint + inceleme kayıtlarında zaten bulunanlar (checkpoint kaybolsa/sıfırlansa
    bile aynı soru yeniden çözülmez)."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out: set[str] = set()
    if CHECKPOINT_FILE.exists():
        try:
            out |= set(json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8")).get("done_ids", []))
        except Exception:
            pass
    if REVIEWS_FILE.exists():
        for line in REVIEWS_FILE.read_text(encoding="utf-8").splitlines():
            m = re.search(r'"question_id":\s*"([^"]+)"', line)
            if m:
                out.add(m.group(1))
    return out


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


import threading

_YEREL = threading.local()            # paralel kipte iş parçacığının kendi anahtarı (_YEREL.anahtar = etiket)
_KILIT = threading.RLock()            # kayıt/checkpoint/maliyet yazımı (paralel kipte iş parçacıkları arası)
# Groq (gpt-oss doğrulayıcı) tek hesap: dakikada 8000 token. Paralel iş parçacıkları aynı anda gönderirse çoğu 429 alıp
# boşa bekler; doğrulama çağrıları sıraya alınır (Gemini düzeltmesi anahtar başına paralel kalır).
_GROQ_KILIT = threading.Lock()


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

    # Sıra MODEL önceliğine göre: güçlü (düşünen) Flash önce BÜTÜN ücretsiz anahtarlarda denenir, sonra (izinliyse)
    # ücretli anahtarda; Flash-Lite yalnız hiçbir Flash kalmadıysa. (Eski sıra anahtar-önce idi: 1. anahtarın Flash'ı
    # bitince diğer anahtarlardaki Flash denenmeden Lite'a düşülüyordu.)
    tiers = _key_tiers()
    tek = getattr(_YEREL, "anahtar", None)
    if tek:                                                  # paralel kip: yalnız bu iş parçacığının ücretsiz anahtarı
        tiers = [t for t in tiers if t[0] == tek and not t[2]]
    free = [(lb, k, pd) for lb, k, pd in tiers if not pd]
    paid_t = [(lb, k, pd) for lb, k, pd in tiers if pd] if ALLOW_PAID else []
    order = []
    for grup in ((STRONG_GEMINI, WEAK_GEMINI) if lite_acik() else (STRONG_GEMINI,)):
        order += [(m, t) for m in grup for t in free] + [(m, t) for m in grup for t in paid_t]
    tried_any = False
    for gecis in range(2):                                   # 2. geçiş: dakikalık sınırlar için kısa bekleme sonrası
        gecici = False
        for model, (label, key, paid) in order:
            if (label, model) in _daily_exhausted:
                continue
            if paid:
                ok, why = paid_allowed()
                if not ok:
                    logging.warning(f"[API] {label} kullanılmadı: {why}")
                    continue
            tried_any = True
            r = _tek_istek(label, key, paid, model, data_bytes, prompt_text)
            if r == "tekrar":
                gecici = True
                continue
            if r in ("gec", "gunluk"):
                continue
            return r
        if not gecici or tek:                                 # paralel kipte bekleme işçinin aralık planındadır
            break
        time.sleep(30)
    free_left = [1 for lb, _k, pd in tiers if not pd for m in FREE_MODELS + (WEAK_GEMINI if lite_acik() else [])
                 if (lb, m) not in _daily_exhausted]
    if tek:
        return None, "none"                                  # paralel kip: işçi kendi aralığıyla yeniden dener
    if not free_left and not ALLOW_PAID:
        raise QuotaExhausted("ücretsiz günlük kotalar doldu")
    if not tried_any:
        raise QuotaExhausted("denenebilecek anahtar/model kalmadı")
    logging.error("[API] hiçbir anahtar/model yanıt vermedi; soru sonraki çalıştırmaya kaldı")
    return None, "none"


_son_cagri: dict[str, float] = {}     # anahtar başına son istek zamanı (dakikalık sınır anahtar başınadır)


def _tek_istek(label: str, key: str, paid: bool, model: str, data_bytes: bytes, prompt_text: str):
    """Tek Gemini isteği. Başarıda (json, model_etiketi); 'tekrar' (geçici hata), 'gunluk' (günlük kota), 'gec' (diğer)."""
    if not paid:                                     # ücretsiz katman: dakikalık sınırın altında kal
        with _KILIT:
            son = _son_cagri.get(label, 0.0)
            wait = 60.0 / max(1, FREE_RPM) - (time.time() - son)
            _son_cagri[label] = time.time() + max(0.0, wait)
        if wait > 0:
            time.sleep(wait)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    req = urllib.request.Request(url, data=data_bytes, method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        _YEREL.yanit_alindi = True                           # kota/erişim sorunu yok: model yanıt verdi
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
3. CEVAP — ÇOK ÖNEMLİ: Sana eski cevap anahtarı VERİLMEZ (öğrenci işaretlerinden gelir, çoğu zaman yanlıştır).
   Doğru cevabı SEN, düzelttiğin soru kökü ve şıkların tıbbi içeriğine ve verilen DERS KAYNAKLARI'na göre belirle.
   Önce her şık için "sik_analizi"nde doğru/yanlış kararını gerekçesiyle yaz, sonra "dogru_secenek"i bu analizden seç.
   Klinik vakalarda verilen değerleri (nabız, tansiyon, şok indeksi = nabız/sistolik TA, GKS, laboratuvar) tek tek hesapla.
   Emin değilsen "cevap_emin": false yaz. Şıkları bir cevaba uysun diye DEĞİŞTİRME.
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
 "sik_analizi": {"A": "DOĞRU: ... ya da YANLIŞ: ... (ifadenin kendisi doğru mu yanlış mı, 1 cümle)", "B": "...", "C": "...", "D": "...", "E": "..."},
 "aciklama_maddeleri": ["...", "..."],
 "dogru_secenek": "A-E (YUKARIDAKİ şık analizi ve açıklamanın gösterdiği şık; onlarla çelişemez)",
 "cevap_emin": true, "cevap_gerekcesi": "...", "kullanilan_kaynaklar": [1, 3],
 "kurul_adi": "TIP310", "ders_adi": "paketteki ders adı", "konu_adi": "paketteki konu adı",
 "degisen_alanlar": ["soru_koku"], "degisiklik_ozeti": "kısa ve somut",
 "YZV": {"degisiklik_ozeti": {"soru_koku_duzeltmesi": "...", "sik_duzeltmesi": "...", "aciklama_duzeltmesi": "...",
          "mufredat_atamasi": "...", "cevap_dogrulamasi": "..."}, "referans_literatur": "varsa standart kaynak"}}"""


def ai_ile_soruyu_duzelt(soru: dict, mufredat_ozeti: str = "") -> tuple[dict | None, str]:
    """Soruyu bulut modeline gönderir. Eski cevap anahtarı verilmez; ders kaynakları (yerel vektör araması) eklenir."""
    # Eski cevap anahtarı modele HİÇ verilmez ve kararda kullanılmaz (kullanıcı kuralı, 2026-10-07)
    girdi = {k: v for k, v in soru.items() if k not in ("dogru_secenek", "aciklama", "kayitli_cevap")}
    ek = ""
    if kok_bozuk(soru):
        ek = ("\nNOT: Bu sorunun kökü bozuk/eksik (bir şıkkın kopyası ya da çok kısa). Şıklara bakarak sorunun ne sorduğunu "
              "kur; kurduğun kök YALNIZ TEK bir şıkkı doğru kılmalı (diğer dört şık kesinlikle yanlış olmalı). Şıkların tıbbi "
              "anlamını değiştirme. Tek cevaplı bir kök kurulamıyorsa cevap_emin=false.\n")
    kaynaklar = kaynaklari_bul(soru.get("soru_koku") or "", soru.get("secenekler") or {})
    soru["_kaynaklar"] = kaynaklar                                # doğrulayıcılar aynı kaynakları görür
    prompt = ("İNCELENECEK SORU:\n" + json.dumps(girdi, ensure_ascii=False, indent=1) + "\n" + ek +
              "\n" + kaynak_metni(kaynaklar) + "\n" + SCHEMA_HINT)
    res, model = call_gemini_json(prompt, system_text())
    if isinstance(res, dict):
        maddeler = [str(m).strip() for m in (res.get("aciklama_maddeleri") or []) if str(m).strip()]
        if maddeler:
            res["aciklama"] = "\n".join(f"• {m}" for m in maddeler)   # site bu satırları madde olarak gösterir
        res.setdefault("review_required", True)
        anlam_koru(soru, res)
        res["_zayif_model"] = any(model.startswith(w) for w in WEAK_GEMINI)
        res["_duzelten_model"] = "gemini:" + model.split(" ")[0]
        cevap_dogrula(soru, res)
        belirsizi_gemini_ile_tamamla(soru, res)
        res.pop("_duzelten_model", None)
        gercek_degisiklikleri_yaz(soru, res)
        res["kaynaklar"] = [{k: c.get(k) for k in ("id", "title", "document_type", "page_number", "similarity")}
                            for c in kaynaklar]
    soru.pop("_kaynaklar", None)
    return res, model


GROUNDING_TYPES = ["lecture_slide", "summary", "transcript"]        # ders materyali (eski soru/AI çıktısı değil)


def kaynaklari_bul(kok: str, secenekler: dict, n: int = 6) -> list[dict]:
    """Soruya anlamca en yakın ders materyali parçaları: yerel embed servisi (e5) + yerel Supabase match_rag_chunks_e5.
    Servis/DB yoksa boş liste (Faz 14 kaynaksız devam eder)."""
    # VARSAYILAN KAPALI: e5-small vektör araması bu sorularda ilgisiz slaytlar getirdi (travma sorusuna hemoglobinopati)
    # ve doğrulayıcıyı yanılttı (2026-10-07 testi). Açmak: PHASE14_KAYNAK=1
    if os.environ.get("PHASE14_KAYNAK") != "1":
        return []
    q = (kok + " " + " ".join(str(v) for v in (secenekler or {}).values() if v))[:1500]
    url = (os.environ.get("LOCAL_SUPABASE_URL") or os.environ.get("SUPABASE_URL") or "http://127.0.0.1:8000").rstrip("/")
    key = os.environ.get("LOCAL_SUPABASE_KEY") or os.environ.get("SUPABASE_SECRET_KEY") or ""
    if not q.strip() or not key:
        return []
    try:
        req = urllib.request.Request(os.environ.get("MEDS_EMBED_URL", "http://127.0.0.1:8091/embed"),
                                     data=json.dumps({"texts": [q], "kind": "query"}).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        vec = json.loads(urllib.request.urlopen(req, timeout=20).read())["vectors"][0]
        body = {"query_embedding": "[" + ",".join(f"{x:.6f}" for x in vec) + "]", "match_count": 60,
                "filter_types": GROUNDING_TYPES, "filter_committee": None}
        req = urllib.request.Request(url + "/rest/v1/rpc/match_rag_chunks_e5", data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", "apikey": key, "Authorization": f"Bearer {key}"})
        rows = json.loads(urllib.request.urlopen(req, timeout=20).read())
        dokum = sinav_dokumu_belgeleri()
        temiz = [r for r in rows if (r.get("similarity") or 0) >= 0.80 and str(r.get("document_id")) not in dokum
                 and not sinav_sayfasi_mi(str(r.get("content") or ""))]
        return temiz[:n]
    except Exception as e:  # noqa: BLE001
        logging.warning(f"[KAYNAK] ders materyali alınamadı: {e}")
        return []


def sinav_sayfasi_mi(t: str) -> bool:
    """ragService.isExamLikePage'in Python eşi: sayfa çıkmış soru/cevap anahtarı gibi mi?"""
    import re
    if re.search(r"Sıra\s*No\s*Cevap|Cevabınız", t, re.I):
        return True
    q = len(re.findall(r"hangisi(dir)?|hangileri|aşağıdakilerden|nedir\s*\?|\?\s*$", t, re.I | re.M))
    opts = len(re.findall(r"(^|\s)[a-eA-E]\s*[).]\s+\S", t, re.M))
    ans = len(re.findall(r"cevap\s*[:=]|doğru cevap", t, re.I))
    num = len(re.findall(r"(^|\s)\d{1,3}\s*[-.)]\s*[^?]{5,120}\?", t))
    return (q >= 2 and opts >= 4) or q >= 3 or ans >= 2 or num >= 2


_DOKUM: set | None = None


def sinav_dokumu_belgeleri() -> set:
    """Sayfalarının yarısından fazlası soru olan 'ders notları' (çıkmış soru PDF'leri, combinepdf vb.) — ders materyali
    sayılmaz (ragService.getExamDumpNoteIds ile aynı ölçüt). data/local_rag_chunks.json'dan bir kez hesaplanır, önbelleklenir."""
    global _DOKUM
    if _DOKUM is not None:
        return _DOKUM
    src = ROOT / "data" / "local_rag_chunks.json"
    cache = ROOT.parent / "meds_temp" / "state" / "sinav_dokumu_belgeleri.json"
    try:
        mt = src.stat().st_mtime
        if cache.exists():
            c = json.loads(cache.read_text(encoding="utf-8"))
            if c.get("mtime") == mt:
                _DOKUM = set(c["ids"])
                return _DOKUM
        d = json.loads(src.read_text(encoding="utf-8"))
        rows = d if isinstance(d, list) else d.get("chunks", [])
        say: dict[str, list[int]] = {}
        for r in rows:
            if r.get("documentType") != "lecture_slide":
                continue
            t = str(r.get("content") or "")
            if len(re.sub(r"[^a-zA-ZçğıöşüÇĞİÖŞÜ]", "", t)) < 40:
                continue
            v = say.setdefault(str(r.get("documentId")), [0, 0])
            v[0] += 1
            v[1] += sinav_sayfasi_mi(t)
        _DOKUM = {k for k, (n, e) in say.items() if e / n >= 0.5}
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({"mtime": mt, "ids": sorted(_DOKUM)}), encoding="utf-8")
        logging.info(f"[KAYNAK] sınav dökümü belge sayısı: {len(_DOKUM)} (ders materyalinden çıkarıldı)")
    except Exception as e:  # noqa: BLE001
        logging.warning(f"[KAYNAK] sınav dökümü listesi hesaplanamadı: {e}")
        _DOKUM = set()
    return _DOKUM


def kaynak_metni(kaynaklar: list[dict]) -> str:
    if not kaynaklar:
        return ""
    parcalar = [f"[{i}] {c.get('title') or ''}{' s.' + str(c['page_number']) if c.get('page_number') else ''}\n"
                f"{' '.join(str(c.get('content') or '').split())[:700]}" for i, c in enumerate(kaynaklar, 1)]
    return "DERS KAYNAKLARI (fakülte ders materyalinden, soruyla anlamca en yakın parçalar):\n" + "\n\n".join(parcalar) + "\n"


def gercek_degisiklikleri_yaz(soru: dict, res: dict) -> None:
    """Koruma/doğrulama modelin değişikliklerini geri aldıysa modelin özeti artık yanlıştır ("düzeltildi" der ama
    değişiklik yoktur). Değişen alanlar özgün ve SON hal karşılaştırılarak yeniden hesaplanır; özet buna göre yazılır,
    modelin özgün özeti 'model_ozeti' alanında saklanır. Geri alınan değişikliğe dayanan açıklama geçersiz işaretlenir."""
    def n(x):
        return " ".join(str(x or "").split()).lower()
    alanlar = []
    if n(res.get("soru_koku")) != n(soru.get("soru_koku")):
        alanlar.append("soru_koku")
    osec, ysec = soru.get("secenekler") or {}, res.get("secenekler") or {}
    if isinstance(osec, dict) and isinstance(ysec, dict) and any(n(osec.get(k)) != n(ysec.get(k)) for k in "ABCDE"):
        alanlar.append("secenekler")
    kayitli = str(soru.get("dogru_secenek") or "").strip().upper()[:1]
    son = str(res.get("dogru_secenek") or "").strip().upper()[:1]
    if son and son != kayitli:
        alanlar.append("dogru_secenek")
    res["cevap_degisti"] = bool(kayitli and son and son != kayitli)
    for k in ("kurul_adi", "ders_adi", "konu_adi", "aciklama_maddeleri"):
        if k in (res.get("degisen_alanlar") or []):
            alanlar.append(k)
    geri_alinan = bool(res.get("anlam_koruma")) or bool(res.get("cevap_belirsiz"))
    if geri_alinan:
        res.setdefault("model_ozeti", res.get("degisiklik_ozeti") or "")   # yeniden doğrulamada ilk özet korunur
        notlar = list(res.get("anlam_koruma") or [])
        d = res.get("cevap_dogrulama") or {}
        if res.get("cevap_belirsiz"):
            notlar.append(f"bağımsız çözücüler aynı şıkta uzlaşamadı (oylar: {d.get('oylar')}) → cevap belirsiz, elle seçilmeli")
        gercek = ", ".join(alanlar) if alanlar else "yok"
        bas = "Otomatik koruma modelin bazı değişikliklerini geri aldı" if res.get("anlam_koruma") else "Cevap belirlenemedi"
        res["degisiklik_ozeti"] = (bas + ": " + "; ".join(notlar) + f". Gerçekte değişen alanlar: {gercek}. Elle inceleyin.")
        # açıklama geçersizliği yalnız cevap_dogrula'nın açıklama↔cevap karşılaştırmasından gelir (kök geri alınması
        # tek başına açıklamayı geçersiz kılmaz; triaj testinde doğru açıklama yanlışlıkla işaretlenmişti)
    yzv = (res.get("YZV") or {}).get("degisiklik_ozeti")
    if isinstance(yzv, dict):                                # modelin gerçekleşmeyen değişiklik iddialarını sil
        for alan, k in (("soru_koku", "soru_koku_duzeltmesi"), ("secenekler", "sik_duzeltmesi"), ("dogru_secenek", "cevap_dogrulamasi")):
            if alan not in alanlar:
                yzv.pop(k, None)
    res["degisen_alanlar"] = alanlar


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
    if ok and yk and not kok_bozuk(soru) and _olumsuz_mu(ok) != _olumsuz_mu(yk):
        res["soru_koku"] = ok
        notlar.append("kökün olumlu/olumsuz yönü değiştirilmişti → özgün kök korundu")
    # Sayısal veri koruması: kökteki değerler (ör. "kapiller dolum <3 sn", nabız 110, Hb 11) değiştirilemez.
    # Model "<3 sn"yi "<2 sn" yapmıştı (2026-10-07 testi) — bu imla değil, vakanın verisini değiştirmektir.
    def _sayilar(t: str) -> list[str]:
        return [x.replace(",", ".") for x in re.findall(r"\d+(?:[.,]\d+)?", t or "")]
    if ok and res.get("soru_koku") and not kok_bozuk(soru):
        from collections import Counter
        eksik = Counter(_sayilar(ok)) - Counter(_sayilar(res["soru_koku"]))
        if eksik:
            res["soru_koku"] = ok
            notlar.append(f"kökteki sayısal değer değiştirilmişti ({', '.join(sorted(eksik))}) → özgün kök korundu")
    osec, ysec = soru.get("secenekler") or {}, res.get("secenekler") or {}
    if isinstance(osec, dict) and isinstance(ysec, dict):
        for k, ov in osec.items():
            ov = str(ov or "").strip()
            yv = str(ysec.get(k) or "").strip()
            if ov and yv and _sayilar(ov) and sorted(_sayilar(ov)) != sorted(_sayilar(yv)):
                ysec[k] = ov                                   # şıktaki sayı da değiştirilemez (1000 mL, 20 mL/kg …)
                notlar.append(f"{k} şıkkındaki sayısal değer değiştirilmişti → özgün şık korundu")
                continue
            if len(ov) >= 3 and yv and difflib.SequenceMatcher(None, ov.lower(), yv.lower()).ratio() < 0.55:
                ysec[k] = ov
                notlar.append(f"{k} şıkkı anlamca değiştirilmişti → özgün şık korundu")
            elif len(ov) >= 3 and yv:
                import re as _re
                kel = lambda t: {w for w in _re.findall(r"[a-zçğıöşü]{4,}", t.lower())}
                dusen = kel(ov) - kel(yv)
                # birleşik yazım düzeltmesi (entübasyondakrikoid → krikoid) değil, gerçek bir kelime düştüyse
                gercek = [w for w in dusen if not any(w in x or x in w or difflib.SequenceMatcher(None, w, x).ratio() >= 0.7
                                                      for x in kel(yv))]   # OCR düzeltmesi (özyolojik→fizyolojik) sayılmaz
                if gercek:
                    notlar.append(f"{k} şıkkında anlam değişmiş olabilir (çıkarılan: {', '.join(sorted(gercek))}) → özgün şık korundu")
                    ysec[k] = ov
        res["secenekler"] = ysec
    if notlar:
        res["review_required"] = True
        res["anlam_koruma"] = notlar
        logging.info("[KORUMA] " + "; ".join(notlar))


def _dogrulayici_sor(prompt: str, max_tokens: int):
    """Önce güçlü doğrulayıcı (gpt-oss); dakikalık sınıra takılırsa bekleyip 3 kez dener, ancak sonra yedek modele geçer.
    (Hemen qwen'e geçmek doğru cevap değişikliklerinin 'zayıf doğrulayıcı' diye reddedilmesine yol açıyordu.)"""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
    import cloud_llm
    for deneme in range(3):
        with _GROQ_KILIT:
            r = cloud_llm.chat(prompt, as_json=True, max_tokens=max_tokens, temperature=0.0, models=VERIFY_MODELS[:1], timeout=120)
        if r:
            return r, (cloud_llm.last_model or {}).get("ad") or VERIFY_MODELS[0]
        time.sleep(20 * (deneme + 1))
    with _GROQ_KILIT:
        r = cloud_llm.chat(prompt, as_json=True, max_tokens=max_tokens, temperature=0.0, models=VERIFY_MODELS[1:], timeout=120)
    return r, (cloud_llm.last_model or {}).get("ad") or ""


def _bagimsiz_cevap(soru_koku: str, secenekler: dict, kaynaklar: list | None = None, modeller: list | None = None) -> tuple[str, str]:
    """Kayıtlı cevabı ve önerilen cevabı GÖRMEDEN soruyu çözer (ücretsiz Groq). (harf, model) ya da ("", "")."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
    try:
        import cloud_llm
    except Exception:
        return "", ""
    prompt = ("Tıp fakültesi sınav sorusu. Adım adım düşün, her şıkkı değerlendir, sonra tek doğru şıkkı seç.\n"
              "Soru kökündeki olumsuzluk ifadelerine (değildir, yanlıştır, olmaz, hariç) özellikle dikkat et.\n\n"
              "Klinik vakada verilen değerleri tek tek hesapla (ör. şok indeksi = nabız / sistolik TA).\n\n" +
              (kaynak_metni(kaynaklar) + "\n" if kaynaklar is not None else "") +
              f"SORU: {soru_koku}\n" + "\n".join(f"{k}) {v}" for k, v in sorted(secenekler.items()) if v) +
              "\n\nAyrıca soru kökü yalnız TEK şıkkı doğru kılıyor mu? Birden fazla şık köke uyuyorsa bunu belirt."
              '\n\nYalnız JSON: {"dogru_secenek": "A-E", "birden_fazla_dogru": false, "uyan_siklar": ["..."], "gerekce": "kısa"}')
    try:
        if modeller:
            sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
            import cloud_llm
            with _GROQ_KILIT:
                r = cloud_llm.chat(prompt, as_json=True, max_tokens=2500, temperature=0.0, models=modeller, timeout=180)
            vm = (cloud_llm.last_model or {}).get("ad") or ""
        else:
            r, vm = _dogrulayici_sor(prompt, 2500)
    except Exception as e:
        logging.warning(f"[DOĞRULAMA] hata: {e}")
        return "", ""
    harf = str((r or {}).get("dogru_secenek") or "").strip().upper()[:1]
    _bagimsiz_cevap.son_coklu = bool((r or {}).get("birden_fazla_dogru"))
    _bagimsiz_cevap.son_uyan = [str(x).strip().upper()[:1] for x in ((r or {}).get("uyan_siklar") or []) if str(x).strip()]
    return (harf if harf in secenekler else ""), vm or "groq"


_bagimsiz_cevap.son_coklu = False
_bagimsiz_cevap.son_uyan = []


def kok_bozuk(soru: dict) -> bool:
    """Özgün kök soru değilse (çok kısa ya da bir şıkkın kopyası, ör. 'Entübasyonda krikoid bası uygulamak.')."""
    import difflib
    k = " ".join(str(soru.get("soru_koku") or "").split()).lower()
    if len(k) < 25:
        return True
    return any(difflib.SequenceMatcher(None, k, " ".join(str(v).split()).lower()).ratio() > 0.75
               for v in (soru.get("secenekler") or {}).values() if v)


def kok_yeniden_yazildi(soru: dict, res: dict) -> bool:
    """Kök baştan kurulduysa (bozuk köktenyeniden yazım ya da anlamca farklı kök) kayıtlı cevap o soruya ait değildir."""
    import difflib
    a = " ".join(str(soru.get("soru_koku") or "").split()).lower()
    b = " ".join(str(res.get("soru_koku") or "").split()).lower()
    return bool(b) and (kok_bozuk(soru) or difflib.SequenceMatcher(None, a, b).ratio() < 0.6)


def _analizden_cevap(soru_koku: str, secenekler: dict, res: dict) -> str:
    """Şık analizindeki DOĞRU/YANLIŞ etiketlerinden cevap: olumlu kökte tek DOĞRU, olumsuz kökte tek YANLIŞ şık."""
    a = res.get("sik_analizi")
    if not isinstance(a, dict):
        return ""
    etiket = {}
    for k, v in a.items():
        t = str(v or "").strip().upper().replace("İ", "I")
        if t.startswith("DOĞRU") or t.startswith("DOGRU"):
            etiket[str(k).upper()[:1]] = True
        elif t.startswith("YANLIŞ") or t.startswith("YANLIS"):
            etiket[str(k).upper()[:1]] = False
    if len(etiket) < len([v for v in secenekler.values() if v]):
        return ""
    hedef = not _olumsuz_mu(soru_koku)
    aday = [k for k, v in etiket.items() if v is hedef]
    return aday[0] if len(aday) == 1 and aday[0] in secenekler else ""


def _aciklamanin_cevabi(soru_koku: str, secenekler: dict, res: dict) -> str:
    """Modelin yazdığı şık analizi + açıklama hangi şıkkı doğru cevap olarak gösteriyor? (işaretlenen harf verilmez)"""
    h = _analizden_cevap(soru_koku, secenekler, res)
    if h:
        return h
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
    try:
        import cloud_llm
    except Exception:
        return ""
    analiz = res.get("sik_analizi") or {}
    maddeler = res.get("aciklama_maddeleri") or [res.get("aciklama") or ""]
    metin = ("\n".join(f"{k}: {v}" for k, v in sorted(analiz.items())) if isinstance(analiz, dict) else str(analiz))
    prompt = ("Aşağıda bir sınav sorusu ve bir öğrencinin yazdığı açıklama var. Tıbbi doğruluğu DEĞERLENDİRME; yalnız bu "
              "açıklamanın hangi şıkkı sorunun cevabı olarak gösterdiğini belirle. Dikkat: açıklama bir şıkkın NEDEN YANLIŞ "
              "olduğunu anlatıyorsa o şık olumlu bir kökte cevap DEĞİLDİR. Soru kökündeki olumsuzluğa dikkat et "
              "(ör. 'hangisi yanlıştır' sorusunda cevap, açıklamanın YANLIŞ dediği şıktır). Açıklama hiçbir şıkkı açıkça "
              "cevap olarak göstermiyorsa 'belirsiz' yaz.\n\n"
              f"SORU: {soru_koku}\n" + "\n".join(f"{k}) {v}" for k, v in sorted(secenekler.items()) if v) +
              f"\n\nŞIK ANALİZİ:\n{metin}\n\nAÇIKLAMA:\n" + "\n".join(str(m) for m in maddeler) +
              '\n\nYalnız JSON: {"aciklamanin_cevabi": "A-E" ya da "belirsiz"}')
    try:
        r, _vm = _dogrulayici_sor(prompt, 2000)
    except Exception:
        return ""
    h = str((r or {}).get("aciklamanin_cevabi") or "").strip().upper()[:1]
    return h if h in secenekler else ""


KOPYA_FILE = OUT_DIR / "kopyalar.json"                         # {kopya_id: asıl_id} — Faz 14'ün atladığı kopyalar


def _kelimeler(t: str) -> set:
    import unicodedata
    t = unicodedata.normalize("NFKD", str(t or "").lower().replace("ı", "i"))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return set(re.findall(r"[a-z]{4,}", t))


def _sayi_imzasi(t) -> tuple:
    """Kökteki sayılar (tarih/başlık artığı olabilecek 4+ haneli sayılar ve 'No' gibi sıra numaraları hariç)."""
    return tuple(sorted(x for x in re.findall(r"\d+(?:[.,]\d+)?", str(t or "")) if len(x.split(".")[0]) <= 3))


def _ayni_soru(k: set, o: set, k2: set, o2: set, sayi: tuple = (), sayi2: tuple = ()) -> bool:
    """İki soru aynı mı? Kök+şık kelimeleri birlikte karşılaştırılır (şıkları köke karışmış, başlık artıklı ya da
    şık sırası farklı kopyalar da yakalanır); şıkları neredeyse aynı olan kısa köklerde kök eşiği düşüktür."""
    j = lambda a, b: len(a & b) / max(1, len(a | b))
    tum, tum2 = k | o, k2 | o2
    if len(tum) < 8 or len(tum2) < 8:
        return False
    if sayi and sayi2 and sayi != sayi2:
        return False                                            # farklı vaka verisi (yaş, nabız, doz…) → farklı soru
    if len(o) < 6 or len(o2) < 6:
        # genel şıklar (Yeşil/Sarı/Kırmızı…): soruyu ayıran vakadır → yalnız uzun ve neredeyse aynı kök kopya sayılır
        return j(k, k2) >= 0.9 and min(len(k), len(k2)) >= 20
    return (j(k, k2) >= 0.8 and j(o, o2) >= 0.7) or j(tum, tum2) >= 0.75 or (j(o, o2) >= 0.9 and len(o) >= 6 and j(k, k2) >= 0.5)


class KopyaDizini:
    """Neredeyse aynı soruları bulur: kök kelimelerinin Jaccard benzerliği ≥ 0.8 VE şık kelimeleri ≥ 0.7.
    (OCR artığı, tarih başlığı ya da küçük yazım farkı olan aynı soru; veritabanında ~160 çift var.)"""

    def __init__(self):
        self.kayit: list[tuple[str, set, set, tuple]] = []
        self.ters: dict[str, set] = {}

    def ekle(self, qid: str, src: dict):
        k, o = _kelimeler(src.get("soru_koku")), _kelimeler(" ".join(str(v) for v in (src.get("secenekler") or {}).values()))
        if len(k) < 4:
            return
        i = len(self.kayit)
        self.kayit.append((qid, k, o, _sayi_imzasi(src.get("soru_koku"))))
        for w in k:
            self.ters.setdefault(w, set()).add(i)

    def yukle_incelenenler(self):
        if not REVIEWS_FILE.exists():
            return
        for line in REVIEWS_FILE.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                self.ekle(str(r.get("question_id")), r.get("source") or {})
            except Exception:
                continue

    def kopyasi_mi(self, qid: str, src: dict) -> str:
        k, o = _kelimeler(src.get("soru_koku")), _kelimeler(" ".join(str(v) for v in (src.get("secenekler") or {}).values()))
        if len(k) < 4:
            return ""
        aday: dict[int, int] = {}
        for w in k:
            for i in self.ters.get(w, ()):
                aday[i] = aday.get(i, 0) + 1
        for i, ortak in sorted(aday.items(), key=lambda x: -x[1])[:50]:
            aid, k2, o2, n2 = self.kayit[i]
            if aid == qid:
                continue
            if _ayni_soru(k, o, k2, o2, _sayi_imzasi(src.get("soru_koku")), n2):
                return aid
        return ""


def birlestirilen_kopyalar() -> dict:
    """meds_database_v2/soru_birlestirme/birlestirmeler.json: {gizlenen_kopya_id: asil_id} (ayrılan gruplar hariç)."""
    f = OUT_DIR.parent / "soru_birlestirme" / "birlestirmeler.json"
    try:
        out = {}
        for g in json.loads(f.read_text(encoding="utf-8")).get("gruplar", []):
            if g.get("durum") != "ayrildi":
                out.update({u: g["asil"] for u in g.get("uyeler", []) if u != g["asil"]})
        return out
    except Exception:
        return {}


def kopya_kaydet(kopya_id: str, asil_id: str):
    try:
        d = json.loads(KOPYA_FILE.read_text(encoding="utf-8")) if KOPYA_FILE.exists() else {}
    except Exception:
        d = {}
    d[kopya_id] = asil_id
    KOPYA_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


GEMINI_COZUCU = ["gemini:gemini-flash-latest", "gemini:gemini-3.5-flash", "gemini:gemini-flash-lite-latest",
                 "gemini:gemini-3.5-flash-lite"]                 # ücretsiz anahtarlar (cloud_llm); Flash yoksa Lite


def belirsizi_gemini_ile_tamamla(soru: dict, res: dict) -> None:
    """Çözücüler uzlaşamadıysa soru Gemini'ye (kör: eski cevap ve diğer oylar gösterilmeden) ayrıca sorulur ve toplam
    3 cevap şıkkı toplanır. Soru 'şüpheli cevap' olarak işaretlenir (/test/cikmis → Şüpheli). 3 cevaptan en az ikisi
    aynıysa o şık öneri olarak yazılır ama soru yine şüpheli kalır; üçü de farklıysa cevap boş kalır."""
    d = res.get("cevap_dogrulama") or {}
    if d.get("sonuc") not in ("belirsiz", "ayni_model_iki_oy_gecersiz") and not res.get("cevap_belirsiz"):
        return
    sec = res.get("secenekler") or soru.get("secenekler") or {}
    kok = res.get("soru_koku") or soru.get("soru_koku") or ""
    oylar = {k: v for k, v in (d.get("oylar") or {}).items() if isinstance(v, str) and len(v) == 1}
    modeller = {"gpt_oss": d.get("dogrulayici_model"), "ucuncu": d.get("ucuncu_model")}
    cevaplar = [{"cozucu": k, "model": modeller.get(k) or res.get("_duzelten_model") or k, "cevap": v} for k, v in oylar.items()]
    # aynı modelin ikinci oyu sayılmaz
    gorulen, tekil = set(), []
    for c in cevaplar:
        if c["model"] in gorulen:
            continue
        gorulen.add(c["model"])
        tekil.append(c)
    cevaplar = tekil
    deneme = 0
    while len(cevaplar) < 3 and deneme < 2:
        deneme += 1
        adaylar = [m for m in GEMINI_COZUCU if m not in gorulen]
        if not adaylar:
            break
        h, m = _bagimsiz_cevap(kok, sec, soru.get("_kaynaklar"), modeller=adaylar)
        if h and m and m not in gorulen:
            gorulen.add(m)
            cevaplar.append({"cozucu": "gemini", "model": m, "cevap": h})
        elif m:
            gorulen.add(m)                                      # yanıt vermeyen modeli tekrar deneme
    say: dict[str, int] = {}
    for c in cevaplar:
        say[c["cevap"]] = say.get(c["cevap"], 0) + 1
    kazanan = max(say, key=say.get) if say else ""
    if kazanan and say[kazanan] >= 2:
        res["dogru_secenek"] = kazanan
        res["cevap_belirsiz"] = False
        d["sonuc"] = "gemini_ile_cogunluk_supheli"
    else:
        res["dogru_secenek"] = ""
        res["cevap_belirsiz"] = True
        d["sonuc"] = "gemini_ile_de_belirsiz"
    res["cevap_emin"] = False
    res["supheli_cevap"] = True
    res["cevap_secenekleri"] = cevaplar                         # toplam 3 cevap (çözücü, model, şık)
    d["oylar"] = {**(d.get("oylar") or {}), **{"gemini": c["cevap"] for c in cevaplar if c["cozucu"] == "gemini"}}
    res["cevap_dogrulama"] = d
    logging.info(f"[DOĞRULAMA] belirsiz → Gemini ile {len(cevaplar)} cevap: "
                 + ", ".join(f"{c['model']}={c['cevap']}" for c in cevaplar) + f" → {res['dogru_secenek'] or 'BELİRSİZ'} (şüpheli)")


def cevap_uyusmazligi(res: dict) -> bool:
    """Çözücüler aynı şıkta birleşmedi mi? (en az bir oy farklıysa ya da cevap belirsizse) → "Cevap Belirsiz" kategorisi."""
    d = (res or {}).get("cevap_dogrulama") or {}
    oylar = {v for v in (d.get("oylar") or {}).values() if isinstance(v, str) and len(v) == 1}
    return bool(res.get("cevap_belirsiz")) or len(oylar) > 1 or d.get("sonuc") == "belirsiz"


def cevap_dogrula(soru: dict, res: dict) -> None:
    """Cevap ESKİ CEVAP ANAHTARI KULLANILMADAN belirlenir (kullanıcı kuralı): aynı ders kaynaklarını gören bağımsız
    çözücülerin çoğunluk oyu — (1) soruyu düzelten modelin şık analizinin gösterdiği şık, (2) gpt-oss-120b (kör),
    (3) ilk ikisi ayrışırsa farklı aileden üçüncü çözücü. En az iki oy aynı şıkta değilse cevap BELİRSİZ bırakılır
    (dogru_secenek="") ve soru elle incelemeye düşer. Açıklamanın savunduğu şık son cevapla çelişirse açıklama geçersiz
    işaretlenir. Eski cevap yalnız bilgi olarak saklanır (res['cevap_dogrulama']['eski_anahtar'])."""
    eski = str(soru.get("dogru_secenek") or "").strip().upper()[:1]
    oneri = str(res.get("dogru_secenek") or "").strip().upper()[:1]
    sec = res.get("secenekler") or soru.get("secenekler") or {}
    if not isinstance(sec, dict):
        return
    kok = res.get("soru_koku") or soru.get("soru_koku") or ""
    kay = soru.get("_kaynaklar")
    ac_harf = _aciklamanin_cevabi(kok, sec, res)
    if ac_harf and oneri and ac_harf != oneri:
        logging.info(f"[DOĞRULAMA] modelin şık analizi/açıklaması {ac_harf}, işaretlediği {oneri} → model oyu {ac_harf} sayılır")
    model_oyu = ac_harf or oneri                               # modelin gerekçesinin gösterdiği şık esas alınır
    zayif = res.pop("_zayif_model", False)
    if zayif:
        model_oyu = ""                                         # Flash-Lite cevabı oy sayılmaz (düşünmeden seçer)
    harf, vmodel = _bagimsiz_cevap(kok, sec, kay)
    coklu = _bagimsiz_cevap.son_coklu
    oylar = {"duzelten_model": model_oyu or ("(Lite, sayılmadı)" if zayif else ""), "gpt_oss": harf}
    d = {"eski_anahtar": eski, "oneri": oneri, "dogrulayici": harf, "dogrulayici_model": vmodel,
         "aciklama_gosterdigi": ac_harf, "kaynak_sayisi": len(kay or [])}
    if not (model_oyu and harf and model_oyu == harf):
        # Üçüncü çözücü doğrulayıcıdan FARKLI model olmalı (aynı modelin iki oyu bağımsız doğrulama değildir)
        adaylar = [m for m in ["gemini:gemini-flash-latest", "gemini:gemini-3.5-flash", "groq:openai/gpt-oss-120b",
                               "groq:qwen/qwen3.8-27b"] if m != vmodel]
        h3, m3 = _bagimsiz_cevap(kok, sec, kay, modeller=adaylar)
        if m3 and m3 == vmodel:
            h3 = ""                                            # yine aynı modele düştüyse oy sayılmaz
        oylar["ucuncu"] = h3
        d["ucuncu"], d["ucuncu_model"] = h3, m3
        coklu = coklu or _bagimsiz_cevap.son_coklu
    sayim: dict[str, int] = {}
    for v in oylar.values():
        if v and len(v) == 1:
            sayim[v] = sayim.get(v, 0) + 1
    kazanan = max(sayim, key=sayim.get) if sayim else ""
    d["oylar"] = oylar
    if kazanan and sayim[kazanan] >= 2:
        res["dogru_secenek"] = kazanan
        res["cevap_belirsiz"] = False
        res["cevap_emin"] = sayim[kazanan] == len([v for v in oylar.values() if v and len(v) == 1]) and not coklu
        d["sonuc"] = "oybirligi" if res["cevap_emin"] else "cogunluk"
    else:
        res["dogru_secenek"] = ""                               # çözücüler uzlaşamadı: cevap işaretlenmez
        res["cevap_emin"] = False
        res["cevap_belirsiz"] = True
        d["sonuc"] = "belirsiz"
    if coklu:
        d["birden_fazla_dogru"] = _bagimsiz_cevap.son_uyan or True
        res["cevap_emin"] = False
    if kok_yeniden_yazildi(soru, res):
        d["kok_yeniden_yazildi"] = True
    son = res["dogru_secenek"]
    res.pop("aciklama_gecersiz", None)
    if ac_harf != son:
        d["aciklama_son_cevapla_celisiyor"] = True             # açıklama başka şıkkı savunuyor ya da hiçbirini
        res["aciklama_gecersiz"] = True
    res["review_required"] = True
    res["cevap_dogrulama"] = d
    logging.info(f"[DOĞRULAMA] oylar {oylar} → {son or 'BELİRSİZ'} ({d['sonuc']}) · eski anahtar {eski or '-'} (kararda kullanılmadı)")


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


from contextlib import contextmanager


@contextmanager
def dosya_kilidi():
    """reviews.jsonl için süreçler arası kilit (Faz 14 işleri ve phase14_belirsiz_gemini.py)."""
    import fcntl
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "reviews.lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)


def kayit_yaz(out_reviews, s_id: str, src: dict, ai_sonuc: dict, model_used: str, stats: dict,
              islenmisler: set, kopya_dizini) -> dict | None:
    """İnceleme kaydını yazar + checkpoint. Kilitli: aynı soru iki kez yazılamaz (paralel kipte de)."""
    ratio = support_ratio(src, ai_sonuc)
    changed = ai_sonuc.get("degisen_alanlar") or []
    if not changed and ai_sonuc.get("YZV", {}).get("degisiklik_yapildi_mi"):
        changed = ["soru_koku", "aciklama"]
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
    if cevap_uyusmazligi(ai_sonuc):
        record["status"] = "review_required"
        record["answer_doubtful"] = True                      # /test/cikmis → "Cevap Belirsiz" kategorisi (+ cevap anketi)
    if ai_sonuc.get("supheli_cevap"):
        record["status"] = "review_required"
        record["suspicious"] = True                           # /test/cikmis → "Şüpheli" (3 cevap: proposal.cevap_secenekleri)
        record["suspicious_at"] = datetime.utcnow().isoformat() + "Z"
    with _KILIT, dosya_kilidi():
        if s_id in load_checkpoints() or s_id in islenmisler:
            logging.warning(f"Soru #{s_id} zaten işlenmiş; ikinci kayıt YAZILMADI")
            return None
        # Uzun süre açık tutulan tutamaç kullanılmaz: başka süreç dosyayı yeniden yazarsa (os.replace) eklenen satır
        # eski dosyaya giderdi (2026-10-08'de 15 kayıt böyle kayboldu). Her kayıtta dosya yeniden açılır.
        with REVIEWS_FILE.open("a", encoding="utf-8") as fo:
            fo.write(json.dumps(record, ensure_ascii=False) + "\n")
        kopya_dizini.ekle(s_id, src)
        stats["islenen"] += 1
        stats["degisiklik_onerisi"] += int(bool(changed))
        stats["inceleme_gerekli"] += int(record["status"] == "review_required")
        save_checkpoint(islenmisler, s_id)
    logging.info(f"✓ Soru #{s_id} inceleme katmanına yazıldı ({record['status']}, kanıt {ratio}, {model_used}).")
    return record


ARALIKLAR = [60, 600, 1800]          # paralel ücretsiz kip: başarısızlıktan sonra bekleme (1 dk → 10 dk → 30 dk)


def ucretsiz_paralel(questions: list, limit: int, islenmisler: set, stats: dict) -> None:
    """Yalnız ücretsiz anahtarlar, her anahtar ayrı iş parçacığında, kendi soru listesiyle.
    Sorular baştan seçilir (işlenmiş/kopya/gizli kopya hariç, seçim içinde de kopya yok) ve anahtarlara sırayla
    dağıtılır; bir soru yalnız bir anahtara atanır. Her anahtar: başarıda bekleme sıfırlanır ve hemen sıradaki soru;
    başarısızlıkta 1 dk → 10 dk → 30 dk (sonra 30 dk'da kalır) bekleyip AYNI soruyu yeniden dener."""
    anahtarlar = [lb for lb, _k, pd in _key_tiers() if not pd]
    if not anahtarlar:
        logging.error("Ücretsiz Gemini anahtarı yok")
        return
    kopya_dizini = KopyaDizini()
    kopya_dizini.yukle_incelenenler()
    gizli = birlestirilen_kopyalar()
    secim: list[tuple[str, dict]] = []
    for q in questions:
        if len(secim) >= limit:
            break
        s_id = str(q.get("id") or "")
        if not s_id or s_id in islenmisler:
            continue
        src = source_view(q)
        if len(src["soru_koku"].strip()) < 15 or len(src["secenekler"]) < 4:
            continue
        asil = gizli.get(s_id) or kopya_dizini.kopyasi_mi(s_id, src)
        if asil:
            kopya_kaydet(s_id, asil)
            save_checkpoint(islenmisler, s_id)
            stats["kopya"] = stats.get("kopya", 0) + 1
            logging.info(f"Soru #{s_id} atlandı: #{asil} ile aynı soru (kopya)")
            continue
        kopya_dizini.ekle(s_id, src)                           # seçim içindeki kopyalar da ayrı anahtara gitmesin
        secim.append((s_id, src))
    if not secim:
        # İncelenecek soru kalmadı: otomatik ücretsiz kip kapatılır (sunucu bekçisi boşuna yeniden başlatmasın)
        try:
            ayar = json.loads(FAZ14_AYAR.read_text(encoding="utf-8")) if FAZ14_AYAR.exists() else {}
            if ayar.get("otomatik_ucretsiz"):
                ayar["otomatik_ucretsiz"] = False
                FAZ14_AYAR.write_text(json.dumps(ayar, ensure_ascii=False, indent=1), encoding="utf-8")
                logging.info("İncelenecek soru kalmadı → otomatik ücretsiz inceleme kapatıldı")
        except Exception as e:  # noqa: BLE001
            logging.warning(f"Ayar güncellenemedi: {e}")
        return
    kuyruklar: dict[str, list] = {a: [] for a in anahtarlar}
    for i, item in enumerate(secim):
        kuyruklar[anahtarlar[i % len(anahtarlar)]].append(item)
    atanan = [sid for k in kuyruklar.values() for sid, _ in k]
    assert len(atanan) == len(set(atanan)), "bir soru birden çok anahtara atandı"
    logging.info(f"Paralel ücretsiz kip: {len(secim)} soru · {len(anahtarlar)} anahtar · "
                 + ", ".join(f"{a}: {len(v)}" for a, v in kuyruklar.items()))
    durum_f = OUT_DIR / "paralel_durum.json"
    durum: dict[str, dict] = {a: {"kalan": len(v), "cozulen": 0, "bekleme_bitis": None, "ardisik_hata": 0}
                              for a, v in kuyruklar.items()}

    def durum_yaz():
        with _KILIT:
            durum_f.write_text(json.dumps({"guncelleme": datetime.now().isoformat(timespec="seconds"),
                                           "anahtarlar": durum}, ensure_ascii=False, indent=1), encoding="utf-8")

    durum_yaz()
    yeni_dizin = KopyaDizini()                                  # kayıt sırasında (kilitli) güncellenir

    def isci(etiket: str, kuyruk: list):
        _YEREL.anahtar = etiket
        hata = 0
        soru_hata: dict[str, int] = {}
        with REVIEWS_FILE.open("a", encoding="utf-8") as out:
            while kuyruk:
                s_id, src = kuyruk[0]
                with _KILIT:
                    zaten = s_id in load_checkpoints() or s_id in islenmisler
                if zaten:                                       # başka yoldan işlendiyse yeniden çözülmez
                    kuyruk.pop(0)
                    continue
                logging.info(f"[{etiket}] Soru #{s_id} inceleniyor ({len(kuyruk)} kaldı)")
                _YEREL.yanit_alindi = False
                try:
                    res, model = ai_ile_soruyu_duzelt(dict(src))
                except Exception as e:  # noqa: BLE001
                    logging.warning(f"[{etiket}] Soru #{s_id} hata: {e}")
                    res, model = None, ""
                if isinstance(res, dict):
                    kayit_yaz(out, s_id, src, res, model, stats, islenmisler, yeni_dizin)
                    kuyruk.pop(0)
                    hata = 0
                    durum[etiket].update(kalan=len(kuyruk), cozulen=durum[etiket]["cozulen"] + 1,
                                         bekleme_bitis=None, ardisik_hata=0)
                    durum_yaz()
                    continue                                    # başarı: beklemeden sıradaki soru
                if getattr(_YEREL, "yanit_alindi", False):
                    # Model yanıt verdi ama soru işlenemedi (bozuk JSON vb.): sorun soruda, anahtarda değil.
                    soru_hata[s_id] = soru_hata.get(s_id, 0) + 1
                    if soru_hata[s_id] >= 2:
                        kuyruk.pop(0)                           # bu turda bırakılır; checkpoint'e girmez, sonra yeniden denenir
                        stats["hata"] += 1
                        logging.warning(f"[{etiket}] Soru #{s_id} iki kez işlenemedi; bu turda bırakıldı")
                        durum[etiket].update(kalan=len(kuyruk))
                        durum_yaz()
                    continue                                    # anahtar sağlıklı: beklemeden devam
                bekle = ARALIKLAR[min(hata, len(ARALIKLAR) - 1)]
                hata += 1
                bitis = datetime.now().timestamp() + bekle
                durum[etiket].update(bekleme_bitis=datetime.fromtimestamp(bitis).isoformat(timespec="seconds"),
                                     ardisik_hata=hata)
                durum_yaz()
                logging.info(f"[{etiket}] yanıt yok · {hata}. ardışık hata · {bekle // 60} dk sonra #{s_id} yeniden denenecek")
                time.sleep(bekle)
                with _KILIT:                                    # günlük kota yenilenmiş olabilir: bu anahtar yeniden denensin
                    for k in [k for k in _daily_exhausted if k[0] == etiket]:
                        _daily_exhausted.discard(k)
        durum[etiket].update(kalan=0, bekleme_bitis=None)
        durum_yaz()
        logging.info(f"[{etiket}] kendi soruları bitti ({durum[etiket]['cozulen']} çözüldü)")

    isler = [threading.Thread(target=isci, args=(a, k), name=a, daemon=True) for a, k in kuyruklar.items() if k]
    for t in isler:
        t.start()
    for t in isler:
        t.join()


def main() -> int:
    parser = argparse.ArgumentParser(description="Faz 14 Bulut Tabanlı Çıkmış Soru İyileştirme")
    parser.add_argument("--limit", type=int, default=10, help="Bu çalıştırmada incelenecek soru sayısı")
    parser.add_argument("--chunk-size", type=int, default=30, help="API'den bir seferde çekilecek soru sayısı")
    parser.add_argument("--direct-apply", action="store_true", help="İnceleme katmanına yazmanın yanı sıra /api üzerinden de doğrudan uygula")
    parser.add_argument("--ucretli-izin", action="store_true", help="ELLE başlatma: ücretsizler tükenince ücretli anahtara geç")
    parser.add_argument("--ucretsiz-otomatik", action="store_true", help="otomatik kip: yalnız ücretsiz, günlük kota bitene kadar")
    parser.add_argument("--ucretsiz-paralel", action="store_true",
                        help="yalnız ücretsiz anahtarlar, her anahtar kendi sorularını paralel çözer (1/10/30 dk aralık)")
    args = parser.parse_args()
    # Aynı anda tek Faz 14: ikinci başlatma aynı soruları yeniden çözmesin
    import fcntl
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _kilit_f = open(OUT_DIR / "faz14.lock", "w")
    try:
        fcntl.flock(_kilit_f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logging.error("Faz 14 zaten çalışıyor (faz14.lock); ikinci çalıştırma başlatılmadı")
        return 0
    if args.ucretsiz_paralel:
        args.ucretli_izin = False
    global ALLOW_PAID
    ALLOW_PAID = bool(args.ucretli_izin) and not args.ucretsiz_otomatik
    if args.ucretsiz_otomatik:
        args.limit = max(args.limit, 5000)                  # kota bitene kadar
    logging.info(f"Kip: {'ELLE (önce ücretsiz, sonra ücretli)' if ALLOW_PAID else 'YALNIZ ÜCRETSİZ' + (' · otomatik' if args.ucretsiz_otomatik else '') + (' · PARALEL' if args.ucretsiz_paralel else '')} · limit {args.limit}")

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
    if args.ucretsiz_paralel:
        ucretsiz_paralel(questions, args.limit, islenmisler, stats)

    kopya_dizini = KopyaDizini()
    kopya_dizini.yukle_incelenenler()
    gizli = birlestirilen_kopyalar()                         # sitede gizlenen kopyalar (asıl soru incelenir)
    with REVIEWS_FILE.open("a", encoding="utf-8") as out_reviews:
        for q in ([] if args.ucretsiz_paralel else questions):
            s_id = str(q.get("id") or "")
            if not s_id or s_id in islenmisler:
                continue
            if stats["islenen"] >= args.limit:
                break

            src = source_view(q)
            if len(src["soru_koku"].strip()) < 15 or len(src["secenekler"]) < 4:
                continue
            asil = gizli.get(s_id) or kopya_dizini.kopyasi_mi(s_id, src)
            if asil:
                # Aynı soru başka kimlikle zaten incelendi (farklı sınav dökümünden ikinci kez girilmiş):
                # yeniden incelenmez, kota harcanmaz, /test/cikmis'e ikinci kez düşmez.
                kopya_kaydet(s_id, asil)
                save_checkpoint(islenmisler, s_id)
                stats["kopya"] = stats.get("kopya", 0) + 1
                logging.info(f"Soru #{s_id} atlandı: #{asil} ile aynı soru (kopya)")
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

            record = kayit_yaz(out_reviews, s_id, src, ai_sonuc, model_used, stats, islenmisler, kopya_dizini)
            if record is None:
                continue

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
