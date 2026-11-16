"""
Bölüm 8: T.C. Sağlık Bakanlığı Destek Programları, Kafein, Fetal Alkol Sendromu ve Sigara
Adımlar: 71 - 80
Checkpoint: Adım 79 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # ADIM 71
    slides.append({
        "slideNumber": 71,
        "title": "Sağlık Bakanlığı Demir Destek Programı Protokolü",
        "subtitle": "16. haftadan doğum sonu 3. aya kadar (toplam 9 ay, günlük 40-60 mg)",
        "badge": "Demir Protokolü",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "T.C. Sağlık Bakanlığı Halk Sağlığı Genel Müdürlüğü, anemi olsun ya da olmasın tüm gebelerin demir depolarını korumak "
            "ve anne-bebek mortalitesini engellemek amacıyla 'Gebelere Profilaktik Demir Destek Programı' yürütmektedir. Bu ulusal "
            "protokol gereğince, klinik anemi bulgusu bulunmayan gebeler de dahil olmak üzere her kadına hekim önerisiyle profilaksi başlanır.\n\n"
            "> [SINAV SPOTU] Sağlık Bakanlığı Demir Destek Programı: 16. GEBELİK HAFTASINDAN BAŞLAYARAK gebelik boyunca 6 ay ve "
            "DOĞUM SONU 3 AY olmak üzere TOPLAM 9 AY SÜREYLE, günlük 40 - 60 MG ELEMENTER DEMİR desteği verilir.\n\n"
            "Laboratuvarda klinik anemi tespit edilen gebelerde ise bu profilaktik doz (40-60 mg) tedavi dozuna (günlük 100-200 mg "
            "elementer demir) yükseltilerek depolar doldurulur."
        ),
        "medicalTerms": [
            {"term": "Profilaktik Demir Desteği", "explanation": "Anemi gelişmesini önlemek amacıyla 16. haftada başlanan günlük 40-60 mg elementer demir protokolüdür."},
            {"term": "Toplam 9 Ay Protokolü", "explanation": "Gebelikte 6 ay ve lohusalıkta 3 ay süren kesintisiz ulusal demir takviyesi programıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sağlık Bakanlığı Demir Programı: 16. haftadan doğum sonu 3. aya kadar (toplam 9 ay).",
            "📌 [SINAV SPOTU] Günlük profilaksi dozu: 40 - 60 mg elementer demir.",
            "📌 [SINAV SPOTU] Klinik anemi olmasa dahi tüm gebelere rutin olarak verilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "16. Hafta Başlangıcı", "desc": "Organogenez bitip fetal büyümenin hızlandığı haftada başlar.", "isKey": True},
                {"title": "Toplam 9 Ay", "desc": "Gebelik içi 6 ay + doğum sonrası 3 ay kesintisiz uygulanır.", "isKey": True},
                {"title": "40-60 mg Doz", "desc": "Günlük elementer demir ihtiyacını garantiye alan dozdur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "T.C. Sağlık Bakanlığı protokolüne göre demir desteğine gebeliğin 16. gebelik haftasında başlanır ve doğum sonu 3. aya kadar sürdürülür.",
                "16. gebelik haftasında",
                "Sağlık Bakanlığı demir desteği başlama haftası"
            ),
            make_active_recall(
                "T.C. Sağlık Bakanlığı'nın gebe demir destek programının başlama haftası, toplam süresi ve günlük dozu nedir?",
                "16. gebelik haftasında başlar; gebelikte 6 ay ve doğum sonu 3 ay olmak üzere toplam 9 ay sürer; günlük doz 40 - 60 mg elementer demirdir."
            )
        ]
    })

    # ADIM 72
    slides.append({
        "slideNumber": 72,
        "title": "Sağlık Bakanlığı D Vitamini Destek Programı Protokolü",
        "subtitle": "12. haftadan doğum sonu 6. aya kadar günlük 1200 IU (9 damla)",
        "badge": "D Vitamini Protokolü",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "D vitamini, kalsiyumun bağırsaktan emilimi, fötal kemik mineralizasyonu ve maternal immün tolerans için elzem bir "
            "prohormondur. Ülkemizde kadınlarda güneş ışığından yetersiz yararlanma ve giyim alışkanlıkları nedeniyle yaygın D vitamini "
            "eksikliği görüldüğünden, T.C. Sağlık Bakanlığı özel bir 'Gebelere D Vitamini Destek Programı' uygulamaktadır.\n\n"
            "> [SINAV SPOTU] Sağlık Bakanlığı D Vitamini Destek Programı: 12. GEBELİK HAFTASINDAN BAŞLAYARAK gebelik boyunca ve "
            "DOĞUM SONRASI 6. AYA KADAR, günlük 1200 IU (30 mcg / günde tek doz 9 damla) D3 vitamini desteği verilir.\n\n"
            "Bu destek kalsiyumla kombine edilmeksizin, saf kolekalsiferol (D3) formunda ücretsiz olarak Aile Sağlığı Merkezleri "
            "aracılığıyla tüm gebelere ulaştırılmaktadır."
        ),
        "medicalTerms": [
            {"term": "1200 IU Protokolü", "explanation": "Sağlık Bakanlığı'nın 12. haftadan postpartum 6. aya kadar uyguladığı günlük 9 damlalık D vitamini standardıdır."},
            {"term": "Kolekalsiferol (D3 Vitamini)", "explanation": "D vitamininin karaciğer ve böbrekte hidroksillenerek aktif kalsitriole dönüşen formudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sağlık Bakanlığı D vitamini programı: 12. haftadan doğum sonu 6. aya kadar sürdürülür.",
            "📌 [SINAV SPOTU] Günlük profilaktik doz: 1200 IU (30 mcg / 9 damla).",
            "📌 [SINAV SPOTU] Bebekte raşitizm ve maternal kemik erimesini önler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "12. Hafta Başlangıcı", "desc": "İlk trimestr sonunda rutin D vitamini desteği tetiklenir.", "isKey": True},
                {"title": "Doğum Sonu 6. Ay", "desc": "Emzirme boyunca anne sütü D vitaminini beslemek için devam eder.", "isKey": True},
                {"title": "1200 IU Standart Doz", "desc": "Toksisite riski taşımayan optimal fizyolojik koruma dozudur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Sağlık Bakanlığı protokolüne göre gebelere 12. haftadan doğum sonu 6. aya kadar günlük 1200 IU D vitamini desteği verilir.",
                "1200 IU",
                "Sağlık Bakanlığı günlük D vitamini dozu"
            ),
            make_active_recall(
                "Sağlık Bakanlığı'nın D vitamini destek programı ne zaman başlar, ne zaman biter ve günlük önerilen doz kaç IU'dur?",
                "12. gebelik haftasında başlar, doğum sonu 6. aya kadar devam eder; günlük önerilen doz 1200 IU'dur (9 damla)."
            )
        ]
    })

    # ADIM 73
    slides.append({
        "slideNumber": 73,
        "title": "D Vitamini Dengesi: Fetal Raşitizm vs Aşırılık Toksisitesi",
        "subtitle": "Bebekte kraniyotabes ve neonatal hipokalsemiye karşı hiperkalsemi sınırı",
        "badge": "Kemik Biyolojisi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "D vitamini anne karnındaki bebeğin iskelet sistemi mineralizasyonu ve kalsiyum homeostazının kilit yöneticisidir. "
            "Annenin D vitamini eksikliğinde fetüs yeterli kalsiyumu kemik matriksine gömemez; doğumda kraniyotabes (yumuşak kafatası), "
            "genişlemiş fontaneller, konjenital raşitizm ve yaşamın ilk günlerinde ölümcül konvülsiyonlara yol açan 'neonatal hipokalsemik tetani' tablosu gelişir.\n\n"
            "> [SINAV SPOTU] D vitamini eksikliği bebekte düşük kemik yoğunluğu, raşitizm ve hipokalsemiye yol açarken; D VİTAMİNİNİN "
            "KONTROLSÜZ AŞIRISI bebekte şiddetli hiperkalsemi, aort stenozu ve yumuşak doku kalsifikasyonuna neden olur!\n\n"
            "Bu nedenle megadoz ampul D vitamini enjeksiyonları gebelikte kesinlikle kontrendikedir; fizyolojik 1200 IU günlük doz güvenli sınırdır."
        ),
        "medicalTerms": [
            {"term": "Neonatal Hipokalsemik Tetani", "explanation": "D vitamini eksikliğiyle doğan bebekte kalsiyum düşüklüğüne bağlı gelişen nöromusküler spazm ve konvülsiyondur."},
            {"term": "Supravalvüler Aort Darlığı", "explanation": "İntrauterin aşırı D vitamini toksisitesi sonucu gelişen doğumsal kardiyak damar darlığıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] D vitamini eksikliği: Konjenital raşitizm, neonatal hipokalsemi ve fontanel genişliği yapar.",
            "📌 [SINAV SPOTU] D vitamini aşırısı: Fetal hiperkalsemi ve supravalvüler aort stenozu gibi toksik etkilere yol açar.",
            "📌 [SINAV SPOTU] Anne mutlaka günde 15-20 dakika doğrudan güneş ışığı almalıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eksiklik Tehdidi", "desc": "Raşitizm ve yenidoğan konvülsif hipokalsemisi tetiklenir.", "isKey": True},
                {"title": "Fazlalık Tehlikesi", "desc": "Aort darlığı ve organ kireçlenmesi yapan megadozlardan kaçınılır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte kontrolsüz yüksek doz D vitamini alınması fetüste tehlikeli fetal hiperkalsemi ve yumuşak doku kireçlenmesine yol açabilir.",
                "fetal hiperkalsemi",
                "Kanda kalsiyumun aşırı yükselmesi durumu"
            ),
            make_active_recall(
                "Gebelikte D vitamini eksikliğinin ve kontrolsüz aşırı dozunun bebek üzerindeki patolojik sonuçları nelerdir?",
                "Eksikliği konjenital raşitizm, düşük kemik mineral yoğunluğu ve neonatal hipokalsemi yapar; aşırısı ise şiddetli fetal hiperkalsemi ve damar darlıklarına (aort stenozu) yol açar."
            )
        ]
    })

    # ADIM 74
    slides.append({
        "slideNumber": 74,
        "title": "Kafein Tüketimi: Günde 5 Fincan Eşiği ve Fetal Toksisite",
        "subtitle": "Plasental vazokonstriksiyon, kemik kalsiyum kaybı ve 200 mg güvenlik sınırı",
        "badge": "Kafein Sınırı",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Kafein (1,3,7-trimetilksantin), plasenta bariyerini hiçbir engelle karşılaşmaksızın serbestçe geçen lipofilik bir santral "
            "sinir sistemi stimülanıdır. Fötal karaciğerde kafeini metabolize edecek sitokrom P450 (CYP1A2) enzimi henüz bulunmadığından, "
            "kafein fetal kanda ve amniyon sıvısında maternal kandan çok daha uzun süre yüksek konsantrasyonda kalır.\n\n"
            "> [SINAV SPOTU] Günde 5 fincandan fazla kahve tüketen gebelerde erken doğum ve düşük doğum ağırlığı (DDA) belirgin "
            "şekilde sıktır. Fetüsün kemik mineralizasyonunu bozar; aşırı çay-kahve tüketimi maternal demir ve çinko emilimini de engeller.\n\n"
            "Uluslararası kılavuzlar gebelikte günlük kafein alımının kesinlikle 200 mg'ın altında (yaklaşık 1-2 fincan hafif kahve) "
            "tutulmasını şart koşmaktadır."
        ),
        "medicalTerms": [
            {"term": "CYP1A2 İmmatüritesi", "explanation": "Fötal karaciğerin kafeini yıkamaması ve kafein yarı ömrünün fetüste 80-100 saate uzamasıdır."},
            {"term": "200 mg Kafein Sınırı", "explanation": "Gebelikte spontan abortus ve DDA riskini artırmayan uluslararası güvenli üst tüketim limitidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Günde 5 fincandan fazla kahve: Erken doğum ve düşük doğum ağırlığı riskini belirgin artırır.",
            "📌 [SINAV SPOTU] Fazla kafein fetal kemik kalsiyumunu azaltır, demir ve çinko emilimini felç eder.",
            "📌 [SINAV SPOTU] Güvenli üst sınır günlük <200 mg kafeindir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "5 Fincan Eşiği", "desc": "Ağır kahve tüketimi preterm eylem ve DDA riskini tırmandırır.", "isKey": True},
                {"title": "Mineral Engeli", "desc": "Demir ve çinko emilimini düşürerek anemiye zemin hazırlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Ders notlarına göre gebelikte günde 5 fincandan fazla kahve tüketilmesi erken doğum ve düşük doğum ağırlığı riskini artırır.",
                "5 fincandan fazla",
                "Yüksek riskli kahve tüketim adedi"
            ),
            make_active_recall(
                "Gebelikte aşırı kafein tüketiminin (günde 5 fincandan fazla) fetüs ve anne üzerindeki 3 majör olumsuz etkisi nedir?",
                "1. Erken doğum ve düşük doğum ağırlığı riskini artırır, 2. Fötal kemik yoğunluğunu ve kalsiyum tutulumunu bozar, 3. Anne bağırsağından demir ve çinko emilimini engeller."
            )
        ]
    })

    # ADIM 75
    slides.append({
        "slideNumber": 75,
        "title": "Alkol ve Teratojenite: Gebelikte Sıfır Alkol Kuralı",
        "subtitle": "Plasental difüzyon, nöroblast apoptozu ve güvenli dozun bulunmayışı",
        "badge": "Alkol Uyarısı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Alkol (etanol), bilinen en güçlü insan teratojenlerinden biridir. Alkol küçük molekül ağırlığı ve amfifilik yapısı nedeniyle "
            "plasenta bariyerini saniyeler içinde aşar ve fötal kandaki alkol konsantrasyonu anne kanındaki konsantrasyona eşitlenir. "
            "Fetüsün henüz alkol dehidrogenaz (ADH) aktivitesi gelişmediği için amniyon sıvısında biriken etanol fetüsü uzun süre zehirler.\n\n"
            "> [KRİTİK UYARI] Gebelikte alkolün 'GÜVENLİ BİR DOZU' ve 'GÜVENLİ BİR DÖNEMİ' KESİNLİKLE YOKTUR! Altın kural gebelik "
            "planlandığı andan doğuma ve emzirmenin sonuna kadar SIFIR ALKOL tüketimidir.\n\n"
            "Etanol nöral krest hücrelerinde kitlesel apoptozu tetikler, L1 hücre yapışma molekülünü bloke ederek nöronal göçü bozar ve "
            "geri dönüşü olmayan bir beyin hasarı yaratır."
        ),
        "medicalTerms": [
            {"term": "Nöral Krest Apoptozu", "explanation": "Alkolün serbest oksijen radikalleri üreterek yüz ve kalp taslağını kuran kök hücreleri öldürmesidir."},
            {"term": "Sıfır Alkol Kuralı", "explanation": "Hafif dozların dahi mikrosefali ve davranış bozukluğu yapabilmesi nedeniyle tam abstinans ilkesidir."}
        ],
        "spotPearls": [
            "📌 [KRİTİK UYARI] Gebelikte güvenli alkol miktarı sıfırdır; en ufak miktar bile fötal beyin korteksini zedeler.",
            "📌 [SINAV SPOTU] Alkol fötal dolaşıma anında geçer ve fötal karaciğer tarafından metabolize edilemez."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sıfır Tolerans", "desc": "Herhangi bir trimestrde alınan alkol kalıcı nörogelişimsel hasar yapar.", "isKey": True},
                {"title": "Hücresel İntihar", "desc": "Etanol gelişmekte olan fetal nöronları apoptoza sürükler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dünya Sağlık Örgütü ve obstetrik kılavuzlarına göre gebelik süresince alkol için güvenli bir doz yoktur ve sıfır alkol esastır.",
                "sıfır alkol",
                "Gebelikteki kesin alkol kuralı"
            ),
            make_active_recall(
                "Gebelikte alkol kullanımı için 'güvenli bir miktar' var mıdır ve fetal dokuların alkole bu denli duyarlı olmasının metabolik nedeni nedir?",
                "Güvenli bir miktar kesinlikle yoktur (sıfır alkol). Fetal karaciğerde alkolü yıkacak alkol dehidrogenaz enzimi henüz sentezlenmediğinden, alkol fetüs dokularında birikerek nöronları doğrudan öldürür."
            )
        ]
    })

    # ADIM 76
    slides.append({
        "slideNumber": 76,
        "title": "Fetal Alkol Sendromu (FAS): Klinik Triad ve Dismorfoloji",
        "subtitle": "İlk trimestrde >60 g/gün alkol; büyüme geriliği, SSS anomalisi ve tipik yüz dismorfizmi",
        "badge": "FAS Triadı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte ağır alkol maruziyetinin en yıkıcı tablosu Fetal Alkol Sendromu'dur (FAS). Epidemiyolojik verilere göre gebeliğin "
            "ilk trimestrinde günlük 60 gramdan fazla saf alkol (yaklaşık 4-5 kadeh) tüketen annelerin bebeklerinin %30 - 40'ında "
            "tam teşekküllü Fetal Alkol Sendromu ortaya çıkar.\n\n"
            "> [SINAV SPOTU] Fetal Alkol Sendromu (FAS) klinik triadı: 1) Doğum öncesi ve sonrası BÜYÜME GERİLİĞİ, 2) Santral Sinir "
            "Sistemi bozuklukları (mikrosefali, derin zeka geriliği, DEHB), 3) Karakteristik YÜZ DİSMORFİZMİ (düz filtrum, ince üst dudak vermilyonu, kısa palpebral fissürler).\n\n"
            "FAS, dünyada genetik olmayan önlenebilir mental retardasyonun en sık nedenidir ve bu çocukların bilişsel hasarı ömür boyu kalıcıdır."
        ),
        "medicalTerms": [
            {"term": "Fetal Alkol Sendromu (FAS)", "explanation": "Gebelikte alkol kullanımıyla ortaya çıkan büyüme geriliği, zeka geriliği ve yüz dismorfisi tablosudur."},
            {"term": "Filtrum Düzleşmesi", "explanation": "Burun tabanı ile üst dudak arasındaki oluğun silinerek düzleşmesi şeklindeki tipik FAS bulgusudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İlk trimestrde >60 g/gün alkol alanların %30-40'ında Fetal Alkol Sendromu gelişir.",
            "📌 [SINAV SPOTU] FAS klinik triadı: Büyüme geriliği + SSS anomalisi (zeka geriliği/mikrosefali) + Karakteristik yüz bulguları.",
            "📌 [SINAV SPOTU] Tipik FAS yüzü: Düz filtrum, ince üst dudak, dar göz kapakları (kısa palpebral fissür)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": ">60 g/gün Eşiği", "desc": "Ağır tüketimde bebeklerin %30-40'ı FAS ile dünyaya gelir.", "isKey": True},
                {"title": "Karakteristik Yüz", "desc": "Düz filtrum, ince üst dudak ve mikrosefali tanısaldır.", "isKey": True},
                {"title": "Kalıcı Zeka Geriliği", "desc": "Nöronal göç bozukluğu geri dönüşsüz beyin hasarı bırakır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "İlk trimestrde günlük 60 g üzerinde alkol alan annelerin bebeklerinde yüzde 30-40 oranında Fetal Alkol Sendromu gelişir.",
                "yüzde 30-40",
                "FAS gelişme olasılığı yüzdesi"
            ),
            make_active_recall(
                "Fetal Alkol Sendromu'nun (FAS) 3 temel klinik bileşeni nedir ve yüz dismorfisinde hangi tipik işaretler görülür?",
                "3 temel bileşen: Büyüme geriliği, SSS anomalileri (mikrosefali ve zeka geriliği) ve karakteristik yüz bulgularıdır. Yüzde: Düz filtrum, ince üst dudak ve kısa palpebral fissürler görülür."
            )
        ]
    })

    # ADIM 77
    slides.append({
        "slideNumber": 77,
        "title": "Sigara ve Tütün Dumanı: Nikotin Vazokonstriksiyonu ve CO Hipoksisi",
        "subtitle": "Düşük doğum ağırlığı, erken dekolman plasenta ve perinatal kayıplar",
        "badge": "Sigaranın Zararları",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte sigara kullanımı fötal büyüme ve sağ kalımı tehdit eden en yaygın modifiye edilebilir risk faktörüdür. Sigara "
            "dumanında bulunan iki majör toksik bileşik ikili bir mekanizmayla fötusu boğar: 1) Nikotin: Güçlü bir sempatomimetik ajan "
            "olarak maternal ve uteroplasental damarlarda şiddetli vazokonstriksiyon yapar ve fötal kan akımını keser. 2) Karbonmonoksit (CO): "
            "Hemoglobine oksijenden 200 kat güçlü bağlanarak karboksihemoglobin oluşturur; oksijen taşıma kapasitesini çökertir.\n\n"
            "> [SINAV SPOTU] Gebelikte sigara kullanımı: Düşük Doğum Ağırlığı (DDA, bebek tartısında 200-300 g azalma), prematüre doğum, "
            "ablasyo plasenta (erken ayrılma), plasenta previa, spontan abortus ve perinatal mortalite riskini doğrudan artırır!\n\n"
            "Pasif içicilik dahi fetal büyüme geriliği yaratmak için yeterlidir; bu nedenle gebelikte kesinlikle sigara içilmemeli ve içilen "
            "ortamlarda bulunulmamalıdır."
        ),
        "medicalTerms": [
            {"term": "Fetal Karboksihemoglobinemi", "explanation": "Karbonmonoksitin fetal hemoglobine bağlanarak dokulara oksijen salınımını engellemesidir."},
            {"term": "Ablasyo Plasenta", "explanation": "Sigaraya bağlı desidual nekroz sonucu plasentanın bebek doğmadan duvardan ayrılmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sigara: Nikotin damarları büzer, CO oksijeni çalar -> Sonuç: Düşük doğum ağırlığı ve hipoksi.",
            "📌 [SINAV SPOTU] Sigara içen gebelerin bebekleri ortalama 200-300 gram daha zayıf doğar.",
            "📌 [SINAV SPOTU] Gebelikte sigara kesinlikle içilmemelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Nikotin ve CO", "desc": "Uteroplasental vazokonstriksiyon ve fötal asfiksi oluşturur.", "isKey": True},
                {"title": "DDA ve Dekolman", "desc": "Bebek ağırlığını 250 g düşürür, plasenta ayrılması riskini katlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Sigara dumanındaki nikotin uteroplasental damarları daraltırken karbonmonoksit fetal kanda hipoksiye yol açar.",
                "karbonmonoksit",
                "Oksijen taşınmasını felç eden tütün gazı"
            ),
            make_active_recall(
                "Gebelikte sigara kullanımının fötal oksijenlenmeyi bozan iki temel farmakolojik mekanizması nedir?",
                "1. Nikotinin uteroplasental damarlarda vazokonstriksiyon yaparak kan akımını azaltması, 2. Karbonmonoksitin fetal hemoglobine bağlanarak karboksihemoglobin oluşturması ve doku oksijenasyonunu çökertmesidir."
            )
        ]
    })

    # ADIM 78
    slides.append({
        "slideNumber": 78,
        "title": "Gebelikte Güvenli Fiziksel Aktivite İlkeleri",
        "subtitle": "Hafif-orta şiddette aerobik egzersiz (yürüme, yüzme, sabit bisiklet) ve kontrendikasyonlar",
        "badge": "Fiziksel Aktivite",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte fiziksel aktivite, tıbbi veya obstetrik bir engel bulunmadığı sürece maternal kardiyovasküler dayanıklılığı artıran, "
            "aşırı kilo alımını engelleyen ve gestasyonel diyabet ile preeklampsi riskini azaltan son derece faydalı bir uygulamadır. "
            "Tavsiye edilen egzersiz tipi; haftada en az 150 dakika orta şiddette aerobik aktivitelerdir.\n\n"
            "> [SINAV SPOTU] Gebelikte en güvenli fiziksel aktiviteler: Tempolu yürüme, yüzme ve sabit bisiklettir. İlk trimestrde "
            "aşırı yorucu aktivitelerden ve 16. haftadan sonra supine (sırtüstü) egzersizlerden kesinlikle kaçınılmalıdır!\n\n"
            "Çoğul gebelik, servikal yetersizlik, vajinal kanama ve erken doğum tehdidi olan gebelerde egzersiz kısıtlanmalı; temas sporları, "
            "düşme riski olan aktiviteler (kayak, binicilik) ve scuba dalış yasaklanmalıdır."
        ),
        "medicalTerms": [
            {"term": "Orta Şiddette Aerobik Egzersiz", "explanation": "Gebenin konuşabildiği ancak şarkı söyleyemediği tempodaki fiziksel aktivitedir."},
            {"term": "Supin Egzersiz Yasağı", "explanation": "16. haftadan sonra sırtüstü pozisyonda vena kava basısı nedeniyle egzersiz yapılmaması kuralıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] En güvenli egzersizler: Yürüme, yüzme, sabit bisiklet.",
            "📌 [SINAV SPOTU] 1. trimestrde aşırı yorucu aktiviteden, 16. haftadan sonra sırtüstü egzersizden kaçınılmalıdır.",
            "📌 [SINAV SPOTU] Çoğul gebelik ve servikal yetmezlikte egzersiz sınırlandırılır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yürüme ve Yüzme", "desc": "Eklemlere yük bindirmeyen altın standart güvenli aktivitelerdir.", "isKey": True},
                {"title": "Sırtüstü Yasağı", "desc": "Supin hipotansif sendrom ve fötal bradikardiyi önlemek için şarttır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte vena cava inferiora basıyı engellemek için ikinci trimestrden itibaren sırtüstü egzersiz hareketlerinden kaçınılmalıdır.",
                "sırtüstü egzersiz",
                "Supin pozisyonda yapılan fiziksel aktivite"
            ),
            make_active_recall(
                "Gebelikte önerilen en güvenli üç egzersiz türü hangileridir ve hangi egzersiz pozisyonundan kaçınılmalıdır?",
                "Önerilenler: Tempolu yürüme, yüzme ve sabit bisiklettir. Kaçınılması gereken: 16. haftadan sonra vena kava basısı yapan sırtüstü (supin) egzersizlerdir."
            )
        ]
    })

    # ADIM 79 [CHECKPOINT 8]
    slides.append({
        "slideNumber": 79,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Destek Programları ve Toksik Maddeler İstasyonu",
        "subtitle": "SB demir ve D vitamini protokolleri, kafein sınırı, FAS ve sigara konsolidasyonu",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 8,
        "synthesisNarrative": (
            "Bu istasyon; Sağlık Bakanlığı'nın demir protokolünü (16. haftadan doğum sonu 3. aya, 9 ay, 40-60 mg), D vitamini protokolünü "
            "(12. haftadan doğum sonu 6. aya, 1200 IU), D vitamini eksikliği ve fazlalığının risklerini, günde 5 fincan kahve eşiğini "
            "(DDA ve kalsiyum kaybı), gebelikte sıfır alkol ilkesini, >60 g alkolde %30-40 gelişen Fetal Alkol Sendromu'nu (triad: büyüme "
            "geriliği, SSS anomalisi, düz filtrum/ince üst dudak) ve sigaranın nikotin/CO ile yaptığı hasarı konsolide eder.\n\n"
            "> [YÜKSEK VERİM] Demir: 16. hafta -> Doğum sonu 3. ay (40-60 mg); D Vitamini: 12. hafta -> Doğum sonu 6. ay (1200 IU); "
            "Kahve >5 fincan = tehlikeli; Alkol = sıfır (FAS: >60 g, düz filtrum); Sigara = nikotin/CO -> DDA."
        ),
        "medicalTerms": [
            {"term": "Ulusal Destek İkilisi", "explanation": "Sağlık Bakanlığı'nın rutin uyguladığı demir (40-60 mg) ve D vitamini (1200 IU) programlarıdır."},
            {"term": "Teratojenik Maruziyet", "explanation": "Alkol, tütün ve aşırı kafeinin fötal organogenez ve ağırlık üzerindeki yıkıcı etkileridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] SB Demir: 16. haftadan doğum sonu 3. aya (toplam 9 ay, 40-60 mg).",
            "📌 [SINAV SPOTU] SB D Vitamini: 12. haftadan doğum sonu 6. aya (günlük 1200 IU / 9 damla).",
            "📌 [SINAV SPOTU] FAS: İlk trimestrde >60 g/gün alkol (%30-40); triad: Büyüme geriliği + SSS + Düz filtrum/ince dudak.",
            "📌 [SINAV SPOTU] Sigara nikotin ve CO ile vazokonstriksiyon ve DDA yapar; güvenli egzersiz yürüme ve yüzmedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "SB Protokolleri", "desc": "Demir (16. hf - 9 ay) ve D vit (12. hf - 6. ay) eksiksiz uygulanır.", "isKey": True},
                {"title": "FAS Triadı", "desc": "Büyüme geriliği, zeka geriliği ve karakteristik yüz anomalisi.", "isKey": True},
                {"title": "Tütün ve Kafein", "desc": "Damar spazmı, oksijen açığı ve fetal kemik kalsiyum kaybı.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-22",
                "T.C. Sağlık Bakanlığı'nın gebelere profilaktik demir desteği protokolünün süresi ve dozu nedir?",
                "16. gebelik haftasından başlayarak 6 ay + doğum sonu 3 ay olmak üzere toplam 9 ay sürer; günlük doz 40-60 mg elementer demirdir.",
                "Demir protokolü parametreleri"
            ),
            make_flashcard(
                "fc-k1-06-23",
                "T.C. Sağlık Bakanlığı'nın D vitamini destek protokolü ne zaman başlar, ne zaman biter ve günlük doz kaçtır?",
                "12. gebelik haftasında başlar, doğum sonrası 6. aya kadar sürer; günlük doz 1200 IU'dur (30 mcg / 9 damla).",
                "D vitamini protokolü"
            ),
            make_flashcard(
                "fc-k1-06-24",
                "Fetal Alkol Sendromu (FAS) hangi tüketim eşiğinde görülür ve klinik tanısal triadı nelerden oluşur?",
                "İlk trimestrde günlük >60 g alkol tüketiminde (%30-40 oranında) görülür. Triad: 1. Büyüme geriliği, 2. SSS gelişim anomalileri (mikrosefali, zeka geriliği), 3. Karakteristik yüz dismorfizmi (düz filtrum, ince üst dudak).",
                "FAS klinik özellikleri"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Sağlık Bakanlığı Destek Programı", "Başlama ve Bitiş Zamanı", "Günlük Profilaktik Doz"],
                [
                    [("Demir Destek Programı", False, ""), ("16. haftadan doğum sonu 3. aya (toplam 9 ay)", False, ""), ("Günlük 40-60 mg elementer demir", True, "Ulusal demir destek dozu")],
                    [("D Vitamini Destek Programı", False, ""), ("12. haftadan doğum sonu 6. aya kadar", False, ""), ("Günlük 1200 IU (9 damla)", True, "Ulusal D vitamini profilaksi dozu")]
                ]
            )
        ]
    })

    # ADIM 80
    slides.append({
        "slideNumber": 80,
        "title": "Karşılaştırmalı Toksikoloji: Sigara vs Alkolün Fetal İmzaları",
        "subtitle": "Simetrik mikrosefali ve dismorfoloji (Alkol) vs Asimetrik büyüme kısıtlılığı ve hipoksi (Sigara)",
        "badge": "Klinik Karşılaştırma",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte maruz kalınan iki yaygın yasal toksik madde olan tütün ve alkol, fötal biyoloji üzerinde tamamen farklı patofizyolojik "
            "hasar profilleri (imzalar) oluşturur. Alkol esas olarak 'hücresel toksisite ve teratogenez' yaratır; organogenez evresinde "
            "nöral krest hücrelerini öldürerek kalıcı kraniofasiyal dismorfolojiye, mikrosefaliye ve derin mental retardasyona yol açar.\n\n"
            "> [SINAV SPOTU] Alkol primer olarak nöronal teratojendir (FAS: kalıcı zeka geriliği ve mikrosefali yapar); sigara ise primer "
            "olarak vasküler hipoksik ajandır (ablasyo plasenta ve kilo kaybı yapar; sigarada FAS gibi yüz anomalisi görülmez!).\n\n"
            "Sigara içen annenin bebeği zayıf ve hipoksik doğsa da yüz yapısı normaldir; alkol maruziyetinde ise hem beyin küçük kalır "
            "hem de yüz çizgileri silinir."
        ),
        "medicalTerms": [
            {"term": "Nöronal Teratogenez", "explanation": "Alkolün beyin korteksi nöronlarını öldürerek kalıcı morfolojik ve bilişsel hasar bırakmasıdır."},
            {"term": "Vasküler Hipoksi İmzası", "explanation": "Sigaranın plasental kanlanmayı bozarak fötal dokuları oksijensiz bırakmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Alkol: Zeka geriliği, mikrosefali, yüz dismorfisi (FAS) yapar.",
            "📌 [SINAV SPOTU] Sigara: DDA, preterm eylem, ablasyo plasenta yapar; yüz anomalisi yapmaz.",
            "📌 [SINAV SPOTU] Her iki madde de büyüme geriliği üretir ancak alkolün zihinsel tahribatı çok daha derindir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Alkol: Teratojen", "desc": "Nöral krest ölümü, yüz dismorfisi ve mental retardasyon.", "isKey": True},
                {"title": "Sigara: Hipoksik", "desc": "Vazokonstriksiyon, karboksihemoglobin ve düşük tartı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Sigara vs Alkolün Fetal Gelişim Üzerindeki Patolojik İmzaları",
                "Gebelikte Alkol Maruziyeti",
                "Primer hücresel teratogenez: Fetal Alkol Sendromu (FAS), nöron göç bozukluğu, mikrosefali, derin zeka geriliği ve tipik yüz dismorfizmi (düz filtrum, ince üst dudak) ile karakterizedir.",
                "Gebelikte Tütün (Sigara) Maruziyeti",
                "Primer vasküler hipoksi: Nikotin vazokonstriksiyonu ve karbonmonoksit hipoksisi sonucu belirgin düşük doğum ağırlığı (200-300 g azalma), erken membran rüptürü ve ablasyo plasenta ile karakterizedir."
            ),
            make_active_recall(
                "Gebelikte alkol ile sigaranın fetüs üzerindeki temel patolojik farkı nedir?",
                "Alkol doğrudan nöronları öldürerek Fetal Alkol Sendromu (zeka geriliği, mikrosefali ve yüz dismorfisi) yapan bir teratojendir. Sigara ise damarları büzüp oksijeni çalarak düşük doğum ağırlığı ve plasenta ayrılması yapan hipoksik bir ajandır (yüz anomalisi yapmaz)."
            )
        ]
    })

    return slides
