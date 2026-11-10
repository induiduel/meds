#!/usr/bin/env python3
"""Ek modül içerik kapısı: b<N>.json (konular), sinav_oncesi.json, genel_sorular.json → 0 HATA olmadan ses/yayın yok.

Kullanım (çalışma dizini meds/): python3 scripts/ek_modul/dogrula.py <dosya.json> [<dosya2.json> …]
                                 python3 scripts/ek_modul/dogrula.py --modul yuruyus-kampcilik   (tüm dosyalar + toplamlar)
Kurallar: scripts/ek_modul/TALIMAT.md
"""
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts"))
try:
    from turkce_uslup import denetle as uslup
except Exception:  # kapı yüklenemezse sessizce atlanmaz
    uslup = None

HARF = "ABCDE"
YASAK = re.compile(r"\b(PDF|slayt\w*|şık\w*|şıkk\w*|çeldirici\w*|hoca\w*|sınavda çık\w*)\b", re.I)
GECISTIRME = re.compile(r"(bu sorunun cevabı değil|olarak geçmez|^yanlıştır\.?$|^doğrudur\.?$)", re.I)
SES_YASAK = re.compile(r"[0-9%°/()\[\]*\"“”_#]|\b(vb|vs|dk|km|kg|ml|cm|sn)\b\.?")
HARF_ANMA = re.compile(r"\b[A-E] (şıkkı|seçeneği)\b")


def kelime(s: str) -> int:
    return len(re.findall(r"[\wçğıöşüÇĞİÖŞÜ'’-]+", re.sub(r"[*>\[\]!]", " ", s)))


class Rapor:
    def __init__(self, ad: str):
        self.ad, self.hata, self.uyari, self.modul = ad, [], [], ""

    def h(self, yer, m): self.hata.append(f"HATA  {self.ad} {yer}: {m}")
    def u(self, yer, m): self.uyari.append(f"UYARI {self.ad} {yer}: {m}")


def ses_denet(r: Rapor, yer: str, s: str, enaz: int | None = None, encok: int | None = None, cumle_encok=24):
    if not isinstance(s, str) or not s.strip():
        return r.h(yer, "ses metni boş")
    m = SES_YASAK.search(s)
    if m:
        r.h(yer, f"ses metninde yasak karakter/kısaltma «{m.group(0)}»: {s[:60]}")
    if HARF_ANMA.search(s):
        r.h(yer, "ses metninde harf anma")
    for c in re.split(r"(?<=[.!?])\s+", s.strip()):
        if kelime(c) > cumle_encok:
            r.h(yer, f"cümle {kelime(c)} kelime (en çok {cumle_encok}): {c[:50]}…")
    n = kelime(s)
    if enaz and n < enaz: r.h(yer, f"{n} kelime (en az {enaz})")
    if encok and n > encok: r.h(yer, f"{n} kelime (en çok {encok})")


def metin_denet(r: Rapor, yer: str, s: str):
    if not isinstance(s, str) or not s.strip():
        return r.h(yer, "metin boş")
    m = YASAK.search(s)
    if m:
        r.h(yer, f"yasak sözcük «{m.group(0)}»")
    if uslup:
        for e in uslup(re.sub(r"\*\*|> \[!\w+\]", "", s), yer):
            r.h(yer, f"üslup: {e}")


