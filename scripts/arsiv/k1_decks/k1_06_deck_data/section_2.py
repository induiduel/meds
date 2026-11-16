"""
Bölüm 2: Anne Ölümü Nedenleri, Komplikasyonlar ve Bakıma Erişimi Engelleyen Faktörler
Adımlar: 11 - 20
Checkpoint: Adım 19 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # ADIM 11
    slides.append({
        "slideNumber": 11,
        "title": "Anne Ölümlerinin %75'ini Oluşturan 5 Temel Komplikasyon",
        "subtitle": "Doğrudan obstetrik ölümlerin küresel dağılım mimarisi",
        "badge": "Mortalite Nedenleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü epidemiyolojik analizleri, dünya genelindeki tüm anne ölümlerinin yaklaşık %75'inin "
            "beş temel doğrudan obstetrik komplikasyondan kaynaklandığını ortaya koymaktadır. Bu komplikasyonlar; "
            "1) Şiddetli kanama (özellikle postpartum kanama), 2) Puerperal enfeksiyonlar (sepsis), 3) Gebelikte yüksek tansiyon "
            "(preeklampsi ve eklampsi), 4) Doğum komplikasyonları (tıkalı doğum ve yırtıklar) ve 5) Güvenli olmayan kürtajdır.\n\n"
            "> [SINAV SPOTU] Tüm anne ölümlerinin ~%75'ini oluşturan 5 ana doğrudan komplikasyon: şiddetli kanama, "
            "enfeksiyonlar, preeklampsi/eklampsi, doğum komplikasyonları ve güvenli olmayan kürtajdır.\n\n"
            "Bu patolojilerin tamamı modern tıp imkanlarıyla öngörülebilir, erken evrede tanınabilir ve tedavi edilebilir "
            "özelliktedir. Ölümlerin gerçekleşmesi tıp bilgisinin yetersizliğinden değil, hizmete zamanında erişilememesinden kaynaklanır."
        ),
        "medicalTerms": [
            {"term": "Doğrudan Obstetrik Ölüm", "explanation": "Gebelik, doğum ve lohusalık durumuna veya obstetrik girişimlere bağlı komplikasyonlardan kaynaklanan ölümdür."},
            {"term": "Dolaylı Obstetrik Ölüm", "explanation": "Gebelik öncesinde var olan veya gebelikte başlayıp gebeliğin fizyolojik etkisiyle kötüleşen hastalıklardan (kalp, anemi) kaynaklanan ölümdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne ölümlerinin ~%75'i beş temel doğrudan komplikasyona bağlıdır.",
            "📌 [SINAV SPOTU] Bu beş neden arasında ilk sırayı daima şiddetli postpartum kanama alır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "%75 Pay", "desc": "Doğrudan 5 obstetrik neden anne ölümlerinin dörtte üçünü oluşturur.", "isKey": True},
                {"title": "Önlenebilirlik", "desc": "Zamanında medikal ve cerrahi müdahale ile tamamen kontrol altına alınabilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dünyadaki toplam anne ölümlerinin yaklaşık yüzde 75 kadarı beş temel doğrudan obstetrik komplikasyona bağlıdır.",
                "yüzde 75",
                "Beş ana nedenin toplam ölümlerdeki yüzdesi"
            ),
            make_active_recall(
                "Anne ölümlerinin yaklaşık %75'ini oluşturan beş temel doğrudan obstetrik neden hangileridir?",
                "1. Şiddetli kanama, 2. Enfeksiyonlar, 3. Gebelikte yüksek tansiyon (preeklampsi/eklampsi), 4. Doğum komplikasyonları, 5. Güvenli olmayan kürtaj."
            )
        ]
    })

    # ADIM 12
    slides.append({
        "slideNumber": 12,
        "title": "Şiddetli Postpartum Kanama (PPH): Bir Numaralı Katil",
        "subtitle": "Uterin atoni, plasenta retansiyonu ve dakikalar içinde gelişen hipovolemik şok",
        "badge": "Postpartum Kanama",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Şiddetli kanama (postpartum hemoraji - PPH), dünya genelinde anne ölümlerinin en sık görülen tekil nedenidir "
            "ve tüm maternal kayıpların yaklaşık %27'sinden sorumludur. Bu kanamaların ezici çoğunluğu doğumun hemen ardından "
            "uterus düz kas liflerinin kasılamaması (uterin atoni) sonucu spiral arterlerin açık kalmasıyla gerçekleşir.\n\n"
            "> [SINAV SPOTU] Anne ölümlerinin en sık tekil nedeni doğum sonrası şiddetli kanamadır (postpartum hemoraji); "
            "en sık etiyolojik neden ise Uterin Atoni'dir.\n\n"
            "Diğer önemli PPH nedenleri; plasenta retansiyonu (parça kalması), doğum kanalı laserasyonları ve koagülopatilerdir "
            "(4T kuralı: Tone, Tissue, Trauma, Thrombin). Sağlıklı bir gebe dakikada 500-700 ml kan kaybedebileceğinden, "
            "dakikalar içinde hipovolemik şok ve kardiyak arrest gelişebilir."
        ),
        "medicalTerms": [
            {"term": "Postpartum Hemoraji (PPH)", "explanation": "Vajinal doğumda >500 ml, sezaryende >1000 ml veya hipovolemi bulgularına yol açan kan kaybıdır."},
            {"term": "Uterin Atoni", "explanation": "Plasenta ayrıldıktan sonra miyometriyumun kasılamaması ve damar ağızlarının açık kalarak aşırı kanamasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne ölümlerinin en sık nedeni şiddetli kanamadır (%27).",
            "📌 [SINAV SPOTU] Postpartum kanamanın en sık nedeni uterin atonidir; profilakside ilk tercih oksitosindir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "En Sık Neden", "desc": "Postpartum kanama anne ölümlerinde küresel olarak birinci sıradadır.", "isKey": True},
                {"title": "Uterin Atoni", "desc": "Miyometriyumun gevşek kalması masif kanamaya zemin hazırlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Postpartum kanamanın en sık karşılaşılan etiyolojik nedeni uterus kas liflerinin kasılamadığı uterin atoni tablosudur.",
                "uterin atoni",
                "Doğum sonu uterus gevşekliği"
            ),
            make_active_recall(
                "Dünya genelinde anne ölümlerinin bir numaralı tekil nedeni nedir ve patofizyolojik olarak en sık hangi mekanizmayla oluşur?",
                "Şiddetli kanamadır (postpartum hemoraji); en sık plasenta ayrıldıktan sonra miyometriyumun kasılamaması sonucu gelişen uterin atoni mekanizmasıyla oluşur."
            )
        ]
    })

    # ADIM 13
    slides.append({
        "slideNumber": 13,
        "title": "Puerperal Enfeksiyonlar ve Doğum Sonu Sepsis",
        "subtitle": "Sterilite ihlalleri, uzamış membran rüptürü ve septik şok tablosu",
        "badge": "Puerperal Sepsis",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Doğum eylemi ve lohusalık döneminde gelişen genital sistem enfeksiyonları (puerperal sepsis), özellikle hijyenik "
            "olmayan koşullarda evde yapılan doğumlarda anne mortalitesinin ikinci önemli sebebidir. Erken membran rüptürü (EMR), "
            "uzamış doğum eylemi, çok sayıda vajinal tuşe yapılması ve plasenta artıklarının kalması bakterilerin intrauterin alana "
            "kolonize olmasına zemin hazırlar.\n\n"
            "> [SINAV SPOTU] Puerperal sepsis çoğunlukla polimikrobiyal olup (Grup B Streptokok, E. coli, anaeroblar), hızla pelvik "
            "peritonit, septik tromboflebit ve septik şoka ilerleyebilir.\n\n"
            "Temiz doğum uygulamaları, el yıkama alışkanlığı ve şüpheli olgularda erken geniş spektrumlu intravenöz antibiyoterapiye "
            "başlanması, anne ölümlerini dramatik biçimde düşüren en kritik halk sağlığı müdahalelerindendir."
        ),
        "medicalTerms": [
            {"term": "Puerperal Sepsis", "explanation": "Doğum sonu 42 gün içinde genital kanaldan kaynaklanan ateş, kötü kokulu loşi ve sistemik enfeksiyon bulgularıdır."},
            {"term": "Endometrit", "explanation": "Doğum sonrası endometriyumun polimikrobiyal bakteriyel invazyonla enfekte olmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Doğum sonu puerperal sepsis, hijyenik olmayan doğumlarda anne ölümlerinin başlıca nedenlerindendir.",
            "📌 [SINAV SPOTU] Erken membran rüptürü ve tekrarlayan tuşeler koryoamniyonit ve puerperal sepsis riskini katlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hijyen Açığı", "desc": "Ev ortamında non-steril aletlerle yapılan doğumlarda risk maksimumdur.", "isKey": True},
                {"title": "Geniş Spektrum", "desc": "Hızlı IV antibiyotik ve kavitenin boşaltılması hayatidir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Doğum sonrası gelişen ve tedavi edilmediğinde septik şoka ilerleyen genital enfeksiyon tablosuna puerperal sepsis denir.",
                "puerperal sepsis",
                "Lohusalık kan zehirlenmesi"
            ),
            make_active_recall(
                "Puerperal sepsis gelişimini tetikleyen en önemli doğum eylemi risk faktörleri nelerdir?",
                "Uzamış membran rüptürü (>18 saat), uzamış travay, steril olmayan koşullarda sık vajinal muayene ve plasenta retansiyonudur."
            )
        ]
    })

    # ADIM 14
    slides.append({
        "slideNumber": 14,
        "title": "Gebelikte Hipertansif Bozukluklar: Preeklampsi ve Eklampsi",
        "subtitle": "Yaygın endotel hasarı, serebral vazospazm ve konvülsiyon krizleri",
        "badge": "Preeklampsi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte hipertansiyon, maternal ölümlerin yaklaşık %14'ünden sorumlu olan ve anne-bebek ikilisini eşzamanlı "
            "tehdit eden multisistemik bir patolojidir. Tablo 20. gebelik haftasından sonra ortaya çıkan kan basıncı yüksekliği "
            "(≥140/90 mmHg) ve proteinüri (veya hedef organ hasarı) ile seyreden preeklampsi şeklinde başlar.\n\n"
            "> [SINAV SPOTU] Preeklampsi tablosuna jeneralize tonik-klonik konvülsiyonların (nöbet) eklenmesi EKLAMPSİ olarak "
            "tanımlanır; profilakside ve nöbet tedavisinde ilk tercih MAGNEZYUM SÜLFAT'tır.\n\n"
            "Patofizyolojide plasental trofoblast invazyon kusuru, spiral arterlerin yetersiz yeniden biçimlenmesi ve salınan "
            "anti-anjiyojenik faktörlerin (sFlt-1) maternal endotel hücrelerini tahrip etmesi yatar. Serebral ödem, intrauterin "
            "gelişme geriliği, HELLP sendromu ve intraserebral kanama en ölümcül tablolardır."
        ),
        "medicalTerms": [
            {"term": "Preeklampsi", "explanation": "20. haftadan sonra gelişen yeni başlangıçlı HT ve proteinüri veya trombositopeni/karaciğer hasarıdır."},
            {"term": "Eklampsi", "explanation": "Preeklamptik gebede başka nörolojik sebep olmaksızın jeneralize grand mal nöbetlerin gelişmesidir."},
            {"term": "Magnezyum Sülfat (MgSO4)", "explanation": "Eklamptik konvülsiyonların önlenmesi ve tedavisinde ilk seçenek membran stabilize edici ajandır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Preeklampsiye konvülsiyon eklenmesi eklampsidir; nöbet profilaksisinde altın standart Magnezyum Sülfattır.",
            "📌 [SINAV SPOTU] Hipertansif bozukluklar maternal ölümlerin yaklaşık %14'ünü oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Endotel Disfonksiyonu", "desc": "Plasental iskemi maternal tüm damar endotelini bozar.", "isKey": True},
                {"title": "MgSO4 Koruması", "desc": "Serebral vazodilatasyon sağlayarak eklamptik nöbetleri keser.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Preeklampsi tablosunda eklamptik nöbetlerin önlenmesi ve tedavisinde altın standart ilaç magnezyum sülfat infüzyonudur.",
                "magnezyum sülfat",
                "Eklampsi profilaksisinde kullanılan iyon tuzu"
            ),
            make_active_recall(
                "Preeklampsi ile eklampsi arasındaki tanısal fark nedir ve eklampsi nöbetinde ilk tercih edilen medikal tedavi nedir?",
                "Preeklampsiye grand mal konvülsiyonların (nöbet) eklenmesi eklampsidir; nöbet kontrolü ve profilaksisinde ilk tercih Magnezyum Sülfattır (MgSO4)."
            )
        ]
    })

    # ADIM 15
    slides.append({
        "slideNumber": 15,
        "title": "Tıkalı Doğum Eylemi (Obstrüktif Travay) ve Komplikasyonları",
        "subtitle": "Uterin rüptür, kemik çatısı darlığı ve doku nekrozu zinciri",
        "badge": "Obstrüktif Travay",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Tıkalı doğum eylemi (obstrüktif travay), güçlü ve düzenli uterin kontraksiyonlara rağmen bebeğin doğum kanalından "
            "mekanik olarak ilerleyememesi durumudur. En sık nedeni sefalopelvik disproporsiyon (çatı darlığı) veya bebeğin transvers "
            "duruş gibi patolojik prezentasyonlarıdır.\n\n"
            "> [SINAV SPOTU] Tedavi edilmeyen obstrüktif travay; Bandl patolojik retraksiyon halkasına, UTERUS RÜPTÜRÜNE, "
            "masif kanamaya ve maternal-fetal ölüme yol açar.\n\n"
            "Travayın uzaması durumunda bebeğin başı maternal simfizis pubis veya sakrum arasında sıkışarak yumuşak doku iskemisine "
            "ve nekrozuna neden olur. Günler süren tıkalı eylem sonucunda mesane ve rektum dokuları delinerek hayat boyu süren "
            "sosyal izolasyon kaynağı olan obstetrik fistüller meydana gelir."
        ),
        "medicalTerms": [
            {"term": "Obstrüktif Travay", "explanation": "İlerleyici mekanik engel nedeniyle doğum eyleminin durması ve cerrahi olmaksızın tamamlanamamasıdır."},
            {"term": "Bandl Halkası", "explanation": "Obstrüktif travayda uterusun alt ve üst segmenti arasında oluşan ve rüptür habercisi olan patolojik çekinti çizgisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tıkalı travayın en korkulan akut sonucu uterus rüptürü ve hemorajik şoktur.",
            "📌 [SINAV SPOTU] Tıkalı travayın en yıkıcı kronik sekeli obstetrik vezikovajinal/rektovajinal fistüldür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mekanik Engel", "desc": "Pelvis darlığı veya anormal fetus duruşu eylemi kilitler.", "isKey": True},
                {"title": "Uterin Rüptür", "desc": "Aşırı gerilen alt segment yırtılarak anneyi dakikalar içinde öldürebilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Tıkalı doğum eyleminde uterus alt segmentinin aşırı incelmesi ve yırtılması tablosuna uterus rüptürü adı verilir.",
                "uterus rüptürü",
                "Rahmin yırtılması komplikasyonu"
            ),
            make_active_recall(
                "Tıkalı doğum eyleminin (obstrüktif travay) zamanında sezaryenle çözülememesi durumunda gelişen akut ve kronik iki majör komplikasyon nedir?",
                "Akut komplikasyon uterus rüptürü ve masif kanamadır; kronik komplikasyon ise iskemiye bağlı pelvik doku nekrozu ve obstetrik fistüldür."
            )
        ]
    })

    # ADIM 16
    slides.append({
        "slideNumber": 16,
        "title": "Güvenli Olmayan Kürtaj: Gizli ve Önlenebilir Yara",
        "subtitle": "Elverişsiz koşullar, ehil olmayan eller ve ölümcül perforasyonlar",
        "badge": "Güvenli Olmayan Kürtaj",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü, güvenli olmayan kürtajı 'istenmeyen bir gebeliğin gerekli becerilere sahip olmayan kişilerce "
            "veya asgari tıbbi standartlara uymayan bir ortamda sonlandırılması' olarak tanımlar. Küresel ölçekte maternal "
            "ölümlerin yaklaşık %8 ila %13'ü doğrudan güvenli olmayan düşük girişimlerinden kaynaklanmaktadır.\n\n"
            "> [SINAV SPOTU] Güvenli olmayan kürtaj; uterin perforasyon, bağırsak yaralanması, şiddetli kanama ve fulminan "
            "Clostridium/sepsis tablosuyla hızla ölüme yol açan, tamamen önlenebilir bir nedendir.\n\n"
            "Yasal engeller, damgalanma ve aile planlaması hizmetlerine erişim yetersizliği, kadınları kimyasal madde içme, "
            "rahme yabancı cisim sokma gibi tehlikeli yollara itmektedir. Etkin doğum kontrol danışmanlığı bu ölümleri sıfırlar."
        ),
        "medicalTerms": [
            {"term": "Güvenli Olmayan Kürtaj (Unsafe Abortion)", "explanation": "Eğitimsiz kişilerce veya tıbbi hijyenden yoksun mekanlarda yapılan yasa dışı gebelik tahliyeleridir."},
            {"term": "Uterin Perforasyon", "explanation": "Kürtaj sırasında aletlerin uterus duvarını delerek batın boşluğuna ve komşu organlara geçmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Güvenli olmayan kürtaj tüm maternal ölümlerin ~%8-13'ünü oluşturur ve %100 önlenebilir.",
            "📌 [SINAV SPOTU] Temel komplikasyonlar uterin delinme, yaygın peritonit, septik şok ve masif kanamadır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Önlenebilir Kayıp", "desc": "Modern kontrasepsiyon hizmetleriyle bu ölümler tamamen engellenebilir.", "isKey": True},
                {"title": "Şiddetli Sepsis", "desc": "Toksik maddeler ve steril olmayan aletler fulminan nekrotizan enfeksiyon yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Güvenli olmayan kürtaj girişimlerinde mekanik aletlerin rahim duvarını delmesi tablosuna uterin perforasyon denir.",
                "uterin perforasyon",
                "Kürtaj sırasında rahmin delinmesi"
            ),
            make_active_recall(
                "Güvenli olmayan kürtaj girişimlerinin yol açtığı en ölümcül cerrahi ve enfeksiyöz komplikasyonlar nelerdir?",
                "Uterin perforasyon, bağırsak yaralanması, masif intraabdominal kanama ve fulminan septik şoktur."
            )
        ]
    })

    # ADIM 17
    slides.append({
        "slideNumber": 17,
        "title": "Dolaylı Maternal Ölüm Nedenleri: Anemi, Kalp ve Sıtma",
        "subtitle": "Gebelikte dekompanse olan önceden var olan sistemik patolojiler",
        "badge": "Dolaylı Nedenler",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Anne ölümlerinin yaklaşık %25'i doğrudan obstetrik cerrahi/mekanik olaylardan değil, gebeliğin getirdiği fizyolojik "
            "yükün tetiklediği dolaylı (indirekt) sistemik hastalıklardan kaynaklanır. Bu nedenlerin başında ağır kronik demir "
            "eksikliği anemisi, maternal kardiyovasküler hastalıklar (özellikle romatizmal kapak hastalıkları ve peripartum kardiyomiyopati), "
            "endemik bölgelerde Plasmodium falciparum sıtması ve HIV/AIDS gelmektedir.\n\n"
            "> [SINAV SPOTU] Gebelikte plazma hacmi %40-50 artarak fizyolojik hemodilüsyon yapar; önceden anemisi olan veya kalp rezervi "
            "kısıtlı kadınlarda bu hipervolemik yük hızla kalp yetmezliğine ve ölüme yol açar.\n\n"
            "Ağır anemi (Hb < 7 g/dl), doğum sırasında normal kabul edilen 300 ml'lik fizyolojik kanamanın bile doku oksijenlenmesini "
            "çökertmesine ve hipovolemik şok tablosunun çok erken gelişmesine neden olur."
        ),
        "medicalTerms": [
            {"term": "Dolaylı Nedenler (Indirect Causes)", "explanation": "Gebelikten önce var olan ve gebeliğin hemodinamik yüküyle agreve olan maternal hastalıklardır."},
            {"term": "Peripartum Kardiyomiyopati", "explanation": "Gebeliğin son ayında veya doğum sonrası ilk 5 ayda sol ventrikül sistolik fonksiyonunun bozulmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dolaylı nedenler içinde anemi, kalp yetmezliği ve enfeksiyonlar (sıtma, HIV) başı çeker.",
            "📌 [SINAV SPOTU] Ağır anemik gebeler minimal postpartum kanamaları dahi tolere edemeyerek arrest olabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemodinamik Yük", "desc": "Gebelikte kalp debisinin ve kan hacminin artışı zayıf kalbi dekompanse eder.", "isKey": True},
                {"title": "Ağır Anemi", "desc": "Oksijen taşıma kapasitesinin çöküşü anne mortalitesini katlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte artan plazma hacmi ve kardiyak debi önceden var olan kardiyovasküler hastalıklar tablosunu kötüleştirerek dolaylı ölümlere yol açar.",
                "kardiyovasküler hastalıklar",
                "Kalp ve dolaşım sistemi patolojileri"
            ),
            make_active_recall(
                "Gebelikte ağır anemi tablosunun doğrudan doğum sırasındaki kan kaybıyla birleştiğinde yarattığı ölümcül risk nedir?",
                "Hb < 7 g/dl olan gebelerde fizyolojik miktardaki kanama dahi miyokardiyal hipoksiye, kompanse edilemeyen akut hipovolemik şoka ve ölüme yol açar."
            )
        ]
    })

    # ADIM 18
    slides.append({
        "slideNumber": 18,
        "title": "Bakıma Erişimi Engelleyen 5 Faktör (DSÖ Kriterleri)",
        "subtitle": "Yoksulluk, mesafe, bilgi eksikliği, kalitesiz hizmet ve kültürel inançlar",
        "badge": "DSÖ Engelleri",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü, kadınların gebelik, doğum ve lohusalık süreçlerinde hayat kurtarıcı obstetrik bakım almasını veya "
            "bakım aramasını engelleyen faktörleri beş temel başlık altında tanımlamıştır: 1) Yoksulluk (ekonomik yetersizlik), "
            "2) Sağlık tesislerine uzaklık ve ulaşım güçlüğü, 3) Bilgi eksikliği (tehlike işaretlerini tanımama), 4) Yetersiz ve "
            "kalitesiz sağlık hizmeti (personel, ilaç ve donanım yokluğu) ve 5) Kültürel inançlar ve geleneksel zararlı uygulamalar.\n\n"
            "> [SINAV SPOTU] DSÖ'ye göre bakım almayı engelleyen faktörler: yoksulluk, tesislere uzaklık, bilgi eksikliği, "
            "yetersiz/kalitesiz hizmet ve kültürel inançlardır. 'Sağlık eğitimi' bir engel DEĞİL, bakıma erişimi artıran çözümdür!\n\n"
            "Bu engeller, kadının evdeki karar verme mekanizmasından başlayarak hastaneye varışına ve tedavi almasına kadar uzanan "
            "zincirin her halkasında ölümcül gecikmelere zemin hazırlamaktadır."
        ),
        "medicalTerms": [
            {"term": "Bakıma Erişim Engeli", "explanation": "Bireyin ihtiyaç duyduğu koruyucu veya tedavi edici sağlık hizmetine ulaşmasını engelleyen yapısal bariyerlerdir."},
            {"term": "Kültürel Bariyer", "explanation": "Kadının erkek izni olmadan evden çıkamaması veya evde yaşlı kadınların doğumu yönetmesi gibi geleneksel engellerdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Bakımı engelleyen DSÖ faktörleri: Yoksulluk, Uzaklık, Bilgi eksikliği, Kalitesiz hizmet, Kültürel inançlar.",
            "📌 [SINAV SPOTU] Sınav sorusu: 'Sağlık eğitimi' bakım engeli DEĞİL, hizmete erişimi güçlendiren unsurdur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "5 Temel Engel", "desc": "DSÖ kılavuzunda net tanımlanmış yapısal ve sosyal bariyerler bütünüdür.", "isKey": True},
                {"title": "Eğitim Çözümdür", "desc": "Sağlık okuryazarlığı ve eğitimi engelleri yıkan en temel araçtır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "DSÖ raporlarına göre kadınların doğum bakımı almasını engelleyen faktörler arasında yoksulluk ve tesislere uzaklık ilk sıralarda yer alır.",
                "yoksulluk",
                "Maddi yetersizlik bariyeri"
            ),
            make_active_recall(
                "DSÖ'ye göre kadınların gebelik ve doğumda bakım almasını engelleyen 5 temel faktör nedir ve sağlık eğitimi bu sınıflamada nerede durur?",
                "5 faktör: 1. Yoksulluk, 2. Tesislere uzaklık, 3. Bilgi eksikliği, 4. Kalitesiz/yetersiz hizmet, 5. Kültürel inançlar. Sağlık eğitimi engel değil, tam tersine bu engelleri aşmayı sağlayan temel çözümdür."
            )
        ]
    })

    # ADIM 19 [CHECKPOINT 2]
    slides.append({
        "slideNumber": 19,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Anne Ölüm Nedenleri ve Bakım Engelleri İstasyonu",
        "subtitle": "Postpartum kanama, preeklampsi, sepsis ve DSÖ engellerinin analitik özeti",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 2,
        "synthesisNarrative": (
            "Bu istasyon, anne ölümlerinin %75'ini oluşturan 5 majör doğrudan obstetrik nedeni (şiddetli kanama, enfeksiyon, "
            "preeklampsi/eklampsi, tıkalı doğum ve güvenli olmayan kürtaj), kanamanın bir numaralı ölüm sebebi olmasını, uterin atoninin "
            "en sık mekanizma olduğunu, eklampside ilk tercihin magnezyum sülfat olduğunu, tıkalı travayın rüptür ve fistül riskini ve "
            "DSÖ'nün 5 bakım engelini (yoksulluk, mesafe, bilgisizlik, kalitesiz hizmet, kültürel inançlar) sentezlemektedir.\n\n"
            "> [YÜKSEK VERİM] Postpartum kanama = 1 numara katil (atoni); Eklampsi = MgSO4 tedavisi; Bakım engelleri = Yoksulluk, "
            "uzaklık, bilgi eksikliği, kalitesiz hizmet, inançlar (Sağlık eğitimi asla engel değildir)."
        ),
        "medicalTerms": [
            {"term": "Maternal Katil Beşli", "explanation": "Kanama, sepsis, preeklampsi, tıkalı doğum, güvensiz kürtaj."},
            {"term": "Üç Gecikme Modeli", "explanation": "Bakım arama, tesise ulaşma ve nitelikli hizmet alma gecikmeleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne ölümlerinde 1 numara: Şiddetli postpartum kanama (en sık etiyoloji: Uterin atoni).",
            "📌 [SINAV SPOTU] Eklampsi konvülsiyon tedavisinde altın standart: Magnezyum Sülfat (MgSO4).",
            "📌 [SINAV SPOTU] DSÖ bakım engelleri: Yoksulluk, mesafe, bilgi eksikliği, kalitesiz hizmet, kültürel inançlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mortalite Beşlisi", "desc": "Kanama, sepsis, eklampsi, tıkalı travay ve güvensiz kürtaj.", "isKey": True},
                {"title": "Eklampsi Protokolü", "desc": "Magnezyum sülfat nöbeti çözer ve tekrarını engeller.", "isKey": True},
                {"title": "Bariyerler Analizi", "desc": "DSÖ 5 engelini aşmak mortaliteyi %75 oranında düşürür.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-04",
                "Anne ölümlerinin en sık görülen tekil nedeni ve bunun en yaygın etiyolojik sebebi nedir?",
                "En sık neden şiddetli doğum sonu kanamadır (postpartum hemoraji); en yaygın etiyolojik mekanizma ise Uterin Atonidir.",
                "PPH ve uterin atoni"
            ),
            make_flashcard(
                "fc-k1-06-05",
                "Preeklampsi tablosunda eklamptik nöbet geliştiğinde ilk tercih edilecek hayat kurtarıcı ilaç nedir?",
                "Magnezyum Sülfattır (MgSO4); serebral vazospazmı çözer ve nöbet profilaksisini sağlar.",
                "Eklampsi ve MgSO4"
            ),
            make_flashcard(
                "fc-k1-06-06",
                "DSÖ'ye göre kadınların obstetrik bakım almasını engelleyen 5 faktör nedir?",
                "1. Yoksulluk, 2. Tesislere uzaklık, 3. Bilgi eksikliği, 4. Yetersiz/kalitesiz hizmet, 5. Kültürel inançlar (Sağlık eğitimi engel değildir).",
                "DSÖ 5 bakım engeli"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Obstetrik Komplikasyon", "Temel Patofizyoloji", "Altın Standart Tedavi / Yaklaşım"],
                [
                    [("Postpartum Kanama", False, ""), ("Uterin atoni ve açık kalan spiral damarlar", False, ""), ("Profilaktik oksitosin ve bimanüel masaj", True, "Uterotonik hormon ve mekanik yaklaşım")],
                    [("Preeklampsi / Eklampsi", False, ""), ("Yaygın endotel hasarı ve serebral vazospazm", False, ""), ("Magnezyum sülfat infüzyonu ve doğum", True, "Nöbet önleyici iyon infüzyonu")],
                    [("Tıkalı Doğum Eylemi", False, ""), ("Sefalopelvik uyumsuzluk ve mekanik ilerlememe", False, ""), ("Acil sezaryen doğum eylemi", True, "Cerrahi doğum müdahalesi")]
                ]
            )
        ]
    })

    # ADIM 20
    slides.append({
        "slideNumber": 20,
        "title": "Üç Gecikme Modeli (Three Delays Model) ve Hayatta Kalma",
        "subtitle": "Karar verme, ulaşım ve sağlık tesisindeki ölümcül zaman kayıpları",
        "badge": "Gecikme Modeli",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Halk sağlığı literatüründe anne ölümlerinin nedenlerini sistemik olarak analiz etmek amacıyla Thaddeus ve Maine "
            "tarafından geliştirilen 'Üç Gecikme Modeli' (Three Delays Model), obstetrik bir komplikasyon ortaya çıktığında yaşanan "
            "ölümcül zaman kayıplarını üç kritik evreye ayırır: 1. Gecikme: Bakım aramaya karar vermede gecikme, 2. Gecikme: "
            "Sağlık tesisine ulaşmada gecikme, 3. Gecikme: Sağlık tesisinde yeterli ve nitelikli bakım almada gecikme.\n\n"
            "> [SINAV SPOTU] Üç Gecikme Modeli: 1. Gecikme kadının/ailenin karar vermesi; 2. Gecikme yollar ve ambulans ulaşımı; "
            "3. Gecikme ise hastanedeki personel, kan ve ilaç eksikliğidir.\n\n"
            "Özellikle üçüncü gecikme (hastanede kan bulunamaması, cerrahın olmaması), hastaneye zamanında yetişen kadınların dahi "
            "önlenebilir nedenlerle kaybedilmesine yol açan en trajik sistemik zaafiyettir."
        ),
        "medicalTerms": [
            {"term": "Üç Gecikme Modeli (Three Delays)", "explanation": "Maternal ölüme giden süreçte karar, ulaşım ve tedavi basamaklarındaki zaman kayıplarını açıklayan modeldir."},
            {"term": "Üçüncü Gecikme (Hizmet Gecikmesi)", "explanation": "Hastanın sağlık kuruluşuna varmasına rağmen personel, ameliyathane veya kan yetersizliği nedeniyle müdahale alamamasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 1. Gecikme: Bakım aramaya karar verme; 2. Gecikme: Tesise ulaşma; 3. Gecikme: Nitelikli bakım alma.",
            "📌 [SINAV SPOTU] Kan bankası ve acil sezaryen ekibinin yokluğu 3. gecikmenin en tipik örnekleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. Gecikme", "desc": "Hastalık işaretlerini tanımama ve evde izin alamama.", "isKey": True},
                {"title": "2. Gecikme", "desc": "Kötü yollar, araç yokluğu ve coğrafi engeller.", "isKey": True},
                {"title": "3. Gecikme", "desc": "Hastanede kan, ilaç veya hekim eksikliği.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Anne sağlığında hastaneye varılmasına rağmen kan ve ilaç bulunamaması sonucu yaşanan zaman kaybına üçüncü gecikme denir.",
                "üçüncü gecikme",
                "Hastanede nitelikli bakım alma safhasındaki gecikme"
            ),
            make_active_recall(
                "Üç Gecikme Modeli'nin (Three Delays) üç basamağı sırasıyla nelerdir ve hastanede kan eksikliği hangi basamağa girer?",
                "1. Bakım aramaya karar vermede gecikme, 2. Sağlık tesisine ulaşmada gecikme, 3. Sağlık tesisinde yeterli ve nitelikli bakım almada gecikme. Hastanede kan veya cerrah bulunamaması 3. Gecikmeye girer."
            )
        ]
    })

    return slides
