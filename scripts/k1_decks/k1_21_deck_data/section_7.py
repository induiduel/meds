# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 7: İnsan Mikrobiyotası ve Steril Bölgeler (Slayt 61 - 70)
Checkpoint 7: Slayt 69
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # Slayt 61: Normal Mikrobiyotanın Tanımı ve Yararları
    slides.append({
        "id": "k1-21-s61",
        "title": "İnsan Mikrobiyotası: Birlikte Yaşadığımız Trilyonlarca Dost",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 61,
        "narrative": (
            "Sağlıklı bir insanın deri ve mukoza yüzeylerinde doku hasarı veya hastalık oluşturmaksızın "
            "doğal olarak yaşayan mikroorganizma topluluğuna **Normal Mikrobiyota (Flora)** adı verilir. "
            "İnsan vücudundaki mikrobiyal hücre sayısı insan ökaryotik hücrelerinin sayısıyla neredeyse eşittir. "
            "Mikrobiyota konağa hayati fizyolojik yararlar sağlar: "
            "1. **Kolonizasyon Direnci (Bakteriyel İnterferans):** Reseptörleri işgal ederek, ortamdaki besinleri tüketerek "
            "ve bakteriyosin adı verilen antimikrobiyal maddeler salgılayarak dışarıdan gelen patojenlerin yerleşmesini engeller. "
            "2. **Metabolik ve Besinsel Katkı:** Kalın bağırsak bakterileri K vitamini ve B grubu vitaminleri (B12, biyotin, folat) sentezler; "
            "sindirilemeyen lifleri fermente ederek kolon epitelini besleyen kısa zincirli yağ asitleri (bütirat, asetat) üretir. "
            "3. **İmmün Sistem Eğitimi:** Mukoza ilişkili lenfoid dokunun (MALT) gelişimini ve sekretuvar IgA üretimini uyarır. "
            "Ancak flora statik değildir; antibiyotiklerle bozulduğunda fırsatçı enfeksiyonların kaynağı haline gelebilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Normal mikrobiyotanın patojenlerin tutunmasını ve çoğalmasını engelleyerek konağı korumasına kolonizasyon direnci adı verilir.",
                "kolonizasyon direnci",
                "Floranın dış patojenlere karşı oluşturduğu biyolojik koruma kalkanı"
            ),
            make_before_after(
                "Dengeli Mikrobiyota ile Antibiyotik Kaynaklı Disbiyoz Karşılaştırması",
                "Dengeli Fizyolojik Mikrobiyota",
                [
                    "Yüksek tür çeşitliliği ve dengeli anaerop-fakültatif oranı",
                    "Patojenlerin tutunmasını engelleyen güçlü kolonizasyon direnci",
                    "K vitamini ve kısa zincirli yağ asitlerinin kesintisiz sentezi",
                    "İnflamasyonsuz sağlıklı mukoza epiteli bütünlüğü"
                ],
                "Antibiyotik Kaynaklı Disbiyoz Tablosu",
                [
                    "Duyarlı flora üyelerinin yok olmasıyla azalan mikrobiyal çeşitlilik",
                    "Kolonizasyon direncinin çökmesiyle fırsatçı patojenlerin patlaması",
                    "Clostridioides difficile aşırı çoğalması ve toksin salınımı",
                    "Epitel hasarı, mukozal inflamasyon ve sulu-kanlı ishaller"
                ]
            ),
            make_active_recall(
                "Kalın bağırsaktaki normal mikrobiyota bakterileri tarafından sentezlenerek pıhtılaşma faktörlerinin (Faktör II, VII, IX, X) yapımına katkı sağlayan kritik vitamin hangisidir?",
                "K vitaminidir (özellikle K2 vitamini / menakinon).",
                "Barsak florası kaynaklı pıhtılaşma vitamini"
            )
        ]
    })

    # Slayt 62: Kesinlikle Steril Olan Vücut Bölgeleri
    slides.append({
        "id": "k1-21-s62",
        "title": "Kesinlikle Steril Kabul Edilen Vücut Bölgeleri",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 62,
        "narrative": (
            "Dış çevreye açık olan deri, solunum yolu, sindirim kanalı ve genital mukozalar trilyonlarca bakteri barındırırken; "
            "insan vücudunun iç ortamı ve kapalı kompartımanları **fizyolojik olarak tamamen sterildir (mikroorganizmasızdır)**. "
            "Bu bölgelerden alınan örneklerde tek bir mikroorganizmanın bile saptanması kural olarak kesin bir enfeksiyonu kanıtlar: "
            "1. **Merkezi Sinir Sistemi ve BOS:** Beyin omurilik sıvısı (BOS), meninksler ve beyin parankimi tamamen sterildir; mikrop varlığı menenjittir. "
            "2. **Dolaşım Sistemi (Kan ve Kemik İliği):** Dolaşım kanı sterildir; kanda canlı bakteri bulunması bakteriyemi/sepsis tablosudur. "
            "3. **Alt Solunum Yolları:** Vokal kordların altı, trakea, bronşlar ve alveoller sterildir (mukosiliyer klirens ve makrofajlar sağlar). "
            "4. **Üst Üriner Sistem:** Böbrek parankimi, renal pelvis, üreterler ve mesane içi idrar sterildir (distal üretra hariç). "
            "5. **Kapalı Vücut Boşlukları:** Plevra boşluğu, periton boşluğu, perikard boşluğu ve eklem içi sinovyal sıvı sterildir. "
            "6. **İç Organlar:** Karaciğer, dalak, pankreas, lenf bezleri sterildir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Fizyolojik olarak vokal kordların altındaki trakea, bronşlar ve akciğer alveolleri tamamen steril kabul edilir.",
                "steril",
                "Alt solunum yollarının mikropsuz olma durumu"
            ),
            make_table(
                ["Vücut Bölgesi", "Sterilite Durumu", "Mikrop Saptanmasının Klinik Anlamı"],
                [
                    ["Beyin Omurilik Sıvısı (BOS)", "Kesinlikle Steril", "Akut pürülan veya aseptik Menenjit"],
                    ["Dolaşım Kanı", "Kesinlikle Steril", "Bakteriyemi, Fungemi ve Sepsis sendromu"],
                    [
                        "Böbrek ve Mesane İdrarı",
                        {"text": "Fizyolojik olarak Steril", "isMasked": True, "hint": "Üst üriner sistem temizliği"},
                        "Piyelonefrit veya Üriner Sistem Enfeksiyonu (ÜSE)"
                    ],
                    ["Plevra ve Periton Sıvısı", "Kesinlikle Steril", "Ampiyem veya Peritonit"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki anatomik vücut bölgelerinden hangisi sağlıklı bir insanda 'fizyolojik olarak steril' olmayıp yoğun bir normal mikrobiyota barındırır?",
                {
                    "A": "Periton boşluğu sıvısı",
                    "B": "Beyin omurilik sıvısı (BOS)",
                    "C": "Orofarenks mukozası",
                    "D": "Sinovyal eklem sıvısı",
                    "E": "Perikardiyal sıvı"
                },
                "C",
                {
                    "A": "A seçeneği kapalı steril vücut boşluğudur.",
                    "B": "B seçeneği kesinlikle steril olmalıdır.",
                    "C": "C seçeneği doğrudur: Orofarenks dış çevreye açıktır ve Viridans streptokoklar ile anaeroblar gibi zengin bir mikrobiyota barındırır.",
                    "D": "D seçeneği sterildir.",
                    "E": "E seçeneği sterildir."
                }
            )
        ]
    })

    # Slayt 63: Deri Mikrobiyotası
    slides.append({
        "id": "k1-21-s63",
        "title": "Deri Mikrobiyotası: KNS, Cutibacterium ve Difteroidler",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 63,
        "narrative": (
            "Deri, yaklaşık 1.8 m²'lik yüzey alanıyla vücudun en geniş dış temas yüzeyidir. "
            "Kuru, tuzlu, dökülen keratinli ve asidik (sebum yağ asitleri nedeniyle pH ~5.5) yapısı nedeniyle "
            "yalnızca bu zorlu koşullara adapte olabilmiş spesifik mikroorganizmalar deride kalıcı flora kurabilir: "
            "1. **Koagülaz-Negatif Stafilokoklar (KNS):** Deri florasının en baskın bakterisidir; "
            "başta **Staphylococcus epidermidis** olmak üzere deri yüzeyinin %90'ını kaplar. "
            "Sağlıklı deride koruyucudur; ancak damar içi kateterler ve cerrahi protezler takıldığında yabancı cisme yapışarak "
            "hastane kaynaklı bakteriyemilerin ve protez enfeksiyonlarının 1 numaralı etkeni haline gelir. "
            "2. **Cutibacterium acnes (eski adı Propionibacterium acnes):** Oksijensiz sebase (yağ bezli) alanlarda "
            "(yüz, göğüs, sırt) kıl foliküllerinin derinliklerinde yaşar; sebum trigliseritlerini parçalayarak serbest yağ asitleri üretir ve akne vulgaris patogenezinde rol oynar. "
            "3. **Korinebakteriler (Difteroidler):** Aksilla ve ayak parmak araları gibi nemli bölgelerde yaşarlar. "
            "4. **Malassezia türleri:** Sebase alanlarda yaşayan lipofilik maya mantarlarıdır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Deri florasının en yaygın üyesi olan ve santral venöz kateter enfeksiyonlarında en sık izole edilen bakteri Staphylococcus epidermidis bakterisidir.",
                "Staphylococcus epidermidis",
                "Koagülaz-negatif deri stafilokoku türü"
            ),
            make_table(
                ["Deri Mikroorganizması", "Baskın Yaşam Bölgesi", "Tıbbi / Klinik Önemi"],
                [
                    [
                        "Staphylococcus epidermidis",
                        "Tüm deri yüzeyi (kuru ve nemli alanlar)",
                        {"text": "Biyofilm ile kateter ve protez enfeksiyonları", "isMasked": True, "hint": "Yabancı cisim enfeksiyonu etkeni"}
                    ],
                    ["Cutibacterium acnes", "Sebase bezler ve kıl folikülleri (yağlı yüz/sırt)", "Akne vulgaris ve omuz cerrahisi protez enfeksiyonu"],
                    ["Corynebacterium (difteroidler)", "Nemli kıvrım yerleri (aksilla, kasık)", "Deri kokusunun oluşumu ve bağışıklık uyarısı"],
                    ["Malassezia türleri", "Saçlı deri ve sebase gövde derisi", "Kepek, seboreik dermatit ve pitiriyazis versikolor"]
                ]
            ),
            make_micro_quiz(
                "Deri mikrobiyotasında sebase bezlerin derinliklerinde yaşayarak sebum trigliseritlerini parçalayan ve ergenlikteki akne lezyonlarında rol oynayan anaerop bakteri hangisidir?",
                {
                    "A": "Cutibacterium acnes",
                    "B": "Streptococcus pyogenes",
                    "C": "Escherichia coli",
                    "D": "Pseudomonas aeruginosa",
                    "E": "Lactobacillus acidophilus"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Cutibacterium acnes (Propionibacterium acnes) sebase foliküllerde yaşayan ve aknede rol oynayan deri kommensalidir.",
                    "B": "B seçeneği selülit ve farenjit yapar.",
                    "C": "C seçeneği kolon florasındadır.",
                    "D": "D seçeneği fırsatçı sucul bakteridir.",
                    "E": "E seçeneği vajina florasındadır."
                }
            )
        ]
    })

    # Slayt 64: Burun ve Orofarenks Mikrobiyotası
    slides.append({
        "id": "k1-21-s64",
        "title": "Burun ve Orofarenks Mikrobiyotası: Nazal S. aureus Taşıyıcılığı",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 64,
        "narrative": (
            "Üst solunum yolu, solunan havayla sürekli temas halinde olduğundan dinamik ve zengin bir mikrobiyotaya ev sahipliği yapar: "
            "1. **Anterior Burun Delikleri (Nares):** Burun mukozası, tıp fakültesi sınavlarının en klasik spot sorusudur: "
            "Sağlıklı erişkin popülasyonun yaklaşık **%20'si kalıcı (persistan)**, %30'u ise geçici olarak **Staphylococcus aureus** taşır! "
            "Bu taşıyıcılık bireyin kendisinde hiçbir burun semptomu oluşturmaz (kolonizasyon); "
            "ancak bu birey cerrahi ameliyata girdiğinde veya sağlık personeli olduğunda, kendi burnundan ellerine "
            "bulaşan S. aureus ile cerrahi yara enfeksiyonlarının ve hastane salgınlarının (özellikle MRSA) ana kaynağı haline gelir. "
            "2. **Orofarenks ve Ağız Boşluğu:** En baskın mikroorganizmalar **Viridans grubu streptokoklardır** "
            "(Streptococcus mutans diş çürüklerinden sorumludur; S. mitis, S. sanguinis). "
            "Ayrıca ağızda zengin anaeroblar (Veillonella, Fusobacterium, Prevotella), Neisseria türleri ve difteroidler bulunur. "
            "Viridans streptokoklar diş çekimi veya fırçalama sırasında kana karışarak (geçici bakteriyemi) "
            "doğuştan hasarlı veya protez kalp kapaklarına tutunup **Subakut İnfektif Endokardite** yol açabilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Sağlıklı erişkin bireylerin yaklaşık yüzde yirmisinde burun deliklerinde kalıcı Staphylococcus aureus taşıyıcılığı saptanır.",
                "Staphylococcus aureus",
                "Burun florasında asemptomatik kolonize olan majör piyojenik bakteri"
            ),
            make_causal_chain(
                "Ağız Florasından İnfektif Endokardite Gidiş Zinciri",
                [
                    "1. Ağız Kolonizasyonu: Viridans streptokoklar diş plağında ve dişeti cebinde yaşar.",
                    "2. Diş Müdahalesi: Diş çekimi veya derin temizlik sırasında dişeti kapillerleri yırtılır.",
                    "3. Geçici Bakteriyemi: Viridans streptokoklar dakikalar süren kısa bir bakteriyemiyle kana karışır.",
                    "4. Hasarlı Kapağa Tutunma: Bakteri dekstran salgılayarak mitral kapaktaki endotel hasarına yapışır.",
                    "5. Subakut Endokardit: Kapak üzerinde vejetasyon, ateş, kalp üfürümü ve emboli tablosu gelişir."
                ]
            ),
            make_active_recall(
                "Diş çekimi sonrasında kana karışarak hasarlı kalp kapaklarında subakut bakteriyel endokardit oluşturan ağız florası grubu hangisidir?",
                "Viridans grubu streptokoklardır (Streptococcus mutans, mitis, sanguinis).",
                "Ağız florasının alfa-hemolitik streptokokları"
            )
        ]
    })

    # Slayt 65: Gastrointestinal Sistem Mikrobiyotası: Mideden Kolona Artış
    slides.append({
        "id": "k1-21-s65",
        "title": "Gastrointestinal Mikrobiyota: Mideden Kolona Artan Yoğunluk",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 65,
        "narrative": (
            "Gastrointestinal sistem boyunca mikroorganizma sayısı ve çeşitliliği anatomik olarak homojen değildir; "
            "**mideden kolona doğru ilerledikçe logaritmik olarak muazzam bir artış gösterir**: "
            "1. **Mide:** Mide sıvısının aşırı asidik pH'sı (pH 1.5 - 2.0) ve pepsin enzimi nedeniyle "
            "mide mikrobiyolojik bir çöl gibidir. Bakteri yoğunluğu son derece düşüktür (< 10³ CFU/ml). "
            "Burada yaşayabilen en meşhur istisna, üreaz enzimiyle üreyi amonyağa çevirerek etrafında nötral bir asit kalkanı oluşturan **Helicobacter pylori**'dir. "
            "2. **Duodenum ve Jejunum:** Mideden gelen asit, hızlı bağırsak peristaltizmi ve safra/pankreas salgılarının "
            "deterjan etkisi nedeniyle ince bağırsağın üst kısımlarında da bakteri sayısı düşüktür (10³ - 10⁵ CFU/ml; ağırlıklı Lactobacillus ve Streptokoklar). "
            "3. **Distal İleum:** İleoçekal kapağa yaklaştıkça peristaltizm yavaşlar, pH nötralleşir ve bakteri sayısı hızla artar (10⁷ - 10⁸ CFU/ml); "
            "burada kolon florasının üyeleri (Enterobacterales ve anaeroblar) belirmeye başlar. "
            "4. **Kalın Bağırsak (Kolon):** İleoçekal kapak geçildikten sonra mikrobiyal yoğunluk zirveye ulaşır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Gastrointestinal sistem boyunca mikroorganizma yoğunluğu mideden kolona doğru ilerledikçe logaritmik olarak artış gösterir.",
                "mideden kolona doğru",
                "Sindirim kanalındaki mikrobiyal yoğunluk artış yönü"
            ),
            make_table(
                ["GİS Anatomik Bölgesi", "Bakteri Yoğunluğu (CFU/ml)", "Baskın Karakteristik Flora"],
                [
                    ["Mide", "< 10³ (Aşırı düşük yoğunluk)", "Asit toleranslı laktobasiller, Helicobacter pylori"],
                    ["Duodenum ve Jejunum", "10³ - 10⁵ (Düşük yoğunluk)", "Streptococcus, Lactobacillus türleri"],
                    [
                        "Distal İleum",
                        {"text": "10⁷ - 10⁸ (Orta-yüksek yoğunluk)", "isMasked": True, "hint": "Kolona geçiş öncesi artış"},
                        "Enterobacterales, Bacteroides, Enterokoklar"
                    ],
                    ["Kolon (Kalın bağırsak)", "10¹¹ - 10¹² (Devasa yoğunluk)", "Zorunlu anaeroblar (Bacteroides), E. coli, Clostridia"]
                ]
            ),
            make_micro_quiz(
                "Helicobacter pylori bakterisinin normalde mikroorganizmalar için öldürücü olan mide asidite ortamında (pH < 2) canlı kalabilmesini ve kolonize olmasını sağlayan anahtar enzimi hangisidir?",
                {
                    "A": "Katalaz",
                    "B": "Üreaz",
                    "C": "Koagülaz",
                    "D": "Amilaz",
                    "E": "Lesitinaz"
                },
                "B",
                {
                    "A": "A seçeneği hidrojen peroksiti parçalar.",
                    "B": "B seçeneği doğrudur: Üreaz üreyi karbondioksit ve bazik amonyağa çevirerek bakterinin etrafında asidi nötralize eden koruyucu bir mikroçevre kurar.",
                    "C": "C seçeneği pıhtılaşma yapar.",
                    "D": "D seçeneği nişasta sindirir.",
                    "E": "E seçeneği membran parçalar."
                }
            )
        ]
    })

    # Slayt 66: Kolon Mikrobiyotası: Anaerobların Saltanatı
    slides.append({
        "id": "k1-21-s66",
        "title": "Kolon Mikrobiyotası: Anaerobların Saltanatı",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 66,
        "narrative": (
            "Kalın bağırsak (kolon), insan vücudundaki en yoğun, en çeşitli ve metabolik açıdan en aktif "
            "mikrobiyal ekosistemdir. Dışkının kuru ağırlığının yaklaşık üçte birini bakteriler oluşturur "
            "(gram başına 10¹¹ - 10¹² koloni oluşturan birim - CFU). "
            "Kolon mikrobiyotasının en kritik sınav bilgisi: **Zorunlu anaerop bakterilerin mutlak hakimiyetidir!** "
            "Kolonda zorunlu anaerobların (oksijensiz yaşayanlar) fakültatif aerop bakterilere (E. coli gibi) oranı **1000:1** düzeyindedir! "
            "En baskın anaerob grup **Bacteroides türleri** (özellikle Bacteroides fragilis) ve **Bifidobacterium**, "
            "Lachnospiraceae ile Clostridium türleridir. "
            "Fakültatif anaerobik Gram-negatif basiller (**Enterobacterales**: Escherichia coli, Klebsiella) ve Enterokoklar "
            "kolon florasının sayıca sadece %0.1'ini oluşturur. "
            "Ancak bir apandisit patlaması veya kolon perforasyonunda periton boşluğuna sızan bu flora, "
            "Bacteroides fragilis ve E. coli'nin sinerjisiyle hayatı tehdit eden polimikrobiyal fekal peritonite yol açar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Kolon mikrobiyotasında zorunlu anaerop bakterilerin fakültatif aerop bakterilere sayısal oranı yaklaşık bine birdir.",
                "bine birdir",
                "Kolonda anaerobların ezici üstünlüğünü gösteren sayısal oran"
            ),
            make_before_after(
                "Kolondaki Zorunlu Anaeroblar ile Fakültatif Enterobacterales Oranı",
                "Zorunlu Anaeroblar (%99.9 Baskın)",
                [
                    "Kolon florasının ezici çoğunluğunu oluştururlar (1000 kat fazla)",
                    "Oksijen varlığında yaşayamazlar, fermantasyon yaparlar",
                    "Kısa zincirli yağ asitleri üreterek kolon sağlığını korurlar",
                    "Örnekler: Bacteroides fragilis, Bifidobacterium, Prevotella"
                ],
                "Fakültatif Aeroplar / Enterobacterales (%0.1 Azınlık)",
                [
                    "Kolon florasının sayıca binde birini oluştururlar",
                    "Oksijenli veya oksijensiz ortamda üreyebilirler",
                    "Kültürde hızla üredikleri için sıkça izole edilirler",
                    "Örnekler: Escherichia coli, Klebsiella pneumoniae, Enterococcus"
                ]
            ),
            make_active_recall(
                "Kalın bağırsak mikrobiyotasında en yoğun bulunan ve kolon perforasyonu sonrasında intraabdominal apselerin en sık anaerop etkeni olan bakteri hangisidir?",
                "Bacteroides fragilis bakterisidir.",
                "Kolonun en baskın gram-negatif zorunlu anaerop basili"
            )
        ]
    })

    # Slayt 67: Vajinal Mikrobiyota: Lactobacillus ve Bakteriyel Vajinoz
    slides.append({
        "id": "k1-21-s67",
        "title": "Vajinal Mikrobiyota: Lactobacillus Koruyuculuğu ve Bakteriyel Vajinoz",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 67,
        "narrative": (
            "Kadın genital sistemi mikrobiyotası, hormonal dalgalanmalara bağlı olarak yaşam döngüsünde dinamik değişimler gösterir: "
            "1. **Üreme Çağındaki Sağlıklı Vajina:** Yüksek östrojen düzeyleri vajina çok katlı yassı epitelinde "
            "yoğun **glikojen** depolanmasını sağlar. Bu glikojeni metabolize eden **Lactobacillus türleri (Döderlein basilleri)** "
            "vajina florasının %90'ından fazlasını oluşturur. Laktobasiller ürettikleri **laktik asit** ile vajinal pH'yı "
            "**asidik düzeyde (pH 3.8 - 4.5)** tutar ve hidrojen peroksit (H2O2) salgılayarak diğer patojenlerin yerleşmesini engeller. "
            "2. **Bakteriyel Vajinoz (BV):** Antibiyotik kullanımı, sık vajinal duş veya hormonal dengesizlikle laktobasiller yok olduğunda "
            "vajinal pH yükselir (> 4.5). Koruyucu asit kalkanı kalkınca başta **Gardnerella vaginalis** olmak üzere "
            "anaeroblar (Prevotella, Mobiluncus) aşırı çoğalır. "
            "Klinikte inflamasyonsuz (lökositsiz), homojen gri-beyaz akıntı, KOH damlatıldığında **bayat balık kokusu (Whiff testi +)** "
            "ve mikroskopta epitel sınırlarını silen bakterilerle kaplı **ipucu hücreleri (Clue cells)** saptanır!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Bakteriyel vajinoz mikroskopisinde vajina yassı epitel hücrelerinin yüzeyine çok sayıda bakterinin yapışmasıyla oluşan hücrelere ipucu hücreleri denir.",
                "ipucu hücreleri",
                "Clue cell olarak bilinen patognomonik vajinal epitel görüntüsü"
            ),
            make_table(
                ["Parametre", "Sağlıklı Normal Vajina", "Bakteriyel Vajinoz (BV)"],
                [
                    ["Baskın Mikroorganizma", "Lactobacillus türleri (Döderlein)", "Gardnerella vaginalis, Mobiluncus, anaeroblar"],
                    ["Vajinal pH Değeri", "Asidik (pH 3.8 - 4.5)", "Yükselmiş alkali/nötr (pH > 4.5)"],
                    [
                        "KOH Whiff (Koku) Testi",
                        "Negatif (Koku oluşmaz)",
                        {"text": "Pozitif (Keskin bayat balık kokusu)", "isMasked": True, "hint": "Aminlerin açığa çıkmasıyla oluşan koku"}
                    ],
                    ["Mikroskopi Bulgusu", "Bol çomak (laktobasil), temiz epitel", "Clue cells (ipucu hücreleri), laktobasil yok"]
                ]
            ),
            make_micro_quiz(
                "Homojen gri-beyaz vajinal akıntı şikayeti olan bir kadında vajinal pH 5.2 ölçülmüş, %10 KOH damlatıldığında balık kokusu alınmış ve mikroskopide clue cells görülmüştür. Bu tablonun temel patofizyolojik başlatıcısı nedir?",
                {
                    "A": "Vajinada Neisseria gonorrhoeae invazyonu",
                    "B": "Koruyucu Lactobacillus florasının kaybı ve vajinal pH'nın yükselmesi",
                    "C": "Candida albicans mayalarının aşırı çoğalması",
                    "D": "Trichomonas vaginalis parazitinin trofozoit invazyonu",
                    "E": "Aşırı östrojen salınımına bağlı asit fazlalığı"
                },
                "B",
                {
                    "A": "A seçeneği bol nötrofilli pürülan servisit yapar.",
                    "B": "B seçeneği doğrudur: Bakteriyel vajinoz bir enfeksiyon değil disbiyozdur; laktobasillerin çökmesi ve anaerobların patlamasıyla karakterizedir.",
                    "C": "C seçeneğinde pH asidiktir (< 4.5) ve koku negatiftir.",
                    "D": "D seçeneğinde çilek serviks ve hareketli kamçılılar görülür.",
                    "E": "E seçeneği asitliği artırır, BV'de asitlik azalır."
                }
            )
        ]
    })

    # Slayt 68: Üriner Sistem Mikrobiyotası ve Ürobiyom
    slides.append({
        "id": "k1-21-s68",
        "title": "Üriner Sistem Mikrobiyotası ve Yeni Kavram: Ürobiyom",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 68,
        "narrative": (
            "Üriner sistem anatomik ve mikrobiyolojik açıdan iki farklı kompartımanda değerlendirilir: "
            "1. **Distal Üretra:** Dış çevreye açılan son 1-2 santimetrelik üretra segmenti, "
            "perine ve deri florasının üyeleri ile (Koagülaz-negatif stafilokoklar, difteroidler, Streptococcus türleri) kolonizedir. "
            "Bu durum idrar tahlili ve kültüründe çok kritik bir kuralı doğurur: "
            "İdrar kültürü alınırken ilk gelen 10-15 ml'lik idrar distal üretrayı yıkadığı için çöpe atılmalı, "
            "flora kontaminasyonunu önlemek için mutlaka **orta akım idrarı (midstream urine)** toplanmalıdır! "
            "2. **Mesane ve Üst Üriner Sistem:** Klasik tıbbi mikrobiyolojide mesane içindeki idrar 'kesinlikle steril' kabul edilirdi. "
            "Ancak son yıllarda gelişen yeni nesil DNA dizileme (16S rRNA NGS) teknolojileri sayesinde, "
            "sağlıklı bireylerin mesanesinde de klasik kültürde üremeyen, düşük biyokütleli özelleşmiş bir mikrobiyal topluluk "
            "bulunduğu kanıtlanmıştır. Bu topluluğa **Ürobiyom (Urobiome)** adı verilmektedir. "
            "Ürobiyomun varlığı bir enfeksiyon anlamına gelmez; asemptomatik bakteriyüri ile karıştırılmamalıdır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "İdrar kültüründe distal üretra florasının kontaminasyonunu engellemek amacıyla ilk idrar atılarak orta akım idrarı toplanmalıdır.",
                "orta akım idrarı",
                "Kültür için en güvenilir temiz idrar örneği alma tekniği"
            ),
            make_table(
                ["Üriner Anatomik Bölge", "Geleneksel Kültür Durumu", "Moleküler / Flora Gerçeği"],
                [
                    ["Distal Üretra Dış Ağzı", "Zengin Flora Üremesi", "Deri ve perine kommensalleri (KNS, Difteroidler)"],
                    [
                        "Mesane İdrarı",
                        "Steril (Üreme Olmaz)",
                        {"text": "Düşük biyokütleli Ürobiyom varlığı", "isMasked": True, "hint": "16S rRNA ile gösterilen yeni mikrobiyom"}
                    ],
                    ["Üreterler ve Böbrek Parankimi", "Kesinlikle Steril", "Mikroorganizma saptanması piyelonefrit göstergesidir"]
                ]
            ),
            make_active_recall(
                "Sağlıklı bireylerin mesanesinde klasik kültür yöntemleriyle üretilemeyen ancak 16S rRNA dizilemeyle saptanan düşük yoğunluklu mikrobiyotaya ne ad verilir?",
                "Ürobiyom (Urobiome) adı verilir.",
                "Mesanenin yeni nesil dizilemeyle keşfedilen mikrobiyotası"
            )
        ]
    })

    # Slayt 69: [TEKRAR SAYFASI - CHECKPOINT 7]
    slides.append({
        "id": "k1-21-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Normal Mikrobiyota ve Steril Bölgeler",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 69,
        "narrative": (
            "Bu yedinci checkpoint sayfasında insan vücudunun steril kompartımanlarını, "
            "kolon florasında anaerobların ezici 1000:1 üstünlüğünü ve "
            "vajinal mikrobiyotada Lactobacillus'un koruyucu asit mekanizmasını "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp7-1",
                "İnsan vücudunda fizyolojik olarak kesinlikle steril kabul edilen başlıca anatomik bölgeler ve vücut sıvıları nelerdir?",
                "Beyin omurilik sıvısı (BOS), dolaşım kanı, alt solunum yolları (vokal kord altı), üst üriner sistem (mesane idrarı, üreter, böbrek) ve kapalı vücut boşluklarıdır (plevra, periton, perikard, eklem).",
                "Normale göre mutlak steril kabul edilen iç kompartımanlar",
                "Steril Bölgeler"
            ),
            make_flashcard(
                "fc-k1-21-cp7-2",
                "Kolon mikrobiyotasında zorunlu anaeroblar ile fakültatif aerop bakterilerin (E. coli) sayısal oranı nasıldır ve en baskın anaerop cins hangisidir?",
                "Zorunlu anaeroblar fakültatif aeroplara göre 1000 kat daha fazladır (1000:1 oranı). En baskın anaerop cins Bacteroides cinsidir (özellikle Bacteroides fragilis).",
                "Kolondaki ezici çoğunluktaki oksijensiz mikrop dengesi",
                "Kolon Florası"
            ),
            make_flashcard(
                "fc-k1-21-cp7-3",
                "Üreme çağındaki sağlıklı bir kadında vajinanın asidik pH'sını sağlayan temel bakteri ve bakteriyel vajinozdaki patofizyolojik değişiklik nedir?",
                "Sağlıklı vajinada glikojenden laktik asit üreten Lactobacillus türleridir (pH 3.8-4.5). Bakteriyel vajinozda laktobasiller çöker, pH 4.5'in üzerine çıkar ve Gardnerella ile anaeroblar aşırı çoğalır.",
                "Döderlein basili ile asidik pH oluşturan genital organ florası bekçisi",
                "Vajinal Mikrobiyota"
            )
        ]
    })

    # Slayt 70: Disbiyoz, Antibiyotikler ve C. difficile Koliti Özeti
    slides.append({
        "id": "k1-21-s70",
        "title": "Disbiyoz ve Antibiyotik İlişkili Kolit: Bölüm Özeti",
        "section": "Mikrobiyota ve Steril Bölgeler",
        "slideNumber": 70,
        "narrative": (
            "Özetle; normal mikrobiyotamız bizi dış patojenlere karşı koruyan canlı bir biyolojik kalkandır. "
            "Ancak modern tıbbın en sık yaptığı hatalardan biri, endikasyonsuz veya aşırı geniş spektrumlu "
            "antibiyotik kullanarak bu dost kalkanı yok etmektir (**Disbiyoz**). "
            "Özellikle klindamisin, florokinolonlar veya geniş spektrumlu sefalosporinler kullanıldığında "
            "kolondaki koruyucu Bacteroides ve anaerop topluluklar ölür. "
            "Bu boşlukta, sporları antibiyotikten etkilenmeyen **Clostridioides difficile** hızla çimlenir ve çoğalır. "
            "Salgıladığı Toksin A (enterotoksin) ve Toksin B (sitotoksin) ile kolon epitelini nekroze eder; "
            "fibrin, nötrofil ve ölü hücrelerden oluşan yalancı zarlarla kaplı **Psödomembranöz Enterokolit** tablosuna yol açar. "
            "Mikrobiyota sağlığı konak sağlığının ayrılmaz bir parçasıdır. "
            "Sekizinci bölümümüzde bir enfeksiyonun kaynaktan çıkıp yeni bir konağa ulaşmasını sağlayan "
            "**Enfeksiyon Zincirini ve hayvanlardan bulaşan Zoonozları** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Geniş spektrumlu antibiyotiklerin kolon florasını yok etmesi sonucu Clostridioides difficile toksinleriyle oluşan tabloya psödomembranöz kolit denir.",
                "psödomembranöz kolit",
                "Sarı-beyaz yalancı zarlarla seyreden antibiyotik ilişkili ağır bağırsak hastalığı"
            ),
            make_causal_chain(
                "Antibiyotik Kullanımından Psödomembranöz Kolite Zincir",
                [
                    "1. Geniş Spektrumlu Tedavi: Hasta klindamisin veya sefalosporin tedavisi alır.",
                    "2. Kolon Florası Yıkımı: Koruyucu anaerobik mikrobiyota ölür ve kolonizasyon direnci çöker.",
                    "3. C. difficile Çimlenmesi: Dirençli sporlar vejetatif bakteriye dönüşerek aşırı çoğalır.",
                    "4. Toksin A ve B Salınımı: Sitotoksinler kolon epitelyal aktin iskeletini parçalar.",
                    "5. Psödomembran Oluşumu: Nötrofil ve fibrinden zengin membranlar, toksik megakolon riski doğar."
                ]
            ),
            make_micro_quiz(
                "Geniş spektrumlu sefalosporin tedavisi sonrası günde 10 kez sulu ishal, ateş ve lökositoz gelişen hastada kolonoskopide mukozada sarı-beyaz kabarık plaklar (psödomembranlar) izleniyor. Kesin tanı ve etken nedir?",
                {
                    "A": "Vibrio cholerae - Kolera",
                    "B": "Clostridioides difficile - Psödomembranöz kolit",
                    "C": "Shigella dysenteriae - Basilli dizanteri",
                    "D": "Entamoeba histolytica - Amip dizanterisi",
                    "E": "Salmonella Enteritidis - Salmonelloz"
                },
                "B",
                {
                    "A": "A seçeneği pirinç suyu gibi ishal yapar, psödomembran yapmaz.",
                    "B": "B seçeneği doğrudur: Antibiyotik ilişkili psödomembranöz kolitin etkeni C. difficile toksinleridir.",
                    "C": "C seçeneği kanlı dizanteri yapar.",
                    "D": "D seçeneği flakon ülseri yapar.",
                    "E": "E seçeneği gıda zehirlenmesidir."
                }
            )
        ]
    })

    return slides
