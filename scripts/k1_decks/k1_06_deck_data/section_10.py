"""
Bölüm 10: Emzirme Döneminde Beslenme Fizyolojisi, Anne Sütü Sentezi ve Kaçınılması Gereken Besinler
Adımlar: 91 - 100
Checkpoint: Adım 99 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # ADIM 91
    slides.append({
        "slideNumber": 91,
        "title": "Anne Sütü Sentez Fizyolojisi: Günlük 800 ml Üretim",
        "subtitle": "Her annenin sütü bebeğine özeldir; prolaktin/oksitosin ekseni ve mide kapasitesi",
        "badge": "Süt Sentezi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Anne sütü, bebeğin optimal büyüme, nörogelişim ve bağışıklık koruması için biyolojik olarak tasarlanmış eşsiz bir "
            "sıvı dokudur. Laktasyon fizyolojisinde prolaktin hormonu meme alveol hücrelerinde süt sentezini tetiklerken, oksitosin "
            "miyoeoepitelyal hücreleri kasarak sütü kanallara fışkırtır (let-down refleksi). Sağlıklı ve emziren bir kadın günde "
            "ortalama 750 - 800 ML SÜT üretir.\n\n"
            "> [SINAV SPOTU] Sağlıklı bir anne günde ortalama 800 ML süt salgılar. Yenidoğan bebeğin mide kapasitesi: 1. ayda "
            "120-150 ml, 3. ayda 150-180 ml ve 6. ayda 180-210 ml düzeyindedir.\n\n"
            "Gebelikte alınan yaklaşık 3,5 kg'lık fizyolojik yağ deposu, laktasyonun ilk aylarında gereken enerjinin bir kısmını "
            "sağlamak üzere kademeli olarak yakılır."
        ),
        "medicalTerms": [
            {"term": "Let-Down Refleksi (Süt İnme)", "explanation": "Bebeğin meme ucunu emmesiyle arka hipofizden salınan oksitosinin süt kanallarını boşaltmasıdır."},
            {"term": "Fizyolojik Mide Kapasitesi", "explanation": "Bebeğin 1. ayda 120-150 ml, 6. ayda yaklaşık 200 ml'ye ulaşan mide hacmidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sağlıklı bir anne günde ortalama yaklaşık 800 ml süt üretir.",
            "📌 [SINAV SPOTU] Bebek mide hacmi: 1. ayda 120-150 ml, 3. ayda 150-180 ml, 6. ayda 180-210 ml'dir.",
            "📌 [SINAV SPOTU] Emzirme gebelikte depolanan maternal yağların erimesini sağlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Günde 800 ml", "desc": "Maternal alveollerin ürettiği ortalama günlük süt hacmidir.", "isKey": True},
                {"title": "Bebek Midesi", "desc": "1. aydaki 120-150 ml'den 6. ayda 200 ml'ye kademeli büyür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Sağlıklı ve yeterli beslenen emzikli bir anne günde ortalama 800 ml anne sütü üretebilme kapasitesine sahiptir.",
                "800 ml",
                "Günlük ortalama üretilen anne sütü hacmi"
            ),
            make_active_recall(
                "Sağlıklı bir emziren annenin günlük ortalama süt üretim miktarı ve bebeğin 1., 3. ve 6. aylardaki mide kapasiteleri nelerdir?",
                "Anne günde ortalama 800 ml süt üretir. Bebek mide kapasitesi: 1. ayda 120-150 ml, 3. ayda 150-180 ml, 6. ayda 180-210 ml'dir."
            )
        ]
    })

    # ADIM 92
    slides.append({
        "slideNumber": 92,
        "title": "Maternal Beslenme ve Süt Miktarı: 'Fazla Yiyenin Sütü Artmaz'",
        "subtitle": "Süt miktarını emme refleksi belirler; 1800 kalori altı ise sütü keser",
        "badge": "Laktasyon Mitleri",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Toplumda emziren kadına sürekli aşırı tatlı, şerbet ve hamur işi yedirme baskısı mevcuttur. Oysa laktasyon fizyolojisinde "
            "kanıtlanmış en kesin gerçek: Yeterli beslenen bir annenin daha fazla beslenmesiyle süt yapımının ARTMAYACAĞIDIR. "
            "Süt miktarını belirleyen ana faktör annenin yediği yemek miktarı değil; bebeğin memeyi boşaltma sıklığı ve prolaktin uyarısıdır.\n\n"
            "> [SINAV SPOTU] Yeterli beslenen anne daha fazla beslenirse süt yapımı ARTMAZ! Yetersiz beslenen kadında ise süt miktarı "
            "azalabilir ancak kalitesi (yalnız protein ve yağ hafif düşer) korunur; GÜNLÜK 1800 KALORİNİN ALTI süt miktarını doğrudan düşürür!\n\n"
            "Anne ne kadar yetersiz beslenirse beslensin kendi dokularını yıkarak süt üretmeye devam eder; bu nedenle 'sütüm az' diyerek "
            "anne sütünden vazgeçilmemeli, ne kadar az olursa olsun bebeğe verilmelidir."
        ),
        "medicalTerms": [
            {"term": "1800 Kalori Eşiği", "explanation": "Emziren annede günlük kalori alımı bu seviyenin altına düştüğünde prolaktin sentezinin ve süt hacminin çökmesidir."},
            {"term": "Otomerokrin Geri Bildirim (FIL)", "explanation": "Memede süt kaldığında süt sentezini durduran yerel inhibitör peptiddir (Feedback Inhibitor of Lactation)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yeterli beslenen anne daha fazla yerse süt yapımı artmaz; kilo alır.",
            "📌 [SINAV SPOTU] Emziren kadında günlük 1800 kalorinin altı süt salgısını belirgin düşürür; şok zayıflama diyeti yasaktır.",
            "📌 [SINAV SPOTU] Ne kadar az olursa olsun anne sütü bebeğe mutlaka verilmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Arz-Talep Dengesi", "desc": "Sütü artıran gıda değil, bebeğin etkin ve sık emmesidir.", "isKey": True},
                {"title": "1800 Kalori Sınırı", "desc": "Aşırı kalori kısıtlaması prolaktin üretimini baltalar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Emziren kadında günlük enerji alımının 1800 kalorinin altına düşmesi anne sütü miktarını belirgin biçimde azaltır.",
                "1800 kalorinin",
                "Süt üretimini düşüren kritik kalori eşiği"
            ),
            make_active_recall(
                "Emziren annenin beslenmesi ile süt yapımı arasındaki ilişki nasıldır ve 'fazla beslenme sütü artırır mı'?",
                "Yeterli beslenen bir anne daha fazla beslenirse süt yapımı artmaz; süt miktarını belirleyen bebeğin emme uyarısıdır. Ancak annenin günlük 1800 kalorinin altına düşmesi süt miktarını doğrudan azaltır."
            )
        ]
    })

    # ADIM 93
    slides.append({
        "slideNumber": 93,
        "title": "Emzirme Döneminde Ek Enerji ve Ek Protein Gereksinimi",
        "subtitle": "Günlük +500 kalori ek enerji; ilk 6 ay +15 g, ikinci 6 ay +12 g protein",
        "badge": "Laktasyon Enerjisi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Günde 800 ml anne sütünün sentezlenebilmesi için maternal metabolizma günde yaklaşık 650-700 kalorilik bir iş gücü "
            "harcar. Bu enerjinin yaklaşık 150-200 kalorisi gebelikte kalçalarda depolanan yağlardan karşılanırken, geri kalan yaklaşık "
            "500 kalorilik açık annenin günlük diyetine eklenmelidir.\n\n"
            "> [SINAV SPOTU] Emziren kadının günlük ek enerji ihtiyacı ortalama +500 KALORİDİR. Ek protein ihtiyacı ise: İlk 6 ayda "
            "kendi gereksinimine EK 15 G/GÜN; ikinci 6 ayda ise EK 12 G/GÜN proteindir.\n\n"
            "Emziklilikte enerji ve vitamin gereksinimi gebelikten BİLE FAZLADIR! Bu ek protein anne sütünün kazein ve peynir altı "
            "suyu (whey) protein fraksiyonlarının kalitesini garanti eder."
        ),
        "medicalTerms": [
            {"term": "+500 Kalori Kuralı", "explanation": "Emziren kadının süt üretim maliyetini karşılamak için günlük diyetine eklenen net enerjidir."},
            {"term": "Kademeli Laktasyon Proteini", "explanation": "İlk 6 ayda günlük +15 g, 6-12. aylarda ise günlük +12 g ek protein standardıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Emziren kadında günlük ek enerji ihtiyacı: +500 kalori.",
            "📌 [SINAV SPOTU] Ek protein: İlk 6 ayda +15 g/gün; ikinci 6 ayda +12 g/gün.",
            "📌 [SINAV SPOTU] Emziklilikte enerji ihtiyacı gebelik döneminden daha yüksektir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "+500 kalori/gün", "desc": "Süt sentezinin günlük diyetten karşılanan metabolik payıdır.", "isKey": True},
                {"title": "İlk 6 Ay: +15 g", "desc": "Bebeğin tek besini anne sütü iken eklenen günlük protein miktarıdır.", "isKey": True},
                {"title": "İkinci 6 Ay: +12 g", "desc": "Tamamlayıcı beslenmeyle birlikte revize edilen protein ekidir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Emziren bir kadının günlük diyetine ilk 6 aylık dönemde kendi ihtiyacına ek olarak 15 g protein eklenmelidir.",
                "15 g",
                "İlk altı aydaki günlük ek protein gramajı"
            ),
            make_active_recall(
                "Emziren kadında günlük ek kalori ihtiyacı ve ilk 6 ay ile ikinci 6 aydaki ek protein ihtiyaçları ne kadardır?",
                "Ek enerji ihtiyacı günlük yaklaşık +500 kaloridir. Ek protein ihtiyacı ilk 6 ayda +15 g/gün, ikinci 6 ayda ise +12 g/gündür."
            )
        ]
    })

    # ADIM 94
    slides.append({
        "slideNumber": 94,
        "title": "Sıvı Dengesi ve Besin Grupları: Tahılın Emziklilikteki Rolü",
        "subtitle": "Günde 2-3 litre sıvı ve gebelikte gerekmeyen tahılın emziklilikte +1,5 porsiyon olması",
        "badge": "Sıvı ve Tahıl",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Anne sütünün yaklaşık %87-88'i saf sudan oluşur. Bu nedenle emziren kadının dehidratasyona girmemesi ve süt akımının "
            "kesintisiz sürmesi için günlük sıvı tüketimi hayati bir faktördür. Emzikli kadının günde 2-3 litre (ortalama 8-12 su bardağı) "
            "sıvı alması ve her emzirme seansında bir bardak su tüketmesi önerilir.\n\n"
            "> [SINAV SPOTU] Besin grupları karşılaştırması: Tahıllar gebelikte ek porsiyon GEREKTİRMEZKEN; emziklilik döneminde "
            "artan enerji ihtiyacını karşılamak için GÜNLÜK +1,5 PORSİYON TAHIL eklenir!\n\n"
            "Et grubu gebelikte +0,5-1 porsiyon iken emziklide +1 porsiyon; süt grubu her iki dönemde de ek 1 porsiyon (toplam 3-4 porsiyon); "
            "meyve-sebze ise 1-2 porsiyon artırılır."
        ),
        "medicalTerms": [
            {"term": "Laktasyonel Hidrasyon", "explanation": "Her emzirmede oksitosin uyarısıyla tetiklenen susama hissine paralel 2-3 litre sıvı tüketimidir."},
            {"term": "+1,5 Porsiyon Tahıl Kuralı", "explanation": "Gebelikte gerek duyulmayan ancak laktasyonda kalori açığını kapatmak için eklenen ekmektir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Emziren anne günde 2-3 litre (8-12 bardak) sıvı tüketmelidir.",
            "📌 [SINAV SPOTU] Tahıl grubu: Gebelikte ek gerekmez; emziklilikte +1,5 porsiyon eklenir.",
            "📌 [SINAV SPOTU] Her emzirme seansı öncesinde veya sonrasında bir bardak su içilmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "2 - 3 Litre Sıvı", "desc": "Günde 800 ml sütün hidrasyon tabanını güvenceye alır.", "isKey": True},
                {"title": "+1,5 Porsiyon Tahıl", "desc": "Laktasyonda gebelikten farklı olarak tahıl porsiyonu artırılır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Besin grupları dengesinde tahıllar gebelikte ek porsiyon gerektirmezken emziklilikte günlük 1,5 porsiyon eklenir.",
                "1,5 porsiyon",
                "Emziklilikte eklenen tahıl porsiyonu"
            ),
            make_active_recall(
                "Gebelikte ve emziklilikte tahıl grubu tüketim önerileri arasındaki fark nedir ve emziren anne ne kadar sıvı tüketmelidir?",
                "Tahıllar gebelikte ek porsiyon gerektirmezken, emziklilikte +1,5 porsiyon eklenir. Emziren annenin günlük sıvı tüketimi 2 - 3 litre (8-12 bardak) olmalıdır."
            )
        ]
    })

    # ADIM 95
    slides.append({
        "slideNumber": 95,
        "title": "Laktasyonda Kaçınılması Gerekenler: Alkol, Sigara ve Kafein",
        "subtitle": "Alkolün oksitosini baskılayıp süt inmesini felç etmesi ve neonatal letarji",
        "badge": "Laktasyon Toksikolojisi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Lohusalıkta tüketilen maddeler meme alveollerinden pasif difüzyonla doğrudan anne sütüne geçer ve bebeğin immatür karaciğerini "
            "zehirler. Halk arasındaki 'bira sütü artırır' inancı ölümcül bir yalandır; etanol arka hipofizden oksitosin salınımını "
            "baskılayarak süt inme refleksini felç eder ve bebeğin emdiği süt miktarını %20 azaltır.\n\n"
            "> [SINAV SPOTU] Emzirmede ALKOL: Oksitosini baskılayarak süt gelmesini engeller; bebekte uyuşukluk (letarji), derin uyku, "
            "doğrusal büyümede azalma ve anormal kilo alımına yol açar. SİGARA: Nikotin süte geçer ve bebeği pasif içici yapar. "
            "KAFEİN: Fazlası bebekte uykusuzluk ve huzursuzluk yapar.\n\n"
            "Emziren annenin tütün içmesi süt hacmini azaltır ve bebekte infantil kolik ile Ani Bebek Ölümü Sendromu (SIDS) riskini katlar."
        ),
        "medicalTerms": [
            {"term": "Oksitosin Blokajı", "explanation": "Alkolün hipotalamusu inhibe ederek miyoepitelyal kasılmayı ve süt ejeksiyonunu durdurmasıdır."},
            {"term": "Neonatal Letarji", "explanation": "Sütteki alkolün bebeğin santral sinir sistemini baskılayarak derin sersemlik ve beslenememe yapmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Alkol süt gelmesini (oksitosini) engeller; bebekte letarji ve büyüme geriliği yapar.",
            "📌 [SINAV SPOTU] Sigara süte geçerek süt miktarını düşürür ve SIDS riskini artırır.",
            "📌 [SINAV SPOTU] Fazla kafein bebekte taşikardi, huzursuzluk ve uykusuzluk yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Alkol Felci", "desc": "Oksitosini keserek sütün memeden akmasını bloke eder.", "isKey": True},
                {"title": "Bebekte Letarji", "desc": "Sütle geçen etanol bebekte derin uyku hali ve beslenme durması yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Emzirme döneminde tüketilen alkol arka hipofizden oksitosin salınımını baskılayarak süt inme refleksini engeller.",
                "oksitosin",
                "Süt fışkırtma refleksini sağlayan hipofiz hormonu"
            ),
            make_active_recall(
                "Emzirme döneminde alkol kullanımının anne sütü salgılanması ve bebek üzerindeki 3 majör etkisi nedir?",
                "1. Annede oksitosini baskılayarak süt inme refleksini bozar ve sütü azaltır, 2. Bebekte letarji (uyuşukluk ve derin uyku) yapar, 3. Doğrusal büyümede gerilemeye yol açar."
            )
        ]
    })

    # ADIM 96
    slides.append({
        "slideNumber": 96,
        "title": "Gebelikte Kesinlikle Yenmemesi Gereken Besinler: Listeria ve Toksoplazma",
        "subtitle": "Pastörize edilmemiş süt, küflü peynirler, çiğ şarküteri ve abortus tehdidi",
        "badge": "Gıda Güvenliği",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte bağışıklık sisteminin hücresel bacağında gelişen fizyolojik tolerans, anneyi gıda kaynaklı intrasellüler "
            "bakterilere karşı 20 kat daha duyarlı hale getirir. Bu enfeksiyonların en ölümcülü Listeria monocytogenes ve Toxoplasma gondii'dir. "
            "Listeria buzdolabı sıcaklığında (+4°C) dahi üreyebilen tek patojendir.\n\n"
            "> [SINAV SPOTU] Gebelikte kesinlikle yenmemesi gerekenler: PASTÖRİZE EDİLMEMİŞ süt ve süt ürünleri (çiğ sütten peynir, "
            "küflü/yumuşak peynirler: rokfor, brie, kamamber; bunlarla yapılan mayonez ve krema); İŞLENMİŞ VE ÇİĞ ETLER (salam, sosis, "
            "sucuk, pastırma, çiğ köfte, az pişmiş et); çiğ deniz ürünleri (sushi) ve iyi yıkanmamış çiğ sebzelerdir!\n\n"
            "Listeriyozis annede hafif gribal semptomlar yapsa da plasentadan fetüse geçerek koryoamniyonit, dissemine granülomatozis "
            "infantiseptika, spontan abortus ve ölü doğuma yol açar."
        ),
        "medicalTerms": [
            {"term": "Listeria monocytogenes", "explanation": "Pastörize edilmemiş süt ve soğuk şarküteriden bulaşan, fetüste sepsis ve ölü doğum yapan bakteridir."},
            {"term": "Toxoplasma gondii", "explanation": "İyi pişmemiş et ve kedi dışkısı bulaşmış sebzelerden geçen, koryoretinit ve hidrosefali yapan parazittir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Pastörize edilmemiş süt ve yumuşak peynirler (küflü peynir) kesinlikle yasaktır (Listeria riski).",
            "📌 [SINAV SPOTU] İşlenmiş etler (salam, sucuk, sosis) ve çiğ etler (çiğ köfte, sushi) yasaktır.",
            "📌 [SINAV SPOTU] Listeria enfeksiyonu spontan düşük ve intrauterin ölü doğumun önemli bir nedenidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Pastörizasyon Şart", "desc": "Çiğ sütten yapılan tüm taze peynirler listeriya kaynağıdır.", "isKey": True},
                {"title": "Şarküteri Yasağı", "desc": "Salam, sosis ve çiğ etler toksoplazma ve listeriya taşır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte pastörize edilmemiş sütten yapılan küflü peynirler fetüste ölü doğuma yol açan Listeria monocytogenes enfeksiyonu riski taşır.",
                "Listeria monocytogenes",
                "Çiğ süt ürünleriyle bulaşan ölü doğum etkeni bakteri"
            ),
            make_active_recall(
                "Gebelikte kesinlikle tüketilmemesi gereken süt ve et grubu ürünleri hangileridir ve hangi enfeksiyonlardan korkulur?",
                "Pastörize edilmemiş süt, taze/küflü peynirler (Listeria riski) ile çiğ/işlenmiş etler (salam, sosis, sucuk, çiğ köfte - Toksoplazma ve Listeria riski) tüketilmemelidir."
            )
        ]
    })

    # ADIM 97
    slides.append({
        "slideNumber": 97,
        "title": "Kabuklu Deniz Ürünleri, Ağır Metaller ve Katkı Maddeli Gıdalar",
        "subtitle": "Dip balıklarında metil cıva riski, midye/karides toksisitesi ve salamura tuz yükü",
        "badge": "Toksik Besinler",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte deniz ürünleri tüketimi DHA açısından teşvik edilmekle birlikte, balığın türü hayati bir ayrımdır. Besin zincirinin "
            "tepesinde yer alan uzun ömürlü ve yırtıcı dip balıkları (köpekbalığı, kılıçbalığı, kral uskumru, büyük ton balığı) "
            "yüksek oranda Metil Cıva (MeHg) biriktirir. Metil cıva plasentayı geçerek fetal beyin korteksinde kalıcı mikrosefali ve serebral palsi yapar.\n\n"
            "> [SINAV SPOTU] Gebelikte kaçınılması gereken diğer ürünler: Kabuklu deniz ürünleri (midye, istiridye, karides - ağır "
            "metal ve norovirüs/hepatit A riski), çiğ sushi; fazla tuz, turşu ve salamura zeytin (ödem/hipertansiyon riski); yağlı kızartmalar "
            "ve boya/katkı maddeli hazır gıdalar (hazır çorba, ketçap vb.).\n\n"
            "Buna karşılık hamsi, istavrit, palamut ve çiftlik somonu gibi yüzey balıkları cıva riski düşük ve güvenli kaynaklardır."
        ),
        "medicalTerms": [
            {"term": "Metil Cıva Toksisitesi", "explanation": "Yırtıcı dip balıklarından geçen ve fetal serebral korteksi tahrip eden nörotoksik ağır metaldir."},
            {"term": "Biyoakümülasyon", "explanation": "Ağır metallerin besin zincirinde yukarı çıkıldıkça büyük balıkların dokusunda katlanarak birikmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kabuklu deniz ürünleri (midye, istiridye) ve çiğ balık kesinlikle tüketilmemelidir.",
            "📌 [SINAV SPOTU] Büyük yırtıcı balıklardan metil cıva nedeniyle kaçınılmalıdır.",
            "📌 [SINAV SPOTU] Aşırı tuz, turşu, salamura ve hazır soslar ödem ve tansiyonu tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Cıva Nörotoksisitesi", "desc": "Dip balıklarındaki ağır metaller fetal beyin gelişimini durdurur.", "isKey": True},
                {"title": "Midye ve Kabuklular", "desc": "Filtre beslenen midyeler ağır metal ve hepatit virüsü deposudur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Besin zincirinde biriken ve fetal beyin hasarı yapan metil cıva nedeniyle gebelerin köpekbalığı ve kılıçbalığı gibi dip balıklarından kaçınması gerekir.",
                "metil cıva",
                "Yırtıcı deniz canlılarındaki nörotoksik ağır metal"
            ),
            make_active_recall(
                "Gebelikte kabuklu deniz ürünlerinin (midye, istiridye) ve büyük yırtıcı balıkların tüketilmesinin yarattığı iki temel toksikolojik tehlike nedir?",
                "1. Büyük yırtıcı balıklarda fetal beyin hasarı yapan metil cıva birikimi, 2. Filtreyle beslenen kabuklu deniz ürünlerinde ağır metal ve viral enfeksiyon (hepatit A/norovirüs) birikimidir."
            )
        ]
    })

    # ADIM 98
    slides.append({
        "slideNumber": 98,
        "title": "Bebek Beslenmesinde İlk 6 Ay Sadece Anne Sütü",
        "subtitle": "Su dahi vermeden ilk 6 ay eksklüzif emzirme ve 2 yaşına kadar sürdürme",
        "badge": "Eksklüzif Emzirme",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü, UNICEF ve T.C. Sağlık Bakanlığı'nın bebek beslenmesindeki değişmez ortak direktifi: Doğumdan sonraki "
            "ilk 6 ay boyunca bebeğe SU DAHİL hiçbir ek gıda veya içecek verilmeksizin 'Sadece Anne Sütü' (Eksklüzif Emzirme) sunulmasıdır. "
            "Anne sütünün %88'i su olduğundan, en sıcak çöl ikliminde dahi bebeğin tüm sıvı ihtiyacını eksiksiz karşılar.\n\n"
            "> [SINAV SPOTU] Bebek beslenmesinde ilk 6 ay YALNIZCA ANNE SÜTÜ verilmelidir; 6. aydan sonra uygun ve güvenli tamamlayıcı "
            "besinlere başlanmalı ve emzirme EN AZ 2 YAŞINA KADAR sürdürülmelidir.\n\n"
            "6 aydan önce başlanan erken ek gıdalar anne sütü alımını azaltır, bağırsak mikrobiyotasını bozar, enfeksiyon ve alerji "
            "riskini dramatik şekilde tırmandırır."
        ),
        "medicalTerms": [
            {"term": "Eksklüzif Emzirme", "explanation": "Bebeğe vitamin-mineral damlaları hariç su dahil hiçbir ek sıvının verilmediği ilk 6 aylık beslenmedir."},
            {"term": "Tamamlayıcı Beslenme", "explanation": "6. aydan itibaren anne sütüne ek olarak bebeğin çiğneme ve sindirimine uygun gıdalara başlanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İlk 6 ay sadece anne sütü verilir; su dahi verilmez.",
            "📌 [SINAV SPOTU] 6. aydan sonra ek gıdaya geçilir ve emzirme 2 yaşına kadar sürdürülür.",
            "📌 [SINAV SPOTU] Anne sütünün %88'i sudur; ek su ihtiyacı yoktur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İlk 6 Ay Tek Başına", "desc": "Bebeğin tüm kalori, sıvı ve immün ihtiyacını tek başına sağlar.", "isKey": True},
                {"title": "2 Yaşına Kadar Devam", "desc": "Tamamlayıcı gıdalarla birlikte emzirme sürdürülür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dünya Sağlık Örgütü bebeklerin ilk 6 ay boyunca su dahil hiçbir ek gıda almadan yalnızca anne sütü ile beslenmesini önerir.",
                "yalnızca anne sütü",
                "İlk 6 aydaki tek besin kaynağı"
            ),
            make_active_recall(
                "Dünya Sağlık Örgütü'nün (DSÖ) bebek beslenmesi konusundaki temel takvimi ve eksklüzif emzirme süresi nedir?",
                "Doğumdan sonraki ilk 6 ay su dahi verilmeksizin sadece anne sütü (eksklüzif emzirme) verilmeli; 6. aydan sonra tamamlayıcı besinlerle birlikte emzirme en az 2 yaşına kadar sürdürülmelidir."
            )
        ]
    })

    # ADIM 99 [CHECKPOINT 10]
    slides.append({
        "slideNumber": 99,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Emzirme Beslenmesi ve Sakınılacak Gıdalar İstasyonu",
        "subtitle": "800 ml üretim, +500 kal, ek protein, +1,5 tahıl ve Listeria yasaklarının konsolidasyonu",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 10,
        "synthesisNarrative": (
            "Bu istasyon; günde 800 ml anne sütü üretimini, 'fazla yiyenin sütü artmaz' kuralını, günlük 1800 kalori altının sütü kesmesini, "
            "emzirmede günlük +500 kalori ve ek protein ihtiyacını (ilk 6 ay +15 g, ikinci 6 ay +12 g), 2-3 litre sıvı alımını, emziklilikte "
            "+1,5 porsiyon tahıl ekini, alkolün oksitosini bloke etmesini, pastörize edilmemiş süt/peynir ve çiğ etlerdeki Listeria/Toksoplazma "
            "riskini ve ilk 6 ay sadece anne sütü ilkesini konsolide eder.\n\n"
            "> [YÜKSEK VERİM] Süt = 800 ml/gün; Ek kalori = +500 kal; Protein = İlk 6 ay +15 g, 2. altı ay +12 g; Tahıl = +1,5 porsiyon; "
            "Sıvı = 2-3 L; <1800 kal = süt düşer; Alkol = oksitosin durur; Çiğ süt/et = Listeria/Toksoplazma riski."
        ),
        "medicalTerms": [
            {"term": "Laktasyon Bütçesi", "explanation": "+500 kalori, +15 g protein, +1,5 porsiyon tahıl, 2-3 L sıvı."},
            {"term": "Gıda Toksisite Bariyeri", "explanation": "Listeria, metil cıva ve alkolden mutlak korunma kurallarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Günde ortalama 800 ml süt üretilir; ek enerji +500 kal, ek protein ilk 6 ay +15 g'dır.",
            "📌 [SINAV SPOTU] Gebelikte gerekmeyen tahıl emziklilikte +1,5 porsiyon artırılır; sıvı 2-3 litredir.",
            "📌 [SINAV SPOTU] 1800 kalori altı sütü azaltır; fazla beslenmek sütü artırmaz.",
            "📌 [SINAV SPOTU] Pastörize edilmemiş süt, küflü peynir, salam-sosis kesinlikle yasaktır (Listeria)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Laktasyon Formülü", "desc": "+500 kal, +15 g protein, +1,5 tahıl ve 2-3 L sıvı.", "isKey": True},
                {"title": "Yasaklılar", "desc": "Pastörize edilmemiş süt, çiğ et, kabuklu deniz ürünleri, alkol.", "isKey": True},
                {"title": "İlk 6 Ay Kuralı", "desc": "Su dahi verilmeden eksklüzif emzirme hayat kurtarır.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-28",
                "Emziren kadında günlük ek kalori ihtiyacı ne kadardır ve ilk 6 ay ile ikinci 6 ayda ne kadar ek protein önerilir?",
                "Günlük ek enerji ihtiyacı +500 kaloridir. Ek protein ihtiyacı ilk 6 ayda +15 g/gün, ikinci 6 ayda ise +12 g/gündür.",
                "Emziklilik kalori ve protein ihtiyacı"
            ),
            make_flashcard(
                "fc-k1-06-29",
                "Tahıl grubu porsiyon önerisi açısından gebelik ile emziklilik dönemi arasındaki fark nedir?",
                "Gebelikte ek tahıl porsiyonuna gerek yoktur; emziklilik döneminde ise artan enerjiyi karşılamak için günlük +1,5 porsiyon tahıl eklenmelidir.",
                "Tahıl porsiyonu farkı"
            ),
            make_flashcard(
                "fc-k1-06-30",
                "Gebelikte pastörize edilmemiş süt ve ürünlerinin tüketilmesinin yasak olmasının temel mikrobiyolojik nedeni nedir?",
                "Buzdolabında bile üreyebilen, plasentayı geçerek fetüste dissemine sepsis, spontan abortus ve ölü doğuma yol açan Listeria monocytogenes enfeksiyonu riskidir.",
                "Pastörize edilmemiş süt ve Listeria"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Dönem / Durum", "Günlük Ek Enerji İhtiyacı", "Temel Besin Grubu Özelliği"],
                [
                    [("Normal Gebelik Dönemi", False, ""), ("Günlük ortalama +340 kalori", False, ""), ("Tahıllarda ek porsiyona gerek yoktur", True, "Gebelikte tahıl artırılmama kuralı")],
                    [("Emziklilik Dönemi (İlk 6 Ay)", False, ""), ("Günlük ortalama +500 kalori", True, "Emziklilikteki ek kalori miktarı"), ("Ek 15 g protein ve +1,5 porsiyon tahıl", False, "")],
                    [("Yetersiz Beslenme (<1800 kal)", False, ""), ("Günlük 1800 kalorinin altı", False, ""), ("Anne sütü salgılanması belirgin düşer", True, "Aşırı kalori kısıtlamasının laktasyonel sonucu")]
                ]
            )
        ]
    })

    # ADIM 100
    slides.append({
        "slideNumber": 100,
        "title": "Büyük Sentez: Gebelik ve Emzirme Beslenmesinin Altın Kuralları",
        "subtitle": "100 adımlık maratonun klinik, halk sağlığı ve kurul sınavı özeti",
        "badge": "Büyük Sentez",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Tıp Fakültesi Kurul 1 Halk Sağlığı disiplini kapsamında ele alınan 'Gebelik ve Emzirme Döneminde Beslenme' mikro-dersi; "
            "yalnızca bir sınav konusu değil, bir toplumun geleceğini inşa eden en maliyet-etkili koruyucu hekimlik sanatıdır. "
            "Anne sağlığı, 2020'de kaybedilen 287.000 kadının ve her gün ölen 800 annenin trajedisini vasıflı doğum personeli ve "
            "kurumsal doğumla durdurma mücadelesidir.\n\n"
            "> [KLİNİK İPUCU] Hekimlik andı: Her gebe kadının tansiyonunu ölç, 24-28. haftada diyabetini tara, 16. haftada demirini, "
            "12. haftada D vitaminini başlat; gebe kalmadan 3 ay önce folatını ver; doğumda aktif üçüncü evreyi yönet ve ilk 6 ay "
            "bebeğe sadece anne sütü verilmesini sağla!\n\n"
            "Bu 100 atomik adımda öğrendiğimiz David Barker fetal programlamasından Sağlık Bakanlığı protokollerine uzanan ilkeler, "
            "mezuniyet sonrasında poliklinikte yazacağınız reçetelerin ve kurtaracağınız hayatların temel taşı olacaktır."
        ),
        "medicalTerms": [
            {"term": "Halk Sağlığı Koruyucu Hekimlik", "explanation": "Hastalıklar ortaya çıkmadan önce primer profilaksiyle toplum sağlığını güvenceye alma sanatıdır."},
            {"term": "Bütüncül Maternal Bakım", "explanation": "Prekonsepsiyondan başlayıp emzirmenin 2. yılına kadar süren kesintisiz izlem zinciridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne ölümlerinin %75'i 5 doğrudan nedene bağlıdır (kanama, sepsis, preeklampsi, tıkalı doğum, kürtaj).",
            "📌 [SINAV SPOTU] David Barker: Fetal beslenme erişkin kardiyovasküler kaderi çizer.",
            "📌 [SINAV SPOTU] Folat 3 ay önce (400 mcg / 4 mg), Demir 16. haftadan 9 ay (40-60 mg), D Vitamini 12. haftadan 6. aya (1200 IU).",
            "📌 [SINAV SPOTU] Emzirmede +500 kalori, ilk 6 ay +15 g protein, +1,5 porsiyon tahıl, 2-3 litre sıvı; ilk 6 ay sadece anne sütü!"
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mortaliteyi Sıfırla", "desc": "Vasıflı ebe, acil obstetrik bakım ve kurumsal doğum.", "isKey": True},
                {"title": "Profilaksi Üçlüsü", "desc": "Folik asit, elemental demir ve D vitamini takviyesi.", "isKey": True},
                {"title": "Laktasyon Zaferi", "desc": "İlk 6 ay sadece anne sütü, 2 yaşına kadar devam.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Gebelik ve emzirme döneminde koruyucu hekimlik açısından Sağlık Bakanlığı'nın yürüttüğü 3 temel profilaksi protokolü (ilaç, zamanlama, doz) nelerdir?",
                "1. Folik Asit: Gebe kalmadan 3 ay önce başlayıp 12. haftaya kadar, 400 mcg/gün (riskli gebede 4 mg/gün). 2. Demir: 16. haftadan doğum sonu 3. aya kadar (toplam 9 ay), 40-60 mg/gün elementer demir. 3. D Vitamini: 12. haftadan doğum sonu 6. aya kadar, 1200 IU/gün."
            ),
            make_cloze(
                "Gebelik ve emzirme sürecinde tüm koruyucu halk sağlığı müdahalelerinin nihai amacı anne ve bebek mortalitesini önlemektir.",
                "mortalitesini",
                "Ölüm oranını simgeleyen tıbbi terim"
            )
        ]
    })

    return slides
