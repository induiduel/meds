#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MedSoru Gelişmiş Tıp Notu & Öğrenme Paketi Oluşturucu (Dinamik Uzunluk, Tablolu, Akıcı & Sıfır GPU)

PROJE_TANITIMI.md süreciyle tam uyumlu:
1. Slayt uzunluğu ve sayfa sayısı ile orantılı dinamik özet ve not derinliği:
   - Kısa slaytlar (10-25 sayfa): ~1.200 - 2.000 kelime
   - Orta slaytlar (25-50 sayfa): ~2.500 - 4.500 kelime
   - Uzun/Geniş slaytlar (50+ sayfa): ~5.000 - 8.000+ kelime tam kapsamlı ders metni
2. Ham OCR ve ASCII bozukluklarının giderilmesi; akıcı, kusursuz tıp Türkçesi.
3. Karşılaştırmalı Markdown tabloları, klinik vaka örnekleri, madde madde algoritmalar.
4. Çift eşitlikli kilit kavram vurguları (`==kavram==`), patofizyolojik sebep-sonuç bağları.
5. İnteraktif öğrenme paketi için JSON çıktısı (bilgi_paketi: anlam -> sonuç, ogrenim_slaytlari).
6. %100 ÜCRETSİZ Bulut AI (Gemini Flash, Groq, OpenCode Zen rotasyonu - MEDS_FREE_ONLY=1).
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SYS_AGENTS = str(ROOT_DIR / "scripts" / "agents")
if SYS_AGENTS not in sys.path:
    sys.path.insert(0, SYS_AGENTS)

import cloud_llm

# ÜCRETSİZ ZORUNLULUĞU KONTROLÜ
os.environ["MEDS_FREE_ONLY"] = "1"

STUDY_K1_DIR = Path(os.environ.get("MEDS_TEMP_DIR", str(ROOT_DIR.parent / "meds_temp"))) / "study" / "k1"
PAKETLER_DIR = ROOT_DIR.parent / "meds_database_v2" / "kurul1_ders_paketleri"
STUDY_K1_DIR.mkdir(parents=True, exist_ok=True)
PAKETLER_DIR.mkdir(parents=True, exist_ok=True)


