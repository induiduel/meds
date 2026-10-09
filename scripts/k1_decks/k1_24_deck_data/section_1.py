# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 1: Emboli Kavramı, Pulmoner Tromboembolizm (PTE) ve Klinik Tablolar (Slayt 1 - 10)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # Slayt 1: Emboli Kavramı ve Patolojik Tanımlar
    slides.append({
        "id": "k1-24-s01",
        "title": "Emboli Kavramı ve Patolojik Tanımlar: Trombozdan Emboliye Geçiş",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 1,
        "narrative": (
            "Hemodinamik patolojilerin en kritik klinik tablolarından biri olan emboli, doku perfüzyonunu ani olarak kesen mekanik bir olaydır: "
            "1. **Emboli (Embolus) Tanımı:** Dolaşım sistemi içinde kaynaklandığı anatomik noktadan koparak kan akımıyla uzak bölgelere taşınan, "
            "damar lümenini kısmen veya tamamen tıkayarak doku hasarına yol açan katı, sıvı veya gaz halindeki kitlelerdir. "
            "2. **Tromboemboli Üstünlüğü:** Tüm klinik embolilerin **>%99'u bir trombüsten kopan parçalardan (tromboemboli)** oluşur. "
            "Geriye kalan nadir kitleler ise yağ damlacıkları, hava/gaz kabarcıkları, amniyon sıvısı kalıntıları veya tümör hücre agregatlarıdır. "
            "3. **Tıkanma Yatağına Göre Ayrım:** "
            "- **Venöz Emboli:** Venöz dolaşımdan koparak sağ kalbe ve ardından pulmoner arter yatağına gider (Pulmoner Tromboembolizm). "
            "- **Arteriyel Emboli:** Sol kalpten veya büyük arterlerden kaynaklanıp periferik organlara dağılır (Sistemik Tromboembolizm ve İskemik Enfarktüs)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Dolaşım sisteminde kaynaklandığı damar duvarından koparak kan akımıyla taşınan ve lümeni tıkayan kitlelerin yüzde doksan dokuzdan fazlası bir trombüs parçasından oluşan tromboembolidir.",
                "tromboembolidir",
                "Trombüsten köken alan en yaygın klinik emboli türü"
            ),
            make_table(
                "Emboli Tipleri ve Temel Patolojik Özellikleri",
                ["Emboli Türü", "Fiziksel / Biyolojik Yapısı", "En Sık Kaynak Noktası", "Tipik Tıkanma Alanı"],
                [
                    [
                        "Tromboemboli (%99)",
                        "Fibrin ve trombosit zengin organize pıhtı",
                        {"text": "Bacak derin venleri veya kalp kaviteleri", "isMasked": True, "hint": "DVT veya mural sol ventrikül trombüsleri"},
                        "Pulmoner arter veya alt ekstremite arterleri"
                    ],
                    ["Yağ Embolisi", "Kemik iliği yağ hücreleri ve lipid damlacıkları", "Uzun kemik (femur/tibia) kırıkları", "Pulmoner ve serebral mikrodolaşım"],
                    ["Amniyon Sıvısı Embolisi", "Fetal skuamöz epitel, lanugo, mukus", "Doğum sırasında yırtılan uterin venler", "Anne pulmoner mikrovasküler yatağı"],
                    ["Hava / Gaz Embolisi", "Azot kabarcıkları veya atmosferik hava", "Dekompresyon (dalış) veya santral venöz kateter", "Sağ ventrikül hava kilidi ve akciğer"]
                ]
            ),
            make_micro_quiz(
                "Patoloji dersi klinik hemodinamik sınıflamasına göre insan vücudunda gelişen embolilerin yüzde doksan dokuzundan sorumlu olan primer patolojik oluşum hangisidir?",
                {
                    "A": "Tromboemboli (Trombüs parçası)",
                    "B": "Amniyon sıvısı globülleri",
                    "C": "Kolesterol kristalleri",
                    "D": "Serbest atmosferik hava kabarcığı",
                    "E": "Kemik iliği kaynaklı yağ damlacığı"
                },
                "A",
                {
                    "A": "Embolilerin >%99'u bir trombüsten kopan parçalardan (tromboemboli) köken alır.",
                    "B": "Amniyon sıvısı embolisi çok nadirdir (~1/40.000 doğum).",
                    "C": "Kolesterol embolisi aterom plağı ülserasyonunda görülür.",
                    "D": "Hava embolisi cerrahi/travmatik iyatrojenik tablodur.",
                    "E": "Yağ embolisi kemik kırıklarında görülür, genel emboliler içinde azınlıktadır."
                }
            )
        ]
    })

    # Slayt 2: Pulmoner Tromboembolizm (PTE) Epidemiyolojisi ve Mortalitesi
    slides.append({
        "id": "k1-24-s02",
        "title": "Pulmoner Tromboembolizmin (PTE) Epidemiyolojisi ve Klinik Önemi",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 2,
        "narrative": (
            "Pulmoner Tromboembolizm (PTE), modern tıpta hastanede yatan hastaların en sinsi ve önlenebilir ölüm nedenlerinden biridir: "
            "1. **İnsidans ve Yük:** Genel popülasyonda yılda yaklaşık 1.000 kişide 1-2 olgu görülür; hastanede yatan hastalarda sıklık dramatik artar. "
            "2. **Hastanede Mortalite Oranı:** Yatan hastaların otopsi serilerinde **%10 - 15 oranında pulmoner emboli** saptanır ve "
            "hastane içi ani ölümlerin en sık kardiyopulmoner nedenidir. "
            "3. **Klinik Sessizlik Paradoksu:** Pulmoner embolilerin **%60 - 80'i klinik olarak sessizdir (asemptomatiktir)**. "
            "Küçük emboliler bronşiyal dolaşım ve pıhtı lizis mekanizmaları sayesinde fark edilmeden organize olur ve damar duvarına kaynaşır. "
            "4. **Tekrarlama Riski (Rekürrens):** Bir kez pulmoner emboli geçiren bir hastada, antikoagülan başlanmazsa "
            "ikinci bir ölümcül emboli atağı geçirme riski katlanarak artar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Pulmoner tromboembolilerin yüzde altmış ile seksen kadarı klinik olarak sessiz seyreder ve küçük boyutu nedeniyle fark edilmeden damar duvarına organize olur.",
                "klinik olarak sessiz",
                "Küçük pulmoner embolilerin asemptomatik seyretme doğası"
            ),
            make_table(
                "Pulmoner Tromboembolizm Klinik Prezantasyon Spektrumu",
                ["Klinik Spektrum", "Görülme Oranı", "Fizyopatolojik Mekanizma", "Klinik Seyir / Prognoz"],
                [
                    [
                        "Sessiz / Asemptomatik",
                        "%60 - 80 (Çoğunluk)",
                        {"text": "Küçük damar tıkanması ve fibrinolizle lizis", "isMasked": True, "hint": "Endojen pıhtı eritme ve organizasyon"},
                        "Klinik bulgu vermez, damar duvarına katılır"
                    ],
                    ["Akut Pulmoner Enfarkt", "%10 - 15", "Sol kalp yetmezliği zemininde distal dal tıkanması", "Plevritik göğüs ağrısı, hemoptizi, frotman"],
                    ["Masif Emboli / Ani Ölüm", "%5", "Ana pulmoner arter bifurkasyonunda eyer embolusu", "Kardiyojenik şok, senkop, dakikalar içinde ölüm"],
                    ["Kronik KTEPH", "< %3", "Tekrarlayan küçük embolilerin fibrotik organizasyonu", "İlerleyici dispne, pulmoner hipertansiyon, kor pulmonale"]
                ]
            ),
            make_active_recall(
                "Hastanede yatan immobilize hastalarda gelişen pulmoner tromboembolilerin büyük çoğunluğunun (%60-80) rutin klinik vizitlerde gözden kaçmasının patofizyolojik nedeni nedir?",
                "Embolilerin küçük boyutlu olması, bronşiyal çift dolaşım sayesinde iskemi yapmaması ve fibrinolizle sessizce organize olmasıdır.",
                "Küçük pıhtıların çift dolaşım altında asemptomatik organizasyonu"
            )
        ]
    })

    # Slayt 3: PTE Kaynakları: Derin Ven Trombozu ve Diz Üstü Venlerin Rolü
    slides.append({
        "id": "k1-24-s03",
        "title": "PTE Kaynakları: Derin Ven Trombozu (DVT) ve Diz Üstü Venlerin Rolü",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 3,
        "narrative": (
            "Pulmoner embolusların köken aldığı anatomik odaklar klinik hekimlik ve koruyucu profilaksi açısından hayati önem taşır: "
            "1. **DVT Hâkimiyeti:** Pulmoner embolilerin **>%95'i alt ekstremite derin ven trombozundan (DVT)** kaynaklanır. "
            "2. **Diz Üstü Venlerin Kritik Önemi:** Embolilerin ezici çoğunluğu **diz üstündeki büyük derin venlerden** köken alır: "
            "- **Vena Poplitea** "
            "- **Vena Femoralis** "
            "- **Vena İliaca** "
            "Bu venlerin lümeni geniş olduğundan büyük pıhtı kitleleri barındırır; kopan parçalar ana pulmoner arterleri tıkayacak kalibreye sahiptir. "
            "3. **Baldır (Diz Altı) Venleri:** Tibial ve peroneal ven trombozları sıktır ancak bu pıhtılar nadiren masif ölümcül emboliye yol açar; "
            "fakat tedavi edilmezse proksimale (femoral vene) ilerleyerek öldürücü risk kazanır. "
            "4. **Nadir Odaklar:** Pelvik venler, vena cava inferior, sağ kalp boşlukları ve üst ekstremite kateter trombüsleri."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Pulmoner tromboembolilerin yüzde doksan beşinden fazlası alt ekstremite derin ven trombozundan, özellikle diz üstü derin venlerden köken alır.",
                "diz üstü derin venlerden",
                "Popliteal, femoral ve iliak venleri kapsayan anatomik seviye"
            ),
            make_table(
                "Venöz Tromboz Odakları ve Pulmoner Emboli Riski Matrisi",
                ["Venöz Anatomik Bölge", "Temsilci Damarlar", "Emboli Boyutu", "Masif Ölümcül PTE Riski"],
                [
                    [
                        "Diz Üstü Derin Venler",
                        "V. Femoralis, V. Poplitea, V. İliaca",
                        "Geniş çaplı, uzun fibrin silendirleri",
                        {"text": "Çok Yüksek (>%90 ölümcül emboli kaynağı)", "isMasked": True, "hint": "Masif ve eyer emboli yapan primer ven grubu"}
                    ],
                    ["Diz Altı (Baldır) Venleri", "V. Tibialis posterior, V. Peronea", "Küçük çaplı pıhtılar", "Düşük (ancak proksimale ilerleyebilir)"],
                    ["Pelvik Pleksus Venleri", "Prostatik ve uterin venöz pleksus", "Orta çaplı pıhtılar", "Cerrahi ve doğum sonrasında belirgin risk"],
                    ["Üst Ekstremite Venleri", "V. Subclavia, V. Jugularis interna", "Kateter ilişkili trombüsler", "Orta dereceli risk"]
                ]
            ),
            make_micro_quiz(
                "Acil servise ani nefes darlığı ve senkop ile getirilen ve pulmoner emboli tanısı alan bir hastada, embolusun koptuğu en olası primer anatomik ven hangisidir?",
                {
                    "A": "Vena femoralis (Diz üstü derin bacak veni)",
                    "B": "Vena saphena magna (Yüzeyel bacak veni)",
                    "C": "Vena cephalica (Üst ekstremite yüzeyel veni)",
                    "D": "Vena mesenterica superior",
                    "E": "Vena portae hepatis"
                },
                "A",
                {
                    "A": "PTE'lerin >%95'i diz üstü derin venlerden (femoral, popliteal, iliak) köken alır.",
                    "B": "Safena magna yüzeyel vendir; tromboflebit yapar ama nadiren PTE kaynağıdır.",
                    "C": "Sefalik ven yüzeyel üst ekstremite venidir.",
                    "D": "Mezenterik ven porta sistemine akar, karaciğere gider.",
                    "E": "Portal ven trombozu karaciğer öncesi portal hipertansiyon yapar, akciğere gidemez."
                }
            )
        ]
    })

    # Slayt 4: Virchow Triadı ile PTE Patogenezi ve Risk Faktörleri
    slides.append({
        "id": "k1-24-s04",
        "title": "Virchow Triadı ile PTE Patogenezi ve Klinik Risk Faktörleri",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 4,
        "narrative": (
            "DVT ve ardından pulmoner emboli gelişimi Rudolf Virchow'un tanımladığı üçlü patolojik zemin üzerinde yükselir: "
            "1. **Staz (Kan Akımında Yavaşlama / Durgunluk):** "
            "Uzun süreli yatak istirahati (>3 gün immobilizasyon), ortopedik alçılama, uzun süreli uçak yolculukları ('ekonomi sınıfı sendromu'), "
            "konjestif kalp yetmezliği ve variköz ven genişlemeleri kanın kapak ceplerinde göllenmesine yol açar. "
            "2. **Endotel Hasarı:** "
            "Kalça ve diz protezi cerrahileri, femur kırıkları, intravenöz kateterler, vaskülitler ve sigara dumanı endotel bütünlüğünü bozar; "
            "açığa çıkan subendotelyal kollajen trombositleri ve intrensek pıhtılaşmayı aktive eder. "
            "3. **Hiperkoagülabilite (Tromboza Yatkınlık):** "
            "- **Genetik Nedenler:** **Faktör V Leiden mutasyonu** (Aktive Protein C direnci), Protrombin G20210A mutasyonu, Antitrombin III eksikliği. "
            "- **Kazanılmış Nedenler:** Kanser (Trousseau sendromu / gezici tromboflebit), oral kontraseptifler, gebelik ve lohusalık, antifosfolipid sendromu."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Kalıtsal hiperkoagülabilite nedenleri arasında toplumda en sık görülen ve aktive protein C direncine yol açan genetik defekt Faktör V Leiden mutasyonudur.",
                "Faktör V Leiden",
                "Aktive protein C tarafından yıkılamayan mutant pıhtılaşma faktörü"
            ),
            make_causal_chain(
                "Virchow Triadı Zemininde Pulmoner Emboli Gelişim Zinciri",
                [
                    "1. İmmobilizasyon: Uzun süre yatağa bağımlı hastada baldır venlerinde kan stazı oluşması",
                    "2. Pıhtı Büyümesi: Trombosit ve fibrin birikimiyle ven kapakçıklarında derin kırmızı trombüsün organize olması",
                    "3. Fragmantasyon: Hastanın aniden ayağa kalkmasıyla artan venöz basınç sonucu trombüsün kopması",
                    "4. Akciğer Tıkanması: Pıhtının vena cava inferior ve sağ kalbi geçerek pulmoner arteri tıkaması"
                ]
            ),
            make_micro_quiz(
                "Pankreas adenokarsinomu olan 62 yaşındaki bir hastada vücudun farklı yerlerinde tekrarlayan venöz tromboz atakları ve ardından pulmoner emboli gelişmiştir. Malignite ilişkili bu hiperkoagülabilite tablosu tıp literatüründe hangi isimle anılır?",
                {
                    "A": "Trousseau Sendromu (Migratuar Tromboflebit)",
                    "B": "Waterhouse-Friderichsen Sendromu",
                    "C": "Goodpasture Sendromu",
                    "D": "Raynaud Fenomeni",
                    "E": "Budd-Chiari Sendromu"
                },
                "A",
                {
                    "A": "Tümörlerin prokoagülan salgılamasıyla gelişen gezici venöz tromboz tablosu Trousseau sendromudur.",
                    "B": "Waterhouse-Friderichsen meningokoksemide bilateral adrenal nekrozdur.",
                    "C": "Goodpasture glomerül ve alveol bazal membranına karşı otoantikor hastalığıdır.",
                    "D": "Raynaud soğukla tetiklenen vazospazmdır.",
                    "E": "Budd-Chiari hepatik ven trombozudur."
                }
            )
        ]
    })

    # Slayt 5: Masif Pulmoner Emboli ve Eyer (Saddle) Embolusu
    slides.append({
        "id": "k1-24-s05",
        "title": "Masif Pulmoner Emboli ve Eyer (Saddle) Embolusu: Akut Kor Pulmonale",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 5,
        "narrative": (
            "Pulmoner embolilerin yaklaşık %5'i dramatik ve ölümcül bir klinik tabloyla seyreder: "
            "1. **Eyer (Saddle) Embolus Tanımı:** Bacak derin venlerinden kopan devasa bir tromboembolusun, "
            "ana pulmoner arterin ikiye ayrıldığı **bifurkasyon (çatallanma) bölgesine bir eyer gibi oturarak** her iki ana pulmoner dalı tıkamasıdır. "
            "2. **Hemodinamik Çöküş:** Pulmoner arter yatağının **>%50'si aniden tıkandığında**, sağ ventrikülün önündeki vasküler direnç fırlar. "
            "3. **Akut Kor Pulmonale:** Sağ ventrikül bu ani dirence karşı pompalayamaz, süratle dilate olur ve akut sağ kalp yetmezliğine girer. "
            "İnterventriküler septum sola doğru bombeleşir ve sol ventrikül doluşunu engeller. "
            "4. **Kardiyojenik Şok ve Elektromekanik Disosiasyon:** Sol ventriküle kan dönemediği için kalp debisi sıfıra iner; "
            "hasta ani dispne, göğüs ağrısı, siyanoz, senkop geçirir ve dakikalar içinde **kardiyak arrest (PEA / Elektromekanik Disosiasyon)** ile kaybedilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Ana pulmoner arterin dallanma noktasına oturarak her iki pulmoner arter lümenini aynı anda tıkayan dev tromboembolusa eyer embolusu adı verilir.",
                "eyer embolusu",
                "Pulmoner bifurkasyona oturan semer şekilli ölümcül kitle"
            ),
            make_table(
                "Masif Pulmoner Embolide Hemodinamik Kaskad",
                ["Patolojik Basamak", "Organ Düzeyindeki Değişim", "Klinik Yansıması"],
                [
                    ["Bifurkasyon Tıkanması", "Ana pulmoner arterde eyer embolus yerleşimi", "Pulmoner kan akımının >%50 ani kesilmesi"],
                    [
                        "Sağ Ventrikül Aşırı Yükü",
                        {"text": "Akut Kor Pulmonale ve sağ ventrikül dilatasyonu", "isMasked": True, "hint": "Akciğer direncine bağlı akut sağ kalp genişlemesi"},
                        "Boyun venlerinde aşırı dolgunluk, hipotansiyon"
                    ],
                    ["Sol Ventrikül Boşalması", "Septumun sola kayması ve doluş yetersizliği", "Kardiyak debide dramatik çöküş ve taşikardi"],
                    ["Kardiyovasküler Arrest", "Doku perfüzyonu kaybı ve miyokard iskemisi", "Elektromekanik disosiasyon ve ani ölüm"]
                ]
            ),
            make_micro_quiz(
                "Büyük bir ortopedik operasyon sonrası taburculuk aşamasındaki hastanın yataktan kalktığı anda aniden yere yığıldığı, derin siyanoz ve nabızsız elektriksel aktivite (PEA) geliştirdiği görülmüştür. Otopside ana pulmoner bifurkasyonda saptanması beklenen lezyon hangisidir?",
                {
                    "A": "Eyer (Saddle) Embolusu",
                    "B": "Koroner arter aterom plağı rüptürü",
                    "C": "Krupöz pnömoni hepatizasyonu",
                    "D": "Sol ventrikül apeksinde kalsifiye anevrizma",
                    "E": "Aort kapak vejetasyonu"
                },
                "A",
                {
                    "A": "Bifurkasyonu tıkayan dev eyer embolusu ani sağ kalp yetmezliği ve PEA ile saniyeler içinde ölüme yol açar.",
                    "B": "Koroner rüptür MI yapar fakat DVT zemininde bifurkasyon tıkayan eyer embolusudur.",
                    "C": "Pnömoni günler içinde gelişen enfeksiyondur.",
                    "D": "Apeks anevrizması kronik lezyondur.",
                    "E": "Aort vejetasyonu sistemik arteriyel emboli yapar, pulmoner arteri tıkamaz."
                }
            )
        ]
    })

    # Slayt 6: Orta Boy Pulmoner Emboliler ve Çift Dolaşım Etkisi
    slides.append({
        "id": "k1-24-s06",
        "title": "Orta Boy Pulmoner Emboliler ve Akciğerin Çift Kan Dolaşımı",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 6,
        "narrative": (
            "Orta boy pulmoner arter dallarını tıkayan embolilerin kliniğini belirleyen en kritik anatomik faktör akciğerin çift kan dolaşımıdır: "
            "1. **Çift Vasküler Beslenme:** Akciğer dokusu iki ayrı arteriyel sistemden beslenir: "
            "- **Pulmoner Arterler:** Fonksiyonel gaz değişimini sağlayan düşük basınçlı sistem. "
            "- **Bronşiyal Arterler:** Torasik aortadan çıkan ve parankimin nutrisyonel gereksinimini sağlayan yüksek basınçlı sistem. "
            "2. **Sağlıklı Kalpteki Seyir:** Kardiyovasküler fonksiyonu normal olan genç bir bireyde orta boy bir pulmoner arter dalı tıkandığında, "
            "bronşiyal arter dolaşımı parankimi canlı tutmaya yeterlidir; **enfarktüs gelişmez**, yalnızca lokal alveolar kanama izlenir. "
            "3. **Kalp Yetmezliğinde Enfarktüs Riski:** Eğer hastada sol kalp yetmezliği (bronşiyal perfüzyonda düşüş) veya kronik KOAH varsa, "
            "orta boy bir pulmoner emboli kollateral yetersizliği nedeniyle **akut pulmoner enfarktüse** yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Akciğer parankiminin orta boy pulmoner embolilere rağmen enfarktüse uğramasını engelleyen temel faktör pulmoner arterlerin yanında torasik aortadan gelen bronşiyal arterlerin sağladığı çift kan dolaşımıdır.",
                "çift kan dolaşımıdır",
                "Akciğeri iki ayrı arteriyel sistemle besleyen anatomik mekanizma"
            ),
            make_table(
                "Akciğerin Vasküler Sistemleri ve İskemiye Yanıtı",
                ["Arteriyel Sistem", "Kaynak Noktası", "Primer İşlevi", "Orta Boy Embolideki Rolü"],
                [
                    ["Pulmoner Arter", "Sağ ventrikül çıkışı", "Alveollerde gaz değişimi (oksijenasyon)", "Tıkandığında lokal perfüzyon kesilir"],
                    [
                        "Bronşiyal Arterler",
                        "Torasik aorta",
                        {"text": "Akciğer parankiminin beslenmesi (nutrisyonel)", "isMasked": True, "hint": "Parankim hücrelerini besleyen sistemik arterler"},
                        "Kollateral sağlayarak enfarktüs gelişimini önler"
                    ]
                ]
            ),
            make_micro_quiz(
                "Sol kalp yetmezliği veya kronik akciğer hastalığı OLMAYAN genç ve sağlıklı bir bireyde orta çaplı bir pulmoner arter dalının tromboemboli ile tıkanması durumunda genellikle enfarktüs gelişmemesinin temel anatomik nedeni hangisidir?",
                {
                    "A": "Bronşiyal arterler yoluyla sağlanan çift dolaşımın dokuyu beslemesi",
                    "B": "Akciğer parankiminin oksijensizliğe saatlerce dirençli olması",
                    "C": "Pulmoner arterlerin düz kas tabakasının bulunmaması",
                    "D": "Plevral sıvının difüzyonla parankimi beslemesi",
                    "E": "Alveol epitelinin doğrudan trakeadan oksijen emebilmesi"
                },
                "A",
                {
                    "A": "Aorttan çıkan bronşiyal arterler parankime oksijen taşımaya devam ettiğinden çift dolaşım enfarktüsü önler.",
                    "B": "Hücreler saatlerce dirençli değildir, bronşiyal kan akımı esastır.",
                    "C": "Damarların kas tabakası iskemi koruması sağlamaz.",
                    "D": "Plevral sıvı besleme yapmaz.",
                    "E": "Doğrudan trakeadan doku perfüzyonu beslenemez."
                }
            )
        ]
    })

    # Slayt 7: Distal Küçük ve Tekrarlayan Emboliler: KTEPH Gelişimi
    slides.append({
        "id": "k1-24-s07",
        "title": "Distal Küçük ve Tekrarlayan Emboliler: Kronik Pulmoner Hipertansiyon",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 7,
        "narrative": (
            "Pulmoner arter yatağının en uç dallarını tutan veya zaman içinde sessizce tekrarlayan tromboemboliler özel kronik klinik tablolara yol açar: "
            "1. **Distal Arteriolar Emboliler:** Uç arteriyollere yerleşen küçük emboliler, plevraya çok yakın oldukları ve "
            "bronşiyal kollateral uç noktalarında bulundukları için sıklıkla **küçük periferik pulmoner enfarktüslere** neden olur. "
            "Hastada batıcı plevritik göğüs ağrısı, nefes darlığı ve kanlı balgam (hemoptizi) görülür; plevral sürtünme sesi (frotman) duyulabilir. "
            "2. **Tekrarlayan (Rekürren) Mikroemboliler:** Aylar veya yıllar boyunca sessizce venöz yataktan kopup akciğere gelen çok sayıda küçük pıhtı, "
            "damar duvarında organizasyon ve intimal fibrozise yol açar. "
            "3. **KTEPH ve Kronik Kor Pulmonale:** Pulmoner damar yatağının toplam kesit alanı daralır; bu durum "
            "**Kronik Tromboembolik Pulmoner Hipertansiyon (KTEPH)** tablosuna ve aylar içinde sağ ventrikül hipertrofisiyle seyreden kronik kor pulmonaleye ilerler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Aylar boyunca tekrarlayan küçük pulmoner embolilerin damar duvarında organize olup lümeni daraltması sonucunda kronik tromboembolik pulmoner hipertansiyon gelişir.",
                "kronik tromboembolik pulmoner hipertansiyon",
                "Tekrarlayan pıhtıların akciğer damar yatağını daraltmasıyla doğan klinik tablo"
            ),
            make_table(
                "Küçük ve Tekrarlayan Pulmoner Embolilerin Klinik Evreleri",
                ["Patoloji Tipi", "Zaman Çizelgesi", "Damarsal Morfoloji", "Uzun Dönem Sonucu"],
                [
                    ["Akut Distal Mikroemboli", "Dakikalar / Saatler", "Uç arteriyolde obstrüksiyon ve lokal iskemi", "Subplevral kama enfarktüs, hemoptizi"],
                    [
                        "Organize Mikroemboli",
                        "Haftalar / Aylar",
                        {"text": "Fibröz bantlar ve damar içi 'ağ' (web) yapıları", "isMasked": True, "hint": "Pıhtı rezolüsyonu sonrası kalan damar içi fibröz köprüler"},
                        "Vasküler lümende kalıcı daralma"
                    ],
                    ["KTEPH", "Yıllar", "Yaygın pulmoner arter medial hipertrofisi", "İlerleyici sağ kalp yetmezliği (Kronik Kor Pulmonale)"]
                ]
            ),
            make_active_recall(
                "Hafif efor dispnesi ile başvuran ve klinik geçmişinde açıklanamayan tekrarlayan DVT öyküsü bulunan bir hastada ekokardiyografide sağ ventrikül kalınlaşması (hipertrofisi) saptanmıştır. Bu kronik sürecin adı nedir?",
                "Kronik Tromboembolik Pulmoner Hipertansiyondur (KTEPH - Kronik Kor Pulmonale).",
                "Tekrarlayan embolilere sekonder gelişen sağ kalp hipertrofisi"
            )
        ]
    })

    # Slayt 8: Pulmoner Enfarktüs Morfolojisi: Kama Biçimli Hemorajik Enfarkt
    slides.append({
        "id": "k1-24-s08",
        "title": "Pulmoner Enfarktüs Morfolojisi: Kama Biçimli Hemorajik Enfarkt",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 8,
        "narrative": (
            "Pulmoner emboliye bağlı gelişen doku nekrozu son derece karakteristik makroskobik ve mikroskobik morfolojiye sahiptir: "
            "1. **Kırmızı (Hemorajik) Yapı:** Akciğer gevşek süngerimsi bir dokudur ve bronşiyal arterlerden kan sızmaya devam eder; "
            "bu nedenle pulmoner enfarktüs **daima kırmızı (hemorajik) tiptedir**. "
            "2. **Kama (Wedge) Morfolojisi:** Enfarkt alanı klasik olarak **kama veya piramit biçimindedir**: "
            "- **Tabanı:** Akciğer plevra yüzeyine oturur. "
            "- **Tepesi (Apeksi):** İskemiye yol açan tıkalı pulmoner arter dalına doğru yönelmiştir. "
            "3. **Plevral Katılım:** Enfarkt plevraya ulaştığında üzerinde steril bir fibrinöz eksüda toplanır (**Fibrinöz Plörit**); "
            "bu durum hastada nefes almakla şiddetlenen batıcı göğüs ağrısı ve plevral frotmana yol açar. "
            "4. **Mikroskopik Görünüm:** Alveol duvarlarında **koagülatif nekroz**, eritrositlerle tamamen dolmuş alveolar lümenler ve "
            "erken dönemde nötrofil, geç dönemde hemosiderin yüklü makrofaj infiltrasyonu görülür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Akciğer enfarktüsleri daima kırmızı hemorajik renkte olup tabanı plevraya oturan ve tepesi tıkalı damara bakan kama biçimli bir morfolojiye sahiptir.",
                "kama biçimli",
                "Akciğer ve katı organ enfarktüslerinin klasik geometrik kesit şekli"
            ),
            make_table(
                "Pulmoner Enfarktüsün Makroskobik ve Mikroskobik Özellikleri",
                ["Patolojik Düzey", "Karakteristik Görünüm", "Altta Yatan Patofizyolojik Neden"],
                [
                    ["Makroskobik Renk", "Koyu kırmızı - mor, sert ve hava içermeyen alan", "Bronşiyal damarlardan nekrotik alana kan sızması"],
                    [
                        "Makroskobik Şekil",
                        {"text": "Kama (Piramit) biçimli geometri", "isMasked": True, "hint": "Tabanı plevrada, tepesi damarda üçgen kesit"},
                        "Damarsal dallanma ağacının vasküler anatomisi"
                    ],
                    ["Plevral Yüzey", "Mat, donuk ve fibrin örtüsüyle kaplı", "Nekrozun visseral plevraya ulaşıp plörit yapması"],
                    ["Mikroskopi", "Koagülatif nekroz ve eritrositle dolu alveoller", "İskemik hücre ölümü ve yoğun kapiller kaçak"]
                ]
            ),
            make_micro_quiz(
                "Otopsi yapılan bir hastanın sağ akciğer alt lobunda tabanı visseral plevraya oturan, koyu kırmızı-kahverengi renkte, sınırları belirgin kama şeklinde solid bir lezyon saptanmıştır. Bu lezyonun patolojik tanısı hangisidir?",
                {
                    "A": "Pulmoner Hemorajik Enfarktüs",
                    "B": "Akut Lober Pnömoni Gri Hepatizasyonu",
                    "C": "Akciğer Tüberkülomu",
                    "D": "Bronşiektazi kavitasyonu",
                    "E": "Silikotik granülomatöz nodül"
                },
                "A",
                {
                    "A": "Tabanı plevraya oturan kama biçimli kırmızı solid lezyon pulmoner hemorajik enfarktüsün klasik otopsi bulgusudur.",
                    "B": "Gri hepatizasyonda tüm lob gridir, pıhtı tıkanmasıyla kama oluşmaz.",
                    "C": "Tüberkülom kazeifikasyon nekrozu içerir.",
                    "D": "Bronşiektazi genişlemiş hava yollarıdır.",
                    "E": "Silikozis konsantrik hyalinize nodüller yapar."
                }
            )
        ]
    })

    # Slayt 9: [TEKRAR SAYFASI - CHECKPOINT 1] Pulmoner Tromboembolizm Patolojisi ve Klinik Tablolar
    slides.append({
        "id": "k1-24-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Pulmoner Tromboembolizm Patolojisi ve Klinik Tablolar",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 9,
        "narrative": (
            "Bu birinci checkpoint sayfasında, emboli kavramı ve pulmoner tromboembolizm ilkelerini özetliyoruz: "
            "1. **Emboli Tanımı:** Dolaşımda serbestçe taşınan katı, sıvı veya gaz kitleleridir; %99'dan fazlası TROMBOEMBOLİDİR. "
            "2. **Kaynak:** Pulmoner embolilerin >%95'i bacak derin ven trombozundan, özellikle DİZ ÜSTÜ (femoral, popliteal, iliak) venlerden kopar. "
            "3. **Virchow Triadı:** Staz, endotel hasarı ve hiperkoagülabilite (Faktör V Leiden, kanser vb.) temel pıhtı zeminidir. "
            "4. **Klinik Dağılım:** %60-80'i sessiz seyreder ve organize olur; %5'i masif olup bifurkasyona oturarak EYER EMBOLUSU ile ani ölüm yapar. "
            "5. **Çift Dolaşım:** Akciğer pulmoner ve bronşiyal çift dolaşıma sahip olduğundan sağlıklı gençlerde orta boy emboli enfarktüs yapmaz. "
            "6. **Pulmoner Enfarkt:** Sol kalp yetmezliği veya distal dal tıkanmasında gelişir; DAİMA KIRMIZI (hemorajik) ve KAMA biçimlidir. "
            "7. **KTEPH:** Tekrarlayan küçük emboliler damar yatağını daraltarak aylar içinde kronik kor pulmonaleye yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s09-1",
                "Pulmoner tromboembolilerin yüzde doksan beşinden fazlası vücudun hangi anatomik damar bölgesindeki derin ven trombozundan kaynaklanır?",
                "Diz üstü alt ekstremite venlerinden kaynaklanır.",
                "Popliteal, femoral ve iliak damar yatağı",
                "PTE Kaynakları"
            ),
            make_flashcard(
                "k1-24-fc-s09-2",
                "Ana pulmoner arterin çatallanma (bifurkasyon) bölgesine oturarak her iki ana dalı birden tıkayan ve ani ölüme yol açan masif emboliye ne ad verilir?",
                "Eyer (saddle) embolusu adı verilir.",
                "Binek hayvanının sırtına konulan semer biçimli kitle anatomisi",
                "Masif Emboli"
            ),
            make_flashcard(
                "k1-24-fc-s09-3",
                "Akciğer dokusunda gelişen enfarktüslerin daima kırmızı (hemorajik) renkte olmasının temel anatomik ve vasküler gerekçesi nedir?",
                "Pulmoner ve bronşiyal çift dolaşım mevcudiyetidir.",
                "Aorttan ayrılan sistemik arterler ile sağ kalpten gelen damarların paralel kanlanması",
                "Pulmoner Enfarktüs"
            )
        ],
        "interactiveElements": [
            make_table(
                "Pulmoner Tromboembolizm Boyut ve Klinik Sonuç Özeti",
                ["Emboli Büyüklüğü / Tipi", "Tıkadığı Damar Düzeyi", "Tipik Klinik Sonucu"],
                [
                    ["Küçük Emboli (%60-80)", "Periferik küçük arteriyoller", "Sessiz, asemptomatik, fibrinoliz ile rezolüsyon"],
                    ["Masif Eyer Embolusu (%5)", "Ana pulmoner arter bifurkasyonu", "Akut sağ kalp yetmezliği, şok ve ani kardiyak arrest"],
                    [
                        "Distal Enfarktüs Embolisi",
                        "Subplevral küçük dallar",
                        {"text": "Kama biçimli kırmızı hemorajik enfarktüs", "isMasked": True, "hint": "Plevritik ağrı ve hemoptiziyle seyreden lezyon"}
                    ],
                    ["Tekrarlayan Mikroemboliler", "Yaygın prekapiller arteriyoller", "KTEPH ve kronik kor pulmonale"]
                ]
            ),
            make_micro_quiz(
                "Pulmoner tromboembolizm patolojisi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Pulmoner embolilerin çoğu (%60-80) asemptomatiktir ve organize olup damar duvarına kaynaşır",
                    "B": "Akciğer enfarktüsleri uç arter beslenmesi nedeniyle daima beyaz (soluk) enfarktüslerdir",
                    "C": "Eyer embolusu ana pulmoner arter bifurkasyonunu tıkayarak akut kor pulmonaleye yol açar",
                    "D": "PTE'lerin en sık kaynağı diz üstü derin ven trombozudur",
                    "E": "Tekrarlayan pulmoner mikroemboliler pulmoner hipertansiyona neden olabilir"
                },
                "B",
                {
                    "A": "Doğrudur; küçük emboliler çoğunlukla sessiz seyreder.",
                    "B": "YANLIŞTIR; Akciğer enfarktüsleri çift dolaşım ve gevşek doku nedeniyle DAİMA KIRMIZI (hemorajik) enfarktüslerdir. Beyaz enfarktüs kalp, dalak ve böbrekte görülür.",
                    "C": "Doğrudur; eyer embolusu masif obstrüksiyon yapar.",
                    "D": "Doğrudur; popliteal ve femoral venler primer kaynaktır.",
                    "E": "Doğrudur; KTEPH gelişebilir."
                }
            )
        ]
    })

    # Slayt 10: Bölüm Özeti: Pulmoner Dolaşımdan Sistemik Tromboembolizme Geçiş
    slides.append({
        "id": "k1-24-s10",
        "title": "Bölüm Özeti: Pulmoner Dolaşımdan Sistemik Tromboembolizme Geçiş",
        "section": "Emboli Kavramı, Pulmoner Tromboembolizm ve Klinik Tablolar",
        "slideNumber": 10,
        "narrative": (
            "Pulmoner tromboembolizm konusunu tamamlarken hekimlik pratiğinde akılda tutulması gereken temel prensipleri topluyoruz: "
            "1. **Venöz Tromboz Akciğerde Sonlanır:** Venöz sistemde oluşan pıhtılar kalbin sağ tarafına geçerek pulmoner arterleri tıkar. "
            "Dolayısıyla bacakta DVT gelişen bir hastanın beynine pıhtı atması normal anatomide imkansızdır (özel intrakardiyak şantlar hariç!). "
            "2. **Ölümcül Risk Dinamikleri:** >%50 tıkanma masif hemodinamik kollaps ve akut kor pulmonale demektir. "
            "3. **Kollateralin Gücü:** Çift dolaşım sayesinde akciğer diğer organlara göre iskemiye daha dirençlidir. "
            "4. **Sonraki Bölüme Köprü:** Bir sonraki bölümümüzde sol kalpten kaynaklanıp arteriyel sistem boyunca periferik organlara dağılan "
            "'Sistemik Tromboembolizm' mekanizmalarını, intrakardiyak mural trombüsleri ve sağdan sola geçen 'Paradoksal Emboli'yi inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Venöz dolaşımda oluşan bir tromboembolusun normal kardiyovasküler yolda sol kalbe geçememesi nedeniyle doğrudan beyin veya böbreğe gitmesi imkansız olup pıhtı akciğer filtre yatağında tutulur.",
                "akciğer filtre yatağında",
                "Venöz kanın sistemik arterlere geçmeden önce süzüldüğü kapiller filtre organı"
            ),
            make_active_recall(
                "Venöz sistemden kopan bir DVT pıhtısının akciğere gitmeden sol kalbe geçerek beyin arterlerini tıkaması (inme yapması) patolojide hangi özel terimle adlandırılır?",
                "Paradoksal emboli (sağdan sola şant aracılığıyla) olarak adlandırılır.",
                "PFO veya ASD üzerinden gerçekleşen çapraz emboli mekanizması"
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi pulmoner tromboemboli patolojisinde hekimin acil klinik alarm olarak değerlendirmesi gereken bir durumdur?",
                {
                    "A": "Ani dispne ve hipotansiyonla birlikte juguler venöz dolgunluk gelişmesi (Sağ ventrikül yetmezliği)",
                    "B": "Küçük bir periferik embolinin aylar içinde rezolüsyona uğraması",
                    "C": "Bronşiyal arterlerin akciğer parankimine oksijen taşımaya devam etmesi",
                    "D": "Genç hastada orta boy embolinin enfarktüs yapmadan atlatılması",
                    "E": "Fibrinolitik sistemin plazmin aracılığıyla küçük fibrin ağlarını eritmesi"
                },
                "A",
                {
                    "A": "Ani dispne, hipotansiyon ve boyun ven dolgunluğu masif eyer embolusu ve akut kor pulmonale alarmıdır.",
                    "B": "Rezolüsyon fizyolojik iyileşmedir.",
                    "C": "Bronşiyal kanlanma koruyucudur.",
                    "D": "Enfarktütsüz atlatma beklenen tablodur.",
                    "E": "Fibrinoliz koruyucu mekanizmadır."
                }
            )
        ]
    })

    return slides
