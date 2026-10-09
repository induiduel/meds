"""
Bölüm 7: Nöral Tüp Defektleri ve Folik Asit Profilaksisi, Gebelikte Anemi ve Demir Metabolizması
Adımlar: 61 - 70
Checkpoint: Adım 69 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # ADIM 61
    slides.append({
        "slideNumber": 61,
        "title": "Folik Asit (B9) ve Nöral Tüp Kapanma Biyolojisi: 28. Gün Eşiği",
        "subtitle": "Prekonsepsiyonel desteğin biyolojik mantığı ve tek karbon metabolizması",
        "badge": "Folik Asit",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Folik asit (pteroilmonoglutamik asit), hücre bölünmesi, pürin ve pirimidin nükleotid sentezi ile DNA metilasyonu için "
            "zorunlu olan tek karbon (metil) transferi biyokimyasal yolağının merkezindedir. İnsan embriyogenezinde beyin ve omuriliğin "
            "temelini oluşturan nöral plak, fertilizasyondan sonraki 21. günde katlanmaya başlar ve en geç 28. günde (kranial ve kaudal "
            "nöroporların kapanmasıyla) tüp yapısını tamamlar.\n\n"
            "> [SINAV SPOTU] Nöral tüp gebeliğin 28. gününde (kadın henüz adet gecikmesini yeni fark ettiği dönemde) kapanmasını tamamlar! "
            "Bu nedenle folik asit desteği gebelik oluştuktan sonra değil, GEBE KALMADAN EN AZ 3 AY ÖNCE başlanmalıdır.\n\n"
            "Folik asit eksikliğinde hücre proliferasyonu duraklar, nöroektoderm kenarları birleşemez ve nöral tüp defektleri (NTD) "
            "ortaya çıkar. Prekonsepsiyonel folat takviyesi bu felaketi %70-85 oranında önleyen en başarılı profilaksi yöntemidir."
        ),
        "medicalTerms": [
            {"term": "Nöral Kapanma (Nörülasyon)", "explanation": "Embriyoda nöral plağın kıvrılarak 28. günde kapalı bir nöral tüp oluşturması sürecidir."},
            {"term": "Prekonsepsiyonel Dönem", "explanation": "Gebelik planlandığı andan itibaren döllenmeye kadar geçen gebelik öncesi hazırlık evresidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nöral tüp fertilizasyondan sonraki 28. günde kapanır; bu nedenle folat gebelik öncesi başlanmalıdır.",
            "📌 [SINAV SPOTU] Planlı gebelikte folik asit desteğine gebe kalmadan 3 ay önce başlanır.",
            "📌 [SINAV SPOTU] Folat desteği nöral tüp defekti riskini %70-85 oranında azaltır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "28. Gün Eşiği", "desc": "Nöral tüp kapanması anne gebeliğini fark etmeden tamamlanır.", "isKey": True},
                {"title": "3 Ay Önce Başlama", "desc": "Eritrosit folat depolarının doyurulması için önceden başlama şarttır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Nöral tüp embriyogenezin 28. gününde kapandığı için folik asit desteğine gebe kalmadan 3 ay önce başlanmalıdır.",
                "3 ay önce",
                "Folik aside başlama zamanı"
            ),
            make_active_recall(
                "Neden folik asit desteği gebelik testi pozitif çıktıktan sonra değil de gebe kalmadan en az 3 ay önce başlanmalıdır?",
                "Çünkü embriyonun omurilik ve beyin taslağını oluşturan nöral tüp fertilizasyondan sonraki 28. günde kapanmasını tamamlar. Gebelik öğrenildiğinde genellikle bu kritik pencere kapanmış olur."
            )
        ]
    })

    # ADIM 62
    slides.append({
        "slideNumber": 62,
        "title": "Nöral Tüp Defektleri Spektrumu: Spina Bifida, Anensefali, Ensefalosel",
        "subtitle": "Kranial ve kaudal nöropor açık kalma patolojileri",
        "badge": "Nöral Tüp Defektleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Nöral tüp defektleri (NTD), nöral kanalın herhangi bir anatomik seviyede kapanamaması sonucu sinir dokusunun açıkta kalması "
            "veya kemik örtüsünün oluşamamasıyla karakterize doğumsal anomaliler spektrumudur. Defektin yerleşim yerine göre üç ana klinik "
            "form tanımlanır: Spina bifida, Anensefali ve Ensefalosel.\n\n"
            "> [SINAV SPOTU] Nöral tüpün anterior (baş) kısmının açık kalması yaşamla bağdaşmayan ANENSEFALİ tablosunu; posterior (omurilik) "
            "kısmının açık kalması ise alt ekstremite felçleri ve inkontinansla seyreden SPİNA BİFİDA (meningomiyelosel) tablosunu üretir.\n\n"
            "Anensefalide serebral hemisferler ve kafatası kemikleri gelişmez, bebekler intrauterin ölür veya doğumdan birkaç saat sonra kaybedilir. "
            "Spina bifidalı çocuklarda ise ömür boyu tekerlekli sandalye bağımlılığı, Arnold-Chiari malformasyonu ve hidrosefali gelişir."
        ),
        "medicalTerms": [
            {"term": "Spina Bifida (Ayrık Omurga)", "explanation": "Vertebra arkuslarının birleşememesi sonucu omurilik ve meninkslerin dışarı fıtıklaşmasıdır."},
            {"term": "Anensefali", "explanation": "Ön nöroporun kapanamaması nedeniyle kalvaryum ve beyin hemisferlerinin yokluğudur; fataldir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Folat eksikliğinde görülen en sık iki NTD formu anensefali ve spina bifidadır.",
            "📌 [SINAV SPOTU] Spina bifida nörolojik defisit, Arnold-Chiari malformasyonu ve hidrosefaliye yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Anensefali", "desc": "Kranial defekt; yaşamla bağdaşmayan fatal beyin yokluğudur.", "isKey": True},
                {"title": "Spina Bifida", "desc": "Omurga kanalı açıklığı; parapleji ve hidrosefali sekeli bırakır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Folat eksikliğinde kranial nöroporun kapanamaması sonucu serebral hemisferlerin ve kafatasının gelişmediği fatal tabloya anensefali denir.",
                "anensefali",
                "Beyin ve kalvaryumun yokluğu anomalisi"
            ),
            make_active_recall(
                "Nöral tüpün ön (kranial) ve arka (kaudal) uçlarının kapanamaması sonucu gelişen iki temel anomali nedir?",
                "Ön ucun kapanamaması anensefaliye (beyin yokluğu); arka ucun kapanamaması ise spina bifidaya (ayrık omurga ve omurilik fıtıklaşması) yol açar."
            )
        ]
    })

    # ADIM 63
    slides.append({
        "slideNumber": 63,
        "title": "Folik Asit Profilaksi Protokolü: 400 mcg vs 4000 mcg (4 mg)",
        "subtitle": "Standart gebe için 400 mcg; NTD öykülü yüksek riskli gebede 10 kat doz (4 mg)",
        "badge": "Profilaksi Protokolü",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Nöral tüp defektlerinin önlenmesinde uygulanan farmakolojik folik asit profilaksisi gebelerin risk durumuna göre iki "
            "farklı dozajda uygulanır. Düşük riskli, daha önce anomalili gebeliği bulunmayan tüm kadınlarda gebe kalmadan 3 ay önce "
            "başlanıp gebeliğin ilk 12 haftası boyunca sürdürülen standart doz günlük 400 mikrogramdır (0,4 mg/gün).\n\n"
            "> [SINAV SPOTU] Standart gebelerde folik asit dozu: Gebe kalmadan 3 ay önce 400 mcg/gün (0,4 mg). Önceki gebeliğinde "
            "NTD öyküsü olan, kendisinde/eşinde NTD bulunan veya antiepileptik (valproat/karbamazepin) kullanan yüksek riskli gebelerde "
            "ise doz 10 KAT ARTIRILARAK GÜNLÜK 4000 MCG (4 MG/GÜN) olarak verilir!\n\n"
            "Diyetle bu yüksek seviyelere (özellikle 4 mg) ulaşmak imkansız olduğundan, tıbbi tablet formunda sentetik folik asit verilmesi "
            "uluslararası kılavuzların tartışmasız ortak emridir."
        ),
        "medicalTerms": [
            {"term": "Standart Profilaksi Dozu", "explanation": "Düşük riskli tüm kadınlarda önerilen günlük 400 mcg (0,4 mg) folik asit takviyesidir."},
            {"term": "Yüksek Riskli Doz (4 mg)", "explanation": "Önceki gebeliğinde NTD olan veya valproat kullanan kadınlara verilen günlük 4000 mcg folik asittir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Rutin gebe kalmadan 3 ay önce başlanan standart folik asit dozu: 400 mcg/gün.",
            "📌 [SINAV SPOTU] Önceki gebelikte NTD öyküsü varlığında doz: 4000 mcg/gün (4 mg/gün - tam 10 kat artış).",
            "📌 [SINAV SPOTU] Profilaksi ilk trimestr sonuna (12. haftaya) kadar kesintisiz devam ettirilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Standart: 400 mcg", "desc": "Tüm kadınlara prekonsepsiyonel 3 ay önce başlanan koruma dozu.", "isKey": True},
                {"title": "Yüksek Risk: 4 mg", "desc": "Önceki öyküde tekrarlama riskini kıran 10 kat yüksek dozdur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Daha önce spina bifidalı bebek doğurmuş yüksek riskli bir gebenin yeni gebelik planında günlük folik asit dozu 4000 mcg seviyesine çıkarılır.",
                "4000 mcg",
                "Yüksek riskli gebedeki 4 mg'lık dozun mikrogram değeri"
            ),
            make_active_recall(
                "Standart planlı bir gebede ve daha önce nöral tüp defektli bebek doğurmuş yüksek riskli bir gebede uygulanacak folik asit profilaksi dozları ve başlama zamanları nasıldır?",
                "Her iki grupta da gebelikten 3 ay önce başlanır. Standart gebede günlük doz 400 mcg (0,4 mg) iken, yüksek riskli gebede doz 10 katına çıkarılarak günlük 4000 mcg (4 mg) olarak verilir."
            )
        ]
    })

    # ADIM 64
    slides.append({
        "slideNumber": 64,
        "title": "Gebelikte En Sık Beslenme Yetersizliği: Demir Eksikliği Anemisi",
        "subtitle": "Küresel gebelerin %40'ını etkileyen en yaygın mikronütrient açığı",
        "badge": "Demir Eksikliği",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte hem gelişmiş hem de gelişmekte olan ülkelerde en sık karşılaşılan tekil beslenme yetersizliği tablosu "
            "'Demir Eksikliği Anemisi'dir. Dünya Sağlık Örgütü tahminlerine göre dünyadaki tüm gebe kadınların yaklaşık %40'ı, "
            "gelişmekte olan ülkelerde ise gebelerin yarısından fazlası anemiktir.\n\n"
            "> [SINAV SPOTU] Gebelikte en sık görülen beslenme yetersizliği DEMİR EKSİKLİĞİ ANEMİSİ'dir. Maternal ölüm, preterm doğum "
            "ve düşük doğum ağırlığının en yaygın hazırlayıcısıdır.\n\n"
            "Doğurganlık çağındaki kadınların menstrüel kanamalar nedeniyle zaten yetersiz demir depolarıyla gebeliğe başlaması ve gebelikte "
            "fetal-plasental dokuların demir talebinin katlanması, demir eksikliğini kaçınılmaz bir halk sağlığı problemi haline getirir."
        ),
        "medicalTerms": [
            {"term": "Demir Eksikliği Anemisi (DEA)", "explanation": "Hemoglobin sentezi için gerekli demirin tükenmesiyle ortaya çıkan mikrositer hipokrom anemidir."},
            {"term": "Demir Deposu (Ferritin)", "explanation": "Karaciğer ve retiküloendotelyal sistemde demiri depolayan ve kanda <15-30 ng/ml olduğunda tükenmeyi gösteren proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelikte en sık görülen nutrisyonel yetersizlik demir eksikliği anemisidir.",
            "📌 [SINAV SPOTU] Demir eksikliği maternal enfeksiyon riskini, doğum yorgunluğunu ve kanamayı tolere edememe riskini katlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "En Sık Yetersizlik", "desc": "Demir eksikliği gebelikteki nütrisyonel bozuklukların zirvesindedir.", "isKey": True},
                {"title": "Yetersiz Depolar", "desc": "Gebelik öncesi boş depolar artan ihtiyacı karşılayamaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte dünya genelinde en sık karşılaşılan nutrisyonel mikrobesin yetersizliği demir eksikliği anemisi tablosudur.",
                "demir eksikliği anemisi",
                "Gebelikteki en yaygın anemi nedeni"
            ),
            make_active_recall(
                "Gebelikte en sık görülen beslenme yetersizliği hangisidir ve doğurganlık çağındaki kadınların bu tabloya yatkın olmasının nedeni nedir?",
                "En sık beslenme yetersizliği demir eksikliği anemisidir. Doğurganlık çağındaki kadınlar menstrüel kan kayıpları ve yetersiz hayvansal beslenme nedeniyle gebeliğe zaten tükenmiş demir depolarıyla başlarlar."
            )
        ]
    })

    # ADIM 65
    slides.append({
        "slideNumber": 65,
        "title": "Maternal Demir Dengesi: Toplam 1000 mg Demir İhtiyacı",
        "subtitle": "Fetüs, plasenta, eritrosit artışı ve doğum kanaması için demir bütçesi",
        "badge": "Demir Dengesi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Tek bir gebelik sürecinin başarıyla tamamlanabilmesi için anne vücudunun karşılamak zorunda olduğu toplam net demir "
            "bütçesi yaklaşık 1000 miligramdır (1 gram saf demir). Bu devasa demir ihtiyacı şu dört kompartmana paylaştırılır: "
            "1) Fötus ve plasenta dokusu için ~300-350 mg, 2) Maternal eritrosit kütlesinin genişlemesi için ~450-500 mg, "
            "3) Doğum sırasındaki kan kaybı için ~200-250 mg ve 4) Günlük bazal kayıplar (cilt, ter, dışkı) için ~200 mg.\n\n"
            "> [SINAV SPOTU] Gebelikte gereken toplam demir miktarı yaklaşık 1000 mg'dır; bu miktarın normal bir diyetle (diyetteki "
            "demirin ancak %10'u emilebildiğinden) karşılanması BİYOLOJİK OLARAK İMKANSIZDIR!\n\n"
            "Bu nedenle hiçbir gebe kadın yalnızca ıspanak veya pekmez yiyerek demir ihtiyacını kapatamaz; mutlaka medikal demir "
            "takviyesi şarttır."
        ),
        "medicalTerms": [
            {"term": "Maternal Demir Bütçesi", "explanation": "Gebelik boyunca fetüs, plasenta ve genişleyen kan hacmi için tüketilen 1000 mg'lık toplam demir havuzudur."},
            {"term": "Fetal Demir Önceliği", "explanation": "Anne anemik olsa dahi plasental transferrin reseptörleriyle demirin öncelikle fetüse çekilmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelik boyunca gereken toplam demir miktarı yaklaşık 1000 mg'dır.",
            "📌 [SINAV SPOTU] Diyetle bu miktar karşılanamaz; rutin demir profilaksisi halk sağlığı zorunluluğudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1000 mg Demir", "desc": "Tüm gebeliğin fötal ve maternal toplam demir maliyetidir.", "isKey": True},
                {"title": "Diyet Yetersizliği", "desc": "Normal beslenme emilim sınırları nedeniyle 1000 mg'ı temin edemez.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte genişleyen eritrosit kitlesi, fetüs ve plasenta için gereken toplam demir miktarı yaklaşık 1000 mg düzeyindedir.",
                "1000 mg",
                "Gebelikteki toplam demir bütçesi"
            ),
            make_active_recall(
                "Gebelikte gereken toplam demir miktarı ne kadardır ve bu miktar neden sadece gıdalarla karşılanamaz?",
                "Gereken miktar yaklaşık 1000 mg'dır. Diyetteki demirin ancak %10'u emilebildiği için, günde 1000 mg emilim sağlamak için gereken gıda miktarı insan tüketim kapasitesinin çok üzerindedir; bu yüzden takviye zorunludur."
            )
        ]
    })

    # ADIM 66
    slides.append({
        "slideNumber": 66,
        "title": "Diyet Demirinin Emilim Dinamikleri: Hem vs Non-Hem Demir",
        "subtitle": "Diyetteki demirin ancak %10'unun emilebilmesi kuralı",
        "badge": "Demir Biyoyararlanımı",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Diyetle alınan demir iki farklı kimyasal formda bulunur: 1) Hem demiri (organik Fe2+): Yalnızca et, balık ve kümes "
            "hayvanlarının miyoglobin ve hemoglobininde bulunur; emilim oranı %20-30 gibi yüksek düzeydedir ve diyet faktörlerinden "
            "etkilenmez. 2) Non-hem demiri (inorganik Fe3+): Kuru baklagiller, kuru meyveler, pekmez ve tahıllarda bulunur; emilim oranı "
            "son derece düşüktür (%2-5 civarı) ve diyet bileşenlerinden yoğun şekilde etkilenir.\n\n"
            "> [SINAV SPOTU] Karışık bir Türk tipi diyette bulunan toplam demirin ORTALAMA YALNIZCA %10'U bağırsaktan emilebilir! "
            "Demirden zengin besinler: kırmızı et, tavuk, balık, kuru baklagiller, kuru meyveler, pekmez ve zenginleştirilmiş tahıllardır.\n\n"
            "Non-hem demirin emilebilmesi için midedeki asit ortamda ve C vitamini varlığında ferrik (Fe3+) formdan ferröz (Fe2+) forma "
            "indirgenmesi zorunludur."
        ),
        "medicalTerms": [
            {"term": "Hem Demiri", "explanation": "Et ürünlerinde porfirin halkasına bağlı bulunan ve doğrudan hem taşıyıcısıyla yüksek oranda emilen demirdir."},
            {"term": "Non-Hem Demiri", "explanation": "Bitkisel gıdalarda ferrik iyon halinde bulunan ve emilimi C vitaminiyle artan demirdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Diyetteki toplam demirin ortalama ancak %10'u emilebilir.",
            "📌 [SINAV SPOTU] Hem demiri (et) %25 oranında emilirken, bitkisel non-hem demiri ancak %2-5 oranında emilir.",
            "📌 [SINAV SPOTU] Demirden zengin besinler: Kırmızı et, kümes hayvanları, kuru baklagiller, kuru meyveler, pekmez."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "%10 Emilim Kuralı", "desc": "Alınan 15 mg demirin ancak 1,5 mg'ı kana geçebilir.", "isKey": True},
                {"title": "Hem Avantajı", "desc": "Hayvansal kaynaklı demir engelleyici faktörlerden etkilenmez.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Standart bir diyette bulunan toplam demirin biyolojik emilim kısıtlılığı nedeniyle ortalama yalnızca yüzde 10 kadarı emilir.",
                "yüzde 10",
                "Diyet demirinin ortalama bağırsak emilim yüzdesi"
            ),
            make_active_recall(
                "Hem demiri ile non-hem demiri arasındaki emilim farkları nelerdir ve diyetteki demirin ortalama ne kadarı emilebilir?",
                "Hem demiri (et) %20-30 oranında kolayca emilir; bitkisel non-hem demiri ise ancak %2-5 oranında emilir. Karışık bir diyette toplam demirin ortalama yalnızca %10'u emilebilir."
            )
        ]
    })

    # ADIM 67
    slides.append({
        "slideNumber": 67,
        "title": "Demir Emilimini Etkileyen Faktörler: C Vitamini vs Çay-Kahve",
        "subtitle": "Tanen ve polifenollerin şelasyon tuzağı ve askorbatın indirgeyici gücü",
        "badge": "Emilim Etkileşimi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Demir eksikliği anemisi olan bir gebede diyet düzenlemesi yapılırken ne yenildiği kadar, neyin neyle birlikte tüketildiği "
            "hayati önem taşır. Çay ve kahvede yoğun miktarda bulunan tanenler (tannik asit) ve polifenoller, kalsiyum tuzları ve "
            "tahıllardaki fitatlar; non-hem demirini bağırsak lümeninde çözünmeyen şelat kompleksleri halinde çökelterek emilimi bloke eder.\n\n"
            "> [SINAV SPOTU] Yemekle birlikte ÇAY VE KAHVE İÇİLMEMELİDİR (demir emilimini engeller; yemekten en az 1-2 saat sonra "
            "tüketilmelidir). C vitamininden zengin taze portakal suyu, kivi, domates ve yeşil salata ise demir emilimini katlar!\n\n"
            "Tek bir fincan demli çay yemekteki demir emilimini %60-70 oranında yok edebilirken; yemeğin yanına eklenen taze limonlu bir "
            "salata demir emilimini 3 katına çıkarabilir."
        ),
        "medicalTerms": [
            {"term": "Tanen (Tannik Asit)", "explanation": "Çay ve kahvede bulunan, demire bağlanarak çözünmez presipitat oluşturan polifenoldür."},
            {"term": "Askorbat Sinerjisi", "explanation": "C vitamininin demiri şelasyonlardan koruyarak duodenal DMT-1 kanalından emilimini artırmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yemekle birlikte çay ve kahve içilmemelidir; demir emilimini felç eder.",
            "📌 [SINAV SPOTU] C vitamininden zengin taze meyve ve sebzeler non-hem demirin kullanımını belirgin artırır.",
            "📌 [SINAV SPOTU] Kalsiyum içeren süt ve yoğurt demir preparatlarıyla aynı anda değil, farklı öğünde alınmalıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Çay-Kahve Yasağı", "desc": "Yemekle eşzamanlı çay tüketimi demiri bağırsağa kilitler.", "isKey": True},
                {"title": "C Vitamini Gücü", "desc": "Portakal suyu ve taze salata demir biyoyararlanımını 3 kat artırır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Yemeklerle birlikte tüketildiğinde demiri çökelterek emilimini engelleyen başlıca içecekler çay-kahve grubudur.",
                "çay-kahve",
                "Tanen içeren ve demir emilimini bozan içecekler"
            ),
            make_active_recall(
                "Gebelikte demir emilimini artıran ve engelleyen en önemli besinsel faktörler nelerdir?",
                "Artıran faktör: C vitamininden zengin taze meyve ve sebzelerdir (Fe3+'ü Fe2+'ye indirger). Engelleyen faktörler: Yemekle birlikte tüketilen çay-kahve (tanenler), kalsiyum ve tahıllardaki fitatlardır."
            )
        ]
    })

    # ADIM 68
    slides.append({
        "slideNumber": 68,
        "title": "Gebelikte Anemi Tanı Kriterleri: Trimestrlere Göre Eşikler",
        "subtitle": "1. ve 3. trimestrde Hb < 11 g/dl; 2. trimestrde Hb < 10,5 g/dl sınırı",
        "badge": "Anemi Eşikleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü (DSÖ) ve T.C. Sağlık Bakanlığı, gebelikte anemi tanısını laboratuvar düzeyinde hemoglobin (Hb) "
            "konsantrasyonuna göre kesin sınırlarla belirlemiştir. Gebe olmayan yetişkin bir kadında anemi sınırı Hb < 12 g/dl iken, "
            "gebelikteki fizyolojik hemodilüsyon nedeniyle bu eşik aşağı çekilir.\n\n"
            "> [SINAV SPOTU] DSÖ'ye göre gebelikte anemi tanımı: 1. ve 3. trimestrde Hemoglobin < 11 G/DL; 2. trimestrde ise "
            "(plazma hacmi artışının zirveye çıkması nedeniyle) Hemoglobin < 10,5 G/DL olarak tanımlanır.\n\n"
            "Hemoglobin değerinin 10,5 - 10,9 g/dl arasında olması ikinci trimestrde fizyolojik hemodilüsyon olarak yorumlanabilirken; "
            "birinci veya üçüncü trimestrde bu değer kesin anemi olarak kabul edilir ve tedavi dozu demir başlanmasını gerektirir."
        ),
        "medicalTerms": [
            {"term": "Trimestr Eşik Değeri", "explanation": "Plazma hacmi dalgalanmalarına göre anemi sınırının 11 veya 10,5 g/dl olarak ayrılmasıdır."},
            {"term": "Ağır Gebelik Anemisi", "explanation": "Hemoglobin düzeyinin 7 g/dl altına düşmesi ve kalp yetmezliği riski oluşturmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 1. ve 3. trimestr anemi sınırı: Hb < 11 g/dl.",
            "📌 [SINAV SPOTU] 2. trimestr anemi sınırı: Hb < 10,5 g/dl (hemodilüsyon zirvesi).",
            "📌 [SINAV SPOTU] Gebe olmayan kadında sınır 12 g/dl iken gebelikte 11 ve 10,5 g/dl'ye iner."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. & 3. Trimestr: <11", "desc": "Gebelikte anemi tanısı koyduran standart hemoglobin eşiğidir.", "isKey": True},
                {"title": "2. Trimestr: <10,5", "desc": "Plazma hacminin zirve yapmasıyla eşik yarım gram aşağı kayar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "DSÖ kriterlerine göre gebeliğin ikinci trimestrinde anemi tanısı koyabilmek için hemoglobin değerinin 10,5 g/dl altına inmesi gerekir.",
                "10,5 g/dl",
                "İkinci trimestr anemi hemoglobin sınırı"
            ),
            make_active_recall(
                "DSÖ'ye göre gebeliğin 1., 2. ve 3. trimestrlerinde anemi kabul edilen hemoglobin (Hb) eşik değerleri nelerdir?",
                "1. Trimestr: Hb < 11,0 g/dl; 2. Trimestr: Hb < 10,5 g/dl; 3. Trimestr: Hb < 11,0 g/dl."
            )
        ]
    })

    # ADIM 69 [CHECKPOINT 7]
    slides.append({
        "slideNumber": 69,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Folik Asit ve Demir Metabolizması İstasyonu",
        "subtitle": "NTD önleme (400 mcg vs 4 mg), 1000 mg demir bütçesi, %10 emilim ve anemi sınırları",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 7,
        "synthesisNarrative": (
            "Bu istasyon; nöral tüpün 28. günde kapanmasını, folik aside gebe kalmadan 3 ay önce başlanmasını, standart dozun 400 mcg "
            "iken NTD öykülü gebede 4000 mcg (4 mg) olmasını, spina bifida ve anensefaliyi, gebelikte en sık yetersizliğin demir eksikliği "
            "anemisi olmasını, gereken 1000 mg demirin normal diyetle karşılanamamasını, diyet demirinin yalnızca %10'unun emilmesini, "
            "çay-kahvenin emilimi bozup C vitamininin artırmasını ve DSÖ anemi sınırlarını (1. ve 3. trimestr <11; 2. trimestr <10,5 g/dl) "
            "pekiştirmektedir.\n\n"
            "> [YÜKSEK VERİM] Folat = 3 ay önce (400 mcg / 4 mg); NTD = 28. gün; Demir = 1000 mg bütçe, %10 emilim; Çay/kahve = yasak; "
            "Anemi eşiği = Hb < 11 g/dl (2. trimestrde < 10,5 g/dl)."
        ),
        "medicalTerms": [
            {"term": "Folat-Demir İkilisi", "explanation": "Gebelikte konjenital anomaliyi ve maternal mortaliteyi önleyen iki temel mikronütrienttir."},
            {"term": "Hemodilüsyon Sınırı", "explanation": "2. trimestrde 10,5 g/dl'ye inen hemoglobin tanı kriteridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Folik asit: 3 ay önce 400 mcg; NTD öyküsünde 4000 mcg (4 mg).",
            "📌 [SINAV SPOTU] Gebelikte en sık nutrisyonel yetersizlik: Demir eksikliği anemisi.",
            "📌 [SINAV SPOTU] Diyetteki demirin ancak %10'u emilir; toplam gereksinim ~1000 mg'dır.",
            "📌 [SINAV SPOTU] Anemi sınırı: 1. ve 3. trimestrde Hb < 11 g/dl; 2. trimestrde Hb < 10,5 g/dl."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Folat Protokolü", "desc": "Gebelikten 3 ay önce başlayarak NTD'yi %80 oranında siler.", "isKey": True},
                {"title": "Demir Zorunluluğu", "desc": "1000 mg bütçe ve %10 emilim takviyeyi mecbur kılar.", "isKey": True},
                {"title": "Trimestr Eşikleri", "desc": "2. trimestrde 10,5 g/dl; diğerlerinde 11 g/dl anemi kabul edilir.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-19",
                "Folik asit desteğine ne zaman başlanmalıdır ve standart gebe ile yüksek riskli gebedeki dozlar nelerdir?",
                "Gebe kalmadan 3 ay önce başlanmalıdır. Standart gebede 400 mcg/gün (0,4 mg); önceki gebelikte NTD olan gebede 4000 mcg/gün (4 mg) verilir.",
                "Folat zamanlama ve dozajı"
            ),
            make_flashcard(
                "fc-k1-06-20",
                "Gebelikte toplam ne kadar demire ihtiyaç vardır ve diyetteki demirin ortalama yüzde kaçı emilebilir?",
                "Toplam yaklaşık 1000 mg demir gereksinimi vardır; diyetteki toplam demirin ortalama yalnızca %10'u emilebilir.",
                "Demir ihtiyacı ve emilim oranı"
            ),
            make_flashcard(
                "fc-k1-06-21",
                "DSÖ kriterlerine göre gebelikte 1., 2. ve 3. trimestr anemi hemoglobin sınırları nelerdir?",
                "1. ve 3. trimestrde Hb < 11,0 g/dl; 2. trimestrde (fizyolojik hemodilüsyon zirvesi nedeniyle) Hb < 10,5 g/dl'dir.",
                "Trimestrlere göre anemi eşikleri"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Parametre / Besin Öğesi", "Standart Durum / Değer", "Özel / Riskli Durum Değeri"],
                [
                    [("Folik Asit Dozu", False, ""), ("Gebe kalmadan 3 ay önce 400 mcg/gün", False, ""), ("NTD öyküsünde 4000 mcg (4 mg/gün)", True, "Yüksek riskli gebedeki 10 kat doz")],
                    [("Anemi Hemoglobin Eşiği", False, ""), ("1. ve 3. trimestrde Hb < 11,0 g/dl", False, ""), ("2. trimestrde Hb < 10,5 g/dl", True, "İkinci üç aydaki özel anemi sınırı")],
                    [("Demir Emilim Verimi", False, ""), ("Diyetteki toplam demirin yüzde 10'u", False, ""), ("C vitamini ile 3 kat artış; çay ile blokaj", True, "Emilimi etkileyen besinsel faktörler")]
                ]
            )
        ]
    })

    # ADIM 70
    slides.append({
        "slideNumber": 70,
        "title": "Maternal Aneminin Doğum Eylemi ve Fetüs Üzerindeki Riskleri",
        "subtitle": "Kanamayı tolere edememe, kalp dekompansasyonu, IUGR ve preterm eylem",
        "badge": "Klinik Komplikasyonlar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte tedavi edilmeyen demir eksikliği anemisi, doğum masasında anneyi dakikalar içinde ölüme sürükleyebilen "
            "en sinsi hazırlayıcı faktördür. Normal bir doğumda kaybedilen 300-500 ml'lik kan, sağlıklı ve Hb düzeyi >11 g/dl olan "
            "bir gebe tarafından kolayca kompanse edilirken; anemik (Hb < 8 g/dl) bir gebede ani hipovolemik şok, miyokard enfarktüsü "
            "ve kardiyak arreste yol açar.\n\n"
            "> [SINAV SPOTU] Maternal aneminin sonuçları: Postpartum kanamayı tolere edememe, anne ölümü, puerperal sepsis artışı; "
            "fetal açıdan ise intrauterin gelişme geriliği (IUGR), preterm doğum ve bebeğin anemiyle doğmasıdır.\n\n"
            "Anemi aynı zamanda miyometriyum kas liflerinin oksijenlenmesini bozarak uterin atoni riskini artırır; yani hem kanamayı "
            "başlatır hem de başlayan kanamayı ölümcül kılar."
        ),
        "medicalTerms": [
            {"term": "Tolerans Kaybı", "explanation": "Kanda eritrosit azlığı nedeniyle minimal fizyolojik kanamalarda bile organ perfüzyonunun çökmesidir."},
            {"term": "Fetal Demir Deposu Yetersizliği", "explanation": "Ağır anemik anneden doğan bebeklerin süt çocukluğunda erken anemiye girmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anemik gebeler doğumdaki normal kan kayıplarını bile tolere edemeyerek arrest olabilir.",
            "📌 [SINAV SPOTU] Maternal anemi uterin doku hipoksisi yaparak postpartum atonik kanama riskini katlar.",
            "📌 [SINAV SPOTU] Bebekte preterm doğum ve düşük doğum ağırlığı riskini belirgin artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Şok Savunmasızlığı", "desc": "Hb düşüklüğü kan kaybına karşı fizyolojik tamponu yok eder.", "isKey": True},
                {"title": "Atoni Kısır Döngüsü", "desc": "Hipoksik rahim kası kasılamaz ve kanama durdurulamaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Ağır anemik gebelerde doğum sırasında uterus kasının oksijensiz kalarak kasılamaması uterin atoni ve masif kanama riskini katlar.",
                "uterin atoni",
                "Rahmin kasılamaması tablosu"
            ),
            make_active_recall(
                "Tedavi edilmemiş maternal demir eksikliği anemisi doğum sırasında anneyi neden ölümcül bir risk altına sokar?",
                "Miyometriyumun hipoksisi nedeniyle uterin atoni kanaması tetiklenir ve gebenin oksijen rezervi kalmadığı için normal kan kayıplarında bile kompanse edilemeyen akut hipovolemik şok ve kardiyak arrest gelişir."
            )
        ]
    })

    return slides
