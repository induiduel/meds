# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 3: Benign Tümör Terminolojisi ve Adlandırma (Slayt 21 - 30)
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
            "title": "Tümör Adlandırma Kuralları ve Parankimal Temel",
            "content": (
                "Tümörlerin sınıflandırılması ve adlandırılması (nomenklatür), rastgele klinik yakıştırmalara değil, "
                "patolojinin uluslararası kabul görmüş histogenetik kurallarına dayanır. Bir neoplazmın adı, kitlenin "
                "biyolojik davranışını (benign veya malign) ve parankimal hücrelerinin hangi embriyolojik/histolojik dokudan "
                "köken aldığını yansıtacak şekilde kurgulanır. Adlandırmanın yegane temeli parankimdir; stroma ne kadar zengin "
                "veya vasküler olursa olsun tümörün temel ismini değiştirmez. Temel kural olarak mezenkimal dokudan köken "
                "alan benign tümörlerin sonuna köken hücre tipinin ardına '-oma' eki getirilirken, epitelyal tümörlerde "
                "adlandırma hem hücresel kökene hem de mikroskobik mimari paterne (glandüler, papiller, kistik) göre yapılır."
            ),
            "elements": [
                make_cloze(
                    "Tümör adlandırmasında temel alınan ve tümörün histogenetik kökenini belirleyen hücresel bileşen parankimdir.",
                    "parankimdir",
                    "Transforme hücre topluluğu"
                ),
                make_active_recall(
                    "Mezenkimal kaynaklı benign tümörlerin adlandırılmasında köken alınan doku adının sonuna getirilen standart ek nedir?",
                    "'-oma' sonekidir.",
                    "İyi huylu mezenkimal takı"
                )
            ]
        },
        # Slayt 22
        {
            "slideNumber": 22,
            "title": "Mezenkimal Benign Tümörler: Kök Hücre ve '-oma' Kuralı",
            "content": (
                "Mezenkimal dokular; embriyolojik mezodermden köken alan fibröz bağ dokusu, yağ dokusu, kıkırdak, kemik, "
                "kan damarları ve kas dokularını kapsar. Mezenkimal kökenli benign bir neoplazmı adlandırmak için köken hücre "
                "tipinin Latince/Grekçe adına '-oma' eki eklenir: Fibröz dokudan köken alan benign tümöre 'fibrom', matür yağ "
                "dokusundan köken alana 'lipom', kıkırdak dokusundan köken alana 'kondrom', kemik dokusundan köken alana ise "
                "'osteom' adı verilir. Lipomlar insan vücudunda en sık saptanan benign yumuşak doku tümörleri olup subkutan "
                "yerleşimli, yumuşak, hareketli ve olgun yağ lobüllerinden oluşan kapsüllü kitlelerdir."
            ),
            "elements": [
                make_table(
                    "Mezenkimal Doku Kökenli Benign Tümörlerin Adlandırılması",
                    ["Köken Doku", "Benign Tümör Adı", "Karakteristik Histolojik Hücre"],
                    [
                        {
                            "cells": ["Fibröz Bağ Dokusu", "Fibrom", "Olgun fibroblastlar ve bol kolajen lifler"],
                            "hiddenIndex": 1,
                            "hint": "Bağ dokusu iyi huylu tümörü"
                        },
                        {
                            "cells": ["Yağ Dokusu", "Lipom", "Tek vakuollü olgun adipositler"],
                            "hiddenIndex": 1,
                            "hint": "En yaygın yumuşak doku kütlesi"
                        },
                        {
                            "cells": ["Kıkırdak Dokusu", "Kondrom", "Lakünler içinde olgun kondrositler"],
                            "hiddenIndex": 1,
                            "hint": "Kıkırdak iyi huylu tümörü"
                        },
                        {
                            "cells": ["Kemik Dokusu", "Osteom", "Lameller kemik trabekülleri ve osteositler"],
                            "hiddenIndex": 1,
                            "hint": "Kemik kaynaklı benign neoplazm"
                        }
                    ]
                ),
                make_cloze(
                    "İnsan yumuşak dokularında en sık rastlanan benign mezenkimal neoplazm olgun yağ hücrelerinden oluşan lipom kitlesidir.",
                    "lipom",
                    "Adiposit kaynaklı iyi huylu ur"
                )
            ]
        },
        # Slayt 23
        {
            "slideNumber": 23,
            "title": "Kas Dokusu Neoplazmları: Rabdomyom ve Leiomyom",
            "content": (
                "Kas dokusu tümörlerinin adlandırılması, kasın çizgili veya düz kas olmasına göre kesin kurallara tabidir. "
                "Çizgili (iskelet) kasından köken alan benign neoplazma 'rabdomyom' (rhabdomyoma) adı verilir; çizgili kas "
                "hücrelerinin diferansiyasyonunu taklit eden bu tümörler oldukça nadir olup en sık çocukluk çağında kalp "
                "kası içinde (tüberoz skleroz ile ilişkili kardiyak rabdomyom) veya baş-boyun bölgesinde saptanır. Düz kas "
                "dokusundan köken alan benign neoplazma ise 'leiomyom' (leiomyoma) adı verilir. Leiomyomlar özellikle kadınlarda "
                "uterus myometriumunda son derece yaygın olup halk arasında 'ur' veya 'myom' olarak bilinir; reprodüktif çağdaki "
                "kadınların dörtte birinde saptanırlar."
            ),
            "elements": [
                make_before_after(
                    "Çizgili Kas vs Düz Kas Benign Neoplazmları",
                    "Rabdomyom (Çizgili Kas)",
                    "İskelet kası diferansiasyonu, çapraz çizgilenme gösterebilen hücreler, nadirdir, kalpte tüberoz sklerozla birliktedir.",
                    "Leiomyom (Düz Kas)",
                    "Düz kas demetleri ve girdapsı patern, iğsi nükleuslar, son derece yaygındır, en sık uterus ve GİS'te görülür.",
                    "Sınavlarda 'rabdo'nun çizgili, 'leio'nun düz kas olduğunu ayırt etmek temel bilgidir."
                ),
                make_micro_quiz(
                    "İskelet (çizgili) kası diferansiyasyonu gösteren benign neoplazmın doğru patolojik adı hangisidir?",
                    [
                        {
                            "text": "Rabdomyom",
                            "isCorrect": True,
                            "explanation": "Doğrudur; 'rabdo-' çizgili kas kökünü simgeler ve rabdomyom benign çizgili kas tümörüdür."
                        },
                        {
                            "text": "Leiomyom",
                            "isCorrect": False,
                            "explanation": "Leiomyom düz kasın benign tümörüdür."
                        },
                        {
                            "text": "Rabdomyosarkom",
                            "isCorrect": False,
                            "explanation": "Rabdomyosarkom çizgili kasın kötü huylu (malign) kanseridir."
                        },
                        {
                            "text": "Kondrosarkom",
                            "isCorrect": False,
                            "explanation": "Kondrosarkom kıkırdağın malign tümörüdür."
                        }
                    ],
                    "Rabdomyom çizgili kasın iyi huylu tümörüdür."
                )
            ]
        },
        # Slayt 24
        {
            "slideNumber": 24,
            "title": "Epitelyal Benign Tümörler: Adenom Tanımı",
            "content": (
                "Epitelyal benign neoplazmların adlandırılması mezenkimal tümörlere göre daha karmaşık olup hem köken alınan "
                "hücreye hem de mikroskobik mimariye göre şekillenir. 'Adenom', iki temel durumu tanımlayan standart epitelyal "
                "terimdir: Birincisi, salgı bezlerinden (örneğin tiroid folliküler adenomu, böbrek tübüler adenomu, adrenal kortikal "
                "adenom) köken alan benign epitel tümörleridir. İkincisi ise bez yapısından köken almasa dahi, mikroskopik "
                "olarak tübüler veya glandüler (asiner) bez benzeri lümenler oluşturan her türlü benign epitel neoplazmıdır "
                "(örneğin kolonik tübüler adenomlar). Adenomlar genellikle hormon salgılama yeteneğine sahip olabilirler."
            ),
            "elements": [
                make_cloze(
                    "Glandüler bez yapıları oluşturan veya bez epiteli hücrelerinden köken alan benign neoplazma adenom adı verilir.",
                    "adenom",
                    "İyi huylu salgı bezi tümörü"
                ),
                make_active_recall(
                    "Endokrin bir organdan köken alan ve hormon salgılayabilen benign epitelyal tümörlere ne ad verilir?",
                    "Adenom adı verilir (örneğin hipofiz veya adrenal adenomu).",
                    "Glandüler iyi huylu epitelyal kitle"
                )
            ]
        },
        # Slayt 25
        {
            "slideNumber": 25,
            "title": "Papillomlar: Parmaksı Projeksiyonlar",
            "content": (
                "Epitelyal yüzeylerden lümene veya dışarıya doğru mikroskobik ya da makroskobik 'parmaksı' (frond-like), "
                "dallanmış ve siğilimsi çıkıntılar yaparak büyüyen benign epitel tümörlerine 'papillom' adı verilir. "
                "Bir papillomun histolojik temel çatısını, merkezde konakçı kökenli gevşek damarsal bir bağ dokusu ekseni "
                "(fibrovasküler kor) ve bu ekseni çepeçevre örten neoplastik epitel tabakası oluşturur. Papillomlar çok katlı "
                "yassı epitelde (deri veya larenks skuamöz papillomu), ürotelyumda (mesane ürotelyal papillomu) veya duktal "
                "epitelde (memenin meme başı akıntısı yapan intraduktal papillomu) sıkça izlenir; larengeal tipleri sıklıkla HPV ile ilişkilidir."
            ),
            "elements": [
                make_table(
                    "Papillom Türleri ve Anatomik Lokalizasyonları",
                    ["Papillom Türü", "Örtücü Epitel Tipi", "Klinik Özellik / Neden"],
                    [
                        {
                            "cells": ["Skuamöz Papillom (Larenks)", "Çok katlı yassı epitel", "HPV 6 ve 11 ilişkili, ses kısıklığı"],
                            "hiddenIndex": 2,
                            "hint": "Viral etiyoloji ve larenks tutulumu"
                        },
                        {
                            "cells": ["İntraduktal Papillom (Meme)", "Kübik duktal epitel", "Spontan kanlı meme başı akıntısı"],
                            "hiddenIndex": 2,
                            "hint": "Areola tepesinden serosözenöz sıvı"
                        },
                        {
                            "cells": ["Ürotelyal Papillom (Mesane)", "Değişici (transizyonel) epitel", "İnce parmaksı kitle, mikroskobik hematüri"],
                            "hiddenIndex": 1,
                            "hint": "Mesane iç örtü epiteli"
                        }
                    ]
                ),
                make_active_recall(
                    "Bir papillomun merkezinde yer alan ve epitel hücrelerini besleyen bağ dokusu eksenine ne ad verilir?",
                    "Fibrovasküler kor (veya bağ dokusu ekseni) adı verilir.",
                    "Damarlı santral mezenkimal eksen"
                )
            ]
        },
        # Slayt 26
        {
            "slideNumber": 26,
            "title": "Polip Kavramı: Tanım ve Klinik Anlam",
            "content": (
                "Patoloji ve klinik pratikte en sık kullanılan ancak en çok yanlış anlaşılan terimlerden biri 'polip'tir. "
                "Polip histolojik bir tanı değil, 'makroskobik veya klinik' bir tanımlamadır. Mukozal bir yüzeyden organ "
                "lümenine doğru parmak, mantar veya kubbe şeklinde çıkıntı (protrüzyon) yapan gözle görülür her türlü kitleye "
                "morfolojik olarak polip adı verilir. Tabanı ince bir sapla mukozaya bağlıysa 'saplı (pediküllü) polip', "
                "geniş bir tabanla doğrudan mukozaya oturuyorsa 'sapsız (sesil) polip' olarak tanımlanır. Polipler tamamen "
                "non-neoplastik inflamatuar/hiperplastik lezyonlar olabileceği gibi, benign adenomlar veya doğrudan erken "
                "malign karsinomlar da olabilirler."
            ),
            "elements": [
                make_before_after(
                    "Polip Terminolojisinin Ayırıcı Özelliği",
                    "Morfolojik Görünüm (Klinik Polip)",
                    "Lümene uzanan çıkıntı; tek başına bakıldığında kitlenin iyi huylu mu, iltihabi mi yoksa kanser mi olduğunu söyleyemez.",
                    "Histopatolojik İnceleme Sonucu",
                    "Biyopsi sonrası polipin bir inflamatuar psödopolip mi, premalign bir tübüler adenom mu yoksa invaziv karsinom mu olduğu kesinleşir.",
                    "Polip saptandığında kanser riskini belirlemek için daima eksizyonel biyopsi şarttır."
                ),
                make_cloze(
                    "Mukozal bir yüzeyden lümen içerisine doğru görünür biçimde kabaran kitlelere morfolojik olarak polip adı verilir.",
                    "polip",
                    "Gözle görülen lüminal çıkıntı"
                )
            ]
        },
        # Slayt 27
        {
            "slideNumber": 27,
            "title": "Kistadenomlar: Kistik Epitelyal Kitleler",
            "content": (
                "Kistadenom, neoplastik glandüler epitelin içi sıvı veya müsin dolu geniş kistik boşluklar oluşturduğu benign "
                "bir epitelyal neoplazmdır. En karakteristik ve en sık yerleşim yeri overlerdir (yumurtalıklar). Over "
                "yüzey epitelinden türeyen kistadenomlar salgıladıkları sıvının kimyasal doğasına göre iki ana sınıfa ayrılır: "
                "İnce, berrak su gibi sıvı içeren 'seröz kistadenom' ve koyu, yapışkan jelatinöz müsin içeren 'müsinöz kistadenom'. "
                "Müsinöz kistadenomlar kadın pelvisinde onlarca santimetreye ve kilolara ulaşabilen dev multikistik abdominal "
                "kitleler oluşturabilir. Eğer kistik boşlukların içine doğru parmaksı çıkıntılar uzanıyorsa lezyon 'papiller "
                "kistadenom' adını alır."
            ),
            "elements": [
                make_table(
                    "Over Kistadenomlarının Karşılaştırmalı Özellikleri",
                    ["Kistadenom Türü", "Kist Sıvısının Niteliği", "Epitel Morfolojisi", "Tipik Boyut"],
                    [
                        {
                            "cells": ["Seröz Kistadenom", "Berrak, sulu seröz sıvı", "Tuba uterina benzeri silyalı silindirik epitel", "Orta boyutlu (genellikle uniloküler)"],
                            "hiddenIndex": 1,
                            "hint": "Saydam ve akışkan kıvam"
                        },
                        {
                            "cells": ["Müsinöz Kistadenom", "Koyu, yapışkan, jelatinöz müsin", "Endoservikal/GİS benzeri müsinli epitel", "Dev boyutlar (multiloküler büyük kitleler)"],
                            "hiddenIndex": 1,
                            "hint": "Ağdalı sümüksü içerik"
                        }
                    ]
                ),
                make_active_recall(
                    "İçerisinde berrak su gibi veya koyu yapışkan müsin sıvısı bulunan benign kistik epitel tümörüne ne ad verilir?",
                    "Kistadenom adı verilir.",
                    "Kistik benign salgı bezi neoplazmı"
                )
            ]
        },
        # Slayt 28
        {
            "slideNumber": 28,
            "title": "Organa Özgü Benign Epitel Tümörleri",
            "content": (
                "Parenkimal solid organlarda görülen benign epitel neoplazmları genellikle o organın özgül epitelyal hücre "
                "adıyla anılır. Karaciğerde hepatositlerden köken alan ve genç kadınlarda oral kontraseptif (doğum kontrol hapı) "
                "kullanımı ile doğrudan tetiklenen benign tümöre 'hepatik adenom' (hepatoselüler adenom) denir; subkapsüler "
                "yerleştiğinde intraperitoneal rüptür ve ölümcül masif kanama riski taşır. Böbrek korteksinde tübül epitelinden "
                "türeyen küçük benign lezyonlara 'renal tübüler adenom' ve bol eozinofilik granüler mitokondri içeren tümöre "
                "'renal onkositem' denir. Akciğer bronşlarında yerleşen benign kitleler ise tarihsel olarak bronşiyal adenom "
                "olarak adlandırılmıştır."
            ),
            "elements": [
                make_cloze(
                    "Oral kontraseptif kullanan genç kadınlarda görülen ve rüptürle masif kanama yapabilen benign karaciğer tümörü hepatik adenom olarak bilinir.",
                    "hepatik adenom",
                    "Karaciğer hücreli iyi huylu ur"
                ),
                make_micro_quiz(
                    "Renal parankimde bol eozinofilik sitoplazmalı ve aşırı mitokondri birikimiyle karakterize benign epitel neoplazmı hangisidir?",
                    [
                        {
                            "text": "Renal onkositem",
                            "isCorrect": True,
                            "explanation": "Doğrudur; onkositem bol mitokondri içeren eozinofilik benign bir böbrek tümörüdür."
                        },
                        {
                            "text": "Renal berrak hücreli karsinom",
                            "isCorrect": False,
                            "explanation": "Berrak hücreli karsinom böbreğin en sık ve malign kanseridir."
                        },
                        {
                            "text": "Wilms tümörü",
                            "isCorrect": False,
                            "explanation": "Wilms tümörü çocukluk çağının oldukça malign nefrobiyoblastomudur."
                        },
                        {
                            "text": "Prostat adenokarsinomu",
                            "isCorrect": False,
                            "explanation": "Prostata özgü malign epitelyal tümördür."
                        }
                    ],
                    "Onkositem mitokondriden zengin iyi huylu epitelyal bir böbrek tümörüdür."
                )
            ]
        },
        # Slayt 29 [CHECKPOINT 3]
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Benign Tümör Terminolojisi",
            "content": (
                "Bu bölümde benign neoplazmların adlandırma ilkelerini ve doku kökenlerini ayrıntılı olarak inceledik. "
                "Mezenkimal benign tümörlerde hücre tipinin sonuna '-oma' eki getirilir: fibrom, lipom, kondrom ve osteom. "
                "Kas dokusunda çizgili kastan türeyen iyi huylu tümör 'rabdomyom', düz kastan türeyen ise 'leiomyom'dur. "
                "Epitelyal benign tümörlerde bez yapısı oluşturan veya salgı bezinden köken alan lezyonlar 'adenom' adını alır. "
                "Parmaksı fibrovasküler çıkıntılar sergileyen epitel neoplazmlarına 'papillom' denir. "
                "Polip histolojik bir terim olmayıp mukozadan lümene taşan makroskobik çıkıntıları simgeler; benign veya malign olabilir. "
                "Kistik boşluklar içeren glandüler kitleler 'kistadenom'dur (over seröz/müsinöz); hepatik adenom ise OKS ile ilişkilidir."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp03-fc01",
                    "front": "Çizgili iskelet kası hücrelerinin diferansiyasyonunu taklit eden iyi huylu mezenkimal neoplazm hangisidir?",
                    "back": "Rabdomyom kütlesidir.",
                    "hint": "Kalpte tüberoz sklerozla görülen kas kitlesi"
                },
                {
                    "id": "k1-28-cp03-fc02",
                    "front": "Salgı bezi yapısı oluşturan veya salgı bezi epitelinden kaynaklanan iyi huylu epitelyal tümör genel olarak ne ad alır?",
                    "back": "Adenom adını alır.",
                    "hint": "Glandüler benign neoplazm terimi"
                },
                {
                    "id": "k1-28-cp03-fc03",
                    "front": "Merkezinde fibrovasküler bağ dokusu ekseni barındıran parmaksı çıkıntılı iyi huylu epitel kitlelerine ne denir?",
                    "back": "Papillom denir.",
                    "hint": "Siğilimsi parmak projeksiyonlu lezyon"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 3 Özet Tablosu: Benign Neoplazm Terminoloji Kılavuzu",
                    ["Hücresel / Dokusal Köken", "Benign Nomenklatür", "Kritik Ayırıcı Örnek"],
                    [
                        {
                            "cells": ["Düz Kas Dokusu", "Leiomyom", "Uterus myomu"],
                            "hiddenIndex": 1,
                            "hint": "Myometriumun en sık uru"
                        },
                        {
                            "cells": ["Çizgili Kas Dokusu", "Rabdomyom", "Kardiyak çizgili kas kitlesi"],
                            "hiddenIndex": 1,
                            "hint": "Tüberoz skleroz kardiyak tümörü"
                        },
                        {
                            "cells": ["Kistik Glandüler Epitel", "Kistadenom", "Over seröz/müsinöz kistleri"],
                            "hiddenIndex": 1,
                            "hint": "Overin sıvı dolu dev kitleleri"
                        }
                    ]
                )
            ]
        },
        # Slayt 30
        {
            "slideNumber": 30,
            "title": "Klinik Karar: Kolon Polipektomisi ve Patolojik Sınıflama",
            "content": (
                "Kolonoskopi sırasında sigmoid kolonda 1.5 cm çapında saplı bir polip saptanan 60 yaşında hastaya "
                "tam endoskopik polipektomi uygulanıyor. Patoloji laboratuvarına gönderilen polipin incelenmesinde ilk "
                "hedef, kitlenin 'non-neoplastik' (hiperplastik polip) mi yoksa 'neoplastik' (adenomatöz polip) mi olduğunu "
                "belirlemektir. Eğer kitle displazi içeren bir tübüler veya villöz adenom ise 'premalign' kabul edilir ve "
                "polip sapında invazyon olup olmadığı dikkatle araştırılır. Sap intakt ise işlem küratiftir; ancak karsinom "
                "sapı invaze edip cerrahi sınıra ulaştıysa hastaya segmental kolon rezeksiyonu planlanmalıdır."
            ),
            "elements": [
                make_branching_logic(
                    "Kolonoskopide saptanan kolonik polipin patoloji raporunda; glandüler yapılarda düşük dereceli displazi izlenen ancak sapa veya muskularis mukozaya invazyon göstermeyen 'tübüler adenom' bildiriliyor. Cerrahi sınır negatiftir.",
                    "Bu patoloji sonucuna göre hastanın onkolojik yönetimi ve izlem protokolü ne olmalıdır?",
                    [
                        {
                            "text": "Polipektomi küratif kabul edilmeli; premalign potansiyel nedeniyle kılavuzlara uygun olarak 3-5 yıl sonra kontrol kolonoskopisi planlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; adenomlar premaligndir, tam çıkarıldığında küratiftir ancak yeni lezyonlar için takip gerektirir."
                        },
                        {
                            "text": "Adenom kesin kanser demek olduğundan hastaya derhal acil total kolektomi uygulanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Adenom benign bir premalign lezyondur, invazyon yoksa kolektomi yapılmaz."
                        },
                        {
                            "text": "Tümör malign olmadığı için hasta bir daha ömrü boyunca kolonoskopiye çağrılmamalıdır.",
                            "isCorrect": False,
                            "explanation": "Adenom öyküsü olan bireylerde yeni adenom ve kanser riski yüksektir, tarama zorunludur."
                        }
                    ]
                )
            ]
        }
    ]
