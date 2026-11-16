# -*- coding: utf-8 -*-
"""
Rebuild Kidney Tumors Deck with High-Quality Medical Standards
learn-bobrek-tumorleri (24 Slayt)
Prof. Dr. Hikmet Keleş & Robbins Pathology
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

def make_slide(slide_num, title, subtitle, narrative, spots, practice_q):
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "content": narrative,
        "synthesisNarrative": narrative,
        "spots": spots,
        "spotPearls": spots,
        "relatedQuestions": [practice_q],
        "practiceQuestion": practice_q
    }

bobrek_tumor_slides = [
    make_slide(
        1,
        "Böbrek Neoplazmlarına Giriş ve Epidemiyoloji",
        "Erişkin Böbrek Maligniteleri, İnsidans ve Edinsel Risk Faktörleri",
        """Böbrek tümörleri geniş bir histopatolojik spektrumu kapsar; erişkinlerde görülen böbrek neoplazmlarının **%85-90'ından fazlası Renal Hücreli Karsinomdur (RCC)**. Erkeklerde kadınlara oranla 2 kat daha sık görülür ve en sık 50-70 yaş grubunda saptanır.

**1. Edinsel Risk Faktörleri:**
• **Sigara Tüketimi:** Açık ara en güçlü ve kanıtlanmış edinsel risk faktörüdür; sigara içenlerde RCC riski içmeyenlere göre 2 kat artar.
• **Obezite ve Hipertansiyon:** Özellikle kadınlarda artmış vücut kitle indeksi bağımsız bir risk faktörüdür; antihipertansif ilaçlardan bağımsız olarak hipertansiyonun kendisi riski artırır.
• **Edinsel Kistik Böbrek Hastalığı:** Kronik böbrek yetmezliği nedeniyle 3-5 yıldan uzun süre diyalize giren hastalarda gelişen kistlerin epitelinden RCC gelişme riski 30 kat fazladır.
• **Mesleki ve Çevresel Toksinler:** Asbest maruziyeti, petrol rafinerisi ürünleri, kadmiyum ve trikloretilen maruziyeti.""",
        [
            {"type": "warning", "badge": "🔴 1 NUMARALI RİSK FAKTÖRÜ", "text": "Renal Hücreli Karsinom için en güçlü ve en önemli değiştirilebilir edinsel risk faktörü Sigara kullanımıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Kronik hemodiyaliz hastalarında gelişen 'edinsel kistik böbrek hastalığı' zemininde Renal Hücreli Karsinom riski normal topluma göre 30 kat artmıştır.", "color": "sky"}
        ],
        {
            "id": "prac-tum-001",
            "question": "Renal hücreli karsinom (RCC) etyolojisinde rol oynayan en güçlü ve kanıtlanmış değiştirilebilir edinsel risk faktörü aşağıdakilerden hangisidir?",
            "options": [
                "A) Kahve tüketimi",
                "B) Sigara kullanımı",
                "C) Alkol tüketimi",
                "D) Kronik kalsiyum taşları",
                "E) Aşırı tuz tüketimi"
            ],
            "correctAnswer": 1,
            "explanation": "Sigara kullanımı Renal Hücreli Karsinom gelişiminde en güçlü ve en iyi dökümante edilmiş çevresel/edinsel risk faktörüdür."
        }
    ),
    make_slide(
        2,
        "Renal Onkositoma: Maun Kahverengisi Kitle ve Yıldızsı Skar",
        "İnterkale Hücreler, Mitokondri Yığılması ve Benign Onkositer Proliferasyon",
        """Renal Onkositoma, böbrek kortikal toplayıcı tübüllerinin **interkale (ara) hücrelerinden** kaynaklanan, tüm böbrek neoplazmlarının yaklaşık %5-10'unu oluşturan **tamamen benign** bir epitelyal tümördür.

**1. Makroskobik Morfoloji (Patognomonik):**
• Genellikle tek taraflı, iyi sınırlı, psödokapsüllü bir kitledir.
• **Renk:** Kesit yüzeyi homojen **maun kahverengisi (mahogany brown)** veya taba rengindedir. Bu renk tümör hücrelerinin sitoplazmasındaki yoğun mitokondri enzimlerinden (sitokromlar) kaynaklanır.
• **Yıldızsı Santral Skar (Stellate Central Scar):** Tümörün tam merkezinde açık renkli, yıldız şeklinde fibröz bir skar alanı izlenir. Bu görünüm onkositoma için son derece karakteristiktir. Nekroz ve kist nadirdir.

