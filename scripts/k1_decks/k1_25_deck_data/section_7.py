# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 7: IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD (Slayt 61 - 70)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # Slayt 61: IgG4 İlişkili Hastalık (IgG4-RD): Tanım ve Üçlü Histopatolojik Damga
    slides.append({
        "id": "k1-25-s61",
        "title": "IgG4 İlişkili Hastalık (IgG4-RD): Tanım ve Üçlü Histopatolojik Damga",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 61,
        "narrative": (
            "IgG4 ilişkili hastalık (IgG4-RD), farklı organlarda tümör benzeri kitleler oluşturan, serumda IgG4 düzeylerinin "
            "yüksekliği ve dokuda özgül histopatolojik bulgularla karakterize fibroinflamatuvar sistemik bir antitedir: "
            "1. **Üçlü Histopatolojik Damga:** "
            "- **IgG4+ Plazma Hücre İnfiltratı:** Biyopside mononükleer hücreler arasında bol miktarda IgG4 pozitif plazma hücresi "
            "saptanır (IgG4+/IgG+ plazma hücresi oranı >%40 tanısaldır). "
            "- **Storiform Fibrozis:** Kollajen liflerinin girdap, fırıldak veya hasır örgüsü şeklinde dizildiği karakteristik fibrozis mimarisidir. "
            "- **Obliteratif Flebit:** Küçük ve orta çaplı venlerin lümeninin lenfoplazmasitik infiltrat ve fibröz dokuyla tamamen tıkanmasıdır. "
            "2. **Klinik Formlar:** Tip 1 Otoimmün Pankreatit, Riedel Tiroiditi, Retroperitoneal Fibrozis (Ormond hastalığı), "
            "Mikulicz hastalığı (tükürük/gözyaşı bezi şişmesi) ve inflamatuar aort anevrizması. Lezyonlar maligniteyi taklit eder "
            "fakat sistemik kortikosteroid tedavisine dramatik derecede hızlı yanıt verir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "IgG4 İlişkili Hastalığın Üçlü Histopatolojik Kriterleri",
                ["Patolojik Kriter", "Mikroskobik Özellik", "Tanısal Değeri"],
                [
                    ["Yoğun Lenfoplazmasitik İnfiltrat", "IgG4+ plazma hücreleri (IgG4/IgG oranı >%40)", "Hastalığın immünohistokimyasal imzası"],
                    [
                        "Storiform Fibrozis",
                        {"text": "Hasır örgüsü veya fırıldak biçimli kollajen dizilimi", "isMasked": True, "hint": "Kollajen demetlerinin girdap şeklinde sarmal oluşturduğu mimari"},
                        "Sklerozan doku mimarisinin patognomonik deseni"
                    ],
                    ["Obliteratif Flebit", "Ven duvarının lenfositlerle sarılıp lümenin tıkanması", "Arterleri korurken venöz dolaşımı söndüren lezyon"]
                ]
            ),
            make_active_recall(
                "Pankreasta veya tiroidde kitle oluşturan IgG4 ilişkili hastalık biyopsisinde kollajen liflerinin hasır örgüsü veya fırıldak benzeri girdaplar oluşturduğu karakteristik fibrozis tipine ne ad verilir?",
                "Storiform fibrozis denir.",
                "Dönen tekerlek veya sepet örgüsü benzeri bağ dokusu deseni"
            )
        ]
    })

    # Slayt 62: Transplant Reddi İmmünolojisi: Doğrudan ve Dolaylı Alloantijen Tanıma
    slides.append({
        "id": "k1-25-s62",
        "title": "Transplant Reddi İmmünolojisi: Doğrudan ve Dolaylı Tanıma",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 62,
        "narrative": (
            "Transplantasyon reddi (rejeksiyon), alıcının bağışıklık sisteminin donör dokusundaki allojenik molekülleri "
            "(özellikle MHC / HLA Sınıf I ve II antijenlerini) yabancı tanıması sonucu grefti yıkıma uğratmasıdır: "
            "1. **Doğrudan (Direkt) Tanıma Yolağı:** "
            "- Donör organın içinde göçmen olarak gelen **donör antijen sunucu hücreleri (otostopçu APC'ler)**, "
            "kendi yüzeylerindeki sağlam donör MHC moleküllerini alıcı T lenfositlerine doğrudan sunar. "
            "- Alıcı CD8+ CTL'leri yabancı donör MHC-I'i, CD4+ T hücreleri ise donör MHC-II'yi tanır. "
            "- **Akut hücresel reddin** erken ve en şiddetli patogenetik yoludur. "
            "2. **Dolaylı (İndirekt) Tanıma Yolağı:** "
            "- Alıcının kendi APC'leri donör greft hücrelerinden dökülen yabancı MHC moleküllerini endositozla alır, "
            "normal bir mikrop gibi parçalar ve kendi alıcı MHC-II molekülleri üzerinde CD4+ T hücrelerine sunar. "
            "- Bu yol antikor üretimini ve **kronik transplant reddini** yönetir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Doğrudan vs Dolaylı Alloantijen Tanıma Ayrımı",
                "Doğrudan (Direkt) Tanıma",
                "Alıcı T hücresinin greftteki donör APC yüzeyindeki sağlam yabancı MHC'yi doğrudan tanıması (Akut ret motoru)",
                "Dolaylı (İndirekt) Tanıma",
                "Alıcı APC'lerinin donör proteinlerini parçalayıp kendi MHC'sinde sunması (Kronik ret ve antikor motoru)"
            ),
            make_micro_quiz(
                "Transplantasyon immünolojisinde alıcı CD8+ ve CD4+ T lenfositlerinin greft dokusu içindeki donör antijen sunucu hücrelerinin yüzeyindeki intakt yabancı MHC moleküllerini doğrudan tanıması hangi tanıma yolağıdır?",
                {
                    "A": "Doğrudan (Direkt) tanıma yolağı",
                    "B": "Dolaylı (İndirekt) tanıma yolağı",
                    "C": "Kross-prezantasyon yolağı",
                    "D": "Toll-benzeri reseptör yolağı",
                    "E": "Kompleman alternatif yolağı"
                },
                "A",
                {
                    "A": "Doğrudur; greftteki yabancı APC'lerin intakt MHC'sinin tanınması doğrudan (direkt) alloreaktivite yolağıdır.",
                    "B": "Yanlış; dolaylı yol alıcının kendi APC'sinin donör proteinini parçalamasıdır.",
                    "C": "Yanlış; kross-prezantasyon eksojen antijenin MHC-I ile sunulmasıdır.",
                    "D": "Yanlış; TLR doğuştan bağışıklık reseptörüdür.",
                    "E": "Yanlış; kompleman yoludur."
                }
            )
        ]
    })

    # Slayt 63: Hiperakut Transplant Reddi: Önceden Var Olan Antikorlar ve Tromboz
    slides.append({
        "id": "k1-25-s63",
        "title": "Hiperakut Transplant Reddi: Önceden Var Olan Antikorlar ve Tromboz",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 63,
        "narrative": (
            "Hiperakut ret, cerrahi vasküler anastomozlar tamamlanıp kan akımı sağlandıktan sonra **dakikalar veya birkaç saat içinde** gelişir: "
            "1. **Patogenetik Zemin:** Alıcının dolaşımında donör endotel antijenlerine karşı **önceden var olan (preforme) antikorların** "
            "bulunmasıdır. Bu antikorlar daha önceki kan transfüzyonları, çoklu gebelikler veya geçirilmiş başarısız bir transplantasyonla oluşmuştur. "
            "2. **Histopatoloji ve Morfoloji:** "
            "- Preforme antikorlar donör vasküler endoteline anında yapışır; klasik kompleman yolağı masif olarak tetiklenir. "
            "- Endotel nekroze olur, bazal membran açığa çıkar; tüm damar lümenlerinde **yaygın trombosit-fibrin mikrotrombüsleri** oluşur. "
            "- Greft damarları tamamen tıkanır; organ ameliyat masasında pembeden aniden mor-siyanotik, soğuk ve gevşek bir kitleye döner. "
            "3. **Önleme:** Ameliyat öncesi donör lenfositleri ile alıcı serumu arasında yapılan **çapraz eşleştirme (cross-match)** testiyle önlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Hiperakut Rejeksiyon Kaskadı",
                [
                    "1. Anastomoz ve Perfüzyon: Ameliyat masasında donör organ damarlarının alıcı dolaşımına bağlanması",
                    "2. Preforme Antikor Bağlanması: Alıcıdaki hazır antikorların donör vasküler endoteline saniyeler içinde yapışması",
                    "3. Kompleman Aktivasyonu ve Lizis: C5b-9 MAC kompleksiyle endotel hücrelerinin nekroza uğraması",
                    "4. Masif Tromboz ve Nekroz: Kılcal damarlarda fibrin mikrotrombüsleri ile greftin dakikalar içinde morarıp ölmesi"
                ]
            ),
            make_cloze(
                "Transplantasyon ameliyatı sırasında dakikalar içinde greftin trombotik tıkanmasına ve nekrozuna yol açan hiperakut reddin temel nedeni alıcıda önceden var olan antikorlardır.",
                "önceden var olan",
                "Önceki kan nakli veya gebelikle kanda hazır bulunan preforme antikor durumu"
            )
        ]
    })

    # Slayt 64: Akut Hücresel ve Akut Hümoral (Antikor Aracılı) Transplant Reddi
    slides.append({
        "id": "k1-25-s64",
        "title": "Akut Hücresel ve Akut Hümoral (Antikor Aracılı) Transplant Reddi",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 64,
        "narrative": (
            "Akut ret, transplantasyondan sonraki günler, haftalar veya aylar içinde ortaya çıkan iki farklı immün tablodur: "
            "1. **Akut Hücresel Ret (T Hücre Aracılı):** "
            "- **Mekanizma:** Doğrudan alloreaktivite ile uyarılmış CD8+ sitotoksik T hücreleri ve CD4+ Th1 hücreleri greft parankimine sızar. "
            "- **Böbrek Biyopsisi Damgaları:** Lenfositler tübül epitel hücrelerinin arasına girerek bazal membranı yırtar (**tubulit**) "
            "ve arter endoteli altına sızarak endoteli lümene doğru kabartır (**endotelit / intimitis**). İmmünsüpresyona mükemmel yanıt verir. "
            "2. **Akut Hümoral (Antikor Aracılı) Ret:** "
            "- **Mekanizma:** Nakilden sonra alıcı B hücreleri donör HLA'sına karşı yeni antikorlar (**Donor-Spesifik Antikorlar / DSA**) üretir. "
            "- **Histopatolojik Damga (C4d Birikimi):** Antikorlar peritübüler kapiller endoteline bağlanır ve komplemanı fikse eder. "
            "Kapiller duvarında kompleman parçalanma ürünü olan **C4d'nin pozitif boyanması** antikor aracılı reddin patognomonik kanıtıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Akut Hücresel vs Akut Antikor Aracılı Rejeksiyon Ayrımı",
                ["Özellik", "Akut Hücresel Ret", "Akut Hümoral (Antikor Aracılı) Ret"],
                [
                    ["Primer İmmün Efektör", "CD8+ CTL ve CD4+ T lenfositleri", "De novo donör-spesifik antikorlar (DSA)"],
                    [
                        "Böbrek Biyopsisindeki Damga",
                        "Tubulit ve endotelit (intimal arterit)",
                        {"text": "Peritübüler kapillerlerde C4d birikimi", "isMasked": True, "hint": "Kompleman aktivasyonunun kapiller endotelindeki floresan kanıtı"}
                    ],
                    ["Etkilenen Mikroanatomi", "Tübül epiteli ve interstisyum", "Peritübüler kapillerler ve glomerül kılcalları"],
                    ["Tedavi Stratejisi", "Yüksek doz pulse kortikosteroid", "Plazmaferez, IVIG ve rituksimab"]
                ]
            ),
            make_active_recall(
                "Böbrek allogreft biyopsisinde antikor aracılı (hümoral) akut reddi doğrulamak için peritübüler kapiller endotelinde immünohistokimya ile aranan patognomonik kompleman parçalanma ürünü hangisidir?",
                "C4d birikimidir.",
                "Klasik kompleman aktivasyonunun endotel bazal zarına kovalent yapışan stabil fragmanı"
            )
        ]
    })

    # Slayt 65: Kronik Transplant Reddi: Vasküler Oklüzyon ve İnterstisyel Fibrozis
    slides.append({
        "id": "k1-25-s65",
        "title": "Kronik Transplant Reddi: Vasküler Oklüzyon ve İnterstisyel Fibrozis",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 65,
        "narrative": (
            "Kronik ret, nakilden aylar veya yıllar sonra ortaya çıkan, yavaş ilerleyen ve immünsüpresif tedaviye dirençli greft kaybıdır: "
            "1. **Patogenez (Dolaylı Tanıma ve Sitokinler):** Alıcı APC'lerinin sunduğu donör peptitleriyle kronik olarak uyarılan "
            "T hücreleri sürekli makrofaj aktivasyonu yapar. Salınan büyüme faktörleri (PDGF, TGF-beta, FGF) damar düz kaslarını uyarır. "
            "2. **Hızlanmış Greft Arteriyosklerozu:** Arter lümeninde düz kas hücrelerinin intimaya göçü, proliferasyonu ve masif "
            "kollajen birikimi izlenir (**intimal fibromusküler hiperplazi**). Arteriyel lümenler konsantrik olarak daralır ve tıkanır. "
            "3. **Parankimal İflas:** Kronik iskemiye bağlı olarak böbrekte yaygın tübüler atrofi ve **interstisyel fibrozis** gelişir "
            "(Kronik allogreft nefropatisi). Kalp naklinde koroner arter tıkanıklıkları, akciğerde obliteratif bronşiyolit izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Akut vs Kronik Rejeksiyon Histopatolojisi",
                "Akut Transplant Reddi",
                "İnterstisyel yoğun lenfosit infiltrasyonu, tubulit, endotelit ve immünsüpresyonla geri döndürülebilir hasar",
                "Kronik Transplant Reddi",
                "İntimal fibromusküler daralma (hızlanmış arteriyoskleroz), tübüler atrofi, interstisyel fibrozis ve geri dönüşümsüz greft kaybı"
            ),
            make_micro_quiz(
                "Transplantasyondan 3 yıl sonra böbrek fonksiyonları sinsi biçimde bozulan bir hastanın biyopsisinde arter lümenlerinde konsantrik intimal düz kas proliferasyonu (hızlanmış arteriyoskleroz), tübüler atrofi ve interstisyel fibrozis saptanıyor. En olası tanı hangisidir?",
                {
                    "A": "Kronik transplant reddi (Kronik allogreft nefropatisi)",
                    "B": "Hiperakut rejeksiyon",
                    "C": "Akut tubulit rejeksiyonu",
                    "D": "Minimal değişiklik hastalığı",
                    "E": "Akut piyelonefrit"
                },
                "A",
                {
                    "A": "Doğrudur; hızlanmış greft arteriyosklerozu ve interstisyel fibrozis kronik reddin patognomonik tablosudur.",
                    "B": "Yanlış; hiperakut ameliyat masasında ilk saatlerde tromboz yapar.",
                    "C": "Yanlış; tubulit akut hücresel rettiğe aittir.",
                    "D": "Yanlış; podosit silinmesiyle seyreden nefrotik sendromdur.",
                    "E": "Yanlış; nötrofilik bakteriyel enfeksiyondur."
                }
            )
        ]
    })

    # Slayt 66: Kemik İliği Nakli İmmünolojisi ve GVHD Paradoksu
    slides.append({
        "id": "k1-25-s66",
        "title": "Kemik İliği Nakli İmmünolojisi ve GVHD Paradoksu",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 66,
        "narrative": (
            "Hematopoietik kök hücre ve kemik iliği naklinde immünolojik reddin yönü geleneksel organ naklinin tam tersidir: "
            "1. **Biyolojik Hazırlık (Kondisyonlama):** Lösemi veya kemik iliği yetmezliği olan alıcıya yüksek doz kemoterapi ve "
            "radyoterapi verilerek alıcının kendi kemik iliği ve immün sistemi tamamen sıfırlanır (myeloablasyon). "
            "2. **GVHD Paradoksu (Graft Alıcıya Karşı):** "
            "- Donörden alınan kemik iliği süspansiyonunda hematopoietik kök hücrelerin yanı sıra matür donör T lenfositleri bulunur. "
            "- Nakledilen bu **donör T lenfositleri**, bağışıklık sistemi sıfırlanmış savunmasız alıcının vücudunu 'tamamen yabancı' olarak algılar. "
            "- Greft donör T hücreleri alıcının sağlıklı organlarına saldırarak öldürücü bir sistemik yıkım başlatır; bu tabloya "
            "**Graft Versus Host Hastalığı (GVHD)** adı verilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Organ Nakli Rejeksiyonu vs Kemik İliği GVHD Paradoksu",
                ["Özellik", "Solid Organ Nakli (Böbrek/Kalp)", "Kemik İliği / Kök Hücre Nakli (GVHD)"],
                [
                    ["Saldıran İmmün Sistem", "Alıcının kendi T ve B lenfositleri", "Greftle verilen DONÖR T lenfositleri"],
                    ["Saldırıya Uğrayan Hedef", "Yalnızca nakledilen donör organı", "Alıcının tüm vücudu ve sağlıklı organları"],
                    [
                        "Alıcının İmmün Durumu",
                        "İmmünokompetan (kendi bağışıklığı var)",
                        {"text": "İmmünosüprese / Myeloablatif (sıfırlanmış)", "isMasked": True, "hint": "Kök hücre nakli öncesi radyoterapiyle bağışıklığın felç edilmesi"}
                    ],
                    ["Klinik Sonuç", "Greft reddi ve organ iflası", "Sistemik GVHD (Deri, karaciğer, bağırsak iflası)"]
                ]
            ),
            make_active_recall(
                "Kemik iliği naklinde donör T lenfositlerinin immünitesi sıfırlanmış alıcının dokularına saldırarak multiorgan hasarı oluşturduğu öldürücü tabloya ne ad verilir?",
                "Graft Versus Host Hastalığı (GVHD) denir.",
                "Graftın konak dokularına saldırdığı alloimmün reaksiyon"
            )
        ]
    })

    # Slayt 67: Akut GVHD Patolojisi ve Üç Klasik Hedef Organ
    slides.append({
        "id": "k1-25-s67",
        "title": "Akut GVHD Patolojisi ve Üç Klasik Hedef Organ",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 67,
        "narrative": (
            "Akut GVHD, kök hücre naklinden sonraki ilk 100 gün içinde (genellikle ilk 2-4 haftada) gelişen fırtınadır: "
            "Donör T hücreleri (özellikle CD8+ sitotoksik T hücreleri) alıcı dokularında üç klasik organı hedefler: "
            "1. **Deri Tutulumu:** Genellikle ilk belirtidir. Avuç içi, ayak tabanı ve boyundan başlayan kaşıntılı makülopapüler döküntü. "
            "Histopatolojide dermo-epidermal bileşkede bazal tabaka vakuolizasyonu ve tek tek keratinositlerin apoptoza uğraması izlenir. "
            "Ağır vakalarda tüm epidermis bülleşerek soyulur (Toksik Epidermal Nekroliz benzeri dökülme). "
            "2. **Karaciğer Tutulumu:** Donör lenfositleri küçük intrahepatik safra kanalı epitelini doğrudan parçalar. "
            "Kanaliküler hasar sonucu safra göllenir; derin kolestaz, belirgin sarılık ve hiperbilirubinemi gelişir. "
            "3. **Gastrointestinal Sistem:** Mide ve bağırsak kript epitel hücreleri apoptozla dökülür. Mukozada erezyonlar açılır; "
            "günde birkaç litreyi bulan sulu, kanlı inatçı diyare ve kramplar oluşur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Akut GVHD Üç Klasik Hedef Organı ve Histopatolojisi",
                ["Hedef Organ", "Karakteristik Histopatolojik Lezyon", "Klinik Yansıması", "Ölümcül Risk"],
                [
                    ["Deri", "Bazal tabaka vakuolizasyonu, keratinosit apoptozu", "Avuç içi/boyundan başlayan eritematöz döküntü", "Yaygın bül ve epidermal soyulma"],
                    [
                        "Karaciğer",
                        "İntrahepatik safra kanalı nekrozu ve kolestaz",
                        {"text": "Aşırı konjuge hiperbilirubinemi ve sarılık", "isMasked": True, "hint": "Safra yolları yıkımı sonucu hastanın derisinin sapsarı olması"},
                        "Hepatik yetmezlik"
                    ],
                    ["GİS (Bağırsak)", "Kript epiteli apoptozu ve mukozal dökülme", "Günde litrelerce süren kanlı sulu diyare", "Masif elektrolit kaybı ve sepsis"]
                ]
            ),
            make_active_recall(
                "Allojenik kemik iliği naklinden 3 hafta sonra gelişen akut GVHD tablosunda etkilenen üç klasik hedef organ hangileridir?",
                "Deri, karaciğer ve gastrointestinal sistemdir (bağırsaklar).",
                "Döküntü, sarılık ve kanlı diyare ile seyreden üçlü organ grubu"
            )
        ]
    })

    # Slayt 68: Kronik GVHD Patolojisi ve Skleroderma Benzeri Tablo
    slides.append({
        "id": "k1-25-s68",
        "title": "Kronik GVHD Patolojisi ve Skleroderma Benzeri Tablo",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 68,
        "narrative": (
            "Kronik GVHD, nakilden 100 günden sonra ortaya çıkan ve sistemik otoimmün hastalıkları (özellikle sklerodermayı) taklit eden tablodur: "
            "1. **Patogenez:** Akut fazdaki sitotoksisitenin yerini T hücre sitokinlerinin (TGF-beta) fibroblastları aralıksız uyarması alır. "
            "2. **Deri (Skleroderma Benzeri):** Dermiste aşırı kollajen birikimi ve kıl folikülü/adneks kaybı izlenir. "
            "Deri taş gibi sertleşir, parmaklarda kontraktürler gelişir. "
            "3. **Ekzokrin Bezler (Sjögren Benzeri):** Tükürük ve lakrimal bezlerin fibrozisle tahrip olması sonucu ağır kseroftalmi "
            "ve kserostomi (kuru göz ve kuru ağız) ortaya çıkar. "
            "4. **Akciğer ve Karaciğer:** Küçük hava yollarının fibröz daralması sonucu **obliteratif bronşiyolit** gelişir; "
            "karaciğerde safra kanalları tamamen silinir (**vanishing bile duct sendromu**)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Akut vs Kronik GVHD Klinik Ayrımı",
                "Akut GVHD (İlk 100 Gün)",
                "Keratinosit apoptozuyla döküntü, safra kanalı nekrozuyla sarılık ve kript lizisiyle masif kanlı diyare",
                "Kronik GVHD (>100 Gün)",
                "Skleroderma benzeri deri taşlaşması, Sjögren benzeri ağız/göz kuruluğu ve obliteratif bronşiyolit"
            ),
            make_micro_quiz(
                "Kemik iliği naklinden 6 ay sonra derisinde taş gibi sertleşme (skleroderma benzeri fibrozis), göz ve ağız kuruluğu ile nefes darlığı gelişen bir hastada en olası tanı hangisidir?",
                {
                    "A": "Kronik Graft Versus Host Hastalığı (Kronik GVHD)",
                    "B": "Akut hiperakut rejeksiyon",
                    "C": "Primer dermatomiyozit",
                    "D": "İzole Goodpasture sendromu",
                    "E": "Tüberkülin deri reaksiyonu"
                },
                "A",
                {
                    "A": "Doğrudur; kök hücre nakli sonrası 100 günden geç gelişen skleroderma ve Sjögren benzeri sistemik fibrozis kronik GVHD tablosudur.",
                    "B": "Yanlış; hiperakut saatler içinde gelişir.",
                    "C": "Yanlış; dermatomiyozit nakil komplikasyonu değildir.",
                    "D": "Yanlış; Goodpasture Tip II nefritidir.",
                    "E": "Yanlış; PPD lokal deri testidir."
                }
            )
        ]
    })

    # Slayt 69: Checkpoint 7
    slides.append({
        "id": "k1-25-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 69,
        "narrative": (
            "Bu yedinci kontrol noktasında, IgG4 ilişkili hastalığı ve transplantasyon immünopatolojisini özetliyoruz: "
            "1. **IgG4-RD:** IgG4+ plazma hücreleri (>%40), girdap desenli storiform fibrozis ve venleri tıkayan obliteratif flebit üçlüsüdür. "
            "2. **Hiperakut Ret:** Preforme antikorlar ameliyat masasında dakikalar içinde kompleman aktivasyonu ve masif mikrotromboz yapar. "
            "3. **Akut Hücresel Ret:** CD8+ CTL'lerin yaptığı tubulit ve endotelit (intimal arterit) tablosudur. "
            "4. **Akut Hümoral Ret:** De novo donör-spesifik antikorlar peritübüler kapillerlerde patognomonik C4d birikimi yapar. "
            "5. **Kronik Ret:** İntimal fibromusküler hiperplazi (hızlanmış greft arteriyosklerozu) ve interstisyel fibrozistir. "
            "6. **GVHD:** Kemik iliği naklinde donör T hücrelerinin alıcı derisine (apoptoz), karaciğerine (kolestaz) ve bağırsağına (kanlı diyare) saldırmasıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s69-1",
                "Akut antikor aracılı (hümoral) transplant reddinde peritübüler kapiller endotelinde patognomonik olarak saptanan kompleman parçalanma belirteci nedir?",
                "C4d proteini birikimidir.",
                "Klasik aktivasyon kaskadının kapiller bazal membranına bağlanan kararlı opsonin türevi",
                "C4d ve Hümoral Ret"
            ),
            make_flashcard(
                "k1-25-fc-s69-2",
                "Transplantasyon ameliyatında cerrahi anastomoz sonrası dakikalar içinde trombotik tıkanma ve greft siyanozu yapan hiperakut reddin temel etyolojisi nedir?",
                "Alıcıda hazır bulunan preforme antikorlardır.",
                "Eski kan nakilleri veya çoklu gebelikler sonucu dolaşımda bekleyen donör spesifik immünoglobulin havuzu",
                "Hiperakut Ret Etyolojisi"
            ),
            make_flashcard(
                "k1-25-fc-s69-3",
                "Kemik iliği naklinden sonra gelişen akut GVHD tablosunda donör lenfositlerinin sitotoksik hasar verdiği üç ana anatomik hedef bölge neresidir?",
                "Deri, karaciğer ve sindirim sistemi parankimidir.",
                "Epidermal büllü eritem, safra kanalı tıkanma sarılığı ve kanamalı enterit tablosu",
                "Akut GVHD Hedef Organları"
            )
        ],
        "interactiveElements": [
            make_table(
                "Transplant Reddi Tipleri Büyük Karşılaştırma Tablosu",
                ["Rejeksiyon Tipi", "Başlangıç Zamanı", "Temel İmmün Mekanizma", "Histopatolojik Karakteristik"],
                [
                    ["Hiperakut Ret", "Dakikalar - Saatler", "Preforme antikorlar ve kompleman", "Yaygın trombotik tıkanma, fibrin nekrozu"],
                    ["Akut Hücresel Ret", "Günler - Haftalar", "CD8+ sitotoksik T hücreleri", "Tubulit ve intimal arterit (endotelit)"],
                    [
                        "Akut Hümoral Ret",
                        "Günler - Haftalar",
                        "De novo antikorlar (DSA)",
                        {"text": "Peritübüler kapiller C4d birikimi", "isMasked": True, "hint": "Mikrovasküler endotelde kompleman birikim kanıtı"}
                    ],
                    ["Kronik Ret", "Aylar - Yıllar", "Dolaylı alloreaktivite, büyüme faktörleri", "Hızlanmış arteriyoskleroz, interstisyel fibrozis"]
                ]
            ),
            make_micro_quiz(
                "Böbrek transplantasyonu yapılan bir hastanın 2. haftada yapılan biyopsisinde tübül epitel hücreleri arasına lenfosit infiltrasyonu (tubulit) ve arteriyel intimanın altında lenfositik kabarma (endotelit) saptanıyor. En olası tanı hangisidir?",
                {
                    "A": "Akut hücresel transplant reddi",
                    "B": "Hiperakut rejeksiyon",
                    "C": "Kronik greft nefropatisi",
                    "D": "Akut GVHD",
                    "E": "Posttransplant lenfoproliferatif hastalık"
                },
                "A",
                {
                    "A": "Doğrudur; tubulit ve endotelit akut hücresel (T hücre aracılı) transplant reddinin klasik histopatolojik bulgularıdır.",
                    "B": "Yanlış; hiperakut trombotiktir ve ilk saatlerde olur.",
                    "C": "Yanlış; kronik ret fibromusküler intimal daralma ve fibrozis yapar.",
                    "D": "Yanlış; GVHD kemik iliği naklinde donörün alıcıya saldırmasıdır.",
                    "E": "Yanlış; PTLD EBV ilişkili lenfomadır."
                }
            )
        ]
    })

    # Slayt 70: Bölüm Özeti: Alloimmüniteden Primer İmmün Yetmezliklere Geçiş
    slides.append({
        "id": "k1-25-s70",
        "title": "Bölüm Özeti: Alloimmüniteden Primer İmmün Yetmezliklere Geçiş",
        "section": "IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD",
        "slideNumber": 70,
        "narrative": (
            "Buraya kadar bağışıklık sisteminin aşırı çalıştığı (Hipersensitivite), kendine saldırdığı (Otoimmünite) "
            "veya yabancı nakil organını reddettiği (Alloimmünite) durumları inceledik: "
            "1. **Tablonun Diğer Yüzü:** Ancak immün sistem her zaman aşırı çalışmaz; bazen genetik mutasyonlar nedeniyle "
            "bağışıklığın temel bileşenleri hiç üretilemez veya fonksiyon göremez. "
            "2. **İmmün Yetmezlikler:** Bağışıklık sisteminin mikroplara karşı savunma yapamadığı bu tablolara **İmmün Yetmezlik Sendromları** denir. "
            "B hücre kusurları tekrarlayan piyojenik bakteriyel enfeksiyonlara yol açarken; T hücre kusurları fırsatçı mantar, virüs ve protozoon enfeksiyonlarına zemin hazırlar. "
            "Bölüm 8'de Bruton agamaglobulinemisinden SCID ve DiGeorge sendromuna kadar primer immün yetmezlikleri inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "İmmün Disfonksiyon Kutupları",
                "Aşırı İmmün Yanıt (Hipersensitivite / Otoimmünite)",
                "İmmün sistemin kontrolsüz hiperaktivitesi, kendi organlarına veya çevresel alerjenlere saldırarak doku hasarı yapması",
                "Yetersiz İmmün Yanıt (İmmün Yetmezlik)",
                "B, T veya kompleman bileşenlerinin genetik yokluğu, fırsatçı patojenlerle fatal enfeksiyonlar ve erken ölüm"
            ),
            make_active_recall(
                "Genetik mutasyonlar sonucu B lenfositleri, T lenfositleri veya fagositoz mekanizmalarının doğuştan kusurlu olmasına ne ad verilir?",
                "Primer (konjenital) immün yetmezlik sendromları denir.",
                "Kalıtsal bağışıklık defektleri grubu"
            )
        ]
    })

    return slides
