#!/usr/bin/env python3
"""Yayın öncesi sıkı çizim + lazer kapısı (H59, kullanıcı kararı 2026-10-25: "bir daha kimse çizim hatası yapmasın").

cizim_dogrula.py tek tek komutları süzer; bu kapı yayınlanacak DERSİN BÜTÜNÜNE bakar ve 0 HATA vermeden çizim/işaret
yayına gitmez (ders zinciri `cizim` adımı, arsiv_yayinla.py, sekil_cizim.py birlestir). Kurallar CIZIM_KURALLARI.md §10.

  K1  Şekil çapası görsele gitmeli: çapada `sekil`/`tablo` dolu cümlenin işareti resim/tablo değilse (sayfada görsel
      varken) HATA. (H59: madde şekli eziyordu.)
  K2  Uydurma çapa yok: `madde` çapası olup lazeri yazıya düşmeyen (kelime/sayfa) cümle oranı > %15 → HATA
      (her cümleye en yakın maddeyi/M0'ı basan toplu betik izi).
  K3  Şekil kapsamı: yazarın şekil/tablo çapası yazdığı ve lazeri resim/tablo olan cümlelerin en az %40'ında görsel
      üstü çizim (kontur/akış/eğri) olmalı (sınama dersleri k2-02/k2-07 %44–52). ≥5 şekil cümlesi olan derste.
      (Çapa dosyası yoksa lazeri resim/tablo olan bütün cümleler sayılır.)
  K4  Resim cümlesinde panel yok: lazeri resim olan cümleye `sema` paneli HATA (H51).
  K5  Bütün resmi çevreleyen kontur yok: kontur kutusu cümlenin resim kutusunun ≥%85'ini kaplıyorsa HATA — anlatılan
      parça dolanır, resim değil.
  K6  Yoğunluk: cümlede >2, sayfada >8 çizim HATA.
  K7  Çizim, cümlenin lazerinin gösterdiği sayfada olmalı (başka sayfaya çizim HATA).
  K8  Etiketsiz ok HATA (H40); kontur 5–20 nokta, koordinatlar 0–1.
  K9  metinHash: işaret ve çizim aynı metin sürümünden olmalı.
  K10 Okunabilir metinli tabloda çizim yok: lazeri tablo olan cümlede kontur/akış/eğri/panel HATA — yalnız marker (H85).
  K11 Kelime ↔ kelime oku yok: akış oku yalnız lazeri resim olan cümlede (resim içinde iki görsel yapı arası) (H85).
  K12 Zoom ölçülü: `yakin` yalnız resim cümlesinde ve sayfanın ≤%20'si (H85).
  K13 Panel düzeni tanımlı olmalı: `sema` komutunun `duzen`i sablonlar.json `duzenler` listesinde değilse HATA; değer
      kartı (`deger`) alanları sablon.coz kuralına uymalı (sayı içeren `deger`, `aciklama`, `cikmis` tam sayı).

Kullanım:
  .venv-ocr/bin/python scripts/cizim/cizim_kapisi.py <key> [--kok data/sesli_anlatim | data/arsiv_25_26/sesli_anlatim]
  .venv-ocr/bin/python scripts/cizim/cizim_kapisi.py --hepsi --kok data/arsiv_25_26/sesli_anlatim
Çıkış: 0 = geçti, 1 = HATA var.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts" / "arsiv_25_26"))

KAPSAM_ALT = 0.40
UYDURMA_UST = 0.15
TUM_RESIM = 0.85


ZOOM_UST = 0.20  # H85: zoom yalnız küçük resim bölgesine

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sablon as SB  # noqa: E402

DUZENLER = set(SB.kutuphane().get("duzenler") or [])


def _alan(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def _kesisim(a, b):
    return _alan([max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])])


def denetle(key: str, kok: Path) -> tuple[list[str], dict]:
    from pdf_isaret import cumle_sonlari, cumle_capalari
    from arsiv_yayinla import metin_paragraflari

    H: list[str] = []
    isr_yol, cz_yol, capa_yol = kok / "isaret" / f"{key}.json", kok / "cizim" / f"{key}.json", kok / "capa" / f"{key}.json"
    if not isr_yol.exists():
        return [f"{key}: işaret dosyası yok"], {}
    isr = json.loads(isr_yol.read_text(encoding="utf-8"))
    cz = json.loads(cz_yol.read_text(encoding="utf-8")) if cz_yol.exists() else {"p": {}}
    I, P = isr.get("c") or {}, cz.get("p") or {}

    if cz_yol.exists() and cz.get("metinHash") and isr.get("metinHash") and cz["metinHash"] != isr["metinHash"]:
        H.append("K9 işaret ve çizim farklı metin sürümünden (metinHash)")

    # K1/K2: çapa → istemci cümlesi (pdf_isaret ile aynı eşleme)
    sekil_cumle, madde_say, madde_bos = 0, 0, 0
    beyanli: set[tuple[str, int]] | None = None  # yazarın şekil/tablo dediği cümleler (K3 bunlarda ölçülür)
    if capa_yol.exists() and (kok / "metin" / f"{key}.md").exists():
        capa = json.loads(capa_yol.read_text(encoding="utf-8")).get("p") or []
        pars = metin_paragraflari((kok / "metin" / f"{key}.md").read_text(encoding="utf-8"))
        beyanli = set()
        for pn, p in enumerate(pars):
            if pn >= len(capa):
                break
            cc = cumle_capalari(p["t"], cumle_sonlari(p["t"]), capa[pn])
            il = I.get(str(pn)) or []
            for ci, cl in enumerate(cc):
                i = il[ci] if ci < len(il) else None
                if not cl or not i:
                    continue
                if any(c.get("sekil") or c.get("tablo") not in (None, False) for c in cl):
                    sekil_cumle += 1
                    beyanli.add((str(pn), ci))
                    # görselli sayfada sekil_isareti hep resim/tablo verir; görselsiz sayfada şekil çapası yazar hatasıdır
                    # (metne düşen kabul, lazeri boşa düşen değil)
                    if i["t"] in ("kelime", "sayfa"):
                        H.append(f"K1 P{pn}.C{ci}: şekil çapası var ama lazer {i['t']} (s.{i.get('s')})")
                if any(c.get("madde") for c in cl):
                    madde_say += 1
                    madde_bos += i["t"] in ("kelime", "sayfa")
    if madde_say >= 10 and madde_bos / madde_say > UYDURMA_UST:
        H.append(f"K2 madde çapalarının %{round(100 * madde_bos / madde_say)}'i yazıya düşmüyor (üst sınır "
                 f"%{int(UYDURMA_UST * 100)}): çapa uydurulmuş olabilir (her cümleye madde/M0 basılmasın)")

    # K3–K8: çizimler
    sekil, cizimli, sayfa_say = 0, 0, {}
    for pn, il in I.items():
        for ci, i in enumerate(il):
            zs = (P.get(pn) or {}).get(str(ci)) or []
            gorsel = bool(i) and i["t"] in ("resim", "tablo")
            if gorsel and i["t"] == "resim" and (beyanli is None or (pn, ci) in beyanli):
                sekil += 1
                # yalnız resim cümleleri sayılır; okunabilir tablo yalnız marker ile vurgulanır (H85, K10)
                cizimli += any(z.get("tur") != "sema" for z in zs)
            yer = f"P{pn}.C{ci}"
            if len(zs) > 2:
                H.append(f"K6 {yer}: cümlede {len(zs)} çizim (en çok 2)")
            for z in zs:
                s = z.get("s")
                sayfa_say[s] = sayfa_say.get(s, 0) + 1
                if i and i.get("s") and s != i["s"] and i["t"] != "sayfa":
                    H.append(f"K7 {yer}: çizim s.{s}, lazer s.{i['s']}")
                if z.get("tur") == "sema" and i and i["t"] == "resim":
                    H.append(f"K4 {yer}: resim anlatılırken panel (sema) — görselin üstünde çiz")
                if i and i["t"] == "tablo":
                    H.append(f"K10 {yer}: okunabilir tabloda {z.get('tur')} — tabloda yalnız marker (H85)")
                if z.get("tur") == "akis" and not (i and i["t"] == "resim"):
                    H.append(f"K11 {yer}: resim dışında ok (kelime ↔ kelime ilişkisi çizilmez, H85)")
                yk = z.get("yakin")
                if yk and (not (i and i["t"] == "resim") or _alan(yk) > ZOOM_UST):
                    H.append(f"K12 {yer}: zoom resim dışında ya da sayfanın %{round(100 * _alan(yk))}'i (üst %{int(ZOOM_UST * 100)})")
                if z.get("tur") == "sema" and z.get("duzen"):
                    if z["duzen"] not in DUZENLER:
                        H.append(f"K13 {yer}: panel düzeni '{z['duzen']}' tanımsız (sablonlar.json duzenler)")
                    elif z["duzen"] == "deger":
                        _, ret = SB.coz({**z, "sablon": z.get("sablon") or "deger_karti"})
                        if ret:
                            H.append(f"K13 {yer}: {ret}")
                if z.get("tur") == "akis" and not str(z.get("etiket") or "").strip():
                    H.append(f"K8 {yer}: etiketsiz ok")
                nk = z.get("nokta") or []
                if any(not (0 <= v <= 1) for q in nk for v in q[:2]):
                    H.append(f"K8 {yer}: koordinat 0–1 dışında")
                if z.get("tur") == "kontur":
                    if not 5 <= len(nk) <= 20:
                        H.append(f"K8 {yer}: kontur {len(nk)} nokta (5–20)")
                    if gorsel and nk and i.get("l"):
                        kb = [min(q[0] for q in nk), min(q[1] for q in nk), max(q[0] for q in nk), max(q[1] for q in nk)]
                        rb = i["l"][0]
                        if _alan(rb) > 0 and _kesisim(kb, rb) / _alan(rb) >= TUM_RESIM:
                            H.append(f"K5 {yer}: kontur bütün resmi çevreliyor — anlatılan parçayı dola")
    for s, n in sayfa_say.items():
        if n > 8:
            H.append(f"K6 s.{s}: sayfada {n} çizim (en çok 8)")
    if sekil >= 5 and cizimli / sekil < KAPSAM_ALT:
        H.append(f"K3 şekil cümlelerinin %{round(100 * cizimli / sekil)}'inde görsel üstü çizim var "
                 f"({cizimli}/{sekil}; alt sınır %{int(KAPSAM_ALT * 100)})")
    return H, {"sekil": sekil, "cizimli": cizimli, "sekil_capa": sekil_cumle, "madde": madde_say, "madde_bos": madde_bos}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key", nargs="?")
    ap.add_argument("--kok", default=str(MEDS / "data" / "sesli_anlatim"))
    ap.add_argument("--hepsi", action="store_true")
    a = ap.parse_args()
    kok = Path(a.kok) if Path(a.kok).is_absolute() else MEDS / a.kok
    keys = sorted(p.stem for p in (kok / "isaret").glob("*.json")) if a.hepsi else [a.key]
    toplam = 0
    for k in keys:
        H, o = denetle(k, kok)
        toplam += len(H)
        print(f"{k}: {len(H)} HATA  (şekil {o.get('cizimli', 0)}/{o.get('sekil', 0)} çizimli)")
        for h in H[:25]:
            print("   -", h)
        if len(H) > 25:
            print(f"   … {len(H) - 25} HATA daha")
    print(f"TOPLAM {toplam} HATA")
    return 1 if toplam else 0


if __name__ == "__main__":
    sys.exit(main())
