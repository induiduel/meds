# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 8: Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK (Slayt 71 - 80)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # Slayt 71: Septik Şok Epidemiyolojisi ve Klinik Önemi
    slides.append({
        "id": "k1-24-s71",
        "title": "Septik Şok Epidemiyolojisi ve Klinik Önemi",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 71,
        "narrative": (
            "Septik şok, yoğun bakım ünitelerinde (YBÜ) karşılaşılan ölümlerin en sık nedenidir ve modern tıbbın "
            "en zorlu klinik tablolarından birini oluşturur: "
            "1. **Mortalite Oranları:** Gelişmiş yoğun bakım desteklerine rağmen septik şok mortalitesi %20 ile %50 arasında seyreder. "
            "2. **Riskli Hasta Grupları:** İleri yaş, prematürite, immünsüpresif tedavi alanlar, kemoterapi hastaları, "
            "büyük cerrahi operasyon geçirenler, invaziv kateter taşıyanlar ve diyabetikler en yüksek risk grubundadır. "
            "3. **Klinik Tanım Evrimi:** Sistemik inflamatuar yanıt sendromu (SIRS) ile başlayan süreç; enfeksiyon varlığında sepsise, "
            "organ disfonksiyonu eklenince ağır sepsise ve sıvı resüsitasyonuna yanıtsız inatçı hipotansiyon ile laktik asidoz "
            "geliştiğinde septik şoka ilerler. Bu ilerlemenin arkasında patojenik mikrobiyal ürünlerin tetiklediği sistemik yıkım yatar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Yeterli intravenöz sıvı resüsitasyonuna rağmen devam eden inatçı arteriyel hipotansiyon ve hiperlaktatemi tablosu septik şok olarak tanımlanır.",
                "septik şok",
                "Enfeksiyon zemininde dolaşım yetmezliğiyle seyreden ölümcül tablo"
            ),
            make_micro_quiz(
                "Modern yoğun bakım ünitelerinde mortalitenin ve çoklu organ yetmezliğinin bir numaralı nedeni olan şok türü hangisidir?",
                {
                    "A": "Septik şok tablosu",
                    "B": "Primer nörojenik şok",
                    "C": "Saf anafilaktik şok",
                    "D": "İzole hemorajik hipovolemi",
                    "E": "Akut dekompresyon şoku"
                },
                "A",
                {
                    "A": "Doğrudur; yoğun bakım ünitelerinde en sık ölüm ve morbidite nedeni septik şoktur.",
                    "B": "Yanlış; nörojenik şok travma merkezlerinde görülür, yoğun bakımdaki en sık ölüm nedeni değildir.",
                    "C": "Yanlış; anafilaksi acil serviste epinefrinle hızla yönetilir.",
                    "D": "Yanlış; hipovolemi kan replasmanıyla hızla düzeltilebilir.",
                    "E": "Yanlış; dekompresyon nadir mesleki tablodur."
                }
            )
        ]
    })

    # Slayt 72: Mikrobiyal Tetikleyiciler: Gram-Pozitif vs Gram-Negatif Üstünlüğü
    slides.append({
        "id": "k1-24-s72",
        "title": "Mikrobiyal Tetikleyiciler: Gram-Pozitif vs Gram-Negatif Üstünlüğü",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 72,
        "narrative": (
            "Tarihsel olarak septik şokun başlıca Gram-negatif endotoksinlerine bağlı olduğu düşünülse de güncel epidemiyoloji "
            "farklı bir tablo ortaya koymaktadır: "
            "1. **Gram-Pozitif Bakteri Liderliği:** Günümüzde septik şok vakalarının en sık nedeni (%40-50) **Gram-pozitif bakterilerdir** "
            "(Streptococcus pneumoniae, Staphylococcus aureus, Enterococcus türleri). "
            "2. **Gram-Negatif Basiller:** Vakaların %30-40'ından sorumludur (Escherichia coli, Klebsiella pneumoniae, Pseudomonas aeruginosa). "
            "3. **Diğer Patojenler:** Fungal etkenler (özellikle Candida türleri immünsüprese hastalarda giderek artmaktadır) ve virüslerdir. "
            "4. **Süperantijenler:** Bazı Gram-pozitif suşlar (S. aureus ve S. pyogenes), T lenfositleri poliklonal olarak aktive eden "
            "süperantijenler (Toksik Şok Sendromu Toksini-1 / TSST-1) üreterek kontrolsüz masif sitokin fırtınasını doğrudan tetikler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Septik Şok Mikrobiyal Ajanları ve Hücre Duvarı Bileşenleri",
                ["Mikroorganizma Grubu", "Görülme Sıklığı", "Primer Tetikleyici Bileşen", "Klinik Örnekler"],
                [
                    [
                        "Gram-Pozitif Bakteriler",
                        "En Sık (%40 - 50)",
                        {"text": "Peptidoglikan ve teikoik asit", "isMasked": True, "hint": "Gram-pozitif hücre duvarının kalın polimerik yapıları"},
                        "S. aureus, S. pneumoniae, Enterokoklar"
                    ],
                    ["Gram-Negatif Bakteriler", "%30 - 40", "Lipopolisakkarit (LPS / Endotoksin)", "E. coli, Klebsiella, Pseudomonas"],
                    ["Mantarlar", "%5 - 10", "Beta-glukan ve mannan polisakkaritleri", "Candida albicans, Aspergillus"],
                    ["Süperantijen Üretenler", "Nadir / Akut", "TSST-1 ve enterotoksinler", "Toksik Şok Sendromu (Tampon kullanımı)"]
                ]
            ),
            make_active_recall(
                "Modern klinik epidemiyolojiye göre septik şok vakalarında en sık izole edilen mikrobiyal bakteri grubu hangisidir?",
                "Gram-pozitif bakterilerdir (Streptokok ve Stafilokoklar).",
                "Hücre duvarında kalın peptidoglikan tabakası taşıyan mikroorganizmalar"
            )
        ]
    })

    # Slayt 73: İmmün Tanıma ve PAMP/TLR Kaskadı
    slides.append({
        "id": "k1-24-s73",
        "title": "İmmün Tanıma ve PAMP/TLR Kaskadı: Endotoksinin Moleküler Yolu",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 73,
        "narrative": (
            "Septik şok patogenezinin ilk moleküler basamağı, mikroorganizmaların yapısal bileşenlerinin konak doğuştan "
            "bağışıklık hücreleri tarafından tanınmasıdır: "
            "1. **PAMP Tanımı:** Patojenle ilişkili moleküler paternler (PAMP), konak hücrelerindeki patern tanıma reseptörlerine bağlanır. "
            "2. **Gram-Negatif Endotoksin (LPS):** Hücre duvarı lipopolisakkariti (LPS) üç parçadan oluşur; toksik biyolojik etkiden sorumlu "
            "olan parça **Lipid A** fraksiyonudur. "
            "3. **TLR-4 ve CD14 Kompleksi:** Dolaşımdaki serbest LPS önce kanda LPS bağlayıcı protein (LBP) ile birleşir. Bu kompleks, "
            "monosit, makrofaj ve nötrofil yüzeyindeki **CD14 reseptörüne ve Toll-benzeri Reseptör 4 (TLR-4)** proteinine aktarılır. "
            "4. **NF-kappaB Aktivasyonu:** TLR-4 aktivasyonu hücre içi sinyal iletimini tetikleyerek transkripsiyon faktörü **NF-kappaB**'yi "
            "çekirdeğe gönderir ve proinflamatuar sitokin genlerinin masif transkripsiyonunu başlatır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Endotoksin Tanıma ve Transkripsiyon Kaskadı",
                [
                    "1. LPS Salınımı: Bakteri lizisiyle Lipid A içeren lipopolisakkaritlerin dolaşıma dökülmesi",
                    "2. LBP Bağlanması: Serum LPS-bağlayıcı proteinin endotoksin molekülünü yakalaması",
                    "3. TLR-4 / CD14 Kompleksi: Makrofaj yüzeyindeki Toll-benzeri reseptörün uyarılması",
                    "4. NF-kappaB Aktivasyonu: Çekirdeğe göç eden faktörün proinflamatuar genleri tetiklemesi"
                ]
            ),
            make_cloze(
                "Gram-negatif bakteri endotoksininin toksik biyolojik etkilerinden sorumlu temel yapısal parçası Lipid A fraksiyonudur.",
                "Lipid A",
                "LPS molekülünün hidrofobik membran bağlayıcı toksik bileşeni"
            )
        ]
    })

    # Slayt 74: Sitokin Fırtınası ve Enflamatuar Mediyatörler
    slides.append({
        "id": "k1-24-s74",
        "title": "Sitokin Fırtınası ve Enflamatuar Mediyatörler",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 74,
        "narrative": (
            "NF-kappaB aktivasyonuyla aktive olan mononükleer fagositler ve endotel hücreleri kontrolsüz bir mediyatör dalgası üretir: "
            "1. **Birincil Proinflamatuar Sitokinler:** **Tümör Nekrozis Faktör-alfa (TNF-alfa)** ve **İnterlökin-1 (IL-1)** "
            "septik şokun orkestra şefleridir. Ateşi, lökositozu ve endotel aktivasyonunu doğrudan uyarırlar. "
            "2. **Sekonder Sitokinler:** Karaciğerden akut faz reaktanlarının (CRP, fibrinojen) sentezini tetikleyen **IL-6** ve "
            "nötrofilleri dokuya çeken **IL-8** (kemokin) hızla yükselir. "
            "3. **Enflamatuar Lipidler ve Kompleman:** Trombosit aktive edici faktör (PAF), lökotrienler ve prostaglandinler vasküler "
            "geçirgenliği artırır; aktive kompleman fragmanları (**C3a, C5a**) anafilatoksin etkisiyle vazodilatasyonu derinleştirir. "
            "4. **Nitrik Oksit:** İndüklenebilir NO sentaz (iNOS) uyarımıyla bol miktarda NO üretilir ve periferik direnç çöker."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Lokal İnflamasyon vs Sitokin Fırtınası",
                "Lokal İnflamasyon (Kontrollü)",
                "Doku düzeyinde kontrollü TNF/IL-1 salınımı, lökosit göçü ve patojenin lokal fagositozla yok edilmesi",
                "Sistemik Sitokin Fırtınası (Septik Şok)",
                "Dolaşıma taşan TNF/IL-1, yaygın endotel hasarı, masif mikrovasküler kaçak ve vasküler tonus çöküşü"
            ),
            make_micro_quiz(
                "Septik şok patogenezinde endotel aktivasyonunu ve sistemik inflamatuar yanıtı başlatan iki temel birincil sitokin hangileridir?",
                {
                    "A": "TNF-alfa ve İnterlökin-1 (IL-1)",
                    "B": "İnterlökin-4 ve İnterlökin-13",
                    "C": "Transforme edici büyüme faktörü-beta (TGF-beta) ve IL-10",
                    "D": "Eritropoietin ve Trombopoietin",
                    "E": "İnterferon-gamma ve IL-35"
                },
                "A",
                {
                    "A": "Doğrudur; TNF-alfa ve IL-1 septik şok kaskadının en kritik primer proinflamatuar sitokinleridir.",
                    "B": "Yanlış; IL-4 ve IL-13 Tip 2 immünite ve alerjiden sorumludur.",
                    "C": "Yanlış; TGF-beta ve IL-10 antienflamatuar sitokinlerdir.",
                    "D": "Yanlış; bunlar hematopoietik büyüme faktörleridir.",
                    "E": "Yanlış; primer septik şok fırtınası makrofaj kaynaklı TNF ve IL-1 ile tetiklenir."
                }
            )
        ]
    })

    # Slayt 75: Yaygın Endotel Aktivasyonu ve Hasarı
    slides.append({
        "id": "k1-24-s75",
        "title": "Yaygın Endotel Aktivasyonu ve Hasarı: Bariyer Fonksiyonunun Kaybı",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 75,
        "narrative": (
            "Septik şokta mortalitenin ana belirleyicisi, tüm vasküler yatak boyunca endotel hücrelerinin aktive olması ve hasarlanmasıdır: "
            "1. **Bariyer Bozulması ve Kapiller Kaçak:** Proinflamatuar sitokinler endotel hücrelerinin hücre-hücre bağlantılarını "
            "(tight junction ve VE-kaderin kompleksleri) gevşetir. Plazma proteinleri ve sıvı hızla interstisyuma kaçarak yaygın ödeme yol açar. "
            "2. **Lökosit Adezyonu:** Endotel yüzeyinde E-selektin, P-selektin, ICAM-1 ve VCAM-1 ekspresyonu aşırı derecede artar. "
            "Nötrofiller damar duvarına yapışır ve salgıladıkları reaktif oksijen radikalleri (ROS) ile proteolitik enzimlerle endoteli deler. "
            "3. **Vazomotor Tonus Felci:** Endotelden aşırı miktarda nitrik oksit (NO) ve prostasiklin (PGI2) salınırken, endotelin sentezi "
            "baskılanır. Damar düz kasları gevşer, arteriyel tonus kaybolur ve vazopressör ilaçlara yanıtsız derin hipotansiyon gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Septik şokta endotel hücrelerinin intersellüler bağlantılarının gevşemesi sonucu protein zengin plazmanın dokuya kaçışına kapiller kaçak sendromu denir.",
                "kapiller kaçak",
                "Damar geçirgenliğinin bozulmasıyla intravasküler sıvının interstisyuma taşması"
            ),
            make_active_recall(
                "Septik şokta damar düz kaslarının aşırı gevşemesine ve vazopressör yanıtsızlığına yol açan temel vasküler gaz mediyatör hangisidir?",
                "Nitrik oksit (NO) molekülüdür.",
                "İndüklenebilir NO sentaz tarafından üretilen güçlü vazodilatatör"
            )
        ]
    })

    # Slayt 76: Pıhtılaşma Bozukluğu ve Prokoagülan Durum
    slides.append({
        "id": "k1-24-s76",
        "title": "Pıhtılaşma Bozukluğu: Prokoagülan Değişim ve Antikoagülan Çöküş",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 76,
        "narrative": (
            "Normalde endotel güçlü bir antitrombotik yüzeydir; ancak septik şokta endotel fenotipi dramatik bir prokoagülan değişime uğrar: "
            "1. **Doku Faktörü (TF) Sentezi:** TNF-alfa ve IL-1, endotel hücreleri ve monositlerde **Doku Faktörü (TF / Faktör III)** "
            "ekspresyonunu tetikler; bu durum ekstrinsik pıhtılaşma yolağını masif olarak aktive eder. "
            "2. **Antikoagülan Mekanizmaların Çöküşü:** Endotel yüzeyindeki **trombomodulin** ve **endotelyal protein C reseptörü (EPCR)** "
            "düzeyleri dramatik şekilde azalır. Aktive Protein C üretilemez; Faktör Va ve VIIIa inaktive edilemez. "
            "Ayrıca Doku Faktörü Yolağı İnhibitörü (TFPI) tükenir ve antitrombin III (AT-III) düzeyi düşer. "
            "3. **Fibrinolizin Baskılanması:** Endotelden bol miktarda **Plazminojen Aktivatör İnhibitörü-1 (PAI-1)** salınır. "
            "Plazmin üretimi durur, oluşan fibrin pıhtıları eritilemez ve mikrovasküler lümenler tıkanmaya terk edilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Endotel Fenotipinin Antitrombotikten Prokoagülana Değişimi",
                ["Moleküler Faktör", "Sağlıklı Endoteldeki Durum", "Septik Şoktaki Değişim", "Patofizyolojik Sonuç"],
                [
                    ["Doku Faktörü (TF)", "Sentezlenmez / Yok", "Masif Ekspresyon", "Ekstrinsik koagülasyon aktivasyonu"],
                    [
                        "Trombomodulin",
                        "Yüksek Ekspresyon",
                        {"text": "Aşırı Azalmış", "isMasked": True, "hint": "Protein C aktivasyonunu engelleyen reseptör kaybı"},
                        "Protein C üretilemez, trombin frenlenemez"
                    ],
                    ["PAI-1 Düzeyi", "Düşük / Dengeli", "İleri Derecede Yüksek", "Fibrinoliz baskılanır, pıhtı eriyemez"],
                    ["Antitrombin III (AT-III)", "Normal Düzeyde", "Tüketilmiş ve Düşük", "Serbest trombin inaktivasyonu bozulur"]
                ]
            ),
            make_active_recall(
                "Septik şokta fibrinolitik aktiviteyi bloke ederek mikrotrombüslerin eritilmesini engelleyen temel inhibitör molekül hangisidir?",
                "Plazminojen Aktivatör İnhibitörü-1 (PAI-1) molekülüdür.",
                "Doku plazminojen aktivatörünü durduran endotelyal inhibitör"
            )
        ]
    })

    # Slayt 77: Dissemine İntravasküler Koagülasyon (DİK)
    slides.append({
        "id": "k1-24-s77",
        "title": "Dissemine İntravasküler Koagülasyon (DİK): Tüketim Koagülopatisi",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 77,
        "narrative": (
            "Doku faktörü salınımı, antikoagülan moleküllerin kaybı ve fibrinolizin bloke edilmesi nihayetinde dissemine "
            "intravasküler koagülasyon (DİK) tablosuna yol açar: "
            "1. **İkili Patoloji Paradoksu:** DİK klinik olarak iki zıt tablonun aynı anda varlığıdır: "
            "- **Yaygın Tromboz:** Tüm mikrodolaşımda (böbrek, beyin, akciğer, sürrenal) fibrin-trombosit mikrotrombüsleri oluşur; "
            "yaygın doku iskemisi ve çoklu organ yetmezliği gelişir. "
            "- **Yaygın Kanama:** Sürekli pıhtı oluşumu vücuttaki fibrinojen, protrombin, Faktör V, Faktör VIII ve trombositleri tüketir "
            "(tüketim koagülopatisi). Sonuçta peteşi, purpura, ekimoz ve kontrolsüz mukozal kanamalar başlar. "
            "2. **Laboratuvar Bulguları:** PT ve aPTT belirgin uzar, trombositopeni derinleşir, fibrinojen düşer ve fibrin yıkım "
            "ürünleri olan **D-dimer** düzeyleri tavan yapar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "DİK Patogenezi ve Tüketim Döngüsü",
                [
                    "1. TF Ekspresyonu: Endotel ve monositlerden doku faktörünün masif açığa çıkması",
                    "2. Mikrovasküler Tromboz: Kılcal damarlarda yaygın fibrin pıhtıları ve doku iskemisi",
                    "3. Faktör Tüketimi: Trombosit, fibrinojen ve pıhtılaşma faktörlerinin tükenmesi",
                    "4. Kontrolsüz Hemoraji: Tüketim koagülopatisiyle spontan peteşi, purpura ve masif kanama"
                ]
            ),
            make_micro_quiz(
                "Septik şok zemininde gelişen dissemine intravasküler koagülasyon (DİK) tablosunda trombositopeni ve uzamış pıhtılaşma testleriyle birlikte tavan yapan fibrin yıkım ürünü hangisidir?",
                {
                    "A": "D-dimer molekülü",
                    "B": "Serum kalsiyum düzeyi",
                    "C": "Alkalen fosfataz enzimi",
                    "D": "Konjuge bilirubin fraksiyonu",
                    "E": "Trombospondin-1 seviyesi"
                },
                "A",
                {
                    "A": "Doğrudur; çapraz bağlı fibrinin plazmince parçalanması sonucu oluşan D-dimer DİK tablosunda en karakteristik yükselen belirteçtir.",
                    "B": "Yanlış; kalsiyum pıhtılaşmada kofaktördür ancak fibrin yıkım ürünü değildir.",
                    "C": "Yanlış; ALP karaciğer ve kemik enzimidir.",
                    "D": "Yanlış; bilirubin hem yıkım ürünüdür.",
                    "E": "Yanlış; trombospondin trombosit alfa granül proteinidir."
                }
            )
        ]
    })

    # Slayt 78: İntravenöz Sıvı Tedavisi Paradoksu ve Vasküler Kaçak
    slides.append({
        "id": "k1-24-s78",
        "title": "İntravenöz Sıvı Tedavisi Paradoksu ve Vasküler Kaçak",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 78,
        "narrative": (
            "Septik şok resüsitasyonunda klinisyeni en çok zorlayan hemodinamik açmaz intravenöz sıvı tedavisidir: "
            "1. **Gereklilik:** Yaygın arteriyoler dilatasyon ve venöz kapasitans göllenmesi nedeniyle efektif dolaşan kan hacmi düşüktür; "
            "hastaya ön yükü artırmak ve kardiyak debiyi desteklemek için agresif intravenöz kristalloid sıvılar verilmelidir. "
            "2. **Patolojik Tuzak (Vasküler Kaçak):** Endotel bariyeri tamamen çöktüğü için damar içine verilen sıvı damar içinde tutunamaz. "
            "Artan hidrostatik basınçla birlikte verilen sıvılar hızla interstisyel boşluğa ve akciğer alveollerine sızar. "
            "3. **Klinik Sonuç:** Aşırı sıvı yüklemesi doku ödemini, perfüzyon mesafesini ve difüzyon bariyerini artırır; "
            "özellikle Akut Respiratuar Distres Sendromu (ARDS) ve hipoksik doku nekrozunu daha da ağırlaştırabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Septik şok tablosunda hızla 30 ml/kg kristalloid infüzyonu yapılan bir hastada arteriyel oksijen satürasyonunun düştüğü ve bilateral yaygın akciğer rallerinin başladığı saptanıyor.",
                [
                    {
                        "text": "Kapiller kaçak ve ARDS riskini gözeterek agresif sıvı infüzyonunu sınırlandırmak ve erken dönemde vazopressör (noradrenalin) desteğine geçmek",
                        "isCorrect": True,
                        "explanation": "Mükemmel. Endotel kaçağı zemininde aşırı sıvı akciğer ödemini kötüleştirir; tonusu düzeltmek için erken vazopressör eklenmelidir."
                    },
                    {
                        "text": "Hipotansiyon devam ettiği için intravenöz sıvı hızını iki katına çıkarmak",
                        "isCorrect": False,
                        "explanation": "Hatalı ve tehlikeli. Aşırı sıvı infüzyonu alveoler sıvı dolumunu artırarak refrakter hipoksemiye ve arrest tablosuna yol açar."
                    }
                ]
            ),
            make_cloze(
                "Septik şokta endotel hasarı nedeniyle damar içi sıvının alveollere sızarak refrakter hipoksemi oluşturduğu akciğer patolojisine ARDS denir.",
                "ARDS",
                "Akut respiratuar distres sendromunun standart medikal kısaltması"
            )
        ]
    })

    # Slayt 79: Checkpoint 8
    slides.append({
        "id": "k1-24-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Septik Şok Patogenezi, Endotel Yıkımı ve DİK Kaskadı",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 79,
        "narrative": (
            "Bu sekizinci kontrol noktasında, septik şokun moleküler patogenezini ve DİK mekanizmasını özetliyoruz: "
            "1. **En Sık Etken:** Modern tıpta septik şokun en sık etkeni Gram-pozitif bakterilerdir (%40-50). "
            "2. **LPS ve TLR-4:** Gram-negatif endotoksinin Lipid A parçası, LBP aracılığıyla TLR-4/CD14 reseptörüne bağlanır. "
            "3. **Sitokin Fırtınası:** NF-kappaB aktivasyonuyla makrofajlardan masif TNF-alfa ve IL-1 salınır. "
            "4. **Endotel Disfonksiyonu:** Damar geçirgenliği artar (kapiller kaçak), aşırı NO üretimiyle vazomotor tonus çöker. "
            "5. **Prokoagülan Dönüşüm:** Doku faktörü (TF) artar; trombomodulin, Protein C ve TFPI azalır; PAI-1 fibrinolizi durdurur. "
            "6. **DİK Tablosu:** Mikrovasküler trombüsler (iskemi) ile pıhtılaşma faktörlerinin tükenmesi (kanama) bir arada seyreder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s79-1",
                "Gram-negatif bakteri lipopolisakkaritinin (LPS) makrofajlar üzerinde sinyal iletimi başlatan primer Toll-benzeri proteini hangisidir?",
                "Dördüncü tip transmembran Toll algılayıcısı (TLR-4).",
                "CD14 kümesiyle eşleşerek bakteriyel endotoksin tanıyan savunma molekülü",
                "TLR-4 Reseptörü"
            ),
            make_flashcard(
                "k1-24-fc-s79-2",
                "Septik şokta endotelin antitrombotik durumdan prokoagülan fenotipe geçişinde ekstrinsik koagülasyonu başlatan membran glikoproteini nedir?",
                "Tromboplastin (Doku Faktörü / TF).",
                "Mononükleer fagositlerden açılarak kalsiyum varlığında yedinci kaskadı tetikleyen bileşen",
                "Doku Faktörü Aktivasyonu"
            ),
            make_flashcard(
                "k1-24-fc-s79-3",
                "DİK tablosunda mikrovasküler fibrin pıhtılarının eritilmesini engelleyen ve endotelden aşırı salınan temel mediyatör hangisidir?",
                "Serpin ailesinden t-PA blokörü (PAI-1).",
                "Damar içi çözülmeyi engelleyen endotelyal baskılayıcı",
                "PAI-1 ve Fibrinoliz Blokajı"
            )
        ],
        "interactiveElements": [
            make_table(
                "Septik Şok Moleküler Patogenez Özeti",
                ["Evre / Mekanizma", "Moleküler Oyuncular", "Hücresel Yanıt", "Nihai Patolojik Sonuç"],
                [
                    ["PAMP Tanıma", "LPS (Lipid A), LBP, CD14, TLR-4", "NF-kappaB nükleer translokasyonu", "Sitokin genlerinin transkripsiyonu"],
                    ["Sitokin Fırtınası", "TNF-alfa, IL-1, IL-6, kemokinler", "Lökosit ve endotel aktivasyonu", "Sistemik inflamatuar yanıt"],
                    [
                        "Koagülopati (DİK)",
                        "Doku Faktörü artışı, PAI-1 artışı, TM kaybı",
                        {"text": "Tüketim koagülopatisi ve mikrotrombüsler", "isMasked": True, "hint": "Trombin fırtınası sonucu faktörlerin tükenmesi"},
                        "Organ iskemisi ve spontan kanama"
                    ],
                    ["Hemodinamik Çöküş", "İndüklenebilir NO, kapiller kaçak", "Düz kas felci ve plazma sızıntısı", "Refrakter hipotansiyon ve şok"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi septik şok zemininde endotel hücrelerinde meydana gelen değişikliklerden biri DEĞİLDİR?",
                {
                    "A": "Doku Faktörü (TF) ekspresyonunun baskılanması",
                    "B": "Trombomodulin ekspresyonunun dramatik azalması",
                    "C": "Plazminojen Aktivatör İnhibitörü-1 (PAI-1) sentezinin artması",
                    "D": "Lökosit adezyon moleküllerinin (ICAM-1, VCAM-1) artması",
                    "E": "İndüklenebilir nitrik oksit senteziyle yaygın vazodilatasyon gelişmesi"
                },
                "A",
                {
                    "A": "Doğrudur; Doku Faktörü baskılanmaz, AKSİNE masif olarak eksprese edilir ve koagülasyonu başlatır.",
                    "B": "Yanlış; trombomodulin azalır ve antikoagülan savunma çöker.",
                    "C": "Yanlış; PAI-1 artar ve fibrinoliz bloke olur.",
                    "D": "Yanlış; lökosit adezyon molekülleri belirgin artar.",
                    "E": "Yanlış; aşırı NO senteziyle damar tonusu felce uğrar."
                }
            )
        ]
    })

    # Slayt 80: Bölüm Özeti: İmmünopatolojiden Metabolik Bozukluklar ve MODS'a Geçiş
    slides.append({
        "id": "k1-24-s80",
        "title": "Bölüm Özeti: İmmünopatolojiden Metabolik Bozukluklar ve MODS'a Geçiş",
        "section": "Septik Şok Patogenezi: İnflamasyon, Endotel Hasarı ve DİK",
        "slideNumber": 80,
        "narrative": (
            "Septik şok patogenezinde endotel hasarı ve DİK kaskadı tamamlandığında, hasar sadece vasküler lümenle sınırlı kalmaz: "
            "1. **Perfüzyon ve Oksijen İletim Blokajı:** Yaygın mikrotrombüsler ve interstisyel ödem, oksijenin kandan hücrelere "
            "difüzyonunu fiziksel olarak imkansız hale getirir. "
            "2. **Hücresel Düzeyde Çöküş:** Dokular hipoksiye sürüklendikçe aerobik solunum durur ve laktik asidoz başlar. "
            "Sitokinler mitokondrileri doğrudan zehirler ve hücresel enerji metabolizmasını felç eder. "
            "3. **Sonraki Bölüme Köprü:** Bir sonraki bölümümüzde hücresel metabolik anormallikleri (hiperlaktatemi, insülin direnci), "
            "adrenal yetmezliği (Waterhouse-Friderichsen sendromu) ve şokun organlar üzerindeki spesifik histopatolojisini "
            "(şok akciğeri/ARDS, şok böbreği/ATN ve sentrilobüler karaciğer nekrozu) inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Septik Şok Hasarının Yayılımı",
                "Vasküler ve İmmünopatolojik Faz",
                "TLR-4 uyarımı, sitokin fırtınası, yaygın endotel kaçağı ve mikrovasküler fibrin mikrotrombüsleri",
                "Metabolik ve Organ Yetmezliği Fazı (MODS)",
                "Mitokondriyal enerji felci, laktik asidoz, akut tübüler nekroz ve alveolar hasar (ARDS)"
            ),
            make_active_recall(
                "Septik şokta doku hipoperfüzyonu ve mitokondriyal fonksiyon kaybının kanda oluşturduğu en temel metabolik asidoz tipi hangisidir?",
                "Laktik asidoz tablosudur (Hiperlaktatemi).",
                "Anaerobik glikoliz sonucu üretilen asit metaboliti"
            )
        ]
    })

    return slides
