#!/usr/bin/env python3
"""
Ortak bulut LLM istemcisi (yerel model yok). Faz 5/6/7 v2, hakem ve lib.chat bunu kullanır.

Model zinciri (yalnız ücretsiz anahtarlar; faturalı GEMINI_BILLED_KEY hiçbir fazda kullanılmaz, MEDS_FREE_ONLY=1):
  groq:openai/gpt-oss-120b → groq:qwen/qwen3.8-27b → [zen:muse-spark-1.3-contributor-free, OPENCODE_API_KEY varsa]
  → gemini:gemini-flash-latest → gemini:gemini-3.5-flash
  (+ MEDS_CLOUD_EXTRA_MODELS, ör. "openrouter:meta/muse-spark-1.3" — OpenRouter hesabında model açılınca)
Kota: 429 "günlük" yanıtı veren model o gün bir daha denenmez (meds_temp/state/cloud_llm.json, süreçler arası);
dakikalık 429'da kısa beklenir. 400/401/403/404 veren model bu süreçte atlanır. Anahtar havuzu sırayla denenir.
Hiçbir model yanıt vermezse None döner (çağıran kendi "atla, sonra dene" mantığını uygular; boş sonuç yazılmaz).
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or ROOT.parent / "meds_temp")
STATE = TEMP / "state" / "cloud_llm.json"
UA = "MedSor/1.0"

DEFAULT_CHAIN = ["groq:openai/gpt-oss-120b", "groq:qwen/qwen3.8-27b", "gemini:gemini-flash-latest", "gemini:gemini-3.5-flash"]


def _env() -> dict:
    env = {}
    try:
        for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.split(" #")[0].strip().strip('"').strip("'")
    except OSError:
        pass
    env.update({k: v for k, v in os.environ.items() if v})
    return env


ENV = _env()
KEYS = {
    "groq": [k for k in (ENV.get("GROQ_API_KEY"), ENV.get("GROQ_API_KEY_2")) if k],
    "gemini": [k for k in (ENV.get("GEMINI_API_KEY"), ENV.get("GEMINI_FREE_KEY_2"), ENV.get("GEMINI_BACKUP_KEY")) if k],
    "openrouter": [k for k in (ENV.get("MUSE_SPARK_API_KEY"), ENV.get("OPENROUTER_API_KEY")) if k],
    # OpenCode Zen: ücretsiz Muse Spark (muse-spark-1.3-contributor-free). opencode.ai'den alınan anahtar gerekir;
    # "contributor" sürümlerinde istemler sağlayıcının model geliştirmesinde kullanılabilir.
    "zen": [k for k in (ENV.get("OPENCODE_API_KEY"),) if k],
}
ZEN_FREE = "zen:muse-spark-1.3-contributor-free"


def chain() -> list[str]:
    extra = [m.strip() for m in (ENV.get("MEDS_CLOUD_EXTRA_MODELS") or "").split(",") if m.strip()]
    base = [m.strip() for m in (ENV.get("MEDS_CLOUD_CHAIN") or "").split(",") if m.strip()] or DEFAULT_CHAIN
    # Ücretsiz Muse Spark anahtar varsa zincire kendiliğinden girer (Groq'tan sonra, Gemini'den önce)
    if KEYS["zen"] and ZEN_FREE not in base and ZEN_FREE not in extra:
        i = next((j for j, m in enumerate(base) if m.startswith("gemini:")), len(base))
        base = base[:i] + [ZEN_FREE] + base[i:]
    return base + extra


# ---- günlük kota durumu (süreçler arası)
_skip_session: set[str] = set()


def _load_state() -> dict:
    try:
        s = json.loads(STATE.read_text(encoding="utf-8"))
        if s.get("gun") == time.strftime("%Y-%m-%d"):
            return s
    except Exception:  # noqa: BLE001
        pass
    return {"gun": time.strftime("%Y-%m-%d"), "kota_dolu": [], "sayac": {}}


def _save_state(s: dict):
    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        tmp = STATE.with_suffix(".tmp")
        tmp.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
        tmp.replace(STATE)
    except OSError:
        pass


def _mark_exhausted(model: str):
    s = _load_state()
    if model not in s["kota_dolu"]:
        s["kota_dolu"].append(model)
    _save_state(s)


def _count(model: str):
    s = _load_state()
    s["sayac"][model] = s["sayac"].get(model, 0) + 1
    _save_state(s)


# ---- sağlayıcı çağrıları
def _post(url: str, body: dict, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "User-Agent": UA, **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _openai_style(base: str, key: str, model: str, system: str | None, prompt: str, as_json: bool, max_tokens: int,
                  temperature: float, timeout: int) -> str:
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    body = {"model": model, "messages": msgs, "temperature": temperature, "max_tokens": max_tokens}
    if as_json:
        body["response_format"] = {"type": "json_object"}
    d = _post(f"{base}/chat/completions", body, {"Authorization": f"Bearer {key}"}, timeout)
    return d["choices"][0]["message"].get("content") or ""


def _gemini(key: str, model: str, system: str | None, prompt: str, as_json: bool, max_tokens: int, temperature: float,
            timeout: int) -> str:
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    if as_json:
        body["generationConfig"]["responseMimeType"] = "application/json"
    d = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", body, {"x-goog-api-key": key}, timeout)
    return d["candidates"][0]["content"]["parts"][0]["text"]


def _call(spec: str, key: str, system, prompt, as_json, max_tokens, temperature, timeout) -> str:
    prov, model = spec.split(":", 1)
    if prov == "groq":
        return _openai_style("https://api.groq.com/openai/v1", key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if prov == "gemini":
        return _gemini(key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if prov == "zen":
        return _openai_style("https://opencode.ai/zen/v1", key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if prov == "openrouter":
        base = (ENV.get("MUSE_SPARK_BASE_URL") or "https://openrouter.ai/api/v1").rstrip("/")
        return _openai_style(base, key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    raise ValueError(f"bilinmeyen sağlayıcı: {prov}")


def _parse_json(raw: str):
    raw = re.sub(r"<think>.*?</think>", "", raw or "", flags=re.S).strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


last_model: dict = {"ad": None}


def chat(prompt: str, system: str | None = None, as_json: bool = False, max_tokens: int = 2048,
         temperature: float = 0.1, timeout: int = 90, models: list[str] | None = None, log=None):
    """Zincirdeki ilk çalışan modelden yanıt (as_json: dict). Hiçbiri yanıt vermezse None.
    models: zinciri bu çağrı için değiştirir (ör. konsensüs için farklı model ailesi)."""
    exhausted = set(_load_state()["kota_dolu"])
    for spec in models or chain():
        if spec in exhausted or spec in _skip_session:
            continue
        prov = spec.split(":", 1)[0]
        keys = KEYS.get(prov) or []
        if not keys:
            _skip_session.add(spec)
            continue
        for key in keys:
            done_with_key = False
            for attempt in range(2):
                try:
                    raw = _call(spec, key, system, prompt, as_json, max_tokens, temperature, timeout)
                except urllib.error.HTTPError as e:
                    body = e.read()[:400].decode("utf-8", "replace")
                    if e.code == 429:
                        if any(t in body for t in ("per day", "TPD", "RPD", "PerDay", "daily", "quota")):
                            done_with_key = True        # bu anahtarın günlük kotası; sıradaki anahtar
                            break
                        time.sleep(20)
                        continue
                    if e.code in (400, 401, 403, 404):
                        if log:
                            log(f"{spec}: HTTP {e.code} — bu süreçte atlanıyor")
                        _skip_session.add(spec)
                        done_with_key = True
                        break
                    time.sleep(5)
                    continue
                except Exception:  # noqa: BLE001
                    time.sleep(3)
                    continue
                out = _parse_json(raw) if as_json else re.sub(r"<think>.*?</think>", "", raw or "", flags=re.S).strip()
                if out:
                    last_model["ad"] = spec
                    _count(spec)
                    return out
                break                                   # boş/bozuk yanıt: sıradaki modele
            if spec in _skip_session:
                break
            if not done_with_key:
                break
        else:
            # tüm anahtarların günlük kotası doldu
            if log:
                log(f"{spec}: günlük kota doldu, bugün atlanacak")
            _mark_exhausted(spec)
    return None


if __name__ == "__main__":
    import sys
    r = chat(sys.argv[1] if len(sys.argv) > 1 else 'JSON ver: {"cevap": "böbreğin fonksiyonel birimi"}', as_json=True, max_tokens=200,
             log=print)
    print(last_model["ad"], r)


# ---- Görsel OCR (Gemini; "düşünme" kapalı, sıcaklık 0) -------------------------------------------------------
VISION_CHAIN = ["gemini:gemini-3.5-flash", "gemini:gemini-flash-latest"]
VISION_PROMPT = ("Bu görüntü bir tıp fakültesi ders slaytı, ders notu ya da sınav sayfasıdır. İçindeki metni BİREBİR yaz. "
                 "Sayfa çok sütunluysa önce sol sütunu baştan sona, sonra sağ sütunu yaz. Başlıkları, madde işaretlerini, "
                 "soru numaralarını ve şıkları (A/B/C veya a/b/c) ayrı satırlarda koru. Tablo varsa Markdown tablosu olarak ver. "
                 "Türkçe karakterleri ve Latince tıbbi terimleri olduğu gibi koru. Okuyamadığın yere [okunamadı] yaz; tahmin etme, "
                 "ekleme yapma, imla düzeltme yapma, açıklama yazma. Görüntüde okunabilir metin yoksa yalnızca BOŞ yaz.")


def vision_ocr(png_bytes: bytes, prompt: str = VISION_PROMPT, timeout: int = 120, log=None) -> str | None:
    """Görüntüdeki metni Gemini ile çıkarır. Yanıt yoksa None (çağıran Tesseract'a düşer)."""
    import base64
    exhausted = set(_load_state()["kota_dolu"])
    data = base64.b64encode(png_bytes).decode()
    for spec in VISION_CHAIN:
        if spec in exhausted or spec in _skip_session:
            continue
        model = spec.split(":", 1)[1]
        keys = KEYS["gemini"]
        all_daily = bool(keys)
        for key in keys:
            body = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/png", "data": data}}, {"text": prompt}]}],
                    "generationConfig": {"temperature": 0, "maxOutputTokens": 8000, "thinkingConfig": {"thinkingBudget": 0}}}
            for attempt in range(2):
                try:
                    d = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", body,
                              {"x-goog-api-key": key}, timeout)
                    parts = (d.get("candidates") or [{}])[0].get("content", {}).get("parts") or []
                    txt = "".join(p.get("text", "") for p in parts).strip()
                    _count(spec + ":vision")
                    last_model["ad"] = spec
                    return "" if txt.upper() in {"BOŞ", "BOS"} else txt
                except urllib.error.HTTPError as e:
                    body_txt = e.read()[:400].decode("utf-8", "replace")
                    if e.code == 429:
                        if any(t in body_txt for t in ("per day", "PerDay", "RPD", "daily", "quota")):
                            break                       # bu anahtarın günlük kotası
                        all_daily = False
                        time.sleep(15)
                        continue
                    all_daily = False
                    if e.code in (400, 401, 403, 404):
                        if log:
                            log(f"{spec} görsel: HTTP {e.code}")
                        break
                    time.sleep(3)
                except Exception:  # noqa: BLE001
                    all_daily = False
                    time.sleep(3)
            else:
                all_daily = False
        if all_daily:
            _mark_exhausted(spec)
    return None
