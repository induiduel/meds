#!/usr/bin/env python3
"""2025-2026 geçmiş yıl arşiv dersleri için PARALEL taslak + ses/zamanlama/.medspak üretici.

Neden:
  Tek oturumda tüm dosyaları (ders_paketi, sayfa_haritasi, ders_notu, ornek_sorular, sozluk, hastaliklar,
  bilgi_havuzu, cikmis_baglantilari, konusma_v2, cizim_aday, deck) sırayla yazmak ders başına 35–50 dk sürüyordu.
  Bu betik:
    1. İndirme + cikar.py + L0 kroki + baglam.json hazır değilse indir_ve_cikar.py'yi çalıştırır.
    2. İskelet aşaması: ders_paketi.json ve sayfa_haritasi.json yoksa üretir.
    3. Paralel aşama (ThreadPoolExecutor, 5 eşzamanlı işçi):
         - deck_parca/<no>.json (her ana başlık ayrı paralel oturumda)
         - deck_ust.json (deste üst bilgisi + ders sonu oyun sayfası)
         - ders_notu.md
         - ornek_sorular.json + cikmis_baglantilari.json
         - sozluk.json + hastaliklar.json + bilgi_havuzu.jsonl
         - konusma_v2.json (+ --turet ile konusma_metni.md, konusma_sayfalari.json, konusma_capalari.json)
         - cizim_aday.json (konusma_v2 biter bitmez)
    4. Deste birleştirme (deck_parca + deck_ust → deck.json, sayfaHaritasi: "teyitli") ve denetle.py + düzeltme turu.
    5. arsiv_yayinla.py ile doğrulama kapıları, EMA GPU ses sentezi, kelime/cümle zamanlaması, PDF işaret,
       canlı çizim yerleşimi ve .medspak paketleme.
    6. Boru hattı (--boru-hatti): Bir dersin GPU ses/zamanlama/.medspak aşaması (Adım 5) çalışırken,
       beklemeden sıradaki dersin indirme ve paralel taslak üretimini (Adım 1–4) başlatır.

Kullanım:
  /home/indu/medsor/meds/.venv-ocr/bin/python scripts/arsiv_25_26/paralel_arsiv_isci.py --key y25-k2-04-serebrovaskuler-hastaliklar-ve-inme
  /home/indu/medsor/meds/.venv-ocr/bin/python scripts/arsiv_25_26/paralel_arsiv_isci.py --kurul2-sirali --baslangic 4 --bitis 15
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
DB_25_26 = ROOT / "meds_database_25_26"
ARSIV_DATA = MEDS / "data" / "arsiv_25_26"
PYTHON = str(MEDS / ".venv-ocr" / "bin" / "python")
CLAUDE_BIN = os.environ.get("MEDS_ISCI_CLAUDE", "claude")
CLAUDE_MODEL = os.environ.get("MEDS_ISCI_MODEL", "claude-opus-5-5")
CLAUDE_EFFORT = os.environ.get("MEDS_ISCI_EFFORT", "low")

TALIMAT = MEDS / "scripts" / "ders_isci" / "TALIMAT.md"
TALIMAT_SESLI = MEDS / "scripts" / "ders_isci" / "TALIMAT_SESLI.md"
TALIMAT_CIZIM = MEDS / "scripts" / "cizim" / "TALIMAT_CIZIM.md"
REHBER = MEDS / "docs" / "OGREN_ETKILESIM_REHBERI.md"

# 2025-2026 Kurul 2 ders eşleşme tablosu (k2.json sırasıyla gecen_yil_d3/kurul 2/ kaynakları)
KURUL2_ARSIV_LISTESI = [
    {"kurul_no": 1, "no": 1, "brans": "Nöroloji", "key": "y25-k2-01-norolojik-hastaya-yaklasim", "baslik": "Nörolojik Hastaya Yaklaşım", "hoca": "Prof.Dr. Şerefnur Öztürk", "file_id": "1diqvLG4POBEMjKRJvtjhinpgeFV3AK7G"},
    {"kurul_no": 2, "no": 2, "brans": "Nöroloji", "key": "y25-k2-02-bilinc-bozuklugu-olan-hastaya-yaklasim", "baslik": "Bilinç Bozukluğu Olan Hastaya Yaklaşım", "hoca": "Prof.Dr. Şerefnur Öztürk", "file_id": "1MwqkUEiLNYOAIAQgUkuyP3mIHY-lGi45"},
    {"kurul_no": 3, "no": 1, "brans": "Tıbbi Patoloji", "key": "y25-k2-03-sss-hasar-bicimleri-odem-hidrosefali-herniasyon", "baslik": "SSS Hasar Biçimleri, Ödem, Hidrosefali, Herniasyon", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "19VgamTxVNVqbjcGK969n1gP7Y78J0NPT"},
    {"kurul_no": 4, "no": 2, "brans": "Tıbbi Patoloji", "key": "y25-k2-04-serebrovaskuler-hastaliklar-ve-inme", "baslik": "Serebrovasküler Hastalıklar ve İnme", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "1Rfbed94gI7l16VC5FX_JBsy2EHy_cF5Z"},
    {"kurul_no": 5, "no": 3, "brans": "Nöroloji", "key": "y25-k2-05-norolojik-muayene", "baslik": "Nörolojik Muayene", "hoca": "Dr. Öğr. Üyesi İrfan Yavaş", "file_id": "1-Y2ANU0zsI8StIhSbfi6f7KyR8wYhXuj"},
    {"kurul_no": 6, "no": 1, "brans": "Anesteziyoloji ve Reanimasyon", "key": "y25-k2-06-agri-yollari-ve-mekanizmalari", "baslik": "Ağrı Yolları ve Mekanizmaları", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1mWQGUboSVEDRs3okAiBnQL3ZcZBGl9Is"},
    {"kurul_no": 7, "no": 1, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-07-genel-anestezik-ilaclar", "baslik": "Genel Anestezik İlaçlar", "hoca": "Dr. Öğr. Üyesi Namık Bilici", "file_id": "1n8VMslC9oGPEzkjeARxDGx3mdJWZK4ek"},
    {"kurul_no": 8, "no": 1, "brans": "Tıbbi Genetik", "key": "y25-k2-08-beyin-ve-iskelet-sistemi-gelisimi-genetigi", "baslik": "Beyin ve İskelet Sistemi Gelişimi Genetiği", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1-bNz4jIy6EFbvbF9dNqbXNH0q9wnXjK8"},
    {"kurul_no": 9, "no": 2, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-09-sss-ilaclari", "baslik": "SSS İlaçları", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1Ullkdi8IH6RA37H4mAH_z7hcjG2dfpT9"},
    {"kurul_no": 10, "no": 4, "brans": "Nöroloji", "key": "y25-k2-10-bas-agrisina-yaklasim", "baslik": "Baş Ağrısına Yaklaşım", "hoca": "Dr. Öğr. Üyesi İrfan Yavaş", "file_id": "1JrRM-rEMmYwjZ8YmRSa-S5JquammIFLo"},
    {"kurul_no": 11, "no": 1, "brans": "Psikiyatri", "key": "y25-k2-11-psikiyatrik-semiyoloji", "baslik": "Psikiyatrik Semiyoloji", "hoca": "Dr. Öğr. Üyesi Nefise Demir", "file_id": "1ZYQIOT67ds-2lPygnREnxrynIME2dFsS"},
    {"kurul_no": 12, "no": 1, "brans": "Beyin ve Sinir Cerrahisi", "key": "y25-k2-12-kafa-travmalari", "baslik": "Kafa ve Omurilik Yaralanmaları", "hoca": "Doç. Dr. Aydın Sinan Apaydın", "file_id": "1ran23mdEnl_4p9CxbiYQwLustck52Agk"},
    {"kurul_no": 13, "no": 2, "brans": "Beyin ve Sinir Cerrahisi", "key": "y25-k2-13-spinal-travmalar", "baslik": "Medulla Spinalis Lezyonları ve Spinal Travmalar", "hoca": "Doç. Dr. Aydın Sinan Apaydın", "file_id": "1qOQ4DYspVXBXoyxahYyNzsfvwWT4LDgf"},
    {"kurul_no": 14, "no": 3, "brans": "Beyin ve Sinir Cerrahisi", "key": "y25-k2-14-beyin-tumorleri", "baslik": "İntrakraniyal Kitlelerde Belirti ve Bulgular (Beyin Tümörleri)", "hoca": "Doç. Dr. Aydın Sinan Apaydın", "file_id": "1NoH24LBMQUz4IZjglxCXgHo5PT6XeujF"},
    {"kurul_no": 15, "no": 2, "brans": "Psikiyatri", "key": "y25-k2-15-sizofrenik-bozukluklar", "baslik": "Şizofrenik Bozukluklar", "hoca": "Dr. Öğr. Üyesi Nefise Demir", "file_id": "1dwzKzWSVXhqYvmR6dPhvoewY50kFdNBn"},
    {"kurul_no": 16, "no": 1, "brans": "FTR", "key": "y25-k2-16-norolojik-rehabilitasyona-giris", "baslik": "Nörolojik Rehabilitasyona Giriş ve Genel İlkeler", "hoca": "Dr. Öğr. Üyesi Şengül Metin Tarhan", "file_id": "18fFBuhZAFMb2fl2f2B4yUi7lX5eNF5EB"},
    {"kurul_no": 17, "no": 5, "brans": "Nöroloji", "key": "y25-k2-17-periferik-noropati", "baslik": "Periferik Nöropati (Polinöropatiler)", "hoca": "Dr. Öğr. Üyesi İrfan Yavaş", "file_id": "1se-lCTorGqvMhZvwNdd6pzMYNmDdoaIC"},
    {"kurul_no": 18, "no": 6, "brans": "Nöroloji", "key": "y25-k2-18-bazal-gangliyonlar", "baslik": "Bazal Gangliyonlar ve Ekstrapiramidal Sistem", "hoca": "Prof.Dr. Şerefnur Öztürk", "file_id": "1vsQkZqumYUmy4lr-k19GRtzOKj8h5-v7"},
    {"kurul_no": 19, "no": 3, "brans": "Psikiyatri", "key": "y25-k2-19-bipolar-bozukluk", "baslik": "Bipolar Bozukluk", "hoca": "Dr. Öğr. Üyesi Nefise Demir", "file_id": "1XPgqSSEb1UUD5vJV3C80fo2ta5mL8B38"},
    {"kurul_no": 20, "no": 4, "brans": "Psikiyatri", "key": "y25-k2-20-psikiyatrik-tedaviler", "baslik": "Psikiyatrik Bozukluklarda Uygulanan Tedaviler", "hoca": "Dr. Öğr. Üyesi Nefise Demir", "file_id": "1Wu0RqPAO1EjQghixvdCfY6F6KjGkSrZp"},
    {"kurul_no": 21, "no": 3, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-21-sedatif-ve-hipnotik-ilaclar", "baslik": "Sedatif ve Hipnotik İlaçlar", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1arS1biNGHbQI9mWCJeOrdNa5HHX9V97J"},
    {"kurul_no": 22, "no": 5, "brans": "Psikiyatri", "key": "y25-k2-22-psikosomatik-bozukluklar", "baslik": "Psikosomatik Bozukluklar", "hoca": "Doç. Dr. Zuhal Koç Apaydın", "file_id": "1vYPkrrW_TMvLclbQH-N4h08wH2vq1mKx"},
    {"kurul_no": 23, "no": 6, "brans": "Psikiyatri", "key": "y25-k2-23-cinsel-kimlik-bozukluklari", "baslik": "Cinsel Kimlik Bozuklukları", "hoca": "Doç. Dr. Zuhal Koç Apaydın", "file_id": "13b369qWQQKDVI-W8hxcI8tQLLrJNHpp4"},
    {"kurul_no": 24, "no": 7, "brans": "Nöroloji", "key": "y25-k2-24-epilepsi", "baslik": "Epilepsi", "hoca": "Dr. Öğr. Üyesi İrfan Yavaş", "file_id": "1MdQA0UU4N-AJ7w-Acdh3t59lhOrNU-p0"},
    {"kurul_no": 25, "no": 4, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-25-antiepileptik-ilaclar", "baslik": "Antiepileptik İlaçlar", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1IxvZix8w-Fil-1-s6BJtFwB5Ys1warQa"},
    {"kurul_no": 26, "no": 2, "brans": "Tıbbi Genetik", "key": "y25-k2-26-norolojik-hastaliklar-genetigi", "baslik": "Nörolojik Hastalıklar ve Genetiği", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1NNryH1J8EH51y-I6Y6MRM_ggnYQwJ3_C"},
    {"kurul_no": 27, "no": 1, "brans": "Aile Hekimliği", "key": "y25-k2-27-periyodik-muayeneler", "baslik": "Aile Hekimliğinde Periyodik Muayeneler", "hoca": "Dr. Öğr. Üyesi M. Murat Şahin", "file_id": "1I4Izo8nwL2U-yZYZbXo_rkc3taInKplc"},
    {"kurul_no": 28, "no": 2, "brans": "FTR", "key": "y25-k2-28-norolojik-hastaliklarda-rehabilitasyon", "baslik": "Sık Görülen Nörolojik Hastalıklar ve Rehabilitasyonu", "hoca": "Dr. Öğr. Üyesi Şengül Metin Tarhan", "file_id": "1qNa0Ebv2jV9nGxS1DDqSx5zvEZctjEoc"},
    {"kurul_no": 29, "no": 3, "brans": "Tıbbi Patoloji", "key": "y25-k2-29-sss-travmasi", "baslik": "SSS Travması", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "1ZBGurpkankJRgM5DA-PM-CsP0ituq6tZ"},
    {"kurul_no": 30, "no": 4, "brans": "Tıbbi Patoloji", "key": "y25-k2-30-norodejeneratif-hastaliklar", "baslik": "Nörodejeneratif Hastalıklar", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "1Z_nV1i9uE9oR7SQMdmKmC0GszCBfQ5Kc"},
    {"kurul_no": 31, "no": 8, "brans": "Nöroloji", "key": "y25-k2-31-medulla-spinalis-hastaliklari", "baslik": "Medulla Spinalis Hastalıkları", "hoca": "Dr. Öğr. Üyesi İrfan Yavaş", "file_id": "1oUD0WI9ZyRo0DPlIuPk6FRcXnNvrLIR4"},
    {"kurul_no": 32, "no": 9, "brans": "Nöroloji", "key": "y25-k2-32-felcler", "baslik": "Felçler", "hoca": "Dr. Öğr. Üyesi İrfan Yavaş", "file_id": "1RxrDo6LZDqjdHUsI0bocJmZjvvaQ1AJm"},
    {"kurul_no": 33, "no": 5, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-33-opioid-analjezikler-ve-antagonistleri", "baslik": "Opioid Analjezikler ve Antagonistleri", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1c03QKnfAjpxKQ1N0QrPQz-Y5wS9O204C"},
    {"kurul_no": 34, "no": 7, "brans": "Psikiyatri", "key": "y25-k2-34-unipolar-depresyon", "baslik": "Unipolar Depresyon", "hoca": "Doç. Dr. Zuhal Koç Apaydın", "file_id": "1J0Ot6flAzeVGTiGQJvMtdigWFBgh3lpb"},
    {"kurul_no": 35, "no": 8, "brans": "Psikiyatri", "key": "y25-k2-35-kisilik-bozukluklari", "baslik": "Kişilik Bozuklukları", "hoca": "Doç. Dr. Zuhal Koç Apaydın", "file_id": "14sPTB97OB57Os0xj7AKUUfoMvzvSxcRL"},
    {"kurul_no": 36, "no": 2, "brans": "Aile Hekimliği", "key": "y25-k2-36-aile-hekimligine-yaklasim-wonca", "baslik": "Aile Hekimliğine Yaklaşım (WONCA Ağacı)", "hoca": "Dr. Öğr. Üyesi M. Murat Şahin", "file_id": "1-bkkb0VBGUiaXotSEgvP33Uxji8QLJHB"},
    {"kurul_no": 37, "no": 9, "brans": "Psikiyatri", "key": "y25-k2-37-okb-ve-iliskili-bozukluklar", "baslik": "OKB ve İlişkili Bozukluklar", "hoca": "Dr. Öğr. Üyesi Nefise Demir", "file_id": "13LCyNqZ5aC2EIiOptmp19jXuwKRm5VCo"},
    {"kurul_no": 38, "no": 10, "brans": "Psikiyatri", "key": "y25-k2-38-travma-ve-stres-baglantili-bozukluklar", "baslik": "Travma ve Stres Bağlantılı Bozukluklar (TSSB)", "hoca": "Dr. Öğr. Üyesi Nefise Demir", "file_id": "1Mhb0lIqWgCr68-FSp6eSN8bB7EXoNKhs"},
    {"kurul_no": 39, "no": 6, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-39-kolinoseptor-bloke-edici-ilaclar", "baslik": "Kolinoseptör Bloke Edici İlaçlar", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1141gu1GHOsMGdxY5_PXih3ibZkL3k-fq"},
    {"kurul_no": 40, "no": 5, "brans": "Tıbbi Patoloji", "key": "y25-k2-40-santral-sinir-sistemi-tumorleri", "baslik": "Santral Sinir Sistemi Tümörleri", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "1F2wnsEYksIsD_tKg0VMvlWwPU3cakbmY"},
    {"kurul_no": 41, "no": 7, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-41-otonom-sinir-sistemi-farmakolojisi", "baslik": "Otonom Sinir Sistemi Farmakolojisi", "hoca": "Dr. Öğr. Üyesi Namık Bilici", "file_id": "1U7dfFzmfILB9dQDgpdfldp531GJWFiMX"},
    {"kurul_no": 42, "no": 11, "brans": "Psikiyatri", "key": "y25-k2-42-norogelisimsel-bozukluklar", "baslik": "Nörogelişimsel Bozukluklar", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1lzZ2Wc2fDmpU-SbVp8gTsWdo-gPheU-e"},
    {"kurul_no": 43, "no": 12, "brans": "Psikiyatri", "key": "y25-k2-43-konsultasyon-liyezon-psikiyatrisi", "baslik": "Konsültasyon Liyezon Psikiyatrisi", "hoca": "Dr. Öğr. Üyesi Pınar Durmaz", "file_id": "1oogWEVf8roPYm1FJ-71BRApAiOTf3ZdR"},
    {"kurul_no": 44, "no": 13, "brans": "Psikiyatri", "key": "y25-k2-44-damgalama", "baslik": "Damgalama", "hoca": "Dr. Öğr. Üyesi Pınar Durmaz", "file_id": "1vNACSBT0S1yiPehPzYK_XBeEXtuj-LSB"},
    {"kurul_no": 45, "no": 14, "brans": "Psikiyatri", "key": "y25-k2-45-intihar-ve-kendine-zarar-verme", "baslik": "İntihar ve Kendine Zarar Verme", "hoca": "Dr. Öğr. Üyesi Pınar Durmaz", "file_id": "1hYSeHahfe8vMike_MjxLxVP0UmF0Z7cm"},
    {"kurul_no": 46, "no": 8, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-46-sempatomimetikler", "baslik": "Sempatomimetikler (Adrenoseptör Agonistler)", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1vmNNMhs1YpVwB2lCFRMKhFK2M0fe1a27"},
    {"kurul_no": 47, "no": 9, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-47-adrenoseptor-antagonist-ilaclar", "baslik": "Adrenoseptör Antagonist İlaçlar", "hoca": "Dr. Öğr. Üyesi Namık Bilici", "file_id": "10aCu_6dZhiYJilToGNHtxPXxlYCAfoQO"},
    {"kurul_no": 48, "no": 10, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-48-lokal-anestezik-ilaclar", "baslik": "Lokal Anestezik İlaçlar", "hoca": "Dr. Öğr. Üyesi Namık Bilici", "file_id": "1dTzOLPR2U9FqMd9kRKhBLx98Zof8vYhi"},
    {"kurul_no": 49, "no": 15, "brans": "Psikiyatri", "key": "y25-k2-49-dikkat-eksikligi-hiperaktivite-bozuklugu", "baslik": "Dikkat Eksikliği Hiperaktivite Bozukluğu (DEHB)", "hoca": "Dr. Öğr. Üyesi Pınar Durmaz", "file_id": "1JgfRNfJxkT2FvUfYhtLRKqBjIjzpcOx-"},
    {"kurul_no": 50, "no": 16, "brans": "Psikiyatri", "key": "y25-k2-50-disa-atim-bozukluklari", "baslik": "Dışa Atım Bozuklukları", "hoca": "Dr. Öğr. Üyesi Pınar Durmaz", "file_id": "14wn-KNjDvKQty36KJt3deFSLb50cD2ln"},
    {"kurul_no": 51, "no": 11, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-51-kolinoseptor-aktive-edici-ve-kolinesteraz-inhibitorleri", "baslik": "Kolinoseptör Aktive Edici ve Kolinesteraz İnhibitörleri", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1mREPQwLDR1Fm87sCBvqtbqSsbJk9JKBi"},
    {"kurul_no": 52, "no": 3, "brans": "Tıbbi Genetik", "key": "y25-k2-52-davranis-genetigi", "baslik": "Davranış Genetiği", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1qvMhjOBZXpnBzcuotm6zcGtlEmmHfT6g"},
    {"kurul_no": 53, "no": 4, "brans": "Tıbbi Genetik", "key": "y25-k2-53-norodejeneratif-hastaliklar-genetigi", "baslik": "Nörodejeneratif Hastalıklar Genetiği", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1ofKxN5x2iVSqtmgT6eA4Efyine_dRyj9"},
    {"kurul_no": 54, "no": 17, "brans": "Psikiyatri", "key": "y25-k2-54-yaygin-anksiyete-bozuklugu", "baslik": "Yaygın Anksiyete Bozukluğu", "hoca": "Doç. Dr. Zuhal Koç Apaydın", "file_id": "1IiHdRkl7zVdMrNEjwLeiP6LgC6DFcuAP"},
    {"kurul_no": 55, "no": 18, "brans": "Psikiyatri", "key": "y25-k2-55-panik-bozukluk", "baslik": "Panik Bozukluk", "hoca": "Doç. Dr. Zuhal Koç Apaydın", "file_id": "14fYBHxTAfwS5UCYhfWCC9W0LIOPwYVFl"},
    {"kurul_no": 58, "no": 12, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-58-alkoller", "baslik": "Alkoller", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "1FOeOsVc0Imx3huyai3i9UKTQ0HJrhguy"},
    {"kurul_no": 59, "no": 5, "brans": "Tıbbi Genetik", "key": "y25-k2-59-psikiyatrik-hastaliklar-ve-genetik-analizi", "baslik": "Psikiyatrik Hastalıklar ve Genetik Analizi", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1w-zFwcy-G2i0vD-qZEnxHqPfEjK-pN9f"},
    {"kurul_no": 60, "no": 13, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-60-miyorelaksan-ilaclar", "baslik": "Miyorelaksan İlaçlar (İskelet Kası Gevşeticileri)", "hoca": "Prof. Dr. Mehmet Özdemir", "file_id": "11GacT05pI0_bDKWKys6Xi10l7HpgYmQz"},
    {"kurul_no": 61, "no": 4, "brans": "Aile Hekimliği", "key": "y25-k2-61-nikotin-bagimliligi-ve-tedavisi", "baslik": "Nikotin Bağımlılığı ve Tedavisi", "hoca": "Dr. Öğr. Üyesi Aybala Cebecik Özcan", "file_id": "1TsGpPrX7wpO4tWFbzm051TIYdudNxGL0"},
    {"kurul_no": 62, "no": 10, "brans": "Nöroloji", "key": "y25-k2-62-kraniyal-sinir-muayenesi", "baslik": "Kraniyal Sinir Muayenesi", "hoca": "Dr. Öğr. Üyesi Serap Arslan", "file_id": "1Lb2iyeX73xo3AR3cAkHY-8UhqUQx4XgI"},
    {"kurul_no": 63, "no": 14, "brans": "Tıbbi Farmakoloji", "key": "y25-k2-63-antidepresan-ilaclar", "baslik": "Antidepresan İlaçlar", "hoca": "Dr. Öğr. Üyesi Namık Bilici", "file_id": "1Mv_adB8AMTuloJsGuGBhNtvntRVqenNG"},
    {"kurul_no": 64, "no": 4, "brans": "Beyin ve Sinir Cerrahisi", "key": "y25-k2-64-omurga-tumorleri", "baslik": "Omurga Tümörleri", "hoca": "Doç. Dr. Aydın Sinan Apaydın", "file_id": "1KagKsjrTCiYoy7JE7qOfSJYMKMv7ntqk"},
    {"kurul_no": 65, "no": 6, "brans": "Tıbbi Patoloji", "key": "y25-k2-65-konjenital-malformasyonlar-ve-perinatal-beyin-hasari", "baslik": "Konjenital Malformasyonlar ve Perinatal Beyin Hasarı", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "1BioHKd8TNLpAsdV6XQGSXtw9AkdrYMfi"},
    {"kurul_no": 66, "no": 7, "brans": "Tıbbi Patoloji", "key": "y25-k2-66-primer-myelin-ve-metabolik-toksik-hastaliklar", "baslik": "Primer Myelin Hastalıkları ve Edinsel Metabolik-Toksik Bozukluklar", "hoca": "Prof.Dr. Hikmet Keleş", "file_id": "1IjnBrwupdrC5JW6J91oXLRQyXsgboQi4"},
]


def log(msg: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    log_yol = DB_25_26 / "paralel_isci.log"
    log_yol.parent.mkdir(parents=True, exist_ok=True)
    with open(log_yol, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def oku(p: Path, varsayilan=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return varsayilan


def yaz(p: Path, veri):
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


def claude_calistir(d: Path, istem: str, oturum_dosya: str = "oturum.json", sure: int = 3600) -> dict:
    oturum = (oku(d / oturum_dosya) or {}).get("session_id")
    cmd = [
        CLAUDE_BIN, "-p", istem,
        "--output-format", "json",
        "--permission-mode", "bypassPermissions",
        "--add-dir", str(MEDS),
        "--model", CLAUDE_MODEL,
        "--effort", CLAUDE_EFFORT,
    ]
    if oturum:
        cmd += ["--resume", oturum]
    try:
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=sure)
    except subprocess.TimeoutExpired:
        return {"hata": "zaman aşımı", "kota": False}
    ham = (r.stdout or "") + (r.stderr or "")
    try:
        js = json.loads(r.stdout)
    except Exception:
        js = {}
    oturum_id = js.get("session_id") or oturum
    if oturum_id:
        yaz(d / oturum_dosya, {"session_id": oturum_id, "zaman": time.time()})
    hata = js.get("is_error") or r.returncode != 0
    kota = bool(hata and re.search(r"usage limit|rate.?limit|limit (?:reached|exceeded)|quota|\b429\b|overloaded", ham, re.I))
    return {"hata": ham[-600:] if hata else "", "kota": kota, "oturum": oturum_id}


def ana_basliklar(d: Path) -> list[dict]:
    h = oku(d / "sayfa_haritasi.json", {}) or {}
    return [b for b in h.get("basliklar", []) if not b.get("ust") and isinstance(b.get("adimlar"), list) and len(b["adimlar"]) == 2]


def on_istem() -> str:
    return (
        f"Talimat dosyası: {TALIMAT} (içindeki /app yolları bu makinede {MEDS} kökündedir; "
        f"Öğren rehberi {REHBER}). Çalışma dizinindeki baglam.json, sayfalar.json ve kaynak.md'yi oku. "
        "Not: baglam.json içinde çıkmış adayları 'aday_cikmislar' veya 'cikmis_adaylari' alanında, "
        "branş 'brans' alanında yer alır. "
    )


def birlestir_deste(d: Path) -> int:
    ust = oku(d / "deck_ust.json", {}) or {}
    basl = ana_basliklar(d)
    parcalar = []
    for b in basl:
        p = oku(d / "deck_parca" / f"{b['no']}.json", None)
        if not p or not isinstance(p.get("slides"), list):
            log(f"[{d.name}] deste parçası eksik/bozuk: {b['no']}")
            return 0
        parcalar.append(p["slides"])
    if not ust.get("deste") or not ust.get("oyun"):
        log(f"[{d.name}] deck_ust.json eksik")
        return 0
    slaytlar = [s for p in parcalar for s in p] + [ust["oyun"]]
    cp = 0
    for i, s in enumerate(slaytlar, 1):
        s["slideNumber"] = i
        if s.get("isCheckpoint") or str(s.get("title", "")).startswith("[TEKRAR SAYFASI"):
            cp += 1
            s["isCheckpoint"] = True
            s["checkpointNumber"] = cp
            s["title"] = re.sub(r"\[TEKRAR SAYFASI - CHECKPOINT(?:\s+\d+)?\]", f"[TEKRAR SAYFASI - CHECKPOINT {cp}]", str(s.get("title", "")))
    deste = {**ust["deste"], "slides": slaytlar, "totalSlides": len(slaytlar), "sayfaHaritasi": "teyitli"}
    eo = sum(len(s.get("interactiveElements") or []) for s in slaytlar)
    deste["totalInteractiveElements"] = eo
    deste["interactiveRatio"] = round(eo / max(1, len(slaytlar)), 2)
    yaz(d / "deck.json", deste)
    return len(slaytlar)


def sesli_ve_cizim_uret(d: Path) -> str:
    """konusma_v2.json + --turet + cizim_aday.json üretir."""
    v2_yol = d / "konusma_v2.json"
    if not v2_yol.exists():
        istem_s = (
            f"Talimat dosyası: {TALIMAT_SESLI} (/app = {MEDS}). Onu ve çalışma dizinindeki kaynak.md, sayfalar.json, "
            "sayfa_haritasi.json, ders_paketi.json, cikmis_baglantilari.json (varsa) ve baglam.json'u oku. "
            "Kurul 2+ dersi: talimatın §v2 bölümüne göre konusma_v2.json'u yaz (atlanan içerik/şekil/tablo sayfası 0 olmalı, "
            "her sayfadaki bilgi maddesi sayısı kadar cümle kurulmalı, görselli sayfalarda slayt.sekil dolu olmalı, "
            "kısaltmalar 'de ne a', 'be o se' gibi Türkçe okunuşla yazılmalı). "
            f"Yazdıktan sonra `{PYTHON} {MEDS}/scripts/sesli_anlatim/konusma_v2.py --dogrula .` ve "
            f"`{PYTHON} {MEDS}/scripts/sesli_anlatim/konusma_v2.py --turet .` ve "
            f"`{PYTHON} {MEDS}/scripts/sesli_anlatim/metin_denetle.py konusma_metni.md` çalıştırıp 0 HATA olana dek düzelt. "
            "Başka dosyaya dokunma."
        )
        claude_calistir(d, istem_s, oturum_dosya="oturum_sesli.json")

    # Türetme ve kapsam kontrolü
    if v2_yol.exists():
        subprocess.run([PYTHON, str(MEDS / "scripts" / "sesli_anlatim" / "konusma_v2.py"), "--turet", str(d)], capture_output=True)
        # Kapsam ve metin denetimi kontrolü
        sys.path.insert(0, str(MEDS / "scripts" / "ders_isci"))
        import isle as IS
        kapsam_h = IS.sesli_kapsam(d)
        r_md = subprocess.run([PYTHON, str(MEDS / "scripts" / "sesli_anlatim" / "metin_denetle.py"), str(d / "konusma_metni.md")], capture_output=True, text=True)
        r_v2 = subprocess.run([PYTHON, str(MEDS / "scripts" / "sesli_anlatim" / "konusma_v2.py"), "--dogrula", str(d)], capture_output=True, text=True)
        if kapsam_h or r_md.returncode != 0 or r_v2.returncode != 0:
            err_txt = "\n".join(kapsam_h[:25]) + "\n" + (r_v2.stdout or "")[-1000:] + "\n" + (r_md.stdout or "")[-1000:]
            claude_calistir(
                d,
                f"konusma_v2.json denetiminde şu hatalar bulundu, hepsini düzelt ve tekrar --dogrula / --turet / metin_denetle çalıştır:\n{err_txt}",
                oturum_dosya="oturum_sesli.json"
            )
            subprocess.run([PYTHON, str(MEDS / "scripts" / "sesli_anlatim" / "konusma_v2.py"), "--turet", str(d)], capture_output=True)

    # cizim_aday.json üretimi (Claude canlı çizim motoru: kontur, akış, odak, şema, zoom)
    cizim_yol = d / "cizim_aday.json"
    if not cizim_yol.exists() and v2_yol.exists():
        sys.path.insert(0, str(MEDS / "scripts" / "cizim"))
        import cizim_uret as CU
        try:
            log(f"[{d.name}] Canlı çizim (kontur, akış oku, şema, zoom) adayları üretiliyor...")
            CU.cizim_aday_uret(d, paralel=4, parti_boyu=6)
        except Exception as e:
            log(f"[{d.name}] cizim_aday_uret hatası: {e}")
    return "tamam" if v2_yol.exists() else "eksik"


def taslak_uret_paralel(ders: dict, max_workers: int = 5) -> bool:
    key = ders["key"]
    t0 = time.time()
    taslak = DB_25_26 / "taslak" / key

    # 1. İndirme + cikar + L0 + baglam.json
    if not (taslak / "baglam.json").exists():
        log(f"[{key}] 1/4 İndirme ve L0 kroki hazırlığı başlatılıyor...")
        cmd = [
            PYTHON, str(MEDS / "scripts" / "arsiv_25_26" / "indir_ve_cikar.py"),
            "--key", key,
            "--kurul", "2",
            "--brans", ders["brans"],
            "--no", str(ders["no"]),
            "--kurul-no", str(ders["kurul_no"]),
            "--baslik", ders["baslik"],
            "--file-id", ders["file_id"],
            "--hoca", ders.get("hoca") or "",
        ]
        r = subprocess.run(cmd, cwd=MEDS)
        if r.returncode != 0:
            log(f"[{key}] HATA: indir_ve_cikar.py başarısız!")
            return False

    # baglam.json uyumluluğu: TALIMAT.md cikmis_adaylari ve program alanlarını bekleyebilir
    baglam = oku(taslak / "baglam.json", {})
    degisti = False
    if "cikmis_adaylari" not in baglam and "aday_cikmislar" in baglam:
        baglam["cikmis_adaylari"] = baglam["aday_cikmislar"]
        degisti = True
    if "program" not in baglam:
        baglam["program"] = {
            "kurul": baglam.get("kurul", 2),
            "ders": baglam.get("brans", ""),
            "konu": baglam.get("konu", ""),
            "ogretim_uyesi": baglam.get("ogretim_uyesi", ""),
            "programda": True,
            "guven": "yuksek",
        }
        degisti = True
    if degisti:
        yaz(taslak / "baglam.json", baglam)

    # 2. İskelet: ders_paketi.json + sayfa_haritasi.json
    if not ((taslak / "ders_paketi.json").exists() and (taslak / "sayfa_haritasi.json").exists() and ana_basliklar(taslak)):
        log(f"[{key}] 2/4 İskelet (ders_paketi.json + sayfa_haritasi.json) üretiliyor...")
        sayfa_say = int(baglam.get("sayfa") or 30)
        hedef_adim = "14–24" if sayfa_say < 25 else ("24–40" if sayfa_say < 50 else "40–65")
        istem_isk = (
            on_istem() +
            f"Görevin YALNIZ TALIMAT §1 `ders_paketi.json` ve §1b `sayfa_haritasi.json` dosyalarını yazmak "
            f"(toplam {hedef_adim} içerik adımı planla; her ana başlık 6–12 içerik adımı olsun; kaynak.md'deki HER sayfa "
            f"sayfa_haritasi.json içinde tam bir kez yer alsın; görselli sayfaları sayfa_goruntu/*.png'den Read ile incele). "
            "Başka dosya YAZMA; bitince tek satır: BİTTİ."
        )
        claude_calistir(taslak, istem_isk, oturum_dosya="oturum_iskelet.json")
        if not ana_basliklar(taslak):
            log(f"[{key}] HATA: İskelet (sayfa_haritasi.json) oluşturulamadı!")
            return False

    # 3. Paralel Üretim: deste parçaları, deste üst+oyun, ders notu, sorular+çıkmış bağları, sözlük+hastalık+havuz, sesli+çizim
    basl = ana_basliklar(taslak)
    on = on_istem() + "ders_paketi.json ve sayfa_haritasi.json YAZILDI (değiştirme); bunlara dayan. "
    isler: list[tuple[str, str, list[str]]] = []

    if not (taslak / "deck.json").exists():
        for i, b in enumerate(basl):
            hedef = f"deck_parca/{b['no']}.json"
            if (taslak / hedef).exists():
                continue
            onceki = "; ".join(f"{x['no']}. {x['baslik']} (adım {x['adimlar'][0]}–{x['adimlar'][1]})" for x in basl[:i]) or "yok"
            isler.append((
                f"deste_{b['no']}",
                on + (
                    f"Görevin: TALIMAT §3 deck.json kurallarıyla YALNIZ ana başlık {b['no']} '{b['baslik']}' için içerik adımları "
                    f"{b['adimlar'][0]}–{b['adimlar'][1]} (sayfalar {b.get('sayfalar')}) slaytlarını yaz; başlığın sonuna bu başlığı "
                    f"pekiştiren bir '[TEKRAR SAYFASI - CHECKPOINT] {b['baslik']}' slaytı ekle. Önceki başlıklar (anlatılmış sayılır): "
                    f"{onceki}. Sonraki başlıkların bilgisi etkileşimlere GİREMEZ (katı kronoloji). Ders sonu oyun sayfası YAZMA. "
                    f"Her slaytta 60–200 kelime maddeli anlatım + 4–5 etkileşim ögesi olsun; her şık açıklaması en az 2 cümle "
                    f"(kavram nedir + bu soruda neden doğru/yanlış) olsun. "
                    f"Çıktı: {hedef} dosyasına yalnız {{\"slides\": [...]}} JSON'u (her içerik slaytında bolum, pdfSayfalari: [ilk, son], "
                    f"sourcePdf: {{\"fileName\": \"{baglam.get('pdf_adi')}\", \"primaryPage\": ilk, \"startPage\": ilk, \"endPage\": son}}). "
                    "Başka dosyaya dokunma; bitince tek satır: BİTTİ."
                ),
                [hedef]
            ))
        if not (taslak / "deck_ust.json").exists():
            isler.append((
                "deste_ust",
                on + (
                    f"Görevin: TALIMAT §3'e göre destenin ÜST bilgisini (id: '{baglam.get('deste_id')}', title, shortTitle, discipline: '{baglam.get('brans')}', "
                    f"committee: 'donem3-kurul2', instructor: '{baglam.get('ogretim_uyesi')}', matchedNoteId: '{key}', overview, highYieldPearls) "
                    "ve ders sonu OYUN SAYFASINI (son slayt, title: '[OYUN SAYFASI] Ders Sonu Oyunları: ...', isGameFinale: true; "
                    "yalnız sequence_order, estimate_slider, perturbation, fix_the_text; dördü de en az 1 kez, toplam 4–6; "
                    "sayılar ders_paketi ile birebir) yaz. Çıktı: deck_ust.json = {\"deste\": {...}, \"oyun\": {...}}. "
                    "Başka dosyaya dokunma; bitince tek satır: BİTTİ."
                ),
                ["deck_ust.json"]
            ))

    if not (taslak / "ders_notu.md").exists():
        isler.append((
            "ders_notu",
            on + "Görevin: TALIMAT §2'ye göre YALNIZ `ders_notu.md`'yi yaz (## bölümleri sayfa_haritasi ana başlıklarıyla aynı sıra ve adla, en sonda ## SPOT BİLGİLER). Başka dosyaya dokunma; bitince tek satır: BİTTİ.",
            ["ders_notu.md"]
        ))
    if not ((taslak / "ornek_sorular.json").exists() and (taslak / "cikmis_baglantilari.json").exists()):
        isler.append((
            "sorular",
            on + "Görevin: TALIMAT §4 ve §6'ya göre YALNIZ `ornek_sorular.json` (her kazanım için en az 3 soru: 1 kolay, 1 orta, 1 zor; her şıkta ≥20 karakter gerekçeli sik_aciklamalari + kanit) ve `cikmis_baglantilari.json`'u yaz. Başka dosyaya dokunma; bitince tek satır: BİTTİ.",
            ["ornek_sorular.json", "cikmis_baglantilari.json"]
        ))
    if not ((taslak / "sozluk.json").exists() and (taslak / "hastaliklar.json").exists() and (taslak / "bilgi_havuzu.jsonl").exists()):
        isler.append((
            "sozluk_hastalik",
            on + "Görevin: TALIMAT §5, §7, §8'e göre YALNIZ `sozluk.json`, `hastaliklar.json` ve `bilgi_havuzu.jsonl`'u kanıtlarıyla yaz. Başka dosyaya dokunma; bitince tek satır: BİTTİ.",
            ["sozluk.json", "hastaliklar.json", "bilgi_havuzu.jsonl"]
        ))

    sesli_gerekli = not ((taslak / "konusma_v2.json").exists() and (taslak / "cizim_aday.json").exists())

    if isler or sesli_gerekli:
        log(f"[{key}] 3/4 Paralel üretim başlıyor: {len(isler)} paket işi + {'sesli/çizim' if sesli_gerekli else 'sesli hazır'} ({max_workers} eşzamanlı işçi)...")

        def calis_parca(item: tuple[str, str, list[str]]):
            ad, istem_p, beklenen = item
            tp = time.time()
            claude_calistir(taslak, istem_p, oturum_dosya=f"oturum_{ad}.json")
            eksik = [b for b in beklenen if not (taslak / b).exists()]
            log(f"[{key}]   → parça bitti: {ad} ({round((time.time() - tp)/60, 1)} dk)" + (f" EKSİK: {eksik}" if eksik else ""))
            return ad, eksik

        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut_ses = ex.submit(sesli_ve_cizim_uret, taslak) if sesli_gerekli else None
            list(ex.map(calis_parca, isler))
            if fut_ses:
                fut_ses.result()

    # Deste parçalarını birleştir
    if not (taslak / "deck.json").exists():
        n_slayt = birlestir_deste(taslak)
        log(f"[{key}] Deste birleştirildi: {n_slayt} slayt")
        if n_slayt:
            # Otomatik onarım (--duzelt)
            subprocess.run([PYTHON, str(MEDS / "scripts" / "validate_learning_decks.py"), str(taslak / "deck.json"), "--duzelt"], capture_output=True)

    if not (taslak / "rapor.md").exists():
        (taslak / "rapor.md").write_text(f"# {key} Arşiv Ders Raporu\n\n- Paralel üretimle oluşturuldu.\n", encoding="utf-8")

    # 4. Denetim ve varsa düzeltme turu
    log(f"[{key}] 4/4 Denetim kapıları kontrol ediliyor...")
    subprocess.run([PYTHON, str(MEDS / "scripts" / "ders_isci" / "denetle.py"), str(taslak)], capture_output=True)
    den = oku(taslak / "denetim.json", {"hata": 999, "hatalar": ["denetim çalışmadı"]})
    for tur_no in range(2):
        if not den.get("hata"):
            break
        hatalar_str = "\n".join((den.get("hatalar") or [])[:50])
        log(f"[{key}]   denetim {den['hata']} HATA buldu (tur {tur_no+1}), düzeltiliyor...")
        claude_calistir(
            taslak,
            on_istem() + f"Denetleyici (`denetle.py`) şu {den['hata']} hatayı buldu. İlgili dosyaları düzenleyerek hepsini düzelt ve `{PYTHON} {MEDS}/scripts/ders_isci/denetle.py .` 0 HATA verene kadar kontrol et:\n{hatalar_str}",
            oturum_dosya="oturum_duzeltme.json"
        )
        subprocess.run([PYTHON, str(MEDS / "scripts" / "ders_isci" / "denetle.py"), str(taslak)], capture_output=True)
        den = oku(taslak / "denetim.json", {"hata": 999})

    sure_dk = round((time.time() - t0) / 60, 1)
    log(f"[{key}] Taslak tamamlandı ({sure_dk} dk) · denetim: {den.get('hata')} HATA")
    return den.get("hata", 999) == 0


def yayinla_ve_medspak(key: str) -> bool:
    tp = time.time()
    log(f"[{key}] ▶ EMA GPU ses + zamanlama + çizim + .medspak yayını başlatılıyor...")
    r = subprocess.run(
        [PYTHON, str(MEDS / "scripts" / "arsiv_25_26" / "arsiv_yayinla.py"), "--key", key],
        cwd=MEDS,
        capture_output=True,
        text=True
    )
    if r.returncode != 0:
        log(f"[{key}] ✖ arsiv_yayinla.py HATA (kod {r.returncode}):\n{(r.stdout + r.stderr)[-1200:]}")
        # Eğer sesli kapsam veya deck hatasıysa bir düzeltme turu çalıştırıp tekrar dene
        taslak = DB_25_26 / "taslak" / key
        claude_calistir(
            taslak,
            f"`arsiv_yayinla.py` şu doğrulama hatasını verdi, ilgili dosyayı düzelt:\n{(r.stdout + r.stderr)[-1500:]}",
            oturum_dosya="oturum_yayin_duzelt.json"
        )
        r2 = subprocess.run([PYTHON, str(MEDS / "scripts" / "arsiv_25_26" / "arsiv_yayinla.py"), "--key", key], cwd=MEDS, capture_output=True, text=True)
        if r2.returncode != 0:
            log(f"[{key}] ✖ arsiv_yayinla.py 2. deneme de başarısız:\n{(r2.stdout + r2.stderr)[-1000:]}")
            return False
    log(f"[{key}] ✔ .medspak tamamlandı ({round((time.time() - tp)/60, 1)} dk)")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="Tek bir ders anahtarı (ör. y25-k2-04-serebrovaskuler-hastaliklar-ve-inme)")
    ap.add_argument("--kurul2-sirali", action="store_true", help="Kurul 2 arşiv derslerini boru hattı (pipeline) ile üret")
    ap.add_argument("--baslangic", type=int, default=3, help="Başlangıç kurul_no (varsayılan: 3)")
    ap.add_argument("--bitis", type=int, default=66, help="Bitiş kurul_no (varsayılan: 66)")
    ap.add_argument("--ters-sira", action="store_true", help="66'dan geriye doğru (sondan başa) üret; diğer oturumla çakışmayı sıfırlar")
    ap.add_argument("--isciler", type=int, default=5, help="Ders içi paralel Claude işçisi sayısı (varsayılan: 5)")
    ap.add_argument("--yalniz-taslak", action="store_true", help="EMA ses/medspak adımını çalıştırma, yalnız paralel taslak üret")
    a = ap.parse_args()

    by_key = {d["key"]: d for d in KURUL2_ARSIV_LISTESI}
    if a.key:
        if a.key not in by_key:
            print(f"HATA: {a.key} listede bulunamadı", file=sys.stderr)
            return 2
        hedefler = [by_key[a.key]]
    elif a.kurul2_sirali:
        hedefler = [d for d in KURUL2_ARSIV_LISTESI if a.baslangic <= d["kurul_no"] <= a.bitis]
        if a.ters_sira:
            hedefler = list(reversed(hedefler))
    else:
        ap.print_help()
        return 1

    # Boru hattı: Bir dersin GPU ses/medspak üretimi arka planda (tek GPU kuyruğunda) çalışırken,
    # sonraki dersin paralel taslak üretimi (CPU + bulut Claude) hiç beklemeden başlar!
    yayin_havuzu = ThreadPoolExecutor(max_workers=1, thread_name_prefix="medspak-gpu")
    bekleyen_yayinlar: list[tuple[str, Future]] = []

    for d in hedefler:
        key = d["key"]
        kurul_no = d["kurul_no"]
        prefix = f"y25-k2-{kurul_no:02d}-"
        medspak_dir = DB_25_26 / "medspak" / "kurul2"
        mevcut_medspaklar = [p for p in medspak_dir.glob(f"{prefix}*.medspak") if p.stat().st_size > 100_000] if medspak_dir.exists() else []
        if mevcut_medspaklar:
            log(f"[{key}] Kurul no {kurul_no} zaten üretilmiş ({mevcut_medspaklar[0].name}), atlanıyor.")
            continue
        # Başka bir oturum aynı kurul_no için farklı bir taslak klasörü açmışsa (veya şu an üzerinde çalışıyorsa) atla
        taslak_dir = DB_25_26 / "taslak"
        diger_taslaklar = [p for p in taslak_dir.glob(f"{prefix}*") if p.name != key and p.is_dir()] if taslak_dir.exists() else []
        if diger_taslaklar:
            log(f"[{key}] Kurul no {kurul_no} başka oturum tarafından işleniyor ({diger_taslaklar[0].name}), çakışmamak için atlanıyor.")
            continue

        ok = taslak_uret_paralel(d, max_workers=a.isciler)
        if not ok:
            log(f"[{key}] Taslakta hata kaldı, yine de yayinla denenecek...")
        if not a.yalniz_taslak:
            fut = yayin_havuzu.submit(yayinla_ve_medspak, key)
            bekleyen_yayinlar.append((key, fut))

    for key, fut in bekleyen_yayinlar:
        fut.result()

    yayin_havuzu.shutdown(wait=True)
    log("Tüm seçili arşiv dersleri tamamlandı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
