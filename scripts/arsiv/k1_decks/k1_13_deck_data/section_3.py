# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-13-s21",
        "title": "Kronik Enflamasyonda Lenfositlerin Rolü ve Adaptif Bağışıklık",
        "content": "Kronik enflamasyonda makrofajlar orkestranın enstrümanı ise, adaptif bağışıklığın yöneticisi olan **lenfositler** bu orkestranın şefidir:\n\n- **Antijen Özgüllüğü:** Doğuştan gelen bağışıklık hücreleri (nötrofil, makrofaj) mikropları genel kalıplarla (PAMP) tanırken, T ve B lenfositleri klonal reseptörleriyle (TCR ve BCR) spesifik antijenik epitopları hedefler.\n- **Kalıcılığın Temeli:** İmmünolojik hafıza lenfositlerce sağlanır. Antijen ortamda kaldığı sürece lenfositler sürekli prolifere olur ve sitokin salgılayarak makrofajları yangı alanında hapseder.\n- **Doku Morfolojisi:** Işık mikroskobunda lenfositler dar mavi/mor sitoplazmalı, koyu hiperkromatik yuvarlak çekirdekli küçük hücreler olarak damar çevrelerinde kuff (perivasküler cuffing) oluştururlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Doğal (Makrofaj) vs Adaptif (Lenfosit) İmmünite Özellikleri",
                "Doğal İmmünite (Makrofaj)",
                "Patojen tanıma reseptörleri (TLR) ile genel mikrop yapılarını tanır; bellek geliştirmez.",
                "Adaptif İmmünite (Lenfosit)",
                "TCR ve antikorlarla özgül epitopları tanır; güçlü immünolojik hafıza ve antijen özgüllüğü sağlar."
            ),
            make_cloze(
                "Kronik enflamasyonda hücresel antijen özgüllüğünü ve immünolojik hafızayı sağlayan hücre grubu lenfositlerdir.",
                "lenfositlerdir",
                "Adaptif bağışıklığın çekirdek hücreleri"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-13-s22",
        "title": "CD4+ T Yardımcı Hücre Alt Grupları: Th1, Th2 ve Th17",
        "content": "Naif CD4+ T hücreleri (Th0), antijen sunan hücreden gelen sitokin sinyaline bağlı olarak üç ana fonksiyonel efektör alt gruba farklılaşır:\n\n1. **Th1 Hücreleri:** IL-12 uyarısıyla farklılaşır; **IFN-γ** üretir. İntraselüler bakterilere, virüslere ve otoimmüniteye karşı hücresel savunmayı yönetir; klasik makrofaj (M1) aktivatörüdür.\n2. **Th2 Hücreleri:** IL-4 uyarısıyla farklılaşır; **IL-4, IL-5 ve IL-13** üretir. Helmintik parazitlere, alerjik reaksiyonlara ve alternatif makrofaj (M2) doku onarımına öncülük eder.\n3. **Th17 Hücreleri:** IL-6, TGF-β ve IL-23 uyarısıyla farklılaşır; **IL-17 ve IL-22** üretir. Nötrofilleri yangı odağına çekerek ekstraselüler bakteri ve mantarlara karşı koyar; şiddetli doku yıkımı ve otoimmünite yaratır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["CD4+ T Alt Grubu", "İndükleyici Sitokin", "Başlıca Efektör Sitokin", "Temel İmmünolojik Rolü"],
                [
                    [
                        {"text": "Th1", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-12 (IL-12)", "isMasked": False, "hint": ""},
                        {"text": "İnterferon-gama (IFN-γ)", "isMasked": True, "hint": "Klasik makrofaj aktivatörü sitokin"},
                        {"text": "İntraselüler mikroplar ve M1 makrofaj aktivasyonu", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Th2", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-4 (IL-4)", "isMasked": False, "hint": ""},
                        {"text": "IL-4, IL-5, IL-13", "isMasked": True, "hint": "Alerji ve eozinofil sitokinleri"},
                        {"text": "Helmintler, alerji ve M2 doku onarımı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Th17", "isMasked": True, "hint": "Nötrofil çeken T lenfosit alt grubu"},
                        {"text": "IL-1, IL-6, IL-23", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-17 (IL-17)", "isMasked": False, "hint": ""},
                        {"text": "Nötrofilik infiltrasyon ve otoimmün inflamasyon", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Helmint enfeksiyonlarında ve alerjik reaksiyonlarda eozinofilleri aktive edip alternatif makrofaj (M2) yanıtını tetikleyen T lenfosit alt grubu hangisidir?",
                "Th2 yardımcı T hücreleridir.",
                "Alerjik ve paraziter T hücre soyu"
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-13-s23",
        "title": "Th1 Lenfositleri ve IFN-γ: Hücresel Bağışıklığın Şefi",
        "content": "Th1 lenfositleri, kronik enflamasyon ve granülomatöz reaksiyonların omurgasını oluşturur:\n\n- **Farklılaşma ve Transkripsiyon:** Dendritik hücre veya makrofajdan gelen IL-12 sinyali, naif T hücresinde **T-bet** anahtar transkripsiyon faktörünü aktive ederek Th1 fenotipini belirler.\n- **İnterferon-gama (IFN-γ) Etkileri:**\n  1. Makrofajları klasik yoldan (M1) uyararak iNOS ve mikrobisidal enzim patlaması yaptırır.\n  2. Makrofajların boyutlarını büyüterek bol pembe sitoplazmalı **epiteloid histiositlere** dönüştürür.\n  3. Makrofajların füzyonunu uyararak **çok çekirdekli Langhans dev hücrelerini** oluşturur.\n  4. B lenfositlerinde opsonizan antikor (IgG) izotip değişimini sağlar.\n- **Hastalıklar:** Tüberküloz, sarkoidoz, Crohn hastalığı ve otoimmün demiyelinizasyon (MS) Th1 baskın patolojilerdir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Th1 / IFN-γ Aracılı Hücresel Savunma Zinciri",
                [
                    "1. Antijenik Tehdit: Makrofaj intraselüler patojeni yakalar ve ortama bolca IL-12 salgılar.",
                    "2. Th1 Farklılaşması: Naif T hücresi T-bet genini açarak Th1 efektör hücresine dönüşür.",
                    "3. Masif IFN-gama Salınımı: Th1 hücresi hedef dokuda yüksek konsantrasyonda IFN-gama üretir.",
                    "4. Epiteloid Dönüşüm ve Granülom: Makrofajlar epiteloid hücrelere ve Langhans dev hücrelerine evrilir."
                ]
            ),
            make_quiz(
                "Granülomatöz enflamasyon gelişiminde makrofajların epiteloid histiositlere ve Langhans tipi dev hücrelere dönüşmesini sağlayan en kritik Th1 sitokini hangisidir?",
                [
                    {"key": "A", "text": "İnterferon-gama (IFN-γ)", "explanation": "A seçeneği DOĞRUDUR: IFN-gama makrofajın epiteloid hücreye ve dev hücreye füzyonundaki majör hormondur."},
                    {"key": "B", "text": "İnterlökin-4", "explanation": "B seçeneği yanlıştır: Th2 sitokinidir, granülom epiteloidleşmesini değil M2 onarımı uyarır."},
                    {"key": "C", "text": "İnterlökin-10", "explanation": "C seçeneği yanlıştır: Anti-enflamatuar sitokindir."},
                    {"key": "D", "text": "Eotaksin", "explanation": "D seçeneği yanlıştır: Eozinofil kemokinidir."},
                    {"key": "E", "text": "Serotonin", "explanation": "E seçeneği yanlıştır: Vazoaktif amindir."}
                ],
                "A"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-13-s24",
        "title": "Th2 Hücreleri ve Alerjik/Eozinofilik Kronik Enflamasyon",
        "content": "Helmintik parazitler ve alerjenler Th1 yerine **Th2 yolunu** aktive eder. Bu yolda rol alan sitokinler tamamen farklı bir patolojik tablo çizer:\n\n- **Farklılaşma Faktörü:** Transkripsiyon faktörü **GATA-3** Th2 fenotipini kontrol eder.\n- **Üçlü Sitokin Cephanesi:**\n  1. **İnterlökin-4 (IL-4):** B lenfositlerinde **IgE antikoruna** sınıf değişimini tetikler. Mast hücrelerini hazırlar.\n  2. **İnterlökin-5 (IL-5):** Eozinofillerin kemik iliğinden çıkışını, dolaşımda sağkalımını ve dokuda aktivasyonunu yöneten primer sitokindir.\n  3. **İnterlökin-13 (IL-13):** Hava yolu ve bağırsak epitelinde aşırı mukus salgısını uyarır; alternatif makrofaj (M2) yolağını aktive ederek fibrozis yapar.\n- **Klinik Tablo:** Kronik astım, atopik dermatit ve alerjik rinitte dokuda bol eozinofil ve mast hücresi birikir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Th1 Yanıtı vs Th2 Yanıtı Patolojik Karşılaştırması",
                "Th1 Yanıtı (Hücresel Savunma)",
                "IFN-gama üretilir; makrofaj aktivasyonu, epiteloid hücreler, granülomlar ve kazeifikasyon nekrozu görülür.",
                "Th2 Yanıtı (Alerjik/Helmint Savunması)",
                "IL-4, IL-5, IL-13 üretilir; eozinofiller, IgE, mast hücreleri ve aşırı mukus salgısı görülür."
            ),
            make_cloze(
                "Alerjik kronik enflamasyonda eozinofillerin kemik iliğinde üretimini ve dokuda sağkalımını yöneten baş sitokin interlökin-5 molekülüdür.",
                "interlökin-5",
                "Eozinofilin spesifik sağkalım sitokini"
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-13-s25",
        "title": "Th17 Lenfositleri ve Doku Tahribatındaki Rolü",
        "content": "Th17 hücreleri, adaptif lenfosit sistemi ile doğal nötrofilik savunmayı birbirine bağlayan özel bir T hücresi soyudur:\n\n- **Farklılaşma:** Naif T hücresinde **RORγt** transkripsiyon faktörünün indüklenmesiyle oluşurlar.\n- **İnterlökin-17 (IL-17) Etkileri:** Epitel hücreleri, fibroblastlar ve endotel hücrelerinden güçlü kemokinlerin (**CXCL8 / IL-8**, CXCL1) salgılanmasını uyarır.\n- **Nötrofil Çağrısı:** Salınan kemokinler kronik enflamasyon alanına **yoğun nötrofil akını** başlatır. Bu nedenle Th17 yanıtı 'akut yangı benzeri nötrofilik hasar' içeren kronik tablolara yol açar.\n- **Klinik Hastalıklar:** Psöriyazis (sedef hastalığı), ankilozan spondilit, romatoid artrit ve multipl skleroz gibi tahripkar otoimmün eklem ve sinir sistemi hastalıklarında başroldedir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Deri biyopsisinde epidermiste hiperkeratoz, parakeratoz ve stratum korneum altında nötrofil mikroapseleri (Munro mikroapseleri) izlenen psöriyazis hastası inceleniyor.",
                "Bu otoimmün kronik tabloda nötrofillerin deriye hücum etmesini sağlayan ve hedefe yönelik monoklonal antikorlarla (sekukinumab) bloke edilen majör sitokin hangisidir?",
                [
                    {
                        "text": "Th17 hücrelerinden salınan İnterlökin-17'dir (IL-17).",
                        "isCorrect": True,
                        "feedback": "Tebrikler! IL-17 keratinositlerden kemokin salgılatarak nötrofilleri deriye çeker; Munro mikroapselerinin ana nedenidir."
                    },
                    {
                        "text": "Th2 hücrelerinden salınan İnterlökin-5'tir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: IL-5 eozinofilleri uyarır, psöriyazisteki nötrofilik mikroapselerden sorumlu değildir."
                    },
                    {
                        "text": "Karaciğerden salınan anjiyotensinojendir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Kan basıncı düzenleyici peptittir, enflamatuar kemokin indüklemez."
                    }
                ]
            ),
            make_recall(
                "Th17 lenfositlerinin farklılaşmasını ve fonksiyonunu kontrol eden anahtar nükleer transkripsiyon faktörü hangisidir?",
                "RORγt'dir (Retinoik asit reseptörü ile ilişkili yetim reseptör gama t).",
                "Th17'nin master gen düzenleyicisi"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-13-s26",
        "title": "Makrofaj-Lenfosit Karşılıklı Etkileşim Döngüsü",
        "content": "Kronik enflamasyonun aylar ve yıllarca sönmeden kendi kendini beslemesinin altında yatan en kritik hücresel mekanizma **makrofaj ile T lenfosit arasındaki iki yönlü pozitif geri bildirim döngüsüdür**:\n\n1. **Makrofaj Başlatır:** Makrofaj fagositozla aldığı antijeni işler ve MHC sınıf II üzerinde CD4+ T hücresine sunar; aynı zamanda **IL-12** salgılar.\n2. **T Hücresi Yanıt Verir:** IL-12 ile aktive olan Th1 hücresi bol miktarda **İnterferon-gama (IFN-γ)** üretir.\n3. **Döngü Şiddetlenir:** IFN-γ makrofaja geri dönerek onu daha fazla aktive eder; makrofaj daha çok antijen sunar, daha çok TNF ve IL-12 salgılar.\n4. **Klinik Sonuç:** Bu karşılıklı kamçılama döngüsü kırılamazsa enflamasyon kronikleşir ve çevredeki doku progresif olarak harap olur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Makrofaj-Lenfosit Pozitif Geri Besleme Döngüsü",
                [
                    "1. Antijen ve IL-12: Makrofaj antijeni T hücresine sunar ve mikroçevreye IL-12 pompalar.",
                    "2. Th1 Aktivasyonu: CD4+ T hücresi aktive olarak klonal çoğalır ve IFN-gama üretir.",
                    "3. IFN-gama Bombardımanı: IFN-gama makrofaj reseptörlerine bağlanarak makrofajı süper-aktive eder.",
                    "4. Sürekli Sitokin Üretimi: Makrofaj daha fazla TNF, IL-1 ve proteaz üreterek kronik yangıyı sürdürür."
                ]
            ),
            make_cloze(
                "Makrofajın salgıladığı IL-12 ile T hücresinin salgıladığı IFN-gama arasındaki karşılıklı kamçılama pozitif geri bildirim döngüsü olarak adlandırılır.",
                "pozitif geri bildirim",
                "Birbirini besleyen ve amplifiye eden döngü"
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-13-s27",
        "title": "B Lenfositleri ve Plazma Hücreleri: Lokal Antikor Fabrikaları",
        "content": "Kronik enflamatuar infiltratın diğer vazgeçilmez üyeleri B lenfositleri ve onların nihai farklılaşmış formu olan **plazma hücreleridir**:\n\n- **Morfolojik Tanı (Sınav Spotu):** Plazma hücreleri ışık mikroskobunda son derece karakteristiktir:\n  - Geniş bazofilik sitoplazma (zengin granüllü endoplazmik retikulum).\n  - Belirgin soluk perinükleer zon (gelişmiş Golgi kompleksi).\n  - Eksantrik yerleşimli yuvarlak çekirdek ve heterokromatinin tekerlek parmağı / saat kadranı şeklinde dizilimi (**cartwheel / clock-face çekirdek**).\n- **Fonksiyon:** İnflamasyon odağında lokal olarak antijenlere karşı spesifik immünglobulinler (antikorlar) üretirler; opsonizasyonu ve kompleman aktivasyonunu tetiklerler.\n- **Klinik Örnek:** Sifiliz gomlarında ve kronik endometritte plazma hücresi varlığı patognomoniktir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Mikroskop altında eksantrik yerleşimli 'saat kadranı' çekirdek kromatini, perinükleer soluk Golgi zonu ve bazofilik sitoplazmasıyla tanınan kronik enflamatuar hücre hangisidir?",
                [
                    {"key": "A", "text": "Plazma hücresi", "explanation": "A seçeneği DOĞRUDUR: Saat kadranı çekirdeği ve zengin GER içeriği plazma hücresinin tipik morfolojik imzasıdır."},
                    {"key": "B", "text": "Nötrofil", "explanation": "B seçeneği yanlıştır: Çok loblu çekirdekli polimorfonükleer hücredir."},
                    {"key": "C", "text": "Eozinofil", "explanation": "C seçeneği yanlıştır: İki loblu çekirdek ve parlak kırmızı granüllüdür."},
                    {"key": "D", "text": "Kupffer hücresi", "explanation": "D seçeneği yanlıştır: Sinüzoidal makrofajdır."},
                    {"key": "E", "text": "Mast hücresi", "explanation": "E seçeneği yanlıştır: Metakromatik granüllü doku hücresidir."}
                ],
                "A"
            ),
            make_cloze(
                "Kronik enflamasyonda antikor üreten plazma hücreleri eksantrik yerleşimli saat kadranı çekirdek kromatini ile mikroskopta kolayca ayırt edilir.",
                "saat kadranı",
                "Heterokromatinin tekerlek parmağı benzeri dizilim adı"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-13-s28",
        "title": "Tersiyer Lenfoid Yapılar: Ektopik Lenfoid Neogenez",
        "content": "Bazı şiddetli ve uzun süreli kronik enflamatuar hastalıklarda, iltihap alanındaki lenfositler ve dentritik hücreler sıradan bir infiltrat olmaktan çıkarak organize bir **lenf düğümü mimarisi** oluştururlar:\n\n- **Tanım:** Lenfoid organ olmayan dokularda (sinovya, tiroid, akciğer) B-hücre folikülleri, T-hücre zonları ve hatta fonksiyonel **germinal merkezler** içeren lenfoid agregatların gelişmesine **Tersiyer Lenfoid Yapılar (TLS)** veya ektopik lenfoid neogenez denir.\n- **Gelişim Mekanizması:** Dokuda lenfotoksin-α/β (LT-α/β) ve CXCL13 gibi homeostatik kemokinlerin kronik üretimi ile tetiklenir.\n- **Klinik Örnekler:**\n  - **Hashimoto Tiroiditi:** Tiroid parankiminde germinal merkezli bol lenfoid folikül oluşumu.\n  - **Romatoid Artrit:** İltihaplı sinoviyumda organize lenf folikülleri.\n  - **Helicobacter pylori Gastriti:** MALT lenfoma öncülü olabilen gastrik lenfoid foliküller.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Dağınık İnfiltrat vs Tersiyer Lenfoid Yapı (TLS)",
                "Dağınık Kronik İnfiltrat",
                "Doku aralıklarında gelişi güzel saçılmış makrofaj, lenfosit ve plazma hücreleridir.",
                "Tersiyer Lenfoid Yapı (TLS)",
                "Organize B/T zonları ve germinal merkezler içeren, adeta dokuda yeni bir lenf düğümü oluşturan yapıdır."
            ),
            make_recall(
                "Kronik lenfositik tiroiditte (Hashimoto tiroiditi) tiroid bezinde mikroskobik olarak görülen ve germinal merkez içeren ektopik lenfoid yapılara ne ad verilir?",
                "Tersiyer Lenfoid Yapılardır (TLS / Lenfoid Foliküller).",
                "Organize olmuş ektopik lenf dokusu"
            )
        ]
    })

    # Slide 29
    slides.append({
        "id": "k1-13-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Lenfosit Alt Grupları ve Lenfosit-Makrofaj Etkileşimi",
        "content": "Bu kontrol noktasında adaptif bağışıklığın kronik enflamasyondaki yönlendirici rolünü ve hücreler arası moleküler köprüleri özetliyoruz:\n\n- **Th1:** IL-12 uyarısıyla oluşur; IFN-γ üretir; klasik M1 makrofajlarını uyarır, epiteloid hücre ve Langhans dev hücrelerini oluşturur.\n- **Th2:** IL-4 uyarısıyla oluşur; IL-4, IL-5, IL-13 üretir; eozinofilleri ve alternatif M2 doku onarımını/fibrozisi tetikler.\n- **Th17:** RORγt geniyle yönetilir; IL-17 üretir; epitelden kemokin salgılatarak nötrofilleri kronik yangı alanına çağırır.\n- **Pozitif Döngü:** Makrofajın IL-12'si ile Th1'in IFN-γ'sı birbirini karşılıklı uyararak yangıyı kronikleştirir.\n- **Plazma Hücresi:** Saat kadranı kromatinli, eksantrik çekirdekli lokal antikor fabrikası.\n- **Tersiyer Lenfoid Yapılar:** Hashimoto ve romatoid artritte gelişen germinal merkezli ektopik foliküller.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Otoimmün kronik enflamasyonda epitel ve endotel hücrelerinden CXCL8 (IL-8) salgılatarak ortama yoğun nötrofil toplanmasını sağlayan ve sedef hastalığında rol alan temel T hücresi alt grubu hangisidir?",
                [
                    {"key": "A", "text": "Th17 yardımcı T hücreleri", "explanation": "A seçeneği DOĞRUDUR: Th17 hücreleri ürettikleri IL-17 ile nötrofil kemotaksisini tetikler."},
                    {"key": "B", "text": "Th2 yardımcı T hücreleri", "explanation": "B seçeneği yanlıştır: Eozinofil ve IgE ilişkili alerjik hücrelerdir."},
                    {"key": "C", "text": "Treg (Regülatuvar T) hücreleri", "explanation": "C seçeneği yanlıştır: İmmün baskılayıcı hücrelerdir."},
                    {"key": "D", "text": "Doğal Öldürücü (NK) hücreler", "explanation": "D seçeneği yanlıştır: Doğal bağışıklık lenfositleridir."},
                    {"key": "E", "text": "Foliküler Dendritik hücreler", "explanation": "E seçeneği yanlıştır: B hücrelerine antijen sunan stroma hücreleridir."}
                ],
                "A"
            ),
            make_cloze(
                "Plazma hücreleri geniş bazofilik sitoplazmaları ve saat kadranı şeklinde dizilmiş heterokromatinli çekirdekleri ile mikroskopta tanınır.",
                "heterokromatinli",
                "Koyu boyanan yoğun nükleer kromatin türü"
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-13-s30",
        "title": "CD8+ Sitotoksik T Lenfositleri ve Kronik Doku Hasarı",
        "content": "Kronik enflamasyonda yalnızca CD4+ yardımcı T hücreleri değil, doğrudan hedef hücreyi öldüren **CD8+ Sitotoksik T Lenfositleri (CTL)** de kritik roller üstlenir:\n\n- **Antijen Tanıma:** CD8+ T hücreleri endojen (hücre içinde sentezlenen) antijenleri tüm çekirdekli hücrelerin yüzeyindeki **MHC Sınıf I** molekülleri aracılığıyla tanır.\n- **Sitotoksik Mekanizma:**\n  1. **Perforin ve Granzim:** Perforin hedef hücre zarında delik açar; serin proteaz olan granzim içeri girerek kaspaz kaskadını tetikler ve hedef hücreyi **apoptoza** götürür.\n  2. **FasL - Fas Yolu:** CTL yüzeyindeki Fas ligandı hedef hücredeki Fas (CD95) ölüm reseptörüne bağlanarak apoptoz sinyali verir.\n- **Klinik Örnekler:** Kronik viral hepatit B ve C'de virüs hepatositi doğrudan öldürmez; hepatosit hasarını ve karaciğer yetmezliğini virüsle enfekte hücreleri tek tek öldüren konak CD8+ T lenfositleri yaratır!",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "CD4+ Yardımcı T vs CD8+ Sitotoksik T Lenfositleri",
                "CD4+ T Lenfositleri (Yönetici)",
                "MHC Sınıf II ile uyarılır; sitokin salgılayarak diğer hücreleri organize eder ve aktive eder.",
                "CD8+ T Lenfositleri (İnfazcı)",
                "MHC Sınıf I ile uyarılır; perforin ve granzim ile virüslü veya yabancı hücreyi doğrudan apoptoza sokar."
            ),
            make_recall(
                "Kronik viral hepatitte karaciğer hücrelerinin tahrip edilerek siroza sürüklenmesinde hepatosit ölümünü doğrudan tetikleyen majör immün hücre grubu hangisidir?",
                "CD8+ Sitotoksik T Lenfositleridir (CTL).",
                "MHC Sınıf I ile çalışan öldürücü T lenfositleri"
            )
        ]
    })

    return slides
