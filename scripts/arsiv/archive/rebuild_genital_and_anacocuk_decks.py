# -*- coding: utf-8 -*-
"""
Rebuild Genital Infections & Maternal-Child Health Decks with High-Quality Medical Standards
1. learn-genital-enfeksiyonlar (24 Slayt)
2. learn-ana-cocuk-sagligi (24 Slayt)
Enfeksiyon Hastalıkları & Halk Sağlığı Anabilim Dalları
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

# ==============================================================================
# 1. GENİTAL ENFEKSİYONLAR (24 SLAYT)
# ==============================================================================
genital_slides = [
    make_slide(
        1,
        "Genital Enfeksiyonlara Giriş ve Klinik Sınıflama",
        "Ülseratif Lezyonlar, Vajinitler, Servisit ve Pelvik Enflamasyon Yelpazesi",
        """Genital sistem enfeksiyonları, poliklinik başvurularının en sık nedenleri arasında yer alan, hem kadın hem erkek üreme sağlığını, fertiliteyi ve gebelik sonuçlarını doğrudan tehdit eden geniş bir hastalıklar grubudur.

**1. Anatomik ve Klinik Sınıflama:**
• **Genital Ülserle Seyreden Enfeksiyonlar:** Herpes Simpleks Virüs (HSV-2), Sifiliz (*Treponema pallidum*), Şankroid (*Haemophilus ducreyi*), Lenfogranüloma Venereum (*C. trachomatis* L1-L3), Granüloma İnguinale (*Klebsiella granulomatis*).
• **Vajinal Enfeksiyonlar (Vajinitler):** Bakteriyel Vajinozis (BV), Vulvovajinal Kandidiyazis, Trichomoniasis.
• **Alt Genital Traktüs İnflamasyonları (Servisit ve Üretrit):** *Neisseria gonorrhoeae*, *Chlamydia trachomatis*, *Mycoplasma genitalium*.
• **Üst Genital Traktüs Enfeksiyonları:** Endometrit, Salpenjit, Tuboovaryan Abse ve Pelvik Enflamatuar Hastalık (PİH).
• **Erkek Genital Enfeksiyonları:** Akut ve kronik bakteriyel prostatit, akut epididimit ve orşit.""",
        [
            {"type": "clinical", "badge": "🔴 TANI ALGORİTMASI", "text": "Genital lezyonla başvuran hastada ilk ayrım: Ülseratif lezyon mu (ağrılı/ağrısız), akıntı ile seyreden vajinit/servisit tablosu mu olduğudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Genital enfeksiyonlarda asemptomatik taşıyıcılık sıktır; ping-pong reenfeksiyonlarını önlemek için cinsel eş tedavisi zorunludur.", "color": "sky"}
        ],
        {
            "id": "prac-gen-001",
            "question": "Aşağıdaki genital enfeksiyon etkenlerinden hangisi karakteristik olarak genital ülserle değil, pürülan endoservikal ve üretral akıntı ile prezante olur?",
            "options": [
                "A) Treponema pallidum",
                "B) Herpes Simplex Virus Tip 2",
                "C) Neisseria gonorrhoeae",
                "D) Haemophilus ducreyi",
                "E) Klebsiella granulomatis"
            ],
            "correctAnswer": 2,
            "explanation": "Neisseria gonorrhoeae mukopürülan servisit ve üretrit etkenidir; ülseratif lezyon oluşturmaz. Diğer seçenekler genital ülser etkenleridir."
        }
    ),
    make_slide(
        2,
        "Genital Ülserlerin Ayırıcı Tanısı: Ağrılı vs Ağrısız Lezyonlar",
        "HSV ve Şankroid (Ağrılı) ile Sifiliz Şankrı ve LGV (Ağrısız) Ayrımı",
        """Genital ülser ayırıcı tanısında ilk ve en kritik anamnez basamağı lezyonun **AĞRILI mı yoksa AĞRISIZ mı** olduğudur.

**1. Ağrılı Genital Ülserler:**
• **Genital Herpes (HSV-1 / HSV-2):** En sık nedendir. Eritematöz zeminde grup yapmış veziküller hızla patlayarak son derece ağrılı, yüzeyel, poliploid ülserler bırakır. İki taraflı ağrılı lenfadenopati (LAP) eşlik eder.
• **Şankroid (*Haemophilus ducreyi*):** Ağrılı, yumuşak kenarlı, tabanı pürülan nekrotik eksüda ile kaplı derin ülserlerdir ('Yumuşak Şankr'). Tek taraflı, son derece ağrılı ve fluktuasyon veren süpüratif lenfadenit (**Bubo**) oluşturur; fistülize olabilir.

