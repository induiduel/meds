#!/usr/bin/env python3
"""Ders zinciri provası: yayımlanmış bir Kurul 1 dersini sahte Kurul 2 dersi gibi zincirin tamamından geçirir (gerçek
Claude + gerçek EMA), canlıya HİÇBİR ŞEY göndermeden.

Yalıtım:
  - branş klasörü `provak2` (site k[2-6]* kalıbını tarar → sitede görünmez; birlestir kurul_no = 1 sayar, zararsız)
  - `oracle` adımı ve içerik sürüm kaydı ÇALIŞMAZ; Öğren adım sesi (gerçek desteye yazar + Oracle'a gönderir) ÇALIŞMAZ
  - bitince src/data/provak2_* ve data/provak2_* → meds_temp/prova/<zaman>/ (paket/dağıtıma girmez)
Rapor: meds_temp/prova/<zaman>/rapor.json (adım, kod, süre, sayılar).
  prova.py [--is 20261011-e9e8f4b0d1] [--adim onem]   (--adim: yalnız o adımdan devam)
"""
import argparse, datetime as dt, json, shutil, sys, time
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
sys.path.insert(0, str(MEDS / "otomasyon")); sys.path.insert(0, str(MEDS / "scripts/ders_isci"))
import ders_zinciri as Z  # noqa: E402

BRANS = "provak2"
ADIMLAR = ["hazirla", "onem", "cozucu", "denetim", "birlestir", "asistan", "ses"]  # oracle YOK


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--is", dest="is_id", default="20261011-e9e8f4b0d1")
    ap.add_argument("--adim", choices=ADIMLAR)
    a = ap.parse_args()
    pk = dict(next(y for y in json.load(open(MEDS / "scripts/ders_isci/yayin_kaydi.json")) if y["is_id"] == a.is_id))
    pk["deste_id"] = None  # Öğren adım sesi gerçek desteye yazar → provada kapalı
    d = {"id": "k2-99", "kod": "2x99", "kurul": 2, "brans": pk["ders"], "konu": pk["konu"], "cikmis_konular": [pk["konu"]],
         "cikmis_kurul": pk.get("kurul", 1)}  # prova: çıkmışlar dersin gerçek kurulundan
    W = Z.W0 / BRANS; W.mkdir(parents=True, exist_ok=True)
    Z.brans_klasoru = lambda _d: BRANS  # noqa: E731  (zincir içi klasör adı)
    # sayfalar.json + sayfa görüntüleri (eski yayınlarda yok; görsel/tablo/hoca vurgusu adımı da sınansın)
    kaynak = Z.kaynak_getir(pk)
    if not (kaynak.parent / "sayfalar.json").exists():
        import cikar
        pdf = KOK / "meds_downloads/drive_root" / pk["pdf"]
        print("sayfa varlıkları:", cikar.sayfa_varliklari(pdf, kaynak.parent))
    rapor = {"is_id": a.is_id, "ders": pk["konu"], "basla": dt.datetime.now().isoformat(timespec="seconds"), "adimlar": []}
    bas = ADIMLAR.index(a.adim) if a.adim else 0
    ok = True
    for x in ADIMLAR[bas:]:
        t0 = time.time(); print(f"\n▶ {x}", flush=True)
        kod = Z.IS[x](d, pk, W, False)
        rapor["adimlar"].append({"adim": x, "kod": kod, "sn": round(time.time() - t0)})
        print(f"  {x}: kod {kod} · {round(time.time() - t0)} sn", flush=True)
        if kod:
            ok = False; break
    # çıktı sayıları
    def say(p, anahtar):
        try:
            j = json.loads(p.read_text()); return len(j.get(anahtar) or [])
        except Exception:  # noqa: BLE001
            return None
    rapor["sayilar"] = {
        "onem_madde": say(W / "onem" / "2x99.json", "maddeler"),
        "cozucu_soru": say(W / "cozucu" / "2x99.json", "sorular"),
        "denetim_raporu": (W / "denetim" / "2x99.md").exists(),
        "onayli": json.loads((W / "onayli.json").read_text()) if (W / "onayli.json").exists() else [],
        "ema_klip": len(list((MEDS / "data" / f"{BRANS}_cozucu").rglob("*.mp3"))) + len(list((MEDS / "data" / f"{BRANS}_asistan").rglob("*.mp3"))),
    }
    rapor["bitti"] = dt.datetime.now().isoformat(timespec="seconds"); rapor["sonuc"] = "TAMAM" if ok else "DURDU"
    hedef = KOK / "meds_temp/prova" / dt.datetime.now().strftime("%Y%m%d_%H%M")
    hedef.mkdir(parents=True, exist_ok=True)
    for p in list((MEDS / "src/data").glob(f"{BRANS}_*")) + list((MEDS / "data").glob(f"{BRANS}_*")):
        on = "src_data" if p.parent == MEDS / "src/data" else "data"  # iki kökte aynı adlı klasörler var
        shutil.move(str(p), hedef / f"{on}__{p.name}")  # pakete/dağıtıma girmesin
    (hedef / "rapor.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1))
    print("\nRAPOR", json.dumps(rapor, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
