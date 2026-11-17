#!/usr/bin/env python3
"""Kurul 3 arşivi: bir ders bitince canlıya dağıt (kullanıcı talimatı 2026-11-17).

Kural 13: her dağıtımda `guncelleme_notu.json` onem+1 + başlık/maddeler; kural 15: kod dağıtımının TEK yolu
`deploy/oracle/dagit.sh`. Bu betik yalnız Kurul 3 arşiv yollarını commit'ler (başka oturumların yarım işine dokunmaz);
ses/PDF/medspak git dışıdır, dagit.sh bunları rsync ile taşır.

  python3 scripts/uretim/arsiv_25_26/k3_dagit.py <key> [<key>…]
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import json
import subprocess
import sys
from pathlib import Path

MEDS = _kok.MEDS
ROOT = MEDS.parent
DB = ROOT / "meds_database_25_26"
SA = MEDS / "data" / "arsiv_25_26" / "sesli_anlatim"
GN = MEDS / "guncelleme_notu.json"


def calistir(komut: list[str], ad: str, **kw) -> tuple[int, str]:
    r = subprocess.run(komut, capture_output=True, text=True, cwd=MEDS, **kw)
    cikti = ((r.stdout or "") + (r.stderr or "")).strip()
    print(f"  {ad}: çıkış {r.returncode}", flush=True)
    if r.returncode != 0 or ad.startswith("dagit"):
        for x in cikti.splitlines()[-12:]:
            print("    " + x[:170], flush=True)
    return r.returncode, cikti


def main() -> int:
    anahtarlar = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not anahtarlar:
        print(__doc__, file=sys.stderr)
        return 2
    tablo = json.loads((DB / "kurul3_eslesme.json").read_text(encoding="utf-8"))
    eksik = [k for k in anahtarlar if k not in tablo]
    if eksik:
        print(f"HATA: bilinmeyen ders: {eksik}", file=sys.stderr)
        return 2

    # 1) yalnız bu derslerin arşiv dosyaları (git dışı ses/pdf/medspak hariç)
    yollar = []
    for k in anahtarlar:
        for alt in ("metin", "v2", "vurgu", "hizalama", "capa", "isaret", "cizim", "cikmis_konum",
                    "cumle_zaman", "kelime_zaman", "terim", "kisaltma"):
            p = SA / alt / f"{k}.json"
            pm = SA / alt / f"{k}.md"
            for x in (p, pm):
                if x.exists():
                    yollar.append(str(x.relative_to(MEDS)))
        g = MEDS / "data" / "arsiv_25_26" / "gunluk" / f"{k}.json"
        if g.exists():
            yollar.append(str(g.relative_to(MEDS)))
        g2 = MEDS / "data" / "sesli_anlatim" / "gunluk" / f"{k}.json"
        if g2.exists():
            yollar.append(str(g2.relative_to(MEDS)))
    yollar.append("data/arsiv_25_26/sesli_anlatim/dersler.json")
    yollar += ["scripts/uretim/arsiv_25_26", "docs/ARSIV_25_26_KURUL3.md",
               # hata defteri bu hattın çözdüğü kök nedenlerle güncellenir; kural kapısı (D4) bunları ister
               "docs/hatalar/ses.md", "docs/hatalar/_dizin.json",
               "docs/KURUL2_YAPILMAYACAK_HATALAR.md", "docs/asama_kurallari"]

    rc, _ = calistir(["git", "add", "--"] + yollar, "git add")
    if rc != 0:
        return 1

    # 2) güncelleme notu (kural 13: onem +1, Türkçe başlık/maddeler)
    nott = json.loads(GN.read_text(encoding="utf-8"))
    nott["onem"] = int(nott.get("onem") or 0) + 1
    basliklar = [tablo[k]["baslik"] for k in anahtarlar]
    nott["baslik"] = "2025-2026 Kurul 3 arşivi: yeni sesli dersler"
    nott["maddeler"] = [
        "2025-2026 Dönem 3 Kurul 3 arşivine yeni sesli dersler eklendi; slayt takibi cümle cümle çalışır.",
        "Eklenen dersler: " + ", ".join(basliklar[:6]) + ("…" if len(basliklar) > 6 else "") + ".",
        "Bu derslerde Öğren destesi ve canlı çizim üretilmedi; sesli anlatım, PDF metin takibi, terim/kısaltma ve çıkmış kartı hazır.",
    ]
    GN.write_text(json.dumps(nott, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    calistir(["git", "add", "--", "guncelleme_notu.json"], "git add not")

    mesaj = "Arşiv 25-26 Kurul 3: " + ", ".join(k.split("-", 3)[-1] for k in anahtarlar[:4]) + \
            (f" (+{len(anahtarlar) - 4})" if len(anahtarlar) > 4 else "")
    rc, cikti = calistir(["git", "commit", "-m", mesaj], "git commit")
    if rc != 0 and "nothing to commit" not in cikti:
        return 1

    # 3) push (başka oturum önce gönderdiyse yeniden dene)
    for i in range(3):
        rc, cikti = calistir(["git", "push", "origin", "HEAD:main"], f"git push ({i + 1})")
        if rc == 0:
            break
    else:
        print("  UYARI: push yapılamadı — dağıtım origin/main'deki sürümü alır", flush=True)

    # 4) canlıya dağıtım (tek yol)
    rc, _ = calistir(["bash", str(MEDS / "deploy" / "oracle" / "dagit.sh")], "dagit")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
