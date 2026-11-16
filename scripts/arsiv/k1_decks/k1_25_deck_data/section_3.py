# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 3: Tip IV (Hücresel / T Lenfosit Aracılı) Hipersensitivite ve Doku Hasarı (Slayt 21 - 30)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # Slayt 21: Tip IV Hipersensitivite: Genel Tanım ve İki Temel Yolak
    slides.append({
        "id": "k1-25-s21",
        "title": "Tip IV Hipersensitivite: Genel Tanım ve İki Temel Yolak",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 21,
        "narrative": (
            "Tip IV aşırı duyarlılık, antikorlardan tamamen bağımsız olarak doğrudan antijene duyarlı hale gelmiş "
            "**T lenfositleri** tarafından yürütülen hücresel bağışıklık reaksiyonudur: "
            "1. **Zaman Penceresi (Gecikmiş Tip):** Antijenle temastan sonra lezyonların ortaya çıkması ve doruğa ulaşması "
            "genellikle **24 ile 48 saat (bazen 72 saat)** sürer; bu nedenle 'Gecikmiş Tip Aşırı Duyarlılık (DTH)' olarak da adlandırılır. "
            "2. **İki Temel Efektör Yolak:** "
            "- **Yolak 1 (CD4+ T Hücre Aracılı Sitokin Hasarı):** Antijen sunumuyla aktive olan CD4+ Th1 ve Th17 lenfositleri "
            "sitokinler salgılar; dokuya masif makrofaj ve nötrofil akını sağlayarak kronik inflamasyon ve nekroz oluşturur. "
            "- **Yolak 2 (CD8+ Sitotoksik T Lenfosit / CTL Hasarı):** CD8+ T hücreleri hedef hücrelerin yüzeyindeki MHC Sınıf I "
            "bağlı antijenleri tanır; perforin ve granzim salarak hedef hücreyi doğrudan apoptoza sürükler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tip IV Hipersensitivitenin İki Temel Efektör Kolu",
                ["Efektör T Hücre Tipi", "Tanınan MHC Molekülü", "Temel Efektör Mekanizma", "Tipik Patolojik Lezyon"],
                [
                    ["CD4+ T Lenfositleri (Th1 / Th17)", "MHC Sınıf II", "IFN-gama ve IL-17 ile makrofaj/nötrofil aktivasyonu", "DTH, kontakt dermatit, granülomlar"],
                    [
                        "CD8+ Sitotoksik T Lenfositleri (CTL)",
                        "MHC Sınıf I",
                        {"text": "Perforin, granzim ve FasL apoptozu", "isMasked": True, "hint": "Hedef hücre zarını delip kaspazları aktive eden mekanizma"},
                        "Viral hepatit (Councilman cisimleri), Tip 1 DM"
                    ]
                ]
            ),
            make_active_recall(
                "Tip IV aşırı duyarlılık reaksiyonlarında antijenle temastan sonra doku reaksiyonunun klinik ve histopatolojik olarak doruğa ulaştığı tipik saat aralığı nedir?",
                "24 ile 48 saat (gecikmiş tip yanıt) aralığıdır.",
                "T hücrelerinin dokuya göçü ve makrofaj aktivasyonu için gereken süre penceresi"
            )
        ]
    })

    # Slayt 22: CD4+ Th1 ve Th17 Yolakları: Sitokin Profili ve Makrofaj Aktivasyonu
    slides.append({
        "id": "k1-25-s22",
        "title": "CD4+ Th1 ve Th17 Yolakları: Sitokin Profili ve Makrofaj Aktivasyonu",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 22,
        "narrative": (
            "CD4+ T hücre aracılı aşırı duyarlılıkta doku hasarının niteliği üretilen sitokin alt tipleriyle belirlenir: "
            "1. **Th1 Yolağı ve Makrofaj Aktivasyonu:** Dendritik hücrelerden salınan IL-12 etkisiyle naif T hücreleri **Th1**'e farklılaşır. "
            "Th1 hücreleri masif miktarda **İnterferon-gama (IFN-gama)** üretir. IFN-gama, monositleri **klasik aktive makrofajlara (M1)** "
            "dönüştürür; makrofajların fagositoz gücü, fagozom içi reaktif oksijen radikali (ROS), nitrik oksit (NO) ve lizozomal enzim "
            "sentezi tavan yapar. Ortaya çıkan makrofaj kaynaklı TNF ve IL-1 inflamasyonu daha da büyütür. "
            "2. **Th17 Yolağı ve Nötrofil Akını:** IL-1, IL-6 ve IL-23 etkisiyle gelişen **Th17** hücreleri **IL-17 ve IL-22** salgılar. "
            "IL-17 kemokin üretimini artırarak dokuya yoğun nötrofil göçü sağlar; pürülan ve nekrotik doku hasarını derinleştirir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Th1 ve M1 Makrofaj Aktivasyon Yolağı",
                [
                    "1. Antijen Sunumu: Dendritik hücrelerin antijeni MHC-II üzerinde naif CD4+ T hücresine sunması",
                    "2. Th1 İndüksiyonu: IL-12 uyarımıyla T-bet transkripsiyon faktörünün aktive olup Th1'e dönüşüm",
                    "3. IFN-gama Salınımı: Th1 lenfositlerinden masif İnterferon-gama sentezlenmesi",
                    "4. M1 Dönüşümü: Doku makrofajlarının aktive olup fagositoz, NO ve lizozom kusmasıyla dokuyu yıkması"
                ]
            ),
            make_cloze(
                "Tip IV gecikmiş tip aşırı duyarlılıkta makrofajları klasik aktive M1 fenotipine dönüştüren temel Th1 sitokini IFN-gama molekülüdür.",
                "IFN-gama",
                "Makrofaj fagositozunu ve granülom gelişimini başlatan anahtar interferon"
            )
        ]
    })

    # Slayt 23: Gecikmiş Tip Aşırı Duyarlılık Prototipi: Tüberkülin (PPD) Testi
    slides.append({
        "id": "k1-25-s23",
        "title": "Gecikmiş Tip Aşırı Duyarlılık Prototipi: Tüberkülin (PPD) Testi",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 23,
        "narrative": (
            "Tüberkülin (Mantoux / PPD) deri testi, insan vücudunda DTH mekanizmasının kusursuz klinik modelidir: "
            "1. **Uygulama:** Mycobacterium tuberculosis protein türevi (PPD), önceden tüberküloz basiliyle karşılaşmış veya "
            "BCG aşısı olmuş bireyin ön kol derisi içine (intradermal) enjekte edilir. "
            "2. **Histopatolojik Gelişim:** "
            "- İlk saatlerde antijen sunucu hücreler PPD'yi yakalar. Dolaşımdaki hafıza T hücreleri deriye göçer. "
            "- **8 - 12. Saatler:** Dermis postkapiller venülleri çevresinde lenfosit ve makrofajlardan oluşan "
            "karakteristik **perivasküler manşonlaşma (cuffing)** başlar. Endotel hücreleri şişer, mikrovasküler geçirgenlik artar. "
            "- **24 - 72. Saatler (Doruk):** Dermis yoğun lenfomononükleer infiltrat ve fibrin eksüdasıyla dolar. "
            "3. **Klinik Değerlendirme:** Test yerinde eritem değil, parmakla hissedilen sert kabarıklık (**indürasyon**) milimetre olarak ölçülür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tüberkülin (PPD) Reaksiyonunun Zaman Çizelgesi ve Histolojisi",
                ["Zaman Penceresi", "Hücresel Olaylar", "Histopatolojik Mikroskopi", "Klinik Muayene Bulgusu"],
                [
                    ["0 - 6. Saat", "PPD antijeninin dermise dağılması", "Minimal nonspesifik nötrofil geçişi", "Enjeksiyon iğne izi dışında sessiz"],
                    [
                        "12 - 24. Saat",
                        "Hafıza CD4+ T hücrelerinin göçü",
                        {"text": "Perivasküler lenfosit manşonlaşması (cuffing)", "isMasked": True, "hint": "Venüller çevresinde lenfositlerin yüzük şeklinde dizilmesi"},
                        "Hafif eritem ve yumuşak ödem"
                    ],
                    ["48 - 72. Saat (Tepe)", "Masif IFN-gama ve makrofaj aktivasyonu", "Dermiste yoğun mononükleer infiltrat ve fibrin", "Sert, palpe edilebilen indürasyon nodülü"]
                ]
            ),
            make_active_recall(
                "Tüberkülin (PPD) deri testinin mikroskobik incelemesinde dermisteki postkapiller venüller çevresinde lenfosit ve makrofajların oluşturduğu tipik histolojik manzaraya ne ad verilir?",
                "Perivasküler manşonlaşma (perivascular cuffing) denir.",
                "Damarlar çevresinde hücrelerin kolluk veya manşet tarzında toplanması"
            )
        ]
    })

    # Slayt 24: Kontakt Dermatit Patolojisi ve Hapten-Taşıyıcı Mekanizması
    slides.append({
        "id": "k1-25-s24",
        "title": "Kontakt Dermatit Patolojisi ve Hapten-Taşıyıcı Mekanizması",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 24,
        "narrative": (
            "Alerjik kontakt dermatit, deriye temas eden küçük kimyasal maddelerin tetiklediği klasik bir epidermal Tip IV reaksiyonudur: "
            "1. **Hapten Kavramı:** Nikel (saat, kemer tokası, takılar), zehirli sarmaşık toksini (urushiol), kozmetikler ve topikal ilaçlar "
            "düşük molekül ağırlıklı **haptenlerdir**. Tek başlarına immün yanıt başlatamazlar; ancak epidermis proteinlerine kovalent "
            "bağlandıklarında bağışıklık sistemi tarafından yabancı olarak algılanan tam antijen komplekslerine dönüşürler. "
            "2. **Sensitizasyon ve Efektör Faz:** Epidermisteki dendritik hücreler (**Langerhans hücreleri**) hapten-protein kompleksini "
            "fagositozla alır, lenf noduna taşır ve CD4+/CD8+ T hücrelerini duyarlılaştırır. "
            "3. **Histopatoloji (Spongiyoz):** Aynı maddeyle tekrar temasta 24-48 saat sonra T hücreleri sitokin salar. Epidermis hücreleri "
            "arasında sıvı birikerek hücreleri ayırır (**spongiyoz / intersellüler ödem**) ve klinik olarak kaşıntılı intraepidermal veziküller oluşur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Normal Epidermis vs Kontakt Dermatit Histopatolojisi",
                "Sağlıklı Epidermis",
                "Birbirine desmozomlarla sıkı sıkıya bağlı keratinositler, kuru stratum korneum ve intakt bazal membran",
                "Alerjik Kontakt Dermatit",
                "Keratinositler arasında masif sıvı toplanması (spongiyoz), mikroveziküller ve dermiste lenfosit infiltratı"
            ),
            make_micro_quiz(
                "Nikel içeren bir saat taktıktan 48 saat sonra bileğinde kaşıntılı, eritematöz veziküller gelişen bir hastanın deri biyopsisinde epidermiste keratinositler arasında sıvı toplanmasıyla karakterize histopatolojik bulgu hangisidir?",
                {
                    "A": "Spongiyoz (intersellüler epidermal ödem)",
                    "B": "Hiperkeratoz ve granüler tabaka kalınlaşması",
                    "C": "Subdermal lipomatoz nekrozu",
                    "D": "Damar duvarında fibrinoid nekroz",
                    "E": "Papiller dermiste multinükleer Langhans dev hücreleri"
                },
                "A",
                {
                    "A": "Doğrudur; kontakt dermatitin karakteristik histopatolojik bulgusu epidermiste hücreler arası ödem olan spongiyozdur.",
                    "B": "Yanlış; hiperkeratoz kronik sürtünmede görülür.",
                    "C": "Yanlış; lipomatoz yağ dokusu patolojisidir.",
                    "D": "Yanlış; fibrinoid nekroz Tip III vaskülitine özgüdür.",
                    "E": "Yanlış; Langhans hücreleri granülomlarda bulunur."
                }
            )
        ]
    })

    # Slayt 25: Granülomatöz İnflamasyon: Kronik DTH'nin Histopatolojik Zirvesi
    slides.append({
        "id": "k1-25-s25",
        "title": "Granülomatöz İnflamasyon: Kronik DTH'nin Histopatolojik Zirvesi",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 25,
        "narrative": (
            "Dokuya giren antijen sindirilemez veya vücuttan temizlenemezse, gecikmiş tip aşırı duyarlılık granülomatöz inflamasyona evrilir: "
            "1. **Tetikleyici Etkenler:** Mycobacterium tuberculosis (tüberküloz), Mycobacterium leprae (lepra), mantarlar (Histoplazmoz), "
            "çözünmeyen inorganik partiküller (berilyum, silika) veya etyolojisi bilinmeyen sarkoidozdur. "
            "2. **Epiteloid Histiyosit Dönüşümü:** Th1 hücrelerinin aralıksız salgıladığı **İnterferon-gama (IFN-gama)** uyarımıyla "
            "makrofajlar devleşir; bol eozinofilik pembe sitoplazmalı, sınırları silik, terlik biçimli çekirdeğe sahip **epiteloid histiyositlere** dönüşür. "
            "3. **Langhans Dev Hücreleri:** Epiteloid histiyositler birbirleriyle kaynaşarak nükleusları periferde at nalı şeklinde dizilmiş "
            "**Langhans tipi multinükleer dev hücreleri** oluşturur. "
            "4. **Kazeifikasyon Nekrozu:** Tüberküloz granülomunun merkezinde hipoksi ve toksik mediyatörlerle peynirimsi **kazeöz nekroz** gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Granülomatöz İnflamasyonun Histolojik Mimarisi",
                ["Granülom Zonu", "Baskın Hücre Tipi", "Morfolojik Özellik", "İmmünolojik Rolü"],
                [
                    ["Santral Çekirdek", "Nekrotik debris (Kazeifikasyon)", "Asellüler, granüler pembe peynirimsi erime", "Basillerin hapsolduğu hipoksik nekroz"],
                    [
                        "Ara Hücresel Tabaka",
                        "Epiteloid histiyositler",
                        {"text": "Bol eozinofilik sitoplazma, terlik çekirdek", "isMasked": True, "hint": "IFN-gama ile aktive olup epitele benzeyen modifiye makrofajlar"},
                        "Antijenin yayılmasını fiziksel sınırlama"
                    ],
                    ["Dev Hücreler", "Langhans dev hücreleri", "At nalı şeklinde dizilmiş çoklu çekirdekler", "Makrofaj füzyonuyla oluşan dev yapılar"],
                    ["Dış Kuşak", "T lenfositleri (CD4+ Th1)", "Yoğun mononükleer lenfositik taç", "Sürekli sitokin (IFN-gama) pompalanması"]
                ]
            ),
            make_active_recall(
                "Tüberküloz granülomlarında epiteloid histiyositlerin birbirleriyle kaynaşması sonucu oluşan ve çekirdekleri at nalı biçiminde dizilen dev hücreye ne ad verilir?",
                "Langhans tipi dev hücre denir.",
                "Periferik çekirdek dizilimli granülomatöz multinükleer histiyositik hücre"
            )
        ]
    })

    # Slayt 26: CD8+ Sitotoksik T Lenfosit (CTL) Aracılı Doku Hasarı
    slides.append({
        "id": "k1-25-s26",
        "title": "CD8+ Sitotoksik T Lenfosit (CTL) Aracılı Doku Hasarı",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 26,
        "narrative": (
            "Tip IV aşırı duyarlılığın ikinci kolu, antijen taşıyan konak hücrelerinin doğrudan CD8+ T lenfositlerince öldürülmesidir: "
            "1. **MHC Sınıf I Tanıması:** Viral enfeksiyonlarda veya tümörlerde hücre içinde üretilen peptitler hücre zarında **MHC Sınıf I** "
            "molekülleriyle sunulur. CD8+ CTL'ler bu kompleksi T hücre reseptörü (TCR) ile tanır. "
            "2. **İkili İnfaz Mekanizması:** "
            "- **Perforin ve Granzim Yolağı:** CTL'ler hedef hücre zarına temas eder; salgılanan **perforin** hedef zarında silindirik "
            "delikler açar. Deliklerden içeri giren nötral serin proteaz **Granzim B**, prokaspaz-3'ü parçalayarak kaspaz kaskadını "
            "ve mitokondriyal DNA fragmantasyonunu başlatır. "
            "- **FasL / Fas Yolağı:** CTL üzerindeki FasL, hedefteki Fas (CD95) reseptörünü çapraz bağlayarak kaspaz-8'i doğrudan uyarır. "
            "3. **Klinik Örnek:** Viral hepatitte CTL'lerin enfekte hepatositleri öldürmesiyle ortaya çıkan büzüşmüş eozinofilik kürelere "
            "**Councilman cisimcikleri (apoptotik cisimcikler)** denir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "CD8+ CTL Hedef Hücre İnfaz Zinciri",
                [
                    "1. TCR - MHC I Kenetlenmesi: Sitotoksik T hücresinin viral antijen yüklü hedef hücreye bağlanması",
                    "2. Polarize Granül Salınımı: CTL lizozom benzeri granüllerinin hücre temas yüzeyine boşalması",
                    "3. Perforin Gözenekleri: Hedef plazma membranında delikler açılması ve içeri granzim B sızması",
                    "4. Kaspaz Kaskadı ve Apoptoz: DNA parçalanması, hücre büzüşmesi ve Councilman cismi oluşumu"
                ]
            ),
            make_cloze(
                "Viral hepatitte CD8+ sitotoksik T lenfositlerinin perforin ve granzim salarak hepatositleri apoptoza uğratması sonucu oluşan apoptotik yapılara Councilman cisimciği denir.",
                "Councilman",
                "Karaciğer biyopsisinde görülen büzüşmüş eozinofilik apoptotik hepatosit kalıntısı"
            )
        ]
    })

    # Slayt 27: Tip IV Zemininde Gelişen Otoimmün Hastalıklar
    slides.append({
        "id": "k1-25-s27",
        "title": "Tip IV Zemininde Gelişen Otoimmün Hastalıklar",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 27,
        "narrative": (
            "Kendi doku antijenlerine karşı tolerans çöktüğünde CD4+ ve CD8+ T lenfositleri kronik otoimmün organ yıkımına yol açar: "
            "1. **Tip 1 Diabetes Mellitus:** Pankreas Langerhans adacıklarındaki insülin üreten **beta hücrelerine** karşı otoantijenik "
            "T hücreleri aktive olur. Adacıklara CD4+ ve CD8+ lenfositler hücum eder (**insülit**); beta hücreleri selektif olarak "
            "yok edilir ve mutlak insülin yetersizliğiyle diyabet başlar. "
            "2. **Multipl Skleroz (MS):** Santral sinir sistemi miyelin kılıf bileşenlerine (**Miyelin Bazik Protein / MBP**) karşı "
            "Th1 ve Th17 lenfositleri kan-beyin bariyerini geçer. Makrofajlar miyelini soyar; aksonal iletim durur, sklerotik plaklar gelişir. "
            "3. **Romatoid Artrit (RA):** Eklem sinovyasında Th1 ve Th17 lenfositleri toplanır. Salınan TNF, IL-1 ve RANKL; osteoklastları "
            "ve sinovyal fibroblastları aşırı uyarır. Kalınlaşan sinovya eklem kıkırdağını eriten granülasyon dokusuna (**pannus**) dönüşür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tip IV Aracılı Otoimmün Hastalıklar ve Hedef Dokular",
                ["Otoimmün Hastalık", "Hedef Hücre / Doku Antijeni", "Efektör T Hücre Mekanizması", "Histopatolojik Sonuç"],
                [
                    ["Tip 1 Diabetes Mellitus", "Pankreas beta hücre antijenleri", "CD8+ CTL sitotoksisitesi ve Th1 sitokinleri", "Adacıklarda insülit ve beta hücre kaybı"],
                    [
                        "Multipl Skleroz (MS)",
                        "Miyelin bazik protein ve proteolipid",
                        {"text": "Th1/Th17 kaynaklı makrofajik demiyelinizasyon", "isMasked": True, "hint": "Beyin ve medulla spinaliste akson kılıflarının eritilmesi"},
                        "Beyaz cevherde sklerotik demiyelinizan plaklar"
                    ],
                    ["Romatoid Artrit", "Sinovyal sitrülinlenmiş proteinler", "Th17/IL-17 osteoklast aktivasyonu", "Sinovyal hipertrofi, pannus ve kemik erozyonu"],
                    ["Crohn Hastalığı", "Bağırsak mikrobiyota antijenleri", "Th1/Th17 aracılı transmural inflamasyon", "Kazeifiye olmayan granülomlar, striktürler"]
                ]
            ),
            make_active_recall(
                "Tip 1 diyabet patogenezinde pankreas Langerhans adacıklarına lenfositlerin göç ederek beta hücrelerini yok etmesi sürecine verilen histopatolojik ad nedir?",
                "İnsülit tablosudur.",
                "Pankreas endokrin adacıklarının lenfositik inflamasyonu"
            )
        ]
    })

    # Slayt 28: Hipersensitivite Tipleri Karşılaştırmalı Büyük Matrisi
    slides.append({
        "id": "k1-25-s28",
        "title": "Hipersensitivite Tipleri Karşılaştırmalı Büyük Matrisi",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 28,
        "narrative": (
            "Dört aşırı duyarlılık tipinin temel immünolojik ve patolojik ilkelerini tek bir matriste özetliyoruz: "
            "1. **Tip I (Ani):** Çözünür alerjen + IgE + Mast hücresi -> Histamin ve lökotrienler -> Vazodilatasyon ve bronkospazm (Dakikalar). "
            "2. **Tip II (Antikor Aracılı):** Sabit hücre/matriks antijeni + IgG/IgM -> Opsonizasyon, kompleman lizisi veya reseptör disfonksiyonu. "
            "3. **Tip III (İmmün Kompleks):** Dolaşan çözünür antijen + IgG/IgM -> Damara çöken orta boy kompleksler -> Kompleman ve nötrofil aktivasyonu -> Fibrinoid nekroz. "
            "4. **Tip IV (Hücresel):** Antijen + CD4+ Th1/Th17 veya CD8+ CTL -> IFN-gama ve makrofaj aktivasyonu (DTH/granülom) veya direkt perforin/granzim apoptozu (24-48 Saat)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Coombs ve Gell Hipersensitivite Büyük Karşılaştırma Matrisi",
                ["Tip", "İmmün Mediyatör", "Antijenin Özelliği", "Histopatoloji", "Prototip Hastalıklar"],
                [
                    ["Tip I", "IgE", "Çözünür çevresel alerjen", "Ödem, mukus, eozinofil", "Astım, saman nezlesi, anafilaksi"],
                    ["Tip II", "IgG, IgM", "Sabit hücre/matriks yüzeyi", "Hücre lizisi, lineer immünofloresan", "Goodpasture, AIHA, Pemfigus, Myastenia"],
                    [
                        "Tip III",
                        "IgG, IgM (Kompleks)",
                        {"text": "Kanda dolaşan serbest antijen", "isMasked": True, "hint": "Kanda antikorla birleşip sonra filtre olan antijen"},
                        "Fibrinoid nekroz, granüler floresan",
                        "Serum hastalığı, SLE nefriti, Arthus"
                    ],
                    ["Tip IV", "T lenfositleri", "Hücresel veya kimyasal antijen", "Perivasküler manşon, granülom, spongiyoz", "PPD, kontakt dermatit, Tüberküloz, Tip 1 DM"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki eşleştirmelerden hangisi Coombs ve Gell sınıflamasına göre patolojik mekanizma ve prototip hastalık açısından YANLIŞTIR?",
                {
                    "A": "Tip I - Mast hücresi ve IgE - Sistemik anafilaksi",
                    "B": "Tip II - Tip IV kollajene karşı lineer antikor - Goodpasture sendromu",
                    "C": "Tip III - Dolaşan immün kompleksler - Akut serum hastalığı",
                    "D": "Tip IV - CD4+ ve CD8+ T lenfositleri - Tüberkülin (PPD) reaksiyonu",
                    "E": "Tip II - Dolaşan antijen-antikor çökmesi - Poststreptokoksik glomerülonefrit"
                },
                "E",
                {
                    "A": "Doğrudur; Tip I IgE ve mast hücre degranülasyonudur.",
                    "B": "Doğrudur; Goodpasture Tip II antikor aracılı doku hasarıdır.",
                    "C": "Doğrudur; serum hastalığı Tip III prototipidir.",
                    "D": "Doğrudur; PPD testi Tip IV DTH prototipidir.",
                    "E": "YANLIŞTIR; Poststreptokoksik glomerülonefrit Tip II DEĞİL, dolaşan komplekslerin glomerüle çökmesiyle oluşan TİP III reaksiyonudur."
                }
            )
        ]
    })

    # Slayt 29: Checkpoint 3
    slides.append({
        "id": "k1-25-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Tip IV Aşırı Duyarlılık ve Granülomatöz Yanıt",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 29,
        "narrative": (
            "Bu üçüncü kontrol noktasında, Tip IV hücresel aşırı duyarlılık mekanizmalarını pekiştiriyoruz: "
            "1. **Antikorsuz Mekanizma:** Tamamen T hücreleri (CD4+ Th1/Th17 ve CD8+ CTL) tarafından yürütülür; tepe noktası 24-48 saattir. "
            "2. **Th1 ve Makrofaj:** Th1 hücreleri IFN-gama salgılar; monositler klasik M1 makrofajlara dönüşerek dokuyu eritir. "
            "3. **Tüberkülin (PPD):** Histolojide venüller çevresinde perivasküler manşonlaşma (cuffing) ve dermiste sert indürasyon izlenir. "
            "4. **Kontakt Dermatit:** Nikel/urushiol gibi haptenlerin epidermis proteinlerine bağlanmasıyla gelişir; histolojisi spongiyozdur. "
            "5. **Granülomatöz Yanıt:** Kronik IFN-gama uyarımıyla makrofajlar epiteloid histiyositlere ve Langhans dev hücrelerine dönüşür. "
            "6. **CD8+ CTL Sitotoksisitesi:** Perforin delik açar, granzim kaspazları tetikler; viral hepatitte Councilman cisimleri oluşur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s29-1",
                "Alerjik kontakt dermatit histopatolojisinde epidermisteki keratinositlerin arasına sıvı sızması sonucu gelişen intersellüler ödeme ne ad verilir?",
                "Spongiyoz tablosudur.",
                "Epidermal hücreler arasında süngerimsi sıvı toplanması manzarası",
                "Spongiyoz"
            ),
            make_flashcard(
                "k1-25-fc-s29-2",
                "CD8+ sitotoksik T lenfositlerinin hedef hücre membranında delikler açarak hücre içi kaspaz aktivasyonunu sağlayan iki temel granül proteini nedir?",
                "Perforin ve granzim molekülleridir.",
                "Gözenek açıcı polipeptit ve kaspaz parçalayıcı serin proteaz",
                "Perforin ve Granzim"
            ),
            make_flashcard(
                "k1-25-fc-s29-3",
                "Tip IV gecikmiş tip aşırı duyarlılık zemininde gelişen tüberküloz granülomlarında epiteloid histiyosit dönüşümünü başlatan temel sitokin hangisidir?",
                "İnterferon-gama (IFN-gama) molekülüdür.",
                "Th1 lenfositlerinden salgılanan primer makrofaj aktive edici faktör",
                "IFN-gama ve Granülom"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tip IV Hipersensitivite Checkpoint Matrisi",
                ["Klinik Form", "Tetikleyici Antijen", "Temel Hücresel Oyuncular", "Histopatolojik Anahtar"],
                [
                    ["Tüberkülin (PPD)", "Tüberküloz mikobakteri proteini", "CD4+ Th1 ve M1 makrofajlar", "Perivasküler manşonlaşma (cuffing)"],
                    ["Kontakt Dermatit", "Nikel, urushiol (Hapten)", "Langerhans hücreleri ve T hücreleri", "Epidermal spongiyoz ve vezikül"],
                    [
                        "Tüberküloz Granülomu",
                        "Sindirim dirençli mikobakteri",
                        {"text": "Epiteloid histiyosit ve Langhans hücresi", "isMasked": True, "hint": "Kronik IFN-gama uyarısıyla modifiye olan makrofajlar"},
                        "Kazeöz nekrozlu granülom"
                    ],
                    ["Viral Hepatit Hasarı", "HBV / HCV viral peptitleri", "CD8+ sitotoksik T hücreleri", "Councilman apoptotik cisimcikleri"]
                ]
            ),
            make_micro_quiz(
                "Viral hepatitte CD8+ sitotoksik T lenfositlerinin enfekte hepatositleri apoptoza uğratmasıyla oluşan eozinofilik apoptotik cisimciklere ne ad verilir?",
                {
                    "A": "Councilman cisimcikleri",
                    "B": "Aschoff cisimcikleri",
                    "C": "Mallory-Denk cisimcikleri",
                    "D": "Lewy cisimcikleri",
                    "E": "Russell cisimcikleri"
                },
                "A",
                {
                    "A": "Doğrudur; Councilman cisimcikleri CTL kaynaklı apoptotik hepatosit kalıntılarıdır.",
                    "B": "Yanlış; Aschoff cisimcikleri romatizmal karditte görülür.",
                    "C": "Yanlış; Mallory-Denk alkolik karaciğerde sitokeratin yığılımıdır.",
                    "D": "Yanlış; Lewy Parkinson hastalığında alfa-sinüklein birikimidir.",
                    "E": "Yanlış; Russell plazma hücresi immünoglobulin globülleridir."
                }
            )
        ]
    })

    # Slayt 30: Bölüm Özeti: Hipersensitiviteden İmmünolojik Tolerans ve Otoimmüniteye Geçiş
    slides.append({
        "id": "k1-25-s30",
        "title": "Bölüm Özeti: Hipersensitiviteden İmmünolojik Toleransa Geçiş",
        "section": "Tip IV Hipersensitivite ve Doku Hasarı",
        "slideNumber": 30,
        "narrative": (
            "Dört aşırı duyarlılık tipinin incelenmesi, immün sistemin dış antijenlere (alerjenler, mikroplar) karşı "
            "verdiği zararlı reaksiyonları netleştirmiştir: "
            "1. **Kendi Antijenlerimiz Sorusu:** Peki bağışıklık sistemi normal şartlarda vücudun kendi trilyonlarca "
            "hücresel ve nükleer antijenine neden saldırmaz? "
            "2. **Toleransın Tanımı:** Kendi antijenlerini tanıyan lenfositlerin susturulması, silinmesi veya kontrol altında "
            "tutulması durumuna **İmmünolojik Tolerans** denir. "
            "3. **Otoimmünitenin Doğuşu:** Tolerans mekanizmaları genetik mutasyonlar veya çevresel tetikleyicilerle kırıldığında "
            "bağışıklık sistemi kendi organlarını yabancı ilan eder (**Otoimmünite**). "
            "Bölüm 4'te santral toleransı (timus/kemik iliği), periferik toleransı (Treg, anerji, Fas/FasL) ve otoimmünitenin "
            "genetik zeminini moleküler düzeyde inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "İmmün Yanıtın İki Yüzü",
                "İmmünolojik Tolerans (Sağlıklı Durum)",
                "Kendi antijenlerini tanıyan lenfositlerin yok edilmesi (delesyon) veya susturulması (anerji/Treg)",
                "Otoimmünite (Hastalık Durumu)",
                "Toleransın çökmesi, otoreaktif T ve B hücrelerinin serbest kalarak kendi parankimini tahrip etmesi"
            ),
            make_active_recall(
                "Bağışıklık sisteminin kendi doku antijenlerine karşı yanıtsız kalması ve kendi dokularını koruması fenomenine verilen genel immünolojik ad nedir?",
                "İmmünolojik toleranstır (Öz tolerans).",
                "Konağın kendi hücrelerine saldırmasını engelleyen savunma freni"
            )
        ]
    })

    return slides
