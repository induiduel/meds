"""Ders işçisi — REVİZYON modu (cihazda çalışır). Var olan Kurul 1 destelerini 2026-27 PDF'inden, Gebelik Hastalıkları
kalitesinde baştan üretir; çıktı taslak/<is_id>/'e yazılır, durum "onay_bekliyor" olur. Canlı veriye yazmaz.

  python3 revize.py                 # LISTE'deki tüm dersler, sırayla (yarım kalan/onay bekleyenler atlanır)
  python3 revize.py k1-02 k1-03     # yalnız seçilenler
  MEDS_REVIZE_PARALEL=2 python3 revize.py
"""
from __future__ import annotations
import sys as _llm_sys, pathlib as _llm_pl; _llm_sys.path[:0] = [str(p / "otomasyon") for p in _llm_pl.Path(__file__).resolve().parents]; from llm_kilit import kilit as _llm_kilit  # noqa: E402  LLM kilidi 2026-10-27
if __name__ == "__main__":
    _llm_kilit("revize")

import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ayarlar import APP, DOWNLOADS, TASLAK, log, oku, yaz  # noqa: E402
import isle  # noqa: E402

K1 = DOWNLOADS / "drive_root" / "Kurul 1"
LISTE = [  # deste_id, PDF (drive_root/Kurul 1 altında), ders
    ("k1p-k1-01-dismorfolojide-genetik-terminoloji", "Tıbbi Genetik/1)DİSMORFOLOJİDE GENETİK TERMİNOLOJİ.pdf", "Tıbbi Genetik"),
    ("k1p-k1-02-patolojiye-giris", "Tıbbi Patoloji/1)Patolojiye Giriş.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-03-hucresel-adaptasyonlar", "Tıbbi Patoloji/4)Hücresel Adaptasyonlar.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-04-hucre-hasari-ve-nekroz-i", "Tıbbi Patoloji/2)Hücre Hasarı ve Nekroz.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-05-hucre-hasari-ve-nekroz-ii", "Tıbbi Patoloji/3)Hücre Hasarı ve Nekroz 2.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar", "Tıbbi Patoloji/5)Hücre İçi Birikimler ve Kalsifikasyonlar.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-08-hucresel-yaslanma", "Tıbbi Patoloji/6)Hücresel Yaşlanma.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese", "Tıbbi Patoloji/7)Akut Enflamasyon.pdf", "Tıbbi Patoloji"),
    ("k1p-k1-10-kromozomal-hastaliklar-ve-genetik-danisma", "Tıbbi Genetik/2)KROMOZOMAL HASTALIKLAR VE GENETİK DANIŞMA.pdf", "Tıbbi Genetik"),
    ("k1p-k1-12-enflamasyonun-kimyasal-mediyatorleri", "Tıbbi Patoloji/8)Enflamasyonun Kimyasal Mediyatörleri.pdf", "Tıbbi Patoloji"),
]

LISTE_ENF_URO = [
    ("k1p-k1-17-cinsel-yolla-bulasan-enfeksiyonlarda-tedavi", "Enfeksiyon Hastalıkları/1)Cinsel yolla bulaşan hastalıklarda tedavi.pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-34-genital-enfeksiyonlar", "Enfeksiyon Hastalıkları/2)Genital enfeksiyonlar.pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-36-izolasyon-yontemleri", "Enfeksiyon Hastalıkları/3)İzolasyon yöntemleri.pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-21-enfeksiyon-hastaliklarinda-genel-kavramlar-ve-teme", "Enfeksiyon Hastalıkları/4)Enfeksiyon Hastalıklarında Temel Kavramlar ve Genel Özellikler.pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-52-uriner-sistem-enfeksiyonlari", "Enfeksiyon Hastalıkları/5)Üriner Sistem Enfeksiyonlari.pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-40-cinsel-yolla-bulasan-hastaliklarda-profilaksi-ve-k", "Enfeksiyon Hastalıkları/6)'Cinsel yolla bulaşan enfeksiyonlarda profilaksi ve korunma' .pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-50-sifilis", "Enfeksiyon Hastalıkları/7)Sifiliz .pdf", "Enfeksiyon Hastalıkları"),
    ("k1p-k1-11-uriner-obstruksiyonun-fizyopatolojisi", "Üroloji/1)Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi.pdf", "Üroloji"),
    ("k1p-k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi", "Üroloji/2)Ürolitiyazis Patofizyolojisi.pdf", "Üroloji"),
    ("k1p-k1-51-uriner-sistem-enfeksiyonlari-laboratuvar-bulgulari", "Üroloji/3)Üriner Sistem Enfeksiyonları.pdf", "Üroloji"),
    ("k1p-k1-39-uriner-sistem-enfeksiyonlarinin-epidemiyoloji-etiy", "Üroloji/4)'Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi'.pdf", "Üroloji"),
    ("k1p-k1-43-uriner-sistemin-spesifik-enfeksiyonlari", "Üroloji/5) Üriner Sistemin Spesifik Enfeksiyonları.pdf", "Üroloji"),
]

