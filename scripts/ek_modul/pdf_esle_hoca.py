#!/usr/bin/env python3
"""Hocanın çalışma soruları · "PDF ile" sesli çözüm: h-/hc- kliplerini çözümlü soru kitapçığına bağlar.

Kitapçık (`ekFoyBelge.ts::cozumluBelge`, pdf id `cozumlu`) setleri hocanın sırasıyla basar; her soru bir blok:
numara satırı (sol kenarda "N."), soru kökü, (çoktan seçmelide) şıklar, açık yeşil zeminli cevap + çözüm kutusu.
Blok sayfa arasında bölünmez (break-inside: avoid). Her klip için:
  s  sayfa, k  sorunun bütün bloğu (kırpılan bölge), l  cümle başına satır kutuları, c  [[cümlenin başladığı saniye, l sırası]]
Cümle → satır: soru klibinde 1. cümle kök (doğru–yanlışta 2. cümle de), şık cümleleri kendi şık satırı; çözüm klibinde
çoktan seçmelinin 1. cümlesi doğru şık, kalan cümleler çözüm kutusunun satırlarına karakter oranıyla dağıtılır (kutu metni
konuşmayla aynı sırada ilerler). Cümle zamanı pdf_esle.py::cumle_zamanlari ile (duraklama, yalnız CPU, LLM yok).

Çıktı: src/data/ek_moduller/<modül>/hoca_pdf_esle.json  {"pdf", "bayt", "klip": {"h-bosluk-1": {...}, "hc-bosluk-1": {...}}}
Kitapçık (foy_pdf.mts --cozumlu) ya da hoca sesleri yeniden üretilirse betik yeniden çalıştırılır; özet (`v`) tutmayan
klipte ekran eşlemeyi kullanmaz.

Kullanım (çalışma dizini meds/): .venv-ocr/bin/python scripts/ek_modul/pdf_esle_hoca.py --modul yuruyus-kampcilik [--kuru]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts/ek_modul"))
sys.path.insert(0, str(KOK / "scripts/sesli_anlatim"))
import ses as S  # noqa: E402
from pdf_esle import cumle_zamanlari  # noqa: E402

KUTU_RENK = (0.933, 0.953, 0.933)  # .q .c zemini #EEF3EE


def kutu_birlesik(kutular: list[list[float]]) -> list[float]:
    return [min(x[0] for x in kutular), min(x[1] for x in kutular), max(x[2] for x in kutular), max(x[3] for x in kutular)]


def bloklar(yol: Path):
    """Belge sırasıyla soru blokları: (sayfa, no, kök satırları, şık satırları [(harf, [kutu…])], kutu satırları [(kutu, metin)])."""
    import pymupdf
    out = []
    for sn, sayfa in enumerate(pymupdf.open(yol), 1):
        w, h = sayfa.rect.width, sayfa.rect.height
        zemin = [d["rect"] for d in sayfa.get_drawings() if d.get("fill") and all(abs(a - b) < 0.01 for a, b in zip(d["fill"], KUTU_RENK))]
        satir = []
        for b in sayfa.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(sp["text"] for sp in l["spans"])
                if t.strip():
                    x0, y0, x1, y1 = l["bbox"]
                    ic = any(r.x0 - 1 <= x0 and x1 <= r.x1 + 1 and r.y0 - 1 <= (y0 + y1) / 2 <= r.y1 + 1 for r in zemin)
                    satir.append(([round(x0 / w, 4), round(y0 / h, 4), round(x1 / w, 4), round(y1 / h, 4)], t, ic))
        satir.sort(key=lambda s: (round((s[0][1] + s[0][3]) / 2, 3), s[0][0]))
        bas = [i for i, s in enumerate(satir) if s[0][0] < 0.1 and re.match(r"\d+\.", s[1].strip()) and not s[2]]
        for j, i in enumerate(bas):
            son = bas[j + 1] if j + 1 < len(bas) else len(satir)
            parca = satir[i:son]
            # bloktan sonra gelen set başlığı (sonraki sayfa başı değilse) bloğa girmesin: kutudan sonrası kesilir
            kutu_son = max((k for k, s in enumerate(parca) if s[2]), default=len(parca) - 1)
            parca = parca[:kutu_son + 1]
            kok, siklar, kutu = [], [], []
            for s in parca:
                if s[2]:
                    kutu.append((s[0], s[1]))
                elif m := re.match(r"\s*([A-E])\)", s[1]):
                    siklar.append((m.group(1), [s[0]]))
                elif siklar and s[0][0] > 0.12:
                    # şık metni iki satıra taştıysa: aynı sütundaki son şıkka eklenir
                    sut = min(siklar, key=lambda x: abs(x[1][0][0] - s[0][0]) + (0 if x[1][-1][3] <= s[0][1] + 0.001 else 9))
                    sut[1].append(s[0])
                else:
                    kok.append(s[0])
            out.append((sn, int(re.match(r"\d+", parca[0][1].strip()).group()), kok, siklar, kutu))
    return out


def oranla(kutu: list[tuple[list[float], str]], cumleler: list[str]) -> list[list[list[float]]]:
    """Cümleleri kutu satırlarına karakter oranıyla dağıtır: her cümle, kutu metninde kendi payına düşen satırları alır."""
    uz = [len(t) for _, t in kutu]
    T, L = sum(uz) or 1, sum(len(c) for c in cumleler) or 1
    sinir, a = [], 0
    for _, t in kutu:
        sinir.append((a / T, (a + len(t)) / T))
        a += len(t)
    out, b = [], 0
    for c in cumleler:
        x0, x1 = b / L, (b + len(c)) / L
        b += len(c)
        sec = [kutu[k][0] for k, (s0, s1) in enumerate(sinir) if s0 < x1 - 1e-6 and s1 > x0 + 1e-6]
        out.append(sec or [kutu[-1][0]])
    return out


def main() -> int:
    a = sys.argv[1:]
    modul = a[a.index("--modul") + 1]
    veri = KOK / "src/data/ek_moduller" / modul
    ozet = next(m for m in json.loads((veri.parent / "index.json").read_text())["moduller"] if m["id"] == modul)
    pdf = next((p["dosya"] for p in ozet["pdf"] if p["id"] == "cozumlu"), None)
    if not pdf:
        raise SystemExit("HATA: index.json'da çözümlü soru kitapçığı (pdf id 'cozumlu') yok")
    pdf_yol = KOK / "public/ek_moduller" / modul / pdf
    hoca = json.loads((veri / "hoca_sorulari.json").read_text())
    klip = json.loads((veri / "klip.json").read_text())
    K = S.klipler(modul)
    ses_kok = KOK / "data/ek_moduller/ses" / modul
    bl = bloklar(pdf_yol)
    sira = [(st, q) for st in hoca["setler"] for q in st["sorular"]]
    if len(bl) != len(sira):
        raise SystemExit(f"HATA: kitapçıkta {len(bl)} soru bloğu var, hoca_sorulari.json'da {len(sira)} soru")

    out, eksik, sinir_n, oturan_n = {}, [], 0, 0
    for (sn, no, kok, siklar, kutu), (st, q) in zip(bl, sira):
        if no != q["no"]:
            raise SystemExit(f"HATA: sıra kaydı: kitapçıkta {no}, beklenen {st['id']}-{q['no']} (s. {sn})")
        if not kutu or not kok:
            raise SystemExit(f"HATA: {st['id']}-{no}: kök ya da çözüm kutusu bulunamadı (s. {sn})")
        tum = kok + [k for _, ks in siklar for k in ks] + [k for k, _ in kutu]
        blok = kutu_birlesik(tum)
        harf = {h: ks for h, ks in siklar}
        if st["tur"] == "cs" and set(harf) != set(q["secenekler"]):
            raise SystemExit(f"HATA: {st['id']}-{no}: şıklar kitapçıkta {sorted(harf)}, veride {sorted(q['secenekler'])}")
        for ad in (f"h-{st['id']}-{no}", f"hc-{st['id']}-{no}"):
            cum = K.get(ad)
            mp3 = ses_kok / f"{ad}.mp3"
            if not cum or ad not in klip or not mp3.exists():
                eksik.append(ad)
                continue
            if ad.startswith("h-"):
                if st["tur"] == "cs":
                    l = [kok] + [harf[h] for h in q["secenekler"]]
                else:
                    l = [kok] * len(cum)
            elif st["tur"] == "cs":
                l = [harf[q["dogru"]]] + (oranla(kutu, cum[1:]) if len(cum) > 1 else [])
            else:
                l = oranla(kutu, cum)
            if len(l) != len(cum):
                raise SystemExit(f"HATA: {ad}: {len(cum)} cümle, {len(l)} satır grubu")
            t, _sure, oturan = cumle_zamanlari(mp3, cum) if len(cum) > 1 else ([0.0], 0, 0)
            sinir_n += len(cum) - 1
            oturan_n += oturan
            out[ad] = {"v": klip[ad]["v"], "s": sn, "k": blok, "l": l, "c": [[tj, j] for j, tj in enumerate(t)]}
    print(f"{modul}: {len(out)} hoca klibi eşlendi ({len(bl)} soru), {oturan_n}/{sinir_n} cümle sınırı duraklamaya oturdu"
          + (f"; sesi olmayan {len(eksik)} klip atlandı: {eksik[:5]}" if eksik else ""))
    if "--kuru" not in a:
        (veri / "hoca_pdf_esle.json").write_text(json.dumps({"pdf": pdf, "bayt": pdf_yol.stat().st_size, "klip": out}, ensure_ascii=False, separators=(",", ":")))
        print(f"yazıldı: {veri / 'hoca_pdf_esle.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
