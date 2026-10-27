"""LLM kilidi (kullanıcı kararı 2026-10-27): LLM/API kullanan hiçbir iş kendiliğinden başlamaz.

Gece 26.10'da otomatik hat kullanıcının Claude limitini tüketti. Artık `claude -p` / ajan CLI çağıran her betik
yalnız elle verilen komutla çalışır: bu bilgisayarda `MEDS_LLM_ELLE=1 python3 …` ya da yönetim panelinin komutu
(panel ortam değişkenini koyar). systemd zamanlayıcısından gelen çağrı (INVOCATION_ID) bayrak olsa da reddedilir.
"""
import os
import sys


def serbest() -> bool:
    if os.environ.get("MEDS_LLM_ELLE") != "1":
        return False
    if os.environ.get("INVOCATION_ID") and os.environ.get("MEDS_LLM_PANEL") != "1":
        return False  # zamanlayıcı/servis
    return True


def kilit(ad: str) -> None:
    if not serbest():
        sys.stderr.write(f"[llm_kilit] {ad}: LLM işi elle komut olmadan çalışmaz (MEDS_LLM_ELLE=1 gerekir). Çıkış 75.\n")
        raise SystemExit(75)
