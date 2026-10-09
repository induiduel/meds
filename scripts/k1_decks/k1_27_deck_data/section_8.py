# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 8: Kalsiyum Taşlarının Patofizyolojisi (Slayt 71 - 80)
Checkpoint: Slayt 79
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_8_slides():
    return [
        # Slayt 71
        {
            "slideNumber": 71,
            "title": "Kalsiyum Taşları ve Metabolik Bozukluk Spektrumu",
            "content": (
                "Kalsiyum taşları (kalsiyum oksalat ve kalsiyum fosfat), tüm üriner sistem taşlarının yaklaşık %80'ini "
                "oluşturarak en yaygın görülen grubu teşkil eder. Bu hastalarda tek bir patoloji yerine birden fazla "
                "metabolik dengesizlik bir arada bulunur. En sık saptanan metabolik anormallik %50'ye varan oranla "
                "'hiperkalsiüri'dir. Bunu sırasıyla hipositratüri (%20-30), hiperürikozüri (%15-25), hiperoksalüri (%10-20), "
                "düşük idrar hacmi ve hipomagnezüri izler. Kapsamlı metabolik değerlendirme yapılan kalsiyum taşı hastalarının "
                "yalnızca %3'ten daha azında hiçbir metabolik anormallik bulunamaz (idiyopatik kalsiyum taşı); geri kalan %97'sinde "
                "spesifik ve tedavi edilebilir fizyopatolojik hedefler mevcuttur."
            ),
            "elements": [
                make_cloze(
                    "Kalsiyum taşı oluşturan hastalarda en sık saptanan metabolik bozukluk yüzde elliye varan sıklıkla hiperkalsiüri durumudur.",
                    "hiperkalsiüri",
                    "İdrarda aşırı kalsiyum atılımı"
                ),
                make_active_recall(
                    "Kalsiyum taşı hastalarında hiçbir metabolik neden bulunamayan gerçek idiyopatik olguların oranı yaklaşık yüzde kaçtır?",
                    "Yüzde üçten daha azdır.",
                    "Yüzde üç altındaki oran"
                )
            ]
        },
        # Slayt 72
        {
            "slideNumber": 72,
            "title": "Hiperkalsiüri: Tanım ve Absorptif Hiperkalsiüri",
            "content": (
                "Hiperkalsiüri, standart bir diyette 24 saatlik idrar kalsiyum atılımının erkeklerde >300 mg/gün, kadınlarda "
                ">250 mg/gün veya her iki cinste vücut ağırlığına göre >4 mg/kg/gün olması olarak tanımlanır. Etiyolojik olarak "
                "üç ana grupta incelenir: absorptif, renal ve resorptif hiperkalsiüri. Absorptif hiperkalsiüri, jejunumdan "
                "bağırsak kalsiyum emiliminin patolojik olarak artmasından kaynaklanır. Tip I absorptif hiperkalsiüri diyetteki "
                "kalsiyum kısıtlamasına rağmen devam eden şiddetli emilim fazlalığıdır. Tip II ise diyet kalsiyumu kısıtlandığında "
                "(<400 mg/gün) idrar kalsiyumunun normale döndüğü daha hafif, diyete bağımlı formdur; her iki tipte de serum PTH "
                "düzeyi normal veya baskılıdır."
            ),
            "elements": [
                make_table(
                    "Hiperkalsiüri Tipleri ve Ayırıcı Tanı Kriterleri",
                    ["Hiperkalsiüri Tipi", "Primer Organ Kusuru", "Serum Kalsiyumu", "Serum PTH Düzeyi"],
                    [
                        {
                            "cells": ["Absorptif (Tip I / II)", "İnce bağırsak (Jejunum)", "Normal", "Normal veya baskılı"],
                            "hiddenIndex": 3,
                            "hint": "Paratiroid hormon düzeyi"
                        },
                        {
                            "cells": ["Renal (Kaçak)", "Böbrek tübülleri", "Normal veya hafif düşük", "Sekonder olarak yüksek"],
                            "hiddenIndex": 3,
                            "hint": "Kalsiyum kaybına reaktif paratiroid yanıtı"
                        },
                        {
                            "cells": ["Resorptif", "Kemik (Adenom)", "Yüksek (Hiperkalsemi)", "Primer olarak yüksek"],
                            "hiddenIndex": 2,
                            "hint": "Kanda kalsiyum yüksekliği"
                        }
                    ]
                ),
                make_cloze(
                    "Bireylerde vücut ağırlığına göre günlük üriner kalsiyum atılımının dört miligram bölü kilogramı aşması hiperkalsiüri kabul edilir.",
                    "dört miligram bölü kilogramı",
                    "Kilo başına kalsiyum üst sınırı"
                )
            ]
        },
        # Slayt 73
        {
            "slideNumber": 73,
            "title": "Renal Hiperkalsiüri: Tübüler Kaçak Mekanizması",
            "content": (
                "Renal hiperkalsiüri, böbrek proksimal tübülü veya Henle kulpunda kalsiyumun geri emilim mekanizmalarındaki "
                "primer bir bozukluğa bağlı olarak ortaya çıkar. Böbrek kalsiyumu tutamaz ve idrara sürekli 'kalsiyum kaçağı' "
                "olur. Bu kontrolsüz idrar kaybı serum iyonize kalsiyum konsantrasyonunu hafifçe düşürür. Düşen serum kalsiyumu "
                "paratiroid bezlerini uyararak 'sekonder hiperparatiroidi' tablosuna yol açar. Yükselen PTH, böbrekte 1-alfa "
                "hidroksilazı aktive ederek 1,25-dihidroksi D vitamini (kalsitriol) sentezini artırır; bu da bağırsaktan "
                "kalsiyum emilimini sekonder olarak yükseltir. Renal hiperkalsiüriyi absorptif formdan ayıran en temel bulgu, "
                "açlık durumunda bile yüksek idrar kalsiyumu ve yüksek serum PTH düzeyidir."
            ),
            "elements": [
                make_causal_chain(
                    "Renal Hiperkalsiüride Tübüler Kaçak ve Sekonder Yanıt Kaskadı",
                    [
                        "1. Tübüler Defekt: Proksimal ve kalın çıkan kolda kalsiyum reabsorpsiyonunun bozulması",
                        "2. Üriner Kaçak: İdrarla zorunlu kalsiyum kaybının başlaması ve serum kalsiyumunun düşme eğilimi",
                        "3. Paratiroid Yanıtı: Kalsiyum düşüşünü kompanse etmek için sekonder PTH salgılanması",
                        "4. Kalsitriol Aktivasyonu: PTH'ın böbrekte aktif D vitamini sentezini tetiklemesi",
                        "5. Barsak Emilimi: Bağırsaktan kalsiyum çekilerek serum seviyesinin dengelenmesi ancak idrarın süpersatüre kalması"
                    ]
                ),
                make_active_recall(
                    "Renal kalsiyum kaçağında paratiroid bezlerinin reaktif olarak uyarılmasıyla gelişen endokrin durum nedir?",
                    "Sekonder hiperparatiroidi durumudur.",
                    "Kalsiyum düşüşüne reaktif hormon yanıtı"
                )
            ]
        },
        # Slayt 74
        {
            "slideNumber": 74,
            "title": "Resorptif Hiperkalsiüri: Primer Hiperparatiroidi vs Sarkoidoz",
            "content": (
                "Resorptif hiperkalsiüri, kemik dokusundan masif kalsiyum yıkımı ve kana karışması sonucu gelişir. "
                "En sık neden, soliter bir paratiroid adenomuna bağlı gelişen 'primer hiperparatiroidi'dir (PHPT). "
                "PHPT'de otonom yüksek PTH kemikten kalsiyum resorpsiyonunu artırır; glomerüler kalsiyum yükü tübüler emilim "
                "kapasitesini aşarak hem 'hiperkalsemi' hem de 'hiperkalsiüri' yaratır. Taş hastasında hiperkalsemi ile hiperkalsiürinin "
                "birlikte görülmesi ayırıcı tanının en kritik adımıdır. Eğer PTH yüksekse tanı kesin primer hiperparatiroididir. "
                "Buna karşın sarkoidoz veya tüberküloz gibi granülomatöz hastalıklarda epiteloid histiositler kontrolsüz "
                "1-alfa hidroksilaz üretir; aşırı D vitamini hiperkalsemi yapar ancak paratiroid bezi baskılanır (PTH düşüktür)."
            ),
            "elements": [
                make_table(
                    "Hiperkalsemik Hiperkalsiüride Laboratuvar Ayırıcı Tanısı",
                    ["Hastalık", "Serum Kalsiyumu", "Serum PTH", "1,25-(OH)2 D Vitamini", "Klinik Özellik"],
                    [
                        {
                            "cells": ["Primer Hiperparatiroidi", "Yüksek", "Yüksek veya uygunsuz normal", "Yüksek / Normal", "Paratiroid adenomu, kemik kistleri"],
                            "hiddenIndex": 2,
                            "hint": "Primer otonom hormon artışı"
                        },
                        {
                            "cells": ["Sarkoidoz / Granülom", "Yüksek", "Tamamen baskılı (Düşük)", "Aşırı Yüksek", "Hiler lenfadenopati, akciğer tutulumu"],
                            "hiddenIndex": 2,
                            "hint": "Ekstra-renal kalsitriol sentezi"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Böbrek taşı olan bir hastada hiperkalsemi saptandığında, primer hiperparatiroidiyi sarkoidozdan ayıran en belirleyici parametre hangisidir?",
                    [
                        {
                            "text": "Primer hiperparatiroidide serum PTH düzeyi yüksek iken sarkoidozda PTH'ın baskılı olması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; sarkoidozda kontrolsüz D vitamini hiperkalsemi yapar ve PTH'ı baskılar."
                        },
                        {
                            "text": "Sarkoidozda idrar kalsiyumunun tamamen sıfır olması",
                            "isCorrect": False,
                            "explanation": "Sarkoidozda da şiddetli hiperkalsiüri görülür."
                        },
                        {
                            "text": "Primer hiperparatiroidide hastaların daima çocuk yaşta olması",
                            "isCorrect": False,
                            "explanation": "Primer hiperparatiroidi çoğunlukla postmenopozal kadınlarda ve erişkinlerde görülür."
                        },
                        {
                            "text": "Sarkoidozda taşların yalnızca saf sistinden oluşması",
                            "isCorrect": False,
                            "explanation": "Sarkoidozda kalsiyum taşları görülür, sistin genetik bir hastalıktır."
                        }
                    ],
                    "PTH düzeyi, hiperkalsemik taş hastalarında etiyolojik ayrımın temel anahtarıdır."
                )
            ]
        },
        # Slayt 75
        {
            "slideNumber": 75,
            "title": "Hiperürikozüri ve Kalsiyum Oksalat Taşı İlişkisi",
            "content": (
                "Hiperürikozüri, 24 saatlik idrarda ürik asit atılımının erkeklerde >800 mg/gün, kadınlarda >750 mg/gün "
                "veya genel olarak >700 mg/gün olmasıdır. En sık neden aşırı hayvansal pürin tüketimidir. İlginç olarak "
                "hiperürikozürisi olan hastaların önemli bir kısmı saf ürik asit taşı değil, kalsiyum oksalat taşı oluşturur. "
                "Bunun nedeni iki mekanizmaya dayanır: İdrar pH'ı >5.5 olduğunda çözünen monosodyum ürat kristalleri, "
                "kalsiyum oksalat için ideal bir heterojen çekirdeklenme (epitaksi) şablonu oluşturur. İkincisi, kolloidal "
                "ürat kristalleri idrardaki koruyucu glikozaminoglikan ve glikoprotein inhibitörleri adsorbe ederek tüketir; "
                "inhibitörsüz kalan idrarda kalsiyum oksalat hızla çöker."
            ),
            "elements": [
                make_cloze(
                    "Yirmi dört saatlik idrarda ürik asit atılımının yedi yüz miligramın üzerine çıkması hiperürikozüri olarak kabul edilir.",
                    "yedi yüz miligramın",
                    "Günlük ürik asit atılım eşiği"
                ),
                make_active_recall(
                    "Hiperürikozürinin kalsiyum oksalat taşı oluşumunu tetiklemesindeki temel fizikokimyasal süreç nedir?",
                    "Monosodyum ürat üzerinde epitaktik heterojen çekirdeklenme ve koruyucu inhibitörlerin emilerek tüketilmesidir.",
                    "Kafes şablonu ve inhibitör adsorpsiyonu"
                )
            ]
        },
        # Slayt 76
        {
            "slideNumber": 76,
            "title": "Diyet Kaynaklı Hiperoksalüri ve Oxalobacter Formigenes",
            "content": (
                "Hiperoksalüri, 24 saatlik idrar oksalat atılımının >40-45 mg/gün olmasıdır. İdrar oksalatındaki ufak bir artış "
                "kalsiyumdaki büyük bir artıştan termodinamik olarak çok daha litojeniktir. Diyet kaynaklı hiperoksalüri, "
                "oksalattan zengin gıdaların (ıspanak, pazı, fındık, ceviz, çikolata, siyah çay, pancar) aşırı tüketilmesi "
                "veya yüksek doz C vitamini (askorbik asidin in vivo oksalata dönüşmesi) alımıyla tetiklenir. Normal insan "
                "kolonunda yaşayan anaerobik bir bakteri olan 'Oxalobacter formigenes', temel enerji kaynağı olarak oksalatı "
                "kullanır ve parçalar. Geniş spektrumlu antibiyotik kullanımıyla O. formigenes florasının yok edilmesi, "
                "serbest oksalat emilimini artırarak taş nükslerini belirgin biçimde tırmandırır."
            ),
            "elements": [
                make_before_after(
                    "Oxalobacter formigenes Varlığının Oksalat Dengesine Etkisi",
                    "İntakt O. formigenes Kolonizasyonu",
                    "Bağırsak lümenindeki serbest oksalat parçalanır, kolonik emilim düşüktür, idrar oksalatı normal sınırlardadır.",
                    "Antibiyotik Sonrası O. formigenes Kaybı",
                    "Oksalat parçalanamaz, bağırsaktan pasif emilim artar, hiperoksalüri gelişir ve kalsiyum taşı riski katlanır.",
                    "Gereksiz antibiyotik kullanımı bağırsak taş koruyucu mikrobiyotasını kalıcı olarak tahrip edebilir."
                ),
                make_active_recall(
                    "Bağırsak lümeninde serbest oksalatı temel enerji kaynağı olarak parçalayarak insanı taştan koruyan simbiyotik bakteri hangisidir?",
                    "Oxalobacter formigenes bakterisidir.",
                    "Oksalat tüketen mikrobiyota üyesi"
                )
            ]
        },
        # Slayt 77
        {
            "slideNumber": 77,
            "title": "Primer Hiperoksalüri: Genetik Enzim Defektleri",
            "content": (
                "Primer hiperoksalüri (PH), karaciğer peroksizomlarında glioksilat metabolizmasında görevli enzimlerin otozomal "
                "resesif kalıtılan mutasyonları sonucu endojen oksalat üretiminin kontrolsüz arttığı ağır bir metabolik hastalıktır. "
                "Tip 1 PH, alanin:glioksilat aminotransferaz (AGXT) enzim eksikliğinden kaynaklanır; en sık (%80) ve en ağır tiptir. "
                "İdrar oksalat atılımı genellikle >100 mg/gün seviyesindedir. Erken çocuklukta tekrarlayan kalsiyum oksalat taşları "
                "ve nefrokalsinozis başlar; böbrek fonksiyonları bozulup GFR <30-40 mL/dk altına indiğinde kalsiyum oksalat "
                "böbrek dışı dokularda (kemik, retina, kalp, damarlar) birikerek öldürücü 'sistemik oksalozis' tablosuna yol açar. "
                "Tip 1 PH'ın nihai küratif tedavisi kombine karaciğer ve böbrek naklidir."
            ),
            "elements": [
                make_table(
                    "Primer Hiperoksalüri Tipleri ve Enzim Kusurları",
                    ["Tip", "Defektif Enzim", "Gen", "Klinik Seyir ve Tedavi"],
                    [
                        {
                            "cells": ["Tip 1 PH", "Alanin:glioksilat aminotransferaz (AGT)", "AGXT", "En ağır tip; sistemik oksalozis, kombine KC-böbrek nakli"],
                            "hiddenIndex": 1,
                            "hint": "Karaciğer peroksizomal transferazı"
                        },
                        {
                            "cells": ["Tip 2 PH", "Glioksilat/hidroksipirüvat redüktaz (GRHPR)", "GRHPR", "Daha ılımlı seyir; izole böbrek nakli genellikle yeterli"],
                            "hiddenIndex": 1,
                            "hint": "Redüktaz enzim eksikliği"
                        },
                        {
                            "cells": ["Tip 3 PH", "4-hidroksi-2-oksoglutarat aldolaz (HOGA)", "HOGA1", "En hafif form; böbrek yetmezliği gelişimi son derece nadir"],
                            "hiddenIndex": 0,
                            "hint": "En hafif mitokondriyal tip"
                        }
                    ]
                ),
                make_cloze(
                    "Primer hiperoksalüri Tip 1 olgularında karaciğerde eksik olan peroksizomal enzim alanin glioksilat aminotransferaz enzimidir.",
                    "alanin glioksilat aminotransferaz",
                    "AGXT geni tarafından kodlanan enzim"
                )
            ]
        },
        # Slayt 78
        {
            "slideNumber": 78,
            "title": "Enterik Hiperoksalüri: Yağ Asidi Sabunlaşması",
            "content": (
                "Enterik hiperoksalüri, yağ malabsorpsiyonuna yol açan gastrointestinal hastalıklarda (Crohn hastalığı, "
                "çölyak, kronik pankreatit, ince bağırsak rezeksiyonları ve Roux-en-Y gastrik bypass cerrahisi) gelişen "
                "özgül bir litogenez tablosudur. Normalde diyetteki serbest kalsiyum bağırsakta oksalat ile bağlanarak "
                "çözünmeyen kalsiyum oksalat oluşturur ve dışkıyla atılır. Ancak yağ malabsorpsiyonunda emilemeyen serbest "
                "yağ asitleri lümendeki kalsiyum ve magnezyuma bağlanarak 'sabunlaşır' (kalsiyum sabunları). Kalsiyum yağ "
                "tarafından tüketildiği için serbest kalan oksalat çözünür hale gelir; ayrıca emilmeyen safra tuzları ve "
                "yağ asitleri kolon mukozasının geçirgenliğini artırır. Serbest oksalat kolondan hızla emilerek masif "
                "hiperoksalüriye ve agresif kalsiyum oksalat taşlarına yol açar."
            ),
            "elements": [
                make_causal_chain(
                    "Yağ Malabsorpsiyonundan Enterik Hiperoksalüriye Uzanan Fizyopatoloji",
                    [
                        "1. Malabsorpsiyon: Crohn veya bypass cerrahisi sonucu bağırsak lümeninde yağ asitlerinin birikmesi",
                        "2. Sabunlaşma: Serbest yağ asitlerinin diyetteki kalsiyum ile birleşerek çözünmez sabunlar yapması",
                        "3. Oksalatın Serbestleşmesi: Kalsiyum bağlayıcısını kaybeden serbest oksalat konsantrasyonunun tırmanması",
                        "4. Kolonik Geçirgenlik Artışı: Safra tuzlarının kolon epitelini irrite ederek geçirgenliği artırması",
                        "5. Masif Absorpsiyon ve Litogenez: Kolondan aşırı emilen oksalatın idrarda şiddetli hiperoksalüri ve taş yapması"
                    ]
                ),
                make_active_recall(
                    "Bariatrik cerrahi veya Crohn hastalığında kalsiyumun yağ asitleriyle birleşerek oksalatı serbest bırakması sürecine ne ad verilir?",
                    "Kalsiyum sabunlaşması sürecidir.",
                    "Yağ ve kalsiyumun kimyasal sabunlaşması"
                )
            ]
        },
        # Slayt 79 [CHECKPOINT 8]
        {
            "slideNumber": 79,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Kalsiyum Taşlarının Patofizyolojisi",
            "content": (
                "Bu bölümde kalsiyum taşlarının patofizyolojisini, hiperkalsiüri, hiperoksalüri ve hiperürikozüri mekanizmalarını inceledik. "
                "Hiperkalsiüri en sık metabolik anormallik olup (>4 mg/kg/gün) absorptif, renal ve resorptif olarak ayrılır. "
                "Resorptif tipte primer hiperparatiroidi (yüksek PTH) mevcuttur; sarkoidozda ise kalsitriol yüksek ancak PTH baskılıdır. "
                "Hiperürikozüri (>700 mg/gün), epitaksi ve inhibitör adsorpsiyonu ile kalsiyum oksalat taşını provoke eder. "
                "Oxalobacter formigenes kolon florasında oksalatı tüketerek korur; antibiyotiklerle kaybı taş riskini artırır. "
                "Primer hiperoksalüri Tip 1, AGXT enzim eksikliğine bağlıdır; idrar oksalatı >100 mg/gün olup kombine KC-böbrek nakli gerektirir. "
                "Enterik hiperoksalüride (Crohn, bypass), yağ asitleri kalsiyumla sabunlaşır, serbest kalan oksalat kolondan emilerek taşlaşır."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp08-fc01",
                    "front": "Taş hastasında hiperkalsemi ile hiperkalsiürinin birlikte bulunduğu tabloda serum PTH'ı yüksekse tanı nedir?",
                    "back": "Primer hiperparatiroidi tablosudur.",
                    "hint": "Otonom paratiroid adenomu hastalığı"
                },
                {
                    "id": "k1-27-cp08-fc02",
                    "front": "Primer hiperoksalüri Tip 1 hastalığında karaciğer peroksizomlarında eksik olan otozomal resesif enzim hangisidir?",
                    "back": "Alanin glioksilat aminotransferaz enzimidir.",
                    "hint": "Hedef substratı glisine dönüştüren hepatik organel katalizörü"
                },
                {
                    "id": "k1-27-cp08-fc03",
                    "front": "Crohn veya gastrik bypass hastalarında yağ asitlerinin kalsiyumu bağlayarak oksalatı serbest bırakması mekanizmasına ne denir?",
                    "back": "Kalsiyum sabunlaşması reaksiyonudur.",
                    "hint": "Gastrointestinal yağ kökenli lüminal tuz kompleksi"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 8 Özet Tablosu: Kalsiyum Taşlarını Tetikleyen Kritik Eşikler",
                    ["Metabolik Bozukluk", "Tanısal Laboratuvar Eşiği", "En Sık Fizyopatolojik Neden"],
                    [
                        {
                            "cells": ["Hiperkalsiüri", "> 4 mg/kg/gün veya >250-300 mg/gün", "İdiyopatik absorptif / renal tübüler kaçak"],
                            "hiddenIndex": 1,
                            "hint": "Günlük kalsiyum atılım limiti"
                        },
                        {
                            "cells": ["Primer Hiperoksalüri", "> 100 mg/gün idrar oksalatı", "Karaciğer AGXT enzim mutasyonu"],
                            "hiddenIndex": 1,
                            "hint": "Aşırı endojen oksalat fazlalığı"
                        }
                    ]
                )
            ]
        },
        # Slayt 80
        {
            "slideNumber": 80,
            "title": "Klinik Karar: Distal Renal Tübüler Asidoz ve Kalsiyum Taşı",
            "content": (
                "Tip 1 (distal) renal tübüler asidoz (dRTA), toplayıcı tübüllerdeki alfa interkale hücrelerin lümene H+ iyonu "
                "pompalayamaması sonucu gelişen klasik bir kalsiyum fosfat ve nefrokalsinozis nedenidir. Hastalarda sistemik "
                "hiperkloremik hipokalemik metabolik asidoz bulunmasına rağmen, idrar pH'ı paradoksal olarak daima alkali "
                "(>6.5) kalır. Sistemik asidoz nedeniyle proksimal tübülde sitrat geri emilimi maksimuma çıkar; bu durum "
                "aşırı şiddetli hipositratüri (<50 mg/gün) ile sonuçlanır. Alkali idrar, hiperkalsiüri ve sıfıra yakın sitrat "
                "bir araya geldiğinde hızlı ve agresif kalsiyum fosfat (apatit ve bruşit) taşları ve nefrokalsinozis gelişir. "
                "Tedavide yüksek doz potasyum sitrat ile asidoz düzeltilmeli ve idrara sitrat kazandırılmalıdır."
            ),
            "elements": [
                make_branching_logic(
                    "24 yaşında kadın hasta, bilateral nefrokalsinozis ve tekrarlayan kalsiyum fosfat taşları ile başvuruyor. Kan gazında hiperkloremik metabolik asidoz (pH 7.28, HCO3 14 mEq/L), serum potasyumu 3.1 mEq/L (düşük), idrar pH'ı ise 6.8 (yüksek) ve idrar sitratı 30 mg/gün ölçülüyor.",
                    "Bu hastadaki taş oluşumunun altta yatan primer tübüler patolojisi ve temel medikal tedavisi ne olmalıdır?",
                    [
                        {
                            "text": "Distal renal tübüler asidoz (Tip 1 RTA); sistemik asidozu düzeltmek ve hipositratüriyi kırmak için yüksek doz potasyum sitrat replasmanı başlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; distal H+ sekresyon kusuru asidoz, yüksek idrar pH'ı ve şiddetli hipositratüri yapar; tedavi potasyum sitrattır."
                        },
                        {
                            "text": "Primer hiperaldosteronizm; acil adrenalektomi yapılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Primer aldosteronizmde metabolik alkaloz görülür, burada ise metabolik asidoz vardır."
                        },
                        {
                            "text": "İdrarı daha da alkalileştirmek için amonyum klorür testi yapılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Amonyum klorür asitleştirici tanı testidir, tedavi edici bir yaklaşım değildir."
                        }
                    ]
                )
            ]
        }
    ]
