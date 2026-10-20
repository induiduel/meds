#!/usr/bin/env python3
"""Hat panosu ders eylemleri — kuyruk işleyici (cihaz). Yönetim › Hat panosu (src/services/hatActionsRoutes.ts) her
eylemi meds_temp/hat/eylemler/<is>.json olarak kuyruğa yazar ve bu betiği geçici bir systemd --user birimiyle başlatır.
Ağır iş istek içinde yapılmaz; bu betik işleri sırayla, tek kopya (flock) ve gece hattı bitince çalıştırır.

Eylemler (yalnız Kurul 2+ ders zinciri; Kurul 1 otomatik hatta değildir):
  surdur   ders_zinciri.py --ders <id>                 takılan/bekleyen adımdan devam (geri çekilme yok sayılır)
  denetci  ders_zinciri.py --ders <id> --adim denetim  bağımsız denetçi yeniden; geçerse sonraki adımlar yeniden çalışır
  bastan   ara çıktılar meds_temp/spot_cozucu/<brans>/_eski/<kod>-<zaman>-bastan/, durum dosyası dersler/_eski/'ye
           kopyalanır, onay düşer, zincir 1. adımdan (hazirla) çalışır. Kaynak değişince yapılanın aynısı.
  cek      yayından çekme: kod onayli.json'dan çıkar → birlestir.py / asistan_birlestir.py yeniden (yalnız onaylılar
           yayına girer) → src/data/<brans>_{onem,cozucu,asistan} öncesi meds_temp/hat/yayindan_cekilen/<id>-<zaman>/
           yedeğinde. Başka dersin dosyası değişirse/silinirse yedek geri konur (kod 11). Durum dosyasına "cekildi"
           yazılır; ders zinciri bu dersi kendiliğinden yeniden yayına almaz (surdur/bastan/denetci kaldırır).
           Oracle'daki Öğren destesi/ders paketi (ders işçisi yayını) bu eylemle geri alınmaz.

  hat_eylem.py --isle            kuyruktaki işleri bitene dek işle (birim bunu çalıştırır)
  hat_eylem.py --goster <is>     işin ne yapacağını yazdırır, hiçbir şeye dokunmaz (kuru)
İş dosyası: {id, ders, kurul, eylem, durum: bekliyor|calisiyor|bitti|hata|iptal, olusturma, baslama, bitis, kod, kim, not}
"""
import argparse, datetime as dt, fcntl, json, os, shutil, subprocess, sys, time
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
EYLEM = KOK / "meds_temp/hat/eylemler"
CEKILEN = KOK / "meds_temp/hat/yayindan_cekilen"
SC = MEDS / "scripts/spot_cozucu"
sys.path.insert(0, str(MEDS / "otomasyon"))
import ders_zinciri as DZ  # noqa: E402

SONRAKI = {"denetim": ["birlestir", "asistan", "ses", "oracle"]}


def simdi():
    return dt.datetime.now().isoformat(timespec="seconds")


def is_yaz(j):
    p = EYLEM / f"{j['id']}.json"; t = p.with_suffix(".tmp")
    t.write_text(json.dumps(j, ensure_ascii=False, indent=1)); t.replace(p)


def ders_bul(did):
    k = int(did.split("-")[0][1:])
    return next((d for d in json.loads((MEDS / f"src/data/dersler/k{k}.json").read_text())["dersler"] if d["id"] == did), None)


def zincir(d, *ek, kuru=False):
    kom = [sys.executable, str(MEDS / "otomasyon/ders_zinciri.py"), "--kurul", str(d["kurul"]), "--ders", d["id"], *ek]
    if kuru:
        print("   (kuru) $", " ".join(kom)); return 0
    print("   $", " ".join(kom), flush=True)
    return subprocess.run(kom, cwd=KOK, env={**os.environ, "CUDA_VISIBLE_DEVICES": ""}).returncode


def cekildi_kaldir(d, kuru):
    s = DZ.durum_oku(d)
    if s.get("cekildi") and not kuru:
        s.pop("cekildi"); DZ.durum_yaz(d, s); print("   'yayından çekildi' işareti kaldırıldı")


def e_surdur(d, kuru):
    cekildi_kaldir(d, kuru)
    return zincir(d, kuru=kuru)


def e_denetci(d, kuru):
    s = DZ.durum_oku(d)
    eksik = [x for x in ("hazirla", "onem", "cozucu") if (s["adimlar"].get(x) or {}).get("kod") != 0]
    if eksik:
        print("   denetçiye gönderilemez: önce şu adımlar geçmeli:", ", ".join(eksik)); return 2
    cekildi_kaldir(d, kuru)
    r = zincir(d, "--adim", "denetim", kuru=kuru)
    if r:
        return r
    if not kuru:  # denetim değişti → birleştirme ve sonrası yeniden (onaylı içerik yeniden yayına girer)
        s = DZ.durum_oku(d)
        for x in SONRAKI["denetim"]:
            s["adimlar"].pop(x, None)
        DZ.durum_yaz(d, s)
    else:
        print("   (kuru) birlestir, asistan, ses, oracle adımları sıfırlanır")
    return zincir(d, kuru=kuru)


