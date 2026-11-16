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
            "slideNumber": 90,
            "title": "Doku Nekrozu Kalıplarının Büyük Karşılaştırma Matrisi",
            "subtitle": "Koagülatif, sıvılaşma ve gangrenöz nekrozun sentezi",
            "badge": "Büyük Sentez",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre Hasarı ve Nekroz - I dersinin çekirdek morfolojik kazanımı, ilk üç doku nekrozu "
                "kalıbı arasındaki ayırıcı tanıyı kusursuz biçimde kavramaktır. Koagülatif nekroz, iskemik "
                "katı organların protein denatürasyonuyla sertleştiği ve mimarisini günlerce koruduğu kalıptır. "
                "Sıvılaşma nekrozu ise püy oluşturan enfeksiyonların ve serebral infarktların litik erimesidir.\n\n"
                "> [TEMEL İLKE] Gangrenöz nekroz ise bu mekanizmaların klinikteki makroskobik uzantısıdır; "
                "saf iskemide kuru, süperenfeksiyonda ıslak, klostridyal gaz üretiminde gazlı gangren adını alır.\n\n"
                "Aşağıdaki matris bu üç temel kalıbın etiyoloji, histoloji, kıvam ve prognoz parametrelerini özetler."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Koagülatif", "desc": "Protein denatürasyonu baskın, doku sert, mimari korunur (Miyokard/Böbrek).", "isKey": True},
                    {"title": "Sıvılaşma", "desc": "Enzimatik hidroliz baskın, viskoz püy/sıvı, mimari silinir (Apse/Beyin).", "isKey": True},
                    {"title": "Gangrenöz", "desc": "Alt ekstremitede koagülatif (kuru) veya sıvılaşma (ıslak) kombinasyonudur.", "isKey": True}
                ],
                "table": {
                    "title": "Üç Temel Doku Nekrozu Kalıbının Büyük Matrisi",
                    "headers": ["Ölçüt", "Koagülatif Nekroz", "Sıvılaşma Nekrozu", "Gangrenöz Nekroz"],
                    "rows": [
                        ["Baskın Süreç", "Protein denatürasyonu", "Enzimatik litik sindirim", "İskemi +/- Bakteriyel litik sindirim"],
                        ["Doku Mimarisi", "Günlerce korunur (Hayalet hücre)", "Hemen erir, tamamen kaybolur", "Kuru tipte korunur, ıslakta erir"],
                        ["Fiziksel Kıvam", "Sert, katı, kuru, opak", "Sıvı, akışkan püy veya kavite", "Mumyalaşmış kuru veya şişmiş kokuşuk"],
                        ["Tipik Organ", "Kalp, Böbrek, Dalak (Katı)", "Beyin (istisna) ve Bakteriyel apseler", "Alt ekstremite, ayak, bağırsak segmenti"],
                        ["İyileşme Modeli", "Kollajenöz fibröz skar", "Kistik kavite (beyin) veya drenaj", "Cerrahi amputasyon veya skar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Koagülatif nekrozda protein denatürasyonu; Sıvılaşma nekrozunda enzimatik hidroliz baskındır.",
                "📌 [SINAV SPOTU] İskemik katı organlar koagülatif nekroza uğrarken, iskemik beyin dokusu sıvılaşma nekrozuna uğrar."
            ],
            "medicalTerms": [
                {"term": "Doku Kalıbı", "explanation": "Nekrozun mikroskobik ve makroskobik görünümünün etiyolojiye göre aldığı karakteristik desendir."},
                {"term": "Fibröz Skar", "explanation": "İyileşme sürecinde fibroblastların ürettiği kollajen bağ dokusu nedbesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Nekroz Kalıpları Büyük Matrisi",
                    ["Parametre", "Koagülatif", "Sıvılaşma", "Gangrenöz"],
                    [
                        [("Mekanizma", False), ("Denatürasyon", True, "Pıhtılaşma"), ("Enzimatik lizis", True, "Erime"), ("İskemi + Enfeksiyon", True, "Kombinasyon")],
                        [("Mimari", False), ("Korunur", True, "Taslak"), ("Silinir", True, "Kavite"), ("Kuru: Korunur / Islak: Erir", True, "Değişken")],
                        [("Kıvam", False), ("Sert ve kuru", True, "Katı"), ("Akışkan sıvı / püy", True, "Sıvı"), ("Mumyalaşmış veya çürük", True, "Klinik")],
                        [("Organ", False), ("Kalp, böbrek", True, "Katı"), ("Beyin, apse", True, "Özel"), ("Bacak, ayak", True, "Uzuv")]
                    ]
                ),
                make_cloze(
                    "İskemik dokularda doku mimarisinin korunduğu en sık nekroz tipi koagülatif nekrozdur.",
                    "koagülatif nekrozdur",
                    "En Sık Tip"
                )
            ]
        },
        {
            "slideNumber": 91,
            "title": "Hücre Hasarının Biyokimyasal Yolakları Entegrasyonu",
            "subtitle": "ATP, kalsiyum, ROS, membran ve mitokondri hasarının ortak kavşağı",
            "badge": "Entegrasyon",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre zedelenmesini başlatan etken ne olursa olsun (hipoksi, toksin, radyasyon veya enfeksiyon), "
                "hücresel ölüm beş temel biyokimyasal yolağın ortak kavşağında düğümlenir: 1) Mitokondriyal "
                "ATP üretiminin çöküşü, 2) Sitozolik kalsiyum homeostazının iflası, 3) Reaktif oksijen "
                "türlerinin (ROS) birikerek oksidatif stres yaratması.\n\n"
                "> [TEMEL İLKE] 4) Plazma ve lizozomal membran geçirgenliğinin bozulması, 5) Nükleer DNA "
                "ve protein katlanma hasarı; bu yolaklar birbirini pozitif geri bildirimle besler.\n\n"
                "Bu yolakların hangisinin önce başladığı etiyolojik ajana bağlıdır; ancak biri çöktüğünde "
                "diğerleri saniyeler içinde devreye girerek hücreyi kaçınılmaz nekroza veya apoptoza taşır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Mitokondri ve ATP", "desc": "Tüm hücresel pompaların ve sentez süreçlerinin enerji kaynağıdır.", "isKey": True},
                    {"title": "Kalsiyum İstilası", "desc": "Fosfolipaz, proteaz ve endonükleazları uyararak hücreyi parçalayan tetiktir.", "isKey": True},
                    {"title": "Membran Delinmesi", "desc": "Hücrenin biyolojik bireyselliğini kaybedip lizise uğradığı son noktadır.", "isKey": True}
                ],
                "table": {
                    "title": "Hücre Hasarının 5 Biyokimyasal Kavşağı",
                    "headers": ["Yolak / Hedef", "Hasar Mekanizması", "Hücresel Sonuç"],
                    "rows": [
                        ["ATP Tükenmesi", "Mitokondriyal iskemi, toksinler", "Na+/K+ pompa iflası, hidropik şişme, glikojen kaybı"],
                        ["Kalsiyum Girişi", "Ca2+ ATPaz durması, ER sızıntısı", "Fosfolipaz, proteaz, endonükleaz aktivasyonu"],
                        ["Reaktif Oksijen (ROS)", "O2 indirgenme defektleri, reperfüzyon", "Lipid peroksidasyonu, protein çapraz bağlanması"],
                        ["Membran Hasarı", "Fosfolipid kaybı, deterjan etkisi", "Hücre içeriğinin kana sızması, inflamasyon"],
                        ["DNA Hasarı", "Radyasyon, alkilleyici ajanlar, ROS", "p53 aktivasyonu, apoptoz veya karyolizis"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarında 5 ortak biyokimyasal kavşak: ATP tükenmesi, kalsiyum artışı, ROS birikimi, membran hasarı ve DNA/protein hasarıdır.",
                "📌 [YÜKSEK VERİM] Hasar yolakları birbirini tetikler; mitokondri hasarı ATP'yi tüketir, ATP tükenmesi kalsiyumu fırlatır, kalsiyum membranı deler."
            ],
            "medicalTerms": [
                {"term": "Biyokimyasal Kavşak", "explanation": "Farklı hasar etkenlerinin hücresel düzeyde birleştiği ortak moleküler patoloji yolaklarıdır."},
                {"term": "Pozitif Geri Bildirim", "explanation": "Hasar basamaklarının birbirini daha da şiddetlendirerek geri dönüşümsüz krizi hızlandırmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hücre Hasarının Entegre Biyokimyasal Akışı",
                    [
                        "1. Primer Hasar: İskemi veya toksin mitokondriyal solunumu durdurur.",
                        "2. ATP Çöküşü: Hücresel ATP hızla sıfırlanır, glikoliz asidoz yapar.",
                        "3. İyon Pompaları İflası: Na+ ve su içeri dolar (şişme), Ca2+ sitoplazmaya hücum eder.",
                        "4. Yıkıcı Enzimler: Kalsiyum fosfolipaz ve proteazları aktive ederek zarları deler.",
                        "5. Nekrotik Lizis: Membran patlar, enzimler kana dökülür ve çevre doku infiltre olur."
                    ]
                ),
                make_cloze(
                    "Hücre hasarında kalsiyum artışının membranları delmesini sağlayan temel enzim fosfolipazdır.",
                    "fosfolipazdır",
                    "Membran Yıkımı"
                )
            ]
        },
        {
            "slideNumber": 92,
            "title": "Klinik Olgu 1: Akut Miyokard Enfarktüsü ve Troponin Yükselmesi",
            "subtitle": "58 yaşında erkek hasta, retrosternal baskı, EKG ve koagülatif nekroz",
            "badge": "Klinik Olgu",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "58 yaşında sigara içen, hipertansif bir erkek hasta, sol kola yayılan şiddetli retrosternal "
                "baskı tarzı göğüs ağrısı ve soğuk terleme ile acil servise getiriliyor. EKG'de V1-V4 "
                "derivasyonlarında ST segment elevasyonu saptanıyor. Acil koroner anjiyografide sol ön "
                "inen arterin (LAD) trombozla tam tıkandığı izleniyor.\n\n"
                "> [PATOFİZYOLOJİK ÇÖZÜM] Miyokard iskemisi 20-30 dakikayı aştığı için subendokardiyal "
                "miyositlerde 'point of no return' aşılmış, mitokondrilerde amorf kalsiyum birikmiş ve plazma zarı yırtılmıştır.\n\n"
                "Membran bütünlüğü bozulduğu için kanda Kardiyak Troponin I ve CK-MB düzeyleri fırlamıştır. "
                "Doku histopatolojisinde dalgalı kas lifleri ve koagülasyon nekrozu izlenir; reperfüzyon "
                "sağlanarak infarkt alanı sınırlandırılır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Klinik Tablo", "desc": "LAD tıkanmasına bağlı transmural anteriyor miyokard enfarktüsüdür.", "isKey": True},
                    {"title": "Patoloji Karşılığı", "desc": "Kalp kasında gelişen klasik koagülatif nekrozdur.", "isKey": True},
                    {"title": "Laboratuvar Kanıtı", "desc": "Plazma zarı delindiği için kanda Troponin I yükselmesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Olgu 1 Patofizyolojik Değerlendirmesi",
                    "headers": ["Klinik / Laboratuvar Parametre", "Hastadaki Bulgu", "Patolojik Mekanizma"],
                    "rows": [
                        ["Göğüs Ağrısı", "Retrosternal baskı, 45 dakikadır sürüyor", "İskemiye bağlı laktik asit birikimi ve nosiseptör uyarımı"],
                        ["Serum Troponin I", "Masif yüksek (> 10 ng/mL)", "Miyosit membran rüptürü ve sitoplazmik protein sızıntısı"],
                        ["Miyokard Biyopsisi (Erken)", "Dalgalı lifler (wavy fibers)", "İskemik gevşek liflerin canlı komşularca çekilmesi"],
                        ["Nekroz Kalıbı", "Koagülatif nekroz", "Asidozla yapısal protein ve enzimlerin denatürasyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyokard enfarktüsünde kanda Troponin I/T yüksekliği miyosit plazma membranının kalıcı olarak parçalandığını kanıtlar.",
                "📌 [KLİNİK İPUCU] İskemi süresi 20-30 dakikayı aştığında geri dönüşümsüz hasar başlar; erken anjiyoplasti miyokard dokusunu kurtarır."
            ],
            "medicalTerms": [
                {"term": "LAD", "explanation": "Sol Ön İnen Koroner Arter; miyokard enfarktüslerinde en sık tıkanan koroner damardır."},
                {"term": "Subendokardiyal Bölge", "explanation": "Ventrikül duvarının en iç katmanı; koroner perfüzyon basıncının en düşük olduğu ve iskeminin ilk başladığı sahadır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Göğüs ağrısı 15. dakikasında olan ve anjiyoyla damarı açılan bir hasta ile ağrısı 4 saattir süren hastanın miyokard kaderi senaryosu.",
                    [
                        {
                            "text": "Her iki hastada da tüm miyokard tamamen ölmüştür ve skar dokusuna dönüşür.",
                            "isCorrect": False,
                            "feedback": "Hatalı! İlk 20 dakikada doku henüz geri dönüşümlü evrededir."
                        },
                        {
                            "text": "15. dakikada açılan hastada miyositler henüz 'point of no return'ü aşmamıştır ve tam fonksiyonel iyileşme mümkündür; 4 saatlik hastada ise geri dönüşümsüz koagülatif nekroz gelişmiştir.",
                            "isCorrect": True,
                            "feedback": "Mükemmel patofizyolojik kavrayış! Kalp kasında 20-30 dakika sınırı geri dönüşümlü ile geri dönüşümsüzü ayırır."
                        },
                        {
                            "text": "4 saatlik hastanın kalbinde sıvılaşma nekrozu gelişir.",
                            "isCorrect": False,
                            "feedback": "Yanlış! Kalpte koagülatif nekroz gelişir."
                        }
                    ]
                ),
                make_cloze(
                    "Akut miyokard enfarktüsünde miyosit membranlarının yırtıldığını ve nekroz geliştiğini kanıtlayan altın standart biyobelirteç kardiyak troponindir.",
                    "kardiyak troponindir",
                    "Kardiyak Belirteç"
                )
            ]
        },
        {
            "slideNumber": 93,
            "title": "Klinik Olgu 2: Serebral İskemik İnme ve Sıvılaşma Kavitasyonu",
            "subtitle": "72 yaşında kadın hasta, ani sağ hemipleji, afazi ve beyin BT bulguları",
            "badge": "Klinik Olgu",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "72 yaşında atriyal fibrilasyonu olan bir kadın hasta, aniden gelişen sağ kol ve bacakta "
                "tam felç (sağ hemipleji) ve konuşamama (afazi) tablosuyla acile getiriliyor. Çekilen beyin "
                "MRG ve BT'sinde sol orta serebral arter (MCA) sulama alanında geniş bir iskemik infarktüs "
                "alanı saptanıyor.\n\n"
                "> [PATOFİZYOLOJİK ÇÖZÜM] Beyin dokusu iskemiye uğradığı için koagüle olamaz; yüksek miyelin "
                "lipiti ve litik enzimler nedeniyle hızla sıvılaşma (likefaksiyon) nekrozuna girer.\n\n"
                "İlk 24 saatte kırmızı nöronlar izlenir; günler içinde doku ensefalomalazi ile çamurlaşır, "
                "mikroglial lipid fagositleri miyelini temizler ve aylar sonra geride astrositer gliozis "
                "ile çevrili kistik bir kavite kalır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Klinik Tablo", "desc": "Sol MCA embolisine bağlı akut iskemik inme (stroke) tablosudur.", "isKey": True},
                    {"title": "Nekroz Tipi", "desc": "İskemiye rağmen koagüle olmayıp eriyen SIVILAŞMA nekrozudur.", "isKey": True},
                    {"title": "Kronik Sonuç", "desc": "Kollajenöz skar yerine sıvı dolu kistik kavite ve glial nedbedir.", "isKey": True}
                ],
                "table": {
                    "title": "Olgu 2 Patofizyolojik Değerlendirmesi",
                    "headers": ["Zaman Dilimi", "Beyindeki Patolojik Olay", "Görüntüleme Karşılığı"],
                    "rows": [
                        ["İlk 12 - 24 Saat", "Kırmızı nöronlar, sitotoksik ödem", "BT'de gri-beyaz cevher ayrımında silinme"],
                        ["3 - 5. Gün", "Ensefalomalazi, doku sıvılaşması", "Belirgin hipodens infarkt alanı, kitle etkisi"],
                        ["2 - 4. Hafta", "Lipid fagositleri (köpüksü makrofajlar)", "Nekrotik alanın rezorpsiyonu, ödem gerilemesi"],
                        ["> 2 Ay", "Kistik kavite ve çevresinde gliozis", "BOS dansitesinde kalıcı kistik boşluk (kavite)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Serebral enfarktüs sıvılaşma nekrozu ile seyreder; iyileşme kistik kavite ve gliozis ile biter.",
                "📌 [YÜKSEK VERİM] Atriyal fibrilasyonda sol atriyal apendikste oluşan trombüsler en sık sol orta serebral artere (MCA) embolize olur."
            ],
            "medicalTerms": [
                {"term": "MCA", "explanation": "Orta Serebral Arter; beynin motor ve dil merkezlerini besleyen, inmede en sık tıkanan damardır."},
                {"term": "Afazi", "explanation": "Beyin hasarı sonucu konuşma, anlama veya ifade etme yeteneğinin bozulmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Serebral İnmenin Patolojik Akışı",
                    [
                        "1. Embolik Tıkanma: Kalpten kopan trombüs sol MCA'yı tıkar.",
                        "2. Akut Hipoksi: Kortikal nöronlar dakikalar içinde ölür ve 'kırmızı nöron' haline gelir.",
                        "3. Sıvılaşma (Ensefalomalazi): Zengin hidrolazlar dokuyu viskoz sıvıya dönüştürür.",
                        "4. Makrofaj Fagositozu: Mikroglialar köpüksü lipid fagositlerine dönerek enkazı temizler.",
                        "5. Kistik Kavite ve Gliozis: Fibröz skar yerine sıvı dolu kalıcı kist ve astrosit ağı kalır."
                    ]
                ),
                make_cloze(
                    "Beyin iskemik enfarktüsü alanında nekrotik miyelin kalıntılarını yutan köpüksü hücrelere lipid fagositleri denir.",
                    "lipid fagositleri",
                    "Fagositik Hücre"
                )
            ]
        },
        {
            "slideNumber": 94,
            "title": "Klinik Olgu 3: Diyabetik Hastada Islak Gangren ve Acil Cerrahi",
            "subtitle": "64 yaşında kontrolsüz diyabetik erkek, ayakta kötü kokulu siyah lezyon ve septik şok",
            "badge": "Klinik Olgu",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "64 yaşında 20 yıldır tip 2 diyabeti olan bir erkek hasta, sağ ayak başparmağında başlayan "
                "ve 1 haftada ayağın sırtına doğru yayılan siyah, şiş, kötü kokulu ve pürülan akıntılı "
                "bir yara ile acile başvuruyor. Hastanın ateşi 39.2°C, tansiyonu 85/50 mmHg ve nabzı 125/dk'dır. "
                "Ayak nabızları palpe edilemiyor.\n\n"
                "> [PATOFİZYOLOJİK ÇÖZÜM] Periferik arter hastalığı zeminindeki koagülatif nekroza (kuru gangren), "
                "mikst piyojenik bakterilerin eklenmesiyle doku hızla SIVILAŞMA nekrozuna (Islak gangren) dönmüştür.\n\n"
                "Demarkasyon hattı yoktur, enfeksiyon hızla bacağa tırmanmaktadır ve hasta septik şoktadır. "
                "Acil diz altı amputasyon ve geniş spektrumlu antibiyoterapi hayat kurtarıcı tek çözümdür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Klinik Tablo", "desc": "Diyabetik vaskülopati zemininde gelişen fulminan ıslak gangren ve sepsistir.", "isKey": True},
                    {"title": "Mekanizma", "desc": "Koagülatif nekrozun bakteriyel enzimlerle ikincil sıvılaşma nekrozuna dönmesidir.", "isKey": True},
                    {"title": "Tedavi Aciliyeti", "desc": "Demarkasyon hattı beklenmeden acil amputasyon yapılması zorunludur.", "isKey": True}
                ],
                "table": {
                    "title": "Olgu 3 Patofizyolojik Değerlendirmesi",
                    "headers": ["Bulgu", "Klinik Görünüm", "Patolojik Anlam"],
                    "rows": [
                        ["Ayak Muayenesi", "Ödemli, mor-siyah, kötü kokulu püy", "İkincil sıvılaşma nekrozu ve çürüme (putrefaksiyon)"],
                        ["Sınır Çizgisi", "Demarkasyon hattı yok, eritem bacağa yayılıyor", "Bakteri enzimlerinin fasyal planlarda proksimale ilerlemesi"],
                        ["Vital Bulgular", "Hipotansiyon (85/50), Taşikardi (125/dk), Ateş", "Bakteriyel toksinlerin kana karışmasıyla gelişen Septik Şok"],
                        ["Cerrahi Karar", "Acil diz altı amputasyon", "Toksemi odağının radikal olarak vücuttan uzaklaştırılması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Islak gangren acil cerrahi tablodur; demarkasyon hattı oluşmaz ve sistemik septik şoka yol açar.",
                "📌 [KLİNİK İPUCU] Diyabetik ayak ülserlerinde kötü koku ve fluktuasyon belirmesi kuru gangrenin ıslak gangrene döndüğünü haber verir."
            ],
            "medicalTerms": [
                {"term": "Septik Şok", "explanation": "Ağır bakteriyel enfeksiyon toksinlerinin yaygın vazodilatasyon ve hipotansiyon yapmasıdır."},
                {"term": "Amputasyon", "explanation": "Geri dönüşsüz gangrenli bir uzvun cerrahi olarak sağlam sınırından kesilip çıkarılmasıdır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Acile getirilen bu hastada cerrahi ekibin vermesi gereken acil yönetim kararı senaryosu.",
                    [
                        {
                            "text": "Hasta eve gönderilip yara yerine sadece merhem sürülmelidir.",
                            "isCorrect": False,
                            "feedback": "Ağır malpraktis! Hasta saatler içinde septik şoktan ölür."
                        },
                        {
                            "text": "Yoğun sıvı resüsitasyonu ve IV antibiyotik başlanarak hasta acilen ameliyathaneye alınmalı ve enfeksiyon sınırının üzerinden acil amputasyon yapılmalıdır.",
                            "isCorrect": True,
                            "feedback": "Mükemmel hayat kurtarıcı cerrahi karar! Islak gangrende toksik odak çıkarılmadan hasta kurtulamaz."
                        },
                        {
                            "text": "Demarkasyon hattının netleşmesi için 2 hafta beklenmelidir.",
                            "isCorrect": False,
                            "feedback": "Islak gangrende demarkasyon hattı beklenmez, hasta o sürede ölür."
                        }
                    ]
                ),
                make_cloze(
                    "Islak gangrende bakteriyel toksinlerin kana karışmasıyla gelişen ölümcül kardiyovasküler çöküşe septik şok adı verilir.",
                    "septik şok",
                    "Sistemik Komplikasyon"
                )
            ]
        },
        {
            "slideNumber": 95,
            "title": "Klinik Olgu 4: Karbon Monoksit Zehirlenmesi ve Hipoksik Hasar",
            "subtitle": "Kışın soba dumanı maruziyeti, kiraz kırmızısı cilt ve globus pallidus nekrozu",
            "badge": "Klinik Olgu",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "24 yaşında bir üniversite öğrencisi, kış gecesi sobalı odada baygın halde bulunuyor. "
                "Acile getirildiğinde komada, solunumu yüzeyel ve cildi ile dudak mukozası karakteristik "
                "olarak 'kiraz kırmızısı' (cherry-red) renkte izleniyor. Kan gazında arteriyel pO2 normal, "
                "ancak karboksihemoglobin düzeyi %55 olarak saptanıyor.\n\n"
                "> [PATOFİZYOLOJİK ÇÖZÜM] Karbon monoksit hemoglobine oksijenden ~200 kat daha yüksek "
                "afiniteyle bağlanarak oksihemoglobin disosiyasyon eğrisini sola kaydırır ve dokulara oksijen sunumunu sıfırlar.\n\n"
                "Kandaki pO2 normal olmasına rağmen hücreler derin hipoksi yaşar. CO zehirlenmesinin en "
                "özgül nöropatolojik bulgusu, bazal ganglionlarda özellikle bilateral 'Globus Pallidus' "
                "simetrik nekrozudur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Karboksihemoglobin", "desc": "CO'nun hemoglobine geri dönüşsüz bağlanarak oksijen transferini felç etmesidir.", "isKey": True},
                    {"title": "Kiraz Kırmızısı Cilt", "desc": "Karboksihemoglobin bileşiğinin parlak kırmızı renginin cilde yansımasıdır.", "isKey": True},
                    {"title": "Globus Pallidus Nekrozu", "desc": "CO zehirlenmesine en duyarlı beyin bölgesinde gelişen bilateral nekrozdur.", "isKey": True}
                ],
                "table": {
                    "title": "Olgu 4 Patofizyolojik Değerlendirmesi",
                    "headers": ["Parametre", "Hastadaki Durum", "Patolojik Mekanizma"],
                    "rows": [
                        ["Karboksihemoglobin", "%55 (Ağır toksik düzey)", "CO'nun demir moleküllerine sıkıca kilitlenmesi"],
                        ["Arteriyel pO2", "Normal (Çözünmüş O2 normal)", "Akciğer gaz difüzyonu sağlamdır fakat taşıma kapasitesi çökmüştür"],
                        ["Cilt Rengi", "Vişne / Kiraz kırmızısı", "Karboksihemoglobin molekülünün parlak kırmızı optik özelliği"],
                        ["Nöropatoloji", "Bilateral Globus Pallidus nekrozu", "Yüksek metabolik O2 ihtiyacı ve CO'nun mitokondri kompleks IV blokajı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Karbon monoksit zehirlenmesinin en karakteristik nöropatolojik lezyonu bilateral Globus Pallidus simetrik nekrozudur.",
                "📌 [SINAV SPOTU] CO zehirlenmesinde siyanoz görülmez; cilt ve mukozalar 'kiraz kırmızısı' (cherry-red) renktedir."
            ],
            "medicalTerms": [
                {"term": "Globus Pallidus", "explanation": "Beyin bazal ganglionlarının bir parçası; CO zehirlenmesinde hipoksik nekroza en duyarlı alandır."},
                {"term": "Kiraz Kırmızısı Renk", "explanation": "Karboksihemoglobin konsantrasyonu yüksek kanda izlenen parlak kırmızı renk tonudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Hipoksi Tipleri: Anoksik vs Karbon Monoksit",
                    "Saf Hipoksik Hipoksi (Boğulma)",
                    "Karbon Monoksit Hipoksisi",
                    [
                        "Arteriyel pO2 belirgin düşüktür",
                        "Kanda indirgenmiş hemoglobin artar",
                        "Ciltte ve dudaklarda morarma (Siyanoz) olur",
                        "Dokular oksijensizlikten soluklaşır"
                    ],
                    [
                        "Arteriyel pO2 normal sınırlardadır",
                        "Karboksihemoglobin konsantrasyonu fırlar",
                        "Ciltte parlak 'Kiraz Kırmızısı' renk görülür",
                        "Bilateral Globus Pallidus nekrozu gelişir"
                    ]
                ),
                make_cloze(
                    "Karbon monoksit zehirlenmesinin beyindeki en karakteristik nekroz lezyonu bilateral globus pallidus nekrozudur.",
                    "globus pallidus",
                    "Nöropatolojik Odak"
                )
            ]
        },
        {
            "slideNumber": 96,
            "title": "Tıbbi Patolojide Sık Yapılan Hatalar ve Kritik Tuzaklar",
            "subtitle": "Kavram kargaşaları, sınav tuzakları ve doğru patolojik mantık",
            "badge": "Kritik Tuzaklar",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patoloji sınavlarında ve klinik değerlendirmelerde en sık düşülen tuzaklar, birbirine "
                "benzeyen ancak patofizyolojik olarak taban tabana zıt olan kavramların karıştırılmasıdır. "
                "Bu tuzakların başında 'hücre ölümü ile morfolojinin eşzamanlı sanılması' gelir; oysa hücre "
                "biyokimyasal olarak öldükten saatler sonra mikroskopta nekroz görünür.\n\n"
                "> [KRİTİK UYARI] Diğer bir tuzak: İskemik enfarktların koagülatif nekroz kuralının beyinde "
                "de geçerli sanılmasıdır; beyin istisnadır ve sıvılaşma nekrozu yapar!\n\n"
                "Ayrıca nekroz ile apoptoz karıştırılmamalıdır; nekroz daima patolojik ve inflamatuardır, "
                "apoptoz ise fizyolojik olabilen ve inflamasyon yapmayan sessiz bir intihardır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Tuzak 1: Morfoloji Gecikmesi", "desc": "Ölüm morfolojiden önce gelir; erken ölümlerde mikroskopi normal kalabilir.", "isKey": True},
                    {"title": "Tuzak 2: Beyin İskemisi", "desc": "Tüm organlar koagüle olurken beyin sıvılaşma nekrozu yapar.", "isKey": True},
                    {"title": "Tuzak 3: Enflamasyon Ayrımı", "desc": "Nekroz daima inflamasyon yapar; apoptozda inflamasyon sıfırdır.", "isKey": True}
                ],
                "table": {
                    "title": "Sık Yapılan Hatalar ve Doğru Bilimsel Gerçekler",
                    "headers": ["Yaygın Yanılgı (Tuzak)", "Doğru Patolojik İlke", "Klinik Gerekçe"],
                    "rows": [
                        ["Hücre ölür ölmez ışık mikroskobunda nekroz görülür", "Hücre ölümü morfolojiden 4-12 saat önce gerçekleşir", "Enzimlerin pıhtılaşması ve sindirim zaman alır"],
                        ["Tüm iskemik enfarktlar koagülatif nekrozdur", "Beyin infarktı SIVILAŞMA nekrozudur", "Beyinde protein az, lipit ve litik enzim çoktur"],
                        ["Nekroz bazen fizyolojik olabilir", "Nekroz DAİMA patolojiktir", "Hücre zarının yırtılması asla normal bir süreç değildir"],
                        ["Apoptoz da çevre dokuda yangı yapar", "Apoptozda inflamasyon ASLA oluşmaz", "Membran sağlam kalır, apoptotik cisimcikler sessizce yutulur"],
                        ["ATP azalması Na+ atılımını artırır", "ATP azalması Na+/K+ pompasını durdurur, Na+ birikir", "Hücresel şişmenin ana nedeni intraselüler Na+ artışıdır"]
                    ]
                }
            },
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Nekroz daima patolojiktir; fizyolojik nekroz diye bir kavram tıpta YOKTUR!",
                "🚨 [KRİTİK UYARI] ATP azalınca hücre dışına sodyum atılmaz; aksine sodyum hücre içinde birikir ve suyu çekerek hidropik şişme yapar."
            ],
            "medicalTerms": [
                {"term": "Fizyolojik Ölüm", "explanation": "Embriyogenez veya doku yenilenmesinde vücudun bilinçli yürüttüğü apoptoz sürecidir."},
                {"term": "Patolojik Nekroz", "explanation": "Zararlı bir stres sonucu hücrenin kontrolsüz olarak patlayıp ölmesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Sınav Tuzakları ve Doğrular",
                    "Hatalı Bilgi / Tuzak",
                    "Doğru Patolojik Bilgi",
                    [
                        "Beyin iskemisinde koagülatif nekroz olur",
                        "Nekroz fizyolojik süreçlerde de görülebilir",
                        "Hücre ölümü anında mikroskopta nekroz çıkar",
                        "ATP tükenince hücre dışına Na+ pompalanır"
                    ],
                    [
                        "Beyin iskemisinde SIVILAŞMA nekrozu gelişir",
                        "Nekroz DAİMA patolojik bir hücresel yıkımdır",
                        "Biyokimyasal ölüm morfolojiden saatler öncedir",
                        "ATP tükenince Na+ hücre içinde birikir ve şişirir"
                    ]
                ),
                make_cloze(
                    "Nekroz daima patolojik bir hücre ölümü olup hücre zarının yırtılmasıyla çevre dokuda mutlaka inflamasyon oluşturur.",
                    "patolojik",
                    "Doğru Nitelik"
                )
            ]
        },
        {
            "slideNumber": 97,
            "title": "TUS ve Kurul Sınavlarında En Sık Sorulan Hücre Hasarı Spotları",
            "subtitle": "Sınav komitelerinin vazgeçilmez soru kalıpları ve anahtar kelimeleri",
            "badge": "Sınav Spotları",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre Hasarı ve Nekroz - I konusu, TUS (Tıpta Uzmanlık Eğitimi Giriş Sınavı) ve dönem 3 kurul "
                "sınavlarında en yüksek soru yoğunluğuna sahip temel patoloji başlığıdır. Komitelerin her yıl "
                "düzenli olarak sorguladığı soru kalıpları belirli anahtar kavramlar etrafında yoğunlaşır.\n\n"
                "> [SINAV SPOTU] En sık sorulan üçlü: 1) Hasarın en erken morfolojik bulgusu (Hidropik şişme), "
                "2) Geri dönüşümsüzlük kriteri (Mitokondri amorf kalsiyumu ve membran yırtığı), 3) Beyin enfarktüsünün nekroz tipi (Sıvılaşma nekrozu).\n\n"
                "Aşağıdaki spotlar son 15 yılın tüm kurul ve uzmanlık sınav sorularının damıtılmış özetidir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "En Erken Bulgu", "desc": "Hücresel şişme (hidropik değişim) = Na+/K+ ATPaz pompa yetmezliği.", "isKey": True},
                    {"title": "Geri Dönüşsüzlük Damgası", "desc": "Mitokondride amorf elektron-yoğun kalsiyum birikintileri.", "isKey": True},
                    {"title": "Büyük İstisna", "desc": "İskemik dokuda koagülatif kuralını bozan tek organ: Beyin (Sıvılaşma).", "isKey": True}
                ],
                "table": {
                    "title": "En Sık Çıkan 5 Sınav Sorusu ve Yanıtı",
                    "headers": ["Soru Konusu", "Doğru Yanıt", "Tuzak Şık"],
                    "rows": [
                        ["Hücre hasarının en sık nedeni", "Hipoksi ve iskemi", "Enfeksiyonlar veya genetik mutasyonlar"],
                        ["En erken geri dönüşümlü morfolojik bulgu", "Hücresel şişme (Hidropik değişim)", "Yağlanma veya eozinofili"],
                        ["Geri dönüşümsüz hasarın EM kriteri", "Mitokondride amorf elektron-yoğun kalsiyum", "ER dilatasyonu veya bleb oluşumu"],
                        ["Beyin iskemik enfarktüsünün nekroz tipi", "Sıvılaşma (Likefaksiyon) nekrozu", "Koagülatif nekroz"],
                        ["Piknozun tanımı", "Çekirdeğin büzüşüp aşırı bazofilik olması", "Çekirdeğin eriyip solması (Karyolizis)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] En erken morfolojik bulgu: Hücresel şişme (hidropik değişim).",
                "📌 [SINAV SPOTU] İskemide doku mimarisinin günlerce korunduğu tip: Koagülatif nekroz.",
                "📌 [SINAV SPOTU] Püy, apse ve beyin infarktının nekroz tipi: Sıvılaşma (likefaksiyon) nekrozu.",
                "📌 [SINAV SPOTU] Kuru gangren koagülatif nekrozdur; enfeksiyon eklenince ıslak gangren (sıvılaşma) olur."
            ],
            "medicalTerms": [
                {"term": "Sınav Spotu", "explanation": "Sınavlarda doğrudan soru kökü veya doğru yanıt seçeneği olarak çıkan yüksek verimli bilgidir."},
                {"term": "Tuzak Şık", "explanation": "Öğrencinin dikkatsizliğini veya kavram kargaşasını ölçmek için konulan çeldirici seçenektir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Sınav Spotları Tablosu",
                    ["Soru Kalıbı", "Doğru Seçenek", "Patolojik İlke"],
                    [
                        [("En sık hasar nedeni", False), ("Hipoksi ve İskemi", True, "Etiyoloji"), ("Vasküler tıkanma sıklığı", False)],
                        [("En erken morfolojik bulgu", False), ("Hücresel Şişme", True, "Erken Değişiklik"), ("Na+/K+ pompa durması", False)],
                        [("Beyin enfarktüsü tipi", False), ("Sıvılaşma Nekrozu", True, "İstisna"), ("Lipid zenginliği ve erime", False)],
                        [("Nükleus büzüşmesi", False), ("Piknoz", True, "Nükleer Terim"), ("Aşırı kromatin yoğunlaşması", False)]
                    ]
                ),
                make_cloze(
                    "Hücre hasarının en erken morfolojik bulgusu hücresel şişmedir.",
                    "hücresel şişmedir",
                    "Erken Değişiklik"
                )
            ]
        },
        {
            "slideNumber": 98,
            "title": "Hücre Hasarından Nekroza: Patofizyolojik Büyük Entegrasyon",
            "subtitle": "Moleküler başlangıçtan makroskobik skarlaşmaya kadar tüm akış",
            "badge": "Büyük Entegrasyon",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre hasarı ve nekroz sürecini bir film şeridi gibi baştan sona zihnimizde canlandırdığımızda, "
                "patolojinin neden tüm klinik branşların temeli olduğu berraklaşır: İskemi veya toksin "
                "hücreye çarpar → Mitokondride ATP biter → Na+/K+ pompası durur → Sodyum ve su dolarak "
                "hücresel şişme ve blebler oluşur (geri dönüşümlü evre).\n\n"
                "> [TEMEL İLKE] Hasar sürerse: Ca2+ sitozole hücum eder → Fosfolipazlar zarları deler → "
                "Mitokondride amorf kalsiyum birikir → Lizozomlar patlar ve otoliz başlar (Point of No Return!)\n\n"
                "Çekirdek piknoz, karyoreksis ve karyolizisle erir; sitoplazma parlak pembe eozinofilik ve "
                "camsı olur; hücre zarı yırtılarak enzimler kana dökülür; çevreye dolan nötrofiller enkazı "
                "temizler ve doku nihayet fibröz bir skar dokusuyla iyileşir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Geri Dönüşümlü Faz", "desc": "Membran sağlam, iyon dengesi bozuk, şişme ve yağlanma hakimdir.", "isKey": True},
                    {"title": "Geri Dönüşümsüz Faz", "desc": "Mitokondri ve membran çöker, kalsiyum enzimleri yıkar, otoliz başlar.", "isKey": True},
                    {"title": "Nekroz ve Onarım", "desc": "Hayalet hücreler, nükleer erime, nötrofil infiltrasyonu ve fibröz skardır.", "isKey": True}
                ],
                "table": {
                    "title": "Hücre Hasarının Eksiksiz Evreleri",
                    "headers": ["Aşama", "Temel Hücresel Olay", "Klinik / Morfolojik Yansıma"],
                    "rows": [
                        ["1. Başlangıç", "İskemi, toksin veya stres maruziyeti", "Fonksiyonel duraklama (kasılma durur)"],
                        ["2. Geri Dönüşümlü", "ATP azalması, Na+ girişi, ER şişmesi", "Bulanık şişme, hidropik değişim, steatoz"],
                        ["3. Eşik Aşımı", "Ca2+ fırlaması, MPTP açılması, zar rüptürü", "Point of no return, kanda enzim artışı"],
                        ["4. Nekroz Morfolojisi", "Protein denatürasyonu, nükleer erime", "Artmış eozinofili, piknoz → karyolizis"],
                        ["5. Enflamasyon & Skar", "Nötrofil heterolizi, makrofaj fagositozu", "Granülasyon dokusu ve kalıcı kollajenöz skar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Tüm sürecin mantığı: Fonksiyon kaybı → Hücre ölümü → EM değişiklikleri → Işık mikroskobisi → Makroskobik skardır.",
                "📌 [YÜKSEK VERİM] Hücre zarı sağlam kaldığı sürece iyileşme mümkündür; membran parçalandığı anda nekroz kaçınılmazdır."
            ],
            "medicalTerms": [
                {"term": "Hücresel Entegrasyon", "explanation": "Moleküler, mikroskobik ve klinik olayların tek bir patofizyolojik zincirde birleşmesidir."},
                {"term": "Enzimatik Heteroliz", "explanation": "Ölü dokunun komşu kandan gelen nötrofil ve monosit enzimleri tarafından sindirilmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hasardan Skara Büyük Patoloji Zinciri",
                    [
                        "1. İskemik Başlangıç: Arter tıkanır, mitokondriyal ATP sentezi durur.",
                        "2. Erken Şişme: Na+/K+ ATPaz durur, hücre içine sodyum ve su dolar (Geri dönüşümlü).",
                        "3. Geri Dönüşsüz Eşik: Sitozolik kalsiyum fırlar, fosfolipazlar zarları deler ve enzimler kana sızar.",
                        "4. Nükleer ve Sitoplazmik Nekroz: Çekirdek piknozdan karyolizise erir, sitoplazma eozinofilik ve camsı olur.",
                        "5. Lökosit Temizliği ve Skar: Nötrofil ve makrofajlar enkazı temizler; fibroblastlar kollajenöz skar dokusu kurar."
                    ]
                ),
                make_cloze(
                    "Hücre hasarında geri dönüşümlü faz ile nekroz arasındaki en kritik hücresel sınır çizgisi membran bütünlüğünün korunmasıdır.",
                    "membran bütünlüğünün korunmasıdır",
                    "Temel Ayrım Çizgisi"
                )
            ]
        },
        {
            "slideNumber": 99,
            "title": "Hücre Hasarı ve Nekroz - I Dersinin Temel Çıkarımları",
            "subtitle": "Klinik hekimlik pratiği için vazgeçilmez patolojik ilkeler",
            "badge": "Klinik Çıkarım",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre Hasarı ve Nekroz - I dersini tamamlarken, geleceğin hekimi olarak klinik pratiğinize "
                "rehberlik edecek temel ilkeleri özetliyoruz: 1) Zaman hayattır: İskemik miyokard ve nöron "
                "hasarında ne kadar erken reperfüzyon sağlanırsa 'point of no return' aşılmadan o kadar çok "
                "hücre kurtarılır.\n\n"
                "> [TEMEL İLKE] 2) Enzimler dokunun aynasıdır: Kanda troponin veya karaciğer transaminazlarının "
                "yükselmesi, ilgili organda membran rüptürü ve geri dönüşümsüz nekrozun başladığını belgeler.\n\n"
                "3) Nekroz kalıbı etiyolojiyi gösterir: Soluk enfarkt katı organ iskemisini, sıvılaşma "
                "beyin iskemisini veya apseleri, gangren ise ekstremite vasküler yetersizliğini işaret eder."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Zamanın Önemi", "desc": "İskemi süresi sınırlandırılarak geri dönüşümsüz nekroz engellenebilir.", "isKey": True},
                    {"title": "Biyobelirteç Değeri", "desc": "Enzim yüksekliği membran delinmesinin kesin klinik kanıtıdır.", "isKey": True},
                    {"title": "Kalıp Rehberliği", "desc": "Nekroz tipi hekimi doğrudan başlatıcı etiyolojik nedene götürür.", "isKey": True}
                ],
                "table": {
                    "title": "Klinik Çıkarımlar Rehberi",
                    "headers": ["Patolojik İlke", "Klinik Karşılığı", "Hekimlik Yaklaşımı"],
                    "rows": [
                        ["İskemi Toleransı Sınırlıdır", "Miyokard 20-30 dk, beyin 3-5 dk", "Acil damar açma (Trombektomi, Anjiyoplasti)"],
                        ["Membran Yırtılması Enzim Salar", "Troponin ve transaminaz yüksekliği", "Organ hasarının derecesini ve takibini belirleme"],
                        ["Apse Sıvılaşma Nekrozudur", "Antibiyotik avasküler püy merkezine giremez", "Cerrahi drenaj ve debridman şarttır"],
                        ["Islak Gangren Sepsis Yapar", "Demarkasyon hattı beklemeden ilerler", "Acil cerrahi amputasyonla hayat kurtarma"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] 'Point of no return' mitokondri ve membran fonksiyonlarının geri kazanılamaz çöküşüdür.",
                "📌 [YÜKSEK VERİM] Patoloji, moleküler biyoloji ile yatak başındaki klinik hasta yönetimi arasındaki en sağlam köprüdür."
            ],
            "medicalTerms": [
                {"term": "Trombektomi", "explanation": "Tıkanmış serebral veya koroner arterdeki pıhtının anjiyografik olarak mekanik çıkarılmasıdır."},
                {"term": "Debridman", "explanation": "Yara tabanındaki nekrotik enfekte dokuların cerrahi olarak tamamen temizlenmesidir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "İskemik dokuda biyokimyasal hücre ölümü mikroskop altındaki morfolojik değişikliklerden çok daha önce gerçekleşir.",
                    "önce",
                    "Zaman Kuralı"
                ),
                make_active_recall(
                    "Klinik pratikte bir hastada kanda organa özgü enzimlerin (ör. Troponin veya ALT) yükselmesi hücresel düzeyde neyin kesin kanıtıdır?",
                    "Hücre zarlarının (plazma membranının) geri dönüşümsüz olarak parçalandığının ve ilgili organda nekrozun başladığının kesin kanıtıdır; çünkü geri dönüşümlü hasarda membran delinmez ve enzimler kana sızamaz."
                )
            ]
        },
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Büyük Sentez ve Final İstasyonu",
            "subtitle": "Hücre Hasarı ve Nekroz - I dersinin tüm kazanımlarının eksiksiz final özeti",
            "badge": "Final Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 10,
            "synthesisNarrative": (
                "Tebrikler! Kurul 1 Tıbbi Patoloji müfredatının en temel ve en kapsamlı derslerinden biri olan "
                "'Hücre Hasarı ve Nekroz - I' dersini tam 100 atomik adımda, tüm morfolojik, biyokimyasal "
                "ve klinik boyutlarıyla başarıyla tamamladınız. Homeostazdan geri dönüşümlü hidropik şişmeye, "
                "geri dönüşümsüz mitokondri krizinden nekroz morfolojisine, koagülatif enfarktlardan "
                "sıvılaşma apselerine ve gangrene kadar tüm spektrumu derinlemesine öğrendiniz.\n\n"
                "> [FİNAL VURGUSU] Aşağıdaki son 3 akıl kartını tamamlayarak toplam 30 akıl kartlık büyük "
                "öğrenme envanterinizi mühürleyin. Bu bilgiler sonraki tüm kurul ve klinik stajlarınızda en büyük gücünüz olacaktır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "100 Adım Tamamlandı", "desc": "Hücre hasarı ve nekroz kavramları eksiksiz sentezlendi.", "isKey": True},
                    {"title": "30 Akıl Kartı", "desc": "10 kontrol noktasında 30 temel klinik patoloji kartı hafızaya alındı.", "isKey": True},
                    {"title": "Tam Klinik Hazırlık", "desc": "TUS ve kurul sınavlarının tüm soru tiplerine tam hakimiyet sağlandı.", "isKey": True}
                ],
                "table": {
                    "title": "Hücre Hasarı ve Nekroz - I Büyük Özet Tablosu",
                    "headers": ["Konu Başlığı", "Temel Mekanizma", "En Kritik Sınav İlkesi"],
                    "rows": [
                        ["Hücre Hasarı", "Homeostazın korunamaması", "En sık neden hipoksi ve iskemidir"],
                        ["Geri Dönüşümlü Hasar", "Na+/K+ ATPaz pompa yetmezliği", "En erken bulgu hücresel şişmedir (membran intakt)"],
                        ["Geri Dönüşümsüz Hasar", "Mitokondri ve membran çöküşü", "Amorf kalsiyum yoğunlukları ve enzim sızıntısı"],
                        ["Nekroz Morfolojisi", "Protein denatürasyonu + RNA kaybı", "Artmış eozinofili, piknoz → karyoreksis → karyolizis"],
                        ["Koagülatif Nekroz", "Asidozla protein denatürasyonu", "Doku mimarisi korunur (hayalet hücreler)"],
                        ["Sıvılaşma Nekrozu", "Enzimatik litik hidroliz baskınlığı", "Beyin infarktı ve bakteriyel apseler"],
                        ["Gangrenöz Nekroz", "Klinik terim; koagülatif +/- sıvılaşma", "Kuru (mumyalaşmış), ıslak (çürümüş), gazlı (krepitasyon)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] En erken geri dönüşümlü bulgu: Hücresel şişme (hidropik değişim); en erken mikroskobik nekroz bulgusu (kalpte): Dalgalı lifler.",
                "📌 [SINAV SPOTU] İskemik katı organlarda Koagülatif; iskemik beyinde Sıvılaşma; diyabetik ayakta Islak gangren gelişir."
            ],
            "medicalTerms": [
                {"term": "Hücresel Homeostaz", "explanation": "Hücrenin iç fizyolojik dengesini koruma yeteneğidir; kaybı hücre hasarını başlatır."},
                {"term": "Nekroz", "explanation": "Canlı organizmada hücre zarlarının parçalanmasıyla gelişen daima patolojik ve inflamatuar hücre ölümüdür."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-028",
                    "Hücre hasarının 'en erken geri dönüşümlü bulgusu' ile 'geri dönüşümsüzlüğün en kesin ultrastrüktürel bulgusu' sırasıyla nelerdir?",
                    "En erken geri dönüşümlü bulgu ATP azalmasına bağlı Na+/K+ ATPaz pompa yetmezliği sonucu oluşan 'Hücresel Şişme'dir (hidropik değişim); geri dönüşümsüzlüğün en kesin bulgusu ise elektron mikroskobunda mitokondri matriksinde görülen 'Büyük Amorf Kalsiyum Yoğunlukları' ve geniş membran yırtıklarıdır."
                ),
                make_flashcard(
                    "fc-k1-04-029",
                    "Nekrozda izlenen nükleer değişikliklerin kronolojik sırası ve anlamları nelerdir?",
                    "1) Piknoz: Kromatinin büzüşerek nükleusun aşırı koyu siyah diske dönmesi, 2) Karyoreksis: Piknotik çekirdeğin parçalanarak nükleer toza dönüşmesi, 3) Karyolizis: DNAaz enzimleriyle DNA'nın tamamen eritilerek çekirdeğin mikroskopta silinmesidir."
                ),
                make_flashcard(
                    "fc-k1-04-030",
                    "Koagülatif nekroz, Sıvılaşma nekrozu ve Gangrenöz nekrozun en tipik klinik prototipleri hangileridir?",
                    "Koagülatif nekrozun prototipi Miyokard ve Böbrek enfarktüsleridir; Sıvılaşma nekrozunun prototipi Piyojenik apseler ve Beyin iskemik infarktlarıdır; Gangrenöz nekrozun prototipi ise periferik arter tıkanıklığı ve diyabette görülen Alt Ekstremite (Ayak) gangrenleridir."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Final İstasyonu Sentezi: Bir tıp öğrencisi olarak 'Koagülatif Nekroz' ile 'Sıvılaşma Nekrozu' arasındaki temel felsefi ve biyolojik farkı tek bir cümleyle nasıl özetlersiniz?",
                    "Koagülatif nekrozda asidoz enzimleri de dondurarak doku mimarisini günlerce ayakta tutan bir protein pıhtılaşmasıdır; sıvılaşma nekrozunda ise litik enzimler doku mimarisini anında eriterek akışkan bir sıvıya veya kaviteye çeviren proteolitik bir sindirimdir."
                ),
                make_cloze(
                    "Hücre hasarı ve nekroz konusunda geri dönüşümlü faz ile nekroz arasındaki en kesin biyokimyasal gösterge membran bütünlüğünün kaybıdır.",
                    "membran bütünlüğünün kaybıdır",
                    "Final İlkesi"
                )
            ]
        }
    ]
