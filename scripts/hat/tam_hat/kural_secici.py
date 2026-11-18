#!/usr/bin/env python3
"""Aşama başına kural özeti + okuma haritası (tam içerik hattı; kullanıcı kararı 2026-10-28, daraltma 2026-11-16).

Hata defteri (docs/KURUL2_YAPILMAYACAK_HATALAR.md = DİZİN, tam metin docs/hatalar/<konu>.md) her alt ajana bütünüyle
okutulmaz. Bu betik dizin sırasıyla konu dosyalarındaki maddeleri ayrıştırır ve her maddeyi EN İLGİLİ aşamaya dağıtır:

  kural_secici.py                     → docs/asama_kurallari/<aşama>.md yeniden üretilir
  kural_secici.py --denetle           → dizin ↔ konu dosyası tutarlılığı + özet bayatlığı + MADDE KAYBI denetimi (kayıp → çıkış 1)
  kural_secici.py --oku <aşama>       → o aşamada okunacak dosyaların listesi (alt ajan istemine)
  kural_secici.py --ozet <aşama>      → o aşamanın en sık tekrarlanan 5–7 hatası (≤300 kelime; istemin başına)
  kural_secici.py --paket <aşama|denetci|hepsi> [--mod tasarruf] [--yaz <klasör>]
                                      → aşamanın TEK okuma dosyası (özet + kurallar + standart belgelerin yalnız ilgili bölümleri)
  kural_secici.py --tam <aşama|H<n>>  → kısaltılmamış (kapılı maddeler dahil TAM metin) aşama özeti ya da tek madde

Daraltma (2026-11-16, ölçüm: aşama başına 11–15k kelime; 1171 başlığın yalnız 343'ü benzersizdi, `"soru"` anahtarı
örnek soruya 164 madde çekiyordu):
  1. Madde → aşama: konu dosyası önceliği (KONU_ONCELIK, +3) + ÖZGÜL anahtar sözcük puanı (başlıkta 2, kural satırında 1).
     En yüksek puanlı aşama alınır; ikinci aşama yalnız puanı ≥ ESIK_IKINCI × birinci ise eklenir (en çok 2). Üç ve daha
     çok aşamaya eşit ilgili madde "genel"e gider. Puanı ESIK_MIN altında kalan ve hat konusu olmayan madde (ön yüz,
     yönetim, altyapı) "genel"de konu başına TEK satırlık kimlik listesine iner — içerik aşamasını ilgilendirmez.
  2. Kapılı madde (kural satırında `betik.py` adı + "kapı" geçen, yani betikle denetlenen) aşama çıktısında tek satırdır:
     `- H<no> <başlık> — betik denetler: <kapı>`. Kapı kısmi ise ("yakalamaz", "denetçi", "elle") tam metin kalır.
     Tam metin `--tam` ile ve docs/hatalar/<konu>.md'de erişilebilir.
  3. Kural metni değiştirilmez: tam metin basılan maddede başlık + ileri-kural satırları (Kural/Doğrusu/Önleme/Kapı) aynen.
  4. Hiçbir madde kaybolmaz: --denetle her dizin maddesinin en az bir çıktı dosyasında (tam ya da tek satır) geçtiğini
     dosya içeriğinden doğrular; önce (dizin) / sonra (çıktı) kimlik kümesini basar.
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import re
import sys
from dataclasses import dataclass, field

KOK = _kok.MEDS
DEFTER = KOK / "docs/KURUL2_YAPILMAYACAK_HATALAR.md"  # dizin: "- **H<n>** · özet → hatalar/<konu>.md" (sıra = madde sırası)
HATALAR = KOK / "docs/hatalar"                           # konu dosyaları: "## "/"### " başlığı = madde sınırı (tam metin)
DIZIN_SATIR = re.compile(r"^- \*\*(.+?)\*\* · .* → hatalar/([\w]+)\.md$")
CIKIS = KOK / "docs/asama_kurallari"

# Aşama → (ÖZGÜL anahtar sözcükler, defter dışında okunacak dosyalar). Sözcük başı sınırıyla aranır ("ema" ≠ "tema").
# Geniş sözcükler ("soru", "tablo", "denetçi", "taslak", "onem") bilinçli olarak YOK: her maddeye eşleşip aşamayı şişiriyordu.
ASAMALAR: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "kaynak": (("hoca dök", "hoca_dokum", "ses kaydı", "öğrenci not", "ogrenci_not", "öğrenci önem", "ogrenci_onem",
                "çıkmış eşle", "cikmis_konum", "cikmis_eslesme", "hizala", "drive", "degerlendirme", "değerlendirme paket",
                "hoca vurgu", "paket.json", "atom"),
               ("docs/KURUL2_DERS_STANDARDI.md", "docs/HOCA_TAHMIN_REHBERI.md", "docs/OGRENCI_ONEM_YONTEMI.md")),
    "anlatim": (("anlatım", "konusma_v2", "metin_denetle", "dolgu", "türkçe", "turkce_uslup", "üslup", "tanımsız",
                 "kronoloji", "sesli yazar", "v2 cümle"),
                ("docs/ANLATIM_KURGU_STANDARDI.md", "docs/TURKCE_USLUP_STANDARDI.md", "docs/KURUL2_DERS_STANDARDI.md",
                 "docs/OGRENCI_ONEM_YONTEMI.md")),
    "ses": (("ema", "xtts", "seslendir", "cümle zaman", "kelime zaman", "cumle_zaman", "kelime_zaman", "okunuş", "klip"), ()),
    "capa_cizim": (("çapa", "capa", "çizim", "cizim", "lazer", "kontur", "panel_sinama", "pdf işareti", "imleç"),
                   ("docs/CIZIM_KURALLARI.md", "scripts/uretim/cizim/TALIMAT_CIZIM.md")),
    "ders_icerik": (("ders_icerik", "içerik paketi", "terim", "kısaltma", "sıralı tablo", "karşılaştırma tablo", "sözlük"),
                    ("docs/DERS_ICERIK_BICIMI.md",)),
    "ogren_deste": (("öğren deste", "öğren destesi", "deste", "cloze", "micro_quiz", "etkileşim", "oyun", "checkpoint",
                     "validate_learning", "quiz"),
                    ("docs/OGREN_ETKILESIM_REHBERI.md",)),
    "ornek_soru": (("örnek soru", "ornek_soru", "şık", "sik_aciklama", "çeldirici", "çözücü", "cozucu", "önem listesi",
                    "onem_dogrula", "soru kökü", "ara soru", "hoca_ara", "soru_uslup", "spot"),
                   ("docs/SIK_ACIKLAMA_STANDARDI.md", "docs/SORU_USLUBU.md", "docs/HOCA_USLUBU_YONTEMI.md",
                    "scripts/uretim/hoca_ara_soru/TALIMAT.md", "docs/OGRENCI_ONEM_YONTEMI.md")),
    "pdf_tasarim": (("ders pdf", "pdf'i", "yazdır", "css", "taşma", "taşıyor", "mobil", "rozet", "boş sayfa",
                     "kenar boşluğu", "üst üste", "pdf_tarama", "dışa aktar"),
                    ("docs/DERS_ICERIK_BICIMI.md",)),
    "yayin": (("dağıt", "dagit", "oracle", "rsync", "commit", "push", "yayın", "guncelleme_notu", "birleştir", "canlı doğrula"),
              ("docs/KURUL_OTOMASYON_EL_KITABI.md",)),
}
# Konu dosyası → asıl aşama (+3 puan). None = hat dışı konu (ön yüz/yönetim/altyapı): yalnız anahtar puanı ESIK_MIN'i
# geçerse bir aşamaya düşer, yoksa "genel"de tek satırlık kimlik listesine iner.
KONU_ONCELIK: dict[str, str | None] = {
    "soru_cozucu": "ornek_soru", "ders_metni_anlatim": "anlatim", "ses": "ses", "cizim": "capa_cizim",
    "ders_metni_terim_kisaltma": "ders_icerik", "ders_metni_degerlendirme": "kaynak", "veri_cikmis": "kaynak",
    "ogren_modul_oyun": "ogren_deste", "on_yuz_disa_aktarim": "pdf_tasarim", "dagitim_sunucu": "yayin",
    "dagitim_icerik_katmani": "yayin", "diger": "genel",
    "on_yuz_oynatici_ders": None, "on_yuz_sayfa_denetimi": None, "on_yuz_tasarim_tema": None,
    "yonetim_basarim": None, "betik_altyapi": None,
}
ONCELIK_PUAN = 3
ESIK_MIN = 3          # öncelik yoksa bir aşamaya düşmek için gereken en az puan
ESIK_IKINCI = 0.75    # ikinci aşama: puan ≥ 0.75 × birinci (ve ≥ ESIK_MIN); üçüncü de geçerse → genel

KURAL_ETIKET = re.compile(r"^- \*\*(Kural|Kurul 2'de doğrusu|Önleme|Çözüm|Kalıcı çözüm|Kapı|Doğrusu)[^*]*\*\*", re.I)
# İleriye-dönük (bir ürün yazan ajana GEREKEN) etiketler. "Çözüm/Kalıcı çözüm" geçmiş kod-hatası düzeltme anlatısıdır;
# özete girmez — yalnız maddede başka ileri-kural yoksa korunur (madde kaybolmasın). (kullanıcı kararı 2026-11-16)
ILERI_ETIKET = ("kural", "kurul 2'de doğrusu", "doğrusu", "önleme", "kapı")
BETIK = re.compile(r"`([\w./-]*\.(?:py|mts|mjs|sh|ts))\b[^`]*`")
KISMI_KAPI = re.compile(r"yakalamaz|denetçi|elle|kapı yok|kapısı yok|açık iş|eklenmedi", re.I)
# --ozet ölçütü izleri: aynı sınıfın tekrar / düzeltilemeyip kalma / yeniden yazım belirtileri.
TEKRAR_IZ = re.compile(r"KALIR|yeniden yaz|tekrar", re.I)
OZET_N, OZET_KELIME = 7, 300


@dataclass
class Madde:
    kim: str            # dizindeki kimlik (H123 / — / H)
    konu: str           # docs/hatalar/<konu>.md
    baslik: str
    metin: str          # tam gövde
    kural: list[str]    # kural satırları (etiketli bloklar ya da düz metin)
    asamalar: list[str] = field(default_factory=list)
    kapi: str | None = None

    @property
    def no(self) -> str:
        m = re.match(r"(H\d+[a-z]?)", re.sub(r"^#+ ", "", self.baslik))
        return m.group(1) if m else ""

    def tek_satir(self) -> str:
        b = re.sub(r"^#+ ", "", self.baslik).strip()
        return f"- {b} — betik denetler: `{self.kapi}`"

    def tam(self) -> str:
        govde = "\n".join(_ileri_filtre(self.kural)) if self.kural else "- (kural satırı yok; ayrıntı defterde)"
        return f"### {self.baslik}\n{govde}\n"

    def cikti(self) -> str:
        return self.tek_satir() if self.kapi else self.tam()


def _ileri_filtre(kural: list[str]) -> list[str]:
    """Kural satır bloklarını ileri-kural (Kural/Doğrusu/Önleme/Kapı) ile sınırla; hiç yoksa ilk bloğu bırak."""
    bloklar: list[dict] = []
    for s in kural:
        if s.startswith("- **"):
            m = re.match(r"- \*\*([^:*]+)", s)
            bloklar.append({"tag": (m.group(1).strip().lower() if m else ""), "satir": [s]})
        elif bloklar:
            bloklar[-1]["satir"].append(s)
    ileri = [b for b in bloklar if any(b["tag"].startswith(t) for t in ILERI_ETIKET)]
    secili = ileri if ileri else bloklar[:1]
    return [l for b in secili for l in b["satir"]]


def _kimlik(baslik: str) -> str:
    t = re.sub(r"^#+ ", "", baslik)
    m = re.match(r"(H\d+[a-z]?(?:\s*[–/-]\s*H?\d+[a-z]?)*(?:,\s*H\d+[a-z]?(?:\s*[–-]\s*H\d+)?)*)(?:\s*\([^)]*\))?", t)
    return m.group(1) if m else ("H" if re.match(r"H\s", t) else "—")


def _birimler() -> list[tuple[str, str, list[str]]]:
    """Dizin sırasıyla (kimlik, konu, madde satırları). Uyuşmazlık HATA (madde kaybolmasın)."""
    birim: dict[str, list[list[str]]] = {}
    for p in sorted(HATALAR.glob("*.md")):
        ls: list[list[str]] = []
        for satir in p.read_text().splitlines():
            if satir.startswith("## ") or satir.startswith("### "):
                ls.append([satir])
            elif ls:
                ls[-1].append(satir)
        birim[p.stem] = ls
    sira = [(m.group(1), m.group(2)) for s in DEFTER.read_text().splitlines() if (m := DIZIN_SATIR.match(s))]
    imlec = {k: 0 for k in birim}
    out: list[tuple[str, str, list[str]]] = []
    hata: list[str] = []
    for kim, konu in sira:
        if konu not in birim or imlec[konu] >= len(birim[konu]):
            hata.append(f"dizinde {kim} → hatalar/{konu}.md ama dosyada karşılık madde yok")
            continue
        b = birim[konu][imlec[konu]]
        imlec[konu] += 1
        if _kimlik(b[0]) != kim:
            hata.append(f"hatalar/{konu}.md sıra uyuşmazlığı: dizin {kim}, dosya {b[0][:60]}")
        out.append((kim, konu, b))
    hata += [f"hatalar/{k}.md: {len(v) - imlec[k]} madde dizinde yok" for k, v in birim.items() if imlec[k] < len(v)]
    if hata:
        raise SystemExit("HATA: hata defteri dizini ↔ konu dosyaları tutarsız:\n  " + "\n  ".join(hata))
    return out


def defter_satirlari() -> list[str]:
    """Geriye uyum: dizin sırasıyla birleşik madde satırları."""
    return [s for _, _, b in _birimler() for s in b]


def _puan(soz: tuple[str, ...], baslik: str, govde: str) -> int:
    p = 0
    for s in soz:
        r = re.compile(r"(?<!\w)" + re.escape(s))
        if r.search(baslik):
            p += 2
        elif r.search(govde):
            p += 1
    return p


def _kapi(kural: list[str]) -> str | None:
    """Betikle denetlenen madde → kapı adı; kapı kısmi/yok ise None (tam metin kalır)."""
    ileri = "\n".join(_ileri_filtre(kural))
    if not re.search(r"kap[ıi]", ileri, re.I) or KISMI_KAPI.search(ileri):
        return None
    for s in ileri.splitlines():
        if re.search(r"kap[ıi]", s, re.I) and (m := BETIK.search(s)):
            return m.group(1)
    m = BETIK.search(ileri)
    return m.group(1) if m else None


def maddeler() -> list[Madde]:
    out: list[Madde] = []
    for kim, konu, b in _birimler():
        bas = re.sub(r"^#+ ", "", b[0]).strip()
        govde = b[1:]
        kural, ici = [], False
        for g in govde:
            if g.startswith("- **"):
                ici = bool(KURAL_ETIKET.match(g))
            if ici:
                kural.append(g)
        if not kural:  # etiketsiz (düz anlatımlı) madde: belirti/kök neden dışındaki satırlar aynen
            kural = [g for g in govde if g.strip() and not re.match(r"- \*\*(Belirti|Görülen|Kök)", g)][:14]
        m = Madde(kim, konu, bas, "\n".join(govde), kural)
        m.kapi = _kapi(kural) if kural else None
        m.asamalar = _ata(m)
        out.append(m)
    return out


def _ata(m: Madde) -> list[str]:
    """Madde → en çok 2 aşama; ['genel'] çok aşamalı; [] = hat dışı (genel'de tek satırlık kimlik listesi)."""
    onc = KONU_ONCELIK.get(m.konu)
    if onc == "genel":
        return ["genel"]
    bas, govde = m.baslik.lower(), "\n".join(m.kural).lower()
    puan = {a: _puan(soz, bas, govde) + (ONCELIK_PUAN if a == onc else 0) for a, (soz, _) in ASAMALAR.items()}
    sira = sorted(puan.items(), key=lambda x: (-x[1], list(ASAMALAR).index(x[0])))
    (a1, p1), (a2, p2), (_, p3) = sira[0], sira[1], sira[2]
    if p1 < ESIK_MIN:
        return [onc] if onc else []
    esik = max(ESIK_MIN, ESIK_IKINCI * p1)
    if p3 >= esik:
        return ["genel"]
    return [a1, a2] if p2 >= esik else [a1]


def _bas(a: str, n: int, ek: str = "") -> str:
    return (f"# Aşama kuralları — {a}\n\n> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç "
            f"`scripts/hat/tam_hat/kural_secici.py`. {n} madde. Tek satırlı maddeleri betik denetler (tam metin: "
            f"`kural_secici.py --tam <H no|aşama>`).{ek}\n\n")


def kovalar(ms: list[Madde], tam: bool = False) -> dict[str, list[str]]:
    kova: dict[str, list[str]] = {a: [] for a in [*ASAMALAR, "genel"]}
    hat_disi: dict[str, list[str]] = {}
    for m in ms:
        if not m.asamalar:
            hat_disi.setdefault(m.konu, []).append(m.no or m.kim)
            continue
        for a in m.asamalar:
            kova[a].append(m.tam() if tam else m.cikti())
    if hat_disi:
        kova["genel"].append("### Hat dışı maddeler (ön yüz/yönetim/altyapı — içerik aşamasını ilgilendirmez; tam metin konu dosyasında)")
        for k, ids in sorted(hat_disi.items()):
            kova["genel"].append(f"- hatalar/{k}.md: {', '.join(ids)}")
    return kova


def uret() -> dict[str, int]:
    CIKIS.mkdir(parents=True, exist_ok=True)
    ms = maddeler()
    for a, liste in kovalar(ms).items():
        (CIKIS / f"{a}.md").write_text(_bas(a, len(liste)) + "\n".join(liste) + "\n", encoding="utf-8")
    return {a: len(l) for a, l in kovalar(ms).items()}


def _tekrar_puani(ms: list[Madde]) -> dict[int, int]:
    """--ozet ölçütü (deterministik): 3 × (bu maddenin H numarasına başka maddelerden yapılan atıf sayısı — aynı sınıfın
    tekrarı) + kendi gövdesindeki KALIR/yeniden yaz/tekrar izi sayısı. Eşitlikte dizin sırası (önce gelen)."""
    tum = [(m.no, m.baslik + "\n" + m.metin) for m in ms]
    out: dict[int, int] = {}
    for i, m in enumerate(ms):
        atif = 0
        if m.no:
            r = re.compile(r"(?<![\w])" + re.escape(m.no) + r"(?![\w])")
            atif = sum(len(r.findall(t)) for j, (_, t) in enumerate(tum) if j != i)
        out[i] = 3 * atif + len(TEKRAR_IZ.findall(m.baslik + "\n" + m.metin))
    return out


def ozet(asama: str) -> str:
    ms = maddeler()
    tp = _tekrar_puani(ms)
    aday = [i for i, m in enumerate(ms) if asama in m.asamalar or (asama == "genel" and m.asamalar == ["genel"])]
    aday.sort(key=lambda i: (-tp[i], i))
    satir = [f"# {asama} — en sık tekrarlanan hatalar (ölçüt: atıf×3 + KALIR/yeniden yazım izi; tam liste "
             f"docs/asama_kurallari/{asama}.md)"]
    for i in aday[:OZET_N]:
        m = ms[i]
        b = " ".join(re.sub(r"\s*\((?:20\d\d|K\d)[^)]*\)", "", m.baslik).split()[:14])
        ilk = next((re.sub(r"^- \*\*[^*]*\*\*:?\s*", "", s).strip() for s in _ileri_filtre(m.kural)
                    if s.strip()), "")
        ilk = " ".join(ilk.split()[:28])
        satir.append(f"- {b} [{tp[i]}]: {ilk}" + (f" (kapı `{m.kapi}`)" if m.kapi else ""))
    while len(" ".join(satir).split()) > OZET_KELIME and len(satir) > 6:
        satir.pop()  # 5 maddenin altına inmeden kelime tavanına sığdır
    return "\n".join(satir)


def tam_cikti(hedef: str) -> str:
    ms = maddeler()
    if hedef in ASAMALAR or hedef == "genel":
        liste = kovalar(ms, tam=True)[hedef]
        return _bas(hedef, len(liste), " TAM SÜRÜM (kapılı maddeler dahil).") + "\n".join(liste)
    bul = [m for m in ms if m.no == hedef or m.kim == hedef]
    if not bul:
        raise SystemExit(f"bulunamadı: {hedef}")
    return "\n".join(f"### {m.baslik}  (hatalar/{m.konu}.md)\n{m.metin}\n" for m in bul)


def kayip_denetle() -> list[str]:
    """Her dizin maddesi en az bir çıktı dosyasında (tam ya da tek satır ya da hat dışı kimlik listesi) geçiyor mu."""
    ms = maddeler()
    icerik = {p.stem: p.read_text(encoding="utf-8") for p in CIKIS.glob("*.md")}
    once = list(range(len(ms)))
    sonra: set[int] = set()
    for i, m in enumerate(ms):
        if not m.asamalar:
            satir = next((s for s in icerik.get("genel", "").splitlines() if s.startswith(f"- hatalar/{m.konu}.md:")), "")
            if re.search(r"(?<![\w])" + re.escape(m.no or m.kim) + r"(?![\w])", satir):
                sonra.add(i)
        elif any(m.cikti() in icerik.get(a, "") for a in m.asamalar):
            sonra.add(i)
    kayip = [f"{ms[i].kim} ({ms[i].konu}): {ms[i].baslik[:70]}" for i in once if i not in sonra]
    tek = sum(1 for m in ms if m.asamalar and m.kapi)
    hd = sum(1 for m in ms if not m.asamalar)
    print(f"madde kümesi: önce (dizin) {len(once)} · sonra (çıktıda) {len(sonra)} · kayıp {len(kayip)} · "
          f"tek satır (kapılı) {tek} · hat dışı kimlik listesi {hd} · tam metin {len(ms) - tek - hd}")
    return kayip


# Yalnız tam modda okunacak (tasarrufta atlanır) belgeler — kullanıcı kararı 2026-11-16.
#  * HOCA_TAHMIN_REHBERI: hoca tahmin katmanı tasarrufta yok (gereksiz token + kanıtsız önem damgası riski).
#  * hoca_ara_soru/TALIMAT: ara soru katmanı tasarrufta üretilmez (mod.py atlar), ama örnek_soru aşaması iki modda da
#    çağrıldığından TALIMAT özete sızıyordu — tasarrufta ölü ağırlık, elenir.
YALNIZ_TAM = {"docs/HOCA_TAHMIN_REHBERI.md", "scripts/uretim/hoca_ara_soru/TALIMAT.md"}


def oku(asama: str, mod: str = "tam") -> list[str]:
    if asama not in ASAMALAR:
        raise SystemExit(f"bilinmeyen aşama: {asama} ({', '.join(ASAMALAR)})")
    dosya = [f"docs/asama_kurallari/{asama}.md", "docs/asama_kurallari/genel.md", *ASAMALAR[asama][1]]
    if mod == "tasarruf":
        dosya = [d for d in dosya if d not in YALNIZ_TAM]
    return [d for d in dosya if (KOK / d).exists()]


# ── Aşama kural PAKETİ (2026-11-17, ölçüm k2-28: aşama girdisinin %60–95'i ders verisi değil, BÜTÜN okutulan standart
# belgelerdi — yayın/denetçi 8,9k kelimenin 6,3k'sı el kitabı; kaynak 6,8k'nın 4,1k'sı iki standart). Paket = aşamanın
# tek dosyası: özet (ilk geçiş öz-denetimi) + aşama kuralları + genel + standart belgelerin YALNIZ o aşamaya ait bölümleri.
# Alt ajan 5–7 dosya yerine TEK dosya okur (araç çağrısı da düşer). Bölüm metni AYNEN alınır, özetlenmez; alınmayan
# bölümler paketin sonunda adıyla listelenir (gerekirse açılır). Haritada olmayan belge bütün girer.
# Önek = başlığın `#` sonrası metninin başı. "## X" seçilince alt "###" bölümleri de gelir. Önek hiçbir başlığa
# uymuyorsa --denetle HATA verir (belge yeniden numaralanınca sessiz kural kaybı olmasın).
BOLUM: dict[str, dict[str, tuple[str, ...]]] = {
    "kaynak": {"docs/KURUL2_DERS_STANDARDI.md": ("0.", "1.", "3.", "10."),
               "docs/OGRENCI_ONEM_YONTEMI.md": ("3.", "5.", "6.")},
    "anlatim": {"docs/KURUL2_DERS_STANDARDI.md": ("0.", "7.", "8."),
                "docs/OGRENCI_ONEM_YONTEMI.md": ("5.",),
                "docs/ANLATIM_KURGU_STANDARDI.md": ("2.", "3.", "4.", "5.", "6.", "Konu bütünlüğü")},
    "ornek_soru": {"docs/OGRENCI_ONEM_YONTEMI.md": ("5.",),
                   "docs/HOCA_USLUBU_YONTEMI.md": ("4.", "5."),
                   "docs/SIK_ACIKLAMA_STANDARDI.md": ("Kural:", "Biçim", "Kaynak sırası", "Kalite kapısı")},
    "yayin": {"docs/KURUL_OTOMASYON_EL_KITABI.md": ("0.", "8.", "10.", "19.", "20.", "21.")},
}
# Bağımsız denetçi madde dağıtımında aşama DEĞİL (ASAMALAR'a girmez); kendi paketi var. Eskiden "yayın" kural setini
# (dağıtım/rsync/commit, 8,9k kelime) okuyordu — tıbbi denetimle ilgisiz. Şimdi: üretim aşamalarının en sık hata özetleri
# + denetçinin bakacakları. (aşama özetleri, {belge: bölüm önekleri}; boş önek = belge bütün)
DENETCI_OZET = ("kaynak", "anlatim", "ornek_soru")
DENETCI_BOLUM: dict[str, tuple[str, ...]] = {
    "docs/TAM_HAT_HIZLI_AKIS.md": ("3.", "7."),
    "docs/KURUL2_DERS_STANDARDI.md": ("0.", "8."),
    "docs/ANLATIM_KURGU_STANDARDI.md": ("5.", "Konu bütünlüğü"),
    "docs/SIK_ACIKLAMA_STANDARDI.md": ("Kural:",),
    "docs/OGRENCI_ONEM_YONTEMI.md": ("6.",),
    "docs/TURKCE_USLUP_STANDARDI.md": (),
}
PAKET_ASAMALAR = (*ASAMALAR, "denetci")


def _bolumler(metin: str) -> list[tuple[int, str, list[str]]]:
    """Belge → (düzey, başlık metni, satırlar). Kod bloğu içindeki `#` başlık sayılmaz. Düzey 0 = ilk başlıktan önceki giriş."""
    out: list[tuple[int, str, list[str]]] = [(0, "", [])]
    cit = False
    for s in metin.splitlines():
        if s.lstrip().startswith("```"):
            cit = not cit
        m = None if cit else re.match(r"^(#{1,3}) +(.*)$", s)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), [s]))
        else:
            out[-1][2].append(s)
    return out


