#!/usr/bin/env python3
"""Ders zinciri provası: yayımlanmış bir Kurul 1 dersini sahte Kurul 2 dersi gibi zincirin tamamından geçirir (gerçek
Claude + gerçek EMA), canlıya HİÇBİR ŞEY göndermeden.

Yalıtım:
  - branş klasörü `provak2`: birleştirme src/data/provak2_{onem,cozucu} yazar → prova sonunda silinir; Öğren eşlemesi
    (bütün branşların cozucu_ogren'i) MEDS_PROVA=1 ile atlanır (2026-10-24: K1 dosyalarına dokunuyordu)
  - `oracle` adımı ve içerik sürüm kaydı ÇALIŞMAZ; Öğren adım sesi (gerçek desteye yazar + Oracle'a gönderir) ÇALIŞMAZ
  - bitince src/data/provak2_* ve data/provak2_* → meds_temp/prova/<zaman>/ (paket/dağıtıma girmez)
Rapor: meds_temp/prova/<zaman>/rapor.json (adım, kod, süre, sayılar).
  prova.py [--is 20261011-e9e8f4b0d1] [--adim onem]   (--adim: yalnız o adımdan devam)
  prova.py --gorev [--sesli] [--ses-yok]   R4 görev yolu: önem/çözücü/asistan/denetim `mod: aktif` gibi, YALNIZ ücretsiz
           ajan katmanıyla (MEDS_GOREV_KATMAN=A: OpenCode, yetmezse yerel Claude; --claudesuz ile Claude kapalı); --sesli taslak kopyasından sesli metin v2 (sesli_bolum);
           --ses-yok EMA adımını atlar. Rapor Claude bütçe sayacındaki farkı da yazar.
"""
import argparse, datetime as dt, json, os, shutil, subprocess, sys, time
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
sys.path.insert(0, str(MEDS / "otomasyon")); sys.path.insert(0, str(MEDS / "scripts/ders_isci"))
import ders_zinciri as Z  # noqa: E402

BRANS = "provak2"
ADIMLAR = ["hazirla", "onem", "cozucu", "denetim", "birlestir", "asistan", "ses"]  # oracle YOK


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--is", dest="is_id", default="20261011-e9e8f4b0d1")
    ap.add_argument("--adim", choices=ADIMLAR)
    ap.add_argument("--gorev", action="store_true"); ap.add_argument("--sesli", action="store_true")
    ap.add_argument("--ses-yok", action="store_true")
    ap.add_argument("--claudesuz", action="store_true", help="görev yolunda yerel Claude yedeğini kapat (yalnız OpenCode)")
    ap.add_argument("--profil", help="ajan profili: karma | opencode | antigravity | claude | commandcode (butce.json)")
    a = ap.parse_args()
    adimlar = [x for x in ADIMLAR if not (a.ses_yok and x == "ses")]
    os.environ["MEDS_PROVA"] = "1"       # ders_zinciri: Öğren eşlemesi (bütün branşlar) atlanır
    claude_once = None
    if a.gorev:
        Z.gorev_modu = lambda _g: "aktif"  # noqa: E731  (provada gölge değil, görev yolu)
        os.environ["MEDS_GOREV_KATMAN"] = "A"      # OpenCode; yetmezse yerel Claude (2026-10-24). --claudesuz: Claude kapalı
        if a.claudesuz:
            os.environ["MEDS_AJAN_CLAUDE"] = "0"
        if a.profil:
            os.environ["MEDS_AJAN_PROFIL"] = a.profil
        sys.path.insert(0, str(MEDS / "otomasyon")); from llm import yonlendir as Y
        claude_once = Y._sayac()["cagri"]
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
    bas = adimlar.index(a.adim) if a.adim else 0
    ok = True
    for x in adimlar[bas:]:
        t0 = time.time(); print(f"\n▶ {x}", flush=True)
        kod = Z.IS[x](d, pk, W, False)
        rapor["adimlar"].append({"adim": x, "kod": kod, "sn": round(time.time() - t0)})
        print(f"  {x}: kod {kod} · {round(time.time() - t0)} sn", flush=True)
        if kod:
            ok = False; break
    if a.sesli and ok:
        # ders işçisi taslağının KOPYASINDA sesli metin v2 (yayımlanmış taslak değişmez)
        T = KOK / "meds_temp/prova" / f"taslak_{a.is_id}"
        if T.exists():
            shutil.rmtree(T)
        shutil.copytree(KOK / pk["kaynak_md"].rsplit("/", 1)[0], T)
        for f in ("konusma_v2.json", "konusma_metni.md", "konusma_sayfalari.json"):
            (T / f).unlink(missing_ok=True)
        t0 = time.time(); print("\n▶ sesli (görev yolu)", flush=True)
        kod = subprocess.run([str(MEDS / ".venv-ocr/bin/python"), str(MEDS / "otomasyon/llm/spot_zinciri.py"), "sesli", str(T), "-"]
                             + (["--katman", "A"] if a.gorev else [])).returncode
        rapor["adimlar"].append({"adim": "sesli", "kod": kod, "sn": round(time.time() - t0), "taslak": str(T)})
        print(f"  sesli: kod {kod} · {round(time.time() - t0)} sn", flush=True)
        ok = ok and kod == 0
        v2 = T / "konusma_v2.json"
        if v2.exists():
            j = json.loads(v2.read_text())
            rapor["sesli"] = {"bolum": len(j["bolumler"]), "cumle": sum(len(p["cumleler"]) for b in j["bolumler"] for p in b["paragraflar"])}
    if claude_once is not None:
        rapor["claude_cagri"] = Y._sayac()["cagri"] - claude_once
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
    for alt in ("_onem", "_cozucu"):                       # provanın branş klasörü canlı veri dizininde kalmasın
        shutil.rmtree(MEDS / "src" / "data" / f"provak2{alt}", ignore_errors=True)
    (hedef / "rapor.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1))
    print("\nRAPOR", json.dumps(rapor, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
