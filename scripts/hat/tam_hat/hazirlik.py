#!/usr/bin/env python3
"""Tam içerik hattı · hazırlık evresi: birbirinden bağımsız girdi işlerini kaynak tavanlı PARALEL yürütür (LLM yok).

  python3 scripts/hat/tam_hat/hazirlik.py <ders klasörü> --ders <key> [--kurul 2] [--cpu-is 2]

Klasörde beklenenler (olanlar işlenir, olmayan iş atlanır — eksiklik durdurmaz, kural 22):
  orijinal.pdf (zorunlu) · ogrenci_not.pdf · hoca_ses.m4a (çok parçalıysa hoca_ses_2.m4a, hoca_ses_3.m4a …)
İşler ve kaynak payı (makine 15 GB RAM / 20 çekirdek; Claude oturumları korunur):
  GPU (tek iş):  hoca dökümü → hoca_dokum.json            hoca_dokum_gpu.sh (AGENTS §10 altıncı istisna, ≤2500 MHz)
  CPU (en çok --cpu-is eşzamanlı, her biri CPUQuota=200% MemoryMax=2G):
     sayfa metni   → sayfalar.json {"1": "...", ...}       pdftotext, sayfa sayfa (kaynak kapısının temeli)
     sayfa görüntü → op/s-NNN.png                          pdftoppm 110 dpi (alt ajanlar görüntüyü açarak okur — H111)
     öğrenci notu  → ogrenci_not_isaret.json               kroki/ogrenci_not.py
     çıkmış aday   → cikmis_aday.json                      ders_isci/isle.py::cikmis_adaylari (sitenin araması; elle doğrulanır — H79)
     öğrenci önem  → ogrenci_onem.json                     ogrenci_onem/oku.py: geçmiş yıl öğrenci notunun A/B birimleri bu
                                                           yılın sayfalarına eşlenir (OGRENCI_ONEM_YONTEMI.md; ders notta yoksa boş geçer)
Her işin süresi ve sonucu <klasör>/hazirlik_durum.json'a yazılır; sonraki evre (anlatım, deste, soru) beklemeden başlar,
yalnız hoca vurgusu gerektiren adım döküm bitince eklenir.
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = _kok.MEDS  # meds/
PY = sys.executable
PY_CV = str(KOK / ".venv-ocr/bin/python")  # cv2 + pymupdf bu ortamda
API = os.environ.get("MEDS_ISCI_API", "http://127.0.0.1:3000")  # yerel site araması (benzer soru)


def cpu_run(ad: str, komut: list[str]) -> list[str]:
    return ["systemd-run", "--user", "--wait", "--collect", "--quiet", "--pipe", f"--unit=meds-hazirlik-{ad}-{os.getpid()}-{int(time.time())}",
            "-p", "CPUQuota=200%", "-p", "MemoryMax=2G", "-p", "OOMScoreAdjust=500",
            "-E", "CUDA_VISIBLE_DEVICES=", *komut]


def calistir(ad: str, komut: list[str], log: Path) -> dict:
    t = time.time()
    with open(log, "w") as f:
        r = subprocess.run(komut, stdout=f, stderr=subprocess.STDOUT, cwd=KOK)
    return {"is": ad, "kod": r.returncode, "sn": round(time.time() - t), "log": str(log)}


def sayfa_metni(pdf: Path, cikti: Path) -> list[str]:
    kod = ("import json,subprocess,sys\n"
           "p,c=sys.argv[1],sys.argv[2]\n"
           "n=int([l for l in subprocess.run(['pdfinfo',p],capture_output=True,text=True).stdout.splitlines() if l.startswith('Pages:')][0].split()[1])\n"
           "import re\n"
           # Slayt madde imi (○/•) pdftotext'te 'o' harfi olarak kelimeye yapışır ('oOsteogenezis'): satır başında ve
           # büyük harften önceki 'o' atılır (k2-08: kaynak kapısının kelime eşlemesini bozuyordu)
           "ay=lambda t: re.sub(r'(?m)^(\\s*)[o•▪●■◦](?=[A-ZÇĞİÖŞÜ])', r'\\1', t)\n"
           "d={str(i):ay(subprocess.run(['pdftotext','-layout','-f',str(i),'-l',str(i),p,'-'],capture_output=True,text=True).stdout) for i in range(1,n+1)}\n"
           "json.dump(d,open(c,'w'),ensure_ascii=False,indent=1);print(n,'sayfa')\n")
    return [PY, "-I", "-c", kod, str(pdf), str(cikti)]


def cikmis_aday(sayfalar: Path, kurul: int, cikti: Path) -> list[str]:
    kod = ("import json,sys\n"
           f"sys.path.insert(0,{str(KOK / 'scripts/uretim/ders_isci')!r})\n"
           "from isle import cikmis_adaylari\n"
           "d=json.load(open(sys.argv[1]))\n"
           "metin=''.join(f'=== SAYFA {k}\\n{v}\\n' for k,v in d.items())\n"
           "a=cikmis_adaylari(metin,int(sys.argv[2]))\n"
           "json.dump(a,open(sys.argv[3],'w'),ensure_ascii=False,indent=1);print(len(a),'aday')\n")
    return ["env", f"MEDS_ISCI_API={API}", PY, "-c", kod, str(sayfalar), str(kurul), str(cikti)]


def ses_parcalari(k: Path) -> list[Path]:
    """Hoca sesi tek ya da çok parça olabilir (H623, k2-41: "Part1" + "Part 2"): hoca_ses.m4a, hoca_ses_2.m4a, hoca_ses_3.mp3 …
    Sıra: parça numarası (numarasız = 1)."""
    def no(p: Path) -> int:
        m = re.search(r"hoca_ses[_-]?(\d+)$", p.stem)
        return int(m.group(1)) if m else 1
    return sorted((p for p in k.glob("hoca_ses*") if p.suffix.lower() in (".m4a", ".mp3", ".wav", ".ogg", ".aac", ".mp4")), key=no)


def dokum_birlestir(parca_dokumleri: list[tuple[str, dict]]) -> dict:
    """Parça dökümlerini tek zaman çizgisine birleştirir: her parçanın zamanları önceki parçaların süre toplamı kadar kaydırılır.
    Çıktıda `parcalar` = [{dosya, bas}] (hangi saniyenin hangi kayda ait olduğu)."""
    out = dict(parca_dokumleri[0][1]); out["segmentler"] = []; out["parcalar"] = []
    bas = 0.0
    for dosya, d in parca_dokumleri:
        out["parcalar"].append({"dosya": dosya, "bas": round(bas, 4)})
        for sg in d.get("segmentler") or []:
            y = dict(sg, bas=sg["bas"] + bas, son=sg["son"] + bas)
            if sg.get("kelimeler"):
                y["kelimeler"] = [[a + bas, b + bas, *r] for a, b, *r in sg["kelimeler"]]
            out["segmentler"].append(y)
        bas += float(d.get("sure") or (d["segmentler"][-1]["son"] if d.get("segmentler") else 0))
    out["sure"] = bas
    out["islem_sn"] = sum(float(d.get("islem_sn") or 0) for _, d in parca_dokumleri)
    return out


def hoca_dokum_parcali(k: Path, parcalar: list[Path], log: Path) -> dict:
    """Her parça GPU'da sırayla dökülür (hoca_dokum_gpu.sh), sonra kaydırmalı birleştirilir → hoca_dokum.json."""
    if len(parcalar) == 1:
        return calistir("hoca_dokum", ["sh", str(KOK / "scripts/uretim/ogrenci_drive/hoca_dokum_gpu.sh"), str(parcalar[0]),
                                       str(k / "hoca_dokum.json")], log)
    t0 = time.time(); dokumler = []
    for i, p in enumerate(parcalar, 1):
        hedef = k / f"hoca_dokum_p{i}.json"
        if not hedef.exists():
            r = calistir(f"hoca_dokum_p{i}", ["sh", str(KOK / "scripts/uretim/ogrenci_drive/hoca_dokum_gpu.sh"), str(p), str(hedef)],
                         log.with_name(f"{log.stem}_p{i}.log"))
            if r["kod"] != 0:
                return {"is": "hoca_dokum", "kod": r["kod"], "sn": round(time.time() - t0), "log": r["log"]}
        dokumler.append((p.name, json.loads(hedef.read_text(encoding="utf-8"))))
    (k / "hoca_dokum.json").write_text(json.dumps(dokum_birlestir(dokumler), ensure_ascii=False), encoding="utf-8")
    log.write_text(f"{len(parcalar)} parça birleştirildi: {[p.name for p in parcalar]}\n", encoding="utf-8")
    return {"is": "hoca_dokum", "kod": 0, "sn": round(time.time() - t0), "log": str(log)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--kurul", type=int, default=2)
    ap.add_argument("--mod", choices=("tam", "tasarruf"), default="tam",
                    help="hat kipi (scripts/hat/tam_hat/mod.py); <klasör>/mod.json'a yazılır, sonraki aşamalar oradan okur")
    ap.add_argument("--cpu-is", type=int, default=2, help="eşzamanlı CPU işi (varsayılan 2; RAM 15 GB)")
    a = ap.parse_args()
    k = a.klasor.resolve()
    pdf = k / "orijinal.pdf"
    if not pdf.exists():  # H623: Drive adıyla indirilmiş tek PDF varsa orijinal.pdf adına bağlanır (sonraki aşamalar bu adı bekler)
        adaylar = [p for p in k.glob("*.pdf") if p.name != "ogrenci_not.pdf"]
        if len(adaylar) == 1:
            pdf.symlink_to(adaylar[0].name)
            print(f"hat başı: {adaylar[0].name} → orijinal.pdf")
        else:
            print(f"HATA: {pdf} yok (klasörde {len(adaylar)} aday PDF; tek PDF'i orijinal.pdf adıyla koyun)", file=sys.stderr)
            return 2
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    # Hat başı kapıları (kullanıcı kararı 2026-11-16):
    #  1) Aşama özetleri defterden eskiyse kendiliğinden yenilenir (kural_secici --denetle → uret); alt ajanlar hep güncel okur.
    #  2) Ders kilidi alınır: aynı dersi başka oturum işliyorsa dur (çakışma/ezme önlenir).
    import kural_secici as KS  # noqa: E402
    _bayat = (not KS.CIKIS.exists()) or any(p.stat().st_mtime < KS.DEFTER.stat().st_mtime for p in KS.CIKIS.glob("*.md"))
    if _bayat:
        KS.uret()
        print("hat başı: aşama özetleri yenilendi (defterden eskiydi)")
    import ders_kilit as DK  # noqa: E402
    # Efemer oturum (koşucu dışında, doğrudan çalıştırma): MEDS_OTURUM yoksa kilidi kimse bırakmaz → sonunda biz bırakırız.
    # MEDS_OTURUM varsa sahibi koşucudur; kilidi tüm hat boyunca tutar ve yayında (E6) kendisi bırakır — biz dokunmayız.
    _efemer = "MEDS_OTURUM" not in os.environ
    _oturum = DK._oturum(None)
    if DK.al(a.ders, "E0-hazırlık", _oturum) != 0:
        return 3  # başka oturum bu dersi işliyor
    try:
        return _govde(a, k, pdf)
    finally:
        if _efemer:
            DK.birak(a.ders, _oturum)  # sızıntıyı önle: efemer oturumun kilidini yalnız kendi aldıysak bırak


def _govde(a, k: Path, pdf: Path) -> int:
    from mod import yapilacak
    (k / "mod.json").write_text(json.dumps({"mod": a.mod, "katmanlar": yapilacak(a.mod)}, ensure_ascii=False, indent=1))
    (k / "op").mkdir(exist_ok=True)
    (k / "loglar").mkdir(exist_ok=True)
    L = lambda ad: k / "loglar" / f"{ad}.log"  # noqa: E731
    t0 = time.time()
    sonuc: list[dict] = []
    with ThreadPoolExecutor(1) as gpu, ThreadPoolExecutor(max(1, a.cpu_is)) as cpu:
        isler = []
        parcalar = ses_parcalari(k)
        if parcalar and not (k / "hoca_dokum.json").exists():
            isler.append(gpu.submit(hoca_dokum_parcali, k, parcalar, L("hoca_dokum")))
        sayfa_is = cpu.submit(calistir, "sayfa_metni", cpu_run("metin", sayfa_metni(pdf, k / "sayfalar.json")), L("sayfa_metni"))
        isler.append(cpu.submit(calistir, "sayfa_goruntu",
                                cpu_run("goruntu", ["pdftoppm", "-r", "110", "-png", str(pdf), str(k / "op" / "s")]), L("sayfa_goruntu")))
        if (k / "ogrenci_not.pdf").exists():
            isler.append(cpu.submit(calistir, "ogrenci_not",
                                    cpu_run("not", [PY_CV, str(KOK / "scripts/uretim/kroki/ogrenci_not.py"), "--ders", a.ders, "--not",
                                                    str(k / "ogrenci_not.pdf"), "--asil", str(pdf), "--cikis",
                                                    str(k / "ogrenci_not_isaret.json")]), L("ogrenci_not")))
        sonuc.append(sayfa_is.result())
        if sonuc[-1]["kod"] == 0:  # çıkmış arama sayfa metnine bağlı; sitenin aramasını kullanır (systemd dışı, ağ işi)
            isler.append(cpu.submit(calistir, "cikmis_aday", cikmis_aday(k / "sayfalar.json", a.kurul, k / "cikmis_aday.json"),
                                    L("cikmis_aday")))
            ders_id = re.match(r"k\d+-\d+", a.ders)  # öğrenci önem verisi ders kimliğiyle (k2-19) tutulur
            if ders_id:  # vektörleme CPU servisine gider (bge-m3 :8094); işin kendisi hafif
                isler.append(cpu.submit(calistir, "ogrenci_onem",
                                        [PY, str(KOK / "scripts/uretim/ogrenci_onem/oku.py"), "--ders", ders_id.group(0), "--sayfalar",
                                         str(k / "sayfalar.json"), "--yaz", str(k / "ogrenci_onem.json")], L("ogrenci_onem")))
        sonuc += [f.result() for f in isler]
    # C6/C7 (2026-11-16, LLM yok): döküm varsa slayt başına kırp (değerlendirme HAM dökümü okumaz) + atom adayı iskeleti.
    sonuc.append(calistir("hoca_kirp", [PY, str(KOK / "scripts/hat/tam_hat/hoca_kirp.py"), str(k)], L("hoca_kirp")))
    if (k / "sayfalar.json").exists():
        sonuc.append(calistir("iskelet", [PY, str(KOK / "scripts/hat/tam_hat/iskelet.py"), "uret", str(k), "--ders", a.ders],
                              L("iskelet")))
    durum = {"ders": a.ders, "mod": a.mod, "toplam_sn": round(time.time() - t0), "isler": sonuc}
    (k / "hazirlik_durum.json").write_text(json.dumps(durum, ensure_ascii=False, indent=1))
    for s in sonuc:
        print(f"{'OK ' if s['kod'] == 0 else 'HATA'} {s['is']:<14} {s['sn']:>5} sn  {s['log']}")
    print(f"toplam {durum['toplam_sn']} sn")
    return 0 if all(s["kod"] == 0 for s in sonuc) else 1


if __name__ == "__main__":
    sys.exit(main())
