#!/usr/bin/env python3
"""2025-2026 Kurul 3 arşiv dersi hazırlığı — TEK ders, tek komut (LLM YOK, yalnız betik).

  k3_ders.py hazirla <key>     → meds_database_25_26/taslak/<key>/  (kaynak.md, sayfalar.json, baglam.json,
                                  cikmis_aday.json, onizleme.md, is.md) + pdf/kurul3/<key>.pdf
  k3_ders.py durum [<key>]     → ders ders hangi katman var (taslak/metin/ses/isaret/medspak)

Hazırlık adımları (hepsi betik, LLM çağrısı yok):
  1. Ham PDF (indirilmiş) → pdf/kurul3/<key>.pdf  (kalıcı ad; sunucu bu yolu okur)
  2. cikar.pdf_metni → kaynak.md (PyMuPDF; metin katmanı <40 karakter ise OCR)  + sayfa_varliklari → sayfalar.json
  3. Görsel/tablo sayfası için sayfa görüntüsü (sayfa_goruntu/N.png) — yalnız okunması gerekenler
  4. Çıkmış adayları: bge-m3 embed ile donem3-kurul3 havuzundan (skor ≥0,48) → cikmis_aday.json
  5. baglam.json: ders kimliği, PDF yolu, sayfa sayısı, program eşleşmesi
  6. onizleme.md: her sayfanın ilk 12 satırı (metin yazarken TEK okuma dosyası; ayrıca kaynak.md açılmaz)
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

import json
import os
import re
import shutil
import sys
from pathlib import Path

MEDS = _kok.MEDS
ROOT = MEDS.parent
DB = ROOT / "meds_database_25_26"
TASLAK = DB / "taslak"
PDF_DIR = DB / "pdf" / "kurul3"
HAM = PDF_DIR / "_ham"
ESLESME = DB / "kurul3_eslesme.json"
ARSIV = MEDS / "data" / "arsiv_25_26"

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "ders_isci"))
sys.path.insert(0, str(MEDS / "scripts" / "altyapi" / "agents"))


def eslesme() -> dict:
    return json.loads(ESLESME.read_text(encoding="utf-8"))


def pdf_kopyala(key: str, e: dict) -> Path:
    hedef = PDF_DIR / f"{key}.pdf"
    if hedef.exists() and hedef.stat().st_size > 1024:
        return hedef
    ham = HAM / f"{e['file_id']}.pdf"
    if not ham.exists():
        raise SystemExit(f"HATA: ham PDF yok: {ham} (önce k3_hazirla.py indir)")
    shutil.copy2(ham, hedef)
    return hedef


def metin_cikar(key: str, pdf: Path, taslak: Path) -> dict:
    import cikar
    kaynak = taslak / "kaynak.md"
    sayfalar = taslak / "sayfalar.json"
    if not kaynak.exists() or not sayfalar.exists():
        metin, bilgi = cikar.pdf_metni(pdf)
        kaynak.write_text(metin, encoding="utf-8")
        varlik = cikar.sayfa_varliklari(pdf, taslak)
        (taslak / "kaynak_bilgi.json").write_text(json.dumps({**bilgi, **varlik}, ensure_ascii=False, indent=1), encoding="utf-8")
    return json.loads((taslak / "kaynak_bilgi.json").read_text(encoding="utf-8"))


def cikmis_adaylar(kurul: int, baslik: str, kaynak_md: str, limit: int = 30) -> list[dict]:
    """indir_ve_cikar.cikmis_esle ile aynı mantık (bge-m3 embed, CPU)."""
    pq = _kok.CIKMIS
    if not pq.exists():
        return []
    tum = json.loads(pq.read_text(encoding="utf-8"))
    cid = f"donem3-kurul{kurul}"
    havuz = [q for q in tum if q.get("committeeId") == cid and not q.get("hidden") and not q.get("iptal")]
    if not havuz:
        return []
    try:
        from lib import embed
        q_texts, parcalar = [], [p.strip()[:800] for p in re.split(r"^=== SAYFA \d+ ===$", kaynak_md, flags=re.M) if p.strip()] or [baslik]
        for q in havuz:
            r = q.get("reconstruction") or {}
            ops = r.get("options") or q.get("options") or []
            ans = q.get("correctAnswer")
            ans_txt = next((o.get("text", "") for o in ops if isinstance(o, dict) and o.get("key") == ans), "")
            q_texts.append(f"{q.get('topic') or ''} {r.get('stem') or q.get('stem') or ''} {ans_txt}".strip())
        sim = (embed(q_texts) @ embed([f"{baslik}: {p}" for p in parcalar[:60]]).T).max(axis=1)
        out = []
        for i in sorted(range(len(havuz)), key=lambda x: float(sim[x]), reverse=True)[:limit]:
            skor = float(sim[i])
            if skor < 0.48:
                continue
            q, r = havuz[i], havuz[i].get("reconstruction") or {}
            ops = r.get("options") or q.get("options") or []
            out.append({
                "id": q["id"], "yil": q.get("examYear"), "konu": q.get("topic"),
                "soru": r.get("stem") or q.get("stem"),
                "secenekler": {o.get("key"): o.get("text") for o in ops if isinstance(o, dict)},
                "cevap": q.get("correctAnswer"), "skor": round(skor, 3),
            })
        return out
    except Exception as ex:  # noqa: BLE001
        print(f"UYARI: çıkmış eşleme yapılamadı ({ex})", file=sys.stderr)
        return []


def onizleme_yaz(taslak: Path, e: dict) -> None:
    """Metin yazarken TEK okuma dosyası: sayfa metni + görselli/tablolu işareti. kaynak.md ayrıca açılmaz."""
    kaynak = (taslak / "kaynak.md").read_text(encoding="utf-8")
    varliklar = {int(x["sayfa"]): x for x in json.loads((taslak / "sayfalar.json").read_text(encoding="utf-8"))}
    s = [f"# {e['baslik']} — kaynak sayfaları ({e['sayfa']} sayfa)", ""]
    parcalar = re.split(r"^=== SAYFA (\d+) ===$", kaynak, flags=re.M)
    for i in range(1, len(parcalar), 2):
        n = int(parcalar[i])
        metin = parcalar[i + 1].strip()
        v = varliklar.get(n) or {}
        etiket = []
        if (v.get("gorsel_orani") or 0) >= 0.18 or (v.get("cizim") or 0) >= 25:
            etiket.append("GÖRSEL VAR — görseli ayrıca anlat (slayt.sekil)")
        if v.get("tablolar"):
            etiket.append(f"TABLO ({len(v['tablolar'])}) — karşılaştırmayı anlat")
        s.append(f"## Sayfa {n} {'· ' + ' · '.join(etiket) if etiket else ''}")
        s.append(metin if metin else "(yalnız görsel — görselin sayfası)")
        s.append("")
    (taslak / "onizleme.md").write_text("\n".join(s), encoding="utf-8")


def hazirla(key: str) -> int:
    tablo = eslesme()
    if key not in tablo:
        print(f"HATA: {key} eşleme tablosunda yok (k3_eslesme.py)", file=sys.stderr)
        return 2
    e = tablo[key]
    taslak = TASLAK / key
    taslak.mkdir(parents=True, exist_ok=True)
    pdf = pdf_kopyala(key, e)
    bilgi = metin_cikar(key, pdf, taslak)
    e["sayfa"] = int(bilgi.get("sayfa") or e.get("sayfa") or 0)
    tablo[key] = e
    ESLESME.write_text(json.dumps(tablo, ensure_ascii=False, indent=1), encoding="utf-8")
    kaynak_md = (taslak / "kaynak.md").read_text(encoding="utf-8")
    aday_yol = taslak / "cikmis_aday.json"
    if not aday_yol.exists():
        adaylar = cikmis_adaylar(3, e["baslik"], kaynak_md)
        aday_yol.write_text(json.dumps(adaylar, ensure_ascii=False, indent=1), encoding="utf-8")
    baglam = {
        "is_id": key, "donem": "2025-2026", "arsiv": True, "kurul": 3,
        "committeeId": "donem3-kurul3",
        "numara": e["kurul_no"], "brans_no": e["brans_no"],
        "ders_id": key, "deste_id": f"k3p-{key}",
        "brans": e["brans"], "konu": e["baslik"], "ogretim_uyesi": e.get("hoca") or "",
        "pdf_yolu": str(pdf.relative_to(ROOT)), "pdf_adi": e["dosya"], "file_id": e["file_id"],
        "sayfa": e["sayfa"], "program": e.get("program") or [],
        "aday_cikmislar": json.loads(aday_yol.read_text(encoding="utf-8")) if aday_yol.exists() else [],
        "kaynak": "arsiv-25-26-kurul3",
    }
    (taslak / "baglam.json").write_text(json.dumps(baglam, ensure_ascii=False, indent=1), encoding="utf-8")
    onizleme_yaz(taslak, e)
    print(f"[{key}] hazır: {e['sayfa']} sayfa · {len(kaynak_md.split())} kelime · "
          f"görselli {bilgi.get('goruntu_sayfa', 0)} · tablolu {bilgi.get('tablo_sayfa', 0)} · "
          f"çıkmış aday {len(baglam['aday_cikmislar'])}")
    return 0


def durum(key: str | None = None) -> int:
    tablo = eslesme()
    anahtarlar = [key] if key else list(tablo)
    sa = ARSIV / "sesli_anlatim"
    for k in anahtarlar:
        t = TASLAK / k
        v = lambda p: "✔" if p.exists() else "·"  # noqa: E731
        print(f"{k:52} taslak{v(t / 'baglam.json')} metin{v(t / 'konusma_v2.json')} "
              f"ses{v(sa / 'ses' / k)} zaman{v(sa / 'cumle_zaman' / f'{k}.json')} "
              f"işaret{v(sa / 'isaret' / f'{k}.json')} terim{v(sa / 'terim' / f'{k}.json')} "
              f"medspak{v(DB / 'medspak' / 'kurul3' / f'{k}.medspak')}")
    return 0


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "durum"
    if c == "hazirla":
        raise SystemExit(hazirla(sys.argv[2]))
    if c == "durum":
        raise SystemExit(durum(sys.argv[2] if len(sys.argv) > 2 else None))
    raise SystemExit(f"bilinmeyen komut: {c}")
