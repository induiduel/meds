"""Görev `sik_aciklama` — örnek sorunun şık açıklamalarını standarda (SIK_ACIKLAMA_STANDARDI.md) getirir.

Hedef: örnek soru kimliği (`src/data/ornek_sorular/kN/<ders>.json` içindeki `…-kNN-qNN`). Girdi: soru, şıklar, doğru
cevap, mevcut açıklamalar (salt okunur), kanıt sayfası + açıklamalarda anılan sayfaların slayt metni. Çıktı: beş şık
açıklaması. Doğru cevap, şıklar ve kök DEĞİŞMEZ; yalnız `sik_aciklamalari` yazılır (uygulamada yedekli).
Betik katmanı: mevcut açıklamalar zaten standardı geçiyorsa model çağrılmaz.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .. import cekirdek as c
from . import _ortak as o

KURALLAR = ["kaynak_sadakati", "sik_aciklama", "turkce_uslup", "cikti_disiplini"]
ORNEK = c.KOK / "src" / "data" / "ornek_sorular"


def bul(soru_id: str) -> tuple[Path, dict, dict]:
    m = re.match(r"(k(\d)-\d{2})", soru_id)
    if not m:
        raise SystemExit(f"örnek soru kimliği kN-NN-… olmalı: {soru_id}")
    for p in sorted((ORNEK / f"k{m.group(2)}").glob(f"{m.group(1)}-*.json")):
        if not soru_id.startswith(p.stem):
            continue
        d = c.oku(p, {})
        for kz in d.get("kazanimlar") or []:
            for q in kz.get("sorular") or []:
                if q.get("id") == soru_id:
                    return p, d, q
    raise SystemExit(f"örnek soru yok: {soru_id}")


def _sayfalar(q: dict) -> list[int]:
    s = [(q.get("kanit") or {}).get("sayfa")]
    for t in (q.get("sik_aciklamalari") or {}).values():
        s += [int(x) for x in re.findall(r"\(s\.\s*(\d+)", t or "")]
    return sorted({x for x in s if isinstance(x, int)})[:6]


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    p, d, q = bul(hedef)
    ders_id = hedef[:5]
    kaynak = o.kaynak_sayfalar(ders_id)
    say = _sayfalar(q)
    slayt = "\n".join(f"Sayfa {s}: {o.sade(kaynak[s], 900)}" for s in say if kaynak.get(s, "").strip())
    sec = q.get("secenekler") or {}
    girdi = (f"Ders: {d.get('konu', ders_id)}\nSoru: {q.get('soru', '')}\n"
             + "\n".join(f"{h}) {sec.get(h, '')}" for h in o.HARFLER)
             + f"\nDoğru cevap: {q.get('dogru')}\nGenel açıklama: {q.get('aciklama', '')}"
             + "\n\n## Mevcut şık açıklamaları (standardı karşılamıyor; bilgiyi koru, biçimi düzelt)\n"
             + "\n".join(f"{h}: {(q.get('sik_aciklamalari') or {}).get(h, '')}" for h in o.HARFLER)
             + (f"\n\n## Slayt metni (dayanak)\n{slayt}" if slayt else ""))
    ornek = {"sik_aciklamalari": {"A": "Yanlış. … (s. 12)", "B": "Yanlış. …", "C": "Doğru. …", "D": "Yanlış. …",
                                  "E": "Yanlış. …"}}
    return {
        "amac": "Bu sorunun beş şıkkının açıklamasını yeniden yaz. Soru, şıklar ve doğru cevap değişmez.",
        "kurallar": KURALLAR,
        "ek_kurallar": [
            "Her açıklama 'Doğru.' ya da 'Yanlış.' ile başlar; yalnız doğru cevabın açıklaması 'Doğru.' ile başlar.",
            "Bilgi slayt metninden ya da mevcut açıklamadan gelir; sayfa biliniyorsa sona '(s. N)' eklenebilir — yalnız dayanakta verilen sayfalar.",
            "Yanlış şıkta kavramı tanıttıktan sonra soruda istenen özelliğin hangi kavrama ait olduğunu söyle.",
        ],
        "girdi": girdi,
        "cikti_bicimi": "Yalnız şu JSON:\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": ["beş şık da var", "önek Doğru./Yanlış. doğru cevapla uyumlu",
                            "her açıklama 2–4 cümle, 20–65 kelime, en az bir olumlu kimlik/işlev cümlesi",
                            "geçiştirici kalıp, harf anma, süreç dili yok", "sayfa numarası yalnız dayanaktaki sayfalardan"],
        "esleme": {},
        "meta": {"soru_id": hedef, "ders_id": ders_id, "kurul": int(hedef[1]), "dosya": str(p.relative_to(c.KOK)),
                 "dogru": q.get("dogru"), "sayfalar": say, "sayfa_sayisi": max(kaynak) if kaynak else None,
                 "mevcut": q.get("sik_aciklamalari") or {}},
    }


def betik(esleme: dict, meta: dict) -> str | None:
    """Mevcut açıklamalar zaten standardı geçiyorsa model gerekmez."""
    return json.dumps({"sik_aciklamalari": meta["mevcut"]}, ensure_ascii=False) if meta.get("mevcut") else None


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    sa = (j or {}).get("sik_aciklamalari") if isinstance(j, dict) else None
    if not isinstance(sa, dict):
        return None, ["cevap JSON değil ya da 'sik_aciklamalari' yok"]
    return {"surum": 1, "soru_id": meta["soru_id"],
            "sik_aciklamalari": {str(h).strip().upper()[:1]: str(t).strip() for h, t in sa.items()}}, []


def dogrula(cikti: dict, meta: dict) -> list[str]:
    e = []
    sa = cikti["sik_aciklamalari"]
    if sorted(sa) != list(o.HARFLER):
        e.append(f"şıklar tam A–E olmalı (var: {''.join(sorted(sa))})")
    for h in o.HARFLER:
        e += o.sik_aciklamasi_denetle(h, sa.get(h, ""), meta["dogru"], h)
        for s in re.findall(r"\(s\.\s*(\d+)", sa.get(h, "")):
            if int(s) not in meta["sayfalar"]:
                e.append(f"{h}: sayfa {s} dayanakta yok (izinli: {meta['sayfalar']})")
    return e


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    return json.dumps({"sik_aciklamalari": cikti["sik_aciklamalari"]}, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    if cikis is not None:
        hedef = cikis / f"{meta['soru_id']}.json"
        c.yaz(hedef, cikti)
        return hedef
    if meta["kurul"] == 1 and not k1_izin:
        raise SystemExit("Kurul 1 verisine otomatik yazım yok (El kitabı §0.4): --cikis DİZİN ile sınama ya da --k1-izin")
    p = c.KOK / meta["dosya"]
    d = c.oku(p, {})
    yedek = c.TEMP / "gorev" / "_yedek" / f"{p.stem}.{c.simdi().replace(':', '')}.json"
    c.yaz(yedek, d)
    for kz in d.get("kazanimlar") or []:
        for q in kz.get("sorular") or []:
            if q.get("id") == meta["soru_id"]:
                if q.get("dogru") != meta["dogru"]:
                    raise SystemExit(f"{meta['soru_id']}: doğru cevap paket hazırlandıktan sonra değişmiş — yeniden hazırla")
                q["sik_aciklamalari"] = cikti["sik_aciklamalari"]
                c.yaz(p, d)
                return p
    raise SystemExit(f"soru dosyada bulunamadı: {meta['soru_id']}")
