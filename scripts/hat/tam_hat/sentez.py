#!/usr/bin/env python3
"""Sentez kipi (yönetici açarsa) · PDF'i modele en ucuz yoldan okutma: METİN betikle, GÖRSEL yalnız gereken sayfada (LLM yok).

  python3 scripts/hat/tam_hat/sentez.py <ders klasörü> [--esik 0.04]    # → <klasör>/baglam/sentez.md + sentez.json

Neden (ölçüm 2026-11-17, k2-13, 20 sayfa): standart hatta alt ajan her sayfanın PNG'sini açar (H111; 110 dpi slayt ≈ 1,1–1,6k
token/görsel) — oysa sayfa metni pdftotext ile zaten bedava çıkıyor. Görselin anlam kattığı sayfa (şekil, MR/BT, şema, tablo
resmi) azınlıktır; kalanında görsel = şablon arka planı + metnin fotoğrafı. Bu betik sayfayı sınıflar:
  - şablon arka planı: aynı resim (xref) sayfaların ≥%40'ında tekrar → yok sayılır
  - içerik resmi: şablon dışı, sayfa alanının ≥ --esik kadarını kaplayan resim
  - vektör şema: ≥ 25 çizim yolu (ok/kutu/akış şeması)
  - seyrek metin: < 12 kelime ve içerik resmi var (resim slaytı)
GORSEL=evet sayfalarda model op/s-NNN.png açar; diğerlerinde YALNIZ metni okur.

MarkItDown (microsoft/markitdown, ücretsiz, .venv-markitdown): slayt PDF'inde pdftotext'ten KÖTÜ çıktı (sayfa sınırı yok,
çok sütunlu madde imlerini sahte tabloya çevirir, +%37 gürültü kelime — k2-13 ölçümü). Bu yüzden PDF'te KULLANILMAZ; yalnız
ders klasöründe PDF olmayan ek kaynak (pptx/docx/xlsx/html — ör. öğrenci notu .docx) varsa onu Markdown'a çevirmek için
çağrılır (`ek_kaynak_md`). Kip açılmazsa standart yol (her sayfa PNG) aynen sürer.
"""
from __future__ import annotations
# Konum-bağımsız kök: scripts/kok.py
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
import subprocess
import sys
from pathlib import Path

KOK = _kok.MEDS
PY_CV = KOK / ".venv-ocr/bin/python"          # pymupdf
MARKITDOWN = KOK / ".venv-markitdown/bin/markitdown"
EK_UZANTI = (".pptx", ".docx", ".xlsx", ".html", ".htm", ".epub")
TOKEN_GORSEL = 1300  # 110 dpi slayt PNG'nin yaklaşık görsel tokeni (ölçüm notu: docs/TAM_HAT_HIZLI_AKIS.md §0.0c)

_SINIF = r'''
import json, sys, pymupdf
from collections import Counter
doc = pymupdf.open(sys.argv[1]); esik = float(sys.argv[2])
sayfa = []
tekrar = Counter()
for p in doc:
    xs = {x[0] for x in p.get_images(full=True)}
    tekrar.update(xs)
n = len(doc)
for i, p in enumerate(doc, 1):
    A = p.rect.width * p.rect.height or 1
    icerik = 0.0
    for x in p.get_images(full=True):
        if n >= 4 and tekrar[x[0]] >= max(3, 0.4 * n):
            continue  # şablon arka planı / logo
        for r in p.get_image_rects(x[0]):
            r = r & p.rect
            icerik += max(0.0, r.width * r.height) / A
    sayfa.append({"s": i, "kelime": len(p.get_text().split()), "resim": round(min(icerik, 1.0), 3),
                  "cizim": len(p.get_drawings())})
print(json.dumps(sayfa))
'''


def siniflandir(pdf: Path, esik: float) -> list[dict]:
    r = subprocess.run([str(PY_CV), "-c", _SINIF, str(pdf), str(esik)], capture_output=True, text=True, check=True)
    out = json.loads(r.stdout)
    for s in out:
        neden = []
        if s["resim"] >= esik:
            neden.append(f"içerik resmi %{round(s['resim'] * 100)}")
        if s["cizim"] >= 25:
            neden.append(f"vektör şema ({s['cizim']} yol)")
        if s["kelime"] < 12 and s["resim"] > 0:
            neden.append("seyrek metin")
        s["gorsel"] = bool(neden)
        s["neden"] = ", ".join(neden)
    return out


