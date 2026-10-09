"""
Bölüm 5: Gebelik Öncesi BKİ'ye Göre Ağırlık Artışı Hedefleri, Tekil ve Çoğul Gebelik Enerji İhtiyaçları
Adımlar: 41 - 50
Checkpoint: Adım 49 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # ADIM 41
    slides.append({
        "slideNumber": 41,
        "title": "Gebelikte Ağırlık Artışının Anatomik ve Fizyolojik Dağılımı",
        "subtitle": "Alınan yaklaşık 12,5 kg kilonun doku ve organ bazında paylaşımı",
        "badge": "Ağırlık Dağılımı",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Gebelikte önerilen ortalama 11,5 - 16,0 kg'lık kilo artışı, kontrolsüz bir maternal yağlanma değil; tam tersine "
            "son derece organize ve işlevsel bir biyolojik doku yapılanmasıdır. Normal bir tekil gebelikte termde kazanılan ortalama "
            "12,5 kilogramlık ağırlığın yaklaşık 3,3-3,5 kg'ını fetüsün kendisi, yaklaşık 0,7 kg'ını plasenta ve yaklaşık 0,8 kg'ını "
            "amniyon sıvısı (toplam fötal ünite ~5 kg) oluşturur.\n\n"
            "> [SINAV SPOTU] Maternal dokulardaki artış: Uterus kas kütlesi ~1,0 kg, meme dokusu ~0,5 kg, kan ve plazma hacmi artışı "
            "~1,5-2,0 kg, interstisyel sıvı ~1,5-2,0 kg ve emzirme için depolanan anne yağ dokusu ~3,5 kg'dır.\n\n"
            "Görüldüğü üzere kazanılan kilonun yarısından fazlası doğrudan dolaşım ve gebelik ürünlerine aittir. Bu nedenle gebelikte "
            "asla zayıflama diyeti yapılmamalı, kilo alımı doku büyümesini destekleyecek hızda tutulmalıdır."
        ),
        "medicalTerms": [
            {"term": "Fetal Ünite Ağırlığı", "explanation": "Bebek, plasenta ve amniyon sıvısının toplam kütlesidir (ortalama 5 kg)."},
            {"term": "Maternal Enerji Deposu", "explanation": "Laktasyon sürecinde günlük 500 kaloriyi karşılamak üzere depolanan fizyolojik yağdır (ortalama 3,5 kg)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelikteki 12,5 kg'lık artışın ~5 kg'ı bebek ve ekleri, ~3,5 kg'ı laktasyon yağ deposu, geri kalanı sıvı ve dokudur.",
            "📌 [SINAV SPOTU] Gebelikte kilo kısıtlaması fetal beyin gelişimini ve doğum ağırlığını bozar; zayıflama diyeti kontrendikedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bebek ve Ekleri", "desc": "Fetüs (~3,4 kg), plasenta (~0,7 kg) ve amniyon sıvısı (~0,8 kg).", "isKey": True},
                {"title": "Maternal Katkı", "desc": "Kan hacmi, uterus, meme dokusu ve emzirme yağ deposu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte fetüs, plasenta ve amniyon sıvısından oluşan fetal ünite doğumda toplam yaklaşık 5 kilogram ağırlığa ulaşır.",
                "5 kilogram",
                "Fetal ünite toplam ortalama ağırlığı"
            ),
            make_active_recall(
                "Gebelikte kazanılan ortalama 12,5 kg'lık ağırlığın anatomik dağılımında anneye ait doku ve depolar nelerdir?",
                "Uterus kas dokusu (~1 kg), meme dokusu (~0,5 kg), artan kan hacmi (~1,5-2 kg), hücre dışı sıvı (~1,5-2 kg) ve emzirmeye hazırlık yağ deposudur (~3,5 kg)."
            )
        ]
    })

    # ADIM 42
    slides.append({
        "slideNumber": 42,
        "title": "Gebelik Öncesi BKİ'ye Göre Kilo Kazanım Hedefleri",
        "subtitle": "Kişiye özgü ağırlık artışı planlaması ve IOM standartları",
        "badge": "BKİ Standartları",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte her kadına tek tip bir kilo alma hedefi dayatmak tıbbi olarak kabul edilemez bir hatadır. İdeal ağırlık artışı, "
            "kadının gebe kaldığı andaki 'Beden Kitle İndeksi'ne (BKİ = kg/m²) göre bireyselleştirilmelidir. Amerikan Tıp Enstitüsü (IOM) "
            "ve T.C. Sağlık Bakanlığı rehberleri gebelik öncesi vücut ağırlığına göre net kilo artışı koridorları çizmiştir.\n\n"
            "> [SINAV SPOTU] Gebelik öncesi BKİ'ye göre önerilen kilo artışları: Normal kilolu (20,0-24,9 kg/m²) için 11,5-16,0 kg; "
            "Fazla kilolu (25,0-29,9 kg/m²) için 7,0-11,5 kg; Obez (≥30 kg/m²) için EN AZ 6,0 kg'dır.\n\n"
            "Zayıf başlayan kadınların depolarını telafi edebilmesi için daha fazla (12,5-18,0 kg) kilo alması istenirken, obez gebelerde "
            "aşırı yağ dokusu bulunduğundan fetal gelişimi bozmayacak asgari artış hedeflenir."
        ),
        "medicalTerms": [
            {"term": "Beden Kitle İndeksi (BKİ)", "explanation": "Vücut ağırlığının boyun karesine bölünmesiyle (kg/m²) hesaplanan obezite sınıflandırma parametresidir."},
            {"term": "IOM Gebelik Kılavuzu", "explanation": "Maternal BKİ'ye göre gebelikte güvenli ağırlık artışı sınırlarını belirleyen uluslararası standarttır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] BKİ 20,0-24,9 (Normal) -> 11,5-16,0 kg ağırlık artışı.",
            "📌 [SINAV SPOTU] BKİ 25,0-29,9 (Hafif Şişman) -> 7,0-11,5 kg ağırlık artışı.",
            "📌 [SINAV SPOTU] BKİ ≥ 30,0 (Obez) -> En az 6,0 kg ağırlık artışı."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bireysel Hedef", "desc": "Kilo artışı koridoru gebelik öncesi tartıya göre belirlenir.", "isKey": True},
                {"title": "BKİ Koridorları", "desc": "Normal için 11,5-16 kg; obez için en az 6 kg esastır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte kilo kazanım hedefleri kadının gebelik öncesindeki beden kitle indeksi değerine göre belirlenir.",
                "beden kitle indeksi",
                "Boy ve kiloya dayalı indeks formülü"
            ),
            make_active_recall(
                "Gebelik öncesi BKİ değerlerine göre önerilen ağırlık artışı hedefleri nelerdir?",
                "BKİ 20,0-24,9 (Normal): 11,5-16,0 kg; BKİ 25,0-29,9 (Hafif şişman): 7,0-11,5 kg; BKİ ≥30 (Obez): En az 6,0 kg."
            )
        ]
    })

    # ADIM 43
    slides.append({
        "slideNumber": 43,
        "title": "Normal BKİ (20,0 - 24,9 kg/m²) Olan Gebede Kilo Yönetimi",
        "subtitle": "11,5 - 16,0 kg aralığı ve haftalık kilo artış temposu",
        "badge": "Normal BKİ",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebeliğe ideal vücut ağırlığıyla (BKİ 20,0 - 24,9 kg/m²) başlayan kadınlar, obstetrik ve neonatal komplikasyon riski "
            "en düşük olan gruptur. Bu gruptaki gebelerin tüm gebelik boyunca toplam 11,5 ile 16,0 kg arasında ağırlık kazanması önerilir. "
            "Bu artışın zamana dağılımı da toplam miktar kadar hayatidir.\n\n"
            "> [SINAV SPOTU] İlk trimestrde normal kilolu gebenin toplam 1,0 - 2,0 kg alması beklenir; 2. ve 3. trimestrde ise "
            "haftalık yaklaşık 400 gram (ayda ~1,5-2 kg) ağırlık artışı ideal kabul edilir.\n\n"
            "Haftalık artışın 1 kg'ı aşması aşırı sıvı tutulumu (preeklampsi ödemi) veya kontrolsüz kaloriye işaret ederken; ayda 1 kg'ın "
            "altında kalması fetal büyüme geriliği şüphesi doğurur."
        ),
        "medicalTerms": [
            {"term": "Haftalık Kilo Temposu", "explanation": "2. ve 3. trimestrde normal kilolu gebede haftada ortalama 0,4 kg'lık stabil tartı artışıdır."},
            {"term": "Patolojik Ağırlık Artışı", "explanation": "Haftada 1 kg'dan fazla ani kilo artışı, genellikle gizli preeklamptik ödem habercisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Normal BKİ'li gebenin hedefi: 11,5 - 16,0 kg toplam ağırlık artışıdır.",
            "📌 [SINAV SPOTU] 2. ve 3. trimestrde haftalık ideal artış hızı ortalama 400 gramdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "11,5 - 16,0 kg", "desc": "Normal BKİ'li kadının tüm gebelikteki altın standart kilo hedefidir.", "isKey": True},
                {"title": "Haftada 400 g", "desc": "İkinci ve üçüncü trimestrdeki dengeli haftalık artış hızıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelik öncesi BKİ değeri 20,0-24,9 olan normal kilolu gebelerde önerilen toplam ağırlık artışı 11,5-16,0 kg aralığındadır.",
                "11,5-16,0 kg",
                "Normal BKİ için önerilen kilo artış aralığı"
            ),
            make_active_recall(
                "Gebelik öncesi normal ağırlıkta olan bir kadının gebelik boyunca toplam ve ikinci yarıda haftalık kilo artış hedefleri nelerdir?",
                "Toplamda 11,5 - 16,0 kg ağırlık artışı; 2. ve 3. trimestrde haftalık ortalama 400 gram artış hedeflenir."
            )
        ]
    })

    # ADIM 44
    slides.append({
        "slideNumber": 44,
        "title": "Kilolu ve Obez Gebelerde Kilo Kısıtlama İlkeleri",
        "subtitle": "BKİ 25,0-29,9 için 7,0-11,5 kg; BKİ ≥30 için en az 6,0 kg",
        "badge": "Kilolu ve Obez",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Gebelikte obezite, preeklampsi, tromboemboli ve gestasyonel diyabet riskini 3-4 kat artıran bağımsız bir mortalite faktörüdür. "
            "Bu nedenle gebelik öncesi hafif şişman olan (BKİ 25,0 - 29,9 kg/m²) gebelerde toplam ağırlık artışı 7,0 - 11,5 kg ile "
            "sınırlandırılmalıdır. Gebelik öncesi obez olan (BKİ ≥ 30 kg/m²) kadınlarda ise önerilen artış en az 6,0 kg'dır "
            "(IOM aralığı 5,0 - 9,0 kg).\n\n"
            "> [SINAV SPOTU] BKİ 25,0-29,9 olan kadınlarda önerilen ağırlık artışı 7,0-11,5 kg; BKİ ≥30 olan obez kadınlarda ise "
            "EN AZ 6,0 KG ağırlık artışı önerilmektedir. Obez gebede bile zayıflama amaçlı kilo kaybı yasaktır!\n\n"
            "Obez gebelerin diyetinde kalori kısıtlaması yapılırken ketozise girilmemesi çok kritiktir; maternal keton cisimcikleri "
            "plasentayı geçerek fetüste nörolojik hasar ve zeka geriliği yapabilir."
        ),
        "medicalTerms": [
            {"term": "Maternal Ketozis", "explanation": "Açlık veya aşırı karbonhidrat kısıtlamasında yağların yakılmasıyla kanda keton birikmesi ve fetal nörotoksisitedir."},
            {"term": "Kontrollü Ağırlık Artışı", "explanation": "Obez gebede bebeğin büyümesini aksatmadan sadece fötal ünite kadar kilo alma stratejisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fazla kilolu (BKİ 25-29,9): 7,0 - 11,5 kg artış önerilir.",
            "📌 [SINAV SPOTU] Obez (BKİ ≥30): En az 6,0 kg artış önerilir; kilo verme diyeti kesinlikle yasaktır.",
            "📌 [SINAV SPOTU] Kilo verme çabası ketozis yaparak fetal beyin hasarına yol açabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "7,0 - 11,5 kg", "desc": "BKİ 25,0-29,9 aralığındaki hafif şişman gebelerin kilo hedefidir.", "isKey": True},
                {"title": "En Az 6,0 kg", "desc": "BKİ ≥30 obez gebelerin güvenli asgari ağırlık artışıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelik öncesi BKİ değeri 30 ve üzerinde olan obez gebelerde gebelik boyunca en az 6,0 kg ağırlık artışı hedeflenir.",
                "en az 6,0 kg",
                "Obez gebeler için önerilen asgari kilo artışı"
            ),
            make_active_recall(
                "Obez bir gebenin (BKİ ≥30) kilo almaması veya zayıflama diyeti uygulayarak kilo vermesi neden tıbben sakıncalıdır?",
                "Zayıflama diyeti maternal keton üretimini (açlık ketozisi) tetikler. Ketonlar plasentayı geçerek fötal santral sinir sistemi gelişimini bozar ve nörobilişsel gerilik yapar."
            )
        ]
    })

    # ADIM 45
    slides.append({
        "slideNumber": 45,
        "title": "Çoğul Gebeliklerde Kilo Artışı: İkiz ve Üçüz Gebelikler",
        "subtitle": "Üçüz gebelikte 23 kg hedefi ve fötal ünite katlanması",
        "badge": "Çoğul Gebelik",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Çoğul gebeliklerde (ikiz, üçüz) anne vücudunun karşılamak zorunda olduğu fötal ünite kütlesi katlanarak büyür. "
            "İki veya daha fazla fetüs, birden çok plasenta ve katlanan amniyon sıvısı hacmi nedeniyle ağırlık artışı hedefleri "
            "tekil gebeliklerden belirgin şekilde ayrışır.\n\n"
            "> [SINAV SPOTU] Normal kilolu ikiz gebeliklerde toplam 16,8 - 24,5 kg (ortalama 18-20 kg) ağırlık kazanımı önerilirken; "
            "ÜÇÜZ GEBELİKLERDE toplam 23 KG ağırlık artışı önerilmektedir.\n\n"
            "Çoğul gebeliklerde erken doğum riski çok yüksek olduğundan, ilk 24 haftada yeterli kilo alımının sağlanması (erken kilo kazanımı) "
            "bebeklerin düşük doğum ağırlığı ile doğmasını engelleyen en kritik prognostik faktördür."
        ),
        "medicalTerms": [
            {"term": "Çoğul Gebelik Ağırlık Hedefi", "explanation": "İkizlerde ~17-24 kg, üçüzlerde ise yaklaşık 23 kg olarak tanımlanan özel kilo koridorudur."},
            {"term": "Erken Gestasyonel Kilo Kazanımı", "explanation": "Çoğul gebelikte prematüre doğum öncesi ilk 20-24 haftada sağlanan hayat kurtarıcı kilo artışıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Üçüz gebeliklerde önerilen toplam ağırlık artışı yaklaşık 23 kg'dır.",
            "📌 [SINAV SPOTU] Çoğul gebeliklerde ilk iki trimestrde sağlanan kilo artışı prematüriteye bağlı mortaliteyi düşürür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Üçüzde 23 kg", "desc": "Üç bebeğin plasenta ve sıvı yükü için hedeflenen kilo artışıdır.", "isKey": True},
                {"title": "İkizde 17-24 kg", "desc": "İkiz bebeklerin organogenezini destekleyen kilo bandıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Beslenme kılavuzlarında üçüz gebelik yaşayan kadınlar için önerilen toplam ağırlık artışı 23 kg olarak belirtilmiştir.",
                "23 kg",
                "Üçüz gebelik için önerilen toplam kilo miktarı"
            ),
            make_active_recall(
                "Üçüz gebelikte önerilen toplam ağırlık artışı kaç kilogramdır ve çoğul gebelikte ilk 24 haftada kilo alımı neden hayatidir?",
                "Önerilen ağırlık artışı 23 kg'dır. İlk 24 haftadaki kilo alımı, kaçınılmaz erken doğum durumunda bebeklerin düşük doğum ağırlığına girmesini engeller."
            )
        ]
    })

    # ADIM 46
    slides.append({
        "slideNumber": 46,
        "title": "Adolesan Gebelikte Kilo Yönetimi: Büyüme Rekabeti",
        "subtitle": "Kılavuz önerilerinin üst sınırını hedefleme zorunluluğu",
        "badge": "Adolesan Beslenmesi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Adolesan gebelikler (özellikle <18 yaş ve menarştan sonraki ilk 2 yıl), anne ve fetüsün besin ögeleri için doğrudan "
            "biyolojik rekabete girdiği en hassas tablolardır. Genç adölesanın kendi epifiz plakları henüz kapanmamış, iskelet kemik "
            "kütlesi ve organ büyümesi tamamlanmamıştır. Hem kendi büyümesini sürdürmek hem de karnındaki fetüsü beslemek zorunda kalır.\n\n"
            "> [SINAV SPOTU] Adolesan gebeliklerde ağırlık artışı hedeflenirken, BKİ'ye göre önerilen kilo koridorlarının DAİMA "
            "ÜST SINIRI hedeflenir (örneğin normal BKİ'de 16 kg'a yakın).\n\n"
            "Adolesan gebede yetersiz kilo alımı doğrudan intrauterin büyüme kısıtlılığına ve annenin boyunun kısa kalmasına yol açarken; "
            "üst sınırda dengeli beslenme her iki biyolojik organizmanın da tam potansiyeline ulaşmasını temin eder."
        ),
        "medicalTerms": [
            {"term": "Besin Rekabeti (Nutrient Partitioning)", "explanation": "Büyümekte olan adolesan anne ile fetüsün aminoasit ve mineralleri paylaşma çatışmasıdır."},
            {"term": "Üst Sınır Hedeflemesi", "explanation": "Adolesan annenin kemik mineralizasyonunu korumak için önerilen kilonun tavan değerine odaklanılmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Adolesan gebeliklerde ağırlık artışında BKİ önerilerinin daima üst sınırı hedeflenir.",
            "📌 [SINAV SPOTU] Genç adölesan kendi büyümesini tamamlamadığı için besin ihtiyacı yetişkin gebeden belirgin fazladır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Üst Sınır İlkesi", "desc": "Kilo koridorunun tavanı hedeflenerek anne büyümesi de korunur.", "isKey": True},
                {"title": "Kemik Koruma", "desc": "Kalsiyum ve protein açığı annede kalıcı boy kısalığı ve osteopeni yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Adolesan gebeliklerde annenin kendi biyolojik büyümesi devam ettiği için ağırlık artışı önerilerinin üst sınırı hedeflenir.",
                "üst sınırı",
                "Kilo koridorunun hedeflenen tepe noktası"
            ),
            make_active_recall(
                "Adolesan gebelerde ağırlık artışı planlanırken neden standart yetişkin önerilerinin üst sınırı hedeflenmelidir?",
                "Adolesan anne adayı kendi boy uzamasını ve kemik gelişimini tamamlamadığı için, hem kendi büyümesini sürdürmek hem de fetüsün ihtiyaçlarını karşılamak adına üst sınıra ihtiyaç duyar."
            )
        ]
    })

    # ADIM 47
    slides.append({
        "slideNumber": 47,
        "title": "Gebelikte Günlük Enerji Gereksinimi ve Toplam Kalori",
        "subtitle": "Günlük 2100 - 2500 kalori ve ortalama 300 - 500 kalori artışı",
        "badge": "Enerji İhtiyacı",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte bazal metabolizma hızının %15-20 artması, kardiyak ve solunumsal iş yükünün tırmanması ve yeni fetal-plasental "
            "dokuların sentezlenmesi maternal kalori ihtiyacını artırır. Ancak bu artış halk arasındaki abartılı algının aksine oldukça "
            "ölçülü bir düzeydedir.\n\n"
            "> [SINAV SPOTU] Gebe bir kadının günlük artan enerji ihtiyacı ortalama 300 - 500 KALORİDİR; gebenin günlük ortalama "
            "toplam enerji ihtiyacı ise 2100 - 2500 KALORİ aralığındadır.\n\n"
            "Günlük 300-500 kalorilik bu ek enerji, yaklaşık bir kase yoğurt, bir dilim tam tahıllı ekmek ve bir porsiyon meyveye denk "
            "gelmektedir. Dolayısıyla 'iki kat yemek' yerine kaliteli ve besin yoğunluğu yüksek gıdalarla bu kalori karşılanmalıdır."
        ),
        "medicalTerms": [
            {"term": "Bazal Metabolizma Hızı Artışı", "explanation": "Gebelikte tiroid aktivitesi ve fötal metabolizma ile BMR'nin yaklaşık %15-20 yükselmesidir."},
            {"term": "Besin Yoğunluğu (Nutrient Density)", "explanation": "Bir gıdanın içerdiği kaloriden bağımsız olarak vitamin, mineral ve protein zenginliğidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelikte günlük artan enerji ihtiyacı ortalama 300 - 500 kaloridir.",
            "📌 [SINAV SPOTU] Gebenin günlük toplam enerji ihtiyacı ortalama 2100 - 2500 kalori arasındadır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "300 - 500 kal Ek", "desc": "Gebelikte günlük fazladan gereken kalori miktarıdır.", "isKey": True},
                {"title": "2100 - 2500 kal Total", "desc": "Gebe kadının gün boyu alması gereken ortalama toplam enerjidir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte annenin günlük artan enerji ihtiyacı ortalama 300-500 kalori civarındadır.",
                "300-500 kalori",
                "Günlük ortalama ek kalori aralığı"
            ),
            make_active_recall(
                "Gebelikte günlük artan ek kalori ihtiyacı ve günlük ortalama toplam enerji gereksinimi ne kadardır?",
                "Günlük artan enerji ihtiyacı ortalama 300 - 500 kaloridir; günlük ortalama toplam enerji ihtiyacı ise 2100 - 2500 kalori aralığındadır."
            )
        ]
    })

    # ADIM 48
    slides.append({
        "slideNumber": 48,
        "title": "Çoğul Gebeliklerde Ek Kalori İhtiyacı: Tekil, İkiz, Üçüz",
        "subtitle": "Normal +340 kal/gün; İkiz +600 kal/gün; Üçüz +900 kal/gün",
        "badge": "Kalori Dağılımı",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Gebelikte fötus sayısı arttıkça maternal metabolizmanın desteklemesi gereken protein sentezi ve enerji harcaması "
            "lineer bir artış sergiler. Çoğul gebeliklerde tekil gebelik kalorisiyle beslenmek ağır bir anne katabolizması ve fetal "
            "açlık doğurur. Bu nedenle ders notlarında ve klinik kılavuzlarda fötus sayısına göre net ek kalori değerleri verilmiştir.\n\n"
            "> [SINAV SPOTU] Duruma göre günlük ek enerji gereksinimi: Normal tekil gebelikte +340 kal/gün; İKİZ GEBELİKTE "
            "+600 kal/gün; ÜÇÜZ GEBELİKTE ise +900 kal/gündür.\n\n"
            "Bu ek enerjinin boş karbonhidratlardan (şeker, hamur işi) değil, protein ve omega-3 yağ asitlerinden zengin kaynaklardan "
            "karşılanması çoğul gebeliklerde sık görülen erken doğum ve düşük doğum ağırlığı riskini minimuma indirir."
        ),
        "medicalTerms": [
            {"term": "Katlanan Kalori Talebi", "explanation": "İkizlerde ek 600, üçüzlerde ek 900 kalori ile fötal metabolizmanın desteklenmesidir."},
            {"term": "Protein-Kalori Orantısı", "explanation": "Kalori artırılırken her 100 kaloriye dengeli gramajda kaliteli protein eklenmesi kuralıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Normal gebelik: +340 kal/gün ek enerji.",
            "📌 [SINAV SPOTU] İkiz gebelik: +600 kal/gün ek enerji.",
            "📌 [SINAV SPOTU] Üçüz gebelik: +900 kal/gün ek enerji."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Tekil: +340 kal", "desc": "Standart tekiz gebelikteki günlük ilave kalori miktarıdır.", "isKey": True},
                {"title": "İkiz: +600 kal", "desc": "İki fötüsün metabolik yükünü karşılayan günlük ek enerjidir.", "isKey": True},
                {"title": "Üçüz: +900 kal", "desc": "Üçüz gebelikte hedeflenen günlük ek kalori artışıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Beslenme rehberlerine göre ikiz gebelik yaşayan bir kadının günlük diyetine eklemesi gereken enerji +600 kal/gün düzeyindedir.",
                "+600 kal/gün",
                "İkiz gebelikte önerilen ek günlük kalori"
            ),
            make_active_recall(
                "Tekil, ikiz ve üçüz gebeliklerde anne diyetine eklenmesi önerilen günlük kalori miktarları nelerdir?",
                "Normal tekil gebelik: +340 kal/gün; İkiz gebelik: +600 kal/gün; Üçüz gebelik: +900 kal/gün."
            )
        ]
    })

    # ADIM 49 [CHECKPOINT 5]
    slides.append({
        "slideNumber": 49,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Ağırlık Kazanımı ve Enerji İhtiyacı İstasyonu",
        "subtitle": "BKİ hedefleri, adölesan ve çoğul gebelik kilo/kalori değerlerinin konsolidasyonu",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 5,
        "synthesisNarrative": (
            "Bu istasyon; gebelikte kazanılan 12,5 kg'ın anatomik dağılımını (~5 kg fötal ünite, ~3,5 kg laktasyon yağı), gebelik öncesi "
            "BKİ'ye göre kilo hedeflerini (Normal: 11,5-16 kg; Kilolu: 7-11,5 kg; Obez: en az 6 kg), üçüz gebelikte 23 kg hedefini, "
            "adölesanlarda üst sınır ilkesini, gebenin günlük toplam 2100-2500 kalori ihtiyacını ve ek enerji tablosunu "
            "(Normal: +340 kal/gün, İkiz: +600 kal/gün, Üçüz: +900 kal/gün) pekiştirmektedir.\n\n"
            "> [YÜKSEK VERİM] Normal BKİ = 11,5-16 kg; Obez = En az 6 kg; Üçüz kilo = 23 kg; Gebe günlük kalori = 2100-2500 kal; "
            "Ek enerji: Tekiz +340, İkiz +600, Üçüz +900 kal/gün."
        ),
        "medicalTerms": [
            {"term": "BKİ Sınıflaması", "explanation": "Normal (20-24,9), Kilolu (25-29,9), Obez (≥30)."},
            {"term": "Çoğul Enerji Skalası", "explanation": "Fötus başına kademeli olarak artan 340 -> 600 -> 900 kalori basamaklarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Normal BKİ: 11,5 - 16,0 kg; Kilolu: 7,0 - 11,5 kg; Obez: En az 6,0 kg ağırlık artışı.",
            "📌 [SINAV SPOTU] Üçüz gebelik toplam kilo hedefi: 23 kg.",
            "📌 [SINAV SPOTU] Ek kalori: Tekil +340 kal/gün, İkiz +600 kal/gün, Üçüz +900 kal/gün."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "BKİ Aralıkları", "desc": "11,5-16 kg (normal), 7-11,5 kg (kilolu), ≥6 kg (obez).", "isKey": True},
                {"title": "Çoğul Değerleri", "desc": "Üçüzde 23 kg ağırlık ve +900 kal/gün ek enerji.", "isKey": True},
                {"title": "Toplam Enerji", "desc": "Günlük 2100-2500 kalori ve ortalama 300-500 kal artış.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-13",
                "Gebelik öncesi BKİ değerlerine göre önerilen toplam ağırlık artışı hedefleri nelerdir?",
                "BKİ 20,0-24,9 (Normal): 11,5-16,0 kg; BKİ 25,0-29,9 (Hafif şişman): 7,0-11,5 kg; BKİ ≥30 (Obez): En az 6,0 kg.",
                "BKİ kilo artışı tablosu"
            ),
            make_flashcard(
                "fc-k1-06-14",
                "Üçüz gebelik yaşayan bir kadın için önerilen toplam ağırlık artışı kaç kilogramdır?",
                "Yaklaşık 23 kg ağırlık artışı önerilmektedir.",
                "Üçüz gebelik kilo hedefi"
            ),
            make_flashcard(
                "fc-k1-06-15",
                "Normal, ikiz ve üçüz gebeliklerde diyetle eklenmesi gereken günlük enerji miktarları nelerdir?",
                "Normal tekil gebelik: +340 kal/gün; İkiz gebelik: +600 kal/gün; Üçüz gebelik: +900 kal/gün.",
                "Ek kalori gereksinimleri"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Gebelik Türü / Durum", "Önerilen Ağırlık Artışı", "Günlük Ek Enerji İhtiyacı"],
                [
                    [("Normal Tekil Gebelik (Normal BKİ)", False, ""), ("11,5 - 16,0 kg toplam artış", False, ""), ("+340 kal/gün ek enerji", True, "Tekil gebelikte günlük ek kalori")],
                    [("İkiz Gebelik", False, ""), ("16,8 - 24,5 kg toplam artış", False, ""), ("+600 kal/gün ek enerji", True, "İkiz gebelikte günlük ek kalori")],
                    [("Üçüz Gebelik", False, ""), ("Yaklaşık 23 kg toplam artış", True, "Üçüz gebelik için önerilen kilo artışı"), ("+900 kal/gün ek enerji", True, "Üçüz gebelikte günlük ek kalori")]
                ]
            )
        ]
    })

    # ADIM 50
    slides.append({
        "slideNumber": 50,
        "title": "Trimesterlere Göre Enerji Dağılımı ve Kalori Zamanlaması",
        "subtitle": "1. trimestrde ek kaloriye gerek yokken, 2. ve 3. trimestrde kademeli artış",
        "badge": "Kalori Zamanlaması",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte artan enerjinin 9 aya homojen dağıtılması biyolojik olarak hatalıdır. Birinci trimestrde (ilk 12-14 hafta) "
            "embriyonun büyüklüğü birkaç gramı geçmez ve maternal metabolik harcama henüz belirgin artmamıştır. Bu nedenle birinci "
            "trimestrde ek kaloriye pratik olarak GEREK YOKTUR; gebe normal dengeli beslenmesine devam etmelidir.\n\n"
            "> [SINAV SPOTU] Enerji artışı trimesterlere göre kademelidir: 1. Trimestrde ek kalori gerekmez; 2. Trimestrde "
            "+300-340 kal/gün; 3. Trimestrde ise hızlı fetal büyüme nedeniyle +450 kal/gün ek enerji önerilir.\n\n"
            "İlk trimestrde aşırı kalori almak sadece maternal yağlanmayı artırırken; 2. ve 3. trimestrde kaliteli protein ve enerji "
            "eklenmesi fötal beyin büyümesini ve doğum tartısını doğrudan destekler."
        ),
        "medicalTerms": [
            {"term": "Trimester Kademelendirmesi", "explanation": "Enerji ihtiyacının fötal büyüme hızına paralel olarak 2. ve 3. trimestrde artırılmasıdır."},
            {"term": "İlk Trimestr Enerji Nötralitesi", "explanation": "İlk 3 ayda fötal kütle küçük olduğu için kalori artışına ihtiyaç duyulmaması durumudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 1. trimestrde ek kalori gerekmez; normal dengeli beslenme yeterlidir.",
            "📌 [SINAV SPOTU] 2. trimestrde +340 kal/gün, 3. trimestrde +450 kal/gün ek kalori hedeflenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. Trimestr: 0 kal", "desc": "Embriyonik dönemde fazladan kalori alımına ihtiyaç yoktur.", "isKey": True},
                {"title": "2. Trimestr: +340", "desc": "Plazma hacmi ve organogenezin büyümesi için ek kalori başlar.", "isKey": True},
                {"title": "3. Trimestr: +450", "desc": "Hızlı fötal yağlanma ve ağırlık kazanımı zirveye çıkar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte ilk trimestrde fötal kütle çok küçük olduğu için günlük diyete ek kalori eklenmesine gerek yoktur.",
                "gerek yoktur",
                "İlk 3 aydaki ilave kalori gerekliliği durumu"
            ),
            make_active_recall(
                "Gebelikte trimesterlere göre ek kalori ihtiyacı nasıl değişir?",
                "1. Trimestrde ek kaloriye gerek yoktur (0 kal). 2. Trimestrde günlük +300-340 kalori, 3. Trimestrde ise günlük +450 kalori eklenmesi önerilir."
            )
        ]
    })

    return slides
