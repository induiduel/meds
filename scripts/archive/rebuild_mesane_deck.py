# -*- coding: utf-8 -*-
"""
Rebuild Bladder Diseases and Tumors Deck with High-Quality Medical Standards
learn-mesane-hastaliklari-tumorleri (24 Slayt)
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

mesane_slides = [
    make_slide(
        1,
        "Alt İdrar Yolu ve Ürotelyum Biyolojisi",
        "Transizyonel Epitel, Şemsiye Hücreleri, Üroplakinler ve Asendan Savunma",
        """Alt idrar yolu anatomik olarak renal kaliksler, renal pelvis, üreterler, mesane ve proksimal üretradan meydana gelir. Bu geniş toplayıcı sistemin lümeni çok katlı özelleşmiş bir epitel olan **Ürotelyum (Transizyonel Epitel)** ile döşelidir.

**1. Ürotelyumun Hücresel Mimarisi:**
• Ürotelyum normalde 5 ila 7 hücre katından oluşur. En altta bazal hücreler, ortada ara hücreler (piriform hücreler) ve en yüzeyde lümene bakan dev **Şemsiye Hücreleri (Umbrella cells)** yer alır.
• Şemsiye hücreleri apikal membranlarında sert protein plakları (**Üroplakinler - UPIa, UPIb, UPII, UPIIIa**) taşır. Bu plaklar idrar ile kan dolaşımı arasında aşılmaz bir ozmotik ve kimyasal bariyer oluşturur; toksik idrar metabolitlerinin dokuya sızmasını engeller.
• Mesane dolup gerildiğinde şemsiye hücreleri yassılaşarak epitel katman sayısını 2-3 kata indirir; idrar boşaldığında tekrar kübikleşir.

**2. Asendan Patojenlere Karşı Savunma:**
Normal idrar akımının yıkama etkisi, mukozal Tamm-Horsfall proteini ve ürotelyal glikozaminoglikan tabakası bakterilerin adezinleriyle tutunmasını zorlaştırır.""",
        [
            {"type": "warning", "badge": "🔴 ANATOMİK / HİSTOLOJİK TEMEL", "text": "Renal pelvisten üretraya kadar tüm toplayıcı sistem ürotelyumla döşelidir; bu nedenle ürotelyal karsinomlar sadece mesanede değil, üreter ve pelviste de multifokal gelişebilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Ürotelyumun lüminal yüzeyindeki geçirimsiz bariyeri oluşturan en dış hücreler 'Şemsiye Hücreleri'dir; apikalinde Üroplakin plakları taşır.", "color": "sky"}
        ],
        {
            "id": "prac-mes-001",
            "question": "Üriner sistem toplayıcı boşluklarını (renal pelvis, üreter, mesane) döşeyen ürotelyumun lümen yüzeyinde yer alan ve idrar bileşenlerinin dokuya sızmasını engelleyen en yüzeyel hücre tabakası hangisidir?",
            "options": [
                "A) Podositler",
                "B) Şemsiye hücreleri (Umbrella cells)",
                "C) İnterkale hücreler",
                "D) Juxtaglomerüler hücreler",
                "E) Von Hansemann histiyositleri"
            ],
            "correctAnswer": 1,
            "explanation": "Ürotelyumun en üst katmanında yer alan şemsiye hücreleri üroplakin plakları sayesinde geçirimsiz osmolar bariyeri oluşturur."
        }
    ),
    make_slide(
        2,
        "Üreter Bozuklukları: UPJ Tıkanıklığı ve Retroperitoneal Fibrozis",
        "Çocukta Konjenital Hidronefroz, Ormond Hastalığı ve Üreteral Medial Deviasyon",
        """Üreter patolojileri nadir olmakla birlikte idrar akımını mekanik olarak engelleyerek hızla hidronefroz ve parankimal böbrek yetmezliğine yol açabilir.

**1. Üreteropelvik Bileşke (UPJ) Tıkanıklığı:**
• **Bebek ve çocuklarda hidronefrozun en sık konjenital nedenidir**. Erkeklerde ve sol üreterde daha sıktır.
• Temel patoloji: UPJ bölgesinde sirküler düz kas demetlerinin organizasyon bozukluğu veya böbrek alt kutbunu besleyen aberan / polar bir renal arterin üreteropelvik bileşkeye dıştan bası yapmasıdır.
• Renal pelvis ileri derecede balonlaşır (hidronefroz); cerrahi piyeloplasti ile düzeltilmezse parankim atrofisine yol açar.

**2. Retroperitoneal Fibrozis (Ormond Hastalığı):**
• Retroperitoneal alanda üreterleri, abdominal aortayı ve vena kava inferioru çevreleyen yoğun, sert, enflamatuar bir fibröz kitledir.
• **Karakteristik Radyolojik Bulgu:** Üreterlerin her iki taraftan orta hatta doğru çekilmesi (**medial deviasyon**) ve bilateral hidronefroz.
• Günümüzde olguların büyük kısmı **IgG4 İlişkili Hastalık** spektrumunda yer alır; kortikosteroid tedavisine çok iyi yanıt verir.""",
        [
            {"type": "warning", "badge": "🔴 PEDİATRİK / RADYOLOJİK KOD", "text": "Çocukta hidronefrozun 1 numaralı konjenital nedeni UPJ Darlığıdır; yetişkinde üreterlerin ortaya çekilmesiyle (medial deviasyon) seyreden bilateral obstrüksiyon Retroperitoneal Fibrozistir (Ormond).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Retroperitoneal fibrozis üreterleri medial pozisyona çeker ve sıklıkla IgG4 ilişkili sistemik fibroinflamatuar hastalık spektrumuna aittir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-002",
            "question": "Bebeklik ve erken çocukluk döneminde konjenital hidronefrozun açık ara en sık görülen anatomik nedeni aşağıdakilerden hangisidir?",
            "options": [
                "A) Posterior üretral valv",
                "B) Üreteropelvik bileşke (UPJ) darlığı / obstrüksiyonu",
                "C) Retroperitoneal fibrozis",
                "D) Üreterosel",
                "E) Mesane ekstrofisi"
            ],
            "correctAnswer": 1,
            "explanation": "Üreteropelvik bileşke (UPJ) obstrüksiyonu çocuklarda konjenital hidronefrozun en sık nedenidir."
        }
    ),
    make_slide(
        3,
        "Mesane Divertikülleri: Patogenez ve Kanser Yayılım Riski",
        "Muskularis Propria Yokluğu, İdrar Stazı, Taş ve Hızlı Evre Atlayan Karsinomlar",
        """Mesane divertikülü, mesane mukozasının mesane duvarındaki zayıf bir noktadan dışarıya doğru fıtıklaşarak (herniye olarak) kese benzeri bir kör cep oluşturmasıdır.

**1. Konjenital vs Edinsel Tipler:**
• **Konjenital Divertiküller:** Mesane kas tabakasının lokalize gelişim defektine bağlıdır; primer divertiküldür.
• **Edinsel Divertiküller (Çok Daha Sık):** Alt idrar yolu çıkım obstrüksiyonuna (en sık **Benign Prostat Hiperplazisi - BPH** veya üretral darlık) ikincil gelişir. Artan intravezikal basınca karşı detrisör kası hipertrofiye uğrar (trabekülasyon); trabeküller arasındaki zayıf noktalardan mukoza fıtıklaşır (**psödodivertikül**).

