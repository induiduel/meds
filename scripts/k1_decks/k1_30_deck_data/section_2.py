# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 30: İleri Tümör Genetiği ve Metabolizması
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 2: RB Yolunu Bozan Mekanizmalar ve CDK İnhibitörleri (Slayt 11 - 20)
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
            "title": "CDKN2A Lokusu ve Biyolojik Karmaşıklığı",
            "content": (
                "Kromozom 9p21 bandında yer alan CDKN2A lokusu, insan genomundaki en olağanüstü tümör baskılayıcı "
                "bölgelerden biridir. Alternatif okuma çerçeveleri (alternative reading frames) kullanarak tamamen "
                "farklı aminoasit dizilerine ve biyolojik işlevlere sahip iki ayrı tümör baskılayıcı proteini "
                "kodlar: **p16/INK4a** ve **p14/ARF**. p16 proteini CDK4 ve CDK6 kinazlarını bloke ederek RB "
                "yolağını aktif (hipofosforile) tutarken; p14/ARF proteini MDM2 ubiquitin ligazını inhibe ederek "
                "p53'ü kararlı kılar. Dolayısıyla CDKN2A lokusunun tek bir homozigot delesyonu, hücrenin hem RB "
                "hem de p53 tümör baskılayıcı kalkanlarını aynı anda düşürmesine neden olur."
            ),
            "elements": [
                make_table(
                    "CDKN2A Lokusunun Kodladığı İki Kritik Protein",
                    ["Protein Adı", "Hedeflediği Molekül", "Regüle Ettiği Yolak", "Fonksiyonel Sonuç"],
                    [
                        {
                            "cells": ["p16 (INK4a)", "CDK4 ve CDK6 kinazları", "RB Yolağı", "RB hipofosforilasyonu ve G1/S durması"],
                            "hiddenIndex": 1,
                            "hint": "Dördüncü ve altıncı siklin bağımlı kinazlar"
                        },
                        {
                            "cells": ["p14 (ARF)", "MDM2 ubiquitin ligazı", "p53 Yolağı", "p53 degradasyonunun önlenmesi ve apoptoz"],
                            "hiddenIndex": 1,
                            "hint": "p53'ü parçalanmaya yönlendiren temel enzim"
                        }
                    ]
                )
            ]
        },

        # Slayt 12
        {
            "slideNumber": 12,
            "title": "p16 (CDKN2A) Kaybı Görülen Tümörler",
            "content": (
                "p16 inaktivasyonu insan neoplazmlarında TP53 mutasyonlarından sonra en sık rastlanan ikinci "
                "genetik sapmadır. Pankreas duktal adenokarsinomlarının %75'inden fazlasında, malign melanomların "
                "(özellikle ailesel displastik nevüs sendromu), glioblastomların, özofagus karsinomlarının ve "
                "mesane karsinomlarının önemli bir kısmında CDKN2A homozigot delesyonu veya promoter CpG ada "
                "hipermetilasyonu saptanır. p16'sını kaybeden neoplastik klonlar, hücre dışı büyüme engellerine ve "
                "kontakt inhibisyona karşı tamamen duyarsızlaşarak kesintisiz bir replikatif hıza kavuşurlar."
            ),
            "elements": [
                make_cloze(
                    "Pankreas duktal adenokarsinomlarında p16 geni vakaların yüzde yetmiş beşinden fazlasında inaktive olur.",
                    "p16",
                    "CDKN2A lokusundan kodlanan CDK4 inhibitörü"
                ),
                make_active_recall(
                    "Ailesel melanom ve displastik nevüs sendromunda en sık mutasyona uğrayan germline tümör baskılayıcı lokus hangisidir?",
                    "Kromozom 9p21'de yer alan CDKN2A (p16/INK4a) lokusudur.",
                    "Melanosit proliferasyonunu denetleyen CDK inhibitör gen lokusu"
                )
            ]
        },

        # Slayt 13
        {
            "slideNumber": 13,
            "title": "Siklin D1 (CCND1) Deregülasyonu ve Onkogenez",
            "content": (
                "Siklin D1 proteini, mitojenik sinyallerin nükleer hedefe aktarılmasında birincil hız kısıtlayıcı "
                "faktördür. Fizyolojik şartlarda hücre S fazına girdikten sonra Siklin D1 hızla yıkılır. Ancak "
                "neoplastik hücrelerde CCND1 geni gen amplifikasyonu veya kromozomal translokasyon ile sürekli "
                "açık tutulabilir. Mantle hücreli lenfomada t(11;14)(q13;q32) translokasyonu sonucu CCND1 geni "
                "immünoglobulin ağır zincir (IgH) promotoru altına taşınır ve masif Siklin D1 üretimi gerçekleşir. "
                "Meme karsinomlarının ise yaklaşık %15-20'sinde CCND1 gen amplifikasyonu saptanır."
            ),
            "elements": [
                make_table(
                    "Siklin D1 Deregülasyonu ile Karakterize Maligniteler",
                    ["Malignite Tipi", "Genetik Değişiklik", "Etki Mekanizması"],
                    [
                        {
                            "cells": ["Mantle Hücreli Lenfoma", "t(11;14)(q13;q32) translokasyonu", "IgH promotoru altında aşırı Siklin D1 transkripsiyonu"],
                            "hiddenIndex": 1,
                            "hint": "On birinci ve on dördüncü kromozomlar arası parça değişimi"
                        },
                        {
                            "cells": ["İnvaziv Meme Karsinomu", "Kromozom 11q13 CCND1 amplifikasyonu", "Kopya sayısı artışı ile CDK4 hiperaktivasyonu"],
                            "hiddenIndex": 1,
                            "hint": "Gen dizisinin katlanarak artması"
                        }
                    ]
                )
            ]
        },

        # Slayt 14
        {
            "slideNumber": 14,
            "title": "CDK4 ve CDK6 Kinazlarının Onkojenik Rolü",
            "content": (
                "CDK4 ve CDK6, Siklin D izoformları ile birleşerek RB'yi fosforilleyen katalitik kinaz "
                "alt birimleridir. CDK4 geninde meydana gelen spesifik nokta mutasyonları (örneğin p16'nın bağlanma "
                "cebini bozan R24C mutasyonu), kinazın p16 inhibitörüne karşı tamamen dirençli hale gelmesine "
                "neden olur. İnhibitör bağlanamadığı için CDK4 kontrolsüz olarak aktif kalır ve hücreyi sürekli "
                "bölünmeye zorlar. Glioblastom ve liposarkomlarda ise CDK4 gen amplifikasyonu sıklıkla MDM2 "
                "amplifikasyonu ile birlikte (aynı 12q14-15 amplikonunda) eş zamanlı olarak bulunur."
            ),
            "elements": [
                make_cloze(
                    "Liposarkom ve glioblastomlarda CDK4 geni sıklıkla MDM2 geni ile aynı amplikonda aşırı kopyalanır.",
                    "CDK4",
                    "Siklin D ile birleşen serin treonin kinaz"
                ),
                make_active_recall(
                    "CDK4'ün p16 inhibitörüne bağlanmasını engelleyerek melanom gelişimine yol açan mutasyonel mekanizma nedir?",
                    "CDK4'ün inhibitör bağlanma cebindeki nokta mutasyonu (ör. R24C) sonucu p16 direncidir.",
                    "Kinaz üzerindeki allosterik bağlanma cebinin şekil değiştirmesi"
                )
            ]
        },

        # Slayt 15
        {
            "slideNumber": 15,
            "title": "Hedefe Yönelik Tedavi: CDK4/6 İnhibitörleri",
            "content": (
                "RB yolağının neoplastik proliferasyondaki kritik rolü, modern onkolojide devrim yaratan yeni bir "
                "hedefe yönelik ilaç sınıfının doğmasını sağlamıştır: **CDK4/6 inhibitörleri** (palbosiklib, "
                "ribosiklib, abemasiklib). Bu küçük moleküller CDK4 ve CDK6 kinazlarının ATP bağlanma ceplerini "
                "seçici olarak bloke eder. Sonuç olarak RB'nin hiperfosforilasyonu engellenir, RB hipofosforile "
                "aktif formunda kilitlenir ve E2F serbest kalamaz. Bu ilaçlar günümüzde özellikle hormon reseptörü "
                "pozitif (HR+), HER2 negatif metastatik meme karsinomlarında birinci basamak standart tedavidir."
            ),
            "elements": [
                make_before_after(
                    "CDK4/6 İnhibitörü Öncesi ve Sonrası Tümör Hücresi Dinamiği",
                    "CDK4/6 İnhibisyonu Öncesi (Aktif Tümör Büyümesi)",
                    "Aşırı Siklin D-CDK4/6 aktivitesi RB'yi sürekli hiperfosforile eder; serbest E2F kontrolsüz S fazı replikasyonu sağlar.",
                    "CDK4/6 İnhibitörü Tedavisi Sonrası (G1 Arresti)",
                    "İlaç CDK4/6'yı kilitler; RB hipofosforile kalarak E2F'yi hapseder ve tümör hücresi G1 fazında kalıcı olarak durur.",
                    "Meme kanserinde progresyonsuz sağkalımı iki katından fazla artıran temel moleküler etki mekanizmasıdır."
                )
            ]
        },

        # Slayt 16
        {
            "slideNumber": 16,
            "title": "DNA Tümör Virüslerinin RB Saldırı Stratejisi",
            "content": (
                "Yalnızca HPV değil, insan ve hayvanlarda neoplazi yapabilen diğer DNA tümör virüsleri de "
                "konak hücresini replikasyona zorlamak için benzer moleküler taktikler geliştirmiştir. "
                "Adenovirüsün **E1A proteini** ve Simian Virüs 40'ın (SV40) **büyük T antijeni (large T)**, "
                "tıpkı HPV E7 gibi hipofosforile RB'nin E2F bağlayan cebine kenetlenir. Bu viral onkoproteinlerin "
                "tamamı RB ile E2F arasındaki bağı koparır. Konak hücresi viral DNA'yı kopyalamak üzere mecburen "
                "S fazına sokulur. Bu mekanizma virüslerin replikatif başarısı ile onkogenez arasındaki doğrudan bağı gösterir."
            ),
            "elements": [
                make_table(
                    "RB Proteinini İnaktive Eden Viral Onkoproteinler",
                    ["DNA Virüsü", "Viral Onkoprotein", "Konak Hücredeki Hedefi", "Yol Açtığı Patoloji"],
                    [
                        {
                            "cells": ["İnsan Papilloma Virüsü (HPV)", "E7 onkoproteini", "Hipofosforile RB'den E2F'yi ayırır", "Serviks ve orofarenks karsinomları"],
                            "hiddenIndex": 1,
                            "hint": "HPV'nin küçük nükleer tümör proteini"
                        },
                        {
                            "cells": ["Adenovirüs", "E1A proteini", "RB cebine bağlanarak E2F'yi serbestleştirir", "Kemirgenlerde deneysel tümörler"],
                            "hiddenIndex": 1,
                            "hint": "Adenovirüs erken eksprese edilen transkripsiyon proteini"
                        },
                        {
                            "cells": ["SV40 (Poliomavirüs)", "Büyük T antijeni (Large T)", "RB ve p53'ü aynı anda bağlar", "Deneysel sarkom ve mezotelyoma"],
                            "hiddenIndex": 1,
                            "hint": "Simian virüsünün büyük antijen proteini"
                        }
                    ]
                )
            ]
        },

        # Slayt 17
        {
            "slideNumber": 17,
            "title": "Küçük Hücreli Akciğer Karsinomunda RB Kaybı",
            "content": (
                "RB gen inaktivasyonunun neredeyse %100 oranında görüldüğü en agresif insan epitelyal neoplazmı "
                "**küçük hücreli akciğer karsinomudur (KHAK)**. Nöroendokrin diferansiyasyon gösteren bu tümörde, "
                "bialelik RB1 delesyonu veya mutasyonu vakaların %95-100'ünde saptanır ve eş zamanlı TP53 "
                "mutasyonu da kuraldır. RB freninin tamamen yokluğu, tümörün mikroskop altında gözlenen aşırı "
                "yüksek mitotik indeksini, ezilme artefaktını ve belirgin nükleer kalıplanmasını (molding) açıklar. "
                "Bu tümörlerde RB eksikliği nedeniyle CDK4/6 inhibitörleri tamamen etkisizdir."
            ),
            "elements": [
                make_cloze(
                    "Küçük hücreli akciğer karsinomunda RB1 gen inaktivasyonu vakaların neredeyse tamamında tespit edilir.",
                    "RB1",
                    "Retinoblastoma tümör baskılayıcı geni"
                ),
                make_active_recall(
                    "RB mutasyonu taşıyan küçük hücreli akciğer karsinomlarında CDK4/6 inhibitörlerinin (palbosiklib vb.) etkisiz olmasının moleküler gerekçesi nedir?",
                    "İlacın hedefi olan downstream RB proteini zaten mevcut olmadığından hücre döngüsü durdurulamaz.",
                    "İnhibitörün fren yapacağı proteinin hücrede tamamen bulunmaması durumu"
                )
            ]
        },

        # Slayt 18
        {
            "slideNumber": 18,
            "title": "Mesane ve Osteosarkomda RB Yolunun Önemi",
            "content": (
                "RB yolağı, yüksek dereceli invaziv üretelyal mesane karsinomları ile kemiğin osteosarkomlarında da "
                "kritik prognostik belirteçtir. İnvaziv mesane kanserlerinin yaklaşık yarısında RB mutasyonu veya "
                "p16 delesyonu mevcuttur; bu sapma derin kas tabakası (muskularis界面) invazyonu ile doğrudan ilişkilidir. "
                "Osteosarkomlarda ise RB kaybı, TP53 mutasyonuyla birlikte kompleks karyotip ve kromotripsis "
                "(kromozomların paramparça olup rastgele birleşmesi) fenotipinin gelişmesine zemin hazırlar. "
                "Bu olgularda genomik instabilite hızı katlanarak artar."
            ),
            "elements": [
                make_micro_quiz(
                    "Aşağıdaki malign neoplazmlardan hangisinde bialelik RB inaktivasyonu patogenezde neredeyse evrensel (%95-100) bir zorunluluktur?",
                    [
                        {
                            "text": "Küçük hücreli akciğer karsinomu (KHAK)",
                            "isCorrect": True,
                            "explanation": "Küçük hücreli akciğer karsinomunda RB1 mutasyonu ve p53 inaktivasyonu hemen hemen tüm olgularda mevcuttur."
                        },
                        {
                            "text": "Papiller tiroid karsinomu",
                            "isCorrect": False,
                            "explanation": "Papiller tiroid karsinonunda BRAF mutasyonları veya RET translokasyonları baskındır."
                        },
                        {
                            "text": "Seminom (testis germ hücreli tümörü)",
                            "isCorrect": False,
                            "explanation": "Seminomlarda izokromozom 12p baskındır, primer bialelik RB mutasyonu tipik değildir."
                        },
                        {
                            "text": "Mide taşlı yüzük hücreli karsinomu",
                            "isCorrect": False,
                            "explanation": "Diffüz mide karsinomunda temel moleküler sapma CDH1 (E-kaderin) inaktivasyonudur."
                        }
                    ],
                    "KHAK nöroendokrin diferansiyasyon ve neredeyse %100 RB kaybı ile seyreder."
                )
            ]
        },

        # Slayt 19: CHECKPOINT 2
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] RB Yolu Bozuklukları ve CDK İnhibitörleri",
            "content": (
                "Bu kontrol noktasında RB yolağını devre dışı bırakan moleküler mekanizmaları ve hedefe yönelik "
                "tedavi stratejilerini özetliyoruz:\n\n"
                "• **CDKN2A Lokusu:** 9p21'de yer alır. Alternatif okuma çerçeveleriyle p16/INK4a (CDK4 inhibitörü) ve p14/ARF (MDM2 inhibitörü, p53 koruyucusu) üretir.\n"
                "• **p16 Kaybı:** Pankreas karsinomlarının %75'inde, ailesel melanomda ve glioblastomda sıktır.\n"
                "• **Siklin D1 Aşırı Ekspresyonu:** Mantle hücreli lenfomada t(11;14) translokasyonu ve meme kanserinde amplifikasyon ile oluşur.\n"
                "• **CDK4/6 İnhibitörleri:** Palbosiklib, ribosiklib, abemasiklib; RB'yi hipofosforile tutup E2F'yi hapsederek G1 durması sağlar.\n"
                "• **Viral İnaktivasyon:** HPV E7, Adenovirüs E1A ve SV40 Büyük T antijeni hipofosforile RB'ye bağlanıp E2F'yi salar.\n"
                "• **KHAK:** Küçük hücreli akciğer karsinomunda RB kaybı neredeyse %100 kuraldır."
            ),
            "flashcards": [
                {
                    "id": "k1-30-fc04",
                    "front": "Kromozom 9p21 bandındaki CDKN2A lokusundan alternatif okuma çerçevesiyle üretilen iki temel tümör baskılayıcı protein hangileridir?",
                    "back": "p16 (INK4a) ve p14 (ARF) proteinleridir.",
                    "hint": "Biri CDK4'ü diğeri MDM2'yi denetleyen iki sayısal protein"
                },
                {
                    "id": "k1-30-fc05",
                    "front": "Mantle hücreli lenfomada Siklin D1 geninin immünoglobulin ağır zincir promotoru altına taşınmasına yol açan translokasyon nedir?",
                    "back": "t(11;14)(q13;q32) translokasyonudur.",
                    "hint": "On birinci ve on dördüncü kromozomlar arası sitogenetik yer değişimi"
                },
                {
                    "id": "k1-30-fc06",
                    "front": "Meme karsinomunda kullanılan palbosiklib ve ribosiklib gibi CDK4/6 inhibitörlerinin tümör hücresindeki moleküler etki mekanizması nedir?",
                    "back": "RB'nin hipofosforile kalarak E2F'yi hapsetmesini sağlamaktır.",
                    "hint": "Retinoblastoma proteinini aktif baskılayıcı formda kilitleme durumu"
                }
            ],
            "elements": [
                make_active_recall(
                    "Adenovirüs E1A, SV40 büyük T ve HPV E7 onkoproteinlerinin konak hücredeki ortak moleküler hedefi nedir?",
                    "Hipofosforile RB proteinine bağlanarak E2F transkripsiyon faktörünü serbestleştirmektir.",
                    "Hücre döngüsünün G1/S kapı bekçisi proteini"
                )
            ]
        },

        # Slayt 20
        {
            "slideNumber": 20,
            "title": "RB Yolağında Karşılıklı Dışlayıcılık (Mutual Exclusivity)",
            "content": (
                "Moleküler onkolojinin en zarif ilkelerinden biri olan 'karşılıklı dışlayıcılık', bir biyolojik "
                "yolağın tek bir kritik halkasının kırılmasının neoplastik fenotip için kafi olduğunu savunur. "
                "Örneğin RB geni mutasyonla inaktive olmuş bir retinoblastom veya küçük hücreli akciğer "
                "karsinomu hücresinde p16 geninin susturulmasına veya Siklin D1 amplifikasyonuna hiçbir zaman "
                "ihtiyaç duyulmaz; çünkü fren zaten kökten sökülmüştür. Tersine, p16'sını homozigot delesyonla "
                "kaybetmiş bir pankreas kanserinde RB geni daima sağlamdır. Bu moleküler kural hedefe yönelik "
                "tedavi seçiminde rehberlik eder."
            ),
            "elements": [
                make_cloze(
                    "Bir karsinom hücresinde RB geni inaktive ise p16 delesyonu veya Siklin D amplifikasyonu karşılıklı dışlayıcılık prensibi gereği görülmez.",
                    "karşılıklı dışlayıcılık",
                    "Aynı yolaktaki mutasyonların tek bir tümörde eş zamanlı seçilmemesi durumu"
                ),
                make_active_recall(
                    "RB geni inaktive olan tümörlerde neden ek olarak p16 delesyonu veya Siklin D1 amplifikasyonu gelişmez?",
                    "Karşılıklı dışlayıcılık prensibi gereği RB yokken upstream regülatörleri mutasyona uğratmak ek seçici avantaj sağlamaz.",
                    "Aynı biyolojik yolda zaten kopmuş olan zincire ikinci darbenin gereksizliği"
                )
            ]
        }
    ]
