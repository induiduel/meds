#!/usr/bin/env python3
"""Anlatım tek kapısı — 4 kapıyı (turet + dogrula + metin_denetle + turkce_uslup) TEK çağrıda toplar ve birlikte raporlar.

Neden (kullanıcı kararı 2026-11-16, iterasyon azaltma): ölçüm, alt-ajan tokeninin girdi boyutundan çok ARAÇ-ÇAĞRISI
sayısına bağlı olduğunu gösterdi (aynı ders 12 çağrı 132k / 36 çağrı 181k). Ajan şu an turet→dogrula→metin_denetle→
turkce_uslup'u 4 ayrı Bash turunda koşup her turda büyüyen bağlamı yeniden işliyor. Bu kapı hepsini bir kez koşup TÜM
sorunları birlikte basar → ajan tek düzeltme turunda hepsini giderir.

Ayrıca **kapı bütünlüğü**: `konusma_v2.py --dogrula`, `kaynak.md` (SAYFA damgalı slayt dökümü) yoksa `slayt.satir`
birebir denetimini SESSİZCE atlıyordu (v2d zayıflığı). Bu kapı, `kaynak.md` yoksa `sayfalar.json`'dan üretir → satır
denetimi HER ZAMAN çalışır.

  python3 scripts/hat/tam_hat/anlatim_kapi.py <v2 dizin> --sayfalar <sayfalar.json> --key <ders key>
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
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

KOK = _kok.MEDS
sys.path.insert(0, str(KOK / "scripts" / "uretim" / "sesli_anlatim"))
sys.path.insert(0, str(KOK / "scripts"))


def _kaynak_garanti(dizin: Path, sayfalar: Path) -> str:
    k = dizin / "kaynak.md"
    if k.exists():
        return "vardı"
    if not sayfalar.exists():
        return "YOK (sayfalar.json da yok — satır denetimi atlanır!)"
    d = json.loads(sayfalar.read_text(encoding="utf-8"))
    k.write_text("".join(f"=== SAYFA {n} ===\n{d[str(n)]}\n" for n in sorted(d, key=int)), encoding="utf-8")
    return "üretildi (sayfalar.json'dan)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dizin", type=Path)
    ap.add_argument("--sayfalar", type=Path, required=True)
    ap.add_argument("--key", required=True)
    a = ap.parse_args()
    dizin = a.dizin
    import konusma_v2 as KV
    import metin_denetle as MD
    from turkce_uslup import denetle as uslup_denetle

    print(f"== Anlatım kapısı · {a.key} ==")
    print(f"kaynak.md: {_kaynak_garanti(dizin, a.sayfalar)}")
    hata: list[str] = []

    # 1) türet (metin + sayfalar + çapalar)
    d = json.loads((dizin / "konusma_v2.json").read_text(encoding="utf-8"))
    md, s = KV.turet(d)
    (dizin / "konusma_metni.md").write_text(md, encoding="utf-8")
    (dizin / "konusma_sayfalari.json").write_text(json.dumps(s), encoding="utf-8")
    (dizin / "konusma_capalari.json").write_text(json.dumps(KV.capalar(d), ensure_ascii=False), encoding="utf-8")
    print(f"türet: {len(s)} paragraf")

    # 2) doğrula (kaynak.md GARANTİLİ → satır-birebir denetimi çalışır)
    h = KV.dogrula(d, KV.kaynak_sayfa(dizin), KV.kaynak_metin(dizin))
    hata += [f"[dogrula] {x}" for x in h]
    import iskelet as ISK  # C7: doldurulmamış iskelet yeri (<DOLDUR>, _iskelet) kalmasın
    hata += [f"[iskelet] {x}" for x in ISK.denetle(d)]

    # 3) metin_denetle (kendi ayrıntısını basar; sayısını toplar)
    # Kurul 2+ / modül derslerinde EMA'ya okunuş gider (ses_metin.hazirla: GABA→gaba, NMDA→ne me de a); kısaltma/rakam
    # denetimi yazıma değil okunuşa uygulanmalı (H643 ek 4: `--yazim`siz kapı doğru okunan 110 kısaltmayı HATA sayıyordu).
    sys.path.insert(0, str(KOK / "scripts" / "uretim" / "ses_ortak"))
    from ses_metin import yol_sec
    MD.YAZIM = yol_sec(ders=a.key) == "uzun"  # Kurul 1 ("bitisik") eski davranışta kalır
    print(f"metin_denetle kipi: {'okunuş (--yazim)' if MD.YAZIM else 'yazım'}")
    buf = io.StringIO()
    with redirect_stdout(buf):
        md_n = MD.denetle(dizin / "konusma_metni.md")
    cikti = buf.getvalue().strip()
    if md_n:
        hata += [f"[metin_denetle] {l}" for l in cikti.splitlines() if "HATA" in l or "uyar" in l.lower()][:40] or [f"[metin_denetle] {md_n} hata"]

    # 4) Türkçe üslup
    u = uslup_denetle((dizin / "konusma_metni.md").read_text(encoding="utf-8"), a.key)
    hata += [f"[turkce_uslup] {x}" for x in (u or [])]

    for x in hata[:120]:
        print(x)
    print(f"ANLATIM KAPISI: {len(hata)} HATA  (dogrula {len(h)} · metin {md_n} · uslup {len(u or [])})")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
