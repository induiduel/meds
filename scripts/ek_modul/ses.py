#!/usr/bin/env python3
"""Ek modül EMA sesleri: src/data/ek_moduller/<modül>/*.json → data/ek_moduller/ses/<modül>/<klip>.mp3 + klip.json.

Klipler:  d-<konu>-<n>  sesli ders bölümü (başlık + `ses` cümleleri)        s-<konu>-<n>  spot (`ses`)
          o-<n>         sınav öncesi bölümü                                 q-<set>-<n>   soru: kök + seçenekler (ekran metninden okunuşa çevrilir)
          c-<set>-<n>   çözüm: "Doğru cevap …" + `ses_cozum`               (<set> = konu id'si ya da genel sorularda "g")
          h-<set>-<n>   hocanın çalışma sorusu (okunur)                    hc-<set>-<n>  cevabı + `cozum` (hoca_sorulari.json)
Ekran metni ile okuma metni ayrıdır: `ses` alanları yazarın konuşma metnidir; soru kökü/seçenekleri için okunuş `oku()` ile
üretilir (sayı, birim, kısaltma → yazıyla). Metni değişmeyen klip atlanır (özet klip.json'da `v`).

EMA DAİMA GPU'da (AGENTS kural 10, 2. istisna):
  bash scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/ek_modul/ses.py --modul yuruyus-kampcilik [--yalniz d-,s-] [--kuru]
`--kuru`: ses üretmez; klip sayısı, tahmini süre ve okunuşa çevrilmiş soru metinlerinde kalan şüpheli karakterleri yazar.
"""
from __future__ import annotations
import hashlib, json, os, re, sys
from pathlib import Path

if os.environ.get("EMA_CIHAZ") != "cuda":  # GPU istisnası: ema_isci.py başındaki koşullar
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("EMA_IS_PARCACIGI", "2")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts/sesli_anlatim"))

BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def sayi(n: int) -> str:
    if n == 0:
        return "sıfır"
    out = []
    for deger, ad in ((1_000_000, "milyon"), (1000, "bin")):
        k, n = divmod(n, deger)
        if k:
            out.append(ad if (k == 1 and ad == "bin") else f"{uc(k)} {ad}")
    if n:
        out.append(uc(n))
    return " ".join(out)


def uc(n: int) -> str:
    y, n = divmod(n, 100)
    o, b = divmod(n, 10)
    return " ".join(x for x in (("yüz" if y == 1 else f"{BIR[y]} yüz") if y else "", ON[o], BIR[b]) if x)


HARF = {"A": "aa", "B": "bee", "C": "cee", "D": "dee", "E": "ee", "F": "fee", "G": "gee", "H": "haa", "I": "ii", "İ": "ii", "K": "kaa",
        "L": "lee", "M": "mee", "N": "nee", "O": "oo", "P": "pee", "R": "ree", "S": "see", "T": "tee", "U": "uu", "V": "vee", "Y": "yee", "Z": "zee",
        "W": "dabılyu", "X": "iks", "Q": "kü"}
BIRIM = [(r"km", "kilometre"), (r"cm", "santimetre"), (r"mm", "milimetre"), (r"kcal", "kilokalori"), (r"kg", "kilo"), (r"ml", "mililitre"),
         (r"m", "metre"), (r"L", "litre"), (r"g", "gram"), (r"dk", "dakika"), (r"sn", "saniye")]
SOZLUK = [(r"\bvb\.?", "ve benzeri"), (r"\bvs\.?", "vesaire"), (r"\bör\.", "örneğin"), (r"UIAA", "uu ii aa aa"), (r"\bTDF\b", "tee dee fee"),
          (r"\bUV\b", "ultraviyole"), (r"\bDDD\b", "dee dee dee"), (r"\bSOS\b", "es o es"), (r"\bGPS\b", "cii pii es"),
          (r"\bMont Blanc\b", "mon blan"), (r"\bEverest\b", "everest"), (r"\bMessner\b", "mesner"), (r"\bReinhold\b", "raynhold"),
          (r"\bBrunton\b", "brantın"), (r"\bBreithaupt\b", "braythaupt"), (r"\bbergschrund\b", "bergşrund"), (r"\bLeave No Trace\b", "liiv no treys"),
          (r"\bself arrest\b", "self arest"), (r"\bfull body\b", "ful badi"), (r"\bhydration pack\b", "su torbası"), (r"\bpowerbank\b", "taşınabilir şarj cihazı"),
          (r"\bstrike[–-]dip\b", "strayk dip"), (r"\bdip direction[–-]dip amount\b", "dip direkşın dip emaunt"), (r"\btrekking\b", "treking"),
          (r"\bhardshell\b", "sert kabuk ceket"), (r"\bsoftshell\b", "yumuşak kabuk ceket"), (r"\bGiardia\b", "ciardiya"), (r"\bCryptosporidium\b", "kriptosporidyum")]


