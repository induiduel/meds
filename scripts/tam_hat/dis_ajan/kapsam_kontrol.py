#!/usr/bin/env python3
"""Kapsam + şekilli sayfa kapısı (dış ajan protokolü §12). LLM yok.

  python3 scripts/tam_hat/dis_ajan/kapsam_kontrol.py <W> <bolum> <sayfalar.json> <ilk>-<son> [--pdf orijinal.pdf]

1) KAPSAM: sayfa metnindeki her cümle/madde, o sayfanın kanıt alıntılarıyla en az %60 kök örtüşmesiyle karşılanmalı.
   Karşılanmayan cümle = anlatılmamış bilgi → HATA. Bilerek atlanıyorsa W/atla_<bolum>.json:
   [{"s":12,"parca":"cümleden ayırt edici bir parça","neden":"en az 10 karakterlik gerekçe"}]  (başlık/sayfa no gibi öğeler otomatik atlanır)
2) ŞEKİL: --pdf verilirse içinde resim bulunan her sayfa için W/sekil_s-NN.json (iki haneli) bulunmalı ve en az bir kayıt taşımalı
   (kayıt biçimi talimat §6). Sayfada resim varken şekil dosyası yoksa HATA: o sayfanın görüntüsünü okumadan geçilemez.
Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import kokler, sayfalar_yukle, yukle  # noqa: E402


def cumleler(metin: str) -> list[str]:
    t = re.sub(r"\n\s*o(?=[A-ZÇĞİÖŞÜ])", "\n• ", metin)  # PDF madde imi 'o'
    # kısa, noktalamasız satır (başlık) kendi bloğu olsun: sonraki cümleyle birleşmesin
    t = re.sub(r"(?m)^[ \t]*([^\n.,;:•]{2,40})[ \t]*\n(?=\s*\S)", lambda m: (m.group(0) + "\n") if len(m.group(1).split()) <= 4 else m.group(0), t)
    t = re.sub(r"[ \t]+", " ", t)
    parcalar = []
    for blok in re.split(r"\n\s*\n|•", t):
        blok = re.sub(r"\s*\n\s*", " ", blok).strip()
        for c in re.split(r"(?<=[.;:])\s+(?=[A-ZÇĞİÖŞÜ0-9])", blok):
            c = c.strip(" \t•o-")
            if len(kokler(c)) >= 3:
                parcalar.append(c)
    return parcalar


def main() -> int:
    if len(sys.argv) < 5:
        print(__doc__)
        return 2
    W, bolum, sayfa_yol, aralik = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), sys.argv[4]
    pdf = Path(sys.argv[sys.argv.index("--pdf") + 1]) if "--pdf" in sys.argv else None
    ilk, son = (int(x) for x in aralik.split("-"))
    sayfalar = sayfalar_yukle(sayfa_yol)
    kanit = yukle(W / f"kanit_{bolum}.json")
    atla = yukle(W / f"atla_{bolum}.json") if (W / f"atla_{bolum}.json").exists() else []
    hata: list[str] = []
    for a in atla:
        if len(str(a.get("neden", ""))) < 10 or not a.get("parca"):
            hata.append(f"[KAPSAM-00] atla kaydı eksik ({a}). Yapılacak: 'parca' ve ≥10 karakterlik 'neden' yaz.")
    for s in range(ilk, son + 1):
        alinti = " ".join(str(k.get("alinti", "")) for k in kanit if isinstance(k, dict) and k.get("s") == s)
        ak = kokler(alinti)
        for c in cumleler(sayfalar.get(str(s), "")):
            ck = kokler(c)
            if any(str(a.get("parca", "")).lower() in c.lower() and a.get("s") == s for a in atla):
                continue
            if len(ck & ak) / len(ck) < 0.60:
                hata.append(f"[KAPSAM-01] s.{s}: anlatılmamış cümle: «{c[:90]}». Yapılacak: bunun için kanıt + cümle ekle; bilerek atlıyorsan atla_{bolum}.json'a gerekçeyle yaz.")
    if pdf:
        r = subprocess.run(["pdfimages", "-list", "-f", str(ilk), "-l", str(son), str(pdf)], capture_output=True, text=True)
        sayfali: dict[int, int] = {}
        for ln in r.stdout.splitlines()[2:]:
            p = ln.split()
            if len(p) > 2 and p[2] == "image":
                sayfali[int(p[0])] = sayfali.get(int(p[0]), 0) + 1
        for s, n in sorted(sayfali.items()):
            f = W / f"sekil_s-{s:02d}.json"
            if not f.exists():
                hata.append(f"[SEKIL-01] s.{s}: sayfada {n} resim var ama {f.name} yok. Yapılacak: op/s-{s:02d}.png'yi kırpıp parça parça oku (kirp.py), şekil dosyasını yaz. Okuyamıyorsan dosyaya {{\"okunamadi\": true, \"neden\": \"…\"}} yaz.")
                continue
            d = json.loads(f.read_text("utf8"))
            if not (isinstance(d, list) and d) and not (isinstance(d, dict) and d.get("okunamadi")):
                hata.append(f"[SEKIL-02] s.{s}: {f.name} boş. Yapılacak: kayıt ekle ya da okunamadi:true + neden yaz.")
    for h in hata:
        print("HATA", h)
    print(f"{'BAŞARISIZ' if hata else 'GEÇTİ'}: sayfa {ilk}-{son}, {len(hata)} hata")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
