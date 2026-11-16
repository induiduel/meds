# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 4: Çevresel Hastalıklar, İklim Değişikliği ve Hava Kirliliği (Slayt 31-40)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_4_slides():
    slides = []

    # Slayt 31: Çevresel Hastalık Kavramı ve Kişisel vs Genel Çevre
    slides.append({
        "id": "k1-26-s31",
        "title": "Çevresel Hastalık Kavramı ve Kişisel vs Genel Çevre",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 31,
        "narrative": (
            "Çevresel hastalık, bireyin yaşadığı veya çalıştığı ortamdaki kimyasal, fiziksel veya biyolojik ajanlara "
            "maruz kalması sonucu gelişen patolojik durumların tamamını tanımlar: "
            "1. **Genel (Dış) Çevre:** Bireyin doğrudan kontrol edemediği, solunan açık hava, içme suyu, tarım toprakları, "
            "sanayi emisyonları ve küresel iklim değişiklikleridir. Toplumun tamamını etkiler. "
            "2. **Kişisel (Bireysel) Çevre:** Bireyin kendi kontrolünde olan veya doğrudan temas ettiği yaşam tarzı seçimleridir: "
            "- Tütün ve sigara kullanımı, alkol tüketimi. "
            "- Diyet ve beslenme alışkanlıkları, kalori dengesi. "
            "- Reçeteli ilaçlar veya kötüye kullanılan yasa dışı maddeler. "
            "3. **Hastalık Yükü:** Günümüzde küresel morbidite ve erken ölümlerin en büyük kısmı, genel çevre kirliliği "
            "ile kişisel çevre seçimlerinin (özellikle tütün ve obezite) birleşik sinerjistik etkisinden kaynaklanır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Genel Çevre ve Kişisel Çevre Ayrımı",
                ["Çevre Türü", "Bileşenler ve Maruziyet Kaynakları", "Kontrol Düzeyi"],
                [
                    ["Genel Çevre", "Açık hava partikülleri, ozon, kükürtdioksit, endüstriyel atıklar", "Toplumsal / Kamusal regülasyon gerektirir"],
                    [
                        "Kişisel Çevre",
                        {"text": "Tütün, alkol, aşırı kalori, reçetesiz ilaçlar", "isMasked": True, "hint": "Bireyin kendi yaşam tarzı ve davranışsal seçimleriyle yönettiği risk alanı"},
                        "Bireysel davranış ve yaşam tarzı değişimi"
                    ],
                    ["Mesleki Çevre", "Asbest, silika tozu, kurşun, benzen, pestisitler", "İş sağlığı ve güvenliği koruma donanımları"]
                ]
            ),
            make_active_recall(
                "Tütün kullanımı, alkol tüketimi, diyet alışkanlıkları ve kötüye kullanılan ilaçlar gibi bireyin doğrudan davranışsal kararlarıyla şekillenen çevresel maruziyet alanına ne ad verilir?",
                "Kişisel (bireysel) çevredir.",
                "Dış atmosfer kirliliğinden farklı olarak kişinin kendi yaşam tarzıyla oluşturduğu maruziyet mikroçevresi"
            )
        ]
    })

    # Slayt 32: Sağlık Eşitsizlikleri ve Sosyal Belirleyiciler
    slides.append({
        "id": "k1-26-s32",
        "title": "Sağlık Eşitsizlikleri ve Sosyal Belirleyiciler",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 32,
        "narrative": (
            "Çevresel maruziyet ve hastalık yükü toplum katmanları arasında eşit dağılmaz; sağlık eşitsizlikleri patolojinin sosyal boyutudur: "
            "1. **Biyolojik 'Irk' Efsanesinin Reddi:** "
            "- İnsan Genom Projesi, insan popülasyonları arasındaki genetik varyasyonun keskin sınırlarla 'biyolojik ırklara' "
            "ayrılamayacağını kanıtlamıştır. Genetik varyasyonların %85-90'ı aynı popülasyon içindeki bireyler arasındadır. "
            "- Bu nedenle modern tıpta 'ırk' biyolojik değil, **sosyal ve çevresel bir kategori** olarak ele alınmalıdır. "
            "2. **Sosyal Belirleyiciler ve Maruziyet Adaletsizliği:** "
            "- Düşük sosyoekonomik düzeydeki gruplar sanayi tesislerine, otoyollara ve hava kirliliği yoğun bölgelere daha yakın yaşar. "
            "- Yetersiz konut koşulları, kurşunlu eski borular ve boyalar, kalitesiz gıdaya mahkumiyet ve temiz hava eksikliği "
            "bu gruplarda hipertansiyon, astım, diyabet ve kronik böbrek hastalığı oranlarını katbekat artırır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Modern Tıpta Irk Kavramının Paradigma Değişimi",
                "Eski Biyolojik Determinizm",
                "Hastalık yatkınlıklarının ve yanıtların biyolojik olarak tanımlanmış sabit ırksal genoma bağlı olduğunun varsayılması",
                "Modern Sosyal ve Çevresel Paradigma",
                "Irkın sosyal bir kurgu olduğunun kabulü; eşitsizliklerin hava kirliliği, yoksulluk ve sağlık erişiminden kaynaklandığının gösterilmesi"
            ),
            make_active_recall(
                "Modern genetik bilimi ve İnsan Genom Projesi verileri ışığında, insan hastalıklarındaki farklılıkları açıklamak için 'ırk' kavramının biyolojik bir temeli olmadığı, bunun yerine hangi bağlamda ele alınması gerektiği vurgulanmaktadır?",
                "Sosyal ve çevresel bir kategori olarak ele alınmalıdır.",
                "Eşitsizliklerin genetik şifreden değil, sosyoekonomik maruziyet ve yaşam koşullarından kaynaklanması"
            )
        ]
    })

    # Slayt 33: Küresel İklim Değişikliği ve Sera Gazları
    slides.append({
        "id": "k1-26-s33",
        "title": "Küresel İklim Değişikliği ve Sera Gazları",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 33,
        "narrative": (
            "20. yüzyılın başından itibaren insan kaynaklı fosil yakıt tüketimi, yeryüzünün enerji dengesini kökten değiştirmiştir: "
            "1. **Sera Gazları:** "
            "- Başta **Karbondioksit ($CO_2$)**, metan ($CH_4$), azot oksitler ve troposferik ozon olmak üzere sera gazları "
            "atmosferde ısıyı hapsederek küresel ısınmaya yol açar. "
            "- Atmosferik $CO_2$ konsantrasyonu Sanayi Devrimi öncesindeki 280 ppm düzeyinden günümüzde **420 ppm'in üzerine** "
            "fırlamış olup, küresel sıcaklık artışıyla kusursuz korelasyon gösterir. "
            "2. **Sıcaklık Projeksiyonları:** 2100 yılına kadar küresel ortalama sıcaklıkta **2°C ile 5°C arasında artış** öngörülmektedir. "
            "3. **Tıbbi Önemi:** İklim krizi bir 'çevre koruma' meselesi olmanın ötesinde, 21. yüzyılın **en büyük küresel halk sağlığı ve "
            "patoloji tehdididir**."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Majör Sera Gazları ve İklimsel Etkileri",
                ["Sera Gazı", "Temel İnsan Kaynağı", "Isı Tutma Potansiyeli ve Eğilim"],
                [
                    ["Karbondioksit (CO2)", "Kömür, petrol, gaz yakılması, ormansızlaşma", "En bol sera gazı, atmosferde yüzyıllarca kalıcı"],
                    [
                        "Metan (CH4)",
                        "Hayvancılık, pirinç tarlaları, gaz kaçakları",
                        {"text": "CO2'den yirmi beş kat daha güçlü sera etkisi", "isMasked": True, "hint": "Kısa vadede atmosferik ısınmayı çok hızlı tetikleyen hidrokarbon gazı"}
                    ],
                    ["Azot Oksitler (N2O)", "Tarım gübreleri, endüstriyel süreçler", "Yüksek ısı tutma kapasitesi ve ozon tabakası incelmesi"]
                ]
            ),
            make_cloze(
                "Fosil yakıt tüketimiyle atmosferde biriken ve Sanayi Devrimi'nden bu yana küresel sıcaklık artışını doğrudan yönlendiren temel sera gazı karbondioksit gazıdır.",
                "karbondioksit",
                "Fosil yakıt yanması sonucu atmosfere salınan ve yüzlerce yıl kalan temel sera gazı"
            )
        ]
    })

    # Slayt 34: İklim Krizinin Sağlık Yansımaları
    slides.append({
        "id": "k1-26-s34",
        "title": "İklim Krizinin Sağlık Yansımaları",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 34,
        "narrative": (
            "İklim değişikliği insan fizyolojisini ve hastalık dağılımını çok boyutlu mekanizmalarla bozar: "
            "1. **Aşırı Sıcak Hava Dalgaları:** "
            "- Yaşlılarda, bebeklerde ve kronik kalp hastalarında kardiyovasküler mortaliteyi katlar (akut koroner sendrom, sıcak çarpması). "
            "2. **Aşırı Hava Olayları ve Seller:** "
            "- Altyapı çöküşü ile kanalizasyon sularının içme suyuna karışması sonucu **su ve gıda kaynaklı enfeksiyon salgınları** "
            "(Kolera, *Cryptosporidium*, *Campylobacter*, Leptospiroz) patlar. "
            "3. **Vektör Ekolojisinin Değişmesi:** "
            "- Sıcaklık ve nem artışı sivrisinek ve kene popülasyonlarının yaşam alanlarını kutuplara ve yüksek rakımlara doğru genişletir. "
            "- **Sıtma (Anofel)**, **Dang humması ve Chikungunya (Aedes)**, **Batı Nil Virüsü (Culex)** ve **Lyme hastalığı (Ixodes kenesi)** "
            "daha önce hiç görülmedikleri coğrafyalarda endemik hale gelir. "
            "4. **Tarımsal Kuraklık:** Mahsul kaybı, gıda kıtlığı, çocukluk çağı şiddetli akut malnütrisyonu ve kitlesel göçler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İklim Krizinin Patolojik ve Bulaşıcı Hastalık Tezahürleri",
                ["İklimsel Değişim", "Etkilenen Biyolojik Yolak", "Klinik / Epidemiyolojik Sonuç"],
                [
                    ["Sıcak Hava Dalgaları", "Termoregülasyon çöküşü, dehidratasyon", "Kardiyovasküler arrest, akut böbrek hasarı, sıcak şoku"],
                    ["Sel ve Altyapı Yıkımı", "Fekal-oral patojenlerin sulara karışması", "Kolera, kriptosporidiyoz, basilli dizanteri salgınları"],
                    [
                        "Vektör Coğrafyası Genişlemesi",
                        "Sivrisinek ve kenelerin üreme mevsiminin uzaması",
                        {"text": "Sıtma, Dang humması, Batı Nil ve Lyme hastalığı", "isMasked": True, "hint": "Tropikal vektörlerin ılıman iklim kuşaklarına yayılmasıyla artan enfeksiyonlar"}
                    ],
                    ["Kuraklık ve Tarım Kaybı", "Besin kalori ve protein arzının çökmesi", "Şiddetli akut malnütrisyon, büyüme geriliği, göçler"]
                ]
            ),
            make_micro_quiz(
                "Küresel ısınma sonucu ortalama kış sıcaklıklarının artması ve don olaylarının azalması, aşağıdaki enfeksiyon hastalıklarından hangisinin vektör aracılığıyla daha geniş coğrafi alanlara yayılmasına doğrudan zemin hazırlar?",
                {
                    "A": "Dang humması ve Sıtma (Aedes ve Anofel sivrisinekleri)",
                    "B": "Tüberküloz (Mycobacterium tuberculosis damlacık yayılımı)",
                    "C": "Hepatit B virüsü (parenteral kan yolu)",
                    "D": "Kuduz virüsü (köpek ısırığı)",
                    "E": "Kistik fibrozis (genetik mutasyon)"
                },
                "A",
                {
                    "A": "Doğrudur; sivrisinek vektörlerinin kışı atlatabilmesi ve üreme alanlarının genişlemesi arbovirüs ve sıtma yayılımını hızlandırır.",
                    "B": "Yanlış; tüberküloz kapalı ortam damlacık enfeksiyonudur.",
                    "C": "Yanlış; HBV kan ve cinsel yolla bulaşır.",
                    "D": "Yanlış; kuduz memeli ısırığı ile geçer.",
                    "E": "Yanlış; KF kalıtsal otozomal resesif hastalıktır."
                }
            )
        ]
    })

    # Slayt 35: Açık Hava Kirliliği Ajanları ve Smog
    slides.append({
        "id": "k1-26-s35",
        "title": "Açık Hava Kirliliği Ajanları ve Smog",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 35,
        "narrative": (
            "Açık hava kirliliği, modern endüstriyel kentlerde her yıl milyonlarca erken ölümden sorumlu küresel bir patolojidir: "
            "1. **EPA Kriter Kirleticileri:** ABD Çevre Koruma Ajansı (EPA) tarafından insan sağlığını tehdit eden altı ana hava kirleticisi "
            "tanımlanmıştır: **Kükürtdioksit ($SO_2$)**, **Karbonmonoksit ($CO$)**, **Azotdioksit ($NO_2$)**, **Troposferik Ozon ($O_3$)**, "
            "**Kurşun ($Pb$)** ve **Partikül Madde (PM)**. "
            "2. **Smog (Hava Kirliliği Dumanı):** "
            "- Kelime anlamı 'smoke' (duman) ve 'fog' (sis) sözcüklerinin birleşimidir. "
            "- İki temel tipi vardır: "
            "- **Klasik (Londra Tipi) Smog:** Kömür yanmasından çıkan $SO_2$ ve nemli sisin birleşimiyle oluşan, indirgeyici sülfürlü dumandır. "
            "- **Fotokimyasal (Los Angeles Tipi) Smog:** Otomobil egzoz gazlarındaki azot oksitler ve uçucu organik bileşiklerin (VOC) "
            "güneş ışığındaki ultraviyole (UV) radyasyonla tepkimeye girmesi sonucu oluşan, **ozon ve serbest radikallerce zengin** "
            "kahverengimsi oksitleyici duman tabakasıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "EPA Majör Hava Kirleticileri ve Patolojik Hedefleri",
                ["Kirletici Ajan", "Ana Emisyon Kaynağı", "Hedef Organ ve Patoloji"],
                [
                    ["Kükürtdioksit (SO2)", "Kömürlü termik santraller, ağır sanayi", "Bronkokonstriksiyon, astım alevlenmesi, asit yağmuru"],
                    ["Azotdioksit (NO2)", "Motorlu taşıt egzozları, enerji santralleri", "Hava yolu hiperreaktivitesi, fotokimyasal ozon üretimi"],
                    [
                        "Troposferik Ozon (O3)",
                        "Egzoz gazlarının güneş ışığıyla fotokimyasal reaksiyonu",
                        {"text": "Alveol epitel lipid peroksidasyonu ve serbest radikal hasarı", "isMasked": True, "hint": "Güneşli sıcak günlerde şehir havasında solunum epitelini yakan güçlü oksidan gaz"}
                    ],
                    ["Partikül Madde (PM)", "Dizel egzoz dumanı, inşaat tozu, lastik aşınması", "Derin akciğer inflamasyonu, KOAH, miyokard enfarktüsü"]
                ]
            ),
            make_active_recall(
                "Motorlu taşıt egzozlarından çıkan azot oksitlerin güneş ışığındaki UV radyasyon etkisiyle havadaki oksijenle reaksiyona girmesi sonucu oluşan ve ozon zengini kahverengi duman tabakasına ne ad verilir?",
                "Fotokimyasal smog tabakasıdır (Los Angeles tipi smog).",
                "Otomobil trafiği ve güneşli havalarda ortaya çıkan oksidan duman sisi"
            )
        ]
    })

    # Slayt 36: Ozon Gazı Toksisitesi
    slides.append({
        "id": "k1-26-s36",
        "title": "Ozon Gazı Toksisitesi",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 36,
        "narrative": (
            "Ozon ($O_3$), stratosferde Dünya'yı zararlı UV ışınlarından koruyan koruyucu bir kalkan iken, soluduğumuz "
            "troposferde (yer seviyesinde) ölümcül bir toksik kirleticidir: "
            "1. **Oluşum Kimyası:** Fabrikalardan veya otomobil egzozlarından salınan azot oksitlerin ($NO_x$) ve uçucu hidrokarbonların "
            "güneş ışığı fotonlarıyla parçalanması sonucu açığa çıkan serbest oksijen atomlarının moleküler oksijenle birleşmesiyle oluşur. "
            "Bu nedenle sıcak, rüzgarsız ve güneşli yaz günlerinde öğleden sonra tepe konsantrasyonuna ulaşır. "
            "2. **Hücresel Hasar Mekanizması:** "
            "- Ozon en güçlü kimyasal oksidanlardan biridir. "
            "- Solunduğunda epitel yüzey sıvısındaki lipidlerle reaksiyona girerek **serbest oksijen radikallerini (ROS)** üretir. "
            "- Hücre zarındaki doymamış yağ asitlerini oksitleyerek **lipid peroksidasyonuna** neden olur. "
            "3. **Klinik Patoloji:** "
            "- Üst ve alt solunum yolu epiteli soyulur (deskuamasyon); Tip 1 pnömositler nekroza gider. "
            "- Enflamatuar sitokinler salgılanır, nötrofilik infiltrasyon başlar. "
            "- Sağlıklı bireylerde göğüs sıkışması ve öksürük; astım ve amfizemli hastalarda ise hayatı tehdit eden alevlenmeler gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Troposferik Ozonun Akciğer Hasarı Oluşturma Basamakları",
                [
                    "1. Fotokimyasal Üretim: Egzoz gazlarının güneş ışığıyla reaksiyona girip yer seviyesinde ozon gazı yapması",
                    "2. Epitel Teması: Ozonun respiratuar bronşiyol ve alveol yüzey sıvısıyla temas etmesi",
                    "3. Lipid Peroksidasyonu: Hücre zarı doymamış yağ asitlerinin serbest radikallerce oksitlenip parçalanması",
                    "4. Deskuamasyon ve Nekroz: Epitel hücrelerinin soyulması ve mukozal bariyerin delinmesi",
                    "5. Akut İnflamasyon: Nötrofillerin toplanması, bronkospazm ve astım alevlenmesi"
                ]
            ),
            make_cloze(
                "Yer seviyesinde solunan ozon gazı solunum epitel hücre zarlarındaki yağ asitlerini oksitleyerek lipid peroksidasyonuna ve serbest radikal hasarına yol açar.",
                "lipid peroksidasyonuna",
                "Hücre zarındaki doymamış fosfolipidlerin serbest oksijen radikalleri tarafından parçalanması süreci"
            )
        ]
    })

    # Slayt 37: Partikül Madde (PM) Patolojisi: PM10 vs PM2.5
    slides.append({
        "id": "k1-26-s37",
        "title": "Partikül Madde (PM) Patolojisi: PM10 vs PM2.5",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 37,
        "narrative": (
            "Partikül madde (Particulate Matter - PM), havada asılı duran katı tanecik ve sıvı damlacıkların karmaşık heterojen karışımıdır: "
            "1. **Boyutun Kritik Önemi (Altın Standart İlke):** "
            "- Partikülün vücuttaki kaderini ve yapacağı doku hasarını belirleyen en kritik parametre **aerodinamik çapıdır**. "
            "2. **Kaba Partiküller (PM10 - Çapı <10 µm):** "
            "- Çapı 10 mikrometreye kadar olan partiküllerdir. "
            "- Burun kılları ve laringeal mukus bariyerini aşarak **trakea, ana bronşlar ve büyük bronşiyollere kadar ulaşabilir**. "
            "- Mukosiliyer temizleme sistemiyle yukarı atılmaya çalışılır; kronik öksürük ve bronşite yol açar. "
            "3. **İnce Partiküller (PM2.5 - Çapı <2.5 µm - EN TEHLİKELİ):** "
            "- Dizel egzozu, kömür yanması ve orman yangınlarından kaynaklanan ultra ince partiküllerdir. "
            "- Bronşiyolleri de aşarak doğrudan **terminal alveollere kadar penetre olur**. "
            "- Alveoler makrofajlar tarafından fagositoza uğrar; makrofajlar bunları eritemeyince kronik IL-1 ve TNF-alfa salgılar. "
            "- Daha da kötüsü: PM2.5 partikülleri alveolokapiller membranı aşarak **doğrudan kan dolaşımına geçer**; "
            "sistemik endotel hasarı, pıhtılaşma aktivasyonu ve akut miyokard enfarktüsü tetikler!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Partikül Madde Boyut Sınıflaması ve Patolojisi",
                ["Partikül Sınıfı", "Aerodinamik Çap", "Penetrasyon Derinliği", "Primer Doku Hasarı"],
                [
                    ["Kaba Partikül (PM10)", "<10 mikrometre", "Üst solunum yolları ve bronşlar", "Mukozal irritasyon, kronik bronşit, hava yolu daralması"],
                    [
                        "İnce Partikül (PM2.5)",
                        "<2.5 mikrometre",
                        {"text": "Terminal alveoller ve kılcal damar kan dolaşımı", "isMasked": True, "hint": "Alveolokapiller gaz değişim bariyerini aşarak doğrudan kana karışabilen ultra ince boyut"},
                        "Alveoler makrofaj aktivasyonu, sistemik endotelit, miyokard enfarktüsü"
                    ],
                    ["Ultra İnce Partikül (PM0.1)", "<0.1 mikrometre (Nanopartikül)", "Tüm dokular ve kan-beyin bariyeri", "Serebral vasküler hasar ve sistemik pro-trombotik durum"]
                ]
            ),
            make_micro_quiz(
                "Hava kirliliğinde solunan partiküllerden çapı 2.5 mikrometrenin altında olanların (PM2.5) insan sağlığı açısından PM10'a kıyasla çok daha ölümcül olmasının temel patolojik gerekçesi nedir?",
                {
                    "A": "Terminal alveollere kadar ulaşıp makrofajları aktive edebilmesi ve kılcal damarları aşarak dolaşıma sızabilmesi",
                    "B": "Burun kıllarına takılarak dışarı atılmasının imkansız olması",
                    "C": "Yalnızca göz konjonktivasında irritasyon oluşturabilmesi",
                    "D": "Kandaki eritrositlerin boyutundan yüz kat daha büyük olması",
                    "E": "Mide asidinde çözünerek bağırsak mukozasını delmesi"
                },
                "A",
                {
                    "A": "Doğrudur; PM2.5 alveoler alana kadar iner, gaz bariyerini geçip sistemik dolaşıma karışır ve vasküler tromboz/enfarktüs yapar.",
                    "B": "Yanlış; bu PM10 için de geçerlidir ancak PM2.5 derin dokuya iner.",
                    "C": "Yanlış; akciğer ve damar sistemini hedefler.",
                    "D": "Yanlış; eritrosit 7.5 mikrondur, PM2.5 ondan küçüktür.",
                    "E": "Yanlış; solunum yoluyla girer."
                }
            )
        ]
    })

    # Slayt 38: İç Ortam Hava Kirliliği: Biyokütle Yakıtları ve Radon
    slides.append({
        "id": "k1-26-s38",
        "title": "İç Ortam Hava Kirliliği: Biyokütle Yakıtları ve Radon",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 38,
        "narrative": (
            "İnsanlar zamanlarının yaklaşık %80-90'ını kapalı mekanlarda geçirir; iç ortam hava kalitesi doğrudan hayati risk taşır: "
            "1. **Biyokütle Yakıtları (Biomass Fuels):** "
            "- Gelişmekte olan ülkelerde ve kırsal alanlarda ısınma ve yemek pişirme amacıyla odun, tezek, odun kömürü ve tarımsal atıklar kullanılır. "
            "- Havalandırması yetersiz evlerde açık ocaklarda yakılan biyokütle; yoğun **partikül madde, polisiklik aromatik hidrokarbonlar (PAH) "
            "ve karbonmonoksit ($CO$)** açığa çıkarır. "
            "- Evdeki kadınlar ve küçük çocuklar sürekli duman solur; çocuklarda ölümcül akut alt solunum yolu enfeksiyonları, kadınlarda ise "
            "sigara içmedikleri halde ağır kronik bronşit ve akciğer karsinomu gelişir. "
            "2. **Karbonmonoksit ($CO$):** Renksiz, kokusuz zehir; kış aylarında soba zehirlenmelerinin temel etkenidir. "
            "3. **Radon Gazı:** Topraktaki uranyumun radyoaktif bozunmasıyla oluşan kokusuz radyoaktif gazdır. "
            "- Bodrum katlarından ve temeldeki çatlaklardan ev içine sızar. "
            "- Sigara içmeyenlerde **akciğer kanserinin bir numaralı nedenidir**!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İç Ortam Kirleticileri ve Patolojik Sonuçları",
                ["Kirletici Ajan", "Kapalı Ortamdaki Kaynağı", "Majör Patolojik Komplikasyon"],
                [
                    ["Biyokütle Dumanı (Tezek/Odun)", "Yetersiz bacalı sobalar ve açık ocaklar", "Kadınlarda sigara dışı KOAH, çocukta ölümcül pnömoni"],
                    ["Karbonmonoksit (CO)", "Kusurlu kombi, soba ve şofben gazları", "Karboksihemoglobinemi, serebral hipoksi ve ani ölüm"],
                    [
                        "Radon Gazı",
                        "Toprak ve temeldeki kayaların radyoaktif bozunumu",
                        {"text": "Sigara içmeyen bireylerde akciğer kanseri (bronkojenik karsinom)", "isMasked": True, "hint": "Topraktan binaların bodrum katlarına sızan alfa yayıcı radyoaktif soy gaz"}
                    ],
                    ["Uçucu Organik Bileşikler (VOC)", "Boya, tiner, yapıştırıcılar, yeni mobilyalar", "Mukozal irritasyon, baş ağrısı, hasta bina sendromu"]
                ]
            ),
            make_active_recall(
                "Topraktaki uranyumun doğal bozunması sonucu binaların bodrum katlarına sızan ve sigara içmeyen bireylerde akciğer kanserinin en sık nedeni olan radyoaktif soy gaz hangisidir?",
                "Radon gazıdır.",
                "Alfa parçacıkları yayarak bronş epitelinde DNA çift zincir kırıkları yapan toprak kökenli soy gaz"
            )
        ]
    })

    # Slayt 39: Checkpoint 4
    slides.append({
        "id": "k1-26-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Çevresel Toksikoloji, İklim Değişikliği ve Hava Kirliliği",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 39,
        "narrative": (
            "Dördüncü kontrol noktamızda çevresel maruziyetleri, iklim krizini ve hava kirliliği patolojisini özetliyoruz: "
            "1. **Çevre Ayrımı:** Genel çevre (toplum maruziyeti) vs kişisel çevre (tütün, alkol, beslenme). "
            "2. **Sosyal Belirleyiciler:** Biyolojik ırk kavramı bilimsel değildir; maruziyet ve sağlık eşitsizliği sosyal sınıfla ilişkilidir. "
            "3. **İklim Değişikliği:** CO2 sera gazı artışı (420 ppm); sıcak dalgaları kardiyovasküler ölümleri katlar, vektörler (sıtma, dang, Lyme) yayılır. "
            "4. **Açık Hava Kirleticileri:** SO2, CO, NO2, Ozon ve Partikül Madde. Fotokimyasal smog güneş ışığı + egzozla ozon üretir. "
            "5. **Ozon:** Güçlü oksidan; hücre zarında lipid peroksidasyonu yapar, epitel deskuamasyonu ve astım alevlenmesi oluşturur. "
            "6. **Partikül Boyutu:** PM10 bronşlara iner; PM2.5 alveollere penetre olur, makrofaj fagositozunu aşarak kana karışır ve miyokard enfarktüsü yapar. "
            "7. **İç Ortam Tehditleri:** Biyokütle dumanı kadın ve çocukları vurur; radon gazı sigara içmeyenlerde akciğer kanserinin baş nedenidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s39-1",
                "Hava kirliliğinde solunan partiküllerden hangileri alveollere ve derin solunum yollarına kadar ulaşarak makrofajları aktive eder?",
                "Çapı on mikrometreden küçük ince taneciklerdir.",
                "Hücresel savunmayı aşarak bronşiyol ve alveol tabanına inebilen solunabilir hava kirliliği fraksiyonu",
                "Partikül Madde"
            ),
            make_flashcard(
                "k1-26-fc-s39-2",
                "Otomobil egzoz gazlarının güneş ışığı (UV) etkisiyle reaksiyona girmesi sonucu oluşan ve epitelde serbest radikal hasarı yapan gaz nedir?",
                "Ozon gazıdır (troposferik ozon).",
                "Üç oksijen atomundan oluşan ve fotokimyasal dumanın ana bileşenini oluşturan oksidan",
                "Ozon Toksisitesi"
            ),
            make_flashcard(
                "k1-26-fc-s39-3",
                "Özellikle gelişmekte olan ülkelerde ev içi havalandırmanın yetersiz olduğu ortamlarda odun ve tezek gibi biyokütle yakıtlarının yakılmasıyla oluşan ölümcül iç ortam gazı nedir?",
                "Karbonmonoksit gazıdır (CO).",
                "Hemoglobine oksijenden iki yüz kat yüksek afiniteyle bağlanarak doku hipoksisine yol açan renksiz zehir",
                "Karbonmonoksit"
            )
        ],
        "interactiveElements": [
            make_table(
                "Çevresel Ajanlar ve Doku Hasarı Karşılaştırma Matrisi",
                ["Ajan / Durum", "Primer Maruziyet Alanı", "Hücresel / Moleküler Toksik Mekanizma", "En Ağır Klinik Sonuç"],
                [
                    ["Troposferik Ozon", "Güneşli şehir havası", "Lipid peroksidasyonu ve serbest oksijen radikalleri", "Epitel nekrozu, ağır astım krizi"],
                    ["PM2.5 İnce Partikül", "Dizel egzozu, kömür dumanı", "Alveolokapiller bariyeri aşma, makrofaj aktivasyonu", "Sistemik vaskülit, miyokard enfarktüsü"],
                    [
                        "Radon Gazı",
                        "Bodrum katları, toprak sızıntısı",
                        {"text": "Alfa radyasyonu ile bronş epitel DNA çift zincir kırığı", "isMasked": True, "hint": "Kokusuz radyoaktif gazın solunmasıyla solunum epitelinde mutasyonel hasar"},
                        "Bronkojenik akciğer kanseri"
                    ],
                    ["Sera Gazları (CO2)", "Küresel atmosfer", "Isı tutulumu, küresel sıcaklık ve vektör yayılımı", "Kardiyovasküler arrest, vektörel salgınlar"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi sigara içmeyen bir bireyde ev içi ortam havasından kaynaklanan ve primer bronkojenik akciğer kanseri gelişimine yol açabilen kanıtlanmış karsinojenik ajandır?",
                {
                    "A": "Radon gazı sızıntısı",
                    "B": "Saf su buharı nemi",
                    "C": "Azot gazı (%78 hava fraksiyonu)",
                    "D": "Karbondioksit konsantrasyonu",
                    "E": "Polen tanecikleri"
                },
                "A",
                {
                    "A": "Doğrudur; radon topraktan binalara sızan alfa yayıcı radyoaktif bir soy gazdır ve sigara dışı akciğer kanserinde bir numaradır.",
                    "B": "Yanlış; su buharı nemdir, karsinojen değildir.",
                    "C": "Yanlış; azot inert atmosferik gazdır.",
                    "D": "Yanlış; CO2 sera gazıdır ancak direkt akciğer karsinojeni değildir.",
                    "E": "Yanlış; polen alerjik rinit yapar, kanser yapmaz."
                }
            )
        ]
    })

    # Slayt 40: Çevresel Kirleticiler ve Sistemik Ateroskleroz
    slides.append({
        "id": "k1-26-s40",
        "title": "Çevresel Kirleticiler ve Sistemik Ateroskleroz",
        "section": "Çevresel Toksikoloji ve Hava Kirliliği",
        "slideNumber": 40,
        "narrative": (
            "Hava kirliliğine bağlı ölümlerin sanılanın aksine yarısından fazlası akciğer hastalıklarından değil, "
            "**kardiyovasküler olaylardan (miyokard enfarktüsü, inme)** kaynaklanır: "
            "1. **Akciğerden Damara Enflamasyon Köprüsü:** "
            "- Solunan PM2.5 ve nano partiküller alveol makrofajları tarafından fagositoza uğradığında masif miktarda "
            "pro-inflamatuar sitokin (**IL-1, IL-6, TNF-alfa**) salgılanır. "
            "- Bu sitokinler dolaşıma karışarak karaciğerden **C-reaktif protein (CRP)** ve fibrinojen sentezini tetikler. "
            "2. **Endotel Disfonksiyonu:** "
            "- Dolaşımdaki partiküller ve serbest radikaller arteriyel endotel hücrelerinde nitrik oksit (NO) sentezini bozar. "
            "- Endotel yüzeyinde adezyon molekülleri (VCAM-1, ICAM-1) eksprese edilir; monositler damar duvarına hücum eder. "
            "3. **Plak Kararsızlığı ve Akut Tromboz:** "
            "- Hava kirliliği aterosklerotik plak içindeki inflamasyonu harlayarak fibröz başlığı inceltir (plak rüptürü riski). "
            "- Eşzamanlı olarak trombosit hiperreaktivitesi ve pıhtılaşma kaskadı tetiklenir; plak yırtıldığında saatler içinde "
            "akut trombotik oklüzyon ve **fatal miyokard enfarktüsü** gerçekleşir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Hava Kirliliğinden Akut Miyokard Enfarktüsüne Giden Yol",
                [
                    "1. Partikül Solunumu: PM2.5 partiküllerinin alveol boşluğuna inip makrofajlarca tanınması",
                    "2. Sitokin Fırtınası: Alveol makrofajlarından IL-6 ve TNF-alfa salgılanıp kana karışması",
                    "3. Karaciğer Akut Fazı: Hepatositlerden CRP ve fibrinojen salgılanarak sistemik yangı başlatılması",
                    "4. Koroner Endotel Hasarı: Koroner damar endotelinin NO kaybetmesi ve aterom plağının iltihaplanması",
                    "5. Plak Rüptürü ve Tromboz: Fibröz kılıfın yırtılıp lümenin trombüsle tıkanmasıyla kalp krizi"
                ]
            ),
            make_active_recall(
                "Açık hava kirliliğine (özellikle PM2.5 partiküllerine) kronik maruziyetin insanlarda solunum yolu ölümlerinden bile daha fazla sayıda erken ölüme yol açtığı temel patolojik sistem hangisidir?",
                "Kardiyovasküler sistemdir (ateroskleroz, miyokard enfarktüsü ve inme).",
                "Sistemik endotel disfonksiyonu ve damar içi tromboz ile seyreden dolaşım patolojisi"
            )
        ]
    })

    return slides
