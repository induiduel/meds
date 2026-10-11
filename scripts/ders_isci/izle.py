#!/usr/bin/env python3
"""Ders işçisi — Drive izleme + kuyruk + işleme döngüsü (Oracle'da 7/24, konteyner: meds-ders-isci).

Her ARALIK_SN'de:
  1. Drive envanteri + artımlı indirme (yapay zekâsız, ücretsiz): scripts/pipeline/01-inventory.mjs + 02-download.mjs,
     yalnız izlenen kök (MEDS_DRIVE_ROOTS=drive_root).
  2. _downloads.json'daki her PDF'in sha256'sı kayıtla karşılaştırılır; yeni/değişen dosya kuyruğa girer.
     İLK çalıştırmada mevcut dosyaların hepsi "mevcut" olarak kaydedilir (yeniden işlenmez).
  3. Saat penceresi (MEDS_ISCI_SAATLER) ve günlük sınır (MEDS_ISCI_GUNLUK) uygunsa kuyruğun başındaki iş isle.py ile
     işlenir; çıktılar yalnız taslak/<is_id>/ altına yazılır (canlıya hiçbir şey yazılmaz; yayın yönetim onayıyla).

  izle.py              sürekli döngü
  izle.py --bir-kez    tek tur (test/cron)
  izle.py --durum      kuyruk ve son işlerin özeti
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ayarlar import (APP, ARALIK_SN, DOWNLOADS, GUNLUK_SINIR, IZLENEN_KOK, KAYIT, KUYRUK, oku, log,  # noqa: E402
                     saat_uygun, yaz, yil_sinifi)


def drive_tara() -> bool:
    env = {**os.environ, "MEDS_DRIVE_ROOTS": IZLENEN_KOK, "MEDS_DOWNLOADS_DIR": str(DOWNLOADS)}
    for betik in ("01-inventory.mjs", "02-download.mjs"):
        r = subprocess.run(["node", str(APP / "scripts" / "pipeline" / betik)], cwd=APP, env=env,
                           capture_output=True, text=True, timeout=1800)
        if r.returncode != 0:
            log(f"Drive taraması hatası ({betik}): {(r.stderr or r.stdout)[-400:]}")
            return False
    return True


def pdfler() -> list[dict]:
    """İzlenen kökteki indirilmiş PDF'ler: {yol (yerel, köke göre), tam, sha256}."""
    d = oku(DOWNLOADS / "_downloads.json", {})
    out = []
    for v in (d.values() if isinstance(d, dict) else d):
        yol = str(v.get("path") or "")
        if v.get("status") != "done" or not yol.lower().endswith(".pdf") or not yol.startswith(IZLENEN_KOK + "/"):
            continue
        tam = DOWNLOADS / yol
        if not tam.exists():
            continue
        sha = v.get("sha256") or hashlib.sha256(tam.read_bytes()).hexdigest()
        out.append({"yol": yol[len(IZLENEN_KOK) + 1:], "tam": str(tam), "sha256": sha})
    return out


def is_id(yol: str, sha: str) -> str:
    return time.strftime("%Y%m%d") + "-" + sha[:10]


def kuyruga_al(ilk_kurulum: bool) -> int:
    kayit = oku(KAYIT, {})
    kuyruk = oku(KUYRUK, [])
    bekleyen = {j["sha256"] for j in kuyruk}
    yeni = 0
    for p in pdfler():
        if p["sha256"] in kayit or p["sha256"] in bekleyen:
            continue
        if "Ders Programı" in p["yol"] or "ders programı" in p["yol"].lower():
            kayit[p["sha256"]] = {"durum": "program", "yol": p["yol"], "zaman": time.time()}
            continue
        if ilk_kurulum:
            kayit[p["sha256"]] = {"durum": "mevcut", "yol": p["yol"], "yil": yil_sinifi(p["yol"], IZLENEN_KOK), "zaman": time.time()}
            continue
        # Kullanıcı kararı: izlenen klasöre YENİ eklenen her dosya bu yılındır; addaki eski yıl işareti yalnız uyarıdır.
        uyari = "dosya adında eski yıl işareti var" if yil_sinifi(p["yol"], IZLENEN_KOK) == "gecmis" else ""
        kuyruk.append({"is_id": is_id(p["yol"], p["sha256"]), "yol": p["yol"], "tam": p["tam"], "sha256": p["sha256"],
                       "yil": "bu_yil", "uyari": uyari, "durum": "bekliyor", "eklendi": time.time(), "deneme": 0})
        yeni += 1
        log(f"kuyruğa alındı: {p['yol']}")
    yaz(KAYIT, kayit)
    yaz(KUYRUK, kuyruk)
    return yeni


