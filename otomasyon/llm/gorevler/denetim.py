"""Görev `denetim` — başka bir görevin doğrulanmış çıktısının bağımsız denetimi (yazar ≠ denetçi, §1.2).

Hedef: denetlenecek işin `is_id`'si (durumu `dogrulandi`) ya da `toplu:<ad>` + `ayar.isler` (ders başına toplu denetim,
D etiketleri; çıktı `{isler: {D1: {karar, bulgular}}}`). Paket: o işin GİRDİ'si + çıktısının okunur biçimi (görev
modülünün `ozet`i). Denetçi, yazarın model ailesinden FARKLI bir aileden seçilir (`haric_aile`).
Çıktı: `{karar: gecer|duzelt, bulgular: [{yer, tur, aciklama, oneri}]}`. Uygulama: hedef işe `denetim.json` yazar ve
durumuna `denetim` alanını ekler; `duzelt` kararlı iş yayına (uygula) geçemez.
"""
from __future__ import annotations

import json
from pathlib import Path

from .. import cekirdek as c

OGRENCI_METNI = False   # çıktı iç veri (kısa etiket taşır); ortak etiket sızıntısı kapısı uygulanmaz
KURALLAR = ["kaynak_sadakati", "cikti_disiplini"]
TURLER = ("tibbi_hata", "kaynak_disi", "celiski", "cevap_hatali", "belirsiz_soru", "uslup", "bicim", "diger")


EK_KURALLAR = [
    "Zevk farkı ya da küçük üslup tercihi bulgu değildir; öğrenciyi yanıltacak ya da yanlış öğretecek şeyler bulgudur.",
    "Girdide olmayan ama tıben doğru bilgi 'kaynak_disi' olarak bildirilir; tıben yanlış bilgi 'tibbi_hata'.",
    "Her bulgu tek bir yere işaret eder ve önerisini içerir.",
    "`ses`, `kok_ses`, `secenek_ses` alanları seslendirme için OKUNUŞ yazımıdır: kısaltmalar harf harf ('HIV' → "
    "'ha i ve', 'DNA' → 'dee nee aa'), sayılar yazıyla, büyük harf ve noktalama sade. Bu bilinçli biçimdir, bulgu değildir; "
    "yalnız okunuş yanlış bir terime ya da anlama götürüyorsa bildir.",
]
AMAC = ("Başka bir yazarın ürettiği içeriği bağımsız denetçi olarak incele. Tıbbi doğruluk, girdideki ders metnine sadakat, "
        "tek doğru cevap, çelişki ve anlaşılırlık açısından YALNIZ GERÇEK sorunları bildir. Sorun yoksa karar 'gecer' ve "
        "bulgular boş dizi.")
ORNEK = {"karar": "duzelt", "bulgular": [{"yer": "2. soru, B şıkkı açıklaması", "tur": "tibbi_hata",
                                          "aciklama": "Neyin neden yanlış olduğu, girdideki dayanağıyla.", "oneri": "Doğru ifade."}]}
TOPLU_SINIR = 60000   # toplu paket girdisi (karakter): ajanların bağlamı geniş; aşan işler sonraki pakete


