# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 5: Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar (Slayt 41 - 50)
Checkpoint 5: Slayt 49
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # Slayt 41: 3. Gebe İzlemi (28-32. Hafta): Erken Doğum Eylemi Bilgilendirmesi
    slides.append({
        "id": "k1-23-s41",
        "title": "3. Gebe İzlemi (28-32. Hafta): Erken Doğum Eylemi Bilgilendirmesi",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 41,
        "narrative": (
            "3. Gebe İzlemi **28-32. haftalar arasında** (üçüncü trimesterin hemen başında) gerçekleştirilir ve "
            "hekimin yaklaşık **20 dakikalık** odaklanmış bir görüşme yapmasını gerektirir: "
            "1. **Rutin Değerlendirmeler:** Kan basıncı (preeklampsi riski bu haftalarda tırmanır), kilo artışı, "
            "anemi muayenesi, ödem değerlendirmesi, FKS dinlenmesi ve mezura ile fundus yüksekliği ölçümü tekrarlanır. "
            "2. **Erken Doğum Eylemi (Preterm Eylem) Bilgilendirmesi:** 37. haftadan önce başlayan doğum eylemi "
            "bebek ölümlerinin en büyük nedenidir. Gebeye erken doğumun uyarıcı işaretleri titizlikle öğretilir: "
            "- Saatte 4 veya daha sık gelen düzenli uterus kasılmaları ve karında sertleşme, "
            "- Adet sancısı benzeri kramp şeklinde kasık ağrıları ve bel ağrısı, "
            "- Vajinal akıntının aniden artması, sulu hale gelmesi veya pembe/kahverengi müköz kanlı akıntı (nişan gelmesi). "
            "Bu belirtilerde gebenin vakit kaybetmeden acil obstetrik servise başvurması hayat kurtarır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Üçüncü gebe izlemi 28-32. haftalarda yapılarak erken doğum eylemi belirtileri ve acil başvuru kuralları anlatılır.",
                "28-32. haftalarda",
                "Üçüncü trimester başındaki kritik gebe kontrol aralığı"
            ),
            make_table(
                "Erken Doğum Eylemi Belirtileri ve Acil Uyarı İşaretleri",
                ["Klinik Belirti", "Fizyopatolojik Mekanizma", "Gebenin Yapması Gereken Davranış"],
                [
                    ["Düzenli Uterus Kasılması", "Myometriumda oksitosin reseptör artışı ve ritmik aktivite", "Hemen sol yan yatarak dinlenmek ve acile başvurmak"],
                    [
                        "Kanlı Müköz Akıntı (Nişan)",
                        {"text": "Servikal silinme ve kanalın açılması", "isMasked": True, "hint": "Rahim ağzı tıkacının düşmesine yol açan servikal genişleme"},
                        "Doğum eyleminin başladığını bilerek hastaneye gitmek"
                    ],
                    ["Sulu Vajinal Akıntı", "Amniyon membran rüptürü (Erken membran rüptürü)", "Enfeksiyon ve kordon sarkması riskiyle acil yatış"]
                ]
            ),
            make_active_recall(
                "3. Gebe İzleminde (28-32. hafta) hekimin gebeye erken doğum eylemi şüphesi durumunda evde istirahat ederken tercih etmesini önereceği en ideal vücut pozisyonu nedir?",
                "Uterusun vena kava inferiora baskısını kaldırıp uteroplasental kan akımını artıran Sol Yan Yatış (Sol Lateral) pozisyonudur.",
                "Kavalyer basıyı önleyen lateral dekübit pozisyonu"
            )
        ]
    })

    # Slayt 42: Doğumun Planlanması: Yer, Personel ve Postpartum Danışmanlık
    slides.append({
        "id": "k1-23-s42",
        "title": "Doğumun Planlanması: Yer, Personel ve Postpartum Danışmanlık",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 42,
        "narrative": (
            "3. Gebe İzlemi, doğum anındaki kaosu ve gecikmeleri (üç gecikme modelinin 1. ve 2. basamağını) "
            "önlemek için **'Doğum Planının Mühürlendiği'** vizittir: "
            "1. **Doğum Yeri ve Ekibinin Kararlaştırılması:** Gebelikte saptanan risk durumuna göre doğumun nerede yapılacağı netleştirilir. "
            "Düşük riskli gebeler ilçe devlet hastanesine yönlendirilirken; çoğul gebelik, preeklampsi, diyabet veya plasenta anomalisi "
            "olan gebeler yenidoğan yoğun bakım ve kan merkezi olan 2. veya 3. basamak eğitim hastanelerine planlanır. "
            "Ulaşım planı, ambulans numarası (112) ve acil çanta hazırlanır. "
            "2. **Emzirme Eğitimi:** İlk yarım saatte emzirme ve kolostrumun önemi anlatılır. "
            "3. **Postpartum Aile Planlaması:** Doğumdan sonra kullanılacak korunma yöntemi (RİA, kondom, tüp ligasyonu) "
            "henüz gebelik bitmeden çiftle birlikte kararlaştırılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Doğumun nerede ve kim tarafından yaptırılacağı ile doğum sonrası aile planlaması kararı üçüncü izlemde netleştirilir.",
                "üçüncü izlemde",
                "28-32. haftalarda yapılan doğum planlama viziti"
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı protokollerine göre doğumun nerede, nasıl ve kim tarafından yaptırılacağına karar verilmesi ve postpartum aile planlaması danışmanlığı öncelikli olarak hangi izlemde verilmelidir?",
                {
                    "A": "1. İzlem (0-14. hafta)",
                    "B": "2. İzlem (18-24. hafta)",
                    "C": "3. İzlem (28-32. hafta)",
                    "D": "Doğum masasında eylem anında",
                    "E": "Doğumdan 1 yıl sonraki çocuk izleminde"
                },
                "C",
                {
                    "A": "Yanlıştır; İlk izlemde tanı ve bazal risk formu esastır.",
                    "B": "Yanlıştır; İkinci izlemde taramalar ön plandadır.",
                    "C": "Doğrudur; Doğum yeri planlaması ve postpartum korunma kararı 3. izlemin (28-32. hafta) ana görevidir.",
                    "D": "Hatalı ve Geçtir; Doğum anında planlama yapılamaz, acil kriz doğar.",
                    "E": "Yanlıştır; Çok geçtir."
                }
            ),
            make_active_recall(
                "Doğum öncesi bakımda lohusalık dönemi aile planlaması danışmanlığının doğumdan sonra değil de henüz gebelik sırasında verilmesinin temel gerekçesi nedir?",
                "Doğum sonrasındaki lohusalık yorgunluğu ve bebek bakımı telaşında korunmanın ihmal edilip erken dönemde yeni bir plansız gebeliğin başlamasını engellemektir.",
                "Erken istenmeyen gebeliklerin önlenmesi zamanlaması"
            )
        ]
    })

    # Slayt 43: 4. Gebe İzlemi (36-38. Hafta): Doğum Eylemi ve Yalancı Sancılar
    slides.append({
        "id": "k1-23-s43",
        "title": "4. Gebe İzlemi (36-38. Hafta): Doğum Eylemi ve Yalancı Sancılar",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 43,
        "narrative": (
            "4. Gebe İzlemi **36-38. haftalar arasında**, doğuma sadece günler veya haftalar kala yapılır. "
            "Bu vizitin odağında doğum eyleminin başlaması ve hastaneye acil kabul koşulları yer alır: "
            "1. **Gerçek Doğum Ağrıları ile Yalancı Ağrılar (Braxton Hicks) Ayrımı:** "
            "- *Braxton Hicks:* Düzensiz aralıklarla gelir, sıklığı ve şiddeti artmaz, dinlenmekle ve pozisyon değiştirmekle geçer, "
            "servikal açılma yapmaz. "
            "- *Gerçek Doğum Sancıları:* Düzenli aralıklarla gelir (ör. 5 dakikada bir), şiddeti ve süresi giderek artar, "
            "yürümekle veya dinlenmekle asla geçmez, rahim ağzında silinme ve dilatasyona (açılma) yol açar. "
            "2. **Su Gelmesi (Membran Rüptürü):** Sancı olsun veya olmasın su geldiğinde gebenin kordon sarkması ve enfeksiyon "
            "riski nedeniyle ayakta durmadan, acilen yatar pozisyonda hastaneye gitmesi gerektiği vurgulanır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gerçek doğum sancıları düzenli aralıklarla gelir, şiddeti giderek artar ve servikal dilatasyona yol açar.",
                "servikal dilatasyona",
                "Rahim ağzının santimetre cinsinden açılma süreci"
            ),
            make_before_after(
                "Braxton Hicks (Yalancı Sancı) vs Gerçek Doğum Eylemi Ağrıları",
                "Braxton Hicks (Yalancı Kasılmalar)",
                "Ağrılar düzensizdir; yürümek veya sıcak duş almakla hafifler ve geçer; rahim ağzında açılma yapmaz.",
                "Gerçek Doğum Kasılmaları",
                "Ağrılar düzenli ritmik aralıklarla gelir; şiddeti katlanarak artar, dinlenmekle geçmez ve servikal açılmayı başlatır.",
                "Doğum sancılarının klinik ayırıcı tanısı"
            ),
            make_active_recall(
                "Terme gelmiş bir gebede hiçbir kasılma veya ağrı olmasa bile amniyon suyunun aniden gelmesi durumunda hekime acil başvurmayı gerektiren en korkulan akut obstetrik komplikasyon nedir?",
                "Göbek kordonunun vajinaya sarkması (kordon prolapsusu) ve fetal asfiksidir.",
                "Kordonun önden gelip sıkışması tehlikesi"
            )
        ]
    })

    # Slayt 44: Leopold Manevraları: Fetusun Durumu, Prezentasyonu ve Pozisyonu
    slides.append({
        "id": "k1-23-s44",
        "title": "Leopold Manevraları: Fetusun Durumu, Prezentasyonu ve Pozisyonu",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 44,
        "narrative": (
            "36. haftadan sonra yapılan 4. izlemin en karakteristik fizik muayene sanatı **Dört Leopold Manevrası'dır**. "
            "Hekim gebenin sağına geçerek karından palpasyonla şu soruları sırasıyla yanıtlar: "
            "1. **1. Leopold Manevrası (Fundus Palpasyonu):** Hekim iki elini fundusa koyar; 'Fundusta ne var?'. "
            "Sert, yuvarlak ve balotman veren kısım baş; yumuşak, düzensiz ve geniş kısım makattır. "
            "2. **2. Leopold Manevrası (Lateral Palpasyon):** Eller yanlara konur; 'Sırt hangi tarafta?'. "
            "Düz, pürüzsüz ve dirençli yüzey fetal sırttır (FKS sırtın üzerinden en iyi dinlenir); girintili çıkıntılı taraf ekstremitelerdir. "
            "3. **3. Leopold Manevrası (Pawlik Tutuşu):** Tek elin baş ve diğer dört parmağıyla simfizis pubis üzeri kavranır; "
            "'Pelvis girişinde hangi kısım var ve hareketli mi?'. "
            "4. **4. Leopold Manevrası (Angajman Değerlendirmesi):** Hekim yüzünü annenin ayaklarına döner ve iki elini pelvis girişine doğru iter; "
            "'Önde gelen kısım kemik pelvise ne kadar girmiş (angaje olmuş) mi?'."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Leopold manevralarında hekimin yüzünü annenin ayaklarına dönerek önde gelen kısmın pelvise angajmanını değerlendirdiği basamak dördüncü Leopold manevrasıdır.",
                "dördüncü Leopold manevrasıdır",
                "Kemik pelvise iniş derecesini saptayan son manevra"
            ),
            make_table(
                "Dört Leopold Manevrasının Klinik Amaç ve Uygulama Şeması",
                ["Manevra Sırası", "Hekimin Elleri / Yönü", "Cevaplanan Temel Klinik Soru", "Saptanan Fetal Özellik"],
                [
                    ["1. Leopold", "İki el fundus tepesinde", "Fundusta hangi fetal kutup var?", "Fetusun durumu (Situs) ve kutbu"],
                    [
                        "2. Leopold",
                        "İki el uterusun yan duvarlarında",
                        {"text": "Fetal sırt hangi tarafta yer alıyor?", "isMasked": True, "hint": "FKS'nin en net dinleneceği pürüzsüz dirençli yüzey"},
                        "Fetusun pozisyonu ve FKS odağı"
                    ],
                    ["3. Leopold (Pawlik)", "Tek el simfizis pubis üzerinde", "Önde gelen kısım nedir ve oynak mı?", "Prezentasyon (Baş mı, Makat mı)"],
                    ["4. Leopold", "Yüz annenin ayaklarına dönük", "Baş kemik pelvise angaje olmuş mu?", "Doğum kanalına giriş derecesi"]
                ]
            ),
            make_micro_quiz(
                "Gebe muayenesinde hekimin iki elini uterusun lateral duvarlarına koyarak dirençli düz bir yüzey ile küçük nodüler çıkıntıları ayırt ettiği 2. Leopold Manevrası'nın temel amacı nedir?",
                {
                    "A": "Fundusta başın mı makatın mı olduğunu anlamak",
                    "B": "Fetal sırtın ve ekstremitelerin hangi tarafta olduğunu belirlemek",
                    "C": "Servikal dilatasyonun kaç santimetre olduğunu ölçmek",
                    "D": "Plasentanın arka duvarda mı ön duvarda mı olduğunu ultrasonla görmek",
                    "E": "Amniyon sıvısının miktarını mililitre olarak hesaplamak"
                },
                "B",
                {
                    "A": "1. Leopold manevrasının amacıdır.",
                    "B": "Doğrudur; 2. Leopold manevrası fetal sırtın ve küçük kısımların lokalizasyonunu belirler.",
                    "C": "Vajinal tuşe ile belirlenir.",
                    "D": "Ultrasonografik incelemedir.",
                    "E": "Ultrasonografik ölçümdür."
                }
            )
        ]
    })

    # Slayt 45: Obstetrik Pelvik Değerlendirme ve Vajinal Muayene
    slides.append({
        "id": "k1-23-s45",
        "title": "Obstetrik Pelvik Değerlendirme ve Vajinal Muayene",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 45,
        "narrative": (
            "4. Gebe İzleminde ve doğum eylemi başladığında yapılan **Obstetrik Vajinal Muayene (Pelvik Tuşe)** "
            "normal doğumun güvenle gerçekleşip gerçekleşemeyeceğini belirleyen son anatomik kontroldür: "
            "1. **Kemik Pelvis Çatısı (Pelvimetri):** Promontoriuma ulaşılabiliyor mu (Konjugata diagonalis ölçümü), "
            "iskial spinalar sivri mi, subpubik açı geniş mi (>90 derece normal)? Darlık varsa sefalopelvik uygunsuzluk (SPU) tanısıyla sezaryen planlanır. "
            "2. **Servikal Olgunlaşma (Bishop Skoru):** Rahim ağzının pozisyonu (arka/orta/ön), kıvamı (sert/orta/yumuşak), "
            "silinmesi (efasman / incelme yüzdesi) ve dilatasyonu (açıklık santimetresi) değerlendirilir. "
            "3. **Prezente Kısmın Seviyesi:** Fetal başın iskial spinalar hizasına göre konumu (-3'ten +3'e kadar) belirlenir; "
            "baş spinalar hizasındayken '0 istasyonu' (sıfır seviyesi) denir ve başın angaje olduğunu gösterir. "
            "**Kritik Kural:** Vajinal kanaması olan gebeye ultrasonla plasenta previa dışlanmadan ASLA körlemesine vajinal muayene YAPILMAZ!"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Fetal başın iskial spinalar seviyesine ulaştığı anatomik duruma sıfır istasyonu veya angajman adı verilir.",
                "sıfır istasyonu",
                "Kemik pelvisin dar darlık seviyesine başın tam oturması"
            ),
            make_table(
                "Vajinal Pelvik Muayenede Değerlendirilen Temel Parametreler",
                ["Muayene Alanı", "Normal Vajinal Doğuma Uygun Bulgu", "Sezaryen Düşündüren Patolojik Bulgu"],
                [
                    ["Subpubik Açı", "Geniş (>90 derece)", "Dar ve sivri (<90 derece)"],
                    [
                        "İskial Spinalar",
                        "Küt ve silik",
                        {"text": "Belirgin çıkıntılı ve sivri", "isMasked": True, "hint": "Doğum kanalının orta darlığını daraltan kemik dikenler"}
                    ],
                    ["Servikal Efasman", "İncelmiş ve yumuşak (%80-100)", "Kalın ve sert (tübüler)"],
                    ["Başın Seviyesi", "0 istasyonu veya pozitif seviyeler", "Yüksekte yüzen baş (-3 istasyonu)"]
                ]
            ),
            make_active_recall(
                "Aktif vajinal kanama ile acil servise başvuran üçüncü trimesterdeki bir gebede parmakla vajinal muayene yapılmasının kesinlikle yasak olmasının nedeni nedir?",
                "Plasenta previa durumunda parmağın plasentayı yırtarak saniyeler içinde ölümcül masif kanamaya yol açma riskidir.",
                "Plasenta dekolmanı ve previa kanama tehlikesi"
            )
        ]
    })

    # Slayt 46: Fetal Anomali Tarama Testleri: İkili Test ve Üçlü Test (16-18. Hafta)
    slides.append({
        "id": "k1-23-s46",
        "title": "Fetal Anomali Tarama Testleri: İkili Test ve Üçlü Test (16-18. Hafta)",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 46,
        "narrative": (
            "Gebelikte kromozomal anomalilerin ve nöral tüp defektlerinin taranması antenatal bakımın ayrılmaz parçasıdır: "
            "1. **Birinci Trimester Taraması (İkili Test - 11-14. Hafta):** Ultrason ile **Ense Kalınlığı (NT - Nuchal Translucency)** ölçümü "
            "ve maternal kanda serbest beta-hCG ile PAPP-A (Pregnancy-Associated Plasma Protein A) düzeylerine bakılır. "
            "Down sendromunda NT kalınlaşır, beta-hCG artar, PAPP-A düşer. "
            "2. **İkinci Trimester Taraması (Üçlü Test - 15-22. Hafta, İdeal 16-18. Hafta):** "
            "Kanda **Maternal Serum Alfa-Fetoprotein (MSAFP)**, serbest beta-hCG ve ankonjuge estriol (uE3) bakılır: "
            "- **Down Sendromu (Trizomi 21):** AFP düşük, uE3 düşük, beta-hCG YÜKSEKTİR. "
            "- **Nöral Tüp Defektleri (Spina Bifida, Anensefali):** Fetal omurilik açıkta olduğundan amniyon sıvısına ve anne kanına "
            "muazzam miktarda AFP sızar; **MSAFP BELİRGİN YÜKSEKTİR**. "
            "- **Trizomi 18 (Edwards Sendromu):** Her üç belirteç de (AFP, uE3, hCG) birden düşüktür."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Üçlü tarama testi en ideal olarak 16-18. haftalar arasında yapılarak Down sendromu ve nöral tüp defekti riskini saptar.",
                "16-18. haftalar",
                "İkinci trimester üçlü biyokimyasal tarama için en optimum altın pencere"
            ),
            make_table(
                "Üçlü Test Biyokimyasal Belirteçleri ve Fetal Patolojiler",
                ["Fetal Genetik / Yapısal Durum", "MSAFP Düzeyi", "Beta-hCG Düzeyi", "Ankonjuge Estriol (uE3)"],
                [
                    [
                        "Down Sendromu (Trizomi 21)",
                        "Düşük",
                        {"text": "Yüksek", "isMasked": True, "hint": "Trizomi 21'de yükselen tek biyokimyasal hormon"},
                        "Düşük"
                    ],
                    ["Nöral Tüp Defekti (Spina Bifida)", "Belirgin Yüksek", "Normal", "Normal"],
                    ["Trizomi 18 (Edwards)", "Düşük", "Düşük", "Düşük"]
                ]
            ),
            make_micro_quiz(
                "Gebelikte 16-18. haftalarda yapılan Üçlü Testte maternal kanda Alfa-Fetoprotein (MSAFP) düzeyinin beklenenden çok yüksek bulunması öncelikle hangi fetal patolojiyi düşündürür?",
                {
                    "A": "Down sendromu (Trizomi 21)",
                    "B": "Nöral tüp defekti (Spina bifida veya Anensefali)",
                    "C": "Turner sendromu (45,X0)",
                    "D": "Fenilketonüri hastalığı",
                    "E": "Konjenital kalça displazisi"
                },
                "B",
                {
                    "A": "Yanlıştır; Down sendromunda AFP düşüktür.",
                    "B": "Doğrudur; Açık nöral tüp defektlerinde fetal BOS anne kanına sızarak AFP'yi çok yükseltir.",
                    "C": "Yanlıştır; Kistik higroma yapar ancak izole yüksek AFP triadı değildir.",
                    "D": "Yanlıştır; Doğum sonrası topuk kanı ile taranır.",
                    "E": "Yanlıştır; İskelet anomalisi olup biyokimyasal AFP ile taranmaz."
                }
            )
        ]
    })

    # Slayt 47: Gebelikte Tetanoz Toksoidi (Td) Aşılama Takvimi (Neonatal Tetanoz)
    slides.append({
        "id": "k1-23-s47",
        "title": "Gebelikte Tetanoz Toksoidi (Td) Aşılama Takvimi (Neonatal Tetanoz)",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 47,
        "narrative": (
            "Gelişmekte olan ülkelerde steril olmayan şartlarda göbek kordonunun kesilmesi (paslı makas, toprak, kül sürme) "
            "yenidoğanda ölüm oranı %90'ı aşan **Neonatal Tetanoza (Maternal ve Neonatal Tetanoz - MNT)** yol açar. "
            "Gebelikte yapılan Tetanoz Toksoidi (Td) aşısı, annede IgG antikorları üreterek plasentadan bebeğe geçer "
            "ve doğacak bebeği neonatal tetanozdan %100 korur. "
            "Sağlık Bakanlığı'nın hiç aşılanmamış gebeler için uyguladığı **5 Dozluk Tetanoz Aşı Takvimi** şöyledir: "
            "- **Td 1:** Gebeliğin 4. ayında (veya ilk karşılaşmada), "
            "- **Td 2:** Td 1'den en az 4 hafta sonra (doğumdan en az 2 hafta önce bitmeli; bebeği korur), "
            "- **Td 3:** Td 2'den en az 6 ay sonra (5 yıl korur), "
            "- **Td 4:** Td 3'ten en az 1 yıl sonra (10 yıl korur), "
            "- **Td 5:** Td 4'ten en az 1 yıl sonra (tüm doğurganlık çağı boyunca ömür boyu korur)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Hiç aşılanmamış bir gebede doğacak bebeğin neonatal tetanozdan korunması için en az iki doz tetanoz aşısı yapılmalıdır.",
                "en az iki doz",
                "Pasif transplasental koruyucu antikor üreten minimum aşı dozu sayısı"
            ),
            make_table(
                "Sağlık Bakanlığı Doğurganlık Çağı Kadın ve Gebe Tetanoz Aşı Takvimi",
                ["Aşı Dozu", "Uygulama Zamanı", "Sağlanan Koruma Süresi", "Klinik Hedef"],
                [
                    ["Td 1", "Gebeliğin 4. ayında (İlk karşılaşmada)", "Koruma yok", "Bağışıklık sistemini hazırlama"],
                    [
                        "Td 2",
                        {"text": "Td 1'den en az 4 hafta sonra", "isMasked": True, "hint": "Doğumdan en az 2 hafta önce tamamlanması gereken ikinci doz"},
                        "1 - 3 Yıl Koruma",
                        "Doğacak bebeği neonatal tetanozdan koruma"
                    ],
                    ["Td 3", "Td 2'den en az 6 ay sonra", "5 Yıl Koruma", "Sonraki gebeliği koruma"],
                    ["Td 4", "Td 3'ten en az 1 yıl sonra", "10 Yıl Koruma", "Uzun süreli maternal bağışıklık"],
                    ["Td 5", "Td 4'ten en az 1 yıl sonra", "Tüm doğurganlık çağı", "Ömür boyu tam koruma"]
                ]
            ),
            make_micro_quiz(
                "Hiç tetanoz aşısı olmamış bir primipar gebeye başvurusunda yapılan ilk doz tetanoz aşısından (Td 1) sonra, doğacak bebeğin neonatal tetanozdan korunabilmesi için ikinci doz (Td 2) en erken ne zaman yapılmalıdır?",
                {
                    "A": "İlk dozdan 24 saat sonra",
                    "B": "İlk dozdan en az 4 hafta sonra",
                    "C": "İlk dozdan 1 yıl sonra",
                    "D": "Yalnızca doğum masasında",
                    "E": "Bebek 6 aylık olduktan sonra"
                },
                "B",
                {
                    "A": "Yanlıştır; İmmün yanıt için süre çok kısadır.",
                    "B": "Doğrudur; Td 2 en az 4 hafta sonra ve doğumdan en az 2 hafta önce yapılmalıdır.",
                    "C": "Yanlıştır; Td 4 ve Td 5 için geçerli aralıktır.",
                    "D": "Yanlıştır; Doğum anında antikor plasentayı geçemez.",
                    "E": "Yanlıştır; Neonatal tetanoz ilk haftalarda öldürür."
                }
            )
        ]
    })

    # Slayt 48: Profilaktik Demir ve Folik Asit Desteği Protokolleri
    slides.append({
        "id": "k1-23-s48",
        "title": "Profilaktik Demir ve Folik Asit Desteği Protokolleri",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 48,
        "narrative": (
            "Sağlık Bakanlığı tüm gebelere ücretsiz olarak iki temel mikro besin desteği sağlar: "
            "1. **Folik Asit Desteği (Nöral Tüp Defekti Profilaksisi):** "
            "Nöral tüp embriyogenezin 28. gününde (kadın henüz gebe olduğunu dahi fark etmeden) kapanır. "
            "Bu nedenle folik asit ideal olarak **gebelikten en az 1 ay önce (prekonsepsiyonel)** başlanmalı "
            "ve gebeliğin **12. haftasının (ilk trimesterin) sonuna kadar** aralıksız sürdürülmelidir. "
            "Düşük riskli kadınlarda günlük doz **400 mcg (0.4 mg)**, önceki gebeliğinde NTD öyküsü olan yüksek riskli kadınlarda **4 mg'dır (10 kat)**. "
            "2. **Demir Desteği (Maternal Anemi Profilaksisi):** "
            "Gebelikte artan plazma ve eritrosit kitlesini karşılamak için **16. gebelik haftasından itibaren** "
            "tüm gebelere kan sayımı normal olsa dahi günlük **40-60 mg elementer demir** profilaksisi başlanır; "
            "bu destek doğum sonrasında da en az 3 ay boyunca sürdürülür."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Nöral tüp defektlerini önlemek için folik asit desteği gebelik öncesinde başlanarak ilk 12 hafta boyunca sürdürülür.",
                "ilk 12 hafta boyunca",
                "Embriyogenezde nöral tüp kapanma sürecini kapsayan ilk trimester süresi"
            ),
            make_table(
                "Gebelikte Rutin Folik Asit ve Demir Desteği Protokolü",
                ["Mikro Besin", "Başlama Zamanı", "Önerilen Günlük Profilaktik Doz", "Sürdürülme Süresi"],
                [
                    ["Folik Asit (Düşük Risk)", "Konsepsiyondan 1 ay önce", "400 mcg/gün (0.4 mg)", "12. gebelik haftasının sonuna kadar"],
                    ["Folik Asit (NTD Öyküsü)", "Konsepsiyondan 1-3 ay önce", "4000 mcg/gün (4.0 mg - 10 kat)", "12. gebelik haftasının sonuna kadar"],
                    [
                        "Demir Profilaksisi",
                        {"text": "16. gebelik haftasından itibaren", "isMasked": True, "hint": "İkinci trimesterde plazma ekspansiyonu hızlanırken başlanan hafta"},
                        "40 - 60 mg/gün elementer demir",
                        "Doğum sonrası lohusalıkta en az 3 ay sürdürülür"
                    ]
                ]
            ),
            make_active_recall(
                "Türkiye'de Sağlık Bakanlığı protokolüne göre rutin profilaktik demir desteğine gebenin kan tahlilleri normal olsa dahi kaçıncı gebelik haftasında başlanır?",
                "16. gebelik haftasından itibaren başlanır.",
                "İkinci trimester demir desteği başlangıç haftası"
            )
        ]
    })

    # Slayt 49: [TEKRAR SAYFASI - CHECKPOINT 5] 3. ve 4. Gebe İzlem, Leopold ve Taramalar
    slides.append({
        "id": "k1-23-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] 3. ve 4. Gebe İzlem, Leopold ve Taramalar",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 49,
        "narrative": (
            "Bu beşinci checkpoint sayfasında, 3. ve 4. izlem dinamiklerini, Leopold manevralarını ve taramaları özetliyoruz: "
            "1. **3. İzlem (28-32. Hafta):** Erken doğum eylemi belirtileri öğretilir, doğum yeri planlanır ve lohusalık aile planlaması kararlaştırılır. "
            "2. **4. İzlem (36-38. Hafta):** Gerçek vs yalancı (Braxton Hicks) doğum ağrıları ayırt edilir; su gelmesi acil başvuru kuralıdır. "
            "3. **Leopold Manevraları:** 1. Leopold fundus kutbu; 2. Leopold sırt ve FKS odağı; 3. Leopold (Pawlik) prezente kısım; 4. Leopold pelvise angajman. "
            "4. **Üçlü Test (16-18. Hafta):** Down sendromunda hCG yüksek, AFP ve uE3 düşük; Nöral Tüp Defektinde AFP çok yüksektir. "
            "5. **Tetanoz:** Td 1 4. ayda, Td 2 en az 4 hafta sonra; 2 doz bebeği neonatal tetanozdan korur. "
            "6. **Profilaksiler:** Folik asit ilk 12 hafta (400 mcg); Demir 16. haftadan lohusalık 3. ayına kadar (40-60 mg)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s49-1",
                "Leopold manevralarında hekimin iki elini karın yan duvarlarına koyarak fetal sırtın yerini belirlediği manevra hangisidir?",
                "İkinci Leopold manevrasıdır.",
                "FKS dinleme odağını gösteren lateral palpasyon basamağı",
                "Fizik Muayene Yöntemleri"
            ),
            make_flashcard(
                "k1-23-fc-s49-2",
                "Gebelikte 16-18. haftalarda yapılan Üçlü Testte maternal kanda Alfa-Fetoprotein (MSAFP) düzeyinin belirgin yüksek çıkması hangi patolojiyi düşündürür?",
                "Spina bifida veya anensefali gibi nöral tüp defektlerini düşündürür.",
                "Omurilik kanalının açık kalmasına bağlı protein sızıntısı",
                "Fetal Tarama Testleri"
            ),
            make_flashcard(
                "k1-23-fc-s49-3",
                "Sağlık Bakanlığı kılavuzuna göre gebelikte rutin profilaktik demir desteğine kaçıncı gebelik haftasından itibaren başlanmalıdır?",
                "On altıncı gebelik haftasından itibaren başlanmalıdır.",
                "Gestasyonel dördüncü ayda devreye giren mineral takviyesi",
                "Maternal Profilaksi"
            )
        ],
        "interactiveElements": [
            make_table(
                "3. ve 4. Gebe İzlemi Temel Görev Matrisi",
                ["Klinik Başlık", "3. İzlem (28-32. Hafta)", "4. İzlem (36-38. Hafta)"],
                [
                    ["Ana Odak", "Erken doğum eylemi tespiti", "Doğum eylemi ve prezentasyon hazırlığı"],
                    ["Doğum Yeri", "Doğum yeri ve hastane kararlaştırılır", "Hastaneye acil başvuru yolları teyit edilir"],
                    [
                        "Fetal Pozisyon Muayenesi",
                        "Fundus yüksekliği takibi",
                        {"text": "Dört Leopold manevrası ile tam palpasyon", "isMasked": True, "hint": "Prezantasyon, situs ve angajmanı belirleyen klasik manevra grubu"}
                    ],
                    ["Aile Planlaması", "Postpartum korunma yöntemi seçilir", "Lohusalıkta uygulanacak yöntem teyit edilir"]
                ]
            )
        ]
    })

    # Slayt 50: Bölüm Özeti: İzlem Basamaklarından Gebelikte Tehlike İşaretlerine Geçiş
    slides.append({
        "id": "k1-23-s50",
        "title": "Bölüm Özeti: İzlem Basamaklarından Gebelikte Tehlike İşaretlerine Geçiş",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 3. ve 4. İzlem ile Fetal Taramalar",
        "slideNumber": 50,
        "narrative": (
            "DÖB'ün 4 kademeli takvimini başarıyla tamamlayan bir gebenin takibinde hekim; erken doğum risklerini, "
            "doğum planını, Leopold manevralarını, tarama testlerini ve tetanoz/demir aşı takvimini eksiksiz yönetmiştir. "
            "Ancak koruyucu hekimliğin en kritik görevi, gebenin ve ailesinin acil bir tehlike anında 'beklemeden derhal hastaneye koşmasını' sağlamaktır. "
            "Gebelikte ortaya çıkan bazı semptomlar sıradan fizyolojik yakınmalar iken; bazıları anne veya fetüsün dakikalar içinde kaybedilebileceğini gösteren **Tehlike İşaretleridir**. "
            "Ayrıca birinci basamak hekimi hangi bulguda gebeyi evine göndereceğini, hangi bulguda acil ambulansla 2. basamağa sevk edeceğini ezbere bilmelidir. "
            "Altıncı bölümümüzde, **'Gebelikte Kardinal Tehlike İşaretleri, Acil Sevk Kriterleri (Hb < 7, Fundus ±4 cm), "
            "Fizyolojik Kilo Dağılımı ve Gebelik Toksemisi (Preeklampsi/Eklampsi)'** incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Gebelikte fizyolojik Braxton Hicks kasılmaları ile gerçek doğum eylemi sancılarını ayırt etmede hekimin sorgulayacağı en temel fark nedir?",
                "Gerçek sancıların düzenli aralıklarla gelmesi, şiddetinin artması, dinlenmekle geçmemesi ve rahim ağzında açılma (dilatasyon) yapmasıdır.",
                "Düzenlilik, şiddet artışı ve servikal açılma kriteri"
            ),
            make_branching_logic(
                "37 haftalık bir gebe, sabah uyandığında iç çamaşırının ılık berrak bir sıvıyla tamamen ıslandığını ancak hiçbir ağrısı veya kasılması olmadığını söylüyor.",
                "Bu gebeye aile hekiminin vereceği en doğru ve acil tıbbi talimat hangisidir?",
                [
                    {
                        "text": "Amniyon zarının erken yırtılmış (Erken Membran Rüptürü) olduğunu, kordon sarkması ve enfeksiyon riski nedeniyle ayakta durmadan, acilen yatar pozisyonda en yakın doğum hastanesine başvurması gerektiğini bildirmek",
                        "isCorrect": True,
                        "feedback": "Kusursuz Hayat Kurtarıcı Yaklaşım: Sancı olmasa dahi membran rüptürü acil obstetrik durumdur; hasta yürütülmeden sevk edilmelidir."
                    },
                    {
                        "text": "Sancı başlayana kadar evde beklemesini, sancı gelmezse 40. haftada kontrole gelmesini söylemek",
                        "isCorrect": False,
                        "feedback": "Ölümcül Hata: Saatler içinde koryoamniyonit ve intrauterin fetal kayıp gelişebilir."
                    },
                    {
                        "text": "Bunun idrar kaçırma olduğunu söyleyip mesane egzersizi tavsiye etmek",
                        "isCorrect": False,
                        "feedback": "Tıbbi İhmal: Amniyon sıvısı şüphesi her zaman hastanede teyit edilmelidir."
                    }
                ]
            )
        ]
    })

    return slides
