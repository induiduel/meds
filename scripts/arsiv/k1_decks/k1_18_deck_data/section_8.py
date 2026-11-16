# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-18-s71",
        "title": "Cumhuriyet Dönemi Öncesi ve Kurtuluş Savaşı'nda Sağlık Durumu",
        "content": "Cumhuriyet kurulduğunda Anadolu halkı yüzyıllar süren savaşların, yoksulluğun ve salgınların pençesinde kırılıyordu (Sınav Spotu):\n\n- **1923 Türkiye'sinin Ağır Sağlık Tablosu:**\n  - Yaklaşık 13 milyonluk nüfusun yarısından fazlası **sıtma, trahom, tüberküloz, tifüs, çiçek ve frengi** ile enfekteydi.\n  - Bebek ölüm hızı binde 250-300 civarındaydı (doğan her 3-4 bebekten biri 1 yaşına gelmeden ölüyordu).\n  - Ülke genelinde yalnızca yaklaşık 554 hekim, 69 eczacı, 4 hemşire ve 136 ebe vardı; hastane yatağı sayısı birkaç bini geçmiyordu.\n- **Savaşta Tifüs ve Sıtma:** Kurtuluş Savaşı ve I. Dünya Savaşı'nda düşman mermisinden daha fazla asker tifüs (bitlerle bulaşan) ve sıtma yüzünden şehit düşmüştür.\n- **Devrim İhtiyacı:** Genç Cumhuriyet, bir yandan bağımsızlığını kazanırken diğer yandan halkın sağlığını sıfırdan inşa etmek zorundaydı.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "1923 Türkiye Sağlık Tablosu vs Günümüz",
                "1923 Cumhuriyeti Başlangıcı",
                "Nüfusun yarısı sıtma, trahom ve veremli; bebek ölüm hızı binde 300; tüm ülkede yalnızca 554 hekim.",
                "Çağdaş Sağlık Düzeyi",
                "Sıtma ve çiçek sıfırlanmış, bebek ölüm hızı binde 8-9'a inmiş ve yüz binlerce sağlık personeli."
            ),
            make_quiz(
                "Türkiye Cumhuriyeti kurulduğunda (1923) ülke genelinde halkı kırıp geçiren en yaygın üç büyük kronik enfeksiyon salgını hangileriydi?",
                [
                    {"key": "A", "text": "Sıtma, Trahom ve Tüberküloz (Verem)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Erken Cumhuriyet döneminde sıtma, göz körlüğü yapan trahom ve verem halk sağlığının bir numaralı düşmanlarıydı."},
                    {"key": "B", "text": "Sarıhumma, Ebola ve Dang", "isCorrect": False, "explanation": "Tropikal Afrika ve Amerika hastalıklarıdır."},
                    {"key": "C", "text": "Alzheimer, Parkinson ve Gut", "isCorrect": False, "explanation": "İleri yaş kronik dejeneratif hastalıklardır."},
                    {"key": "D", "text": "Kuduz, Şarbon ve Kırım-Kongo", "isCorrect": False, "explanation": "Yaygın salgın üçlüsü değildir."}
                ]
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-18-s72",
        "title": "Dr. Refik Saydam ve Erken Cumhuriyet Dönemi Sağlık Teşkilatlanması",
        "content": "Cumhuriyet'in ilk Sağlık Bakanı olan Dr. Refik Saydam (1881-1942), Türkiye'nin modern koruyucu sağlık teşkilatının mimarıdır (Sınav Spotu):\n\n- **İlk Sağlık Bakanlığı:**\n  - 2 Mayıs 1920'de TBMM açıldıktan hemen sonra 'Sıhhiye ve Muavenet-i İçtimaiye Vekaleti' kuruldu ve başına askeri hekim Dr. Refik Saydam getirildi (14 yıl bakanlık yaptı).\n- **Temel Sağlık Yasaları:**\n  - **1593 Sayılı Umumi Hıfzıssıhha Kanunu (1930):** Türkiye'nin halk sağlığı anayasasıdır; bulaşıcı hastalıklarla mücadele, aşı zorunlulukları, çevre sağlığı, gıda denetimi ve belediye temizlik kurallarını eksiksiz düzenlemiştir.\n  - **Tababet ve Şuabatı San'atlarının Tarzı İcrasına Dair Kanun (1928):** Hekimlik mesleğinin yasal çerçevesini çizmiştir.\n- **Dikey Mücadele Örgütleri:** Sıtma Savaş, Trahom Savaş ve Verem Savaş dispanserleri kuruldu.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Kanun / Kurum", "Tarih", "Halk Sağlığındaki Rolü"],
                [
                    ["Sıhhiye Vekaleti", "2 Mayıs 1920", "Türkiye'nin ilk Sağlık Bakanlığı'nın kuruluşu"],
                    ["Umumi Hıfzıssıhha Kanunu (1593)", "1930", "Cumhuriyet'in koruyucu hekimlik ve halk sağlığı anayasası"],
                    ["Sıtma ve Trahom Dispanserleri", "1925-1930'lar", "Saha taramaları ve halka ücretsiz kinin ve ilaç dağıtımı"]
                ]
            ),
            make_cloze(
                "1930 yılında çıkarılan ve Türkiye'de koruyucu hekimliğin, bulaşıcı hastalıklarla mücadelenin ve aşılamanın temelini oluşturan yasa Umumi Hıfzıssıhha Kanunu'dur.",
                "Umumi Hıfzıssıhha Kanunu",
                "1593 sayılı tarihi Türk halk sağlığı kanununun adı"
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-18-s73",
        "title": "Hıfzıssıhha Enstitüsü ve Türkiye'nin Kendi Aşısını Ürettiği Yıllar",
        "content": "Dr. Refik Saydam'ın öncülüğünde 1928 yılında Ankara'da kurulan Refik Saydam Hıfzıssıhha Enstitüsü, Cumhuriyet tıbbının gurur abidesidir (Sınav Spotu):\n\n- **Aşı ve Serum Bağımsızlığı:**\n  - Genç Türkiye Cumhuriyeti dışa bağımlı kalmamak için aşılarını kendi laboratuvarlarında üretmeye başladı.\n  - **Çiçek, kuduz, kolera, tifo, dizanteri, difteri, tetanos ve BCG (verem) aşıları ile serumlar** Hıfzıssıhha'da yerli olarak üretildi.\n- **Uluslararası Yardım:**\n  - 1940'lı yıllarda Türkiye yalnızca kendi ihtiyacını karşılamakla kalmamış; kolera salgını yaşayan Çin'e, difteriyle boğuşan Yunanistan'a ve Suriye'ye **milyonlarca doz aşı hibe etmiştir**.\n- **Hıfzıssıhha Okulu:** Halk sağlığı uzmanlarının, epidemiyologların ve laboratuvar uzmanlarının yetiştirildiği seçkin bir bilim yuvası olmuştur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Yerli Aşı Üreten Hıfzıssıhha vs Dışa Bağımlılık",
                "Refik Saydam Hıfzıssıhha Enstitüsü (1928)",
                "Çiçek, kuduz, tifo ve BCG aşılarını Türkiye kendi üretiyor, salgın yaşayan komşu ülkelere aşı ihraç ediyordu.",
                "Aşı Bağımsızlığının Önemi",
                "Kendi aşısını ve serumunu üretebilen bir halk sağlığı sistemi ulusal güvenliğin ve bağımsızlığın teminatıdır."
            ),
            make_quiz(
                "1928 yılında Ankara'da kurulan; Türkiye'nin çiçek, kuduz, tifo, kolera ve BCG aşılarını üreterek salgın yaşayan ülkelere aşı ihraç eden tarihi ulusal kurum hangisidir?",
                [
                    {"key": "A", "text": "Refik Saydam Hıfzıssıhha Enstitüsü", "isCorrect": True, "explanation": "Doğru cevap A'dır: Refik Saydam Hıfzıssıhha Enstitüsü Türkiye'nin yerli aşı ve serum üretim üssüydü."},
                    {"key": "B", "text": "Kızılay Kan Merkezi", "isCorrect": False, "explanation": "Kan bağışı ve afet yardım kuruluşudur."},
                    {"key": "C", "text": "Gülhane Askeri Tıp Akademisi", "isCorrect": False, "explanation": "Askeri tıp fakültesi ve hastanesidir."},
                    {"key": "D", "text": "TÜBİTAK", "isCorrect": False, "explanation": "1963'te kurulan bilimsel araştırma kurumudur."}
                ]
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-18-s74",
        "title": "Prof. Dr. Nusret Fişek (1914-1990): Yaşamı, Misyonu ve Görevleri",
        "content": "Prof. Dr. Nusret Fişek, çağdaş Türkiye'de toplum hekimliği ve halk sağlığı disiplininin tartışmasız en büyük kurucu lideridir (Sınav Spotu):\n\n- **Seçkin Bir Tıp Kariyeri:**\n  - 1938'de İstanbul Tıp Fakültesi'ni birincilikle bitirdi; biyokimya ve bakteriyoloji uzmanı oldu; Harvard Üniversitesi'nde halk sağlığı doktorası yaptı.\n- **Üstlendiği Kritik Görevler:**\n  1. **Sağlık Bakanlığı Müsteşarlığı (1960-1965):** Türk sağlık sisteminin en büyük reform kanunlarını bizzat hazırladı ve yasalaştırdı.\n  2. **Refik Saydam Hıfzıssıhha Okulu Müdürlüğü.**\n  3. **Hacettepe Üniversitesi Toplum Hekimliği Enstitüsü Kurucusu ve Başkanı.**\n  4. **Türk Tabipleri Birliği (TTB) Merkez Konseyi Başkanlığı (1984-1990):** Hekim hakları, barış ve tıp etiği mücadelesi verdi.\n- **Yaşam Felsefesi:** 'Herkese eşit, ücretsiz ve nitelikli sağlık hizmeti' sunulması için ömrünü adamıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Dönem / Yıl", "Nusret Fişek'in Üstlendiği Görev", "Halk Sağlığı Mirası"],
                [
                    ["1960-1965", "Sağlık Bakanlığı Müsteşarı", "224 Sayılı Sosyalleştirme Kanunu ve Nüfus Planlaması Kanunu'nun mimarı"],
                    ["1965-1983", "Hacettepe Toplum Hekimliği Başkanı", "Türkiye'de halk sağlığı uzmanlarının yetiştirilmesi ve saha eğitimleri"],
                    ["1984-1990", "Türk Tabipleri Birliği (TTB) Başkanı", "Hekim bağımsızlığı, tıp etiği ve insan hakları savunuculuğu"]
                ]
            ),
            make_cloze(
                "Türkiye'ye toplum hekimliği kavramını getiren, 224 Sayılı Sosyalleştirme Kanunu'nu çıkaran ve TTB Başkanlığı yapan hekim Prof. Dr. Nusret Fişek'tir.",
                "Nusret Fişek",
                "Türk halk sağlığının kurucu babası olan efsanevi hekim ve akademisyen"
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-18-s75",
        "title": "224 Sayılı Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun (1961)",
        "content": "5 Ocak 1961 tarihinde kabul edilen 224 Sayılı Kanun, Türk tıp tarihinin en devrimci ve ileri görüşlü sağlık reformudur (Sınav Spotu):\n\n- **Sosyalleştirmenin Anlamı Nedir?**\n  - Sağlık hizmetlerinin bireylerin alım gücüne bakılmaksızın, devlet bütçesinden karşılanarak **tüm yurttaşlara eşit, parasız ve eksiksiz** sunulmasıdır.\n- **224 Sayılı Yasanın Temel İlkeleri:**\n  1. **Eşitlik:** Zengin-yoksul ayrımı olmadan herkes ihtiyacı kadar sağlık hizmeti alır.\n  2. **Entegrasyon (Bütüncül Hizmet):** Koruyucu hekimlik (aşı, çevre, gebe takibi) ile tedavi edici hekimlik (muayene, ilaç) aynı çatı altında birleştirilmiştir.\n  3. **Kademeli Sevk Zinciri:** Hasta önce birinci basamağa başvurur; gerekirse ikinci (devlet hastanesi) ve üçüncü basamağa (üniversite) sevk edilir.\n  4. **Ekip Hizmeti:** Hekim tek başına değil; ebe, hemşire ve sağlık memuruyla bir ekip halinde çalışır.\n  5. **Nüfusa Göre Örgütlenme:** Her sağlık ocağı belirli bir coğrafi nüfustan (ortalama 5.000-10.000 kişi) sorumludur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "224 Sayılı Kanunun Getirdiği Basamaklı Sağlık Sistemi",
                [
                    "1. Sağlık Evi (Köy Düzeyi): Ebe köyde yaşar, gebeleri ve bebekleri düzenli izler.",
                    "2. Sağlık Ocağı (Birinci Basamak): Hekim başkanlığındaki ekip koruyucu ve ayaktan tedaviyi sunar.",
                    "3. İlçe / İl Devlet Hastanesi (İkinci Basamak): Yataklı tedavi ve uzman hekimlik hizmeti verilir.",
                    "4. Üniversite Hastanesi (Üçüncü Basamak): İleri tetkik, eğitim ve karmaşık cerrahiler yürütülür."
                ]
            ),
            make_cloze(
                "Türkiye'de sağlık hizmetlerinin sosyalleştirilmesini, sağlık ocakları sistemini ve entegre koruyucu hekimliği kuran tarihi kanun 224 sayılı kanundur.",
                "224 sayılı",
                "1961 yılında çıkarılan Sosyalleştirme Kanunu'nun numarası"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-18-s76",
        "title": "Sağlık Ocakları Sistemi: Köyde Ebe, İlçede Hekim Modeli",
        "content": "Nusret Fişek'in kurduğu Sağlık Ocakları modeli, hizmeti hastanın ayağına götürmenin dünyadaki en başarılı örneklerindendir (Sınav Spotu):\n\n- **Örgütlenme Piramidi:**\n  - **Sağlık Evi (Köy Düzeyi - 2.000-3.000 Nüfus):**\n    - Köyde bir ebe ikamet eder. Ebe köydeki tüm doğurgan yaştaki kadınları, gebeleri ve bebekleri düzenli ev ziyaretleriyle evinde takip eder; aşılarını yapar.\n  - **Sağlık Ocağı (Kasaba/İlçe Düzeyi - 5.000-10.000 Nüfus):**\n    - Sağlık ocağı ekibi: 1 Hekim (Ocak Tabibi), 1-2 Hemşire, 2 Ebe, 1 Sağlık Memuru, 1 Şoför ve 1 Hizmetli.\n- **Kayıt ve Sürveyans Sistemi:**\n  - **Form 012 (Aşı Kartı), Form 005 (Gebe İzlem Kartı) ve ETF (Ev Halkı Tespit Fişi):** Her hanenin suyu, tuvaleti, kronik hastaları tek tek fişlenir ve kapı kapı izlenirdi.\n- **İlk Pilot Uygulama (Muş İli - 1963):** Sosyalleştirme ilk kez Doğu Anadolu'da, Muş ilinde başlatılmış ve başarıyla tüm Türkiye'ye yayılmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Sağlık Birimi", "Sorumlu Nüfus", "Personel Yapısı", "Temel Görev ve İşlevi"],
                [
                    ["Sağlık Evi", "2.000-3.000 kişi (Köy)", "1 Köy Ebesi", "Gebe-bebek izlemi, doğum, aşılama ve ev ziyaretleri"],
                    ["Sağlık Ocağı", "5.000-10.000 kişi", "Hekim, ebe, hemşire, sağlık memuru", "Entegre koruyucu aşı, çevre sağlığı, ayaktan tedavi ve sevk"]
                ]
            ),
            make_quiz(
                "224 Sayılı Sosyalleştirme Kanunu kapsamında sağlık ocakları ve köylerde kurulan sağlık evleri modeli ilk kez 1963 yılında pilot il olarak nerede uygulanmaya başlanmıştır?",
                [
                    {"key": "A", "text": "Muş", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sağlık hizmetlerinin sosyalleştirilmesi ilk olarak 1963 yılında Muş ilinde pilot olarak başlatılmıştır."},
                    {"key": "B", "text": "İstanbul", "isCorrect": False, "explanation": "Büyükşehirlerde sosyalleştirme daha geç uygulanmıştır."},
                    {"key": "C", "text": "İzmir", "isCorrect": False, "explanation": "Ege pilot bölge değildi."},
                    {"key": "D", "text": "Ankara", "isCorrect": False, "explanation": "Başkent pilot bölge seçilmemiştir."}
                ]
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-18-s77",
        "title": "Nüfus Planlaması Kanunu (1965): Aşırı Nüfus Artışına Karşı Koruyucu Adım",
        "content": "Cumhuriyet'in ilk yıllarında savaş kayıplarını telafi etmek için 'doğurganlığı teşvik eden (pronatalist)' bir nüfus politikası izlenmişti (Sınav Spotu):\n\n- **Pronatalist Dönem (1923-1960):**\n  - Doğum kontrolü yasaklanmış, 6 çocuktan fazlasına madalya verilmişti.\n- **Kritik Kırılma ve Nusret Fişek'in Uyarısı:**\n  - 1960'lara gelindiğinde kontrolsüz hızlı nüfus artışı; yoksulluk, gecekondulaşma, anne ölümleri ve kadınların sağlıksız düşüklerle (kriminal abortus) hayatını kaybetmesi gibi devasa halk sağlığı sorunları yarattı.\n  - Nusret Fişek, aşırı nüfus artışının kalkınmayı yutan en büyük tehdit olduğunu hükümete anlattı.\n- **557 Sayılı Nüfus Planlaması Kanunu (1965):**\n  - Gebeliği önleyici yöntemlerin (RİA, doğum kontrol hapı, prezervatif) ithali, üretimi ve halka ücretsiz dağıtımı yasal hale getirildi.\n  - Ailelerin istedikleri sayıda ve istedikleri zamanda çocuk sahibi olma hakkı kamusal güvenceye kavuşturuldu.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Pronatalist Dönem (1923-1960) vs Nüfus Planlaması (1965)",
                "Pronatalist Dönem (1923-1960)",
                "Doğum kontrolü yasaktı; kadınlar ehil olmayan ellerde yasa dışı düşük yaparken kanama ve sepsisten ölüyordu.",
                "1965 Nüfus Planlaması Kanunu",
                "Aile planlaması hakkı sağlandı; sağlık ocaklarında ücretsiz doğum kontrolüyle anne ve bebek ölümleri hızla düştü."
            ),
            make_cloze(
                "Türkiye'de ailelerin istedikleri zaman ve bakabilecekleri sayıda çocuk sahibi olmalarını sağlayan ve doğum kontrolünü serbest bırakan yasa 1965 yılında çıkarılan Nüfus Planlaması Kanunu'dur.",
                "Nüfus Planlaması Kanunu",
                "Nusret Fişek'in öncülüğünde 1965'te çıkarılan tarihi kanun"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-18-s78",
        "title": "Nusret Fişek'in 'Herkese Eşit, Nitelikli ve Parasız Sağlık' Mirası",
        "content": "Nusret Fişek'in yarattığı sağlık felsefesi yalnızca Türkiye'de değil, tüm dünyada örnek gösterilen bir halk sağlığı ekolü olmuştur (Sınav Spotu):\n\n- **Fişek Modelinin 4 Kutsal Kuralı:**\n  1. **Sağlık Hizmeti Alınıp Satılan Bir Meta Değildir:** Sağlık piyasa koşullarına ve kar hırsına terk edilemez; devletin yurttaşına sunmak zorunda olduğu en temel haktır.\n  2. **Korumaya Mutlak Öncelik:** Devlet parasını hastanelerdeki pahalı cihazlara değil, önce temiz suya, aşıya, gebelerin beslenmesine ve kanalizasyona harcamalıdır.\n  3. **Hekimlik Ekip İşidir:** Hekimin en yakın çalışma arkadaşı köydeki ebe ve sağlık memurudur; onlar olmadan hekim halka ulaşamaz.\n  4. **Halkın Katılımı:** Halkın güvenini kazanmadan ve halkı eğitmeden hiçbir sağlık politikası başarılı olamaz.\n- **Dünya Sağlık Örgütü Ödülü:** DSÖ, 1978 Alma-Ata Deklarasyonu'nu hazırlarken Nusret Fişek'in 224 Sayılı Kanunu'nu en başarılı 'Temel Sağlık Hizmetleri' modellerinden biri olarak referans almıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Nusret Fişek Felsefesinin Dört Temel Taşı",
                [
                    "1. Hak Olarak Sağlık: Ticari meta değil, anayasal kamusal hizmet anlayışı.",
                    "2. Koruma Önceliği: Kaynakların hastalığı önlemeye ve aşıya yönlendirilmesi.",
                    "3. Ekip ve Dayanışma: Hekim, ebe ve hemşirenin eşitlikçi ekip ruhu.",
                    "4. Sahada Varlık: Masada oturan değil, halkın evine giren toplum hekimliği."
                ]
            ),
            make_quiz(
                "Dünya Sağlık Örgütü'nün 1978 yılında ilan ettiği Alma-Ata Temel Sağlık Hizmetleri modeline öncülük eden ve Türkiye'de 1961'de uygulanan tarihi sistem hangisidir?",
                [
                    {"key": "A", "text": "224 Sayılı Sağlık Hizmetlerinin Sosyalleştirilmesi ve Sağlık Ocakları Sistemi", "isCorrect": True, "explanation": "Doğru cevap A'dır: 224 sayılı yasa Alma-Ata'dan 17 yıl önce Temel Sağlık Hizmetleri ilkelerini eksiksiz kurmuştur."},
                    {"key": "B", "text": "Özel hastaneler işletme modeli", "isCorrect": False, "explanation": "Piyasa modelidir."},
                    {"key": "C", "text": "Miazma temizleme programı", "isCorrect": False, "explanation": "19. yüzyıl miazma anlayışıdır."},
                    {"key": "D", "text": "Yalnızca askeri sahra hastaneleri sistemi", "isCorrect": False, "explanation": "Tüm toplumu kapsamaz."}
                ]
            )
        ]
    })

    # Slide 79 - CHECKPOINT 8
    slides.append({
        "id": "k1-18-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Türkiye'de Sosyalleştirilmiş Sağlık ve Nusret Fişek",
        "content": "Bu checkpointte Türkiye Cumhuriyeti'nin halk sağlığı devrimini ve Nusret Fişek modelini özetliyoruz:\n\n- **1923 Tablosu:** Nüfusun yarısı sıtma, trahom ve veremliydi; bebek ölüm hızı binde 300'dü; 554 hekim vardı.\n- **Dr. Refik Saydam:** İlk Sağlık Bakanı; 1593 Sayılı Umumi Hıfzıssıhha Kanunu'nu (1930) çıkardı; Refik Saydam Hıfzıssıhha Enstitüsü'nü kurarak yerli aşı ve serum üretimini başlattı.\n- **Prof. Dr. Nusret Fişek:** Türk halk sağlığının kurucusudur; Sağlık Bakanlığı Müsteşarlığı, Hıfzıssıhha Okulu Müdürlüğü, Hacettepe Toplum Hekimliği Enstitüsü ve TTB Başkanlığı yaptı.\n- **224 Sayılı Kanun (1961):** Sağlık hizmetlerinin sosyalleştirilmesi kanunudur; eşit, entegre, ekip tabanlı, kademeli sevk zincirli Sağlık Ocakları sistemini kurdu (Pilot il: Muş, 1963).\n- **Nüfus Planlaması Kanunu (1965):** Kontrolsüz nüfus artışını ve yasa dışı düşükleri önlemek için doğum kontrolünü serbest bıraktı.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Kanun / Kurum", "Yıl / Öncü", "Türk Halk Sağlığına Kazandırdığı Temel Değer"],
                [
                    ["Umumi Hıfzıssıhha Kanunu (1593)", "1930 (Refik Saydam)", "Bulaşıcı hastalıklarla mücadele ve çevre sağlığının temel yasası"],
                    ["Hıfzıssıhha Enstitüsü", "1928 (Refik Saydam)", "Çiçek, tifo, kuduz ve BCG aşılarında ulusal bağımsızlık"],
                    ["224 Sayılı Kanun", "1961 (Nusret Fişek)", "Sağlık hizmetlerinin sosyalleştirilmesi ve Sağlık Ocakları devrimi"],
                    ["Nüfus Planlaması Kanunu", "1965 (Nusret Fişek)", "Ücretsiz aile planlaması ve anne ölümlerinin önlenmesi"]
                ]
            ),
            make_chain(
                "Türkiye'nin Halk Sağlığı Devrim Basamakları",
                [
                    "1. Refik Saydam Dönemi: Sıtma, trahom ve verem dispanserleri ile yerli aşı üretimi.",
                    "2. 224 Sayılı Yasa (1961): Köyde ebe, sağlık ocağında hekimle entegre koruyucu hekimlik.",
                    "3. Muş Pilot Uygulaması (1963): Sosyalleştirilmiş sağlık modelinin sahada başarısı.",
                    "4. Nüfus Planlaması (1965): Aile planlamasıyla anne ve bebek sağlığının güvenceye alınması."
                ]
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-18-s80",
        "title": "Bölüm Özeti: Sağlık Ocaklarından Temel Sağlık Hizmetleri ve Alma-Ata'ya Geçiş",
        "content": "Bölüm 8 boyunca Türkiye'nin yokluklar içinden kendi aşısını üreten ve Sağlık Ocakları modeliyle dünyaya ilham veren halk sağlığı serüvenini inceledik:\n\n- **Özet:** Refik Saydam temelleri attı, Nusret Fişek 224 sayılı kanunla sağlık ocaklarını ve aile planlamasını kurdu.\n- **Sonraki Bölüm (Bölüm 9):** Fişek modelinin dünya sahnesindeki küresel yankısı olan **1978 Alma-Ata Bildirgesi'ni, '2000 Yılında Herkese Sağlık' hedefini, Temel Sağlık Hizmetleri (TSH) ilkelerini ve halk sağlığının temel yasalarını** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "1961 yılında çıkarılan ve Türkiye'de sağlık ocakları sistemini, koruyucu hekimlik entegrasyonunu ve sevk zincirini kuran kanunun numarası nedir?",
                "224 sayılı kanun (Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun)",
                "Nusret Fişek'in mimarı olduğu tarihi yasa numarası"
            ),
            make_quiz(
                "Cumhuriyet'in ilk Sağlık Bakanı olan, 1593 sayılı Umumi Hıfzıssıhha Kanunu'nu çıkaran ve Ankara'da yerli aşı üreten Hıfzıssıhha Enstitüsü'nü kuran hekim kimdir?",
                [
                    {"key": "A", "text": "Dr. Refik Saydam", "isCorrect": True, "explanation": "Doğru cevap A'dır: Dr. Refik Saydam Cumhuriyet'in ilk sağlık bakanı ve hıfzıssıhha teşkilatının kurucusudur."},
                    {"key": "B", "text": "Prof. Dr. Nusret Fişek", "isCorrect": False, "explanation": "Fişek 1960'larda sosyalleştirmeyi kurmuştur."},
                    {"key": "C", "text": "Dr. Besim Ömer Paşa", "isCorrect": False, "explanation": "Kadın doğum ve Kızılay öncüsüdür."},
                    {"key": "D", "text": "Dr. Adnan Adıvar", "isCorrect": False, "explanation": "İlk TBMM döneminde kısa süre vekillik yapmıştır."}
                ]
            )
        ]
    })

    return slides
