#!/usr/bin/env python3
"""MeDSor hat çalıştırıcısı — otomasyon/hat.json kayıt defterini okur.

  hat.py --liste                 aşamalar, durum, bağımlılık sırası, eksikler
  hat.py --dogrula               defter tutarlılığı (bilinmeyen bağımlılık, döngü, eksik betik)
  hat.py --gece [--kacirilan]    'gece' tetikli + durum=hazir yerel aşamaları sırayla çalıştırır
  hat.py --calistir ID           tek aşama
Her çalıştırma meds_temp/hat/durum.json'a (son başarı zamanı, çıkış kodu) ve hat.log'a yazılır.
"Oracle:" ile başlayan komutlar sunucuda çalışır; burada yalnız listelenir.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
DEFTER = MEDS / "otomasyon/hat.json"
DURUM = KOK / "meds_temp/hat/durum.json"


def yukle():
    return json.loads(DEFTER.read_text())


def sira(asamalar):
    ad = {a["id"]: a for a in asamalar}; out, gez = [], set()
    def ziyaret(i, yol=()):
        if i in yol: raise SystemExit(f"HATA döngü: {' → '.join(yol + (i,))}")
        if i in gez: return
        for g in ad[i].get("gerekir", []): ziyaret(g, yol + (i,))
        gez.add(i); out.append(ad[i])
    for a in asamalar: ziyaret(a["id"])
    return out


def degiskenler():
    sys.path.insert(0, str(MEDS / "scripts/takvim"))
    from aktif_kurul import durum
    d = durum(dt.date.today().isoformat())
    return {"aktif_kurul": str(d["aktif"]), "son_sinav": str(d["son_sinav"] or "")}


def dogrula(df):
    ids = {a["id"] for a in df["asamalar"]}; hata = []
    for a in df["asamalar"]:
        for g in a.get("gerekir", []):
            if g not in ids: hata.append(f"{a['id']}: bilinmeyen bağımlılık {g}")
        if a.get("durum") not in ("hazir", "el", "plan"): hata.append(f"{a['id']}: durum geçersiz")
        k = a.get("komut", "")
        if a.get("durum") == "hazir" and not k.startswith("Oracle:"):
            for yol in re.findall(r"meds/[\w./-]+\.(?:py|sh)", k):
                if not (KOK / yol).exists(): hata.append(f"{a['id']}: betik yok {yol}")
    sira(df["asamalar"])
    return hata


def kaydet_durum(aid, kod, not_=""):
    """durum.json'a tek aşamanın sonucunu yazar (kilitli oku-değiştir-yaz: elle --calistir ile gece işi çakışmasın)."""
    import fcntl
    DURUM.parent.mkdir(parents=True, exist_ok=True)
    with open(DURUM.parent / ".durum.lock", "w") as k:
        fcntl.flock(k, fcntl.LOCK_EX)
        durum = json.loads(DURUM.read_text()) if DURUM.exists() else {}
        simdi = dt.datetime.now().isoformat(timespec="seconds")
        onceki = durum.get(aid, {})
        durum[aid] = {"son": simdi, "kod": kod, "son_basari": simdi if kod == 0 else onceki.get("son_basari"),
                      **({"not": not_} if not_ else {})}
        tmp = DURUM.with_suffix(".tmp"); tmp.write_text(json.dumps(durum, ensure_ascii=False, indent=1)); tmp.replace(DURUM)
    with open(DURUM.parent / "hat.log", "a") as f:
        f.write(f"{dt.datetime.now().isoformat(timespec='seconds')} {aid} kod={kod}{' ' + not_ if not_ else ''}\n")


def calistir(a, v):
    komut = a["komut"].format(**v, ders_id="", deste_id="")
    print(f"▶ {a['id']}: {komut}")
    r = subprocess.run(komut, shell=True, cwd=KOK, env={**os.environ, "CUDA_VISIBLE_DEVICES": ""})
    kaydet_durum(a["id"], r.returncode)
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--liste", action="store_true"); ap.add_argument("--dogrula", action="store_true")
    ap.add_argument("--gece", action="store_true"); ap.add_argument("--kacirilan", action="store_true")
    ap.add_argument("--calistir")
    a = ap.parse_args(); df = yukle()
    if a.dogrula or a.liste:
        h = dogrula(df)
        if a.liste:
            dr = json.loads(DURUM.read_text()) if DURUM.exists() else {}
            for s in sira(df["asamalar"]):
                print(f"{s['durum']:5} {s['kapsam']:6} {s['id']:18} ← {','.join(s.get('gerekir', [])) or '-':28} "
                      f"son başarı: {dr.get(s['id'], {}).get('son_basari') or '-'}")
                if s.get("eksik"): print(f"{'':32}eksik: {s['eksik']}")
        for x in h: print("HATA", x)
        print(f"{len(df['asamalar'])} aşama · {len(h)} HATA"); sys.exit(1 if h else 0)
    v = degiskenler()
    if a.calistir:
        s = next((x for x in df["asamalar"] if x["id"] == a.calistir), None) or sys.exit(f"bilinmeyen aşama {a.calistir}")
        sys.exit(calistir(s, v))
    if a.gece:
        dr = json.loads(DURUM.read_text()) if DURUM.exists() else {}
        bugun = dt.date.today().isoformat(); kotu = 0
        dusen: set[str] = set()  # bu gece başarısız olan (ya da bağımlılığı düştüğü için atlanan) aşamalar
        for s in sira(df["asamalar"]):
            if s["durum"] != "hazir" or "gece" not in s.get("tetik", []) or s["komut"].startswith("Oracle:"):
                continue
            if a.kacirilan and (dr.get(s["id"], {}).get("son_basari") or "") >= bugun:
                continue  # bugün zaten başarıyla çalıştı
            neden = [g for g in s.get("gerekir", []) if g in dusen]
            if neden:  # bağımlılık bu gece düştü: bu aşama çalışmaz (yarım girdiyle yayın yok)
                dusen.add(s["id"]); kotu += 1
                kaydet_durum(s["id"], 10, f"bağımlılık başarısız: {', '.join(neden)}")
                print(f"⏭ {s['id']}: atlandı (bağımlılık başarısız: {', '.join(neden)})")
                continue
            kod = calistir(s, v)
            if kod == 3:  # bilinçli atlama (ör. çalışma ağacı kirli): hata değil ama başarı da değil, panoda görünür
                print(f"⏭ {s['id']}: atlandı (kod 3)")
                continue
            if kod != 0:
                dusen.add(s["id"]); kotu += 1
        sys.exit(1 if kotu else 0)
    ap.print_help()


if __name__ == "__main__":
    main()