def temas_sayfalari(klasor: Path, sayfalar: list[int], hedef: Path, n: int = 9) -> list[str]:
    """Aday sayfaları 3x3 küçük resim ızgarasına (temas sayfası) dizer: 9 sayfa ≈ 1 görsel tokeni. Model önce bunlara bakar,
    YALNIZ tanısal görüntü/şema/resim-tablo olan sayfanın tam PNG'sini açar (süs görseli, arka plan, stok resim elenir)."""
    from PIL import Image, ImageDraw
    cikti = []
    for t in range(0, len(sayfalar), n):
        grup = sayfalar[t:t + n]
        W, H = 480, 270
        c = Image.new("RGB", (W * 3, H * ((len(grup) + 2) // 3)), "white")
        ciz = ImageDraw.Draw(c)
        for j, s in enumerate(grup):
            f = klasor / "op" / f"s-{s:02d}.png"
            if not f.exists():
                f = klasor / "op" / f"s-{s:03d}.png"
            im = Image.open(f).convert("RGB")
            im.thumbnail((W - 4, H - 4))
            x, y = (j % 3) * W, (j // 3) * H
            c.paste(im, (x + 2, y + 2))
            ciz.rectangle([x, y, x + 46, y + 26], fill="black")
            ciz.text((x + 6, y + 6), f"s{s}", fill="yellow")
        ad = f"temas_{t // n + 1}.png"
        c.save(hedef / ad)
        cikti.append(ad)
    return cikti


def ek_kaynak_md(klasor: Path, hedef: Path) -> list[str]:
    """PDF dışı ek kaynakları MarkItDown ile .md'ye çevirir (yoksa sessiz geçer)."""
    yazilan = []
    if not MARKITDOWN.exists():
        return yazilan
    for f in sorted(klasor.iterdir()):
        if f.suffix.lower() in EK_UZANTI:
            r = subprocess.run([str(MARKITDOWN), str(f)], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                o = hedef / f"ek_{f.stem}.md"
                o.write_text(r.stdout, encoding="utf-8")
                yazilan.append(o.name)
    return yazilan


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--esik", type=float, default=0.04, help="içerik resmi alan eşiği (sayfa oranı)")
    a = ap.parse_args()
    k = a.klasor.resolve()
    pdf, say = k / "orijinal.pdf", k / "sayfalar.json"
    if not pdf.exists() or not say.exists():
        print("HATA: orijinal.pdf + sayfalar.json gerekli (önce hazirlik.py)", file=sys.stderr)
        return 2
    metin = json.loads(say.read_text(encoding="utf-8"))
    sinif = siniflandir(pdf, a.esik)
    b = k / "baglam"
    b.mkdir(exist_ok=True)
    g = [s for s in sinif if s["gorsel"]]
    satir = [f"# Sentez kaynağı — {len(sinif)} sayfa, görsel açılacak {len(g)} sayfa",
             "Kural: metin aşağıda; YALNIZ `GÖRSEL: aç` yazan sayfada `op/s-NNN.png` aç. Diğer sayfaların PNG'sini AÇMA.",
             "TUR KURALI (ölçüldü, §0.0c): bu dosya + temas sayfalarını TEK mesajda paralel oku; seçilen PNG'leri TEK mesajda "
             "paralel oku; çıktıları tek mesajda yaz. Sayfa sayfa sırayla okuma, ara doğrulama okuması yapma.", ""]
    for s in sinif:
        etiket = f"GÖRSEL: aç op/s-{s['s']:02d}.png ({s['neden']})" if s["gorsel"] else "GÖRSEL: gerekmez"
        satir += [f"## Sayfa {s['s']} · {etiket}", (metin.get(str(s["s"])) or "").strip() or "(metin yok)", ""]
    (b / "sentez.md").write_text("\n".join(satir), encoding="utf-8")
    ek = ek_kaynak_md(k, b)
    temas = temas_sayfalari(k, [s["s"] for s in g], b) if g else []
    satir[1:1] = [f"Önce `baglam/{' , baglam/'.join(temas)}` (temas sayfası, aday sayfaların küçük resmi) bak; yalnız tanısal "
                  "görüntü (BT/MR/grafi/histoloji), şema, akış, resim olarak gömülü tablo olan sayfanın tam PNG'sini aç; süs/arka plan/"
                  "stok resim için AÇMA. Seçimini `baglam/sentez_secim.json` = {\"ac\": [sayfa…], \"gerekce\": {…}} yaz."] if temas else []
    (b / "sentez.md").write_text("\n".join(satir), encoding="utf-8")
    ozet = {"sayfa": len(sinif), "gorsel_sayfa": len(g), "temas": temas,
            "gorsel_token_tahmini_standart": len(sinif) * TOKEN_GORSEL,
            "gorsel_token_tahmini_sentez_ust_sinir": (len(temas) + len(g)) * TOKEN_GORSEL, "ek_md": ek, "sayfalar": sinif}
    (b / "sentez.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"sentez: {len(g)}/{len(sinif)} sayfada görsel · tahmini görsel token {ozet['gorsel_token_tahmini_standart']} → "
          f"≤{ozet['gorsel_token_tahmini_sentez_ust_sinir']} (temas {len(temas)} + seçilen)" + (f" · ek md: {', '.join(ek)}" if ek else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
