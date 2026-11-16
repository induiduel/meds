# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_23_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve halk sağlığı karar verme senaryoları) ögeleri."""
    return {
        3: make_branching_logic(
            "Bir toplum sağlığı merkezinde görev yapan hekim, bölgesindeki 0-1 yaş bebek ve anne ölümlerinin yüksek olduğunu belirliyor. İlçe sağlık müdürü acil eylem planı hazırlanmasını istiyor.",
            "Toplumda anne ve bebek ölümlerini kalıcı olarak düşürmede en yüksek maliyet-etkili birinci basamak müdahale stratejisi hangisidir?",
            [
                {
                    "text": "Doğum öncesi bakım (DÖB), lohusa izlemi ve Genişletilmiş Bağışıklama Programı (GBP) kapsamındaki aşıların %95 üzerine çıkarılması",
                    "isCorrect": True,
                    "feedback": "Kusursuz Halk Sağlığı Kararı: Düzenli DÖB preeklampsi ve kanama riskini önceden yakalar; aşılar ve lohusa takibi önlenebilir bebek/anne mortalitesini %80'e varan oranda düşürür."
                },
                {
                    "text": "Bölgedeki tüm gebelerin doğrudan üçüncü basamak üniversite hastanesine elektif sezaryen için sevk edilmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Gereksiz sezaryen anne ve bebek komplikasyon riskini artırır ve birinci basamak koruyucu hekimlik ilkelerine aykırıdır."
                },
                {
                    "text": "Yalnızca yeni doğan bebeklere antibiyotik profilaksisi dağıtılması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Rutin antibiyotik direnç yaratır, anne ölümlerini veya asfiksiyi önlemez."
                }
            ]
        ),
        7: make_branching_logic(
            "Sahada bir hekim, bölgesinde bebek ölüm hızının binde 28 olduğunu ve bu ölümlerin %70'inin ilk 28 günde (neonatal dönem) gerçekleştiğini saptıyor.",
            "Neonatal ölümleri azaltmak için birinci basamakta öncelikle hangi alana odaklanılmalıdır?",
            [
                {
                    "text": "Nitelikli doğum öncesi bakım (DÖB), hastanede güvenli doğum, asfiksi önleme ve ilk hafta bebek izlemlerinin eksiksiz yapılması",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik ve Epidemiyolojik Yaklaşım: Neonatal ölümlerin temel nedenleri prematürite, asfiksi ve konjenital anomalilerdir; gebelik takibi ve hastane doğumu bunları önler."
                },
                {
                    "text": "Sadece 1 yaş üstü çocuklara ek gıda vitamin takviyesi yapılması",
                    "isCorrect": False,
                    "feedback": "Hatalı: 1 yaş sonrası müdahaleler neonatal (ilk 28 gün) mortaliteyi etkilemez."
                },
                {
                    "text": "Kırsal alanda evde ebesiz doğumların teşvik edilmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Evde yardımsız doğum neonatal ve maternal mortaliteyi katlayarak artırır."
                }
            ]
        ),
        13: make_branching_logic(
            "Birinci basamak hekimi, bölgesinde 1 yılda gerçekleşen 10 anne ölümünden 6'sının şiddetli postpartum kanama (atoni), 3'ünün preeklampsi/eklampsi nedeniyle olduğunu belirliyor.",
            "Bu ölümlerin epidemiyolojik sınıflaması ve önlenebilirlik durumu hangisidir?",
            [
                {
                    "text": "Doğrudan obstetrik anne ölümleridir ve nitelikli antenatal/postpartum bakım ile neredeyse %100 önlenebilir niteliktedir",
                    "isCorrect": True,
                    "feedback": "Kusursuz Epidemiyolojik Analiz: Atoni kanaması ve eklampsi doğrudan obstetrik nedenlerdir ve uygun sağlık hizmetiyle önlenebilir mortalite kategorisindedir."
                },
                {
                    "text": "Dolaylı obstetrik anne ölümleridir ve tıbbi müdahalelerle önlenmesi mümkün değildir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Gebeliğin doğrudan komplikasyonları doğrudan obstetrik ölümdür ve önlenebilirdir."
                },
                {
                    "text": "Tamamen tesadüfi (gebelik dışı) ölümler olup sağlık sistemiyle ilişkisizdir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Atoni ve eklampsi doğrudan gebelik patolojisidir."
                }
            ]
        ),
        17: make_branching_logic(
            "Bir hekim bir ilçede Anne Ölüm Oranı (AÖO) hesaplamak istiyor. İlçede o yıl 2.000 canlı doğum ve gebeliğe bağlı 1 anne ölümü gerçekleşmiştir.",
            "Bu ilçenin yüz binde Anne Ölüm Oranı ve ulusal ortalamaya (yüz binde 12-13) göre durumu nasıldır?",
            [
                {
                    "text": "AÖO = (1 / 2000) * 100.000 = 50'dir; Türkiye ortalamasından belirgin yüksektir ve acil önlem gerektirir",
                    "isCorrect": True,
                    "feedback": "Doğru Biyoistatistiksel Hesap: 1/2000 oran yüz binde 50'ye denk gelir; bu oran Türkiye ortalamasının (13) yaklaşık 4 katıdır."
                },
                {
                    "text": "AÖO = 1'dir ve Türkiye ortalamasından çok daha düşüktür",
                    "isCorrect": False,
                    "feedback": "Hatalı: AÖO katsayısı 100.000 canlı doğumdur, mutlak sayı oranlanmalıdır."
                },
                {
                    "text": "AÖO binde 50'dir ve hesaplanamaz",
                    "isCorrect": False,
                    "feedback": "Hatalı: AÖO binde değil yüz binde hesaplanır."
                }
            ]
        ),
        23: make_branching_logic(
            "Sağlık ocağına başvuran 28 haftalık bir gebenin ilk kez sağlık kuruluşuna geldiği ve daha önce hiç izlem yaptırmadığı saptanıyor. Kessner İndeksi'ne göre sınıflandırılmak isteniyor.",
            "İlk viziti 28. haftada (3. trimester) olan ve yalnızca 1 izlemi bulunan bu gebenin Kessner bakım kategorisi nedir?",
            [
                {
                    "text": "Yetersiz Bakım (Inadequate care) kategorisindedir",
                    "isCorrect": True,
                    "feedback": "Doğru Kessner Sınıflaması: Bakımın 3. trimesterde başlaması veya toplam izlem sayısının gestasyonel haftaya göre kritik eşiğin altında olması yetersiz bakımdır."
                },
                {
                    "text": "Yeterli Bakım (Adequate care) kategorisindedir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Yeterli bakım ilk 14 haftada başlamalı ve en az 4 izlem içermelidir."
                },
                {
                    "text": "Orta Düzey Bakım (Intermediate care) kategorisindedir",
                    "isCorrect": False,
                    "feedback": "Hatalı: 28. haftada ilk kez gelen gebe yetersiz kategorisine girer."
                }
            ]
        ),
        27: make_branching_logic(
            "Birinci basamak izleminde 17 yaşında, 5. gebeliği olan ve önceki iki doğumu arasında 11 ay bulunan bir gebe tespit ediliyor.",
            "Bu gebede anne ve perinatal ölüm riskini artıran '4 Çok Kuralı' risk faktörleri hangileridir?",
            [
                {
                    "text": "Çok genç yaş (<18), çok sayıda doğum (>4) ve çok sık doğum (<2 yıl aralık) faktörlerinin üçü birden mevcuttur",
                    "isCorrect": True,
                    "feedback": "Kusursuz Risk Analizi: 17 yaş erken yaş, 5. gebelik çok doğum, 11 ay aralık ise sık doğum riskidir."
                },
                {
                    "text": "Yalnızca çok yaşlı anne kategorisine girmektedir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Gebe 17 yaşındadır, yaşlı değil erken yaştır."
                },
                {
                    "text": "Hiçbir risk faktörü yoktur, tamamen fizyolojik bir gebeliktir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Çok genç yaş, sık doğum ve çok doğum en ağır obstetrik risk faktörleridir."
                }
            ]
        ),
        33: make_branching_logic(
            "Aile sağlığı merkezine ilk kez başvuran 8 haftalık bir gebeye Sağlık Bakanlığı protokolüne göre 1. Gebe İzlemi yapılacaktır.",
            "Bu ilk izlemde yapılması gereken standart laboratuvar ve klinik tetkik paketi hangisidir?",
            [
                {
                    "text": "Kan grubu, tam kan sayımı (Hb/Hct), tam idrar tahlili, açlık kan şekeri, TSH, HBsAg, sifiliz (VDRL/RPR) ve kan basıncı ölçümü",
                    "isCorrect": True,
                    "feedback": "Kusursuz Antenatal Yönetim: 1. izlem temel bazal parametreleri belirler; anemi, bakteriüri, tiroid hastalığı ve enfeksiyonları erken yakalar."
                },
                {
                    "text": "Yalnızca ultrasonografi ile bebeğin cinsiyetine bakılıp taburcu edilmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı: 8. haftada cinsiyet belirlenemez ve laboratuvar taramaları yapılmalıdır."
                },
                {
                    "text": "Doğrudan amniyosentez ve karyotip analizi yapılması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Amniyosentez invazivdir, rutin ilk izlem testi değildir."
                }
            ]
        ),
        37: make_branching_logic(
            "10 haftalık gebeliği olan bir kadının laboratuvarında hemoglobin 9.5 g/dl saptanıyor. Hasta daha önce hiç demir preparatı kullanmamış.",
            "Bu gebede anemi yönetimi ve demir desteği nasıl planlanmalıdır?",
            [
                {
                    "text": "Gebelikte Hb <11 g/dl anemi kabul edilir; derhal tedavi dozunda elemental demir (100-200 mg/gün) başlanmalı ve beslenme eğitimi verilmelidir",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik Karar: 1. ve 3. trimesterde Hb <11 g/dl anemidir; profilaktik doz (40-60 mg) yetersiz kalır, tedavi dozu başlanmalıdır."
                },
                {
                    "text": "Gebelikte 9.5 g/dl normal kabul edilir, hiçbir şey yapmaya gerek yoktur",
                    "isCorrect": False,
                    "feedback": "Hatalı: Hb <11 g/dl aşikar anemidir; prematürite ve düşük doğum ağırlığı riskini artırır."
                },
                {
                    "text": "Gebelik derhal sonlandırılmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı ve Tehlikeli: Demir eksikliği anemisi kolayca tedavi edilen medikal bir durumdur."
                }
            ]
        ),
        43: make_branching_logic(
            "20 haftalık bir gebeye 2. izlemde Leopold manevraları uygulanmak isteniyor. Hekim uterus fundusuna iki elini koyarak fundustaki fetal kısmı palpe ediyor.",
            "Uterus fundusunda hangi fetal kutbun (baş mı, makat mı) bulunduğunu belirleyen bu manevra hangisidir?",
            [
                {
                    "text": "1. Leopold Manevrası",
                    "isCorrect": True,
                    "feedback": "Doğru Obstetrik Muayene: 1. Leopold manevrası fundusa bakarak fetal kutbu (yuvarlak sert baş veya yumuşak geniş makat) tespit eder."
                },
                {
                    "text": "2. Leopold Manevrası",
                    "isCorrect": False,
                    "feedback": "Hatalı: 2. Leopold manevrası uterusun yan duvarlarını palpe ederek fetal sırtı (prezantasyon pozisyonunu) belirler."
                },
                {
                    "text": "4. Leopold Manevrası",
                    "isCorrect": False,
                    "feedback": "Hatalı: 4. Leopold manevrası pelvise doğru bakarak önde gelen kısmın pelvise giriş derecesini değerlendirir."
                }
            ]
        ),
        47: make_branching_logic(
            "24 haftalık bir gebede diyabet taraması planlanıyor. Hasta daha önce diyabet öyküsü olmadığını belirtiyor.",
            "Sağlık Bakanlığı rehberine göre gestasyonel diyabet taramasında altın standart yaklaşım hangisidir?",
            [
                {
                    "text": "24-28. haftalarda 75 g Oral Glukoz Tolerans Testi (OGTT) ile açlık, 1. saat ve 2. saat plazma glukoz düzeylerine bakılması",
                    "isCorrect": True,
                    "feedback": "Doğru Tarama Protokolü: 24-28. haftalar plasental hormonların insülin direncini zirveye çıkardığı evredir; 75 g OGTT tek basamaklı altın standarttır."
                },
                {
                    "text": "Yalnızca idrarda glukoz bakılması",
                    "isCorrect": False,
                    "feedback": "Hatalı: İdrarda glukoz fizyolojik glukozüri nedeniyle tanısal değildir."
                },
                {
                    "text": "Doğuma kadar hiçbir glukoz testi yapılmaması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Taranmayan GDM makrozomi, omuz distozisi ve fetal ölüm riskini artırır."
                }
            ]
        ),
        53: make_branching_logic(
            "34 haftalık bir gebe şiddetli baş ağrısı, görmede bulanıklık ve epigastrik ağrı şikayetiyle ASM'ye başvuruyor. Kan basıncı 165/110 mmHg, idrar çubuğunda protein 3+ saptanıyor.",
            "Bu gebede ön tanı nedir ve hekimin yapması gereken ilk acil müdahale hangisidir?",
            [
                {
                    "text": "Ağır Preeklampsi tablosudur; damar yolu açılıp hasta sol yan pozisyonda ivedilikle donanımlı kadın doğum aciline sevk edilmelidir",
                    "isCorrect": True,
                    "feedback": "Hayat Kurtarıcı Klinik Karar: Tansiyon >160/110, görme bozukluğu ve epigastrik ağrı yaklaşan eklampsi nöbeti ve HELLP habercisidir; acil sevk şarttır."
                },
                {
                    "text": "Basit migren atağıdır, evde karanlık odada istirahat önerilmelidir",
                    "isCorrect": False,
                    "feedback": "Ölümcül Hata: Ağır preeklampsiyi atlamak konvülsiyon (eklampsi) ve anne-bebek kaybına yol açar."
                },
                {
                    "text": "Hemen ASM'de normal doğum başlatılmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı: 34 haftalık preeklamptik hasta birinci basamakta doğurtulmaz, tersiyer merkeze sevk edilir."
                }
            ]
        ),
        57: make_branching_logic(
            "36 haftalık bir gebe ağrısız, parlak kırmızı renkli yoğun vajinal kanama ile acil birime getiriliyor. Uterus muayenede gevşek ve ağrısız bulunuyor.",
            "Bu klinik tabloda en olası ön tanı hangisidir ve hangi muayene KESİNLİKLE YAPILMAMALIDIR?",
            [
                {
                    "text": "Plasenta Previa düşünülmelidir; plasentayı yırtıp öldürücü kanamaya yol açabileceğinden dijital vajinal muayene kesinlikle yapılmamalıdır",
                    "isCorrect": True,
                    "feedback": "Hayati Obstetrik Kural: Ağrısız parlak kanamada Plasenta Previa ekarte edilmeden parmakla tuşe yapmak masif kanama ve arrest nedenidir; tanı USG ile konur."
                },
                {
                    "text": "Ablasyo plasentadır ve acil parmakla serviks açıklığına bakılmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı: Ablasyoda kanama koyu renkli ve ağrılıdır; dijital muayene kanamayı artırabilir."
                },
                {
                    "text": "Fizyolojik nişan atımıdır, hasta evine gönderilebilir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Yoğun kırmızı kanama nişan değildir, acil cerrahi patolojidir."
                }
            ]
        ),
        63: make_branching_logic(
            "Vajinal doğumdan 1 saat sonra lohusada fundusun göbek üstüne çıktığı, yumuşak sünger kıvamında olduğu ve pedlerinin hızla kanla dolduğu görülüyor.",
            "Bu postpartum atoni kanaması tablosunda hekimin ilk uygulaması gereken mekanik ve medikal tedavi ikilisi hangisidir?",
            [
                {
                    "text": "Bimanuel fundus masajı ve intravenöz Oksitosin infüzyonu",
                    "isCorrect": True,
                    "feedback": "Kusursuz Hayat Kurtarma: Bimanuel masaj miyometriyumu mekanik olarak kasar; oksitosin spiral arterleri sıkıştırarak kanamayı durdurur."
                },
                {
                    "text": "Hastaya bol buzlu su içirmek ve ayağa kaldırmak",
                    "isCorrect": False,
                    "feedback": "Hatalı: Ayağa kaldırmak senkopa yol açar ve atoniye etki etmez."
                },
                {
                    "text": "Yalnızca geniş spektrumlu antibiyotik başlayıp beklemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Atoni mekanik kasılma sorunudur, antibiyotikle durdurulamaz."
                }
            ]
        ),
        67: make_branching_logic(
            "Doğum sonrası 10. günde olan bir lohusa sol memesinde şiddetli ağrı, kızarıklık, 38.8 derece ateş ve titreme şikayetiyle başvuruyor. Sol memede kama şeklinde eritemli sert alan palpe ediliyor.",
            "Puerperal mastit tanısı konan bu lohusanın emzirme yönetimi nasıl olmalıdır?",
            [
                {
                    "text": "Etkilenen memede süt stazını önlemek için emzirmeye kesinlikle devam edilmeli veya süt sağılmalı, uygun antibiyotik başlanmalıdır",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik Yönetim: Mastitte sütün boşaltılması tedavinin temelidir; emzirmeyi kesmek apse oluşumunu tetikler."
                },
                {
                    "text": "Bebek zehirlenir endişesiyle emzirme derhal kalıcı olarak kesilmelidir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Mastitte süt bebeğe zarar vermez; sütün boşaltılmaması apseye götürür."
                },
                {
                    "text": "Meme cerrahi olarak derhal eksize edilmelidir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Apseleşmemiş mastitte cerrahi yapılmaz, medikal tedavi ve drenaj yeterlidir."
                }
            ]
        ),
        73: make_branching_logic(
            "Doğumdan sonraki 4. günde ASM'ye getirilen term bebeğin tartısında doğum ağırlığına göre %6 kayıp olduğu, hafif sarılık başladığı ancak emmesinin güçlü olduğu görülüyor.",
            "Hekimin bu bebek izlemindeki değerlendirmesi hangisi olmalıdır?",
            [
                {
                    "text": "İlk haftadaki %5-10 tartı kaybı fizyolojiktir; anne sütüne sık aralıklarla devam edilmesi ve 7-10. günde doğum tartısının kontrolü önerilmelidir",
                    "isCorrect": True,
                    "feedback": "Doğru Sağlam Çocuk Yönetimi: İlk haftadaki hafif tartı kaybı normaldir; aktif emzirme desteklenmelidir."
                },
                {
                    "text": "Bebeğe sütün yetmediği düşünülerek hazır formül mama başlanmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı: Gereksiz mama anne sütünün kesilmesine neden olur."
                },
                {
                    "text": "Bebek derhal yoğun bakıma yatırılmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı: %6 kilo kaybı stabildir, yatış endikasyonu değildir."
                }
            ]
        ),
        77: make_branching_logic(
            "4 haftalık kız bebeğin kalça muayenesinde Ortolani testinde sol kalçada hafif 'klik' hissi alınıyor. Aile bebeği geleneksel olarak sıkı kundakladığını belirtiyor.",
            "Gelişimsel Kalça Displazisi (GKD) şüphesi olan bu bebekte hekimin ilk adımı ne olmalıdır?",
            [
                {
                    "text": "Kundaklama derhal yasaklanmalı, 4-6. haftalarda Kalça USG çekilerek tanı kesinleştirilip Pavlik bandajı için yönlendirilmelidir",
                    "isCorrect": True,
                    "feedback": "Kusursuz Ortopedik/Pediatrik Yaklaşım: Kundaklama en büyük çevresel risktir; ilk 6 ayda altın standart Kalça USG'dir ve cerrahisiz bandajla düzelir."
                },
                {
                    "text": "Direkt grafi çekilip kemik kırığı aranmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı: İlk aylarda femur başı kıkırdaktır, röntgende görünmez, USG gereklidir."
                },
                {
                    "text": "Yürüme çağına (1 yaşına) kadar hiçbir müdahale yapılmadan beklenmelidir",
                    "isCorrect": False,
                    "feedback": "Hatalı: 1 yaşına kadar beklenirse cerrahi ameliyat gerekir, erken tanı başarının anahtarıdır."
                }
            ]
        ),
        83: make_branching_logic(
            "Sağlık ocağına getirilen 1 yaşındaki bir çocuğun tartısı 9.6 kg (doğum tartısı 3200 g), boyu 75 cm (doğum boyu 50 cm) ölçülüyor.",
            "Bu çocuğun 1 yaşındaki fiziksel büyüme göstergeleri nasıl yorumlanmalıdır?",
            [
                {
                    "text": "Mükemmel ve beklenen standart büyümedir; 1 yaşında kilo doğumun 3 katı, boy ise 1.5 katı olmuştur",
                    "isCorrect": True,
                    "feedback": "Tam Büyüme Değerlendirmesi: 1 yaşında kilonun 3 katına (3200x3 = 9600 g) ve boyun 1.5 katına (50x1.5 = 75 cm) ulaşması altın standarttır."
                },
                {
                    "text": "Ağır büyüme geriliği vardır, kilo doğumun en az 5 katı olmalıydı",
                    "isCorrect": False,
                    "feedback": "Hatalı: 1 yaşında 3 kat normaldir, 5 kat obezitedir."
                },
                {
                    "text": "Boy çok uzundur, patolojik jigantizm araştırılmalıdır",
                    "isCorrect": False,
                    "feedback": "Hatalı: 75 cm 1 yaş için ortalama 50. persentil değeridir."
                }
            ]
        ),
        87: make_branching_logic(
            "Ateş ve kusma şikayetiyle getirilen 5 aylık bir bebeğin dik oturur muayenesinde ön fontanelin tahta gibi sert, dışarı doğru kabarmış (bombe) olduğu görülüyor.",
            "Bu bebekte hekimin ekarte etmesi gereken en acil ölümcül klinik patoloji hangisidir?",
            [
                {
                    "text": "Akut Bakteriyel Menenjit veya Kafa İçi Basınç Artışı Sendromu (KİBAS)",
                    "isCorrect": True,
                    "feedback": "Hayati Tanı: Ateşle birlikte bombe fontanel menenjit ve KİBAS'ın primer fizik muayene bulgusudur; ivedi lomber ponksiyon ve antibiyoterapi gerektirir."
                },
                {
                    "text": "Ağır dehidratasyon ve ishal",
                    "isCorrect": False,
                    "feedback": "Hatalı: Dehidratasyonda fontanel kabarmaz, tam tersine içe çöker (çökük fontanel)."
                },
                {
                    "text": "D vitamini eksikliği (raşitizm)",
                    "isCorrect": False,
                    "feedback": "Hatalı: Raşitizm fontaneli bombeleştirmez, kapanmasını geciktirir."
                }
            ]
        ),
        93: make_branching_logic(
            "Rutin 6. ay izlemine getirilen bir süt çocuğunun nöromotor muayenesinde destek almadan düz zeminde desteksiz oturduğu ve oyuncağını sol elinden sağ eline geçirdiği saptanıyor.",
            "Bu bebeğin 6. ay gelişimsel kazanımları nasıl yorumlanmalıdır?",
            [
                {
                    "text": "Nöromotor gelişimi yaşıyla tam uyumludur; 6. ayda desteksiz oturma ve el transferi beklenen temel basamaklardır",
                    "isCorrect": True,
                    "feedback": "Doğru Gelişimsel Değerlendirme: 6. ayın karakteristik dönüm noktaları bağımsız desteksiz oturma ve iki el arası obje aktarımıdır."
                },
                {
                    "text": "Gelişimsel gerilik vardır, 6. ayda çocuğun koşması gerekirdi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Koşma 2 yaş civarında beklenir."
                },
                {
                    "text": "Desteksiz oturma patolojiktir, derhal beyin MR çekilmelidir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Desteksiz oturma normal ve arzu edilen sağlıklı motor olgunluktur."
                }
            ]
        )
    }

