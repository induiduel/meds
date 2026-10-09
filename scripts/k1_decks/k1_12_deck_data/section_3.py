# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-12-s21",
        "title": "Lipoksijenaz Yolağına Giriş: 5-Lipoksijenaz ve Lökotrien Biyosentezi",
        "content": "Araşidonik asit metabolizmasının ikinci büyük kolu **Lipoksijenaz (LOX)** yolağıdır. Bu yolakta görev yapan temel enzim lökositlerde (özellikle nötrofiller, monositler, bazofiller ve mast hücreleri) yoğun olarak bulunan **5-Lipoksijenazdır (5-LOX)**. Enzimin aktivasyonu hücre içi kalsiyum artışı ve nükleer zardaki 5-lipoksijenaz aktive edici protein (FLAP) ile etkileşime girmesiyle gerçekleşir. 5-LOX enzimi serbest araşidonik aside moleküler oksijen ekleyerek önce kararsız hidroperoksi türevi olan 5-HPETE'yi (5-hidroperoksieikozatetraenoik asit), ardından da halkasal epoksit yapısındaki kararsız **Lökotrien A4'ü (LTA4)** sentezler. LTA4 enzimatik yol ayrımının merkezidir; hücre tipine göre ya LTB4'e ya da sisteinil lökotrienlere dönüştürülür.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Lökositlerde lökotrien biyosentezini baslatan temel sitozolik enzim bes-lipoksijenazdır.",
                "bes-lipoksijenazdır",
                "Lökotrien yolağının ilk basamak enzimi"
            ),
            make_recall(
                "5-Lipoksijenaz enziminin nükleer zara tutunarak aktifleşmesini sağlayan yardımcı transmembran protein hangisidir?",
                "FLAP'tır (5-lipoxygenase activating protein).",
                "5-LOX aktive edici protein kısaltması"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-12-s22",
        "title": "Lökotrien B4 (LTB4): Güçlü Nötrofil Kemoatraktanı ve Aktivasyonu",
        "content": "LTA4 hidrolaz enzimi aracılığıyla LTA4'ten sentezlenen **Lökotrien B4 (LTB4)**, akut enflamasyonun hücresel fazında en kritik rolü oynayan lipid mediyatördür. Nötrofiller ve makrofajlar tarafından yüksek miktarda üretilir. LTB4'ün kardinal fonksiyonları şunlardır:\n\n1. **Güçlü Nötrofil Kemotaksisi:** Enflamasyon sahasına nötrofil, monosit ve T lenfosit göçünü tetikleyen vücuttaki en güçlü endojen kemoatraktanlardan biridir (kompleman C5a ile yarışır).\n2. **Lökosit Adezyonu:** Nötrofil yüzeyindeki beta-2 integrinlerin (CD11b/CD18 - Mac-1) afinitesini artırarak endotel üzerindeki ICAM-1'e sıkıca tutunmalarını sağlar.\n3. **Fagositik Aktivasyon:** Nötrofillerde lizozomal enzim salınımını (degranülasyon) ve NADPH oksidaz aracılı reaktif oksijen türleri (ROS / oksidatif patlama) üretimini tetikleyerek mikrobisidal gücü artırır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Akut enflamasyonda nötrofiller için en güçlü kemotaktik etkiyi gösteren, integrin adezyonunu ve reaktif oksijen türleri üretimini artıran lökotrien hangisidir?",
                [
                    {"key": "A", "text": "Lökotrien B4 (LTB4)", "explanation": "A seçeneği DOĞRUDUR: LTB4 nötrofillerin primer güçlü kemoatraktanı ve aktivatörüdür."},
                    {"key": "B", "text": "Lökotrien C4 (LTC4)", "explanation": "B seçeneği yanlıştır: LTC4 bronkokonstriktör sisteinil lökotriendir."},
                    {"key": "C", "text": "Prostaglandin E2 (PGE2)", "explanation": "C seçeneği yanlıştır: Ateş ve ağrı mediyatörüdür."},
                    {"key": "D", "text": "Tromboksan A2 (TXA2)", "explanation": "D seçeneği yanlıştır: Trombosit agregasyonunu yönetir."},
                    {"key": "E", "text": "Lipoksin A4 (LXA4)", "explanation": "E seçeneği yanlıştır: Nötrofil kemotaksisini inhibe eder."}
                ],
                "A"
            ),
            make_cloze(
                "Nötrofil toplanması ve kemotaksisinde rol oynayan en güçlü lipid mediyatör lökotrien B dörttür.",
                "lökotrien B dörttür",
                "LTB4 mediyatörünün tam adı"
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-12-s23",
        "title": "Sisteinil Lökotrienler (LTC4, LTD4, LTE4): Bronkokonstriksiyon ve Geçirgenlik",
        "content": "LTA4 molekülüne glutatyon S-transferaz enzimiyle glutatyon tripeptidi eklendiğinde **Lökotrien C4 (LTC4)** oluşur. Ardından glutamik asit koparılarak **LTD4**, glisin koparılarak **LTE4** meydana gelir. Yapılarında sistein amino asidi taşıdıkları için bu üçlüye **Sisteinil Lökotrienler (CysLT)** veya tarihsel adıyla 'Anafilaksinin Yavaş Etkili Maddesi (SRS-A)' denir. Başlıca mast hücreleri, bazofiller ve eozinofiller tarafından üretilirler. Biyolojik etkileri vasküler ve pulmoner sistemde son derece yıkıcıdır:\n\n- **Şiddetli Bronkokonstriksiyon:** Bronş düz kaslarını kasma güçleri **histaminden yaklaşık 1000 kat daha fazladır**; bronkospazm saatler boyunca sürer.\n- **Vasküler Permeabilite Artışı:** Postkapiller venüllerde interendotelyal aralıkları açarak masif plazma eksüdasyonuna ve hava yolu duvarı ödemine yol açarlar.\n- **Mukus Hipersekresyonu:** Solunum epitelinde mukus bezlerini uyararak lümeni tıkayan koyu tıkaçlar oluştururlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Sisteinil Lökotrien", "Yapısal Özellik", "Majör Biyolojik Etki"],
                [
                    [
                        {"text": "LTC4", "isMasked": False, "hint": ""},
                        {"text": "Glutatyon eklenmiş ilk konjuge lökotrien", "isMasked": True, "hint": "LTA4'e glutatyon bağlanması"},
                        {"text": "Güçlü bronkospazm ve venül geçirgenliği", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "LTD4", "isMasked": False, "hint": ""},
                        {"text": "Sisteinil-glisin türevi ara ürün", "isMasked": True, "hint": "Glutamatın koparılmasıyla oluşan yapı"},
                        {"text": "CysLT1 reseptörüne en yüksek afiniteli ligand", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "LTE4", "isMasked": False, "hint": ""},
                        {"text": "Yalnızca sistein kalıntısı içeren son stabil ürün", "isMasked": True, "hint": "Glisinin de koparılmasıyla kalan peptid"},
                        {"text": "Kalıcı uzamış bronkokonstriksiyon ve idrar atılımı", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "LTC4, LTD4 ve LTE4'ün bronş düz kaslarını kasıcı güçleri histamine kıyasla yaklaşık kaç kat daha fazladır?",
                "Yaklaşık 1000 kat daha fazladır.",
                "Bin katlık devasa güç farkı"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-12-s24",
        "title": "Sisteinil Lökotrienlerin Astım ve Anaflaksi Patogenezindeki Rolü",
        "content": "Bronşiyal astım patofizyolojisinde havayolu obstrüksiyonunun temel sorumlusu sisteinil lökotrienlerdir (LTC4, LTD4, LTE4). Alerjenle karşılaşan mast hücreleri ve solunum mukozasına sızan eozinofiller yüksek miktarda CysLT salgılarlar. Bu moleküller bronş düz kas hücrelerindeki **CysLT1 reseptörlerine** bağlanır. Ortaya çıkan tablo üçlü bir patolojidir:\n\n1. **İnatçı Bronkospazm:** Düz kaslar şiddetle kasılır, hava yolu direnci tepe yapar ve ekspiratuar hırıltı (wheezing) gelişir.\n2. **Mukozal Ödem:** Mikrovasküler sızıntı sonucu bronş submukozası şişerek lümeni içeriden daraltır.\n3. **Mukus Tıkaçları:** Goblet hücrelerinin uyarılmasıyla lümene dökülen viskoz mukus hava yollarını mekanik olarak kilitler.\n\nSistemik anaflakside ise larenks ödemi ve asfiksiye yol açarak ölümcül solunum durmasının birincil tetikleyicisi olurlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Astımda Histamin ve Sisteinil Lökotrienler",
                "Histamin Etkisi",
                "Hızlı başlar, erken geçicidir; bronkokonstriksiyon hafif-orta şiddettedir ve dakikalar içinde zayıflar.",
                "Sisteinil Lökotrien Etkisi",
                "Histaminden 1000 kat güçlüdür; bronkospazm, derin mukozal ödem ve mukus tıkaçları saatlerce sürer."
            ),
            make_cloze(
                "Astım patogenezinde bronş düz kasındaki CysLT1 reseptörlerine bağlanarak inatçı bronkospazm yapan mediyatörler sisteinil lökotrienlerdir.",
                "sisteinil lökotrienlerdir",
                "LTC4, LTD4 ve LTE4 ailesinin genel adı"
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-12-s25",
        "title": "Lipoksinler (LXA4, LXB4): Transselüler Biyosentez Mekanizması",
        "content": "Eikozanoid ailesi içinde diğer tüm üyelerin aksine **anti-inflamatuar** özellik gösteren özelleşmiş moleküllere **Lipoksinler (LXA4 ve LXB4)** denir. 'Lipoxygenase interaction products' kelimelerinden adlandırılmışlardır. Lipoksinlerin en ilginç özelliği sentezlerinin tek bir hücrede değil, iki farklı hücre tipinin işbirliğiyle (transselüler biyosentez) gerçekleşmesidir:\n\n1. **Nötrofil-Trombosit İşbirliği:** Enflamasyon sahasındaki nötrofil 5-LOX enzimiyle araşidonik asitten LTA4 üretir. LTA4 nötrofilden dışarı salınır ve komşu trombosit tarafından içeri alınır. Trombosit bünyesindeki **12-Lipoksijenaz (12-LOX)** enzimi bu LTA4'ü substrat olarak kullanarak **Lipoksin A4 ve B4** sentezler.\n2. **Mukozal Epitel-Lökosit İşbirliği:** Solunum veya bağırsak epitelindeki 15-LOX araşidonik asidi 15-HETE'ye çevirir; nötrofil bunu alarak 5-LOX ile lipoksine dönüştürür.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Lipoksin Transselüler Sentez Zinciri",
                [
                    "1. Nötrofilde 5-LOX: Araşidonik asidin LTA4 ara ürününe dönüştürülmesi",
                    "2. Transselüler Transfer: LTA4'ün komşu aktive trombosite aktarılması",
                    "3. Trombositte 12-LOX: 12-lipoksijenazın LTA4'ü lipoksinlere çevirmesi",
                    "4. Anti-İnflamatuar Salınım: LXA4 ve LXB4'ün dokuya verilerek enflamasyonu frenlemesi"
                ]
            ),
            make_recall(
                "Nötrofil kaynaklı LTA4'ü alarak 12-lipoksijenaz enzimiyle lipoksinlere dönüştüren komşu kan hücresi hangisidir?",
                "Trombosittir (kan pulcuğu).",
                "12-LOX taşıyan çekirdeksiz hemostatik hücre"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-12-s26",
        "title": "Lipoksinlerin Anti-İnflamatuar ve Rezolüsyon Fonksiyonları",
        "content": "Lipoksinler (LXA4, LXB4), enflamatuar reaksiyonun zirve noktasından sonra dokunun sakinleşmesini ve iyileşme fazına geçmesini (rezolüsyon) sağlayan endojen 'fren' mekanizmalarıdır. FPR2 (ALX) reseptörleri üzerinden şu zıt ve koruyucu etkileri gösterirler:\n\n1. **Nötrofil Göçünün İnhibisyonu:** Nötrofillerin kemotaksisini, endotel adezyonunu ve vasküler duvardan transmigrasyonunu güçlü şekilde bloke ederler; böylece dokuya daha fazla nötrofil akmasını durdururlar.\n2. **Eozinofil Alımının Baskılanması:** Alerjik doku hasarını sınırlar.\n3. **Monosit Kemotaksisi ve Eferositozun Uyarılması:** Nötrofilleri durdururken paradoksal olarak monosit ve makrofajların gelişini uyarırlar. En önemlisi makrofajları uyararak apoptoza uğramış yaşlı nötrofilleri yutmalarını (eferositoz) sağlarlar. Bu sayede doku nekrozdan temizlenir ve onarım süreci başlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Lökotrienler ve Lipoksinlerin Zıt Rolleri",
                "Lökotrienler (LTB4, CysLT)",
                "Pro-inflamatuardır; nötrofilleri toplar, doku ödemi yapar ve bronkospazm üretir.",
                "Lipoksinler (LXA4, LXB4)",
                "Anti-inflamatuardır; nötrofil göçünü durdurur, rezolüsyonu (çözünmeyi) ve doku temizliğini sağlar."
            ),
            make_cloze(
                "Eikozanoidler içinde nötrofil kemotaksisini ve adezyonunu inhibe ederek enflamasyonun çözünmesini saglayan mediyatörler lipoksinlerdir.",
                "lipoksinlerdir",
                "LXA4 ve LXB4 moleküllerinin ait olduğu çözücü grup"
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-12-s27",
        "title": "Eikozanoidleri Hedefleyen İlaçlar - I: Non-Steroid Antiinflamatuarlar (NSAİİ)",
        "content": "Klinik tıbbın en yaygın reçete edilen ilaç grubu olan **Non-Steroid Antiinflamatuar İlaçlar (NSAİİ)**, siklooksijenaz (COX) enziminin aktif bölgesine bağlanarak prostaglandin ve tromboksan sentezini durdururlar. Bu grubun üyeleri:\n\n- **Aspirin (Asetilsalisilik Asit):** Siklooksijenaz enziminin aktif bölgesindeki Serin-530 amino asidini kovalent olarak **geri dönüşümsüz (irreversible)** asetiller. Trombositlerde TXA2 üretimini hücre ömrü boyunca durdurarak kardiyoprotektif antitrombotik etki sağlar.\n- **İbuprofen, Naproksen, İndometazin, Diklofenak:** COX-1 ve COX-2 aktif cebine yarışmalı olarak bağlanarak enzimi **geri dönüşümlü (reversible)** inhibe ederler.\n\nNSAİİ'lerin analjezik (ağrı kesici), antipiretik (ateş düşürücü) ve antiinflamatuar etkileri temel olarak PGE2 sentezinin baskılanmasına dayanır. Ancak konstitütif COX-1'in bloke edilmesi mide mukozasında koruyucu prostaglandinleri yok ederek gastrit ve peptik ülsere yol açar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İlaç Grubu", "Enzimatik Mekanizma", "Klinik Etki ve Risk"],
                [
                    [
                        {"text": "Aspirin", "isMasked": False, "hint": ""},
                        {"text": "Serin rezidüsünün geri dönüşümsüz asetilasyonu", "isMasked": True, "hint": "Kovalent ve kalıcı enzim modifikasyonu"},
                        {"text": "Antitrombotik kardiyoproteksiyon; kanama riski", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Geleneksel NSAİİ (İbuprofen vb.)", "isMasked": False, "hint": ""},
                        {"text": "COX-1 ve COX-2'nin yarışmalı geri dönüşümlü blokajı", "isMasked": True, "hint": "Çift izoform kompetitif inhibisyonu"},
                        {"text": "Ağrı, ateş ve inflamasyon kontrolü; peptik ülser riski", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Aspirinin diğer geleneksel NSAİİ'lerden farklı olarak siklooksijenaz enzimini inhibe etme tarzı nedir?",
                "Geri dönüşümsüz (kovalent asetilasyon ile) inhibisyondur.",
                "Kalıcı kovalent bağlanma biçimi"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-12-s28",
        "title": "Eikozanoidleri Hedefleyen İlaçlar - II: Seçici COX-2 İnhibitörleri ve Tromboz Riski",
        "content": "Geleneksel NSAİİ'lerin mide ülseri yapıcı yan etkilerinden kaçınmak amacıyla yalnızca inflamasyon bölgesinde üretilen COX-2'yi hedefleyen **Seçici COX-2 İnhibitörleri (Koksibler: Selekoksib, Rofekoksib)** geliştirilmiştir. Bu moleküller COX-2'nin daha geniş olan yan cebine bağlanarak COX-1'e dokunmazlar; bu sayede mide mukozası korunur. Ancak bu seçicilik büyük bir kardiyovasküler felakete zemin hazırlamıştır:\n\n- Endotel hücrelerindeki COX-2 selektif olarak baskılandığında, vazodilatatör ve antitrombotik olan **Prostasiklin (PGI2)** üretimi dibe vurur.\n- Buna karşılık, trombositlerdeki COX-1 hiç etkilenmediği için trombosit kaynaklı **Tromboksan A2 (TXA2)** sentezi kesintisiz ve engelsiz devam eder.\n- TXA2 / PGI2 dengesi protrombotik yöne kayar; koroner arterlerde kontrolsüz trombosit agregasyonu ve vazokonstriksiyon gelişir. Bu durum miyokard enfarktüsü ve inme riskini katladığı için bazı koksibler piyasadan çekilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Seçici COX-2 inhibitörlerinin (koksibler) miyokard enfarktüsü ve vasküler tromboz riskini artırmasının temel patofizyolojik mekanizması hangisidir?",
                [
                    {"key": "A", "text": "Endotelyal antitrombotik PGI2 sentezi baskılanırken, trombositteki COX-1 kaynaklı TXA2 üretiminin engelsiz sürmesi", "explanation": "A seçeneği DOĞRUDUR: Endotelde PGI2 çöker fakat trombositte TXA2 tam hız devam eder; bu durum pıhtılaşma lehine ölümcül bir dengesizlik yaratır."},
                    {"key": "B", "text": "Kandaki tüm eritrositlerin parçalanarak damarları tıkaması", "explanation": "B seçeneği yanlıştır: Hemolitik bir etki söz konusu değildir."},
                    {"key": "C", "text": "Karaciğerin aniden tüm fibrinojen üretimini durdurması", "explanation": "C seçeneği yanlıştır: Fibrinojen düşmez."},
                    {"key": "D", "text": "Lökotrienlerin tamamen yok olarak kanı dondurması", "explanation": "D seçeneği yanlıştır: Lökotrienler COX enziminden bağımsızdır."},
                    {"key": "E", "text": "Mide mukozasında aşırı asit üretilip kana karışması", "explanation": "E seçeneği anlamsızdır."}
                ],
                "A"
            ),
            make_cloze(
                "Seçici COX-2 inhibitörleri endotelyal prostasiklin üretimini baskılayıp TXA2 dengesini bozarak kardiyovasküler tromboz riskini artırabilir.",
                "tromboz riskini",
                "Damar içinde pıhtı oluşumu tehlikesi"
            )
        ]
    })

    # Slide 29 (CHECKPOINT 3)
    slides.append({
        "id": "k1-12-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Lipoksijenaz Yolağı, Lökotrienler, Lipoksinler ve Farmakolojik Hedefler",
        "content": "Lipoksijenaz yolağı ve eikozanoid farmakolojisinin kilit ilkeleri:\n\n1. **5-LOX ve FLAP:** Lökositlerde araşidonik asitten önce 5-HPETE ve LTA4 üretir.\n2. **LTB4:** Nötrofillerin en güçlü kemoatraktanıdır; integrin adezyonunu ve ROS üretimini tetikler.\n3. **CysLT (LTC4, LTD4, LTE4):** Sisteinil lökotrienlerdir; histaminden 1000 kat güçlü bronkokonstriksiyon, derin permeabilite ve mukus artışı yaparlar; astım ve anaflaksinin temel aktörüdür.\n4. **Lipoksinler (LXA4, LXB4):** 12-LOX ile transselüler (nötrofil-trombosit) sentezlenir; anti-inflamatuardır, nötrofil alımını durdurur, eferositozu ve çözünmeyi uyarır.\n5. **Aspirin:** COX'u geri dönüşümsüz asetiller; düşük dozda trombosit TXA2'sini sıfırlayarak antitrombotik koruma sağlar.\n6. **Seçici COX-2 İnhibitörleri:** Mideyi korur ancak endotel PGI2'sini kesip trombosit TXA2'sine dokunmadığı için tromboz riskini artırır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Araşidonik Asit Metabolitlerinin Etki Yelpazesi",
                [
                    "1. Pro-enflamatuar Vazoaktif: PGE2, PGI2, PGD2 ile vazodilatasyon ve ağrı/ateş",
                    "2. Protrombotik Hemostatik: TXA2 ile trombosit agregasyonu ve damar büzülmesi",
                    "3. Lökosit ve Solunum Hasarı: LTB4 ile nötrofil akını, LTC4/D4/E4 ile astmatik bronkospazm",
                    "4. Anti-enflamatuar Rezolüsyon: Lipoksinler (LXA4/B4) ile dokunun sakinleşip temizlenmesi"
                ]
            ),
            make_recall(
                "Lökotrien ailesinde bronş düz kaslarını histaminden 1000 kat daha güçlü kasan sisteinil lökotrien üçlüsü hangileridir?",
                "LTC4, LTD4 ve LTE4'tür.",
                "Sistein içeren üçlü lökotrien grubu"
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-12-s30",
        "title": "Lökotrien Yolağını Hedefleyen İlaçlar: Zileuton ve Montelukast",
        "content": "Astım ve alerjik rinit tedavisinde lökotrienlerin yıkıcı etkilerini engellemek amacıyla farmakolojide iki ana stratejik ilaç sınıfı kullanılır:\n\n1. **5-Lipoksijenaz Enzim İnhibitörleri (Zileuton):** 5-LOX enzimini doğrudan inhibe ederek araşidonik asitten hiçbir lökotrienin (ne LTB4 ne de sisteinil lökotrienler) üretilememesini sağlar. Hem hücresel nötrofilik infiltrasyonu hem de bronkospazmı en baştan keser.\n2. **Lökotrien Reseptör Antagonistleri (LTRA - Montelukast, Zafirlukast, Pranlukast):** Bronş düz kası ve solunum epiteli üzerindeki **CysLT1 reseptörlerini** selektif olarak bloke ederler. Lökotrien LTC4 ve LTD4 sentezlense dahi reseptörüne bağlanamaz. Sonuç olarak bronkokonstriksiyon, mukozal ödem ve aşırı mukus salgısı engellenir; kronik astım kontrolünde ve egzersize bağlı bronkospazm profilaksisinde yaygın kullanılır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Kronik alerjik astımı olan 14 yaşında bir hastaya nefes darlığı ataklarını ve gece öksürüklerini önlemek amacıyla günde tek doz oral montelukast başlanıyor. Hastanın solunum fonksiyon testlerinde belirgin düzelme kaydediliyor.",
                "Montelukastın bu klinik başarısını sağlayan primer etki mekanizması hangisidir?",
                [
                    {
                        "text": "Bronş düz kasındaki CysLT1 reseptörlerini selektif olarak bloke ederek LTC4 ve LTD4'ün bronkokonstriktör etkisini engeller.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Montelukast bir CysLT1 reseptör antagonistidir; sisteinil lökotrienlerin bronşları daraltmasını önler."
                    },
                    {
                        "text": "5-lipoksijenaz enzimini kovalent bağlayarak araşidonik asit üretimini tamamen sıfırlar.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. 5-LOX inhibitörü Zileuton'dur; montelukast ise reseptör antagonistidir."
                    },
                    {
                        "text": "Akciğerlerdeki tüm histamin moleküllerini kimyasal olarak yok eder.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Montelukast lökotrien yolağı ilacıdır, antihistaminik değildir."
                    }
                ]
            ),
            make_cloze(
                "Montelukast ve zafirlukast bronş düz kasındaki CysLT1 reseptörlerini selektif olarak bloke eden lökotrien antagonistleridir.",
                "CysLT1 reseptörlerini",
                "Sisteinil lökotrienlerin bağlandığı temel hava yolu reseptörü"
            )
        ]
    })

    return slides