def oku(s: str) -> str:
    """Ekran metni → okunuş: sayılar, birimler, simgeler, kısaltmalar yazıyla; biçim imleri atılır."""
    s = re.sub(r"\*\*|[“”\"_#]", "", s)
    for pat, y in SOZLUK:
        s = re.sub(pat, y, s, flags=0 if any(c.isupper() for c in pat) else re.I)  # büyük harfli kalıp (ad, kısaltma) harfe duyarlı
    s = re.sub(r"(\d)\.(\d{3})\b", r"\1\2", s)                                   # 25.000 → 25000
    s = re.sub(r"\b1:(\d+)\b", lambda m: f"bir bölü {sayi(int(m.group(1)))}", s)  # ölçek
    s = re.sub(r"%\s*(\d+)", lambda m: f"yüzde {m.group(1)}", s)
    s = re.sub(r"(\d+)\s*°\s*[–-]\s*(\d+)\s*°", r"\1 ile \2 derece", s)             # 0°–360°
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 bölü \2", s)                               # 120/40 (eğim yönü/eğim açısı)
    s = re.sub(r"(\d+)\s*°\s*C\b", r"\1 derece", s)
    s = re.sub(r"(\d+)\s*°", r"\1 derece", s)
    s = re.sub(r"(\d+(?:,\d+)?)\s*[–-]\s*(\d+(?:,\d+)?)", r"\1 ile \2", s)          # 50–70 m → elli ile yetmiş metre
    for b, ad in BIRIM:
        s = re.sub(rf"(\d)\s*{b}\b(?!['’])", rf"\1 {ad}", s)
        s = re.sub(rf"(\d)\s*{b}['’]", rf"\1 {ad}", s)  # 100 m'de → yüz metrede
    s = re.sub(r"(\d+),(\d+)", lambda m: f"{sayi(int(m.group(1)))} virgül {sayi(int(m.group(2)))}", s)
    s = re.sub(r"(\d+)['’](\w+)", lambda m: f"{sayi(int(m.group(1)))}{m.group(2)}", s)  # 1924'te → bin dokuz yüz yirmi dörtte
    s = re.sub(r"\d+", lambda m: sayi(int(m.group(0))), s)
    s = s.replace("+", " artı ").replace("=", " eşittir ").replace("&", " ve ").replace("→", ", ").replace("/", " ya da ")
    s = re.sub(r"\b([NSEW])\b", lambda m: {"N": "en", "S": "es", "E": "e", "W": "dabılyu"}[m.group(1)], s)
    s = re.sub(r"\b[A-ZÇĞİÖŞÜ]{2,5}\b", lambda m: " ".join(HARF.get(c, c.lower()) for c in m.group(0)), s)
    s = re.sub(r"\(([^)]*)\)", r", \1,", s)
    s = re.sub(r"\s*[–—]\s*", ", ", s)
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r",\s*([.?!])", r"\1", s)
    return re.sub(r"\s{2,}", " ", s).strip()


SIK = {"A": "a", "B": "be", "C": "ce", "D": "de", "E": "e"}


def parcala(cumleler: list[str], n: int = 2) -> list[str]:
    """Konuşma cümlelerini 2'şerli paragraflara böler (EMA paragraf sonunda nefes payı bırakır)."""
    return [" ".join(cumleler[i:i + n]) for i in range(0, len(cumleler), n)]


