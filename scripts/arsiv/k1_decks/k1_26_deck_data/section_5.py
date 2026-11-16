# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 5: Ağır Metal Toksisitesi: Kurşun, Cıva, Arsenik, Kadmiyum (Slayt 41-50)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_5_slides():
    slides = []

    # Slayt 41: Ağır Metal Toksikolojisine Giriş
    slides.append({
        "id": "k1-26-s41",
        "title": "Ağır Metal Toksikolojisine Giriş",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 41,
        "narrative": (
            "Ağır metaller, yüksek yoğunluklu elementler olup çevre kirliliği ve mesleki maruziyetin en tehlikeli aktörleridir: "
            "1. **Biyoakümülasyon ve Yarı Ömür:** Ağır metaller vücutta metabolize edilerek yok edilemez; "
            "dokularda (kemik, böbrek, karaciğer, beyin) yıllarca birikir (biyoakümülasyon) ve biyolojik yarı ömürleri onlarca yılı bulabilir. "
            "2. **Evrensel Toksik Mekanizma: Sülfhidril (-SH) Bağlanması:** "
            "- Kurşun, cıva ve arsenik; hücresel enzimlerin ve yapısal proteinlerin aktif merkezlerinde bulunan **sülfhidril (-SH) gruplarına** "
            "yüksek afiniteyle kovalent olarak bağlanır. "
            "- Enzim konformasyonunu bozar, katalitik aktiviteyi bloke eder ve proteini inaktive eder. "
            "3. **Kalsiyum ve Çinko Taklidi:** Kurşun, $Ca^{2+}$ ve $Zn^{2+}$ iyonlarını taklit ederek kemik matriksine çöker, "
            "iyon kanallarını bozar ve nörotransmitter salınımını felç eder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Ağır Metallerin Temel Toksik Etki Prensipleri",
                ["Mekanizma", "Biyokimyasal Karşılığı", "Patolojik Sonucu"],
                [
                    ["Sülfhidril (-SH) İnhibisyonu", "Enzim aktif merkezindeki sisteinlere bağlanma", "Kritik metabolik yolakların ve antioksidan enzimlerin felci"],
                    [
                        "Katyon Taklidi",
                        "Ca2+ ve Zn2+ yerine iyon kanallarına oturma",
                        {"text": "Kemik hidroksiapatit kristallerinde kalıcı depolanma", "isMasked": True, "hint": "Ağır metalin kemik kalsiyumunun yerine geçerek on yıllarca dokuda kalması"}
                    ],
                    ["Oksidatif Stres", "Fenton reaksiyonları ile serbest radikal (ROS) üretimi", "Membran lipid peroksidasyonu ve DNA kırıkları"]
                ]
            ),
            make_active_recall(
                "Kurşun, cıva ve arsenik gibi ağır metallerin hücresel enzimlerin aktif merkezlerine bağlanarak onları inaktive etmesini sağlayan temel kimyasal fonksiyonel grup hangisidir?",
                "Sülfhidril (-SH / tiyol) gruplarıdır.",
                "Sistein aminoasidinde yer alan kükürt ve hidrojen atomu bağı"
            )
        ]
    })

    # Slayt 42: Kurşun (Pb) Maruziyet Yolları ve Çevresel Kaynaklar
    slides.append({
        "id": "k1-26-s42",
        "title": "Kurşun (Pb) Maruziyet Yolları ve Çevresel Kaynaklar",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 42,
        "narrative": (
            "Kurşun ($Pb$), çevrede yaygın olarak bulunan ve hiçbir biyolojik faydası olmayan son derece sinsi bir toksindir: "
            "1. **Tarihsel ve Güncel Kaynaklar:** "
            "- **Eski Boyalar:** 1978 öncesi inşa edilmiş eski binalarda kullanılan kurşun bazlı yağlı boyalar dökülüp pul pul dökülür; "
            "emekleyen bebeklerin bu boya kırıntılarını ve tozunu yemesi (**pika davranışı**) en önemli çocukluk çağı zehirlenme yoludur. "
            "- **Su Tesisatı:** Eski kurşun borulardan ve kurşun lehimli bakır borulardan içme suyuna kurşun sızar (Flint su krizi prototipi). "
            "- **Sanayi ve Mesleki Maruziyet:** Akü imalatı ve geri dönüşümü, lehimcilik, dökümhaneler, oto tamirciliği ve boya sanayii. "
            "2. **Kurşunsuz Benzin Başarısı:** Benzine vuruntu önleyici olarak eklenen tetraetil kurşunun yasaklanmasıyla "
            "toplumun kan kurşun seviyelerinde %80'den fazla dramatik düşüş sağlanmıştır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Kurşun Maruziyetinde Çocuk vs Erişkin Ayrımı",
                "Çocukluk Çağı Maruziyeti",
                "Eski evlerde dökülen tatlımsı kurşunlu boya pullarının ve tozunun pika ile yutulması; GIS emilimi %50'dir",
                "Erişkin / Mesleki Maruziyet",
                "Akü fabrikaları ve dökümhanelerde kurşun buharı ve tozunun solunması; GIS emilimi %10 civarındadır"
            ),
            make_cloze(
                "Küçük çocuklarda eski binaların dökülen kurşunlu boya parçalarını ağza alma ve yutma davranışına pika adı verilir.",
                "pika",
                "Besin değeri olmayan maddeleri yeme ile karakterize çocukluk çağı alışkanlığı"
            )
        ]
    })

    # Slayt 43: Çocuklarda Kurşun Emilimi ve Nörogelişimsel Hasar
    slides.append({
        "id": "k1-26-s43",
        "title": "Çocuklarda Kurşun Emilimi ve Nörogelişimsel Hasar",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 43,
        "narrative": (
            "Çocuklar kurşun toksisitesine karşı erişkinlere kıyasla anatomik ve fizyolojik olarak katbekat daha savunmasızdır: "
            "1. **Gastrointestinal Emilim Farkı:** Yutulan kurşunun erişkinlerde yalnızca yaklaşık **%10'u** emilirken, "
            "küçük çocuklarda bağırsaktan emilim oranı **%50'ye kadar ulaşır**! Kalsiyum veya demir eksikliği olan çocuklarda emilim daha da artar. "
            "2. **Kan-Beyin Bariyeri Geçirgenliği:** Çocuklarda kan-beyin bariyeri henüz tam olgunlaşmamıştır; kurşun hızla serebral "
            "kortekse geçer. "
            "3. **Santral Sinir Sistemi (SSS) Toksisitesi:** "
            "- Kurşun $Ca^{2+}$ iyonunu taklit ederek presinaptik nörotransmitter salınımını bozar ve sinaptogenezi engeller. "
            "- **Düşük Doz Kronik Maruziyet:** Belirgin klinik semptom olmaksızın **IQ puanında düşüş**, dikkat eksikliği ve hiperaktivite (DEHB), "
            "okul başarısızlığı ve agresif davranış bozukluklarına yol açar (güvenli bir kan kurşun eşiği yoktur!). "
            "- **Yüksek Doz Akut Zehirlenme:** Şiddetli **kurşun ensefalopatisi**, yaygın serebral ödem, inatçı konvülsiyonlar, koma ve kalıcı zeka geriliği."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Çocukta Kurşun Maruziyetinden Ensefalopatiye Giden Yolak",
                [
                    "1. Oral Alım: Kurşunlu boya tozunun yutulması ve bağırsaktan yüzde elli oranında yüksek emilimi",
                    "2. Bariyer Aşımı: Olgunlaşmamış kan-beyin bariyerini aşarak serebral nöronlara ulaşması",
                    "3. Kalsiyum Antagonizmi: Sinaptik vezikül salınımını ve protein kinaz C aktivasyonunu felç etmesi",
                    "4. Endotel Hasarı: Serebral kapiller endotelde sızıntı, kanama ve masif serebral ödem gelişimi",
                    "5. Nörokognitif Çöküş: İnatçı nöbetler, koma ve kalıcı bilişsel gerilik (ensefalopati)"
                ]
            ),
            make_active_recall(
                "Küçük çocuklarda gastrointestinal sistemden kurşun emilim oranının (%50) erişkinlere (%10) göre beş kat yüksek olması ve hangi anatomik bariyerin henüz immatür olması nörotoksisiteyi katlamaktadır?",
                "Kan-beyin bariyeridir.",
                "Beyin kapiller endotelinin sıkı bağlantılarından oluşan koruyucu endotelyal filtre"
            )
        ]
    })

    # Slayt 44: Kurşun Toksisitesinde Hematolojik Hasar
    slides.append({
        "id": "k1-26-s44",
        "title": "Kurşun Toksisitesinde Hematolojik Hasar: Anemi ve Bazofilik Beneklenme",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 44,
        "narrative": (
            "Hematolojik sistem kurşunun en duyarlı hedefidir ve periferik kanda tanısal patognomonik izler bırakır: "
            "1. **Hem Sentez Enzimlerinin İnhibisyonu:** "
            "- Kurşun, hem biyosentezinde rol alan iki kritik enzimin aktif merkezindeki sülfhidril (-SH) gruplarına bağlanarak bloke eder: "
            "  * **Delta-Aminolevulinik Asit Dehidrataz (ALA-Dehidrataz):** İnhibe olunca kanda ve idrarda ALA birikir. "
            "  * **Ferrokelataz:** Protoporfirin IX halkasına demir ($Fe^{2+}$) atomunun takılmasını katalizler. Kurşun bu enzimi felç edince "
            "demir hem molekülüne bağlanamaz; eritrositlerde **Serbest Eritrosit Protoporfirini (FEP)** ve çinko-protoporfirin fırlar! "
            "2. **Anemi Morfolojisi:** Hem sentezi durduğu için tipik **Mikrositer Hipokromik Anemi** gelişir (demir eksikliği anemisiyle karışabilir). "
            "3. **Patognomonik Periferik Yayma: Bazofilik Beneklenme (Basophilic Stippling):** "
            "- Kurşun, eritrositlerde ribozomları yıkan **pirimidin-5'-nükleotidaz** enzimini inhibe eder. "
            "- Parçalanamayan ribozomal RNA (rRNA) eritrosit sitoplazmasında kümelenir; Wright boyasında eritrositlerin içinde "
            "**noktasal koyu mavi-mor tanecikler (bazofilik beneklenme)** şeklinde görülür!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kurşunun Hem Sentezini ve Eritrositleri Bozma Mekanizması",
                ["Hedef Enzim / Yapı", "Kurşunun Toksik Etkisi", "Laboratuvar / Morfolojik Belirteç"],
                [
                    ["ALA-Dehidrataz", "Enzim inhibisyonu ve substrat birikimi", "İdrar ve kanda delta-ALA yükselmesi"],
                    [
                        "Ferrokelataz",
                        "Demirin protoporfirine takılamaması",
                        {"text": "Çinko protoporfirin ve serbest protoporfirin artışı", "isMasked": True, "hint": "Demir bağlanamayan porfirin halkasının eritrositte oluşturduğu floresan belirteç"}
                    ],
                    ["Pirimidin-5'-Nükleotidaz", "Ribozomal RNA yıkımının durması", "Periferik yaymada eritrositlerde BAZOFİLİK BENEKLENME"],
                    ["Genel Eritrosit Morfolojisi", "Hemoglobin sentezinin çökmesi", "Mikrositer hipokromik anemi"]
                ]
            ),
            make_micro_quiz(
                "Kurşun zehirlenmesi olan bir hastanın periferik kan yaymasında eritrositlerin sitoplazmasında izlenen koyu mavi-mor noktasal 'bazofilik beneklenme' görüntüsünün biyokimyasal ve organel düzlemindeki temel nedeni nedir?",
                {
                    "A": "Pirimidin-5'-nükleotidaz inhibisyonuna bağlı ribozomal RNA kümelerinin parçalanamayıp çökmesi",
                    "B": "Demir kristallerinin mitokondri membranını yırtarak sitoplazmaya saçılması",
                    "C": "Hücre çekirdeğinin parçalanarak DNA fragmanlarının etrafa dağılması",
                    "D": "Lipid damlacıklarının Sudan boyasıyla boyanması",
                    "E": "Bakteriyel toksinlerin eritrosit zarını delmesi"
                },
                "A",
                {
                    "A": "Doğrudur; pirimidin-5'-nükleotidaz bloke olunca rRNA parçalanamaz ve karakteristik bazofilik benekleri yapar.",
                    "B": "Yanlış; demir birikimi sideroblastik anemide halkalı sideroblast yapar.",
                    "C": "Yanlış; Howell-Jolly cisimciği DNA artığıdır, beneklenme rRNA'dır.",
                    "D": "Yanlış; lipid birikimi değildir.",
                    "E": "Yanlış; bakteriyel enfeksiyon değildir."
                }
            )
        ]
    })

    # Slayt 45: Kurşun Toksisitesinde İskelet ve Sinir Tutulumu
    slides.append({
        "id": "k1-26-s45",
        "title": "Kurşun Toksisitesinde İskelet ve Sinir Tutulumu",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 45,
        "narrative": (
            "Kurşun zehirlenmesi, kemiklerde ve periferik sinir sisteminde tanı koydurucu karakteristik izler bırakır: "
            "1. **İskelet ve Kemik Tutulumu (Kurşun Çizgileri - Lead Lines):** "
            "- Emilim sonrası vücuttaki kurşunun **%80-85'i kemiklerde** kalsiyumla yarışarak hidroksiapatit kristallerine çöker. "
            "- Çocuklarda kemik büyüme plaklarında osteoklastik kıkırdak rezorpsiyonunu baskılar; kalsifiye kıkırdak dokusu yıkılamaz. "
            "- Radyografide uzun kemiklerin metafizlerinde (özellikle diz çevresi: femur distali ve tibia proksimali) "
            "son derece belirgin beyaz radyoopak bantlar (**Radyolojik Kurşun Çizgileri**) izlenir. "
            "2. **Burton Çizgisi (Diş Eti Bulgusu):** "
            "- Tükürükteki kurşunun ağızdaki bakterilerin ürettiği hidrojen sülfürle reaksiyona girmesiyle **çözünmeyen siyah kurşun sülfür ($PbS$)** çöker. "
            "- Diş eti kenarında mor-mavi-siyah renkte hiperkromatize çizgi (**Burton çizgisi**) oluşur. "
            "3. **Erişkinde Motor Periferik Nöropati (Düşük El / Bilek Düşmesi):** "
            "- Erişkinlerde sensoryal değil, **saf motor periferik nöropati** gelişir. "
            "- En çok kullanılan kasları innerve eden sinirler etkilenir: En klasik tutulum **radial sinirin motor felcidir**. "
            "Ekstansör kaslar çalışamaz; hasta el bileğini yukarı kaldıramaz (**Düşük El / Wrist Drop**). Bazen peroneal sinir tutulumuyla düşük ayak da eşlik eder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kurşunun Kemik, Diş Eti ve Sinir Bulguları",
                ["Anatomik Bölge", "Karakteristik Patolojik Lezyon", "Patofizyolojik Mekanizma"],
                [
                    ["Kemik Metafizleri (Röntgen)", "Radyoopak Kurşun Çizgileri (Lead Lines)", "Kalsifiye kıkırdak rezorpsiyonunun durması ve kurşun depolanması"],
                    [
                        "Diş Eti Sınırı",
                        {"text": "Burton çizgisi (mavi-siyah kurşun sülfür hattı)", "isMasked": True, "hint": "Ağız bakterilerinin sülfürü ile tükürük kurşununun birleşerek diş etine çökmesi"},
                        "Gingival kurşun sülfür (PbS) presipitasyonu"
                    ],
                    ["Radial Sinir", "Düşük el (Wrist drop / bilek düşmesi)", "Motor aksonal dejenerasyon ve demiyelinizasyon"],
                    ["Gastrointestinal", "Şiddetli kurşun koliği (kolik abdominal ağrı)", "Bağırsak düz kas tonusunun ve otonomik gangliyonların bozulması"]
                ]
            ),
            make_active_recall(
                "Akü imalatında çalışan bir işçide bilateral el bileğini yukarı kaldıramama (düşük el) ve diş etlerinde mavi-siyah hiperpigmente çizgi saptanması durumunda altta yatan kesin mesleki zehirlenme nedir?",
                "Kronik kurşun zehirlenmesidir (satürnizm).",
                "Ağır metalin radial motor nöropati ve Burton çizgisi yapması tablosu"
            )
        ]
    })

    # Slayt 46: Cıva (Hg) Toksisitesi ve Minamata Hastalığı
    slides.append({
        "id": "k1-26-s46",
        "title": "Cıva (Hg) Toksisitesi ve Minamata Hastalığı",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 46,
        "narrative": (
            "Cıva ($Hg$), doğada elementer, inorganik ve organik formlarda bulunan güçlü bir nörotoksindir: "
            "1. **Metilcıva ve Sucul Besin Zinciri:** "
            "- Sanayi atıklarıyla göllere ve denizlere dökülen inorganik cıva, dipteki anaerobik bakteriler tarafından "
            "aşırı derecede lipofilik ve toksik olan **Metilcıva ($CH_3Hg$)** bileşiğine dönüştürülür (biyometilasyon). "
            "- Metilcıva planktonlardan balıklara doğru besin zincirinde katlanarak zenginleşir (biyoakümülasyon). "
            "2. **Minamata Hastalığı (Tarihsel Felaket):** "
            "- 1950'lerde Japonya'nın Minamata Körfezi'nde kimya fabrikasının atıklarıyla kirlenen balıkları yiyen gebe kadınlar, "
            "kendilerinde hafif semptomlar olduğu halde bebeklerini ağır anomalilerle doğurmuşlardır: "
            "- Metilcıva plasenta bariyerini kolayca geçer; gelişmekte olan fetal beyinde nöronal göçü ve bölünmeyi felç eder. "
            "- Sonuç: **Fetal mikrosefali**, serebral palsi, sağırlık, körlük ve derin mental retardasyon. "
            "3. **Erişkin Cıva Zehirlenmesi:** Serebellar ataksi, görme alanı daralması (tünel görme), parasteziler, "
            "aşırı duygusal dalgalanmalar ('deli şapkacı' sendromu) ve nefrotik böbrek hasarı."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Metilcıvanın Fetal Beyin Hasarı Oluşturma Döngüsü",
                [
                    "1. Biyometilasyon: İnorganik cıva atıklarının dip bakterilerince metilcıvaya çevrilmesi",
                    "2. Biyomagnifikasyon: Büyük yırtıcı balıklarda cıva konsantrasyonunun binlerce kat artması",
                    "3. Anne Tarafından Tüketim: Gebelikte kontamine deniz ürünlerinin yenmesi",
                    "4. Plasental Geçiş: Metilcıvanın aminoasit taşıyıcılarıyla plasentayı ve fetal kan-beyin bariyerini aşması",
                    "5. Serebral Hasar: Fetal nöron göçünün durması, mikrosefali ve Minamata hastalığı"
                ]
            ),
            make_cloze(
                "Japonya'da cıva ile kirlenmiş balıkların tüketilmesi sonucu fötal mikrosefali ve serebral palsi ile beliren konjenital toksik tabloya Minamata hastalığı adı verilir.",
                "Minamata hastalığı",
                "Deniz ürünlerindeki metilcıva birikimiyle anne karnındaki bebek beynini tahrip eden tarihi nörotoksik facia"
            )
        ]
    })

    # Slayt 47: Arsenik (As) Maruziyeti ve Karsinojenez
    slides.append({
        "id": "k1-26-s47",
        "title": "Arsenik (As) Maruziyeti ve Karsinojenez",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 47,
        "narrative": (
            "Arsenik ($As$), tarih boyunca cinayet zehri olarak bilinirken, günümüzde yeraltı sularından kaynaklanan kitlesel bir halk sağlığı sorunudur: "
            "1. **Maruziyet Yolları:** "
            "- Özellikle Bangladeş, Hindistan ve Tayvan'da derin kuyu sularının doğal arsenik yataklarından süzülmesiyle **içme suları kontamine olur**. "
            "- Tarımsal pestisitler ve madencilik süreçleri de önemli kaynaklardır. "
            "2. **Toksik Biyokimyasal Mekanizma:** "
            "- Trivalan arsenik ($As^{3+}$), piruvat dehidrogenaz kompleksindeki **lipoik asit sülfhidril gruplarına bağlanarak Krebs döngüsünü durdurur**. "
            "- Pentavalan arsenik ($As^{5+}$) ise inorganik fosfatın ($PO_4^{3-}$) yerini alarak **mitokondriyal ATP sentezini bozar (kenetsizleştirir)**. "
            "3. **Karakteristik Doku Bulguları:** "
            "- **Cilt Belirteçleri:** Avuç içi ve ayak tabanlarında noktasal sert nasırlar (**palmar ve plantar hiperkeratoz**) ve "
            "gövdede 'çiseleyen yağmur damlaları' manzarası veren alacalı **hiperpigmentasyon**. "
            "4. **Karsinojenik Potansiyel (IARC Grup 1):** "
            "- Arsenik maruziyeti; **cilt kanserleri (skuamöz hücreli karsinom ve bazal hücreli karsinom)**, "
            "**akciğer kanseri** ve **mesane ürotelyal karsinomu** riskini katlar!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Arsenik Toksisitesinin Patolojik Spektrumu",
                ["Hedef Organ / Sistem", "Patolojik Lezyon", "Moleküler / Biyolojik Mekanizma"],
                [
                    ["Cilt (Kutanöz)", "Palmar-plantar hiperkeratoz ve hiperpigmentasyon", "Keratinosit proliferasyonu ve melanosit uyarımı"],
                    [
                        "Maligniteler",
                        {"text": "Cilt (SCC/BCC), akciğer ve mesane kanserleri", "isMasked": True, "hint": "Kronik arsenik maruziyetinin epitel dokularda tetiklediği primer organ kanserleri"},
                        "DNA tamir enzim inhibisyonu ve kromozomal kırıklar"
                    ],
                    ["Kardiyovasküler", "Siyah ayak hastalığı (Blackfoot disease)", "Periferik vaskülopati ve gangrenöz nekroz"],
                    ["Metabolik", "Mitokondriyal ATP tükenmesi", "Fosfat taklidi ve piruvat dehidrogenaz blokajı"]
                ]
            ),
            make_active_recall(
                "Yeraltı içme sularında yüksek arsenik bulunan bölgelerde yaşayan bireylerin avuç içlerinde ve ayak tabanlarında ortaya çıkan patognomonik cilt kalınlaşması lezyonuna ne ad verilir?",
                "Palmar ve plantar hiperkeratozdur.",
                "El ve ayak tabanı derisinde arsenik birikimiyle oluşan keratin birikintisi"
            )
        ]
    })

    # Slayt 48: Kadmiyum (Cd) Toksisitesi ve İtai-İtai Hastalığı
    slides.append({
        "id": "k1-26-s48",
        "title": "Kadmiyum (Cd) Toksisitesi ve İtai-İtai Hastalığı",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 48,
        "narrative": (
            "Kadmiyum ($Cd$), modern sanayide pillerden çevreye yayılan ve böbrek ile kemiği vuran tehlikeli bir metaldir: "
            "1. **Maruziyet:** Nikel-kadmiyum şarjlı pillerin üretimi ve atıkları, kadmiyumlu maden suları ile sulanan pirinç tarlaları "
            "ve en önemlisi **TÜTÜN DUMANI** (tütün yaprağı topraktaki kadmiyumu emer; sigara içenlerin kadmiyum düzeyi iki kat fazladır). "
            "2. **Renal Tübüler Hasar (İlk Hedef):** "
            "- Kadmiyum kanda metalotiyonin proteinine bağlanarak böbreğe gider. "
            "- Proksimal tübüllerde birikir ve tübül epitelini tahrip eder. "
            "- Sonuç: Glomerüller sağlam olduğu halde düşük molekül ağırlıklı proteinlerin idrarla kaybedildiği **tübüler proteinüri** "
            "(beta-2 mikroglobulinüri), hiperkalsiüri ve kalsiyum taşı taşları. "
            "3. **Kemik Patolojisi: İtai-İtai Hastalığı:** "
            "- Japonya'da kadmiyumlu çeltik tarlalarından beslenen menopoz sonrası kadınlarda görülmüştür ('itai-itai' = 'canım acıyor'). "
            "- Ağır kalsiyum kaybı ve D vitamini hidroksilasyon bozukluğu sonucu şiddetli **osteomalazi, osteoporoz ve patolojik kemik kırıkları** "
            "gelişir; hastalar şiddetli kemik ağrılarıyla kıvranır. "
            "4. **Kanser:** Akciğer kanseri riskini artırır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Kadmiyumun Böbrek ve Kemik Hasarı Ayrımı",
                "Renal Proksimal Tübül Hasarı",
                "Metalotiyonin-kadmiyum birikimi ile tübüler proteinüri, kalsiyum kaçağı ve nefrokalsinozis",
                "İskelet Sistemi (İtai-İtai)",
                "İdrarla kalsiyum kaybı ve osteoblastik defekt sonucu şiddetli osteomalazi, yaygın kemik ağrıları ve patolojik kırıklar"
            ),
            make_cloze(
                "Kadmiyum ile kontamine pirinç tüketimi sonucu böbrek tübüler hasarı, şiddetli osteomalazi ve kemik ağrılarıyla beliren tabloya İtai-İtai hastalığı denir.",
                "İtai-İtai",
                "Japonca canım acıyor anlamına gelen ve kadmiyum kaynaklı kemik erimesini tanımlayan hastalık"
            )
        ]
    })

    # Slayt 49: Checkpoint 5
    slides.append({
        "id": "k1-26-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Ağır Metal Patolojisi ve Toksikolojik Belirteçler",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 49,
        "narrative": (
            "Beşinci kontrol noktamızda ağır metallerin patolojik etkilerini ve tanısal belirteçlerini pekiştiriyoruz: "
            "1. **Ortak Kimya:** Sülfhidril (-SH) gruplarına bağlanarak enzimleri felç etme ve biyoakümülasyon. "
            "2. **Kurşun Hematolojisi:** ALA dehidrataz ve ferrokelataz blokajı; serbest protoporfirin artışı, mikrositer anemi ve "
            "rRNA agregasyonu ile eritrositlerde patognomonik bazofilik beneklenme. "
            "3. **Kurşun Doku İmzaları:** Çocuklarda metafizlerde radyoopak kurşun çizgileri; diş etinde kurşun sülfürden Burton çizgisi; "
            "erişkinde radial sinir motor felci ile düşük el (bilek düşmesi). "
            "4. **Cıva:** Metilcıva besin zincirinde zenginleşir; plasentayı aşarak fetal mikrosefali ve serebral palsi yapar (Minamata hastalığı). "
            "5. **Arsenik:** Yeraltı sularından; palmar/plantar hiperkeratoz, hiperpigmentasyon; cilt, akciğer ve mesane kanseri. "
            "6. **Kadmiyum:** Piller ve sigara dumanı; proksimal tübül hasarı ile proteinüri; ağır osteomalazi ve kemik ağrıları (İtai-İtai)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s49-1",
                "Kurşun zehirlenmesinde eritrositlerde ribozomal RNA agregasyonu sonucu periferik yaymada izlenen patognomonik morfolojik bulgu nedir?",
                "Eritrositlerde bazofilik beneklenmedir.",
                "Kırmızı kan hücreleri sitoplazmasında mavi tanecikli çökmeler",
                "Kurşun Anemisi"
            ),
            make_flashcard(
                "k1-26-fc-s49-2",
                "Erişkin kurşun zehirlenmesinde motor periferik nöropatinin en klasik klinik motor belirtisi nedir?",
                "Düşük el ve bilek düşmesidir.",
                "Radial motor lif felciyle karpal eklemin yukarı kaldırılamaması tablosu",
                "Nörotoksisite"
            ),
            make_flashcard(
                "k1-26-fc-s49-3",
                "Japonya'da cıva yüklü endüstriyel atıklarla kirlenmiş balıkların tüketilmesi sonucu fötal serebral hasar ve ataksi ile beliren toksik tablonun adı nedir?",
                "Minamata hastalığıdır.",
                "Metilcıvanın plasentayı aşarak anne karnındaki bebek beyninde yaptığı ağır toksisite tablosu",
                "Cıva Zehirlenmesi"
            )
        ],
        "interactiveElements": [
            make_table(
                "Dört Büyük Ağır Metalin Karşılaştırmalı Özet Matrisi",
                ["Metal", "Ana Maruziyet Kaynağı", "Patognomonik Klinik / Morfolojik Belirteç", "Primer Organ Hasarı"],
                [
                    ["Kurşun (Pb)", "Eski boya, su borusu, akü", "Bazofilik beneklenme, Burton çizgisi, düşük el", "SSS (çocuk), hematolojik, kemik"],
                    ["Cıva (Hg)", "Metilcıvalı kontamine balıklar", "Minamata hastalığı (fetal mikrosefali)", "Serebellum ve serebral korteks"],
                    [
                        "Arsenik (As)",
                        "Yeraltı içme suları, madenler",
                        {"text": "Palmar/plantar hiperkeratoz, hiperpigmentasyon", "isMasked": True, "hint": "El ayası ve ayak tabanında siğil benzeri kalınlaşmalar oluşturan metal"},
                        "Cilt, akciğer ve mesane karsinomu"
                    ],
                    ["Kadmiyum (Cd)", "Şarjlı piller, sigara dumanı", "İtai-İtai hastalığı (kemik ağrıları)", "Böbrek proksimal tübülü, osteomalazi"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi kronik kurşun zehirlenmesi tanısı konulan erişkin bir fabrika işçisinde periferik sinir sistemi tutulumuna bağlı olarak ortaya çıkan en klasik nörolojik motor defisittir?",
                {
                    "A": "Radial sinir felcine bağlı düşük el (bilek düşmesi)",
                    "B": "Yalnızca ayak tabanında yanıcı duyu kaybı",
                    "C": "Göz kapağında istemsiz tikler",
                    "D": "Fasiyal sinir felcine bağlı ağızda asimetri",
                    "E": "Dilde istemsiz fasikülasyonlar"
                },
                "A",
                {
                    "A": "Doğrudur; erişkinde kurşun en çok kullanılan motor siniri vurur, bu da radial sinir felci ve düşük eldir.",
                    "B": "Yanlış; kurşun duysal değil saf motordur.",
                    "C": "Yanlış; tik nörolojik kurşun hasarı değildir.",
                    "D": "Yanlış; periferik fasyal felç Bell felcidir.",
                    "E": "Yanlış; dil fasikülasyonu ALS bulgusudur."
                }
            )
        ]
    })

    # Slayt 50: Ağır Metal Tanısı ve Şelasyon Tedavisi
    slides.append({
        "id": "k1-26-s50",
        "title": "Ağır Metal Tanısı ve Şelasyon Tedavisi",
        "section": "Ağır Metal Toksisitesi",
        "slideNumber": 50,
        "narrative": (
            "Ağır metal zehirlenmelerinde klinik şüphe, erken laboratuvar doğrulaması ve acil toksikolojik müdahale hayat kurtarır: "
            "1. **Tanısal Doğrulama:** "
            "- **Kurşun:** Tam kanda **Venöz Kan Kurşun Düzeyi (BLL)** ölçülür (kapiller parmak ucu kanı cilt kontaminasyonu nedeniyle yanıltıcı olabilir). "
            "Çocuklarda 3.5-5 µg/dL üzeri değerler bile gelişimsel risk kabul edilir. "
            "- **Cıva ve Arsenik:** Cıva için tam kan ve idrar; arsenik için idrar arsenik düzeyi ve kronik maruziyette saç/tırnak analizleri. "
            "2. **Şelasyon Tedavisi (Chelation Therapy):** "
            "- Ağır metalleri bağlayarak suda çözünür kompleksler oluşturan ve böbrekten idrarla atılmalarını sağlayan moleküllerdir: "
            "  * **Kalsiyum Disodyum EDTA ($CaNa_2EDTA$):** Kemik ve yumuşak dokudaki kurşunu kuvvetle şelatlar. "
            "  * **DMSA (Süksimer):** Oral yoldan kullanılabilen, özellikle çocukluk çağı kurşun zehirlenmesinde tercih edilen şelatördür. "
            "  * **Dimerkaprol (BAL - British Anti-Lewisite):** Arsenik ve cıva zehirlenmesinde acil intramusküler şelatördür. "
            "3. **İlk ve En Hayati İlke:** Şelasyondan önce hastayı **maruziyet kaynağından derhal uzaklaştırmak** esastır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Ağır Metallerde Şelasyon Tedavisi Protokolü",
                ["Ağır Metal", "Birinci Seçenek Şelatör Ajan", "Uygulama Yolu ve Etki Mekanizması"],
                [
                    ["Kurşun (Çocuk)", "DMSA (Süksimer)", "Oral şelatör; kurşunla halka oluşturup idrarla atılım"],
                    ["Kurşun (Ağır / Ensefalopati)", "CaNa2EDTA + Dimerkaprol (BAL)", "Damar içi ve kas içi acil parenteral şelasyon kombinasyonu"],
                    [
                        "Arsenik ve İnorganik Cıva",
                        {"text": "Dimerkaprol (BAL) veya DMSA", "isMasked": True, "hint": "Sülfhidril grupları içeren ve arseniği enzimlerden söküp atan antidot"},
                        "Doku enzimlerini metal bağından kurtarma"
                    ]
                ]
            ),
            make_active_recall(
                "Ağır metal zehirlenmelerinde toksik metalleri kovalent halka içine hapsederek suda çözünür hale getiren ve idrarla atılımını sağlayan kimyasal bileşikler sınıfına ne ad verilir?",
                "Şelatör ajanlardır (şelasyon tedavisi).",
                "Metal iyonlarını kıskaç gibi bağlayarak vücuttan uzaklaştıran antidot molekülleri"
            )
        ]
    })

    return slides