def get_extra_sliders():
    """Before/after slider (tedavi öncesi/sonrası, halk sağlığı müdahaleleri, fizyolojik değişimler) ögeleri."""
    return {
        4: make_before_after(
            "Türkiye'de Sağlık Hizmetlerinin Sosyalleştirilmesi Öncesi ve Sonrası Anne Ölüm Oranı",
            "1960'lar Öncesi: Anne Ölüm Oranı yüz binde 200'lerin üzerinde, kırsal alanda ebesiz ev doğumları yaygın ve maternal ölümler önlenemez kabul ediliyordu.",
            "Günümüz (ASM Sistemi): AÖO yüz binde 12-13 seviyesine indirilmiş, hastanede doğum oranı %99'u geçmiş ve gebe izlemleri entegre edilmiştir."
        ),
        8: make_before_after(
            "Bebek Ölüm Hızında Temel Sağlık Hizmetleri Öncesi ve Sonrası Değişim",
            "1970'ler: Bebek Ölüm Hızı binde 150 düzeyinde; kızamık, ishal, tetanoz ve prematürite nedeniyle her 7 bebekten biri 1 yaşına ulaşamadan kaybediliyordu.",
            "Günümüz GBP Takvimi: BÖH binde 9 düzeyine düşürülmüş; 13 antijene karşı rutin aşılama ve DÖB ile önlenebilir bebek ölümleri dramatik azalmıştır."
        ),
        14: make_before_after(
            "Doğrudan Obstetrik Nedenlerde Acil Müdahale Öncesi ve Sonrası Seyir",
            "Müdahale Öncesi: Atoni kanamasında uterus gevşek, spiral arterler açık ve hasta dakikalar içinde hipovolemik şok ve koagülopatiye sürüklenir.",
            "Müdahale Sonrası (Bimanuel Masaj + Oksitosin): Miyometriyum tahta gibi sert kasılır, spiral damarlar mekanik sıkışır ve kanama tamamen durur."
        ),
        18: make_before_after(
            "Türkiye'de Sezaryen Oranlarının Yıllara Göre Seyri ve Halk Sağlığı Hedefi",
            "1990'lar Başlangıcı: Sezaryen oranı %10-15 düzeyinde olup DSÖ'nün tıbbi gereklilik sınırları ile tam uyumlu seyrediyordu.",
            "Günümüz Durumu: Sezaryen oranı %50'nin üzerine çıkarak halk sağlığı sorunu haline gelmiş; normal doğum eylem planları öncelik kazanmıştır."
        ),
        24: make_before_after(
            "Kessner İndeksinde Yetersiz Bakım ile Yeterli Bakım Alan Gebelerin Prognozu",
            "Yetersiz Bakım (Inadequate): Gebelik izlemi 3. trimesterde başlamış veya hiç yapılmamış; preeklampsi, anemi ve düşük doğum ağırlığı riski 4 kat yüksektir.",
            "Yeterli Bakım (Adequate): İzlem ilk 14 haftada başlamış ve en az 4 vizit yapılmış; maternal ve perinatal komplikasyonlar erkenden önlenmiştir."
        ),
        28: make_before_after(
            "Doğum Aralığının 2 Yıldan Kısa Olması ile 2 Yıldan Uzun Olması Arasındaki Fark",
            "Doğum Aralığı < 2 Yıl: Annenin demir, kalsiyum ve folat depoları tükenmiş; erken doğum, düşük doğum ağırlığı ve maternal anemi riski katlanır.",
            "Doğum Aralığı > 2 Yıl: Maternal besin depoları tamamen yenilenmiş, uterus involüsyonu tamamlanmış; bebek ve anne sağlığı güvenceye alınmıştır."
        ),
        34: make_before_after(
            "Gebelikte Folik Asit Desteğinin Başlama Zamanı ve Nöral Tüp Defekti (NTD) Riski",
            "Konsepsiyon Sonrası Geç Başlama: Nöral tüp gebeliğin 28. gününde kapandığından geç başlanan folik asit spina bifida ve anensefaliyi önleyemez.",
            "Prekonsepsiyonel Başlama (Gebelikte 1 Ay Önce): Maternal folat seviyesi optimal düzeye ulaşır; spina bifida ve anensefali riski %70 oranında engellenir."
        ),
        38: make_before_after(
            "Gebelikte Rutin Demir Profilaksisi Öncesi ve Sonrası Hematolojik Tablo",
            "Demir Desteği Verilmediğinde: Plazma hacim artışına (hemodilüsyon) bağlı olarak Hb <10 g/dl'ye düşer, doku hipoksisi ve postpartum atoni riski artar.",
            "Profilaktik Demir (40-60 mg) Alındığında: Maternal hemoglobin deposu ve ferritin korunur; fetal demir transferi ve doğum toleransı ideal seviyede kalır."
        ),
        44: make_before_after(
            "20. Haftada Uterus Fundus Yüksekliğinin Göbek Çizgisiyle İlişkisi",
            "20. Hafta Öncesi: Uterus simfizis pubis ile göbek arasında büyür; karından palpasyonla pelvik kemik üzerinde hissedilir.",
            "20. Hafta ve Sonrası: Uterus fundusu tam göbek seviyesine ulaşır (20 cm); gestasyonel haftayla santimetre ölçümü birebir örtüşür."
        ),
        48: make_before_after(
            "Gebelikte Tetanoz Aşısı Yapılmadığı ve Yapıldığı Durumlarda Neonatal Seyir",
            "Aşısız Gebelik: Doğumda steril olmayan alet temasında Clostridium tetani toksini bebekte göbekten girerek ölümcül neonatal tetanoz (trismus, opistotonus) yapar.",
            "İki Doz Td Aşılı Gebelik: Annede oluşan IgG antikorları plasentadan bebeğe geçerek ilk aylarda neonatal tetanoza karşı %100 koruyucu bağışıklık sağlar."
        ),
        54: make_before_after(
            "Preeklampsi Kliniğinde Erken Teşhis Öncesi ve Sonrası Dönem",
            "Tedavisiz/Geç Tanı: Hipertansiyon ve endotel hasarı eklampsi nöbetlerine, beyin kanamasına, HELLP sendromuna ve ablasyo plasentaya ilerler.",
            "Erken Tespit ve Magnezyum Sülfat: Nöbet eşiği yükseltilir, vazospazm çözülür, kan basıncı kontrol altına alınarak anne ve bebek güvenle doğurtulur."
        ),
        58: make_before_after(
            "Plasenta Previa Kanamasında Dijital Muayene Yapıldığında ve Yapılmadığında",
            "Dijital Muayene Yapılırsa (Hatalı Müdahale): Muayene eden parmak plasenta dokusunu yırtarak saniyeler içinde masif fetal ve maternal kanamaya yol açar.",
            "Ultrasonografi ile Yaklaşım (Doğru Protokol): Serviks iç ağzını kapatan plasenta invaziv olmayan USG ile net görüntülenir ve cerrahi hazırlık yapılır."
        ),
        64: make_before_after(
            "Lohusalıkta Mesanenin Dolu Olması ile Boşaltılması Arasındaki Myometrium Yanıtı",
            "Mesane Dolu (Glob Vezikale): Şişen mesane uterusu yukarı ve sağa iter, fundusun kasılmasını mekanik olarak bloke eder ve atoni kanaması tetiklenir.",
            "Mesane Kateterle Boşaltıldığında: Uterus pelvik tabana iner, kas lifleri spiral arterler üzerine güçlüce kasılır ve kanama kontrol altına alınır."
        ),
        68: make_before_after(
            "Serviks Kanseri Taraması (HPV-DNA/Smear) Yapılmayan ve Yapılan Kadınlarda Seyir",
            "Taramasız Dönem: HPV enfeksiyonu sessizce CIN ve invaziv serviks karsinomuna ilerler; hasta ancak ileri evrede kanama ve ağrıyla başvurur.",
            "5 Yılda Bir Tarama Yapıldığında: Lezyonlar preinvaziv evrede (CIN 1-3) yakalanarak basit lokal işlemlerle kansere dönüşmeden %100 tedavi edilir."
        ),
        74: make_before_after(
            "Yenidoğanda Kundak Yapılan ve Yapılmayan Kalçalarda Gelişim",
            "Kundaklama Yapıldığında (Hatalı Uygulama): Alt ekstremiteler zorla ekstansiyon ve addüksiyona getirilir; femur başı asetabulumdan dışarı kayarak kalıcı GKD oluşur.",
            "Serbest Doğal Pozisyon (Kurbağa Pozisyonu): Kalçalar fleksiyon ve abdüksiyonda serbest bırakılır; femur başı asetabulum çukurunu derinleştirerek sağlıklı gelişir."
        ),
        78: make_before_after(
            "Fenilketonüri Taraması Yapılmayan ve Yapılan Çocuklarda Nörolojik Seyir",
            "Taranmadığında (Doğal Seyir): Kanda biriken fenilalanin miyelin kılıfı yıkar; çocukta ağır ve geri dönüşsüz zeka geriliği (IQ <30) ve konvülsiyonlar gelişir.",
            "Topuk Kanıyla Erken Tanı ve Diyet: Doğumdan itibaren fenilalaninden kısıtlı diyet uygulanır; çocuk tamamen normal zeka ve bilişsel kapasiteyle büyür."
        ),
        84: make_before_after(
            "Doğumda ve 12. Ayda Baş-Göğüs Çevresi Orantısı",
            "Doğum Anı: Baş çevresi (34-36 cm) göğüs çevresinden 1.5-2 cm daha büyüktür; beyin dokusu baskın hacimdedir.",
            "12. Ay (1 Yaş): Göğüs kafesi akciğer solunumuyla hızla genişler ve baş çevresi ile göğüs çevresi birbirine tam EŞİTLENİR (~46-47 cm)."
        ),
        88: make_before_after(
            "Ön Fontanelin Normal Zamanda Kapanması ile Raşitizmde Açık Kalması",
            "Normal Fizyolojik Süreç: D vitamini ve kalsiyum dengesiyle kemikleşme tamamlanır ve ön fontanel 9-18. aylar arasında tamamen kapanır.",
            "Raşitizm (D Vitamini Eksikliği): Kemik mineralizasyonu bozulur, kraniyotabes oluşur ve ön fontanel 18 aydan sonra hala geniş açık kalır."
        ),
        94: make_before_after(
            "Süt Çocuğunda 4. Ay ile 6. Ay Arasındaki Motor Postür Dönüşümü",
            "4. Ay Postürü: Bebek ancak arkasına yastık desteği konulduğunda destekle oturabilir, desteği çekilince devrilir.",
            "6. Ay Dönüm Noktası: Gövde ve omurga kasları dikleşir, postural refleksler olgunlaşır ve bebek hiçbir yardıma ihtiyaç duymadan desteksiz oturur."
        )
    }

