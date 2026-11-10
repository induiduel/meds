#!/usr/bin/env python3
"""Ek modül PDF kitapçıkları: src/data/ek_moduller/<modül>/ → public/ek_moduller/<modül>/pdf/*.pdf (başsız Chrome).

Dört kitapçık (index.json `pdf` listesindeki adlarla): ders kitapçığı (resimli, 16 konu), spot bilgiler, sınav öncesi özet,
soru kitapçığı (sorular + cevap anahtarı + açıklamalı çözümler). Ekran metni basılır; okuma (`ses`) metni basılmaz.
Kullanım (çalışma dizini meds/): python3 scripts/ek_modul/pdf.py --modul yuruyus-kampcilik [--yalniz ders,spot,sinav,soru] [--html]
"""
from __future__ import annotations
import html, json, re, subprocess, sys, tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]

CSS = """
@page { size: A4; margin: 17mm 16mm 18mm; @bottom-center { content: counter(page); font: 600 8.5pt Lato, sans-serif; color: #8a9490; } }
@page kapak { margin: 0; @bottom-center { content: none; } }
* { box-sizing: border-box; }
html { font: 10.4pt/1.55 Lato, 'Noto Sans', 'Liberation Sans', sans-serif; color: #1E2A2E; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; }
h1, h2, h3, h4, p, ul, ol, figure { margin: 0; padding: 0; }
b, strong { font-weight: 800; }
.kapak { page: kapak; height: 297mm; padding: 22mm 20mm; background: #F4EEE2; display: flex; flex-direction: column; break-after: page; }
.kapak .ust { font: 800 9.5pt Lato; letter-spacing: .16em; text-transform: uppercase; color: #2F5D50; }
.kapak img { width: 100%; border-radius: 9mm; margin: 14mm 0 12mm; }
.kapak h1 { font: 900 38pt/1.05 Lato; color: #1E2A2E; letter-spacing: -.01em; }
.kapak .alt { font: 500 15pt/1.35 Lato; color: #2F5D50; margin-top: 4mm; }
.kapak .ack { margin-top: 6mm; max-width: 125mm; color: #46524f; font-size: 11pt; }
.kapak .dip { margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; font: 700 9pt Lato; color: #6b7672; }
.kapak .dip b { font: 900 13pt Lato; color: #2F5D50; }
.icindekiler { break-after: page; }
.icindekiler h2 { font: 900 22pt Lato; margin-bottom: 7mm; }
.icindekiler ol { list-style: none; columns: 2; column-gap: 9mm; }
.icindekiler li { break-inside: avoid; margin-bottom: 5.5mm; }
.icindekiler .b { display: flex; gap: 3mm; align-items: baseline; font: 800 11.5pt Lato; color: #2F5D50; }
.icindekiler .b i { font-style: normal; font-weight: 900; color: #D9865B; }
.icindekiler .k { padding-left: 6.5mm; color: #46524f; font-size: 9.8pt; }
.nasil { margin-top: 8mm; padding: 5mm 6mm; border-radius: 4mm; background: #EEF3EE; font-size: 9.8pt; color: #33403d; }
.konu { break-before: page; }
.konu-ust { display: flex; gap: 5mm; align-items: flex-start; margin-bottom: 5mm; }
.konu-no { flex: none; width: 15mm; height: 15mm; border-radius: 4.5mm; background: #2F5D50; color: #fff; display: grid; place-items: center; font: 900 15pt Lato; }
.konu-ust small { display: block; font: 800 8pt Lato; letter-spacing: .14em; text-transform: uppercase; color: #D9865B; }
.konu-ust h2 { font: 900 19pt/1.15 Lato; }
.konu-ust p { color: #55615e; margin-top: 1mm; }
figure.g { margin: 0 0 5mm; break-inside: avoid; }
figure.g img { width: 100%; border-radius: 5mm; display: block; }
figure.g.kucuk { width: 72%; margin-left: auto; margin-right: auto; }
figure.g figcaption { font-size: 8.4pt; color: #7a8582; text-align: center; margin-top: 1.5mm; }
.bolum { break-inside: avoid; margin-bottom: 4.5mm; padding-left: 5mm; border-left: 1.1mm solid #CFE0CF; }
.bolum h3 { font: 800 12pt/1.25 Lato; color: #2F5D50; margin-bottom: 1.2mm; }
.bolum h3 i { font-style: normal; color: #D9865B; margin-right: 1.5mm; }
.md p { margin-bottom: 1.6mm; }
.md ul { list-style: none; margin-bottom: 1.6mm; }
.md li { position: relative; padding-left: 4.2mm; margin-bottom: .9mm; }
.md li::before { content: ""; position: absolute; left: .6mm; top: .62em; width: 1.5mm; height: 1.5mm; border-radius: 50%; background: #7FA387; }
.vurgu { padding: 2.4mm 3.5mm; border-radius: 2.5mm; background: #FBF1D6; font-weight: 700; }
.vurgu.note { background: #E4EEF1; }
.akilda { break-inside: avoid; display: flex; gap: 5mm; align-items: center; padding: 4.5mm 5.5mm; border-radius: 4mm; background: #24384F; color: #fff; margin: 5mm 0; }
.akilda .kod { flex: none; font: 900 16pt Lato; letter-spacing: .08em; color: #F2C14E; }
.akilda b { display: block; font-size: 10.6pt; }
.akilda span { font-size: 9.2pt; opacity: .86; }
.yy { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; break-inside: avoid; margin-bottom: 5mm; }
.yy > div { padding: 4mm 4.5mm; border-radius: 4mm; background: #EEF3EE; }
.yy > div.yapma { background: #F8E9E4; }
.yy h4 { font: 900 10pt Lato; letter-spacing: .08em; text-transform: uppercase; color: #2F5D50; margin-bottom: 1.5mm; }
.yy .yapma h4 { color: #C8553D; }
.yy li { list-style: none; position: relative; padding-left: 5mm; font-size: 9.6pt; margin-bottom: .8mm; }
.yy li::before { content: "✓"; position: absolute; left: 0; font-weight: 900; color: #2F5D50; }
.yy .yapma li::before { content: "✕"; color: #C8553D; }
.kutu-b { font: 900 10pt Lato; letter-spacing: .1em; text-transform: uppercase; color: #D9865B; margin: 5mm 0 2mm; break-after: avoid; }
.spotlar { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm 4mm; }
.spotlar li { break-inside: avoid; padding: 2.6mm 3.5mm; border-radius: 3mm; background: #F4EEE2; font-size: 9.6pt; }
.et { break-inside: avoid; padding: 4mm 5mm; border-radius: 4mm; border: .4mm solid #E4D8C3; margin-bottom: 3.5mm; font-size: 9.6pt; }
.et h4 { font: 800 10.6pt Lato; margin-bottom: 1.5mm; }
.et ol, .et ul { padding-left: 5mm; }
.et .cvp { margin-top: 2mm; padding-top: 1.6mm; border-top: .3mm dashed #cdbfa6; color: #55615e; font-size: 8.8pt; }
.esle { display: grid; grid-template-columns: 1fr 1fr; gap: 1mm 6mm; }
.bant { break-before: page; break-after: avoid; padding: 6mm 7mm; border-radius: 5mm; background: #2F5D50; color: #fff; margin-bottom: 6mm; }
.bant small { font: 800 8.5pt Lato; letter-spacing: .16em; text-transform: uppercase; opacity: .8; }
.bant h2 { font: 900 20pt/1.15 Lato; }
.bant p { opacity: .9; margin-top: 1mm; }
.bant + .konu { break-before: avoid; }
.soru { break-inside: avoid; margin-bottom: 4.2mm; }
.soru .kok { font-weight: 700; }
.soru .kok i { font-style: normal; font-weight: 900; color: #2F5D50; margin-right: 1.5mm; }
.soru ol { list-style: none; margin-top: 1mm; padding-left: 6mm; }
.soru ol li { margin-bottom: .3mm; }
.soru ol li b { color: #55615e; margin-right: 1.2mm; }
.iki { columns: 2; column-gap: 9mm; }
.anahtar { display: grid; grid-template-columns: repeat(8, 1fr); gap: 1.5mm; margin-bottom: 5mm; }
.anahtar span { padding: 1.4mm 0; text-align: center; border-radius: 2mm; background: #F4EEE2; font-size: 9.4pt; }
.anahtar b { color: #2F5D50; }
.coz { break-inside: avoid; margin-bottom: 2.8mm; font-size: 9.5pt; }
.coz b.n { color: #2F5D50; margin-right: 1.2mm; }
.h-set { font: 900 13pt Lato; color: #2F5D50; margin: 6mm 0 2.5mm; break-after: avoid; }
.part { break-inside: avoid; margin-bottom: 6mm; padding: 5mm 6mm; border-radius: 4.5mm; background: #F7F3EA; }
.part h3 { font: 900 13pt Lato; color: #2F5D50; margin-bottom: 2mm; }
.part h3 i { font-style: normal; color: #D9865B; margin-right: 2mm; }
"""

