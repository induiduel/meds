# -*- coding: utf-8 -*-
"""
Rebuild Tubulointerstitial Diseases Deck with High-Quality Medical Standards
learn-tubulointerstisyel-hastaliklar (24 Slayt)
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

tubulo_slides = [
    make_slide(
        1,
        "Tübülointerstisyel Böbrek Hastalıkları: Genel Çerçeve ve Sınıflama",
        "Glomerüllerin Korunduğu, Primer Tübül ve İnterstisyum Patolojileri",
        """Tübülointerstisyel nefritler (TİN), primer patolojik hasarın böbrek tübülleri ve interstisyel bağ dokusu üzerinde yoğunlaştığı, glomerüllerin ve renal damarların ise en azından başlangıç döneminde korunduğu heterojen bir hastalıklar grubudur.

**1. Temel Klinik ve Fizyopatolojik Özellikler:**
• Glomerül filtrasyon bariyeri sağlam olduğu için nefrotik düzeyde masif proteinüri, belirgin dismorfik hematüri ve eritrosit silindirleri izlenmez.
• Buna karşılık tübüler fonksiyon bozukluğu kardinal bulgudur: Konsantrasyon kusuru (poliüri, noktüri), renal tübüler asidoz (idrar asidifikasyon bozukluğu), tuz kaybı (tuz kaybettiren nefropati) ve tübüler proteinüri (beta-2 mikroglobulin atılımı).

**2. Etyolojik Sınıflama:**
• **Enfeksiyöz Nedenler:** Akut ve kronik piyelonefrit (bakteriyel), fungal ve viral enfeksiyonlar.
• **İlaç ve Toksin Hasarı:** Akut interstisyel nefrit (hipersensitivite), analjezik nefropatisi, ağır metal toksisitesi (kurşun, kadmiyum).
• **Metabolik Bozukluklar:** Ürat nefropatisi (gut, tümör lizis), nefrokalsinozis, hipokalemik nefropati, okzalozis.
• **İmmünolojik / Sistemik:** Hafif zincir (miyelom) böbreği, Sjögren sendromu, sarkoidoz, IgG4 ilişkili tubulointerstisyel nefrit.""",
        [
            {"type": "warning", "badge": "🔴 PATOFİZYOLOJİK AYRIM", "text": "Tübülointerstisyel hastalıklarda idrarda masif proteinüri veya eritrosit silindiri görülmez; en erken klinik bulgu tübül hasarına bağlı konsantrasyon yetersizliği (izostenüri, noktüri) ve poliüridir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Glomerülopatilerin aksine tübülointerstisyel hastalıklarda idrarla atılan protein albümin değil, proksimal tübülde geri emilemeyen düşük molekül ağırlıklı beta-2 mikroglobulindir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-001",
            "question": "Aşağıdaki klinik ve laboratuvar bulgularından hangisi bir primer glomerülonefritten ziyade tübülointerstisyel nefriti destekler?",
            "options": [
                "A) 24 saatlik idrarda 5 gram selektif albüminüri",
                "B) İdrar sedimentinde dismorfik eritrositler ve eritrosit silindirleri",
                "C) İdrar konsantrasyon yeteneğinde bozulmaya bağlı erken poliüri ve noktüri",
                "D) Yüzde ve göz kapaklarında yaygın anazarka tipi ödem",
                "E) Serumda kompleman C3 ve C4 düzeylerinin aşırı düşmesi"
            ],
            "correctAnswer": 2,
            "explanation": "Tübül epitelinin medüller konsantrasyon mekanizması hasar gördüğünde en erken bulgu idrarı konsantre edememe (izostenüri), poliüri ve noktüridir. Masif albüminüri ve eritrosit silindirleri glomerül hasarına aittir."
        }
    ),
    make_slide(
        2,
        "Akut Tübüler Hasar / Nekroz (ATH / ATN): İskemik vs Nefrotoksik Tipler",
        "Akut Böbrek Hasarının 1 Numaralı İntrensek Nedeni ve Çamur Rengi Silindirler",
        """Akut Tübüler Hasar (ATH), klinik olarak ani gelişen oligürik veya non-oligürik akut böbrek hasarının (ABH) en sık intrensek nedenidir. Tübül epitel hücrelerinin hasarlanması ve dökülmesiyle seyreder.

**1. Etyolojik Mekanizmalar:**
• **İskemik ATH:** Ağır hipovolemi, septik şok, kardiyojenik şok, masif kanama veya yanıklar sonucu renal perfüzyonun kritik düzeyin altına inmesiyle gelişir.
• **Nefrotoksik ATH:**
  - *Ekzojen Toksinler:* Aminoglikozidler (Gentamisin), iyotlu radyokontrast maddeler, Sisplatin, Amfoterisin B.
  - *Endojen Toksinler:* Rabdomiyolizde kas yıkımıyla açığa çıkan **Miyoglobin**, intravasküler hemolizde **Hemoglobin**, multipl miyelomda monoklonal hafif zincirler.

