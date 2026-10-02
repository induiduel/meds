# -*- coding: utf-8 -*-
"""
generate_thrombosis_complete.py
Ders: Prof. Dr. Hikmet Keleş - Tromboz Patofizyolojisi (Kurul 1 / Dönem 2)
Tüm 24 slayt, spotlar, flashcardlar, 24 özgün çalışma sorusu, chunk_8 ve sözlük/ansiklopedi entegrasyonu.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_ID = "learn-tromboz-patofizyolojisi-tam"
DECK_TITLE = "Tromboz Patofizyolojisi ve Damar Tıkanıklıkları"
DISCIPLINE = "Tıbbi Patoloji"
INSTRUCTOR = "Prof. Dr. Hikmet Keleş"
COMMITTEE = "Dönem 2 / 1. Kurul (Hücre ve Doku Hasarı Mekanizmaları)"

# 24 SLIDES DATA
slides = [
    # SLIDE 1
    {
        "id": "slide-1",
        "title": "Hemostaz vs. Tromboz: Fizyolojik Savunmadan Patolojik Tıkanıklığa",
        "subtitle": "Normal hemostaz ile patolojik damar içi trombüs oluşumu arasındaki temel ayrımlar",
        "content": """**GİRİŞ VE PATOFİZYOLOJİK ÇERÇEVE**
Vasküler sistem, kanı sıvı ve akışkan tutarken aynı zamanda zedelenme durumunda anında pıhtılaştırabilecek dinamik bir dengeye (hemostatik denge) sahiptir.

1. **Hemostaz (Fizyolojik Süreç):**
   - Vasküler yaralanma veya travma sonrası kanamayı durdurmak ve sınırlamak amacıyla damar hasar bölgesinde lokalize, kontrollü kan pıhtısı oluşumudur.
   - Yara iyileşmesi başladığında pıhtı kontrollü bir şekilde lizise uğrar (çözülür).

