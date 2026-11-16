# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 9: Kanser Epidemiyolojisi, Çevresel/Mesleki Karsinojenler ve Kronik İnflamasyon Zeminleri (Slayt 81 - 90)
Checkpoint: Slayt 89
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_9_slides():
    return [
        # Slayt 81
        {
            "slideNumber": 81,
            "title": "Kanser Epidemiyolojisi: Küresel ve Ulusal Boyut",
            "content": (
                "Kanser epidemiyolojisi, malign neoplazmların sıklığını, coğrafi dağılımını ve etiyolojik "
                "risk faktörlerini inceleyerek koruyucu tıp stratejilerinin temelini oluşturur. Küresel "
                "ölçekte kardiyovasküler hastalıklardan sonra en sık ikinci ölüm nedeni kanserdir. Erkeklerde "
                "en sık saptanan yeni vaka prostat kanseri iken, kadınlarda en yüksek insidansa sahip "
                "tümör meme karsinomudur. Buna karşılık, hem erkeklerde hem de kadınlarda kansere bağlı "
                "mortalite listesinin zirvesinde açık ara **akciğer kanseri** yer almaktadır. Son dekadlarda "
                "gelişmiş ülkelerde tütün kullanımının azalması ve erken tarama protokollerinin (kolonoskopi, "
                "mamografi, Pap smear) yaygınlaşması sayesinde kolon, serviks ve mide kanseri mortalitesinde "
                "belirgin düşüşler kaydedilmiştir. Ancak obezite ve sedanter yaşam tarzı gibi metabolik "
                "risk faktörlerinin artışıyla ilişkili endometrial ve pankreatik karsinom sıklığı yükselmektedir. "
                "Epidemiyolojik veriler, neoplastik dönüşümün multifaktöriyel doğasını net biçimde kanıtlar."
            ),
            "elements": [
                make_cloze(
                    "Hem erkek hem de kadın popülasyonda kansere bağlı mortalitede birinci sırada yer alan organ akciğerdir.",
                    "akciğerdir",
                    "Toraks içi solunum parankimi"
                ),
                make_table(
                    "Cinsiyete Göre En Sık Görülen Kanser İstatistiği",
                    ["Parametre", "Erkek Popülasyon", "Kadın Popülasyon", "Ortak Lider"],
                    [
                        {
                            "cells": ["En Sık İnsidans (Yeni Vaka)", "Prostat bezi karsinomu", "Meme bezi karsinomu", "Değişken organ profili"],
                            "hiddenIndex": 1,
                            "hint": "Pelvik pelis erkek genital organı"
                        },
                        {
                            "cells": ["En Yüksek Mortalite (Ölüm)", "Bronkojenik tümör", "Bronkojenik tümör", "Akciğer malignitesi"],
                            "hiddenIndex": 3,
                            "hint": "Solunum yolları epitelyal kökeni"
                        }
                    ]
                )
            ]
        },

        # Slayt 82
        {
            "slideNumber": 82,
            "title": "Coğrafi Dağılım ve Göçmen Çalışmaları",
            "content": (
                "Kanser türlerinin dünya genelindeki insidans oranları dramatik coğrafi varyasyonlar sergiler. "
                "Örneğin mide adenokarsinomu Japonya'da Amerika Birleşik Devletleri'ne kıyasla yaklaşık 7-8 kat "
                "daha sık görülürken; Batı ülkelerinde kolon, meme ve prostat kanseri oranları Asya ülkelerine "
                "göre katbekat yüksektir. Bu dramatik farkların kalıtsal mı yoksa eksojen çevresel etkenlere "
                "mi bağlı olduğunu çözmenin en güçlü epidemiyolojik aracı **göçmen çalışmalarıdır**. Japonya'dan "
                "Amerika'ya göç eden birinci kuşak bireylerde kendi ülkelerinin tümör paterni sürerken; ikinci ve "
                "üçüncü kuşak torunlarda mide kanseri riski hızla düşerek ABD ortalamasına inmekte, buna karşılık "
                "kolon ve meme karsinomu insidansı yerel Amerikan nüfusu düzeyine fırlamaktadır. Bu olgu, "
                "spesifik neoplazmların etiyolojisinde genetik mirastan ziyade beslenme, tütsülenmiş gıdalar, "
                "obezite ve enfeksiyöz ajanlar gibi çevresel maruziyetlerin belirleyici rol oynadığını gösterir."
            ),
            "elements": [
                make_before_after(
                    "Göçmen Kuşaklarında Kanser İnsidansı Dönüşümü",
                    "Japonya'da Yaşayan Nüfus",
                    "Tütsülenmiş balık, yüksek tuz ve H. pylori nedeniyle çok yüksek mide kanseri oranı.",
                    "ABD'ye Göç Eden 2. ve 3. Kuşak",
                    "Mide kanseri riski yerel düzeye gerilerken, batı tipi diyetle kolon ve meme kanseri hızla artar.",
                    "Karsinogenezde çevresel ve diyetetik faktörlerin genetik kökene baskın gelebildiğinin kanıtıdır."
                ),
                make_active_recall(
                    "Göçmen çalışmalarında yeni nesillerde kanser paterninin değişmesi hangi etiyolojik gerçeği kanıtlar?",
                    "Kanser patogenezinde çevresel faktörler ve yaşam tarzı maruziyetlerinin kalıtsal arka plandan daha baskın olduğunu kanıtlar.",
                    "Eksojen değişkenlerin genoma üstünlüğü"
                )
            ]
        },

        # Slayt 83
        {
            "slideNumber": 83,
            "title": "Çevresel Karsinojenler: Tütün, Alkol ve Diyet Sinerjisi",
            "content": (
                "İnsan kanserlerinin yaklaşık %80-90'ı eksojen çevresel faktörlerin ve yaşam tarzı alışkanlıklarının "
                "uzun süreli etkisiyle tetiklenir. **Tütün dumanı**, içerdiği polisiklik aromatik hidrokarbonlar, "
                "nitrozaminler ve aromatik aminler nedeniyle tek başına akciğer, larinks, farinks, özofagus, "
                "pankreas ve mesane karsinomlarının majör etiyolojik sorumlusudur. **Alkol tüketimi** ise "
                "özellikle hepatosellüler karsinom (siroz üzerinden), oral kavite, larinks ve meme kanseri "
                "riskini katlar. Tütün ve alkol birlikte tüketildiğinde oral kavite, larinks ve özofagus "
                "skuamöz karsinom riskinde basit bir toplamsal etki değil, **katlanarak artan sinerjik** bir risk "
                "artışı ortaya çıkar. Alkol, karsinojenik kimyasalların mukoza epiteline penetrasyonunu artıran "
                "bir solvent gibi davranırken, hepatik sitokrom P450 enzim sistemlerini indükleyerek prokarsinojenlerin "
                "aktif elektrofilik DNA hasarlayıcı metabolitlere dönüşümünü belirgin biçimde hızlandırır."
            ),
            "elements": [
                make_causal_chain(
                    "Tütün ve Alkol Birlikteliğinde Sinerjik Epitelyal Karsinogenez Zinciri",
                    [
                        "1. Solvent Etkisi: Etanol mukozal epitelyal geçirgenliği artırarak tütün karsinojenlerinin hücreye girişini kolaylaştırır.",
                        "2. Enzimatik Aktivasyon: Sitokrom P450 izoformları indüklenerek tütün prokarsinojenleri reaktif elektrofillere çevrilir.",
                        "3. DNA Katkısı Oluşumu: Benzopiren diol epoksit ve asetaldehit guanin bazlarına kovalent bağlanarak aduklar kurar.",
                        "4. Replikatif Mutasyon: Onarım sınırını aşan transisyon ve transversiyon mutasyonları TP53 genini inaktive eder.",
                        "5. Neoplastik Transformasyon: Skuamöz epitelde premalign displazi tablosu derinleşerek invaziv karsinoma evrilir."
                    ]
                ),
                make_micro_quiz(
                    "Tütün dumanı maruziyetine ek olarak düzenli etanol tüketiminin oral kavite ve üst solunum-sindirim yolu skuamöz karsinom riskini katlamasının temel mekanizması nedir?",
                    [
                        {
                            "key": "A",
                            "text": "Alkolün direkt olarak timin dimerleri oluşturması ve nükleotid onarımını tamamen durdurması",
                            "isCorrect": False,
                            "explanation": "Timin dimerleri alkol tarafından değil, ultraviyole radyasyon tarafından meydana getirilir."
                        },
                        {
                            "key": "B",
                            "text": "Alkolün mukozal geçirgenliği artırarak tütün karsinojenlerinin penetrasyonunu ve sitokrom aracılı metabolik aktivasyonunu sinerjik hızlandırması",
                            "isCorrect": True,
                            "explanation": "Alkol mukozal bariyeri zayıflatan bir solvent gibi davranır ve mikrozomal P450 aktivasyonuyla prokarsinojenleri aktifleştirerek sinerjik hasar oluşturur."
                        },
                        {
                            "key": "C",
                            "text": "Etanolün DNA polimeraz aktivitesini artırarak protoonkogen amplifikasyonuna yol açması",
                            "isCorrect": False,
                            "explanation": "Etanol DNA polimeraz amplifikasyonuyla direkt onkogen kopya sayısı artışı yapmaz."
                        },
                        {
                            "key": "D",
                            "text": "Alkolün Langerhans hücrelerini öldürerek tip 1 hipersensitiviteyi tetiklemesi",
                            "isCorrect": False,
                            "explanation": "Langerhans hücre kaybı ve tip 1 hipersensitivite malign neoplazi mekanizması değildir."
                        }
                    ],
                    "Alkol ve tütünün ortak kullanımı oral ve özofageal skuamöz karsinom riskinde çarpan etkisiyle sinerji oluşturur."
                )
            ]
        },

        # Slayt 84
        {
            "slideNumber": 84,
            "title": "Mesleki Karsinojenler: Asbest, Benzen ve Vinil Klorür",
            "content": (
                "Endüstriyel iş kollarında çalışan personelin maruz kaldığı kimyasal ve fiziksel ajanlar, "
                "öngörülebilir hedef organlarda özgül neoplazmların gelişmesine yol açar. **Asbest lifleri** "
                "(özellikle amfibol formları), madencilik, gemi yapımı, yalıtım ve fren balatası sektörlerinde "
                "maruziyet sonucu akciğer karsinomu ve plevral/peritoneal **malign mezotelyoma** riskini muazzam "
                "ölçüde artırır. Asbest maruziyeti olan bir birey sigara da içiyorsa, akciğer kanseri riski "
                "yaklaşık 50-60 katına katlanır. **Benzen**, boya, yapıştırıcı ve petrol rafinerilerinde çalışanlarda "
                "kemik iliği hematopoezini bozarak aplastik anemi ve özellikle **akut miyeloid lösemi (AML)** "
                "tablosuna zemin hazırlar. Plastik endüstrisinde polivinil klorür (PVC) sentezinde kullanılan "
                "**vinil klorür monomeri** ise karaciğerde son derece nadir görülen agresif bir vasküler endotelyal "
                "malignite olan **hepatik anjiyosarkom** gelişimine neden olan klasik mesleki ajandır."
            ),
            "elements": [
                make_table(
                    "Klasik Mesleki Karsinojenler ve Karakteristik Maligniteler",
                    ["Mesleki Karsinojen", "Sık Maruziyet Sektörü", "Karakteristik Hedef Malignite", "Önemli Klinik Özellik"],
                    [
                        {
                            "cells": ["Asbest lifleri", "Yalıtım, tersane, fren balatası", "Malign Mezotelyoma ve Akciğer Ca", "Sigara ile çarpıcı sinerji"],
                            "hiddenIndex": 2,
                            "hint": "Plevra mezotel kaynaklı agresif neoplazm"
                        },
                        {
                            "cells": ["Benzen buharı", "Boya, yapıştırıcı, solvent endüstrisi", "Akut Miyeloid Lösemi (AML)", "Miyelotoksik kemik iliği hasarı"],
                            "hiddenIndex": 2,
                            "hint": "Granülositik seri hematolojik malignite"
                        },
                        {
                            "cells": ["Vinil klorür", "PVC plastik imalatı ve polimerizasyon", "Hepatik Anjiyosarkom", "Endotelyal agresif vasküler tümör"],
                            "hiddenIndex": 2,
                            "hint": "Karaciğer damar endotelinden türeyen tümör"
                        }
                    ]
                ),
                make_cloze(
                    "Plastik sanayisinde PVC üretiminde çalışan işçilerde karaciğerde görülen karakteristik malign endotelyal tümör anjiyosarkomdur.",
                    "anjiyosarkomdur",
                    "Damar endoteli kaynaklı hepatik sarkom türü"
                )
            ]
        },

        # Slayt 85
        {
            "slideNumber": 85,
            "title": "Mesleki ve Çevresel Toksinler: Ağır Metaller ve Radon",
            "content": (
                "Ağır metaller ve çevresel radyasyon kaynakları, DNA tamir mekanizmalarını bozarak ve reaktif "
                "oksijen radikalleri (ROS) üreterek karsinogenezi indükler. **Arsenik**, pestisitler, kontamine "
                "yeraltı suları ve metal ergitme tesislerinde maruz kalınan bir toksindir; karakteristik olarak "
                "avuç içi ve ayak tabanlarında hiperkeratoz, ciltte **skuamöz hücreli karsinom** ve **bazal hücreli "
                "karsinom**, ayrıca akciğer karsinomuna yol açar. **Krom (özellikle hekzahidrik bileşikler)** ve "
                "**nikel**, paslanmaz çelik üretimi, elektrokaplama ve kaynak işlerinde solunum yolu epiteline "
                "sitotoksik hasar vererek nazofarenks ve **akciğer bronş karsinomu** riskini katlar. Doğada uranyum "
                "parçalanma ürünü olan radyoaktif soy gaz **radon**, maden ocaklarında ve iyi havalandırılmayan "
                "bina bodrumlarında birikerek alfa parçacıkları yayar. Sigara içmeyen bireylerde gelişen "
                "akciğer kanserinin en sık çevresel sebebi radyoaktif radon gazı inhalasyonudur."
            ),
            "elements": [
                make_active_recall(
                    "Sigara içmeyen bireylerde akciğer karsinomuna yol açan en önemli çevresel ve konutsal radyoaktif ajan hangisidir?",
                    "Uranyum bozunumu sonucu bodrum katlarında biriken ve alfa ışıması yayan radon gazıdır.",
                    "Toprak altı izotop salınımı"
                ),
                make_cloze(
                    "Kontamine kuyu suyu ve pestisit maruziyetiyle avuç içlerinde palmar hiperkeratoz ve cilt karsinomlarına yol açan ağır metal arseniktir.",
                    "arseniktir",
                    "Toksik kuyu suyu elementi"
                )
            ]
        },

        # Slayt 86
        {
            "slideNumber": 86,
            "title": "Yaş Faktörü ve Çocukluk Çağı Maligniteleri",
            "content": (
                "Kanser insidansı genel olarak yaşla birlikte katlanarak artar; olguların büyük kısmı 55 yaş "
                "üzerinde saptanır. Yaşlanmayla birlikte kanser sıklığının artması iki temel mekanizmaya dayanır: "
                "onkojenik somatik mutasyonların zaman içinde genomda kümülatif birikimi ve yaşlanan immün sistemin "
                "(immünosenesans) neoplastik hücreleri tanıyıp elimine etme kapasitesinin zayıflaması. Buna "
                "karşılık kanser, çocukluk çağında (özellikle 1-14 yaş) travma sonrası en sık ikinci ölüm nedenidir. "
                "Ancak çocukluk çağı kanserlerinin histogenetik profili erişkinlerden tamamen farklıdır. Erişkinlerde "
                "epitelyal kökenli karsinomlar baskınken; pediyatrik yaş grubunda hematopoetik sistem neoplazmları "
                "(özellikle akut lenfoblastik lösemi - ALL), santral sinir sistemi tümörleri ve embriyonik "
                "primitif mezenşimden köken alan **blastik tümörler (küçük yuvarlak mavi hücreli neoplazmlar)** "
                "görülür. Wilms tümörü (nefroblastom), nöroblastom, retinoblastom ve rabdomyosarkom bu primitif "
                "pediyatrik tümörlerin en karakteristik örnekleridir."
            ),
            "elements": [
                make_before_after(
                    "Yaş Gruplarına Göre Kanserlerin Histogenetik Dağılımı",
                    "Erişkin Çağı Maligniteleri (>55 Yaş)",
                    "Çoğunlukla karsinomlar (akciğer, meme, prostat, kolon). Uzun süreli karsinojen maruziyeti ve mutasyon birikimi hakimdir.",
                    "Çocukluk Çağı Maligniteleri (0-14 Yaş)",
                    "Lösemiler (ALL), lenfomalar, SSS tümörleri ve blastik primitif mezenkimal/nöroektodermal tümörler hakimdir.",
                    "Çocukluk çağı tümörleri çevresel karsinojenlerden ziyade gelişimsel/embriyonik genetik anomalilerle ilişkilidir."
                ),
                make_micro_quiz(
                    "Pediyatrik popülasyonda (çocukluk çağı) en sık saptanan malign neoplazm grubu aşağıdakilerden hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Akciğer skuamöz hücreli karsinomu",
                            "isCorrect": False,
                            "explanation": "Akciğer skuamöz karsinomu ileri yaş ve uzun süreli sigara maruziyetiyle gelişen erişkin tümörüdür."
                        },
                        {
                            "key": "B",
                            "text": "Akut lenfoblastik lösemi (ALL) ve santral sinir sistemi neoplazmları",
                            "isCorrect": True,
                            "explanation": "Pediyatrik malignitelerin başında akut lösemiler (özellikle ALL) ve beyin/santral sinir sistemi tümörleri gelir."
                        },
                        {
                            "key": "C",
                            "text": "Mide taşlı yüzük hücreli adenokarsinomu",
                            "isCorrect": False,
                            "explanation": "Mide adenokarsinomu erişkin ve ileri yaş epitel malignitesidir."
                        },
                        {
                            "key": "D",
                            "text": "Prostat asiner adenokarsinomu",
                            "isCorrect": False,
                            "explanation": "Prostat kanseri yaşlı erkek populasyonunun tipik neoplazmıdır."
                        }
                    ],
                    "Pediyatrik maligniteler erişkin karsinomlarından farklı olarak lösemi, lenfoma ve blastom ağırlıklıdır."
                )
            ]
        },

        # Slayt 87
        {
            "slideNumber": 87,
            "title": "Kronik İnflamasyon Zemininde Malignite: Helicobacter pylori",
            "content": (
                "Kronik doku inflamasyonu, kanser gelişimini tetikleyen en önemli patolojik zeminlerden biridir. "
                "İnflamatuar mikroçevrede aktive olan makrofaj ve nötrofiller yoğun miktarda reaktif oksijen ve "
                "azot türleri üreterek çevre doku hücrelerinin genomunda doğrudan DNA hasarı oluşturur. Eş zamanlı "
                "olarak salınan sitokinler (TNF, IL-6) ve büyüme faktörleri, doku tamiri amacıyla kök hücreleri "
                "sürekli replikasyona zorlar; replike olan hücreler ise mutasyonel hasarı sabitleyerek neoplastik "
                "dönüşüme uğrar. Bu sürecin en yetkin örneği **Helicobacter pylori** enfeksiyonudur. Kronik H. pylori "
                "gastriti, zamanla gastrik mukozada asit salgılayan pariyetal hücre kaybına (atrofik gastrit) ve "
                "bunun yerini goblet hücreli bağırsak epitelinin almasına (**intestinal metaplazi**) neden olur. "
                "Metaplastik epitel displaziye, ardından invaziv **gastrik adenokarsinoma** ilerler. Ayrıca kronik "
                "antijenik uyarım, mide mukozasında lenfoid doku birikimine ve monoklonal B hücreli **MALT lenfoma** "
                "(ekstranodal marjinal zon lenfoma) oluşumuna yol açar."
            ),
            "elements": [
                make_causal_chain(
                    "H. pylori Aracılı Gastrik Adenokarsinogenez (Pelayo Correa) Sekansı",
                    [
                        "1. Kronik Yüzeyel Gastrit: H. pylori kolonizasyonu ve CagA/VacA toksinleri mukozal nötrofil/mononükleer infiltrasyon başlatır.",
                        "2. Kronik Atrofik Gastrit: Asit üreten pariyetal hücrelerin kaybı ve mukozal bez yapısının ilerleyici silinmesi gelişir.",
                        "3. İntestinal Metaplazi: Gastrik foveoler epitel adaptif olarak intestinal tip goblet ve absorptif hücrelere dönüşür.",
                        "4. Displazi (İntraepitelyal Neoplazi): Metaplastik glandlarda nükleer atipi, stratifikasyon ve polarite kaybı ortaya çıkar.",
                        "5. İnvaziv Gastrik Adenokarsinom: Displastik epitel hücreleri bazal membranı yırtarak lamina propriaya ve submukozaya infiltre olur."
                    ]
                ),
                make_cloze(
                    "H. pylori kaynaklı kronik B hücre stimülasyonu sonucu midede gelişen ve antibiyotik tedavisiyle gerileyebilen neoplazm MALT lenfomadır.",
                    "lenfomadır",
                    "Mukozayla ilişkili lenfoid tümör"
                )
            ]
        },

        # Slayt 88
        {
            "slideNumber": 88,
            "title": "Kronik İnflamasyon ve Kanser Modelleri: Barrett, İBH ve Parazitler",
            "content": (
                "Kalıcı epitel hasarı ve kronik inflamasyon, vücudun farklı anatomik bölgelerinde spesifik "
                "kanser öncüsü zeminler yaratır. Gastroözofageal reflü hastalığında mide asidinin distal "
                "özofagus çok katlı yassı epitelini tahrip etmesi sonucu koruyucu goblet hücreli intestinal epitel "
                "gelişir; bu durum **Barrett özofagus** olarak adlandırılır ve özofagus adenokarsinomu riskini "
                "yaklaşık 30-40 kat artırır. **İnflamatuar Bağırsak Hastalıklarında (özellikle Ülseratif Kolit)** "
                "yıllar boyu süren nükslerle seyreden kolit atakları, normal adenom-karsinom sekansından farklı "
                "olarak diffüz ve multifokal displaziler üzerinden kolorektal karsinom riskini yükseltir. "
                "Enfeksiyöz paraziter zeminlerde ise, Orta Doğu ve Mısır'da endemik olan **Schistosoma haematobium** "
                "yumurtalarının mesane duvarında oluşturduğu granülomatöz kronik sistit, mesanede ürotelyal karsinomdan "
                "ziyade nadir görülen **skuamöz hücreli karsinom** gelişmesine öncülük eder. Güneydoğu Asya'da "
                "biliyer kanallara yerleşen karaciğer kelebeği **Opisthorchis viverrini** ise kronik kolanjit "
                "üzerinden safra yolu kanseri olan **kolanjiyokarsinom** riskini katlar."
            ),
            "elements": [
                make_table(
                    "Kronik İnflamasyon Zeminleri ve İlişkili Maligniteler",
                    ["Klinik İnflamasyon Tablosu", "Etiyolojik Ajan / Süreç", "Prekanseröz Değişiklik", "Gelişen Karakteristik Malignite"],
                    [
                        {
                            "cells": ["Kronik GÖRH", "Mide asit ve safra reflüsü", "Barrett Özofagus (Metaplazi)", "Özofagus Adenokarsinomu"],
                            "hiddenIndex": 3,
                            "hint": "Distal yemek borusu glandüler kanseri"
                        },
                        {
                            "cells": ["Ülseratif Kolit", "Otoimmün/immün kolon inflamasyonu", "Düz mukozada multifokal displazi", "Kolorektal Adenokarsinom"],
                            "hiddenIndex": 3,
                            "hint": "Kalın bağırsak epitelyal tümörü"
                        },
                        {
                            "cells": ["Schistosomiasis", "Schistosoma haematobium yumurtaları", "Mesane skuamöz metaplazisi", "Mesane Skuamöz Karsinomu"],
                            "hiddenIndex": 3,
                            "hint": "Mesanede ürotelyal dışı keratinize kanser"
                        }
                    ]
                ),
                make_active_recall(
                    "Schistosoma haematobium enfeksiyonunun mesanede klasik ürotelyal karsinom yerine spesifik olarak tetiklediği kanser türü nedir?",
                    "Kronik irritasyon ve skuamöz metaplazi zemininde gelişen mesane skuamöz hücreli karsinomudur.",
                    "Üriner kese yassı epitel neoplazmı"
                )
            ]
        },

        # Slayt 89: CHECKPOINT 9
        {
            "slideNumber": 89,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Kanser Epidemiyolojisi ve Çevresel Karsinojenler",
            "content": (
                "Dokuzuncu bölümün bu tekrar sayfasında, kanser insidansı ve mortalitesini belirleyen "
                "çevresel, mesleki ve biyolojik faktörlerin klinik korelasyonu özetlenmektedir. Kansere "
                "bağlı ölümlerde akciğer karsinomunun her iki cinsiyette de birinci sırada yer aldığı "
                "unutulmamalıdır. Göçmen çalışmaları kanser insidansındaki coğrafi varyasyonların temelinde "
                "genetik mirastan ziyade eksojen çevresel maruziyetlerin yattığını açıkça ispatlamıştır. "
                "Tütün ve alkol üst solunum-sindirim karsinomlarında sinerjik etki gösterirken; asbest "
                "mezotelyoma, benzen AML, vinil klorür ise karaciğer anjiyosarkomu için patognomonik mesleki "
                "tetikleyicilerdir. Çocukluk çağı maligniteleri erişkin karsinomlarının aksine blastik "
                "küçük yuvarlak hücreli tümörler ve lösemilerden oluşur. H. pylori, Barrett özofagus ve "
                "ülseratif kolit gibi kronik inflamatuar zeminler, kalıcı hücresel proliferasyon ve oksidatif "
                "DNA hasarı yaratarak epitelyal displazi ve invaziv karsinom sekansını yönetir."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp09-fc01",
                    "front": "Plastik endüstrisinde PVC polimerizasyonunda çalışan personelde görülen ve hepatik endotelden köken alan nadir malign neoplazm hangisidir?",
                    "back": "Hepatik anjiyosarkomdur.",
                    "hint": "Karaciğer vasküler kordon malignitesi"
                },
                {
                    "id": "k1-28-cp09-fc02",
                    "front": "Hem erkek hem de kadın cinsiyette kansere bağlı ölümlerin dünyada ve ülkemizde birinci sıradaki nedeni hangi neoplazmdır?",
                    "back": "Akciğer karsinomudur.",
                    "hint": "Solunum sistemi bronş malignitesi"
                },
                {
                    "id": "k1-28-cp09-fc03",
                    "front": "Maden ocaklarında ve iyi havalandırılmayan bodrumlarda uranyum bozunumuyla biriken sigara dışı en sık akciğer kanseri sebebi radyoaktif gaz hangisidir?",
                    "back": "Radon gazıdır.",
                    "hint": "Toprak altı izotop salınımı"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 9 Özet Tablosu: Mesleki Karsinojenler ve Hedef Organlar",
                    ["Karsinojen Ajan", "Tipik Endüstriyel Maruziyet", "Karakteristik Malignite"],
                    [
                        {
                            "cells": ["Asbest lifleri", "Gemi yapımı ve yalıtım sanayisi", "Malign Mezotelyoma"],
                            "hiddenIndex": 2,
                            "hint": "Plevra mezotel tabakası kanseri"
                        },
                        {
                            "cells": ["Vinil klorür monomeri", "Plastik ve PVC imalat fabrikaları", "Hepatik Anjiyosarkom"],
                            "hiddenIndex": 2,
                            "hint": "Karaciğer endotelyal vasküler sarkom"
                        }
                    ]
                )
            ]
        },

        # Slayt 90
        {
            "slideNumber": 90,
            "title": "Klinik Karar: Mesleki ve Çevresel Risk Faktörlerinin Yönetimi",
            "content": (
                "Klinik pratikte hekimin ayrıntılı meslek ve çevre maruziyeti öyküsü alması, neoplastik "
                "hastalıkların erken tanı ve ayırıcı tanısında hayati öneme sahiptir. Yıllarca tersanede "
                "veya bina yalıtım sektöründe çalışmış, asbest tozu solumuş ve eş zamanlı uzun süre tütün "
                "kullanmış bir hastada hem akciğer karsinomu hem de plevral kalsifikasyonlar/mezotelyoma "
                "riski çok yüksektir. Plevrada kalınlaşma ve hemorajik plevral efüzyon saptandığında, "
                "biyopside mezotelyoma ile adenokarsinom ayrımı kritik bir patolojik basamaktır. "
                "Ayrıca hastanın çalışma arkadaşlarında veya aynı ortamı paylaşanlarda benzer mesleki "
                "hastalık riskinin sorgulanması ve koruyucu önlemlerin devreye sokulması tıbbi sorumluluktur."
            ),
            "elements": [
                make_branching_logic(
                    "35 yıl boyunca tersanede yalıtım işçisi olarak çalışmış ve 40 paket-yıl sigara öyküsü olan 62 yaşındaki erkek hasta, ilerleyici nefes darlığı ve sağ yan ağrısı ile başvuruyor. Toraks BT'de plevrada nodüler kalınlaşma ve masif plevral efüzyon izleniyor.",
                    "Bu hastada patoloğun sitolojik veya biyoptik incelemede öncelikle odaklanması gereken klinik-patolojik antite ve risk faktörü etkileşimi hangisidir?",
                    [
                        {
                            "text": "Asbest maruziyeti ve sigara sinerjisi sorgulanmalı; histopatolojide malign mezotelyoma ve akciğer karsinomu ayrımı için kalretinin ve WT1 immünohistokimyasal paneli uygulanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Tersane yalıtımı asbest maruziyetinin klasik kaynağıdır. Mezotelyoma tanısında mezotelyal belirteçler (kalretinin, WT1) ve karsinom belirteçleri birlikte değerlendirilir; sigara ile asbest akciğer kanseri riskini katlar."
                        },
                        {
                            "text": "Hastada benzen toksisitesine bağlı aplastik anemi geliştiği kabul edilmeli ve acil kemik iliği nakli planlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Benzen solvent maruziyetiyle AML veya aplastik anemi yapar; tersane yalıtımı ve plevral kitle tablosu asbest/mezotelyoma tablosudur."
                        },
                        {
                            "text": "Masif efüzyonun tek sebebi vinil klorür zehirlenmesi olup karaciğer ultrasonografisi ile anjiyosarkom aranmalıdır.",
                            "isCorrect": False,
                            "explanation": "Vinil klorür karaciğer anjiyosarkomu yapar, plevral asbestozis tablosu oluşturmaz."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Kronik reflü hastasında distal özofagusta gelişen Barrett metaplazisinin ve sonrasında adenokarsinomun gelişiminde patogenetik anahtar basamak nedir?",
                    [
                        {
                            "key": "A",
                            "text": "Skuamöz epitelin asit hasarı sonucu mukus salgılayan goblet hücreli intestinal kolumnar epitele dönüşmesi",
                            "isCorrect": True,
                            "explanation": "Barrett özofagus, skuamöz epitelin asit ve safraya karşı koruyucu intestinal kolumnar epitele (metaplazi) dönüşmesidir; displazi zemininde adenokarsinom gelişir."
                        },
                        {
                            "key": "B",
                            "text": "Asidin özofagus submukozasında direkt osteoklastik kemik metaplazisi başlatması",
                            "isCorrect": False,
                            "explanation": "Kemik metaplazisi değil, intestinal glandüler metaplazi gelişir."
                        },
                        {
                            "key": "C",
                            "text": "H. pylori bakterisinin özofagus lümeninde çoğalarak üreaz üretmesi",
                            "isCorrect": False,
                            "explanation": "H. pylori midede yerleşir, distal özofagus Barrett reflü ile tetiklenir."
                        },
                        {
                            "key": "D",
                            "text": "Epitelin doğrudan vasküler anjiyosarkoma dönüşmesi",
                            "isCorrect": False,
                            "explanation": "Anjiyosarkom damar endoteli malignitesidir, epitelyal metaplazi sonucu gelişmez."
                        }
                    ],
                    "Barrett özofagus asit irritasyonuna adaptif intestinal metaplazi yanıtıdır."
                )
            ]
        }
    ]
