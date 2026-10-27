#!/usr/bin/env python3
"""Tam içerik hattı · hazırlık evresi: birbirinden bağımsız girdi işlerini kaynak tavanlı PARALEL yürütür (LLM yok).

  python3 scripts/tam_hat/hazirlik.py <ders klasörü> --ders <key> [--kurul 2] [--cpu-is 2]

Klasörde beklenenler (olanlar işlenir, olmayan iş atlanır — eksiklik durdurmaz, kural 22):
  orijinal.pdf (zorunlu) · ogrenci_not.pdf · hoca_ses.m4a
İşler ve kaynak payı (makine 15 GB RAM / 20 çekirdek; Claude oturumları korunur):
  GPU (tek iş):  hoca dökümü → hoca_dokum.json            hoca_dokum_gpu.sh (AGENTS §10 altıncı istisna, ≤2500 MHz)
  CPU (en çok --cpu-is eşzamanlı, her biri CPUQuota=200% MemoryMax=2G):
     sayfa metni   → sayfalar.json {"1": "...", ...}       pdftotext, sayfa sayfa (kaynak kapısının temeli)
     sayfa görüntü → op/s-NNN.png                          pdftoppm 110 dpi (alt ajanlar görüntüyü açarak okur — H111)
     öğrenci notu  → ogrenci_not_isaret.json               kroki/ogrenci_not.py
     çıkmış aday   → cikmis_aday.json                      ders_isci/isle.py::cikmis_adaylari (sitenin araması; elle doğrulanır — H79)
Her işin süresi ve sonucu <klasör>/hazirlik_durum.json'a yazılır; sonraki evre (anlatım, deste, soru) beklemeden başlar,
yalnız hoca vurgusu gerektiren adım döküm bitince eklenir.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]  # meds/
PY = sys.executable
PY_CV = str(KOK / ".venv-ocr/bin/python")  # cv2 + pymupdf bu ortamda
API = os.environ.get("MEDS_ISCI_API", "http://127.0.0.1:3000")  # yerel site araması (benzer soru)


def cpu_run(ad: str, komut: list[str]) -> list[str]:
    return ["systemd-run", "--user", "--wait", "--collect", "--quiet", "--pipe", f"--unit=meds-hazirlik-{ad}-{int(time.time())}",
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
           f"sys.path.insert(0,{str(KOK / 'scripts/ders_isci')!r})\n"
           "from isle import cikmis_adaylari\n"
           "d=json.load(open(sys.argv[1]))\n"
           "metin=''.join(f'=== SAYFA {k}\\n{v}\\n' for k,v in d.items())\n"
           "a=cikmis_adaylari(metin,int(sys.argv[2]))\n"
           "json.dump(a,open(sys.argv[3],'w'),ensure_ascii=False,indent=1);print(len(a),'aday')\n")
    return ["env", f"MEDS_ISCI_API={API}", PY, "-c", kod, str(sayfalar), str(kurul), str(cikti)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--kurul", type=int, default=2)
    ap.add_argument("--cpu-is", type=int, default=2, help="eşzamanlı CPU işi (varsayılan 2; RAM 15 GB)")
    a = ap.parse_args()
    k = a.klasor.resolve()
    pdf = k / "orijinal.pdf"
    if not pdf.exists():
        print(f"HATA: {pdf} yok", file=sys.stderr)
        return 2
    (k / "op").mkdir(exist_ok=True)
    (k / "loglar").mkdir(exist_ok=True)
    L = lambda ad: k / "loglar" / f"{ad}.log"  # noqa: E731
    t0 = time.time()
    sonuc: list[dict] = []
    with ThreadPoolExecutor(1) as gpu, ThreadPoolExecutor(max(1, a.cpu_is)) as cpu:
        isler = []
        ses = k / "hoca_ses.m4a"
        if ses.exists() and not (k / "hoca_dokum.json").exists():
            isler.append(gpu.submit(calistir, "hoca_dokum",
                                    ["sh", str(KOK / "scripts/ogrenci_drive/hoca_dokum_gpu.sh"), str(ses), str(k / "hoca_dokum.json")],
                                    L("hoca_dokum")))
        sayfa_is = cpu.submit(calistir, "sayfa_metni", cpu_run("metin", sayfa_metni(pdf, k / "sayfalar.json")), L("sayfa_metni"))
        isler.append(cpu.submit(calistir, "sayfa_goruntu",
                                cpu_run("goruntu", ["pdftoppm", "-r", "110", "-png", str(pdf), str(k / "op" / "s")]), L("sayfa_goruntu")))
        if (k / "ogrenci_not.pdf").exists():
            isler.append(cpu.submit(calistir, "ogrenci_not",
                                    cpu_run("not", [PY_CV, str(KOK / "scripts/kroki/ogrenci_not.py"), "--ders", a.ders, "--not",
                                                    str(k / "ogrenci_not.pdf"), "--asil", str(pdf), "--cikis",
                                                    str(k / "ogrenci_not_isaret.json")]), L("ogrenci_not")))
        sonuc.append(sayfa_is.result())
        if sonuc[-1]["kod"] == 0:  # çıkmış arama sayfa metnine bağlı; sitenin aramasını kullanır (systemd dışı, ağ işi)
            isler.append(cpu.submit(calistir, "cikmis_aday", cikmis_aday(k / "sayfalar.json", a.kurul, k / "cikmis_aday.json"),
                                    L("cikmis_aday")))
        sonuc += [f.result() for f in isler]
    durum = {"ders": a.ders, "toplam_sn": round(time.time() - t0), "isler": sonuc}
    (k / "hazirlik_durum.json").write_text(json.dumps(durum, ensure_ascii=False, indent=1))
    for s in sonuc:
        print(f"{'OK ' if s['kod'] == 0 else 'HATA'} {s['is']:<14} {s['sn']:>5} sn  {s['log']}")
    print(f"toplam {durum['toplam_sn']} sn")
    return 0 if all(s["kod"] == 0 for s in sonuc) else 1


if __name__ == "__main__":
    sys.exit(main())
