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


KAPSAM_SURUM = ":v3"   # kapsam/eşleşme mantığı değişince artır → tüm PDF'ler yeniden haritalanır


def kapsam_guncelle() -> int:
    """Her izlenen-kök PDF'i için kapsam (hangi konular, hangi sayfalar). Dosya başına bir kez; içerik değişirse yeniden."""
    from cikar import pdf_metni  # noqa: E402
    from isle import program_eslesmesi  # noqa: E402
    from kapsam import pdf_kapsami  # noqa: E402
    from checklist import KAPSAM  # noqa: E402
    kap = oku(KAPSAM, {})
    imza = oku(KAPSAM.with_name("kapsam_imza.json"), {})
    yeni = 0
    for p in pdfler():
        if "ders programı" in p["yol"].lower() or imza.get(p["yol"]) == p["sha256"] + KAPSAM_SURUM:
            continue
        try:
            metin, _ = pdf_metni(Path(p["tam"]))
            ana = program_eslesmesi(p["yol"], metin)
            kap[p["yol"]] = pdf_kapsami(p["yol"], metin, ana)
            imza[p["yol"]] = p["sha256"] + KAPSAM_SURUM
            yeni += 1
            yaz(KAPSAM, kap)
            yaz(KAPSAM.with_name("kapsam_imza.json"), imza)
        except Exception as e:  # noqa: BLE001
            log(f"kapsam hesaplanamadı: {p['yol']}: {e}")
    if yeni:
        log(f"kapsam: {yeni} PDF için konu/sayfa haritası güncellendi")
    return yeni


def kuyruga_al(ilk_kurulum: bool) -> int:
    """Kural (kullanıcı, 2026-10-11): Drive'daki HER PDF'in kapsadığı konulardan biri 2026-27 checklist'inde tamam değilse
    ('islenmeli' ya da 'yenilenmeli') PDF kuyruğa alınır — yalnız eksik konularıyla. Hepsi tamamsa yalnız kaydedilir."""
    from checklist import olustur  # noqa: E402
    kayit = oku(KAYIT, {})
    kuyruk = oku(KUYRUK, [])
    liste = olustur()
    bekleyen = {j["sha256"] for j in kuyruk if j["durum"] in ("bekliyor", "isleniyor", "taslak")}
    yeni = 0
    for p in pdfler():
        if "ders programı" in p["yol"].lower():
            kayit.setdefault(p["sha256"], {"durum": "program", "yol": p["yol"], "zaman": time.time()})
            continue
        if p["sha256"] in bekleyen or kayit.get(p["sha256"], {}).get("durum") in ("taslak", "hata"):
            continue
        # Karar checklist'ten: bu PDF'in bağlı olduğu satırlardan 2026-27 için eksik olanlar (kaynak kimliği + kesin konu eşitliği)
        konular = liste.get("pdf_konulari", {}).get(p["yol"]) or []
        eksik = [{**k, "konu": k.get("satir_konu") or k["konu"]} for k in konular if k.get("durum") in ("islenmeli", "yenilenmeli")]
        if not konular or not eksik:
            kayit.setdefault(p["sha256"], {"durum": "kapsanmis", "yol": p["yol"], "zaman": time.time()})
            continue
        uyari = "dosya adında eski yıl işareti var" if yil_sinifi(p["yol"], IZLENEN_KOK) == "gecmis" else ""
        kuyruk.append({"is_id": is_id(p["yol"], p["sha256"]), "yol": p["yol"], "tam": p["tam"], "sha256": p["sha256"],
                       "yil": "bu_yil", "uyari": uyari, "durum": "bekliyor", "eklendi": time.time(), "deneme": 0,
                       "konular": eksik})
        kayit.pop(p["sha256"], None)
        yeni += 1
        log(f"kuyruğa alındı: {p['yol']} → " + ", ".join(f"{k['konu']} (s.{k.get('sayfa_bas')}–{k.get('sayfa_bit')})" for k in eksik))
    yaz(KAYIT, kayit)
    yaz(KUYRUK, kuyruk)
    olustur()  # kuyruk değişti: checklist + rapor güncel kalsın
    return yeni


def bugun_islenen() -> int:
    bas = time.mktime(time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d"))
    return sum(1 for v in oku(KAYIT, {}).values() if v.get("durum") == "taslak" and v.get("zaman", 0) >= bas)


def sira_isle(zorla_is_id: str | None = None):
    kuyruk = oku(KUYRUK, [])
    simdi = time.time()
    if zorla_is_id:  # elle başlatma (test): saat penceresi ve günlük sınır atlanır
        hazir = [j for j in kuyruk if j["is_id"] == zorla_is_id or zorla_is_id in j["yol"]]
        if not hazir:
            log(f"kuyrukta yok: {zorla_is_id}")
            return
    else:
        hazir = [j for j in kuyruk if j["durum"] == "bekliyor" and j.get("sonra", 0) <= simdi]
        if not hazir:
            return
        if not saat_uygun():
            return
        if bugun_islenen() >= GUNLUK_SINIR:
            return
    j = hazir[0]
    j_kayit = next(k for k in kuyruk if k["is_id"] == j["is_id"])
    j_kayit["durum"] = "isleniyor"          # aynı iş iki kez başlamasın (döngü + elle)
    j_kayit["basladi"] = time.time()
    yaz(KUYRUK, kuyruk)
    log(f"işleniyor: {j['is_id']} {j['yol']}")
    from isle import isle  # noqa: E402  (ağır bağımlılıklar yalnız iş varken yüklensin)
    sonuc = isle(j)
    kuyruk = oku(KUYRUK, [])
    for k in kuyruk:
        if k["is_id"] != j["is_id"]:
            continue
        k["deneme"] = k.get("deneme", 0) + 1
        k["durum"] = "bekliyor"
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
    kapsam_guncelle()
    n = kuyruga_al(ilk)
    if n:
        log(f"{n} PDF kuyrukta (2026-27 checklist'inde eksik konuları var)")
    sira_isle()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bir-kez", action="store_true")
    ap.add_argument("--taramasiz", action="store_true", help="Drive taramadan yalnız kuyruk/işleme")
    ap.add_argument("--durum", action="store_true")
    ap.add_argument("--simdi", metavar="IS_ID_VEYA_AD", help="bu işi şimdi işle (saat/günlük sınır atlanır)")
    ap.add_argument("--checklist", action="store_true", help="yalnız kapsam + checklist + rapor (işleme yok)")
    a = ap.parse_args()
    if a.durum:
        return durum()
    if a.simdi:
        return sira_isle(a.simdi)
    if a.checklist:
        kapsam_guncelle()
        from checklist import olustur  # noqa: E402
        v = olustur()
        return print(f"checklist: {len(v['konular'])} konu → {v['sayim']}")
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
