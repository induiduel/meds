#!/usr/bin/env python3
"""Öğrenci sentez notları (hocanın sözlü vurgularını yapay zekâyla derleyen arkadaş Drive'ı) → Markdown → vurgu birimleri.

LLM YOK (kural 20 dışı). Artımlı: aynı Drive kimliği + aynı boyut bir kez işlenir (tekrar yok).

Aşamalar (hepsi `calistir` ile sırayla; her biri ayrı da çağrılabilir):
  cek     Drive ağacını tarar, Kurul N PDF'lerini indirir      → meds_temp/ogrenci_sentez/pdf/<yol>
  cevir   MarkItDown ile SAYFA SAYFA Markdown (sayfa sınırı korunur; `<!-- sayfa N -->`)
          + pdftotext ile sözcük kapsama kapısı (MarkItDown sözcük kaçırırsa HATA)  → md/<yol>.md
  ayikla  Hoca vurgu ifadeleri (sözlük: VURGU) içeren her BLOK — başlık yolu + tam paragraf/madde/tablo satırı;
          ardışık bağlam satırı kesilmez → vurgu/<yol>.json
  esle    PDF → ders kimliği (src/data/dersler/k<N>.json); belirsizse HATA, elle `eslesme.json` ile sabitlenir
  kapi    Kayıpsızlık: md'deki tetik sayısı == çıkarılan birimlerdeki tetik sayısı; kapsama ≥ %98; eşlemesiz PDF yok
  yayinla vurgu → meds_temp/ogrenci_sentez/ders/<k2-xx>.json (tam hat `baglam.py` buradan okur)
  fark    yayımlanmış sesli derslerde anlatımda karşılığı zayıf birimler → fark/<k2-xx>.md (revizyon adayı)

Kullanım:  python3 scripts/uretim/ogrenci_sentez/sentez.py calistir [--kurul 2] [--zorla]
           python3 scripts/uretim/ogrenci_sentez/sentez.py durum | fark [--esik 0.5]
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

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

MEDS = _kok.MEDS
KLASOR_ID = "1rDVhXMvhgGkU0f71ZHPs6n-qDx5zPry5"
IS = MEDS.parent / "meds_temp" / "ogrenci_sentez"
MD_PY = MEDS / ".venv-markitdown/bin/python"
ESLESME = Path(__file__).resolve().parent / "eslesme.json"   # elle sabitlenen PDF→ders (git'te)
DEFTER = IS / "defter.json"                                     # artımlılık: id → boyut/sha

sys.path.insert(0, str(MEDS / "scripts/uretim/ogrenci_drive"))

# ── Vurgu sözlüğü (katlanmış küçük harf, aksansız eşleşme). Geniş tutulur: kaçırmak > fazla almak.
VURGU = [
    r"sorar[ıi]m", r"soraca[gğ][ıi]m", r"sorabilir[ıi]m", r"sordum", r"soruldu", r"sorulur", r"sorulabilir", r"sorulmu[sş]",
    r"soru (?:gelir|gelebilir|[cç][ıi]kar|[cç][ıi]kabilir)", r"s[ıi]navda", r"s[ıi]nav (?:vurgu|tuza[gğ]|sorusu|i[cç]in)",
    r"[cç][ıi]km[ıi][sş]", r"\b[cç][ıi]kar\b", r"[cç][ıi]kabilir", r"\btus(?:'?ta|'?da|ta|da|'?un)?\b", r"tuza[gğ]", r"tuzak",
    r"hoca(?:n[ıi]n|m[ıi]z)? ?(?:vurgu|[oö]zellikle|dedi|s[oö]yledi|belirtti|uyard[ıi]|alt[ıi]n[ıi] [cç]izdi)", r"hoca vurgusu",
    r"vurgula", r"[oö]nemli", r"[cç]ok [oö]nemli", r"kritik", r"mutlaka", r"kesinlikle", r"dikkat", r"unutmay", r"ezber",
    r"buraya bak", r"buralara bak", r"\bbak[ıi]n\b", r"[oö][gğ]renin", r"\bbilin\b", r"bilmeniz", r"bilmelisiniz", r"akl[ıi]n[ıi]zda",
    r"alt[ıi]n[ıi] [cç]iz", r"alt[ıi] [cç]izil", r"y[ıi]ld[ıi]zl[ıi]", r"klasik soru", r"favori", r"\bspot",
    r"⭐", r"❗", r"‼", r"⚠", r"🔥", r"🎯", r"📌", r"💡", r"🚨",
]
VURGU_RE = re.compile("|".join(f"(?:{v})" for v in VURGU), re.I)


def katla(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace("İ", "i").replace("I", "ı")
    return s.lower()


def yaz_json(p: Path, v) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    t.replace(p)


def oku_json(p: Path, var=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else var


# ── cek
def cek(kurul: int, zorla: bool) -> list[dict]:
    import ogrenci_drive as OD
    dosyalar = []

    def r(i, yol):
        for x in OD.drive_klasor_listele(i):
            p = yol + [x["name"]]
            if "folder" in x["mime"]:
                r(x["id"], p)
            elif x["mime"] == "application/pdf":
                dosyalar.append({"id": x["id"], "yol": "/".join(p)})
    r(KLASOR_ID, [])
    if not dosyalar:
        raise SystemExit("HATA: Drive klasörü boş/okunamadı — eski indirmeler korunur, hiçbir şey ezilmedi")
    secili = [d for d in dosyalar if d["yol"].startswith(f"Kurul{kurul}/")]
    yaz_json(IS / "agac.json", dosyalar)
    for d in secili:
        hedef = IS / "pdf" / d["yol"]
        OD.dosya_indir(d["id"], hedef, zorla=zorla)
        if not hedef.exists() or hedef.read_bytes()[:4] != b"%PDF":
            raise SystemExit(f"HATA: {d['yol']} PDF değil/inmedi (Drive izin sayfası?)")
    print(f"cek: Kurul{kurul} {len(secili)} PDF (Drive toplam {len(dosyalar)})")
    return secili


# ── cevir
def _sayfa(pdf: Path) -> int:
    o = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", o).group(1))


def _sozcuk(t: str) -> list[str]:
    return re.findall(r"[0-9a-zçğıöşüâîû]{3,}", katla(t))


def _ocr_gerekirse(pdf: Path, yol: str, n: int) -> Path:
    """jsPDF/html2canvas notları sayfa RESMİdir (metin katmanı yok). Sayfa başına <40 sözcük → ocrmypdf (tur+eng, CPU)."""
    ham = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
    if len(_sozcuk(ham)) >= 40 * n:
        return pdf
    hedef = IS / "ocr" / yol
    if hedef.exists() and hedef.stat().st_mtime >= pdf.stat().st_mtime:
        return hedef
    hedef.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ocrmypdf", "-q", "--force-ocr", "-l", "tur+eng", "--jobs", "4", "--output-type", "pdf",
                    str(pdf), str(hedef)], check=True, env={**__import__("os").environ, "CUDA_VISIBLE_DEVICES": ""})
    return hedef


SON = re.compile(r"[.!?:;)\]»”\"]\s*$")
ALTBILGI = re.compile(r"(?i)gizli / ki[sş]isel [cç]al[ıi][sş]ma notu|standart: gfm|med-yield|haz[ıi]rlanm[ıi][sş]t[ıi]r\.?$|"
                      r"^- kurul \(|^©? ?ders: |hazirlik serisi|haz[ıi]rl[ıi]k seri|birebir entegre$")
MADDE = re.compile(r"^\s*(?:[»«•*◦▪●e]|[eos](?=\s)|\d{1,2}[.)])\s+")  # OCR madde imleri: » « * e o s → "- "


def _baslik_mi(t: str) -> bool:
    t = t.strip().lstrip("|").strip()
    harf = [c for c in t if c.isalpha()]
    return 3 <= len(t) <= 140 and len(harf) >= 4 and sum(c.isupper() for c in harf) / len(harf) > 0.8


def _pdftotext_md(pdf: Path, n: int) -> list[str]:
    """Okuma sırası korunur; boş satır = paragraf, madde imi = yeni madde, BÜYÜK HARF satır = başlık. Sözcük düşürülmez."""
    out = []
    for i in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True).stdout
        L = []
        onceki = ""
        for sat in t.replace("\f", "").splitlines():
            if not sat.strip():
                L.append(""); continue
            devam = bool(onceki) and not SON.search(onceki) and len(onceki.split()) > 4
            onceki = sat.strip()
            if _baslik_mi(sat) and not devam:
                L += ["", "## " + sat.strip().lstrip("|").strip(), ""]
            elif MADDE.match(sat):
                L += ["", "- " + MADDE.sub("", sat, 1).strip()]
            else:
                L.append(sat.strip())
        out.append(f"<!-- sayfa {i} -->\n" + re.sub(r"\n{3,}", "\n\n", "\n".join(L)).strip() + "\n")
    return out


def _markitdown_md(pdf: Path, n: int) -> list[str]:
    parca = []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdfseparate", str(pdf), f"{td}/s-%d.pdf"], check=True)
        for i in range(1, n + 1):
            o = subprocess.run([str(MD_PY), "-I", "-m", "markitdown", f"{td}/s-{i}.pdf"],
                               capture_output=True, text=True, check=True).stdout
            parca.append(f"<!-- sayfa {i} -->\n{o.strip()}\n")
    return parca


def _kapsama(ham_kume: set, metin: str) -> float:
    return len(ham_kume & set(_sozcuk(metin))) / max(1, len(ham_kume))


def cevir(secili: list[dict], zorla: bool) -> None:
    """MarkItDown birincil; sözcük kapsaması <%98 ise (OCR katmanında satırları boşluksuz birleştirir — H-kaydı)
    okuma sıralı pdftotext→Markdown kullanılır. Hangisi seçildiyse defterde `motor` olarak yazılır."""
    if not MD_PY.exists():
        raise SystemExit(f"HATA: MarkItDown yok ({MD_PY}); `python3 -m venv .venv-markitdown && .venv-markitdown/bin/pip install 'markitdown[pdf]'`")
    defter = oku_json(DEFTER, {})
    for d in secili:
        pdf = IS / "pdf" / d["yol"]
        sha = hashlib.sha256(pdf.read_bytes()).hexdigest()[:16]
        md = (IS / "md" / d["yol"]).with_suffix(".md")
        e = defter.get(d["id"], {})
        if not zorla and md.exists() and e.get("sha") == sha and e.get("kapsama", 0) >= 0.98:
            continue
        n = _sayfa(pdf)
        kay = _ocr_gerekirse(pdf, d["yol"], n)
        ham = set(_sozcuk(subprocess.run(["pdftotext", str(kay), "-"], capture_output=True, text=True).stdout))
        parca = _markitdown_md(kay, n)
        k_md = _kapsama(ham, "\n".join(parca))
        motor = "markitdown"
        if k_md < 0.98:
            parca, motor = _pdftotext_md(kay, n), "pdftotext"
        metin = "\n".join(parca)
        kapsama = _kapsama(ham, metin)
        md.parent.mkdir(parents=True, exist_ok=True)
        md.write_text(f"# {Path(d['yol']).stem}\n<!-- kaynak: drive {d['id']} · {n} sayfa · {motor}"
                      f"{' · OCR' if kay != pdf else ''} -->\n\n{metin}", encoding="utf-8")
        defter[d["id"]] = {"yol": d["yol"], "sha": sha, "sayfa": n, "motor": motor, "ocr": kay != pdf,
                           "kapsama": round(kapsama, 4), "markitdown_kapsama": round(k_md, 4),
                           "eksik_sozcuk": sorted(ham - set(_sozcuk(metin)))[:40]}
        print(f"cevir: {d['yol']} {n} s · {motor} kapsama %{kapsama*100:.1f} (markitdown %{k_md*100:.1f})")
    yaz_json(DEFTER, defter)


# ── ayikla: blok = başlık yolu altındaki paragraf / madde (alt satırlarıyla); vurgulu başlığın TÜM bölümü alınır
def _yarim(cur: list[str]) -> bool:
    """Blok cümle ortasında bitiyorsa (OCR boş satırı / sayfa sonu) sonraki düz satırla birleşir; madde/başlık birleşmez.
    Kısa etiket satırları (≤4 sözcük, tablo hücresi) yarım sayılmaz."""
    if not cur:
        return False
    son = cur[-1].strip()
    return bool(son) and not SON.search(son) and len(" ".join(cur).split()) > 6


def bloklar(md: str) -> list[dict]:
    out, yol, sayfa, cur, cur_s = [], "", 1, [], 1
    bolum_vurgu = False

    def kapat():
        nonlocal cur
        if cur and any(x.strip() for x in cur):
            out.append({"sayfa": cur_s, "yol": yol, "metin": "\n".join(cur).strip(), "bolum_vurgu": bolum_vurgu})
        cur = []
    for sat in md.splitlines():
        m = re.match(r"<!-- sayfa (\d+) -->", sat)
        if m:
            sayfa = int(m.group(1))
            if not _yarim(cur):
                kapat()
            continue
        if sat.startswith("<!--") or (sat.startswith("# ") and sayfa == 1 and not out and not cur):
            continue
        h = re.match(r"#{1,6}\s+(.*)", sat)
        if h:
            kapat()
            yol = h.group(1).strip()
            bolum_vurgu = bool(VURGU_RE.search(katla(yol)))
            out.append({"sayfa": sayfa, "yol": yol, "metin": sat.strip(), "baslik": True, "bolum_vurgu": bolum_vurgu})
            continue
        if not sat.strip():
            if not _yarim(cur):
                kapat()
            continue
        if (sat.startswith("- ") or sat.lstrip().startswith("|")) and cur:
            kapat()
        if not cur:
            cur_s = sayfa
        cur.append(sat)
    kapat()
    return out


def ayikla(secili: list[dict]) -> dict:
    ozet = {}
    for d in secili:
        md = (IS / "md" / d["yol"]).with_suffix(".md")
        metin = md.read_text(encoding="utf-8")
        bl = bloklar(metin)
        birim = []
        for b in bl:
            t = VURGU_RE.findall(katla(b["metin"]))
            if ALTBILGI.search(katla(b["metin"])) and not re.search(r"(?i)hoca|tuza|sorul", b["metin"]):
                continue   # kapak/altbilgi (ör. "TUS HAZIRLIK SERİSİ", "Gizli/Kişisel Çalışma Notu"): bilgi değil
            if t or b.get("bolum_vurgu"):
                b["tetik"] = sorted({x.strip() for x in t}) or ["(bölüm başlığı vurgulu)"]
                b["id"] = "OS" + hashlib.sha1((d["id"] + b["metin"]).encode()).hexdigest()[:8]
                birim.append(b)
        # kayıpsızlık: tüm md'deki tetik sayısı (yorum satırları hariç) == birimlerdeki
        top = sum(len(VURGU_RE.findall(katla(b["metin"]))) for b in bl
                  if not (ALTBILGI.search(katla(b["metin"])) and not re.search(r"(?i)hoca|tuza|sorul", b["metin"])))
        # bağımsız sayım: ham md'deki tetik ≥ blok toplamı olmalı (blok bölücü metin düşürmüyor mu?)
        govde = "\n".join(x for x in metin.splitlines() if not x.startswith("<!--") and not x.startswith("# "))
        if len(VURGU_RE.findall(katla(govde))) != sum(len(VURGU_RE.findall(katla(b["metin"]))) for b in bl):
            raise SystemExit(f"HATA: blok bölücü metin kaybetti: {d['yol']}")
        alinan = sum(len(VURGU_RE.findall(katla(b["metin"]))) for b in birim)
        yaz_json((IS / "vurgu" / d["yol"]).with_suffix(".json"),
                 {"kaynak": d["yol"], "drive": d["id"], "tetik_md": top, "tetik_birim": alinan, "birimler": birim})
        ozet[d["yol"]] = (len(birim), top, alinan)
        print(f"ayikla: {d['yol']} {len(birim)} birim · tetik {alinan}/{top}")
    return ozet


# ── esle
def _norm(s: str) -> set[str]:
    s = re.sub(r"^\d+\)\s*", "", katla(Path(s).stem))
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return {w[:5] for w in re.findall(r"[a-z0-9]{3,}", s)} - {"hasta", "yakla", "ilacl", "bozuk", "hasta"}


def esle(secili: list[dict], kurul: int) -> dict:
    dersler = json.loads((MEDS / f"src/data/dersler/k{kurul}.json").read_text(encoding="utf-8"))
    dersler = dersler if isinstance(dersler, list) else dersler.get("dersler", [])
    sabit = oku_json(ESLESME, {})
    sonuc, sorun = {}, []
    for d in secili:
        if d["yol"] in sabit:
            sonuc[d["yol"]] = sabit[d["yol"]]; continue
        brans = _norm(d["yol"].split("/")[1])
        a = _norm(d["yol"])
        puan = []
        for x in dersler:
            b = _norm(x["konu"])
            ort = len(a & b) / max(1, len(a | b))
            if brans & _norm(x["brans"]) or katla(d["yol"].split("/")[1])[:4] in katla(x["brans"]):
                ort += 0.15
            puan.append((round(ort, 3), x["id"], x["konu"]))
        puan.sort(reverse=True)
        if puan[0][0] >= 0.5 and puan[0][0] - puan[1][0] >= 0.2:
            sonuc[d["yol"]] = [puan[0][1]]
        else:
            sorun.append((d["yol"], puan[:3]))
    for y, p in sorun:
        print(f"esle BELİRSİZ: {y} → adaylar {p}  (eslesme.json'a elle yaz)")
    yaz_json(IS / "eslesme_sonuc.json", sonuc)
    return {"sonuc": sonuc, "sorun": sorun}


# ── kapı + yayın
def kapi(secili: list[dict], ozet: dict, es: dict) -> int:
    hata = 0
    defter = oku_json(DEFTER, {})
    for d in secili:
        k = defter.get(d["id"], {}).get("kapsama", 0)
        if k < 0.98:
            print(f"HATA kapsama %{k*100:.1f} < 98: {d['yol']} eksik: {defter[d['id']].get('eksik_sozcuk')[:12]}"); hata += 1
        n, top, al = ozet.get(d["yol"], (0, 0, 0))
        if top != al:
            print(f"HATA tetik kaybı {al}/{top}: {d['yol']}"); hata += 1
    for y, _ in es["sorun"]:
        print(f"HATA eşlemesiz: {y}"); hata += 1
    print(f"kapi: {hata} HATA")
    return hata


def yayinla(secili: list[dict], es: dict) -> None:
    ders: dict[str, list] = {}
    for d in secili:
        for key in es["sonuc"].get(d["yol"], []):
            v = oku_json((IS / "vurgu" / d["yol"]).with_suffix(".json"))
            ders.setdefault(key, []).append({"kaynak": d["yol"], "md": str((IS / "md" / d["yol"]).with_suffix(".md")),
                                             "birimler": v["birimler"]})
    for key, k in ders.items():
        yaz_json(IS / "ders" / f"{key}.json", {"ders": key, "tur": "ogrenci_sentez_hoca_sozlu",
                                               "uyari": "Öğrenci+YZ derlemesi: hocanın sözlü vurgusu İDDİASI. Bilgi yalnız 2026-27 slaytında karşılığı varsa kullanılır; çıkmış damgası DEĞİL.",
                                               "kaynaklar": k})
    print(f"yayinla: {len(ders)} ders → {IS/'ders'}")


# ── fark: yayımlanmış sesli dersin anlatımında karşılığı ZAYIF olan sentez birimleri (LLM yok, kök örtüşmesi).
# Revizyon adayı listesidir; H531 gereği anlatım baştan yazılmaz, yalnız ilgili slayt kısmen revize edilir.
DUR = set("bunun icin olan olarak daha veya gibi ancak sonra kadar ozellikle durumda sonucu neden olur nedeniyle iliskili".split())


def _kok(t: str) -> set[str]:
    t = unicodedata.normalize("NFKD", katla(t)).encode("ascii", "ignore").decode()
    return {w[:5] for w in re.findall(r"[a-z0-9]{5,}", t)} - {w[:5] for w in DUR}


def fark(kurul: int, esik: float) -> None:
    for p in sorted((IS / "ders").glob(f"k{kurul}-*.json")):
        key = p.stem
        an = sorted((MEDS / "data/sesli_anlatim/metin").glob(f"{key}-*.md"))
        if not an:
            continue  # ders henüz yayımlanmadı → tam hat baglam'dan zaten okur
        ak = _kok(an[0].read_text(encoding="utf-8"))
        eksik = []
        for k in oku_json(p)["kaynaklar"]:
            for b in k["birimler"]:
                if b.get("baslik"):
                    continue
                kk = _kok(re.sub(VURGU_RE, " ", katla(b["metin"])))
                if len(kk) < 3:
                    continue
                o = len(kk & ak) / len(kk)
                if o < esik:
                    eksik.append((round(o, 2), b))
        L = [f"# {key} — anlatımda karşılığı zayıf sentez birimleri (örtüşme < {esik}; {len(eksik)} birim)",
             f"> anlatım: {an[0].relative_to(MEDS)} · Önce 2026-27 slaytında karşılığı var mı bak; yoksa EKLEME.", ""]
        for o, b in sorted(eksik, key=lambda x: x[0]):
            L.append(f"- ({o}) ös{b['sayfa']} «{b['yol'][:60]}» [{','.join(b['tetik'])[:40]}]: {re.sub(r'\\s+', ' ', b['metin'])}")
        (IS / "fark").mkdir(exist_ok=True)
        (IS / "fark" / f"{key}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print(f"fark: {key} {len(eksik)} zayıf birim → fark/{key}.md")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komut", choices=("calistir", "durum", "fark"))
    ap.add_argument("--kurul", type=int, default=2)
    ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--esik", type=float, default=0.5, help="fark: kök örtüşme eşiği")
    a = ap.parse_args()
    if a.komut == "durum":
        for p in sorted((IS / "ders").glob("*.json")):
            v = oku_json(p)
            print(p.stem, sum(len(k["birimler"]) for k in v["kaynaklar"]), "birim ·", ", ".join(k["kaynak"] for k in v["kaynaklar"]))
        return 0
    if a.komut == "fark":
        fark(a.kurul, a.esik)
        return 0
    secili = cek(a.kurul, a.zorla)
    cevir(secili, a.zorla)
    ozet = ayikla(secili)
    es = esle(secili, a.kurul)
    h = kapi(secili, ozet, es)
    yayinla(secili, es)   # eşlenenler yayınlanır; HATA varsa çıkış 1 (eşlemesizler beklemede)
    fark(a.kurul, 0.5)
    return 1 if h else 0


if __name__ == "__main__":
    sys.exit(main())
