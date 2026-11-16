#!/usr/bin/env python3
"""Örnek soru tek kapısı — 4 kapıyı (soru_uslup + sik_aciklama + profil_kapisi + kaynak_kapisi) TEK çağrıda toplar.

Neden (kullanıcı kararı 2026-11-16, iterasyon azaltma): ajan bu 4 kapıyı ayrı Bash turlarında koşup her turda büyüyen
bağlamı yeniden işliyor; biri geçince öteki patlıyor → çok tur. Bu kapı hepsini bir kez koşup TÜM sorunları birlikte basar.
sik_aciklama.py'nin CLI'si yok (yalnız `denetle(metin, yer)`), bu yüzden her şık açıklaması tek tek buradan denetlenir.

  python3 scripts/hat/tam_hat/ornek_soru_kapi.py <ornek_sorular.json> --uslup <soru_uslubu.json> --ders "<ders>" --sayfalar <sayfalar.json>
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
import subprocess
import sys
from pathlib import Path

KOK = _kok.MEDS
PY = sys.executable


def _gate(ad: str, cmd: list[str]) -> list[str]:
    r = subprocess.run(cmd, cwd=KOK, capture_output=True, text=True)
    out = (r.stdout + "\n" + r.stderr)
    # Alt kapı çökerse (traceback/exception) çıkış 0 olsa bile HATA say — yoksa "0 HATA" yanılgısı doğar (kullanıcı gözlemi 2026-11-16).
    if "Traceback (most recent call last)" in out or r.returncode < 0:
        son = (out.strip().splitlines() or ["(çıktı yok)"])[-1]
        return [f"[{ad}] alt kapı çöktü (çıkış {r.returncode}): {son[:200]}"]
    if r.returncode == 0:
        return []
    satir = [f"[{ad}] {l.strip()}" for l in out.splitlines() if "HATA" in l or "hata" in l.lower()]
    return satir[:40] or [f"[{ad}] çıkış {r.returncode}: {out.strip()[:200]}"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", type=Path)
    ap.add_argument("--uslup", type=Path, required=True)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--sayfalar", type=Path, required=True)
    a = ap.parse_args()
    sys.path.insert(0, str(KOK / "scripts"))
    from sik_aciklama import denetle as sik_denetle

    print(f"== Örnek soru kapısı · {a.dosya.name} ==")
    hata: list[str] = []
    hata += _gate("soru_uslup", [PY, "scripts/hat/tam_hat/soru_uslup.py", str(a.dosya), "--uslup", str(a.uslup)])
    hata += _gate("profil", [PY, "scripts/uretim/hoca_profili/profil_kapisi.py", str(a.dosya), "--ders", a.ders])
    hata += _gate("kaynak", [PY, "scripts/hat/tam_hat/kaynak_kapisi.py", str(a.dosya), str(a.sayfalar)])

    # sik_aciklama: her kazanım → her soru → her şık açıklaması (CLI yok, fonksiyonla)
    d = json.loads(a.dosya.read_text(encoding="utf-8"))
    sik_n = 0
    for kz in d.get("kazanimlar", []):
        for q in kz.get("sorular", []):
            qid = q.get("id") or f"kz{kz.get('no')}"
            for h, t in (q.get("sik_aciklamalari") or {}).items():
                sik_n += 1
                for issue in (sik_denetle(t or "", f"{qid}.{h}") or []):
                    hata.append(f"[sik_aciklama] {issue}")

    for x in hata[:120]:
        print(x)
    print(f"ÖRNEK SORU KAPISI: {len(hata)} HATA  (şık açıklaması denetlenen: {sik_n})")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
