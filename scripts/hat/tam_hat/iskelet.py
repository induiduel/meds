#!/usr/bin/env python3
"""Çıktı iskeleti + kimlik ataması betikle (C7, 2026-11-16) — model kimlik/numara/kaynak alanı yazmasın, yalnız içerik doldursun.
DETERMİNİSTİK: LLM yok.

  python3 scripts/hat/tam_hat/iskelet.py uret <ders klasörü> --ders <key>     # → <klasör>/baglam/iskelet_<aşama>.json
  python3 scripts/hat/tam_hat/iskelet.py numarala <çıktı.json> --tur anlatim|ornek_soru [--ders <key>]
                                                                             # eksik/boş kimlikleri sırayla doldurur (var olana dokunmaz)
  python3 scripts/hat/tam_hat/iskelet.py denetle <çıktı.json>                 # doldurulmamış iskelet yeri kaldı mı (çıkış 1)

Uygulanan aşamalar (gerçek kapıların beklediği alanlardan çıkarıldı):
  anlatim       konusma_v2.json: surum/ders_id/anahtar + bölüm (atom `hedef`ine göre ardışık slayt grubu) + slayt başına paragraf
                (id <did>-pNNN, sayfa dolu), cumleler []. Kapı (konusma_v2 --dogrula) boş paragrafı "cümle yok", boş bölüm
                başlığını "başlık boş" diye reddeder → boş iskelet GEÇMEZ. Cümle kimliği: `numarala --tur anlatim`.
  ornek_soru    src/data/ornek_sorular/k2/<dosya>.json üst alanları (paket'ten konu/hoca) + bilgi paketi başına kazanım (no dolu,
                metin "", `_s` kaynak slaytlar), sorular []. Soru kimliği <id>-qNN: `numarala --tur ornek_soru`.
  cikmis_analiz degerlendirme/cikmis_analiz.json: `sorular` = doğrulanmış her çıkmış için {aciklama:[], ornek:"", tuzak:""} +
                bağlam (`_s`, `_kok`, `_cevap`). ders_analizi --dogrula boş açıklamayı (<3 cümle / ornek yok) reddeder.
  degerlendirme atom ADAYLARI: slayt başına madde satırları (`s` + birebir `kanit` dolu) — `atom_adaylari` anahtarında, `atomlar`a
                DEĞİL: degerlendirme_dogrula boş `ifade`yi denetlemediği için iskelet asla `atomlar`a konmaz (kapı zayıflamasın).
                ÖLÇÜM (k2-28): 3,5k kelime — slayt metnini (sayfalar.json 2,0k) İKİNCİ kez taşıyor; bu yüzden brife KONMAZ,
                yalnız isteğe bağlı başvuru dosyasıdır (atom kimliği ataması için).
Uygulanmayan: önem listesi (madde sayısı/seçimi modelin kararıdır; `onem_dogrula` kendi şemasını denetler), çözücü (ref'ler
örnek soru kimliklerinden gelir → örnek soru numaralandıktan sonra betikle kopyalanabilir, ayrı iş), çizim/çapa (tasarruf dışı).
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
import re
import sys
from pathlib import Path

KOK = _kok.MEDS
DEPO = KOK.parent / "meds_database_v2" / "ders_bilgi"
DOLDUR = "<DOLDUR>"  # denetle() bu işareti arar; model bunu içerikle değiştirir
ASAMALAR = ("anlatim", "ornek_soru", "cikmis_analiz", "degerlendirme")


def _did(key: str) -> str:
    m = re.match(r"k(\d)-(\d{2})", key)
    return f"k{m.group(1)}-{m.group(2)}" if m else key


def _paket(key: str) -> dict | None:
    p = DEPO / key / "degerlendirme" / "paket.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def isk_anlatim(key: str, sayf: dict, pk: dict | None) -> dict:
    did = _did(key)
    hedef: dict[int, str] = {}
    for a in (pk or {}).get("atomik_bilgi_envanteri", {}).get("atomlar", []):
        hedef.setdefault(int(a.get("s") or 0), a.get("hedef") or "")
    bol, son = [], None
    np_ = 0
    for s in sorted(sayf, key=int):
        h = hedef.get(int(s)) or son or DOLDUR
        if h != son or not bol:
            bol.append({"id": f"{did}-b{len(bol) + 1:02d}", "baslik": h, "paragraflar": []})
            son = h
        np_ += 1
        bol[-1]["paragraflar"].append({"id": f"{did}-p{np_:03d}", "sayfa": int(s), "cumleler": []})
    return {"_iskelet": "anlatım: paragraf/bölüm kimliklerini ve sayfa alanını DEĞİŞTİRME; cümle ekle (id boş bırakılabilir → "
                        "iskelet.py numarala --tur anlatim). Konuşulmayan slaytın paragrafını sil; bölüm başlığını düzeltebilirsin.",
            "surum": 2, "ders_id": did, "anahtar": key, "baslik": (pk or {}).get("konu") or DOLDUR, "bolumler": bol}


def isk_ornek(key: str, pk: dict | None) -> dict:
    pk = pk or {}
    kz = [{"no": i + 1, "metin": DOLDUR, "_s": b.get("s"), "_bp": b.get("id"), "_baslik": b.get("baslik"), "sorular": []}
          for i, b in enumerate(sorted(pk.get("bilgi_paketleri", []), key=lambda b: (min(b.get("s") or [0]), str(b.get("id")))))]
    return {"_iskelet": "örnek soru: kazanım `no` ve sırasını DEĞİŞTİRME; `metin`i yaz, `sorular`a soru ekle (id boş → iskelet.py "
                        "numarala --tur ornek_soru). Alt çizgili (_s/_bp/_baslik) alanlar bağlamdır, kalabilir.",
            "id": DOLDUR, "kurul": int(key[1]) if re.match(r"k\d", key) else DOLDUR, "ders": pk.get("brans") or DOLDUR,
            "konu": pk.get("konu") or DOLDUR, "ogretim_uyesi": pk.get("ogretim_uyesi") or DOLDUR, "kazanimlar": kz}


def isk_cikmis(key: str, pk: dict | None) -> dict:
    ckp = (pk or {}).get("cikmis", {}).get("kaynak")
    q = []
    if ckp and (KOK / ckp).exists():
        q = [x for x in json.loads((KOK / ckp).read_text(encoding="utf-8")).get("q", []) if x.get("dogrulandi", True)]
    return {"_iskelet": "çıkmış analizi: soru kimliklerini DEĞİŞTİRME; her soruya aciklama (≥3 cümle) + ornek + tuzak yaz.",
            "giris": DOLDUR,
            "sorular": {str(x.get("id")): {"_s": x.get("s"), "_seviye": x.get("seviye"), "_kok": str(x.get("kok", ""))[:200],
                                           "_cevap": x.get("cevap"), "aciklama": [], "ornek": DOLDUR, "tuzak": DOLDUR} for x in q}}


def isk_degerlendirme(key: str, sayf: dict) -> dict:
    ad = []
    for s in sorted(sayf, key=int):
        for ln in sayf[s].splitlines():
            t = re.sub(r"^\s*[•▪●■◦o\-–]\s+", "", ln).strip()
            if len(t.split()) >= 4 and not t.isupper():
                ad.append({"s": int(s), "kanit": t})
    for i, a in enumerate(ad, 1):
        a["id"] = f"{key}-a{i:02d}"
    return {"_iskelet": "değerlendirme: atom_adaylari slayt satırlarıdır (kanıt birebir). Atom yazarken kimliği/s/kanit'i KORU, "
                        "ifade/kategori/baslik/hedef ekle ve `atomik_bilgi_envanteri.atomlar`a TAŞI; anlamsız adayı at.",
            "atom_adaylari": ad}


def uret(klasor: Path, key: str) -> dict[str, Path]:
    sayf = json.loads((klasor / "sayfalar.json").read_text(encoding="utf-8"))
    pk = _paket(key)
    bg = klasor / "baglam"
    bg.mkdir(parents=True, exist_ok=True)
    out = {"degerlendirme": isk_degerlendirme(key, sayf)}
    if pk:  # paket (E1) sonrası aşamalar
        out |= {"anlatim": isk_anlatim(key, sayf, pk), "ornek_soru": isk_ornek(key, pk), "cikmis_analiz": isk_cikmis(key, pk)}
    yol = {}
    for a, o in out.items():
        yol[a] = bg / f"iskelet_{a}.json"
        yol[a].write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
    return yol


def numarala(d: dict, tur: str, key: str | None = None) -> int:
    """Boş/eksik kimlikleri doldurur; var olan kimliğe dokunmaz (yayınlı deeplink korunur). Döner: atanan sayısı."""
    n = 0
    if tur == "anlatim":
        did = d.get("ders_id") or _did(key or "")
        gor = set()
        for b in d.get("bolumler", []):
            gor |= {b.get("id")} | {p.get("id") for p in b.get("paragraflar", [])} | \
                {c.get("id") for p in b.get("paragraflar", []) for c in p.get("cumleler", [])}
        sayac = {t: max([int(m.group(1)) for i in gor if i and (m := re.fullmatch(rf"{re.escape(did)}-{t}(\d+)", i))] or [0])
                 for t in "bpc"}
        gen = {"b": 2, "p": 3, "c": 4}

        def ver(x: dict, t: str) -> None:
            nonlocal n
            if not x.get("id"):
                sayac[t] += 1
                x["id"] = f"{did}-{t}{sayac[t]:0{gen[t]}d}"
                n += 1
        for b in d.get("bolumler", []):
            ver(b, "b")
            for p in b.get("paragraflar", []):
                ver(p, "p")
                for c in p.get("cumleler", []):
                    ver(c, "c")
    elif tur == "ornek_soru":
        onek = d.get("id")
        if not onek or onek == DOLDUR:
            raise SystemExit("HATA: üst `id` dolu olmalı (soru kimliği <id>-qNN)")
        qs = [q for kz in d.get("kazanimlar", []) for q in kz.get("sorular", [])]
        mx = max([int(m.group(1)) for q in qs if (m := re.fullmatch(rf"{re.escape(onek)}-q(\d+)", q.get("id") or ""))] or [0])
        for kz in d.get("kazanimlar", []):
            for q in kz.get("sorular", []):
                q.setdefault("kazanim", kz.get("no"))
                if not q.get("id"):
                    mx += 1
                    q["id"] = f"{onek}-q{mx:02d}"
                    n += 1
        d["soru_sayisi"] = len(qs)
    else:
        raise SystemExit(f"bilinmeyen tür: {tur}")
    return n


def denetle(d) -> list[str]:
    h = []

    def gez(x, yol):
        if isinstance(x, dict):
            for k, v in x.items():
                gez(v, f"{yol}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                gez(v, f"{yol}[{i}]")
        elif x == DOLDUR:
            h.append(f"doldurulmamış: {yol}")
    gez(d, "$")
    if isinstance(d, dict) and "_iskelet" in d:
        h.append("`_iskelet` talimat alanı çıktıda kalmış (silinmeli)")
    return h


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("eylem", choices=("uret", "numarala", "denetle"))
    ap.add_argument("yol", type=Path)
    ap.add_argument("--ders")
    ap.add_argument("--tur", choices=("anlatim", "ornek_soru"))
    a = ap.parse_args()
    if a.eylem == "uret":
        if not a.ders:
            ap.error("--ders gerekli")
        for asama, p in uret(a.yol, a.ders).items():
            print(f"  iskelet_{asama}.json  {len(p.read_text(encoding='utf-8').split())} kelime  {p}")
        return 0
    d = json.loads(a.yol.read_text(encoding="utf-8"))
    if a.eylem == "numarala":
        n = numarala(d, a.tur, a.ders)
        a.yol.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{a.yol}: {n} kimlik atandı")
        return 0
    h = denetle(d)
    for x in h[:50]:
        print("HATA", x)
    print(f"iskelet denetimi: {len(h)} HATA")
    return 1 if h else 0


if __name__ == "__main__":
    sys.exit(main())