**2. Ağrısız Genital Ülserler:**
• **Primer Sifiliz (Sert Şankr - *Treponema pallidum*):** Tipik olarak tek, sert ve endüre kenarlı, tabanı temiz ve **TAMAMEN AĞRISIZDIR**. Ağrısız, lastik kıvamında bölgesel lenfadenopati eşlik eder.
• **Lenfogranüloma Venereum (LGV - *Chlamydia trachomatis* L1-L3):** Geçici, kendiliğinden iyileşen küçük ağrısız herpetiform papül/ülser; sonrasında inguinal ligamanın iki yanında ağrılı oluk oluşturan dev bubonlar (**Oluk / Groove belirtisi**).
• **Granüloma İnguinale (Donovanosis - *Klebsiella granulomatis*):** Ağrısız, kolay kanayan sığır eti kırmızısı (beefy-red) granülasyon ülserleri; gerçek LAP yapmaz (psödobubo). Giemsa boyasında **Donovan cisimcikleri** izlenir.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK AYIRICI TANI", "text": "Ağrılı ülser = HSV veya Şankroid (H. ducreyi); Ağrısız endüre sert ülser = Sifiliz şankrı; Oluk belirtili ağrısız papül = LGV; Donovan cisimcikli sığır eti kırmızısı = Donovanosis.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV MATRİSİ", "text": "TUS ve komitelerde en popüler soru: Sifiliz şankrı ağrısız ve sertken; Şankroid (H. ducreyi) son derece ağrılı ve yumuşaktır.", "color": "sky"}
        ],
        {
            "id": "prac-gen-002",
            "question": "Genital bölgesinde son derece ağrılı, yumuşak kenarlı, tabanı nekrotik akıntılı derin ülser ve kasığında fluktuasyon veren süpüratif ağrılı bubo saptanan hastada en olası etken hangisidir?",
            "options": [
                "A) Treponema pallidum",
                "B) Haemophilus ducreyi",
                "C) Chlamydia trachomatis L2",
                "D) Klebsiella granulomatis",
                "E) Human Papilloma Virus"
            ],
            "correctAnswer": 1,
            "explanation": "Son derece ağrılı yumuşak ülser ve süpüratif lenfadenit (bubo) Haemophilus ducreyi'nin yol açtığı Şankroid (yumuşak şankr) tablosudur."
        }
    ),
    make_slide(
        3,
        "Normal Vajinal Ekosistem ve Laktobasil Dengesi",
        "Lactobacillus crispatus, Laktik Asit, Asidik pH (<4.5) ve Hidrojen Peroksit Bariyeri",
        """Sağlıklı bir vajinal mikroçevre dinamik bir mikrobiyal dengeye dayanır.

**1. Savunmanın Temel Direği: Laktobasiller:**
• Sağlıklı üreme çağındaki bir kadında vajen florasının **%95'inden fazlasını Laktobasiller (*Lactobacillus crispatus*, *L. jensenii*)** oluşturur (Döderlein basilleri).
• Östrojen hormonu vajen çok katlı yassı epitelinde **glikojen** depolanmasını sağlar.
• Dökülen epiteldeki glikojeni metabolize eden laktobasiller **laktik asit** üreterek vajinal pH'yı **3.8 ila 4.5 arasında (asidik)** tutar.
• Asidik pH, patojen mikroorganizmaların ve fırsatçı anaerobların çoğalmasını engelleyen en kritik kimyasal kalkanıdır.
• Ayrıca laktobasiller bakteriosinler ve **Hidrojen Peroksit (H2O2)** üreterek patojen invazyonunu baskılar.

**2. Dengeyi Bozan Durumlar:**
Geniş spektrumlu antibiyotik kullanımı, vajinal duş, sık cinsel ilişki (sperm alkalendir), menopoz (östrojen düşüşü) ve rahim içi araç laktobasil popülasyonunu azaltarak vajinit gelişimine zemin hazırlar.""",
        [
            {"type": "clinical", "badge": "🔴 FİZYOLOJİK EŞİK", "text": "Normal sağlıklı vajinal pH 3.8 - 4.5 arasındadır; pH'nın 4.5'in üzerine çıkması daima patolojiktir (Bakteriyel Vajinozis veya Trikomanas lehine).", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Vajinanın asidik pH'sını koruyan ve glikojeni laktik aside çeviren koruyucu flora bakterisi Laktobasillerdir (Döderlein basilleri).", "color": "sky"}
        ],
        {
            "id": "prac-gen-003",
            "question": "Üreme çağındaki sağlıklı bir kadında vajina lümeninin asidik pH'da (3.8-4.5) kalmasını ve patojen bakterilere karşı doğal savunmayı sağlayan temel flora elemanı hangisidir?",
            "options": [
                "A) Gardnerella vaginalis",
                "B) Candida albicans",
                "C) Lactobacillus türleri (Döderlein basilleri)",
                "D) Ureaplasma urealyticum",
                "E) Streptococcus agalactiae"
            ],
            "correctAnswer": 2,
            "explanation": "Vajen epitelindeki glikojenden laktik asit sentezleyerek asidik pH oluşturan temel koruyucu mikroorganizma Laktobasillerdir."
        }
    ),
    make_slide(
        4,
        "Vulvovajinal Kandidiyazis: Patogenez, Klinik ve Tedavi",
        "Candida albicans, Peynir Kesiği Akıntı, Şiddetli Kaşıntı ve Normal pH (<4.5)",
        """Vulvovajinal kandidiyazis, kadınların yaklaşık %75'inin yaşamı boyunca en az bir kez karşılaştığı en sık semptomatik vajinal enfeksiyonlardan biridir. Olguların **%85-90'ından *Candida albicans*** sorumludur (kalan olgularda *C. glabrata* ve *C. krusei*).

**1. Kolaylaştırıcı Risk Faktörleri:**
Geniş spektrumlu antibiyotik kullanımı (laktobasilleri öldürür), kontrolsüz Diabetes Mellitus (glukoz artışı), gebelik (yüksek östrojen), immünsüpresyon (HIV, kortikosteroid) ve kombine oral kontraseptifler.

**2. Klinik Belirti ve Bulgular:**
• **Şiddetli Pruritus (Kaşıntı):** En belirgin ve rahatsız edici semptomdur. Vulvada eritem, ödem ve ekskoriyasyon eşlik eder.
• **Tipik Akıntı:** Kokusuz, beyaz, kalın, parçalı, vajen duvarına yapışık **'peynir kesiği' / 'kesilmiş süt'** görünümündedir.
• **Vajinal pH:** **NORMALDİR (<4.5)**. pH'nın normal kalması kandidiyazisi Bakteriyel Vajinozis ve Trikomanas'tan ayıran en kritik laboratuvar testidir!

**3. Tanı ve Tedavi:**
• Islak yaymada (%10 KOH ile hazırlanan nativ preparat): Tomurcuklanan maya hücreleri (blastosporlar) ve **psödohifler** izlenir.
• **Tedavi:** Topikal azol fitilleri (Klotrimazol, Mikonazol) veya oral tek doz **Flukonazol 150 mg**.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK AYIRICI TANI", "text": "Vajinal akıntısı olan hastada pH <4.5 (normal) ise ve kaşıntı belirginse tanı Vulvovajinal Kandidiyazistir; diğer iki vajinitte pH daima >4.5'tir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Peynir kesiği benzeri akıntı, normal vajinal pH (<4.5) ve %10 KOH preparatında psödohiflerin görülmesi Candida vulvovajinitinin klasik tablosudur.", "color": "sky"}
        ],
        {
            "id": "prac-gen-004",
            "question": "Yoğun vajinal kaşıntı ve beyaz peynir kesiği benzeri kokusuz akıntısı olan bir kadında ölçülen vajinal pH 4.0 (normal) saptanıyor. Nativ preparatta psödohifler görülen bu hastada en olası etken ve tedavi hangisidir?",
            "options": [
                "A) Gardnerella vaginalis — Oral Metronidazol",
                "B) Candida albicans — Tek doz oral Flukonazol",
                "C) Trichomonas vaginalis — Tek doz Metronidazol",
                "D) Chlamydia trachomatis — Doksisiklin",
                "E) Neisseria gonorrhoeae — Seftriakson"
            ],
            "correctAnswer": 1,
            "explanation": "Normal vajinal pH (<4.5), yoğun kaşıntı, peynir kesiği akıntı ve psödohifler Candida albicans enfeksiyonunu gösterir; tedavide oral flukonazol kullanılır."
        }
    ),
    make_slide(
        5,
        "Bakteriyel Vajinozis (BV): Patogenez ve Floranın Çöküşü",
        "Laktobasil Kaybı, Gardnerella vaginalis ve Polimikrobiyal Anaerob Patolojisi",
        """Bakteriyel Vajinozis (BV), doğurganlık çağındaki kadınlarda vajinal akıntının **en sık nedenidir**. Klasik bir enflamatuar enfeksiyon (lökosit infiltrasyonu) olmayıp, vajinal mikrobiyotanın derin bir disbiyozisidir (bu nedenle vajinit değil vajinozis adını alır).

**1. Patogenetik Mekanizma:**
• Hidrojen peroksit üreten koruyucu Laktobasiller dramatik olarak azalır veya tamamen yok olur.
• Laktobasil baskısının kalkmasıyla vajinada kommensal bulunan anaerobik ve fakültatif bakteriler 100-1000 kat aşırı çoğalır.
• **Sorumlu Polimikrobiyal Flora:**
  - **Gardnerella vaginalis:** Epitele tutunarak biyofilm oluşturan ana öncüdür.
  - *Atopobium vaginae*,
  - Anaeroblar: *Mobiluncus* türleri, *Prevotella*, *Bacteroides*, *Peptostreptococcus*,
  - *Mycoplasma hominis*.
• Anaerob bakterilerin ürettiği dekarboksilaz enzimleri aminleri (kadaveyrin, putresin) parçalar; bu uçucu aminler karakteristik çürük balık kokusuna yol açar.
• Asidik pH yükselir ve **pH >4.5** olur.""",
        [
            {"type": "clinical", "badge": "🔴 PATOFİZYOLOJİK ÖZELİK", "text": "Bakteriyel vajinozis klasik bir yangı değildir; vajen duvarında eritem veya lökositoz izlenmez, polimikrobiyal anaerobik disbiyozistir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Bakteriyel vajinoziste koruyucu laktobasiller kaybolur; yerini Gardnerella vaginalis ve anaeroblar (Mobiluncus, Prevotella) alır.", "color": "sky"}
        ],
        {
            "id": "prac-gen-005",
            "question": "Bakteriyel Vajinozis patogenezinde vajinal ekosistemde meydana gelen temel mikrobiyolojik değişiklik aşağıdakilerden hangisidir?",
            "options": [
                "A) Laktobasillerin aşırı çoğalarak pH'yı 3.0'a düşürmesi",
                "B) Hidrojen peroksit üreten Laktobasillerin kaybolması ve Gardnerella vaginalis ile anaerobların aşırı çoğalması",
                "C) Sadece Candida albicans türlerinin biyofilm yapması",
                "D) Treponema pallidum spiroketlerinin invazyonu",
                "E) HSV-2 virüsünün nöral ganglionlara yerleşmesi"
            ],
            "correctAnswer": 1,
            "explanation": "Bakteriyel vajinozisin temel patogenetik basamağı hidrojen peroksit üreten laktobasillerin kaybı ve anaerobik bakterilerle Gardnerella vaginalis'in masif artışıdır."
        }
    ),
    make_slide(
        6,
        "Bakteriyel Vajinoziste Amsel Kriterleri ve 'İpucu Hücreleri' (Clue Cells)",
        "Homojen Akıntı, pH >4.5, Pozitif Koku Testi ve Clue Cells ile Kesin Tanı",
        """Bakteriyel Vajinozis klinik tanısında dünya standartlarında **Amsel Kriterleri** kullanılır.

**1. Amsel Kriterleri (4 Kriterden En Az 3'ü Varsa Tanı Kesindir):**
1. **Homojen, İnce, Gri-Beyaz Akıntı:** Vajen duvarlarını pürüzsüzce sıvayan, köpüksüz, homojen akıntı.
2. **Vajinal pH > 4.5:** Laktik asit azaldığı için pH daima 4.5'in üzerindedir (genellikle 5.0 - 5.5).
3. **Pozitif Koku Testi (Whiff Testi):** Vajinal akıntı üzerine %10 KOH (potasyum hidroksit) damlatıldığında aminlerin buharlaşmasıyla keskin, tipik **'bayat/çürük balık kokusu'** açığa çıkmasıdır. Cinsel ilişki sonrası da alkalizasyonla bu koku belirginleşir.
4. **İpucu Hücreleri (Clue Cells) Varlığı:** Tanının en spesifik mikroskobik kriteridir.

**2. 'Clue Cells' (İpucu Hücreleri) Nedir?**
Salin ile hazırlanan taze ıslak yaymada incelenir. Yassı epitel hücrelerinin sitoplazmik sınırları ve membranları o kadar yoğun bakteri kümesiyle (*Gardnerella vaginalis* ve kokobasiller) kaplanmıştır ki **hücre sınırları tamamen silinmiş, buzlu cam / zımpara kağıdı benzeri noktalı bir görünüm** kazanmıştır. Epitel hücrelerinin >%20'sinin clue cell olması patognomoniktir. Belirgin lökosit (PNL) görülmez!""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Islak preparatta sınırları bakterilerle silinmiş 'Clue Cells' (İpucu Hücreleri) görülmesi Bakteriyel Vajinozis için patognomoniktir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN ÇOK SORULAN TUS KRİTERİ", "text": "Amsel kriterleri: 1) Gri-beyaz homojen akıntı, 2) pH >4.5, 3) KOH ile pozitif koku (Whiff) testi, 4) Clue cells varlığı. Tanı için en az 3'ü gereklidir.", "color": "sky"}
        ],
        {
            "id": "prac-gen-006",
            "question": "Kötü kokulu vajinal akıntısı olan bir kadında vajinal pH 5.2 ölçülüyor; %10 KOH damlatıldığında balık kokusu alınıyor ve mikroskopta sınırları bakterilerce örtülmüş 'Clue Cells' (ipucu hücreleri) izleniyor. Tanı nedir?",
            "options": [
                "A) Vulvovajinal kandidiyazis",
                "B) Bakteriyel vajinozis",
                "C) Trikomoniyazis",
                "D) Atrofik vajinit",
                "E) Gonokokkal servisit"
            ],
            "correctAnswer": 1,
            "explanation": "Homojen akıntı, pH >4.5, pozitif Whiff testi ve Clue cells varlığı Bakteriyel Vajinozisin Amsel tanı kriterleridir."
        }
    ),
    make_slide(
        7,
        "Bakteriyel Vajinozis: Obstetrik Komplikasyonlar ve Tedavi",
        "Erken Doğum, Erken Membran Rüptürü (EMR), Koryoamniyonit ve Metronidazol Rejimi",
        """Bakteriyel vajinozis sadece bir akıntı problemi olmayıp, gebelikte ve jinekolojik cerrahide çok ağır komplikasyonlara yol açar.

**1. Obstetrik ve Jinekolojik Tehlikeler:**
• Anaerob bakterilerin salgıladığı proteazlar ve fosfolipaz A2 servikovajinal kollajeni yıkar ve prostaglandin üretimini uyarır.
• **Gebelikte:** Erken doğum (preterm eylem), Erken Membran Rüptürü (EMR / suyun erken gelmesi), Koryoamniyonit ve Postpartum Endometrit riskini katlar.
• **Jinekolojide:** Pelvik Enflamatuar Hastalık (PİH) gelişimine zemin hazırlar ve HIV bulaşma riskini artırır.

**2. Tedavi Protokolü:**
• Temel amaç anaerob florayı baskılayıp laktobasillerin geri dönmesini sağlamaktır.
• **Standart Tedavi:**
  - **Oral Metronidazol:** 500 mg günde 2 kez, 7 gün boyunca, VEYA
  - **Topikal Metronidazol jel (%0.75):** Günde 1 kez 5 gün intravajinal, VEYA
  - **Klindamisin %2 krem:** Gece yatarken 7 gün intravajinal.
• **Cinsel Eş Tedavisi:** BV cinsel yolla bulaşan klasik bir enfeksiyon kabul edilmediği için **rutin cinsel eş tedavisi önerilmez** (nüksü azaltmadığı kanıtlanmıştır).""",
        [
            {"type": "clinical", "badge": "🔴 TERAPÖTİK KURAL", "text": "Bakteriyel vajinoziste rutin partner tedavisi önerilmez (Trichomonas'ta ise partner tedavisi ZORUNLUDUR). Tedavide 7 günlük Metronidazol esastır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Gebelikte Bakteriyel Vajinozis taranıp tedavi edilmelidir çünkü tedavi edilmediğinde Erken Doğum ve EMR riskini belirgin artırır.", "color": "sky"}
        ],
        {
            "id": "prac-gen-007",
            "question": "Bakteriyel vajinozis tedavisi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Tedavide birinci seçenek oral tek doz flukonazoldür",
                "B) Tüm olgularda asemptomatik erkek cinsel partnerin de eş zamanlı tedavisi zorunludur",
                "C) Standart tedavi oral veya topikal Metronidazol ile anaerobların baskılanmasıdır",
                "D) Gebelikte tedavi verilmesi kesinlikle kontrendikedir",
                "E) Tedavi sonrasında laktobasillerin çoğalması engellenmelidir"
            ],
            "correctAnswer": 2,
            "explanation": "Bakteriyel vajinozisin standart tedavisi oral veya intravajinal Metronidazoldür; rutin partner tedavisi gerekmez."
        }
    ),
    make_slide(
        8,
        "Trikomanas Enfeksiyonu (Trichomoniasis): Biyoloji ve Klinik",
        "Trichomonas vaginalis, Köpüklü Sarı-Yeşil Akıntı, 'Çilek Serviks' ve Kamçılı Trofozoit",
        """Trichomoniasis, kamçılı bir protozoon olan **Trichomonas vaginalis** tarafından oluşturulan, dünyada en sık görülen viral olmayan cinsel yolla bulaşan enfeksiyondur.

**1. Biyolojik Özellikleri:**
• *Trichomonas vaginalis* kist formu **OLMAYAN**, sadece hareketli **trofozoit** formu bulunan tek hücreli anaerobik bir parazittir.
• Ön ucunda 4 adet serbest kamçı (flagella) ve 1 adet dalgalı membran taşır.
• Trofozoitler vajen ve üretra skuamöz epiteline tutunarak yüzey hasarı oluşturur.

**2. Klinik Tablo:**
• **Karakteristik Akıntı:** Bol miktarda, **köpüklü, sarı-yeşil renkli, kötü kokulu** pürülan akıntı.
• **Vajinal pH:** Belirgin olarak **yüksektir (>5.0 - 6.5)**.
• **Kolpitis Makularis ('Çilek Serviks' / Strawberry Cervix):** Muayenede vajen duvarında ve özellikle servikste yaygın noktasal peteşiyel kanamalar ve belirgin eritem izlenir; serviks tipik bir çilek görünümü alır (hastaların %10-20'sinde patognomoniktir).
• Vulvada yanma, dizüri ve disparoni sıktır.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Servikste peteşiyal kanamalarla oluşan 'Çilek Serviks' (strawberry cervix) ve köpüklü yeşil akıntı Trichomonas vaginalis için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "T. vaginalis kist formu oluşturmaz; sadece hareketli trofozoit formu bulunur ve cinsel yolla bulaşır.", "color": "sky"}
        ],
        {
            "id": "prac-gen-008",
            "question": "Kötü kokulu, sarı-yeşil renkli, bol köpüklü vajinal akıntı ve spekulum muayenesinde servikste yaygın peteşiyel eritematöz odaklar ('çilek serviks') izlenen hastada en olası etken hangisidir?",
            "options": [
                "A) Candida albicans",
                "B) Gardnerella vaginalis",
                "C) Trichomonas vaginalis",
                "D) Neisseria gonorrhoeae",
                "E) Treponema pallidum"
            ],
            "correctAnswer": 2,
            "explanation": "Köpüklü sarı-yeşil akıntı ve servikste 'çilek serviks' (kolpitis makularis) manzarası paraziter bir enfeksiyon olan Trichomonas vaginalis'e özgüdür."
        }
    ),
    make_slide(
        9,
        "Trikomoniyazis Tanı ve Tedavisi: Nativ Preparat ve Eş Tedavisi Zorunluluğu",
        "Islak Yaymada Çırpınan Kamçılı Parazitler ve 2 Gram Tek Doz Metronidazol",
        """Trikomanas tanısı hızlı poliklinik mikroskopisi ile kolayca konabilir.

**1. Tanı Yöntemleri:**
• **Nativ Islak Preparat (Salin Mikroskopisi):** Taze vajinal sekresyondan hemen lam-lamel arası hazırlanır. Işık mikroskobunda lökositlerden biraz büyük, armut biçimli, **kamçılarıyla aktif olarak çırpınan, dönme hareketi yapan canlı trofozoitler** doğrudan görülür. (Sensitivite %60-70).
• **Kültür ve NAAT (PCR):** Şüpheli ancak nativ yayması negatif olgularda nükleik asit amplifikasyon testleri (NAAT) altın standarttır.

**2. Tedavi İlkeleri ve Hayati Eş Kuralı:**
• **Standart Tedavi:** Oral tek doz **2 gram Metronidazol** veya Tinidazol (alternatif olarak 7 gün 2x500 mg).
• **ZORUNLU Cinsel Eş Tedavisi:** Trichomonas kesinlikle cinsel yolla bulaşır. Erkeklerde genellikle asemptomatik üretral kolonizasyon yapar. **Erkek partner tedavi edilmezse kadında 'ping-pong' şeklinde sürekli reenfeksiyon gelişir!** Bu nedenle semptomu olsun veya olmasın cinsel partner mutlaka eş zamanlı olarak tedavi edilmelidir.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN KURAL", "text": "Trichomonas tanısı konduğunda asemptomatik olsa dahi CİNSEL PARTNERİN TEDAVİSİ ZORUNLUDUR; aksi halde reenfeksiyon kaçınılmazdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Taze ıslak yaymada kamçılarıyla hareket eden armut biçimli parazitlerin görülmesi Trichomonas vaginalis için tanı koydurucudur.", "color": "sky"}
        ],
        {
            "id": "prac-gen-009",
            "question": "Vajinal akıntı şikayeti olan bir hastanın taze nativ preparatında kamçıları ile aktif burgu hareketi yapan hareketli mikroorganizmalar saptanıyor. Bu hastanın yönetiminde atlanmaması gereken en kritik basamak hangisidir?",
            "options": [
                "A) Hastaya topikal nistatin fitil başlanması",
                "B) Asemptomatik cinsel partnerin de eş zamanlı olarak oral Metronidazol ile tedavi edilmesi",
                "C) Hastaya oral doksisiklin tedavisi verilmesi",
                "D) Hastanın rahmine acil RİA takılması",
                "E) Sadece vajinal duş önerilmesi"
            ],
            "correctAnswer": 1,
            "explanation": "Trichomonas vaginalis kesin cinsel yolla bulaşan bir patojendir; reenfeksiyonu engellemek için asemptomatik partnerin de mutlaka eş zamanlı tedavi edilmesi şarttır."
        }
    ),
    make_slide(
        10,
        "Vajinitlerin Büyük Karşılaştırma Atlası",
        "Kandidiyazis, Bakteriyel Vajinozis ve Trikomoniyazis Ayırıcı Tanı Tablosu",
        """Üç majör vajinal enfeksiyonun klinik, laboratuvar ve mikroskobik karşılaştırmalı matrisi:

| Özellik | Kandida Vulvovajiniti | Bakteriyel Vajinozis (BV) | Trikomoniyazis |
| :--- | :--- | :--- | :--- |
| **Etyoloji** | *Candida albicans* (Mantar) | Polimikrobiyal (Gardnerella + anaeroblar) | *Trichomonas vaginalis* (Protozoon) |
| **Baskın Semptom** | **Şiddetli kaşıntı**, yanma, eritem | Kötü koku (ilişki sonrası artar) | Bol akıntı, kaşıntı, dizüri |
| **Akıntı Görünümü** | Beyaz, kalın, **peynir kesiği** gibi | İnce, homojen, **gri-beyaz**, akıcı | Bol, **köpüklü, sarı-yeşil**, pürülan |
| **Vajinal pH** | **NORMAL (<4.5)** | **YÜKSEK (>4.5)** | **YÜKSEK (>5.0 - 6.0)** |
| **Whiff (Koku) Testi** | Negatif | **Pozitif (Çürük balık kokusu)** | Genellikle pozitif / değişken |
| **Mikroskopi Bulgusu** | **Psödohifler** ve tomurcuklanan maya | **Clue Cells (İpucu hücreleri)** | **Hareketli kamçılı trofozoitler** |
| **Serviks Muayenesi** | Normal mukoza veya eritem | Normal mukoza (enflamasyon yok) | **'Çilek Serviks'** (peteşiyel kanamalar) |
| **Birinci Basamak Tedavi** | Oral Flukonazol (tek doz 150 mg) | Oral Metronidazol (7 gün 2x500 mg) | Oral Metronidazol (Tek doz 2 g) |
| **Cinsel Partner Tedavisi** | **GEREKMEZ** | **GEREKMEZ** | **ZORUNLUDUR!** |""",
        [
            {"type": "warning", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "pH <4.5 ise = Kandida; pH >4.5 + Clue cell = Bakteriyel Vajinozis; pH >4.5 + Köpüklü yeşil akıntı + Trofozoit = Trikomanas.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV MATRİSİ", "text": "Bu tablo hem Kadın Doğum, hem Tıbbi Mikrobiyoloji, hem de İntaniye komitelerinin en garanti soru kaynağıdır.", "color": "sky"}
        ],
        {
            "id": "prac-gen-010",
            "question": "Aşağıdaki eşleştirmelerden hangisinde vajinal enfeksiyon tipi, vajinal pH ve mikroskobik bulgu doğru olarak verilmiştir?",
            "options": [
                "A) Bakteriyel vajinozis — pH <4.5 — Psödohifler",
                "B) Candida vulvovajiniti — pH <4.5 — Tomurcuklanan maya ve psödohifler",
                "C) Trichomoniasis — pH <4.0 — Clue cells",
                "D) Candida vulvovajiniti — pH >5.5 — Hareketli trofozoitler",
                "E) Bakteriyel vajinozis — pH <4.0 — Bol lökosit silindirleri"
            ],
            "correctAnswer": 1,
            "explanation": "Candida vulvovajinitinde vajinal pH normaldir (<4.5) ve mikroskopta psödohifler ile tomurcuklanan maya hücreleri izlenir."
        }
    ),
    make_slide(
        11,
        "Servisit Patolojisi: Mukopürülan Endoservikal Enflamasyon",
        "Neisseria gonorrhoeae ve Chlamydia trachomatis, Ektopi ve Frajilite",
        """Servisit, endoservikal glandüler epiteli veya ektoservikal çok katlı yassı epiteli tutan akut veya kronik enfeksiyondur. Kadınlarda cinsel yolla bulaşan enfeksiyonların en sık lokalizasyonudur.

**1. Başlıca Etyolojik Patojenler:**
• **Chlamydia trachomatis (D-K Serotipleri):** Açık ara en sık saptanan servisit etkenidir. Olguların **%70-80'i tamamen asemptomatiktir!** Bu sessiz seyir nedeniyle 'gizli salgın' olarak adlandırılır.
• **Neisseria gonorrhoeae (Gonokok):** Gram-negatif diplokok. Akut, belirgin pürülan eksüdasyon ile seyreder.
• *Mycoplasma genitalium* ve *Trichomonas vaginalis*.

**2. Klinik Bulgular:**
• Spekulum muayenesinde endoservikal kanaldan dışarı sızan **sarı-yeşil mukopürülan eksüda**.
• **Servikal Frajilite (Kolay Kanama):** Endoservikal pamuklu çubukla örnek alınırken mukozanın aniden kanamaya başlaması (kontakt kanama / postkoital kanama).
• Servikal eritem ve ödem.
• Hastalarda genellikle belirgin vajinal akıntı veya asemptomatik muayene bulgusu vardır; tedavi edilmediğinde hızla üst genital yola tırmanır.""",
        [
            {"type": "clinical", "badge": "🔴 TANI BULGUSU", "text": "Endoservikal kanalda mukopürülan sarı akıntı ve pamuklu çubuk dokundurulduğunda kolay kanama (frajilite) Akut Servisitin kardinal muayene bulgusudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Mukopürülan servisitin iki ana etkeni Chlamydia trachomatis ve Neisseria gonorrhoeae'dir; klamidya olgularının çoğunluğu asemptomatiktir.", "color": "sky"}
        ],
        {
            "id": "prac-gen-011",
            "question": "Cinsel olarak aktif 24 yaşındaki bir kadında spekulum muayenesinde endoservikal kanaldan mukopürülan sarı akıntı sızdığı ve eküvyonla temas edildiğinde serviksin kolayca kanadığı (servikal frajilite) izleniyor. Bu tabloda öncelikle taranması gereken iki majör etken hangisidir?",
            "options": [
                "A) Candida albicans ve Gardnerella vaginalis",
                "B) Chlamydia trachomatis ve Neisseria gonorrhoeae",
                "C) Treponema pallidum ve HSV-2",
                "D) HPV Tip 16 ve Tip 18",
                "E) E. coli ve Klebsiella pneumoniae"
            ],
            "correctAnswer": 1,
            "explanation": "Mukopürülan servisit ve servikal frajilite tablosunun en sık iki etkeni Chlamydia trachomatis ve Neisseria gonorrhoeae'dir."
        }
    ),
    make_slide(
        12,
        "Pelvik Enflamatuar Hastalık (PİH): Patogenez ve Asendan Yayılım",
        "Endometrit, Salpenjit, Tuboovaryan Abse ve Polimikrobiyal Peritonit",
        """Pelvik Enflamatuar Hastalık (PİH), mikroorganizmaların vajina ve serviksten yukarıya tırmanarak endometriyum, tuba uterinalar (fallop tüpleri), overler ve pelvik peritonu tuttuğu asendan bir enfeksiyon tablosudur.

**1. Asendan Patogenez:**
• Gonokok ve Klamidya servikal mukus bariyerini aşar.
• **Endometrit:** Uterusun iç tabakasının tutulumu; düzensiz adet kanamaları, lekelenme.
• **Akut Salpenjit:** Fallop tüplerinin pürülan enflamasyonu; lümen püs ile dolar (**piyosalpenks**).
• **Tuboovaryan Abse (TOA):** Pürülan enfeksiyon over parankimine yayılır ve tüple over birleşerek büyük süpüratif bir abse kitlesi oluşturur.
• İlerleyen dönemde anaerob bakteriler ve enterik floranın da eklenmesiyle polimikrobiyal ağır bir pelvik peritonit tablosu gelişir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGENEZ BASAMAĞI", "text": "PİH asendan bir enfeksiyondur: Servisit -> Endometrit -> Salpenjit -> Tuboovaryan Abse -> Pelvik Peritonit şeklinde yayılır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "PİH başlangıçta Gonore ve Klamidya ile başlar; ancak ilerleyen evrede anaerobların da katıldığı polimikrobiyal bir enfeksiyona dönüşür.", "color": "sky"}
        ],
        {
            "id": "prac-gen-012",
            "question": "Aşağıdakilerden hangisi Pelvik Enflamatuar Hastalık (PİH) gelişiminde asendan yayılım basamaklarından biri değildir?",
            "options": [
                "A) Endometrit",
                "B) Akut salpenjit",
                "C) Tuboovaryan abse",
                "D) Bartolin bezi apsesi",
                "E) Pelvik peritonit"
            ],
            "correctAnswer": 3,
            "explanation": "Bartolin bezi vulvada yer alan bir dış genital yapıdır; üst genital traktüsün asendan enfeksiyonu (PİH) kapsamında yer almaz."
        }
    ),
    make_slide(
        13,
        "PİH Klinik Tanı Kriterleri: Servikal Hareket Hassasiyeti ('Chandelier Belirtisi')",
        "Alt Karın Ağrısı, Adneksiyal Hassasiyet ve Yüksek Ateş Triadı",
        """PİH klinik olarak sinsi seyredebileceği gibi peritonit tablosuyla akut batını da taklit edebilir. Tanı geciktiğinde fertilite kalıcı olarak bozulduğu için şüphe anında ampirik tedaviye başlanmalıdır.

**1. CDC Asgari Tanı Kriterleri (En Az Biri Olmalıdır):**
Pelvik muayenede başka bir neden bulunmaksızın şu 3 bulgudan en az birinin varlığı PİH tanısı koydurur:
1. **Servikal Hareket Hassasiyeti (Chandelier Belirtisi):** Bimanuel muayenede serviks parmakla sağa-sola hareket ettirildiğinde periton irritasyonuna bağlı hastanın yerinden sıçrayacak kadar şiddetli ağrı duymasıdır.
2. **Uterus Hassasiyeti.**
3. **Adneksiyal Hassasiyet (Bilateral tüp ve overlerde ağrı).**

**2. Destekleyici Ek Kriterler:**
• Oral vücut sıcaklığı >38.3 °C,
• Anormal servikal/vajinal mukopürülan akıntı,
• Kanda lökositoz ve CRP / Sedimantasyon yüksekliği,
• Servikal kültür veya NAAT testinde Gonore veya Klamidya pozitifliği.""",
        [
            {"type": "clinical", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Jinekolojik muayenede serviksin hareket ettirilmesiyle hastanın şiddetli ağrı duyması 'Servikal Hareket Hassasiyeti' (Chandelier sign) PİH'in klinik imzasıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "PİH tanısında tek başına servikal hareket hassasiyeti veya adneksiyal hassasiyet ampirik tedaviye başlamak için yeterlidir.", "color": "sky"}
        ],
        {
            "id": "prac-gen-013",
            "question": "Kasık ağrısı ve ateşi olan 22 yaşındaki bir kadında bimanuel jinekolojik muayenede serviksin sağa-sola hareket ettirilmesiyle masif ağrı hissedildiği ('chandelier' belirtisi) ve bilateral adneksiyal hassasiyet olduğu saptanıyor. En olası tanı hangisidir?",
            "options": [
                "A) Akut apandisit",
                "B) Pelvik Enflamatuar Hastalık (PİH)",
                "C) Over kist rüptürü",
                "D) Endometriozis",
                "E) İnterstisyel sistit"
            ],
            "correctAnswer": 1,
            "explanation": "Servikal hareket hassasiyeti (chandelier belirtisi) ve adneksiyal ağrı Pelvik Enflamatuar Hastalığın (PİH) en karakteristik muayene bulgusudur."
        }
    ),
    make_slide(
        14,
        "Fitz-Hugh-Curtis Sendromu ve PİH'in Uzun Dönem Sekelleri",
        "Perihepatit, 'Keman Teli' (Violin-String) Yapışıklıkları, Ektopik Gebelik ve İnfertilite",
        """Pelvik Enflamatuar Hastalık kadın üreme sisteminde kalıcı anatomik tahribat bırakır.

**1. Fitz-Hugh-Curtis Sendromu (Gonokokkal / Klamidyal Perihepatit):**
• PİH'li hastaların %5-10'unda enfeksiyon parakolik oluklar boyunca karın içi sıvı akımıyla yukarıya, karaciğer kapsülüne ulaşır.
• Karaciğer kapsülü ile anterior karın duvarı peritonu arasında fibröz yapışıklıklar gelişir.
• **Patognomonik Laparoskopik Manzara:** Karaciğer kapsülü üzerinde ince, gergin, fibröz **'Keman Teli' (Violin-String adhesions)** yapışıklıkları izlenir.
• **Klinik:** Sağ üst kadranda plöritik, nefes almakla artan karaciğer ağrısı; sıklıkla akut kolesistit ile karıştırılır! Karaciğer enzimleri normaldir.

**2. PİH'in Uzun Dönem Ağır Sekelleri:**
• **Tubal İnfertilite (Kısırlık):** Tüplerdeki skarlaşma ve fibrozis sonucu lümen tıkanır. Tek bir PİH atağından sonra infertilite riski %12, üç ataktan sonra **%50'nin üzerine** çıkar!
• **Ektopik (Dış) Gebelik:** Tüp lümenindeki yapışıklıklar döllenmiş zigotun uterusa ulaşmasını engeller; dış gebelik riski 7-10 kat artar.
• **Kronik Pelvik Ağrı:** Kalıcı pelvik adezyonlara bağlı devamlı kasık ağrısı.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "PİH atağı sonrası karaciğer kapsülü ile karın duvarı arasında 'Keman Teli' (violin-string) yapışıklıkları görülmesi Fitz-Hugh-Curtis Sendromudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "PİH'in en önemli iki uzun dönem sekeli tubal hasara bağlı İnfertilite ve Ektopik (dış) gebelik riskinin katlanmasıdır.", "color": "sky"}
        ],
        {
            "id": "prac-gen-014",
            "question": "Geçirilmiş pelvik enfeksiyon öyküsü olan genç bir kadında sağ üst kadran ağrısı gelişiyor. Laparoskopide karaciğer kapsülü ile karın duvarı arasında ince 'keman teli' (violin-string) tarzında fibröz yapışıklıklar izleniyor. Tanı nedir?",
            "options": [
                "A) Budd-Chiari sendromu",
                "B) Fitz-Hugh-Curtis sendromu",
                "C) Meigs sendromu",
                "D) Asherman sendromu",
                "E) Sheehan sendromu"
            ],
            "correctAnswer": 1,
            "explanation": "PİH zemininde karaciğer kapsülü ile parietal periton arasında oluşan 'keman teli' yapışıklıkları Fitz-Hugh-Curtis Sendromunun (perihepatit) patognomonik lezyonudur."
        }
    ),
    make_slide(
        15,
        "PİH ve Servisit Tedavi Protokolleri: Geniş Spektrumlu Kombinasyonlar",
        "Seftriakson + Doksisiklin + Metronidazol Üçlüsü ve Yatarak Tedavi Kriterleri",
        """PİH polimikrobiyal bir enfeksiyon olduğu için tek bir antibiyotik asla yeterli değildir; tedavi mutlaka Gonore, Klamidya ve anaerobları aynı anda kapsamalıdır.

**1. Ayaktan Standart Tedavi Protokolü:**
• **Seftriakson 500 mg İM tek doz** (*N. gonorrhoeae* için) +
• **Doksisiklin 100 mg oral günde 2 kez, 14 gün** (*C. trachomatis* için) +
• **Metronidazol 500 mg oral günde 2 kez, 14 gün** (Anaeroblar ve eşlik eden bakteriyel vajinozis için).

**2. Hastaneye Yatış (Parenteral Tedavi) Endikasyonları:**
• Tuboovaryan abse (TOA) şüphesi veya varlığı,
• Gebe hastalar (doksisiklin gebede kontrendikedir, teratojendir!),
• Oral tedaviyi tolere edemeyen, bulantı-kusması olan hastalar,
• Ağır klinik tablo, yüksek ateş, peritonit bulguları,
• Ayaktan oral tedaviye 72 saatte yanıt alınamaması,
• Akut apandisit gibi cerrahi acillerin ekarte edilememesi.""",
        [
            {"type": "clinical", "badge": "🔴 TERAPÖTİK PROTOKOL", "text": "PİH tedavisinde Seftriakson (Gonore) + Doksisiklin (Klamidya) + Metronidazol (Anaerob) üçlüsü 14 gün boyunca eksiksiz uygulanmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Gebelikte PİH geliştiğinde doksisiklin kontrendike olduğu için hasta mutlaka hastaneye yatırılır ve parenteral ampisilin/sulbaktam + gentamisin rejimleri verilir.", "color": "sky"}
        ],
        {
            "id": "prac-gen-015",
            "question": "Pelvik Enflamatuar Hastalık (PİH) tanısı alan ayaktan bir hastada Gonore, Klamidya ve anaerob bakterileri kapsayan birinci basamak ampirik tedavi kombinasyonu hangisidir?",
            "options": [
                "A) Yalnızca tek doz oral siprofloksasin",
                "B) İM Seftriakson + Oral Doksisiklin + Oral Metronidazol",
                "C) Yalnızca oral amoksisilin",
                "D) Tek doz intramusküler penisilin G",
                "E) Yalnızca oral flukonazol"
            ],
            "correctAnswer": 1,
            "explanation": "CDC kılavuzlarına göre PİH ayaktan standart tedavisi İM Seftriakson + 14 gün oral Doksisiklin + oral Metronidazol kombinasyonudur."
        }
    ),
    make_slide(
        16,
        "Erkek Genital Enfeksiyonları: Akut ve Kronik Prostatit",
        "Rektal Tuşede Sıcak ve Hassas Prostat, Prostat Masajı Kontrendikasyonu ve Etyoloji",
        """Prostatit, prostat bezinin enflamatuar ve enfeksiyöz hastalıklarını kapsar; genç ve orta yaşlı erkeklerde en sık ürolojik tanıdır.

**1. Akut Bakteriyel Prostatit (Kategori I):**
• **Etyoloji:** En sık etken **Escherichia coli (%80)** ve diğer enterik Gram-negatif basillerdir (*Klebsiella, Proteus, Pseudomonas*). Genellikle enfekte idrarın prostat kanallarına intraprostatik reflüsü ile gelişir.
• **Klinik Tablo:** Ani başlayan yüksek ateş, titreme, perineal ve suprapubik ağrı, dizüri ve akut üriner retansiyon (idrar yapamama).
• **Fizik Muayene:** Rektal tuşede prostat bezi ileri derecede **büyümüş, şiş, sıcak, ödemli ve dokunmakla aşırı derecede hassastır (ağrılıdır)**.
• **HAYATİ KONTRENDİKASYON:** Akut prostatit şüphesi olan hastada **PROSTAT MASAJI KESİNLİKLE KONTRENDİKEDİR!** Masaj yapılması bakterilerin masif olarak kan dolaşımına karışmasına ve ölümcül **Gram-negatif bakteriyemiye / septik şoka** yol açar!

**2. Kronik Bakteriyel Prostatit (Kategori II):**
• Tekrarlayan idrar yolu enfeksiyonları; rektal tuşede prostat hafif hassas veya normaldir. Teşhis Meares-Stamey 4 kap testi veya prostat masajı sonrası idrar kültürü ile konur.""",
        [
            {"type": "warning", "badge": "🔴 HAYATİ KONTRENDİKASYON", "text": "Akut bakteriyel prostatitte bakteriyemi ve septik şok riskinden dolayı PROSTAT MASAJI YAPILMASI KESİNLİKLE KONTRENDİKEDİR!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Akut prostatitte en sık etken E. coli'dir; rektal tuşede sıcak ve aşırı hassas prostat bulunur; florokinolonlar prostat dokusuna iyi geçtiği için ilk tercihtir.", "color": "sky"}
        ],
        {
            "id": "prac-gen-016",
            "question": "Ateş, titreme, perineal ağrı ve idrar yapmada zorluk ile başvuran 45 yaşındaki bir erkekte rektal tuşede prostat son derece ödemli, sıcak ve aşırı hassas bulunuyor. Bu hastada sepsis ve bakteriyemi riskinden dolayı KESİNLİKLE YAPILMAMASI gereken girişim hangisidir?",
            "options": [
                "A) İdrar kültürü almak",
                "B) Kan kültürü almak",
                "C) Prostat masajı yapmak",
                "D) Damar yolu açıp hidrasyon sağlamak",
                "E) Sistemik florokinolon başlamak"
            ],
            "correctAnswer": 2,
            "explanation": "Akut bakteriyel prostatitte prostat masajı yapılması bakterilerin venöz pleksusa dökülerek fulminan bakteriyemi ve septik şoka yol açması riski nedeniyle kesinlikle kontrendikedir."
        }
    ),
    make_slide(
        17,
        "Epididimit ve Orşit Patolojisi: Prehn Belirtisi ve Kabakulak",
        "Yaşa Göre Etyoloji (<35 Yaş STD vs >35 Yaş Enterik), Testis Torsiyonu Ayrımı",
        """Epididimit ve orşit skrotum içi yapıların akut enflamatuar hastalıklarıdır; testis torsiyonu ile ayırıcı tanısı acildir.

**1. Akut Epididimit Etyolojisi (Yaşa Göre Ayrım):**
• **< 35 Yaş Cinsel Olarak Aktif Erkekler:** Neredeyse daima cinsel yolla bulaşan patojenler sorumludur: **Chlamydia trachomatis** (en sık) ve *Neisseria gonorrhoeae*.
• **> 35 Yaş veya Ürolojik Girişim Öyküsü Olanlar:** BPH ve üriner staz ilişkili enterik bakteriler sorumludur: **Escherichia coli** ve *Pseudomonas*.

**2. Prehn Belirtisi (Testis Torsiyonundan Ayrım):**
• Skrotum yukarıya, simfizis pubise doğru elle kaldırıldığında:
  - Ağrı azalıyorsa: **Pozitif Prehn Belirtisi** -> **Akut Epididimit** lehinedir.
  - Ağrı azalmıyor veya daha da artıyorsa: **Negatif Prehn Belirtisi** -> **Testis Torsiyonu** lehinedir (acil cerrahi!).
• Renkli Doppler USG'de epididimitte kan akımı artmıştır (hiperemi); torsiyonda kan akımı tamamen durmuştur.

**3. Kabakulak Orşiti (Mumps Orchitis):**
• Kabakulak (Mumps virüsü) parotitinden **4 ila 7 gün sonra** başlar.
• Postpubertal erkeklerin %20-30'unda gelişir; olguların 1/3'ü bilateraldir.
• Ağır interstisyel ödem ve seminifer tübül atrofisine yol açarak **kalıcı infertilite (kısırlık)** riski oluşturur.""",
        [
            {"type": "clinical", "badge": "🔴 ACİL AYIRICI TANI", "text": "Akut skrotal ağrıda Doppler USG ile kan akımı artışı = Epididimit; kan akımı sıfır = Testis Torsiyonu (ilk 6 saatte acil ameliyat şart!).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "35 yaş altında epididimit etkeni Klamidya ve Gonore iken; 35 yaş üstünde E. coli'dir. Testisin kaldırılmasıyla ağrının azalmasına Prehn belirtisi denir.", "color": "sky"}
        ],
        {
            "id": "prac-gen-017",
            "question": "23 yaşındaki bekar bir erkekte ani başlayan tek taraflı skrotal ağrı ve şişlik saptanıyor. Doppler ultrasonda epididimde hiperemi saptanan ve Prehn belirtisi pozitif olan bu hastada en olası etken hangisidir?",
            "options": [
                "A) Escherichia coli",
                "B) Chlamydia trachomatis",
                "C) Kabakulak virüsü",
                "D) Mycobacterium tuberculosis",
                "E) Pseudomonas aeruginosa"
            ],
            "correctAnswer": 1,
            "explanation": "35 yaş altındaki cinsel aktif genç erkeklerde akut epididimitin açık ara en sık etkeni Chlamydia trachomatis'tir (ikinci sırada Gonore)."
        }
    ),
    make_slide(
        18,
        "Genital Sistem Enfeksiyonlarında Laboratuvar Tanı Yöntemleri",
        "Gram Boyama, Nativ Preparat, NAAT (PCR) ve Serolojik Testler",
        """Genital enfeksiyonlarda etkenin mikrobiyolojik olarak hızla saptanması doğru antimikrobiyal rejimin seçilmesini sağlar.

**1. Doğrudan Mikroskopi ve Boyama Yöntemleri:**
• **Üretral Akıntıda Gram Boyama:** Nötrofillerin içinde (intrasellüler) Gram-negatif böbrek fasulyesi şeklinde çiftler (**diplokoklar**) görülmesi *Neisseria gonorrhoeae* tanısını dakikalar içinde koydurur (erkekte sensitivite >%95).
• **Nativ Islak Preparat:** Taze salin ile Trikomanas (hareketli kamçılı) ve Clue cells (bakteriyel vajinozis); %10 KOH ile Candida psödohifleri.
• **Tzanck Yayması:** HSV vezikül tabanından kazıntı; Giemsa boyasında **multinükleer dev hücreler** ve Cowdry A nükleer inklüzyonları.

**2. Moleküler Testler (NAAT / PCR):**
• Günümüzde Chlamydia trachomatis, Neisseria gonorrhoeae, Mycoplasma genitalium ve Trichomonas vaginalis tanısında kültürün yerini almış **altın standart yöntemdir**.
• İlk idrar örneğinden (first-catch urine) veya vajinal sürüntüden çalışılabilir.

**3. Seroloji:**
Sifiliz tanısında Nontreponemal (VDRL, RPR) ve Treponemal (TPHA, FTA-ABS) test kombinasyonu.""",
        [
            {"type": "clinical", "badge": "🔴 MİKROBİYOLOJİK KODLAMA", "text": "İntrasellüler Gram(-) diplokok = Gonore; Tzanck'ta multinükleer dev hücre = HSV; KOH ile psödohif = Kandida; Clue cell = BV.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Klamidya ve Gonore taramasında kültürün yerini alan en hassas altın standart yöntem NAAT'tır (Nükleik Asit Amplifikasyon Testi).", "color": "sky"}
        ],
        {
            "id": "prac-gen-018",
            "question": "Pürülan üretral akıntısı olan 26 yaşındaki bir erkeğin akıntı yaymasında lökosit sitoplazması içinde çok sayıda Gram-negatif diplokok izleniyor. Tanı nedir?",
            "options": [
                "A) Klamidyal üretrit",
                "B) Gonokokkal üretrit (Gonore)",
                "C) Trikomoniyazis",
                "D) Üreaplazma üretriti",
                "E) Sifiliz şankrı"
            ],
            "correctAnswer": 1,
            "explanation": "Lökosit içi Gram-negatif diplokoklar Neisseria gonorrhoeae'nin (Gonore) patognomonik mikroskobik görüntüsüdür."
        }
    ),
    make_slide(
        19,
        "Genital Ülser ve Enfeksiyonların Büyük Karşılaştırma Matrisi",
        "Etken, Ülser Morfolojisi, Ağrı Durumu, Lenfadenopati ve Tedavi Tablosu",
        """Genital ülserle seyreden başlıca enfeksiyonların Robbins ve Enfeksiyon kılavuzlarına göre büyük ayırıcı tanı tablosu:

| Hastalık | Etken Patojen | Ülser Sayısı ve Karakteri | Ağrı Durumu | Lenfadenopati (LAP) Özelliği | Tanı Yöntemi | Birinci Basamak Tedavi |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Genital Herpes** | HSV-1 / HSV-2 (DNA virüsü) | Çoklu, vezikül sonrası sığ ülserler | **Çok Ağrılı** | Bilateral ağrılı, süpürasyonsuz | PCR, Tzanck (dev hücre) | Oral Asiklovir / Valasiklovir |
| **Şankroid** | *Haemophilus ducreyi* (G- basil) | 1-3 adet, derin, **yumuşak kenarlı**, pürülan | **Aşırı Ağrılı** | Tek taraflı, süpüratif **Bubo** | Kültür, PCR | Azitromisin (1g) veya Seftriakson |
| **Primer Sifiliz** | *Treponema pallidum* (Spiroket) | Tek, yuvarlak, **sert endüre kenarlı**, temiz taban | **Tamamen Ağrısız** | Bilateral ağrısız, lastik kıvamında | Karanlık saha, VDRL/TPHA | **Benzatin Penisilin G** (2.4 MU İM) |
| **Lenfogranüloma Venereum** | *C. trachomatis* (L1, L2, L3) | Geçici, küçük, kaybolan papül | Ağrısız | **Oluk (Groove) belirtili** ağrılı bubonlar | NAAT / PCR, Seroloji | Doksisiklin (21 gün) |
| **Granüloma İnguinale** | *Klebsiella granulomatis* | Sığır eti kırmızısı, kanamalı granülasyon | Ağrısız | Gerçek LAP yok (Psödobubo) | Biyopside **Donovan cisimcikleri** | Azitromisin (en az 3 hafta) |""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Ağrılı: HSV (vezikül) ve Şankroid (yumuşak). Ağrısız: Sifiliz (sert), LGV (oluk belirtisi) ve Donovanosis (sığır eti granülasyonu).", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu tablo tıp fakültesi komite ve TUS sınavlarında genital ülser sorularının eksiksiz çözüm şablonudur.", "color": "sky"}
        ],
        {
            "id": "prac-gen-019",
            "question": "Aşağıdaki genital lezyonlardan hangisi tek, yuvarlak, tabanı temiz, sert endüre kenarlı ve TAMAMEN AĞRISIZ olması ile karakterizedir?",
            "options": [
                "A) Herpes simpleks ülseri",
                "B) Şankroid yumuşak şankrı",
                "C) Primer Sifiliz sert şankrı",
                "D) Behçet hastalığı oral/genital aftı",
                "E) Follikülit"
            ],
            "correctAnswer": 2,
            "explanation": "Tek, temiz tabanlı, sert endüre ve ağrısız lezyon Treponema pallidum'un neden olduğu Primer Sifiliz Şankrıdır."
        }
    ),
    make_slide(
        20,
        "Ders 2 Kapsamlı Sentezi: Genital Enfeksiyonların Klinik Kodları",
        "Enfeksiyon Hastalıkları Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Genital Enfeksiyonlar dersinin komite ve klinik odaklı 10 altın kuralı:

**1. Genital Enfeksiyonların 10 Altın Kuralı:**
1. *Ağrılı Ülser:* HSV (veziküller, Tzanck'ta multinükleer dev hücreler) ve Şankroid (H. ducreyi, yumuşak pürülan taban, süpüratif bubo).
2. *Ağrısız Ülser:* Sifiliz (sert şankr, benzatin penisilin), LGV (oluk belirtili bubo), Donovanosis (sığır eti granülasyonu, Donovan cisimcikleri).
3. *Vajinal Ekosistem:* Laktobasiller glikojenden laktik asit üreterek pH'yı <4.5 tutar; flora kaybı disbiyozise yol açar.
4. *Kandidiyazis:* Şiddetli kaşıntı, peynir kesiği akıntı, vajinal pH NORMALDİR (<4.5), psödohifler görülür; oral Flukonazol.
5. *Bakteriyel Vajinozis:* En sık vajinal akıntı nedeni; Laktobasil kaybı ve anaerob/Gardnerella artışı; gri-beyaz homojen akıntı, pH >4.5, pozitif Whiff testi ve Clue Cells; Metronidazol.
6. *Trichomoniasis:* Köpüklü sarı-yeşil akıntı, pH >5.0, çilek serviks (strawberry cervix), nativde hareketli kamçılı trofozoitler; Metronidazol + PARTNER TEDAVİSİ ZORUNLUDUR.
7. *Servisit:* Chlamydia (en sık, %70 asemptomatik) ve Gonore; mukopürülan akıntı ve servikal frajilite.
8. *PİH:* Asendan polimikrobiyal enfeksiyon; servikal hareket hassasiyeti (chandelier) patognomoniktir; Seftriakson + Doksisiklin + Metronidazol.
9. *Fitz-Hugh-Curtis:* Perihepatit; karaciğer kapsülünde 'keman teli' (violin-string) yapışıklıkları; sağ üst kadran ağrısı.
10. *Akut Prostatit:* Rektal tuşede sıcak ve aşırı hassas prostat; PROSTAT MASAJI KONTRENDİKEDİR (bakteriyemi riski!).""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Klinikte akıntı ile gelen kadında pH ölçümü ilk adımdır: <4.5 ise Kandida; >4.5 ise BV veya Trikomanas düşünülür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta özetlenen 10 altın kural genital sistem enfeksiyonları konusundaki tüm komite sorularını eksiksiz çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-gen-020",
            "question": "Aşağıdaki eşleştirmelerden hangisinde genital enfeksiyon ve karakteristik klinik/patolojik bulgu yanlış verilmiştir?",
            "options": [
                "A) Bakteriyel vajinozis — Clue cells ve pozitif koku (Whiff) testi",
                "B) Trichomonas vaginalis — Çilek serviks ve köpüklü akıntı",
                "C) Candida albicans — Vajinal pH'nın 6.0'a yükselmesi",
                "D) Fitz-Hugh-Curtis sendromu — Keman teli benzeri perihepatik yapışıklıklar",
                "E) Şankroid — Ağrılı yumuşak ülser ve süpüratif lenfadenit"
            ],
            "correctAnswer": 2,
            "explanation": "Candida albicans enfeksiyonunda vajinal pH yükselmez; normal asidik sınırlarda (<4.5) kalır. pH'nın 6.0'a çıkması Trikomanas lehinedir."
        }
    )
]

print("Genital Enfeksiyonlar 20 slayt başarıyla tanımlandı.")

# ==============================================================================
# 2. ANA ÇOCUK SAĞLIĞI DÜZEYİNİN İZLENMESİ (24 SLAYT)
# ==============================================================================
anacocuk_slides = [
    make_slide(
        1,
        "Ana Çocuk Sağlığı (AÇS): Genel Çerçeve ve Öncelikli Risk Grubu",
        "Koruyucu Hekimliğin Temel Direği, Nüfus Oranları ve Biyososyal Hassasiyet",
        """Ana ve Çocuk Sağlığı (AÇS) hizmetleri, koruyucu hekimlik ve halk sağlığının dünyada ve Türkiye'de en öncelikli, en hassas çalışma alanını oluşturur.

**1. Neden Öncelikli Risk Grubudur?**
• **Toplumun Sayısal Çoğunluğu:** Türkiye nüfusunun yaklaşık %50'den fazlasını 15-49 yaş doğurganlık çağındaki kadınlar ve 0-18 yaş çocuklar oluşturur.
• **Biyolojik ve Fizyolojik Hassasiyet:** Gebelik, doğum, lohusalık ve çocukluk dönemi büyüme-gelişmenin en hızlı olduğu, malnütrisyon, enfeksiyon ve mortalite riskine en açık biyolojik evrelerdir.
• **Toplumsal Gelecek ve Gelişmişlik Göstergesi:** Bir ülkenin sosyoekonomik gelişmişlik düzeyini, insani kalkınmasını ve sağlık sisteminin başarısını yansıtan en duyarlı uluslararası göstergeler doğrudan Ana ve Çocuk Sağlığı mortalite istatistikleridir.

**2. AÇS Temel Hedefleri:**
Gebelik öncesi danışmanlık, Doğum Öncesi Bakım (DÖB), hastanede güvenli doğum, emzirmenin teşviki, aşılama, büyüme-gelişme takibi ve istenmeyen gebeliklerin modern yöntemlerle önlenmesi.""",
        [
            {"type": "clinical", "badge": "🔴 HALK SAĞLIĞI İLKESİ", "text": "Anne ve çocuk sağlığı göstergeleri (Anne Ölüm Oranı, Bebek Ölüm Hızı) bir ülkenin sosyoekonomik gelişmişliğinin en hassas aynasıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Halk sağlığında 15-49 yaş grubu kadınlar 'Doğurganlık Çağı Kadın Nüfusu' olarak tanımlanır ve AÇS hizmetlerinin ana hedef kitlesidir.", "color": "sky"}
        ],
        {
            "id": "prac-acs-001",
            "question": "Halk sağlığında anne ve çocuk sağlığının öncelikli risk grubu olarak kabul edilmesinin temel nedenleri arasında aşağıdakilerden hangisi yer almaz?",
            "options": [
                "A) Nüfusun sayısal olarak büyük bir kısmını oluşturmaları",
                "B) Büyüme, gelişme ve gebelik nedeniyle biyolojik olarak hastalıklara daha duyarlı olmaları",
                "C) Sağlık düzeylerinin ülkenin gelişmişlik düzeyini en duyarlı yansıtan gösterge olması",
                "D) Sağlık göstergelerinin sadece genetik faktörlere bağlı olup çevre ve beslenmeden etkilenmemesi",
                "E) Önleyici hizmetlerle morbidite ve mortalitelerinin büyük oranda önlenebilir olması"
            ],
            "correctAnswer": 3,
            "explanation": "AÇS morbidite ve mortalitesi genetikten çok sosyoekonomik durum, beslenme, hijyen ve sağlık hizmetlerine erişim gibi çevresel faktörlerden etkilenir ve önlenebilir."
        }
    ),
    make_slide(
        2,
        "Anne Ölümü ve Anne Ölüm Oranı (AÖO): Tanım ve Hesaplama",
        "Gebelikte, Doğumda veya Sonrasındaki 42 Gün İçindeki Obstetrik Ölümler",
        """Anne ölümü, bir sağlık sisteminin kalitesini ve kadın sağlığına verilen değeri gösteren en kritik uluslararası epidemiyolojik ölçüttür.

**1. DSÖ Anne Ölümü Tanımı:**
Bir kadının gebelik süresince veya gebeliğin sonlanmasından (doğum, düşük, kürtaj) sonraki **42 GÜN İÇİNDE**, gebeliğin süresine ve yerine bakılmaksızın, **gebelik sürecinden kaynaklanan veya gebeliğin ağırlaştırdığı nedenlerle** meydana gelen ölümüdür.
• **Hariç Tutulanlar:** Kaza, cinayet, intihar gibi tesadüfi veya rastlantısal (akidental) nedenlerle meydana gelen ölümler anne ölümü kabul **EDİLMEZ**.

**2. Anne Ölüm Oranı (AÖO) Formülü:**
• Bir yılda meydana gelen doğrudan ve dolaylı Anne Ölümü Sayısı / Aynı yıldaki **100.000 Canlı Doğum Sayısı**.
• Paydada toplam kadın nüfusu DEĞİL, **100.000 Canlı Doğum** yer alır! Bu formül mortalite riskini doğrudan obstetrik olay sıklığına oranlar.
• Türkiye'de AÖO son 20 yılda 100.000 canlı doğumda 60'lardan **12-13 seviyelerine** düşürülmüştür.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK EPİDEMİYOLOJİK TANIM", "text": "Anne ölümü süresi gebelik ve gebeliğin sonlanmasından sonraki İLK 42 GÜNDÜR (6 hafta / lohusalık dönemi); kaza ve intihar gibi rastlantısal ölümler dahil edilmez.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SORUSU", "text": "Anne Ölüm Oranı (Maternal Mortality Ratio) hesaplanırken paydada '100.000 Canlı Doğum Sayısı' kullanılır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-002",
            "question": "Dünya Sağlık Örgütü (DSÖ) kriterlerine göre bir ölümün 'Anne Ölümü' olarak kaydedilebilmesi için gebeliğin sonlanmasından itibaren geçmesi gereken maksimum süre ne kadardır?",
            "options": [
                "A) 7 gün",
                "B) 28 gün",
                "C) 42 gün (6 hafta)",
                "D) 3 ay",
                "E) 1 yıl"
            ],
            "correctAnswer": 2,
            "explanation": "DSÖ tanımına göre gebelik süresince veya gebeliğin sonlanmasından sonraki 42 gün (lohusalık sonuna kadar) içinde obstetrik nedenlerle gelişen ölümler Anne Ölümü kabul edilir."
        }
    ),
    make_slide(
        3,
        "Anne Ölümlerinin Başlıca Nedenleri: Doğrudan vs Dolaylı Nedenler",
        "Postpartum Kanamalar, Preeklampsi/Eklampsi ve Tromboemboli",
        """Anne ölümleri tıbbi mekanizmalarına göre doğrudan ve dolaylı obstetrik nedenler olarak ikiye ayrılır.

**1. Doğrudan Obstetrik Nedenler (%75-80):**
Doğrudan gebelik, doğum ve lohusalık sürecinin kendi komplikasyonlarına bağlı ölümlerdir:
• **Postpartum Kanamalar (1 Numara):** Dünyada ve gelişmekte olan ülkelerde anne ölümlerinin en sık nedenidir; özellikle **Uterin Atoni** (rahmin kasılamaması), plasenta dekolmanı ve doğum kanalı laserasyonları.
• **Hipertansif Bozukluklar:** Preeklampsi, Eklampsi ve HELLP sendromu (intraserebral kanama, karaciğer rüptürü).
• **Lohusalık Enfeksiyonları (Puerperal Sepsis):** Endometrit, septik abortus.
• **Tromboembolizm:** Gebelikte artan hiperkoagülabilite sonucu Pulmoner Tromboemboli ve Amniyon Sıvı Embolisi.
• Distosi (zor/tıkanmış doğum) ve uterus rüptürü.

**2. Dolaylı Obstetrik Nedenler (%20-25):**
Gebelikten önce var olan veya gebelikte başlayıp gebeliğin fizyolojik yüküyle ağırlaşan hastalıklar:
• Romatizmal kalp kapak hastalıkları, peripartum kardiyomiyopati, şiddetli anemi, kontrolsüz diyabet ve enfeksiyonlar (viral hepatitler, tüberküloz).""",
        [
            {"type": "clinical", "badge": "🔴 1 NUMARALI ANNE ÖLÜM NEDENİ", "text": "Doğrudan anne ölümlerinin dünyada en sık nedeni 'Postpartum Kanamalar'dır (özellikle Uterin Atoni); ikinci sırada Hipertansif aciller (Preeklampsi/Eklampsi) gelir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Uterin atoni doğum sonrası ilk 24 saatteki masif postpartum kanamaların en sık nedenidir; doğum sonrası uterus masajı ve oksitosin profilaksisi hayat kurtarır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-003",
            "question": "Dünya genelinde doğrudan anne ölümlerinin en sık görülen nedeni aşağıdakilerden hangisidir?",
            "options": [
                "A) Puerperal sepsis",
                "B) Postpartum kanamalar (özellikle uterin atoni)",
                "C) Eklampsi nöbetleri",
                "D) Amniyon sıvı embolisi",
                "E) Ektopik gebelik rüptürü"
            ],
            "correctAnswer": 1,
            "explanation": "Doğrudan obstetrik anne ölümlerinin küresel çapta en sık nedeni doğum sonrası masif kanamalardır (özellikle uterin atoni)."
        }
    ),
    make_slide(
        4,
        "Doğum Öncesi Bakım (DÖB): Protokoller ve İzlem Takvimi",
        "Sağlık Bakanlığı Kılavuzu: Nitelikli En Az 4 İzlem Standardı",
        """Doğum Öncesi Bakım (DÖB), anne ve fetusun gebelik boyunca düzenli aralıklarla izlenerek risklerin erken taranması, önlenmesi ve tedavi edilmesini sağlayan koruyucu hekimlik sürecidir.

**1. Sağlık Bakanlığı Standart İzlem Takvimi (En Az 4 İzlem):**
Düşük riskli sağlıklı bir gebede devlet tarafından güvence altına alınan **en az 4 nitelikli izlem** protokolü:
• **1. İzlem (İlk 14 Hafta içinde - Tercihen ilk 8-10 hafta):** Gebeliğin teyidi, tam anamnez, risk değerlendirmesi, kan grubu, tam kan sayımı, TSH, tam idrar/kültür, rubella, hepatit B ve sifiliz taraması. Folik asit desteği.
• **2. İzlem (18 - 24. Haftalar):** Fetal anomali taraması (ayrıntılı ultrason), fundus yüksekliği, tansiyon, kilo, fetal kalp sesleri (FKS).
• **3. İzlem (28 - 32. Haftalar):** Gestasyonel diyabet taraması (OGTT), kan uyuşmazlığı varsa anti-D profilaksisi (28. hafta), demir desteği.
• **4. İzlem (36 - 38. Haftalar):** Doğum eylemi planı, prezentasyon kontrolü, doğumun nerede yapılacağının belirlenmesi.
• *(Gerektiğinde 40. haftaya kadar izlemler sıklaştırılır).*""",
        [
            {"type": "clinical", "badge": "🔴 PROTOKOL STANDARDI", "text": "Sağlık Bakanlığı protokolüne göre her gebenin risksiz dahi olsa gebeliği boyunca EN AZ 4 KEZ nitelikli Doğum Öncesi Bakım (DÖB) alması zorunludur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "DÖB 1. izlemi ilk 14 hafta içinde; 2. izlem 18-24. haftada; 3. izlem 28-32. haftada; 4. izlem 36-38. haftada yapılır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-004",
            "question": "T.C. Sağlık Bakanlığı Doğum Öncesi Bakım Yönetim Rehberi'ne göre düşük riskli normal bir gebelikte yapılması gereken asgari izlem sayısı kaçtır?",
            "options": [
                "A) En az 1",
                "B) En az 2",
                "C) En az 4",
                "D) En az 8",
                "E) En az 12"
            ],
            "correctAnswer": 2,
            "explanation": "Sağlık Bakanlığı kılavuzlarına göre komplikasyonsuz sağlıklı bir gebelikte asgari standart izlem sayısı en az 4'tür."
        }
    ),
    make_slide(
        5,
        "Gebelikte Rutin Profilaksi Programları: Demir ve D Vitamini Desteği",
        "Nöral Tüp Defektini Önlemede Folik Asit, Anemi Profilaksisi ve D Vitamini Damlası",
        """Sağlık Bakanlığı gebelik sürecinde tüm kadınlara ücretsiz olarak üç temel mikronütrient destek programı yürütmektedir.

**1. Folik Asit Desteği (Nöral Tüp Defekti Profilaksisi):**
• Nöral tüp embriyonik hayatın 28. gününde kapandığı için gebelik öğrenildiğinde başlanması geç olabilir!
• **Standart Doz:** Gebelik planlayan tüm kadınlara **gebelikten en az 1 ay önce başlanıp gebeliğin ilk 3 ayı (12. hafta) boyunca günlük 400 mikrogram (0.4 mg)** folik asit verilir.
• Önceki gebeliğinde NTD (Spina bifida, anansefali) öyküsü olanlarda doz 10 kat artırılarak **günlük 4 mg** verilir.

**2. Demir Desteği (Maternal Anemi Profilaksisi):**
• Gebelikte artan plazma hacmi (fizyolojik hemodilüsyon) ve fetal demir ihtiyacı nedeniyle demir eksikliği anemisi kaçınılmazdır.
• Anemi olmasa dahi **16. gebelik haftasından başlayarak** doğuma kadar ve doğum sonrası 3 ay boyunca tüm gebelere günlük **40-60 mg elementer demir** profilaksisi verilir.

**3. D Vitamini Destek Programı:**
• **12. gebelik haftasından başlayarak** gebelik boyunca ve emzirme döneminde 6 ay boyunca günlük **1200 IU (9 damla)** D vitamini ücretsiz verilir.""",
        [
            {"type": "clinical", "badge": "🔴 PROFİLAKSİ TAKVİMİ", "text": "Folik asit: Konsepsiyondan 1 ay önce başlar, ilk 12 hafta sürer (400 mcg); Demir: 16. haftadan lohusalık 3. aya kadar; D Vitamini: 12. haftadan emzirme 6. aya kadar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Spina bifida ve anensefali gibi nöral tüp defektlerini önlemek için perikonsepsiyonel dönemde folik asit desteği şarttır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-005",
            "question": "Nöral tüp defekti (spina bifida/anansefali) öyküsü bulunmayan ve gebelik planlayan sağlıklı bir kadında folik asit desteği ne zaman başlamalı ve günlük doz ne kadar olmalıdır?",
            "options": [
                "A) Gebelik testinin pozitif çıktığı gün — 100 mcg",
                "B) Gebe kalmadan en az 1 ay önce — 400 mcg (0.4 mg)",
                "C) Gebeliğin 20. haftasında — 4 mg",
                "D) Yalnızca doğumdan sonra — 1 mg",
                "E) Gebeliğin 36. haftasında — 5 mg"
            ],
            "correctAnswer": 1,
            "explanation": "Nöral tüp defektlerini önlemek için standart folik asit desteği gebelikten en az 1 ay önce başlanmalı ve günde 400 mikrogram (0.4 mg) olarak ilk trimester sonuna kadar verilmelidir."
        }
    ),
    make_slide(
        6,
        "Bebek ve Çocuk Ölüm Göstergeleri: Bebek Ölüm Hızı (BÖH)",
        "Neonatal (İlk 28 Gün) ve Postneonatal (29-365 Gün) Mortalite Analizi",
        """Çocukluk çağı mortalite ölçütleri halk sağlığının en hassas epidemiyolojik barometreleridir.

**1. Bebek Ölüm Hızı (BÖH / IMR):**
• Bir yılda 1 yaşını tamamlamadan (0-365 gün) ölen bebek sayısı / Aynı yıldaki **1.000 Canlı Doğum Sayısı**.
• Paydada **1.000 Canlı Doğum** kullanılır!
• Türkiye'de BÖH 1980'lerde binde 100'lerin üzerindeyken günümüzde binde 8-9 seviyelerine gerilemiştir.

**2. BÖH'ün İki Kritik Bileşeni:**
• **Neonatal Ölüm Hızı (NÖH):** Yaşamın **ilk 28 günü içindeki** ölümlerdir (0-28 gün):
  - *Erken Neonatal:* İlk 7 gün (0-6 gün).
  - *Geç Neonatal:* 7-28. günler.
  - *Nedenleri:* Doğum travmaları, konjenital anomaliler, prematürite, RDS, asfiksi. Sağlık hizmeti kalitesini yansıtır.
• **Postneonatal Ölüm Hızı (PNÖH):** Yaşamın **29. günü ile 365. günü arasındaki** ölümlerdir:
  - *Nedenleri:* Enfeksiyonlar (pnömoni, gastroenterit) ve malnütrisyon. Doğrudan çevre koşullarını, sosyoekonomik düzeyi ve beslenmeyi yansıtır.
• **Beş Yaş Altı Ölüm Hızı:** 5 yaşını doldurmadan ölen çocuk sayısı / 1.000 Canlı Doğum.""",
        [
            {"type": "warning", "badge": "🔴 EPİDEMİYOLOJİK AYRIM", "text": "Neonatal ölümler (ilk 28 gün) prematürite ve konjenital anomalilere bağlı olup obstetrik/yenidoğan bakım kalitesini; Postneonatal ölümler (29-365 gün) enfeksiyon ve beslenmeye bağlı olup çevre hijyenini yansıtır!", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN TUS KURALI", "text": "Bebek Ölüm Hızı formülünde payda daima '1.000 Canlı Doğum'dur; ilk 28 gün neonatal, 29-365 gün postneonatal dönemdir.", "color": "sky"}
        ],
        {
            "id": "prac-acs-006",
            "question": "Bir toplumda postneonatal ölüm hızının (29-365 gün) yüksek olması öncelikle aşağıdakilerden hangisinin yetersiz olduğunu gösterir?",
            "options": [
                "A) Anne karnındaki genetik tarama testlerinin",
                "B) Çevre sağlığı, beslenme koşulları ve enfeksiyon kontrolünün",
                "C) Yenidoğan yoğun bakım kuvöz sayısının",
                "D) Sezaryen ameliyathane donanımının",
                "E) Doğumhanedeki fetal monitörizasyonun"
            ],
            "correctAnswer": 1,
            "explanation": "Postneonatal ölümler (1 ay - 1 yaş arası) en sık pnömoni, ishal ve beslenme yetersizliğinden kaynaklandığı için doğrudan çevre sağlığı ve sosyoekonomik koşulların aynasıdır."
        }
    ),
    make_slide(
        7,
        "Yenidoğan Tarama Programları (NTP): Topuk Kanı Taraması",
        "Fenilketonüri, Konjenital Hipotiroidi, Biyotinidaz, Kistik Fibrozis, KAH ve SMA",
        """Yenidoğan Tarama Programı (NTP), tedavi edilmediğinde zeka geriliğine veya ölüme yol açan metabolik ve genetik hastalıkların semptomlar ortaya çıkmadan taranmasını sağlayan en başarılı koruyucu halk sağlığı uygulamasıdır.

**1. Örnek Alma Kuralı (Guthrie Kağıdı):**
• Bebek doğduktan sonra **en az 24-48 saat ağızdan beslendikten (protein aldıktan) sonra** özel filtre kağıdına (Guthrie kartı) topuktan birkaç damla kan alınır.
• Bebeğin beslenmeden önce kanının alınması Fenilketonüri için yalancı negatifliğe yol açabilir!

**2. Türkiye'de Taranan 6 Temel Hastalık:**
1. **Fenilketonüri (FKU):** Fenilalanin hidroksilaz eksikliği; erken özel diyetle zeka geriliği %100 önlenir.
2. **Konjenital Hipotiroidi (KHT):** TSH ölçümü ile taranır; tiroid hormonu verilmezse kalıcı kretenizm gelişir.
3. **Biyotinidaz Eksikliği:** Biyotinidaz enzim aktivitesi ölçülür; nörolojik hasar ve saç-deri döküntüsü önlenir.
4. **Kistik Fibrozis (KF):** İmmünreaktif Tripsinojen (IRT) düzeyi ile taranır.
5. **Konjenital Adrenal Hiperplazi (KAH):** 17-OH Progesteron düzeyi; tuz kaybı krizi ve ambigus genitalya önlenir.
6. **Spinal Müsküler Atrofi (SMA):** SMN1 gen delesyonu; erken gen tedavisi imkanı sağlar.""",
        [
            {"type": "warning", "badge": "🔴 TARAMA KURALI", "text": "Topuk kanı bebek en az 24-48 saat proteinle (anne sütü/mama) beslendikten sonra alınmalıdır; aç bebekte Fenilketonüri atlanabilir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Türkiye Ulusal Yenidoğan Tarama Programında taranan 6 hastalık: Fenilketonüri, Konjenital Hipotiroidi, Biyotinidaz, Kistik Fibrozis, KAH ve SMA'dır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-007",
            "question": "Aşağıdaki hastalıklardan hangisi Türkiye'de Sağlık Bakanlığı Ulusal Yenidoğan Tarama Programı kapsamında topuk kanından rutin olarak taranan hastalıklardan biri değildir?",
            "options": [
                "A) Fenilketonüri (FKU)",
                "B) Konjenital Hipotiroidi (KHT)",
                "C) Duchenne Muskuler Distrofi (DMD)",
                "D) Biyotinidaz Eksikliği",
                "E) Kistik Fibrozis (KF)"
            ],
            "correctAnswer": 2,
            "explanation": "DMD yenidoğan topuk kanı taramasında yer almaz. Rutin taranan 6 hastalık: FKU, Hipotiroidi, Biyotinidaz, Kistik Fibrozis, KAH ve SMA'dır."
        }
    ),
    make_slide(
        8,
        "Çocukluk Çağı Aşı Takvimi ve Aşı ile Önlenebilir Hastalıklar",
        "Genişletilmiş Bağışıklama Programı (GBP): Hepatit B, BCG, KKK, DaBT-İPA-Hib ve Suçiçeği",
        """Genişletilmiş Bağışıklama Programı (GBP), çocukluk çağında aşı ile önlenebilir bulaşıcı hastalıkları yok etmeyi veya kontrol altına almayı hedefleyen temel koruyucu stratejidir.

**1. Sağlık Bakanlığı Aşı Takvimi Önemli Dönüm Noktaları:**
• **Doğumda:** Hepatit B 1. doz (hastaneden taburcu olmadan).
• **1. Ayın Sonu:** Hepatit B 2. doz.
• **2. Ayın Sonu:** **BCG (Verem aşısı - sol omuza intradermal)**, 5'li Karma aşı 1. doz (**DaBT-İPA-Hib**), Konjuge Pnömokok Aşısı (KPA) 1. doz.
• **4. Ayın Sonu:** 5'li Karma 2. doz, KPA 2. doz.
• **6. Ayın Sonu:** 5'li Karma 3. doz, Hepatit B 3. doz, Oral Polio Aşısı (OPA) 1. doz.
• **12. Ayın Sonu (1 Yaş):** **KKK (Kızamık-Kızamıkçık-Kabakulak)** 1. doz, KPA pekiştirme, Suçiçeği tek doz.
• **18. Ayın Sonu:** 5'li Karma pekiştirme dozu, OPA 2. doz, Hepatit A 1. doz.
• **24. Ayın Sonu:** Hepatit A 2. doz.""",
        [
            {"type": "clinical", "badge": "🔴 AŞI TAKVİMİ KURALI", "text": "BCG aşısı 2. ayın sonunda intradermal uygulanır; KKK ve Suçiçeği aşıları canlı viral aşılar olup 12. ayın sonunda (1 yaş) yapılır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Doğumda uygulanan ilk aşı Hepatit B aşısıdır; canlı atenüe aşılar (BCG, KKK, Suçiçeği, OPA, Rotavirüs) immün yetmezlikte kontrendikedir.", "color": "sky"}
        ],
        {
            "id": "prac-acs-008",
            "question": "T.C. Sağlık Bakanlığı aşı takvimine göre sağlıklı bir bebeğe doğumdan hemen sonra (hastaneden çıkmadan) uygulanan İLK aşı hangisidir?",
            "options": [
                "A) BCG (Verem)",
                "B) Hepatit B 1. doz",
                "C) KKK (Kızamık-Kızamıkçık-Kabakulak)",
                "D) DaBT-İPA-Hib",
                "E) Oral Polio Aşısı"
            ],
            "correctAnswer": 1,
            "explanation": "Doğumda bebeğe uygulanan ilk aşı Hepatit B aşısının birinci dozudur. BCG aşısı ise 2. ayın sonunda yapılır."
        }
    ),
    make_slide(
        9,
        "Bebek Beslenmesi: Anne Sütü ve Tamamlayıcı Beslenme İlkeleri",
        "İlk 6 Ay Sadece Anne Sütü, Kolostrum, Emzirmenin Koruyucu İmmünolojisi",
        """Anne sütü, bebeğin büyüme ve gelişmesi için en mükemmel, yeri doldurulamaz biyolojik besindir.

**1. Emzirmenin Temel İlkeleri:**
• **İlk 6 Ay SADECE Anne Sütü:** İlk 6 ayda su dahil hiçbir ek gıda, içecek veya mama verilmemelidir; anne sütü bebeğin tüm sıvı, kalori ve besin ihtiyacını eksiksiz karşılar.
• **2 Yaş ve Ötesine Kadar:** 6. aydan sonra uygun tamamlayıcı besinlerle birlikte emzirmeye en az 2 yaşına kadar devam edilmelidir.

**2. Kolostrum (Ağız Sütü) — Bebeğin İlk Aşısı:**
• Doğumdan sonraki ilk birkaç gün (1-5 gün) salgılanan koyu sarı renkli süttür.
• Olgun süte göre protein, mineraller, lökositler ve özellikle **Salgısal IgA (Secretory IgA)** yönünden son derece zengindir.
• Bebeğin gastrointestinal mukozasını kaplayarak patojen invazyonuna karşı korur; mekonyumun atılmasını kolaylaştırıcı laksatif etkiye sahiptir.
• **Emzirmenin İmmünolojik Üstünlüğü:** Anne sütü laktoferrin, lizozim, bifidus faktörü ve oligosakkaritler içerir; bebeği ishal, pnömoni ve orta kulak iltihabından korur.""",
        [
            {"type": "clinical", "badge": "🔴 BESLENME KURALI", "text": "Bebeklere ilk 6 ay su dahi verilmeden SADECE anne sütü verilmelidir; ilk günlerde gelen Kolostrum salgısal IgA deposudur ve kesinlikle bebeğe verilmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Anne sütündeki en baskın immünglobulin Salgısal IgA'dır (sIgA); gastrointestinal sistem mukozasını patojenlere karşı korur.", "color": "sky"}
        ],
        {
            "id": "prac-acs-009",
            "question": "Doğumdan sonraki ilk birkaç gün salgılanan, bebeğin bağırsak mukozasını enfeksiyonlara karşı koruyan ve Salgısal IgA (sIgA) açısından son derece zengin olan ilk süte ne ad verilir?",
            "options": [
                "A) Kolostrum (Ağız sütü)",
                "B) Geçiş sütü",
                "C) Olgun süt",
                "D) Laktoferrin sütü",
                "E) Kazein sütü"
            ],
            "correctAnswer": 0,
            "explanation": "Doğum sonrası ilk günlerde salgılanan protein ve sIgA'dan zengin ilk süte Kolostrum (ağız sütü) denir."
        }
    ),
    make_slide(
        10,
        "Büyüme ve Gelişmenin İzlenmesi: Persentil Eğrileri ve Gelişim Basamakları",
        "Boy, Kilo, Baş Çevresi Ölçümleri, Persentil Düşüşleri ve 'Failure to Thrive'",
        """Büyüme (vücut boyutlarının artması) ve gelişme (nöromotor fonksiyonların olgunlaşması) çocuk sağlığının en temel göstergeleridir.

**1. Antropometrik Ölçümler ve Büyüme Eğrileri:**
• **Vücut Ağırlığı (Kilo):** Akut beslenme durumunu (malnütrisyon) ve dehidratasyonu en hızlı yansıtır. Bebek 5. ayda doğum kilosunun 2 katına, 1 yaşında 3 katına ulaşır.
• **Boy Uzunluğu:** Kronik beslenme yetersizliğini ve genetik potansiyeli yansıtır (kronik malnütrisyonda boy uzaması durur - bodurluk / stunting).
• **Baş Çevresi:** Beyin gelişimini yansıtır; ilk 2 yılda her izlemde ölçülmelidir (mikrosefali / hidrosefali tespiti).

**2. Persentil Eğrilerinin Yorumlanması:**
• 3. ve 97. persentiller normalin alt ve üst sınırlarıdır.
• **Büyümede Alarm Durumu:** Tek bir persentil değerinden ziyade **çocuğun kendi persentil eğrisinden aşağıya doğru 2 majör persentil çizgisi birden düşmesi** (örneğin 50. persentilden 10. persentilin altına gerileme) 'Büyüme-Gelişme Geriliği' (Failure to Thrive) kabul edilir ve acil organik/sosyal araştırma gerektirir.""",
        [
            {"type": "clinical", "badge": "🔴 PEDİATRİK ALARM", "text": "Çocuğun büyüme eğrisinde 2 majör persentil çizgisini birden kaybetmesi veya boy/kilonun 3. persentilin altına düşmesi patolojiktir; acil tetkik gerektirir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Sağlıklı bir süt çocuğu doğum kilosunun 2 katına ortalama 5. ayda, 3 katına ise 1 yaşında (12. ay) ulaşır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-010",
            "question": "Doğum ağırlığı 3.200 gram olan zamanında doğmuş sağlıklı bir bebeğin 1 yaşını doldurduğunda (12. ayında) beklenen ortalama vücut ağırlığı yaklaşık ne kadar olmalıdır?",
            "options": [
                "A) 6.400 gram",
                "B) 7.500 gram",
                "C) 9.600 gram (Doğum kilosunun 3 katı)",
                "D) 12.500 gram",
                "E) 15.000 gram"
            ],
            "correctAnswer": 2,
            "explanation": "Normal bir bebek ortalama 5. ayda doğum kilosunun 2 katına, 1 yaşında ise doğum kilosunun 3 katına (3.2 x 3 = ~9.6 kg) ulaşır."
        }
    ),
    make_slide(
        11,
        "Bebeklerde D Vitamini ve Demir Profilaksisi Protokolleri",
        "Raşitizmi Önlemede 400 IU D Vitamini ve 4. Ayda Profilaktik Demir Başlanması",
        """Sağlık Bakanlığı tüm bebeklere ücretsiz olarak iki ulusal profilaksi programı yürütmektedir.

**1. D Vitamini Profilaksisi (Nutrisyonel Raşitizmi Önleme):**
• Anne sütü bebeğin tüm ihtiyaçlarını karşılarken **D vitamini içeriği düşüktür**.
• Bu nedenle beslenme şeklinden (anne sütü veya mama) bağımsız olarak tüm bebeklere **doğumdan sonraki İLK HAFTADAN BAŞLANARAK 1 YAŞINA KADAR günlük 400 IU (3 damla)** D vitamini verilir.
• Bu program sayesinde ülkemizde nutrisyonel raşitizm (kemik eğrilikleri, kraniyotabes, göğüs deformiteleri) sıklığı %6'lardan binde 1'in altına düşmüştür.

**2. Demir Profilaksisi (Demir Eksikliği Anemisini Önleme):**
• Zamanında (teröpatik terme) doğan bebeklerin karaciğer demir depoları 4-6 ay yeterlidir.
• Term doğan tüm bebeklere anemi olmasa dahi **4. aydan itibaren 1 yaşına kadar günlük 10 mg (1 mg/kg/gün)** profilaktik elementer demir damlası başlanır.
• **Prematüre veya Düşük Doğum Ağırlıklı Bebeklerde:** Depolar az olduğu için profilaksiye **2. aydan itibaren 2 mg/kg/gün** dozunda başlanır.""",
        [
            {"type": "clinical", "badge": "🔴 PROFİLAKSİ TAKVİMİ", "text": "D Vitamini: Doğumdan itibaren ilk haftada başlar, 1 yaşına kadar günde 400 IU; Demir: Term bebekte 4. ayda, prematürede 2. ayda başlar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Term bebeklerde demir depoları 4. ayda tükendiği için rutin demir profilaksisine 4. ayda başlanır; prematürelerde ise 2. ayda başlanır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-011",
            "question": "Zamanında (term) ve normal doğum kilosuyla dünyaya gelen sağlıklı bir bebeğe raşitizmi ve demir eksikliği anemisini önlemek amacıyla D vitamini ve demir profilaksisi ne zaman başlanmalıdır?",
            "options": [
                "A) D vitamini 1. haftada — Demir 4. ayda",
                "B) D vitamini 6. ayda — Demir 1. yaşta",
                "C) D vitamini doğumda — Demir doğumda",
                "D) D vitamini 4. ayda — Demir 1. haftada",
                "E) Sadece anemi çıkarsa başlanmalıdır"
            ],
            "correctAnswer": 0,
            "explanation": "Sağlık Bakanlığı protokolüne göre D vitamini doğumdan sonraki ilk hafta içinde (400 IU/gün), profilaktik demir ise term bebekte 4. ayda başlanır."
        }
    ),
    make_slide(
        12,
        "Ders 2-AÇS Kapsamlı Sentezi: Ana Çocuk Sağlığı İzleminin Klinik Kodları",
        "Halk Sağlığı Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Ana Çocuk Sağlığı Düzeyinin İzlenmesi dersinin komite ve sınav odaklı 10 altın kuralı:

**1. AÇS İzleminin 10 Altın Kuralı:**
1. *Öncelikli Grup:* Kadın ve çocuk nüfusu toplumun çoğunluğudur; biyolojik riskleri yüksektir; göstergeleri ülkenin gelişmişlik aynasıdır.
2. *Anne Ölümü:* Gebelikte veya gebeliğin bitiminden sonraki İLK 42 GÜN içindeki obstetrik ölümlerdir; akidental/tesadüfi ölümler sayılmaz.
3. *Anne Ölüm Oranı (AÖO):* Anne Ölümü Sayısı / 100.000 Canlı Doğum. 1 numaralı neden Postpartum Kanamalardır (Uterin atoni).
4. *Doğum Öncesi Bakım (DÖB):* Risksiz gebede dahi EN AZ 4 NİTELİKLİ İZLEM yapılmalıdır (1. izlem ilk 14 hafta, 2. izlem 18-24 hf, 3. izlem 28-32 hf, 4. izlem 36-38 hf).
5. *Maternal Destekler:* Folik asit konsepsiyondan 1 ay önce başlar, 12. haftaya kadar sürer (400 mcg); Demir 16. haftada başlar; D vitamini 12. haftada başlar.
6. *Bebek Ölüm Hızı (BÖH):* 1 yaş altı ölümler / 1.000 Canlı Doğum.
7. *Neonatal vs Postneonatal:* Neonatal (0-28 gün) sağlık hizmeti kalitesini ve prematüriteti; Postneonatal (29-365 gün) çevre sağlığı, beslenme ve enfeksiyon kontrolünü yansıtır.
8. *Topuk Kanı Taraması:* Bebek en az 24-48 saat beslendikten sonra alınır; FKU, Hipotiroidi, Biyotinidaz, Kistik Fibrozis, KAH ve SMA taranır.
9. *Aşı Takvimi:* Doğumda ilk aşı Hepatit B'dir; BCG 2. ayda sol omuza intradermal; KKK ve Suçiçeği 12. ayda yapılır.
10. *Bebek Beslenmesi:* İlk 6 ay SADECE anne sütü; D vitamini 1. haftada (400 IU), demir 4. ayda başlanır.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Halk sağlığında anne ve çocuk sağlığını korumak tüm toplumun geleceğini kurtarır: DÖB 4 izlem + D vitamini/demir desteği + Topuk kanı taraması + Aşı takvimi.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slayttaki 10 altın kural halk sağlığı ve çocuk sağlığı komite sınavlarının eksiksiz soru haritasıdır.", "color": "sky"}
        ],
        {
            "id": "prac-acs-012",
            "question": "Aşağıdaki halk sağlığı göstergelerinden hangisinin hesaplanmasında paydada '100.000 Canlı Doğum' kullanılır?",
            "options": [
                "A) Bebek Ölüm Hızı",
                "B) Neonatal Ölüm Hızı",
                "C) Anne Ölüm Oranı (AÖO)",
                "D) Beş Yaş Altı Ölüm Hızı",
                "E) Kaba Doğum Hızı"
            ],
            "correctAnswer": 2,
            "explanation": "Bebek, neonatal ve beş yaş altı ölüm hızlarında paydada 1.000 canlı doğum kullanılırken; Anne Ölüm Oranında (AÖO) paydada 100.000 Canlı Doğum kullanılır."
        }
    )
]

print("Ana Çocuk Sağlığı 12 slayt başarıyla tanımlandı.")

# Güncelleme: Veritabanına işle
target_genital = 'learn-genital-enfeksiyonlar'
target_anacocuk = 'learn-ana-cocuk-sagligi'

for d in decks:
    if d.get('id') == target_genital:
        d['title'] = "Genital Enfeksiyonlar, Tanı ve Tedavi İlkeleri"
        d['shortTitle'] = "Genital Enfeksiyonlar"
        d['discipline'] = "Enfeksiyon Hastalıkları"
        d['committee'] = "Kurul 1"
        d['summary'] = "Genital ülser ayırıcı tanısı (Ağrılı HSV/Şankroid vs Ağrısız Sifiliz/LGV/Donovanosis), Vajinitler atlası (Kandidiyazis, Bakteriyel Vajinozis Amsel kriterleri ve Clue cells, Trikomoniyazis çilek serviks), Mukopürülan servisit (Gonore ve Klamidya), Pelvik Enflamatuar Hastalık (Chandelier belirtisi, Fitz-Hugh-Curtis keman teli yapışıklıkları) ve Erkek genital enfeksiyonları (Prostat masajı kontrendikasyonu, Prehn belirtisi)."
        d['slides'] = genital_slides
        print(f"'{target_genital}' güvertesi güncellendi.")
    elif d.get('id') == target_anacocuk:
        d['title'] = "Ana Çocuk Sağlığı Düzeyinin İzlenmesi"
        d['shortTitle'] = "Ana Çocuk Sağlığı"
        d['discipline'] = "Halk Sağlığı"
        d['committee'] = "Kurul 1"
        d['summary'] = "AÇS öncelikli risk grubu kavramı, Anne Ölüm Oranı (AÖO 42 gün kuralı, 100.000 canlı doğum), Doğrudan anne ölüm nedenleri (Uterin atoni), Doğum Öncesi Bakım (DÖB en az 4 izlem protokolü), Gebelikte folik asit, demir ve D vitamini desteği, Bebek Ölüm Hızı (BÖH), Neonatal vs Postneonatal mortalite analizi, Topuk kanı tarama programı (6 hastalık) ve Çocukluk çağı aşı takvimi."
        d['slides'] = anacocuk_slides
        print(f"'{target_anacocuk}' güvertesi güncellendi.")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("Genital Enfeksiyonlar ve Ana Çocuk Sağlığı güverteleri güncellendi.")
