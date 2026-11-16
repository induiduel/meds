# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 5: Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri (Slayt 41 - 50)
Checkpoint 5: Slayt 49
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # Slayt 41: Anne Sütünün Mucizesi ve Yaşlara Göre Karşılama Oranları
    slides.append({
        "id": "k1-22-s41",
        "title": "Anne Sütünün Mucizesi ve Yaşlara Göre Karşılama Oranları",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 41,
        "narrative": (
            "Anne sütü, insan yavrusunun biyolojik, nörolojik ve immünolojik ihtiyaçlarına göre miligram düzeyinde "
            "tasarlanmış eşsiz ve dinamik bir sıvıdır. "
            "Her zaman hazır, taze, steril, ideal vücut ısısında ve ekonomik olarak maliyetsizdir. "
            "**Yaş Dönemlerine Göre Bebeğin Besin İhtiyacını Karşılama Oranı:** "
            "- **İlk 6 Ayda:** Bebeğin enerji, sıvı, protein, yağ ve vitamin ihtiyacının **tam %100'ünü tek başına** karşılar. "
            "- **6 - 12 Ay Arasında:** Tamamlayıcı gıdalar başlansa bile günlük gereksinimin **yaklaşık %50'sini** karşılamaya devam eder. "
            "- **12 - 24 Ay (İkinci Yaşta):** Bebeğin besin ve enerji ihtiyacının **yaklaşık %30'unu** ve kritik immünolojik desteği sağlamayı sürdürür. "
            "Bu nedenle DSÖ, emzirmenin tamamlayıcı besinlerle birlikte en az 2 yaşına kadar sürdürülmesini altın standart önerir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütü ilk 6 ayda bebeğin tüm besin gereksiniminin yüzde yüzünü tek başına eksiksiz karşılar.",
                "yüzde yüzünü",
                "İlk yarım yılda ihtiyacın tamamını karşılama oranı"
            ),
            make_table(
                "Anne Sütünün Çocukluk Dönemlerine Göre Besin Karşılama Oranları",
                ["Yaşam Evresi", "Anne Sütünün İhtiyacı Karşılama Oranı", "Gereken Beslenme Rejimi"],
                [
                    ["İlk 6 Ay (0 - 6 Ay)", "Tam %100", "Sadece Anne Sütü (Su dahi verilmez)"],
                    [
                        "İkinci 6 Ay (6 - 12 Ay)",
                        {"text": "Yaklaşık %50", "isMasked": True, "hint": "Yarı yarıya devam eden anne sütü payı"},
                        "Anne sütü + Güvenli tamamlayıcı besinler"
                    ],
                    ["İkinci Yaş (12 - 24 Ay)", "Yaklaşık %30", "Aile sofrası + Anne sütü devamı"]
                ]
            ),
            make_micro_quiz(
                "Anne sütünün çocukluk çağındaki gereksinimleri karşılama kapasitesi ile ilgili hangisi doğrudur?",
                {
                    "A": "İlk 3 aydan sonra anne sütünün hiçbir besleyici değeri kalmaz",
                    "B": "İlk 6 ayda ihtiyacın %100'ünü, 6-12 ayda %50'sini, ikinci yılda %30'unu karşılar",
                    "C": "6. aydan sonra anne sütü verilmesi bebeğin ek gıda almasını engellediği için derhal kesilmelidir",
                    "D": "İlk 6 ayda anne sütü sadece su ihtiyacını karşılar, kalori için mama şarttır",
                    "E": "İkinci yılda anne sütü zararlı hale gelir ve meme kanserini tetikler"
                },
                "B",
                "Doğru cevap B'dir: Anne sütü ilk 6 ayda %100, ikinci 6 ayda %50 ve ikinci yaşta %30 oranında gereksinimi karşılayarak emzirmenin 2 yaşına kadar sürmesini rasyonel kılar. Diğer seçenekler hatalı mitlerdir."
            )
        ]
    })

    # Slayt 42: Sekretuvar İmmünglobulin A (sIgA): Mukozal Zırh
    slides.append({
        "id": "k1-22-s42",
        "title": "Sekretuvar İmmünglobulin A (sIgA): Mukozal Zırh",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 42,
        "narrative": (
            "Anne sütünün en baskın immünoglobulini **Sekretuvar IgA'dır (sIgA)**. "
            "Salgısal komponent (secretory component) ile donatılmış iki IgA molekülünün birleşmesinden oluşan bu dimerik yapı, "
            "mide asidine ve bağırsaktaki proteolitik enzimlere olağanüstü dirençlidir; parçalanmadan lümende kalır. "
            "**sIgA'nın İmmünolojik Mekanizmaları:** "
            "1. **Mukozal Boya (Antiseptik Zırh):** Bağırsak epitel yüzeyini koruyucu bir tabaka gibi boyar; "
            "rotavirüs, E. coli, Shigella ve Salmonella gibi patojenlerin epitel reseptörlerine tutunmasını (adezyonunu) sterik olarak engeller. "
            "2. **İnflamasyonsuz Temizlik:** Komplemanı aktive etmez; bu sayede bağırsak dokusunda tahrip edici inflamasyon yaratmadan patojenleri aglutine eder ve dışkıyla atar. "
            "3. **Entero-Mammarian Yol:** Anne solunum veya sindirim yolunda hangi mikropla karşılaşırsa, "
            "peyer plaklarındaki B lenfositler meme bezine göç ederek doğrudan o mikropa özgü sIgA üretir ve süte salgılar!"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki sekretuvar IgA bağırsak mukozasını kaplayarak patojen bakterilerin epitele tutunmasını mekanik olarak bloke eder.",
                "sekretuvar IgA",
                "Mukozal salgılarda bulunan dimerik koruyucu antikor"
            ),
            make_causal_chain(
                "Entero-Mammarian İmmün Göç ve Bebeği Koruma Zinciri",
                [
                    "1. Maternal Temas: Anne çevredeki patojen bir mikropla solunum veya sindirim yoluyla karşılaşır.",
                    "2. Peyer Plak Aktivasyonu: Bağırsak lenfoid dokusunda patojene spesifik B lenfosit klonları uyarılır.",
                    "3. Meme Bezine Göç: B lenfositler kan yoluyla meme dokusuna ulaşıp plazma hücresine dönüşür.",
                    "4. Hedefe Özgü Salgı: Bebeğe aktarılan sütte o spesifik mikroba karşı yoğun sIgA yer alır."
                ]
            ),
            make_active_recall(
                "Sekretuvar IgA'nın (sIgA) bebek bağırsağında proteolitik enzimler ve asit tarafından parçalanmasını engelleyen yapısal parçası nedir?",
                "Meme epiteli tarafından eklenen 'Salgısal Parça' (Secretory Component) polipeptididir.",
                "Dimerik antikorun enzimatik direncini sağlayan salgısal komponent"
            )
        ]
    })

    # Slayt 43: Laktoferrin ve Lizozim: Antibakteriyel İkili
    slides.append({
        "id": "k1-22-s43",
        "title": "Laktoferrin ve Lizozim: Antibakteriyel İkili",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 43,
        "narrative": (
            "Anne sütünde bulunan antimikrobiyal proteinlerin başında **Laktoferrin** ve **Lizozim** gelir: "
            "- **Laktoferrin (Demir Bağlayıcı Protein):** "
            "Anne sütü whey proteinlerinin büyük kısmını oluşturur. "
            "Serbest demir iyonlarını (Fe3+) olağanüstü yüksek bir afiniteyle bağlar. "
            "E. coli, Pseudomonas, Salmonella ve Candida gibi patojen mikroorganizmalar çoğalabilmek için ortamda serbest demire muhtaçtır. "
            "Laktoferrin ortamdaki tüm demiri kaparak bakterileri 'demir açlığına' mahkum eder ve çoğalmalarını durdurur (**bakteriyostatik etki**). "
            "Ayrıca demiri bağlayarak bebeğin bağırsağından emilimini %50-60'a fırlatır. "
            "- **Lizozim:** "
            "Anne sütünde inek sütünden **300 kat daha fazla** bulunur. "
            "Bakteri hücre duvarındaki peptidoglikan tabakasını enzimatik olarak parçalayarak bakterileri lizise uğratır (**bakterisidal etki**). "
            "Laktoferrin ve lizozim sinerjik çalışarak bebek bağırsağını steril tutar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki laktoferrin ortamdaki serbest demiri bağlayarak patojen bakterilerin çoğalmasını bakteriyostatik olarak durdurur.",
                "laktoferrin",
                "Demir şelatlayıcı antimikrobiyal whey proteini"
            ),
            make_before_after(
                "Laktoferrin ve Lizozimin Antimikrobiyal Etki Mekanizmaları",
                "Laktoferrin Etkisi (Bakteriyostatik)",
                "Serbest demiri kapar; patojen bakterileri aç bırakarak üremelerini ve biyofilm kurmalarını bloke eder.",
                "Lizozim Etkisi (Bakterisidal)",
                "Bakteri hücre duvarındaki peptidoglikan bağlarını hidrolize ederek hücre zarını patlatır ve eritir.",
                "Mikrobu demir açlığıyla durduran protein ile hücre duvarını yıkan enzimin işbirliği"
            ),
            make_micro_quiz(
                "Anne sütündeki laktoferrinin fizyolojik ve antimikrobiyal fonksiyonları ile ilgili hangisi yanlıştır?",
                {
                    "A": "Serbest demir iyonlarını güçlü şekilde bağlayarak bakterilerin demire ulaşmasını engeller",
                    "B": "E. coli ve diğer enterik bakterilerin çoğalmasını bakteriyostatik olarak baskılar",
                    "C": "Bağladığı demiri bebek enterositlerine aktararak demir biyoyararlanımını artırır",
                    "D": "Yalnızca inek sütünde bulunur, insan sütünde kesinlikle laktoferrin yoktur",
                    "E": "Antiviral, antifungal ve antiinflamatuar etkilere sahiptir"
                },
                "D",
                "Doğru cevap D'dir: Laktoferrin anne sütünün en karakteristik ve en bol whey proteinidir; inek sütünde ise miktarı son derece azdır. A, B, C ve E seçenekleri laktoferrinin temel bilimsel özellikleridir."
            )
        ]
    })

    # Slayt 44: Anne Sütü Oligosakkaritleri (HMO): Prebiyotik ve Tuzak Reseptör
    slides.append({
        "id": "k1-22-s44",
        "title": "Anne Sütü Oligosakkaritleri (HMO): Prebiyotik ve Tuzak Reseptör",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 44,
        "narrative": (
            "Anne sütünde laktoz ve yağdan sonra konsantrasyon olarak üçüncü sırada gelen en zengin katı madde "
            "**Anne Sütü Oligosakkaritleridir (Human Milk Oligosaccharides - HMO)**. "
            "Anne sütünde 200'den fazla farklı HMO türü bulunur (en meşhuru 2'-fukozillaktoz - 2'-FL). "
            "Bebek sindirim enzimleri HMO'ları parçalayamaz; bu şekerler kalori vermez. Peki neden bu kadar boldur? "
            "**HMO'ların 2 Devrimsel Görevi:** "
            "1. **Prebiyotik Fonksiyon:** Kolona sağlam ulaşan HMO'lar, yalnızca yararlı *Bifidobacterium infantis* bakterileri "
            "tarafından fermente edilir. Yararlı mikrobiyotayı besler, asidik ortam kurar ve patojenleri kovar. "
            "2. **Tuzak (Decoy) Reseptör Görevi:** HMO'ların moleküler yapısı, bağırsak epitel hücrelerindeki reseptör glikoproteinlerine "
            "tıpatıp benzer! Patojen bakteri, virüs ve toksinler epitele tutunacaklarını sanarak lümendeki HMO'lara bağlanırlar. "
            "Böylece epitele temas edemeden dışkıyla vücuttan süpürülüp atılırlar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütü oligosakkaritleri bağırsak epitel reseptörlerini taklit ederek patojenleri kendine bağlayan tuzak reseptör görevi görür.",
                "tuzak reseptör",
                "Patojenleri epitele yapışmaktan alıkoyan yalancı bağlanma şaşırtmacası"
            ),
            make_causal_chain(
                "HMO'ların Aldatıcı Tuzak Mekanizması ile Patojen Eliminasyonu",
                [
                    "1. Lümen Varlığı: Sindirilmeyen HMO molekülleri bağırsak lümeninde serbestçe dolaşır.",
                    "2. Yanıltıcı Benzerlik: Moleküler yüzeyi enterosit membran glikanlarıyla tıpatıp aynıdır.",
                    "3. Patojen Bağlanması: Virüs veya bakteri epitel yerine HMO şekerlerine kilitlenir.",
                    "4. Zararsız Dışkılama: Patojen epitele invaze olamadan süt şekerleriyle feçesle atılır."
                ]
            ),
            make_active_recall(
                "Anne sütü oligosakkaritlerinin (HMO) bebek tarafından sindirilip kaloriye dönüştürülememesine rağmen anne sütünde bu denli bol bulunmasının temel amacı nedir?",
                "Yararlı Bifidobakterileri besleyen bir prebiyotik olması ve patojen mikroorganizmaların bağırsak hücrelerine yapışmasını engelleyen tuzak (decoy) reseptör işlevi görmesidir.",
                "Prebiyotik mikrobiyota besini ve tuzak reseptör fonksiyonu"
            )
        ]
    })

    # Slayt 45: Anne Sütündeki Canlı Hücreler: Lökositler ve Kök Hücreler
    slides.append({
        "id": "k1-22-s45",
        "title": "Anne Sütündeki Canlı Hücreler: Lökositler ve Kök Hücreler",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 45,
        "narrative": (
            "Anne sütü cansız bir sıvı değil, **canlı bir doku naklidir**! "
            "Bir mililitre anne sütünde milyonlarca canlı konak hücresi bulunur (özellikle kolostrumda ml'de 1-5 milyon hücre): "
            "- **Makrofajlar (%80):** Sütteki lökositlerin ezici çoğunluğunu oluşturur. "
            "Fagositoz yaparak mikropları yok eder, sIgA, lizozim ve kompleman salgılar. "
            "- **Nötrofiller ve Lenfositler (%10-20):** T lenfositler (CD4+ ve CD8+) ve B lenfositler bebeğin bağırsağından "
            "geçerek mezenterik lenf nodlarına yerleşir ve bebeğin hücresel bağışıklığını eğitir. "
            "- **Kök Hücreler (Stem Cells):** Anne sütünde pluripotent benzeri canlı kök hücrelerin bulunduğu kanıtlanmıştır! "
            "Bu kök hücreler bebek bağırsağını aşarak kan dolaşımına karışır; beyin, karaciğer ve pankreas gibi organlara "
            "göç ederek doku rejenerasyonuna ve organ olgunlaşmasına doğrudan katılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki lökositlerin yaklaşık yüzde seksenini fagositoz yapan canlı makrofajlar oluşturur.",
                "yüzde seksenini",
                "Anne sütü akyuvarları içindeki makrofaj baskınlık oranı"
            ),
            make_table(
                "Anne Sütündeki Canlı Hücresel Elemanlar ve Fonksiyonları",
                ["Hücre Tipi", "Sütteki Oranı / Varlığı", "Temel Biyolojik Görevi"],
                [
                    ["Makrofajlar", "Lökositlerin ~%80'i", "Lümende fagositoz, antikor ve lizozim üretimi"],
                    [
                        "Kök Hücreler",
                        {"text": "Pluripotent benzeri canlı hücreler", "isMasked": True, "hint": "Farklı doku elemanlarına dönüşme yeteneğinde öncül biyolojik yapılar"},
                        "Bebek organlarına göçerek doku matürasyonu ve rejenerasyonu"
                    ],
                    ["T Lenfositler", "%10 - 15", "Hücresel bağışıklık transferi ve sitokin üretimi"],
                    ["B Lenfositler", "%5", "Lokal mukozal antikor sentezi"]
                ]
            ),
            make_micro_quiz(
                "Anne sütündeki canlı hücre içeriği ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Kolostrumda mililitrede milyonlarca canlı hücre bulunur",
                    "B": "Sütteki en baskın akyuvar tipi fagositoz yapan makrofajlardır",
                    "C": "Anne sütündeki lökositlerin tamamı ölüdür ve hiçbir biyolojik aktivite göstermez",
                    "D": "Anne sütündeki kök hücreler bebeğin organlarına göç ederek gelişime katılır",
                    "E": "T ve B lenfositler bebeğin bağışıklık sisteminin olgunlaşmasını destekler"
                },
                "C",
                "Doğru cevap C'dir: Anne sütündeki hücreler kesinlikle ölü değildir; hareket edebilen, fagositoz yapabilen ve sitokin salgılayan son derece aktif canlı hücrelerdir. Bu nedenle anne sütü canlı bir biyolojik dokudur."
            )
        ]
    })

    # Slayt 46: Anne Sütünün Enzimatik Gücü: BSSL ve Sindirim Kolaylığı
    slides.append({
        "id": "k1-22-s46",
        "title": "Anne Sütünün Enzimatik Gücü: BSSL ve Sindirim Kolaylığı",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 46,
        "narrative": (
            "Anne sütü, bebeğin sindirim sistemi enzimlerinin yetersizliğini kendi içinde taşıdığı **aktif sindirim enzimleri** ile telafi eder: "
            "- **Safra Tuzu Bağımlı Lipaz (BSSL - Bile Salt-Stimulated Lipase):** "
            "Anne sütünde bol miktarda bulunan bu enzim midede inaktiftir; süt duodenuma geçip safra tuzlarıyla temas ettiği anda "
            "muazzam bir hızla aktifleşir! "
            "Trigliseritleri monogliserit ve serbest yağ asitlerine yıkar. "
            "Böylece bebek pankreası henüz yeterli lipaz üretemezken bile anne sütü kendi kendini sindirerek %95 emilim sağlar. "
            "- **Meme Sütü Amilazı:** "
            "Tükürük ve pankreas amilazından farklı olarak glikojen ve polisakkaritleri sindirmeye devam eder. "
            "Bu aktif enzimler sayesinde anne sütü alan bebeklerde hazımsızlık, gaz sancısı veya yağlı dışkılama (steatore) görülmez."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütünde bulunan safra tuzu bağımlı lipaz duodenuma geçtiğinde aktifleşerek sütün kendi yağlarını sindirmesini sağlar.",
                "safra tuzu bağımlı lipaz",
                "Bile tuzlarıyla uyarılan anne sütü lipolitik enzimi"
            ),
            make_before_after(
                "Anne Sütü Sindirimi ile İnek Sütü Sindirimi Kıyası",
                "Anne Sütü Sindirim Dinamiği",
                "İçerdiği aktif BSSL enzimi sayesinde yağlar bağırsakta hızla erir; mideyi 1.5 saatte terk eder, hazımsızlık yapmaz.",
                "İnek Sütü Sindirim Dinamiği",
                "Aktif lipaz içermez; kazein midede taş gibi sert pıhtı yapar, mide 4 saatte boşalmaz, yağlar feçesle atılır.",
                "Kendi kendini sindiren enzimatik anne sütü ile mideyi tıkayan kazeinli inek sütü ayrımı"
            ),
            make_active_recall(
                "Bebek pankreasının lipaz üretimi yetersiz olmasına rağmen anne sütü alan bebeklerin yağları mükemmel sindirebilmesinin nedeni nedir?",
                "Anne sütünün kendi içinde taşıdığı Safra Tuzu Bağımlı Lipaz (BSSL) enziminin duodenal safrayla birleşerek yağları kendiliğinden sindirmesidir.",
                "BSSL enziminin otonom lipolitik aktivitesi"
            )
        ]
    })

    # Slayt 47: Büyüme Faktörleri ve Hormonlar: Epidermal Büyüme Faktörü (EGF)
    slides.append({
        "id": "k1-22-s47",
        "title": "Büyüme Faktörleri ve Hormonlar: Epidermal Büyüme Faktörü (EGF)",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 47,
        "narrative": (
            "Anne sütü, bebeğin bağırsak mukozasını ve endokrin sistemini olgunlaştıran güçlü biyoaktif faktörlerle doludur: "
            "- **Epidermal Büyüme Faktörü (EGF):** "
            "Kolostrumda ve anne sütünde yüksek konsantrasyonda bulunur. "
            "Bağırsak epitel hücrelerinin bölünmesini ve villusların uzamasını tetikler; bağırsak geçirgenliğini (tight junction) kapatır. "
            "Bu sayede prematüre bebeklerde ölümcül bir bağırsak nekrozu olan **Nekrotizan Enterokolit (NEK)** gelişimini engeller. "
            "- **Hormonlar (İnsülin, Leptin, Adiponektin, Ghrelin):** "
            "Anne sütü iştahı ve tokluk merkezini (hipotalamus) düzenleyen leptin ve adiponektin hormonları içerir. "
            "Bebek tokluk hissettiğinde memeyi bırakır; bu biyolojik geri bildirim, çocuğun ömür boyu aşırı yemeyi öğrenmesini engelleyerek "
            "erişkin obezitesine karşı en kuvvetli zırhı örer."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki epidermal büyüme faktörü bağırsak epitel matürasyonunu hızlandırarak nekrotizan enterokolit tablosunu önler.",
                "nekrotizan enterokolit",
                "Prematüre bebeklerin ölümcül iskemik gangrenöz bağırsak patolojisi"
            ),
            make_causal_chain(
                "EGF Aracılı İntestinal Koruma Mekanizması",
                [
                    "1. Kolostrum Alımı: Bebek ilk saatlerde yüksek konsantrasyonda EGF içeren kolostrumu emer.",
                    "2. Epitel Reseptör Uyarımı: Enterosit membranındaki EGF reseptörleri tirozin kinazı aktive eder.",
                    "3. Sıkı Bağlantıların Kapanması: Hücreler arası 'tight junction' proteinleri kenetlenerek geçirgenlik düşer.",
                    "4. NEK Koruması: Patojen bakteriler mukozayı delemeyerek nekrotizan enterokolit engellenir."
                ]
            ),
            make_active_recall(
                "Anne sütünde bulunan leptin ve adiponektin gibi tokluk hormonlarının çocuğun gelecekteki metabolik sağlığına en büyük katkısı nedir?",
                "Hipotalamik iştah ve tokluk merkezini fizyolojik programlayarak bebeğin kendi doygunluğunu kontrol etmesini sağlaması ve ileride obezite gelişimini engellemesidir.",
                "İştah regülasyonu ve obezite önleme etkisi"
            )
        ]
    })

    # Slayt 48: Anne Sütünün Bebek Sağlığına Uzun Dönemli Koruyucu Etkileri
    slides.append({
        "id": "k1-22-s48",
        "title": "Anne Sütünün Bebek Sağlığına Uzun Dönemli Koruyucu Etkileri",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 48,
        "narrative": (
            "Anne sütü ile beslenmenin yararları sadece bebeklik dönemiyle sınırlı kalmaz; bireyin tüm yaşamına yayılır: "
            "1. **Enfeksiyon Koruması:** İlk 6 ay sadece anne sütü alan bebeklerde ilk 2 yılda **akut otitis media (orta kulak iltihabı) riski %43 azalır**! "
            "Gastroenterit ve pnömoni sıklığı dramatik şekilde düşer. "
            "2. **Kronik Hastalık ve Obezite Kalkanı:** Uzun süreli emzirme, çocukluk ve erişkinlik çağı obezitesine, "
            "Tip 1 ve Tip 2 Diabetes Mellitusa, Çölyak hastalığına ve inflamatuar bağırsak hastalıklarına (Crohn/ÜK) karşı kanıtlanmış en güçlü koruyucudur. "
            "3. **Ağız, Diş ve Çene Sağlığı:** Memeden emme çene kemiklerini çalıştırarak maloklüzyonları önler; 12 aya kadar diş çürüklerinden korur. "
            "4. **Bilişsel Kapasite (IQ):** Emzirme süresi arttıkça çocukluk ve erişkinlik IQ test skorları ve akademik başarı anlamlı derecede yüksek bulunur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İlk 6 ay sadece anne sütüyle beslenen bebeklerde ilk iki yılda orta kulak iltihabı görülme riski yüzde kırk üç azalır.",
                "yüzde kırk üç",
                "Akut otitis media sıklığında sağlanan kanıtlanmış gerileme payı"
            ),
            make_table(
                "Anne Sütünün Akut ve Kronik Hastalıklara Karşı Kanıtlanmış Koruyuculuğu",
                ["Hastalık Tablosu", "Anne Sütü ile Sağlanan Koruma Düzeyi", "Koruyucu Biyolojik Mekanizma"],
                [
                    ["Akut Otitis Media (AOM)", "%43 azalma", "sIgA ile nazofarenks patojen kolonizasyonunun kırılması"],
                    [
                        "Çocukluk ve Erişkin Obezitesi",
                        {"text": "En güçlü koruyucu faktör", "isMasked": True, "hint": "Aşırı kilo ve yağlanmaya karşı en kuvvetli kalkan"},
                        "Düşük protein, leptin tokluk kontrolü ve metabolik programlama"
                    ],
                    ["Gastroenterit ve İshal", "%60 - 80 azalma", "sIgA, laktoferrin ve HMO tuzak reseptörleri"],
                    ["Nekrotizan Enterokolit (NEK)", "%75 azalma", "EGF ile bağırsak mukozal bariyerinin kapatılması"]
                ]
            ),
            make_micro_quiz(
                "Anne sütünün bebek sağlığı üzerindeki uzun dönemli faydaları ile ilgili hangisi yanlıştır?",
                {
                    "A": "İlk iki yılda akut otitis media (orta kulak iltihabı) riskini %43 oranında azaltır",
                    "B": "Uzun süreli emzirme erişkin obezitesi ve tip 2 diyabete karşı en önemli koruyucu faktördür",
                    "C": "Emzirilen bebeklerin zeka testleri ve okul başarıları formül mama alanlara göre daha yüksektir",
                    "D": "Memeden emme çene-diş kapanma bozukluklarını (maloklüzyon) belirgin azaltır",
                    "E": "Anne sütü alan bebeklerde 20 yaşına gelindiğinde tüm bağışıklık fonksiyonları sıfırlanır"
                },
                "E",
                "Doğru cevap E'dir: Anne sütünün immünolojik ve metabolik programlama etkileri ömür boyu kalıcıdır ve bağışıklığı sıfırlamaz; aksine erişkin dönemde astım, alerji ve otoimmün hastalıklara karşı direnç sağlar."
            )
        ]
    })

    # Slayt 49: [TEKRAR SAYFASI - CHECKPOINT 5] Anne Sütü İmmünolojisi ve Koruyucu Etmenler
    slides.append({
        "id": "k1-22-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Anne Sütü İmmünolojisi ve Koruyucu Etmenler",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 49,
        "narrative": (
            "Bu beşinci checkpoint sayfasında, anne sütünün biyoaktif ve immünolojik üstünlüklerini "
            "özetleyen temel mekanizmaları kilitliyoruz: "
            "1. **Karşılama Oranı:** İlk 6 ay %100, 6-12 ay %50, 12-24 ay %30; 2 yaşına kadar emzirme esastır. "
            "2. **Sekretuvar IgA (sIgA):** Dimerik yapısıyla asitte parçalanmaz; bağırsak epitelini zırh gibi boyar. "
            "3. **Laktoferrin:** Serbest demiri bağlayarak bakterileri aç bırakır (bakteriyostatik) ve demir emilimini artırır. "
            "4. **Lizozim ve BSSL:** Lizozim bakteri çeperini eritir (bakterisidal); BSSL sütün yağlarını kendiliğinden sindirir. "
            "5. **HMO:** Prebiyotiktir ve patojenleri kendine bağlayan tuzak (decoy) reseptör görevi görür. "
            "6. **Canlı Doku:** Lökositlerin %80'i makrofajdır; ayrıca kök hücreler içerir; otitis media riskini %43 azaltır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "k1-22-fc-13",
                "Anne sütünde bulunan, bebek bağırsak mukozasını kaplayarak patojen mikroorganizmaların tutunmasını engelleyen majör antikor sınıfı nedir?",
                "Sekretuvar İmmünglobulin A (sIgA)",
                "Mukozal bariyerin dimerik salgısal antikor kalkanı",
                "İmmünoloji"
            ),
            make_flashcard(
                "k1-22-fc-14",
                "Anne sütünde yüksek konsantrasyonda bulunan, serbest demiri bağlayarak bakterilerin çoğalmasını durduran (bakteriyostatik) koruyucu glikoprotein nedir?",
                "Laktoferrin",
                "Demir yakalayıcı antimikrobiyal süt proteini",
                "İmmünoloji"
            ),
            make_flashcard(
                "k1-22-fc-15",
                "Anne sütünde sindirilemeyen ancak yararlı Bifidobakterilerin üremesini sağlayan ve patojenlerin hücre reseptörlerine bağlanmasını taklit ederek engelleyen şeker bileşikleri nelerdir?",
                "Anne sütü oligosakkaritleri (HMO)",
                "Prebiyotik ve tuzak reseptör görevi gören kompleks şekerler",
                "İmmünoloji"
            )
        ]
    })

    # Slayt 50: Bölüm Özeti: İmmünolojik Biyolojiden Sütün Evrelerine Geçiş
    slides.append({
        "id": "k1-22-s50",
        "title": "Bölüm Özeti: İmmünolojik Biyolojiden Sütün Evrelerine Geçiş",
        "section": "Anne Sütünün Eşsiz Biyolojisi ve İmmünolojik Üstünlükleri",
        "slideNumber": 50,
        "narrative": (
            "Anne sütünün immünolojik zırhını ve biyoaktif gücünü kavradıktan sonra, bu eşsiz sıvının "
            "zaman içindeki dinamik değişimini anlamak gerekir. "
            "Anne sütü doğumdan sütten kesilene kadar aynı bileşimde kalmaz; "
            "ilk günlerdeki sarı-koyu kolostrumdan olgun süte, tek bir emzirme seansının başındaki ön sütten sonundaki yağlı son süte kadar "
            "dakika dakika bebeğin ihtiyaçlarına göre formül değiştirir. "
            "Ayrıca emzirme yalnızca bebeği değil, anneyi de meme ve over kanserinden, postpartum kanamadan ve depresyondan korur. "
            "Altıncı bölümümüzde, kolostrum, geçiş sütü, olgun süt, ön/son süt ayrımı ve emzirmenin anne sağlığına mucizevi faydaları incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütü durağan bir formül olmayıp doğum sonrası günlere ve emzirme seansının dakikalarına göre dinamik olarak değişir.",
                "dinamik olarak",
                "Zamana ve ihtiyaca göre sürekli uyum sağlayan değişken yapı"
            ),
            make_causal_chain(
                "Emzirmenin Anne ve Bebek İkilisindeki Dinamik Etkileşimi",
                [
                    "1. Doğum: İlk 5 gün protein ve sIgA zengini kolostrum salgılanarak bebek korunur.",
                    "2. Günlük Ritim: Ön süt susuzluğu giderirken, yağlı son süt doygunluk sağlar.",
                    "3. Anne Koruması: Emzirme uterusu kasarak kanamayı durdurur; over ve meme kanserini azaltır.",
                    "4. Çift Taraflı Şifa: Hem bebek ideal beslenir hem de anne metabolik ve ruhsal olarak hızla toparlanır."
                ]
            ),
            make_active_recall(
                "Anne sütünün tek bir emzirme seansı içinde bile kompozisyon değiştirmesinin (ön süt - son süt) en temel fizyolojik amacı nedir?",
                "Ön sütün yüksek su ve laktoz ile bebeğin susuzluğunu gidermesi; emzirmenin sonuna doğru 4-5 kat artan yağlı son sütün ise yüksek kalori ve tokluk hissi sağlamasıdır.",
                "Ön süt susuzluk ve son süt doygunluk mekanizması"
            )
        ]
    })

    return slides
