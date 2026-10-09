# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-13-s51",
        "title": "Kazeöz vs Non-Kazeöz Granülomların Ayırıcı Patolojisi",
        "content": "Granülomatöz hastalıkların patolojik sınıflandırmasında ilk ve en kritik basamak lezyonun merkezinde **kazeöz (kazeifikasyon) nekrozunun** bulunup bulunmadığıdır:\n\n1. **Kazeöz (Nekrotizan) Granülomlar:**\n   - Merkezde hücre sınırlarının ve nükleusların tamamen eridiği, peynirimsi nekrotik bir kitle bulunur.\n   - Tipik Nedenler: **Tüberküloz** (en sık), bazı derin mantar enfeksiyonları (Histoplazmoz, Koksidioidomikoz), nadiren Tularemi.\n2. **Non-Kazeöz (Nekrotizan Olmayan) Granülomlar:**\n   - Granülomun merkezinde asellüler bir nekroz alanı yoktur; merkez tamamen sıkı paketlenmiş canlı epiteloid hücrelerle doludur.\n   - Tipik Nedenler: **Sarkoidoz**, **Crohn hastalığı**, berilyozis ve yabancı cisim granülomları.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kazeöz vs Non-Kazeöz Granülom Karşılaştırması",
                "Kazeöz Granülom (Ör. Tüberküloz)",
                "Merkezde amorf granüler eozinofilik peynirimsi nekroz mevcuttur; Langhans dev hücreleri sıktır.",
                "Non-Kazeöz Granülom (Ör. Sarkoidoz, Crohn)",
                "Merkezde nekroz kesinlikle yoktur; tamamen canlı epiteloid histiositlerle doludur."
            ),
            make_quiz(
                "Aşağıdaki granülomatöz hastalıklardan hangisinin karakteristik histopatolojik bulgusu merkezinde kazeifikasyon nekrozu İÇERMEYEN (non-kazeöz) 'çıplak' granülomlardır?",
                [
                    {"key": "A", "text": "Sarkoidoz", "explanation": "A seçeneği DOĞRUDUR: Sarkoidoz kural olarak nekrozsuz (non-kazeöz) çıplak granülomlarla seyreder."},
                    {"key": "B", "text": "Mycobacterium tuberculosis enfeksiyonu", "explanation": "B seçeneği yanlıştır: Tipik kazeöz nekrotizan granülom etkenidir."},
                    {"key": "C", "text": "Histoplazmoz", "explanation": "C seçeneği yanlıştır: Merkezinde kazeöz nekroz sık görülür."},
                    {"key": "D", "text": "Koksidioidomikoz", "explanation": "D seçeneği yanlıştır: Nekrotizan granülom yapar."},
                    {"key": "E", "text": "Tersiyer Sifiliz gom lezyonu", "explanation": "E seçeneği yanlıştır: Gom merkezinde nekroz barındırır."}
                ],
                "A"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-13-s52",
        "title": "Kazeifikasyon Nekrozu Morfolojisi: Peynirimsi Yapı",
        "content": "Kazeifikasyon nekrozu, koagülasyon ve likefaksiyon nekrozunun özel bir kombinasyonudur:\n\n- **Makroskobik Görünüm:** Organ kesitinde beyaz-sarımsı, ufalanabilir, yumuşak, tulum peynirine benzeyen peynirimsi (cheesy) bir materyal şeklinde görülür ('kazeöz' Latince peynir demektir).\n- **Mikroskobik Görünüm (Sınav Spotu):**\n  - Standart H&E boyasında hücre sınırları ve çekirdekler tamamen kaybolmuştur.\n  - Yerinde yapısal konturu seçilemeyen, **homojen, amorf, granüler ve parlak eozinofilik (pembe)** bir hücresel enkaz izlenir.\n  - Bu amorf alanın çevresini epiteloid histiosit çemberi ve Langhans tipi dev hücreler çevreler.\n- **Oluşum Nedeni:** Mikobakteri hücre duvarındaki lipidlerin (kord faktörü) ve konak T-hücre kaynaklı aşırı TNF/IFN-γ toksisitesinin birleşimidir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Kazeifikasyon nekrozunun mikroskopik incelemesinde hücre konturları tamamen silinmiş olup homojen amorf granüler eozinofilik materyal izlenir.",
                "amorf granüler eozinofilik",
                "Nekroz alanının mikroskobik pembe görünüm tanımı"
            ),
            make_recall(
                "Makroskopik olarak peynirimsi sarı-beyaz ufalanan kitle, mikroskopik olarak amorf eozinofilik granüler artık içeren nekroz tipine ne ad verilir?",
                "Kazeifikasyon nekrozudur (kazeöz nekroz).",
                "Tüberkülozun karakteristik peynirimsi nekrozu"
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-13-s53",
        "title": "Tüberküloz Granülomu (Tüberkül), Ghon Odağı ve Kavite",
        "content": "Tüberküloz, granülomatöz enflamasyonun tıp tarihindeki en klasik prototipidir:\n\n- **Tüberkül:** Kazeöz nekroz merkezli, epiteloid histiosit ve Langhans dev hücresi içeren tüberküloz granülomuna verilen özel addır.\n- **Primer Tüberküloz (Ghon Kompleksi):**\n  - Basili ilk kez soluyan bireyde akciğerin alt lob üst kısmı veya üst lob alt kısmında subplevral kazeöz odak oluşur (**Ghon Odağı**).\n  - Basiller hiler lenf düğümüne yayılır; Ghon odağı + hiler lenfadenopati = **Ghon Kompleksi**.\n  - Zamanla kalsifiye olup skarlaşırsa **Ranke Kompleksi** adını alır.\n- **Sekonder (Reaktivasyon) Tüberküloz:** Bağışıklık düştüğünde akciğer apeksinde granülomlar patlar; nekrotik materyal bronşa dökülerek **kavite (boşluk)** oluşturur. Hasta basili dışarı öksürür (bulaşıcı evre).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Primer Tüberkülozdan Sekonder Kavitasyona Evreler",
                [
                    "1. Ghon Odağı: Akciğer parankiminde kazeöz nekrozlu primer granülom odağı gelişir.",
                    "2. Hiler Yayılım: Basiller lenfatikle drene olup hiler lenf nodunda kazeifikasyon yapar (Ghon Kompleksi).",
                    "3. Fibrokalsifik Skar: Lezyon kalsifiye olarak sessizleşir ve Ranke kompleksine dönüşür.",
                    "4. Reaktivasyon ve Kavite: İmmünite düşünce apeks granülomları bronşa açılarak kavernöz kavite açar."
                ]
            ),
            make_quiz(
                "Akciğer parankimindeki kazeifiye subplevral tüberküloz odağı ile aynı taraf hiler lenf düğümü kazeifikasyonunun oluşturduğu anatomik lezyon kompleksine ne ad verilir?",
                [
                    {"key": "A", "text": "Ghon kompleksi", "explanation": "A seçeneği DOĞRUDUR: Subplevral odak + hiler lenfadenit = Ghon kompleksidir."},
                    {"key": "B", "text": "Ranke kompleksi", "explanation": "B seçeneği yanlıştır: Ghon kompleksinin kalsifiye olmuş radyolojik izidir."},
                    {"key": "C", "text": "Aschoff nodülü", "explanation": "C seçeneği yanlıştır: Akut romatizmal kardit odağıdır."},
                    {"key": "D", "text": "Schaumann cisimciği", "explanation": "D seçeneği yanlıştır: Sarkoidozdaki inklüzyondur."},
                    {"key": "E", "text": "Munro mikroapsesi", "explanation": "E seçeneği yanlıştır: Psöriyazisteki nötrofil odağıdır."}
                ],
                "A"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-13-s54",
        "title": "Tüberküloz Tanısında Mikobakterilerin Gösterilmesi: EZN ve Floresan",
        "content": "Granülomda kazeöz nekroz görmek tüberküloz şüphesini en tepeye taşır ancak kesin tanı için basilin histolojik veya mikrobiyolojik olarak gösterilmesi şarttır:\n\n- **Neden Standart Boyada Görünmez?** Mikobakterilerin hücre duvarı %60 oranında mikolik asit ve kompleks lipidler içerir. Bu mumsu lipid tabakası standart Gram veya H&E boyalarını geçirmez.\n- **Ehrlich-Ziehl-Neelsen (EZN / ARB) Boyaması (Sınav Spotu):**\n  - Karbol fuksin ile ısıtılarak boyanır; ardından asit-alkol karışımıyla yıkandığında rengini kaybetmez (**Aside Dirençli Basil - ARB**).\n  - Mikroskopta mavi arka plan üzerinde ince, uzun, kıvrık **parlak kırmızı/pembe basiller** şeklinde parlar.\n- **Auramin-Rhodamin Floresan Boyası:** Floresan mikroskobunda basiller karanlık zeminde parlak yeşil/sarı parıldar; tarama hızı EZN'ye göre çok daha yüksektir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Standart H&E vs Ziehl-Neelsen (EZN) Boyama",
                "Standart Hematoksilen & Eozin (H&E)",
                "Kazeöz nekroz, epiteloid hücre ve Langhans dev hücrelerini gösterir; basili göstermez.",
                "Ehrlich-Ziehl-Neelsen (EZN)",
                "Mavi zemin üzerinde aside dirençli kırmızı mikobakteri basillerini doğrudan gösterir."
            ),
            make_cloze(
                "Tüberküloz basilleri hücre duvarlarındaki zengin mikolik asit içeriği nedeniyle asit-alkol ile solmaz ve aside dirençli basil olarak adlandırılır.",
                "aside dirençli basil",
                "ARB kısaltmasının açık Türkçe patoloji adı"
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-13-s55",
        "title": "Sarkoidoz Granülomları ve İntraselüler İnklüzyonlar",
        "content": "Sarkoidoz, etiyolojisi tam bilinmeyen, bilateral hiler lenfadenopati ve akciğer tutulumuyla karakterize sistemik bir granülomatöz hastalıktır:\n\n- **Histopatolojik İmza (Sınav Spotu):**\n  - **Non-kazeöz (Nekrozsuz) Granülomlar:** Tüberkülozun aksine granülom merkezinde kazeifikasyon nekrozu ASLA bulunmaz; 'çıplak granülom' (naked granuloma) olarak adlandırılır.\n  - Sıkı paketlenmiş epiteloid hücreler, Langhans dev hücreleri ve seyrek periferik lenfosit kuşağı.\n- **Tanısal Sitoplazmik İnklüzyonlar (Dev Hücre İçinde):**\n  1. **Schaumann Cisimcikleri:** Konsantrik lamine kalsiyum ve protein çökeltileridir.\n  2. **Asteroid Cisimcikleri:** Dev hücre sitoplazmasında yıldız şeklinde uzantıları olan lipid/protein inklüzyonlarıdır.\n- **Önemli Not:** Bu inklüzyonlar sarkoidoza özgül (patognomonik) değildir ancak kuvvetle destekler.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İnklüzyon / Görünüm", "Hücre İçi Lokalizasyon", "Mikroskobik Özelliği"],
                [
                    [
                        {"text": "Schaumann Cisimciği", "isMasked": False, "hint": ""},
                        {"text": "Dev hücre sitoplazması", "isMasked": False, "hint": ""},
                        {"text": "Konsantrik lamine kalsiyum ve protein çöküntüleri", "isMasked": True, "hint": "Kireçli halkasal inklüzyon"}
                    ],
                    [
                        {"text": "Asteroid Cisimciği", "isMasked": True, "hint": "Yıldızsı şekilli inklüzyon"},
                        {"text": "Dev hücre sitoplazması", "isMasked": False, "hint": ""},
                        {"text": "Yıldız şeklinde ışınsal kolları olan eozinofilik yapı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Çıplak Granülom", "isMasked": False, "hint": ""},
                        {"text": "Sarkoidoz lezyonunun geneli", "isMasked": False, "hint": ""},
                        {"text": "Merkezinde nekroz olmayan, seyrek lenfositli nodül", "isMasked": True, "hint": "Non-kazeöz granülomun diğer adı"}
                    ]
                ]
            ),
            make_recall(
                "Sarkoidozlu hastaların dev hücre sitoplazmasında izlenen, kalsiyum ve demir içeren konsantrik tabakalı inklüzyon cisimciğine ne ad verilir?",
                "Schaumann cisimciğidir.",
                "Konsantrik lamine kalsiyum inklüzyonu"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-13-s56",
        "title": "Crohn Hastalığı: Transmural Non-Kazeöz Granülomlar",
        "content": "Crohn hastalığı, ağızdan anüse kadar gastrointestinal kanalın herhangi bir segmentini tutabilen kronik inflamatuar bağırsak hastalığıdır:\n\n- **Histopatolojik Özellikler:**\n  - **Transmural Enflamasyon:** Yangı yalnızca mukoza ile sınırlı kalmaz; submukoza, muskularis ve serozayı aşarak tüm bağırsak duvarını tutar.\n  - **Non-Kazeöz Granülomlar (Sınav Spotu):** Vakaların yaklaşık %50-60'ında bağırsak duvarının tüm katlarında ve mezenterik lenf nodlarında kazeifikasyon nekrozu içermeyen küçük granülomlar saptanır.\n- **Ülseratif Kolit ile Ayrım:** Ülseratif kolitte granülom ASLA görülmez ve yangı yalnızca mukoza-submukoza ile sınırlıdır.\n- **Makroskopi:** Normal mukoza adacıkları ile atlamalı lezyonlar (**skip lesions**) ve kaldırım taşı (**cobblestone**) manzarası izlenir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Crohn Hastalığı vs Ülseratif Kolit Granülom Ayrımı",
                "Crohn Hastalığı",
                "Transmural tutulum, atlamalı lezyonlar ve non-kazeöz granülomlar mevcuttur.",
                "Ülseratif Kolit",
                "Yalnızca mukoza/submukoza tutulumu, rektumdan diffüz yayılım; granülom kesinlikle yoktur."
            ),
            make_quiz(
                "İnflamatuar bağırsak hastalıklarında bağırsak duvarı biyopsisinde 'non-kazeöz granülom' ve 'transmural enflamasyon' görülmesi hangi hastalığı kesinleştirir?",
                [
                    {"key": "A", "text": "Crohn hastalığı", "explanation": "A seçeneği DOĞRUDUR: Non-kazeöz granülom ve transmural yayılım Crohn hastalığının ayırıcı histolojik imzasıdır."},
                    {"key": "B", "text": "Ülseratif kolit", "explanation": "B seçeneği yanlıştır: Ülseratif kolitte granülom bulunmaz."},
                    {"key": "C", "text": "İskemik kolit", "explanation": "C seçeneği yanlıştır: Vasküler oklüzyona bağlı mukozal nekrozdur."},
                    {"key": "D", "text": "Psödomembranöz enterokolit", "explanation": "D seçeneği yanlıştır: C. difficile toksinine bağlı fibrinli membranlardır."},
                    {"key": "E", "text": "Çölyak hastalığı", "explanation": "E seçeneği yanlıştır: Villus atrofisi ve intraepitelyal lenfositozla seyreder."}
                ],
                "A"
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-13-s57",
        "title": "Lepra (Hansen Hastalığı): Tüberküloid vs Lepromatöz Uçurum",
        "content": "Mycobacterium leprae enfeksiyonu, konağın hücresel bağışıklık gücünün granülom morfolojisini nasıl baştan aşağı değiştirdiğini gösteren en dramatik patoloji modelidir:\n\n1. **Tüberküloid Lepra (Yüksek Hücresel İmmünite / Th1 Baskın):**\n   - Konak basile karşı güçlü Th1 ve IFN-γ yanıtı verir.\n   - **Morfoloji:** Sinir lifleri çevresinde iyi organize olmuş, kazeifiye olmayan **belirgin granülomlar** izlenir. Basiller granülom içinde hapsedildiği için dokuda basil sayısı çok azdır (**paucibacillary**).\n   - Dermal sinir hasarı sonucu anesteziye plaklar görülür.\n2. **Lepromatöz Lepra (Çökmüş Hücresel İmmünite / Th2 ve Anerji):**\n   - Konak basili durduramaz; Th1 yanıtı çökmüştür.\n   - **Morfoloji:** Granülom OLUŞTURULAMAZ! Makrofajlar basilleri sindiremeyip içlerinde biriktirir; köpüksü dev histiositlere dönüşürler (**Virchow Hücreleri / Lepra Hücreleri**).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Tüberküloid Lepra", "Lepromatöz Lepra"],
                [
                    [
                        {"text": "Konak İmmün Yanıtı", "isMasked": False, "hint": ""},
                        {"text": "Güçlü Th1 hücresel bağışıklık", "isMasked": False, "hint": ""},
                        {"text": "Çökmüş hücresel immünite (anerji, zayıf Th2)", "isMasked": True, "hint": "Mikroba karşı bağışıklığın iflası"}
                    ],
                    [
                        {"text": "Granülom Varlığı", "isMasked": False, "hint": ""},
                        {"text": "Belirgin, organize epitoloid granülomlar var", "isMasked": True, "hint": "Karantina yapısının varlığı"},
                        {"text": "Granülom yok; köpüksü makrofaj agregatları", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Dokudaki Basil Sayısı", "isMasked": False, "hint": ""},
                        {"text": "Çok az sayıda basil (paucibacillary)", "isMasked": False, "hint": ""},
                        {"text": "Milyonlarca basil içeren Virchow hücreleri", "isMasked": True, "hint": "Basil dolu köpüksü makrofajlar"}
                    ]
                ]
            ),
            make_recall(
                "Leprada güçlü Th1 hücresel yanıtı olan formda iyi organize granülomlar görülürken, hücresel yanıtın çöktüğü lepromatöz formda görülen basil dolu köpüksü makrofajlara ne ad verilir?",
                "Virchow hücreleridir (lepra hücreleri).",
                "Lepromatöz lepranın tanısal köpüksü hücresi"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-13-s58",
        "title": "Lepromatöz Lepra: Virchow Hücreleri ve Fasiyes Leonina",
        "content": "Lepromatöz leprada konak mikroorganizmayı sınırlayamadığı için basiller kontrolsüz şekilde dokularda yayılır:\n\n- **Virchow Hücreleri (Lepra Hücreleri):** Sitoplazması lipid damlacıkları ve milyonlarca Mycobacterium leprae basili içeren dev köpüksü makrofajlardır. Bu basiller Fite-Faraco boyasıyla fagositer sitoplazmada sigara paketi gibi demetler halinde (globi) görülür.\n- **Fasiyes Leonina (Aslan Yüzü):** Dermal köpüksü histiosit infiltrasyonu kaşlarda, kulak memelerinde, burun ve alında derin nodüler kıvrımlar oluşturarak hastaya aslan yüzü görünümü kazandırır.\n- **Grenz Zonu:** Epidermis ile dermisteki bu masif histiosit infiltratı arasında dar bir sağlam kollajen şeridi (**Grenz zonu**) korunur; granülomatöz tüberkülozda ise epidermis sıklıkla ülsere olur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Tüberküloid Lepra Plağı vs Lepromatöz Lepra Nodülleri",
                "Tüberküloid Lepra",
                "Hissiz, hipopigmente, net sınırlı lezyonlar; biyopside sinirleri tahrip eden granülomlar.",
                "Lepromatöz Lepra",
                "Yaygın simetrik nodüller, aslan yüzü görünümü; biyopside basil dolu Virchow hücreleri."
            ),
            make_cloze(
                "Lepromatöz leprada dermisteki masif Virchow hücresi infiltrasyonu ile üstteki epidermis arasında korunan dar kollajen tabakasına Grenz zonu adı verilir.",
                "Grenz zonu",
                "İnfiltrat ile epidermis arasındaki sınır bölgesi"
            )
        ]
    })

    # Slide 59
    slides.append({
        "id": "k1-13-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Kazeöz vs Non-Kazeöz Granülomlar ve Temel Hastalıklar",
        "content": "Bu kontrol noktasında kazeöz ve non-kazeöz granülomatöz patolojileri ve klasik hastalık prototiplerini pekiştiriyoruz:\n\n- **Kazeöz (Nekrotizan):** Tüberküloz (tüberkül, amorf pembe nekroz, EZN ile aside dirençli kırmızı basiller) ve derin mantar enfeksiyonları.\n- **Non-Kazeöz (Nekrozsuz):** Sarkoidoz (çıplak granülom, Schaumann ve Asteroid cisimcikleri) ve Crohn hastalığı (transmural tutulum, atlamalı lezyonlar).\n- **Primer Tüberküloz:** Ghon odağı + hiler lenfadenit = Ghon kompleksi; kalsifiye olunca Ranke kompleksi.\n- **Sekonder Tüberküloz:** Apekste reaktivasyon, kaviteleşme ve bronşa açılma.\n- **Lepra Spektrumu:** Güçlü Th1 yanıtında iyi organize granülomlar (tüberküloid); çökmüş Th1 yanıtında basil dolu köpüksü Virchow hücreleri ve aslan yüzü (lepromatöz).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Bilateral hiler lenfadenopati ve akciğerde non-kazeifiye granülomlar saptanan bir hastanın dev hücre sitoplazmasında konsantrik kalsiyum birikimleri (Schaumann) ve yıldızsı inklüzyonlar (Asteroid) izlenmesi en çok hangi tanıyı destekler?",
                [
                    {"key": "A", "text": "Sarkoidoz", "explanation": "A seçeneği DOĞRUDUR: Bilateral hiler lenfadenopati, non-kazeöz granülomlar ve bu inklüzyonlar sarkoidozun klasik tablosudur."},
                    {"key": "B", "text": "Primer akciğer tüberkülozu", "explanation": "B seçeneği yanlıştır: Kazeifikasyon nekrozu ve EZN pozitifliği beklenir."},
                    {"key": "C", "text": "Silikozis", "explanation": "C seçeneği yanlıştır: Polarize ışıkta parlayan silika kristalleri ve kollajenöz nodüller görülür."},
                    {"key": "D", "text": "Aktinomiçoz", "explanation": "D seçeneği yanlıştır: Sülfür granüllü pürülan apse yapar."},
                    {"key": "E", "text": "Lepromatöz lepra", "explanation": "E seçeneği yanlıştır: Virchow köpüksü hücreleri hakimdir."}
                ],
                "A"
            ),
            make_cloze(
                "Tüberküloz basilleri kazeifikasyon nekrozu zemininde Ehrlich-Ziehl-Neelsen boyası ile boyandığında mavi zeminde parlak kırmızı basiller olarak görülür.",
                "kırmızı",
                "ARB basillerinin EZN boyasındaki rengi"
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-13-s60",
        "title": "Mantar Enfeksiyonlarında Granülomlar ve GMS/PAS Boyaları",
        "content": "Bazı sistemik ve dimorfik mantarlar, tüberkülozla birebir karışan kazeöz nekrotizan granülomlar oluştururlar:\n\n- **Başlıca Mantar Etkenleri:**\n  - **Histoplasma capsulatum:** Kuş ve yarasa gübresi maruziyeti; makrofajlar içinde 2-4 mikronluk küçük tomurcuklanan mayalar.\n  - **Blastomyces dermatitidis:** Geniş tabanlı tomurcuklanan çift konturlu kalın duvarlı iri mayalar.\n  - **Coccidioides immitis:** İçinde çok sayıda endospor barındıran dev sferüller (20-100 mikron).\n- **Özel Mantar Boyaları (Sınav Spotu):** Mantar hücre duvarındaki zengin polisakkaritler standart H&E ile soluk kalır. Kesin tanı için iki özel boya kullanılır:\n  1. **Grocott Metenamin Gümüş (GMS):** Mantar duvarını **kömür siyahı** boyar.\n  2. **Periyodik Asit Schiff (PAS):** Mantar duvarını **parlak macenta kırmızısı** boyar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Akciğer biyopsisinde kazeifiye granülom izlenen ancak EZN boyamasında mikobakteri saptanmayan hastada mantar enfeksiyonu şüphesiyle özel histokimyasal boyama yapılıyor.",
                "Mantar hücre duvarındaki polisakkaritleri seçici olarak gümüşleyip kömür siyahı renge boyayan ve mantar teşhisinde altın standart olan boya hangisidir?",
                [
                    {
                        "text": "Grocott Metenamin Gümüş (GMS) boyasıdır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! GMS mantar duvarını simsiyah boyayarak histoplazma veya koksidioides mayalarını net olarak gösterir."
                    },
                    {
                        "text": "Prusya mavisi boyasıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Prusya mavisi hemosiderin demirini maviye boyar."
                    },
                    {
                        "text": "Kongo kırmızısı boyasıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Kongo kırmızısı amiloid teşhisinde kullanılır."
                    }
                ]
            ),
            make_recall(
                "Mantar hücre duvarındaki kompleks polisakkaritleri parlak macenta/pembe renge boyayan histokimyasal reaksiyon hangisidir?",
                "Periyodik Asit Schiff (PAS) boyasıdır.",
                "Glikojen ve mantar duvarı boyası"
            )
        ]
    })

    return slides
