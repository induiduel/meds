# -*- coding: utf-8 -*-
"""
Rebuild Congenital Genital Anomalies & Prenatal Diagnosis Decks with Highest Medical Quality Standards
1. learn-dogumsal-genital-anomaliler (24 Slides - Tıbbi Genetik / Embriyoloji)
2. learn-prenatal-tani (24 Slides - Tıbbi Genetik / Perinatoloji)
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
# 1. DOĞUMSAL GENİTAL GELİŞİM ANOMALİLERİ (24 SLAYT)
# ==============================================================================
anomalies_slides = [
    make_slide(
        1,
        "Cinsiyet Farklılaşmasının Temel Evreleri ve Zaman Çizelgesi",
        "Genetik, Gonadal ve Fenotipik Cinsiyetin Bipotansiyel Gelişim Basamakları",
        """İnsan embriyogenezinde cinsiyetin belirlenmesi ve farklılaşması üç temel ardışık basamakta gerçekleşir: genetik (kromozomal) cinsiyet, gonadal cinsiyet ve fenotipik (somatik) cinsiyet.

**1. Gelişimsel Basamaklar:**
• **Genetik Cinsiyet:** Fertilizasyon anında sperm hücresinin X veya Y kromozomu taşımasıyla kesinleşir (46,XX veya 46,XY).
• **Gonadal Cinsiyet:** İlk 6 hafta boyunca primitif gonadlar her iki cinste de tamamen farksızdır (bipotansiyel/indiferan gonad evresi). 7. haftadan itibaren genetik sinyaller doğrultusunda primitif gonad korteks ve medullası testis veya overe yönelir.
• **Fenotipik Cinsiyet:** Gonadlardan salgılanan spesifik hormonal sinyallere yanıt olarak iç genital kanalların (Wolff ve Müller) ve dış genital organların 9-12. haftalar arasında erkek veya kadın yönünde özelleşmesidir.

Eğer Y kromozomuna bağlı kaskad devreye girmezse iç ve dış yapılar varsayılan (default) olarak kadın fenotipine doğru evrilir.""",
        [
            {"type": "clinical", "badge": "🔴 EMBRİYOLOJİK DÖNÜM NOKTASI", "text": "Embriyonik 6. haftaya kadar gonadlar ve iç kanallar tamamen bipotansiyeldir; farklılaşma 7. haftada testiküler gen kaskadıyla başlar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Cinsiyet gelişiminde sıra: 1. Genetik cinsiyet (fertilizasyon) -> 2. Gonadal cinsiyet (7. hafta) -> 3. Fenotipik cinsiyettir (9-12. hafta).", "color": "sky"}
        ],
        {
            "id": "prac-cgb-001",
            "question": "İnsan embriyosunda bipotansiyel indiferan gonad evresinin sona erip gonadal farklılaşmanın başladığı kritik gelişim dönemi aşağıdakilerden hangisidir?",
            "options": [
                "A) Fertilizasyon anı (0. gün)",
                "B) İmplantasyon dönemi (2. hafta)",
                "C) Embriyonik 7. hafta",
                "D) Fetal 16. hafta",
                "E) Fetal 24. hafta"
            ],
            "correctAnswer": "C",
            "explanation": "Gonadlar embriyonik 6. haftanın sonuna kadar indiferandır. 7. haftada SRY geninin aktivasyonu ile testis kordları farklılaşmaya başlar."
        }
    ),
    make_slide(
        2,
        "Genetik Cinsiyet ve SRY Geninin Moleküler Rolü",
        "Yp11.3 Bölgesi, SRY Proteini ve Testis Farklılaşma Kaskadı",
        """Erkek yönünde gonadal farklılaşmayı başlatan ana genetik anahtar, Y kromozomunun kısa kolunda (Yp11.3) lokalize olan *SRY* (Sex-determining Region Y) genidir.

**1. Moleküler Etki Mekanizması:**
• *SRY*, HMG (High Mobility Group) kutusu içeren bir DNA bağlayıcı transkripsiyon faktörü kodlar.
• *SRY* proteini, indiferan gonadın destek hücre öncüllerinde *SOX9* (SRY-box 9) geninin ekspresyonunu güçlü bir şekilde uyarır.
• *SOX9*, *SF1* (Steroidogenic Factor 1) ve *WT1* (Wilms Tumor 1) ile iş birliği yaparak indiferan destek hücrelerini primitif **Sertoli hücrelerine** dönüştürür.
• Sertoli hücreleri testis kordlarını oluşturarak germ hücrelerini çevreler ve Leydig hücrelerinin farklılaşmasını indükler.

