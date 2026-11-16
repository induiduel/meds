# -*- coding: utf-8 -*-
from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_steps():
    return [
        {
            "slideNumber": 50,
            "title": "Nekrozun Sitoplazmik Morfolojisi: Artmış Eozinofili",
            "subtitle": "Denatüre proteinler, RNA kaybı ve koyu pembe boyanma mekanizması",
            "badge": "Histopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Rutin patoloji kesitlerinde hematoksilen-eozin (H&E) ile boyanmış bir dokuda nekrotik "
                "hücreleri canlı hücrelerden ayıran en çarpıcı sitoplazmik bulgu 'artmış eozinofili'dir. "
                "Nekroza uğrayan hücreler canlı komşularına kıyasla çok daha parlak, koyu pembe-kırmızı "
                "bir renkte görünür. Bu eozinofili artışı iki temel biyokimyasal olaya dayanır.\n\n"
                "> [SINAV SPOTU] 1) Denatüre olan sitoplazmik proteinler eozin boyasını çok daha güçlü bağlar, "
                "2) Sitoplazmadaki RNA molekülleri ribonükleazlarla yıkıldığı için normal bazofilik (mavi) ton kaybolur.\n\n"
                "Bazofilinin kaybı ve eozin affinitesinin artışı, mikroskop altında ölü hücrelerin canlı "
                "dokudan adeta alev gibi parlayarak ayrılmasını sağlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Protein Denatürasyonu", "desc": "Pıhtılaşan proteinlerin asidik eozin boyasını aşırı miktarda tutmasıdır.", "isKey": True},
                    {"title": "RNA Kaybı", "desc": "Sitoplazmaya mavi (bazofilik) rengi veren ribozomal RNA'nın erimesidir.", "isKey": True},
                    {"title": "Görsel Kontrast", "desc": "Canlı hücrelerin soluk pembeliğine karşı nekrotik hücrelerin koyu cam pembeliğidir.", "isKey": False}
                ],
                "table": {
                    "title": "Eozinofili Artışının Biyokimyasal Nedenleri",
                    "headers": ["Bileşen", "Normal Hücrede Durum", "Nekrotik Hücrede Değişim"],
                    "rows": [
                        ["Sitoplazmik Proteinler", "Doğal katlanmış, normal eozin tutulumu", "Denatüre olmuş, eozin bağlama kapasitesi masif artmış"],
                        ["Ribozomal RNA (rRNA)", "Sitoplazmada bol, bazofili (mavilik) verir", "RNaz enzimleri tarafından tamamen parçalanmış (kayıp)"],
                        ["Genel Boyanma Rengi", "Hafif morumsu-pembe (amfofilik)", "Homojen, parlak, koyu kırmızı-pembe (hiperozeinofilik)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozda sitoplazmanın artmış eozinofili göstermesinin iki nedeni: Denatüre proteinlerin eozini fazla bağlaması ve RNA kaybıdır.",
                "📌 [YÜKSEK VERİM] Sitoplazmadaki RNA normalde bazofilik (mavi) boyanma sağlar; RNA kaybı sitoplazmayı saf pembe eozinofil yapar."
            ],
            "medicalTerms": [
                {"term": "Eozinofili", "explanation": "Asidik bir boya olan eozinin bazik proteinlere bağlanarak pembe-kırmızı renk vermesidir."},
                {"term": "Bazofili", "explanation": "Bazik boya olan hematoksilenin nükleik asitlere bağlanarak mavi-mor renk vermesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Sitoplazma Boyanma Mekanizması",
                    "Canlı Hücre Sitoplazması",
                    "Nekrotik Hücre Sitoplazması",
                    [
                        "Doğal katlanmış proteinler vardır",
                        "Ribozomal RNA aktiftir",
                        "Hematoksilen kısmen tutunur (mavimsi ton)",
                        "Normal pembe-mor amfofilik görünüm"
                    ],
                    [
                        "Proteinler asidozla denatüre olmuştur",
                        "RNA enzimatik olarak parçalanmıştır",
                        "Eozin boyası masif bağlanır",
                        "Parlak, homojen, koyu kırmızı-pembe görünüm"
                    ]
                ),
                make_cloze(
                    "Nekrozda sitoplazmanın daha koyu pembe boyanmasının nedeni protein denatürasyonu ve sitoplazmik RNA kaybıdır.",
                    "RNA kaybıdır",
                    "Biyokimyasal Neden"
                )
            ]
        },
        {
            "slideNumber": 51,
            "title": "Camsı (Glassy) Homojen Sitoplazma ve Glikojen Kaybı",
            "subtitle": "Glikojen depolarının tükenmesi ve sitoplazmik pürüzsüzleşme",
            "badge": "Histopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Canlı hücrelerin sitoplazması organeller, protein granülleri ve glikojen partikülleri "
                "nedeniyle ince granüllü ve hafif pürüzlü bir dokuya sahiptir. Ancak nekrotik hücreler "
                "incelendiğinde bu ince granülasyonun tamamen kaybolduğu ve sitoplazmanın pürüzsüz, 'camsı' "
                "(glassy) homojen bir görünüm aldığı izlenir.\n\n"
                "> [TEMEL İLKE] İskemi sırasında anaerobik glikoliz glikojen partiküllerini tamamen tüketir; "
                "proteinlerin de pıhtılaşarak tek bir blok oluşturması sitoplazmaya camsı homojenlik kazandırır.\n\n"
                "PAS (Periyodik Asit-Schiff) boyası uygulandığında, canlı hücreler glikojen nedeniyle mor "
                "boyanırken nekrotik hücreler glikojen depolarını tükettiği için boyanmaz."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Glikojen Tüketimi", "desc": "Anaerobik glikolizle intraselüler glikojen granüllerinin sıfırlanmasıdır.", "isKey": True},
                    {"title": "Camsı Görünüm", "desc": "Pıhtılaşan proteinlerin optik olarak homojen ve pürüzsüz bir alan oluşturmasıdır.", "isKey": True},
                    {"title": "PAS Negatifliği", "desc": "Nekrotik hücrelerin glikojen boyası tutmayarak canlılardan ayrılmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Sitoplazmik Granülasyon Karşılaştırması",
                    "headers": ["Parametre", "Canlı Hücre", "Nekrotik Hücre"],
                    "rows": [
                        ["Sitoplazmik Doku", "İnce granüllü, pürüzlü", "Camsı, parlak, tamamen homojen"],
                        ["Glikojen Varlığı", "Bol (sitoplazmik partiküller)", "Tükenmiş (PAS boyası negatif)"],
                        ["Organel Durumu", "Ayrı ayrı organel sınırları", "Koagüle olmuş tek parça protein kitlesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrotik hücrelerin sitoplazmasının 'camsı homojen' görünmesinin temel nedeni glikojen kaybı ve protein koagülasyonudur.",
                "📌 [YÜKSEK VERİM] Glikojen anaerobik glikolizin ilk dakikalarında ATP üretmek için hızla tüketilir."
            ],
            "medicalTerms": [
                {"term": "Camsı (Glassy) Görünüm", "explanation": "Granüler yapısını kaybedip pürüzsüz ve tekdüze boyanan sitoplazmik görüntüdür."},
                {"term": "PAS Boyası", "explanation": "Periyodik Asit-Schiff; dokudaki glikojen ve bazal membran karbonhidratlarını parlak macenta boyar."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Nekrotik hücrelerde sitoplazmanın camsı ve homojen görünüm almasında glikojen partiküllerinin kaybı kritik rol oynar.",
                    "glikojen partiküllerinin kaybı",
                    "Sitoplazmik Kayıp"
                ),
                make_active_recall(
                    "Canlı bir karaciğer hücresi ile nekrotik bir karaciğer hücresi PAS boyası ile nasıl ayırt edilir?",
                    "Canlı hepatositler zengin glikojen depoları nedeniyle PAS boyasında parlak eflatun/pembe boyanır; nekrotik hepatositler ise glikojeni tükettiği için boyanmaz ve soluk kalır."
                )
            ]
        },
        {
            "slideNumber": 52,
            "title": "Sitoplazmik Vakuolizasyon: Güve Yeniği Görünümü",
            "subtitle": "Sindirilmiş organellerin oluşturduğu sitoplazmik mikro-kaviteler",
            "badge": "Histopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Nekroz ilerledikçe otolitik lizozomal enzimler belirli organel kümelerini sindirip eritir. "
                "Eriyen mitokondri ve endoplazmik retikulum bölgeleri sitoplazmada geride optik olarak "
                "boşluklar bırakır. Bu durum nekrotik sitoplazmanın yer yer 'vakuolize' ve delik deşik "
                "bir görünüm almasına yol açar.\n\n"
                "> [TEMEL İLKE] Bu mikroskobik morfolojiye patolojide 'güve yeniği' (moth-eaten) görünümü "
                "adı verilir; organellerin enzimatik lizisini temsil eder.\n\n"
                "Hidropik şişmedeki düzenli su vakuollerinin aksine, nekrozdaki vakuoller düzensiz, parçalı "
                "ve lizis alanlarına karşılık gelen şekilsiz kavitelerdir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Güve Yeniği", "desc": "Sitoplazmada lizozomal sindirim sonucu açılan düzensiz mikro-deliklerdir.", "isKey": True},
                    {"title": "Organel Sindirimi", "desc": "Otolitik hidrolazların organel adacıklarını eritmesidir.", "isKey": True},
                    {"title": "İleri Evre Göstergesi", "desc": "Membran parçalanmasının ve enzimatik erimenin ilerlediğini gösterir.", "isKey": False}
                ],
                "table": {
                    "title": "Sitoplazmik Boşlukların Ayırıcı Tanısı",
                    "headers": ["Lezyon", "Vakuol Niteliği", "İçerik ve Anlam"],
                    "rows": [
                        ["Hidropik Şişme", "Düzenli, yuvarlak, berrak", "Genişlemiş ER sisternaları (Su birikimi)"],
                        ["Steatoz", "Tek veya çoklu küresel vakuol", "Nötral trigliserit lipit damlacıkları"],
                        ["Nekrotik Vakuolizasyon", "Düzensiz, parçalı, güve yeniği", "Sindirilmiş organel kalıntıları (Otoliz)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrotik hücre sitoplazmasında izlenen güve yeniği (moth-eaten) görünümü, lizozomal enzimlerin organelleri sindirmesini yansıtır.",
                "📌 [YÜKSEK VERİM] Bu vakuoller hücresel şişmedeki su vakuolleriyle karıştırılmamalıdır; nekroza özgü litik boşluklardır."
            ],
            "medicalTerms": [
                {"term": "Güve Yeniği Görünümü", "explanation": "Sitoplazmik organellerin enzimatik sindirimiyle oluşan düzensiz mikro-kaviter deliklerdir."},
                {"term": "Kaviter Lizis", "explanation": "Hücre veya doku parçalarının eriyerek yerinde boş kaviteler bırakmasıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Nekrotik hücre sitoplazmasında organellerin lizozomal sindirimi sonucu oluşan delikli morfolojiye güve yeniği görünümü denir.",
                    "güve yeniği",
                    "Histolojik Patern"
                ),
                make_active_recall(
                    "Nekrozun sitoplazmik morfolojisindeki 3 ana bulgu nedir?",
                    "1) Artmış eozinofili (protein denatürasyonu + RNA kaybı), 2) Camsı homojen görünüm (glikojen kaybı), 3) Sitoplazmik vakuolizasyon / güve yeniği görünümü (organel sindirimi)."
                )
            ]
        },
        {
            "slideNumber": 53,
            "title": "Miyelin Figürleri ve Distrofik Kalsifikasyon Başlangıcı",
            "subtitle": "Fosfolipid sarmalları, yağ asitleri ve kalsiyum sabunlaşması",
            "badge": "Kalsifikasyon",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Parçalanan hücre zarları ve organel membranları fosfolipidlerden son derece zengindir. "
                "Bu fosfolipidler sulu sitozol ortamında kendiliğinden konsantrik lameller sarmallar "
                "halinde kümelenir; elektron mikroskobunda sinir miyelin kılıfına benzediği için bunlara "
                "'miyelin figürleri' denir.\n\n"
                "> [TEMEL İLKE] Miyelin figürleri zamanla parçalanarak yağ asitlerine ayrışır; açığa çıkan "
                "serbest yağ asitleri ekstraselüler kalsiyumu bağlayarak kalsiyum sabunları oluşturur.\n\n"
                "Bu sabunlar üzerine kalsiyum fosfat ve hidroksiapatit kristalleri çöker; bu süreç nekrotik "
                "dokuda serum kalsiyumu normal olduğu halde gelişen 'distrofik kalsifikasyon'un başlangıcıdır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Miyelin Figürleri", "desc": "Parçalanmış hücre membranlarının oluşturduğu konsantrik fosfolipid sarmallarıdır.", "isKey": True},
                    {"title": "Yağ Asidi Açığa Çıkışı", "desc": "Fosfolipidlerin parçalanarak serbest yağ asitlerine dönüşmesidir.", "isKey": True},
                    {"title": "Distrofik Kalsifikasyon", "desc": "Ölü dokudaki kalsiyum sabunlarının hidroksiapatite kristalleşmesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Membran Kalıntılarından Kalsifikasyona Giden Yol",
                    "headers": ["Aşama", "Kimyasal Yapı", "Morfolojik Görünüm"],
                    "rows": [
                        ["1. Membran Parçalanması", "Fosfolipid çift tabaka rüptürü", "Miyelin figürleri (EM'de soğan zarı)"],
                        ["2. Yağ Asidi Salınımı", "Fosfolipaz etkisiyle serbest yağ asitleri", "Amorf lipid agregatları"],
                        ["3. Sabunlaşma", "Kalsiyum + Yağ Asidi kompleksi", "Kalsiyum sabunları"],
                        ["4. Distrofik Kalsifikasyon", "Kalsiyum fosfat (Hidroksiapatit)", "H&E'de koyu mavi-mor bazofilik amorf çökeltiler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyelin figürleri, hasarlı hücre ve organel membranlarından türeyen konsantrik fosfolipid kümeleridir.",
                "📌 [SINAV SPOTU] Nekrotik hücrelerde yağ asitlerinin kalsiyumla birleşmesi distrofik kalsifikasyonun çekirdeğini oluşturur."
            ],
            "medicalTerms": [
                {"term": "Miyelin Figürü", "explanation": "Nekrotik hücre membranlarından kopan fosfolipidlerin oluşturduğu sarmal lameller yapılardır."},
                {"term": "Sabunlaşma (Saponifikasyon)", "explanation": "Serbest yağ asitlerinin kalsiyum iyonlarıyla birleşerek erimeyen kalsiyum sabunları oluşturmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Membran Hasarından Kalsifikasyona Gidiş Zinciri",
                    [
                        "1. Membran Lizisi: Plazma ve organel membranları parçalanır.",
                        "2. Miyelin Figürleri: Fosfolipidler konsantrik lameller oluşturarak toplanır.",
                        "3. Yağ Asidi Ayrışması: Fosfolipazlar lipidleri parçalayarak serbest yağ asitleri üretir.",
                        "4. Kalsiyum Bağlanması: Yağ asitleri kalsiyum iyonlarını çöktürerek sabunlar oluşturur.",
                        "5. Distrofik Kalsifikasyon: Hidroksiapatit kristalleri birikerek nekrotik alanı taşlaştırır."
                    ]
                ),
                make_cloze(
                    "Nekrotik dokularda parçalanan membran fosfolipidlerinin oluşturduğu konsantrik sarmal yapılara miyelin figürleri denir.",
                    "miyelin figürleri",
                    "Ultrastrüktürel Yapı"
                )
            ]
        },
        {
            "slideNumber": 54,
            "title": "Nekrozun Elektron Mikroskobundaki Temel Bulguları",
            "subtitle": "Membran süreksizlikleri, matriks amorf çökeltileri ve lizozom rüptürü",
            "badge": "Ultrastrüktür",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Transmisyon elektron mikroskobisi (TEM), nekrozun erken evrelerindeki yıkıcı değişiklikleri "
                "ışık mikroskobundan çok önce netleştirir. Nekroza uğramış bir hücrenin elektron mikroskobik "
                "özellikleri geri dönüşümlü hasardan tamamen farklıdır. En belirgin bulgu hücre zarında "
                "geniş 'süreksizlikler' (yırtıklar ve delikler) görülmesidir.\n\n"
                "> [TEMEL İLKE] Mitokondriler ileri derecede şişmiştir ve matrikslerinde kalsiyum ve "
                "protein içeren büyük amorf yoğunluklar bulunur; lizozom zarları tamamen parçalanmıştır.\n\n"
                "Endoplazmik retikulum zarları lize olmuş, nükleer membran çift tabakası aralanmış ve "
                "sitoplazma içinde serbest miyelin figürleri dağılmıştır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Zar Süreksizliği", "desc": "Plazma membranında açık delik ve yırtıkların TEM ile gösterilmesidir.", "isKey": True},
                    {"title": "Amorf Yoğunluklar", "desc": "Mitokondri matriksinde kalsiyum çökelmesiyle oluşan koyu odaklardır.", "isKey": True},
                    {"title": "Lizozom Rüptürü", "desc": "Litil enzim paketlerinin sitoplazmaya tamamen boşalmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "EM'de Geri Dönüşümlü vs Nekrotik Organeller",
                    "headers": ["Organel", "Geri Dönüşümlü Hasar", "Nekroz (Geri Dönüşümsüz)"],
                    "rows": [
                        ["Plazma Zarı", "Blebler var, membran devamlılığı tam", "Geniş membran delikleri ve süreksizlikler"],
                        ["Mitokondriler", "Hafif şişme, kristalar korunmuş", "Masif şişme, krista lizisi, amorf yoğunluklar"],
                        ["Lizozomlar", "Zar sağlam, enzimler içeride hapis", "Zar rüptüre, enzimler sitozole saçılmış"],
                        ["Hücre Çekirdeği", "Kromatin hafif kümelenmiş", "Piknoz, karyoreksis veya tam nükleer lizis"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozun elektron mikroskobu bulguları: Plazma zarı süreksizlikleri, mitokondride amorf yoğunluklar ve lizozom rüptürüdür.",
                "📌 [YÜKSEK VERİM] Geri dönüşümlü hasarda membran devamlılığı korunurken nekrozda zarda fiziksel kopmalar (süreksizlik) vardır."
            ],
            "medicalTerms": [
                {"term": "Membran Süreksizliği", "explanation": "Hücre zarındaki lipid çift tabakanın anatomik bütünlüğünü kaybedip yırtılmasıdır."},
                {"term": "Matriks Yoğunluğu", "explanation": "Mitokondri içinde ağır hasar sonucu çöken kalsiyum ve protein agregatlarıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "EM Organel Bulguları",
                    ["Organel", "Hasar Tipi", "Karakteristik Görünüm"],
                    [
                        [("Plazma Zarı", False), ("Geniş delinmeler", True, "Membran Yırtığı"), ("Membran süreksizliği", False)],
                        [("Mitokondri", False), ("Büyük elektron-yoğun çökelti", True, "Kalsiyum Birikimi"), ("Amorf yoğunluklar", False)],
                        [("Lizozom", False), ("Litik enzim sızıntısı", True, "Asit Hidrolaz"), ("Lizozomal rüptür", False)],
                        [("Membran Artığı", False), ("Konsantrik fosfolipid sarmalı", True, "Lipid Tabakası"), ("Miyelin figürleri", False)]
                    ]
                ),
                make_cloze(
                    "Nekrozun elektron mikroskobundaki en belirgin membranöz bulgusu plazma zarında geniş membran süreksizliklerinin izlenmesidir.",
                    "membran süreksizliklerinin",
                    "Zar Kusuru"
                )
            ]
        },
        {
            "slideNumber": 55,
            "title": "Nekrozun Sitoplazmik Bulgularının Sentezi",
            "subtitle": "Eozinofili, homojenlik, vakuoller ve sabunlaşmanın tam tablosu",
            "badge": "Sentez",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Nekroza uğrayan bir hücrenin sitoplazması, canlı bir hücreden tamamen farklı bir biyofiziksel "
                "ve kimyasal ortama dönüşür. Bir patoloğun mikroskopta nekrozu anında tanımasını sağlayan "
                "tüm sitoplazmik ipuçları bir araya geldiğinde tablo tamamlanır: 1) Koyu pembe artmış "
                "eozinofili, 2) Glikojen yokluğuna bağlı camsı homojenlik, 3) Organel sindirimine bağlı "
                "güve yeniği vakuolizasyonu, 4) Yağ asidi sabunlaşması.\n\n"
                "> [TEMEL İLKE] Bu değişikliklerin tümü, enzimatik otoliz ile kimyasal protein denatürasyonunun "
                "aynı anda ve birbiriyle yarışarak gerçekleşmesinin doğal morfolojik sonucudur.\n\n"
                "Artık bu sitoplazma metabolik bir makine değil; lökositleri uyaran bir kimyasal enkazdır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Artmış Eozinofili", "desc": "Denatüre proteinler + RNA kaybının yarattığı koyu pembe renktir.", "isKey": True},
                    {"title": "Camsı Homojenlik", "desc": "Glikojen depolarının erimesiyle oluşan pürüzsüzlüktür.", "isKey": True},
                    {"title": "Güve Yeniği", "desc": "Otolitik enzimlerin organelleri eritip boşluklar açmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Sitoplazmik Nekroz Bulguları Matrisi",
                    "headers": ["Morfolojik Bulgu", "Görülen Mikroskobik Resim", "Altta Yatan Biyokimya"],
                    "rows": [
                        ["Artmış Eozinofili", "Parlak koyu pembe/kırmızı boyanma", "Protein denatürasyonu + Ribozomal RNA kaybı"],
                        ["Camsı Görünüm", "Pürüzsüz homojen sitoplazma", "Glikojen partiküllerinin tükenmesi"],
                        ["Vakuolizasyon", "Güve yeniği şeklinde delikler", "Lizozomal enzimlerle organel sindirimi"],
                        ["Miyelin Figürleri", "Soğan zarı lamelleri (EM)", "Fosfolipidlerin sulu ortamda kümeleşmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrotik hücre sitoplazmasının 3 kardinal bulgusu: Artmış eozinofili, camsı homojen görünüm ve vakuolizasyondur (güve yeniği).",
                "📌 [YÜKSEK VERİM] Eozinofili artışı denatüre proteinlere eozin bağlanması ve bazofilik RNA'nın kaybı ile açıklanır."
            ],
            "medicalTerms": [
                {"term": "Kardinal Bulgu", "explanation": "Bir hastalığı veya patolojik tabloyu kesin olarak tanımlayan en temel belirtidir."},
                {"term": "Amfofilik", "explanation": "Hem asidik (eozin) hem de bazik (hematoksilen) boyaları dengeli tutarak morumsu-pembe boyanmadır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Nekrozda sitoplazmanın camsı homojen görünüm almasının nedeni glikojen partiküllerinin tükenmesidir.",
                    "glikojen partiküllerinin tükenmesidir",
                    "Metabolik Neden"
                ),
                make_active_recall(
                    "Canlı hücre sitoplazması amfofilik (morumsu) boyanırken nekrotik hücre sitoplazması neden saf kırmızı-pembe (eozinofilik) boyanır?",
                    "Canlı hücrede bol miktarda ribozomal RNA vardır ve bu nükleik asit hematoksileni tutarak mavi ton verir; nekrozda RNA eritildiği ve proteinler pıhtılaştığı için mavi ton kaybolur ve eozin baskın hale gelir."
                )
            ]
        },
        {
            "slideNumber": 56,
            "title": "Nekrozda Nükleer Değişiklikler: Evrensel 3 Basamak",
            "subtitle": "Piknoz, karyoreksis ve karyolizis mekanizmaları",
            "badge": "Nükleer Değişiklikler",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patolojide hücre ölümünün en kesin, en güvenilir ve tartışmasız kanıtı NÜKLEUSUN (çekirdeğin) "
                "morfolojik değişikliğidir. Sitoplazmik değişiklikler bazen yanıltıcı veya artefakt "
                "olabilirken, nükleer değişiklikler hücrenin geri dönüşümsüz olarak öldüğünü belgeler. "
                "Nekroza uğrayan bir hücrenin çekirdeği istisnasız üç evreden biri veya ardışık akışıyla parçalanır.\n\n"
                "> [SINAV SPOTU] Nekrozun 3 klasik nükleer değişikliği: 1) Piknoz (çekirdeğin büzülmesi), "
                "2) Karyoreksis (çekirdeğin parçalanması), 3) Karyolizis (çekirdeğin erimesi ve solmasıdır).\n\n"
                "Bu üç aşama endonükleaz enzimlerinin DNA'yı ve nükleoproteinleri parçalama derecesini yansıtır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "1. Piknoz", "desc": "Kromatinin aşırı büzüşerek yoğun siyah bir kitleye dönmesidir.", "isKey": True},
                    {"title": "2. Karyoreksis", "desc": "Piknotik çekirdeğin ufalanarak 'nükleer toz' oluşturmasıdır.", "isKey": True},
                    {"title": "3. Karyolizis", "desc": "DNAaz ile kromatini eriyip çekirdeğin mikroskopta silinmesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Nekrozun 3 Nükleer Değişikliği",
                    "headers": ["Evre", "Morfolojik Görünüm", "Biyokimyasal Mekanizma"],
                    "rows": [
                        ["Piknoz", "Çekirdek küçülmüş, aşırı koyu siyah/mor (bazofilik)", "Kromatin yoğunlaşması ve nükleer büzülme"],
                        ["Karyoreksis", "Piknotik çekirdek parçalanmış, nükleer kırıntılar", "Nükleus zarı yırtılması ve mekanik parçalanma"],
                        ["Karyolizis", "Bazofili kaybı, çekirdeğin silikleşmesi ve yok oluşu", "DNAaz enzimleriyle DNA'nın tamamen sindirilmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozda izlenen 3 nükleer değişiklik: Piknoz (büzülme), Karyoreksis (parçalanma) ve Karyolizisdir (erime).",
                "📌 [YÜKSEK VERİM] Hücre ölümünün patolojideki en kesin ve güvenilir mikroskobik kanıtı nükleer değişikliklerdir."
            ],
            "medicalTerms": [
                {"term": "Piknoz", "explanation": "Nekrozda nükleusun su kaybedip büzülerek aşırı koyu ve yoğun bazofilik hale gelmesidir."},
                {"term": "Karyolizis", "explanation": "DNAaz enzimlerinin DNA'yı eritmesiyle nükleus bazofilisinin solup kaybolmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Nükleer Yıkımın Sıralı Evreleri",
                    [
                        "1. Normal Nükleus: Canlı hücrede açık kromatinli ve düzenli nükleoluslu çekirdek.",
                        "2. Piknoz: Asidoz ve DNA hasarıyla kromatin büzülür, çekirdek küçülür ve kapkara olur.",
                        "3. Karyoreksis: Piknotik çekirdek küçük granüllere uvalanır (nükleer toz).",
                        "4. Karyolizis: DNAaz enzimleri nükleik asitleri tamamen sindirir, bazofili solar.",
                        "5. Akarion: Çekirdek tamamen silinir; geride sadece 'hayalet hücre' kalır."
                    ]
                ),
                make_cloze(
                    "Nekrozda çekirdeğin büzülerek aşırı koyu ve yoğun siyah bir kitle haline gelmesine piknoz denir.",
                    "piknoz",
                    "Nükleer Değişiklik"
                )
            ]
        },
        {
            "slideNumber": 57,
            "title": "Piknoz (Pyknosis): Nükleer Büzülme ve Aşırı Bazofili",
            "subtitle": "Kromatin yoğunlaşması, nükleer kondansasyon ve mürekkep damlası görünümü",
            "badge": "Piknoz",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Piknoz, nekroz sürecinde çekirdeğin uğradığı ilk klasik morfolojik değişikliktir. İskemik "
                "asidoz ve erken endonükleaz kesimleri, nükleer kromatin iplikçiklerinin birbirine sıkıca "
                "yapışmasına ve su kaybederek büzüşmesine neden olur. Çekirdek normal hacminin çok küçük "
                "bir kısmına kadar küçülür.\n\n"
                "> [TEMEL İLKE] Yoğunlaşan nükleik asitler hematoksilen boyasını aşırı derecede çeker; bu "
                "nedenle piknotik çekirdek homojen, sert, kapkara veya koyu mor bir 'mürekkep damlası' gibi görünür.\n\n"
                "Çekirdekçik (nükleolus) ve normal kromatin paterni tamamen silinmiştir. Piknoz apoptozda da "
                "görülebilir; ancak nekrozda ardından gelen basamaklar apoptozdan tamamen ayrılır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Büzülme (Kondansasyon)", "desc": "Çekirdek hacminin dramatik şekilde küçülmesidir.", "isKey": True},
                    {"title": "Aşırı Bazofili", "desc": "Sıkışan DNA fosfat gruplarının hematoksileni yoğun tutmasıdır.", "isKey": True},
                    {"title": "Mürekkep Damlası", "desc": "Çekirdeğin iç yapısını yitirip homojen siyah bir lekeye dönmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Normal Çekirdek vs Piknotik Çekirdek",
                    "headers": ["Özellik", "Normal Canlı Çekirdek", "Piknotik Çekirdek"],
                    "rows": [
                        ["Boyut", "Standart hücresel orana uygun (N/S oranı)", "Belirgin küçülmüş, büzüşmüş"],
                        ["Kromatin Yapısı", "Açık ökromatin ve heterokromatin alanları", "Homojen, tek parça, yoğun kitle"],
                        ["Boyanma Rengi", "Mavi-mor (açık ve koyu adacıklar)", "Koyu siyah-mor (aşırı bazofilik)"],
                        ["Çekirdekçik", "Belirgin nükleolus görülebilir", "Tamamen kaybolmuş"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Piknoz: Çekirdeğin büzüşmesi ve bazofilisinin artmasıyla koyu, küçük, yoğun bir kitleye dönüşmesidir.",
                "📌 [YÜKSEK VERİM] Piknotik nükleusta kromatin detayları seçilemez; homojen koyu bir disk halindedir."
            ],
            "medicalTerms": [
                {"term": "N/S Oranı", "explanation": "Nükleus alanının sitoplazma alanına oranıdır; hücrenin farklılaşma ve malignite derecesini gösterir."},
                {"term": "Ökromatin", "explanation": "DNA transkripsiyonunun aktif olduğu, mikroskopta açık renk görünen gevşek kromatin formudur."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Nekrozda nükleusun su kaybedip büzülerek homojen koyu siyah bir kitleye dönmesine piknoz adı verilir.",
                    "piknoz",
                    "İlk Nükleer Evre"
                ),
                make_active_recall(
                    "Piknotik bir çekirdek neden normal canlı çekirdeğe göre çok daha koyu bazofilik (siyah-mor) boyanır?",
                    "Kromatin ileri derecede büzüşüp yoğunlaştığı için birim alandaki negatif yüklü DNA fosfat gruplarının yoğunluğu katbekat artar; bu durum pozitif yüklü hematoksilen boyasını mıknatıs gibi çekerek aşırı koyu boyanma yaratır."
                )
            ]
        },
        {
            "slideNumber": 58,
            "title": "Karyoreksis (Karyorrhexis): Nükleer Parçalanma",
            "subtitle": "Piknotik çekirdeğin ufalanması ve 'Nükleer Toz' (Nuclear Dust) oluşumu",
            "badge": "Karyoreksis",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Piknoz evresinden sonra veya bazı hasar tiplerinde doğrudan doğruya 'karyoreksis' evresi "
                "gelişir. Endonükleaz aktivitesinin artması ve hücre içi kalsiyum bağımlı proteazların "
                "nükleer membranı (lamin ağını) parçalaması sonucu, o yoğun piknotik çekirdek mekanik "
                "bütünlüğünü koruyamaz.\n\n"
                "> [SINAV SPOTU] Piknotik nükleus parçalanır ve sitoplazma içine çok sayıda küçük, koyu "
                "bazofilik kırıntılar halinde saçılır; bu tabloya 'nükleer toz' (nuclear dust) adı verilir.\n\n"
                "Işık mikroskobunda tek bir çekirdek yerine, sitoplazmada veya hücrelerarası alanda dağılmış "
                "düzensiz siyah parçacıklar izlenir. Lökositlerin parçalanmasında da (lökositoklazi) aynı tablo görülür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Nükleer Ufalanma", "desc": "Piknotik çekirdeğin küçük fragmanlara ayrılmasıdır.", "isKey": True},
                    {"title": "Nükleer Toz", "desc": "Sitoplazmaya saçılan küçük bazofilik kırıntıların mikroskobik adıdır.", "isKey": True},
                    {"title": "Lamin Parçalanması", "desc": "Çekirdek iskeletinin proteazlar tarafından kesilmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Karyoreksis Bulguları",
                    "headers": ["Parametre", "Histolojik Resim", "Patofizyolojik Neden"],
                    "rows": [
                        ["Çekirdek Şekli", "Parçalı, çok sayıda kırıntı", "Nükleer zarın ve kromatinin kırılması"],
                        ["Dağılım", "Sitoplazma içine serpilmiş", "Nükleer membranın rüptüre olması"],
                        ["Klinik Terim", "Nükleer toz (Nuclear dust)", "Lökositoklastik vaskülit ve nekroz sahaları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Karyoreksis: Piknotik çekirdeğin parçalanarak sitoplazmaya saçılan kırıntılara ('nükleer toz') dönüşmesidir.",
                "📌 [YÜKSEK VERİM] Lökositoklastik vaskülitte damar duvarında izlenen 'nükleer toz', nötrofillerin karyoreksise uğramış çekirdek kalıntılarıdır."
            ],
            "medicalTerms": [
                {"term": "Karyoreksis", "explanation": "Nekrotik hücre çekirdeğinin parçalanarak sitoplazma içine saçılması olayıdır."},
                {"term": "Nükleer Toz", "explanation": "Karyoreksis sonucu oluşan küçük, koyu boyanan nükleus kırıntılarıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Piknotik çekirdeğin parçalanarak sitoplazmaya saçılması sonucu oluşan küçük bazofilik kırıntılara nükleer toz adı verilir.",
                    "nükleer toz",
                    "Mikroskobik Kalıntı"
                ),
                make_active_recall(
                    "Piknoz ile Karyoreksis arasındaki morfolojik fark nedir?",
                    "Piknozda çekirdek tek parça halinde küçülmüş ve kapkaradır; karyoreksiste ise bu çekirdek mekanik olarak ufalanmış ve sitoplazmaya çok sayıda küçük parçacık (nükleer toz) halinde dağılmıştır."
                )
            ]
        },
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Sitoplazmik Nekroz Morfolojisi ve Eozinofili",
            "subtitle": "Artmış eozinofili, camsı homojenlik, miyelin figürleri ve piknoz",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 6,
            "synthesisNarrative": (
                "Altıncı kontrol noktasında, nekrozun sitoplazmik ve erken nükleer değişikliklerini pekiştiriyoruz. "
                "Nekrotik hücrelerin canlılardan en belirgin mikroskobik farkı artmış eozinofili (koyu pembe "
                "boyanma) ve nükleer piknozdur.\n\n"
                "> [ÖZET VURGU] Eozinofilinin artması denatüre proteinlerin eozini fazla bağlaması ve bazofilik "
                "RNA'nın kaybı ile açıklanır; camsı görünüm ise glikojen tükenmesinden kaynaklanır.\n\n"
                "Aşağıdaki 3 akıl kartını dikkatle inceleyerek bu kritik histopatolojik bilgileri hafızanıza sabitleyin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Eozinofili Nedeni", "desc": "Protein denatürasyonu + Ribonükleazlarla RNA kaybı.", "isKey": True},
                    {"title": "Camsı Sitoplazma", "desc": "Anaerobik glikolizle glikojen partiküllerinin tükenmesi.", "isKey": True},
                    {"title": "Piknoz", "desc": "Çekirdeğin büzüşerek aşırı koyu homojen bir kitleye dönmesi.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 6 Sentez Tablosu",
                    "headers": ["Bulgu", "Morfoloji", "Patofizyolojik Neden"],
                    "rows": [
                        ["Artmış Eozinofili", "Koyu pembe sitoplazma", "Denatüre protein + RNA kaybı"],
                        ["Camsı Görünüm", "Pürüzsüz homojenlik", "Glikojen depolarının sıfırlanması"],
                        ["Güve Yeniği", "Sitoplazmik kaviteler", "Lizozomal enzimlerin organel sindirimi"],
                        ["Piknoz", "Küçülmüş kapkara nükleus", "Asidozla kromatinin aşırı yoğunlaşması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozda sitoplazmanın artmış eozinofili göstermesinin iki nedeni: Denatüre proteinlerin eozini fazla bağlaması ve RNA kaybıdır.",
                "📌 [SINAV SPOTU] Piknoz: Çekirdeğin büzülerek yoğun bazofilik bir kitleye dönüşmesidir."
            ],
            "medicalTerms": [
                {"term": "Nükleaz", "explanation": "DNA veya RNA zincirlerindeki fosfodiester bağlarını parçalayan enzimlerdir."},
                {"term": "Ribonükleaz (RNaz)", "explanation": "Sitoplazmik RNA'yı parçalayarak hücrenin bazofilik boyanmasını ortadan kaldıran enzimdir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-016",
                    "Nekroza uğrayan bir hücrenin sitoplazmasının canlı hücreye göre çok daha parlak ve koyu pembe (artmış eozinofili) boyanmasının 2 temel nedeni nedir?",
                    "1) Asidozla denatüre olan sitoplazmik proteinlerin eozin boyasını aşırı miktarda bağlaması, 2) Normalde sitoplazmaya mavi (bazofilik) ton veren ribozomal RNA'nın enzimlerle parçalanarak kaybolmasıdır."
                ),
                make_flashcard(
                    "fc-k1-04-017",
                    "Nekrozda izlenen 'camsı' (glassy) homojen sitoplazma görünümünün biyokimyasal nedeni nedir?",
                    "İskemi sırasında erken dönemde artan anaerobik glikoliz nedeniyle hücre içindeki tüm glikojen partiküllerinin tükenmesi ve proteinlerin pıhtılaşmasıdır."
                ),
                make_flashcard(
                    "fc-k1-04-018",
                    "Piknoz ile Karyoreksis arasındaki en temel morfolojik fark nedir?",
                    "Piknozda çekirdek tek parça halinde küçülmüş, büzüşmüş ve homojen siyahtır; Karyoreksiste ise bu piknotik çekirdek parçalanarak sitoplazma içine nükleer toz (kırıntılar) halinde dağılmıştır."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 6 Sentezi: Bir dokuda 'Piknoz' izlenmesi hücrenin hangi evrede olduğunu kesin olarak kanıtlar?",
                    "Hücrenin geri dönüşümlü fazı geride bırakıp kesin ve geri dönüşümsüz olarak ÖLDÜĞÜNÜ (nekroza girdiğini) kanıtlar; çünkü piknoz çekirdek erimesinin ilk kesin basamağıdır."
                ),
                make_cloze(
                    "Nekrozda çekirdeğin parçalanarak sitoplazmaya saçılan küçük parçacıklar oluşturmasına karyoreksis denir.",
                    "karyoreksis",
                    "Parçalanma Evresi"
                )
            ]
        }
    ]