def is_goster(hedef: str) -> tuple[str, str, dict, dict]:
    """Denetlenecek işin (girdi, çıktı özeti, paket, durum). Kısmi kabulde düşen ögeler sonraki partide işlendiği için
    denetçi yalnız kabul edilen ögelerin girdisini görür (yoksa "Q3 çıktıda yok" yanlış bulgusu, 2026-10-24)."""
    d = c.durum(hedef)
    if d.get("durum") not in ("dogrulandi", "uygulandi"):
        raise SystemExit(f"denetim için hedef iş doğrulanmış olmalı: {hedef} ({d.get('durum')})")
    _, pj = c.paket(hedef)
    m = c.modul(pj["gorev"])
    cikti = c.oku(c.is_klasoru(hedef) / "cikti.json")
    goster = m.ozet(cikti, pj["esleme"], pj["meta"])
    girdi = pj["girdi_metni"]
    oge = getattr(m, "OGE", None)
    if oge and isinstance(cikti.get(oge[0]), list) and cikti[oge[0]] and "_etiket" in cikti[oge[0]][0]:
        from .. import yonlendir
        girdi = yonlendir._girdi_suz(girdi, {x["_etiket"] for x in cikti[oge[0]]})
    return girdi, goster, pj, d


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    if hedef.startswith("toplu:"):
        return _toplu_hazirla(hedef, ayar or {})
    girdi, goster, pj, d = is_goster(hedef)
    return {
        "amac": AMAC,
        "kurallar": KURALLAR,
        "ek_kurallar": EK_KURALLAR,
        "girdi": f"## Yazara verilen girdi\n{girdi}\n\n## Yazarın çıktısı\n{goster}",
        "cikti_bicimi": ("Yalnız şu JSON; tur şunlardan biri: " + ", ".join(TURLER) + "\n"
                         + json.dumps(ORNEK, ensure_ascii=False, indent=1)),
        "denetim_listesi": ["karar gecer ya da duzelt", "duzelt ise en az bir bulgu", "her bulguda yer, tur, aciklama, oneri"],
        "esleme": {},
        "meta": {"hedef_is": hedef, "hedef_gorev": pj["gorev"], "haric_aile": d.get("aile"),
                 "kurul": pj["meta"].get("kurul")},
    }


def _toplu_hazirla(hedef: str, ayar: dict) -> dict:
    """Ders başına toplu denetim (2026-10-24): `ayar.isler` = aynı yazar ajanından gelen doğrulanmış işler. Her iş D1, D2 …
    etiketiyle kendi girdisi ve çıktısıyla gelir; denetçi her biri için ayrı karar + bulgu yazar (16 çağrı → birkaç çağrı)."""
    isler = ayar.get("isler") or []
    if not isler:
        raise SystemExit("toplu denetim: ayar.isler boş")
    et = c.Etiketler()
    bloklar, aile, gorevler = [], set(), {}
    for is_id in isler:
        girdi, goster, pj, d = is_goster(is_id)
        D = et.ekle("D", is_id)
        aile.add(d.get("aile")); gorevler[is_id] = pj["gorev"]
        bloklar.append(f"### {D} — {pj['gorev']}\n#### Yazara verilen girdi\n{girdi}\n\n#### Yazarın çıktısı\n{goster}")
    ornek = {"isler": {"D1": ORNEK, "D2": {"karar": "gecer", "bulgular": []}}}
    return {
        "amac": AMAC + " Aşağıda birden çok iş var (D1, D2 …); her birini AYRI denetle, bulguyu ait olduğu işe yaz.",
        "kurallar": KURALLAR,
        "ek_kurallar": EK_KURALLAR + ["Bir işin girdisi yalnız o işin çıktısı için dayanaktır; işler arasında karşılaştırma "
                                      "yapma, her D etiketi için bir kayıt yaz."],
        "girdi": "\n\n".join(bloklar),
        "cikti_bicimi": ("Yalnız şu JSON (girdideki her D için bir kayıt); tur şunlardan biri: " + ", ".join(TURLER) + "\n"
                         + json.dumps(ornek, ensure_ascii=False, indent=1)),
        "denetim_listesi": ["her D için kayıt", "karar gecer ya da duzelt", "duzelt ise en az bir bulgu",
                            "her bulguda yer, tur, aciklama, oneri"],
        "esleme": et.esleme,
        "meta": {"hedef_is": hedef, "toplu": True, "isler": isler, "gorevler": gorevler,
                 "haric_aile": next(iter(aile)) if len(aile) == 1 else None, "_esleme": dict(et.esleme)},
    }


