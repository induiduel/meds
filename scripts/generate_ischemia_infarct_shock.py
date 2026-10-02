# -*- coding: utf-8 -*-
"""
generate_ischemia_infarct_shock.py
Prof. Dr. Hikmet Keleş - Ders 12: Emboli, Enfarktüs ve Şok Patolojisi (Kurul 1 / Dönem 2)
24 slaytlık %500 derinlikli öğrenme güvertesi, 24 özgün çalışma sorusu,
chunk_8 ve index.json entegrasyonu, ansiklopedi ve sözlük zenginleştirmesi.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_ID = "learn-iskemi-infarktus-ve-sok"
DECK_TITLE = "İskemi, İnfarktüs ve Şok Patolojisi"
DISCIPLINE = "Tıbbi Patoloji"
INSTRUCTOR = "Prof. Dr. Hikmet Keleş"
COMMITTEE = "Dönem 2 / 1. Kurul (Hücre ve Doku Hasarı Mekanizmaları)"

print(f"Starting generation for {DECK_TITLE} ({DECK_ID})...")

slides = [
    # SLIDE 1
    {
        "id": "slide-1",
        "title": "Emboli Patofizyolojisi: Tanım, Fiziksel Durumlar ve Dolaşım Dinamikleri",
        "subtitle": "Kan akımı ile taşınan katı, sıvı veya gaz kitlelerin vasküler tıkanma oluşturma mekanizması",
        "content": """**EMBOLİ TANIMI VE GENEL BİYOLOJİSİ**
Emboli, kan akımı ile damar yatağında sürüklenen ve oluştuğu primer odaktan uzaktaki bir vasküler lümene takılarak parsiyel ya da tam tıkanıklığa yol açan damar içi kitlelerdir.

