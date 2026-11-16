# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-13-s31",
        "title": "Eozinofillerin Biyolojisi: Parazitler ve Alerji",
        "content": "Eozinofiller, kemik iliğinde üretilen ve dokularda özellikle **helmintik parazit enfeksiyonları** ve **IgE aracılı alerjik reaksiyonlarda** toplanan özelleşmiş granülositlerdir:\n\n- **Morfolojik Tanı:** İki loblu (gözlük şeklinde / bilobüle) çekirdek ve eozin boyasıyla parlak kırmızı/turuncu boyanan yoğun iri sitoplazmik granüllere sahiptirler.\n- **Kinetik ve Dağılım:** Kanda dolaşım ömürleri kısadır (yaklaşık 8-12 saat); esas görev yerleri mukozalardır (solunum yolu, gastrointestinal sistem epiteli altı).\n- **İmmünolojik Köprü:** Yüzeylerinde IgE için düşük ve yüksek afiniteli Fc reseptörleri taşırlar. Parazit yüzeyine yapışmış IgE antikorlarına bağlanarak granüllerini parazitin kutikulası üzerine boşaltırlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Nötrofil vs Eozinofil Granülosit Karşılaştırması",
                "Nötrofil (Bakteriyel Savunma)",
                "3-5 loblu çekirdek; soluk nötral granüller; bakterileri fagositozla öldürür.",
                "Eozinofil (Paraziter ve Alerjik Savunma)",
                "2 loblu çekirdek; parlak eozinofilik granüller; parazitleri ekstraselüler granül deşarjıyla deler."
            ),
            make_cloze(
                "Eozinofiller mikroskop altında iki loblu çekirdekleri ve eozin boyasıyla parlak kırmızı boyanan sitoplazmik granülleri ile ayırt edilir.",
                "iki loblu",
                "Eozinofil çekirdeğinin lob sayısı"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-13-s32",
        "title": "Eozinofil Kemotaksisi: Eotaksin ve İnterlökin-5 Sinyali",
        "content": "Eozinofillerin yangı odağına toplanması ve hayatta kalması iki temel molekülün koordinasyonu ile gerçekleşir:\n\n1. **Eotaksin Ailesi (CCL11 / Eotaksin-1, CCL24, CCL26):** Epitel hücreleri ve fibroblastlar tarafından salgılanan en spesifik eozinofil kemokinidir. Eozinofillerin yüzeyinde bolca bulunan **CCR3** kemokin reseptörüne bağlanarak hücreleri doğrudan dokuya çeker.\n2. **İnterlökin-5 (IL-5):** Th2 lenfositleri ve mast hücrelerinden salınır; kemik iliğinden eozinofil üretimini kamçılar ve dokudaki eozinofillerin apoptozunu engelleyerek haftalarca canlı kalmalarını sağlar.\n3. **Hedefli İlaçlar:** Dirençli eozinofilik astımda IL-5'i nötralize eden monoklonal antikorlar (**mepolizumab, reslizumab**) ve IL-5R blokerleri (**benralizumab**) kullanılır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Eozinofil Çıkış ve Aktivasyon Kaskadı",
                [
                    "1. Th2 Uyarımı: Alerjen veya helmint uyarısıyla Th2 hücreleri bolca IL-5 salgılar.",
                    "2. İlikten Salınım: IL-5 kemik iliğini uyararak kana yoğun olgun eozinofil deşarjı yaptırır.",
                    "3. Eotaksin Kemotaksisi: Solunum yolu epitelinden salınan CCL11 (eotaksin) CCR3'e bağlanarak eozinofili dokuya çeker.",
                    "4. Doku Sağkalımı: IL-5 dokudaki eozinofilin apoptozunu durdurarak kronik inflamatuar hasarı sürdürür."
                ]
            ),
            make_quiz(
                "Alerjik enflamasyonda eozinofillerin CCR3 reseptörüne bağlanarak onları spesifik olarak yangı odağına çeken temel kemokin hangisidir?",
                [
                    {"key": "A", "text": "Eotaksin (CCL11)", "explanation": "A seçeneği DOĞRUDUR: Eotaksin CCR3 reseptörüyle eozinofilleri çeken majör kemokindir."},
                    {"key": "B", "text": "İnterlökin-8 (CXCL8)", "explanation": "B seçeneği yanlıştır: Nötrofil kemokinidir."},
                    {"key": "C", "text": "MCP-1 (CCL2)", "explanation": "C seçeneği yanlıştır: Monosit kemokinidir."},
                    {"key": "D", "text": "Lenfotoksin-alfa", "explanation": "D seçeneği yanlıştır: Lenfoid doku düzenleyicisidir."},
                    {"key": "E", "text": "Bradikinin", "explanation": "E seçeneği yanlıştır: Kinin sistem peptididir."}
                ],
                "A"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-13-s33",
        "title": "Eozinofil Granül İçeriği ve Doku Toksisitesi",
        "content": "Eozinofillerin sitoplazmik granülleri parazitleri öldürmek için evrimleşmiş son derece toksik proteinlerle doludur; ancak bu proteinler kronik yangıda konak dokusuna ağır zarar verir:\n\n1. **Majör Temel Protein (MBP - Major Basic Protein):** Granül kristaloid çekirdeğinde yer alır; güçlü parazitisidaldir. Ancak kronik astımda bronş epitelini parçalar, epitel dökülmesine ve hiperreaktiviteye yol açar.\n2. **Eozinofil Katyonik Protein (ECP):** Parazit ve konak hücre zarında porlar açan nörotoksik bir ribonükleazdır.\n3. **Eozinofil Peroksidaz (EPO):** Hidrojen peroksiti halojenürlerle birleştirerek sitotoksik hipohalojen asitler üretir.\n4. **Charcot-Leyden Kristalleri:** Eozinofiller parçalandığında açığa çıkan eozinofil lizofosfolipaz proteinlerinin (galektin-10) oluşturduğu elmas şeklindeki mikroskobik kristallerdir (astım balgamında görülür).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Eozinofil Granül Proteini", "Biyokimyasal Özelliği", "Klinik / Doku Etkisi"],
                [
                    [
                        {"text": "Majör Temel Protein (MBP)", "isMasked": False, "hint": ""},
                        {"text": "Kristaloid çekirdekteki yüksek bazik protein", "isMasked": False, "hint": ""},
                        {"text": "Parazit öldürme ve bronş epitel dökülmesi", "isMasked": True, "hint": "Astımda hava yolu epitelini soyan protein"}
                    ],
                    [
                        {"text": "Eozinofil Katyonik Protein (ECP)", "isMasked": True, "hint": "Zarda por açan katyonik ribonükleaz"},
                        {"text": "Hücre zarını delen por oluşturan ribonükleaz", "isMasked": False, "hint": ""},
                        {"text": "Helmint membran lizisi ve nörotoksisite", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Charcot-Leyden Kristalleri", "isMasked": False, "hint": ""},
                        {"text": "Lizofosfolipaz (Galektin-10) agregatı", "isMasked": True, "hint": "Parçalanan eozinofillerden çöken elmas kristal"},
                        {"text": "Alerjik astım ve parazit balgamında tanısal belirteç", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Astımlı hastaların balgamında veya parazitozlu dokularda eozinofil lizofosfolipaz enziminin çökmesiyle oluşan çift piramidal elmas kristallere ne ad verilir?",
                "Charcot-Leyden kristalleridir.",
                "Eozinofil kökenli tanısal elmas kristaller"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-13-s34",
        "title": "Mast Hücrelerinin Kronik Enflamasyondaki Rolü",
        "content": "Mast hücreleri yalnızca akut alerjik anaflaksinin değil, aynı zamanda kronik enflamasyon ve fibrozisin de önemli düzenleyicilerindendir:\n\n- **Dokuda Konumlanma:** Kan damarlarının, sinirlerin ve mukozal bariyerlerin çevresinde yerleşik beklerler.\n- **Preforme ve Yeni Sentezlenen Sitokinler:** Mast hücreleri granüllerinde önceden sentezlenmiş **hazır TNF-α** depolayan nadir hücrelerdendir. Uyarılma sonrası saatlerce TNF, IL-1, kemokinler ve lökotrienler salgılamaya devam ederler.\n- **Fibrozis ile Bağlantı:** Mast hücre granüllerindeki **triptaz ve kimaz** enzimleri, fibroblast proliferasyonunu uyarır ve latent pro-TGF-β'yı aktif formuna dönüştürerek kollajen sentezini kamçılar.\n- **Klinik:** Romatoid artrit sinovyumunda ve sklerodermalı deri lezyonlarında mast hücresi sayısı katbekat artmıştır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Eklem kıkırdağında kronik yıkım ve fibrozis izlenen romatoid artrit sinovya biyopsisinde damar çevrelerinde yoğun metakromatik granüllü hücreler saptanıyor.",
                "Bu hücrelerin salgıladığı triptaz ve kimaz enzimleri aracılığıyla latent TGF-β'yı aktive ederek eklemde fibrozisi tetikleyen hücresel kaynak hangisidir?",
                [
                    {
                        "text": "Doku mast hücreleridir.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Mast hücreleri granüllerindeki triptaz ve kimaz ile latent TGF-beta'yı parçalayıp aktif hale getirerek fibrozisi uyarır."
                    },
                    {
                        "text": "Eritrositlerdir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Eritrositlerin fibrotik proteaz salgılama yeteneği yoktur."
                    },
                    {
                        "text": "Plazma hücreleridir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Plazma hücreleri antikor üretir, triptaz salgılamaz."
                    }
                ]
            ),
            make_cloze(
                "Mast hücre granüllerinde yer alan triptaz ve kimaz enzimleri fibroblastları uyararak kronik yangıda doku fibrozisini destekler.",
                "triptaz ve kimaz",
                "Mast hücresine özgü iki nötral proteaz"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-13-s35",
        "title": "Kronik Enflamasyonda Nötrofillerin Varlığı: Aktif Kronik Tablolar",
        "content": "Kural olarak nötrofiller akut enflamasyonun hücresi olmakla birlikte, bazı özel kronik tablolarda aylarca yangı alanında kalmaya devam ederler. Bu duruma **Aktif Kronik Enflamasyon** denir:\n\n- **Neden Süreklilik Gösterirler?** Persistan mikrop varlığı veya aralıksız Th17/IL-17 uyarımı nötrofil akışını hiç durdurmaz.\n- **Klasik Örnekler:**\n  1. **Kronik Osteomiyelit:** Nekrotik ölü kemik parçası (sekestr) bakteriler için sığınak oluşturur; aylar geçmesine rağmen ortamda nötrofilik eksüda ve püy akıntısı devam eder.\n  2. **Sigaraya Bağlı KOAH:** Bronş ve bronşiyol lümeninde nötrofil infiltrasyonu sürekli elastaz salgılayarak alveol duvarlarını yıkar (amfizem).\n  3. **Aktinomiçoz (Actinomyces israelii):** Yoğun nötrofil mikroapseleri ve ortasında 'sülfür granülleri' içeren granülomatöz ve apseli kronik tablodur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Saf Kronik Enflamasyon vs Aktif Kronik Enflamasyon",
                "Saf Kronik Enflamasyon",
                "Yalnızca mononükleer hücreler (makrofaj, lenfosit, plazma hücresi) ve fibrozis izlenir.",
                "Aktif Kronik Enflamasyon (Ör. Kronik Osteomiyelit)",
                "Mononükleer infiltrat ve fibrozisin ortasında süregelen canlı nötrofil odakları ve püy mevcuttur."
            ),
            make_recall(
                "Aylar boyu süren bir enfeksiyonda mononükleer infiltratın yanı sıra devam eden nötrofil odaklarının ve püy sızıntısının varlığına ne ad verilir?",
                "Aktif kronik enflamasyondur (süregelen kronik süpüratif süreç).",
                "Nötrofil içeren kronik tablo tanımı"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-13-s36",
        "title": "Doku Fibroblastları ve Miyofibroblastlar",
        "content": "Kronik enflamasyonun 'onarım ve skar' ayağını yürüten ana mezenkimal aktörler fibroblastlar ve miyofibroblastlardır:\n\n- **Fibroblast Farklılaşması:** İstirahat halindeki doku fibroblastları, makrofaj ve mast hücrelerinden gelen **TGF-β** ve **PDGF** uyarısıyla prolifere olur.\n- **Miyofibroblast Dönüşümü:** TGF-β etkisiyle fibroblastlar sitoplazmalarında **alfa-düz kas aktini (α-SMA)** eksprese ederek miyofibroblastlara dönüşür.\n- **Kritik Fonksiyonlar:**\n  1. Tip I ve Tip III kollajen, fibronektin ve proteoglikan sentezleyerek ekstraselüler matriksi yeniden kurarlar.\n  2. Sahip oldukları aktin-miyozin demetleri ile kasılarak yara kenarlarını veya doku defektini birbirine çekerler (**doku kontraksiyonu**).\n  3. Aşırı çalışmaları organ lümenlerinde darlıklara (striktür) ve fonksiyon kaybına yol açar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Fibroblast Aktivasyonu ve Doku Skarlaşma Basamakları",
                [
                    "1. Sitokin Sinyali: M2 makrofajları hasar alanına yüksek düzeyde TGF-beta ve PDGF salgılar.",
                    "2. Proliferasyon: Lokal doku fibroblastları çoğalır ve kollajen sentezlemeye başlar.",
                    "3. Miyofibroblast Farklılaşması: Sitoplazmada alfa-SMA aktin filamentleri belirir.",
                    "4. Kontraksiyon ve Skar: Hücreler kasılarak defekti büzer ve kalıcı fibröz skar bırakır."
                ]
            ),
            make_cloze(
                "TGF-beta uyarısıyla alfa-düz kas aktini sentezleyerek kasılma yeteneği kazanan fibroblastlara miyofibroblast adı verilir.",
                "miyofibroblast",
                "Kasılma yeteneği olan mezenkimal onarım hücresi"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-13-s37",
        "title": "Endotel Hücreleri ve Anjiyogenez Kaskadı",
        "content": "Kronik enflamasyon odağı yüksek metabolik aktiviteye sahip milyonlarca lökosit barındırdığından şiddetli bir oksijen ve besin açlığı (doku hipoksisi) yaşar:\n\n- **HIF-1α Aktivasyonu:** Hipoksi, hücrelerde Hipoksiyle İndüklenen Faktör-1α (HIF-1α) transkripsiyonunu uyarır.\n- **VEGF Patlaması:** Makrofajlar ve tümör/parankim hücreleri yoğun şekilde **VEGF (Vasküler Endotelyal Büyüme Faktörü)** ve **bFGF** salgılar.\n- **Damar Tomurcuklanması:** Sağlam venül endotel hücreleri bazal membranı eritir; kemotaktik VEGF gradiyentine doğru göç ederek lümenli yeni kapiller tüpler oluşturur (anjiyogenez).\n- **Klinik Yansıması:** Yeni oluşan bu damarlar tam olgunlaşmadığı için endotel bağlantıları gevşektir ve 'sızıntılıdır' (leaky vessels); bu nedenle kronik granülasyon dokusu ödemli ve kanamaya yatkındır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Matür Damar vs Kronik Anjiyojenik Yeni Damar",
                "Matür Sağlıklı Kapiller",
                "Sıkı endotel bağlantıları, sağlam bazal membran ve perisit desteği ile sızıntısızdır.",
                "Yeni Oluşan Anjiyojenik Damar",
                "Gevşek endotel bağlantıları, eksik bazal membran; aşırı geçirgen ve ödeme yatkındır."
            ),
            make_quiz(
                "Kronik enflamasyon odağındaki doku hipoksisi sonucu aktive olan ve VEGF transkripsiyonunu başlatarak yeni damarlanmayı tetikleyen temel hücre içi transkripsiyon faktörü hangisidir?",
                [
                    {"key": "A", "text": "HIF-1α (Hipoksiyle İndüklenen Faktör-1α)", "explanation": "A seçeneği DOĞRUDUR: Oksijen düşüşünde stabilize olup VEGF sentezleten tepe regülatördür."},
                    {"key": "B", "text": "NF-κB", "explanation": "B seçeneği yanlıştır: Pro-enflamatuar sitokin transkripsiyon faktörüdür."},
                    {"key": "C", "text": "T-bet", "explanation": "C seçeneği yanlıştır: Th1 farklılaşma faktörüdür."},
                    {"key": "D", "text": "GATA-3", "explanation": "D seçeneği yanlıştır: Th2 farklılaşma faktörüdür."},
                    {"key": "E", "text": "Kaspaz-3", "explanation": "E seçeneği yanlıştır: Apoptoz yürütücü proteazdır."}
                ],
                "A"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-13-s38",
        "title": "Doğal Öldürücü (NK) Hücreler ve İnnate Lenfoid Hücreler",
        "content": "Kronik enflamasyonda adaptif lenfositlerin sahaya inmesinden önce ve süreç boyunca doğal bağışıklığın lenfoid kolları devrededir:\n\n- **Doğal Öldürücü (NK) Hücreler:** TCR taşımazlar. Yüzeyinde MHC Sınıf I ekspresyonu kaybolmuş virüslü veya tümör hücrelerini doğrudan perforin/granzim ile öldürürler. Ayrıca erken dönemde bolca **IFN-γ** üreterek makrofaj aktivasyonunu başlatırlar.\n- **İnnate Lenfoid Hücreler (ILC'ler):** TCR ve antijen özgüllüğü bulunmayan doku yerleşik lenfositlerdir. Sitokin profillerine göre T yardımcı hücrelerini taklit ederler:\n  - **ILC1:** T-bet taşır, IFN-γ salgılar (Th1 benzeri).\n  - **ILC2:** GATA-3 taşır, IL-5 ve IL-13 salgılar (Th2 benzeri).\n  - **ILC3:** RORγt taşır, IL-17 ve IL-22 salgılar (Th17 benzeri). Mukozal bariyer savunmasını sağlarlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İnnate Lenfoid Hücre (ILC)", "Benzer T Hücre Soyu", "Temel Sitokin Ürünü"],
                [
                    [
                        {"text": "ILC1", "isMasked": False, "hint": ""},
                        {"text": "Th1 lenfositi", "isMasked": False, "hint": ""},
                        {"text": "İnterferon-gama (IFN-γ)", "isMasked": True, "hint": "Makrofaj aktive edici majör sitokin"}
                    ],
                    [
                        {"text": "ILC2", "isMasked": True, "hint": "Th2 benzeri doğal lenfoid hücre"},
                        {"text": "Th2 lenfositi", "isMasked": False, "hint": ""},
                        {"text": "IL-5 ve IL-13", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "ILC3", "isMasked": False, "hint": ""},
                        {"text": "Th17 lenfositi", "isMasked": True, "hint": "Nötrofil çeken soy benzeri"},
                        {"text": "IL-17 ve IL-22", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Doğal öldürücü (NK) hücrelerin hedef hücreyi öldürmesini engelleyen ve eksikliğinde lizis başlatan hücre yüzey inhibitör reseptör ligantı nedir?",
                "MHC Sınıf I molekülleridir (Kayıp 'self' hipotezi).",
                "Tüm sağlıklı hücrelerde bulunan doku uygunluk antijeni"
            )
        ]
    })

    # Slide 39
    slides.append({
        "id": "k1-13-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Kronik Enflamasyonun Yardımcı Hücreleri ve Hücresel Ağ Yapısı",
        "content": "Bu kontrol noktasında kronik enflamasyonda makrofaj ve T lenfositlere eşlik eden diğer kritik hücresel elemanları özetliyoruz:\n\n- **Eozinofiller:** İki loblu çekirdekli, CCR3/eotaksin ve IL-5 ile dokuya çekilen, MBP ve ECP ile parazit/doku hasarı yapan hücreler; Charcot-Leyden kristalleri.\n- **Mast Hücreleri:** Hazır TNF-α depoları, triptaz ve kimaz ile latent TGF-β aktivasyonu ve fibrozis tetikleyicisi.\n- **Nötrofiller (Aktif Kronik):** Kronik osteomiyelit ve sigaraya bağlı KOAH'ta süregelen püy ve doku yıkımı.\n- **Miyofibroblastlar:** TGF-β uyarısıyla α-SMA eksprese eden, kollajen sentezleyip yarayı büzen hücreler.\n- **Endotel ve Anjiyogenez:** Hipoksi → HIF-1α → VEGF → yeni sızıntılı kılcal damarlar.\n- **ILC Ailesi:** TCR içermeyen doku lenfositleri (ILC1 Th1'i, ILC2 Th2'yi, ILC3 Th17'yi taklit eder).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Astımlı bir hastanın bronş lavajında bulunan, eozinofil kaynaklı Charcot-Leyden kristallerinin kimyasal yapısını oluşturan temel enzim proteini hangisidir?",
                [
                    {"key": "A", "text": "Lizofosfolipaz (Galektin-10)", "explanation": "A seçeneği DOĞRUDUR: Charcot-Leyden kristalleri eozinofil lizofosfolipaz enziminin agregatıdır."},
                    {"key": "B", "text": "Miyeloperoksidaz", "explanation": "B seçeneği yanlıştır: Nötrofil azurofilik granül enzimidir."},
                    {"key": "C", "text": "Asit fosfataz", "explanation": "C seçeneği yanlıştır: Lizozomal enzimdir."},
                    {"key": "D", "text": "Arginaz-1", "explanation": "D seçeneği yanlıştır: M2 makrofaj enzimidir."},
                    {"key": "E", "text": "Elastaz", "explanation": "E seçeneği yanlıştır: Nötrofil serin proteazıdır."}
                ],
                "A"
            ),
            make_cloze(
                "Miyofibroblastlar sitoplazmalarında alfa-düz kas aktini eksprese ederek yara kontraksiyonunu ve doku büzülmesini sağlarlar.",
                "alfa-düz kas aktini",
                "Miyofibroblastın kasılmasını sağlayan sitoskeletal protein"
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-13-s40",
        "title": "Kronik Enflamatuar İnfiltratın Histopatolojik Raporlanması",
        "content": "Biyopsi materyalini inceleyen patolog kronik enflamatuar infiltratı raporlarken klinik hekime yol gösterici kritik parametreleri belirtir:\n\n1. **Dağılım Deseni (Patern):**\n   - **İnterstisyel / Diffüz:** Doku lifleri arasına homojen yayılmış hücreler (ör. interstisyel nefrit).\n   - **Perivasküler Cuffing:** Damarlar etrafında manşon oluşturan lenfositler (ör. viral ensefalit, sifiliz).\n   - **Agregat / Foliküler:** Germinal merkezli lenfoid yapılar (ör. Hashimoto, romatoid artrit).\n   - **Granülomatöz:** Epiteloid histiositlerden oluşan sınırları belirgin nodüller.\n2. **Hücresel Kompozisyon:** Makrofaj/lenfosit oranı, plazma hücresi zenginliği (sifiliz/otoimmünite lehine), eozinofil varlığı (alerji/parazit lehine), nötrofil eşliği (aktif alevlenme lehine).\n3. **Fibrozis ve Parankim Kaybı:** Fibrozisin evrelenmesi (kronik hepatitte Evre 0-4 skorlaması).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Diffüz İnterstisyel İnfiltrat vs Nodüler / Granülomatöz İnfiltrat",
                "Diffüz İnterstisyel Patern",
                "Hücreler doku parankimi arasına saçılmıştır; sınırları belirsizdir (ör. kronik interstisyel nefrit).",
                "Nodüler / Granülomatöz Patern",
                "Epiteloid histiositler sınırları net nodüller halinde toplanmıştır (ör. tüberküloz, sarkoidoz)."
            ),
            make_recall(
                "Doku biyopsisinde damarların çevresinde manşon şeklinde sıkıca kümelenen lenfosit infiltrasyonuna patolojide ne ad verilir?",
                "Perivasküler kuffing (perivascular cuffing).",
                "Damar çevresi manşonlaşma terimi"
            )
        ]
    })

    return slides
