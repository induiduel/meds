"""Görev `som_sec` — anlatılan yapının görseldeki yeri: model yalnız NUMARA seçer (Set-of-Mark, ICERIK_MOTORU_V3.md §17.1).

Hedef: sayfa kimliği `kN-NN-pNN`; `--ayar sorgu="…"` anlatımda sözü edilen yapı (ör. "hipertrofiye uğramış miyosit").
Girdi: numaralı SoM kopyası (scripts/kroki/som.py; yoksa üretilir) + her numaranın betikle bulunan etiketi (bölgeye düşen
slayt yazısı). Model koordinat yazmaz: `{"numara": 3}` ya da `{"numara": null}` (yapı görselde yoksa).
Kapı: numara SoM eşlemesinde var; etiketi sorguyla AÇIKÇA örtüşen bir bölge varken etiketi örtüşmeyen başka bölge seçilemez.
Uygulama: `meds_database_v2/ders_bilgi/<ders>/l1/som_secim.json` {sorgu karması: {sayfa, sorgu, roi, numara, model}}.
Katman: yalnız Ü (Gemini görsel) ve elle — Claude araçsız çağrıda görüntü göremez.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .. import cekirdek as c

sys.path.insert(0, str(c.KOK / "scripts" / "kroki"))

OGRENCI_METNI = False   # çıktı iç veri (kısa etiket taşır); ortak etiket sızıntısı kapısı uygulanmaz
KURALLAR = ["cikti_disiplini"]


def _som(ders: str, sayfa: int) -> tuple[Path, dict, list[dict]]:
    from ortak import TEMP, oku
    import l0kayit
    d = TEMP / "kroki" / ders / "som"
    g, m = d / f"p{sayfa:02d}.webp", d / f"p{sayfa:02d}.json"
    _, s = l0kayit.sayfa(ders, sayfa)
    if not g.exists() or not m.exists():
        import cv2
        import pymupdf
        import som
        from ortak import pdf_bul, yaz
        roi, goruntu = som.sayfa_som(pymupdf.open(pdf_bul(ders)), s, ders)
        if not roi:
            raise SystemExit(f"{ders} s{sayfa}: numaralanacak görsel bölge yok")
        d.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(g), goruntu, [cv2.IMWRITE_WEBP_QUALITY, 70])
        yaz(m, {str(r["no"]): r["id"] for r in roi}, 1)
        s = {**s, "roi": roi}
    return g, oku(m), s.get("roi") or []


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    m = re.fullmatch(r"(k\d-\d{2})-p(\d+)", hedef)
    sorgu = ((ayar or {}).get("sorgu") or "").strip()
    if not m or not sorgu:
        raise SystemExit("som_sec hedefi kN-NN-pNN ve --ayar sorgu=\"…\" gerekli")
    ders, sayfa = m.group(1), int(m.group(2))
    g, esleme, roi = _som(ders, sayfa)
    etiket = {str(r["no"]): r.get("etiket", "") for r in roi}
    satir = "\n".join(f"{n}: {etiket.get(n) or '(yazısız bölge)'}" for n in sorted(esleme, key=int))
    return {
        "amac": (f"Ekteki slayt görselinde turuncu çerçeveli ve numaralı bölgeler var. Anlatımda sözü edilen yapı hangi "
                 f"numaralı bölgede? Yapı: \"{sorgu}\". Yapı hiçbir numaralı bölgede değilse numara null."),
        "kurallar": KURALLAR,
        "ek_kurallar": ["Koordinat yazma; yalnız görseldeki numarayı seç.",
                        "Bölgenin içindeki yazı (aşağıda) yapının adıysa o bölgeyi tercih et; emin değilsen null."],
        "girdi": f"Görsel: {g}\nBölgeler ve içlerindeki slayt yazısı:\n{satir}",
        "cikti_bicimi": 'Yalnız şu JSON: {"numara": 3}  ya da  {"numara": null}',
        "denetim_listesi": ["numara görseldeki bir numara ya da null"],
        "esleme": {},
        "meta": {"ders_id": ders, "sayfa": sayfa, "sorgu": sorgu, "gorsel": str(g), "som": esleme, "etiket": etiket,
                 "kurul": int(ders[1])},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or "numara" not in j:
        return None, ["cevap JSON değil ya da 'numara' yok"]
    n = j["numara"]
    n = None if n in (None, "", "null") else str(int(n)) if str(n).strip().isdigit() else str(n)
    return {"surum": 1, "ders_id": meta["ders_id"], "sayfa": meta["sayfa"], "sorgu": meta["sorgu"], "numara": n,
            "roi": meta["som"].get(n) if n else None}, []


def dogrula(cikti: dict, meta: dict) -> list[str]:
    from ortak import kokler
    e = []
    n = cikti["numara"]
    if n is not None and n not in meta["som"]:
        return [f"numara {n} görselde yok (var: {', '.join(sorted(meta['som'], key=int))})"]
    sk = kokler(meta["sorgu"])
    ortusen = [k for k, t in meta["etiket"].items() if t and len(sk & kokler(t)) >= max(1, len(sk) // 2)]
    if ortusen and n not in ortusen:
        e.append(f"etiketi sorguyla örtüşen bölge(ler) {ortusen} varken {n} seçildi")
    return e


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    return json.dumps({"numara": int(cikti["numara"]) if cikti["numara"] else None})


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    from ortak import DEPO, oku
    if cikis is not None:
        p = cikis / f"{meta['ders_id']}-p{meta['sayfa']:02d}-{c.sha(meta['sorgu'], 8)}.json"
        c.yaz(p, cikti)
        return p
    p = DEPO / meta["ders_id"] / "l1" / "som_secim.json"
    d = oku(p) or {}
    d[c.sha(f"{meta['sayfa']}|{meta['sorgu']}", 12)] = {k: cikti[k] for k in ("sayfa", "sorgu", "numara", "roi")}
    c.yaz(p, d)
    return p


def sinama_ornekleri(meta: dict) -> tuple[dict, list[dict]]:
    from ortak import kokler
    sk = kokler(meta["sorgu"])
    ortusen = [k for k, t in meta["etiket"].items() if t and len(sk & kokler(t)) >= max(1, len(sk) // 2)]
    iyi_no = ortusen[0] if ortusen else sorted(meta["som"], key=int)[0]
    kotu = [{"ad": "olmayan numara", "degistir": [[["numara"], 99]], "beklenen": "görselde yok"}]
    baska = [k for k in meta["som"] if k not in ortusen]
    if ortusen and baska:
        kotu.append({"ad": "etiketle çelişen seçim", "degistir": [[["numara"], int(baska[0])]], "beklenen": "örtüşen"})
    return {"numara": int(iyi_no)}, kotu