e = html.escape


def kalin(s: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", e(s))


def md(s: str) -> str:
    out, liste = [], []
    def bosalt():
        if liste:
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in liste) + "</ul>")
            liste.clear()
    for x in (y.strip() for y in s.split("\n")):
        if not x:
            continue
        if x.startswith("- "):
            liste.append(kalin(x[2:])); continue
        bosalt()
        m = re.match(r">\s*\[!(IMPORTANT|NOTE)\]\s*(.*)", x)
        out.append(f'<p class="vurgu {"note" if m.group(1) == "NOTE" else ""}">{kalin(m.group(2))}</p>' if m else f"<p>{kalin(re.sub(r'^>\\s*', '', x))}</p>")
    bosalt()
    return '<div class="md">' + "".join(out) + "</div>"


def belge(baslik: str, govde: str) -> str:
    return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{e(baslik)}</title><style>{CSS}</style></head><body>{govde}</body></html>'


def kapak(m: dict, tur: str, ack: str, gorsel_kok: str) -> str:
    return (f'<section class="kapak"><div class="ust">{e(m["tur"])} · Kurul {m["kurul"]}</div><img src="{gorsel_kok}/{m["kapak"]}" alt="">'
            f'<h1>{e(m["ad"])}</h1><div class="alt">{e(tur)}</div><p class="ack">{e(ack)}</p>'
            f'<div class="dip"><span>Ek modüller</span><b>MeDSor</b></div></section>')


