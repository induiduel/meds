# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 8: Enfeksiyon Zinciri ve Zoonozlar (Slayt 71 - 80)
Checkpoint 8: Slayt 79
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # Slayt 71: Enfeksiyon Zincirinin 6 Temel Halkası
    slides.append({
        "id": "k1-21-s71",
        "title": "Enfeksiyon Zincirinin 6 Temel Halkası",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 71,
        "narrative": (
            "Bir enfeksiyon hastalığının ortaya çıkabilmesi ve toplumda yayılabilmesi, "
            "birbirine bağlı altı halkanın eksiksiz bir şekilde tamamlanmasına bağlıdır. "
            "Epidemiyolojide bu modele **Enfeksiyon Zinciri (Chain of Infection)** adı verilir: "
            "1. **Enfeksiyon Etkeni:** Bakteri, virüs, mantar, parazit veya prion. "
            "2. **Kaynak / Rezervuar:** Patojenin doğal olarak yaşadığı ve çoğaldığı insan, hayvan, su veya toprak. "
            "3. **Kaynaktan Çıkış Kapısı:** Etkenin rezervuarı terk ettiği yol (solunum sekresyonları, dışkı, idrar, kan, genital akıntı, deri lezyonları). "
            "4. **Bulaşma Yolu:** Etkenin kaynaktan yeni konağa taşınma biçimi (doğrudan temas, damlacık, havayolu, vektörler veya kontamine araç-gereçler). "
            "5. **Yeni Konağa Giriş Kapısı:** Etkenin yeni vücuda sızdığı nokta (solunum yolu, gastrointestinal kanal, zedelenmiş deri, mukoza, parenteral enjeksiyon, transplasental). "
            "6. **Duyarlı Konak:** İmmün direnci yetersiz, aşısız veya genetik olarak duyarlı birey. "
            "**Altın Kural:** Bu 6 halkadan herhangi biri tek başına kırılırsa, enfeksiyon döngüsü derhal durur ve hastalık oluşamaz!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Enfeksiyon zincirini oluşturan altı halkadan herhangi biri kırıldığında enfeksiyon hastalığı gelişimi durur.",
                "halkadan herhangi biri",
                "Zincirin tek bir bileşeninin engellenmesinin yeterliliği kuralı"
            ),
            make_causal_chain(
                "Enfeksiyon Zincirinin Akış Halkaları",
                [
                    "1. Etken: Patojen mikroorganizma yaşam döngüsünü sürdürür.",
                    "2. Rezervuar: İnsan veya hayvan rezervuarında çoğalarak birikir.",
                    "3. Çıkış Kapısı: Öksürük, dışkılama veya kanama ile rezervuardan dışarı atılır.",
                    "4. Bulaşma Yolu: Hava, temas, kontamine su veya vektörle çevreye yayılır.",
                    "5. Giriş Kapısı: Yeni konağın mukozasından veya çatlak derisinden içeri sızar.",
                    "6. Duyarlı Konak: İmmünitesi yetersiz konakta doku invazyonu ve hastalık başlar."
                ]
            ),
            make_micro_quiz(
                "Enfeksiyon zinciri modeli ve halk sağlığı önlemleri ile ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?",
                {
                    "A": "El hijyeni ve maske kullanımı - Bulaşma yolunu ve giriş kapısını hedefler",
                    "B": "Toplumun aşılanması - Duyarlı konak halkasını kırar",
                    "C": "Hastaların izolasyonu - Kaynaktan çıkış ve bulaşma halkasını sınırlar",
                    "D": "Klorlama ve su sanitasyonu - Rezervuar ve bulaşma kaynağını yok eder",
                    "E": "Enfeksiyon gelişmesi için altı halkanın yalnızca birinin bulunması yeterlidir"
                },
                "E",
                {
                    "A": "A seçeneği doğrudur; temas ve damlacık bulaşını keser.",
                    "B": "B seçeneği doğrudur; aşılama konağı duyarsız/dirençli hale getirir.",
                    "C": "C seçeneği doğrudur; etkenin yayılımını engeller.",
                    "D": "D seçeneği doğrudur; sucul kaynağı sterilize eder.",
                    "E": "E seçeneği yanlıştır: Enfeksiyon gelişebilmesi için altı halkanın tamamının kesintisiz birbirine bağlanması şarttır; tek bir halkanın kırılması bile enfeksiyonu engeller."
                }
            )
        ]
    })

    # Slayt 72: Bulaşma Yolları: Damlacık vs Havayolu (Airborne)
    slides.append({
        "id": "k1-21-s72",
        "title": "Bulaşma Yolları: Damlacık ile Havayolu (Airborne) Ayrımı",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 72,
        "narrative": (
            "Solunum yoluyla bulaşan enfeksiyonlarda en sık karıştırılan ve hastane enfeksiyon kontrolünde "
            "hayati önem taşıyan ayrım **Damlacık (Droplet)** ile **Havayolu (Airborne / Damlacık Çekirdeği)** farkıdır: "
            "1. **Damlacık Bulaşı (Droplet):** Konuşma, öksürme veya hapşırma ile havaya saçılan **büyük partiküllerdir (> 5 mikron)**. "
            "Ağır oldukları için havada uzun süre asılı kalamazlar; yerçekimi etkisiyle **1 ila 2 metre içinde yere çökerler**. "
            "Bulaşma ancak enfekte kişiyle 1-2 metrelik yakın temas mesafesinde, damlacıkların göz, burun veya ağız mukozasına konmasıyla olur. "
            "Standart cerrahi maske tam koruma sağlar (örneğin İnfluenza, Neisseria meningitidis menenjiti, Boğmaca, RSV). "
            "2. **Havayolu Bulaşı (Airborne / Damlacık Çekirdeği):** Sıvı kısmı buharlaşmış **mikroskobik küçük partiküllerdir (< 5 mikron)**. "
            "Hafif oldukları için hava akımlarıyla saatlerce havada asılı kalabilir ve havalandırma kanallarıyla oda dışına, koridorlara yayılabilirler. "
            "Standart cerrahi maske korumaz; **N95 / FFP2 respiratör maske** ve **negatif basınçlı izolasyon odası** zorunludur! "
            "Havayoluyla bulaşan klasik üçlü: **Tüberküloz (M. tuberculosis), Kızamık (Measles) ve Suçiçeği (Varicella)**'dir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mikroskobik damlacık çekirdekleriyle saatlerce havada asılı kalarak negatif basınçlı oda gerektiren havayolu bulaşının klasik etkeni Mycobacterium tuberculosis basilidir.",
                "Mycobacterium tuberculosis",
                "N95 maske ve negatif basınçlı oda gerektiren tüberküloz etkeni"
            ),
            make_before_after(
                "Damlacık İzolasyonu ile Havayolu (Airborne) İzolasyonu Karşılaştırması",
                "Damlacık Bulaşı (> 5 mikron)",
                [
                    "Partikül boyutu büyüktür, yerçekimiyle 1-2 metre içinde çöker",
                    "Havalandırma kanallarıyla uzak odalara yayılmaz",
                    "Standart tıbbi cerrahi maske takılması yeterlidir",
                    "Örnekler: İnfluenza, Meningokok menenjiti, Boğmaca"
                ],
                "Havayolu Bulaşı (< 5 mikron / Damlacık Çekirdeği)",
                [
                    "Küçük partiküller saatlerce havada asılı kalır ve metrelerce sürüklenir",
                    "Normal oda havasından koridorlara sızabilir",
                    "Özel N95 / FFP2 maske ve negatif basınçlı izolasyon odası şarttır",
                    "Örnekler: Tüberküloz, Kızamık, Suçiçeği (VZV)"
                ]
            ),
            make_micro_quiz(
                "Hastanede yatan bir hastada aktif akciğer tüberkülozu saptandığında enfeksiyon kontrol komitesinin derhal uygulaması gereken izolasyon tipi ve maske standardı hangisidir?",
                {
                    "A": "Standart temas izolasyonu - Eldiven ve önlük",
                    "B": "Damlacık izolasyonu - Standart cerrahi maske ve normal tek kişilik oda",
                    "C": "Solunum (Havayolu / Airborne) izolasyonu - Negatif basınçlı oda ve N95/FFP2 maske",
                    "D": "Ters koruyucu izolasyon - Pozitif basınçlı oda ve steril eldiven",
                    "E": "Yalnızca el dezenfeksiyonu ile normal koğuş takibi"
                },
                "C",
                {
                    "A": "A seçeneği temasla bulaşan dirençli bakteriler içindir.",
                    "B": "B seçeneği tüberküloz için yetersizdir; basil damlacık çekirdeğiyle havada asılı kalır.",
                    "C": "C seçeneği doğrudur: Tüberküloz < 5 mikron damlacık çekirdeği ile bulaşır; saatte 6-12 hava değişimi yapan negatif basınçlı oda ve N95 maske şarttır.",
                    "D": "D seçeneği nötropenik hastaları korumak içindir.",
                    "E": "E seçeneği ölümcül hastane salgınına yol açar."
                }
            )
        ]
    })

    # Slayt 73: Fekal-Oral, Parenteral ve Vertikal Bulaş
    slides.append({
        "id": "k1-21-s73",
        "title": "Fekal-Oral, Parenteral ve Vertikal İletim Yolları",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 73,
        "narrative": (
            "Solunum dışındaki temel enfeksiyon iletim yolları şunlardır: "
            "1. **Fekal-Oral Yol:** Enfekte bireyin dışkısıyla çevreye atılan mikroorganizmaların "
            "kontamine içme suları, gıdalar, kirli eller veya sinekler aracılığıyla duyarlı konağın ağzından girmesidir (5F kuralı: Feces, Fingers, Flies, Foods, Fluids). "
            "Gelişmekte olan ülkelerde çocuk ölümlerinin en sık nedenidir (Hepatit A, Poliovirüs, Kolera, Shigella, Salmonella, Giardia, Rotavirüs). "
            "2. **Parenteral / Kan Yoluyla Bulaş:** Kontamine kan ve kan ürünleri transfüzyonu, steril olmayan iğne ve enjektör paylaşımı "
            "(damar içi madde bağımlıları), dövme, piercing veya sağlık çalışanlarında iğne batması kazalarıyla bulaşır. "
            "Başlıca kan patojenleri: **Hepatit B (HBV), Hepatit C (HCV) ve HIV**'dir. "
            "3. **Vertikal (Anneden Bebeğe) İletim:** Gebelik sırasında transplasental olarak fetüse geçiş "
            "(**TORCH kompleksi**: Toksoplazma, Diğerleri [Sifilis, Parvovirüs], Rubella, Sitomegalovirüs, Herpes), "
            "doğum eyleminde vajinal sekresyonlarla temas (Grup B Streptokok, HSV-2, Klamidya, Gonokok) "
            "veya emzirme yoluyla anne sütünden bulaş (HIV, HTLV-1, CMV)."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Gebelikte anneden transplasental yolla fetüse geçerek konjenital malformasyonlara yol açan patojen grubu TORCH kompleksi olarak adlandırılır.",
                "TORCH kompleksi",
                "Konjenital intrauterin enfeksiyon etkenlerinin klasik akronimi"
            ),
            make_table(
                ["İletim Yolu", "Temel Bulaş Araçları", "Klasik Enfeksiyon Etkenleri"],
                [
                    ["Fekal-Oral Yol", "Kirli su, kontamine gıda, yıkanmamış eller", "Hepatit A, Rotavirüs, Kolera, Shigella, Giardia"],
                    [
                        "Parenteral (Kan) Yolu",
                        {"text": "İğne batması, kan nakli, enjektör paylaşımı", "isMasked": True, "hint": "Damar içi enjeksiyon ve biyolojik sıvı maruziyeti"},
                        "Hepatit B (HBV), Hepatit C (HCV), HIV"
                    ],
                    ["Vertikal (Transplasental)", "Plasenta yoluyla maternal kandan fetüse", "Rubella (Kızamıkçık), Toksoplazma, CMV, Sifilis"]
                ]
            ),
            make_micro_quiz(
                "Acil serviste çalışan bir hemşirenin parmağına Hepatit B pozitif bir hastanın kanlı iğnesi battığında bulaşma yolu hangi kategoriye girer?",
                {
                    "A": "Fekal-oral bulaş",
                    "B": "Damlacık bulaşı",
                    "C": "Parenteral (perkütan) bulaş",
                    "D": "Vektörel bulaş",
                    "E": "Havayolu (airborne) bulaşı"
                },
                "C",
                {
                    "A": "A seçeneği sindirim yoludur.",
                    "B": "B seçeneği solunum yoludur.",
                    "C": "C seçeneği doğrudur: İğne batması, kesici-delici alet yaralanmaları ve kan teması parenteral (perkütan) bulaşma yoludur.",
                    "D": "D seçeneği eklem bacaklı ısırmasıdır.",
                    "E": "E seçeneği aerosol solunmasıdır."
                }
            )
        ]
    })

    # Slayt 74: Zinciri Kırma Stratejileri
    slides.append({
        "id": "k1-21-s74",
        "title": "Enfeksiyon Zincirini Kırma: El Hijyeni ve İzolasyon",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 74,
        "narrative": (
            "Enfeksiyon hastalıklarıyla mücadelenin en temel kuralı, zincirin en zayıf halkasını hedef alarak "
            "döngüyü kırmaktır. Farklı halkalara yönelik kanıtlanmış stratejiler şunlardır: "
            "1. **Bulaşma Yolunu Kırmak - El Hijyeni:** Sağlık hizmeti ilişkili enfeksiyonların (hastane enfeksiyonları) "
            "önlenmesinde dünyadaki **en ucuz, en basit ve en etkili tek yöntem el hijyenidir**! "
            "Ellerin alkol bazlı el dezenfektanları ile ovalanması veya su ve sabunla en az 20-30 saniye yıkanması, "
            "patojenlerin hastadan hastaya taşınmasını %50'den fazla azaltır. "
            "(Önemli İstisna: Clostridioides difficile sporları ve Norovirüs alkole dirençlidir; bu vakalarda mutlaka **su ve sabunla mekanik yıkama** şarttır!). "
            "2. **Çıkış Kapısı ve Bulaşı Kırmak - İzolasyon Önlemleri:** Standart önlemler, temas izolasyonu (önlük/eldiven), "
            "damlacık izolasyonu (cerrahi maske) ve solunum izolasyonu (negatif basınç, N95). "
            "3. **Duyarlı Konağı Korumak - İmmünizasyon:** Aşılar toplumda duyarlı birey sayısını azaltır; "
            "aşılama oranı belirli bir eşiği aştığında aşılanamayan bebek ve kanser hastalarını da koruyan **Toplumsal (Sürü) Bağışıklık (Herd Immunity)** oluşur."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Hastanelerde enfeksiyonların hastadan hastaya çapraz bulaşmasını engellemede en etkili ve ucuz yöntem el hijyenidir.",
                "el hijyenidir",
                "Semmelweis'tan bu yana hastane enfeksiyonunu önleyen temel uygulama"
            ),
            make_table(
                ["Enfeksiyon Zinciri Halkası", "Uygulanan Halk Sağlığı Müdahalesi", "Hedeflenen Amaç"],
                [
                    ["Rezervuar / Kaynak", "Vaka tespiti, izolasyon ve taşıyıcı tedavisi", "Mikrop kaynağının çevreye saçılımını kesmek"],
                    [
                        "Bulaşma Yolu",
                        {"text": "El hijyeni, dezenfeksiyon, maske, su klorlama", "isMasked": True, "hint": "Ajanın yeni kişiye transferini durdurma"},
                        "Patojenin kaynaktan yeni konağa geçişini fiziksel engellemek"
                    ],
                    ["Duyarlı Konak", "Genişletilmiş aşılama programları ve profilaksi", "Toplumsal bağışıklık eşiğini aşarak duyarlılığı sıfırlamak"]
                ]
            ),
            make_micro_quiz(
                "Clostridioides difficile psödomembranöz koliti olan bir hastanın odasından çıkan sağlık personelinin el hijyeninde alkollü el antiseptiği yerine 'su ve sabunla yıkamayı' tercih etmesinin mikrobiyolojik nedeni nedir?",
                {
                    "A": "Alkolün C. difficile vejetatif hücrelerini aşırı çoğaltması",
                    "B": "C. difficile endosporlarının alkole dirençli olması ve ancak su-sabunla mekanik olarak uzaklaştırılabilmesi",
                    "C": "Su ve sabunun C. difficile DNA'sını doğrudan parçalaması",
                    "D": "Hastanede alkol tüketimini azaltmak",
                    "E": "C. difficile'in yalnızca soğuk suda ölebilmesi"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; alkol bakteriyi beslemez.",
                    "B": "B seçeneği doğrudur: Bakteriyel endosporlar alkollü dezenfektanlarla inaktive edilemez; su ve sabunla sürtünerek ellerden mekanik olarak akıtılmalıdır.",
                    "C": "C seçeneği yanlıştır; sabun kimyasal sporosidal değildir, mekanik temizlik yapar.",
                    "D": "D seçeneği tıbbi gerekçe değildir.",
                    "E": "E seçeneği yanlıştır."
                }
            )
        ]
    })

    # Slayt 75: Zoonotik Enfeksiyonlar: Tanım ve Küresel Önem
    slides.append({
        "id": "k1-21-s75",
        "title": "Zoonozlar: Hayvanlardan İnsanlara Bulaşan Tehditler",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 75,
        "narrative": (
            "Omurgalı hayvanlardan insanlara doğal koşullar altında doğrudan veya dolaylı olarak bulaşan "
            "enfeksiyon hastalıklarına **Zoonoz (Zoonotik Enfeksiyon)** adı verilir. "
            "İnsanlarda görülen tüm enfeksiyon hastalıklarının yaklaşık %60'ı, yeni ortaya çıkan (emerging) "
            "enfeksiyonların ise %75'i zoonotik kökenlidir! "
            "Zoonozlar insan hekimliği ile veteriner hekimliğin ayrılmaz bir bütün olduğunu savunan "
            "**Tek Sağlık (One Health)** konseptinin merkezinde yer alır. "
            "Zoonozların bulaşma yolları son derece çeşitlidir: "
            "Enfekte hayvanın ısırması veya tırmalaması (kuduz, kedi tırmığı), "
            "enfekte hayvan dokularına veya salgılarına doğrudan temas (şarbon, bruselloz), "
            "pastörize edilmemiş süt ve süt ürünlerinin tüketimi (bruselloz, Q ateşi, tüberküloz bovis), "
            "az pişmiş etlerin yenmesi (trişinoz, tenyazis, toksoplazmoz) "
            "veya hayvanlardan kan emen artropod vektörler aracılığıyla (KKKA, Lyme, leishmaniasis). "
            "Zoonozların çoğunda insan bir 'son konak'tır (dead-end host); yani hastalık insandan insana kolay kolay yayılmaz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Omurgalı hayvanlar ile insanlar arasında doğal olarak bulaşabilen enfeksiyon hastalıklarına zoonoz adı verilir.",
                "zoonoz",
                "Hayvan kaynaklı enfeksiyon hastalıklarının genel tıbbi adı"
            ),
            make_before_after(
                "Antroponoz ile Zoonoz Karşılaştırması",
                "Antroponoz (İnsana Özgü Enfeksiyonlar)",
                [
                    "Rezervuar yalnızca insandır (hayvan rezervuarı yoktur)",
                    "Bulaşma insandan insana gerçekleşir",
                    "Aşılama ile yeryüzünden tamamen eradike edilebilir",
                    "Örnekler: Çiçek hastalığı (Variola), Çocuk felci (Polio), Kızamık"
                ],
                "Zoonoz (Hayvan Kaynaklı Enfeksiyonlar)",
                [
                    "Doğal rezervuar yabani veya evcil omurgalı hayvanlardır",
                    "İnsan genellikle tesadüfi son konaktır (dead-end host)",
                    "Doğadaki hayvan rezervuarı sürdüğü için eradikasyonu imkansıza yakındır",
                    "Örnekler: Kuduz, Şarbon, Bruselloz, Tularemi, KKKA"
                ]
            ),
            make_active_recall(
                "İnsan sağlığı, hayvan sağlığı ve çevre sağlığının birbirinden ayrılamaz bir bütün olduğunu savunan modern halk sağlığı yaklaşımı hangisidir?",
                "Tek Sağlık (One Health) yaklaşımıdır.",
                "İnsan-hayvan-çevre entegre sağlık konsepti"
            )
        ]
    })

    # Slayt 76: Çiftlik Hayvanları Kaynaklı Zoonozlar
    slides.append({
        "id": "k1-21-s76",
        "title": "Çiftlik Hayvanları Kaynaklı Zoonozlar: Brusella, Şarbon ve Q Ateşi",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 76,
        "narrative": (
            "Kırsal bölgelerde sığır, koyun ve keçilerle temas eden veya bunların ürünlerini tüketenlerde gelişen majör zoonozlar: "
            "1. **Bruselloz (Malta Humması / Dalgalı Ateş):** Etkenleri Brucella melitensis (koyun/keçi - en virülan), "
            "B. abortus (sığır) ve B. suis'tir. En sık **çiğ sütten yapılmış taze peynir ve krema tüketimiyle** bulaşır. "
            "Fakültatif hücre içi bakteridir; dalgalı (undülan) ateş, gece terlemesi, hepatosplenomegali ve en sık iskelet komplikasyonu olarak **sakroileit** yapar. "
            "2. **Şarbon (Anthrax - Bacillus anthracis):** Sporlu Gram-pozitif büyük basildir. Enfekte hayvan derisi, kılı ve yünüyle temas sonucu bulaşır. "
            "En sık formu deride ağrısız, kaşıntılı, çevresi ödemli ve merkezinde siyah nekrotik kabuk bulunan **Kutanöz Şarbon (Malign Püstül)**'dür. "
            "Sporların solunmasıyla gelişen Akciğer Şarbonu (Yün Eğirici Hastalığı) masif hemorajik mediastinite yol açar. "
            "3. **Q Ateşi (Coxiella burnetii):** Enfekte koyun/keçilerin doğum sıvıları ve plasentasındaki spor benzeri partiküllerin solunmasıyla bulaşır; "
            "kültür negatif endokarditin ve atipik pnömoninin önemli bir nedenidir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Çiğ sütten yapılan taze peynir tüketimi sonrası dalgalı ateş ve sakroileit ile başvuran hastada en olası etken Brucella melitensis bakterisidir.",
                "Brucella melitensis",
                "Malta humması yapan koyun-keçi kaynaklı hücre içi bakteri"
            ),
            make_table(
                ["Çiftlik Zoonozu", "Rezervuar Hayvan ve Bulaş Yolu", "Karakteristik Klinik Tablo"],
                [
                    [
                        "Bruselloz (Malta Humması)",
                        "Koyun, keçi, sığır; pastörize edilmemiş süt/peynir",
                        {"text": "Dalgalı ateş, sakroileit ve splenomegali", "isMasked": True, "hint": "Gece terlemesi ve eklem tutulumu"}
                    ],
                    ["Şarbon (Kutanöz Form)", "Sığır, koyun derisi ve yünüyle temas", "Ağrısız siyah nekrotik eskar lezyonu (Malign püstül)"],
                    ["Şarbon (İnhalasyon Formu)", "Yün eğiricilerde spor solunması", "Genişlemiş mediastinum ve hemorajik mediastinit"],
                    ["Q Ateşi (Coxiella)", "Koyun/keçi doğum sıvısı aerosolü", "Atipik pnömoni, hepatit ve kültür-negatif endokardit"]
                ]
            ),
            make_micro_quiz(
                "Koyun kırkımı ve yün ticareti ile uğraşan bir çobanın el bileğinde kaşıntılı bir papül olarak başlayan, daha sonra çevresinde veziküller ve merkezinde ağrısız siyah nekrotik bir kabuk (eskar) gelişen lezyonun etkeni hangisidir?",
                {
                    "A": "Bacillus anthracis",
                    "B": "Brucella abortus",
                    "C": "Coxiella burnetii",
                    "D": "Francisella tularensis",
                    "E": "Listeria monocytogenes"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Bacillus anthracis kutanöz şarbonda klasik ağrısız siyah nekrotik eskar (kömür karası / anthrax) oluşturur.",
                    "B": "B seçeneği brusellozdur, deri eskarı yapmaz.",
                    "C": "C seçeneği Q ateşidir.",
                    "D": "D seçeneği ağrılı ülseroglandüler lezyon yapar.",
                    "E": "E seçeneği menenjit yapar."
                }
            )
        ]
    })

    # Slayt 77: Evcil Hayvanlar (Kedi ve Köpek) Kaynaklı Zoonozlar
    slides.append({
        "id": "k1-21-s77",
        "title": "Evcil Hayvan Kaynaklı Zoonozlar: Kedi ve Köpek Tehditleri",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 77,
        "narrative": (
            "Evlerimizde birlikte yaşadığımız kedi ve köpekler de belirli ölümcül patojenlerin taşıyıcısıdır: "
            "1. **Kuduz Virüsü (Rabies - Rhabdoviridae):** Enfekte köpeğin (veya yarasa, tilki) ısırmasıyla tükürükten bulaşır. "
            "Kas dokusunda çoğaldıktan sonra periferik sinir aksonları boyunca retrograd taşınmayla beyne ulaşır. "
            "Aşırı tükürük salgısı, yutma spazmı, sudan korkma (**hidrofobi**), ajitasyon ve koma ile seyreder. "
            "Klinik belirtiler başladıktan sonra mortalite %100'e yakındır; şüpheli temasta acil yara yıkama, aşı ve kuduz immünglobulini (RIG) hayat kurtarır! "
            "2. **Kistik Ekinokokkoz (Echinococcus granulosus):** Köpek bağırsağında yaşayan küçük tenyanın yumurtalarıyla bulaşır; insanda karaciğer ve akciğer hidatik kisti yapar. "
            "3. **Toksoplazmoz (Toxoplasma gondii):** Kedilerin dışkısıyla atılan ookistlerle bulaşır. "
            "4. **Kedi Tırmığı Hastalığı (Bartonella henselae):** Kedi tırmalaması veya ısırması sonrası bölgesel lenf bezlerinde "
            "haftalarca süren granülomatöz ve süpüratif lenfadenopati (LAP) yapar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Kedi tırmalaması sonrası bölgesel lenf nodlarında subakut ağrılı lenfadenit yapan bakteri Bartonella henselae bakterisidir.",
                "Bartonella henselae",
                "Kedi tırmığı hastalığının etkeni olan gram-negatif basil"
            ),
            make_causal_chain(
                "Kuduz Virüsünün Nöroinvazyon Mekanizması",
                [
                    "1. Isırık Teması: Kuduz hayvanın tükürüğündeki virüs ısırık yarasından kas dokusuna girer.",
                    "2. Kas İçi Replikasyon: Virüs nöromusküler kavşağa yakın çizgili kas hücrelerinde çoğalır.",
                    "3. Retrograd Aksonal Taşınma: Motor sinir uçlarına bağlanarak günde 1-2 cm hızla omuriliğe tırmanır.",
                    "4. Santral Sinir Sistemi Tutulumu: Beyin sapı, limbik sistem ve hipokampusta Negri cisimcikleri oluşturur.",
                    "5. Fatal Ensefalit: Hidrofobi, laringeal spazm, solunum arresti ve ölüm gerçekleşir."
                ]
            ),
            make_active_recall(
                "Kuduz virüsünün enfekte ettiği nöronların sitoplazmasında ışık mikroskobunda izlenen patognomonik eozinofilik inklüzyon cisimciklerine ne ad verilir?",
                "Negri cisimcikleri (Negri bodies) adı verilir.",
                "Kuduz histopatolojisinin klasik intrasitoplazmik inklüzyonu"
            )
        ]
    })

    # Slayt 78: Kemirici ve Kuş Kaynaklı Zoonozlar
    slides.append({
        "id": "k1-21-s78",
        "title": "Kemirici ve Kuş Zoonozları: Veba, Leptospiroz, Hantavirüs",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 78,
        "narrative": (
            "Yabani kemiriciler (fare, sıçan) ve kuşlar insan yerleşimlerine yakın yaşadıklarında ölümcül salgınların kaynağı olurlar: "
            "1. **Leptospiroz (Leptospira interrogans):** Kemiricilerin böbrek tübüllerinde asemptomatik yaşar ve idrarlarıyla sulara saçılır. "
            "Çiftçiler, kanalizasyon işçileri veya su sporcuları kontamine suya temas ettiklerinde derideki sıyrıklardan veya konjonktivadan girer. "
            "Ağır formuna **Weil Sendromu** denir: Sarılık, akut böbrek yetmezliği, pulmoner kanama ve **konjonktival süfüzyon** (gözde kızarıklık) ile seyreder. "
            "2. **Hantavirüs Enfeksiyonları:** Kemirici dışkı ve idrarının kuruyup toz haline gelerek aerosol olarak solunmasıyla bulaşır. "
            "Avrasya'da Kanamalı Ateşle Seyreden Böbrek Sendromu (HFRS); Amerika'da ise fatal pulmoner ödemle giden Hantavirüs Pulmoner Sendromu (HPS) yapar. "
            "3. **Kuş Zoonozları:** Güvercin dışkısıyla zengin topraklarda Cryptococcus neoformans ürer. "
            "Göçmen su kuşları yüksek patojeniteli **Avian İnfluenza (Kuş Gribi - H5N1)** virüslerinin doğal rezervuarıdır. "
            "Kafes kuşları ise Chlamydia psittaci ile psittakoz bulaştırır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Kemirici idrarıyla kirlenmiş sularla temas sonrası sarılık, böbrek yetmezliği ve konjonktival süfüzyonla seyreden ağır leptospiroz tablosuna Weil sendromu denir.",
                "Weil sendromu",
                "Leptospira interrogans kaynaklı ikterik kanamalı tablo"
            ),
            make_table(
                ["Rezervuar Canlı", "Bulaştırdığı Majör Patojen", "Karakteristik Klinik Tablo"],
                [
                    [
                        "Kemirici İdrarı (Sıçan)",
                        "Leptospira interrogans",
                        {"text": "Weil sendromu (Sarılık ve böbrek yetmezliği)", "isMasked": True, "hint": "Gözde süfüzyon ve nefrit yapan spiroket"}
                    ],
                    ["Kemirici Dışkı Aerosolü", "Hantavirüs", "Kanamalı ateşle seyreden böbrek sendromu (HFRS)"],
                    ["Kafes Kuşları (Papağan)", "Chlamydia psittaci", "Psittakoz (Splenomegalili atipik pnömoni)"],
                    ["Yabani Su Kuşları", "Avian İnfluenza A (H5N1)", "Kuş gribi, akut solunum sıkıntısı sendromu (ARDS)"]
                ]
            ),
            make_micro_quiz(
                "Sel baskını sonrası çeltik tarlasında çalışan bir tarım işçisinde yüksek ateş, bacak kaslarında şiddetli ağrı, sarılık, kreatinin yüksekliği ve gözlerde belirgin konjonktival kızarıklık (süfüzyon) saptanıyor. En olası tanı nedir?",
                {
                    "A": "Leptospiroz (Weil hastalığı)",
                    "B": "Hepatit A",
                    "C": "Bruselloz",
                    "D": "Kuduz",
                    "E": "Tifo"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Kemirici idrarı karışmış su teması, sarılık, nefrit ve konjonktival süfüzyon birlikteliği Leptospiroz (Weil hastalığı) için klasiktir.",
                    "B": "B seçeneği nefrit ve konjonktival süfüzyon yapmaz.",
                    "C": "C seçeneği çiğ sütten geçer, akut sarılık-nefrit tablosu nadirdir.",
                    "D": "D seçeneği hidrofobi yapar.",
                    "E": "E seçeneği bağırsak perforasyonu yapar."
                }
            )
        ]
    })

    # Slayt 79: [TEKRAR SAYFASI - CHECKPOINT 8]
    slides.append({
        "id": "k1-21-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Enfeksiyon Zinciri ve Zoonozlar",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 79,
        "narrative": (
            "Bu sekizinci checkpoint sayfasında enfeksiyon zincirinin kırılma prensiplerini, "
            "damlacık ile havayolu (tüberküloz) izolasyon standartları arasındaki N95 farkını, "
            "çiğ süt kaynaklı Brusella ve köpek kaynaklı kist hidatik zoonozlarını "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp8-1",
                "Damlacık bulaşı ile havayolu (airborne / damlacık çekirdeği) bulaşı arasındaki partikül boyutu, mesafe ve maske farkı nedir?",
                "Damlacık partikülleri büyüktür (>5 µm), 1-2 metrede çöker ve cerrahi maskeyle korunulur. Havayolu partikülleri küçüktür (<5 µm), saatlerce havada asılı kalır; N95/FFP2 maske ve negatif basınçlı oda gerektirir.",
                "Tanecik çap sınırı ile ortamda süzülme süresine göre filtre tercihi",
                "İzolasyon İlkeleri"
            ),
            make_flashcard(
                "fc-k1-21-cp8-2",
                "Bruselloz (Malta Humması) insanlara en sık hangi yolla bulaşır ve en karakteristik klinik bulguları nelerdir?",
                "Pastörize edilmemiş çiğ sütten yapılan taze peynir ve süt ürünlerinin tüketimiyle bulaşır. Dalgalı (undülan) ateş, gece terlemesi, hepatosplenomegali ve sakroileit ile karakterizedir.",
                "Kaynatılmamış mandıra besinleri, inişli çıkışlı termal pikler ve leğen kemiği eklemi inflamasyonu",
                "Çiftlik Zoonozları"
            ),
            make_flashcard(
                "fc-k1-21-cp8-3",
                "Kuduz şüpheli bir hayvan ısırığı sonrasında derhal yapılması gereken ilk acil tıbbi müdahale nedir?",
                "Isırık yarasının derhal bol basınçlı su ve sabunla en az 15 dakika boyunca yıkanması ve ardından aşı ile kuduz immünglobulin profilaksisinin planlanmasıdır.",
                "Travma odağının köpüklü tazyikli sıvıyla arındırılması ve acil seroterapi tedbiri",
                "Kuduz Profilaksisi"
            )
        ]
    })

    # Slayt 80: Tularemi ve Zoonozlar Bölüm Özeti
    slides.append({
        "id": "k1-21-s80",
        "title": "Tularemi (Avcı Hastalığı) ve Zoonozlar Bölüm Özeti",
        "section": "Enfeksiyon Zinciri ve Zoonozlar",
        "slideNumber": 80,
        "narrative": (
            "Zoonozlar bahsini kapatırken Türkiye'de su kaynaklı salgınlar yapan **Tularemiyi** incelemek şarttır: "
            "Etkeni küçük Gram-negatif kokobasil olan **Francisella tularensis**'tir. "
            "Doğal rezervuarı **yabani tavşanlar ve kemiricilerdir** (Avcı hastalığı). "
            "İnfeksiyöz dozu aşırı düşüktür (10 bakteri bile hastalık başlatabilir; potansiyel biyoterör ajanıdır). "
            "Bulaş yolları; enfekte tavşan etinin/derisinin yüzülmesi, kene/sivrisinek ısırıkları veya kemirici ölülerinin "
            "karıştığı klorlanmamış köy şebeke sularının içilmesidir. "
            "En sık formu; temas yerinde ağrılı nekrotik ülser ve bölgesel lenfadenitle seyreden **Ülseroglandüler Tularemi**; "
            "kirli suların içilmesiyle gelişen formu ise boğazda membran ve boyunda dev lenfadenitle giden **Orofarengeal Tularemi**'dir. "
            "Özetle; mikroorganizmalar hayvan rezervuarlarından çıkıp zincirin halkalarını aşarak insana ulaşır. "
            "Peki vücuda giren bir mikrop insan dokusunda nasıl bir zaman çizelgesi izler? "
            "Dokuzuncu bölümümüzde **enfeksiyon hastalığının doğal seyrini ve inkübasyondan nekahate klinik evrelerini** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Yabani tavşan teması veya kontamine köy içme sularıyla bulaşarak boyunda süpüratif lenfadenit yapan etken Francisella tularensis bakterisidir.",
                "Francisella tularensis",
                "Avcı hastalığı ve su kaynaklı tularemi etkeni kokobasil"
            ),
            make_table(
                ["Klinik Tularemi Formu", "Giriş Yolu ve Bulaş Kaynağı", "Tipik Fizik Muayene Bulgusu"],
                [
                    ["Ülseroglandüler Form", "Tavşan derisi yüzme veya kene ısırığı", "Deri inokülasyon yerinde ağrılı ülser ve süpüratif bölgesel LAP"],
                    [
                        "Orofarengeal Form",
                        {"text": "Kontamine şebeke sularının içilmesi", "isMasked": True, "hint": "Su kaynaklı tularemi salgın formu"},
                        "Eksüdatif farenjit, tonsillit ve masif ağrılı servikal lenfadenit"
                    ],
                    ["Pnömonik Form", "Aerosollerin solunması (laboratuvar kazası)", "Yüksek mortaliteli nekrotizan atipik pnömoni"]
                ]
            ),
            make_micro_quiz(
                "Klorlanmamış kaynak suyu tüketen bir köyde çok sayıda köylüde boğaz ağrısı, tonsillerde beyaz eksüda ve boyunda antibiyotiklere yanıtsız dev boyutta ağrılı lenfadenopatiler gelişiyor. En olası tanı nedir?",
                {
                    "A": "Orofarengeal Tularemi (Francisella tularensis)",
                    "B": "Streptokoksik farenjit",
                    "C": "Kuduz",
                    "D": "Leptospiroz",
                    "E": "Tifo"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Türkiye'de klorlanmamış köy sularıyla bulaşan orofarengeal tularemi salgınları penisiline dirençli servikal LAP ile karakterizedir.",
                    "B": "B seçeneği beta-laktamlara hızla yanıt verir ve epidemik su kaynaklı lenfadenit yapmaz.",
                    "C": "C seçeneği ısırıkla bulaşır.",
                    "D": "D seçeneği sarılık yapar.",
                    "E": "E seçeneği bağırsak tutar."
                }
            )
        ]
    })

    return slides