2. **Tromboz (Patolojik Süreç):**
   - Sağlam veya minimal hasarlı bir damarın ya da kalp boşluklarının lümeninde, uygunsuz, aşırı veya kontrolsüz hemostatik mekanizmaların tetiklenmesiyle pıhtı (**trombüs**) oluşmasıdır.
   - Kan akımını kısmen veya tamamen tıkayarak distal dokularda iskemi ve enfarktüse, koparak emboliye yol açar.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Hemostaz ve Tromboz Ayrımı:**\n  ▫ Hemostaz: Vasküler bütünlük bozulduğunda kan kaybını önleyen **fizyolojik, lokalize ve kendini sınırlayan** yanıt.\n  ▫ Tromboz: Sağlam ya da hafif zedelenmiş endotel üzerinde oluşan **patolojik, kontrolsüz ve potansiyel olarak ölümcül** damar içi pıhtılaşma.\n  ▫ Trombozun en tehlikeli klinik sonuçları: **Akut Miyokard Enfarktüsü, İskemik İnme ve Pulmoner Tromboemboli**'dir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Sınav Klasikleri:**\n  ▫ *Hemostaz ile tromboz arasındaki en temel fark nedir?* → Hemostazın **doku hasarına fizyolojik ve kontrollü yanıt** olmasına karşılık, trombozun **uygunsuz/kontrolsüz hemostatik aktivasyonla intralüminal tıkanıklık** oluşturmasıdır."
        ],
        "flashcards": [
            {
                "question": "Hemostaz ile tromboz arasındaki temel patofizyolojik fark nedir?",
                "answer": "Hemostaz yaralanmaya yanıt olarak kanamayı sınırlayan fizyolojik ve kontrollü pıhtılaşmadır; tromboz ise damar içinde kontrolsüz/uygunsuz pıhtı oluşumuyla lümeni tıkayan patolojik süreçtir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q1",
            "question": "Hemostaz ve tromboz süreçlerinin patofizyolojisi karşılaştırıldığında aşağıdakilerden hangisi trombozu hemostazdan ayıran temel patolojik özelliktir?",
            "options": [
                "A) Fibrinojenin fibrine dönüşümünü içermesi",
                "B) Trombosit adezyon ve agregasyonunun rol oynaması",
                "C) Damar bütünlüğü bozulmadan veya minimal lezyon zemininde kontrolsüz gelişip lümeni tıkaması",
                "D) Koagülasyon kaskadında trombin enziminin üretilmesi",
                "E) Vasküler endotel hücreleri ile etkileşim halinde olması"
            ],
            "correctAnswer": "C",
            "explanation": "Her iki süreçte de trombositler, koagülasyon faktörleri (trombin, fibrin) ve endotel rol oynar. Ancak hemostaz vasküler hasara lokalize ve kontrollü fizyolojik yanıt iken; tromboz, damar içinde kontrolsüz ve uygunsuz gelişerek lümeni tıkayan patolojik bir süreçtir."
        }
    },

    # SLIDE 2
    {
        "id": "slide-2",
        "title": "Normal Hemostazın Dört Evresi ve Kronolojik Akışı",
        "subtitle": "Vasküler yaralanma anından pıhtının sınırlandırılmasına kadar gerçekleşen 4 basamak",
        "content": """**HEMOSTAZIN BASAMAKLARI (ŞEKİL 3.5)**
Damar duvarında bir zedelenme meydana geldiğinde hemostaz son derece koordineli 4 aşamada ilerler:

1. **Evre 1: Arteriyel Vazokonstriksiyon:**
   - Yaralanmanın hemen ardından saniyeler içinde gelişir. Kan akımını geçici olarak azaltır.
2. **Evre 2: Primer Hemostaz (Trombosit Tıkacı):**
   - Subendotelyal ekstrasellüler matriks (kollajen) ve von Willebrand Faktörü (vWF) açığa çıkar. Trombositler yapışır (adezyon), aktive olur, salgı yapar ve birleşerek gevşek **primer trombosit tıkacını** oluşturur.
3. **Evre 3: Sekonder Hemostaz (Fibrin Ağı Oluşumu):**
   - Hasar bölgesinde Doku Faktörü (Tromboplastin / Faktör III) açığa çıkar. Koagülasyon kaskadı tetiklenerek **trombin** üretilir; trombin fibrinojeni fibrine çevirir. Trombosit tıkacı fibrin ağı ile zırh gibi sağlamlaşır.
4. **Evre 4: Pıhtı Stabilizasyonu ve Çözülme (Fibrinoliz):**
   - Faktör XIII fibrini çapraz bağlarla kovalent bağlar. Trombosit tıkacı büzülür. Eş zamanlı olarak t-PA ve plazmin devreye girerek pıhtının gereksiz büyümesini engeller ve tamir sonrası pıhtıyı eritir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Kronolojik Sıralama:**\n  ▫ 1. Saniyeler: ==Arteriyel Vazokonstriksiyon== (Nörojenik + Endotelin)\n  ▫ 2. İlk dakikalar: ==Primer Hemostaz== (Trombosit tıkacı)\n  ▫ 3. Dakikalar: ==Sekonder Hemostaz== (Doku faktörü → Koagülasyon → Fibrin)\n  ▫ 4. Saatler/Günler: ==Pıhtı Stabilizasyonu ve Fibrinoliz== (FXIII çapraz bağlama + t-PA/Plazmin)",
            "🔵 ÇIKMIŞ SORU:\n▸ **Sınav Sorusu:**\n  ▫ *Vasküler hasar sonrasında en erken devreye giren ve ilk saniyelerde kan kaybını geçici azaltan mekanizma nedir?* → **Arteriyel vazokonstriksiyon** (Endotelin ve lokal nörojenik refleksler)."
        ],
        "flashcards": [
            {
                "question": "Hemostazın dört ana evresi sırasıyla nelerdir?",
                "answer": "1) Arteriyel Vazokonstriksiyon, 2) Primer Hemostaz (Trombosit tıkacı), 3) Sekonder Hemostaz (Fibrin ağı oluşumu), 4) Pıhtı Stabilizasyonu ve Fibrinoliz."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q2",
            "question": "Damar duvarında meydana gelen akut bir travma sonrasında hemostatik yanıtın ilk saniyelerinde gözlenen ve kan kaybını geçici olarak yavaşlatan ilk basamak aşağıdakilerden hangisidir?",
            "options": [
                "A) Faktör XIII aracılı fibrin çapraz bağlanması",
                "B) Nörojenik refleksler ve endotelin salınımıyla oluşan arteriyel vazokonstriksiyon",
                "C) Plazminojenin t-PA ile plazmine dönüştürülmesi",
                "D) Doku faktörünün Faktör VII ile kompleks oluşturması",
                "E) GpIIb/IIIa reseptörleri aracılığıyla fibrinojen köprülerinin kurulması"
            ],
            "correctAnswer": "B",
            "explanation": "Damar hasarının hemen ardından ilk saniyelerde gelişen ilk hemostatik basamak lokal nörojenik refleksler ve endotelden salınan endotelin etkisiyle oluşan geçici arteriyel vazokonstriksiyondur."
        }
    },

    # SLIDE 3
    {
        "id": "slide-3",
        "title": "Basamak 1: Arteriyel Vazokonstriksiyon & Endotelin Dinamikleri",
        "subtitle": "İlk saniyelerdeki nörojenik refleksler, endotelin peptidi ve vazokonstriksiyonun sınırları",
        "content": """**ARTERYEL VAZOKONSTRİKSİYONUN DETAYLARI**
Travmatik damar yaralanmasının hemen ardından lokal kan akımını acilen azaltmak için arteriyel düz kaslar kasılır.

1. **Tetikleyici Mekanizmalar:**
   - **Lokal nörojenik refleksler:** Ağrı ve mekanik gerilme reseptörlerinin uyarılmasıyla sempatik vazomotor yanıt.
   - **Endotelin:** Hasarlı endotel hücreleri tarafından sentezlenen ve salgılanan 21 amino asitlik, bilinen en güçlü endojen vazokonstriktör peptid.

2. **Fizyolojik Önemi ve Sınırları:**
   - Hasarlı bölgeye gelen kan debisini geçici olarak düşürerek trombositlerin ve pıhtılaşma faktörlerinin yıkanıp sürüklenmesini önler.
   - **Geçicidir:** Vazokonstriksiyon dakikalar içinde zayıflar; bu nedenle kanamanın kalıcı durdurulması için acilen primer ve sekonder hemostaz devreye girmelidir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Vazokonstriksiyon Özellikleri:**\n  ▫ **Endotelin:** Endotelyal hasarla salınan en güçlü lokal vazokonstriktör peptid.\n  ▫ **Süreç Geçicidir:** Tek başına vazokonstriksiyon kanamayı durduramaz; sadece hemostatik bileşenlerin hasar bölgesinde toplanabilmesi için zaman kazandırır.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite Sorusu:**\n  ▫ *Vasküler hasar sonrası arteriyel vazokonstriksiyondan sorumlu en güçlü endotel kaynaklı lokal mediyatör hangisidir?* → **Endotelin**."
        ],
        "flashcards": [
            {
                "question": "Damar hasarında arteriyel vazokonstriksiyondan sorumlu güçlü endotel kaynaklı peptid nedir?",
                "answer": "Endotelin."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q3",
            "question": "Hemostazın ilk basamağı olan arteriyel vazokonstriksiyon ile ilgili olarak aşağıdakilerden hangisi yanlıştır?",
            "options": [
                "A) Lokal nörojenik refleksler tarafından tetiklenir.",
                "B) Hasarlı endotelden salınan güçlü vazokonstriktör peptit olan endotelin rol oynar.",
                "C) Hasarlı bölgedeki lokal kan akımını geçici olarak azaltır.",
                "D) Tek başına kalıcı hemostazı sağlamak için yeterlidir ve fibrinolizi engeller.",
                "E) Trombositlerin hasarlı yüzeye tutunabilmesi için uygun hemodinamik ortam hazırlar."
            ],
            "correctAnswer": "D",
            "explanation": "Arteriyel vazokonstriksiyon geçici bir yanıttır. Tek başına kalıcı hemostazı sağlayamaz; trombosit ve koagülasyon faktörleri devreye girmezse dakikalar içinde kanama yeniden şiddetlenir."
        }
    },

    # SLIDE 4
    {
        "id": "slide-4",
        "title": "Basamak 2: Primer Hemostaz ve Trombosit Biyolojisi",
        "subtitle": "Kemik iliği megakaryositlerinden köken alan çekirdeksiz disklerin granül içeriği",
        "content": """**TROMBOSİTLERİN YAPISI VE GRANÜLLERİ**
Trombositler, kemik iliğindeki megakaryositlerin sitoplazmik uzantılarından koparak dolaşıma giren 1.5-3 µm çapında, çekirdeksiz disklerdir. Ömürleri 7-10 gündür.

1. **Glikoprotein Reseptörleri (Glikokaliks):**
   - **GpIb (Glikoprotein Ib-IX-V):** vWF'ye bağlanarak adezyonu sağlar.
   - **GpIIb/IIIa (İntegrin αIIbβ3):** Fibrinojene bağlanarak agregasyonu sağlar.
   - **PAR (Proteaz-aktive reseptörler - PAR-1, PAR-4):** Trombin ile güçlü şekilde aktive olur.

2. **Trombosit İçi Granül Tipleri:**
   - **Alfa (α) Granülleri:** Protein içerir.
     - P-selektin (adhezyon molekülü, aktivasyonda zara taşınır)
     - Fibrinojen, Fibronektin
     - Faktör V ve Faktör VIII
     - PDGF (Trombosit kaynaklı büyüme faktörü - fibroblast proliferasyonu)
     - TGF-β
   - **Yoğun / Delta (δ) Granülleri:** Küçük moleküller içerir.
     - ADP (Adenozin difosfat - güçlü trombosit aktivatörü)
     - ATP
     - İyonize Kalsiyum ($Ca^{2+}$ - koagülasyon kaskadı için şarttır!)
     - Serotonin (5-HT - vazokonstriktör)
     - Epinefrin""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Granül İçeriklerinin Ayrımı:**\n  ▫ ==Alfa Granülleri:== Proteinler → *Fibrinojen, Faktör V, Faktör VIII, vWF, PDGF, TGF-β, P-selektin*.\n  ▫ ==Yoğun (Delta) Granülleri:== Küçük moleküller → *ADP, ATP, Kalsiyum ($Ca^{2+}$), Serotonin, Histamin*.\n  ▫ Kalsiyum ($Ca^{2+}$) koagülasyon enzim komplekslerinin montajı için vazgeçilmezdir!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Soruları:**\n  ▫ *Aşağıdakilerden hangisi trombositlerin yoğun (delta) granüllerinde yer alır?* → **ADP, Serotonin, Kalsiyum** (P-selektin, PDGF ve Fibrinojen alfa granüllerindedir!)."
        ],
        "flashcards": [
            {
                "question": "Trombositlerin alfa granüllerinde ve yoğun (delta) granüllerinde bulunan temel moleküller nelerdir?",
                "answer": "Alfa: Fibrinojen, FV, FVIII, vWF, PDGF, TGF-β, P-selektin. Yoğun (Delta): ADP, ATP, Kalsiyum (Ca2+), Serotonin."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q4",
            "question": "Trombosit aktivasyonu sırasında salgılanan granüller ve içerikleri eşleştirildiğinde, aşağıdakilerden hangisi 'yoğun (delta) granüller' içerisinde yer alan temel bileşenlerden biridir?",
            "options": [
                "A) Trombosit kaynaklı büyüme faktörü (PDGF)",
                "B) P-selektin adhezyon molekülü",
                "C) İyonize Kalsiyum ($Ca^{2+}$) ve ADP",
                "D) Faktör V ve Faktör VIII",
                "E) Fibrinojen ve fibronektin"
            ],
            "correctAnswer": "C",
            "explanation": "Trombositlerin yoğun (delta) granülleri ADP, ATP, Serotonin ve Kalsiyum içerir. PDGF, P-selektin, Faktör V, Faktör VIII ve fibrinojen ise alfa granüllerinde depolanır."
        }
    },

    # SLIDE 5
    {
        "id": "slide-5",
        "title": "Trombosit Adhezyonu ve Aktivasyonu: vWF - GpIb Aksı",
        "subtitle": "Subendotelyal kollajen ile etkileşim, şekil değişikliği ve Bernard-Soulier Sendromu",
        "content": """**TROMBOSİT ADHEZYONU VE AKTİVASYONU**
Endotel hasar gördüğünde subendotelyal ekstrasellüler matriks (kollajen) doğrudan kana maruz kalır.

1. **Adhezyon (Yapışma) Mekanizması:**
   - Yüksek akım hızlarında (arterlerdeki yüksek 'shear stress') trombositlerin doğrudan kollajene tutunması zordur.
   - Endotelden ve plazmadan gelen **von Willebrand Faktörü (vWF)**, subendotelyal kollajene bağlanır.
   - Trombosit yüzeyindeki **Glikoprotein Ib (GpIb)** reseptörü, vWF'ye kilitlenerek trombositi hasarlı yüzeye çimler gibi yapıştırır.
   - **Bernard-Soulier Sendromu:** GpIb reseptörünün konjenital eksikliğidir; trombositler subendotele yapışamaz. Periferik yaymada **dev trombositler (makrotrombositopeni)** ve kanama diyatezi görülür.

2. **Aktivasyon ve Şekil Değişikliği:**
   - Adezyonu takiben trombosit disk şeklinden çok kollu, dikenimsi (**psödopodlu**) bir yapıya dönüşür.
   - Bu şekil değişikliği yüzey alanını dramatik artırır ve negatif yüklü fosfolipitleri (fosfatidilserin) hücre zarı dışına çevirerek koagülasyon faktör kompleksleri için şasi oluşturur.
   - Granül salgılanması başlar: ADP ve Tromboksan A2 (TxA2) sentezlenip dışarı atılır.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Adhezyon Çifti ve Hastalığı:**\n  ▫ Subendotelyal Bağlantı: ==vWF + GpIb==\n  ▫ **Bernard-Soulier Sendromu:** GpIb reseptör eksikliği → Adhezyon bozukluğu, dev trombositler, trombositopeni.\n  ▫ **von Willebrand Hastalığı:** vWF eksikliği/defekti → En sık kalıtsal kanama bozukluğu.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Trombosit yüzeyinde bulunan Glikoprotein Ib (GpIb) reseptörünün doğuştan eksikliği ile karakterize, dev trombositlerin eşlik ettiği adezyon bozukluğu hastalığı hangisidir?* → **Bernard-Soulier Sendromu**."
        ],
        "flashcards": [
            {
                "question": "Trombositlerin subendotelyal kollajene yapışmasını sağlayan reseptör ve köprü molekül nedir? Eksikliğinde ne görülür?",
                "answer": "Reseptör: GpIb, Köprü: vWF (von Willebrand Faktörü). GpIb eksikliğinde Bernard-Soulier Sendromu (adezyon kusuru, dev trombositler) görülür."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q5",
            "question": "Damar duvarı hasar gördüğünde yüksek akım hızlarında trombositlerin subendotelyal kollajene adezyonunu sağlayan yüzey reseptörü ve bu reseptörün konjenital eksikliğinde ortaya çıkan klinik sendrom aşağıdakilerden hangisinde doğru eşleştirilmiştir?",
            "options": [
                "A) GpIIb/IIIa - Glanzmann Trombastenisi",
                "B) GpIb - Bernard-Soulier Sendromu",
                "C) P2Y12 - von Willebrand Hastalığı",
                "D) PAR-1 - Trousseau Sendromu",
                "E) Fibrinojen reseptörü - Faktör V Leiden"
            ],
            "correctAnswer": "B",
            "explanation": "Trombositlerin subendotelyal vWF'ye tutunarak adezyon yapmasını sağlayan reseptör GpIb (Glikoprotein Ib-IX-V) kompleksidir ve konjenital eksikliği Bernard-Soulier Sendromu'na yol açar."
        }
    },

    # SLIDE 6
    {
        "id": "slide-6",
        "title": "Trombosit Agregasyonu: GpIIb/IIIa Kompleksi ve Glanzmann Trombastenisi",
        "subtitle": "Trombositlerin birbirine bağlanması, fibrinojen köprüleri ve antitrombositik ilaç hedefleri",
        "content": """**TROMBOSİT AGREGASYONU VE FİBRİNOJEN KÖPRÜLERİ**
Aktivasyon sonucu salınan **ADP** ve **Tromboksan A2 (TxA2)**, çevredeki diğer trombositleri de ortama çeker (amplifikasyon).

1. **GpIIb/IIIa Reseptörünün Konformasyonel Değişimi:**
   - Dinlenme halindeki trombositlerde GpIIb/IIIa (αIIbβ3 integrin) inaktiftir.
   - ADP (P2Y12 reseptörü üzerinden) ve TxA2 uyarılarıyla hücre içi sinyal iletimi gerçekleşir ('inside-out signaling') ve GpIIb/IIIa aktive konformasyona geçer.
   - Aktive GpIIb/IIIa, plazmadaki bivalan (iki uçlu) bir molekül olan **fibrinojene** kuvvetle bağlanır.
   - Fibrinojen, iki ayrı trombositin GpIIb/IIIa reseptörlerini birbirine köprüleyerek trombositlerin kümeleşmesini (**agregasyon**) sağlar.

2. **Glanzmann Trombastenisi:**
   - GpIIb/IIIa reseptör kompleksinin otozomal resesif kalıtsal eksikliğidir.
   - Trombosit adezyonu normaldir (GpIb sağlamdır), ancak trombositler birbirine bağlanamaz (agregasyon kusuru). Şiddetli mukokutanöz kanamalarla seyreder.

3. **Klinik ve Farmakolojik Hedefler:**
   - **Aspirin:** Siklooksijenaz-1'i (COX-1) geri dönüşümsüz inhibe ederek TxA2 sentezini engeller.
   - **Klopidogrel / Prasugrel / Tikagrelor:** Trombosit P2Y12 (ADP) reseptörünü bloke eder.
   - **Absiksimab, Tirofiban, Eptifibatid:** GpIIb/IIIa reseptörünü doğrudan bloke eder.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Agregasyon Özeti:**\n  ▫ Agregasyon Köprüsü: ==Fibrinojen== (bazen vWF de bağlanabilir).\n  ▫ Reseptör: ==GpIIb/IIIa (αIIbβ3)==\n  ▫ **Glanzmann Trombastenisi:** GpIIb/IIIa eksikliği → Agregasyon defekti, kanama zamanı uzar.\n  ▫ **Farmakoloji:** Klopidogrel (P2Y12 ADP blokeri), Aspirin (COX-1 / TxA2 inhibitörü), Absiksimab (GpIIb/IIIa blokeri).",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Trombosit agregasyonunda komşu trombositler arasında köprü kurarak bağlanmayı sağlayan plazma proteini ve trombosit yüzey reseptörü hangisidir?* → **Fibrinojen ve GpIIb/IIIa reseptörü**."
        ],
        "flashcards": [
            {
                "question": "Glanzmann trombastenisinde eksik olan yüzey reseptörü ve fonksiyonel kusur nedir?",
                "answer": "GpIIb/IIIa (αIIbβ3 integrin) reseptörü eksiktir; fibrinojen köprüleri kurulamaz ve trombosit agregasyonu bozulur."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q6",
            "question": "Trombositlerin birbirine bağlanarak agregasyon oluşturmasında rol oynayan GpIIb/IIIa reseptörünün konjenital eksikliği sonucu gelişen, kanama zamanının uzadığı ancak trombosit adezyonunun korunduğu hastalık aşağıdakilerden hangisidir?",
            "options": [
                "A) Bernard-Soulier Sendromu",
                "B) von Willebrand Hastalığı",
                "C) Glanzmann Trombastenisi",
                "D) Hemofili A",
                "E) Faktör V Leiden Mutasyonu"
            ],
            "correctAnswer": "C",
            "explanation": "Glanzmann trombastenisi GpIIb/IIIa reseptörünün eksikliği sonucu gelişir; trombosit agregasyonu bozulurken adezyon (GpIb) korunur."
        }
    },

    # SLIDE 7
    {
        "id": "slide-7",
        "title": "Basamak 3: Sekonder Hemostaz ve Koagülasyon Kaskadı",
        "subtitle": "Zimojen proenzimlerin ardışık proteolitik aktivasyonu ve pıhtılaşma faktörleri",
        "content": """**KOAGÜLASYON KASKADININ TEMEL MİMARİSİ**
Primer hemostazla oluşan trombosit tıkacı gevşektir ve kan akımının hidrodinamik gücüyle kolayca yerinden sökülebilir. Sekonder hemostaz, bu tıkacın üzerine çözünmeyen **fibrin zırhı** örerek pıhtıyı mekanik olarak sağlamlaştırır.

1. **Pıhtılaşma Faktörlerinin Doğası:**
   - Faktörlerin çoğu karaciğerde sentezlenen inaktif proenzimlerdir (zimojenler).
   - Bir faktör aktifleştiğinde (örn. Faktör X → Faktör Xa), bir sonraki proenzimi sınırlı proteoliz yoluyla parçalayarak aktif enzim haline getirir.
   - Kaskadın her basamağı sinyali katlanarak büyütür (enzimatik amplifikasyon).

2. **Enzim Kompleksinin Montajı İçin 3 Gereksinim:**
   - Her majör basamakta 3 bileşen bir araya gelmelidir:
     1. **Bir Enzim** (örn. Faktör IXa)
     2. **Bir Substrat** (örn. Faktör X)
     3. **Bir Kofaktör** (örn. Faktör VIIIa)
   - Bu kompleks, aktive trombositlerin yüzeyinde dışa dönmüş **negatif yüklü fosfolipitler** üzerinde ve **Kalsiyum ($Ca^{2+}$)** iyonları aracılığıyla kurulur.
   - K Vitamini: Faktör II, VII, IX, X, Protein C ve Protein S'nin glutamik asit kalıntılarının $\gamma$-karboksillenmesi için zorunludur. $\gamma$-karboksillenme olmazsa kalsiyum bağlanamaz ve pıhtılaşma gerçekleşemez!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **K Vitaminine Bağımlı Faktörler:**\n  ▫ ==1972 Faktörleri:== **Faktör X (10), Faktör IX (9), Faktör VII (7), Faktör II (Protrombin)**.\n  ▫ Doğal antikoagülanlar: **Protein C ve Protein S**.\n  ▫ Warfarin (Kumadin): Karaciğerde Epoksit Redüktazı inhibe ederek K vitaminini baskılar; bu faktörler fonksiyonel üretilemez.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Sınav Sorusu:**\n  ▫ *Koagülasyon kaskadında enzim komplekslerinin trombosit fosfolipit yüzeyine montajı için mutlak gerekli olan iyon hangisidir?* → **Kalsiyum ($Ca^{2+}$ - Faktör IV)**."
        ],
        "flashcards": [
            {
                "question": "K vitaminine bağımlı koagülasyon faktörleri ve doğal antikoagülanlar hangileridir?",
                "answer": "Faktör II, VII, IX, X (1972) ile Protein C ve Protein S."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q7",
            "question": "Koagülasyon kaskadında enzim, substrat ve kofaktör komplekslerinin aktive trombosit zarı üzerindeki negatif yüklü fosfolipit yüzeyine bağlanabilmesi için aşağıdakilerden hangisi mutlak gereklidir?",
            "options": [
                "A) Magnezyum ($Mg^{2+}$) iyonları",
                "B) İyonize Kalsiyum ($Ca^{2+}$) iyonları ve gama-karboksillenmiş glutamat kalıntıları",
                "C) Heparan sülfat proteoglikanları",
                "D) Nitrik oksit (NO)",
                "E) Prostasiklin (PGI2)"
            ],
            "correctAnswer": "B",
            "explanation": "K vitamini bağımlı faktörlerin fosfolipid yüzeylere tutunabilmesi, gama-karboksilasyon sayesinde Kalsiyum (Ca2+) iyon köprüleri kurabilmelerine bağlıdır."
        }
    },

    # SLIDE 8
    {
        "id": "slide-8",
        "title": "Koagülasyon Yollarının İn Vitro Analizi: PT vs. aPTT",
        "subtitle": "Ekstrinsik, intrinsik ve ortak yolun laboratuvar testleri ve izleme parametreleri",
        "content": """**İN VİTRO KOAGÜLASYON TESTLERİ: PT VE aPTT**
Geleneksel laboratuvar sınıflamasında koagülasyon kaskadı ekstrinsik, intrinsik ve ortak yol olarak üçe ayrılır.

1. **Protrombin Zamanı (PT / INR) – Ekstrinsik ve Ortak Yol:**
   - Plazmaya **Doku Faktörü (Tromboplastin)**, fosfolipid ve kalsiyum eklenerek pıhtılaşma süresi ölçülür.
   - **Değerlendirilen Faktörler:** Ekstrinsik yolun anahtar enzimi olan **Faktör VII** ile ortak yol faktörleri (**Faktör X, V, II/Protrombin ve Fibrinojen**).
   - Klinik Kullanım: Karaciğer sentez kapasitesi, K vitamini eksikliği ve **Warfarin (Kumadin)** tedavisinin takibi (INR hedefi: 2.0-3.0). En kısa yarı ömürlü faktör Faktör VII olduğu için PT hızla uzar.

2. **Aktive Parsiyel Tromboplastin Zamanı (aPTT) – İntrinsik ve Ortak Yol:**
   - Plazmaya negatif yüklü bir yüzey aktivatörü (kaolin, silika), fosfolipid ve kalsiyum eklenerek ölçülür.
   - **Değerlendirilen Faktörler:** İntrinsik yol faktörleri (**Faktör XII, XI, IX, VIII**) ve ortak yol faktörleri (**Faktör X, V, II, Fibrinojen**).
   - Klinik Kullanım: **Standart (Fraksiyone Olmayan) Heparin** tedavisinin takibi, Hemofili A (FVIII eksikliği), Hemofili B (FIX eksikliği) ve Lupus Antikoagülanı araştırması.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Laboratuvar Eşleştirmesi:**\n  ▫ ==PT / INR:== Ekstrinsik yol → **Faktör VII** + Ortak yol. (Warfarin takibi).\n  ▫ ==aPTT:== İntrinsik yol → **Faktör XII, XI, IX, VIII** + Ortak yol. (Heparin takibi, Hemofili A/B).\n  ▫ ==Ortak Yol:== **Faktör X, V, II (Protrombin), I (Fibrinojen)**. Hem PT hem aPTT'yi uzatır!",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Oral antikoagülan Warfarin kullanan bir hastada tedavi etkinliğini takip etmek için hangi test kullanılır ve hangi faktörün hızla tükenmesine bağlıdır?* → **PT (INR)** ve **Faktör VII** (en kısa yarı ömürlü faktör)."
        ],
        "flashcards": [
            {
                "question": "PT ve aPTT testleri koagülasyon kaskadının hangi yollarını ve faktörlerini değerlendirir?",
                "answer": "PT: Ekstrinsik yol (Faktör VII) ve ortak yol (X, V, II, I). aPTT: İntrinsik yol (Faktör XII, XI, IX, VIII) ve ortak yol (X, V, II, I)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q8",
            "question": "Hemofili A (Faktör VIII eksikliği) tanısı olan bir hastanın koagülasyon testleri değerlendirildiğinde aşağıdakilerden hangisinin görülmesi beklenir?",
            "options": [
                "A) Yalnızca PT uzamıştır, aPTT normaldir.",
                "B) Yalnızca aPTT uzamıştır, PT normaldir.",
                "C) Hem PT hem aPTT belirgin uzamıştır.",
                "D) Kanama zamanı uzamıştır, PT ve aPTT normaldir.",
                "E) Fibrinojen düzeyi sıfıra inmiştir."
            ],
            "correctAnswer": "B",
            "explanation": "Faktör VIII intrinsik yolun bileşenidir. Eksikliğinde (Hemofili A) intrinsik yolu ölçen aPTT uzarken, ekstrinsik yolu ölçen PT normal kalır."
        }
    },

    # SLIDE 9
    {
        "id": "slide-9",
        "title": "İn Vivo Koagülasyon ve Trombinin (Faktör IIa) Çift Yönlü Rolü",
        "subtitle": "Doku faktörüyle başlayan fizyolojik kaskad ve trombinin hemostaz-antikoagülasyon anahtarı",
        "content": """**İN VİVO GERÇEKLİK VE TROMBİNİN MERKEZİ ROLÜ**
Laboratuvardaki ayrımın aksine, in vivo (canlıda) koagülasyon kaskadı tek bir ana yolla başlar: **Doku Faktörü (TF) - Faktör VIIa Kompleksi**.

1. **İn Vivo Başlama ve Amplifikasyon:**
   - Hasar gören damar duvarından salınan TF, Faktör VII'yi aktive eder.
   - TF-FVIIa kompleksi doğrudan Faktör X'u ve Faktör IX'u aktive eder.
   - Üretilen az miktardaki trombin, geri besleme ile Faktör V, Faktör VIII ve Faktör XI'i aktive ederek kaskadı katlar (**Trombin Patlaması - Thrombin Burst**).

2. **Trombinin (Faktör IIa) Çok Yönlü Fonksiyonları:**
   - **Fibrinojen → Çözünmeyen Fibrin:** Fibrinojenin fibrinopeptid A ve B kısımlarını keserek fibrin monomerleri oluşturur.
   - **Trombosit Aktivasyonu:** PAR-1 ve PAR-4 reseptörleri aracılığıyla trombositleri en güçlü şekilde aktive eder ve granül salgısını tetikler.
   - **Kofaktör Aktivasyonu:** Faktör V ve VIII'i aktive ederek tenaz ve protrombinaz komplekslerini roketler; FXIII'ü aktive ederek pıhtıyı kilitler.
   - **Proenflamatuar Etkiler:** Endotel ve lökositlerde adezyon molekülleri ve kemokin salınımını artırır.
   - **Antikoagülan Dönüşüm (Paradoks / Güvenlik Şalteri):** Sağlam endotelde bulunan **Trombomodulin**'e bağlandığında prokoagülan etkisini tamamen kaybeder ve **Protein C**'yi aktive ederek kaskadı kapatır!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Trombinin Çift Karakteri:**\n  ▫ Prokoagülan Trombin: Fibrinojen → Fibrin, Trombosit PAR aktivasyonu, FV, FVIII, FXIII aktivasyonu.\n  ▫ Antikoagülan Trombin: ==Trombomodulin== ile birleştiğinde **Aktive Protein C (APC)** üretir; bu da FVa ve FVIIIa'yı yıkarak pıhtılaşmayı sonlandırır.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Trombin endotel yüzeyindeki trombomoduline bağlandığında hangi molekülü aktive ederek antikoagülan bir özellik kazanır?* → **Protein C**."
        ],
        "flashcards": [
            {
                "question": "Trombin sağlam endotelde trombomoduline bağlandığında hangi fizyolojik olayı başlatır?",
                "answer": "Protein C'yi aktive eder (APC oluşur); APC, Protein S kofaktörlüğünde Faktör Va ve Faktör VIIIa'yı parçalayarak koagülasyonu frenler."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q9",
            "question": "Hemostazın düzenlenmesinde merkezi bir kavşak olan trombinin prokoagülan etkisini kaybedip antikoagülan bir fonksiyona geçmesini sağlayan mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Faktör XIII ile birleşerek kovalent bağ yapması",
                "B) Sağlam endotel yüzeyindeki trombomoduline bağlanarak Protein C'yi aktive etmesi",
                "C) von Willebrand Faktörü ile kompleks oluşturup trombosit adezyonunu engellemesi",
                "D) Doku faktörünü doğrudan parçalayarak ekstrinsik yolu durdurması",
                "E) Fibrinojeni fibrine dönüştürmeyi tamamen durdurup albümine çevirmesi"
            ],
            "correctAnswer": "B",
            "explanation": "Trombin sağlam endotelde trombomoduline bağlandığında pıhtılaştırıcı özelliklerini kaybeder ve Protein C'yi aktive ederek (APC) FVa ve FVIIIa'yı yıkar; böylece doğal bir antikoagülan şalter görevi görür."
        }
    },

    # SLIDE 10
    {
        "id": "slide-10",
        "title": "Basamak 4: Pıhtı Stabilizasyonu ve Fibrinoliz Kaskadı",
        "subtitle": "Faktör XIII çapraz bağları, t-PA, plazminojen aktivasyonu ve D-Dimer oluşumu",
        "content": """**PIHTI STABİLİZASYONU VE FİBRİNOLİZ**
Trombin fibrinojeni kestiğinde fibrin monomerleri uç uca zayıf hidrojen bağlarıyla dizilir.

1. **Pıhtı Stabilizasyonu (Faktör XIII):**
   - Trombin tarafından aktive edilen **Faktör XIIIa (Fibrin Stabilize Edici Faktör)**, bir transglutaminazdır.
   - Fibrin monomerlerinin glutamin ve lizin amino asitleri arasında **kovalent çapraz bağlar** kurar.
   - Pıhtı proteolitik yıkıma son derece dirençli, sağlam bir jele dönüşür.

2. **Fibrinoliz (Pıhtının Çözülmesi):**
   - Pıhtının kontrolsüz şekilde damar boyunca ilerlemesini önlemek ve doku tamiri sonrasında lümeni açmak için fibrinoliz zorunludur.
   - **Plazminojen → Plazmin:** Endotelden salınan **Doku Plazminojen Aktivatörü (t-PA)**, plazminojeni aktif enzim olan **plazmin**'e dönüştürür.
   - **Plazminin Görevi:** Çapraz bağlı fibrini sindirerek erir hale getirir.
   - **Fibrin Yıkım Ürünleri ve D-Dimer:** Çapraz bağlı fibrinin plazmin tarafından parçalanmasıyla **D-Dimer** açığa çıkar.
   - D-Dimer kanda DVT, Pulmoner Emboli ve DİK (Dissemine İntravasküler Koagülasyon) gibi aktif trombotik süreçlerin taranmasında çok değerli bir negatif prediktif belirteçtir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Fibrinoliz ve Belirteçler:**\n  ▫ **Faktör XIIIa:** Fibrini kovalent çapraz bağlar; pıhtıyı stabil kılar.\n  ▫ **Plazmin:** Fibrin ağını yıkar.\n  ▫ ==D-Dimer:== Sadece **çapraz bağlı (stabil) fibrinin** plazminle yıkılması sonucu oluşur! Fibrinojen yıkımında D-Dimer oluşmaz!\n  ▫ Fibrinoliz İnhibitörleri: PAI-1 (t-PA'yı inhibe eder), Alfa-2 antiplazmin (serbest plazmini inhibe eder).",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *D-Dimer testi vücutta hangi sürecin gerçekleştiğini doğrudan kanıtlar?* → **Faktör XIII ile çapraz bağlanmış fibrin pıhtısının plazmin tarafından eritildiğini** (aktif sekonder hemostaz ve fibrinoliz)."
        ],
        "flashcards": [
            {
                "question": "Kanda yüksek D-Dimer saptanması patofizyolojik olarak neyi gösterir?",
                "answer": "Faktör XIII tarafından kovalent çapraz bağlanmış stabil fibrin pıhtısının plazmin tarafından aktif olarak parçalandığını gösterir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q10",
            "question": "Derin ven trombozu veya pulmoner emboli şüphesi olan bir hastada plazmada ölçülen D-Dimer yüksekliği, biyokimyasal ve patofizyolojik olarak aşağıdakilerden hangisinin doğrudan göstergesidir?",
            "options": [
                "A) Karaciğerde fibrinojen sentezinin durduğunun",
                "B) Çapraz bağlı stabil fibrinin plazmin enzimi tarafından parçalandığının",
                "C) Endotelden endotelin salgısının aşırı arttığının",
                "D) Faktör V Leiden mutasyonunun homozigot olduğunun",
                "E) Yalnızca primer trombosit tıkacının çözündüğünün"
            ],
            "correctAnswer": "B",
            "explanation": "D-Dimer, Faktör XIII ile çapraz bağlanmış stabil fibrin ağının plazmin tarafından proteolitik olarak yıkılmasıyla ortaya çıkan spesifik bir fibrin yıkım ürünüdür."
        }
    },

    # SLIDE 11
    {
        "id": "slide-11",
        "title": "Endotel Hücresinin İkili Doğası: Normal Antitrombotik Kalkan",
        "subtitle": "Sağlam endotelin antitrombositik, antikoagülan ve fibrinolitik savunma mekanizmaları",
        "content": """**ENDOTELİN ANTİTROMBOTİK FONKSİYONLARI**
Sağlam endotel örtüsü, kanın pıhtılaşmasını aktif olarak engelleyen mükemmel bir antitrombotik kalkandır.

1. **Trombosit İnhibitör Etkiler (Antitrombositik):**
   - Sağlam endotel, subendotelyal kollajen ve vWF'yi kandan fiziksel olarak izole eder.
   - **Prostasiklin ($PGI_2$) ve Nitrik Oksit (NO):** Endotelden sürekli salınır. Trombosit adhezyon ve agregasyonunu güçlü şekilde inhibe eder; aynı zamanda güçlü vazodilatörlerdir.
   - **Adenozin Difosfataz (ADPaz / CD39):** Trombositleri aktive eden serbest ADP'yi parçalayarak adenozine çevirir.

2. **Antikoagülan Etkiler:**
   - **Trombomodulin:** Trombin ile birleşerek Protein C'yi aktive eder.
   - **Heparan Sülfat Proteoglikanları:** Endotel yüzeyinde bulunur. Plazmadaki **Antitrombin III (AT-III)**'e bağlanarak onun trombin, Faktör Xa ve Faktör IXa'yı inaktive etme hızını 1000 kat artırır (endojen heparin etkisi!).
   - **TFPI (Doku Faktörü Yolu İnhibitörü):** Endotel yüzeyinde sentezlenir; Doku Faktörü - FVIIa kompleksini ve FXa'yı doğrudan inhibe eder.

3. **Fibrinolitik Etkiler:**
   - Endotel hücreleri **Doku Plazminojen Aktivatörü (t-PA)** sentezleyip salgılayarak damar yüzeyinde oluşan mikropıhtıları anında temizler.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Endotelin Antitrombotik Cephanesi:**\n  ▫ Antitrombositik: ==Prostasiklin ($PGI_2$), Nitrik Oksit (NO), ADPaz (CD39)==\n  ▫ Antikoagülan: ==Trombomodulin, Heparan Sülfat (AT-III aktivatörü), TFPI==\n  ▫ Fibrinolitik: ==t-PA (Doku plazminojen aktivatörü)==\n  ▫ Heparin ilacı, endoteldeki heparan sülfatın Antitrombin III'ü aktive etme mekanizmasını taklit eder!",
            "🔵 ÇIKMIŞ SORU:\n▸ **Sınav Sorusu:**\n  ▫ *Endotel yüzeyinde bulunan ve kanda Antitrombin III'e bağlanarak pıhtılaşma faktörlerinin inaktivasyonunu bin kat hızlandıran endojen molekül hangisidir?* → **Heparan Sülfat**."
        ],
        "flashcards": [
            {
                "question": "Endotel hücresinin trombosit agregasyonunu engelleyen ve vazodilatasyon yapan iki temel endojen salgısı nedir?",
                "answer": "Prostasiklin (PGI2) ve Nitrik Oksit (NO)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q11",
            "question": "Sağlam endotel hücrelerinin yüzeyinde bulunan, plazmadaki Antitrombin III ile etkileşime girerek trombin ve Faktör Xa'nın inaktivasyon hızını bin kat artıran endotelyal molekül aşağıdakilerden hangisidir?",
            "options": [
                "A) Trombospondin",
                "B) von Willebrand Faktörü",
                "C) Heparan Sülfat Proteoglikanları",
                "D) Fibronektin",
                "E) Doku Faktörü (Tromboplastin)"
            ],
            "correctAnswer": "C",
            "explanation": "Endotel yüzeyindeki heparan sülfat proteoglikanları kofaktör olarak davranarak Antitrombin III'ün konformasyonunu değiştirir ve trombin ile Faktör Xa'yı hızla nötralize etmesini sağlar."
        }
    },

    # SLIDE 12
    {
        "id": "slide-12",
        "title": "Trombozun Etiyopatogenezi: Virchow Üçlüsü (Triad of Virchow)",
        "subtitle": "Rudolf Virchow'un 1856'da tanımladığı üç ana patolojik sütun ve etkileşimleri",
        "content": """**VİRCHOW ÜÇLÜSÜ (TRIAD OF VIRCHOW)**
Tromboz oluşumunun altında yatan üç temel anormallik ilk kez 1856'da Rudolf Virchow tarafından tanımlanmıştır:

1. **Endotel Hasarı / Disfonksiyonu (En Kritik Bileşen):**
   - Tek başına arteriyel ve kardiyak trombozu başlatmak için yeterlidir.
   - Aterosklerotik plak yırtılması, vaskülit, hipertansiyon, sigara dumanı ve hiperkolesterolemi endoteli bozar.

2. **Anormal Kan Akımı (Staz ve Türbülans):**
   - **Staz (Yavaşlama/Durgunluk):** Özellikle venöz sistemde (derin venlerde) ve anevrizmalarda temel faktördür.
   - **Türbülans (Girdaplı Akım):** Arteriyel bifurkasyonlarda, stenotik kapaklarda ve anevrizmalarda endotel hasarını tetikler.

3. **Hiperkoagülabilite (Trombofili):**
   - Kanın pıhtılaşma eğiliminin kalıtsal veya edinsel olarak anormal derecede artmasıdır.
   - Özellikle venöz trombozlarda (DVT) klinik tabloyu yönlendirir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Virchow Üçlüsü Bileşenleri:**\n  ▫ 1. ==Endotel Hasarı== (Arteriyel/kardiyak trombozda 1 numaralı neden!)\n  ▫ 2. ==Anormal Kan Akımı== (Staz: venöz trombozda 1 numara; Türbülans: endotel hasarı yapar)\n  ▫ 3. ==Hiperkoagülabilite== (Trombofili - kanda artmış koagülasyon eğilimi)\n  ▫ Bu üç bileşen tek başına veya bir arada bulunarak trombozu tetikler.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Virchow üçlüsünde arteriyel ve intrakardiyak trombozun en sık ve en önemli nedeni hangisidir?* → **Endotel hasarı** (Venöz trombozda ise staz ve hiperkoagülabilite öne çıkar)."
        ],
        "flashcards": [
            {
                "question": "Virchow üçlüsünü oluşturan 3 patofizyolojik bileşen nedir?",
                "answer": "1) Endotel Hasarı, 2) Anormal Kan Akımı (Staz ve Türbülans), 3) Hiperkoagülabilite (Trombofili)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q12",
            "question": "Tromboz patofizyolojisinde Virchow üçlüsünü oluşturan üç temel bileşenden arteriyel ve intrakardiyak trombüs gelişiminde en sık primer tetikleyici olan faktör aşağıdakilerden hangisidir?",
            "options": [
                "A) Venöz staz",
                "B) Endotel hasarı ve disfonksiyonu",
                "C) Antitrombin III fazlalığı",
                "D) Eritrosit sayısının azalması",
                "E) Hipotansiyon"
            ],
            "correctAnswer": "B",
            "explanation": "Arteriyel ve kardiyak sistemde kan akımı çok hızlıdır; bu nedenle trombüsün tutunabilmesi için endotel hasarı (ateroskleroz, enfarktüs skarı, vaskülit) primer ve en kritik başlatıcı faktördür."
        }
    },

    # SLIDE 13
    {
        "id": "slide-13",
        "title": "Virchow 1: Endotel Hasarı ve Protrombotik Endotel Aktivasyonu",
        "subtitle": "Fiziksel soyulmadan biyokimyasal disfonksiyona: Prokoagülan fenotip değişimi",
        "content": """**ENDOTEL HASARI VE AKTİVASYONU**
Endotel hasarı sadece endotelin fiziksel olarak soyulup subendotelyal matriksin açığa çıkması (denüdasyon) demek değildir; biyokimyasal olarak aktive olup protrombotik hale gelmesini de kapsar.

1. **Fiziksel Endotel Hasarı:**
   - Miyokard enfarktüsü sonrası endokard hasarı, ülseröz aterosklerotik plak rüptürü, vaskülitler, travma.
   - Kollajen ve vWF doğrudan kanla temas eder; trombosit adezyonu ve Doku Faktörü açığa çıkarak trombüs oluşur.

2. **Endotel Aktivasyonu / Disfonksiyonu (Biyokimyasal Hasar):**
   - Fiziksel kayıp olmasa dahi; sigara toksinleri, hiperkolesterolemi (LDL oksidasyonu), hipertansiyon, hiperhomosisteinemi, sitokinler (TNF, IL-1) ve endotoksinler endotel hücresini 'protrombotik' yöne kaydırır:
   - **Prokoagülan Gen İfadesi:** Doku faktörü (TF) sentezi artar; vWF salınımı artar.
   - **Antikoagülan Fonksiyon Kaybı:** Trombomodulin düzeyi azalır, heparan sülfat azalır, TFPI baskılanır.
   - **Antifibrinolitik Etki:** t-PA salgısı azalırken PAI-1 (plazminojen aktivatör inhibitörü-1) salgısı artar.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Endotel Aktivasyonunun Protrombotik Özeti:**\n  ▫ Prokoagülanlar ↑: ==Doku Faktörü (TF), vWF== artar.\n  ▫ Antikoagülanlar ↓: ==Trombomodulin, Heparan Sülfat== azalır (Protein C aktive edilemez!).\n  ▫ Antifibrinolitik ↑: ==PAI-1== artar, t-PA baskılanır (pıhtı eritilemez!).",
            "🔵 ÇIKMIŞ SORU:\n▸ **Sınav Sorusu:**\n  ▫ *Ateroskleroz ve endotoksemi zemininde aktive olan endotelde hangisi gözlenir?* → **Doku faktörü ve PAI-1 salınımının artması, trombomodulin ekspresyonunun azalması**."
        ],
        "flashcards": [
            {
                "question": "Endotel aktivasyonu (disfonksiyonu) sırasında prokoagülan ve antifibrinolitik dengede ne tür değişimler olur?",
                "answer": "Doku Faktörü (TF), vWF ve PAI-1 sentezi artar; Trombomodulin, heparan sülfat ve t-PA ekspresyonu azalır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q13",
            "question": "İnflamatuar sitokinler (TNF, IL-1) veya sigara dumanı etkisiyle aktive olan endotel hücresinde gözlenen fenotipik değişikliklerle ilgili aşağıdakilerden hangisi yanlıştır?",
            "options": [
                "A) Yüzeyinde Doku Faktörü (TF) ekspresyonu artar.",
                "B) PAI-1 (plazminojen aktivatör inhibitörü) salgısını artırarak fibrinolizi baskılar.",
                "C) Trombomodulin ekspresyonunu azaltarak Protein C aktivasyonunu düşürür.",
                "D) Nitrik oksit ve prostasiklin salgısını aşırı artırarak pıhtılaşmayı kalıcı olarak imkansız kılar.",
                "E) von Willebrand Faktörü (vWF) salgısını artırır."
            ],
            "correctAnswer": "D",
            "explanation": "Aktive ve hasarlı endotelde koruyucu olan Prostasiklin (PGI2) ve Nitrik Oksit (NO) üretimi azalır; endotel protrombotik (pıhtılaşmayı kolaylaştırıcı) bir fenotipe bürünür."
        }
    },

    # SLIDE 14
    {
        "id": "slide-14",
        "title": "Virchow 2: Anormal Kan Akımı Dinamikleri: Staz ve Türbülans",
        "subtitle": "Normal laminer akımın bozulması, aksiyal akış kaybı ve marjinasyon",
        "content": """**ANORMAL KAN AKIMI: STAZ VE TÜRBÜLANS**
Normal damarlarda kan **laminer** akar: Şekilli elemanlar (eritrositler, lökositler, trombositler) lümenin merkezinde (aksiyal akım), plazma ise damar duvarına komşu yavaş akan bir kılıf halinde hareket eder.

1. **Türbülans (Girdaplı Akım):**
   - Karşılaşılan endotelyal çıkıntılar, aterosklerotik plaklar, arteriyel çatallanmalar (bifurkasyon) ve anevrizmalarda görülür.
   - **Mekanizma:** Girdaplar doğrudan endotel aşınmasına/hasarına yol açar ve lokal staz cepleri oluşturur.

2. **Staz (Kan Akımının Yavaşlaması / Durgunluk):**
   - Özellikle venöz dolaşımda (uzun süre yatak istirahati, alçılı bacak, uzun uçak yolculukları), varislerde, kalp yetmezliğinde ve atriyal fibrilasyonda görülür.
   - **Mekanizma 1 (Marjinasyon):** Aksiyal akım bozulur; trombositler plazma kılıfını aşarak endotel yüzeyine çarpar ve temas eder (marjinasyon).
   - **Mekanizma 2 (Konsantrasyon):** Aktive olmuş pıhtılaşma faktörleri taze kan akımıyla seyreltilip karaciğere taşınamaz; hasar bölgesinde yoğunlaşır.
   - **Mekanizma 3 (Antikoagülan Yetersizliği):** Doğal pıhtılaşma inhibitörlerinin ortama gelişi gecikir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Staz ve Türbülansın Sonuçları:**\n  ▫ Laminer akım bozulunca: Trombositler duvara yaklaşır (==Marjinasyon==).\n  ▫ Aktive pıhtılaşma faktörleri taze kanla yıkanamaz (konsantre olur).\n  ▫ Doğal antikoagülanların ortama girişi engellenir.\n  ▫ Endotel hücre aktivasyonu tetiklenir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Venöz tromboz patogenezinde en sık görülen ve trombositlerin endotel yüzeyine marjinasyonuna olanak tanıyan primer akım bozukluğu nedir?* → **Staz (kan akımının yavaşlaması/durgunluğu)**."
        ],
        "flashcards": [
            {
                "question": "Normal laminer kan akımının bozulup staz gelişmesi trombozu hangi mekanizmalarla kolaylaştırır?",
                "answer": "1) Trombositlerin endotel yüzeyine temasını (marjinasyon) sağlar, 2) Aktif faktörlerin yıkanıp seyreltilmesini önler, 3) Doğal inhibitörlerin akışını engeller."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q14",
            "question": "Venöz dolaşımda staz (kan akımının yavaşlaması) meydana geldiğinde tromboz gelişimini kolaylaştıran patofizyolojik mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Trombositlerin lümen merkezinde toplanıp endotelden tamamen uzaklaşması",
                "B) Aktive pıhtılaşma faktörlerinin taze kanla seyreltilmesinin önlenmesi ve trombositlerin marjinasyonu",
                "C) Antitrombin III düzeyinin lokal olarak aşırı yükselmesi",
                "D) Plazminojenin aşırı hızla plazmine dönüştürülmesi",
                "E) Prostasiklin üretiminin katlanarak artması"
            ],
            "correctAnswer": "B",
            "explanation": "Staz durumunda aksiyal akım bozulur; trombositler endotel yüzeyine marjine olur ve aktive olan koagülasyon faktörleri yıkanıp seyreltilemediği için lokal olarak birikerek trombozu başlatır."
        }
    },

    # SLIDE 15
    {
        "id": "slide-15",
        "title": "Virchow 3: Hiperkoagülabilite (Trombofili) Genel Sınıflandırması",
        "subtitle": "Kalıtsal (primer) ve edinsel (sekonder) trombofililerin etiyolojik tablosu",
        "content": """**HİPERKOAGÜLABİLİTE (TROMBOFİLİ) TABLOSU**
Hiperkoagülabilite, pıhtılaşmaya anormal yatkınlık yaratan her türlü kan bozukluğunu ifade eder. Venöz trombozlarda kritik rol oynar.

1. **Primer (Kalıtsal / Genetik) Nedenler:**
   - **Çok Sık Görülenler:**
     - **Faktör V Leiden mutasyonu:** Beyaz ırkın %2-15'inde bulunur. Aktive Protein C direnci (APC resistance).
     - **Protrombin G20210A mutasyonu:** Toplumun %1-2'sinde; artmış protrombin mRNA transkripsiyonu.
     - **Homosisteinemi:** Metilentetrahidrofolat redüktaz (MTHFR) polimorfizmi.
   - **Nadir Görülenler (Ancak Tromboz Riski Çok Yüksek Olanlar):**
     - Antitrombin III (AT-III) eksikliği
     - Protein C eksikliği
     - Protein S eksikliği

2. **Sekonder (Edinilmiş / Kazanılmış) Nedenler:**
   - **Yüksek Risk:** Uzamış yatak istirahati / immobilizasyon, miyokard enfarktüsü, atriyal fibrilasyon, doku hasarı (kırık, yanık, majör cerrahi), **kanser (özellikle adenokarsinomlar)**, prostetik kalp kapakları, DİK, **Heparin Kaynaklı Trombositopeni (HIT)**, **Antifosfolipid Antikor Sendromu (APS)**.
   - **Düşük Risk:** Gebelik ve lohusalık, oral kontraseptif kullanımı, nefrotik sendrom (idrarla AT-III kaybı), obezite, sigara.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Trombofili Sınıflandırması:**\n  ▫ ==En Sık Kalıtsal Neden:== **Faktör V Leiden mutasyonu**.\n  ▫ ==İkinci En Sık Kalıtsal Neden:== **Protrombin G20210A gen mutasyonu**.\n  ▫ ==Nadir ama Şiddetli Kalıtsal Nedenler:== **Antitrombin III, Protein C ve Protein S eksiklikleri** (genç yaşta masif DVT!).\n  ▫ Malignitelerde tümörden salınan prokoagülanlar Trousseau sendromuna (gezici tromboflebit) yol açar.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Kalıtsal trombofililer içinde toplumda en sık saptanan genetik mutasyon hangisidir?* → **Faktör V Leiden mutasyonu**."
        ],
        "flashcards": [
            {
                "question": "En sık ve ikinci en sık görülen kalıtsal (primer) trombofili nedenleri nelerdir?",
                "answer": "1. Faktör V Leiden mutasyonu (en sık), 2. Protrombin G20210A gen mutasyonu (ikinci en sık)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q15",
            "question": "Toplumda kalıtsal (primer) hiperkoagülabilite etiyolojisinde en sık saptanan genetik mutasyon aşağıdakilerden hangisidir?",
            "options": [
                "A) Antitrombin III gen delesyonu",
                "B) Protein C promotör mutasyonu",
                "C) Faktör V Leiden mutasyonu",
                "D) Fibrinojen alfa zincir mutasyonu",
                "E) Faktör VIII inversiyon mutasyonu"
            ],
            "correctAnswer": "C",
            "explanation": "Kalıtsal trombofililer içinde en sık görüleni Faktör V Leiden mutasyonudur (beyaz ırkta %2-15 sıklık). İkinci sırada Protrombin G20210A mutasyonu gelir."
        }
    },

    # SLIDE 16
    {
        "id": "slide-16",
        "title": "Kalıtsal Trombofililer 1: Faktör V Leiden Mutasyonu",
        "subtitle": "Arg506Gln nokta mutasyonu, Aktive Protein C (APC) direnci ve tromboz riski",
        "content": """**FAKTÖR V LEİDEN MUTASYONU VE APC DİRENCİ**
Kalıtsal hiperkoagülabilite nedenlerinin açık ara en yaygınıdır.

1. **Moleküler Mekanizma:**
   - Normalde Aktive Protein C (APC), Faktör Va'yı spesifik bir amino asit bölgesinden (**Arjinin-506**) keserek inaktive eder ve kaskadı frenler.
   - Faktör V geninde tek nükleotid değişimi (G→A) sonucu 506. pozisyondaki **Arjinin yerine Glutamin** geçer (**Arg506Gln mutasyonu**).
   - Bu mutasyon Faktör V'in pıhtılaştırıcı aktivitesini bozmaz; ancak Protein C'nin Faktör Va'yı kesip inaktive etmesini imkansız hale getirir!
   - Sonuç: Faktör Va yıkılamaz, sürekli aktif kalır ve kontrolsüz trombin üretimi devam eder (**Aktive Protein C Direnci - APC Resistance**).

2. **Klinik Yansıma ve Risk:**
   - **Heterozigot Bireyler:** Venöz tromboz riski yaklaşık **5-8 kat** artmıştır. Genellikle klinik olarak sessizdir; ancak gebelik veya doğum kontrol hapı eklendiğinde DVT patlak verir!
   - **Homozigot Bireyler:** Venöz tromboz riski **50-80 kat** artmıştır. Genç yaşta tekrarlayan derin ven trombozları ve pulmoner emboli görülür.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Faktör V Leiden Formülü:**\n  ▫ Mutasyon: ==Faktör V geninde Arg506Gln (Arjinin → Glutamin)==\n  ▫ Sonuç: **Aktive Protein C Direnci (APC resistance)**.\n  ▫ Faktör Va inaktive edilemez → Koagülasyon kaskadı açık kalır → DVT ve PE riski katlanır.\n  ▫ Doğum kontrol hapı (Östrojen) alan heterozigot kadınlarda tromboz riski 30 katına çıkar!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Faktör V Leiden mutasyonunun temel biyokimyasal sonucu nedir?* → **Faktör Va'nın Aktive Protein C (APC) tarafından parçalanmaya dirençli hale gelmesi**."
        ],
        "flashcards": [
            {
                "question": "Faktör V Leiden mutasyonunda hangi amino asit değişir ve patogenetik sonuç nedir?",
                "answer": "Arjinin yerine Glutamin geçer (Arg506Gln); Faktör Va Aktive Protein C (APC) tarafından yıkılamaz (APC direnci) ve tromboz riski artar."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q16",
            "question": "Faktör V Leiden mutasyonuna sahip bir hastada venöz tromboz gelişimine yol açan temel patofizyolojik mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Faktör V'in trombosit membranına bağlanamaması",
                "B) Faktör Va molekülünün Aktive Protein C (APC) tarafından proteolitik inaktivasyona dirençli hale gelmesi",
                "C) Karaciğerde Antitrombin III sentezinin bloke olması",
                "D) D-Dimer yıkımının durması",
                "E) Fibrinojenin kovalent çapraz bağlanamaması"
            ],
            "correctAnswer": "B",
            "explanation": "Faktör V Leiden mutasyonunda Faktör V genindeki Arg506Gln değişimi nedeniyle Faktör Va, Aktive Protein C (APC) tarafından inaktive edilemez (APC direnci). Bu durum kaskadın frenlenememesine ve hiperkoagülabiliteye yol açar."
        }
    },

    # SLIDE 17
    {
        "id": "slide-17",
        "title": "Kalıtsal Trombofililer 2: Protrombin G20210A ve Diğerleri",
        "subtitle": "Protrombin mRNA stabilizasyonu, Antitrombin III, Protein C ve Protein S eksiklikleri",
        "content": """**DİĞER KALITSAL HİPERKOAGÜLABİLİTE NEDENLERİ**

1. **Protrombin G20210A Mutasyonu:**
   - İkinci en sık kalıtsal trombofili nedenidir (toplumda %1-2).
   - Protrombin geninin kodlamayan **3'-UTR bölgesinde** tek baz değişimi (Guanin → Adenin) vardır.
   - **Mekanizma:** Protrombin mRNA'sının translasyonel stabilitesini artırır. Plazmada normalden yaklaşık **%30 daha fazla protrombin (Faktör II)** üretilir.
   - Venöz tromboz riskini 2-3 kat artırır.

2. **Antitrombin III (AT-III) Eksikliği:**
   - Otozomal dominant geçer; nadirdir ancak tromboz riski son derece yüksektir!
   - Trombin, Faktör Xa ve Faktör IXa nötralize edilemez.
   - **Klinik İpucu (Heparin Direnci):** Standart heparin AT-III üzerinden etki gösterdiği için, AT-III eksikliği olan hastalara heparin verildiğinde aPTT uzamaz (heparin etkisiz kalır)!

3. **Protein C ve Protein S Eksiklikleri:**
   - Faktör Va ve Faktör VIIIa inaktive edilemez. Genç yaşta tekrarlayan DVT ve pulmoner emboli yapar.
   - **Warfarin Nekrozu Riski:** Warfarin başlandığında Protein C'nin yarı ömrü çok kısa olduğu için hızla tükenir; diğer faktörler henüz aktifken geçici bir hiperkoagülasyon dönemi oluşur ve mikrotrombüslerle deride nekroz gelişebilir!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Kritik Klinik İpuçları:**\n  ▫ ==Protrombin G20210A:== 3' UTR mutasyonu → mRNA artışı → Plazma Protrombin düzeyi ↑.\n  ▫ ==Antitrombin III Eksikliği:== **Heparin direnci** görülür! (Heparin AT-III olmadan çalışamaz).\n  ▫ ==Protein C/S Eksikliği:== Warfarin başlandığında **deri nekrozu (Warfarin-induced skin necrosis)** riski!",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Derin ven trombozu nedeniyle intravenöz heparin tedavisi başlanan ancak terapötik aPTT uzaması sağlanamayan (heparin direnci gelişen) bir hastada altta yatan en olası kalıtsal defekt nedir?* → **Antitrombin III eksikliği**."
        ],
        "flashcards": [
            {
                "question": "Heparin direnci (heparine rağmen aPTT'nin uzamaması) hangi kalıtsal trombofilide tipiktir?",
                "answer": "Antitrombin III (AT-III) eksikliği; çünkü heparin etkisini AT-III üzerinden gösterir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q17",
            "question": "Derin ven trombozu atağı geçiren 24 yaşındaki bir erkek hastaya intravenöz standart heparin başlanmasına rağmen terapötik aPTT düzeyine ulaşılamamış (heparine yanıtsızlık / heparin direnci) ve tromboz ilerlemiştir. Bu hastada öncelikle şüphelenilmesi gereken kalıtsal pıhtılaşma bozukluğu aşağıdakilerden hangisidir?",
            "options": [
                "A) Protein C eksikliği",
                "B) Antitrombin III eksikliği",
                "C) Faktör XIII eksikliği",
                "D) Glanzmann trombastenisi",
                "E) Bernard-Soulier sendromu"
            ],
            "correctAnswer": "B",
            "explanation": "Heparin, antikoagülan etkisini plazmadaki Antitrombin III'e bağlanarak gösterir. Antitrombin III eksikliği olan hastalarda heparin hedef molekül bulamadığı için aPTT uzamaz ve heparin direnci gelişir."
        }
    },

    # SLIDE 18
    {
        "id": "slide-18",
        "title": "Edinilmiş Trombofililer: Klinik Risk Grupları ve Trousseau Sendromu",
        "subtitle": "Kanser hiperkoagülabilite ilişkisi, göç eden tromboflebit ve diğer risk faktörleri",
        "content": """**EDİNİLMİŞ (SEKONDER) HİPERKOAGÜLABİLİTE DURUMLARI**
Klinik pratikte tromboz vakalarının büyük çoğunluğu edinsel risk faktörlerine sekonderdir.

1. **Kanser ve Trousseau Sendromu (Gezici Tromboflebit):**
   - Özellikle müsinöz adenokarsinomlarda (pankreas, mide, akciğer, kolon kanserleri) tümör hücreleri dolaşıma **doku faktörü benzeri prokoagülanlar** ve müsin salgılar.
   - **Trousseau Sendromu (Tromboflebitis Migrans):** Vücudun farklı yerlerinde tekrarlayan, bir kaybolup başka bir vende yeniden ortaya çıkan venöz trombozlardır. Çoğu zaman gizli (okült) bir iç organ kanserinin (özellikle pankreas başı karsinomu) ilk klinik işaretidir!

2. **İmmobilizasyon ve Majör Cerrahi:**
   - Kalça ve diz cerrahisi, politravma, uzun süreli yatak istirahati. Bacak kas pompasının durması masif staza yol açar.

3. **Östrojen ve Gebelik:**
   - Gebelik, lohusalık ve oral kontraseptif kullanımı: Karaciğerde pıhtılaşma faktörlerinin (Fibrinojen, FVII, FVIII, FX) sentezini artırırken, Antitrombin III sentezini azaltır.

4. **Nefrotik Sendrom:**
   - Glomerüler bazal membran geçirgenliği bozulduğu için küçük moleküllü bir protein olan **Antitrombin III idrarla kaybedilir**. Hastalarda renal ven trombozu ve DVT sıktır.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Klinik İpuçları:**\n  ▫ ==Trousseau Sendromu (Tromboflebitis Migrans):== Gezici venöz trombozlar → **Pankreas / Mide adenokarsinomu** habercisi!\n  ▫ ==Nefrotik Sendrom:== İdrarla **Antitrombin III kaybı** nedeniyle hiperkoagülabilite ve renal ven trombozu.\n  ▫ ==Östrojen / OKS:== Karaciğerde faktör sentezini artırır, AT-III'ü azaltır.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Sorusu:**\n  ▫ *Vücudun farklı ekstremitelerinde tekrarlayan gezici yüzeyel ven trombozları (tromboflebitis migrans / Trousseau sendromu) saptanan bir hastada öncelikle hangi organ kanseri taranmalıdır?* → **Pankreas kanseri (adenokarsinom)**."
        ],
        "flashcards": [
            {
                "question": "Trousseau sendromu (tromboflebitis migrans) nedir ve hangi kanserle en güçlü ilişkilidir?",
                "answer": "Gezici, tekrarlayan venöz trombozlardır; tümör prokoagülanlarına bağlı gelişir ve en sık pankreas adenokarsinomu ile ilişkilidir."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q18",
            "question": "62 yaşında erkek hasta, sol bacakta yüzeyel ven iltihabı ve trombozu ile başvuruyor. Tedaviyle gerileyen lezyon 3 hafta sonra sağ kolunda ve ardından sağ bacağında tekrarlıyor (tromboflebitis migrans). Bu klinik tablodan (Trousseau sendromu) şüphelenilen hastada en olası altta yatan malignite aşağıdakilerden hangisidir?",
            "options": [
                "A) Pankreas adenokarsinomu",
                "B) Tiroid papiller karsinomu",
                "C) Prostat adenokarsinomu",
                "D) Deri bazal hücreli karsinomu",
                "E) Osteosarkom"
            ],
            "correctAnswer": "A",
            "explanation": "Trousseau sendromu (gezici tromboflebit), tümör hücrelerinden salınan prokoagülan faktörlerin tetiklediği paraneoplastik bir hiperkoagülabilitedir ve en klasik olarak pankreas adenokarsinomunda görülür."
        }
    },

    # SLIDE 19
    {
        "id": "slide-19",
        "title": "Özel İmmün Trombotik Tablolar 1: Heparin Kaynaklı Trombositopeni (HIT)",
        "subtitle": "PF4-Heparin komplekslerine karşı IgG antikorları, tüketim ve paradoksal tromboz",
        "content": """**HEPARİN KAYNAKLI TROMBOSİTOPENİ (HIT)**
Heparin tedavisi alan hastaların yaklaşık %1-5'inde ortaya çıkan, antikoagülan verilmesine rağmen şiddetli tromboza yol açan hayatı tehdit edici immün tablodur.

1. **Tip I HIT vs. Tip II HIT:**
   - **Tip I HIT:** Heparinin trombositler üzerindeki doğrudan hafif toplanma etkisidir. Tedaviden 1-2 gün sonra trombositler hafif düşer, klinik önemi yoktur, heparin kesilmez.
   - **Tip II HIT (Gerçek İmmün HIT):** Şiddetli ve tehlikelidir.

2. **Tip II HIT İmmünopatogenezi:**
   - Dolaşımdaki heparin molekülleri, trombosit alfa granüllerinden salınan **Trombosit Faktörü 4 (Platelet Factor 4 - PF4)** ile birleşerek immünojenik bir neoantijen kompleksi oluşturur.
   - Vücut bu **Heparin-PF4 kompleksine karşı IgG otoantikorları** üretir.
   - Bu IgG antikorlarının Fc ucu, trombositlerin yüzeyindeki **FcγRIIa reseptörlerine** bağlanır.
   - Trombositler kontrolsüz şekilde aşırı aktive olur; granüllerini boşaltır, agregasyon yapar ve tüketilir.
   - **Klinik Paradoks:** Kanda trombosit sayısı düşer (**trombositopeni**), ancak aşırı trombosit aktivasyonu nedeniyle hem arteriyel hem venöz yatakta yaygın ölümcül pıhtılar (**paradoksal tromboz**) gelişir!

3. **Tedavi:**
   - Heparin derhal kesilmeli, kesinlikle düşük molekül ağırlıklı heparin (LMWH) verilmemelidir (çapraz reaksiyon!).
   - **Direkt Trombin İnhibitörleri (Argatroban, Bivalirudin)** veya Fondaparinuks başlanmalıdır.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **HIT Tip II Önemli Noktalar:**\n  ▫ Antijen Kompleksi: ==Heparin + Trombosit Faktörü 4 (PF4)==\n  ▫ Antikor: ==IgG otoantikorları== (Trombosit FcγRIIa reseptörünü uyarır).\n  ▫ Paradoks: **Trombositopeni olmasına rağmen KANAMA DEĞİL TROMBOZ görülür!**\n  ▫ Tedavi: Heparin derhal kesilir; **Argatroban** gibi direkt trombin inhibitörüne geçilir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Fraksiyone olmayan heparin tedavisi alan bir hastada 5-10 gün sonra trombosit sayısında %50'den fazla düşüş ve eşlik eden yeni derin ven trombozu geliştiğinde tanı ve sorumlu antikor hedefi nedir?* → **HIT Tip II** ve **Heparin-PF4 kompleksi**."
        ],
        "flashcards": [
            {
                "question": "Tip II Heparin Kaynaklı Trombositopeni'de (HIT) antikorlar hangi moleküler komplekse karşı oluşur ve klinik paradoks nedir?",
                "answer": "Heparin-PF4 (Trombosit Faktörü 4) kompleksine karşı IgG antikorları oluşur. Paradoks: Trombositopeni olmasına rağmen kanama yerine yaygın tromboz görülür."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q19",
            "question": "Pulmoner emboli nedeniyle standart fraksiyone olmayan heparin infüzyonu başlanan bir hastada tedavinin 6. gününde trombosit sayısı 250.000/µL'den 65.000/µL'ye gerilemiş ve sol bacağında yeni bir derin ven trombozu tespit edilmiştir. Bu hastadaki patolojik sürecin moleküler hedefi aşağıdakilerden hangisidir?",
            "options": [
                "A) GpIIb/IIIa reseptörüne bağlanan IgE",
                "B) Heparin ve Trombosit Faktörü 4 (PF4) kompleksine karşı gelişen IgG otoantikorları",
                "C) von Willebrand Faktörünü parçalayan ADAMTS13 metalloproteinazı",
                "D) Eritrosit membranındaki Rh antijenleri",
                "E) Plazminojen aktivatör inhibitörü-1 (PAI-1)"
            ],
            "correctAnswer": "B",
            "explanation": "Tip II HIT'te Heparin-PF4 kompleksine karşı oluşan IgG otoantikorları trombosit Fc reseptörlerine bağlanarak masif trombosit aktivasyonuna, agregasyona, trombosit tüketimine ve paradoksal tromboza yol açar."
        }
    },

    # SLIDE 20
    {
        "id": "slide-20",
        "title": "Özel İmmün Trombotik Tablolar 2: Antifosfolipid Antikor Sendromu (APS)",
        "subtitle": "Klinik triad, Lupus Antikoagülanı paradoksu ve Anti-beta-2 glikoprotein I",
        "content": """**ANTİFOSFOLİPİD ANTİKOR SENDROMU (APS)**
Fosfolipidlere ve fosfolipide bağlı plazma proteinlerine karşı otoantikorların varlığıyla karakterize sistemik otoimmün trombofili tablosudur.

1. **Hedef Antijenler ve Antikor Tipleri:**
   - Antikorlar serbest fosfolipidlerden ziyade plazma protein-lipit komplekslerine yöneliktir:
     - **Anti-β2-Glikoprotein I (Anti-β2-GPI)**
     - **Antikardiyolipin antikorları** (Sifiliz VDRL/RPR testinde yalancı pozitiflik yapar!)
     - **Lupus Antikoagülanı (LA)**

2. **Klinik Triad:**
   - **Tekrarlayan Trombozlar:** Hem arteriyel (inme, MI, ekstremite gangreni) hem venöz (DVT, PE, renal/hepatik ven trombozları) yatakta!
   - **Tekrarlayan Gebelik Kayıpları:** Plasental damarlarda tromboz ve enfarktüs nedeniyle tekrarlayan düşükler ve ölü doğumlar.
   - **Trombositopeni:** Trombosit yüzey antijenlerine bağlanma ve periferik tüketim.

3. **Lupus Antikoagülanı Paradoksu (ÇOK ÖNEMLİ):**
   - **İn Vitro (Laboratuvar):** Antikorlar test tüpündeki fosfolipitlere bağlanarak koagülasyon faktörlerinin montajını engeller; bu nedenle **aPTT testi paradoksal olarak UZAR**.
   - **İn Vivo (Canlı Vücutta):** Endoteli ve trombositleri aktive ederek tam tersine **HİPERKOAGÜLASYON ve ŞİDDETLİ TROMBOZA** yol açar!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **APS Klinik ve Laboratuvar Paradoksu:**\n  ▫ Klinik Triad: ==Tekrarlayan trombozlar (arter ve ven) + Tekrarlayan düşükler + Trombositopeni==.\n  ▫ ==Lupus Antikoagülanı Paradoksu:==\n    - Test tüpünde (in vitro): **aPTT UZAR** (kanamaya eğilim gibi görünür).\n    - Canlıda (in vivo): **Şiddetli TROMBOZ** yapar!\n  ▫ Sifiliz testinde (VDRL) yalancı pozitifliğe yol açabilir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Klasikleri:**\n  ▫ *Genç bir kadında tekrarlayan düşükler, bacakta derin ven trombozu ve laboratuvarda aPTT uzaması saptandığında en olası tanı nedir?* → **Antifosfolipid Antikor Sendromu (Lupus Antikoagülanı)**."
        ],
        "flashcards": [
            {
                "question": "Antifosfolipid Antikor Sendromu'nda (Lupus Antikoagülanı) in vitro ve in vivo pıhtılaşma davranışı nasıldır?",
                "answer": "İn vitro ortamda fosfolipitleri bağladığı için aPTT paradoksal olarak uzar; ancak in vivo ortamda güçlü bir hiperkoagülasyon ve tromboz oluşturur."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q20",
            "question": "28 yaşında kadın hasta, üçüncü kez gebeliğin ilk trimesterinde düşük yapması ve sağ bacağında derin ven trombozu gelişmesi üzerine araştırılıyor. Laboratuvarda trombositopeni ve paradoksal olarak aPTT testinde uzama tespit ediliyor. Bu hastada en olası tanı aşağıdakilerden hangisidir?",
            "options": [
                "A) Faktör V Leiden mutasyonu",
                "B) Bernard-Soulier Sendromu",
                "C) Antifosfolipid Antikor Sendromu (APS)",
                "D) Hemofili B",
                "E) von Willebrand Hastalığı Tip 1"
            ],
            "correctAnswer": "C",
            "explanation": "Tekrarlayan fetal kayıplar, derin ven trombozu, trombositopeni ve laboratuvarda in vitro aPTT uzaması (Lupus Antikoagülanı paradoksu) Antifosfolipid Antikor Sendromu'nun klasik klinik tablosudur."
        }
    },

    # SLIDE 21
    {
        "id": "slide-21",
        "title": "Trombüs Morfolojisi ve Makroskopi: Zahn Çizgileri",
        "subtitle": "Canlıda akan kanda oluşan trombüsün mikroskobik imzası: Lines of Zahn",
        "content": """**TROMBÜS MORFOLOJİSİ VE ZAHN ÇİZGİLERİ (LINES OF ZAHN)**
Trombüsler damar sisteminin herhangi bir yerinde gelişebilir ve oluştukları damar yatağının hemodinamik özelliklerine göre morfolojik farklılıklar gösterir.

1. **Zahn Çizgileri (Lines of Zahn):**
   - Akan kanda ve canlı bir organizmada oluşan trombüslerin hem makroskobik hem de mikroskobik olarak en karakteristik özelliğidir.
   - **Yapısı:** Ardışık laminasyon gösteren iki farklı kattan oluşur:
     1. **Açık Renkli Katmanlar:** Trombositler ve fibrin ağından zengindir.
     2. **Koyu Kırmızı Katmanlar:** Yoğun eritrosit kümelerinden oluşur.
   - **Patolojik Önemi:** Zahn çizgilerinin varlığı, pıhtının **ölümden önce, dolaşımın ve kan akımının aktif olduğu bir damarda** oluştuğunu kesin olarak kanıtlar!
   - Ölüm sonrası (post-mortem) pıhtılarda Zahn çizgileri KESİNLİKLE BULUNMAZ!

2. **Gelişme Yönü:**
   - Trombüsler damar duvarına tutundukları odak noktasından kalbe doğru uzama eğilimindedir:
     - **Arteriyel Trombüsler:** Kan akım yönünün tersine (**retrograd**) büyür.
     - **Venöz Trombüsler:** Kan akım yönünde (**antegrad**) büyür.
   - Uzayan serbest kuyruk kısmı kırılmaya ve emboli oluşturmaya en yatkın kısımdır.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Zahn Çizgilerinin Anlamı:**\n  ▫ ==Açık tabakalar:== Trombosit + Fibrin.\n  ▫ ==Koyu tabakalar:== Eritrositler.\n  ▫ Anlamı: **Pıhtının canlıda, akan kanda oluştuğunu kanıtlar!**\n  ▫ Ölüm sonrası pıhtıda Zahn çizgisi **YOKTUR**.\n  ▫ Büyüme yönü: Arterde akıma ters (retrograd); vende akım yönünde (antegrad).",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Otopsi sırasında damar lümeninde bulunan bir kitlenin ölüm öncesi gerçek bir trombüs olduğunu gösteren en değerli mikroskobik bulgu nedir?* → **Zahn çizgilerinin (Lines of Zahn) varlığı**."
        ],
        "flashcards": [
            {
                "question": "Zahn çizgileri (Lines of Zahn) neyi gösterir ve hangi katmanlardan oluşur?",
                "answer": "Pıhtının canlıda ve akan kanda oluştuğunu gösterir. Açık renkli trombosit/fibrin katmanları ile koyu renkli eritrosit katmanlarının ardışık diziliminden oluşur."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q21",
            "question": "Adli bir otopside aort ve ana dallarında lümeni tıkayan bir pıhtı kitlesi inceleniyor. Histopatolojik kesitlerde ardışık açık renkli trombosit-fibrin tabakaları ile koyu renkli eritrosit tabakalarının oluşturduğu çizgilenmeler (Zahn çizgileri) gözleniyor. Bu bulgu adli patolojik olarak aşağıdakilerden hangisini kesin olarak kanıtlar?",
            "options": [
                "A) Pıhtının ölüm sonrası durgun kanın çökmesiyle oluştuğunu",
                "B) Pıhtının hasta hayattayken ve kan akımı devam ederken oluştuğunu",
                "C) Hastada hemofili hastalığı bulunduğunu",
                "D) Hastanın siyanür zehirlenmesine bağlı öldüğünü",
                "E) Pıhtının yağ embolisine sekonder geliştiğini"
            ],
            "correctAnswer": "B",
            "explanation": "Zahn çizgileri yalnızca canlı bir organizmada ve akan kanın yarattığı laminasyonla oluşur; varlığı pıhtının ölüm öncesinde (ante-mortem) oluştuğunun kesin kanıtıdır."
        }
    },

    # SLIDE 22
    {
        "id": "slide-22",
        "title": "Arteriyel ve Venöz Trombüslerin Karşılaştırmalı Ayırıcı Tanısı",
        "subtitle": "Beyaz trombüs vs. Kırmızı (staz) trombüsü: Etyoloji, lokalizasyon ve klinik tablo",
        "content": """**ARTERİYEL VS. VENÖZ TROMBÜSLER**
İki damar yatağındaki trombüsler hemodinami, kompozisyon ve klinik sonuçlar açısından taban tabana zıttır:

1. **Arteriyel Trombüsler (Beyaz Trombüs):**
   - **Tetikleyici:** Tipik olarak **endotel hasarı** (aterosklerotik plak yırtılması).
   - **Akım:** Yüksek akım ve yüksek kayma hızı.
   - **Bileşim:** Trombositten ve fibrinden zengindir, eritrosit azdır; grimsi-beyaz ve serttir.
   - **Büyüme:** Kan akımına ters (retrograd). Genellikle lümeni tıkayıcıdır (oklüzif).
   - **Sık Yerleşim:** Koroner arterler, serebral arterler, femoral arterler.
   - **Temel Klinik:** Distal dokuda **iskemi ve enfarktüs** (MI, İskemik İnme, kangren).

2. **Venöz Trombüsler / Flebotromboz (Kırmızı / Staz Trombüsü):**
   - **Tetikleyici:** Tipik olarak **staz ve hiperkoagülabilite**.
   - **Akım:** Yavaş akım hızı.
   - **Bileşim:** Eritrositlerden çok zengindir, gevşek fibrin ağı içerir; koyu kırmızı ve jelatinsidir.
   - **Büyüme:** Kan akımı yönünde (antegrad - kalbe doğru).
   - **Sık Yerleşim:** %90 alt ekstremite derin venleri (popliteal, femoral, iliyak venler).
   - **Temel Klinik:** Lokal ödem, ağrı ve koparak **Pulmoner Emboli** oluşturma!""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Karşılaştırma Tablosu:**\n  ▫ ==Arteriyel Trombüs:== Endotel hasarı → Trombositten zengin (Beyaz) → Retrograd büyüme → **Enfarktüs / İskemi**.\n  ▫ ==Venöz Trombüs:== Staz/Hiperkoagülabilite → Eritrositten zengin (Kırmızı) → Antegrad büyüme → **Pulmoner Emboli**.\n  ▫ Venöz trombüsler neredeyse daima oklüziftir ve uzun bir serbest kuyruk içerir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Sınav Sorusu:**\n  ▫ *Arteriyel trombüslerin temel patogenetik nedeni ve baskın hücresel bileşeni nedir?* → **Endotel hasarı ve trombositler** (Venöz trombüslerde ise staz ve eritrositler baskındır)."
        ],
        "flashcards": [
            {
                "question": "Arteriyel trombüs ile venöz trombüs arasındaki temel etiyolojik ve bileşimsel fark nedir?",
                "answer": "Arteriyel trombüs endotel hasarı zemininde gelişir ve trombositten zengindir (beyaz trombüs); venöz trombüs staz zemininde gelişir ve eritrositten zengindir (kırmızı trombüs)."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q22",
            "question": "Arteriyel ve venöz trombüslerin patolojik özellikleri karşılaştırıldığında aşağıdakilerden hangisi venöz trombüsler (flebotromboz) için doğru bir ifadedir?",
            "options": [
                "A) Genellikle endotelin mekanik yırtılması zemininde gelişir.",
                "B) Trombositten son derece zengin, sert ve beyaz renkli pıhtılardır.",
                "C) Çoğunlukla staz zemininde gelişir, eritrositten zengindir ve kan akımı yönünde büyür.",
                "D) Kan akım yönünün tersine doğru (retrograd) ilerleme gösterir.",
                "E) En sık koroner ve serebral arterlerde yerleşir."
            ],
            "correctAnswer": "C",
            "explanation": "Venöz trombüsler tipik olarak staz ve hiperkoagülabilite zemininde gelişir, bol miktarda hapsolmuş eritrosit içerdiği için kırmızıdır ve kan akımı yönünde (antegrad) kalbe doğru uzar."
        }
    },

    # SLIDE 23
    {
        "id": "slide-23",
        "title": "Mural Trombüsler, Kapak Vejetasyonları ve Post-Mortem Pıhtı Ayrımı",
        "subtitle": "Kalp boşlukları, endokardit tipleri ve ölüm sonrası pıhtının (currant jelly / chicken fat) özellikleri",
        "content": """**ÖZEL TROMBÜS FORMLARI VE POST-MORTEM AYRIMI**

1. **Mural Trombüsler:**
   - Kalp odacıklarının (atriyum veya ventrikül) duvarına veya genişlemiş aort lümenine yapışık trombüslerdir.
   - Sık nedenler: Miyokard enfarktüsü sonrası kontraktilitesi bozulan sol ventrikül duvarı, dilate kardiyomiyopati, atriyal fibrilasyon (sol atriyal apendiks) ve aort anevrizmaları.

2. **Kapak Vejetasyonları (Endokarditler):**
   - **İnfektif Endokardit:** Bakteri veya mantar kolonileri içeren büyük, düzensiz, kapakları tahrip eden enfekte trombüslerdir.
   - **Nonbakteriyel Trombotik Endokardit (NBTE / Marantik Endokardit):** Kanser (trousseau), sepsis veya kaşeksi zemininde hiperkoagülabiliteye bağlı oluşan, kapağı tahrip etmeyen **steril** fibrin-trombosit vejetasyonlarıdır.
   - **Libman-Sacks Endokarditi (SLE):** Sistemik Lupus Eritematozus hastalarında kapakların **her iki yüzünde (hem ventriküler hem atriyal yüz)** görülebilen küçük steril vejetasyonlar.

3. **Ölüm Sonrası (Post-Mortem) Pıhtı vs. Ante-Mortem Trombüs:**
   - **Post-Mortem Pıhtı:**
     - Zahn çizgisi İÇERMEZ. Damar duvarına yapışık DEĞİLDİR (kolayca çekilip lümenden çıkarılır).
     - Jelatinöz kıvamdadır.
     - Yerçekimiyle çöken eritrositler nedeniyle alt kısmı koyu kırmızı (**"Frenk Üzümü Jölesi" / Currant Jelly**), üst kısmı ise plazmadan zengin sarımsı renktedir (**"Tavuk Yağı" / Chicken Fat**).
   - **Gerçek Trombüs:** Damar duvarına sıkıca yapışıktır, kuru, granüler ve kırılgandır; Zahn çizgileri içerir.""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Post-Mortem Pıhtı Ayrımı:**\n  ▫ ==Post-Mortem Pıhtı:== Yumuşak, jelatinöz, elastik, damara yapışık **DEĞİL**, altta *frenk üzümü jölesi*, üstte *tavuk yağı* görünümü, Zahn çizgisi **YOK**.\n  ▫ ==Gerçek Trombüs:== Kuru, sert, kırılgan, damar duvarına **SIKICA YAPIŞIK**, Zahn çizgileri **VAR**.\n  ▫ ==Libman-Sacks Endokarditi:== SLE'de kapakların her iki yüzünde yerleşen steril vejetasyonlar.",
            "🔵 ÇIKMIŞ SORU:\n▸ **TUS & Komite Soruları:**\n  ▫ *Otopsi sırasında damar lümeninden çekildiğinde damar duvarına yapışık olmayan, alt tarafı koyu kırmızı frenk üzümü jölesi, üst tarafı sarı tavuk yağı görünümünde olan oluşum nedir?* → **Post-mortem (ölüm sonrası) pıhtı**."
        ],
        "flashcards": [
            {
                "question": "Post-mortem (ölüm sonrası) pıhtının gerçek trombüsten ayırt edilmesini sağlayan temel makroskobik özellikleri nelerdir?",
                "answer": "Damar duvarına yapışık değildir, Zahn çizgisi içermez, jelatinözdür, altta frenk üzümü jölesi (kırmızı) ve üstte tavuk yağı (sarı) görünümü vardır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q23",
            "question": "Bir otopsi sırasında femoral ven lümeni açıldığında lümeni dolduran, ancak damar endoteline yapışık olmayan, homojen jelatinöz kıvamda, alt kısmı koyu kırmızı (frenk üzümü jölesi) ve üst kısmı açık sarımsı (tavuk yağı) renkte olan ve Zahn çizgisi içermeyen bir kitle çıkarılıyor. Bu bulgu aşağıdakilerden hangisi ile en uyumludur?",
            "options": [
                "A) Eski organize olmuş arteriyel trombüs",
                "B) Post-mortem (ölüm sonrası) pıhtı",
                "C) Libman-Sacks endokardit vejetasyonu",
                "D) Aterosklerotik plak rüptürü",
                "E) Marantik endokardit vejetasyonu"
            ],
            "correctAnswer": "B",
            "explanation": "Damar duvarına yapışık olmama, jelatinöz elastik kıvam, 'tavuk yağı ve frenk üzümü jölesi' katmanlaşması ve Zahn çizgilerinin yokluğu ölüm sonrası (post-mortem) pıhtının patognomonik özellikleridir."
        }
    },

    # SLIDE 24
    {
        "id": "slide-24",
        "title": "Trombozun Akıbeti (4 Temel Yol) ve Klinik Komplikasyonlar Özeti",
        "subtitle": "Propagasyon, embolizasyon, dissolüsyon ve organizasyon/rekanalizasyon mekanizmaları",
        "content": """**TROMBOZUN AKIBETİ (FATE OF THROMBUS)**
Bir trombüs oluştuktan sonraki günlerde 4 temel yoldan birini izler:

1. **Propagasyon (İlerleme / Büyüme):**
   - Trombüs daha fazla trombosit ve fibrin toplayarak damar boyunca uzar ve lümeni tamamen tıkar.

2. **Embolizasyon (Kopma ve Taşınma):**
   - Trombüsün bir parçası veya tamamı damar duvarından koparak kan akımıyla uzak dokulara taşınır.
   - **Derin Ven Trombozu (DVT):** Kopan parça vena kava inferior yoluyla sağ kalbe ve oradan pulmoner arterlere giderek ölümcül **Pulmoner Tromboemboli** tablosuna yol açar!
   - **Sol Kalp Mural Trombüsleri:** Aort yoluyla beyin, böbrek, dalak ve bacaklara giderek sistemik infarktüs yapar.

3. **Dissolüsyon (Eriyme / Lizis):**
   - Yeni oluşan taze pıhtılarda fibrinolitik sistem (t-PA ve plazmin) pıhtıyı hızla parçalayarak damarı tamamen açabilir.
   - **Klinik Zaman Penceresi:** Pıhtı eskidikçe fibrin çapraz bağları artar ve plazmine dirençli hale gelir. Bu nedenle akut iskemik inme ve MI'da t-PA tedavisi **ilk birkaç saat içinde** verilmelidir!

4. **Organizasyon ve Rekanalizasyon:**
   - Eski trombüslerin içine endotel hücreleri, düz kas hücreleri ve fibroblastlar göç eder (granülasyon dokusu benzeri).
   - Zamanla trombüsün içinde yeni kapiller lümenler açılarak kan akımı kısmen yeniden sağlanır (**rekanalizasyon**). Bazen kalsifiye olup damar içinde taşlaşabilir (**flebolit**).""",
        "spots": [
            "🔴 ÖNEMLİ:\n▸ **Trombozun 4 Olası Akıbeti:**\n  ▫ 1. ==Propagasyon:== Büyüyüp damarı tıkaması.\n  ▫ 2. ==Embolizasyon:== Kopup uzak organı tıkaması (DVT → Pulmoner Emboli).\n  ▫ 3. ==Dissolüsyon:== t-PA ile erimesi (Taze pıhtıda etkilidir, eskidikçe direnç kazanır).\n  ▫ 4. ==Organizasyon & Rekanalizasyon:== Fibrozis ve yeni kılcal damar kanallarının açılması.\n  ▫ Kalsifiye pıhtı kalıntısına **flebolit** denir.",
            "🔵 ÇIKMIŞ SORU:\n▸ **Komite & TUS Klasikleri:**\n  ▫ *Akut miyokard enfarktüsü veya iskemik inme geçiren bir hastada trombolitik (t-PA) tedavisinin yalnızca ilk saatlerde etkili olabilmesinin ve geç dönemde yanıtsız kalmasının nedeni nedir?* → **Eski trombüslerin fibrin çapraz bağları ve organizasyon nedeniyle fibrinolize direnç kazanması**."
        ],
        "flashcards": [
            {
                "question": "Bir trombüsün organizasyonu ve rekanalizasyonu ne anlama gelir?",
                "answer": "Trombüs içine fibroblast ve endotel hücrelerinin göç ederek bağ dokusu oluşturması ve pıhtı içinde yeni kapiller kanallar açarak kan akımını kısmen yeniden sağlamasıdır."
            }
        ],
        "practiceQuestion": {
            "id": "tromboz-q24",
            "question": "Eski ve kronikleşmiş bir venöz trombüsün damar duvarındaki fibroblastlar, düz kas hücreleri ve endotel hücreleri tarafından istila edilerek bağ dokusuna dönüştürülmesi ve içinde yeni kapiller damar lümenleri açılarak kan akımının kısmen restore edilmesi süreci aşağıdakilerden hangisidir?",
            "options": [
                "A) Propagasyon",
                "B) Paradoksal embolizasyon",
                "C) Organizasyon ve rekanalizasyon",
                "D) Fibrinoid nekroz",
                "E) Primer hemostaz"
            ],
            "correctAnswer": "C",
            "explanation": "Eski trombüsün bağ dokusu ile yer değiştirmesi organizasyon; bu bağ dokusu kitlesi içinde yeni vasküler lümenlerin açılarak kan geçişine izin vermesi ise rekanalizasyon olarak adlandırılır."
        }
    }
]

