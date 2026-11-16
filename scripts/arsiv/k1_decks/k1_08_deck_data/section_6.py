"""
Section 6: Replikatif Yaşlanma, Telomerler ve Hayflick Limiti (Slayt 51 - 60)
"""
from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-08-s51",
        "title": "Replikatif Senesens ve Hayflick Limiti",
        "subtitle": "Normal insan somatik hücrelerinin kültür ortamındaki sınırlı bölünme kapasitesi",
        "badge": "Replikatif Yaşlanma",
        "badgeColor": "blue",
        "coreContent": {
            "text": (
                "1961 yılında Leonard Hayflick, insan embriyonik fibroblastlarının in vitro kültürde sınırsız çoğalamadığını keşfetti.\n\n"
                "Embriyonik fibroblastlar yaklaşık **50-60 bölünme** yaptıktan sonra mitozu kalıcı olarak durdurur ve senesense girer (**Hayflick Limiti**).\n\n"
                "Yaşlı bireylerden alınan fibroblastlar ise sadece 20-30 kez bölünebilir.\n\n"
                "> Bu deney, normal somatik hücrelerin içinde yerleşik bir ==replikatif sayacın (hücresel saat)== bulunduğunu ilk kez kanıtlamıştır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Normal insan somatik hücrelerinin bölünme sınırını tanımlayan kavrama Hayflick Limiti adı verilir.",
                "Hayflick Limiti",
                "Leonard Hayflick tarafından keşfedilen hücresel mitoz tavanı"
            ),
            make_active_recall(
                "Yenidoğan bir bebekten alınan fibroblast ile 80 yaşındaki bir bireyden alınan fibroblastın kültürdeki bölünme farkı nedir?",
                "Yenidoğan hücresi yaklaşık 50-60 kez bölünebilirken; 80 yaşındaki bireyin hücresi telomerleri önceden aşındığı için sadece 20-30 kez bölünüp erkenden senesense girer."
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-08-s52",
        "title": "Telomerlerin Moleküler Yapısı: TTAGGG Tekrarları",
        "subtitle": "Kromozom uçlarında yer alan kodlamayan nükleoprotein kütükleri",
        "badge": "Kromozom Biyolojisi",
        "badgeColor": "indigo",
        "coreContent": {
            "text": (
                "**Telomerler**, ökaryotik lineer kromozomların her iki ucunda yer alan, herhangi bir proteini kodlamayan "
                "özel nükleotid dizileridir.\n\n"
                "Tüm omurgalılarda değişmeyen evrensel dizi: ==5'-TTAGGG-3'== hekzanükleotid tekrarlarıdır.\n\n"
                "İnsanda doğumda telomer boyu yaklaşık 10-15 kilobaz (kb) uzunluğundadır.\n\n"
                "> En uçta tek iplikli 3' çıkıntısı (3' G-overhang) bulunur ve kendi üzerine kıvrılarak **t-loop** halkasını oluşturur."
            )
        },
        "interactiveElements": [
            make_cloze(
                "İnsan kromozom uçlarındaki telomerleri oluşturan evrensel hekzanükleotid tekrar dizisi TTAGGG dizisidir.",
                "TTAGGG",
                "Timin-Timin-Adenin-Guanin-Guanin-Guanin dizilimi"
            ),
            make_active_recall(
                "Telomerlerin kromozom stabilitesi açısından en temel görevi nedir?",
                "Kromozom uçlarını nükleaz enzimlerinden korumak ve kromozom uçlarının hücresel DNA tamir sistemlerince çift zincir kırığı sanılıp birbirine yapışmasını (uç uca füzyon) engellemektir."
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-08-s53",
        "title": "Shelterin Kompleksi: Kromozom Uçlarını Koruyan Kalkan",
        "subtitle": "Altı alt birimli koruyucu nükleoprotein zırh ve t-loop stabilizasyonu",
        "badge": "Nükleer Kompleks",
        "badgeColor": "purple",
        "coreContent": {
            "text": (
                "Telomer DNA'sı çıplak değildir; **Shelterin** adı verilen 6 üyeli özel bir protein kompleksi tarafından sarılmıştır.\n\n"
                "Shelterin alt birimleri: **TRF1, TRF2, RAP1, TIN2, TPP1 ve POT1**.\n\n"
                "Bu kompleks tek iplikli 3' ucunu çift iplikli bölgenin içine sokarak **t-loop** (telomeric loop) düğümünü bağlar.\n\n"
                "> Eğer Shelterin kompleksi (özellikle **TRF2**) hasarlanırsa, hücre kromozom ucunu kırık DNA zanneder ve ATM kinaz derhal DDR alarmı çalar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomer uçlarını sararak kırık DNA alarmını engelleyen altı proteinli koruyucu komplekse Shelterin kompleksi denir.",
                "Shelterin",
                "TRF1 ve TRF2'yi içeren koruyucu protein zırhı"
            ),
            make_before_after(
                "Korumalı Shelterin t-loop Yapısı ile Açığa Çıkmış Telomer Ucu",
                "Korumalı Telomer (t-loop)",
                "3' uç içeri sokulmuştur; DNA tamir sensörleri (ATM/ATR) uca bağlanamaz, hücre güvenle bölünür.",
                "Açığa Çıkmış Kısa Telomer",
                "Shelterin bağı çöker, açık serbest DNA ucu kalır; ATM/ATR uca bağlanıp kalıcı çift zincir kırık alarmı verir."
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-08-s54",
        "title": "Son Replikasyon Problemi (End-Replication Problem)",
        "subtitle": "DNA polimerazın doğasından kaynaklanan kaçınılmaz telomer kaybı",
        "badge": "Biyokimyasal Engel",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "DNA polimeraz enzimleri sentezi ancak 5' -> 3' yönünde yapabilir ve başlamak için bir **RNA primere** muhtaçtır.\n\n"
                "Kesintili zincirde (lagging strand) en uçtaki RNA primeri çıkarıldığında, polimeraz geriye dönüp bu boşluğu dolduramaz.\n\n"
                "Bu biyolojik zorunluluğa ==son replikasyon problemi== adı verilir.\n\n"
                "> Sonuç olarak, insan somatik hücreleri her hücre bölünmesinde uçtan **50 ila 100 baz çifti** telomer DNA'sını geri dönüşsüz olarak kaybeder."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Kesintili zincirin en ucundaki RNA primerinin kaldırılamaması sonucu her bölünmede telomer kısalmasına son replikasyon problemi denir.",
                "son replikasyon problemi",
                "Lineer DNA kopyalamasında uçların tam sentezlenememesi çıkmazı"
            ),
            make_causal_chain(
                "Son Replikasyon Problemi ve Telomer Kaybı Zinciri",
                [
                    "1. Replikasyon Başlangıcı: Primaz enzimi kesintili zincirin en ucuna RNA primeri koyar.",
                    "2. Sentez: DNA polimeraz Okazaki parçasını sentezler.",
                    "3. Primer Çıkarılması: RNA primeri nükleazlar tarafından eritilir.",
                    "4. Uç Boşluğu: Polimeraz 3' uca geriden başlayamayacağı için uç boş kalır.",
                    "5. Kısalma: Yeni sentezlenen kromozom 50-100 baz daha kısa kalır."
                ]
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-08-s55",
        "title": "Kritik Telomer Boyu: Hücresel Saatin Çalması",
        "subtitle": "Kilobaz bazında erime ve telomerik t-loop kapağının açılması",
        "badge": "Hücresel Saat",
        "badgeColor": "amber",
        "coreContent": {
            "text": (
                "Doğumda 10-15 kb olan telomerler her mitozla eriyerek genç erişkinde 8-10 kb'a, yaşlılarda ise 3-5 kb'a iner.\n\n"
                "Telomer boyu yaklaşık **4 kilobazın altına** indiğinde artık Shelterin kompleksi t-loop yapısını koruyamaz.\n\n"
                "Telomerik kapak (cap) açılır; çıplak DNA uçları açığa çıkar.\n\n"
                "> Bu an, hücresel saat için 'alarm çalma' anıdır; hücre telomerini çift zincir kırığı gibi algılar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomer boyu kritik eşiğin altına indiğinde koruyucu kapak açılarak hücreyi replikatif senesense sürükler.",
                "replikatif senesense",
                "Mitoz kapasitesinin tükenmesiyle girilen durağan faz"
            ),
            make_active_recall(
                "Normal bir somatik hücrede her bölünmede yaklaşık kaç baz çifti telomer DNA'sı aşınır?",
                "Yaklaşık 50 ila 100 (bazı kaynaklara göre 50-200) baz çifti telomerik DNA kaybı gerçekleşir."
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-08-s56",
        "title": "Açılan Telomerlerin DNA Hasar Yanıtını (DDR) Tetiklemesi",
        "subtitle": "Kromozom ucuna ATM bağlanması ve kalıcı telomer ilişkili odak (TAF)",
        "badge": "Sinyal İletimi",
        "badgeColor": "rose",
        "coreContent": {
            "text": (
                "Kapağı açılan çıplak telomer ucu, hücrenin gözünde 'tamir edilmesi gereken kırık bir çift zincir DNA'dır.\n\n"
                "Hasar algılayıcı **ATM** kinazı doğrudan telomer uçlarına yapışır ve histone H2AX'i fosforiller (**TAF** / Telomere-Associated Foci).\n\n"
                "Fakat ortada tamir edilecek gerçek bir kırık parçası yoktur; uç kalıcı olarak çıplaktır.\n\n"
                "> Bu nedenle DDR sinyali **hiç kapanmaz**; p53 sürekli fosforillenmiş halde kalarak hücreyi kalıcı senesense kilitler."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Açılan telomer uçlarında oluşan ve hiç sönmeyen DNA hasar odaklarına TAF odakları denir.",
                "TAF",
                "Telomere-associated foci kısaltması"
            ),
            make_causal_chain(
                "Telomer Açılmasından Senesens Döngüsüne",
                [
                    "1. Uç Açılması: Telomer 4 kb'ın altına inip Shelterin korumasını kaybeder.",
                    "2. ATM Kenetlenmesi: ATM kinaz açık ucu çift zincir kırığı sanıp bağlanır.",
                    "3. Kalıcı Fosforilasyon: Chk2 ve p53 sürekli aktif durumda tutulur.",
                    "4. p21 Patlaması: p21 proteini CDK2 ve CDK4/6'yı tamamen dondurur.",
                    "5. Replikatif Senesens: Hücre döngüsü bir daha açılmamak üzere G1/S'te kilitlenir."
                ]
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-08-s57",
        "title": "p53/p21 ve p16/Rb ile İki Kademeli Replikatif Blokaj",
        "subtitle": "Mortality Stage 1 (M1) evresi ve senesens kalesinin inşası",
        "badge": "Hücre Siklusu Kontrolü",
        "badgeColor": "cyan",
        "coreContent": {
            "text": (
                "Replikatif senesens tek bir moleküle bırakılmayıp iki kademeli çifte kilit sistemiyle mühürlenir:\n\n"
                "1. **M1 Evresi (İlk Blok - p53/p21):** Kısalan telomer DDR yoluyla p53'ü, o da p21'i uyarır. Hücre döngüsü durur.\n"
                "2. **Kalıcı Kilit (p16INK4a/Rb):** Süreç uzadıkça p16 birikir; CDK4/6'yı susturur ve Rb hipofosforile kalarak transkripsiyonu sonsuza dek kilitler.\n\n"
                "> Eğer hücrede hem p53 hem de Rb mutasyonla devre dışı bırakılırsa (örneğin viral onkoproteinler E6/E7 ile), hücre M1 senesensini atlatır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Replikatif senesensin ilk aşamasında hücre döngüsünü durduran birinci kilit p53/p21 eksenidir.",
                "p53/p21",
                "M1 evresi tümör baskılayıcı inhibitör çifti"
            ),
            make_table(
                ["Kontrol Basamağı", "Tetikleyici Uyarı", "Anahtar Molekül ve Etkisi"],
                [
                    [("M1 Başlatıcı Blok", False, ""), ("Telomer kısalması ve ATM uyarımı", False, ""), ("p53 stabilizasyonu ve p21 artışı", True, "Hücre siklusunu durduran ilk bariyer")],
                    [("Kalıcı Senesens Mührü", False, ""), ("Kromatin gevşemesi ve epigenetik stres", False, ""), ("p16INK4a artışı ve Rb hipofosforilasyonu", True, "Geri dönüşsüz kilit mekanizması")],
                    [("M2 Kriz Evresi", False, ""), ("p53/Rb kaybı sonrası bölünmenin sürmesi", False, ""), ("Kromozomal köprüleşme ve mitotik felaket", True, "Genomik instabilite ve yıkım dönemi")]
                ]
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-08-s58",
        "title": "Somatik, Kök ve Germ Hücrelerinde Telomer Dinamiği",
        "subtitle": "Üç farklı hücre sınıfında telomer kısalma hızı ve biyolojik kader",
        "badge": "Karşılaştırmalı Histoloji",
        "badgeColor": "slate",
        "coreContent": {
            "text": (
                "İnsan vücudundaki hücre tipleri telomer saati açısından üçe ayrılır:\n\n"
                "1. **Çoğu Somatik Hücre:** Telomeraz aktivitesi tamamen kapalıdır (yoktur). Her bölünmede telomer kısalır -> Replikatif senesens kaçınılmazdır.\n"
                "2. **Kök Hücreler (Hematopoetik vb.):** Düşük-orta düzeyde telomeraz aktivitesi vardır. Telomer kaybı yavaşlatılır ancak tamamen durdurulamaz (yaşla kök hücre rezervi azalır).\n"
                "3. **Germ Hücreleri (Sperm/Oosit):** Telomeraz aktivitesi çok yüksektir; telomer boyu korunur ve nesilden nesile aktarılır."
            )
        },
        "interactiveElements": [
            make_table(
                ["Hücre Sınıfı", "Telomeraz Aktivite Düzeyi", "Telomer Boyunun Yaşam Boyu Seyri"],
                [
                    [("Germ Hücreleri", False, ""), ("Çok Yüksek (Sürekli aktif)", False, ""), ("Telomer boyu tamamen korunur", True, "Gelecek kuşaklara aktarılan stabil kromozom")],
                    [("Kök Hücreler", False, ""), ("Düşük - Orta Seviyede", False, ""), ("Yavaşça kısalır, sınırlı koruma", True, "Doku yenilenmesinde rezerv tükenmesi")],
                    [("Somatik Hücreler", False, ""), ("Yok veya Eser Miktarda", False, ""), ("Her mitozda hızla kısalır", True, "Replikatif yaşlanmaya gidiş")]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki insan hücre tiplerinden hangisinde fizyolojik olarak yüksek telomeraz aktivitesi bulunur ve telomer boyu nesiller boyu korunur?",
                {
                    "A": "Deri keratinositleri",
                    "B": "Germ hücreleri (gamet öncülleri)",
                    "C": "Karaciğer hepatositleri",
                    "D": "Kalp kası miyositleri",
                    "E": "Böbrek tübül epiteli"
                },
                "B",
                {
                    "A": "Somatik hücredir, telomerazı kapalıdır.",
                    "B": "Doğru cevap B'dir: Germ hücrelerinde telomeraz sürekli yüksek eksprese edilir ve türün devamını sağlar.",
                    "C": "Somatiktir.",
                    "D": "Bölünmeyen post-mitotik somatiktir.",
                    "E": "Somatiktir."
                }
            )
        ]
    })

    # Slide 59 (CHECKPOINT 6)
    slides.append({
        "id": "k1-08-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Telomerler, Hayflick Limiti ve Replikatif Yaşlanma",
        "subtitle": "Bölüm 6 TTAGGG, Shelterin, Son Replikasyon Çıkmazı ve p16/p53",
        "badge": "Checkpoint 6",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 6,
        "coreContent": {
            "text": (
                "Altıncı kontrol noktasında telomer ve senesens ilkelerini sabitliyoruz:\n\n"
                "1. **Hayflick Limiti:** Normal somatik hücrelerin in vitro 50-60 bölünmeyle sınırlı olması.\n"
                "2. **Dizi ve Yapı:** 5'-TTAGGG-3' tekrarları; Shelterin kompleksi t-loop ile ucu saklar.\n"
                "3. **Son Replikasyon Problemi:** RNA primeri doldurulamadığı için her mitozda 50-100 bç kayıp.\n"
                "4. **Kritik Eşik:** Telomer 4 kb'ın altına inince kapak açılır, ATM bağlanır, TAF odakları oluşur.\n"
                "5. **M1 Blokajı:** p53/p21 ve p16/Rb hücre döngüsünü G1/S fazında kilitler."
            )
        },
        "interactiveElements": [
            make_micro_quiz(
                "İnsan kromozom uçlarındaki telomerleri oluşturan hekzanükleotid tekrar dizisi hangisidir?",
                {
                    "A": "TATAAA",
                    "B": "TTAGGG",
                    "C": "AATAAA",
                    "D": "CGCGGCG",
                    "E": "ATCGAT"
                },
                "B",
                {
                    "A": "TATA kutusu promotörüdür.",
                    "B": "Doğru cevap B'dir: Telomerlerin evrensel omurgalı dizisi 5'-TTAGGG-3' tekrarıdır.",
                    "C": "Poliadenilasyon sinyalidir.",
                    "D": "CpG adacığıdır.",
                    "E": "Rastgele dizidir."
                }
            ),
            make_active_recall(
                "Telomerlerin kısalması olmasaydı ve somatik hücreler sınırsız bölünebilseydi insan vücudunda hangi hastalık riski dramatik şekilde artardı?",
                "Malign neoplaziler (kanserler); çünkü telomer kısalması genetik hasar biriktiren hücrelerin kontrolsüzce çoğalmasını engelleyen en temel evrimsel tümör baskılama bariyeridir."
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-08-s60",
        "title": "Telomer Kısalması: Kanserden Koruyan Evrimsel Bir Fren",
        "subtitle": "Kısa vadede tümör baskılama, uzun vadede doku yaşlanması ve tükenme",
        "badge": "Evrimsel Paradoks",
        "badgeColor": "emerald",
        "coreContent": {
            "text": (
                "Telomer kısalması bir 'kusur' veya 'hata' değil; organizmayı gençlikte kanserden koruyan hayati bir **tümör baskılama mekanizmasıdır**.\n\n"
                "Eğer bir hücre onkogenik mutasyon geçirirse kontrolsüz bölünmeye başlar.\n\n"
                "Ancak telomer sayacı her mitozda eksildiği için bu hücre 40-50 bölünme sonra kaçınılmaz olarak duvara toslar (senesense girer) ve tümör kitlesi büyümeden durdurulur.\n\n"
                "> Bedeli ise ileri yaşta dokuların yenilenememesi, kök hücrelerin tükenmesi ve kaçınılmaz **organizma yaşlanmasıdır**."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomer kısalması kontrolsüz bölünen mutant klonları durdurarak kanserden koruyan evrimsel bir tümör baskılama bariyeridir.",
                "tümör baskılama",
                "Kanser gelişimine set çeken biyolojik mekanizma"
            ),
            make_branching_logic(
                "Bir genetik laboratuvarı tüm somatik hücrelerde telomerazı sürekli açık tutan transgenik bir fare üretiyor. Bu farenin yaşam beklentisi ve karşılaşacağı en büyük sağlık sorunu ne olur?",
                [
                    {"text": "Sonsuza dek yaşar ve hiçbir hastalık geçirmez.", "isCorrect": False, "feedback": "Kanser baskılama mekanizması çökecektir."},
                    {"text": "Telomer saati kalktığı için erken yaşta yaygın spontan malign tümörler (kanserler) gelişir ve erken ölür.", "isCorrect": True, "feedback": "Kusursuz onkolojik muhakeme! Telomer kısalması kanser frenidir; telomerazı denetimsiz açık tutulan hayvanlar masif tümör gelişiminden kaybedilir."},
                    {"text": "Anında aplastik anemi gelişir.", "isCorrect": False, "feedback": "Aplastik anemi telomeraz eksikliğinde görülür."}
                ]
            )
        ]
    })

    return slides
