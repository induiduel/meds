"""
Bölüm 5: Patolojik Apoptoz Nedenleri ve Morfolojik Özellikler
Adımlar: 41 - 50
Checkpoint: Adım 49 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # ADIM 41
    slides.append({
        "slideNumber": 41,
        "title": "Patolojik Apoptoz: DNA Hasarı ve Hücresel Savunma",
        "subtitle": "Radyasyon, kemoterapi ve serbest radikallerin tetiklediği p53 bağımlı intihar",
        "badge": "DNA Hasarı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücreler ultraviyole ışık, iyonizan radyasyon, alkilleyici kemoterapi ilaçları veya aşırı serbest radikal "
            "(ROS) saldırısına uğradığında çift sarmallı DNA kırıkları meydana gelir. Eğer bu hasar tamir edilemeyecek "
            "boyuttaysa, hücre genomik dengesizlik ve malignite riskini önlemek adına apoptoza sevk edilir.\n\n"
            "Bu süreçte ana orkestra şefi 'p53' tümör baskılayıcı proteinidir. p53 hasarı algıladığında önce hücre "
            "döngüsünü G1 evresinde durdurur. Hasar onarılamazsa, proapoptotik 'BH3-only' proteinlerini aktive eder.\n\n"
            "> [SINAV SPOTU] Patolojik DNA hasarında apoptoz mitokondriyal (içsel) yolağı ateşleyerek kaspazları "
            "devreye sokar; böylece potansiyel kanser hücreleri vücuttan temizlenir.\n\n"
            "Kanser hücrelerinin çoğunda p53 mutasyona uğramıştır; bu sayede tümör hücreleri kemoterapiye direnç gösterir."
        ),
        "medicalTerms": [
            {"term": "Genotoksik Stres", "explanation": "Radyasyon, toksin veya ROS ile DNA yapısında kırık ve hasar oluşması."},
            {"term": "BH3-only Proteinler", "explanation": "Hücre içi stresi ve DNA hasarını algılayarak mitokondriyal apoptozu başlatan öncü moleküller (Bim, Bid, Puma, Noxa)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] DNA hasarında (radyasyon, kemoterapi) apoptoz proapoptotik BH3-only proteinler ve mitokondriyal yol ile tetiklenir.",
            "📌 [SINAV SPOTU] p53 tamir edilemeyen DNA hasarında apoptoz emrini veren ana mekanizmadır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Genom Güvenliği", "desc": "Onarılamaz DNA kırıklarında hücrenin apoptozla feda edilmesi.", "isKey": True},
                {"title": "Mitokondriyal Yolak", "desc": "BH3-only proteinlerinin Bax/Bak üzerinden mitokondriyi delmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Radyasyona Bağlı DNA Hasarı ve Apoptoz Zinciri",
                [
                    "1. Radyasyon Darbesi: İyonizan ışınlar çift zincirli DNA kırıklarına neden olur.",
                    "2. p53 Akümülasyonu: DNA hasar sensörleri (ATM/ATR) p53 proteinini fosforilleyerek stabilize eder.",
                    "3. BH3-only Transkripsiyonu: p53 Puma ve Noxa gibi pro-apoptotik proteinlerin sentezini patlatır.",
                    "4. Mitokondri Sızıntısı: Puma/Noxa Bax ve Bak'ı aktive ederek mitokondriden sitokrom c sızdırır.",
                    "5. Kaspaz Apoptozu: Sitokrom c Kaspaz-9 ve Kaspaz-3'ü devreye sokarak hücreyi parçalar."
                ]
            ),
            make_cloze(
                "İyonizan radyasyon ve kemoterapiye bağlı DNA hasarında hücreyi apoptoza yönlendiren temel yolak mitokondriyal yolak mekanizmasıdır.",
                "mitokondriyal yolak",
                "İçsel sitokrom c sızıntısına dayalı apoptoz yolağı"
            )
        ]
    })

    # ADIM 42
    slides.append({
        "slideNumber": 42,
        "title": "Yanlış Katlanmış Protein Birikimi: ER Stresi Kaynaklı Apoptoz",
        "subtitle": "Kıvrılamayan mutant proteinlerin şaperon kapasitesini aşarak hücreyi öldürmesi",
        "badge": "ER Stresi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Genetik mutasyonlar, serbest radikal hasarı veya yaşlanma sonucu endoplazmik retikulumda (ER) yanlış "
            "katlanmış proteinler kümelenebilir. Hücre başlangıçta şaperon molekülleri (BiP/GRP78) üreterek bu proteinleri "
            "düzeltmeye veya proteazomlara gönderip yıkmaya çalışır (Adaptif UPR).\n\n"
            "Ancak yanlış katlanmış protein yükü hücrenin adaptif kapasitesini aştığında 'terminal ER stresi' gelişir.\n\n"
            "> [SINAV SPOTU] ER zarındaki stres sensörleri (IRE1, PERK, ATF6) proapoptotik BH3-only proteinleri ve "
            "CHOP faktörünü aktive ederek doğrudan apoptozu indükler.\n\n"
            "Alzheimer hastalığı (amiloid-beta), Parkinson hastalığı (alfa-sinüklein) ve Huntington koresi gibi "
            "nörodejeneratif hastalıkların temelinde yanlış katlanmış protein birikimine bağlı patolojik apoptoz yatar."
        ),
        "medicalTerms": [
            {"term": "ER Stresi", "explanation": "Endoplazmik retikulum lümeninde anormal katlanmış proteinlerin birikmesiyle oluşan metabolik kriz."},
            {"term": "Katlanmamış Protein Yanıtı (UPR)", "explanation": "ER stresini çözmek için şaperon sentezini artıran, çözülemezse apoptoza götüren sinyal ağı."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yanlış katlanmış protein birikimi ER stresini ve proapoptotik BH3-only proteinleri tetikler.",
            "📌 [SINAV SPOTU] Nörodejeneratif hastalıklar (Alzheimer, Parkinson) ER stresi kaynaklı patolojik apoptoz örnekleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Şaperon Yetmezliği", "desc": "Katlanamayan proteinlerin ER lümeninde toksik kümelenmesi.", "isKey": True},
                {"title": "Nörodejenerasyon", "desc": "Alzheimer ve Parkinson'da nöronların apoptozla kaybı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Alfa-1 antitripsin eksikliği olan bir hastanın hepatositlerinde mutant proteinler endoplazmik retikulumda kıvrılamayıp birikiyor. Hücre bu kriz karşısında hangi yolu izler?",
                [
                    {
                        "text": "Proteinler lümende kristalize olur ve hücre hiçbir zarar görmeden mitoz bölünmesini hızlandırır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! ER stresi mitozu değil hücre hasarını ve duraklamayı tetikler."
                    },
                    {
                        "text": "Önce şaperonlarla düzeltmeye çalışır; kapasite aşılırsa BH3-only proteinler ve CHOP üzerinden apoptozu aktive eder.",
                        "isCorrect": True,
                        "feedback": "Kusursuz patofizyolojik mantık! Adaptif kapasite aşılınca hücre ER stresi aracılı apoptoza gider."
                    },
                    {
                        "text": "Hücre derhal gazlı gangrene uğrayarak patlar.",
                        "isCorrect": False,
                        "feedback": "Tıbbi olarak anlamsızdır."
                    }
                ]
            ),
            make_cloze(
                "Endoplazmik retikulumda katlanmamış proteinlerin aşırı birikmesi sonucu tetiklenen hücresel krize ER stresi denir.",
                "ER stresi",
                "Endoplazmik retikulumun aşırı protein yüküyle boğulması durumu"
            )
        ]
    })

    # ADIM 43
    slides.append({
        "slideNumber": 43,
        "title": "Viral Enfeksiyonlarda Apoptoz: Konak ve Virüs Arasındaki Savaş",
        "subtitle": "Viral hepatitlerde Councilman cisimcikleri ve sitotoksik T hücre saldırısı",
        "badge": "Viral Patoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Viral enfeksiyonlar sırasında apoptoz iki farklı mekanizmayla ortaya çıkabilir. İlk mekanizma, virüsün "
            "kendi proteinlerinin hücre içi kaspazları veya proapoptotik genleri doğrudan aktive etmesidir.\n\n"
            "İkinci ve çok daha yaygın mekanizma ise konağın bağışıklık sistemidir. Enfekte hücreler viral peptitleri "
            "MHC-I ile yüzeylerinde sergilediklerinde, CD8+ Sitotoksik T Lenfositler (CTL) hedef hücreyi tanır ve "
            "perforin/granzim ve FasL ile apoptoza sürükler.\n\n"
            "> [SINAV SPOTU] Akut viral hepatitte (HBV, HCV) sitotoksik T hücreleri tarafından apoptoza uğratılan "
            "büzüşmüş, koyu pembe ve çekirdeksiz hepatositlere 'Councilman cisimciği' (apoptotik hepatosit) adı verilir.\n\n"
            "Bazı virüsler (ör. EBV, HPV) ise hücreyi canlı tutarak çoğalabilmek için apoptozu engelleyen proteinler üretir."
        ),
        "medicalTerms": [
            {"term": "Councilman Cisimciği", "explanation": "Viral hepatitte apoptoza uğrayarak büzüşen ve sinüzoidlere dökülen koyu eozinofilik hepatosit kalıntısı."},
            {"term": "Viral Apoptoz", "explanation": "Enfekte hücrenin virüs yayılımını önlemek için CTL'lerce apoptozla imha edilmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Viral enfeksiyonlarda apoptoz; viral proteinlerle veya sitotoksik T lenfositlerin (CTL) kaspaz aktivasyonu ile gerçekleşir.",
            "📌 [SINAV SPOTU] Viral hepatitte görülen Councilman cisimcikleri tipik apoptotik hepatositlerdir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İmmün İnfaz", "desc": "CTL'lerin enfekte hücreyi perforin/granzim ile apoptoza göndermesi.", "isKey": True},
                {"title": "Councilman Cisimciği", "desc": "Hepatit biyopsisinde büzüşmüş yuvarlak apoptotik hepatosit kalıntısı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Akut viral hepatitli bir hastanın karaciğer biyopsisinde sinüzoid kenarında izlenen, sitoplazması büzüşmüş ve koyu pembe boyanan, kaspaz aktivasyonlu apoptotik hepatosite ne ad verilir?",
                {
                    "A": "Mallory-Denk cisimciği",
                    "B": "Councilman cisimciği",
                    "C": "Lewy cisimciği",
                    "D": "Aschoff nodülü",
                    "E": "Russell cisimciği"
                },
                "B",
                {
                    "A": "Mallory-Denk alkolik hepatitte keratin agregatıdır.",
                    "B": "Doğru cevap B'dir: Councilman cisimciği viral hepatitteki apoptotik hepatosittir.",
                    "C": "Lewy cisimleri Parkinson hastalığında nöronlarda görülür.",
                    "D": "Aschoff granülomu romatizmal karditte izlenir.",
                    "E": "Russell cisimleri plazma hücrelerinde immünoglobulindir."
                }
            ),
            make_cloze(
                "Akut viral hepatitte sitotoksik T lenfositlerin etkisiyle apoptoza uğrayan hepatosit kalıntılarına Councilman cisimciği denir.",
                "Councilman cisimciği",
                "Viral hepatitteki apoptotik hepatositlerin özel patoloji adı"
            )
        ]
    })

    # ADIM 44
    slides.append({
        "slideNumber": 44,
        "title": "Apoptozun Morfolojik Evreleri: Hücre Büzüşmesi (Shrinkage)",
        "subtitle": "Sitoplazmanın yoğunlaşması ve organellerin sıkıca paketlenmesi",
        "badge": "Morfoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun morfolojik incelemesi yapıldığında nekroz ile taban tabana zıt bir hacim dinamiği gözlenir. "
            "Nekrozda ATP azlığı sonucu Na+/K+ ATPaz durur ve hücre su alarak devasa boyutlara şişerken (onkozis); "
            "apoptozda hücre belirgin şekilde 'küçülür ve büzüşür' (cell shrinkage).\n\n"
            "Kaspazların etkisiyle iyon kanalları regüle edilir, hücre sitozolik su ve elektrolit kaybeder. "
            "Sitoplazma yoğunlaşır ve dehidrate olur.\n\n"
            "> [SINAV SPOTU] Sitoplazmanın bu aşırı yoğunlaşması ve organellerin dar bir alana sıkıca paketlenmesi "
            "sonucu hücre hematoksilen-eozin preparatlarında son derece koyu pembe (koyu eozinofilik) bir renk alır.\n\n"
            "Hücre komşu epitel hücreleriyle yaptığı dezmozom ve bağlantı komplekslerini çözerek komşularından ayrışır."
        ),
        "medicalTerms": [
            {"term": "Hücre Büzüşmesi (Shrinkage)", "explanation": "Apoptozun ilk morfolojik bulgusu olan sitozolik su kaybı ve hücre boyutunda küçülme."},
            {"term": "Organel Paketlenmesi", "explanation": "Mitokondri ve endoplazmik retikulumun yoğunlaşan sitoplazmada sıkışarak kümelenmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nekrozda hücre şişer (onkozis); Apoptozda hücre BÜZÜŞÜR ve KÜÇÜLÜR (shrinkage).",
            "📌 [SINAV SPOTU] Sitoplazma yoğunlaşır, organeller sıkı paketlenir ve hücre koyu eozinofilik boyanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hacim Dinamiği", "desc": "Su ve potasyum kaybıyla hücre hacminin küçülmesi.", "isKey": True},
                {"title": "Ayrışma Prensibi", "desc": "Komşu hücrelerle bağlantıların koparılarak bağımsızlaşma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Nekroz vs Apoptoz Hücre Boyutu Dinamiği",
                "Nekroz Boyutu (Şişme)",
                "ATP yokluğunda Na+/K+ pompası durur; hücre içine kontrolsüz su girer ve hücre patlayacak kadar şişer (onkozis).",
                "Apoptoz Boyutu (Büzüşme)",
                "Hücre su ve elektrolit kaybederek büzüşür ve küçülür; sitoplazma yoğunlaşır ve koyu eozinofilik hale gelir."
            ),
            make_cloze(
                "Nekrozda hücre hacmi şişerken apoptozda hücre büzüşür ve küçülür; organeller yoğunlaşarak sıkı paketlenir.",
                "büzüşür",
                "Apoptozdaki hücre boyut değişimi yönü"
            )
        ]
    })

    # ADIM 45
    slides.append({
        "slideNumber": 45,
        "title": "Kromatin Kondansasyonu ve Hilal Morfolojisi: Apoptozun İmzası",
        "subtitle": "Kromatinin nükleer zarın hemen altına hilal şeklinde toplanması ve yoğunlaşması",
        "badge": "Çekirdek Morfolojisi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun ışık ve elektron mikroskobunda en karakteristik ve tanı koydurucu morfolojik özelliği "
            "'kromatin kondansasyonu'dur (yoğunlaşması). Normal hücrede dağınık ve şeffaf duran ökromatin, "
            "kaspaz-aktive endonükleazların etkisiyle kümeleşmeye başlar.\n\n"
            "Kondanse olan kromatin blokları nükleer membranın hemen iç yüzeyine göç eder ve burada toplanır. "
            "Elektron mikroskobunda nükleer zar kenarlarında adeta hilal şeklinde dizilmiş koyu siyah heterokromatin kütleleri izlenir.\n\n"
            "> [SINAV SPOTU] Kromatin kondansasyonu ve çekirdek zarı çevresinde hilal (crescent) şeklinde toplanması "
            "apoptozun en değişmez ve en erken nükleer bulgusudur.\n\n"
            "Daha sonra çekirdek nükleozomlar arası mesafelerden kırılarak çok sayıda küçük parçaya bölünür."
        ),
        "medicalTerms": [
            {"term": "Kromatin Kondansasyonu", "explanation": "Nükleer DNA'nın sıkışarak nükleer zar altına çekilmesi ve hilal şeklinde yoğunlaşması."},
            {"term": "Kromatin Hilalleri (Crescents)", "explanation": "Elektron mikroskobunda nükleer membran altında görülen hilal biçimli heterokromatin yığınları."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kromatin kondansasyonu apoptozun en karakteristik morfolojik özelliğidir.",
            "📌 [SINAV SPOTU] Kromatin kenarlara toplanır; çekirdek çevresinde hilal şeklinde yoğunlaşmalar oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Marjinasyon", "desc": "Kromatinin nükleer zar çeperine doğru itilip yığılması.", "isKey": True},
                {"title": "Hilal Görünümü", "desc": "Elektron mikrografında çekirdek çevresinde hilal biçimli kütleler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Patolojik Süreç", "Çekirdek Değişikliği", "Kromatin Organizasyonu"],
                [
                    [("Apoptoz", False, ""), ("Kromatin Kondansasyonu ve Hilaller", True, "Apoptoza özgü nükleer şekil"), ("Nükleer zar altına toplanma", False, "")],
                    [("Nekroz (Karyolizis)", False, ""), ("Nükleer Soluklaşma ve Erime", True, "DNAaz enzimatik yıkımı"), ("Bazofilik rengin tamamen kaybolması", False, "")],
                    [("Nekroz (Piknoz)", False, ""), ("Rastgele Büzüşme ve Katılaşma", True, "Nükleer kütle küçülmesi"), ("Koyu siyah homojen bilye nükleus", False, "")]
                ]
            ),
            make_cloze(
                "Apoptoz sürecinde kromatin kondanse olarak çekirdek zarının hemen altında hilal şeklinde toplanır.",
                "hilal",
                "Kromatinin nükleer kenarda oluşturduğu geometrik biçim"
            )
        ]
    })

    # ADIM 46
    slides.append({
        "slideNumber": 46,
        "title": "Zar Kabarcıklanması ve Tomurcuklanma (Blebbing): Apoptotik Cisimcikler",
        "subtitle": "Hücre iskeletinin kaspazlarla kesilmesi ve membranla çevrili paketlerin ayrılması",
        "badge": "Tomurcuklanma",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptoz ilerledikçe hücre iskeletini (aktin, fodrin, lamin) oluşturan yapısal proteinler Kaspaz-3 "
            "tarafından sistematik olarak kesilir. Sitoskeleton bütünlüğünü kaybeden hücre plazma membranı "
            "dışarıya doğru fıtıklaşarak parmaksı çıkıntılar ve kabarcıklar oluşturur (membrane blebbing).\n\n"
            "Bu kabarcıkların içine yoğunlaşmış sitoplazma, sıkı organeller ve nükleus parçacıkları dolar. "
            "Ardından tomurcuklar hücre gövdesinden boğumlanarak bağımsız veziküller halinde ayrılır.\n\n"
            "> [SINAV SPOTU] Plazma zarı ile tamamen çevrelenmiş, içinde çekirdek ve organel parçaları barındıran "
            "bu paketlere 'Apoptotik Cisimcikler' (apoptotic bodies) adı verilir.\n\n"
            "Böylece hücre tek bir anda patlamak yerine onlarca küçük, yutulması kolay güvenli pakete bölünmüş olur."
        ),
        "medicalTerms": [
            {"term": "Tomurcuklanma (Blebbing)", "explanation": "Sitoskeleton gevşemesiyle plazma zarının dışa doğru balonlaşması ve boğumlanması."},
            {"term": "Apoptotik Cisimcik", "explanation": "Zarla sarılı, hücresel içerik sızdırmayan, makrofaj fagositozuna hazır küçük hücre parçası."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Plazma zarında kabarcıklanma (blebbing) ve tomurcuklanma meydana gelir.",
            "📌 [SINAV SPOTU] Hücre, zar ile çevrili sitoplazma ve çekirdek parçaları içeren 'apoptotik cisimciklere' bölünür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sitoskeleton Yıkımı", "desc": "Kaspazların aktini kesmesiyle zar stabilitesinin bozulması.", "isKey": True},
                {"title": "Paketleme Sistemi", "desc": "Zarla kaplı güvenli apoptotik cisimcikler üretilmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Apoptotik Cisimcik Oluşum Zinciri",
                [
                    "1. Efektör Kaspaz Aktivasyonu: Kaspaz-3 aktifleşerek aktin ve lamin proteinlerini parçalar.",
                    "2. Hücre İskeletinin Çöküşü: Zar desteğini kaybeden plazma membranı dışa doğru tomurcuklanır.",
                    "3. Organel Yüklenmesi: Sitoplazmik kabarcıkların içine organeller ve çekirdek kırıntıları girer.",
                    "4. Boğumlanma ve Ayrılma: Kabarcıkların boynu sıkışarak bağımsız apoptotik cisimcikler kopar.",
                    "5. Zarlı Koruma: Parçacıklar dış zarlarını koruduğu için hücre içi enzimler dışarı sızamaz."
                ]
            ),
            make_cloze(
                "Apoptozda hücre zarıyla sarılı sitoplazma ve çekirdek parçalarını barındıran yapılara apoptotik cisimcikler denir.",
                "apoptotik cisimcikler",
                "Zarla çevrili paketlenmiş hücresel kalıntılar"
            )
        ]
    })

    # ADIM 47
    slides.append({
        "slideNumber": 47,
        "title": "Fosfatidilserin Dışa Dönüşü: Makrofajlar İçin 'Beni Ye' Sinyali",
        "subtitle": "Flippaz enziminin durması ve skramblaz ile iç tabakadaki lipidlerin dışa takla atması",
        "badge": "Beni Ye Sinyali",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Canlı bir hücrenin plazma membranında fosfolipidler son derece asimetrik bir dağılıma sahiptir. "
            "Negatif yüklü bir fosfolipid olan 'Fosfatidilserin (PS)', normalde hücre içindeki ATP bağımlı flippaz "
            "enzimi sayesinde daima zarın İÇ (sitoplazmik) yaprağında tutulur.\n\n"
            "Apoptoz kaspaz kaskadı aktive olduğunda, flippaz enzimi inaktive edilirken fosfolipidleri rastgele "
            "karıştıran 'Skramblaz' enzimi uyarılır. Sonuç olarak fosfatidilserin molekülleri dış yaprağa geçer.\n\n"
            "> [SINAV SPOTU] Plazma zarının dış yüzeyinde beliren fosfatidilserin, dolaşan makrofajlar için "
            "evrensel bir 'Beni Ye' (Eat Me) sinyalidir!\n\n"
            "Laboratuvarda apoptotik hücreleri erken evrede saptamak için fosfatidilserine yüksek afiniteyle bağlanan "
            "floresan işaretli 'Anneksin V' (Annexin V) proteini kullanılır."
        ),
        "medicalTerms": [
            {"term": "Fosfatidilserin (PS)", "explanation": "Normalde zarın iç yaprağında bulunan, apoptozda dışa dönerek fagositozu tetikleyen fosfolipid."},
            {"term": "Anneksin V", "explanation": "Dışa dönen fosfatidilserini bağlayarak apoptotik hücreleri akım sitometrisinde tespit eden reaktif."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Apoptotik hücrelerin plazma zarında Fosfatidilserin iç tabakadan dış tabakaya geçer ('Beni ye' sinyali).",
            "📌 [SINAV SPOTU] Erken apoptozu saptamak için laboratuvarda Anneksin V (Annexin V) boyası kullanılır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Membran Asimetri Kaybı", "desc": "Fosfatidilserinin zarın dış yüzeyine takla atması.", "isKey": True},
                {"title": "Anneksin V Testi", "desc": "Akım sitometrisinde apoptotik hücreleri işaretleme prensibi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Sağlıklı Membran vs Apoptotik Membran Fosfatidilserin Dağılımı",
                "Sağlıklı Hücre Membranı",
                "Fosfatidilserin (PS) ATP bağımlı flippaz ile YALNIZCA iç (sitoplazmik) yaprakta hapsedilmiştir. Dışta PS yoktur.",
                "Apoptotik Hücre Membranı",
                "Skramblaz aktivasyonu ile Fosfatidilserin DIŞ yaprağa döner; makrofaj reseptörleri için 'Beni ye' bayrağı oluşturur."
            ),
            make_cloze(
                "Apoptotik hücrelerde makrofajlar tarafından tanınmayı sağlayan beni ye sinyalini plazma zarının dışına çıkan fosfatidilserin oluşturur.",
                "fosfatidilserin",
                "Zar iç yaprağından dış yaprağa takla atan anyonik fosfolipid"
            )
        ]
    })

    # ADIM 48
    slides.append({
        "slideNumber": 48,
        "title": "Sessiz Fagositoz: İçerik Sızmadan Yangısız Temizlik",
        "subtitle": "Makrofajların apoptotik cisimcikleri inflamasyon üretmeden dakikalar içinde yutması",
        "badge": "Fagositoz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun en kusursuz zaferi, geride hiçbir enkaz ve doku hasarı bırakmamasıdır. Nekrozda hücre patlayıp "
            "sitoplazmik enzimler ve DAMP (Hasar İlişkili Moleküler Paternler) molekülleri ortama saçıldığından nötrofiller "
            "hücum eder ve şiddetli yangı oluşur.\n\n"
            "Apoptozda ise apoptotik hücreler soluble çekici faktörler salgılar ve dış zarlarındaki fosfatidilserin "
            "sayesinde makrofajlar tarafından anında tanınır.\n\n"
            "> [SINAV SPOTU] Makrofajlar apoptotik cisimcikleri saniyeler içinde fagositozla yutar. İçerik hücre dışına "
            "asla sızmadığı için inflamatuar yanıt sıfırdır!\n\n"
            "Dahası, apoptotik hücreyi yutan makrofajlar ortama anti-enflamatuar sitokinler (TGF-beta ve IL-10) "
            "salgılayarak çevredeki olası inflamasyonu dahi aktif olarak bastırır."
        ),
        "medicalTerms": [
            {"term": "Sessiz Fagositoz (Efferositoz)", "explanation": "Apoptotik cisimciklerin çevreye hiçbir inflamatuar mediyatör saçılmadan makrofajlarca yutulması."},
            {"term": "Anti-enflamatuar Yanıt", "explanation": "Apoptotik hücre temizliği sırasında TGF-beta ve IL-10 salınarak yangının önlenmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Apoptotik cisimcikler makrofajlarca içerik dışarı sızmadan hızla yutulur.",
            "📌 [SINAV SPOTU] Apoptozda inflamatuar reaksiyon minimaldir veya tamamen yoktur.",
            "📌 [SINAV SPOTU] Makrofajlar temizlik sırasında anti-inflamatuar faktörler (TGF-β, IL-10) salgılar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sıfır Sızıntı", "desc": "Lizozomal enzimlerin dokuya yayılmasının tamamen engellenmesi.", "isKey": True},
                {"title": "Anti-inflamatuar İklim", "desc": "TGF-beta ve IL-10 üretimiyle çevre dokunun korunması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Nekroza uğrayan dokuda şiddetli inflamasyon ve ödem görülürken, kitlesel apoptoz geçiren bir organda neden inflamasyon gelişmez?",
                "Çünkü apoptozda plazma zarı sağlam kalır, içerik dışarı sızmaz ve apoptotik cisimcikler makrofajlarca hızla ve sessizce fagositozla temizlenir."
            ),
            make_cloze(
                "Apoptotik cisimcikler makrofajlar tarafından hızla yutulduğu ve hücre içeriği dışarı sızmadığı için dokuda inflamatuar yanıt oluşmaz.",
                "inflamatuar yanıt",
                "Doku hasarına karşı lökositlerin oluşturduğu yangısal tepki"
            )
        ]
    })

    # ADIM 49 (CHECKPOINT 5)
    slides.append({
        "slideNumber": 49,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Patolojik Apoptoz ve Morfolojik Bulgular",
        "subtitle": "DNA hasarı, ER stresi, Councilman cisimcikleri, kromatin hilalleri ve fagositoz sentezi",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 5,
        "synthesisNarrative": (
            "Bu kontrol noktasında, apoptozun patolojik tetikleyicilerini ve ışık/elektron mikroskobundaki "
            "morfolojik basamaklarını tek bir zihinsel haritada birleştiriyoruz.\n\n"
            "Patolojik apoptoz; p53 aracılı DNA hasarı, yanlış katlanmış proteinlerin yol açtığı ER stresi ve "
            "viral hepatitteki Councilman cisimcikleri gibi hücresel felaketlerde devreye girer.\n\n"
            "> [ÖZET REÇETE] Morfolojik Apoptoz Kılavuzu:\n"
            "1. Hücre büzüşmesi ve yoğunlaşma (shrinkage - koyu eozinofilik)\n"
            "2. Kromatin kondansasyonu (nükleer zar altında hilal şeklinde marjinasyon)\n"
            "3. Zar kabarcıklanması (blebbing) ve apoptotik cisimcikler\n"
            "4. Fosfatidilserin dışa dönmesi ('Beni ye' sinyali - Anneksin V pozitifliği)\n"
            "5. Makrofajlarca sessiz fagositoz -> Sıfır İnflamasyon!\n\n"
            "Bu morfolojik sıra apoptozun histolojik teşhisinde altın standarttır."
        ),
        "medicalTerms": [
            {"term": "Apoptotik Morfoloji", "explanation": "Büzüşme, kromatin marjinasyonu, tomurcuklanma ve apoptotik cisimcikler bütünü."},
            {"term": "Efferositoz", "explanation": "Apoptotik cisimciklerin makrofajlarca yangısız ortadan kaldırılması."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Hücre büzüşmesi (shrinkage) + nükleer zar altında kromatin hilalleri apoptozun imzasıdır.",
            "📌 [CHECKPOINT ÖZETİ] Apoptotik cisimcikler zarla çevrilidir; içerik dışarı sızmaz.",
            "📌 [CHECKPOINT ÖZETİ] Fosfatidilserin dışa dönerek 'Beni ye' sinyali verir; Anneksin V ile boyanır.",
            "📌 [CHECKPOINT ÖZETİ] Makrofajlar sessizce yutar; ortamda inflamasyon gelişmez."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-13",
                "Apoptozun ışık ve elektron mikroskobundaki en erken ve en karakteristik nükleer bulgusu nedir?",
                "Kromatin kondansasyonudur; kromatin çekirdek zarının hemen altında hilal (crescent) şeklinde toplanır ve yoğunlaşır."
            ),
            make_flashcard(
                "fc-k1-05-14",
                "Apoptotik hücrelerin makrofajlar tarafından hızla tanınıp yutulmasını sağlayan biyokimyasal 'Beni ye' sinyali nedir?",
                "Normalde zarın iç tabakasında bulunan fosfatidilserin molekülünün dış tabakaya takla atmasıdır (flip-flop)."
            ),
            make_flashcard(
                "fc-k1-05-15",
                "Akut viral hepatitte görülen Councilman cisimciği nedir ve patolojik anlamı nedir?",
                "Sitotoksik T lenfositler tarafından apoptoza uğratılmış, büzüşmüş, koyu pembe ve çekirdeksiz hepatosit kalıntısıdır."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Apoptoz Morfolojisinin Kronolojik Evreleri",
                "headers": ["Evre No", "Morfolojik Olay", "Biyokimyasal / Hücresel Karşılığı"],
                "rows": [
                    ["1. Evre", "Hücre Büzüşmesi (Shrinkage)", "İyon/su kaybı, sitoplazmik yoğunlaşma (koyu pembe)"],
                    ["2. Evre", "Kromatin Kondansasyonu", "Nükleer zar altında hilal biçimli kromatin yığılması"],
                    ["3. Evre", "Zar Kabarcıklanması (Blebbing)", "Kaspazların aktin iskeletini kesmesiyle dışa fıtıklaşma"],
                    ["4. Evre", "Apoptotik Cisimciklerin Kopması", "Zarla sarılı sitoplazma ve nükleus parçalarının ayrılması"],
                    ["5. Evre", "Fosfatidilserin Dışa Dönüşü", "Makrofajlar için 'Beni ye' sinyalinin belirmesi"],
                    ["6. Evre", "Sessiz Makrofaj Fagositozu", "İçerik sızmadan yangısız ve iz bırakmadan temizlenme"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Apoptoz Evresi", "Mikroskobik Değişiklik", "Doğru Tanımlama"],
                [
                    [("Hücre Gövdesi", False, ""), ("Büzüşme ve Koyu Eozinofili", True, "Sitoplazma yoğunlaşması"), ("Hücre büzüşmesi (Shrinkage)", False, "")],
                    [("Çekirdek", False, ""), ("Zar Altında Hilal Şeklinde Marjinasyon", True, "Nükleusun kenar görüntüsü"), ("Kromatin kondansasyonu", False, "")],
                    [("Zar Dış Yüzeyi", False, ""), ("Fosfatidilserin Maruziyeti", True, "Dış yaprağa çıkan fosfolipid"), ("Beni Ye (Eat Me) sinyali", False, "")]
                ]
            ),
            make_active_recall(
                "Neden laboratuvarda erken apoptoz geçiren hücreleri saptamak için Anneksin V reaktifi kullanılır?",
                "Çünkü Anneksin V, apoptozda zarın dışına çıkan fosfatidilserine yüksek afiniteyle bağlanarak hücreyi floresan olarak işaretler."
            )
        ]
    })

    # ADIM 50
    slides.append({
        "slideNumber": 50,
        "title": "Kaspaz Biyokimyası: Aspartat Kalıntısından Kesen Proteazlar",
        "subtitle": "Aktif bölgesinde sistein barındıran ve aspartik asit sonrası peptid bağını parçalayan enzim ailesi",
        "badge": "Enzimoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun tüm morfolojik ve hücresel değişimlerini icra eden moleküler makine 'Kaspaz' (Caspase) "
            "enzim ailesidir. Kaspaz ismi rastgele verilmiş bir kısaltma değildir; enzimin çalışma prensibini tanımlar:\n\n"
            "'C' = Aktif bölgesinde bir sistein (cysteine) kalıntısı barındırır.\n"
            "'Aspase' = Hedef proteinleri daima spesifik bir aspartik asit (aspartate) aminoasidinden hemen sonra keser.\n\n"
            "> [SINAV SPOTU] Tüm kaspazlar sağlıklı hücrelerde inaktif öncül formda ('prokaspaz') sentezlenir. "
            "Böylece hücre kendi kendini yanlışlıkla sindirmekten korunur.\n\n"
            "Apoptoz sinyali geldiğinde başlatıcı kaspazlar proteolitik kesimle aktive olur ve infazcı kaspazları tetikleyen "
            "bir domino kaskadı (kaspaz kaskadı) başlatır."
        ),
        "medicalTerms": [
            {"term": "Prokaspaz", "explanation": "İnaktif prodomaine sahip, proteolitik kesimle aktif kaspaza dönüşen öncül enzim formu."},
            {"term": "Sistein-Aspartat Proteaz", "explanation": "Aktif bölgesindeki sisteinle substratın aspartatından sonraki bağı hidrolize eden kaspaz tanımı."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kaspazlar aktif bölgesinde sistein taşır ve proteinleri aspartik asit kalıntısından sonra parçalar.",
            "📌 [SINAV SPOTU] Hücrede inaktif prokaspaz formunda bulunurlar; proteolitik kesimle aktive olurlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Etimolojik Prensip", "desc": "Sistein bağımlı, aspartat spesifik proteolitik aktivite.", "isKey": True},
                {"title": "Proenzim Güvenliği", "desc": "İnaktif prokaspaz olarak depolanıp sinyalle kesilme.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Apoptozda hücresel proteinleri parçalayarak hücresel ölümü yöneten kaspaz (caspase) enzim ailesinin temel biyokimyasal çalışma özelliği nedir?",
                {
                    "A": "Aktif bölgesinde serin taşır ve tirozin sonrası keser",
                    "B": "Aktif bölgesinde sistein taşır ve aspartik asit sonrası keser",
                    "C": "Çinko bağımlı metalloproteinazdır ve lösin sonrası keser",
                    "D": "Aktif bölgesinde lizin taşır ve glutamat sonrası keser",
                    "E": "Magnezyum bağımlı kinazdır ve treonini fosforiller"
                },
                "B",
                {
                    "A": "Serin proteazlar (tripsin vb.) farklıdır.",
                    "B": "Doğru cevap B'dir: Kaspaz = Cysteine-dependent Aspartate-directed protease.",
                    "C": "MMP'ler ekstraselüler matrisi yıkar.",
                    "D": "Kaspaz mekanizması değildir.",
                    "E": "Kaspaz bir kinaz değil proteazdır."
                }
            ),
            make_cloze(
                "Kaspazlar aktif bölgelerinde sistein taşır ve hedef hücresel proteinleri aspartik asit kalıntısından sonra parçalar.",
                "aspartik asit",
                "Kaspaz enzimlerinin proteini kestikleri hedef aminoasit"
            )
        ]
    })

    return slides