*SRY* geninin kaybı veya fonksiyon yitimi mutasyonları 46,XY gonadal disgenezisine (Swyer sendromu) yol açarken, *SRY*'nin X kromozomuna translokasyonu 46,XX erkek sendromuna sebep olur.""",
        [
            {"type": "clinical", "badge": "🔴 KRİTİK GEN KASKADI", "text": "Testis gelişiminin birincil genetik tetikleyicisi SRY olup, doğrudan hedefi SOX9 aktivasyonudur; SOX9 Sertoli hücre kimliğini belirler.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / KOMİTE SORUSU", "text": "46,XX karyotipe sahip bireyde fenotipik erkeklik saptanırsa en olası genetik mekanizma Yp üzerindeki SRY geninin X kromozomuna translokasyonudur.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-002",
            "question": "Erkek cinsiyet gelişiminde indiferan gonadda Sertoli hücrelerinin farklılaşmasını başlatan ve SRY geni tarafından doğrudan aktive edilen temel transkripsiyon faktörü hangisidir?",
            "options": [
                "A) WNT4",
                "B) SOX9",
                "C) DAX1",
                "D) FOXL2",
                "E) RSPO1"
            ],
            "correctAnswer": "B",
            "explanation": "SRY proteini doğrudan SOX9 ekspresyonunu aktive eder. SOX9, indiferan destek hücrelerinin Sertoli hücrelerine farklılaşmasını sağlayan ana yürütücüdür."
        }
    ),
    make_slide(
        3,
        "Kadın Gonadal Farklılaşması ve WNT4/RSPO1/FOXL2 Yolağı",
        "Over Gelişiminin Aktif Genetik Programı ve Testis Yolağının Baskılanması",
        """Geleneksel embriyolojide over gelişiminin 'pasif' bir süreç olduğu düşünülmekteydi. Güncel moleküler genetik kanıtlar, over gelişiminin de aktif bir genetik ağ tarafından yürütüldüğünü ve bu yolağın testis kaskadını aktif olarak baskıladığını göstermiştir.

**1. Over Farklılaşmasının Genetik Yürütücüleri:**
• **WNT4 ve RSPO1:** İndiferan gonadda *WNT4* ve *RSPO1* sinyali *beta-katenin* yolağını aktive eder. Beta-katenin, *SOX9* ekspresyonunu baskılar ve Sertoli hücresi oluşumunu engeller.
• **FOXL2:** Çatalbaş transkripsiyon faktörü olan *FOXL2*, granüloza hücrelerinin farklılaşması ve folikülogenez için zorunludur. Doğum sonrası overde bile SOX9'un susturulmasını sürdürür.
• **DAX1 (NR0B1):** X kromozomunda yer alır; dozaj hassasiyeti gösterir. Duplikasyonunda SRY'yi antagonize ederek XY bireyde dişi fenotipe (gonadal disgenezi) neden olur.

Bu genetik denge sayesinde germ hücreleri mayoz bölünmeye girer ve primitif foliküller (oosit + granüloza hücreleri) organize olur.""",
        [
            {"type": "clinical", "badge": "🔴 AKTİF GENETİK BLOKAJ", "text": "WNT4, RSPO1 ve beta-katenin yolağı SOX9'u baskılayarak testis gelişimini engeller; over oluşumu pasif değil aktif bir moleküler süreçtir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 AKADEMİK VURGU", "text": "DAX1 geninin duplikasyonu, SRY varlığına rağmen testiküler kaskadı antagonize ederek 46,XY bireyde over/streak gonad gelişimine yol açar.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-003",
            "question": "Over farklılaşmasında beta-katenin yolağını aktive ederek SOX9 ekspresyonunu baskılayan ve granüloza hücresi gelişimini destekleyen temel sinyal molekülleri hangileridir?",
            "options": [
                "A) SRY ve WT1",
                "B) WNT4 ve RSPO1",
                "C) Dihidrotestosteron ve 5-alfa redüktaz",
                "D) SF1 ve AMH",
                "E) Testosteron ve İnhibin-B"
            ],
            "correctAnswer": "B",
            "explanation": "WNT4 ve RSPO1, beta-katenin üzerinden SOX9'u baskılayarak indiferan gonadın over yönünde farklılaşmasını sağlayan kritik aktif moleküllerdir."
        }
    ),
    make_slide(
        4,
        "İç Genital Kanalların Farklılaşması: Wolff ve Müller Sistemleri",
        "Mezonefrik ve Paramezonefrik Kanalların Bipotansiyel Anatomisi ve Regülasyonu",
        """Embriyonik 7. haftada fetusun her iki tarafında iki çift genital kanal sistemi yer alır: mezonefrik (Wolff) kanalları ve paramezonefrik (Müller) kanalları.

**1. Çift Kanal Anatomisi ve Kaderi:**
• **Wolff (Mezonefrik) Kanalı:** Testosteron varlığında erkek iç genital yollarını (epididim, vaz deferens, seminal vezikül) oluşturur. Androjen yokluğunda geriler ve kadında Gartner kanalı kisti veya epooforon kalıntıları şeklinde kalır.
• **Müller (Paramezonefrik) Kanalı:** Anti-Müllerian Hormon (AMH) yokluğunda kadın iç genital organlarını (fallop tüpleri, korpus uterus, serviks ve vajina üst 1/3'ü) oluşturur. Erkekte AMH etkisiyle apoptoza uğrar; kalıntısı prostatik utrikulustur.

İç genital sistemin yönlenmesinde gonadın kendisi değil, o gonaddan salgılanan iki hormon (AMH ve Testosteron) belirleyicidir.""",
        [
            {"type": "clinical", "badge": "🔴 ÇİFT HORMON KURALI", "text": "Erkek iç genitalyasının oluşumu için İKİ hormon şarttır: Sertoli'den AMH (Müller'i yok eder) ve Leydig'den Testosteron (Wolff'u geliştirir).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Kadında mezonefrik (Wolff) kanal kalıntısına Gartner kanalı/kisti, erkekte paramezonefrik (Müller) kanal kalıntısına ise prostatik utrikulus adı verilir.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-004",
            "question": "Erkek embriyosunda paramezonefrik (Müller) kanalının gerilemesini sağlayan Anti-Müllerian Hormon (AMH) hangi hücreler tarafından salgılanır?",
            "options": [
                "A) Leydig hücreleri",
                "B) Sertoli hücreleri",
                "C) Granüloza hücreleri",
                "D) Teka hücreleri",
                "E) Prostatik stromal hücreler"
            ],
            "correctAnswer": "B",
            "explanation": "AMH (veya MIS), testiste gelişen primitif Sertoli hücreleri tarafından sentezlenir ve paramezonefrik kanalın apoptozla gerilemesini sağlar."
        }
    ),
    make_slide(
        5,
        "Anti-Müllerian Hormon (AMH) ve Persistan Müllerian Kanal Sendromu",
        "TGF-Beta Süperailesi, AMHR2 Kusurları ve PMDS Patolojisi",
        """Anti-Müllerian Hormon (AMH/MIS), TGF-beta süperailesine ait bir glikoproteindir. Paramezonefrik kanal mezenşiminde bulunan tip II serin/treonin kinaz reseptörüne (AMHR2) bağlanarak paramezonefrik kanalın 8-10. haftalarda kaspaz bağımlı apoptozla regrese olmasını sağlar.

**1. Persistan Müllerian Kanal Sendromu (PMDS):**
• **Genetik Etiyoloji:** AMH geni veya *AMHR2* reseptör genindeki otozomal resesif inaktive edici mutasyonlar.
• **Klinik Tablo:** Karyotip 46,XY'dir. Leydig hücre fonksiyonu ve testosteron sentezi normal olduğu için dış genital organlar tamamen normal erkektir; Wolff kanalı türevleri (epididim, vaz deferens) gelişmiştir.
• **Kritik Patoloji:** Müller kanalları gerileyemez; erkekte uterus ve fallop tüpleri mevcuttur. Çoğunlukla inmemiş testis (kriptorşidizm) veya fıtık kesesi içinde uterus bulunması (hernia uteri inguinalis) operasyonunda tesadüfen saptanır.""",
        [
            {"type": "clinical", "badge": "🔴 KLİNİK TUZAK", "text": "PMDS'li olgular dıştan normal erkektir; testisler skrotuma inerken uterusu da fıtık kesesine çekebilir (hernia uteri inguinalis).", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS KLASİĞİ", "text": "46,XY karyotipli, normal erkek dış genitalyasına sahip bir çocukta fıtık kesesi içinde uterus ve fallop tüpü saptanırsa tanı PMDS'dir (AMH veya AMHR2 defekti).", "color": "sky"}
        ],
        {
            "id": "prac-cgb-005",
            "question": "İnguinal herni onarımı sırasında fıtık kesesi içinde fallop tüpü ve rudimenter uterus saptanan, dış genitalyası tamamen normal virilize erkek olan 5 yaşındaki hastada en olası defekt hangisidir?",
            "options": [
                "A) 5-alfa redüktaz eksikliği",
                "B) Androjen reseptör mutasyonu",
                "C) Anti-Müllerian Hormon (AMH) veya reseptör mutasyonu",
                "D) 21-hidroksilaz eksikliği",
                "E) SRY gen delesyonu"
            ],
            "correctAnswer": "C",
            "explanation": "Normal erkek dış genitalyası + uterus/tüp varlığı Persistan Müllerian Kanal Sendromu'nu (PMDS) işaret eder; mekanizma AMH sentez veya reseptör kusurudur."
        }
    ),
    make_slide(
        6,
        "Testosteron ve Wolff Kanalı Türevlerinin Farklılaşması",
        "Leydig Hücreleri, Parakrin Etki Mekanizması ve Anatomik Türevler",
        """Testis kordları oluştuktan sonra, 8. haftada interstisyel mezenşimden gelişen Leydig hücreleri fetal hCG ve ardından hipofizer LH uyarısıyla yoğun testosteron sentezine başlar.

**1. Wolff Kanalının Farklılaşma Dinamikleri:**
• **Lokal Yüksek Konsantrasyon İhtiyacı:** Testosteron, ipsilateral Wolff kanalını parakrin (lokal difüzyon) yolla uyarır. Bu nedenle tek taraflı gonad disgenezi veya agenezisinde, sadece testisin bulunduğu taraftaki Wolff kanalı gelişir.
• **Wolff Kanalından Gelişen Yapılar:**
  - Epididim başı, gövdesi ve kuyruğu
  - Duktus (vaz) deferens
  - Seminal veziküller
  - Ejakülatör kanallar
• **Testosteronun Doğrudan Etkisi:** Bu yapılar 5-alfa redüktaz dönüşümüne ihtiyaç duymadan, doğrudan **testosteronun kendisi** tarafından uyarılır. Prostat ise dihidrotestosteron (DHT) bağımlıdır.""",
        [
            {"type": "clinical", "badge": "🔴 PARAKRİN ETKİ PRENSİBİ", "text": "Wolff kanalının gelişimi için testosteronun dolaşımdaki seviyesi değil, testisten lokal dokuya difüze olan parakrin yüksek konsantrasyonu gereklidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ KOMİTE SORUSU", "text": "Epididim, vaz deferens ve seminal vezikül doğrudan TESTOSTERON ile gelişirken; prostat, skrotum ve penis DİHİDROTESTOSTERON (DHT) bağımlıdır.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-006",
            "question": "Aşağıdaki anatomik yapılardan hangisinin embriyolojik gelişimi dihidrotestosterondan ziyade doğrudan testosteronun parakrin etkisiyle mezonefrik kanaldan farklılaşır?",
            "options": [
                "A) Prostat bezi",
                "B) Skrotum",
                "C) Seminal vezikül",
                "D) Penil üretra",
                "E) Glans penis"
            ],
            "correctAnswer": "C",
            "explanation": "Seminal vezikül, vaz deferens ve epididim mezonefrik (Wolff) kanal türevi olup doğrudan testosteron uyarısıyla gelişir. Prostat ve dış genitalya DHT bağımlıdır."
        }
    ),
    make_slide(
        7,
        "Dihidrotestosteron (DHT) ve Dış Genitalya Maskülinizasyonu",
        "5-Alfa Redüktaz Tip 2, Genital Tüberkül, Ürogenital Sinüs ve Katlantılar",
        """Erkek dış genital organlarının maskülinizasyonu için testosteronun hedef dokularda çok daha güçlü bir androjen olan dihidrotestosterona (DHT) dönüşmesi şarttır.

**1. 5-Alfa Redüktaz Tip 2 ve Doku Dönüşümü:**
• *SRD5A2* geni tarafından kodlanan 5-alfa redüktaz tip 2 enzimi, hedef dokularda testosteronu DHT'ye indirger. DHT androjen reseptörüne testosterondan katbekat yüksek afiniteyle bağlanır.
• **Genital Tüberkül:** DHT etkisiyle uzar ve fallus/glans penisi oluşturur (kadında klitoris).
• **Ürogenital Katlantılar (Urogenital folds):** Ventral hatta birleşerek penil (spongiyöz) üretrayı ve ventral penil cildi oluşturur (kadında labia minora).
• **Labioskrotal Şişlikler (Labioscrotal swellings):** Orta hatta füzyona uğrayarak skrotumu meydana getirir (kadında labia majora).
• **Ürogenital Sinüs:** Prostat ve bulbouretral bezleri meydana getirir.""",
        [
            {"type": "clinical", "badge": "🔴 ANATOMİK KARŞILIKLAR", "text": "Genital tüberkül -> Glans penis/klitoris; Ürogenital katlantı -> Penil üretra/labia minora; Labioskrotal şişlik -> Skrotum/labia majora.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS VE DUS VURGUSU", "text": "Penil üretranın ventralde birleşme kusuru HİPOSPADİAS ile sonuçlanır; bu süreç 5-alfa redüktaz veya androjen reseptör yetersizliklerinde bozulur.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-007",
            "question": "Erkek embriyosunda skrotumun geliştiği indiferan dış genital taslak aşağıdakilerden hangisidir?",
            "options": [
                "A) Genital tüberkül",
                "B) Ürogenital katlantılar",
                "C) Labioskrotal şişlikler",
                "D) Sinovajinal yumrular",
                "E) Paramezonefrik kanal"
            ],
            "correctAnswer": "C",
            "explanation": "Labioskrotal şişlikler erkekte orta hatta birleşerek skrotumu, kadında ise birleşmeyerek labia majoraları oluşturur."
        }
    ),
    make_slide(
        8,
        "Kadın Dış Genitalya ve Müller Kanal Türevleri",
        "Androjen Yokluğunda Dişi Fenotipin İnşası ve Vajina Embriyolojisi",
        """Kadın fetusta testosteron ve AMH salgılanmadığı için gelişim varsayılan dişi anatomisi yönünde ilerler.

**1. Müller Kanalı Türevleri ve Füzyon:**
• Sağ ve sol paramezonefrik kanalların kranyal parçaları açık kalarak **fallop tüplerini (tuba uterina)** oluşturur.
• Kaudal parçaları orta hatta birbiriyle kaynaşarak tek bir uterovajinal kanal meydana getirir; bundan **korpus uterus**, **serviks** ve **vajinanın üst 1/3'lük bölümü** gelişir.
• İki kanalın birleşme hattındaki dokunun rezorbe olmasıyla tek lümenli kavum uteri açığa çıkar (rezorbsiyon kusurunda uterin septum oluşur).

**2. Vajinanın İkili Embriyolojik Kökeni:**
• Üst 1/3 kısım: Paramezonefrik (Müller) kanallarının kaudal füzyonu (mezoderm).
• Alt 2/3 kısım: Ürogenital sinüsten kaynaklanan sinovajinal yumruların kanalize olması (endoderm). Bu iki köken himen zarında buluşur.""",
        [
            {"type": "clinical", "badge": "🔴 İKİLİ KÖKEN KURALI", "text": "Vajina çift kökenlidir: Üst 1/3 Müller kaynaklı (mezoderm), alt 2/3 ürogenital sinüs kaynaklıdır (endoderm).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Uterus bikornis kanal füzyon kusurundan, uterus septus ise birleşen kanallar arasındaki septumun rezorbe olamamasından kaynaklanır.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-008",
            "question": "Vajinanın embriyolojik gelişimi ile ilgili olarak alt 2/3'lük kısmın köken aldığı yapı aşağıdakilerden hangisidir?",
            "options": [
                "A) Mezonefrik (Wolff) kanalı",
                "B) Paramezonefrik (Müller) kanalı",
                "C) Ürogenital sinüs (sinovajinal yumrular)",
                "D) Genital tüberkül",
                "E) Alantois kalıntısı"
            ],
            "correctAnswer": "C",
            "explanation": "Vajinanın üst 1/3'ü Müller kanallarından, alt 2/3'ü ise ürogenital sinüsten gelişen sinovajinal yumruların kanalize olmasıyla meydana gelir."
        }
    ),
    make_slide(
        9,
        "Cinsiyet Gelişim Bozuklukları (CGB / DSD) Güncel Chicago Sınıflaması",
        "Terminoloji Değişimi: İnterseks ve Hermafroditizm Yerine Modern Konsensus",
        """2006 Chicago Konsensus Toplantısı ile 'hermafroditizm', 'psödohermafroditizm' ve 'interseks' terimleri terk edilmiş; hastayı ve aileyi etiketlemeyen 'Cinsiyet Gelişim Bozuklukları' (Disorders of Sex Development - DSD) sınıflaması benimsenmiştir.

**1. Chicago Konsensusu Temel Kategorileri:**
• **1. Kromozomal CGB (Sex Chromosome DSD):** Karyotipik anöploidiler veya mozaisizmler.
  - Turner sendromu (45,X ve varyantları)
  - Klinefelter sendromu (47,XXY ve varyantları)
  - Mikst Gonadal Disgenezi (45,X/46,XY mozaisizmi)
  - Ovotestiküler CGB (kimerizm/mozaisizm)
• **2. 46,XY CGB (Eski Erkek Psödohermafroditizm):** Testis gelişimi bozuklukları, androjen sentez veya etki defektleri (CAIS, PAIS, 5-ARD).
• **3. 46,XX CGB (Eski Kadın Psödohermafroditizm):** Fetal/maternal aşırı androjen maruziyeti; en sık neden Konjenital Adrenal Hiperplazi (KAH).""",
        [
            {"type": "clinical", "badge": "🔴 MODERN TERMİNOLOJİ", "text": "Klinik pratikte 'hermafrodit' yerine karyotip tabanlı CGB (DSD) sınıflaması kullanılır: Kromozomal, 46,XY ve 46,XX CGB.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK CGB NEDENİ", "text": "Yenidoğanda ambigius genitalyanın ve 46,XX CGB grubunun açık ara en sık nedeni Konjenital Adrenal Hiperplazi'dir (21-OH eksikliği).", "color": "sky"}
        ],
        {
            "id": "prac-cgb-009",
            "question": "Chicago Konsensus sınıflamasına göre yenidoğanda saptanan ambigius genitalya olgularında 46,XX Cinsiyet Gelişim Bozukluğunun en sık görülen nedeni hangisidir?",
            "options": [
                "A) Tam androjen duyarsızlığı",
                "B) Konjenital adrenal hiperplazi (21-hidroksilaz eksikliği)",
                "C) 5-alfa redüktaz tip 2 eksikliği",
                "D) Turner sendromu",
                "E) Swyer sendromu"
            ],
            "correctAnswer": "B",
            "explanation": "46,XX CGB'nin en sık nedeni (%90+) fetal adrenal bezden aşırı androjen üretimine yol açan Konjenital Adrenal Hiperplazidir (özellikle 21-OH eksikliği)."
        }
    ),
    make_slide(
        10,
        "Turner Sendromu (45,X) ve Gonadal Disgenezi",
        "SHOX Geni, Fibröz Streak Gonadlar, Kardiyovasküler ve Somatik Bulgular",
        """Turner sendromu, dişi fenotipinde bir X kromozomunun tamamen veya kısmen yokluğu ile karakterize, en sık görülen seks kromozomu anöploidisidir (~1/2500 canlı kız doğum).

**1. Patogenez ve Gonadal Patoloji:**
• En sık karyotip 45,X'tir (%50); %30-40 mozaisizm (45,X/46,XX) veya izokromozom Xq [46,X,i(Xq)] görülür.
• İntrauterin 12-16. haftaya kadar oosit sayısı normaldir; ancak ikinci trimesterden itibaren hızlanmış oosit atrezisi gerçekleşir.
• Doğumda overler fibröz bir bağ dokusu bandına dönüşmüştür (**streak gonad / çizgi gonad**).
• Folikül kalmadığı için östrojen ve inhibin üretilemez; hipofizden negatif feed-back kaybıyla **FSH ve LH aşırı yükselir (hipergonadotropik hipogonadizm)**.

**2. Klinik Bulgular:**
• Kısa boy (Xp üzerindeki *SHOX* geninin tek kopya kalması).
• Yele boyun (kistik higroma kalıntısı - pterygium colli), düşük saç çizgisi, kalkık tırnaklar, kubitus valgus, kalkan göğüs ve meme uçları arası mesafe artışı.
• Aort koarktasyonu ve biküspit aort kapağı (%30).""",
        [
            {"type": "clinical", "badge": "🔴 KARDİYOLOJİK RİSK", "text": "Turner sendromlu her hastada aort koarktasyonu ve biküspit aort kapağı taranmalıdır; aort diseksiyonu riski yüksektir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Primer amenore ve boy kısalığı ile başvuran hastada yüksek FSH/LH ve streak gonadlar saptanırsa ilk düşünülmesi gereken tanı Turner sendromudur.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-010",
            "question": "Primer amenore, boy kısalığı, yele boyun ve kalkan göğüs deformitesi olan 16 yaşındaki kız hastanın ekokardiyografisinde en sık saptanması beklenen konjenital kardiyak anomali hangisidir?",
            "options": [
                "A) Ventriküler septal defekt",
                "B) Biküspit aort kapağı ve aort koarktasyonu",
                "C) Fallot tetralojisi",
                "D) Büyük arter transpozisyonu",
                "E) Ebstein anomalisi"
            ],
            "correctAnswer": "B",
            "explanation": "Turner sendromunda (45,X) en sık eşlik eden sol kalp ve vasküler anomaliler biküspit aort kapağı ve aort koarktasyonudur."
        }
    ),
    make_slide(
        11,
        "Klinefelter Sendromu (47,XXY) ve Testiküler Disgenezi",
        "Seminifer Tübül Hiyalinizasyonu, Hipergonadotropik Hipogonadizm ve Jinekomasti",
        """Klinefelter sendromu, fazladan en az bir X kromozomunun varlığı ile seyreden, erkek hipogonadizminin ve genetik infertilitesinin en sık nedenidir (~1/600 canlı erkek doğum).

**1. Genetik ve Histopatolojik Temel:**
• En sık karyotip 47,XXY'dir (%80-90); maternal veya paternal mayotik ayrılamama (nondisjunction) sonucu oluşur.
• Puberte döneminde seminifer tübüllerde ilerleyici fibrozis ve hiyalinizasyon başlar; Sertoli hücreleri ve germ hücreleri harap olur (**azospermi**).
• Leydig hücreleri atrofik tübüller arasında psödohiperplazi gösterir ancak steroidojenik kapasiteleri düşüktür; testosteron üretimi yetersizdir.
• İnhibin-B ve testosteron eksikliği nedeniyle **FSH ve LH belirgin yüksektir**.

**2. Klinik Tablo:**
• Uzun boy ve orantısız uzun ekstremiteler (östrojen azlığına bağlı epifiz hatlarının geç kapanması).
• Küçük, sert testisler (genellikle <4 ml) ve mikropenis.
• Jinekomasti (östrojen/androjen oranı artışına bağlı; meme kanseri riski 20-50 kat artmıştır).
• Azalmış sakal/vücut kılı, kadın tipi pubik kıllanma, osteoporoz ve hafif öğrenme güçlükleri.""",
        [
            {"type": "clinical", "badge": "🔴 ONKOLOJİK DİKKAT", "text": "Klinefelter sendromlu erkeklerde artmış östrojen/androjen oranı nedeniyle erkek meme karsinomu riski dramatik şekilde yükselmiştir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / DUS SORUSU", "text": "Küçük sert testisler, jinekomasti, azospermi, uzun boy ve yüksek gonadotropinler (FSH/LH) ile başvuran hastada tanı Klinefelter (47,XXY) sendromudur.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-011",
            "question": "İnfertilite şikayetiyle başvuran, muayenesinde bilateral 2 ml sert testisler, belirgin jinekomasti, uzun boy ve kollar saptanan 26 yaşındaki hastanın hormon profilinde ve karyotipinde ne beklenir?",
            "options": [
                "A) Düşük FSH/LH, normal testosteron - 46,XY",
                "B) Yüksek FSH/LH, düşük testosteron - 47,XXY",
                "C) Yüksek FSH, normal testosteron - 45,X",
                "D) Düşük FSH/LH, yüksek testosteron - 47,XYY",
                "E) Normal hormonlar - 46,XY"
            ],
            "correctAnswer": "B",
            "explanation": "Küçük sert testisler, jinekomasti ve azospermi ile seyreden Klinefelter sendromunda (47,XXY) tübüler hasar nedeniyle primer hipogonadizm (yüksek FSH/LH, düşük T) gelişir."
        }
    ),
    make_slide(
        12,
        "Saf Gonadal Disgenezi: Swyer Sendromu (46,XY)",
        "SRY İnaktivasyonu, Normal Dişi İç/Dış Genitalyası ve Malignite Riski",
        """Swyer sendromu (46,XY Saf Gonadal Disgenezi), Y kromozomu taşımasına rağmen testiküler gelişimin embriyonik evrede tamamen başarısız olduğu nadir bir tablodur.

**1. Etyopatogenez ve Mekanizma:**
• Vakaların %15-20'sinde *SRY* geninde mutasyon veya delesyon saptanır; diğer olgularda *MAP3K1*, *SOX9*, *NR5A1 (SF1)* veya *DHH* mutasyonları rol oynar.
• Testis oluşamadığı için Sertoli ve Leydig hücreleri yoktur; dolayısıyla **ne AMH ne de Testosteron üretilebilir**.
• AMH olmadığı için Müller kanalları gerileyemez: Normal tuba uterina, uterus ve serviks gelişir.
• Testosteron ve DHT olmadığı için Wolff kanalları geriler ve dış genitalya tamamen normal kadın fenotipinde şekillenir.

**2. Klinik Özellikler ve Yönetim:**
• Normal boyda, normal kadın dış genitalyasına sahip ergen kız primer amenore ve meme gelişiminin olmaması (hipoöstrojenizm) ile başvurur.
• Ultrasonografide hipoplazik uterus ve bilateral fibröz streak gonadlar izlenir.
• **Malignite Riski:** Y kromozomu materyali taşıyan streak gonadlarda **gonadoblastoma** ve **disgerminom** gelişme riski %20-30 civarındadır. Tanı anında profilaktik **bilateral gonadektomi** uygulanmalıdır.""",
        [
            {"type": "clinical", "badge": "🔴 ACİL CERRAHİ ENDİKASYON", "text": "Y kromozomu taşıyan streak gonadlarda gonadoblastoma/disgerminom riski çok yüksektir; tanı konur konmaz bilateral gonadektomi yapılmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS AYIRICI TANISI", "text": "46,XY karyotipli bir hastada UTERUS VARSA Swyer sendromudur; UTERUS YOKSA Androjen Duyarsızlığı Sendromudur (CAIS).", "color": "sky"}
        ],
        {
            "id": "prac-cgb-012",
            "question": "17 yaşında primer amenore ve sekonder cinsiyet karakterlerinin gelişmemesi nedeniyle araştırılan, karyotipi 46,XY olan, pelvik USG'de hipoplazik uterus ve bilateral streak gonadlar saptanan hastada en kritik yaklaşım hangisidir?",
            "options": [
                "A) Testosteron replasmanı",
                "B) Gonadoblastoma riski nedeniyle acil bilateral gonadektomi",
                "C) Hidrokortizon infüzyonu",
                "D) GnRH pompası tedavisi",
                "E) Histerektomi yapılması"
            ],
            "correctAnswer": "B",
            "explanation": "46,XY saf gonadal disgenezide (Swyer sendromu) intraabdominal Y kromozomu taşıyan disgenezik gonadlarda malignite riski çok yüksek olduğundan derhal gonadektomi önerilir."
        }
    ),
    make_slide(
        13,
        "46,XX Saf Gonadal Disgenezi",
        "Normal Karyotip, Normal Boy, Çizgi Overler ve Hipergonadotropik Hipogonadizm",
        """46,XX Saf Gonadal Disgenezi, normal dişi karyotipine sahip bireylerde overlerin embriyonik veya erken fetal dönemde gelişemeyerek fibröz streak dokuya dönüşmesi tablosudur.

**1. Etiyopatogenez ve Genetik:**
• Çoğunlukla otozomal resesif geçişlidir; FSH reseptör (*FSHR*), *LHCGR*, *BMP15* veya *FOXL2* mutasyonları suçlanmıştır.
• Perrault Sendromu: 46,XX gonadal disgeneziye sensörinöral işitme kaybının eşlik ettiği otozomal resesif klinik varyanttır.

**2. Turner Sendromundan Kritik Ayırıcı Tanı:**
• Karyotip 46,XX'tir (Turner'da 45,X).
• Boy uzunluğu normaldir; çünkü boy kısalığından sorumlu *SHOX* geni (Xp22.33) iki aktif kopyaya sahiptir (Turner'da tek kopyadır).
• Turner sendromunun somatik stigmaları (yele boyun, aort koarktasyonu, kalkan göğüs) kesinlikle bulunmaz.
• Müllerian organlar (uterus, tubalar, vajina) tamamen normaldir ancak östrojen eksikliğine bağlı infantil kalır.
• Tedavide siklik östrojen-progesteron replasmanı verilerek meme gelişimi ve uterus büyümesi sağlanır; fertilite donör oosit ile mümkündür.""",
        [
            {"type": "clinical", "badge": "🔴 BOY VE SHOX AYRIMI", "text": "46,XX gonadal disgenezili hastaların boyu tamamen normaldir; çünkü iki adet X kromozomuna bağlı çift doz SHOX geni eksprese edilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KLİNİK AYIRICI TANI", "text": "Primer amenore + normal boy + streak gonad + normal uterus + somatik stigmaların yokluğu = 46,XX Saf Gonadal Disgenezi.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-013",
            "question": "16 yaşında primer amenore ve meme gelişim geriliği ile getirilen, boyu 50. persentilde olan, Turner sendromu somatik stigmaları taşımayan, USG'de infantil uterus ve streak gonadlar saptanan hastada en olası durum hangisidir?",
            "options": [
                "A) Turner sendromu (45,X)",
                "B) 46,XX Saf Gonadal Disgenezi",
                "C) Tam androjen duyarsızlığı sendromu",
                "D) Mayer-Rokitansky-Küster-Hauser sendromu",
                "E) Konjenital adrenal hiperplazi"
            ],
            "correctAnswer": "B",
            "explanation": "Normal boy, somatik stigma yokluğu, streak overler ve infantil uterus birlikteliği tipik olarak 46,XX Saf Gonadal Disgenezi tablosudur."
        }
    ),
    make_slide(
        14,
        "46,XX Cinsiyet Gelişim Bozukluğu ve Konjenital Adrenal Hiperplazi",
        "21-Hidroksilaz Eksikliği, Steroid Biyosentezi ve Virilizasyon Mekanizması",
        """Konjenital Adrenal Hiperplazi (KAH), adrenal kortekste kortizol biyosentezinde görevli enzimlerin otozomal resesif kalıtılan eksikliği sonucu gelişen ve 46,XX bireylerde ambigius genitalyanın en sık nedenini oluşturan hastalıktır.

**1. 21-Hidroksilaz Eksikliği Mekanizması:**
• Olguların %90-95'inden *CYP21A2* gen mutasyonlarına bağlı **21-hidroksilaz eksikliği** sorumludur.
• 21-hidroksilaz, progesteronu 11-deoksikortikosterona (aldosteron yolu) ve 17-OH progesteronu 11-deoksikortizole (kortizol yolu) dönüştürür.
• Enzim blokajı nedeniyle kortizol üretilemez -> hipofizden negatif feed-back kalkar -> **ACTH aşırı derecede yükselir**.
• Aşırı ACTH adrenal korteksi hiperplaziye uğratır ve biriken prekürsörler (özellikle 17-hidroksiprogesteron) bloke olmayan **androjen yolağına (DHEA, androstenedion, testosteron)** kayar.

**2. Fetal Etkiler:**
• 46,XX dişi fetusta overler ve Müllerian yapılar (uterus, tüpler, vajina üstü) tamamen normaldir (AMH yoktur).
• Ancak adrenalden salgılanan yüksek androjenler dış genitalyayı virilize eder: Klitoromegali, ürogenital sinüs açıklığı ve labioskrotal füzyon gelişir.""",
        [
            {"type": "clinical", "badge": "🔴 PATOGNOMONİK BİYOKİMYA", "text": "21-hidroksilaz eksikliğinde plazmada 17-hidroksiprogesteron (17-OHP) aşırı yükselir; yenidoğan tarama testinin temel belirtecidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "KAH'lı 46,XX bebekte iç genital organlar (uterus ve tubalar) tamamen normal dişidir; çünkü fetal overler AMH üretmez!", "color": "sky"}
        ],
        {
            "id": "prac-cgb-014",
            "question": "Konjenital adrenal hiperplazili (21-hidroksilaz eksikliği) 46,XX karyotipli bir yenidoğanın iç genital organları ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Müller kanalları gerilemiştir, uterus bulunmaz.",
                "B) Epididim ve vaz deferens gelişmiştir.",
                "C) Uterus, fallop tüpleri ve overler tamamen normaldir.",
                "D) Bilateral streak gonadlar ve rudimenter kordonlar mevcuttur.",
                "E) Prostat bezi ve seminal veziküller mevcuttur."
            ],
            "correctAnswer": "C",
            "explanation": "KAH'da testis dokusu olmadığı için AMH sentezlenmez; bu nedenle Müller kanalları normal dişi yönünde gelişir (uterus, tüpler ve overler mevcuttur)."
        }
    ),
    make_slide(
        15,
        "KAH'da Klinik Tipler: Tuz Kaybettiren, Basit Virilizan ve Non-Klasik",
        "Tuz Kaybı Krizi, Elektrolit Bozuklukları ve Acil Hayat Kurtarıcı Tedavi",
        """21-hidroksilaz eksikliğinde klinik tablo, rezidüel enzim aktivitesinin derecesine bağlı olarak üç ana formda karşımıza çıkar.

**1. Klasik Tuz Kaybettiren Form (%75):**
• Enzim aktivitesi <%1'dir. Hem kortizol hem de aldosteron sentezi tamamen çöker.
• Doğumdan sonraki 1-3. haftalarda: Kusma, kilo kaybı, dehidratasyon, hipotansiyon ve hipovolemik şok tablosu gelişir.
• **Tipik Laboratuvar:** **Hiponatremi, Hiperkalemi, Metabolik Asidoz ve Hipoglisemi**.
• Erkek bebeklerde dış genitalya normal olduğu için tanı gecikebilir ve kriz ölümcül olabilir! Kız bebeklerde ambigius genitalya erken tanı sağlar.

**2. Basit Virilizan Form (%25):**
• Enzim aktivitesi %1-2 civarındadır; aldosteron üretimi tuz kaybını önlemeye yeterlidir.
• Kızlarda doğumda ambigius genitalya; erkeklerde ise erken çocuklukta izoseksüel yalancı erken puberte (penis büyümesi, pubik kıllanma, hızlı boy uzaması ama küçük testisler).

**3. Non-Klasik (Geç Başlayan) Form:**
• Enzim aktivitesi %20-50'dir. Doğumda genital anomali yoktur; adölesanda hirsutizm, oligomenore ve akne (PCOS benzeri) ile prezante olur.""",
        [
            {"type": "clinical", "badge": "🔴 ACİL KRİTİK TABLO", "text": "Yenidoğan döneminde açıklanamayan kusma, dehidratasyon, HİPONATREMİ ve HİPERKALEMİ saptandığında aksi kanıtlanana kadar KAH tuz kaybı krizi düşünülmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS VE YANDAL SORUSU", "text": "Tuz kaybettiren KAH krizinin acil medikal tedavisi: İntravenöz izotonik sıvı + glikoz + parenteral hidrokortizon ve mineralokortikoid (fludrokortizon) replasmanıdır.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-015",
            "question": "Doğumdan sonraki 12. günde emmede azalma, fışkırır tarzda kusma ve halsizlik ile getirilen erkek bebeğin serum sodyumu 118 mEq/L, potasyumu 7.2 mEq/L ve kan şekeri 45 mg/dL bulunuyor. En olası tanı hangisidir?",
            "options": [
                "A) İnfantil hipertrofik pilor stenozu",
                "B) Klasik tuz kaybettiren konjenital adrenal hiperplazi",
                "C) Hirschsprung hastalığı",
                "D) Nekrotizan enterokolit",
                "E) Malrotasyon ve volvulus"
            ],
            "correctAnswer": "B",
            "explanation": "Pilor stenozunda hipokalemik hipokloremik alkaloz beklenirken; KAH tuz kaybında hiponatremi, hiperkalemi, asidoz ve hipoglisemi görülür."
        }
    ),
    make_slide(
        16,
        "46,XY Cinsiyet Gelişim Bozuklukları ve Androjen Sentez Kusurları",
        "Leydig Hücre Hipoplazisi, 17-Beta HSD Eksikliği ve 17-Alfa Hidroksilaz Yetmezliği",
        """46,XY genetik yapısına sahip bir bireyde yetersiz virilizasyon (ambigius veya dişi dış genitalya), testosteron biyosentezindeki defektlerden kaynaklanabilir.

**1. Leydig Hücre Hipoplazisi (LHCGR Mutasyonu):**
• LH/hCG reseptör genindeki inaktive edici mutasyonlar nedeniyle fetal Leydig hücreleri uyarılamaz ve gelişemez.
• Sertoli hücreleri normal olduğu için **AMH salgılanır ve Müller kanalları geriler (uterus yoktur)**.
• Testosteron sentezlenemediği için Wolff kanalları gelişemez ve dış genitalya tamamen dişi yönünde kalır.

**2. 17-Beta Hidroksisteroid Dehidrogenaz Tip 3 (17β-HSD3) Eksikliği:**
• Androstenedionun testosterona dönüşümünü katalizler.
• Testosteron düşüktür; plazmada **Androstenedion / Testosteron oranı belirgin artmıştır**.
• Doğumda dişi veya hafif virilize dış genitalya; pubertede periferik enzimlerle (17β-HSD tip 1) testosteron üretimiyle belirgin virilizasyon ve klitoromegali gelişir.

**3. 17-Alfa Hidroksilaz (CYP17A1) Eksikliği:**
• Hem kortizol hem seks steroidi sentezi durur. Mineralokortikoid prekürsörü kortikosteron artar: **Hipertansiyon ve hipokalemi** ile birlikte dişi dış genitalyası izlenir.""",
        [
            {"type": "clinical", "badge": "🔴 HİPERTANSİYON İPUCU", "text": "46,XY ambigius veya dişi genitalyaya eşlik eden HİPERTANSİYON ve HİPOKALEMİ saptandığında 17-alfa hidroksilaz eksikliği akla gelmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ KOMİTE SORUSU", "text": "17-beta HSD3 eksikliğinde karakteristik tanısal laboratuvar bulgusu androstenedion/testosteron oranının belirgin yükselmesidir.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-016",
            "question": "46,XY karyotipli bir olguda uterus ve tubaların bulunmadığı, ancak dış genitalyanın tamamen dişi fenotipinde olduğu ve plazmada androstenedion/testosteron oranının yüksek bulunduğu durum hangisidir?",
            "options": [
                "A) 21-hidroksilaz eksikliği",
                "B) 17-beta hidroksisteroid dehidrogenaz tip 3 eksikliği",
                "C) Swyer sendromu",
                "D) Turner sendromu",
                "E) Persistan Müllerian kanal sendromu"
            ],
            "correctAnswer": "B",
            "explanation": "17-beta HSD3 eksikliğinde androstenedion testosterona dönüşemez; oran yükselir, AMH normal olduğu için Müller yapıları geriler, dış genitalya dişidir."
        }
    ),
    make_slide(
        17,
        "5-Alfa Redüktaz Tip 2 Eksikliği (5-ARD)",
        "SRD5A2 Mutasyonu, Guevedoces Fenomeni ve Pubertal Virilizasyon",
        """5-alfa redüktaz tip 2 eksikliği, testosteronun dihidrotestosterona (DHT) dönüşememesiyle karakterize, otozomal resesif kalıtılan bir 46,XY CGB tablosudur.

**1. Fizyopatolojik Temel:**
• Testis gelişimi, Sertoli ve Leydig hücre fonksiyonları normaldir.
• **AMH normaldir:** Müller kanalları geriler; uterus, fallop tüpü ve üst vajina yoktur.
• **Testosteron normal veya yüksektir:** Wolff kanalları gelişir; epididim, vaz deferens ve seminal veziküller mevcuttur (testosteron bağımlı).
• **DHT yetersizdir:** Dış genital organlar virilize olamaz. Doğumda dişi dış genitalya, pseudovajinal perineoskrotal hipospadias veya mikropenis ile prezante olur. Testisler genellikle inguinal kanalda veya labia majoralardadır.

**2. Pubertede Dönüşüm (Guevedoces Fenomeni):**
• Puberteye kadar kız çocuğu olarak yetiştirilen bireyde, pubertede hipofizer LH patlamasıyla devasa miktarda testosteron üretilir ve karaciğerdeki 5-alfa redüktaz tip 1 izoenzimi devreye girer.
• Penis uzar, testisler skrotuma iner, ses kalınlaşır, kas kitlesi artar; **ancak jinekomasti gelişmez!** (Meme gelişimi androjen fazlalığı ile baskılanır).""",
        [
            {"type": "clinical", "badge": "🔴 JİNEKOMASTİ YOKLUĞU", "text": "5-ARD olgularında pubertede virilizasyon olurken JİNEKOMASTİ OLMAZ; bu özellik meme gelişen Androjen Duyarsızlığı Sendromundan en temel klinik farktır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / DUS SORUSU", "text": "Doğumda dişi veya şüpheli genitalyası olan, pubertede sesi kalınlaşıp klitorisi penise dönüşen ancak meme gelişimi olmayan 46,XY olguda tanı 5-alfa redüktaz eksikliğidir.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-017",
            "question": "Kız çocuğu olarak büyütülen 14 yaşındaki hastada puberte döneminde ses kalınlaşması, klitoromegali ve kas kütlesinde artış saptanıyor. Memeleri gelişmemiş olan hastanın karyotipi 46,XY ve pelvik USG'de uterus saptanmıyor. En olası tanı hangisidir?",
            "options": [
                "A) Tam androjen duyarsızlığı sendromu",
                "B) 5-alfa redüktaz tip 2 eksikliği",
                "C) Mayer-Rokitansky-Küster-Hauser sendromu",
                "D) Swyer sendromu",
                "E) Turner sendromu"
            ],
            "correctAnswer": "B",
            "explanation": "46,XY karyotip + uterus yokluğu + pubertede güçlü virilizasyon + meme gelişiminin OLMAMASI 5-alfa redüktaz tip 2 eksikliğinin klasik kliniğidir."
        }
    ),
    make_slide(
        18,
        "Tam Androjen Duyarsızlığı Sendromu (CAIS / Testiküler Feminizasyon)",
        "Androjen Reseptör Mutasyonu, 46,XY Karyotip ve Kusursuz Dişi Fenotipi",
        """Tam Androjen Duyarsızlığı Sendromu (Complete Androgen Insensitivity Syndrome - CAIS), X kromozomunda yer alan androjen reseptör (*AR*) genindeki inaktive edici mutasyonlar sonucu hedef dokuların androjenlere tamamen yanıtsız kalmasıdır.

**1. Anatomik ve Hormonal Mekanizma:**
• **Karyotip:** 46,XY'dir. Testisler mevcuttur (intraabdominal, inguinal veya labial yerleşimli).
• **Sertoli Hücreleri Normaldir:** Normal düzeyde AMH salgılarlar. Bu nedenle **Müllerian yapılar geriler; Uterus, tubalar ve vajinanın üst kısmı YOKTUR**. Vajina 2-3 cm derinliğinde kör bir kese şeklindedir.
• **Androjen Reseptörü Çalışmaz:** Dokular testosteron ve DHT'yi algılayamaz. Bu nedenle Wolff kanalları da geriler; dış genitalya kusursuz bir kadın fenotipinde gelişir.
• **Aromataz Etkisi:** Aşırı testosteron aromatize edilerek östrojene dönüşür. Androjenik fren mekanizması olmadığı için **mükemmel meme gelişimi** ve tipik kadın vücut konturu oluşur.
• Ancak androjen etkisi sıfır olduğu için **aksiller ve pubik kıllanma YOKTUR veya son derece seyrektir**.""",
        [
            {"type": "clinical", "badge": "🔴 PATOGNOMONİK BULGU", "text": "CAIS'de meme gelişimi Tanner evre 5 düzeyinde mükemmeldir, ancak aksiller ve pubik kıllanma tamamen yoktur (veya seyrektir).", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS KLASİĞİ", "text": "46,XY karyotip + meme gelişimi var + kör vajina + uterus yok + pubik/aksiller kıl yok = Tam Androjen Duyarsızlığı Sendromu (Testiküler Feminizasyon).", "color": "sky"}
        ],
        {
            "id": "prac-cgb-018",
            "question": "17 yaşında primer amenore nedeniyle başvuran, boyu uzun, meme gelişimi Tanner evre 5 olan ancak aksiller ve pubik kıllanması bulunmayan hastanın jinekolojik muayenesinde vajinasının kör bir çöküntü olduğu ve pelvik USG'de uterusun bulunmadığı görülüyor. Karyotipi 46,XY olan bu hastada en olası tanı hangisidir?",
            "options": [
                "A) Swyer sendromu",
                "B) Mayer-Rokitansky-Küster-Hauser sendromu",
                "C) Tam androjen duyarsızlığı sendromu",
                "D) 5-alfa redüktaz eksikliği",
                "E) Turner sendromu"
            ],
            "correctAnswer": "C",
            "explanation": "46,XY karyotipinde mükemmel meme gelişimi, uterus yokluğu, kör vajina ve pubik/aksiller kıllanma yokluğu CAIS (testiküler feminizasyon) için patognomoniktir."
        }
    ),
    make_slide(
        19,
        "Parsiyel Androjen Duyarsızlığı Sendromu (PAIS)",
        "Reifenstein Sendromu Yelpazesi: Ambigius Genitalya ve Jinekomasti",
        """Androjen reseptöründe parsiyel fonksiyon kaybı olduğunda klinik tablo Parsiyel Androjen Duyarsızlığı Sendromu (PAIS; tarihsel adıyla Reifenstein sendromu yelpazesi) olarak adlandırılır.

**1. Klinik Yelpaze ve Fenotipik Çeşitlilik:**
• Dokuların androjene kısmi yanıt verebilmesi nedeniyle fenotip geniştir:
  - Hafif formlarda: Yalnızca infertilite ve izole mikropenis veya hafif jinekomasti.
  - Orta/Ağır formlarda: Doğumda belirgin **ambigius genitalya**, bifid skrotum, perineoskrotal hipospadias, psödovajinal boşluk ve inmemiş testisler.
• **İç Genitalya:** AMH normal olduğu için uterus ve tuba uterina bulunmaz; Wolff kanalı türevleri ise hipoplaziktir.
• **Pubertede:** Hem androjen hem östrojen etkisi yarışır; belirgin **jinekomasti** ile birlikte yetersiz virilizasyon (seyrek sakal, ince ses) görülür.

Tedavi ve cinsiyet yönlendirmesi olgunun fenotipine, dış genitalyanın cerrahiye uygunluğuna ve androjen duyarlılık derecesine göre multidisipliner konsey kararıyla belirlenir.""",
        [
            {"type": "clinical", "badge": "🔴 PUBERTE BULGUSU", "text": "PAIS olgularında pubertede jinekomasti gelişimi neredeyse evrenseldir; çünkü kısmi reseptör blokajında aromatazla oluşan östrojen etkisi baskın çıkar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE SORUSU", "text": "46,XY karyotipli hastada ambigius genitalya, uterus yokluğu ve pubertede jinekomasti birlikteliği Parsiyel Androjen Duyarsızlığı (Reifenstein) sendromunu düşündürür.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-019",
            "question": "46,XY karyotipli, doğumda bifid skrotum ve perineoskrotal hipospadias saptanan, pelvik USG'de uterus ve over izlenmeyen, pubertede belirgin jinekomasti gelişen hastada en olası tanı hangisidir?",
            "options": [
                "A) Konjenital adrenal hiperplazi",
                "B) Parsiyel androjen duyarsızlığı sendromu",
                "C) Mayer-Rokitansky-Küster-Hauser sendromu",
                "D) Swyer sendromu",
                "E) Saf Leydig hücre agenezisi"
            ],
            "correctAnswer": "B",
            "explanation": "46,XY karyotipinde ambigius genitalya, uterus yokluğu ve pubertede belirgin jinekomasti gelişimi Parsiyel Androjen Duyarsızlığı Sendromu (PAIS) ile uyumludur."
        }
    ),
    make_slide(
        20,
        "Mayer-Rokitansky-Küster-Hauser (MRKH) Sendromu: Müllerian Agenezi",
        "46,XX Karyotip, Normal Overler, Uterus-Vajina Agenezisi ve Tip 2 Anomaliler",
        """MRKH Sendromu (Müllerian Agenezi), embriyonik dönemde paramezonefrik kanalların gelişememesi sonucu uterus ve vajinanın üst 2/3'ünün konjenital yokluğu ile karakterizedir. Primer amenorenin Turner'dan sonraki en sık 2. nedenidir (~1/4500 kız doğum).

**1. Klinik ve Hormonal Profil:**
• **Karyotip:** Tamamen normal dişi karyotipidir (**46,XX**).
• **Over Fonksiyonları:** Overler embriyolojik olarak genital kabartıdan geliştiği için Müllerian sistemden bağımsızdır; **overler ve folikül rezervi tamamen normaldir**.
• **Sekonder Cinsiyet Karakterleri:** Östrojen ve progesteron üretimi normal olduğundan **meme gelişimi, aksiller ve pubik kıllanma, kadın tipi yağ dağılımı Tanner evre 5 düzeyinde kusursuzdur**.
• Başvuru nedeni ergenlikte menstrüasyonun hiç başlamamasıdır (**primer amenore**). Muayenede vajina sığ bir kör çukur şeklindedir; USG/MRG'de uterus ve serviks izlenmez.

**2. Tipleri:**
• **Tip 1 (İzole):** Yalnızca ürogenital traktus etkilenir.
• **Tip 2 (MURCS Asosiasyonu):** Müllerian ageneziye Renal agenezi/ektopi (%30-40) ve Serviko-torasik vertebra segmentasyon kusurları (Klippel-Feil anomalisi) eşlik eder.""",
        [
            {"type": "clinical", "badge": "🔴 RENAL VE VERTEBRAL TARAMA", "text": "MRKH tanısı alan her genç kıza mutlaka renal ultrasonografi ve omurga grafisi çekilmelidir (tek taraflı böbrek agenezisi ve iskelet anomalileri sıktır).", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / DUS AYIRICI TANISI", "text": "Normal dişi fenotipi + Tanner 5 meme + NORMAL pubik kıl + UTERUS YOK = MRKH (46,XX). Pubik kıl YOK ise = CAIS (46,XY).", "color": "sky"}
        ],
        {
            "id": "prac-cgb-020",
            "question": "16 yaşında primer amenore ile başvuran kız hastada meme gelişimi ve pubik kıllanma tamamen normal (Tanner 5) bulunuyor. Pelvik ultrasonda overler normal boyutta izlenirken uterus ve vajina üst kısmı izlenmiyor. Karyotipi 46,XX olan bu hastada en olası tanı hangisidir?",
            "options": [
                "A) Turner sendromu",
                "B) Mayer-Rokitansky-Küster-Hauser sendromu",
                "C) Tam androjen duyarsızlığı sendromu",
                "D) Swyer sendromu",
                "E) Konjenital adrenal hiperplazi"
            ],
            "correctAnswer": "B",
            "explanation": "46,XX dişi karyotipinde normal overler ve normal sekonder seks karakterleri (kıllanma dahil) ile birlikte konjenital uterus ve vajina yokluğu MRKH sendromudur."
        }
    ),
    make_slide(
        21,
        "Müllerian Füzyon ve Septum Rezorbsiyon Anomalileri",
        "Uterus Didelfis, Bikornis, Septus, Arkuat ve Obstetrik Komplikasyonlar",
        """Paramezonefrik kanalların orta hatta birleşmesi veya birleşme sonrası aradaki dokunun rezorbe olması süreçlerindeki aksamalar çeşitli konjenital uterin anomalilere yol açar (ASRM Sınıflaması).

**1. Başlıca Uterin Anomaliler:**
• **Uterus Didelfis (Sınıf III):** Müller kanallarının tam füzyon kusurudur. Tamamen ayrı iki hemiserviks ve iki uterus gövdesi mevcuttur; sıklıkla longitüdinal vajinal septum eşlik eder.
• **Uterus Bikornis (Sınıf IV):** Müller kanallarının parsiyel füzyon kusurudur. Fundusta derin bir çentik (>1 cm) bulunur; uterin boynuzlar ayrılmıştır ancak tek bir serviks (bikornis unikollis) veya çift serviks olabilir.
• **Uterus Septus (Sınıf V):** Kanallar normal şekilde birleşmiş ancak aradaki median fibröz/fibromüsküler septum rezorbe olamamıştır. Dış fundal kontur normal ve düzdür. **Tekrarlayan 1. ve 2. trimester düşüklerinin (habitüel abortus) en sık konjenital nedenidir!** Septum avasküler olduğu için implantasyon başarısız olur. Tedavisi histeroskopik septum rezeksiyonudur.
• **Uterus Arkuat (Sınıf VI):** Fundusta <1 cm hafif konkav çöküntü; benign bir varyant kabul edilir.""",
        [
            {"type": "clinical", "badge": "🔴 TEKRARLAYAN DÜŞÜK TUZAĞI", "text": "Konjenital uterin anomaliler içinde tekrarlayan gebelik kaybı ve erken doğuma en sık neden olanı UTERUS SEPTUS'tur; dış konturu tamamen düzdür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Histeroskopi ile tedavi edilebilen ve tekrarlayan abortus öyküsü olan kadında kavum uteriyi ikiye bölen avasküler septum anomalisi Uterus Septus'tur.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-021",
            "question": "Üç kez ardışık 10-12. gebelik haftalarında spontan abortus öyküsü olan 28 yaşındaki kadının çekilen histerosalpingografisinde (HSG) ve MRG'sinde fundal dış konturun düz olduğu, kavum uteriyi fundustan servikse kadar ayıran doku bandı izleniyor. En olası tanı ve tedavi yöntemi hangisidir?",
            "options": [
                "A) Uterus didelfis - Laparotomi ile metroplasti",
                "B) Uterus septus - Histeroskopik septum rezeksiyonu",
                "C) Uterus bikornis - Strassman metroplastisi",
                "D) Asherman sendromu - Servikal dilatasyon",
                "E) Uterus arkuat - İzlem"
            ],
            "correctAnswer": "B",
            "explanation": "Fundal dış konturun düz olması ve tekrarlayan abortuslara yol açması Uterus Septus için tipiktir; altın standart tedavi histeroskopik septum rezeksiyonudur."
        }
    ),
    make_slide(
        22,
        "Himen ve Vajinal Kanalizasyon Kusurları",
        "İmperfore Himen, Transvers Vajinal Septum ve Hematokolpos Kliniği",
        """Vajinal kanalizasyonun ve lümen açılmasının tamamlanamaması obstrüktif genital anomalilere yol açar.

**1. İmperfore Himen:**
• Kadın genital sisteminin en sık görülen obstrüktif anomalisidir (~1/1000-2000 kız).
• Müllerian lümen ile ürogenital sinüsün birleştiği seviyedeki endodermal epitelin perforasyonunun gerçekleşmemesi sonucu oluşur.
• **Klinik Tablo:** Puberte çağına kadar asemptomatiktir. Menarş başladığında kan dışarı akamaz; menstrüel sikluslarla tekrarlayan **siklik kasık/pelvik ağrı**, idrar yapmada zorlanma ve **kriptomenore (gizli kanama)** gelişir.
• Vajina kanla dolarak devasa boyutlara ulaşır (**hematokolpos**); tedavi edilmezse uterus kavitesine (**hematometra**) ve tubalara (**hematosalpenks**) geri teperek pelvik endometriozise yol açabilir.
• Muayenede introitusta bombeleşen, **mavimsi-mor renkli, fluktuasyon veren parlak membran** patognomoniktir. Tedavisi haç şeklinde insizyondur (himenotomi).

**2. Transvers Vajinal Septum:**
• Sinovajinal yumruların Müllerian kanalla füzyon bölgesinde kanalizasyon kusurudur; sıklıkla üst ve orta 1/3 birleşim yerindedir.""",
        [
            {"type": "clinical", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Ergenlikte siklik kasık ağrısı olup kanaması olmayan kızda introitusta mavi-mor kabarık kitle görülmesi imperfore himen için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE KLASİĞİ", "text": "İmperfore himen tedavisinde aspirasyon yapılmaz; enfeksiyon (piyokolpos) riskini önlemek için cerrahi himenotomi (haç insizyon) uygulanır.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-022",
            "question": "14 yaşındaki kız çocuğu her ay düzenli aralıklarla tekrarlayan şiddetli kasık ağrısı ve idrar yapmada güçlük şikayetiyle getiriliyor. Fizik muayenede sekonder cinsiyet özellikleri Tanner evre 4 olan hastanın vulva muayenesinde introitusta dışarı doğru bombeleşen, gergin, mavimsi kistik bir yapı gözleniyor. En olası tanı hangisidir?",
            "options": [
                "A) Mayer-Rokitansky-Küster-Hauser sendromu",
                "B) İmperfore himen (Hematokolpos)",
                "C) Bartholin bezi apsesi",
                "D) Gartner kanalı kisti",
                "E) Rhabdomyosarkom (Sarkoma botryoides)"
            ],
            "correctAnswer": "B",
            "explanation": "Pubertede siklik pelvik ağrı, menstrüel kanama olmaması (kriptomenore) ve introitusta mavimsi bombeleşen zar imperfore himen (hematokolpos) bulgusudur."
        }
    ),
    make_slide(
        23,
        "Hipospadias, Epispadias ve Kriptorşidizm",
        "Ürogenital Katlantı Kapanma Kusurları, Dorsal Defektler ve İnmemiş Testis",
        """Erkek dış genital organlarının en sık görülen doğumsal anomalileri üretra ve testis iniş defektleridir.

**1. Hipospadias:**
• Ürogenital katlantıların ventral hatta orta çizgide tam birleşememesi sonucu eksternal üretra orifisinin penis ventralinde (alt yüzünde) açılmasıdır (~1/300 erkek bebek).
• Üçlü anomali komponenti: Ektopik ventral mea, **kordi** (penisin ventrale eğriliği) ve prepisyumun dorsalde toplanması (**kukuleta sünnet derisi**).
• **Kritik Kural:** Sünnet derisi cerrahi onarımda üretra rekonstrüksiyonu için greft olarak kullanılacağından **kesinlikle sünnet yapılmamalıdır!**

**2. Epispadias:**
• Üretra orifisinin penisin dorsal (üst) yüzünde açılmasıdır; genital tüberkülün kaudale göç kusurudur. Sıklıkla **ekstrofi vezika** kompleksiyle birliktedir.

**3. Kriptorşidizm (İnmemiş Testis):**
• Testisin skrotuma inişini tamamlayamamasıdır. Term bebekte %3, prematürelerde %30 görülür.
• Çoğu 3-6. ayda kendiliğinden iner. 6. aydan sonra inmemişse fertiliteyi korumak ve seminom/malignite riskini kontrol altına almak için **6-12. aylar arasında orşiopeksi** ameliyatı yapılmalıdır.""",
        [
            {"type": "clinical", "badge": "🔴 KESİN KONTRENDİKASYON", "text": "Hipospadiaslı yenidoğanlarda sünnet KESİNLİKLE yasaktır; sünnet derisi neouretranın cerrahi rekonstrüksiyonunda kullanılacaktır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "İnmemiş testiste cerrahi orşiopeksi için ideal zaman 6-12. aylardır; testis skrotuma indirilse dahi germ hücreli tümör (seminom) riski normale inmez.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-023",
            "question": "Yenidoğan muayenesinde eksternal meatusun penisin alt yüzeyinde yerleştiği, ventral kordi ve dorsal prepisyum fazlalığı saptanan bebekte aileye verilmesi gereken en kritik ilk öneri hangisidir?",
            "options": [
                "A) Hemen profilaktik orşiopeksi yapılmalıdır.",
                "B) Bebeğe kesinlikle sünnet yapılmamalıdır.",
                "C) Yüksek doz testosteron tedavisi başlanmalıdır.",
                "D) Derhal sistoskopi uygulanmalıdır.",
                "E) Acil laparotomi ile gonadlar araştırılmalıdır."
            ],
            "correctAnswer": "B",
            "explanation": "Hipospadias saptanan yenidoğanlarda sünnet derisi üretroplasti ameliyatında rekonstrüksiyon dokusu olarak kullanılacağından sünnet kesinlikle kontrendikedir."
        }
    ),
    make_slide(
        24,
        "Ambigius Genitalyalı Yenidoğana Klinik ve Genetik Yaklaşım",
        "Acil Algoritma, Tuz Kaybı Taraması, Karyotipleme ve Multidisipliner Yönetim",
        """Ambigius genitalya (cinsiyeti belirsiz dış genitalya), yenidoğan döneminde acil tıbbi ve psikososyal yönetim gerektiren önemli bir durumdur.

**1. Acil Klinik Yönetim Adımları:**
• **1. Adım - Hayati Tehdit Taraması:** Olası bir 21-OH eksikliğine bağlı tuz kaybettiren KAH krizini önlemek için acilen serum elektrolitleri (Na, K), kan gazı, kan şekeri ve 17-OH progesteron ölçülmelidir.
• **2. Adım - Fizik Muayene:** Gonadlar palpe ediliyor mu? (Skrotum veya labium majusta gonad palpe ediliyorsa olguda en az bir Y kromozomu / fonksiyonel testis dokusu vardır).
• **3. Adım - Görüntüleme:** Pelvik ultrasonografi ile uterus ve Müllerian yapıların varlığı araştırılır. Uterus varsa olgu büyük olasılıkla 46,XX virilize dişidir (KAH).
• **4. Adım - Hızlı Genetik:** Floresan in situ hibridizasyon (FISH) veya QF-PCR ile SRY ve X/Y varlığı 24-48 saatte belirlenir, ardından tam karyotip analizi yapılır.

**2. Cinsiyet Atamasında Temel İlkeler:**
• Aileye cinsiyet beyanı için acele edilmemelidir. Çocuk endokrinolojisi, genetik, çocuk cerrahisi/ürolojisi ve psikiyatri uzmanlarından oluşan multidisipliner ekip karar vermelidir.""",
        [
            {"type": "clinical", "badge": "🔴 İLK VE EN KRİTİK ADIM", "text": "Ambigius genitalyalı bebekte ilk adım adrenal kriz (hiponatremi/hiperkalemi) riskini değerlendirmektir; hayat kurtarıcıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 AMBİGİUS MUAYENE KURALI", "text": "Ambigius genitalyada inguinal veya labioskrotal bölgede GONAD PALPE EDİLİYORSA olgu neredeyse kesinlikle Y kromozomu taşımaktadır.", "color": "sky"}
        ],
        {
            "id": "prac-cgb-024",
            "question": "Doğum odasında ambigius genitalya saptanan bir bebekte hekimin yapması gereken İLK ve EN ACİL klinik yaklaşım aşağıdakilerden hangisidir?",
            "options": [
                "A) Hemen cerrahi cinsiyet düzeltme ameliyatı planlamak",
                "B) Aileye çocuğun cinsiyetini erkek olarak bildirmek",
                "C) Yaşamı tehdit eden tuz kaybı krizini önlemek için elektrolit ve 17-OH progesteron düzeylerini kontrol etmek",
                "D) Bebeğe büyüme hormonu başlamak",
                "E) Acil tanısal laparoskopi yapmak"
            ],
            "correctAnswer": "C",
            "explanation": "Ambigius genitalyalı bebekte en sık ve ölümcül neden KAH'tır. Hayatı tehdit eden tuz kaybı krizini yakalamak için acil elektrolit ve 17-OHP takibi ilk adımdır."
        }
    )
]

# ==============================================================================
# 2. PRENATAL TANI VE UYGULAMA ALANLARI (24 SLAYT)
# ==============================================================================
prenatal_slides = [
    make_slide(
        1,
        "Prenatal Tanının Amaçları, İlkeleri ve Endikasyonları",
        "İntrauterin Teşhis Stratejileri, Aile Danışmanlığı ve Risk Endikasyonları",
        """Prenatal tanı; fetustaki genetik, kromozomal veya yapısal anomalilerin doğum öncesinde saptanmasını, aileye doğru ve tarafsız bilgi verilmesini, gerektiğinde fetal tedavi veya doğum şekli/yerinin planlanmasını hedefleyen perinatolojik ve genetik disiplindir.

**1. Temel Prenatal Tanı Endikasyonları:**
• **İleri Anne Yaşı:** Doğum anında anne yaşının ≥35 olması (kromozomal anöploidi riski katlanarak artar).
• **Önceki Gebelikte Anomali Öyküsü:** Trizomi, açık nöral tüp defekti veya genetik sendromlu çocuk öyküsü.
• **Ebeveynlerde Dengeli Kromozomal Yeniden Düzenlenme:** Ebeveynlerden birinde dengeli resiprokal veya Robertsonyan translokasyon, inversiyon taşıyıcılığı.
• **Ailevi Monogenik Hastalık Öyküsü:** Kistik fibrozis, SMA, Talasemi, Duchenne Musküler Distrofi vb. mutasyon taşıyıcılığı.
• **Anormal Tarama Testi veya Ultrasonografi:** İkili/üçlü/dörtlü test veya NIPT'de yüksek risk, USG'de majör fetal anomali veya ense kalınlığı (NT) artışı.""",
        [
            {"type": "clinical", "badge": "🔴 TARAMA VE TANI AYRIMI", "text": "Tarama testleri (ikili test, NIPT) yalnızca risk belirler; kesin teşhis için invaziv tanı testleri (CVS, Amniyosentez) zorunludur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Prenatal tanı endikasyonları içinde ebeveynde dengeli translokasyon taşıyıcılığı fetusta dengesiz genom riski nedeniyle doğrudan invaziv tanı gerektirir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-001",
            "question": "Aşağıdakilerden hangisi doğrudan kesin tanı koyduran invaziv prenatal genetik tanı yöntemlerinden biridir?",
            "options": [
                "A) Birinci trimester ikili tarama testi",
                "B) Maternal kanda hücresiz fetal DNA (cffDNA / NIPT)",
                "C) Amniyosentez",
                "D) İkinci trimester dörtlü tarama testi",
                "E) Fetal ense kalınlığı (NT) ultrasonografik ölçümü"
            ],
            "correctAnswer": "C",
            "explanation": "İkili test, dörtlü test, NT ölçümü ve NIPT tarama testleridir. Amniyosentez, CVS ve kordosentez ise doğrudan fetal hücrelerden sitogenetik analiz sağlayan invaziv tanı testleridir."
        }
    ),
    make_slide(
        2,
        "Fetal Ense Kalınlığı (Nuchal Translucency - NT) Ölçümü",
        "11-13+6. Haftalar, FMF Kriterleri, Trizomiler ve Konjenital Kalp Defektleri",
        """Fetal ense kalınlığı (NT), birinci trimesterde fetusun boyun arkasında cilt ile servikal omurga arasındaki cilt altı sıvı birikiminin ultrasonografik kesitidir.

**1. Fetal Medicine Foundation (FMF) Ölçüm Standartları:**
• **Gebelik Haftası:** 11 hafta 0 gün ile 13 hafta 6 gün arasında yapılmalıdır.
• **Fetal Boyut:** Baş-popo uzunluğu (Crown-Rump Length - CRL) **45 mm ile 84 mm** arasında olmalıdır.
• **Görüntüleme:** Fetus midsagittal planda, nötral pozisyonda olmalı; ekranın %75'ini fetal baş ve toraks kaplamalıdır.
• **Kaliper Yerleşimi:** Sıvı alanını sınırlayan parlak çizgilerin 'içten içe' (inner to inner) yerleştirilmesi zorunludur; fetal cilt ile amniyon zarı ayırt edilmelidir.

**2. Artmış NT (>3.5 mm veya >95. persentil) Klinik Anlamı:**
• **Trizomi 21 (Down), Trizomi 18 (Edwards) ve Trizomi 13 (Patau) sendromları**.
• **Turner sendromu (45,X):** Çoğunlukla dev kistik higroma şeklinde izlenir.
• **Majör Konjenital Kalp Defektleri:** Karyotip normal çıksa dahi fetal ekokardiyografi endikasyonudur!
• **Noonan sendromu** ve diğer RASopatiler, iskelet displazileri.""",
        [
            {"type": "clinical", "badge": "🔴 KARYOTİP NORMAL OLSA BİLE", "text": "NT >3.5 mm olan bir fetusta karyotip normal çıksa dahi mutlaka fetal ekokardiyografi ve mikrodizi (CMA) yapılmalıdır (kalp defekti ve sendrom riski!).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Fetal ense kalınlığı (NT) ölçümü CRL 45-84 mm arasında (11-13+6 hafta), midsagittal kesitte ve kaliperler içten içe konularak yapılır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-002",
            "question": "12. gebelik haftasında (CRL: 58 mm) yapılan ultrasonografide fetal ense kalınlığı (NT) 4.2 mm ölçülen ve yapılan koryon villus örneklemesinde karyotipi normal (46,XX) saptanan bir fetusta bundan sonraki en kritik basamak hangisi olmalıdır?",
            "options": [
                "A) Derhal gebeliğin sonlandırılması",
                "B) İkinci trimesterde fetal ekokardiyografi ve detaylı anomali taraması yapılması",
                "C) Sadece rutin üçüncü trimester takibine geçilmesi",
                "D) Maternal kanda serbest beta-hCG ölçümü yapılması",
                "E) Gebeye profilaktik folik asit tedavisi başlanması"
            ],
            "correctAnswer": "B",
            "explanation": "Karyotip normal olsa bile artmış NT (>3.5 mm) majör konjenital kalp defektleri ve genetik mikrodelesyon sendromları ile yakından ilişkilidir; detaylı anomali USG ve fetal eko zorunludur."
        }
    ),
    make_slide(
        3,
        "Erken Ultrasonografik Belirteçler: Nazal Kemik ve Duktus Venozus Doppler",
        "Nazal Kemik Hipoplazisi, Duktus Venozus Ters 'a' Dalgası ve Triküspit Yetmezliği",
        """Birinci trimesterde NT ölçümüne eklenen ek ultrasonografik belirteçler, Down sendromu ve diğer anöploidilerin yakalama oranını artırır ve yalancı pozitifliği düşürür.

**1. Nazal Kemik (Nasal Bone):**
• 11-13+6. haftalarda midsagittal yüzde nazal kemik iki paralel hiperekojenik çizgi şeklinde izlenir (üstteki cilt, alttaki daha kalın olan nazal kemik).
• Trizomi 21'li fetusların yaklaşık %60-70'inde nazal kemik hipoplaziktir veya **tamamen izlenemez (agenezi)**. Öglisemi/normal fetusta görülme oranı <%1-2'dir.

**2. Duktus Venozus Doppler İncelemesi:**
• Duktus venozus, umbilikal venöz kanı doğrudan vena kava inferiora aktaran şanttır.
• Ventriküler sistol (S), ventriküler diyastol (D) ve atriyal kontraksiyon (**a dalgası**) fazlarından oluşur.
• Atriyal kontraksiyon sırasında **ters (retrograd / negatif) a dalgası** görülmesi, fetal kardiyak aşırı yüklenmeyi veya artmış santral venöz basıncı gösterir. Down sendromu ve konjenital kalp defektlerinde güçlü bir risk artış belirtecidir.

**3. Triküspit Kapak Regürjitasyonu:**
• Sistolik pik velositesinin >60 cm/sn olması triküspit yetmezliğini gösterir; trizomi riskini 6-8 kat artırır.""",
        [
            {"type": "clinical", "badge": "🔴 DUCTUS VENOZUS ALARMI", "text": "Duktus venozus doppler incelemesinde 'a' dalgasının negatif (ters) olması hem trizomiler hem de konjenital kalp patolojileri için alarm bulgusudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / DUS VURGUSU", "text": "Birinci trimester taramasında nazal kemiğin izlenmemesi Down sendromu riskini belirgin artıran en özgül USG belirteçlerinden biridir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-003",
            "question": "12. gebelik haftasında yapılan ultrasonografik incelemede fetal duktus venozus doppler akımında atriyal kontraksiyon fazında (a dalgası) ters akım (ters a dalgası) saptanması durumunda fetusta en çok şüphelenilmesi gereken iki patoloji grubu hangisidir?",
            "options": [
                "A) Spina bifida ve anensefali",
                "B) Kromozomal anöploidiler (Trizomiler) ve konjenital kalp anomalileri",
                "C) Renal agenezi ve Potter sendromu",
                "D) Omfalosel ve gastroşizis",
                "E) Fetal hidrosefali ve Dandy-Walker malformasyonu"
            ],
            "correctAnswer": "B",
            "explanation": "Duktus venozus 'a' dalgasında ters akım, kardiyak yüklenmeyi yansıtır ve kromozomal anöploidiler (özellikle Trizomi 21 ve 18) ile majör kalp defektleri ile ilişkilidir."
        }
    ),
    make_slide(
        4,
        "Birinci Trimester İkili Tarama Testi",
        "Serbest Beta-hCG, PAPP-A ve NT Kombinasyonu: Matematiksel Risk Hesabı",
        """İkili tarama testi (kombine test), 11 hafta 0 gün ile 13 hafta 6 gün arasında (CRL 45-84 mm) yapılan, Down sendromu (Trizomi 21) ve Trizomi 18 için en değerli birinci trimester biyokimyasal tarama yöntemidir.

**1. Biyokimyasal Parametreler ve Değerlendirme:**
• **Serbest Beta-hCG (Free β-hCG):** Sinsityotrofoblastlarca üretilir. Down sendromlu gebeliklerde maternal kanda belirgin olarak **artmıştır (~2.0 MoM)**.
• **PAPP-A (Pregnancy-Associated Plasma Protein A):** Trofoblast kaynaklı metalloproteinazdır. Down sendromunda ve Trizomi 18'de maternal serumda belirgin olarak **azalmıştır (~0.5 MoM)**.
• Değerler mutlak konsantrasyon yerine, gebelik haftasına göre normalize edilmiş **MoM (Multiples of Median)** katları cinsinden ifade edilir.

**2. Kombine Risk Hesabı:**
• Maternal yaş riski + NT kalınlığı + Serbest beta-hCG MoM + PAPP-A MoM verileri logaritmik bir yazılımla birleştirilir.
• Yakalama (detection) oranı yaklaşık **%85-90**, yalancı pozitiflik oranı **%5**'tir.
• Eşik değer genellikle 1/250 veya 1/300 kabul edilir; bu eşiğin üzerindeki riskler 'yüksek risk' olarak tanımlanır ve invaziv tanı önerilir.""",
        [
            {"type": "clinical", "badge": "🔴 TUS VE KLİNİK FORMÜL", "text": "Down sendromunda birinci trimester biyokimyası: Serbest beta-hCG YÜKSEK, PAPP-A DÜŞÜK, NT ARTMIŞTIR.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "İkili tarama testinde kullanılan maternal serum biyokimyasal belirteçleri Serbest Beta-hCG ve PAPP-A'dır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-004",
            "question": "Birinci trimester kombine tarama testinde Trizomi 21 (Down sendromu) saptanan bir fetusta serum biyokimyasal belirteçlerinin beklenen değişimi nasıldır?",
            "options": [
                "A) Serbest beta-hCG artar, PAPP-A artar",
                "B) Serbest beta-hCG azalır, PAPP-A azalır",
                "C) Serbest beta-hCG artar, PAPP-A azalır",
                "D) Serbest beta-hCG azalır, PAPP-A artar",
                "E) Biyokimyasal belirteçler değişmez, yalnızca NT artar"
            ],
            "correctAnswer": "C",
            "explanation": "Down sendromunda birinci trimester maternal serumunda Serbest beta-hCG artarken (~2 MoM), PAPP-A seviyesi azalır (~0.5 MoM)."
        }
    ),
    make_slide(
        5,
        "İkinci Trimester Üçlü ve Dörtlü Tarama Testleri",
        "15-20. Haftalar: AFP, hCG, uE3 ve İnhibin-A Dinamikleri",
        """Birinci trimester taramasını kaçıran gebelerde veya açık nöral tüp defekti riskini değerlendirmek amacıyla 15 ile 20. gebelik haftaları arasında (en ideal 16-18. haftalar) biyokimyasal tarama testleri uygulanır.

**1. Üçlü Test (Triple Test) Parametreleri:**
• **Maternal Serum Alfa-Fetoprotein (MSAFP):** Fetal karaciğer ve vitellüs kesesinden sentezlenir.
• **Total hCG:** Plasental sinsityotrofoblastlardan sentezlenir.
• **Ankonjuge Östriol (uE3):** Fetal adrenal korteks (DHEA-S), fetal karaciğer (16-OH DHEA-S) ve plasentanın (östriol sentezi) ortak fetoplasental ünitesi tarafından üretilir.

**2. Dörtlü Test (Quadruple Test):**
• Üçlü teste dördüncü bir belirteç olarak **Dimerik İnhibin-A (DIA)** eklenir.
• İnhibin-A eklenmesi Down sendromu yakalama oranını %65-70'ten **%80-83'e** yükseltir, yalancı pozitifliği azaltır.

Tüm parametreler maternal ağırlık, etnisite, sigara kullanımı, diyabet varlığı ve gebelik haftasına göre standardize edilerek MoM değerine dönüştürülür.""",
        [
            {"type": "clinical", "badge": "🔴 FETOPLASENTAL BÜTÜNLÜK", "text": "uE3 (östriol) fetal adrenal, fetal karaciğer ve plasentanın ortak çalışmasıyla sentezlenir; fetal ölümde veya adrenal hipoplazide sıfıra iner.", "color": "rose"},
            {"type": "exam", "badge": "🔵 DÖRTLÜ TEST BİLEŞENLERİ", "text": "Dörtlü tarama testinde ölçülen parametreler: MSAFP + total hCG + uE3 + Dimerik İnhibin-A'dır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-005",
            "question": "İkinci trimester dörtlü tarama testinde, üçlü test bileşenlerine eklenerek Down sendromu yakalama oranını artıran dördüncü biyokimyasal belirteç hangisidir?",
            "options": [
                "A) PAPP-A",
                "B) Dimerik İnhibin-A",
                "C) Serbest estron",
                "D) Progesteron",
                "E) Plasental laktojen (hPL)"
            ],
            "correctAnswer": "B",
            "explanation": "Dörtlü test, üçlü test parametrelerine (AFP, hCG, uE3) Dimerik İnhibin-A eklenmesiyle oluşturulur ve Down sendromu duyarlılığını artırır."
        }
    ),
    make_slide(
        6,
        "Down Sendromunda (Trizomi 21) Üçlü ve Dörtlü Test Profili",
        "Biyokimyasal Parmak İzi: 'HIgh' Kuralı (hCG ve İnhibin-A Artışı)",
        """İkinci trimester maternal serum biyokimyasal belirteçleri Down sendromunda son derece karakteristik ve ezberlenmesi kolay bir patern sergiler.

**1. Belirteç Seviyeleri ve MoM Değerleri:**
• **hCG:** Belirgin olarak **YÜKSEK (~2.0 MoM)**.
• **Dimerik İnhibin-A:** Belirgin olarak **YÜKSEK (~1.8-2.0 MoM)**.
• **MSAFP:** Belirgin olarak **DÜŞÜK (~0.7 MoM)**.
• **uE3 (Östriol):** Belirgin olarak **DÜŞÜK (~0.7 MoM)**.

**2. Klinik Hatırlatıcı Mnemonic ('HIgh' Kuralı):**
• Down sendromunda **H** ve **I** harfleriyle başlayanlar **YÜKSEKTİR (HIgh)**:
  - **H** -> hCG (Yüksek)
  - **I** -> İnhibin-A (Yüksek)
• Diğer iki parametre (AFP ve uE3) ise **DÜŞÜKTÜR**.

Bu patern saptandığında fetus için Trizomi 21 riski yüksek rapor edilir. Ancak kesin tanı için mutlaka amniyosentez veya CVS ile fetal karyotipleme önerilmelidir.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN MNEMONIC", "text": "Down sendromunda 'HIgh' kuralı: hCG ve İnhibin-A YÜKSEK; AFP ve uE3 DÜŞÜKTÜR.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "İkinci trimester maternal serum taramasında AFP düşük, uE3 düşük, hCG yüksek ve İnhibin-A yüksek saptanan gebelikte en olası anöploidi Trizomi 21'dir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-006",
            "question": "16. gebelik haftasında yapılan dörtlü tarama testinde MSAFP: 0.6 MoM (düşük), uE3: 0.5 MoM (düşük), hCG: 2.3 MoM (yüksek) ve İnhibin-A: 2.1 MoM (yüksek) saptanan bir gebelikte en olası tanı hangisidir?",
            "options": [
                "A) Trizomi 18 (Edwards sendromu)",
                "B) Açık spina bifida",
                "C) Trizomi 21 (Down sendromu)",
                "D) Turner sendromu",
                "E) Fetal anensefali"
            ],
            "correctAnswer": "C",
            "explanation": "AFP ve uE3'ün düşük; hCG ve İnhibin-A'nın yüksek olması Down sendromunun (Trizomi 21) tipik dörtlü test biyokimyasal profilidir."
        }
    ),
    make_slide(
        7,
        "Edwards Sendromu (Trizomi 18) Biyokimyasal Profili",
        "Tüm Biyokimyasal Belirteçlerin Çöküşü: Trizomi 18'in Ayrımı",
        """Trizomi 18 (Edwards sendromu), ağır intrauterin gelişme geriliği, multipl konjenital anomaliler ve yüksek perinatal mortalite ile seyreden ağır bir anöploididir.

**1. Trizomi 18 Biyokimyasal Belirteç Davranışı:**
• Down sendromundan farklı olarak Trizomi 18'de maternal serum belirteçlerinin tamamında genel bir çöküş izlenir:
  - **MSAFP:** Çok düşük (<0.6 MoM)
  - **hCG:** Çok düşük (<0.3-0.5 MoM)
  - **uE3:** Çok düşük (<0.4 MoM)
  - **PAPP-A (1. trimester):** İleri derecede düşük
• **Özet Kural:** Trizomi 18'de **HER ŞEY DÜŞÜKTÜR!** (Yalnızca birinci trimesterde NT artmıştır).

**2. Tipik Ultrasonografi Bulguları:**
• Koroid pleksus kistleri, 'çilek kafa' (strawberry head) kranium anomalisi.
• Fleksiyon kontraktürleri: Üst üste binmiş parmaklar (clenched hands - 2. ve 5. parmakların 3. ve 4. üzerine binmesi).
• Ayakta rocker-bottom deformitesi (tahta at ayağı / pes planovalgus), ventriküler septal defekt ve omfalosel.""",
        [
            {"type": "clinical", "badge": "🔴 AYIRICI TANI KURALI", "text": "Down sendromunda hCG yükselirken; Edwards sendromunda (Trizomi 18) hCG, AFP ve uE3'ün tamamı belirgin şekilde DÜŞÜKTÜR.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Üçlü tarama testinde AFP, hCG ve uE3 değerlerinin her üçünün birden ileri derecede düşük bulunması Trizomi 18'i işaret eder.", "color": "sky"}
        ],
        {
            "id": "prac-pre-007",
            "question": "17. gebelik haftasında yapılan üçlü tarama testinde serum AFP düzeyi 0.4 MoM, hCG düzeyi 0.3 MoM ve uE3 düzeyi 0.3 MoM olarak rapor edilen gebelikte en kuvvetle şüphelenilmesi gereken kromozomal anöploidi hangisidir?",
            "options": [
                "A) Trizomi 21 (Down sendromu)",
                "B) Trizomi 18 (Edwards sendromu)",
                "C) Klinefelter sendromu",
                "D) 47,XXX sendromu",
                "E) Triploidi tip 1"
            ],
            "correctAnswer": "B",
            "explanation": "Üçlü testte üç belirtecin birden (AFP, hCG, uE3) belirgin şekilde düşük olması Trizomi 18 (Edwards sendromu) için patognomoniktir."
        }
    ),
    make_slide(
        8,
        "Maternal Serum Alfa-Fetoprotein (MSAFP) Yüksekliği",
        "Açık Nöral Tüp Defektleri, Karın Duvarı Defektleri ve Obstetrik Nedenler",
        """Alfa-fetoprotein (AFP), fetal karaciğer tarafından üretilen albümin benzeri majör plazma proteinidir. Fetal idrarla amniyotik sıvıya geçer ve plasenta/membranlar aracılığıyla maternal kana sızar.

**1. MSAFP Yüksekliği Tanımı (>2.0 - 2.5 MoM):**
• Normal fetusta AFP'nin maternal dolaşıma sızması son derece kısıtlıdır. Fetal cildin bütünlüğünün bozulduğu durumlarda fetal serum amniyotik sıvıya, oradan da maternal kana akar ve MSAFP aşırı yükselir.

**2. MSAFP Yüksekliğinin Başlıca Nedenleri:**
• **1. Yanlış Gebelik Haftası Hesabı:** En sık nedendir! Gebelik haftasının ultrasona göre olduğundan küçük hesaplanması (aslında daha ileri hafta olması).
• **2. Çoğul Gebelik:** İki veya daha fazla fetusun toplam üretim artışı.
• **3. Açık Nöral Tüp Defektleri (ONTD):** Anensefali (en yüksek artış), Açık Spina Bifida (meningosel, miyelomeningosel). Kapalı spina bifidada (ciltle örtülü) AFP artmaz!
• **4. Karın Duvarı Defektleri:** Gastroşizis (bağırsaklar direkt amniyona temas ettiği için AFP çok yüksek) ve Omfalosel.
• **5. Fetal Ölüm (İrauterin Eksitus):** Doku lizisi ile masif salınım.
• **6. Plasental Patolojiler:** Plasenta akreta, dekolman plasenta.""",
        [
            {"type": "clinical", "badge": "🔴 İLK YAPILACAK İŞLEM", "text": "MSAFP yüksekliği saptandığında ilk yapılması gereken basamak: Ultrasonografi ile gebelik haftasının ve fetal canlılığın doğrulanmasıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Spina bifida aperta'da (açık nöral tüp defekti) MSAFP belirgin yükselirken; spina bifida okülta'da (cilt kapalı) MSAFP normal sınırlardadır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-008",
            "question": "16. gebelik haftasında rutin taramada maternal serum alfa-fetoprotein (MSAFP) düzeyi 4.5 MoM (belirgin yüksek) olarak saptanan asemptomatik gebede hekimin atması gereken İLK adım aşağıdakilerden hangisi olmalıdır?",
            "options": [
                "A) Hemen amniyosentez planlamak",
                "B) Ayrıntılı ultrasonografi yaparak gebelik haftasını teyit etmek ve çoğul gebelik/fetal anomalileri araştırmak",
                "C) Acil gebelik terminasyonu önermek",
                "D) Maternal kanda serbest fetal DNA (NIPT) testi istemek",
                "E) Yüksek doz folik asit tedavisi başlamak"
            ],
            "correctAnswer": "B",
            "explanation": "MSAFP yüksekliğinin en sık nedeni gestasyonel yaşın yanlış hesaplanması ve çoğul gebeliktir; bu nedenle ilk basamak daima ultrasonografik değerlendirmedir."
        }
    ),
    make_slide(
        9,
        "Amniyotik Sıvıda AFP ve Asetilkolinesteraz (AChE) İncelemesi",
        "Açık Nöral Tüp Defektlerinin Kesin Biyokimyasal Tanı Yöntemi",
        """Ultrasonografide nöral tüp defektinden şüphelenilen veya açıklanamayan belirgin MSAFP yüksekliği devam eden olgularda amniyosentez ile amniyotik sıvı biyokimyası incelenir.

**1. Amniyotik Sıvı AFP (AFAFP) Düzeyi:**
• Fetal nöral dokunun açıkta olduğu anensefali ve miyelomeningosel olgularında serebrospinal sıvı doğrudan amniyon kesesine drene olur; AFAFP aşırı yükselir.
• Ancak AFAFP, fetal kan kontaminasyonunda veya karın duvarı defektlerinde de yalancı pozitif yüksek çıkabilir.

**2. Amniyotik Sıvı Asetilkolinesteraz (AChE) Analizi:**
• **AChE Testi:** Jel elektroforezi yöntemiyle incelenir.
• Asetilkolinesteraz nöronal kaynaklı spesifik bir enzimdir; normal amniyotik sıvıda kesinlikle bulunmaz.
• Amniyotik sıvıda AChE bandının pozitif saptanması, açıkta bir nöral doku olduğunu kesin olarak kanıtlar (**Açık Nöral Tüp Defekti için altın standart biyokimyasal tanı**).
• Karın duvarı defektlerinde (omfalosel, gastroşizis) AFP artsa dahi AChE elektroforezi **negatiftir** (nöronal doku yoktur).""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN STANDART AYRIM", "text": "Amniyotik sıvıda pozitif Asetilkolinesteraz (AChE) varlığı Açık Nöral Tüp Defektini karın duvarı defektlerinden kesin olarak ayıran patognomonik kanıttır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / DUS SORUSU", "text": "Maternal serum ve amniyon sıvısında yüksek AFP saptanan fetusta açık nöral tüp defektini teyit eden en özgül laboratuvar testi amniyotik sıvı jel elektroforezinde Asetilkolinesteraz varlığıdır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-009",
            "question": "Maternal serum AFP yüksekliği nedeniyle yapılan amniyosentezde amniyotik sıvı alfa-fetoprotein düzeyi yüksek bulunan bir fetusta, açık nöral tüp defektini (spina bifida aperta) omfalosel gibi diğer defektlerden kesin olarak ayıran spesifik test hangisidir?",
            "options": [
                "A) Amniyotik sıvı total protein düzeyi",
                "B) Amniyotik sıvı jel elektroforezinde Asetilkolinesteraz (AChE) varlığı",
                "C) Amniyotik sıvı glukoz konsantrasyonu",
                "D) Amniyotik sıvı karyotip analizi",
                "E) Fetal eritrosit sayısı"
            ],
            "correctAnswer": "B",
            "explanation": "Asetilkolinesteraz nöral dokuya özgüdür; açık nöral defektinde amniyotik sıvıya geçer ve elektroforezde pozitif bant vermesi tanıyı kesinleştirir."
        }
    ),
    make_slide(
        10,
        "Hücresiz Fetal DNA (Cell-free Fetal DNA - cffDNA / NIPT)",
        "Maternal Plazma Trofoblast DNA'sı, Fetal Fraksiyon ve Yeni Nesil Dizileme",
        """Hücresiz fetal DNA (cffDNA) taraması (Non-İnvaziv Prenatal Test - NIPT), maternal periferik kanda dolaşan serbest DNA parçacıklarının yeni nesil dizileme (NGS) teknolojileriyle analiz edilmesine dayanan devrim niteliğinde bir tarama testidir.

**1. Biyolojik Köken ve Dinamikler:**
• Maternal kanda dolaşan serbest DNA'nın yaklaşık **%10-15'i fetusa (daha doğrusu plasental sinsityotrofoblastların apoptozuna)** aittir. Geri kalanı anaya aittir.
• Gebeliğin **10. haftasından itibaren** maternal kanda tespit edilebilir seviyeye ulaşır.
• Yarı ömrü çok kısadır (dakikalar-saatler); doğumdan sonra 1-2 gün içinde maternal kandan tamamen temizlenir (önceki gebeliklerden kalıntı DNA kalmaz).

**2. Klinik Performans:**
• Trizomi 21 (Down sendromu) için saptama duyarlılığı **>%99**, yalancı pozitiflik oranı ise **<%0.1**'dir.
• Trizomi 18 ve Trizomi 13 için duyarlılık sırasıyla %97 ve %90 civarındadır.
• Cinsiyet tespiti ve Rh uygunsuzluğunda fetal RhD genotiplendirmesinde mükemmel doğruluk sağlar.""",
        [
            {"type": "clinical", "badge": "🔴 PLASENTAL KÖKEN GERÇEĞİ", "text": "Dolaşımdaki fetal DNA doğrudan fetusun kendisinden değil plasental sinsityotrofoblastlardan kaynaklanır; bu nedenle plasental mozaisizm yanıltabilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Maternal kanda serbest fetal DNA (cffDNA) gebeliğin en erken 10. haftasından itibaren güvenle test edilebilir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-010",
            "question": "Maternal kanda serbest dolaşan hücre dışı fetal DNA (cffDNA) analizi ile ilgili aşağıdaki ifadelerden hangisi BİYOLOJİK OLARAK YANLIŞTIR?",
            "options": [
                "A) Dolaşımdaki cffDNA'nın ana kaynağı plasental trofoblastik apoptozdur.",
                "B) Doğumdan sonra aylarca maternal plazmada sebat eder ve sonraki gebelikleri yanıltır.",
                "C) Gebeliğin 10. haftasından itibaren test edilebilir düzeye ulaşır.",
                "D) Down sendromu için saptama duyarlılığı %99'un üzerindedir.",
                "E) Fetal fraksiyonun %4'ün altında olması testin başarısız sonuçlanmasına yol açar."
            ],
            "correctAnswer": "B",
            "explanation": "cffDNA'nın maternal plazmadaki yarı ömrü dakikalar düzeyindedir ve doğumdan sonraki saatler içinde tamamen temizlenir; sonraki gebeliklere asla kalmaz."
        }
    ),
    make_slide(
        11,
        "NIPT'nin Sınırlılıkları, Fetal Fraksiyon ve Yalancı Sonuç Nedenleri",
        "Düşük Fetal Fraksiyon, Kısıtlı Plasental Mozaisizm ve Vanishing Twin Tuzakları",
        """NIPT mükemmel bir tarama performansı sunsa da kesin tanı koydurmaz; tarama testi niteliğini korur.

**1. Fetal Fraksiyon (FF) Kavramı ve Başarısız Testler:**
• Maternal kanda toplam serbest DNA içindeki fetal DNA oranıdır. Güvenilir bir test sonucu için FF'nin **en az %4** olması şarttır.
• **Düşük Fetal Fraksiyon Nedenleri:** Aşırı maternal obezite (maternal plazma volümü ve adipozit parçalanması artar, fetal oran düşer), erken gebelik haftası (<10. hafta), heparin/enoksaparin kullanımı ve fetal anöploidiler (özellikle Trizomi 18 ve Trizomi 13'te plasenta küçük olduğu için FF düşüktür).

**2. Yalancı Pozitif ve Yalancı Negatiflik Nedenleri:**
• **Kısıtlı Plasental Mozaisizm (CPM):** Anöploidi sadece plasentada sınırlıdır, fetus tamamen öploidtir. NIPT pozitif çıkar ama fetus sağlıklıdır!
• **Kaybolan İkiz (Vanishing Twin):** Erken haftada ölen anöploid ikiz eşinin plasentasından haftalarca maternal kana DNA dökülmeye devam eder.
• **Maternal Biyoloji:** Annede bilinmeyen mozaik Turner (45,X/46,XX), benign/malign maternal tümörler veya maternal kopya sayısı varyasyonları.""",
        [
            {"type": "clinical", "badge": "🔴 KESİN TANI İLKESİ", "text": "NIPT sonucu 'yüksek risk' gelen hiçbir gebelik bu sonuca dayanılarak termine edilemez; mutlaka CVS veya amniyosentezle invaziv tanı teyidi yapılmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE / TUS SORUSU", "text": "NIPT testinde yalancı pozitifliğin en sık biyolojik nedenleri kısıtlı plasental mozaisizm (CPM) ve kaybolan ikiz (vanishing twin) sendromudur.", "color": "sky"}
        ],
        {
            "id": "prac-pre-011",
            "question": "32 yaşında primigravid gebede 11. haftada yapılan NIPT testinde Trizomi 21 riski yüksek (>%99) olarak rapor ediliyor. Ultrasonografide fetusta herhangi bir majör anomali saptanmıyor. Bu aşamada hastaya verilmesi gereken en doğru tıbbi yaklaşım hangisidir?",
            "options": [
                "A) NIPT kesin tanı koydurur, gebelik derhal sonlandırılmalıdır.",
                "B) NIPT bir tarama testidir; sonuç amniyosentez veya CVS ile invaziv olarak teyit edilmelidir.",
                "C) Test geçersizdir, ikinci trimesterde üçlü tarama testi yapılmalıdır.",
                "D) Bir ay sonra NIPT testi tekrarlanmalıdır.",
                "E) Fetal biyopsi yapılmadan gebeye profilaktik kemoterapi verilmelidir."
            ],
            "correctAnswer": "B",
            "explanation": "NIPT ne kadar yüksek duyarlılığa sahip olursa olsun bir tarama testidir; plasental mozaisizm gibi nedenlerle yalancı pozitiflik olabileceğinden invaziv tanı (CVS/Amniyosentez) şarttır."
        }
    ),
    make_slide(
        12,
        "İnvaziv Prenatal Tanı Yöntemlerine Genel Bakış ve Risk Dengesi",
        "Karyotiplemenin Altın Standardı, İşlemle İlgili Fetal Kayıp Oranları ve Rh İmmünizasyonu",
        """İnvaziv prenatal tanı yöntemleri; fetal doku veya hücrelerin (trofoblast, amniyosit, fetal eritrosit/lenfosit) doğrudan uterin kaviteden örneklenerek sitogenetik, moleküler veya biyokimyasal analiz yapılmasını sağlar.

**1. Başlıca İnvaziv Yöntemler ve Zamanlamaları:**
• **Koryon Villus Örneklemesi (CVS):** 10 hafta 0 gün ile 13 hafta 6 gün arasında (1. Trimester).
• **Amniyosentez:** 15 ile 20. gebelik haftaları arasında (2. Trimester).
• **Kordosentez (PUBS):** ≥18-20. gebelik haftalarından itibaren doğuma kadar.

**2. İşlem Riski ve Güncel Kanıtlar:**
• Tarihsel kaynaklarda %1-2 olarak bildirilen işleme bağlı gebelik kaybı (düşük) riski, modern yüksek çözünürlüklü gerçek zamanlı ultrasonografi kılavuzluğunda deneyimli ellerde **<%0.1-0.2 (1/500 - 1/1000)** düzeyine gerilemiştir.
• **Rh Uygunsuzluğu Yönetimi:** Anne Rh(-), baba Rh(+) ise fetomaternal kanama riski nedeniyle işlemden sonraki ilk 72 saat içinde anneye mutlaka **300 mcg Anti-D İmmünglobulin (Rhogam)** enjeksiyonu yapılmalıdır.""",
        [
            {"type": "clinical", "badge": "🔴 RH İMMÜNİZASYON KURALI", "text": "Rh-negatif gebelerde invaziv işlem (CVS, amniyosentez, kordosentez) sonrasında maternal izoimmünizasyonu önlemek için profilaktik Anti-D Ig zorunludur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "İnvaziv prenatal testlerin uygulama sıralaması: En erken CVS (10-13 hafta) -> Amniyosentez (15-20 hafta) -> Kordosentezdir (≥18-20 hafta).", "color": "sky"}
        ],
        {
            "id": "prac-pre-012",
            "question": "A Rh negatif kan grubuna sahip bir gebenin prenatal sitogenetik inceleme amacıyla amniyosentez işlemi tamamlandıktan hemen sonra maternal izoimmünizasyonu engellemek için yapılması gereken standart uygulama hangisidir?",
            "options": [
                "A) Anneye profilaktik geniş spektrumlu antibiyotik başlanması",
                "B) İlk 72 saat içinde intramüsküler Anti-D immünglobulin uygulanması",
                "C) Anneye yüksek doz intravenöz kortikosteroid verilmesi",
                "D) Fetal kan grubunun doğum anına kadar beklenmesi",
                "E) Fetal transfizyon yapılması"
            ],
            "correctAnswer": "B",
            "explanation": "Rh-negatif duyarlanmamış gebelerde invaziv girişim sonrasında fetomaternal kanamaya bağlı sensitizasyonu önlemek için ilk 72 saatte Anti-D immünglobulin uygulanır."
        }
    ),
    make_slide(
        13,
        "Koryon Villus Örneklemesi (CVS) Endikasyonları ve Tekniği",
        "10-13+6. Haftalar, Transabdominal ve Transservikal Yaklaşım, Erken Tanı Avantajı",
        """Koryon villus örneklemesi (CVS), birinci trimesterde plasentanın fetal komponenti olan koryon frondozumdan trofoblastik doku biyopsisidir.

**1. Uygulama Detayları:**
• **Optimal Zamanlama:** 10 hafta 0 gün ile 13 hafta 6 gün arasıdır. 10. haftadan önce **asla yapılmamalıdır!** (Transvers uzuv amputasyonları ve oromandibular malformasyon riski nedeniyle).
• **Girişim Yolları:**
  - **Transabdominal:** Plasenta fundus veya anterior yerleşimli olduğunda tercih edilir; 18-20G iğne ile USG eşliğinde girilir.
  - **Transservikal:** Plasenta posterior yerleşimli olduğunda steril polietilen kateter ve mandrenle servikal kanaldan girilerek aspire edilir.

**2. Başlıca Avantajları:**
• En büyük üstünlüğü **erken tanı** sağlamasıdır. Sonuçlar gebeliğin 11-12. haftasında çıkar. Anöploidi veya ölümcül tek gen hastalığı saptanırsa gebelik birinci trimesterde daha güvenli, cerrahi ve psikolojik komplikasyonu az olan küretaj yöntemiyle sonlandırılabilir.""",
        [
            {"type": "clinical", "badge": "🔴 10. HAFTA TABUSU", "text": "CVS 10. haftadan önce yapılırsa fetal ekstremite amputasyonu ve mikrognatiye (oromandibular limb hipogenezi) neden olur; 10. haftadan önce KONTRENDİKEDİR.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Birinci trimesterde fetal karyotipi ve tek gen hastalıklarını en erken dönemde belirleyen invaziv prenatal tanı yöntemi Koryon Villus Örneklemesidir (CVS).", "color": "sky"}
        ],
        {
            "id": "prac-pre-013",
            "question": "Ailesinde kistik fibrozis mutasyonu taşıyıcılığı olan ve birinci trimesterde fetusun etkilenip etkilenmediğini en erken dönemde kesin olarak öğrenmek isteyen 11 haftalık gebeye önerilmesi gereken en uygun invaziv prenatal tanı yöntemi hangisidir?",
            "options": [
                "A) Amniyosentez",
                "B) Kordosentez",
                "C) Koryon villus örneklemesi (CVS)",
                "D) Fetal cilt biyopsisi",
                "E) Fetoskopi"
            ],
            "correctAnswer": "C",
            "explanation": "10-13. gebelik haftalarında fetal DNA elde ederek en erken kesin sitogenetik ve moleküler tanı sağlayan yöntem Koryon Villus Örneklemesidir (CVS)."
        }
    ),
    make_slide(
        14,
        "CVS'de Kısıtlı Plasental Mozaisizm (CPM) Tuzakları",
        "Sitotrofoblast ve Mezenkimal Kor Ayrımı, Tip 1-2-3 CPM ve Amniyosentezle Teyit",
        """CVS'nin en önemli sitogenetik açmazı, örneklenen dokunun doğrudan fetusun kendisi değil trofoblastik plasenta dokusu olmasıdır. Bu durum vakaların %1-2'sinde Kısıtlı Plasental Mozaisizm (Confined Placental Mosaicism - CPM) tablosuna yol açar.

**1. Hücre Hatları ve İnceleme Yöntemleri:**
• **Direkt Preparat (Kısa Dönem):** Bölünmekte olan sitotrofoblastları yansıtır.
• **Kültür Preparatı (Uzun Dönem):** Villus mezenkimal kor hücrelerini yansıtır.

**2. CPM Tipleri ve Klinik Önemi:**
• **Tip 1 CPM:** Mozaisizm sadece sitotrofoblastlardadır.
• **Tip 2 CPM:** Mozaisizm sadece villus stromasındadır (mezenkim).
• **Tip 3 CPM:** Hem sitotrofoblastta hem de villus mezenkiminde mozaik anöploidi vardır, ancak **fetus tamamen öploid ve normaldir**.
• **Yönetim:** CVS'de mozaik bir anöploidi saptandığında, bu anöploidinin fetusa mı yoksa sadece plasentaya mı ait olduğunu anlamak için **16. haftada AMNİYOSENTEZ yapılması şarttır!** Fetal amniyositler embriyo epiblastından köken aldığı için gerçek fetal durumu yansıtır.""",
        [
            {"type": "clinical", "badge": "🔴 MOZAİSİZM PROTOKOLÜ", "text": "CVS sonucunda mozaik kromozom anomalisi çıktığında gebelik sonlandırılmaz; gerçek fetal durumu görmek için amniyosentez yapılarak teyit edilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 AKADEMİK SORU", "text": "CVS'de saptanan kısıtlı plasental mozaisizmin fetusa yansıyıp yansımadığını doğrulamada tercih edilen tanı yöntemi amniyosentezdir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-014",
            "question": "11. haftada ileri anne yaşı nedeniyle yapılan CVS analizinde hücrelerin %30'unda Trizomi 18, %70'inde normal 46,XX saptanan (mozaisizm) bir gebelikte, bu durumun kısıtlı plasental mozaisizm (CPM) olup olmadığını teyit etmek için yapılması gereken en doğru basamak hangisidir?",
            "options": [
                "A) Hemen gebeliğin sonlandırılması",
                "B) 16. haftada amniyosentez yapılarak gerçek fetal amniyositlerin incelenmesi",
                "C) Hemen ikinci bir CVS tekrarlanması",
                "D) Maternal kanda serbest fetal DNA bakılması",
                "E) Üçüncü trimesterde kordosentez beklenmesi"
            ],
            "correctAnswer": "B",
            "explanation": "CVS'de saptanan mozaisizmin fetusu etkileyip etkilemediği amniyosentez ile netleştirilir; çünkü amniyosentez hücreleri doğrudan fetal ektoderm ve endodermden dökülür."
        }
    ),
    make_slide(
        15,
        "Amniyosentez: Uygulama Zamanı, Tekniği ve Altın Standart Rolü",
        "15-20. Haftalar, Amniyotik Sıvı Aspirasyonu, Amniyosit Kültürü ve Güvenilirlik",
        """Amniyosentez, ultrasonografi kılavuzluğunda ince bir spinal iğne ile amniyon kesesine girilerek amniyotik sıvı ve içinde bulunan deskuame fetal hücrelerin (amniyositlerin) aspire edilmesidir.

**1. Teknik Detaylar ve Zamanlama:**
• **Uygulama Zamanı:** 15 hafta 0 gün ile 20 hafta 0 gün arasıdır (en sık 16-18. haftalar).
• **Teknik:** Sürekli gerçek zamanlı USG altında, fetustan ve plasental kord insersiyonundan uzak bir sıvı cebine 20-22G iğne ile girilir.
• **Miktar:** İlk 2 ml aspire edilen sıvı maternal hücre kontaminasyonu riski nedeniyle atılır; ardından sitogenetik ve biyokimyasal analizler için **15-20 ml berrak sıvı** aspire edilir. Fetus bu sıvıyı birkaç saat içinde fetal idrarla yeniler.

**2. Avantajları ve Kısıtlılıkları:**
• Fetal deri, solunum ve üriner epitelden dökülen gerçek fetal hücreler incelendiği için kısıtlı plasental mozaisizm tuzağı yaşanmaz; sitogenetik doğruluğu **>%99.5**'tir.
• Kısıtlılığı: Hücrelerin in vitro kültürde pasajlanması gerektiğinden konvansiyonel karyotip sonucunun çıkması **10-14 gün (1-2 hafta)** sürer.""",
        [
            {"type": "clinical", "badge": "🔴 MATERNAL KONTAMİNASYON ÖNLEMİ", "text": "Amniyosentezde aspire edilen ilk 1-2 ml sıvı maternal doku bulaşması (desidua) riski nedeniyle dökülür; analize sonraki sıvı verilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Konvansiyonel sitogenetikte gerçek fetal hücreleri örneklemesi nedeniyle fetal kromozom anomalisi tanısında altın standart yöntem ikinci trimester amniyosentezdir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-015",
            "question": "Amniyosentez işlemi sırasında maternal hücre kontaminasyonu riskini en aza indirmek amacıyla standart olarak uygulanan teknik yaklaşım hangisidir?",
            "options": [
                "A) İşleme başlamadan önce maternal koldan kan alınması",
                "B) İğne girdikten sonra aspire edilen ilk 1-2 ml amniyotik sıvının atılması",
                "C) Mutlaka genel anestezi altında yapılması",
                "D) Yalnızca transservikal kateter kullanılması",
                "E) 10 ml'den fazla sıvı aspire edilmemesi"
            ],
            "correctAnswer": "B",
            "explanation": "İğnenin karın duvarı ve myometriumu geçerken maternal hücreleri lümene çekme riskine karşı aspire edilen ilk 1-2 ml sıvı atılır, devamı kültüre gönderilir."
        }
    ),
    make_slide(
        16,
        "Erken Amniyosentez Neden Önerilmez? (<15. Hafta)",
        "Amniyon-Koryon Füzyon Yokluğu, Pes Ekinovarus ve Fetal Kayıp Riskleri",
        """Geçmiş yıllarda koryon villus örneklemesine alternatif olarak gebeliğin 11-14. haftalarında 'Erken Amniyosentez' uygulanması denenmiş, ancak yapılan geniş randomize çalışmalar sonucunda terk edilmiştir.

**1. Erken Amniyosentezin Başlıca Komplikasyonları:**
• **1. Pes Ekinovarus (Talipes Equinovarus / Yumru Ayak):** Erken haftalarda amniyon sıvısının çekilmesi oligohidramniyosa yol açar ve intrauterin bası nedeniyle fetusta yumru ayak (pes ekinovarus) deformitesi sıklığı kontrol grubuna göre 10 kat artar.
• **2. Amniyon-Koryon Füzyonunun Tamamlanmamış Olması:** 14-15. haftaya kadar amniyon zarı ile koryon zarı henüz birbirine tam yapışmamıştır (fizyolojik korioamniyotik ayrılma). İğne girişi sırasında membranların çadırlaşması (tenting) ve yırtılması riski çok yüksektir.
• **3. Yüksek Fetal Kayıp Oranı:** Gebelik kaybı oranı standart amniyosenteze göre belirgin şekilde yüksektir (%2-3).
• **4. Kültür Başarısızlığı:** Erken haftalarda amniyotik sıvıdaki canlı fetal hücre sayısı az olduğundan hücre kültürü başarısızlığı sıktır.""",
        [
            {"type": "clinical", "badge": "🔴 KESİN BİLGİ", "text": "Erken amniyosentez (<15. hafta) fetusta pes ekinovarus (yumru ayak) riskini artırdığı için güncel perinatolojide kesinlikle terk edilmiştir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "15. haftadan önce yapılan erken amniyosentezin en karakteristik fetal ortopedik komplikasyonu talipes ekinovarustur (pes ekinovarus).", "color": "sky"}
        ],
        {
            "id": "prac-pre-016",
            "question": "15. gebelik haftasından önce yapılan 'erken amniyosentez' girişiminin günümüzde terk edilmesinin ve önerilmemesinin en önemli nedeni olan spesifik fetal anomali hangisidir?",
            "options": [
                "A) Ventriküler septal defekt",
                "B) Talipes ekinovarus (pes ekinovarus / yumru ayak)",
                "C) Kraniyosinostozis",
                "D) Duodenal atrezi",
                "E) Radial agenezi"
            ],
            "correctAnswer": "B",
            "explanation": "Erken amniyosentezde sıvı kaybına bağlı bası etkisiyle fetal ayaklarda talipes ekinovarus (yumru ayak) gelişme riski dramatik şekilde artmaktadır."
        }
    ),
    make_slide(
        17,
        "Kordosentez (Perkütan Umbilikal Kan Örneklemesi - PUBS)",
        "≥18-20. Haftalar, Umbilikal Ven Ponksiyonu, Fetal Kan Gazı, Anemi ve Hızlı Karyotip",
        """Kordosentez (PUBS), ultrasonografi eşliğinde umbilikal kordondan doğrudan fetal kan örneği alınması veya fetusa damar içi kan/ilaç transfüzyonu yapılması işlemidir.

**1. Teknik Özellikler ve Zamanlama:**
• Kord damarları yeterli lümene ulaştığı için genellikle **≥18-20. gebelik haftalarından sonra** uygulanabilir.
• İğne tercihen umbilikal kordun plasentaya giriş yerine (insersiyon bölgesi) yakın ve sabit olan **umbilikal vene** yönlendirilir.
• Alınan kanın fetal kana ait olduğu, maternal eritrositlerden ayırt edilmek üzere **Kleihauer-Betke testi** veya eritrosit MCV analizi ile anında doğrulanır.

**2. Başlıca Endikasyonları:**
• **Fetal Anemi Tanı ve Tedavisi:** Rh izoimmünizasyonu veya Parvovirüs B19 enfeksiyonuna bağlı hidrops fetalis gelişen olgularda hematokrit tayini ve **intrauterin intravasküler kan transfüzyonu**.
• **Acil Hızlı Karyotipleme:** Geç saptanan fetal anomalilerde fetal lenfositler fitohemaglütininle uyarılarak **48-72 saat içinde metafaz analizi** elde edilir.
• Fetal trombositopeni ve konjenital enfeksiyon serolojisi.""",
        [
            {"type": "clinical", "badge": "🔴 FETAL ANEMİDE HAYAT KURTARICI", "text": "Kordosentez yalnızca tanı yöntemi değildir; ağır fetal anemide umbilikal ven yoluyla intrauterin kan transfüzyonu hayat kurtarır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ KOMİTE SORUSU", "text": "Kordosentezde kan örneği tercihen plasental kord insersiyonuna yakın bölgeden ve UMBİLİKAL VEN'den aspire edilir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-017",
            "question": "24. gebelik haftasında saptanan multipl anomalili bir fetusta gebelik terminasyonu yasal sınırına yaklaşılması nedeniyle 48-72 saat içinde en hızlı sitogenetik karyotip sonucuna ulaşmak için hangi yöntem tercih edilmelidir?",
            "options": [
                "A) İkinci trimester amniyosentezi",
                "B) Maternal kanda serbest fetal DNA",
                "C) Kordosentez (Fetal lenfosit kültürü)",
                "D) Koryon villus örneklemesi",
                "E) Fetal idrar aspirasyonu"
            ],
            "correctAnswer": "C",
            "explanation": "Kordosentez ile elde edilen fetal lenfositler hızla bölünmeye girer ve 48-72 saat içinde tam metafaz karyotipi verir; amniyosentez ise 10-14 gün sürer."
        }
    ),
    make_slide(
        18,
        "Konvansiyonel Sitogenetik (Karyotipleme) ve G-Bantlama",
        "Metafaz Kromozomları, 400-550 Bant Çözünürlük ve Yapısal/Sayısal Anomaliler",
        """Konvansiyonel karyotip analizi, hücrelerin bölünme fazında metafazda durdurularak Giemsa boyası ile boyanması (G-bantlama) ve mikroskop altında tek tek homolog çiftler halinde incelenmesidir.

**1. Analiz Prensibi:**
• Amniyositler veya fetal lenfositler in vitro kültüre ekilir.
• Mitozu metafazda durdurmak için mikrotübül inhibitörü olan **kolşisin (veya kolsemid)** eklenir.
• Hipotonik solüsyonla hücreler şişirilir, fikse edilir ve Giemsa ile boyanır.
• Kromozomların heterokromatin (koyu) ve ökromatin (açık) bantları analiz edilir.

**2. Tanı Gücü ve Sınırları:**
• **Saptayabildikleri:** Sayısal anomaliler (trizomiler, monozomiler, poliploidiler) ve **dengeli/dengesiz yapısal kromozom yeniden düzenlenmeleri** (resiprokal translokasyonlar, Robertsonyan translokasyonlar, inversiyonlar).
• **Saptayamadıkları:** Optik mikroskop çözünürlüğü **5-10 megabaz (Mb)** altındaki submikroskopik delesyonları ve tek gen mutasyonlarını göremez.""",
        [
            {"type": "clinical", "badge": "🔴 DENGELİ TRANSLOKASYON ÜSTÜNLÜĞÜ", "text": "Karyotip, dengeli translokasyonları ve inversiyonları tespit edebilen altın standarttır; mikrodizi (CMA) dengeli translokasyonları göremez!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Hücre kültüründe metafaz plağı elde etmek ve mitozu durdurmak amacıyla tübülini bağlayan kolşisin (kolsemid) kullanılır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-018",
            "question": "Amniyosentez materyalinden yapılan sitogenetik incelemede fetal hücrelerin mitoz bölünmesini metafaz evresinde durdurarak kromozomların morfolojik analizine olanak tanıyan kimyasal ajan hangisidir?",
            "options": [
                "A) Kolşisin (Kolsemid)",
                "B) Fitohemaglütinin",
                "C) Sitokalasin B",
                "D) Penisilin-Streptomisin",
                "E) Metotreksat"
            ],
            "correctAnswer": "A",
            "explanation": "Kolşisin (veya kolsemid), mikrotübül polimerizasyonunu engelleyerek hücrelerin anafaza geçmesini durdurur ve kromozomları metafazda hapseder."
        }
    ),
    make_slide(
        19,
        "Hızlı Anöploidi Taraması: QF-PCR ve FISH",
        "Kültürsüz 24-48 Saatte Sonuç: 13, 18, 21, X ve Y Kromozomlarının Hızlı Analizi",
        """Konvansiyonel hücre kültürünün 1-2 hafta sürmesi, ebeveynlerde ciddi anksiyeteye ve yasal terminasyon sürelerinin daralmasına yol açar. Bu nedenle kültür gerektirmeyen hızlı moleküler sitogenetik yöntemler geliştirilmiştir.

**1. Floresan İn Situ Hibridizasyon (FISH):**
• Bölünmeyen interfaz hücre çekirdeklerine spesifik kromozom bölgelerini (13, 18, 21, X, Y) hedefleyen floresan boyalı DNA probları hibridize edilir.
• Floresan mikroskobunda çekirdek içindeki floresan sinyal sayısı sayılır (örneğin 3 adet 21 sinyali = Trizomi 21).

**2. Kantitatif Floresan PCR (QF-PCR):**
• Günümüzde FISH'in yerini alan en yaygın yöntemdir.
• 13, 18, 21, X ve Y kromozomlarına özgü yüksek polimorfik **kısa ardışık tekrar (STR / mikrosatellit)** bölgeleri floresan primerlerle çoğaltılır.
• Kapiller elektroforezde pik alanları ve oranları hesaplanır. Normal diploid bireyde 1:1 pik oranı görülürken, trizomide 1:1:1 üç pik veya 2:1 çift doz piki izlenir.
• **En Büyük Üstünlüğü:** 24-48 saatte kesin anöploidi tanısı koyar ve maternal kan kontaminasyonunu kolayca deşifre eder.""",
        [
            {"type": "clinical", "badge": "🔴 HIZLI ANÖPLOİDİ KURTARICISI", "text": "QF-PCR ve FISH kültür gerektirmez; 24-48 saat içinde Down, Edwards, Patau ve Turner anomalilerini saptar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Amniyosentez sıvısından kültür yapmadan 24-48 saatte en sık görülen trizomileri (13, 18, 21) mikrosatellit STR analiziyle saptayan yöntem QF-PCR'dır.", "color": "sky"}
        ],
        {
            "id": "prac-pre-019",
            "question": "Amniyosentez yapılan bir gebede hücre kültürünü beklemeden 24 saat içinde 13, 18, 21, X ve Y kromozomlarına ait sayısal anöploidileri polimorfik STR belirteçleri ile hızlıca analiz eden moleküler test hangisidir?",
            "options": [
                "A) QF-PCR (Kantitatif Floresan PCR)",
                "B) Western Blot",
                "C) Sanger dizileme",
                "D) Northern Blot",
                "E) RFLP analizi"
            ],
            "correctAnswer": "A",
            "explanation": "QF-PCR, kültür gerektirmeksizin 13, 18, 21, X ve Y anöploidilerini STR lokusları üzerinden 24-48 saat içinde kantitatif olarak saptar."
        }
    ),
    make_slide(
        20,
        "Kromozomal Mikrodizi Analizi (CMA / Array-CGH)",
        "Submikroskopik Kopya Sayısı Varyasyonları (CNV) ve Yapısal Fetal Anomalilerde Rolü",
        """Kromozomal Mikrodizi Analizi (Chromosomal Microarray Analysis - CMA) veya Karşılaştırmalı Genomik Hibridizasyon (Array-CGH), tüm insan genomunu submikroskopik düzeyde (<50-100 kilobaz) tarayabilen yüksek çözünürlüklü moleküler sitogenetik platformdur.

**1. Çalışma Prensibi:**
• Fetal DNA ve referans normal kontrol DNA'sı farklı floresan boyalarla (örneğin kırmızı ve yeşil) işaretlenir.
• Yüz binlerce spesifik oligonükleotit prob içeren çip üzerine hibridize edilir.
• Renk yoğunluk oranlarından fetal DNA'daki **Kopya Sayısı Varyasyonları (Copy Number Variations - CNV)** yani mikrodelesyonlar ve mikroduplikasyonlar belirlenir.

**2. Klinik Endikasyonlar ve Üstünlükleri:**
• Ultrasonografide majör yapısal anomali saptanan fetuslarda konvansiyonel karyotip normal olsa dahi olguların **%6-7'sinde klinik anlamlı patojenik CNV (mikrodelesyon/duplikasyon)** saptar.
• 22q11.2 delesyonu (DiGeorge sendromu), 1p36 delesyonu, Williams sendromu ve Angelman/Prader-Willi gibi optik mikroskopla görülemeyen mikrodelesyonları net olarak yakalar.
• **En Önemli Kısıtlılığı:** Genetik materyal kaybı veya kazancı olmayan **dengeli translokasyonları ve inversiyonları SAPTAYAMAZ!**""",
        [
            {"type": "clinical", "badge": "🔴 BİRİNCİ BASAMAK TANI TESTİ", "text": "Ultrasonografide fetal yapısal anomali saptandığında güncel kılavuzlara göre ilk basamakta önerilen genetik test Mikrodizi Analizidir (CMA).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VE YANDAL", "text": "Array-CGH mikrodelesyonları ve kopya sayısı artışlarını mükemmel saptar; ancak dengeli resiprokal translokasyonları ve inversiyonları KESİNLİKLE saptayamaz.", "color": "sky"}
        ],
        {
            "id": "prac-pre-020",
            "question": "Fetal ultrasonografide ventriküler septal defekt, timus hipoplazisi ve konotrunkal kalp anomalisi saptanan bir fetusta 22q11.2 mikrodelesyonunu (DiGeorge sendromu) en yüksek doğrulukla saptayabilen genetik test yöntemi hangisidir?",
            "options": [
                "A) Standart G-bant karyotip analizi",
                "B) Kromozomal mikrodizi analizi (CMA / Array-CGH)",
                "C) Hemoglobin elektroforezi",
                "D) Üçlü tarama testi",
                "E) Maternal kanda AFP bakılması"
            ],
            "correctAnswer": "B",
            "explanation": "22q11.2 delesyonu submikroskopiktir ve standart karyotipte gözden kaçabilir; submikroskopik CNV'leri saptamada Array-CGH (CMA) altın standarttır."
        }
    ),
    make_slide(
        21,
        "Preimplantasyon Genetik Tanı (PGT-A, PGT-M, PGT-SR)",
        "Trofektoderm Biyopsisi, Blastokist Evresi, Tek Gen Hastalıkları ve Translokasyonlar",
        """Preimplantasyon Genetik Testleme (PGT), yardımcı üreme teknikleri (İn Vitro Fertilizasyon - IVF) ile elde edilen embriyoların uterusa transfer edilmeden önce genetik olarak incelenmesidir.

**1. Biyopsi Evresi ve Tekniği:**
• Günümüzde standart yaklaşım **5. gün Blastokist evresinde Trofektoderm Biyopsisidir**.
• İç hücre kitlesine (fetusu oluşturacak embriyoblast) dokunulmadan, plasentayı oluşturacak trofektoderm tabakasından 5-8 adet hücre lazer yardımıyla aspire edilir. Embriyoya zarar verme riski son derece düşüktür.

**2. PGT Kategorileri:**
• **PGT-A (Aneuploidy):** İleri anne yaşı veya tekrarlayan IVF başarısızlığında sayısal kromozom anöploidilerini taramak için yapılır.
• **PGT-M (Monogenic/Single Gene Defects):** Ebeveynlerin taşıdığı bilinen tek gen hastalıklarının (Kistik Fibrozis, Spinal Müsküler Atrofi-SMA, Orak Hücreli Anemi, Huntington) embriyoda araştırılmasıdır.
• **PGT-SR (Structural Rearrangements):** Ebeveynlerden birinde dengeli resiprokal veya Robertsonyan translokasyon varlığında dengesiz embriyoları dışlamak için uygulanır.""",
        [
            {"type": "clinical", "badge": "🔴 EMBRİYONUN KORUNMASI", "text": "Blastokist evresi trofektoderm biyopsisinde iç hücre kitlesine (fetal taslak) dokunulmaz; yalnızca gelecekteki trofoblast hücreleri örneklenir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "SMA veya Talasemi taşıyıcısı çiftlerde sağlıklı embriyonun seçilerek transfer edilmesini sağlayan preimplantasyon yöntemi PGT-M'dir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-021",
            "question": "Her ikisi de Spinal Müsküler Atrofi (SMA) taşıyıcısı olan bir çiftin sağlıklı çocuk sahibi olabilmesi amacıyla tüp bebek sürecinde embriyoların tek gen hastalığı açısından taranması hangi PGT kategorisine girer?",
            "options": [
                "A) PGT-A",
                "B) PGT-M",
                "C) PGT-SR",
                "D) NIPT",
                "E) FISH"
            ],
            "correctAnswer": "B",
            "explanation": "Monogenik (tek gen) kalıtsal hastalıkların embriyo transferi öncesinde taranması PGT-M (Preimplantation Genetic Testing for Monogenic defects) olarak adlandırılır."
        }
    ),
    make_slide(
        22,
        "Konjenital Fetal Enfeksiyonların Prenatal Tanısı (TORCH)",
        "Sitomegalovirüs, Tokzoplazma, Parvovirüs B19: Maternal Seroloji ve Amniyotik PCR",
        """Gebelikte geçirilen primer maternal enfeksiyonlar vertikal yolla fetusa geçerek konjenital enfeksiyon sendromlarına yol açabilir.

**1. Maternal Serolojik Yaklaşım:**
• Şüpheli maternal enfeksiyonda kanda IgM ve IgG bakılır. IgM pozitifliği tek başına akut enfeksiyonu kanıtlamaz (yalancı pozitiflik veya persistan IgM olabilir).
• **IgG Avidite Testi:** Yüksek avidite, enfeksiyonun en az 3-4 ay önce geçirildiğini gösterir ve erken gebelikteki primer enfeksiyon şüphesini ekarte ettirir. Düşük avidite ise yakın zamanda geçirilmiş primer enfeksiyonu destekler.

**2. Fetal Enfeksiyonun Kesin Tanısı:**
• Altın standart, **amniyosentez ile amniyotik sıvıda viral/paraziter DNA'nın PCR ile gösterilmesidir**.
• **Zamanlama Kuralı:** Amniyosentez, maternal primer enfeksiyonun üzerinden **en az 6-8 hafta geçtikten sonra** ve **fetal 21. gebelik haftasından sonra** yapılmalıdır! (Fetal böbreklerin olgunlaşıp virüsü idrarla amniyotik sıvıya atabilmesi için bu süre zorunludur; erken yapılırsa yalancı negatif çıkar).

**3. Parvovirüs B19 ve Fetal Hidrops:**
• Eritrosit öncüllerini enfekte ederek aplastik krize ve ağır fetal anemiye yol açar. Tanı ve takipte **orta serebral arter (MCA) tepe sistolik hızı (PSV)** doppler ölçümü kullanılır (>1.5 MoM fetal anemi göstergesidir).""",
        [
            {"type": "clinical", "badge": "🔴 21. HAFTA KURALI", "text": "Konjenital CMV ve Tokzoplazma tanısında amniyosentez PCR incelemesi maternal enfeksiyondan ≥6-8 hafta sonra ve ≥21. haftada yapılmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "Fetal anemi ve hidrops şüphesinde fetal eritrosit yıkımını ve anemi derecesini non-invaziv olarak en iyi gösteren doppler parametresi MCA tepe sistolik akım hızıdır (MCA-PSV).", "color": "sky"}
        ],
        {
            "id": "prac-pre-022",
            "question": "Gebelikte Parvovirüs B19 enfeksiyonu geçiren ve ultrasonda hidrops fetalis geliştiği gözlenen bir fetusta non-invaziv olarak fetal anemiyi saptamada kullanılan en güvenilir ultrasonografik doppler parametresi hangisidir?",
            "options": [
                "A) Umbilikal arter pulsatilite indeksi",
                "B) Uterin arter çentikleşmesi",
                "C) Fetal orta serebral arter pik sistolik velositesi (MCA-PSV)",
                "D) Duktus venozus pulsatilite indeksi",
                "E) Fetal renal arter rezistans indeksi"
            ],
            "correctAnswer": "C",
            "explanation": "Fetal anemide kan vizkozitesi azalır ve kardiyak debi artar; orta serebral arter (MCA) pik sistolik akım hızının >1.5 MoM olması ciddi fetal anemi bulgusudur."
        }
    ),
    make_slide(
        23,
        "İntrauterin Fetal Tedavi Yaklaşımları",
        "Medikal Tedaviler, Fetoskopik Lazer Cerrahisi, Spina Bifida Onarımı ve FETO",
        """Gelişen teknoloji sayesinde fetus artık bağımsız bir hasta olarak kabul edilmekte; prenatal dönemde saptanan bazı ölümcül patolojiler intrauterin olarak tedavi edilebilmektedir.

**1. Medikal Fetal Tedaviler:**
• **Konjenital Adrenal Hiperplazi (KAH):** Riskli 46,XX fetuslarda virilizasyonu önlemek için anneye plasentadan yıkılmadan geçen **Deksametazon** başlanması (8. haftadan önce).
• **Fetal Aritmiler:** Fetal supraventriküler taşikardilerde transplasental digoksin, flekainid veya sotalol tedavisi.
• **Fetal Hipotiroidi:** Amniyotik kavite içine levotiroksin enjeksiyonu.

**2. İnvaziv Fetal Cerrahi Girişimler:**
• **İkizden İkize Transfüzyon Sendromu (TTTS):** Monokoryonik ikizlerde plasental vasküler anastomozların fetoskopi altında **lazer fotokoagülasyon** ile yakılması (altın standart tedavi).
• **Açık Spina Bifida (Miyelomeningosel):** 22-26. haftalarda açık fetal cerrahi veya fetoskopik cerrahi ile nöral tüp onarımı (Arnold-Chiari malformasyonu gerilemesini sağlar).
• **Konjenital Diyafragma Hernisi (CDH):** Akciğer hipoplazisini engellemek için trakeanın balonla geçici tıkanması (**FETO** - Fetoendoskopik Trakeal Oklüzyon).""",
        [
            {"type": "clinical", "badge": "🔴 TTTS'DE LAZER ABLASYONU", "text": "Monokoryonik ikizlerde gelişen TTTS tablosunda sağkalımı en çok artıran standart tedavi yöntemi fetoskopik plasental lazer fotokoagülasyondur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "KAH riski taşıyan fetusta dişi dış genitalya virilizasyonunu önlemek amacıyla anneye plasentayı geçebilen deksametazon verilir.", "color": "sky"}
        ],
        {
            "id": "prac-pre-023",
            "question": "Monokoryonik diamniyotik ikiz gebelikte 19. haftada bir fetusta polihidramniyos ve dev mesane, diğer fetusta oligohidramniyos ve mesanenin izlenememesi ile karakterize İkizden İkize Transfüzyon Sendromu (TTTS) saptanıyor. En etkin küratif tedavi yöntemi hangisidir?",
            "options": [
                "A) Acil doğum eyleminin başlatılması",
                "B) Fetoskopik plasental vasküler anastomozların lazer fotokoagülasyonu",
                "C) Alıcı fetusa kordosentez ile kan transfüzyonu",
                "D) Verici fetustan seri amniyoredüksiyon yapılması",
                "E) Anneye yüksek doz kortikosteroid verilmesi"
            ],
            "correctAnswer": "B",
            "explanation": "TTTS'de patolojinin temeli monokoryonik plasentadaki derin arteriyo-venöz anastomozlardır; fetoskopik lazer ablasyonu bu anastomozları kapatarak her iki bebeğin sağkalımını sağlar."
        }
    ),
    make_slide(
        24,
        "Prenatal Genetik Danışmanlık ve Etik-Yasal Çerçeve",
        "Yönlendirici Olmayan (Non-Direktif) Danışmanlık, Otonomi ve Yasal Esaslar",
        """Genetik danışmanlık; prenatal test öncesinde ve sonrasında ebeveynlere testlerin riskleri, sınırlılıkları, yalancı pozitiflik/negatiflik oranları ve olası fetal hastalıkların prognozu hakkında bilgi verilmesi sürecidir.

**1. Temel Etik İlkeler:**
• **Yönlendirici Olmayan (Non-Direktif) Danışmanlık:** Danışman ebeveyn adına asla karar vermez; test yaptırma, invaziv işleme devam etme veya gebeliği sonlandırma kararını ailenin kendi inanç, değer ve otonomisine bırakır.
• **Aydınlatılmış Onam:** Herhangi bir invaziv girişim öncesinde işleme bağlı fetal kayıp oranı, enfeksiyon, kanama ve testin sınırlılıkları ayrıntılı olarak anlatılmalı ve yazılı onam alınmalıdır.

**2. Türkiye'de Yasal ve Tıbbi Çerçeve:**
• Normal şartlarda isteğe bağlı gebelik sonlandırma yasal sınırı 10. gebelik haftasıdır.
• Ancak fetus için ağır malformasyon, letal anöploidi veya anne hayatını tehdit eden tıbbi durumlarda, kadın doğum, genetik, çocuk cerrahisi ve pediatri uzmanlarından oluşan **resmi Sağlık Kurulu Raporu (Tıbbi Kurul Kararı)** ile 10. haftadan sonra da gebelik sonlandırılabilir.""",
        [
            {"type": "clinical", "badge": "🔴 ETİK İLKE", "text": "Genetik danışmanlıkta hekim kendi kişisel veya ahlaki görüşünü empoze edemez; süreç tamamen non-direktif ve ailenin otonomisine dayalı olmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Ağır fetal anomalilerde 10. haftadan sonra gebelik terminasyonu için resmi çok hekimli Sağlık Kurulu Raporu düzenlenmesi kanuni zorunluluktur.", "color": "sky"}
        ],
        {
            "id": "prac-pre-024",
            "question": "Amniyosentez sonucunda fetusta Trizomi 18 (Edwards sendromu) saptanan bir gebeye verilecek genetik danışmanlıkta hekimin benimsemesi gereken EN TEMEL profesyonel etik ilke aşağıdakilerden hangisidir?",
            "options": [
                "A) Gebeliğin derhal sonlandırılması konusunda ebeveyne ısrarcı olmak",
                "B) Aileye tarafsız, tıbbi gerçekleri içeren bilgi vererek kararı ebeveynin özerkliğine bırakan non-direktif (yönlendirici olmayan) yaklaşım sergilemek",
                "C) Ebeveynin kaygılanmaması için sendromun ağır prognozunu gizlemek",
                "D) Kararı hekimin kendi kişisel inançlarına göre şekillendirmesi",
                "E) Bebeğin doğum anına kadar hiçbir tedaviye alınmaması gerektiğini bildirmek"
            ],
            "correctAnswer": "B",
            "explanation": "Genetik danışmanlığın evrensel altın kuralı yönlendirici olmayan (non-direktif) yaklaşımdır. Ebeveynlere tüm bilimsel gerçekler ve seçenekler sunulur, nihai karar ailenin özerkliğine bırakılır."
        }
    )
]

# ==============================================================================
# 3. GÜNCELLEME VE ENTEGRASYON
# ==============================================================================
updated_count = 0
for d in decks:
    if d['id'] == 'learn-dogumsal-genital-anomaliler':
        d['title'] = "Doğumsal Genital Gelişim Anomalileri ve Cinsiyet Farklılaşma Bozuklukları"
        d['description'] = "Kromozomal, gonadal ve fenotipik cinsiyet farklılaşması, SRY kaskadı, AMH ve androjen biyosentezi, Turner, Klinefelter, Swyer, KAH, CAIS, MRKH sendromları ve ambigius genitalya yaklaşımı."
        d['slides'] = anomalies_slides
        d['totalSlides'] = len(anomalies_slides)
        updated_count += 1
        print("Updated learn-dogumsal-genital-anomaliler with", len(anomalies_slides), "slides.")
    elif d['id'] == 'learn-prenatal-tani':
        d['title'] = "Prenatal Tanı Yöntemleri ve Klinik Uygulama Alanları"
        d['description'] = "Fetal ense kalınlığı (NT), duktus venozus, ikili, üçlü, dörtlü tarama testleri, cffDNA (NIPT), koryon villus örneklemesi (CVS), amniyosentez, kordosentez, QF-PCR, karyotipleme, mikrodizi (CMA) ve intrauterin fetal tedaviler."
        d['slides'] = prenatal_slides
        d['totalSlides'] = len(prenatal_slides)
        updated_count += 1
        print("Updated learn-prenatal-tani with", len(prenatal_slides), "slides.")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"Başarıyla tamamlandı! {updated_count} güverte güncellendi.")
