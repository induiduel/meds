#!/usr/bin/env python3
"""Kurul ders kayıt defteri: src/data/dersler/k<N>.json — her üreticinin (ders işçisi, spot/önem, asistan, çözücü,
EMA ses, olası soru, Öğren eşleme) ORTAK ders listesi. Ders listesini betiklerin içine sabit yazma; buradan oku.

Kaynak (öncelik): meds_database/taxonomy/donem3_ders_programi.json — ders işçisinin (isle.py program_eslesmesi)
kullandığı ayrıştırma; konu adları birebir aynı olsun diye. Yoksa src/data/kurul_takvimi.json'dan ayrıştırılır
(hücreler satırlara bölünmüş olabilir; branş adı çapa: konu = branştan sonra, unvana ya da sonraki branşa kadar).

Kimlik ve kodlar KARARLIDIR (GELECEK_PLANLAMASI §5). Dosya varsa mevcut kayıtların `id`/`kod`/`no`'su korunur,
yeni ders sona eklenir; derse elle yazılmış alanlar (pdf, cikmis_konular, durum, not) ezilmez.
  id   : k<N>-<sıra 2 hane>             (ders programı sırası; ör. k2-07)
  kod  : <N><branş harfi><branş sırası>  (ör. 2n03 = Kurul 2 Nöroloji 3. ders) — branşlar arası ve kurullar arası tekil.
         Kurul 1'in eski kodları (07, e01, u03, …) değişmez; bu şema Kurul 2'den itibaren geçerlidir.
Kullanım: python3 ders_kaydi.py --kurul 2 [--yaz]
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
TAKVIM = MEDS / "src/data/kurul_takvimi.json"
DISIPLIN = MEDS / "src/data/curriculum_disciplines.json"
HARF = {b["ad"]: b["harf"] for b in json.loads((MEDS / "src/data/dersler/branslar.json").read_text())["branslar"]}  # tek kaynak
UNVAN = re.compile(r"\b(?:PROF|DOÇ|DOC|DR|UZM|ÖĞR|ÜYESİ|Prof|Doç|Dr|Uzm)\b\.?")
DISI = re.compile(r"(?i)^(klinik ve mesleki beceriler|bağımsız öğrenme|resmi tatil|alan dışı seçmeli)")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("İ", "i").replace("I", "ı").lower()
    return re.sub(r"[^0-9a-zçğıöşü]+", " ", s).strip()


def ayikla(metin, branslar):
    """Bir hücreden (branş, konu, hoca) parçaları."""
    desen = "|".join(re.escape(b) for b in sorted(branslar, key=len, reverse=True))
    out = []
    parcalar = list(re.finditer(rf"(?<![A-Za-zÇĞİÖŞÜçğıöşü])(?:{desen})(?![A-Za-zÇĞİÖŞÜçğıöşü])", metin))
    for i, m in enumerate(parcalar):
        son = parcalar[i + 1].start() if i + 1 < len(parcalar) else len(metin)
        govde = metin[m.end():son].strip(" :-")
        u = UNVAN.search(govde)
        konu = (govde[:u.start()] if u else govde).strip(" :-")
        hoca = govde[u.start():].strip(" :-") if u else ""
        if len(konu) >= 4 and not DISI.match(konu):
            out.append((m.group(0), konu, hoca))
    return out


PROGRAM = MEDS.parent / "meds_database/taxonomy/donem3_ders_programi.json"


def programdan(kurul):
    if not PROGRAM.exists():
        return None
    p = json.loads(PROGRAM.read_text())
    k = next((x for x in p.get("kurullar", []) if x.get("kurul") == kurul), None)
    if not k:
        return None
    out = {}
    for x in k.get("konular", []):
        if x.get("tur", "ders") != "ders" or not x.get("konu") or not x.get("ders"):
            continue
        konu, hoca = x["konu"], x.get("ogretim_uyesi") or ""
        u = UNVAN.search(konu)  # kaynakta bazen hoca adı konuya yapışık ("Panik Bozukluk Doç. Dr. …")
        if u and u.start() > 3:
            konu, hoca = konu[:u.start()].strip(" :-"), hoca or konu[u.start():].strip()
        a = (x["ders"], norm(konu))
        d = out.setdefault(a, {"brans": x["ders"], "konu": konu, "ogretim_uyesi": hoca,
                               "tarih": x.get("tarih"), "saat": (x.get("saat_dilimleri") or [""])[0], "saat_sayisi": 0})
        d["saat_sayisi"] += int(x.get("saat") or 1)
    return out


def uret(kurul, onceki):
    dersler = programdan(kurul)
    if dersler is None:
        dersler = takvimden(kurul)
    return kimliklendir(kurul, dersler, onceki)


def takvimden(kurul):
    t = json.loads(TAKVIM.read_text())
    k = next(x for x in t["kurullar"] if x["kurul"] == kurul)
    branslar = json.loads(DISIPLIN.read_text()).get(str(kurul)) or list(HARF)
    dersler = {}
    for d in sorted(k["dersler"], key=lambda x: (x["tarih"], x["saat"])):
        for brans, konu, hoca in ayikla(d["metin"], branslar):
            anahtar = (brans, norm(konu))
            x = dersler.setdefault(anahtar, {"brans": brans, "konu": konu, "ogretim_uyesi": "", "tarih": d["tarih"],
                                             "saat": d["saat"], "saat_sayisi": 0})
            x["saat_sayisi"] += 1
            if len(hoca) > len(x["ogretim_uyesi"]) and len(hoca.split()) >= 3:
                x["ogretim_uyesi"] = re.sub(r"\s+", " ", hoca)
    # Kesik konu: bir konu başka bir konunun önekiyse (aynı branş) uzun olanda birleşir
    for a in list(dersler):
        for b in list(dersler):
            if a != b and a in dersler and b in dersler and a[0] == b[0] and b[1].startswith(a[1]) and len(a[1]) >= 12:
                dersler[b]["saat_sayisi"] += dersler.pop(a)["saat_sayisi"]
    return dersler


def kimliklendir(kurul, dersler, onceki):
    eski = {(x["brans"], norm(x["konu"])): x for x in onceki}
    sayac, out = {}, []  # sayaç HARFE göre: aynı branşın farklı yazımları (Anestezi/Anesteziyoloji) çakışmasın
    bilinmeyen = sorted({x["brans"] for x in dersler.values() if x["brans"] not in HARF})
    if bilinmeyen:
        raise SystemExit(f"HATA: branslar.json'da tanımsız branş: {bilinmeyen} — src/data/dersler/branslar.json'a ekleyin")
    for x in onceki:  # kararlılık: önceki kimlik/kodlar
        h = x["kod"][1]
        sayac[h] = max(sayac.get(h, 0), int(x["kod"][2:]))
    sira = max([int(x["id"].split("-")[1]) for x in onceki] or [0])
    for anahtar, x in sorted(dersler.items(), key=lambda kv: (kv[1]["tarih"], kv[1]["saat"])):
        e = eski.pop(anahtar, None)
        if e:
            e.update({k2: x[k2] for k2 in ("tarih", "saat", "saat_sayisi")})
            if not e.get("ogretim_uyesi"): e["ogretim_uyesi"] = x["ogretim_uyesi"]
            out.append(e); continue
        h = HARF[x["brans"]]
        sira += 1; sayac[h] = sayac.get(h, 0) + 1
        out.append({"id": f"k{kurul}-{sira:02d}", "kod": f"{kurul}{h}{sayac[h]:02d}",
                    "kurul": kurul, **x, "pdf": None, "cikmis_konular": [], "durum": {}})
    for e in eski.values():  # programdan düşen ders silinmez, işaretlenir
        e["programda_yok"] = True; out.append(e)
    return sorted(out, key=lambda x: x["id"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--kurul", type=int, required=True); ap.add_argument("--yaz", action="store_true")
    a = ap.parse_args()
    yol = MEDS / f"src/data/dersler/k{a.kurul}.json"
    onceki = json.loads(yol.read_text())["dersler"] if yol.exists() else []
    dersler = uret(a.kurul, onceki)
    for x in dersler:
        print(f"{x['id']} {x['kod']:5} {x['tarih']} {x['saat_sayisi']}s {x['brans'][:16]:16} {x['konu'][:55]:55} {x['ogretim_uyesi'][:30]}")
    import collections
    cift = [k for k, n in collections.Counter(x["kod"] for x in dersler).items() if n > 1]
    if cift:
        print("HATA: aynı kod birden çok derste:", cift); sys.exit(1)
    print(f"{len(dersler)} ders")
    if a.yaz:
        yol.write_text(json.dumps({"surum": 1, "kurul": a.kurul, "kaynak": "kurul_takvimi.json", "dersler": dersler},
                                  ensure_ascii=False, indent=1) + "\n")
        print("yazıldı:", yol)
