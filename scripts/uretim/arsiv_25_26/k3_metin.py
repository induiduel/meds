#!/usr/bin/env python3
"""Kurul 3 arşiv metni: kompakt kaynak biçimi → konusma_v2.json (kimlik, vurgu, çapa otomatik).

Neden: konusma_v2.json'u elle JSON yazmak hem pahalı hem hataya açık (kimlik, sıra, vurgu, çapa). Burada metin
satır satır yazılır; kimlikler/vurgu/çapa bu betikte üretilir. Kapılar değişmez (konusma_v2.dogrula + metin_denetle).

Girdi: <taslak>/metin.tsv
  @@ Bölüm başlığı
  s<N>|<ses cümlesi>|<ekran maddesi>|<slayt satırı>[|<çıkmış id,çıkmış id>][|<şekil tarifi>][|<düzey 1>]
    - N = kaynak.md sayfa numarası (=== SAYFA N ===)
    - slayt satırı: o sayfadan HARFİ HARFİNE kopya; birden çok satır `;;` ile. Çapa yoksa `-`.
    - alanlar sırayla; boş alan = boş bırak (ör. `s5|ses|ekran|-|-|retina şeması`)
  #yorum satırı (yok sayılır)

Çıktı: konusma_v2.json + konusma_metni.md + konusma_sayfalari.json + konusma_capalari.json
  k3_metin.py <key>            → üret + kapıları çalıştır (0 HATA ise çıkış 0)
  k3_metin.py <key> --kuru     → yalnız üret (kapı yok)
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

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"
sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "sesli_anlatim"))


def vurgu_uret(ekran: str) -> list[dict]:
    """Ekrandaki **kalın** ifadeleri terim vurgusu yap (metin ekranda var, kural sağlanır)."""
    out = []
    for m in re.finditer(r"\*\*([^*]+)\*\*", ekran):
        t = m.group(1).strip()
        if t:
            out.append({"metin": t, "tur": "terim"})
    return out


def yaz(key: str) -> int:
    taslak = DB / "taslak" / key
    kaynak_yol = taslak / "metin.tsv"
    if not kaynak_yol.exists():
        print(f"HATA: {kaynak_yol} yok", file=sys.stderr)
        return 2
    baglam = json.loads((taslak / "baglam.json").read_text(encoding="utf-8"))
    did = re.match(r"^(?:y25-)?(k\d-\d{2})", key).group(1)
    baslik = baglam["konu"]
    bolumler: list[dict] = []
    b = p = c_n = 0
    p_tum = 0    # paragraf numarası ders içinde tekil (bölümle sıfırlanmaz: kimlik çakışmasın)
    for no, satir in enumerate(kaynak_yol.read_text(encoding="utf-8").splitlines(), 1):
        s = satir.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("@@"):
            b += 1
            p = 0
            bolumler.append({"id": f"{did}-b{b:02d}", "baslik": s[2:].strip(), "paragraflar": []})
            continue
        if "|" not in s:
            print(f"HATA satır {no}: biçim (s<N>|ses|ekran|satır): {s[:60]}", file=sys.stderr)
            return 2
        alan = s.split("|")
        if len(alan) < 4:
            print(f"HATA satır {no}: en az 4 alan gerekli: {s[:60]}", file=sys.stderr)
            return 2
        m = re.fullmatch(r"s(\d+)", alan[0].strip())
        if not m:
            print(f"HATA satır {no}: sayfa alanı 's<N>' değil: {alan[0][:20]}", file=sys.stderr)
            return 2
        sayfa = int(m.group(1))
        ses, ekran, satirlar = alan[1].strip(), alan[2].strip(), alan[3].strip()
        cikmis = [x.strip() for x in (alan[4].strip() if len(alan) > 4 else "").split(",") if x.strip()]
        sekil = (alan[5].strip() if len(alan) > 5 else "") or None
        duzey = int(alan[6]) if len(alan) > 6 and alan[6].strip().isdigit() else 0
        if not bolumler:
            b += 1
            bolumler.append({"id": f"{did}-b{b:02d}", "baslik": baslik, "paragraflar": []})
        # paragraf: her 4–6 cümlede yeni paragraf (EMA parça sınırı ve oynatıcı bölmesi için)
        son = bolumler[-1]["paragraflar"][-1] if bolumler[-1]["paragraflar"] else None
        if son is None or son["sayfa"] != sayfa or len(son["cumleler"]) >= 5:
            p += 1
            p_tum += 1
            son = {"id": f"{did}-p{p_tum:03d}", "sayfa": sayfa, "cumleler": []}
            bolumler[-1]["paragraflar"].append(son)
        c_n += 1
        sl = None
        if (satirlar and satirlar != "-") or sekil:
            sl = {"sayfa": sayfa}
            if satirlar and satirlar != "-":
                sl["satir"] = [x.strip() for x in satirlar.split(";;") if x.strip()]
            else:
                sl["satir"] = []
            if sekil:
                sl["sekil"] = sekil
        cu = {
            "id": f"{did}-c{c_n:04d}",
            "ses": ses,
            "ekran": ekran,
            "duzey": duzey,
            "slayt": sl,
        }
        vg = vurgu_uret(ekran)
        if cikmis:
            cu["cikmis"] = cikmis
            vg.append({"metin": (re.findall(r"\*\*([^*]+)\*\*", ekran) or [" ".join(ekran.replace("**", "").split()[:3])])[0], "tur": "cikmis"})
        if vg:
            cu["vurgu"] = vg
        son["cumleler"].append(cu)
    v2 = {"surum": 2, "ders_id": did, "anahtar": key, "baslik": baslik, "donem": "2025-2026", "bolumler": bolumler}
    (taslak / "konusma_v2.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    import konusma_v2 as KV
    md, sayfalar = KV.turet(v2)
    (taslak / "konusma_metni.md").write_text(md, encoding="utf-8")
    (taslak / "konusma_sayfalari.json").write_text(json.dumps(sayfalar), encoding="utf-8")
    (taslak / "konusma_capalari.json").write_text(json.dumps(KV.capalar(v2), ensure_ascii=False), encoding="utf-8")
    print(f"[{key}] {len(bolumler)} bölüm · {c_n} cümle · {len(md.split())} kelime")
    return 0


def kapilar(key: str) -> int:
    taslak = DB / "taslak" / key
    import konusma_v2 as KV
    v2 = json.loads((taslak / "konusma_v2.json").read_text(encoding="utf-8"))
    h = KV.dogrula(v2, KV.kaynak_sayfa(taslak), KV.kaynak_metin(taslak))
    for x in h[:40]:
        print("HATA", x)
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "uretim" / "sesli_anlatim" / "metin_denetle.py"),
                        str(taslak / "konusma_metni.md")], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[-2500:])
    sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "arsiv_25_26"))
    import k3_yayinla as Y
    kh = Y.kapsam(taslak, v2)
    for x in kh:
        print("KAPSAM", x)
    return 0 if not h and r.returncode == 0 and not kh else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    rc = yaz(a.key)
    if rc == 0 and not a.kuru:
        rc = kapilar(a.key)
    raise SystemExit(rc)
