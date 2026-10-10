import json, os, sys, re
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

# Topics map across 10 sections:
# Sec 1: 1-10 (Servisit Etyolojisi, Flora, Chlamydia, HSV, Semptomlar & Checkpoint 1)
# Sec 2: 11-20 (Servisit Tanı ve Tedavisi, Endoservikal Polip Patolojisi & Checkpoint 2)
# Sec 3: 21-30 (Serviks Histolojisi, Transformasyon Zonu, Metaplazi & Checkpoint 3)
# Sec 4: 31-40 (HPV Virolojisi, Risk Sınıflaması, Bulaş ve Doğal Seyir & Checkpoint 4)
# Sec 5: 41-50 (HPV Moleküler Onkogenezi: E6/p53 ve E7/RB İnaktivasyonu & Checkpoint 5)
# Sec 6: 51-60 (SIL ve CIN Sınıflaması: LSIL vs HSIL Doğal Seyir Dinamikleri & Checkpoint 6)
# Sec 7: 61-70 (Histopatolojik Özellikler: Koilositoz, Atipi ve Kolposkopi & Checkpoint 7)
# Sec 8: 71-80 (Pap Smear Taraması, Bethesda Sistemi ve HPV DNA Testi & Checkpoint 8)
# Sec 9: 81-90 (HPV Aşılaması: Hedef Popülasyon, Valanslar ve Koruyuculuk & Checkpoint 9)
# Sec 10: 91-100 (İnvaziv Serviks Karsinomu: Tipler, Fıçı Serviks, Yayılım, Üremi & Checkpoint 10)

print("Planning deck 49...")