def soru_denet(r: Rapor, yer: str, q: dict):
    for a in ("kok", "secenekler", "dogru", "cozum", "siklar", "ses_cozum", "zorluk"):
        if a not in q:
            return r.h(yer, f"alan eksik: {a}")
    if list(q["secenekler"]) != list(HARF) or list(q["siklar"]) != list(HARF):
        r.h(yer, "seçenekler/siklar A–E olmalı")
        return
    if q["dogru"] not in HARF: r.h(yer, "dogru A–E değil")
    if q["zorluk"] not in ("kolay", "orta", "zor"): r.h(yer, "zorluk kolay/orta/zor olmalı")
    metin_denet(r, yer + " kök", q["kok"])
    if kelime(q["kok"]) > 45: r.h(yer, f"kök {kelime(q['kok'])} kelime (en çok 45)")
    sec = q["secenekler"]
    if len({s.strip().lower() for s in sec.values()}) < 5: r.h(yer, "yinelenen seçenek")
    for hf, s in sec.items():
        if kelime(s) > 14: r.h(yer, f"seçenek {hf} {kelime(s)} kelime (en çok 14)")
        if re.search(r"hepsi|hiçbiri", s, re.I): r.h(yer, f"seçenek {hf}: hepsi/hiçbiri yasak")
        metin_denet(r, f"{yer} seçenek {hf}", s)
    uz = {hf: len(s) for hf, s in sec.items()}
    if q["dogru"] in uz and uz[q["dogru"]] == max(uz.values()) and list(uz.values()).count(max(uz.values())) == 1 \
            and uz[q["dogru"]] > 1.25 * sorted(uz.values())[-2]:
        r.h(yer, "doğru seçenek belirgin biçimde en uzun")
    for hf, s in q["siklar"].items():
        y = f"{yer} açıklama {hf}"
        metin_denet(r, y, s)
        n = kelime(s)
        if n < 14 or n > 40: r.h(y, f"{n} kelime (14–40)")
        if GECISTIRME.search(s.strip()): r.h(y, "geçiştirme cümlesi")
        if HARF_ANMA.search(s): r.h(y, "harf anma")
    metin_denet(r, yer + " çözüm", q["cozum"])
    n = kelime(q["cozum"])
    if n < 12 or n > 40: r.h(yer + " çözüm", f"{n} kelime (12–40)")
    ses_denet(r, yer + " ses_cozum", q["ses_cozum"], 25, 60)


