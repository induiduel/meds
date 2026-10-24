"""Drive hafif yoklaması (R5 "anında tetik", 2026-10-24).

Drive'a API anahtarı/hizmet hesabı olmadan, herkese açık klasör sayfaları okunarak erişiliyor (pipeline/01-inventory.mjs);
bu yüzden `changes.watch` bildirimi kurulamaz (OAuth/hizmet hesabı + Google Cloud kaydı gerekir). Yerine: `hizli_bakis_dk`'da
bir (varsayılan 5) yalnız kök klasör + aktif ve sonraki kurulun klasörleri ve doğrudan alt klasörleri okunur (birkaç istek);
dosya kimliklerinin özeti değişince tam Drive taraması hemen istenir (tara_iste.json). Yeni PDF ya da yeni açılan
"Kurul N" klasörü böylece ≤5 dk'da görülür (tam tarama 50–60 dk'da bir).
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
import urllib.request

from ayarlar import APP, DOWNLOADS, STATE, log, oku, yaz

KOK_ID = "1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W"     # pipeline/config.mjs drive_root
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36"
DURUM = STATE / "hizli_bakis.json"


def klasor_listesi(klasor_id: str) -> list[tuple[str, str, str]] | None:
    """(id, ad, mime) listesi; okunamazsa None (karşılaştırmaya girmez)."""
    try:
        r = urllib.request.urlopen(urllib.request.Request(f"https://drive.google.com/drive/folders/{klasor_id}",
                                                          headers={"User-Agent": UA, "Accept-Language": "tr-TR,tr;q=0.9"}), timeout=30)
        html = r.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return None
    m = re.search(r"window\['_DRIVE_ivd'\]\s*=\s*'([^']+)'", html)
    if not m:
        return []
    ham = re.sub(r"\\\\x([0-9a-fA-F]{2})", lambda x: chr(int(x.group(1), 16)), m.group(1))
    ham = re.sub(r"\\x([0-9a-fA-F]{2})", lambda x: chr(int(x.group(1), 16)), ham)
    try:
        veri = json.loads(ham)
    except Exception:  # noqa: BLE001
        return None
    out, gor = [], set()

    def gez(v):
        if not isinstance(v, list):
            return
        if len(v) > 3 and isinstance(v[0], str) and len(v[0]) >= 25 and isinstance(v[2], str) and isinstance(v[3], str) \
                and v[0] not in gor:
            gor.add(v[0]); out.append((v[0], v[2], v[3]))
        for x in v:
            gez(x)
    gez(veri)
    return [o for o in out if o[0] != klasor_id]


def _aktif_kurul() -> int:
    try:
        r = subprocess.run(["python3", str(APP / "scripts" / "takvim" / "aktif_kurul.py")], capture_output=True, text=True, timeout=30)
        return int((r.stdout or "").strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return 0


def bak() -> bool:
    """Bir yoklama. → True: değişiklik bulundu, tam tarama istendi."""
    kok = klasor_listesi(KOK_ID)
    if kok is None:
        return False
    k = _aktif_kurul()
    hedef = {"kok": KOK_ID}
    for fid, ad, mime in kok:
        n = re.match(r"^\s*Kurul\s*(\d+)", ad, re.I)
        if mime.endswith("folder") and n and int(n.group(1)) in (k, k + 1):
            hedef[ad] = fid
    imza, sayi = {}, 0
    for ad, fid in hedef.items():
        L = kok if fid == KOK_ID else klasor_listesi(fid)
        if L is None:
            return False                      # yarım okuma: karşılaştırma yok
        alt = [x for x in L if x[2].endswith("folder")] if fid != KOK_ID else []
        kim = sorted(x[0] for x in L)
        for aid, aad, _ in alt[:15]:
            A = klasor_listesi(aid)
            if A is None:
                return False
            kim += sorted(x[0] for x in A)
        imza[ad] = hashlib.sha1(",".join(kim).encode()).hexdigest()[:16]
        sayi += len(kim)
    once = oku(DURUM, {}) or {}
    yaz(DURUM, {"zaman": time.time(), "imza": imza, "oge": sayi, "kurul": k})
    if once.get("imza") and once["imza"] != imza:
        degisen = sorted(set(imza) ^ set(once["imza"]) | {a for a in imza if once["imza"].get(a) != imza[a]})
        log(f"Drive hızlı bakış: değişiklik ({', '.join(degisen)}) → tam tarama istendi")
        if not (STATE / "tara_iste.json").exists():
            yaz(STATE / "tara_iste.json", {"zaman": time.time(), "yollar": [], "neden": "hızlı bakış"})
        return True
    return False


if __name__ == "__main__":
    t = time.time()
    print("değişiklik:", bak(), "·", round(time.time() - t, 1), "sn ·", json.dumps(oku(DURUM, {}), ensure_ascii=False)[:300])
