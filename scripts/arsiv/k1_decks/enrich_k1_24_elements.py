# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_24_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar senaryoları) ögeleri (25 adet)."""
    return {
        2: make_branching_logic(
            "Acil servise ani başlayan nefes darlığı, plöritik göğüs ağrısı ve hemoptizi ile getirilen 62 yaşında bir hastada sağ bacakta asimetrik şişlik ve hassasiyet saptanıyor.",
            "Hastanın hemodinamisi stabil olduğuna göre acil patofizyolojik tanı ve doğrulama stratejisi ne olmalıdır?",
            [
                {
                    "text": "Derin ven trombozu kaynaklı pulmoner tromboembolizm ön tanısıyla acil kontrastlı toraks BT anjiyografi planlanması",
                    "isCorrect": True,
                    "feedback": "Mükemmel Patolojik ve Klinik Yaklaşım: Pulmoner embolilerin >%95'i alt ekstremite derin ven trombozundan köken alır; kontrastlı BT anjiyografi tıkalı pulmoner dalları gösteren altın standarttır."
                },
                {
                    "text": "Hastada yalnızca primer bakteriyel lober pnömoni düşünülerek ampirik oral antibiyotik başlanıp taburcu edilmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı ve ölümcül: Bacakta asimetrik ödem ve ani plöritik ağrı pulmoner tromboembolizmin klasik tablosudur; emboli atlanırsa masif obstrüksiyonla ani ölüm gelişebilir."
                }
            ]
        ),
        4: make_branching_logic(
            "Pulmoner arter ana dallarını tam tıkayan eyer (saddle) emboli tanısı konulan bir hastada ani senkop, derin hipotansiyon ve boyun venlerinde masif dolgunluk gelişiyor.",
            "Bu hemodinamik tablonun altta yatan primer patofizyolojik mekanizması nedir?",
            [
                {
                    "text": "Sağ ventrikül çıkış yolunun mekanik obstrüksiyonuna bağlı akut kor pulmonale ve sol kalbe kan dönüşünün çökmesi",
                    "isCorrect": True,
                    "feedback": "Doğru Patofizyolojik Değerlendirme: Eyer emboli sağ ventrikülün pulmoner yatağa kan pompalamasını aniden engeller; akut sağ kalp yetmezliği ve sol kalp dolum çöküşü gelişir."
                },
                {
                    "text": "Sistemik arteriyoler yatakta yaygın vazodilatasyona bağlı sıcak şok gelişimi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Eyer emboli obstrüktif mekanik şok tablosudur; periferik vazodilatasyon değil, kompansatuar vazokonstriksiyon görülür."
                }
            ]
        ),
        6: make_branching_logic(
            "Femur cisim kırığı nedeniyle ortopedi servisinde yatan genç bir hastada kırığın 48. saatinde ani solunum sıkıntısı, konfüzyon ve aksiller bölgede peteşiyal döküntüler beliriyor.",
            "Klinik tablonun patolojik tanısı ve lezyonların mikroskobik zemini nedir?",
            [
                {
                    "text": "Kemik iliği kökenli yağ embolisi sendromudur; lipid damlacıkları mikrovasküler lümenleri tıkayarak endotel hasarı yapar",
                    "isCorrect": True,
                    "feedback": "Kusursuz Patoloji Bilgisi: Uzun kemik kırıklarından 1-3 gün sonra gelişen dispne, konfüzyon ve peteşi klasik yağ embolisi triadıdır."
                },
                {
                    "text": "Kemik iliğinden kaynaklanan masif gaz embolisidir ve hiperbarik oksijen odası dışında tedavisi yoktur",
                    "isCorrect": False,
                    "feedback": "Hatalı: Kırık sonrası saçılan materyal gaz kabarcığı değil, medüller kavitedeki nötral lipid damlacıklarıdır."
                }
            ]
        ),
        8: make_branching_logic(
            "Zorlu ve uzamış bir doğum eylemi sırasında aniden derin siyanoz, dispne, şok tablosu ve vajinal kontrolsüz kanama gelişen lohusa annede ölüm gerçekleşiyor.",
            "Otopsi incelemesinde pulmoner damarlarda hangi patognomonik mikroskobik bulgu beklenir?",
            [
                {
                    "text": "Maternal pulmoner mikrodolaşımda fetal skuamöz epitel hücreleri, lanugo kılları ve mukus birikintileri",
                    "isCorrect": True,
                    "feedback": "Doğru Histopatolojik Tanı: Uterin ven yırtılmasıyla anne kanına karışan amniyon sıvısı skuamöz hücreler ve lanugo kıllarıyla pulmoner kapillerleri tıkar ve DİK'i tetikler."
                },
                {
                    "text": "Alveol duvarlarında yalnızca amiloid fibril depolanması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bu akut tablonun amiloidozla ilişkisi yoktur; primer amniyon sıvısı embolisidir."
                }
            ]
        ),
        12: make_branching_logic(
            "Tüplü dalış (scuba) yapan bir dalgıç su yüzeyine çok hızlı yükseliyor ve dakikalar içinde şiddetli retrosternal ağrı, nefes darlığı ve eklem ağrıları ile kıvranmaya başlıyor.",
            "Bu akut hemodinamik krizin patogenezi ve temel fiziksel gaz bileşeni hangisidir?",
            [
                {
                    "text": "Kanda çözünmüş azot (nitrojen) gazının ani dekompresyonla gaz kabarcıklarına dönüşmesi ve damarları tıkaması (vurgun)",
                    "isCorrect": True,
                    "feedback": "Mükemmel Fizyopatoloji: Yüksek basınçta kanda çözünen nitrojen, ani yüzeye çıkışta kandan gaz fazına ayrışır ve damar içinde mikroemboliler oluşturur."
                },
                {
                    "text": "Karbondioksit gazının eritrositler içinde kristalize olarak damar duvarını yırtması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Dekompresyon hastalığının temel gazı yüksek oranda çözünen azot (N2) gazıdır."
                }
            ]
        ),
        14: make_branching_logic(
            "Kronik dekompresyon hastalığı olan eski bir profesyonel dalgıçta iki taraflı kalça ağrısı ve hareket kısıtlılığı saptanıyor. Radyografide femur başında avasküler çökme görülüyor.",
            "Bu kronik patolojik tablonun tıbbi adı ve kemikteki histopatolojisi nedir?",
            [
                {
                    "text": "Caisson hastalığı zemininde gelişen aseptik iskemik kemik nekrozu (osteonekroz)",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik Patoloji: Azot kabarcıklarının kemik iliğinde kalıcı iskemik tıkanıklık yapması sonucu femur başı ve tibyada kalıcı aseptik osteonekroz (Caisson) gelişir."
                },
                {
                    "text": "Gut artritine bağlı ürat kristalleri birikimi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Caisson hastalığı pürin metabolizması hastalığı değil, gaz embolisine bağlı avasküler nekrozdur."
                }
            ]
        ),
        16: make_branching_logic(
            "Sol atriyal fibrilasyonu olan 74 yaşındaki bir hastada aniden sol bacakta şiddetli ağrı, soğukluk, solukluk ve nabızsızlık gelişiyor.",
            "Bu arteriyel embolinin en olası kaynak noktası ve patolojik mekanizması nedir?",
            [
                {
                    "text": "Sol atriyal apendikste staza bağlı oluşan mural trombüsten kopan sistemik arteriyel tromboemboli",
                    "isCorrect": True,
                    "feedback": "Kusursuz Klinik Patoloji: Sistemik arteriyel embolilerin %80'i sol kalp mural trombüslerinden (AF'de atriyum, MI'da sol ventrikül) kaynaklanır ve en sık alt ekstremite arterlerini tıkar."
                },
                {
                    "text": "Bacak derin venlerinde oluşan DVT'nin doğrudan femoral artere atlaması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Normal dolaşımda venöz pıhtı artere geçemez (paradoksal emboli hariç); sistemik emboliler sol kalpten kaynaklanır."
                }
            ]
        ),
        18: make_branching_logic(
            "Akut transmural anterior miyokard enfarktüsü geçiren bir hastanın 5. gününde ekokardiyografide sol ventrikül apeksinde akinezi ve lümene uzanan organize trombüs saptanıyor.",
            "Bu trombüsün periferik dolaşıma kopması halinde gelişecek en tehlikeli komplikasyon hangisidir?",
            [
                {
                    "text": "Serebral arteriyel yatağa embolize olarak iskemik serebral enfarktüs (inme) geliştirmesi",
                    "isCorrect": True,
                    "feedback": "Doğru Nörovasküler Değerlendirme: Sol ventrikül mural trombüsleri karotis ve serebral arterlere (özellikle MCA) atılarak masif iskemik inmelere yol açabilir."
                },
                {
                    "text": "Karaciğer portal venine giderek portal hipertansiyon oluşturması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Sol kalpten çıkan arteriyel emboliler portal vene değil, çölyak/mezenterik arterler aracılığıyla sistemik organlara gider."
                }
            ]
        ),
        22: make_branching_logic(
            "Şiddetli aterosklerozu olan yaşlı bir hastada koroner anjiyografi sonrası akut böbrek yetmezliği, parmaklarda morarma (mavi parmak) ve karın ağrısı gelişiyor.",
            "Böbrek biyopsisinde glomerüler arteriyollerde hangi karakteristik patoloji beklenir?",
            [
                {
                    "text": "Arteriyol lümenini dolduran bikonveks, iğsi şekilli kolesterol kristali yarıkları (kolesterol aterom embolisi)",
                    "isCorrect": True,
                    "feedback": "Mükemmel Histopatoloji: Aort içi kateter manipülasyonu aterom plaklarını yırtarak kolesterol kristallerini periferik arteriyollere döker; dokuda iğsi yarıklar karakteristiktir."
                },
                {
                    "text": "Tüm lümende tek biçimli amiloid AL depolanması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bu tablo amiloidoz değil, aterosklerotik plağın yırtılmasıyla gelişen kolesterol embolizmidir."
                }
            ]
        ),
        24: make_branching_logic(
            "Masif DVT saptanan bir hastada sol ventrikülden köken alan herhangi bir patoloji olmaksızın aniden serebral inme gelişiyor. EKO'da patent foramen ovale (PFO) tespit ediliyor.",
            "Venöz pıhtının arteriyel dolaşıma geçtiği bu istisnai emboli tipine ne ad verilir?",
            [
                {
                    "text": "Sağ-sol kardiyak şant üzerinden arteriyel yatağa geçen paradoksal emboli",
                    "isCorrect": True,
                    "feedback": "Doğru Patoloji Tanımı: Normalde akciğerde filtre olan venöz pıhtı, PFO veya ASD gibi defektlerden sağdan sola geçerek beyne ulaştığında paradoksal emboli adını alır."
                },
                {
                    "text": "Retrograd lenfatik emboli",
                    "isCorrect": False,
                    "feedback": "Hatalı: Pıhtı kardiyak şanttan geçmiştir; lenfatik yolla arteriyel sisteme geçiş olmaz."
                }
            ]
        ),
        26: make_branching_logic(
            "Santral venöz kateter takılması sırasında hastanın derin nefes almasıyla kateter ucundan sisteme hava kaçıyor ve hasta aniden siyanoz ile senkopa giriyor.",
            "Sağ ventrikülde hava kilidi (air lock) gelişen hastaya acil olarak verilmesi gereken pozisyon hangisidir?",
            [
                {
                    "text": "Sol lateral dekübit ve Trendelenburg pozisyonu (sağ ventrikül tepe noktasında havayı hapsedip pulmoner çıkışı açmak)",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik Acil Kararı: Sol yan yatış ve baş aşağı eğim havanın sağ ventrikül tepe noktasında toplanmasını sağlayarak pulmoner arter kapağının tıkanmasını engeller."
                },
                {
                    "text": "Yüksek Fowler dik oturur pozisyon",
                    "isCorrect": False,
                    "feedback": "Hatalı: Dik pozisyonda hava kabarcıkları doğrudan pulmoner arter çıkış kapağına yükselerek çıkış yolunu tamamen kilitler."
                }
            ]
        ),
        28: make_branching_logic(
            "İleri evre musinöz adenokarsinomu olan bir hastanın otopsisinde akciğer mikrovasküler lümenlerinde tümör hücre agregatları ve çevresinde taze mikrotrombüsler izleniyor.",
            "Bu patolojik tablonun klinik tıptaki adı ve yayılım biçimi nedir?",
            [
                {
                    "text": "Malign tümör hücre embolisi ve mikrovasküler karsinomatoz lenfanjit/arteriyolit",
                    "isCorrect": True,
                    "feedback": "Doğru Onkopatoloji: Kanser hücre kümeleri damar içine girerek embolus gibi davranabilir ve mikrodolaşımı tıkayarak lokal iskemik hasara yol açabilir."
                },
                {
                    "text": "Benign leiomyomatozis",
                    "isCorrect": False,
                    "feedback": "Hatalı: Malign glandüler kanserlerin damar invazyonu tümör embolizmidir."
                }
            ]
        ),
        32: make_branching_logic(
            "Sol böbrek arterinin bir dalı akut emboli ile tıkanan bir hastada 48 saat sonra otopsi veya nefrektomi materyali inceleniyor.",
            "Uç arter dolaşımlı böbrek parankiminde gelişen enfarktüsün makroskopik rengi ve geometrisi nedir?",
            [
                {
                    "text": "Tabanı böbrek korteksine, tepesi tıkalı damara bakan kama biçimli beyaz (soluk/anemik) enfarktüs",
                    "isCorrect": True,
                    "feedback": "Kusursuz Patoloji Bilgisi: Uç arterli solid organlarda (böbrek, dalak, kalp) doku sert olduğu için kan sızamaz; enfarktüs soluk beyaz renkte ve kama biçimlidir."
                },
                {
                    "text": "Tüm böbreğe yayılan yuvarlak siyah difüz amiloidoz alanı",
                    "isCorrect": False,
                    "feedback": "Hatalı: Böbrek enfarktüsü siyah difüz amiloidoz değil, sınırları keskin beyaz kama lezyonudur."
                }
            ]
        ),
        34: make_branching_logic(
            "Kronik sol kalp yetmezliği olan bir hastada alt lob pulmoner arter dalı tıkanıyor ve hasta plöritik ağrı ile hemoptizi çıkarıyor.",
            "Çift kan dolaşımına sahip akciğer dokusunda gelişen bu enfarktüsün rengi ve morfolojisi nedir?",
            [
                {
                    "text": "Bronşiyal arterlerden kan sızması nedeniyle tabanı plevraya bakan kırmızı (hemorajik) kama enfarktüs",
                    "isCorrect": True,
                    "feedback": "Doğru Organ Morfolojisi: Akciğer hem pulmoner hem bronşiyal çift dolaşıma sahiptir; tıkanan alana bronşiyal sistemden kan sızdığı için kırmızı enfarktüs oluşur."
                },
                {
                    "text": "Tamamen kansız, porselen beyazı sert kalsifikasyon nodülü",
                    "isCorrect": False,
                    "feedback": "Hatalı: Akciğer gevşek dokulu ve çift dolaşımlı olduğu için enfarktüsü beyaz değil daima kırmızıdır."
                }
            ]
        ),
        36: make_branching_logic(
            "Tromboemboliye bağlı akut transvers kolon iskemisi gelişen bir hastada laparotomide bağırsak anslarının mor-siyah renkte, ödemli ve lümeninin kanlı olduğu görülüyor.",
            "İnce veya kalın bağırsak enfarktüslerinin daima kırmızı (hemorajik) olmasının nedeni nedir?",
            [
                {
                    "text": "Zengin kollateral mezenterik damar ağından nekrotik gevşek alana kan sızması ve venöz drenaj yetersizliği",
                    "isCorrect": True,
                    "feedback": "Mükemmel Anatomi ve Patoloji: Bağırsak duvarı zengin anastomozlara sahip gevşek bir dokudur; kan nekroz alanına serbestçe dolarak kırmızı enfarktüs yapar."
                },
                {
                    "text": "Bağırsakta hiçbir zaman arteriyel kanlanmanın bulunmaması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bağırsak SMA ve IMA gibi dev arterlerle kanlanır; anastomozların zenginliği kanamaya yol açar."
                }
            ]
        ),
        38: make_branching_logic(
            "Akut testis torsiyonu geçiren 16 yaşındaki bir erkekte spermatik kord 360 derece dönüyor. Cerrahi eksplorasyonda testisin masif büyüdüğü ve patlıcan moru renge büründüğü saptanıyor.",
            "Bu tablonun patofizyolojik mekanizması ve enfarktüs tipi hangisidir?",
            [
                {
                    "text": "İnce duvarlı venöz dönüşün tıkanması sonucu kanın dokudan çıkamamasına bağlı kırmızı (venöz) enfarktüs",
                    "isCorrect": True,
                    "feedback": "Kusursuz Patoloji Bilgisi: Torsiyonda venler hemen tıkanır, kalın duvarlı arter kan pompalamaya devam eder; organ kanla göllenir ve venöz kırmızı enfarktüs gelişir."
                },
                {
                    "text": "Yalnızca lenfatik sıvı fazlalığına bağlı beyaz parankim şişmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Testis torsiyonu saf venöz tıkanmaya bağlı masif hemorajik enfarktüs örneğidir."
                }
            ]
        ),
        42: make_branching_logic(
            "Sol anterior inen (LAD) koroner arteri tıkanan bir hastada akut miyokard enfarktüsünün 24. saatinde etkilenen bölgenin histopatolojik incelemesinde ne görülür?",
            "İskemik miyositlerde beklenen klasik hücresel nekroz paterni hangisidir?",
            [
                {
                    "text": "Hücre çekirdeklerinin kaybolduğu (karyolizis), sitoplazmanın hipereozinofilik boyandığı koagülatif nekroz ve nötrofil infiltrasyonu",
                    "isCorrect": True,
                    "feedback": "Doğru Histopatoloji: Miyokard enfarktüsünün ilk 24-48 saatinde hayalet hücreler (koagülatif nekroz), dalgalı lifler ve nötrofil akını karakteristiktir."
                },
                {
                    "text": "Yaygın granülomatöz dev hücreler ve kazeifikasyon nekrozu",
                    "isCorrect": False,
                    "feedback": "Hatalı: Kazeifikasyon tüberküloza özgüdür; iskemik miyokard koagülatif nekroza girer."
                }
            ]
        ),
        44: make_branching_logic(
            "Sağ orta serebral arter (MCA) tıkanıklığı nedeniyle sol hemipleji gelişen bir hastanın 2 hafta sonraki beyin MRG ve otopsisinde enfarkt alanı inceleniyor.",
            "Beyin parankiminde gelişen enfarktüsün diğer organlardan farkı olan nekroz türü hangisidir?",
            [
                {
                    "text": "Yüksek lipid ve hidrolitik enzimler nedeniyle dokunun eriyip kiste dönüştüğü sıvılaşma (likuefaksiyon) nekrozu",
                    "isCorrect": True,
                    "feedback": "Kusursuz Beyin Patolojisi Kuralı: Santral sinir sisteminde iskemik nekroz koagülatif DEĞİL, daima sıvılaşma (likuefaksiyon) nekrozu ile kavitasyon oluşturur."
                },
                {
                    "text": "Kalsiyum sabunlaşmasıyla seyreden enzimatik yağ nekrozu",
                    "isCorrect": False,
                    "feedback": "Hatalı: Yağ nekrozu akut pankreatitte veya meme travmasında görülür; beyinde likuefaksiyon nekrozu olur."
                }
            ]
        ),
        46: make_branching_logic(
            "Transmural miyokard enfarktüsü geçiren bir hastada 1-2 ay sonra nekroz alanının tamamen skar dokusuna dönüştüğü görülüyor.",
            "İyileşen miyokard enfarktüsü alanında parankimal hücre rejenerasyonu neden gerçekleşemez?",
            [
                {
                    "text": "Erişkin kardiyak miyositlerin kalıcı (permanent) hücre olup bölünme yeteneğinin bulunmaması",
                    "isCorrect": True,
                    "feedback": "Doğru Hücre Biyolojisi: Nöronlar ve kalp kası hücreleri bölünemez; ölen parankim kollajen skar dokusu ile onarılır."
                },
                {
                    "text": "Kalp kasında kollajen sentezleyen hiçbir fibroblastın bulunmaması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Fibroblastlar bol miktarda bulunur ve nekroz alanını kollajen skar dokusuna dönüştürür."
                }
            ]
        ),
        48: make_branching_logic(
            "Beyin dokusunda geniş sıvılaşma nekrozu geliştikten 6 ay sonra çekilen kranial görüntülemede kistik bir boşluk saptanıyor.",
            "Beyinde fibröz kollajen skar yerine kist çeperini oluşturan astrosit proliferasyonuna ne ad verilir?",
            [
                {
                    "text": "Reaktif astrositlerin uzantılarıyla oluşturduğu glial skar (gliozis dokusu)",
                    "isCorrect": True,
                    "feedback": "Kusursuz Nöropatoloji: Santral sinir sisteminde fibroblast azdır; doku tamiri gitter hücreleri (makrofajlar) ve astrositik gliozis ile sağlanır."
                },
                {
                    "text": "Primer Schwannoma proliferasyonu",
                    "isCorrect": False,
                    "feedback": "Hatalı: Schwann hücreleri periferik sinirlerdedir; beyin parankiminde gliozisi astrositler yapar."
                }
            ]
        ),
        52: make_branching_logic(
            "Subakut bakteriyel endokardit vejetasyonundan kopan bir septik embolus dalak arteriyolünü tıkıyor.",
            "Enfarkt alanında steril koagülatif nekroz yerine yoğun nötrofilik erime ve püy birikmesiyle karakterize lezyon nedir?",
            [
                {
                    "text": "Septik enfarktüs ve sekonder dalak apsesi oluşumu",
                    "isCorrect": True,
                    "feedback": "Doğru Patoloji Bilgisi: Canlı pirojenik bakteri içeren trombüs dokuya ulaştığında enfarktüs süpüratif erimeye uğrar ve apseye dönüşür."
                },
                {
                    "text": "Steril beyaz hyalin plak oluşumu",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bakteriyel varlık nötrofilleri çeker ve apse oluşturur."
                }
            ]
        ),
        54: make_branching_logic(
            "Hangi organın iskemik enfarktüslere karşı direnci, zengin çift dolaşımı (karaciğer arteri ve portal ven) sayesinde en yüksektir?",
            "İzole karaciğer arter tıkanmasında parankimin canlı kalabilmesinin anatomik nedeni nedir?",
            [
                {
                    "text": "Hepatik arter tıkansa bile karaciğerin oksijen ihtiyacının yaklaşık yarısını portal venöz akımdan karşılayabilmesi",
                    "isCorrect": True,
                    "feedback": "Doğru Hepatoselüler Fizyoloji: Karaciğer çift dolaşıma sahiptir; portal ven parsiyel oksijenlenmiş kan taşıyarak enfarktüs gelişimini büyük oranda önler."
                },
                {
                    "text": "Karaciğer parankiminin hiç oksijene ihtiyaç duymadan anaerobik yaşaması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Karaciğer yüksek metabolik organ olup oksijene muhtaçtır; koruma çift dolaşımla sağlanır."
                }
            ]
        ),
        56: make_branching_logic(
            "Akut koroner sendrom nedeniyle primer perkütan koroner girişim (anjiyografi ile stent) yapılan bir hastada reperfüzyon sonrası kardiyak enzimlerde ani sıçrama ve ventriküler aritmi görülüyor.",
            "Tıkalı damar açılmasına rağmen doku hasarının artması tablosuna ne ad verilir?",
            [
                {
                    "text": "Oksijen serbest radikalleri ve kalsiyum yüklenmesiyle tetiklenen reperfüzyon hasarı",
                    "isCorrect": True,
                    "feedback": "Kusursuz Patofizyoloji: Tıkalı damarın hızla açılması dokuya bol oksijen getirir; hasarlı mitokondriler masif serbest radikal (ROS) üreterek kontraksiyon band nekrozunu artırır."
                },
                {
                    "text": "Primer kardiyak sarkoidoz atağı",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bu akut patoloji reperfüzyon hasarı ve kontraksiyon band nekrozudur."
                }
            ]
        ),
        58: make_branching_logic(
            "Şokta hücrelerin hipoksiye duyarlılıkları karşılaştırıldığında, 3-4 dakika içinde geri dönüşümsüz nekroza giren en hassas hücre grubu hangisidir?",
            "Hücresel iskemiye direnç sıralaması patolojik olarak nasıldır?",
            [
                {
                    "text": "Nöronlar (3-4 dk) > Miyositler (20-30 dk) > Fibroblastlar ve osteositler (saatler)",
                    "isCorrect": True,
                    "feedback": "Doğru Patoloji Hiyerarşisi: Beyin nöronları en hassas (3-4 dk), miyokard orta (20-30 dk), mezenkimal bağ dokusu hücreleri ise en dirençlidir."
                },
                {
                    "text": "Kemik hücreleri nöronlardan çok daha erken saatler içinde ölür",
                    "isCorrect": False,
                    "feedback": "Hatalı: Fibroblast ve kemik hücreleri saatlerce iskemiye dayanabilir."
                }
            ]
        )
    }