def etkinlik(x: dict) -> str:
    t = x["tur"]
    if t == "dogru_yanlis":
        ic = "<ol>" + "".join(f"<li>{e(f['metin'])}</li>" for f in x["ifadeler"]) + "</ol>"
        cvp = " · ".join(f"{i}. {'Doğru' if f['dogru'] else 'Yanlış'}" for i, f in enumerate(x["ifadeler"], 1))
    elif t == "sirala":
        import random
        r = random.Random(x["baslik"]); k = x["adimlar"][:]; r.shuffle(k)
        if k == x["adimlar"]: k = k[1:] + k[:1]
        ic = f"<p>{e(x['soru'])}</p><ul>" + "".join(f"<li>{e(a)}</li>" for a in k) + "</ul>"
        cvp = " → ".join(x["adimlar"])
    else:
        import random
        r = random.Random(x["baslik"]); sag = [c["sag"] for c in x["ciftler"]]; r.shuffle(sag)
        ic = '<div class="esle">' + "".join(f"<span>{i}. {e(c['sol'])}</span><span>{chr(96 + i)}) {e(s)}</span>" for i, (c, s) in enumerate(zip(x["ciftler"], sag), 1)) + "</div>"
        cvp = " · ".join(f"{i}–{chr(97 + sag.index(c['sag']))}" for i, c in enumerate(x["ciftler"], 1))
    return f'<div class="et"><h4>{e(x["baslik"])}</h4>{ic}<p class="cvp"><b>Cevap:</b> {e(cvp)}</p></div>'


