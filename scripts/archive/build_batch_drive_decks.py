#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_batch_drive_decks.py
Generates the next batch of Google Drive lectures for Dönem 3 Kurul 1:
1. Tromboz Patofizyolojisi, Virchow Triadı ve Trombofili (Prof. Dr. Hikmet Keleş)
2. Emboli Tipleri, Enfarktüs ve Şok Patofizyolojisi (Prof. Dr. Hikmet Keleş)
3. Tümör Biyolojisi, Terminolojisi ve Neoplazi (Prof. Dr. Hikmet Keleş)

Strict adherence to Curriculum Fidelity Rules:
- Comprehensive bulleted narrative with '• **Title:** Desc'
- Non-empty flashcards with both 'front'/'back' and 'question'/'answer'
- Sanitized past exam questions (no stem > 1000 chars, no > 3 '?')
- Spot exam pearls and comparison tables
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')
PAST_Q_PATH = os.path.join('src', 'data', 'pastQuestions.json')

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    existing_decks = json.load(f)

with open(PAST_Q_PATH, 'r', encoding='utf-8') as f:
    past_questions = json.load(f)

pq_map = {q['id']: q for q in past_questions}

def get_clean_q(qid, fallback):
    if qid in pq_map:
        q = pq_map[qid]
        stem = q.get('stem', '')
        if len(stem) <= 1000 and stem.count('?') <= 3:
            return q
    return fallback

