#!/usr/bin/env python3
"""Son Prova (Kurul 1) planı: part → ders PDF'leri, kelime hedefleri, yazar kaynakları ve soru havuzu katalogları.

Çıktı: plan.json, havuz/<kod>.md (yazar ajanın okuyacağı çıkmış + soru havuzu kataloğu)
Kullanım: python3 meds_temp/son_prova/plan.py
"""
import json
import re
import unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parent
ROOT = KOK.parents[1]
MEDS = ROOT / "meds"
TEMP = ROOT / "meds_temp"
KURUL = 1
DAKIKA_KELIME = 112  # EMA 1× ≈ 112 kelime/dk (TBG kampı ölçümü)

# Sınav soru dağılımı (fakülte duyurusu, Kurul 1 teorik)
SINAV = {
    "patoloji": ("Tıbbi Patoloji", 34),
    "enfeksiyon": ("Enfeksiyon Hastalıkları", 22),
    "genetik": ("Tıbbi Genetik", 12),
    "uroloji": ("Üroloji", 12),
    "halksagligi": ("Halk Sağlığı", 10),
    "kadindogum": ("Kadın Hastalıkları ve Doğum", 6),
    "farmakoloji": ("Tıbbi Farmakoloji", 4),
}
# part: (key, branş, başlık, ders kodları (PDF sırası), toplam kelime hedefi, yazar grupları)
PARTLAR = [
    ("k1-95-blok-ozet-patoloji-1", "patoloji", "Tümör biyolojisi, karsinogenez, tümör immünolojisi ve evreleme (Patoloji 16–20)",
     ["16", "17", "18", "19", "20"], 9200, [["16", "17", "18"], ["19", "20"]]),
    ("k1-96-blok-ozet-patoloji-2", "patoloji", "Böbrek ve mesane patolojisi (Patoloji 21–27)",
     ["21", "22", "23", "24", "25", "26", "26b"], 9800, [["21", "22", "23"], ["24", "25", "26", "26b"]]),
    ("k1-97-blok-ozet-patoloji-3", "patoloji", "Kadın genital, gebelik, meme ve erkek genital patolojisi (Patoloji 28–35)",
     ["28", "39", "30", "31", "32", "33", "34", "35"], 10400, [["28", "39", "30", "31"], ["32", "33", "34", "35"]]),
]


# Ders başına elle düzeltmeler (2026-10-21 denetimi): slayt metni bu yılın PDF'iyle aynı olmalı
DUZELT = {
    "e11": {"pdf_metin": "meds_temp/son_prova/pdf_metin_e11_2026.md", "sayfa": 52,
            "pdf_ad": "11)Bağışıklığı Baskılanmış Hastalarda Enfeksiyonlar.pdf",
            "not": "2026 dersi Uz. Dr. Merve Kaçar; eski (Begüm Şahin) slayt metni KULLANILMAZ"},
    "h06": {"drive_ad": "6)Türkiyede Sağlık Hizmetlerinin Sunumu.pdf"},
    "h07": {"pdf_yok": True},  # PDF Drive'da paylaşılmadı: özet PDF'te slayt metni sayfaları
}
# hizalaması (tek PDF'i) olmayan dersler
ELLE = {("enfeksiyon", "e11"): "k1-47-bagisikligi-baskili-hastalarda-enfeksiyon", ("halksagligi", "h06"): "k1-63-turkiye-de-saglik-hizmetleri",
        ("halksagligi", "h07"): "k1-06-gebelik-ve-emzirme-doneminde-beslenme", ("patoloji", "35"): "k1-65-meme-kanseri-ve-molekuler-tipleri"}


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def anahtar(s: str) -> str:
    s = nfc(s).lower()
    s = re.sub(r"^\s*\d+\s*\)", "", s)
    s = re.sub(r"\.pdf$", "", s)
    return re.sub(r"[^a-zçğıöşü0-9]+", "", s)


def pdf_listesi(b: str) -> list[dict]:
    if b == "patoloji":
        return json.loads((TEMP / "patoloji_onem/pdf_liste.json").read_text(encoding="utf-8"))
    return json.loads((TEMP / f"spot_cozucu/{b}/pdf_liste.json").read_text(encoding="utf-8"))


def kaynak_kod(b: str, kod: str) -> str:
    """Slayt atfında kullanılan kod: patoloji 07 → p07, diğerleri olduğu gibi (e05, u03 …)."""
    return f"p{kod}" if b == "patoloji" else kod


def pdf_metin(b: str, kod: str) -> Path:
    return TEMP / ("patoloji_onem/pdf_metin" if b == "patoloji" else f"spot_cozucu/{b}/pdf_metin") / f"{kod}.md"


