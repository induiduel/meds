# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 6: Kristalizasyon İnhibitörleri ve Promotörleri (Slayt 51 - 60)
Checkpoint: Slayt 59
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_6_slides():
    return [
        # Slayt 51
        {
            "slideNumber": 51,
            "title": "İnhibitörler: Küçük Moleküller ve Makromoleküler Faktörler",
            "content": (
                "İnsan idrarı fizyolojik koşullarda bile günün belirli saatlerinde kalsiyum oksalat açısından metastabil "
                "sınırların üzerindedir; buna rağmen popülasyonun büyük kısmında taş oluşmamasının nedeni idrarda bulunan "
                "güçlü 'kristalizasyon inhibitörleri'dir. Bu inhibitörler kimyasal yapılarına göre iki ana sınıfa ayrılır: "
                "küçük molekül ağırlıklı inorganik/organik iyonlar (sitrat, magnezyum, pirofosfat) ve böbrek tübüllerinden "
                "salgılanan büyük makromoleküler proteinler (nefrokalsin, osteopontin, Tamm-Horsfall proteini, inter-alfa-tripsin "
                "inhibitörü ve glikozaminoglikanlar). Bu moleküller nükleasyonu, kristal yüzey büyümesini ve agregasyonu "
                "farklı basamaklarda bloke ederek koruyucu bir kalkan oluştururlar."
            ),
            "elements": [
                make_table(
                    "İdrar Kristalizasyon İnhibitörlerinin Sınıflandırılması",
                    ["İnhibitör Sınıfı", "Ana Temsilciler", "Temel Moleküler Mekanizma"],
                    [
                        {
                            "cells": ["Küçük Moleküllü İnhibitörler", "Sitrat, Magnezyum, Pirofosfat", "Kalsiyum veya oksalatı şelate etme, kafese bağlanma"],
                            "hiddenIndex": 1,
                            "hint": "Düşük molekül ağırlıklı inorganik/organik iyonlar"
                        },
                        {
                            "cells": ["Makromoleküler Proteinler", "Nefrokalsin, Osteopontin, Tamm-Horsfall, GAG", "Kristal yüzeyini kaplama, agregasyon ve adezyonu engelleme"],
                            "hiddenIndex": 1,
                            "hint": "Böbrekten salgılanan koruyucu proteinler"
                        }
                    ]
                ),
                make_cloze(
                    "İdrarda kristal oluşumunu engelleyen düşük molekül ağırlıklı en kritik organik anyon sitrat molekülüdür.",
                    "sitrat",
                    "En önemli endojen inhibitör"
                )
            ]
        },
        # Slayt 52
        {
            "slideNumber": 52,
            "title": "Sitrat: Doğal İnhibitörün Dörtlü Koruyucu Mekanizması",
            "content": (
                "Sitrat, insan idrarındaki en güçlü, en etkili ve klinik olarak en kolay modüle edilebilen doğal taş "
                "inhibitörüdür. Taş oluşumunu dört farklı ve sinerjistik mekanizma ile engeller: Birincisi, idrardaki serbest "
                "iyonize kalsiyum ile son derece çözünür bir kompleks (kalsiyum sitrat) oluşturarak serbest kalsiyum miktarını "
                "ve dolayısıyla kalsiyum oksalat süpersatürasyonunu azaltır. İkincisi, kalsiyum oksalat kristallerinin kendiliğinden "
                "çökelmesini (spontan nükleasyon) doğrudan bloke eder. Üçüncüsü, mikrokristallerin yüzeyine yapışarak birbirine "
                "bağlanmasını (aglomerasyon/agregasyon) önler. Dördüncüsü, monosodyum ürat kristalleri üzerinde kalsiyum oksalatın "
                "heterojen çekirdeklenmesini (epitaksi) kuvvetle inhibe eder."
            ),
            "elements": [
                make_causal_chain(
                    "Sitratın Litogenezi Engelleyen Dört Basamaklı Koruyucu Yolu",
                    [
                        "1. Kalsiyum Şelasyonu: İyonize kalsiyumu bağlayarak çözünür kalsiyum sitrat kompleksi yapması",
                        "2. Süpersatürasyon Düşüşü: Serbest kalsiyum azaldığı için CaOx doygunluğunun gerilemesi",
                        "3. Nükleasyon Blokajı: Yeni kalsiyum oksalat çekirdeklerinin oluşumunun engellenmesi",
                        "4. Agregasyon ve Epitaksi Engeli: Kristallerin birleşmesinin ve ürat üzerinde büyümesinin durdurulması"
                    ]
                ),
                make_active_recall(
                    "Sitratın serbest kalsiyum iyonlarını bağlayarak süpersatürasyonu düşürmesini sağlayan çözünür kompleks nedir?",
                    "Kalsiyum sitrat kompleksidir.",
                    "Kalsiyum ve sitrat bileşimi"
                )
            ]
        },
        # Slayt 53
        {
            "slideNumber": 53,
            "title": "Magnezyum, Pirofosfat ve Çinko",
            "content": (
                "İnorganik iyonlar arasında yer alan magnezyum (Mg2+), pirofosfat ve çinko litogenez üzerinde kritik "
                "inhibitör etkilere sahiptir. Magnezyum, bağırsak lümeninde ve idrarda oksalat iyonları ile yarışmalı olarak "
                "bağlanır ve çözünür magnezyum oksalat bileşiği oluşturur. Bu durum kalsiyumun oksalat ile birleşmesini "
                "önleyerek CaOx süpersatürasyonunu doğrudan düşürür; hipomagnezüri taş hastalarında sıkça hipositratüriye "
                "eşlik eder. Pirofosfat ise kalsiyum fosfat ve bruşit kristallerinin büyümesini engelleyen güçlü bir inorganik "
                "inhibitördür. Çinko iyonları ise kristal kafes hataları yaratarak kristal yüzey büyümesini sonlandırır."
            ),
            "elements": [
                make_before_after(
                    "Magnezyumun Oksalat Dinamiklerine Etkisi",
                    "Düşük Magnezyum (Hipomagnezüri)",
                    "Oksalat serbest kalır, kalsiyum ile hızla birleşir, kalsiyum oksalat aşırı doygunluğu zirveye tırmanır.",
                    "Yeterli / Yüksek Magnezyum",
                    "Magnezyum oksalatı bağlar, çözünür kompleksler idrarla atılır, kalsiyum serbest kalarak taştan korunur.",
                    "Diyetle magnezyum alımı hem bağırsak emilimini hem de idrar süpersatürasyonunu dengeler."
                ),
                make_cloze(
                    "Magnezyum iyonu idrarda oksalat ile yarışmalı olarak birleşerek kalsiyum oksalat doygunluğunu azaltır.",
                    "oksalat ile yarışmalı",
                    "Kalsiyum yerine anyon bağlama"
                )
            ]
        },
        # Slayt 54
        {
            "slideNumber": 54,
            "title": "Nefrokalsin: COM Agregasyonunun Güçlü İnhibitörü",
            "content": (
                "Nefrokalsin, böbrek proksimal tübülleri ve Henle kulpunun çıkan kalın kolu epitelinden salgılanan, "
                "yaklaşık 14 kDa molekül ağırlığına sahip asidik bir glikoproteindir. Yapısında yüksek oranda aspartik "
                "asit, glutamik asit ve fosfoserin amino asitleri barındırır. Nefrokalsinin normal bireylerdeki 'A ve B' "
                "izoformları, kalsiyum oksalat monohidrat (COM) kristallerinin büyümesini ve özellikle agregasyonunu "
                "nanomolar konsantrasyonlarda bile son derece güçlü bir biçimde inhibe eder. Taş oluşturan hastalarda ise "
                "nefrokalsin molekülünün yapısında gama-karboksiglutamik asit (Gla) eksikliği saptanmış olup bu anormal form "
                "(C ve D izoformları) inhibitör etkinliğini tamamen kaybetmiştir."
            ),
            "elements": [
                make_active_recall(
                    "Böbrek tübüllerinden salgılanan ve kalsiyum oksalat monohidrat agregasyonunu nanomolar düzeyde engelleyen asidik glikoprotein hangisidir?",
                    "Nefrokalsin glikoproteinidir.",
                    "Böbrek kaynaklı asidik inhibitör"
                ),
                make_micro_quiz(
                    "Taş oluşturan bireylerde nefrokalsin molekülünün koruyucu inhibitör yeteneğini kaybetmesine yol açan yapısal bozukluk nedir?",
                    [
                        {
                            "text": "Gama-karboksiglutamik asit (Gla) içeriğinde eksiklik ve anormal C/D izoform yapısı",
                            "isCorrect": True,
                            "explanation": "Doğrudur; Gla kalıntıları eksik olduğunda kalsiyum bağlama ve yüzey inhibisyonu bozulur."
                        },
                        {
                            "text": "Molekülün aşırı miktarda hemoglobin proteini içermesi",
                            "isCorrect": False,
                            "explanation": "Nefrokalsin bir tübüler glikoproteindir, hemoglobin içermez."
                        },
                        {
                            "text": "Protein sentezinin pankreas adacıklarında gerçekleşmesi",
                            "isCorrect": False,
                            "explanation": "Nefrokalsin renal tübül hücrelerinde üretilir."
                        },
                        {
                            "text": "Üreaz enzimi tarafından tamamen parçalanması",
                            "isCorrect": False,
                            "explanation": "Üreaz üreyi parçalar, nefrokalsin mutasyonunu açıklamaz."
                        }
                    ],
                    "Nefrokalsinin inhibitör gücü gama-karboksiglutamik asit içeriğine kesin olarak bağımlıdır."
                )
            ]
        },
        # Slayt 55
        {
            "slideNumber": 55,
            "title": "Osteopontin (Uropontin): Çok Yönlü Tübüler Koruyucu",
            "content": (
                "Osteopontin (idrardaki adıyla uropontin), kemik dokusunun yanı sıra Henle kulpunda ve toplayıcı tübüllerde "
                "yoğun şekilde sentezlenen, fosforile ve polianyonik bir glikoproteindir. Osteopontin litogenezde adeta "
                "çok yönlü bir savunma kalkanı oluşturur: Kalsiyum oksalat kristallerinin nükleasyonunu, yüzey büyümesini "
                "ve partikül agregasyonunu kuvvetle baskılar. Bununla da kalmayıp, hasarlı tübüler epitel hücrelerinin "
                "apikal yüzeyindeki kristal reseptörlerini (integrik yapılar) örterek kalsiyum oksalat monohidrat kristallerinin "
                "epitele yapışmasını (adezyonunu) doğrudan engeller ve kristallerin endositozla hücreye alınmasını önler."
            ),
            "elements": [
                make_cloze(
                    "Hem nükleasyonu hem de kristallerin tübül epitel hücrelerine adezyonunu engelleyen polianyonik koruyucu osteopontin proteinidir.",
                    "osteopontin",
                    "Kemik ve idrarda bulunan uropontin"
                ),
                make_before_after(
                    "Osteopontinin Epitelyal Korumadaki Rolü",
                    "Osteopontin Yetersizliğinde",
                    "Kristaller doğrudan çıplak epitele yapışır, hücre hasarı tetiklenir, sabit partikül oluşumu hızlanır.",
                    "Yeterli ve Fonksiyonel Osteopontin Varlığında",
                    "Epitel zarı kaplanır, kristal bağlanma reseptörleri bloke edilir; serbest kalan kristaller idrarla atılır.",
                    "Osteopontin, kristal-epitel etkileşimini bloke eden en temel endojen bariyerlerden biridir."
                )
            ]
        },
        # Slayt 56
        {
            "slideNumber": 56,
            "title": "Tamm-Horsfall Proteini (Üromodulin): İkili Doğası",
            "content": (
                "Tamm-Horsfall proteini (THP), bilinen diğer adıyla üromodulin, normal insan idrarında en bol bulunan "
                "primer proteindir (günlük 30-50 mg salgılanır) ve sadece Henle kulpunun çıkan kalın kolu epitel hücreleri "
                "tarafından üretilir. THP'nin taş oluşumundaki rolü son derece ilginç ve ortam koşullarına (pH, iyonik güç) "
                "bağlı 'ikili' (ambivalent) bir karaktere sahiptir. Alkali veya nötr idrar pH'ında ve düşük iyonik güçte "
                "çözünür monomerler halinde bulunur ve kalsiyum oksalat agregasyonunun en güçlü inhibitörlerinden biridir. "
                "Buna karşın asidik idrarda (pH <5.5) veya yüksek kalsiyum konsantrasyonunda polimerize olarak jel benzeri "
                "ağlar oluşturur; kristalleri yakalayarak çökelmeyi ve litogenezi teşvik eden bir promotöre dönüşür."
            ),
            "elements": [
                make_table(
                    "Tamm-Horsfall Proteininin Ortam Koşullarına Göre Davranışı",
                    ["İdrar Koşulu", "Moleküler Formu", "Litogenezdeki Etkisi", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Alkali / Nötr pH (>6.0)", "Monomerik çözünür faz", "Güçlü İnhibitör", "CaOx kristal agregasyonunun önlenmesi"],
                            "hiddenIndex": 2,
                            "hint": "Koruyucu engelleyici durum"
                        },
                        {
                            "cells": ["Asidik pH (<5.5) / Yüksek Ca", "Polimerize jel ağı", "Promotör (Teşvik edici)", "Kristallerin yakalanması ve taş oluşumu"],
                            "hiddenIndex": 2,
                            "hint": "Taş oluşumunu hızlandırıcı durum"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Tamm-Horsfall proteininin kalsiyum oksalat agregasyonunu engelleyen güçlü bir inhibitör olarak davranabilmesi için idrar ortamının nasıl olması gerekir?",
                    [
                        {
                            "text": "Alkali veya nötr pH düzeyinde ve düşük iyonik güçte bulunması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; alkali ortamda monomerik kalarak güçlü inhibitör etki sergiler."
                        },
                        {
                            "text": "pH değerinin 4.5'in altına düşürülmüş aşırı asidik ortamda olması",
                            "isCorrect": False,
                            "explanation": "Asidik pH'ta THP polimerize olarak promotöre dönüşür."
                        },
                        {
                            "text": "Kalsiyum konsantrasyonunun maksimum doygunluğa çıkarılması",
                            "isCorrect": False,
                            "explanation": "Yüksek kalsiyum THP polimerizasyonunu ve çökelmesini tetikler."
                        },
                        {
                            "text": "Böbrek toplayıcı kanallarının tamamen tıkanmış olması",
                            "isCorrect": False,
                            "explanation": "Tıkanıklık staz yaratır, proteinin inhibitör davranışını desteklemez."
                        }
                    ],
                    "Tamm-Horsfall proteini alkali idrarda koruyucu inhibitör, asidik idrarda ise agregat promotörüdür."
                )
            ]
        },
        # Slayt 57
        {
            "slideNumber": 57,
            "title": "Glikozaminoglikanlar (GAG) ve Üriner Bariyer",
            "content": (
                "Glikozaminoglikanlar (GAG), idrarda ve mesane ürotelyum yüzeyinde bulunan sülfatlanmış polisakkarit "
                "zincirleridir. Başlıca türleri heparan sülfat, kondroitin sülfat, dermatan sülfat, hyaluronan ve keratan "
                "sülfattır. GAG molekülleri yoğun negatif elektrostatik yüklere sahiptir. Bu polianyonik yapıları sayesinde "
                "kalsiyum oksalat kristallerinin yüzeyine tutunarak kristaller arasındaki karşılıklı çekim kuvvetlerini "
                "nötralize eder ve agregasyonu kuvvetle engeller. Ayrıca ürotelyum apikal yüzeyinde impermeabl bir anti-adherent "
                "glikozaminoglikan tabakası oluşturarak bakterilerin ve kristallerin mukozaya yapışmasını mekanik ve elektriksel "
                "olarak bloke ederler."
            ),
            "elements": [
                make_cloze(
                    "Ürotelyumu kaplayarak kristal adezyonunu engelleyen negatif yüklü polisakkarit ailesine glikozaminoglikanlar adı verilir.",
                    "glikozaminoglikanlar",
                    "Mukopolisakkarit koruyucu kalkan"
                ),
                make_active_recall(
                    "Glikozaminoglikanların (heparan sülfat, kondroitin sülfat vb.) kalsiyum kristallerinin agregasyonunu engellemedeki temel fiziksel özelliği nedir?",
                    "Yoğun negatif yüzey yükleri taşıyarak kristalleri elektriksel olarak birbirini iter hale getirmeleridir.",
                    "Anyonik elektrostatik itme"
                )
            ]
        },
        # Slayt 58
        {
            "slideNumber": 58,
            "title": "Litogenez Promotörleri (Teşvik Edicileri)",
            "content": (
                "Litogenez sadece inhibitörlerin yokluğuyla değil, aynı zamanda kristalleşmeyi aktif olarak hızlandıran "
                "'promotör' faktörlerin varlığıyla tetiklenir. En önemli kristal promotörleri arasında monosodyum ürat "
                "ve serbest ürik asit kristalleri yer alır; bu kristaller epitaktik nükleasyon başlatmanın yanı sıra idrardaki "
                "doğal glikoprotein inhibitörleri (nefrokalsin ve GAG) kendi yüzeylerine adsorbe ederek tüketirler. Diğer "
                "güçlü promotörler; soyulmuş tübüler hücre membran parçaları, lökosit nükleer artıkları, hücresel lipidler, "
                "asidik idrarda polimerize olmuş Tamm-Horsfall proteini ve bakteriyel biyofilmlerdir."
            ),
            "elements": [
                make_before_after(
                    "İnhibitör - Promotör Dengesi ve Litogenez",
                    "İnhibitör Üstünlüğü (Sağlıklı Durum)",
                    "Yüksek sitrat, magnezyum ve monomerik THP; kristaller oluşsa bile agregasyon ve adezyon engellenir, taş oluşmaz.",
                    "Promotör Üstünlüğü (Litogenik Durum)",
                    "Düşük sitrat, hücresel debris, ürat kristalleri ve polimerize THP; nükleasyon hızlanır, kristaller yapışarak taşa döner.",
                    "Metabolik tedavinin ana hedefi promotörleri azaltıp inhibitör konsantrasyonunu yükseltmektir."
                ),
                make_active_recall(
                    "Ürik asit kristallerinin kalsiyum taşı oluşumunu teşvik etmede epitaksi dışındaki ikinci sinsi mekanizması nedir?",
                    "İdrardaki koruyucu inhibitör glikoproteinleri kendi yüzeyine bağlayarak etkisizleştirmesidir.",
                    "Koruyucu faktörlerin adsorpsiyonla tükenmesi"
                )
            ]
        },
        # Slayt 59 [CHECKPOINT 6]
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Kristalizasyon İnhibitörleri ve Promotörler",
            "content": (
                "Bu bölümde idrarda litogenezi engelleyen inhibitörleri ve kolaylaştıran promotör faktörleri inceledik. "
                "Sitrat, serbest kalsiyumu bağlama, nükleasyonu durdurma, agregasyonu engelleme ve epitaksiyi bloke etme olmak üzere 4'lü etkiye sahiptir. "
                "Magnezyum, oksalat ile yarışarak çözünür magnezyum oksalat yapar ve kalsiyum oksalat süpersatürasyonunu düşürür. "
                "Nefrokalsin, yapısındaki Gla kalıntıları sayesinde nanomolar düzeyde COM agregasyonunu engelleyen asidik glikoproteindir. "
                "Osteopontin hem nükleasyonu hem de kristallerin epitele adezyonunu engelleyen çok yönlü polianyonik kalkandır. "
                "Tamm-Horsfall proteini alkali idrarda güçlü bir inhibitör iken, asidik idrarda polimerize olarak agregasyon promotörüne dönüşür. "
                "GAG'lar negatif yükleriyle kristalleri iter; ürat kristalleri ve hücresel debris ise inhibitörleri tüketerek promotör rol oynar."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp06-fc01",
                    "front": "İyonize kalsiyumu şelate ederek serbest doygunluğu düşüren idrardaki en güçlü organik anyon inhibitör nedir?",
                    "back": "Sitrat anyonudur.",
                    "hint": "Narenciyede bol bulunan koruyucu tuz"
                },
                {
                    "id": "k1-27-cp06-fc02",
                    "front": "Tamm-Horsfall proteininin kristal agregasyonunu destekleyen bir promotör haline dönüştüğü idrar ortamı nasıldır?",
                    "back": "Beş buçuğun altındaki asidik idrar ortamıdır.",
                    "hint": "Düşük hidrojen iyon tamponlama durumu"
                },
                {
                    "id": "k1-27-cp06-fc03",
                    "front": "Proksimal tübülden salgılanıp yapısındaki Gla kalıntılarıyla kalsiyum agregasyonunu nanomolar düzeyde durduran protein nedir?",
                    "back": "Nefrokalsin proteinidir.",
                    "hint": "Böbrek kaynaklı asidik polipeptit"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 6 Özet Tablosu: İnhibitörlerin Karşılaştırmalı Rolleri",
                    ["İnhibitör Molekül", "Kimyasal Yapı", "Temel Savunma Mekanizması"],
                    [
                        {
                            "cells": ["Sitrat", "Organik trikarboksilik anyon", "Kalsiyum şelasyonu, nükleasyon ve agregasyon blokajı"],
                            "hiddenIndex": 0,
                            "hint": "En güçlü çözünür kompleks yapıcı"
                        },
                        {
                            "cells": ["Tamm-Horsfall (THP)", "Renal tübüler glikoprotein", "Alkali ortamda agregasyon inhibisyonu"],
                            "hiddenIndex": 0,
                            "hint": "Henle çıkan kolu proteini"
                        }
                    ]
                )
            ]
        },
        # Slayt 60
        {
            "slideNumber": 60,
            "title": "Klinik Karar: Hipositratüri Tedavisinde Potasyum Sitrat",
            "content": (
                "Tekrarlayan kalsiyum taşı olan ve 24 saatlik idrar analizinde belirgin hipositratüri (<320 mg/gün) saptanan "
                "bir hastada en fizyolojik ve etkili tıbbi tedavi 'potasyum sitrat' replasmanıdır. Verilen sitrat karaciğerde "
                "bikarbonata metabolize edilerek sistemik alkalinizasyon sağlar; bu durum renal proksimal tübül hücre içi "
                "pH'ını artırır ve sodyum-dikarboksilat taşıyıcı 1 (NaDC-1) üzerinden sitrat geri emilimini baskılayarak "
                "idrara bol miktarda serbest sitrat atılmasını sağlar. Sodyum sitrat yerine potasyum sitrat tercih edilmelidir; "
                "çünkü sodyum yükü hiperkalsiüriyi tetiklerken potasyum kalsiyum atılımını daha da azaltır."
            ),
            "elements": [
                make_branching_logic(
                    "45 yaşında tekrarlayan kalsiyum oksalat taşları düşüren erkek hastanın 24 saatlik idrar analizinde kalsiyum normal, ancak sitrat düzeyi 140 mg/gün (belirgin düşük) ve idrar pH'ı 5.4 saptanıyor.",
                    "Bu hastada taş nüksünü önlemek için tercih edilmesi gereken en uygun medikal tedavi stratejisi nedir?",
                    [
                        {
                            "text": "Oral potasyum sitrat tedavisi başlanarak hem idrar sitrat atılımı artırılmalı hem de idrar pH'ı 6.5 civarına dengelenmelidir.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; potasyum sitrat hipositratüriyi düzeltir, sodyum sitrat gibi kalsiüri yapmaz."
                        },
                        {
                            "text": "Yüksek doz sodyum bikarbonat ve sodyum klorür infüzyonu uygulanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Sodyum yükü renal tübüler kalsiyum atılımını artırarak hiperkalsiüriye ve yeni taşlara yol açar."
                        },
                        {
                            "text": "Sitrat emilimini artırmak için idrarı asitleştirici fosfat solüsyonları verilmelidir.",
                            "isCorrect": False,
                            "explanation": "İdrarı asitleştirmek tübüler sitrat geri emilimini artırır ve idrar sitratını sıfırlar."
                        }
                    ]
                )
            ]
        }
    ]