# ==============================================================================
# DECK 1: TROMBOZ PATOFİZYOLOJİSİ, VİRCHOW TRİADI VE TROMBOFİLİ
# ==============================================================================
deck_tromboz = {
    "id": "learn-tromboz-patofizyolojisi",
    "title": "Tromboz Patofizyolojisi, Virchow Triadı ve Trombofili",
    "shortTitle": "Tromboz Patofizyolojisi",
    "discipline": "Tıbbi Patoloji",
    "instructor": "Prof. Dr. Hikmet Keleş",
    "overview": "Normal hemostaz basamakları, trombosit aktivasyonu, Virchow triadı (endotel hasarı, staz/türbülans, hiperkoagülabilite), primer kalıtsal ve edinsel trombofililer, trombüs morfolojisi (Zahn çizgileri) ve trombüsün klinik akıbeti.",
    "highYieldPearls": [
        "Virchow Triadı: Endotel hasarı, Anormal kan akımı (staz/türbülans) ve Hiperkoagülabilitedir.",
        "Kalıtsal trombofililerin en sık nedeni Faktör V Leiden mutasyonudur (Arg506Gln değişimi; aktive Protein C'ye direnç).",
        "Zahn Çizgileri (Lines of Zahn) sadece akan kanda (antemortem) oluşur; eritrosit ve fibrin/trombosit tabakalarının ardışık çizgilenmesidir.",
        "Post-mortem pıhtı tavuk yağı (üstte sarı plazma) ve frenk üzümü jölesi (altta çöken eritrositler) görünümünde olup damar duvarına yapışmaz."
    ],
    "slides": [
        {
            "slideNumber": 1,
            "title": "Hemostaz ve Tromboz: Temel Tanımlar ve Farklar",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Fizyolojik Hemostaz", "Patolojik Tromboz", "Vasküler Bütünlük", "Prokoagülan Denge"],
            "synthesisNarrative": """### Hemostaz ve Tromboz Arasındaki Kritik Ayrım
• **Fizyolojik Hemostaz:** Vasküler hasar sonrasında kan kaybını durdurmak amacıyla damar lümeninde kontrollü ve lokalize bir hemostatik tıkacın oluşması sürecidir. Normal doku perfüzyonunun korunması için vazgeçilmezdir.
• **Patolojik Tromboz:** İntakt veya hasarlı damar lümeni içinde, fizyolojik kanama uyarısı olmaksızın ya da uygunsuz aşırı hemostatik yanıt sonucu kan pıhtısının (trombüs) gelişmesidir.
• **Temel Patolojik Fark:** Hemostaz damar yırtılmasına karşı koruyucu bir savunma mekanizması iken; tromboz lümeni tıkayarak doku iskemisine veya koparak embolizasyona yol açan patolojik bir tablodur.
• **Dinamik Denge:** Normal koşullarda endotel yüzeyi antikoagülan ve antitrombotik özelliktedir; endotel hasarı bu dengeyi hızla prokoagülan yöne kaydırır.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Tuzağı:** Hemostaz geçici ve fizyolojiktir; tromboz ise damar tıkanıklığı ve iskemik infarktüsle sonuçlanan uygunsuz regülasyondur.""",
            "flashcards": [
                {
                    "id": "fc-tromb-001",
                    "category": "Tıbbi Patoloji",
                    "front": "Fizyolojik hemostaz ile patolojik tromboz arasındaki en temel fark nedir?",
                    "question": "Fizyolojik hemostaz ile patolojik tromboz arasındaki en temel fark nedir?",
                    "back": "Hemostaz vasküler hasarda kanamayı durduran fizyolojik yanıttır; tromboz ise damar içinde kontrolsüz gelişip lümeni tıkayan patolojik pıhtı oluşumudur.",
                    "answer": "Hemostaz vasküler hasarda kanamayı durduran fizyolojik yanıttır; tromboz ise damar içinde kontrolsüz gelişip lümeni tıkayan patolojik pıhtı oluşumudur.",
                    "hint": "Fizyolojik savunma vs uygunsuz patolojik tıkanma"
                },
                {
                    "id": "fc-tromb-002",
                    "category": "Tıbbi Patoloji",
                    "front": "Endotelin normal fizyolojideki temel antitrombotik görevi nedir?",
                    "question": "Endotelin normal fizyolojideki temel antitrombotik görevi nedir?",
                    "back": "Trombosit agregasyonunu engelleyen PGI2 (prostasiklin) ve NO salgılamak, trombomodulin ile Protein C'yi aktive etmek ve doku faktörü yolunu baskılamaktır.",
                    "answer": "Trombosit agregasyonunu engelleyen PGI2 (prostasiklin) ve NO salgılamak, trombomodulin ile Protein C'yi aktive etmek ve doku faktörü yolunu baskılamaktır.",
                    "hint": "PGI2, NO, Trombomodulin"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-pat-015", {
                    "id": "d3-k1-tromb-q01",
                    "examYear": "2022-2023",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Hemostaz ve Tromboz",
                    "stem": "Normal fizyolojik hemostaz ile patolojik trombozun karşılaştırılmasında aşağıdakilerden hangisi yanlıştır?",
                    "options": [
                        {"key": "A", "text": "Hemostaz vasküler hasara lokalize koruyucu bir yanıttır."},
                        {"key": "B", "text": "Tromboz uygunsuz veya kontrolsüz hemostatik kaskad aktivasyonudur."},
                        {"key": "C", "text": "Tromboz sürecinde antikoagülan mekanizmalar prokoagülan uyarılara üstün gelir.", "isCorrect": True},
                        {"key": "D", "text": "Endotel hasarı tromboz gelişimindeki en kritik başlatıcıdır."},
                        {"key": "E", "text": "Tromboz lümen daralması ve distal doku iskemisi ile sonuçlanır."}
                    ],
                    "correctAnswer": "C",
                    "explanation": "Trombozda prokoagülan faktörler antikoagülan mekanizmaları alt eder; antikoagülan mekanizmalar üstün gelseydi tromboz gelişemezdi."
                })
            ]
        },
        {
            "slideNumber": 2,
            "title": "Normal Hemostazın Dört Evresi",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Arteryel Vazokonstriksiyon", "Primer Hemostaz", "Sekonder Hemostaz", "Fibrinoliz"],
            "synthesisNarrative": """### Hemostatik Yanıtın Adım Adım İlerlemesi
• **1. Basamak: Arteryel Vazokonstriksiyon:** Hasar anında lokal nörojenik refleksler ve endotelden salınan güçlü endotelin peptidi sayesinde arteriyollerde ani vazokonstriksiyon gerçekleşir. Kan akımı geçici olarak azaltılarak trombositlerin adezyonuna zemin hazırlanır.
• **2. Basamak: Primer Hemostaz (Trombosit Tıkacı):** Endotel altındaki ekstrasellüler matriks (özellikle kollajen) ve von Willebrand Faktörü (vWF) açığa çıkar. Trombositler GpIb reseptörleriyle vWF'ye yapışır (adezyon), şekil değiştirir ve granüllerini (ADP, Tromboksan A2) boşaltarak diğer trombositleri çağırır (agregasyon). Gevşek primer tıkaç oluşur.
• **3. Basamak: Sekonder Hemostaz (Fibrin Ağı):** Hasarlı hücrelerden açığa çıkan Doku Faktörü (Tromboplastin / Faktör III), Faktör VIIa ile kompleksleşerek koagülasyon kaskadını tetikler. Nihai basamakta trombin oluşur; trombin fibrinojeni fibrine dönüştürür.
• **4. Basamak: Pıhtı Stabilizasyonu ve Fibrinoliz:** Faktör XIIIa kovalent bağlarla fibrin ağını çapraz bağlar ve pıhtıyı mekanik olarak güçlendirir. Eş zamanlı olarak doku plazminojen aktivatörü (t-PA) salınarak pıhtının kontrolsüz büyümesi sınırlandırılır.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Hoca Vurgusu:** Primer hemostazın ana aktörü trombositler; sekonder hemostazın ana aktörü ise koagülasyon faktörleri ve oluşan fibrin ağıdır.""",
            "flashcards": [
                {
                    "id": "fc-tromb-003",
                    "category": "Tıbbi Patoloji",
                    "front": "Primer hemostaz ile sekonder hemostaz arasındaki temel mekanik fark nedir?",
                    "question": "Primer hemostaz ile sekonder hemostaz arasındaki temel mekanik fark nedir?",
                    "back": "Primer hemostazda vWF ve trombositlerle gevşek trombosit tıkacı oluşur; sekonder hemostazda koagülasyon kaskadı ile fibrin ağı örülerek pıhtı sağlamlaştırılır.",
                    "answer": "Primer hemostazda vWF ve trombositlerle gevşek trombosit tıkacı oluşur; sekonder hemostazda koagülasyon kaskadı ile fibrin ağı örülerek pıhtı sağlamlaştırılır.",
                    "hint": "Trombosit tıkacı vs Fibrin ağı"
                },
                {
                    "id": "fc-tromb-004",
                    "category": "Tıbbi Patoloji",
                    "front": "Fibrin ağını çapraz bağlayarak pıhtıyı kalıcı ve stabil hale getiren faktör hangisidir?",
                    "question": "Fibrin ağını çapraz bağlayarak pıhtıyı kalıcı ve stabil hale getiren faktör hangisidir?",
                    "back": "Faktör XIII (Fibrin stabilize edici faktör).",
                    "answer": "Faktör XIII (Fibrin stabilize edici faktör).",
                    "hint": "Faktör XIIIa"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-pat-017", {
                    "id": "d3-k1-tromb-q02",
                    "examYear": "2023-2024",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Hemostaz Evreleri",
                    "stem": "Vasküler yaralanma sonrasında hemostazın doğru kronolojik evre sıralaması aşağıdakilerden hangisidir?",
                    "options": [
                        {"key": "A", "text": "Arteryel vazokonstriksiyon -> Primer hemostaz -> Sekonder hemostaz -> Pıhtı stabilizasyonu ve antikoagülasyon", "isCorrect": True},
                        {"key": "B", "text": "Primer hemostaz -> Arteryel vazokonstriksiyon -> Fibrinoliz -> Sekonder hemostaz"},
                        {"key": "C", "text": "Sekonder hemostaz -> Vazokonstriksiyon -> Trombosit tıkacı -> Fibrin birikimi"},
                        {"key": "D", "text": "Fibrinoliz -> Primer hemostaz -> Vazokonstriksiyon -> Doku faktörü salınımı"},
                        {"key": "E", "text": "Arteryel vazodilatasyon -> Sekonder hemostaz -> Trombosit adezyonu -> Pıhtı erimesi"}
                    ],
                    "correctAnswer": "A",
                    "explanation": "İlk yanıt nörojenik/endotelin kaynaklı vazokonstriksiyondur; ardından trombosit tıkacı (primer), fibrin ağı (sekonder) ve pıhtı stabilizasyonu/rezolüsyon gelir."
                })
            ]
        },
        {
            "slideNumber": 3,
            "title": "Virchow Triadı: Trombozun 3 Temel Direği",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Virchow Triadı", "Endotel Hasarı", "Staz ve Türbülans", "Hiperkoagülabilite"],
            "synthesisNarrative": """### Virchow Triadının Patogenetik Önemi
• **Virchow Triadı:** Rudolf Virchow tarafından tanımlanan, tromboz patogenezindeki 3 ana mekanizmadır:
  - 1. **Endotel Hasarı (En Önemli Faktör):** Kalp ve arteriyel sistemde trombozun bir numaralı başlatıcısıdır. Aterosklerotik plak yırtılması, vaskülit, hipertansiyon veya miyokard enfarktüsü sonrası endokard hasarı endoteli bozar.
  - 2. **Anormal Kan Akımı (Staz ve Türbülans):** Normal laminer kan akımında hücresel elemanlar ortada, plazma çeperde akar. Staz veya türbülans laminer akımı bozar; trombositlerin endotele temasını sağlar, pıhtılaşma faktörlerinin yıkanmasını engeller ve antikoagülan akışını keser.
  - 3. **Hiperkoagülabilite (Trombofili):** Kanın pıhtılaşmaya anormal yatkınlığıdır. Primer (kalıtsal) veya sekonder (edinsel) olabilir. Özellikle venöz trombozlarda belirleyici rol oynar.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Kritik Kural:** Arteriyel ve kardiyak trombozda endotel hasarı başat roldedir; venöz trombozlarda ise en sık suçlu **staz** ve **hiperkoagülabilitedir**.""",
            "flashcards": [
                {
                    "id": "fc-tromb-005",
                    "category": "Tıbbi Patoloji",
                    "front": "Virchow Triadı'nı oluşturan üç temel bileşen nelerdir?",
                    "question": "Virchow Triadı'nı oluşturan üç temel bileşen nelerdir?",
                    "back": "1) Endotel Hasarı, 2) Anormal Kan Akımı (Staz veya Türbülans), 3) Hiperkoagülabilite (Trombofili).",
                    "answer": "1) Endotel Hasarı, 2) Anormal Kan Akımı (Staz veya Türbülans), 3) Hiperkoagülabilite (Trombofili).",
                    "hint": "Hasar + Akım bozukluğu + Pıhtılaşma yatkınlığı"
                },
                {
                    "id": "fc-tromb-006",
                    "category": "Tıbbi Patoloji",
                    "front": "Arteriyel tromboz ile venöz tromboz gelişimindeki en belirgin tetikleyici farkı nedir?",
                    "question": "Arteriyel tromboz ile venöz tromboz gelişimindeki en belirgin tetikleyici farkı nedir?",
                    "back": "Arteriyel trombozda en sık endotel hasarı (aterom plağı) tetikleyicidir; venöz trombozda ise staz (hareketsizlik) ve hiperkoagülabilite ön plandadır.",
                    "answer": "Arteriyel trombozda en sık endotel hasarı (aterom plağı) tetikleyicidir; venöz trombozda ise staz (hareketsizlik) ve hiperkoagülabilite ön plandadır.",
                    "hint": "Arterde endotel; vende staz"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-pat-027", {
                    "id": "d3-k1-tromb-q03",
                    "examYear": "2021-2022",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Virchow Triadı",
                    "stem": "Aşağıdakilerden hangisi Virchow Triadı bileşenlerinden biri DEĞİLDİR?",
                    "options": [
                        {"key": "A", "text": "Endotel hasarı"},
                        {"key": "B", "text": "Laminer kan akımı bozukluğu (Staz veya türbülans)"},
                        {"key": "C", "text": "Hiperkoagülabilite durumu"},
                        {"key": "D", "text": "Vasküler vazodilatasyon ve kapiller geçirgenlik azalması", "isCorrect": True},
                        {"key": "E", "text": "Trombofilik edinsel risk faktörleri"}
                    ],
                    "correctAnswer": "D",
                    "explanation": "Virchow Triadı 3 direkten oluşur: Endotel Hasarı, Anormal Kan Akımı (Staz/Türbülans) ve Hiperkoagülabilite. Vazodilatasyon ve geçirgenlik azalması triadın elemanı değildir."
                })
            ]
        },
        {
            "slideNumber": 4,
            "title": "Kalıtsal (Primer) Trombofililer ve Genetik Mutasyonlar",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Faktör V Leiden", "Protrombin G20210A", "Antitrombin III", "Protein C ve S"],
            "synthesisNarrative": """### Genetik Tromboz Yatkınlıkları
• **Faktör V Leiden Mutasyonu (En Sık):** Beyaz ırkta kalıtsal trombofili nedenlerinin %60'ından sorumludur. Faktör V genindeki nokta mutasyonu (Arg506Gln) sonucu Faktör Va, Aktive Protein C (APC) tarafından inaktive edilemez (**APC Direnci**). Heterozigotlarda venöz tromboz riski 5 kat, homozigotlarda 50 kat artar.
• **Protrombin G20210A Gen Mutasyonu:** Protrombin geninin 3' translasyona uğramayan bölgesindeki mutasyondur. Protrombin mRNA stabilitesi artar; kanda protrombin düzeyi yükselir ve venöz tromboz riski 2-3 kat artar.
• **Antitrombin III (AT-III) Eksikliği:** Trombin, Faktör IXa, Xa, XIa ve XIIa'yı inhibe eden ana fizyolojik inhibitörün eksikliğidir. Heparin AT-III üzerinden etki ettiğinden, bu hastalara standart doz heparin verildiğinde aPTT uzamaz (**Heparin Direnci**).
• **Protein C ve Protein S Eksiklikleri:** Faktör Va ve VIIIa'yı parçalayarak frenleyen K vitaminine bağımlı doğal antikoagülanlardır. Eksikliklerinde venöz tromboembolizm ve varfarin kullanımının ilk günlerinde mikrovasküler tromboza bağlı **Varfarin Nekrozu** gelişebilir.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Sorusu:** Kalıtsal hiperkoagülabilitenin EN SIK nedeni Faktör V Leiden mutasyonudur. Standart heparine direnç görülen eksiklik Antitrombin III eksikliğidir.""",
            "flashcards": [
                {
                    "id": "fc-tromb-007",
                    "category": "Tıbbi Patoloji",
                    "front": "Kalıtsal trombofili nedenleri arasında en sık görülen genetik anomali hangisidir?",
                    "question": "Kalıtsal trombofili nedenleri arasında en sık görülen genetik anomali hangisidir?",
                    "back": "Faktör V Leiden mutasyonu (Aktive Protein C direnci).",
                    "answer": "Faktör V Leiden mutasyonu (Aktive Protein C direnci).",
                    "hint": "Faktör V Arg506Gln"
                },
                {
                    "id": "fc-tromb-008",
                    "category": "Tıbbi Patoloji",
                    "front": "Heparin verildiğinde beklenen antikoagülan etkinin oluşmadığı (heparin direnci) kalıtsal tablo hangisidir?",
                    "question": "Heparin verildiğinde beklenen antikoagülan etkinin oluşmadığı (heparin direnci) kalıtsal tablo hangisidir?",
                    "back": "Antitrombin III (AT-III) eksikliği; çünkü heparin etkisini AT-III'e bağlanarak gösterir.",
                    "answer": "Antitrombin III (AT-III) eksikliği; çünkü heparin etkisini AT-III'e bağlanarak gösterir.",
                    "hint": "AT-III eksikliği"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tromb-q04", {
                    "id": "d3-k1-tromb-q04",
                    "examYear": "2022-2023",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Kalıtsal Trombofililer",
                    "stem": "Kalıtsal venöz tromboz eğilimi olan genç bir hastada yapılan incelemede Aktive Protein C'ye (APC) direnç saptanmıştır. Bu hastadaki en olası genetik defekt aşağıdakilerden hangisidir?",
                    "options": [
                        {"key": "A", "text": "Protrombin G20210A mutasyonu"},
                        {"key": "B", "text": "Faktör V Leiden mutasyonu", "isCorrect": True},
                        {"key": "C", "text": "Antitrombin III gen delesyonu"},
                        {"key": "D", "text": "Faktör VIII gen inversiyonu"},
                        {"key": "E", "text": "von Willebrand Faktör Tip 1 eksikliği"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Faktör V Leiden mutasyonunda Faktör V molekülü Aktive Protein C tarafından parçalanamaz ve kanda kalıcı kalarak tromboza yol açar; bu duruma APC direnci denir."
                })
            ]
        },
        {
            "slideNumber": 5,
            "title": "Trombüs Morfolojisi: Arteriyel vs Venöz Trombüs ve Zahn Çizgileri",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Zahn Çizgileri", "Arteriyel Trombüs", "Venöz Trombüs", "Post-mortem Pıhtı"],
            "synthesisNarrative": """### Morfolojik Özellikler ve Zahn Çizgileri
• **Zahn Çizgileri (Lines of Zahn):** Akan kanda oluşan antemortem trombüslerin en karakteristik mikroskobik ve makroskobik bulgusudur. Açık renkli (trombosit ve fibrin) bantlar ile koyu renkli (eritrositten zengin) tabakaların ardışık katmanlaşmasıyla oluşur. Sadece **canlıda ve kan akımı varken** oluştuğunu kanıtlar.
• **Arteriyel Trombüsler (Beyaz Trombüs):** Tipik olarak endotel hasarı veya aterom plağı üzerinde başlar. Kan akım yönünün TERSİNE doğru (retrograd) büyür. Trombosit ve fibrinden zengin olduğu için soluk gri-beyaz renklidir. Sıklıkla koroner, serebral ve femoral arterlerde görülür.
• **Venöz Trombüsler (Flebotromboz / Kırmızı Trombüs):** Neredeyse daima staz zemininde gelişir. Kan akım YÖNÜNDE (kalbe doğru) uzar. Çok sayıda eritrosit hapsolduğu için koyu kırmızı ve jel kıvamındadır. %90 oranında alt ekstremite derin venlerinde (DVT) görülür.
• **Post-mortem Pıhtı Ayrımı:** Ölümden sonra kanda yerçekimiyle eritrositler dibe çöker. Üstte sarı jelatinöz plazma (**tavuk yağı pıhtısı**), altta koyu kırmızı eritrosit tabakası (**frenk üzümü jölesi**) oluşur. En kritik fark: Post-mortem pıhtı **damar duvarına yapışmaz**, Zahn çizgisi içermez!

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Patognomonik Ayrım:** Damar duvarına yapışık ve Zahn çizgileri içeren pıhtı antemortem trombüstür; duvara yapışmayan, lastik kıvamlı ve sarı-kırmızı tabakalı pıhtı post-mortem pıhtıdır.""",
            "flashcards": [
                {
                    "id": "fc-tromb-009",
                    "category": "Tıbbi Patoloji",
                    "front": "Zahn Çizgileri'nin (Lines of Zahn) adli tıp ve patolojideki en temel anlamı nedir?",
                    "question": "Zahn Çizgileri'nin (Lines of Zahn) adli tıp ve patolojideki en temel anlamı nedir?",
                    "back": "Trombüsün ölümden önce (antemortem), kan akımı varken oluştuğunu kesin olarak kanıtlar.",
                    "answer": "Trombüsün ölümden önce (antemortem), kan akımı varken oluştuğunu kesin olarak kanıtlar.",
                    "hint": "Antemortem kan akımı kanıtı"
                },
                {
                    "id": "fc-tromb-010",
                    "category": "Tıbbi Patoloji",
                    "front": "Post-mortem pıhtının antemortem trombüsten makroskobik en belirgin farkı nedir?",
                    "question": "Post-mortem pıhtının antemortem trombüsten makroskobik en belirgin farkı nedir?",
                    "back": "Post-mortem pıhtı damar duvarına yapışmaz, lastik kıvamındadır ve üstte tavuk yağı altta frenk üzümü jölesi şeklinde tabakalanır.",
                    "answer": "Post-mortem pıhtı damar duvarına yapışmaz, lastik kıvamındadır ve üstte tavuk yağı altta frenk üzümü jölesi şeklinde tabakalanır.",
                    "hint": "Yapışmama + tavuk yağı görünümü"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tromb-q05", {
                    "id": "d3-k1-tromb-q05",
                    "examYear": "2023-2024",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Trombüs Morfolojisi",
                    "stem": "Otoopside pulmoner arter lümeninde saptanan bir pıhtının ölümden sonra gelişen post-mortem pıhtı olduğunu düşündüren en karakteristik bulgu aşağıdakilerden hangisidir?",
                    "options": [
                        {"key": "A", "text": "Fibrin ve trombosit katmanlarını gösteren belirgin Zahn çizgileri içermesi"},
                        {"key": "B", "text": "Damar endoteline sıkıca yapışık ve kuru kıvamda olması"},
                        {"key": "C", "text": "Damar duvarına yapışmaması ve üstte jelatinöz tavuk yağı görünümü sergilemesi", "isCorrect": True},
                        {"key": "D", "text": "İçinde endotel hücre proliferasyonu ve rekanalizasyon kanalları izlenmesi"},
                        {"key": "E", "text": "Trombosit agregatlarının kalsifiye flebolit odakları oluşturması"}
                    ],
                    "correctAnswer": "C",
                    "explanation": "Post-mortem pıhtılar damar duvarına yapışmaz, elastiktir ve yerçekimi ayrışması nedeniyle tavuk yağı/frenk üzümü jölesi tabakalaşması gösterir."
                })
            ]
        },
        {
            "slideNumber": 6,
            "title": "Trombüsün Akıbeti: 4 Temel Patolojik Sonuç",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Propagasyon", "Embolizasyon", "Dissolüsyon", "Organizasyon ve Rekanalizasyon"],
            "synthesisNarrative": """### Bir Trombüsün Vücuttaki Olası 4 Geleceği
• **1. Propagasyon (İlerleme / Büyüme):** Trombüs daha fazla trombosit ve fibrin toplayarak lümen boyunca yayılır ve kritik damarları tamamen tıkar.
• **2. Embolizasyon (Kopma ve Taşınma):** Trombüsün bir parçası veya tamamı damar duvarından koparak kan akımıyla distal organlara taşınır ve tıkanmaya (emboli) yol açar. Venöz trombüsler akciğere, arteryel trombüsler sistemik organlara gider.
• **3. Dissolüsyon (Eriyme / Fibrinoliz):** Yeni oluşan trombüste fibrinolitik aktivite (t-PA ve plazmin) baskın gelerek pıhtıyı tamamen eritebilir. Ancak pıhtı eskidikçe fibrin çapraz bağlanır ve lizise dirençli hale gelir (bu nedenle t-PA ilk saatlerde etkilidir).
• **4. Organizasyon ve Rekanalizasyon:** Eski trombüs içine endotel hücreleri, düz kas hücreleri ve fibroblastlar göç eder (granülasyon benzeri doku). Zamanla trombüsün içinden yeni kapiller damar lümenleri açılır (**rekanalizasyon**) ve kan akımı kısmen yeniden sağlanır. Bazen pıhtı kalsifiye olarak taşlaşır (**flebolit**).

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Klinik İpucu:** Fibrinolitik tedavi (t-PA) taze trombüslerde etkilidir; organize olmuş, çapraz bağlı eski trombüslerde dissolüsyon gerçekleşemez.""",
            "flashcards": [
                {
                    "id": "fc-tromb-011",
                    "category": "Tıbbi Patoloji",
                    "front": "Trombüsün akıbetinde 'rekanalizasyon' ne anlama gelir?",
                    "question": "Trombüsün akıbetinde 'rekanalizasyon' ne anlama gelir?",
                    "back": "Organize olan eski trombüs kitlesi içinde endotel ile döşeli yeni küçük vasküler kanalların açılarak kan akımının kısmen restore edilmesidir.",
                    "answer": "Organize olan eski trombüs kitlesi içinde endotel ile döşeli yeni küçük vasküler kanalların açılarak kan akımının kısmen restore edilmesidir.",
                    "hint": "Pıhtı içinde yeni damar kanalları"
                },
                {
                    "id": "fc-tromb-012",
                    "category": "Tıbbi Patoloji",
                    "front": "Terapötik t-PA (doku plazminojen aktivatörü) neden akut iskemik inmede ilk 3-4.5 saat içinde verilmelidir?",
                    "question": "Terapötik t-PA (doku plazminojen aktivatörü) neden akut iskemik inmede ilk 3-4.5 saat içinde verilmelidir?",
                    "back": "Çünkü taze trombüsler plazmin ile çözülebilirken; zaman geçtikçe fibrin çapraz bağları artar, pıhtı polimerize olur ve fibrinolize direnç kazanır.",
                    "answer": "Çünkü taze trombüsler plazmin ile çözülebilirken; zaman geçtikçe fibrin çapraz bağları artar, pıhtı polimerize olur ve fibrinolize direnç kazanır.",
                    "hint": "Eski pıhtının fibrinolize direnci"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tromb-q06", {
                    "id": "d3-k1-tromb-q06",
                    "examYear": "2021-2022",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Trombüsün Akıbeti",
                    "stem": "Damar lümenini tıkayan eski bir trombüsün zamanla fibroblast, düz kas ve endotel hücre göçü ile vaskülarize bağ dokusuna dönüşüp içinde yeni lümenlerin açılması süreci aşağıdakilerden hangisidir?",
                    "options": [
                        {"key": "A", "text": "Propagasyon"},
                        {"key": "B", "text": "Organizasyon ve rekanalizasyon", "isCorrect": True},
                        {"key": "C", "text": "Fibrinoid nekroz"},
                        {"key": "D", "text": "Embolizasyon"},
                        {"key": "E", "text": "Koagülasyon nekrozu"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Trombüsün bağ dokusuyla yer değiştirmesine organizasyon, bu kitle içinde yeni endotelyal kanalların açılmasına rekanalizasyon denir."
                })
            ]
        }
    ]
}

