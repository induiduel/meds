# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 9: Diyet Kanserojenleri, Vitamin Eksiklikleri ve Pediatrik Patoloji (Slayt 81-90)
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

def get_section_9_slides():
    slides = []

    # Slayt 81: Diyet, Yağ Tüketimi ve Ateroskleroz
    slides.append({
        "id": "k1-26-s81",
        "title": "Diyet, Yağ Tüketimi ve Ateroskleroz",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 81,
        "narrative": (
            "Diyet bileşimi, kardiyovasküler ateroskleroz ve iskemik kalp hastalığı riskini doğrudan modüle eder: "
            "1. **Doymuş Yağlar ve Kolesterol:** "
            "- Kırmızı et, tereyağı ve tam yağlı süt ürünlerindeki doymuş yağ asitleri karaciğerde LDL reseptör ekspresyonunu baskılar. "
            "- Dolaşımdaki LDL kolesterol temizlenemez; plazma LDL'si yükselir ve koroner ateroskleroz hızlanır. "
            "2. **Trans Yağ Asitleri (En Aterojenik Yağ):** "
            "- Bitkisel sıvı yağların endüstriyel olarak hidrojenlenmesiyle (margarinler, fast-food kızartmalar) üretilir. "
            "- Çifte felaket yaratır: **LDL'yi artırırken, koruyucu HDL kolesterolü düşürür**; endotel disfonksiyonunu ve sistemik inflamasyonu tetikler. "
            "3. **Doymamış Yağ Asitleri ve Koruyucu Etki:** "
            "- Tekli doymamış yağlar (Zeytinyağı - Akdeniz diyeti) ve çoklu doymamış omega-3 yağ asitleri (Balık yağı - EPA ve DHA) "
            "trigliseridleri düşürür, trombosit agregasyonunu baskılar ve kardiyovasküler mortaliteyi anlamlı derecede azaltır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Diyetteki Yağ Türleri ve Kardiyovasküler Etkileri",
                ["Yağ Asidi Sınıfı", "Besinsel Kaynaklar", "Lipid Profili ve Ateroskleroz Riski"],
                [
                    ["Doymuş Yağlar", "Kırmızı et, domuz yağı, tereyağı", "LDL kolesterolü artırır, aterosklerozu hızlandırır"],
                    [
                        "Endüstriyel Trans Yağlar",
                        "Margarin, fırıncılık ürünleri, kızartmalar",
                        {"text": "LDL'yi fırlatırken koruyucu HDL'yi düşürür (en tehlikeli)", "isMasked": True, "hint": "Kardiyovasküler riski çift yönlü bozan suni hidrojenlenmiş yağ türü"}
                    ],
                    ["Tekli Doymamış Yağlar", "Zeytinyağı, fındık yağı, avokado", "LDL'yi düşürür, HDL'yi korur (anti-aterojenik)"],
                    ["Omega-3 Yağ Asitleri", "Somon, uskumru, keten tohumu", "Trigliseridleri düşürür, antienflamatuar ve antiaritmik"]
                ]
            ),
            make_active_recall(
                "Endüstriyel gıdalarda ve margarinlerde bulunan, kanda aterojenik LDL kolesterolü yükseltirken aynı zamanda damar koruyucu HDL kolesterolü düşürerek ateroskleroz riskini en fazla artıran yağ asidi türü nedir?",
                "Trans yağ asitleridir (endüstriyel trans yağlar).",
                "Bitkisel sıvı yağların hidrojenlenmesiyle elde edilen yapay yağ sınıfı"
            )
        ]
    })

    # Slayt 82: Diyet Lifleri ve Kolorektal Kanser
    slides.append({
        "id": "k1-26-s82",
        "title": "Diyet Lifleri ve Kolorektal Kanser",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 82,
        "narrative": (
            "Diyet lifi (posa), sindirilemeyen kompleks bitkisel karbonhidratlar olup gastrointestinal sağlığın ve kanser korumasının temel taşıdır: "
            "1. **Dışkı Hacmi ve Seyreltme:** Lifler su tutarak fekal kütleyi artırır; diyetle alınan veya bakteriyel metabolizma "
            "sonucu açığa çıkan prokarsinojenlerin ve safra asitlerinin konsantrasyonunu seyreltir. "
            "2. **Transit Süresinin Kısaltılması:** Bağırsak peristaltizmini hızlandırır; dışkının kolonda kalış süresini kısaltarak "
            "kanserojen maddelerin kolonik mukoza epiteliyle temas süresini en aza indirir. "
            "3. **Mikrobiyota ve Kısa Zincirli Yağ Asitleri (SCFA):** "
            "- Kolon bakterileri çözünür lifleri fermente ederek **Kısa Zincirli Yağ Asitleri (özellikle Bütirat)** üretir. "
            "- Bütirat, kolonositlerin bir numaralı birincil enerji kaynağıdır. "
            "- Kolon epitelinde apoptozu düzenler, histon deasetilazı (HDAC) inhibe ederek tümör baskılayıcı genleri uyarır ve "
            "**kolorektal karsinom gelişimine karşı güçlü koruyucu bariyer** oluşturur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Düşük Lifli Batı Diyeti vs Yüksek Lifli Koruyucu Diyet",
                "Düşük Lifli / Yüksek Yağlı Diyet",
                "Uzamış kolonik geçiş süresi, konsantre karsinojenler ve sekonder safra asitlerinin mukozayı mutasyona uğratması",
                "Yüksek Lifli Sebze/Meyve Diyeti",
                "Hızlı fekal atılım, seyreltilmiş toksinler ve mikrobiyal bütirat üretimiyle kolon kanserine karşı aktif koruma"
            ),
            make_cloze(
                "Kolon bakterileri tarafından diyet liflerinin fermantasyonu sonucu üretilen ve kolonositlere enerji vererek kolorektal kansere karşı koruyan temel kısa zincirli yağ asidi bütirattır.",
                "bütirattır",
                "Dört karbonlu anti-karsinojenik kısa zincirli yağ asidi"
            )
        ]
    })

    # Slayt 83: Diyetle Alınan Kanserojenler: Aflatoksin B1
    slides.append({
        "id": "k1-26-s83",
        "title": "Diyetle Alınan Kanserojenler: Aflatoksin B1",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 83,
        "narrative": (
            "Diyetle alınan doğal toksinlerin en tehlikelisi, küflenmiş gıdalarda üreyen Aflatoksin B1'dir: "
            "1. **Köken ve Kaynak:** "
            "- Sıcak ve nemli depolama koşullarında yer fıstığı, mısır, fındık ve tahıllarda üreyen **Aspergillus flavus ve Aspergillus parasiticus** "
            "mantarları tarafından sentezlenen bir mikotoksindir. "
            "- Özellikle Sahra Altı Afrika ve Güneydoğu Asya'da depolanan tahıllarda yüksek konsantrasyonda bulunur. "
            "2. **Moleküler Karsinojenez Mekanizması:** "
            "- Karaciğerde sitokrom P450 (CYP1A2 ve CYP3A4) enzimleri tarafından son derece reaktif **Aflatoksin-2,3-epoksite** dönüştürülür. "
            "- Bu epoksit, DNA'daki guanin bazlarına kovalent bağlanarak DNA aduktı oluşturur. "
            "- **Patognomonik İmzalı Mutasyon:** Tümör baskılayıcı **TP53 geninin 249. kodonunda spesifik transversion mutasyonuna (G:C -> T:A)** yol açar (arginin yerine serin değişimi)! "
            "3. **Hepatit B İle Ölümcül Sinerji:** Hepatit B virüsü (HBV) taşıyıcılığı olan bir birey aynı zamanda aflatoksin aldığında, "
            "**Hepatoselüler Karsinom (HCC)** gelişme riski tek başına maruziyetlerin toplamı değil, yüzlerce kat çarpımsal artış sergiler!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Aflatoksinden Hepatoselüler Karsinoma Giden Moleküler Yol",
                [
                    "1. Gıda Küflenmesi: Nemli depolanan fıstık ve mısırda Aspergillus flavus mantarının üremesi",
                    "2. Aflatoksin Alımı: Diyetle alınan mikotoksinin portal venle karaciğere ulaşması",
                    "3. Sitokrom Epoksidasyonu: Hepatosit P450 enzimlerinin aflatoksini reaktif 2,3-epoksite çevirmesi",
                    "4. TP53 Kodon 249 Mutasyonu: DNA guaninlerine bağlanarak p53 geninde spesifik G->T transversionu yapması",
                    "5. Malign Transformasyon: Apoptoz kontrolünün çökmesiyle primer Hepatoselüler Karsinom (HCC) patlaması"
                ]
            ),
            make_active_recall(
                "Küflü tahıl ve fıstıklarda üreyen Aspergillus flavus kaynaklı Aflatoksin B1'in karaciğerde hepatoselüler karsinom başlatırken TP53 geninde mutasyona uğrattığı spesifik aminoasit kodonu hangisidir?",
                "Kodon 249 mutasyonudur (G:C -> T:A transversiyonu).",
                "p53 geninde arginin-serin değişimine yol açan karsinojenik parmak izi lokusu"
            )
        ]
    })

    # Slayt 84: Nitrozaminler ve Mide Kanseri
    slides.append({
        "id": "k1-26-s84",
        "title": "Nitrozaminler ve Mide Kanseri",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 84,
        "narrative": (
            "Gıdaların korunması ve işlenmesi amacıyla kullanılan kimyasallar sindirim sistemi karsinojenezinde belirleyicidir: "
            "1. **Nitrit ve Nitratlar:** "
            "- İşlenmiş et ürünlerine (sosis, salam, pastırma) botulizm bakterisini (*Clostridium botulinum*) engellemek ve "
            "kırmızı rengi korumak için sodyum nitrit ve nitrat tuzları eklenir. "
            "2. **Endojen Nitrozamin Teşekkülü:** "
            "- Midedeki asidik ortamda veya yüksek ısıda pişirme sırasında (tütsüleme, mangal, kızartma), nitritler besinlerdeki "
            "sekonder aminlerle reaksiyona girerek **Nitrozaminlere ve Nitrozamidlere** dönüşür. "
            "- Ayrıca tuzlu, salamura ve tütsülenmiş gıdaların aşırı tüketimi mide mukozasını kimyasal olarak aşındırır. "
            "3. **Mide Karsinojenezi (İntestinal Tip Gastrik Adenokarsinom):** "
            "- Nitrozaminler mide mukozasında DNA alkilasyonu yaparak kronik atrofik gastrit, intestinal metaplazi ve displaziye yol açar. "
            "- **Helicobacter pylori** enfeksiyonunun varlığı, mukozal inflamasyonu harlayarak nitrozaminlerin karsinojenik gücünü katlar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Diyet Kanserojenleri ve Hedef Maligniteler",
                ["Besinsel Kanserojen", "Temel Gıda Kaynağı", "İlişkili Kanser Türü", "Önleyici Beslenme Stratejisi"],
                [
                    ["Aflatoksin B1", "Küflü fıstık, mısır, tahıl", "Hepatoselüler Karsinom (HCC)", "Kuru ve havalandırmalı depolama, HBV aşısı"],
                    [
                        "Nitrozaminler / Nitritler",
                        "Tütsülenmiş etler, salamura, sosis",
                        {"text": "İntestinal tip mide adenokarsinomu", "isMasked": True, "hint": "Midede atrofi ve metaplazi üzerinden gelişen mukozal epitelyal kanser"},
                        "Taze sebze/meyve, C vitamini (nitrozasyon bloker)"
                    ],
                    ["Heterosiklik Aminler", "Kömür ateşinde aşırı pişmiş et", "Kolorektal karsinom", "Düşük ısıda haşlama/fırınlama"]
                ]
            ),
            make_cloze(
                "İşlenmiş et ürünlerindeki nitritlerin mide asidinde aminlerle birleşmesi sonucu oluşan ve mide adenokarsinomuna yol açan kimyasal bileşiklere nitrozaminler adı verilir.",
                "nitrozaminler",
                "Mide mukozasında DNA alkilasyonu yapan güçlü karsinojenik azotlu bileşikler sınıfı"
            )
        ]
    })

    # Slayt 85: Yağda Eriyen Vitamin Eksiklikleri: A ve D Vitamini
    slides.append({
        "id": "k1-26-s85",
        "title": "Yağda Eriyen Vitamin Eksiklikleri: A ve D Vitamini",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 85,
        "narrative": (
            "Yağda eriyen vitaminler (A, D, E, K) vücutta depolanır; ancak yağ malabsorpsiyonunda (kistik fibrozis, çölyak) hızla eksilir: "
            "1. **A Vitamini (Retinol):** "
            "- Retinada rodopsin görme pigmentinin bileşenidir; eksikliğinde ilk bulgu **Gece Körlüğüdür (Niktalopi)**. "
            "- Epitel farklılaşmasını sürdürür; eksikliğinde mukus salgılayan epitel yerini kuru skuamöz keratinize epitele bırakır (**Skuamöz Metaplazi**). "
            "- **Kseroftalmi (Göz Kuruluğu):** Kornea kurur; konjonktivada keratin köpükleri (**Bitot Lekeleri**) oluşur; "
            "kornea yumuşar ve delinir (**Keratomalazi** - çocukluk körlüğünün majör nedeni). "
            "- İmmün yetmezlik yapar; çocuklarda kızamık enfeksiyonunu ölümcül kılar. "
            "2. **D Vitamini (Kalsitriol):** "
            "- Kalsiyum ve fosfat homeostazını sağlar. "
            "- Eksikliğinde çocuklarda epifiz büyüme plağında mineralizasyon bozulur: **Raşitizm (Rickets)** (kıkırdak yığılması, göğüste raşitik tespih, bacaklarda O-bacak deformitesi). "
            "- Erişkinlerde ise mineralize olmamış osteoid birikimiyle kemik yumuşaması: **Osteomalazi** gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "A ve D Vitamini Patolojisi Karşılaştırması",
                ["Vitamin", "Fizyolojik Fonksiyon", "Eksiklik Morfolojisi ve Kliniği"],
                [
                    ["A Vitamini (Retinol)", "Görme pigmenti, epitel diferansiasyonu", "Gece körlüğü, Bitot lekeleri, keratomalazi, skuamöz metaplazi"],
                    [
                        "D Vitamini (Kalsiferol)",
                        "Kemik mineralizasyonu ve Ca emilimi",
                        {"text": "Çocukta Raşitizm (raşitik tespih), erişkinde Osteomalazi", "isMasked": True, "hint": "Kalsiyum çöktürülememesi sonucu kemik epifiz ve osteoidinin yumuşaması tablosu"}
                    ]
                ]
            ),
            make_active_recall(
                "A vitamini eksikliği olan bir çocuğun göz konjonktivasında keratin artıklarının birikmesiyle oluşan grimsi-gümüş renkli köpüksü üçgen lezyonlara ne ad verilir?",
                "Bitot lekeleridir (Bitot spots).",
                "Kseroftalmi tablosunda göz beyazı üzerinde keratinize epitel birikintisi plakları"
            )
        ]
    })

    # Slayt 86: Suda Eriyen Vitamin Eksiklikleri: C Vitamini ve Skorbüt
    slides.append({
        "id": "k1-26-s86",
        "title": "Suda Eriyen Vitamin Eksiklikleri: C Vitamini ve Skorbüt",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 86,
        "narrative": (
            "C Vitamini (Askorbik Asit), taze sebze ve turunçgillerde bolca bulunan, vücutta sentezlenemeyen esansiyel bir vitamindir: "
            "1. **Biyokimyasal Rolü:** "
            "- Kollajen biyosentezinde **prolil ve lizil hidroksilaz** enzimlerinin aktif merkezindeki demiri ($Fe^{2+}$) indirgenmiş halde tutan esansiyel kofaktördür. "
            "- Hidroksiprolin ve hidroksilizin olmadan kollajen polipeptitleri üçlü sarmal (triple helix) yapamaz ve hücre dışına salınamaz; "
            "kollajen lifleri son derece zayıf ve kırılgandır. "
            "2. **Skorbüt (Scurvy) Hastalığı:** "
            "- **Damar Kırılganlığı ve Kanamalar:** Kapiller bazal membran kollajeni çöker; kılcal damarlar patlar. "
            "Ciltte kıl folikülleri çevresinde **perifoliküler peteşiler ve purpuralar** oluşur. "
            "- **Gingival Patoloji:** Diş etleri aşırı derecede şiş, morumsu, süngerimsi ve spontan kanamalıdır; dişler gevşeyip düşer. "
            "- **Subperiosteal Kanamalar:** Özellikle çocuklarda uzun kemik periostu altına masif kanamalar olur; periost gerilir ve "
            "şiddetli kemik ağrısıyla çocuk bacaklarını hareket ettiremez (**sahte felç / pseudoparalizi**). "
            "- Yetersiz kollajen nedeniyle ameliyat ve travma yaraları iyileşemez, yaralar açılır (yara açılması)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "C Vitamini Eksikliğinden Skorbüt Kanamalarına Giden Yolak",
                [
                    "1. Askorbik Asit Yokluğu: Diyetle taze meyve ve sebze alımının aylarca sıfırlanması",
                    "2. Enzim Felci: Prolil ve lizil hidroksilaz enzimlerinin kofaktörsüz kalarak durması",
                    "3. Bozuk Üçlü Sarmal: Hidroksillenmemiş prokollajenin stabil fibriller oluşturamaması",
                    "4. Kapiller Frajilite: Damar duvarı bazal membranının desteğini kaybedip çatlaması",
                    "5. Skorbüt Kanamaları: Diş eti hipertrofisi, perifoliküler peteşi ve subperiosteal hematomlar"
                ]
            ),
            make_active_recall(
                "Kollajen sentezinde prolil ve lizil hidroksilaz enzimlerinin kofaktörü olan ve eksikliğinde diş eti kanamaları, perifoliküler purpura ve subperiosteal hematomlarla giden skorbüte yol açan vitamin nedir?",
                "C vitaminidir (askorbik asit).",
                "Kollajen üçlü heliks stabilitesini sağlayan suda eriyen antioksidan vitamin"
            )
        ]
    })

    # Slayt 87: Pediatrik Patolojiye Giriş ve Prematürite
    slides.append({
        "id": "k1-26-s87",
        "title": "Pediatrik Patolojiye Giriş ve Prematürite",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 87,
        "narrative": (
            "Pediatrik patoloji, organ gelişimi tamamlanmamış büyüme evresindeki bebek ve çocukların özgün hastalıklarını inceler: "
            "1. **Prematürite (Erken Doğum):** Gebeliğin 37. haftasından önce gerçekleşen doğumlardır. "
            "Yenidoğan ölümlerinin ve konjenital sekellerin en büyük nedenidir. "
            "2. **Respiratuar Distres Sendromu (RDS / Hiyalin Membran Hastalığı):** "
            "- Prematüre akciğerinde Tip 2 pnömositler henüz olgunlaşmamıştır; **sürfaktan (dipalmitoilfosfatidilkolin)** sentezlenemez. "
            "- Alveol yüzey gerilimi düşürülemez; her ekspiryumda alveoller tamamen kollabe olur (**yaygın mikroatelektazi**). "
            "- Hipoksi ve endotel sızıntısıyla alveol lümenlerine dökülen fibrin ve nekrotik epitel artıkları, "
            "alveol çeperlerini pembe camsı bir kılıf gibi sarar (**Hiyalin Membranlar**). Bebek boğularak kaybedilir. "
            "3. **Nekrotizan Enterokolit (NEK):** "
            "- Prematüre bağırsak mukozasında iskemi, formüla mama ile beslenme ve bakteriyel kolonizasyon sonucu gelişir. "
            "- Terminal ileum ve kolonda tam kat koagülasyon nekrozu; bağırsak duvarında gaz kabarcıkları (**pnömatozis intestinalis**) ve perforasyon."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Yenidoğan RDS'sinde Sürfaktan Varlığı ve Yokluğu",
                "Normal Matür Akciğer (Sürfaktan Var)",
                "Alveol yüzey gerilimi düşüktür; ekspiryum sonunda alveoller açık kalır, nefes almak kolay ve doğaldır",
                "Prematüre Akciğeri (RDS / Sürfaktan Yok)",
                "Alveoller ekspiryumda tamamen çöker; fibrin birikimiyle hiyalin membranlar oluşur, ağır solunum çöküşü gelişir"
            ),
            make_cloze(
                "Prematüre bebeklerde sürfaktan eksikliği sonucu alveol duvarlarını saran pembe fibrinöz kılıflara hiyalin membran adı verilir.",
                "hiyalin membran",
                "Alveol boşluklarında gaz değişimini engelleyen eozinofilik camsı protein kılıfı"
            )
        ]
    })

    # Slayt 88: Pediatrik Neoplaziler: Küçük Yuvarlak Mavi Hücreli Tümörler
    slides.append({
        "id": "k1-26-s88",
        "title": "Pediatrik Neoplaziler: Küçük Yuvarlak Mavi Hücreli Tümörler",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 88,
        "narrative": (
            "Çocukluk çağı maligniteleri erişkin karsinomlarından köken, morfoloji ve genetik açıdan tamamen farklıdır: "
            "1. **Blastik ve Embriyonal Karakter:** "
            "- Erişkinlerde epitelyal karsinomlar hakimken, çocuklarda hematopoietik sistem (lösemiler/lenfomalar), "
            "SSS tümörleri ve embriyonal dokulardan köken alan **'blastomlar'** hakimdir. "
            "2. **Küçük Yuvarlak Mavi Hücreli Tümörler (KYMHT):** "
            "- Işık mikroskopisinde dar sitoplazmalı, hiperkromatik koyu mavi nükleuslu primitif embriyonik hücrelerden oluşan tümör grubudur. "
            "- **Nöroblastom:** Sürrenal medulladan veya sempatik zincirden köken alır; nöropil zemini ve **Homer-Wright rozetleri** karakteristiktir. "
            "Moleküler kötü prognoz belirteci: **N-MYC gen amplifikasyonudur**. İdrarda VMA ve HVA yükselir. "
            "- **Wilms Tümörü (Nefroblastom):** Böbreğin en sık pediatrik tümörüdür; trifazik morfoloji (blastem, stroma, epitelyal tübüller) "
            "ve WT1/WT2 gen mutasyonları gösterir. "
            "- **Retinoblastom:** Göz içi malignitesi; **RB1** tümör baskılayıcı gen mutasyonu; Flexner-Wintersteiner rozetleri."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Pediatrik Embriyonal Tümörler ve Genetik Belirteçleri",
                ["Tümör Adı", "Köken Aldığı Doku", "Karakteristik Histopatoloji", "Genetik / Prognostik Belirteç"],
                [
                    ["Nöroblastom", "Sürrenal medulla / Sempatik gangliyon", "Homer-Wright rozetleri, nöropil", "N-MYC gen amplifikasyonu (kötü prognoz)"],
                    [
                        "Wilms Tümörü (Nefroblastom)",
                        "Metanefrik böbrek blastemi",
                        {"text": "Trifazik yapı: Blastem, iğsi stroma, primitif tübüller", "isMasked": True, "hint": "Embriyonal böbrek dokusunu taklit eden üçlü hücresel tümör bileşeni"},
                        "WT1 (11p13) ve WT2 (11p15) defektleri"
                    ],
                    ["Retinoblastom", "Retina nöroepitelyumu", "Flexner-Wintersteiner rozetleri", "RB1 (13q14) çift alel inaktivasyonu"]
                ]
            ),
            make_micro_quiz(
                "İki yaşında bir çocuğun batın ultrasonografisinde böbrek üstü bezinde kitle saptanmış, biyopside küçük yuvarlak mavi hücreler ve nöropil içeren Homer-Wright rozetleri izlenmiştir. Bu nöroblastom olgusunda agresif seyir ve kötü prognozu gösteren moleküler belirteç hangisidir?",
                {
                    "A": "N-MYC onkogen amplifikasyonu",
                    "B": "HER2 gen duplikasyonu",
                    "C": "BCR-ABL füzyonu",
                    "D": "APC gen mutasyonu",
                    "E": "BRAF V600E mutasyonu"
                },
                "A",
                {
                    "A": "Doğrudur; nöroblastomda çift dakika kromozomlar veya homojen boyanan bölgeler şeklinde N-MYC amplifikasyonu çok kötü prognoz işaretidir.",
                    "B": "Yanlış; HER2 meme ve mide karsinomundadır.",
                    "C": "Yanlış; BCR-ABL kronik miyeloid lösemidedir.",
                    "D": "Yanlış; APC kolon polipozisindedir.",
                    "E": "Yanlış; BRAF melanom ve tiroiddedir."
                }
            )
        ]
    })

    # Slayt 89: Checkpoint 9
    slides.append({
        "id": "k1-26-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Diyet Kanserojenleri, Vitaminler ve Pediatrik Patoloji",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 89,
        "narrative": (
            "Dokuzuncu kontrol noktamızda diyet kanserojenlerini, vitaminleri ve pediatrik patolojiyi pekiştiriyoruz: "
            "1. **Yağlar:** Doymuş ve trans yağlar LDL'yi yükseltir ve ateroskleroz yapar; lifler ise bütirat üreterek kolon kanserinden korur. "
            "2. **Aflatoksin B1:** Aspergillus flavus; küflü tahıllarda; TP53 kodon 249 mutasyonu ile Hepatoselüler Karsinom (HBV ile sinerji). "
            "3. **Nitrozaminler:** İşlenmiş etlerdeki nitritler mide asidinde oluşur; gastrik adenokarsinom yapar. "
            "4. **A ve D Vitamini:** A vitamini eksikliğinde gece körlüğü, Bitot lekeleri ve kseroftalmi; D vitamini eksikliğinde çocukta raşitizm, erişkinde osteomalazi. "
            "5. **C Vitamini:** Kollajen prolil/lizil hidroksilaz kofaktörüdür; eksikliğinde diş eti kanaması, perifoliküler peteşi ve skorbüt gelişir. "
            "6. **Pediatri:** Prematürede sürfaktan eksikliği RDS (hiyalin membran) yapar; Nöroblastomda N-MYC amplifikasyonu kötü prognozludur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s89-1",
                "Nemli depolanan fıstık ve tahıllarda üreyen Aspergillus flavus mantarının ürettiği ve TP53 geninde spesifik mutasyonla karaciğer kanserine yol açan mikotoksin nedir?",
                "Aflatoksin B1 toksinidir.",
                "Küflü tarım ürünlerinde üreyen ve hepatoselüler karsinomu tetikleyen güçlü fungal kanserojen",
                "Diyet Kanserojenleri"
            ),
            make_flashcard(
                "k1-26-fc-s89-2",
                "Kollajen sentezinde prolin ve lizin aminoasitlerinin hidroksilasyonunda esansiyel kofaktör olan ve eksikliğinde skorbüt tablosu gelişen vitamin nedir?",
                "C vitaminidir (askorbik asit).",
                "Eksikliğinde gingival kanama, perifoliküler peteşi ve bağ dokusu frajilitesi görülen besin kofaktörü",
                "Vitamin Eksiklikleri"
            ),
            make_flashcard(
                "k1-26-fc-s89-3",
                "Prematüre yenidoğanlarda alveolar tip 2 pnömositlerin yetersiz sürfaktan üretimine bağlı olarak atelektazi ve gaz değişim çöküşüyle seyreden akciğer tablosu nedir?",
                "Respiratuar distres sendromudur (RDS / hiyalin membran hastalığı).",
                "Dipalmitoillesitin eksikliğiyle alveollerin ekspiryumda kollabe olduğu erken doğum patolojisi",
                "Pediatrik Patoloji"
            )
        ],
        "interactiveElements": [
            make_table(
                "Beslenme ve Pediatrik Patoloji Checkpoint Özeti",
                ["Kavram / Hastalık", "Temel Moleküler Bozukluk", "Karakteristik Histopatolojik Belirteç", "Primer Organ"],
                [
                    ["Aflatoksin B1", "TP53 kodon 249 mutasyonu", "Hepatoselüler karsinom ve displazi", "Karaciğer"],
                    ["Skorbüt (C Vitamini)", "Prolil/lizil hidroksilaz inaktivasyonu", "Defektif kollajen, kapiller rüptürler", "Diş eti, kemik periostu, cilt"],
                    [
                        "Yenidoğan RDS",
                        "Tip 2 pnömosit sürfaktan eksikliği",
                        {"text": "Alveolleri döşeyen eozinofilik hiyalin membranlar", "isMasked": True, "hint": "Atelektazi zemininde plazma proteinlerinin alveol duvarına yapışması"},
                        "Akciğer alveolleri"
                    ],
                    ["Nöroblastom", "Sempatik nöroblast neoplazisi", "Homer-Wright rozetleri, N-MYC amplifikasyonu", "Sürrenal medulla"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi C vitamini eksikliğine bağlı skorbüt hastalığında kemiklerde ve periost altında meydana gelen patolojik kanama tablosunu en iyi açıklar?",
                {
                    "A": "Kollajen hidroksilasyonunun bozulması sonucu kapiller endotel bazal membran desteğinin çökmesi",
                    "B": "Karaciğerde pıhtılaşma faktörlerinin sentezlenememesi",
                    "C": "Kanda trombosit sayısının sıfıra inmesi",
                    "D": "Kemik iliğinde eritrosit üretiminin durması",
                    "E": "Kalsiyum kristallerinin damarları kesmesi"
                },
                "A",
                {
                    "A": "Doğrudur; askorbik asit yokluğunda kollajen üçlü heliksi kurulamaz, damar duvarı frajil hale gelir ve periost altı hematomlar oluşur.",
                    "B": "Yanlış; bu K vitamini veya karaciğer yetmezliğidir.",
                    "C": "Yanlış; trombositopeni skorbüt primer nedeni değildir.",
                    "D": "Yanlış; anemi ikincil olabilir ama primer vasküler defekttir.",
                    "E": "Yanlış; kalsiyum mekanik kesisi olmaz."
                }
            )
        ]
    })

    # Slayt 90: Ani Bebek Ölümü Sendromu (SIDS)
    slides.append({
        "id": "k1-26-s90",
        "title": "Ani Bebek Ölümü Sendromu (SIDS)",
        "section": "Diyet Kanserojenleri ve Pediatrik Patoloji",
        "slideNumber": 90,
        "narrative": (
            "Ani Bebek Ölümü Sendromu (SIDS / Beşik Ölümü), 1 yaş altındaki bir bebeğin ayrıntılı postmortem otopsi, "
            "olay yeri incelemesi ve klinik öykü araştırmasına rağmen açıklanamayan ani ve beklenmedik ölümüdür: "
            "1. **Üçlü Risk Hipotezi (Triple-Risk Model):** "
            "- **Savunmasız Bebek (Vulnerable Infant):** Beyin sapında (arkuat çekirdek) kardiyorespiratuar kontrolü ve "
            "uykudan uyanma (arousal) refleksini yöneten **serotonerjik (5-HT) nöronal iletim sisteminde gelişimsel gecikme/defekt**. "
            "- **Kritik Gelişim Evresi:** En sık 2. ile 4. aylar arasında görülür (otonomik kontrolün yeniden şekillendiği evre). "
            "- **Dışsal Tetikleyici Faktör:** **YÜZÜSTÜ (PRONE) UYUMA POZİSYONU**, yumuşak yatak, aşırı giydirme/ortam sıcaklığı ve "
            "anne-baba yanında aynı yatakta uyuma (co-sleeping). "
            "2. **Önlenebilir En Kritik Risk Faktörü:** "
            "- Gebelikte ve doğum sonrasında **anne sigarası maruziyeti** SIDS riskini 2-3 kat artırır. "
            "- Bebeklerin sırtüstü (supine) yatırılması kampanyası ('Back to Sleep') ile küresel SIDS ölümleri %50'den fazla azalmıştır!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "SIDS Riskinde Uyku Pozisyonu Paradigması",
                "Yüzüstü (Prone) Uyuma Pozisyonu",
                "Asfiksi durumunda uyanma refleksinin baskılanması, ekshale edilen CO2'in yeniden solunması ve SIDS patlaması",
                "Sırtüstü (Supine) Güvenli Uyku Pozisyonu",
                "Havayolu açıklığının korunması ve SIDS vakalarında %50'nin üzerinde dramatik hayat kurtarıcı düşüş"
            ),
            make_active_recall(
                "Ani Bebek Ölümü Sendromunu (SIDS) önlemek amacıyla dünya çapında başlatılan ve bebeklerin daima sırtüstü yatırılmasını öğütleyerek ölümleri yarı yarıya azaltan küresel kampanyanın adı nedir?",
                "'Sırtüstü Uyku' kampanyasıdır (Back to Sleep).",
                "Yüzüstü yatışın getirdiği asfiksi riskini sırtüstü pozisyonla engelleyen küresel rehber"
            )
        ]
    })

    return slides