def e_bastan(d, kuru):
    W = DZ.W0 / DZ.brans_klasoru(d); kod = d["kod"]; ts = f"{dt.datetime.now():%Y%m%d%H%M%S}"
    eski = W / "_eski" / f"{kod}-{ts}-bastan"
    for alt in ("onem", "cozucu", "denetim", "asistan/cikti", "onem_haritasi", "cikmis", "girdi"):
        f = W / alt / (f"{kod}.md" if alt == "denetim" else f"{kod}.json")
        if f.exists():
            print(f"   yedek: {f.relative_to(KOK)} → {eski.relative_to(KOK)}/")
            if not kuru:
                eski.mkdir(parents=True, exist_ok=True); shutil.copy2(f, eski / f"{alt.replace('/', '_')}_{f.name}")
                if alt in ("onem", "cozucu", "denetim", "asistan/cikti"):
                    f.unlink()  # yazar Claude eski çıktıyı görmesin (kaynak değişince yapılanın aynısı)
    sp = DZ.DURUM / f"{d['id']}.json"
    if kuru:
        print(f"   (kuru) durum {sp.relative_to(KOK)} → dersler/_eski/, onay düşer, zincir baştan")
        return zincir(d, kuru=True)
    if sp.exists():
        (DZ.DURUM / "_eski").mkdir(parents=True, exist_ok=True); shutil.copy2(sp, DZ.DURUM / "_eski" / f"{d['id']}-{ts}.json")
    s = DZ.durum_oku(d)
    DZ.durum_yaz(d, {"kaynak_sha": s.get("kaynak_sha"), "adimlar": {}, "hata_sayisi": 0, "bastan": simdi()})
    if W.exists():
        DZ.onayli_yaz(W, kod, False)
    return zincir(d)


def _dosyalar(klasor):
    return {f.name: f.read_bytes() for f in klasor.glob("*.json") if f.name != "index.json"} if klasor.exists() else {}


def _index_kodlar(klasor):
    p = klasor / "index.json"
    try:
        return [x.get("kod") for x in json.loads(p.read_text()).get("dersler") or []]
    except (OSError, ValueError):
        return []


def e_cek(d, kuru):
    if d["kurul"] < 2:
        print("   Kurul 1 içeriği otomatik hatta değil; yayından çekme yapılmaz"); return 2
    W = DZ.W0 / DZ.brans_klasoru(d); kod = d["kod"]
    hedef = [MEDS / "src/data" / f"{W.name}_{t}" for t in ("onem", "cozucu", "asistan")]
    ait = lambda ad: ad == f"{kod}.json" or ad.startswith(f"{kod}-")  # noqa: E731  çözücü setleri <kod>-1.json
    yayinda = [f"{k.name}/{n}" for k in hedef for n in _dosyalar(k) if ait(n)]
    print(f"   yayındaki dosyalar ({len(yayinda)}):", ", ".join(yayinda) or "-")
    if kuru:
        print(f"   (kuru) yedek → {CEKILEN.relative_to(KOK)}/{d['id']}-<zaman>/; {kod} onayli.json'dan çıkar; "
              f"birlestir.py {W.name} --taslak; asistan_birlestir.py {W.name}; ogren_esle.py; başka ders değişirse geri al")
        return 0
    if not yayinda:
        print("   bu dersin yayımlanmış zincir çıktısı yok; yalnız işaret konur")
    yedek = CEKILEN / f"{d['id']}-{dt.datetime.now():%Y%m%d%H%M%S}"
    yedek.mkdir(parents=True, exist_ok=True)
    once = {}
    for k in hedef:
        if k.exists():
            shutil.copytree(k, yedek / k.name)
        once[k] = (_dosyalar(k), _index_kodlar(k))
    onayli_once = (W / "onayli.json").read_text() if (W / "onayli.json").exists() else None
    if onayli_once is not None:
        (yedek / "onayli.json").write_text(onayli_once)
    if W.exists():
        DZ.onayli_yaz(W, kod, False)
    r = 0
    if (W / "girdi").exists():
        r = subprocess.run([sys.executable, str(SC / "birlestir.py"), W.name, "--taslak"], cwd=KOK).returncode
    if r == 0 and (W / "asistan" / "cikti").exists() and (hedef[0] / "index.json").exists():
        r = subprocess.run([sys.executable, str(SC / "asistan_birlestir.py"), W.name], cwd=KOK).returncode
    # başka dersler aynen kalmalı: dosya içeriği birebir, index kod sırası yalnız bu ders eksik
    sorun = []
    for k in hedef:
        f0, i0 = once[k]; f1, i1 = _dosyalar(k), _index_kodlar(k)
        for ad, icerik in f0.items():
            if not ait(ad) and f1.get(ad) != icerik:
                sorun.append(f"{k.name}/{ad} {'silindi' if ad not in f1 else 'değişti'}")
        if [x for x in i0 if not (x == kod or str(x).startswith(f"{kod}-"))] != [x for x in i1]:
            sorun.append(f"{k.name}/index.json başka dersleri de değiştirdi")
        if any(ait(ad) for ad in f1):
            sorun.append(f"{k.name}: {kod} hâlâ yayında")
    if r or sorun:
        print("   HATA: yayından çekme beklenmeyen değişiklik yaptı — yedek geri konuyor:", *sorun[:10], sep="\n     ")
        for k in hedef:
            shutil.rmtree(k, ignore_errors=True)
            if (yedek / k.name).exists():
                shutil.copytree(yedek / k.name, k)
        if onayli_once is not None:
            (W / "onayli.json").write_text(onayli_once)
        return r or 11
    subprocess.run([sys.executable, str(SC / "ogren_esle.py")], cwd=MEDS)
    s = DZ.durum_oku(d)
    s["cekildi"] = {"zaman": simdi(), "yedek": str(yedek.relative_to(KOK)), "dosyalar": yayinda}
    DZ.durum_yaz(d, s)
    print(f"   {d['id']} yayından çekildi; yedek {yedek.relative_to(KOK)}. Canlıya gece içerik dağıtımıyla (icerik_dagit) gider.")
    return 0