**2. Mikroskobik Bulgular:**
• Büyük, poligonal hücrelerden oluşur.
• Sitoplazma mitokondrilerle tıka basa dolu olduğu için **yoğun eozinofilik ve belirgin ince granülerdir (onkositer sitoplazma)**.
• Yuvarlak, düzgün sınırlı merkezi nükleuslar izlenir; nükleer atipi ve mitotik figürler görülmez.
• Elektron mikroskobunda sitoplazmanın tamamen yoğun mitokondrilerle dolu olduğu kesinleştirilir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Maun kahverengisi kesit yüzü, merkezinde yıldızsı fibröz skar (stellate scar) ve mikroskopta mitokondriyle dolu onkositik hücreler Renal Onkositoma için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Renal onkositoma toplayıcı tübüllerin interkale hücrelerinden kaynaklanır; tamamen benigndir ve metastaz yapmaz.", "color": "sky"}
        ],
        {
            "id": "prac-tum-002",
            "question": "Nefrektomi materyalinde böbrek korteksinde 5 cm çapında, iyi sınırlı, maun kahverengisi kesit yüzü gösteren ve merkezinde yıldızsı fibröz skar bulunan bir tümör saptanıyor. Mikroskopta hücrelerin mitokondriden zengin yoğun eozinofilik granüler sitoplazmalı olduğu izleniyor. Tanı nedir?",
            "options": [
                "A) Berrak hücreli renal karsinom",
                "B) Renal onkositoma",
                "C) Papiller renal karsinom",
                "D) Anjiyomiyolipom",
                "E) Wilms tümörü"
            ],
            "correctAnswer": 1,
            "explanation": "Maun kahverengisi renk, santral yıldızsı skar ve sitoplazması mitokondri dolu onkositer hücreler Renal Onkositomanın patognomonik triadıdır."
        }
    ),
    make_slide(
        3,
        "Anjiyomiyolipom (AML) ve Tüberöz Skleroz Birlikteliği",
        "Damar, Kas, Yağ Triadı, Wunderlich Sendromu ve HMB-45 Pozitif PEComa",
        """Anjiyomiyolipom (AML), böbrekte mezenkimal dokulardan köken alan benign bir tümördür.

**1. Histopatolojik Triad:**
Tümör üç temel doku elemanının değişken oranlarda karışımından oluşur:
1. **Anjiyo:** Kalın duvarlı, elastik laminası eksik veya disorganize, kanamaya yatkın displastik kan damarları,
2. **Miyo:** İğsi veya epiteloid morfolojide neoplazik düz kas hücreleri demetleri,
3. **Lipom:** Matür yağ dokusu (lipositler).

**2. Klinik Birliktelikler ve Wunderlich Sendromu:**
• **Sporadik Form (%80):** Genellikle orta yaşlı kadınlarda tek taraflı ve soliter kitle olarak saptanır.
• **Tüberöz Skleroz Birlikteliği (%20):** Tüberöz sklerozlu hastaların **%25-50'sinde** anjiyomiyolipom bulunur. Bu olgularda tümörler tipik olarak **bilateral, multipl ve devasa boyutlardadır**. *TSC1* (Hamartin) veya *TSC2* (Tüberin) gen mutasyonları rol oynar.
• **Wunderlich Sendromu:** Damar duvarlarının elastik laminadan yoksun olması nedeniyle 4 cm'den büyük tümörler aniden yırtılarak hayatı tehdit eden **masif spontan retroperitoneal kanamaya** yol açabilir.

**3. İmmünohistokimya:**
AML hücreleri perivasküler epiteloid hücre (PEComa) ailesine aittir; hem düz kas belirteçleri (SMA) hem de melanositik belirteçler olan **HMB-45 ve Melan-A** ile kuvvetli pozitif boyanır.""",
        [
            {"type": "warning", "badge": "🔴 HAYATİ ACİL", "text": "4 cm'den büyük anjiyomiyolipomlar spontan rüptürle masif retroperitoneal hematom (Wunderlich sendromu) riski taşır; profilaktik embolizasyon veya cerrahi gerektirir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Damar, düz kas ve yağ dokusundan oluşan anjiyomiyolipom Tüberöz Skleroz ile güçlü birliktelik gösterir ve melanositik belirteç olan HMB-45 ile pozitiftir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-003",
            "question": "Yüzünde anjiyofibromları (adenoma sebaseum) ve zeka geriliği olan bir gençte bilateral dev böbrek kitleleri saptanıyor. Biyopside kalın duvarlı damarlar, düz kas ve yağ dokusu izleniyor. İmmünohistokimyada HMB-45 pozitif boyanan bu antite hangisidir?",
            "options": [
                "A) Renal hücreli karsinom",
                "B) Anjiyomiyolipom (AML)",
                "C) Renal onkositoma",
                "D) Medüller karsinom",
                "E) Jukstaglomerüler hücreli tümör"
            ],
            "correctAnswer": 1,
            "explanation": "Damar, kas ve yağ dokusu triadı içeren ve Tüberöz skleroz ile ilişkili HMB-45 pozitif tümör Anjiyomiyolipomdur (AML)."
        }
    ),
    make_slide(
        4,
        "Renal Hücreli Karsinom (RCC): Berrak Hücreli Varyant ve VHL Genetiği",
        "Kromozom 3p Delesyonu, VHL İnaktivasyonu, HIF-1-Alfa Artışı ve Anjiyogenez",
        """Berrak Hücreli Renal Hücreli Karsinom (ccRCC), tüm böbrek kanserlerinin **%70-80'ini oluşturan en sık ve en ölümcül alt tiptir**. Proksimal konvolüt tübül epitelinden kaynaklanır.

**1. Moleküler Genetik ve VHL Yolağı:**
• Hem ailesel hem de sporadik olguların %90'ından fazlasında temel genetik defekt **Kromozom 3p delesyonu** ve bu bölgede yer alan **VHL (Von Hippel-Lindau)** tümör süpresör geninin inaktivasyonudur (mutasyon veya hipermetilasyon).
• **Knudson'ın İki Vuruş Hipotezi:** Ailesel Von Hippel-Lindau sendromunda hasta birinci vuruşu germline mutasyonla miras alır, ikinci alel somatik olarak kaybedilir. Sporadik olgularda ise her iki alel de yaşam boyu somatik mutasyonla inaktive olur.

**2. VHL Proteini ve HIF Biyolojisi:**
• Normalde VHL proteini bir ubiquitin ligaz kompleksinin parçasıdır; oksijen varlığında **HIF-1-alfa (Hipoksi ile İndüklenen Faktör)** proteinini yıkar.
• VHL inaktive olduğunda veya mutasyona uğradığında HIF-1-alfa proteini parçalanamaz ve nükleusta birikir.
• Aşırı biriken HIF-1-alfa hücreyi sürekli hipoksideymiş gibi uyarır: Masif **VEGF (Vasküler Endotelyal Büyüme Faktörü)** ve **PDGF** salgılanarak tümörde kontrolsüz anjiyogenez tetiklenir; ayrıca **GLUT-1** artırılarak tümör glikolizi hızlandırılır.""",
        [
            {"type": "warning", "badge": "🔴 MOLEKÜLER KOD", "text": "Berrak hücreli RCC'nin moleküler temeli Kromozom 3p kaybı ve VHL gen inaktivasyonudur; bu durum HIF-1-alfa birikimi ve masif VEGF salınımına yol açar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "ccRCC'de tümörün aşırı vaskülarize olmasının temel nedeni VHL kaybına bağlı biriken HIF-1-alfa'nın VEGF üretimini tetiklemesidir. Hedefe yönelik tirozin kinaz inhibitörleri bu yolağı hedefler.", "color": "sky"}
        ],
        {
            "id": "prac-tum-004",
            "question": "Berrak hücreli renal hücreli karsinomların (ccRCC) patogenezinde en sık saptanan kromozom anormalliği ve inaktive olan tümör süpresör gen aşağıdakilerden hangisidir?",
            "options": [
                "A) Kromozom 11p delesyonu — WT1",
                "B) Kromozom 3p delesyonu — VHL",
                "C) Kromozom 7 trizomisi — MET",
                "D) Kromozom 17p delesyonu — TP53",
                "E) Kromozom 13q delesyonu — RB1"
            ],
            "correctAnswer": 1,
            "explanation": "Berrak hücreli RCC patogenezinde kromozom 3p delesyonu ve VHL tümör süpresör geninin inaktivasyonu olguların %90'ından fazlasında saptanır."
        }
    ),
    make_slide(
        5,
        "Berrak Hücreli RCC Morfolojisi: Makroskopi, Mikroskopi ve Vasküler Yayılım",
        "Altın Sarısı Kitle, Berrak Sitoplazma, İnce Kapiller Ağ ve Renal Ven Trombozu",
        """Berrak hücreli RCC morfolojik olarak son derece zengin ve karakteristik özellikler taşır.

**1. Makroskobik Görünüm:**
• Genellikle böbreğin üst kutbunda yerleşen, korteksten kaynaklanan büyük küre şeklinde bir kitledir.
• **Kesit Yüzeyi:** Tümör hücrelerinin yüksek lipid ve kolesterol içeriği nedeniyle tipik **parlak altın sarısı / turuncu** renktedir.
• Tümör içinde geniş iskemik nekroz alanları, kistik dejenerasyon ve taze/eski kanama odakları izlenir (alacalı görünüm).
• **Vasküler Yayılım (Tümör Trombüsü):** ccRCC damar invazyonuna olağanüstü meyillidir. Tümör doğrudan **Renal Vene invaze olur** ve bir tümör trombüsü şeklinde **Vena Cava Inferior (VCI)'a ve hatta sağ atriyuma kadar uzanabilir!**

**2. Mikroskobik Bulgular:**
• Hücreler kordonlar, yuvalar veya tübüler yapılar oluşturur.
• Sitoplazma glikojen ve nötral lipidlerden son derece zengindir; rutin histolojik takip sırasında bu maddeler eridiği için mikroskopta **optik olarak tamamen boş, berrak (clear)** görünür.
• Hücre sınırları son derece belirgindir.
• Hücre yuvalarının çevresinde zengin, narin, ince duvarlı dallanan kapiller damar ağı izlenir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK YAYILIM", "text": "Renal ven içine girip Vena Cava Inferior boyunca sağ atriyuma kadar ilerleyen tümör trombüsü Berrak Hücreli Renal Karsinomun klasik yayılım yoludur!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "ccRCC'de hücre sitoplazmasının berrak görünmesinin nedeni hücre içinde aşırı miktarda biriken 'Glikojen ve Lipid' damlacıklarının preparat hazırlanırken erimesidir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-005",
            "question": "Böbrek üst kutbunda yerleşen altın sarısı renkli, kanamalı ve nekrotik bir kitle nedeniyle opere edilen hastanın patoloji raporunda tümörün renal ven lümenine invaze olarak tümör trombüsü oluşturduğu ve mikroskopta narin kapillerler çevresinde berrak sitoplazmalı hücrelerden oluştuğu belirtiliyor. Tanı nedir?",
            "options": [
                "A) Renal onkositoma",
                "B) Berrak hücreli renal hücreli karsinom",
                "C) Kromofob karsinom",
                "D) Anjiyomiyolipom",
                "E) Ürotelyal karsinom"
            ],
            "correctAnswer": 1,
            "explanation": "Altın sarısı renk, berrak sitoplazma ve renal ven invazyonu Berrak Hücreli Renal Hücreli Karsinomun (ccRCC) patognomonik tablosudur."
        }
    ),
    make_slide(
        6,
        "Papiller Renal Hücreli Karsinom: MET Protoonkogeni ve Köpüksü Makrofajlar",
        "Kromozom 7 ve 17 Trizomisi, Papiller Mimarî ve Psammom Cisimcikleri",
        """Papiller Renal Hücreli Karsinom (pRCC), tüm böbrek kanserlerinin yaklaşık **%10-15'ini oluşturan ikinci en sık tiptir**. Distal veya proksimal konvolüt tübüllerden kaynaklanır.

**1. Genetik ve Moleküler Patogenez:**
• ccRCC'den tamamen farklı bir genetik mekanizmaya sahiptir; kromozom 3p delesyonu veya VHL mutasyonu **İÇERMEZ**.
• En karakteristik sitogenetik anormallik **Kromozom 7 ve Kromozom 17 trizomisi (trizomi 7 ve 17)** ve erkeklerde Y kromozomu kaybıdır.
• Kromozom 7 üzerinde yer alan hepatosit büyüme faktörü reseptörünü kodlayan **MET protoonkogeninde** mutasyon veya amplifikasyon izlenir. Hem ailesel herediter papiller RCC olgularında hem de sporadik formlarda MET sinyal yolağının aşırı aktivasyonu hücre proliferasyonunu sürdürür.
• Renal tümörler içinde **en sık multifokal ve bilateral olma eğilimi gösteren** karsinomdur.

**2. Morfolojik Özellikler:**
• **Makroskopi:** ccRCC gibi sarı değil; genellikle kahverengimsi-kırmızı, kistik dejenerasyon ve nekroz içeren, belirgin psödokapsüllü bir kitledir.
• **Mikroskopi:** İnce fibrovasküler korlar üzerinde dizilmiş tek veya çok sıralı kubik/silindirik epitel hücrelerinden oluşan **papiller yapılar**.
• **Patognomonik İpucu:** Papillaların fibrovasküler merkezinde (korlarında) bol miktarda **köpüksü makrofaj (foamy histiocyte) kümeleri** ve konsantrik laminasyonlu kalsifiye **Psammom cisimcikleri** izlenir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Papiller korların merkezinde 'köpüksü makrofaj kümeleri' ve Psammom cisimcikleri Papiller RCC için tanı koydurucudur; MET mutasyonu ve Trizomi 7/17 ile ilişkilidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Renal karsinomlar içinde multifokal ve iki taraflı (bilateral) görülme sıklığı en yüksek olan tip Papiller Renal Hücreli Karsinomdur.", "color": "sky"}
        ],
        {
            "id": "prac-tum-006",
            "question": "Böbrek rezeksiyon materyalinde bilateral multifokal kitleler izlenen hastada sitogenetikte trizomi 7 ve trizomi 17 saptanıyor. Mikroskopta fibrovasküler papiller korlar, psammom cisimcikleri ve köpüksü makrofajlar izlenen tümör hangisidir?",
            "options": [
                "A) Berrak hücreli karsinom",
                "B) Papiller renal hücreli karsinom",
                "C) Kromofob renal karsinom",
                "D) Renal onkositoma",
                "E) Medüller karsinom"
            ],
            "correctAnswer": 1,
            "explanation": "Trizomi 7/17, MET mutasyonu, papiller mimari, psammom cisimcikleri ve köpüksü makrofajlar Papiller RCC'nin karakteristik bulgularıdır."
        }
    ),
    make_slide(
        7,
        "Kromofob Renal Hücreli Karsinom: Bitki Hücresi Görünümü ve Perinükleer Halo",
        "Çoklu Hipodiploidi, 'Raisinoid' Nükleus ve Kolloidal Demir Pozitifliği",
        """Kromofob Renal Hücreli Karsinom (chRCC), böbrek kortikal toplayıcı kanallarının **interkale hücrelerinden** kaynaklanan, tüm RCC'lerin yaklaşık **%5'ini oluşturan** özel bir alt tiptir. Renal onkositoma ile aynı hücre kökenine sahiptir.

**1. Sitogenetik Özellikler:**
• ccRCC veya pRCC'deki gibi spesifik bir gen amplifikasyonundan ziyade **aşırı kromozom kayıpları (yaygın hipodiploidi)** karakteristiktir.
• Özellikle kromozom 1, 2, 6, 10, 13, 17 ve 21'in monozomisi (kaybı) saptanır.

**2. Mikroskobik Morfoloji:**
• **Belirgin Hücre Sınırları ('Bitki Hücresi' Manzarası):** Hücre membranları çok kalın ve koyu sınırlıdır; adeta bitki hücre duvarlarını andırır.
• **Soluk Retiküler Sitoplazma:** Sitoplazma soluk pembe renkte ve ince vakuollüdür.
• **Perinükleer Halo ve Kuru Üzüm Nükleus:** Nükleusların çevresinde açık berrak bir boşluk (**perinükleer halo**) bulunur. Nükleuslar düzensiz, buruşuk ve girintili çıkıntılıdır; kuru üzüme benzetildiği için **'raisinoid nucleus'** olarak tanımlanır.
• **Hale Kolloidal Demir Boyası:** Mikrodivertiküler vezikülleri içerdiği için sitoplazma Hale kolloidal demir boyası ile diffüz mavi pozitif boyanır (Onkositomadan ayrımda kritiktir).

**3. Prognoz:**
ccRCC ve pRCC ile karşılaştırıldığında **prognozu açık ara en iyi olan RCC alt tipidir**; metastaz oranı %5'in altındadır.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Bitki hücresi benzeri belirgin sınırlar, kuru üzüm (raisinoid) nükleus, perinükleer halo ve Hale kolloidal demir pozitifliği Kromofob RCC için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Kromofob RCC interkale hücrelerden kaynaklanır; çoklu kromozom kayıpları içerir ve temel böbrek kanserleri içinde prognozu en mükemmel olandır.", "color": "sky"}
        ],
        {
            "id": "prac-tum-007",
            "question": "Böbrek kitlesi rezeke edilen hastanın biyopsisinde hücrelerin bitki hücresi gibi çok belirgin sınırlara sahip olduğu, sitoplazmada nükleus etrafında berrak bir halo (perinükleer halo) ve büzüşmüş 'kuru üzüm' benzeri nükleus bulunduğu görülüyor. Hale kolloidal demir boyası pozitif saptanan ve prognozu çok iyi olan bu tümör hangisidir?",
            "options": [
                "A) Berrak hücreli karsinom",
                "B) Kromofob renal hücreli karsinom",
                "C) Wilms tümörü",
                "D) Renal sarkom",
                "E) Toplayıcı kanal karsinomu"
            ],
            "correctAnswer": 1,
            "explanation": "Bitki hücresi sınırları, perinükleer halo, raisinoid nükleus ve kolloidal demir pozitifliği mükemmel prognozlu Kromofob RCC'nin ayırt edici özellikleridir."
        }
    ),
    make_slide(
        8,
        "Wilms Tümörü (Nefroblastom): Çocukluk Çağının Nefrojenik Malignitesi",
        "Trifazik Histoloji (Blastem, Epitel, Stroma), WT1/WT2 Mutasyonları ve Nefrojenik Kalıntılar",
        """Wilms tümörü (Nefroblastom), 2 ila 5 yaş arasındaki çocuklarda böbreğin açık ara **en sık primer malign tümörüdür** (pediyatrik böbrek kanserlerinin %95'i). Primitif nefrojenik blastemin embriyonik kalıntılarından köken alır.

**1. Klasik Trifazik Histopatoloji:**
Wilms tümörü klasik olarak üç embriyonik doku komponentinin birlikteliği ile karakterizedir:
1. **Blastemal Komponent:** Yuvarlak, küçük, hiperkromatik mavi çekirdekli primitif mezenkimal hücre tabakaları ('küçük yuvarlak mavi hücreli tümör').
2. **Epitelyal Komponent:** Embriyonik tübülleri ve abortif glomerül taslaklarını (**glomerüloid cisimcikler**) andıran yapılar.
3. **Stromal Komponent:** İğsi hücreli miksoid bağ dokusu, düz kas, iskelet kası (rabdomiyoblastlar), kıkırdak ve yağ odakları.

**2. Nefrojenik Kalıntılar (Nephrogenic Rests):**
Tümör çevresindeki böbrek parankiminde persiste eden embriyonik blastem odaklarıdır. Wilms tümörünün öncül (prekürsör) lezyonlarıdır; karşı böbrekte de bulunması bilateral Wilms tümörü riskini işaret eder.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Blastemal küçük mavi hücreler, abortif tübül/glomerüloid epitelyal yapılar ve miksoid stromal komponentten oluşan 'Trifazik Histoloji' Wilms Tümörü için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Wilms tümörünün prekürsör lezyonu 'nefrojenik kalıntılar'dır (nephrogenic rests); bilateral tümör gelişiminin habercisidir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-008",
            "question": "3 yaşındaki bir çocuğun karnında saptanan dev kitle nedeniyle yapılan nefrektomide mikroskopta primitif blastemal mavi hücreler, abortif glomerüloid yapılar ve iğsi hücreli stroma birlikteliği (trifazik patern) izleniyor. Tanı nedir?",
            "options": [
                "A) Nöroblastom",
                "B) Wilms tümörü (Nefroblastom)",
                "C) Renal berrak hücreli karsinom",
                "D) Rabdomiyosarkom",
                "E) Ewing sarkomu"
            ],
            "correctAnswer": 1,
            "explanation": "Çocukluk çağında blastem, epitel ve stromadan oluşan trifazik histoloji Wilms Tümörünün (Nefroblastom) klasik patolojik imzasıdır."
        }
    ),
    make_slide(
        9,
        "Wilms Tümörü ile İlişkili Genetik Sendromlar: WAGR, Denys-Drash ve Beckwith-Wiedemann",
        "WT1 (11p13) ve WT2 (11p15 - IGF2 İmpringing Bozukluğu), Anaplazi ve TP53",
        """Wilms tümörlerinin yaklaşık %10'u doğumsal genetik sendromlar zemininde gelişir. Bu sendromlar kromozom 11p bölgesindeki genlerle ilişkilidir.

**1. WT1 Geni İlişkili Sendromlar (Kromozom 11p13):**
• **WAGR Sendromu:** 11p13 mikrodelesyonu sonucu yan yana bulunan *WT1* ve *PAX6* genleri kaybolur:
  - **W:** Wilms tümörü (%33 risk),
  - **A:** Aniridi (göz irisinin yokluğu — *PAX6* geni kaybı),
  - **G:** Genitoüriner anomaliler (kriptorşidizm, hipospadias),
  - **R:** Retardasyon (zihinsel gerilik).
• **Denys-Drash Sendromu:** *WT1* geninde missense mutasyon:
  - Wilms tümörü riski **%90**,
  - Erken başlangıçlı nefrotik sendrom (diffüz mezangiyal skleroz),
  - Erkek psödohermafroditizmi (gonadal disgenezi).

**2. WT2 Geni İlişkili Sendrom (Kromozom 11p15 - Beckwith-Wiedemann Sendromu):**
• Genomik imprinting (damgalama) bozukluğu sonucu maternal allelin kaybı ve babadan gelen *IGF2* (İnsülin benzeri büyüme faktörü-2) aşırı ekspresyonu.
• **Klinik Triad:** Organomegali (karaciğer, böbrek büyümesi), **Makroglossi** (dev dil), **Omfalosel** (karın duvarı defekti) ve hemihipertrofi. Wilms tümörü ve hepatoblastom riski artar.

**3. Anaplazi ve TP53:**
Wilms tümöründe fokal veya diffüz anaplazi (dev atipik nükleuslar, atipik mitozlar) **TP53 mutasyonunu** yansıtır; kemoterapiye direnç ve kötü prognozun 1 numaralı belirtecidir.""",
        [
            {"type": "warning", "badge": "🔴 GENETİK KODLAMA", "text": "Aniridi + Wilms = WAGR (WT1 + PAX6); Nefrotik sendrom + Wilms + Psödohermafroditizm = Denys-Drash; Makroglossi + Omfalosel + Wilms = Beckwith-Wiedemann (11p15/IGF2).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Wilms tümöründe kemoterapiye direncin ve kötü prognozun en güçlü histolojik göstergesi 'anaplazi' varlığıdır ve TP53 mutasyonu ile ilişkilidir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-009",
            "question": "Doğumda makroglossi (büyük dil), omfalosel ve vücudun sağ yarısında belirgin büyüme (hemihipertrofi) saptanan 2 yaşındaki bir bebekte karında saptanan kitlenin en olası tanısı ve sorumlu genetik bölge hangisidir?",
            "options": [
                "A) Nöroblastom — N-MYC amplifikasyonu",
                "B) Beckwith-Wiedemann sendromu ilişkili Wilms tümörü — Kromozom 11p15 (WT2 / IGF2)",
                "C) WAGR sendromu — Kromozom 13q14",
                "D) Denys-Drash sendromu — Kromozom 3p25",
                "E) Li-Fraumeni sendromu — TP53"
            ],
            "correctAnswer": 1,
            "explanation": "Makroglossi, omfalosel ve hemihipertrofi Beckwith-Wiedemann sendromunun (11p15 / IGF2 imprinting bozukluğu) bulgularıdır ve Wilms tümörü riskini belirgin artırır."
        }
    ),
    make_slide(
        10,
        "Renal Hücreli Karsinomda Klinik Tablo ve Klasik Triad",
        "Ağrısız Makroskopik Hematüri, Yan Ağrısı ve Palpabl Kitle",
        """Renal Hücreli Karsinom tarihsel olarak 'dahiliyecinin tümörü' (internist's tumor) olarak adlandırılmıştır; zira klinik bulguları son derece sinsi, değişken ve sistemik semptomlarla perdelenmiş olabilir.

**1. Klasik Klinik Triad:**
1. **Hematüri (%50-60):** En sık görülen başvuru bulgusudur; aralıklı, ağrısız, makroskopik veya mikroskopik olabilir.
2. **Yan Ağrısı (Flank Pain) (%40):** Tümörün böbrek kapsülünü germesi veya üreteri tıkayan kan pıhtılarına bağlıdır.
3. **Palpabl Abdominal Kitle (%30-40):** Özellikle zayıf hastalarda ve alt kutup yerleşimli büyük tümörlerde palpe edilir.
• **En Kritik Sınav İpucu:** Bu klasik triad (hematüri + ağrı + kitle) hastaların **yalnızca %10'unda bir arada bulunur!** Triadın tam olarak mevcut olması genellikle hastalığın ileri evreye ulaştığını gösterir.

**2. İnsidental Yakalama (Rastlantısal Teşhis):**
Günümüzde ultrasonografi ve BT'nin yaygın kullanımı sayesinde RCC olgularının **%50'sinden fazlası tamamen asemptomatik iken**, başka nedenlerle yapılan batın görüntülemelerinde tesadüfen (insidentaloma) yakalanmaktadır.""",
        [
            {"type": "clinical", "badge": "🔴 KLİNİK GERÇEK", "text": "RCC'nin klasik triadı olan 'Hematüri + Yan Ağrısı + Kitle' hastaların sadece %10'unda bir arada bulunur; günümüzde hastaların yarıdan fazlası asemptomatik rastlantısal tümörlerdir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SPOTU", "text": "RCC'nin en sık görülen başvuru semptomu 'makroskopik veya mikroskopik hematüri'dir (%60).", "color": "sky"}
        ],
        {
            "id": "prac-tum-010",
            "question": "Renal hücreli karsinomun (RCC) klasik semptom triadı olan hematüri, yan ağrısı ve palpabl kitle tablosunun hastaların tanı anında bir arada bulunma oranı yaklaşık ne kadardır?",
            "options": [
                "A) %10",
                "B) %50",
                "C) %75",
                "D) %90",
                "E) %100"
            ],
            "correctAnswer": 0,
            "explanation": "Klasik triad (hematüri, ağrı, palpabl kitle) hastaların yalnızca yaklaşık %10'unda bir arada izlenir ve genellikle ileri evre hastalığı simgeler."
        }
    ),
    make_slide(
        11,
        "RCC ve Paraneoplastik Sendromlar: Hormonlar ve Stauffer Sendromu",
        "Eritropoietin (Polisitemi), PTHrP (Hiperkalsemi), Renin (Hipertansiyon) ve Hepatik Disfonksiyon",
        """RCC, çeşitli hormon ve sitokin benzeri molekülleri ektopik olarak salgılama yeteneği nedeniyle en sık paraneoplastik sendrom oluşturan malignitelerden biridir (hastaların %10-15'inde görülür).

**1. Başlıca Paraneoplastik Salgılar ve Klinikler:**
• **Polisitemi (%5-10):** Tümör hücrelerinin ektopik **Eritropoietin (EPO)** salgılaması sonucu hemoglobin ve hematokrit aşırı yükselir. (Diğer taraftan kronik hastalık anemisi daha sıktır).
• **Hiperkalsemi:** Kemik metastazı olmaksızın tümörden salgılanan **Paratiroid Hormon İlişkili Peptit (PTHrP)** nedeniyle gelişir.
• **Hipertansiyon:** Tümör hücrelerinin doğrudan **Renin** salgılaması veya tümör basısına bağlı renal iskemi sonucu gelişir.
• **Cushing Sendromu:** Ektopik ACTH üretimi.
• **Jinekomasti ve Galaktore:** Gonadotropin salınımı.
• **AA Tipi Sekonder Amiloidoz:** Kronik IL-6 uyarısına bağlı SAA proteininin birikmesi.

**2. Stauffer Sendromu:**
Renal hücreli karsinomun karaciğere metastazı OLMADAN, tümörden salgılanan interlökin-6 (IL-6) nedeniyle karaciğer fonksiyon testlerinin (özellikle alkalen fosfataz ve bilirubin) bozulması, hepatomegali ve ateş tablosudur. Tümör cerrahi olarak çıkarıldığında hepatik disfonksiyon tamamen düzelir!""",
        [
            {"type": "warning", "badge": "🔴 PARANEOPLASTİK SENDROM", "text": "Metastaz olmadan gelişen karaciğer disfonksiyonu 'Stauffer Sendromu' olarak adlandırılır; tümörün nefrektomi ile çıkarılmasıyla karaciğer fonksiyonları normale döner.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "RCC'de en sık görülen paraneoplastik sendromlar hiperkalsemi (PTHrP) ve polisitemidir (EPO).", "color": "sky"}
        ],
        {
            "id": "prac-tum-011",
            "question": "Böbrek kitlesi saptanan bir hastada karaciğer metastazı olmadığı halde serum alkalen fosfataz ve bilirubin düzeyleri yüksek bulunuyor, hepatomegali izleniyor. Nefrektomi sonrası karaciğer testleri tamamen normale dönüyor. Bu paraneoplastik tablo hangisidir?",
            "options": [
                "A) Cushing sendromu",
                "B) Stauffer sendromu",
                "C) Budd-Chiari sendromu",
                "D) Gilbert sendromu",
                "E) Zollinger-Ellison sendromu"
            ],
            "correctAnswer": 1,
            "explanation": "Renal hücreli karsinomda metastaz olmaksızın gelişen ve nefrektomi sonrası düzelen paraneoplastik hepatik disfonksiyon tablosu Stauffer Sendromudur."
        }
    ),
    make_slide(
        12,
        "RCC Yayılım Yolları: Vasküler Trombüs, Lenfatik ve Organ Metastazları",
        "Renal Ven, VCI, Akciğer (Top Mermisi), Kemik (Litik) ve Atipik Böbrek Metastazları",
        """RCC, erken dönemde hematojen yolla yayılabilen son derece agresif bir biyolojiye sahiptir.

**1. Doğrudan ve Vasküler Yayılım:**
• Tümör böbrek kapsülünü aşarak perirenal yağ dokusuna (Gerota fasyası içine) yayılabilir.
• **Vasküler Yayılım:** Tümör hücreleri renal ven endotelini invaze ederek intralüminal polipoid bir trombüs oluşturur. Bu trombüs **Vena Cava Inferior boyunca büyüyerek diyaframı geçip sağ atriyuma kadar uzanabilir!** Sağ testiküler/sol testiküler ven tıkanması sonucu sol tarafta ani gelişen varikosel (sağda da olabilir) RCC habercisi olabilir.

**2. Metastaz Organları:**
• **Akciğerler (%50+):** En sık uzak metastaz yeridir; akciğer grafisinde karakteristik yuvarlak, düzgün sınırlı **'top mermisi' (cannonball) metastazları** oluşturur.
• **Kemikler (%33):** Genellikle ağrılı ve patolojik kırıklara yol açan **saf osteolitik** metastazlar yapar.
• **Bölgesel Lenf Nodları (%30):** Paraaortik ve interaortokaval lenf nodları.
• **Karaciğer, Beyin ve Adrenal Bez.**
• **Atipik Metastazlar:** Tiroid bezi ve pankreas gibi diğer tümörlerin çok nadir metastaz yaptığı organlara metastaz yapabilme özelliğiyle bilinir.""",
        [
            {"type": "clinical", "badge": "🔴 FİZİK MUAYENE İPUCU", "text": "Özellikle ileri yaş bir erkekte yeni başlayan ve sırtüstü yatmakla kaybolmayan SOL varikosel sol renal venin tümör trombüsüyle tıkandığını düşündürmelidir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "RCC en sık akciğere ('top mermisi' lezyonlar) ve kemiğe (saf osteolitik) metastaz yapar; renal ven/VCI invazyonu karakteristiktir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-012",
            "question": "62 yaşındaki bir erkek hastada sol tarafta yeni başlayan, yatmakla küçülmeyen varikosel ve akciğer grafisinde 'top mermisi' görünümünde bilateral yuvarlak kitleler saptanıyor. En olası primer odak hangisidir?",
            "options": [
                "A) Prostat karsinomu",
                "B) Renal hücreli karsinom",
                "C) Mide adenokarsinomu",
                "D) Kolon karsinomu",
                "E) Testis seminomu"
            ],
            "correctAnswer": 1,
            "explanation": "Sol renal venin tümör trombüsüyle tıkanması sol testiküler venöz drenajı bozarak sol varikosele yol açar; akciğere top mermisi metastazı Renal Hücreli Karsinom için klasiktir."
        }
    ),
    make_slide(
        13,
        "Böbrek Tümörlerinde Evreleme: TNM Sistemi ve Gerota Fasyası Kuralı",
        "T1'den T4'e Anatomik Sınırlar ve Bölgesel Lenf Nodu Değerlendirmesi",
        """Renal Hücreli Karsinomun prognozunu belirleyen en temel parametre anatomik TNM evresidir.

**1. Primer Tümör (T) Evrelemesi (AJCC/UICC):**
• **T1:** Tümör böbrek kapsülü içinde sınırlıdır ve en büyük çapı **≤ 7 cm**'dir.
  - *T1a:* Çap ≤ 4 cm (Parsiyel nefrektomi için ideal grup).
  - *T1b:* Çap > 4 cm ama ≤ 7 cm.
• **T2:** Tümör böbreğe sınırlıdır ancak en büyük çapı **> 7 cm**'dir.
  - *T2a:* > 7 cm ama ≤ 10 cm.
  - *T2b:* > 10 cm.
• **T3:** Tümör ana renal vene yayılmıştır VEYA Gerota fasyasını aşmadan perirenal / pelvik yağ dokusuna uzanmıştır:
  - *T3a:* Perirenal yağ dokusu / renal sinüs yağı invazyonu VEYA renal ven dal invazyonu.
  - *T3b:* Diyafram altındaki Vena Cava Inferior'a uzanan tümör trombüsü.
  - *T3c:* Diyafram üstündeki VCI'ya veya sağ atriyuma uzanan tümör trombüsü.
• **T4:** Tümör **Gerota fasyasını kesin olarak aşmıştır** VEYA aynı taraf sürrenal (adrenal) bezine doğrudan bitişik yayılım göstermiştir.

**2. Nodal (N) ve Metastaz (M) Evresi:**
• **N0:** Bölgesel lenf nodu metastazı yok; **N1:** Bölgesel lenf nodu metastazı var.
• **M0:** Uzak metastaz yok; **M1:** Uzak organ metastazı var.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK EVRE EŞİĞİ", "text": "Böbreğe sınırlı tümörlerde T1 (≤7 cm) ile T2 (>7 cm) sınırı 7 santimetredir; 4 cm altındaki T1a tümörlerde nefron koruyucu cerrahi (parsiyel nefrektomi) altın standarttır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Tümörün renal ven veya Vena Cava Inferior içine uzanması lezyonu T3 evresine sokar; Gerota fasyasının aşılması ise doğrudan T4'tür.", "color": "sky"}
        ],
        {
            "id": "prac-tum-013",
            "question": "Böbrek kesitinde 5 cm çapında olan ancak renal ven ana kökünü invaze ederek lümeni tıkayan bir renal hücreli karsinomun TNM sistemindeki T evresi aşağıdakilerden hangisidir?",
            "options": [
                "A) T1b",
                "B) T2a",
                "C) T3a",
                "D) T3b",
                "E) T4"
            ],
            "correctAnswer": 2,
            "explanation": "Tümörün renal ven veya sinüs yağını invaze etmesi boyuttan bağımsız olarak lezyonu T3a evresine taşır."
        }
    ),
    make_slide(
        14,
        "WHO / ISUP Nükleer Derecelendirme Sistemi (Fuhrman Modifikasyonu)",
        "Nükleol Belirginliği, Kromatin Yapısı ve Pleomorfizme Göre Derece 1-4",
        """Berrak hücreli ve papiller RCC'de histolojik nükleer derece, tümörün biyolojik agresifliğini ve metastaz potansiyelini öngören bağımsız bir prognostik faktördür. Günümüzde klasik Fuhrman sınıflaması yerini Dünya Sağlık Örgütü ve Uluslararası Ürolojik Patoloji Derneği'nin **(WHO/ISUP) Nükleer Derecelendirme Sistemine** bırakmıştır.

**1. WHO/ISUP Derecelendirme Kriterleri (Nükleol Odaklı):**
• **Derece 1 (Grade 1):** Nükleoller x400 büyütmede dahi görünmez veya belirsizdir; nükleuslar küçük, yuvarlak ve monotondur.
• **Derece 2 (Grade 2):** Nükleoller x400 büyük büyütmede açıkça seçilebilir, ancak x100 küçük büyütmede görülmez.
• **Derece 3 (Grade 3):** Nükleoller x100 küçük büyütmede dahi belirgin ve göze çarpıcıdır; nükleer pleomorfizm belirgindir.
• **Derece 4 (Grade 4):** Ağır nükleer pleomorfizm, multinükleer dev tümör hücreleri VEYA tümörde **sarkomatoid / rabdoid diferansiasyon** varlığı. Sarkomatoid diferansiasyon varlığı diğer alanların derecesine bakılmaksızın tümörü doğrudan Derece 4 yapar ve en kötü prognozu simgeler!""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Bir RCC'de sarkomatoid diferansiasyon (iğsi hücreli atipik alanlar) görülmesi tümörü doğrudan WHO/ISUP Derece 4 yapar ve kemodirençli agresif gidişi gösterir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "WHO/ISUP sisteminde derecelendirme nükleolün x100 ve x400 büyütmedeki görünürlüğüne dayanır.", "color": "sky"}
        ],
        {
            "id": "prac-tum-014",
            "question": "Böbrek rezeksiyonunda berrak hücreli RCC tanısı alan bir tümörün histopatolojik incelemesinde yer yer malign iğsi hücreler içeren 'sarkomatoid diferansiasyon' alanları saptanıyor. Bu tümörün WHO/ISUP nükleer derecesi kaçtır?",
            "options": [
                "A) Derece 1",
                "B) Derece 2",
                "C) Derece 3",
                "D) Derece 4",
                "E) Derecelendirilemez"
            ],
            "correctAnswer": 3,
            "explanation": "Sarkomatoid veya rabdoid diferansiasyonun varlığı, diğer nükleer özelliklerden bağımsız olarak tümörü doğrudan en yüksek derece olan WHO/ISUP Derece 4 yapar."
        }
    ),
    make_slide(
        15,
        "Diğer Nadir Renal Karsinom Tipleri: Toplayıcı Kanal ve Medüller Karsinom",
        "Bellini Kanalları, Desmoplazi, Orak Hücreli Anemi Taşıyıcılığı ve INI-1 Kaybı",
        """RCC'lerin %1-2'sini oluşturan toplayıcı kanal karsinomları böbrek medullasından kaynaklanır ve son derece ölümcül seyreder.

**1. Toplayıcı Kanal Karsinomu (Bellini Kanalı Karsinomu):**
• Renal medulladaki Bellini toplayıcı kanallarından köken alır.
• **Morfoloji:** Medullada yerleşen, düzensiz tübüller ve kordonlar oluşturan atipik hücreler ve çevresinde son derece yoğun, sert **desmoplastik stroma reaksiyonu**.
• Tanı anında olguların %70'inde bölgesel veya uzak metastaz mevcuttur; klasik kemoterapiye yanıtsızdır.

**2. Renal Medüller Karsinom:**
• Neredeyse münhasıran **Orak Hücreli Anemi Taşıyıcısı (HbAS)** veya hastası olan genç siyahilerde görülür.
• Medülladaki kronik hipoksi ve oraklaşma zemininde gelişir.
• **Genetik İmzası:** **SMARCB1 (INI-1)** tümör süpresör geninin çift alelik kaybıdır; immünohistokimyada nükleer INI-1 boyanması tamamen kaybolur.
• İnanılmaz derecede agresiftir; tanı anında hemen tüm hastalarda uzak metastaz mevcuttur ve ortalama sağkalım birkaç aydır.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BİRLİKTELİK", "text": "Genç orak hücreli anemi taşıyıcısında saptanan böbrek kanseri 'Renal Medüller Karsinom'dur; INI-1 (SMARCB1) kaybı ile karakterizedir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Toplayıcı kanal karsinomu Bellini kanallarından köken alır ve yoğun desmoplazi içerir; medüller karsinom ise orak hücre zemininde gelişir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-015",
            "question": "Orak hücreli hemoglobinopati (HbAS) taşıyıcısı olan 22 yaşındaki siyahi bir erkekte hızla büyüyen medüller yerleşimli böbrek kitlesi saptanıyor. Biyopside nükleer INI-1 (SMARCB1) protein ekspresyonunun kaybolduğu saptanıyor. Tanı nedir?",
            "options": [
                "A) Berrak hücreli karsinom",
                "B) Renal medüller karsinom",
                "C) Renal onkositoma",
                "D) Anjiyomiyolipom",
                "E) Papiller karsinom tip 1"
            ],
            "correctAnswer": 1,
            "explanation": "Orak hücre zemininde genç bireylerde gelişen ve INI-1 kaybı gösteren son derece agresif medüller tümör Renal Medüller Karsinomdur."
        }
    ),
    make_slide(
        16,
        "Renal Papiller Adenom ve Karsinom Ayrım Kriterleri",
        "Kortikal Küçük Papiller Lezyonlar: 15 mm ve 5 mm Eşik Tartışması",
        """Renal papiller adenomlar, böbrek korteksinde son derece sık rastlanan (otopsilerde %20-40) mikroskopik benign glandüler lezyonlardır.

**1. Morfolojik Özellikler:**
• Boyutları genellikle 1-3 mm çapında, soluk sarı-gri renkli, kapsülsüz küçük nodüllerdir.
• Mikroskobik olarak papiller böbrek hücreli karsinom ile **morfolojik ve sitogenetik olarak (trizomi 7 ve 17) birebir aynıdır!**

**2. Ayırıcı Tanı Kriteri (Boyut Eşiği):**
• Papiller bir proliferasyonun 'adenom' mu yoksa 'karsinom' mu kabul edileceği tarihsel olarak boyut kriterine dayanır.
• Klasik kitaplarda ve Robbins Patolojide malignite potansiyeli sınırı **15 mm (1.5 cm)** kabul edilirken; güncel WHO sınıflamasında bu sınır **5 mm (0.5 cm)** seviyesine çekilmiştir.
• 5 mm altındaki papiller lezyonlar 'papiller adenom' kabul edilirken; 5 mm'yi aşan veya nükleer atipi gösteren tüm lezyonlar 'Papiller Renal Hücreli Karsinom' olarak rapor edilir.""",
        [
            {"type": "clinical", "badge": "🔴 PATOLOJİK AYRIM", "text": "Papiller adenom ile papiller karsinom mikroskobik olarak ayırt edilemez; ayrım tamamen lezyonun çapına ve nükleer özelliklerine dayanır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Böbrek korteksinde rastlantısal saptanan birkaç milimetrelik küçük sarı papiller lezyonlar 'Renal Papiller Adenom'dur.", "color": "sky"}
        ],
        {
            "id": "prac-tum-016",
            "question": "Böbrek otopsisinde kortekste subkapsüler yerleşimli 3 mm çapında iyi sınırlı sarı lezyon saptanıyor. Mikroskopta papiller mimari izlenen bu asemptomatik küçük lezyonun en olası tanısı hangisidir?",
            "options": [
                "A) Renal papiller adenom",
                "B) İleri evre Berrak hücreli karsinom",
                "C) Toplayıcı kanal karsinomu",
                "D) Wilms tümörü",
                "E) Malakoplaki"
            ],
            "correctAnswer": 0,
            "explanation": "Böbrek korteksinde birkaç milimetre çapında papiller mimari gösteren benign lezyonlar Renal Papiller Adenom olarak adlandırılır."
        }
    ),
    make_slide(
        17,
        "Kistik Renal Karsinomlar: Kistik Berrak Hücreli RCC ve Multiloküler Kistik Neoplazm",
        "Düşük Malign Potansiyelli Multiloküler Kistik Renal Neoplazm (MCLCRCC)",
        """Tümörlerin kistik dejenerasyonu ile gerçek kistik renal neoplazmlar arasında biyolojik davranış açısından keskin bir fark vardır.

**1. Sekonder Kistik Dejenerasyon:**
Büyük berrak hücreli veya papiller karsinomların merkezinde hızlı büyüme ve iskemik nekroza bağlı psödokistler oluşabilir; agresif seyreder.

**2. Düşük Malign Potansiyelli Multiloküler Kistik Renal Neoplazm:**
• Eskiden kistik berrak hücreli karsinom olarak adlandırılan, güncel WHO sınıflamasında benign seyri nedeniyle bu adı alan antitedir.
• **Morfoloji:** Tamamen fibröz septalarla ayrılmış çok sayıda kistik boşluktan oluşur; solid tümör kitlesi **asla içermez**.
• Kistlerin içini döşeyen ve fibröz septalarda tek tük kümelenen hücreler berrak sitoplazmalıdır (VHL mutasyonu taşır).
• **Prognoz:** Metastaz potansiyeli **SIFIRDIR (%0)**. Cerrahi rezeksiyon ile %100 tam şifa sağlanır.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Multiloküler kistik renal neoplazmda hiçbir solid büyüme odağı bulunmamalıdır; solid alan varlığı klasik berrak hücreli RCC tanısını gerektirir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Düşük malign potansiyelli multiloküler kistik neoplazm berrak hücreler içermesine rağmen metastaz yapmaz (%0 nüks/metastaz).", "color": "sky"}
        ],
        {
            "id": "prac-tum-017",
            "question": "Böbrekte çok sayıda kistik boşluktan oluşan, septalarında berrak hücreler izlenen ancak hiçbir solid tümör nodülü içermeyen lezyonun metastaz potansiyeli nedir?",
            "options": [
                "A) %80 metastaz yapar",
                "B) %50 bölgesel lenf noduna yayılır",
                "C) Metastaz yapmaz (%0 metastaz potansiyeli)",
                "D) Sadece beyne metastaz yapar",
                "E) Sadece kemik iliğine yayılır"
            ],
            "correctAnswer": 2,
            "explanation": "Düşük malign potansiyelli multiloküler kistik renal neoplazmda solid alan bulunmadığı sürece metastaz riski %0'dır."
        }
    ),
    make_slide(
        18,
        "Renal Hücreli Karsinomlarda İmmünohistokimyasal Belirteç Haritası",
        "CD10, RCC Antijeni, CK7, AMACR (Racemase) ve Kolloidal Demir",
        """RCC alt tiplerinin kesin histolojik ayırıcı tanısında immünohistokimya (İHK) vazgeçilmez bir tanısal paneldir.

**1. Başlıca Belirteçler ve Boyanma Profili:**
• **Berrak Hücreli RCC (ccRCC):**
  - **CD10:** Pozitif (proksimal tübül fırçamsı kenar belirteci).
  - **RCC Antijeni:** Kuvvetli pozitif.
  - **Vimentin:** Pozitif.
  - **Sitokeratin 7 (CK7):** NEGATİF (önemli ayırıcı tanı!).
• **Papiller RCC (pRCC):**
  - **CK7:** Diffüz kuvvetli POZİTİF.
  - **AMACR (Alfa-metilasil-KoA rasemaz):** Karakteristik granüler pozitif.
  - **CD10:** Pozitif.
• **Kromofob RCC (chRCC):**
  - **CK7:** Diffüz sitoplazmik POZİTİF.
  - **CD10 ve Vimentin:** NEGATİF.
  - **Hale Kolloidal Demir:** Diffüz sitoplazmik retiküler mavi boyanma.
• **Onkositoma:**
  - **CK7:** Negatif veya sadece tek tük hücrelerde dağınık pozitif.
  - **Hale Kolloidal Demir:** Sadece apikal/negatif boyanma.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK AYRIM", "text": "Berrak hücreli RCC'de CK7 negatiftir; Papiller ve Kromofob RCC'de ise CK7 diffüz pozitiftir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Papiller karsinomun en spesifik immünohistokimyasal belirteci AMACR (Racemase) ve CK7'dir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-018",
            "question": "Böbrek tümörleri ayırıcı tanısında CK7 diffüz pozitif, AMACR (racemase) kuvvetli granüler pozitif boyanan tümör alt tipi hangisidir?",
            "options": [
                "A) Berrak hücreli karsinom",
                "B) Papiller renal hücreli karsinom",
                "C) Renal onkositoma",
                "D) Anjiyomiyolipom",
                "E) Toplayıcı kanal karsinomu"
            ],
            "correctAnswer": 1,
            "explanation": "CK7 ve AMACR (alfa-metilasil-KoA rasemaz) ko-pozitifliği Papiller Renal Hücreli Karsinom için karakteristik İHK profildir."
        }
    ),
    make_slide(
        19,
        "Herediter Renal Karsinom Sendromları",
        "Von Hippel-Lindau, Herediter Papiller Karsinom ve Birt-Hogg-Dubé Sendromu",
        """Tüm böbrek kanserlerinin yaklaşık %3-5'i ailesel otozomal dominant kalıtılan genetik sendromlar zemininde gelişir. Bu olgular erken yaşta, bilateral ve multifokal tümörlerle karakterizedir.

**1. Von Hippel-Lindau (VHL) Sendromu:**
• *VHL* geni (3p25) germline mutasyonu.
• **Tümör Spektrumu:** Bilateral multifokal **Berrak Hücreli RCC**, Serebellar ve retinal **hemanjiyoblastomlar**, Feokromositoma, pankreas kistleri ve nöroendokrin tümörler.

**2. Herediter Papiller Renal Karsinom (HPRCC):**
• *MET* protoonkogeni (7q31) germline mutasyonu. Bilateral multifokal **Papiller RCC Tip 1**.

**3. Birt-Hogg-Dubé (BHD) Sendromu:**
• *FLCN* geni (Folikülin, 17p11) mutasyonu.
• Yüzde kutanöz **fibrofolikülomlar**, akciğer kistleri, spontan pnömotoraks ve böbrekte **Kromofob RCC ile Onkositoma** birlikteliği (Onkositozis).

**4. Herediter Leiomiyomatozis ve Renal Hücreli Karsinom (HLRCC):**
• Fumarat Hidrataz (*FH*) mutasyonu; uterin ve kutanöz leiomiyomlar ve son derece agresif papiller RCC Tip 2.""",
        [
            {"type": "warning", "badge": "🔴 GENETİK EŞLEŞTİRME", "text": "Serebellar hemanjiyoblastom + Feokromositoma + ccRCC = VHL; Ciltte fibrofolikülom + Kromofob/Onkositoma = Birt-Hogg-Dubé.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Von Hippel-Lindau sendromunda en sık ölüm nedeni bilateral berrak hücreli renal karsinom veya santral sinir sistemi hemanjiyoblastomlarıdır.", "color": "sky"}
        ],
        {
            "id": "prac-tum-019",
            "question": "Cildinde fibrofolikülomlar, akciğer tomografisinde kistler ve bilateral böbrek tümörleri (kromofob RCC ve onkositoma) saptanan bir hastada mutasyona uğramış gen hangisidir?",
            "options": [
                "A) VHL",
                "B) FLCN (Folikülin / Birt-Hogg-Dubé)",
                "C) MET",
                "D) WT1",
                "E) TSC1"
            ],
            "correctAnswer": 1,
            "explanation": "Fibrofolikülomlar, pulmoner kistler ve kromofob RCC/onkositoma birlikteliği FLCN mutasyonuna bağlı Birt-Hogg-Dubé sendromunun tablosudur."
        }
    ),
    make_slide(
        20,
        "RCC'de Cerrahi Tedavi ve Sistemik Tedavi Stratejileri",
        "Parsiyel Nefrektomi, Tirozin Kinaz İnhibitörleri ve İmmün Kontrol Noktası Blokajı",
        """RCC klasik sitotoksik kemoterapiye ve radyoterapiye son derece dirençlidir; bu nedenle tedavi cerrahi rezeksiyona ve hedefe yönelik moleküler ajanlara dayanır.

**1. Cerrahi Tedavi İlkeleri:**
• **Parsiyel Nefrektomi (Nefron Koruyucu Cerrahi):** ≤4 cm (T1a) tümörlerde, soliter böbrekte veya bilateral tümörlerde altın standarttır; onkolojik sonuçları radikal nefrektomi ile eşdeğerdir.
• **Radikal Nefrektomi:** Böbreğin Gerota fasyası, perirenal yağ dokusu ve aynı taraf adrenal bezle birlikte çıkarılmasıdır; >7 cm veya santral yerleşimli lezyonlarda uygulanır.

**2. Metastatik Hastalıkta Sistemik Tedavi:**
• Klasik kemoterapi etkisizdir (tümör hücrelerinde P-glikoprotein çok yüksektir).
• **VEGF ve Tirozin Kinaz İnhibitörleri (TKI):** Sunitinib, Kabozantinib, Aksitinib (VHL-HIF-VEGF anjiyogenez yolağını bloke eder).
• **mTOR İnhibitörleri:** Everolimus, Temsirolimus.
• **İmmün Kontrol Noktası İnhibitörleri (Checkpoint İnhibitörleri):** Nivolumab (anti-PD-1) ve İpilimumab (anti-CTLA-4) kombinasyonu günümüzde birinci basamak standart tedavi haline gelmiştir.""",
        [
            {"type": "clinical", "badge": "🔴 ONKOLOJİK KURAL", "text": "RCC klasik kemoterapiye tamamen dirençlidir; metastatik hastalıkta VHL yolağını hedefleyen TKI'lar (Sunitinib) ve İmmün checkpoint inhibitörleri (anti-PD-1) kullanılır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "4 cm'den küçük böbrek tümörlerinde nefron fonksiyonunu korumak için ilk tercih cerrahi yöntem parsiyel nefrektomidir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-020",
            "question": "Metastatik berrak hücreli renal hücreli karsinom tedavisinde tümörün VHL inaktivasyonuna bağlı aşırı anjiyogenezini hedef alan tirozin kinaz inhibitörü ajan hangisidir?",
            "options": [
                "A) Sisplatin",
                "B) Doksorubisin",
                "C) Sunitinib",
                "D) Metotreksat",
                "E) Vinkristin"
            ],
            "correctAnswer": 2,
            "explanation": "Sunitinib VEGF reseptör tirozin kinazını bloke ederek tümörün aşırı vaskülarizasyonunu baskılayan hedefe yönelik standart ajandır."
        }
    ),
    make_slide(
        21,
        "Pediyatrik vs Erişkin Böbrek Tümörleri: Karşılaştırmalı Ayrım",
        "Wilms Tümörü vs Nöroblastom ve RCC Ayrımının Klinik Kriterleri",
        """Çocuklarda karında kitle ile başvuran olgularda Wilms tümörü ile Nöroblastom ayrımı en kritik pediatrik cerrahi ve patoloji sorusudur.

**1. Wilms Tümörü vs Nöroblastom Karşılaştırması:**
• **Köken:** Wilms böbrek parankiminden köken alır; Nöroblastom ise adrenal medulla veya sempatik zincir nöral krest hücrelerinden köken alır.
• **Orta Hattı Geçme:** Wilms tümörü böbrekte düzgün sınırlı küre şeklindedir ve **orta hattı nadiren geçer**; Nöroblastom ise diffüz infiltredir ve **orta hattı sıklıkla geçer**.
• **Kalsifikasyon:** Wilms'te kalsifikasyon nadirdir; Nöroblastomda yaygın kaba kalsifikasyonlar kuraldır.
• **İdrar Katekolaminleri:** Wilms'te normaldir; Nöroblastomda idrar VMA (vanilmandelik asit) ve HVA aşırı yüksektir.

**2. Erişkin vs Pediyatrik:**
Erişkinde Wilms son derece nadirdir (<%1); çocukta ise RCC %2-3'ü geçmez (çocukta RCC genellikle Xp11 translokasyon karsinomudur).""",
        [
            {"type": "warning", "badge": "🔴 PEDİATRİK AYRIM", "text": "Orta hattı geçmeyen düzgün sınırlı böbrek kitlesi = Wilms Tümörü; Orta hattı geçen, kalsifiye, VMA yüksek kitle = Nöroblastom.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Wilms tümörü böbrek içinde sınırlı kalarak kalsifikasyon içermezken; adrenal nöroblastom kalsifiye olup orta hattı geçer ve idrarda VMA yükseltir.", "color": "sky"}
        ],
        {
            "id": "prac-tum-021",
            "question": "2 yaşındaki bir çocuğun karnında saptanan kitlenin adrenal kaynaklı Nöroblastom değil, böbrek parankim kaynaklı Wilms Tümörü olduğunu en çok destekleyen bulgu hangisidir?",
            "options": [
                "A) İdrarda VMA (vanilmandelik asit) yüksekliği",
                "B) Kitlenin batında orta hattı geçmemesi ve böbrek parankimini genişletmesi",
                "C) BT'de kitle içinde yoğun kaba kalsifikasyonlar izlenmesi",
                "D) Kemik iliğinde rozet oluşturan hücrelerin görülmesi",
                "E) N-MYC onkogen amplifikasyonu"
            ],
            "correctAnswer": 1,
            "explanation": "Wilms tümörü böbrek parankiminde yuvarlak sınırlı büyür ve orta hattı geçmez; nöroblastom ise orta hattı geçer, kalsifiyedir ve katekolamin (VMA) salgılar."
        }
    ),
    make_slide(
        22,
        "Böbrek Tümörleri Büyük Patoloji Karşılaştırma Matrisi",
        "Berrak Hücreli, Papiller, Kromofob RCC, Onkositoma ve AML Tablosu",
        """Böbreğin primer epitelyal ve mezenkimal neoplazmlarının büyük karşılaştırma matrisi:

| Tümör Tipi | Sıklık | Hücre Kökeni | Genetik Bozukluk | Makroskopi | Karakteristik Mikroskopi | Prognoz |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Berrak Hücreli RCC** | %70-80 | Proksimal tübül | **Kromozom 3p kaybı, VHL** | Altın sarısı, nekrotik, renal ven trombüsü | Berrak sitoplazma (lipid/glikojen), narin kapiller ağ | Orta / Kötü |
| **Papiller RCC** | %10-15 | Distal/proksimal tübül | **Trizomi 7, 17, MET** | Kahverengi, kistik, multifokal | Papiller korlar, **köpüksü makrofajlar**, psammom | Berrak hücreliden iyi |
| **Kromofob RCC** | %5 | İnterkale hücreler | Çoklu hipodiploidi | Bej-kahverengi, solid | **Bitki hücresi sınırı**, perinükleer halo, kolloidal demir+ | **Çok iyi** (%95) |
| **Onkositoma** | %5-10 | İnterkale hücreler | 1 ve Y kromozom kaybı | **Maun kahverengisi**, **santral yıldızsı skar** | Mitokondri dolu granüler onkositik eozinofilik hücreler | **Benign** (%100) |
| **Anjiyomiyolipom** | %1-2 | Perivasküler epiteloid | *TSC1* / *TSC2* mutasyonu | Sarı-gri düzensiz | Kalın damar + Düz kas + Yağ, **HMB-45+** | Benign (kanama riski) |""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Altın sarısı = ccRCC; Maun kahverengi + yıldız skar = Onkositoma; Bitki hücresi + halo = Kromofob; Köpüksü makrofaj + psammom = Papiller.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV TABLOSU", "text": "Bu tablo böbrek tümörleri patolojisi dersinin komite ve TUS sınavlarındaki eksiksiz soru şablonudur.", "color": "sky"}
        ],
        {
            "id": "prac-tum-022",
            "question": "Aşağıdaki böbrek tümörü ve hücresel köken eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) Berrak hücreli RCC — Proksimal tübül epiteli",
                "B) Renal onkositoma — Toplayıcı kanal interkale hücreleri",
                "C) Kromofob RCC — Toplayıcı kanal interkale hücreleri",
                "D) Wilms tümörü — Metanefrik blastem kalıntıları",
                "E) Anjiyomiyolipom — Podosit slit diyaframı"
            ],
            "correctAnswer": 4,
            "explanation": "Anjiyomiyolipom podositlerden değil, perivasküler epiteloid mezenkimal hücrelerden (PEComa) kaynaklanır."
        }
    ),
    make_slide(
        23,
        "Böbrek Kitlelerine Klinik ve Radyolojik Tanı Algoritması",
        "İnsidental Kitle, Kontrastlı BT/MRG, Biyopsi Endikasyonu ve Cerrahi Karar",
        """Klinik pratikte böbrekte solid veya kistik kitle saptanan hastada adım adım izlenecek protokol:

**1. Görüntüleme Protokolü:**
• İlk Basamak: Ultrasonografi (kistik mi solid mi ayrımı).
• İkinci Basamak (Kesin Karar): **Dört Fazlı Kontrastlı Batın BT veya Dinamik Renal MRG**.
  - Kontrast Tutulumu: Lezyonda kontrast sonrası >15-20 Hounsfield Ünitesi (HU) dansite artışı olması vaskülarize solid neoplazmı (RCC) kanıtlar.

**2. Böbrek Kitlelerinde Biyopsi Yapılmalı mıdır?**
• Klasik olarak cerrahiye uygun rezektabl renal kitlelerde tümör ekimi riski ve sonucun cerrahi kararı değiştirmemesi nedeniyle **rutin biyopsi YAPILMAZ!** Doğrudan nefrektomi yapılır.
• **Renal Kitle Biyopsisinin Sınırlı Endikasyonları:**
  - Ameliyat edilemeyecek metastatik hastalarda sistemik tedavi öncesi histolojik alt tip belirleme,
  - Termal ablasyon (kriyoterapi, RF ablasyon) planlanan küçük tümörler,
  - Renal lenfoma, metastaz veya abse şüphesi olan durumlar.""",
        [
            {"type": "clinical", "badge": "🔴 CERRAHİ KURAL", "text": "Böbrekte kontrast tutan rezektabl solid kitle saptandığında biyopsi yapılmaz; doğrudan parsiyel veya radikal nefrektomi planlanır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ BİLGİ", "text": "RCC şüphesinde kontrastlı dinamik BT'de >20 HU dansite artışı neoplazik vaskülarizasyonun altın standart kanıtıdır.", "color": "sky"}
        ],
        {
            "id": "prac-tum-023",
            "question": "58 yaşındaki bir hastada rastlantısal olarak saptanan 5 cm'lik solid kortikal böbrek kitlesinde kontrastlı BT'de belirgin kontrast tutulumu izleniyor. Metastaz saptanmayan bu hastada standart klinik yaklaşım ne olmalıdır?",
            "options": [
                "A) Cerrahi öncesi kesin tanı için böbrek iğne biyopsisi yapmak",
                "B) Biyopsi yapmadan doğrudan cerrahi rezeksiyon (nefrektomi) planlamak",
                "C) 6 ay sonra ultrasonla takip etmek",
                "D) Sistemik kemoterapi başlamak",
                "E) Yüksek doz radyoterapi uygulamak"
            ],
            "correctAnswer": 1,
            "explanation": "Rezektabl solid renal kitlelerde tümör ekimi riski ve cerrahi endikasyonun net olması nedeniyle ameliyat öncesi iğne biyopsisi yapılmaz, doğrudan nefrektomiye gidilir."
        }
    ),
    make_slide(
        24,
        "Ders 26 Kapsamlı Sentezi: Böbrek Tümörleri Patolojisinin Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Prof. Dr. Hikmet Keleş'in Böbrek Tümörleri dersinin en kritik sınav ve klinik özeti:

**1. Böbrek Tümörleri Patolojisinin 10 Altın Kuralı:**
1. *RCC Risk Faktörü:* En güçlü edinsel faktör Sigaradır; diyaliz hastalarında gelişen edinsel kistik hastalık riski 30 kat artırır.
2. *Onkositoma:* Maun kahverengisi kitle, merkezinde yıldızsı fibröz skar; mitokondri dolu eozinofilik hücreler; tamamen benigndir.
3. *Anjiyomiyolipom (AML):* Damar + Düz kas + Yağ; Tüberöz skleroz birlikteliği; HMB-45 pozitif; 4 cm üzeri Wunderlich hematom riski.
4. *Berrak Hücreli RCC:* %70-80 en sık tip; Kromozom 3p delesyonu ve VHL inaktivasyonu; HIF-1-alfa birikimi ve masif VEGF salınımı; altın sarısı renk, berrak sitoplazma (lipid/glikojen); renal ven ve VCI'ya tümör trombüsü.
5. *Papiller RCC:* Trizomi 7 ve 17, MET mutasyonu; multifokal ve bilateral; papiller korlarda köpüksü makrofajlar ve psammom cisimcikleri; CK7 ve AMACR pozitif.
6. *Kromofob RCC:* İnterkale hücreler, çoklu hipodiploidi; bitki hücresi sınırları, perinükleer halo, kuru üzüm nükleus, kolloidal demir pozitif; prognozu en iyi RCC.
7. *Wilms Tümörü:* 2-5 yaş çocuk; trifazik histoloji (blastem, epitel, stroma); WT1 (11p13 - WAGR, Denys-Drash), WT2 (11p15 - Beckwith-Wiedemann); anaplazide TP53.
8. *RCC Triadı ve Paraneoplazi:* Triad (hematüri + ağrı + kitle) sadece %10'da tamdır; en sık semptom hematüridir; paraneoplastik: PTHrP (hiperkalsemi), EPO (polisitemi), Stauffer sendromu (hepatik disfonksiyon).
9. *WHO/ISUP Derecelendirme:* Nükleol belirginliğine dayanır; sarkomatoid diferansiasyon doğrudan Derece 4'tür.
10. *TNM Evrelemesi:* T1 ≤7 cm (T1a ≤4 cm parsiyel nefrektomi); T2 >7 cm; T3 renal ven/yağ invazyonu; T4 Gerota fasyasını aşma.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Böbrek kanserinde erken evrede parsiyel nefrektomi küratiftir; metastatik hastalıkta VHL yolağını hedefleyen TKI ve immünoterapi esastır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slayttaki 10 altın kural komite ve TUS sınavlarında böbrek tümörleri konusundaki tüm soruları eksiksiz çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-tum-024",
            "question": "Aşağıdaki böbrek tümörü ve genetik mekanizma eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) Berrak hücreli RCC — Kromozom 3p delesyonu ve VHL inaktivasyonu",
                "B) Papiller RCC — Trizomi 7, trizomi 17 ve MET protoonkogen aktivasyonu",
                "C) Wilms tümörü — Kromozom 11p13 (WT1) ve 11p15 (WT2)",
                "D) Anjiyomiyolipom — TSC1 ve TSC2 mutasyonları",
                "E) Kromofob RCC — Kromozom 3p delesyonu ve VHL aşırı ifadesi"
            ],
            "correctAnswer": 4,
            "explanation": "Kromozom 3p delesyonu ve VHL inaktivasyonu Berrak Hücreli RCC'ye özgüdür. Kromofob RCC'de VHL mutasyonu bulunmaz; yaygın kromozom kayıpları (hipodiploidi) görülür."
        }
    )
]

print("Böbrek Tümörleri 24 slayt başarıyla tanımlandı.")

target_id = 'learn-bobrek-tumorleri'
for d in decks:
    if d.get('id') == target_id:
        d['title'] = "Böbrek Tümörleri Patolojisi"
        d['shortTitle'] = "Böbrek Tümörleri Patolojisi"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Renal Hücreli Karsinom alt tipleri (Berrak hücreli 3p/VHL, Papiller MET/Trizomi 7-17, Kromofob kolloidal demir), Onkositoma (maun kahverengi, yıldız skar), Anjiyomiyolipom (Tüberöz skleroz, HMB-45), Wilms Tümörü (Trifazik histoloji, WAGR, Beckwith-Wiedemann), Paraneoplastik sendromlar ve WHO/ISUP evreleme sistemi."
        d['slides'] = bobrek_tumor_slides
        print(f"'{target_id}' güvertesi 24 yüksek kaliteli slaytla güncellendi.")
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("Böbrek Tümörleri güncellemesi tamamlandı.")