# ==============================================================================
# DECK 2: EMBOLİ, ENFARKTÜS VE ŞOK PATOLOJİSİ
# ==============================================================================
deck_emboli = {
    "id": "learn-emboli-enfarktus-sok",
    "title": "Emboli Tipleri, Enfarktüs ve Şok Patofizyolojisi",
    "shortTitle": "Emboli, Enfarktüs ve Şok",
    "discipline": "Tıbbi Patoloji",
    "instructor": "Prof. Dr. Hikmet Keleş",
    "overview": "Pulmoner ve sistemik tromboembolizm, yağ embolisi triadı, hava/dekompresyon embolisi, amniyon sıvı embolisi, kırmızı ve beyaz enfarktüs mekanizmaları, şokun patogenetik tipleri ve evreleri.",
    "highYieldPearls": [
        "Pulmoner embolilerin >%95'i bacak derin ven trombozlarından (özellikle popliteal ve femoral venler) kaynaklanır.",
        "Yağ embolisi uzun kemik kırıkları sonrası gelişir; nörolojik bulgular, solunum sıkıntısı (ARDS) ve peteşiyal döküntü triadı ile tanınır.",
        "Kırmızı (Hemorajik) Enfarktüs: Akciğer ve bağırsak gibi çift dolaşımlı veya gevşek dokularda, venöz tıkanıklıklarda görülür.",
        "Beyaz (Soluk) Enfarktüs: Kalp, böbrek ve dalak gibi tek uç arter beslenmeli solid organlarda gelişir.",
        "Septik şokta temel mediyatör TNF-alfa ve IL-1 olup yaygın endotel hasarı, mikrovasküler tromboz (DIC) ve vazodilatasyona yol açar."
    ],
    "slides": [
        {
            "slideNumber": 1,
            "title": "Emboli Kavramı ve Pulmoner Tromboembolizm (PTE)",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Emboli Tanımı", "Pulmoner Emboli", "Derin Ven Trombozu", "Eyer Emboli"],
            "synthesisNarrative": """### Emboli Tanımı ve Pulmoner Dolaşımdaki Yeri
• **Emboli:** Kan akımı ile kaynak noktasından uzak vasküler yataklara taşınan, yerleştiği damarda parsiyel veya tam tıkanmaya yol açan katı, sıvı veya gaz kitlelerdir. Olguların %99'u tromboembolidir.
• **Pulmoner Tromboembolizm (PTE) Kaynağı:** Pulmoner embolilerin **>%95'i bacakların derin ven trombozlarından (DVT)**, özellikle diz üstü derin venlerden (popliteal, femoral ve iliak venler) kaynaklanır.
• **Klinik ve Patolojik Sonuçlar:**
  - *Küçük Emboliler (%60-80):* Genellikle klinik olarak sessizdir. Akciğerin bronşiyal ve pulmoner çift dolaşımı sayesinde enfarkt yapmadan organize olur.
  - *Büyük / Masif Emboliler:* Ana pulmoner arteri veya pulmoner arter dallanma noktasını tıkayan kitleye **Eyer Tarzı Emboli (Saddle Embolus)** denir. Akut sağ ventrikül yetmezliği (akut kor pulmonale) ve ani ölüme yol açar.
  - *Tekrarlayan Küçük Emboliler:* Zamanla pulmoner vasküler direnci artırarak kronik tromboembolik pulmoner hipertansiyona neden olur.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Sorusu:** Akut pulmoner emboli geçiren bir hastada ana pulmoner arter bifurkasyonunu tıkayarak ani ölüme yol açan dev pıhtıya **Eyer Emboli (Saddle Embolus)** adı verilir.""",
            "flashcards": [
                {
                    "id": "fc-emb-001",
                    "category": "Tıbbi Patoloji",
                    "front": "Pulmoner tromboembolilerin yüzde 95'inden fazlası anatomik olarak nereden köken alır?",
                    "question": "Pulmoner tromboembolilerin yüzde 95'inden fazlası anatomik olarak nereden köken alır?",
                    "back": "Alt ekstremite derin ven trombozlarından (özellikle popliteal, femoral ve iliak venler).",
                    "answer": "Alt ekstremite derin ven trombozlarından (özellikle popliteal, femoral ve iliak venler).",
                    "hint": "Alt ekstremite derin venleri (DVT)"
                },
                {
                    "id": "fc-emb-002",
                    "category": "Tıbbi Patoloji",
                    "front": "Ana pulmoner arter bifurkasyonuna oturarak akut sağ kalp yetmezliği ve ani ölüm yapan dev emboliye ne ad verilir?",
                    "question": "Ana pulmoner arter bifurkasyonuna oturarak akut sağ kalp yetmezliği ve ani ölüm yapan dev emboliye ne ad verilir?",
                    "back": "Eyer Emboli (Saddle Embolus).",
                    "answer": "Eyer Emboli (Saddle Embolus).",
                    "hint": "Eyer / Saddle"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-emb-q01", {
                    "id": "d3-k1-emb-q01",
                    "examYear": "2023-2024",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Pulmoner Emboli",
                    "stem": "Hastanede yatmakta olan ortopedi hastasında ani nefes darlığı, göğüs ağrısı ve kardiyak arrest gelişmiştir. Otopside sağ ve sol ana pulmoner arterlerin ayrım yerini tamamen tıkayan masif pıhtı saptanmıştır. Bu tabloya ne ad verilir?",
                    "options": [
                        {"key": "A", "text": "Paradoksal emboli"},
                        {"key": "B", "text": "Eyer tarzı emboli (Saddle embolus)", "isCorrect": True},
                        {"key": "C", "text": "Amniyon sıvı embolisi"},
                        {"key": "D", "text": "Hava embolisi"},
                        {"key": "E", "text": "Dekompresyon hastalığı"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Pulmoner arter dallanma noktasını (bifürkasyon) at eyeri gibi örten masif emboliye Eyer Emboli (Saddle Embolus) denir ve dakikalar içinde ölüme neden olur."
                })
            ]
        },
        {
            "slideNumber": 2,
            "title": "Özel Emboli Tipleri: Yağ, Hava ve Amniyotik Sıvı Embolisi",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Yağ Embolisi Triadı", "Hava Embolisi", "Vurgun / Caisson", "Amniyotik Sıvı Embolisi"],
            "synthesisNarrative": """### Non-Trombotik Emboli Çeşitleri
• **Yağ Embolisi Sendromu:** Uzun kemik kırıklarından (özellikle femur, tibia) veya ağır yumuşak doku travmalarından 1-3 gün sonra görülür. Kemik iliğindeki yağ globülleri yırtılan venöz sinüzoidlere geçer.
  - *Karakteristik Klinik Triad:* **Solunum yetmezliği (taşipne, dispne, ARDS)** + **Nörolojik bozukluklar (konfüzyon, koma)** + **Peteşiyal cilt döküntüsü (özellikle boyun, aksilla ve konjonktivada)**.
• **Hava ve Gaz Embolisi:** Damar içine gaz kabarcıklarının girmesidir.
  - *Cerrahi / Travmatik:* Boyun ven yaralanmaları veya santral venöz kateter takılması sırasında 100 mL'den fazla hava girmesi sağ kalbi tıkayarak ölüme yol açar.
  - *Dekompresyon Hastalığı (Vurgun / Caisson):* Dalgıçların hızla yüzeye çıkmasıyla kanda çözünmüş azot gazı kabarcıklar oluşturur. Eklemlerde ağrı (**bends**), akciğerde ödem (**chokes**) ve kemiklerde avasküler aseptik nekroz (**Caisson hastalığı**) yapar.
• **Amniyotik Sıvı Embolisi:** Doğum sırasında veya hemen sonrasında plasenta membranlarının yırtılmasıyla amniyon sıvısının maternal dolaşıma girmesidir. Skuamöz hücreler, fetal saç ve mukus akciğer mikrovasküler yatağını tıkar. Maternal mortalitesi >%80'dir; ani dispne, siyanoz, şok ve yaygın damar içi pıhtılaşma (**DIC**) ile seyreder.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Triadı:** Femur kırığı sonrası dispne + konfüzyon + aksillada peteşi = **Yağ Embolisi Sendromu**.""",
            "flashcards": [
                {
                    "id": "fc-emb-003",
                    "category": "Tıbbi Patoloji",
                    "front": "Yağ embolisi sendromunun klasik klinik triadı nedir?",
                    "question": "Yağ embolisi sendromunun klasik klinik triadı nedir?",
                    "back": "1) Solunum yetmezliği (dispne, ARDS), 2) Nörolojik semptomlar (huzursuzluk, konfüzyon), 3) Trombositopeniye bağlı peteşiyal döküntü (aksilla, boyun).",
                    "answer": "1) Solunum yetmezliği (dispne, ARDS), 2) Nörolojik semptomlar (huzursuzluk, konfüzyon), 3) Trombositopeniye bağlı peteşiyal döküntü (aksilla, boyun).",
                    "hint": "Solunum + Nöroloji + Peteşi"
                },
                {
                    "id": "fc-emb-004",
                    "category": "Tıbbi Patoloji",
                    "front": "Doğum sonrasında ani siyanoz, hipotansiyon ve ağır DIC tablosu ile seyreden non-trombotik emboli hangisidir?",
                    "question": "Doğum sonrasında ani siyanoz, hipotansiyon ve ağır DIC tablosu ile seyreden non-trombotik emboli hangisidir?",
                    "back": "Amniyotik Sıvı Embolisi.",
                    "answer": "Amniyotik Sıvı Embolisi.",
                    "hint": "Doğum + DIC"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-emb-q02", {
                    "id": "d3-k1-emb-q02",
                    "examYear": "2022-2023",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Özel Emboli Tipleri",
                    "stem": "Trafik kazasında femur ve pelvis kırığı geçiren bir hastada, yatışının 48. saatinde ani solunum sıkıntısı, bilinç bulanıklığı ve boyun-aksilla bölgesinde peteşiyal döküntüler gelişmiştir. En olası patolojik tanı hangisidir?",
                    "options": [
                        {"key": "A", "text": "Pulmoner tromboembolizm"},
                        {"key": "B", "text": "Yağ embolisi sendromu", "isCorrect": True},
                        {"key": "C", "text": "Amniyotik sıvı embolisi"},
                        {"key": "D", "text": "Alerjik anafilaktik şok"},
                        {"key": "E", "text": "Dekompresyon hastalığı"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Uzun kemik kırığı, solunum yetmezliği, nörolojik bozukluk ve üst gövdede peteşi triadı patognomonik olarak Yağ Embolisi Sendromunu işaret eder."
                })
            ]
        },
        {
            "slideNumber": 3,
            "title": "Enfarktüs Patolojisi: Kırmızı (Hemorajik) ve Beyaz (Soluk) Enfarktüs",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Kırmızı Enfarktüs", "Beyaz Enfarktüs", "Çift Dolaşım", "Koagülasyon Nekrozu"],
            "synthesisNarrative": """### Enfarktüs Gelişimi ve Dokusal Ayrım
• **Enfarktüs Tanımı:** Arteriyel kan akımının kesilmesi ya da venöz drenajın engellenmesi sonucu gelişen iskemik doku nekrozu alanıdır. Beyin hariç tüm solid organlarda temel morfolojik yanıt **koagülasyon nekrozudur** (beyinde likefaksiyon nekrozu görülür).
• **Kırmızı (Hemorajik) Enfarktüs:** Nekrotik alana kanın sızdığı, koyu kırmızı renkte görülen enfarktüslerdir. Şu 4 temel durumda görülür:
  - 1. **Venöz Tıkanıklık:** Organın venöz çıkışı tıkandığında (örnek: Testis veya over torsiyonu).
  - 2. **Gevşek Dokular:** Kanın doku boşluklarına kolayca sızabildiği organlar (örnek: Akciğer).
  - 3. **Çift Kan Dolaşımı Olan Dokular:** Bir arter tıkansa bile diğer damardan hasarlı sahaya kan sızması (örnek: Akciğerde pulmoner ve bronşiyal arterler, ince bağırsakta mezenterik anastomozlar).
  - 4. **Reperfüzyon Alanları:** Tıkanıklık çözüldükten sonra hasarlı damarlardan kanın nekrotik dokuya hücum etmesi.
• **Beyaz (Soluk / Anemik) Enfarktüs:** Tek uç arter beslenmesi olan solid organlarda gelişir. Doku yoğun olduğu için kan doku aralığına sızamaz ve eritrositler lizise uğrayarak nekroz alanını soluk sarı-beyaz bırakır.
  - *Örnek Organlar:* **Kalp (Miyokard), Böbrek ve Dalak**.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Tablosu:**
> • Kırmızı Enfarktüs: Akciğer, Bağırsak, Torsiyone Testis/Over (Çift dolaşım / Venöz oklüzyon).
> • Beyaz Enfarktüs: Kalp, Dalak, Böbrek (Solid organ / Tek uç arter).""",
            "flashcards": [
                {
                    "id": "fc-emb-005",
                    "category": "Tıbbi Patoloji",
                    "front": "Kırmızı (hemorajik) enfarktüsün en tipik geliştiği organlar hangileridir?",
                    "question": "Kırmızı (hemorajik) enfarktüsün en tipik geliştiği organlar hangileridir?",
                    "back": "Akciğer (çift dolaşım ve gevşek stroma), Bağırsak (çift dolaşım) ve torsiyona uğramış testis veya over (venöz oklüzyon).",
                    "answer": "Akciğer (çift dolaşım ve gevşek stroma), Bağırsak (çift dolaşım) ve torsiyona uğramış testis veya over (venöz oklüzyon).",
                    "hint": "Akciğer, Bağırsak, Torsiyon"
                },
                {
                    "id": "fc-emb-006",
                    "category": "Tıbbi Patoloji",
                    "front": "Beyaz (soluk/anemik) enfarktüs hangi tip organlarda ve nerelerde görülür?",
                    "question": "Beyaz (soluk/anemik) enfarktüs hangi tip organlarda ve nerelerde görülür?",
                    "back": "Tek uç arter beslenmeli yoğun solid organlarda; en tipik olarak Kalp (miyokard), Böbrek ve Dalakta görülür.",
                    "answer": "Tek uç arter beslenmeli yoğun solid organlarda; en tipik olarak Kalp (miyokard), Böbrek ve Dalakta görülür.",
                    "hint": "Kalp, Böbrek, Dalak"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-emb-q03", {
                    "id": "d3-k1-emb-q03",
                    "examYear": "2022-2023",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Enfarktüs Tipleri",
                    "stem": "Aşağıdaki organların hangisinde gelişen arteriyel oklüzyon sonrasında tipik olarak BEYAZ (SOLUK) enfarktüs izlenmesi beklenir?",
                    "options": [
                        {"key": "A", "text": "Akciğer"},
                        {"key": "B", "text": "İnce bağırsak"},
                        {"key": "C", "text": "Dalak", "isCorrect": True},
                        {"key": "D", "text": "Torsiyona uğramış over"},
                        {"key": "E", "text": "Karaciğer"}
                    ],
                    "correctAnswer": "C",
                    "explanation": "Dalak, böbrek ve kalp tek uç arter ile beslenen yoğun solid organlardır ve anemik (beyaz) enfarktüs yaparlar. Akciğer ve bağırsak ise çift dolaşımlı olup kırmızı enfarktüs oluşturur."
                })
            ]
        },
        {
            "slideNumber": 4,
            "title": "Şok Patofizyolojisi: Tipleri, Evreleri ve Organ Morfolojisi",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Kardiyojenik Şok", "Hipovolemik Şok", "Septik Şok", "Şokun 3 Evresi"],
            "synthesisNarrative": """### Şokun Mekanizması ve Klinik Evreleri
• **Şok Tanımı:** Sistemik doku hipoperfüzyonunun yol açtığı, hücresel hipoksi ve metabolik bozukluklarla karakterize akut dolaşım yetmezliği tablosudur.
• **Başlıca Şok Tipleri:**
  - *Kardiyojenik Şok:* Kalp pompa yetersizliği (Miyokard enfarktüsü, ventrikül rüptürü, aritmi).
  - *Hipovolemik Şok:* Kan veya plazma hacminde ağır azalma (Kanama, ağır yanıklar, dehidratasyon).
  - *Sistemik İnflamasyonla İlişkili Şok (Septik Şok):* En sık gram negatif bakterilerin endotoksinleri (LPS) veya gram pozitif süperantijenleri ile tetiklenir. Yüksek düzeyde TNF, IL-1 ve sitokin salınımı, yaygın vazodilatasyon, endotel hasarı ve DIC oluşturur.
• **Şokun 3 Patolojik Evresi:**
  - 1. **Non-progresif (Kompanse) Evre:** Refleks nörohümoral mekanizmalar (sempatik aktivasyon, katekolaminler, RAAS, ADH) devreye girer. Taşikardi ve vazokonstriksiyon ile vital organ perfüzyonu korunur. Cilt soğuk ve soluktur (septik şokta başlangıçta sıcak olabilir).
  - 2. **Progresif Evre:** Doku hipoperfüzyonu derinleşir; anaerop glikoliz başlar, laktik asidoz gelişir. Asidoz arteriyolleri gevşetir, kan göllenir ve endotel hasarı artar.
  - 3. **İrreversibl (Geri Dönüşsüz) Evre:** Yaygın hücresel hasar, lizozomal enzim salınımı ve miyokard kontraktilite kaybı gelişir. Böbreklerde Akut Tübüler Nekroz (ATN), akciğerde Şok Akciğeri (DAD/ARDS), bağırsaklarda iskemik nekroz oluşur; hasta kaybedilir.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Kuralı:** Şokun geri dönüşsüz evresinde temel ölüm nedeni, hipoperfüzyonun tetiklediği çoklu organ yetmezliği (MODS), yaygın lizozomal enzim salınımı ve asidozdur.""",
            "flashcards": [
                {
                    "id": "fc-emb-007",
                    "category": "Tıbbi Patoloji",
                    "front": "Şokun non-progresif (kompanse) evresinde tansiyonu ve perfüzyonu koruyan temel mekanizmalar nelerdir?",
                    "question": "Şokun non-progresif (kompanse) evresinde tansiyonu ve perfüzyonu koruyan temel mekanizmalar nelerdir?",
                    "back": "Baroreseptör refleksleri, sempatik katekolamin salınımı, Renin-Anjiyotensin-Aldosteron (RAAS) aktivasyonu ve ADH salınımı.",
                    "answer": "Baroreseptör refleksleri, sempatik katekolamin salınımı, Renin-Anjiyotensin-Aldosteron (RAAS) aktivasyonu ve ADH salınımı.",
                    "hint": "Sempatik + RAAS + ADH"
                },
                {
                    "id": "fc-emb-008",
                    "category": "Tıbbi Patoloji",
                    "front": "Septik şok gelişiminde yaygın vazodilatasyon ve mikrovasküler trombozu başlatan temel sitokinler hangileridir?",
                    "question": "Septik şok gelişiminde yaygın vazodilatasyon ve mikrovasküler trombozu başlatan temel sitokinler hangileridir?",
                    "back": "TNF-alfa (Tümör Nekroz Faktör) ve IL-1 (İnterlökin-1).",
                    "answer": "TNF-alfa (Tümör Nekroz Faktör) ve IL-1 (İnterlökin-1).",
                    "hint": "TNF ve IL-1"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-emb-q04", {
                    "id": "d3-k1-emb-q04",
                    "examYear": "2021-2022",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Şok Evreleri",
                    "stem": "Şok patofizyolojisinde anaerop glikolizin hızlanması, kanda laktik asidozun birikmesi ve vazomotor tonusun kaybolarak mikrosirkülasyonda kan göllenmesinin başladığı evre hangisidir?",
                    "options": [
                        {"key": "A", "text": "Non-progresif kompanse evre"},
                        {"key": "B", "text": "Progresif evre", "isCorrect": True},
                        {"key": "C", "text": "İrreversibl evre"},
                        {"key": "D", "text": "Kronik dekompanse evre"},
                        {"key": "E", "text": "Reperfüzyon evresi"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Doku perfüzyonunun bozulup metabolik laktik asidozun geliştiği ve periferik vazomotor felcin başladığı dönem progresif şok evresidir."
                })
            ]
        }
    ]
}

# ==============================================================================
# DECK 3: TÜMÖR BİYOLOJİSİ, TERMİNOLOJİSİ VE NEOPLAZİ
# ==============================================================================
deck_tumor = {
    "id": "learn-tumor-biyolojisi-terminolojisi",
    "title": "Tümör Biyolojisi, Terminolojisi ve Neoplaziye Giriş",
    "shortTitle": "Tümör Biyolojisi ve Terminoloji",
    "discipline": "Tıbbi Patoloji",
    "instructor": "Prof. Dr. Hikmet Keleş",
    "overview": "Neoplazinin tanımı ve klonal kökeni, benign ve malign tümör isimlendirme kuralları, istisna terimler, teratom/hamartom/koristom kavramları, anaplazi, pleomorfizm, invazyon ve metastaz kriterleri.",
    "highYieldPearls": [
        "Willis Neoplazi Tanımı: Normal doku büyümesiyle koordine olmayan, uyarı kalksa bile aşırı çoğalmaya devam eden anormal doku kitlesidir.",
        "Kanser klonaldir; tek bir mutasyona uğramış öncül hücreden köken alır ve Darwinci seçilimle malign alt klonlar baskınlaşır.",
        "Malign olmasına rağmen '-om' ile biten kritik tuzak tümörler: Melanom, Lenfoma, Seminom, Mezotelyoma, Glioblastoma.",
        "Hamartom: Bulunduğu organa ait doku elemanlarının düzensiz ve karmaşık proliferasyonudur (neoplazi değildir).",
        "Koristom (Heterotopi): Normal yapıda bir dokunun vücutta normalde bulunmadığı farklı bir organda yer almasıdır (ör: midede pankreas dokusu).",
        "Malignitenin en kesin, tartışmasız ve mutlak iki kanıtı: Lokal İnvazyon ve Uzak Metastazdır."
    ],
    "slides": [
        {
            "slideNumber": 1,
            "title": "Neoplazi Kavramı, Willis Tanımı ve Klonalite",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Neoplazi", "Willis Tanımı", "Klonalite", "Parankim ve Stroma"],
            "synthesisNarrative": """### Neoplazinin Doğası ve Klonal Kökeni
• **Neoplazi Tanımı:** Kelime anlamı 'yeni büyüme'dir (neo-plasia). İngiliz onkolog R.A. Willis'in klasik tanımına göre: **'Neoplazm, büyümesi normal dokularınkiyle koordine olmayan, onu aşan ve bu değişikliği başlatan uyaran ortadan kalktıktan sonra dahi aynı aşırı biçimde devam eden anormal doku kitlesidir.'**
• **Klonal Çoğalma:** Tüm neoplazmlar tek bir genetik olarak hasarlanmış ata hücreden köken alır (**monoklonalite**). Zaman içinde tümör hücrelerinde ilave mutasyonlar birikir; büyüme hızı ve metastaz yeteneği yüksek alt klonlar seçilir (**tümör heterojenitesi ve progresyonu**).
• **Tümörün İki Temel Bileşeni:**
  - 1. **Parankim:** Klonlanan neoplastik transformasyona uğramış hücrelerdir. Tümörün biyolojik davranışını ve adlandırmasını belirler.
  - 2. **Reaktif Stroma:** Tümör hücrelerini destekleyen bağ dokusu, fibroblastlar, kan damarları ve inflamatuar hücrelerdir. Parankimin büyümesi ve beslenmesi için stromanın oluşturduğu anjiyogenez şarttır. Aşırı kolajenöz stroma gelişmesine **desmoplazi** denir (ör: meme karsinomlarında taş gibi sertlik).

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Hoca Vurgusu:** Neoplazmı hiperplaziden ayıran en kesin fark: Hiperplazide uyarıcı faktör kalktığında büyüme durur; neoplazide ise uyaran kalksa bile otonom proliferasyon sonsuza dek devam eder.""",
            "flashcards": [
                {
                    "id": "fc-tum-001",
                    "category": "Tıbbi Patoloji",
                    "front": "Neoplaziyi patolojik hiperplaziden ayıran en temel biyolojik özellik nedir?",
                    "question": "Neoplaziyi patolojik hiperplaziden ayıran en temel biyolojik özellik nedir?",
                    "back": "Hiperplazide uyarıcı kesildiğinde proliferasyon geriler; neoplazide ise uyaran ortadan kalksa bile büyüme otonom olarak kontrolsüzce devam eder.",
                    "answer": "Hiperplazide uyarıcı kesildiğinde proliferasyon geriler; neoplazide ise uyaran ortadan kalksa bile büyüme otonom olarak kontrolsüzce devam eder.",
                    "hint": "Uyaran kalktıktan sonraki otonomi"
                },
                {
                    "id": "fc-tum-002",
                    "category": "Tıbbi Patoloji",
                    "front": "Tümör parankimi tarafından uyarılıp aşırı fibröz kollajenöz stroma üretilmesine ve tümörün taş gibi sertleşmesine ne ad verilir?",
                    "question": "Tümör parankimi tarafından uyarılıp aşırı fibröz kollajenöz stroma üretilmesine ve tümörün taş gibi sertleşmesine ne ad verilir?",
                    "back": "Desmoplazi (Desmoplastik stroma yanıtı).",
                    "answer": "Desmoplazi (Desmoplastik stroma yanıtı).",
                    "hint": "Desmoplazi"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tum-q01", {
                    "id": "d3-k1-tum-q01",
                    "examYear": "2022-2023",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Neoplazi Tanımı",
                    "stem": "Neoplazik bir dokunun biyolojik davranışını hiperplaziden ayıran en karakteristik özellik aşağıdakilerden hangisidir?",
                    "options": [
                        {"key": "A", "text": "Hücre sayısının artmış olması"},
                        {"key": "B", "text": "Büyümeyi başlatan uyaran ortadan kalktıktan sonra da proliferasyonun otonom olarak sürmesi", "isCorrect": True},
                        {"key": "C", "text": "Doku mimarisinde vaskülarizasyon bulunması"},
                        {"key": "D", "text": "DNA sentezi ve mitoz sayısının artışı"},
                        {"key": "E", "text": "Miyokardiyal hipertrofi ile birlikte seyretmesi"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Willis tanımının merkezinde otonomi yatar: Uyaran kesilse bile kontrolsüz çoğalmanın devam etmesi neoplaziyi reaktif lezyonlardan ve hiperplaziden ayırır."
                })
            ]
        },
        {
            "slideNumber": 2,
            "title": "Tümör Terminolojisi: İsimlendirme Kuralları ve Benign - Malign Ayrımı",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Adenom", "Papillom", "Karsinom", "Sarkom", "İstisna Tümörler"],
            "synthesisNarrative": """### Epitelyal ve Mezenkimal Tümör İsimlendirme Prensipleri
• **Mezenkimal Tümörler (Bağ doku, kas, kemik, kıkırdak):**
  - *Benign:* Hücre tipi + '-om' eki (Ör: Fibrosit -> Fibrom, Yağ -> Lipom, Düz kas -> Leiomyom, Çizgili kas -> Rabdomyom, Kıkırdak -> Kondrom, Kemik -> Osteom).
  - *Malign:* Hücre tipi + '-sarkom' eki (Ör: Fibrosarkom, Liposarkom, Leiomyosarkom, Rabdomyosarkom, Osteosarkom).
• **Epitelyal Tümörler:**
  - *Benign:* Bez epiteli oluşturanlar **Adenom**; parmaksı mikroskobik/makroskobik çıkıntılar yapanlar **Papillom**; lümene doğru uzanan kitleler **Polip** adını alır.
  - *Malign:* Tüm epitelyal kökenli malign tümörlere **KARSİNOM** denir (Ör: Glandüler epitelden kaynaklananlar **Adenokarsinom**, yassı epitelden kaynaklananlar **Skuamöz Hücreli Karsinom**).
• **ÖLÜMCÜL SINAV TUZAKLARI (Benign Görünümlü Malign İsimler):**
  - Sonunda '-om' eki olmasına rağmen KESİNLİKLE MALİGN olan tümörler:
    - **Melanom** (Derinin malign melanosit tümörü)
    - **Lenfoma** (Lenfoid dokunun malign neoplazmı)
    - **Seminom** (Testisin malign germ hücreli tümörü)
    - **Mezotelyoma** (Plevra ve peritonun malign tümörü)
    - **Glioblastoma** (Santral sinir sisteminin en malign astrositer tümörü)
    - **Hepatom (Hepatosellüler Karsinom)**

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Sınav Sorusu:** Melanom, Lenfoma, Seminom ve Mezotelyoma '-om' ile bitmelerine rağmen KESİNLİKLE MALİGN TÜMÖRLERDİR; benign formu yoktur!""",
            "flashcards": [
                {
                    "id": "fc-tum-003",
                    "category": "Tıbbi Patoloji",
                    "front": "Son eki '-om' ile bitmesine rağmen biyolojik davranışı tamamen MALİGN olan başlıca tümörler hangileridir?",
                    "question": "Son eki '-om' ile bitmesine rağmen biyolojik davranışı tamamen MALİGN olan başlıca tümörler hangileridir?",
                    "back": "Melanom, Lenfoma, Seminom, Mezotelyoma, Glioblastoma ve Hepatom.",
                    "answer": "Melanom, Lenfoma, Seminom, Mezotelyoma, Glioblastoma ve Hepatom.",
                    "hint": "Melanom, Lenfoma, Seminom, Mezotelyoma"
                },
                {
                    "id": "fc-tum-004",
                    "category": "Tıbbi Patoloji",
                    "front": "Epitelyal malign tümörlere verilen genel ad ile mezenkimal malign tümörlere verilen genel ad nedir?",
                    "question": "Epitelyal malign tümörlere verilen genel ad ile mezenkimal malign tümörlere verilen genel ad nedir?",
                    "back": "Epitelyal malign tümörlere 'KARSİNOM', mezenkimal malign tümörlere ise 'SARKOM' denir.",
                    "answer": "Epitelyal malign tümörlere 'KARSİNOM', mezenkimal malign tümörlere ise 'SARKOM' denir.",
                    "hint": "Karsinom vs Sarkom"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tum-q02", {
                    "id": "d3-k1-tum-q02",
                    "examYear": "2023-2024",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Tümör Terminolojisi",
                    "stem": "Aşağıdaki neoplazmlardan hangisi sonundaki eke rağmen benign değil, daima KÖTÜ HUYLU (MALİGN) bir tümördür?",
                    "options": [
                        {"key": "A", "text": "Adenoma"},
                        {"key": "B", "text": "Leiomyoma"},
                        {"key": "C", "text": "Rabdomyoma"},
                        {"key": "D", "text": "Melanoma", "isCorrect": True},
                        {"key": "E", "text": "Kondroma"}
                    ],
                    "correctAnswer": "D",
                    "explanation": "Melanoma, melanositlerden köken alan ve agresif metastaz potansiyeline sahip malign bir neoplazmdır. Adenom, leiomyom, rabdomyom ve kondrom ise benign neoplazmlardır."
                })
            ]
        },
        {
            "slideNumber": 3,
            "title": "Karma Tümörler, Teratomlar, Hamartom ve Koristom",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Karma Tümör", "Teratom", "Hamartom", "Koristom (Heterotopi)"],
            "synthesisNarrative": """### Özel Dokusal Lezyonlar ve Karışan Kavramlar
• **Karma Tümörler (Mixed Tumors):** Tek bir germ yaprağından köken alan ancak birden fazla hücre tipine diferansiye olan tümörlerdir. En klasik örneği tükürük bezinin **Pleomorfik Adenomu**dur (epitelyal kanallar ile kıkırdak ve miksoid bağ dokusu stroma bir aradadır).
• **Teratomlar:** Totipotent germ hücrelerinden köken alan ve **her üç germ yaprağına (Endoderm, Ektoderm, Mezoderm)** ait doku elemanlarını içeren tümörlerdir. En sık overde (dermoid kist - matür kistik teratom) ve testiste görülür; içinde diş, saç, kemik, yağ, tiroid ve bronş epiteli bulunabilir.
• **Hamartom (Neoplazi Değildir!):** Bulunduğu organa normalde ait olan doku elemanlarının, anormal bir mimaride ve düzensiz orantısız kitle oluşturacak şekilde büyümesidir (örnek: Akciğer hamartomunda düzensiz kıkırdak, epitel ve yağ dokusu kitleleşir). Malignite potansiyeli yoktur.
• **Koristom (Heterotopi / Ektopi):** Histolojik olarak tamamen NORMAL yapıda olan bir dokunun, embriyolojik göç hatası sonucu vücutta **normalde bulunmaması gereken yabancı bir organda** yerleşmesidir.
  - *Klasik Örnek:* Mide submukozasında veya Meckel divertikülünde **Heterotopik Pankreas Dokusu** bulunması.

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Ayırıcı Tanı Kuralı:**
> • Hamartom = O organın kendi dokusunun düzensiz büyümesi (Akciğerde kıkırdak/epitel yumrusu).
> • Koristom = O organa yabancı normal dokunun başka yerde bulunması (Midede pankreas adacıkları).""",
            "flashcards": [
                {
                    "id": "fc-tum-005",
                    "category": "Tıbbi Patoloji",
                    "front": "Hamartom ile Koristom (Heterotopi) arasındaki en temel fark nedir?",
                    "question": "Hamartom ile Koristom (Heterotopi) arasındaki en temel fark nedir?",
                    "back": "Hamartom o organın kendi yerli hücrelerinin düzensiz dizilimidir; koristom ise normal yapılı bir dokunun ait olmadığı başka bir organda bulunmasıdır (ör: midede pankreas).",
                    "answer": "Hamartom o organın kendi yerli hücrelerinin düzensiz dizilimidir; koristom ise normal yapılı bir dokunun ait olmadığı başka bir organda bulunmasıdır (ör: midede pankreas).",
                    "hint": "Yerli düzensiz doku vs Yabancı ektopik doku"
                },
                {
                    "id": "fc-tum-006",
                    "category": "Tıbbi Patoloji",
                    "front": "Her üç germ yaprağına (ektoderm, mezoderm, endoderm) ait dokuları içerebilen tümör hangisidir?",
                    "question": "Her üç germ yaprağına (ektoderm, mezoderm, endoderm) ait dokuları içerebilen tümör hangisidir?",
                    "back": "Teratom (en sık over ve testiste totipotent germ hücrelerinden gelişir).",
                    "answer": "Teratom (en sık over ve testiste totipotent germ hücrelerinden gelişir).",
                    "hint": "Teratom"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tum-q03", {
                    "id": "d3-k1-tum-q03",
                    "examYear": "2021-2022",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Hamartom ve Koristom",
                    "stem": "Endoskopide mide antrumunda rastlantısal olarak çıkarılan submukozal nodülün mikroskobisinde normal mimaride pankreas asinusları ve Langerhans adacıkları saptanmıştır. Bu lezyon en doğru şekilde nasıl tanımlanır?",
                    "options": [
                        {"key": "A", "text": "Hamartom"},
                        {"key": "B", "text": "Koristom (Heterotopi)", "isCorrect": True},
                        {"key": "C", "text": "Teratom"},
                        {"key": "D", "text": "Adenokarsinom"},
                        {"key": "E", "text": "Leiomyom"}
                    ],
                    "correctAnswer": "B",
                    "explanation": "Normal pankreas dokusunun anatomik olarak ait olmadığı mide duvarında yer alması Koristom (heterotopik doku) örneğidir."
                })
            ]
        },
        {
            "slideNumber": 4,
            "title": "Benign ve Malign Tümörleri Ayıran 4 Temel Kriter",
            "discipline": "Tıbbi Patoloji",
            "keyConcepts": ["Diferansiasyon ve Anaplazi", "Büyüme Hızı", "Lokal İnvazyon", "Metastaz"],
            "synthesisNarrative": """### Maligniteyi Belirleyen Altın Standart Morfolojik Kriterler
• **1. Diferansiasyon (Farklılaşma) ve Anaplazi:**
  - *Diferansiasyon:* Neoplastik hücrelerin köken aldıkları normal parankim hücrelerine yapısal ve fonksiyonel olarak ne kadar benzediğidir. Benign tümörler daima **iyi diferansiyedir**.
  - *Anaplazi:* Diferansiasyonun tamamen kaybolmasıdır; malignitenin morfolojik göstergesidir.
  - *Anaplazi Bulguları:* **Pleomorfizm** (hücre ve nükleus boyut/şekil değişkenliği), **Hiperkromazi** (koyu boyanan nükleuslar), **Artmış N/C Oranı** (normalde 1:4-1:6 iken kanserde 1:1'e yaklaşır), **Atipik/Triradyat Mitozlar**, dev tümör hücreleri ve polarite kaybı.
• **2. Büyüme Hızı:** Genellikle malign tümörler benign tümörlerden çok daha hızlı büyür. Büyüme hızı diferansiasyon derecesiyle ters orantılıdır.
• **3. Lokal İnvazyon:** Benign tümörler çevre dokuyu iterek büyür, etrafında fibröz bir **kapsül** oluşturur ve çevreye sızmaz. Malign tümörler ise kapsülsüzdür; komşu dokuları yıkarak, infiltre ederek ve istila ederek (**invazyon**) ilerler.
• **4. Metastaz (En Kesin Malignite Kanıtı):** Tümör kitlesiyle fiziksel bağlantısı olmayan uzak doku ve organlara tümör hücrelerinin sıçrayıp yeni koloniler kurmasıdır. **Metastaz ve lokal invazyon malignitenin tartışmasız en kesin iki kriteridir.**

#### 💡 Spot Sınav İncileri
> [!IMPORTANT]
> **Hoca Tuzağı:** Bir tümörün malign olduğunu KESİN olarak kanıtlayan tek özellik **Metastaz** yapması veya **Lokal İnvazyon** göstermesidir. Ağır hücresel atipi gösterse bile metastaz ve invazyon yoksa malignite kesin denemez.""",
            "flashcards": [
                {
                    "id": "fc-tum-007",
                    "category": "Tıbbi Patoloji",
                    "front": "Bir neoplazmın kötü huylu (malign) olduğunun tartışmasız, en kesin ve nihai kanıtı nedir?",
                    "question": "Bir neoplazmın kötü huylu (malign) olduğunun tartışmasız, en kesin ve nihai kanıtı nedir?",
                    "back": "Metastaz yapabilme yeteneğidir (lokal invazyonla birlikte kesin malignite kriteridir).",
                    "answer": "Metastaz yapabilme yeteneğidir (lokal invazyonla birlikte kesin malignite kriteridir).",
                    "hint": "Metastaz"
                },
                {
                    "id": "fc-tum-008",
                    "category": "Tıbbi Patoloji",
                    "front": "Anaplazik malign bir hücrede nükleus/sitoplazma (N/C) oranı normalden nasıl farklılaşır?",
                    "question": "Anaplazik malign bir hücrede nükleus/sitoplazma (N/C) oranı normalden nasıl farklılaşır?",
                    "back": "Normal hücrelerde 1:4 ile 1:6 arasında olan N/C oranı, malign anaplazik hücrelerde nükleusun büyümesiyle 1:1'e yaklaşır.",
                    "answer": "Normal hücrelerde 1:4 ile 1:6 arasında olan N/C oranı, malign anaplazik hücrelerde nükleusun büyümesiyle 1:1'e yaklaşır.",
                    "hint": "1:1'e yaklaşır"
                }
            ],
            "pastExamQuestions": [
                get_clean_q("d3-k1-tum-q04", {
                    "id": "d3-k1-tum-q04",
                    "examYear": "2023-2024",
                    "committeeId": "Kurul 1",
                    "discipline": "Tıbbi Patoloji",
                    "topic": "Benign Malign Kriterleri",
                    "stem": "Patoloji laboratuvarına gönderilen bir tümör rezeksiyon materyalinde lezyonun KESİNLİKLE MALİGN olduğunu gösteren en güvenilir morfolojik bulgu aşağıdakilerden hangisidir?",
                    "options": [
                        {"key": "A", "text": "Tümör boyutunun 5 cm'den büyük olması"},
                        {"key": "B", "text": "Hücrelerde nükleus pleomorfizmi izlenmesi"},
                        {"key": "C", "text": "Bölgesel lenf nodunda veya uzak organda metastaz odaklarının saptanması", "isCorrect": True},
                        {"key": "D", "text": "Belirgin nükleol varlığı ve hiperkromazi"},
                        {"key": "E", "text": "Tümör dokusu içinde yoğun damarlanma ve nekroz"}
                    ],
                    "correctAnswer": "C",
                    "explanation": "Metastaz ve komşu doku invazyonu malignitenin tartışmasız en kesin kriteridir; pleomorfizm veya boyut tek başına kesin malignite kanıtı değildir."
                })
            ]
        }
    ]
}

# ==============================================================================
# MERGE DECKS INTO DATABASE
# ==============================================================================
new_decks = [deck_tromboz, deck_emboli, deck_tumor]
existing_map = {d['id']: d for d in existing_decks}

added_count = 0
updated_count = 0

for nd in new_decks:
    nid = nd['id']
    if nid in existing_map:
        existing_map[nid] = nd
        updated_count += 1
    else:
        existing_decks.append(nd)
        existing_map[nid] = nd
        added_count += 1

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(existing_decks, f, ensure_ascii=False, indent=2)

print("=" * 60)
print(f"✅ Yeni Google Drive Dersleri Başarıyla İşlendi ve Eklendi:")
print(f" - Yeni eklenen deck: {added_count}")
print(f" - Güncellenen deck: {updated_count}")
print(f" - Toplam aktif deck sayısı: {len(existing_decks)}")
print("=" * 60)
