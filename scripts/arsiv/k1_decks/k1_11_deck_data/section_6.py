# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-11-s51",
        "title": "Obstrüksiyonda Tübüler Fonksiyon Bozukluklarına Genel Bakış",
        "content": "Üriner obstrüksiyonda tübüler sistemin fonksiyonel bozulması iki belirgin aşamada seyreder:\n\n- **Başlangıç Evresi:** Obstrüksiyonun erken saatlerinde glomerüler filtrasyon basıncı düşerken tübüllerde sıvı akışı yavaşlar. Proksimal tübül sıvıyı daha yavaş taşıdığından su ve sodyumun temas süresi uzar; geri emilim göreceli olarak artar. Bu erken dönemde idrar volümü azalır (oligüri) ve idrar osmolaritesi artar (konsantre idrar).\n- **İleri / Kronik Evre:** Tıkanıklık sürdükçe medüller iskemi ve tübüler epitel hasarı derinleşir. Toplayıcı kanallar hormonlara yanıt veremez hale gelir. İleri dönemde **ADH'ya (Antidiüretik Hormon / Vazopressin) karşı direnç** gelişir; konsantrasyon kabiliyeti çöker, idrar dilüe, **hipostenürik ve poliürik** bir yapı kazanır. İdrar asidifikasyonu bozulur ve azotemi belirginleşir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Tübüler Yanıtın Dönemsel Evrimi",
                "Başlangıç Dönemi",
                "İdrar akımı yavaşlar, sıvı teması uzar; idrar volümü azalır ve osmolaritesi artar.",
                "İleri (Kronik) Dönem",
                "ADH direnci gelişir, konsantrasyon çöker; idrar dilüe, hipostenürik ve poliürik hale gelir."
            ),
            make_cloze(
                "Üriner obstrüksiyonun ileri döneminde toplayıcı kanallarda ADH direncine bağlı olarak idrar konsantre edilemez ve hipostenüri gelişir.",
                "hipostenüri",
                "İdrar dansitesinin plazma dansitesinin altına inmesi durumu"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-11-s52",
        "title": "Medüller Hipertonisite Kaybı ve Karşı Akım Mekanizmasının Bozulması",
        "content": "Normal bir böbreğin idrarı konsantre edebilmesi, renal medullada papilla ucuna doğru giderek artan hipertonik bir ozmotik gradyentin (300 mOsm/kg'dan 1200 mOsm/kg'a) korunmasına bağlıdır. Bu gradyent Henle kulpunun kalın çıkan kolundaki Na-K-2Cl kotransportörlerinin aktif sodyum pompalaması ve vaza rektaların karşı akım değişim mekanizmasıyla oluşturulur. Obstrüksiyonda gelişen medüller iskemi, Na-K-2Cl taşıyıcılarının ATP bağımlı çalışmasını sekteye uğratır; sodyum ve klor medüller interstisyuma pompalanamaz. Ayrıca retrograd basınç vaza rekta kılcallarındaki perfüzyonu bozarak interstisyel solütleri yıkayıp götürür ('washout'). Medüller hipertonisite kaybolduğunda, toplayıcı kanaldan suyun interstisyuma çekilmesini sağlayan ozmotik itici güç tamamen sıfırlanır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Medüller Konsantrasyon Mekanizmasının Çöküşü",
                [
                    "1. Medüller İskemi: Yüksek basıncın medüller kapillerleri sıkıştırması",
                    "2. Pompa İflası: Henle çıkan kolunda ATP tükenmesi ve aktif sodyum transportunun durması",
                    "3. Medüller Yıkanma: Ozmotik medüller gradyentin tamamen silinmesi",
                    "4. Su Geri Emilim Kaybı: Ozmotik çekim kuvveti kalmadığından konsantre idrar yapılamaması"
                ]
            ),
            make_recall(
                "Böbreğin idrarı konsantre etmesini sağlayan medüller ozmotik gradyenti kuran Henle kulpu segmenti hangisidir?",
                "Henle kulpunun kalın çıkan koludur.",
                "Aktif Na-K-2Cl pompalarının bulunduğu segment"
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-11-s53",
        "title": "Toplayıcı Kanallarda Vazopressin (ADH) Direnci ve Nefrojenik DI",
        "content": "Kronik üriner obstrüksiyonun en karakteristik tübüler patolojisi, hipofizden salınan Antidiüretik Hormona (ADH / Arginin Vazopressin) karşı toplayıcı kanal esas (principal) hücrelerinde gelişen edinsel dirençtir. Normalde ADH bazolateral V2 reseptörlerine bağlanarak cAMP yolağı üzerinden Akuaporin-2 (AQP2) su kanallarının apikal membrana yerleşmesini sağlar. Obstrükte böbrekte hem V2 reseptör yoğunluğu azalır hem de hücre içi cAMP sinyal iletimi bozulur; bunun sonucunda apikal membran AQP2 ekspresyonu %70-80 oranında azalır. Vücutta yüksek miktarda ADH bulunmasına rağmen toplayıcı tübül epiteli suya karşı tamamen geçirimsiz kalır. Bu durum edinsel bir **nefrojenik diyabetes insipidus (NDI)** tablosu oluşturur; hasta bol miktarda düşük dansiteli idrar çıkarır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Üriner obstrüksiyonda gelişen edinsel nefrojenik diyabetes insipidus tablosunda toplayıcı tübüllerdeki temel moleküler defekt hangisidir?",
                [
                    {"key": "A", "text": "Toplayıcı kanal hücrelerinde Akuaporin-2 su kanallarının ekspresyonunda ve yerleşiminde belirgin azalma", "explanation": "A seçeneği doğrudur: ADH direnci sonucu AQP2 kanalları apikal membrana taşınamaz ve su geçirgenliği çöker."},
                    {"key": "B", "text": "Hipotalamustan vazopressin sentezinin kalıcı durması", "explanation": "B seçeneği yanlıştır: Bu santral DI tablosudur, obstrüksiyon periferik tübüler direnç yapar."},
                    {"key": "C", "text": "Glomerül bazal membranının tüm proteinleri sızdırması", "explanation": "C seçeneği yanlıştır: Bu nefrotik sendrom mekanizmasıdır."},
                    {"key": "D", "text": "Proksimal tübülde glukoz taşıyıcılarının (SGLT2) aşırı çoğalması", "explanation": "D seçeneği yanlıştır: Glukoz transportu ile ADH direnci ilişkisizdir."},
                    {"key": "E", "text": "Aldosteron hormonunun tamamen sıfırlanması", "explanation": "E seçeneği yanlıştır: Aldosteron yokluğu değil AQP2 eksikliği su kaybını açıklar."}
                ],
                "A"
            ),
            make_cloze(
                "Toplayıcı kanal apikal membranında suya geçirgenliği sağlayan akuaporin-iki kanallarının ekspresyon kaybı obstrüktif poliürinin ana nedenidir.",
                "akuaporin-iki",
                "ADH kontrolündeki temel apikal su kanalı proteini"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-11-s54",
        "title": "İdrar Konsantrasyon Yeteneğinde Bozulma: Hipostenüri ve Poliüri",
        "content": "Medüller hipertonisitenin kaybı ve toplayıcı kanallardaki ADH direnci birleştiğinde böbreğin idrarı konsantre etme kabiliyeti tamamen çöker. Normalde susuzluk durumunda idrar dansitesi 1030'un üzerine, osmolaritesi 1200 mOsm/kg'a kadar çıkarılabilir. Obstrüktif üropatili bir hastada ise idrar konsantre edilemez ve dansite plazma dansitesine (1010 / ~290 mOsm/kg) veya daha altına sabitlenir; buna **hipostenüri / izostenüri** denir. Tıkanıklık kısmi olduğunda hasta paradoksal olarak 'bol idrar çıkarma (poliüri)' ve gece sık idrara kalkma (noktüri) şikayetiyle başvurabilir. Klinisyenin obstrüksiyonu dışlamak için 'hastanın idrarı bol çıkıyor, tıkanıklık olamaz' yanılgısına düşmemesi gerekir; parsiyel obstrüksiyonda konsantrasyon defekti nedeniyle poliüri en sık görülen bulgulardan biridir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "62 yaşında erkek hasta, son aylarda günde 3.5 litre açık renkli idrar çıkarma ve geceleri 4-5 kez idrara kalkma şikayetiyle başvuruyor. İdrar dansitesi 1006 ölçülüyor. USG'de bilateral orta derecede hidronefroz ve BPH saptanıyor.",
                "Bu hastadaki poliüri ve düşük idrar dansitesinin fizyopatolojik izahı nedir?",
                [
                    {
                        "text": "Parsiyel kronik obstrüksiyona bağlı gelişen ADH direnci ve medüller gradyent kaybı sonucu idrar konsantre edilememektedir (hipostenürik poliüri).",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Parsiyel tıkanıklıkta konsantrasyon kabiliyetinin çökmesi bol ve düşük dansiteli idrar çıkarmaya yol açar."
                    },
                    {
                        "text": "Böbreklerin aşırı fonksiyon kazanarak glomerüler filtrasyon hızını normalin 3 katına çıkarmasıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Obstrüksiyonda GFR artmaz, azalır; poliüri tübüler konsantrasyon yetersizliğinden kaynaklanır."
                    },
                    {
                        "text": "Primer psikojenik polidipsi olup obstrüksiyonla hiçbir nedensel bağlantısı yoktur.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Bilateral hidronefroz ve BPH varlığı organik obstrüktif nefrojenik DI tablosunu gösterir."
                    }
                ]
            ),
            make_recall(
                "Obstrüksiyonda idrar konsantrasyon yeteneğinin kaybolmasıyla idrar dansitesinin plazma seviyesine veya altına inmesi tablosuna ne ad verilir?",
                "Hipostenüri (veya izostenüri).",
                "Düşük özgül ağırlıklı idrar durumu"
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-11-s55",
        "title": "İdrar Asidifikasyon Kapasitesinde Kayıp: Tip 4 / Tip 1 RTA Benzeri Tablo",
        "content": "Böbrek, metabolik asit yükünü nötralize etmek için distal nefron ve toplayıcı kanallardaki interkale (intercalated) hücreler aracılığıyla lümene H+ iyonu pompalar. Üriner obstrüksiyonda kortikal ve medüller toplayıcı kanallardaki alfa-interkale hücrelerin apikal H+-ATPaz ve H+/K+-ATPaz pompaları hasara uğrar. Bu durum idrarın asidifiye edilmesini engeller; sistemik asidoz varlığında dahi idrar pH'sı 5.5'in altına düşürülemez. Tablo klinik olarak Distal Renal Tübüler Asidoz (Tip 1 RTA) veya hiperkalemik Tip 4 RTA benzeri bir asidifikasyon defekti sergiler. Hidrojen iyonlarının atılamaması kanda birikerek hiperkloremik, normal anyon açıklı metabolik asidoz gelişimine zemin hazırlar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Obstrüktif üropatide toplayıcı kanal interkale hücre hasarına bağlı olarak idrar asidifikasyon kapasitesi belirgin sekilde düser.",
                "asidifikasyon kapasitesi",
                "İdrara hidrojen pompalayarak pH'yı düşürme yeteneği"
            ),
            make_quiz(
                "Obstrüktif nefropatide asit-baz dengesizliğinin ortaya çıkmasından sorumlu temel tübüler hücre grubu hangisidir?",
                [
                    {"key": "A", "text": "Toplayıcı kanal alfa-interkale hücreleri", "explanation": "A seçeneği doğrudur: H+-ATPaz pompaları içeren alfa-interkale hücreleri hasar gördüğünde H+ atılamaz ve asidifikasyon çöker."},
                    {"key": "B", "text": "Jukstaglomerüler granüler hücreler", "explanation": "B seçeneği yanlıştır: Bu hücreler renin salgılar, H+ pompalamaz."},
                    {"key": "C", "text": "Mesanjiyal fagositik hücreler", "explanation": "C seçeneği yanlıştır: Mesanjiyum glomerül destek dokusudur."},
                    {"key": "D", "text": "Henle ince inen kol endoteli", "explanation": "D seçeneği yanlıştır: Pasif su geçişi yapar, asit pompası içermez."},
                    {"key": "E", "text": "Macula densa kemoreseptörleri", "explanation": "E seçeneği yanlıştır: Tübüloglomerüler feedback sodyum sensörüdür."}
                ],
                "A"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-11-s56",
        "title": "Titrabl Asit, Amonyak Ekskresyonu ve Bikarbonat Emilim Defektleri",
        "content": "Obstrüksiyona bağlı idrar asidifikasyon bozukluğunun biyokimyasal temeli üç ana sütunda gerçekleşir:\n\n1. **Titrabl Asit Eliminasyonunda Azalma:** İdrardaki en önemli tampon olan fosfat (HPO4^2-) moleküllerine hidrojen bağlanarak H2PO4- şeklinde atılması süreci sekteye uğrar; titrabl asit ekskresyonu yarı yarıya azalır.\n2. **Amonyak (NH3 / NH4+) Ekskresyonunda Bozulma:** Proksimal tübülde glutaminden amonyak üretimi ve distal toplayıcı kanala difüzyonu bozulur; idrarla amonyum atımı dramatik şekilde düşer.\n3. **Bikarbonat Reabsorpsiyonunda Bozulma:** Proksimal tübül iskemiye uğradığında fırçamsı kenardaki Na+/H+ değiştiricisi (NHE3) ve karbonik anhidraz enzim aktivitesi geriler; filtre edilen bikarbonatın geri emilimi aksar.\n\nBu üç defektin toplamı, obstrüksiyon hastalarında kanda bikarbonat düzeyinin 15-18 mEq/L'ye kadar inmesine yol açar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Asit Eliminasyon Bileşeni", "Normal Mekanizma", "Obstrüksiyondaki Patoloji"],
                [
                    [
                        {"text": "Titrabl Asit (Fosfat Tamponu)", "isMasked": False, "hint": ""},
                        {"text": "Lümendeki HPO4'e H+ bağlanarak atılır", "isMasked": True, "hint": "Lümen içi fosfat tamponlama reaksiyonu"},
                        {"text": "H+ sekresyonu azaldığından titrabl asit atımı düşer", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Amonyak Ekskresyonu", "isMasked": False, "hint": ""},
                        {"text": "Glutaminden sentezlenip NH4+ olarak idrara verilir", "isMasked": True, "hint": "Tübüler yeni bikarbonat kazandıran temel mekanizma"},
                        {"text": "Amonyakogenez ve tübüler transfer bozulur", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Bikarbonat Geri Emilimi", "isMasked": False, "hint": ""},
                        {"text": "Proksimal tübülde %85-90 oranında reabsorbe edilir", "isMasked": True, "hint": "Filtre edilen alkali rezervin geri kazanımı"},
                        {"text": "İskemik epitelde proksimal emilim defekti gelişir", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Obstrüktif üropatide idrar asidifikasyonunun çöküşünü gösteren ve lümendeki fosfat tamponunun yetersiz kullanımını yansıtan parametre nedir?",
                "Titrabl asit eliminasyonunun azalmasıdır.",
                "Fosfata bağlı asit atım parametresi"
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-11-s57",
        "title": "Tübüler Elektrolit Taşınması: Sodyum ve Potasyum Dinamikleri",
        "content": "Obstrüksiyon tübüler elektrolit taşıyıcı proteinlerin ekspresyonunu geniş çapta baskılar. Proksimal tübüldeki NHE3, Henle kalın çıkan kolundaki NKCC2 ve toplayıcı kanallardaki epitelyal sodyum kanalları (ENaC) azalır. Bunun sonucunda böbreğin fraksiyonel sodyum ekskresyonu (FeNa) artar; hasta 'tuz kaybettiren nefropati' tablosuna girer. Diğer taraftan, toplayıcı kanalların aldosterona yanıtı zayıflar ve lümene potasyum sekresyonu (ROMK kanalları üzerinden) sekteye uğrar. GFR düşüklüğü ve azalmış distal tübüler akım hızı ile birleştiğinde vücutta potasyum birikimi (hiperkalemi) riski belirginleşir. Ancak tek taraflı obstrüksiyonda sağlam böbrek fazla potasyumu ve tuzu kompanse edebildiğinden elektrolit bozuklukları bilateral tıkanıklıklarda çok daha yıkıcıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Tübüler Elektrolit Dengesizliği Zinciri",
                [
                    "1. Taşıyıcı Kaybı: ENaC ve NKCC2 proteinlerinin tübül membranında azalması",
                    "2. Tuz Kaybı: Tübüler sodyum geri emiliminin yetersizleşmesi ve natriürez",
                    "3. Potasyum Sekresyon Kaybı: Lümene K+ atımının bozulması ve aldosteron direnci",
                    "4. Elektrolit İflası: Sistemik hiperkalemi ve hiponatremi riski"
                ]
            ),
            make_recall(
                "Obstrüksiyonda tübüler sodyum geri emilim kapasitesinin düşmesi sonucu böbrekten sodyum kaybına ne ad verilir?",
                "Tuz kaybettiren nefropati (salt-wasting nephropathy).",
                "Sodyumun idrarla kontrolsüz atılması tablosu"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-11-s58",
        "title": "Kritik Korunan Fonksiyon: Üriner Dilüsyon Kapasitesinin Sağlam Kalması",
        "content": "Tıp fakültesi kurullarında ve üroloji uzmanlık sınavlarında en sık sorulan kardinal fizyopatolojik ilkelerden biri, obstrüksiyon sonrasında tübüler fonksiyonların geri dönüş paternidir. Obstrüksiyon giderildikten sonra normal böbreğe kıyasla: GFR azalmış, renal kan akımı düşmüş, idrarı konsantre etme kabiliyeti ciddi derecede bozulmuş, hidrojen ve fosfat ekskresyonu aksamış ve sodyum geri emilimi hafif hasarlı kalmaktadır. ANCAK BÖBREĞİN **ÜRİNER DİLÜSYON (İDRARI SULANDIRMA) YETENEĞİ ETKİLENMEZ!** Su yüklemesi yapıldığında böbrek toplayıcı kanallarını suya kapalı tutarak idrar dansitesini 1001-1002 seviyelerine kadar düşürebilir ve aşırı serbest suyu atabilir. Dilüsyon kapasitesinin korunması, kortikal dilüsyon segmentinin obstrüksiyon basıncına medullaya göre daha dirençli olmasından kaynaklanır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Üriner obstrüksiyon giderildikten sonra iyileşme döneminde böbreğin diğer tüm fonksiyonları bozulmuşken normal kalan ve ETKİLENMEYEN fonksiyon hangisidir?",
                [
                    {"key": "A", "text": "Üriner dilüsyon yeteneği", "explanation": "A seçeneği DOĞRUDUR: Ders notunun açık vurgusuyla obstrüksiyon sonrası 'üriner dilüsyon yeteneği etkilenmez'."},
                    {"key": "B", "text": "İdrar konsantrasyon yeteneği", "explanation": "B seçeneği yanlıştır: Konsantrasyon kabiliyetinde ağır yetmezlik gelişir."},
                    {"key": "C", "text": "Glomerüler filtrasyon hızı (GFR)", "explanation": "C seçeneği yanlıştır: GFR belirgin derecede azalmıştır."},
                    {"key": "D", "text": "Renal kan akımı (RBF)", "explanation": "D seçeneği yanlıştır: Renal kan akımı normalin altındadır."},
                    {"key": "E", "text": "Hidrojen ve fosfat ekskresyon kapasitesi", "explanation": "E seçeneği yanlıştır: Asit atım kapasitesi de hasarlıdır."}
                ],
                "A"
            ),
            make_cloze(
                "Üriner obstrüksiyon dekomprese edildikten sonra böbreğin konsantrasyon yeteneği bozulurken üriner dilüsyon yeteneği etkilenmez.",
                "üriner dilüsyon yeteneği",
                "İdrarı sulandırabilme ve serbest suyu atabilme kapasitesi"
            )
        ]
    })

    # Slide 59 (CHECKPOINT 6)
    slides.append({
        "id": "k1-11-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Tübüler Bozukluklar, ADH Direnci ve Hipostenüri",
        "content": "Obstrüksiyonda tübüler sistem değişikliklerinin kilit sentezi:\n\n1. **Zaman Çizelgesi:** Başlangıçta idrar akımı yavaşlar, hacim azalır, osmolarite artar. İleri dönemde ADH direnciyle konsantrasyon çöker, hipostenüri ve poliüri gelişir.\n2. **Medüller Yıkanma:** İskemi nedeniyle Henle kalın çıkan kolundaki aktif sodyum pompalaması durur ve medüller ozmotik gradyent silinir.\n3. **Nefrojenik DI:** Toplayıcı kanallarda Akuaporin-2 su kanallarının sentez ve membran yerleşimi engellenir; suya geçirimsizlik poliüri yapar.\n4. **Asidifikasyon:** Alfa-interkale hücre hasarıyla H+ atılamaz; titrabl asit ve amonyum düşer, metabolik asidoz gelişir.\n5. **Altın Kural:** Obstrüksiyon sonrası GFR, RBF, konsantrasyon ve asit atımı bozulur; ancak **üriner dilüsyon yeteneği sağlam kalır**.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Tübüler Fonksiyon", "Obstrüksiyondaki Durumu", "Klinik Yansıması"],
                [
                    [
                        {"text": "Konsantrasyon Yeteneği", "isMasked": False, "hint": ""},
                        {"text": "Ağır hasarlı (ADH direnci + AQP2 kaybı)", "isMasked": True, "hint": "Su tutma mekanizmasının çöküşü"},
                        {"text": "Poliüri, noktüri ve hipostenüri", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Asidifikasyon Kapasitesi", "isMasked": False, "hint": ""},
                        {"text": "Bozulmuş (İnterkale H+-ATPaz hasarı)", "isMasked": True, "hint": "Asit iyonu pompalama defekti"},
                        {"text": "Metabolik asidoz, yüksek idrar pH'sı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Dilüsyon Yeteneği", "isMasked": False, "hint": ""},
                        {"text": "ETKİLENMEZ (Sağlam kalır)", "isMasked": True, "hint": "Ders notundaki en kritik sınav spotu"},
                        {"text": "Su yüklemesinde idrarı sulandırabilme", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Obstrüksiyon giderildikten sonra konsantrasyon kabiliyetinin iflas etmesine karşın sağlam kalan tek tübüler fonksiyon nedir?",
                "Üriner dilüsyon yeteneğidir.",
                "Kritik spot kuralı hatırlayınız"
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-11-s60",
        "title": "Obstrüksiyon Giderildikten Sonra İyileşmeyi Belirleyen Faktörler",
        "content": "Obstrüksiyon cerrahi veya kateterle giderildikten sonra böbrek fonksiyonlarının nihai toparlanma düzeyini belirleyen dört temel etken bulunmaktadır:\n\n1. **Obstrüksiyonun Süresi:** Süre uzadıkça nefron ölümü ve skleroz arttığından fonksiyonel geri kazanım düşer.\n2. **Enfeksiyon Varlığı:** Obstrüksiyona eşlik eden piyelonefrit veya piyonefroz, bakteriyel enzimler ve lökosit infiltrasyonu ile parankim yıkımını katlayarak geri dönüşümsüzleştirir.\n3. **İntrarenal vs Ekstrarenal Pelvis Mimarisi:** Ekstrarenal pelvis basıncı emerek parankimi bir miktar korurken, intrarenal pelvis varlığında fonksiyonel kayıp çok daha ağırdır.\n4. **Koruyucu Reflü Mekanizmalarının Etkinliği:** Pyelointerstisyel ve pyelolenfatik reflünün dekompresyon gücü ne kadar yüksek olmuşsa, böbrek fonksiyonel rezervi o kadar iyi korunmuştur.\n\nİyileşen böbrek genellikle daha az miktarda ve kalitesiz idrar üretebilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "Bir üroloji servisinde iki ayrı hastaya taş obstrüksiyonu nedeniyle JJ stent takılıyor. Birinci hasta 5 gündür tıkanıklık yaşayan ve idrarı steril olan genç hasta; ikinci hasta ise 4 haftadır obstrükte olan, idrar kültüründe E. coli üreyen ve intrarenal pelvis anatomisine sahip diyabetik hasta.",
                "Hangi hastada dekompresyon sonrası fonksiyonel iyileşme potansiyeli çok daha düşüktür ve neden?",
                [
                    {
                        "text": "İkinci hastada; çünkü obstrüksiyon süresi uzun, parankim hasarını artıran enfeksiyon mevcut ve basıncı doğrudan dokuya ileten intrarenal pelvis yapısı vardır.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Süre, enfeksiyon ve intrarenal pelvis yapısı iyileşmeyi olumsuz etkileyen en majör prognostik faktörlerdir."
                    },
                    {
                        "text": "Birinci hastada; çünkü erken müdahale edilen böbreklerde şok tablosu daha ağır seyreder.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Erken müdahale nefronları kurtarır, prognozu çok daha üstün kılar."
                    },
                    {
                        "text": "Her iki hastada da yaş ve anatomiden bağımsız olarak iyileşme oranları birebir eşittir.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Süre, enfeksiyon ve pelvis anatomisi iyileşmeyi dramatik ölçüde farklılaştırır."
                    }
                ]
            ),
            make_cloze(
                "Obstrüksiyon giderildikten sonra böbrek fonksiyonlarının düzelmesini belirleyen en kritik klinik etkenler süre, enfeksiyon, pelvis tipi ve koruyucu reflülerdir.",
                "koruyucu reflülerdir",
                "İdrarın sinüse ve lenfatiklere sızarak basıncı düşürdüğü güvenlik yolları"
            )
        ]
    })

    return slides
