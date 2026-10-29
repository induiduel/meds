#!/usr/bin/env python3
"""Tek komutla bölüm kapısı (dış ajan protokolü §12-3). Her bölüm bitince ÇALIŞTIR; HATA varsa sonraki bölüme geçme.

  python3 scripts/tam_hat/dis_ajan/bolum_kontrol.py <W> <bolum> <sayfalar.json>
Okur: W/kanit_<bolum>.json ve W/uretim_<bolum>.json. Sırayla kanit_dogrula, kanit_tutarlilik, kapsam_kontrol çalıştırır.
  python3 scripts/tam_hat/dis_ajan/bolum_kontrol.py <W> <bolum> <sayfalar.json> <ilk>-<son> <orijinal.pdf>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

D = Path(__file__).resolve().parent


def main() -> int:
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    W, bolum, sayfalar, aralik, pdf = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    kanit, uretim = W / f"kanit_{bolum}.json", W / f"uretim_{bolum}.json"
    for f in (kanit, uretim, Path(sayfalar), Path(pdf)):
        if not f.exists():
            print(f"HATA dosya yok: {f}. Yapılacak: önce kanıtı, sonra üretimi yaz (kanıt önce!).")
            return 1
    kod = 0
    for ad, args in (("KANIT", ["kanit_dogrula.py", str(kanit), sayfalar]), ("TUTARLILIK", ["kanit_tutarlilik.py", str(uretim), str(kanit)]), ("KAPSAM", ["kapsam_kontrol.py", str(W), bolum, sayfalar, aralik, "--pdf", pdf])):
        print(f"--- {ad} ---")
        r = subprocess.run([sys.executable, "-I", str(D / args[0]), *args[1:]], capture_output=True, text=True)
        print(r.stdout.rstrip())
        if r.returncode:
            kod = 1
            if ad == "KANIT":
                print("DUR: kanıt hatalıyken tutarlılık anlamsız. Önce kanıtı düzelt.")
                break
    # METİN: bölüm cümlelerini paragraflara (p) dizip sitenin gerçek ses denetimini (--yazim) çalıştır
    import json, tempfile
    U = json.loads(uretim.read_text("utf8"))
    par: dict = {}
    for u in U:
        par.setdefault(u.get("p"), []).append(str(u.get("metin", "")))
    md = "# Bölüm denetimi\n\n@@ " + bolum + "\n\n" + "\n\n".join(" ".join(v) for v in par.values()) + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf8") as t:
        t.write(md)
    print("--- METİN (metin_denetle, sitenin gerçek ses denetimi) ---")
    r = subprocess.run([sys.executable, "-I", str(D.parents[1] / "sesli_anlatim" / "metin_denetle.py"), "--yazim", t.name], capture_output=True, text=True)
    print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "HATA" in l or "Traceback" in l or "Error" in l) or "GEÇTİ: 0 HATA")
    if r.returncode:
        kod = 1
    print("SONUÇ:", "BAŞARISIZ — yalnız yukarıdaki kimlikleri düzelt, sonra bu komutu yeniden çalıştır." if kod else "GEÇTİ — sonraki bölüme geçebilirsin.")
    return kod


if __name__ == "__main__":
    sys.exit(main())
