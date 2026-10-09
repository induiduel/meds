"""
Akut Enflamasyon (Ders 9) - Bölüm 2: Tarihsel Temeller, 5 Kardinal Belirti ve 5R Adımları
Slayt 11 - 20 (Checkpoint 2: Slayt 19)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "slideNumber": 11,
        "title": "Tarihsel Kökenler: Mısır Papirüslerinden Antik Roma'ya",
        "subtitle": "Edwin Smith papirüsü, Celsus'un dört kardinal bulgusu ve Virchow'un beşinci katkısı",
        "badge": "Tıp Tarihi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Enflamasyon insanlık tarihinin bilinen en eski klinik gözlemlerinden biridir. MÖ 3000 yıllarına ait "
            "antik Mısır **Edwin Smith Cerrahi Papirüsü** yaralardaki ısı artışı ve akıntıyı tarif eden ilk yazılı belgedir.\n\n"
            "> [TEMEL BİLGİ] MS 1. yüzyılda Romalı yazar **Cornelius Celsus**, 'De Medicina' adlı eserinde enflamasyonun "
            "bugün de tıp eğitiminin temel taşı olan dört kardinal lokal belirtisini ölümsüzleştirmiştir: **Rubor (Kızarıklık)**, "
            "**Tumor (Şişlik)**, **Calor (Sıcaklık)** ve **Dolor (Ağrı)**.\n\n"
            "Yaklaşık 1800 yıl sonra, 19. yüzyılda hücresel patolojinin babası **Rudolf Virchow**, bu dört klasik bulguya "
            "beşinci kardinal belirtiyi eklemiştir: **Functio Laesa (Fonksiyon Kaybı)**."
        ),
        "medicalTerms": [
            {"term": "Kardinal Belirti", "explanation": "Bir hastalığın veya patolojik durumun en tipik, karakteristik ana klinik göstergeleridir."},
            {"term": "Functio Laesa", "explanation": "İltihaplı doku veya organın mekanik ödem ve ağrı nedeniyle normal fizyolojik görevini yapamamasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Celsus'un 4 bulgusu: Rubor, Tumor, Calor, Dolor; Virchow'un eklediği 5. bulgu: Functio laesa'dır.",
            "📌 [SINAV SPOTU] Edwin Smith papirüsü enflamasyondan bahseden en eski cerrahi kaynaktır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Celsus Dörtlüsü", "desc": "Rubor (kızarıklık), Tumor (şişlik), Calor (sıcaklık), Dolor (ağrı).", "isKey": True},
                {"title": "Virchow Katkısı", "desc": "Functio laesa (işlev kaybı) ile tablo tamamlanmıştır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Enflamasyonun dört klasik kardinal bulgusuna beşinci olarak fonksiyon kaybını (functio laesa) ekleyen bilim insanı Rudolf Virchow olmuştur.",
                "Rudolf Virchow",
                "Hücresel patolojinin kurucusu olan ünlü Alman patoloğu anımsayınız"
            ),
            make_active_recall(
                "Cornelius Celsus tarafından MS 1. yüzyılda tarif edilen dört klasik kardinal lokal enflamasyon bulgusu Latince terimleriyle nelerdir?",
                "1) Rubor (kızarıklık), 2) Tumor (şişlik/ödem), 3) Calor (sıcaklık artışı), 4) Dolor (ağrı/acı)."
            )
        ]
    })

    # Slide 12
    slides.append({
        "slideNumber": 12,
        "title": "Rubor (Kızarıklık) ve Calor (Sıcaklık): Hipereminin Fizyopatolojisi",
        "subtitle": "Arteriyoler vazodilatasyon, kapiller yatak genişlemesi ve lokal kan göllenmesi",
        "badge": "Vasküler Patoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Enflamasyonlu bir derinin veya mukozanın parlak kırmızı renkte görülmesi (**Rubor**) ve el dokundurulduğunda "
            "ılık hissedilmesi (**Calor**), ortak bir hemodinamik olayın doğrudan sonucudur:\n\n"
            "- Hasar anında salınan **histamin ve nitrik oksit (NO)**, prekapiller sfinkterleri ve prekapiller arteriyol "
            "düz kaslarını gevşetir.\n"
            "- Açılan kapiller yataklara yüksek debiyle arteryel kan hücum eder; bu duruma **aktif hiperemi** denir.\n"
            "- Eritrositlerin taşıdığı oksijenli oksihemoglobin dokuya canlı kırmızı rengi (rubor) verir.\n"
            "- Vücudun 37°C'lik sıcak santral kor kanının periferik dokuya hızla dolması ise yüzeyel sıcaklık artışını (calor) oluşturur.\n\n"
            "> Not: Calor bulgusu yalnızca yüzeyel deri/ekstremite enflamasyonlarında belirgindir; vücut içi iç organlar zaten 37°C'dedir."
        ),
        "medicalTerms": [
            {"term": "Aktif Hiperemi", "explanation": "Arteriyollerin genişlemesi sonucu dokudaki kapiller yataklara arteryel kan akışının artmasıdır."},
            {"term": "Nitrik Oksit (NO)", "explanation": "Endotelden salınarak damar düz kasında cGMP artışı yoluyla vazodilatasyon yapan gaz mediyatördür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Rubor ve Calor'un altta yatan ortak fizyopatolojik mekanizması arteriyoler vazodilatasyon ve aktif hiperemidir.",
            "📌 [SINAV SPOTU] Histamin ve Nitrik Oksit (NO) erken faz vazodilatasyonunun primer mediyatörleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Rubor Mekanizması", "desc": "Genişleyen kapillerlerde oksihemoglobin zengini eritrosit göllenmesi.", "isKey": True},
                {"title": "Calor Mekanizması", "desc": "Sıcak kor kanın periferik mikrodolaşıma pompalanması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "İstirahat Doku Perfüzyonu vs Enflamatuvar Aktif Hiperemi",
                "İstirahat Doku Perfüzyonu",
                "Prekapiller sfinkterlerin çoğu kapalıdır, kapiller yatağın sadece bir kısmı perfüze edilir, doku pembe-normal renktedir.",
                "Enflamatuvar Aktif Hiperemi",
                "Prekapiller sfinkterler tamamen açılır, tüm kapiller ağ genişler, masif kan göllenmesiyle rubor ve calor oluşur."
            ),
            make_cloze(
                "Akut enflasyonda rubor ve calor bulgularının ortaya çıkışından sorumlu temel vasküler mekanizma aktif hiperemi gelişimidir.",
                "aktif hiperemi",
                "Arteriyollerin genişlemesiyle kapiller yatağa hücum eden kan akımı artışı"
            )
        ]
    })

    # Slide 13
    slides.append({
        "slideNumber": 13,
        "title": "Tumor (Şişlik): Vasküler Kaçak ve Eksüda Birikimi",
        "subtitle": "Artmış mikrovasküler geçirgenlik, plazma proteinleri ve doku turgor basıncının artışı",
        "badge": "Ödem Biyolojisi",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Enflamasyonun üçüncü kardinal belirtisi olan **Tumor (Şişlik)**, hasarlı dokuda interstisyel sıvı hacminin "
            "patolojik olarak artmasıdır (enflamatuvar ödem).\n\n"
            "Gelişim mekanizması iki yönlüdür:\n\n"
            "1. **Hidrostatik Basınç Artışı:** Vazodilatasyon nedeniyle kapiller içi kan basıncı yükselir ve sıvıyı dışarı iter.\n"
            "2. **Endotelyal Geçirgenlik Artışı (Ana Faktör):** Postkapiller venüllerde endotel hücreleri büzüşür; "
            "aralarındaki interendotelyal porlar açılır. Normalde damarda kalan albümin ve fibrinojen gibi dev plazma "
            "proteinleri dokuya kaçar.\n\n"
            "> Proteinlerin dokuya geçmesi interstisyel kolloid onkotik basıncı fırlatır; Starling dengesi çöker ve masif "
            "**protein zengini sıvı (eksüda)** dokuyu şişirir."
        ),
        "medicalTerms": [
            {"term": "Eksüda", "explanation": "Artmış vasküler geçirgenliğe bağlı gelişen, protein ve hücresel debris içeriği yüksek enflamatuvar ödem sıvısıdır."},
            {"term": "Kolloid Onkotik Basınç", "explanation": "Plazma proteinlerinin (başta albümin) suyu damar lümeninde tutmasını sağlayan ozmotik çekim gücüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tumor (enflamatuvar şişlik) transüda değil, yüksek proteinli EKSÜDA birikimidir.",
            "📌 [SINAV SPOTU] Enflamatuvar ödemin en kritik belirleyicisi mikrovasküler geçirgenlik artışıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Venüler Porlar", "desc": "Endotel kontraksiyonu ile proteinlerin geçebileceği yarıklar oluşur.", "isKey": True},
                {"title": "Onkotik Çöküş", "desc": "Dokuya kaçan albümin suyu damardan interstisyuma çeker.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Enflamatuvar Ödem (Tumor) Oluşum Zinciri",
                [
                    "1. Enflamatuvar mediyatörler postkapiller venül endotel hücrelerindeki reseptörlere bağlanır",
                    "2. Endotel hücreleri aktomiyozin iskeletini kasarak aralarında interendotelyal boşluklar açar",
                    "3. Albümin ve fibrinojen gibi yüksek molekül ağırlıklı plazma proteinleri doku aralığına sızar",
                    "4. İnterstisyel kolloid onkotik basınç yükselerek suyu çeker ve klinikte 'Tumor' (şişlik) belirir"
                ]
            ),
            make_active_recall(
                "Kalp yetmezliğindeki ödem ile akut enflamasyondaki ödem arasındaki temel biyokimyasal fark nedir?",
                "Kalp yetmezliğindeki ödem vasküler geçirgenlik artışı olmaksızın sadece hidrostatik basınç artışına bağlı proteinsiz 'transüda'dır; akut enflamasyondaki ödem ise geçirgenlik artışına bağlı protein ve hücreden zengin 'eksüda'dır."
            )
        ]
    })

    # Slide 14
    slides.append({
        "slideNumber": 14,
        "title": "Dolor (Ağrı): Nosiseptörlerin Kimyasal ve Mekanik Uyarımı",
        "subtitle": "Bradikinin, PGE2, doku asidozu ve ödemin yarattığı gerilim basıncı",
        "badge": "Ağrı Nörobiyolojisi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Dördüncü kardinal bulgu olan **Dolor (Ağrı)**, konağı hasarlı bölgeyi korumaya ve istirahate sevk eden "
            "yaşamsal bir alarm mekanizmasıdır. Ağrının ortaya çıkışı iki sinerjistik faktörle yönetilir:\n\n"
            "- **Doğrudan Kimyasal Nosiseptif Uyarım:** Kinin kaskadından üretilen **bradikinin** ve mast hücrelerinden "
            "salınan **histamin**, serbest sinir uçlarındaki (C lifleri ve A-delta lifleri) spesifik reseptörlere bağlanarak "
            "aksiyon potansiyeli başlatır.\n"
            "- **Duyarlılaşma (Hiperaljezi):** Siklooksijenaz yolağından sentezlenen **Prostaglandin E2 (PGE2)** ağrı "
            "eşik değerini düşürür; sinirleri bradikinin ve mekanik basıya aşırı duyarlı hale getirir.\n"
            "- **Mekanik Gerilim:** Eksüdanın yarattığı doku turgoru ve şişlik sinir uçlarını fiziksel olarak gerer."
        ),
        "medicalTerms": [
            {"term": "Nosiseptör", "explanation": "Doku hasarı, kimyasal mediyatörler veya mekanik gerilimle uyarılan ağrı duyusu reseptörüdür."},
            {"term": "Hiperaljezi", "explanation": "Prostaglandinler gibi mediyatörlerin etkisiyle ağrı eşiğinin düşmesi ve hafif uyaranların bile şiddetli ağrı algılatmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enflamasyonda ağrıyı doğrudan başlatan en güçlü kimyasal mediyatör BRADİKİNİN'dir.",
            "📌 [SINAV SPOTU] PGE2 doğrudan ağrı oluşturmaktan ziyade nosiseptörleri bradikinine duyarlılaştırır (hiperaljezi)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bradikinin Gücü", "desc": "Serbest sinir uçlarını doğrudan depolarize eden birincil algogen ajan.", "isKey": True},
                {"title": "PGE2 Rolü", "desc": "Ağrı eşiğini düşürerek zonklayıcı hassasiyet yaratır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Akut enflasyonda sinir uçlarını doğrudan uyararak ağrı oluşturan en güçlü plazma kaynaklı mediyatör bradikinin molekülüdür.",
                "bradikinin",
                "Kallikrein-kininojen sisteminden üretilen 9 aminoasitlik güçlü ağrı mediyatörü"
            ),
            make_micro_quiz(
                "Aspirin ve ibuprofen gibi NSAİİ (Non-steroid anti-inflamatuvar) ilaçların enflamatuvar ağrıyı dindirme mekanizması aşağıdakilerden hangisidir?",
                {
                    "A": "Bradikinin reseptörlerini irreversibl bloke etmek",
                    "B": "Siklooksijenaz (COX) enzimini inhibe ederek ağrı eşiğini düşüren PGE2 sentezini kesmek",
                    "C": "Histaminin H1 reseptörlerine bağlanmasını engellemek",
                    "D": "Nötrofillerin damardan göçünü tamamen felç etmek",
                    "E": "Endotel hücrelerini uyararak nitrik oksit salgılatmak"
                },
                "B",
                {
                    "A": "NSAİİ'lar bradikinin reseptör blokörü değildir.",
                    "B": "Doğru cevap B'dir: COX-1 ve COX-2 inhibisyonu ile PGE2 üretimi durur; nosiseptörlerin duyarlılaşması (hiperaljezi) engellenir.",
                    "C": "Bu antihistaminiklerin mekanizmasıdır.",
                    "D": "Nötrofil göçünü doğrudan felç etmezler.",
                    "E": "Nitrik oksit sentezini artırmazlar."
                }
            )
        ]
    })

    # Slide 15
    slides.append({
        "slideNumber": 15,
        "title": "Functio Laesa (Fonksiyon Kaybı): Enflamasyonun Bütünleşik Sonucu",
        "subtitle": "Ağrı inhibisyonu, mekanik deformite ve parankimal hücre yıkımının organ işlevini durdurması",
        "badge": "Virchow İlkesi",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Rudolf Virchow tarafından tanımlanan beşinci kardinal bulgu olan **Functio Laesa (Fonksiyon Kaybı)**, "
            "diğer dört bulgunun ve hücresel yıkımın kümülatif sonucudur:\n\n"
            "1. **Mekanik İmpedans:** Şiddetli eksüdasyon ve doku şişliği (tumor) organın hareket kabiliyetini sınırlar. "
            "Örneğin akut artritte eklem boşluğuna dolan sıvı eklem hareket açıklığını mekanik olarak kilitler.\n"
            "2. **Refleks Nöral İnhibisyon:** Şiddetli ağrı (dolor) koruyucu kas spazmlarına ve refleks motor inhibisyona "
            "yol açarak bireyin o ekstremiteyi kullanmasını engeller.\n"
            "3. **Parankim Hasarı:** Akut hepatitte hepatosit nekrozu sarılık ve koagülopatiye; akut pnömonide alveollerin "
            "nötrofil ve fibrinle dolması gaz değişim yetersizliğine yol açar."
        ),
        "medicalTerms": [
            {"term": "Mekanik İmpedans", "explanation": "Ödem ve şişlik nedeniyle eklem veya lümenli organlarda fiziksel hareket kısıtlılığı doğmasıdır."},
            {"term": "Koruyucu Spazm", "explanation": "Ağrılı odağı hareketsiz tutmak amacıyla çevre iskelet kaslarının istemsizce kasılı kalmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Functio laesa hem mekanik bası, hem ağrıya bağlı refleks felç, hem de parankim nekrozuyla şekillenir.",
            "📌 [SINAV SPOTU] Akut apandisitteki batın defansı (tahta karın) ağrıya karşı gelişen koruyucu spazm örneğidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mekanik Blokaj", "desc": "Ödem sıvısı dokunun esnemesini ve hareketini engeller.", "isKey": True},
                {"title": "Hücresel İflas", "desc": "Parankim hücreleri nekroza uğrayarak organ fonksiyonu çöker.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Kardinal Belirti", "Tarihsel Tanımlayıcı", "Altta Yatan Temel Fizyopatolojik Mekanizma"],
                [
                    [("Rubor (Kızarıklık)", False, ""), ("Cornelius Celsus", False, ""), ("Arteriyoler vazodilatasyon ve kapiller yatakta aktif hiperemi", True, "Oksijenli kanın mikrodolaşımda göllenmesi")],
                    [("Tumor (Şişlik)", False, ""), ("Cornelius Celsus", False, ""), ("Artmış vasküler geçirgenlik ve interstisyel eksüda birikimi", True, "Endotel aralıklarından proteinli sıvı kaçağı")],
                    [("Calor (Sıcaklık)", False, ""), ("Cornelius Celsus", False, ""), ("Genişleyen damarlarla 37°C santral kor kanının taşınması", True, "Lokal perfüzyon artışının termal yansıması")],
                    [("Dolor (Ağrı)", False, ""), ("Cornelius Celsus", False, ""), ("Bradikinin ve mekanik basıncın nosiseptörleri uyarması (PGE2)", True, "Sinir uçlarının kimyasal ve fiziksel uyarımı")],
                    [("Functio Laesa (Kayıp)", False, ""), ("Rudolf Virchow", False, ""), ("Ödem, ağrı spazmı ve parankimal hücre yıkımının bileşkesi", True, "Organın fizyolojik görevini yürütememesi")]
                ]
            ),
            make_active_recall(
                "Akut pnömoni geçiren bir hastada nefes darlığı ve hipoksemi gelişmesi beş kardinal belirtiden hangisinin doğrudan karşılığıdır?",
                "Functio laesa (fonksiyon kaybı); çünkü alveollerin eksüdayla dolması akciğerin primer görevi olan gaz değişim fonksiyonunu bozar."
            )
        ]
    })

    # Slide 16
    slides.append({
        "slideNumber": 16,
        "title": "Enflamatuvar Yanıtın Beş Aşaması: '5R' Kuralı",
        "subtitle": "Recognition, Recruitment, Removal, Regulation ve Resolution/Repair orkestrasyonu",
        "badge": "Yanıt Dinamiği",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Modern immünopatolojide enflamatuvar kaskad mantıksal ve kronolojik olarak İngilizce baş harfleriyle "
            "**'5R' prensibi** çerçevesinde incelenir:\n\n"
            "1. **Recognition (Tanıma):** Doku yerleşik sentinellerinin zararlı ajanı reseptörleriyle saptaması.\n"
            "2. **Recruitment (Lökosit ve Protein Alımı):** Dolaşımdaki savunma güçlerinin damardan hasar alanına çağrılması.\n"
            "3. **Removal (Etkenin Yok Edilmesi):** Lökositlerin patojeni fagositoz ve intrasellüler sindirimle imha etmesi.\n"
            "4. **Regulation (Düzenleme / Frenleme):** Görevi biten yanıtın anti-enflamatuvar mekanizmalarla durdurulması.\n"
            "5. **Resolution / Repair (Rezolüsyon ve Onarım):** Dokunun temizlenip rejenerasyon veya skar ile tamir edilmesi."
        ),
        "medicalTerms": [
            {"term": "5R Kuralı", "explanation": "Enflamasyonun tanıma, çağırma, yok etme, sonlandırma ve onarım basamaklarını özetleyen evrensel patoloji şablonudur."},
            {"term": "Recruitment", "explanation": "Lökositlerin kandan çekilerek hasarlı dokuya adhezyon ve kemotaksiyle toplanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enflamasyonun 5R adımları: Recognition -> Recruitment -> Removal -> Regulation -> Repair.",
            "📌 [SINAV SPOTU] Regulation basamağının aksaması kontrolsüz kronik doku tahribatına yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sıralı Algoritma", "desc": "Tanı -> Çağır -> Yok Et -> Frenle -> Onar.", "isKey": True},
                {"title": "Denge", "desc": "Her aşama bir sonraki fazın başlaması için biyolojik sinyal üretir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "5R Aşamalarının Kronolojik İlerleyişi",
                [
                    "1. Recognition: Makrofajlar ve mast hücreleri bakteri duvarındaki PAMPs yapılarını algılar",
                    "2. Recruitment: Salınan sitokin ve kemokinler nötrofilleri hasarlı dokuya mobilize eder",
                    "3. Removal: Nötrofiller ve monositler bakterileri fagosite edip litik enzimlerle yok eder",
                    "4. Regulation: Kısa ömürlü nötrofiller apoptoza gider ve lipoksinler yangıyı durdurur",
                    "5. Repair: M2 makrofajlar büyüme faktörleri salgılayarak fibroblastları ve anjiyogenezi uyarır"
                ]
            ),
            make_cloze(
                "Enflamatuvar yanıtın 5R adımları içinde lökosit ve plazma proteinlerinin kandan dokuya çağrılmasını ifade eden terim recruitment terimidir.",
                "recruitment",
                "İngilizce askere alma veya hücreleri göreve çağırma anlamına gelen terim"
            )
        ]
    })

    # Slide 17
    slides.append({
        "slideNumber": 17,
        "title": "Adım 1 ve 2: Recognition (Tanıma) ve Recruitment (Çağırma)",
        "subtitle": "Sentinel hücre reseptörleri alarm verir; selektinler ve integrinler lökositleri damardan çeker",
        "badge": "Erken Faz",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Enflamasyonun başarısı ilk iki adımın kusursuz senkronizasyonuna bağlıdır:\n\n"
            "- **Recognition (Tanıma):** Doku makrofajları, dendritik hücreler ve mast hücreleri yüzeylerinde ve "
            "endozomlarında **Örüntü Tanıma Reseptörleri (PRR)** taşır. Bakteri endotoksinini (LPS) sezen TLR4 veya "
            "ürat kristallerini sezen NLRP3 inflamazomu saniyeler içinde aktive olur. Alarm sitokinleri (TNF, IL-1) salgılanır.\n\n"
            "- **Recruitment (Hücre Alımı):** Bu sitokinler komşu postkapiller venül endotelini uyarır. "
            "Endotelde selektinler (E-selektin, P-selektin) ve integrin ligandları (ICAM-1, VCAM-1) eksprese edilir. "
            "Dolaşımdaki nötrofiller damar duvarına tutunur ve kemokin gradyanını izleyerek dokuya akar."
        ),
        "medicalTerms": [
            {"term": "PRR (Pattern Recognition Receptors)", "explanation": "Mikropların korunmuş yapılarını veya hasarlı hücre artıklarını tanıyan konak reseptörleridir."},
            {"term": "Kemokin Gradyanı", "explanation": "Hasar odağında en yüksek, damar çevresinde daha düşük olan ve lökositlere yön gösteren kimyasal konsantrasyon eğrisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Recognition basamağında başrol doku makrofajı ve mast hücrelerindeki TLR ve inflamazomundur.",
            "📌 [SINAV SPOTU] Recruitment basamağı endotel adezyon molekülleri ve kemokinler aracılığıyla yürütülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Alarm Zilleri", "desc": "Sentineller mikrop varlığını sezip sitokin püskürtür.", "isKey": True},
                {"title": "Göç Koridoru", "desc": "Endotel adezyon molekülleriyle nötrofillere kapıyı açar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Recognition Öncesi vs Recruitment Sonrası Doku",
                "Recognition Öncesi Doku",
                "Damarlar sakin, lökositler lümenin ortasında hızla akmakta, dokuda sadece az sayıda sentinel hücre beklemektedir.",
                "Recruitment Sonrası Doku",
                "Damarlar genişlemiş, endotel selektinlerle kaplanmış, binlerce nötrofil perivasküler alana hücum etmiştir."
            ),
            make_active_recall(
                "Enflamasyonun 'Recognition' aşamasında dokudaki sentinel makrofajlar mikropları hangi reseptör aileleri aracılığıyla tanır?",
                "Toll-like reseptörler (TLR), NOD-like reseptörler (NLR / İnflamazom), C-tipi lektin reseptörleri (CLR) ve RIG-I benzeri reseptörler (RLR) aracılığıyla tanır."
            )
        ]
    })

    # Slide 18
    slides.append({
        "slideNumber": 18,
        "title": "Adım 3, 4 ve 5: Removal, Regulation ve Repair",
        "subtitle": "Fagositoz ile temizlik, yangıyı sonlandıran frenler ve fibroblastik onarım",
        "badge": "Geç Faz ve Rezolüsyon",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Enflamasyonun ikinci yarısı temizlik, güvenlik ve yeniden inşa aşamalarını kapsar:\n\n"
            "- **Removal (Temizleme):** Nötrofil ve makrofajlar opsonize edilmiş mikropları fagozom içine alır. "
            "Lizozom ile birleşen fagozomda NADPH oksidaz kaynaklı süperoksit ve miyeloperoksidaz (MPO) mikropları yok eder.\n\n"
            "- **Regulation (Sonlandırma):** Nötrofillerin ömrü kısadır (1-2 gün) ve hızla apoptoza giderler. Arakidonik asit "
            "yolağı pro-enflamatuvar lökotrienlerden anti-enflamatuvar **lipoksin, rezolvin ve protektinlere** kayar. "
            "Makrofajlar IL-10 ve TGF-β salgılayarak yangıyı frenler.\n\n"
            "- **Repair (Onarım):** M2 (alternatif aktive) makrofajlar VEGF, FGF ve PDGF salarak yeni damarlar (anjiyogenez) "
            "ve granülasyon dokusu oluşturur."
        ),
        "medicalTerms": [
            {"term": "Lipoksinler", "explanation": "Arakidonik asitten sentezlenen ve nötrofil alımını durduran yangı sonlandırıcı lipid mediyatörlerdir."},
            {"term": "M2 Makrofaj", "explanation": "İnflamasyonu baskılayıp büyüme faktörleri salgılayarak doku onarımını ve fibrozisi yöneten alternatif makrofaj fenotipidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enflamasyonu sonlandıran anahtarlar: Nötrofil apoptozu, lipoksinler/rezolvinler ve IL-10/TGF-beta'dır.",
            "📌 [SINAV SPOTU] Doku onarımını ve granülasyon dokusu oluşumunu M2 makrofajlar yönetir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Removal", "desc": "Fago-lizozomal sindirimle mikrobiyal temizlik.", "isKey": True},
                {"title": "Regulation & Repair", "desc": "Lipoksinlerle yangıyı durdurup M2 makrofajla tamir etme.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut enflamasyon odağında mikroplar başarıyla temizlendikten sonra ortamın kronikleşmeden tam bir doku onarımına (rezolüsyona) geçmesi için hangi moleküler dönüşüm zorunludur?",
                [
                    {"text": "Arakidonik asit metabolizmasının lökotrienlerden lipoksin ve rezolvinlere kayması, nötrofil apoptozu ve M2 makrofajların devreye girmesi", "isCorrect": True, "feedback": "Harika tıp muhakemesi! Rezolüsyon pasif bir olay değil, lipoksinler ve M2 fenotipiyle yürütülen aktif bir programdır."},
                    {"text": "Daha fazla nötrofil çağrılarak ortama yüksek dozda elastaz ve hidroksil radikali pompalanması", "isCorrect": False, "feedback": "Bu durum doku nekrozunu ve kronikleşmeyi artırır."},
                    {"text": "Endotel hücrelerinin apoptoza giderek tüm mikrodolaşımın tromboze olması", "isCorrect": False, "feedback": "Tromboz infarkta ve iskemik nekroza yol açar, onarımı engeller."}
                ]
            ),
            make_cloze(
                "Akut enflamasyonun sonlanma fazında nötrofil göçünü durdurarak rezolüsyonu başlatan koruyucu lipid mediyatörlere lipoksinler adı verilir.",
                "lipoksinler",
                "Arakidonik asit 12-lipoksijenaz ve 15-lipoksijenaz yolağından üretilen anti-enflamatuvar moleküller"
            )
        ]
    })

    # Slide 19 (CHECKPOINT 2)
    slides.append({
        "slideNumber": 19,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Kardinal Belirtiler ve 5R Orkestrasyonu",
        "subtitle": "Bölüm 2 Celsus-Virchow Beşlisi, Nosiseptörler, Eksüda ve Enflamasyonun 5 Evresi",
        "badge": "Checkpoint 2",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "İkinci kontrol noktasında klinik bulgular ile hücresel evreleri tam entegre ediyoruz:\n\n"
            "1. **Beş Kardinal Belirti:**\n"
            "   - **Rubor ve Calor:** Arteriyoler vazodilatasyon ve aktif hiperemi.\n"
            "   - **Tumor:** Artmış vasküler geçirgenlik ve interstisyel eksüda.\n"
            "   - **Dolor:** Bradikinin uyarımı ve PGE2 hiperaljezisi.\n"
            "   - **Functio Laesa:** Mekanik ödem, ağrı refleksi ve doku nekrozu.\n"
            "2. **5R Dinamiği:**\n"
            "   - **Recognition:** TLR ve inflamazom ile PAMP/DAMP algılanması.\n"
            "   - **Recruitment:** Selektin, integrin ve kemokinlerle nötrofil göçü.\n"
            "   - **Removal:** Fagositoz, NADPH oksidaz ve lizozomal enzimlerle öldürme.\n"
            "   - **Regulation:** Nötrofil apoptozu, lipoksinler, rezolvinler, IL-10.\n"
            "   - **Repair:** M2 makrofajlar, anjiyogenez ve fibroblastik skarlaşma."
        ),
        "medicalTerms": [
            {"term": "Rezolvin", "explanation": "Omega-3 yağ asitlerinden (EPA ve DHA) sentezlenen ve enflamasyonu aktif olarak söndüren mediyatörlerdir."},
            {"term": "Fibrin Eksüdası", "explanation": "Geçirgenliği aşırı artmış damarlardan sızan fibrinojenin polimerize olmasıyla dokuda biriken ağsı pıhtı tabakasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Celsus 4'lüsü: Rubor, Tumor, Calor, Dolor; Virchow 5'lisi: Functio Laesa.",
            "📌 [SINAV SPOTU] Enflamasyonun 5R'si: Recognition, Recruitment, Removal, Regulation, Repair."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kardinal Özet", "desc": "Vazodilatasyon (Rubor/Calor), Sızıntı (Tumor), Bradikinin (Dolor), Kayıp (Functio).", "isKey": True},
                {"title": "5R Özet", "desc": "Tanı -> Çağır -> Yok Et -> Düzenle -> Onar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Akut enflamasyonda ortaya çıkan 'Tumor' (şişlik) bulgusu ile konjestif kalp yetmezliğinde bacaklarda oluşan gode bırakan ödem arasındaki temel patolojik mekanizma farkı nedir?",
                "Akut enflasyondaki şişlik mikrovasküler endotel geçirgenliğinin artması sonucu yüksek proteinli 'eksüda' birikimidir; kalp yetmezliğindeki ödem ise damar geçirgenliği normal iken venöz hidrostatik basıncın artması sonucu proteinden fakir 'transüda' birikimidir."
            ),
            make_micro_quiz(
                "Aşağıdaki mediyatör çiftlerinden hangisi akut enflamasyonda sinir uçlarını doğrudan uyararak veya duyarlılaştırarak 'Dolor' (ağrı) kardinal bulgusunu meydana getirir?",
                {
                    "A": "Bradikinin ve Prostaglandin E2 (PGE2)",
                    "B": "Histamin ve Heparin",
                    "C": "Nitrik Oksit ve İnterlökin-10",
                    "D": "Lipoksin A4 ve Rezolvin E1",
                    "E": "Tromboksan A2 ve Lökotrien B4"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Bradikinin nosiseptörleri doğrudan depolarize ederken, PGE2 ağrı eşiğini düşürerek hiperaljezi yaratır.",
                    "B": "Histamin kaşıntı ve ödem yapar.",
                    "C": "IL-10 anti-enflamatuvardır.",
                    "D": "Lipoksin ve rezolvin yangıyı söndürür.",
                    "E": "Tromboksan vazokonstriktördür."
                }
            ),
            make_cloze(
                "Celsus'un dört klasik belirtisine yaklaşık 1800 yıl sonra fonksiyon kaybı (functio laesa) kavramını ekleyen hekim Rudolf Virchow olmuştur.",
                "Rudolf Virchow",
                "Modern hücresel patolojinin babası olan 19. yüzyıl Alman hekimi"
            )
        ]
    })

    # Slide 20
    slides.append({
        "slideNumber": 20,
        "title": "Bölüm 2 Entegrasyonu: Akut Apandisitte 5 Kardinal Belirti",
        "subtitle": "Klinik patoloji viziti: Lümen obstrüksiyonundan cerrahi masasına uzanan enflamasyon tablosu",
        "badge": "Klinik Uygulama",
        "badgeColor": "rose",
        "synthesisNarrative": (
            "Kardinal belirtiler ve 5R döngüsünü somutlaştırmak için klasik bir klinik model: **Akut Apandisit**.\n\n"
            "1. **Tetikleyici ve Recognition:** Fekalit apandiks lümenini tıkar; mukozada iskemi ve bakteriyel proliferasyon "
            "başlar. Doku makrofajları bakteriyel PAMPs moleküllerini tanır.\n"
            "2. **Rubor ve Calor:** Seröz damarlarda masif vazodilatasyon gelişir; ameliyatta apandiks hiperemik ve kıpkırmızıdır.\n"
            "3. **Tumor:** Venüler geçirgenlik artışıyla duvar kalınlaşır, lümen pürülan eksüdayla şişer.\n"
            "4. **Dolor:** Bradikinin ve serozal gerilim periton nosiseptörlerini uyarır; sağ alt kadranda şiddetli ağrı başlar.\n"
            "5. **Functio Laesa:** Bağırsak peristaltizmi durur (lokal paralitik ileus) ve karın kasları tahta gibi sertleşir."
        ),
        "medicalTerms": [
            {"term": "Fekalit", "explanation": "Apandiks lümenini tıkayarak mukozal iskemi ve bakteriyel apandisiti başlatan taşlaşmış feçes parçasıdır."},
            {"term": "Paralitik İleus", "explanation": "Enflamasyona bağlı olarak bağırsak düz kaslarının motilitesinin durması ve lümen içeriğinin ilerleyememesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut apandisitte McBurney hassasiyeti ve defans somatik peritonun kimyasal ve mekanik uyarımını yansıtır.",
            "📌 [SINAV SPOTU] Apandiks duvarında nötrofil infiltrasyonu patolojik kesin akut apandisit tanısı için şarttır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lokalizasyon", "desc": "Fekalit tıkanması bakteriyel çoğalmayı ve alarmı başlatır.", "isKey": True},
                {"title": "Klinik Yansıma", "desc": "Rubor, tumor, calor, dolor ve ileus ile functio laesa eşlik eder.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Akut apandisitin histopatolojik kesin tanısı için apandiksin muskularis propria tabakasında nötrofil infiltrasyonu görülmesi şarttır.",
                "nötrofil",
                "Akut enflamasyonun duvar katmanlarını istila eden karakteristik hücre tipi"
            ),
            make_active_recall(
                "Akut apandisitte cerrah batını açtığında apandiksin normal parlak açık pembe rengini kaybedip donuk, şiş ve kıpkırmızı (rubor) görünmesinin mikroskobik nedeni nedir?",
                "Serozal ve muskuler tabakalardaki mikrovasküler prekapiller arteriyollerin vazodilatasyona uğraması, kapiller yatakların aktif hiperemi ile aşırı kanla dolması ve damar dışına fibrinli eksüda sızmasıdır."
            )
        ]
    })

    return slides