def ders_html(m, basliklar, g) -> str:
    konular = [(b, k) for b in basliklar for k in b["konular"]]
    ic = '<section class="icindekiler"><h2>İçindekiler</h2><ol>' + "".join(
        f'<li><div class="b"><i>{b["no"]}</i>{e(b["baslik"])}</div>' + "".join(f'<div class="k">{e(k["id"])} · {e(k["baslik"])}</div>' for k in b["konular"]) + "</li>"
        for b in basliklar) + ('</ol><p class="nasil"><b>Nasıl çalışılır?</b> Her konu kısa bölümlerden oluşur: önce notu oku, görsele bak, '
                               'akılda tutma kodunu ve yap–yapma listesini ezberle, sonra spot bilgileri ve küçük etkinlikleri çöz. '
                               'Sesli anlatım, sesli çözümlü sorular ve hocanın çalışma soruları sitede: Ders çalış › Ek modüller.</p></section>')
    out = [kapak(m, "Ders kitapçığı", m["aciklama"], g), ic]
    for b, k in konular:
        s = [f'<section class="konu"><div class="konu-ust"><div class="konu-no">{e(k["id"])}</div><div><small>{b["no"]}. {e(b["baslik"])}</small>'
             f'<h2>{e(k["baslik"])}</h2><p>{e(k["ozet"])}</p></div></div>',
             f'<figure class="g"><img src="{g}/{k["gorsel"]}" alt="{e(k["gorsel_alt"])}"></figure>']
        for i, bl in enumerate(k["bolumler"], 1):
            s.append(f'<div class="bolum"><h3><i>{i}</i>{e(bl["baslik"])}</h3>{md(bl["ekran"])}</div>')
        a = k["akilda"]
        s.append(f'<div class="akilda"><div class="kod">{e(a["kod"])}</div><div><b>{e(a["acilim"])}</b><span>{e(a["not"])}</span></div></div>')
        s.append('<div class="yy"><div><h4>Yap</h4><ul>' + "".join(f"<li>{e(x)}</li>" for x in k["yap"]) + '</ul></div><div class="yapma"><h4>Yapma</h4><ul>'
                 + "".join(f"<li>{e(x)}</li>" for x in k["yapma"]) + "</ul></div></div>")
        for eg in k.get("ek_gorseller") or []:
            s.append(f'<figure class="g kucuk"><img src="{g}/{eg["dosya"]}" alt=""><figcaption>{e(eg["alt"])}</figcaption></figure>')
        s.append('<div class="kutu-b">Spot bilgiler</div><ul class="spotlar">' + "".join(f"<li>{kalin(x['metin'])}</li>" for x in k["spotlar"]) + "</ul>")
        s.append('<div class="kutu-b">Kendini dene</div>' + "".join(etkinlik(x) for x in k["etkinlikler"]))
        out.append("".join(s) + "</section>")
    return belge(f'{m["ad"]} — Ders kitapçığı', "".join(out))


def spot_html(m, basliklar, g) -> str:
    out = [kapak(m, "Spot bilgiler", "Her konunun en akılda kalması gereken tek cümlelik bilgileri. Sınavdan önce on dakikada göz gezdir.", g)]
    for b in basliklar:
        out.append(f'<h2 class="h-set">{b["no"]}. {e(b["baslik"])}</h2>')
        for k in b["konular"]:
            out.append(f'<div class="kutu-b">{e(k["id"])} · {e(k["baslik"])}</div><ul class="spotlar">' + "".join(f"<li>{kalin(x['metin'])}</li>" for x in k["spotlar"])
                       + f'<li><b>{e(k["akilda"]["kod"])}</b> — {e(k["akilda"]["acilim"])}</li></ul>')
    return belge(f'{m["ad"]} — Spot bilgiler', "".join(out))


