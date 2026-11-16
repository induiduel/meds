# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-13-s11",
        "title": "Mononükleer Fagosit Sistemi: Kemik İliğinden Dokulara",
        "content": "Mononükleer Fagosit Sistemi (MFS - eski adıyla Retiküloendotelyal Sistem), kemik iliğinde ortak bir hematopoetik kök hücreden köken alan, kan monositleri ve doku makrofajlarından oluşan bütünleşik bir hücresel savunma ağıdır:\n\n- **Gelişim Basamakları:** Kemik iliğindeki myeloid kök hücre → monoblast → promonosit → kanda dolaşan monosit.\n- **Kinetik:** Monositler kanda yaklaşık 1 gün (8-24 saat) dolaşırlar. Dokulara geçtiklerinde boyutları katlanarak artar, lizozom ve mitokondri sayıları çoğalır ve doku makrofajlarına (histiositlere) dönüşürler.\n- **Embriyonik Köken:** Bazı organlardaki yerleşik makrofajlar ise kemik iliğinden değil, embriyogenez sırasında vitellus kesesi ve fetal karaciğerden dokulara göç edip orada mitozla çoğalarak ömür boyu yerleşik kalan hücrelerdir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Mononükleer Fagosit Sistemi Farklılaşma Hattı",
                [
                    "1. Kemik İliği Öncülü: Myeloid hematopoetik kök hücreden monoblast ve promonosit oluşur.",
                    "2. Kan Dolaşımı: Monositler kana salınarak ortalama 1 gün boyunca dolaşımda devriye gezer.",
                    "3. Dokuya Ekstravazasyon: Kemotaktik sinyallerle damar dışına çıkarak doku aralığına yerleşir.",
                    "4. Makrofaj Olgunlaşması: Hücre hacmi büyür, fagositoz organelleri artar ve aktif doku makrofajı olur."
                ]
            ),
            make_cloze(
                "Kanda 1 gün dolaşan monositler dokuya geçtiklerinde hacimce büyüyüp lizozomlarını artırarak doku makrofajı haline gelir.",
                "doku makrofajı",
                "Monositin dokudaki olgun fagositer adı"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-13-s12",
        "title": "Dokuya Yerleşik Makrofajlar ve Anatomik Dağılımları",
        "content": "Vücudun farklı organ ve dokuları, kendilerine özgü mikroçevreye uyum sağlamış yerleşik (rezidan) makrofaj popülasyonlarına sahiptir:\n\n1. **Karaciğer:** Karaciğer sinüzoidlerinde yer alan ve portal kandan gelen bakterileri süzen **Kupffer hücreleri**.\n2. **Merkezi Sinir Sistemi:** Beyin parankiminde glial matriks içinde yer alan, embriyonik vitellus kesesi kökenli **Mikroglia hücreleri**.\n3. **Akciğer:** Alveol lümeninde hava ile gelen toz ve mikropları temizleyen **Alveoler makrofajlar (toz hücreleri)**.\n4. **Dalak ve Lenf Düğümleri:** Sinüs endoteli boyunca yerleşen ve yaşlı eritrositler ile lenfatik antijenleri yakalayan **Sinüs histiyositleri**.\n5. **Kemik:** Kemik matriksini yıkan çok çekirdekli dev fagositer hücreler olan **Osteoklastlar**.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Organ / Anatomik Bölge", "Yerleşik Rezidan Makrofaj Adı", "Özgül Fonksiyonu"],
                [
                    [
                        {"text": "Karaciğer Sinüzoidleri", "isMasked": False, "hint": ""},
                        {"text": "Kupffer hücreleri", "isMasked": True, "hint": "Portal kandan gelen partikülleri süzen hepatik hücreler"},
                        {"text": "Portal kan temizliği ve eritrosit yıkımı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Merkezi Sinir Sistemi", "isMasked": False, "hint": ""},
                        {"text": "Mikroglia", "isMasked": True, "hint": "Beyin parankimindeki resident fagositer hücre"},
                        {"text": "Nöronal debris temizliği ve nöroinflamasyon", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kemik Dokusu", "isMasked": True, "hint": "Kemik erimesinden sorumlu dev hücre"},
                        {"text": "Osteoklastlar", "isMasked": False, "hint": ""},
                        {"text": "Kemik rezorpsiyonu ve matriks remodelizasyonu", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Merkezi sinir sistemi parankiminde nöronal atıkları ve mikropları temizleyen mononükleer fagosit sistemi hücresi hangisidir?",
                "Mikrogliadır.",
                "Beynin rezidan makrofajı"
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-13-s13",
        "title": "Makrofaj Kemotaksisi ve MCP-1 (CCL2) Sinyali",
        "content": "Akut enflamasyonun 24-48. saatinden itibaren veya primer kronik süreçlerde monositlerin dokuya çağrılması özel kemokinler ve adezyon molekülleriyle yönlendirilir:\n\n- **Monosit Kemoatraktan Protein-1 (MCP-1 / CCL2):** Endotel, fibroblastlar ve makrofajlarca üretilen en güçlü monosit kemoatraktanıdır. Monosit yüzeyindeki CCR2 reseptörüne bağlanır.\n- **Endotel Adezyonu:** Monositler yüzeylerindeki VLA-4 (α4β1 integrin) ile endoteldeki **VCAM-1**'e, Mac-1 (αMβ2) ile **ICAM-1**'e bağlanarak venüllerden dokuya sızarlar.\n- **Klinik Önem:** MCP-1/CCR2 aksı aterosklerozda plak oluşumunun, romatoid artritte sinoviyal monosit akınının ve diyabetik nefropatide glomerüler hasarın baş sorumlusudur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Nötrofil vs Monosit Kemotaksis Sinyalleri",
                "Nötrofil Kemotaksisi (Akut Faz)",
                "IL-8 (CXCL8), LTB4 ve C5a CXCR1/2 reseptörleri üzerinden dakikalar içinde nötrofil çeker.",
                "Monosit Kemotaksisi (Kronik Faz)",
                "MCP-1 (CCL2), MIP-1alfa CCR2/5 reseptörleri üzerinden saatler-günler içinde monosit çeker."
            ),
            make_cloze(
                "Monositlerin dolaşımdan kronik enflamasyon odağına göç etmesinde rol oynayan en önemli kemokin ve reseptör çifti MCP-1 ve CCR2 aksıdır.",
                "MCP-1 ve CCR2",
                "Monosit kemoatraktan protein ve reseptör adı"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-13-s14",
        "title": "Makrofajın Dört Temel Kardinal Görevi",
        "content": "Kronik enflamasyonun orkestra şefi makrofajdır. Tek başına dört devasa biyolojik fonksiyonu yürütür:\n\n1. **Fagositoz ve Mikrobisidal Aktivite:** Opsonize olmuş bakterileri, nekrotik hücre artıklarını ve yabancı partikülleri yutar; fagozomda lizozomal enzimler, ROS ve NO ile parçalar.\n2. **Mediyatör ve Sitokin Fabrikası:** TNF-α, IL-1, IL-6, IL-12, kemokinler ve eikozanoidler salgılayarak enflamasyonu amplifiye eder.\n3. **Antijen Sunumu (APC):** Yuttuğu proteinleri işler ve MHC sınıf II molekülleri üzerinde CD4+ yardımcı T hücrelerine sunarak adaptif immüniteyi ateşler.\n4. **Doku Onarımı ve Fibrogenezis:** İyileşme fazında büyüme faktörleri (PDGF, FGF, VEGF, TGF-β) salgılayarak fibroblastları, damarlanmayı ve kollajen sentezini uyarır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Makrofajların hem mikrop öldürme hem de doku onarımı yapabilme yeteneğini yöneten, T hücrelerinden gelen sinyallere göre şekillenen iki zıt fonksiyonel kutup hangileridir?",
                [
                    {"key": "A", "text": "Klasik (M1) ve Alternatif (M2) aktivasyon yolları", "explanation": "A seçeneği DOĞRUDUR: M1 mikrop öldürücü pro-enflamatuar, M2 doku onarıcı anti-enflamatuar fenotiptir."},
                    {"key": "B", "text": "Th1 ve Th2 lenfosit diferansiyasyonu", "explanation": "B seçeneği yanlıştır: Bunlar T lenfosit alt gruplarıdır, makrofaj kutbu değildir."},
                    {"key": "C", "text": "Kupffer ve Mikroglia hücre tipleri", "explanation": "C seçeneği yanlıştır: Bunlar anatomik lokalizasyon adlarıdır."},
                    {"key": "D", "text": "H1 ve H2 reseptör ekspresyonu", "explanation": "D seçeneği yanlıştır: Histamin reseptörleridir."},
                    {"key": "E", "text": "Siklooksijenaz ve Lipoksijenaz enzimleri", "explanation": "E seçeneği yanlıştır: Eikozanoid enzimleridir."}
                ],
                "A"
            ),
            make_recall(
                "Makrofajların yüzeylerindeki hangi molekül kompleksi peptit antijenleri CD4+ yardımcı T lenfositlerine sunmalarını sağlar?",
                "MHC Sınıf II molekülleridir (Major Histokompatibilite Kompleksi Tip II).",
                "Antijen sunucu hücrelerin majör doku uygunluk molekülü"
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-13-s15",
        "title": "Klasik Makrofaj Aktivasyonu (M1 Yolu): Mikrop Avcısı",
        "content": "Klasik yolak (M1), konağın mikroplara karşı verdiği sert saldırı ve savunma hattıdır:\n\n- **Tetikleyiciler:** Bakteriyel endotoksinler (LPS), TLR ligandları ve özellikle antijene yanıt veren CD4+ Th1 hücrelerinden salınan **İnterferon-gama (IFN-γ)**.\n- **Biyokimyasal Silahlar:** İndüklenebilir nitrik oksit sentaz (iNOS) ile aşırı NO üretimi; NADPH oksidaz ile süperoksit ve hidrojen peroksit (ROS) patlaması; asit hidrolazlar.\n- **Salgılanan Sitokinler:** **IL-1, TNF-α, IL-6, IL-12 ve IL-23**.\n  - IL-12 naif T hücrelerini Th1 yönüne sürükleyerek daha fazla IFN-γ üretilmesini sağlar (pozitif geri besleme).\n- **Patolojik Fatura:** M1 fenotipi mikropları başarıyla yok eder ancak uzadığında dokuda ağır nekroz ve parankim tahribatına (bystander doku hasarı) yol açar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Klasik (M1) Makrofaj Aktivasyon ve Efektör Zinciri",
                [
                    "1. İkili Uyarı: Makrofaj mikroptan LPS/TLR sinyali ve Th1 hücresinden IFN-gama uyarısı alır.",
                    "2. Enzimatik Patlama: Hücrede iNOS ve NADPH oksidaz enzimleri maksimum eksprese edilir.",
                    "3. Toksik Radikal Üretimi: Yüksek miktarda NO, süperoksit ve peroksinitrit sentezlenir.",
                    "4. Fagozomal Öldürme ve Doku Hasarı: Mikrop yok edilirken çevreye saçılan enzimler parankimi tahrip eder."
                ]
            ),
            make_cloze(
                "Klasik M1 makrofaj aktivasyonunu başlatan en güçlü sitokin Th1 lenfositlerinden salınan interferon-gama molekülüdür.",
                "interferon-gama",
                "Th1 kaynaklı majör makrofaj aktive edici sitokin"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-13-s16",
        "title": "Alternatif Makrofaj Aktivasyonu (M2 Yolu): Onarım ve Fibrozis",
        "content": "Alternatif yolak (M2), enflamasyonun dindirilmesi, doku artıklarının temizlenmesi ve hasarlı bölgenin tamir edilmesi için programlanmıştır:\n\n- **Tetikleyiciler:** Th2 lenfositlerinden ve eozinofillerden salgılanan **İnterlökin-4 (IL-4)** ve **İnterlökin-13 (IL-13)** sitokinleridir (IFN-γ ile uyarılmaz, aksine IFN-γ M2'yi baskılar).\n- **Biyokimyasal Özellik:** M2 makrofajlarında iNOS baskılanır; arginin amino asidi **Arginaz-1** enzimiyle ornitin ve **proline** dönüştürülür. Prolin, kollajen sentezinin temel yapıtaşıdır!\n- **Salgılanan Sitokinler ve Faktörler:**\n  - **TGF-β ve IL-10:** Güçlü anti-enflamatuar etki; M1 hücrelerini ve T-lenfositleri susturur.\n  - **VEGF, PDGF ve FGF:** Fibroblast proliferasyonu, anjiyogenez ve yara izi (skar) oluşumu.\n- **Mikrobisidal Aktivite:** Son derece sınırlıdır; parazitlere karşı koruma dışında mikrop öldürme gücü düşüktür.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "M1 (Klasik) vs M2 (Alternatif) Makrofaj Karşılaştırması",
                "M1 Makrofaj (Mikrop Avcısı)",
                "IFN-gama ile uyarılır; iNOS ve ROS ile mikropları ve dokuyu yıkar; IL-1, TNF salgılar.",
                "M2 Makrofaj (Doku Onarıcısı)",
                "IL-4 ve IL-13 ile uyarılır; Arginaz ve TGF-beta ile kollajen sentezi, anjiyogenez ve fibrozis yapar."
            ),
            make_quiz(
                "Alternatif (M2) makrofaj aktivasyonunu uyararak doku tamiri, anjiyogenez ve kollajen sentezini (fibrozis) tetikleyen temel sitokin çifti hangisidir?",
                [
                    {"key": "A", "text": "İnterlökin-4 ve İnterlökin-13", "explanation": "A seçeneği DOĞRUDUR: IL-4 ve IL-13 alternatif yolun baş tetikleyicileridir."},
                    {"key": "B", "text": "İnterferon-gama ve TNF-alfa", "explanation": "B seçeneği yanlıştır: Klasik M1 yolunun tetikleyicileridir."},
                    {"key": "C", "text": "İnterlökin-1 ve İnterlökin-6", "explanation": "C seçeneği yanlıştır: Akut pro-enflamatuar sitokinlerdir."},
                    {"key": "D", "text": "İnterlökin-8 ve LTB4", "explanation": "D seçeneği yanlıştır: Nötrofil kemotaktik ajanlarıdır."},
                    {"key": "E", "text": "Bradikinin ve Histamin", "explanation": "E seçeneği yanlıştır: Vazoaktif mediyatörlerdir."}
                ],
                "A"
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-13-s17",
        "title": "M1 ve M2 Dengesizliği: Doku Yıkımından Organ Fibrozisine",
        "content": "Sağlıklı bir doku iyileşmesinde önce M1 makrofajlar mikrop ve nekrotik dokuyu süpürür; ardından mikroçevre M2 fenotipine evrilerek doku kollajenle tamir edilir. Bu dengenin bozulması patolojinin temelini atar:\n\n- **Aşırı ve Süregelen M1 Yanıtı:** Otoimmün hastalıklarda (romatoid artrit, multipl skleroz, inflamatuar bağırsak hastalıkları) M1 baskın kalır; aralıksız sitokin ve proteaz deşarjıyla parankim erir ve kronik ülserasyonlar gelişir.\n- **Aşırı ve Kontrolsüz M2 Yanıtı:** Doku hasarı sonrası M2 fenotipi susturulamazsa, sürekli TGF-β salınımı sonucu fibroblastlar aşırı kollajen üretir. Sonuç: **Organ Fibrozisi**.\n  - Karaciğer sirozu, sistemik skleroz (skleroderma), idiyopatik pulmoner fibrozis ve kronik böbrek yetmezliği kontrolsüz M2/fibrogenik yanıtın ürünleridir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Sistemik skleroz (skleroderma) hastasında deri biyopsisinde dermal kalınlaşma, yoğun kollajen lif demetleri ve parankim kaybı izleniyor.",
                "Bu hastada kontrolsüz ekstraselüler matriks birikimi ve progresif fibrozise yol açan baskın makrofaj aktivasyon paterni ve anahtar sitokin nedir?",
                [
                    {
                        "text": "Alternatif (M2) makrofaj aktivasyonu ve aşırı TGF-β salınımıdır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! M2 makrofajlarının ürettiği TGF-beta ve PDGF fibroblastları uyararak kontrolsüz organ fibrozisine yol açar."
                    },
                    {
                        "text": "Klasik (M1) aktivasyon ve aşırı nitrik oksit üretimidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: M1 doku hasarı ve nekroz yapar, fibrotik matriks birikiminin baş sorumlusu M2 yoludur."
                    },
                    {
                        "text": "Yalnızca akut nötrofilik histamin degranülasyonudur.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Histamin vazoaktif amindir, fibrogenezisi yönetmez."
                    }
                ]
            ),
            make_cloze(
                "Kontrolsüz alternatif makrofaj aktivasyonu sonucu salgılanan TGF-beta fibroblastları uyararak karaciğer sirozu ve pulmoner fibrozis gibi tablolara yol açar.",
                "TGF-beta",
                "En güçlü profibrotik sitokin"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-13-s18",
        "title": "Makrofaj Kaynaklı Sitokinler ve Büyüme Faktörleri",
        "content": "Makrofajlar çok yönlü bir endokrin ve parakrin salgı fabrikasıdır. Ürettikleri moleküller kronik yangının seyrini tayin eder:\n\n1. **Enflamatuar Sitokinler:**\n   - **TNF-α ve IL-1:** Endotel aktivasyonu, adezyon molekül artışı, ateş, kaşeksi.\n   - **IL-6:** Karaciğerden akut faz proteinleri (CRP, fibrinojen) sentezi.\n   - **IL-12 ve IL-23:** T lenfositlerinin Th1 ve Th17 alt gruplarına farklılaşması.\n2. **Büyüme ve Onarım Faktörleri:**\n   - **TGF-β (Transforming Growth Factor-β):** Fibroblast kemotaksisi ve kollajen sentezi; T ve B hücre proliferasyonunun baskılanması.\n   - **PDGF (Trombosit Kaynaklı Büyüme Faktörü):** Düz kas ve fibroblast proliferasyonu.\n   - **FGF (Fibroblast Büyüme Faktörü):** Anjiyogenez ve granülasyon dokusu oluşumu.\n   - **VEGF (Vasküler Endotelyal Büyüme Faktörü):** Yeni kapiller damar tomurcuklanması.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Makrofaj Faktörü", "Hedef Hücre / Doku", "Başlıca Biyolojik Etki"],
                [
                    [
                        {"text": "İnterlökin-12 (IL-12)", "isMasked": False, "hint": ""},
                        {"text": "Naif CD4+ T hücreleri", "isMasked": False, "hint": ""},
                        {"text": "Th1 farklılaşması ve IFN-gama salgısı uyarımı", "isMasked": True, "hint": "Hücresel immüniteye yönlendirme"}
                    ],
                    [
                        {"text": "VEGF ve FGF", "isMasked": True, "hint": "Damar oluşturan büyüme faktörleri"},
                        {"text": "Vasküler endotel hücreleri", "isMasked": False, "hint": ""},
                        {"text": "Anjiyogenez ve yeni damar oluşumu", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "TGF-β", "isMasked": False, "hint": ""},
                        {"text": "Fibroblastlar ve lökositler", "isMasked": True, "hint": "Kollajen üreten mezenkimal hücreler"},
                        {"text": "Kollajen sentezi ve güçlü immünosupresyon", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Kronik doku hasarında yeni kapiller damarların oluşmasını (anjiyogenez) sağlayan makrofaj kökenli en önemli büyüme faktörü hangisidir?",
                "Vasküler Endotelyal Büyüme Faktörüdür (VEGF / FGF ile birlikte).",
                "Damar endotelini çoğaltan temel faktör"
            )
        ]
    })

    # Slide 19
    slides.append({
        "id": "k1-13-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Mononükleer Fagosit Sistemi ve Makrofaj Aktivasyon Yolakları",
        "content": "Bu kontrol noktasında kronik enflamasyonun merkezindeki makrofaj biyolojisini, aktivasyon yolaklarını ve moleküler ürünlerini özetliyoruz:\n\n- **Mononükleer Fagosit Sistemi:** Kanda monosit, dokuda makrofaj. Yerleşikler: Kupffer (karaciğer), mikroglia (beyin), alveoler makrofaj (akciğer), sinüs histiyositi (dalak/lenf nodu).\n- **Klasik Aktivasyon (M1):** IFN-γ ve LPS uyarısıyla tetiklenir; iNOS, ROS ve lizozomal enzimlerle mikropları öldürür, doku nekrozu yapar; IL-1, TNF, IL-12 salgılar.\n- **Alternatif Aktivasyon (M2):** IL-4 ve IL-13 uyarısıyla tetiklenir; arginaz-1 ile prolin/kollajen sentezi, TGF-β, VEGF ve PDGF ile doku onarımı, anjiyogenez ve fibrozis yapar.\n- **Patoloji Köprüsü:** Süregelen M1 otoimmün doku erimesine; süregelen M2 ise organ fibrozisine (siroz, pulmoner fibrozis) yol açar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Karaciğer sinüzoidlerinde yerleşerek portal dolaşımla gelen antijenleri ve mikroorganizmaları süzen mononükleer fagosit sistemi üyesi hücre hangisidir?",
                [
                    {"key": "A", "text": "Kupffer hücresi", "explanation": "A seçeneği DOĞRUDUR: Karaciğerin yerleşik rezidan makrofajıdır."},
                    {"key": "B", "text": "Mikroglia", "explanation": "B seçeneği yanlıştır: Beyin rezidan makrofajıdır."},
                    {"key": "C", "text": "Osteoklast", "explanation": "C seçeneği yanlıştır: Kemik rezorpsiyon hücresidir."},
                    {"key": "D", "text": "İto (Yıldızsı) hücresi", "explanation": "D seçeneği yanlıştır: Karaciğerde A vitamini depolayan ve sirozda kollajen üreten perisinüzoidal mezenkimal hücredir."},
                    {"key": "E", "text": "Langerhans hücresi", "explanation": "E seçeneği yanlıştır: Deri epidermisinde yer alan dentritik hücredir."}
                ],
                "A"
            ),
            make_cloze(
                "Klasik M1 makrofaj aktivasyonunda indüklenebilir nitrik oksit sentaz enzimi rol oynarken, alternatif M2 aktivasyonunda arginaz-1 enzimi kollajen sentezini destekler.",
                "arginaz-1",
                "M2 yolunda arginini proline çeviren enzim"
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-13-s20",
        "title": "Makrofajların Antijen Sunucu Rolü ve T Hücre Aktivasyonu",
        "content": "Makrofajlar yalnızca çöpçü hücreler değil, aynı zamanda edinsel bağışıklığı aktive eden **profesyonel Antijen Sunucu Hücrelerdir (APC)**:\n\n- **Antijen İşleme:** Fagositozla yutulan ekstraselüler proteinler endozom/lizozom içinde 10-15 amino asitlik oligopeptitlere parçalanır.\n- **MHC Sınıf II Ekspresyonu:** İşlenen peptitler endoplazmik retikulumdan gelen MHC sınıf II moleküllerine yüklenerek hücre yüzeyine taşınır.\n- **T Hücre Tanıması ve İkili Sinyal:**\n  1. **Sinyal 1:** Naif CD4+ T hücresinin TCR reseptörü antijen-MHC II kompleksine bağlanır.\n  2. **Sinyal 2 (Ko-stimülasyon):** Makrofaj yüzeyindeki **B7 (CD80/CD86)** molekülleri, T hücresindeki **CD28** reseptörüne kenetlenir.\n- **Sonuç:** T hücresi aktive olur, klonal olarak çoğalır ve makrofaja yanıt olarak IFN-γ salgılar. Bu çift taraflı kenetlenme kronik yangının motorudur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Antijen Tanıma (Sinyal 1) vs Ko-Stimülasyon (Sinyal 2)",
                "Sinyal 1 (Antijen Özgüllüğü)",
                "TCR reseptörü makrofajdaki MHC Sınıf II + Peptit kompleksine bağlanarak antijeni tanır.",
                "Sinyal 2 (Ko-Stimülasyon)",
                "Makrofajdaki B7-1/B7-2 molekülleri T hücresindeki CD28'e bağlanarak tam aktivasyon sağlar."
            ),
            make_recall(
                "Profesyonel antijen sunucu makrofajların yüzeyinde bulunan ve T lenfositlerindeki CD28 reseptörüne bağlanarak ko-stimülasyon sağlayan molekül ailesi nedir?",
                "B7 ailesidir (B7-1 / CD80 ve B7-2 / CD86).",
                "İkinci aktivasyon sinyalini veren zar ligandı"
            )
        ]
    })

    return slides
