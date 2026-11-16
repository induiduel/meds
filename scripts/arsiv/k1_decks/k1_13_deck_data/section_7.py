# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-13-s61",
        "title": "Sifiliz Üçüncül Evresi: Gom (Gumma) ve Plazma Hücresi İnfiltrasyonu",
        "content": "Treponema pallidum enfeksiyonunun (sifiliz) yıllar sonra ortaya çıkan tersiyer (üçüncül) evresi, kemik, deri, karaciğer ve aortta tahripkar granülomlarla seyreder:\n\n- **Gom (Gumma) Lezyonu:** Lastik kıvamında, merkezinde nekrotik debris içeren granülomatöz nodüllerdir. Nekroz alanında tüberkülozdan farklı olarak hücre konturları hayalet gibi kısmen seçilebilir (koagülatif gom nekrozu).\n- **Histopatolojik İmza (Sınav Spotu):** Gom lezyonunun ve genel sifilitik lezyonların en ayırt edici özelliği, damar çevrelerinde ve granülom kenarında **yoğun, masif Plazma Hücresi infiltrasyonu** ve damar lümenini tıkayan proliferatif **Endarteritis Obliterans** varlığıdır.\n- **Klinik Sonuç:** Aortta vasa vasorumların tıkanması sifilitik aortit, anevrizma ve kapak yetmezliğine yol açar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Tüberküloz Tüberkülü vs Sifiliz Gom Lezyonu",
                "Tüberküloz Tüberkülü",
                "Merkezde amorf kazeöz nekroz, Langhans dev hücreleri ve lenfosit mantosu hakimdir.",
                "Sifiliz Gom (Gumma) Lezyonu",
                "Lastiksi nekroz, endarteritis obliterans ve çevreleyen belirgin plazma hücresi zenginliği hakimdir."
            ),
            make_quiz(
                "Tersiyer sifilizde görülen gom (gumma) lezyonunun histopatolojik incelemesinde granülom çevresinde en baskın ve tanı koydurucu olan mononükleer hücre tipi hangisidir?",
                [
                    {"key": "A", "text": "Plazma hücresi", "explanation": "A seçeneği DOĞRUDUR: Sifiliz lezyonlarının histopatolojik damgası endarteritis obliterans ve zengin plazma hücresi infiltratıdır."},
                    {"key": "B", "text": "Eozinofil", "explanation": "B seçeneği yanlıştır: Alerji ve parazit hücresidir."},
                    {"key": "C", "text": "Nötrofil", "explanation": "C seçeneği yanlıştır: Akut yangı hücresidir."},
                    {"key": "D", "text": "Mast hücresi", "explanation": "D seçeneği yanlıştır: Histamin hücresidir."},
                    {"key": "E", "text": "Bazofil", "explanation": "E seçeneği yanlıştır: Dolaşımdaki granülosittir."}
                ],
                "A"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-13-s62",
        "title": "Kedi Tırmığı Hastalığı: Süpüratif ve Stellat Granülomlar",
        "content": "Kedi tırmığı hastalığı (Cat-scratch disease), pleomorfik bir gram-negatif basil olan **Bartonella henselae** tarafından oluşturulur:\n\n- **Klinik Tablo:** Kedi tırmalamasından 1-3 hafta sonra bölgesel lenf düğümünde (aksiller, servikal) ağrılı lenfadenopati gelişir.\n- **Histopatolojik İmza (Sınav Spotu):**\n  - Lenf düğümünde sınırları düzensiz, kol veya uzantılar veren **yıldız şeklinde (stellat)** granülomlar oluşur.\n  - Granülomun merkezinde amorf nekroz değil, **yoğun parçalanmış nötrofil topluluğu (süpüratif / apseli nekroz)** yer alır!\n  - Bu nötrofilik çekirdeğin çevresini palizat dizilimli epiteloid histiositler sarar; dev hücre nadirdir.\n- **Özel Boyama:** Bakteriler **Warthin-Starry gümüş boyası** ile nekroz odağında siyah kümeler şeklinde gösterilir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kedi Tırmığı Hastalığında Stellat Granülom Evrimi",
                [
                    "1. İnokülasyon: Kedi tırmığı ile Bartonella henselae dermise girer ve drene edici lenf noduna ulaşır.",
                    "2. Nötrofil Akını: Bakteriler lenfoid foliküllerde yoğun nötrofilik mikroapseler tetikler.",
                    "3. Epiteloid Palizat: Makrofajlar apsenin etrafını çevreleyerek yıldızsı (stellat) kollar oluşturan bir duvar örer.",
                    "4. Süpüratif Granülom: Merkezinde püy ve nükleer debris içeren klasik stellat nekrotizan granülom oturur."
                ]
            ),
            make_cloze(
                "Bartonella henselae enfeksiyonunda lenf düğümünde merkezinde nötrofiller içeren yıldız şeklinde stellat granülomlar izlenir.",
                "stellat",
                "Yıldız benzeri granülom morfolojisi"
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-13-s63",
        "title": "Süpüratif Granülomlar: Tularemi ve Lenfogranüloma Venereum",
        "content": "Granülom merkezinde nötrofil ve apseli nekroz bulunması 'süpüratif granülom' (nekrotizan granülomatöz lenfadenit) olarak tanımlanır ve sınırlı sayıda spesifik etkeni düşündürür:\n\n1. **Kedi Tırmığı Hastalığı:** Bartonella henselae (aksiller/servikal lenfadenit).\n2. **Tularemi (Francisella tularensis):** Kemirgen ve av hayvanı teması veya kontamine su/kene ısırığı; şiddetli ağrılı lenfadenit ve merkezinde nötrofilli granülomlar.\n3. **Lenfogranüloma Venereum (LGV):** Chlamydia trachomatis (L1, L2, L3 serovarları); inguinal lenf düğümlerinde birbirine açılan kanallar ve stellat apseli granülomlar oluşturan cinsel yolla bulaşan enfeksiyon.\n4. **Yersiniyoz (Yersinia pseudotuberculosis):** Mezenterik lenfadenit tablosunda süpüratif granülomlar oluşturarak akut apandisiti taklit eder.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hastalık Adı", "Etken Mikroorganizma", "Karakteristik Histopatoloji"],
                [
                    [
                        {"text": "Kedi Tırmığı Hastalığı", "isMasked": False, "hint": ""},
                        {"text": "Bartonella henselae", "isMasked": True, "hint": "Kedi tırmığı etkeni gram-negatif basil"},
                        {"text": "Yıldızsı (stellat) süpüratif nekrotizan granülom", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Lenfogranüloma Venereum", "isMasked": True, "hint": "Cinsel yolla bulaşan klamidya hastalığı"},
                        {"text": "Chlamydia trachomatis (L1-L3)", "isMasked": False, "hint": ""},
                        {"text": "İnguinal lenf nodunda oluklaşan stellat apseli granülom", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Tularemi", "isMasked": False, "hint": ""},
                        {"text": "Francisella tularensis", "isMasked": False, "hint": ""},
                        {"text": "Ağrılı lenf nodunda santral nötrofilli granülom", "isMasked": True, "hint": "Apseli nekrotizan lenf nodu lezyonu"}
                    ]
                ]
            ),
            make_recall(
                "Granülom merkezinde kazeöz nekroz yerine parçalanmış nötrofil kümeleri ve püy içeren granülom tipine genel olarak ne ad verilir?",
                "Süpüratif (apseli) granülomdur.",
                "Nötrofil içeren granülom tipi"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-13-s64",
        "title": "Yabancı Cisim Granülomları: Non-İmmün İzolasyon",
        "content": "Yabancı cisim granülomları, mikroorganizma veya T hücresi aracılı immün yanıt olmaksızın gelişen saf **fiziksel reaksiyonlardır**:\n\n- **Tetikleyici Materyaller:**\n  - Eksojen: Cerrahi dikiş iplikleri (ipek, katgüt, naylon), talk pudrası (cerrahi eldiven veya IV ilaç bağımlılığı), dövme pigmentleri, cam veya ahşap parçaları.\n  - Endojen: Rüptüre epidermoid kistten dokuya sızan keratin pulları, eklemde biriken ürat kristalleri.\n- **Histopatoloji:**\n  - Lezyonun merkezinde yabancı cisim yer alır.\n  - Etrafını saran yabancı cisim tipi dev hücreler ve epiteloid makrofajlar bulunur.\n  - T-hücre aracılı sitokin patlaması olmadığı için lezyonda **kazeöz nekroz görülmez** ve lenfosit mantosu tüberküloz kadar belirgin değildir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İmmün Granülom (Tüberküloz) vs Yabancı Cisim Granülomu",
                "İmmün Granülom (Tüberküloz)",
                "CD4+ Th1 hücreleri ve IFN-gama ile yönetilir; kazeifikasyon nekrozu ve Langhans dev hücreleri sıktır.",
                "Yabancı Cisim Granülomu",
                "T hücresi ve sitokin yanıtı zayıftır; nekroz yoktur; ortada yabancı partikül ve kaotik dev hücreler bulunur."
            ),
            make_cloze(
                "Cerrahi dikiş ipliği veya talk gibi inert maddelerin etrafında oluşan granülomlara yabancı cisim granülomu adı verilir.",
                "yabancı cisim granülomu",
                "Non-immün fiziksel granülom tipi"
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-13-s65",
        "title": "Polarize Işık Mikroskopisi ve Çift Kırıcılık (Birefringens)",
        "content": "Biyopsi kesitinde yabancı cisim granülomundan şüphelenildiğinde patoloğun başvurduğu en güçlü fiziksel tanı aracı **polarize ışık mikroskobudur**:\n\n- **Birefringens (Çift Kırıcılık) Nedir?** Kristalize veya lifli asimetrik yapıların ışığı iki farklı yönde kırarak polarize filtreler altında karanlık zeminde **parlak, beyaz veya renkli olarak parıldamasıdır**.\n- **Çift Kırıcı Materyaller (Sınav Spotu):**\n  - **Talk Pudrası:** IV ilaç bağımlılarının akciğerinde dev hücreler içinde yıldız şeklinde parlak kristaller.\n  - **Cerrahi Sütür Lifleri:** Dev hücrelerin ortasında parlak lif demetleri.\n  - **Silika Partikülleri:** Silikozis nodüllerinde parıldayan mineral parçacıkları.\n- **Çift Kırıcı Olmayan Yabancı Cisimler:** Ahşap kıymıklar ve bazı sentetik plastikler polarize ışıkta parlamayabilir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "İntravenöz madde bağımlılığı olan 34 yaşındaki hastanın akciğer biyopsisinde perivasküler alanda çok çekirdekli dev hücreler içeren granülomatöz odaklar saptanıyor.",
                "Dev hücrelerin sitoplazmasında talk kristallerini tespit etmek ve yabancı cisim granülomu tanısını doğrulamak için mikroskopta hangi inceleme yöntemi kullanılmalıdır?",
                [
                    {
                        "text": "Polarize ışık mikroskopisi ile çift kırıcılık (birefringens) incelenmelidir.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Talk partikülleri polarize filtreler altında karanlık zeminde parlak kristaller olarak çift kırıcılık gösterir."
                    },
                    {
                        "text": "Yalnızca Ehrlich-Ziehl-Neelsen asit boyası yapılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: EZN mikobakterileri boyar, mineral talk kristallerini göstermez."
                    },
                    {
                        "text": "Gram boyası ile bakteri aranmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Tablo bakteriyel değil kristal yabancı cisim reaksiyonudur."
                    }
                ]
            ),
            make_recall(
                "Kristal veya lifli yabancı partiküllerin polarize ışık mikroskobunda karanlık fonda parlak ışık demeti olarak parlaması optik özelliğine ne ad verilir?",
                "Çift kırıcılıktır (birefringens).",
                "Polarize ışıkta parıldama özelliği"
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-13-s66",
        "title": "Berilyozis: Sarkoidozu Taklit Eden Metal Granülomu",
        "content": "Berilyozis, havacılık, nükleer sanayi, seramik ve floresan lamba endüstrisinde çalışan işçilerin berilyum tozu ve buharı solumasıyla gelişen mesleki bir akciğer hastalığıdır:\n\n- **İmmünolojik Mekanizma:** Sıradan bir toksik reaksiyon değildir; berilyum bir **hapten** gibi davranarak konak HLA-DP proteinlerine bağlanır ve gecikmiş tip (Tip IV) aşırı duyarlık uyarır.\n- **Histopatoloji (Sınav Spotu):** Akciğer ve hiler lenf düğümlerinde **sarkoidoz ile tamamen aynı görünen non-kazeöz granülomlar** oluşturur!\n- **Ayırıcı Tanı:** Bir hastada sarkoidoz benzeri non-kazeöz granülom görüldüğünde mutlaka berilyum maruziyeti sorgulanmalı; kanda Berilyum Lenfosit Proliferasyon Testi (BeLPT) pozitifliği ile ayırt edilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sarkoidoz vs Kronik Berilyozis",
                "Sarkoidoz",
                "Etiyolojisi bilinmez; sistemik non-kazeöz granülomlar; berilyum maruziyeti yoktur.",
                "Kronik Berilyozis",
                "Havacılık/elektronik sanayinde berilyum buharı solunması; histolojik olarak sarkoidozla özdeştir."
            ),
            make_cloze(
                "Berilyum buharı solunması sonucu gelişen berilyozis hastalığı histopatolojik olarak sarkoidoz ile tamamen aynı görünen non-kazeöz granülomlar oluşturur.",
                "sarkoidoz",
                "Berilyozisin histolojik olarak taklit ettiği hastalık"
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-13-s67",
        "title": "Paraziter Granülomlar: Şistozomiyazis ve Eozinofilik Yanıt",
        "content": "Bazı helmintik parazitlerin dokularda takılıp kalan yumurtaları son derece güçlü bir granülomatöz reaksiyon tetikler:\n\n- **Schistosoma mansoni ve japonicum:** Karaciğer portal venüllerine göç eden parazit yumurtaları portal alanlarda takılır.\n- **Histopatolojik Özellik (Sınav Spotu):**\n  - Parazit yumurtasının sert kitin kabuğunun etrafını saran epiteloid histiositler ve dev hücreler.\n  - Bu granülomun manto tabakasında ve çevresinde tüberkülozdan farklı olarak **olağanüstü zengin Eozinofil lökosit infiltrasyonu** bulunur!\n- **Klinik Sonuç:** Milyonlarca yumurta çevresinde gelişen fibrozis, karaciğer parankimini bozmadan portal damarları sıkar (**Symmers'in pipo sapı fibrozisi / pipe-stem fibrosis**); presinüzoidal portal hipertansiyon ve ölümcül özofagus varis kanamaları yapar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Şistozomal Portal Fibrozis Gelişim Basamakları",
                [
                    "1. Yumurta Çöküşü: Schistosoma yumurtaları kan akımıyla karaciğer presinüzoidal portal venlerine oturur.",
                    "2. Eozinofilik Granülom: Yumurta antijenleri Th2 yanıtı tetikler; etrafta bol eozinofilli granülomlar oluşur.",
                    "3. Pipo Sapı Fibrozisi: Yoğun kollajen birikimi portal traktusları beyaz pipo sapları gibi kalınlaştırır.",
                    "4. Portal Hipertansiyon: Parankim sağlamken portal kan akımı tıkanır; masif splenomegali ve varisler açılır."
                ]
            ),
            make_quiz(
                "Karaciğer portal alanlarında parazit yumurtaları etrafında gelişen ve eozinofillerden çok zengin granülomlarla seyreden 'pipo sapı' fibrozis tablosuna yol açan helmint hangisidir?",
                [
                    {"key": "A", "text": "Schistosoma mansoni", "explanation": "A seçeneği DOĞRUDUR: Schistosoma yumurtaları portal fibrozis ve eozinofilik granülomların klasik etkenidir."},
                    {"key": "B", "text": "Enterobius vermicularis", "explanation": "B seçeneği yanlıştır: Kıl kurdu perianal kaşıntı yapar, portal granülom yapmaz."},
                    {"key": "C", "text": "Taenia saginata", "explanation": "C seçeneği yanlıştır: İntestinal sestoddur."},
                    {"key": "D", "text": "Ascaris lumbricoides", "explanation": "D seçeneği yanlıştır: Bağırsak lümeninde yaşar."},
                    {"key": "E", "text": "Giardia lamblia", "explanation": "E seçeneği yanlıştır: Duodenum kamçılı protozoonudur."}
                ],
                "A"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-13-s68",
        "title": "Granülomatöz Vaskülitler: Dev Hücreli Arterit ve Takayasu",
        "content": "Granülomatöz enflamasyon yalnızca organ parankiminde değil, arter duvarlarının bizzat kendisinde de gelişebilir:\n\n1. **Dev Hücreli (Temporal) Arterit:**\n   - 50 yaş üstü bireylerde en sık görülen sistemik vaskülittir; kranial dalları (özellikle arteria temporalis) tutar.\n   - **Morfoloji (Sınav Spotu):** Arter duvarında (tunica media) lamina elastica internanın parçalanmasıyla giden **granülomatöz enflamasyon ve çok çekirdekli dev hücreler**.\n   - Tedavi edilmezse oftalmik arter tıkanıklığına bağlı **ani körlük** yapar!\n2. **Takayasu Arteriti (Nabızsızlık Hastalığı):**\n   - Genç kadınlarda aort kökü ve majör dallarını (subklaviyan, karotis) tutan transmural fibröz skar ve granülomatöz arterittir; üst ekstremitede nabız alınamaz.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Temporal Arterit vs Takayasu Arteriti",
                "Dev Hücreli (Temporal) Arterit",
                ">50 yaş, temporal ve oftalmik arter tutulumu; baş ağrısı, ani görme kaybı ve yüksek ESR.",
                "Takayasu Arteriti",
                "<40 yaş kadınlar, aort kavsi ve subklaviyan arter tutulumu; kollarda nabızsızlık ve klaudikasyon."
            ),
            make_cloze(
                "Dev hücreli arteritte temporal arter duvarındaki lamina elastica interna parçalanır ve tunica mediada granülomatöz dev hücreler izlenir.",
                "lamina elastica interna",
                "Damar duvarında elastik liflerin oluşturduğu iç sınır membranı"
            )
        ]
    })

    # Slide 69
    slides.append({
        "id": "k1-13-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Özel Granülomatöz Hastalıklar, Vaskülitler ve Yabancı Cisimler",
        "content": "Bu kontrol noktasında kazeöz olmayan özel granülom tiplerini, etkenlerini ve tanısal patolojilerini özetliyoruz:\n\n- **Sifiliz (Gumma):** Lastiksi nekroz, belirgin plazma hücresi zenginliği ve endarteritis obliterans.\n- **Kedi Tırmığı (Bartonella):** Yıldızsı (stellat) süpüratif nekrotizan granülom, merkezde nötrofiller, Warthin-Starry boyası.\n- **Yabancı Cisim Granülomları:** T-hücre bağımsız inert yanıt; polarize ışık mikroskobunda parlayan talk/sütür partikülleri (birefringens).\n- **Berilyozis:** Sarkoidozu histopatolojik olarak birebir taklit eden mesleki metal granülomu.\n- **Şistozomiyazis:** Parazit yumurtaları çevresinde eozinofilden zengin granülomlar ve pipo sapı fibrozisi.\n- **Granülomatöz Vaskülitler:** Temporal arterit (yaşlılarda kranial tutulum, körlük riski) ve Takayasu arteriti (genç kadında aort tutulumu, nabızsızlık).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Genç bir kadında sol kolda nabız alınamaması, tansiyon farkı ve aort kavsinde transmural granülomatöz inflamasyon izlenmesi hangi vaskülit tanısını koydurur?",
                [
                    {"key": "A", "text": "Takayasu arteriti", "explanation": "A seçeneği DOĞRUDUR: Genç kadınlarda aort dallarını tutarak nabızsızlığa yol açan dev hücreli granülomatöz arterittir."},
                    {"key": "B", "text": "Poliarteritis nodoza", "explanation": "B seçeneği yanlıştır: Orta çaplı damarlarda granülomsuz transmural nekrotizan vaskülittir."},
                    {"key": "C", "text": "Kawasaki hastalığı", "explanation": "C seçeneği yanlıştır: Çocuklarda koroner arter anevrizması yapan vaskülittir."},
                    {"key": "D", "text": "Mikroskopik polianjiyit", "explanation": "D seçeneği yanlıştır: Küçük damarları tutan granülomsuz lökositoklastik vaskülittir."},
                    {"key": "E", "text": "Henoch-Schönlein purpurası", "explanation": "E seçeneği yanlıştır: IgA birikimli kutanöz vaskülittir."}
                ],
                "A"
            ),
            make_cloze(
                "Yabancı cisim granülomlarında dikiş iplikleri ve talk kristalleri polarize ışık mikroskobunda çift kırıcılık göstererek parlak ışık saçarlar.",
                "çift kırıcılık",
                "Birefringens optik kırma terimi"
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-13-s70",
        "title": "Nekrotizan Granülomatöz Vaskülit: Granülomatöz Polianjiyit (Wegener)",
        "content": "Granülomatöz Polianjiyit (GPA - eski adıyla Wegener Granülomatozu), üst-alt solunum yollarını ve böbrekleri hedef alan ölümcül bir sistemik vaskülittir:\n\n- **Klinik Triad:**\n  1. Üst solunum yolu nekrotizan granülomları (kronik sinüzit, nazal septum perforasyonu / semer burun).\n  2. Akciğerde kavitasyon oluşturan nekrotizan granülomlar (tüberkülozla çok karışır!).\n  3. Böbrekte fokal nekrotizan kresentik glomerülonefrit.\n- **Laboratuvar İşareti (Sınav Spotu):** Nötrofil sitoplazmasındaki proteinaz-3 (PR3) enzimine karşı gelişen **c-ANCA (sitoplazmik antinötrofil sitoplazmik antikor)** hastaların %95'inde pozitiftir.\n- **Patoloji:** Küçük ve orta çaplı damarlarda transmural nekrotizan vaskülit ve damar çevresinde coğrafi nekrozlu granülomlar izlenir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Burun kanaması, semer burun deformitesi, akciğerde kavitasyonlu nodülleri ve idrarda hematürisi olan 45 yaşındaki hastanın serumunda c-ANCA (anti-PR3) antikoru yüksek titrede pozitif bulunuyor.",
                "Solunum yollarında kavitasyonlu nekrotizan granülomlar ve küçük damar vaskülitiyle seyreden bu otoimmün tablo nedir?",
                [
                    {
                        "text": "Granülomatöz Polianjiyittir (Wegener Granülomatozu).",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Üst/alt solunum granülomları, kresentik GN ve c-ANCA pozitifliği Granülomatöz Polianjiyitin kesin triyadıdır."
                    },
                    {
                        "text": "Akciğer Tüberkülozudur.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Tüberküloz kavite yapar ancak c-ANCA pozitifliği ve semer burun kıkırdak lizisi yapmaz."
                    },
                    {
                        "text": "Basit sinüzittir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Sistemik vaskülit ve glomerülonefrit basit enfeksiyonla açıklanamaz."
                    }
                ]
            ),
            make_recall(
                "Granülomatöz polianjiyitte (Wegener) nötrofillerin sitoplazmasındaki proteinaz-3 enzimine karşı oluşan otoantikor belirteci nedir?",
                "c-ANCA'dır (Sitoplazmik Antinötrofil Sitoplazmik Antikor / PR3-ANCA).",
                "Wegener'in klasik laboratuvar serolojik antikor belirteci"
            )
        ]
    })

    return slides
