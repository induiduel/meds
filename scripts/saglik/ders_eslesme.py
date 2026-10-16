#!/usr/bin/env python3
"""
Sağlık Bakanlığı sekmesi: ders slaytları + çıkmış sorularla eşleşme dizini → src/data/saglik/ders_eslesme.json

Kaynaklar
  - Slaytlar: halk sağlığı destelerinin (baglantilar.json'daki desteler + "Halk Sağlığı" disiplinli desteler) slayt anlatımı,
    cümlelere bölünür.
  - Çıkmış sorular: src/data/saglik/sorular/*.json (Sağlık sekmesine bağlı çıkmış sorular). Metin = soru kökü + (olumlu
    sorularda) doğru şık; "değildir / yanlıştır" türü sorularda doğru şık yanlış bilgi olduğundan alınmaz.

Çıktı (surum 3)
  - cumleler: [{d, s, b, t, y}]  (soru ise ek alanlar q = soru id, qy = sınav yılı, qk = kurul; d = "", s = 0)
  - dizin: kanonik sayı → [[cümle no, başlangıç, bitiş, kendi yılı]]  (kendi yılı: "2013'te 2.10", "2.10 (2013)" gibi sayıya
    bitişik yıl; yoksa 0). Ön yüz (saglikDers.ts) aynı sayıyı + aynı yılı + ortak ad sözcüklerini arar; aynı gösterge ve yıl
    için slaytta FARKLI bir değer varsa onu da bildirir ("slaytta 1,69 yazıyor").
  - terimler: [{t, k, s, q, a?}]  t = görünen ad, k = kök dizisi (eşleştirme), s = slayt cümleleri, q = soru cümleleri,
    a = kısaltma (büyük harf, birebir aranır). Terim yalnız sayfadaki veride + slaytta + (çıkmış soruda / sözlükte /
    slaytta kalın) geçiyorsa alınır; çok genel sözcükler ve süs büyük harfler elenir.

Çalıştırma: python3 scripts/saglik/ders_eslesme.py [--rapor]   (baglantilari_kur.py'den sonra)
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
DESTELER = KOK / "src/data/interactive_learning_decks.json"
SAGLIK = KOK / "src/data/saglik"
BAG = SAGLIK / "baglantilar.json"
SOZLUK = KOK / "src/data/medical_glossary.json"
CIKTI = SAGLIK / "ders_eslesme.json"
# Sayfada gösterilen veri dosyaları (terimlerin sayfada geçip geçmediği buradan anlaşılır)
DISIPLIN = ("Halk Sağlığı", "Enfeksiyon Hastalıkları", "Kadın Hastalıkları ve Doğum")
SAYFA_VERI = ["karabuk", "turkiye", "asi", "anne_yenidogan", "mevzuat_teskilat", "kavramlar", "havuz"]

SAYI = re.compile(r"(?<![\w.,/])(%\s?)?(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(?![\w])(\s?%|\s?‰)?")
YIL = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")
# Sayının hemen önündeki yıl: "2013'te 2.10", "2022 yılında TDH 1.69", "2025: 1.42"
ONCE_YIL = re.compile(r"(19[5-9]\d|20[0-4]\d)[\s'’:=a-zA-ZçğıöşüÇĞİÖŞÜ()]{0,16}$")
# Sayının hemen ardındaki yıl: "1,42 (2025)", "1,42 ile (2025 yılı)"
SONRA_YIL = re.compile(r"^[\s'’a-zA-ZçğıöşüÇĞİÖŞÜ%‰]{0,8}\(\s*(19[5-9]\d|20[0-4]\d)\b")
OLUMSUZ = re.compile(r"değildir|yanlıştır|yanlış olan|olamaz|bulunmaz|yoktur|dışında|hariç|beklenmez|önerilmez|söylenemez|yer almaz|içermez", re.I)


def kanonik(ham: str) -> str | None:
    """'249.614' → '249614', '7,8' → '7.8', '1.42' → '1.42' (tek nokta + ≠3 hane ondalık sayılır)"""
    s = ham.strip()
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        f = float(s)
    except ValueError:
        return None
    return (f"{f:.6f}".rstrip("0").rstrip(".")) or "0"


def anlamli(ham: str, kan: str, yuzde: bool) -> bool:
    if yuzde or "," in ham or ("." in kan):
        return True
    n = float(kan)
    if 1950 <= n <= 2049 and re.fullmatch(r"\d{4}", ham):
        return False  # yıl
    return n >= 10


SERI = re.compile(r"(19[5-9]\d|20[0-4]\d)\s*[-–]\s*(19[5-9]\d|20[0-4]\d)\s*:\s*")


def kendi_yili(c: str, a: int, b: int) -> int:
    """Sayıya bitişik yıl (önünde ≤16 harf ya da ardında parantez içinde); yoksa 0. saglikDers.ts kendiYili ile aynı kural.
    Ek: "2018-2023: 13,5 → 13 → 13 → 13 → 12,6 → 13,5" dizisinde sıradaki yıl."""
    for m in SERI.finditer(c):
        y1, y2 = int(m.group(1)), int(m.group(2))
        parca = c[m.end():]
        okli = re.split(r"\s*→\s*", parca)
        if len(okli) >= 3 and y2 - y1 + 1 == len(okli):
            konum = m.end()
            for i, o in enumerate(okli):
                if konum <= a < konum + len(o):
                    return y1 + i
                konum += len(o)
                konum += len(re.match(r"\s*→\s*", c[konum:]).group()) if re.match(r"\s*→\s*", c[konum:]) else 0
    on = c[max(0, a - 22):a]
    m = ONCE_YIL.search(on)
    if m and not re.search(r"\d", on[m.end(1):]):
        return int(m.group(1))
    m = SONRA_YIL.search(c[b:b + 24])
    return int(m.group(1)) if m else 0


def temizle(t: str) -> str:
    t = re.sub(r"\*\*|==|__|`|#+\s*", "", t or "")
    t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\(times|cdot)", lambda m: "×" if m.group(1) == "times" else "·", t).replace("$", "")
    t = re.sub(r"^\s*>\s*\[![A-Z]+\]\s*", "", t, flags=re.M)
    return t


def cumleler(t: str) -> list[str]:
    parcalar: list[str] = []
    for satir in re.split(r"\n+", t):
        satir = re.sub(r"^\s*[-*•]\s*", "", satir).strip()
        if not satir:
            continue
        # Sayılardaki noktayı bölme ("7.8", "249.614"): nokta + boşluk + büyük harf / satır sonu
        for c in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9(])", satir):
            c = c.strip()
            if c:
                parcalar.append(c)
    return parcalar


def kisalt(c: str, bas: int, son: int, uzun: int = 240) -> tuple[str, int, int]:
    """Cümle çok uzunsa sayının çevresinden kes; sayının yeni konumunu da döndür"""
    if len(c) <= uzun:
        return c, bas, son
    sol = max(0, bas - uzun // 2)
    sag = min(len(c), sol + uzun)
    sol = max(0, sag - uzun)
    on = "… " if sol > 0 else ""
    arka = " …" if sag < len(c) else ""
    return on + c[sol:sag] + arka, bas - sol + len(on), son - sol + len(on)


# ---------------------------------------------------------------------------------------------------------------
# Terimler — saglikDers.ts'deki terimKatla / terimKoku / sozcukler ile birebir aynı kurallar
# ---------------------------------------------------------------------------------------------------------------
HARF = "A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû"
SOZCUK = re.compile(rf"[{HARF}]+(?:['’][{HARF}]+)?")


def terim_katla(s: str) -> str:
    """Türkçe küçük harf + aksan katlama; ğ → k (sağlık / sağlığı aynı köke düşsün)"""
    s = s.replace("İ", "i").replace("I", "ı").lower()
    tablo = str.maketrans({"ı": "i", "ş": "s", "ç": "c", "ğ": "k", "ö": "o", "ü": "u", "â": "a", "î": "i", "û": "u"})
    return s.translate(tablo)


def terim_koku(w: str) -> str:
    """Kök: kısa sözcük olduğu gibi, uzun sözcüğün ilk ~%75'i (en az 4 harf): 'merkezi' → 'merkez', 'dispanseri' → 'dispanse'"""
    return w if len(w) <= 4 else w[: max(4, math.ceil(len(w) * 0.75))]


