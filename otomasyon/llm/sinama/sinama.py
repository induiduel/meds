"""Görev sözleşmesi öz-sınaması — model çağırmaz (gorev.py sinama; hat.py --dogrula'ya bağlanabilir).

Her görev için: (1) paket belirlenimci mi (aynı girdi → aynı is_id), (2) iyi örnek cevap derlenip 0 HATA veriyor mu,
(3) gidiş-dönüş: tersine(derle(x)) yeniden derlenince aynı çıktı mı, (4) bilinen kötü cevaplar REDDEDİLİYOR mu
(kapı bozulursa her şeyi geçirmesin — H5 dersi). İş klasörleri geçici dizinde açılır, gerçek işlere dokunmaz.
Örnek cevaplar `ornekler.json`'da (Kurul 1 verisi yalnız OKUNUR).
"""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from .. import cekirdek as c
from .. import yonlendir

ORNEK = json.loads((Path(__file__).with_name("ornekler.json")).read_text(encoding="utf-8"))


def _derle(is_id, cevap):
    return yonlendir.degerlendir(is_id, cevap if isinstance(cevap, str) else json.dumps(cevap, ensure_ascii=False))


VERI = Path(__file__).with_name("veri")


def _gorev_sina(ad: str, o: dict, rapor: list):
    m = c.modul(ad)
    hedef = o["hedef"]
    o = {**o, "ayar": {k: (v.replace("{VERI}", str(VERI)) if isinstance(v, str) else v) for k, v in (o.get("ayar") or {}).items()}}
    if ad == "denetim":
        hedef = next(r["is_id"] for r in rapor if r["gorev"] == "parca_sorusu")   # doğrulanmış işi denetler
    is1 = c.is_ac(ad, hedef, m.hazirla(hedef, o.get("ayar", {})))
    is2 = c.is_ac(ad, hedef, m.hazirla(hedef, o.get("ayar", {})))
    sonuc = {"gorev": ad, "is_id": is1, "hatalar": []}
    if is1 != is2:
        sonuc["hatalar"].append("paket belirlenimci değil (aynı girdi iki farklı iş)")
    _, pj = c.paket(is1)
    if o.get("uretici"):
        o = {**o, **dict(zip(("iyi", "kotu"), m.sinama_ornekleri(pj["meta"])))}
    cikti, h = _derle(is1, o["iyi"])
    if h:
        sonuc["hatalar"] += [f"iyi örnek reddedildi: {x}" for x in h]
    else:
        geri = m.tersine(cikti, pj["esleme"], pj["meta"])
        cikti2, h2 = _derle(is1, geri)
        if h2 or cikti2 != cikti:
            sonuc["hatalar"].append("gidiş-dönüş tutmuyor: tersine(derle(x)) aynı çıktıyı vermiyor")
        yonlendir.kaydet_sonuc(is1, cikti, [])
        c.durum_yaz(is1, durum="dogrulandi", katman="sinama", aile="sinama", model="sinama")
    for kotu in o.get("kotu", []):
        bozuk = copy.deepcopy(o["iyi"])
        for yol, deger in kotu["degistir"]:
            hedef_ = bozuk
            for anahtar in yol[:-1]:
                hedef_ = hedef_[anahtar]
            hedef_[yol[-1]] = deger
        _, hk = _derle(is1, bozuk)
        if not any(kotu["beklenen"] in x for x in hk):
            sonuc["hatalar"].append(f"kötü örnek '{kotu['ad']}' yakalanmadı (beklenen: {kotu['beklenen']!r}; çıkan: {hk[:3]})")
    rapor.append(sonuc)


def main() -> int:
    eski = (c.IS_DIZIN, c.ONBELLEK)
    with tempfile.TemporaryDirectory(prefix="gorev_sinama_") as t:
        c.IS_DIZIN, c.ONBELLEK = Path(t) / "is", Path(t) / "onbellek"
        rapor: list = []
        try:
            # json ayıklayıcı: kod bloğu, önsöz, <think>
            for metin in ['```json\n{"a": 1}\n```', 'Elbette! {"a": 1} umarım işe yarar', '<think>{"x":2}</think>{"a": 1}']:
                if c.json_cikar(metin) != {"a": 1}:
                    rapor.append({"gorev": "json_cikar", "hatalar": [f"ayıklanamadı: {metin!r}"]})
            for ad in ("parca_sorusu", "sik_aciklama", "denetim", "kanit_bagla", "som_sec", "onem_listesi", "cozucu_sorusu"):
                if ad in ORNEK:
                    _gorev_sina(ad, ORNEK[ad], rapor)
        finally:
            c.IS_DIZIN, c.ONBELLEK = eski
    toplam = 0
    for r in rapor:
        toplam += len(r["hatalar"])
        print(f"{r['gorev']:14} {'TAMAM' if not r['hatalar'] else str(len(r['hatalar'])) + ' HATA'}")
        for h in r["hatalar"]:
            print("   -", h)
    print(f"{toplam} HATA")
    return 0 if toplam == 0 else 1
