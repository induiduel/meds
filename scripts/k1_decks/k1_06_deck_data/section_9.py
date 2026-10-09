"""
Bölüm 9: Gebelikte Sık Sağlık Sorunları, Toksemi, Pika ve Besinsel Tedavi İlkeleri
Adımlar: 81 - 90
Checkpoint: Adım 89 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # ADIM 81
    slides.append({
        "slideNumber": 81,
        "title": "Gebelikte Trimestrlere Göre Sık Görülen Fizyolojik Yakınmalar",
        "subtitle": "İlk 3 ay, tüm gebelik ve son 3 aya özgü semptom kronolojisi",
        "badge": "Semptom Kronolojisi",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Gebelikte hormonal ve mekanik adaptasyonların seyrine paralel olarak her trimestrde belirgin semptom grupları "
            "ön plana çıkar. İlk 3 ayda (1. trimestr) yükselen hCG ve östrojen nedeniyle bulantı-kusma ve aşırı tükürük salgısı "
            "(ptiyalizm) baskındır. Tüm gebelik boyunca kabızlık, diş eti problemleri, vajinal akıntı artışı, meme hassasiyeti, "
            "sık idrara çıkma, bayılma hissi, varis, hemoroid ve yorgunluk sürebilir.\n\n"
            "> [SINAV SPOTU] Son 3 ayda (3. trimestr) büyüyen uterusun mekanik basısı nedeniyle MİDE YANMASI VE REFLÜ, kas krampları, "
            "periferik ödem, solunum sıkıntısı, sırt-bel ağrısı, ellerde parestezi (karpal tünel) ve uykusuzluk pik yapar.\n\n"
            "Bu semptomların büyük kısmı fizyolojik değişimlerin doğal yansımasıdır; hekim ve ebenin rolü gereksiz ilaç kullanımını "
            "önleyerek semptomları yaşam tarzı ve diyet modifikasyonlarıyla hafifletmektir."
        ),
        "medicalTerms": [
            {"term": "Ptiyalizm (Siyalore)", "explanation": "Gebelikte özellikle ilk aylarda tükürük bezlerinin aşırı salgı yapması durumudur."},
            {"term": "Trimestr Kronolojisi", "explanation": "Gebelikte semptomların embriyonik, metabolik ve mekanik evrelere göre dağılımıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İlk 3 ay: Bulantı-kusma ve tükürük salgısında artış (ptiyalizm).",
            "📌 [SINAV SPOTU] Son 3 ay: Mide yanması/reflü, kas krampları, ödem, dispne ve sırt-bel ağrısı.",
            "📌 [SINAV SPOTU] Tüm gebelik boyu: Kabızlık, hemoroid, yorgunluk ve pollaküri."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İlk 3 Ay: Bulantı", "desc": "hCG pikine bağlı gastrointestinal adaptasyon semptomlarıdır.", "isKey": True},
                {"title": "Son 3 Ay: Mekanik Bası", "desc": "Büyüyen uterus diyaframı ve mideyi yukarı iterek reflü ve dispne yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebeliğin son 3 ayında büyüyen uterusun mideye mekanik bası yapmasıyla mide yanması ve reflü şikayetleri zirveye çıkar.",
                "mide yanması ve reflü",
                "Son trimestrdeki tipik gastrointestinal yakınma"
            ),
            make_active_recall(
                "Gebeliğin ilk 3 ayı ile son 3 ayında en sık görülen karakteristik yakınmalar nelerdir?",
                "İlk 3 ayda bulantı-kusma ve tükürük salgısı artışı; son 3 ayda ise mide yanması/reflü, kas krampları, alt ekstremite ödemi ve solunum sıkıntısıdır."
            )
        ]
    })

    # ADIM 82
    slides.append({
        "slideNumber": 82,
        "title": "Sabah Bulantısı (Emesis Gravidarum) ve Diyet Önlemleri",
        "subtitle": "hCG zirvesi, sabah kuru gıda atıştırma ve sık-az beslenme kuralı",
        "badge": "Bulantı Yönetimi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelik bulantı ve kusması (emesis gravidarum), gebelerin yaklaşık %70-80'ini etkileyen, genellikle 6. haftada başlayıp "
            "12-14. haftalarda (hCG düzeyinin plato çizip düşmesiyle) kendiliğinden gerileyen fizyolojik bir durumdur. Boş midede biriken "
            "asit ve hipoglisemi bulantıyı şiddetlendirir.\n\n"
            "> [SINAV SPOTU] Bulantı-kusmada temel diyet önerileri: Sabah yataktan kalkmadan önce TUZLU BİR ŞEYLER (kraker, leblebi, "
            "kızarmış ekmek) atıştırmak; SIK VE AZ YEMEK; kızartma, yağlı ve baharatlı gıdalardan kaçınmak; asitli içecekleri ve çay-kahveyi azaltmaktır.\n\n"
            "Sıvıların yemek sırasında değil, öğün aralarında yudum yudum tüketilmesi mide gerginliğini önleyerek kusma refleksini belirgin biçimde yatıştırır."
        ),
        "medicalTerms": [
            {"term": "Emesis Gravidarum", "explanation": "Gebelikte ilk trimestrde görülen, kilo kaybı ve dehidratasyon yapmayan hafif-orta bulantı-kusmadır."},
            {"term": "Sabah Kuru Gıda Kuralı", "explanation": "Uyanır uyanmaz yataktan doğrulmadan tuzlu kraker yiyerek mide asidini nötralize etme taktiğidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sabah yataktan kalkmadan önce tuzlu kraker/leblebi atıştırmak bulantıyı önler.",
            "📌 [SINAV SPOTU] Sık ve az beslenilmeli; kızartma, yağlı, baharatlı ve kokulu gıdalardan kaçınılmalıdır.",
            "📌 [SINAV SPOTU] Sıvılar yemekle değil, öğün aralarında yavaş yavaş içilmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kuru Kraker", "desc": "Mide boşken asidin mukozayı uyarmasını engelleyen ilk savunmadır.", "isKey": True},
                {"title": "Sık ve Az Porsiyon", "desc": "Mide distansiyonunu önleyerek vagal kusma uyarısını keser.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte sabah bulantısını engellemek için sabah yataktan kalkmadan önce tuzlu bir şey atıştırmak önerilir.",
                "tuzlu bir şey",
                "Sabah uyanınca ilk tüketilecek gıda niteliği"
            ),
            make_active_recall(
                "Gebelikte fizyolojik bulantı ve kusmayı hafifletmek için gebeye verilecek 4 temel diyet tavsiyesi nedir?",
                "1. Sabah yataktan kalkmadan tuzlu kraker/leblebi atıştırmak, 2. Az az ve sık sık beslenmek, 3. Yağlı, kızartma ve ağır baharatlılardan kaçınmak, 4. Sıvıları öğün aralarında tüketmektir."
            )
        ]
    })

    # ADIM 83
    slides.append({
        "slideNumber": 83,
        "title": "Hiperemezis Gravidarum (HG): Patolojik Kusma ve Yatış",
        "subtitle": "Kilo kaybı (>%5), dehidratasyon, ketonüri ve sıvı-elektrolit tedavisi",
        "badge": "Hiperemezis",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelik bulantı ve kusması inatçı hale gelip annenin oral beslenmesini tamamen imkansız kıldığında tablo 'Hiperemezis Gravidarum' "
            "(HG) olarak adlandırılan ciddi bir klinik patolojiye dönüşür. HG gebeliklerin yaklaşık %0,5 - 2'sinde görülür ve birinci "
            "trimestrde hastaneye yatışların en sık nedenidir.\n\n"
            "> [SINAV SPOTU] Hiperemezis Gravidarum tanı kriterleri: Sürekli inatçı kusma, gebelik öncesi vücut ağırlığının >%5'inden "
            "fazla KİLO KAYBI, dehidratasyon, elektrolit imbalansı (hipokalemi) ve idrarda KETONÜRİ varlığıdır.\n\n"
            "HG hastanesinde yatırılarak tedavi edilir; oral alım 24-48 saat kesilir, intravenöz sıvı-elektrolit infüzyonu, tiamin (B1 vitamini - "
            "Wernicke ensefalopatisini önlemek için) ve parenteral beslenme uygulanır."
        ),
        "medicalTerms": [
            {"term": "Hiperemezis Gravidarum", "explanation": "İnatçı kusma, %5'ten fazla kilo kaybı, ketonüri ve sıvı-elektrolit bozukluğuyla seyreden ağır tablodur."},
            {"term": "Wernicke Ensefalopatisi", "explanation": "Uzamış kusmada tiamin (B1) verilmeden dekstroz infüzyonu yapıldığında gelişen serebral hasardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hiperemezis kriteri: >%5 kilo kaybı, dehidratasyon ve idrarda ketonüri.",
            "📌 [SINAV SPOTU] Hiperemezis tablosunda tedavi hastanede yatırılarak sıvı-elektrolit ve parenteral destekle yapılır.",
            "📌 [SINAV SPOTU] Dekstroz takılmadan önce mutlaka Tiamin (B1 vitamini) verilmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": ">%5 Kilo Kaybı", "desc": "Maternal katabolizmanın ve açlığın laboratuvar kanıtıdır.", "isKey": True},
                {"title": "Ketonüri Varlığı", "desc": "Karbonhidrat tükenince yağların kontrolsüz yıkıldığını gösterir.", "isKey": True},
                {"title": "Hastanede Yatış", "desc": "Oral kesilip IV sıvı ve antiemetik tedavisi başlanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Ağır bulantı-kusması olan gebede açlık ve yağ katabolizması sonucu idrarda ketonüri saptanması hiperemezis gravidarum tanısını koydurur.",
                "ketonüri",
                "İdrarda keton cisimcikleri saptanması"
            ),
            make_active_recall(
                "Fizyolojik gebelik bulantısı ile hastaneye yatış gerektiren Hiperemezis Gravidarum arasındaki klinik ayrım kriterleri nelerdir?",
                "Hiperemeziste gebelik öncesi kilonun %5'inden fazla kayıp, klinik dehidratasyon bulguları, elektrolit bozuklukları ve idrarda belirgin ketonüri mevcuttur."
            )
        ]
    })

    # ADIM 84
    slides.append({
        "slideNumber": 84,
        "title": "Gastroözofageal Reflü ve Pirozis: Mide Yanması İlkeleri",
        "subtitle": "Alt özofagus sfinkter gevşemesi, yüksek yastık ve yatmadan önce yememe kuralı",
        "badge": "Reflü ve Pirozis",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Gebelikte mide yanması ve retrosternal pirozis, gebelerin yarısından fazlasında özellikle 2. ve 3. trimestrde ortaya "
            "çıkan son derece rahatsız edici bir semptomdur. İki mekanizma birleşir: 1) Progesteronun alt özofagus sfinkterini (AÖS) "
            "gevşetmesi, 2) Büyüyen uterusun mideyi yukarı ve sola doğru iterek intragastrik basıncı artırması.\n\n"
            "> [SINAV SPOTU] Mide yanmasında diyet ve yaşam tarzı kuralları: Bir defada az yemek, yavaş yemek ve iyi çiğnemek; "
            "YEMEKTEN HEMEN SONRA YATMAMAK; gaz yapıcı ve asit artırıcı besinlerden kaçınmak; uyumadan önce yememek ve BAŞI YÜKSEKTE UYUMAKTIR.\n\n"
            "Çikolata, nane, domates salçası, turunçgiller ve kızartmalar AÖS basıncını daha da düşürdüğü için kısıtlanmalı; antiasit "
            "kullanımı gerekirse alüminyumsuz ve sodyumsuz magnezyum-kalsiyum preparatları seçilmelidir."
        ),
        "medicalTerms": [
            {"term": "Pirozis (Mide Yanması)", "explanation": "Mide asidinin yemek borusu mukozasını tahriş etmesiyle göğüs kemiği arkasında hissedilen yanmadır."},
            {"term": "Anti-reflü Pozisyonu", "explanation": "Yerçekimi etkisiyle asit kaçışını engellemek için yatak başının 15-20 cm yükseltilmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mide yanmasında: Yemekten hemen sonra yatılmamalı, uyumadan en az 2-3 saat önce yeme kesilmelidir.",
            "📌 [SINAV SPOTU] Yatak başı yüksek tutulmalı, yemekler az porsiyonlarla ve iyi çiğnenerek tüketilmelidir.",
            "📌 [SINAV SPOTU] Çikolata, kahve, nane ve yağlı kızartmalar reflüyü tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yatıştan Önce Yememe", "desc": "Dolu mideyle uzanmak yerçekimi bariyerini sıfırlar.", "isKey": True},
                {"title": "Yüksek Yastık", "desc": "Yatak başını yükseltmek asidin özofagusa çıkışını önler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte mide yanması ve reflüyü önlemek için yemeklerden sonra hemen yatılmamalı ve uyurken başı yüksekte uyumak tercih edilmelidir.",
                "başı yüksekte",
                "Reflüyü engelleyen yatış pozisyonu"
            ),
            make_active_recall(
                "Gebelikte son dönemde sıklaşan mide yanması (reflü) yakınmasını engellemek için gebeye verilecek 4 temel yaşam tarzı önerisi nedir?",
                "1. Bir defada az yemek ve iyi çiğnemek, 2. Yemekten hemen sonra uzanmamak/yatmamak, 3. Uyumadan önce yememek, 4. Yatak başını yükselterek (başı yüksekte) uyumaktır."
            )
        ]
    })

    # ADIM 85
    slides.append({
        "slideNumber": 85,
        "title": "Gebelikte Konstipasyon (Kabızlık) ve Hemoroid Yönetimi",
        "subtitle": "Günde 8-12 bardak sıvı, posalı besinler ve düzenli fiziksel aktivite",
        "badge": "Kabızlık Yönetimi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte konstipasyon (kabızlık), kadınların yaklaşık %40'ını etkileyen ve progesterona bağlı bağırsak hipomotilitesi, "
            "kolondan artan su emilimi, uterusun rektuma mekanik basısı ve kullanılan oral demir preparatlarının yan etkisiyle tetiklenen "
            "kronik bir sorundur. Şiddetli kabızlık ve ıkınma, pelvik venöz göllenmeyle birleştiğinde ağrılı hemoroidlere yol açar.\n\n"
            "> [SINAV SPOTU] Konstipasyon yönetiminde altın kural: Günde 8 - 12 BARDAK SIVI (2-3 litre su); posadan zengin kuru baklagiller, "
            "kepekli/tam tahıllar, kuru meyveler (erik, kayısı, incir), taze sebze ve uygun hafif egzersizdir.\n\n"
            "Laksatif ilaçlar dehidratasyon ve uterus kontraksiyonlarını uyarabileceği için hekime danışılmadan asla kullanılmamalı; "
            "sorun beslenme ve posa zenginleştirmesiyle çözülmelidir."
        ),
        "medicalTerms": [
            {"term": "Diyet Posası (Lif)", "explanation": "Sindirim enzimleriyle parçalanmayan, suyu tutarak dışkı hacmini ve bağırsak peristaltizmini artıran karbonhidratlardır."},
            {"term": "Hemoroid", "explanation": "Ikınma ve pelvik bası nedeniyle rektal venlerin genişleyerek varisleşmesi ve tromboze olmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kabızlıkta sıvı hedefi: Günde 8 - 12 bardak sıvı.",
            "📌 [SINAV SPOTU] Diyet: Kuru baklagiller, kepekli tahıllar, kuru erik/kayısı ve taze sebzeler.",
            "📌 [SINAV SPOTU] Düzenli yürüyüş bağırsak peristaltizmini mekanik olarak uyarır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "8-12 Bardak Sıvı", "desc": "Kolonda sertleşen dışkıyı yumuşatmak için su tüketimi şarttır.", "isKey": True},
                {"title": "Çözünür ve Çözünmez Posa", "desc": "Kepekli tahıllar ve kuru meyveler bağırsak pasajını hızlandırır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte konstipasyonun önlenmesinde diyet posası artırılırken gebe kadına günde 8-12 bardak sıvı tüketmesi önerilir.",
                "8-12 bardak",
                "Günlük önerilen sıvı bardak aralığı"
            ),
            make_active_recall(
                "Gebelikte progesteron ve demir ilaçlarına bağlı gelişen kabızlığı çözmek için önerilen besinsel yaklaşım nedir?",
                "Günde 8 - 12 bardak sıvı tüketmek; posadan zengin kuru baklagil, kepekli tahıl, kuru ve taze meyve-sebze yemek ve düzenli hafif egzersiz yapmaktır."
            )
        ]
    })

    # ADIM 86
    slides.append({
        "slideNumber": 86,
        "title": "Pika Sendromu: Besin Olmayan Maddeleri Aşerme",
        "subtitle": "Toprak, kil, tebeşir, buz yeme; demir ve çinko eksikliği biyobelirteci",
        "badge": "Pika Sendromu",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Gebelikte görülen en ilginç ve klinik açıdan anlamlı yeme bozukluklarından biri 'Pika'dır. Pika; besin değeri taşımayan "
            "ve gıda dışı maddelerin (toprak - jeofaji, kil, kireç, tebeşir, çiğ nişasta - amilofaji, buz - pagofaji, kül, kahve telvesi) "
            "karşı konulamaz bir arzuyla sürekli yenmesi veya aşerilmesidir.\n\n"
            "> [SINAV SPOTU] Pika sendromu hemen daima altta yatan şiddetli DEMİR EKSİKLİĞİ ANEMİSİ veya ÇİNKO EKSİKLİĞİ ile ilişkilidir. "
            "Toprak ve kil yemek bağırsakta demiri bağlayarak anemiyi daha da derinleştiren bir kısır döngü yaratır!\n\n"
            "Pika davranışı gösteren gebede paraziter enfeksiyonlar, kurşun zehirlenmesi ve bağırsak tıkanması (obstrüksiyon) gelişebilir. "
            "Etiyolojideki demir ve çinko eksikliği medikal olarak düzeltildiğinde aşerme isteği hızla kaybolur."
        ),
        "medicalTerms": [
            {"term": "Pika Sendromu", "explanation": "Gıda dışı maddelerin (toprak, kil, tebeşir, buz vb.) aşırı ve kompulsif biçimde tüketilmesidir."},
            {"term": "Jeofaji", "explanation": "Pika kapsamında toprak veya kil yeme davranışıdır; parazit ve kurşun intoksikasyonu riski taşır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Pika sendromu demir ve çinko eksikliği ile doğrudan ilişkilidir.",
            "📌 [SINAV SPOTU] En sık tüketilen maddeler toprak, kil, tebeşir ve buzdur.",
            "📌 [SINAV SPOTU] Tedavide temel basamak demir preparatı replasmanıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Demir Eksikliği İmzası", "desc": "Vücudun mineral açlığı santral tat anomalisi üretir.", "isKey": True},
                {"title": "Toksisite Tehlikesi", "desc": "Toprak yemek parazit yumurtaları ve ağır metal zehirlenmesi yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte toprak, kil ve tebeşir gibi besin dışı maddeleri yeme alışkanlığına pika sendromu adı verilir.",
                "pika sendromu",
                "Besin dışı maddeleri yeme patolojisi"
            ),
            make_active_recall(
                "Pika sendromu nedir, gebelikte en sık hangi iki mikronütrient eksikliğine ikincil gelişir?",
                "Pika besin olmayan maddelerin (toprak, kil, tebeşir, buz) aşerilip yenmesidir; en sık şiddetli demir eksikliği anemisi ve çinko eksikliğine bağlı gelişir."
            )
        ]
    })

    # ADIM 87
    slides.append({
        "slideNumber": 87,
        "title": "Gebelik Toksemisi (Preeklampsi) ve Diyet Yanılgıları",
        "subtitle": "Hipertansiyon, proteinüri, ödem triadı ve tuz kısıtlamama gerçeği",
        "badge": "Toksemi ve Diyet",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Halk arasında 'gebelik zehirlenmesi' veya 'gebeliğin neden olduğu hipertansiyon' olarak bilinen toksemi; hipertansiyon, "
            "proteinüri ve patolojik ödem ile karakterizedir. Etiyolojisi tam aydınlatılamamış olmakla birlikte plasental iskemi, "
            "düşük sosyoekonomik düzey, prenatal bakımsızlık ve protein-kalori yetersizliği ile güçlü korelasyon gösterir.\n\n"
            "> [SINAV SPOTU] Preeklampside en yaygın klinik hata gebe kadının diyetinden TUZUN TAMAMEN ÇIKARILMASIDIR! Preeklampside "
            "zaten intravasküler hipovolemi vardır; tuzu aşırı kısıtlamak plasental perfüzyonu çökerterek fötal distresi tetikler.\n\n"
            "Besinsel bir eksiklik yoksa özel bir diyet değişikliği gerekmez; gebe normal tuzlu, proteini ve kalsiyumu yeterli dengeli "
            "diyetine devam etmelidir. Ödem için asla diüretik ilaç verilmemelidir."
        ),
        "medicalTerms": [
            {"term": "Gebelik Toksemisi", "explanation": "20. haftadan sonra kan basıncı yüksekliği, protein kaçağı ve ödemle seyreden preeklampsi tablosudur."},
            {"term": "İntravasküler Hipovolemi", "explanation": "Preeklampside damar içi sıvının dokulara kaçması sonucu damar yatağının susuz kalmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Toksemi triadı: Hipertansiyon + Proteinüri + Ödem.",
            "📌 [SINAV SPOTU] Toksemide tuz tamamen kesilmez; aşırı tuz kısıtlaması plasental kan akımını bozar.",
            "📌 [SINAV SPOTU] Yetersiz beslenme toksemi riskini artırır; protein ve kalsiyum desteği koruyucudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Klinik Triad", "desc": "Tansiyon yüksekliği, idrarda protein ve patolojik ödem.", "isKey": True},
                {"title": "Tuz Tuzağı", "desc": "Sıfır tuz diyeti intravasküler hacmi tüketerek bebeği tehlikeye atar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte hipertansiyon, proteinüri ve ödem ile karakterize klinik tabloya halk arasında gebelik toksemisi adı verilir.",
                "gebelik toksemisi",
                "Gebelik zehirlenmesi tıbbi terimi"
            ),
            make_active_recall(
                "Gebelik toksemisinin (preeklampsi) karakteristik klinik triadı nedir ve bu gebelerde neden aşırı tuz kısıtlaması yapılmamalıdır?",
                "Triad: Hipertansiyon, proteinüri ve ödemdir. Preeklampside damar içi sıvı azaldığından (intravasküler hipovolemi), tuzu aşırı kesmek uteroplasental kan akımını daha da bozarak fötal asfiksiye yol açabilir."
            )
        ]
    })

    # ADIM 88
    slides.append({
        "slideNumber": 88,
        "title": "Diş Eti Problemleri ve Gebelik Epulisi (Epulis Gravidarum)",
        "subtitle": "Östrojen ve progesterona bağlı gingival vaskülarizasyon ve C vitamini",
        "badge": "Oral Sağlık",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte yüksek östrojen ve progesteron hormonları, diş eti mukozasında damarlanmayı (anjiyogenez) artırır ve gingival "
            "ödem yaratır. Bu durum bakteriyel plaklara karşı aşırı bir inflamatuar yanıta yol açarak 'gebelik gingivitisi' ve lokalize "
            "bir piyojenik granülom türü olan 'Epulis gravidarum' (gebelik epulisi) lezyonlarının gelişmesine zemin hazırlar.\n\n"
            "> [SINAV SPOTU] Gebelikte diş eti kanamaları sık görülür; yönetimde yumuşak kıllı fırça ve diş ipi kullanımı, yemeklerden "
            "sonra ağzın çalkalanması ve C vitamininden zengin taze sebze-meyve tüketimi esastır.\n\n"
            "Diş eti enfeksiyonları (periodontit) sistemik proinflamatuar sitokinler salarak erken doğum ve düşük doğum ağırlığı riskini "
            "2 katına çıkardığından, DÖB kapsamında dental muayene ihmal edilmemelidir."
        ),
        "medicalTerms": [
            {"term": "Epulis Gravidarum", "explanation": "Gebelikte diş etinde hormonal uyarı ve plak irritasyonuyla gelişen selim, kırmızı, kolay kanayan vasküler yumrudur."},
            {"term": "Gebelik Gingivitisi", "explanation": "Östrojen etkisiyle diş etlerinin ödemli, hiperemik ve fırçalarken kolayca kanar hale gelmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Diş eti problemleri: Yumuşak fırça, diş ipi ve C vitamini zengin beslenme ile kontrol edilir.",
            "📌 [SINAV SPOTU] Periodontal enfeksiyonlar erken doğum ve düşük doğum ağırlığı riskini artırır.",
            "📌 [SINAV SPOTU] Epulis gravidarum doğum sonrasında hormonların düşmesiyle çoğunlukla kendiliğinden geriler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hormonal Şişkinlik", "desc": "Östrojen diş eti kılcal damarlarını genişleterek kanamaya yatkınlaştırır.", "isKey": True},
                {"title": "C Vitamini Koruması", "desc": "Kollajen ve kapiller bütünlüğü destekleyerek kanamayı hafifletir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte diş etlerinde hormonal damarlanma artışına bağlı gelişen iyi huylu vasküler kitleye epulis gravidarum denir.",
                "epulis gravidarum",
                "Gebelikte diş etinde oluşan piyojenik granülom"
            ),
            make_active_recall(
                "Gebelikte diş eti problemlerini önlemek ve yönetmek için önerilen hijyen ve beslenme ilkeleri nelerdir?",
                "Yumuşak fırça ve diş ipi kullanmak, yemeklerden sonra ağzı suyla çalkalamak ve diş eti kapillerlerini güçlendiren C vitamininden zengin taze sebze ve meyveler tüketmektir."
            )
        ]
    })

    # ADIM 89 [CHECKPOINT 9]
    slides.append({
        "slideNumber": 89,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Gebelikte Sık Sorunlar ve Diyet İstasyonu",
        "subtitle": "Emesis, hiperemezis, reflü, konstipasyon, pika ve toksemi diyet yönetiminin konsolidasyonu",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 9,
        "synthesisNarrative": (
            "Bu istasyon; ilk 3 ayda bulantı/kusma, son 3 ayda reflü/dispne kronolojisini, sabah kuru gıda kuralını, hiperemezis gravidarumdaki "
            ">%5 kilo kaybı ve ketonüriyi, reflüde yemekten hemen sonra yatmama ve başı yüksekte uyuma taktiğini, kabızlıkta 8-12 bardak su "
            "ve posayı, pika sendromunun demir ve çinko eksikliği bağlantısını, gebelik toksemisinde tuzu tamamen kesmeme ilkesini ve diş eti "
            "sağlığında C vitaminini konsolide eder.\n\n"
            "> [YÜKSEK VERİM] Bulantı = sabah kuru kraker; Hiperemezis = >%5 kilo kaybı + ketonüri (yatış); Reflü = yüksek yastık, tok "
            "yatmama; Kabızlık = 8-12 bardak su, posa; Pika = demir/çinko eksikliği; Toksemi = tuz kısıtlanmaz!"
        ),
        "medicalTerms": [
            {"term": "Diyetetik Semptom Protokolleri", "explanation": "Gebelikte ilaçsız yaşam tarzı ve besin zamanlamasıyla yakınmaları çözme yöntemleridir."},
            {"term": "Tuz Paradoksu", "explanation": "Preeklampside yaygın inancın aksine tuzu sıfırlamanın plasentayı iskemik bırakması gerçeğidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Bulantı: Sabah yataktan çıkmadan tuzlu kraker/leblebi; az ve sık beslenme.",
            "📌 [SINAV SPOTU] Hiperemezis: >%5 kilo kaybı, ketonüri; hastanede IV hidrasyon gerektirir.",
            "📌 [SINAV SPOTU] Reflü: Yemekten sonra hemen yatmama, başı yüksekte uyuma.",
            "📌 [SINAV SPOTU] Kabızlık: 8-12 bardak sıvı ve posa; Pika: Demir/çinko eksikliği; Toksemi: Tuz aşırı kısıtlanmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Gastrointestinal Sorunlar", "desc": "Bulantı, reflü ve kabızlık besin zamanlamasıyla hafifletilir.", "isKey": True},
                {"title": "Kritik Belirteçler", "desc": "Ketonüri hiperemezisi, toprak yeme demir açlığını gösterir.", "isKey": True},
                {"title": "Toksemide Diyet", "desc": "Tuz kesilmez, dengeli protein ve kalsiyum sürdürülür.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-25",
                "Gebelikte fizyolojik sabah bulantısı ve kusmasını önlemede en etkili diyet taktiği nedir?",
                "Sabah uyanınca yataktan hiç kalkmadan önce tuzlu bir şeyler (kraker, leblebi) atıştırmak ve gün boyu az az, sık sık beslenmektir.",
                "Bulantı önleme taktiği"
            ),
            make_flashcard(
                "fc-k1-06-26",
                "Hiperemezis Gravidarum tablosunu normal gebelik bulantısından ayıran ve hastaneye yatış gerektiren 3 majör bulgu nedir?",
                "Gebelik öncesi vücut ağırlığının %5'inden fazla kilo kaybı, klinik dehidratasyon/elektrolit bozukluğu ve idrarda ketonüri varlığıdır.",
                "Hiperemezis tanı kriterleri"
            ),
            make_flashcard(
                "fc-k1-06-27",
                "Pika sendromu nedir ve gebelikte hangi iki mineral eksikliği ile güçlü şekilde ilişkilidir?",
                "Pika besin olmayan maddelerin (toprak, kil, tebeşir, buz) aşerilip yenmesidir; şiddetli demir eksikliği ve çinko eksikliği ile ilişkilidir.",
                "Pika ve mineral eksiklikleri"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Gebelik Sağlık Sorunu", "Temel Patofizyolojik Neden", "Önerilen Besinsel ve Davranışsal Tedavi"],
                [
                    [("Sabah Bulantısı", False, ""), ("hCG piki ve açlıkta biriken mide asidi", False, ""), ("Yataktan kalkmadan tuzlu kraker atıştırmak", True, "Sabah bulantısını kesen kuru gıda taktiği")],
                    [("Mide Yanması (Reflü)", False, ""), ("AÖS sfinkter gevşemesi ve uterusun basısı", False, ""), ("Yemekten sonra yatmama ve başı yüksekte uyuma", True, "Reflüyü engelleyen yatış kuralı")],
                    [("Konstipasyon (Kabızlık)", False, ""), ("Progesteron hipomotilitesi ve demir hapları", False, ""), ("Günde 8-12 bardak sıvı ve posalı beslenme", True, "Bağırsak pasajını açan sıvı ve lif hedefi")]
                ]
            )
        ]
    })

    # ADIM 90
    slides.append({
        "slideNumber": 90,
        "title": "Klinik Karar Algoritması: Hafif Bulantıdan Hiperemezis Yatışına",
        "subtitle": "Kilo kaybı, ketonüri ve sıvı-elektrolit değerlendirmesinde basamaklı yaklaşım",
        "badge": "Klinik Karar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelik bulantısı ile başvuran bir gebenin klinik yönetimi basamaklı bir triyaj protokolü gerektirir. Birinci basamakta "
            "vital bulgular, kilo takibi ve idrar tahlili değerlendirilir. Gebe kilo kaybetmemişse, idrarda keton negatifse ve mukozaları "
            "nemliyse ayaktan diyet modifikasyonu (kraker, sık-az yemek, zencefil, B6 vitamini - piridoksin) yeterlidir.\n\n"
            "> [SINAV SPOTU] Eğer gebe su dahi içemiyorsa, kilo kaybı >%5 ise, idrarda 2+ ketonüri ve ortostatik hipotansiyon varsa "
            "hasta DERHAL HASTANEYE YATIRILIR. Oral beslenme kesilerek IV hidrasyon ve tiamin replasmanı başlatılır.\n\n"
            "Bu ayrımı doğru yapmak hem anneyi ölümcül Mallory-Weiss yırtığı ve Wernicke ensefalopatisinden korur hem de fetüsün "
            "erken dönemde ağır keton toksisitesine maruz kalmasını engeller."
        ),
        "medicalTerms": [
            {"term": "Mallory-Weiss Yırtığı", "explanation": "Şiddetli öğürme ve kusma sonucu gastroözofageal bileşkede mukozal laserasyon ve hematemez gelişmesidir."},
            {"term": "Piridoksin (B6 Vitamini)", "explanation": "Gebelikte hafif-orta bulantı ve kusmanın medikal tedavisinde ilk basamak güvenli vitamindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kilo kaybı yok, keton negatif -> Diyet ve B6 vitamini ile ayaktan takip.",
            "📌 [SINAV SPOTU] Kilo kaybı >%5, ketonüri pozitif -> Hastaneye yatış, IV sıvı ve tiamin.",
            "📌 [SINAV SPOTU] İnatçı kusmalarda parenteral dekstroz öncesi tiamin verilmesi kuraldır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hafif Form", "desc": "Ayaktan kuru gıda, sık porsiyon ve piridoksin desteği.", "isKey": True},
                {"title": "Hiperemezis Formu", "desc": "Hastanede yatış, IV izotonik infüzyonu ve parenteral izlem.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "8 haftalık gebe kadın günde 6-7 kez kustuğunu, 4 kilo verdiğini (gebelik öncesi 60 kg) belirtiyor. İdrar tahlilinde 3+ keton saptanıyor.",
                [
                    {
                        "text": "Evde tuzlu kraker yemesini ve bol çay içmesini önerip 1 ay sonra kontrole çağırmak.",
                        "isCorrect": False,
                        "feedback": "Yanlış! Hastada >%5 kilo kaybı ve ağır ketonüri mevcuttur; bu tablo Hiperemezis Gravidarumdur ve evde takip edilemez."
                    },
                    {
                        "text": "Hastayı derhal servise yatırmak, oral alımı durdurup IV sıvı-elektrolit ve tiamin tedavisi başlatmak.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Doğru karar. Kilo kaybı %6,6 ve belirgin ketonüri varlığı acil hospitalizasyon ve IV hidrasyon gerektirir."
                    }
                ]
            ),
            make_active_recall(
                "Gebelikte kusması olan bir hastada ayaktan takip ile hastaneye yatış kararını belirleyen iki temel laboratuvar ve fizik muayene bulgusu nedir?",
                "Gebelik öncesi vücut ağırlığının %5'inden fazla kilo kaybı ve idrarda ketonüri varlığıdır."
            )
        ]
    })

    return slides