print(f"Prepared {len(slides)} comprehensive slides.")


# -------------------------------------------------------------
# ENCYCLOPEDIA & GLOSSARY DATA FOR THROMBOSIS & HEMOSTASIS
# -------------------------------------------------------------

encyclopedia_entries = [
    {
        "id": "ekstrinsik-koagulasyon-yolu",
        "title": "Ekstrinsik Koagülasyon Yolu (Doku Faktörü Yolu)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Damar hasarı sonrasında subendotelyal doku faktörünün (TF / Faktör III) açığa çıkmasıyla başlayan, in vivo pıhtılaşmanın ana başlatıcı yolu olan ve laboratuvarda Protrombin Zamanı (PT / INR) ile ölçülen koagülasyon koludur.",
        "mechanism": [
            "▸ Vasküler hasarla subendotelyal doku faktörü (TF / Tromboplastin) kana maruz kalır.",
            "▸ Doku faktörü, dolaşımdaki Faktör VII ile $Ca^{2+}$ varlığında birleşerek **TF-FVIIa kompleksi** oluşturur.",
            "▸ TF-FVIIa kompleksi doğrudan **Faktör X**'u aktive ederek ortak yola girer; aynı zamanda Faktör IX'u da aktive ederek intrinsik yolu besler.",
            "▸ Doku faktörü yolu inhibitörü (TFPI) tarafından hızla baskılanır; bu nedenle pıhtının devamlılığı intrinsik yolun amplifikasyonuna bağlıdır."
        ],
        "clinicalSignificance": [
            "▸ İn vivo koagülasyonun birincil başlatıcısıdır.",
            "▸ Laboratuvarda **Protrombin Zamanı (PT)** ve **INR** ile değerlendirilir.",
            "▸ Faktör VII en kısa yarı ömürlü faktör olduğu için karaciğer yetmezliğinde ve Warfarin tedavisinde ilk bozulan yoldur."
        ],
        "differentialDiagnosis": [
            "▸ **İntrinsik Yol:** Yabancı/negatif yüzey temasıyla (FXII) başlar, aPTT ile ölçülür.",
            "▸ **Ekstrinsik Yol:** Doku hasarı (TF) ile başlar, PT ile ölçülür."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Ekstrinsik yolun anahtar enzimi **Faktör VII**'dir.",
            "🔵 ÇIKMIŞ SORU: Warfarin (Kumadin) tedavisinde takip edilen test **PT (INR)** olup, ekstrinsik yolun hızla tükenen Faktör VII'sine duyarlıdır."
        ],
        "relatedTerms": ["intrinsik-koagulasyon-yolu", "ortak-koagulasyon-yolu", "doku-faktoru", "faktor-vii", "protrombin-zamani"]
    },
    {
        "id": "intrinsik-koagulasyon-yolu",
        "title": "İntrinsik Koagülasyon Yolu (Temas Faktörleri Yolu)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Faktör XII'nin negatif yüklü yüzeylerle teması veya trombinin geri beslemesiyle aktive olan, Faktör XI, IX ve VIII bileşenlerinden oluşan ve laboratuvarda aPTT ile izlenen pıhtılaşma yolu.",
        "mechanism": [
            "▸ İn vitro temas fazı: Faktör XII (Hageman faktörü) negatif yüzeye temasla XIIa'ya dönüşür.",
            "▸ FXIIa → FXI'i aktive eder (FXIa).",
            "▸ FXIa → $Ca^{2+}$ varlığında FIX'u aktive eder (FIXa).",
            "▸ FIXa, kofaktör FVIIIa, $Ca^{2+}$ ve trombosit fosfolipit yüzeyinde birleşerek **Tenaz Kompleksi** oluşturur.",
            "▸ Tenaz kompleksi **Faktör X**'u keserek aktive eder (FXa) ve ortak yola geçer.",
            "▸ İn vivo ortamda ise bu yol esas olarak az miktarda üretilen trombin tarafından FXI ve FVIII'in aktive edilmesiyle bir 'amplifikasyon döngüsü' olarak işler."
        ],
        "clinicalSignificance": [
            "▸ Laboratuvarda **aPTT (Aktive Parsiyel Tromboplastin Zamanı)** testi ile takip edilir.",
            "▸ **Hemofili A (FVIII eksikliği)** ve **Hemofili B (FIX eksikliği)** bu yoldaki defektlerdir.",
            "▸ Standart (fraksiyone olmayan) heparin tedavisi bu yol üzerinden aPTT ile izlenir."
        ],
        "differentialDiagnosis": [
            "▸ **Hemofili A:** FVIII eksikliği, X'e bağlı resesif, izole aPTT uzaması.",
            "▸ **Hemofili B (Christmas Hastalığı):** FIX eksikliği, X'e bağlı resesif, izole aPTT uzaması.",
            "▸ **FXII Eksikliği:** aPTT belirgin uzar ancak in vivo KANAMA OLMAZ!"
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Faktör XII eksikliğinde test tüpünde aPTT aşırı uzar ama hastada kanama diyatezi KESİNLİKLE GÖRÜLMEZ!",
            "🔵 ÇIKMIŞ SORU: Hemofili A'da izole **aPTT uzaması** saptanır, PT ve kanama zamanı tamamen normaldir."
        ],
        "relatedTerms": ["ekstrinsik-koagulasyon-yolu", "ortak-koagulasyon-yolu", "faktor-viii", "faktor-ix", "aptt-testi"]
    },
    {
        "id": "ortak-koagulasyon-yolu",
        "title": "Ortak Koagülasyon Yolu (Faktör X - Trombin - Fibrin Aksı)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Ekstrinsik ve intrinsik yolların Faktör X aktivasyonu üzerinde birleştiği, Faktör V, Protrombin (FII) ve Fibrinojen (FI) bileşenleriyle fibrin pıhtısını üreten ortak enzimatik hat.",
        "mechanism": [
            "▸ Hem ekstrinsik (TF-FVIIa) hem intrinsik (FIXa-FVIIIa) yollar **Faktör X**'u FXa'ya dönüştürür.",
            "▸ FXa, kofaktör FVa, fosfolipid ve $Ca^{2+}$ ile trombosit zarında **Protrombinaz Kompleksi** oluşturur.",
            "▸ Protrombinaz, Protrombini (FII) keserek aktif **Trombin (FIIa)** haline getirir.",
            "▸ Trombin, çözünür Fibrinojeni keserek çözünmeyen **Fibrin monomerleri** üretir.",
            "▸ Trombin ayrıca FXIII'ü aktive eder; FXIIIa fibrini çapraz bağlarla kilitler."
        ],
        "clinicalSignificance": [
            "▸ Ortak yol faktörlerinin (X, V, II, I) eksikliğinde **HEM PT HEM aPTT UZAR**.",
            "▸ Karaciğer yetmezliği, yaygın damar içi pıhtılaşma (DİK) ve aşırı antikoagülan dozunda her iki test birden bozulur.",
            "▸ Yeni nesil oral antikoagülanlar (Rivaroksaban, Apiksaban) doğrudan Faktör Xa'yı; Dabigatran ise doğrudan Trombini bloke eder."
        ],
        "differentialDiagnosis": [
            "▸ Yalnızca PT uzun: Faktör VII eksikliği (ekstrinsik).",
            "▸ Yalnızca aPTT uzun: Faktör XII, XI, IX, VIII eksikliği (intrinsik).",
            "▸ Hem PT hem aPTT uzun: Faktör X, V, II veya fibrinojen eksikliği (ortak yol)."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Ortak yol faktörleri **Faktör X, V, II (Protrombin) ve I (Fibrinojen)**'dir.",
            "🔵 ÇIKMIŞ SORU: Hem PT hem aPTT testinin birlikte uzadığı durumlarda ortak yol faktörleri (X, V, II, I) taranmalıdır."
        ],
        "relatedTerms": ["trombin", "faktor-x", "faktor-v", "fibrinojen", "faktor-xiii"]
    },
    {
        "id": "arteriyel-tromboz",
        "title": "Arteriyel Trombüs (Beyaz Trombüs)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Kardiyovasküler",
        "summary": "Yüksek akım hızına sahip arterlerde endotel hasarı (özellikle ateroskleroz) zemininde gelişen, trombosit ve fibrinden zengin, akıma ters (retrograd) büyüyen ve distal dokularda enfarktüse yol açan tıkayıcı pıhtıdır.",
        "mechanism": [
            "▸ Aterosklerotik plak yırtılması veya endotel aşınması subendoteli açığa çıkarır.",
            "▸ Yüksek kayma geriliminde (shear stress) vWF ve trombosit GpIb etkileşimi ile masif trombosit adezyonu gerçekleşir.",
            "▸ Trombositler aktive olup GpIIb/IIIa üzerinden fibrinojenle kümelenir.",
            "▸ Pıhtı hızlı akıma rağmen duvara yapışık kalır; akım yönünün tersine (**retrograd**) uzar.",
            "▸ Lümeni tamamen tıkadığında distal doku perfüzyonu durur."
        ],
        "clinicalSignificance": [
            "▸ En sık görüldüğü yerler: Koroner arterler (%MI), Serebral arterler (%İskemik inme), Femoral ve iliak arterler (alt ekstremite iskemisi/gangren).",
            "▸ Trombositten zengin olduğu için tedavisinde ve profilaksisinde **Antiagreganlar (Aspirin, Klopidogrel)** ön plandadır."
        ],
        "differentialDiagnosis": [
            "▸ **Venöz Trombüs:** Staz zemininde oluşur, eritrositten zengindir (kırmızı), kalbe doğru (antegrad) büyür, pulmoner emboli yapar.",
            "▸ **Arteriyel Trombüs:** Endotel hasarı zemininde oluşur, trombositten zengindir (beyaz), retrograd büyür, iskemi/enfarktüs yapar."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Arteriyel trombüslerin en sık nedeni **aterosklerotik plak rüptürü**dür.",
            "🔵 ÇIKMIŞ SORU: Arteriyel trombüsler akım yönünün tersine (**retrograd**) büyürken, venöz trombüsler akım yönünde (**antegrad**) kalbe doğru uzar."
        ],
        "relatedTerms": ["venoz-tromboz", "zahn-cizgileri", "ateroskleroz", "enfarktus", "aspirin"]
    },
    {
        "id": "venoz-tromboz",
        "title": "Venöz Trombüs (Kırmızı Trombüs / Flebotromboz)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Vasküler",
        "summary": "Düşük akım hızına sahip venlerde staz ve hiperkoagülabilite zemininde gelişen, yoğun eritrosit ve fibrin ağı içeren, akım yönünde (antegrad) büyüyen ve pulmoner tromboembolinin ana kaynağı olan pıhtı.",
        "mechanism": [
            "▸ İmmobilizasyon, kalp yetmezliği veya varislerde venöz akım yavaşlar (staz).",
            "▸ Laminer akım bozulur; trombositler marjine olur ve aktive koagülasyon faktörleri yıkanamaz.",
            "▸ Fibrin ağı içinde çok sayıda eritrosit hapsolur; pıhtı koyu kırmızı, jelatinöz bir kitleye dönüşür.",
            "▸ Pıhtı damar duvarına tutunduğu odaktan kalbe doğru (**antegrad**) uzar.",
            "▸ Lümen içinde serbest dalgalanan uzun bir kuyruk oluşturur; bu kuyruk kolayca kopar."
        ],
        "clinicalSignificance": [
            "▸ %90 oranında alt ekstremite derin venlerinde (**Derin Ven Trombozu - DVT**: popliteal, femoral, iliyak venler) yerleşir.",
            "▸ En ölümcül komplikasyonu koparak vena kava inferior yoluyla sağ kalbe ve akciğere gitmesidir (**Pulmoner Tromboemboli - PTE**).",
            "▸ Eritrosit ve fibrinden zengin olduğu için tedavisinde ve profilaksisinde **Antikoagülanlar (Heparin, Warfarin, DOAK)** kullanılır."
        ],
        "differentialDiagnosis": [
            "▸ **Arteriyel Trombüs:** Beyaz, trombositten zengin, enfarktüs yapar.",
            "▸ **Venöz Trombüs:** Kırmızı, eritrositten zengin, pulmoner emboli yapar."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Venöz trombüsler neredeyse daima tıkayıcıdır (oklüzif) ve kan akımı yönünde (**antegrad**) büyür.",
            "🔵 ÇIKMIŞ SORU: Pulmoner tromboembolilerin %95'ten fazlası **alt ekstremite derin ven trombozlarından (DVT)** kaynaklanır."
        ],
        "relatedTerms": ["arteriyel-tromboz", "pulmoner-tromboemboli", "derin-ven-trombozu", "virchow-uclusu", "staz"]
    },
    {
        "id": "zahn-cizgileri",
        "title": "Zahn Çizgileri (Lines of Zahn)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Adli Patoloji",
        "summary": "Yalnızca canlı organizmada ve akan kanın yarattığı laminasyon altında oluşan, açık renkli trombosit-fibrin tabakaları ile koyu renkli eritrosit tabakalarının ardışık mikroskobik ve makroskobik çizgilenmesidir.",
        "mechanism": [
            "▸ Akan kan trombüsün yüzeyinden geçerken ilk olarak trombositler ve fibrin çöker (açık renkli tabaka).",
            "▸ Ardından akım girdaplarında çok sayıda eritrosit pıhtı yüzeyine tutunur (koyu kırmızı tabaka).",
            "▸ Bu döngü kat kat tekrarlanarak karakteristik çizgili (lamine) görünümü oluşturur.",
            "▸ Ölümden sonra dolaşım durduğu için bu ardışık dinamik tabakalaşma gerçekleşemez."
        ],
        "clinicalSignificance": [
            "▸ Adli patolojide ve otopside damar lümenindeki pıhtının **ante-mortem (ölüm öncesi)** oluştuğunun kesin kanıtıdır.",
            "▸ Aort ve kalp boşluklarındaki trombüslerde makroskobik olarak çıplak gözle dahi seçilebilir."
        ],
        "differentialDiagnosis": [
            "▸ **Zahn Çizgileri İçeren Pıhtı:** Ante-mortem gerçek trombüs (duvara yapışık, kuru, kırılgan).",
            "▸ **Zahn Çizgisi İçermeyen Pıhtı:** Post-mortem ölüm sonrası pıhtı (duvara yapışmaz, jelatinöz, frenk üzümü jölesi ve tavuk yağı görünümü)."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Açık katmanlar = Trombosit ve Fibrin; Koyu katmanlar = Eritrositler.",
            "🔵 ÇIKMIŞ SORU: Otopsi kesitinde damar içi kitlenin ölümden önce oluştuğunu gösteren en spesifik histopatolojik bulgu **Zahn çizgilerinin (Lines of Zahn)** varlığıdır."
        ],
        "relatedTerms": ["post-mortem-pihti", "arteriyel-tromboz", "mural-tromboz", "ante-mortem-tromboz"]
    },
    {
        "id": "post-mortem-pihti",
        "title": "Post-Mortem (Ölüm Sonrası) Pıhtı",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Adli Tıp",
        "summary": "Ölümün ardından dolaşımın durmasıyla damar lümeninde kalan kanın yerçekimi etkisiyle çökelmesi sonucu oluşan, duvara yapışmayan, Zahn çizgisi içermeyen jelatinöz yalancı pıhtıdır.",
        "mechanism": [
            "▸ Kalp durduktan sonra kan akımı kesilir.",
            "▸ Ağır olan eritrositler yerçekimi etkisiyle kabın/damarın alt kısmına çöker.",
            "▸ Üst kısımda berrak, hücreden fakir plazma sıvısı toplanır.",
            "▸ Yavaş fibrin oluşumuyla homojen, elastik bir jel kıvamı kazanır.",
            "▸ Endotel reaksiyonu veya canlı doku yanıtı olmadığı için damar intimasına kesinlikle tutunmaz."
        ],
        "clinicalSignificance": [
            "▸ Otopside damar lümeni açıldığında tek parça halinde kolayca çekilerek çıkarılabilir.",
            "▸ Patolog veya adli tıp uzmanı tarafından gerçek ölümcül trombüslerle karıştırılmamalıdır."
        ],
        "differentialDiagnosis": [
            "▸ **Alt Katman:** Koyu kırmızı renkli, çöken eritrositler = **'Frenk Üzümü Jölesi' (Currant Jelly)** görünümü.",
            "▸ **Üst Katman:** Açık sarı renkli, plazma ve fibrin = **'Tavuk Yağı' (Chicken Fat)** görünümü.",
            "▸ **Gerçek Trombüs:** Kuru, granüler, kırılgan, duvara yapışık, Zahn çizgileri pozitif."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Post-mortem pıhtı damar duvarına **YAPIŞIK DEĞİLDİR** ve **ZAHN ÇİZGİSİ İÇERMEZ**.",
            "🔵 ÇIKMIŞ SORU: Frenk üzümü jölesi ve tavuk yağı görünümünde iki tabakalı jel kıvamındaki kitle **post-mortem pıhtıdır**."
        ],
        "relatedTerms": ["zahn-cizgileri", "arteriyel-tromboz", "venoz-tromboz", "otopsi-bulgulari"]
    },
    {
        "id": "mural-tromboz",
        "title": "Mural Trombüs",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Kardiyovasküler",
        "summary": "Kalp odacıklarının (atriyum veya ventrikül) endokardiyal duvarına ya da genişlemiş aort lümenine yapışık olarak gelişen, lümeni tamamen tıkamayan ancak sistemik emboli riski çok yüksek olan trombüs.",
        "mechanism": [
            "▸ Sol ventrikülde: Akut transmural miyokard enfarktüsü endokardiyal nekroz yapar; diskinetik/akinetik miyokard staz ve endotel hasarı oluşturur.",
            "▸ Sol atriyumda: Mitral darlığı ve atriyal fibrilasyon sol atriyal apendikste masif staza yol açar.",
            "▸ Aortta: Aterosklerotik ülserasyonlar veya anevrizmatik genişlemeler (türbülans ve staz) üzerinde gelişir."
        ],
        "clinicalSignificance": [
            "▸ Sistemik arteriyel embolilerin en sık kaynağıdır.",
            "▸ Sol ventrikül veya sol atriyumdan kopan parçalar aorta fırlatılarak **beyne (inme), böbreğe, dalağa ve alt ekstremiteye** giderek yaygın infarktüslere yol açar."
        ],
        "differentialDiagnosis": [
            "▸ **Oklüzif Trombüs:** Lümeni tamamen kapatır (küçük arterler ve derin venlerde tipik).",
            "▸ **Mural Trombüs:** Geniş çaplı boşluklarda duvara yapışık kalır, lümeni daraltır ama tamamen tıkamaz."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Sol ventrikül mural trombüslerinin 1 numaralı nedeni **ön duvar miyokard enfarktüsü ve sol ventrikül anevrizması**dır.",
            "🔵 ÇIKMIŞ SORU: Atriyal fibrilasyonda mural trombüslerin en sık yerleştiği anatomik odak **sol atriyal apendiks (aurikula)**'dır."
        ],
        "relatedTerms": ["miyokard-enfarktusu", "atriyal-fibrilasyon", "iskemik-inme", "anevrizma"]
    },
    {
        "id": "faktor-v-leiden",
        "title": "Faktör V Leiden Mutasyonu (Aktive Protein C Direnci)",
        "category": "genetic",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "summary": "Faktör V geninde 506. kodondaki Arg506Gln nokta mutasyonu sonucu Faktör Va'nın Aktive Protein C (APC) tarafından yıkılamamasıyla karakterize, toplumda en sık görülen kalıtsal trombofilidir.",
        "mechanism": [
            "▸ Faktör V geninde tek nükleotid değişimi (G1691A) gerçekleşir.",
            "▸ 506. pozisyondaki Arjinin amino asidi Glutamin'e dönüşür (**Arg506Gln**).",
            "▸ Normalde Aktive Protein C (APC), FVa'yı tam bu Arg506 bölgesinden keserek yok eder.",
            "▸ Mutasyonlu Faktör V pıhtılaşma işlevini eksiksiz sürdürür ancak APC tarafından kesilemez (**APC Direnci**).",
            "▸ Faktör Va dolaşımda uzun süre aktif kalır; protrombinaz kompleksi durmaksızın trombin üretir."
        ],
        "clinicalSignificance": [
            "▸ Beyaz ırkın %2-15'inde bulunur; kalıtsal venöz trombozların en sık nedenidir.",
            "▸ Heterozigotlarda venöz tromboz riski 5-8 kat; homozigotlarda 50-80 kat artar.",
            "▸ Oral kontraseptif (östrojen) kullanan heterozigot kadınlarda tromboz riski 30 kattan fazla artış gösterir!"
        ],
        "differentialDiagnosis": [
            "▸ **Protrombin G20210A:** 3' UTR mutasyonu, aşırı protrombin üretimi.",
            "▸ **Faktör V Leiden:** Arg506Gln mutasyonu, inaktive edilemeyen Faktör Va."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Faktör V Leiden mutasyonu = **Arg506Gln** = **Aktive Protein C (APC) Direnci**.",
            "🔵 ÇIKMIŞ SORU: Kalıtsal venöz tromboz etiyolojisinde en sık saptanan genetik defekt **Faktör V Leiden mutasyonu**dur."
        ],
        "relatedTerms": ["protein-c", "protein-s", "protrombin-g20210a", "derin-ven-trombozu", "trombofili"]
    },
    {
        "id": "protrombin-g20210a",
        "title": "Protrombin G20210A Gen Mutasyonu",
        "category": "genetic",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "summary": "Protrombin geninin 3' kodlamayan bölgesindeki (3'-UTR) G20210A tek nükleotid değişimi sonucu kanda protrombin (Faktör II) düzeyinin %30 artmasıyla seyreden ikinci en sık kalıtsal trombofili.",
        "mechanism": [
            "▸ Protrombin geninin 3' çevrilmeyen bölgesinde (3'-untranslated region / UTR) 20210. pozisyonda Guanin yerine Adenin geçer.",
            "▸ Bu mutasyon protein yapısını değiştirmez; ancak **protrombin mRNA'sının hücre içinde parçalanmasını geciktirerek stabilitesini artırır**.",
            "▸ Translasyon verimi yükselir ve karaciğerden plazmaya salınan Protrombin (Faktör II) miktarı normalin yaklaşık %130'una ulaşır.",
            "▸ Fazla protrombin, kaskad tetiklendiğinde çok daha yüksek miktarda trombin patlamasına (thrombin burst) yol açar."
        ],
        "clinicalSignificance": [
            "▸ Toplumun yaklaşık %1-2'sinde saptanır; kalıtsal trombofililerde 2. sırada yer alır.",
            "▸ Venöz tromboz riskini 2-3 kat artırır.",
            "▸ Gebelik ve cerrahi gibi edinsel faktörlerle birleştiğinde derin ven trombozunu tetikler."
        ],
        "differentialDiagnosis": [
            "▸ Faktör V Leiden mutasyonu (Arg506Gln) protein dizisini değiştirir; Protrombin G20210A ise kodlamayan 3' UTR'dedir ve protein yapısını bozmaz, sadece sentez miktarını artırır."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Mutasyon kodlayan bölgede değil, **3' UTR bölgesindedir** ve mRNA stabilitesini artırır.",
            "🔵 ÇIKMIŞ SORU: İkinci en sık kalıtsal hiperkoagülabilite nedeni **Protrombin G20210A mutasyonu**dur."
        ],
        "relatedTerms": ["faktor-v-leiden", "trombin", "protrombin", "derin-ven-trombozu"]
    },
    {
        "id": "heparin-induced-thrombocytopenia-hit-tip-2",
        "title": "Heparin Kaynaklı Trombositopeni Tip II (İmmün HIT)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Fraksiyone olmayan heparin kullanımı sonrası Trombosit Faktörü 4 (PF4)-Heparin komplekslerine karşı gelişen IgG otoantikorlarının trombositleri kontrolsüz aktive etmesiyle seyreden, trombositopeniye rağmen ölümcül trombozlarla karakterize immün paradoks.",
        "mechanism": [
            "▸ Negatif yüklü heparin, trombosit alfa granüllerinden çıkan pozitif yüklü **Trombosit Faktörü 4 (PF4)**'e bağlanır.",
            "▸ Ortaya çıkan immünojenik Heparin-PF4 kompleksine karşı **IgG yapısında otoantikorlar** üretilir.",
            "▸ IgG antikorlarının Fc kuyrukları trombosit zarındaki **FcγRIIa reseptörlerini** çapraz bağlar.",
            "▸ Trombositler aşırı aktive olur; mikropartiküller salar, agregasyon yapar ve dalakta tüketime uğrar.",
            "▸ **Paradoksal Tromboz:** Trombosit sayısı %50'den fazla düşer (trombositopeni), ancak açığa çıkan prokoagülan mikropartiküller yaygın arteriyel ve venöz trombozlara yol açar!"
        ],
        "clinicalSignificance": [
            "▸ Genellikle heparin başlandıktan **5-10 gün sonra** ortaya çıkar.",
            "▸ Derhal **HEPARİN KESİLMELİDİR**! Düşük molekül ağırlıklı heparin (LMWH) verilmez (çapraz reaksiyon %100'e yakındır).",
            "▸ Tedavide **Direkt Trombin İnhibitörleri (Argatroban, Bivalirudin)** veya Fondaparinuks kullanılır."
        ],
        "differentialDiagnosis": [
            "▸ **Tip I HIT:** Non-immündir, tedavinin 1-2. gününde hafif trombosit düşüşü olur, pıhtı yapmaz, klinik önemi yoktur, heparin kesilmez.",
            "▸ **Tip II HIT:** İmmündir (IgG), 5-10. günde çıkar, trombosit %50 düşer, masif tromboz yapar, heparin derhal kesilir."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: HIT Tip II'de hedef antijen: ==Heparin - PF4 kompleksi==; reseptör: ==FcγRIIa==.",
            "🔵 ÇIKMIŞ SORU: Heparin tedavisi altında trombosit sayısı aniden düşen ve bacağında yeni DVT gelişen hastada ilaç kesilip **Argatroban (direkt trombin inhibitörü)** başlanmalıdır."
        ],
        "relatedTerms": ["heparin", "trombositopeni", "argatroban", "virchow-uclusu"]
    },
    {
        "id": "antifosfolipid-antikor-sendromu-aps",
        "title": "Antifosfolipid Antikor Sendromu (APS)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Romatoloji",
        "summary": "Fosfolipid-protein komplekslerine (özellikle β2-glikoprotein I) karşı gelişen otoantikorların varlığıyla karakterize; tekrarlayan arteriyel/venöz trombozlar, tekrarlayan gebelik kayıpları ve trombositopeni ile seyreden sistemik otoimmün trombofili.",
        "mechanism": [
            "▸ Plazma proteinleri (özellikle **β2-glikoprotein I** ve protrombin) anyonik fosfolipidlere bağlandığında neoantijen konformasyonu kazanır.",
            "▸ Bağışıklık sistemi bu komplekslere karşı **Anti-β2-GPI, Antikardiyolipin ve Lupus Antikoagülanı (LA)** antikorları üretir.",
            "▸ Antikorlar endotel hücrelerini, trombositleri ve kompleman sistemini uyararak protrombotik durumu tetikler.",
            "▸ Trofoblast hücre fonksiyonlarını bozarak plasental damarlarda enfarktüslere ve fetal kayıplara neden olur."
        ],
        "clinicalSignificance": [
            "▸ **Primer APS:** Altta yatan başka bir otoimmün hastalık olmadan izole görülür.",
            "▸ **Sekonder APS:** En sık **Sistemik Lupus Eritematozus (SLE)** zemininde gelişir.",
            "▸ **Katastrofik APS (Asherson Sendromu):** Günler içinde birden fazla organda yaygın mikrovasküler trombozlarla seyreden ölümcül fulminan tablodur."
        ],
        "differentialDiagnosis": [
            "▸ **Laboratuvar Paradoksu:** Test tüpünde koagülasyon fosfolipidlerini bloke ettiği için **aPTT paradoksal olarak uzar**; ancak hastanın vücudunda **tromboz** yapar!"
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Klinik Triad: ==Tekrarlayan tromboz + Tekrarlayan düşükler + Trombositopeni==.",
            "🔵 ÇIKMIŞ SORU: Lupus antikoagülanı in vitro testte **aPTT'yi uzatırken**, in vivo ortamda **hiperkoagülabilite ve tromboz** oluşturur."
        ],
        "relatedTerms": ["lupus-antikoagulani", "sistemik-lupus-eritematozus", "libman-sacks-endokarditi", "derin-ven-trombozu"]
    },
    {
        "id": "lupus-antikoagulani",
        "title": "Lupus Antikoagülanı (LA)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Laboratuvarda in vitro aPTT pıhtılaşma süresini uzatan, ancak klinik olarak in vivo damar içi tromboza yol açan antifosfolipid otoantikor ailesi üyesi.",
        "mechanism": [
            "▸ Test tüpünde aPTT reaktifindeki fosfolipid yüzeylerine bağlanarak pıhtılaşma faktör komplekslerinin montajını geciktirir.",
            "▸ Bu nedenle laboratuvar testinde aPTT uzamış (kanama bozukluğu gibi) rapor edilir.",
            "▸ Normal plazma ile karıştırıldığında (karışım testi) aPTT düzelmez (inhibitör varlığı kanıtlanır).",
            "▸ Ancak in vivo damar yatağında endotel aktivasyonu ve trombosit agregasyonunu tetikleyerek şiddetli tromboz yapar."
        ],
        "clinicalSignificance": [
            "▸ Antifosfolipid antikor sendromunun en güçlü tromboz prediktörüdür.",
            "▸ Genç yaşta inme, DVT, pulmoner emboli ve tekrarlayan gebelik kayıplarında araştırılmalıdır."
        ],
        "differentialDiagnosis": [
            "▸ **Faktör Eksikliği (Hemofili):** Normal plazma eklendiğinde aPTT düzelir.",
            "▸ **Lupus Antikoagülanı:** Normal plazma eklendiğinde aPTT DÜZELMEZ (inhibitör varlığı)."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Adı 'antikoagülan' olmasına rağmen hastada kanamaya değil **TROMBOZA** yol açar!",
            "🔵 ÇIKMIŞ SORU: Karışım testinde (mixing study) normale dönmeyen aPTT uzaması **Lupus Antikoagülanı** varlığını gösterir."
        ],
        "relatedTerms": ["antifosfolipid-antikor-sendromu-aps", "aptt-testi", "sistemik-lupus-eritematozus"]
    },
    {
        "id": "trousseau-sendromu",
        "title": "Trousseau Sendromu (Tromboflebitis Migrans)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Onkoloji",
        "summary": "Malign tümörlerin (özellikle müsinöz adenokarsinomların) salgıladığı prokoagülan faktörler nedeniyle vücudun farklı yerlerinde tekrarlayan, bir kaybolup başka bir vende ortaya çıkan gezici yüzeyel ven trombozlarıdır.",
        "mechanism": [
            "▸ Kanser hücreleri (özellikle pankreas, mide, akciğer, kolon adenokarsinomları) dolaşıma Doku Faktörü benzeri veziküller ve müsin molekülleri salar.",
            "▸ Müsin, lökosit L-selektin ve trombosit P-selektini ile etkileşerek yaygın mikroagregatları tetikler.",
            "▸ Düşük dereceli kronik DİK ve endotel hasarı eşliğinde ekstremite yüzeyel venlerinde tekrarlayan pıhtılar ve periflebit gelişir.",
            "▸ Lezyonlar tipik olarak göç edicidir (migrans): Bir kolda iyileşirken haftalar sonra diğer bacakta belirir."
        ],
        "clinicalSignificance": [
            "▸ Çoğu zaman henüz teşhis edilmemiş gizli (okült) bir iç organ kanserinin ilk klinik prezentasyonudur.",
            "▸ Armand Trousseau 1865'te bu sendromu tanımlamış ve daha sonra kendisinde de gelişen gezici tromboflebit sonrası pankreas kanserinden vefat etmiştir."
        ],
        "differentialDiagnosis": [
            "▸ **Buerger Hastalığı (Tromboanjitis Obliterans):** Genç sigara içen erkeklerde distal ekstremite iskemi ve flebiti; kanserle ilişkisizdir.",
            "▸ **Trousseau Sendromu:** İleri yaşta gezici flebit; iç organ adenokarsinomu ile ilişkilidir."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Trousseau sendromunda en sık sorumlu kanser **Pankreas Adenokarsinomu**'dur.",
            "🔵 ÇIKMIŞ SORU: Tromboflebitis migrans (gezici yüzeyel ven trombozu) kliniği olan hastada ilk araştırılması gereken tümör **pankreas kanseri**dir."
        ],
        "relatedTerms": ["adenokarsinom", "virchow-uclusu", "doku-faktoru", "derin-ven-trombozu"]
    },
    {
        "id": "bernard-soulier-sendromu",
        "title": "Bernard-Soulier Sendromu (Dev Trombosit Sendromu)",
        "category": "genetic",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Trombosit yüzeyindeki Glikoprotein Ib (GpIb-IX-V) reseptör kompleksinin otozomal resesif eksikliği sonucu trombositlerin von Willebrand Faktörüne (vWF) ve subendotele yapışamadığı, dev trombositlerle seyreden kalıtsal kanama bozukluğu.",
        "mechanism": [
            "▸ GpIb genlerindeki mutasyonlar nedeniyle trombosit zarı üzerinde fonksiyonel GpIb reseptörü bulunamaz.",
            "▸ Damar hasarında açığa çıkan subendotelyal vWF'ye bağlanma gerçekleşemez (**Adhezyon Kusuru**).",
            "▸ Primer hemostaz tıkacı kurulamaz; kanama zamanı belirgin uzar.",
            "▸ Megakaryosit olgunlaşma defekti nedeniyle kanda trombosit sayısı hafif düşüktür ve trombositler eritrosit boyutunda **dev (makrotrombosit)** morfolojidedir."
        ],
        "clinicalSignificance": [
            "▸ Mukokutanöz kanamalar, burun kanamaları (epistaksis), diş eti kanamaları ve menoraji ile başvurur.",
            "▸ Ristosetin ile trombosit agregasyon testinde **agregasyon olmaz**; plazma eklenmesiyle de düzelmez (vWF sağlamdır, reseptör yoktur!)."
        ],
        "differentialDiagnosis": [
            "▸ **Glanzmann Trombastenisi:** GpIIb/IIIa eksikliği, agregasyon bozukluğu, trombosit boyutları normaldir.",
            "▸ **Bernard-Soulier Sendromu:** GpIb eksikliği, adhezyon bozukluğu, dev trombositler (makrotrombositopeni)."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Bernard-Soulier = **GpIb Eksikliği** = **Adhezyon Kusuru** + **Dev Trombositler**.",
            "🔵 ÇIKMIŞ SORU: Trombosit adezyon testi ristosetin ile bozuk olan ve periferik yaymada dev trombositlerin görüldüğü hastalık **Bernard-Soulier sendromu**dur."
        ],
        "relatedTerms": ["glanzmann-trombastenisi", "von-willebrand-faktoru", "primer-hemostaz"]
    },
    {
        "id": "glanzmann-trombastenisi",
        "title": "Glanzmann Trombastenisi",
        "category": "genetic",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Trombosit yüzeyindeki Glikoprotein IIb/IIIa (İntegrin αIIbβ3) reseptör kompleksinin otozomal resesif kalıtsal eksikliği sonucu trombositlerin fibrinojen köprüleriyle birbirine bağlanamadığı (agregasyon kusuru) kanama hastalığı.",
        "mechanism": [
            "▸ ITGA2B veya ITGB3 gen mutasyonları sonucu GpIIb/IIIa integrini üretilemez.",
            "▸ Trombosit adezyonu normaldir (GpIb ve vWF sağlam olduğu için subendotele yapışırlar).",
            "▸ Ancak aktive trombositler arasına fibrinojen molekülleri köprü kuramaz (**Agregasyon Bozukluğu**).",
            "▸ Trombositler birbiriyle kümelenemediği için primer tıkacın büyümesi durur; kanama zamanı uzar."
        ],
        "clinicalSignificance": [
            "▸ Şiddetli purpura, peteşi, epistaksis ve gastrointestinal kanamalar.",
            "▸ Periferik yaymada trombosit sayısı ve boyutları tamamen **normaldir**, ancak lam üzerinde kümelenme yapamazlar (tek tek dağınık dururlar).",
            "▸ Ristosetin testi normaldir (adezyon sağlamdır); ADP, kollajen ve epinefrin ile agregasyon **sıfırdır**."
        ],
        "differentialDiagnosis": [
            "▸ **Bernard-Soulier:** GpIb eksikliği, adhezyon kusuru, dev trombositler.",
            "▸ **Glanzmann:** GpIIb/IIIa eksikliği, agregasyon kusuru, normal boyutlu trombositler."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Glanzmann = **GpIIb/IIIa Eksikliği** = **Agregasyon Kusuru** (Fibrinojen bağlanamaz).",
            "🔵 ÇIKMIŞ SORU: Trombosit adezyonu normal olan ancak fibrinojen köprüleri kurulamadığı için agregasyon yapamayan kalıtsal defekt **Glanzmann trombastenisi**dir."
        ],
        "relatedTerms": ["bernard-soulier-sendromu", "fibrinojen", "primer-hemostaz", "aspirin"]
    },
    {
        "id": "libman-sacks-endokarditi",
        "title": "Libman-Sacks Endokarditi (SLE Endokarditi)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Kardiyoloji",
        "summary": "Sistemik Lupus Eritematozus (SLE) ve Antifosfolipid Antikor Sendromu zemininde kalp kapaklarının hem ventriküler hem atriyal yüzeylerinde gelişen küçük, steril, verrüköz vejetasyonlardır.",
        "mechanism": [
            "▸ İmmün kompleks birikimi ve antifosfolipid antikorların endotel zedelenmesiyle tetiklenir.",
            "▸ Kapak endokardında mukoid dejenerasyon ve fibrin birikimi oluşur.",
            "▸ Bakteriyel veya fungal mikroorganizma içermez (**Steril Vejetasyonlar**).",
            "▸ Karakteristik olarak kalp kapaklarının **her iki yüzünde (hem kan akım yönünde hem serbest alt yüzde)** yerleşebilir."
        ],
        "clinicalSignificance": [
            "▸ En sık mitral ve aort kapaklarını tutar.",
            "▸ Genellikle asemptomatiktir ancak kapak yetmezliğine, kalsifikasyona veya sekonder bakteriyel süperenfeksiyona zemin hazırlayabilir.",
            "▸ Tromboemboli riski taşır."
        ],
        "differentialDiagnosis": [
            "▸ **İnfektif Endokardit:** Bakteriyel, kapağı tahrip eden, büyük, düzensiz vejetasyonlar.",
            "▸ **Marantik Endokardit (NBTE):** Kanser hastalarında kapak kapanma hattında steril vejetasyonlar.",
            "▸ **Libman-Sacks Endokarditi:** SLE'de kapakların her iki yüzünde yerleşen küçük steril vejetasyonlar."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Libman-Sacks vejetasyonları **sterildir** ve kapakların **HER İKİ YÜZÜNDE** de bulunabilir.",
            "🔵 ÇIKMIŞ SORU: Sistemik Lupus Eritematozus hastasında mitral kapağın hem atriyal hem ventriküler yüzeyine yapışık küçük verrüköz steril oluşumlar **Libman-Sacks endokarditi**dir."
        ],
        "relatedTerms": ["antifosfolipid-antikor-sendromu-aps", "sistemik-lupus-eritematozus", "nonbakteriyel-trombotik-endokardit-nbte"]
    },
    {
        "id": "nonbakteriyel-trombotik-endokardit-nbte",
        "title": "Nonbakteriyel Trombotik Endokardit (NBTE / Marantik Endokardit)",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Kardiyovasküler",
        "summary": "İleri evre kanserler (özellikle müsinöz adenokarsinomlar), kronik sepsis veya aşırı kaşeksi zemininde hiperkoagülabiliteye bağlı olarak kalp kapak kapanma çizgilerinde oluşan tahribatsız ve steril fibrin-trombosit vejetasyonlarıdır.",
        "mechanism": [
            "▸ Sistemik hiperkoagülabilite (Trousseau sendromu, DİK) ve hafif hemodinamik travma bir araya gelir.",
            "▸ Kalp kapağı üzerinde lökosit infiltrasyonu veya belirgin enflamasyon olmadan saf fibrin ve trombosit kümeleri çöker.",
            "▸ Altta yatan kapak dokusunda nekroz veya tahribat (destrüksiyon) **YOKTUR**.",
            "▸ Mikroorganizma içermez (**Sterildir**)."
        ],
        "clinicalSignificance": [
            "▸ Vejetasyonlar kapağa çok gevşek tutunmuştur; bu nedenle son derece kolay koparak **serebral, böbrek veya dalak infarktüslerine (sistemik emboli)** yol açar.",
            "▸ Maligniteli hastalarda ani gelişen felçlerin (inme) önemli bir nedenidir."
        ],
        "differentialDiagnosis": [
            "▸ **İnfektif Endokardit:** Kapakta destrüksiyon, delinme (perforasyon) ve yoğun nötrofilik eksüda vardır.",
            "▸ **NBTE:** Kapakta destrüksiyon yoktur, enflamasyon yoktur, steril fibrin-trombosit kitlesidir."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: NBTE vejetasyonları **sterildir**, kapak dokusunu **tahrip etmez** ancak **çok kolay emboli atar**.",
            "🔵 ÇIKMIŞ SORU: İleri evre kanser veya kaşeksi hastasında kalp kapaklarının kapanma hattında tahribatsız, steril fibrin trombüsleri saptanması **Nonbakteriyel Trombotik Endokardit (Marantik Endokardit)** tanısı koydurur."
        ],
        "relatedTerms": ["trousseau-sendromu", "libman-sacks-endokarditi", "infektif-endokardit", "emboli"]
    },
    {
        "id": "trombomodulin-protein-c-aksi",
        "title": "Trombomodulin - Protein C Aksı",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Biyokimya",
        "summary": "Sağlam endotel yüzeyindeki trombomodulin reseptörünün trombin ile birleşerek onun pıhtılaştırıcı etkisini yok etmesi ve Protein C'yi aktive ederek Faktör Va ve VIIIa'yı parçalatan en önemli doğal antikoagülan fren mekanizmasıdır.",
        "mechanism": [
            "▸ Sağlam endotel yüzeyinde **Trombomodulin** adlı transmembran glikoprotein bulunur.",
            "▸ Dolaşımdaki aktif Trombin (FIIa) trombomoduline bağlanır.",
            "▸ Bu bağlanma trombinin şeklini değiştirir; trombin artık fibrinojeni kesemez ve trombositleri aktive edemez.",
            "▸ Bunun yerine endotelyal Protein C Reseptörü (EPCR) üzerindeki **Protein C**'yi parçalayarak aktif enzim haline getirir (**Aktive Protein C - APC**).",
            "▸ APC, kofaktörü olan **Protein S** varlığında koagülasyon kaskadının vazgeçilmez amplifikatörleri olan **Faktör Va ve Faktör VIIIa'yı proteolitik olarak parçalayarak inaktive eder**."
        ],
        "clinicalSignificance": [
            "▸ Koagülasyonun hasarlı bölge dışına taşmasını önleyen en güçlü hücresel güvenlik şalteridir.",
            "▸ Protein C veya Protein S genetik eksikliklerinde bu fren mekanizması çalışamaz; genç yaşta tekrarlayan ağır venöz trombozlar ve Warfarin deri nekrozu gelişir."
        ],
        "differentialDiagnosis": [
            "▸ **Faktör V Leiden:** Trombomodulin ve Protein C sağlamdır; ancak hedef olan Faktör Va mutasyon nedeniyle APC tarafından kesilemez."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: Trombin trombomoduline bağlandığında **prokoagülan kimliğini kaybeder ve antikoagülan bir enzime dönüşür!**",
            "🔵 ÇIKMIŞ SORU: Aktive Protein C (APC), kofaktör Protein S ile birlikte koagülasyon kaskadında hangi iki faktörü parçalayarak inaktive eder? → **Faktör Va ve Faktör VIIIa**."
        ],
        "relatedTerms": ["faktor-v-leiden", "protein-c", "protein-s", "trombin", "endotel"]
    },
    {
        "id": "antitrombin-iii-eksikligi",
        "title": "Antitrombin III (AT-III) ve Eksikliği",
        "category": "pathology",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "summary": "Trombin, Faktör Xa ve Faktör IXa'yı inaktive eden temel serin proteaz inhibitörüdür; kalıtsal eksikliğinde veya nefrotik sendromda idrarla kaybında ağır venöz trombozlar ve klasik 'Heparin Direnci' gelişir.",
        "mechanism": [
            "▸ Karaciğerde sentezlenen tek zincirli bir glikoproteindir (serpin ailesi).",
            "▸ Dolaşımda serbest Trombin (FIIa), Faktör Xa, IXa, XIa ve XIIa'nın aktif merkezine yavaşça bağlanarak onları nötralize eder.",
            "▸ Endotelyal **Heparan Sülfat** veya dışarıdan verilen **Heparin** molekülüne bağlandığında konformasyonu değişir ve inaktivasyon hızı **1000 ila 2000 kat** artar!",
            "▸ Eksikliğinde koagülasyon faktörleri dolaşımda serbestçe aktif kalır; masif pıhtılaşma eğilimi doğar."
        ],
        "clinicalSignificance": [
            "▸ **Kalıtsal Eksiklik:** Otozomal dominant geçer; genç erişkinlerde hayatı tehdit eden DVT ve mezenterik/renal ven trombozları görülür.",
            "▸ **Heparin Direnci:** Standart heparin etkisini AT-III üzerinden gösterdiği için, AT-III düzeyi düşük hastalara yüksek doz heparin verilse bile aPTT uzamaz!",
            "▸ **Nefrotik Sendrom:** Düşük molekül ağırlıklı AT-III idrarla atıldığı için edinsel eksiklik ve renal ven trombozu sıktır."
        ],
        "differentialDiagnosis": [
            "▸ **Protein C/S Eksikliği:** Warfarin başlandığında deri nekrozu riski taşır.",
            "▸ **AT-III Eksikliği:** Heparin başlandığında heparin direnci (aPTT'nin uzamaması) ile kendini belli eder."
        ],
        "highYieldFacts": [
            "🔴 ÖNEMLİ: AT-III eksikliğinde heparin **etki gösteremez (heparin direnci)**; tedavi için taze donmuş plazma veya AT-III konsantresi gerekir.",
            "🔵 ÇIKMIŞ SORU: Heparin infüzyonuna rağmen aPTT uzamayan bir hastada altta yatan defekt **Antitrombin III eksikliği**dir."
        ],
        "relatedTerms": ["heparan-sulfat", "heparin", "trombin", "nefrotik-sendrom"]
    }
]