# 2026-10-12 · kalan Kurul 1 dersleri (hafif revize → "Her ikisini tut" V2). Kaynak: deckPdfSources.json'daki içerikle
# doğrulanmış PDF. Bir PDF birden çok ders içeriyorsa sayfa aralığı verilir; ikinci PDF'in sayfaları kaynak.md'de
# +1000 kaydırılır (=== SAYFA 1035 === → o PDF'in 35. sayfası).
P, G, H, KD, EH, U = "Tıbbi Patoloji/", "Tıbbi Genetik/", "Halk Sağlığı/", "Kadın Hastalıkları ve Doğum/", "Enfeksiyon Hastalıkları/", "Üroloji/"
LISTE_KALAN = [  # deste_id, [(PDF, (ilk, son) | None), ...], ders
    ("k1p-k1-01-dismorfolojide-genetik-terminoloji", [(G + "1)DİSMORFOLOJİDE GENETİK TERMİNOLOJİ.pdf", None)], "Tıbbi Genetik"),
    ("k1p-k1-02-patolojiye-giris", [(P + "1)Patolojiye Giriş.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-03-hucresel-adaptasyonlar", [(P + "4)Hücresel Adaptasyonlar.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-04-hucre-hasari-ve-nekroz-i", [(P + "2)Hücre Hasarı ve Nekroz.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-05-hucre-hasari-ve-nekroz-ii", [(P + "3)Hücre Hasarı ve Nekroz 2.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar", [(P + "5)Hücre İçi Birikimler ve Kalsifikasyonlar.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-08-hucresel-yaslanma", [(P + "6)Hücresel Yaşlanma.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese", [(P + "7)Akut Enflamasyon.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-10-kromozomal-hastaliklar-ve-genetik-danisma", [(G + "2)KROMOZOMAL HASTALIKLAR VE GENETİK DANIŞMA.pdf", None)], "Tıbbi Genetik"),
    ("k1p-k1-12-enflamasyonun-kimyasal-mediyatorleri", [(P + "8)Enflamasyonun Kimyasal Mediyatörleri.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-13-kronik-ve-granulomatoz-enflamasyon", [(P + "9)Kronik ve Granülamatöz Enflamasyon .pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri", [(H + "4)'Salgın Hastalıklarda Kontrol ve Korunma'.pdf", None)], "Halk Sağlığı"),
    ("k1p-k1-15-doku-onarimi-ve-yara-iyilesmesi", [(P + "10)Doku Onarımı ve Yara İyileşmesi.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-16-odem-hiperemi-konjesyon-ve-kanama", [(P + "11)Ödem, Hiperemi, Konjesyon ve Kanama.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-18-halk-sagligi-tarihcesi", [(H + "1)Halk SağlığıTarihçesi.pdf", None)], "Halk Sağlığı"),
    ("k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri", [(G + "3)'DOĞUMSAL KADIN-ERKEK GELİŞİM ANOMALİLERİ'.pdf", None)], "Tıbbi Genetik"),
    ("k1p-k1-20-tromboz-patofizyolojisi", [(P + "12) Tromboz Patofizyolojisi.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-22-bebek-beslenmesi", [(H + "3)BEBEK BESLENMESİ.pdf", None)], "Halk Sağlığı"),
    ("k1p-k1-23-ana-cocuk-sagligi-duzeyinin-izlenmesi", [(H + "2)Ana çocuk sağ.izleme .pdf", None)], "Halk Sağlığı"),
    ("k1p-k1-24-emboli-enfarktus-ve-sok", [(P + "13) Emboli,enfarktüs ve şok.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-25-asiri-duyarlilik-ve-otoimmunite", [(P + "14)Aşırı duyarlılık ve otoimmünite.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-26-genetik-pediatrik-ve-cevresel-patoloji", [(P + "15)Genetik,pediatrik ve çevresel patoloji.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-28-tumor-biyolojisi-ve-terminolojisi", [(P + "16)Tümör Biyolojisi ve Terminolojisi.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-29-karsinojenezin-molekuler-temeli", [(P + "17)Karsinojenezin Moleküler Temeli.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-30-ileri-tumor-genetigi-ve-metabolizmasi", [(P + "18)İleri Tümör Genetiği ve Metabolizması.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-31-urogenital-sistem-tumorlerinde-genetik-belirtecler", [(G + "4)'ÜROGENİTAL SİSTEM TÜMÖRLERİNDE GENETİK BELİRTEÇLER.'.pdf", None)], "Tıbbi Genetik"),
    ("k1p-k1-32-tumor-immunolojisi-ve-metastaz-mekanizmalari", [(P + "19)Tümör İmmünolojisi ve Metastaz Mekanizmaları.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-33-tumor-evrelemesi-derecelendirme-ve-laboratuvar-tan", [(P + "20)Tümör Evrelemesi, Derecelendirme ve LaboratuvarTanısı.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-35-prenatal-tani-yontemleri", [(G + "5)PRENATAL TANI ve UYGULAMA ALANLARI.pdf", None)], "Tıbbi Genetik"),
    ("k1p-k1-37-glomeruler-hastaliklar-nefrotik-sendrom", [(P + "21)Glomerüler Hastalıklar_ Nefrotik Sendrom.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-38-glomeruler-hastaliklar-nefritik-sendrom", [(P + "22)Glomeruler Hastalıklar_ Nefritik Sendrom.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-41-sistemik-hastaliklarda-bobrek-hasari", [(P + "23)Sistemik Hastalıklarda Böbrek Hasarı.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-42-tubulointerstisyel-hastaliklar", [(P + "24) Tübülointerstisyel Hastalıklar.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-44-vaskuler-ve-kistik-bobrek-hastaliklari", [(P + "25) Vasküler ve Kistik Böbrek Hastalıkları.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-45-bobrek-tumorleri", [(P + "26)Böbrek Tümörleri.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-46-mesane-hastaliklari-ve-tumorleri", [(P + "26)Mesane Hastalıkları ve Tümörleri.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-48-vulva-vajen-ve-serviks-hastaliklari", [(P + "28)Vulva, Vajen ve Serviks Hastalıkları.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis", [(P + "39)İnvaziv Serviks Kanseri ve Endometriyozis.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-53-endometriyal-hiperplazi-ve-kanserleri", [(P + "30)Endometrial Hiperplazi ve Kanserleri.pdf", (1, 75))], "Tıbbi Patoloji"),
    ("k1p-k1-54-uterus-duz-kas-ve-trofoblastik-tumorleri", [(P + "30)Endometrial Hiperplazi ve Kanserleri.pdf", (76, 92)),
                                                            (P + "32)Gebelik Hastalıkları .pdf", (35, 65))], "Tıbbi Patoloji"),
    ("k1p-k1-55-over-tumorleri", [(P + "31)Ovidukt ve Ovaryum Patolojisi.pdf", None)], "Tıbbi Patoloji"),
    ("k1p-k1-56-memenin-benign-hastaliklari", [(P + "33) Memenin Benign Hastalıkları.pdf", (1, 40))], "Tıbbi Patoloji"),
    ("k1p-k1-65-meme-kanseri-ve-molekuler-tipleri", [(P + "33) Memenin Benign Hastalıkları.pdf", (41, 72))], "Tıbbi Patoloji"),
    ("k1p-k1-58-enurezis-nokturna", [(U + "6)Enürezis.pdf", None)], "Üroloji"),
    ("k1p-k1-61-abortus", [(KD + "1)Abortus_2026.pdf", None)], "Kadın Hastalıkları ve Doğum"),
    ("k1p-k1-62-uretral-akinti", [(EH + "8)ÜRETRAL AKINTI.pdf", None)], "Enfeksiyon Hastalıkları"),
]

HAFIF_KURALLAR = """
HAFİF REVİZE (baglam.hafif = true) — bu ders yayında V1 olarak KALACAK; senin çıktın yanına V2 olarak eklenecek.
- Yalnız şunları üret: ders_paketi.json (bilgi_paketi kanıtlı, tüm önemli bilgiler) → sayfa_haritasi.json
  (TALIMAT §1b: başlıklar 1–20 adım, her sayfa teyitli, şekiller anlatılır) → deck.json (`bolum`, `pdfSayfalari`,
  `sayfaHaritasi: "teyitli"`) → sozluk.json →
  cikmis_baglantilari.json → rapor.md. ders_notu.md, ornek_sorular.json, hastaliklar.json, bilgi_havuzu.jsonl ÜRETME
  (V1'inkiler kullanılır). denetle.py bu dosyaların yokluğunu yalnız UYARI sayar.
- `baglam.kaynak_dosyalari` birden çok PDF ya da sayfa aralığı verebilir: kaynak.md YALNIZ bu dersin sayfalarını içerir.
  Sayfa no ≥ 1000 ise ikinci PDF'tir (1035 → o PDF'in 35. sayfası). Slayt `sourcePdf` = {"fileName": <o PDF'in adı>,
  "primaryPage": <o PDF'teki GERÇEK sayfa>} — kanıt `sayfa` ise kaynak.md'deki numara.
- Slayt sayısı içerikle orantılı (kısa ders ~40–60, uzun/yoğun ders 80–150); dolgu yok, her slayt yeni bilgi.
- SON slayt ders sonu oyun sayfasıdır (TALIMAT.md deck.json maddesi, rehber §5.14); doğrulama `--oyun-zorunlu` ile.
"""

EK_KURALLAR = """
REVİZYON MODU (kullanıcı kuralları — TALIMAT.md ile çelişirse BUNLAR geçerli):
- Bu ders zaten yayında (`baglam.mevcut_deste_dosyasi`). Onu yalnız neyin eksik/hatalı olduğunu görmek için oku; içeriği
  KOPYALAMA. Paketi 2026-27 ders PDF'inden (kaynak.md) baştan, "Gebelik Hastalıkları" destesi (k1p-k1-67) kalitesinde üret.
  `deck.json` id'si `baglam.deste_id` olmalı. rapor.md'de "Eski desteye göre değişenler" başlığı aç.
- Kapsam eksiksiz: ders notundaki HER ifade, bilgi, madde, tablo satırı anlamlı ve açıklayıcı biçimde desteye ve ders
  notuna girer (atlama yok). rapor.md'de sayfa sayfa kapsama tablosu ver (sayfa → slayt numaraları).
- Görseller: `baglam.gorsel_klasoru`ndaki sayfa görüntülerini (sayfa_NNN.png) Read aracıyla incele. Önemli bir görsel
  (histoloji, şema, grafik, karyotip, tablo resmi) varsa neyi gösterdiğini ve önemli bulgularını ilgili slaytta anlat;
  süs/logo görsellerini atla. rapor.md'de "İncelenen görseller" listesi ver.
- Ders notunda YER ALMAYAN bilgi oranı en çok %10: referans kanıtlı (kanit.referans) kayıtlar toplamın %10'unu aşmaz;
  yalnız kopuk/hatalı slayt bilgisini tamamlamak için. Halüsinasyon yok, tıbbi hata yok; emin değilsen yazma.
- Adım sayısı 50–150 (içerik yoğunluğuna göre; dolgu slaytı yok). Her adımda 2–6 interaktif öge (11 tür dengeli,
  adım başına en çok 1 causal_chain).
- Her adımdaki interaktif öge YALNIZCA o adımda veya önceki adımlarda anlatılan bilgiyi sorgular; ileriye sızıntı yok.
  Karşılaştırmalarda iki taraf da daha önce işlenmiş olmalı.
- Sonda kendi denetimini yap: denetle.py 0 HATA + rapor.md'ye referanslı/toplam oranını yaz.
"""


def is_id(deste_id: str) -> str:
    return time.strftime("%Y%m%d") + "-" + hashlib.sha1(("revize:" + deste_id).encode()).hexdigest()[:10]


def gorseller(pdf: Path, hedef: Path) -> int:
    hedef.mkdir(parents=True, exist_ok=True)
    if any(hedef.glob("sayfa_*.png")):
        return len(list(hedef.glob("sayfa_*.png")))
    import pymupdf as fitz
    doc = fitz.open(pdf)
    n = 0
    for i, sayfa in enumerate(doc, 1):
        if sayfa.get_images():  # yalnız görsel içeren sayfalar
            sayfa.get_pixmap(dpi=90).save(hedef / f"sayfa_{i:03d}.png")
            n += 1
    return n


def _pdf_bul(pdf_rel: str) -> Path:
    import unicodedata
    nfc = lambda x: unicodedata.normalize("NFC", x)
    return next((f for f in K1.rglob("*.pdf") if nfc(str(f.relative_to(K1))) == nfc(pdf_rel)), K1 / pdf_rel)


def _parcali_kaynak(kaynaklar: list, d: Path) -> tuple[str, dict, int, list]:
    """Birden çok PDF / sayfa aralığı → tek kaynak.md (ikinci PDF +1000 kaydırılır) + görseller."""
    parca, ocr, dosyalar, gn = [], [], [], 0
    (d / "gorseller").mkdir(parents=True, exist_ok=True)
    for i, (rel, aralik) in enumerate(kaynaklar):
        pdf, ofset = _pdf_bul(rel), 1000 * i
        metin, bilgi = isle.pdf_metni(pdf)
        bas, bit = aralik or (1, bilgi["sayfa"])
        for blok in metin.split("=== SAYFA ")[1:]:
            n = int(blok.split(" ===")[0])
            if bas <= n <= bit:
                parca.append(f"=== SAYFA {n + ofset} ===" + blok.rstrip().split(" ===", 1)[1])
        ocr += [n + ofset for n in bilgi.get("ocr_sayfalar", []) if bas <= n <= bit]
        import pymupdf as fitz
        with fitz.open(pdf) as doc:
            for n in range(bas, bit + 1):
                sayfa = doc[n - 1]
                hedef = d / "gorseller" / f"sayfa_{n + ofset:04d}.png"
                if sayfa.get_images() and not hedef.exists():
                    sayfa.get_pixmap(dpi=90).save(hedef)
                    gn += 1
        dosyalar.append({"pdf_adi": pdf.name, "yol": f"drive_root/Kurul 1/{rel}", "sayfalar": [bas, bit], "sayfa_ofseti": ofset})
    metin = "\n\n".join(parca)
    return metin, {"sayfa": len(parca), "ocr_sayfalar": ocr, "karakter": len(metin)}, gn, dosyalar


def revize_et(deste_id: str, pdf_rel, ders: str) -> dict:
    kaynaklar = pdf_rel if isinstance(pdf_rel, list) else None  # hafif revize: [(PDF, aralık), ...]
    if kaynaklar:
        pdf_rel = kaynaklar[0][0]
    pdf = _pdf_bul(pdf_rel)
    iid = is_id(deste_id)
    # aynı deste için daha önce açılmış taslak varsa onu sürdür
    for eski in TASLAK.glob("*-" + iid.split("-")[1]):
        iid = eski.name
    d = TASLAK / iid
    du = oku(d / "durum.json", {})
    if du.get("durum") == "onay_bekliyor":
        return {"deste": deste_id, "durum": "zaten onay bekliyor", "is_id": iid}
    d.mkdir(parents=True, exist_ok=True)
    dosyalar = None
    if kaynaklar:
        if not (d / "kaynak.md").exists() or not (d / "baglam.json").exists():
            metin, bilgi, gn, dosyalar = _parcali_kaynak(kaynaklar, d)
            (d / "kaynak.md").write_text(metin, encoding="utf-8")
            yaz(d / "kaynak_bilgi.json", bilgi)
        gn = len(list((d / "gorseller").glob("sayfa_*.png")))
    else:
        if not (d / "kaynak.md").exists():
            metin, bilgi = isle.pdf_metni(pdf)
            (d / "kaynak.md").write_text(metin, encoding="utf-8")
            yaz(d / "kaynak_bilgi.json", bilgi)
        gn = gorseller(pdf, d / "gorseller")
    if not (d / "baglam.json").exists():
        konu = pdf.stem.split(")", 1)[-1].strip(" '")
        j = {"is_id": iid, "yol": f"drive_root/Kurul 1/{pdf_rel}", "tam": str(pdf), "yil": "2026-27",
             "konu_zorla": {"kurul": 1, "ders": ders, "konu": konu, "programda": True, "guven": "yuksek", "yontem": "revize"}}
        b = isle.baglam_hazirla(j, d, (d / "kaynak.md").read_text(encoding="utf-8"), oku(d / "kaynak_bilgi.json", {}))
        decks = oku(APP / "src" / "data" / "interactive_learning_decks.json", [])
        eski = next(x for x in decks if x["id"] == deste_id)
        yaz(d / "mevcut_deste.json", eski)
        b.update({"mod": "guncelleme", "revize": True, "deste_id": deste_id, "ders_id": deste_id.split("-", 1)[1],
                  "numara": int(deste_id.split("-")[2]), "mevcut_deste_dosyasi": "mevcut_deste.json",
                  "gorsel_klasoru": "gorseller", "gorsel_sayisi": gn})
        if dosyalar:
            b.update({"hafif": True, "kaynak_dosyalari": dosyalar})
        yaz(d / "baglam.json", b)
    if os.environ.get("MEDS_REVIZE_HAZIRLA"):  # yalnız hazırlık (Claude oturum içinden çalışacak)
        return {"deste": deste_id, "durum": "hazir", "is_id": iid, "klasor": str(d)}
    log(f"revize başlıyor: {deste_id} ({iid})")
    istem = (f"Talimat dosyası: {isle.TALIMAT}. Talimattaki /app yolu bu makinede {APP} demektir "
             f"(ör. /app/docs/OGREN_ETKILESIM_REHBERI.md → {APP}/docs/OGREN_ETKILESIM_REHBERI.md). Önce talimatı, "
             "baglam.json'u ve kaynak.md'yi oku; sonra talimattaki iş sırasıyla tüm çıktıları üret ve denetle.py 0 HATA "
             "olana kadar düzelt." + EK_KURALLAR + (HAFIF_KURALLAR if kaynaklar else ""))
    onceki = oku(d / "oturum.json", {}).get("session_id")
    if onceki:
        istem = "Kota/kesinti nedeniyle yarım kaldın. Klasördeki mevcut dosyalara bakıp kaldığın yerden devam et; " + istem
    r = isle.claude(d, istem, onceki, sure=6 * 3600)
    if r["kota"]:
        return {"deste": deste_id, "durum": "kota", "is_id": iid}
    den = isle.denetle(d)
    for _ in range(2):
        if not den.get("hata"):
            break
        r = isle.claude(d, f"Denetleyici {den['hata']} HATA buldu. Hepsini düzelt, sonra denetle.py'yi yeniden çalıştır:\n"
                           + "\n".join(den.get("hatalar", [])[:60]), r.get("oturum"))
        den = isle.denetle(d)
    s = den.get("sayilar", {})
    ozet = (f"REVİZE · {deste_id} · {s.get('slayt', 0)} slayt · {s.get('soru', 0)} soru · {s.get('terim', 0)} terim · "
            f"{s.get('hastalik', 0)} hastalık · denetim {den.get('hata', '?')} HATA")
    yaz(d / "durum.json", {"durum": "onay_bekliyor", "ozet": ozet, "denetim_hata": den.get("hata"), "zaman": time.time(),
                           "deste_id": deste_id, "ders_id": deste_id.split("-", 1)[1], "revize": True})
    log(f"revize taslak hazır: {iid} → {ozet}")
    return {"deste": deste_id, "durum": "onay_bekliyor", "is_id": iid, "ozet": ozet}


if __name__ == "__main__":
    sec = sys.argv[1:]
    kaynak = {"enf_uro": LISTE_ENF_URO, "kalan": LISTE_KALAN}.get(os.environ.get("MEDS_REVIZE_GRUP", ""), LISTE)
    isler = [x for x in kaynak if not sec or any(x[0].startswith("k1p-" + s) for s in sec)]
    with ThreadPoolExecutor(int(os.environ.get("MEDS_REVIZE_PARALEL", "1"))) as ex:
        for r in ex.map(lambda x: revize_et(*x), isler):
            print(json.dumps(r, ensure_ascii=False), flush=True)
