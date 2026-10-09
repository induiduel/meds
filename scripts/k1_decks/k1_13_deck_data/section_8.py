# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-13-s71",
        "title": "Kronik Enflamasyonun Sistemik Etkileri: Kaşeksi ve Anoreksi",
        "content": "Aylarca süren kronik enflamasyonda sitokinler yalnızca lokal dokuda kalmaz, kana sızarak hastanın tüm metabolizmasını tüketir:\n\n- **Kaşeksi (Cytokine Cachexia):** İleri derecede zayıflama, derin kas erimesi, yağ dokusu kaybı ve halsizlik tablosudur.\n- **Kilit Sitokin TNF-α (Kaşektin):** Eskiden 'kaşektin' olarak adlandırılan TNF-α, hipotalamusta iştah merkezini baskılayarak anoreksi (iştahsızlık) yapar. Aynı zamanda adipositlerde **lipoprotein lipaz (LPL)** enzimini inhibe ederek serbest yağ asitlerinin yağ dokusuna girişini engeller ve kaslarda proteolizi tetikler.\n- **Diğer Sitokinler:** IL-1 ve IL-6 metabolik hızı artırır; protein yıkımını hızlandırarak hastayı 'tükenme' sendromuna sokar (tüberküloz ve ileri evre kanserlerdeki kaşeksi).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Basit Açlık vs Sitokin Aracılı Kaşeksi",
                "Basit Açlık (Kalori Kısıtlaması)",
                "Metabolik hız düşer, öncelikle yağ depoları yakılır; kas dokusu olabildiğince korunur.",
                "Sitokin Aracılı Kaşeksi (TNF-alfa)",
                "Metabolik hız artar; lipoprotein lipaz inhibe olur; kas proteolizi ve derin erime durdurulamaz."
            ),
            make_cloze(
                "Kronik enflamasyon ve kanserde derin kilo kaybı ve kas erimesine yol açan kaşeksin olarak da bilinen temel sitokin TNF-alfa molekülüdür.",
                "TNF-alfa",
                "Kaşeksiye yol açan majör makrofaj sitokini"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-13-s72",
        "title": "Kronik Hastalık Anemisi: Hepsidinin Demiri Kilitlemesi",
        "content": "Kronik enflamasyonu olan hastalarda (romatoid artrit, tüberküloz, osteomiyelit) vücutta bol demir depolandığı halde eritrosit sentezlenemez. Bu tabloya **Kronik Hastalık Anemisi (İnflamatuar Anemi)** denir:\n\n- **Moleküler Mekanizma (Sınav Spotu):**\n  1. Kronik yangıda salınan **İnterlökin-6 (IL-6)**, karaciğer hepatositlerinden **Hepsidin** hormonunun aşırı sentezlenmesini tetikler.\n  2. Hepsidin, enterositlerin ve makrofajların demir çıkış kapısı olan **Ferroportin** kanalına bağlanarak onu hücre içine çeker ve yıkar.\n  3. Sonuç: Diyetle alınan demir emilemez; makrofajlar fagositozla elde ettikleri demiri dışarı salamaz. Demir retiküloendotelyal depolarda hapsolur; eritroid öncüllere demir verilemez.\n- **Laboratuvar:** Serum demiri düşük, ferritin (depo) NORMAL veya YÜKSEK, transferrin satürasyonu düşüktür.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hepsidin Aracılı Kronik Hastalık Anemisi Zinciri",
                [
                    "1. IL-6 Patlaması: Kronik mononükleer yangı alanından salınan IL-6 karaciğer hepatositlerini uyarır.",
                    "2. Hepsidin Sentezi: Karaciğer bol miktarda hepsidin hormonunu kana pompalar.",
                    "3. Ferroportin Yıkımı: Hepsidin ferroportin kanallarını bağlayıp yıkar; demir kapıları kilitlenir.",
                    "4. Demir Hapsi ve Anemi: Demir makrofaj fagozomunda hapsolur; eritropoez demirsiz kalarak anemi gelişir."
                ]
            ),
            make_quiz(
                "Kronik enflamasyonda IL-6 etkisiyle karaciğerden sentezlenen ve ferroportin kanallarını yıkarak demiri makrofajlarda hapseden hormon hangisidir?",
                [
                    {"key": "A", "text": "Hepsidin", "explanation": "A seçeneği DOĞRUDUR: Hepsidin demir emilimini ve salınımını ferroportini yıkarak durduran ana hormondur."},
                    {"key": "B", "text": "Ferritin", "explanation": "B seçeneği yanlıştır: Demir depolayan proteindir."},
                    {"key": "C", "text": "Transferrin", "explanation": "C seçeneği yanlıştır: Kanda demir taşıyan proteindir."},
                    {"key": "D", "text": "Eritropoietin", "explanation": "D seçeneği yanlıştır: Kemik iliğinde eritrosit uyarımı yapan böbrek hormonudur."},
                    {"key": "E", "text": "Haptoglobin", "explanation": "E seçeneği yanlıştır: Serbest hemoglobini bağlayan proteindir."}
                ],
                "A"
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-13-s73",
        "title": "Sekonder Reaktif Amiloidoz (AA Amiloidoz)",
        "content": "Uzun yıllar tedavi edilmemiş kronik enflamatuar hastalıklarda en korkulan sistemik komplikasyon dokularda amiloid birikimidir:\n\n- **Serum Amiloid A (SAA):** Kronik enflamasyonda IL-1, TNF ve IL-6 etkisiyle hepatositlerce sürekli sentezlenen bir akut faz reaktanıdır.\n- **Fibril Dönüşümü:** Yıllarca yüksek kalan SAA molekülleri mononükleer fagositlerce tam parçalanamaz; beta-kırmalı (β-pleated sheet) tabakalara katlanarak **Amiloid A (AA) fibrillerine** dönüşür.\n- **Organ Tutulumu (Sınav Spotu):** AA amiloidoz en çok **böbrekleri (glomerülleri)** tutar; masif proteinüri, nefrotik sendrom ve üremiye yol açar. Karaciğer ve dalakta da birikir.\n- **Tanı:** Dokuda **Kongo kırmızısı (Congo red)** boyası ile boyanır; polarize ışık mikroskobunda karakteristik **elma yeşili çift kırıcılık (apple-green birefringence)** verir!",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Amiloid Tipi", "Öncül Serum Proteini", "En Sık Klinik Neden"],
                [
                    [
                        {"text": "Sekonder Amiloidoz (AA)", "isMasked": False, "hint": ""},
                        {"text": "Serum Amiloid A (SAA)", "isMasked": True, "hint": "Karaciğer akut faz proteini"},
                        {"text": "Romatoid Artrit, Bronşektazi, Kronik Osteomiyelit, FMF", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Primer Amiloidoz (AL)", "isMasked": True, "hint": "İmmünglobulin hafif zincir amiloidi"},
                        {"text": "İmmünglobulin hafif zincirleri (kappa/lambda)", "isMasked": False, "hint": ""},
                        {"text": "Multipl Myelom ve Plazma Hücre Diskrazileri", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kongo Kırmızısı Boyama", "isMasked": False, "hint": ""},
                        {"text": "Beta-kırmalı tabakalara bağlanma", "isMasked": False, "hint": ""},
                        {"text": "Polarize ışıkta elma yeşili çift kırıcılık", "isMasked": True, "hint": "Amiloidin optik polarizasyon rengi"}
                    ]
                ]
            ),
            make_recall(
                "Kronik osteomiyelit veya romatoid artrit zemininde gelişen sekonder AA amiloidoz doku kesitinde Kongo kırmızısı ile boyandığında polarize ışıkta hangi renkte parlar?",
                "Elma yeşili renkte çift kırıcılık verir (apple-green birefringence).",
                "Kongo kırmızısının polarize ışıktaki tanısal yeşil rengi"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-13-s74",
        "title": "Doku Yıkımının Kaçınılmaz Sonu: Organ Fibrozisi",
        "content": "Akut enflamasyonda parankim çatı (ekstraselüler matriks) sağlamsa doku rejenerasyonla orijinal haline döner. Kronik enflamasyonda ise doku çatısı çökmüştür:\n\n- **Parankim İflası:** Sürekli makrofaj ve T-hücre saldırısı parankim hücrelerinin kök hücre rezervini tüketir ve apoptoz/nekroz ile yok eder.\n- **Yara İzi ile Yama:** Vücut kaybedilen parankim hücrelerinin yerini dolduramaz; tek çare defekti fibröz bağ dokusu ile doldurup yamamaktır (**fibrozis / skarlaşma**).\n- **Fonksiyonel Çöküş:** Kollajen birikimi yapısal dayanıklılık sağlar ancak hiçbir fonksiyonel görevi (sekresyon, filtrasyon, gaz değişimi) yerine getiremez. Akciğer sertleşir, karaciğer kanı geçiremez, böbrek idrar süzemez.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Tam Rejenerasyon vs Fibröz Skarlaşma",
                "Tam Rejenerasyon (Hafif Hasar)",
                "Matriks çatısı sağlamdır; parankim hücreleri bölünerek orijinal anatomik yapıyı geri kurar.",
                "Fibröz Skarlaşma (Kronik Enflamasyon)",
                "Çatı çökmüştür; parankim yerine yoğun kollajen dolar; organ sertleşir ve fonksiyonunu kaybeder."
            ),
            make_cloze(
                "Kronik enflamasyonda hasara uğrayan fonksiyonel parankim hücrelerinin yerini fibröz bağ dokusunun alması sürecine skarlaşma adı verilir.",
                "skarlaşma",
                "Yara izi ve bağ dokusu yaması terimi"
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-13-s75",
        "title": "Dönüştürücü Büyüme Faktörü-Beta (TGF-β): Fibrogenezisin Efendisi",
        "content": "Tıbbi patolojide fibrogenezisin, kollajen birikiminin ve skar oluşumunun en güçlü moleküler yöneticisi **TGF-β (Transforming Growth Factor-β)**'dır:\n\n- **Hücresel Kaynaklar:** Dokuda esas olarak alternatif aktive olmuş **M2 makrofajlar**, trombositler, regülatuvar T hücreleri ve endotel tarafından salınır.\n- **Kollajen Fabrikası:**\n  1. Fibroblastların kemotaksisini ve mitozunu şiddetle uyarır.\n  2. Fibroblastları **alfa-SMA pozitif miyofibroblastlara** dönüştürür.\n  3. **Tip I ve Tip III kollajen**, fibronektin ve proteoglikan genlerinin transkripsiyonunu (Smad yolağı üzerinden) doğrudan tetikler.\n  4. Matriks Metalloproteinazları (MMP) inhibe eden **TIMP** (doku metalloproteinaz inhibitörleri) sentezini artırarak üretilen kollajenin yıkılmasını engeller!",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "TGF-β Aracılı Ekstraselüler Matriks Birikim Zinciri",
                [
                    "1. M2 Makrofaj Salgısı: Hasarlı dokuda M2 makrofajları yoğun latent TGF-beta salgılar.",
                    "2. Smad Sinyal İletimi: TGF-beta fibroblast yüzey reseptörüne bağlanarak Smad2/3 yolunu aktive eder.",
                    "3. Kollajen Transkripsiyonu: Fibroblast çekirdeğinde Tip I kollajen ve fibronektin üretimi fırlar.",
                    "4. Yıkım Blokajı (TIMP): TIMP molekülleri MMP enzimlerini felç eder; kollajen erimez ve kalıcı fibrozis oturur."
                ]
            ),
            make_quiz(
                "Kronik enflamasyonda hem fibroblastları uyararak kollajen sentezleten hem de metalloproteinazları baskılayarak kollajen yıkımını engelleyen en güçlü profibrotik sitokin hangisidir?",
                [
                    {"key": "A", "text": "Dönüştürücü Büyüme Faktörü-Beta (TGF-β)", "explanation": "A seçeneği DOĞRUDUR: TGF-beta kollajen üretimini artırıp yıkımını engelleyen baş fibrogenik faktördür."},
                    {"key": "B", "text": "Tümör Nekroz Faktörü (TNF)", "explanation": "B seçeneği yanlıştır: Yıkıcı ve pro-enflamatuar sitokindir."},
                    {"key": "C", "text": "İnterlökin-8", "explanation": "C seçeneği yanlıştır: Nötrofil kemokinidir."},
                    {"key": "D", "text": "İnterferon-alfa", "explanation": "D seçeneği yanlıştır: Antiviral sitokindir."},
                    {"key": "E", "text": "Bradikinin", "explanation": "E seçeneği yanlıştır: Ağrı ve permeabilite peptididir."}
                ],
                "A"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-13-s76",
        "title": "Organ Düzeyinde Kronik Fibrozis Modelleri",
        "content": "Kronik enflamasyonun tetiklediği aşırı fibrogenezis vücudun hayati organlarını taş gibi sertleştirerek iflasa sürükler:\n\n1. **Karaciğer Sirozu:** Kronik hepatit B/C veya alkolizmde aralıksız enflamasyon; karaciğer Ito (yıldızsı) hücreleri miyofibroblasta dönüşür; portal-santral köprüleşme fibrozisi ve rejenerasyon nodülleriyle parankim mimarisi tamamen bozulur.\n2. **İdiyopatik Pulmoner Fibrozis (IPF):** Alveol epitelinin tekrarlayan mikroyaralanmaları ve anormal M2 onarımı; bal peteği akciğer (honeycombing) ve solunum yetmezliği.\n3. **Kronik Böbrek Hastalığı (Son Dönem Böbrek):** Glomerüloskleroz ve tübülointerstisyel fibrozis; nefronların yerini kollajenin almasıyla böbrek büzüşür (atrofik granüler böbrek).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sağlıklı Karaciğer Parankimi vs Sirotik Karaciğer",
                "Normal Karaciğer",
                "Düzenli hepatosit kordonları, açık sinüzoidler ve minimal bağ dokusu içerir.",
                "Sirotik Karaciğer (Kronik Enflamasyon)",
                "Fibröz septalarla çevrili rejenerasyon nodülleri; portal hipertansiyon ve karaciğer yetmezliği."
            ),
            make_cloze(
                "Karaciğerde kronik enflamasyon zemininde kollajen sentezleyerek siroza gidişi başlatan hücreler perisinüzoidal Ito hücreleridir.",
                "Ito hücreleridir",
                "A vitamini depolayan karaciğer yıldızsı hücresi"
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-13-s77",
        "title": "Kronik Enflamasyon ve Karsinojenez Kesişimi",
        "content": "Rudolf Virchow 1863 yılında kanserlerin kronik enflamasyon odaklarından kaynaklandığını öne sürmüştür. Günümüz moleküler tıbbı bu hipotezi doğrulamıştır:\n\n- **Sürekli Rejenerasyon ve Replikatif Stres:** Doku yıkıldıkça kök hücreler aralıksız bölünmeye zorlanır. Her DNA replikasyonu spontan mutasyon riskini katlar.\n- **Oksidatif DNA Hasarı:** Makrofajların ürettiği serbest oksijen radikalleri (ROS) ve reaktif nitrojen türleri (RNS) doğrudan DNA çift zincir kırıklarına ve nokta mutasyonlara (8-okso-guanin) yol açar.\n- **Apoptozun Engellenmesi:** Enflamatuar transkripsiyon faktörü **NF-κB** ve **STAT3**, anti-apoptotik genleri (Bcl-2, Bcl-xL) uyararak hasarlı hücrelerin intihar etmesini önler.\n- **Anjiyogenez Desteği:** Kronik yangıdaki VEGF ve sitokinler tümör damarlanmasına hazır bir yatak sağlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kronik Enflamasyondan Malign Transformasyona Moleküler Adımlar",
                [
                    "1. Sürekli Sitokin Uyarısı: Makrofajlardan salınan TNF ve IL-6 epiteli sürekli bölünmeye zorlar.",
                    "2. Oksidatif Mutajenez: ROS ve RNS nükleer DNA'yı bombalayarak onkogen/tümör baskılayıcı mutasyonlar yapar.",
                    "3. NF-κB ve Sağkalım: Apoptoz mekanizmaları felç edilir; hasarlı mutant hücreler hayatta kalır.",
                    "4. İnvazyon ve Tümör: Anjiyogenez ve makrofaj MMP'leri mutant klonun invaziv kansere dönüşmesini sağlar."
                ]
            ),
            make_recall(
                "Kronik enflamasyonda hücrelerin apoptoza gitmesini engelleyerek kanserleşmeyi kolaylaştıran temel pro-enflamatuar transkripsiyon faktörü hangisidir?",
                "NF-κB'dir (Nükleer Faktör Kappa B).",
                "İltihap ve hücre sağkalımının ana transkripsiyon faktörü"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-13-s78",
        "title": "Kronik Enflamasyon Zemininde Gelişen Kanser Örnekleri",
        "content": "Klinik pratikte birçok malign neoplazi iyi tanımlanmış kronik enflamatuar süreçlerin zemininde yeşerir:\n\n1. **Helicobacter pylori Gastriti:** Yıllarca süren kronik atrofik gastrit ve intestinal metaplazi zemininde **Gastrik Adenokarsinom** ve **MALT Lenfoma**.\n2. **Ülseratif Kolit:** 8-10 yıldan uzun süren pankolit hastalarında displazi zemininde **Kolorektal Kanser** riski 20-30 kat artar.\n3. **Kronik Viral Hepatit (HBV ve HCV):** Siroz zemininde sürekli hepatosit rejenerasyonu ve **Hepatosellüler Karsinom (HCC)**.\n4. **Kronik Osteomiyelit Fistül Traktı:** Drenaj fistülünün deri ağzında gelişen **Skuamöz Hücreli Karsinom (Marjolin Ülseri)**.\n5. **Schistosoma haematobium:** Mesane duvarında kronik granülomatöz sistit zemininde **Skuamöz Hücreli Mesane Kanseri**.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kronik Enflamatuar Durum", "Altta Yatan Etken / Hastalık", "Gelişen Malign Neoplazi"],
                [
                    [
                        {"text": "Kronik Atrofik Gastrit", "isMasked": False, "hint": ""},
                        {"text": "Helicobacter pylori enfeksiyonu", "isMasked": False, "hint": ""},
                        {"text": "Mide Adenokarsinomu ve MALT Lenfoma", "isMasked": True, "hint": "Kronik gastrit zemininde çıkan mide kanseri"}
                    ],
                    [
                        {"text": "Kronik Osteomiyelit Fistülü", "isMasked": True, "hint": "Kemik iltihabının cilde açılan kanalı"},
                        {"text": "Persistan bakteriyel kemik enfeksiyonu", "isMasked": False, "hint": ""},
                        {"text": "Skuamöz Hücreli Karsinom (Marjolin Ülseri)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kronik Ülseratif Kolit", "isMasked": False, "hint": ""},
                        {"text": "İnflamatuar Bağırsak Hastalığı", "isMasked": False, "hint": ""},
                        {"text": "Kolorektal Adenokarsinom", "isMasked": True, "hint": "Kolonda gelişen malign epitel tümörü"}
                    ]
                ]
            ),
            make_quiz(
                "Yıllardır drene olan kronik osteomiyelit fistül traktının deri ağzında veya eski yanık skarı zemininde gelişen skuamöz hücreli karsinoma ne ad verilir?",
                [
                    {"key": "A", "text": "Marjolin ülseri", "explanation": "A seçeneği DOĞRUDUR: Kronik fistül veya skar zemininde gelişen skuamöz karsinom Marjolin ülseridir."},
                    {"key": "B", "text": "Ghon kompleksi", "explanation": "B seçeneği yanlıştır: Tüberküloz lezyonudur."},
                    {"key": "C", "text": "Krukenberg tümörü", "explanation": "C seçeneği yanlıştır: Mide kanserinin overe metastazıdır."},
                    {"key": "D", "text": "Brenner tümörü", "explanation": "D seçeneği yanlıştır: Overin transizyonel epitel tümörüdür."},
                    {"key": "E", "text": "Wilms tümörü", "explanation": "E seçeneği yanlıştır: Çocukluk çağı böbrek nefroblastomudur."}
                ],
                "A"
            )
        ]
    })

    # Slide 79
    slides.append({
        "id": "k1-13-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Sistemik Etkiler, Amiloidoz, Fibrogenezis ve Neoplazi Kesişimi",
        "content": "Bu kontrol noktasında kronik enflamasyonun tüm vücuda yayılan sistemik hasarlarını ve uzun dönem komplikasyonlarını özetliyoruz:\n\n- **Kaşeksi:** TNF-α (kaşektin) etkisiyle iştah merkezinin baskılanması, LPL inhibisyonu ve kas proteolizi.\n- **Kronik Hastalık Anemisi:** IL-6 → karaciğerde Hepsidin artışı → ferroportin yıkımı → demirin makrofajlarda hapsolması.\n- **Sekonder AA Amiloidoz:** Karaciğer kökenli SAA artışı → böbrek glomerüllerinde beta-kırmalı tabakalar → Kongo kırmızısı ile elma yeşili çift kırıcılık.\n- **Organ Fibrozisi:** Çöken parankimin yerine M2 makrofaj kaynaklı TGF-β ile kollajen dolması (siroz, pulmoner fibrozis).\n- **Karsinojenez Köprüsü:** Sürekli replikasyon stresi + ROS mutasyonları + NF-κB sağkalımı (H. pylori-Mide CA, Marjolin ülseri).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Kronik osteomiyelitli bir hastada gelişen nefrotik sendrom tablosunda böbrek biyopsisinde Kongo kırmızısı ile boyanan ve polarize ışıkta elma yeşili çift kırıcılık veren amiloid fibril tipi hangisidir?",
                [
                    {"key": "A", "text": "AA (Serum Amiloid A kökenli fibriller)", "explanation": "A seçeneği DOĞRUDUR: Kronik enfeksiyon ve enflamasyonda biriken amiloid tipi AA'dır."},
                    {"key": "B", "text": "AL (Hafif zincir amiloidi)", "explanation": "B seçeneği yanlıştır: Plazma hücre diskrazilerinde (multipl myelom) görülür."},
                    {"key": "C", "text": "ATTR (Transtiretin amiloidi)", "explanation": "C seçeneği yanlıştır: Senil kardiyak amiloidozda birikir."},
                    {"key": "D", "text": "A-beta amiloidi", "explanation": "D seçeneği yanlıştır: Alzheimer hastalığında beyinde birikir."},
                    {"key": "E", "text": "Beta-2 mikroglobulin", "explanation": "E seçeneği yanlıştır: Kronik hemodiyaliz hastalarında eklemlerde birikir."}
                ],
                "A"
            ),
            make_cloze(
                "Kronik enflamasyonda karaciğerden salınan SAA proteininin birikmesiyle böbrekte nefrotik sendroma yol açan tabloya sekonder amiloidoz adı verilir.",
                "sekonder amiloidoz",
                "Kronik yangıya ikincil gelişen amiloid birikimi"
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-13-s80",
        "title": "'Non-Klasik' Düşük Dereceli Kronik Enflamasyon",
        "content": "Geleneksel patoloji enflamasyonu enfeksiyon ve otoimmüniteyle tanımlarken, 21. yüzyıl tıbbı **'düşük dereceli sessiz kronik enflamasyonun' (low-grade chronic inflammation)** modern çağın en öldürücü hastalıklarının motoru olduğunu kanıtlamıştır:\n\n1. **Tip 2 Diyabet ve İnsülin Direnci:** Obezitede hipertrofik adipositler hipoksiye girer; yağ dokusuna sızan M1 makrofajlar TNF-α ve IL-1β salgılar. Bu sitokinler insülin reseptör substratını (IRS-1) serin fosforilasyonu ile inaktive ederek insülin direncini başlatır.\n2. **Ateroskleroz:** İntimadaki okside LDL'nin makrofaj köpük hücreleri oluşturması ve aralıksız sitokin salması damar sertliğini ilerletir.\n3. **Alzheimer Hastalığı:** Beyinde biriken amiloid-beta plakları mikroglia hücrelerini sürekli uyararak nörotoksik sitokin salgılatır ve nöron ölümünü hızlandırır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Klasik Enfeksiyöz Enflamasyon vs Düşük Dereceli Metabolik Enflamasyon",
                "Klasik Enflamasyon (Tüberküloz, Apse)",
                "Ateş, lökositoz, yüksek CRP ve belirgin histolojik hücre toplanması izlenir.",
                "Metabolik Enflamasyon (Metaflammation)",
                "Sessiz, klinik semptomsuz, subklinik sitokin yüksekliği; insülin direnci ve aterogenez yapar."
            ),
            make_recall(
                "Obezitede genişleyen yağ dokusuna sızan makrofajların salgıladığı ve insülin reseptör sinyalini bozarak diyabete zemin hazırlayan temel sitokin hangisidir?",
                "Tümör Nekroz Faktörü-alfadır (TNF-α / IL-1β ile birlikte).",
                "İnsülin direncini tetikleyen adipokin/sitokin"
            )
        ]
    })

    return slides
