# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 2: Benign ve Malign Neoplazmların Morfolojisi (Slayt 11 - 20)
Checkpoint: Slayt 19
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_2_slides():
    return [
        # Slayt 11
        {
            "slideNumber": 11,
            "title": "Benign ve Malign Neoplazmların Ayrım Kriterleri",
            "content": (
                "Neoplazmların benign (iyi huylu) veya malign (kötü huylu) olarak iki temel sınıfa ayrılması, onkolojik "
                "tedavi stratejisini ve hastanın sağkalım beklentisini belirleyen en kritik patolojik değerlendirmedir. "
                "Bir tümörün benign ya da malign olduğunu belirlemede patolog dört ana morfolojik ve biyolojik kriteri "
                "kombine olarak inceler: Parankimal hücrelerin diferansiyasyon derecesi ve anaplazi varlığı, kitlenin "
                "büyüme hızı, lokal invazyon ve çevre dokulara sızma özelliği ile uzak dokulara metastaz yapma yeteneği. "
                "Benign tümörler genellikle lokalize kalırken, malign tümörler invaziv büyüme ve metastazla karakterizedir."
            ),
            "elements": [
                make_table(
                    "Benign ve Malign Neoplazmların Temel Ayırıcı Özellikleri",
                    ["Özellik", "Benign Neoplazm", "Malign Neoplazm"],
                    [
                        {
                            "cells": ["Diferansiyasyon", "İyi diferansiye (Normale benzer)", "Değişken (İyi, orta, az diferansiye veya anaplastik)"],
                            "hiddenIndex": 1,
                            "hint": "Fizyolojik dokuya yakın hücresel olgunluk"
                        },
                        {
                            "cells": ["Kapsül ve Sınır", "Genellikle fibröz kapsüllü, keskin sınırlı", "Kapsülsüz, çevreye sızan düzensiz sınırlar"],
                            "hiddenIndex": 1,
                            "hint": "Bağ dokusu zarı ile çevrelenme"
                        },
                        {
                            "cells": ["Lokal İnvazyon", "Kesinlikle yok (İtici büyüme)", "Daima var (İnfiltratif yıkıcı büyüme)"],
                            "hiddenIndex": 2,
                            "hint": "Çevre doku içine girme yeteneği"
                        },
                        {
                            "cells": ["Metastaz", "Asla görülmez", "Sıktır (Malignitenin kesin kanıtı)"],
                            "hiddenIndex": 2,
                            "hint": "Uzak organlara yayılım"
                        }
                    ]
                ),
                make_cloze(
                    "Malignitenin patolojik incelemede tartışılamaz kesin kanıtı uzak dokularda metastaz varlığıdır.",
                    "metastaz",
                    "Uzak organa neoplastik yayılım"
                )
            ]
        },
        # Slayt 12
        {
            "slideNumber": 12,
            "title": "Diferansiyasyon Derecesi: Normale Benzerlik Spektrumu",
            "content": (
                "Diferansiyasyon, bir neoplazmın parankimal hücrelerinin, köken aldığı normal olgun hücrelere morfolojik "
                "ve fonksiyonel açıdan ne derecede benzediğini ifade eder. Benign neoplazmlar kural olarak 'iyi diferansiye' "
                "hücrelerden oluşur; örneğin bir lipomdaki yağ hücreleri normal adipositlerden, bir leiomyomdaki düz kas "
                "hücreleri ise normal myometrium hücrelerinden neredeyse farksızdır. Malign neoplazmlar ise iyi diferansiyeden "
                "tamamen diferansiyasyonsuz (anaplastik) hale kadar uzanan geniş bir yelpaze sergiler. Diferansiyasyon derecesi "
                "azaldıkça tümörün agresifliği, büyüme hızı ve metastaz potansiyeli geometrik olarak artış gösterir."
            ),
            "elements": [
                make_before_after(
                    "Diferansiyasyon Spektrumu ve Biyolojik Davranış",
                    "İyi Diferansiye Malign Kitle",
                    "Bez yapıları ve keratin üretimi korunmuştur, mitoz azdır, biyolojik seyir nispeten daha yavaştır.",
                    "Az Diferansiye / Anaplastik Kitle",
                    "Köken dokuya hiçbir benzerlik kalmamıştır; aşırı pleomorfizm, atipik mitozlar ve agresif erken metastaz izlenir.",
                    "Patolojik evreleme ve derecelendirmede (grading) diferansiyasyon skoru birincil parametredir."
                ),
                make_active_recall(
                    "Bir tümörün köken aldığı normal doku hücrelerine yapısal ve fonksiyonel benzerlik derecesine ne ad verilir?",
                    "Diferansiyasyon derecesi adı verilir.",
                    "Farklılaşma ve olgunlaşma düzeyi"
                )
            ]
        },
        # Slayt 13
        {
            "slideNumber": 13,
            "title": "Büyüme Hızı ve Apoptoz-Proliferasyon Dengesi",
            "content": (
                "Genel bir biyolojik kural olarak benign tümörler yavaş, malign tümörler ise hızlı büyüme gösterirler; "
                "ancak bu mutlak bir kural değildir. Bir tümörün net büyüme hızı sadece hücre bölünme hızına değil, aynı "
                "zamanda 'proliferasyon fraksiyonu' (bölünme havuzundaki hücre oranı) ile 'hücre kaybı' (apoptoz ve nekroz) "
                "arasındaki dinamik dengeye bağlıdır. Hızlı büyüyen malign tümörlerde hücre kaybı oranı %70-80'e kadar çıkabilir. "
                "Bazı benign tümörler hormon uyarısıyla son derece hızlı büyüyebilir; örneğin uterin leiomyomlar gebelikteki "
                "yüksek östrojen etkisiyle haftalar içinde hızla dev boyutlara ulaşıp ağrılı kırmızı nekroza (karneöz dejenerasyon) uğrayabilir."
            ),
            "elements": [
                make_micro_quiz(
                    "Aşağıdakilerden hangisi benign bir neoplazmın gebelikte hızla büyüyüp nekroza uğramasına klasik örnektir?",
                    [
                        {
                            "text": "Uterus leiomyomunun östrojen etkisiyle büyümesi ve kırmızı dejenerasyonu",
                            "isCorrect": True,
                            "explanation": "Doğrudur; leiomyomlar hormonal uyarıya duyarlıdır ve gebelikte hızla büyüyebilir."
                        },
                        {
                            "text": "Ciltteki bazal hücreli karsinomun metastaz yapması",
                            "isCorrect": False,
                            "explanation": "BCC malign bir tümördür ve neredeyse hiç metastaz yapmaz."
                        },
                        {
                            "text": "Kemik osteosarkomunun kendiliğinden erimesi",
                            "isCorrect": False,
                            "explanation": "Osteosarkom oldukça malign ve agresif bir kemik tümörüdür."
                        },
                        {
                            "text": "Akciğer küçük hücreli karsinomunun iyi huylu kalması",
                            "isCorrect": False,
                            "explanation": "Küçük hücreli karsinom en ölümcül malign neoplazmlardandır."
                        }
                    ],
                    "Büyüme hızı tek başına benign-malign ayrımını mutlak olarak belirlemez."
                ),
                make_cloze(
                    "Bir tümörün büyüme hızını belirleyen en kritik kinetik parametre bölünme havuzundaki proliferasyon fraksiyonu oranıdır.",
                    "proliferasyon fraksiyonu",
                    "Aktif bölünen hücrelerin yüzdesi"
                )
            ]
        },
        # Slayt 14
        {
            "slideNumber": 14,
            "title": "Tümör Sınırları ve Kapsül: İtici Büyüme",
            "content": (
                "Benign neoplazmların büyük çoğunluğu yavaş ve ekspansil (itici) biçimde büyürler. Tümör genişledikçe "
                "etrafındaki normal konakçı dokuyu sıkıştırır; sıkışan stromal parankimin atrofisi ve reaktif fibroblastik "
                "kollajen sentezi sonucu tümörün çevresinde belirgin bir 'fibröz kapsül' meydana gelir. Bu fibröz kapsül, "
                "tümörü çevre normal dokulardan keskin, düzlemsel bir sınırla ayırır. Örneğin memenin benign bir tümörü olan "
                "fibroadenom, son derece düzgün sınırlı, hareketli ve belirgin kapsüllüdür; bu sayede cerrah tarafından "
                "normal meme dokusuna zarar vermeksizin tek bir hamlede 'enükleasyon' (kabuğundan soyma) yöntemiyle kolayca çıkarılabilir."
            ),
            "elements": [
                make_before_after(
                    "Benign vs Malign Tümörün Makroskobik Sınırları",
                    "Benign Kitle (Meme Fibroadenomu)",
                    "Keskin sınırlı, fibröz kapsüllü, çevre dokudan kolayca ayrılır, cerrahi enükleasyon düzlemi mevcuttur.",
                    "Malign Kitle (Meme İnvaziv Karsinomu)",
                    "Kapsülsüz, yıldızsı (spiküle) çıkıntılarla normal yağ ve duktus dokusuna saplanan, tahta sertliğinde kitle.",
                    "Kapsül varlığı benign kitlelerin cerrahi olarak tam çıkarılmasını son derece kolaylaştırır."
                ),
                make_active_recall(
                    "Benign tümörlerin çevre dokuları iterek sıkıştırması sonucu etrafında oluşan koruyucu bağ dokusu kılıfına ne denir?",
                    "Fibröz kapsül adı verilir.",
                    "Sıkışmış konak doku zarı"
                )
            ]
        },
        # Slayt 15
        {
            "slideNumber": 15,
            "title": "Kapsül İhlali ve Mikroskobik Tümör Dilcikleri",
            "content": (
                "Malign neoplazmlar kural olarak gerçek bir kapsülden yoksundur; çevre doku sınırları düzensiz, girintili "
                "çıkıntılı ve siliktir. Nadiren bazı malign kitleler (örneğin renal hücreli karsinom veya folliküler tiroid "
                "karsinomu) etraflarında sıkışmış dokudan oluşan bir 'yalancı kapsül' (pseudokapsül) sergileyebilir. Ancak "
                "patolojik incelemede bu psödokapsülün bütünlüğü daima kusurludur. Kanser hücreleri mikroskobik 'tümör dilcikleri' "
                "(tumor tongues) veya kordonlar halinde kapsülü delip geçer (transkapsüler invazyon) ve çevre yağ dokusuna "
                "ve lenfovasküler kanallara sızar. Bu nedenle malign tümörlerde cerrahi enükleasyon kesinlikle yetersizdir; "
                "mutlaka geniş bir 'negatif cerrahi sınır' marjini ile rezeksiyon yapılmalıdır."
            ),
            "elements": [
                make_causal_chain(
                    "Malign Hücrelerin Kapsül İhlali ve Çevreye İnfiltrasyonu",
                    [
                        "1. Psödokapsül Teması: Malign hücrelerin sıkışmış konak fibröz sınırına dayanması",
                        "2. Matriks Yıkımı: Tümör hücrelerinden salgılanan matriks metalloproteinazların (MMP) kolajeni eritmesi",
                        "3. Transkapsüler Geçiş: Hücre kordonlarının mikroskobik dilcikler halinde kapsülü delmesi",
                        "4. İnfiltratif Yayılım: Kapsül ötesindeki konak yağ ve bağ dokusu aralıklarına sızarak cerrahi sınırı aşması"
                    ]
                ),
                make_cloze(
                    "Malign kitlelerin çevre dokulara sızarken oluşturduğu mikroskobik uzantılara tümör dilcikleri adı verilir.",
                    "tümör dilcikleri",
                    "Kapsülü delen kanser kordonları"
                )
            ]
        },
        # Slayt 16
        {
            "slideNumber": 16,
            "title": "Lokal İnvazyon: Malignitenin En Güvenilir Yerel Ölçütü",
            "content": (
                "Metastazdan sonra maligniteyi benign durumdan ayıran en güvenilir ve en temel histopatolojik özellik 'lokal "
                "invazyon'dur. Benign tümörler çevre dokuları iter ancak asla komşu organ parankiminin veya bazal membranın "
                "içine doğru yıkıcı bir infiltrasyon göstermezler. Malign tümörler ise çevre dokuları proinflamatuar enzimlerle "
                "eriterek, bağ dokusu düzlemlerini parçalayarak ilerler. Bu infiltratif büyüme paterni nedeniyle cerrah makroskopik "
                "olarak tümörün tam olarak nerede bittiğini çıplak gözle ayırt edemez. Örneğin bir bazal hücreli karsinom "
                "uzak metastaz yapmasa dahi lokal olarak yüz kemiklerini, kıkırdakları ve derin fasyaları kemirerek harabiyet yaratır."
            ),
            "elements": [
                make_micro_quiz(
                    "Bir tümörün mikroskobik incelemesinde çevre kas lifleri arasına kontrolsüz sızması ve dokuyu yıkması (lokal invazyon) neyin kesin kanıtıdır?",
                    [
                        {
                            "text": "Tümörün malign karakterde olduğunun güvenilir kanıtıdır",
                            "isCorrect": True,
                            "explanation": "Doğrudur; lokal invazyon benign tümörlerde asla görülmez, malignitenin temel ölçütüdür."
                        },
                        {
                            "text": "Tümörün tamamen enfeksiyöz bir apse olduğunun kanıtıdır",
                            "isCorrect": False,
                            "explanation": "İnvazyon neoplastik bir malignite özelliğidir."
                        },
                        {
                            "text": "Tümörün kesinlikle doğumsal bir hamartom olduğunun kanıtıdır",
                            "isCorrect": False,
                            "explanation": "Hamartomlar benign lezyonlardır ve lokal invazyon yapmazlar."
                        },
                        {
                            "text": "Hastada hiçbir cerrahi müdahaleye gerek kalmadığının kanıtıdır",
                            "isCorrect": False,
                            "explanation": "Lokal invazyon acil ve geniş cerrahi rezeksiyon gerektirir."
                        }
                    ],
                    "Lokal invazyon malignitenin en güvenilir histopatolojik ayırt edici kriteridir."
                ),
                make_active_recall(
                    "Uzak organ metastazı yapmadığı halde son derece agresif lokal invazyonla kemik ve kıkırdağı harap eden deri kanseri hangisidir?",
                    "Bazal hücreli karsinomdur (BCC).",
                    "Lokal destrüktif deri kanseri"
                )
            ]
        },
        # Slayt 17
        {
            "slideNumber": 17,
            "title": "Benign Tümörlerin İstisnaları: Hemanjiyom ve Kritik Konum",
            "content": (
                "Benign tümörlerin 'daima kapsüllü ve zararsız' olduğu yönündeki genel kuralın önemli patolojik ve klinik "
                "istisnaları vardır. Patolojik istisna: Kan damarlarından köken alan benign vasküler tümörler (hemanjiyomlar), "
                "özellikle karaciğerde ve deride, fibröz bir kapsüle sahip değildir ve çevre doku aralıklarına sınırsızca "
                "sızarak yayılabilirler. Klinik istisna: 'Benign' bir tümör histolojik olarak tamamen iyi huylu olsa bile, "
                "bulunduğu kritik anatomik lokalizasyon nedeniyle ölümcül olabilir. Örneğin kafa içinde foramen magnum veya "
                "üçüncü ventrikülde yerleşen küçük bir ependimom/meningiom beyin sapına bası yaparak herniasyon ve ani ölüme, "
                "veya ana safra kanalındaki küçük bir adenom safra stazı ve biliyer sepsise yol açabilir."
            ),
            "elements": [
                make_table(
                    "Benign Tümörlerde Morfolojik ve Klinik İstisnalar",
                    ["Tümör / Durum", "İstisnai Özellik", "Klinik / Morfolojik Sonuç"],
                    [
                        {
                            "cells": ["Hemanjiyom (Karaciğer/Deri)", "Kapsülsüz ve sınırsız yayılım", "Benign olmasına rağmen kapsülsüzdür"],
                            "hiddenIndex": 1,
                            "hint": "Zarsız damarsal büyüme"
                        },
                        {
                            "cells": ["Kafatası İçi Meningiom", "Kritik anatomik yerleşim", "Histolojik benign olmasına rağmen basıyla öldürücü"],
                            "hiddenIndex": 2,
                            "hint": "Beyin sapı basısı ve herniasyon"
                        },
                        {
                            "cells": ["Beta Hücreli İnsülinoma", "Hormonal hipersekresyon", "1 cm kitleyle ölümcül hipoglisemik koma"],
                            "hiddenIndex": 2,
                            "hint": "Langerhans adacığı metabolik baygınlığı"
                        }
                    ]
                ),
                make_cloze(
                    "Karaciğer veya deride yerleşen benign vasküler tümörler olan hemanjiyomlar kapsülsüz büyüme sergileyen klasik patolojik istisnadır.",
                    "hemanjiyomlar",
                    "Benign damar tümörleri"
                )
            ]
        },
        # Slayt 18
        {
            "slideNumber": 18,
            "title": "Model Karşılaştırma: Leiomyom vs Leiomyosarkom",
            "content": (
                "Düz kas neoplazmları, benign ve malign davranış farkını kavramak için klasik bir tıp fakültesi modelidir. "
                "Uterusun benign düz kas tümörü olan 'leiomyom' (myom); küçük-orta boyutlu, çok iyi sınırlı, yuvarlak, "
                "kesit yüzeyi beyaz-gri renkte, girdapsı (vorteks) desen gösteren, nekroz ve atipik mitoz içermeyen bir kitledir. "
                "Buna karşılık uterusun malign düz kas tümörü olan 'leiomyosarkom'; genellikle dev boyutlu, sınırları belirsiz, "
                "çevre myometriuma sızan, kesit yüzeyi yumuşak ve etsi (balık eti kıvamında), geniş kanama ve koagülatif nekroz "
                "alanları içeren, bol atipik mitozlu ve uzak hematojen metastaz potansiyeline sahip ölümcül bir sarkomdur."
            ),
            "elements": [
                make_before_after(
                    "Uterus Düz Kas Tümörlerinin Patolojik Ayrımı",
                    "Leiomyom (Benign Myom)",
                    "Keskin sınırlı, beyaz girdapsı kesit yüzeyi, düzgün mekik hücreler, nekroz yok, mitoz çok az (<5/10 BBA).",
                    "Leiomyosarkom (Malign)",
                    "Sınırları belirsiz infiltratif kitle, balık eti kıvamı, yaygın kanama-nekroz, pleomorfik hücreler ve bol atipik mitoz (>10/10 BBA).",
                    "Malign düz kas tanısında hücresel atipi, mitotik indeks ve koagülatif tümör nekrozu kritik triad oluşturur."
                ),
                make_active_recall(
                    "Bir uterin düz kas tümöründe leiomyom yerine leiomyosarkom tanısı koyduran en kritik mikroskobik kriter triadı nedir?",
                    "Hücresel atipi, yüksek mitotik figür sayısı ve tümör hücre nekrozudur.",
                    "Malign düzensizlik, bölünme sıklığı ve doku ölümü"
                )
            ]
        },
        # Slayt 19 [CHECKPOINT 2]
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Benign ve Malign Neoplazmlar",
            "content": (
                "Bu bölümde benign ve malign tümörlerin morfolojik, biyolojik ve davranışsal farklarını özetledik. "
                "Benign tümörler iyi diferansiye olup normale benzer; genellikle fibröz bir kapsülle çevrilidir ve iterek büyürler. "
                "Malign tümörler ise kapsülsüzdür, çevre dokuları yıkarak lokal invazyon yaparlar ve uzak metastaz yeteneğine sahiptirler. "
                "Büyüme hızı tek başına kriter değildir; hormonal uyarıyla benign kitleler (leiomyom) gebelikte aniden hızla büyüyebilir. "
                "Hemanjiyomlar benign olmalarına rağmen kapsülsüz olabilen klasik morfolojik istisnalardır. "
                "Kafatası içindeki benign meningiomlar veya endokrin kitleler (insülinoma) yerleşimleri nedeniyle ölümcül olabilir. "
                "Leiomyom düzgün sınırlı girdapsı iken, leiomyosarkom kanama-nekroz içeren, bol atipik mitozlu infiltratif bir kitledir."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp02-fc01",
                    "front": "Benign bir neoplazm olmasına rağmen belirgin fibröz kapsülü bulunmayan ve çevre dokuya sınırsız yayılabilen damar tümörü nedir?",
                    "back": "Hemanjiyom tümörüdür.",
                    "hint": "Vasküler endotel kaynaklı kitle"
                },
                {
                    "id": "k1-28-cp02-fc02",
                    "front": "Histolojik olarak tamamen iyi huylu olan kafa içi bir kitlenin ölümcül sonuç doğurmasına yol açan primer faktör nedir?",
                    "back": "Kritik anatomik yerleşimidir.",
                    "hint": "Hayatsal merkezlere bası konumu"
                },
                {
                    "id": "k1-28-cp02-fc03",
                    "front": "Uterus düz kas neoplazmlarında iyi huylu leiomyomu kötü huylu leiomyosarkomdan ayıran en kritik makroskobik bulgu nedir?",
                    "back": "Yaygın kanama ve nekrozdur.",
                    "hint": "Doku ölümü ve vasküler göllenme odakları"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 2 Özet Tablosu: Benign vs Malign Biyolojik Davranış",
                    ["Ölçüt", "Benign Davranış", "Malign Davranış"],
                    [
                        {
                            "cells": ["Büyüme Şekli", "Ekspansil, itici, kapsüllü", "İnfiltratif, invaziv, kapsülsüz"],
                            "hiddenIndex": 1,
                            "hint": "Zar yapısı ve dokuyu itme"
                        },
                        {
                            "cells": ["Metastaz Kabiliyeti", "Kesinlikle Sıfır", "Mevcut (Malignitenin ana kuralı)"],
                            "hiddenIndex": 1,
                            "hint": "Metastatik potansiyel yokluğu"
                        }
                    ]
                )
            ]
        },
        # Slayt 20
        {
            "slideNumber": 20,
            "title": "Klinik Karar: Cerrahi Sınır Marjinlerinin Değerlendirilmesi",
            "content": (
                "Kanser cerrahisinde çıkarılan spesimenin patolojik incelenmesinde en hayati basamak 'cerrahi sınır' "
                "(rezeksiyon marjini) kontrolüdür. Patolog rezeke edilen dokunun dış yüzeyini özel kalıcı çini mürekkepleriyle "
                "boyar. Mikroskop altında tümör hücrelerinin mürekkepli cerrahi sınıra temas ettiği görülürse 'pozitif cerrahi sınır' "
                "(R1 rezeksiyon) rapor edilir. Pozitif sınır, hastanın vücudunda mikroskobik tümör odaklarının geride kaldığını "
                "kanıtlar ve lokal nüks riskini katlar; bu durum hastanın yeniden ameliyata alınarak re-eksizyon yapılmasını "
                "veya cerrahi yatağa ek radyoterapi verilmesini zorunlu kılar. Sınır negatif (R0) ise cerrahi küratif kabul edilir."
            ),
            "elements": [
                make_branching_logic(
                    "Meme karsinomu nedeniyle meme koruyucu cerrahi uygulanan 48 yaşında hastanın patoloji raporunda, boyalı lateral cerrahi sınırda mürekkeple temas eden invaziv tümör adacıkları (pozitif sınır) saptanıyor.",
                    "Bu patolojik rapor karşısında multidisipliner onkoloji konseyinin alması gereken en doğru klinik karar ne olmalıdır?",
                    [
                        {
                            "text": "Lokal nüksü engellemek amacıyla cerrahi yatak yeniden açılarak lateral marjin re-eksizyonu yapılmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; pozitif cerrahi sınır geride kanser kaldığını gösterir ve re-eksizyon gerektirir."
                        },
                        {
                            "text": "Tümör tamamen çıkarılmış kabul edilerek hasta hiçbir tedavi verilmeden taburcu edilmelidir.",
                            "isCorrect": False,
                            "explanation": "Sınır pozitifliği tedavi edilmezse lokal nüks kaçınılmazdır."
                        },
                        {
                            "text": "Hastaya derhal profilaktik kemik iliği nakli uygulanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Lokal cerrahi sınır pozitifliği kemik iliği nakli endikasyonu değildir."
                        }
                    ]
                )
            ]
        }
    ]