def sozcukler(s: str) -> list[tuple[str, str, int, int]]:
    """(özgün sözcük — kesme ekinden önce, katlanmış, başlangıç, bitiş)"""
    out = []
    for m in SOZCUK.finditer(s):
        w = re.split(r"['’]", m.group())[0]
        out.append((w, terim_katla(w), m.start(), m.start() + len(w)))
    return out


def ardisik(s: str) -> list[list[tuple[str, str, int, int]]]:
    """Aralarında yalnız boşluk/tire olan sözcük dizileri (noktalama diziyi böler)"""
    diziler: list[list] = []
    cur: list = []
    son = -1
    for x in sozcukler(s):
        if cur and not re.fullmatch(r"[\s\-]*", s[son:x[2]]) and not re.fullmatch(r"['’][^\s]*\s*", s[son:x[2]]):
            diziler.append(cur)
            cur = []
        cur.append(x)
        son = x[3]
    if cur:
        diziler.append(cur)
    return diziler


def eslesir(sayfa: str, terim: str, tek: bool = False) -> bool:
    """Sayfa sözcüğü (katlanmış) terim sözcüğünün köküyle başlar ve çok uzamaz. Tek sözcüklü terimde sözcüğün tamamı
    aranır ("servisit" ≠ "servisi")"""
    if tek and len(terim) > 4:
        return sayfa.startswith(terim) and len(sayfa) <= len(terim) + 6
    k = terim_koku(terim)
    if len(terim) <= 4:
        return sayfa == terim or (sayfa.startswith(terim) and len(sayfa) - len(terim) <= 4 and len(terim) >= 3)
    return sayfa.startswith(k) and len(sayfa) <= len(terim) + 6


