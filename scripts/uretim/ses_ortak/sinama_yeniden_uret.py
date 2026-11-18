#!/usr/bin/env python3
"""yeniden_uret.py birim sınaması — GPU'suz, sahte üretici, geçici dizinde (gerçek data/meds_temp'e dokunmaz).

Senaryo: 5 klip; sahte kapı 2'sini reddeder → takas yalnız 3'ünde, reddedilen 2'nin eski dosyası/kaydı yerinde; yeniden
çalıştırınca 0 üretim; yarıda kesilen takas (hazır dosya taşınmış, kayıt yazılmamış) tamamlanır; geri-al eskileri geri koyar.
Kullanım: python3 scripts/uretim/ses_ortak/sinama_yeniden_uret.py   (0 HATA → çıkış 0)
"""
from __future__ import annotations

import json
import sys
import tempfile
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yeniden_uret as Y  # noqa: E402
import ses_klip as SK  # noqa: E402

HATA = []


def bak(kosul, mesaj):
    print(("  tamam " if kosul else "  HATA  ") + mesaj)
    if not kosul:
        HATA.append(mesaj)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="yeniden_sinama_"))
    data = tmp / "data"
    Y.IS, Y.TEMP = tmp / "is", tmp
    Y.DURUM, Y.HAZIR, Y.ESKI, Y.LOG = Y.IS / "durum.jsonl", Y.IS / "hazir", Y.IS / "eski", tmp / "log"
    SK.DATA = data
    d = data / "sahte_cozucu/ses/01"
    d.mkdir(parents=True)
    kayit = {}
    rows = []
    for i in range(5):
        (d / f"q-{i}.mp3").write_bytes(b"ESKI%d" % i)
        kayit[f"q-{i}"] = {"h": f"h{i}", "sure": 1.0, "zaman": [[0, 1]]}
        rows.append({"modul": "sahte_cozucu", "klasor": "01", "klip": f"q-{i}", "cumleler": [f"Cümle {i}."],
                     "okunus": {f"Cümle {i}.": f"Cümle {i}."}})
    (d / "kayit.json").write_text(json.dumps(kayit))
    uretim = []

    def sahte_uretici(r):
        uretim.append(r["klip"])
        return b"YENI-" + r["klip"].encode(), [[0, 2]], 2.0, []

    red = {"q-1", "q-3"}

    def sahte_kapi(yeni, eski, motor):
        return "sahte ret" if yeni.stem in red else None

    # 1. tur
    Y.parti_uret("sahte_cozucu", rows, sahte_uretici)
    s = Y.kapi_ve_takas("sahte_cozucu", rows, kapi=sahte_kapi)
    k = json.loads((d / "kayit.json").read_text())
    bak(len(uretim) == 5, f"5 klip üretildi ({len(uretim)})")
    bak(s == {"gecti": 3, "red": 2}, f"kapı: 3 geçti 2 red ({s})")
    bak(all((d / f"q-{i}.mp3").read_bytes() == b"YENI-q-%d" % i for i in (0, 2, 4)), "geçen 3 klip yeni dosya")
    bak(all((d / f"q-{i}.mp3").read_bytes() == b"ESKI%d" % i for i in (1, 3)), "reddedilen 2 klip eski dosya yerinde")
    bak(all(k[f"q-{i}"]["sure"] == 2.0 and k[f"q-{i}"]["h"] == f"h{i}" for i in (0, 2, 4)), "kayıt: sure güncel, h korunmuş")
    bak(all(k[f"q-{i}"]["sure"] == 1.0 for i in (1, 3)), "kayıt: reddedilenler değişmedi")
    bak(all((Y.ESKI / "sahte_cozucu/sahte_cozucu/ses/01" / f"q-{i}.mp3").read_bytes() == b"ESKI%d" % i for i in (0, 2, 4)),
        "eski 3 klip yedekte")
    bak(not any(Y.HAZIR.rglob("*.mp3")), "hazırlık dizini boşaldı")
    df = Y.defter_oku()
    bak(sorted(x["durum"] for x in df.values()) == ["kapidan_gecti"] * 3 + ["reddedildi"] * 2, "defter durumları")
    # 2. tur: sürdürme
    uretim.clear()
    b = Y.bekleyenler(rows, Y.defter_oku(), False)
    Y.parti_uret("sahte_cozucu", b, sahte_uretici)
    bak(not b and not uretim, f"yeniden çalıştırınca 0 iş ({len(b)} bekleyen)")
    b2 = Y.bekleyenler(rows, Y.defter_oku(), True)
    bak(sorted(r["klip"] for r in b2) == ["q-1", "q-3"], "--yeniden-dene yalnız reddedilen 2'yi alır")
    # 3. yarım takas: q-1 yeniden üretilip taşınmış ama kayıt/defter yazılmamış gibi
    red.clear()
    Y.parti_uret("sahte_cozucu", [rows[1]], sahte_uretici)
    hy = Y.hazir_yol(rows[1])
    Y.ESKI.joinpath("sahte_cozucu/sahte_cozucu/ses/01").mkdir(parents=True, exist_ok=True)
    (Y.ESKI / "sahte_cozucu/sahte_cozucu/ses/01/q-1.mp3").write_bytes(b"ESKI1")
    Y.defter_yaz(anahtar=Y.anahtar(rows[1]), kok="sahte_cozucu", durum="uretildi", eski_kayit=kayit["q-1"])
    hy.replace(d / "q-1.mp3")
    s = Y.kapi_ve_takas("sahte_cozucu", rows, kapi=sahte_kapi)
    k = json.loads((d / "kayit.json").read_text())
    bak(s["gecti"] == 1 and k["q-1"]["sure"] == 2.0, f"yarım takas tamamlandı ({s}, sure {k['q-1']['sure']})")
    # 4. geri-al
    Y.k_geri_al(types.SimpleNamespace(kok=["sahte_cozucu"]))
    k = json.loads((d / "kayit.json").read_text())
    bak(all((d / f"q-{i}.mp3").read_bytes() == b"ESKI%d" % i for i in range(5)), "geri-al: 5 klibin hepsi eski dosya")
    bak(all(k[f"q-{i}"]["sure"] == 1.0 for i in range(5)), "geri-al: kayıt eski hâlinde")
    bak(not Y.bekleyenler(rows, Y.defter_oku(), False), "geri alınanlar varsayılan koşuda yeniden üretilmez")
    print(f"{'0 HATA' if not HATA else str(len(HATA)) + ' HATA'}  ({tmp})")
    return 1 if HATA else 0


if __name__ == "__main__":
    sys.exit(main())
