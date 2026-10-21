#!/usr/bin/env python3
"""Son Prova partlarını sesli ders biçimine derler (TBG kampı derle.py'nin genel sürümü).

Girdi: parca/<part-key>/aNN.json (dogrula.py 0 HATA), plan.json
Çıktı: cikti/<part-key>/
  <key>.md        — "# Başlık", "@@ N · Aşama" (aşama girişi), "@@ N.M · Alt başlık", paragraflar (sesli ders metni)
  hizalama.json   — {deckId, dosyalar:[özet PDF], paragraflar[{dosya, sayfa, guven, sayfalar[], dosyalar[]}], kaynak[]}
                     sayfa numaraları KIRPILMIŞ özet PDF'in sayfalarıdır; kaynak[i] = özet PDF'in (i+1). sayfasının aslı
  vurgu.json      — çıkmış/önemli cümleler (sesli ders vurgusu)
  kirp.json       — pdf_kirp.mjs girdisi: kaynak PDF'ler ve sayfa sırası + sayfa üstü etiketleri
  asamalar.json   — aşama → ders, başlık, paragraf aralığı, aşama sonu soruları, check-up adayları (site verisine girer)
Kullanım: python3 meds_temp/son_prova/derle.py [part-key ...]   (boşsa parçası olan tüm partlar)
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parent
ROOT = KOK.parents[1]
MEDS = ROOT / "meds"
sys.path.insert(0, str(KOK))
from dogrula import sinirlar  # noqa: E402

PLAN = json.loads((KOK / "plan.json").read_text(encoding="utf-8"))
BRANS_KLASOR = {"patoloji": "Tıbbi Patoloji", "enfeksiyon": "Enfeksiyon Hastalıkları", "genetik": "Tıbbi Genetik",
                "uroloji": "Üroloji", "halksagligi": "Halk Sağlığı", "kadindogum": "Kadın Hastalıkları ve Doğum",
                "farmakoloji": "Tıbbi Farmakoloji"}
KISA_BRANS = {"patoloji": "Patoloji", "enfeksiyon": "Enfeksiyon", "genetik": "Genetik", "uroloji": "Üroloji",
              "halksagligi": "Halk Sağlığı", "kadindogum": "Kadın Doğum", "farmakoloji": "Farmakoloji"}


def klasor(part: dict) -> str:
    return part.get("drive_klasor") or BRANS_KLASOR[part["brans"]]


def kisa(part: dict) -> str:
    return part.get("kisa") or KISA_BRANS[part["brans"]]

ONEMLI = re.compile(r"^(Burası önemli|Çıkmış sorularda)|çıkmış sorularda|çıkmış soruda|sınavda soru|sınavda sorul")
DIKKAT = re.compile(r"^(Dikkat edin|Vaka kökünde|Karıştırılmasın)")

# TBG kampından taşınan genetik metninde kalabilecek "BRCA bir" biçimi → BRCA1 (yalnız genetik partlarında)
SAYI = {"bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9, "on": 10,
        "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50, "altmış": 60, "yetmiş": 70, "seksen": 80, "doksan": 90}
GEN = ["SOX", "BRCA", "FGFR", "SF", "WNT", "MLH", "FOXL", "DAX", "WT", "MSH", "PMS", "CDK", "FMR", "RSPO", "BAP", "TSC",
       "TP", "STK", "CDH", "HOXB", "CHEK", "PALB", "HER", "PAX", "EMX", "LHX", "BCL", "MDM", "SFRP", "ERBB"]
SAYI_RE = r"(?:doksan|seksen|yetmiş|altmış|elli|kırk|otuz|yirmi|on)(?: (?:bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz))?|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz"


def gen_duzelt(t: str) -> str:
    kok = "|".join(sorted(GEN, key=len, reverse=True))
    return re.sub(rf"\b({kok}) ({SAYI_RE})\b(?![a-zçğıöşü])", lambda m: f"{m.group(1)}{sum(SAYI[w] for w in m.group(2).split())}", t)


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


_SESLI = {d["key"]: d["baslik"] for d in json.loads((MEDS / "data/sesli_anlatim/dersler.json").read_text(encoding="utf-8"))}


def ders_adi(d: dict) -> str:
    """Ekranda ve PDF şeridinde gösterilen ders adı: sesli dersin başlığı (düzgün yazım), yoksa PDF adı"""
    k = Path(d.get("sesli_anlatim") or "").stem
    return _SESLI.get(k) or d["ad"]


def ders_no(ad: str) -> str:
    m = re.match(r"\s*(\d+)\s*\)", ad)
    return m.group(1) if m else ""


def kaynak_pdf(part: dict, ders: dict) -> str:
    """Drive'daki kaynak PDF'in göreli yolu (meds_downloads/drive_root'a göre). Kurul 2+: plan_kurul.py `drive_yol` verir."""
    if ders.get("drive_yol") and (ROOT / "meds_downloads/drive_root" / ders["drive_yol"]).exists():
        return ders["drive_yol"]
    p = Path(f"Kurul {PLAN['kurul']}") / klasor(part) / (ders.get("drive_ad") or ders["pdf_ad"])
    tam = ROOT / "meds_downloads/drive_root" / p
    if not tam.exists():
        # Drive adları NFD gelebilir
        klasor = tam.parent
        hedef = nfc(ders.get("drive_ad") or ders["pdf_ad"])
        ad_anahtar = lambda s: re.sub(r"[^a-zçğıöşü0-9]+", "", re.sub(r"^\s*\d+\s*\)", "", nfc(s).lower()))
        adaylar = [f for f in klasor.iterdir() if nfc(f.name) == hedef] or \
            [f for f in klasor.iterdir() if f.suffix.lower() == ".pdf" and ad_anahtar(f.name) == ad_anahtar(hedef)]
        if len(adaylar) == 1:
            return str(Path(f"Kurul {PLAN['kurul']}") / klasor(part) / adaylar[0].name)
        if not adaylar and ders.get("pdf_yok"):
            return f"@metin:{ders['pdf_metin']}"
        raise SystemExit(f"kaynak PDF yok ya da belirsiz: {tam} ({[a.name for a in adaylar]})")
    return str(p)


def derle(part: dict) -> dict:
    key = part["key"]
    dosyalar = sorted((KOK / "parca" / key).glob("a*.json"))
    if not dosyalar:
        raise SystemExit(f"{key}: aşama dosyası yok")
    asamalar_ham = [json.loads(p.read_text(encoding="utf-8")) for p in dosyalar]
    dersler = {d["slayt_kod"]: d for d in part["dersler"]}
    sira = {d["slayt_kod"]: i for i, d in enumerate(part["dersler"])}
    genetik = part["brans"] == "genetik"

    # 1) kullanılan slayt sayfaları → kırpılmış PDF sırası (ders sırası, sayfa sırası)
    kullan = set()
    for a in asamalar_ham:
        ks = [a.get("giris_k")] + [c.get("k") for b in a["bolumler"] for par in b["paragraflar"] for c in par]
        for k in ks:
            if k:
                kod, s = k.split(":")
                kullan.add((kod, int(s)))
    sayfalar = sorted(kullan, key=lambda x: (sira[x[0]], x[1]))
    yeni = {x: i + 1 for i, x in enumerate(sayfalar)}

    baslik_part = f"{kisa(part)} · {part['baslik']}"
    md = [f"# {baslik_part}", ""]
    hz = []
    vurgu = {}
    asamalar = []
    son = None

    def paragraf(cumleler):
        nonlocal son
        ts, ss = [], []
        for c in cumleler:
            t = gen_duzelt(c["t"]) if genetik else c["t"]
            ts.append(t)
            k = c.get("k")
            if k:
                kod, s = k.split(":")
                son = yeni[(kod, int(s))]
            if son is None:
                raise SystemExit(f"{key}: ilk cümlenin slaytı yok: {t[:60]}")
            ss.append(son)
        m = " ".join(ts)
        if len(sinirlar(m)) != len(ts):
            raise SystemExit(f"{key}: cümle sınırı kaydı: {m[:90]}")
        v, bas = [], 0
        for t in ts:
            o = 3 if ONEMLI.search(t) else 2 if DIKKAT.search(t) else 0
            if o:
                v.append([bas, bas + len(t), "c", o])
            bas += len(t) + 1
        if v:
            vurgu[str(len(hz))] = v
        md.extend([m, ""])
        hz.append({"dosya": 0, "sayfa": ss[0], "guven": 1, "sayfalar": ss, "dosyalar": [0] * len(ss)})

    for n, a in enumerate(asamalar_ham, 1):
        ilk = len(hz)
        md.append(f"@@ {n} · {a['baslik']}")
        paragraf([{"t": a["giris"], "k": a.get("giris_k")}])
        for bi, b in enumerate(a["bolumler"], 1):
            md.append(f"@@ {n}.{bi} · {gen_duzelt(b['baslik']) if genetik else b['baslik']}")
            for par in b["paragraflar"]:
                paragraf(par)
        d = dersler[a["ders"]]
        asamalar.append({
            "no": n, "baslik": a["baslik"], "ders": a["ders"], "dersAd": ders_adi(d), "dersNo": ders_no(d["pdf_ad"]),
            "p": [ilk, len(hz) - 1],
            "sayfa": [min(x for p in hz[ilk:] for x in p["sayfalar"]), max(x for p in hz[ilk:] for x in p["sayfalar"])],
            "sorular": a["sorular"], "checkup": a["checkup"],
            "cikmis": len(a.get("karsilanan_cikmis") or []),
        })

    out = KOK / "cikti" / key
    out.mkdir(parents=True, exist_ok=True)
    metin = "\n".join(md).rstrip() + "\n"
    (out / f"{key}.md").write_text(metin, encoding="utf-8")
    pdf_ad = f"Son Prova - {kisa(part)}{' ' + str(part['no']) if part['key'][-1].isdigit() else ''} - özet slaytlar.pdf"
    kaynak = []
    for kod, s in sayfalar:
        d = dersler[kod]
        kaynak.append({"kod": kod, "no": ders_no(d["pdf_ad"]), "ad": ders_adi(d), "s": s})
    hizalama = {
        "deckId": f"k1p-{key}",
        "dosyalar": [{"path": f"Son Prova/{key}.pdf", "name": pdf_ad, "pages": len(sayfalar)}],
        "paragraflar": hz,
        "sayfaKaynak": kaynak,
        "kaynak": "son_prova/derle.py",
    }
    (out / "hizalama.json").write_text(json.dumps(hizalama, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "vurgu.json").write_text(json.dumps({"surum": 1, "p": vurgu}, ensure_ascii=False), encoding="utf-8")
    # pdf_kirp.mjs girdisi
    kaynaklar = {}
    for kod in {k for k, _ in sayfalar}:
        kaynaklar[kod] = kaynak_pdf(part, dersler[kod])
    (out / "kirp.json").write_text(json.dumps({
        "cikti": f"data/son_prova/pdf/{key}.pdf", "ad": pdf_ad,
        "kaynaklar": kaynaklar,
        "sayfalar": [{"kod": k, "s": s, "etiket": f"{kisa(part)} {dersler[k].get('no') or ders_no(dersler[k]['pdf_ad'])}) {ders_adi(dersler[k])} · slayt {s}"}
                     for k, s in sayfalar],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "asamalar.json").write_text(json.dumps(asamalar, ensure_ascii=False, indent=1), encoding="utf-8")
    kelime = sum(len(x.split()) for x in md if x and not x.startswith(("#", "@@")))
    print(f"{key}: {len(asamalar)} aşama · {len(hz)} paragraf · {kelime} kelime ≈ {kelime / PLAN['dakika_kelime']:.0f} dk · "
          f"özet PDF {len(sayfalar)} sayfa ({len(kaynaklar)} ders PDF'inden)")
    return {"key": key, "asamalar": asamalar, "kelime": kelime, "sayfa": len(sayfalar)}


def main():
    istek = sys.argv[1:]
    for p in PLAN["partlar"]:
        if istek and p["key"] not in istek:
            continue
        if not istek and not list((KOK / "parca" / p["key"]).glob("a*.json")):
            continue
        derle(p)


if __name__ == "__main__":
    main()
