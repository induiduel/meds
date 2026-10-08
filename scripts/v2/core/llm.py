"""LLM katmanı — GPU YOK. Yalnızca ücretsiz bulut sağlayıcıları.

Yerel Ollama/GPU modelleri (gemma3, qwen3, bge-m3, qwen3-vl) KULLANILMAZ. Model zinciri yalnızca
ücretsiz anahtarlarla çalışır; faturalı anahtar `MEDS_FREE_ONLY=1` iken asla denenmez.

Zincir: groq:gpt-oss-120b → groq:qwen3.8-27b → zen:muse-spark-free → gemini:flash-latest → gemini:3.5-flash
Kota: 429 "günlük" yanıtı veren model o gün atlanır (CORE_DIR/_state/llm_usage.json, süreçler arası).
Hata: CORE_DIR/_state/llm_errors.jsonl içine yazılır. Hiçbir model yanıt vermezse None döner.
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.error
import urllib.request
from typing import Any, Callable

from .. import config
from . import store

UA = "MedSoruCoreV2/1.0"
DEFAULT_CHAIN = [
    "groq:openai/gpt-oss-120b",
    "groq:qwen/qwen3.8-27b",
    "gemini:gemini-flash-latest",
    "gemini:gemini-3.5-flash",
]
ZEN_FREE = "zen:muse-spark-1.3-contributor-free"
VISION_CHAIN = ["gemini:gemini-3.5-flash", "gemini:gemini-flash-latest"]
# Structured-outputs (response_format=json_object) desteklemeyen modeller:
# HTTP 400 veriyor; bu modellerde JSON ham metin olarak alınır, parse_json() ayrıştırır.
NO_STRUCTURED_OUTPUT = {
    "inclusionai/ling-3.1-flash:free",
    "inclusionai/ling-3.0-flash-sante:free",
    "poolside/laguna-s-2.1-free",
}

_skip_session: set[str] = set()
last_model: dict = {"ad": None}


def keys() -> dict[str, list[str]]:
    """Ortamdan ücretsiz anahtar havuzları (config .env'yi zaten yüklemiş olmalı)."""
    env = os.environ
    gemini = [env["GEMINI_API_KEY"]] if env.get("GEMINI_API_KEY") else []
    free = sorted((n for n in env if n.startswith("GEMINI_FREE_KEY_") and n[16:].isdigit()),
                  key=lambda n: int(n[16:]))
    gemini += [env[n] for n in free if env.get(n)]
    return {
        "groq": [k for k in (env.get("GROQ_API_KEY"), env.get("GROQ_API_KEY_2")) if k],
        "gemini": list(dict.fromkeys(gemini)),
        "zen": [env["OPENCODE_API_KEY"]] if env.get("OPENCODE_API_KEY") else [],
        "openrouter": [k for k in (env.get("MUSE_SPARK_API_KEY"), env.get("OPENROUTER_API_KEY")) if k],
        "cmd": [env["CMD_API_KEY"]] if env.get("CMD_API_KEY") else [],
        "cmdmsg": [env["CMD_API_KEY"]] if env.get("CMD_API_KEY") else [],
    }


def chain() -> list[str]:
    env = os.environ
    base = [m.strip() for m in (env.get("MEDS_CLOUD_CHAIN") or "").split(",") if m.strip()] or DEFAULT_CHAIN
    extra = [m.strip() for m in (env.get("MEDS_CLOUD_EXTRA_MODELS") or "").split(",") if m.strip()]
    if keys()["zen"] and ZEN_FREE not in base and ZEN_FREE not in extra:
        i = next((j for j, m in enumerate(base) if m.startswith("gemini:")), len(base))
        base = base[:i] + [ZEN_FREE] + base[i:]
    # Command Code Provider — birincil (chat/completions) ve ikincil (messages/Anthropic).
    cmd_models = [m.strip() for m in (env.get("MEDS_CMD_MODELS") or "deepseek/deepseek-v4.1-flash"
                  ).split(",") if m.strip()]
    msg_models = [m.strip() for m in (env.get("MEDS_CMD_MSG_MODELS") or "claude-sonnet-5-5"
                  ).split(",") if m.strip()]
    cmd_chain = [f"cmd:{m}" for m in cmd_models] if keys().get("cmd") else []
    msg_chain = [f"cmdmsg:{m}" for m in msg_models] if keys().get("cmdmsg") else []
    if env.get("MEDS_CMD_ONLY"):
        # Yalnızca belirtilen modeller; yedek bulut kullanılmaz.
        # API yanıt verirse bu modellerle çalış, vermeyse çağlayan dursun/bilsin.
        return cmd_chain
    return cmd_chain + msg_chain + base + extra


# ---- günlük kota durumu (süreçler arası) ----------------------------------------------------

def _state_path():
    return config.STATE_DIR / "llm_usage.json"


def _load_usage() -> dict:
    data = store.read_json(_state_path(), {}) or {}
    if data.get("gun") != time.strftime("%Y-%m-%d"):
        return {"gun": time.strftime("%Y-%m-%d"), "kota_dolu": [], "sayac": {}}
    return data


def _save_usage(state: dict) -> None:
    try:
        store.atomic_write_json(_state_path(), state)
    except OSError:
        pass


def _mark_exhausted(model: str) -> None:
    state = _load_usage()
    if model not in state["kota_dolu"]:
        state["kota_dolu"].append(model)
    _save_usage(state)


def _count(model: str) -> None:
    state = _load_usage()
    state["sayac"][model] = state["sayac"].get(model, 0) + 1
    _save_usage(state)


def _log_error(record: dict) -> None:
    try:
        config.ensure_core_dirs()
        store.append_jsonl(config.STATE_DIR / "llm_errors.jsonl", {**record, "zaman": store.now_iso()})
    except OSError:
        pass


# ---- sağlayıcı çağrıları --------------------------------------------------------------------

def _post(url: str, body: dict, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA, **headers},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _openai_style(base: str, key: str, model: str, system: str | None, prompt: str,
                  as_json: bool, max_tokens: int, temperature: float, timeout: int) -> str:
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    body: dict[str, Any] = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if as_json and model not in NO_STRUCTURED_OUTPUT:
        body["response_format"] = {"type": "json_object"}
    data = _post(f"{base}/chat/completions", body, {"Authorization": f"Bearer {key}"}, timeout)
    return data["choices"][0]["message"].get("content") or ""


def _gemini(key: str, model: str, system: str | None, prompt: str, as_json: bool,
            max_tokens: int, temperature: float, timeout: int) -> str:
    body: dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    if as_json:
        body["generationConfig"]["responseMimeType"] = "application/json"
    data = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                 body, {"x-goog-api-key": key}, timeout)
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _anthropic(base: str, key: str, model: str, system: str | None, prompt: str, as_json: bool,
               max_tokens: int, temperature: float, timeout: int) -> str:
    body: dict[str, Any] = {"model": model, "max_tokens": max_tokens,
                            "messages": [{"role": "user", "content": prompt}]}
    if system:
        body["system"] = system
    req = urllib.request.Request(
        f"{base}/messages", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA,
                 "Authorization": f"Bearer {key}", "anthropic-version": "2023-06-01"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    parts = data.get("content") or []
    return "".join(p.get("text", "") for p in parts if isinstance(p, dict))


def _call(spec: str, key: str, system, prompt, as_json, max_tokens, temperature, timeout) -> str:
    provider, model = spec.split(":", 1)
    if provider == "groq":
        return _openai_style("https://api.groq.com/openai/v1", key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if provider == "gemini":
        return _gemini(key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if provider == "zen":
        return _openai_style("https://opencode.ai/zen/v1", key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if provider == "openrouter":
        base = (os.environ.get("MUSE_SPARK_BASE_URL") or "https://openrouter.ai/api/v1").rstrip("/")
        return _openai_style(base, key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if provider == "cmd":
        base = (os.environ.get("CMD_API_BASE_URL") or "https://api.commandcode.ai/provider/v1").rstrip("/")
        return _openai_style(base, key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    if provider == "cmdmsg":
        base = (os.environ.get("CMD_API_BASE_URL") or "https://api.commandcode.ai/provider/v1").rstrip("/")
        return _anthropic(base, key, model, system, prompt, as_json, max_tokens, temperature, timeout)
    raise ValueError(f"bilinmeyen sağlayıcı: {provider}")


def strip_think(raw: str) -> str:
    return re.sub(r"<think>.*?</think>", "", raw or "", flags=re.S).strip()


def parse_json(raw: str) -> Any:
    """Modelin JSON yanıtını (kod bloğu/düşünce gürültüsü olabilir) ayrıştırır; başarısızsa None."""
    raw = strip_think(raw)
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


def chat(prompt: str, system: str | None = None, *, as_json: bool = False, max_tokens: int = 2048,
         temperature: float = 0.1, timeout: int = 90, models: list[str] | None = None,
         log: Callable[[str], None] | None = None) -> Any:
    """Zincirdeki ilk çalışan ücretsiz modelden yanıt. `as_json=True` ise dict, aksi halde str.
    Hiçbir model yanıt vermezse None (çağıran 'atla, sonra dene' uygular; boş sonuç yazılmaz)."""
    pool = keys()
    exhausted = set(_load_usage()["kota_dolu"])
    for spec in models or chain():
        if spec in exhausted or spec in _skip_session:
            continue
        provider = spec.split(":", 1)[0]
        provider_keys = pool.get(provider) or []
        if not provider_keys:
            _skip_session.add(spec)
            _log_error({"model": spec, "durum": "anahtar-yok"})
            continue
        for key in provider_keys:
            daily_done = False
            for _attempt in range(2):
                try:
                    raw = _call(spec, key, system, prompt, as_json, max_tokens, temperature, timeout)
                except urllib.error.HTTPError as e:
                    body = e.read()[:400].decode("utf-8", "replace")
                    _log_error({"model": spec, "durum": f"HTTP {e.code}", "govde": body})
                    if e.code == 429:
                        if any(t in body for t in ("per day", "TPD", "RPD", "PerDay", "daily", "quota")):
                            daily_done = True
                            break
                        time.sleep(15)
                        continue
                    if e.code in (400, 401, 403, 404):
                        if log:
                            log(f"{spec}: HTTP {e.code} — bu süreçte atlanıyor")
                        _skip_session.add(spec)
                        daily_done = True
                        break
                    time.sleep(5)
                    continue
                except Exception as e:  # noqa: BLE001
                    _log_error({"model": spec, "durum": "istisna", "mesaj": str(e)[:200]})
                    time.sleep(3)
                    continue
                out = parse_json(raw) if as_json else strip_think(raw)
                if out:
                    last_model["ad"] = spec
                    _count(spec)
                    return out
                break
            if spec in _skip_session:
                break
            if not daily_done:
                break
        else:
            if log:
                log(f"{spec}: günlük kota doldu, bugün atlanacak")
            _mark_exhausted(spec)
    return None


def chat_json(prompt: str, system: str | None = None, **kwargs) -> Any:
    return chat(prompt, system, as_json=True, **kwargs)


# ---- görsel OCR (ücretsiz Gemini vision; GPU yok) -------------------------------------------

VISION_PROMPT = (
    "Bu görüntü bir tıp fakültesi ders slaytı, ders notu ya da sınav sayfasıdır. İçindeki metni BİREBİR yaz. "
    "Sayfa çok sütunluysa önce sol sütunu baştan sona, sonra sağ sütunu yaz. Başlıkları, madde işaretlerini, "
    "soru numaralarını ve şıkları ayrı satırlarda koru. Tablo varsa Markdown tablosu olarak ver. "
    "Türkçe karakterleri ve Latince tıbbi terimleri olduğu gibi koru. Okuyamadığın yere [okunamadı] yaz; "
    "tahmin etme, ekleme yapma, imla düzeltme yapma, açıklama yazma. Okunabilir metin yoksa yalnızca BOŞ yaz."
)


def vision_ocr(png_bytes: bytes, prompt: str = VISION_PROMPT, timeout: int = 120,
               log: Callable[[str], None] | None = None) -> str | None:
    """Görüntüdeki metni ücretsiz Gemini ile çıkarır (web OCR/GPU vision yerine).
    Yanıt yoksa None döner (çağıran CPU Tesseract'a düşer)."""
    pool = keys()
    exhausted = set(_load_usage()["kota_dolu"])
    data = base64.b64encode(png_bytes).decode()
    for spec in VISION_CHAIN:
        if spec in exhausted or spec in _skip_session:
            continue
        model = spec.split(":", 1)[1]
        for key in pool.get("gemini") or []:
            body = {
                "contents": [{"parts": [
                    {"inline_data": {"mime_type": "image/png", "data": data}},
                    {"text": prompt},
                ]}],
                "generationConfig": {"temperature": 0, "maxOutputTokens": 8000,
                                     "thinkingConfig": {"thinkingBudget": 0}},
            }
            for _attempt in range(2):
                try:
                    resp = _post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                        body, {"x-goog-api-key": key}, timeout)
                    parts = (resp.get("candidates") or [{}])[0].get("content", {}).get("parts") or []
                    text = "".join(p.get("text", "") for p in parts).strip()
                    _count(spec + ":vision")
                    last_model["ad"] = spec
                    return "" if text.upper() in {"BOŞ", "BOS"} else text
                except urllib.error.HTTPError as e:
                    _log_error({"model": spec + ":vision", "durum": f"HTTP {e.code}"})
                    break
                except Exception as e:  # noqa: BLE001
                    _log_error({"model": spec + ":vision", "durum": "istisna", "mesaj": str(e)[:200]})
                    time.sleep(3)
    return None
