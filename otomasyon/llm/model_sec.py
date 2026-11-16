"""Ajan model kimliği — tek kaynak (2026-11-13).

`claude -p` artık Claude aboneliğiyle değil **OpenDesign geçidi**yle çalışır: masaüstü/CLI isteği yerel
köprüden (`http://127.0.0.1:8787`) geçide gider ve Anthropic kimlikleri geçit kimliklerine eşlenir
(`claude-opus-5-5` → `deepseek-v4-pro`, `claude-sonnet-5-5` → `deepseek-v4.1-flash`).

Zincirlerdeki (`ders_zinciri`, `son_prova_zinciri`, `hastalik_zinciri`, `checkup_zinciri`, `kamp_zinciri`,
`olasi_soru/gece.sh`, `cizim_uret`, `paralel_arsiv_isci`, `ders_isci`) model kimliği koda gömülmez; buradan gelir.

Sıra: `MEDS_AJAN_MODEL` (+ denetçi için `MEDS_AJAN_MODEL_DENETCI`) > `butce.json` → `claude.model` >
`~/.claude/settings.json` → `env.ANTHROPIC_DEFAULT_OPUS_MODEL` (denetçide SONNET) > `claude-opus-5-5`.
Masaüstü seçicisi değişince ajanlar kendiliğinden aynı adı kullanır; adların köprüde karşılığı vardır
(`scripts/altyapi/opendesign/rotalar.json`, `--kontrol` ile denetlenir). Geçit kimliği doğrudan da verilebilir
(`MEDS_AJAN_MODEL=deepseek-v4.1-flash`); Claude Code bilinmeyen adı olduğu gibi köprüye geçirir.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]                     # meds/
VARSAYILAN = "claude-opus-5-5"                                 # köprüde deepseek-v4-pro
DENETCI = "claude-opus-4-7"                                    # köprüde glm-5.3-flashx (yazardan AYRI aile, kural 31)
# denetçi yazarla aynı aileye çözülürse sırayla denenen takma adlar (rotalar.json'da tanımlı; glm → gpt → kimi)
DENETCI_YEDEK = ("claude-opus-4-7", "claude-fable-6", "claude-opus-5")
HIZLI = "claude-haiku-4-5-20251001"                            # köprüde claude-haiku-5.5


def _butce() -> dict:
    try:
        return (json.loads((MEDS / "otomasyon/llm/butce.json").read_text(encoding="utf-8")) or {}).get("claude", {}) or {}
    except (OSError, json.JSONDecodeError):
        return {}


def _claude_env() -> dict:
    """Masaüstü uygulamasının geçit ayarları (model adları köprüde tanımlı olanlar)."""
    try:
        for ad in (".claude/gecit.json", ".claude/settings.json"):  # 2026-11-16: geçit ayrı dosyada (etkileşimli claude geçitsiz)
            p = Path.home().joinpath(ad)
            if p.exists():
                env = (json.loads(p.read_text(encoding="utf-8")) or {}).get("env", {}) or {}
                if env.get("ANTHROPIC_AUTH_TOKEN") or env.get("ANTHROPIC_DEFAULT_OPUS_MODEL"):
                    return env
        return {}
    except (OSError, json.JSONDecodeError):
        return {}


def aile(ad: str) -> str:
    """Model adının (Anthropic takma adı ya da geçit kimliği) geçitteki ailesi: deepseek, glm, gpt, kimi …"""
    try:
        import sys
        sys.path.insert(0, str(MEDS / "otomasyon"))
        from llm.opendesign import aile as _aile  # noqa: PLC0415
        return _aile(ad)
    except Exception:  # noqa: BLE001
        return (ad or "").split("-")[0]


def _ham(rol: str) -> str:
    if rol == "denetci":
        ozel = os.environ.get("MEDS_AJAN_MODEL_DENETCI")
        if ozel:
            return ozel
    elif rol == "hizli":
        ozel = os.environ.get("MEDS_AJAN_MODEL_HIZLI")
        if ozel:
            return ozel
    ortam = os.environ.get("MEDS_AJAN_MODEL")
    if ortam:
        return ortam
    b = _butce()
    env = _claude_env()
    if rol == "denetci":
        return b.get("model_denetci") or env.get("ANTHROPIC_DEFAULT_SONNET_MODEL") or DENETCI
    if rol == "hizli":
        return b.get("model_hizli") or env.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") or HIZLI
    return b.get("model") or env.get("ANTHROPIC_DEFAULT_OPUS_MODEL") or VARSAYILAN


def ajan_model(rol: str = "yazar") -> str:
    """Agentik `claude -p --model` kimliği. `rol`: yazar | denetci | hizli.
    Denetçi yazarla AYNI aileye çözülürse (ör. MEDS_AJAN_MODEL hepsini deepseek'e çekti) DENETCI_YEDEK'ten ilk farklı aile
    seçilir (yazar ≠ denetçi, AGENTS kural 14/26/31). Yalnız açık `MEDS_AJAN_MODEL_DENETCI` olduğu gibi kalır."""
    ad = _ham(rol)
    if rol == "denetci" and not os.environ.get("MEDS_AJAN_MODEL_DENETCI"):
        yazar_aile = aile(_ham("yazar"))
        if aile(ad) == yazar_aile:
            ad = next((x for x in DENETCI_YEDEK if aile(x) != yazar_aile), ad)
    return ad


def gecit_model(rol: str = "yazar") -> str:
    """Aynı kimliğin geçitteki karşılığı (günlük/rapora yazmak için)."""
    try:
        import sys
        sys.path.insert(0, str(MEDS / "otomasyon"))
        from llm.opendesign import model_id  # noqa: PLC0415
        return model_id(ajan_model(rol))
    except Exception:  # noqa: BLE001
        return ajan_model(rol)


if __name__ == "__main__":
    import sys
    print(gecit_model(sys.argv[1] if len(sys.argv) > 1 else "yazar"))
