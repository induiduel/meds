#!/usr/bin/env python3
"""
Evrensel Mekanizma ve Yolak Çıkarıcı Motoru (Universal Pathway & Mechanism Engine)
Tıp fakültesi amfi ders notlarından, PDF slaytlarından veya konu metinlerinden
adım adım dinamik görselleştirme şemalarını (MechanismPathway) otomatik olarak çıkarır ve üretir.

Kullanım:
    python3 scripts/mechanism_generator/pathway_engine.py --metin "Apoptoz kaskadı..."
    python3 scripts/mechanism_generator/pathway_engine.py --ders-id "k1p-k1-04-hucre-hasari-ve-nekroz-i"
"""

import json
import os
import re
import sys
from typing import Dict, List, Any, Optional

SYSTEM_PROMPT = """Sen tıp fakültesi eğitiminde uzmanlaşmış bir tıbbi mekanizma modelleme asistanısın.
Sana verilen tıp dersi metnini, slaytını veya PDF içeriğini analiz ederek, konudaki biyolojik, 
biyokimyasal, fizyopatolojik veya farmakolojik süreci "Adım Adım Animasyonlu Mekanizma Şeması"na dönüştüreceksin.

Dönüştürülecek şema JSON formatında olmalı ve şu yapıyı taşımalıdır:
{
  "id": "benzersiz-kebab-case-id",
  "title": "Mekanizmanın Tam Başlığı",
  "subtitle": "Kısa alt başlık ve kilit enzim/ilaçlar",
  "discipline": "Dersin Disiplini (örn. Tıbbi Patoloji, Farmakoloji, Fizyoloji)",
  "summary": "1-2 cümlelik genel mekanizma özeti",
  "nodes": [
    {
      "id": "node_id",
      "label": "Görünen Başlık",
      "sublabel": "Kısa açıklama veya molekül adı",
      "type": "substrate | enzyme | intermediate | product | drug_inhibitor | drug_activator | cell | clinical_effect",
      "badge": "Kısa kategori etiketi (örn. Enzim, (-) İlaç, Son Ürün)",
      "tooltip": "Detaylı tıbbi açıklama"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "from": "kaynak_node_id",
      "to": "hedef_node_id",
      "type": "conversion | inhibition | activation | synthesis",
      "label": "Basamak veya enzim adı"
    }
  ],
  "steps": [
    {
      "stepNumber": 1,
      "title": "Aşama 1: ...",
      "subtitle": "Aşamanın alt başlığı",
      "description": "- **Madde 1:** Açıklama\\n- **Madde 2:** Açıklama",
      "narration": "EMA seslendiricisinin okuyacağı akıcı, profesyonel, tane tane Türkçe konuşma metni (30-60 kelime).",
      "activeNodeIds": ["bu_adimda_parlayan_node_idleri"],
      "activeEdgeIds": ["bu_adimda_parlayan_ok_idleri"],
      "spotlight": "📌 [SINAV SPOTU] Bu adıma dair en kritik TUS/komite bilgisi.",
      "durationSeconds": 10
    }
  ]
}

Kurallar:
1. Kesinlikle hayali veya spekülatif bilgi uydurma; ders metnindeki tıbbi gerçeklere tam sadık kal.
2. Düğümler (nodes) mantıksal bir akış izlemeli (Başlangıç -> Enzim/Dönüşüm -> Ara Ürün -> Son Ürün/Klinik Yanıt).
3. İlaçlar ve inhibitörler varsa mutlaka 'drug_inhibitor' ve 'inhibition' oku ile basamağa bağlanmalı.
4. Narration (EMA metni) tıp öğrencisine bir hoca gibi tane tane, anlaşılır ve vurgulu hitap etmeli.
5. Her adımda spotlight (sınav spotu) mutlaka bulunmalı.
"""

# Mekanizma adaylarını tespit etmek için anahtar kelimeler
MECHANISM_KEYWORDS = [
    r'kaskad', r'yolak', r'yolağı', r'mekanizma', r'aktivasyon', r'inhibisyon',
    r'sentez', r'enzim', r'araşidonik', r'apoptoz', r'kaspaz', r'koagülasyon',
    r'hemostaz', r'kompleman', r'adezyon', r'marjinasyon', r'transmigrasyon',
    r'reseptör', r'sinyal', r'fosforilasyon', r'kemotaksis'
]

def detect_mechanism_in_text(text: str) -> bool:
    """Verilen metinde görselleştirilebilir bir mekanizma olup olmadığını tespit eder."""
    matches = 0
    lower = text.lower()
    for kw in MECHANISM_KEYWORDS:
        if re.search(kw, lower):
            matches += 1
    return matches >= 2


def build_pathway_prompt(lecture_title: str, slide_title: str, text: str) -> str:
    """LLM için zenginleştirilmiş çıkarım promptu hazırlar."""
    return f"""Aşağıdaki tıp fakültesi ders içeriğini analiz et ve adım adım görselleştirilebilir bir MechanismPathway JSON yapısı üret:

Ders Başlığı: {lecture_title}
Slayt Başlığı: {slide_title}

İçerik:
\"\"\"
{text}
\"\"\"

Yalnızca geçerli JSON formatında yanıt ver. Markdown kod bloğu ```json ... ``` kullanabilirsin."""


if __name__ == '__main__':
    print("Evrensel Mekanizma Motoru Hazır.")
    print("Tespit edilen anahtar desenler:", len(MECHANISM_KEYWORDS))
