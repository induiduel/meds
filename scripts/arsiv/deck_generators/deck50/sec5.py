from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec5():
    slides = []

    # Slide 41: Tersiyer Sifiliz Patogenezi ve Hücresel İmmün Yanıt
    slide41_text = """
    ## Tersiyer Sifiliz Patogenezi ve Hücresel İmmün Yanıt

    Tersiyer sifiliz, genellikle primer enfeksiyondan yıllar hatta on yıllar sonra ortaya çıkan, hastalığın ileri ve sıklıkla yıkıcı evresidir. Bu aşamada patogenezi yönlendiren temel faktör, doğrudan artan treponemal yük değil, **hücresel immün yanıtın** aşırı reaksiyonudur.

    Gecikmiş hücresel immünite, spiroket antijenlerine karşı güçlü bir tepki vererek doku hasarına yol açar. Bu süreçte T lenfositleri ve makrofajlar yoğun bir şekilde aktive olur ve dokularda lokalize granülomatöz inflamasyon alanları gelişir.

    > Tersiyer sifilizdeki patolojik lezyonlar, büyük ölçüde organizmanın *T. pallidum* varlığına karşı gösterdiği abartılı hücresel immün yanıtın bir sonucudur, mikroorganizmanın doğrudan doku yıkımından çok konak immünitesi hasardan sorumludur.
    """
    slides.append(make_slide(
        title="Tersiyer Sifiliz Patogenezi ve Hücresel İmmün Yanıt",
        text=slide41_text,
        elements=[
            make_cloze("Tersiyer sifiliz, genellikle primer enfeksiyondan yıllar sonra gelişir ve patogenezin temelinde spiroket yükünden ziyade {{hücresel immün yanıtın}} aşırı reaksiyonu yatar."),
            make_cloze("Doku hasarı, spiroketlere karşı {{gecikmiş}} hücresel immünitenin güçlü tepkisi sonucu gelişir."),
            make_quiz(
                question="Tersiyer sifilizde doku hasarının birincil nedeni aşağıdakilerden hangisidir?",
                options=[
                    "Masif treponemal çoğalma",
                    "Aşırı hücresel immün yanıt",
                    "Dolaşımdaki immün kompleks birikimi",
                    "Doğrudan endotel hücre invazyonu"
                ],
                answer="Aşırı hücresel immün yanıt",
                explanation="Tersiyer evrede doku hasarı, mikroorganizmanın kendisinden ziyade konağın abartılı hücresel immün yanıtına bağlıdır."
            ),
            make_chain([
                "Tersiyer evrede T hücreleri ve makrofajların aktivasyonu...",
                "Güçlü bir gecikmiş hücresel immün yanıta neden olur...",
                "Bunun sonucunda dokularda granülomatöz inflamasyon ve harabiyet gelişir."
            ])
        ]
    ))

    # Slide 42: Gom (Gumma) Tanımı ve Tip IV Aşırı Duyarlılık Mekanizması
    slide42_text = """
    ## Gom (Gumma) Tanımı ve Tip IV Aşırı Duyarlılık Mekanizması

    Tersiyer sifilizin karakteristik lezyonu **gom (gumma)** olarak adlandırılır. Gomlar, dokularda yıkıma neden olan lokalize granülomatöz kitlelerdir ve aslen **Tip IV aşırı duyarlılık** (gecikmiş tip) reaksiyonunun klasik bir örneğidir.

    Makrofajlar ve T lenfositlerin aşırı aktivasyonuyla, az sayıdaki spiroket antijenine karşı şiddetli bir inflamatuvar yanıt verilir. Bu yanıt, fibroblastların da katılımıyla dokuları fibrotik ve nekrotik alanlara dönüştürür.

    > Gom lezyonları, vücudun herhangi bir dokusunda ortaya çıkabilen, klinik olarak destrüktif (yıkıcı) ancak histolojik olarak granülomatöz bir yapı sergileyen, Tip IV immünolojik reaksiyon sahalarıdır.
    """
    slides.append(make_slide(
        title="Gom (Gumma) Tanımı ve Tip IV Aşırı Duyarlılık Mekanizması",
        text=slide42_text,
        elements=[
            make_cloze("Tersiyer sifilizin tipik granülomatöz lezyonuna {{gom}} (gumma) adı verilir."),
            make_cloze("Gom gelişimi immünolojik olarak {{Tip IV}} aşırı duyarlılık (gecikmiş tip) reaksiyonudur."),
            make_quiz(
                question="Gom lezyonlarının temel immünolojik mekanizması aşağıdakilerden hangisidir?",
                options=[
                    "Tip I anafilaktik reaksiyon",
                    "Tip II sitotoksik reaksiyon",
                    "Tip III immün kompleks reaksiyonu",
                    "Tip IV gecikmiş aşırı duyarlılık"
                ],
                answer="Tip IV gecikmiş aşırı duyarlılık",
                explanation="Gomlar, makrofaj ve T hücre aracılı Tip IV aşırı duyarlılık reaksiyonu sonucu oluşur."
            ),
            make_chain([
                "Az sayıda kalan spiroket antijenine karşı...",
                "Tip IV aşırı duyarlılık reaksiyonu tetiklenir...",
                "Lokalize, yıkıcı granülomatöz lezyonlar olan gomlar oluşur."
            ])
        ]
    ))

    # Slide 43: Gom Histopatolojisi: Granülamatöz Nekroz ve Düşük Bakteri Yükü
    slide43_text = """
    ## Gom Histopatolojisi: Granülamatöz Nekroz ve Düşük Bakteri Yükü

    Mikroskobik incelemede bir gom, merkezi koagülatif nekroz alanı ve bu alanı çevreleyen epiteloid makrofajlar, dev hücreler, plazma hücreleri ile lenfositlerden oluşan tipik bir granülomatöz yapı sergiler. Kenarlarda fibrozis belirgindir.

    Gomların en dikkat çekici özelliklerinden biri, içerdikleri spiroket sayısının son derece düşük olmasıdır. Gümüşleme boyaları veya karanlık alan mikroskopisi ile mikroorganizmaları saptamak çok nadiren mümkündür.

    > Histolojik olarak tüberküloz granülomlarına benzeyebilen gomlar, merkezi lastiğimsi nekroz ve çevresel lenfoplazmasitik infiltrasyon ile karakterizedir, ancak bakteri yükü yok denecek kadar azdır.
    """
    slides.append(make_slide(
        title="Gom Histopatolojisi: Granülamatöz Nekroz ve Düşük Bakteri Yükü",
        text=slide43_text,
        elements=[
            make_cloze("Gomların merkezinde {{koagülatif nekroz}}, çevresinde ise epiteloid hücreler ve plazma hücrelerinden zengin infiltrasyon bulunur."),
            make_cloze("Gom lezyonlarında spiroket (bakteri) yükü son derece {{düşüktür}}."),
            make_spot_lie(
                question="Gom histopatolojisi hakkında hangisi yanlıştır (tuzaktır)? Odak: Granülom yapısı",
                lies=[
                    "Gom lezyonlarında Gümüşleme boyası ile bol miktarda spiroket saptanır."
                ],
                truths=[
                    "Merkezi nekroz ve çevresel granülomatöz inflamasyon görülür.",
                    "Makrofajlar ve plazma hücreleri lezyonun hücresel bileşenlerindendir.",
                    "Bakteri yükü çok düşük olduğundan mikroorganizma göstermek zordur."
                ],
                explanation="Gom lezyonları immünolojik hiperreaktivite sonucu oluşur ve içlerindeki *T. pallidum* miktarı çok düşüktür; bol miktarda spiroket saptanmaz.",
                isLie=True
            ),
            make_recall("Gom lezyonlarında spiroketlerin kolayca gösterilmesini bekler miyiz?", "Hayır, bakteri yükü çok düşüktür.")
        ]
    ))

    # Slide 44: Kutanöz Gom Lezyonları: Nodüler Ülsere Cilt Yıkımları
    slide44_text = """
    ## Kutanöz Gom Lezyonları: Nodüler Ülsere Cilt Yıkımları

    Gomlar deride yerleştiğinde, kutanöz (deri) lezyonlar olarak ortaya çıkar. Bunlar genellikle asimetrik, ağrısız, nodüler veya ülseratif yapıdadır. Deri gomları yavaşça büyür ve iyileşirken tipik olarak "at nalı" veya "yay" şeklinde, ortası atrofik skar bırakan lezyonlara dönüşebilir.

    Yüz, saçlı deri, gövde ve ekstremitelerde görülebilirler. Bu lezyonlar sekonder sifilizdeki yaygın döküntülerin aksine lokalize, daha az sayıda ancak daha destrüktiftir ve ciddi doku kaybına yol açarlar.

    > Kutanöz gomlar, derin doku yıkımı ve skar dokusu oluşumu ile sonlanan, derideki lokalize granülomatöz süreçlerdir.
    """
    slides.append(make_slide(
        title="Kutanöz Gom Lezyonları: Nodüler Ülsere Cilt Yıkımları",
        text=slide44_text,
        elements=[
            make_cloze("Kutanöz gomlar deride iyileşirken genellikle at nalı şeklinde veya ortası {{atrofik skar}} bırakan lezyonlar oluşturur."),
            make_cloze("Sekonder sifiliz döküntülerinin aksine kutanöz gomlar daha lokalize ve {{destrüktif}} (yıkıcı) özelliktedir."),
            make_table(
                headers=["Özellik", "Sekonder Sifiliz Deri Lezyonu", "Kutanöz Gom (Tersiyer)"],
                rows=[
                    ["Dağılım", "Yaygın, simetrik", "Lokalize, asimetrik"],
                    ["Yıkıcılık", "Yüzeysel, skarsız iyileşir", "Derin, destrüktif, skarlı iyileşir"],
                    ["Bakteri Yükü", "Çok yüksek", "Çok düşük"]
                ]
            ),
            make_recall("Kutanöz gomların iyileşme dokusu karakteristiği nedir?", "Atrofik skar (genellikle at nalı şeklinde) bırakarak iyileşirler.")
        ]
    ))

    # Slide 45: Kemik Gom Tutulumu: Tibia, Fibula ve Gece Kemik Ağrıları
    slide45_text = """
    ## Kemik Gom Tutulumu: Tibia, Fibula ve Gece Kemik Ağrıları

    İskelet sistemi, gomların sık görüldüğü yerlerden biridir. Kemik gomları özellikle uzun kemiklerde, en sık tibia ve fibulada yerleşir. Lezyonlar periostit (periost inflamasyonu) veya osteite neden olarak kemikte destrüksiyon ve yeni kemik oluşumuyla sonuçlanır.

    Hastaların en sık şikayeti, özellikle gece istirahatte artan şiddetli kemik ağrılarıdır. Tibia anterior yüzünde periost kalınlaşması sonucu "kılıç kını kaval kemiği" (saber shin) görünümü gelişebilir.

    > Kemik tutulumu olan tersiyer sifilizde, gece artan kemik ağrısı ve uzun kemiklerdeki (tibia) şekil bozuklukları, gommatöz periostitin klinik yansımalarıdır.
    """
    slides.append(make_slide(
        title="Kemik Gom Tutulumu: Tibia, Fibula ve Gece Kemik Ağrıları",
        text=slide45_text,
        elements=[
            make_cloze("Kemik gomlarında klinik semptomların başında, özellikle {{gece}} artan şiddetli kemik ağrıları gelir."),
            make_cloze("Tibiada periost kalınlaşması sonucu ortaya çıkan deformiteye {{kılıç kını}} kaval kemiği (saber shin) denir."),
            make_quiz(
                question="Kemik gomlarının en belirgin klinik şikayeti nedir?",
                options=[
                    "Gündüz aktivite ile artan eklem ağrısı",
                    "Gece artan kemik ağrısı",
                    "Kemiklerde asimetrik kısalma",
                    "Patolojik kırıklar"
                ],
                answer="Gece artan kemik ağrısı",
                explanation="Kemik gomları (osteit/periostit) klasik olarak gece kötüleşen, istirahat ağrısı ile karakterizedir."
            ),
            make_chain([
                "Tibiada granülomatöz inflamasyon (gom)...",
                "Periostit ve yeni kemik yapımına neden olur...",
                "Ön yüzün kalınlaşmasıyla 'kılıç kını' deformitesi oluşur."
            ])
        ]
    ))

    # Slide 46: Klavikula ve Kraniyum Gom Lezyonları: Lokal Hassasiyet ve Osteolitik Harabiyet
    slide46_text = """
    ## Klavikula ve Kraniyum Gom Lezyonları: Lokal Hassasiyet ve Osteolitik Harabiyet

    Uzun kemikler dışında klavikula ve kraniyum (kafatası) da kemik gomlarının hedefindedir. Klavikula üzerinde yerleşen lezyonlar sternoklaviküler ekleme yakın lokal şişlik ve hassasiyet yaratır.

    Kraniyumda ise gomlar daha çok yassı kemikleri tutarak osteolitik (kemik yıkıcı) harabiyete neden olur. Radyolojik incelemelerde, kafatasında güve yeniği şeklinde defektler ve çevresinde skleroz gözlenebilir. Bu durum baş ağrısı ve lokalize kafa derisi hassasiyeti ile kendini gösterir.

    > Kraniyal ve klaviküler gomlar, lokalize destrüktif osteolitik lezyonlar oluşturur ve hastada bölgesel ağrı, şişlik ve radyolojik defektlere yol açar.
    """
    slides.append(make_slide(
        title="Klavikula ve Kraniyum Gom Lezyonları: Lokal Hassasiyet ve Osteolitik Harabiyet",
        text=slide46_text,
        elements=[
            make_cloze("Kraniyumdaki gom lezyonları radyolojide kemik yıkımı nedeniyle {{osteolitik}} defektler olarak izlenir."),
            make_cloze("Klavikula üzerindeki gomlar lokal şişlik ve {{hassasiyet}} ile kendini gösterir."),
            make_spot_lie(
                question="Kraniyum ve klavikula gomları hakkında hangisi yanlıştır (tuzaktır)? Odak: Patolojik bulgu",
                lies=[
                    "Kraniyumdaki gomlar sadece osteoblastik (yapım) lezyonlar oluşturur."
                ],
                truths=[
                    "Kraniyumda güve yeniği tarzı osteolitik lezyonlar yapabilirler.",
                    "Lokal hassasiyet ve bölgesel ağrı sık görülen semptomlardır.",
                    "Kemikte yıkım ve çevresel skleroz birlikte görülebilir."
                ],
                explanation="Gomlar kraniyumda osteolitik (yıkıcı) harabiyete neden olur; sadece yapım lezyonları oluşturmazlar.",
                isLie=True
            ),
            make_recall("Kafatası kemiklerindeki gom lezyonları radyolojik olarak nasıl görünür?", "Güve yeniği tarzında osteolitik (kemik yıkıcı) defektler olarak görünür.")
        ]
    ))

    # Slide 47: Visseral Gom: Karaciğer Tutulumu, Hepar Lobatum ve Sarılık
    slide47_text = """
    ## Visseral Gom: Karaciğer Tutulumu, Hepar Lobatum ve Sarılık

    İç organlar (visseral) arasında gomların en sık yerleştiği organ karaciğerdir. Karaciğerde gelişen çok sayıda gom, iyileşme sürecinde yoğun fibröz skar dokusu oluşturarak karaciğerin dış yüzeyini derin yarıklarla böler. Bu deformasyona **hepar lobatum** adı verilir.

    Hepar lobatum anatomik bozulmaya yol açsa da, genellikle klinik olarak ciddi karaciğer yetmezliği yapmaz. Ancak safra yollarına bası olursa sarılık veya portal vene bası olursa hafif portal hipertansiyon bulguları ortaya çıkabilir.

    > Karaciğer gomlarının iyileşmesiyle oluşan kaba, lobüle skar yapısına hepar lobatum denir; fonksiyonel yetmezlikten ziyade mekanik bası semptomlarına neden olabilir.
    """
    slides.append(make_slide(
        title="Visseral Gom: Karaciğer Tutulumu, Hepar Lobatum ve Sarılık",
        text=slide47_text,
        elements=[
            make_cloze("Karaciğerde çok sayıda gomun skarlı iyileşmesi sonucu organın lobüle görünüm almasına {{hepar lobatum}} denir."),
            make_cloze("Karaciğer gomları sıklıkla ağır yetmezlik yapmaz, ancak safra yollarına bası yaparsa {{sarılık}} görülebilir."),
            make_quiz(
                question="Hepar lobatum gelişen bir hastada sarılık görülmesinin en olası nedeni aşağıdakilerden hangisidir?",
                options=[
                    "Masif hepatosit nekrozu",
                    "Safra yollarına dışarıdan bası",
                    "Otoimmün hepatit atağı",
                    "Primer biliyer kolanjit gelişimi"
                ],
                answer="Safra yollarına dışarıdan bası",
                explanation="Gom skarları mekanik bası ile safra yollarını tıkayarak tıkanma sarılığına yol açabilir."
            ),
            make_chain([
                "Karaciğerde granülomatöz gomların gelişimi...",
                "İyileşme sürecinde yoğun fibröz skar oluşumu...",
                "Karaciğerde derin yarıklar ve 'hepar lobatum' görünümü."
            ])
        ]
    ))

    # Slide 48: Gom Lezyonlarının Destrüktif Doğası ve Komplikasyonları
    slide48_text = """
    ## Gom Lezyonlarının Destrüktif Doğası ve Komplikasyonları

    Gomlar hangi organda yerleşirse yerleşsin derin ve yıkıcı (destrüktif) bir doğaya sahiptir. Örneğin damak veya nazal septumda yerleşen gomlar, kıkırdak ve kemik perforasyonlarına yol açarak yüzde "semer burun" deformitesi veya damak delinmesi yapabilir.

    Larenkste yerleştiğinde ses kısıklığına, solunum yolu obstrüksiyonuna; midede yerleştiğinde ise ülsere kanserleri taklit eden semptomlara neden olabilirler. Gomların komplikasyonları, yerleştikleri dokunun anatomik fonksiyonunu kaybetmesinden kaynaklanır.

    > Gomlar granülomatöz inflamasyon ve fibrozisle, yerleştikleri organlarda septum perforasyonu veya larengeal stenoz gibi kalıcı, ağır yapısal yıkımlara neden olurlar.
    """
    slides.append(make_slide(
        title="Gom Lezyonlarının Destrüktif Doğası ve Komplikasyonları",
        text=slide48_text,
        elements=[
            make_cloze("Nazal septum veya damakta yerleşen gomlar doku yıkımı yaparak {{perforasyonlara}} (delinmelere) neden olabilir."),
            make_cloze("Gomlar nazal kemik ve kıkırdağı yıkarak yüzde {{semer burun}} deformitesine yol açabilir."),
            make_table(
                headers=["Yerleşim Yeri", "Olası Komplikasyon"],
                rows=[
                    ["Damak / Nazal Septum", "Perforasyon, Semer Burun"],
                    ["Larenks", "Ses kısıklığı, Hava yolu obstrüksiyonu"],
                    ["Karaciğer", "Hepar lobatum, Safra yolu basısı"]
                ]
            ),
            make_recall("Damakta yerleşen bir gom nasıl bir komplikasyona yol açabilir?", "Doku yıkımına bağlı damak perforasyonu (delinmesi) yapabilir.")
        ]
    ))

    # Slide 49: Tersiyer Dönemde Bulaştırıcılığın Bulunmaması İlkesi
    slide49_text = """
    ## Tersiyer Dönemde Bulaştırıcılığın Bulunmaması İlkesi

    Sifilizin tersiyer dönemi, hastalığın en ağır klinik tablolara sahip olmasına rağmen **bulaştırıcı (enfeksiyöz) değildir**. Çünkü tersiyer dönem lezyonları (gomlar, kardiyovasküler tutulum) içindeki spiroket yükü yok denecek kadar azdır.

    Bulaş, temelde yüksek spiroket yüküne sahip şankr (primer) ve kondilomata lata gibi sekonder dönem lezyonlarıyla gerçekleşir. Hastalar tersiyer evrede yıkıcı doku hasarları yaşasalar da, cinsel temasla hastalığı başkalarına bulaştırmazlar.

    > Tersiyer sifiliz, klinik olarak destrüktiftir ancak lezyonlardaki spiroket azlığı nedeniyle cinsel partnerler için bulaştırıcı kabul edilmez.
    """
    slides.append(make_slide(
        title="Tersiyer Dönemde Bulaştırıcılığın Bulunmaması İlkesi",
        text=slide49_text,
        elements=[
            make_cloze("Tersiyer sifiliz dönemindeki hastalar, cinsel temas ile {{bulaştırıcı}} değildir."),
            make_cloze("Bu dönemde bulaşıcılığın olmamasının nedeni, lezyonlardaki {{spiroket}} (bakteri) yükünün çok düşük olmasıdır."),
            make_spot_lie(
                question="Tersiyer evre sifiliz ile ilgili hangisi yanlıştır (tuzaktır)? Odak: Bulaştırıcılık",
                lies=[
                    "Tersiyer gomlardan alınan akıntı ile hastalık çok kolay bulaşır."
                ],
                truths=[
                    "Tersiyer evre cinsel yolla bulaştırıcı kabul edilmez.",
                    "Gom lezyonlarında spiroket yükü yok denecek kadar azdır.",
                    "Bulaş esas olarak primer ve sekonder evrelerde görülür."
                ],
                explanation="Tersiyer dönemdeki gomlarda bakteri (spiroket) bulunmadığından, hastalar cinsel yolla bulaştırıcı değildir.",
                isLie=True
            ),
            make_recall("Tersiyer evredeki bir hasta hastalığını eşine bulaştırır mı?", "Hayır, lezyonlarda bakteri azlığı nedeniyle bulaştırıcı değildir.")
        ]
    ))

    # Slide 50: [TEKRAR SAYFASI - CHECKPOINT 5]
    slide50_text = """
    ## [TEKRAR SAYFASI - CHECKPOINT 5] Tersiyer Sifiliz ve Gommatöz Lezyonlar

    Tersiyer sifiliz, Tip IV hücresel immün yanıtın patolojik hale geldiği yıkıcı evredir.
    Önemli kavramlar:
    - **Gom (Gumma):** Granülomatöz nekrotizan lezyon; spiroket yükü çok düşüktür.
    - **Deri ve Kemik:** Atrofik skar bırakan deri ülserleri, tibia kılıç kını deformitesi, gece ağrıları.
    - **Visseral Gom:** Karaciğerde hepar lobatum.
    - **Bulaşıcılık:** Gomlar bakteri içermediği için tersiyer evre bulaştırıcı DEĞİLDİR.
    """
    slides.append(make_slide(
        title="[TEKRAR SAYFASI - CHECKPOINT 5] Tersiyer Sifiliz ve Gommatöz Lezyonlar",
        text=slide50_text,
        elements=[
            make_cloze("Gom lezyonlarının immünolojik temeli {{Tip IV}} aşırı duyarlılık reaksiyonudur."),
            make_cloze("Karaciğer gomlarının iyileşmesi ile organda oluşan lobüle deformasyona {{hepar lobatum}} denir."),
            make_table(
                headers=["Kavram", "Açıklama"],
                rows=[
                    ["Hücresel İmmünite", "Tersiyer evrede doku yıkımından sorumlu abartılı yanıt"],
                    ["Kemik Gom", "Gece ağrısı ve osteolitik/osteoblastik harabiyet"],
                    ["Bulaştırıcılık", "Tersiyer evrede yoktur (Spiroket yükü çok düşük)"]
                ]
            ),
            make_recall("Tersiyer sifilizde kıkırdak ve kemik yıkımına bağlı damakta ne tür bir komplikasyon görülebilir?", "Perforasyon (delinme) görülebilir.")
        ]
    ))

    return slides