GENEL = set("""
saglik saglikli hizmet hizmeti hizmetleri merkez merkezi il ilce turkiye karabuk yil yili yillik sayi sayisi oran orani hiz hizi
toplam genel bakanlik bakanligi mudurluk mudurlugu kurum kurumu birim birimi program programi veri bilgi tablo kaynak durum
alan konu tur cesit grup grubu bolum kisim yer zaman sure donem gun hafta ay saat yas kisi insan nufus erkek kadin cocuk bebek
yeni eski ilk son buyuk kucuk yuksek dusuk fazla az daha cok en her bazi tum diger ayni onemli temel ana yan ust alt ic dis
artis azalma dusus yukselis deger degeri olcum duzey duzeyi seviye kademe basamak tanim ozet sonuc not ornek amac hedef
kontrol risk etki etken neden sonra once kadar gore icin ile veya bir bu su o ve de da ki mi
hafta haftalar haftasi gunler aylar arasi arasinda tarafindan kez kim ne nereden hicbir tek orta tip tipler oda kisilik
uygulama uygulamalar yontem yontemler yontemi amac amaclar degisiklik ornek ornekler ornekleme kavram kavramlar madde maddeler
danisma genisleme karsilastirma maliyet siklik kriter teknik niteligi gorevleri gorunum hareket bakim izlem izlemi
""".split())
# Tek sözcükte istenmeyen ekler (çoğul, bulunma/ayrılma, yüklem, mastar): "Annede", "Kazalar", "yanlıştır", "İzlemek"
EK = ("lar", "ler", "lari", "leri", "de", "da", "te", "ta", "den", "dan", "ten", "tan", "dir", "tir", "dur", "tur", "maz", "mez",
      "mak", "mek", "masi", "mesi", "ndan", "nden", "nda", "nde", "si", "su", "ini", "ina", "ine", "dur", "abilir", "ebilir", "ir", "ur")
# Elle elenen terimler (katlanmış, boşlukla): genel/bağlamsız ifadeler
RED = {"kadin dogum", "tarama araci", "saglik personeli", "diger saglik personeli", "risk faktoru", "bulasici hastalika",
       "enfeksiyon hastaliki", "dikkat", "kokeni", "yonunu", "sirala", "siralama", "tarihce", "yararlanma", "yorumlama",
       "zorunluluk", "baslatici", "siniflama", "boyama", "dayanikli", "hareket", "bebek ve cocuklar", "kucuk cocuklar ve anneleri",
       "etkili faktorler", "duzenleme", "ikincil", "ucuncul", "niteliki", "sinirlama", "istege bakli", "ongoru", "geri bildirim", "abd",
       "yasini doldurmadan", "hastanede kalis", "hizmet sunumu", "hastalikin nedeni", "hedef kitle", "etiyoloji", "poliklinik",
       "sayili kanun", "isyeri"}
