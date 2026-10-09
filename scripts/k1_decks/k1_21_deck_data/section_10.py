# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 10: Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet (Slayt 91 - 100)
Checkpoint 10: Slayt 100
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: Mikrobiyolojik Tanı Yöntemleri I: Direkt Mikroskopi ve Kültür
    slides.append({
        "id": "k1-21-s91",
        "title": "Mikrobiyolojik Tanı Yöntemleri I: Direkt Mikroskopi ve Kültür",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 91,
        "narrative": (
            "Enfeksiyon hastalıklarının kesin tanısı klinik şüphenin laboratuvar verileriyle kanıtlanmasına dayanır. "
            "Geleneksel mikrobiyolojide ilk ve en hızlı adım **direkt mikroskopidir**. "
            "Gram boyama bakterileri hücre duvarı yapısına göre mor boyanan Gram-pozitifler ve pembe boyanan Gram-negatifler "
            "olarak saniyeler içinde ayırır; mikroskop başında lökosit varlığı inflamasyonun kanıtıdır. "
            "Asido-rezistan basil (ARB) için Ziehl-Neelsen boyası tüberküloz mikobakterilerini gösterirken, "
            "kapsüllü Cryptococcus mantarları için çini mürekkebi kullanılır. "
            "Bakteriyolojide **altın standart tanı yöntemi kültürdür**. "
            "Klinik örnek zenginleştirilmiş besiyerlerine (kanlı agar, çikolata agar, MacConkey/EMB agar) ekilerek "
            "canlı bakteri kolonileri üretilir; etken tür düzeyinde identifiye edilir ve antibiyotik duyarlılık testi (antibiyogram) "
            "yapılarak hedefe yönelik akılcı tedavi belirlenir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Bakteriyel enfeksiyonların kesin tanısında canlı mikroorganizmanın besiyerinde üretildiği kültür yöntemi altın standarttır.",
                "kültür yöntemi",
                "Canlı patojenin koloniler halinde üretilip antibiyograma tabi tutulması"
            ),
            make_causal_chain(
                "Mikrobiyolojik Örnekten Kesin Tanıya Kültür Aşamaları",
                [
                    "1. Doğru Örnekleme: Enfeksiyon odağından aseptik kurallarla numune alınır.",
                    "2. Direkt Yayma: Gram boyama ile mor/pembe bakteri morfolojisi ön tanı verir.",
                    "3. Katı Besiyerine Ekim: Kanlı veya çikolata agarda 37 derecede 18-24 saat inkübe edilir.",
                    "4. Koloni İdentifikasyonu: Biyokimyasal veya MALDI-TOF kütle spektrometrisi ile tür saptanır.",
                    "5. Antibiyogram: Disk difüzyon veya MİK ile en duyarlı antibiyotik raporlanır."
                ]
            ),
            make_table(
                "Temel Mikroskopi Boyama Yöntemleri ve Hedefleri",
                ["Boyama Yöntemi", "Temel İlkesi / Boyar Madde", "Ayırt Edilen Mikroorganizma Grubu"],
                [
                    ["Gram Boyama", "Kristal viyole ve safranin", "Hücre duvarına göre Gram-pozitif mor / Gram-negatif pembe"],
                    [
                        "Ziehl-Neelsen (ARB)",
                        {"text": "Karbol fuksin ve asit-alkol direnci", "isMasked": True, "hint": "Mikobakteriyel balmumu tabakasını hedefleyen boyama tekniği"},
                        "Mycobacterium tuberculosis ve diğer atipik mikobakteriler"
                    ],
                    ["Çini Mürekkebi", "Negatif boyama (arka plan siyah)", "Cryptococcus neoformans (Kapsül negatif boyanır)"],
                    ["Giemsa Boyama", "Metilen mavisi ve eozin türevleri", "Plasmodium sıtma parazitleri ve Leishmania amastigotları"]
                ]
            )
        ]
    })

    # Slayt 92: Serolojik Tanı İlkeleri: Antijen ve Antikor Dinamikleri
    slides.append({
        "id": "k1-21-s92",
        "title": "Serolojik Tanı İlkeleri: Antijen ve Antikor Dinamikleri",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 92,
        "narrative": (
            "Kültürde üretilmesi zor veya aylar süren mikroorganizmalarda (virüsler, Brucella, Treponema pallidum, "
            "Borrelia, Toxoplasma) **serolojik tanı** yöntemleri devreye girer. "
            "Seroloji, serumda patojene ait antijenlerin (ör. HBsAg, Cryptococcus kapsül antijeni) veya konağın "
            "ürettiği spesifik antikorların (ELISA, aglütinasyon, immünofloresan) saptanmasına dayanır. "
            "**Serolojik Tanının Temel Kuralları:** "
            "1. **Spesifik IgM Pozitifliği:** Akut ve yakın zamanda geçirilmekte olan primer enfeksiyonun göstergesidir; "
            "haftalar içinde kandan kaybolur. "
            "2. **Spesifik IgG Pozitifliği:** Geçirilmiş enfeksiyonu, kronikleşmeyi veya aşılamaya bağlı kalıcı bağışıklığı gösterir. "
            "3. **Titre Artışı Kuralı:** Tek başına IgG pozitifliği akut/geçirilmiş ayrımı yapamaz. Akut fazda ve 2-3 hafta sonra "
            "(nekahat evresinde) alınan çift serum örneğinde spesifik IgG antikor titresinde **en az 4 kat artış (serokonversiyon)** "
            "saptanması taze akut enfeksiyonun kesin kanıtıdır!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Akut enfeksiyonun serolojik kanıtı için çift serum örneğinde spesifik antikor titresinde en az 4 kat artış gösterilmelidir.",
                "en az 4 kat artış",
                "İki serum numunesi arasındaki diagnostik katlanma eşiği"
            ),
            make_before_after(
                "Akut Faz IgM ile İyileşme Fazı IgG Antikor Dinamiği",
                "Akut Faz Antikor Yanıtı (IgM)",
                "İlk 1-2 haftada sentezlenir, pentamerik yapısıyla aviditesi düşüktür; akut enfeksiyonun ilk serolojik işaretidir.",
                "Kalıcı Bağışıklık Yanıtı (IgG)",
                "3-4. haftalarda pik yapar, yüksek afiniteye sahiptir; plasentayı geçer ve yıllarca koruyucu hafıza sağlar.",
                "Erken dönem geçici savunma ile uzun süreli bağışık bellek antikorunun farkı"
            ),
            make_active_recall(
                "Klinik pratikte tek bir serum örneğinde bakılan spesifik IgG pozitifliği neden taze akut enfeksiyon tanısı koyduramaz?",
                "Çünkü IgG antikorları aylar veya yıllar önce geçirilmiş eski bir enfeksiyonun veya geçmiş aşılamanın kalıntısı olabilir.",
                "Kalıcı hafıza antikorunun zamanlama belirsizliği"
            )
        ]
    })

    # Slayt 93: Moleküler Tanı Devrimi: Polimeraz Zincir Reaksiyonu (PCR)
    slides.append({
        "id": "k1-21-s93",
        "title": "Moleküler Tanı Devrimi: Polimeraz Zincir Reaksiyonu (PCR)",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 93,
        "narrative": (
            "Moleküler biyoloji teknikleri, enfeksiyon hastalıkları tanısında hız ve duyarlılık devrimi yaratmıştır. "
            "Bu yöntemlerin başında gelen **Polimeraz Zincir Reaksiyonu (PCR)**, klinik örnekte bulunan patojene özgü "
            "DNA veya RNA (RT-PCR) dizilerini in vitro ortamda milyonlarca kez çoğaltarak saptar. "
            "**Moleküler Testlerin Devrimsel Üstünlükleri:** "
            "- **Olağanüstü Hız:** Kültürde üremesi haftalar süren Mycobacterium tuberculosis veya hiç üremeyen Hepatit C, "
            "SARS-CoV-2 ve HIV virüsleri birkaç saat içinde kesin olarak tanımlanır. "
            "- **Yüksek Duyarlılık:** Çok düşük inokulumdaki (mililitrede birkaç kopya) nükleik asit moleküllerini bile yakalar. "
            "- **Viral Yük Ölçümü (Kantitatif Real-Time PCR):** Hastalığın şiddetini, prognozunu ve antiviral tedavinin "
            "başarısını (ör. HIV ve HBV viral yük baskılanması) sayısal kopya sayısı ile izlemeyi sağlar. "
            "- **Direnç Genlerinin Hızlı Tespiti:** Bakterinin üremesini beklemeden rifampisin (rpoB) veya metisilin (mecA) "
            "direnç genlerini direkt kanda veya balgamda tespit edebilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Patojene ait genetik materyalin çoğaltılarak saptandığı ve viral yük takibinde kullanılan yöntem polimeraz zincir reaksiyonudur.",
                "polimeraz zincir reaksiyonudur",
                "Nükleik asit amplifikasyon tekniği"
            ),
            make_table(
                "Mikrobiyolojik Tanı Yöntemlerinin Karşılaştırmalı Gücü",
                ["Yöntem Türü", "Uygulama Hızı", "Duyarlılık / Özgüllük", "En Büyük Avantajı"],
                [
                    ["Gram Mikroskopi", "10 - 15 dakika", "Düşük / Orta", "Yatak başında derhal ön fikir vermesi"],
                    [
                        "Bakteri Kültürü",
                        "24 - 72 saat",
                        "Yüksek (Altın standart)",
                        {"text": "Canlı bakteri antibiyogramı yapılabilmesi", "isMasked": True, "hint": "İlaç duyarlılık testinin üreyen izolat üzerinde uygulanması"}
                    ],
                    ["Seroloji (ELISA)", "Saatler", "Orta / Yüksek", "Kültürü yapılamayan mikroplarda dolaylı tanı"],
                    ["Moleküler (RT-PCR)", "1 - 3 saat", "Çok Yüksek", "Kopya düzeyinde viral yük ve direnç geni tayini"]
                ]
            ),
            make_micro_quiz(
                "Moleküler tanı yöntemleri (Real-Time PCR) ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Kültürü yapılamayan veya son derece yavaş üreyen viral ve bakteriyel etkenleri hızla saptar",
                    "B": "Kantitatif ölçüm sayesinde kanda viral yük takibi ve tedavi yanıtı değerlendirilebilir",
                    "C": "Canlı patojen ile ölü patojene ait nükleik asit artıklarını her zaman mükemmelen ayırt eder",
                    "D": "Genomik mutasyonları ve antibiyotik direnç genlerini (mecA, rpoB) tespit edebilir",
                    "E": "Geleneksel serolojik testlere göre pencere döneminde tanı koyma şansı çok daha yüksektir"
                },
                "C",
                "Doğru cevap C'dir: PCR nükleik asit dizilerini çoğalttığı için ortamda ölü mikrop artıklarına ait DNA parçaları kalsa bile pozitif çıkabilir; dolayısıyla canlı ve ölü patojen ayrımını her zaman yapamaz. A, B, D ve E moleküler testlerin gerçek üstünlükleridir."
            )
        ]
    })

    # Slayt 94: Kan Kültürü Alma İlkeleri ve Sepsis Tanısı
    slides.append({
        "id": "k1-21-s94",
        "title": "Kan Kültürü Alma İlkeleri ve Sepsis Tanısı",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 94,
        "narrative": (
            "Dolaşım sistemine bakteri (bakteriyemi) veya mantar (fungemi) karışması sepsisin habercisidir ve "
            "acil tanı gerektirir. **Kan kültürü**, bakteriyemi tanısında tıbbın en değerli laboratuvar testidir; "
            "ancak tek bir teknik hata sonucu kontaminasyona veya yalancı negatifliğe sürükleyebilir. "
            "**Kan Kültürü Alımının 5 Altın Kuralı:** "
            "1. **Zamanlama:** Kan örnekleri mutlaka **ateşin yükselmeye başladığı (titreme anı)** dönemde alınmalıdır; "
            "bakteri yükünün kanda en yoğun olduğu an bu andır. "
            "2. **Antibiyotik Öncesi:** Numune antibiyotik tedavisi başlanmadan ÖNCE alınmalıdır (antibiyotik mikrobu öldürerek üremeyi engeller). "
            "3. **Mükemmel Antisepsi:** Ven ponksiyon bölgesi %70 alkol ve ardından klorheksidin/iyot ile en az 1-2 dakika dezenfekte edilmeli, kuruması beklenmelidir. "
            "4. **İki Ayrı Giriş (Set Kuralı):** En az 2 farklı damardan (sağ ve sol kol), her sette bir aerop ve bir anaerop şişe olacak şekilde kan alınır. "
            "5. **Yeterli Hacim:** Yetişkinlerde her şişeye 8-10 ml kan verilmelidir; yetersiz hacim tanı duyarlılığını ciddi oranda düşürür."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Kan kültürü alınırken yalancı negatifliği önlemek için kan mutlaka antibiyotik tedavisi başlanmadan önce alınmalıdır.",
                "antibiyotik tedavisi",
                "Etken mikroorganizmayı baskılayan medikal girişim"
            ),
            make_causal_chain(
                "Aseptik Kan Kültürü Alım Aşamaları",
                [
                    "1. Zamanlama: Hasta titreme hissettiğinde ve ateş yükselirken hazırlık yapılır.",
                    "2. Deri Antisepsisi: Ven bölgesi klorheksidin ile merkezden çevreye silinip kurutulur.",
                    "3. Çift Damar Girişi: Farklı venlerden ayrı enjektörlerle 10'ar ml kan çekilir.",
                    "4. Şişelere İnokülasyon: Önce aerop ardından anaerop kan kültürü şişesine aktarılır.",
                    "5. Otomatize İnkübasyon: Şişeler kontinü CO2 ölçümlü kan kültürü cihazına yüklenir."
                ]
            ),
            make_branching_logic(
                "Acil servise 39.5 derece ateş, titreme ve taşikardi ile getirilen 65 yaşındaki pnömoni şüpheli hastaya antibiyotik başlanacaktır. Nöbetçi hekimin kan kültürü alma konusundaki en doğru yaklaşımı hangisi olmalıdır?",
                [
                    {
                        "text": "Antibiyotik verilmeden önce derhal iki farklı periferik venden aseptik kurallarla birer set (aerop + anaerop) kan kültürü alıp hemen ardından ampirik antibiyotiği başlatmak.",
                        "isCorrect": True,
                        "explanation": "Doğru. Kan kültürleri antibiyotik öncesi alınmalıdır ki kanda canlı bakteri üreyebilsin; ancak sepsiste antibiyotik geciktirilmemeli, kültür alımı hemen tamamlanıp dakikalar içinde tedaviye geçilmelidir."
                    },
                    {
                        "text": "Geniş spektrumlu antibiyotiği derhal damardan verip, ateş düştükten 24 saat sonra kan kültürü almak.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Antibiyotik verildikten sonra kanda bakteri üreme şansı dramatik şekilde düşer ve etken saptanamaz."
                    },
                    {
                        "text": "Sadece tek bir parmak ucu delinerek birkaç damla kanı tek bir kültür şişesine damlatmak.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Yetişkinde her şişe için 8-10 ml venöz kan gerekir; parmak ucu kanı yetersizdir ve cilt florasıyla kontamine olur."
                    },
                    {
                        "text": "Hastada lökositoz yoksa kan kültürü almayı tamamen reddetmek.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Ateş ve sepsiste lökositoz şart değildir, lökopeni bile görülebilir; kan kültürü endikedir."
                    }
                ]
            )
        ]
    })

    # Slayt 95: Antimikrobiyal Tedavi Prensipleri ve Direnç Sorunu
    slides.append({
        "id": "k1-21-s95",
        "title": "Antimikrobiyal Tedavi Prensipleri ve Direnç Sorunu",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 95,
        "narrative": (
            "Antimikrobiyal tedavi, mikroorganizmanın selektif toksisite ilkesine göre yok edilmesini hedefler. "
            "Klinik enfeksiyon pratiğinde tedavi iki aşamada yürütülür: "
            "1. **Ampirik Tedavi:** Patojen ve antibiyogram henüz belli değilken, hastanın klinik tablosuna, enfeksiyon "
            "odağına ve yerel direnç oranlarına göre en olası patojenleri kapsayan geniş spektrumlu tedavi başlanmasıdır. "
            "2. **Etkene Yönelik (De-eskalasyon) Tedavi:** Kültür ve antibiyogram sonucu çıktığında (48-72 saat), "
            "etkili olan en dar spektrumlu, en az toksik ve en ucuz ilaca geçilmesidir. "
            "Bakterisidal ilaçlar mikroorganizmayı doğrudan öldürürken (ör. penisilinler, sefalosporinler, aminoglikozitler), "
            "bakteriyostatik ilaçlar üremesini durdurur ve yok edilmesini konak immünitesine bırakır (ör. makrolidler, tetrasiklinler). "
            "Gereksiz ve uygunsuz antibiyotik kullanımı küresel çapta ölümcül dirençli süper-bakterilerin "
            "(MRSA, VRE, Karbapenem-dirençli Enterobacterales - CRE) doğmasına yol açmıştır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Kültür ve antibiyogram sonucu geldikten sonra geniş spektrumlu tedaviden dar spektrumlu hedefe yönelik ilaca geçilmesine de-eskalasyon denir.",
                "de-eskalasyon",
                "Antibiyotik basamağını daraltıp hedef odaklı hale getirme stratejisi"
            ),
            make_before_after(
                "Ampirik Tedavi ile De-eskalasyon Tedavisi Kıyaslaması",
                "Ampirik Başlangıç Tedavisi",
                "Kültür sonucu beklenirken en olası etkenleri kapsayan geniş spektrumlu antibiyotik kombinasyonu uygulanır.",
                "Hedefe Yönelik De-eskalasyon",
                "Antibiyograma göre etkeni öldüren en dar spektrumlu, florayı en az bozan spesifik ilaca dönülür.",
                "Klinik aciliyette geniş kapsama ile kültür sonrası selektif daraltmanın uyumu"
            ),
            make_active_recall(
                "Nötropenik veya immünsüprese hastalarda neden bakteriyostatik yerine bakterisidal antibiyotikler tercih edilmelidir?",
                "Çünkü bakteriyostatik ajanlar mikrobu öldürmeyip sadece durdurur; mikroorganizmanın tam temizliği için sağlam lökosit ve immün sistem gerekir, bu da immünsüprese bireylerde yetersizdir.",
                "Konak fagositoz eksikliğinde doğrudan öldürücü ajan zorunluluğu"
            )
        ]
    })

    # Slayt 96: İmmünoprofilaksi: Aktif ve Pasif Bağışıklama
    slides.append({
        "id": "k1-21-s96",
        "title": "İmmünoprofilaksi: Aktif ve Pasif Bağışıklama",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 96,
        "narrative": (
            "Enfeksiyon hastalıklarıyla mücadelenin en maliyet-etkin ve koruyucu yolu **immünoprofilaksidir**. "
            "İmmünoprofilaksi iki temel mekanizmayla sağlanır: "
            "1. **Aktif Bağışıklama (Aşılar):** Patojenin kendisinin (canlı atenüe) veya parçalarının (inaktif, toksoid, "
            "rekombinant, mRNA) vücuda verilerek konağın kendi immün sisteminin uyarılmasıdır. "
            "Koruyuculuğun başlaması birkaç hafta sürer ancak bellek hücreleri (B ve T lenfositler) sayesinde koruma **yıllarca veya ömür boyu** kalıcıdır. "
            "Canlı atenüe aşılar (ör. KKK, suçiçeği, sarı humma, BCG) güçlü hücresel ve humoral yanıt oluşturur ancak immün yetmezliklilerde ve gebelerde kontrendikedir! "
            "2. **Pasif Bağışıklama (Antiserum / İmmünglobulinler):** Başka bir canlıda üretilmiş hazır antikorların (tetanoz antitoksini, "
            "kuduz immünglobulini - RIG, Hepatit B immünglobulini - HBIG) kişiye enjekte edilmesidir. "
            "Koruma **derhal (anında)** başlar, acil temas sonrası profilakside hayat kurtarır; ancak hazır antikorlar parçalandığında (2-4 hafta) "
            "koruma tamamen biter, immünolojik bellek oluşturmaz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Hazır antikorların verilmesiyle anında başlayan ancak kalıcı bellek bırakmayan bağışıklama tipine pasif bağışıklama denir.",
                "pasif bağışıklama",
                "Dışarıdan hazır immünglobulin aktarımıyla sağlanan geçici koruma"
            ),
            make_table(
                "Aktif ve Pasif Bağışıklamanın Temel Farkları",
                ["Kriter / Özellik", "Aktif Bağışıklama (Aşılar)", "Pasif Bağışıklama (İmmünglobulinler)"],
                [
                    ["Verilen Madde", "Antijen (zayıflatılmış/ölü etken, toksoid, mRNA)", "Dışarıdan hazır spesifik antikorlar (IgG)"],
                    [
                        "Korumanın Başlama Hızı",
                        {"text": "Yavaş (2-4 hafta sonra gelişir)", "isMasked": True, "hint": "Konağın antikor sentezlemesi için gereken latent süre"},
                        "Anında (enjeksiyon anında koruma başlar)"
                    ],
                    ["Koruma Süresi", "Uzun süreli (yıllar veya ömür boyu)", "Kısa süreli (2 - 4 hafta)"],
                    ["İmmünolojik Bellek", "Kuvvetli bellek B ve T hücresi oluşur", "Bellek hücresi asla oluşmaz"]
                ]
            ),
            make_micro_quiz(
                "Aşılar ve immünoprofilaksi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Canlı atenüe aşılar replike olabilen zayıflatılmış suşlar içerir ve gebelerde kontrendikedir",
                    "B": "Tetanoz toksoid aşısı aktif bağışıklık sağlarken, tetanoz antiserumu pasif koruma sağlar",
                    "C": "Pasif bağışıklama ile verilen antikorlar konakta ömür boyu kalıcı bellek lenfositi üretir",
                    "D": "Kuduz şüpheli yüksek riskli ısırıklarda hem kuduz aşısı hem de hazır immünglobulin birlikte uygulanır",
                    "E": "İnaktif ve rekombinant aşılar immün yetmezliği olan hastalarda kural olarak güvenle yapılabilir"
                },
                "C",
                "Doğru cevap C'dir: Pasif bağışıklama hazır antikor transferidir; antikorlar birkaç hafta içinde yarılanır ve vücuttan atılır, konakta hiçbir bellek lenfositi oluşturmaz. Diğer seçenekler immünoprofilaksinin temel kurallarıdır."
            )
        ]
    })

    # Slayt 97: Hastane Enfeksiyonları (Sağlık Hizmeti İlişkili Enfeksiyonlar - SHİE)
    slides.append({
        "id": "k1-21-s97",
        "title": "Hastane Enfeksiyonları (Sağlık Hizmeti İlişkili Enfeksiyonlar - SHİE)",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 97,
        "narrative": (
            "Modern tıbbın ve hastanelerin en büyük komplikasyonlarından biri **Sağlık Hizmeti İlişkili Enfeksiyonlardır (SHİE)**. "
            "**Klasik Tanım:** Hastanın hastaneye yatış anında kuluçka (inkübasyon) döneminde olmayan, "
            "**yatıştan en az 48 saat sonra** ortaya çıkan veya taburcu olduktan sonraki ilk 10 gün (cerrahi implantlarda 30-90 gün) "
            "içinde gelişen enfeksiyonlara hastane enfeksiyonu (nozokomiyal enfeksiyon) denir. "
            "SHİE etkenleri genellikle hastane florasındaki çoklu antibiyotik dirençli bakterilerdir (Acinetobacter, Pseudomonas, "
            "Klebsiella, MRSA). "
            "**En Sık Görülen Dört SHİE Türü:** "
            "1. **Ventilatör İlişkili Pnömoni (VİP):** Entübe yoğun bakım hastalarında aspirasyona bağlı gelişir. "
            "2. **Santral Kateter İlişkili Kan Dolaşımı Enfeksiyonu (Kİ-KDİ):** Damar içi kateter lümeninden mikrop sızması. "
            "3. **Kateter İlişkili Üriner Sistem Enfeksiyonu (Kİ-ÜSE):** İdrar sondası takılı hastalarda en sık görülen hastane enfeksiyonu. "
            "4. **Cerrahi Alan Enfeksiyonu (CAİ):** Ameliyat kesisinde gelişen enfeksiyonlar. "
            "SHİE yayılımını önlemenin **tek başına en ucuz, en kolay ve en etkili yolu el hijyenidir**!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Hastanın yatışında inkübasyon evresinde bulunmayan ve yatıştan en az 48 saat sonra ortaya çıkan tablolara hastane enfeksiyonu denir.",
                "48 saat sonra",
                "Nozokomiyal enfeksiyon kabulü için gereken asgari yatış süresi"
            ),
            make_table(
                "Majör Sağlık Hizmeti İlişkili Enfeksiyon (SHİE) Tipleri",
                ["SHİE Tipi", "Başlıca Risk Faktörü / Girişim", "En Etkili Önleme Paketi"],
                [
                    [
                        "Ventilatör İlişkili Pnömoni (VİP)",
                        "Endotrakeal entübasyon ve mekanik ventilasyon",
                        {"text": "Yatak başının 30-45 derece yükseltilmesi ve ağız bakımı", "isMasked": True, "hint": "Aspirasyonu önleyici mekanik pozisyon kuralı"}
                    ],
                    ["Kateter İlişkili Kan Dolaşımı (Kİ-KDİ)", "Santral venöz kateter takılması", "Maksimal steril bariyer önlemleri ve klorheksidin antisepsisi"],
                    ["Kateter İlişkili Üriner Enfeksiyon (Kİ-ÜSE)", "Kalıcı idrar sondası (Foley kateter)", "Sondanın endikasyon biter bitmez derhal çekilmesi"],
                    ["Cerrahi Alan Enfeksiyonu (CAİ)", "Cerrahi insizyon ve doku diseksiyonu", "İnsizyondan 30-60 dk önce tek doz profilaktik antibiyotik"]
                ]
            ),
            make_micro_quiz(
                "Hastane enfeksiyonları (SHİE) ve epidemiyolojisi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Hastaneye yatıştan en az 48 saat sonra beliren klinik tablolar SHİE kabul edilir",
                    "B": "Hastane enfeksiyonlarının önlenmesinde en etkili ve en ucuz yöntem personelin el hijyenidir",
                    "C": "SHİE etkeni bakteriler toplum kökenli suşlara göre antibiyotiklere çok daha dirençlidir",
                    "D": "Kalıcı idrar sondası takılı hastalarda gelişen bakteriüri her zaman derhal çift antibiyotikle tedavi edilmelidir",
                    "E": "Yatış anında inkübasyon evresinde olup hastanede patlak veren hastalıklar SHİE sayılmaz"
                },
                "D",
                "Doğru cevap D'dir: Sonda takılı hastalarda semptomsuz bakteri varlığı (asemptomatik bakteriüri) sık görülür ve antibiyotikle tedavi edilmez; gereksiz antibiyotik dirençli mutantların seçilmesine yol açar; ilk adım sondanın çekilmesidir. A, B, C ve E seçenekleri tamamen doğrudur."
            )
        ]
    })

    # Slayt 98: Biyogüvenlik Düzeyleri (BSL 1 - 4) ve Laboratuvar Emniyeti
    slides.append({
        "id": "k1-21-s98",
        "title": "Biyogüvenlik Düzeyleri (BSL 1 - 4) ve Laboratuvar Emniyeti",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 98,
        "narrative": (
            "Enfeksiyon etkenleriyle çalışan tanı ve araştırma laboratuvarları, hem çalışanları hem de toplumu "
            "bulaş riskinden korumak için mikroorganizmanın patojenitesine göre dört **Biyogüvenlik Düzeyine (BSL / BGD 1-4)** ayrılmıştır: "
            "- **BSL-1 (Düşük Risk):** Sağlıklı yetişkinlerde hastalık yapmayan mikroplar (ör. laboratuvar suşu E. coli K12, "
            "Bacillus subtilis). Standart açık tezgah çalışması yeterlidir. "
            "- **BSL-2 (Orta Risk):** İnsanlarda hastalık yapan ancak aerosol riski sınırlı, aşısı veya tedavisi bulunan standart patojenler "
            "(ör. Staphylococcus aureus, Salmonella, Hepatit B, HIV). Biyogüvenlik kabini (Laminar flow) ve eldiven kullanılır. "
            "- **BSL-3 (Yüksek Bireysel / Orta Toplumsal Risk):** İnhalasyonla (aerosol) bulaşabilen, ciddi ve potansiyel ölümcül sistemik "
            "hastalık yapan etkenler (ör. Mycobacterium tuberculosis, Bacillus anthracis, SARS-CoV-2, Brucella, Tularemi). "
            "Negatif basınçlı çift kapılı özel hava filtreli laboratuvar şarttır. "
            "- **BSL-4 (Maksimum Risk):** Aerosolle kolayca yayılan, fatalitesi çok yüksek, **tedavisi ve aşısı bulunmayan** ölümcül virüsler "
            "(ör. Ebola virüsü, Marburg virüsü, Lassa, Kırım-Kongo Kanamalı Ateşi virüsü). Pozitif basınçlı astronot giysisi tipi özel hava beslemeli tulumlarla çalışılır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Aerosolle bulaşan, tedavisi ve aşısı olmayan ölümcül virüslerle yalnızca BSL-4 düzeyindeki pozitif basınçlı tulumlu laboratuvarlarda çalışılabilir.",
                "BSL-4",
                "En üst düzey biyogüvenlik koruma kategorisi"
            ),
            make_table(
                "Biyogüvenlik Seviyeleri (BSL 1-4) Özellikleri",
                ["Düzey", "Bireysel / Toplumsal Risk", "Prototip Patojenler", "Gereken Koruyucu Altyapı"],
                [
                    ["BSL-1", "Yok / Minimal", "E. coli K12, B. subtilis", "Açık tezgah, standart laboratuvar önlüğü"],
                    ["BSL-2", "Orta / Düşük", "S. aureus, HBV, Salmonella", "Sınıf II biyogüvenlik kabini, eldiven"],
                    [
                        "BSL-3",
                        "Yüksek / Düşük-Orta",
                        "M. tuberculosis, B. anthracis, Tularemi",
                        {"text": "Negatif hava basıncı, HEPA filtre, çift kilitli kapı", "isMasked": True, "hint": "Aerosol partiküllerin çevre ortama sızmasını engelleyen gradyan düzeneği"}
                    ],
                    ["BSL-4", "Çok Yüksek / Çok Yüksek", "Ebola, Marburg, Lassa virüsleri", "Pozitif basınçlı tam vücut tulumu, hava kilidi"]
                ]
            ),
            make_active_recall(
                "Mycobacterium tuberculosis ve Brucella kültürleriyle çalışırken neden standart BSL-2 yerine mutlaka BSL-3 önlemleri alınmalıdır?",
                "Çünkü bu bakteriler laboratuvarda tüp açılması veya vorteksleme sırasında kolayca aerosol oluşturur ve solunum yoluyla laboratuvar çalışanlarına bulaşarak ölümcül enfeksiyon yapabilir.",
                "Aerosol inhalasyon riski ve yüksek laboratuvar bulaşıcılığı"
            )
        ]
    })

    # Slayt 99: Yeni ve Yeniden Ortaya Çıkan Enfeksiyonlar ve Tek Sağlık
    slides.append({
        "id": "k1-21-s99",
        "title": "Yeni ve Yeniden Ortaya Çıkan Enfeksiyonlar ve Tek Sağlık",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 99,
        "narrative": (
            "21. yüzyılda enfeksiyon hastalıkları asla geride kalmış bir tıp konusu değildir; küresel hareketlilik, "
            "iklim krizi, ormansızlaşma ve yabani hayatla artan temas yeni salgınları tetiklemektedir. "
            "Bu süreçte iki kritik epidemiyolojik kavram öne çıkar: "
            "1. **Yeni Ortaya Çıkan Enfeksiyonlar (Emerging Infections):** İnsan popülasyonunda daha önce hiç görülmemiş "
            "veya ilk kez tanımlanan hastalıklar (ör. HIV/AIDS, SARS, MERS, SARS-CoV-2, Kuş gribi H5N1). "
            "Bu etkenlerin **%75'ten fazlası hayvanlardan insanlara atlayan zoonotik patojenlerdir**! "
            "2. **Yeniden Ortaya Çıkan Enfeksiyonlar (Re-emerging Infections):** Daha önce kontrol altına alınmış veya "
            "azalmışken aşı karşıtlığı, savaşlar veya antibiyotik direnci nedeniyle tekrar patlama yapan hastalıklar (ör. Kızamık, Boğmaca, Tüberküloz). "
            "**Tek Sağlık (One Health) Yaklaşımı:** "
            "İnsan sağlığı, hayvan sağlığı ve çevre ekosisteminin birbirinden ayrılamaz bir bütün olduğunu kabul eden küresel stratejidir. "
            "Gelecekteki pandemileri önlemenin tek yolu, hayvan rezervuarlarını ve ekosistemleri insan hekimleri, veteriner hekimler "
            "ve çevre bilimcilerle ortaklaşa izlemektir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "İnsan, hayvan ve çevre sağlığının ortak izlenmesini öngören küresel multidisipliner yaklaşıma Tek Sağlık denir.",
                "Tek Sağlık",
                "İnsan ve ekosistem bütünlüğünü savunan tıp paradigması"
            ),
            make_before_after(
                "Yeni Ortaya Çıkan ile Yeniden Hortlayan Enfeksiyonlar",
                "Yeni Ortaya Çıkan (Emerging)",
                "İlk kez tanımlanan, genellikle yabani hayvan rezervuarından türe sıçrayan ve toplumda immünitesi bulunmayan etkenler (SARS-CoV-2).",
                "Yeniden Hortlayan (Re-emerging)",
                "Aşı veya antibiyotikle geriletilmişken aşı terki veya direnç yüzünden yeniden salgın yapan eski etkenler (Kızamık, Tüberküloz).",
                "Sıfırdan doğan virüsler ile unutulmuşken geri dönen klasik mikropların ayrımı"
            ),
            make_micro_quiz(
                "Yeni ortaya çıkan (emerging) enfeksiyonlar ve Tek Sağlık (One Health) konsepti ile ilgili hangisi doğrudur?",
                {
                    "A": "Yeni ortaya çıkan insan enfeksiyonlarının %75'inden fazlası zoonotik kökenlidir",
                    "B": "Aşı karşıtlığının artması sadece yeni enfeksiyonların ortaya çıkışını etkiler, eski hastalıklara tesir etmez",
                    "C": "Tek Sağlık yaklaşımı veteriner hekimliği insan tıbbından tamamen ayırmayı hedefler",
                    "D": "Antibiyotik direnci yalnız hastanelerde görülür, hayvancılık sektöründeki ilaç kullanımı direnç oluşturmaz",
                    "E": "Tüberküloz ve kızamık dünyada ilk kez 2020'de tanımlanmış emerging enfeksiyonlardır"
                },
                "A",
                "Doğru cevap A'dır: İnsanlarda yeni tanımlanan enfeksiyon etkenlerinin %75'i hayvanlardan (özellikle yarasalar, kemiriciler, kuşlar) tür atlamasıyla bulaşan zoonozlardır. B yanlıştır (kızamık gibi re-emerging hastalıkları hortlatır); C yanlıştır (ortak işbirliğini hedefler); D yanlıştır (veteriner antibiyotik kullanımı direncin ana kaynağıdır); E yanlıştır (ikisi de binlerce yıllık re-emerging hastalıklardır)."
            )
        ]
    })

    # Slayt 100: [TEKRAR SAYFASI - CHECKPOINT 10] Enfeksiyon Hastalıkları Büyük Özeti
    slides.append({
        "id": "k1-21-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Enfeksiyon Hastalıkları Büyük Özeti",
        "section": "Tanısal Mikrobiyoloji İlkeleri ve Büyük Özet",
        "slideNumber": 100,
        "narrative": (
            "Tebrikler! Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler dersinin 100 slaytlık "
            "büyük öğrenme yolculuğunu başarıyla tamamladınız. "
            "Bu son checkpoint sayfasında tanısal mikrobiyoloji, profilaksi, hastane enfeksiyonları ve Tek Sağlık "
            "prensiplerinin en hayati noktalarını kilitliyoruz: "
            "1. **Tanı Piramidi:** Direkt mikroskopi ön tanı verir, kültür altın standarttır, PCR moleküler hız ve kantitasyon sağlar. "
            "2. **Seroloji Mantığı:** Akut evrede IgM veya çift serumda 4 kat titre artışı; geçirilmiş evrede IgG pozitifliği. "
            "3. **Kan Kültürü:** Ateş yükselirken, antibiyotik öncesi, mükemmel cilt dezenfeksiyonu ile 2 farklı venden ikişer şişe. "
            "4. **İmmünoprofilaksi:** Aktif bağışıklık (aşılar) geç başlar ama kalıcı bellek bırakır; pasif bağışıklık anında başlar fakat geçicidir. "
            "5. **SHİE ve Biyogüvenlik:** Yatıştan 48 saat sonra gelişen nozokomiyal enfeksiyonların bir numaralı düşmanı el hijyenidir; "
            "Ebola/Marburg gibi tedavisi olmayan ölümcüller BSL-4 düzeyinde pozitif basınçlı tulumla çalışılır. "
            "6. **Gelecek:** Zoonozlar insan patojenlerinin beşiğidir; insan, hayvan ve çevre Tek Sağlık çatısında korunmalıdır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "k1-21-fc-28",
                "Hastanın hastaneye yatışından en az 48 saat sonra gelişen veya taburcu olduktan sonraki ilk 10 gün içinde ortaya çıkan enfeksiyonlara ne ad verilir?",
                "Sağlık hizmeti ilişkili enfeksiyon (Hastane enfeksiyonu / Nozokomiyal enfeksiyon)",
                "Yatış anında kuluçkada bulunmayan edinsel klinik tablo",
                "Tanı ve Korunma"
            ),
            make_flashcard(
                "k1-21-fc-29",
                "Akut bir enfeksiyonun serolojik tanısında son 2-3 hafta arayla alınan çift serum örneğinde spesifik antikor titresinde kaç kat artış tanı koydurucudur?",
                "En az 4 kat titre artışı",
                "Serokonversiyonu ve aktif immün yanıtı kanıtlayan standart serolojik misli yükseliş oranı",
                "Tanı ve Korunma"
            ),
            make_flashcard(
                "k1-21-fc-30",
                "İnsan, evcil/yabani hayvan ve çevre sağlığının birbirinden ayrılamaz bir bütün olduğunu savunan multidisipliner küresel tıp yaklaşımı nedir?",
                "Tek Sağlık (One Health) yaklaşımı",
                "Zoonozların kontrolünde tüm canlı ekosistemini ortak değerlendiren küresel paradigma",
                "Tanı ve Korunma"
            )
        ]
    })

    return slides
