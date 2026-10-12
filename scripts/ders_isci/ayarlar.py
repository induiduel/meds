"""Ders işçisi ortak ayarları. Tümü ortam değişkeniyle ezilebilir (Oracle'da compose, cihazda .env)."""
from __future__ import annotations

import json
import os
import re
import tempfile
import time
from pathlib import Path

APP = Path(os.environ.get("MEDS_APP_DIR") or Path(__file__).resolve().parents[2])          # meds/
ROOT = APP.parent                                                                          # medsor/
DOWNLOADS = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or ROOT / "meds_downloads")
DATABASE = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT / "meds_database")
# Durum: senkronlanan klasörlerin DIŞINDA (cihaz↔Oracle rsync'i ezmesin)
STATE = Path(os.environ.get("MEDS_ISCI_DIR") or ROOT / "ders_isci")
KAYIT = STATE / "islenen.json"          # sha256 → {durum, yol, is_id, zaman}
KUYRUK = STATE / "kuyruk.json"          # bekleyen işler
TASLAK = STATE / "taslak"               # her iş: taslak/<is_id>/ (onay bekleyen çıktılar)
GUNLUK = STATE / "gunluk.log"

IZLENEN_KOK = os.environ.get("MEDS_ISCI_KOK", "drive_root")   # yalnız kullanıcının bu yılki klasörü
BU_YIL_BASLANGIC = int(os.environ.get("MEDS_ISCI_YIL", "2026"))  # 2026-27 akademik yılı
GUNLUK_SINIR = int(os.environ.get("MEDS_ISCI_GUNLUK", "2"))      # Max 5x: günde en çok 2 ders
SAATLER = os.environ.get("MEDS_ISCI_SAATLER", "01-08")           # Claude işi yalnız bu saatlerde (TR saati)
ARALIK_SN = int(os.environ.get("MEDS_ISCI_ARALIK", "1800"))      # Drive tarama aralığı (30 dk)
CLAUDE_BIN = os.environ.get("MEDS_ISCI_CLAUDE", "claude")
CLAUDE_MODEL = os.environ.get("MEDS_ISCI_MODEL", "claude-opus-5-5")  # kullanıcı kararı (2026-10-12): Opus 5.5
CLAUDE_EFFORT = os.environ.get("MEDS_ISCI_EFFORT", "low")            # düşük efor; boş: CLI varsayılanı
API = os.environ.get("MEDS_ISCI_API", "http://meds-server:3000")  # bildirim + benzer soru için site API'si
EMBED = os.environ.get("MEDS_EMBED_URL", "http://meds-embed:8094/embed")


def log(msg: str):
    STATE.mkdir(parents=True, exist_ok=True)
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(GUNLUK, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def oku(p: Path, varsayilan):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return varsayilan


def yaz(p: Path, veri):
    """Atomik yazım: yarım dosya kalmaz."""
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=".tmp_")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


_YIL = re.compile(r"(?<!\d)(20\d\d|\d\d)\s*[-_/ ]\s*(20\d\d|\d\d)(?!\d)|(?<!\d)(20\d\d)(?!\d)")


def yil_sinifi(yol: str, kok: str) -> str:
    """'bu_yil' | 'gecmis'. Kullanıcı kararı: izlenen klasöre eklenen = bu yıl; ancak yolunda daha eski bir yıl
    işareti (ör. '2024', '24-25', '2025-2026') olan dosya geçmiş yıldır. Diğer kökler (çıkmış/eski notlar) geçmiştir."""
    if kok != IZLENEN_KOK:
        return "gecmis"
    for m in _YIL.finditer(yol):
        if m.group(3):
            y = int(m.group(3))
        else:
            a = m.group(1)
            y = int(a) if len(a) == 4 else 2000 + int(a)
        if 2000 <= y < BU_YIL_BASLANGIC:
            return "gecmis"
    return "bu_yil"


def saat_uygun() -> bool:
    a, b = (int(x) for x in SAATLER.split("-"))
    h = time.localtime().tm_hour
    return a <= h < b if a < b else (h >= a or h < b)