def bolum_sec(yol: str, onekler: tuple[str, ...]) -> tuple[str, list[str], list[str]]:
    """(seçilen metin AYNEN, alınmayan başlıklar, hiçbir başlığa uymayan önekler). Önek boşsa belge bütün döner."""
    metin = (KOK / yol).read_text(encoding="utf-8")
    if not onekler:
        return metin.strip(), [], []
    al: list[str] = []
    atla: list[str] = []
    uydu: set[str] = set()
    acik = 0  # >0: bu düzeydeki seçili bölümün alt bölümlerini de al
    for duzey, baslik, satir in _bolumler(metin):
        if duzey == 0:
            continue
        o = next((x for x in onekler if baslik.startswith(x)), None)
        if o is not None:
            uydu.add(o)
            acik = duzey
            al += satir
        elif acik and duzey > acik:
            al += satir
        else:
            acik = 0
            if duzey == 2:
                atla.append(baslik)
    return "\n".join(al).strip(), atla, [x for x in onekler if x not in uydu]


def _genel_dar() -> str:
    """genel.md'den içerik aşamasına yaramayan kısımlar düşer: gövdesiz başlıklar ve 'Hat dışı maddeler' kimlik listesi."""
    out: list[str] = []
    for duzey, baslik, satir in _bolumler((CIKIS / "genel.md").read_text(encoding="utf-8")):
        if duzey == 3 and not baslik.startswith("Hat dışı") and any(x.strip() for x in satir[1:]):
            out += satir
    return "\n".join(out).strip()


