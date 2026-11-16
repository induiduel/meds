# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 3: Boyut, Lokalizasyon ve Radyolojik Özellikler (Slayt 21 - 30)
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
            "title": "Taşların Boyut Sınıflaması ve Spontan Düşme Olasılığı",
            "content": (
                "Üriner sistem taşlarının klinik yönetimi ve girişimsel tedavi gereksinimi en büyük çap boyutuyla doğrudan "
                "ilişkilidir. Çapı 4 milimetrenin altındaki taşların yaklaşık %80'i medikal ekspulsif tedavi veya konservatif "
                "izlemle spontan olarak üreterden geçerek düşme potansiyeline sahiptir. Buna karşılık çapı 7 milimetrenin üzerine "
                "çıkan taşlarda spontan düşme oranı %20'nin altına iner; 10 milimetreyi aşan taşlarda ise cerrahi müdahale "
                "kaçınılmaz hale gelir. Taşın milimetrik boyutu, üreter lümen çapı ve üreter peristaltizminin kontraktil gücü "
                "arasındaki mekanik denge, taşın ilerlemesini veya üreter duvarında impakte kalarak obstrüksiyon yaratmasını belirler."
            ),
            "elements": [
                make_table(
                    "Taş Boyutuna Göre Spontan Pasaj ve Girişim İhtiyacı",
                    ["Taş Çapı (mm)", "Spontan Pasaj Olasılığı", "Ortalama Düşme Süresi", "Önerilen Yaklaşım"],
                    [
                        {
                            "cells": ["< 4 mm", "Yüksek (~%80)", "1 - 2 hafta", "Konservatif izlem, hidrasyon, analjezi"],
                            "hiddenIndex": 1,
                            "hint": "Yüksek spontan düşme yüzdesi"
                        },
                        {
                            "cells": ["4 - 6 mm", "Orta (~%50)", "2 - 4 hafta", "Medikal ekspulsif tedavi (alfa-bloker)"],
                            "hiddenIndex": 1,
                            "hint": "Yarı yarıya düşme ihtimali"
                        },
                        {
                            "cells": ["> 7 mm", "Düşük (<%20)", "Spontan pasaj nadir", "Endoürolojik cerrahi veya ESWL"],
                            "hiddenIndex": 3,
                            "hint": "Girişimsel tedavi endikasyonu"
                        }
                    ]
                ),
                make_cloze(
                    "Dört milimetrenin altındaki üreter taşlarında spontan pasaj şansı yüzde seksen seviyesine kadar ulaşmaktadır.",
                    "yüzde seksen",
                    "Oldukça yüksek başarı oranı"
                )
            ]
        },
        # Slayt 22
        {
            "slideNumber": 22,
            "title": "Anatomik Lokalizasyon: Kaliksler ve Renal Pelvis",
            "content": (
                "Böbrek içinde taşlar üst kaliks, orta kaliks, alt kaliks veya renal pelvis yerleşimli olabilir. "
                "Alt kaliks taşları, kaliks infundibulumunun dar olması, infundibulopelvik açının dar (akut) olması ve "
                "yerçekimi etkisi nedeniyle spontan temizlenme açısından en dezavantajlı gruptur. Renal pelvisi tamamen doldurup "
                "tüm majör ve minör kalikslere doğru dallanan kitlelere 'kısmi' veya 'tam koraliform' (staghorn) taş adı verilir. "
                "Staghorn taşlar tedavi edilmediğinde hidronefroz, kronik böbrek enfeksiyonu, renal parankim atrofisi ve sepsise "
                "yol açarak böbrek fonksiyonlarının geri dönüşsüz kaybına neden olur."
            ),
            "elements": [
                make_active_recall(
                    "Yerçekimi etkisi ve dar infundibulopelvik açı nedeniyle temizlenmesi en güç olan böbrek içi lokalizasyon neresidir?",
                    "Alt kaliks bölgesidir.",
                    "Böbreğin taban toplayıcı sistemi"
                ),
                make_before_after(
                    "Böbrek İçi Taş Yerleşimlerinin Temizlenme Dinamiği",
                    "Üst ve Orta Kaliks Taşları",
                    "Yerçekimi desteğiyle renal pelvise ve üretere geçiş göreceli kolaydır; ESWL sonrası parçaların dökülmesi hızlıdır.",
                    "Alt Kaliks Taşları",
                    "Akut infundibulopelvik açı ve yerçekimi aleyhine konum nedeniyle fragmanlar kaliks dibinde göllenir ve temizlenemez.",
                    "Alt kutup taşlarında infundibulum anatomisi girişim türünün seçiminde birincil kriterdir."
                )
            ]
        },
        # Slayt 23
        {
            "slideNumber": 23,
            "title": "Üreterik Anatomik Darlıklar ve İmpaksiyon",
            "content": (
                "Üreter boyunca taşların takılarak obstrüksiyona yol açtığı üç kritik fizyolojik darlık noktası bulunur. "
                "Birinci darlık, renal pelvisin üretere dönüştüğü üreteropelvik bileşkedir (UPJ - çapı ~2 mm). "
                "İkinci darlık, üreterin iliak damarları (arteria ve vena iliaca communis/externa) önden çaprazladığı pelvik "
                "kenar bölgesidir. Üçüncü ve en dar nokta ise üreterin mesane duvarından oblik olarak geçtiği üreterovezikal "
                "bileşkedir (UVJ - çapı 1-2 mm). Üreter taşlarının %60'ından fazlası UVJ seviyesinde takılmakta ve burada "
                "şiddetli üreter spazmına bağlı akut renal kolik atağını tetiklemektedir."
            ),
            "elements": [
                make_causal_chain(
                    "Taşın Üreter Boyunca İlerlemesi ve UVJ İmpaksiyonu",
                    [
                        "1. Pelvisten Çıkış: Taşın renal pelvisten ayrılarak UPJ'ye girmesi ve ilk mekanik dirençle karşılaşması",
                        "2. Abdominal Üreter Pasajı: Peristaltik dalgalarla psoas kası boyunca ilerleme",
                        "3. İliak Çapraz: Damar pulsasyonu ve pelvik kenar darlığından geçiş",
                        "4. UVJ Sıkışması: İntramural detrusor liflerinin en dar lümeninde takılma ve impaksiyon",
                        "5. Renal Kolik: Proksimal lümende basınç artışı, kapsül gerilmesi ve şiddetli nosiseptif ağrı"
                    ]
                ),
                make_cloze(
                    "Üreterin mesane içine girdiği en dar anatomik darlık noktası üreterovezikal bileşke olarak tanımlanır.",
                    "üreterovezikal bileşke",
                    "Mesane duvarı geçiş noktası"
                )
            ]
        },
        # Slayt 24
        {
            "slideNumber": 24,
            "title": "Mesane Taşları: Primer ve Sekonder Nedenler",
            "content": (
                "Mesane taşları üriner taşların yaklaşık %5'ini oluşturur ve çoğunlukla erkek popülasyonda gözlenir. "
                "Etiyolojik olarak primer ve sekonder olmak üzere ikiye ayrılır. Primer mesane taşları, altta yatan bir "
                "obstrüksiyon olmaksızın, yetersiz protein ve süt tüketimi olan çocuklarda dehidratasyon ve beslenme "
                "bozukluğuna bağlı gelişen amonyum ürat taşlarıdır. Sekonder mesane taşları ise erişkinlerde çok daha sıktır; "
                "benign prostat hiperplazisi (BPH), üretra darlığı veya nörojenik mesane nedeniyle gelişen infravezikal "
                "obstrüksiyon ve idrar stazı zemininde enfeksiyon ve kristal birikimiyle meydana gelir."
            ),
            "elements": [
                make_table(
                    "Primer ve Sekonder Mesane Taşlarının Karşılaştırması",
                    ["Özellik", "Primer Mesane Taşı", "Sekonder Mesane Taşı"],
                    [
                        {
                            "cells": ["Hedef Popülasyon", "Gelişmekte olan ülkelerdeki çocuklar", "Yaşlı erkek hastalar (BPH zemininde)"],
                            "hiddenIndex": 2,
                            "hint": "İleri yaş erkeklerde prostatik zemin"
                        },
                        {
                            "cells": ["Temel Patogenez", "Beslenme bozukluğu, düşük fosfat/protein", "İnfravezikal obstrüksiyon, idrar stazı"],
                            "hiddenIndex": 2,
                            "hint": "Mesane çıkım tıkanıklığı"
                        },
                        {
                            "cells": ["Yaygın Taş Tipi", "Amonyum ürat ve ürik asit", "Kalsiyum oksalat veya strüvit"],
                            "hiddenIndex": 1,
                            "hint": "Pediatrik malnütrisyon taşı"
                        }
                    ]
                ),
                make_active_recall(
                    "Yaşlı erkeklerde sekonder mesane taşı gelişimine zemin hazırlayan en yaygın altta yatan patoloji nedir?",
                    "Benign prostat hiperplazisine bağlı mesane çıkım obstrüksiyonu ve stazdır.",
                    "Prostat büyümesi tıkanıklığı"
                )
            ]
        },
        # Slayt 25
        {
            "slideNumber": 25,
            "title": "Radyolojik Özellikler: Radyoopak Taşlar",
            "content": (
                "Üriner taşların direkt üriner sistem grafisinde (DÜSG) görünürlüğü, içerdikleri kimyasal elementlerin "
                "atom numarasına ve kristalin moleküler yoğunluğuna bağlıdır. Kalsiyum (atom numarası 20) ve fosfor "
                "(atom numarası 15) yüksek elektron yoğunluğuna sahip olduklarından X-ışınlarını kuvvetle absorbe ederler. "
                "Bu nedenle kalsiyum oksalat monohidrat, kalsiyum oksalat dihidrat, kalsiyum fosfat ve bruşit taşları "
                "kemik dansitesine yakın parlak beyaz gölgeler olarak DÜSG'de net biçimde seçilir. Bu taşlar 'belirgin radyoopak' "
                "olarak sınıflandırılır ve konvansiyonel grafilerle kolaylıkla takip edilebilir."
            ),
            "elements": [
                make_cloze(
                    "İçerdikleri kalsiyum elementi nedeniyle X-ışınlarını güçlü şekilde soğuran kalsiyum taşları belirgin radyoopak karakter sergiler.",
                    "belirgin radyoopak",
                    "Radyografide net beyaz görünen"
                ),
                make_micro_quiz(
                    "Aşağıdaki taş bileşenlerinden hangisi direkt grafide en yüksek radyoopasiteye sahiptir?",
                    [
                        {
                            "text": "Kalsiyum fosfat ve kalsiyum oksalat",
                            "isCorrect": True,
                            "explanation": "Doğrudur; kalsiyumun yüksek atom numarası nedeniyle en opak taşlardır."
                        },
                        {
                            "text": "Saf ürik asit",
                            "isCorrect": False,
                            "explanation": "Ürik asit karbon, hidrojen ve azottan oluşur; tamamen radyolüsendir."
                        },
                        {
                            "text": "Ksantin",
                            "isCorrect": False,
                            "explanation": "Ksantin direkt grafide görünmez, radyolüsendir."
                        },
                        {
                            "text": "İndinavir",
                            "isCorrect": False,
                            "explanation": "İndinavir organik bir proteaz inhibitörüdür, grafide hiç görünmez."
                        }
                    ],
                    "Kalsiyum tuzları konvansiyonel grafilerde en yüksek opasiteyi verir."
                )
            ]
        },
        # Slayt 26
        {
            "slideNumber": 26,
            "title": "Zayıf Radyoopak Taşlar: Strüvit ve Sistin",
            "content": (
                "Magnezyum amonyum fosfat (strüvit), karbonat apatit ve sistin taşları 'zayıf radyoopak' (semi-opak) "
                "taşlar kümesini oluşturur. Strüvit taşlarında magnezyum ve fosfor bulunmakla birlikte, amonyum ve su moleküllerinin "
                "varlığı kalsiyum taşlarına kıyasla X-ışını absorbsiyonunu düşürür; bu nedenle buzlu cam (ground-glass) veya "
                "hafif silik dansite verirler. Sistin molekülü ise bünyesinde kükürt atomları (atom numarası 16) barındırır. "
                "Kükürt atomları sistine hafif-orta derecede bir radyoopasite kazandırır ve homojen, düzgün sınırlı, balmumu "
                "benzeri bir gölge oluşturmasını sağlar. Bu taşlar bağırsak gazlarının arkasında kolaylıkla gözden kaçabilir."
            ),
            "elements": [
                make_table(
                    "Radyolojik Opasite Derecelerine Göre Taş Sınıflaması",
                    ["Opasite Düzeyi", "Taş Tipleri", "Fiziksel / Kimyasal Neden"],
                    [
                        {
                            "cells": ["Radyoopak", "Kalsiyum oksalat (mono/dihidrat), Kalsiyum fosfatlar", "Kalsiyumun yüksek atom ağırlığı"],
                            "hiddenIndex": 1,
                            "hint": "En yaygın inorganik kalsiyum kalkülleri"
                        },
                        {
                            "cells": ["Zayıf Radyoopak", "Strüvit, karbonat apatit, sistin", "Magnezyum varlığı veya sistindeki kükürt atomları"],
                            "hiddenIndex": 1,
                            "hint": "Enfeksiyon ve aminoasit taşı grubu"
                        },
                        {
                            "cells": ["Radyolüsen", "Ürik asit, amonyum ürat, ksantin, 2,8-DHA, ilaçlar", "Düşük atom numaralı organik yapı (C, H, O, N)"],
                            "hiddenIndex": 0,
                            "hint": "Grafide hiç seçilmeyen grup"
                        }
                    ]
                ),
                make_active_recall(
                    "Sistin taşlarının direkt grafide zayıf radyoopak görünmesini sağlayan moleküler bileşen nedir?",
                    "Sistin amino asidinin yapısında bulunan kükürt atomlarıdır.",
                    "Sülfür elementi varlığı"
                )
            ]
        },
        # Slayt 27
        {
            "slideNumber": 27,
            "title": "Radyolüsen Taşlar: Ürik Asit ve Organik Kalküller",
            "content": (
                "Radyolüsen taşlar, direkt üriner sistem grafisinde (DÜSG) hiçbir gölge vermeyen ve tamamen görünmez "
                "olan kalküllerdir. Bu grupta saf ürik asit, amonyum ürat, ksantin, 2,8-dihidroksiadenin ve indinavir gibi "
                "doğrudan çöken ilaç taşları yer alır. Bu bileşikler karbon, hidrojen, oksijen ve azot gibi düşük atom "
                "numarasına sahip hafif elementlerden oluştukları için X-ışınlarını yumuşak doku veya idrar ile aynı oranda "
                "geçirirler. Radyolüsen bir taş obstrüksiyon yaptığında DÜSG tamamen normal görülebilir; tanı ancak "
                "ultrasonografide akustik gölgelenme veya kontrassız bilgisayarlı tomografide hiperdans kitlenin görülmesiyle konur."
            ),
            "elements": [
                make_cloze(
                    "Karbon ve azot gibi hafif atomlardan oluşan saf ürik asit taşları direkt radyografide bütünüyle radyolüsen izlenir.",
                    "radyolüsen",
                    "X-ışınını tutmayan şeffaf görünüm"
                ),
                make_before_after(
                    "Radyoopak vs Radyolüsen Taşın Tanısal Görüntülenmesi",
                    "Radyoopak Taş (CaOx)",
                    "DÜSG'de kemik gibi beyaz görünür, skopi altında ESWL uygulanabilir, takipte ucuz konvansiyonel grafi yeterlidir.",
                    "Radyolüsen Taş (Ürik Asit)",
                    "DÜSG'de tamamen görünmez, skopiyle takip edilemez, tanı için kontrassız BT ve ultrasonografi zorunludur.",
                    "DÜSG negatifliği akut kolikli bir hastada taş tanısını asla dışlamaz."
                )
            ]
        },
        # Slayt 28
        {
            "slideNumber": 28,
            "title": "Görüntüleme Yöntemleri: Ultrason, DÜSG ve Düşük Doz BT",
            "content": (
                "Ürolitiyazis şüphesinde günümüzdeki altın standart görüntüleme yöntemi 'kontrassız düşük doz helikal "
                "bilgisayarlı tomografi'dir (BT). Kontrassız BT, ürik asit ve sistin dahil olmak üzere indinavir hariç tüm "
                "taş tiplerini (%99 duyarlılık ve özgüllükle) milimetrik olarak tespit eder; ayrıca taşın Hounsfield ünitesi "
                "(HU) değerini ölçerek taş sertliği ve kimyasal bileşimi hakkında tahmin yapılmasına olanak tanır. "
                "Ultrasonografi (USG) ise radyasyonsuz olması nedeniyle gebelerde ve çocuklarda ilk seçenektir; taşın arkasında "
                "posterior akustik gölge ve renkli Doppler'de 'twinkling' (parlama) artefaktı oluşturarak tanı koydurur."
            ),
            "elements": [
                make_micro_quiz(
                    "Hemen hemen tüm taş tiplerini yüksek duyarlılıkla saptayan ve altın standart kabul edilen görüntüleme yöntemi hangisidir?",
                    [
                        {
                            "text": "Kontrassız helikal bilgisayarlı tomografi",
                            "isCorrect": True,
                            "explanation": "Doğrudur; indinavir dışındaki tüm taşları HU dansitesiyle net olarak gösterir."
                        },
                        {
                            "text": "İntravenöz piyelografi (İVP)",
                            "isCorrect": False,
                            "explanation": "Kontrast nefrotoksisitesi ve düşük duyarlılık nedeniyle altın standart değildir."
                        },
                        {
                            "text": "Manyetik rezonans ürografi (MRÜ)",
                            "isCorrect": False,
                            "explanation": "Kalsiyum sinyal vermediği için taş saptamada BT'den çok daha zayıftır."
                        },
                        {
                            "text": "Yalnızca direkt üriner sistem grafisi",
                            "isCorrect": False,
                            "explanation": "Radyolüsen taşları (%10) tamamen kaçırır, duyarlılığı düşüktür."
                        }
                    ],
                    "Kontrassız BT günümüzde üriner sistem taşlarının kesin referans görüntüleme modalitesidir."
                ),
                make_active_recall(
                    "Ultrasonografide renkli Doppler uygulandığında taş yüzeyindeki akustik yansımalara bağlı görülen tipik artefakt nedir?",
                    "Twinkling (parlama veya pırıltı) artefaktıdır.",
                    "Renkli mozaik eko deseni"
                )
            ]
        },
        # Slayt 29 [CHECKPOINT 3]
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Lokalizasyon ve Radyolojik Özellikler",
            "content": (
                "Bu bölümde taşların boyut dinamiklerini, anatomik impaksiyon alanlarını ve radyolojik sınıflamasını özetledik. "
                "Dört milimetrenin altındaki taşlar %80 oranında spontan pasajla atılırken, 7 milimetrenin üzerindeki taşlar girişim gerektirir. "
                "Böbrek içinde alt kaliks taşları dar açı ve yerçekimi etkisiyle en zor temizlenen lokalizasyondur. "
                "Üreterde taş impaksiyonu en sık üreterovezikal bileşke (UVJ) düzeyinde meydana gelir. "
                "Mesane taşları yaşlı erkeklerde prostat hiperplazisine bağlı sekonder stazla sıklıkla gelişir. "
                "Kalsiyum içeren taşlar belirgin radyoopaktır; strüvit ve sistin zayıf radyoopak, saf ürik asit ise radyolüsendir. "
                "Kontrassız düşük doz helikal BT, ürolitiyaziste altın standart görüntüleme yöntemi olup taşa ait dansiteyi (HU) tam verir."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp03-fc01",
                    "front": "Spontan pasaj olasılığı yüzde seksen olan, konservatif izleme en uygun taş çapı sınırı kaç milimetredir?",
                    "back": "Dört milimetre altındaki kitlelerdir.",
                    "hint": "En ufak çap basamağı"
                },
                {
                    "id": "k1-27-cp03-fc02",
                    "front": "Üreter boyunca taşların en sık takılarak akut renal kolik atağına yol açtığı en dar anatomik geçiş noktası neresidir?",
                    "back": "Üreterovezikal bileşke bölgesidir.",
                    "hint": "İntramural detrusor içi darlık"
                },
                {
                    "id": "k1-27-cp03-fc03",
                    "front": "Hafif atomlardan oluştuğu için konvansiyonel direkt grafide hiçbir gölge vermeyen saf radyolüsen taş türü nedir?",
                    "back": "Ürik asit kaynaklı kalküllerdir.",
                    "hint": "Asidik idrarda çöken pürin metaboliti"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 3 Özet Tablosu: Radyolojik Görünüm ve Boyut Kriterleri",
                    ["Parametre", "Kritik Değer / Tanım", "Klinik Önemi"],
                    [
                        {
                            "cells": ["Spontan Pasaj Eşiği", "< 4 mm (~%80 düşme)", "Medikal takip ve konservatif tedavi"],
                            "hiddenIndex": 1,
                            "hint": "Düşme ihtimali en yüksek aralık"
                        },
                        {
                            "cells": ["Radyolüsen Taş", "Ürik asit / Ksantin", "DÜSG'de saptanamaz, BT veya USG şarttır"],
                            "hiddenIndex": 1,
                            "hint": "Grafide şeffaf kalan kalkül"
                        }
                    ]
                )
            ]
        },
        # Slayt 30
        {
            "slideNumber": 30,
            "title": "Klinik Karar: Akut Kolik Olgusunda Görüntüleme Protokolü",
            "content": (
                "Acil servise ani başlayan, kasığa vuran şiddetli sol yan ağrısı ve mikroskobik hematüri ile başvuran "
                "hastada ilk tanısal basamak klinik durumun ve hemodinamik tablonun stabilizasyonudur. Hasta gebe değilse "
                "ve nefrotoksisite riski yoksa, kontrastsız düşük doz abdominal BT ilk tercih olarak planlanmalıdır. "
                "Kontrassız BT sayesinde taşın milimetrik boyutu, tam lokalizasyonu, hidronefrozun evresi ve perinefritik "
                "sıvı sızıntısı hızla ortaya konur. Eğer hasta gebe ise ilk basamakta kesinlikle ultrasonografi kullanılmalı, "
                "direkt grafi ve bilgisayarlı tomografinin iyonize radyasyon riskinden kaçınılmalıdır."
            ),
            "elements": [
                make_branching_logic(
                    "26 yaşında 18 haftalık gebe kadın hasta, sağ böbrek lojunda şiddetli kıvrandırıcı ağrı ve bulantı ile acil servise getiriliyor. İdrar tahlilinde bol eritrosit saptanıyor.",
                    "Fetusun radyasyon güvenliğini korurken akut obstrüktif ürolitiyazis tanısını koymak için hangi modalite seçilmelidir?",
                    [
                        {
                            "text": "İlk seçenek olarak obstetrik ve renal ultrasonografi uygulanmalı, böbrekte dilatasyon ve varsa taş aranmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; ultrasonografi iyonize radyasyon içermediği için gebelerde birinci basamak tanı aracıdır."
                        },
                        {
                            "text": "Kontrassız çok kesitli tüm batın tomografisi çekilmelidir.",
                            "isCorrect": False,
                            "explanation": "Gebelikte tomografi yüksek radyasyon nedeniyle ancak USG yetersiz kaldığında ve çok zorunlu hallerde düşünülür."
                        },
                        {
                            "text": "Radyoopak taşları görmek için acil direkt üriner sistem grafisi (DÜSG) çekilmelidir.",
                            "isCorrect": False,
                            "explanation": "DÜSG fetal radyasyon riski taşır ve gebelikte ilk tercih olamaz."
                        }
                    ]
                )
            ]
        }
    ]