def bugun_islenen() -> int:
    bas = time.mktime(time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d"))
    return sum(1 for v in oku(KAYIT, {}).values() if v.get("durum") == "taslak" and v.get("zaman", 0) >= bas)


def sira_isle():
    kuyruk = oku(KUYRUK, [])
    simdi = time.time()
    hazir = [j for j in kuyruk if j["durum"] == "bekliyor" and j.get("sonra", 0) <= simdi]
    if not hazir:
        return
    if not saat_uygun():
        return
    if bugun_islenen() >= GUNLUK_SINIR:
        return
    j = hazir[0]
    log(f"işleniyor: {j['is_id']} {j['yol']}")
    from isle import isle  # noqa: E402  (ağır bağımlılıklar yalnız iş varken yüklensin)
    sonuc = isle(j)
    kuyruk = oku(KUYRUK, [])
    for k in kuyruk:
        if k["is_id"] != j["is_id"]:
            continue
        k["deneme"] = k.get("deneme", 0) + 1
        if sonuc["durum"] == "taslak":
            k["durum"] = "taslak"
        elif sonuc["durum"] == "kota":
            k["sonra"] = time.time() + 3600          # abonelik kotası: 1 saat sonra yeniden
            k["deneme"] -= 1
        elif k["deneme"] >= 3:
            k["durum"] = "hata"
        else:
            k["sonra"] = time.time() + 1800
        k["son_mesaj"] = sonuc.get("mesaj", "")[:500]
    yaz(KUYRUK, kuyruk)
    if sonuc["durum"] in ("taslak", "hata") or any(k["is_id"] == j["is_id"] and k["durum"] == "hata" for k in kuyruk):
        kayit = oku(KAYIT, {})
        kayit[j["sha256"]] = {"durum": sonuc["durum"], "yol": j["yol"], "is_id": j["is_id"], "zaman": time.time()}
        yaz(KAYIT, kayit)


def durum():
    kuyruk = oku(KUYRUK, [])
    kayit = oku(KAYIT, {})
    from collections import Counter
    print("kayıt:", dict(Counter(v.get("durum") for v in kayit.values())))
    print("kuyruk:", dict(Counter(j["durum"] for j in kuyruk)))
    for j in kuyruk[-10:]:
        print(f"  {j['is_id']} {j['durum']:<9} {j['yol']}  {j.get('son_mesaj', '')[:80]}")


def tur(tara: bool = True):
    ilk = not KAYIT.exists()
    if tara and not drive_tara():
        return
    n = kuyruga_al(ilk)
    if ilk:
        log(f"ilk kurulum: mevcut {len(oku(KAYIT, {}))} dosya 'mevcut' olarak kaydedildi (yeniden işlenmez)")
    elif n:
        log(f"{n} yeni ders PDF'i kuyrukta")
    sira_isle()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bir-kez", action="store_true")
    ap.add_argument("--taramasiz", action="store_true", help="Drive taramadan yalnız kuyruk/işleme")
    ap.add_argument("--durum", action="store_true")
    a = ap.parse_args()
    if a.durum:
        return durum()
    if a.bir_kez:
        return tur(not a.taramasiz)
    log(f"ders işçisi başladı: kök={IZLENEN_KOK} aralık={ARALIK_SN}s günlük={GUNLUK_SINIR}")
    while True:
        try:
            tur()
        except Exception as e:  # noqa: BLE001
            log(f"tur hatası: {e!r}")
        time.sleep(ARALIK_SN)


if __name__ == "__main__":
    main()