def get_extra_sliders():
    """Before-after slider (patolojik durum ve doku karşılaştırma) ögeleri (18 adet)."""
    return {
        3: make_before_after(
            "Tromboz ve Emboli Karşılaştırması",
            "Lokalize Trombüs",
            "Damar duvarına yapışık, endotel hasarı zemininde oluşan organize pıhtı kitlesi",
            "Dolaşan Emboli",
            "Kaynak noktasından koparak kan akımıyla uzak doku mikrodolaşımını tıkayan kitle"
        ),
        5: make_before_after(
            "Pulmoner Emboli Şiddet Yelpazesi",
            "Küçük Periferik Emboli",
            "Sessiz klinik veya plöritik ağrı, kama biçimli kırmızı pulmoner enfarktüs",
            "Masif Eyer (Saddle) Emboli",
            "Pulmoner ana trunkus tıkanması, akut sağ ventrikül dilatasyonu ve ani arrest"
        ),
        7: make_before_after(
            "DVT ve Sistemik Arteriyel Tromboz Kaynakları",
            "Venöz Tromboembolizm Kaynağı",
            "Alt ekstremite derin venleri (femoral, popliteal, iliyak venler) ve pelvik venler",
            "Sistemik Tromboembolizm Kaynağı",
            "Sol ventrikül duvarı (MI sonrası), sol atriyal apendiks (AF) ve aort aterom plakları"
        ),
        11: make_before_after(
            "Akut vs Kronik Dekompresyon Patolojisi",
            "Akut Vurgun (Bends & Chokes)",
            "Eklem periartiküler gaz kabarcıkları, substernal solunum sıkıntısı ve amfizem",
            "Kronik Caisson Hastalığı",
            "Femur ve humerus başında kalıcı aseptik osteonekroz ve eklem harabiyeti"
        ),
        15: make_before_after(
            "Hava Embolisi Hacim Eşiği ve Sonuçları",
            "Küçük Venöz Hava Kabarcıkları (<20 ml)",
            "Pulmoner kapiller yatakta mikrokabarcıkların sessizce emilmesi ve kompanse edilmesi",
            "Masif Venöz Hava Girişi (>100 ml)",
            "Sağ ventrikülde hava köpüğü kilidi (air lock) ve mekanik debi çöküşü"
        ),
        21: make_before_after(
            "Amniyon Sıvısı Embolisinde İkili Tehlike",
            "Mekanik Pulmoner Obstrüksiyon",
            "Fetal skuamöz debrislerin pulmoner arteriyolleri tıkayarak bronkospazm yapması",
            "Anafilaktoid ve Koagülasyon Çöküşü",
            "Masif doku faktörü salınımıyla dissemine intravasküler koagülasyon (DİK) ve atoni"
        ),
        23: make_before_after(
            "Beyaz (Anemik) vs Kırmızı (Hemorajik) Enfarktüs",
            "Beyaz Enfarktüs (Solid Organ)",
            "Kalp, böbrek ve dalakta uç arter tıkanmasıyla oluşan kansız soluk iskemik nekroz",
            "Kırmızı Enfarktüs (Gevşek/Çift Dolaşım)",
            "Akciğer, bağırsak ve testiste kanın nekrotik sahaya göllenmesiyle oluşan hemorajik alan"
        ),
        27: make_before_after(
            "Enfarktüs İyileşme Basamakları",
            "Erken Nekroz Fazı (1-3 Gün)",
            "Koagülatif hayalet hücreler, nötrofil infiltrasyonu ve belirgin hiperemi halkası",
            "Geç Skar Fazı (Haftalar-Aylar)",
            "Kollajen birikimi, neovaskülarizasyon gerilemesi ve kalıcı fibröz bağ dokusu skarı"
        ),
        31: make_before_after(
            "Beyin ve Diğer Organların İskemik Nekroz Ayrımı",
            "Solid Organlar (Böbrek/Kalp)",
            "Hücresel mimarinin haftalarca korunduğu sert koagülatif hayalet nekroz",
            "Beyin Parankimi (Serebrum)",
            "Mikroglia makrofajları ve lizozomlarla hızla sıvılaşan likuefaksiyon kisti"
        ),
        33: make_before_after(
            "Kollajen Skar vs Glial Skar",
            "Sistemik Doku Skarı",
            "Fibroblastların bol tip I ve III kollajen senteziyle oluşturduğu sert skar dokusu",
            "Serebral Gliozis",
            "Astrositlerin uzantılarıyla ördüğü kistik boşluğu sınırlayan glial skar örgüsü"
        ),
        37: make_before_after(
            "Steril vs Septik Enfarktüs",
            "Steril Enfarktüs",
            "Mikroorganizma içermeyen koagülatif iskemik nekroz ve granülasyonla tamir",
            "Septik Enfarktüs",
            "Canlı bakteri taşıyan embolusla enfarktın apseye ve süpüratif erimeye dönüşmesi"
        ),
        41: make_before_after(
            "Doku Oksijen Hassasiyeti Hiyerarşisi",
            "Yüksek Hassasiyetli Hücreler",
            "Serebral korteks nöronları (3-4 dk) ve kardiyak miyositler (20-30 dk)",
            "Düşük Hassasiyetli Hücreler",
            "Fibroblastlar, kondrositler ve osteositler (saatlerce hipoksiye dayanıklı)"
        ),
        45: make_before_after(
            "Reperfüzyon Hasarı Dinamikleri",
            "İskemik Korunma Fazı",
            "Azalmış ATP, anaerobik glikoliz, intraselüler kalsiyum ve ksantin birikimi",
            "Oksijen Akını (Reperfüzyon)",
            "Masif süperoksit ve hidroksil radikalleri, mitokondri membran por açılması ve kontraksiyon bandları"
        ),
        51: make_before_after(
            "Kardiyojenik ve Hipovolemik Şok Ayrımı",
            "Hipovolemik Şok",
            "Volüm kaybı, düşük debi, düşük PCWP ve kompansatuar vazokonstriksiyon (yüksek SVR)",
            "Kardiyojenik Şok",
            "Miyokard pompa yetmezliği, düşük debi, yüksek PCWP ve kompansatuar yüksek SVR"
        ),
        53: make_before_after(
            "Erken vs Geç Septik Şok",
            "Erken Septik Şok (Sıcak Şok)",
            "Düşük periferik direnç, NO aracılı vazodilatasyon, sıcak pembe cilt ve yüksek debi",
            "Geç Septik Şok (Soğuk Şok)",
            "Miyokard depresyonu, DİK, kapiller kaçak, soğuk siyanotik cilt ve dekompanse arrest"
        ),
        55: make_before_after(
            "Sağlıklı Endotel vs Septik Endotel",
            "Sağlıklı Antitrombotik Endotel",
            "Trombomodulin, EPCR, TFPI ekspresyonu, serbest t-PA salınımı ve pürüzsüz yüzey",
            "Septik Prokoagülan Endotel",
            "Masif Doku Faktörü açığa çıkışı, PAI-1 fırlaması, lökosit adezyonu ve kapiller kaçak"
        ),
        57: make_before_after(
            "Şok Akciğeri (ARDS) Evreleri",
            "Eksüdatif Akut Faz",
            "Kapiller konjesyon, Tip I pnömosit dökülmesi ve pembe hiyalin membranlar",
            "Organize Proliferatif Faz",
            "Tip II pnömosit hiperplazisi, fibroblast göçü ve interstisyel fibrozis"
        ),
        60: make_before_after(
            "İskemik ATN Evreleri",
            "Başlangıç ve Oligürik Dönem",
            "Proksimal tübül epitel soyulması, granüler silendirler, GFR çöküşü ve azotemi",
            "İyileşme ve Poliürik Dönem",
            "Tübüler epitel rejenerasyonu, konsantrasyon yetersizliği nedeniyle bol idrar"
        )
    }