EYLEMLER = {"surdur": e_surdur, "denetci": e_denetci, "bastan": e_bastan, "cek": e_cek}


def gece_calisiyor():
    r = subprocess.run(["systemctl", "--user", "is-active", "--quiet", "meds-hat-gece.service"])
    return r.returncode == 0


def isle():
    EYLEM.mkdir(parents=True, exist_ok=True)
    kilit = open(EYLEM / ".isle.lock", "w")
    try:
        fcntl.flock(kilit, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("başka bir işleyici çalışıyor"); return 0
    # önceki işleyici yarıda kaldıysa (makine kapandı) işi yeniden sıraya al
    for p in EYLEM.glob("*.json"):
        j = json.loads(p.read_text())
        if j.get("durum") == "calisiyor":
            j["durum"] = "bekliyor"; j["not"] = "işleyici yarıda kaldı; yeniden sıraya alındı"; is_yaz(j)
    while True:
        bekleyen = sorted((json.loads(p.read_text()) for p in EYLEM.glob("*.json")), key=lambda j: j.get("olusturma") or "")
        bekleyen = [j for j in bekleyen if j.get("durum") == "bekliyor"]
        if not bekleyen:
            return 0
        if gece_calisiyor():  # gece hattı ders zincirini çalıştırıyor olabilir: çakışma yok
            print("gece hattı çalışıyor; 60 sn sonra yeniden bakılacak", flush=True); time.sleep(60); continue
        j = bekleyen[0]
        d = ders_bul(j["ders"])
        j.update(durum="calisiyor", baslama=simdi(), pid=os.getpid()); is_yaz(j)
        log = EYLEM / f"{j['id']}.log"
        asil = (os.dup(1), os.dup(2))
        with open(log, "a") as f:
            sys.stdout.flush(); os.dup2(f.fileno(), 1); os.dup2(f.fileno(), 2)
            print(f"=== {simdi()} {j['eylem']} {j['ders']} (isteyen: {j.get('kim') or '-'})", flush=True)
            try:
                kod = EYLEMLER[j["eylem"]](d, bool(j.get("kuru"))) if d else 2
                if not d:
                    print("   ders kayıt defterinde yok")
            except Exception as e:  # iş düşse de kuyruk sürsün; hata panoda görünür
                print("   HATA:", repr(e)); kod = 1
            print(f"=== {simdi()} bitti kod={kod}", flush=True)
            os.dup2(asil[0], 1); os.dup2(asil[1], 2); os.close(asil[0]); os.close(asil[1])
        j.update(durum="bitti" if kod == 0 else "hata", bitis=simdi(), kod=kod); is_yaz(j)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--isle", action="store_true"); ap.add_argument("--goster")
    a = ap.parse_args()
    if a.goster:
        p = Path(a.goster)
        j = json.loads(p.read_text()) if p.exists() else {"ders": a.goster.split(":")[0], "eylem": a.goster.split(":")[1]}
        d = ders_bul(j["ders"])
        if not d:
            sys.exit("ders yok")
        print(f"{j['eylem']} {d['id']} ({d['konu']})")
        return EYLEMLER[j["eylem"]](d, True)
    if a.isle:
        return isle()
    ap.print_help(); return 0


if __name__ == "__main__":
    sys.exit(main())