def sorular_denet(r: Rapor, yer: str, sorular: list, adet: int | None, dagilim: dict | None):
    if adet is not None and len(sorular) != adet:
        r.h(yer, f"{len(sorular)} soru (tam {adet} olmalı)")
    for i, q in enumerate(sorular, 1):
        if q.get("no") != i: r.h(f"{yer} soru {i}", f"no {q.get('no')} (sıralı olmalı)")
        soru_denet(r, f"{yer} soru {i}", q)
    z = Counter(q.get("zorluk") for q in sorular)
    if dagilim and dict(z) != dagilim:
        r.h(yer, f"zorluk dağılımı {dict(z)} (olmalı {dagilim})")
    d = Counter(q.get("dogru") for q in sorular)
    n = len(sorular)
    if n >= 8:
        alt, ust = max(1, n // 5 - 2), n // 5 + 2 if n > 8 else 2
        for hf in HARF:
            if not alt <= d.get(hf, 0) <= ust:
                r.h(yer, f"doğru harf dağılımı dengesiz: {dict(d)} (her harf {alt}–{ust})")
                break
    kokler = [re.sub(r"\W+", " ", q.get("kok", "").lower()).strip() for q in sorular]
    for k, c in Counter(kokler).items():
        if c > 1: r.h(yer, f"yinelenen kök: {k[:50]}")


def ekran_denet(r: Rapor, yer: str, s: str):
    metin_denet(r, yer, s)
    madde = [x for x in s.splitlines() if x.strip().startswith("- ")]
    if not 3 <= len(madde) <= 5: r.h(yer, f"{len(madde)} madde (3–5)")
    for x in madde:
        if not re.match(r"- \*\*[^*]+\*\*", x.strip()): r.h(yer, f"madde «- **Anahtar:** …» biçiminde değil: {x[:40]}")
        if kelime(x) > 18: r.h(yer, f"madde {kelime(x)} kelime (en çok 16): {x[:40]}")
    if len(re.findall(r"^> \[!(IMPORTANT|NOTE)\]", s, re.M)) > 1: r.h(yer, "birden çok vurgu kutusu")
    if s.lstrip().startswith(("-", ">")): r.h(yer, "giriş cümlesi yok")
    n = kelime(s)
    if n < 35 or n > 95: r.h(yer, f"ekran {n} kelime (35–90)")


def konu_denet(r: Rapor, k: dict):
    y = f"konu {k.get('id')}"
    for a in ("id", "baslik", "ozet", "gorsel", "gorsel_alt", "bolumler", "akilda", "yap", "yapma", "spotlar", "etkinlikler", "sorular"):
        if a not in k:
            return r.h(y, f"alan eksik: {a}")
    if not 4 <= len(k["bolumler"]) <= 6: r.h(y, f"{len(k['bolumler'])} bölüm (4–6)")
    for i, b in enumerate(k["bolumler"], 1):
        ekran_denet(r, f"{y} bölüm {i} ekran", b.get("ekran", ""))
        ses = b.get("ses") or []
        if not 5 <= len(ses) <= 8: r.h(f"{y} bölüm {i}", f"{len(ses)} ses cümlesi (5–8)")
        ses_denet(r, f"{y} bölüm {i} ses", " ".join(ses), 60, 125, 22)
    for g in [{"dosya": k["gorsel"]}] + list(k.get("ek_gorseller") or []):
        if not (KOK / "public/ek_moduller" / r.modul / g["dosya"]).exists(): r.u(y, f"görsel dosyası yok: {g['dosya']}")
    ak = k["akilda"]
    if not all(ak.get(a) for a in ("kod", "acilim", "not")): r.h(y, "akilda: kod/acilim/not zorunlu")
    for ad in ("yap", "yapma"):
        if not 3 <= len(k[ad]) <= 5: r.h(y, f"{ad}: {len(k[ad])} madde (3–5)")
        for m in k[ad]:
            metin_denet(r, f"{y} {ad}", m)
            if kelime(m) > 13: r.h(f"{y} {ad}", f"madde {kelime(m)} kelime (en çok 12): {m[:40]}")
    if len(k["spotlar"]) != 7: r.h(y, f"{len(k['spotlar'])} spot (7)")
    for i, s in enumerate(k["spotlar"], 1):
        metin_denet(r, f"{y} spot {i}", s.get("metin", ""))
        if "**" not in s.get("metin", ""): r.h(f"{y} spot {i}", "kalın anahtar yok")
        if kelime(s.get("metin", "")) > 23: r.h(f"{y} spot {i}", "metin 22 kelimeyi aşıyor")
        ses_denet(r, f"{y} spot {i} ses", s.get("ses", ""), None, 26, 26)
    et = k["etkinlikler"]
    if len(et) != 2 or et[0].get("tur") == et[1].get("tur"): r.h(y, "2 farklı türde etkinlik olmalı")
    for i, e in enumerate(et, 1):
        ye, t = f"{y} etkinlik {i}", e.get("tur")
        if not e.get("baslik"): r.h(ye, "başlık yok")
        if t == "dogru_yanlis":
            f = e.get("ifadeler") or []
            if not 4 <= len(f) <= 5: r.h(ye, "4–5 ifade")
            if sum(1 for x in f if x.get("dogru") is True) < 1 or sum(1 for x in f if x.get("dogru") is False) < 2:
                r.h(ye, "en az 1 doğru, en az 2 yanlış ifade")
            for x in f:
                metin_denet(r, ye, x.get("metin", "")); metin_denet(r, ye, x.get("aciklama", ""))
        elif t == "sirala":
            if not 4 <= len(e.get("adimlar") or []) <= 6: r.h(ye, "4–6 adım")
            if not e.get("aciklama"): r.h(ye, "açıklama yok")
        elif t == "esle":
            c = e.get("ciftler") or []
            if not 4 <= len(c) <= 5: r.h(ye, "4–5 çift")
            if len({x.get("sag") for x in c}) != len(c) or len({x.get("sol") for x in c}) != len(c): r.h(ye, "yinelenen eş")
            for x in c:
                if kelime(x.get("sol", "")) > 7 or kelime(x.get("sag", "")) > 7: r.h(ye, "eş 6 kelimeyi aşıyor")
        else:
            r.h(ye, f"bilinmeyen tür {t}")
    sorular_denet(r, y, k["sorular"], 8, {"kolay": 3, "orta": 3, "zor": 2})


def dosya_denet(yol: Path) -> Rapor:
    r = Rapor(yol.name)
    r.modul = yol.resolve().parent.name
    try:
        j = json.loads(yol.read_text())
    except Exception as e:
        r.h("-", f"JSON okunamadı: {e}")
        return r
    if "konular" in j:
        if len(j["konular"]) != 2: r.h("-", f"{len(j['konular'])} konu (2)")
        for k in j["konular"]:
            konu_denet(r, k)
    elif "partlar" in j:  # sınav öncesi anlatıcı
        for i, p in enumerate(j["partlar"], 1):
            y = f"part {i}"
            metin_denet(r, y, p.get("ekran", ""))
            madde = [x for x in p.get("ekran", "").splitlines() if x.strip().startswith("- ")]
            if not 5 <= len(madde) <= 9: r.h(y, f"{len(madde)} madde (5–9)")
            ses = p.get("ses") or []
            if not 6 <= len(ses) <= 12: r.h(y, f"{len(ses)} ses cümlesi (6–12)")
            ses_denet(r, y + " ses", " ".join(ses), 80, 190, 22)
    elif "sorular" in j:  # genel (sınav öncesi) sorular
        sorular_denet(r, "genel", j["sorular"], None, None)
        for i, q in enumerate(j["sorular"], 1):
            if not q.get("konu"): r.h(f"genel soru {i}", "konu (ör. \"4b\") alanı yok")
    else:
        r.h("-", "tanınmayan dosya")
    return r


def pdf_esle_denet(kok: Path) -> list[str]:
    """"PDF ile dinle" eşlemesi (pdf_esle.py) güncel mi: kitapçık ve klipler eşlemeden sonra değişmemiş, her bölüm eşlenmiş,
    kutular sayfanın içinde, cümle sayısı ve zaman sırası doğru olmalı. Eskimişse betik yeniden çalıştırılır."""
    out: list[str] = []
    e = json.loads((kok / "pdf_esle.json").read_text())
    klip = json.loads((kok / "klip.json").read_text()) if (kok / "klip.json").exists() else {}
    pdf = KOK / "public/ek_moduller" / kok.name / e.get("pdf", "")
    yeniden = f"scripts/ek_modul/pdf_esle.py --modul {kok.name} yeniden çalıştırılmalı"
    if not pdf.is_file():
        return [f"HATA  pdf_esle: kitapçık yok ({e.get('pdf')})"]
    if pdf.stat().st_size != e.get("bayt"):
        out.append(f"HATA  pdf_esle: ders kitapçığı eşlemeden sonra yeniden üretilmiş; {yeniden}")
    for f in sorted(kok.glob("b*.json")):
        for k in json.loads(f.read_text())["konular"]:
            for i, b in enumerate(k["bolumler"], 1):
                ad = f"d-{k['id']}-{i}"
                x = e["klip"].get(ad)
                if ad not in klip:
                    continue  # sesi üretilmemiş bölüm eşlenmez
                if not x:
                    out.append(f"HATA  pdf_esle {ad}: eşleme yok; {yeniden}"); continue
                if x["v"] != klip[ad]["v"]:
                    out.append(f"HATA  pdf_esle {ad}: ses eşlemeden sonra yeniden üretilmiş; {yeniden}"); continue
                c = x["c"]
                if len(c) != len(b["ses"]) + 1:
                    out.append(f"HATA  pdf_esle {ad}: {len(c)} cümle zamanı, beklenen {len(b['ses']) + 1} (başlık + ses)")
                if any(c[j][0] >= c[j + 1][0] for j in range(len(c) - 1)) or c[0][0] != 0 or c[-1][0] >= klip[ad]["sure"]:
                    out.append(f"HATA  pdf_esle {ad}: cümle zamanları sıralı değil ya da klip süresini aşıyor")
                if any(not -1 <= m < len(x["l"]) for _t, m in c):
                    out.append(f"HATA  pdf_esle {ad}: cümle olmayan bir maddeye bağlı")
                if any(not (0 <= q[0] < q[2] <= 1 and 0 <= q[1] < q[3] <= 1) for q in [x["k"], *[q for l in x["l"] for q in l]]):
                    out.append(f"HATA  pdf_esle {ad}: kutu sayfanın dışında")
    return out


def main() -> int:
    arg = sys.argv[1:]
    if arg[:1] == ["--modul"]:
        kok = KOK / "src/data/ek_moduller" / arg[1]
        dosyalar = sorted(kok.glob("b*.json")) + [p for p in (kok / "sinav_oncesi.json", kok / "genel_sorular.json") if p.exists()]
    else:
        dosyalar = [Path(a) for a in arg]
    if not dosyalar:
        print(__doc__); return 2
    hata = 0
    for d in dosyalar:
        r = dosya_denet(d)
        for s in r.uyari + r.hata: print(s)
        hata += len(r.hata)
    if arg[:1] == ["--modul"] and (kok / "pdf_esle.json").exists():
        for satir in pdf_esle_denet(kok):
            print(satir); hata += satir.startswith("HATA")
    if uslup is None:
        print("HATA  turkce_uslup kapısı yüklenemedi"); hata += 1
    print(f"— {len(dosyalar)} dosya, {hata} HATA")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