YASAK = {"tuik", "karabuk", "turkiye", "tc", "ii", "iii", "iv", "vi", "tl", "iu", "pm", "no", "im", "sc", "ml", "mg", "kg", "cm", "mm", "dk", "sn", "ozeti",
         "proto", "not", "pdf", "url", "web"}


def kok_dizisi(s: str) -> list[str]:
    return [x[1] for x in sozcukler(s)]


def main() -> None:
    rapor = "--rapor" in sys.argv
    desteler = json.loads(DESTELER.read_text(encoding="utf-8"))
    bag = json.loads(BAG.read_text(encoding="utf-8"))
    kisa: dict[str, str] = {}
    for b in bag.get("bolumler", {}).values():
        for d in b.get("desteler", []):
            kisa[d["id"]] = d.get("kisa") or d.get("baslik") or d["id"]
    # Sağlık sekmesine bağlı desteler + Halk Sağlığı + aşı/salgın/anne-çocuk bölümlerinin dersleri (Enfeksiyon, Kadın Doğum)
    secili = [d for d in desteler if d.get("id") in kisa or any(x in (d.get("discipline") or "") for x in DISIPLIN)]
    # Aynı cümle birden çok destede varsa ilk deste yazılır: sitenin bağladığı (en yeni sürüm) desteler önce, eski "learn-*" sonra
    secili.sort(key=lambda d: (d.get("id") not in kisa, str(d.get("id", "")).startswith("learn-"), not str(d.get("id", "")).endswith("-v2")))

    # Cümleler bir kez saklanır; dizin sayı → [[cümle no, başlangıç, bitiş, kendi yılı], …]
    cumle_l: list[dict] = []
    gorulen: set[str] = set()
    deste_ad: dict[str, str] = {}
    dizin: dict[str, list[list[int]]] = {}
    # Terim taraması için tüm slayt cümleleri (sayısız olanlar da); cümle listesine yalnız terim bağlanırsa girer
    tum_slayt: list[dict] = []
    ham_slayt: list[str] = []

    def cumle_ekle(kayit: dict) -> int:
        no = len(cumle_l)
        cumle_l.append(kayit)
        return no

    def sayilari_isle(c: str) -> list[tuple[str, int, int, int]]:
        bulunan = []
        for m in SAYI.finditer(c):
            ham = m.group(2)
            kan = kanonik(ham)
            if kan and anlamli(ham, kan, bool(m.group(1) or m.group(3))):
                bulunan.append((kan, m.start(2), m.end(2), kendi_yili(c, m.start(2), m.end(2))))
        return bulunan

    for d in secili:
        did = d["id"]
        deste_ad[did] = kisa.get(did) or d.get("shortTitle") or d.get("title") or did
        for i, s in enumerate(d.get("slides") or []):
            ham = s.get("synthesisNarrative") or s.get("content") or ""
            ham_slayt.append(ham + "\n" + (s.get("title") or ""))
            metin = temizle(ham)
            baslik = (s.get("title") or "").strip()[:110]
            for c in cumleler(metin):
                bulunan = sayilari_isle(c)
                if bulunan and len(c) > 260:  # uzun cümle: ilk sayının çevresi
                    t, _, _ = kisalt(c, bulunan[0][1], bulunan[0][2], 260)
                    kay = t.index(c[bulunan[0][1]:bulunan[0][2]]) - bulunan[0][1] if c[bulunan[0][1]:bulunan[0][2]] in t else 0
                    bulunan = [(k, a + kay, b + kay, y) for k, a, b, y in bulunan if 0 <= a + kay and b + kay <= len(t) and t[a + kay:b + kay] == c[a:b]]
                    c = t
                ozet = re.sub(r"\W+", "", c.lower())[:200]
                # Aynı cümle destenin eski/yeni sürümünde tekrar ediyorsa bir kez (ilk deste) yazılır
                if ozet in gorulen:
                    continue
                gorulen.add(ozet)
                kayit = {"d": did, "s": i + 1, "b": baslik, "t": c if len(c) <= 300 else c[:297] + " …",
                         "y": sorted(set(YIL.findall(c)) | set(YIL.findall(baslik)))}
                if bulunan:
                    no = cumle_ekle(kayit)
                    for kan, a, b, y in bulunan:
                        dizin.setdefault(kan, []).append([no, a, b, y])
                    kayit["_no"] = no
                tum_slayt.append(kayit)

    # ---- çıkmış sorular
    sorular: dict[str, dict] = {}
    for f in sorted((SAGLIK / "sorular").glob("*.json")):
        for q in json.loads(f.read_text(encoding="utf-8")):
            sorular.setdefault(q["id"], q)
    soru_kayit: list[dict] = []
    for q in sorular.values():
        kok = re.sub(r"\s*\n\s*", " / ", (q.get("kok") or "").strip())
        if not kok:
            continue
        dogru = next((o.get("t") or "" for o in q.get("secenekler") or [] if o.get("k") == q.get("dogru")), "")
        t = kok if (OLUMSUZ.search(kok) or not dogru) else f"{kok} — Doğru cevap: {dogru.strip()}"
        if len(t) > 360:
            t = t[:357] + " …"
        kayit = {"d": "", "s": 0, "b": q.get("konu") or q.get("ders") or "", "t": t, "y": sorted(set(YIL.findall(t))),
                 "q": q["id"], "qy": q.get("yil") or "", "qk": q.get("kurul") or 0}
        bulunan = sayilari_isle(t)
        if bulunan:
            no = cumle_ekle(kayit)
            kayit["_no"] = no
            for kan, a, b, y in bulunan:
                dizin.setdefault(kan, []).append([no, a, b, y])
        soru_kayit.append(kayit)

    # ---- terimler
    kucuk = Counter()
    for t in ham_slayt:
        for w, f, _, _ in sozcukler(t):
            if w.islower():
                kucuk[f] += 1
    aday: dict[tuple[str, ...], dict] = {}

    def aday_ekle(gorunen: str, tur: str) -> None:
        gorunen = re.sub(r"\s+", " ", gorunen).strip(" -–:;,.")
        gorunen = re.sub(r"['’][a-zçğıöşü]+$", "", gorunen)  # "Doğum Öncesi Bakım'dır" → "Doğum Öncesi Bakım"
        sz = sozcukler(gorunen)
        if not sz or len(sz) > 6:
            return
        k = tuple(x[1] for x in sz)
        if " ".join(k) in RED or gorunen.startswith(("'", "’")):
            return
        if tur == "kisa":
            if sz[0][1] in YASAK:
                return
        else:
            harf = sum(len(x) for x in k)
            if any(x in YASAK for x in k):
                return
            if len(k) == 1 and (harf < 6 or k[0] in GENEL):
                return
            if len(k) > 1 and (harf < 10 or all(x in GENEL or len(x) <= 2 for x in k)):
                return
            if k[0] in GENEL and len(k[0]) <= 3 or k[-1] in {"ve", "ile", "veya", "icin", "de", "da"}:
                return
        a = aday.setdefault(k, {"t": gorunen, "tur": set()})
        a["tur"].add(tur)

    for t in ham_slayt:
        for m in re.finditer(r"\*\*([^*\n]{3,80})\*\*(\s*:)?", t):
            if m.group(2):
                continue  # "**Tanım:**" gibi etiket
            b = re.sub(r"\([^)]*\)", "", m.group(1))
            b = re.sub(r"[\d%.,:;‰–\-/]+", " ", b)
            aday_ekle(b, "kalin")
        # Kısaltmalar: büyük harf, küçük harfli sözcük olarak hiç geçmiyor, en az bir kez parantezde / tanım yanında
        for m in re.finditer(r"(?<![\wÇĞİÖŞÜçğıöşü])([A-ZÇĞİÖŞÜ]{3,6})(?![\wÇĞİÖŞÜçğıöşü])", t):
            w = m.group(1)
            if kucuk[terim_katla(w)]:
                continue
            on, ar = t[max(0, m.start() - 2):m.start()], t[m.end():m.end() + 2]
            komsu = t[max(0, m.start() - 30):m.start()] + t[m.end():m.end() + 30]
            if "(" in on or ar.strip().startswith("(") or ")" in ar or re.search(r"[a-zçğıöşü]{3,}", komsu):
                aday_ekle(w, "kisa")
        # Özel ad dizileri: "Sağlıkta Dönüşüm Programı", "Umumi Hıfzıssıhha Kanunu"
        for dz in ardisik(re.sub(r"\*\*", "", t)):
            run: list = []
            for x in dz + [None]:
                if x and ((x[0][:1].isupper() and not x[0].isupper()) or (run and x[1] == "ve")):
                    run.append(x)
                    continue
                while run and run[-1][1] == "ve":
                    run.pop()
                if 2 <= len(run) <= 6:
                    aday_ekle(" ".join(y[0] for y in run), "ozel")
                run = []
    try:
        sozluk = json.loads(SOZLUK.read_text(encoding="utf-8"))
        for g in sozluk.values():
            aday_ekle(re.sub(r"\([^)]*\)", "", g.get("term") or ""), "sozluk")
    except FileNotFoundError:
        pass

    # Terimin geçtiği yerler (kök dizisi ardışık sözcüklerde)
    def bul(metin_diziler: list[list[tuple[str, str, int, int]]], k: tuple[str, ...], kisaltma: str | None) -> bool:
        n = len(k)
        for dz in metin_diziler:
            for i in range(len(dz) - n + 1):
                if kisaltma:
                    if dz[i][0] == kisaltma:
                        return True
                    continue
                if all(eslesir(dz[i + j][1], k[j], n == 1) for j in range(n)):
                    return True
        return False

    # İlk sözcüğe göre kova (hız)
    def kova(kayitlar: list[tuple[int, list]]) -> dict[str, list[int]]:
        out: dict[str, list[int]] = {}
        for idx, diz in kayitlar:
            for dz in diz:
                for x in dz:
                    out.setdefault(x[1][:3], []).append(idx)
        return {k: sorted(set(v)) for k, v in out.items()}

    slayt_diz = [(i, ardisik(r["t"])) for i, r in enumerate(tum_slayt)]
    soru_diz = [(i, ardisik(r["t"])) for i, r in enumerate(soru_kayit)]
    sayfa_metin: list[str] = []

    def metinler(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("kaynak", "konum", "id", "kod", "url", "tarih", "kaynaklar", "sorular", "ek"):
                    continue
                yield from metinler(v)
        elif isinstance(o, list):
            for v in o:
                yield from metinler(v)

    # Sayfada geçen sayılar (metindeki sayılar + verideki sayısal değerler): dizin yalnız bunları tutar
    sayfa_sayi: set[str] = set()

    def sayisal(o):
        if isinstance(o, bool):
            return
        if isinstance(o, (int, float)):
            sayfa_sayi.add(f"{float(o):.6f}".rstrip("0").rstrip(".") or "0")
        elif isinstance(o, dict):
            for v in o.values():
                sayisal(v)
        elif isinstance(o, list):
            for v in o:
                sayisal(v)

    for ad in SAYFA_VERI:
        p = SAGLIK / f"{ad}.json"
        if p.exists():
            veri = json.loads(p.read_text(encoding="utf-8"))
            sayfa_metin += list(metinler(veri))
            sayisal(veri)
    for t in sayfa_metin:
        for m in SAYI.finditer(t):
            k = kanonik(m.group(2))
            if k:
                sayfa_sayi.add(k)
    sayfa_diz = [(i, ardisik(t)) for i, t in enumerate(sayfa_metin)]
    k_slayt, k_soru, k_sayfa = kova(slayt_diz), kova(soru_diz), kova(sayfa_diz)
    sd, qd, pd = dict(slayt_diz), dict(soru_diz), dict(sayfa_diz)

    def yerler(k: tuple[str, ...], kisaltma: str | None, kv: dict, dz: dict) -> list[int]:
        bas = terim_katla(kisaltma)[:3] if kisaltma else k[0][:3]
        return [i for i in kv.get(bas, []) if bul(dz[i], k, kisaltma)]

    terimler: list[dict] = []
    elenen = Counter()
    for k, a in aday.items():
        kisaltma = a["t"] if a["tur"] == {"kisa"} else None
        s_yer = yerler(k, kisaltma, k_slayt, sd)
        if not s_yer:
            elenen["slaytta yok"] += 1
            continue
        if len(s_yer) > 60 and not kisaltma:
            elenen["slaytta çok genel"] += 1
            continue
        p_yer = yerler(k, kisaltma, k_sayfa, pd)
        if not p_yer:
            elenen["sayfada yok"] += 1
            continue
        q_yer = yerler(k, kisaltma, k_soru, qd)
        destek = bool(q_yer) or "sozluk" in a["tur"] or "kalin" in a["tur"] or kisaltma is not None
        if not destek:
            elenen["destek yok"] += 1
            continue
        # Tek sözcük: sözlükte olmalı ya da (kalın + çıkmışta + ekli/genel değil); kalın tek sözcükler çoğu zaman etiket
        if len(k) == 1 and not kisaltma and "sozluk" not in a["tur"]:
            if not q_yer or len(s_yer) > 35 or k[0].endswith(EK) or k[0] in GENEL:
                elenen["tek sözcük, destek zayıf"] += 1
                continue
        # Çok sözcüklü: en az bir içerik sözcüğü (≥5 harf, genel değil); son sözcük yüklem/zaman eki taşımasın
        if len(k) > 1 and not any(len(x) >= 5 and x not in GENEL for x in k):
            elenen["çok sözcük, içerik yok"] += 1
            continue
        if len(k) > 1 and (k[-1] in GENEL and len(k) == 2 or re.search(r"(dir|dır|tir|tır|dur|tur|maz|mez|ir|ur|ar|er)$", k[-1]) and "sozluk" not in a["tur"] and "ozel" not in a["tur"]):
            elenen["çok sözcük, yüklem/genel son"] += 1
            continue
        # Slayt cümlesi: kalın geçtiği / kısa ve tanım gibi olanlar önce
        def puan(i: int) -> tuple:
            r = tum_slayt[i]
            return (len(r["t"]) > 220, len(r["t"]))
        s_sec = sorted(s_yer, key=puan)[:3]
        nolar = []
        for i in s_sec:
            r = tum_slayt[i]
            if "_no" not in r:
                r["_no"] = cumle_ekle(r)
            nolar.append(r["_no"])
        q_nolar = []
        for i in q_yer[:3]:
            r = soru_kayit[i]
            if "_no" not in r:
                r["_no"] = cumle_ekle(r)
            q_nolar.append(r["_no"])
        oge = {"t": a["t"], "k": list(k), "s": nolar, "q": q_nolar, "n": len(s_yer), "nq": len(q_yer)}
        if kisaltma:
            oge["a"] = kisaltma
        terimler.append(oge)
    # Uzun terim önce (sayfada en uzun eşleşme kazanır)
    terimler.sort(key=lambda x: (-len(x["k"]), x["t"]))
    # Sayfada hiç geçmeyen sayıların dizini ve yalnız onlara bağlı cümleler atılır (dosya küçülür); cümleler yeniden numaralanır
    # (yıla bitişik sayılar kalır: sayfadaki aynı yılın farklı değeriyle karşılaştırılır — "slaytta 1,69 yazıyor")
    dizin = {k: (v if k in sayfa_sayi else [e for e in v if e[3]]) for k, v in dizin.items()}
    dizin = {k: v for k, v in dizin.items() if v}
    kullanilan = sorted({e[0] for l in dizin.values() for e in l} | {n for t in terimler for n in t["s"] + t["q"]})
    yeni_no = {eski: i for i, eski in enumerate(kullanilan)}
    cumle_l = [cumle_l[i] for i in kullanilan]
    for l in dizin.values():
        for e in l:
            e[0] = yeni_no[e[0]]
    for t in terimler:
        t["s"] = [yeni_no[n] for n in t["s"]]
        t["q"] = [yeni_no[n] for n in t["q"]]
    # Slayt başlıkları bir kez yazılır (cümlede başlık numarası); ön yüz yüklerken geri açar
    basliklar: list[str] = []
    bno: dict[str, int] = {}
    for r in cumle_l:
        r.pop("_no", None)
        b = r.get("b") or ""
        if b not in bno:
            bno[b] = len(basliklar)
            basliklar.append(b)
        r["b"] = bno[b]
        if not r.get("y"):
            r.pop("y", None)
    cikti = {"surum": 3, "uretim": date.today().isoformat(), "desteler": deste_ad, "basliklar": basliklar, "cumleler": cumle_l, "dizin": dizin, "terimler": terimler}
    CIKTI.write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(secili)} deste · {len(soru_kayit)} çıkmış soru · {len(dizin)} farklı sayı · {len(terimler)} terim · "
          f"{len(cumle_l)} cümle → {CIKTI.relative_to(KOK)} ({CIKTI.stat().st_size // 1024} KB)")
    if rapor:
        print("elenen adaylar:", dict(elenen))
        for t in sorted(terimler, key=lambda x: -x["nq"]):
            print(f"  {t['t']!r:45} slayt {t['n']:3} · çıkmış {t['nq']:3}{' · kısaltma' if 'a' in t else ''}")


if __name__ == "__main__":
    main()