def get_extra_chains():
    """Causal chain (patofizyolojik mekanizma zinciri) ögeleri (19 adet)."""
    return {
        1: make_causal_chain(
            "Derin Ven Trombozundan Pulmoner Emboliye Kaskad",
            [
                "1. Venöz Staz ve Hasar: Virchow triadı zemininde bacak derin venlerinde fibrin pıhtısı oluşması",
                "2. Trombüsün Kopması: Kas kontraksiyonu veya basınçla pıhtı fragmanının ana venöz dolaşıma ayrılması",
                "3. Kaval ve Kardiyak Geçiş: İnferior vena kava ve sağ kalpten geçerek pulmoner arteriyel ağaca ulaşması",
                "4. Pulmoner Tıkanma: Çapı daralan pulmoner arter dallarında takılarak lokal perfüzyonu kesmesi"
            ]
        ),
        10: make_causal_chain(
            "Eyer (Saddle) Embolide Akut Sağ Kalp Yetmezliği",
            [
                "1. Bifurkasyon Tıkanması: Masif pıhtının ana pulmoner arter çatallanmasına tam oturması",
                "2. Sağ Ventrikül Ard Yük Artışı: Pulmoner vasküler direncin aniden aşırı yükselmesi",
                "3. Akut Kor Pulmonale: Sağ ventrikülün aşırı genişlemesi ve sistolik ejeksiyonun durması",
                "4. Kardiyak Kollaps: Sol ventriküle kan dönememesi sonucu kardiyak outputun sıfırlanması"
            ]
        ),
        13: make_causal_chain(
            "Yağ Embolisi Sendromu Patogenezi",
            [
                "1. Kemik Kırığı: Uzun kemik medüller venlerinin yırtılması ve lipid globüllerinin açığa çıkması",
                "2. Yağ Mikroembolileri: Yağ damlacıklarının pulmoner ve serebral kapillerleri mekanik tıkaması",
                "3. Toksik Serbest Yağ Asitleri: Lipaz enzimiyle yağların parçalanması ve toksik endotelyal lizis",
                "4. Sistemik Triad: Solunum sıkıntısı, ensefalopati konfüzyonu ve konjonktival peteşiler"
            ]
        ),
        17: make_causal_chain(
            "Amniyon Sıvısı Embolisinde Ölümcül Yolak",
            [
                "1. Uterin Ven Yırtılması: Doğum travmasıyla amniyon sıvısının maternal dolaşıma sızması",
                "2. Pulmoner Mikroemboli: Fetal skuamöz hücrelerin akciğer kapillerlerini mekanik tıkaması",
                "3. Anafilaktoid Yanıt: Sıvıdaki vazoaktif maddelerle şiddetli pulmoner vazokonstriksiyon ve şok",
                "4. DİK ve Tromboplastik Fırtına: Yüksek doku faktörü içeriğiyle kontrolsüz ölümcül kanama"
            ]
        ),
        25: make_causal_chain(
            "Gaz Embolisinde Dekompresyon (Vurgun) Mekanizması",
            [
                "1. Yüksek Basınçta Dalış: Derinlikte solunan havadaki azot gazının kanda ve yağ dokusunda çözünmesi",
                "2. Hızlı Yüzeye Çıkış: Ortam basıncının aniden düşmesiyle çözünmüş azotun gaz kabarcığına dönüşmesi",
                "3. İntravasküler Gaz Kilidi: Azot kabarcıklarının kemik ve eklem mikrodolaşımını mekanik tıkaması",
                "4. İskemik Ağrı ve Osteonekroz: Eklemde bükülme ağrıları (bends) ve Caisson aseptik kemik nekrozu"
            ]
        ),
        29: make_causal_chain(
            "Miyokard Enfarktüsünde Koagülatif Nekroz Kaskadı",
            [
                "1. Koroner Aterotromboz: Aterom plağının yırtılmasıyla lümende masif trombotik oklüzyon",
                "2. Oksidatif Fosforilasyon Kaybı: Saniyeler içinde mitokondriyal ATP sentezinin durması",
                "3. İyon Dengesi Çöküşü: Kalsiyum yüklenmesi, membran geçirgenliği ve geri dönüşümsüz miyosit ölümü",
                "4. Koagülatif İskelet: Hücresel enzimlerin inaktive olmasıyla hayalet hücre mimarisinin kalması"
            ]
        ),
        35: make_causal_chain(
            "Serebral İskemide Sıvılaşma (Likuefaksiyon) Nekrozu",
            [
                "1. Serebral Arter Oklüzyonu: Nöronlara oksijen ve glukoz iletiminin akut kesilmesi",
                "2. Nöronal Lizozomal Yıkım: Zengin hidrolitik enzimlerin hızla serbest kalarak hücreyi eritmesi",
                "3. Makrofaj Fagositozu: Gitter hücrelerinin lipid zengini miyelin enkazını temizlemesi",
                "4. Kistik Gliozis Boşluğu: Sıvılaşan alanın kiste dönmesi ve astrositik skar ile sınırlanması"
            ]
        ),
        43: make_causal_chain(
            "Testis Torsiyonunda Kırmızı Venöz Enfarktüs",
            [
                "1. Funikulus Rotasyonu: Spermatik kordun kendi ekseni etrafında dönmesi",
                "2. Venöz Drenaj Blokajı: Düşük basınçlı pampiniform venlerin anında tıkanması",
                "3. Arteriyel Girişin Sürmesi: Yüksek basınçlı testiküler arterin dokuya kan pompalamaya devam etmesi",
                "4. Masif Hemoraji ve Nekroz: Parankimin venöz kanla boğulması ve kırmızı enfarktüse dönüşmesi"
            ]
        ),
        47: make_causal_chain(
            "Enfarktüs İyileşmesinde Granülasyon Dokusu Kaskadı",
            [
                "1. İnflamatuar Akın: Nekroz sınırına ilk 24-48 saatte nötrofillerin ve ardından makrofajların göçü",
                "2. Fagositik Temizlik: Ölü hücresel artıkların makrofajlarca enzimatik fagositozla yok edilmesi",
                "3. Anjiyogenez ve Fibroplazi: VEGF ve TGF-beta uyarımıyla yeni kapillerlerin ve fibroblastların belirmesi",
                "4. Skar Maturasyonu: Granülasyon dokusunun yoğun kollajen depolanmasıyla beyaz skara dönüşmesi"
            ]
        ),
        51: make_causal_chain(
            "Kardiyojenik Şokta İlerleyen Pompa Yetmezliği",
            [
                "1. Masif Miyokard Nekrozu: Sol ventrikül kas kitlesinin %40'ından fazlasının enfarktı",
                "2. İleri Akım Çöküşü: Sol ventrikül sistolik debisinin ve kardiyak outputun kritik düşmesi",
                "3. Geriye Akım Konjesyonu: Sol atriyal ve pulmoner kapiller uç basıncının (PCWP) aşırı artması",
                "4. Pulmoner Ödem ve Asfiksi: Alveollere transüda sızması ve hipokseminin miyokardı daha da bozması"
            ]
        ),
        71: make_causal_chain(
            "Septik Şokta Endotoksin Tanıma ve NF-kappaB Kaskadı",
            [
                "1. LPS Salınımı: Gram-negatif bakteri duvarından Lipid A parçacıklarının serbest kalması",
                "2. Kompleksleşme: Serumda LBP proteininin LPS'yi bağlayarak CD14 koreseptörüne sunması",
                "3. TLR-4 İletimi: Toll-benzeri reseptör 4 aracılığıyla hücre içi MyD88 sinyal kaskadının tetiklenmesi",
                "4. Transkripsiyonel Patlama: NF-kappaB'nin nükleusa girerek TNF ve IL-1 genlerini masif açması"
            ]
        ),
        73: make_causal_chain(
            "Septik Şokta Sitokin Fırtınası ve Nitrik Oksit Yolu",
            [
                "1. Makrofaj Aktivasyonu: TNF-alfa ve IL-1 sitokinlerinin sistemik dolaşıma dökülmesi",
                "2. iNOS İndüksiyonu: Damar düz kaslarında indüklenebilir nitrik oksit sentaz enziminin uyarılması",
                "3. Masif NO Üretimi: Damar endotel ve düz kasında aşırı cGMP birikimi ve kas gevşemesi",
                "4. Vazomotor Felç: Sistemik vasküler direncin çökmesi ve vazopressörlere yanıtsız hipotansiyon"
            ]
        ),
        75: make_causal_chain(
            "Dissemine İntravasküler Koagülasyon (DİK) İkili Kısır Döngüsü",
            [
                "1. Doku Faktörü Patlaması: Endotel ve monositlerden ekstrinsik yolak faktörünün kontrolsüz sunulması",
                "2. Mikrotromboz Dalgası: Kılcal damarlarda fibrin mikrotrombüsleri oluşması ve organ iskemisi",
                "3. Faktör Tüketimi: Fibrinojen, Faktör V, VIII ve trombositlerin tükenerek hemostazın sıfırlanması",
                "4. Masif Kanama ve Hemoraji: Tüketim koagülopatisiyle spontan purpura, peteşi ve fatal iç kanama"
            ]
        ),
        81: make_causal_chain(
            "Sitopatik Hipoksi ve Hücresel Enerji Çöküşü",
            [
                "1. Sitokin Toksisitesi: Peroksinitrit ve TNF'nin mitokondri Kompleks I ve IV'ü doğrudan inaktive etmesi",
                "2. Solunum Zinciri Durması: Hücreye oksijen ulaşsa bile mitokondrinin elektron aktaramaması",
                "3. ATP Tükenmesi: Hücre içi enerjinin sıfırlanması ve membran Na+/K+ pompalarının çökmesi",
                "4. Kalsiyum Yüklenmesi ve Otoliz: Sitoplazmaya kalsiyum akması ve lizozomal enzimlerin hücreyi eritmesi"
            ]
        ),
        83: make_causal_chain(
            "Laktik Asidoz ve Miyokard Depresyon Döngüsü",
            [
                "1. Doku Hipoperfüzyonu: Aerobik solunumun durması ve anaerobik glikolizin aşırı hızlanması",
                "2. Pirüvat-Laktat Dönüşümü: LDH enzimiyle laktat üretilmesi ve hepatik Cori klirensinin durması",
                "3. Asidemi: Arteriyel kan pH'ının kritik düzeyin (<7.20) altına inmesi",
                "4. Kontraktilite Felci: Düşük pH'ın miyokard kontraktilitesini ve periferik damar tonusunu çökertmesi"
            ]
        ),
        85: make_causal_chain(
            "Şok Akciğerinde (ARDS) Diffüz Alveoler Hasar",
            [
                "1. Nötrofil Aktivasyonu: Pulmoner kapillerlerde lökositlerin kümelenmesi ve proteaz salınımı",
                "2. Alveolokapiller Hasar: Kapiller endotel ve Tip I pnömosit hücrelerinin lizise uğraması",
                "3. Eksüda ve Hiyalin Membran: Fibrinden zengin plazmanın alveole dolup pembe tabaka oluşturması",
                "4. Refrakter Hipoksemi: Alveoler kollaps, sürfaktan kaybı ve oksijen difüzyonunun tamamen durması"
            ]
        ),
        87: make_causal_chain(
            "İskemik Akut Tübüler Nekrozda (ATN) Anüri Kaskadı",
            [
                "1. Renal Kortikal İskemi: Şokta gelişen vazokonstriksiyonla renal kan akımının kritik düşmesi",
                "2. Tübül Epitel Nekrozu: Proksimal tübül hücrelerinin parçalanarak bazal membrandan dökülmesi",
                "3. Lümen Obstrüksiyonu: Nekrotik debrislerin Tamm-Horsfall proteiniyle silendirler oluşturup tübülü tıkaması",
                "4. Geri Sızıntı ve Oligüri: Glomerüler filtratın interstisyuma geri kaçması ve idrar çıkışının durması"
            ]
        ),
        91: make_causal_chain(
            "Waterhouse-Friderichsen Sendromunda Adrenal Kriz",
            [
                "1. Meningokoksik Bakteriyemi: Neisseria meningitidis endotoksinlerinin sistemik DİK başlatması",
                "2. Adrenal Sinüzoid Trombozu: Zengin vasküler sürrenal korteks kapillerlerinde mikrotrombüsler",
                "3. Masif Hemorajik Nekroz: İki taraflı böbrek üstü bezi dokusunun kanamalı erimeye uğraması",
                "4. Akut Kortikosteroid Çöküşü: Kortizol yokluğuyla vazopressör yanıtsız derin şok ve ölüm"
            ]
        ),
        93: make_causal_chain(
            "Şokun İrreversibl Evresinde Terminal Çöküş",
            [
                "1. Lizozomal Membran Yırtılması: Hücre içi asit hidrolazların sitoplazmaya yayılarak organelleri sindirmesi",
                "2. İskemik Bağırsak Translokasyonu: Mukozal bariyerin çökmesiyle lüminal bakterilerin kana boşalması",
                "3. İkincil Toksemik Şok: Masif bakteriyemi ile derinleşen geri dönüşümsüz vazomotor felç",
                "4. Hücresel Ölüm ve Arrest: Resüsitasyona ve vazopressörlere yanıtsız çoklu organ ölümü"
            ]
        )
    }

