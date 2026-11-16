# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 9: Ürik Asit ve Sistin Taşlarının Patofizyolojisi (Slayt 81 - 90)
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
            "title": "Ürik Asit Taşları: Fizikokimya ve pKa (5.35) Önemi",
            "content": (
                "Ürik asit taşları tüm böbrek taşlarının yaklaşık %8-10'unu oluşturur ve direkt üriner sistem grafisinde "
                "bütünüyle radyolüsen izlenmeleriyle klinik olarak ayrışır. Ürik asit, pürin nükleotidlerinin (adenin ve guanin) "
                "katabolizmasının son ürünüdür ve zayıf bir diprotik organik asittir. İlk iyonlaşma sabiti olan pKa değeri "
                "kesin olarak 5.35'tir. Bu pKa değeri şu anlama gelir: İdrar pH'ı 5.35 olduğunda, toplam ürik asidin tam yarısı (%50) "
                "çözünürlüğü yüksek olan iyonize ürat şeklinde, diğer yarısı (%50) ise suda çok zor çözünen serbest ürik asit "
                "formundadır. İdrar pH'ı 5.0'e düştüğünde serbest ürik asit oranı %85'e tırmanarak hızla çöker; pH 6.5'in üzerine "
                "çıktığında ise çözünürlük 10 kat artarak çökelme durur."
            ),
            "elements": [
                make_cloze(
                    "Ürik asidin suda çözünürlük dengesini belirleyen birinci dissosiasyon sabiti pKa değeri beş virgül otuz beş olarak saptanmıştır.",
                    "beş virgül otuz beş",
                    "İyonlaşma yarılanma pH değeri"
                ),
                make_active_recall(
                    "İdrar pH'ı pKa olan 5.35'in altına indiğinde ürik asit molekülünün çözünürlüğünde meydana gelen temel fizikokimyasal değişim nedir?",
                    "İyonize üratın çözünmeyen serbest ürik aside dönüşerek hızla kristalleşmesidir.",
                    "Katı kristal faza geçiş"
                )
            ]
        },
        # Slayt 82
        {
            "slideNumber": 82,
            "title": "Kronik Düşük İdrar pH'ının Etyolojisi",
            "content": (
                "Ürik asit taşı oluşturan hastaların çoğunda 24 saatlik idrar ürik asit miktarı tamamen normal sınırlardadır; "
                "bu hastalardaki temel suçlu 'kronik olarak aşırı asidik idrar' (pH <5.5) çıkarılmasıdır. Kalıcı düşük idrar pH'ı "
                "üç ana klinik tabloda gözlenir: Birincisi, gut diyatezi ve metabolik sendromdur (tübüler amonyogenez kusuru). "
                "İkincisi, ileostomi, Crohn veya laksatif bağımlılığına bağlı kronik ishallerdir; dışkıyla yoğun alkali (bikarbonat) "
                "ve su kaybedilmesi böbreğin kompanse edici olarak aşırı asit pompalamasına ve asidik konsantre idrar üretmesine yol açar. "
                "Üçüncüsü ise aşırı hayvansal protein tüketimine bağlı sülfat ve fosfat yüküdür."
            ),
            "elements": [
                make_table(
                    "Kronik Asidik İdrar (pH < 5.5) Nedenleri ve Mekanizmaları",
                    ["Klinik Tablo", "Primer Asit-Baz Kusuru", "Renal Mekanizma", "Taş Riski"],
                    [
                        {
                            "cells": ["Metabolik Sendrom / Tip 2 DM", "İnsülin direnci", "Bozulmuş tübüler amonyogenez", "Ürik asit ve mikst CaOx"],
                            "hiddenIndex": 2,
                            "hint": "Amonyum tampon üretim azlığı"
                        },
                        {
                            "cells": ["Kronik İshal / İleostomi", "Gastrointestinal bikarbonat kaybı", "Konsantre asidik idrar salgılanması", "Ürik asit ve amonyum ürat"],
                            "hiddenIndex": 1,
                            "hint": "Bağırsaktan baz atılımı"
                        },
                        {
                            "cells": ["Aşırı Pürin / Protein", "Kükürtlü amino asit asidozu", "Net asit atılımında belirgin artış", "Ürik asit"],
                            "hiddenIndex": 3,
                            "hint": "En yaygın asit taşı"
                        }
                    ]
                ),
                make_active_recall(
                    "İleostomili veya kronik ishalli hastalarda ürik asit taşı sıklığını artıran temel gastrointestinal kayıp nedir?",
                    "Dışkıyla masif su ve bikarbonat kaybı yaşanmasıdır.",
                    "Alkali baz ve sıvı boşalması"
                )
            ]
        },
        # Slayt 83
        {
            "slideNumber": 83,
            "title": "Tip 2 Diyabette Renal Asidifikasyon Bozukluğu",
            "content": (
                "Tip 2 diyabet ve metabolik sendromlu hastalarda ürik asit taşı sıklığı genel popülasyona göre 3-4 kat daha "
                "yüksektir. Bu patolojinin temelinde 'renal tübüler insülin direnci' yatar. Normal fizyolojide insülin, "
                "proksimal tübül hücrelerinde glutamin metabolizmasını uyararak amonyum (NH4+) üretimini ve sekresyonunu teşvik eder. "
                "İnsülin direnci geliştiğinde tübüler amonyogenez çöker; idrara yeterli amonyum salgılanamaz. Amonyum en önemli "
                "üriner bazik tampon olduğu için, tamponlanamayan serbest protonlar (H+) idrar pH'ının 5.0 gibi son derece "
                "asidik seviyelere çakılmasına neden olur. Bu durum hiperürikozüri olmasa bile spontan ürik asit kristalizasyonunu garantiler."
            ),
            "elements": [
                make_causal_chain(
                    "İnsülin Direncinden Ürik Asit Litogenezine Tübüler Basamaklar",
                    [
                        "1. Tübüler İnsülin Direnci: Proksimal tübül epitelinde insülin sinyal yolunun körelmesi",
                        "2. Amonyogenez İnhibisyonu: Glutaminaz enzim aktivitesinin ve NH4+ sentezinin baskılanması",
                        "3. Tamponlama Yıkımı: İdrar lümenindeki hidrojen iyonlarının tamponlayıcı amonyum bulamaması",
                        "4. İdrar pH Çöküşü: İdrar pH'ının kalıcı olarak 5.0 - 5.3 aralığına gerilemesi",
                        "5. Ürisit Çökelmesi: pKa eşiğinin altında kalan çözünmeyen ürik asidin masif taş kitlesine dönüşmesi"
                    ]
                ),
                make_cloze(
                    "Tip 2 diyabette idrarın tamponlanamayarak aşırı asidik kalmasına yol açan primer tübüler defekt amonyogenez kusurudur.",
                    "amonyogenez kusurudur",
                    "Amonyum sentez yetersizliği"
                )
            ]
        },
        # Slayt 84
        {
            "slideNumber": 84,
            "title": "Ürik Asit Taşlarının Medikal Eriyebilirliği (Kemoliz)",
            "content": (
                "Ürik asit taşları, cerrahi müdahaleye gerek kalmaksızın yalnızca farmakolojik tedavi ile tamamen "
                "eritilebilen (oral kemoliz) yegane taş türüdür. Kemolizin temeli, idrar pH'ını ürik asidin pKa değerinin "
                "(5.35) belirgin biçimde üzerine, ideal olarak '6.5 - 7.0' aralığına yükseltmektir. Bu amaçla birinci seçenek "
                "ilaç potasyum sitrattır (veya sodyum-potasyum bikarbonat). İdrar pH'ı 6.5'e çıktığında çözünmeyen ürik asit "
                "hızla çözünür monosodyum/potasyum ürata dönüşür ve mevcut taşlar haftalar içinde eriyerek küçülür. Ancak "
                "idrar pH'ının 7.2'nin üzerine çıkarılmasından kesinlikle kaçınılmalıdır; aksi halde taş yüzeyinde kalsiyum "
                "fosfat (apatit) çökerek taşı erimez bir kabukla kaplayabilir."
            ),
            "elements": [
                make_before_after(
                    "Ürik Asit Taşında pH Düzeyinin Kemoliz Dinamiği",
                    "Asidik İdrar (pH < 5.5)",
                    "Ürik asit doymuş ve çözünmez kristal kafesi halindedir; taş sürekli büyür ve medikal olarak erimez.",
                    "Alkalinize İdrar (pH 6.5 - 7.0)",
                    "Çözünürlük 10-20 kat artar; mevcut taş yüzeyinden iyonlar sökülerek çözünür ürata dönüşür ve taş erir.",
                    "Oral potasyum sitrat ile kemoliz ürolojide ameliyatsız taş yok etmenin en başarılı örneğidir."
                ),
                make_micro_quiz(
                    "Ürik asit taşlarının oral kemolizinde hedeflenen en güvenli ve etkili idrar pH aralığı hangisidir?",
                    [
                        {
                            "text": "6.5 ile 7.0 aralığı",
                            "isCorrect": True,
                            "explanation": "Doğrudur; bu aralıkta ürik asit maksimum erir, kalsiyum fosfat çökmesi riski minimize edilir."
                        },
                        {
                            "text": "4.5 ile 5.0 aralığı",
                            "isCorrect": False,
                            "explanation": "Bu aralık aşırı asidiktir ve ürik asidin taşlaşmasını daha da hızlandırır."
                        },
                        {
                            "text": "8.0 ile 8.5 aralığı",
                            "isCorrect": False,
                            "explanation": "Bu kadar yüksek pH kalsiyum fosfat çökmesine ve strüvite davetiye çıkarır."
                        },
                        {
                            "text": "Tam olarak 1.0 değeri",
                            "isCorrect": False,
                            "explanation": "İdrar pH'ı 1.0 olamaz; ölümcül bir asit düzeyidir."
                        }
                    ],
                    "Hedeflenen kemoliz pH'ı 6.5 - 7.0 bandıdır."
                )
            ]
        },
        # Slayt 85
        {
            "slideNumber": 85,
            "title": "Sistinüri: Genetik Temel ve Taşıyıcı Kusurları",
            "content": (
                "Sistinüri, böbrek proksimal tübül epitelinde ve ince bağırsak jejunum mukozasında bulunan apikal "
                "heterodimerik amino asit taşıyıcı kompleksinin otozomal resesif kalıtılan kalıtsal bir hastalığıdır. "
                "Taşıyıcı sistem iki alt birimden oluşur: ağır zinciri kodlayan 'SLC3A1' geni (kromozom 2p) ve hafif "
                "zinciri kodlayan 'SLC7A9' geni (kromozom 19q). SLC3A1 mutasyonları Tip A sistinüriyi (klasik resesif), "
                "SLC7A9 mutasyonları ise Tip B sistinüriyi oluşturur. Bu taşıyıcı kompleksi filtre edilen dibazik amino "
                "asitlerin (sistin, ornitin, lizin, arjinin) geri emiliminden sorumludur. Taşıyıcı bozulduğunda idrara "
                "masif miktarda serbest sistin dökülür."
            ),
            "elements": [
                make_table(
                    "Sistinüri Tipleri ve Moleküler Genetik Özellikleri",
                    ["Sistinüri Tipi", "Mutasyona Uğrayan Gen", "Kromozomal Bölge", "Protein Alt Birimi"],
                    [
                        {
                            "cells": ["Tip A Sistinüri", "SLC3A1", "Kromozom 2p", "rBAT ağır zincir glikoproteini"],
                            "hiddenIndex": 1,
                            "hint": "Ağır zincir geni"
                        },
                        {
                            "cells": ["Tip B Sistinüri", "SLC7A9", "Kromozom 19q", "b0,+AT hafif zincir katalitik alt birimi"],
                            "hiddenIndex": 1,
                            "hint": "Hafif zincir geni"
                        }
                    ]
                ),
                make_active_recall(
                    "Tip A sistinüriye yol açan rBAT ağır zincir glikoproteinini kodlayan gen hangisidir?",
                    "SLC3A1 genidir.",
                    "Klasik tip A sistinüri geni"
                )
            ]
        },
        # Slayt 86
        {
            "slideNumber": 86,
            "title": "COLA Amino Asitleri ve Sistin Çözünmezliği",
            "content": (
                "Sistinüri defektinde idrarla atılımı artan dört temel amino asit 'COLA' akronimi ile kodlanır: "
                "Sistin, Ornitin, Lizin ve Arjinin. Bu amino asitlerden ornitin, lizin ve arjinin idrarda son derece yüksek "
                "çözünürlüğe sahiptir ve asla taş oluşturmazlar. Buna karşın iki sistein molekülünün disülfit bağıyla birleşmesinden "
                "oluşan 'sistin', fizyolojik idrar pH aralığında (pH 5.0 - 7.0) son derece zayıf bir çözünürlüğe sahiptir "
                "(maksimum çözünürlük ~250 mg/L). Normal bireylerde 24 saatlik idrar sistini <30 mg iken, homozigot sistinürili "
                "hastalarda bu değer sıklıkla 600 - 1500 mg/gün seviyelerine tırmanır. Çözünürlük limiti hızla aşıldığı için "
                "sistin kristalleri çöker ve genç yaşta dev koraliform taşlar oluşturur."
            ),
            "elements": [
                make_cloze(
                    "Sistinüri transport defektinde atılan amino asitlerden yalnızca sistin molekülü idrarda çözünemeyerek taşlaşır.",
                    "yalnızca sistin molekülü",
                    "Çözünürlüğü son derece düşük disülfit amino asit"
                ),
                make_before_after(
                    "COLA Amino Asitlerinin İdrardaki Çözünürlük Davranışı",
                    "Ornitin, Lizin ve Arjinin",
                    "Polar ve son derece hidrofiliktirler; gramlarca atılsalar bile idrar suyunda tamamen erirler ve taş yapmazlar.",
                    "Sistin (Disülfit Köprülü)",
                    "Apolar ve hidrofobiktir; 250 mg/L üzerinde derhal çöker ve sert, balmumu benzeri agresif taşlar meydana getirir.",
                    "Taş riskini belirleyen tek faktör serbest sistinin konsantrasyonudur."
                )
            ]
        },
        # Slayt 87
        {
            "slideNumber": 87,
            "title": "Sistin Çözünürlük Eğrisi: pH ve Sodyum Bağımlılığı",
            "content": (
                "Sistinin idrardaki çözünürlük davranışı iki temel değişkene sıkı sıkıya bağlıdır: idrar pH'ı ve idrar sodyum "
                "konsantrasyonu. Sistinin çözünürlüğü pH 7.0'ye kadar neredeyse sabittir (~250 mg/L). Ancak idrar pH'ı 7.5'in "
                "üzerine çıkarıldığında çözünürlük exponansiyel olarak tırmanarak iki katına (>500 mg/L) çıkar. İkinci kritik "
                "faktör sodyumdur: Proksimal tübülde sistin geri emilimi sodyum transportu ile yakından bağlantılıdır. Yüksek "
                "diyet sodyumu lümene sistin kaçışını artırırken, sıkı sodyum kısıtlaması (<2 gram/gün) sistin atılımını "
                "doğrudan %30-40 oranında azaltır."
            ),
            "elements": [
                make_causal_chain(
                    "Sodyum Kısıtlamasından Sistinüri Kontrolüne Uzanan Yol",
                    [
                        "1. Diyet Sodyum Kısıtlaması: Günlük sofra tuzu alımının 2 gramın altına çekilmesi",
                        "2. Tübüler Sodyum Düşüşü: Proksimal tübül lümenindeki sodyum konsantrasyonunun gerilemesi",
                        "3. Sistin Sekresyonunun Azalması: Sodyum-amino asit elektriksel gradyentinin sistin atılımını düşürmesi",
                        "4. İdrar Sistini Gerilemesi: 24 saatlik idrar sistininin 250 mg/L çözünürlük sınırının altına inmesi"
                    ]
                ),
                make_active_recall(
                    "Sistin molekülünün idrarda çözünürlüğünü belirgin olarak artırmak için hedeflenen idrar pH düzeyi nedir?",
                    "Yedi buçuğun (7.5) üzerine çıkarılmasıdır.",
                    "Belirgin alkali pH eşiği"
                )
            ]
        },
        # Slayt 88
        {
            "slideNumber": 88,
            "title": "Sistin Taşlarında Tanı ve Tiol İlaçları",
            "content": (
                "Sistinüri tanısı, idrar sedimentinde karakteristik patognomonik 'altıgen' (hekzagonal) plak şeklinde "
                "kristallerin görülmesi veya sodyum siyanür-nitroprussid testinin pozitif çıkmasıyla (mor/kırmızı renk) "
                "konur. Konservatif tedavide günde en az 3.5 - 4 litre idrar çıkaracak hidrasyon, potasyum sitrat ile "
                "idrar pH'ının >7.5 tutulması ve tuz kısıtlaması esastır. Bu önlemlere rağmen sistin konsantrasyonu "
                ">250-300 mg/L kalan hastalarda 'tiol türevi ilaçlar' (D-penisilamin veya alfa-merkaptopropiyonilglisin / "
                "tiopronin) başlanır. Bu ilaçlar sistinin disülfit bağını kırarak sistin-ilaç mikst disülfitleri oluşturur; "
                "bu yeni bileşikler sistinden 50 kat daha fazla çözünür ve taşlaşmayı durdurur."
            ),
            "elements": [
                make_table(
                    "Sistinüri Tanı ve Tedavi Basamakları",
                    ["Aşama", "Yöntem / İlaç", "Hedeflenen Fizyolojik Değer", "Mekanizma"],
                    [
                        {
                            "cells": ["İdrar Mikroskopisi", "Hekzagonal kristaller", "Tanısal patognomonik", "Altıgen sistin plaklarının saptanması"],
                            "hiddenIndex": 0,
                            "hint": "Mikroskobik tanı şekli"
                        },
                        {
                            "cells": ["Birinci Basamak", "Potasyum sitrat + Bol Sıvı", "İdrar pH > 7.5, Hacim >3.5 L", "Çözünürlüğü artırma ve dilüsyon"],
                            "hiddenIndex": 2,
                            "hint": "Hedef idrar pH ve hacim sınırı"
                        },
                        {
                            "cells": ["İkinci Basamak (Tiol)", "Tiopronin (Alfa-MPG)", "Serbest sistin < 250 mg/L", "Disülfit bağını kırarak çözünür kompleks yapma"],
                            "hiddenIndex": 1,
                            "hint": "Tiol grubu şelatör ilaç"
                        }
                    ]
                ),
                make_cloze(
                    "İdrar sedimentinde saptanan hekzagonal altıgen kristaller sistinüri hastalığı için patognomonik kabul edilir.",
                    "sistinüri hastalığı",
                    "COLA taşıyıcı defekti hastalığı"
                )
            ]
        },
        # Slayt 89 [CHECKPOINT 9]
        {
            "slideNumber": 89,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Ürik Asit ve Sistin Taşları",
            "content": (
                "Bu bölümde ürik asit ve sistin taşlarının patofizyolojisini, fizikokimyasını ve tedavisini inceledik. "
                "Ürik asit taşları direkt grafide radyolüsendir; oluşumundaki ana etken pKa'nın (5.35) altında seyreden düşük idrar pH'ıdır. "
                "Metabolik sendrom ve diyabette tübüler amonyogenez kusuru idrarı tamponsuz bırakarak asidikleştirir. "
                "Ürik asit taşları ameliyatsız eriyebilen tek taş türüdür; potasyum sitrat ile idrar pH'ı 6.5 - 7.0 aralığına çekilerek kemoliz sağlanır. "
                "Sistinüri, SLC3A1 ve SLC7A9 mutasyonlarıyla COLA amino asitlerinin geri emilim bozukluğudur. "
                "COLA grubunda sadece serbest sistin çözünemez (çözünürlük ~250 mg/L); altıgen (hekzagonal) kristaller patognomoniktir. "
                "Sistin tedavisinde tuz kısıtlaması, idrar pH'ının >7.5 tutulması ve dirençli olgularda disülfit bağını kıran tiol ilaçları (tiopronin) kullanılır."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp09-fc01",
                    "front": "Ürik asit taşlarının medikal kemoliz tedavisinde hedeflenen en ideal idrar pH aralığı nedir?",
                    "back": "Altı buçuk ile yedi aralığıdır.",
                    "hint": "Asidi çözen ılımlı nötralize band"
                },
                {
                    "id": "k1-27-cp09-fc02",
                    "front": "İdrar sedimentinde altıgen hekzagonal kristallerin görülmesi hangi herediter taş hastalığı için patognomoniktir?",
                    "back": "Sistinüri hastalığı için patognomoniktir.",
                    "hint": "Dibazik amino asit transport bozukluğu"
                },
                {
                    "id": "k1-27-cp09-fc03",
                    "front": "Dirençli sistinüri olgularında sistinin disülfit köprülerini kırarak çözünür mikst kompleksler oluşturan ilaç grubu nedir?",
                    "back": "Tiol türevi ilaç grubudur.",
                    "hint": "Sülfidril bağı taşıyan şelatörler"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 9 Özet Tablosu: Ürik Asit ve Sistin Karşılaştırması",
                    ["Özellik", "Ürik Asit Taşı", "Sistin Taşı"],
                    [
                        {
                            "cells": ["Radyolojik Görünüm", "Tamamen Radyolüsen", "Zayıf Radyoopak (Kükürtlü)"],
                            "hiddenIndex": 0,
                            "hint": "Görüntüleme opasitesi"
                        },
                        {
                            "cells": ["Hedeflenen Tedavi pH'ı", "6.5 - 7.0", "> 7.5"],
                            "hiddenIndex": 1,
                            "hint": "Kemoliz pH aralığı"
                        },
                        {
                            "cells": ["Karakteristik Kristal", "Romboid / Elmas", "Hekzagonal (Altıgen)"],
                            "hiddenIndex": 2,
                            "hint": "Sistin mikroskopi morfolojisi"
                        }
                    ]
                )
            ]
        },
        # Slayt 90
        {
            "slideNumber": 90,
            "title": "Klinik Karar: Ürik Asit Taşında Oral Kemoliz Yönetimi",
            "content": (
                "Bilgisayarlı tomografide renal pelviste 18 mm boyutunda, düşük Hounsfield ünitesine sahip (HU ~450) ve "
                "DÜSG'de tamamen radyolüsen olan bir taş saptandığında, idrar pH'ı 5.1 ölçülen hastaya cerrahi yerine "
                "oral kemoliz protokolü önerilmelidir. Hastaya oral potasyum sitrat tedavisi başlanır ve idrar pH'ını günde "
                "3 kez idrar pH stribiyle ölçerek 6.5 - 7.0 arasında tutması tembihlenir. Eşlik eden hiperürisemi veya "
                "aşırı hiperürikozüri varsa ksantin oksidaz inhibitörü allopurinol tedaviye eklenir. Düzenli kemoliz ile "
                "taşın haftalar içinde tamamen eridiği radyolojik olarak gösterilebilir."
            ),
            "elements": [
                make_branching_logic(
                    "52 yaşında obez erkek hastada sağ böbrek pelvisinde 2 cm'lik taş saptanıyor. Taş DÜSG'de görünmüyor, kontrassız BT'de 420 HU dansitede izleniyor. İdrar pH'ı 5.2 olarak ölçülüyor. Hasta cerrahi istemiyor.",
                    "Bu hastada taşın tamamen eritilmesi (kemoliz) amacıyla izlenmesi gereken en uygun klinik protokol nedir?",
                    [
                        {
                            "text": "Oral potasyum sitrat başlanarak idrar pH'ı günde üç kez striplerle takip edilmeli ve 6.5-7.0 bandında tutularak taşın çözünmesi sağlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; ürik asit taşları 6.5-7.0 pH aralığında çözünerek cerrahisiz tamamen yok edilebilir."
                        },
                        {
                            "text": "Hastaya yüksek doz C vitamini verilerek idrar pH'ı 4.5'e çekilmelidir.",
                            "isCorrect": False,
                            "explanation": "İdrarı asitleştirmek ürik asidi çözer değil tam tersine daha da taşlaştırır."
                        },
                        {
                            "text": "Taşın erimesi imkansız olduğundan zorunlu açık cerrahi nefrektomi planlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Ürik asit taşları medikal olarak eritilebilen tek taştır, nefrektomi endikasyonu yoktur."
                        }
                    ]
                )
            ]
        }
    ]
