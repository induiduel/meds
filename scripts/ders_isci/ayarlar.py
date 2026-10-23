"""Ders işçisi ortak ayarları. Tümü ortam değişkeniyle ezilebilir (Oracle'da compose, cihazda .env)."""
from __future__ import annotations

import json
import os
import re
import tempfile
import threading
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
# yöneticinin onay ekranından yüklediği öğrenci notu / ses kaydı: site sunucusu yazar (data/ders_isci_ekler/<is_id>/{not,ses}/),
# işçi salt okunur görür (/app/data …) — iki konteynerin ortak yazılabilir klasörü yok (2026-10-24)
EK_DIZIN = Path(os.environ.get("MEDS_ISCI_EK_DIZIN") or APP / "data" / "ders_isci_ekler")
TASLAK = STATE / "taslak"               # her iş: taslak/<is_id>/ (onay bekleyen çıktılar)
GUNLUK = STATE / "gunluk.log"

IZLENEN_KOK = os.environ.get("MEDS_ISCI_KOK", "drive_root")   # yalnız kullanıcının bu yılki klasörü
BU_YIL_BASLANGIC = int(os.environ.get("MEDS_ISCI_YIL", "2026"))  # 2026-27 akademik yılı
GUNLUK_SINIR = int(os.environ.get("MEDS_ISCI_GUNLUK", "4"))      # kullanıcı kararı (2026-10-13): günde en çok 4 ders
DERS_ARASI_SN = int(os.environ.get("MEDS_ISCI_DERS_ARASI", "10800"))  # iki ders başlangıcı arası en az 3 saat
SAATLER = os.environ.get("MEDS_ISCI_SAATLER", "00-24")           # Claude işi yalnız bu saatlerde (TR saati); 00-24 = tüm gün
ARALIK_SN = int(os.environ.get("MEDS_ISCI_ARALIK", "7200"))      # Drive tarama aralığı (2 saat → günde 12 kontrol)
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


# Kuyruk dosyasını okuyup-yazan iş parçacıkları (döngü, işleme, iç API) birbirini ezmesin
KUYRUK_KILIT = threading.RLock()

# ── Çalışma anı ayarları (yönetim paneli → API /ayarlar → STATE/ayar.json) ──
# Ortam değişkenleri yalnız ilk varsayılandır; panelden kaydedilen değer her döngüde okunur (yeniden başlatma gerekmez).
AYAR = STATE / "ayar.json"
AYAR_TANIM: dict[str, tuple] = {  # anahtar → (tür, varsayılan, alt, üst)
    "duraklat": (bool, False, None, None),               # işleme başlama durur (Drive taraması sürer)
    "otomatik_tarama": (bool, True, None, None),         # Drive'ı düzenli tara
    "otomatik_kuyruk": (bool, True, None, None),         # taramada yeni PDF'leri kendiliğinden kuyruğa al
    "onay_iste": (bool, True, None, None),               # kullanıcı kararı (2026-10-24): yeni PDF önce yönetici onayı bekler
                                                          # (telefon bildirimi; not/ses ekleyip ya da yalnız PDF ile başlatır)
    "gunluk_sinir": (int, 8, 0, 48),                     # kullanıcı kararı (2026-10-15): günde en çok 8 ders
    "ders_arasi_dk": (int, 60, 0, 1440),                 # kullanıcı kararı (2026-10-15): saatte en çok 1 ders
    "saat_bas": (int, 0, 0, 23),                         # işleme penceresi başlangıç saati (TR)
    "saat_bit": (int, 24, 1, 24),                        # bitiş saati (24 = gece yarısı); bas>bit gece aşırı pencere
    "tarama_dk": (int, 60, 10, 1440),                    # Drive tarama aralığı
    "model": (str, CLAUDE_MODEL, None, None),
    "effort": (str, CLAUDE_EFFORT, None, None),          # low | medium | high | "" (CLI varsayılanı)
    "sadakat_esigi": (float, 0.80, 0.0, 1.0),            # yayın denetimi: ders notu sadakat alt sınırı
    "canli_ders": (bool, True, None, None),              # taslakta canlı ders konuşma metni de yaz; yayında Emel + EMA sesi
    "otomatik_onay": (bool, True, None, None),           # Kurul 2+: kapılar 0 HATA + yüksek eşleşme → yönetici onayı beklenmez (2026-10-20)
}
MODELLER = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-1", "claude-haiku-4-5-20251001"]
EFORLAR = ["", "low", "medium", "high"]


def ayar() -> dict:
    kayit = oku(AYAR, {}) or {}
    out = {}
    for k, (tur, vars_, alt, ust) in AYAR_TANIM.items():
        v = kayit.get(k, vars_)
        try:
            v = (v if isinstance(v, bool) else str(v).lower() in ("1", "true", "evet")) if tur is bool else tur(v)
        except (TypeError, ValueError):
            v = vars_
        if alt is not None:
            v = min(ust, max(alt, v))
        out[k] = v
    if out["model"] not in MODELLER:
        out["model"] = CLAUDE_MODEL
    if out["effort"] not in EFORLAR:
        out["effort"] = CLAUDE_EFFORT
    return out


def ayar_kaydet(degisen: dict, kim: str = "") -> dict:
    mevcut = ayar()
    yeni = {**mevcut, **{k: v for k, v in (degisen or {}).items() if k in AYAR_TANIM}}
    yaz(AYAR, yeni)
    son = ayar()
    fark = {k: son[k] for k in son if son[k] != mevcut[k]}
    if fark:
        log(f"ayar değişti ({kim or 'panel'}): " + ", ".join(f"{k}={v}" for k, v in fark.items()))
    return son


def saat_uygun() -> bool:
    a_ = ayar()
    a, b = a_["saat_bas"], a_["saat_bit"]
    h = time.localtime().tm_hour
    return a <= h < b if a < b else (h >= a or h < b)
