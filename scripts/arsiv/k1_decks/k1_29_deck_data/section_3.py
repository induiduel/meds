# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 3: Gen Amplifikasyonu, Delesyonlar ve Sitogenetik Belirteçler (Slayt 21 - 30)
Checkpoint: Slayt 29
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_3_slides():
    return [
        # Slayt 21
        {
            "slideNumber": 21,
            "title": "Gen Amplifikasyonu İlkeleri",
            "content": (
                "Gen amplifikasyonu, genomun belirli bir DNA bölgesinin kopyalanma hataları sonucu sayısız defa "
                "artması ve o lokustaki gen kopya sayısının onlarca veya yüzlerce kata fırlaması olayıdır. "
                "Bu mekanizma kural olarak protoonkogenleri hedefler ve onkoproteinin hücrede aşırı düzeyde "
                "birikmesine yol açarak malign transformasyonu körükler. Amplifiye olan genin nükleotid dizisinde "
                "bir anormallik bulunmaz; protein tamamen normal yapıda üretilir ancak hücre başına düşen protein "
                "miktarı fizyolojik sınırları muazzam ölçüde aşar. Tümör sitogenetiğinde amplifiye DNA parçaları "
                "iki temel morfolojik formda tespit edilir: Ekstrakromozomal küçük halkasal parçacıklar olan "
                "**çift dakikalar (double minutes)** ve kromozomun kendi içine entegre olmuş **homojen boyanan "
                "bölgeler (homogeneously staining regions - HSR)**."
            ),
            "elements": [
                make_cloze(
                    "Gen amplifikasyonu sonucunda onkoprotein dizisinde mutasyon olmaksızın sadece kopya sayısı artar.",
                    "kopya",
                    "Genetik materyal adedi artışı"
                ),
                make_table(
                    "Gen Amplifikasyonunun Temel Biyolojik Özellikleri",
                    ["Parametre", "Biyolojik Karşılık", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Etkilenen Gen Sınıfı", "Protoonkogenler", "Malign proliferasyonu pompalayan onkoprotein aşırılığı"],
                            "hiddenIndex": 1,
                            "hint": "Büyümeyi hızlandıran genler"
                        },
                        {
                            "cells": ["Protein Yapısı", "Normal (Vahşi tip/Wild-type)", "Normal proteinin sayıca yüzlerce kat fazla üretilmesi"],
                            "hiddenIndex": 1,
                            "hint": "Dizi mutasyonu taşımayan yapı"
                        }
                    ]
                )
            ]
        },

        # Slayt 22
        {
            "slideNumber": 22,
            "title": "Sitogenetik Belirteçler: Çift Dakikalar (Double Minutes)",
            "content": (
                "**Çift dakikalar (double minutes - dmin)**, gen amplifikasyonunun en karakteristik sitogenetik "
                "tezahürlerinden biridir. Karyotip analizinde veya floresan in situ hibridizasyonda (FISH) metafaz "
                "plaklarında kromozomların dışında, sitoplazmada dağınık duran çok küçük, çiftler halinde yuvarlak "
                "kromatin parçacıkları olarak izlenirler. Bu yapılar **ekstrakromozomal (kromozom dışı)** olup "
                "dairesel DNA halkalarından oluşur. En kritik biyolojik özellikleri, bir **sentromere sahip "
                "olmamalarıdır**. Sentromerleri bulunmadığı için hücre bölünmesi (mitoz) sırasında iğ ipliklerine "
                "bağlanamazlar ve yavru hücrelere eşit bölünmezler (asimetrik dağılım). Bu durum, tümör klonu "
                "içerisinde bazı hücrelerin yüzlerce kopya onkogen biriktirmesine ve hızla büyümesine yol açar."
            ),
            "elements": [
                make_table(
                    "Çift Dakikaların (dmin) Biyolojik Karakteristiği",
                    ["Yapısal Özellik", "Moleküler Detay", "Hücresel Sonuç"],
                    [
                        {
                            "cells": ["Kromozom Konumu", "Ekstrakromozomal (Kromozom dışı serbest dairesel DNA)", "Metafazda kromozomlardan bağımsız saçılma"],
                            "hiddenIndex": 1,
                            "hint": "Hücre çekirdeğinde bağımsız halkacıklar"
                        },
                        {
                            "cells": ["Sentromer Varlığı", "Sentromersiz yapı", "Mitozda iğ ipliklerine tutunamama ve asimetrik yavru dağılımı"],
                            "hiddenIndex": 1,
                            "hint": "Kinetokor ve tutunma bölgesi yokluğu"
                        }
                    ]
                ),
                make_active_recall(
                    "Tümör sitogenetiğinde sentromeri bulunmayan, metafaz plağında serbest halkasal çiftler halinde görülen ekstrakromozomal DNA parçacıklarına ne ad verilir?",
                    "Çift dakikalar (Double minutes - dmin) adı verilir.",
                    "İkili mikroskobik kromatin tanecikleri"
                )
            ]
        },

        # Slayt 23
        {
            "slideNumber": 23,
            "title": "Sitogenetik Belirteçler: Homojen Boyanan Bölgeler (HSR)",
            "content": (
                "Gen amplifikasyonunun ikinci ana sitogenetik formu **Homojen Boyanan Bölgelerdir (Homogeneously "
                "Staining Regions - HSR)**. Çift dakikaların aksine HSR yapıları, amplifiye olan DNA dizilerinin "
                "tekrar tekrar bir araya gelerek bir konak kromozomun içine kovalent olarak entegre olmasıyla "
                "oluşur. G-bantlama sitogenetik analizinde normal kromozomlar açık ve koyu bant desenleri sergilerken, "
                "amplifiye bölge tekdüze, soluk ve desensiz bir bant alanı olarak boyanır; 'homojen boyanan bölge' "
                "ismi buradan gelir. HSR segmentleri kromozom yapısına katıldıkları için **sentromerik kontrole "
                "tabidirler**; bu sayede mitoz bölünme sırasında yavru hücrelere kararlı ve eşit biçimde aktarılırlar. "
                "Genellikle çift dakikalar evrimsel süreçte kromozoma entegre olarak HSR segmentlerine dönüşürler."
            ),
            "elements": [
                make_before_after(
                    "Çift Dakikalar (dmin) ile Homojen Boyanan Bölgelerin (HSR) Karşılaştırması",
                    "Çift Dakikalar (Double Minutes)",
                    "Sentromersiz, ekstrakromozomal serbest halkasal DNA. Mitozda iğ ipliğine bağlanamaz, yavru hücrelere asimetrik dağılır.",
                    "Homojen Boyanan Bölgeler (HSR)",
                    "Kromozoma entegre lineer segment. Sentromere bağlıdır, mitozda her iki yavru hücreye eşit ve kararlı aktarılır.",
                    "Her iki form da onkogenin hücrede yüzlerce kat amplifiye olmasının sitogenetik kanıtıdır."
                ),
                make_cloze(
                    "Amplifiye DNA dizilerinin bir kromozoma entegre olup tekdüze desensiz boyandığı segmentlere homojen boyanan bölgeler (HSR) denir.",
                    "homojen",
                    "Tekdüze bant paterni"
                )
            ]
        },

        # Slayt 24
        {
            "slideNumber": 24,
            "title": "Pediatrik Nöroblastom ve MYCN Amplifikasyonu",
            "content": (
                "Gen amplifikasyonunun prognoz ve klinik evre ile en kusursuz korelasyon gösterdiği pediyatrik "
                "tümör **Nöroblastomdur**. Sempatik zincir veya adrenal medulla nöroendokrin hücrelerinden köken "
                "alan nöroblastom, çocukluk çağının en sık ekstrakraniyal solid tümörüdür. Normalde 2. kromozomun "
                "kısa kolunda (2p24) tek kopya halinde bulunan **MYCN (N-myc) protoonkogeni**, agresif olgularda "
                "çift dakikalar veya HSR şeklinde 100-300 kopyaya kadar amplifiye olur. Tümör dokusunda FISH ile "
                "MYCN amplifikasyonunun saptanması, hastanın yaşından veya tümörün evresinden bağımsız olarak "
                "**son derece kötü bir prognozun**, hızlı progresyonun ve kemoterapi direncinin en güçlü göstergesidir. "
                "Bu olgular derhal yüksek riskli grupta sınıflandırılarak yoğun tedavi protokollerine alınır."
            ),
            "elements": [
                make_causal_chain(
                    "Nöroblastomda MYCN Amplifikasyonu ve Agresif Klinik Seyir Kaskadı",
                    [
                        "1. 2p24 Lokus Replikasyon Hatası: Nöroblastik kök hücrede MYCN geni kontrolsüz yeniden replike edilir.",
                        "2. Çift Dakikalar / HSR Birikimi: Hücre nükleusunda onlarca ekstrakromozomal halka ve geniş HSR bantları türer.",
                        "3. N-Myc Aşırı Üretimi: Nükleer transkripsiyon faktörü hücresel farklılaşmayı durdurup blastik bölünmeyi körükler.",
                        "4. İmmün Kaçış ve Metastaz: Agresif nöroblastom klonları hızla kemik iliğine, kortikal kemiğe ve karaciğere yayılır.",
                        "5. Kötü Prognoz ve Direnç: Standart kemoterapiye direnç gelişir; yoğun multiajan tedavi protokolü zorunlu hale gelir."
                    ]
                ),
                make_active_recall(
                    "Pediyatrik nöroblastom hastalarında saptandığında evreden bağımsız en güçlü kötü prognoz göstergesi olan amplifiye onkogen hangisidir?",
                    "MYCN (N-myc) protoonkogenidir.",
                    "İkinci kromozom nöral onkogeni"
                )
            ]
        },

        # Slayt 25
        {
            "slideNumber": 25,
            "title": "Meme ve Mide Karsinomlarında HER2 / ERBB2",
            "content": (
                "**HER2 (İnsan Epidermal Büyüme Faktörü Reseptörü 2)** veya **ERBB2**, 17. kromozomda (17q12) "
                "kodlanan ve tirozin kinaz aktivitesine sahip transmembranöz bir büyüme faktörü reseptörüdür. İnvaziv "
                "meme karsinomlarının yaklaşık %15-20'sinde ve mide/gastroözofageal bileşke adenokarsinomlarının "
                "önemli bir kısmında HER2 geninde yüksek düzeyli amplifikasyon saptanır. Bu durum hücre zarında "
                "milyonlarca HER2 reseptörünün birikmesine (aşırı ekspresyon) yol açar; reseptörler ligand olmadan "
                "da kendi kendilerine homodimerleşerek hücreye sürekli mitojenik sinyal pompalar. HER2 amplifiye "
                "tümörler tarihsel olarak son derece agresif seyrederken; günümüzde HER2'nin hücre dışı alanını "
                "hedefleyen monoklonal antikor **Trastuzumab (Herceptin)** sayesinde hastaların sağkalım oranları "
                "dramatik biçimde yükselmiştir."
            ),
            "elements": [
                make_table(
                    "HER2 / ERBB2 Onkogen Amplifikasyonu Özellikleri",
                    ["Özellik", "Moleküler / Patolojik Karşılık", "Klinik Tedavi"],
                    [
                        {
                            "cells": ["Kromozomal Konum", "17q12 lokusu", "ERBB2 reseptör geni kopya patlaması"],
                            "hiddenIndex": 1,
                            "hint": "Onyedi numaralı kromozom kolu"
                        },
                        {
                            "cells": ["Tanısal Yöntem", "İmmünohistokimya (3+) ve FISH", "Gen kopya sayısının ve membranöz proteinin teyidi"],
                            "hiddenIndex": 1,
                            "hint": "Boyama ve floresan mikroskopi"
                        },
                        {
                            "cells": ["Hedefe Yönelik İlaç", "Trastuzumab (Anti-HER2 antikoru)", "Ligandsız dimerizasyonu bloke ederek sağkalımı uzatma"],
                            "hiddenIndex": 1,
                            "hint": "Meme hedefe yönelik monoklonal ajanı"
                        }
                    ]
                ),
                make_cloze(
                    "HER2 gen amplifikasyonu saptanan meme ve mide kanserlerinde reseptörün ekstraselüler alanını bloke eden monoklonal antikor Trastuzumab ilacıdır.",
                    "Trastuzumab",
                    "Hedefe yönelik monoklonal meme antikoru"
                )
            ]
        },

        # Slayt 26
        {
            "slideNumber": 26,
            "title": "Kromozomal Delesyonlar ve Heterozigotluk Kaybı",
            "content": (
                "Kromozomal delesyonlar, bir kromozom segmentinin kırılarak kaybolmasıdır. Amplifikasyonların "
                "aksine delesyonlar protoonkogenleri değil, **tümör baskılayıcı genleri (TSG)** devre dışı bırakır. "
                "Bir tümör baskılayıcı genin bulunduğu lokustaki delesyon, o genin bir alelinin fiziksel olarak "
                "yok olması anlamına gelir. Kalıtsal bir kanser sendromunda birey zaten birinci darbeyi germline "
                "olarak mutasyonlu taşırken; hedef hücrede sağlam ikinci alelin delesyonla yitirilmesi olgusuna "
                "**Heterozigotluk Kaybı (Loss of Heterozygosity - LOH)** denir. LOH, katı solid tümörlerde tümör "
                "baskılayıcı genlerin inaktive olmasındaki en yaygın ikinci vuruş mekanizmasıdır. Sitogenetik "
                "incelemelerde delesyonlar mikrosatellit belirteç kaybı veya komparatif genomik hibridizasyon (CGH) "
                "ile haritalandırılır."
            ),
            "elements": [
                make_before_after(
                    "Heterozigot Doku vs Heterozigotluk Kaybı (LOH)",
                    "Sağlam Heterozigot Hücre (+ / -)",
                    "Bir mutant alel ve bir sağlam alel bulunur. Sağlam alel yeterli miktarda baskılayıcı protein üreterek hücreyi tümörleşmeden korur.",
                    "LOH Gelişmiş Neoplastik Hücre (- / 0)",
                    "Sağlam alel delesyonla tamamen kaybolur. Hücrede fonksiyonel fren proteini kalmaz ve malign proliferasyon başlar.",
                    "LOH analizi solid tümörlerde tümör baskılayıcı gen inaktivasyonunu saptayan altın standarttır."
                ),
                make_cloze(
                    "Sağlam tümör baskılayıcı alelin delesyon veya somatik mutasyonla silinmesi olayına heterozigotluk kaybı (LOH) denir.",
                    "heterozigotluk",
                    "İkili alel farklılığının yitimi"
                )
            ]
        },

        # Slayt 27
        {
            "slideNumber": 27,
            "title": "Retinoblastomda 13q14 Delesyonu ve RB1 Kaybı",
            "content": (
                "Delesyon mekanizması ile tümör baskılayıcı kaybının klasik tarihi modeli **13q14 delesyonudur**. "
                "13. kromozomun uzun kolunda yer alan **RB1 geni**, hücre döngüsünün G1-S kontrol noktasında nöbet "
                "tutan prototipik kapı bekçisidir. Retinoblastom hastalarının sitogenetik analizinde 13q14 bölgesinde "
                "mikrodelesyonlar saptanmıştır. Ailesel formda birey birinci mutant RB1 alelini tüm hücrelerinde "
                "taşırken, retina hücrelerinde 13q14 bölgesindeki sağlam alelin somatik delesyonu (LOH) retinoblastom "
                "gelişimiyle sonuçlanır. Bu hastalarda yalnızca çocuklukta göz içi retinoblastom riski değil; "
                "ilerleyen ergenlik ve erişkinlik döneminde kemik dokusunda primer mezenkimal malignite olan "
                "**osteosarkom ve yumuşak doku sarkomu** gelişme riski de yüzlerce kat artmıştır."
            ),
            "elements": [
                make_table(
                    "13q14 Delesyonu ve RB1 Fonksiyonel Yitimi",
                    ["Genetik Parametre", "Patolojik Karşılık", "Klinik Sonuç"],
                    [
                        {
                            "cells": ["Kromozomal Bölge", "13q14 lokusu delesyonu", "RB1 tümör baskılayıcı geninin homozigot kaybı"],
                            "hiddenIndex": 1,
                            "hint": "On üç numaralı kromozom bandı"
                        },
                        {
                            "cells": ["Hücresel Mekanizma", "E2F faktörünün sınırsız serbest kalması", "Hücrenin kontrolsüzce S fazına girmesi"],
                            "hiddenIndex": 1,
                            "hint": "Transkripsiyon baskısının kalkması"
                        },
                        {
                            "cells": ["İkinci Malignite Riski", "Osteosarkom ve yumuşak doku sarkomları", "Genç erişkinlikte kemik karsinogenezi"],
                            "hiddenIndex": 1,
                            "hint": "Malign mezenkimal kemik neoplazmı"
                        }
                    ]
                ),
                make_active_recall(
                    "Retinoblastom ve osteosarkom patogenezinde kritik olan RB1 tümör baskılayıcı geninin yerleşik olduğu kromozomal lokus neresidir?",
                    "13. kromozomun uzun kolundaki 13q14 lokusudur.",
                    "On üç numaralı kromozom bölgesi"
                )
            ]
        },

        # Slayt 28
        {
            "slideNumber": 28,
            "title": "Anöploidi ve Kromozomal Kararsızlık (CIN)",
            "content": (
                "İnsan somatik hücreleri normalde 46 kromozom (2n diploid) içerir. **Anöploidi**, hücrenin haploid "
                "sayının (n=23) tam katı olmayan anormal sayıda kromozom taşıması durumudur (örneğin 47, 53 veya "
                "72 kromozom). İnsan kanserlerinin, özellikle solid karsinomların %85'inden fazlasında belirgin "
                "anöploidi ve **Kromozomal Kararsızlık (Chromosomal Instability - CIN)** mevcuttur. Anöploidi; mitoz "
                "sırasında kardeş kromatidlerin kinetokorlara bağlanmasını denetleyen **iğ ipliği kontrol noktası "
                "(spindle assembly checkpoint - SAC)** proteinlerindeki (MAD2, BUB1) kusurlar ve sentrozom "
                "hiperamplifikasyonu sonucu ortaya çıkar. Anöploid hücrelerde kromozom sayısı dengesizliği, onkogenlerin "
                "dozajını artırırken tümör baskılayıcı genlerin kaybını kolaylaştırarak neoplastik agresifliği fırlatır."
            ),
            "elements": [
                make_before_after(
                    "Diploid Sağlıklı Genom vs Kanser Anöploidisi",
                    "Normal Diploid Hücre (2n = 46)",
                    "Kusursuz mitoz kontrolü, simetrik iki kutuplu iğ iplikleri ve kromatidlerin hatasız eşit ayrılması.",
                    "Anöploid Kanser Hücresi (CIN Fenotipi)",
                    "Sentrozom amplifikasyonu, çok kutuplu (tripolar) mitozlar, ayrılmama (nondisjunction) ve kaotik kromozom sayıları.",
                    "Anöploidi kanser hücresine mutasyonel esneklik ve tedavi direnci sağlayan majör itici güçtür."
                ),
                make_micro_quiz(
                    "Katı karsinomların büyük kısmında saptanan, kromozom sayısının haploid sayının tam katı olmaması durumuna ve yapısal/sayısal dengesizliğe ne ad verilir?",
                    [
                        {
                            "key": "A",
                            "text": "Öploidi",
                            "isCorrect": False,
                            "explanation": "Öploidi haploid sayının tam katı olan normal kromozom takımıdır."
                        },
                        {
                            "key": "B",
                            "text": "Anöploidi (Kromozomal İnstabilite)",
                            "isCorrect": True,
                            "explanation": "Anöploidi haploid sayının katı olmayan kromozom düzensizliğidir ve karsinomların %85'inde görülür."
                        },
                        {
                            "key": "C",
                            "text": "Dengeli resiprokal translokasyon",
                            "isCorrect": False,
                            "explanation": "Dengeli translokasyonda genetik materyal kaybı veya kromozom sayısı değişimi olmaz."
                        },
                        {
                            "key": "D",
                            "text": "Mikrosatellit stabilitesi",
                            "isCorrect": False,
                            "explanation": "Mikrosatellit stabilitesi nükleotid düzeyindeki eşleşme durumudur, kromozom sayısıyla ilişkisizdir."
                        }
                    ],
                    "Anöploidi kromozom ayrılma kusurlarından kaynaklanan sayısal genom dengesizliğidir."
                )
            ]
        },

        # Slayt 29: CHECKPOINT 3
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Gen Amplifikasyonu ve Kromozomal Delesyonlar",
            "content": (
                "Üçüncü bölümün bu tekrar sayfasında, onkogen aşırı ekspresyonu ve tümör baskılayıcı inaktivasyonuna "
                "yol açan sitogenetik anomaliler özetlenmektedir. Gen amplifikasyonu onkogen kopya sayısını fırlatır; "
                "sitogenetikte sentromersiz ekstrakromozomal çift dakikalar (dmin) veya kromozoma entegre homojen "
                "boyanan bölgeler (HSR) halinde görülür. Nöroblastomda MYCN amplifikasyonu evreden bağımsız en "
                "güçlü kötü prognoz kriteridir. Meme ve midede HER2/ERBB2 amplifikasyonu agresif seyri simgeler "
                "ancak Trastuzumab ile hedeflenir. Kromozomal delesyonlar ise heterozigotluk kaybı (LOH) ile tümör "
                "baskılayıcıları yok eder; 13q14 delesyonu retinoblastom ve osteosarkoma öncülük eder. Anöploidi "
                "mitoz ayrılma kusurları sonucu gelişen sayısal kaostur."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp03-fc01",
                    "front": "Tümör sitogenetiğinde sentromeri bulunmayan, metafaz plağında serbest halkasal çiftler halinde izlenen amplifiye DNA parçacıklarına ne ad verilir?",
                    "back": "Çift dakikalar (Double minutes - dmin) adı verilir.",
                    "hint": "İkili serbest kromatin tanecikleri"
                },
                {
                    "id": "k1-29-cp03-fc02",
                    "front": "Pediyatrik nöroblastomda saptandığında evreden bağımsız en kötü prognozu gösteren amplifiye onkogen hangisidir?",
                    "back": "MYCN (N-myc) onkogenidir.",
                    "hint": "İkinci kromozom nöroendokrin transkripsiyon geni"
                },
                {
                    "id": "k1-29-cp03-fc03",
                    "front": "Retinoblastom ve osteosarkom gelişiminde rol oynayan RB1 geninin silinmesine yol açan karakteristik kromozomal delesyon bölgesi neresidir?",
                    "back": "13q14 lokusudur.",
                    "hint": "On üç numaralı kromozom uzun kol bandı"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 3 Özet Tablosu: Amplifikasyon ve Delesyon Modelleri",
                    ["Genetik Lezyon", "Karakteristik Örnek", "Klinik Onkolojik Sonuç"],
                    [
                        {
                            "cells": ["Onkogen Amplifikasyonu", "MYCN (Nöroblastom) ve HER2 (Meme Ca)", "Kötü prognoz ve hedefe yönelik antikor duyarlılığı"],
                            "hiddenIndex": 1,
                            "hint": "Kopya sayısı fırlayan iki onkogen"
                        },
                        {
                            "cells": ["Kromozomal Delesyon (LOH)", "13q14 Elesyonu (RB1 geni)", "Retinoblastom ve ikincil osteosarkom riski"],
                            "hiddenIndex": 1,
                            "hint": "Göz küresi tümörü delesyon odağı"
                        }
                    ]
                )
            ]
        },

        # Slayt 30
        {
            "slideNumber": 30,
            "title": "Klinik Karar: Nöroblastom ve Meme Kanserinde FISH Değerlendirmesi",
            "content": (
                "Moleküler patoloji laboratuvarında Floresan İn Situ Hibridizasyon (FISH) yöntemi, spesifik gen "
                "amplifikasyonlarını ve delesyonları hücre nükleusunda doğrudan sayısallaştıran altın standarttır. "
                "Yeni tanı konmuş 18 aylık bir nöroblastom hastasında tümör dokusunda MYCN gen kopyalarının "
                "santromer 2 probuna oranının (MYCN/CEP2) 4'ün üzerinde olması veya >10 kopya bulunması 'MYCN "
                "amplifiye' olarak raporlanır ve hastayı en yoğun kemoterapi protokolüne sevk eder. Meme karsinomunda "
                "ise immünohistokimya ile şüpheli (+2) bulunan olgularda HER2/CEP17 oranının >2.0 olması HER2 "
                "amplifikasyonunu kesinleştirerek hastaya Trastuzumab başlanmasının yolunu açar."
            ),
            "elements": [
                make_branching_logic(
                    "14 aylık erkek çocukta batında dev retroperitoneal kitle saptanıyor; biyopside nöroblastom tanısı konuyor. Tümör evresi lokalize (Evre 2) olarak değerlendiriliyor ancak moleküler patoloji raporunda FISH analiziyle tümör nükleuslarında çift dakikalar (dmin) şeklinde 80 kopya MYCN amplifikasyonu saptanıyor.",
                    "Bu moleküler rapor karşısında onkoloji konseyinin hastanın prognozu ve tedavisi hakkındaki en doğru klinik kararı ne olmalıdır?",
                    [
                        {
                            "text": "Evre erken olsa dahi MYCN amplifikasyonu hastayı otomatikman yüksek riskli gruba sokar; agresif kemoterapi ve kemik iliği nakli planlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Nöroblastomda MYCN amplifikasyonu evreden bağımsız olarak son derece agresif gidişatı simgeler ve yüksek risk protokolü gerektirir."
                        },
                        {
                            "text": "Evre 2 erken olduğundan moleküler sonuç dikkate alınmamalı ve hasta yalnızca cerrahi eksizyonla izlenmelidir.",
                            "isCorrect": False,
                            "explanation": "MYCN amplifiye nöroblastomlar lokalize dahi olsa cerrahiyle iyileşmez, hızla sistemik nüks eder."
                        },
                        {
                            "text": "Çift dakikalar sentromer içerdiği için tümörün iyi diferansiye ganglionöroma dönüştüğü kabul edilmelidir.",
                            "isCorrect": False,
                            "explanation": "Çift dakikalar sentromersiz olup habis karsinogenezin göstergesidir."
                        }
                    ]
                ),
                make_micro_quiz(
                    "İnvaziv duktal meme karsinomunda hedefe yönelik Trastuzumab tedavisi planlanmadan önce tümör dokusunda amplifikasyonu doğrulanması gereken onkogen hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "HER2 / ERBB2",
                            "isCorrect": True,
                            "explanation": "Trastuzumab HER2 amplifikasyonu taşıyan meme karsinomlarında ekstraselüler reseptör alanını bloke eden hedefe yönelik ilaçtır."
                        },
                        {
                            "key": "B",
                            "text": "MYCN",
                            "isCorrect": False,
                            "explanation": "MYCN nöroblastomda amplifiye olan onkogendir."
                        },
                        {
                            "key": "C",
                            "text": "RB1",
                            "isCorrect": False,
                            "explanation": "RB1 bir onkogen değil, tümör baskılayıcı gendir."
                        },
                        {
                            "key": "D",
                            "text": "BCL2",
                            "isCorrect": False,
                            "explanation": "BCL2 foliküler lenfomada translokasyona uğrar."
                        }
                    ],
                    "Meme karsinomunda hedefe yönelik antikor tedavisi HER2 amplifikasyonuna dayanır."
                )
            ]
        }
    ]
