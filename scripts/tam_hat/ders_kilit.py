#!/usr/bin/env python3
"""Ders bazlı kilit — aynı dersi iki oturumun aynı anda işleyip birbirinin işini ezmesini önler
(kullanıcı kararı 2026-11-16: 6. partide dört ders iki oturumda işlendi, biri diğerinin 60 soruluk setini ezdi).

Tasarım (2026-11-16 düzeltmesi — eski sürüm yarış/TOCTOU içeriyordu, 8 eşzamanlı `al`'de 2–4 oturum birden alıyordu):
  * **Atomik alım:** kilit dosyası `os.open(O_CREAT|O_EXCL)` ile oluşturulur — aynı anda yalnız BİR oturum oluşturabilir.
    Dosya varsa: bizimse nabız tazelenir; canlı başkasındaysa 1 döner; bayatsa atomik `os.replace` ile devralınır + doğrulanır.
  * **Bayatlık yalnız nabızla** (`son_canli` > KADER_SN). PID canlılığı KULLANILMAZ: CLI süreci yazdıktan hemen sonra ölür,
    pid'e bakmak kilidi anında "bayat" yapardı (eski bug). Uzun işte sahip `canli` ile nabız atar; `yayin` adımında `birak`.
  * **Oturum kimliği** `MEDS_OTURUM` ortam değişkeni (kosucu tek kez üretip tüm adımlara geçirir). Yoksa alıma özel
    rastgele kimlik — başka komut aynı dersi ezemez (korur), ama bırakmak için `MEDS_OTURUM` gerekir (yoksa KADER_SN'de düşer).

  ders_kilit.py al  <key> [--asama E0] [--oturum ID]   → atomik al; başkası tutuyorsa çıkış 1
  ders_kilit.py canli <key> [--oturum ID]              → nabız (son_canli tazele)
  ders_kilit.py birak <key> [--oturum ID]              → bırak (yalnız sahibi)
  ders_kilit.py durum [<key>]                          → kilit(ler) durumu
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import uuid
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KILIT_DIR = KOK / "data" / "ders_kilit"
KADER_SN = 3 * 3600  # 3 saat nabızsız kalan kilit bayat sayılır (sahip `canli` ile uzatır)


def _oturum(verilen: str | None) -> str:
    return verilen or os.environ.get("MEDS_OTURUM") or f"{socket.gethostname()}:{uuid.uuid4().hex[:8]}"


def _bayat(k: dict) -> bool:
    return (time.time() - k.get("son_canli", 0)) > KADER_SN


def _oku(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _govde(key: str, asama: str, oturum: str, baslama: float) -> str:
    return json.dumps({"oturum": oturum, "host": socket.gethostname(), "key": key,
                       "baslama": baslama, "son_canli": time.time(), "asama": asama}, ensure_ascii=False, indent=1)


def al(key: str, asama: str, oturum: str) -> int:
    KILIT_DIR.mkdir(parents=True, exist_ok=True)
    p = KILIT_DIR / f"{key}.json"
    # ATOMİK alım: içeriği temp'e yaz, `os.link` ile bağla. link atomiktir + hedef varsa hata verir; dosya İÇERİKLE
    # birlikte belirir (O_EXCL'in boş-dosya penceresi yok — eski bug: boşken okuyan ikinci oturum devralıyordu).
    tmp = KILIT_DIR / f".{key}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
    tmp.write_text(_govde(key, asama, oturum, time.time()), encoding="utf-8")
    try:
        os.link(tmp, p)
        tmp.unlink(missing_ok=True)
        print(f"kilit alındı: {key} (oturum {oturum}, aşama {asama})")
        return 0
    except FileExistsError:
        tmp.unlink(missing_ok=True)
    mevcut = _oku(p)
    if mevcut and mevcut.get("oturum") == oturum:  # bizim kilidimiz → nabız
        p.write_text(_govde(key, asama, oturum, mevcut.get("baslama", time.time())), encoding="utf-8")
        print(f"kilit tazelendi: {key} (aşama {asama})")
        return 0
    if mevcut and not _bayat(mevcut):  # canlı başkası
        yas = round((time.time() - mevcut.get("son_canli", 0)) / 60)
        print(f"KİLİTLİ: {key} başka oturumda ({mevcut.get('oturum')}, {yas} dk nabız, aşama {mevcut.get('asama')}). "
              f"Bırakması beklenir ya da {KADER_SN // 3600} saat nabızsız kalınca düşer.", file=sys.stderr)
        return 1
    # bayat ya da okunamaz → atomik devral (os.replace) + doğrula
    tmp = KILIT_DIR / f"{key}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
    tmp.write_text(_govde(key, asama, oturum, time.time()), encoding="utf-8")
    os.replace(tmp, p)
    son = _oku(p)
    if son and son.get("oturum") == oturum:
        print(f"bayat kilit devralındı: {key} (oturum {oturum})")
        return 0
    print(f"KİLİTLİ: {key} devralma yarışını başkası kazandı", file=sys.stderr)
    return 1


def canli(key: str, oturum: str) -> int:
    p = KILIT_DIR / f"{key}.json"
    k = _oku(p)
    if not k or k.get("oturum") != oturum:
        print(f"UYARI: {key} kilidi sende değil; nabız atılmadı", file=sys.stderr)
        return 1
    k["son_canli"] = time.time()
    p.write_text(json.dumps(k, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


def birak(key: str, oturum: str) -> int:
    p = KILIT_DIR / f"{key}.json"
    k = _oku(p)
    if k and k.get("oturum") not in (oturum, None):
        print(f"UYARI: {key} kilidi başka oturumda ({k.get('oturum')}); bırakılmadı", file=sys.stderr)
        return 1
    p.unlink(missing_ok=True)
    print(f"kilit bırakıldı: {key}")
    return 0


def durum(key: str | None) -> int:
    if not KILIT_DIR.exists():
        print("kilit yok")
        return 0
    for p in sorted(KILIT_DIR.glob("*.json")):
        if key and p.stem != key:
            continue
        k = _oku(p) or {}
        yas = round((time.time() - k.get("son_canli", 0)) / 60)
        print(f"  {p.stem}: {k.get('oturum')} · aşama {k.get('asama')} · {yas} dk · {'BAYAT' if _bayat(k) else 'canlı'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("eylem", choices=("al", "canli", "birak", "durum"))
    ap.add_argument("key", nargs="?")
    ap.add_argument("--asama", default="?")
    ap.add_argument("--oturum")
    a = ap.parse_args()
    oturum = _oturum(a.oturum)
    if a.eylem == "durum":
        return durum(a.key)
    if not a.key:
        ap.error("key gerekli")
    return {"al": lambda: al(a.key, a.asama, oturum),
            "canli": lambda: canli(a.key, oturum),
            "birak": lambda: birak(a.key, oturum)}[a.eylem]()


if __name__ == "__main__":
    sys.exit(main())