def nokta(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in ".?!" else s + "."


def klipler(modul: str) -> dict[str, list[str]]:
    kok = KOK / "src/data/ek_moduller" / modul
    K: dict[str, list[str]] = {}

    def soru(onek: str, q: dict):
        sec = q["secenekler"]
        K[f"q-{onek}-{q['no']}"] = [nokta(oku(q["kok"]))] + [nokta(f"{SIK[h]} şıkkı: {oku(sec[h])}") for h in sec]
        K[f"c-{onek}-{q['no']}"] = [nokta(f"Doğru cevap {SIK[q['dogru']]} şıkkı: {oku(sec[q['dogru']])}")] + parcala(re.split(r"(?<=[.!?])\s+", q["ses_cozum"].strip()))

    for f in sorted(kok.glob("b*.json")):
        for k in json.loads(f.read_text())["konular"]:
            for i, b in enumerate(k["bolumler"], 1):
                K[f"d-{k['id']}-{i}"] = [nokta(oku(b["baslik"]))] + parcala(b["ses"])
            for i, s in enumerate(k["spotlar"], 1):
                K[f"s-{k['id']}-{i}"] = [s["ses"]]
            for q in k["sorular"]:
                soru(k["id"], q)
    if (kok / "sinav_oncesi.json").exists():
        for i, p in enumerate(json.loads((kok / "sinav_oncesi.json").read_text())["partlar"], 1):
            K[f"o-{i}"] = [nokta(oku(p["baslik"]))] + parcala(p["ses"])
    if (kok / "genel_sorular.json").exists():
        for q in json.loads((kok / "genel_sorular.json").read_text())["sorular"]:
            soru("g", q)
    if (kok / "hoca_sorulari.json").exists():
        for st in json.loads((kok / "hoca_sorulari.json").read_text())["setler"]:
            for q in st["sorular"]:
                if not q.get("cozum"):
                    continue
                k = f"{st['id']}-{q['no']}"
                if st["tur"] == "bosluk":
                    # Boşluklu kök okunmaz: okunuş için soru biçimine çevrilmiş `okunus` (dogrula.py zorunlu tutar)
                    K[f"h-{k}"] = [nokta(oku(q.get("okunus") or re.sub(r"_{2,}", " boşluk ", q["metin"])))]
                    K[f"hc-{k}"] = [nokta(f"Cevap: {oku(q['cevap'])}")] + parcala(re.split(r"(?<=[.!?])\s+", q["cozum"].strip())) + hata_ses(q)
                elif st["tur"] == "dy":
                    K[f"h-{k}"] = [nokta(oku(q["metin"])), "Doğru mu, yanlış mı?"]
                    K[f"hc-{k}"] = parcala(re.split(r"(?<=[.!?])\s+", q["cozum"].strip())) + hata_ses(q)
                else:
                    sec = q["secenekler"]
                    K[f"h-{k}"] = [nokta(oku(q["kok"]))] + [nokta(f"{SIK[h]} şıkkı: {oku(sec[h])}") for h in sec]
                    K[f"hc-{k}"] = [nokta(f"Doğru cevap {SIK[q['dogru']]} şıkkı: {oku(sec[q['dogru']])}")] + parcala(re.split(r"(?<=[.!?])\s+", q["cozum"].strip())) + hata_ses(q)
    return K


def hata_ses(q: dict) -> list[str]:
    """Hocanın sorusundaki hata notu: çözümün sonuna okunur (anahtar değiştirilmez)."""
    h = q.get("hata")
    if not h:
        return []
    return parcala(re.split(r"(?<=[.!?])\s+", oku(f"Dikkat, bu soruda bir hata var. {h['hata']} Doğrusu şu: {h['dogrusu']} {h['neden']} Peki neden böyle yazıldı? {h['yazilma']}").strip()))


def main() -> int:
    a = sys.argv[1:]
    modul = a[a.index("--modul") + 1]
    yalniz = tuple(a[a.index("--yalniz") + 1].split(",")) if "--yalniz" in a else None
    K = klipler(modul)
    if yalniz:
        K = {k: v for k, v in K.items() if k.startswith(yalniz)}
    cikti = KOK / "data/ek_moduller/ses" / modul
    dizin_yol = KOK / "src/data/ek_moduller" / modul / "klip.json"
    dizin = json.loads(dizin_yol.read_text()) if dizin_yol.exists() else {}
    ozet = {k: hashlib.sha1("\n".join(v).encode()).hexdigest()[:12] for k, v in K.items()}
    is_ = [k for k in K if dizin.get(k, {}).get("v") != ozet[k] or not (cikti / f"{k}.mp3").exists()]
    harf = sum(len(" ".join(K[k])) for k in is_)
    print(f"{modul}: {len(K)} klip, {len(is_)} üretilecek, ≈{harf / 18 / 60:.0f} dk ses", flush=True)
    if "--kuru" in a:
        for k, v in K.items():
            t = " ".join(v)
            m = re.findall(r"[^\wçğıöşüÇĞİÖŞÜ\s.,;:?!'’-]|\d", t)
            if m:
                print(f"  ŞÜPHELİ {k}: {sorted(set(m))} | {t[:110]}")
        if "--goster" in a:
            for k in list(K)[:400]:
                if k.startswith(tuple(a[a.index("--goster") + 1].split(","))):
                    print(k, "→", " | ".join(K[k]))
        return 0
    cikti.mkdir(parents=True, exist_ok=True)
    import ema_isci as E
    tts = E.model_yukle()
    for n, k in enumerate(is_, 1):
        mp3, _z, sure, notlar = E.parca_uret(tts, {"paragraflar": K[k], "bolumBasi": False}, True)
        (cikti / f"{k}.mp3").write_bytes(mp3)
        dizin[k] = {"v": ozet[k], "sure": round(sure, 2)}
        if n % 10 == 0 or n == len(is_):
            dizin_yol.write_text(json.dumps(dizin, ensure_ascii=False, indent=0))
        E.log(f"[{n}/{len(is_)}] {k}: {sure:.1f} sn {notlar or ''}")
    # artık içerikte olmayan klipler silinir (yalnız tam koşuda)
    if not yalniz:
        for f in cikti.glob("*.mp3"):
            if f.stem not in K:
                f.unlink()
        dizin = {k: v for k, v in dizin.items() if k in K}
    dizin_yol.write_text(json.dumps(dizin, ensure_ascii=False, indent=0))
    E.log(f"tamam: {len(is_)} üretildi, {len(dizin)} klip dizinde")
    return 0


if __name__ == "__main__":
    sys.exit(main())
