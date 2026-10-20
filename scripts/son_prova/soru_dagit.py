#!/usr/bin/env python3
"""Son Prova soru dağıtımı ve site verisi.

Kaynak: derlenmiş partlar (cikti/<key>/asamalar.json), plan.json, soru çözücü havuzları (meds/src/data/<brans>_cozucu/).
Her soru tek bir yerde kullanılır: aşama sonu (yazar seçti) → part check-up (yazar seçti) → genel check-up → deneme 1–3.
  - Genel check-up: branşın her aşamasından 2 soru (aşamanın dersinden, sayfası aşamanın slaytlarına en yakın), en az 20.
  - Deneme: sınav dağılımı (Patoloji 34, Enfeksiyon 22, …); ders payı çıkmış sıklığına göre (patoloji ders başına ≈1),
    zorluk kolay–orta (orta ağırlıklı, zor yok), üç deneme ayrık; aynı kökü taşıyan sorular tekrar etmez.
  - Her soru bir aşamaya bağlanır (yanlışta "bu bölüme dön" yönlendirmesi).
Çıktı: meds/src/data/son_prova/k1/index.json, sorular/<brans>.json
Kullanım: python3 meds_temp/son_prova/soru_dagit.py
"""
import hashlib
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent
ROOT = KOK.parents[1]
MEDS = ROOT / "meds"
PLAN = json.loads((KOK / "plan.json").read_text(encoding="utf-8"))
OUT = MEDS / "src/data/son_prova" / f"k{PLAN['kurul']}"
DENEME_SAY = 3
DENEME_DK = 120  # 100 soru (fakültenin teorik sınav süresine yakın)
TOHUM = 20261021


def kok_anahtar(t: str) -> str:
    return re.sub(r"[^a-zçğıöşü0-9]+", "", (t or "").lower())[:160]


def havuz_yukle(brans: str) -> dict[str, dict]:
    out = {}
    for f in sorted((MEDS / f"src/data/{brans}_cozucu").glob("*.json")):
        if f.stem == "index":
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        klasor = d.get("klasor") or d["kod"]
        kod = re.sub(r"-\d+$", "", d["kod"])
        for q in d["sorular"]:
            n = q["no"]
            klip = {}
            for k, v in (d.get("klip") or {}).items():
                m = re.fullmatch(r"([qicd])-(\d+)|s-(\d+)-([A-E])", k)
                if not m:
                    continue
                if m.group(1) and int(m.group(2)) == n:
                    klip[m.group(1)] = v["v"]
                elif m.group(3) and int(m.group(3)) == n:
                    klip[f"s{m.group(4)}"] = v["v"]
            out[f"{brans}/{d['kod']}#{n}"] = {**q, "_kod": kod, "_kl": klasor, "_klip": klip}
    return out


def slayt_kodu(brans: str, kod: str) -> str:
    return f"p{kod}" if brans == "patoloji" else kod