def calculate_target_length(raw_text: str, total_slides: int = 0) -> tuple[int, int, int]:
    """
    Slaytın uzunluğu ve sayfa sayısıyla orantılı dinamik hedef uzunluğu belirler.
    Döner: (hedef_kelime_sayisi, minimum_tablo_sayisi, slayt_bolum_sayisi)
    """
    word_count = len(raw_text.split())
    slides = total_slides or max(1, word_count // 70)

    if slides <= 20:
        target_words = max(1200, slides * 75)
        min_tables = 2
        sections = 6
    elif slides <= 45:
        target_words = max(2200, slides * 85)
        min_tables = 4
        sections = 8
    elif slides <= 75:
        target_words = max(3800, slides * 95)
        min_tables = 6
        sections = 10
    else:
        target_words = max(5500, min(8500, slides * 105))
        min_tables = 8
        sections = 12

    return target_words, min_tables, sections


PROMPT_SYSTEM = """Sen tıp fakültesi amfi derslerini ve amfi slaytlarını dünyadaki en nitelikli tıp fakültesi ders notlarına ve RAG öğrenme paketlerine dönüştüren uzman bir tıp profesörü ve baş editörsün.

SENİN YAZIM VE KALİTE İLKELERİN:
1. DERİNLİK VE UZUNLUK: Notun uzunluğu amfi slaytının sayfa/konu hacmiyle doğru orantılı olmalıdır. Yüzeysel geçiştirme asla yapma. Slaytta geçen her mekanizmayı, her ilacı, her patolojiyi derinlemesine açıkla.
2. OCR VE DİL ONARIMI: Amfi slaytlarındaki bozuk OCR karakterlerini, yapışmış kelimeleri ve ASCII hatalarını temizle; akıcı, akademik ve mükemmel bir tıp Türkçesi kur.
3. ANLATIM DÜZENİ:
   - Başlık ve Öğrenim Hedefleri
   - Karşılaştırmalı Markdown Tabloları (özellikler, sınıflamalar, ayırıcı tanılar, ilaç grupları mutlaka tablo olsun)
   - Patofizyolojik/Klinik Mekanizmalar (sebep-sonuç ilişkileri, basamak basamak numaralı listeler)
   - Klinik Vaka / Örnek Uygulamalar (teorik bilgiyi pekiştiren pratik tıp örnekleri)
   - Önemli yerlerde `==kilit kavram vurguları==`
   - Sınav için Hızlı Tekrar / Spot Bilgiler
   - Varsa Çıkmış Sorular (<details> akordeon formatında doğru cevap ve ayrıntılı çözüm notuyla)
4. SIFIR UYDURMA: Kaynakta olmayan bilgiyi uydurma; tıp terminolojisine ve dersin amfi içeriğine sadık kal.
"""

PROMPT_USER_TEMPLATE = """DERS: {ders}
KONU: {konu}
ÖĞRETİM ÜYESİ: {hoca}
SLAYT HACMİ: Yaklaşık {slides} sayfa
HEDEF UZUNLUK: Bu slaytın kapsamına uygun olarak en az ~{target_words} kelimelik, en az {min_tables} karşılaştırmalı tablo içeren, eksiksiz bir tıp ders çalışma metni oluştur.

=== AMFİ SLAYTLARI HAM METNİ ===
{kaynak_metin}

=== İLGİLİ ÇIKMIŞ SORULAR ===
{cikmis_sorular}

Lütfen yukarıdaki kurallara, tablo zenginliğine ve dinamik uzunluk standardına tam uygun Türkçe Markdown ders notunu üret.
"""


def generate_study_note(
    ders: str,
    konu: str,
    hoca: str,
    kaynak_metin: str,
    cikmis_sorular: str = "",
    total_slides: int = 0
) -> str:
    target_words, min_tables, sections = calculate_target_length(kaynak_metin, total_slides)

    prompt = PROMPT_USER_TEMPLATE.format(
        ders=ders,
        konu=konu,
        hoca=hoca,
        slides=total_slides or max(1, len(kaynak_metin.split()) // 70),
        target_words=target_words,
        min_tables=min_tables,
        kaynak_metin=kaynak_metin[:25000],  # Ücretsiz modellerin geniş bağlam penceresinden faydalan
        cikmis_sorular=cikmis_sorular or "Bu derse ait doğrudan atanmış soru bulunmamaktadır."
    )

    out = cloud_llm.chat(
        prompt=prompt,
        system=PROMPT_SYSTEM,
        max_tokens=8192,
        timeout=180
    )
    return out or ""


def process_all_current_lessons(limit: int = 0):
    catalog_path = ROOT_DIR.parent / "meds_database" / "2026_2027_guncel_kaynaklar.json"
    if not catalog_path.exists():
        print(f"[HATA] Katalog bulunamadı: {catalog_path}")
        return

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    files = catalog.get("files", [])
    print(f"Toplam 2026-2027 güncel ders sayısı: {len(files)}")

    success = 0
    for idx, f in enumerate(files, 1):
        if limit and success >= limit:
            break

        name = f["name"]
        sid = f["source_id"]
        rel_path = f["rel_path"]
        ders = f["discipline"]
        konu = name.replace(".pdf", "")

        # Dosya adını ve yolunu eşleştir
        base_name = name.replace(".pdf", "")
        matches = list((ROOT_DIR.parent / "meds_temp" / "temp1" / "drive_root").rglob(f"*{base_name.strip()}*.md"))
        if not matches:
            matches = list((ROOT_DIR.parent / "meds_temp" / "temp1").rglob(f"*{base_name.strip()[:15]}*.md"))

        raw_text = ""
        if matches:
            raw_text = matches[0].read_text(encoding="utf-8")

        if not raw_text or len(raw_text.strip()) < 100:
            print(f"[{idx}/{len(files)}] [ATLANDI - Metin Yok]: {name}")
            continue

        slug = re.sub(r"[^a-zA-Z0-9_\-]+", "_", konu.lower()).strip("_")
        out_file = STUDY_K1_DIR / f"2026_{idx:02d}_{slug}.md"

        if out_file.exists() and out_file.stat().st_size > 1500:
            print(f"[{idx}/{len(files)}] [ZATEN HAZIR]: {out_file.name}")
            success += 1
            continue

        print(f"[{idx}/{len(files)}] 🚀 Üretiliyor: {konu} ({ders})...")
        note = generate_study_note(
            ders=ders,
            konu=konu,
            hoca="Fakülte Öğretim Üyesi",
            kaynak_metin=raw_text
        )

        if note and len(note) > 500:
            out_file.write_text(note, encoding="utf-8")
            print(f"[{idx}/{len(files)}] ✅ Tamamlandı ({len(note.split())} kelime) -> {out_file.name}")
            success += 1
        else:
            print(f"[{idx}/{len(files)}] ⚠️ Başarısız veya boş yanıt: {konu}")

    print(f"\n[Bitti] Toplam {success} adet ders notu hazırlandı.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Tüm dersler için üretimi başlat")
    parser.add_argument("--limit", type=int, default=0, help="Üretilecek maksimum ders sayısı")
    args = parser.parse_args()

    if args.run:
        process_all_current_lessons(limit=args.limit)
    else:
        print("[Pipeline Study Generator v2] Dinamik uzunluklu, tablolu ve ücretsiz bulut AI motoru hazır.")
        print("Üretimi başlatmak için: python meds/scripts/pipeline/generate_cloud_study_notes.py --run")