**2. Morfolojik Özellikler:**
• **İskemik Tip:** Tübül hasarı **yama tarzında (fokal)** ve kesintilidir. En duyarlı segmentler oksijen tüketimi en yüksek olan **proksimal tubulusun düz parçası (S3 segmenti)** ve **medüller Henle çıkan kalın koludur**. Tübüler bazal membran yırtılır (**tübüloreksis**).
• **Nefrotoksik Tip:** Tübül hasarı **diffüz ve süreklidir**. Özellikle proksimal konvolüt tubulus epitelinde yaygın nekroz izlenir ancak bazal membran genellikle intaktır.
• Dökülen nekrotik epitel hücreleri ve Tamm-Horsfall proteini tübül lümenini tıkayarak idrar sedimentinde patognomonik **'çamur rengi granüler silindirler' (muddy brown granular casts)** oluşturur.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "İdrar sedimentinde 'çamur rengi granüler silindirler' (muddy brown casts) ve tubuler epitel hücreleri görülmesi Akut Tübüler Hasar / Nekroz için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "İskemik ATH'de tübüler bazal membran yırtılır (tübüloreksis) ve hasar yamalıdır; toksik ATH'de ise bazal membran korunur ve proksimal tübül diffüz etkilenir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-002",
            "question": "Septik şok tablosunda yoğun bakımda izlenen hastada ani gelişen oligüri sonrası yapılan idrar mikroskopisinde 'çamur rengi granüler silindirler' (muddy brown casts) saptanıyor. En olası tanı hangisidir?",
            "options": [
                "A) Akut poststreptokokkal glomerülonefrit",
                "B) İskemik akut tübüler hasar / nekroz",
                "C) Minimal değişiklik hastalığı",
                "D) Üriner sistem taş obstrüksiyonu",
                "E) Renal ven trombozu"
            ],
            "correctAnswer": 1,
            "explanation": "Şok ve ağır hipotansiyon zemininde çamur rengi granüler silindirlerin izlenmesi iskemik Akut Tübüler Hasarın (ATH/ATN) klasik göstergesidir."
        }
    ),
    make_slide(
        3,
        "Akut Piyelonefrit: Etyoloji ve Enfeksiyon Yolları",
        "Enterik Gram-Negatif Basiller, Asendan Yayılım ve Vezikoüreteral Reflü (VUR)",
        """Akut piyelonefrit, böbrek parankiminin ve renal pelvisin akut süpüratif bakteriyel enfeksiyonudur. Kadınlarda kısa üretra, hormonal değişiklikler ve gebelik nedeniyle çok daha sıktır.

**1. Etyolojik Etkenler:**
• Olguların **%85'inden fazlasından enterik Gram-negatif basiller** sorumludur:
  - **Escherichia coli (UPEC):** 1 numaralı etken. P-fimbriya (pap pili) adezinleri sayesinde ürotelyuma ve tübül epiteline sıkıca tutunur.
  - Diğer enterik bakteriler: *Proteus mirabilis* (ürez enzimi ile taş oluşturur), *Klebsiella pneumoniae*, *Enterobacter*.
  - Kateterli ve nozokomiyal olgularda: *Pseudomonas aeruginosa*, *Enterococcus faecalis*, *Staphylococcus aureus* (hematojen yayılımda 1 numara).

**2. Enfeksiyon Yolları:**
• **Asendan Enfeksiyon Yolu (%95+):** En sık yoldur. Fekal floradan gelen bakteriler perineyi kolonize eder -> Üretraya girer -> Mesaneye ulaşır (sistit) -> Üreterler boyunca böbreğe tırmanır.
• Normalde idrar akımı ve vezikoüreteral bileşkedeki valv mekanizması reflüyü engeller. Ancak **Vezikoüreteral Reflü (VUR)** veya obstrüksiyon varlığında mikroorganizmalar renal pelvise ve toplayıcı kanallara ulaşır.
• **Hematojen Yol (%5):** Septisemi ve infektif endokardit sırasında (özellikle S. aureus ve mantarlar) kan yoluyla böbreğe yayılır.""",
        [
            {"type": "warning", "badge": "🔴 PATOGENEZ KRİTİĞİ", "text": "Asendan piyelonefrit gelişiminde en kritik anatomik/fonksiyonel defekt üreteral valv mekanizmasının yetersizliği sonucu oluşan Vezikoüreteral Reflüdür (VUR).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Akut piyelonefritin en sık etkeni E. coli'dir (%85); E. coli'nin ürotelyuma tutunmasını sağlayan en önemli virülans faktörü P-fimbriyadır (P-pili).", "color": "sky"}
        ],
        {
            "id": "prac-tub-003",
            "question": "Toplum kökenli akut piyelonefrit olgularının %85'inden sorumlu olan ve böbrek toplayıcı kanallarına P-fimbriyalarıyla tutunan en sık mikroorganizma hangisidir?",
            "options": [
                "A) Proteus mirabilis",
                "B) Klebsiella pneumoniae",
                "C) Uropatojenik Escherichia coli (UPEC)",
                "D) Pseudomonas aeruginosa",
                "E) Staphylococcus saprophyticus"
            ],
            "correctAnswer": 2,
            "explanation": "Üropatojenik E. coli (UPEC) akut piyelonefritin açık ara en sık etkenidir ve P-fimbriyaları ile renal epitelyal reseptörlere bağlanır."
        }
    ),
    make_slide(
        4,
        "Akut Piyelonefrit Morfolojisi: Süpüratif İnflamasyon ve Mikroabseler",
        "Kortekste Sarımtırak Abseler, Tübül İçi Nötrofiller ve Lökosit Silindirleri",
        """Akut piyelonefrit, böbrekte karakteristik bir akut süpüratif eksüdatif tablo oluşturur.

**1. Makroskobik Görünüm:**
• Böbrek büyümüş, ödemli ve konjestedir.
• Böbrek subkapsüler korteks yüzeyinde ve kesit yüzeyinde etrafı hiperemik kırmızı bir zonla çevrili **küçük, sarımtırak ayrık süpüratif abseler (mikroabseler)** izlenir.
• Renal pelvis ve kalikslerin mukozası hiperemik, ödemli ve üzeri pürülan eksüda ile kaplıdır.

**2. Mikroskobik Bulgular:**
• **İnterstisyel Nötrofilik İnfiltrasyon:** İnterstisyumda masif polimorfonükleer lökosit (nötrofil) birikimi ve ödem izlenir.
• **Tübüler Hasar ve Lökosit Tıkaçları:** Nötrofiller tübül lümenlerine dökülür; tübül epitelinde nekroz gelişir.
• **İdrar Sedimenti:** İdrarda bol lökosit (piyüri), bakteri ve tübül lümeninde kalıplaşan **Lökosit Silindirleri (WBC casts)** izlenir. Lökosit silindiri enfeksiyonun alt üriner sistemde (sistit) sınırlı kalmayıp böbrek parankimini (piyelonefrit) tuttuğunun **patognomonik kanıtıdır**.
• Glomerüller bu evrede genellikle korunmuştur; nekroz ancak ileri apseli formlarda glomerüle yayılır.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "İdrar sedimentinde 'Lökosit Silindirleri' (WBC casts) görülmesi enfeksiyonun sistit değil, kesinlikle Akut Piyelonefrit olduğunu kanıtlar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Akut piyelonefritin mikroskopisinde tübül epitelinde nekroz, lümende nötrofil tıkaçları ve kortekste sarı mikroabseler görülür; glomerüller ise başlangıçta korunur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-004",
            "question": "Ateş, titreme, dizüri ve sağ yan ağrısı olan 30 yaşındaki bir kadında yapılan idrar mikroskopisinde sistiti ekarte ettirip kesin Akut Piyelonefrit tanısı koyduran bulgu hangisidir?",
            "options": [
                "A) Bol lökosit ve bakteri saptanması",
                "B) Pozitif lökosit esteraz testi",
                "C) İdrar sedimentinde lökosit silindirleri (WBC casts) görülmesi",
                "D) İdrar kültüründe 10^5 koloni E. coli üremesi",
                "E) Mikroskopik hematüri varlığı"
            ],
            "correctAnswer": 2,
            "explanation": "Lökosit silindirleri nötrofillerin böbrek tübüllerinde Tamm-Horsfall proteini ile silindir kalıbı oluşturmasıyla meydana gelir ve enfeksiyonun böbrek parankiminde olduğunu (piyelonefrit) kanıtlar."
        }
    ),
    make_slide(
        5,
        "Akut Piyelonefritin Ağır Komplikasyonları",
        "Papiller Nekroz, Piyonefroz ve Perinefrik Abse",
        """Akut piyelonefrit uygun tedavi edilmediğinde veya diyabet ve obstrüksiyon gibi kolaylaştırıcı zeminlerde hayatı tehdit eden üç büyük komplikasyona yol açar.

**1. Renal Papiller Nekroz (Nekrotizan Papillit):**
• Renal piramitlerin uç kısımlarının (papillaların) iskemik ve süpüratif koagülasyon nekrozuna uğrayarak kopmasıdır.
• Özellikle şu 4 durumda gelişir (**KODLAMA: POST / DOPA**):
  1. *Diabetes Mellitus* (en sık zemin),
  2. *Analjezik Nefropatisi* (fenasetin/NSAİİ),
  3. *Orak Hücreli Anemi / Taşıyıcılığı*,
  4. *Üriner Sistem Obstrüksiyonu*.
• Nekroze papilla kopup üreteri tıkayarak akut renal koliğe ve anüriye yol açabilir.

**2. Piyonefroz:**
Toplayıcı sistemde tam veya tama yakın bir obstrüksiyon (örneğin staghorn taş veya üreter tümörü) varlığında renal pelvis, kaliksler ve üreterin püs (iltihap) ile dolarak dev bir abse kesesine dönüşmesidir.

**3. Perinefrik Abse:**
Bakteriyel süpürasyonun böbrek fibröz kapsülünü delerek perirenal yağ dokusuna ve Gerota fasyasına yayılmasıdır; cerrahi drenaj gerektirir.""",
        [
            {"type": "warning", "badge": "🔴 HAYATİ KOMPLİKASYON", "text": "Papiller nekrozun en sık görüldüğü klinik zemin Diabetes Mellitus'tur; nekroze olan papilla üreteri tıkayarak akut anüriye ve ürosepsise neden olabilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS BİLGİSİ", "text": "Papiller nekroz nedenleri: Diyabet, Analjezik nefropatisi, Orak hücreli anemi ve Obstrüksiyondur. Kesit yüzeyinde papilla uçları gri-beyaz nekrotiktir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-005",
            "question": "Aşağıdaki klinik durumlardan hangisi akut piyelonefrit seyrinde Renal Papiller Nekroz gelişimi açısından en yüksek risk faktörünü oluşturur?",
            "options": [
                "A) Genç yaşta gebelik",
                "B) Kontrolsüz Diabetes Mellitus",
                "C) Minimal değişiklik hastalığı",
                "D) İzole kalsiyum taşları",
                "E) Basit böbrek kisti"
            ],
            "correctAnswer": 1,
            "explanation": "Renal papiller nekrozun açık ara en sık görüldüğü klinik durum Diabetes Mellitus'tur (diyabetik mikroanjiyopati + enfeksiyon kombinasyonu)."
        }
    ),
    make_slide(
        6,
        "Kronik Piyelonefrit ve Reflü Nefropatisi: Patogenez ve Skar Dağılımı",
        "Böbrek Kutuplarında (Polar) Kaba U-Şekilli Skarlar ve Kaliks Küntleşmesi",
        """Kronik piyelonefrit, renal parankimin tekrarlayan veya devam eden bakteriyel enfeksiyonları, kronik enflamasyon, doku yıkımı ve skarlaşmasıyla karakterize ilerleyici bir tablodur. Son dönem böbrek yetmezliğine gidişin önemli nedenlerindendir.

**1. İki Ana Form:**
• **Kronik Reflü Nefropatisi:** Çocukluk çağında vezikoüreteral reflü (VUR) ve intrarenal reflü zemininde gelişir. En sık görülen kronik piyelonefrit formudur.
• **Kronik Obstrüktif Piyelonefrit:** Taş, posterior üretral valv, prostat hiperplazisi gibi obstrüktif lezyonların üzerine eklenen tekrarlayan enfeksiyonlarla oluşur.

**2. Karakteristik Makroskobik Morfoloji:**
• Böbrekler asimetrik olarak küçülmüştür ve düzensiz yüzeylidir.
• **Kaba, U-Şekilli Kortikal Skarlar:** Skarlar en sık böbreğin **üst ve alt kutuplarında (polar bölgelerde)** yerleşir. Bunun nedeni bileşik kalikslerin (compound calyces) konkav papilla yapısı nedeniyle intrarenal reflüye izin vermesidir (orta zonlardaki papillalar reflüye dirençlidir).
• **Kaliks Deformasyonu (Küntleşme):** Skarın hemen altında yer alan kaliks genişlemiş, küntleşmiş ve deforme olmuştur. Skarın altında kaliks deformasyonu bulunması piyelonefriti vasküler skarlardan (vasküler skar kaliksi deforme etmez) ayıran en kritik kriterdir.""",
        [
            {"type": "warning", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "Kronik piyelonefrit skarı kaliksi deforme edip küntleştirirken; vasküler aterosklerotik infarkt skarı kaliksi deforme etmez.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Kronik piyelonefritte kaba U-şekilli skarlar intrarenal reflüye açık olan böbreğin ÜST VE ALT KUTUPLARINDA (polar) yerleşir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-006",
            "question": "Kronik piyelonefritte kaba kortikal parankimal skarların ve kaliks küntleşmesinin en sık böbreğin üst ve alt kutuplarında (polar) yerleşmesinin temel anatomik nedeni nedir?",
            "options": [
                "A) Polar bölgelerde kan akımının daha fazla olması",
                "B) Üst ve alt kutuplardaki bileşik kaliks papillalarının intrarenal reflüye izin veren morfolojisi",
                "C) Glomerüllerin sadece kutuplarda yer alması",
                "D) Polar bölgelerde kapsülün olmaması",
                "E) Lenfatik drenajın kutuplarda tıkalı olması"
            ],
            "correctAnswer": 1,
            "explanation": "Böbreğin üst ve alt kutuplarındaki bileşik kaliksler düzleşmiş veya konkav papillaya sahiptir; bu anatomik yapı idrarın toplayıcı kanallara geri kaçmasına (intrarenal reflü) izin vererek polar skarlara yol açar."
        }
    ),
    make_slide(
        7,
        "Kronik Piyelonefrit Mikroskopisi: Tübüler 'Tiroidizasyon' ve İnterstisyel Fibrozis",
        "Eozinofilik Kolloid Benzeri Silindirlerle Dolu Atrofik Tübüller",
        """Kronik piyelonefritin mikroskobik histopatolojisi, tübüler hasarın ve kronik yangının kendine has adaptif görünümünü yansıtır.

**1. Mikroskobik Bulgular:**
• **Tübüler Atrofi ve 'Tiroidizasyon' Manzarası:** Bazı tübüller tamamen atrofiye uğrayıp kaybolurken, bazı tübüller ileri derecede dilate olur. Bu dilate tübüllerin lümeni homojen, eozinofilik, PAS pozitif proteinöz silindirlerle (Tamm-Horsfall proteini) dolar. Düşük büyütmede bu alanlar tiroid bezinin kolloid dolu foliküllerine o kadar benzer ki bu görünüme **'Tiroidizasyon' (tiroid benzeri böbrek)** denir.
• **Kronik İnterstisyel Enflamasyon:** İnterstisyumda yaygın lenfosit, plazma hücresi ve histiyosit infiltrasyonu ile yoğun kollajen birikimi (interstisyel fibrozis).
• **Periglomerüler Fibrozis:** Glomerüllerin Bowman kapsülü çevresinde konsantrik laminer kollajen kılıfı (soğan zarı benzeri periglomerüler fibrozis) gelişir. Zamanla glomerüller tamamen hyalinize olur.
• **Vasküler Lezyonlar:** Skar alanlarındaki arterlerde lümeni daraltan obliteratif intimal proliferasyon.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Böbrek kesitinde tiroid bezi foliküllerini andıran kolloid benzeri silindirlerle dolu dilate tübüller (Tiroidizasyon) Kronik Piyelonefritin klasik mikroskobik bulgusudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Tiroidizasyon mikroskobik olarak dilate tübül lümenlerinde Tamm-Horsfall proteini birikmesiyle oluşur ve kronik tübülointerstisyel yıkımı simgeler.", "color": "sky"}
        ],
        {
            "id": "prac-tub-007",
            "question": "Böbrek biyopsisinde tübüllerin yer yer atrofiye uğradığı, bazı alanlarda ise dilate tübüllerin homojen pembe kolloid benzeri materyalle dolarak tiroid dokusuna benzer görünüm ('tiroidizasyon') oluşturduğu saptanan hastada en olası tanı hangisidir?",
            "options": [
                "A) Akut poststreptokokkal GN",
                "B) Kronik piyelonefrit",
                "C) Minimal değişiklik hastalığı",
                "D) Membranöz nefropati",
                "E) Akut interstisyel nefrit"
            ],
            "correctAnswer": 1,
            "explanation": "Böbrek parankiminde tübüllerin dilate olup pembe silindirlerle dolması sonucu oluşan 'tiroidizasyon' manzarası Kronik Piyelonefrit için karakteristiktir."
        }
    ),
    make_slide(
        8,
        "Ksantogranülamatöz Piyelonefrit (XPN): Proteus, Taş ve Kanser Taklitçisi",
        "Staghorn Taş, Köpüksü Makrofajlar (Köpüklü Histiyositler) ve Renal Karsinomla Karışma",
        """Ksantogranülamatöz Piyelonefrit (XPN), böbrek parankiminin yıkılarak yerini lipid yüklü köpüksü makrofajlardan oluşan sarı-turuncu kitlelere bıraktığı, nadir görülen agresif bir kronik bakteriyel piyelonefrit varyantıdır.

**1. Etyoloji ve Patogenez:**
• Neredeyse daima kronik üriner sistem obstrüksiyonu ve rekürren enfeksiyon zemininde gelişir.
• En sık sorumlu patojen **Proteus mirabilis**'tir (ürez enzimi ile üreyi parçalayarak ortamı alkalileştirir ve magnezyum amonyum fosfat / **strüvit / geyik boynuzu (staghorn) taşlarına** yol açar). E. coli de eşlik edebilir.

**2. Makroskobik Görünüm ve Klinik Tuzak:**
• Böbrek ileri derecede büyümüştür. Pelviste genellikle büyük bir staghorn taş bulunur.
• Böbrek parankiminde kaliksler çevresinde yerleşen **büyük, sarı-turuncu, nekrotik nodüler kitleler** izlenir.
• Bu lezyonlar renal parankimi aşarak çevre perinefrik dokuya ve retroperitona infiltre olabilir.
• **En Kritik Klinik Tuzak:** Hem radyolojik olarak (BT/MRG) hem de makroskobik olarak **Renal Hücreli Karsinomu (RCC - Berrak Hücreli Karsinom)** taklit eder; ameliyatta sıklıkla böbrek tümörü sanılarak nefrektomi yapılır!

**3. Mikroskobik Bulgular:**
Bol lipid yüklü **köpüksü makrofajlar (ksantoma hücreleri)**, Touton dev hücreleri, plazma hücreleri, lenfositler ve nekroz odakları izlenir.""",
        [
            {"type": "warning", "badge": "🔴 RADYOLOJİK / CERRAHİ TUZAK", "text": "Ksantogranülamatöz piyelonefrit sarı-turuncu rengi, kitle etkisi ve çevreye invazyonu nedeniyle radyolojik ve cerrahi olarak Berrak Hücreli Karsinomla (RCC) en sık karışan benign lezyondur!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Proteus enfeksiyonu, staghorn taş ve biyopside bol miktarda lipid yüklü 'köpüksü makrofajlar' (ksantoma hücreleri) Ksantogranülamatöz Piyelonefrit tanısını koydurur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-008",
            "question": "Renal pelviste büyük bir staghorn taş bulunan hastada BT'de böbrek parankimini harap eden sarı-turuncu kitle lezyonları saptanıyor. Biyopside bol miktarda lipid yüklü köpüksü histiyositler izleniyor. Renal karsinomu taklit eden bu antite hangisidir?",
            "options": [
                "A) Malakoplaki",
                "B) Ksantogranülamatöz piyelonefrit",
                "C) Renal onkositoma",
                "D) Anjiyomiyolipom",
                "E) Tuberoskleroz böbreği"
            ],
            "correctAnswer": 1,
            "explanation": "Staghorn taş zemininde sarı-turuncu nodüller ve köpüksü makrofaj infiltrasyonu ile giden ve RCC'yi taklit eden antite Ksantogranülamatöz Piyelonefrittir (XPN)."
        }
    ),
    make_slide(
        9,
        "Malakoplaki: Michaelis-Gutmann Cisimcikleri ve Makrofaj Lizozom Kusuru",
        "Kalsifiye Konsantrik Cisimcikler, Von Kossa Boyası ve Kronik E. coli Enfeksiyonu",
        """Malakoplaki, mesanede ve bazen böbrek parankiminde yumuşak, sarımsı mukozal plaklar oluşturan nadir bir kronik granülomatöz enflamatuar hastalıktır.

**1. Patogenez:**
• Kronik **Escherichia coli** veya diğer Gram-negatif enfeksiyonlar zemininde gelişir.
• Temel defekt makrofajların fagositoz fonksiyonundadır: Makrofajlar bakterileri yutar ancak fago-lizozomal enzim aktivitesindeki defekt nedeniyle bakterileri tamamen sindirip lize edemez.
• Parçalanmamış bakteri artıkları makrofaj sitoplazmasında kalsiyum ve demir tuzlarıyla mineralize olur.

**2. Karakteristik Mikroskobik Bulgu:**
• Büyük eozinofilik granüler histiyositler (**von Hansemann hücreleri**).
• **Michaelis-Gutmann Cisimcikleri:** Histiyositlerin içinde veya ekstraselüler alanda yer alan, ortasında kalsifiye bir çekirdek bulunan konsantrik laminasyonlu kireçlenme odaklarıdır.
• **Özel Boyalar:** Michaelis-Gutmann cisimcikleri **kalsiyum için Von Kossa**, **demir için Prusya Mavisi (Perls)** ve PAS boyaları ile kuvvetli pozitif boyanır. Bu cisimciklerin görülmesi malakoplaki için **patognomoniktir**.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Konsantrik laminasyon gösteren kalsifiye 'Michaelis-Gutmann cisimcikleri' Malakoplaki için patognomoniktir; Von Kossa boyası ile pozitif boyanır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Malakoplakinin patogenezindeki temel mekanizma makrofajların yuttukları bakterileri lizozomal defekt nedeniyle sindirememesi ve mineralizasyondur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-009",
            "question": "Kronik üriner enfeksiyonu olan bir hastanın mesane mukozasından alınan biyopside, histiyosit sitoplazmalarında Von Kossa ve demir boyası ile boyanan konsantrik kalsifiye 'Michaelis-Gutmann cisimcikleri' saptanıyor. Tanı nedir?",
            "options": [
                "A) Ksantogranülamatöz sistit",
                "B) Malakoplaki",
                "C) Şistozomiyazis",
                "D) Ürotelyal karsinom in situ",
                "E) Folliküler sistit"
            ],
            "correctAnswer": 1,
            "explanation": "Von Kossa pozitif Michaelis-Gutmann cisimcikleri makrofajların sindiremediği bakteri artıklarının mineralizasyonuyla oluşur ve Malakoplakinin patognomonik lezyonudur."
        }
    ),
    make_slide(
        10,
        "Akut İlaç İlişkili İnterstisyel Nefrit (AİN): İmmünopatogenez",
        "Tip I (IgE) ve Tip IV Hipersensitivite, Dozdan Bağımsız İmmün Reaksiyon",
        """Akut İlaç İlişkili İnterstisyel Nefrit (AİN), çeşitli ilaçların kullanımına ikincil olarak gelişen, glomerülleri koruyup interstisyumda ödem ve lökosit infiltrasyonu ile giden akut böbrek hasarı tablosudur. İntrensek akut böbrek yetmezliğinin %15'inden sorumludur.

**1. İmmünopatogenetik Mekanizma:**
• Bu tablo ilacın doğrudan toksik etkisine bağlı DEĞİLDİR; **immünolojik bir hipersensitivite reaksiyonudur**.
• Bu nedenle **dozdan bağımsızdır**; ilacın çok küçük dozlarında bile tetiklenebilir ve ilaca ikinci maruziyette çok daha hızlı ve şiddetli alevlenir.
• İlaç tübüler bazal membrana bağlanarak bir 'hapten' gibi davranır veya tübül hücre antijenlerini değiştirir.
• Hem **Tip I Hipersensitivite** (IgE aracılı mast hücre degranülasyonu) hem de **Tip IV Gecikmiş Hipersensitivite** (CD4+ ve CD8+ T lenfositlerin sitotoksik aktivasyonu) birlikte rol oynar.

**2. En Sık Sorumlu İlaç Grupları:**
• **Antibiyotikler (%50+):** Sentetik penisilinler (Metisilin, Ampisilin, Amoksisilin), Sefalosporinler, Sülfonamidler, Kinolonlar (Siprofloksasin), Rifampin.
• **Non-Steroid Antiinflamatuar İlaçlar (NSAİİ):** İbuprofen, Naproksen, İndometasin.
• **Proton Pompa İnhibitörleri (PPİ):** Omeprazol, Pantoprazol, Lansoprazol (günümüzde en sık gözden kaçan nedenlerden biridir).
• **Diüretikler:** Tiyazidler, Furosemid.""",
        [
            {"type": "clinical", "badge": "🔴 KRİTİK İMMÜNOLOJİ", "text": "Akut interstisyel nefrit ilacın toksisitesiyle değil immünolojik aşırı duyarlılıkla oluşur; bu nedenle dozdan bağımsızdır ve ilacın kesilmesiyle geri döner.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "AİN gelişiminde Tip I (IgE) ve Tip IV (hücresel) hipersensitivite mekanizmaları rol oynar; en sık sorumlu ajanlar penisilinler, NSAİİ ve PPI'lardır.", "color": "sky"}
        ],
        {
            "id": "prac-tub-010",
            "question": "Pnömoni tedavisi için ampisilin başlanan hastada 10 gün sonra kreatinin yükselmesi saptanıyor. Bu durumun ilacın doza bağlı nefrotoksisitesi değil, immün hipersensitivite aracılı Akut İnterstisyel Nefrit olduğunu kanıtlayan özellik hangisidir?",
            "options": [
                "A) Hasarın sadece ilacın çok yüksek kan seviyelerinde ortaya çıkması",
                "B) İlacın dozuyla ilişkisiz olması ve küçük bir dozda bile reaksiyonun tetiklenebilmesi",
                "C) Böbrek boyutlarının küçülmüş olması",
                "D) Glomerüllerde tel halka lezyonlarının bulunması",
                "E) İdrarda masif 10 gram albüminüri saptanması"
            ],
            "correctAnswer": 1,
            "explanation": "Akut interstisyel nefrit immünolojik bir hipersensitivite (alerji) reaksiyonu olduğundan dozdan bağımsızdır; ilacın minimal dozu dahi reaksiyonu başlatabilir."
        }
    ),
    make_slide(
        11,
        "Akut İnterstisyel Nefrit: Klinik Triad ve Hansel Boyası",
        "Ateş, Makülopapüler Döküntü, Periferik Eozinofili ve Eozinofilüri",
        """Akut interstisyel nefrit genellikle ilaç maruziyetinden **2 ila 40 gün (ortalama 10-15 gün)** sonra başlar.

**1. Klasik Klinik Triad:**
Klinik olarak hastaların %30-40'ında klasik alerjik triad mevcuttur:
1. **Ateş (%70-80):** Açıklanamayan subfebril veya yüksek ateş.
2. **Döküntü (%30-50):** Gövdede ve ekstremitelerde kaşıntılı, eritematöz makülopapüler cilt döküntüsü.
3. **Eozinofili (%70-80):** Periferik kanda belirgin eozinofil artışı.
• Bu triada genellikle hafif yan ağrısı ve oligürik/non-oligürik böbrek yetmezliği (kreatinin artışı) eşlik eder.

**2. İdrar Tetkiki ve Eozinofilüri:**
• İdrarda hafif-orta proteinüri (genellikle <1-2 g/gün), mikroskopik hematüri ve lökositüri mevcuttur.
• **Eozinofilüri:** İdrar sedimentinde eozinofil lökositlerin gösterilmesidir. Standart Wright-Giemsa boyası yerine **Hansel boyası** ile idrar sedimenti boyandığında eozinofillerin parlak kırmızı granülleri net olarak gösterilir. İdrardaki lökositlerin >%1'inin eozinofil olması AİN tanısını güçlü biçimde destekler.""",
        [
            {"type": "clinical", "badge": "🔴 TANI BULGUSU", "text": "Antibiyotik veya PPİ başlanan hastada ateş + döküntü + eozinofili triadı ve idrarda Hansel boyasıyla eozinofil görülmesi AİN tanısını koydurur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "İdrar sedimentinde eozinofilleri en duyarlı gösteren özel boya Hansel boyasıdır; AİN için oldukça değerlidir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-011",
            "question": "Yeni bir antibiyotik tedavisi başlandıktan 12 gün sonra ateşi çıkan, vücudunda makülopapüler döküntü beliren ve kreatinini yükselen hastada Akut İnterstisyel Nefrit tanısını desteklemek için idrarda eozinofilleri gösteren boya hangisidir?",
            "options": [
                "A) Ziehl-Neelsen boyası",
                "B) Hansel boyası",
                "C) Kongo kırmızısı",
                "D) Prusya mavisi",
                "E) Von Kossa boyası"
            ],
            "correctAnswer": 1,
            "explanation": "İdrar sedimentindeki eozinofil lökositleri göstermek için en hassas boyama yöntemi Hansel boyasıdır (Wright boyasına göre çok daha üstündür)."
        }
    ),
    make_slide(
        12,
        "AİN Morfolojisi: İnterstisyel Eozinofiller, Tubulit ve Non-Nekrotizan Granülomlar",
        "İnterstisyel Ödem, Mononükleer İnfiltrat ve Tübül Epiteline Lökosit Göçü",
        """AİN'de böbrek biyopsisi tanıyı kesinleştiren altın standart incelemedir.

**1. Işık Mikroskopisi (LM):**
• **İnterstisyel Ödem ve Enflamasyon:** İnterstisyum belirgin şekilde genişlemiş ve ödemlidir. İnterstisyel alanda yoğun hücresel infiltrasyon izlenir.
• **İnfiltratın İçeriği:** İnfiltratın ana gövdesini lenfositler (özellikle CD4+ ve CD8+ T hücreleri) ve makrofajlar oluşturur. Ancak tanı koydurucu en kritik hücreler **eozinofil lökositler** ve plazma hücreleridir.
• **Tubulit (Tubulitis):** Lenfosit ve eozinofillerin tübüler bazal membranı geçerek tübül epitel hücrelerinin arasına sızması ve epiteli hasarlamasıdır.
• **Granülomatöz Reaksiyon:** Özellikle metisilin ve NSAİİ ilişkili olgularda nekrotizan olmayan epiteloid histiyositik granülomlar ve dev hücreler izlenebilir.

**2. İmmünofloresan (İF):**
Genellikle tamamen negatiftir (immün kompleks depoziti bulunmaz). Ancak metisilin kullanımına bağlı bazı olgularda tübüler bazal membran boyunca lineer IgG veya C3 birikimi izlenebilir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK AYRIM", "text": "Akut piyelonefritte infiltrat NÖTROFİL ağırlıklı iken; Akut İnterstisyel Nefritte infiltrat LENFOSİT ve EOZİNOFİL ağırlıklıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "AİN biyopsisinde interstisyumda ödem, yoğun lenfosit ve eozinofil infiltrasyonu ile tübül epiteli arasına lökosit sızması (tubulit) izlenir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-012",
            "question": "Akut İnterstisyel Nefrit tanılı bir hastanın böbrek biyopsisinde interstisyel alanda aşağıdaki enflamatuar hücrelerden hangisinin belirgin artışı tanıyı en çok destekler?",
            "options": [
                "A) Nötrofiller",
                "B) Eozinofiller ve T lenfositler",
                "C) Mast hücreleri ve bazofiller",
                "D) Yalnızca B lenfositler",
                "E) Multinükleer osteoklastlar"
            ],
            "correctAnswer": 1,
            "explanation": "AİN histopatolojisinde interstisyel ödemle birlikte en karakteristik infiltrat T lenfositler ve eozinofil lökositlerdir."
        }
    ),
    make_slide(
        13,
        "NSAİİ Nefropatisi: Çift Patoloji (AİN + Minimal Değişiklik Benzeri Nefrotik Sendrom)",
        "Siklooksijenaz İnhibisyonu, Lökotrien Şantı ve Podosit Hasarı Birlikteliği",
        """Non-steroid antiinflamatuar ilaçlar (NSAİİ) böbrekte çok çeşitli patolojik tablolara yol açabilir. Bunlar içinde en özgün ve sınavlarda en çok sorulan tablo **AİN ile Nefrotik Sendromun aynı anda geliştiği tablodur**.

**1. Patogenetik Mekanizma:**
• NSAİİ'ler COX-1 ve COX-2 enzimlerini inhibe ederek vazodilatatör prostaglandinlerin (PGI2, PGE2) sentezini bloke eder. Bu durum renal vazokonstriksiyona ve prerenal hemodinamik azotemiye yol açar.
• Prostaglandin yolu bloke olunca araşidonik asit 5-lipooksijenaz yoluna kayar (**lökotrien şantı**). Aşırı üretilen lökotrienler ve immün mediyatörler T hücrelerini aktive eder.

**2. Eş Zamanlı İki Lezyon:**
• **Lezyon 1 (İnterstisyumda):** Tipik Akut İnterstisyel Nefrit (ödem ve mononükleer/eozinofilik infiltrasyon).
• **Lezyon 2 (Glomerülde):** Minimal Değişiklik Hastalığına (MDH) benzer şekilde podosit ayaksı çıkıntılarında yaygın silinme.
• **Klinik Tablo:** Hasta hem interstisyel nefrite bağlı böbrek fonksiyon bozukluğu hem de masif **nefrotik proteinüri (>3.5 g/gün)** ile başvurur. İlaç kesildiğinde her iki patoloji de geriler.""",
        [
            {"type": "warning", "badge": "🔴 ÖZGÜN ÇİFT PATOLOJİ", "text": "Bir hastada Akut İnterstisyel Nefrit tablosuna masif nefrotik proteinüri ve podosit silinmesi eşlik ediyorsa sorumlu ilaç Non-Steroid Antiinflamatuardır (NSAİİ)!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "NSAİİ kullanımına ikincil gelişen nefropatide morfolojik olarak AİN ve Minimal Değişiklik Hastalığı (podosit silinmesi) birlikte görülür.", "color": "sky"}
        ],
        {
            "id": "prac-tub-013",
            "question": "Kronik eklem ağrıları nedeniyle yoğun ibuprofen (NSAİİ) kullanan 60 yaşındaki bir hastada akut böbrek yetmezliği ve 6 g/gün masif proteinüri saptanıyor. Biyopside tübülointerstisyel nefrit ve elektron mikroskobunda podosit ayaksı çıkıntılarında yaygın silinme izleniyor. Bu klinik tabloyu açıklayan etken hangisidir?",
            "options": [
                "A) Penisilin toksisitesi",
                "B) NSAİİ ilişkili nefropati",
                "C) Streptokok süperantijeni",
                "D) Kontrast nefropatisi",
                "E) Sisplatin toksisitesi"
            ],
            "correctAnswer": 1,
            "explanation": "NSAİİ'ler hem interstisyumu hasarlayarak AİN oluşturabilir hem de podosit ayaksı çıkıntılarını silerek nefrotik düzeyde proteinüriye (Minimal Değişiklik benzeri tablo) yol açabilir."
        }
    ),
    make_slide(
        14,
        "Analjezik Nefropatisi: Kronik Toksisite, Papiller Nekroz ve Ürotelyal Malignite",
        "Fenasetin / Asetaminofen / Aspirin Kombinasyonları ve Renal Pelvis Kanseri Riski",
        """Analjezik nefropatisi, uzun yıllar boyunca yüksek miktarda kombine analjezik (özellikle fenasetin, parasetamol, aspirin ve kafein karışımları) tüketen bireylerde gelişen kronik bir tübülointerstisyel hastalıktır. Genellikle baş ağrısı veya kas-iskelet ağrısı nedeniyle kümülatif olarak kilogramlarca analjezik alan kadınlarda görülür.

**1. Patogenez ve Papiller İskelet Hasarı:**
• **Fenasetin ve Metabolitleri (Asetaminofen):** Papilla uçlarında konsantre olur. Hücre içi glutatyonu tüketerek toksik serbest radikaller oluşturur ve lipid peroksidasyonuna yol açar.
• **Aspirin:** Prostaglandin sentezini inhibe ederek vasa rekta kan akımını azaltır ve medüller iskemiyi derinleştirir.
• Bu iki etkinin birleşimi **renal papiller nekroz** ile sonuçlanır. Nekroze papillalar kalsifiye olur veya dökülerek idrar yolunu tıkar.

**2. Ürotelyal Karsinom Riski:**
Analjezik nefropatisi olan hastaların **%8-10'unda renal pelvis veya üreter kaynaklı Ürotelyal (Transizyonel Hücreli) Karsinom** gelişir. Fenasetin metabolitlerinin karsinojenik etkisine bağlıdır. Bu nedenle hastalar idrarda ağrısız hematüri açısından ömür boyu izlenmelidir.""",
        [
            {"type": "warning", "badge": "🔴 ONKOLOJİK RİSK", "text": "Analjezik nefropatisi zemininde renal pelvis ve üreterde transizyonel hücreli (ürotelyal) karsinom riski dramatik olarak artar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Yıllarca kombine analjezik kullanımı sonucu papiller nekroz ve sonrasında ürotelyal karsinom gelişimi Analjezik Nefropatisinin klasik tablosudur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-014",
            "question": "30 yıldır kronik baş ağrısı nedeniyle fenasetin ve aspirin içeren analjezik karışımları tüketen bir kadında papiller nekroz zemininde gelişen böbrek yetmezliği saptanıyor. Bu hastada uzun dönemde hangi kanser türünün gelişme riski en yüksektir?",
            "options": [
                "A) Renal hücreli karsinom (berrak hücreli)",
                "B) Renal pelvis kaynaklı ürotelyal (transizyonel) karsinom",
                "C) Wilms tümörü",
                "D) Renal anjiyosarkom",
                "E) Prostat adenokarsinomu"
            ],
            "correctAnswer": 1,
            "explanation": "Fenasetin içeren analjeziklerin kronik kullanımı renal toplayıcı sistemde (pelvis ve üreter) Ürotelyal Karsinom gelişme riskini belirgin derecede artırır."
        }
    ),
    make_slide(
        15,
        "Miyelom Böbreği (Hafif Zincir Cast Nefropatisi): Patoloji ve Dev Hücre Reaksiyonu",
        "Bence-Jones Proteinleri, Tamm-Horsfall Kompleksleşmesi ve Kırılgan Silindirler",
        """Multipl Miyelom, monoklonal plazma hücrelerinin neoplazik proliferasyonudur; hastaların en az %50'sinde renal yetmezlik gelişir ve prognozu doğrudan belirler.

**1. Cast Nefropatisi Patogenezi:**
• Klonal plazma hücreleri aşırı miktarda monoklonal immünglobulin hafif zinciri (**Bence-Jones proteini**, kapa veya lambda) sentezler.
• Düşük molekül ağırlıklı serbest hafif zincirler glomerülden filtre olur. Proksimal tübülün endositoz kapasitesi aşılınca distal tübül ve toplayıcı kanallara ulaşır.
• Distal nefronda Henle çıkan kalın kolundan salgılanan **Tamm-Horsfall mukoproteini (üromodülin)** ile bu hafif zincirler asidik idrar ortamında çöker ve lümeni tıkayan sert agregatlar oluşturur.

**2. Karakteristik Morfoloji:**
• **Kırılgan / Çatlaklı Silindirler:** Distal tübüllerde ve toplayıcı kanallarda yerleşen, ışık mikroskobunda amorf, yoğun eozinofilik, kenarları keskin ve **çatlaklar/kırıklar gösteren (fractured / cracked casts)** büyük silindirler izlenir.
• **Dev Hücre Reaksiyonu:** Silindirlerin çevresinde tübül epitelini aşındıran mononükleer hücreler ve multinükleer histiyositik **yabancı cisim dev hücreleri** reaksiyonu gelişir. Bu görünüm Miyelom Böbreği için **patognomoniktir**.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Distal tübüllerde çatlaklı eozinofilik silindirler ve çevresinde çok çekirdekli dev hücre reaksiyonu 'Miyelom Böbreği' (Cast Nefropatisi) için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Bence-Jones proteinleri standart idrar çubuğuyla (dipstick) saptanamaz (dipstick sadece albümine duyarlıdır); sülfosalisilik asit testi veya idrar protein elektroforezi şarttır.", "color": "sky"}
        ],
        {
            "id": "prac-tub-015",
            "question": "Sedimentasyon hızı çok yüksek, anemisi ve hiperkalsemisi olan 68 yaşındaki bir hastada gelişen böbrek yetmezliği nedeniyle yapılan biyopside tübüllerde kırıklar içeren eozinofilik silindirler ve çevresinde yabancı cisim dev hücre reaksiyonu saptanıyor. Tanı nedir?",
            "options": [
                "A) Akut poststreptokokkal GN",
                "B) Miyelom böbreği (Hafif zincir cast nefropatisi)",
                "C) Membranöz nefropati",
                "D) Diyabetik glomerüloskleroz",
                "E) Alport sendromu"
            ],
            "correctAnswer": 1,
            "explanation": "Bence-Jones proteinlerinin tübüllerde oluşturduğu kırılgan silindirler ve multinükleer dev hücre reaksiyonu Multipl Miyelomun klasik böbrek tutulumudur (Cast Nefropatisi)."
        }
    ),
    make_slide(
        16,
        "Ürat Nefropatisi ve Gut Böbreği",
        "Akut Ürik Asit Nefropatisi vs Kronik Ürat Nefropatisi ve Tofüs Oluşumu",
        """Ürik asit metabolizma bozuklukları böbrekte üç farklı klinikopatolojik tabloya neden olur:

**1. Akut Ürik Asit Nefropatisi (Tümör Lizis Sendromu):**
• Lösemi ve lenfoma hastalarında kemoterapi verilmesiyle milyonlarca tümör hücresinin aniden parçalanması sonucu aşırı miktarda nükleik asit pürinleri ürik aside yıkılır.
• Aşırı yüksek ürik asit konsantrasyonu, özellikle asidik olan toplayıcı kanallarda ve distal tübüllerde **serbest ürik asit kristallerinin masif çökelmesine** yol açar.
• Tübüller mekanik olarak tıkanır ve anürik akut böbrek yetmezliği gelişir. Profilakside hidrasyon, idrarın alkalinizasyonu ve Rasburikaz / Allopurinol kullanılır.

**2. Kronik Ürat Nefropatisi (Gut Böbreği):**
• Uzun süreli hiperürisemi zemininde monosodyum ürat kristallerinin renal interstisyumda yavaşça depolanmasıdır.
• Kristaller tübüllerde değil, **interstisyumda tofüs benzeri odaklar** oluşturur.
• Çevresinde yabancı cisim dev hücreleri, lenfositler ve belirgin fibrozis gelişir; kronik böbrek yetmezliğine ilerler.

**3. Ürik Asit Nefrolitiyazisi:**
Radyolüsen (direkt grafide görülmeyen) ürik asit taşlarıdır.""",
        [
            {"type": "clinical", "badge": "🔴 ONKOLOJİK ACİL", "text": "Tümör lizis sendromunda akut ürik asit nefropatisini önlemek için kemoterapi öncesinde agresif hidrasyon ve ürik asidi parçalayan Rasburikaz tedavisi hayati önemdedir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Akut ürat nefropatisinde kristaller tübül lümenini tıkar; kronik ürat nefropatisinde ise monosodyum ürat kristalleri interstisyumda tofüs oluşturur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-016",
            "question": "Akut lösemi nedeniyle kemoterapi başlanan hastada saatler içinde anüri gelişiyor. İdrar mikroskopisinde bol miktarda iğne şeklinde ürik asit kristalleri izleniyor. Bu patolojide tübülleri tıkayan primer mekanizma hangisidir?",
            "options": [
                "A) Glomerüllerde subepitelyal hörgüçlerin birikmesi",
                "B) Asidik idrar ortamında toplayıcı kanallarda ürik asit kristallerinin masif çökelmesi",
                "C) Böbrek veninin trombozla tıkanması",
                "D) Podosit ayaksı çıkıntılarının silinmesi",
                "E) İnterstisyumda eozinofilik apse odaklarının oluşması"
            ],
            "correctAnswer": 1,
            "explanation": "Tümör lizis sendromunda pürin yıkımı sonucu aşırı üretilen ürik asit asidik distal toplayıcı kanallarda kristalleşerek lümeni mekanik olarak tıkar ve akut böbrek hasarı yapar."
        }
    ),
    make_slide(
        17,
        "Nefrokalsinozis: Hiperkalsemiye Bağlı Tübüler Kireçlenme",
        "Primer Hiperparatiroidizm, Metastatik Kalsifikasyon ve Konsantrasyon Kusuru",
        """Nefrokalsinozis, böbrek parankiminde (özellikle tübül bazal membranlarında, epitelinde ve interstisyumda) kalsiyum tuzlarının (kalsiyum fosfat veya kalsiyum okzalat) diffüz olarak birikmesidir.

**1. Etyolojik Nedenler:**
• Sistemik hiperkalsemi ile seyreden tüm durumlar (**metastatik kalsifikasyon**):
  - **Primer Hiperparatiroidizm:** Paratiroid adenomuna bağlı aşırı PTH salgısı (1 numaralı neden).
  - Maligniteye bağlı hiperkalsemi (kemik metastazları, PTHrP salgılayan tümörler).
  - Multipl Miyelom (kemik lizisi).
  - D vitamini intoksikasyonu ve Sarkoidoz (granülomlarda 1-alfa hidroksilaz aktivitesi).
  - Süt-alkali sendromu.

**2. Patoloji ve Klinik:**
• Kalsiyum tuzları öncelikle Henle kulpunda ve distal toplayıcı tübüllerde birikir. Tübül epitelinde hasar, deskuamasyon ve lümen tıkanıklığı oluşur.
• Kalsiyum birikimleri Von Kossa boyası ile siyah, hematoksilen-eozinde bazofilik koyu mavi boyanır.
• **En Erken Klinik Belirti:** Antidiüretik hormonun (ADH) medüller toplayıcı tübüllere etkisinin bozulması sonucu gelişen **nefrojenik diabetes insipidus (poliüri, polidipsi)** tablosudur. İlerleyen evrelerde taşlar ve interstisyel fibrozis eşlik eder.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Nefrokalsinozis normal dokuya kalsiyum çökmesi olduğu için metastatik kalsifikasyon örneğidir; en sık nedeni primer hiperparatiroidizmdir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Hiperkalseminin böbrekteki en erken fonksiyonel etkisi ADH duyarsızlığına bağlı gelişen konsantrasyon kusuru ve poliüridir (Nefrojenik Dİ).", "color": "sky"}
        ],
        {
            "id": "prac-tub-017",
            "question": "Primer hiperparatiroidizm tanısı alan bir hastada bilateral böbrek medullasında yaygın kalsiyum depolanması (nefrokalsinozis) saptanıyor. Bu patolojik kalsifikasyon tipi aşağıdakilerden hangisidir?",
            "options": [
                "A) Distrofik kalsifikasyon",
                "B) Metastatik kalsifikasyon",
                "C) Hyalin dejenerasyonu",
                "D) Amiloidoz",
                "E) Fibrinoid nekroz"
            ],
            "correctAnswer": 1,
            "explanation": "Serum kalsiyumunun yüksek olduğu zeminlerde normal dokularda kalsiyum birikmesi 'Metastatik Kalsifikasyon' olarak adlandırılır (Primer hiperparatiroidizm klasik örneğidir)."
        }
    ),
    make_slide(
        18,
        "Ağır Metal ve Toksin Nefropatileri: Kurşun, Kadmiyum ve Balkan Nefropatisi",
        "İntranükleer İnklüzyonlar, Fanconi Sendromu ve Aristolohik Asit Karsinogenezi",
        """Çevresel ve mesleki maruziyetler sonucu gelişen tübülointerstisyel hastalıklar spesifik morfolojik ipuçları barındırır.

**1. Kurşun Nefropatisi (Satürnizm):**
• Akü fabrikası, kurşunlu boya veya kaçak alkol maruziyeti olanlarda görülür.
• Proksimal tübül epitel hücre çekirdeklerinde **asido-rezistan koyu eozinofilik intranükleer inklüzyon cisimcikleri** izlenir (kurşun-protein kompleksleri).
• Yıllar içinde tübüler atrofi, interstisyel fibrozis, gut krizi (**satürnin gut**) ve hipertansiyona yol açar.

**2. Kadmiyum Nefropatisi:**
• Madencilik ve pil sanayii çalışanlarında görülür. Kadmiyum proksimal tübüllerde birikerek tübüler proteinüri, glikozüri, aminoasidüri ve fosfatüri ile seyreden tam bir **Fanconi Sendromu** tablosu oluşturur; kemiklerde osteomalaziye yol açar (Itai-Itai hastalığı).

**3. Balkan Endemik Nefropatisi ve Aristolohik Asit:**
• Güneydoğu Avrupa'da Tuna nehri havzasında endemik olan kronik interstisyel nefrittir.
• Unlara karışan *Aristolochia clematitis* tohumlarındaki **Aristolohik Asit** toksinine bağlıdır. Ağır bilateral kortikal atrofi ve çok yüksek oranda **üst üriner sistem ürotelyal karsinomu** geliştirir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Proksimal tübül hücre çekirdeklerinde eozinofilik asido-rezistan inklüzyon cisimcikleri Kurşun Nefropatisinin patognomonik mikroskobik bulgusudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Balkan nefropatisinin etkeni Aristolohik asittir; tübülointerstisyel fibrozis ve renal pelvis/üreterde ürotelyal kanser riskini dramatik artırır.", "color": "sky"}
        ],
        {
            "id": "prac-tub-018",
            "question": "Akü imalatında çalışan bir işçide böbrek yetmezliği, gut krizleri ve hipertansiyon saptanıyor. Biyopside proksimal tübül epitel hücre çekirdeklerinde asido-rezistan eozinofilik intranükleer inklüzyonlar izleniyor. Sorumlu ağır metal hangisidir?",
            "options": [
                "A) Cıva",
                "B) Kadmiyum",
                "C) Kurşun",
                "D) Arsenik",
                "E) Altın"
            ],
            "correctAnswer": 2,
            "explanation": "Kurşun nefropatisinde proksimal tübül epitel çekirdeklerinde kurşun-protein komplekslerinden oluşan asido-rezistan inklüzyonlar karakteristiktir; satürnin gut eşlik eder."
        }
    ),
    make_slide(
        19,
        "IgG4 İlişkili Tübülointerstisyel Nefrit",
        "Storiform Fibrozis, Obliteratif Flebit ve Bol IgG4+ Plazma Hücreleri",
        """IgG4 İlişkili Hastalık (IgG4-RD), vücutta birçok organda tümör benzeri kitle lezyonları, yoğun doku infiltrasyonu ve fibrozis ile seyreden sistemik fibroinflamatuar bir antitedir. Böbrekte en sık tutulum şekli IgG4 ilişkili tübülointerstisyel nefrittir.

**1. Klinik ve Seroloji:**
• Genellikle otoimmün pankreatit (Tip 1), retroperitoneal fibrozis (Ormond hastalığı), Riedel tiroiditi veya tükürük bezi tutulumu (Mikulicz hastalığı) olan hastalarda eşlik eden böbrek fonksiyon bozukluğu şeklinde ortaya çıkar.
• Serumda **IgG4 düzeyi belirgin derecede yüksektir**; kompleman C3 ve C4 düşüklüğü görülebilir.

**2. Histopatolojik Tanı Triadı:**
1. **Yoğun Plazmasitik İnfiltrat:** İnterstisyumda bol miktarda lenfosit ve özellikle **IgG4 pozitif plazma hücreleri** (>10-30 IgG4+ plazma hücresi / büyük büyütme alanı).
2. **Storiform Fibrozis:** Kollajen demetlerinin fırıldak veya hasır sepet örgüsü şeklinde dairesel dizildiği karakteristik 'storiform' fibrozis deseni.
3. **Obliteratif Flebit:** İnterstisyel ven lümenlerinin enflamatuar infiltrat ve miyofibroblastlar tarafından tıkanması.
• Kortikosteroid tedavisine dramatik ve hızlı yanıt verir.""",
        [
            {"type": "clinical", "badge": "🔴 SİSTEMİK BİRLİKTELİK", "text": "Otoimmün pankreatiti veya retroperitoneal fibrozisi olan bir hastada tübülointerstisyel nefrit saptandığında akla ilk IgG4 ilişkili hastalık gelmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "IgG4 ilişkili hastalığın histopatolojik üçlüsü: Storiform fibrozis, obliteratif flebit ve yoğun IgG4+ plazma hücresi infiltrasyonudur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-019",
            "question": "Retroperitoneal kitle ve otoimmün pankreatit öyküsü olan 58 yaşındaki hastada gelişen böbrek yetmezliği biyopsisinde interstisyumda 'storiform fibrozis', obliteratif flebit ve bol miktarda IgG4 pozitif plazma hücreleri izleniyor. Tanı nedir?",
            "options": [
                "A) Akut poststreptokokkal GN",
                "B) IgG4 ilişkili tübülointerstisyel nefrit",
                "C) Membranöz nefropati",
                "D) Sarkoidoz böbreği",
                "E) Malakoplaki"
            ],
            "correctAnswer": 1,
            "explanation": "Storiform fibrozis, obliteratif flebit ve IgG4+ plazma hücre infiltrasyonu IgG4 ilişkili tubulointerstisyel nefritin patognomonik üçlüsüdür."
        }
    ),
    make_slide(
        20,
        "Tübülointerstisyel Hastalıklarda İdrar Sedimenti Haritası",
        "Lökosit Silindiri, Eozinofilüri, Çamur Rengi Silindir ve Kristallerin Ayırıcı Gücü",
        """İdrar mikroskopisi, tübülointerstisyel hastalıkların ayırıcı tanısında biyopsi öncesi en hızlı ve spesifik tanısal rehberdir.

**1. Silindir Tipleri ve Klinik Karşılıkları:**
• **Lökosit Silindirleri (WBC Casts):** Nötrofillerin tübül lümeninde protein matrikse oturması.
  - *Anlamı:* Tübül içi bakteriyel veya aktif yangı.
  - *Hastalıklar:* **Akut Piyelonefrit** (1 numara), Akut İnterstisyel Nefrit.
• **Çamur Rengi Granüler Silindirler (Muddy Brown Casts):** Nekroze tubuler epitel hücre döküntüleri.
  - *Anlamı:* Şiddetli tubuler iskemik/toksik nekroz.
  - *Hastalık:* **Akut Tübüler Hasar / Nekroz (ATH/ATN)**.
• **Kırık Eozinofilik Silindirler (Cast Nefropatisi):**
  - *Anlamı:* Bence-Jones hafif zincirlerinin Tamm-Horsfall ile presipitasyonu.
  - *Hastalık:* **Multipl Miyelom (Miyelom Böbreği)**.
• **Eozinofilüri (Hansel Boyasında >%1 Eozinofil):**
  - *Anlamı:* İlaç ilişkili alerjik aşırı duyarlılık.
  - *Hastalık:* **Akut İlaç İlişkili İnterstisyel Nefrit (AİN)**.
• **Zarf / Mekik Şekilli Kalsiyum Okzalat Kristalleri:**
  - *Anlamı:* Etilen glikol (antifriz) zehirlenmesi veya aşırı okzalat yükü.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Lökosit silindiri = Akut Piyelonefrit; Çamur rengi granüler silindir = ATN; Eozinofilüri = AİN; Kırık silindir + dev hücre = Miyelom.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu 4 idrar sedimenti bulgusu nefroloji ve patoloji klinik sorularının en kilit ayrım noktasıdır.", "color": "sky"}
        ],
        {
            "id": "prac-tub-020",
            "question": "Aşağıdaki idrar mikroskopisi bulgusu ve ilişkili olduğu tübülointerstisyel hastalık eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) Lökosit silindirleri — Akut piyelonefrit",
                "B) Çamur rengi granüler silindirler — Akut tübüler nekroz (ATN)",
                "C) İdrarda eozinofiller (Hansel+) — Akut ilaç ilişkili interstisyel nefrit",
                "D) Eritrosit silindirleri — Minimal değişiklik hastalığı",
                "E) Kırık silindirler ve Bence-Jones — Multipl miyelom"
            ],
            "correctAnswer": 3,
            "explanation": "Eritrosit silindirleri nefritik sendromun (APSGN, RPGN) bulgusudur; Minimal Değişiklik Hastalığında idrar hücresiz (bland) olup eritrosit silindiri içermez."
        }
    ),
    make_slide(
        21,
        "Tübülointerstisyel Nefritlerde Biyopsi Endikasyonları ve Terapötik Yaklaşım",
        "İlaç Kesilmesi, Steroid Zamanlaması ve Geri Dönüşsüz Fibrozis Riski",
        """Tübülointerstisyel nefrit şüphesi olan bir hastada klinik yönetim ve tedavi zamanlaması doku hasarının kalıcı hale gelmesini engellemek açısından kritiktir.

**1. Biyopsi Ne Zaman Yapılmalıdır?**
• Tipik bakteriyel piyelonefritte biyopsi yapılmaz (enfeksiyon yayılma ve kanama riski).
• Şüpheli AİN olgularında: Şüpheli ilaç kesilmesine rağmen **3-5 gün içinde böbrek fonksiyonlarında düzelme başlamazsa**, veya tanıdan emin olunamıyorsa kesin tanı için **böbrek biyopsisi şarttır**.
• Biyopsi hem interstisyel yangıyı hem de fibrozis derecesini gösterir.

**2. Terapötik İlkeler:**
• **AİN:**
  - 1. Adım: Sorumlu ilacın (antibiyotik, NSAİİ, PPİ) derhal kesilmesi.
  - 2. Adım: İlaç kesilmesine rağmen kreatinin düşmüyorsa veya biyopside ağır enflamasyon varsa erken dönemde **oral kortikosteroid (Prednizon 1 mg/kg/gün)** başlanmalıdır. Erken başlanan steroid tübülointerstisyel fibrozis gelişimini engeller.
• **Akut Piyelonefrit:**
  - Uygun parenteral antibiyotik tedavisi (Seftriakson, florokinolonlar veya karbapenem) en az 10-14 gün sürdürülür.
• **Obstrüktif ve Reflü Olguları:** Ürolojik dekompresyon (stent/nefrostomi) ve VUR düzeltilmesi.""",
        [
            {"type": "clinical", "badge": "🔴 TERAPÖTİK ZAMANLAMA", "text": "AİN'de steroid tedavisine erken (ilk 1-2 hafta içinde) başlanması böbrek fonksiyonlarının tam düzelmesini sağlar; gecikildiğinde geri dönüşsüz tübülointerstisyel fibrozis gelişir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ BİLGİ", "text": "AİN tedavisinde ilk ve en önemli adım sorumlu ilacın derhal kesilmesidir; düzelmeyen olgularda kortikosteroidler verilir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-021",
            "question": "Akut ilaç ilişkili interstisyel nefrit (AİN) tanısı düşünülen bir hastada tedavi yönetiminde atılması gereken İLK ve EN KRİTİK basamak aşağıdakilerden hangisidir?",
            "options": [
                "A) Acil hemodiyaliz kateteri takılması",
                "B) Şüpheli ilacın derhal kesilmesi",
                "C) Yüksek doz siklofosfamid başlanması",
                "D) Çift taraflı perkütan nefrostomi açılması",
                "E) Hastaya geniş spektrumlu aminoglikozid başlanması"
            ],
            "correctAnswer": 1,
            "explanation": "AİN yönetiminde ilk basamak şüpheli tetikleyici ilacın derhal kesilmesidir; olguların önemli bir kısmı ilacın kesilmesiyle kendiliğinden düzelir."
        }
    ),
    make_slide(
        22,
        "Akut vs Kronik Piyelonefrit: Patoloji Karşılaştırma Matrisi",
        "Etyoloji, Makroskopi, Mikroskopi ve Komplikasyonların Karşılaştırmalı Tablosu",
        """Akut ve kronik piyelonefritin patolojik ve klinik parametrelere göre karşılaştırmalı matrisi:

| Parametre | Akut Piyelonefrit | Kronik Piyelonefrit |
| :--- | :--- | :--- |
| **Temel Etyoloji** | Akut asendan bakteriyel enfeksiyon (E. coli %85) | Tekrarlayan VUR (Reflü nefropatisi) veya kronik obstrüksiyon |
| **Böbrek Boyutu** | Büyümüş, ödemli, hiperemik | Simetrik/asimetrik küçülmüş, büzüşmüş |
| **Korteks Yüzeyi** | Ayrık sarımtırak mikroabseler | Kaba U-şekilli polar skarlar (üst ve alt kutuplarda) |
| **Kaliks Yapısı** | Hiperemik mukoza, pürülan eksüda | **Genişlemiş, küntleşmiş, deforme kaliksler** |
| **Mikroskobik İnfiltrat** | Nötrofiller (PMN), tübüler nekroz | Lenfositler, plazma hücreleri, interstisyel fibrozis |
| **Tübüler Özellik** | Nötrofil tıkaçları, tübülit | **Tiroidizasyon** (kolloid benzeri silindirler) |
| **Glomerül Durumu** | Tamamen korunmuş (erken dönemde) | Periglomerüler konsantrik fibrozis, hyalinizasyon |
| **İdrar Sedimenti** | Lökosit silindirleri, bol bakteri, piyüri | Geniş balmumu silindirleri, hafif proteinüri |
| **Klinik Tablo** | Ateş, titreme, kostavertebral açı hassasiyeti | Sinsi ilerleyen böbrek yetmezliği, hipertansiyon |""",
        [
            {"type": "warning", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "Akut piyelonefritin imzası kortikal mikroabseler ve nötrofillerdir; Kronik piyelonefritin imzası ise polar U-skarlar, kaliks küntleşmesi ve mikroskopik tiroidizasyondur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV SPOTU", "text": "Bu karşılaştırma tablosu tıp fakültesi komite sınavlarında akut-kronik piyelonefrit ayrımının eksiksiz şablonudur.", "color": "sky"}
        ],
        {
            "id": "prac-tub-022",
            "question": "Aşağıdaki patolojik bulgulardan hangisi akut piyelonefritten ziyade KRONİK piyelonefrit tanısını kesin olarak destekler?",
            "options": [
                "A) Korteks yüzeyinde etrafı hiperemik küçük sarı mikroabseler",
                "B) İnterstisyumda nötrofil infiltrasyonu",
                "C) Böbrek kutuplarında kaba U-skarlar ve altındaki kalikslerin küntleşmesi",
                "D) İdrarda lökosit silindirleri saptanması",
                "E) Renal pelviste pürülan eksüda birikimi"
            ],
            "correctAnswer": 2,
            "explanation": "Böbrek kutuplarında kaba U-şekilli skarlar ve altındaki kalikslerin deforme olup küntleşmesi Kronik Piyelonefritin (Reflü nefropatisi) ayırt edici makroskobik bulgusudur."
        }
    ),
    make_slide(
        23,
        "Tübülointerstisyel Hastalıklarda Ayırıcı Tanı ve Vaka Algoritması",
        "Klinik Prezentasyon, Laboratuvar ve Patoloji Eşleştirme Tablosu",
        """Tübülointerstisyel patolojilerin klinik vaka ipuçlarına göre tanı algoritması:

| Klinik Tablo / İpucu | Olası Tanı | Karakteristik Patolojik / İdrar Bulgusu |
| :--- | :--- | :--- |
| Şok, sepsis sonrası ani oligüri | **Akut Tübüler Hasar (ATH/ATN)** | İdrarda **çamur rengi granüler silindirler**, proksimal tübül nekrozu |
| Ateş, titreme, yan ağrısı, dizüri | **Akut Piyelonefrit** | İdrarda **lökosit silindirleri**, kortekste mikroabseler, nötrofiller |
| İlaç (antibiyotik/PPİ) sonrası döküntü, ateş | **Akut İnterstisyel Nefrit (AİN)** | İdrarda **Hansel ile eozinofil**, dokuda lenfosit/eozinofil, tubulit |
| Proteus enfeksiyonu, staghorn taş, sarı kitle | **Ksantogranülamatöz Piyelonefrit** | Bol lipid yüklü **köpüksü makrofajlar (ksantoma)**, RCC taklitçisi |
| Kronik analjezik kullanımı, hematüri | **Analjezik Nefropatisi** | **Papiller nekroz**, tübüler atrofi, **ürotelyal karsinom** riski |
| Yaşlı hasta, anemi, hiperkalsemi, kemik ağrısı | **Miyelom Böbreği** | Distal tübüllerde **çatlaklı silindirler** ve **dev hücre reaksiyonu** |
| Tümör kemoterapisi sonrası ani anüri | **Akut Ürik Asit Nefropatisi** | Toplayıcı tübüllerde **ürik asit kristal tıkaçları** |
| Diyabet, orak hücre veya obstrüksiyonda anüri | **Renal Papiller Nekroz** | Papilla uçlarında gri-beyaz koagülasyon nekrozu |""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Köpüksü makrofaj + taş = XPN; Çatlaklı silindir + dev hücre = Miyelom; Eozinofilüri = AİN; Polar skar + tiroidizasyon = Kronik Piyelonefrit.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu eşleştirme tablosu komite ve TUS klinik vaka sorularının çözülmesini sağlayan anahtar matristir.", "color": "sky"}
        ],
        {
            "id": "prac-tub-023",
            "question": "Aşağıdaki klinik tablolardan hangisinde böbrek biyopsisinde distal tübüllerde kırılgan eozinofilik silindirler ve çevresinde yabancı cisim dev hücre reaksiyonu izlenmesi beklenir?",
            "options": [
                "A) Akut poststreptokokkal GN",
                "B) Bence-Jones proteinürisi olan Multipl Miyelom hastası",
                "C) Gentamisin kullanan septik hasta",
                "D) E. coli ürosepsisi olan diyabetik hasta",
                "E) FMF zemininde amiloidoz gelişen hasta"
            ],
            "correctAnswer": 1,
            "explanation": "Multipl miyelomda hafif zincirlerin toplayıcı tübüllerde birikmesiyle oluşan kırılgan silindirler ve multinükleer dev hücre reaksiyonu patognomoniktir."
        }
    ),
    make_slide(
        24,
        "Ders 22 Kapsamlı Sentezi: Tübülointerstisyel Patolojinin Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Prof. Dr. Hikmet Keleş'in Tübülointerstisyel Hastalıklar dersinin en kritik sınav ve klinik özeti:

**1. Tübülointerstisyel Patolojinin 10 Altın Kuralı:**
1. *Tübülointerstisyel Hastalık:* Glomerüller başlangıçta korunur; en erken klinik bulgu tübül hasarına bağlı izostenüri ve noktüridir; albüminüri subnefrotiktir.
2. *Akut Tübüler Hasar (ATN):* İskemik veya nefrotoksik; idrarda çamur rengi granüler silindirler (muddy brown casts); iskemik tipte bazal membran yırtılır (tübüloreksis).
3. *Akut Piyelonefrit:* En sık etken P-fimbriyası olan UPEC (%85); asendan yol ve VUR temeldir; idrarda lökosit silindirleri (WBC casts) patognomoniktir.
4. *Papiller Nekroz:* En sık Diabetes Mellitus zemininde görülür (ayrıca analjezik, orak hücre, obstrüksiyon).
5. *Kronik Piyelonefrit:* Böbreğin üst ve alt kutuplarında kaba U-skarlar ve altındaki kalikslerin deformasyonu (küntleşmesi); mikroskopide tübüler Tiroidizasyon.
6. *Ksantogranülamatöz Piyelonefrit (XPN):* Proteus enfeksiyonu, staghorn taş ve lipid yüklü köpüksü makrofajlar; makroskobik olarak RCC'yi (böbrek kanseri) taklit eder.
7. *Malakoplaki:* Sindirilemeyen bakteri artıkları; konsantrik kalsifiye Michaelis-Gutmann cisimcikleri (Von Kossa pozitif).
8. *Akut İnterstisyel Nefrit (AİN):* Dozdan bağımsız immün reaksiyon (Tip I ve IV); antibiyotik/NSAİİ/PPİ; Ateş + Döküntü + Eozinofili; idrarda Hansel ile eozinofil.
9. *NSAİİ Çift Patolojisi:* İnterstisyumda AİN + Glomerülde Minimal Değişiklik benzeri podosit silinmesi (masif nefrotik proteinüri).
10. *Miyelom Böbreği:* Hafif zincirler (Bence-Jones); distal tübüllerde çatlaklı silindirler ve yabancı cisim dev hücre reaksiyonu.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Tübülointerstisyel hastalıklarda idrar sedimenti anahtardır: Lökosit silindiri = Piyelonefrit; Çamur silindiri = ATN; Eozinofil = AİN; Çatlak silindir = Miyelom.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slayttaki 10 altın kural komite ve TUS sınavlarında tübülointerstisyel hastalıklar konusundan gelen soruların tamamını çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-tub-024",
            "question": "Aşağıdaki klinik tablolardan hangisinde böbreğin üst ve alt kutuplarında derin U-şekilli skarlar, kaliks küntleşmesi ve mikroskopta tiroidizasyon izlenmesi beklenir?",
            "options": [
                "A) Akut ilaç ilişkili interstisyel nefrit",
                "B) Vezikoüreteral reflüye bağlı Kronik Piyelonefrit",
                "C) Minimal değişiklik hastalığı",
                "D) Goodpasture sendromu",
                "E) Akut ürik asit nefropatisi"
            ],
            "correctAnswer": 1,
            "explanation": "Kutup bölgelerinde (polar) U-şekilli kaba skarlar, kaliks deformasyonu ve mikroskopide tiroidizasyon Kronik Piyelonefritin (özellikle reflü nefropatisinin) patognomonik triadıdır."
        }
    )
]

print("Tübülointerstisyel Hastalıklar 24 slayt başarıyla tanımlandı.")

target_id = 'learn-tubulointerstisyel-hastaliklar'
for d in decks:
    if d.get('id') == target_id:
        d['title'] = "Tübülointerstisyel Böbrek Hastalıkları Patolojisi"
        d['shortTitle'] = "Tübülointerstisyel Patoloji"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Akut tübüler hasar/nekroz (çamur rengi silindirler), Akut piyelonefrit (UPEC, lökosit silindirleri), Papiller nekroz, Kronik piyelonefrit (polar U-skarlar, tiroidizasyon), Ksantogranülamatöz piyelonefrit (XPN, köpüksü makrofajlar), Malakoplaki (Michaelis-Gutmann), Akut interstisyel nefrit (Hansel eozinofilüri), NSAİİ nefropatisi ve Miyelom böbreği."
        d['slides'] = tubulo_slides
        print(f"'{target_id}' güvertesi 24 yüksek kaliteli slaytla güncellendi.")
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("Tübülointerstisyel Hastalıklar güncellemesi tamamlandı.")