# GLOSSARY TERMS FOR TOOLTIP / TOAST DICTIONARY
glossary_terms = {
    "Hemostaz": "Damar zedelenmesi sonrasında kanamayı durdurmak amacıyla damar lümeninde fizyolojik, lokalize ve kontrollü pıhtı oluşumu ve ardından gelen doku onarımı süreci.",
    "Tromboz": "Sağlam veya hasarlı bir damarın ya da kalp boşluklarının lümeninde uygunsuz ve kontrolsüz pıhtı (trombüs) oluşmasıyla damar lümeninin tıkanması patolojisi.",
    "Trombüs": "Canlı bir organizmada damar veya kalp boşlukları içinde kanın şekilli elemanları ve fibrin ağından oluşan patolojik intralüminal pıhtı kitlesi.",
    "Virchow Üçlüsü": "Trombozun patogenezinde rol oynayan 3 temel etken: 1) Endotel hasarı, 2) Anormal kan akımı (staz ve türbülans), 3) Hiperkoagülabilite (trombofili).",
    "Endotelin": "Vasküler hasar sonrasında hasarlı endotel hücrelerinden salgılanan ve hemostazın ilk saniyelerinde arteriyel vazokonstriksiyona yol açan bilinen en güçlü endojen vazokonstriktör peptid.",
    "vWF (von Willebrand Faktörü)": "Endotel hücreleri ve megakaryositlerde sentezlenen; subendotelyal kollajen ile trombosit GpIb reseptörü arasında köprü kurarak adezyonu sağlayan multimerik glikoprotein.",
    "Glikoprotein Ib (GpIb)": "Trombosit yüzeyinde bulunan ve subendotelyal vWF'ye bağlanarak trombosit adezyonunu sağlayan reseptör kompleksi; eksikliğinde Bernard-Soulier sendromu gelişir.",
    "Glikoprotein IIb/IIIa (GpIIb/IIIa)": "Trombosit aktivasyonuyla konformasyon değiştiren ve komşu trombositler arasında fibrinojen köprüleri kurarak agregasyonu sağlayan integrin reseptörü; eksikliğinde Glanzmann trombastenisi gelişir.",
    "Bernard-Soulier Sendromu": "GpIb reseptör eksikliği sonucu trombositlerin subendotele yapışamadığı, kanama zamanının uzadığı ve periferik yaymada dev trombositlerin görüldüğü kalıtsal adezyon bozukluğu.",
    "Glanzmann Trombastenisi": "GpIIb/IIIa reseptör eksikliği sonucu trombositlerin fibrinojen köprüleriyle birbirine bağlanamadığı (agregasyon kusuru) kalıtsal kanama bozukluğu.",
    "Doku Faktörü (Tromboplastin / Faktör III)": "Subendotel ve adventisyada bolca bulunan; vasküler hasarla açığa çıkıp Faktör VIIa ile birleşerek in vivo koagülasyonu başlatan membran glikoproteini.",
    "Protrombin Zamanı (PT)": "Plazmaya doku faktörü eklenerek ölçülen; ekstrinsik (FVII) ve ortak (X, V, II, I) yolları değerlendiren ve Warfarin tedavisinde takip edilen koagülasyon testi.",
    "aPTT (Aktive Parsiyel Tromboplastin Zamanı)": "Negatif yüklü yüzey temasıyla ölçülen; intrinsik (XII, XI, IX, VIII) ve ortak yolları değerlendiren ve standart heparin tedavisinde izlenen koagülasyon testi.",
    "Trombin (Faktör IIa)": "Fibrinojeni fibrine çeviren, trombositleri PAR reseptörleriyle aktive eden ve trombomoduline bağlandığında Protein C'yi aktive ederek antikoagülan etki gösteren merkezi serin proteaz.",
    "Trombomodulin": "Sağlam endotel yüzeyinde bulunan; trombine bağlanarak onun prokoagülan etkisini yok eden ve Protein C'yi aktive etmesini sağlayan antikoagülan reseptör.",
    "Protein C": "K vitaminine bağımlı doğal antikoagülan enzim; kofaktör Protein S ile birlikte Faktör Va ve Faktör VIIIa'yı parçalayarak koagülasyon kaskadını frenler.",
    "Antitrombin III (AT-III)": "Endotelyal heparan sülfat ve heparin varlığında aktivitesi bin kat artan; trombin, Faktör Xa ve Faktör IXa'yı inaktive eden temel plazma inhibitörü.",
    "Faktör V Leiden": "Faktör V geninde Arg506Gln nokta mutasyonu sonucu Faktör Va'nın Aktive Protein C (APC) tarafından yıkılamamasıyla seyreden ve en sık görülen kalıtsal venöz trombofili.",
    "Protrombin G20210A": "Protrombin geninin 3' UTR bölgesindeki mutasyon sonucu mRNA stabilitesinin artması ve kanda aşırı protrombin üretimiyle seyreden ikinci en sık kalıtsal trombofili.",
    "Trousseau Sendromu": "Özellikle pankreas ve müsinöz adenokarsinomlarda tümör kaynaklı prokoagülanlar nedeniyle vücutta tekrarlayan gezici yüzeyel ven trombozları (tromboflebitis migrans).",
    "HIT Tip II (Heparin Kaynaklı Trombositopeni)": "Heparin-PF4 kompleksine karşı gelişen IgG otoantikorlarının trombositleri tüketip aynı zamanda masif aktive ederek trombositopeni eşliğinde şiddetli tromboza yol açtığı immün tablo.",
    "Antifosfolipid Antikor Sendromu (APS)": "β2-glikoprotein I ve fosfolipidlere karşı otoantikorlarla karakterize; tekrarlayan arteriyel/venöz trombozlar, tekrarlayan düşükler ve trombositopeni triadı.",
    "Lupus Antikoagülanı": "Test tüpünde fosfolipidleri bağlayarak in vitro aPTT'yi uzatan, ancak canlı vücutta güçlü bir hiperkoagülasyon ve tromboz oluşturan antifosfolipid otoantikor.",
    "Zahn Çizgileri": "Yalnızca canlıda ve akan kanda oluşan trombüslerde görülen; açık renkli trombosit-fibrin tabakaları ile koyu renkli eritrosit tabakalarının ardışık laminasyon çizgileri.",
    "Mural Trombüs": "Kalp odacıkları (sol ventrikül, sol atriyum) veya anevrizmatik aort duvarına yapışık gelişen ve sistemik arteriyel embolilerin en sık kaynağı olan pıhtı.",
    "Libman-Sacks Endokarditi": "Sistemik Lupus Eritematozus hastalarında kalp kapaklarının her iki yüzeyinde gelişebilen küçük, steril, verrüköz vejetasyonlar.",
    "Marantik Endokardit (NBTE)": "Kanser ve kaşeksi hastalarında kapak kapanma hattında gelişen, kapağı tahrip etmeyen steril fibrin-trombosit vejetasyonları.",
    "Post-Mortem Pıhtı": "Ölüm sonrası kanın yerçekimiyle çökmesi sonucu oluşan; duvara yapışmayan, Zahn çizgisi içermeyen, altta frenk üzümü jölesi ve üstte tavuk yağı görünümündeki yalancı pıhtı.",
    "D-Dimer": "Faktör XIII ile çapraz bağlanmış stabil fibrin pıhtısının plazmin tarafından eritilmesiyle açığa çıkan; DVT, PE ve DİK tanısında yüksek negatif prediktif değere sahip fibrin yıkım ürünü.",
    "Flebolit": "Eski ve organize olmuş venöz trombüsün zaman içinde kalsifiye olarak damar lümeni içinde taşlaşmış kireç odağı haline gelmesi."
}

