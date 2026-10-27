#!/usr/bin/env python3
"""Hat sağlık denetimi: canlı site, Oracle SSH, yerel 3000, vektör servisleri, EMA işçisi, disk.
Sorun varsa çıkış 1 + meds_temp/hat/saglik.json; hat.py bunu durum.json'a yazar (yönetim › Hat panosunda kırmızı).
Bağımlı aşamalar (Oracle'a yükleyenler) sağlık kötüyken boşuna denemesin diye `oracle_ok` alanı okunur.
  saglik.py [--sessiz]
"""
import json, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "meds_temp/hat/saglik.json"


def http(url, t=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MeDSor-saglik/1 (+hat)"})
        with urllib.request.urlopen(req, timeout=t) as r:
            return r.status
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", None) or str(e)[:80]


def ssh_ok():
    try:
        return subprocess.run(["ssh", "-o", "ConnectTimeout=12", "-o", "BatchMode=yes", "medsor-oracle", "true"],
                              capture_output=True, timeout=30).returncode == 0
    except subprocess.TimeoutExpired:
        return False


def birim(ad):
    return subprocess.run(["systemctl", "--user", "is-active", ad], capture_output=True, text=True).stdout.strip()


def turev_eksikleri(api="https://api.nofrostlife.com.tr"):
    """H12: canlıda sesi olan derslerde türev veri (cümle zamanı, PDF işareti) var mı. Sunucu metin karması tutmayan
    dosyayı göndermez → özellik sessizce kaybolur; burada görünür olur. Döner {k2: [...], k1: [...]} (eksik ders anahtarları)."""
    out = {"k2": [], "k1": []}
    try:
        req = urllib.request.Request(f"{api}/api/canli-ders?sinama=1", headers={"User-Agent": "MeDSor-saglik/1 (+hat)"})
        dersler = json.load(urllib.request.urlopen(req, timeout=30)).get("dersler") or []
    except Exception as e:  # noqa: BLE001
        return {"hata": str(e)[:120]}
    for d in dersler:
        try:
            req = urllib.request.Request(f"{api}/api/canli-ders/{d['key']}", headers={"User-Agent": "MeDSor-saglik/1 (+hat)"})
            x = json.load(urllib.request.urlopen(req, timeout=30))
        except Exception:  # noqa: BLE001
            continue
        sesli = [v for v in x.get("varyantlar") or [] if v.get("ses")]
        if not sesli:
            continue
        k2 = str(d["key"])[:2] in ("k2", "k3", "k4", "k5", "k6")
        kontrol = [("cumleZaman", any(v.get("cumleZaman") for v in sesli))]
        if x.get("pdf"):  # PDF'i olmayan derste (2026-27 slaytı Drive'da yok) işaret üretilemez — eksik sayılmaz
            kontrol.append(("isaret", bool(x.get("isaret"))))
        if k2:  # kelime zamanlaması yalnız cihazda (GPU, meds-kelime-zaman-hat) üretilir: cihaz kapalıysa gecikir → görünür olsun
            kontrol.append(("kelimeZaman", any(v.get("kelimeZaman") for v in sesli)))
        eksik = [a for a, ok in kontrol if not ok]
        if eksik:
            out["k2" if str(d["key"])[:2] in ("k2", "k3", "k4", "k5", "k6") else "k1"].append(f"{d['key']}: {','.join(eksik)}")
    return out


def kapi_oz_sinama():
    """H5: kapılar bilinen iyi/kötü örnekle doğru karar veriyor mu (çöken kapı her şeyi 'içerik hatası' diye reddeder)."""
    import sys as _s
    _s.path.insert(0, str(KOK / "meds/scripts")); _s.path.insert(0, str(KOK / "meds/scripts/sesli_anlatim"))
    sorun = []
    try:
        from turkce_uslup import denetle as us
        if us("Hücre sayısı artar ve organ büyür.", "x") or not us("Bu bulgunun imzası nedir?", "x"):
            sorun.append("turkce_uslup")
    except Exception as e:  # noqa: BLE001
        sorun.append(f"turkce_uslup çöktü: {e}")
    try:
        from sik_aciklama import denetle as sk
        iyi = ("Penisilin G, Treponema pallidumun hücre duvarı sentezini bozan bir beta-laktam antibiyotiktir. "
               "Sifilizin tüm evrelerinde ilk seçenektir, bu yüzden soruda doğru cevap budur.")
        if sk(iyi, "x") or not sk("Bu sorunun cevabı değil.", "x"):
            sorun.append("sik_aciklama")
    except Exception as e:  # noqa: BLE001
        sorun.append(f"sik_aciklama çöktü: {e}")
    try:
        import konusma_v2 as kv
        c = {"id": "k2-01-c0001", "ses": "Hücre sayısı artar ve organ büyür.", "ekran": "**Hiperplazi**: hücre sayısı artar",
             "duzey": 0, "vurgu": [{"metin": "Hiperplazi", "tur": "terim"}]}
        d = {"surum": 2, "ders_id": "k2-01", "bolumler": [{"id": "k2-01-b01", "baslik": "x", "paragraflar": [
            {"id": "k2-01-p001", "sayfa": 1, "cumleler": [c]}]}]}
        kotu = json.loads(json.dumps(d)); kotu["bolumler"][0]["paragraflar"][0]["cumleler"][0]["id"] = "yanlis"
        if kv.dogrula(d, {1}) or not kv.dogrula(kotu, {1}):
            sorun.append("konusma_v2")
    except Exception as e:  # noqa: BLE001
        sorun.append(f"konusma_v2 çöktü: {e}")
    return sorun


def kayit_defteri_sorunlari():
    """H16: ders kimliği/kodu ve branş içi numara her kurulda tekil olmalı (Drive "33)" çakışması K1'de iki dersi aynı
    numaraya düşürmüştü). Sesli ders listesi K2+ numarayı yalnız buradan alır (src/services/canliDers.ts)."""
    sorun = []
    for p in sorted((KOK / "meds/src/data/dersler").glob("k[1-6].json")):
        ds = json.loads(p.read_text()).get("dersler") or []
        for alan in ("id", "kod"):
            g = [d[alan] for d in ds]
            sorun += [f"{p.stem}: {alan} çift {x}" for x in sorted({x for x in g if g.count(x) > 1})]
        bn = [(d["brans"], d["kod"].rstrip("0123456789"), int("".join(c for c in d["kod"][-2:] if c.isdigit()) or 0)) for d in ds]
        sorun += [f"{p.stem}: {b} numara {n} çift" for b, _, n in sorted({x for x in bn if bn.count(x) > 1})]
    return sorun


def ema_alt_surec_okunusu():
    """H17: ema_isci.sentezle alt süreçte çalışır; okunuş ayarı (uzun kısaltma / modül) orada da kurulmalı."""
    import inspect, sys as _s
    _s.path.insert(0, str(KOK / "meds/scripts/sesli_anlatim"))
    try:
        import ema_isci as E
        return [] if "uzun_kisaltma_ayarla(" in inspect.getsource(E.sentezle) else ["ema_isci.sentezle okunuş ayarını kurmuyor"]
    except Exception as e:  # noqa: BLE001
        return [f"ema_isci yüklenemedi: {e}"]


def claude_cli():
    """Gece hattının LLM aşamaları `claude -p` ile çalışır. 2026-10-23'te masaüstü uygulaması CLI'ı başka klasöre taşıdı,
    ~/.local/bin/claude sarmalayıcısı bulamadı ve her Claude aşaması sessizce düştü → sürüm sorgusu sağlık maddesi."""
    import subprocess
    try:
        r = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=60)
        return r.returncode == 0 and "Claude Code" in r.stdout
    except Exception:  # noqa: BLE001
        return False


