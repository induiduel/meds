#!/usr/bin/env python3
"""Kanıt doğrulayıcı (dış ajan protokolü §12-1). LLM yok.

  python3 scripts/tam_hat/dis_ajan/kanit_dogrula.py <kanit_bolum.json> <sayfalar.json>

Girdi: liste. Her kayıt: {"id":"k1","bilgi":"kısa düz cümle","s":12,"alinti":"PDF sayfasından birebir parça","gorsel":false}
Denetler: alanlar tam; id benzersiz; alıntı en az 12 karakter; alıntı s−1…s+1 sayfa metninde birebir geçiyor (Türkçe katlama,
boşluk ve satır sonu tirelemesi göz ardı); `bilgi` alıntıdan türüyor (bilgideki sayı alıntıda var, bilgi alıntıyı çelişmiyor).
`belirsiz: true` kayıt anlatımda KULLANILAMAZ (burada HATA). Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import norm, sayilar, yukle, sayfa_metni, sayfalar_yukle  # noqa: E402


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    kanit = yukle(Path(sys.argv[1]))
    sayfalar = sayfalar_yukle(Path(sys.argv[2]))
    hata: list[str] = []
    if not isinstance(kanit, list) or not kanit:
        print("HATA [KANIT-00] kanıt dosyası boş ya da liste değil. Yapılacak: her bilgi için bir kayıt içeren JSON listesi yaz.")
        return 1
    gorulen: set[str] = set()
    for i, k in enumerate(kanit):
        kim = k.get("id", f"#{i}") if isinstance(k, dict) else f"#{i}"
        if not isinstance(k, dict):
            hata.append(f"[KANIT-01] {kim}: kayıt sözlük değil. Yapılacak: {{id,bilgi,s,alinti}} biçimine çevir.")
            continue
        for f in ("id", "bilgi", "s", "alinti"):
            if k.get(f) in (None, "", 0):
                hata.append(f"[KANIT-02] {kim}: '{f}' alanı boş. Yapılacak: alanı doldur; boş bırakma.")
        if k.get("id") in gorulen:
            hata.append(f"[KANIT-03] {kim}: id tekrar ediyor. Yapılacak: her kayda benzersiz id ver (k1, k2…).")
        gorulen.add(k.get("id"))
        if k.get("belirsiz"):
            hata.append(f"[KANIT-04] {kim}: belirsiz=true kayıt kullanılamaz. Yapılacak: kaydı sil; o bilgiyi anlatma ve rapora 'belirsiz' diye yaz.")
            continue
        if not isinstance(k.get("s"), int):
            hata.append(f"[KANIT-05] {kim}: 's' tam sayı sayfa numarası olmalı. Yapılacak: PDF sayfa numarasını sayı olarak yaz.")
            continue
        a = norm(str(k.get("alinti", "")))
        if len(a) < 12:
            hata.append(f"[KANIT-06] {kim}: alıntı çok kısa (<12 karakter). Yapılacak: anlamlı, birebir bir parça kopyala.")
            continue
        if str(k["s"]) not in sayfalar:
            hata.append(f"[KANIT-07] {kim}: sayfa {k['s']} sayfalar.json'da yok. Yapılacak: gerçek sayfa numarasını yaz; sayfa uydurma.")
            continue
        if a not in norm(sayfa_metni(sayfalar, k["s"])):
            hata.append(f"[KANIT-08] {kim}: alıntı sayfa {k['s']}±1 metninde BİREBİR geçmiyor. Yapılacak: sayfa metninden kopyala-yapıştır yap; "
                        f"özetleme/çeviri yok. Şekilden okuduysan etiketi metin katmanında da bul, bulamazsan bu kaydı at.")
            continue
        fazla = sayilar(str(k.get("bilgi", ""))) - sayilar(str(k.get("alinti", "")))
        if fazla:
            hata.append(f"[KANIT-09] {kim}: bilgide {sorted(fazla)} sayısı alıntıda yok. Yapılacak: sayıyı alıntıdan al ya da alıntıyı genişlet.")
    for h in hata:
        print("HATA", h)
    print(f"{'BAŞARISIZ' if hata else 'GEÇTİ'}: {len(kanit)} kayıt, {len(hata)} hata")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
