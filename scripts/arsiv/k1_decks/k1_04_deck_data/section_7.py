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
            "slideNumber": 60,
            "title": "Karyolizis (Karyolysis): Nükleer Erime ve Çekirdeğin Silinmesi",
            "subtitle": "DNAaz aktivasyonu, bazofili kaybı ve nükleusun tamamen kaybolması",
            "badge": "Karyolizis",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Karyolizis, nekroz sürecinde nükleer yıkımın nihai ve geri dönüşsüz son evresidir. "
                "Lizozomal membranların yırtılmasıyla sitozole ve nükleusa ulaşan deoksiribonükleaz (DNAaz) "
                "enzimleri, nükleer DNA'yı fosfodiester bağlarından sindirmeye başlar. DNA parçalandıkça "
                "negatif yükler ve bazofilite ortadan kalkar.\n\n"
                "> [SINAV SPOTU] Karyoliziste nükleusun mavi (bazofilik) rengi yavaşça solar; çekirdek adeta "
                "bir silgiyle silinmiş gibi silikleşir ve 1-2 gün içinde mikroskopta tamamen görünmez hale gelir.\n\n"
                "Geride sadece hücresel dış sınırları ve pembe sitoplazması kalmış olan 'hayalet hücre' kalır. "
                "Bu tablo koagülatif nekrozun mikroskobik tanısının omurgasıdır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "DNAaz Aktivasyonu", "desc": "Nükleusun lizozomal DNAaz enzimleri tarafından kimyasal olarak eritilmesidir.", "isKey": True},
                    {"title": "Bazofili Kaybı", "desc": "Mavi renkli nükleus boyanmasının solup pembeleşerek silinmesidir.", "isKey": True},
                    {"title": "Akarion (Çekirdeksizlik)", "desc": "1-2 gün sonra nekroz alanında hiçbir çekirdeğin kalmamasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Karyolizis Mekanizması",
                    "headers": ["Parametre", "Biyokimyasal Olay", "Mikroskobik Görüntü"],
                    "rows": [
                        ["Başlangıç", "DNAaz nükleer kromatini hidrolize eder", "Koyu mavi nükleus rengi açılır, grileşir"],
                        ["İlerleme", "Fosfodiester bağları tamamen kopar", "Çekirdek sınırları silinir, 'hayalet çekirdek'"],
                        ["Bitiş (1-2 Gün)", "Nükleer materyal tamamen erir ve dağılır", "Çekirdek tamamen kaybolmuştur (Akarion)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Karyolizis: DNAaz aktivasyonu sonucu nükleus bazofilisinin solması ve çekirdeğin tamamen eriyip kaybolmasıdır.",
                "📌 [YÜKSEK VERİM] 1-2 gün içinde nekrotik hücredeki çekirdek tamamen yok olur; bu durum koagülatif nekrozda hayalet hücreyi oluşturur."
            ],
            "medicalTerms": [
                {"term": "Karyolizis", "explanation": "DNAaz etkisiyle çekirdeğin boyanma özelliğini yitirip eriyerek tamamen kaybolmasıdır."},
                {"term": "DNAaz", "explanation": "DNA zincirlerini monomer ve oligonükleotidlere parçalayan hidrolitik enzimdir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "DNAaz enzimleri tarafından nükleer DNA'nın eritilmesi sonucu çekirdeğin solup kaybolmasına karyolizis denir.",
                    "karyolizis",
                    "Son Nükleer Evre"
                ),
                make_active_recall(
                    "Nekrozda nükleer değişikliklerin kronolojik sırası nasıldır?",
                    "Piknoz (çekirdeğin büzüşüp koyulaşması) → Karyoreksis (çekirdeğin nükleer toz halinde parçalanması) → Karyolizis (DNAaz ile çekirdeğin eriyip tamamen silinmesi)."
                )
            ]
        },
        {
            "slideNumber": 61,
            "title": "Nükleer Değişikliklerin Zaman Akışı ve Karşılaştırması",
            "subtitle": "İskemiden tam çekirdek kaybına uzanan 48 saatlik kronoloji",
            "badge": "Kronoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre zedelenmesinde nükleer değişikliklerin ortaya çıkışı ve ilerleyişi belirli bir zaman "
                "akışına bağlıdır. İskeminin ilk 4 saatinde çekirdek henüz normal veya hafif kromatin "
                "topaklanması gösterirken; 4-12. saatler arasında piknoz ve erken karyoreksis belirir.\n\n"
                "> [TEMEL İLKE] 24-48 saat geçtiğinde karyolizis tamamlanır; ölü hücrelerin neredeyse tamamı "
                "çekirdeksiz hale gelir ve çevreye sızan lökositler alanı doldurur.\n\n"
                "Apoptozda ise nükleer değişiklikler çok daha hızlı (dakikalar-saatler) gerçekleşir ve kaspaz "
                "aracılı düzenli internükleozomal kesimle apoptotik cisimciklere paketlenir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "İlk 4 Saat", "desc": "Nükleus ışık mikroskobunda henüz normal görünebilir.", "isKey": True},
                    {"title": "4 - 12 Saat", "desc": "Piknoz ve erken karyoreksis açıkça seçilir.", "isKey": True},
                    {"title": "24 - 48 Saat", "desc": "Karyolizis tamamlanır; dokuda çekirdeksiz ölü hücreler kalır.", "isKey": True}
                ],
                "table": {
                    "title": "Nükleer Değişikliklerin Zaman Çizelgesi",
                    "headers": ["Zaman Aralığı", "Baskın Nükleer Değişiklik", "Işık Mikroskobu Görünümü"],
                    "rows": [
                        ["0 - 4 Saat", "Hafif kromatin kümelenmesi", "Çekirdek yerinde ve sağlam görünür"],
                        ["4 - 12 Saat", "Piknoz", "Büzüşmüş, homojen siyah-mor nükleus"],
                        ["12 - 24 Saat", "Karyoreksis", "Parçalanmış nükleer toz kırıntıları"],
                        ["24 - 48 Saat", "Karyolizis", "Silikleşmiş, solmuş ve kaybolmuş çekirdekler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozun 24-48. saatinde karyolizis tamamlanır ve mikroskopta çekirdek tamamen kaybolur.",
                "📌 [YÜKSEK VERİM] Patolog mikroskopta çekirdeksiz hayalet hücreler gördüğünde enfarktüsün en az 1-2 günlük olduğunu anlar."
            ],
            "medicalTerms": [
                {"term": "Nükleer Kronoloji", "explanation": "Hücre ölümünden sonra çekirdeğin ufalma ve erime basamaklarının zamansal takibidir."},
                {"term": "Akarion", "explanation": "Histolojide çekirdeğini tamamen kaybetmiş ölü hücre durumunu tanımlayan terimdir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Çekirdek Kaybının Zamansal Seyri",
                    [
                        "1. İlk Saatler: Hücre öldüğü halde çekirdek ışık mikroskobunda seçilebilir.",
                        "2. 6. Saat: Asidozla nükleus büzülür ve piknoz oturur.",
                        "3. 18. Saat: Nükleer laminler parçalanır, karyoreksis ile nükleer toz saçılır.",
                        "4. 36. Saat: DNAaz aktivitesiyle karyolizis gerçekleşir, nükleus silinir.",
                        "5. 48. Saat: Doku tamamen çekirdeksiz koagüle hayalet hücrelere döner."
                    ]
                ),
                make_cloze(
                    "Nekrozda nükleer karyolizis tamamlandığında hücreler çekirdeklerini tamamen kaybederek hayalet hücre haline gelir.",
                    "karyolizis",
                    "Nükleer Erime"
                )
            ]
        },
        {
            "slideNumber": 62,
            "title": "Nükleer Değişiklikler: Nekroz vs Apoptoz Ayrımı",
            "subtitle": "Kromatin marjinasyonu, internükleozomal kesim ve apoptotik cisimcikler",
            "badge": "Ayırıcı Tanı",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Nekroz ile apoptozun nükleer parçalanma biçimleri iki ölüm tipinin altında yatan moleküler "
                "mekanizma farkını kusursuz şekilde yansıtır. Nekrozda endonükleazlar kontrolsüz aktive olur "
                "ve DNA'yı gelişi güzel parçalayarak karyolizisle eritir. Elektroforezde DNA 'smear' "
                "(yayma) şeklinde amorf bir leke verir.\n\n"
                "> [TEMEL İLKE] Apoptozda ise kaspazla aktive olan CAD (Kaspazla aktive deoksiribonükleaz), "
                "DNA'yı yalnız nükleozomlar arasındaki bağlayıcı bölgelerden düzenli olarak 180-200 baz çiftlik "
                "katlar halinde keser; jelde tipik 'DNA merdiveni' (DNA ladder) oluşturur.\n\n"
                "Apoptozda kromatin nükleer zarın altına hilal şeklinde (marjinasyon) dizilir ve zarla "
                "çevrili apoptotik cisimciklere bölünür; nekrozda ise zar patlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "DNA Merdiveni", "desc": "Apoptozda 180-200 baz çiftlik internükleozomal düzenli kesimdir.", "isKey": True},
                    {"title": "Smear Deseni", "desc": "Nekrozda gelişigüzel rastgele DNA erimesinin oluşturduğu lekedir.", "isKey": True},
                    {"title": "Kromatin Marjinasyonu", "desc": "Apoptozda kromatinin nükleer zar altında hilal oluşturmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Nükleer Yıkım: Nekroz vs Apoptoz",
                    "headers": ["Parametre", "Nekroz", "Apoptoz"],
                    "rows": [
                        ["DNA Kesim Patern", "Gelişigüzel, rastgele parçalanma", "Düzenli, internükleozomal kesim (180-200 bp)"],
                        ["Jel Elektroforezi", "Smear (yaygın leke) görünümü", "DNA ladder (merdiven) görünümü"],
                        ["Nükleer Membran", "Parçalanır, kırıntılar sitoplazmaya sızar", "Sağlam kalır, apoptotik cisimciklere paketlenir"],
                        ["Kromatin Dağılımı", "Piknoz ve karyolizisle homojen erime", "Nükleer membran altında hilal şeklinde kümelenme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Agaroz jel elektroforezinde düzenli 'DNA merdiveni' (ladder) görülmesi Apoptozun; düzensiz 'smear' görülmesi Nekrozun kanıtıdır.",
                "📌 [YÜKSEK VERİM] Apoptozda DNA nükleozom aralarından 180-200 baz çifti ve katları şeklinde düzenli kesilir."
            ],
            "medicalTerms": [
                {"term": "DNA Merdiveni", "explanation": "Apoptozda internükleozomal kesimle oluşan 180-200 bp katlarının elektroforezde basamak gibi dizilmesidir."},
                {"term": "Smear Deseni", "explanation": "Nekrozda rastgele DNA parçalanmasının jelde oluşturduğu sürekli bulanık boyanma lekesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "DNA Parçalanma Desenleri",
                    "Apoptoz (Düzenli İntihar)",
                    "Nekroz (Kaotik Yıkım)",
                    [
                        "Internükleozomal düzenli kesim",
                        "180 - 200 baz çiftlik fragmanlar",
                        "Jelde tipik 'DNA Merdiveni' (ladder)",
                        "Kaspaz bağımlı kontrollü nükleaz"
                    ],
                    [
                        "Gelişigüzel rastgele DNA lizisi",
                        "Her boyutta dağınık nükleik asit parçaları",
                        "Jelde düzensiz 'Smear' (yayma lekesi)",
                        "Kalsiyum bağımlı kaotik endonükleazlar"
                    ]
                ),
                make_cloze(
                    "Agaroz jel elektroforezinde 180-200 baz çifti katları şeklinde DNA merdiveni oluşumu apoptoz için karakteristiktir.",
                    "apoptoz",
                    "Ölüm Tipi"
                )
            ]
        },
        {
            "slideNumber": 63,
            "title": "Nekrozun Sitoplazmik ve Nükleer Değişikliklerinin Bütünleşik Özeti",
            "subtitle": "Mikroskop altında nekrozu canlı dokudan ayıran tam tanısal liste",
            "badge": "Tam Özet",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patoloji uzmanı mikroskop başına geçtiğinde bir dokuda nekroz tanısı koymak için sitoplazma "
                "ve çekirdekteki bulguları bir bütün halinde değerlendirir. Nekrotik alanda sitoplazma: "
                "1) Koyu pembe (artmış eozinofilik), 2) Camsı homojen (glikojen yok), 3) Vakuolize "
                "(güve yeniği organel sindirimi).\n\n"
                "> [TEMEL İLKE] Çekirdekte ise: Önce büzülme (piknoz), sonra ufalanma (karyoreksis), nihayet "
                "erime (karyolizis) ve tam kayıp izlenir; doku sınırları ise koagülatif nekrozda korunur.\n\n"
                "Bu değişikliklerin çevresinde canlı dokudan gelen nötrofil infiltrasyonu, konjesyon ve "
                "ödem bulunur. Bu liste histopatolojinin en temel alfabelerinden biridir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Sitoplazmik Üçlü", "desc": "Artmış eozinofili + Camsı homojenlik + Güve yeniği vakuolleri.", "isKey": True},
                    {"title": "Nükleer Üçlü", "desc": "Piknoz + Karyoreksis + Karyolizis ve tam çekirdek kaybı.", "isKey": True},
                    {"title": "Çevre Yanıtı", "desc": "Canlı dokunun nekrotik sınıra verdiği nötrofilik infiltrasyon kuşağıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Nekrozun Tam Histopatolojik Kontrol Listesi",
                    "headers": ["Bölge", "Histolojik Değişiklik", "Görünüm Karşılığı"],
                    "rows": [
                        ["Sitoplazma", "Protein denatürasyonu + RNA kaybı", "Parlak koyu pembe eozinofili"],
                        ["Sitoplazma", "Glikojen tüketimi", "Camsı pürüzsüz homojenlik"],
                        ["Sitoplazma", "Organel otolizi", "Güve yeniği mikro-vakuolizasyon"],
                        ["Nükleus", "Kromatin kondansasyonu", "Piknoz (siyah büzük çekirdek)"],
                        ["Nükleus", "Zar yırtılması", "Karyoreksis (nükleer toz parçacıkları)"],
                        ["Nükleus", "DNAaz sindirimi", "Karyolizis (erime ve tam çekirdeksizlik)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozun sitoplazmik bulguları: Artmış eozinofili, camsı homojenlik, vakuolizasyon; nükleer bulguları: Piknoz, karyoreksis, karyolizisdir.",
                "📌 [YÜKSEK VERİM] Bu bulguların tamamı dokuda canlılığın bittiğini ve hücresel ölümün gerçekleştiğini kanıtlar."
            ],
            "medicalTerms": [
                {"term": "Histopatolojik Kontrol Listesi", "explanation": "Bir lezyonun mikroskobik tanısını doğrulamak için taranan kriterler bütünüdür."},
                {"term": "Nötrofilik Kuşak", "explanation": "Nekrotik alanı canlı sağlam dokudan ayıran yoğun lökosit sınır hattıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Nekroz Tanı Kriterleri",
                    ["Hücre Kısmı", "Klasik Değişiklik", "Patolojik İsim"],
                    [
                        [("Sitoplazma", False), ("Denatüre protein + RNA kaybı", True, "Boyanma Değişimi"), ("Artmış eozinofili", False)],
                        [("Sitoplazma", False), ("Glikojen tükenmesi", True, "Karbonhidrat Yokluğu"), ("Camsı homojen görünüm", False)],
                        [("Nükleus", False), ("Çekirdeğin büzüşmesi", True, "Yoğunlaşma"), ("Piknoz", False)],
                        [("Nükleus", False), ("Çekirdeğin parçalanması", True, "Ufalanma"), ("Karyoreksis", False)],
                        [("Nükleus", False), ("Çekirdeğin erimesi", True, "DNAaz Sindirimi"), ("Karyolizis", False)]
                    ]
                ),
                make_cloze(
                    "Nekrozda nükleer DNA'nın DNAaz enzimleri tarafından eritilerek çekirdeğin solup kaybolmasına karyolizis denir.",
                    "karyolizis",
                    "Nükleer Erime"
                )
            ]
        },
        {
            "slideNumber": 64,
            "title": "Kazeöz, Yağ ve Fibrinoid Nekroza Genel Bakış",
            "subtitle": "Sonraki derslerde derinleştirilecek diğer 3 doku nekrozu kalıbı",
            "badge": "Ön Bakış",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Doku nekrozu kalıpları içinde koagülatif, likefaksiyon ve gangrenöz nekroz en sık rastlanan "
                "ilk üç tip olmakla birlikte; spesifik klinik tablolarda ortaya çıkan üç özel nekroz kalıbı "
                "daha vardır: Kazeöz nekroz, Yağ nekrozu ve Fibrinoid nekroz. Bu kalıplar patoloji müfredatının "
                "ilerleyen derslerinde (Hücre Hasarı II ve İnflamasyon) çok ayrıntılı ele alınacaktır.\n\n"
                "> [TEMEL İLKE] Kazeöz nekroz tüberkülozda peynirleşme görüntüsüdür; Yağ nekrozu akut pankreatitte "
                "lipazların yağı sabunlaştırmasıdır; Fibrinoid nekroz ise damar duvarında antikor ve fibrin birikimidir.\n\n"
                "Her bir nekroz tipi kendine özgü histolojik ve klinik parmak izine sahiptir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Kazeöz Nekroz", "desc": "Tüberküloz granülomunun merkezindeki peynirimsi sarı-beyaz amorf nekrozdur.", "isKey": True},
                    {"title": "Yağ Nekrozu", "desc": "Pankreatik lipazların periton yağını eritip kalsiyum tebeşir odakları yapmasıdır.", "isKey": True},
                    {"title": "Fibrinoid Nekroz", "desc": "Malign hipertansiyon ve vaskülitlerde damar duvarında parlak pembe fibrin birikimidir.", "isKey": True}
                ],
                "table": {
                    "title": "İleri 3 Doku Nekrozu Kalıbı",
                    "headers": ["Nekroz Tipi", "Karakteristik Görünüm", "Klasik Hastalık"],
                    "rows": [
                        ["Kazeöz Nekroz", "Peynirimsi, sarı-beyaz, yapısız amorf enkaz", "Tüberküloz (Mycobacterium tuberculosis)"],
                        ["Yağ Nekrozu", "Tebeşir beyazı sabunlaşma odakları", "Akut Pankreatit, Meme Travması"],
                        ["Fibrinoid Nekroz", "Damar duvarında parlak homojen pembe birikim", "Poliarteritis Nodoza, Malign Hipertansiyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Tüberküloz enfeksiyonunun patognomonik nekroz tipi Kazeöz (peynirleşme) nekrozdur.",
                "📌 [SINAV SPOTU] Akut pankreatitte yağ asitlerinin kalsiyumla birleşmesi tebeşir beyazı Yağ Nekrozu odakları oluşturur.",
                "📌 [SINAV SPOTU] Damar duvarında antijen-antikor kompleksleri ve fibrinin birikmesi Fibrinoid nekrozdur."
            ],
            "medicalTerms": [
                {"term": "Kazeöz Nekroz", "explanation": "Tüberküloz granülomunda doku mimarisinin tamamen silinip peynirimsi enkaz bıraktığı nekrozdur."},
                {"term": "Fibrinoid Nekroz", "explanation": "Damar duvarına immün kompleks ve fibrin sızmasıyla oluşan parlak eozinofilik nekrozdur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Özel Nekroz Tipleri Karşılaştırması",
                    "Kazeöz Nekroz",
                    "Fibrinoid Nekroz",
                    [
                        "Tüberküloz enfeksiyonunda görülür",
                        "Doku mimarisi tamamen silinir",
                        "Peynirimsi sarı-beyaz amorf görünüm",
                        "Granülom kuşağı ile çevrilidir"
                    ],
                    [
                        "İmmün vaskülit ve malign hipertansiyonda görülür",
                        "Arter ve arteriyol duvarında sınırlıdır",
                        "Parlak pembe camsı fibrin birikimi",
                        "Lökosit parçalanması eşlik eder"
                    ]
                ),
                make_cloze(
                    "Tüberküloz enfeksiyonunda granülomların merkezinde izlenen peynirleşme nekrozuna kazeöz nekroz adı verilir.",
                    "kazeöz nekroz",
                    "Özel Nekroz Kalıbı"
                )
            ]
        },
        {
            "slideNumber": 65,
            "title": "Nekrozun Histokimyasal Belirteçleri ve Ayırıcı Boyalar",
            "subtitle": "H&E, PAS, Masson Trikrom, Oil Red O ve von Kossa boyaları",
            "badge": "Histokimya",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Rutin H&E boyası nekrozu tanımak için çoğu zaman yeterli olsa da, nekrozun tipini, "
                "etiyolojisini ve dokudaki kimyasal kalıntıları ayırt etmek için özel histokimyasal boyalara "
                "başvurulur. Karaciğerde yağlanma ile nekrotik vakuolizasyon şüphesinde donmuş kesitte "
                "Oil Red O uygulanır. Nekroz alanında distrofik kalsifikasyon başlamışsa kalsiyum tuzları "
                "von Kossa (siyah) veya Alizarin Red (kırmızı) ile kanıtlanır.\n\n"
                "> [TEMEL İLKE] İyileşen nekroz alanındaki kollajen ve fibröz skar dokusu Masson Trikrom boyası "
                "ile parlak mavi boyanarak canlı miyokard dokusundan (kırmızı) net olarak ayrılır.\n\n"
                "Glikojen kaybını göstermek için PAS boyası, demir pigmenti birikimi için Prusya mavisi kullanılır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Oil Red O", "desc": "Donmuş kesitte nötral trigliserit damlalarını parlak kırmızı boyar.", "isKey": True},
                    {"title": "von Kossa", "desc": "Distrofik kalsifikasyondaki kalsiyum fosfat tuzlarını siyah boyar.", "isKey": True},
                    {"title": "Masson Trikrom", "desc": "Nekroz sonrası gelişen kollajenöz skar dokusunu mavi boyar.", "isKey": False}
                ],
                "table": {
                    "title": "Nekroz Patolojisinde Özel Histokimyasal Boyalar",
                    "headers": ["Özel Boya", "Boyanan Hedef Madde", "Pozitif Boyanma Rengi"],
                    "rows": [
                        ["Hematoksilen & Eozin (H&E)", "Proteinler (Eozin) / Nükleik asit (H)", "Pembe (protein) / Koyu mavi (nükleus)"],
                        ["Oil Red O / Sudan IV", "Nötral lipidler (Trigliseritler)", "Parlak kırmızı / Turuncu"],
                        ["von Kossa / Alizarin Red", "Kalsiyum fosfat / Kalsiyum tuzları", "Siyah (von Kossa) / Kırmızı (Alizarin)"],
                        ["Masson Trikrom", "Kollajen lifleri (Fibröz skar)", "Parlak mavi (kas kırmızıdır)"],
                        ["PAS (Periodic Acid Schiff)", "Glikojen ve bazal membran", "Parlak macenta / eflatun"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Masson trikrom boyası kollajen liflerini ve skarı maviye, canlı kas liflerini kırmızıya boyar.",
                "📌 [YÜKSEK VERİM] Kalsiyum birikimlerini mikroskopta doğrulamak için von Kossa (siyah) veya Alizarin Red (kırmızı) boyaları kullanılır."
            ],
            "medicalTerms": [
                {"term": "von Kossa Boyası", "explanation": "Gümüş nitrat reaksiyonuyla dokudaki kalsiyum fosfat tuzlarını siyah çökelti olarak gösteren boyadır."},
                {"term": "Masson Trikrom", "explanation": "Kollajen bağ dokusunu canlı parankimden ayırmak için kullanılan üçlü histopatolojik boyadır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Özel Boyalar ve Hedefleri",
                    ["Boya Adı", "Hedeflenen Madde", "Ortaya Çıkan Renk"],
                    [
                        [("Oil Red O", False), ("Nötral lipid (yağ)", True, "Lipid"), ("Parlak kırmızı", False)],
                        [("von Kossa", False), ("Kalsiyum tuzları", True, "Mineral"), ("Siyah çökelti", False)],
                        [("Masson Trikrom", False), ("Kollajen lifleri (Skar)", True, "Bağ Dokusu"), ("Parlak mavi", False)],
                        [("PAS Boyası", False), ("Glikojen ve karbonhidrat", True, "Polisakkarit"), ("Parlak macenta", False)]
                    ]
                ),
                make_cloze(
                    "Nekroz sonrası gelişen fibröz skar dokusundaki kollajen liflerini maviye boyayan özel patoloji boyası Masson trikrom boyasıdır.",
                    "Masson trikrom boyasıdır",
                    "Histokimyasal Boya"
                )
            ]
        },
        {
            "slideNumber": 66,
            "title": "İskemik Enfarktlarda Renk Ayrımı: Soluk (Beyaz) vs Kırmızı (Hemorajik)",
            "subtitle": "Katı organlar ile çift dolaşımlı ve gevşek organların patolojisi",
            "badge": "Enfarktüs Tipleri",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "İskemiye bağlı enfarktüsler makroskobik renklerine ve içerdikleri kan miktarına göre "
                "iki ana gruba ayrılır: 1) Soluk (beyaz/anemik) enfarktlar, 2) Kırmızı (hemorajik) enfarktlar. "
                "Soluk enfarktlar, kalp, böbrek ve dalak gibi tek ve uç arterle beslenen, doku yoğunluğu "
                "yüksek 'katı parankimatöz' organlarda arter tıkanmasıyla oluşur; doku içine kan sızamaz.\n\n"
                "> [TEMEL İLKE] Kırmızı (hemorajik) enfarktlar ise: Çift dolaşımı olan organlarda (akciğer ve "
                "karaciğer), gevşek dokularda (akciğer), venöz tıkanmalarda (over/testis torsiyonu) ve reperfüzyon sonrası oluşur.\n\n"
                "Gevşek ve çift dolaşımlı dokuda iskemik nekroz alanına komşu damarlardan kan sızar ve doku kanla boyanır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Soluk Enfarkt", "desc": "Kalp, böbrek, dalakta tek arter tıkanmasıyla oluşan kansız beyaz nekrozdur.", "isKey": True},
                    {"title": "Kırmızı Enfarkt", "desc": "Akciğer, bağırsak, testis gibi organlarda kan göllenmesiyle oluşan nekrozdur.", "isKey": True},
                    {"title": "Çift Dolaşım Kuralı", "desc": "Akciğer (pulmoner + bronşiyal arter) ve karaciğer (hepatik arter + portal ven) kırmızı enfarkt yapar.", "isKey": True}
                ],
                "table": {
                    "title": "Soluk vs Kırmızı Enfarktüs Ayırıcı Tanısı",
                    "headers": ["Özellik", "Soluk (Beyaz) Enfarkt", "Kırmızı (Hemorajik) Enfarkt"],
                    "rows": [
                        ["Tipik Organlar", "Kalp, Böbrek, Dalak", "Akciğer, İnce Bağırsak, Testis, Beyin (reperfüzyon)"],
                        ["Doku Yapısı", "Katı, yoğun hücreli parankim", "Gevşek doku, geniş venöz ağ"],
                        ["Damar Sistemi", "Tek uç arter (End-arter)", "Çift dolaşım veya zengin kollateral"],
                        ["Neden", "Arteriyel tıkanma", "Venöz obstrüksiyon (torsiyon), reperfüzyon, emboli"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Soluk enfarkt katı organlarda (kalp, böbrek, dalak); Kırmızı (hemorajik) enfarkt gevşek ve çift dolaşımlı organlarda (akciğer, bağırsak) görülür.",
                "📌 [SINAV SPOTU] Testis veya over torsiyonunda venöz drenaj tıkandığı için masif hemorajik (kırmızı) enfarktüs gelişir."
            ],
            "medicalTerms": [
                {"term": "Hemorajik Enfarkt", "explanation": "İskemik nekroz alanının içine eritrositlerin sızarak dokuyu koyu kırmızıya boyadığı enfarktüs tipidir."},
                {"term": "Çift Dolaşım", "explanation": "Bir organın iki farklı arteriyel veya vasküler kaynaktan eşzamanlı kanlanmasıdır (Akciğer ve Karaciğer)."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Enfarktüs Tipleri Karşılaştırması",
                    "Soluk (Beyaz) Enfarkt",
                    "Kırmızı (Hemorajik) Enfarkt",
                    [
                        "Kalp, böbrek ve dalakta görülür",
                        "Katı ve yoğun parankim organlarıdır",
                        "Tek bir uç arter tıkanır",
                        "Nekroz alanına kan sızamaz, doku beyazdır"
                    ],
                    [
                        "Akciğer, bağırsak ve testiste görülür",
                        "Gevşek doku veya venöz tıkanmadır",
                        "Çift dolaşım veya kollateraller vardır",
                        "Nekroz alanına masif kan dolar, doku kırmızıdır"
                    ]
                ),
                make_cloze(
                    "Akciğerde pulmoner emboli sonucu gelişen iskemik enfarktüs çift kan dolaşımı nedeniyle kırmızı enfarktüs kalıbındadır.",
                    "kırmızı enfarktüs",
                    "Enfarktüs Kalıbı"
                )
            ]
        },
        {
            "slideNumber": 67,
            "title": "İskemik Doku Hasarında Sitolojik Ayrıntılar",
            "subtitle": "Kollajen koruyuculuğu, bazal membran dayanıklılığı ve parankim kırılganlığı",
            "badge": "Sitoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "İskemi bir organı vurduğunda o organdaki tüm hücreler aynı hızda ve aynı şekilde ölmez. "
                "Yüksek metabolizmaya sahip parankim hücreleri (epitel, kas, nöron) dakikalar içinde "
                "nekroza uğrarken; destek dokusunu oluşturan stromal hücreler (fibroblastlar) ve ekstraselüler "
                "matriks elemanları (kollajen, bazal membran) iskemiye olağanüstü dirençlidir.\n\n"
                "> [TEMEL İLKE] Örneğin böbrekte iskemik hasarda tübül epiteli dökülürken tübül bazal membranı "
                "sağlam kalır; bu bazal membran iskeleti kök hücrelerin bölünerek dokuyu onarması için bir şablon sunar.\n\n"
                "Bazal membran da yırtılırsa (tübüloreksis) reepitelizasyon bozulur ve kaçınılmaz interstisyel "
                "fibrozis gelişir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Parankim Kırılganlığı", "desc": "İyon pompası ve mitokondri yükü fazla olan epitelin erken ölümüdür.", "isKey": True},
                    {"title": "Stroma Direnci", "desc": "Fibroblast ve kollajen liflerinin saatlerce iskemiden etkilenmemesidir.", "isKey": True},
                    {"title": "Bazal Membran Şablonu", "desc": "Epitel rejenerasyonu için yol gösterici anatomik kılavuzdur.", "isKey": False}
                ],
                "table": {
                    "title": "Dokudaki Hücre Tiplerinin İskemi Direnci",
                    "headers": ["Hücre / Doku Tipi", "Metabolik Hız", "İskemiye Direnç Düzeyi"],
                    "rows": [
                        ["Özelleşmiş Epitel (Böbrek, Bağırsak)", "Çok yüksek", "Düşük (30-60 dakikada nekroz)"],
                        ["Vasküler Endotel", "Orta", "Orta (1-2 saatte geçirgenlik artışı)"],
                        ["İnterstisyel Fibroblast", "Düşük", "Yüksek (Saatler boyu canlı kalır)"],
                        ["Tip IV Kollajen (Bazal Membran)", "Asellüler yapı", "Çok yüksek (Proteolitik enzimler yıkana dek dirençli)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İskemik dokuda bazal membran sağlam kaldığı sürece kök hücreler organize olarak parankimi orijinal haliyle rejenere edebilir.",
                "📌 [YÜKSEK VERİM] Parankim hücreleri ölürken stromal bağ dokusu iskeletinin ayakta kalması doku çatısını korur."
            ],
            "medicalTerms": [
                {"term": "Tübüloreksis", "explanation": "İskemik böbrek hasarında tübül bazal membranının yırtılması ve rejenere olma şansının kaybolmasıdır."},
                {"term": "Stroma", "explanation": "Organların parankim hücrelerini taşıyan destekleyici bağ dokusu ve damar çatısıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "İskemik dokuda epitel hücrelerinin rejenerasyonla dokuyu tamir edebilmesi için bazal membran bütünlüğünün korunması şarttır.",
                    "bazal membran",
                    "Anatomik Şablon"
                ),
                make_active_recall(
                    "Akut böbrek hasarında toksik hasar ile iskemik hasar arasındaki bazal membran farkı nedir?",
                    "Toksik hasarda bazal membran genellikle sağlam kalır ve rejenerasyon tam olur; ağır iskemik hasarda ise bazal membran yırtılabilir (tübüloreksis) ve tam iyileşme zorlaşır."
                )
            ]
        },
        {
            "slideNumber": 68,
            "title": "İskemik Enfarktlarda İltihabi Sınır Kuşağı",
            "subtitle": "Marjinal hiperemi, lökosit adezyonu ve sınır demarcasyonu",
            "badge": "Enflamasyon",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "İskemik bir enfarktüsün makroskobik ve mikroskobik incelemesinde en dikkat çekici "
                "bölgelerden biri, ölü doku ile canlı dokunun kesiştiği 'sınır hattı'dır (demarkasyon hattı). "
                "Nekrotik merkezde kan dolaşımı tamamen kesilmişken, bu merkeze komşu canlı dokudaki "
                "kapillerler aşırı derecede genişler (vazodilatasyon) ve eritrositlerle dolar.\n\n"
                "> [TEMEL İLKE] Bu vasküler reaksiyon nekrotik lezyonun çevresinde makroskopide parlak kırmızı, "
                "ince bir hiperemi halkası oluşturur; nekrozun sağlam dokudan ayrıldığı sınırdır.\n\n"
                "Bu sınır kuşağındaki endotel hücreleri selektin ve integrin reseptörlerini artırarak "
                "nötrofillerin damardan çıkıp nekrotik dokuya hücum etmesini sağlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Demarkasyon Hattı", "desc": "Nekrotik ölü dokuyu canlı komşu dokudan ayıran sınır çizgisidir.", "isKey": True},
                    {"title": "Marjinal Hiperemi", "desc": "Canlı sınırdaki kapillerlerin vazodilatasyonla kan dolmasıdır.", "isKey": True},
                    {"title": "Nötrofil Göçü", "desc": "Lökositlerin bu canlı damarlardan çıkarak nekroz alanına ilerlemesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Enfarktüs Sınır Kuşağının Dinamikleri",
                    "headers": ["Bölge", "Dolaşım Durumu", "Hücresel Hakimiyet"],
                    "rows": [
                        ["Nekrotik Merkez", "Sıfır perfüzyon (damarlar tıkalı)", "Çekirdeksiz hayalet hücreler, pıhtılaşmış protein"],
                        ["Demarkasyon Sınırı", "Aşırı perfüzyon (marjinal hiperemi)", "Genişlemiş kapillerler, diapedez yapan nötrofiller"],
                        ["Komşu Canlı Doku", "Normal perfüzyon", "Sağlıklı parankim hücreleri"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Soluk bir böbrek veya miyokard enfarktüsünün çevresindeki kırmızı sınır kuşağı marjinal hiperemi ve akut enflamasyondur.",
                "📌 [YÜKSEK VERİM] Demarkasyon hattı canlı vücudun nekroz alanını sınırlama ve temizleme çabasının başladığı yerdir."
            ],
            "medicalTerms": [
                {"term": "Demarkasyon Hattı", "explanation": "Nekrotik doku ile çevre canlı doku arasındaki belirgin iltihabi ayrım sınırıdır."},
                {"term": "Marjinal Hiperemi", "explanation": "Nekrozun hemen komşuluğundaki canlı damarların aşırı kanla dolarak oluşturduğu kırmızı halkadır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Enfarktüs Sınır Kuşağında Enflamasyon Başlangıcı",
                    [
                        "1. Doku Nekrozu: İskemik alandaki hücreler ölür ve sitozolik mediyatörleri salar.",
                        "2. Mediyatör Difüzyonu: Nekroz alanından komşu canlı damarlara histamin ve sitokinler yayılır.",
                        "3. Marjinal Vazodilatasyon: Canlı kapillerler genişler ve kırmızı bir hiperemi halkası oluşur.",
                        "4. Lökosit Adezyonu: Nötrofiller damar endoteline tutunur ve dokuya sızar (diapedez).",
                        "5. Nekroza Hücum: Lökositler demarkasyon hattından içeri girerek hayalet hücreleri sindirmeye başlar."
                    ]
                ),
                make_cloze(
                    "Soluk bir enfarktüsün çevresinde canlı dokunun damarsal yanıtıyla oluşan kırmızı halkaya marjinal hiperemi sınırı denir.",
                    "marjinal hiperemi",
                    "İltihabi Sınır"
                )
            ]
        },
        {
            "slideNumber": 69,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Nükleer Nekroz Evreleri",
            "subtitle": "Karyolizis, DNA merdiveni vs smear, soluk vs kırmızı enfarktlar",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 7,
            "synthesisNarrative": (
                "Yedinci kontrol noktasında, nekrozun nükleer son evresi olan karyolizisi, apoptoz ile "
                "nekrozun DNA parçalanma paternlerini ve organ enfarktlarının renk ayrımını özetliyoruz. "
                "Karyolizis DNAaz aktivitesiyle nükleusun tamamen silinmesidir.\n\n"
                "> [ÖZET VURGU] Elektroforezde DNA merdiveni Apoptozun, düzensiz smear Nekrozun kanıtıdır; "
                "soluk enfarkt katı organlarda, kırmızı enfarkt çift dolaşımlı ve gevşek dokularda görülür.\n\n"
                "Aşağıdaki 3 akıl kartını dikkatle gözden geçirerek bu temel patoloji kurallarını pekiştirin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Karyolizis", "desc": "DNAaz ile bazofilinin solması ve çekirdeğin tamamen yok olmasıdır.", "isKey": True},
                    {"title": "DNA Merdiveni", "desc": "Apoptoza özgü internükleozomal düzenli 180-200 bp kesim desenidir.", "isKey": True},
                    {"title": "Soluk vs Kırmızı", "desc": "Katı organlarda soluk; çift dolaşımlı ve gevşek organlarda kırmızı enfarkt.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 7 Sentez Tablosu",
                    "headers": ["Kavram", "Biyolojik Temel", "Klinik / Sınav Önemi"],
                    "rows": [
                        ["Karyolizis", "Lizozomal DNAaz sindirimi", "Çekirdeğin tamamen eridiği son nekroz evresi"],
                        ["DNA Merdiveni", "180-200 bp internükleozomal kesim", "Apoptozun elektroforetik altın standardı"],
                        ["Soluk Enfarkt", "Katı tek arterli organ (Böbrek/Kalp)", "Kansız beyaz koagülasyon nekrozu"],
                        ["Kırmızı Enfarkt", "Çift dolaşım ve venöz tıkanma (Akciğer)", "Kan göllenmesiyle oluşan koyu kırmızı enfarkt"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] DNA merdiveni (ladder) Apoptozun; DNA smear lekesi Nekrozun göstergesidir.",
                "📌 [SINAV SPOTU] Soluk enfarkt kalp, böbrek, dalakta; Kırmızı enfarkt akciğer ve bağırsakta görülür."
            ],
            "medicalTerms": [
                {"term": "Nükleozom", "explanation": "Sekiz histon proteininin etrafına sarılmış 146 baz çiftlik temel DNA paketleme birimidir."},
                {"term": "Torsiyon", "explanation": "Testis veya over gibi organların kendi vasküler sapı etrafında dönerek venöz dolaşımı boğmasıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-019",
                    "Karyolizis evresinde çekirdeğin mavi (bazofilik) renginin solmasının ve mikroskopta tamamen görünmez olmasının enzimatik nedeni nedir?",
                    "Lizozomlardan salınan asit deoksiribonükleaz (DNAaz) enzimlerinin DNA'yı tamamen parçalaması ve negatif yüklü fosfat gruplarının ortadan kalkmasıyla hematoksilen tutulumunun sıfırlanmasıdır."
                ),
                make_flashcard(
                    "fc-k1-04-020",
                    "Agaroz jel elektroforezinde apoptoz ile nekroz arasındaki DNA kesim deseni farkı nasıldır?",
                    "Apoptozda DNA nükleozom aralarından düzenli olarak kesildiği için jelde 180-200 baz çifti ve katlarından oluşan 'DNA Merdiveni' (ladder) görülür; nekrozda ise rastgele eridiği için homojen bir 'Smear' (leke) izlenir."
                ),
                make_flashcard(
                    "fc-k1-04-021",
                    "Neden böbrek ve dalak enfarktları soluk (beyaz) iken akciğer ve bağırsak enfarktları kırmızı (hemorajik) renktedir?",
                    "Böbrek ve dalak tek bir uç arterle beslenen yoğun katı organlardır ve dokuya kan sızamaz; akciğer ve bağırsak ise çift dolaşıma (pulmoner + bronşiyal) veya zengin kollaterallere sahip gevşek dokulardır ve nekroz alanına masif kan sızar."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 7 Sentezi: Bir organ torsiyonunda (örneğin testis torsiyonu) neden daima kırmızı (hemorajik) enfarktüs gelişir?",
                    "Çünkü ince duvarlı venler kalın duvarlı arterlerden önce basıya uğrar ve tıkanır; arteriyel kan dokuya girmeye devam ederken venöz çıkış kapalı olduğu için organ masif kanla şişer ve hemorajik nekroza uğrar."
                ),
                make_cloze(
                    "Agaroz jel elektroforezinde rastgele ve kaotik DNA yıkımını gösteren leke görünümüne smear deseni denir.",
                    "smear deseni",
                    "Elektroforez Bulgusu"
                )
            ]
        }
    ]