def paket(asama: str, mod: str = "tam") -> str:
    """Aşamanın TEK okuma dosyası. Kural metinleri aynen; yalnız aşamayla ilgisiz belge bölümleri dışarıda kalır."""
    if asama not in PAKET_ASAMALAR:
        raise SystemExit(f"bilinmeyen aşama: {asama} ({', '.join(PAKET_ASAMALAR)})")
    p = [f"# Kural paketi — {asama} · kip {mod}",
         "> ÜRETİLMİŞ: `kural_secici.py --paket`. Bu aşamada kural için YALNIZ bu dosya okunur; listedeki belgeleri ayrıca "
         "açma. Bir madde belirsizse: `kural_secici.py --tam <H no>`.", ""]
    if asama == "denetci":
        p += ["## Bu hatta en sık yapılan hatalar (önce bunlara bak)"]
        p += [ozet(a) for a in DENETCI_OZET]
        belgeler = DENETCI_BOLUM
    else:
        p += ["## İlk geçişte doğru: yazmadan önce oku, teslimden önce kendin denetle", ozet(asama), "",
              "## Aşama kuralları", (CIKIS / f"{asama}.md").read_text(encoding="utf-8").split("\n\n", 2)[-1].strip(), "",
              "## Genel", _genel_dar()]
        belgeler = {d: BOLUM.get(asama, {}).get(d, ()) for d in oku(asama, mod)
                    if not d.startswith("docs/asama_kurallari/")}
    for yol, onek in belgeler.items():
        if not (KOK / yol).exists():
            continue
        metin, atla, _ = bolum_sec(yol, onek)
        p += ["", f"## Belge: {yol}" + (" (yalnız ilgili bölümler)" if onek else ""), metin]
        if atla:
            p.append(f"\n_(Bu aşamaya ait olmadığı için alınmadı — gerekirse `{yol}`: " + " · ".join(a[:48] for a in atla) + ")_")
    return "\n".join(p) + "\n"