def main():
    partlar = []
    for p in PLAN["partlar"]:
        f = KOK / "cikti" / p["key"] / "asamalar.json"
        if not f.exists():
            print(f"UYARI derlenmemiş part: {p['key']}")
            continue
        hz = json.loads((KOK / "cikti" / p["key"] / "hizalama.json").read_text(encoding="utf-8"))
        asamalar = json.loads(f.read_text(encoding="utf-8"))
        # aşamanın asıl slayt sayfaları (kaynak PDF): genel/deneme sorusunu en yakın aşamaya bağlamak için
        for a in asamalar:
            ss = sorted({x for par in hz["paragraflar"][a["p"][0]:a["p"][1] + 1] for x in par["sayfalar"]})
            a["_asil"] = [(hz["sayfaKaynak"][s - 1]["kod"], hz["sayfaKaynak"][s - 1]["s"]) for s in ss]
        kelime = len((KOK / "cikti" / p["key"] / f"{p['key']}.md").read_text(encoding="utf-8").split())
        partlar.append({**p, "asamalar": asamalar, "_kelime": kelime, "_sayfa": len(hz["sayfaKaynak"])})

    brans_sira = list(PLAN["sinav"])
    havuz = {b: havuz_yukle(b) for b in brans_sira}
    kullanildi: set[str] = set()
    kok_kullanildi: set[str] = set()
    sorular_out = defaultdict(dict)  # brans → ref → soru
    asama_of: dict[str, list] = {}

    def kaydet(ref: str, part_key: str, no: int):
        b = ref.split("/")[0]
        q = havuz[b][ref]
        kullanildi.add(ref)
        kok_kullanildi.add(kok_anahtar(q["soru"]))
        asama_of[ref] = [part_key, no]
        sorular_out[b][ref] = {
            "soru": q["soru"], "secenekler": q["secenekler"], "dogru": q["dogru"], "ipucu": q.get("ipucu", ""),
            "siklar": q.get("siklar", {}), "cozum": q.get("cozum", ""), "tur": q.get("tur"),
            **({"sinav": q["sinav"]} if q.get("sinav") else {}), **({"zorluk": q["zorluk"]} if q.get("zorluk") else {}),
            "kaynak": {"kod": slayt_kodu(b, q["_kod"]), "s": q.get("sayfa") or []},
            "asama": [part_key, no], "kl": q["_kl"], "klip": q["_klip"],
        }

    hata = 0
    # 1) yazarın seçtikleri
    for p in partlar:
        for a in p["asamalar"]:
            for r in a["sorular"] + a["checkup"]:
                if r in kullanildi:
                    print(f"HATA tekrar eden soru {r} ({p['key']} a{a['no']})")
                    hata += 1
                kaydet(r, p["key"], a["no"])

    def en_yakin_asama(b: str, q: dict):
        """sorunun dersine ait aşamalardan sayfası en yakın olanı"""
        kod = slayt_kodu(b, q["_kod"])
        ss = q.get("sayfa") or []
        best = None
        for p in partlar:
            if p["brans"] != b:
                continue
            for a in p["asamalar"]:
                sayfalar = [s for k, s in a["_asil"] if k == kod]
                if not sayfalar:
                    continue
                uzak = min((abs(s - x) for s in sayfalar for x in ss), default=999)
                if a["ders"] == kod:
                    uzak -= 0.5
                if best is None or uzak < best[0]:
                    best = (uzak, p["key"], a["no"])
        return best

    def uygun(b: str, r: str, q: dict) -> bool:
        return r not in kullanildi and kok_anahtar(q["soru"]) not in kok_kullanildi and q.get("dogru") in (q.get("secenekler") or {})

    rnd = random.Random(TOHUM)
    zorluk_puan = {"orta": 0, None: 0.3, "kolay": 0.6, "zor": 3}

    def sec(b: str, adaylar: list[str], n: int, zor_yok=True, kolay_oran=0.0) -> list[str]:
        q = havuz[b]
        c = [r for r in adaylar if uygun(b, r, q[r]) and not (zor_yok and q[r].get("zorluk") == "zor")]
        if len(c) < n and zor_yok:  # havuz dar: zor sorular da aday
            c = [r for r in adaylar if uygun(b, r, q[r])]
        rnd.shuffle(c)
        c.sort(key=lambda r: (zorluk_puan.get(q[r].get("zorluk"), 1) + (0.2 if q[r].get("tur") == "cikmis" else 0)))
        if kolay_oran:  # deneme: kolay–orta arası, ortaya yakın → payın bir kısmı kolay/çıkmış önce
            k = round(n * kolay_oran)
            kolay = [r for r in c if q[r].get("zorluk") == "kolay" or q[r].get("tur") == "cikmis"][:k]
            c = kolay + [r for r in c if r not in kolay]
        out = []
        for r in c:
            if len(out) >= n:
                break
            if kok_anahtar(q[r]["soru"]) in kok_kullanildi:
                continue
            out.append(r)
            kok_kullanildi.add(kok_anahtar(q[r]["soru"]))
        return out

    # 2) genel check-up: aşama başına 2 soru (o aşamanın dersinden, sayfası aşamaya en yakın)
    genel = defaultdict(list)
    for b in brans_sira:
        for p in [x for x in partlar if x["brans"] == b]:
            for a in p["asamalar"]:
                adaylar = []
                for r, q in havuz[b].items():
                    if slayt_kodu(b, q["_kod"]) != a["ders"] or not uygun(b, r, q):
                        continue
                    e = en_yakin_asama(b, q)
                    if e and e[1] == p["key"] and e[2] == a["no"]:
                        adaylar.append(r)
                n = 2 if b in ("patoloji", "kadindogum", "farmakoloji") else 3
                for r in sec(b, adaylar, n):
                    kaydet(r, p["key"], a["no"])
                    genel[b].append(r)

    # 3) denemeler: branş soru sayısı, ders payı çıkmış sıklığına göre
    denemeler = [[] for _ in range(DENEME_SAY)]
    for b in brans_sira:
        n_b = PLAN["sinav"][b]["soru"]
        dersler = [d for p in partlar if p["brans"] == b for d in p["dersler"]]
        if not dersler:
            continue
        if b == "patoloji":
            agirlik = {d["slayt_kod"]: 1 + (1 if d["kod"] == "15" else 0) for d in dersler}
        else:
            agirlik = {d["slayt_kod"]: 1 + d["cikmis"] for d in dersler}
        top = sum(agirlik.values())
        for di in range(DENEME_SAY):
            # en büyük kalan yöntemi; deneme başına kalanlar dönerek dağıtılır
            pay = {k: n_b * w / top for k, w in agirlik.items()}
            tam = {k: int(v) for k, v in pay.items()}
            kalan = n_b - sum(tam.values())
            sira = sorted(pay, key=lambda k: (-(pay[k] - tam[k]), (hash(k) + di) % 7))
            for k in sira[di % len(sira):] + sira[:di % len(sira)]:
                if kalan <= 0:
                    break
                tam[k] += 1
                kalan -= 1
            secilen = []
            for kod, n in tam.items():
                adaylar = [r for r, q in havuz[b].items() if slayt_kodu(b, q["_kod"]) == kod]
                secilen += sec(b, adaylar, n, kolay_oran=0.3)
            if len(secilen) < n_b:  # dersin havuzu yetmediyse branşın kalanından
                adaylar = list(havuz[b])
                secilen += sec(b, adaylar, n_b - len(secilen))
            for r in secilen:
                e = en_yakin_asama(b, havuz[b][r])
                if not e:
                    print(f"HATA aşaması bulunamayan deneme sorusu {r}")
                    hata += 1
                    continue
                kaydet(r, e[1], e[2])
                denemeler[di].append(r)
            if len(secilen) != n_b:
                print(f"HATA deneme {di + 1} {b}: {len(secilen)}/{n_b}")
                hata += 1

    # 4) index
    dk = PLAN["dakika_kelime"]
    index = {
        "kurul": PLAN["kurul"], "ad": "Son Prova", "sinav": PLAN["sinav"],
        "dersler": [], "denemeler": [{"no": i + 1, "sure": DENEME_DK, "sorular": d} for i, d in enumerate(denemeler)],
    }
    for b in brans_sira:
        ps = [p for p in partlar if p["brans"] == b]
        if not ps:
            continue
        index["dersler"].append({
            "brans": b, "ad": PLAN["sinav"][b]["ad"], "soru": PLAN["sinav"][b]["soru"], "genel": genel[b],
            "partlar": [{
                "key": p["key"], "no": p["no"], "baslik": p["baslik"], "kelime": p["_kelime"], "tahminiDk": round(p["_kelime"] / dk),
                "sayfa": p["_sayfa"], "dersler": [{"kod": d["slayt_kod"], "no": re.match(r"\s*(\d+)", d["pdf_ad"]).group(1), "ad": a_ad}
                                                  for d, a_ad in ((d, next((a["dersAd"] for a in p["asamalar"] if a["ders"] == d["slayt_kod"]), d["ad"])) for d in p["dersler"])],
                "asamalar": [{k: a[k] for k in ("no", "baslik", "ders", "dersAd", "dersNo", "p", "sorular", "checkup")} for a in p["asamalar"]],
            } for p in ps],
        })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sorular").mkdir(exist_ok=True)
    for b, qs in sorular_out.items():
        (OUT / "sorular" / f"{b}.json").write_text(json.dumps(qs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ozet = hashlib.sha1(json.dumps(index, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:10]
    index["surum"] = ozet
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")

    # rapor
    for d in index["dersler"]:
        a = sum(len(x["sorular"]) for p in d["partlar"] for x in p["asamalar"])
        c = sum(len(x["checkup"]) for p in d["partlar"] for x in p["asamalar"])
        print(f"{d['brans']:12} partlar {len(d['partlar'])} · aşama sorusu {a} · check-up {c} · genel {len(d['genel'])} · "
              f"havuz {len(havuz[d['brans']])} → kullanılan {len(sorular_out[d['brans']])}")
    for i, dn in enumerate(denemeler, 1):
        say = defaultdict(int)
        zr = defaultdict(int)
        for r in dn:
            say[r.split("/")[0]] += 1
            q = havuz[r.split("/")[0]][r]
            zr[q.get("zorluk") or q.get("tur")] += 1
        print(f"deneme {i}: {len(dn)} soru {dict(say)} zorluk {dict(zr)}")
    if hata:
        print(f"{hata} HATA")
        sys.exit(1)


if __name__ == "__main__":
    main()