def sesli_anahtarlar() -> dict[str, str]:
    """Drive PDF adı anahtarı → Kurul 1 sesli anlatım anahtarı (hizalama dosyalarından)."""
    out = {}
    for p in (MEDS / "data/sesli_anlatim/hizalama").glob("k1-*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        fs = d.get("dosyalar") or []
        if len(fs) == 1 and p.stem != "k1-70-tbg-sinav-kampi":
            out.setdefault(anahtar(fs[0].get("name", "")), p.stem)
    return out


def cikmislar(b: str, kod: str) -> list[dict]:
    if b == "patoloji":
        d = json.loads((TEMP / "patoloji_onem/cikmis_pdf.json").read_text(encoding="utf-8"))
        return d.get(kod.lstrip("0") if kod != "26b" else "26b", d.get(kod, []))
    p = TEMP / f"spot_cozucu/{b}/cikmis/{kod}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def havuz(b: str, kod: str) -> list[dict]:
    out = []
    d = MEDS / f"src/data/{b}_cozucu"
    dosyalar = [d / f"{kod}.json"] if (d / f"{kod}.json").exists() else sorted(d.glob(f"{kod}-*.json"))
    for f in dosyalar:
        j = json.loads(f.read_text(encoding="utf-8"))
        for q in j["sorular"]:
            out.append({"ref": f"{b}/{f.stem}#{q['no']}", **q})
    return out


def kisalt(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    sesli = sesli_anahtarlar()
    notlar = sorted((ROOT / "meds_database_v2/ders_notlari_k1/notlar").glob("*.md"))
    plan = {"kurul": KURUL, "dakika_kelime": DAKIKA_KELIME, "sinav": {b: {"ad": a, "soru": n} for b, (a, n) in SINAV.items()}, "partlar": []}
    for key, b, baslik, kodlar, hedef, gruplar in PARTLAR:
        liste = {x["kod"]: x for x in pdf_listesi(b)}
        dersler = []
        for kod in kodlar:
            x = liste[kod]
            cik = cikmislar(b, kod)
            hv = havuz(b, kod)
            sk = ELLE.get((b, kod)) or sesli.get(anahtar(x["ad"]))
            no = re.match(r"k1-(\d+)-", sk or "")
            notf = [str(n.relative_to(ROOT)) for n in notlar if no and n.name.startswith(f"{int(no.group(1)):02d}_")]
            sayfa = len(re.findall(r"^=== SAYFA \d+", pdf_metin(b, kod).read_text(encoding="utf-8"), re.M))
            dersler.append({
                "kod": kod, "slayt_kod": kaynak_kod(b, kod), "ad": re.sub(r"^\s*\d+\s*\)\s*|\.pdf$|['’]", "", nfc(x["ad"])).strip(),
                "pdf_ad": nfc(x["ad"]), "sayfa": sayfa or x["sayfa"], "cikmis": len(cik), "havuz": len(hv),
                "pdf_metin": str(pdf_metin(b, kod).relative_to(ROOT)),
                "sesli_anlatim": f"meds/data/sesli_anlatim/metin/{sk}.md" if sk else None,
                "ders_notu": notf[0] if notf else None,
                "onem": f"meds/src/data/{b}_onem/{kod}.json",
                "havuz_katalog": f"meds_temp/blok_ozet/havuz/{kaynak_kod(b, kod)}.md",
                **DUZELT.get(kaynak_kod(b, kod), {}),
            })
            # katalog
            md = [f"# {nfc(x['ad'])} — slayt kodu {kaynak_kod(b, kod)} ({sayfa} sayfa)", "",
                  f"## Çıkmış sorular ({len(cik)}) — her birinin bilgisi metinde geçmeli", ""]
            for c in cik:
                sec = c.get("secenekler") or {}
                md.append(f"- **{c.get('id')}** · {c.get('sinav', '')} · {kisalt(c.get('kok', ''), 400)}")
                md.append("  " + " | ".join(f"{h}) {kisalt(v, 90)}" for h, v in sorted(sec.items())) + f" → **{c.get('dogru')}**")
            md += ["", f"## Soru havuzu ({len(hv)}) — aşama sorusu ve check-up adayı seçmek için (ref ile)", ""]
            for q in hv:
                d = q.get("dogru")
                md.append(f"- `{q['ref']}` · {q.get('tur')}{'/' + q['zorluk'] if q.get('zorluk') else ''} · s.{q.get('sayfa', '?')} · "
                          f"{kisalt(q.get('soru', ''), 260)} → **{d}) {kisalt((q.get('secenekler') or {}).get(d, ''), 80)}**")
            (KOK / "havuz" / f"{kaynak_kod(b, kod)}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        # kelime hedefi: çıkmış (%50), sayfa (%30), eşit (%20)
        if hedef:
            tc = sum(d["cikmis"] for d in dersler) or 1
            ts = sum(d["sayfa"] for d in dersler) or 1
            for d in dersler:
                # patoloji: hoca her ders slaytından ~1 soru soruyor → derslere eşite yakın pay
                a, c, e = (0.2, 0.3, 0.5) if b == "patoloji" else (0.5, 0.3, 0.2)
                w = a * d["cikmis"] / tc + c * d["sayfa"] / ts + e / len(dersler)
                d["hedef_kelime"] = int(round(hedef * w / 50) * 50)
        plan["partlar"].append({
            "key": key, "brans": b, "brans_ad": SINAV[b][0], "no": int(key.rsplit("-", 1)[-1]) if key[-1].isdigit() else 1,
            "baslik": baslik, "hedef_kelime": hedef, "hedef_dakika": round(hedef / DAKIKA_KELIME), "dersler": dersler,
            "yazar_gruplari": gruplar,
        })
    (KOK / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in plan["partlar"]:
        print(p["key"], p["hedef_kelime"], p["hedef_dakika"], "dk", [(d["kod"], d.get("hedef_kelime"), d["cikmis"], d["havuz"], bool(d["sesli_anlatim"]), bool(d["ders_notu"])) for d in p["dersler"]])


if __name__ == "__main__":
    main()