def _tek_derle(j) -> tuple[dict | None, str | None]:
    if not isinstance(j, dict) or j.get("karar") not in ("gecer", "duzelt") or not isinstance(j.get("bulgular"), list):
        return None, "karar (gecer|duzelt) / bulgular dizisi yok"
    return {"karar": j["karar"], "bulgular": [{k: str(x.get(k) or "").strip() for k in ("yer", "tur", "aciklama", "oneri")}
                                              for x in j["bulgular"] if isinstance(x, dict)]}, None


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if meta.get("toplu"):
        if not isinstance(j, dict) or not isinstance(j.get("isler"), dict):
            return None, ["cevap JSON değil ya da 'isler' nesnesi yok"]
        et = c.Etiketler(esleme)
        out, e = [], []
        for D, x in j["isler"].items():
            u = et.uzun(str(D))
            if not u:
                e.append(f"{D}: bilinmeyen iş etiketi"); continue
            r, h = _tek_derle(x)
            if h:
                e.append(f"{D}: {h}"); continue
            out.append({"hedef_is": u, **r})
        return {"surum": 1, "toplu": True, "isler": out}, e
    r, h = _tek_derle(j)
    if h:
        return None, [f"cevap JSON değil ya da {h}"]
    return {"surum": 1, "hedef_is": meta["hedef_is"], **r}, []


def _tek_dogrula(cikti: dict, on: str = "") -> list[str]:
    e = []
    if cikti["karar"] == "duzelt" and not cikti["bulgular"]:
        e.append(f"{on}karar duzelt ama bulgu yok")
    if cikti["karar"] == "gecer" and cikti["bulgular"]:
        e.append(f"{on}karar gecer ama bulgu var — ya kararı duzelt yap ya bulguları kaldır")
    for i, b in enumerate(cikti["bulgular"], 1):
        if b["tur"] not in TURLER:
            e.append(f"{on}bulgu {i}: tur {b['tur']!r} tanımsız")
        if not b["yer"] or len(b["aciklama"].split()) < 4:
            e.append(f"{on}bulgu {i}: yer ve gerekçeli açıklama zorunlu")
    return e


def dogrula(cikti: dict, meta: dict) -> list[str]:
    if not cikti.get("toplu"):
        return _tek_dogrula(cikti)
    ters = {v: k for k, v in (meta.get("_esleme") or {}).items()}
    e = []
    gelen = {x["hedef_is"] for x in cikti["isler"]}
    for is_id in meta["isler"]:
        if is_id not in gelen:
            e.append(f"{ters.get(is_id, is_id)}: kayıt yok (her D için karar yaz)")
    for x in cikti["isler"]:
        e += _tek_dogrula(x, f"{ters.get(x['hedef_is'], x['hedef_is'])}: ")
    return e


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    if cikti.get("toplu"):
        et = c.Etiketler(esleme)
        return json.dumps({"isler": {et.kisa(x["hedef_is"]): {"karar": x["karar"], "bulgular": x["bulgular"]}
                                     for x in cikti["isler"]}}, ensure_ascii=False, indent=1)
    return json.dumps({"karar": cikti["karar"], "bulgular": cikti["bulgular"]}, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    """Denetim raporu hedef işin klasörüne yazılır (içerik verisine dokunmaz; Kurul 1'de de serbest). Toplu denetimde
    her hedef işe kendi kaydı yazılır."""
    for x in (cikti["isler"] if cikti.get("toplu") else [cikti]):
        hedef = c.is_klasoru(x["hedef_is"])
        c.yaz(hedef / "denetim.json", {"surum": 1, "hedef_is": x["hedef_is"], "karar": x["karar"], "bulgular": x["bulgular"],
                                       **({"toplu_is": meta.get("hedef_is")} if cikti.get("toplu") else {})})
        c.durum_yaz(x["hedef_is"], denetim={"karar": x["karar"], "bulgu": len(x["bulgular"]),
                                            "turler": sorted({b["tur"] for b in x["bulgular"]}), "zaman": c.simdi(),
                                            "icerik": icerik_izi(x["hedef_is"])})
    return c.is_klasoru(cikti["isler"][0]["hedef_is"] if cikti.get("toplu") else cikti["hedef_is"]) / "denetim.json"


def icerik_izi(is_id: str) -> str:
    """Denetlenen çıktının izi: iş yeniden UYGULANSA da içerik aynıysa yeniden denetlenmez (2026-10-24; zaman damgasıyla
    karar verilince değişmemiş 6 iş yeniden denetlenip yeni, gereksiz bulgular çıkıyordu)."""
    return c.sha(json.dumps(c.oku(c.is_klasoru(is_id) / "cikti.json"), ensure_ascii=False, sort_keys=True), 16)
