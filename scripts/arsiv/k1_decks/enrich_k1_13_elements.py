# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını garanti eder.
"""

from scripts.k1_13_deck_data.helpers import (
    make_branching_logic, make_causal_chain, make_before_after, make_table
)

def get_extra_branching():
    """Branching logic (klinik karar verme) oranını artırmak için hedeflenen slaytlara eklenecek ögeler."""
    return {
        4: make_branching_logic(
            "42 yaşında kadın hasta, her iki el bileği ve metakarpofalangeal eklemlerde 6 aydır süren sabah tutukluğu (1 saatten uzun) ve şişlik ile başvuruyor. Eklem biyopsisinde sinoviyal hiperplazi, lenfositik foliküller ve kıkırdak üzerinde pannus dokusu izleniyor.",
            "Bu hastada eklem kıkırdağı ve kemik trabeküllerinin erimesine yol açan kronik enflamatuar tablonun temel immünopatolojik mekanizması nedir?",
            [
                {
                    "text": "Otoantijenlerin tükenmemesi nedeniyle T lenfositleri ve makrofajların aralıksız sitokin (TNF, IL-1, IL-6) üretmesidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Romatoid artritte otoantijenler ortadan kaldırılamadığı için sinovyumda kronik mononükleer yangı ve masum doku erimesi sürer."
                },
                {
                    "text": "Tekrarlayan akut piyojenik stafilokok enfeksiyonudur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Tablo bakteriyel septik artrit değil, simetrik otoimmün kronik poliartrittir."
                },
                {
                    "text": "Aşırı ürik asit kristallerinin nötrofillerle apse oluşturmasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bu akut gut artritidir; romatoid artritte pannus ve lenfositik infiltrasyon görülür."
                }
            ]
        ),
        8: make_branching_logic(
            "Trafik kazası sonrası açık tibia kırığı geçiren hastada 4 ay sonra kırık bölgesinden sarı püy akıntısı ve radyografide kemik içinde sklerotik kemikle çevrili avasküler ölü kemik parçası (sekestr) saptanıyor.",
            "Kronik osteomiyelit tablosundaki bu hastada antibiyotik tedavisinin tek başına yetersiz kalmasının temel patolojik gerekçesi nedir?",
            [
                {
                    "text": "Sekestr dokusunun kan dolaşımından yoksun (avasküler) olması nedeniyle antibiyotiklerin bakteri odağına ulaşamamasıdır; cerrahi sekestrektomi gerekir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Ölü kemik avaskülerdir; antibiyotikler kemiğe geçemez, cerrahi debridman ve sekestrektomi şarttır."
                },
                {
                    "text": "Bakterilerin tamamen virulansını kaybetmesidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bakteriler canlıdır ve kronik süpürasyona yol açar."
                },
                {
                    "text": "Kemikte kalsiyum birikiminin antibiyotiği parçalamasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Sorun kimyasal parçalanma değil, kanlanmanın olmamasıdır."
                }
            ]
        ),
        14: make_branching_logic(
            "Siroz ve portal hipertansiyonu olan bir hastada portal kandan gelen bakterilerin karaciğerde filtrelenememesi sonucu sık sık spontan bakteriyel peritonit ve bakteriyemi atakları gelişiyor.",
            "Portal dolaşımla gelen mikroorganizmaları ve endotoksinleri fagositozla süzen, ancak sirozda şantlar nedeniyle devre dışı kalan karaciğer rezidan makrofajları hangisidir?",
            [
                {
                    "text": "Karaciğer sinüzoidlerinde yerleşik Kupffer hücreleridir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Kupffer hücreleri portal kanın majör fagositer filtre istasyonudur."
                },
                {
                    "text": "Perisinüzoidal Ito hücreleridir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Ito hücreleri A vitamini depolar ve kollajen sentezler; fagositoz yapmaz."
                },
                {
                    "text": "Safra kanalikül epitel hücreleridir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kolanjiositler epitel hücreleridir, makrofaj değildir."
                }
            ]
        ),
        18: make_branching_logic(
            "İdiyopatik pulmoner fibrozis tanılı hastanın akciğer doku incelemesinde fibroblastik odaklar, bol kollajen birikimi ve M2 makrofaj zenginliği izleniyor.",
            "Bu hastada fibroblastları doğrudan aktive ederek ekstraselüler matriks birikimini ve geri dönüşsüz akciğer fibrozisini tetikleyen ana makrofaj sitokini hangisidir?",
            [
                {
                    "text": "M2 makrofaj kökenli Dönüştürücü Büyüme Faktörü-Beta'dır (TGF-β).",
                    "isCorrect": True,
                    "feedback": "Doğrudur. TGF-beta dokuda kollajen sentezinin ve miyofibroblast aktivasyonunun anahtar sitokinidir."
                },
                {
                    "text": "M1 makrofaj kökenli Tümör Nekroz Faktörüdür.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. TNF nekroz ve akut yangı yapar; fibrogenezisin primer hormonu TGF-betadır."
                },
                {
                    "text": "Histamin ve Serotonindir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Vazoaktif aminlerin organ fibrozisinde rolü yoktur."
                }
            ]
        ),
        24: make_branching_logic(
            "Yüksek doz inhale steroid ve uzun etkili beta-agoniste rağmen sık astım alevlenmesi yaşayan, kanda ve balgamda belirgin eozinofili saptanan 28 yaşındaki hastaya biyolojik tedavi düşünülmektedir.",
            "Eozinofillerin kemik iliğinden çıkışını, farklılaşmasını ve dokuda sağkalımını keserek eozinofilik enflamasyonu söndürmek için hangi sitokin bloke edilmelidir?",
            [
                {
                    "text": "İnterlökin-5 (IL-5) mepolizumab veya reslizumab ile bloke edilmelidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. IL-5 eozinofillerin primer büyüme ve sağkalım sitokinidir; blokajı eozinofil sayısını sıfırlar."
                },
                {
                    "text": "İnterlökin-1 beta bloke edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. IL-1 ateşi ve inflamazomu yönetir, eozinofil için spesifik değildir."
                },
                {
                    "text": "İnterferon-gama bloke edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. IFN-gama Th1 sitokinidir, alerjik astımda zaten baskılanmıştır."
                }
            ]
        ),
        32: make_branching_logic(
            "Katı gıdaları yutarken takılma (disfaji) ve retrosternal yanma şikayetiyle başvuran 20 yaşındaki atopik hastanın özofagus biyopsisinde skuamöz epitel içine sızmış bol miktarda (>15/HPF) eozinofil lökosit saptanıyor (Eozinofilik Özofajit).",
            "Bu hastada eozinofilleri özofagus epiteline çeken ve kemotaksis sağlayan en spesifik kemokin ailesi hangisidir?",
            [
                {
                    "text": "CCR3 reseptörüne bağlanan Eotaksin (CCL11, CCL24, CCL26) ailesidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Eotaksin epitelden salınarak CCR3 taşıyan eozinofilleri doğrudan mukozaya çeker."
                },
                {
                    "text": "CXCR1 reseptörüne bağlanan İnterlökin-8'dir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. IL-8 nötrofilleri çeker, eozinofilleri çekmez."
                },
                {
                    "text": "CCR2 reseptörüne bağlanan MCP-1'dir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. MCP-1 monosit kemoatraktanıdır."
                }
            ]
        ),
        44: make_branching_logic(
            "Lenf düğümü biyopsisinde granülom merkezinde epiteloid histiositlerin kaynaşmasıyla oluşmuş çok çekirdekli dev hücreler saptanıyor. Çekirdeklerin hücre periferinde at nalı gibi dizildiği izleniyor.",
            "Bu morfolojik çekirdek dizilimine sahip olan ve tüberkülozda klasik olarak saptanan dev hücre tipi hangisidir?",
            [
                {
                    "text": "Langhans tipi dev hücredir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. At nalı veya taç şeklinde periferik çekirdek dizilimi Langhans dev hücresinin imzasıdır."
                },
                {
                    "text": "Yabancı cisim tipi dev hücredir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Yabancı cisim tipinde çekirdekler sitoplazmada dağınık ve kaotiktir."
                },
                {
                    "text": "Touton tipi dev hücredir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Touton hücresinde çekirdekler tam halka oluşturur ve etrafı köpüksü lipidle çevrilidir."
                }
            ]
        ),
        54: make_branching_logic(
            "Boyunda kazeöz nekrotizan lenfadeniti olan hastanın lenf nodu biyopsisinde Ehrlich-Ziehl-Neelsen boyasında aside dirençli basil görülemiyor (paucibacillary olgu).",
            "Tüberküloz şüphesi son derece yüksek olan bu hastada doku kesitinde basil varlığını 24 saat içinde kesin olarak kanıtlayacak en duyarlı yöntem nedir?",
            [
                {
                    "text": "Parafin blok dokusundan tüberküloza özgü IS6110 dizisine yönelik Polimeraz Zincir Reaksiyonu (PCR) yapılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. PCR mikroskobik boyamada görülemeyen çok az sayıdaki basil DNA'sını dahi saptar."
                },
                {
                    "text": "Yalnızca Gram boyası tekrarlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Tüberküloz basili Gram boyası tutmaz."
                },
                {
                    "text": "Hasta hiçbir tedavi verilmeden 1 yıl sonra kontrole çağrılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kazeöz nekroz tüberküloz lehinedir, tanı geciktirilemez."
                }
            ]
        ),
        58: make_branching_logic(
            "Yüzünde 'aslan yüzü' (fasiyes leonina) görünümü ve kulak memelerinde nodülleri olan hastanın deri biyopsisinde granülom görülmüyor; dermisi dolduran köpüksü sitoplazmalı makrofajlar ve içlerinde milyonlarca basil saptanıyor.",
            "Hücresel bağışıklığın çöktüğü bu Lepromatöz Lepra tablosunda izlenen köpüksü hücrelere ve hastada izlenen immünolojik duruma ne ad verilir?",
            [
                {
                    "text": "Virchow (lepra) hücreleri izlenir; konakta Th1 hücresel yanıtı anerjiktir (çökmüştür).",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Lepromatöz leprada Th1 çökmüştür; granülom yapılamaz, basil dolu Virchow hücreleri birikir."
                },
                {
                    "text": "Langhans hücreleri izlenir; aşırı güçlü Th1 yanıtı mevcuttur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Güçlü Th1 yanıtında granülomlu tüberküloid lepra görülür, lepromatöz değil."
                },
                {
                    "text": "Reed-Sternberg hücreleri izlenir; tablo malign lenfomadır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Hastalık bakteriyel lepradır, Hodgkin lenfoma değildir."
                }
            ]
        ),
        64: make_branching_logic(
            "Kolesistektomi ameliyatından 6 ay sonra ameliyat kesi yerinde sert, ağrısız bir nodül beliren hastadan alınan eksizyonel biyopside merkezde lifli bir materyal ve çevresinde düzensiz dağılmış çekirdekleri olan dev hücreler görülüyor.",
            "Nekroz içermeyen bu reaksiyonun tanısı nedir ve polarize ışık mikroskobunda ne izlenir?",
            [
                {
                    "text": "Cerrahi dikiş ipliğine bağlı yabancı cisim granülomudur; polarize ışıkta iplik lifleri çift kırıcılıkla (birefringens) parlar.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Cerrahi sütürler yabancı cisim granülomu yapar ve polarize ışıkta parlak çift kırıcılık gösterir."
                },
                {
                    "text": "Kazeöz nekrozlu tüberküloz granülomudur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Dikiş granülomunda kazeifikasyon nekrozu ve mikobakteri bulunmaz."
                },
                {
                    "text": "Malign liposarkom tümörüdür.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Tablo neoplazi değil reaktif yabancı cisim granülomudur."
                }
            ]
        ),
        68: make_branching_logic(
            "72 yaşında kadın hasta, son 2 haftadır şiddetli tek taraflı şakak ağrısı, çiğneme sırasında çenede yorulma ve sol gözde geçici görme kararması şikayetleriyle başvuruyor. Sedimentasyon hızı 110 mm/saat ölçülüyor.",
            "Körlük riski nedeniyle acil yüksek doz kortikosteroid başlanması gereken ve arter biyopsisinde tunica mediada granülomatöz dev hücreler beklenen vaskülit hangisidir?",
            [
                {
                    "text": "Dev Hücreli (Temporal) Arterittir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Yaşlı hastada şakak ağrısı, çene kladikasyosu, yüksek ESR ve görme kaybı riski temporal arteriti kesinleştirir."
                },
                {
                    "text": "Takayasu arteritidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Takayasu genç kadınlarda aort dallarını tutar, 72 yaşta temporal kranial tutulum dev hücreli arterittir."
                },
                {
                    "text": "Henoch-Schönlein purpurasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Çocuklarda IgA vaskülitidir."
                }
            ]
        ),
        72: make_branching_logic(
            "10 yıldır romatoid artrit tedavisi gören hastada hemoglobin 9.2 g/dL, serum demiri düşük, ferritin düzeyi ise yüksek (450 ng/mL) saptanıyor. Oral demir tedavisine hiçbir yanıt alınamıyor.",
            "Bu hastadaki Kronik Hastalık Anemisinde oral demirin emilememesinden ve makrofajlarda hapsolmasından sorumlu olan, IL-6 ile karaciğerden salınan peptit hormon hangisidir?",
            [
                {
                    "text": "Hepsidindir (ferroportin kanallarını yıkar).",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Kronik enflamasyonda IL-6 hepsidini artırır; hepsidin ferroportini yıkarak demiri kilitler."
                },
                {
                    "text": "Eritropoietindir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Eritropoietin kemik iliğini uyarır, demiri kilitleyen hepsidindir."
                },
                {
                    "text": "Transferrindir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Transferrin demir taşıyıcı proteindir, kronik yangıda sentezi azalır."
                }
            ]
        ),
        76: make_branching_logic(
            "Kronik hepatit B enfeksiyonuna bağlı karaciğer sirozu gelişen bir hastada portal ven basıncının artması sonucu splenomegali, assit ve özofagus varisleri gelişiyor.",
            "Karaciğer parankim mimarisini tamamen bozan fibröz septaları oluşturan ve A vitamini depolayan hücreden miyofibroblasta dönüşen hücre hangisidir?",
            [
                {
                    "text": "Perisinüzoidal Ito (karaciğer yıldızsı) hücreleridir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Karaciğerde fibrogenezisin ve sirotik kollajen üretiminin baş mimarı Ito hücreleridir."
                },
                {
                    "text": "Kupffer fagositer hücreleridir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kupffer makrofajdır, sitokin salar ancak kollajen matriksi üreten Ito hücresidir."
                },
                {
                    "text": "Sinüzoid endotel hücreleridir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Endotel hücreleri kollajen septa oluşturmaz."
                }
            ]
        ),
        84: make_branching_logic(
            "Kemoterapi alan nötropenik lösemi hastasında akciğerde kavitasyonlu infiltrat saptanıyor. Biyopside kazeifiye nekroz izleniyor ancak Ziehl-Neelsen boyası negatif bulunuyor.",
            "Fırsatçı derin mantar enfeksiyonlarını dışlamak için kesite Grocott Metenamin Gümüş (GMS) boyası uygulandığında mikroskopta ne görülmesi mantar lehinedir?",
            [
                {
                    "text": "Mantar hücre duvarlarının ve hiflerinin açık yeşil zemin üzerinde kömür siyahı renkte boyanmasıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. GMS mantar duvarını simsiyah gümüşleyerek mikroskopta parlamasını sağlar."
                },
                {
                    "text": "Hücrelerin parlak sarı renkte görünmesidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. GMS gümüş reaksiyonu kömür siyahı renk verir."
                },
                {
                    "text": "Yalnızca eritrositlerin mavi boyanmasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. GMS mantar teşhis boyasıdır."
                }
            ]
        ),
        94: make_branching_logic(
            "İdiyopatik pulmoner fibrozis tanısı kesinleşen 62 yaşındaki erkek hastada solunum fonksiyon testlerinde restriktif bozulma ve efor dispnesinde hızlı ilerleme saptanıyor.",
            "Akciğerde kollajen birikimini ve fibroblast proliferasyonunu yavaşlatmak amacıyla PDGFR, FGFR ve VEGFR reseptörlerini bloke eden anti-fibrotik kinaz inhibitörü hangisidir?",
            [
                {
                    "text": "Nintedanibdir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Nintedanib üçlü büyüme faktörü reseptör inhibitörü olarak pulmoner fibrozis ilerlemesini yavaşlatır."
                },
                {
                    "text": "Aspirindir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Aspirin trombosit ve COX inhibitörüdür, anti-fibrotik değildir."
                },
                {
                    "text": "Penisilindir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Antibakteriyel ajandır, pulmoner fibroziste yeri yoktur."
                }
            ]
        )
    }

def get_extra_tables():
    """Interactive table oranını artırmak için hedeflenen slaytlara eklenecek tablolar."""
    return {
        2: make_table(
            ["Kriter", "Akut Enflamasyon", "Kronik Enflamasyon"],
            [
                [
                    {"text": "Vasküler Yanıt", "isMasked": False, "hint": ""},
                    {"text": "Vazodilatasyon ve belirgin permeabilite artışı", "isMasked": False, "hint": ""},
                    {"text": "Anjiyogenez (yeni damar tomurcuklanması)", "isMasked": True, "hint": "Kronik fazdaki damar oluşumu"}
                ],
                [
                    {"text": "Hücresel İnfiltrat", "isMasked": False, "hint": ""},
                    {"text": "Nötrofil polimorfları", "isMasked": True, "hint": "İlk saatlerin savunma hücresi"},
                    {"text": "Mononükleer lökositler (makrofaj, lenfosit)", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Doku Onarımı", "isMasked": False, "hint": ""},
                    {"text": "Minimal skar veya tam rezolüsyon", "isMasked": False, "hint": ""},
                    {"text": "Yaygın fibrozis ve parankim kaybı", "isMasked": True, "hint": "Kalıcı bağ dokusu birikimi"}
                ]
            ]
        ),
        22: make_table(
            ["T Yardımcı Hücre", "Başlıca Efektör Sitokin", "Klasik Hastalık Modeli"],
            [
                [
                    {"text": "Th1", "isMasked": False, "hint": ""},
                    {"text": "İnterferon-gama (IFN-γ)", "isMasked": True, "hint": "Makrofaj aktive eden Th1 sitokini"},
                    {"text": "Tüberküloz, Sarkoidoz, Crohn Hastalığı", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Th2", "isMasked": True, "hint": "Alerji ve parazit T hücresi"},
                    {"text": "IL-4, IL-5, IL-13", "isMasked": False, "hint": ""},
                    {"text": "Bronşiyal Astım, Atopik Dermatit", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Th17", "isMasked": False, "hint": ""},
                    {"text": "İnterlökin-17 (IL-17)", "isMasked": True, "hint": "Nötrofil toplayan sitokin"},
                    {"text": "Psöriyazis, Ankilozan Spondilit", "isMasked": False, "hint": ""}
                ]
            ]
        ),
        42: make_table(
            ["Granülom Tabakası", "Hücresel / Yapısal İçerik", "Biyolojik Fonksiyonu"],
            [
                [
                    {"text": "Santral Merkez", "isMasked": False, "hint": ""},
                    {"text": "Kazeöz nekroz veya yabancı partikül", "isMasked": True, "hint": "Hapsedilen zararlı odak"},
                    {"text": "Etkenin izole edildiği nekrotik çekirdek", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Orta Katman", "isMasked": True, "hint": "Epiteloid hücre kalkanı"},
                    {"text": "Epiteloid histiositler ve dev hücreler", "isMasked": False, "hint": ""},
                    {"text": "Sıkı kenetlenmiş hücresel karantina kalkanı", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Periferik Manto", "isMasked": False, "hint": ""},
                    {"text": "T/B lenfositleri ve fibroblastik kollajen", "isMasked": False, "hint": ""},
                    {"text": "Sitokin desteği ve fibröz sınırlandırma", "isMasked": True, "hint": "Kapsül ve lenfosit kuşağı"}
                ]
            ]
        ),
        62: make_table(
            ["Nekrotizan Granülomatöz Hastalık", "Etken Patojen", "Özgün Histopatolojik Nitelik"],
            [
                [
                    {"text": "Kedi Tırmığı Hastalığı", "isMasked": False, "hint": ""},
                    {"text": "Bartonella henselae", "isMasked": True, "hint": "Gram-negatif çomak etken"},
                    {"text": "Merkezde nötrofilli yıldızsı (stellat) mikroapseler", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Lenfogranüloma Venereum", "isMasked": True, "hint": "Klamidya lenfadeniti"},
                    {"text": "Chlamydia trachomatis (L1-L3)", "isMasked": False, "hint": ""},
                    {"text": "İnguinal lenf nodunda oluklaşan süpüratif apseler", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Tüberküloz Lenfadenit", "isMasked": False, "hint": ""},
                    {"text": "Mycobacterium tuberculosis", "isMasked": False, "hint": ""},
                    {"text": "Amorf kazeöz nekroz ve Langhans dev hücreleri", "isMasked": True, "hint": "Klasik peynirimsi nekroz"}
                ]
            ]
        ),
        82: make_table(
            ["Histopatolojik Boya", "Hedeflenen Biyolojik Yapı", "Mikroskopta Pozitif Renk"],
            [
                [
                    {"text": "Ehrlich-Ziehl-Neelsen (EZN)", "isMasked": False, "hint": ""},
                    {"text": "Mikobakteri hücre duvarı mikolik asidi", "isMasked": True, "hint": "Asit-fast mumsu lipid"},
                    {"text": "Mavi fonda parlak kırmızı basiller", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Grocott Metenamin Gümüş (GMS)", "isMasked": True, "hint": "Mantar duvarı gümüş boyası"},
                    {"text": "Mantar duvarı polisakkaritleri", "isMasked": False, "hint": ""},
                    {"text": "Açık yeşil fonda kömür siyahı yapılar", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Masson Trikrom", "isMasked": False, "hint": ""},
                    {"text": "Kollajen lifleri ve fibrozis", "isMasked": False, "hint": ""},
                    {"text": "Parlak mavi renkte boyanma", "isMasked": True, "hint": "Trikromdaki bağ dokusu rengi"}
                ]
            ]
        )
    }

def get_extra_chains():
    """Causal chain oranını artırmak için hedeflenen slaytlara eklenecek zincirler."""
    return {
        16: make_causal_chain(
            "M2 Makrofaj Arginaz-1 ve Kollajen Sentez Zinciri",
            [
                "1. Th2 Uyarımı: Dokuda biriken IL-4 ve IL-13 makrofajdaki M2 sinyalini açar.",
                "2. Arginaz-1 Aktivasyonu: iNOS baskılanır; arginaz-1 enzimi hücrede hızla artar.",
                "3. Ornitin ve Prolin Üretimi: Arginin amino asidi ornitine ve ardından proline çevrilir.",
                "4. Kollajen Triple-Heliks: Prolin ve hidroksiprolin fibroblastlarda kollajen liflerinin temelini kurar."
            ]
        ),
        52: make_causal_chain(
            "Tüberkülozda Kazeifikasyon Nekrozu Gelişim Zinciri",
            [
                "1. Makrofajda Basil Üremesi: Tüberküloz basilleri fagozomda çoğalarak makrofajı doldurur.",
                "2. Th1 ve TNF Patlaması: T hücreleri yoğun IFN-gama ve makrofajlar yüksek dozda TNF-alfa salar.",
                "3. Toksik Doku Erimesi: Aşırı TNF ve serbest radikaller makrofajları ve parankimi topluca öldürür.",
                "4. Kazeöz Enkaz: Hücre zarları erir; mikolik asit lipidleri ve hücresel proteinler peynirimsi nekroza döner."
            ]
        )
    }

def enrich_slides(slides):
    """Slayt listesini alır ve eklenen elemanlarla zenginleştirip dengeli olarak geri döndürür."""
    branching_map = get_extra_branching()
    table_map = get_extra_tables()
    chain_map = get_extra_chains()

    for idx, slide in enumerate(slides, start=1):
        if idx in branching_map:
            slide["elements"].append(branching_map[idx])
        if idx in table_map:
            slide["elements"].append(table_map[idx])
        if idx in chain_map:
            slide["elements"].append(chain_map[idx])

    return slides
