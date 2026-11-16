# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 1: Temel Terminoloji ve Kavramsal Çerçeve (Slayt 1 - 10)
Checkpoint 1: Slayt 9
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # Slayt 1: Enfeksiyon ve Enfeksiyon Hastalığı Ayrımı
    slides.append({
        "id": "k1-21-s01",
        "title": "Enfeksiyon ve Enfeksiyon Hastalığı Ayrımı",
        "section": "Temel Terminoloji",
        "slideNumber": 1,
        "narrative": (
            "Klinik mikrobiyoloji ve enfeksiyon hastalıkları disiplininde en temel kavramsal ayrım, "
            "**enfeksiyon** ile **enfeksiyon hastalığı** arasındaki farktır. "
            "Enfeksiyon; potansiyel olarak hastalık yapabilen bir mikroorganizmanın (bakteri, virüs, mantar veya parazit) "
            "konak dokularına girmesi, yerleşmesi ve/veya burada çoğalması sürecidir. "
            "Burada hayati kural şudur: **Her enfeksiyon mutlaka klinik hastalıkla sonuçlanmaz!** "
            "Enfeksiyonların önemli bir kısmı konak bağışıklık sistemi tarafından sınırlandırılarak tamamen "
            "asemptomatik (belirtisiz) veya subklinik düzeyde seyredebilir. "
            "Buna karşılık, mikroorganizmanın çoğalması veya salgıladığı toksinler sonucunda konakta "
            "doku hasarı meydana gelir ve buna bağlı objektif fiziksel bulgular ile subjektif belirtiler "
            "(ateş, ağrı, organ disfonksiyonu) ortaya çıkarsa bu tabloya **enfeksiyon hastalığı** adı verilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mikroorganizmanın konakta çoğalmasına rağmen hiçbir klinik belirti vermediği durumlara subklinik enfeksiyon denir.",
                "subklinik enfeksiyon",
                "Belirti oluşturmaksızın sessizce ilerleyen mikrobiyal süreç"
            ),
            make_before_after(
                "Enfeksiyon ile Enfeksiyon Hastalığı Karşılaştırması",
                "Enfeksiyon (Kolonizasyon / Giriş)",
                [
                    "Mikroorganizmanın konağa girişi, yerleşmesi ve çoğalması",
                    "Klinik semptom ve fizik muayene bulgusu zorunlu değildir",
                    "Konak savunması etkeni sessizce temizleyebilir veya sınırlandırabilir",
                    "Örnek: Asemptomatik SARS-CoV-2 PCR pozitifliği"
                ],
                "Enfeksiyon Hastalığı (Klinik Tablo)",
                [
                    "Konakta aşikar hücresel/doku hasarı ve inflamasyon varlığı",
                    "Ateş, lökositoz, ağrı gibi objektif klinik bulgular mevcuttur",
                    "Fizyopatolojik süreç organ disfonksiyonuna yol açabilir",
                    "Örnek: Akut lober pnömoni veya ürosepsis tablosu"
                ]
            ),
            make_micro_quiz(
                "Enfeksiyon ve enfeksiyon hastalığı kavramları ile ilgili aşağıdaki ifadelerden hangisi biyolojik olarak doğrudur?",
                {
                    "A": "Vücuda giren her patojen mikroorganizma istisnasız enfeksiyon hastalığına yol açar.",
                    "B": "Enfeksiyon varlığı için mutlaka yüksek ateş ve lökositoz bulunması şarttır.",
                    "C": "Enfeksiyon mikroorganizmanın yerleşip çoğalmasıdır; belirti ve doku hasarı eklendiğinde enfeksiyon hastalığı adını alır.",
                    "D": "Enfeksiyon hastalığı terimi sadece virüslere bağlı klinik tablolar için kullanılır.",
                    "E": "Asemptomatik taşıyıcılarda enfeksiyon biyolojik olarak hiç gerçekleşmemiştir."
                },
                "C",
                {
                    "A": "A seçeneği yanlıştır; pek çok enfeksiyon subklinik kalır ve hastalık tablosuna ilerlemez.",
                    "B": "B seçeneği yanlıştır; subklinik enfeksiyonlarda ateş veya lökositoz görülmeyebilir.",
                    "C": "C seçeneği doğrudur: Enfeksiyon etkenin yerleşip çoğalmasıdır; klinik semptom ve doku hasarı geliştiğinde enfeksiyon hastalığı oluşur.",
                    "D": "D seçeneği yanlıştır; bakteri, mantar ve parazitler de enfeksiyon hastalığı yapar.",
                    "E": "E seçeneği yanlıştır; asemptomatik taşıyıcıda enfeksiyon vardır ancak hastalık belirtisi yoktur."
                }
            )
        ]
    })

    # Slayt 2: Patojenite ve Virülans Kavramları
    slides.append({
        "id": "k1-21-s02",
        "title": "Patojenite ve Virülans: Nitelik ve Derece Farkı",
        "section": "Temel Terminoloji",
        "slideNumber": 2,
        "narrative": (
            "Enfeksiyon tıbbında etkenin hastalık yapma potansiyeli iki temel terimle ifade edilir: "
            "**Patojenite** ve **Virülans**. Bu iki kavram sıklıkla birbiriyle karıştırılsa da aralarında net bir fark vardır. "
            "Patojenite, bir mikroorganizma türünün duyarlı bir konakta **hastalık oluşturabilme kapasitesidir (niteliksel özellik)**. "
            "Bir mikroorganizma ya patojendir (hastalık yapabilir) ya da non-patojendir (zararsızdır). "
            "Buna karşılık **Virülans**, patojenitenin derecesini veya şiddetini ifade eden **niceliksel bir ölçüttür**. "
            "Aynı mikroorganizma türünün farklı suşları çok farklı virülans düzeylerine sahip olabilir. "
            "Örneğin; kapsüllü Streptococcus pneumoniae suşları yüksek virülans gösterip fatal menenjit yaparken, "
            "kapsülsüz suşlar fagositozla hızla temizlenir ve düşük virülanslıdır. "
            "Virülans deneysel olarak **LD50 (Letal Doz 50 - deney hayvanlarının %50'sini öldüren doz)** "
            "ve **ID50 (İnfeksiyöz Doz 50 - %50'sinde enfeksiyon oluşturan doz)** parametreleri ile ölçülür. "
            "LD50 veya ID50 değeri ne kadar düşükse, o mikroorganizmanın virülansı o kadar yüksektir!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Patojenitenin derecesini ve oluşturduğu hastalığın ağırlık düzeyini ifade eden niceliksel terime virülans adı verilir.",
                "virülans",
                "Hastalık yapma şiddetinin derecesini belirten mikrobiyolojik terim"
            ),
            make_table(
                ["Kavram", "Tanım Niteliği", "Deneysel / Klinik Ölçüm"],
                [
                    ["Patojenite", "Hastalık oluşturabilme kapasitesi (Niteliksel)", "Patojen vs Non-patojen ayrımı"],
                    [
                        "Virülans",
                        {"text": "Patojenitenin derecesi ve şiddeti", "isMasked": True, "hint": "Patolojinin tahribat düzeyi"},
                        "LD50 ve ID50 sayısal değerleri"
                    ],
                    ["ID50 (İnfeksiyöz Doz)", "Deneklerin %50'sinde enfeksiyon başlatan doz", "Sayı küçüldükçe bulaştırıcılık artar"],
                    ["LD50 (Letal Doz)", "Deneklerin %50'sini öldüren mikrop dozu", "Sayı küçüldükçe ölümcüllük artar"]
                ]
            ),
            make_micro_quiz(
                "Deneysel mikrobiyoloji çalışmasında A bakterisinin LD50 değeri 10 hücre, B bakterisinin LD50 değeri 100.000 hücre olarak saptanmıştır. Bu veriye göre hangisi doğrudur?",
                {
                    "A": "B bakterisinin virülansı A bakterisinden 10.000 kat daha yüksektir.",
                    "B": "A bakterisi çok daha düşük dozda ölüm meydana getirdiği için virülansı B'den belirgin şekilde yüksektir.",
                    "C": "A bakterisi non-patojen bir flora elemanıdır.",
                    "D": "LD50 değeri ile virülans arasında doğru orantı mevcuttur.",
                    "E": "B bakterisi yalnızca hücre kültüründe çoğalabilir."
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; LD50 ne kadar düşükse virülans o kadar yüksektir.",
                    "B": "B seçeneği doğrudur: A bakterisi sadece 10 hücre ile deneklerin yarısını öldürebildiği için son derece yüksek virülanslıdır.",
                    "C": "C seçeneği yanlıştır; 10 hücre ile öldüren bakteri son derece ölümcül bir patojendir.",
                    "D": "D seçeneği yanlıştır; LD50 ile virülans ters orantılıdır.",
                    "E": "E seçeneği verilen veriden çıkarılamaz."
                }
            )
        ]
    })

    # Slayt 3: Kolonizasyon Dinamikleri
    slides.append({
        "id": "k1-21-s03",
        "title": "Kolonizasyon Dinamikleri: Patojenin Sessiz Yerleşimi",
        "section": "Temel Terminoloji",
        "slideNumber": 3,
        "narrative": (
            "Mikroorganizmaların insan vücudu ile kurduğu en yaygın etkileşim biçimlerinden biri **kolonizasyondur**. "
            "Kolonizasyon; bir mikroorganizmanın deri veya mukoza yüzeylerine tutunması, yerleşmesi ve orada çoğalması, "
            "ancak konak dokularına **invazyon yapmaması ve hiçbir hücresel hasar veya klinik hastalık belirtisi oluşturmamasıdır**. "
            "Kolonize olan mikroorganizma konağın fizyolojisini bozmaz; konak da belirgin bir yangısal (inflamatuar) yanıt vermez. "
            "Tıbbi pratikteki en klasik örnek: Sağlıklı erişkin bireylerin yaklaşık %20-30'unun anterior burun deliklerinde "
            "(anterior nares) **Staphylococcus aureus** taşımasıdır. Bu durum bir hastalık değil, basit bir kolonizasyondur. "
            "Ancak cerrahi bir insizyon, kateter takılması veya bağışıklığın baskılanması gibi anatomik bariyer bozulmalarında, "
            "burunda kolonize olan S. aureus cerrahi yara enfeksiyonuna veya bakteriyemiye yol açarak öldürücü bir enfeksiyon hastalığına dönüşebilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Sağlıklı erişkinlerin yaklaşık yüzde yirmisinde burun mukozasında doku hasarı yapmadan Staphylococcus aureus kolonizasyonu bulunur.",
                "kolonizasyonu",
                "Doku invazyonu ve hasar olmaksızın yerleşip çoğalma durumu"
            ),
            make_causal_chain(
                "Kolonizasyondan İnvaziv Enfeksiyona Geçiş Zinciri",
                [
                    "1. Nazal Tutunma: S. aureus burun mukozasındaki epitel hücre yüzeyine adezinlerle yapışır.",
                    "2. Asemptomatik Kolonizasyon: Bakteri mukozada çoğalır ancak dokuya invaze olmaz ve lökosit uyarılmaz.",
                    "3. Anatomik Bariyer İhlali: Hastaya santral venöz kateter takılır veya cerrahi insizyon yapılır.",
                    "4. Doku İnvazyonu: Mukozadaki bakteri açık damar yoluna girerek subkutan dokuya yayılır.",
                    "5. Enfeksiyon Hastalığı: Doku nekrozu, cerrahi alan apsesi, ateş ve lökositoz tablosu gelişir."
                ]
            ),
            make_active_recall(
                "Bir mikroorganizmanın doku hasarı ve bağışıklık yanıtı uyarmaksızın mukozalara yerleşip çoğalmasına ne ad verilir?",
                "Kolonizasyon adı verilir.",
                "Asemptomatik mikrobiyal yerleşim ve çoğalma terimi"
            )
        ]
    })

    # Slayt 4: Fırsatçı Patojenler ve Disbiyoz
    slides.append({
        "id": "k1-21-s04",
        "title": "Fırsatçı Patojenler ve Mikrobiyota Disbiyozu",
        "section": "Temel Terminoloji",
        "slideNumber": 4,
        "narrative": (
            "Mikroorganizmalar hastalık yapma potansiyellerine göre primer (zorunlu) patojenler ve **fırsatçı patojenler** olarak ikiye ayrılır. "
            "Primer patojenler (örneğin Mycobacterium tuberculosis veya Shigella) sağlıklı bireylerde bile hastalık oluşturabilirken; "
            "fırsatçı patojenler normal koşullarda bağışıklığı tam bireylerde hastalık oluşturamaz veya normal flora üyesi olarak sessizce yaşarlar. "
            "Ancak ne zaman ki konak savunması çöker (HIV/AIDS, kemoterapi, nötropeni), anatomik bariyerler bozulur "
            "veya geniş spektrumlu antibiyotik kullanımıyla normal flora dengesi (disbiyoz) bozulursa, "
            "bu mikroorganizmalar 'fırsatı yakalayarak' ağır ve invaziv enfeksiyonlara yol açarlar. "
            "Başlıca klinik prototipler: "
            "1. **Candida albicans:** Normal ağız ve vajina florasındayken, antibiyotik veya immünsüpresyonda oral pamukçuk ve invaziv kandidiyaza neden olur. "
            "2. **Pneumocystis jirovecii:** CD4 T lenfositleri 200'ün altına düşen HIV hastalarında ölümcül atipik pnömoni yapar. "
            "3. **Clostridioides difficile:** Geniş spektrumlu antibiyotiklerle kolon florası baskılanınca çoğalarak psödomembranöz enterokolite yol açar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Geniş spektrumlu antibiyotik tedavisi sonrasında kolon florasının baskılanmasıyla çoğalarak psödomembranöz kolit yapan fırsatçı bakteri Clostridioides difficile bakterisidir.",
                "Clostridioides difficile",
                "Antibiyotik ilişkili ishal ve psödomembran yapan sporlu anaerop etken"
            ),
            make_table(
                ["Fırsatçı Patojen", "Fırsat Yaratan Klinik Zemin", "Oluşturduğu Tipik Tablo"],
                [
                    ["Candida albicans", "Geniş spektrumlu antibiyotik veya steroid", "Oral pamukçuk ve vajinal kandidiyaz"],
                    [
                        "Pneumocystis jirovecii",
                        {"text": "Hücresel immün yetmezlik (CD4 < 200)", "isMasked": True, "hint": "HIV/AIDS hastalarındaki T lenfosit eşiği"},
                        "Hayatı tehdit eden interstisyel fırsatçı pnömoni"
                    ],
                    ["Clostridioides difficile", "Florayı yok eden antibiyotik disbiyozu", "Toksin aracılı psödomembranöz kolit"],
                    ["Pseudomonas aeruginosa", "Nötropeni, ağır yanıklar ve mekanik ventilatör", "Nekrotizan pnömoni ve ektima gangrenozum"]
                ]
            ),
            make_micro_quiz(
                "Fırsatçı patojenlerin genel özellikleri ile ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?",
                {
                    "A": "Pneumocystis jirovecii - Hücresel bağışıklık yetmezliğinde pnömoni",
                    "B": "Candida albicans - Nötropenik hastada sistemik kandidiyaz",
                    "C": "Clostridioides difficile - Normal floranın antibiyotikle bozulması sonucu kolit",
                    "D": "Mycobacterium tuberculosis - Yalnızca terminal AIDS hastalarında hastalık yapabilen zayıf fırsatçı",
                    "E": "Koagülaz-negatif stafilokoklar - İntravenöz kateteri olan hastada bakteriyemi"
                },
                "D",
                {
                    "A": "A seçeneği doğrudur; hücresel immün yetmezlikte klasik fırsatçıdır.",
                    "B": "B seçeneği doğrudur; nötropenide invaziv kandidiyaz gelişir.",
                    "C": "C seçeneği doğrudur; antibiyotik sonrası disbiyoz ile aktive olur.",
                    "D": "D seçeneği yanlıştır: M. tuberculosis primer (zorunlu) bir patojendir; bağışıklığı tamamen sağlam bireylerde de tüberküloz hastalığı oluşturabilir.",
                    "E": "E seçeneği doğrudur; yabancı cisim üzerinde biyofilm yapan fırsatçıdır."
                }
            )
        ]
    })

    # Slayt 5: Taşıyıcılık (Portörlük) ve Rezervuar Kavramları
    slides.append({
        "id": "k1-21-s05",
        "title": "Taşıyıcılık (Portörlük) ve Enfeksiyon Rezervuarları",
        "section": "Temel Terminoloji",
        "slideNumber": 5,
        "narrative": (
            "Enfeksiyon epidemiyolojisinde etkenin doğada nerede barındığı ve topluma nasıl yayıldığı "
            "**rezervuar** ve **taşıyıcı (portör)** kavramları ile açıklanır. "
            "Rezervuar; patojen mikroorganizmanın doğal olarak yaşadığı, çoğaldığı ve yaşamını sürdürmek için "
            "bağımlı olduğu ekolojik ortamdır. Rezervuarlar insanlar, hayvanlar veya cansız çevre olabilir. "
            "Örneğin; Legionella pneumophila'nın rezervuarı tatlı su kaynakları ve soğutma kuleleridir; "
            "Tetanoz etkeni Clostridium tetani'nin rezervuarı ise toprak ve hayvan dışkısıdır. "
            "**Taşıyıcı (Portör)** ise; kendisinde hiçbir klinik hastalık belirtisi bulunmadığı halde, "
            "vücudunda enfeksiyon etkenini barındıran ve bunu çevreye saçarak duyarlı insanlara bulaştıran kişidir. "
            "Epidemiyolojinin en meşhur örneği 'Tifolu Mary' (Mary Mallon) vakasıdır; safra kesesinde kronik olarak "
            "**Salmonella Typhi** taşıyan bu aşçı, kendisi hiç hastalanmadan onlarca insanın tifo kapmasına ve ölmesine yol açmıştır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Hastalık belirtisi göstermeden mikroorganizmayı vücudunda barındırıp çevreye bulaştıran kişilere portör adı verilir.",
                "portör",
                "Asemptomatik mikrop yayıcı birey terimi"
            ),
            make_before_after(
                "Rezervuar ile Kaynak Ayrımı",
                "Rezervuar (Doğal Barınak)",
                [
                    "Patojenin doğal olarak yaşadığı, çoğaldığı ekolojik ortam",
                    "Etkenin türünü devam ettirebilmesi için primer yaşam alanı",
                    "Örnek: Tatlı sular ve klima sistemleri (Legionella için)",
                    "Örnek: Küçük kemiriciler ve geyikler (Lyme Borrelia için)"
                ],
                "Kaynak (Bulaştırıcı Ortam)",
                [
                    "Patojenin konağa doğrudan veya dolaylı geçtiği anlık ortam",
                    "Etkenin içinde çoğalması zorunlu değildir, sadece aktarır",
                    "Örnek: Kontamine olmuş bir cerrahi alet veya kirli su bardağı",
                    "Örnek: Enfekte bir aşçının hazırladığı soğuk salata tabağı"
                ]
            ),
            make_active_recall(
                "Kronik asemptomatik Salmonella Typhi taşıyıcılığında bakterinin vücutta yıllarca saklandığı ve periyodik olarak dışkıya saçıldığı temel anatomik organ neresidir?",
                "Safra kesesidir (kolelitiyazis zemininde safra kesesi lümeni ve taş yüzeyleri).",
                "Tifo portörlüğünün primer hepatobiliyer odağı"
            )
        ]
    })

    # Slayt 6: Endojen vs Ekzojen Enfeksiyonlar
    slides.append({
        "id": "k1-21-s06",
        "title": "Bulaş Kaynağına Göre: Endojen ve Ekzojen Enfeksiyonlar",
        "section": "Temel Terminoloji",
        "slideNumber": 6,
        "narrative": (
            "Enfeksiyon hastalıkları patojenin konağa nereden ulaştığına bağlı olarak iki ana kaynaktan köken alır: "
            "1. **Endojen Enfeksiyonlar:** Hastalığı başlatan mikroorganizma, hastanın kendi normal mikrobiyotasında "
            "(deri, ağız, bağırsak, genital mukoza) zaten mevcuttur. "
            "Normalde zararsız olan bu flora üyesi; mukozal bariyerin bozulması, yabancı cisim yerleştirilmesi veya "
            "steril bir doku bölgesine yer değiştirmesi sonucunda patojen hale gelir. "
            "Örnekler: Deri florasındaki koagülaz-negatif stafilokokların (S. epidermidis) damar içi katetere yapışarak bakteriyemi yapması; "
            "kalın bağırsak florasındaki Escherichia coli'nin perine üzerinden üretraya tırmanarak akut sistit (idrar yolu enfeksiyonu) yapması; "
            "ağız florasındaki Viridans streptokokların diş çekimi sonrası hasarlı kalp kapaklarına yerleşip infektif endokardit oluşturmasıdır. "
            "2. **Ekzojen Enfeksiyonlar:** Mikroorganizma hastanın vücut dışındaki kaynaklardan "
            "(diğer insanlar, hayvanlar, kontamine gıdalar, hava damlacıkları veya tıbbi cihazlar) konağa girer. "
            "Örnekler: İnfluenza virüsü, kuduz virüsü, kolera (Vibrio cholerae) ve tetanozdur."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Normal kalın bağırsak florasında yaşayan Escherichia coli bakterisinin üretraya tırmanarak mesanede sistit yapması endojen enfeksiyon örneğidir.",
                "endojen enfeksiyon",
                "Bireyin iç kommensal kolonilerinden türeyen patoloji kaynağı"
            ),
            make_table(
                ["Enfeksiyon Tipi", "Patojenin Orijini", "Klasik Klinik Örnekler"],
                [
                    [
                        "Endojen Enfeksiyon",
                        {"text": "Konağın kendi normal mikrobiyotası", "isMasked": True, "hint": "Vücutta önceden bulunan flora elemanları"},
                        "E. coli üriner enfeksiyonu, S. epidermidis kateter sepsisi, Candida vajiniti"
                    ],
                    ["Ekzojen Enfeksiyon", "Vücut dışı çevre, insan veya hayvan", "Kızamık, Kuduz, Kolera, Şarbon, İnfluenza pnömonisi"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki enfeksiyon tablolarından hangisi tipik bir 'endojen enfeksiyon' örneğidir?",
                {
                    "A": "Köpek ısırması sonrası gelişen kuduz ensefaliti",
                    "B": "Kontamine konserve tüketimi sonrası gelişen Clostridium botulinum intoksikasyonu",
                    "C": "Kolon florasındaki E. coli'nin yukarı tırmanmasıyla gelişen akut piyelonefrit",
                    "D": "Kene tutunması sonrası gelişen Kırım-Kongo Kanamalı Ateşi",
                    "E": "Tüberkülozlu bir hastanın öksürük damlacıklarının solunmasıyla gelişen primer akciğer tüberkülozu"
                },
                "C",
                {
                    "A": "A seçeneği ekzojendir; hayvan tükürüğü ile bulaşır.",
                    "B": "B seçeneği ekzojendir; dış ortam gıdası ile alınır.",
                    "C": "C seçeneği doğrudur: E. coli hastanın kendi bağırsak florasının üyesidir; yer değiştirerek üriner sisteme girdiğinde endojen enfeksiyon oluşturur.",
                    "D": "D seçeneği ekzojendir; kene vektörü ile dışarıdan gelir.",
                    "E": "E seçeneği ekzojendir; dış ortamdan solunumla alınır."
                }
            )
        ]
    })

    # Slayt 7: Epidemiyolojik Dağılım: Endemi, Epidemi, Pandemi
    slides.append({
        "id": "k1-21-s07",
        "title": "Epidemiyolojik Dağılım: Endemi, Epidemi ve Pandemi",
        "section": "Temel Terminoloji",
        "slideNumber": 7,
        "narrative": (
            "Enfeksiyon hastalıklarının toplumda ve coğrafyada görülme sıklığı ve yayılım hızı, "
            "halk sağlığı ve epidemiyolojide 3 temel terimle sınıflandırılır: "
            "1. **Endemi:** Bir enfeksiyon hastalığının belirli bir coğrafi bölgede veya belirli bir toplulukta, "
            "zaman içinde **alışılmış (beklenen) sıklıkta ve sürekli olarak** görülmesidir. "
            "Örneğin; sıtmanın tropikal Sahra altı Afrika'da sürekli bulunması endemik bir durumdur. "
            "Türkiye'de ise Kırım-Kongo Kanamalı Ateşi (KKKA) İç Anadolu ve Orta Karadeniz havzasında endemiktir. "
            "2. **Epidemi (Salgın):** Belirli bir bölgede veya popülasyonda, bir hastalığın vaka sayısının "
            "**geçmiş deneyimlere göre beklenenden belirgin derecede daha fazla** ortaya çıkmasıdır. "
            "Bir su şebekesine kanalizasyon karışması sonucu bir şehirde aniden yüzlerce tifo veya kolera vakasının çıkması bir epidemidir. "
            "3. **Pandemi:** Bir enfeksiyon hastalığının kıtalararası veya dünya çapında çok geniş bir coğrafyada "
            "milyonlarca insanı etkileyecek şekilde küresel düzeyde yayılmasıdır. "
            "1918 İspanyol gribi ve 2020 SARS-CoV-2 (COVID-19) pandemisi küresel pandemi örnekleridir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Bir hastalığın birden fazla kıtaya yayılarak dünya çapında kitleleri etkilemesine pandemi adı verilir.",
                "pandemi",
                "Küresel ölçekteki salgınları ifade eden epidemiyolojik terim"
            ),
            make_table(
                ["Epidemiyolojik Düzey", "Görülme Karakteristiği", "Coğrafi / Zamansal Örnek"],
                [
                    ["Endemi", "Belirli bölgede alışılmış, beklenen sıklık", "Afrika'da sıtma, Orta Karadeniz'de KKKA"],
                    [
                        "Epidemi (Salgın)",
                        {"text": "Beklenenden çok daha fazla vaka artışı", "isMasked": True, "hint": "Sınırları aşan ani patlama"},
                        "Bir ilçede içme suyundan kaynaklanan ani kolera patlaması"
                    ],
                    ["Pandemi", "Kıtalararası, küresel çapta yayılım", "COVID-19 ve 1918 İnfluenza salgınları"]
                ]
            ),
            make_micro_quiz(
                "Bir enfeksiyon hastalığının belirli bir bölgede yıllardır 'beklenen ve alışılmış sıklıkta' sabit olarak görülmesi hangi epidemiyolojik terimle tanımlanır?",
                {
                    "A": "Pandemi",
                    "B": "Epidemi",
                    "C": "Endemi",
                    "D": "Sporadik olgu",
                    "E": "Hiperendemi"
                },
                "C",
                {
                    "A": "A seçeneği küresel yayılımı ifade eder.",
                    "B": "B seçeneği beklenenden belirgin fazla vaka artışıdır.",
                    "C": "C seçeneği doğrudur: Endemi belirli bir coğrafyada alışılmış sıklıkta seyretme durumudur.",
                    "D": "D seçeneği tek tük, düzensiz çıkan vakalardır.",
                    "E": "E seçeneği her yaşta aşırı yüksek prevalansla giden durumdur."
                }
            )
        ]
    })

    # Slayt 8: Enfeksiyon Hastalıklarında Genel Sistemik Belirti ve Bulgular
    slides.append({
        "id": "k1-21-s08",
        "title": "Enfeksiyon Hastalıklarında Sistemik Belirti ve Bulgular",
        "section": "Temel Terminoloji",
        "slideNumber": 8,
        "narrative": (
            "Enfeksiyon hastalıklarında mikroorganizmanın metabolik ürünleri ve konağın immün yanıtı "
            "(özellikle IL-1, TNF-alfa, IL-6 gibi proinflamatuar sitokinler) tüm sistemleri etkileyen genel klinik yanıtlara yol açar: "
            "1. **Genel Bulgular:** Hipotalamik termoregülasyon merkezinin pirojenlerle uyarılması sonucu **ateş**, "
            "deri vazokonstriksiyonuna bağlı **üşüme-titreme**, halsizlik, yaygın miyalji ve iştahsızlık (anoreksiya). "
            "2. **Kardiyovasküler:** Vücut sıcaklığındaki her 1°C artış kalp hızını dakikada yaklaşık 10 atım artırır (**taşikardi**). "
            "Ağır sepsiste ise vazodilatasyon ve kapiller kaçak nedeniyle hipotansiyon ve şok gelişir. "
            "3. **Hematolojik Yanıt:** Bakteriyel enfeksiyonlarda tipik olarak nötrofilik **lökositoz ve sola kayma** (çomak artışı); "
            "viral enfeksiyonlarda ise göreceli lenfositoz veya lökopeni izlenir. "
            "4. **Retiküloendotelyal Sistem:** Patojenlerin ve antijenlerin lenf bezlerinde süzülmesiyle **lenfadenopati (LAP)**, "
            "karaciğer ve dalakta mononükleer fagosit sistemin aktivasyonuyla **hepatosplenomegali** gelişebilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Vücut sıcaklığındaki her bir santigrat derece artışa karşılık nabız hızında yaklaşık on atımlık taşikardi yanıtı beklenir.",
                "taşikardi",
                "Ateşe eşlik eden kalp hızı artışı terimi"
            ),
            make_before_after(
                "Bakteriyel ve Viral Enfeksiyonlarda Hematolojik Yanıt",
                "Tipik Akut Bakteriyel Enfeksiyon",
                [
                    "Beyaz küre: Belirgin lökositoz (>12.000 /mm³)",
                    "Diferansiyel sayım: Nötrofil hakimiyeti (%70-80 üzeri)",
                    "Periferik yayma: Sola kayma (çomak ve bant formları artışı)",
                    "Akut faz reaktanları: Çok yüksek CRP ve Prokalsitonin artışı"
                ],
                "Tipik Viral Enfeksiyon",
                [
                    "Beyaz küre: Normal veya lökopeni (<4.000 /mm³)",
                    "Diferansiyel sayım: Göreceli veya mutlak lenfositoz",
                    "Periferik yayma: Atipik lenfositler (Downey hücreleri)",
                    "Akut faz reaktanları: CRP hafif-orta artar, prokalsitonin genellikle normaldir"
                ]
            ),
            make_active_recall(
                "Enfeksiyon hastalıklarında hipotalamustaki termostat merkezini uyararak ateşi tetikleyen temel endojen sitokinler hangileridir?",
                "İnterlökin-1 (IL-1), Tümör Nekroz Faktörü-alfa (TNF-alfa) ve İnterlökin-6'dır (IL-6).",
                "Endojen pirojen sitokin üçlüsü"
            )
        ]
    })

    # Slayt 9: [TEKRAR SAYFASI - CHECKPOINT 1]
    slides.append({
        "id": "k1-21-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Enfeksiyon Terminolojisi ve Temel Kavramlar",
        "section": "Temel Terminoloji",
        "slideNumber": 9,
        "narrative": (
            "Bu ilk checkpoint sayfasında enfeksiyon ile enfeksiyon hastalığı arasındaki temel farkı, "
            "virülans ve patojenite kavramlarının niteliksel/niceliksel ayrımını ve "
            "kolonizasyon ile endojen enfeksiyon mekanizmalarını "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp1-1",
                "Enfeksiyon ile enfeksiyon hastalığı arasındaki temel biyolojik ve klinik fark nedir?",
                "Enfeksiyon mikroorganizmanın konağa girip yerleşmesi ve çoğalmasıdır (asemptomatik olabilir). Enfeksiyon hastalığı ise mikroorganizmanın veya toksinlerinin doku hasarı yaparak klinik belirti ve bulgu oluşturmasıdır.",
                "Semptomsuz tutunum ile aşikar patolojik tablonun farkı",
                "Temel Terminoloji"
            ),
            make_flashcard(
                "fc-k1-21-cp1-2",
                "Patojenite ile virülans terimleri arasındaki nitelik-nicelik ayrımı nasıldır?",
                "Patojenite bir mikroorganizmanın hastalık yapabilme yeteneğidir (niteliksel: patojen veya non-patojen). Virülans ise patojenitenin derecesi ve hastalığın şiddetidir (niceliksel: LD50 ve ID50 ile ölçülür).",
                "Maraz oluşturma vasfı ile letal doza dayalı tehlike tartımı",
                "Mikrobiyal Nitelikler"
            ),
            make_flashcard(
                "fc-k1-21-cp1-3",
                "Kolonizasyon nedir ve hangi koşulda endojen bir enfeksiyon hastalığına dönüşür?",
                "Kolonizasyon mikroorganizmanın doku hasarı ve bağışıklık yanıtı yapmadan mukoza/deride çoğalmasıdır. Anatomik bariyerler bozulduğunda veya steril dokulara geçtiğinde endojen enfeksiyon hastalığına dönüşür.",
                "Zararsız yüzeyel üremenin savunma ihlaliyle parankime yayılması",
                "Kolonizasyon Dinamikleri"
            )
        ]
    })

    # Slayt 10: Bölüm Özeti ve Etkenler Alemine Geçiş
    slides.append({
        "id": "k1-21-s10",
        "title": "Temel Terminoloji Özeti: Patojenler Alemine Bakış",
        "section": "Temel Terminoloji",
        "slideNumber": 10,
        "narrative": (
            "Özetle; enfeksiyon mikroorganizmanın konak ile ilk biyolojik temasını ve çoğalmasını simgelerken, "
            "enfeksiyon hastalığı bu çoğalmanın doku hasarı ve sistemik yangısal bulgularla (ateş, taşikardi, lökositoz) "
            "somutlaştığı patolojik evredir. "
            "Patojenite mikroorganizmanın hastalık yapabilme yeteneği, virülans ise bu yeteneğin derecesidir. "
            "Bakteriler mukozalarımızda sessizce kolonize olarak yaşayabilirken, konak immünitesi çöktüğünde fırsatçı patojenlere dönüşebilirler. "
            "Enfeksiyonlar hastanın kendi florasından (endojen) veya dış çevreden (ekzojen) kaynaklanabilir; "
            "toplumda endemik, epidemik ya da küresel pandemi şeklinde yayılabilirler. "
            "İnsan vücudunda enfeksiyon oluşturabilen biyolojik etkenler alemi; aselüler prion ve virüslerden, "
            "prokaryotik bakterilere, ökaryotik mantar ve parazitlere kadar devasa bir çeşitlilik gösterir. "
            "İkinci bölümümüzde bu etkenler aleminin en küçük ve en gizemli üyeleri olan **prionlar ve virüsleri** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Deneysel çalışmalarda bir patojenin LD50 dozu ne kadar düşükse mikroorganizmanın virülansı o kadar yüksektir.",
                "virülansı",
                "Düşük öldürücü dozun temsil ettiği mikrobiyolojik patojenite derecesi"
            ),
            make_table(
                ["Etken Biyolojik Grubu", "Hücresel Organizasyon", "Örnek Enfeksiyon Etkenleri"],
                [
                    ["Aselüler Etkenler", "Hücresiz, nükleik asitsiz veya protein kılıflı", "Prionlar (CJD), Virüsler (İnfluenza, HIV)"],
                    [
                        "Prokaryotlar",
                        {"text": "Tek hücreli, çekirdek zarsız mikroorganizmalar", "isMasked": True, "hint": "Peptidoglikan duvarlı basit hücreler"},
                        "Tipik bakteriler, Klamidyalar, Mikoplazmalar, Riketsiyalar"
                    ],
                    ["Ökaryotlar", "Gerçek çekirdek ve membranlı organeller", "Mantarlar (Candida), Protozoonlar (Sıtma), Helmintler"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki biyolojik etkenlerden hangisi hücresel bir yapıya veya genetik nükleik aside sahip olmayan aselüler bir enfeksiyon ajanıdır?",
                {
                    "A": "Mycoplasma pneumoniae",
                    "B": "Prion proteini (PrPSc)",
                    "C": "Candida albicans",
                    "D": "Chlamydia trachomatis",
                    "E": "Toxoplasma gondii"
                },
                "B",
                {
                    "A": "A seçeneği hücresel yapısı olan bir prokaryotik bakteridir.",
                    "B": "B seçeneği doğrudur: Prionlar hiçbir nükleik asit (DNA/RNA) içermeyen, yalnızca hatalı katlanmış enfeksiyöz proteinlerden ibaret aselüler ajanlardır.",
                    "C": "C seçeneği ökaryotik bir mayadır.",
                    "D": "D seçeneği zorunlu hücre içi bir bakteridir.",
                    "E": "E seçeneği ökaryotik bir protozoondur."
                }
            )
        ]
    })

    return slides
