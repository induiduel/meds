# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 1: Aşırı Duyarlılık Reaksiyonları: Genel Bakış, Tip I (Ani) Hipersensitivite ve Anafilaksi (Slayt 1 - 10)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # Slayt 1: İmmünopatolojide Aşırı Duyarlılık Kavramı ve Coombs-Gell Sınıflaması
    slides.append({
        "id": "k1-25-s01",
        "title": "İmmünopatolojide Aşırı Duyarlılık Kavramı ve Coombs-Gell Sınıflaması",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 1,
        "narrative": (
            "İmmün sistem normalde konağı patojen mikroorganizmalardan korumak üzere evrimleşmiştir; ancak bu yanıt "
            "uygunsuz, aşırı veya kontrolsüz hale geldiğinde kendi dokularını tahrip eden bir silaha dönüşür: "
            "1. **Aşırı Duyarlılık (Hipersensitivite) Tanımı:** İmmünolojik mekanizmaların vücutta inflamasyon, hücre ölümü "
            "ve doku hasarı meydana getirmesi durumudur. "
            "2. **Tetikleyici Antijen Kaynakları:** "
            "- **Öz Antijenler (Otoantijenler):** Kendi doku bileşenlerine karşı toleransın kırılması (Otoimmünite). "
            "- **Zararsız Çevresel Antijenler:** Normalde bağışık bireylerde tepki oluşturmayan polen, akar veya ilaçlar (Alerji/Atopi). "
            "- **Kalıcı Mikrobiyal Antijenler:** Vücuttan temizlenemeyen kronik mikrobiyal yapılar (Tüberküloz granülomu). "
            "3. **Coombs ve Gell Sınıflaması:** Doku hasarını oluşturan immünolojik mekanizmaya göre Tip I, Tip II, Tip III ve Tip IV "
            "olarak dört ana grupta incelenir. İlk üç tip antikor aracılı (hümoral), dördüncü tip ise T lenfosit aracılı (hücresel) yanıttır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İmmün sistemin doku hasarı oluşturan reaksiyonları Coombs ve Gell sınıflamasına göre başlıca dört temel tipe ayrılır.",
                "dört",
                "Hipersensitivite tiplerinin klasik Roma rakamlarıyla ifade edilen toplam sayısı"
            ),
            make_table(
                "Coombs ve Gell Hipersensitivite Sınıflaması Genel Bakış",
                ["Aşırı Duyarlılık Tipi", "Temel İmmün Mekanizma", "Histopatolojik Karakter", "Prototip Klinik Örnek"],
                [
                    ["Tip I (Ani Tip)", "IgE antikorları ve mast hücre degranülasyonu", "Vazodilatasyon, ödem, bronkospazm", "Anafilaksi, alerjik astım"],
                    ["Tip II (Antikor Aracılı)", "IgG / IgM antikorları ve opsonizasyon", "Hücre lizisi, fagositoz, doku hasarı", "Otoimmün hemolitik anemi, Goodpasture"],
                    [
                        "Tip III (İmmün Kompleks)",
                        "Dolaşan Ag-Ab komplekslerinin çökmesi",
                        {"text": "Fibrinoid vaskülit ve nötrofilik infiltrasyon", "isMasked": True, "hint": "Damar duvarında fibrin ve nötrofil birikimiyle seyreden nekrotizan lezyon"},
                        "Serum hastalığı, SLE nefriti"
                    ],
                    ["Tip IV (Hücresel / Gecikmiş)", "CD4+ Th1/Th17 ve CD8+ sitotoksik T hücreleri", "Perivasküler lenfomononükleer infiltrat, granülom", "Kontakt dermatit, Tüberkülin PPD"]
                ]
            ),
            make_micro_quiz(
                "Coombs ve Gell sınıflamasına göre aşırı duyarlılık reaksiyonlarından hangisi antikorlar (immünoglobulinler) yerine doğrudan T lenfositleri aracılığıyla doku hasarı oluşturur?",
                {
                    "A": "Tip IV Aşırı Duyarlılık (Hücresel Tip)",
                    "B": "Tip I Aşırı Duyarlılık (Ani Tip)",
                    "C": "Tip II Aşırı Duyarlılık (Sitotoksik Tip)",
                    "D": "Tip III Aşırı Duyarlılık (İmmün Kompleks Tipi)",
                    "E": "Tip I ve Tip II Kombinasyonu"
                },
                "A",
                {
                    "A": "Doğrudur; Tip IV hipersensitivite antikorlardan bağımsız olup CD4+ ve CD8+ T lenfositleri tarafından yürütülür.",
                    "B": "Yanlış; Tip I IgE antikorları aracılıdır.",
                    "C": "Yanlış; Tip II IgG ve IgM antikorları aracılıdır.",
                    "D": "Yanlış; Tip III antijen-antikor immün kompleksleri aracılıdır.",
                    "E": "Yanlış; her ikisi de antikor bağımlıdır."
                }
            )
        ]
    })

    # Slayt 2: Tip I Aşırı Duyarlılık: Tanım, Atopi ve Genetik Zemin
    slides.append({
        "id": "k1-25-s02",
        "title": "Tip I Aşırı Duyarlılık: Tanım, Atopi ve Genetik Zemin",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 2,
        "narrative": (
            "Tip I aşırı duyarlılık, önceden duyarlılaşmış bir bireyde antijenle (alerjen) temas sonrası dakikalar içinde "
            "gelişen ani immünolojik yanıttır: "
            "1. **Atopi Kavramı:** Çevresel yaygın alerjenlere (polenler, ev tozu akarları, hayvan tüyleri) karşı ailesel olarak "
            "aşırı **IgE antikorları** üretme ve Tip I aşırı duyarlılık geliştirme genetik yatkınlığına **atopi** denir. "
            "2. **Th2 Hücre Üstünlüğü:** Atopik bireylerde antijen sunucu hücreler antijeni naif CD4+ T hücrelerine sunduğunda, "
            "yanıt Th1 yerine **T helper 2 (Th2)** yönüne sapar. "
            "3. **Kritik Sitokinler:** "
            "- **İnterlökin-4 (IL-4) ve IL-13:** B lenfositlerinde immünoglobulin sınıf değişimini uyararak **IgE** sentezini tetikler. "
            "- **İnterlökin-5 (IL-5):** Kemik iliğinden eozinofillerin üretimini, farklılaşmasını ve dokuya göçünü aktive eder. "
            "Atopik bireylerde serum IgE düzeyleri ve periferik kanda eozinofil oranları belirgin şekilde yüksektir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Atopik Bireyde IgE Sınıf Değişim Kaskadı",
                [
                    "1. Alerjen Teması: Mukozadan giren çevresel antijenin dendritik hücrelerce yakalanması",
                    "2. Th2 Farklılaşması: Naif CD4+ T hücrelerinin IL-4 etkisiyle Th2 fenotipine dönüşmesi",
                    "3. Sitokin Sentezi: Th2 hücrelerinden masif IL-4 ve IL-13 salgılanması",
                    "4. IgE İndüksiyonu: B lenfositlerinde sınıf değişim rekombinasyonu ile masif IgE üretilmesi"
                ]
            ),
            make_cloze(
                "Atopik bireylerde B lenfositlerinin IgE antikorları üretmesini indükleyen temel sitokinler IL-4 ve IL-13 mediyatörleridir.",
                "IL-4",
                "Th2 hücrelerinden salınan ve B hücrelerinde IgE izotip değişimini başlatan interlökin"
            )
        ]
    })

    # Slayt 3: Mast Hücresi ve Bazofiller: FcepsilonRI Reseptörü ve Sensitizasyon
    slides.append({
        "id": "k1-25-s03",
        "title": "Mast Hücresi ve Bazofiller: FcepsilonRI Reseptörü ve Sensitizasyon",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 3,
        "narrative": (
            "Tip I aşırı duyarlılık reaksiyonunun klinik olarak ortaya çıkabilmesi için önceden sessiz bir hazırlık evresi gereklidir: "
            "1. **Sensitizasyon (Duyarlılaşma) Fazı:** Alerjenle ilk temas sırasında üretilen IgE antikorları, dokularda yerleşik "
            "mast hücrelerinin ve dolaşımdaki bazofillerin membranındaki yüksek afiniteli **FcepsilonRI** reseptörlerine bağlanır. "
            "2. **FcepsilonRI Reseptör Mimarisi:** Bir alfa (IgE Fc bölgesini bağlar), bir beta ve iki gamma sinyal iletim zincirinden oluşur. "
            "Afinitesi o kadar yüksektir ki serumdaki eser miktardaki IgE moleküllerini bile yakalar ve hücre yüzeyinde aylarca stabil tutar. "
            "3. **Klinik Sessizlik:** Sensitizasyon aşamasında hiçbir doku hasarı, semptom veya inflamasyon izlenmez. Mast hücresi adeta "
            "tetikte bekleyen bir mayın gibi antijenik hedefe kilitlenmiş antikorlarla donatılmış olur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Mast Hücresi Sensitizasyon Bileşenleri",
                ["Bileşen", "Hücresel / Moleküler Yapı", "Bağlanma Bölgesi", "Fonksiyonel Görevi"],
                [
                    ["IgE Molekülü", "Monomerik immünoglobulin", "Fc bölgesi FcepsilonRI'ye bağlanır", "Alerjeni tanıyan özgül anten görevi"],
                    [
                        "FcepsilonRI Reseptörü",
                        "Yüksek afiniteli tetramerik reseptör",
                        {"text": "Alfa zinciri IgE'yi tutar", "isMasked": True, "hint": "Reseptörün immünoglobulini yakalayan dış parçası"},
                        "Mast hücresi membranına IgE'yi kilitler"
                    ],
                    ["Beta ve Gamma Zinciri", "İntraselüler ITAM motifleri", "Sitoplazmik protein kinazlar", "Çapraz bağlanmada kalsiyum sinyali iletimi"]
                ]
            ),
            make_active_recall(
                "Mast hücreleri ve bazofillerin membranında yer alan ve IgE molekülünün Fc kuyruğuna son derece yüksek afiniteyle bağlanan reseptör hangisidir?",
                "FcepsilonRI (Fc-epsilon-Reseptör-1) reseptörüdür.",
                "Tip I alerjik duyarlılaşmadan sorumlu yüksek afiniteli IgE yüzey algılayıcısı"
            )
        ]
    })

    # Slayt 4: Efektör Faz: Antijenle Yeniden Karşılaşma ve Degranülasyon
    slides.append({
        "id": "k1-25-s04",
        "title": "Efektör Faz: Antijenle Yeniden Karşılaşma ve Degranülasyon",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 4,
        "narrative": (
            "Duyarlılaşmış mast hücreleri aynı alerjenle ikinci kez karşılaştığında saniyeler içinde efektör faz tetiklenir: "
            "1. **Çapraz Bağlanma (Cross-linking):** Multivalan antijen molekülü, mast hücresi yüzeyinde yan yana duran en az "
            "iki IgE molekülünü aynı anda bağlayarak reseptörleri bir araya toplar. "
            "2. **Hücre İçi Sinyal İletimi:** Reseptör kümelenmesi gamma zincirlerindeki ITAM motiflerini fosforiller; "
            "Syk tirozin kinaz aktive olur ve fosfolipaz C-gama (PLC-gama) uyarılır. "
            "3. **Kalsiyum Fırlaması ve Ekzositoz:** İnozitol trisfosfat (IP3) endoplazmik retikulumdan sitoplazmaya masif kalsiyum salar. "
            "Kalsiyum artışı, mast hücresi sitoplazmasındaki veziküllerin hücre zarıyla kaynaşmasını sağlayarak **degranülasyonu** başlatır. "
            "Bu süreç antijen girişinden sonraki ilk 5 ile 30 dakika içinde doruğa çıkar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Mast Hücresi Degranülasyon Sinyal Yolağı",
                [
                    "1. Antijen Çapraz Bağlanması: Multivalan alerjenin bitişik iki IgE molekülünü kenetlemesi",
                    "2. Tirozin Kinaz Uyarımı: FcepsilonRI beta/gamma zincir fosforilasyonu ve Syk aktivasyonu",
                    "3. PLC-gama ve IP3 Artışı: Membran fosfolipidlerinin yıkımıyla hücre içi kalsiyum fırlaması",
                    "4. Ekzositoz: Granül zarlarının plazma membranıyla kaynaşarak mediyatörleri dışarı boşaltması"
                ]
            ),
            make_cloze(
                "Mast hücresi degranülasyonunu başlatan temel moleküler olay alerjenin yüzeydeki IgE moleküllerini çapraz bağlamasıdır.",
                "çapraz bağlaması",
                "İki bitişik reseptörün aynı antijen molekülüyle kenetlenmesi olayı"
            )
        ]
    })

    # Slayt 5: Erken Faz Mediyatörleri: Preforme Granül İçerikleri
    slides.append({
        "id": "k1-25-s05",
        "title": "Erken Faz Mediyatörleri: Preforme Granül İçerikleri",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 5,
        "narrative": (
            "Mast hücresi granüllerinde önceden sentezlenmiş ve depolanmış (preforme) mediyatörler dakikalar içinde çevre dokuya yayılır: "
            "1. **Histamin (En Önemli Vazoaktif Amin):** "
            "- **Vasküler Etki:** Postkapiller venüllerdeki H1 reseptörlerine bağlanarak endotel hücrelerinin kasılmasına, "
            "aralıkların açılmasına ve masif plazma sızıntısına (ödem) yol açar. "
            "- **Düz Kas Etkisi:** Bronşiyal ve intestinal düz kaslarda şiddetli spazm (bronkokonstriksiyon ve kramp) oluşturur. "
            "2. **Nötral Proteazlar (Triptaz ve Kimaz):** Dokuda bazal membran proteinlerini ve ekstraselüler matriksi parçalayarak ödemi yayar. "
            "Kandaki **triptaz düzeyi**, anafilaktik şok şüphesinde mast hücre aktivasyonunu kanıtlayan en güvenilir biyokimyasal belirteçtir. "
            "3. **Kemotaktik Faktörler:** Eozinofil kemotaktik faktörü (ECF-A) ve nötrofil kemotaktik faktörü lökositleri bölgeye çeker."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Mast Hücresi Preforme Mediyatörleri ve Hedef Etkileri",
                ["Preforme Mediyatör", "Kimyasal Yapısı", "Hedef Doku / Reseptör", "Klinik Patolojik Etki"],
                [
                    ["Histamin", "Vazoaktif amin", "H1 reseptörleri (endotel ve bronş düz kası)", "Vazodilatasyon, kapiller kaçak, bronkospazm"],
                    [
                        "Triptaz",
                        "Nötral serin proteaz",
                        {"text": "Serum düzeyi ölçümü (kanda stabil)", "isMasked": True, "hint": "Anafilaksi tanısında laboratuvarda ölçülen altın belirteç"},
                        "Doku hasarı ve anafilaksinin kesin kanıtı"
                    ],
                    ["Heparin", "Sülfatlı proteoglikan", "Lokal mikrodolaşım", "Lokal antikoagülasyon ve granül stabilitesi"],
                    ["ECF-A", "Kemotaktik oligopeptit", "Dolaşımdaki eozinofiller", "Geç faza eozinofil göçünün başlatılması"]
                ]
            ),
            make_active_recall(
                "Klinik pratikte anafilaktik şok geçiren bir hastada mast hücre degranülasyonunu doğrulamak için kanda bakılan en spesifik proteaz enzimi hangisidir?",
                "Serum triptaz düzeyidir.",
                "Mast hücre granüllerinden salınan serin proteaz enzimi"
            )
        ]
    })

    # Slayt 6: Geç Faz Mediyatörleri: De Novo Sentezlenen Lipidler ve Sitokinler
    slides.append({
        "id": "k1-25-s06",
        "title": "Geç Faz Mediyatörleri: De Novo Sentezlenen Lipidler ve Sitokinler",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 6,
        "narrative": (
            "Mast hücresi aktivasyonu sadece granülleri boşaltmakla kalmaz; membran lipidlerini ve çekirdek genlerini de uyarır: "
            "1. **De Novo Lipid Mediyatörler (Araşidonik Asit Yolağı):** "
            "- **Lökotrienler (LTC4, LTD4, LTE4):** 5-lipoksijenaz yoluyla sentezlenir. Histaminden **1000 kat daha güçlü** "
            "bronkokonstriktör ve damar geçirgenliği artırıcı etkiye sahiptirler (klasik anafilaksinin yavaş etkili maddesi / SRS-A). "
            "- **Prostaglandin D2 (PGD2):** Siklooksijenaz yoluyla üretilir; şiddetli bronkospazm ve mukus hipersekresyonu yapar. "
            "- **Trombosit Aktive Edici Faktör (PAF):** Trombosit agregasyonu, lökosit adezyonu ve mikrovasküler kaçak sağlar. "
            "2. **Sitokin Fırtınası (Geç Faz Yanıtı):** TNF-alfa, IL-1, IL-4 ve özellikle eozinofilleri dokuda yaşatan **IL-5** salınır. "
            "Antijen temasından 2 ile 8 saat sonra başlayan **geç faz reaksiyonu**, eozinofillerin doku yıkımıyla seyreder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Tip I Aşırı Duyarlılıkta İki Aşamalı Yanıt",
                "Erken Faz (İlk Dakikalar)",
                "Histamin salınımı, ani vazodilatasyon, kapiller kaçak, eritem, ödem ve geçici bronkospazm",
                "Geç Faz (2 - 8 Saat Sonra)",
                "Lökotrienler ve IL-5 ile dokuya toplanan eozinofil ve nötrofillerin kalıcı doku destrüksiyonu"
            ),
            make_micro_quiz(
                "Tip I aşırı duyarlılıkta mast hücre membranından sentezlenen ve histaminden yaklaşık bin kat daha güçlü bronkokonstriksiyon oluşturan lipid mediyatör grubu hangisidir?",
                {
                    "A": "Sisteinil lökotrienler (LTC4, LTD4, LTE4)",
                    "B": "Tromboksan A2",
                    "C": "Bradikinin",
                    "D": "Prostasiklin (PGI2)",
                    "E": "Nitrik oksit (NO)"
                },
                "A",
                {
                    "A": "Doğrudur; sisteinil lökotrienler histaminden kat kat güçlü bronkokonstriktör ve permeabilite artırıcı lipidlerdir.",
                    "B": "Yanlış; tromboksan trombosit agregasyonu yapar.",
                    "C": "Yanlış; bradikinin plazma kinin sisteminden üretilen peptittir.",
                    "D": "Yanlış; prostasiklin vazodilatatördür.",
                    "E": "Yanlış; NO gaz yapıda vazodilatatördür."
                }
            )
        ]
    })

    # Slayt 7: Klinik Yelpaze: Lokal Atopik Reaksiyonlar
    slides.append({
        "id": "k1-25-s07",
        "title": "Klinik Yelpaze: Lokal Atopik Reaksiyonlar ve Histopatolojisi",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 7,
        "narrative": (
            "Tip I aşırı duyarlılık alerjenin giriş kapısına göre lokal klinik tablolara neden olur: "
            "1. **Alerjik Rinit (Saman Nezlesi):** Polenlerin burun mukozasına temasıyla gelişir; mukozal ödem, sulu burun akıntısı, "
            "hapşırma ve konjonktivit izlenir. "
            "2. **Bronşiyal Astım:** İnhale alerjenlerle bronşlarda gelişen tablodur. Bronkospazm, aşırı mukus tıkacı, eozinofilik eksüda "
            "ve epitel dökülmesi görülür. Balgamda dökülen epitel hücreleri (**Curschmann spiralleri**) ve eozinofil granül protein kristalleri "
            "(**Charcot-Leyden kristalleri**) patognomoniktir. "
            "3. **Ürtiker ve Anjiyoödem:** Cilde temas veya besin alımıyla dermiste mast hücre uyarımı; dermiste geçici kaşıntılı eritematöz "
            "plaklar (ürtiker) veya derin submukozal dokularda yaygın ödem (anjiyoödem) oluşur. Larenks anjiyoödemi asfiksi yapabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Lokal Tip I Aşırı Duyarlılık Klinik Formları",
                ["Klinik Tablo", "Alerjen Giriş Yolu", "Etkilenen Hedef Organ", "Karakteristik Histopatolojik Bulgu"],
                [
                    ["Alerjik Rinit", "Solunum (İnhalasyon)", "Nazal mukoza ve konjonktiva", "Mukozal ödem ve eozinofilik infiltrasyon"],
                    [
                        "Bronşiyal Astım",
                        "Solunum (Derin İnhalasyon)",
                        "Bronş ve bronşiyoller",
                        {"text": "Charcot-Leyden kristalleri ve Curschmann spiralleri", "isMasked": True, "hint": "Astımlı hastanın balgamında izlenen eozinofil kristalleri ve mukus tıkaçları"},
                    ],
                    ["Ürtiker (Kurdeşen)", "Deri teması veya sistemik gıda", "Papiller ve retiküler dermis", "Dermal mikrovasküler kaçak ve kaşıntılı kabarıklık"],
                    ["Gastroenterit", "Gastrointestinal emilim", "Mide ve bağırsak mukozası", "Mukozal ödem, peristaltizm artışı ve kramp/kusma"]
                ]
            ),
            make_active_recall(
                "Alerjik bronşiyal astım hastasının balgamında eozinofil membran proteinlerinin (galektin-10) birikmesiyle oluşan hekzagonal elmas biçimli kristallere ne ad verilir?",
                "Charcot-Leyden kristalleri denir.",
                "Eozinofil lizisi sonucu ortaya çıkan mikroskobik kristal yapılar"
            )
        ]
    })

    # Slayt 8: Sistemik Anafilaksi Patolojisi ve Acil Yönetimi
    slides.append({
        "id": "k1-25-s08",
        "title": "Sistemik Anafilaksi Patolojisi ve Acil Yönetimi",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 8,
        "narrative": (
            "Sistemik anafilaksi, antijenin doğrudan dolaşıma girmesiyle tüm vücut mast hücrelerinin aynı anda uyarılmasıdır: "
            "1. **En Sık Nedenler:** Parenteral ilaçlar (özellikle penisilin ve sefalosporinler), arı ve böcek sokmaları, "
            "radyoopak kontrast maddeler ve besin maddeleridir (yer fıstığı, kabuklu deniz ürünleri). "
            "2. **Ölümcül Patofizyoloji:** "
            "- **Solunum Yolu Asfiksisi:** Şiddetli laringeal ödem ve difüz bronkokonstriksiyon trakeayı tamamen tıkar. "
            "- **Kardiyovasküler Çöküş:** Yaygın vazodilatasyon ve kapiller kaçak sonucu intravasküler kan interstisyuma boşalır; "
            "dakikalar içinde derin hipotansiyon ve anafilaktik şok gelişir. "
            "3. **Hayat Kurtarıcı Tedavi:** Zaman kaybedilmeden intramusküler **Epinefrin (Adrenalin)** uygulanmalıdır. "
            "Epinefrin alfa-1 etkisiyle damarları büzüp tansiyonu yükseltir, beta-2 etkisiyle bronkodilatasyon sağlar ve mast hücresini stabilize eder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Penisilin enjeksiyonunun 3. dakikasında hastada dilde ve boğazda şişme, stridor, hırıltılı solunum, yaygın ürtiker ve tansiyon 60/30 mmHg saptanıyor.",
                [
                    {
                        "text": "Sistemik anafilaksi tanısıyla derhal uyluk anterolateraline intramusküler epinefrin (adrenalin) uygulamak, havayolunu açmak ve oksijen ile intravenöz sıvı başlamak",
                        "isCorrect": True,
                        "explanation": "Mükemmel Acil Karar: Anafilakside tek hayat kurtarıcı ilaç epinefrindir; alfa ve beta agonist etkisiyle laringeal ödemi ve hipotansiyonu dakikalar içinde geri çevirir."
                    },
                    {
                        "text": "Yalnızca oral antihistaminik tablet verip hastayı evine dinlenmeye göndermek",
                        "isCorrect": False,
                        "explanation": "Ölümcül hata! Antihistaminikler anafilaktik şoku ve laringeal ödemi durduramaz; hasta dakikalar içinde asfiksi ve arrestle kaybedilir."
                    }
                ]
            ),
            make_cloze(
                "Sistemik anafilaksi tablosunda hem bronkodilatasyon sağlayan hem de vazokonstriksiyonla şoku düzelten ilk tercih ilaç epinefrindir.",
                "epinefrindir",
                "Adrenalin olarak da bilinen alfa ve beta adrenerjik acil resüsitasyon hormonu"
            )
        ]
    })

    # Slayt 9: Checkpoint 1
    slides.append({
        "id": "k1-25-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Tip I Aşırı Duyarlılık ve Anafilaksi",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 9,
        "narrative": (
            "Bu birinci kontrol noktasında, Tip I aşırı duyarlılık ve anafilaksi patolojisini özetliyoruz: "
            "1. **Mekanizma:** Alerjen temasında Th2 hücreleri IL-4 ve IL-13 salgılar; B hücreleri IgE üretir. "
            "2. **Sensitizasyon:** IgE antikorları mast hücre yüzeyindeki yüksek afiniteli FcepsilonRI reseptörüne bağlanır. "
            "3. **Efektör Faz:** Alerjenle tekrar karşılaşmada iki bitişik IgE çapraz bağlanır, hücre içi kalsiyum artar ve degranülasyon olur. "
            "4. **Erken Faz Mediyatörleri:** Preforme granüllerden histamin ve triptaz salınır (dakikalar içinde). "
            "5. **Geç Faz Mediyatörleri:** Araşidonik asitten lökotrienler (LTC4/D4/E4 - SRS-A) sentezlenir ve IL-5 ile eozinofiller toplanır. "
            "6. **Klinik Formlar:** Astımda Charcot-Leyden ve Curschmann bulguları; anafilakside asfiksi ve şok riski vardır (tedavi epinefrin)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s09-1",
                "Tip I aşırı duyarlılık reaksiyonunda naif B lenfositlerinde IgE sınıf değişimini başlatan temel T helper sitokinleri hangileridir?",
                "İnterlökin-4 (IL-4) ve İnterlökin-13 (IL-13) molekülleridir.",
                "Th2 lenfositlerince salgılanan ve B hücresinde antikor izotip dönüşümü yaptıran faktörler",
                "Th2 Sitokinleri ve IgE"
            ),
            make_flashcard(
                "k1-25-fc-s09-2",
                "Mast hücre granüllerinden salınan ve anafilaksi tanısında laboratuvarda mast hücresi aktivasyonunun kanıtı olarak ölçülen temel proteaz nedir?",
                "Triptaz enzimidir.",
                "Kanda yarı ömrü uzun olan nötral serin endopeptidaz belirteci",
                "Serum Triptaz Belirteci"
            ),
            make_flashcard(
                "k1-25-fc-s09-3",
                "Alerjik bronşiyal astım tanısı alan bir hastanın mikroskopik balgam incelemesinde eozinofil membran proteinlerinden köken alan kristal yapılara ne ad verilir?",
                "Charcot-Leyden kristalleri denir.",
                "Eozinofilik granül yıkımıyla meydana gelen hekzagonal elmas biçimli lameller",
                "Charcot-Leyden Kristalleri"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tip I Hipersensitivite Checkpoint Karşılaştırma Matrisi",
                ["Aşama", "Tetikleyici Faktör", "Anahtar Molekül", "Klinik Görünüm"],
                [
                    ["Duyarlılaşma (Sensitizasyon)", "İlk alerjen girişi", "FcepsilonRI + IgE bağlanması", "Asemptomatik hazırlık dönemi"],
                    ["Erken Efektör Yanıt", "İkinci antijen maruziyeti", "Histamin + Triptaz", "Vazodilatasyon, ödem, eritem"],
                    [
                        "Geç Faz Reaksiyonu",
                        "De novo lipid sentezi",
                        {"text": "Lökotrienler (LTC4/D4) + Eozinofiller", "isMasked": True, "hint": "Geç fazda doku hasarından sorumlu primer lipidler ve lökositler"},
                        "Doku hasarı, eozinofilik eksüda"
                    ],
                    ["Sistemik Kriz (Anafilaksi)", "Parenteral antijen yükü", "Masif vazodilatasyon ve laringeal ödem", "Asfiksi ve anafilaktik şok"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi Tip I aşırı duyarlılık reaksiyonunun geç fazında (antijen temasından 2-8 saat sonra) doku hasarının gelişiminden sorumlu olan temel faktördür?",
                {
                    "A": "Lökotrienler ve dokuya göç eden eozinofillerin toksik granül proteinleri",
                    "B": "Preforme depolanmış histamin moleküllerinin tükenmesi",
                    "C": "Kompleman membran atak kompleksinin (C5b-9) aktivasyonu",
                    "D": "CD8+ sitotoksik T lenfositlerinin perforin salgılaması",
                    "E": "Dolaşan immün komplekslerin glomerüllerde birikmesi"
                },
                "A",
                {
                    "A": "Doğrudur; geç faz reaksiyonu de novo lökotrienler ve IL-5 ile dokuya toplanan eozinofillerin toksik enzimleriyle gerçekleşir.",
                    "B": "Yanlış; histamin erken fazda görev alır.",
                    "C": "Yanlış; kompleman Tip II ve III reaksiyonlarında etkindir.",
                    "D": "Yanlış; CD8+ hücreler Tip IV reaksiyonudur.",
                    "E": "Yanlış; immün kompleks birikimi Tip III mekanizmasıdır."
                }
            )
        ]
    })

    # Slayt 10: Bölüm Özeti: Tip I'den Antikor ve İmmün Kompleks Aracılı Doku Hasarına Geçiş
    slides.append({
        "id": "k1-25-s10",
        "title": "Bölüm Özeti: Tip I'den Antikor ve İmmün Kompleks Hasarına Geçiş",
        "section": "Aşırı Duyarlılık Reaksiyonları ve Tip I Hipersensitivite",
        "slideNumber": 10,
        "narrative": (
            "Tip I aşırı duyarlılıkta primer hasar serbest alerjenlerin IgE ile mast hücrelerini uyarmasıyla sınırlıdır: "
            "1. **Hedef Farkı:** Tip I'de antijen serbest çözünür bir moleküldür; hedef hücre mast hücresidir. "
            "2. **Tip II'ye Geçiş (Hücre Yüzey Antijenleri):** Tip II aşırı duyarlılıkta antijenler çözünür alerjenler değildir; "
            "doğrudan spesifik hücrelerin yüzeyinde (eritrosit, trombosit, bazal membran) yerleşik moleküllerdir. "
            "Burada görevli antikorlar IgE değil, **IgG ve IgM** izotipleridir; fagositoz, kompleman lizisi veya fonksiyon bozukluğu yaparlar. "
            "3. **Tip III'e Geçiş (Dolaşan Kompleksler):** Tip III'te ise antijen ve antikor kanda birleşerek immün kompleksler "
            "oluşturur ve damar duvarına çökerek fibrinoid nekrozlu vaskülit yapar. "
            "Bölüm 2'de bu iki antikor aracılı doku hasarı mekanizmasını inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Hipersensitivite Antijen Yerleşim Dinamikleri",
                "Tip I Hipersensitivite",
                "Çözünür çevresel alerjenler, IgE antikorları ve mast hücresinden ani vazoaktif mediyatör salınımı",
                "Tip II ve Tip III Hipersensitivite",
                "Sabit hücre/doku antijenlerine IgG/IgM bağlanması (Tip II) veya kanda dolaşan immün komplekslerin damara çökmesi (Tip III)"
            ),
            make_active_recall(
                "Coombs ve Gell sınıflamasında doğrudan hücre membranındaki veya ekstraselüler matriks yüzeyindeki sabit antijenlere bağlanan antikorların oluşturduğu hipersensitivite tipi hangisidir?",
                "Tip II (Antikor aracılı / Sitotoksik) aşırı duyarlılıktır.",
                "Hücre yüzey antijenine bağlanan IgG veya IgM aracılı mekanizma"
            )
        ]
    })

    return slides