# -------------------------------------------------------------
# MAIN INTEGRATION EXECUTION
# -------------------------------------------------------------

def run_integration():
    print("Executing full integration for Tromboz Patofizyolojisi...")

    # 1. READ INTERACTIVE LEARNING DECKS
    decks_file = "src/data/interactive_learning_decks.json"
    with open(decks_file, "r", encoding="utf-8") as f:
        decks = json.load(f)

    # Prepare deck object
    new_deck = {
        "id": DECK_ID,
        "title": DECK_TITLE,
        "discipline": DISCIPLINE,
        "instructor": INSTRUCTOR,
        "committee": COMMITTEE,
        "description": "Prof. Dr. Hikmet Keleş'in Dönem 2 Kurul 1 Patoloji ders notundan derlenmiş, normal hemostaz basamaklarından Virchow üçlüsüne, genetik trombofililerden Zahn çizgilerine kadar %500 derinlikli 24 slayt ve 24 özgün çalışma sorusu içeren kapsamlı interaktif öğrenme güvertesi.",
        "slidesCount": len(slides),
        "detailLevel": "500%",
        "slides": slides
    }

    # Check if deck already exists
    existing_index = next((i for i, d in enumerate(decks) if d.get("id") == DECK_ID), None)
    if existing_index is not None:
        decks[existing_index] = new_deck
        print(f"Updated existing deck: {DECK_ID}")
    else:
        decks.append(new_deck)
        print(f"Appended new deck: {DECK_ID}. Total decks: {len(decks)}")

    with open(decks_file, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    # 2. SAVE STUDY QUESTIONS TO CHUNK_8
    c8_file = "src/data/study_questions/chunk_8.json"
    with open(c8_file, "r", encoding="utf-8") as f:
        chunk_8 = json.load(f)

    added_questions = 0
    for s in slides:
        pq = s.get("practiceQuestion")
        if pq:
            q_obj = {
                "id": f"sq-tromboz-{pq['id']}",
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
            # Avoid duplicate
            if not any(x.get("id") == q_obj["id"] for x in chunk_8):
                chunk_8.append(q_obj)
                added_questions += 1

    print(f"Added {added_questions} questions to chunk_8. Total now: {len(chunk_8)}")
    with open(c8_file, "w", encoding="utf-8") as f:
        json.dump(chunk_8, f, ensure_ascii=False, indent=2)

    # 3. UPDATE STUDY QUESTIONS INDEX
    idx_file = "src/data/study_questions/index.json"
    with open(idx_file, "r", encoding="utf-8") as f:
        idx_data = json.load(f)

    # Recalculate total questions across all chunks
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
    print(f"Updated study_questions/index.json! Total study questions: {total_q}")

    # 4. UPDATE LEARNING QUEUE
    queue_file = "src/data/learning_batch_queue.json"
    with open(queue_file, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    # Mark DECK_ID as completed
    for item in queue_data:
        if item.get("id") == DECK_ID:
            item["status"] = "completed"
            item["slidesCount"] = len(slides)
            item["detailLevel"] = "500%"

    # Determine next in queue if available
    # Check if there is another next item or add next course
    has_next = any(x.get("status") == "next_in_queue" and x.get("id") != DECK_ID for x in queue_data)
    if not has_next:
        # Check next Kurul 1 course: 13) İskemi, İnfarktüs ve Şok Patolojisi
        next_item = {
            "id": "learn-iskemi-infarktus-ve-sok",
            "title": "İskemi, İnfarktüs ve Şok Patolojisi",
            "discipline": "Tıbbi Patoloji",
            "status": "next_in_queue",
            "slidesCount": 24,
            "detailLevel": "500% (Planlanan)"
        }
        queue_data.append(next_item)
        print("Added next course to queue: learn-iskemi-infarktus-ve-sok")

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

    print("ALL INTEGRATION TASKS SUCCESSFULLY COMPLETED!")

if __name__ == "__main__":
    run_integration()