def get_extra_chains():
    """Causal chain (patofizyolojik mekanizma zinciri, halk sağlığı akışları) ögeleri."""
    return {
        6: make_causal_chain(
            "Bebek Mortalitesi Azaltma Mekanizması Zinciri",
            [
                "1. Nitelikli DÖB: Gebelik komplikasyonlarının ve enfeksiyonların erken taranması",
                "2. Kurumsal Güvenli Doğum: Doğumun hastanede eğitimli sağlık personeli ile gerçekleştirilmesi",
                "3. Neonatal Resüsitasyon: Doğum salonunda asfiksinin önlenmesi ve ilk 1 saatte emzirmenin başlatılması",
                "4. GBP Aşıları: 1. aydan itibaren Hepatit B, BCG ve karma aşılarla ölümcül enfeksiyon kalkanı kurulması"
            ]
        ),
        12: make_causal_chain(
            "Doğrudan Anne Ölümü Patofizyolojik Akış Zinciri",
            [
                "1. Etyolojik Trik: Uterus atonisi veya ablasyo plasenta nedeniyle kontrolsüz damar açılması",
                "2. Hızlı Kan Kaybı: Doğum sonrasında dakikalar içinde 1000 ml üzeri kontrolsüz kan kaybı gelişmesi",
                "3. Hemodinamik Çöküş: Hipovolemik şok, doku hipoksisi ve tüketim koagülopatisinin (DİK) tetiklenmesi",
                "4. İvedi Müdahale: Bimanuel masaj, oksitosin ve acil cerrahi ligasyon ile hayatın kurtarılması"
            ]
        ),
        16: make_causal_chain(
            "Anne Ölümü Sürveyans ve Kök Neden Analiz Zinciri",
            [
                "1. Ölüm Vakası: Sağlık kuruluşunda veya evde bir anne ölümünün gerçekleşmesi",
                "2. 24 Saat Bildirimi: Durumun aile hekimi veya hastane tarafından derhal İl Sağlık Müdürlüğü'ne bildirilmesi",
                "3. İnceleme Komisyonu: Anne Ölümleri Komisyonu tarafından tıbbi kayıtların ve gecikme modellerinin incelenmesi",
                "4. Sistem İyileştirmesi: Önlenebilir hatanın tespit edilip ulusal klinik rehberlerin güncellenmesi"
            ]
        ),
        22: make_causal_chain(
            "Kessner İndeksi Yetersiz Bakım Patoloji Zinciri",
            [
                "1. Bakımda Gecikme: Gebeliğin ilk 6 ayında hiçbir hekim veya ebe kontrolüne gidilmemesi",
                "2. Taranmayan Riskler: Asemptomatik bakteriürinin, aneminin ve gestasyonel hipertansiyonun atlanması",
                "3. Komplikasyon Gelişimi: Tedavisiz kalan patolojilerin akut pyelonefrit veya preeklampsi krizine dönüşmesi",
                "4. Kötü Perinatal Sonuç: Erken doğum, intrauterin gelişme geriliği ve perinatal ölümle tablonun sonlanması"
            ]
        ),
        26: make_causal_chain(
            "Gebelikte 4 Çok Kuralı ve Maternal Tükenmişlik Zinciri",
            [
                "1. Sık ve Çok Doğum: Kadının 2 yıldan kısa aralıklarla 4'ten fazla doğum yapması",
                "2. Biyolojik Depo Kaybı: Maternal demir, folik asit, kalsiyum ve protein rezervlerinin tükenmesi",
                "3. Uterus Yorgunluğu: Çoklu gerilmelere bağlı myometrium liflerinin elastikiyetini kaybetmesi",
                "4. Doğum Sonu Felaketi: Doğum eylemi sonrasında myometriyumun kasılamaması ve masif atoni kanaması"
            ]
        ),
        32: make_causal_chain(
            "Gebelikte Folik Asit Eksikliği ve Nöral Tüp Defekti Zinciri",
            [
                "1. Diyet Yetersizliği: Prekonsepsiyonel dönemde yeşil yapraklı sebze ve folat alımının yetersiz olması",
                "2. DNA Metilasyon Bozukluğu: Embriyonik hücre bölünmesinde timidin sentezi ve DNA kapanmasının aksaması",
                "3. Kapanma Başarısızlığı: Fetal nöral plağın gebeliğin 28. gününde nöral tüpü tam kapatamaması",
                "4. Konjenital Malformasyon: Spina bifida veya anensefali gibi ağır doğumsal anomalilerin ortaya çıkması"
            ]
        ),
        36: make_causal_chain(
            "Gebelikte Fizyolojik Hemodilüsyon ve Anemi Mekanizma Zinciri",
            [
                "1. Plazma Artışı: Gebelikte plazma hacminin yaklaşık %45-50 oranında belirgin artması",
                "2. Eritrosit Uyumsuzluğu: Kırmızı kan hücresi kitlesinin ise yalnızca %20-30 oranında artabilmesi",
                "3. Konsantrasyon Düşüşü: Kanda göreceli seyreltilme (fizyolojik hemodilüsyon) sonucu Hb seviyesinin gerilemesi",
                "4. Demir Tüketimi: Fetal gereksinim nedeniyle demir depoları tükenerek aşikar anemi tablosunun oturması"
            ]
        ),
        42: make_causal_chain(
            "Leopold Manevraları ile Fetal Pozisyon Belirleme Zinciri",
            [
                "1. 1. Leopold: Uterus fundusu iki elle palpe edilerek baş veya makat kutbunun ayırt edilmesi",
                "2. 2. Leopold: Yan duvarlar taranarak fetal sırtın sağda mı solda mı olduğunun saptanması",
                "3. 3. Leopold: Simfizis pubis üzerinde tek elle önde gelen kısmın hareketliliğinin test edilmesi",
                "4. 4. Leopold: Pelvise doğru dönülerek fetal başın angajman ve iniş derinliğinin kesinleştirilmesi"
            ]
        ),
        46: make_causal_chain(
            "Gebelikte Preeklampsi Patogenez Zinciri",
            [
                "1. Bozuk Trofoblast İnvazyonu: Spiral arterlerin geniş kas damarlarına dönüşememesi",
                "2. Plasental Hipoksi: Uteroplasental perfüzyonun bozulması ve dolaşıma anti-anjiyogenik faktör salınması",
                "3. Sistemik Endotel Hasarı: Maternal damarlarda yaygın vazospazm, kapiller kaçak ve trombosit tüketimi",
                "4. Klinik Sendrom: Kan basıncının >140/90 mmHg olması, böbrek hasarıyla proteinüri ve yaygın ödem tablosu"
            ]
        ),
        52: make_causal_chain(
            "Ağır Preeklampsiden Eklampsi Krizine İlerleme Zinciri",
            [
                "1. Şiddetli Vazospazm: Beyin arterlerinde aşırı vazokonstriksiyon ve serebral perfüzyon bozukluğu",
                "2. Serebral Ödem: Kan-beyin bariyeri hasarıyla temporal/oksipital loblarda mikrovasküler ödem oluşması",
                "3. Prodrom Belirtileri: Gebe kadında zonklayıcı baş ağrısı, görme bulanıklığı ve epigastrik ağrı başlaması",
                "4. Jeneralize Konvülsiyon: Beyin korteksinde deşarj ile tonik-klonik eklampsi nöbeti ve koma tablosu"
            ]
        ),
        56: make_causal_chain(
            "Postpartum Atoni Kanaması Oluşum Zinciri",
            [
                "1. Aşırı Gerilme: Çoğul gebelik, polihidramnios veya iri bebek nedeniyle myometriyumun aşırı gerilmesi",
                "2. Kas Yorgunluğu: Uzamış travay veya hızlı doğum sonrası myometriyum kas liflerinin kasılamaması",
                "3. Açık Spiral Arterler: Plasenta yatağındaki yüzlerce geniş damarın mekanik olarak kapatılamaması",
                "4. Masif Hemoraji: İlk 24 saatte dakikalar içinde 1000 ml üzeri kan kaybıyla atoni şokunun gelişmesi"
            ]
        ),
        62: make_causal_chain(
            "Lohusalıkta Uterin İnvolüsyon Mekanizma Zinciri",
            [
                "1. Doğum Sonu: Doğumun hemen ardından uterus yaklaşık 1000 gram ağırlığında ve göbek hizasındadır",
                "2. Oksitosin Uyarısı: Emzirmeyle salınan oksitosin sayesinde myometriyum lifleri ritmik ve güçlü kasılır",
                "3. Protolitik Yıkım: Fazla sitoplazmik proteinler ve hücreler otoliz yoluyla parçalanıp uzaklaştırılır",
                "4. 6. Hafta Sonu: 42 günün sonunda uterus normal gebe olmayan 60 gramlık pelvik boyutuna döner"
            ]
        ),
        66: make_causal_chain(
            "Puerperal Sepsis Gelişim Zinciri",
            [
                "1. İntrauterin Kontaminasyon: Doğum sırasında vajinal floranın veya nozokomiyal bakterilerin açık kaviteye girmesi",
                "2. Endometrit: Plasenta implantasyon alanında nekrotik dokular üzerinde polimikrobiyal enfeksiyon üremesi",
                "3. Sistemik Yayılım: Bakterilerin pelvik venler ve lenfatikler yoluyla genel kan dolaşımına karışması",
                "4. Septik Şok: Yüksek ateş, lökositoz, kötü kokulu loşi, hipotansiyon ve ölümcül maternal sepsis"
            ]
        ),
        72: make_causal_chain(
            "Gelişimsel Kalça Displazisi Tanı ve Tedavi Zinciri",
            [
                "1. Risk ve Muayene: Pozitif aile öyküsü veya makat doğum olan bebekte Ortolani testiyle klik aranması",
                "2. 4-6. Hafta USG: Kıkırdak femur başı kemikleşmeden dinamik ultrason ile alfa açısının ölçülmesi",
                "3. Displazi Tespiti: Asetabuler çatının sığ olduğunun ve femur başı instabilitesinin doğrulanması",
                "4. Erken Dinamik Bandaj: Pavlik bandajı takılarak femur başının asetabulumu doğal oymasının sağlanması"
            ]
        ),
        76: make_causal_chain(
            "Yenidoğan Fenilketonüri Taraması ve Koruma Zinciri",
            [
                "1. Enteral Beslenme: Bebeğin doğumdan sonra en az 48 saat anne sütü alarak proteine maruz kalması",
                "2. Topuk Kanı Alımı: Guthrie kartına özel filtre kağıdına topuktan kılcal kan damlatılıp laboratuvara yollanması",
                "3. Fenilalanin Yüksekliği: Fenilalanin hidroksilaz eksikliğine bağlı kanda metabolit yüksekliğinin saptanması",
                "4. Diyetle Kurtarma: İlk haftalarda fenilalaninsiz özel formülle nöronal miyelin hasarının tamamen önlenmesi"
            ]
        ),
        82: make_causal_chain(
            "Süt Çocuğunda Fizyolojik Kilo Katlanma Zinciri",
            [
                "1. Doğum Tartısı: Sağlıklı miadında bir bebeğin ortalama 3200 gram ile dünyaya gelmesi",
                "2. 5. Ay Dönüm Noktası: Düzenli anne sütü beslenmesiyle doğum ağırlığının 2 katına (~6.5 kg) ulaşılması",
                "3. 1. Yaş Zirvesi: Ek gıdalarla birlikte 12. ayda doğum ağırlığının tam 3 katına (~9.6 kg) çıkılması",
                "4. 2. Yaş Takibi: İkinci yaşın sonunda doğum ağırlığının 4 katına (~12.8 kg) erişilerek bebekliğin tamamlanması"
            ]
        ),
        86: make_causal_chain(
            "Ön Fontanel Kapanma ve Kraniyosinostoz Patoloji Zinciri",
            [
                "1. Açık Sütürler: Doğumda ön fontanelin (baklava) ve kafa sütürlerinin membranöz açık olması",
                "2. Beyin Büyümesi: İlk 1 yılda beyin hacminin hızla artması için fontanelin esnek genişleme sağlaması",
                "3. Erken Kemikleşme: Sütürlerin vaktinden önce kaynamasıyla kraniyosinostoz ve mikrosefalinin gelişmesi",
                "4. Normal Kapanma: Beyin büyüme atağı yavaşlayınca 9-18. aylar arasında ön fontanelin fizyolojik kapanması"
            ]
        ),
        92: make_causal_chain(
            "Süt Çocuğunda Nöromotor Olgunlaşma (Sefalokaudal) Zinciri",
            [
                "1. 2. Ay (Baş Kontrolü): Miyelinizasyonun boyun kaslarına ulaşmasıyla başın dik tutulabilmesi",
                "2. 4. Ay (Gövde Kontrolü): Sırt kaslarının güçlenmesiyle destekle oturabilme ve kahkaha atma",
                "3. 6. Ay (Pelvik Denge): Lumbosakral olgunlaşmayla desteksiz bağımsız oturma ve el transferi",
                "4. 12. Ay (Alt Ekstremite): Bacak sinirlerinin miyelinlenmesiyle sıralama ve bağımsız yürüme adımları"
            ]
        )
    }

def enrich_k1_23_elements(slides):
    """Slides listesine ekstra interaktif ögeleri enjekte eder."""
    extra_branching = get_extra_branching()
    extra_sliders = get_extra_sliders()
    extra_chains = get_extra_chains()

    for s in slides:
        num = s["slideNumber"]
        elems = s.setdefault("interactiveElements", [])

        if num in extra_branching:
            elems.append(extra_branching[num])
        if num in extra_sliders:
            elems.append(extra_sliders[num])
        if num in extra_chains:
            elems.append(extra_chains[num])

    return slides
