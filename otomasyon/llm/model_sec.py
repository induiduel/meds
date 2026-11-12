"""Ajan model kimliği — tek kaynak (2026-11-13).

`claude -p` artık Claude aboneliğiyle değil **OpenDesign geçidi**yle çalışır: masaüstü/CLI isteği yerel
köprüden (`http://127.0.0.1:8787`) geçide gider ve Anthropic kimlikleri geçit kimliklerine eşlenir
(`claude-opus-5-5` → `deepseek-v4-pro`, `claude-sonnet-5-5` → `deepseek-v4.1-flash`).

Zincirlerdeki (`ders_zinciri`, `son_prova_zinciri`, `hastalik_zinciri`, `checkup_zinciri`, `kamp_zinciri`,
`olasi_soru/gece.sh`, `cizim_uret`, `paralel_arsiv_isci`, `ders_isci`) model kimliği koda gömülmez; buradan gelir.

Sıra: `MEDS_AJAN_MODEL` (+ denetçi için `MEDS_AJAN_MODEL_DENETCI`) > `butce.json` → `claude.model` >
`~/.claude/settings.json` → `env.ANTHROPIC_DEFAULT_OPUS_MODEL` (denetçide SONNET) > `claude-opus-5-5`.
Masaüstü seçicisi değişince ajanlar kendiliğinden aynı adı kullanır; adların köprüde karşılığı vardır
(`scripts/opendesign/rotalar.json`, `--kontrol` ile denetlenir). Geçit kimliği doğrudan da verilebilir
(`MEDS_AJAN_MODEL=deepseek-v4.1-flash`); Claude Code bilinmeyen adı olduğu gibi köprüye geçirir.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]                     # meds/
VARSAYILAN = "claude-opus-5-5"                                 # köprüde deepseek-v4-pro
DENETCI = "claude-sonnet-5-5"                                  # köprüde deepseek-v4.1-flash
HIZLI = "claude-haiku-4-5-20251001"                            # köprüde claude-haiku-5.5


def _butce() -> dict:
    try:
        return (json.loads((MEDS / "otomasyon/llm/butce.json").read_text(encoding="utf-8")) or {}).get("claude", {}) or {}
    except (OSError, json.JSONDecodeError):
        return {}


def _claude_env() -> dict:
    """Masaüstü uygulamasının geçit ayarları (model adları köprüde tanımlı olanlar)."""
    try:
        return (json.loads(Path.home().joinpath(".claude/settings.json").read_text(encoding="utf-8")) or {}).get("env", {}) or {}
    except (OSError, json.JSONDecodeError):
        return {}


def ajan_model(rol: str = "yazar") -> str:
    """Agentik `claude -p --model` kimliği. `rol`: yazar | denetci | hizli."""
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
        # yazar ≠ denetçi (AGENTS kural 14/26): ayrı aile istenmedikçe glm'e düşülür
        return b.get("model_denetci") or env.get("ANTHROPIC_DEFAULT_SONNET_MODEL") or DENETCI
    if rol == "hizli":
        return b.get("model_hizli") or env.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") or HIZLI
    return b.get("model") or env.get("ANTHROPIC_DEFAULT_OPUS_MODEL") or VARSAYILAN


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
