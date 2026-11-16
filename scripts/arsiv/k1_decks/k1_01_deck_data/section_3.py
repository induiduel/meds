#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 3 Builder: Dismorfoloji ve Kraniyofasiyal Muayene (Adım 22 - 36 + Tekrar Sayfası)
"""

from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall
)

def get_steps():
    return [
        {
            "slideNumber": 22,
            "title": "Dismorfoloji Biliminin Doğuşu ve Dr. David W. Smith'in Klinik Mirası",
            "subtitle": "Doğumsal yapısal defektlerin sistematik fenotipik analizi",
            "badge": "Tarihçe & Tanım",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Dismorfoloji terimi 1966 yılında Dr. David W. Smith tarafından tıbbi literatüre kazandırılmıştır. Smith, insan morfolojisindeki doğumsal yapısal varyasyonların rastgele kusurlar olmadığını, embriyolojik doku etkileşimlerinin ve genetik mutasyonların dışa yansıyan birer haritası olduğunu kanıtlamıştır.\n\nDismorfolojik yaklaşımın temel ilkeleri:\n- **Bütüncül Bakış:** Hekim hastaya tek bir organ kusuru (örneğin sadece VSD veya yarık damak) olarak bakmaz; saç çizgisinden ayak parmaklarına kadar tüm bedeni tarar.\n  - **Morfogenez Zamanlaması:** Bir anomalinin varlığı, intrauterin yaşamda o dokunun hangi embriyolojik haftada hasar gördüğünü ortaya koyar.\n  - **Atlas ve Veri Tabanı Kullanımı:** David Smith'in 'Recognizable Patterns of Human Malformation' kitabı bugün dahi klinik genetiğin başucu atlasıdır.",
            "medicalTerms": [
                {"term": "Dismorfoloji", "explanation": "İnsan embriyogenezindeki morfolojik kusurları ve doğumsal yapısal anomalileri inceleyen klinik bilim dalı."},
                {"term": "Morfogenez", "explanation": "Embriyoda hücrelerin organize olarak doku ve organ biçimlerini oluşturma süreci."}
            ],
            "spotPearls": [
                "Dismorfoloji terimini ilk kez Dr. David W. Smith kullanmış ve doğumsal anomalilerin sendromik kalıplarını tanımlamıştır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tıbbi genetikte doğumsal yapısal defektleri ve anormal morfolojik kalıpları inceleyen 'dismorfoloji' kavramını ilk kez tanımlayan hekim kimdir?",
                    {
                        "A": "Dr. David W. Smith (1966)",
                        "B": "Dr. Jerome Lejeune (1959)",
                        "C": "Gregor Mendel (1865)",
                        "D": "James Watson ve Francis Crick (1953)"
                    },
                    "A",
                    {
                        "A": "Doğru! Dr. David W. Smith dismorfoloji terimini 1966'da türetmiş ve klinik genetiğin temelini atmıştır.",
                        "B": "Yanlış. Jerome Lejeune Trizomi 21'in kromozomal temelini bulmuştur.",
                        "C": "Yanlış. Mendel klasik bezelye kalıtımının babasıdır.",
                        "D": "Yanlış. Watson ve Crick DNA çift sarmal yapısını aydınlatmıştır."
                    }
                ),
                make_cloze(
                    "Doğumsal yapısal defektlerin embriyolojik ve klinik analizini yapan bilim dalı olan dismorfoloji kavramı 1966 yılında Dr. David W. Smith tarafından tanımlanmıştır.",
                    "Dr. David W. Smith",
                    "Dismorfoloji teriminin öncüsü hekim"
                )
            ]
        },
        {
            "slideNumber": 23,
            "title": "Dismorfik Özellik Nedir? Normal Varyasyon ile Patoloji Sınırı",
            "subtitle": "Popülasyon sıklığı, etnik farklılıklar ve ailevi benzerlikler",
            "badge": "Klinik Yaklaşım",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Dismorfik özellik; bireyin fiziksel yapısında toplumun genel morfolojik standartlarından belirgin sapma gösteren yapısal özelliktir.\n\nBir özelliğin patolojik kabul edilebilmesi için şu üç kritik filtre uygulanır:\n- **1. Popülasyon ve Etnik Kriter:** Bir toplumda nüfusun %4'ünden daha azında görülen özellikler minör anomali / dismorfik özellik adayıdır. Örneğin epikantus Asya ırkında tamamen normal bir varyasyon iken, Kafkas ırkında Down sendromu veya FAS lehine güçlü bir dismorfik bulgudur.\n- **2. Ailevi Özellik (Familial Trait):** Bebeğin burnundaki hafif eğrilik veya basıklık anne veya babasında da tamamen sağlıklı şekilde varsa bu genetik sendrom değil, 'ailevi varyasyon'dur.\n- **3. Sayısal Kümelenme:** İzole tek bir minör varyasyon normal iken, farklı anatomik bölgelerde birden fazla varyasyonun birikmesi sendrom lehinedir.",
            "coreContent": {
                "table": {
                    "title": "Normal Varyasyon ile Dismorfik Özellik Ayrımı",
                    "headers": ["Parametre", "Normal Ailevi / Etnik Varyasyon", "Patolojik Dismorfik Özellik"],
                    "rows": [
                        ["Popülasyon Sıklığı", "Toplumda yaygın (> %4 - %5)", "Toplumda nadir (< %2 - %4)"],
                        ["Aile Sorgulaması", "Anne veya babada birebir mevcuttur", "Ebeveynlerde yoktur, de novo kümelenir"],
                        ["Etnik Özgüllük", "Bireyin kendi etnik kökeninde olağandır", "Etnik kökene yabancı ve izole bir yapıdır"],
                        ["Eşlik Eden Durum", "İç organ veya gelişimsel kusur eşlik etmez", "Genellikle bilişsel gerilik veya majör kusurla birliktedir"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Normal Varyasyon", "explanation": "Sağlıklı bireylerde görülen, organ fonksiyonunu bozmayan anatomik çeşitlilik."},
                {"term": "Epikantal Katlantı", "explanation": "İç kantal bölgeyi örten deri kıvrımı; Asya toplumlarında fizyolojik, beyaz ırkta sendromik bulgudur."}
            ],
            "spotPearls": [
                "Ebeveynlerin muayenesi dismorfolojide zorunludur; anne veya babada bulunan izole bir özellik sendromik değil ailevi varyasyondur."
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Etnik Varyasyon",
                    "Dismorfik Patolojik Özellik",
                    ["Toplumda sık görülür (>%4)", "Etnik grupta fizyolojiktir (Örn: Asya'da epikantus)", "Tek başınadır, organ hasarı eşlik etmez"],
                    ["Toplumda nadirdir (<%4)", "Etnik yapıya uymaz (Örn: Beyaz ırkta epikantus)", "Farklı bölgelerdeki diğer minör/majörlerle kümelenir"]
                ),
                make_micro_quiz(
                    "Yeni doğan bir bebeğin muayenesinde saptanan bir yüz bulgusunun 'patolojik bir dismorfik anomali' mi yoksa 'normal bir ailevi varyasyon' mu olduğunu ayırt etmede İLK ve EN ETKİLİ klinik adım nedir?",
                    {
                        "A": "Anne ve babanın fizik muayenesini ve yüz fotoğraflarını incelemek",
                        "B": "Hemen tüm genom dizilemesi (WGS) istemek",
                        "C": "Bebeğe kemik iliği biyopsisi yapmak",
                        "D": "Sadece laboratuvar kan biyokimyasına bakmak"
                    },
                    "A",
                    {
                        "A": "Doğru! Ebeveynlerin yüz morfolojisi incelenmeden dismorfolojik tanı konulamaz; ailede bulunan özellikler sendromik olmayabilir.",
                        "B": "Yanlış. Klinik değerlendirme olmadan ileri genetik test istenmez.",
                        "C": "Yanlış. İnvaziv ve endikasyonsuzdur.",
                        "D": "Yanlış. Kan biyokimyası yüz morfolojisinin aileviliğini gösteremez."
                    }
                )
            ]
        },
        {
            "slideNumber": 24,
            "title": "Kraniyofasiyal Muayene: Baş Şekilleri ve Kraniyosinostoz Dinamiği",
            "subtitle": "Kafatası sütürlerinin erken kapanması ve kafa indeksinin değişimi",
            "badge": "Kraniyal Anatomi",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Kafatası şekli, fötal ve neonatal dönemde beyin parankiminin büyümesi ve kafatası kemik sütürlerinin serbestçe genişlemesiyle belirlenir.\n\nSütürlerin erken kaynaşması (kraniyosinostoz) kafa morfolojisini bozar:\n- **Skafosefali / Dolikosefali:** Sagittal sütürün erken kapanmasıyla baş ön-arka eksende aşırı uzar, yanlardan daralır (tekne kafa).\n- **Brakisefali:** Koronal sütürün çift taraflı erken kapanması veya hipoplazi sonucu baş ön-arka eksende çok kısa ve düzdür (Down sendromu).\n- **Plagiosefali:** Koronal veya lambdoid sütürün tek taraflı erken kapanmasıyla ortaya çıkan asimetrik baş şeklidir (yatış pozisyonuna bağlı deformasyonel de olabilir).\n- **Trigonosefali:** Metopik sütürün erken kapanmasıyla alnın üçgen şeklinde sivrilmesidir.",
            "coreContent": {
                "table": {
                    "title": "Kraniyosinostoz Tipleri ve Etkilenen Sütürler",
                    "headers": ["Baş Şekli", "Kapanan Sütür", "Kafa Morfolojisi", "Sık Görülen Durumlar"],
                    "rows": [
                        ["Skafosefali (Dolikosefali)", "Sagittal Sütür (%50-60)", "Uzun, dar 'tekne' kafa", "En sık izole kraniyosinostoz tipidir"],
                        ["Brakisefali", "Bilateral Koronal Sütür", "Ön-arka basık, geniş kafa", "Down Sendromu, Apert Sendromu"],
                        ["Plagiosefali", "Unilateral Koronal / Lambdoid", "Asimetrik kafa tabanı ve yüz", "Pozisyonel deformasyon veya sinostoz"],
                        ["Trigonosefali", "Metopik Sütür", "Alında sivri kemik çıkıntı (üçgen)", "Opitz C sendromu, 9p delesyonu"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Kraniyosinostoz", "explanation": "Kafatası kemiklerini ayıran sütürlerin bir veya birkaçının erken kemikleşerek kapanması."},
                {"term": "Skafosefali", "explanation": "Sagittal sütürün erken kapanması sonucu başın ön-arka eksende uzun, yanlardan basık olması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] En sık görülen izole kraniyosinostoz tipi sagittal sütürün kapanmasıyla oluşan skafosefali (dolikosefali) tablosudur."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Kafa Şekilleri ve Sütür Eşleşme Ezber Tablosu",
                    ["Kafa Şekli", "Erken Kapanan Sütür", "Tipik Morfoloji"],
                    [
                        [("Skafosefali (En Sık)", False), ("Sagittal Sütür", True, "Sagittal"), ("Ön-arka uzun, dar kafa", False)],
                        [("Brakisefali", False), ("Bilateral Koronal", True, "Koronal"), ("Ön-arka yassı, düz oksiput", False)],
                        [("Trigonosefali", False), ("Metopik Sütür", True, "Metopik"), ("Alında üçgen sivrilme", False)]
                    ]
                ),
                make_micro_quiz(
                    "Yenidoğan bir bebekte en sık karşılaşılan izole kraniyosinostoz tipi ve erken kapanan kranial sütür hangisidir?",
                    {
                        "A": "Skafosefali — Sagittal sütür",
                        "B": "Trigonosefali — Metopik sütür",
                        "C": "Plagiosefali — Sfenoparietal sütür",
                        "D": "Oksisefali — Skuamöz sütür"
                    },
                    "A",
                    {
                        "A": "Doğru! İzole kraniyosinostozların %50-60'ı sagittal sütürün erken kapanmasıyla meydana gelen skafosefalidir.",
                        "B": "Yanlış. Trigonosefali daha nadirdir.",
                        "C": "Yanlış. Plagiosefali ikinci sıklıktadır ancak en sık değildir.",
                        "D": "Yanlış. Oksisefali çoklu sütür kapanmasıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 25,
            "title": "Göz Bölgesi Dismorfolojisi: Telekantus, Hipertelorizm ve Hipotelorizm",
            "subtitle": "Kantal mesafe, pupil mesafesi ve orbita kemik mesafesinin objektif ölçümü",
            "badge": "Fasiyal Ölçüm",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Gözler arası mesafenin değerlendirilmesinde klinisyenin göz kararı bakışı yanıltıcı olabilir; cetvelle objektif ölçüm şarttır.\n\nÜç kavram birbiriyle sıkça karıştırılır ve sınavların klasik tuzağıdır:\n- **Telekantus:** İç kantal mesafe (iki gözün iç köşe mesafesi) geniştir ancak orbitanın kemik çatısı ve interpupiller mesafe tamamen NORMALDİR (Örn: Waardenburg sendromu).\n- **Hipertelorizm:** Gerçek orbita kemik mesafesinin artışıdır. Hem iç kantal, hem interpupiller hem de dış kantal mesafeler yaşa göre >97. persentildedir (Örn: Noonan sendromu, Kraniyofasiyal dizostozlar).\n- **Hipotelorizm:** Gözlerin ve orbitanın birbirine anormal derecede yakın olmasıdır; en ağır formu siklopiye kadar giden ==Holoprozensefali== spektrumunun temel bulgusudur.",
            "coreContent": {
                "table": {
                    "title": "Telekantus, Hipertelorizm ve Hipotelorizm Ayırıcı Tanısı",
                    "headers": ["Kavram", "İç Kantal Mesafe", "İnterpupiller Mesafe", "Kemik Orbita Aralığı", "Tipik Sendromik Örnek"],
                    "rows": [
                        ["Telekantus", "Artmış (>97p)", "NORMAL", "NORMAL", "Waardenburg Sendromu"],
                        ["Hipertelorizm", "Artmış (>97p)", "Artmış (>97p)", "Artmış (Geniş Kemik)", "Noonan, Aarskog, DiGeorge"],
                        ["Hipotelorizm", "Azalmış (<3p)", "Azalmış (<3p)", "Azalmış (Yakın Kemik)", "Holoprozensefali, Trizomi 13"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Telekantus", "explanation": "İnterpupiller mesafe normal iken yalnızca iç kantal açılar arası mesafenin artmış olması."},
                {"term": "Hipertelorizm", "explanation": "Kemik orbitanın genişlemesi sonucu hem kantal hem de pupil mesafelerinin artması."}
            ],
            "spotPearls": [
                "📌 [SINAV TUZAĞI] Telekantusta interpupiller mesafe ve kemik orbita aralığı NORMALDİR; gerçek genişleme Hipertelorizmde görülür!"
            ],
            "interactiveElements": [
                make_before_after(
                    "Telekantus",
                    "Hipertelorizm",
                    ["Yalnızca iç kantal mesafe artmıştır", "İnterpupiller mesafe NORMALDİR", "Kemik orbita aralığı NORMALDİR", "Tipik örnek: Waardenburg sendromu"],
                    ["Tüm mesafeler (iç kantal, pupil, dış kantal) artmıştır", "İnterpupiller mesafe ARTMIŞTIR", "Kemik orbita aralığı GENİŞLEMİŞTİR", "Tipik örnek: Noonan ve Kraniyosinostozlar"]
                ),
                make_micro_quiz(
                    "Fizik muayenede iç kantal mesafesi geniş ölçülen bir çocukta interpupiller mesafenin ve kemik orbita aralığının NORMAL olduğunun saptanması durumunda doğru tıbbi terim hangisidir?",
                    {
                        "A": "Telekantus",
                        "B": "Hipertelorizm",
                        "C": "Hipotelorizm",
                        "D": "Mikroftalmi"
                    },
                    "A",
                    {
                        "A": "Doğru! İnterpupiller mesafe normalken sadece iç kantal mesafenin geniş olmasına Telekantus denir.",
                        "B": "Yanlış. Hipertelorizmde interpupiller mesafe ve kemik orbita aralığı da geniştir.",
                        "C": "Yanlış. Hipotelorizmde mesafeler daralmıştır.",
                        "D": "Yanlış. Mikroftalmi göz küresinin küçük olmasıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 26,
            "title": "Palpebral Çatlak Eğimi: Yukarı Çekik ve Aşağı Çekik Gözler",
            "subtitle": "İç kantal ve dış kantal noktaları birleştiren çizginin yatay açısı",
            "badge": "Fasiyal Ölçüm",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Göz kapaklarının açıklığı olan palpebral fissürün yatay düzlemle yaptığı açı, klinik dismorfolojide sendrom ipuçlarının başında gelir.\n\n- **Yukarı Çekik (Upslanting Palpebral Fissures):** Dış kantal açı, iç kantal açıya göre daha yukarıda yer alır. En klasik örneği ==Down Sendromudur== (ayrıca Prader-Willi sendromunda da görülür).\n- **Aşağı Çekik (Downslanting Palpebral Fissures):** Dış kantal açı, iç kantal açının belirgin şekilde altındadır. Malar hipoplazi (elmacık kemiği az gelişimi) ile birliktedir. Tipik örnekleri: ==Treacher Collins Sendromu==, ==Noonan Sendromu== ve ==Sotos Sendromu==dur.\n\n> 💡 **Klinik İpucu:** Her iki gözün iç kantusları arasına çekilen hayali yatay çizgi, dış kantusun nerede durduğunu net olarak gösterir.",
            "coreContent": {
                "table": {
                    "title": "Palpebral Çatlak Eğimine Göre Sendromlar",
                    "headers": ["Palpebral Eğim", "Mekanizma / Eşlik Eden Yapı", "Klasik Sendromik Örnekler"],
                    "rows": [
                        ["Yukarı Çekik (Up-slanting)", "Brakisefali, maksiller hipoplazi", "Down Sendromu (Trizomi 21), Prader-Willi"],
                        ["Aşağı Çekik (Down-slanting)", "Malar kemik hipoplazisi, 1. ve 2. ark defekti", "Treacher Collins, Noonan, Marfan, Rubinstein-Taybi"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Palpebral Fissür", "explanation": "Üst ve alt göz kapakları arasında kalan elips şeklindeki göz açıklığı."},
                {"term": "Treacher Collins", "explanation": "1. ve 2. faringeal ark defekti sonucu malar hipoplazi ve aşağı çekik gözlerle seyreden sendrom."}
            ],
            "spotPearls": [
                "Down sendromunda palpebral fissürler yukarı çekik (up-slanting); Treacher Collins ve Noonan sendromunda ise aşağı çekiktir (down-slanting)."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Aşağıdaki sendromlardan hangisinde tipik olarak AŞAĞI ÇEKİK (down-slanting) palpebral fissürler görülür?",
                    {
                        "A": "Treacher Collins Sendromu",
                        "B": "Down Sendromu (Trizomi 21)",
                        "C": "Prader-Willi Sendromu",
                        "D": "Frajil X Sendromu"
                    },
                    "A",
                    {
                        "A": "Doğru! Treacher Collins sendromunda zigoma ve malar kemik hipoplazisi nedeniyle palpebral fissürler belirgin olarak aşağı çekiktir.",
                        "B": "Yanlış. Down sendromunda gözler yukarı çekiktir (up-slanting).",
                        "C": "Yanlış. Prader-Willi'de badem göz ve hafif yukarı çekiklik görülür.",
                        "D": "Yanlış. Frajil X'te uzun yüz ve büyük kulaklar belirgindir."
                    }
                ),
                make_cloze(
                    "Down sendromunda dış kantal açının iç kantal açıya göre daha yukarıda yer alması durumuna yukarı çekik (up-slanting) palpebral fissür adı verilir.",
                    "yukarı çekik",
                    "Down sendromu tipik göz eğimi"
                )
            ]
        },
        {
            "slideNumber": 27,
            "title": "Kulak Dismorfolojisi: Düşük Kulak (Low-set) ve Posterior Rotasyon",
            "subtitle": "Kafatasındaki embriyolojik göç kusurları ve 15 derecelik rotasyon açısı",
            "badge": "Kulak Anatomisi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Dış kulak embriyogenezde boyun bölgesinden başlar ve mandibula geliştikçe kranial yönde yukarıya doğru göç eder. Fasiyal kemik gelişimi aksadığında kulaklar aşağıda kalır.\n\n- **Düşük Kulak (Low-set Ears):** Her iki gözün dış kantuslarını birleştiren hayali yatay referans çizgisinin kulak heliksinin en üst noktasının (heliks apeksi) ÜSTÜNDE kalmasıdır (normalde heliksin 1/3'ü bu çizginin üstünde olmalıdır).\n- **Posterior Rotasyon:** Dış kulağın dikey aksı normalde yüzün dikey aksına paralel veya en fazla 10-15° geriye eğimlidir. Bu eğim >15° olduğunda 'arkaya rotasyonlu kulak' olarak adlandırılır.\n- **Eşlik Eden Durumlar:** Düşük ve arkaya rotasyonlu kulaklar neredeyse tüm otozomal kromozomal trizomilerin (Down, Edwards, Patau) ve Potter sekansının ortak minör bulgusudur.",
            "medicalTerms": [
                {"term": "Düşük Kulak (Low-set)", "explanation": "Kulak kepçesinin üst sınırının kantal yatay referans çizgisinin altında kalması."},
                {"term": "Posterior Rotasyon", "explanation": "Kulak dikey aksının geriye doğru 15 dereceden fazla açılanması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Düşük kulak saptanabilmesi için gözün dış kantusundan çekilen yatay çizginin, kulağın heliks tepesinin yukarısından geçmesi gerekir."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kulak Göçü ve Düşük Kulak Patogenezi",
                    [
                        "Embriyolojik 6. haftada aurikula taslakları servikal (boyun) bölgede belirir.",
                        "1. ve 2. faringeal arklardan köken alan 6 adet His tepesi (auricular hillocks) birleşir.",
                        "Mandibulanın öne ve aşağı büyümesiyle kulak kraniyofasiyal düzlemde yukarıya tırmanır.",
                        "Mandibula ve kranium hipoplazisinde göç duraklar; kulaklar düşük (low-set) ve arkaya rotasyonlu kalır."
                    ]
                ),
                make_micro_quiz(
                    "Bir bebeğin fizik muayenesinde kulağın 'düşük yerleşimli' (low-set ear) kabul edilebilmesi için anatomik referans hattı nasıl olmalıdır?",
                    {
                        "A": "Göz dış kantusundan geçen yatay çizginin kulak heliksinin en üst noktasının üzerinden geçmesi",
                        "B": "Kulağın tragusunun burun kanadı ile aynı hizada olması",
                        "C": "Kulak memesinin klavikula kemiğine temas etmesi",
                        "D": "Kulak kepçesinin kafa derisine tamamen yapışık olması"
                    },
                    "A",
                    {
                        "A": "Doğru! Dış kantustan çekilen yatay çizgi heliksin üzerinden geçiyorsa (kulak çizginin altında kalıyorsa) düşük kulak tanısı konur.",
                        "B": "Yanlış. Referans noktası tragus değil dış kantus ve heliks apeksidir.",
                        "C": "Yanlış. Bu aşırı bir tanımlamadır.",
                        "D": "Yanlış. Bu yapışık kulak memesidir, yerleşim yüksekliği değildir."
                    }
                )
            ]
        },
        {
            "slideNumber": 28,
            "title": "Burun, Filtrum ve Ağız Dismorfolojisi: FAS ve Sendromik İpuçları",
            "subtitle": "Kısa burun, antevert burun delikleri, silik filtrum ve ince üst dudak",
            "badge": "Fasiyal Örüntü",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Orta yüz bölgesi, nöral krest hücrelerinin göçüne ve embriyonik frontonazal çıkıntıların birleşmesine doğrudan bağımlıdır.\n\n- **Düz Burun Kökü (Depressed Nasal Bridge):** Burun kemiğinin hipoplazisidir; Down sendromu ve Akondroplazide çok belirgindir.\n- **Antevert Burun Delikleri (Upturned Nose):** Burun ucunun yukarı kalkık olması ve deliklerin karşıdan bakışta görünmesidir (Smith-Lemli-Opitz).\n- **Filtrum ve Üst Dudak Anomalisi:** Burun tabanı ile üst dudak kırmızı çizgisi arasındaki oluk filtrumdur. ==Silik / Düz Filtrum== ve ==İnce Üst Dudak (Vermilion)== Fetal Alkol Sendromunun (FAS) kardinal tanısal bulgusudur.\n- **Mikrognati ve Çene:** Küçük alt çene mikrognatidir; Pierre Robin sekansında dilin geriye kaymasına (glossozis) ve yarık damağa yol açar.",
            "coreContent": {
                "table": {
                    "title": "Orta Yüz Dismorfolojik Belirteçleri",
                    "headers": ["Fasiyal Yapı", "Anormal Tanımlama", "Klasik Sendrom"],
                    "rows": [
                        ["Burun Kökü", "Düz / Basık (Depressed bridge)", "Down Sendromu, Akondroplazi, Williams"],
                        ["Filtrum", "Tamamen düz / silik (Smooth philtrum)", "Fetal Alkol Sendromu (FAS)"],
                        ["Üst Dudak", "Çok ince kırmızı çizgi (Thin vermilion)", "Fetal Alkol Sendromu (FAS)"],
                        ["Alt Çene", "Şiddetli küçük çene (Mikrognati)", "Pierre Robin Sekansı, Treacher Collins"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Filtrum", "explanation": "Burun kökü altı ile üst dudak çizgisi arasında uzanan anatomik dikey oluk."},
                {"term": "Mikrognati", "explanation": "Alt çenenin (mandibula) normalden belirgin olarak küçük ve yetersiz gelişmiş olması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Düz/silik filtrum + çok ince üst dudak (vermilion) kombinasyonu Fetal Alkol Sendromunun (FAS) en tipik fasiyal belirtecidir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Fizik muayenesinde mikrosefali, boy kısalığı, düz silik filtrum ve çok ince üst dudak (thin vermilion) saptanan bir bebekte öncelikle hangi teratojenik sendrom düşünülmelidir?",
                    {
                        "A": "Fetal Alkol Sendromu (FAS)",
                        "B": "Talidomid Embriyopatisi",
                        "C": "Konjenital Rubella Sendromu",
                        "D": "Valproik Asit Sendromu"
                    },
                    "A",
                    {
                        "A": "Doğru! Silik filtrum ve ince üst dudak Fetal Alkol Sendromunun (FAS) en patognomonik yüz stigmalarıdır.",
                        "B": "Yanlış. Talidomidin ana bulgusu fokomeli (ekstremite yokluğu) tablosudur.",
                        "C": "Yanlış. Rubella katarakt, PDA ve sağırlık yapar.",
                        "D": "Yanlış. Valproat trigonosefali ve bifid uvula ile seyreder."
                    }
                ),
                make_cloze(
                    "Fetal Alkol Sendromunda (FAS) üst dudak ile burun tabanı arasındaki anatomik oluğun kaybolmasına silik / düz filtrum adı verilir.",
                    "silik / düz filtrum",
                    "FAS kardinal fasiyal bulgusu"
                )
            ]
        },
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Kraniyofasiyal Dismorfoloji ve Ayırıcı Tanı Matrisi",
            "subtitle": "Kafa, göz, kulak ve orta yüz belirteçlerinin eksiksiz sentez tablosu",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu tekrar modülü, Bölüm 3'te öğrenilen kraniyofasiyal muayene terminolojisini, kafa sütürlerini ve sendromik göz-kulak-yüz örüntülerini kalıcı hafızaya kazımak için oluşturulmuştur.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Skafosefali:** En sık kraniyosinostoz; ==Sagittal sütür== erken kapanır (tekne kafa).\n- **Brakisefali:** Koronal sütürler kapanır veya hipoplaziktir; ön-arka eksende yassı kafadır (Down sendromu).\n- **Telekantus vs Hipertelorizm:** Telekantusta interpupiller mesafe ve kemik ==NORMALDİR==; Hipertelorizmde tüm mesafeler ==ARTMIŞTIR==.\n- **Palpebral Çatlak:** Down sendromunda ==Yukarı Çekik==; Treacher Collins ve Noonan'da ==Aşağı Çekik==.\n- **Düşük Kulak:** Dış kantus yatay çizgisi heliks tepesinin ==ÜSTÜNDEDİR==.\n- **FAS Yüzü:** Düz/silik filtrum + İnce üst dudak + Kısa burun.",
            "coreContent": {
                "table": {
                    "title": "Kraniyofasiyal Belirteçler Büyük Ayırıcı Tanı Tablosu",
                    "headers": ["Anatomik Bölge", "Klinik Terim", "Ayırt Edici Özellik", "Karakteristik Sendrom"],
                    "rows": [
                        ["Kafatası", "Skafosefali", "Sagittal sütür kapanması (en sık)", "İzole kraniyosinostoz"],
                        ["Kafatası", "Brakisefali", "Ön-arka kısalık, yassı oksiput", "Down Sendromu, Apert"],
                        ["Göz Aralığı", "Telekantus", "Sadece iç kantal mesafe geniş, pupiller normal", "Waardenburg Sendromu"],
                        ["Göz Aralığı", "Hipertelorizm", "Kemik orbita ve pupiller mesafe artmış", "Noonan, Kraniyofasiyal sendromlar"],
                        ["Göz Eğimi", "Yukarı Çekik", "Dış kantus iç kantustan yukarıda", "Down Sendromu"],
                        ["Göz Eğimi", "Aşağı Çekik", "Dış kantus iç kantustan aşağıda", "Treacher Collins, Noonan"],
                        ["Orta Yüz", "Düz Filtrum & İnce Dudak", "Burun-dudak oluğu silik, vermilion dar", "Fetal Alkol Sendromu (FAS)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Skafosefali", "explanation": "Sagittal sütürün erken kapanmasıyla oluşan ön-arka eksende uzun dar kafa biçimi."},
                {"term": "Telekantus", "explanation": "Pupil aralığı ve kemik orbita normalken iç kantuslar arası mesafenin geniş olması."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] Telekantus: Kemik normal | Hipertelorizm: Kemik geniş | Hipotelorizm: Kemik dar.",
                "📌 [TEKRAR SPOTU] Silik filtrum ve ince üst dudak = FAS; Aşağı çekik göz = Treacher Collins; Yukarı çekik göz = Down sendromu."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Kraniyofasiyal Dismorfoloji Sentez ve Ezber Tablosu",
                    ["Muayene Alanı", "Patolojik Bulgu", "Karakteristik Sendrom"],
                    [
                        [("En Sık Kranial Sinostoz", False), ("Skafosefali (Sagittal)", True, "Sagittal"), ("İzole kranial deformite", False)],
                        [("Göz Mesafesi (Kemik Normal)", False), ("Telekantus", True, "İç kantal geniş"), ("Waardenburg Sendromu", True, "Waardenburg")],
                        [("Göz Eğimi (Yukarı Çekik)", False), ("Up-slanting Palpebral", True, "Yukarı eğim"), ("Down Sendromu", True, "Trizomi 21")],
                        [("Göz Eğimi (Aşağı Çekik)", False), ("Down-slanting Palpebral", True, "Aşağı eğim"), ("Treacher Collins / Noonan", True, "Malar hipoplazi")],
                        [("Orta Yüz (Düz Filtrum)", False), ("Smooth Philtrum + İnce Dudak", True, "FAS yüzü"), ("Fetal Alkol Sendromu", True, "FAS")]
                    ]
                ),
                make_micro_quiz(
                    "Fizik muayenesinde telekantus, işitme kaybı ve gözlerinde heterokromi (farklı göz renkleri) saptanan bir hastada en olası genetik sendrom hangisidir?",
                    {
                        "A": "Waardenburg Sendromu",
                        "B": "Down Sendromu",
                        "C": "Treacher Collins Sendromu",
                        "D": "Fetal Alkol Sendromu"
                    },
                    "A",
                    {
                        "A": "Doğru! Nöral krest melanosit göç bozukluğu olan Waardenburg sendromunda telekantus, iris heterokromisi ve sensorinöral işitme kaybı klasiktir.",
                        "B": "Yanlış. Down sendromunda yukarı çekik göz ve epikantus vardır.",
                        "C": "Yanlış. Treacher Collins'te aşağı çekik göz ve iletim tipi işitme kaybı vardır.",
                        "D": "Yanlış. FAS'ta silik filtrum ve mikrosefali görülür."
                    }
                ),
                make_micro_quiz(
                    "Sagittal sütürün intrauterin dönemde erkenden kemikleşip kapanması sonucunda ortaya çıkan tekne kafa deformitesine ne ad verilir?",
                    {
                        "A": "Skafosefali (Dolikosefali)",
                        "B": "Brakisefali",
                        "C": "Trigonosefali",
                        "D": "Plagiosefali"
                    },
                    "A",
                    {
                        "A": "Doğru! Sagittal sütür erken kapandığında baş yanlara büyüyemez, ön-arka eksende aşırı uzayarak skafosefali (tekne kafa) tablosu oluşur.",
                        "B": "Yanlış. Brakisefali koronal sütür kapanmasıdır.",
                        "C": "Yanlış. Trigonosefali metopik sütür kapanmasıdır.",
                        "D": "Yanlış. Plagiosefali asimetrik kafa deformitesidir."
                    }
                )
            ]
        }
    ]