**2. Klinik Komplikasyonlar ve Kritik Onkolojik Tuzak:**
• Divertikül boynu dar olduğu için idrar boşalamaz; kronik staz nedeniyle **tekrarlayan inatçı üriner enfeksiyonlar ve mesane taşları** oluşur.
• **En Kritik Patolojik Risk:** Divertikül duvarında **muskularis propria (detrisör kas tabakası) BULUNMAZ**; duvar sadece mukoza ve ince adventisyadan ibarettir!
• Bu nedenle divertikül içinde gelişen ürotelyal karsinomlar kas bariyeri olmadığı için **çok erken evrede perivezikal yağ dokusuna yayılır (hızla T3 evresine atlar)**; prognozu normal mesane kanserlerine göre çok daha kötüdür!""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK TUZAK", "text": "Mesane divertikül duvarında muskularis propria kas tabakası bulunmaz; bu nedenle divertikül içinde gelişen kanserler kas engeline takılmadan derhal perivezikal dokuya invaze olur!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Edinsel mesane divertikülleri en sık BPH kaynaklı çıkım obstrüksiyonuna bağlı gelişir; staz taşları ve enfeksiyon sıktır.", "color": "sky"}
        ],
        {
            "id": "prac-mes-003",
            "question": "Mesane divertikülü içerisinde gelişen bir ürotelyal karsinomun standart mesane duvarında gelişen tümörlere kıyasla çok daha hızlı perivezikal yayılım göstermesinin ve evre atlamasının temel anatomik nedeni nedir?",
            "options": [
                "A) Divertikül epitelinin şemsiye hücrelerinden yoksun olması",
                "B) Divertikül duvarında muskularis propria (kalın detrisör kas tabakası) bulunmaması",
                "C) Divertikül içinde kan akımının olmaması",
                "D) Divertikül mukozasının keratinize olması",
                "E) Divertikülün sadece böbrek kutbunda yerleşmesi"
            ],
            "correctAnswer": 1,
            "explanation": "Edinsel psödodivertikül duvarı sadece mukoza ve lamina propriadan ibarettir; muskularis propria bulunmadığı için tümörler doğrudan perivezikal dokuya (T3) invaze olur."
        }
    ),
    make_slide(
        4,
        "Sistit Patolojisi: Akut Bakteriyel Sistit ve Sık Etkenler",
        "E. coli, Staphylococcus saprophyticus, Dizüri-Pollaküri Triadı ve Piyüri",
        """Sistit, mesane mukozasının enflamasyonudur. Kadınlarda kısa üretra anatomisi, cinsel aktivite ve gebelik nedeniyle erkeklere göre çok daha yaygındır (kadınların %50'si yaşam boyu en az bir kez sistit atağı geçirir).

**1. Etyolojik Mikroorganizmalar:**
• **Escherichia coli (%70-85):** Açık ara en sık etken. Fekal floradan kontamine olur.
• **Staphylococcus saprophyticus (%10-15):** Özellikle genç, cinsel olarak aktif kadınlarda E. coli'den sonraki 2 numaralı etkendir. Koagülaz negatif stafilokoktur, novobiyosine dirençlidir.
• Diğer enterik bakteriler: *Proteus mirabilis*, *Klebsiella pneumoniae*, *Enterococcus faecalis*.
• Nozokomiyal / Kateter ilişkili: *Pseudomonas aeruginosa*, *Candida albicans*.

**2. Klinik Triad ve İdrar İncelemesi:**
• **Dizüri** (idrar yaparken yanma), **Pollaküri** (sık idrara çıkma) ve **Urgency** (ani sıkışma hissi) triadı. Suprapubik dolgunluk ve ağrı eşlik eder. Sistemik ateş ve kostavertebral açı hassasiyeti **YOKTUR** (ateş varsa piyelonefrit düşünülür!).
• İdrar tetkikinde lökositüri (piyüri), bakteriüri, pozitif lökosit esteraz ve nitrit testleri pozitiftir. İdrarda lökosit silindiri **GÖRÜLMEZ** (lökosit silindiri sadece piyelonefritte oluşur).""",
        [
            {"type": "clinical", "badge": "🔴 KLİNİK AYIRICI TANI", "text": "Sistitte ateş, titreme ve kostavertebral açı hassasiyeti bulunmaz; bu sistemik bulguların veya idrarda lökosit silindirinin varlığı enfeksiyonun böbreğe ulaştığını (Piyelonefrit) kanıtlar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Genç cinsel aktif kadınlarda E. coli'den sonra en sık sistit etkeni Staphylococcus saprophyticus'tur; novobiyosine dirençlidir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-004",
            "question": "22 yaşındaki yeni evli bir kadında dizüri ve sık idrara çıkma şikayetleri ile yapılan idrar kültüründe koagülaz negatif, novobiyosine dirençli Gram-pozitif kok ürüyor. En olası etken hangisidir?",
            "options": [
                "A) Staphylococcus aureus",
                "B) Staphylococcus epidermidis",
                "C) Staphylococcus saprophyticus",
                "D) Streptococcus agalactiae",
                "E) Enterococcus faecalis"
            ],
            "correctAnswer": 2,
            "explanation": "Genç kadınlarda akut sistite yol açan koagülaz negatif ve novobiyosine dirençli stafilokok Staphylococcus saprophyticus'tur (balayı sistiti)."
        }
    ),
    make_slide(
        5,
        "Özel Sistit Tipleri: Hemorajik, İnterstisyel (Hunner Ülseri) ve Eozinofilik",
        "Siklofosfamid (Akrolein / MESNA), Mast Hücreleri ve Transmural Fibrozis",
        """Bakteriyel sistitlerin dışında kalan özel sistit formları klinik ve histopatolojik özellikleri ile sınavların gözde konularıdır.

**1. Hemorajik Sistit:**
• Mesane mukozasında yaygın kanama ve nekroz odakları ile karakterizedir.
• **Etyoloji:**
  1. *Kemoterapötik İlaçlar:* **Siklofosfamid ve İfosfamid**. İdrarla atılan toksik metabolit **Akrolein (Acrolein)** mesane ürotelyumunu yakarak masif hematüriye yol açar. Korunmada mesane irrigasyonu ve akroleini nötralize eden **MESNA** (2-merkaptoetansülfonat) infüzyonu kullanılır.
  2. *Viral Enfeksiyonlar:* İmmünsüprese çocuklarda ve kemik iliği nakli alıcılarında **Adenovirüs Tip 11 ve 34** ile BK virüs.

**2. İnterstisyel Sistit (Ağrılı Mesane Sendromu):**
• Çoğunlukla orta yaşlı kadınlarda görülen, idrar kültürü steril olan, kronik pelvik ağrı ve şiddetli pollaküri tablosudur.
• **Morfoloji:** Sistoskopide mesane gerildiğinde mukoza fissürleri, peteşiyal kanamalar ve olguların bir kısmında patognomonik **Hunner Ülserleri** izlenir.
• Biyopside mesane duvarının tüm katlarında yaygın **mast hücresi infiltrasyonu** ve ileri evrede transmural fibrozis (küçük büzüşmüş mesane) görülür.

**3. Eozinofilik Sistit:**
Alerjik diyatezi olanlarda mesane duvarında yoğun eozinofil infiltrasyonudur.""",
        [
            {"type": "warning", "badge": "🔴 FARMAKOLOJİK ANTİDOT", "text": "Siklofosfamid hemorajik sistitinden sorumlu metabolit Akroleindir; profilakside akroleini bağlayan MESNA verilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "İnterstisyel sistitin sistoskopik imzası Hunner ülserleridir; histopatolojide mesane duvarında yoğun 'mast hücresi' infiltrasyonu izlenir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-005",
            "question": "Lenfoma nedeniyle siklofosfamid kemoterapisi alan bir hastada masif ağrılı hematüri gelişiyor. Bu toksik hemorajik sistit tablosundan sorumlu idrar metaboliti ve önleyici ajan hangisidir?",
            "options": [
                "A) Ürik asit — Allopurinol",
                "B) Akrolein — MESNA",
                "C) Hidroksiüre — Folinik asit",
                "D) Siklosporin — Kortikosteroid",
                "E) Metotreksat — N-asetilsistein"
            ],
            "correctAnswer": 1,
            "explanation": "Siklofosfamidin mesane toksisitesinden sorumlu metaboliti Akroleindir; idrarda akroleini bağlayarak hemorajik sistiti önleyen ajan MESNA'dır."
        }
    ),
    make_slide(
        6,
        "Kronik İrritasyon, Metaplazi ve Schistosoma haematobium",
        "Von Brunn Adacıkları, Sistitis Kistika/Glandülaris ve Skuamöz Hücreli Karsinom",
        """Mesane mukozası kronik mekanik, kimyasal veya enfeksiyöz irritasyona maruz kaldığında çeşitli metaplastik ve proliferatif reaksiyonlar geliştirir.

**1. Von Brunn Adacıkları ve Sistitis Kistika/Glandülaris:**
• Kronik enflamasyonda ürotelyum bazal tabakası lamina propriaya doğru tomurcuklanarak içe çöker; bu yuvalara **Von Brunn adacıkları** denir.
• Bu adacıkların merkezindeki hücreler sıvı salgılayıp lüle kistik genişleme yaparsa **Sistitis Kistika**; epitel müsin salgılayan kolumnar epitele dönerse **Sistitis Glandülaris** adını alır. Adenokarsinom öncülü değildir, reaktiftir.

**2. Skuamöz Metaplazi ve Schistosoma haematobium:**
• Normalde transizyonel olan ürotelyumun kronik irritasyon sonucu çok katlı yassı (skuamöz) epitele dönüşmesidir.
• **Schistosoma haematobium:** Mısır (Nil vadisi) ve Orta Doğu'da endemik bir parazittir. Parazitin dikensi yumurtaları mesane venöz pleksusundan mesane duvarına geçer.
• Duvara gömülen yumurtalar çevresinde yoğun granülomatöz reaksiyon, fibrozis ve yaygın **keratinize skuamöz metaplazi (lökoplaki)** oluşturur.
• **En Kritik Sonuç:** Batı dünyasında mesane kanserlerinin %90'ı ürotelyal iken; *S. haematobium* endemik bölgelerinde mesane kanserlerinin **%75'i Skuamöz Hücreli Karsinomdur (SCC)!**""",
        [
            {"type": "warning", "badge": "🔴 ONKOLOJİK BAĞLANTI", "text": "Schistosoma haematobium enfeksiyonu mesanede yaygın skuamöz metaplaziye ve doğrudan Skuamöz Hücreli Karsinom (SCC) gelişimine yol açar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Mısır seyahati öyküsü, hematüri ve mesane biyopsisinde terminal dikensi parazit yumurtaları zemininde gelişen kanser Skuamöz Hücreli Karsinomdur.", "color": "sky"}
        ],
        {
            "id": "prac-mes-006",
            "question": "Nil nehri havzasında yaşayan ve kronik idrar yolu enfeksiyonu öyküsü olan bir hastanın mesane biyopsisinde lamina propriada kalsifiye parazit yumurtaları ve yaygın keratinize skuamöz metaplazi izleniyor. Bu hastada gelişme riski en yüksek olan mesane malignitesi hangisidir?",
            "options": [
                "A) Papiller ürotelyal karsinom",
                "B) Skuamöz hücreli karsinom (SCC)",
                "C) Mesane adenokarsinomu",
                "D) Küçük hücreli nöroendokrin karsinom",
                "E) Rabdomiyosarkom"
            ],
            "correctAnswer": 1,
            "explanation": "Schistosoma haematobium enfeksiyonu mesanede kronik skuamöz metaplazi oluşturarak baskın olarak Skuamöz Hücreli Karsinom gelişimine yol açar."
        }
    ),
    make_slide(
        7,
        "Mesane Tümörlerine Giriş ve Saha Kanseri (Field Cancerization) Kavramı",
        "İdrar Yolu Maligniteleri, Endüstriyel Maruziyet ve Çok Odaklı (Multifokal) Nüksler",
        """Mesane kanseri, tüm üriner sistem neoplazmları içinde en sık görülenidir (erkeklerde 4. en sık kanser). Olguların **%90'ından fazlası Ürotelyal (Transizyonel Hücreli) Karsinomdur**.

**1. Majör Epidemiyolojik Risk Faktörleri:**
• **Sigara Tüketimi:** Açık ara en önemli risk faktörüdür; mesane kanseri olgularının %50-65'inden sigara dumanındaki karsinojenik nitrozaminler ve aromatik aminler sorumludur.
• **Endüstriyel Kimyasallar (Arilaminler):** Boya, kauçuk, tekstil, plastik ve deri sanayiinde çalışan işçilerde **2-naftilamin, benzidin ve 4-aminobifenil** maruziyeti riski katlar.
• **Tıbbi Faktörler:** Siklofosfamid tedavisi, fenasetin kullanımı, pelvik radyoterapi.

**2. Saha Kanseri (Field Cancerization) Hipotezi:**
• İdrarla atılan karsinojenler böbrek pelvisinden üretraya kadar tüm üriner toplayıcı sistem mukozasını sürekli ve eşit olarak yıkar.
• Bu nedenle ürotelyumun tamamında subklinik genetik mutasyonlar (örneğin 9p ve 9q delesyonları) meydana gelir.
• **Sonuç:** Mesane tümörleri tipik olarak **multifokaldir (aynı anda birkaç odakta)** ve bir tümör rezeke edildikten sonra mesanenin başka bir yerinde veya üst üriner sistemde yeni bir tümör çıkma olasılığı (%70) son derece yüksektir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KAVRAM", "text": "Tüm ürotelyumun karsinojeneze maruz kalması 'Saha Kanseri' (Field Cancerization) olarak tanımlanır; mesane kanserlerinin yüksek multifokalite ve nüks oranını açıklar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Mesane kanserinde sigaradan sonra en klasik mesleki risk faktörü boya ve kauçuk sanayiinde kullanılan 'Arilaminler'dir (2-naftilamin).", "color": "sky"}
        ],
        {
            "id": "prac-mes-007",
            "question": "Boya ve kauçuk fabrikasında 25 yıl çalışan bir işçide mesane kanseri saptanıyor. Bu endüstriyel mesleki maruziyette ürotelyal karsinojenezden sorumlu temel kimyasal karsinojen grubu hangisidir?",
            "options": [
                "A) Asbest lifleri",
                "B) Aromatik aminler / Arilaminler (2-naftilamin, benzidin)",
                "C) Alkol türevleri",
                "D) Polisistein bileşikleri",
                "E) Ağır cıva tuzları"
            ],
            "correctAnswer": 1,
            "explanation": "Boya, kauçuk ve tekstil sanayiinde kullanılan aromatik aminler (arilaminler, özellikle 2-naftilamin) mesane karsinogenezinde klasik mesleki etkendir."
        }
    ),
    make_slide(
        8,
        "Ürotelyal Karsinomda İki Ayrı Genetik ve Morfolojik Yol",
        "Papiller Yol (FGFR3) vs Karsinoma İn Situ / İnvaziv Yol (TP53 ve RB)",
        """Ürotelyal karsinomlar tek bir hastalık olmayıp, klinik, morfolojik ve moleküler olarak birbirinden tamamen farklı iki ayrı karsinojenez yolağından gelişir.

**1. Papiller Yolak (Düşük Dereceli / Yüzeyel Yol):**
• Başlangıç lezyonu ürotelyal hiperplazi veya düşük dereceli papiller neoplazmdır.
• **Genetik Bozukluklar:** **FGFR3 (Fibroblast Büyüme Faktörü Reseptörü 3)** mutasyonu (%70-80) ve *PIK3CA* mutasyonları ile kromozom 9p/9q kayıpları. *TP53* mutasyonu içermez!
• **Morfoloji ve Klinik:** Ekzofitik, ince parmaksı papiller tümörlerdir. Lamina propriaya invaze olmazlar (Ta evresi). Rezeksiyon sonrası nüks oranları yüksektir (%70) ancak kas invazyonu ve metastaz riski çok düşüktür (%5-10).

**2. Non-Papiller / Düz Yolak (Yüksek Dereceli / İnvaziv Yol):**
• Başlangıç lezyonu düz **Karsinoma İn Situ (CIS)** veya doğrudan yüksek dereceli invaziv lezyondur.
• **Genetik Bozukluklar:** **TP53** tümör süpresör gen mutasyonu/inaktivasyonu ve **RB (Retinoblastom)** gen kaybı.
• **Morfoloji ve Klinik:** Papiller yapı oluşturmaz; düz mukoza üzerinde kadife kırmızısı plaklar yapar. Hücreler ileri derecede anaplastik ve pleomorfiktir. Hızla lamina propriayı ve **muskularis propriayı invaze eder (T2-T4)**; uzak metastaz ve mortalite riski çok yüksektir.""",
        [
            {"type": "warning", "badge": "🔴 GENETİK İKİ YOLAK", "text": "Papiller yüzeyel yol FGFR3 mutasyonuna bağlı olup nükseder ama invazyon nadirdir; Düz invaziv yol TP53 ve RB kaybına bağlı olup hızla kas invazyonu ve metastaz yapar!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Düşük dereceli papiller mesane tümörlerinde FGFR3 mutasyonu; yüksek dereceli invaziv mesane kanseri ve Karsinoma İn Situ'da (CIS) ise TP53 mutasyonu karakteristiktir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-008",
            "question": "Mesane karsinomunda düşük dereceli, non-invaziv papiller ürotelyal tümörlerin gelişiminde en sık mutasyona uğrayan onkogen aşağıdakilerden hangisidir?",
            "options": [
                "A) TP53",
                "B) FGFR3",
                "C) RB1",
                "D) VHL",
                "E) MET"
            ],
            "correctAnswer": 1,
            "explanation": "Düşük dereceli papiller ürotelyal neoplazmların yaklaşık %70'inde FGFR3 geninde aktive edici mutasyonlar saptanır."
        }
    ),
    make_slide(
        9,
        "Ürotelyal Neoplazmların WHO / ISUP Histolojik Sınıflaması",
        "Papillom, PUNLMP, Düşük Dereceli ve Yüksek Dereceli Papiller Karsinom",
        """Dünya Sağlık Örgütü ve ISUP, invaziv olmayan papiller ürotelyal lezyonları hücresel atipi ve polarite kaybı derecesine göre 4 kesin basamağa ayırmıştır.

**1. Ürotelyal Papillom:**
• Genellikle genç hastalarda tek, küçük ekzofitik lezyon. İnce fibrovasküler korları döşeyen epitel normal ürotelyumdan ayırt edilemez; nükleer atipi ve mitoz **SIFIRDIR**. Tamamen benigndir.

**2. Düşük Malign Potansiyelli Papiller Ürotelyal Neoplazm (PUNLMP):**
• Papillomdan daha kalın bir epitel tabakası vardır ancak hücreler monomorftur, polarite korunmuştur. Nükleer atipi yoktur veya minimaldir; mitoz çok nadirdir.
• Nüks edebilir ancak ilerleme (progresyon) göstermez.

**3. Düşük Dereceli Papiller Ürotelyal Karsinom:**
• Papiller mimari intaktır; hücrelerde düzenli sıralanma kısmen korunmuştur.
• Hafif-orta nükleer pleomorfizm, hafif hiperkromazi ve bazal tabakalarda tek tük mitoz izlenir. Kas invazyonu riski <%10'dur.

**4. Yüksek Dereceli Papiller Ürotelyal Karsinom:**
• Hücrelerde tam bir organizasyon ve polarite kaybı vardır.
• Nükleuslar ileri derecede pleomorfik, dev hiperkromatik ve kromatini kabalaşmıştır. Yüzey katmanları dahil tüm katlarda atipik mitotik figürler izlenir.
• Kas invazyonu riski **>%80'dir**; metastaz potansiyeli çok yüksektir.""",
        [
            {"type": "clinical", "badge": "🔴 PATOLOJİK AYRIM", "text": "PUNLMP ile düşük dereceli karsinom ayrımında mimari polarite ve hafif nükleer atipi varlığı esastır; yüksek dereceli karsinomda ise polarite tamamen çöker ve belirgin anaplazi izlenir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Yüksek dereceli papiller karsinomda nükleer pleomorfizm çok ağırdır ve kas invazyonu riski %80'in üzerindedir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-009",
            "question": "Mesane biyopsisinde papiller mimari gösteren ancak hücrelerinde belirgin polarite kaybı, dev hiperkromatik nükleuslar, nükleer pleomorfizm ve atipik mitozlar saptanan tümörün histopatolojik tanısı nedir?",
            "options": [
                "A) Ürotelyal papillom",
                "B) PUNLMP",
                "C) Düşük dereceli papiller karsinom",
                "D) Yüksek dereceli papiller ürotelyal karsinom",
                "E) İnvert papillom"
            ],
            "correctAnswer": 3,
            "explanation": "Ağır nükleer pleomorfizm, polarite kaybı ve sık mitotik figürler Yüksek Dereceli Papiller Ürotelyal Karsinomun kriterleridir."
        }
    ),
    make_slide(
        10,
        "Karsinoma İn Situ (CIS): Düz, Yüksek Dereceli Malign Lezyon",
        "Kadife Kırmızısı Mukoza, Kohezyon Kaybı, İdrar Sitolojisi ve TP53",
        """Karsinoma İn Situ (CIS), ürotelyal karsinom spektrumunun en tehlikeli, en kolay gözden kaçan ve en agresif öncül lezyonudur.

**1. Makroskobik ve Sistoskopik Özellikler:**
• CIS papiller veya ekzofitik bir kitle **OLUŞTURMAZ**.
• Sistoskopide mukoza düzeyinde sadece **hafif kızarıklık, granülarite veya 'kadife kırmızısı' (velvety red) düz plaklar** şeklinde görülür; bazen sistit ile karıştırılarak atlanabilir.
• Mesane mukozasında multifokal ve diffüz yayılma eğilimi gösterir.

**2. Mikroskobik Bulgular:**
• Bazal membran sağlamdır; lamina propriaya invazyon henüz yoktur.
• Ancak ürotelyumun tüm katmanları malign, iri, hiperkromatik, pleomorfik ve atipik mitozlar içeren **yüksek dereceli malign hücrelerle doludur**.
• **Hücresel Kohezyon Kaybı (Dökülme):** Malign hücrelerin birbirine tutunması (dezmozomlar) bozulmuştur; hücreler kolayca idrar lümenine dökülür.
• **İdrar Sitolojisinin Rolü:** Dökülen bu hücreler nedeniyle **İdrar Sitolojisi CIS tanısında %90-95 gibi olağanüstü yüksek bir duyarlılığa sahiptir!**
• Tedavi edilmediğinde %60-70 olguda hızla kas invaziv karsinoma ilerler. Birinci basamak tedavisi intravezikal **BCG** aşılamasıdır.""",
        [
            {"type": "warning", "badge": "🔴 TANI TUZAĞI", "text": "Karsinoma in situ kitle yapmaz, sistoskopide düz kadife kırmızısı görünür; ancak sitolojik olarak en yüksek dereceli malignitedir ve idrar sitolojisinde dökülen malign hücrelerle yakalanır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Mesane CIS lezyonunda hücreler kohezyonunu kaybettiği için idrar sitolojisinin sensitivitesi çok yüksektir; genetik olarak TP53 mutasyonu taşır.", "color": "sky"}
        ],
        {
            "id": "prac-mes-010",
            "question": "Sistoskopide mesane tabanında kitle oluşturmayan, düz kadife kırmızısı mukozal alanlar izlenen ve idrar sitolojisinde yoğun anaplastik malign hücreler saptanan lezyonun patolojik tanısı hangisidir?",
            "options": [
                "A) Akut bakteriyel sistit",
                "B) Ürotelyal papillom",
                "C) Düz Karsinoma İn Situ (CIS)",
                "D) Malakoplaki",
                "E) Sistitis glandülaris"
            ],
            "correctAnswer": 2,
            "explanation": "Kitle yapmayan düz kadife kırmızısı mukoza ve idrar sitolojisinde yüksek dereceli malign hücreler Karsinoma İn Situ'nun (CIS) klasik prezentasyonudur."
        }
    ),
    make_slide(
        11,
        "İnvaziv Ürotelyal Karsinom ve Muskularis Propria İnvazyonu",
        "T1 vs T2 Ayrımı: Radikal Sistektomi Kararını Belirleyen Altın Sınır",
        """Mesane kanserinde cerrahi ve onkolojik tedaviyi ikiye bölen en kritik patolojik dönüm noktası **tümörün Muskularis Propria (detrisör kas tabakasını) invaze edip etmediğidir**.

**1. T1: Lamina Propria İnvazyonu (Kas İnvaziv Olmayan):**
• Tümör bazal membranı aşmış ve epiteli destekleyen subepitelyal bağ dokusuna (**lamina propria**) invaze olmuştur.
• Ancak kalın demetler oluşturan **muskularis propria sağlamdır**.
• Bu lezyonlar Transüretral Rezeksiyon (TUR-M) ve intravezikal BCG/kemoterapi ile organ koruyucu yaklaşımla tedavi edilebilir.

**2. T2: Muskularis Propria İnvazyonu (Kas İnvaziv Karsinom):**
• Tümör hücreleri lamina propriayı aşarak kalın, organizeli detrisör düz kas demetlerinin arasına girmiştir.
• **Terapötik Karar:** T2 ve üzeri tümörlerde mesaneyi korumak imkansızdır; standart tedavi **Radikal Sistektomi** (mesane, prostat/seminal veziküller veya uterus/overlerin çıkarılması) ve lenf nodu diseksiyonudur.
• **Patoloji Raporunun 1 Numaralı Sorumluluğu:** Patolog TUR materyalinde mutlaka detrisör kas tabakasının bulunup bulunmadığını ve invaze olup olmadığını rapor etmek zorundadır!""",
        [
            {"type": "warning", "badge": "🔴 HAYATİ TEDAVİ SINIRI", "text": "Mesane kanserinde kas invazyonu (muskularis propria invazyonu - T2) radikal sistektomi kararını belirleyen en kritik prognostik sınırdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Mesane tümörü rezeksiyonunda (TUR) patoloğun kas invazyonunu değerlendirebilmesi için biyopsi örneğinde 'muskularis propria' bulunması zorunludur.", "color": "sky"}
        ],
        {
            "id": "prac-mes-011",
            "question": "Mesane kanseri tanısıyla TUR uygulanan bir hastada radikal sistektomi (mesanenin tamamen çıkarılması) endikasyonunu doğuran en kritik histopatolojik evreleme kriteri hangisidir?",
            "options": [
                "A) Şemsiye hücrelerinin kaybolması",
                "B) Lamina propriaya tümör hücrelerinin sızması (T1)",
                "C) Muskularis propria (detrisör kas tabakası) invazyonunun saptanması (T2)",
                "D) Tümör içinde psammom cisimciği bulunması",
                "E) İdrar sitolojisinde tek tük hücre görülmesi"
            ],
            "correctAnswer": 2,
            "explanation": "Tümörün muskularis propria kas tabakasını invaze etmesi (T2 - kas invaziv mesane kanseri) radikal sistektominin kesin endikasyonunu oluşturur."
        }
    ),
    make_slide(
        12,
        "Mesane Kanserinde Klinik Tablo ve İdrar Sitolojisinin Gücü",
        "Ağrısız Makroskopik Hematüri, Sitolojik Derece ve Tümör Belirteçleri",
        """Mesane kanserinin klinik semptomları ve tanı yöntemleri erken teşhis için hayati önem taşır.

**1. En Sık Başvuru Semptomu:**
• Hastaların **%80-90'ında ilk ve en sık klinik belirti Ağrısız Makroskopik Hematüridir (Painless Gross Hematuria)**. İdrar baştan sona parlak kırmızı veya pıhtılıdır; yanma veya kolik ağrı eşlik etmez.
• Karsinoma in situ olgularında veya trigona yakın tümörlerde irritatif semptomlar (dizüri, sık idrara çıkma, acil sıkışma) ön planda olabilir.

**2. İdrar Sitolojisinin Rolü:**
• İdrar sitolojisi dökülen ürotelyal hücrelerin mikroskopta incelenmesidir.
• **Yüksek Dereceli Karsinom ve CIS'te:** Duyarlılığı **%80-95** arasındadır; nükleer atipi ve kohezyon kaybı nedeniyle son derece başarılıdır.
• **Düşük Dereceli Karsinomda:** Hücreler normale çok benzediği için duyarlılığı düşüktür (%20-40).
• **Sistoskopi ve Biyopsi:** Kesin tanı ve tümör evrelemesi sistoskopi altında yapılan Transüretral Rezeksiyon (TUR-M) ile konur.""",
        [
            {"type": "clinical", "badge": "🔴 1 NUMARALI KLİNİK BULGU", "text": "50 yaş üstü bir bireyde aksi kanıtlanana kadar 'Ağrısız Makroskopik Hematüri' mesane kanseri kabul edilmeli ve derhal sistoskopi yapılmalıdır!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "İdrar sitolojisi yüksek dereceli karsinom ve CIS tanısında çok duyarlıdır; ancak düşük dereceli tümörlerde yalancı negatiflik oranı yüksektir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-012",
            "question": "60 yaşındaki bir erkekte hiçbir ağrı veya dizüri olmaksızın aniden ortaya çıkan pıhtılı makroskopik hematüride ilk şüphelenilmesi ve ekarte edilmesi gereken malignite hangisidir?",
            "options": [
                "A) Akut bakteriyel sistit",
                "B) Mesane ürotelyal karsinomu",
                "C) Benign prostat hiperplazisi",
                "D) Akut interstisyel nefrit",
                "E) Renal onkositoma"
            ],
            "correctAnswer": 1,
            "explanation": "Ağrısız makroskopik hematüri ileri yaşta mesane ürotelyal karsinomunun en tipik ve en sık görülen kardinal başvuru semptomudur."
        }
    ),
    make_slide(
        13,
        "Mesane Kanserinin Nadir Varyantları: Skuamöz Hücreli, Adenokarsinom ve Nöroendokrin",
        "Urakus Artığı (Kubbe Adenokarsinomu), Kronik Taş/Kateter ve Küçük Hücreli Karsinom",
        """Mesane malignitelerinin %90'ı ürotelyal karsinom olmakla birlikte, kalan %10'luk grup kendine has etyolojileri olan agresif varyantlardan oluşur.

**1. Skuamöz Hücreli Karsinom (SCC) (%5):**
• Batı dünyasında kronik mesane taşları, uzun süreli daimi üretral kateter kullanımı ve rekürren enfeksiyonların oluşturduğu kronik keratinize skuamöz metaplazi zemininde gelişir.
• Schistosoma haematobium endemik bölgelerinde 1 numaralı mesane kanseridir. Tipik keratin incileri ve intersellüler köprüler izlenir.

**2. Mesane Adenokarsinomu (%1-2):**
• **Urakus Kanseri (Urachal Carcinoma):** Embriyonik urakus kalıntısından (allantois kanalı) kaynaklanır. Patognomonik olarak **mesane tavanında / kubbesinde (dome)** yerleşir. Jelatinöz müsin gölleri içeren kolumnar hücreli müsinöz adenokarsinomdur.
• Non-urakal adenokarsinomlar ise mesane tabanında sistitis glandülaris veya ekstrofi vezika zemininde gelişir.

**3. Küçük Hücreli Nöroendokrin Karsinom (<%1):**
• Akciğerin küçük hücreli karsinomu ile birebir aynı morfolojidedir. Nöroendokrin belirteçler (sinaptofizin, kromogranin) pozitiftir; son derece agresiftir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK LOKALİZASYON", "text": "Mesane kubbesinde (tavanında) yerleşen müsinöz kitle embriyonik Urakus artığı kaynaklı Adenokarsinomdur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Yıllarca daimi kateter kullanan paraplejik hastada gelişen mesane kanseri tipi Skuamöz Hücreli Karsinomdur (SCC).", "color": "sky"}
        ],
        {
            "id": "prac-mes-013",
            "question": "Sistoskopide mesane tavanında (kubbesinde) yerleşim gösteren ve biyopsisinde bol müsin üreten glandüler yapılar izlenen tümörün en olası kökeni hangisidir?",
            "options": [
                "A) Urakus kalıntısı (urakal adenokarsinom)",
                "B) Von Brunn adacıkları",
                "C) Prostatik üretra",
                "D) Mezonefrik kanal artığı",
                "E) Şemsiye hücreleri"
            ],
            "correctAnswer": 0,
            "explanation": "Mesane kubbesinde (dome) yerleşen müsinöz adenokarsinomlar patent kalmış embriyonik urakus artıklarından köken alır."
        }
    ),
    make_slide(
        14,
        "Mesane Kanserinde TNM Evrelemesi",
        "Ta, TIS, T1, T2a/b, T3 ve T4 Anatomik Derinlik Basamakları",
        """Mesane ürotelyal karsinomunda prognoz ve tedavi protokolü doğrudan TNM anatomik derinlik basamaklarına göre belirlenir.

**1. Primer Tümör (T) Evreleri:**
• **Ta:** Non-invaziv papiller karsinom (tümör epitel içinde sınırlıdır, bazal membranı aşmamıştır).
• **Tis (CIS):** Karsinoma in situ (düz, yüksek dereceli non-invaziv epitel içi lezyon).
• **T1:** Tümör bazal membranı aşmış, subepitelyal bağ dokusuna (**lamina propria**) invaze olmuştur; muskularis propria intaktır.
• *(Ta, Tis ve T1 lezyonları 'Kasa İnvaze Olmayan Mesane Kanseri' grubunu oluşturur)*.
• **T2:** Tümör **Muskularis Propriayı (detrisör kası)** invaze etmiştir:
  - *T2a:* İç (yüzeyel) yarım kas invazyonu.
  - *T2b:* Dış (derin) yarım kas invazyonu.
• **T3:** Tümör kas tabakasını tamamen aşarak **perivezikal yağ dokusuna** yayılmıştır:
  - *T3a:* Mikroskopik perivezikal yağ invazyonu.
  - *T3b:* Makroskobik perivezikal kitle.
• **T4:** Tümör komşu organlara doğrudan yayılmıştır:
  - *T4a:* Prostat stroması, seminal vezikül, uterus veya vajina invazyonu.
  - *T4b:* Pelvik duvar veya karın duvarı invazyonu.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK EVRE EŞİĞİ", "text": "Ta/T1 kasa invaze olmayan mesane kanseridir (TUR + BCG); T2 ve üzeri kasa invaze mesane kanseridir (Radikal Sistektomi).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Tümörün lamina propriayı geçip ilk kez muskularis propria kas demetlerine girdiği evre T2 evresidir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-014",
            "question": "Mesane rezeksiyon materyalinde ürotelyal karsinomun detrisör kas tabakasını (muskularis propria) tamamen aşarak perivezikal yağ dokusuna mikroskopik olarak yayıldığı saptandığında T evresi nedir?",
            "options": [
                "A) T1",
                "B) T2b",
                "C) T3a",
                "D) T4a",
                "E) Tis"
            ],
            "correctAnswer": 2,
            "explanation": "Perivezikal yağ dokusuna mikroskopik yayılım T3a evresi olarak tanımlanır."
        }
    ),
    make_slide(
        15,
        "Yüzeyel Mesane Kanserinde İntravezikal BCG İmmünoterapisi",
        "Canlı Zayıflatılmış M. bovis, CD4/CD8 T Hücre Yanıtı ve Granülomatöz Enflamasyon",
        """Kasa invaze olmayan yüksek riskli yüzeyel mesane kanserlerinde (özellikle T1, yüksek dereceli Ta ve Karsinoma İn Situ - CIS) TUR-M sonrasında nüksü ve progresyonu önlemede altın standart tedavi **İntravezikal BCG (Bacillus Calmette-Guérin)** uygulamasıdır.

**1. Etki Mekanizması:**
• Canlı zayıflatılmış *Mycobacterium bovis* bakterisi sonda ile doğrudan mesane içine verilir.
• BCG basilleri ürotelyum ve tümör hücreleri tarafından endositozla yutulur.
• Masif lokal immün yanıt tetiklenir: Makrofajlar aktive olur, interferon-gama salgılanır ve mesane duvarında **CD4+ ve CD8+ sitotoksik T lenfositlerin** öncülük ettiği hücresel immünite uyarılır.
• T lenfositler kalıntı tümör hücrelerini ve CIS odaklarını lizise uğratır.

**2. Histopatolojik Yanıt ve Yan Etkiler:**
• Biyopside mesane mukozasında tipik **kazeifiye olmayan epiteloid histiyositik granülomlar** izlenir (bu beklenen terapötik bir yanıttır).
• Komplikasyon: Sistemik emilim olursa tüberküloz benzeri tablo (**BCG sepsisi** / milier yayılım); tedavide izoniazid ve rifampisin verilir.""",
        [
            {"type": "clinical", "badge": "🔴 TERAPÖTİK MEKANİZMA", "text": "İntravezikal BCG immünoterapisi mesane duvarında granülomatöz reaksiyon ve sitotoksik T hücre yanıtı oluşturarak CIS ve nüksleri yok eder.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Karsinoma in situ (CIS) ve yüksek riskli yüzeyel mesane kanserinde rezeksiyon sonrası nüksü en güçlü engelleyen lokal tedavi intravezikal BCG'dir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-015",
            "question": "Mesane Karsinoma İn Situ (CIS) tanısıyla intravezikal BCG tedavisi alan hastanın kontrol mesane biyopsisinde saptanması beklenen ve ilacın terapötik immün yanıt oluşturduğunu gösteren histopatolojik bulgu hangisidir?",
            "options": [
                "A) Michaelis-Gutmann kalsifiye cisimcikleri",
                "B) Lamina propriada kazeifiye olmayan granülomatöz enflamasyon",
                "C) Yaygın skuamöz metaplazi",
                "D) Amiloid birikimi",
                "E) Tel halka (wire-loop) lezyonları"
            ],
            "correctAnswer": 1,
            "explanation": "İntravezikal BCG canlı mikobakteri içerdiğinden mesane mukozasında granülomatöz enflamasyon ve T hücresel immün yanıt oluşturarak antitümöral etki gösterir."
        }
    ),
    make_slide(
        16,
        "Ürotelyal Karsinomda İmmünohistokimyasal Belirteç Paneli",
        "GATA3, p63, Sitokeratin 7/20 ve Üroplakin III",
        """Metastatik bir adenokarsinom veya karsinomun mesane ürotelyumu kaynaklı olup olmadığını kesinleştirmede spesifik immünohistokimyasal paneller kullanılır.

**1. Başlıca Ürotelyal Belirteçler:**
• **GATA3:** Ürotelyal diferansiasyonun **en sensitif ve en güvenilir transkripsiyon faktörü belirtecidir** (%85-90 pozitif). (Meme kanserinde de pozitiftir).
• **p63:** Ürotelyumun bazal ve ara tabakalarını kuvvetle boyar; ürotelyal kökeni destekler.
• **Sitokeratin Profili (CK7+/CK20+):** Ürotelyal karsinomlar tipik olarak **hem CK7 hem de CK20 ko-pozitifliği** gösteren nadir karsinomlardandır.
• **Üroplakin III (UPIII):** En spesifik belirteçtir (%100 özgül); ancak ileri evre dediferansiye tümörlerde sensitivitesi düşer (%50-60).

**2. CIS İmmün Profili:**
Normal ürotelyumda CK20 sadece en üstteki şemsiye hücrelerinde pozitiftir; p53 negatiftir. **Karsinoma İn Situ'da (CIS) ise CK20 ve p53 tüm epitel katmanlarında diffüz pozitif hale gelir!**""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Metastatik karsinomda ürotelyal kökeni gösteren en sensitif nükleer belirteç GATA3'tür; tipik sitokeratin profili ise CK7(+) / CK20(+)'dir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "CIS tanısında şüpheli ürotelyumda CK20'nin tüm katmanlarda diffüz boyanması ve p53 nükleer aşırı ekspresyonu malign transformasyonu kanıtlar.", "color": "sky"}
        ],
        {
            "id": "prac-mes-016",
            "question": "Karaciğerinde metastatik kitle saptanan bir hastanın biyopsisinde nükleer GATA3 pozitif, CK7 pozitif ve CK20 pozitif boyanma izleniyor. Bu metastazın en olası primer organ odağı hangisidir?",
            "options": [
                "A) Kolon adenokarsinomu",
                "B) Mesane ürotelyal karsinomu",
                "C) Prostat karsinomu",
                "D) Renal berrak hücreli karsinom",
                "E) Akciğer yassı hücreli karsinomu"
            ],
            "correctAnswer": 1,
            "explanation": "GATA3 nükleer pozitifliği ve CK7+/CK20+ sitokeratin profili Ürotelyal Karsinom için karakteristik immünohistokimyasal imzadır."
        }
    ),
    make_slide(
        17,
        "Mesane Kanserinde Metastaz Yolları ve Hedef Organlar",
        "Obturatuar/İlyak Lenf Nodları, Karaciğer, Akciğer ve Kemik",
        """Mesane ürotelyal karsinomu kas invazyonu yaptıktan sonra (T2 ve üzeri) lenfatik ve vasküler kanallar aracılığıyla hızla yayılır.

**1. Lenfatik Yayılım:**
• İlk tutulan lenf nodları perivezikal ve obturatuar lenf nodlarıdır.
• Ardından internal ilyak, eksternal ilyak ve presakral lenf nodlarına yayılır.
• Pelvik nodları aşan tümör ana ilyak ve retroperitoneal paraaortik lenf nodlarına ulaşır (N evresini belirler).

**2. Hematojen Uzak Metastaz Organları:**
• **Karaciğer (%35-40):** En sık hematojen metastaz yeridir; çoklu kitleler.
• **Akciğerler (%30):** İkincil metastaz odağı.
• **Kemikler (%25):** Genellikle osteolitik kemik metastazları; pelvis, vertebra ve femur tutulumu.
• **Kemik İliği ve Sürrenal Bezler.**

**3. Prognoz:**
Kasa invaze olmayan tümörlerde 5 yıllık sağkalım %90'ın üzerindeyken; uzak metastaz varlığında (M1) kemoterapi/immünoterapiye rağmen 5 yıllık sağkalım %10-15 seviyelerine iner.""",
        [
            {"type": "clinical", "badge": "🔴 EVRELEME KRİTİĞİ", "text": "Radikal sistektomi sırasında genişletilmiş pelvik lenf nodu diseksiyonu (obturatuar, internal/eksternal ilyak) hem evreleme hem de bölgesel kontrol için şarttır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Mesane kanserinin en sık bölgesel lenf nodu istasyonu obturatuar ve internal ilyak nodlar; en sık uzak organ metastaz yeri ise karaciğerdir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-017",
            "question": "Kas invaziv mesane ürotelyal karsinomunda bölgesel lenfatik yayılımın İLK gerçekleştiği anatomik lenf nodu istasyonu hangisidir?",
            "options": [
                "A) Paraaortik lenf nodları",
                "B) Obturatuar ve internal ilyak lenf nodları",
                "C) Yüzeyel inguinal lenf nodları",
                "D) Mediastinal lenf nodları",
                "E) Aksiller lenf nodları"
            ],
            "correctAnswer": 1,
            "explanation": "Mesane lenfatik drenajı öncelikle obturatuar, internal ve eksternal ilyak pelvik lenf nodlarına dökülür."
        }
    ),
    make_slide(
        18,
        "Üreter ve Renal Pelvis Ürotelyal Tümörleri: Üst Üriner Sistem Özellikleri",
        "Bilateralite, Balkan Nefropatisi, Obstrüksiyon ve Nefroüreterektomi Gereksinimi",
        """Ürotelyal karsinomların %5-10'u üst üriner sistemde (renal kaliksler, renal pelvis ve üreter) yerleşir.

**1. Klinik ve Patolojik Özellikler:**
• Mesane tümörlerine kıyasla çok daha erken dönemde semptom verir: Tümör üreteri tıkayarak **akut renal kolik ve hidronefroza** yol açar; pıhtılı hematüri sıktır.
• **İnce Duvar Riski:** Renal pelvis ve üreter duvarı mesaneye göre çok incedir (muskularis propria çok incedir). Bu nedenle üst üriner sistem tümörleri **çok daha erken evrede parankime ve periüreterik dokuya invaze olur!**
• **Balkan Endemik Nefropatisi ve Aristolohik Asit:** Üst üriner sistem ürotelyal karsinom riskini yüzlerce kat artırır; sıklıkla bilateral ve multifokaldir.

**2. Standart Cerrahi Tedavi:**
"Saha kanseri" nedeniyle tüm üreter güzergahında nüks riski yüksek olduğundan standart cerrahi tedavi **Radikal Nefroüreterektomi ve Mesane Kafı (Cuff) Eksizyonudur** (üreterin mesaneye girdiği delikle birlikte çıkarılması şarttır; aksi halde üreter güdüğünde tümör nükseder).""",
        [
            {"type": "warning", "badge": "🔴 CERRAHİ KURAL", "text": "Üst üriner sistem ürotelyal karsinomunda cerrahi altın standart Nefroüreterektomi + Mesane Kafı Eksizyonudur; üreter güdüğü bırakılırsa olguların %50'sinde güdükte kanser nüksü gelişir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Balkan nefropatisinde Aristolohik aside bağlı olarak renal pelvis ve üreterde bilateral ürotelyal karsinom riski olağanüstü artmıştır.", "color": "sky"}
        ],
        {
            "id": "prac-mes-018",
            "question": "Renal pelviste yüksek dereceli ürotelyal karsinom saptanan bir hastada nüksleri önlemek amacıyla uygulanması gereken standart cerrahi rezeksiyon sınırı hangisidir?",
            "options": [
                "A) Yalnızca böbreğin çıkarılması (basit nefrektomi)",
                "B) Nefroüreterektomi ve mesane kafı (cuff) rezeksiyonu",
                "C) Yalnızca tümörün lazerle yakılması",
                "D) Parsiyel nefrektomi",
                "E) Sadece üreterin çıkarılması"
            ],
            "correctAnswer": 1,
            "explanation": "Üst üriner sistem ürotelyal karsinomlarında tüm üreter boyunca nüks riskini önlemek için böbrek, tüm üreter ve mesaneye girdiği delik (kaf) birlikte çıkarılmalıdır (Radikal Nefroüreterektomi)."
        }
    ),
    make_slide(
        19,
        "Mesane Karsinomunda Güncel Moleküler Sınıflama ve Hedefe Yönelik Tedaviler",
        "Lüminal vs Bazal Tipler, FGFR İnhibitörleri (Erdafitinib) ve PD-L1 İmmünoterapisi",
        """Genomik profilleme mesane kanserinin moleküler alt tiplerini ortaya çıkarmış ve ileri evre tedaviyi tamamen değiştirmiştir.

**1. Lüminal vs Bazal-Skuamoid Alt Tipler:**
• **Lüminal Tip:** GATA3, FOXA1 ve PPAR-gama ekspresyonu; sıklıkla *FGFR3* mutasyonları taşır. Daha iyi prognoza sahiptir.
• **Bazal-Skuamoid Tip:** Sitokeratin 5/6 ve CD44 ekspresyonu; sıklıkla *TP53* ve *RB1* kaybı taşır. Çok agresiftir ancak neoadjuvan kemoterapiye daha duyarlıdır.

**2. Hedefe Yönelik ve İmmünoterapötik Ajanlar:**
• **FGFR Tirozin Kinaz İnhibitörleri:** *FGFR2/3* mutasyonu veya füzyonu taşıyan metastatik olgularda **Erdafitinib** hedefe yönelik oral tedavidir.
• **İmmün Kontrol Noktası İnhibitörleri:** Atezolizumab (anti-PD-L1), Pembrolizumab (anti-PD-1) ve Nivolumab sisplatin uygun olmayan veya dirençli olgularda standarttır.
• **Antikor-İlaç Konjugatları (ADC):** Nektin-4'ü hedefleyen **Enfortumab Vedotin**.""",
        [
            {"type": "clinical", "badge": "🔴 MOLEKÜLER ONKOLOJİ", "text": "Metastatik mesane kanserinde FGFR3 mutasyonu taşıyan olgularda oral FGFR inhibitörü Erdafitinib hedefe yönelik spesifik ajandır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 GÜNCEL TIP SPOTU", "text": "Lüminal mesane kanserleri FGFR3 mutasyonu taşırken; bazal-skuamoid tipler TP53 mutasyonu ve CK5/6 ekspresyonu gösterir.", "color": "sky"}
        ],
        {
            "id": "prac-mes-019",
            "question": "Metastatik ürotelyal karsinom tanılı bir hastanın moleküler genetik analizinde FGFR3 aktive edici gen mutasyonu saptanıyor. Bu hastaya başlanabilecek hedefe yönelik selektif FGFR inhibitörü ilaç hangisidir?",
            "options": [
                "A) Erdafitinib",
                "B) İmatinib",
                "C) Trastuzumab",
                "D) Sunitinib",
                "E) Rituksimab"
            ],
            "correctAnswer": 0,
            "explanation": "Erdafitinib, FGFR mutasyonu veya füzyonu taşıyan ileri evre/metastatik ürotelyal karsinomda onaylı selektif FGFR tirozin kinaz inhibitörüdür."
        }
    ),
    make_slide(
        20,
        "Mesane Lezyonlarında Histopatolojik Ayırıcı Tanı Atlası",
        "İnvert Papillom, Polipoid Sistit, CIS ve İnvaziv Karsinom Karşılaştırması",
        """Mesane biyopsilerinde benign hiperplastik reaksiyonlar ile karsinom ayrımı kritik incelikler barındırır.

**1. İnvert Papillom:**
• Mukozanın dışarı değil, **lamina propria içine doğru endofitik kordonlar ve anastomozlaşan adacıklar şeklinde büyümesidir**.
• Hücreler sitolojik olarak tamamen normaldir; atipi veya mitoz yoktur. Benign kabul edilir ancak rezeke edilmelidir.

**2. Polipoid Sistit:**
• Kalıcı mesane sondası veya kronik kateter basısına ikincil gelişen, ekzofitik parmaksı polipoid mukozal çıkıntılardır.
• Düşük dereceli papiller karsinomu taklit edebilir; ancak mikroskopta stromada yoğun ödem ve enflamasyon varken hücrelerde nükleer atipi bulunmaz.

**3. Radyasyon Sistiti:**
• Pelvik radyoterapiden aylar/yıllar sonra gelişir; lamina propriada atipik dev 'radyasyon fibroblastları', vasküler telenjiektaziler ve hiyalinize skleroz izlenir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK AYRIM", "text": "Daimi üretral kateter kullanan hastada sistoskopide görülen polipoid lezyonlar karsinom değil reaktif 'Polipoid Sistit'tir; stromada yoğun ödem karakteristiktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "İnvert papillom lamina propriaya doğru endofitik büyüyen benign bir lezyondur; malign invazyonla karıştırılmamalıdır.", "color": "sky"}
        ],
        {
            "id": "prac-mes-020",
            "question": "3 aydır foley mesane sondası takılı olan bir hastada kontrol sistoskopisinde mesane kubbesinde parmaksı polipoid lezyonlar izleniyor. Biyopside ödemli lamina propria üzerinde hafif hiperplastik ancak atipisiz ürotelyum saptanıyor. Tanı nedir?",
            "options": [
                "A) Yüksek dereceli papiller karsinom",
                "B) Polipoid sistit",
                "C) Malakoplaki",
                "D) Schistosoma granülomu",
                "E) Karsinoma in situ"
            ],
            "correctAnswer": 1,
            "explanation": "Kronik kateter irritasyonuna yanıt olarak gelişen atipisiz polipoid mukozal reaksiyon Polipoid Sistit olarak tanımlanır."
        }
    ),
    make_slide(
        21,
        "Mesane Kanserli Hastaya Klinik Yaklaşım ve Yönetim Algoritması",
        "Hematüri Taramasından TUR-M, BCG ve Radikal Sistektomiye Tedavi Haritası",
        """Ağrısız hematüri ile başvuran hastada kılavuzlara uygun klinik protokol:

**1. Tanı Basamakları:**
• Fizik muayene ve İdrar tahlili + İdrar sitolojisi.
• Üriner USG ve Kontrastlı Bilgisayarlı Tomografi Ürografi (BT Ürografi: üst idrar yollarını incelemek için).
• **Fleksibl Sistoskopi:** Mesane mukozasını doğrudan görerek lezyonu lokalize etmek için altın standarttır.

**2. Tedavi Basamakları:**
1. *Transüretral Rezeksiyon (TUR-M):* Tümör köküyle birlikte rezeke edilir, derin kas biyopsisi alınır.
2. *Patoloji Sonucuna Göre:*
   - **Ta / PUNLMP (Düşük Risk):** TUR-M sonrası tek doz intravezikal kemoterapi (Mitomisin C); sistoskopi ile takip.
   - **T1 / CIS / Yüksek Dereceli Ta (Yüksek Risk):** 6 haftalık indüksiyon **İntravezikal BCG** tedavisi ve idame BCG.
   - **T2 ve Üzeri (Kas İnvaziv):** Neoadjuvan sisplatin bazlı kemoterapi -> **Radikal Sistektomi + Pelvik Lenfadenektomi + Üriner Diversiyon (İleal Loop / Neobladder)**.
   - **Metastatik (M1):** Sistemik kemoterapi (Gemsitabin + Sisplatin) veya İmmünoterapi (anti-PD-1) / Erdafitinib.""",
        [
            {"type": "clinical", "badge": "🔴 TEDAVİ ALGORİTMASI", "text": "Mesane kanserinde kas invazyonu yoksa organ koruyucu TUR + intravezikal BCG; kas invazyonu varsa (T2+) altın standart Radikal Sistektomidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "T1 yüksek dereceli mesane kanserinde nüks ve kas invazyonunu engellemede en etkili kanıtlanmış tedavi intravezikal BCG instilasyonudur.", "color": "sky"}
        ],
        {
            "id": "prac-mes-021",
            "question": "Mesane tümörü nedeniyle TUR-M uygulanan ve patolojisi 'Kasa invaze olmayan lamina propriaya sınırlı yüksek dereceli ürotelyal karsinom (T1)' olarak raporlanan hastada nüks ve progresyonu önlemek için en uygun sonraki adım hangisidir?",
            "options": [
                "A) Radyoterapi vermek",
                "B) İntravezikal BCG immünoterapisi başlamak",
                "C) Acil hemodiyalize almak",
                "D) Hiçbir takip yapmamak",
                "E) Kemik iliği nakli yapmak"
            ],
            "correctAnswer": 1,
            "explanation": "T1 yüksek dereceli kasa invaze olmayan mesane kanserlerinde TUR sonrası nüks ve kas invazyonu riskini en aza indiren standart tedavi intravezikal BCG'dir."
        }
    ),
    make_slide(
        22,
        "Mesane Patolojileri Büyük Karşılaştırma Matrisi",
        "Sistit Tipleri, Papiller vs Düz Tümörler ve Histolojik Varyantlar Tablosu",
        """Mesane hastalıklarının Robbins patolojisine göre büyük karşılaştırma matrisi:

| Hastalık / Antite | Etyoloji / Zemin | Karakteristik Morfolojik Özellik | Histopatolojik İpucu | Klinik Seyir |
| :--- | :--- | :--- | :--- | :--- |
| **Akut Bakteriyel Sistit** | E. coli (%80), S. saprophyticus | Mukoza hiperemik, nötrofiller | Epitelde ödem, lökosit infiltrasyonu | Dizüri, pollaküri, lökositüri |
| **Hemorajik Sistit** | Siklofosfamid (Akrolein), Adenovirüs | Masif mukozal kanama, nekroz | Mukozal erozyon, vasküler hasar | Masif pıhtılı hematüri (MESNA) |
| **İnterstisyel Sistit** | Otoimmün / Nörojenik | **Hunner ülserleri**, mukoza fissürleri | Mesane duvarında **bol mast hücreleri** | Kronik ağrı, steril idrar |
| **Schistosomiasis** | *S. haematobium* yumurtaları | Granülomlar, kalsifiye yumurtalar | **Skuamöz metaplazi** -> **SCC riski** | Hematüri, endemik Mısır |
| **Düşük Dereceli Papiller** | Sigara, arilamin (**FGFR3**) | Ekzofitik parmaksı papiller tümör | Nükleer polarite korunmuş, hafif atipi | Nüks sık (%70), invazyon nadir |
| **Karsinoma İn Situ (CIS)** | Sigara (**TP53, RB**) | **Düz kadife kırmızısı plak** | Tüm katlarda anaplastik hücreler | **İdrar sitolojisi %95+**, BCG yanıtı |
| **Kas İnvaziv Karsinom** | De novo veya CIS ilerlemesi | Ülserovejetan sert kitle | **Muskularis propria invazyonu (T2)** | Ağrısız hematüri, **Radikal Sistektomi** |
| **Urakal Adenokarsinom** | Embriyonik urakus kalıntısı | **Mesane kubbesinde (dome)** kitle | Müsin gölleri içinde kolumnar bezler | Kötü prognoz |""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Akrolein = Hemorajik sistit; Hunner ülseri + mast hücresi = İnterstisyel sistit; Parazit yumurtası = SCC; Kubbe kitlesi = Urakal adenokarsinom.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu tablo alt idrar yolu ve mesane patolojisi komite sorularının tamamını tek bakışta çözdüren altın tablodur.", "color": "sky"}
        ],
        {
            "id": "prac-mes-022",
            "question": "Aşağıdaki mesane lezyonu ve karakteristik patolojik bulgu eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) İnterstisyel sistit — Hunner ülseri ve bol mast hücreleri",
                "B) Schistosoma haematobium — Skuamöz metaplazi ve SCC riski",
                "C) Urakus karsinomu — Mesane kubbesinde müsinöz adenokarsinom",
                "D) Düşük dereceli papiller karsinom — TP53 mutasyonu ve erken kas invazyonu",
                "E) Malakoplaki — Michaelis-Gutmann cisimcikleri"
            ],
            "correctAnswer": 3,
            "explanation": "Düşük dereceli papiller karsinomda TP53 değil FGFR3 mutasyonu görülür ve kas invazyonu nadirdir. TP53 mutasyonu ve kas invazyonu yüksek dereceli / düz yolak karsinomlarına aittir."
        }
    ),
    make_slide(
        23,
        "Hematüri Ayırıcı Tanısı ve Ürolojik vs Nefrolojik Ayrım Algoritması",
        "İdrar Rengi, Proteinüri, Silindirler ve Sistoskopi Endikasyonları",
        """Klinik pratikte hematüri ile başvuran hastada nefrolojik (glomerüler) ile ürolojik (tümör/taş) kaynak ayrımı:

| Parametre | Nefrolojik (Glomerüler) Hematüri | Ürolojik (Ekstraglomerüler) Hematüri |
| :--- | :--- | :--- |
| **İdrar Rengi** | Kahverengi, çay rengi, kola rengi | Parlak kırmızı, pembe, taze kan |
| **Pıhtı Varlığı** | **ASLA PIHTI BULUNMAZ** (tübüler ürokinaz eritir) | **Pıhtı bulunabilir** (tümör, taş kanaması) |
| **Eritrosit Morfolojisi** | **Dismorfik eritrositler** (akantositler >%5) | İzosellüler, yuvarlak, taze normal eritrositler |
| **Silindirler** | **Eritrosit silindirleri (RBC casts)** | Silindir bulunmaz |
| **Proteinüri** | Belirgin (>500 mg - masif proteinüri) | Yok veya minimal (<300 mg/gün) |
| **Klinik Tablo** | Ödem, hipertansiyon, oligüri (Nefritik) | Ağrısız kanama (Tümör) veya Renal kolik (Taş) |
| **Sonraki Adım** | Renal biyopsi, kompleman, seroloji | **Sistoskopi, Kontrastlı BT Ürografi** |""",
        [
            {"type": "clinical", "badge": "🔴 KRİTİK KLİNİK AYRIM", "text": "İdrarda pıhtı olması kanamanın glomerülden değil kesinlikle ürolojik (tümör/taş) kaynaklı olduğunu gösterir; glomerüler kanamada pıhtı asla oluşmaz!", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN ÇOK SORULAN SINAV MATRİSİ", "text": "Pıhtılı parlak kırmızı idrar = Sistoskopi / Üroloji; Kola renkli pıhtısız idrar + eritrosit silindiri = Biyopsi / Nefroloji.", "color": "sky"}
        ],
        {
            "id": "prac-mes-023",
            "question": "Aşağıdaki hematüri özelliklerinden hangisi kanamanın bir glomerülonefrite (nefrolojik) değil, kesinlikle mesane tümörü veya ürolojik bir lezyona bağlı olduğunu kanıtlar?",
            "options": [
                "A) İdrarda dismorfik akantositlerin görülmesi",
                "B) İdrar sedimentinde eritrosit silindirlerinin bulunması",
                "C) İdrarda makroskopik kan pıhtılarının (clots) saptanması",
                "D) Eşlik eden 3 g/gün proteinüri olması",
                "E) Serum C3 kompleman düzeyinin düşük olması"
            ],
            "correctAnswer": 2,
            "explanation": "Glomerüler kanamalarda tübüler ürokinaz enzimi pıhtılaşmayı engeller, bu nedenle pıhtı görülmez. Makroskopik pıhtı varlığı kanamanın kesinlikle ekstraglomerüler / ürolojik kaynaklı (tümör, taş vb.) olduğunu kanıtlar."
        }
    ),
    make_slide(
        24,
        "Ders 26-B Kapsamlı Sentezi: Mesane Hastalıkları ve Tümörlerinin Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Prof. Dr. Hikmet Keleş'in Mesane Hastalıkları ve Tümörleri dersinin en kritik sınav ve klinik özeti:

**1. Mesane Patolojisinin 10 Altın Kuralı:**
1. *Ürotelyum:* Şemsiye hücreleri ve Üroplakin plakları idrar bariyerini oluşturur; tüm toplayıcı sistem ürotelyum kaplıdır.
2. *UPJ Darlığı:* Çocukta hidronefrozun en sık konjenital nedenidir.
3. *Mesane Divertikülü:* Muskularis propria kas tabakasından yoksundur; bu nedenle içindeki kanserler hızla perivezikal dokuya (T3) invaze olur.
4. *Sistit:* E. coli en sık etken; genç kadında S. saprophyticus; sistitte ateş ve lökosit silindiri bulunmaz (varsa piyelonefrit).
5. *Hemorajik Sistit:* Siklofosfamidin Akrolein metabolitine bağlıdır; korumada MESNA verilir.
6. *İnterstisyel Sistit:* Hunner ülserleri ve mesane duvarında yoğun mast hücresi infiltrasyonu.
7. *Schistosoma haematobium:* Parazit yumurtaları, skuamöz metaplazi ve yüksek oranda Skuamöz Hücreli Karsinom (SCC).
8. *Mesane Kanserinde İki Yolak:* Papiller yol = FGFR3 mutasyonu (düşük dereceli, yüzeyel, nüks sık); Düz CIS yolu = TP53 ve RB mutasyonu (yüksek dereceli, kas invaziv).
9. *Karsinoma İn Situ (CIS):* Kitle yapmaz, düz kadife kırmızısıdır; yüksek dereceli anaplazi içerir; idrar sitolojisi %95 duyarlıdır; tedavide intravezikal BCG verilir.
10. *Klinik ve Evreleme:* En sık bulgu Ağrısız Makroskopik Hematüridir; T1 lamina propriada sınırlıdır (TUR+BCG); T2 muskularis propriayı invaze eder ve Radikal Sistektomi gerektirir.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "50 yaş üstü ağrısız pıhtılı hematüri = Mesane kanseri şüphesi -> Sistoskopi; Kas invazyonu (T2) saptandığında altın standart Radikal Sistektomidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta yer alan 10 altın kural alt idrar yolu ve mesane neoplazmları komite ve TUS sorularının tamamını çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-mes-024",
            "question": "Mesane ürotelyal karsinomlarının moleküler patogenezinde Karsinoma İn Situ (CIS) ve kas invaziv agresif karsinom gelişimi ile en güçlü ilişkili tümör süpresör gen mutasyonu hangisidir?",
            "options": [
                "A) FGFR3",
                "B) TP53",
                "C) MET",
                "D) VHL",
                "E) WT1"
            ],
            "correctAnswer": 1,
            "explanation": "TP53 (ve RB1) gen mutasyonu yüksek dereceli düz yolak, Karsinoma İn Situ ve erken kas invazyonu gösteren agresif mesane karsinomlarının temel moleküler sürücüsüdür."
        }
    )
]

print("Mesane Hastalıkları ve Tümörleri 24 slayt başarıyla tanımlandı.")

target_id = 'learn-mesane-hastaliklari-tumorleri'
for d in decks:
    if d.get('id') == target_id:
        d['title'] = "Mesane Hastalıkları ve Tümörleri Patolojisi"
        d['shortTitle'] = "Mesane Patolojisi"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Ürotelyum biyolojisi, UPJ darlığı, Retroperitoneal fibrozis, Mesane divertikülleri, Özel sistitler (Siklofosfamid/MESNA, Hunner ülserli interstisyel sistit, Schistosoma SCC ilişkisi), Ürotelyal karsinomda iki yolak (FGFR3 papiller vs TP53 düz CIS), Muskularis propria invazyonu (T1 vs T2 sistektomi) ve İntravezikal BCG immünoterapisi."
        d['slides'] = mesane_slides
        print(f"'{target_id}' güvertesi 24 yüksek kaliteli slaytla güncellendi.")
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("Mesane Hastalıkları ve Tümörleri güncellemesi tamamlandı.")
