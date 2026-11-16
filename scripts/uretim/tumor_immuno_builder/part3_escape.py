# -*- coding: utf-8 -*-
"""
Part 3: Tümörün İmmün Kaçış Mekanizmaları ve İmmünoterapi (Slayt 11 - 15)
Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde.
"""

slides_part3 = [
    # SLIDE 11
    {
        "slideNumber": 11,
        "title": "Antijen İşleme ve Sunum Yolunun Kaybı (İmmün Körlük)",
        "subtitle": "Beta-2 mikroglobulin mutasyonları, TAP kusurları ve immünoediting",
        "badge": "İmmün Kaçış",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser İmmünodüzenlemesinin kaçış evresinde tümör 'görünmez pelerinini' giyer. Beta-2 mikroglobulini mutasyona uğratıp zardan MHC-I'i siler. T hücresi tümöre bakar ama hiçbir şey göremez; buna immün körlük diyoruz!",
            "note": "Prof. Dr. Hikmet Keleş, B2M mutasyonlarının hem edinsel immün kaçışta hem de checkpoint inhibitörlerine karşı gelişen sekonder dirençte temel biyobelirteç olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Kanser İmmünodüzenlemesi (Immunoediting): Eliminasyon, Denge ve Kaçış\n"
            "Tümör ve bağışıklık sistemi arasındaki dinamik etkileşim **Kanser İmmünodüzenlemesi (Cancer Immunoediting)** olarak adlandırılan "
            "üç evreli bir süreçtir: 1) **Eliminasyon (Gözetim):** İmmün sistem neoplastik klonları başarıyla yok eder. 2) **Denge (Equilibrium):** "
            "İmmün sistem tümör büyümesini kontrol altında tutar ancak tam eradikasyon sağlayamaz; bu evrede immün baskıya en dirençli mutant "
            "subklonlar seçilir (immünoseleksiyon). 3) **Kaçış (Escape):** Bağışıklık denetiminden kurtulan mutant klonlar kontrolsüzce "
            "çoğalarak klinik kanser kitlesini oluşturur.\n\n"
            "### Beta-2 Mikroglobulin (B2M) Mutasyonları ve MHC Sınıf I Kaybı\n"
            "Sitotoksik CD8+ T lenfositlerin bir tümör hücresini öldürebilmesi için hücre zarında fonksiyonel bir **MHC Sınıf I** kompleksi "
            "bulunmalıdır. Bu kompleks üç alfa alanından oluşan ağır zincir ile buna non-kovalan bağlı **Beta-2 Mikroglobulin (B2M)** "
            "hafif zincirinden meydana gelir. Malign melanom ve kolorektal karsinomlarda B2M geninde delesyon veya inaktive edici "
            "mutasyonlar sıkça gelişir. B2M olmadığında MHC Sınıf I ağır zinciri endoplazmik retikulumda katlanamaz ve hücre yüzeyine "
            "taşınamaz! Zarda MHC-I bulunmayan tümör hücresi CD8+ CTL'ler için tamamen görünmez hale gelir (**İmmün Körlük / Immune "
            "Blindness**). B2M kaybı, aynı zamanda Anti-PD-1 immünoterapisine başlangıçta yanıt veren hastalarda sonradan gelişen "
            "**sekonder (edinilmiş) direncin** en sık moleküler nedenidir.\n\n"
            "### Antijen İşleme ve Taşıma (APM) Bozuklukları\n"
            "Tümörler ayrıca peptit işleme zincirinin diğer halkalarını da sabote ederler:\n"
            "- **TAP1 ve TAP2 (Transporter associated with Antigen Processing) Defektleri:** Sitozolde proteazom tarafından kesilen "
            "tümör peptitlerinin endoplazmik retikulum lümenine pompalanması durur; MHC-I boş kalır ve hücre içinde parçalanır.\n"
            "- **LMP2 / LMP7 Proteazom Kusurları:** İmmünoproteazom alt birimlerinin kaybı antijenlerin uygun boyutlarda kesilmesini engeller.\n"
            "- **Antijenik Kayıp (Modülasyon):** İmmün sistem belirli bir neoantijene saldırdığında, bu antijeni kodlayan geni mutasyonla "
            "kaybeden alt klonlar hayatta kalarak kitleye hakim olur.\n\n"
            "🔴 **ÖNEMLİ:** Beta-2 mikroglobulin (B2M) mutasyonu sonucu MHC Sınıf I'in hücre zarına çıkamaması, tümörün CD8+ CTL saldırısından "
            "kaçmasını sağlar ve Anti-PD-1 tedavisine sekonder direnç doğurur.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Tümör hücresinde sitozolde üretilen antijenik peptitlerin endoplazmik retikulum lümenine taşınmasını "
            "sağlayan ve defektinde antijen sunumu bozulan taşıyıcı protein kompleksi TAP'tır."
        ),
        "content": (
            "### Kanser İmmünodüzenlemesi (Immunoediting): Eliminasyon, Denge ve Kaçış\n"
            "Tümör ve bağışıklık sistemi arasındaki dinamik etkileşim **Kanser İmmünodüzenlemesi (Cancer Immunoediting)** olarak adlandırılan "
            "üç evreli bir süreçtir: 1) **Eliminasyon (Gözetim):** İmmün sistem neoplastik klonları başarıyla yok eder. 2) **Denge (Equilibrium):** "
            "İmmün sistem tümör büyümesini kontrol altında tutar ancak tam eradikasyon sağlayamaz; bu evrede immün baskıya en dirençli mutant "
            "subklonlar seçilir (immünoseleksiyon). 3) **Kaçış (Escape):** Bağışıklık denetiminden kurtulan mutant klonlar kontrolsüzce "
            "çoğalarak klinik kanser kitlesini oluşturur.\n\n"
            "### Beta-2 Mikroglobulin (B2M) Mutasyonları ve MHC Sınıf I Kaybı\n"
            "Sitotoksik CD8+ T lenfositlerin bir tümör hücresini öldürebilmesi için hücre zarında fonksiyonel bir **MHC Sınıf I** kompleksi "
            "bulunmalıdır. Bu kompleks üç alfa alanından oluşan ağır zincir ile buna non-kovalan bağlı **Beta-2 Mikroglobulin (B2M)** "
            "hafif zincirinden meydana gelir. Malign melanom ve kolorektal karsinomlarda B2M geninde delesyon veya inaktive edici "
            "mutasyonlar sıkça gelişir. B2M olmadığında MHC Sınıf I ağır zinciri endoplazmik retikulumda katlanamaz ve hücre yüzeyine "
            "taşınamaz! Zarda MHC-I bulunmayan tümör hücresi CD8+ CTL'ler için tamamen görünmez hale gelir (**İmmün Körlük / Immune "
            "Blindness**). B2M kaybı, aynı zamanda Anti-PD-1 immünoterapisine başlangıçta yanıt veren hastalarda sonradan gelişen "
            "**sekonder (edinilmiş) direncin** en sık moleküler nedenidir.\n\n"
            "### Antijen İşleme ve Taşıma (APM) Bozuklukları\n"
            "Tümörler ayrıca peptit işleme zincirinin diğer halkalarını da sabote ederler:\n"
            "- **TAP1 ve TAP2 (Transporter associated with Antigen Processing) Defektleri:** Sitozolde proteazom tarafından kesilen "
            "tümör peptitlerinin endoplazmik retikulum lümenine pompalanması durur; MHC-I boş kalır ve hücre içinde parçalanır.\n"
            "- **LMP2 / LMP7 Proteazom Kusurları:** İmmünoproteazom alt birimlerinin kaybı antijenlerin uygun boyutlarda kesilmesini engeller.\n"
            "- **Antijenik Kayıp (Modülasyon):** İmmün sistem belirli bir neoantijene saldırdığında, bu antijeni kodlayan geni mutasyonla "
            "kaybeden alt klonlar hayatta kalarak kitleye hakim olur.\n\n"
            "🔴 **ÖNEMLİ:** Beta-2 mikroglobulin (B2M) mutasyonu sonucu MHC Sınıf I'in hücre zarına çıkamaması, tümörün CD8+ CTL saldırısından "
            "kaçmasını sağlar ve Anti-PD-1 tedavisine sekonder direnç doğurur.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Tümör hücresinde sitozolde üretilen antijenik peptitlerin endoplazmik retikulum lümenine taşınmasını "
            "sağlayan ve defektinde antijen sunumu bozulan taşıyıcı protein kompleksi TAP'tır."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** B2M mutasyonu MHC Sınıf I'in hücre yüzeyine taşınmasını imkansız kılar; tümör CTL için görünmez hale gelir.",
            "🔵 **ÇIKMIŞ SORU:** Kanser İmmünodüzenlemesinin (Immunoediting) 'Kaçış' evresinde, immün saldırıya dirençli mutant subklonlar seçilerek tümör progresyonu gerçekleşir.",
            "⚡ **DİRENÇ:** Anti-PD-1 immünoterapisi alırken nükseden melanom olgularında en sık saptanan edinsel direnç mutasyonu B2M gen kaybıdır."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** TAP kusurları sitoplazmik peptitlerin ER lümenine taşınmasını engelleyerek MHC-I'in boş kalıp yıkılmasına neden olur.",
            "🔵 **ÇIKMIŞ SORU:** Tümör hücrelerinin bağışıklık sisteminin tanıdığı spesifik neoantijenleri eksprese etmeyi durdurması 'Antijenik Kayıp' olarak adlandırılır.",
            "⚡ **DİRENÇ:** MHC-I kaybı CTL'den kaçış sağlasa da hücreyi NK hücrelerinin missing-self saldırısına duyarlı hale getirebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Kanser İmmünodüzenlemesi",
                    "desc": "Eliminasyon, Denge ve Kaçış (3E kuralı) basamaklarıyla tümörün immün baskı altında evrilmesidir.",
                    "isKey": True
                },
                {
                    "title": "B2M Gen İnaktivasyonu",
                    "desc": "MHC-I yüzeye çıkamaz; CTL hücreleri neoantijenleri tanıyamaz ve edinsel tedavi direnci başlar.",
                    "isKey": True
                },
                {
                    "title": "TAP ve Proteazom Kusurları",
                    "desc": "Antijen işleme mekanizmasının (APM) bozulması peptitlerin ER'ye geçişini felç eder.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Antijen Sunum Yolundaki Kusurlar ve İmmünolojik Sonuçları",
                "headers": ["Moleküler Kusur", "Etkilenen Biyolojik Adım", "CTL Yanıtı Üzerine Etkisi", "Klinik / Terapötik Yansıması"],
                "rows": [
                    ["B2M Mutasyonu / Delesyonu", "MHC-I ağır zincirinin hücre zarına taşınması", "CTL tanıma yeteneği tamamen çöker", "Anti-PD-1 tedavisine sekonder edinsel direnç"],
                    ["TAP1 / TAP2 Kusuru", "Peptitlerin sitozolden ER lümenine taşınması", "MHC-I molekülleri peptitsiz kalır ve yıkılır", "Düşük antijen sunumu, zayıf immünojenite"],
                    ["LMP2 / LMP7 Defekti", "Proteazomda antijenik kesim işlemi", "Uygun neoantijen epitopları üretilemez", "Tümör antijen repertuarının daralması"],
                    ["Spesifik Neoantijen Kaybı", "Mutant genin transkripsiyonunun durması", "Tümöre özgü CTL klonu hedefsiz kalır", "Klonal seleksiyonla nüks gelişimi"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-11-01",
                "category": "İmmün Kaçış",
                "front": "Tümör hücresinde Beta-2 mikroglobulin (B2M) gen mutasyonunun en yıkıcı immünolojik sonucu nedir?",
                "hint": "MHC Sınıf I molekülünün hücre zarına taşınması.",
                "back": "MHC Sınıf I zarda eksprese edilemez; tümör hücresi **CD8+ CTL'ler için görünmez hale gelir (İmmün Körlük)**.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide B2M kaybının immünoterapi başarısızlığının en önemli nedeni olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-11-02",
                "category": "Kanser İmmünodüzenlemesi",
                "front": "Kanser İmmünodüzenlemesinin (3E) hangi evresinde konağın bağışıklık sistemi en dirençli subklonları seçerek kaçışa zemin hazırlar?",
                "hint": "Eliminasyon ile Kaçış arasındaki ara evre.",
                "back": "**Denge (Equilibrium) Evresi**. İmmün baskı tümörü tamamen temizleyemez; bu süreçte immünorezistan mutant subklonlar klonal olarak seçilir.",
                "facultyNote": "Immunoediting basamakları TUS'ta kavramsal soru olarak sorgulanmaktadır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-11",
            "question": "Metastatik malign melanom tanısıyla Pembrolizumab (Anti-PD-1) tedavisi başlanan ve 18 ay boyunca tam radyolojik remisyonda kalan 59 yaşındaki bir hastada, 20. ayda karaciğerde yeni metastatik odaklar gelişiyor. Yapılan yeni biyopsi materyalinde tümör hücrelerinde Beta-2 mikroglobulin (B2M) geninde bialelik inaktive edici mutasyon saptanıyor. Bu direnç tablosunun patofizyolojik açıklaması hangisidir?",
            "options": [
                "A) B2M mutasyonu tümör hücrelerinin hücre siklusunu hızlandırarak mitozu durdurulamaz hale getirmiştir.",
                "B) B2M kaybı nedeniyle MHC Sınıf I molekülü hücre zarına taşınamamış; tümör hücreleri CTL tarafından tanınamaz hale gelerek edinsel immün kaçış sağlamıştır.",
                "C) B2M proteini doğrudan PD-1 reseptörüne bağlandığı için ilacın etkinliğini artırmıştır.",
                "D) Hastada pembrolizumaba karşı nötralizan IgE antikorları gelişmiştir.",
                "E) B2M mutasyonu yalnızca eritrositlerde glikoz taşınmasını bozan selim bir polimorfizmdir."
            ],
            "answer": "B",
            "explanation": "Anti-PD-1 tedavisi alan hastalarda başlangıçta mükemmel yanıt varken aylar sonra nüks gelişmesine 'edinsel (sekonder) immünoterapi direnci' denir. Bunun en sık saptanan moleküler mekanizması Beta-2 mikroglobulin (B2M) gen mutasyonudur. B2M olmadan MHC Sınıf I katlanıp hücre zarına çıkamaz. Yüzeyinde MHC-I taşımayan tümör hücresi, etrafta çok sayıda aktive CD8+ T hücresi bulunsa bile tanınamaz ('İmmün Körlük') ve tümör progresyon gösterir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 12
    {
        "slideNumber": 12,
        "title": "İmmün Kontrol Noktaları I: PD-1 / PD-L1 Yolağı ve T Hücre Tükenmişliği",
        "subtitle": "SHP-2 fosfataz sinyali, periferal tolerans istismarı ve monoklonal inhibitörler",
        "badge": "Kontrol Noktası Blokajı",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "PD-1 ve PD-L1 etkileşimi T hücresinin elindeki silahı düşürmektir. Tümör hücresi yüzeyine PD-L1 bayrağını diker; T hücresindeki PD-1'e bağlandığı anda SHP-2 fosfatazı aktive olur ve T hücresini 'tükenmişlik' uykusuna sokar.",
            "note": "Prof. Dr. Hikmet Keleş, PD-1 inhibitörlerinin (Pembrolizumab, Nivolumab) etki mekanizmasının ve adaptif immün direnç kavramının sınavların en popüler konusu olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### PD-1 ve PD-L1'in Fizyolojik Fonksiyonu\n"
            "Sağlıklı bir organizmada **Programlanmış Hücre Ölümü-1 (PD-1 / CD279)** reseptörü, aktive olmuş T lenfositleri, B hücreleri "
            "ve monositler üzerinde eksprese edilen bir eş-inhibitör reseptördür. Temel ligantları **PD-L1 (B7-H1 / CD274)** ve **PD-L2 (CD273)**'dir. "
            "Fizyolojik görevi, enfeksiyon alanlarında kronik inflamasyonu sınırlandırmak, doku hasarını önlemek ve periferik dokularda "
            "otoimmün reaksiyonları baskılamaktır (**periferik tolerans**).\n\n"
            "### Tümörde PD-L1 İstismarı ve Adaptif İmmün Direnç\n"
            "Malign neoplaziler bu periferik tolerans mekanizmasını iki yolla istismar ederler:\n"
            "1. **İntrensek Onkojenik İndüksiyon:** Tümör hücresindeki onkojenik mutasyonlar (örn. PTEN kaybı, EGFR aktivasyonu, ALK füzyonları) "
            "PI3K/Akt yolağı üzerinden konstitütif olarak PD-L1 ekspresyonunu artırır.\n"
            "2. **Adaptif İmmün Direnç (Diyalektik Yanıt):** Tümör yatağına sızan CD8+ CTL'ler tümörü yok etmek amacıyla **İnterferon-gama "
            "(IFN-γ)** salgılar. Ancak tümör hücreleri bu IFN-γ sinyalini JAK/STAT yolağı ile algılayarak paradoksal bir savunma kalkanı "
            "kurar: Hücre yüzeylerine yoğun şekilde **PD-L1** yerleştirirler!\n\n"
            "### Moleküler İletim: SHP-2 Fosfatazı ve T Hücre Tükenmişliği (Exhaustion)\n"
            "PD-L1, T lenfosit üzerindeki PD-1'e bağlandığında, PD-1'in sitoplazmik kuyruğundaki ITSM motifi fosforillenir. Bu bölgeye "
            "sitoplazmik tirozin fosfataz olan **SHP-2** bağlanarak aktive olur. SHP-2, TCR kompleksindeki ZAP-70'i ve CD28 yolağındaki "
            "PI3K'yı doğrudan defosforile eder. Sonuçta T hücresinin proliferasyonu durur, IL-2 ve sitotoksik granül salınımı kesilir. "
            "Sürekli antijen maruziyeti altındaki T lenfositi geri dönüşümsüz bir **Tükenmişlik (Exhaustion)** durumuna girer.\n\n"
            "### Farmakolojik Blokaj (İmmün Kontrol Noktası İnhibitörleri)\n"
            "- **Anti-PD-1 Monoklonal Antikorlar:** **Pembrolizumab**, **Nivolumab**, **Cemiplimab**.\n"
            "- **Anti-PD-L1 Monoklonal Antikorlar:** **Atezolizumab**, **Durvalumab**, **Avelumab**.\n"
            "Bu ilaçlar PD-1 ile PD-L1 arasındaki bağı fiziksel olarak bloke ederek T hücresindeki freni kaldırır; tükenmiş CTL'leri "
            "yeniden canlandırarak tümörü yok etmelerini sağlar.\n\n"
            "🔴 **ÖNEMLİ:** PD-1/PD-L1 etkileşimi SHP-2 fosfatazı üzerinden TCR ve CD28 sinyallerini defosforilasyonla keser; T hücresini "
            "'tükenmiş' (exhausted) fenotipe sokarak inaktive eder.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Tümör hücrelerinde eksprese edilen PD-L1 molekülüne bağlanarak T lenfositlerinin inaktivasyonunu sağlayan "
            "ve Pembrolizumab ile hedeflenen reseptör PD-1'dir (CD279)."
        ),
        "content": (
            "### PD-1 ve PD-L1'in Fizyolojik Fonksiyonu\n"
            "Sağlıklı bir organizmada **Programlanmış Hücre Ölümü-1 (PD-1 / CD279)** reseptörü, aktive olmuş T lenfositleri, B hücreleri "
            "ve monositler üzerinde eksprese edilen bir eş-inhibitör reseptördür. Temel ligantları **PD-L1 (B7-H1 / CD274)** ve **PD-L2 (CD273)**'dir. "
            "Fizyolojik görevi, enfeksiyon alanlarında kronik inflamasyonu sınırlandırmak, doku hasarını önlemek ve periferik dokularda "
            "otoimmün reaksiyonları baskılamaktır (**periferik tolerans**).\n\n"
            "### Tümörde PD-L1 İstismarı ve Adaptif İmmün Direnç\n"
            "Malign neoplaziler bu periferik tolerans mekanizmasını iki yolla istismar ederler:\n"
            "1. **İntrensek Onkojenik İndüksiyon:** Tümör hücresindeki onkojenik mutasyonlar (örn. PTEN kaybı, EGFR aktivasyonu, ALK füzyonları) "
            "PI3K/Akt yolağı üzerinden konstitütif olarak PD-L1 ekspresyonunu artırır.\n"
            "2. **Adaptif İmmün Direnç (Diyalektik Yanıt):** Tümör yatağına sızan CD8+ CTL'ler tümörü yok etmek amacıyla **İnterferon-gama "
            "(IFN-γ)** salgılar. Ancak tümör hücreleri bu IFN-γ sinyalini JAK/STAT yolağı ile algılayarak paradoksal bir savunma kalkanı "
            "kurar: Hücre yüzeylerine yoğun şekilde **PD-L1** yerleştirirler!\n\n"
            "### Moleküler İletim: SHP-2 Fosfatazı ve T Hücre Tükenmişliği (Exhaustion)\n"
            "PD-L1, T lenfosit üzerindeki PD-1'e bağlandığında, PD-1'in sitoplazmik kuyruğundaki ITSM motifi fosforillenir. Bu bölgeye "
            "sitoplazmik tirozin fosfataz olan **SHP-2** bağlanarak aktive olur. SHP-2, TCR kompleksindeki ZAP-70'i ve CD28 yolağındaki "
            "PI3K'yı doğrudan defosforile eder. Sonuçta T hücresinin proliferasyonu durur, IL-2 ve sitotoksik granül salınımı kesilir. "
            "Sürekli antijen maruziyeti altındaki T lenfositi geri dönüşümsüz bir **Tükenmişlik (Exhaustion)** durumuna girer.\n\n"
            "### Farmakolojik Blokaj (İmmün Kontrol Noktası İnhibitörleri)\n"
            "- **Anti-PD-1 Monoklonal Antikorlar:** **Pembrolizumab**, **Nivolumab**, **Cemiplimab**.\n"
            "- **Anti-PD-L1 Monoklonal Antikorlar:** **Atezolizumab**, **Durvalumab**, **Avelumab**.\n"
            "Bu ilaçlar PD-1 ile PD-L1 arasındaki bağı fiziksel olarak bloke ederek T hücresindeki freni kaldırır; tükenmiş CTL'leri "
            "yeniden canlandırarak tümörü yok etmelerini sağlar.\n\n"
            "🔴 **ÖNEMLİ:** PD-1/PD-L1 etkileşimi SHP-2 fosfatazı üzerinden TCR ve CD28 sinyallerini defosforilasyonla keser; T hücresini "
            "'tükenmiş' (exhausted) fenotipe sokarak inaktive eder.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Tümör hücrelerinde eksprese edilen PD-L1 molekülüne bağlanarak T lenfositlerinin inaktivasyonunu sağlayan "
            "ve Pembrolizumab ile hedeflenen reseptör PD-1'dir (CD279)."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** PD-1/PD-L1 bağlanması SHP-2 fosfatazı aktive eder; TCR downstream kinazları defosforile olarak T hücresi 'tükenmişlik' fenotipine sokulur.",
            "🔵 **ÇIKMIŞ SORU:** T hücrelerinin salgıladığı IFN-γ'ya yanıt olarak tümör hücrelerinin JAK/STAT üzerinden yüzeyine PD-L1 yerleştirmesi 'Adaptif İmmün Direnç'tir.",
            "⚡ **İLAÇLAR:** Pembrolizumab ve Nivolumab doğrudan T hücresindeki PD-1'i; Atezolizumab ve Durvalumab ise tümördeki PD-L1'i bloke eder."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** PD-1 ekspresyonu kronik antijen maruziyetiyle tükenmiş T lenfositlerinde en yüksek seviyededir.",
            "🔵 **ÇIKMIŞ SORU:** Küçük hücreli dışı akciğer karsinomunda Pembrolizumab tedavisi öncesi patolojik biyopside PD-L1 TPS skoru bakılır.",
            "⚡ **İLAÇLAR:** Anti-PD-1/PD-L1 tedavileri T hücresinin üzerindeki freni kaldırarak otoimmünite benzeri immün ilişkili yan etkilere yol açabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Periferik Tolerans İstismarı",
                    "desc": "Tümör hücreleri PD-L1 eksprese ederek dokuda otoimmüniteyi önleyen periferik kontrol noktasını sömürür.",
                    "isKey": True
                },
                {
                    "title": "SHP-2 Fosfataz Sinyali",
                    "desc": "ITSM motifi üzerinden aktive olan SHP-2, ZAP-70 ve PI3K'yı susturarak T hücresini anerji ve tükenmişliğe iter.",
                    "isKey": True
                },
                {
                    "title": "Terapötik Monoklonal Antikorlar",
                    "desc": "Anti-PD-1 (Pembrolizumab) ve Anti-PD-L1 (Atezolizumab) bu teması kırarak sitotoksisiteyi yeniden canlandırır.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "İmmün Kontrol Noktası İnhibitörleri (Anti-PD-1 vs Anti-PD-L1)",
                "headers": ["İlaç Sınıfı", "Örnek İlaçlar", "Hedeflenen Molekül", "Hedef Hücre Tipi", "Başlıca Onaylı Endikasyonlar"],
                "rows": [
                    ["Anti-PD-1 Antikorları", "Pembrolizumab, Nivolumab, Cemiplimab", "PD-1 (CD279)", "Aktive / Tükenmiş T Lenfositler", "Melanom, KHDAK, MSI-H tümörler, Hodgkin lenfoma"],
                    ["Anti-PD-L1 Antikorları", "Atezolizumab, Durvalumab, Avelumab", "PD-L1 (CD274 / B7-H1)", "Tümör hücreleri ve TAM / MDSC", "Ürotelyal Ca, Küçük hücreli akciğer Ca, TNBC"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-12-01",
                "category": "Kontrol Noktaları",
                "front": "PD-1 reseptörüne PD-L1 bağlandığında T hücresi içinde hangi fosfataz aktive olarak TCR sinyallerini kapatır?",
                "hint": "Tirozin fosfataz ailesi üyesi.",
                "back": "**SHP-2 fosfatazı**. ZAP-70 ve CD28 downstream sinyallerini defosforile ederek T hücresini tükenmişlik fenotipine sokar.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide SHP-2'nin T hücresi içindeki temel şalter olduğunu vurgulamıştır."
            },
            {
                "id": "imm-fc-12-02",
                "category": "İmmünoterapi",
                "front": "Tümör yatağındaki T hücrelerinin saldığı IFN-γ'nın tümör hücrelerinde PD-L1 artışına yol açmasına ne ad verilir?",
                "hint": "Bağışıklığa karşı geliştirilen adaptif yanıt.",
                "back": "**Adaptif İmmün Direnç**. Tümör, lenfositlerin saldırı silahı olan IFN-γ'yı algılayıp kendini korumak için PD-L1 zırhı giyer.",
                "facultyNote": "TUS ve Board sınavlarında adaptif direnç kavramı mekanizma sorularında sıkça çıkar."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-12",
            "question": "Metastatik küçük hücreli dışı akciğer karsinomu (KHDAK) tanısı alan bir hastanın tümör biyopsisinde immünohistokimyasal boyama ile tümör hücrelerinin %60'ında kuvvetli membranöz PD-L1 ekspresyonu (TPS > %50) saptanıyor. Bu hastaya başlanan Pembrolizumab monoklonal antikor tedavisinin hücresel ve moleküler etki mekanizması ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) Doğrudan tümör DNA'sına interkale olarak topoizomeraz enzimini inhibe eder.",
                "B) Tümör hücrelerindeki VEGF reseptörünü bloke ederek anjiyogenezi durdurur.",
                "C) T lenfositlerindeki PD-1 reseptörüne bağlanıp PD-L1 ile etkileşimini bloke ederek SHP-2 fosfataz aktivasyonunu engeller ve tükenmiş CTL'leri yeniden aktive eder.",
                "D) B hücrelerinde antikor üretimini tamamen durdurarak otoimmün toksisiteyi engeller.",
                "E) Yalnızca eritrosit membranındaki CD47 molekülünü kapatarak fagositozu artırır."
            ],
            "answer": "C",
            "explanation": "Pembrolizumab, T lenfosit yüzeyindeki PD-1 (CD279) eş-inhibitör reseptörüne bağlanan hümanize bir monoklonal antikordur. Tümör hücrelerindeki PD-L1'in PD-1'e bağlanmasını fiziksel olarak engelleyerek T hücresi içindeki SHP-2 fosfataz aktivasyonunu ve defosforilasyonu durdurur. Böylece T hücresindeki fren kaldırılır; 'tükenmiş' (exhausted) durumdaki sitotoksik CD8+ T lenfositleri yeniden aktive olarak tümörü lize eder.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 13
    {
        "slideNumber": 13,
        "title": "İmmün Kontrol Noktaları II: CTLA-4 Yolağı ve Lenfoid Düzenleme",
        "subtitle": "B7-1/B7-2 yarışmalı antagonizması, İpilimumab ve irAE toksisiteleri",
        "badge": "Kontrol Noktası Blokajı",
        "badgeColor": "indigo",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "CTLA-4 ordunun kışladan çıkışını durduran nöbetçidir! Lenf nodunda B7 molekülünü CD28'in elinden 20-100 kat daha yüksek bir aşkla kapar. İpilimumab bu nöbetçiyi ekarte eder; tüm kışla (T hücre ordusu) tümörün üzerine yürür ama otoimmün fırtınaya dikkat!",
            "note": "Prof. Dr. Hikmet Keleş, CTLA-4 blokajının endokrin yan etkisi olan hipofizitin TUS sınavlarında klasik bir vaka sorusu olduğunu vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### CTLA-4'ün Biyolojik Doğası ve Erken Dönem Düzenleme\n"
            "**Sitotoksik T Lenfosit Antijeni-4 (CTLA-4 / CD152)**, T hücresi aktivasyonunun en erken evresinde, özellikle sekonder "
            "lenfoid organlarda (**lenf nodlarında**) T hücresi uyarılma eşiğini ayarlayan ana negatif düzenleyicidir. Naif T hücrelerinde "
            "intrasellüler veziküllerde saklanır; TCR uyarımı sonrasında hızla hücre zarına taşınır. Ayrıca Düzenleyici T hücrelerinde "
            "(**Treg**) konstitütif (sürekli) olarak eksprese edilir.\n\n"
            "### CD28 ile B7 İçin Yarışma (Kompetitif İnhibisyon)\n"
            "Bir T hücresinin tam olarak uyarılabilmesi için antijen sunan hücre (APC) yüzeyindeki B7-1 (CD80) veya B7-2 (CD86) "
            "moleküllerinin T hücresindeki kostimülatör reseptör **CD28**'e bağlanması zorunludur. CTLA-4, bu B7 ligandlarına CD28'den "
            "**20 ila 100 kat daha yüksek afiniteyle bağlanır!** Hücre yüzeyine çıktığı anda ortamdaki tüm B7 moleküllerini yarışmalı "
            "olarak kapar ve CD28'in bağlanmasını engeller. Dahası, CTLA-4 bağlandığı B7 moleküllerini endositozla içeri çekip yıkar "
            "(**trans-endositoz**). İntrasellüler olarak Akt aktivasyonunu durdurarak lenf nodundaki naif T hücresi klonal genişlemesini "
            "erken dönemde sonlandırır.\n\n"
            "### İpilimumab ve Terapötik CTLA-4 Blokajı\n"
            "**İpilimumab**, CTLA-4'e karşı geliştirilmiş tam insan monoklonal antikordur (2018 Nobel Ödülü James Allison). İpilimumab "
            "CTLA-4'ü bloke ettiğinde, lenf nodunda T hücresi uyarılma eşiği düşer; poliklonal CD8+ CTL ordusu sınırsızca genişleyerek "
            "tümöre saldırır. Günümüzde metastatik melanomda **Nivolumab + İpilimumab** kombinasyonu çift kontrol noktası blokajıyla "
            "en yüksek yanıt oranlarını sağlamaktadır.\n\n"
            "### İmmün İlişkili İstenmeyen Olaylar (irAE)\n"
            "CTLA-4 sentral toleransın ana bekçisi olduğu için blokajında şiddetli sistemik otoimmün tablolar gelişir:\n"
            "- **Hipofizit (Hypophysitis):** Ön hipofiz bezinin otoimmün inflamasyonu sonucu baş ağrısı, görme bozukluğu, TSH/ACTH "
            "yıkımı ve panhipopituitarizm. En karakteristik endokrin yan etkidir.\n"
            "- **Otoimmün Kolit:** Günde 10-15 kez sulu-kanlı diyare ve bağırsak perforasyonu riski.\n"
            "- Diğerleri: Ağır hepatit, dermatit ve tiroidit. Tedavisinde yüksek doz sistemik kortikosteroidler (prednizolon) ve gerekirse "
            "anti-TNF (İnfliksimab) kullanılır.\n\n"
            "🔴 **ÖNEMLİ:** CTLA-4, B7 moleküllerine CD28'den 20-100 kat yüksek afiniteyle bağlanarak lenf nodundaki T hücresi aktivasyonunu "
            "erken dönemde durdurur; İpilimumab ile hedeflenir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** CTLA-4 blokajı yapan monoklonal antikor İpilimumab'dır; en karakteristik ve tanısal endokrin komplikasyonu "
            "ise hipofiz bezinin otoimmün destrüksiyonu olan Hipofizittir."
        ),
        "content": (
            "### CTLA-4'ün Biyolojik Doğası ve Erken Dönem Düzenleme\n"
            "**Sitotoksik T Lenfosit Antijeni-4 (CTLA-4 / CD152)**, T hücresi aktivasyonunun en erken evresinde, özellikle sekonder "
            "lenfoid organlarda (**lenf nodlarında**) T hücresi uyarılma eşiğini ayarlayan ana negatif düzenleyicidir. Naif T hücrelerinde "
            "intrasellüler veziküllerde saklanır; TCR uyarımı sonrasında hızla hücre zarına taşınır. Ayrıca Düzenleyici T hücrelerinde "
            "(**Treg**) konstitütif (sürekli) olarak eksprese edilir.\n\n"
            "### CD28 ile B7 İçin Yarışma (Kompetitif İnhibisyon)\n"
            "Bir T hücresinin tam olarak uyarılabilmesi için antijen sunan hücre (APC) yüzeyindeki B7-1 (CD80) veya B7-2 (CD86) "
            "moleküllerinin T hücresindeki kostimülatör reseptör **CD28**'e bağlanması zorunludur. CTLA-4, bu B7 ligandlarına CD28'den "
            "**20 ila 100 kat daha yüksek afiniteyle bağlanır!** Hücre yüzeyine çıktığı anda ortamdaki tüm B7 moleküllerini yarışmalı "
            "olarak kapar ve CD28'in bağlanmasını engeller. Dahası, CTLA-4 bağlandığı B7 moleküllerini endositozla içeri çekip yıkar "
            "(**trans-endositoz**). İntrasellüler olarak Akt aktivasyonunu durdurarak lenf nodundaki naif T hücresi klonal genişlemesini "
            "erken dönemde sonlandırır.\n\n"
            "### İpilimumab ve Terapötik CTLA-4 Blokajı\n"
            "**İpilimumab**, CTLA-4'e karşı geliştirilmiş tam insan monoklonal antikordur (2018 Nobel Ödülü James Allison). İpilimumab "
            "CTLA-4'ü bloke ettiğinde, lenf nodunda T hücresi uyarılma eşiği düşer; poliklonal CD8+ CTL ordusu sınırsızca genişleyerek "
            "tümöre saldırır. Günümüzde metastatik melanomda **Nivolumab + İpilimumab** kombinasyonu çift kontrol noktası blokajıyla "
            "en yüksek yanıt oranlarını sağlamaktadır.\n\n"
            "### İmmün İlişkili İstenmeyen Olaylar (irAE)\n"
            "CTLA-4 sentral toleransın ana bekçisi olduğu için blokajında şiddetli sistemik otoimmün tablolar gelişir:\n"
            "- **Hipofizit (Hypophysitis):** Ön hipofiz bezinin otoimmün inflamasyonu sonucu baş ağrısı, görme bozukluğu, TSH/ACTH "
            "yıkımı ve panhipopituitarizm. En karakteristik endokrin yan etkidir.\n"
            "- **Otoimmün Kolit:** Günde 10-15 kez sulu-kanlı diyare ve bağırsak perforasyonu riski.\n"
            "- Diğerleri: Ağır hepatit, dermatit ve tiroidit. Tedavisinde yüksek doz sistemik kortikosteroidler (prednizolon) ve gerekirse "
            "anti-TNF (İnfliksimab) kullanılır.\n\n"
            "🔴 **ÖNEMLİ:** CTLA-4, B7 moleküllerine CD28'den 20-100 kat yüksek afiniteyle bağlanarak lenf nodundaki T hücresi aktivasyonunu "
            "erken dönemde durdurur; İpilimumab ile hedeflenir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** CTLA-4 blokajı yapan monoklonal antikor İpilimumab'dır; en karakteristik ve tanısal endokrin komplikasyonu "
            "ise hipofiz bezinin otoimmün destrüksiyonu olan Hipofizittir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** CTLA-4, B7-1 ve B7-2 moleküllerine CD28'den 20-100 kat daha yüksek afiniteyle bağlanarak lenf nodunda T hücre aktivasyonunu erken dönemde baskılar.",
            "🔵 **ÇIKMIŞ SORU:** İpilimumab (Anti-CTLA-4) tedavisi alan hastada baş ağrısı, hipotansiyon ve çoklu hipofiz hormon eksikliği gelişmesi durumunda öncelikle 'Otoimmün Hipofizit' düşünülmelidir.",
            "⚡ **KONTROL NOKTASI FARKI:** CTLA-4 lenf nodunda aktivasyon fazını (erken) frenlerken; PD-1 periferik dokularda efektör fazı (geç) frenler."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Treg hücreleri konstitütif CTLA-4 ekspresyonu sayesinde APC'lerin B7 ligandlarını trans-endositozla temizleyerek diğer T hücrelerini baskılar.",
            "🔵 **ÇIKMIŞ SORU:** İmmün kontrol noktası inhibitörlerine bağlı gelişen şiddetli otoimmün kolit ve hipofizitin tedavisinde ilk basamak yüksek doz sistemik kortikosteroidlerdir.",
            "⚡ **KONTROL NOKTASI FARKI:** Çift kontrol noktası blokajı (Nivolumab + İpilimumab) sağkalımı belirgin artırır ancak irAE riskini %50'nin üzerine çıkarır."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "B7 İçin Yarışmalı Afinite Üstünlüğü",
                    "desc": "CD28'den 20-100 kat yüksek afiniteyle B7'ye bağlanıp T hücresinin ikinci kostimülatör sinyalini çalar.",
                    "isKey": True
                },
                {
                    "title": "İpilimumab ve Nobel Ödülü",
                    "desc": "CTLA-4'ü bloke ederek lenf nodundaki naif T hücrelerinin klonal genişleme eşiğini dramatik şekilde düşürür.",
                    "isKey": True
                },
                {
                    "title": "İmmün İlişkili Toksisiteler (irAE)",
                    "desc": "Hipofizit ve otoimmün kolit gibi hayatı tehdit eden otoimmün komplikasyonlar steroid ile tedavi edilir.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "CTLA-4 vs PD-1 Kontrol Noktaları Karşılaştırması",
                "headers": ["Özellik", "CTLA-4 (CD152)", "PD-1 (CD279)"],
                "rows": [
                    ["Birincil Etki Alanı", "Sekonder Lenfoid Organlar (Lenf Nodları)", "Periferik Dokular ve Tümör Mikroçevresi"],
                    ["Etki Ettiği Evre", "Aktivasyon Fazı (Erken safha)", "Efektör Faz (Geç safha)"],
                    ["Ligandları", "B7-1 (CD80) ve B7-2 (CD86)", "PD-L1 (CD274) ve PD-L2 (CD273)"],
                    ["Etki Mekanizması", "B7 için CD28 ile yarışmalı antagonizma", "SHP-2 fosfatazı ile TCR/CD28 sinyalinin kesilmesi"],
                    ["Terapötik Antikor", "İpilimumab, Tremelimumab", "Pembrolizumab, Nivolumab, Cemiplimab"],
                    ["Karakteristik Toksisite", "Ağır Otoimmün Hipofizit ve Kolit", "Pnömonit, Tiroidit, Nefrit"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-13-01",
                "category": "CTLA-4 Mekanizması",
                "front": "CTLA-4 molekülü T lenfosit aktivasyonunu hangi mekanizmayla durdurur?",
                "hint": "CD28 ile kostimülasyon yarışması.",
                "back": "APC üzerindeki **B7-1 (CD80) ve B7-2 (CD86)** ligandlarına **CD28'den 20-100 kat daha yüksek afiniteyle** bağlanarak kostimülasyon sinyalini yarışmalı olarak bloke eder.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide CTLA-4 ve CD28 yarışmasının afinite farkını özellikle sormuştur."
            },
            {
                "id": "imm-fc-13-02",
                "category": "İlaç Toksisitesi",
                "front": "İpilimumab (Anti-CTLA-4) kullanan bir kanser hastasında en karakteristik ve özgül endokrinolojik yan etki hangisidir?",
                "hint": "Sella tursika içindeki bezin iltihabı.",
                "back": "**Otoimmün Hipofizit (Ön hipofiz yetmezliği)**. Baş ağrısı, halsizlik, sekonder adrenal yetmezlik ve TSH eksikliği ile seyreder.",
                "facultyNote": "TUS ve Dahiliye Board sınavlarında İpilimumab-Hipofizit eşleştirmesi defalarca sorulmuştur."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-13",
            "question": "Metastatik malign melanom tanısıyla İpilimumab (Anti-CTLA-4 monoklonal antikoru) tedavisi başlanan 50 yaşındaki bir hastada tedavinin 8. haftasında şiddetli baş ağrısı, görme alanı daralması, halsizlik ve hipotansiyon gelişiyor. Yapılan hormonal tetkiklerde ACTH, TSH ve LH/FSH düzeylerinin belirgin düştüğü, hipofiz MRG'sinde bezde difüz kontrast tutulumu ve genişleme saptanıyor. Bu klinik tablonun patofizyolojisi ve CTLA-4 fonksiyonu ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) İpilimumab doğrudan hipofiz bezi hücrelerini enfekte eden rekombinant bir virüstür.",
                "B) İpilimumab lenf nodunda B7-CD28 kostimülasyonu üzerindeki CTLA-4 frenini kaldırarak genel immün toleransı gevşetmiş ve otoimmün hipofizit tablosu gelişmiştir.",
                "C) Hipofiz adenomu gelişmiştir ve acil cerrahi rezeksiyon yapılmalıdır.",
                "D) CTLA-4 yalnızca periferik dokularda eksprese edildiği için bu tablo ilaca bağlı olamaz.",
                "E) İpilimumab böbrekten sodyum atılımını artırarak hipofiz bezinde infarkta yol açmıştır."
            ],
            "answer": "B",
            "explanation": "İpilimumab, T hücre aktivasyonunu erken fazda frenleyen CTLA-4 molekülünü bloke eden bir monoklonal antikordur. CTLA-4 sistemik self-toleransın korunmasında kritik bir bekçidir. Blokajı ile T hücre aktivasyon eşiği düşer ve hastanın bağışıklık sistemi kendi dokularına da saldırabilir (immün ilişkili advers olaylar - irAE). En karakteristik endokrin komplikasyonu ön hipofiz bezinin lenfositik inflamasyonu olan 'Otoimmün Hipofizit'tir; panhipopituitarizm ve baş ağrısı ile seyreder. Tedavisinde yüksek doz sistemik steroid replasmanı gerekir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 14
    {
        "slideNumber": 14,
        "title": "İmmünsüpresif Mikroçevre: Treg, MDSC, IDO ve Adenozin Yolağı",
        "subtitle": "FoxP3+ T hücreleri, miyeloid baskılayıcılar, triptofan tükenmesi ve metabolik kaçış",
        "badge": "İmmünsüpresif Stroma",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Tümör çevresi tam bir biyokimyasal bataklıktır. FoxP3+ Treg hücreleri ortamdaki tüm IL-2'yi emer, IDO enzimi triptofanı parçalayıp T hücresini aç bırakır, CD73 ise ATP'yi adenozine çevirip lenfositleri uyuşturur!",
            "note": "Prof. Dr. Hikmet Keleş, Treg'lerin CD25 reseptörüyle IL-2 tüketiminin ve IDO'nun triptofan yıkımının sınavların vazgeçilmez patofizyolojik tuzakları olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Tümör Mikroçevresinde İmmünosüpresif Ağ\n"
            "Malign neoplaziler sadece hücre yüzeyi kontrol noktalarıyla (PD-1, CTLA-4) yetinmezler; çevrelerinde bağışıklık hücrelerini felç eden "
            "çok katmanlı bir immünsüpresif hücre ve metabolik ortam ağı örerler.\n\n"
            "### 1. Düzenleyici T Hücreleri (Treg - CD4+ CD25+ FoxP3+)\n"
            "Tümörler CCL22 kemokini salarak **Treg** hücrelerini tümör içine davet ederler. Treg'ler üç ana mekanizmayla CTL'leri susturur:\n"
            "- **IL-2 Tüketimi (Sünger Etkisi):** Yüzeylerinde yüksek afiniteli IL-2 reseptörü alfa zinciri (**CD25**) taşırlar. Çevredeki tüm "
            "IL-2'yi adeta bir sünger gibi tüketirler; ortamda IL-2 kalmayınca efektör CD8+ CTL'ler enerji krizine girip apoptoza uğrar.\n"
            "- **Baskılayıcı Sitokinler:** Yoğun miktarda **TGF-beta** ve **IL-10** salgılayarak CTL ve dendritik hücre fonksiyonunu kilitlerler.\n"
            "- **CTLA-4 ile B7 Temizliği:** Konstitütif CTLA-4 ile dendritik hücrelerdeki B7'leri endositozla ortadan kaldırırlar.\n\n"
            "### 2. Miyeloid Kökenli Baskılayıcı Hücreler (MDSC - CD11b+ CD33+)\n"
            "Kemik iliğinde immatür kalmış myeloid öncüllerdir. Tümörün saldığı GM-CSF ve IL-6 ile aktive olurlar:\n"
            "- **Arjinaz-1 (Arg-1)** ve **iNOS** eksprese ederler. Mikroçevredeki L-arjinini tüketirler; L-arjinin tükenince T lenfositlerin "
            "**TCR zeta zinciri** sentezlenemez ve T hücresi antijenleri tanıyamaz hale gelir.\n\n"
            "### 3. Metabolik Baskılama: IDO ve Adenozin Yolu\n"
            "- **İndolamin 2,3-dioksijenaz (IDO):** Tümör hücreleri ve tolerojenik DC'ler tarafından salgılanır. T hücrelerinin hayatta "
            "kalması için esansiyel bir aminoasit olan **L-triptofanı** parçalayarak **kinürenine** dönüştürür. Triptofansız kalan T hücreleri "
            "G1 arrestine girip enerjisiz kalırken; biriken kinürenin T hücrelerinde apoptozu tetikler.\n"
            "- **CD39 ve CD73 Ektoenzimleri:** Tümör stromasındaki hücre ölümlerinden kaynaklanan ekstrasellüler ATP'yi parçalayarak "
            "**Adenozin** üretirler. Adenozin, T ve NK hücrelerindeki **A2A reseptörüne** bağlanarak hücre içi cAMP'yi artırır ve sitotoksik "
            "aktiviteyi tamamen felç eder.\n\n"
            "🔴 **ÖNEMLİ:** İndolamin 2,3-dioksijenaz (IDO) enzimi, T hücreleri için esansiyel olan triptofanı kinürenine yıkarak T lenfositlerini "
            "aç bırakır, prolifere olmalarını engeller ve apoptoza sokar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Tümör stromasında bulunan ve CD4+ CD25+ yüzey belirteçleri ile nükleer FoxP3 transkripsiyon faktörü taşıyarak "
            "antitümör yanıtı baskılayan lenfosit alt grubu Düzenleyici T hücreleridir (Treg)."
        ),
        "content": (
            "### Tümör Mikroçevresinde İmmünosüpresif Ağ\n"
            "Malign neoplaziler sadece hücre yüzeyi kontrol noktalarıyla (PD-1, CTLA-4) yetinmezler; çevrelerinde bağışıklık hücrelerini felç eden "
            "çok katmanlı bir immünsüpresif hücre ve metabolik ortam ağı örerler.\n\n"
            "### 1. Düzenleyici T Hücreleri (Treg - CD4+ CD25+ FoxP3+)\n"
            "Tümörler CCL22 kemokini salarak **Treg** hücrelerini tümör içine davet ederler. Treg'ler üç ana mekanizmayla CTL'leri susturur:\n"
            "- **IL-2 Tüketimi (Sünger Etkisi):** Yüzeylerinde yüksek afiniteli IL-2 reseptörü alfa zinciri (**CD25**) taşırlar. Çevredeki tüm "
            "IL-2'yi adeta bir sünger gibi tüketirler; ortamda IL-2 kalmayınca efektör CD8+ CTL'ler enerji krizine girip apoptoza uğrar.\n"
            "- **Baskılayıcı Sitokinler:** Yoğun miktarda **TGF-beta** ve **IL-10** salgılayarak CTL ve dendritik hücre fonksiyonunu kilitlerler.\n"
            "- **CTLA-4 ile B7 Temizliği:** Konstitütif CTLA-4 ile dendritik hücrelerdeki B7'leri endositozla ortadan kaldırırlar.\n\n"
            "### 2. Miyeloid Kökenli Baskılayıcı Hücreler (MDSC - CD11b+ CD33+)\n"
            "Kemik iliğinde immatür kalmış myeloid öncüllerdir. Tümörün saldığı GM-CSF ve IL-6 ile aktive olurlar:\n"
            "- **Arjinaz-1 (Arg-1)** ve **iNOS** eksprese ederler. Mikroçevredeki L-arjinini tüketirler; L-arjinin tükenince T lenfositlerin "
            "**TCR zeta zinciri** sentezlenemez ve T hücresi antijenleri tanıyamaz hale gelir.\n\n"
            "### 3. Metabolik Baskılama: IDO ve Adenozin Yolu\n"
            "- **İndolamin 2,3-dioksijenaz (IDO):** Tümör hücreleri ve tolerojenik DC'ler tarafından salgılanır. T hücrelerinin hayatta "
            "kalması için esansiyel bir aminoasit olan **L-triptofanı** parçalayarak **kinürenine** dönüştürür. Triptofansız kalan T hücreleri "
            "G1 arrestine girip enerjisiz kalırken; biriken kinürenin T hücrelerinde apoptozu tetikler.\n"
            "- **CD39 ve CD73 Ektoenzimleri:** Tümör stromasındaki hücre ölümlerinden kaynaklanan ekstrasellüler ATP'yi parçalayarak "
            "**Adenozin** üretirler. Adenozin, T ve NK hücrelerindeki **A2A reseptörüne** bağlanarak hücre içi cAMP'yi artırır ve sitotoksik "
            "aktiviteyi tamamen felç eder.\n\n"
            "🔴 **ÖNEMLİ:** İndolamin 2,3-dioksijenaz (IDO) enzimi, T hücreleri için esansiyel olan triptofanı kinürenine yıkarak T lenfositlerini "
            "aç bırakır, prolifere olmalarını engeller ve apoptoza sokar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Tümör stromasında bulunan ve CD4+ CD25+ yüzey belirteçleri ile nükleer FoxP3 transkripsiyon faktörü taşıyarak "
            "antitümör yanıtı baskılayan lenfosit alt grubu Düzenleyici T hücreleridir (Treg)."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** IDO enzimi triptofanı kinürenine yıkarak T lenfositlerini besinsiz bırakır ve apoptoza sevk eder.",
            "🔵 **ÇIKMIŞ SORU:** Düzenleyici T hücreleri (Treg) CD4+ CD25+ yüzey belirteçleri ve FoxP3 transkripsiyon faktörü ile tanımlanır; TGF-beta ve IL-10 salarlar.",
            "⚡ **METABOLİK:** CD39 ve CD73 ektoenzimleri hücre dışı ATP'yi parçalayıp adenozin üreterek A2A reseptörü üzerinden T hücrelerini felç eder."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Treg hücreleri yüksek afiniteli CD25 ile ortamdaki tüm IL-2'yi emerek efektör CD8+ CTL'leri sitokinsiz bırakır.",
            "🔵 **ÇIKMIŞ SORU:** MDSC hücreleri Arjinaz-1 ile L-arjinini tüketerek T hücrelerinin TCR zeta zinciri ekspresyonunu bozar.",
            "⚡ **METABOLİK:** Tümör stromasında TGF-beta artışı hem CTL sitotoksisitesini baskılar hem de fibroblastları uyararak desmoplazi yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "FoxP3+ Treg Hücreleri",
                    "desc": "CD25 ile IL-2'yi tüketir, TGF-beta ve IL-10 salarak antitümör sitotoksisiteyi kilitler.",
                    "isKey": True
                },
                {
                    "title": "MDSC ve Arjinin Yoksunluğu",
                    "desc": "Arg-1 enzimi ile ortamdaki arjinini tüketerek T hücre TCR zeta zinciri fonksiyonunu bozar.",
                    "isKey": True
                },
                {
                    "title": "IDO ve Adenozin Yolu",
                    "desc": "Triptofanın kinürenine yıkımı ve ATP'nin adenozine dönüşümü lenfositleri metabolik olarak felç eder.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Tümör Mikroçevresindeki Başlıca İmmünsüpresif Hücre ve Faktörler",
                "headers": ["Baskılayıcı Faktör", "Hücresel Kaynak", "Etki Mekanizması", "İmmünolojik Sonuç"],
                "rows": [
                    ["Treg (CD4+CD25+FoxP3+)", "Timus ve periferik indüklenmiş", "IL-2 tüketimi (CD25), TGF-beta ve IL-10 salınımı", "CTL proliferasyonunun durması ve apoptoz"],
                    ["MDSC (CD11b+CD33+)", "İmmatür myeloid öncüller", "Arjinaz-1 (Arg-1) ve iNOS ile L-arjinin tüketimi", "TCR zeta zinciri kaybı ve antijen tanıyamama"],
                    ["IDO Enzimi", "Tümör hücreleri, tolerojenik DC", "L-triptofanın kinürenine katabolizması", "T hücre G1 arresti ve kinürenin toksisitesi"],
                    ["CD39 / CD73 Eksen", "Tümör hücreleri ve endotel", "Ekstrasellüler ATP -> AMP -> Adenozin dönüşümü", "A2A reseptörü ile cAMP artışı ve sitotoksisite felci"],
                    ["TGF-beta", "Tümör, M2 TAM, fibroblastlar", "SMAD2/3 fosforilasyonu ile CTL ve NK inaktivasyonu", "İmmün felç ve desmoplastik stroma oluşumu"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-14-01",
                "category": "İmmünosüpresif Mikroçevre",
                "front": "Tümör hücrelerinde ekspresyonu artan İndolamin 2,3-dioksijenaz (IDO) enzimi T hücrelerini nasıl etkisiz hale getirir?",
                "hint": "Esansiyel bir aminoasidin yıkımı ve toksik metabolit.",
                "back": "T hücreleri için vazgeçilmez olan **L-triptofanı kinürenine yıkar**; T hücreleri triptofansız kalarak bölünemez ve biriken kinürenin etkisiyle apoptoza gider.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide IDO inhibitörlerinin yeni nesil immünoterapilerde denendiğini vurgulamıştır."
            },
            {
                "id": "imm-fc-14-02",
                "category": "Treg Biyolojisi",
                "front": "Düzenleyici T hücrelerinin (Treg) diğer T lenfositleri aç bırakarak öldürmesini sağlayan yüzey reseptörü hangisidir?",
                "hint": "Yüksek afiniteli IL-2 reseptör zinciri.",
                "back": "**CD25 (IL-2 reseptörü alfa zinciri)**. Ortamdaki tüm IL-2'yi tüketerek efektör CTL'leri sitokinsiz bırakır.",
                "facultyNote": "FoxP3 ve CD25, immünoloji ve patoloji sınavlarında Treg'lerin kardinal belirteçleridir."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-14",
            "question": "Pankreas duktal adenokarsinomu zemininde tümör mikroçevresi incelenen bir hastada, tümör dokusunda yoğun CD4+ CD25+ FoxP3+ hücreler ve yüksek düzeyde İndolamin 2,3-dioksijenaz (IDO) enzim aktivitesi tespit ediliyor. Bu mikroçevresel faktörlerin antitümör lenfositler üzerindeki etkisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) IDO enzimi triptofanı artırarak CD8+ sitotoksik T lenfositlerin litik granül salınımını uyarır.",
                "B) FoxP3+ hücreler IL-2 salgılayarak naif CD8+ T lenfositlerinin patlayıcı çoğalmasını sağlarlar.",
                "C) FoxP3+ hücreler yüksek afiniteli CD25 ile ortamdaki IL-2'yi tüketir; IDO ise esansiyel triptofanı parçalayarak T hücrelerini metabolik krize sokup apoptoza sürükler.",
                "D) IDO enzimi doğrudan DNA mismatch repair proteinlerini tamir ederek tümör mutasyon yükünü sıfırlar.",
                "E) Bu mikroçevre T hücrelerinde perforin gen transkripsiyonunu 10 kat artırarak tümörün nekrozuna yol açar."
            ],
            "answer": "C",
            "explanation": "Tümör mikroçevresindeki en güçlü immünosüpresif hücresel aktörler Düzenleyici T hücreleridir (Treg: CD4+ CD25+ FoxP3+). Treg'ler yüksek afiniteli IL-2 reseptörü (CD25) sayesinde çevredeki IL-2 sitokinini tüketerek CD8+ CTL'leri sitokinsiz bırakır, ayrıca TGF-beta ve IL-10 salarlar. İndolamin 2,3-dioksijenaz (IDO) ise T lenfositlerin yaşaması için zorunlu olan L-triptofanı parçalayarak kinürenine dönüştürür; triptofansız kalan efektör T hücreleri G1 arrestine ve apoptoza uğrar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 15
    {
        "slideNumber": 15,
        "title": "İmmünoonkolojide Terapötik Ufuklar: CAR-T, Aşılar ve Psödoprogresyon",
        "subtitle": "Genetiği değiştirilmiş T hücreleri, sitokin salınım sendromu (CRS) ve biyobelirteçler",
        "badge": "İmmünoterapi",
        "badgeColor": "cyan",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "CAR-T hücresi genetik mühendisliğin şaheseridir. T hücresine bir monoklonal antikorun gözünü takarsınız; MHC Sınıf I'e hiç ihtiyaç duymadan hedefi vurur! Ancak salınan IL-6 sitokin fırtınasına (CRS) dikkat etmeli, Tocilizumab'ı hazır tutmalısınız.",
            "note": "Prof. Dr. Hikmet Keleş, CAR-T hücrelerinin MHC-bağımsız hedef tanımasının ve immünoterapide görülen 'psödoprogresyon' olgusunun sınav tuzakları olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Kimerik Antijen Reseptör T Hücresi (CAR-T) Devrimi\n"
            "**CAR-T hücre tedavisi**, hastanın periferik kanından toplanan otolog T lenfositlerinin viral vektörler aracılığıyla genetik "
            "olarak yeniden programlanması esasına dayanır. Hücreye sentetik bir **Kimerik Antijen Reseptörü (CAR)** eklenir:\n"
            "- **Hücre Dışı Bölüm:** Bir monoklonal antikorun antijene bağlanan değişken fragmanından (**scFv**) oluşur.\n"
            "- **Hücre İçi Bölüm:** TCR'ın sinyal ileten **CD3-zeta** kuyruğu ile güçlü kostimülatör domainler (**4-1BB / CD137 veya CD28**) içerir.\n"
            "- **En Kritik Biyolojik Avantajı:** CAR-T hücreleri hedef antijeni **MHC Sınıf I MOLEKÜLÜNE İHTİYAÇ DUYMADAN DOĞRUDAN TANIR!** "
            "Böylece tümör hücresinin en büyük kaçış kozu olan MHC kaybı veya B2M mutasyonları tamamen etkisiz hale gelir.\n"
            "- **Klinik Başarı:** CD19 antijenini hedefleyen CAR-T (Tisagenlecleucel, Axicabtagene) refrakter **B-ALL ve B hücreli lenfomalarda** "
            "%80'in üzerinde tam remisyon sağlamaktadır.\n\n"
            "### CAR-T Toksisiteleri: Sitokin Salınım Sendromu (CRS) ve ICANS\n"
            "1. **Sitokin Salınım Sendromu (Cytokine Release Syndrome - CRS):** İnfüze edilen CAR-T hücrelerinin hedefi tanımasıyla tetiklenen "
            "kontrolsüz bir immün yanıttır. Özellikle makrofajlardan devasa miktarda **İnterlökin-6 (IL-6)**, IFN-γ ve TNF-alfa boşalır. "
            "Klinikte inatçı yüksek ateş, hipotansiyon, vasküler geçirgenlik artışı, şok ve multiorgan yetmezliği gelişir. Tedavide spesifik "
            "**IL-6 reseptör antagonisti Tocilizumab** ve kortikosteroidler kullanılır.\n"
            "2. **ICANS (İmmün Efektör Hücre İlişkili Nörotoksisite):** Konfüzyon, afazi, nöbet ve beyin ödemi ile seyreder.\n\n"
            "### Psödoprogresyon (Yalancı İlerleme) Fenomeni\n"
            "Kontrol noktası inhibitörü (Anti-PD-1) başlanan bir hastada ilk radyolojik değerlendirmede (BT/MRG) lezyonların belirgin "
            "olarak büyüdüğü veya yeni nodüllerin belirdiği görülebilir. Bu klinik durum gerçek bir tümör progresyonu değildir! İlacın "
            "etkisiyle tümör yatağına milyonlarca T lenfositinin hücum etmesi sonucu gelişen **yoğun lenfosit infiltrasyonu ve inflamatuar "
            "ödemdir**. Biyopside tümör hücrelerinin parçalandığı ve yerini lenfositlere bıraktığı görülür. Tedaviye devam edildiğinde kitle "
            "zamanla tamamen küçülür.\n\n"
            "🔴 **ÖNEMLİ:** CAR-T hücreleri hedef antijenleri MHC Sınıf I molekülüne İHTİYAÇ DUYMADAN doğrudan tanır; böylece tümörün "
            "MHC kaybı kaçış mekanizmasını tamamen baypas eder.\n\n"
            "🔵 **ÇIKMIŞ SORU:** CAR-T hücre tedavisinin en tehlikeli komplikasyonu olan Sitokin Salınım Sendromunda (CRS) ana medyatör "
            "İnterlökin-6'dır (IL-6) ve tedavisinde Tocilizumab kullanılır."
        ),
        "content": (
            "### Kimerik Antijen Reseptör T Hücresi (CAR-T) Devrimi\n"
            "**CAR-T hücre tedavisi**, hastanın periferik kanından toplanan otolog T lenfositlerinin viral vektörler aracılığıyla genetik "
            "olarak yeniden programlanması esasına dayanır. Hücreye sentetik bir **Kimerik Antijen Reseptörü (CAR)** eklenir:\n"
            "- **Hücre Dışı Bölüm:** Bir monoklonal antikorun antijene bağlanan değişken fragmanından (**scFv**) oluşur.\n"
            "- **Hücre İçi Bölüm:** TCR'ın sinyal ileten **CD3-zeta** kuyruğu ile güçlü kostimülatör domainler (**4-1BB / CD137 veya CD28**) içerir.\n"
            "- **En Kritik Biyolojik Avantajı:** CAR-T hücreleri hedef antijeni **MHC Sınıf I MOLEKÜLÜNE İHTİYAÇ DUYMADAN DOĞRUDAN TANIR!** "
            "Böylece tümör hücresinin en büyük kaçış kozu olan MHC kaybı veya B2M mutasyonları tamamen etkisiz hale gelir.\n"
            "- **Klinik Başarı:** CD19 antijenini hedefleyen CAR-T (Tisagenlecleucel, Axicabtagene) refrakter **B-ALL ve B hücreli lenfomalarda** "
            "%80'in üzerinde tam remisyon sağlamaktadır.\n\n"
            "### CAR-T Toksisiteleri: Sitokin Salınım Sendromu (CRS) ve ICANS\n"
            "1. **Sitokin Salınım Sendromu (Cytokine Release Syndrome - CRS):** İnfüze edilen CAR-T hücrelerinin hedefi tanımasıyla tetiklenen "
            "kontrolsüz bir immün yanıttır. Özellikle makrofajlardan devasa miktarda **İnterlökin-6 (IL-6)**, IFN-γ ve TNF-alfa boşalır. "
            "Klinikte inatçı yüksek ateş, hipotansiyon, vasküler geçirgenlik artışı, şok ve multiorgan yetmezliği gelişir. Tedavide spesifik "
            "**IL-6 reseptör antagonisti Tocilizumab** ve kortikosteroidler kullanılır.\n"
            "2. **ICANS (İmmün Efektör Hücre İlişkili Nörotoksisite):** Konfüzyon, afazi, nöbet ve beyin ödemi ile seyreder.\n\n"
            "### Psödoprogresyon (Yalancı İlerleme) Fenomeni\n"
            "Kontrol noktası inhibitörü (Anti-PD-1) başlanan bir hastada ilk radyolojik değerlendirmede (BT/MRG) lezyonların belirgin "
            "olarak büyüdüğü veya yeni nodüllerin belirdiği görülebilir. Bu klinik durum gerçek bir tümör progresyonu değildir! İlacın "
            "etkisiyle tümör yatağına milyonlarca T lenfositinin hücum etmesi sonucu gelişen **yoğun lenfosit infiltrasyonu ve inflamatuar "
            "ödemdir**. Biyopside tümör hücrelerinin parçalandığı ve yerini lenfositlere bıraktığı görülür. Tedaviye devam edildiğinde kitle "
            "zamanla tamamen küçülür.\n\n"
            "🔴 **ÖNEMLİ:** CAR-T hücreleri hedef antijenleri MHC Sınıf I molekülüne İHTİYAÇ DUYMADAN doğrudan tanır; böylece tümörün "
            "MHC kaybı kaçış mekanizmasını tamamen baypas eder.\n\n"
            "🔵 **ÇIKMIŞ SORU:** CAR-T hücre tedavisinin en tehlikeli komplikasyonu olan Sitokin Salınım Sendromunda (CRS) ana medyatör "
            "İnterlökin-6'dır (IL-6) ve tedavisinde Tocilizumab kullanılır."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** CAR-T hücreleri antijeni monoklonal antikor scFv ucuyla MHC-I bağımsız olarak tanır; MHC kaybı olan tümörlerde bile tam sitotoksisite sağlar.",
            "🔵 **ÇIKMIŞ SORU:** CAR-T ilişkili Sitokin Salınım Sendromunun (CRS) tedavisinde kullanılan anti-IL-6 reseptör monoklonal antikoru Tocilizumab'dır.",
            "⚡ **KLİNİK ONKOLOJİ:** İmmünoterapi sonrası tümörün radyolojik olarak geçici büyümesi 'Psödoprogresyon'dur; yoğun T lenfosit infiltrasyonu ve ödemden kaynaklanır."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** CAR reseptörünün hücre içi parçası CD3-zeta ve 4-1BB/CD28 kostimülatör domainlerini içerir.",
            "🔵 **ÇIKMIŞ SORU:** B-hücreli akut lenfoblastik lösemi tedavisinde en sık hedeflenen CAR-T antijeni CD19'dur.",
            "⚡ **KLİNİK ONKOLOJİ:** Psödoprogresyonda hastanın genel performans durumu iyidir, lezyondaki büyüme gerçek tümör artışı değildir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "MHC-Bağımsız Hedefleme",
                    "desc": "scFv antikoru sayesinde tümör antijenini MHC sunumuna ihtiyaç duymadan doğrudan tanıyıp yok eder.",
                    "isKey": True
                },
                {
                    "title": "Sitokin Salınım Sendromu (CRS)",
                    "desc": "IL-6 patlaması ile gelişen hayatı tehdit eden sistemik tablodur; Tocilizumab ile tedavi edilir.",
                    "isKey": True
                },
                {
                    "title": "Psödoprogresyon Algoritması",
                    "desc": "Tümör yatağına akın eden lenfositler kitleyi radyolojik olarak geçici büyütür; tedavi kesilmemelidir.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "CAR-T Hücre Tedavisi vs Klasik Checkpoint İnhibitörleri",
                "headers": ["Özellik", "CAR-T Hücre Tedavisi", "Kontrol Noktası İnhibitörleri (Anti-PD-1)"],
                "rows": [
                    ["Uygulanan Ajan", "Genetiği değiştirilmiş canlı T hücreleri", "Monoklonal antikor proteini (ilaç)"],
                    ["MHC Sınıf I Bağımlılığı", "MHC'den TAMAMEN BAĞIMSIZDIR", "MHC Sınıf I varlığına KESİNLİKLE BAĞIMLIDIR"],
                    ["B2M Kaybında Etki", "Etkilenmez, tümörü öldürmeyi sürdürür", "Etkisiz kalır (direnç gelişir)"],
                    ["En Sık Kullanıldığı Alan", "Hematolojik maligniteler (B-ALL, Lenfoma)", "Solid tümörler (Melanom, KHDAK, Böbrek Ca)"],
                    ["Başlıca Toksisite", "Sitokin Salınım Sendromu (IL-6), ICANS", "Otoimmünite benzeri olaylar (Kolit, Hipofizit)"],
                    ["Toksisite Antidotu", "Tocilizumab (Anti-IL-6R), Steroid", "Sistemik yüksek doz Kortikosteroidler"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-15-01",
                "category": "CAR-T Biyolojisi",
                "front": "CAR-T hücrelerinin klasik endojen CD8+ T lenfositlerine kıyasla en üstün biyolojik avantajı nedir?",
                "hint": "MHC Sınıf I bağımlılığı.",
                "back": "Hedef tümör antijenini **MHC Sınıf I molekülüne ihtiyaç duymadan doğrudan** tanımasıdır; tümör MHC-I'i kaybetse bile öldürür.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide CAR-T'nin MHC bağımsızlığının sınavda mutlaka sorulacağını belirtmiştir."
            },
            {
                "id": "imm-fc-15-02",
                "category": "Onkolojik Yanıt",
                "front": "İmmün kontrol noktası inhibitörü başlanan bir hastada ilk ay kontrolünde tümörün büyümesi durumunda ne düşünülmelidir?",
                "hint": "Yalancı progresyon ve lenfosit hücumu.",
                "back": "**Psödoprogresyon (Yalancı İlerleme)**. Tümör dokusuna yoğun T lenfosit akını ve oluşan inflamatuar ödem nedeniyle kitle geçici olarak büyük görünür.",
                "facultyNote": "Radyolojide iRECIST kriterleri psödoprogresyonu gerçek tümör progresyonundan ayırmak için kullanılır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-15",
            "question": "Refrakter B hücreli akut lenfoblastik lösemi (B-ALL) nedeniyle CD19 hedefli CAR-T hücre infüzyonu yapılan 22 yaşındaki bir hastada infüzyondan 5 gün sonra 39.8°C ateş, taşikardi, hipotansiyon ve dispne gelişiyor. Laboratuvarda serum ferritin ve İnterlökin-6 (IL-6) düzeylerinin devasa yükseldiği saptanıyor. Bu hastanın klinik tablosu ve tedavisi ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) Hastada graft-versus-host hastalığı gelişmiştir; acil radyoterapi uygulanmalıdır.",
                "B) CAR-T hücrelerinin tümör hücrelerini öldüremediğini ve löseminin blastik krize girdiğini gösterir.",
                "C) Tablo Sitokin Salınım Sendromudur (CRS); patogenezinde IL-6 başroldedir ve tedavisinde IL-6 reseptör antagonisti Tocilizumab kullanılır.",
                "D) Hastaya acilen yüksek doz IL-2 infüzyonu verilerek CAR-T hücreleri uyarılmalıdır.",
                "E) Yalnızca hafif bir alerjik reaksiyondur, antihistaminik verilip taburcu edilmelidir."
            ],
            "answer": "C",
            "explanation": "Kimerik Antijen Reseptör T hücresi (CAR-T) infüzyonunun en sık ve en tehlikeli komplikasyonu Sitokin Salınım Sendromudur (CRS). İnfüze edilen T hücrelerinin ve aktive olan makrofajların devasa miktarda inflamatuar sitokin (özellikle İnterlökin-6 / IL-6, TNF-alfa ve IFN-gama) salgılamasıyla ortaya çıkar; yüksek ateş, vasküler kollaps ve şokla seyreder. Tedavisinde spesifik monoklonal anti-IL-6 reseptör antikoru olan Tocilizumab ve sistemik kortikosteroidler hayat kurtarıcıdır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    }
]