1. **Fiziksel Durumlarına Göre Emboli Tipleri:**
   - **Katı Emboliler:** Açık ara en yaygındır (%99).
     - **Tromboemboli:** Kopmuş trombüs parçaları (%95'ten fazlası!).
     - Aterom plağı debrisleri (kolesterol kristalleri).
     - Tümör embolileri (metastaz aracı).
     - Parazit yumurtaları, yabancı cisimler (talk, kateter parçaları).
   - **Sıvı Emboliler:**
     - **Yağ embolisi:** Kemik kırıkları sonrası kemik iliği kaynaklı nötral yağ damlacıkları.
     - **Amniyon sıvısı embolisi:** Doğum sırasında açığa çıkan plasental-fetal sıvı.
   - **Gaz Embolileri:**
     - **Hava embolisi:** Boyun ven cerrahisi veya travma.
     - **Azot gazı embolisi:** Dekompresyon hastalığı (dalgıçlarda vurgun / caisson hastalığı).

2. **Dolaşım Dinamiklerine Göre Temel Ayrımlar:**
   - **Pulmoner Emboli:** Venöz sistemden kaynaklanır, sağ kalpten geçerek pulmoner arterleri tıkar.
   - **Sistemik (Arteriyel) Emboli:** Sol kalp veya aorttan kaynaklanır, periferik organ arterlerini tıkar.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Emboli Tanımı ve Sıklık Dağılımı:**\n  ▫ Embolilerin **>%99'u tromboemboli** (trombüs kaynaklı) şeklindedir.\n  ▫ Nadir fakat ölümcül tipler: ==Amniyon sıvısı, Yağ ve Gaz embolileri==dir.\n  ▫ Emboli mekanik tıkanma yanında distal vazospazm ve trombosit aktivasyonu da tetikler.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Klinik pratikte saptanan embolilerin ezici çoğunluğu hangi fiziksel ve patolojik kökene sahiptir?* → **Kopmuş trombüs parçalarından oluşan tromboemboli**."
        ],
        "flashcards": [
            {
                "question": "Emboli nedir ve en sık hangi formu görülür?",
                "answer": "Oluştuğu yerden kopup kan akımıyla taşınarak uzak damarları tıkayan katı, sıvı veya gaz kitledir; %99'dan fazlası trombüs kökenli tromboembolidir."
            }
        ],
        "practiceQuestion": {
            "id": "emboli-q1",
            "question": "Vasküler lümende taşınarak tıkanmaya yol açan emboli olgularının etiyolojisi değerlendirildiğinde, tüm klinik vakaların %95'inden fazlasını oluşturan en sık emboli tipi aşağıdakilerden hangisidir?",
            "options": [
                "A) Uzun kemik kırığı sonrası gelişen yağ embolisi",
                "B) Derin ven veya intrakardiyak trombüslerden kopan tromboemboli",
                "C) Dalgıçlarda gözlenen dekompresyon nitrojen gaz embolisi",
                "D) Doğum travması sonrası amniyon sıvısı embolisi",
                "E) Aterosklerotik plak rüptürüne bağlı kolesterol kristal embolisi"
            ],
            "correctAnswer": "B",
            "explanation": "Embolilerin ezici çoğunluğu (>%95) venöz veya arteriyel trombüslerden kopan parçaların dolaşımda sürüklenmesiyle oluşan tromboembolilerdir."
        }
    },

    # SLIDE 2
    {
        "id": "slide-2",
        "title": "Pulmoner Tromboembolizm (PTE): Kaynaklar ve DVT İlişkisi",
        "subtitle": "Alt ekstremite derin venlerinden sağ kalbe ve pulmoner yatağa uzanan ölümcül göç",
        "content": """**PULMONER TROMBOEMBOLİZMİN KAYNAĞI VE EPİDEMİYOLOJİSİ**
Hastanede yatan hastalarda en sık önlenebilir ölüm nedenlerinden biridir.

1. **Primer Kaynak (%95 Kuralı):**
   - Pulmoner embolilerin **>%95'i alt ekstremite derin ven trombozlarından (DVT)** köken alır.
   - Özellikle **diz üzerindeki derin venler** (Popliteal, Femoral ve İliyak venler) masif ve ölümcül embolilerin ana kaynağıdır.
   - Baldır (baldır kası içi soleus/gastroknemius) ven trombozları nadiren majör emboliye yol açar; ancak tedavi edilmezse uyluğa doğru propage olur.

2. **Dolaşım Yolu:**
   - Trombüs bacak derin veninden kopar → Vena kava inferior → Sağ atriyum → Triküspit kapak → Sağ ventrikül → Pulmoner arter gövdesi ve dalları.

3. **Risk Faktörleri (Virchow Zemininde):**
   - Majör ortopedik cerrahi (kalça ve diz protezi), kanser (pankreas, akciğer), uzamış immobilizasyon (>3 gün yatak istirahati), ileri yaş, gebelik/OKS kullanımı ve kalıtsal trombofililer (Faktör V Leiden).""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **PTE Kaynak Kuralı:**\n  ▫ En sık kaynak: ==Diz üzerindeki derin bacak venleri== (*Popliteal, Femoral, İliyak venler*).\n  ▫ Üst ekstremite venleri ve pelvik venler nadir kaynaklardır.\n  ▫ Bir kez PE geçiren hastada yeni bir atak gelişme riski katbekat artar.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Pulmoner tromboembolilerin en sık kaynaklandığı anatomik vasküler odak neresidir?* → **Alt ekstremite derin venleri (popliteal, femoral ve iliak venler)**."
        ],
        "flashcards": [
            {
                "question": "Pulmoner embolilerin yüzde kaçı nereden köken alır?",
                "answer": "%95'ten fazlası alt ekstremite diz üstü derin ven trombozlarından (popliteal, femoral, iliyak venler) köken alır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q2",
            "question": "Klinikte pulmoner tromboembolizm (PTE) tanısı alan bir hastada, embolinin koptuğu primer anatomik vasküler yatak en yüksek olasılıkla aşağıdakilerden hangisidir?",
            "options": [
                "A) Üst ekstremite sefalik ve bazilik venleri",
                "B) Karın duvarı yüzeyel epigastrik venleri",
                "C) Alt ekstremite diz üstü derin venleri (femoral, popliteal, iliyak venler)",
                "D) Mezenterik venöz pleksus",
                "E) Renal venler"
            ],
            "correctAnswer": "C",
            "explanation": "Pulmoner embolilerin %95'ten fazlası alt ekstremitenin diz üstü derin venlerinden (özellikle femoral, popliteal ve iliak venler) kaynaklanır."
        }
    },

    # SLIDE 3
    {
        "id": "slide-3",
        "title": "Eyer Emboli (Saddle Embolus) ve Masif Pulmoner Emboli",
        "subtitle": "Pulmoner arter bifurkasyonunun tıkanması, akut kor pulmonale ve ani ölüm",
        "content": """**MASİF PULMONER EMBOLİ VE EYER EMBOLİSİ**
Pulmoner embolilerin klinik tablosu, embolinin boyutuna ve tıkadığı damar çapına göre tam sessizlikten saniyeler içinde ani ölüme kadar geniş bir yelpazedir.

1. **Eyer Emboli (Saddle Embolus):**
   - Bacak derin veninden kopan çok büyük boyutlu bir trombüs ana pulmoner arterin sağ ve sol dallara ayrıldığı çatala (**bifurkasyona**) oturur ve bir 'eyer' gibi iki ana dalı birden kilitler.

2. **Klinik ve Hemodinamik Sonuçlar:**
   - **Pulmoner Vasküler Yatağın %60'ından Fazlasının Akut Tıkanması:**
     - Sağ ventrikülün önünde aşırı bir son-yük (afterload) direnci doğar.
     - Kan akciğerlere pompalanamaz; sol ventriküle kan dönüşü (preload) sıfırlanır.
     - **Akut Kor Pulmonale (Akut Sağ Kalp Yetmezliği):** Sağ ventrikül aniden genişler (akut dilatasyon), ventriküler septum sola doğru itilir.
     - Sistemik hipotansiyon, kardiyojenik şok ve **elektromekanik disosiasyonla ani ölüm** gelişir.
   - Hasta genellikle nefes alamadığını belirterek yere yığılır; dakikalar içinde ölüm gerçekleşir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Eyer Emboli Özellikleri:**\n  ▫ Yerleşim: ==Ana pulmoner arter bifurkasyonu==.\n  ▫ Hemodinami: Pulmoner vasküler yatağın **>%60'ı aniden tıkanır**.\n  ▫ Sonuç: **Akut Kor Pulmonale**, kardiyovasküler kollaps ve ani ölüm.\n  ▫ İskemi veya enfarktüs gelişmeye vakit kalmadan ölüm gerçekleşir!",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Masif pulmoner embolide ani ölüme yol açan primer hemodinamik mekanizma nedir?* → **Pulmoner arter bifurkasyonunun tıkanması sonucu gelişen akut sağ kalp yetmezliği (akut kor pulmonale) ve sol ventrikül doluşunun çökmesi**."
        ],
        "flashcards": [
            {
                "question": "Eyer emboli (saddle embolus) nereye yerleşir ve ölüm mekanizması nedir?",
                "answer": "Ana pulmoner arter bifurkasyonuna oturur; pulmoner yatağın >%60'ını tıkayarak akut sağ ventrikül yetmezliğine (akut kor pulmonale) ve kardiyojenik şoka yol açar."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q3",
            "question": "Kalça protezi operasyonunun 4. gününde aniden şiddetli nefes darlığı, siyanoz ve senkop gelişen 68 yaşındaki hasta resüsitasyona yanıt vermeyerek kaybediliyor. Otopside ana pulmoner arter çatallanmasını tamamen tıkayan dev bir trombüs kitlesi (eyer emboli) saptanıyor. Bu hastada ani ölüme yol açan temel patofizyolojik süreç aşağıdakilerden hangisidir?",
            "options": [
                "A) Akciğer parankiminde yaygın masif hemorajik enfarktüs gelişimi",
                "B) Pulmoner yatağın akut tıkanması sonucu gelişen akut sağ kalp yetmezliği (kor pulmonale) ve kardiyak debinin çökmesi",
                "C) Koroner arterlerin refleks spazmına bağlı akut sol ventrikül enfarktüsü",
                "D) Beyin sapında diffüz nörojenik vazodilatasyon",
                "E) Akut alveolit ve sürfaktan kaybı"
            ],
            "correctAnswer": "B",
            "explanation": "Eyer embolisinde akciğer parankiminde enfarktüs oluşmaya vakit kalmaz; pulmoner vasküler yatağın >%60'ı aniden tıkandığı için akut sağ kalp yetmezliği (akut kor pulmonale), sol ventriküle kan dönememesi ve kardiyojenik şok ile ani ölüm meydana gelir."
        }
    },

    # SLIDE 4
    {
        "id": "slide-4",
        "title": "Akciğerin Çift Kan Dolaşımı ve Pulmoner Enfarktüs Mekanizması",
        "subtitle": "Pulmoner arter ve bronşiyal arterlerin koruyucu kollateral ağı ve istisnaları",
        "content": """**AKCİĞERDE ENFARKTÜS NEDEN NADİRDİR? (ÇİFT DOLAŞIM MUCİZESİ)**
Orta ve küçük boyutlu pulmoner emboliler her zaman doku nekrozuna (enfarktüs) yol açmaz.

1. **Akciğerin Çift Vasküler Beslenmesi:**
   - **Pulmoner Arterler:** Gaz değişimi için venöz kanı taşır.
   - **Bronşiyal Arterler:** Aorttan çıkan temiz arteryel kanı taşır ve parankimi besler.
   - Pulmoner arter dallarından biri tıkandığında, sağlam bronşiyal arter kollateral akımı sayesinde akciğer parankimi oksijensiz kalmaz ve **enfarktüs gelişmez**.

2. **Pulmoner Enfarktüs Ne Zaman Gelişir?**
   - Pulmoner emboli ancak şu iki durumda enfarktüse yol açar:
     1. **Kardiyovasküler Yetmezlik / Konjestif Kalp Yetmezliği:** Sol kalp yetmezliği olan veya hipotansif hastalarda bronşiyal arter perfüzyonu da bozulmuştur; kollateral koruma çöker.
     2. **En Uç (Distal) Dalların Tıkanması:** Çok küçük periferik arteriyollerin tıkanmasında bronşiyal anastomozlar yetersiz kalabilir.
   - Akciğer enfarktüsleri çift kanlanma ve gevşek doku nedeniyle tipik olarak **Kırmızı (Hemorajik) Enfarktüs** morfolojisindedir!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Çift Dolaşım Kuralı:**\n  ▫ Akciğer çift kan dolaşımına sahiptir: ==Pulmoner arter + Bronşiyal arterler==.\n  ▫ Bu nedenle genç ve kalbi sağlam bireylerde pulmoner emboli **enfarktüs yapmaz**!\n  ▫ Pulmoner enfarktüs gelişmesi için hastada genellikle **altta yatan sol kalp yetmezliği** bulunmalıdır.\n  ▫ Gelişen enfarktüs daima **Kırmızı (Hemorajik)** tiptedir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Pulmoner emboli geçiren sağlıklı genç bir hastada akciğer parankiminde enfarktüs gelişmesini engelleyen temel anatomik faktör nedir?* → **Bronşiyal arterlerden sağlanan zengin kollateral çift kan dolaşımı**."
        ],
        "flashcards": [
            {
                "question": "Pulmoner embolilerin çoğunun akciğerde enfarktüs yapmamasının anatomik nedeni nedir?",
                "answer": "Akciğerin hem pulmoner arter hem de aorttan çıkan bronşiyal arterlerle çift kan dolaşımına sahip olmasıdır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q4",
            "question": "Pulmoner emboli olgularının büyük bir kısmında akciğer dokusunda iskemik nekroz (enfarktüs) gelişmemesini sağlayan temel fizyolojik ve anatomik mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Akciğer parankiminin oksijen gereksiniminin sıfır olması",
                "B) Aorttan köken alan bronşiyal arterler sayesinde akciğerin çift kan dolaşımına sahip olması",
                "C) Alveollerdeki yüksek nitrojen gaz basıncı",
                "D) Pulmoner venlerdeki kapakçıkların geriye kan akışını engellemesi",
                "E) Akciğer endotelinde aşırı miktarda trombomodulin bulunması"
            ],
            "correctAnswer": "B",
            "explanation": "Akciğer çift dolaşıma sahiptir (pulmoner arterler ve bronşiyal arterler). Pulmoner arter dalı tıkansa dahi bronşiyal dolaşım parankimi beslemeyi sürdürerek enfarktüs gelişimini önler."
        }
    },

    # SLIDE 5
    {
        "id": "slide-5",
        "title": "Sistemik Tromboembolizm: İntrakardiyak Kaynaklar ve Hedefler",
        "subtitle": "Sol ventrikül, sol atriyum ve aorttan organ yataklarına arteriyel emboli dağılımı",
        "content": """**SİSTEMİK (ARTERİYEL) TROMBOEMBOLİZM**
Sistemik emboliler arteriyel dolaşımda seyahat eder ve uç arterleri tıkayarak distal dokularda iskemik nekroza (enfarktüs) yol açar.

1. **Primer Kaynaklar (%80 Sol Kalp):**
   - **İntrakardiyak Mural Trombüsler (%80-85):**
     - **Sol Ventrikül İnfarktüs Skarları (~%60-65):** Miyokard enfarktüsü sonrası akinetik/diskinetik ventrikül duvarında oluşan trombüsler.
     - **Dilate Sol Atriyum ve Atriyal Fibrilasyon (~%20-25):** Mitral kapak darlığında sol atriyal apendikste gelişen trombüsler.
   - **Diğer Kaynaklar:**
     - Aort anevrizmaları ve ülseröz aterosklerotik plaklar (%10).
     - Kalp kapak vejetasyonları (infektif veya nonbakteriyel endokardit).

2. **Hedef Organ Yatakları:**
   - **Alt Ekstremiteler (%70-75):** Femoral, popliteal arterleri tıkar; akut bacak iskemisi (soğukluk, nabızsızlık, şiddetli ağrı, gangren).
   - **Beyin (%10):** Serebral arterleri tıkayarak **iskemik inmeye (felç)** yol açar.
   - **İntestinal / Mezenterik Yatak:** Mezenter iskemi ve bağırsak kangreni.
   - **Böbrekler ve Dalak:** Kama şeklinde beyaz (soluk) enfarktüsler.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Sistemik Emboli Özeti:**\n  ▫ 1 Numaralı Kaynak: ==Sol Kalp Boşlukları (%80)== (*Sol ventrikül MI skarı ve sol atriyal apendiks*).\n  ▫ 1 Numaralı Hedef: ==Alt Ekstremite Arterleri (%75)==.\n  ▫ 2 Numaralı Hedef: ==Beyin (%10)== (İskemik inme!).\n  ▫ Tıkanan organlarda uç arter yapısı nedeniyle doku nekrozu kaçınılmazdır.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Sorusu:**\n  ▫ *Sistemik arteriyel tromboembolilerin en sık kaynaklandığı odak ve en sık yerleştiği anatomik hedef organ neresidir?* → Kaynak: **Sol ventrikül/atriyum mural trombüsleri**; Hedef: **Alt ekstremiteler**."
        ],
        "flashcards": [
            {
                "question": "Sistemik arteriyel embolilerin en sık kaynağı ve en sık yerleştiği hedef neresidir?",
                "answer": "En sık kaynak: İntrakardiyak sol kalp mural trombüsleri (%80); en sık hedef: Alt ekstremite arterleri (%75)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q5",
            "question": "Atriyal fibrilasyonu olan 72 yaşındaki bir hastada aniden sağ bacakta şiddetli ağrı, solukluk, soğukluk ve nabızsızlık gelişiyor. Acil embolektomi ile femoral arter lümeninden trombüs çıkarılıyor. Bu hastada sistemik embolinin kaynaklandığı en olası intrakardiyak odak aşağıdakilerden hangisidir?",
            "options": [
                "A) Sağ atriyum apendiksi",
                "B) Sol atriyal apendiks mural trombüsü",
                "C) Pulmoner arter kapak vejetasyonu",
                "D) Vena kava inferior lümeni",
                "E) Triküspit kapak kordaları"
            ],
            "correctAnswer": "B",
            "explanation": "Atriyal fibrilasyonda kanın göllenmesi ve staz nedeniyle mural trombüslerin en sık oluştuğu odak sol atriyal apendikstir; buradan kopan pıhtı sistemik arteriyel yolla bacak arterlerini tıkar."
        }
    },

    # SLIDE 6
    {
        "id": "slide-6",
        "title": "Paradoksal Emboli: Sağdan Sola İntrakardiyak Şantlar",
        "subtitle": "Venöz kaynaklı pıhtının Patent Foramen Ovale (PFO) veya ASD ile arteriyel sisteme geçişi",
        "content": """**PARADOKSAL EMBOLİZMİN PATOFİZYOLOJİSİ**
Normalde venöz sistemden kopan bir trombüs sağ kalbe gelir ve akciğer kapiller filtresine takılarak pulmoner emboli oluşturur.

1. **Tanım ve Mekanizma:**
   - Venöz dolaşımdan (DVT) köken alan bir embolinin, sağ kalpten pulmoner dolaşıma gitmek yerine intrakardiyak bir defektten **sağdan sola şant** yaparak sol kalbe ve oradan sistemik arteriyel dolaşıma (örneğin beyne) geçmesidir.

2. **Altta Yatan Kardiyak Defektler:**
   - **Patent Foramen Ovale (PFO):** Erişkinlerin yaklaşık %20-25'inde foramen ovale fonksiyonel olarak kapalı olsa da anatomik olarak açıktır.
   - **Atriyal Septal Defekt (ASD):**
   - **Ventriküler Septal Defekt (VSD):**

3. **Tetikleyici Faktör (Şantın Tersine Dönmesi):**
   - Normalde sol atriyum basıncı sağ atriyumdan yüksektir (soldan sağa kaçak eğilimi vardır).
   - Ancak hastada pulmoner hipertansiyon geliştiğinde, öksürme, ıkınma (Valsalva manevrası) veya büyük bir PE sağ kalbi zorladığında **sağ atriyum basıncı aniden sol atriyum basıncını aşar**.
   - PFO kapağı açılır; venöz bacaktaki pıhtı sağ atriyumdan sol atriyuma geçer ve beyne giderek genç yaşta **kriptojenik iskemik inmeye** yol açar!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Paradoksal Emboli Kriterleri:**\n  ▫ Pıhtının kaynağı: ==Venöz sistem (DVT)==.\n  ▫ Geçiş kapısı: ==Patent Foramen Ovale (PFO) veya ASD==.\n  ▫ Sonuç: Pulmoner emboli yerine **Sistemik arteriyel emboli (Beyin inmesi)**.\n  ▫ Genç bir hastada bacakta DVT varken aynı anda inme (felç) gelişiyorsa akla ilk paradoksal emboli gelmelidir!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Bacağında derin ven trombozu olan genç bir hastada serebral enfarktüs (inme) geliştiğinde en olası intrakardiyak anomali nedir?* → **Patent Foramen Ovale (PFO) / Atriyal Septal Defekt (ASD)**."
        ],
        "flashcards": [
            {
                "question": "Paradoksal emboli nedir ve en sık hangi kardiyak defekt zemininde gelişir?",
                "answer": "Venöz kaynaklı (DVT) bir trombüsün Patent Foramen Ovale (PFO) veya ASD üzerinden sağ kalpten sol kalbe geçip sistemik arteriyel yatağı (örn. beyin) tıkamasıdır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q6",
            "question": "32 yaşında kadın hasta, sol bacağında ağrı ve şişlik (DVT) şikayeti varken aniden gelişen sağ hemipleji ve konuşma bozukluğu (akut iskemik inme) tablosuyla acil servise getiriliyor. Venöz sistemden kaynaklanan bir pıhtının beyin arterlerini tıkamasını açıklayan patolojik tablo ve altta yatan en olası defekt aşağıdakilerden hangisidir?",
            "options": [
                "A) Retrograd emboli - Aort koarktasyonu",
                "B) Paradoksal emboli - Patent Foramen Ovale (PFO)",
                "C) Amniyon sıvı embolisi - Mitral kapak prolapsusu",
                "D) Yağ embolisi - Ventriküler anevrizma",
                "E) Hava embolisi - Duktus arteriozus"
            ],
            "correctAnswer": "B",
            "explanation": "Venöz dolaşımdaki bir trombüsün intrakardiyak sağdan sola şant (en sık PFO veya ASD) aracılığıyla arteriyel sisteme geçerek serebral enfarktüs yapması 'paradoksal emboli' olarak adlandırılır."
        }
    },

    # SLIDE 7
    {
        "id": "slide-7",
        "title": "Yağ Embolisi Sendromu: Uzun Kemik Kırıkları ve Klinik Triad",
        "subtitle": "Kemik iliği yağının dolaşıma karışması, mekanik obstrüksiyon ve biyokimyasal toksisite",
        "content": """**YAĞ EMBOLİSİ SENDROMU (FAT EMBOLISM SYNDROME - FES)**
Özellikle femur ve tibia gibi yağlı kemik iliğinden zengin uzun kemik kırıklarından 1 ila 3 gün sonra ortaya çıkan spesifik bir klinik tablodur.

1. **Patogenez (İki Aşamalı Teori):**
   - **Mekanik Teori:** Kırık bölgesinde yırtılan kemik iliği venülleri içine medüller adipositler ve kemik iliği doku parçaları emilir. Yağ globülleri pulmoner ve serebral mikrosirkülasyona takılır.
   - **Biyokimyasal Toksisite Teorisi:** Yağ damlacıkları vasküler lipazlar tarafından **serbest yağ asitlerine (FFA)** hidrolize edilir. Serbest yağ asitleri endotel hücreleri için doğrudan toksiktir; akut akciğer hasarı (ARDS), yaygın trombosit aktivasyonu ve peteşiyal kanamalara neden olur.

2. **Karakteristik Klinik Triad:**
   - Kırıktan **24-72 saat sonra** aniden başlar:
     1. **Solunum Yetmezliği (Takipne, Dispne, Hipoksemi):** Pulmoner kapiller tıkanma ve ARDS.
     2. **Nörolojik Bulgular:** Huzursuzluk, konfüzyon, ajitasyon, koma (serebral mikroemboliler).
     3. **Peteşiyal Döküntü (Patognomonik):** Üst gövde, boyun, aksilla ve konjonktivada yaygın peteşiler (trombositopeni ve endotel toksisitesine bağlı).
   - Otopside akciğer ve beyin kapillerlerinde yağ damlacıklarını göstermek için rutin parafin kesit yerine **donuk (frozen) kesit ve Oil Red O veya Sudan boyası** kullanılmalıdır!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Yağ Embolisi Sendromu Triadı:**\n  ▫ 1. ==Solunum Yetmezliği (Dispne, Hipoksemi, ARDS)==\n  ▫ 2. ==Nörolojik Değişiklikler (Konfüzyon, Koma)==\n  ▫ 3. ==Peteşiyal Döküntü (Boyun, göğüs, aksilla, konjonktiva)==\n  ▫ Semptomlar kırıktan **1-3 gün sonra** başlar.\n  ▫ Histopatolojide donuk kesitte **Oil Red O / Sudan** pozitif yağ damlacıkları saptanır.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Femur kırığı geçiren bir hastada 48 saat sonra dispne, konfüzyon ve boyun-göğüs bölgesinde peteşiyal döküntüler geliştiğinde en olası tanı nedir?* → **Yağ embolisi sendromu**."
        ],
        "flashcards": [
            {
                "question": "Yağ embolisi sendromunun klasik klinik triadı nedir?",
                "answer": "1) Solunum yetmezliği (hipoksemi, dispne), 2) Nörolojik bozukluklar (konfüzyon, koma), 3) Peteşiyal cilt döküntüsü (aksilla, boyun, konjonktiva)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q7",
            "question": "Motosiklet kazası sonrası izole kapalı femur cisim kırığı nedeniyle yatırılan 22 yaşındaki bir hastada travmanın 36. saatinde aniden takipne, şiddetli dispne, oryantasyon bozukluğu ve boyun ile aksilla bölgesinde yaygın peteşiyal döküntüler gelişiyor. Bu hastada patolojiyi açıklayan en olası tanı ve mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Yağ Embolisi Sendromu - Kemik iliği yağının dolaşıma karışması ve serbest yağ asidi toksisitesi",
                "B) Eyer embolisi - Vena kava inferior tıkanıklığı",
                "C) Hipovolemik şok - Masif iç kanama",
                "D) Anafilaktik şok - Analjezik alerjisi",
                "E) Dekompresyon hastalığı - Azot gazı kabarcıkları"
            ],
            "correctAnswer": "A",
            "explanation": "Uzun kemik (femur) kırığından 24-72 saat sonra ortaya çıkan solunum sıkıntısı, nörolojik semptomlar ve peteşiyal döküntü klasik Yağ Embolisi Sendromu triadıdır."
        }
    },

    # SLIDE 8
    {
        "id": "slide-8",
        "title": "Gaz ve Hava Embolisi: Dekompresyon Hastalığı (Vurgun)",
        "subtitle": "Henry Kanunu, çözünmüş azot gazının kabarcıklaşması ve Caisson hastalığı",
        "content": """**GAZ VE HAVA EMBOLİSİ**
Dolaşım sistemine giren gaz kabarcıkları kapiller damarları tıkayarak mekanik iskemiye ve yabancı cisim reaksiyonuna neden olur.

1. **Hava Embolisi (İatrojenik / Travmatik):**
   - Boyun veya toraks cerrahisi, santral venöz kateter takılması/çıkarılması, doğum veya kürtaj sırasında venöz negatif basınçla hava emilmesi.
   - Ölümcül olabilmesi için genellikle **>100 mL hava** hızla dolaşıma girmelidir; sağ ventrikülde köpüklü hava tıkacı oluşturarak kan akımını durdurur.

2. **Dekompresyon Hastalığı (Vurgun / Caisson Hastalığı):**
   - **Fiziksel İlke (Henry Kanunu):** Yüksek basınç altında gazların sıvılardaki çözünürlüğü artar.
   - Derin deniz dalgıçları veya basınçlı tünel (caisson) işçileri yüksek basınç altında solurken kanda ve yağ dokusunda yüksek miktarda **Azot ($N_2$) gazı** çözünür.
   - Eğer yüzeye aniden (hızlı) çıkılırsa, basınç aniden düşer ve çözünmüş azot kanda sıvı halden çıkarak **gaz kabarcıkları (baloncuklar)** oluşturur (tıpkı gazoz kapağının aniden açılması gibi!).
   - **Klinik Tablo:**
     - **The Bends (Kıvrılma):** Eklem periostu ve iskelet kaslarında oluşan kabarcıklar dayanılmaz eklem ağrılarına yol açar.
     - **The Chokes (Boğulma):** Akciğer mikrosirkülasyonundaki gaz embolileri masif dispne ve göğüs ağrısı yapar.
     - **Caisson Hastalığı (Kronik Form):** Femur başı, tibia ve humerusta gaz kabarcıklarının besleyici damarları tıkaması sonucu gelişen kronik **Aseptik Kemik Nekrozu (Avasküler Nekroz)**.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Vurgun ve Caisson Özeti:**\n  ▫ Gaz Tipi: ==Azot ($N_2$) gazı kabarcıkları==.\n  ▫ *The Bends:* Şiddetli kas ve eklem ağrıları.\n  ▫ *The Chokes:* Pulmoner gaz embolisine bağlı boğulma hissi ve dispne.\n  ▫ *Caisson Hastalığı:* Femur ve humerus başında kalıcı **avasküler osteonekroz**.\n  ▫ Tedavi: **Hiperbarik Oksijen Odası** (azotun yeniden çözünmesi sağlanır).",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Dalgıçlarda aniden su yüzeyine çıkılması sonucu kanda azot kabarcıklarının oluşmasıyla gelişen, kemiklerde avasküler nekroza yol açan tablo nedir?* → **Dekompresyon Hastalığı (Caisson Hastalığı)**."
        ],
        "flashcards": [
            {
                "question": "Dekompresyon hastalığında (vurgun) kanda kabarcık oluşturan gaz hangisidir ve kronik kemik komplikasyonuna ne ad verilir?",
                "answer": "Azot (N2) gazıdır; kronik kemik iskemisi ve nekrozuna Caisson hastalığı (avasküler nekroz) denir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q8",
            "question": "Derin deniz dalışı sonrasında hızla su yüzeyine çıkan profesyonel bir dalgıçta şiddetli eklem ve kas ağrıları (the bends) ile nefes darlığı (the chokes) gelişiyor. Yıllar sonra çekilen kalça grafisinde femur başında avasküler osteonekroz alanları (Caisson hastalığı) saptanıyor. Bu patolojide kanda gaz kabarcıkları oluşturarak emboliye yol açan gaz aşağıdakilerden hangisidir?",
            "options": [
                "A) Karbonmonoksit ($CO$)",
                "B) Karbondioksit ($CO_2$)",
                "C) Azot ($N_2$)",
                "D) Helyum ($He$)",
                "E) Saf Oksijen ($O_2$)"
            ],
            "correctAnswer": "C",
            "explanation": "Dekompresyon hastalığında Henry kanunu uyarınca yüksek basınçta kanda çözünmüş olan Azot (N2) gazı, ani basınç düşüşünde çözünürlüğünü kaybederek kanda mikro ve makro kabarcıklar halinde gaz embolisi oluşturur."
        }
    },

    # SLIDE 9
    {
        "id": "slide-9",
        "title": "Amniyon Sıvı Embolisi: Fetal Hücreler, Şok ve DİK",
        "subtitle": "Doğum sırasında maternal dolaşıma fetal döküntülerin geçişi ve immün-anafilaktoid şok",
        "content": """**AMNİYON SIVISI EMBOLİSİ (AMNIOTIC FLUID EMBOLISM - AFE)**
Gebelikte anne ölümlerinin en korkulan ve mortalitesi en yüksek (>%80) komplikasyonlarından biridir.

1. **Gelişim Mekanizması:**
   - Doğum eylemi sırasında veya hemen doğum sonrasında plasental zarların yırtılması ve uterin venlerin açılmasıyla amniyon sıvısı anne dolaşımına girer.
   - Anne kanına geçen amniyon sıvısında **fetal skuamöz epitel hücreleri (vernix caseosa), lanugo tüyleri, fetal yağ dokusu ve mekonyum** bulunur.

2. **İki Aşamalı Patofizyolojik Yanıt:**
   - **Mekanik Değil, Ağır Biyokimyasal ve İmmün Reaksiyon:**
     - Amniyon sıvısındaki prokoagülan ve vazoaktif maddeler masif pulmoner vazospazmı, sağ kalp yetmezliğini ve anafilaksi benzeri şoku tetikler (**Gebelikte Anafilaktoid Sendrom**).
   - **Yaygın Damar İçi Pıhtılaşma (DİK):**
     - Amniyon sıvısındaki doku faktörü benzeri prokoagülanlar maternal koagülasyon kaskadını kontrolsüz tetikler; hastaların en az %50'sinde masif **DİK ve durdurulamayan uterin atoni kanaması** gelişir.

3. **Morfopatolojik Tanı (Otopside):**
   - Maternal akciğer kapillerlerinde ve pulmoner arteriyollerinde **fetal döküntü skuamları, verniks ve lanugo tüylerinin** gösterilmesiyle kesin tanı konur.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Amniyon Sıvı Embolisi Özeti:**\n  ▫ Mortalite: **>%80** (Anne ölümlerinin en trajik nedeni).\n  ▫ Klinik: Doğum anında **ani dispne, siyanoz, hipotansif şok, koma ve DİK**.\n  ▫ Otopside: Maternal pulmoner damarlarda **fetal skuamöz hücreler ve lanugo kılları** görülür.\n  ▫ Doku faktörü salınımıyla ağır tüketim koagülopatisi (DİK) gelişir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Doğum eylemi sırasında aniden kardiyovasküler şok, dispne ve DİK tablosuna girerek ölen bir kadının akciğer histopatolojisinde maternal pulmoner kapillerlerde ne görülmesi beklenir?* → **Fetal skuamöz epitel hücreleri ve lanugo tüyleri**."
        ],
        "flashcards": [
            {
                "question": "Amniyon sıvısı embolisinde otopside maternal akciğer kapillerlerinde ne saptanır?",
                "answer": "Fetal kaynaklı skuamöz hücreler (skuamlar), verniks parçacıkları ve lanugo kılları saptanır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q9",
            "question": "Zorlu bir vajinal doğum eyleminin hemen ardından aniden şiddetli dispne, siyanoz, derin hipotansif şok ve nöbet geçiren primigravid bir kadında dakikalar içinde yaygın damar içi pıhtılaşma (DİK) ve vajinal masif kanama gelişiyor. Otopside maternal akciğer mikrosirkülasyonunda fetal skuamöz hücreler ve mekonyum debrisleri gösteriliyor. Bu klinik tablonun tanısı aşağıdakilerden hangisidir?",
            "options": [
                "A) Pulmoner tromboembolizm",
                "B) Amniyon sıvısı embolisi",
                "C) Yağ embolisi sendromu",
                "D) Eklampsi krizi",
                "E) Peripartum kardiyomiyopati"
            ],
            "correctAnswer": "B",
            "explanation": "Doğum sırasında aniden gelişen kardiyovasküler kollaps, solunum yetmezliği, DİK ve maternal akciğer damarlarında fetal skuamların görülmesi Amniyon Sıvısı Embolisi'nin klasik tablosudur."
        }
    },

    # SLIDE 10
    {
        "id": "slide-10",
        "title": "Enfarktüs Patofizyolojisi: İskemik Nekrozun Tanımı ve Etiyolojisi",
        "subtitle": "Arteriyel tıkanma veya venöz drenaj yetersizliğine bağlı gelişen doku nekrozu",
        "content": """**ENFARKTÜS TANIMI VE ETİYOLOJİSİ**
Enfarktüs, bir doku veya organın arteriyel kanlanmasının kesilmesi ya da venöz drenajının tıkanması sonucu gelişen lokalize **iskemik doku nekrozu** alanıdır.

1. **Etiyolojik Nedenler:**
   - **Arteriyel Tromboz ve Tromboemboli (%99):** Enfarktüslerin neredeyse tamamı bir arterin trombüs veya emboli ile akut tıkanması sonucu doğar.
   - **Vazospazm:** Koroner arter vazospazmı (Prinzmetal anjina / kokain kullanımı).
   - **Aterom İçi Kanama:** Aterosklerotik plağın içine kanama olarak lümeni aniden kapatması.
   - **Dıştan Bası:** Bir tümörün, fibröz bandın veya fıtık kesesinin damarı sıkıştırması.
   - **Damarsal Torsiyon (Dönme):** Testis veya over torsiyonunda pedikülün kendi etrafında dönerek önce venleri, sonra arterleri boğması.
   - **Damar Duvarının Yırtılması:** Aort diseksiyonu.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Enfarktüs Etiyolojisi:**\n  ▫ En sık neden: ==Arteriyel tromboz ve tromboemboli (%99)==.\n  ▫ Venöz kökenli enfarktüsler nadirdir; sadece drenajın tek bir vene bağlı olduğu organlarda (testis torsiyonu, over torsiyonu, superior mezenterik ven trombozu) görülür.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite Sorusu:**\n  ▫ *Enfarktüs gelişimine yol açan en yaygın patolojik mekanizma hangisidir?* → **Arteriyel lümenin tromboz veya emboli ile akut oklüzyonu**."
        ],
        "flashcards": [
            {
                "question": "Enfarktüs nedir ve en sık hangi vasküler hadiseye bağlı gelişir?",
                "answer": "Arteriyel beslenmenin veya venöz drenajın kesilmesine bağlı gelişen iskemik doku nekrozudur; %99 arteriyel tromboz veya emboliye bağlıdır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q10",
            "question": "Bir doku veya organda iskemik nekroz (enfarktüs) gelişimine yol açan etiyolojik mekanizmalar arasında açık ara en sık saptanan patolojik olay aşağıdakilerden hangisidir?",
            "options": [
                "A) Lokal lenfatik drenajın tıkanması",
                "B) Arteriyel damar lümeninin tromboz veya tromboemboli ile akut tıkanması",
                "C) Hipotermi sonucu periferik vazokonstriksiyon",
                "D) Eritrosit membranında ozmotik frajilite artışı",
                "E) Histamin salınımıyla gelişen lokal arteriyel dilatasyon"
            ],
            "correctAnswer": "B",
            "explanation": "Enfarktüs olgularının neredeyse tamamı (>%99) besleyici bir arterin tromboz veya emboli ile akut tıkanmasına sekonder gelişir."
        }
    },

    # SLIDE 11
    {
        "id": "slide-11",
        "title": "Beyaz (Soluk / Anemik) Enfarktüs: Solid Organlar ve Uç Arterler",
        "subtitle": "Kalp, dalak ve böbrekte uç arter tıkanıklığı ile gelişen koagülasyon nekrozu",
        "content": """**BEYAZ (SOLUK / ANEMİK) ENFARKTÜSLER**
Enfarktüsler renklerine ve içerdikleri kan miktarına göre beyaz (soluk) ve kırmızı (hemorajik) olmak üzere ikiye ayrılır.

1. **Beyaz Enfarktüsün Gelişme Koşulları:**
   - **Solid (Yoğun) Parankimli Organlar:** Kalp, böbrek, dalak.
   - **Uç Arter (Son Arter / End-Artery) Dolaşımı:** Kollateral kan desteği bulunmayan veya minimal olan damar mimarisi.
   - **Tek Girişli Arteriyel Beslenme.**

2. **Neden Beyaz (Soluk) Görünür?**
   - Tıkanan arter nedeniyle doku aniden kansız kalır.
   - Solid parankimin sert ve yoğun yapısı, komşu komşu kapillerlerden nekroz alanına eritrositlerin sızmasını sınırlar.
   - İlk saatlerde hafif hemorajik olsa da, 24-48 saat içinde nekroze olan hücreler şişer, komşu damarları ezer ve eritrositler lizise uğrar; nekroz alanı tebeşir gibi **soluk, sarı-beyaz** bir renge bürünür.
   - Etrafında hiperemi ve enflamasyon nedeniyle **kırmızı bir sınır kuşağı** bulunur.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Beyaz Enfarktüs Organları:**\n  ▫ ==Kalp (Miyokard), Böbrek, Dalak==.\n  ▫ Koşullar: **Solid organ + Uç arter (End-artery)**.\n  ▫ Histopatoloji: Beyin hariç tüm solid organlarda **Koagülasyon Nekrozu** görülür (hücre hatları haftalarca hayalet hücreler şeklinde korunur).",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Aşağıdaki organların hangisinde arteriyel tıkanma sonrası tipik olarak 'beyaz (soluk/anemik) enfarktüs' gelişmesi beklenir?* → **Dalak, Böbrek veya Kalp** (Akciğer ve bağırsakta kırmızı enfarktüs olur!)."
        ],
        "flashcards": [
            {
                "question": "Beyaz (soluk) enfarktüs hangi tip organlarda görülür ve klasik örnekleri nelerdir?",
                "answer": "Uç arter dolaşımına sahip solid organlarda görülür; klasik örnekleri kalp, böbrek ve dalaktır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q11",
            "question": "Sol ventrikül mural trombüsünden kopan bir embolinin dalak arterinin bir dalını tıkaması sonucu dalak dokusunda kama şeklinde sarı-beyaz renkli, tabanı kapsüle oturan bir nekroz alanı (beyaz enfarktüs) gelişiyor. Dalakta enfarktüsün beyaz (soluk) olmasını sağlayan temel doku özelliği aşağıdakilerden hangisidir?",
            "options": [
                "A) Çift kan dolaşımına ve zengin venöz kollaterallere sahip olması",
                "B) Organın solid parankimli olması ve uç arter (end-artery) dolaşımına sahip olması",
                "C) Parankimin aşırı gevşek ve süngerimsi bağ dokusundan oluşması",
                "D) Enfarktüsün venöz drenaj bozukluğu zemininde gelişmesi",
                "E) Doku içine yoğun reperfüzyon kanaması olması"
            ],
            "correctAnswer": "B",
            "explanation": "Dalak, böbrek ve kalp gibi solid organlarda uç arter dolaşımı vardır; kollateral akım olmadığı ve parankim yoğun olduğu için kanama sızamaz ve soluk (beyaz) enfarktüs gelişir."
        }
    },

    # SLIDE 12
    {
        "id": "slide-12",
        "title": "Kırmızı (Hemorajik) Enfarktüs: Çift Dolaşımlı ve Gevşek Dokular",
        "subtitle": "Akciğer, ince bağırsak, venöz tıkanıklıklar ve reperfüzyon zemininde kanlı nekroz",
        "content": """**KIRMIZI (HEMORAJİK) ENFARKTÜSLER**
İskemik nekroz alanının içine yoğun miktarda eritrosit ve kan sızmasıyla oluşan koyu kırmızı-mor renkli enfarktüslerdir.

1. **Kırmızı Enfarktüsün Geliştiği 5 Temel Durum:**
   1. **Venöz Tıkanıklıklar:** Dokuya arteriyel kan girişi sürerken venöz çıkış tıkanır; organ kanla göllenir ve nekroze olur (Örn: **Testis torsiyonu, Over torsiyonu**, Superior mezenterik ven trombozu).
   2. **Gevşek ve Süngerimsi Dokular:** **Akciğer** gibi gevşek parankimli organlarda nekroz alanına çevre dokulardan kolayca kan sızar.
   3. **Çift Kan Dolaşımına Sahip Dokular:** **Akciğer** (pulmoner + bronşiyal) ve **İnce Bağırsak** (çift mezenterik arklar). Tıkanmayan diğer arterden nekroze alana kan pompalanır.
   4. **Önceden Konjesyone Olan Dokular:** Yavaş kan akımı olan venöz staz alanları.
   5. **Reperfüzyon Hasarı:** Tıkanmış bir arterin trombolitik (t-PA), anjiyoplasti veya spazmın çözülmesiyle yeniden açılması; hasar görmüş nekrotik kapillerlerden parankime masif kan fışkırır.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Kırmızı Enfarktüsün 5 Kuralı:**\n  ▫ 1. ==Venöz Oklüzyon== (Testis/over torsiyonu)\n  ▫ 2. ==Gevşek doku== (Akciğer)\n  ▫ 3. ==Çift dolaşım== (Akciğer, İnce bağırsak)\n  ▫ 4. ==Önceden konjesyone doku==\n  ▫ 5. ==Reperfüzyon== (t-PA veya anjiyo sonrası kanama).\n  ▫ Akciğer ve ince bağırsak enfarktüsleri **DAİMA KIRMIZIDIR**!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Akut testis torsiyonu olan bir hastada gelişen enfarktüsün tipi ve temel mekanizması nedir?* → **Kırmızı (hemorajik) enfarktüs ve venöz drenajın tıkanması**."
        ],
        "flashcards": [
            {
                "question": "Kırmızı (hemorajik) enfarktüs gelişmesini sağlayan başlıca durumlar nelerdir?",
                "answer": "1) Venöz tıkanıklıklar (torsiyonlar), 2) Gevşek dokular (akciğer), 3) Çift dolaşımlı organlar (akciğer, bağırsak), 4) Reperfüzyon (damarın yeniden açılması)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q12",
            "question": "Şiddetli skrotal ağrı ile başvuran 16 yaşındaki bir erkekte spermatik kordun kendi etrafında dönmesi (testis torsiyonu) sonucu cerrahiye alınıyor. Testisin koyu mor-siyah renkte, aşırı kanlı ve nekroze olduğu saptanıyor. Testiste gelişen bu enfarktüsün kırmızı (hemorajik) olmasının primer patogenetik nedeni aşağıdakilerden hangisidir?",
            "options": [
                "A) Uç arter oklüzyonu sonucu hiç kan girmemesi",
                "B) Venöz drenajın tıkanması sonucu arteriyel kanın dokuda göllenmesi ve kanamalı nekroz",
                "C) Testis parankiminin aşırı sert ve solid olması",
                "D) Siyanür intoksikasyonu gelişmesi",
                "E) Doku plazminojen aktivatörünün (t-PA) aşırı salınması"
            ],
            "correctAnswer": "B",
            "explanation": "Testis torsiyonunda ince duvarlı venöz damarlar ilk tıkanır; arteriyel kan dokuya girmeye devam eder ancak çıkamadığı için masif venöz konjesyon, rüptür ve kırmızı (hemorajik) enfarktüs gelişir."
        }
    },

    # SLIDE 13
    {
        "id": "slide-13",
        "title": "Enfarktüsün Morfolojisi: Kama Şekli ve Nekroz Tipleri",
        "subtitle": "Kama morfolojisi, koagülasyon nekrozu ve santral sinir sisteminin likefaksiyon istisnası",
        "content": """**ENFARKTÜSÜN MAKRO VE MİKROSKOBİK MORFOLOJİSİ**

1. **Makroskobik Morfoloji (Kama / Wedge-Shaped Görünüm):**
   - Solid organ enfarktüsleri (dalak, böbrek, akciğer) tipik olarak **kama (üçgen)** şeklindedir:
     - **Tepesi (Apex):** Tıkanan arterin bulunduğu vasküler çatala bakar.
     - **Tabanı (Base):** Organın dış yüzeyine / serozasına (örneğin böbrek veya dalak kapsülüne, akciğer plevrasına) oturur.
   - Serozaya komşu taban üzerinde fibröz eksüda birikir (**Fibrinöz Plevrit veya Perisplenit**); bu durum hastada nefes alıp vermekle batan plöretik göğüs/yan ağrısına yol açar!

2. **Mikroskobik Morfoloji (Nekroz Tipleri):**
   - **Tüm Vücut Organları (Kalp, Böbrek, Dalak vb.):** İskemik hasar tipik olarak **Koagülasyon Nekrozu** ile sonuçlanır. Hücre proteinleri denatüre olur, hücre sınırları ve mimarisi korunur ancak çekirdekler kaybolur (**Hayalet / Ghost Hücreler**).
   - **Santral Sinir Sistemi (BEYİN İSTİSNASI):** Beyin parankiminde iskemik nekroz koagülasyon nekrozu değil, zengin lipit ve hidrolitik enzim içeriği nedeniyle **Likefaksiyon (Sıvılaşma / Kollikuasyon) Nekrozu** ile sonlanır! Doku yumuşar, erir ve kistik bir kavitasyon bırakır.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Enfarktüs Morfolojisi ve Beyin Kuralı:**\n  ▫ Makroskopi: ==Kama şeklinde== (Tepe damara, taban serozaya/kapsüle bakar).\n  ▫ Vücuttaki tüm solid organ enfarktüsleri: ==Koagülasyon Nekrozu== (Hayalet hücreler).\n  ▫ **BEYİN ENFARKTÜSÜ İSTİSNASI:** Kesinlikle ==Likefaksiyon (Sıvılaşma) Nekrozu== gelişir!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Soruları:**\n  ▫ *Serebral arter oklüzyonu sonucu beyin dokusunda gelişen iskemik enfarktüsün histopatolojik nekroz tipi nedir?* → **Likefaksiyon (sıvılaşma) nekrozu**."
        ],
        "flashcards": [
            {
                "question": "Enfarktüs makroskobik olarak ne şekildedir ve beyin dokusunda hangi nekroz tipi gelişir?",
                "answer": "Kama (üçgen) şeklindedir (tabanı kapsüle bakar); diğer organlarda koagülasyon nekrozu görülürken beyinde Likefaksiyon (sıvılaşma) nekrozu gelişir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q13",
            "question": "Sol orta serebral arter (MCA) tıkanıklığı sonucu inme geçiren ve aylar sonra vefat eden bir hastanın beyin otopsisinde lezyon bölgesinde kistik bir boşluk saptanıyor. Beyin enfarktüslerinde koagülasyon nekrozu yerine görülen bu spesifik nekroz tipi aşağıdakilerden hangisidir?",
            "options": [
                "A) Kazeifikasyon nekrozu",
                "B) Yağ nekrozu",
                "C) Likefaksiyon (sıvılaşma / kollikuasyon) nekrozu",
                "D) Fibrinoid nekroz",
                "E) Gangrenöz nekroz"
            ],
            "correctAnswer": "C",
            "explanation": "Santral sinir sisteminde (beyin ve omurilik) iskemik hasar, zengin lipit içeriği ve otolitik enzimler nedeniyle koagülasyon nekrozu değil, likefaksiyon (sıvılaşma) nekrozu ile sonuçlanır."
        }
    },

    # SLIDE 14
    {
        "id": "slide-14",
        "title": "İskemi ve Enfarktüs Gelişimini Etkileyen Dört Kritik Faktör",
        "subtitle": "Kollateral dolaşım, oklüzyon hızı, dokunun hipoksiye duyarlılığı ve kan oksijen içeriği",
        "content": """**ENFARKTÜSÜ BELİRLEYEN 4 FAKTÖR**
Bir damar tıkandığında her zaman enfarktüs gelişmez; tablonun ciddiyetini 4 temel parametre belirler:

1. **Vasküler Yatağın Anatomisi (Kollateral Dolaşım):**
   - Çift dolaşımlı organlar (karaciğer: hepatik arter + portal ven; akciğer: pulmoner + bronşiyal) veya zengin anastomozlu organlar (el palmar arkı, bağırsak arkadları) enfarktüse karşı dirençlidir.
   - Uç artere sahip organlar (böbrek ve dalak) tıkanmada anında nekroza gider.

2. **Oklüzyonun Gelişme Hızı:**
   - Yavaş gelişen darlıklar (kronik ateroskleroz) yeni alternatif damar yollarının (**kollateral / anjiyogenez**) açılması için zaman kazandırır; tam tıkanma olsa bile enfarktüs gelişmeyebilir.
   - Ani tromboembolik tıkanmalar kollateral gelişmesine fırsat vermez; masif nekroz yapar.

3. **Dokunun Hipoksiye Hassasiyeti (İskemik Dayanıklılık):**
   - **Nöronlar:** İskemiye en hassas hücrelerdir; **3-4 dakikalık** iskemi geri dönüşümsüz ölüm yapar.
   - **Miyositler (Kalp Kası):** **20-30 dakika** dayanabilir; ardından nekroz başlar.
   - **Fibroblastlar ve İskelet Kası:** Saatlerce canlı kalabilir.

4. **Kandaki Oksijen İçeriği:**
   - Şiddetli anemi, hipoksi veya karbonmonoksit zehirlenmesi olan bir hastada kısmi bir arter darlığı bile hızla enfarktüsü tetikler.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **İskemiye Hücresel Dayanıklılık Sıralaması:**\n  ▫ 1. En Duyarlı: ==Nöronlar (3-4 dakika)==.\n  ▫ 2. İkinci Duyarlı: ==Miyokard hücreleri (20-30 dakika)==.\n  ▫ 3. En Dirençli: ==Fibroblastlar ve ekstrasellüler matriks (saatler)==.\n  ▫ Yavaş gelişen darlık kollateral damar gelişimini uyararak enfarktüsü engeller.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Sorusu:**\n  ▫ *Akut iskemide geri dönüşümsüz hücresel hasara en erken uğrayan (iskemiye en duyarlı) parankimal hücre hangisidir?* → **Santral sinir sistemi nöronları (3-4 dakika)**."
        ],
        "flashcards": [
            {
                "question": "İskemiye en duyarlı hücre tipi hangisidir ve ne kadar sürede geri dönüşümsüz ölür?",
                "answer": "Santral sinir sistemi nöronlarıdır; 3-4 dakikalık iskemi sonrası geri dönüşümsüz hücre ölümü başlar."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q14",
            "question": "Ani ve tam bir arteriyel tıkanma durumunda hücresel düzeyde geri dönüşümsüz iskemik hasarın ve nekrozun en erken (en kısa sürede) başladığı doku/hücre grubu aşağıdakilerden hangisidir?",
            "options": [
                "A) İskelet kası lifleri",
                "B) Beyin korteks nöronları (3-4 dakika)",
                "C) Miyokard kas lifleri (20-30 dakika)",
                "D) Cilt fibroblastları",
                "E) Renal tübül epitel hücreleri"
            ],
            "correctAnswer": "B",
            "explanation": "Beyin nöronları iskemiye vücuttaki en duyarlı hücrelerdir; kan akımı kesildikten 3-4 dakika sonra geri dönüşümsüz hücre ölümü gerçekleşir."
        }
    },

    # SLIDE 15
    {
        "id": "slide-15",
        "title": "Şok Patofizyolojisi: Sistemik Hipoperfüzyon ve Hücresel Hipoksi",
        "subtitle": "Kardiyak debi veya efektif dolaşan hacmin yetersizliği sonucu hücresel enerji çöküşü",
        "content": """**ŞOKUN TANIMI VE PATOFİZYOLOJİK TEMELİ**
Şok, kardiyak debideki azalma veya efektif dolaşan intravasküler kan hacminin yetersizliği sonucu, tüm vücutta doku perfüzyonunun ve oksijen sunumunun hücresel gereksinimi karşılayamayacak düzeye inmesidir (**Sistemik Hipoperfüzyon**).

1. **Hücresel Düzeyde Ne Olur?**
   - Oksijen yetersizliği → Mitokondriyal oksidatif fosforilasyon durur.
   - Hücre zorunlu olarak **anaerobik glikolize** geçer.
   - Laktik asit birikir → **Laktik Asidoz** gelişir; hücre içi pH düşer.
   - ATP bağımlı $Na^+/K^+$ ATPaz pompası çöker; hücre içine sodyum ve su girer (hücresel şişme).
   - Lisozom enzimleri serbest kalır, membranlar parçalanır ve çoklu organ yetmezliği başlar.

2. **Şokun 5 Ana Kategorisi:**
   1. **Kardiyojenik Şok:** Miyokard pompa yetmezliği.
   2. **Hipovolemik Şok:** Kan veya plazma hacmi kaybı.
   3. **Septik Şok:** Sistemik enfeksiyon, sitokin fırtınası ve vazodilatasyon.
   4. **Nörojenik Şok:** Sempatik tonus kaybı, vazodilatasyon.
   5. **Anafilaktik Şok:** IgE aracılı sistemik vazodilatasyon ve vasküler kaçak.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Şokun Özü:**\n  ▫ Şok bir tansiyon düşüklüğü değil, **hücresel düzeyde oksijen yetersizliği ve metabolik enerji krizidir**.\n  ▫ Ana metabolik belirteç: ==Laktik Asidoz== (Anaerobik glikoliz sonucu kanda laktat birikimi).\n  ▫ Tedavi edilmezse hücresel şişme geri dönüşümsüz doku nekrozuna evrilir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite Sorusu:**\n  ▫ *Şok tablosunda hücresel hipoksinin erken ve karakteristik biyokimyasal sonucu nedir?* → **Anaerobik glikoliz aktivasyonu ve laktik asidoz gelişimi**."
        ],
        "flashcards": [
            {
                "question": "Şok patofizyolojisinde hücresel düzeyde gelişen primer metabolik kriz nedir?",
                "answer": "Oksidatif fosforilasyonun durması, anaerobik glikolize geçiş ve laktik asidoz sonucu ATP tükenmesidir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q15",
            "question": "Şok tablosunun hücresel ve metabolik patofizyolojisi incelendiğinde, doku hipoperfüzyonuna yanıt olarak hücrede mitokondriyal solunumun durmasıyla tetiklenen ve kanda biriken temel biyokimyasal belirteç aşağıdakilerden hangisidir?",
            "options": [
                "A) Piruvat kinaz eksikliği",
                "B) Laktik asit (Laktik asidoz)",
                "C) Serbest yağ asitleri düşüşü",
                "D) Üre sentezinde masif artış",
                "E) Glukoz-6-fosfataz birikimi"
            ],
            "correctAnswer": "B",
            "explanation": "Hipoperfüzyon nedeniyle oksijensiz kalan hücreler anaerobik glikolize geçer; piruvat laktata dönüştürülür ve kanda laktik asit birikerek metabolik laktik asidoz oluşturur."
        }
    },

    # SLIDE 16
    {
        "id": "slide-16",
        "title": "Kardiyojenik Şok: Miyokardiyal Pompa Yetersizliği",
        "subtitle": "Geniş enfarktüsler, ventriküler aritmiler ve mekanik kardiyak yetmezlikler",
        "content": """**KARDİYOJENİK ŞOK PATOFİZYOLOJİSİ**
Miyokard hasarı sonucu kalbin periferik dokuların metabolik ihtiyacını karşılayacak kanı pompalayamaması (akut kardiyak debi çöküşü) tablosudur.

1. **Etiyolojik Nedenler:**
   - **Geniş Miyokard Enfarktüsü:** Sol ventrikül kas kitlesinin **>%40'ının enfarktüse uğraması** durumunda kardiyojenik şok kaçınılmazdır (en sık neden!).
   - **Ventriküler Aritmiler:** Ventriküler taşikardi / fibrilasyon.
   - **Mekanik Komplikasyonlar:** Papiller adale rüptürü (akut masif mitral yetmezlik), ventriküler septal rüptür (VSD), sol ventrikül serbest duvar rüptürü (akut kardiyak tamponad).
   - Ağır miyokardit veya kardiyomiyopati.

2. **Klinik ve Hemodinamik Özellikler:**
   - **Kardiyak Debi (CO):** Belirgin olarak DÜŞMÜŞTÜR.
   - **Sistemik Vasküler Direnç (SVR):** Kompansatuar vazokonstriksiyon nedeniyle ARTMIŞTIR (soluk, soğuk, nemli cilt!).
   - **Pulmoner Kılcal Uç Basıncı (PCWP):** Sol ventrikül boşalamadığı için sol atriyum ve pulmoner venlerde kan göllenir; PCWP **YÜKSEKTİR** (Akut Pulmoner Ödem tablosu eşlik eder).""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Kardiyojenik Şok Hemodinamiği:**\n  ▫ Etyoloji: Sol ventrikül kitlesinin **>%40 enfarktüsü**.\n  ▫ Kardiyak Debi: ↓↓↓ Düşük.\n  ▫ Cilt: **Soğuk, soluk, nemli** (Kompansatuar vazokonstriksiyon).\n  ▫ Akciğer: **Pulmoner ödem ve raller** (PCWP yüksek).\n  ▫ Hipovolemik şoktan farkı: Kardiyojenik şokta juguler venöz dolgunluk ve pulmoner ödem vardır!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Akut miyokard enfarktüsü geçiren bir hastada kardiyojenik şok gelişmesi için sol ventrikül miyokard kitlesinin en az yüzde kaçının fonksiyon dışı kalması gerekir?* → **En az %40**."
        ],
        "flashcards": [
            {
                "question": "Kardiyojenik şokta kardiyak debi, periferik direnç ve cilt bulguları nasıldır?",
                "answer": "Kardiyak debi düşüktür; periferik vasküler direnç kompanse etmek için artmıştır; cilt soğuk, soluk ve terli (nemli) görünümdedir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q16",
            "question": "Akut anterior miyokard enfarktüsü tanısıyla koroner yoğun bakımda izlenen 65 yaşındaki hastada kan basıncı 75/40 mmHg'ye geriliyor, taşikardi, dispne, akciğer bazallerinde yaygın yaş raller ve boyun venöz dolgunluğu gelişiyor; ekstremiteleri soğuk ve nemli bulunuyor. Bu hastada kardiyojenik şok tanısını destekleyen temel hemodinamik bulgular aşağıdakilerden hangisinde doğru verilmiştir?",
            "options": [
                "A) Kardiyak debi artmış, periferik vasküler direnç düşmüş",
                "B) Kardiyak debi düşmüş, pulmoner kapiller uç basıncı (PCWP) yükselmiş ve periferik direnç artmış",
                "C) Kardiyak debi normal, venöz doluş sıfırlanmış",
                "D) Pulmoner kapiller uç basıncı düşmüş, cilt sıcak ve pembe",
                "E) Sistemik vasküler direnç sıfıra inmiş"
            ],
            "correctAnswer": "B",
            "explanation": "Kardiyojenik şokta sol ventrikül pompa yetmezliği nedeniyle kardiyak debi düşer; geride kan göllendiği için PCWP artar (akciğer ödemi); vücut tansiyonu korumak için vazokonstriksiyon yapar (SVR artar, cilt soğuk-nemli)."
        }
    },

    # SLIDE 17
    {
        "id": "slide-17",
        "title": "Hipovolemik Şok: İntravasküler Hacim Kaybı ve Kompansasyon",
        "subtitle": "Hemoraji, yanıklar, aşırı sıvı kayıpları ve sempatik-RAAS savunma mekanizmaları",
        "content": """**HİPOVOLEMİK ŞOK MEKANİZMASI**
Dolaşımdaki kan veya plazma hacminin akut kaybı sonucu ventrikül doluşunun (preload) çökmesiyle gelişir.

1. **Etiyolojik Nedenler:**
   - **Hemorajik Şok:** Masif iç veya dış kanamalar (rüptüre aort anevrizması, travma, ektopik gebelik rüptürü, gastrointestinal kanamalar).
   - **Plazma ve Sıvı Kayıpları:** Geniş yanıklar (plazma kaybı), şiddetli kusma/ishal (kolera, gastroenterit), diyabetik ketoasidoz (ozmotik diürez).

2. **Kompansasyon Mekanizmaları:**
   - Karotid sinüs ve aortik baroreseptörler uyarılır → **Yoğun sempatik deşarj**:
     - Taşikardi (nabız hızlanır).
     - Periferik vazokonstriksiyon (deri, kas ve böbrek damarları büzülür; kan beyin ve kalbe yönlendirilir).
   - **RAAS (Renin-Anjiyotensin-Aldosteron) Aktivasyonu:** Renal perfüzyon düşer; renin salınır, anjiyotensin II damarları kasar, aldosteron sodyum ve su tutar.
   - **ADH (Vazopressin) Salınımı:** İdrar miktarı azalır (**oligüri/anüri**).

3. **Hemodinami:**
   - Kardiyak debi düşüktür; venöz doluş basınçları (CVP ve PCWP) **DÜŞÜKTÜR**; periferik direnç artmıştır (cilt soğuk, soluk, kapiller dolum uzamış).""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Hipovolemik Şok Özeti:**\n  ▫ Primer Sorun: ==İntravasküler hacim kaybı==.\n  ▫ Cilt: **Soğuk, soluk, terli**.\n  ▫ Boyun venleri: **Düzleşmiş (Kollabe)**; CVP ve PCWP çok düşüktür (kardiyojenik şokun tam tersi!).\n  ▫ İdrar çıkışı: Azalmış (**Oligüri <0.5 mL/kg/saat**) - hipovoleminin en duyarlı göstergesi.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite Sorusu:**\n  ▫ *Akut kanama geçiren bir hastada şok kompanzasyonunda devreye giren ve idrar çıkışını azaltarak hacmi korumaya çalışan temel hormonal aks hangisidir?* → **Renin-Anjiyotensin-Aldosteron Sistemi (RAAS) ve ADH**."
        ],
        "flashcards": [
            {
                "question": "Hipovolemik şokta boyun venleri ve pulmoner uç basıncı (PCWP) kardiyojenik şoktan nasıl ayrılır?",
                "answer": "Kardiyojenik şokta venler dolgun ve PCWP yüksektir; hipovolemik şokta ise intravasküler hacim azaldığı için boyun venleri düzleşmiştir ve PCWP düşüktür."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q17",
            "question": "Trafik kazası sonrası dalak rüptürü nedeniyle masif intraabdominal kanaması olan 28 yaşındaki bir hastada gelişen hipovolemik şok tablosunda aşağıdakilerden hangisinin görülmesi beklenmez?",
            "options": [
                "A) Taşikardi ve hipotansiyon",
                "B) Cildin soğuk, soluk ve nemli olması",
                "C) İdrar çıkışında belirgin azalma (oligüri)",
                "D) Boyun venöz dolgunluğu ve bilateral yaygın akciğer ödemi",
                "E) Santral venöz basıncın (CVP) belirgin düşmesi"
            ],
            "correctAnswer": "D",
            "explanation": "Boyun venöz dolgunluğu ve akciğer ödemi volüm yüklenmesi veya kardiyojenik şokta görülür; hipovolemik şokta intravasküler hacim boşaldığı için boyun venleri kollabedir ve akciğerler temizdir."
        }
    },

    # SLIDE 18
    {
        "id": "slide-18",
        "title": "Septik Şok 1: PAMP'lar, Toll-Like Reseptörler ve Sitokin Fırtınası",
        "subtitle": "Enfeksiyona karşı konağın disregüle immün yanıtı ve moleküler mediyatörler",
        "content": """**SEPTİK ŞOKUN MOLEKÜLER TETİKLEYİCİLERİ**
Septik şok, sistemik bir enfeksiyona karşı konağın verdiği kontrolsüz ve orantısız immün yanıtın yol açtığı, hücresel metabolizma anormallikleri ve derin vazodilatasyonla seyreden hayatı tehdit edici tablodur.

1. **Mikrobiyal Tetikleyiciler (PAMP'lar):**
   - **Gram-Negatif Bakteriler (En Klasik):** Hücre duvarındaki **Lipopolisakkarit (LPS / Endotoksin)**.
   - **Gram-Pozitif Bakteriler (En Sık Neden!):** Peptidoglikanlar ve lipoteikoik asit.
   - Mantarlar ve diğer mikroorganizmalar.

2. **Reseptör Tanıma ve Hücresel Aktivasyon:**
   - Dolaşımdaki LPS, serumdaki LBP (LPS-bağlayıcı protein) ile birleşir.
   - Makrofaj ve monositlerin yüzeyindeki **CD14 ve Toll-Like Reseptör 4 (TLR4)** kompleksine bağlanır.
   - Hücre içi NF-$\kappa$B sinyal yolu aktive olur.

3. **Sitokin Fırtınası (Aşırı İmmün Yanıt):**
   - Masif miktarda primer proenflamatuar sitokin salgılanır:
     - **Tümör Nekrozis Faktör-alfa (TNF-$\alpha$)**
     - **İnterlökin-1 (IL-1)**
     - **İnterlökin-6 (IL-6)**
     - İnterlökin-12 ve IFN-$\gamma$
   - Bu sitokinler ikincil mediyatörleri (lökotrienler, PAF, NO, kompleman) tetikleyerek lokal enflamasyonu kontrolsüz sistemik yangıya çevirir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Septik Şokun Moleküler Aksı:**\n  ▫ Endotoksin: ==LPS (Lipopolisakkarit)==.\n  ▫ Reseptör Kompleksi: ==CD14 + TLR4 (Toll-like reseptör 4)==.\n  ▫ Anahtar Sitokinler: ==TNF-$\alpha$ ve IL-1==.\n  ▫ Gram-pozitif bakteriler günümüzde sıklık olarak gram-negatiflerin önüne geçmiştir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Soruları:**\n  ▫ *Gram-negatif bakteri septik şokunda endotoksin (LPS) makrofaj yüzeyindeki hangi reseptör kompleksi tarafından tanınır?* → **TLR4 (Toll-Like Reseptör 4) ve CD14**."
        ],
        "flashcards": [
            {
                "question": "Septik şokta gram-negatif endotoksin (LPS) makrofajlarda hangi reseptörle tanınır ve hangi ana sitokinleri salgılatır?",
                "answer": "TLR4 (Toll-like reseptör 4) ve CD14 kompleksiyle tanınır; primer olarak TNF-alfa ve IL-1 salınımını tetikler."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q18",
            "question": "Gram-negatif sepsis ve septik şok patofizyolojisinde, bakteriyel hücre duvarı lipopolisakkaritinin (LPS / endotoksin) immün sistem hücreleri tarafından tanınarak masif TNF-alfa ve IL-1 salınımını başlatan temel hücresel reseptör kompleksi aşağıdakilerden hangisidir?",
            "options": [
                "A) Mannoz reseptörü",
                "B) Toll-Like Reseptör 4 (TLR4) ve CD14",
                "C) CD40 ve CD40L",
                "D) İntegrin alfa-4 beta-1",
                "E) T hücre reseptörü (TCR)"
            ],
            "correctAnswer": "B",
            "explanation": "LPS molekülü, monosit ve makrofaj yüzeyindeki CD14 kofaktörü aracılığıyla TLR4 (Toll-like receptor 4) reseptörüne bağlanarak sitokin fırtınasını tetikler."
        }
    },

    # SLIDE 19
    {
        "id": "slide-19",
        "title": "Septik Şok 2: Sistemik Endotel Hasarı, Vazodilatasyon ve DİK",
        "subtitle": "İndüklenebilir NO sentaz (iNOS), kapiller kaçak, mikrotrombüsler ve metabolik çöküş",
        "content": """**SEPTİK ŞOKTA VASKÜLER VE METABOLİK ANORMALLİKLER**
Sitokin fırtınası endotel hücreleri üzerinde yıkıcı sistemik etkiler yaratır:

1. **Sistemik Vazodilatasyon ve Sıcak Şok:**
   - Sitokinler damar düz kaslarında **İndüklenebilir Nitrik Oksit Sentazı (iNOS)** aşırı uyarır.
   - Yüksek miktarda **Nitrik Oksit (NO)** sentezlenir.
   - Tüm periferik arteriyoller aşırı genişler (vazodilatasyon); sistemik vasküler direnç (SVR) çöker.
   - Kan deride göllenir; bu nedenle erken dönemde diğer şokların aksine **cilt sıcak, pembe ve kurudur ('Sıcak Şok' / Warm Shock)**!

2. **Yaygın Endotel Hasarı ve Vasküler Kaçak:**
   - Endotel bağlantıları gevşer; plazma ve albümin interstisyuma sızar (**üçüncü boşluğa kaçış**). Masif anazarka ödemi ve hipovolemi gelişir.

3. **Dissemine İntravasküler Koagülasyon (DİK):**
   - Sitokinler endotelde Doku Faktörü sentezini artırır; trombomodulin ve protein C'yi baskılar.
   - Tüm mikrosirkülasyonda yaygın fibrin-trombosit mikrotrombüsleri oluşur. Dokular iskemik nekroza uğrarken kanda trombosit ve faktörler tükenir (tüketim koagülopatisi ve yaygın kanamalar).

4. **İmmünsüpresyon ve Metabolik Anormallikler:**
   - Hiperglisemi (glukoneogenez ve insülin direnci), ardından adrenal yetmezlik ve laktik asidoz.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Septik Şokun Belirteçleri:**\n  ▫ Aşırı Vazodilatasyon: ==iNOS aktivasyonu ve Nitrik Oksit (NO)==.\n  ▫ Erken Klinik: Cilt **sıcak ve pembedir (Sıcak Şok)**; ilerledikçe soğuk şoka döner.\n  ▫ Koagülasyon: Doku faktörü patlamasıyla **DİK (Dissemine İntravasküler Koagülasyon)** gelişir.\n  ▫ Sıvı Kaybı: Yaygın endotel hasarıyla **vasküler kaçak ve masif ödem**.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Septik şokta sistemik vazodilatasyondan ve periferik vasküler direncin çökmesinden sorumlu olan temel endotelyal gevşetici molekül nedir?* → **Nitrik Oksit (NO) - iNOS aktivasyonu**."
        ],
        "flashcards": [
            {
                "question": "Septik şokun erken döneminde cildin soğuk değil de sıcak/pembe olmasının nedeni nedir?",
                "answer": "iNOS kaynaklı aşırı Nitrik Oksit (NO) üretimine bağlı sistemik vazodilatasyon ve deride kan göllenmesidir (Sıcak Şok)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q19",
            "question": "Ürosepsis zemininde yoğun bakımda takip edilen bir hastada hipotansiyon olmasına rağmen ekstremitelerin sıcak ve pembe olduğu saptanıyor. Septik şokun bu erken evresinde periferik vazodilatasyona yol açarak sistemik vasküler direncin düşmesine neden olan temel mediyatör aşağıdakilerden hangisidir?",
            "options": [
                "A) Endotelin-1",
                "B) Nitrik Oksit (NO)",
                "C) Tromboksan A2",
                "D) Anjiyotensin II",
                "E) Lökotrien C4"
            ],
            "correctAnswer": "B",
            "explanation": "Septik şokta proenflamatuar sitokinler endotel ve damar düz kasında iNOS enzimini uyararak yüksek miktarda Nitrik Oksit (NO) sentezletir; NO güçlü vazodilatasyon yaparak erken dönemde 'sıcak şok' tablosuna yol açar."
        }
    },

    # SLIDE 20
    {
        "id": "slide-20",
        "title": "Özel Şok Tipleri: Nörojenik Şok ve Anafilaktik Şok",
        "subtitle": "Sempatik tonus kaybı ve IgE aracılı yaygın vazodilatasyon dinamikleri",
        "content": """**NÖROJENİK VE ANAFİLAKTİK ŞOK**

1. **Nörojenik Şok:**
   - **Tetikleyici:** Yüksek spinal kord yaralanmaları (servikal/üst torakal kord transeksiyonu), spinal anestezi komplikasyonu veya şiddetli beyin travması.
   - **Mekanizma:** Sempatik vazomotor tonus aniden kesilir.
   - **Sonuç:** Vasküler yataktaki arter ve venler tamamen gevşer. Kan periferik venöz göllere toplanır; kalbe venöz dönüş sıfırlanır.
   - **Karakteristik Klinik İpucu (Paradoks):** Diğer şok tiplerinde kompanzatuar taşikardi görülürken, nörojenik şokta sempatik uyarı yokluğu ve vagal baskınlık nedeniyle **HİPOTANSİYON + BRADİKARDİ** birlikteliği görülür! Cilt sıcak ve kurudur.

2. **Anafilaktik Şok:**
   - **Tetikleyici:** Tip I aşırı duyarlılık reaksiyonu (böcek sokması, penisilin, fıstık, lateks vb.).
   - **Mekanizma:** Antijen duyarlı bireyde mast hücreleri ve bazofillerin yüzeyindeki **IgE moleküllerini** çapraz bağlar.
   - **Salınan Mediyatörler:** Masif **Histamin**, lökotrienler ve PAF salınımı.
   - **Sonuç:**
     - Sistemik yaygın vazodilatasyon (derin hipotansiyon).
     - Ani kapiller geçirgenlik artışı (ödem, laringeal spazm/stridor, boğulma).
     - Bronkospazm (şiddetli astım benzeri dispne).
   - **Acil Tedavi:** İntramüsküler **Adrenalin (Epinefrin)**.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Ayırıcı Tanı Özeti:**\n  ▫ ==Nörojenik Şok:== Sempatik felç → **Hipotansiyon + BRADİKARDİ** (Taşikardi OLMAZ!).\n  ▫ ==Anafilaktik Şok:== IgE + Histamin → Yaygın vazodilatasyon, **bronkospazm, laringeal ödem**.\n  ▫ Anafilaktik şokta hayat kurtarıcı ilk ilaç: **İntramüsküler Adrenalin**.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Spinal kord travması sonrası hipotansiyon gelişen bir hastada diğer şok tiplerinden farklı olarak bradikardi görülmesi hangi şok tipini işaret eder?* → **Nörojenik Şok**."
        ],
        "flashcards": [
            {
                "question": "Nörojenik şoku diğer hipovolemik veya kardiyojenik şoklardan ayıran tipik nabız bulgusu nedir?",
                "answer": "Sempatik tonus kaybına bağlı olarak taşikardi yerine Bradikardi (yavaş nabız) görülmesidir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q20",
            "question": "Trafik kazasında C5 vertebra kırığı ve spinal kord kesisi saptanan 24 yaşındaki bir hastada kan basıncı 70/40 mmHg olarak ölçülüyor. Fizik muayenede taşikardi yerine nabzın 48/dakika (bradikardi) olduğu ve cildin sıcak-kuru olduğu tespit ediliyor. Bu klinik tablo aşağıdaki şok tiplerinden hangisine özgüdür?",
            "options": [
                "A) Hipovolemik şok",
                "B) Kardiyojenik şok",
                "C) Nörojenik şok",
                "D) Obstrüktif şok",
                "E) Septik şok"
            ],
            "correctAnswer": "C",
            "explanation": "Spinal kord hasarında sempatik vazomotor uyarının kesilmesiyle gelişen nörojenik şokta, taşikardi yanıtı oluşamaz; hipotansiyon ile birlikte paradoksal bradikardi ve sıcak-kuru cilt görülür."
        }
    },

    # SLIDE 21
    {
        "id": "slide-21",
        "title": "Şokun Üç Evresi: Kompanse, Progresif ve İrreversibl",
        "subtitle": "Kompansatuar nörohümoral yanıttan geri dönüşümsüz hücresel otolize giden süreç",
        "content": """**ŞOKUN KLİNİK VE PATOLOJİK EVRELERİ**
Altta yatan neden ne olursa olsun, şok tablosu kontrol altına alınmazsa 3 kronolojik evreden geçer:

1. **Evre 1: Nonprogresif (Kompanse) Evre:**
   - Refleks kompansasyon mekanizmaları tam kapasite devrededir.
   - Baroreseptör refleksleri, katekolamin salınımı, RAAS aktivasyonu, ADH artışı ve sempatik vazokonstriksiyon.
   - Kan yaşamsal organlara (beyin ve koronerler) yönlendirilir; periferik vazokonstriksiyon sayesinde **kan basıncı korunur**.
   - Hasta taşikardik, hafif soluk ve oligüriktir; bu evrede uygun sıvı/tedavi ile **tamamen geri döndürülebilir**!

2. **Evre 2: Progresif Evre (Doku Hipoperfüzyonu):**
   - Kompansasyon mekanizmaları yetersiz kalır.
   - Dokularda yaygın hipoksi ve anaerobik glikoliz başlar.
   - **Laktik Asidoz:** Düşük pH arteriyollerin vazomotor tonusunu felç eder; damarlar genişler ve kan mikrosirkülasyonda göllenir.
   - Endotel hasarı başlar; vital organ fonksiyonları bozulur, idrar miktarı kritik derecede düşer.

3. **Evre 3: İrreversibl (Geri Dönüşümsüz) Evre:**
   - Hücresel hasar öyle bir boyuta ulaşır ki hemodinamik parametreler (tansiyon, nabız) düzeltilse bile hasta kurtarılamaz.
   - Mitokondriler şişer, lizozomal asit hidrolazlar sitoplazmaya sızar.
   - Miyokardiyal depresan faktörler kalbi durdurur; bağırsak bariyeri çöker ve kana bakteriyel endotoksinler karışır.
   - Böbreklerde tam anüri, karaciğer ve akciğer yetmezliği (**MODS**) ve **Ölüm**.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Şok Evrelerinin Ayrımı:**\n  ▫ ==1. Nonprogresif (Kompanse):== Refleksler aktiftir, tansiyon korunur, tamamen kür sağlanabilir.\n  ▫ ==2. Progresif:== Laktik asidoz gelişir, damar tonusu çöker, perfüzyon bozulur.\n  ▫ ==3. İrreversibl (Geri Dönüşümsüz):== Masif hücre ölümü, lizozom enzim salınımı; tedaviye rağmen ölüm kaçınılmazdır.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Sorusu:**\n  ▫ *Şokun progresif evreden irreversibl evreye geçişinde rol oynayan en temel hücresel patoloji nedir?* → **Yaygın mitokondriyal hasar, lizozomal enzimlerin serbestleşmesi ve hücresel ATP üretiminin kalıcı çöküşü**."
        ],
        "flashcards": [
            {
                "question": "Şokun nonprogresif (kompanse) evresi ile progresif evresi arasındaki temel klinik-patolojik fark nedir?",
                "answer": "Kompanse evrede nörohümoral reflekslerle tansiyon korunur; progresif evrede laktik asidoz ve doku hipoperfüzyonu başlar, tansiyon düşer."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q21",
            "question": "Şok tablosunda olan bir hastada yoğun sıvı resüsitasyonuna ve yüksek doz inotropik/vazopressör ajanlara rağmen kardiyak fonksiyonların giderek çökmesi, tübüler epitelin yaygın nekrozu (anüri), bağırsak florasının kana karışması ve hücresel düzeyde lizozomal enzimlerin sitozole dökülerek otolizi başlatması şokun hangi evresinde olduğunu gösterir?",
            "options": [
                "A) Nonprogresif evre",
                "B) Kompanse erken evre",
                "C) İrreversibl (geri dönüşümsüz) evre",
                "D) İzole kardiyojenik evre",
                "E) Pre-şok dönemi"
            ],
            "correctAnswer": "C",
            "explanation": "Tedaviyle hemodinaminin düzeltilmesine rağmen organ yetmezliklerinin durdurulamadığı, yaygın hücresel nekroz ve lizozomal enzim kaçağının olduğu evre şokun irreversibl (geri dönüşümsüz) evresidir."
        }
    },

    # SLIDE 22
    {
        "id": "slide-22",
        "title": "Şokun Organ Morfolojisi 1: Şok Böbreği (Akut Tübüler Nekroz)",
        "subtitle": "Renal iskemi, tübül epitel nekrozu, silendirler ve oligürik akut böbrek yetmezliği",
        "content": """**ŞOKUN ORGANLARA ETKİSİ: ŞOK BÖBREĞİ (ATN)**
Böbrekler kardiyak debinin yaklaşık %20-25'ini alır; bu nedenle sistemik hipoperfüzyona en hassas organların başında gelir.

1. **İskemik Akut Tübüler Nekroz (ATN):**
   - Şok sırasında gelişen şiddetli ve uzamış renal hipoperfüzyon **İskemik ATN** tablosuna yol açar.
   - En duyarlı yapılar: Metabolik aktivitesi en yüksek olan **Proksimal Kıvrıntılı Tübüller** ve Henle kulpunun kalın çıkan koludur.

2. **Histopatolojik Bulgular:**
   - Proksimal tübül epitel hücrelerinde fırçamsı kenar kaybı, şişme, tübül lümenine dökülme ve yama tarzında fokal nekrozlar.
   - Dökülen epitel hücreleri ve Tamm-Horsfall proteini lümende birleşerek **Granüler Silendirler (Çamur Rengi Silendirler)** oluşturur.
   - Tübüler obstrüksiyon ve geri kaçış glomerüler filtrasyonu sıfırlar.

3. **Klinik Seyir ve Reversibilite:**
   - İdrar miktarı dramatik düşer (**Oligüri <400 mL/gün veya Anüri**).
   - Tübül bazal membranı sağlam kalmışsa ve hasta diyaliz ile yaşatılırsa, tübül epitel hücreleri rejenere olarak haftalar içinde **tam iyileşme** sağlayabilir!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Şok Böbreği (İskemik ATN):**\n  ▫ En Duyarlı Bölge: ==Proksimal Tübüller ve Henle Kalın Çıkan Kolu==.\n  ▫ İdrar İncelemesi: ==Çamur rengi granüler silendirler==.\n  ▫ Glomerüller genellikle sağlamdır; hasar tübüllerde odaklanır.\n  ▫ Tübül bazal membranı sağlamsa epitel prolifere olup kendini yenileyebilir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Şok böbreğinde (iskemik akut tübüler nekroz) hipoksiye en duyarlı tübüler segment hangisidir?* → **Proksimal kıvrıntılı tübül (özellikle düz segmenti P3)**."
        ],
        "flashcards": [
            {
                "question": "Şok böbreğinde (iskemik ATN) iskemik hasara en hassas tübül bölümü hangisidir?",
                "answer": "Proksimal kıvrıntılı tübül epitelidir (yüksek metabolik ve transport aktivitesi nedeniyle)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q22",
            "question": "Ağır hemorajik şok sonrasında oligüri gelişen ve idrar sedimentinde tipik çamur rengi granüler silendirler saptanan bir hastada gelişen iskemik akut tübüler nekrozda (şok böbreği), hipoksik hasara en duyarlı olan nefron segmenti aşağıdakilerden hangisidir?",
            "options": [
                "A) Distal kıvrıntılı tübül",
                "B) Toplayıcı kanallar",
                "C) Proksimal kıvrıntılı tübül epiteli",
                "D) Glomerüler mezangiyal hücreler",
                "E) Henle kulpunun ince inen kolu"
            ],
            "correctAnswer": "C",
            "explanation": "Böbrekte metabolik transport yükü ve oksijen tüketimi en yüksek olan hücreler proksimal tübül epiteli olduğundan iskemik şok hasarına en duyarlı bölgedir."
        }
    },

    # SLIDE 23
    {
        "id": "slide-23",
        "title": "Şok Akciğeri (ARDS) ve Adrenal Bezler (Waterhouse-Friderichsen)",
        "subtitle": "Diffüz alveoler hasar, hyalen membranlar ve meningokoksemik adrenal apopleksi",
        "content": """**ŞOK AKCİĞERİ (ARDS) VE ADRENAL HASAR**

1. **Şok Akciğeri (Diffüz Alveoler Hasar / ARDS):**
   - Özellikle **Septik Şok** ve ağır travmada gelişir; hipovolemik şokta akciğerler genellikle korunur.
   - **Patogenez:** Pulmoner kapiller yatakta aktive olan nötrofiller alveolokapiller membrana yapışır ve proteolitik enzimler ile serbest oksijen radikalleri salar.
   - **Histopatoloji:**
     - Alveol kapiller endotelinde ve Tip I pnömositlerde yaygın nekroz.
     - Alveol lümenlerine protein ve fibrinden zengin eksüda dolar.
     - Dökülen ölü epitel hücreleri ve fibrin birleşerek alveol iç yüzeyini pembe bir bant gibi kaplayan karakteristik **Hyalen Membranları** oluşturur.
     - Akciğerler ağır, kaskatı ve hava içermez hale gelir (Klinik: Ağır refrakter hipoksemi).

2. **Adrenal Bez Hasarı (Waterhouse-Friderichsen Sendromu):**
   - Şokta stres hormonu üretimi için adrenal korteks lipidleri boşalır.
   - **Waterhouse-Friderichsen Sendromu:** Özellikle *Neisseria meningitidis* (Meningokoksemi) sepsisli çocuklarda, masif DİK zemininde her iki sürrenal bezde gelişen **Bilateral Masif Adrenal Hemoraji / Nekroz** tablosudur. Akut adrenal yetmezlik ve saatler içinde ölüm görülür.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Kritik Morfolojik Eşleşmeler:**\n  ▫ ==Şok Akciğeri (ARDS / DAD):== Alveol duvarlarında **pembe Hyalen Membranlar**; en sık septik şokta görülür.\n  ▫ ==Waterhouse-Friderichsen Sendromu:== Meningokoksemide **Bilateral Adrenal Kanama ve Nekroz**.\n  ▫ Karaciğerde şok morfolojisi: Santrilobüler nekroz (Zon 3 nekrozu).\n  ▫ Midede şok morfolojisi: Akut stres erozyonları ve ülserleri (Curling ülseri).",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Soruları:**\n  ▫ *Meningokok sepsisi geçiren çocukta bilateral adrenal bezlerde masif hemoraji ve akut sürrenal yetmezlikle seyreden ölümcül sendrom nedir?* → **Waterhouse-Friderichsen Sendromu**."
        ],
        "flashcards": [
            {
                "question": "Şok akciğerinin (ARDS / Diffüz Alveoler Hasar) histopatolojik belirteci nedir ve en sık hangi şokta görülür?",
                "answer": "Alveol lümenini döşeyen pembe fibrinöz Hyalen Membranlardır; en sık Septik Şokta görülür."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q23",
            "question": "Yüksek ateş, peteşiyal döküntüler ve meningeal irritasyon bulgularıyla acile getirilen 5 yaşındaki çocukta saatler içinde fulminan septik şok gelişiyor ve hasta kaybediliyor. Otopside her iki böbrek üstü bezinin (adrenallerin) tamamen kanamalı nekrozla harap olduğu saptanıyor. Bu klinik ve patolojik antite aşağıdakilerden hangisidir?",
            "options": [
                "A) Cushing sendromu",
                "B) Waterhouse-Friderichsen sendromu",
                "C) Conn sendromu",
                "D) Sheehan sendromu",
                "E) Goodpasture sendromu"
            ],
            "correctAnswer": "B",
            "explanation": "Meningokoksemiye bağlı fulminan sepsiste bilateral sürrenal bezlerin masif hemorajik nekrozu ve akut adrenal yetmezlik gelişmesi Waterhouse-Friderichsen sendromu olarak adlandırılır."
        }
    },

    # SLIDE 24
    {
        "id": "slide-24",
        "title": "Şokun Klinik Seyri, Çoklu Organ Yetmezliği (MODS) ve Mortalite",
        "subtitle": "Klinik yönetim prensipleri, organ hasar sırası ve patoloji-klinik entegrasyonu",
        "content": """**ŞOKUN KLİNİK SEYRİ VE ÇOKLU ORGAN YETMEZLİĞİ (MODS)**
Şok tablosunda mortalite ve prognoz, altta yatan nedene, şokun süresine ve hastanın rezervine doğrudan bağlıdır.

1. **Klinik Bulguların Karşılaştırmalı Özeti:**
   - **Hipovolemik ve Kardiyojenik Şok:** Hipotansiyon, zayıf ve hızlı nabız, takipne, oligüri, **soğuk, soluk, nemli cilt**.
   - **Septik Şok (Erken Evre):** Hipotansiyon, taşikardi, **sıcak, pembe, kuru cilt**.
   - **Nörojenik Şok:** Hipotansiyon, **bradikardi**, sıcak cilt.

2. **Çoklu Organ Yetmezliği Sendromu (MODS):**
   - Sistemik hipoperfüzyon ve sitokin hasarı devam ederse organlar domino taşları gibi sırayla iflas eder:
     1. **Akciğerler (ARDS):** Oksijenizasyon çöker.
     2. **Böbrekler (ATN):** Anüri, üre/kreatinin artışı, hiperkalemi.
     3. **Karaciğer:** Santrilobüler nekroz, sarılık, koagülopati.
     4. **Gastrointestinal Sistem:** Mukoza iskemisi, bakteriyel translokasyon.
     5. **Kalp:** Asidoz ve hiperkalemi ile kardiyak arrest.

3. **Mortalite Oranları:**
   - Gençlerde hipovolemik şok uygun sıvı/kan replasmanı ile **%85-90 yaşatılabilir**.
   - Septik şokta mortalite **%40-60**; kardiyojenik şokta ise **%70-80** seviyesindedir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Klinik Özet:**\n  ▫ Hipovolemik ve Kardiyojenik Şok = **Soğuk Şok** (Periferik vazokonstriksiyon).\n  ▫ Erken Septik Şok ve Nörojenik Şok = **Sıcak Şok** (Periferik vazodilatasyon).\n  ▫ Nörojenik Şokun İmzası = **Bradikardi**.\n  ▫ Tedavide altın kural: İrreversibl evreye girmeden önce erken volüm ve perfüzyon restorasyonudur.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Sorusu:**\n  ▫ *Aşağıdaki şok tiplerinin hangisinde erken dönemde periferik vazodilatasyona bağlı olarak cildin sıcak ve pembe olması beklenir?* → **Septik Şok (Erken 'Sıcak Şok' evresi)**."
        ],
        "flashcards": [
            {
                "question": "Hangi şok tiplerinde cilt soğuk ve soluk, hangilerinde ise erken dönemde sıcak ve pembedir?",
                "answer": "Kardiyojenik ve Hipovolemik şokta cilt soğuk-soluktur; erken Septik şok ve Nörojenik şokta ise sıcak ve pembedir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-infarkt-q24",
            "question": "Farklı şok tiplerinin klinik özellikleri karşılaştırıldığında, erken dönemde periferik vasküler direncin düşmesine bağlı olarak hastanın cildinin sıcak ve pembe olması (sıcak şok) en karakteristik olarak hangi şok tipinde gözlenir?",
            "options": [
                "A) Masif kanamaya bağlı hipovolemik şok",
                "B) Geniş miyokard enfarktüsüne bağlı kardiyojenik şok",
                "C) Gram-negatif bakteriyemiye bağlı erken septik şok",
                "D) Kardiyak tamponada bağlı obstrüktif şok",
                "E) Ağır dehidratasyona bağlı hipovolemik şok"
            ],
            "correctAnswer": "C",
            "explanation": "Erken septik şokta NO salınımına bağlı sistemik vazodilatasyon geliştiğinden diğer şokların aksine cilt sıcak ve pembedir (sıcak şok); hipovolemik ve kardiyojenik şokta ise vazokonstriksiyon nedeniyle cilt soğuk ve soluktur."
        }
    }
]

print(f"Prepared {len(slides)} slides for Ischemia, Infarction and Shock.")


# -------------------------------------------------------------
# ENCYCLOPEDIA & GLOSSARY DATA FOR ISCHEMIA, INFARCT & SHOCK
# -------------------------------------------------------------

encyclopedia_entries = [
    {
        "id": "pulmoner-tromboembolizm-pte",
        "title": "Pulmoner Tromboembolizm (PTE)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Göğüs Hastalıkları",
        "summary": "Venöz dolaşımdan (özellikle alt ekstremite derin venlerinden) kopan trombüslerin sağ kalbi geçerek pulmoner arteriyel yatağı tıkamasıyla karakterize, hipoksemi, akut sağ kalp yetmezliği ve ani ölüme yol açabilen hayatı tehdit edici vasküler acil tablodur.",
        "mechanism": [
            "▸ Pulmoner embolilerin **>%95'i alt ekstremite diz üstü derin ven trombozlarından (popliteal, femoral, iliak venler)** kaynaklanır.",
            "▸ Kopan trombüs parçası vena kava inferior yoluyla sağ atriyum ve sağ ventriküle gelir; oradan ana pulmoner artere fırlatılır.",
            "▸ Pulmoner vasküler yatak tıkandığında pulmoner vasküler direnç akut olarak yükselir.",
            "▸ Sağ ventrikül art-yükü kaldırabilmek için genişler; sol ventriküle kan doluşu azalarak kardiyak debi çöker.",
            "▸ Havalanan ancak kanlanamayan alveollerde ölü boşluk (dead space) ventilasyonu oluşur; şiddetli hipoksemi gelişir."
        ],
        "clinicalSignificance": [
            "▸ Çoğu küçük emboli klinik olarak sessizdir veya zamanla rezorbe olur.",
            "▸ Masif pulmoner emboliler (>%60 yatak tıkanması) saniyeler içinde **akut kor pulmonale, kardiyojenik şok ve ani ölüme** yol açar.",
            "▸ Orta boy emboliler kalbi sağlam bireylerde bronşiyal arterlerin çift dolaşımı nedeniyle enfarktüs yapmaz; ancak sol kalp yetmezliği olanlarda **kırmızı (hemorajik) akciğer enfarktüsüne** neden olur."
        ],
        "differentialDiagnosis": [
            "▸ **Sistemik Tromboemboli:** Sol kalpten çıkar, periferik organları (bacak, beyin) tıkar.",
            "▸ **Pulmoner Tromboemboli:** Sağ kalpten çıkar, akciğer dolaşımını tıkar."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: PTE'lerin >%95'i alt ekstremite derin ven trombozundan (DVT) köken alır.",
            "🔵 ÇIKMIŞ SORU: Masif pulmoner embolide ani ölüme yol açan mekanizma **akut kor pulmonale ve sol ventrikül doluşunun çökmesidir**."
        ],
        "relatedTerms": ["derin-ven-trombozu", "eyer-emboli-saddle-embolus", "paradoksal-emboli", "kirmizi-hemorajik-enfarktus"]
    },
    {
        "id": "eyer-emboli-saddle-embolus",
        "title": "Eyer Emboli (Saddle Embolus)",
        "subtitle": "Pulmoner arter bifurkasyonunu tıkayan dev pıhtı",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Adli Tıp",
        "summary": "Ana pulmoner arterin sağ ve sol ana dallara ayrıldığı çatal noktasına (bifurkasyon) at nalı / eyer gibi oturan, her iki akciğer kan akımını aniden keserek saniyeler içinde akut sağ kalp yetmezliği ve kardiyovasküler kollapsla ani ölüme yol açan masif tromboemboli formudur.",
        "mechanism": [
            "▸ Geniş çaplı bacak venlerinden (iliyak veya femoral ven) kopan bütün halindeki büyük bir trombüs kitlesi sağ kalpten geçer.",
            "▸ Ana pulmoner arter bifurkasyonunda takılıp kalır.",
            "▸ Pulmoner arter yatağının **>%60'ını aniden tıkar**.",
            "▸ Sağ ventrikül kanı pompalayamaz, aniden genişler (akut dilatasyon) ve akut kor pulmonale gelişir.",
            "▸ Akciğerlere kan gidemediği için sol ventrikül doluşu (preload) sıfırlanır; periferik nabızlar kaybolur ve hasta elektromekanik disosiasyonla kaybedilir."
        ],
        "clinicalSignificance": [
            "▸ Akut cerrahi sonrası yatan veya uzun süre hareketsiz kalan hastalarda ani ölümün en dramatik nedenidir.",
            "▸ Akciğer dokusunda iskemik enfarktüs gelişmeye vakit kalmadan ölüm meydana gelir.",
            "▸ Otopside ana pulmoner arter açıldığında çatala oturmuş devasa pıhtı doğrudan gözlenir."
        ],
        "differentialDiagnosis": [
            "▸ **Küçük Pulmoner Emboliler:** Distal dalları tıkar, plöretik ağrı ve hemoptizi yapabilir.",
            "▸ **Eyer Emboli:** Ana arteri tıkar, ağrı yerine ani senkop ve dakikalar içinde ölüm yapar."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Eyer embolisinde doku enfarktüsü **GELİŞMEYE VAKİT BULAMAZ**; ölüm kardiyovasküler şoktandır.",
            "🔵 ÇIKMIŞ SORU: Ana pulmoner arter bifurkasyonuna oturan eyer embolisinde hastanın aniden kaybedilmesinin nedeni **akut sağ ventrikül yetmezliği ve kardiyojenik şoktur**."
        ],
        "relatedTerms": ["pulmoner-tromboembolizm-pte", "derin-ven-trombozu", "akut-kor-pulmonale", "ani-olum"]
    },
    {
        "id": "paradoksal-emboli",
        "title": "Paradoksal Emboli",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Nöroloji",
        "summary": "Venöz dolaşımdan (DVT) köken alan bir pıhtının, intrakardiyak bir defekt (en sık Patent Foramen Ovale - PFO veya ASD) aracılığıyla sağ kalpten sol kalbe geçerek sistemik arteriyel yatakta (örneğin beyinde) tıkanıklık ve enfarktüs oluşturmasıdır.",
        "mechanism": [
            "▸ Hasta bacağında DVT taşırken pulmoner hipertansiyon, Valsalva manevrası veya öksürük nedeniyle sağ atriyum basıncı aniden sol atriyum basıncını geçer.",
            "▸ Bu basınç farkı **Patent Foramen Ovale (PFO)** veya **Atriyal Septal Defekt (ASD)** kapağını açar.",
            "▸ Venöz pıhtı pulmoner kapiller filtreye gitmek yerine sağ atriyumdan sol atriyuma kaçar (**sağdan sola şant**).",
            "▸ Sol ventrikülden aorta fırlatılır ve karotid arterler yoluyla serebral dolaşımı tıkayarak akut iskemik inmeye neden olur."
        ],
        "clinicalSignificance": [
            "▸ Genç yaşta altta yatan ateroskleroz olmaksızın gelişen kriptojenik inmelerin (nedeni belirsiz felçlerin) en önemli nedenidir.",
            "▸ Tanıda kontrastlı ekokardiyografi (kabarcık testi - bubble study) ile sağdan sola geçiş gösterilir.",
            "▸ Tedavide perkütan PFO kapatılması uygulanır."
        ],
        "differentialDiagnosis": [
            "▸ **Normal Tromboemboli:** Venöz pıhtı akciğere gider; arteriyel pıhtı periferik organlara gider.",
            "▸ **Paradoksal Emboli:** Venöz pıhtı şant yoluyla arteriyel organa (beyin, böbrek) gider."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Paradoksal emboli için **sağdan sola şant (en sık PFO veya ASD)** zorunludur.",
            "🔵 ÇIKMIŞ SORU: Derin ven trombozu olan genç bir hastada aynı anda beyin enfarktüsü (inme) saptanması **Paradoksal Emboli (PFO/ASD)** tanısını koydurur."
        ],
        "relatedTerms": ["pulmoner-tromboembolizm-pte", "sistemik-tromboembolizm", "iskemik-inme", "patent-foramen-ovale"]
    },
    {
        "id": "yag-embolisi-sendromu",
        "title": "Yağ Embolisi Sendromu (Fat Embolism Syndrome - FES)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Ortopedi",
        "summary": "Özellikle femur ve tibia gibi uzun kemik kırıkları veya ortopedik travmalardan 24-72 saat sonra ortaya çıkan; solunum yetmezliği, nörolojik konfüzyon ve peteşiyal döküntü triadı ile seyreden multisistemik tablodur.",
        "mechanism": [
            "▸ Kırık alanında parçalanan kemik iliği venöz sinüzoidlerine serbest medüller yağ globülleri girer.",
            "▸ Yağ damlacıkları pulmoner kapillerleri mekanik olarak tıkar.",
            "▸ Endotelyal lipazlar yağı **toksik serbest yağ asitlerine (FFA)** yıkar.",
            "▸ Serbest yağ asitleri endotelde masif hasar, kapiller kaçak ve yaygın trombosit agregasyonu tetikler.",
            "▸ Sistemik dolaşıma geçen mikrodamlacıklar beyin kapillerlerini tıkayarak konfüzyona, dermal kapillerleri patlatarak peteşilere yol açar."
        ],
        "clinicalSignificance": [
            "▸ Klasik Triad: **Solunum yetmezliği (ARDS) + Nörolojik disfonksiyon (konfüzyon/koma) + Peteşiyal cilt döküntüsü** (aksilla, boyun, konjonktiva).",
            "▸ Otopside tanısı için standart parafin blok yerine **donuk (frozen) kesit ve Oil Red O / Sudan** boyası kullanılmalıdır (çünkü parafin takibindeki alkol ve ksilol yağı eritir!)."
        ],
        "differentialDiagnosis": [
            "▸ **Pulmoner Tromboemboli:** Kırıktan hemen sonra değil 5-10 gün sonra çıkar, peteşi yapmaz.",
            "▸ **Yağ Embolisi:** Kırıktan 1-3 gün sonra çıkar, peteşiyal döküntü patognomoniktir."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Peteşiyal döküntü en sık **aksilla, göğüs ön yüzü, boyun ve konjonktivada** görülür.",
            "🔵 ÇIKMIŞ SORU: Femur kırığından 48 saat sonra dispne, konfüzyon ve aksiller peteşiler gelişen hastada tanı **Yağ Embolisi Sendromu**dur."
        ],
        "relatedTerms": ["pulmoner-tromboembolizm-pte", "ards-diffuz-alveoler-hasar", "kemik-kirigi", "prakseoloji"]
    },
    {
        "id": "dekompresyon-hastaligi-caisson",
        "title": "Dekompresyon Hastalığı (Vurgun / Caisson Hastalığı)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Sualtı Hekimliği",
        "summary": "Yüksek atmosferik basınçta kanda ve dokularda çözünen azot gazının, ani basınç düşüşünde sıvı fazdan çıkıp gaz kabarcıkları oluşturmasıyla gelişen; akut dönemde ağrılı kas-eklem spazmları (bends), kronik dönemde ise aseptik kemik nekrozu (Caisson hastalığı) yapan gaz embolisi tablosudur.",
        "mechanism": [
            "▸ Henry kanunu gereğince yüksek basınçta (derin dalış) solunan **Azot ($N_2$) gazı** kanda ve özellikle lipitten zengin yağ dokusunda çözünür.",
            "▸ Yüzeye aniden çıkıldığında ortam basıncı hızla düşer; azot gazı çözünür kalamaz ve kanda mikro/makro gaz kabarcıkları halinde çöker.",
            "▸ Gaz kabarcıkları kapiller damarları mekanik olarak tıkar ve endotel yırtılmalarına yol açar.",
            "▸ Kas, eklem ve tendonlarda biriken gaz şiddetli ağrılı büzülmelere (**the bends**) neden olur.",
            "▸ Akciğer mikrosirkülasyonundaki kabarcıklar nefes darlığı ve boğulma hissi (**the chokes**) yaratır.",
            "▸ Kemiklerin besleyici damarlarını tıkaması sonucu femur ve humerus başında kronik **avasküler osteonekroz (Caisson hastalığı)** gelişir."
        ],
        "clinicalSignificance": [
            "▸ Akut acil tedavisi hastanın derhal **Hiperbarik Oksijen Yeniden Basınçlandırma Odasına** alınmasıdır (böylece azot gazı tekrar kanda çözünür).",
            "▸ Dalgıçlar ve basınçlı tünel işçilerinde meslek hastalığıdır."
        ],
        "differentialDiagnosis": [
            "▸ **İatrojenik Hava Embolisi:** Santral kateterden giren hava (sağ kalpte köpük tıkacı).",
            "▸ **Dekompresyon:** Basınç düşüşüyle doku içinden çıkan azot kabarcıkları."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Sorumlu gaz ==Azot ($N_2$)==; kronik kemik komplikasyonu ==Aseptik Kemik Nekrozu (Caisson Hastalığı)==.",
            "🔵 ÇIKMIŞ SORU: Dalgıçlarda hızlı dekompresyon sonrası femur ve humerus başında gelişen avasküler osteonekroza **Caisson Hastalığı** denir."
        ],
        "relatedTerms": ["gaz-embolisi", "avaskuler-nekroz", "hiperbarik-oksijen", "kemik-patolojisi"]
    },
    {
        "id": "amniyon-sivisi-embolisi",
        "title": "Amniyon Sıvısı Embolisi (AFE)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Kadın Hastalıkları ve Doğum",
        "summary": "Doğum sırasında veya hemen sonrasında plasental yırtıklar aracılığıyla maternal dolaşıma fetal hücre ve sıvı geçişi sonucu gelişen; ani kardiyovasküler şok, solunum yetmezliği ve yaygın damar içi pıhtılaşma (DİK) ile seyreden, mortalitesi %80'i aşan trajik obstetrik komplikasyondur.",
        "mechanism": [
            "▸ Uterin venler açılır ve amniyon sıvısı anne dolaşımına hücum eder.",
            "▸ Sıvı içinde bulunan **fetal skuamöz epitel hücreleri, lanugo tüyleri, verniks kazeoza ve mekonyum** anne pulmoner damarlarına ulaşır.",
            "▸ Tablo basit bir mekanik tıkanma değildir; amniyon sıvısındaki vazoaktif aminler ve prokoagülanlar masif anafilaktoid şok ve pulmoner vazokonstriksiyonu tetikler (**Gebelikte Anafilaktoid Sendrom**).",
            "▸ Amniyon sıvısındaki doku faktörü aktivitesi maternal dolaşımda fulminan **Dissemine İntravasküler Koagülasyonu (DİK)** başlatır."
        ],
        "clinicalSignificance": [
            "▸ Gelişmiş ülkelerde anne ölümlerinin en sık nedenlerinden biridir (mortalite >%80).",
            "▸ Sağ kurtulan kadınların çoğunda kalıcı nörolojik hasar kalır.",
            "▸ Otopside maternal akciğer damarlarında **fetal skuamoz epitel hücrelerinin ve lanugo tüylerinin** görülmesiyle doğrulanır."
        ],
        "differentialDiagnosis": [
            "▸ **Pulmoner Tromboemboli:** DİK nadirdir, lohusalıkta daha geç çıkar.",
            "▸ **Amniyon Sıvı Embolisi:** Doğum eylemi anında aniden başlar; kardiyak kollaps + masif DİK kanaması birliktedir."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Otopside tanı: ==Maternal pulmoner kapillerlerde fetal skuamöz hücreler ve lanugo kılları==.",
            "🔵 ÇIKMIŞ SORU: Doğum sırasında aniden şoka giren ve DİK gelişerek vefat eden annenin otopsisinde maternal akciğer damarlarında **fetal skuamlar** aranır."
        ],
        "relatedTerms": ["dissemine-intravaskuler-koagulasyon-dik", "septik-sok", "tromboemboli", "gebelik-komplikasyonlari"]
    },
    {
        "id": "beyaz-soluk-enfarktus",
        "title": "Beyaz (Soluk / Anemik) Enfarktüs",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji",
        "summary": "Uç arter (end-artery) dolaşımına sahip solid organlarda (kalp, böbrek, dalak) arteriyel tıkanma sonucu gelişen, doku yoğunluğu nedeniyle kanın içeri sızamadığı, tebeşir gibi sarı-beyaz renkli koagülasyon nekrozu alanıdır.",
        "mechanism": [
            "▸ Solid parankimli organda besleyici tek uç arter (kollaterali olmayan) trombüs veya emboli ile aniden tıkanır.",
            "▸ Dokunun kanlanması tamamen kesilir; hücreler iskemik nekroza uğrar.",
            "▸ Solid dokunun yoğun hücre mimarisi, komşu sağlam kapillerlerden nekroz odağına eritrositlerin sızmasını engeller.",
            "▸ Nekrotik hücrelerin şişmesi ve eritrositlerin hızla erimesiyle enfarkt alanı sarı-beyaz bir renk alır.",
            "▸ Etrafında akut enflamatuar yanıta bağlı ince hiperemik kırmızı bir kenar kuşağı oluşur."
        ],
        "clinicalSignificance": [
            "▸ En tipik örnekleri: **Miyokard Enfarktüsü, Renal Enfarktüs ve Splenik Enfarktüs**.",
            "▸ Makroskobik olarak kama (üçgen) şeklindedir; tabanı organ kapsülüne oturur.",
            "▸ Kapsül üzerinde fibrin birikimi perisplenit veya perikardite yol açarak şiddetli batıcı ağrı yapar."
        ],
        "differentialDiagnosis": [
            "▸ **Kırmızı Enfarktüs:** Çift dolaşımlı veya gevşek dokularda (akciğer, bağırsak) ya da venöz tıkanmada kanlı nekroz.",
            "▸ **Beyaz Enfarktüs:** Solid uç arterli organlarda (kalp, böbrek, dalak) kansız soluk nekroz."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Beyaz enfarktüs organları: ==Kalp, Dalak, Böbrek== (Solid organ + Uç arter).",
            "🔵 ÇIKMIŞ SORU: Dalak ve böbrekte arter tıkanıklığı sonucu gelişen kama şeklindeki sarı-beyaz lezyon **anemik (beyaz) enfarktüstür**."
        ],
        "relatedTerms": ["kirmizi-hemorajik-enfarktus", "koagulasyon-nekrozu", "miyokard-enfarktusu", "splenik-enfarktus"]
    },
    {
        "id": "kirmizi-hemorajik-enfarktus",
        "title": "Kırmızı (Hemorajik) Enfarktüs",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji",
        "summary": "Çift kan dolaşımına sahip organlarda (akciğer, ince bağırsak), gevşek dokularda, venöz drenaj tıkanıklıklarında (testis/over torsiyonu) veya tıkanmış bir arterin yeniden açılması (reperfüzyon) sonrasında nekroz alanına masif kan sızmasıyla oluşan koyu kırmızı-mor iskemik nekrozdur.",
        "mechanism": [
            "▸ **Çift Dolaşım Mekanizması:** Akciğerde pulmoner arter tıkansa dahi sağlam bronşiyal arterden nekroze alana kan pompalanır; damar endoteli ölü olduğu için kan parankime taşar.",
            "▸ **Venöz Tıkanıklık:** Testis torsiyonunda venöz çıkış tıkanır; arter kanı pompalamayı sürdürür ancak çıkış olmadığı için kapillerler patlar ve organ kan gölüne döner.",
            "▸ **Gevşek Doku:** Akciğer alveolleri süngerimsi olduğu için çevre sağlam damarlardan sızan eritrositlerle kolayca dolar.",
            "▸ **Reperfüzyon:** Trombolitik tedavi ile açılan damarın taze kanı, nekroze olmuş geçirgen kapillerlerden dışarı fışkırır."
        ],
        "clinicalSignificance": [
            "▸ En klasik organlar: **Akciğer, İnce Bağırsak, Testis, Over**.",
            "▸ Akciğer enfarktüsleri daima kırmızıdır; tabanı plevraya oturan kama şeklinde lezyonlardır; plöretik göğüs ağrısı ve hemoptizi yapar.",
            "▸ Testis/over torsiyonunda acil detorsiyon yapılmazsa organ nekroze olup kaybedilir."
        ],
        "differentialDiagnosis": [
            "▸ **Beyaz Enfarktüs:** Kalp, böbrek, dalak (uç arterler, solid doku).",
            "▸ **Kırmızı Enfarktüs:** Akciğer, bağırsak, testis torsiyonu (çift dolaşım, venöz tıkanıklık, gevşek doku)."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Akciğer ve bağırsak enfarktüsleri **DAİMA KIRMIZI (HEMORAJİK)** tiptedir.",
            "🔵 ÇIKMIŞ SORU: Testis torsiyonunda gelişen enfarktüs tipi **kırmızı (hemorajik) enfarktüs** olup venöz drenaj bozukluğuna sekonderdir."
        ],
        "relatedTerms": ["beyaz-soluk-enfarktus", "pulmoner-tromboembolizm-pte", "testis-torsiyonu", "reperfuzyon-hasari"]
    },
    {
        "id": "kardiyojenik-sok",
        "title": "Kardiyojenik Şok",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Kardiyoloji",
        "summary": "Miyokardiyal pompa yetersizliği sonucu kardiyak debinin periferik doku perfüzyonunu sağlayamayacak düzeye inmesiyle karakterize; yüksek mortaliteye (>%70), yüksek periferik dirence ve pulmoner ödeme sahip şok tablosudur.",
        "mechanism": [
            "▸ En sık neden: Sol ventrikül miyokard kütlesinin **>%40'ını tutan transmural enfarktüs**.",
            "▸ Sol ventrikül sistolik fonksiyonu çöker; kardiyak debi (CO) ve atım hacmi dramatik düşer.",
            "▸ Sol ventrikül kanı boşaltamaz; diyastol sonu basınç artar ve geriye doğru sol atriyum ile pulmoner venlere yansır (**PCWP >18 mmHg**).",
            "▸ Pulmoner kapiller hidrostatik basınç onkotik basıncı aşınca alveollere sıvı sızar (**Akut Pulmoner Ödem**).",
            "▸ Vücut hipotansiyona karşı sempatik vazokonstriksiyon geliştirir; sistemik vasküler direnç (SVR) artar ve cilt soğuk, soluk, nemli hale gelir."
        ],
        "clinicalSignificance": [
            "▸ Miyokard enfarktüsü hastalarında hastane içi ölümlerin en sık nedenidir.",
            "▸ Klinik: Şiddetli hipotansiyon, taşikardi, dispne, akciğerde yaş raller, boyun venöz dolgunluğu ve periferik siyanoz.",
            "▸ Tedavide inotropik ajanlar (Dobutamin), vazopressörler ve mekanik destek sistemleri (intraaortik balon pompası - IABP, ECMO) kullanılır."
        ],
        "differentialDiagnosis": [
            "▸ **Hipovolemik Şok:** CVP ve PCWP düşüktür, akciğerler temizdir, boyun venleri kollabedir.",
            "▸ **Kardiyojenik Şok:** CVP ve PCWP yüksektir, akciğer ödemi ve boyun venöz dolgunluğu vardır."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Sol ventrikülün **%40'ından fazlası** enfarktüse uğradığında kardiyojenik şok gelişir.",
            "🔵 ÇIKMIŞ SORU: Kardiyojenik şokta kardiyak debi **düşük**, pulmoner kapiller uç basıncı (PCWP) ve periferik vasküler direnç (SVR) ise **yüksektir**."
        ],
        "relatedTerms": ["hipovolemik-sok", "septik-sok", "miyokard-enfarktusu", "pulmoner-odem"]
    },
    {
        "id": "septik-sok",
        "title": "Septik Şok",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Yoğun Bakım",
        "summary": "Enfeksiyona karşı konağın kontrolsüz disregüle immün yanıtı sonucu ortaya çıkan; proenflamatuar sitokin fırtınası, indüklenebilir nitrik oksit (iNOS) aracılı masif sistemik vazodilatasyon, kapiller kaçak ve yaygın mikrotrombüslerle (DİK) karakterize yüksek mortaliteli şok tablosudur.",
        "mechanism": [
            "▸ PAMP'lar (Gram negatif LPS veya Gram pozitif peptidoglikanlar), makrofaj TLR4/CD14 reseptörlerine bağlanır.",
            "▸ Masif **TNF-$\alpha$, IL-1 ve IL-6** salınımı ile sitokin fırtınası başlar.",
            "▸ Endotel ve düz kaslarda **iNOS (İndüklenebilir NO Sentaz)** uyarılır; aşırı **Nitrik Oksit (NO)** sentezi sistemik arteriyolleri felç edercesine genişletir (vazodilatasyon).",
            "▸ Periferik direnç (SVR) çöker; erken evrede kan deride göllenir (**Sıcak Şok / Warm Shock**).",
            "▸ Endotel bağlantıları kopar; plazma doku aralığına sızarak masif hipovolemi ve ödem yapar.",
            "▸ Doku faktörü patlamasıyla yaygın damar içi mikrotrombüsler (**DİK**) oluşur ve doku oksijenlenmesi durur."
        ],
        "clinicalSignificance": [
            "▸ Yoğun bakım ünitelerinde sepsis kaynaklı ölümlerin başlıca sebebidir (mortalite %40-60).",
            "▸ Yeterli sıvı resüsitasyonuna rağmen ortalama arter basıncını $\ge 65$ mmHg tutmak için vazopressör gereksinimi ve serum laktat düzeyinin $>2$ mmol/L olması ile tanımlanır.",
            "▸ Erken geniş spektrumlu antibiyotik, agresif kristaloid sıvı ve Noradrenalin infüzyonu esastır."
        ],
        "differentialDiagnosis": [
            "▸ **Kardiyojenik/Hipovolemik Şok:** Erken dönemde periferik direnç artar, cilt soğuk ve soluktur (Soğuk Şok).",
            "▸ **Septik Şok:** Erken dönemde NO etkisiyle periferik direnç çöker, cilt sıcak ve pembedir (Sıcak Şok)."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Septik şokta sistemik vazodilatasyondan sorumlu temel aracı **Nitrik Oksit (NO) ve iNOS** aktivasyonudur.",
            "🔵 ÇIKMIŞ SORU: Gram negatif sepsiste endotoksinin makrofajlarda bağlandığı reseptör **Toll-Like Reseptör 4 (TLR4)**'tür."
        ],
        "relatedTerms": ["kardiyojenik-sok", "hipovolemik-sok", "dissemine-intravaskuler-koagulasyon-dik", "sok-akcigeri-ards"]
    },
    {
        "id": "sok-bobrek-atn",
        "title": "Şok Böbreği (İskemik Akut Tübüler Nekroz - ATN)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Nefroloji",
        "summary": "Herhangi bir şok tablosunda uzamış renal hipoperfüzyon sonucu gelişen, metabolik aktivitesi yüksek proksimal tübül epitelinin nekrozu ve dökülmesiyle karakterize, oligüri ve çamur rengi granüler silendirlerle seyreden akut böbrek hasarı tablosudur.",
        "mechanism": [
            "▸ Şokta kanın beyin ve kalbe yönlendirilmesi için renal arteriyollerde yoğun vazokonstriksiyon gelişir.",
            "▸ Renal perfüzyon kritik eşiğin altına iner; tübül epiteli oksijensiz kalır.",
            "▸ **Proksimal kıvrıntılı tübüller** ve Henle kalın çıkan kolu hücreleri ATP tükenmesiyle nekroze olur ve bazal membrandan dökülür.",
            "▸ Dökülen nekrotik hücreler tübül lümenini tıkayarak intratübüler basıncı artırır; glomerüler filtrasyon durur.",
            "▸ İdrar sedimentinde patognomonik **Çamur Rengi Granüler Silendirler (Muddy brown casts)** görülür."
        ],
        "clinicalSignificance": [
            "▸ Şok hastalarında gelişen akut oligüri (<400 mL/gün) veya anürinin en sık nedenidir.",
            "▸ Tübül bazal membranı korunmuşsa (rüptüre olmamışsa), hasta diyaliz ile desteklendiğinde 1-3 hafta içinde epitel prolifere olarak böbrek fonksiyonları tamamen düzelebilir (**Reversibl Potansiyel**)."
        ],
        "differentialDiagnosis": [
            "▸ **Prerenal Azotemi:** Tübül nekrozu yoktur, fraksiyonel sodyum atılımı (FeNa) <%1'dir, sıvı verilince hızla düzelir.",
            "▸ **İskemik ATN:** Tübül nekrozu vardır, FeNa >%2'dir, çamur rengi silendirler pozitiftir, sıvıya hemen yanıt vermez."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: İskemik ATN'de en hassas hücreler ==Proksimal Tübül Epiteli==dir.",
            "🔵 ÇIKMIŞ SORU: Şok sonrası oligüri gelişen hastanın idrarında saptanan **çamur rengi granüler silendirler** iskemik akut tübüler nekrozun (şok böbreği) en karakteristik bulgusudur."
        ],
        "relatedTerms": ["akut-tubuler-nekroz", "hipovolemik-sok", "septik-sok", "prerenal-azotemi"]
    },
    {
        "id": "sok-akcigeri-ards",
        "title": "Şok Akciğeri (Diffüz Alveoler Hasar / ARDS)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Göğüs Hastalıkları",
        "summary": "Özellikle septik şok, ağır travma veya pankreatit zemininde alveolokapiller membranın nötrofil kaynaklı akut yaygın hasarı sonucu gelişen; alveol içi zengin fibrinli eksüda ve pembe hyalen membran oluşumuyla seyreden ağır solunum yetmezliği tablosudur.",
        "mechanism": [
            "▸ Sistemik sitokinler (TNF, IL-1) pulmoner kapiller endotelini aktive eder.",
            "▸ Çok sayıda nötrofil pulmoner kapiller yatağa sekestre olur ve aktive olur.",
            "▸ Nötrofillerden proteazlar, reaktif oksijen radikalleri (ROS) ve lökotrienler salınır.",
            "▸ Kapiller endoteli ve Tip I pnömositler nekroze olur; mikrovasküler permeabilite tavan yapar.",
            "▸ Alveol boşluklarına plazma proteinleri, fibrin ve nekrotik hücre artıkları dolar.",
            "▸ Bu proteinli eksüda alveol iç duvarına yapışarak karakteristik pembe **Hyalen Membranları** oluşturur.",
            "▸ Sürfaktan inaktive olur, alveoller kollabe olur (mikroatelektaziler) ve gaz değişimi çöker."
        ],
        "clinicalSignificance": [
            "▸ Septik şok hastalarında en erken iflas eden organdır.",
            "▸ Oksijen tedavisine dirençli (refrakter) şiddetli hipoksemi ($PaO_2/FiO_2 \le 300$) ve akciğer grafisinde bilateral yaygın infiltrasyonlar.",
            "▸ İyileşen olgularda Tip II pnömosit hiperplazisi ve fibroblastik organizasyonla interstisyel fibrozis kalabilir."
        ],
        "differentialDiagnosis": [
            "▸ **Kardiyojenik Pulmoner Ödem:** PCWP >18 mmHg, sol kalp yetmezliği vardır, hyalen membran görülmez.",
            "▸ **Non-Kardiyojenik Pulmoner Ödem (ARDS):** PCWP normaldir (<18 mmHg), endotel geçirgenlik hasarı vardır, hyalen membranlar pozitiftir."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: ARDS'nin histopatolojik tanımı ==Diffüz Alveoler Hasar (DAD)== olup belirteci **Hyalen Membranlar**dır.",
            "🔵 ÇIKMIŞ SORU: Septik şok otopsisinde akciğer mikroskopisinde alveol lümenlerini döşeyen pembe fibrinöz örtüler **Hyalen Membranlar (ARDS / Şok Akciğeri)** tanısı koydurur."
        ],
        "relatedTerms": ["septik-sok", "ards-diffuz-alveoler-hasar", "hyalen-membran", "tip-2-pnomosit"]
    },
    {
        "id": "waterhouse-friderichsen-sendromu",
        "title": "Waterhouse-Friderichsen Sendromu",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Endokrinoloji",
        "summary": "Özellikle Neisseria meningitidis (meningokok) sepsisi geçiren çocuklarda yaygın damar içi pıhtılaşma (DİK) zemininde her iki adrenal bezde masif hemorajik nekroz ve akut sürrenal yetmezlikle seyreden fulminan ve ölümcül tablodur.",
        "mechanism": [
            "▸ *Neisseria meningitidis* bakteriyemisi kanda aşırı endotoksin (LPS) açığa çıkarır.",
            "▸ Şiddetli sitokin salınımıyla fulminan septik şok ve yaygın DİK gelişir.",
            "▸ Adrenal korteks venüllerinde mikrotrombüsler oluşur ve venöz çıkış tıkanır.",
            "▸ Yüksek adrenal arteriyel basınç zemininde sürrenal bezlerin parankimi içine masif iki taraflı kanama ve nekroz gerçekleşir (**Bilateral Adrenal Apopleksi**).",
            "▸ Kortizol ve aldosteron sentezi aniden sıfırlanır; periferik damar tonusu tamamen çöker ve kardiyovasküler kollaps derinleşir."
        ],
        "clinicalSignificance": [
            "▸ Ateş, yaygın peteşiyal/purpurik deri döküntüleri (purpura fulminans) ve hızla derinleşen hipotansiyon.",
            "▸ Saatler içinde hastayı ölüme götüren pediatrik bir acildir.",
            "▸ Tedavide acil antibiyoterapi yanında stres dozu hidrokortizon replasmanı şarttır."
        ],
        "differentialDiagnosis": [
            "▸ **Addison Hastalığı:** Kronik otoimmün adrenal korteks yıkımıdır; yavaş gelişir.",
            "▸ **Waterhouse-Friderichsen:** Akut meningokoksemik hemoraji ve saatler içinde ölümcül apopleksi."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Klasik etken: ==Neisseria meningitidis (Meningokok)==; Lezyon: ==Bilateral Masif Adrenal Hemorajik Nekroz==.",
            "🔵 ÇIKMIŞ SORU: Meningokoksemili çocukta purpura fulminans ve her iki adrenal bezde yaygın kanamalı nekrozla seyreden ölümcül tablo **Waterhouse-Friderichsen Sendromu**dur."
        ],
        "relatedTerms": ["septik-sok", "dissemine-intravaskuler-koagulasyon-dik", "adrenal-yetmezlik", "meningokoksemi"]
    }
]

# -------------------------------------------------------------
# GLOSSARY TERMS FOR TOOLTIP / TOAST
# -------------------------------------------------------------

glossary_terms = {
    "Emboli": "Kan akımı ile taşınarak oluştuğu odaktan uzaktaki bir damar lümenini kısmen veya tamamen tıkayan katı, sıvı veya gaz kitle.",
    "Tromboemboli": "Bir venöz veya arteriyel trombüsten koparak dolaşıma katılan ve tüm embolilerin %95'inden fazlasını oluşturan pıhtı embolisi.",
    "Pulmoner Tromboembolizm (PTE)": "Alt ekstremite derin venlerinden (DVT) kopan pıhtıların sağ kalbi geçerek pulmoner arter yatağını tıkaması tablosu.",
    "Eyer Emboli (Saddle Embolus)": "Ana pulmoner arterin sağ ve sol ana dallara ayrıldığı çatal noktasına (bifurkasyona) oturarak akut sağ kalp yetmezliği ve ani ölüme yol açan dev tromboemboli.",
    "Paradoksal Emboli": "Venöz kaynaklı bir pıhtının patent foramen ovale (PFO) veya ASD üzerinden sağ kalpten sol kalbe geçerek sistemik arter yatağını (örn. beyin) tıkaması.",
    "Yağ Embolisi Sendromu": "Uzun kemik (femur/tibia) kırıklarından 1-3 gün sonra dispne, konfüzyon ve aksiller peteşiyal döküntü triadı ile ortaya çıkan tablo.",
    "Dekompresyon Hastalığı": "Hızlı basınç düşüşünde kanda çözünmüş azot (N2) gazının kabarcıklaşarak eklem ağrıları (bends) ve akciğerde gaz embolisi (chokes) yapması.",
    "Caisson Hastalığı": "Dekompresyon hastalığına bağlı gaz embolilerinin kemik besleyici damarlarını tıkaması sonucu femur ve humerus başında gelişen kronik avasküler osteonekroz.",
    "Amniyon Sıvısı Embolisi": "Doğum sırasında fetal skuamöz epitel ve lanugo tüylerinin anne dolaşımına geçmesiyle tetiklenen kardiyovasküler şok ve masif DİK tablosu.",
    "Enfarktüs": "Arteriyel beslenmenin veya venöz drenajın kesilmesine bağlı olarak bir dokuda gelişen lokalize iskemik nekroz alanı.",
    "Beyaz (Soluk) Enfarktüs": "Kalp, dalak ve böbrek gibi solid organlarda uç arterlerin tıkanması sonucu gelişen kansız koagülasyon nekrozu.",
    "Kırmızı (Hemorajik) Enfarktüs": "Akciğer ve bağırsak gibi çift dolaşımlı veya gevşek dokularda ya da testis torsiyonu gibi venöz tıkanıklıklarda gelişen kanamalı iskemik nekroz.",
    "Koagülasyon Nekrozu": "İskemi sonucu hücre proteinlerinin denatüre olduğu, çekirdeklerin kaybolduğu ancak hayalet hücre sınırlarının korunduğu temel nekroz tipi.",
    "Likefaksiyon Nekrozu": "Santral sinir sisteminde (beyin) iskemik enfarktüs sonucu dokunun hidrolitik enzimlerle eriyerek kistik bir kavitasyon oluşturduğu sıvılaşma nekrozu.",
    "Şok": "Kardiyak debideki azalma veya efektif dolaşan hacmin yetersizliği sonucu dokuların hücresel oksijen ihtiyacını karşılayamadığı sistemik hipoperfüzyon durumu.",
    "Laktik Asidoz": "Şok sırasında hücresel hipoksi nedeniyle mitokondriyal solunumun durması ve anaerobik glikoliz sonucu kanda laktat birikmesiyle oluşan metabolik kriz.",
    "Kardiyojenik Şok": "Geniş miyokard enfarktüsü (>%40 sol ventrikül kaybı) veya aritmiler sonucu kalbin pompa fonksiyonunun çökmesiyle gelişen şok.",
    "Hipovolemik Şok": "Masif kanama, yanık veya ağır kusma-ishal sonucu intravasküler kan ve plazma hacminin akut kaybıyla gelişen soğuk şok tablosu.",
    "Septik Şok": "Sistemik enfeksiyona karşı konağın kontrolsüz sitokin yanıtı ve aşırı nitrik oksit (NO) üretimi sonucu periferik vazodilatasyon ve DİK ile seyreden şok.",
    "Sıcak Şok (Warm Shock)": "Septik şokun erken döneminde indüklenebilir NO sentaz (iNOS) aracılı aşırı vazodilatasyon nedeniyle cildin sıcak, pembe ve kuru olması.",
    "Nörojenik Şok": "Spinal kord travmasında sempatik tonusun aniden felç olması sonucu vazodilatasyon, hipotansiyon ve paradoksal bradikardi ile seyreden şok.",
    "Anafilaktik Şok": "Tip I aşırı duyarlılık reaksiyonunda IgE aracılı masif histamin salınımıyla gelişen hipotansiyon, laringeal ödem ve bronkospazm tablosu.",
    "Şok Böbreği (İskemik ATN)": "Uzamış şok hipoperfüzyonunda proksimal tübül epitelinin nekroze olup lümene dökülmesiyle seyreden oligürik akut böbrek hasarı.",
    "Çamur Rengi Silendirler": "İskemik akut tübüler nekrozda (şok böbreği) dökülen nekrotik tübül epitel hücrelerinin idrarda oluşturduğu patognomonik granüler silendirler.",
    "Şok Akciğeri (ARDS)": "Septik şokta aktive nötrofillerin alveolokapiller membranı yıkmasıyla alveol içi fibrinöz hyalen membranların oluştuğu ağır solunum yetmezliği.",
    "Hyalen Membran": "ARDS ve şok akciğerinde nekrotik epitel artıkları ve fibrinli eksüdanın alveol iç duvarını pembe homojen bir bant gibi kaplamasıyla oluşan lezyon.",
    "Waterhouse-Friderichsen Sendromu": "Meningokoksemide bilateral adrenal bezlerde masif hemorajik nekroz ve akut sürrenal yetmezlikle seyreden fulminan sendrom.",
    "MODS (Çoklu Organ Yetmezliği Sendromu)": "Tedavi edilemeyen şokun terminal evresinde akciğer, böbrek, karaciğer ve kalbin art arda fonksiyonlarını kaybetmesi.",
    "Kor Pulmonale": "Pulmoner arter yatağındaki basınç artışı veya masif emboli nedeniyle sağ ventrikülün akut veya kronik olarak genişleyip yetmezliğe girmesi.",
    "Oligüri": "Erişkin bir bireyde idrar çıkışının 24 saatte 400 mL'nin (<0.5 mL/kg/saat) altına inmesi; şokta renal hipoperfüzyonun en erken klinik işaretidir."
}

# -------------------------------------------------------------
# MAIN INTEGRATION LOGIC
# -------------------------------------------------------------

def run_integration():
    print(f"Executing integration for {DECK_TITLE}...")

    # 1. ADD DECK TO interactive_learning_decks.json
    decks_file = "src/data/interactive_learning_decks.json"
    with open(decks_file, "r", encoding="utf-8") as f:
        decks = json.load(f)

    new_deck = {
        "id": DECK_ID,
        "title": DECK_TITLE,
        "discipline": DISCIPLINE,
        "instructor": INSTRUCTOR,
        "committee": COMMITTEE,
        "description": "Prof. Dr. Hikmet Keleş'in Dönem 2 Kurul 1 Patoloji ders notundan derlenmiş; emboli tiplerinden (tromboemboli, eyer emboli, yağ, gaz ve amniyon embolisi) enfarktüs çeşitlerine (beyaz vs kırmızı enfarktüs, likefaksiyon istisnası), şok etiyolojisinden (kardiyojenik, hipovolemik, septik şok) organ morfolojilerine (ATN, ARDS, Waterhouse-Friderichsen) kadar %500 derinlikli 24 slayt ve 24 özgün çalışma sorusu içeren kapsamlı interaktif öğrenme güvertesi.",
        "slidesCount": len(slides),
        "detailLevel": "500%",
        "slides": slides
    }

    existing_index = next((i for i, d in enumerate(decks) if d.get("id") == DECK_ID), None)
    if existing_index is not None:
        decks[existing_index] = new_deck
        print(f"Updated existing deck: {DECK_ID}")
    else:
        decks.append(new_deck)
        print(f"Appended new deck: {DECK_ID}. Total decks: {len(decks)}")

    with open(decks_file, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    # 2. ADD STUDY QUESTIONS TO chunk_8.json
    c8_file = "src/data/study_questions/chunk_8.json"
    with open(c8_file, "r", encoding="utf-8") as f:
        chunk_8 = json.load(f)

    added_questions = 0
    for s in slides:
        pq = s.get("practiceQuestion")
        if pq:
            q_obj = {
                "id": f"sq-iskemi-sok-{pq['id']}",
                "deckId": DECK_ID,
                "deckTitle": DECK_TITLE,
                "slideId": s["id"],
                "slideTitle": s["title"],
                "discipline": DISCIPLINE,
                "committee": COMMITTEE,
                "instructor": INSTRUCTOR,
                "question": pq["question"],
                "options": pq["options"],
                "correctAnswer": pq["correctAnswer"],
                "explanation": pq["explanation"],
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
            if not any(x.get("id") == q_obj["id"] for x in chunk_8):
                chunk_8.append(q_obj)
                added_questions += 1

    print(f"Added {added_questions} questions to chunk_8. Total now: {len(chunk_8)}")
    with open(c8_file, "w", encoding="utf-8") as f:
        json.dump(chunk_8, f, ensure_ascii=False, indent=2)

    # 3. UPDATE STUDY QUESTIONS index.json
    idx_file = "src/data/study_questions/index.json"
    with open(idx_file, "r", encoding="utf-8") as f:
        idx_data = json.load(f)

    total_q = 0
    for ch in idx_data.get("chunks", []):
        if ch["chunkId"] == "chunk_8":
            ch["questionCount"] = len(chunk_8)
            if DECK_ID not in ch.get("decksCovered", []):
                ch.setdefault("decksCovered", []).append(DECK_ID)
        total_q += ch.get("questionCount", len(chunk_8))

    idx_data["totalQuestions"] = total_q
    with open(idx_file, "w", encoding="utf-8") as f:
        json.dump(idx_data, f, ensure_ascii=False, indent=2)
    print(f"Updated study_questions/index.json! Total study questions across all chunks: {total_q}")

    # 4. UPDATE LEARNING QUEUE
    queue_file = "src/data/learning_batch_queue.json"
    with open(queue_file, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    for item in queue_data:
        if item.get("id") == DECK_ID:
            item["status"] = "completed"
            item["slidesCount"] = len(slides)
            item["detailLevel"] = "500%"

    # Add next Kurul 1 course: 16) Tümör Biyolojisi ve Terminolojisi
    next_deck_id = "learn-tumor-biyolojisi-ve-terminolojisi"
    has_next = any(x.get("status") == "next_in_queue" and x.get("id") != DECK_ID for x in queue_data)
    if not has_next:
        next_item = {
            "id": next_deck_id,
            "title": "Tümör Biyolojisi ve Terminolojisi",
            "discipline": "Tıbbi Patoloji",
            "status": "next_in_queue",
            "slidesCount": 24,
            "detailLevel": "500% (Planlanan)"
        }
        queue_data.append(next_item)
        print(f"Added next course to queue: {next_deck_id}")

    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, ensure_ascii=False, indent=2)

    # 5. EXPAND ENCYCLOPEDIA
    enc_file = "src/data/medical_encyclopedia.json"
    with open(enc_file, "r", encoding="utf-8") as f:
        encyclopedia = json.load(f)

    enc_added = 0
    enc_updated = 0
    for entry in encyclopedia_entries:
        existing = next((e for e in encyclopedia if e.get("id") == entry["id"]), None)
        if existing:
            existing.update(entry)
            enc_updated += 1
        else:
            encyclopedia.append(entry)
            enc_added += 1

    print(f"Encyclopedia: Added {enc_added} new entries, updated {enc_updated} entries. Total now: {len(encyclopedia)}")
    with open(enc_file, "w", encoding="utf-8") as f:
        json.dump(encyclopedia, f, ensure_ascii=False, indent=2)

    # 6. EXPAND GLOSSARY
    glo_file = "src/data/medical_glossary.json"
    with open(glo_file, "r", encoding="utf-8") as f:
        glossary = json.load(f)

    glo_added = 0
    for term, definition in glossary_terms.items():
        if term not in glossary or len(definition) > len(glossary.get(term, "")):
            glossary[term] = definition
            glo_added += 1

    print(f"Glossary: Added/Updated {glo_added} terms. Total now: {len(glossary)}")
    with open(glo_file, "w", encoding="utf-8") as f:
        json.dump(glossary, f, ensure_ascii=False, indent=2)

    print(f"ALL INTEGRATION TASKS SUCCESSFULLY COMPLETED FOR {DECK_ID}!")

if __name__ == "__main__":
    run_integration()
