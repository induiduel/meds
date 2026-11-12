"""OpenDesign geçidi istemcisi (2026-11-13) — Claude/Anthropic aboneliği yerine geçit modelleri.

Geçit Anthropic Messages API'siyle konuşur (`POST /v1/messages`). İki adres:
  * yerel köprü  `http://127.0.0.1:8787`  (masaüstü + terminal `claude` da bunu kullanır)
  * genel geçit  `https://amr-link.open-design.ai`  (köprünün ilettiği asıl adres; Oracle gibi köprüsüz makineler)

Sıra: `MEDS_OPENDESIGN_URL` > köprü çalışıyorsa köprü > genel geçit.
Anahtar: `MEDS_OPENDESIGN_KEY` > `ANTHROPIC_AUTH_TOKEN` > `meds/.env` (`MEDS_OPENDESIGN_KEY` / `OPEN_DESIGN_API_KEY`)
        > `~/.claude/settings.json` → `env.ANTHROPIC_AUTH_TOKEN`.

Bu modül TEK yerdir: `yonlendir.py`, `scripts/agents/cloud_llm.py`, `scripts/v2/core/llm.py` ve doğrulama
betikleri buradan çağırır. LLM kilidi çağıranın sorumluluğundadır (`otomasyon/llm_kilit.py`); bu modül kendi
başına iş başlatmaz, yalnız verilen isteği gönderir.

Model aileleri yazar ≠ denetçi kuralı için: `deepseek-*` yazar, `glm-*`/`gpt-*`/`kimi-*` denetçi.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]          # meds/
KOPRU_URL = "http://127.0.0.1:8787"
GENEL_URL = "https://amr-link.open-design.ai"
VARSAYILAN_MODEL = "deepseek-v4.1-flash"
DENETCI_MODEL = "glm-5.3-flash"
AGIR_MODEL = "deepseek-v4-pro"

# Geçitteki modeller (2026-11-13). `aile` yazar≠denetçi ayrımı, `goruntu` görsel girdi desteği.
MODELLER: dict[str, dict] = {
    "deepseek-v4.1-flash": {"aile": "deepseek", "etiket": "DeepSeek V4.1 Flash", "maliyet": "low", "goruntu": True, "varsayilan": True},
    "deepseek-v4-pro": {"aile": "deepseek", "etiket": "DeepSeek V4 Pro", "maliyet": "high", "goruntu": False},
    "deepseek-v4.1-flash-eco": {"aile": "deepseek", "etiket": "DeepSeek V4.1 Flash Eco", "maliyet": "low", "goruntu": False},
    "deepseek-v4-flash": {"aile": "deepseek", "etiket": "DeepSeek V4 Flash", "maliyet": "medium", "goruntu": False},
    "deepseek-v4-flash-vision-exp": {"aile": "deepseek", "etiket": "DeepSeek V4 Flash Vision (deneysel)", "maliyet": "medium", "goruntu": True},
    "claude-haiku-5.5": {"aile": "anthropic", "etiket": "Claude Haiku 5.5", "maliyet": "low", "goruntu": True},
    "glm-5.3-flash": {"aile": "glm", "etiket": "GLM 5.3 Flash", "maliyet": "low", "goruntu": True},
    "glm-5.3-flashx": {"aile": "glm", "etiket": "GLM 5.3 FlashX", "maliyet": "medium", "goruntu": True},
    "gpt-6-luna": {"aile": "gpt", "etiket": "GPT-6 Luna", "maliyet": "low", "goruntu": True},
    "kimi-k2.7-code": {"aile": "kimi", "etiket": "Kimi K2.7 Code", "maliyet": "medium", "goruntu": True},
    "minimax-m3.1-flash": {"aile": "minimax", "etiket": "MiniMax M3.1 Flash", "maliyet": "low", "goruntu": True},
    "mimo-v2.6-flash": {"aile": "mimo", "etiket": "MiMo 2.6 Flash", "maliyet": "low", "goruntu": True},
    "mimo-v2.6-pro": {"aile": "mimo", "etiket": "MiMo 2.6 Pro", "maliyet": "medium", "goruntu": True},
    "hy4-preview": {"aile": "hy4", "etiket": "HY4 (önizleme)", "maliyet": "medium", "goruntu": False},
}

# Anthropic kimlikleri (depoda `--model claude-opus-5-5` gibi geçen eski çağrılar) → geçit kimliği.
# Köprüsüz makinelerde (Oracle) doğrudan geçide gidildiği için bu tablo köprü haritasıyla aynı olmalı:
# `scripts/opendesign/rotalar.json` ile `kopru.py --doctor` eşleşmeyi denetler.
ESLEME = {
    "claude-opus-5-5": "deepseek-v4-pro",
    "claude-opus-5-1": "deepseek-v4-pro",
    "claude-opus-4-8": "deepseek-v4-pro",
    "claude-opus-4-7": "glm-5.3-flashx",
    "claude-opus-5": "kimi-k2.7-code",
    "claude-sonnet-5-5": "deepseek-v4.1-flash",
    "claude-sonnet-5": "deepseek-v4.1-flash",
    "claude-haiku-5-5": "claude-haiku-5.5",
    "claude-haiku-4-5-20251001": "claude-haiku-5.5",
}

_UA = "MeDSor/OpenDesign-1.0"


class GecitHatasi(Exception):
    """Geçit yanıt vermedi ya da hata döndü. `kod` HTTP kodu (ağ hatasında None)."""

    def __init__(self, mesaj: str, kod: int | None = None):
        super().__init__(mesaj)
        self.kod = kod


# ── ayar ────────────────────────────────────────────────────────────────────────────────────────────────────────
def _dotenv() -> dict:
    out: dict[str, str] = {}
    try:
        for satir in (KOK / ".env").read_text(encoding="utf-8").splitlines():
            satir = satir.strip()
            if "=" in satir and not satir.startswith("#"):
                k, v = satir.split("=", 1)
                out[k.strip()] = v.split(" #")[0].strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def _claude_ayari() -> dict:
    try:
        return (json.loads(Path.home().joinpath(".claude/settings.json").read_text(encoding="utf-8")) or {}).get("env", {}) or {}
    except (OSError, json.JSONDecodeError):
        return {}


def anahtar() -> str:
    """Anahtarı URL denemesi yapmadan çözer (başka istemcilerin anahtar havuzu için)."""
    ortam = os.environ
    env = _dotenv()
    return (ortam.get("MEDS_OPENDESIGN_KEY") or ortam.get("OPEN_DESIGN_API_KEY")
            or ortam.get("ANTHROPIC_AUTH_TOKEN") or env.get("MEDS_OPENDESIGN_KEY")
            or env.get("OPEN_DESIGN_API_KEY") or _claude_ayari().get("ANTHROPIC_AUTH_TOKEN") or "")


def ayar() -> dict:
    """`{"url", "anahtar", "kaynak"}` — hiçbiri yoksa `anahtar` boş döner (çağıran atlar)."""
    ortam = os.environ
    env = _dotenv()
    anahtar_ = anahtar()
    url = (ortam.get("MEDS_OPENDESIGN_URL") or env.get("MEDS_OPENDESIGN_URL") or "").rstrip("/")
    kaynak = "ortam" if (ortam.get("MEDS_OPENDESIGN_KEY") or ortam.get("MEDS_OPENDESIGN_URL")) else "dosya"
    if not url:
        url = KOPRU_URL if kopru_var() else GENEL_URL
        kaynak += ":kopru" if url == KOPRU_URL else ":genel"
    return {"url": url, "anahtar": anahtar_, "kaynak": kaynak}


def kopru_var(zaman_asimi: float = 0.6) -> bool:
    """Yerel köprü ayakta mı (hızlı, isteğe bağlı)."""
    try:
        with urllib.request.urlopen(KOPRU_URL + "/health", timeout=zaman_asimi) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def model_id(ad: str | None) -> str:
    """Anthropic kimliği ya da kısa ad → geçit kimliği. Bilinmeyen ad olduğu gibi kalır."""
    if not ad:
        return VARSAYILAN_MODEL
    ad = ad.strip()
    return ESLEME.get(ad, ad)


def aile(model: str) -> str:
    return (MODELLER.get(model_id(model)) or {}).get("aile") or model_id(model).split("-")[0]


# ── HTTP ───────────────────────────────────────────────────────────────────────────────────────────────────────
def _istek(yol: str, govde: dict | None, zaman_asimi: float, akis: bool = False):
    a = ayar()
    if not a["anahtar"]:
        raise GecitHatasi("OpenDesign anahtarı yok (MEDS_OPENDESIGN_KEY / ANTHROPIC_AUTH_TOKEN)")
    veri = json.dumps(govde, ensure_ascii=False).encode() if govde is not None else None
    r = urllib.request.Request(
        a["url"] + yol, data=veri,
        headers={
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": a["anahtar"],
            "authorization": "Bearer " + a["anahtar"],
            "user-agent": _UA,
            "accept": "text/event-stream" if akis else "application/json",
        },
        method="POST" if veri is not None else "GET",
    )
    return urllib.request.urlopen(r, timeout=zaman_asimi)


def _govde(istem: str, sistem: str | None, model: str, max_tokens: int, sicaklik: float,
           as_json: bool, gorseller: list[str] | None) -> dict:
    icerik: list[dict] = [{"type": "text", "text": istem}]
    for g in gorseller or []:
        icerik.insert(0, {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": g}})
    g = {
        "model": model_id(model),
        "max_tokens": int(max_tokens),
        "temperature": float(sicaklik),
        "messages": [{"role": "user", "content": icerik}],
    }
    if sistem:
        g["system"] = sistem
    if as_json:
        # Geçit Anthropic biçimi konuşur; JSON'u istem sonunda da isteriz (modele göre destek değişir).
        g["system"] = (g.get("system", "") + "\n\nYALNIZ geçerli JSON yaz; açıklama, kod bloğu, önsöz ekleme.").strip()
    return g


def _metin(yanit: dict) -> str:
    parcalar = [b.get("text", "") for b in (yanit.get("content") or []) if b.get("type", "text") == "text"]
    return "".join(parcalar)


def sohbet(istem: str, sistem: str | None = None, model: str = VARSAYILAN_MODEL, as_json: bool = False,
           max_tokens: int = 4096, sicaklik: float = 0.1, zaman_asimi: float = 600, deneme: int = 2,
           gorseller: list[str] | None = None, gunluk=None) -> str | None:
    """Tek atımlık yanıt. Ağ/5xx'te `deneme` kez yineler; 400/401/404'te hemen `GecitHatasi` atar.
    Boş yanıtta None döner (çağıran sıradaki modele geçer)."""
    govde = _govde(istem, sistem, model, max_tokens, sicaklik, as_json, gorseller)
    son: Exception | None = None
    for i in range(max(1, deneme)):
        try:
            with _istek("/v1/messages", govde, zaman_asimi) as r:
                yanit = json.loads(r.read())
            metin = _metin(yanit).strip()
            if not metin:
                if gunluk:
                    gunluk(f"{model_id(model)}: boş yanıt (stop={yanit.get('stop_reason')})")
                return None
            return metin
        except urllib.error.HTTPError as e:
            ayrinti = ""
            try:
                ayrinti = e.read()[:300].decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                pass
            son = GecitHatasi(f"HTTP {e.code}: {ayrinti}", e.code)
            if e.code in (400, 401, 403, 404, 413):
                raise son
            if e.code == 429 and i + 1 < deneme:
                time.sleep(15)
                continue
            time.sleep(2 + i * 2)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            son = GecitHatasi(f"{type(e).__name__}: {str(e)[:200]}")
            time.sleep(2 + i * 2)
    raise son or GecitHatasi("bilinmeyen hata")


_JSON_SARMA = re.compile(r"^```(?:json)?\s*|\s*```$", re.S)
_THINK = re.compile(r"<think>.*?</think>", re.S)


def json_cikar(metin: str):
    """Metinden JSON nesnesi/dizisi çıkarır; bulamazsa None (kod bloğu ve düşünme bloğu hoşgörüsü)."""
    metin = _THINK.sub("", metin or "").strip()
    metin = _JSON_SARMA.sub("", metin).strip()
    try:
        return json.loads(metin)
    except json.JSONDecodeError:
        for kalip in (r"\{.*\}", r"\[.*\]"):
            m = re.search(kalip, metin, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    continue
    return None


def sohbet_json(istem: str, sistem: str | None = None, model: str = VARSAYILAN_MODEL, **kw):
    """JSON isteyip ayrıştırır; ayrıştırılamazsa ham metni `ham` anahtarıyla döndürür."""
    metin = sohbet(istem, sistem=sistem, model=model, as_json=True, **kw)
    if metin is None:
        return None
    veri = json_cikar(metin)
    return veri if veri is not None else {"ham": metin}


# ── sağlık / model listesi ────────────────────────────────────────────────────────────────────────────────────
def saglik(zaman_asimi: float = 3) -> dict:
    a = ayar()
    try:
        with _istek("/health", None, zaman_asimi) as r:
            return {"durum": "ok", "url": a["url"], "kod": r.status, "govde": json.loads(r.read() or b"{}")}
    except Exception as e:  # noqa: BLE001
        return {"durum": "yok", "url": a["url"], "hata": f"{type(e).__name__}: {str(e)[:160]}", "kaynak": a["kaynak"]}


def modeller(zaman_asimi: float = 5) -> list[dict]:
    try:
        with _istek("/v1/models", None, zaman_asimi) as r:
            return json.loads(r.read()).get("data", [])
    except Exception:  # noqa: BLE001
        return []


def anahtar_ozeti() -> str:
    a = ayar()
    k = a["anahtar"]
    return f"{a['url']} · anahtar {'…' + k[-4:] if k else 'YOK'} ({a['kaynak']})"


def _cli(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] in ("--saglik", "saglik"):
        print(json.dumps(saglik(), ensure_ascii=False, indent=1))
        print("ayar:", anahtar_ozeti())
        return 0
    if argv[0] in ("--modeller", "modeller"):
        for m in modeller() or [{"id": k, **v} for k, v in MODELLER.items()]:
            print(f"{m.get('id'):34} {m.get('owned_by', '')}")
        return 0
    if argv[0] in ("--dene", "dene"):
        istem = " ".join(argv[1:]) or "Tek cümleyle kendini tanıt."
        t0 = time.time()
        try:
            print(sohbet(istem))
        except GecitHatasi as e:
            print(f"HATA: {e}", file=sys.stderr)
            return 1
        print(f"({time.time() - t0:.1f} sn)", file=sys.stderr)
        return 0
    print(f"bilinmeyen komut: {argv[0]}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