def sinav_html(m, so, g) -> str:
    out = [kapak(m, "Sınav öncesi özet", so.get("giris") or "Bütün dersin son tekrarı: başlık başlık en çok sorulabilecek bilgiler.", g)]
    for i, p in enumerate(so["partlar"], 1):
        out.append(f'<div class="part"><h3><i>{i}</i>{e(re.sub(r"^\d+\.\s*", "", p["baslik"]))}</h3>{md(p["ekran"])}</div>')
    return belge(f'{m["ad"]} — Sınav öncesi özet', "".join(out))


def soru_html(m, basliklar, genel, g) -> str:
    setler = [(f'{k["id"]} · {k["baslik"]}', k["sorular"]) for b in basliklar for k in b["konular"]]
    if genel:
        setler.append(("Genel tekrar soruları (bütün konular)", genel))
    n = sum(len(s) for _, s in setler)
    out = [kapak(m, "Soru kitapçığı", f"{n} soru: konu soruları yalnız o konuya kadar öğretilenleri, genel tekrar soruları bütün dersi yoklar. "
                                      "Sonda cevap anahtarı ve açıklamalı çözümler var.", g)]
    for ad, sorular in setler:
        out.append(f'<h2 class="h-set">{e(ad)}</h2><div class="iki">' + "".join(
            f'<div class="soru"><p class="kok"><i>{q["no"]}.</i>{e(q["kok"])}</p><ol>' + "".join(f"<li><b>{h})</b>{e(v)}</li>" for h, v in q["secenekler"].items()) + "</ol></div>"
            for q in sorular) + "</div>")
    out.append('<div class="bant"><small>Soru kitapçığı</small><h2>Cevap anahtarı ve çözümler</h2></div>')
    for ad, sorular in setler:
        out.append(f'<h2 class="h-set">{e(ad)}</h2><div class="anahtar">' + "".join(f"<span>{q['no']}. <b>{q['dogru']}</b></span>" for q in sorular) + '</div><div class="iki">'
                   + "".join(f'<p class="coz"><b class="n">{q["no"]}. {q["dogru"]}</b>{e(q["cozum"])}</p>' for q in sorular) + "</div>")
    return belge(f'{m["ad"]} — Soru kitapçığı', "".join(out))


def main() -> int:
    a = sys.argv[1:]
    modul = a[a.index("--modul") + 1]
    yalniz = a[a.index("--yalniz") + 1].split(",") if "--yalniz" in a else ["ders", "spot", "sinav", "soru"]
    veri = KOK / "src/data/ek_moduller"
    m = next(x for x in json.loads((veri / "index.json").read_text())["moduller"] if x["id"] == modul)
    kok = veri / modul
    basliklar = sorted((json.loads(f.read_text()) for f in kok.glob("b*.json")), key=lambda b: b["no"])
    so = json.loads((kok / "sinav_oncesi.json").read_text()) if (kok / "sinav_oncesi.json").exists() else None
    genel = json.loads((kok / "genel_sorular.json").read_text())["sorular"] if (kok / "genel_sorular.json").exists() else []
    gorsel = (KOK / "public/ek_moduller" / modul).as_uri()
    cikti = KOK / "public/ek_moduller" / modul
    uret = {"ders": lambda: ders_html(m, basliklar, gorsel), "spot": lambda: spot_html(m, basliklar, gorsel),
            "sinav": (lambda: sinav_html(m, so, gorsel)) if so else None, "soru": lambda: soru_html(m, basliklar, genel, gorsel)}
    for p in m["pdf"]:
        if p["id"] not in yalniz or not uret.get(p["id"]):
            continue
        hedef = cikti / p["dosya"]
        hedef.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=tempfile.gettempdir()) as f:
            f.write(uret[p["id"]]())
        if "--html" in a:
            print(p["id"], f.name)
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                        f"--print-to-pdf={hedef}", Path(f.name).as_uri()], check=True, capture_output=True, timeout=180)
        print(f"{p['id']}: {hedef.relative_to(KOK)} ({hedef.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