def paket_yaz(klasor, mod: str = "tam", asamalar: tuple[str, ...] | None = None) -> dict[str, int]:
    """<klasör>/baglam/kural_<aşama>.md dosyalarını yazar (baglam.py çağırır). Dönen: aşama → kelime."""
    hedef = _Path(klasor) / "baglam"
    hedef.mkdir(parents=True, exist_ok=True)
    out: dict[str, int] = {}
    for a in asamalar or PAKET_ASAMALAR:
        t = paket(a, mod)
        (hedef / f"kural_{a}.md").write_text(t, encoding="utf-8")
        out[a] = len(t.split())
    return out


def bolum_denetle() -> list[str]:
    hata = []
    for ad, harita in [*BOLUM.items(), ("denetci", DENETCI_BOLUM)]:
        for yol, onek in harita.items():
            if not (KOK / yol).exists():
                hata.append(f"{ad}: belge yok {yol}")
                continue
            for o in bolum_sec(yol, onek)[2]:
                hata.append(f"{ad}: {yol} içinde '{o}' ile başlayan başlık yok (BOLUM haritasını güncelle)")
    return hata


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--denetle", action="store_true")
    ap.add_argument("--oku")
    ap.add_argument("--ozet")
    ap.add_argument("--tam")
    ap.add_argument("--paket", help="aşamanın TEK okuma dosyası (özet + kurallar + standartların ilgili bölümleri); 'hepsi' + --yaz <klasör>")
    ap.add_argument("--yaz", help="--paket çıktısını <klasör>/baglam/kural_<aşama>.md olarak yaz")
    ap.add_argument("--mod", choices=("tam", "tasarruf"), default="tam")
    a = ap.parse_args()
    if a.paket:
        if a.yaz:
            for k, n in paket_yaz(a.yaz, a.mod, None if a.paket == "hepsi" else (a.paket,)).items():
                print(f"baglam/kural_{k}.md  {n} kelime")
        else:
            print(paket(a.paket, a.mod), end="")
        return 0
    if a.oku:
        print("\n".join(oku(a.oku, a.mod)))
        return 0
    if a.ozet:
        if a.ozet not in ASAMALAR and a.ozet != "genel":
            raise SystemExit(f"bilinmeyen aşama: {a.ozet}")
        print(ozet(a.ozet))
        return 0
    if a.tam:
        print(tam_cikti(a.tam))
        return 0
    if a.denetle:
        defter_satirlari()  # dizin ↔ konu dosyası tutarlılığı (uyuşmazlıkta HATA ile çıkar)
        son = max([DEFTER.stat().st_mtime, *(p.stat().st_mtime for p in HATALAR.glob("*.md"))])
        eski = [p.name for p in CIKIS.glob("*.md") if p.stat().st_mtime < son] or \
               ([] if CIKIS.exists() else ["(yok)"])
        if eski:
            print(f"HATA: aşama özetleri defterden eski ({', '.join(eski)}); kural_secici.py çalıştır", file=sys.stderr)
            return 1
        kayip = kayip_denetle()
        if kayip:
            print("HATA: çıktıda geçmeyen madde (kural kaybı); kural_secici.py çalıştır:\n  " + "\n  ".join(kayip),
                  file=sys.stderr)
            return 1
        bh = bolum_denetle()
        if bh:
            print("HATA: kural paketi bölüm haritası belgeyle uyuşmuyor:\n  " + "\n  ".join(bh), file=sys.stderr)
            return 1
        print("aşama özetleri güncel")
        return 0
    for asama, n in uret().items():
        print(f"{asama:<12} {n:>3} madde")
    return 0


if __name__ == "__main__":
    sys.exit(main())