def main():
    s = {
        "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "canli_api": http("https://api.nofrostlife.com.tr/api/health"),
        "oracle_ssh": ssh_ok(),
        "yerel_3000": http("http://127.0.0.1:3000/api/health"),
        "embed_bge": birim("meds-embed-bge"), "ema_isci": birim("meds-ema"), "claude_cli": claude_cli(),
        "disk_bos_gb": round(shutil.disk_usage(str(KOK)).free / 1e9, 1),
    }
    s["oracle_ok"] = s["canli_api"] == 200 and s["oracle_ssh"]
    s["kapi_ariza"] = kapi_oz_sinama() + ema_alt_surec_okunusu()
    s["kayit_defteri"] = kayit_defteri_sorunlari()
    s["turev_eksik"] = turev_eksikleri() if s["canli_api"] == 200 else {"hata": "canlı API yok"}
    sorun = [k for k, ok in [("canli_api", s["canli_api"] == 200), ("oracle_ssh", s["oracle_ssh"]),
                             ("yerel_3000", s["yerel_3000"] == 200), ("embed_bge", s["embed_bge"] == "active"),
                             ("ema_isci", s["ema_isci"] == "active"), ("claude_cli", s["claude_cli"]),
                             ("disk", s["disk_bos_gb"] >= 10),
                             ("kapi_ariza", not s["kapi_ariza"]), ("kayit_defteri", not s["kayit_defteri"]),
                             ("turev_eksik_k2", not (s["turev_eksik"].get("k2") or []))] if not ok]  # K1 eksikleri yalnız rapor
    s["sorun"] = sorun
    CIKTI.parent.mkdir(parents=True, exist_ok=True); CIKTI.write_text(json.dumps(s, ensure_ascii=False, indent=1))
    if "--sessiz" not in sys.argv:
        print(json.dumps(s, ensure_ascii=False))
    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main())
