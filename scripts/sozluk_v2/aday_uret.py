#!/usr/bin/env python3
"""Sözlük v2 — aday terim şablonu (300–1000 terim).

Kaynaklar (yalnız veritabanındaki doğrulanmış katman):
  - meds_database_v2/ders_notlari_k1/notlar/*.md : başlıklar (##, ###) ve kalın terimler (**X**)
  - meds_database_v2/tibbi_terimler_sozlugu/tibbi_terimler_sozlugu.json : özel tıbbi terimler

Sözlükte (site medical_encyclopedia.json + medical_glossary.json) adı ya da eşanlamlısı
zaten olan terimler alınmaz. Çıktı: meds_temp/sozluk_v2/sablon_terimler.json

Var olan şablondaki `durum` (tamam/red) ve elle verilen alanlar korunur; betik yeniden
çalıştırılınca yalnız yeni adaylar eklenir.

Kullanım: python3 meds/scripts/sozluk_v2/aday_uret.py [--hedef 1000]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
NOTLAR = ROOT / "meds_database_v2/ders_notlari_k1"
TERIMLER = ROOT / "meds_database_v2/tibbi_terimler_sozlugu/tibbi_terimler_sozlugu.json"
SITE = ROOT / "meds/src/data"
OUT = ROOT / "meds_temp/sozluk_v2/sablon_terimler.json"


def norm(s: str) -> str:
    s = re.sub(r"\(.*?\)", " ", s or "").replace("İ", "i").replace("I", "ı").lower()
    return " ".join(re.sub(r"[^\wçğıöşü ]", " ", s).split())


def slug(s: str) -> str:
    tr = str.maketrans("çğıöşüâî", "cgiosuai")
    return re.sub(r"[^a-z0-9]+", "-", norm(s).translate(tr)).strip("-")[:70]


# Bölüm başlığı / genel söz (kavram değil)
GENEL = set(norm(x) for x in """
tanım tanımı etiyoloji etyoloji patogenez patofizyoloji morfoloji klinik klinik bulgular tanı tedavi
tanı ve tedavi tedavi ilkeleri komplikasyonlar prognoz epidemiyoloji insidans prevalans risk faktörleri
yan etkiler yan etkileri endikasyonlar etki mekanizması mekanizma sınıflama sınıflandırma özet sonuç
öğrenim hedefleri giriş genel özellikler temel prensip histolojik özellikler makroskopi mikroskopi
akciğer mide böbrek karaciğer deri kalp beyin seyir önemli ayırıcı tanı korunma kontrol örnek örnekler
tablo not dikkat sınav spotu klinik önem tedavi edilmezse enfeksiyon dışı bakteriler virüsler mantarlar
yetişkin çocuk erkek kadın gebelik yaşlılar komplet inkomplet tip tipler alt tipler diğer diğerleri
""".split("\n")) | set(norm(w) for w in "tanım etiyoloji patogenez morfoloji klinik tanı tedavi seyir prognoz etkenler belirtiler bulgular nedenler".split())

KAT_KURAL = [  # (kategori, regex) — ilk eşleşen kazanır
    ("ilac", r"(mab|mus|limus|sporin|pril|sartan|vir|azol|misin|sillin|floksasin|siklin|mid|fen|ilaç|inhibitör|antagonist|agonist|aşı\b|aşısı|profilaksi|kemoterapi|steroid|glukokortikoid|interferon|metotreksat|azatioprin|siklofosfamid|penisilin|seftriakson|doksisiklin|azitromisin|fosfomisin|nitrofurantoin)"),
    ("patojen", r"(virüs|virus|bakteri|treponema|chlamydia|klamidya|neisseria|gonore|candida|kandida|aspergill|mukor|mycoplasma|ureaplasma|trichomonas|gardnerella|escherichia|e\. coli|proteus|klebsiella|stafilokok|streptokok|enterokok|listeria|toxoplasma|toksoplazma|sitomegalovirüs|cmv|hpv|hsv|hiv|hbv|hcv|ebv|hhv|pneumocystis|jirovecii|mikobakteri|mycobacterium|tüberküloz basil|haemophilus|pseudomonas|parazit|mantar)"),
    ("genetik", r"(trizomi|monozomi|delesyon|translokasyon|mozaik|kromozom|karyotip|mutasyon|\bgen\b|geni\b|onkogen|baskılayıcı|tp53|brca|rb\b|ras\b|myc|her2|vhl|wt1|sry|kalıtım|otozomal|x'e bağlı|poliploidi|anöploidi|imprinting|disomi|fish|pgt|pgd|karyotip|amniyosentez|kordosentez|cvs)"),
    ("hastalik", r"(sendrom|hastalığı|hastalık|karsinom|sarkom|tümör|tümörü|lenfoma|lösemi|melanom|oma\b|om\b|(?<!as)it\b|(?<!as)iti\b|oz\b|ozu\b|iyazis|pati|patisi|emi\b|emisi|üri\b|ürisi|yetmezlik|enfeksiyon|ülser|kist|hiperplazi|displazi|neoplazi|skleroz|nefrit|sifiliz|frengi|gonore|endometriozis|adenomyozis|abortus|preeklampsi|eklampsi|mol\b|koryokarsinom|enürezis|taş|litiyazis)"),
    ("patoloji", r"(nekroz|apoptoz|atrofi|hipertrofi|metaplazi|kalsifikasyon|birikim|enflamasyon|inflamasyon|granülom|ödem|trombüs|tromboz|emboli|enfarktüs|şok|fibrozis|skar|onarım|iyileşme|hiperemi|konjesyon|kanama|amiloid|hiyalin|pigment|lipofuksin|ateroskleroz|anaplazi|invazyon|metastaz|kemotaksi|fagositoz|diapedez)"),
    ("protein", r"(kinaz|reseptör|interlökin|il-\d|tnf|kemokin|sitokin|kompleman|immünoglobulin|ig[agmde]\b|antikor|antijen|enzim|faktör|kaspaz|siklin|integrin|kadherin|selektin|prostaglandin|lökotrien|histamin|bradikinin|serotonin|nitrik oksit|hormon|hcg|afp|psa|ca[- ]?125)"),
    ("tani", r"(test|tarama|biyopsi|smear|pap|ultrason|usg|kültür|boyama|serolo|vdrl|rpr|tpha|elisa|pcr|idrar tahlili|tetkik|görüntüleme|evreleme|derecelendirme|gleason|tnm)"),
    ("halk-sagligi", r"(oran|hızı|hız\b|sağlık hizmet|aile hekim|bakım|izlem|sürveyans|bağışıklama|beslenme|emzirme|anne sütü|salgın|karantina|izolasyon|dezenfeksiyon|sterilizasyon|tnsa|ölüm|mortalite|morbidite)"),
]

DERS_KAT = {"Tıbbi Farmakoloji": "ilac", "Halk Sağlığı": "halk-sagligi", "Tıbbi Genetik": "genetik"}

TT_KAT = {
    "hastalik_sendrom": "hastalik", "ilac": "ilac", "patojen": "patojen", "gen_protein_biyobelirtec": "protein",
    "tani_yontem": "tani", "belirti_semptom_bulgu": "terim", "fizyoloji_mekanizma": "patoloji",
    "anatomi_doku_hucre": "terim", "donem_siklus_kavram": "terim",
}


def kategori(term: str, ders: str, ipucu: str | None = None) -> str:
    t = norm(term)
    for kat, rx in KAT_KURAL:
        if re.search(rx, t):
            return kat
    return ipucu or DERS_KAT.get(ders) or "terim"


# Başlıkta bu sözler varsa bölüm başlığıdır, kavram değil
YAPI = re.compile(r"(\b(ve|ile|veya|ya da)\b.*\b(ve|ile)\b|[–—]|\b(giriş|özet|özeti|nedenleri|nedenler|etkileri|etkiler|özellikleri|özellikler|"
                  r"morfolojisi|morfoloji|klinik|tanım|tanımı|tanımlar|sınıfla\w*|karşılaştır\w*|yaklaşım|değerlendirme|"
                  r"temel|genel|bilgiler|kavramlar|örnek\w*|tablo\w*|sonuçları|evresi|mekanizmalar\w*|yolları|"
                  r"faktörler\w*|hedefleri|dağılım|önlenmesi|korunma|tedavisi|tanısı|bulguları|ilkeleri|"
                  r"dönemi|başlığı|üyesi|kaynak\w*|soru\w*|cevap|çözüm|spot|kısa|diğer|başlıca|önemli|çerçeve|"
                  r"riskleri|kimlere|endikasyonları|uygulama\w*|yöntemleri|izlemi|amaçları|durum)\b)", re.I)
# Tek başına kavram olmayan sıfat/genel söz (terim sözlüğü gürültüsü)
SIFAT = re.compile(r"^(sık|genç|yaşlı|klinik|solid|malign|benign|agresif|hafif|ağır|risk|tanı|tedavi|hasta|hastalık|"
                   r"enfeksiyon hastalıkları|bağışıklık sistemi|sinir sistemi|nükleik asit|kan basıncı|yağ doku|"
                   r"lenf düğümleri|lenf nodu|t lenfosit\w*|b lenfosit\w*|t hücre\w*|bazal hücre|ölüm oranı|"
                   r"hidrojen peroksit|gastrointestinal \w+)\b", re.I)


def kavram_mi(k: str) -> bool:
    if not 3 <= len(k) <= 60 or len(k.split()) > 6:
        return False
    if YAPI.search(k) or SIFAT.search(k):
        return False
    if re.match(r"^(soru|tablo|şekil|örnek|not|adım)\b", k, re.I) or re.search(r"[=<>%+/|]|\d{4}|\?$", k):
        return False
    if k[0].islower() and len(k.split()) == 1:  # tek küçük harfli söz: çoğunlukla cümle parçası
        return False
    n = norm(k)
    if not n or n in GENEL or len(n) < 4:
        return False
    if re.match(r"^(ve|ile|ya da|veya|için|en|çok|daha|bu|bir|her|tüm|olan|ise|gibi)\b", n):
        return False
    return True


def sozlukte_olan(haric_v2: bool = False) -> set[str]:
    """haric_v2: sozluk_v2'nin kendi eklediği kayıtlar sayılmaz (doğrulayıcı yeniden birleştirmede kullanır)."""
    have: set[str] = set()
    for e in json.loads((SITE / "medical_encyclopedia.json").read_text()):
        if haric_v2 and e.get("uretici") == "sozluk_v2":
            continue
        for x in [e.get("term"), e.get("latinName"), *(e.get("aliases") or [])]:
            if x:
                have.add(norm(x))
    for v in json.loads((SITE / "medical_glossary.json").read_text()).values():
        if haric_v2 and (v.get("dogrulama") or {}).get("uretici") == "sozluk_v2":
            continue
        for x in [v.get("term"), *(v.get("aliases") or [])]:
            if x:
                have.add(norm(x))
    return have - {""}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hedef", type=int, default=1000)
    a = ap.parse_args()

    index = json.loads((NOTLAR / "index.json").read_text())
    have = sozlukte_olan()
    aday: dict[str, dict] = {}

    def ekle(term: str, ders: dict, satir: int, puan: float, tur: str, ipucu: str | None = None):
        term = re.sub(r"\s+", " ", term).strip(" :–-")
        if not kavram_mi(term):
            return
        k = norm(term)
        if k in have:
            return
        r = aday.setdefault(k, {"term": term, "puan": 0.0, "dersler": {}, "turler": set(), "ipucu": ipucu})
        r["puan"] += puan
        r["turler"].add(tur)
        r["dersler"].setdefault(ders["id"], {"ders_id": ders["id"], "ders": ders["ders"], "konu": ders["title"],
                                             "dosya": ders["dosya"], "satir": satir})

    for d in index:
        lines = (NOTLAR / d["dosya"]).read_text().splitlines()
        govde = False
        for i, ln in enumerate(lines, 1):
            if re.match(r"^##\s", ln):
                govde = not re.search(r"(soru|öğrenim hedef|spot bilgi|kaynak|özet)", ln, re.I)
            if not govde:
                continue
            m = re.match(r"^#{2,4}\s+(?:\d+(?:\.\d+)*\.?\s*)?(.+)$", ln)
            if m:
                ekle(re.sub(r"[*=]", "", m.group(1)), d, i, 3.0, "baslik")
            for m in re.finditer(r"\*\*([^*\n]{3,60}?):?\*\*", ln):
                ekle(m.group(1), d, i, 1.0, "kalin")

    tt = json.loads(TERIMLER.read_text())["terimler"].values()
    by_dosya = {d["dosya"]: d for d in index}
    for t in tt:
        if not (t.get("tibbi_terim") and t.get("ozel_terim")) or t.get("kategori") not in TT_KAT:
            continue
        if not ((t.get("kimlik") or {}).get("qid") or (t.get("kodlar") or {}).get("icd10")):
            continue
        if t["kategori"] in ("anatomi_doku_hucre", "fizyoloji_mekanizma", "donem_siklus_kavram") and t.get("kelime_sayisi", 1) < 2:
            continue
        gd = [g for g in t.get("gectigi_dersler") or [] if g.get("dosya") in by_dosya]
        for g in gd[:3]:
            d = by_dosya[g["dosya"]]
            lines = (NOTLAR / d["dosya"]).read_text().splitlines()
            satir = next((i for i, ln in enumerate(lines, 1) if norm(t["turkce"]) in norm(ln)), 0)
            ekle(t["turkce"], d, satir, 0.8 + 0.4 * len(gd), "terim_sozlugu", TT_KAT[t["kategori"]])

    # Önceki şablonu koru
    eski = {}
    if OUT.exists():
        for r in json.loads(OUT.read_text())["terimler"]:
            eski[r["id"]] = r

    rows = []
    for k, r in aday.items():
        dersler = list(r["dersler"].values())
        puan = r["puan"] + 1.5 * (len(dersler) - 1)
        if puan < 1.5 or len(dersler) > 12:
            continue
        ilk = dersler[0]
        rows.append({
            "id": "s2-" + slug(r["term"]),
            "term": r["term"],
            "category": kategori(r["term"], ilk["ders"], r["ipucu"]),
            "subcategory": f"{ilk['ders']} › {ilk['konu']}",
            "discipline": ilk["ders"],
            "kurul": "Kurul 1",
            "oncelik": round(puan, 1),
            "kaynak_tur": sorted(r["turler"]),
            "dersler": dersler[:5],
            "durum": "bos",
        })
    # Elle/ajanla elenen adaylar (bölüm başlığı, genel söz, yinelenen) geri gelmez
    elenen_p = OUT.parent / "elenen_adaylar.json"
    elenen = {r["id"] for r in json.loads(elenen_p.read_text())} if elenen_p.exists() else set()
    rows = [r for r in rows if r["id"] not in elenen]
    rows.sort(key=lambda x: -x["oncelik"])
    seen, out = set(), []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        out.append({**r, **{k: v for k, v in eski.get(r["id"], {}).items() if k in ("durum", "term", "category", "subcategory", "not", "parti", "kart_id")}})
    # elle eklenen (aday listesinde olmayan) şablon satırları korunur
    for rid, r in eski.items():
        if rid not in seen:
            out.append(r)
            seen.add(rid)
    # eski şablon satırları (kürasyonlu) önce, yeni adaylar sonra
    out.sort(key=lambda r: (r["id"] not in eski, r.get("sira", 10**6) if r["id"] in eski else -r["oncelik"]))
    out = out[: max(a.hedef, sum(1 for r in out if r["durum"] != "bos"))]
    for i, r in enumerate(out, 1):
        r["sira"] = i
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "surum": 1,
        "aciklama": "Sözlük v2 aday terim şablonu. Kart şeması: meds_temp/sozluk_v2/SABLON.md",
        "hedef": "300-1000",
        "istatistik": {
            "toplam": len(out),
            "durum": dict(collections.Counter(r["durum"] for r in out)),
            "kategori": dict(collections.Counter(r["category"] for r in out)),
        },
        "terimler": out,
    }, ensure_ascii=False, indent=1))
    print(json.dumps({"aday": len(aday), "sablon": len(out),
                      "kategori": collections.Counter(r["category"] for r in out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
