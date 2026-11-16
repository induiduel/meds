# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 30: İleri Tümör Genetiği ve Metabolizması
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 1: Retinoblastoma Proteini (RB) ve G1/S Kontrol Noktası (Slayt 1 - 10)
Checkpoint: Slayt 9
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_1_slides():
    return [
        # Slayt 1
        {
            "slideNumber": 1,
            "title": "İleri Tümör Genetiğine Giriş ve Hücre Döngüsü Frenleri",
            "content": (
                "Hücre döngüsünün kusursuz ilerlemesi, mitojenik uyarıların tetiklediği siklin-bağımlı kinazlar "
                "ile genom bütünlüğünü koruyan tümör baskılayıcı genlerin oluşturduğu hassas dengeye bağlıdır. "
                "Kanser gelişiminde bu dengenin bozulması, özellikle hücrenin bölünmeye geri dönüşümsüz olarak "
                "karar verdiği G1/S kontrol noktasındaki denetim mekanizmalarının çökmesiyle başlar. Bu kontrol "
                "noktasının en kritik kapı bekçisi retinoblastoma (RB) proteinidir. RB yolu insan kanserlerinin "
                "neredeyse tamamında doğrudan mutasyonlarla veya bu yolu kontrol eden regülatör proteinlerin "
                "sapmalarıyla devre dışı bırakılmaktadır. Tümör baskılayıcı genlerin keşfi ve moleküler onkolojinin "
                "temelleri bu prototipik genin incelenmesiyle anlaşılmıştır."
            ),
            "elements": [
                make_cloze(
                    "Hücre döngüsünün bölünmeye adandığı en kritik denetim noktası G1/S kontrol kapısıdır.",
                    "G1/S",
                    "Hücre döngüsünün sentez öncesi kritik geçiş fazı"
                ),
                make_active_recall(
                    "İnsan neoplazmlarında hücre döngüsünün en sık bozulan ve neredeyse evrensel olarak devre dışı kalan kontrol noktası hangisidir?",
                    "G1/S kontrol noktası (kısıtlama / restriction noktası) olarak bilinir.",
                    "DNA replikasyonuna başlamadan önceki moleküler karar eşiği"
                )
            ]
        },

        # Slayt 2
        {
            "slideNumber": 2,
            "title": "Retinoblastoma Proteini (RB) ve Moleküler Keşfi",
            "content": (
                "Retinoblastoma (RB) geni, kromozom 13q14 lokusunda yer alan ve moleküler tıpta keşfedilen ilk "
                "tümör baskılayıcı gen olma özelliğini taşıyan temel düzenleyicidir. RB geni tarafından kodlanan "
                "nükleer fosfoprotein, hücre döngüsünün G1 fazından S fazına geçişini negatif yönde denetler. "
                "RB'nin kaybı ilk olarak çocukluk çağının nadir bir retina malignitesi olan retinoblastomda "
                "tanımlanmış olsa da, günümüzde osteosarkom, meme, küçük hücreli akciğer karsinomu ve mesane "
                "kanserleri gibi çok çeşitli erişkin epitelyal ve mezenkimal malignitelerinde de RB inaktivasyonu "
                "belgelenmiştir. Bu proteinin yokluğu hücreyi mitojenik faktörlerden bağımsız çoğalmaya iter."
            ),
            "elements": [
                make_table(
                    "RB Geni Temel Genetik ve Patolojik Özellikleri",
                    ["Özellik", "Moleküler Tanım", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Kromozomal Lokus", "Kromozom 13q14 bandı", "Sitogenetik delesyonlarda retinoblastom riski"],
                            "hiddenIndex": 1,
                            "hint": "Onüçüncü kromozomun uzun kolu bölgesi"
                        },
                        {
                            "cells": ["Gen Sınıfı", "Tümör baskılayıcı gen", "Hücresel düzeyde resesif işlev kaybı"],
                            "hiddenIndex": 1,
                            "hint": "Kanser gelişimini engelleyen gen ailesi"
                        },
                        {
                            "cells": ["İkincil Malignite", "Osteosarkom ve yumuşak doku sarkomu", "Kalıtsal olgularda ileri yaş riski"],
                            "hiddenIndex": 1,
                            "hint": "Kemik kaynaklı primer malign neoplazm"
                        }
                    ]
                )
            ]
        },

        # Slayt 3
        {
            "slideNumber": 3,
            "title": "RB'nin Biyokimyasal Çalışma Mekanizması",
            "content": (
                "RB proteini hücre döngüsünü fosforilasyon durumuna göre dinamik olarak yöneten bir moleküler "
                "şalter gibi çalışır. G0 ve erken G1 evresinde RB proteini **hipofosforile (aktif)** durumdadır. "
                "Bu aktif formunda E2F transkripsiyon faktörleri ailesine sıkıca bağlanarak onları hapseder. "
                "Aynı zamanda histon deasetilaz (HDAC) ve histon metiltransferaz enzimlerini promotor bölgelere "
                "çekerek kromatini kapalı konumda tutar; böylece S fazına geçiş için şart olan genlerin "
                "(siklin E, DNA polimeraz) transkripsiyonunu tamamen susturur. Hücre bu sayede istirahat halinde "
                "kalır ve gereksiz bölünmeler mutlak olarak engellenir."
            ),
            "elements": [
                make_cloze(
                    "Hipofosforile durumdaki RB proteini E2F transkripsiyon faktörlerini bağlayarak transkripsiyonu susturur.",
                    "E2F",
                    "S fazı genlerini aktive eden temel düzenleyici protein"
                ),
                make_active_recall(
                    "RB proteininin hücre döngüsünü durduran ve E2F'yi bloke eden biyolojik olarak aktif formu hangisidir?",
                    "Hipofosforile (az fosforillenmiş veya defosforile) RB formudur.",
                    "Fosfat yükü düşük olan moleküler konfigürasyon"
                )
            ]
        },

        # Slayt 4
        {
            "slideNumber": 4,
            "title": "RB Hiperfosforilasyonu ve G1/S Eşiğinin Aşılması",
            "content": (
                "Hücre dışı büyüme faktörleri (EGF, PDGF) hücre yüzeyindeki reseptörleri uyardığında, intrasellüler "
                "sinyal kaskadları Siklin D sentezini patlatır. Siklin D, partner kinazları olan CDK4 ve CDK6 ile "
                "kompleks oluşturarak RB proteinini ilk basamakta fosforiller. Ardından aktive olan Siklin E-CDK2 "
                "kompleksi RB'yi **hiperfosforile (inaktif)** hale getirir. Hiperfosforilasyon RB'nin konformasyonunu "
                "değiştirerek E2F'yi serbest bırakmasına neden olur. Serbest kalan E2F nükleusta Siklin E ve DNA "
                "sentez enzimlerini transkribe eder ve hücre geri dönüşümsüz olarak S fazına fırlar."
            ),
            "elements": [
                make_causal_chain(
                    "Büyüme Sinyalinden G1/S Geçişine RB Kaskadı",
                    [
                        "1. Sinyal İletimi: Büyüme faktörleri hücre yüzeyinde Siklin D sentezini tetikler.",
                        "2. İlk Fosforilasyon: Siklin D-CDK4/6 kompleksi hipofosforile RB'ye fosfat grupları ekler.",
                        "3. İkincil Dalga: Siklin E-CDK2 kompleksi RB'yi hiperfosforile ederek tam inaktivasyona uğratır.",
                        "4. E2F Serbestleşmesi: Konformasyonu bozulan RB, hapsedilmiş E2F transkripsiyon faktörünü salar.",
                        "5. S Fazı Başlangıcı: Serbest E2F replikasyon genlerini ateşleyerek DNA sentezini başlatır."
                    ]
                )
            ]
        },

        # Slayt 5
        {
            "slideNumber": 5,
            "title": "Knudson'ın İki Vuruş (Two-Hit) Hipotezi",
            "content": (
                "Alfred Knudson, retinoblastom epidemiyolojisini matematiksel olarak modellerken tümör baskılayıcı "
                "genlerin temel kalıtım kuralı olan 'iki vuruş' hipotezini ortaya koymuştur. Bu modele göre "
                "retinal hücrelerin malign transformasyonu için RB geninin her iki alelinin de işlevsiz hale "
                "gelmesi zorunludur. Hipotez, kanser yatkınlığının ailesel olarak otozomal dominant bir özellikle "
                "aktarılmasına rağmen, hücresel düzeyde karsinogenezin resesif bir fenomen olduğunu ve ancak her "
                "iki kopyanın inaktivasyonu ile fenotipin ortaya çıktığını mükemmel şekilde izah eder."
            ),
            "elements": [
                make_table(
                    "Ailesel ve Sporadik Retinoblastom Karşılaştırması",
                    ["Ölçüt", "Ailesel Retinoblastom", "Sporadik Retinoblastom"],
                    [
                        {
                            "cells": ["İlk Vuruş (1. Darbe)", "Germline mutant alel (tüm hücrelerde mevcut)", "Somatik mutasyon (tek bir retinal hücrede)"],
                            "hiddenIndex": 1,
                            "hint": "Ebeveynden aktarılan gametik genetik hasar"
                        },
                        {
                            "cells": ["İkinci Vuruş (2. Darbe)", "Retina hücresinde somatik mutasyon", "Aynı hücrede ikinci bağımsız somatik mutasyon"],
                            "hiddenIndex": 1,
                            "hint": "Doğum sonrası hedef dokuda kazanılan lokal hasar"
                        },
                        {
                            "cells": ["Tümör Dağılımı", "Bilateral ve multifokal tutulum sıktır", "Unilateral ve unifokal tutulum kuraldır"],
                            "hiddenIndex": 1,
                            "hint": "İki gözün birden etkilenmesi durumu"
                        },
                        {
                            "cells": ["Başlangıç Yaşı", "Erken bebeklik dönemi (ortalama ilk yaş)", "Daha ileri çocukluk dönemi (2-4 yaş)"],
                            "hiddenIndex": 1,
                            "hint": "Hayatın ilk aylarında erken klinik bulgu"
                        }
                    ]
                )
            ]
        },

        # Slayt 6
        {
            "slideNumber": 6,
            "title": "Ailesel Retinoblastomda Sekonder Neoplazmlar",
            "content": (
                "Ailesel retinoblastomlu çocuklarda vücudun trilyonlarca somatik hücresinin tamamı ilk darbeyi "
                "(tek kopyası inaktif RB alelini) taşımaktadır. Bu nedenle gözdeki retinoblastom cerrahi veya "
                "radyoterapiyle tamamen tedavi edilse dahi, birey hayat boyu diğer dokularda gelişebilecek yeni "
                "kanserler açısından aşırı yüksek risk altındadır. Bu hastaların ergenlik ve genç erişkinlik "
                "döneminde özellikle **osteosarkom**, yumuşak doku sarkomları, melanom ve meme karsinomu "
                "geliştirme olasılıkları yüzlerce kat artmıştır. Radyoterapi uygulanması bu riski katlamaktadır."
            ),
            "elements": [
                make_cloze(
                    "Ailesel retinoblastom tanılı çocuklarda ileri yaşlarda en sık gelişen mezenkimal malignite osteosarkom olarak kaydedilir.",
                    "osteosarkom",
                    "Primer malign kemik tümörü"
                ),
                make_active_recall(
                    "Kalıtsal RB mutasyonu taşıyan olgularda göz dışı organlarda en sık görülen ve radyoterapi ile insidansı artan sekonder malign tümör hangisidir?",
                    "Osteosarkom (malign kemik tümörü) ve yumuşak doku sarkomlarıdır.",
                    "Kemik matriksi üreten agresif mezenkimal karsinom dışı tümör"
                )
            ]
        },

        # Slayt 7
        {
            "slideNumber": 7,
            "title": "RB Yolağının İntrasellüler Regülatörleri: CDK İnhibitörleri",
            "content": (
                "Fizyolojik şartlarda RB'nin hiperfosforilasyonu serbest bırakılmaz; hücre içi büyüme inhibitörleri "
                "bu kinazları sıkı bir baskı altında tutar. Siklin bağımlı kinaz inhibitörleri (CKI) iki ana aileye "
                "ayrılır: INK4 ailesi (p16/INK4A, p15, p18, p19) ve CIP/KIP ailesi (p21, p27, p57). Özellikle "
                "**p16 (CDKN2A)** spesifik olarak CDK4 ve CDK6 kinazlarına bağlanarak onların Siklin D ile "
                "birleşmesini engeller. Böylece RB'nin fosforillenmesini önler ve hücreyi G1 evresinde kilitler. "
                "p16 kaybı, RB geni sağlam olsa bile RB'nin sürekli hiperfosforile kalmasına yol açar."
            ),
            "elements": [
                make_table(
                    "CDK İnhibitör Aileleri ve RB Yolağı İlişkisi",
                    ["İnhibitör Ailesi", "Prototip Protein", "Etki Mekanizması", "RB Üzerindeki Net Etki"],
                    [
                        {
                            "cells": ["INK4 Ailesi", "p16 (CDKN2A)", "Spesifik olarak CDK4 ve CDK6'yı bloke eder", "RB'nin hipofosforile (aktif) kalmasını sağlar"],
                            "hiddenIndex": 1,
                            "hint": "On altıncı kilodaltonluk klasik tümör baskılayıcı"
                        },
                        {
                            "cells": ["CIP/KIP Ailesi", "p21 (CDKN1A)", "Tüm siklin-CDK komplekslerini geniş spektrumda inhibe eder", "G1/S ve G2/M durmasını tetikler"],
                            "hiddenIndex": 1,
                            "hint": "p53 transkripsiyonu ile indüklenen yirmi bir kilodaltonluk inhibitör"
                        }
                    ]
                )
            ]
        },

        # Slayt 8
        {
            "slideNumber": 8,
            "title": "Onkojenik Virüsler ve RB İnaktivasyonu: HPV E7",
            "content": (
                "Tümör baskılayıcı RB proteininin devre dışı kalması yalnız intrinsik genetik mutasyonlarla değil, "
                "onkojenik DNA virüslerinin ürettiği viral onkoproteinlerle de gerçekleşebilir. Yüksek riskli "
                "İnsan Papilloma Virüsleri (HPV tip 16 ve 18) tarafından sentezlenen **E7 onkoproteini**, konak "
                "hücresindeki hipofosforile RB'ye yüksek afiniteyle bağlanır. E7, RB ile E2F arasındaki bağı fiziksel "
                "olarak kopararak E2F'nin ortama kontrolsüz salınmasını sağlar. Aynı zamanda p21 ve p27'yi de bloke "
                "ederek büyüme faktörü gereksinimi olmaksızın hücreyi doğrudan mitoza sürükler."
            ),
            "elements": [
                make_cloze(
                    "Yüksek riskli HPV tiplerinin ürettiği E7 viral proteini doğrudan hipofosforile RB'ye bağlanıp E2F'yi serbest bırakır.",
                    "E7",
                    "HPV'nin RB'yi hedef alan küçük viral onkoproteini"
                ),
                make_micro_quiz(
                    "Yüksek riskli HPV (tip 16 ve 18) enfeksiyonunda E7 onkoproteininin karsinogenezi tetikleyen birincil moleküler hedefi hangisidir?",
                    [
                        {
                            "text": "Hipofosforile RB'ye bağlanarak E2F transkripsiyon faktörünü serbest bırakmak",
                            "isCorrect": True,
                            "explanation": "E7 proteini RB'yi fonksiyonel olarak inaktive eder ve E2F'yi salarak hücre döngüsünü tetikler."
                        },
                        {
                            "text": "Mitokondri membranında sitokrom c salınımını doğrudan başlatmak",
                            "isCorrect": False,
                            "explanation": "Bu pro-apoptotik bir etkidir; oysa viral enfeksiyon hücre sağkalımını artırır."
                        },
                        {
                            "text": "Hücre zarındaki EGF reseptörlerini endositozla parçalamak",
                            "isCorrect": False,
                            "explanation": "E7 nükleer döngü proteinleriyle etkileşir, yüzey reseptörlerini yıkmaz."
                        },
                        {
                            "text": "Yalnızca telomeraz enziminin promotorunu metilleyerek susturmak",
                            "isCorrect": False,
                            "explanation": "HPV telomerazı susturmaz, aksine karsinom hücrelerinde immortalizasyonu destekler."
                        }
                    ],
                    "HPV E7 proteini hipofosforile RB'yi hedef alırken, E6 proteini p53'ü parçalar."
                )
            ]
        },

        # Slayt 9: CHECKPOINT 1
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Retinoblastoma Proteini (RB) ve G1/S Kontrolü",
            "content": (
                "Bu kontrol noktasında RB tümör baskılayıcı geninin moleküler biyolojisini ve Knudson'ın iki "
                "vuruş hipotezini özetliyoruz:\n\n"
                "• **RB Geni ve Lokusu:** Kromozom 13q14 bandında yer alır; keşfedilen ilk tümör baskılayıcı gendir.\n"
                "• **Hipofosforile Form:** Aktiftir; E2F transkripsiyon faktörlerini bağlayarak hücre döngüsünü G1'de kilitler.\n"
                "• **Hiperfosforile Form:** İnaktiftir; Siklin D-CDK4/6 ve Siklin E-CDK2 etkisiyle fosforillenir, E2F serbest kalır.\n"
                "• **Knudson Hipotezi:** Ailesel olgularda 1. darbe germline, 2. darbe somatiktir (bilateral, erken). Sporadikte her iki darbe aynı hücrede somatiktir (unilateral, geç).\n"
                "• **Klinik Risk:** Kalıtsal RB mutasyonu taşıyanlarda ileri yaşta osteosarkom riski çok yüksektir.\n"
                "• **Viral Onkogenez:** HPV E7 proteini hipofosforile RB'ye bağlanıp E2F'yi serbest bırakır."
            ),
            "flashcards": [
                {
                    "id": "k1-30-fc01",
                    "front": "RB proteininin biyolojik olarak aktif olup E2F transkripsiyon faktörünü hapsederek hücre döngüsünü durduran formu hangisidir?",
                    "back": "Hipofosforile formudur.",
                    "hint": "Üzerinde az sayıda fosfat grubu taşıyan moleküler durum"
                },
                {
                    "id": "k1-30-fc02",
                    "front": "Knudson'ın çift darbe hipotezine göre ailesel retinoblastomda birinci darbe genetik olarak hangi hücre hattında yer alır?",
                    "back": "Germ hattında (germline) yer alır.",
                    "hint": "Ebeveynden döllenmeyle aktarılan gametik hücre kökeni"
                },
                {
                    "id": "k1-30-fc03",
                    "front": "Ailesel retinoblastomlu çocuklarda göz tümörü tedavi edilse dahi ergenlikte gelişme riski en yüksek olan sekonder mezenkimal malignite nedir?",
                    "back": "Osteosarkomdur.",
                    "hint": "Malign kemik dokusu üreten primer iskelet tümörü"
                }
            ],
            "elements": [
                make_active_recall(
                    "RB yolunu bozan viral onkoprotein hangisidir ve hangi mekanizmayla etki gösterir?",
                    "HPV E7 onkoproteinidir; hipofosforile RB'ye bağlanarak E2F'yi serbest bırakır.",
                    "Serviks karsinomu etkeni virüsün nükleer proteini"
                )
            ]
        },

        # Slayt 10
        {
            "slideNumber": 10,
            "title": "RB Yolağının Evrensel Kanser Hipotezi",
            "content": (
                "Modern moleküler patoloji verileri, insan kanserlerinin istisnasız tamamına yakınında G1/S "
                "kontrol noktasının devre dışı bırakıldığını göstermektedir. Bu kontrol noktasının çökmesi dört "
                "ana moleküler kapıdan biriyle gerçekleştirilir: (1) RB geninin doğrudan mutasyonel inaktivasyonu, "
                "(2) CDK4 geninin aktive edici mutasyonu veya amplifikasyonu, (3) Siklin D geninin amplifikasyonu "
                "veya aşırı ekspresyonu, (4) p16 (CDKN2A) geninin delesyonu veya promoter hipermetilasyonu ile "
                "susturulması. Bu dört olay birbirini dışlar (mutually exclusive); yani bir tümörde bu kapılardan "
                "biri kırıldığında hücre döngüsü freni tamamen kalktığı için diğer mutasyonlara gerek kalmaz."
            ),
            "elements": [
                make_table(
                    "G1/S Kontrol Kapısını Kıran Dört Temel Sapma",
                    ["Bileşen", "Sapmanın Doğası", "Etkilenen Kanser Örnekleri"],
                    [
                        {
                            "cells": ["RB Geni", "İşlev kaybı delesyon veya nokta mutasyonu", "Retinoblastom, osteosarkom, küçük hücreli akciğer karsinomu"],
                            "hiddenIndex": 1,
                            "hint": "Protein aktivitesinin ortadan kalkması durumu"
                        },
                        {
                            "cells": ["p16 (CDKN2A)", "Homozigot delesyon veya promoter hipermetilasyonu", "Pankreas adenokarsinomu, melanom, glioblastom"],
                            "hiddenIndex": 1,
                            "hint": "İki kopyanın birden kromozomdan silinmesi hali"
                        },
                        {
                            "cells": ["Siklin D1 (CCND1)", "Gen amplifikasyonu veya translokasyon", "Meme karsinomu, mantle hücreli lenfoma"],
                            "hiddenIndex": 1,
                            "hint": "Gen kopya sayısının anormal çoğalması"
                        },
                        {
                            "cells": ["CDK4", "Aktive edici nokta mutasyonu veya amplifikasyon", "Glioblastom, sarkomlar, melanom"],
                            "hiddenIndex": 1,
                            "hint": "Kinazın frenlenemez şekilde sürekli çalışması"
                        }
                    ]
                )
            ]
        }
    ]