def get_extra_recalls():
    """Active recall (yüksek verimli aktif hatırlama) ögeleri (7 adet)."""
    return {
        1: make_active_recall(
            "Klinik pratikte karşılaşılan embolilerin yüzde doksan dokuzundan fazlasının köken aldığı primer yapı nedir?",
            "Tromboembolidir (Kopan trombüs parçası).",
            "Hemostaz pıhtısından kopan kitle"
        ),
        11: make_active_recall(
            "Bacak derin ven trombozundan köken alan venöz embolilerin pulmoner yatağa gitmeden sistemik arteriyel dolaşıma geçtiği duruma ne ad verilir?",
            "Paradoksal emboli denir (PFO veya ASD üzerinden).",
            "Sağ-sol kardiyak şantlı emboli türü"
        ),
        21: make_active_recall(
            "Amniyon sıvısı embolisinde anne ölümünün arkasındaki iki temel ölümcül patoloji nedir?",
            "Anafilaktoid kardiyorespiratuar şok ve dissemine intravasküler koagülasyondur (DİK).",
            "Alerjik benzeri çöküş ve tüketim kanaması"
        ),
        31: make_active_recall(
            "Patolojide tüm solid organ enfarktüsleri koagülatif nekrozla sonlanırken, hangi organda her zaman likuefaksiyon (sıvılaşma) nekrozu görülür?",
            "Beyin (santral sinir sistemi) dokusudur.",
            "Yüksek lipidli eriyen serebral parankim"
        ),
        41: make_active_recall(
            "Testis torsiyonu veya strangüle fıtıkta venöz dönüşün engellenmesiyle gelişen enfarktüs tipi daima ne renktir?",
            "Kırmızı (hemorajik) renktedir.",
            "Venöz tıkanmada kan göllenmesi rengi"
        ),
        71: make_active_recall(
            "Septik şokta endotel hücreleri ve monositlerin yüzeyinde ekstrinsik koagülasyonu başlatan membran proteini hangisidir?",
            "Doku Faktörüdür (TF / Faktör III).",
            "Faktör VIIa ile kompleks kuran prokoagülan molekül"
        ),
        81: make_active_recall(
            "Şok akciğeri (ARDS) histopatolojisinde alveol duvarlarını kaplayan pembe protein-fibrin katmanlarına ne ad verilir?",
            "Hiyalin membranlar denir.",
            "Diffüz alveoler hasarın pembe camsı mikroskobik örtüsü"
        )
    }

def enrich_k1_24_elements(slides):
    """
    100 slaytlık listeyi alır, her slayta eksik elemanları dengeli şekilde ekleyerek
    tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
    """
    extra_branching = get_extra_branching()
    extra_sliders = get_extra_sliders()
    extra_chains = get_extra_chains()
    extra_recalls = get_extra_recalls()

    for idx, slide in enumerate(slides, start=1):
        elements = slide.get("interactiveElements") or slide.get("elements") or []

        if idx in extra_branching:
            elements.append(extra_branching[idx])
        if idx in extra_sliders:
            elements.append(extra_sliders[idx])
        if idx in extra_chains:
            elements.append(extra_chains[idx])
        if idx in extra_recalls:
            elements.append(extra_recalls[idx])

        slide["elements"] = elements
        slide["interactiveElements"] = elements

    return slides
