# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-20-s01",
        "title": "Hemostaz ve Tromboz Kavramları: Fizyolojik Denge vs İntravasküler Patoloji",
        "content": "Kardiyovasküler sistemin bütünlüğü ve dokuların canlılığı, damar içi kanın sıvı (akışkan) halde kalmasına ve damar yaralanmalarında anında lokal bir tıkaç oluşturulmasına bağlıdır (Sınav Spotu):\n\n- **Normal Hemostaz:** Damar duvarı yaralandığında kan kaybını önlemek amacıyla hasar bölgesinde lokalize, kontrollü ve geçici bir hemostatik tıkaç (pıhtı) oluşturulması sürecidir; fizyolojik ve koruyucudur.\n- **Tromboz:** Canlı bir organizmada, sağlam bir damarın lümeni içinde veya hasarlı damarda gereksiz/aşırı şekilde kan hücreleri ve fibrin kitlelerinin toplanarak kan akımını engellemesidir.\n- **Patolojik Nitelik:** Tromboz, hemostatik mekanizmaların uygunsuz, aşırı ve kontrolsüz bir şekilde devreye girmesiyle ortaya çıkan patolojik bir süreçtir.\n- **Klinik Önem:** Günümüzde gelişmiş toplumlardaki en sık ölüm nedenleri olan miyokard enfarktüsü, iskemik inme ve pulmoner tromboembolinin temelinde tromboz yatar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Fizyolojik Hemostaz vs Patolojik Tromboz",
                "Fizyolojik Hemostaz (Koruyucu)",
                "Damar hasarı sonrasında kanamayı durdurmak için lokal, sınırlı ve çözülebilen pıhtı oluşumudur.",
                "Patolojik Tromboz (Tıkayıcı)",
                "Canlı damar lümeninde uygunsuz, aşırı ve kontrolsüz hemostatik yanıtla lümenin tıkanmasıdır."
            ),
            make_cloze(
                "Canlı bir organizmada damar lümeni içinde uygunsuz ve aşırı hemostatik yanıt sonucu pıhtı kitlesi oluşmasına tromboz adı verilir.",
                "tromboz",
                "Damar içi kan akımını engelleyen patolojik pıhtılaşma süreci"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-20-s02",
        "title": "Hemostazın Üç Ana Bileşeni: Endotel, Trombositler ve Faktörler",
        "content": "Hemostaz ve tromboz, üç temel biyolojik bileşenin sürekli ve son derece hassas etkileşimiyle gerçekleşir (Sınav Spotu):\n\n- **1. Endotel Hücreleri:**\n  - Normal şartlarda damar duvarını örten endotel güçlü bir **antitrombotik yüzeydir** (trombosit agregasyonunu ve pıhtılaşmayı engeller).\n  - Ancak hasar gördüğünde veya aktive olduğunda doku faktörü ve adezyon molekülleri salgılayarak güçlü bir **protrombotik yüzeye** dönüşür.\n- **2. Trombositler (Trombositik Tıkaç):**\n  - Damar bütünlüğü bozulduğunda subendotelyal matrikse hızla yapışır, aktive olur, granüllerini boşaltır ve primer hemostatik tıkacı oluşturur.\n- **3. Koagülasyon Kaskadı (Pıhtılaşma Faktörleri):**\n  - Çoğu karaciğerde sentezlenen ve plazmada inaktif proenzimler halinde dolaşan faktörlerdir; aktive olarak çözünür fibrinojeni çözünmeyen **fibrin ağına** dönüştürür.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hemostaz Bileşeni", "Normal Durumdaki Rolü", "Hasar Anındaki Rolü"],
                [
                    ["Endotel Hücreleri", "Antitrombotik yüzey (PGI2, NO, trombomodulin)", "Protrombotik yüzey (Doku faktörü, vWF salgısı)"],
                    ["Trombositler", "İnaktif yuvarlak dolaşım hücre fragmanları", "Adezyon, aktivasyon, degranülasyon ve agregasyon"],
                    ["Koagülasyon Faktörleri", "İnaktif proenzimler halinde dolaşım", "Kaskad aktivasyonu ile fibrin polimeri oluşturma"]
                ]
            ),
            make_quiz(
                "Aşağıdakilerden hangisi normal hemostatik dengenin sağlanmasında rol alan üç temel anatomik ve biyokimyasal bileşenden biridir?",
                [
                    {"key": "A", "text": "Endotel hücreleri, trombositler ve koagülasyon faktörleri", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hemostaz endotel, trombositler ve pıhtılaşma faktörlerinin dinamik dengesiyle yürütülür."},
                    {"key": "B", "text": "Yalnızca kemik iliği ve dalak stroması", "isCorrect": False, "explanation": "Hemostaz damar içi lokal sistemdir."},
                    {"key": "C", "text": "Yalnızca böbrek eritropoietini ve lökositler", "isCorrect": False, "explanation": "Eritropoietin eritrosit yapımını uyarır, pıhtılaşma bileşeni değildir."},
                    {"key": "D", "text": "Yalnızca lenf düğümleri ve T lenfositler", "isCorrect": False, "explanation": "T lenfositler hücresel bağışıklıktan sorumludur."}
                ]
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-20-s03",
        "title": "1. Basamak: Geçici Arteriyel Vazokonstriksiyon ve Endotelin-1",
        "content": "Damar duvarı hasar gördüğünde kan kaybını ilk saniyelerde azaltmak için anlık bir vazomotor yanıt gelişir (Sınav Spotu):\n\n- **Hemen Gerçekleşen Yanıt:** Damar yaralanmasını takip eden milisaniyeler içinde etkilenen arteriyol ve kapillerlerde belirgin bir **arteriyel vazokonstriksiyon** (damar daralması) meydana gelir.\n- **İki Temel Mekanizma:**\n  1. **Nörojenik Refleks:** Ağrı reseptörleri ve sempatik sinir uçlarının lokal refleks uyarımı ile düz kas kontraksiyonu tetiklenir.\n  2. **Endotelin-1 Salgısı:** Hasarlı ve aktive olmuş endotel hücrelerinden lokal olarak güçlü bir peptit vazokonstriktör olan **endotelin** salgılanır.\n- **Geçici Nitelik:** Bu vazokonstriksiyon kan akımını ve kanamayı belirgin azaltır ancak **geçicidir (dakikalar sürer)**; kanamanın kalıcı durması için trombositlerin ve pıhtılaşma sisteminin hemen devreye girmesi şarttır.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Vasküler Yaralanmada İlk Basamak: Vazokonstriksiyon",
                [
                    "1. Mekanik Hasar: Damar duvarı endoteli ve düz kas tabakası yırtılır.",
                    "2. Nörojenik Refleks: Sempatik otonom sinir uçları lokal refleksle uyarılır.",
                    "3. Endotelin-1 Salınımı: Endotelden güçlü vazokonstriktör peptit salgılanır.",
                    "4. Arteriyoler Daralma: Düz kaslar kasılarak lümen çapı daraltılır.",
                    "5. Kanama Hızında Düşüş: Hasarlı bölgeye gelen kan akımı geçici olarak azaltılır."
                ]
            ),
            make_cloze(
                "Damar hasarı anında nörojenik reflekslerin yanı sıra hasarlı endotelden salgılanan endotelin hormonu güçlü lokal vazokonstriksiyona yol açar.",
                "endotelin",
                "Endotelden salgılanan güçlü lokal damar daraltıcı peptit molekül"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-20-s04",
        "title": "2. Basamak: Primer Hemostaz ve Gevşek Trombosit Tıkacı",
        "content": "Endotelin yırtılmasıyla damar altı bağ dokusu dolaşıma açılır ve primer hemostatik mekanizma tetiklenir (Sınav Spotu):\n\n- **Subendotelyal Matriksin Açığa Çıkması:** Endotel bariyeri kalktığında alttaki **von Willebrand faktörü (vWF)** ve **kollajen lifleri** kan akımıyla temas eder.\n- **Trombosit Adezyonu (Yapışma):** Trombositler yüzeylerindeki **Glikoprotein Ib (GpIb)** reseptörleri aracılığıyla subendotelyal vWF'ye sıkıca yapışır.\n- **Aktivasyon ve Şekil Değişikliği:** Trombositler disk şeklinden yalancı ayaklı (psödopodlu) dikenli bir küreye dönüşür; membranlarındaki negatif yüklü fosfatidilserin dış yüzeye döner.\n- **Degranülasyon ve Agregasyon:** Trombositlerden **ADP** ve **Tromboksan A2 (TxA2)** salgılanır; bu aracılar yeni trombositleri bölgeye çağırır (toplanma).\n- **GpIIb/IIIa ve Fibrinojen:** Aktive trombositler **GpIIb/IIIa** reseptörleri üzerinden **fibrinojen köprüleriyle** birbirine kenetlenerek **primer hemostatik tıkacı (gevşek trombosit tıkacı)** oluşturur.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Trombosit Adezyonu (GpIb) vs Trombosit Agregasyonu (GpIIb/IIIa)",
                "Trombosit Adezyonu (GpIb / vWF)",
                "Trombositlerin damar duvarındaki subendotelyal kollajen ve vWF'ye yapışmasıdır.",
                "Trombosit Agregasyonu (GpIIb/IIIa / Fibrinojen)",
                "Trombositlerin fibrinojen köprüleri aracılığıyla birbirine bağlanıp kümelenmesidir."
            ),
            make_cloze(
                "Primer hemostaz sürecinde trombositlerin birbirine bağlanarak agregasyon yapmasını GpIIb/IIIa reseptörleri ve aradaki fibrinojen köprüleri sağlar.",
                "GpIIb/IIIa",
                "Trombosit agregasyonunda fibrinojeni bağlayan kilit yüzey glikoproteini"
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-20-s05",
        "title": "3. Basamak: Sekonder Hemostaz, Doku Faktörü ve Fibrin Ağı",
        "content": "Primer trombosit tıkacı yumuşaktır ve yüksek kan basıncında kolayca süpürülebilir; bu tıkacın sağlamlaştırılması sekonder hemostaz ile sağlanır (Sınav Spotu):\n\n- **Doku Faktörünün (Tromboplastin / Faktör III) Açığa Çıkması:** Yaralanma bölgesinde subendotelyal hücrelerin (fibroblastlar ve düz kas hücreleri) zarında bulunan **Doku Faktörü (TF)** kana maruz kalır.\n- **Kaskadın Ateşlenmesi:** Doku faktörü plazmadaki **Faktör VIIa** ile birleşerek ekstrinsik koagülasyon kaskadını başlatır; Faktör IX ve X aktive edilir.\n- **Trombin Patlaması (Faktör IIa):** Kaskadın merkezinde protrombin, güçlü proteolitik enzim olan **trombine** dönüştürülür.\n- **Fibrin Ağı:** Trombin dolaşımdaki çözünür bir plazma proteini olan **fibrinojeni** parçalayarak çözünmeyen **fibrin monomerlerine** ve ardından fibrin polimerlerine dönüştürür.\n- **Çimentolama:** Fibrin polimerleri trombosit tıkacının arasına örümcek ağı gibi girerek primer tıkacı sağlam, sert bir **sekonder hemostatik tıkaca** çevirir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Sekonder Hemostazın Temel Basamakları",
                [
                    "1. TF Salınımı: Subendotelyal fibroblastlardan doku faktörü açığa çıkar.",
                    "2. TF-VIIa Kompleksi: Doku faktörü Faktör VIIa'yı bağlayarak kaskadı açar.",
                    "3. Faktör Xa Üretimi: Tenaz kompleksi Faktör X'u aktif Faktör Xa'ya çevirir.",
                    "4. Trombin Oluşumu: Protrombinaz kompleksi protrombini trombine (IIa) dönüştürür.",
                    "5. Fibrin Ağı: Trombin fibrinojeni çözünmeyen fibrin liflerine polimerize eder."
                ]
            ),
            make_quiz(
                "Sekonder hemostazı in vivo ortamda başlatan en kritik subendotelyal glikoprotein hangisidir?",
                [
                    {"key": "A", "text": "Doku Faktörü (Tromboplastin / Faktör III)", "isCorrect": True, "explanation": "Doğru cevap A'dır: İn vivo koagülasyon kaskadını başlatan anahtar molekül subendotelyal hücrelerde bulunan Doku Faktörüdür (TF)."},
                    {"key": "B", "text": "Faktör XII (Hageman Faktörü)", "isCorrect": False, "explanation": "Faktör XII in vitro kontakt yolunu başlatır, in vivo hemostazda kritik değildir."},
                    {"key": "C", "text": "Antitrombin III", "isCorrect": False, "explanation": "Antitrombin III pıhtılaşmayı başlatan değil durduran bir inhibitördür."},
                    {"key": "D", "text": "Protein C", "isCorrect": False, "explanation": "Protein C antikoagülan bir proteindir."}
                ]
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-20-s06",
        "title": "4. Basamak: Pıhtı Konsolidasyonu, Faktör XIII ve Sınırlama",
        "content": "Fibrin oluştuktan sonra pıhtı stabilize edilir ve damar lümenini tamamen tıkamaması için antikoagülan mekanizmalarla sınırlandırılır (Sınav Spotu):\n\n- **Fibrinin Çapraz Bağlanması (Faktör XIIIa):**\n  - Trombin tarafından aktive edilen **Faktör XIIIa (Fibrin stabilize edici faktör)**, komşu fibrin monomerleri arasında kovalent glutamil-lisil çapraz bağları kurar.\n  - Bu işlem pıhtıyı mekanik gerilmelere ve erken enzimatik yıkıma karşı son derece dayanıklı hale getirir.\n- **Pıhtı Retraksiyonu (Kasılma):**\n  - Trombositlerin içindeki aktin ve miyozin mikrofilamanları kasılarak pıhtıyı büzüştürür; yaranın kenarları birbirine yaklaşır ve serum dışarı sızar.\n- **Antitrombotik ve Fibrinolitik Sınırlama:**\n  - Sağlam komşu endotel hücrelerinden salgılanan **t-PA (doku plazminojen aktivatörü)** ve **trombomodulin**, pıhtının hasarsız damar bölgelerine yayılmasını önler; doku onarımı tamamlandığında pıhtı eritilir (fibrinoliz).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Stabilizasyon ve Sınırlama Faktörü", "Biyolojik Fonksiyonu", "Eksikliğinde Sonuç"],
                [
                    ["Faktör XIIIa", "Fibrin lifleri arasında kovalent çapraz bağ kurma", "Gecikmiş kanama ve yara iyileşmesinde bozulma"],
                    ["Trombosit Aktin-Miyozin", "Pıhtı retraksiyonu (büzüşme) sağlama", "Gevşek, zayıf hemostatik tıkaç"],
                    ["t-PA ve Trombomodulin", "Pıhtının hasarsız lümene taşmasını engelleme", "Kontrolsüz yaygın tromboz riski"]
                ]
            ),
            make_cloze(
                "Fibrin polimerleri arasında kovalent çapraz bağlar kurarak hemostatik pıhtıyı mekanik olarak stabilize eden enzim Faktör XIIIa enzimidir.",
                "Faktör XIIIa",
                "Trombin tarafından aktive edilen fibrin stabilize edici faktör"
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-20-s07",
        "title": "Primer vs Sekonder Hemostaz Kanama Bulguları",
        "content": "Klinik patolojide bir kanama bozukluğu ile karşılaşıldığında hemostazın hangi basamağının bozuk olduğunu anlamak için fizik muayene bulguları çok değerlidir (Sınav Spotu):\n\n- **Primer Hemostaz Kusurları (Trombosit ve vWF Bozuklukları):**\n  - Trombositopeni, trombosit fonksiyon bozuklukları veya von Willebrand hastalığında görülür.\n  - Kanama tipi: **Mukozal kanamalar** (epistaksis / burun kanaması, diş eti kanaması, menoraji) ve **deride yüzeyel kanamalar** (**peteşi** [1-2 mm], **purpura** [3-5 mm], ekimoz).\n  - Cerrahi veya diş çekimi sonrası kanama hemen başlar.\n- **Sekonder Hemostaz Kusurları (Pıhtılaşma Faktör Eksiklikleri):**\n  - Hemofili A (Faktör VIII), Hemofili B (Faktör IX) veya K vitamini eksikliğinde görülür.\n  - Kanama tipi: **Derin doku kanamaları**, eklem içi kanamalar (**hemartroz**) ve büyük kas içi **hematomlar** karakteristiktir (peteşiler görülmez).\n  - Cerrahi veya travma sonrası kanama hemen değil, saatler sonra başlar (gecikmiş kanama).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Primer Hemostaz Kusuru vs Sekonder Hemostaz Kusuru",
                "Primer Hemostaz Kusuru (Trombosit)",
                "Peteşi, purpura, mukozal kanamalar (diş eti, burun) tipiktir; travma anında hemen kanar.",
                "Sekonder Hemostaz Kusuru (Faktörler)",
                "Hemartroz (eklem içi kanama) ve derin kas hematomları tipiktir; gecikmiş kanama görülür."
            ),
            make_quiz(
                "Diz ekleminde ağrılı şişlik (hemartroz) ve uyluk kası içinde masif derin hematom ile acil servise getirilen bir çocukta öncelikle hangi hemostatik basamakta defekt düşünülmelidir?",
                [
                    {"key": "A", "text": "Sekonder hemostaz (Pıhtılaşma faktör eksikliği, örn. Hemofili)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hemartroz ve derin kas hematomları sekonder hemostaz (koagülasyon faktörleri) bozukluklarının klasik patognomonik bulgusudur."},
                    {"key": "B", "text": "Primer hemostaz (İzole trombositopeni)", "isCorrect": False, "explanation": "Trombositopenide peteşi ve mukozal kanama görülür, hemartroz beklenmez."},
                    {"key": "C", "text": "Geçici arteriyel vazokonstriksiyon fazı", "isCorrect": False, "explanation": "Vazokonstriksiyon hemartroz tablosu yapmaz."},
                    {"key": "D", "text": "Aşırı endotelin-1 salınımı", "isCorrect": False, "explanation": "Endotelin fazlalığı kanama değil vazokonstriksiyon yapar."}
                ]
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-20-s08",
        "title": "Kardiyovasküler Ölümlerin Temeli: Trombozun Klinik ve Patolojik Ağırlığı",
        "content": "Tromboz, modern tıbbın en ölümcül hastalıklarının ortak nihai patolojik zeminidir (Sınav Spotu):\n\n- **İskemi ve Enfarktüs:**\n  - Bir arterin lümeninde gelişen tromboz, o damarın beslediği dokunun arteryel perfüzyonunu keser.\n  - Koroner arterde gelişirse $\\to$ **Miyokard Enfarktüsü (Kalp Krizi)**,\n  - Serebral arterde gelişirse $\\to$ **İskemik İnme (Felç)**,\n  - Mezenterik arterde gelişirse $\\to$ **Bağırsak Kangreni ve Peritonit**.\n- **Tromboemboli Riski:**\n  - Derin venlerde oluşan trombüsler koparak vena cava yoluyla sağ kalbe ve oradan akciğerlere ulaşır $\\to$ **Pulmoner Tromboemboli (PTE)**.\n  - Masif PTE dakikalar içinde akut sağ kalp yetmezliği ve ani kardiyak ölüm yaratır.\n- **Epidemiyoloji:** Dünyadaki her 4 ölümden 1'i trombozla ilişkili bir kardiyovasküler olaydan kaynaklanır.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Tromboz Bölgesi", "Oluşan Klinik Tablo", "Hayati Tehlike Mekanizması"],
                [
                    ["Koroner Arter", "Akut Miyokard Enfarktüsü (STEMI)", "Sol ventrikül nekrozu, kardiyojenik şok, aritmi"],
                    ["Serebral Arter", "Akut İskemik İnme", "Beyin dokusu enfarktüsü ve nörolojik kayıp"],
                    ["Derin Venler (DVT)", "Pulmoner Emboli (PTE)", "Pulmoner arter tıkanması ve ani sağ kalp yetmezliği"],
                    ["Mezenter Arter", "Akut Mezenterik İskemi", "Bağırsak nekrozu, peritonit ve septik şok"]
                ]
            ),
            make_cloze(
                "Alt ekstremite derin venlerinde oluşan bir trombüsün koparak pulmoner dolaşımı tıkaması sonucu gelişen tabloya pulmoner tromboemboli adı verilir.",
                "pulmoner tromboemboli",
                "DVT'nin en korkulan ve hayatı tehdit eden kardiyorespiratuvar komplikasyonu"
            )
        ]
    })

    # Slide 9 - CHECKPOINT 1
    slides.append({
        "id": "k1-20-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Hemostazın Dört Temel Basamağı",
        "content": "Bu checkpointte normal hemostazın dört ardışık evresini ve klinik özelliklerini özetliyoruz:\n\n- **1. Arteriyel Vazokonstriksiyon:** Hasar anında milisaniyeler içinde başlar; sempatik nörojenik refleksler ve endotelden salgılanan **endotelin** ile yürütülür; geçicidir.\n- **2. Primer Hemostaz:** Subendotelyal kollajen ve **vWF** açığa çıkar; trombositler **GpIb** ile yapışır, aktive olur, ADP ve TxA2 salgılar; **GpIIb/IIIa-fibrinojen** köprüleriyle gevşek trombosit tıkacı kurulur.\n- **3. Sekonder Hemostaz:** Subendotelyal **Doku Faktörü (TF)** ve Faktör VIIa kaskadı ateşler; protrombin **trombine** döner; trombin fibrinojeni parçalayarak çözünmeyen **fibrin ağını** örer.\n- **4. Konsolidasyon ve Sınırlama:** **Faktör XIIIa** fibrini kovalent çapraz bağlar; aktin-miyozin pıhtıyı büzer; endotelyal t-PA ve antikoagülanlar pıhtıyı sınırlar.\n- **Klinik Ayrım:** Primer hemostaz defektlerinde peteşi, purpura ve mukozal kanama; sekonder hemostaz defektlerinde **hemartroz ve derin kas hematomları** görülür.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Basamak No", "Basamak Adı", "Kilit Molekül / Reseptör", "Nihai Ürün"],
                [
                    ["1. Basamak", "Arteriyel Vazokonstriksiyon", "Endotelin-1 ve Sempatik refleks", "Geçici damar daralması"],
                    ["2. Basamak", "Primer Hemostaz", "vWF, GpIb, GpIIb/IIIa, ADP, TxA2", "Gevşek Trombosit Tıkacı"],
                    ["3. Basamak", "Sekonder Hemostaz", "Doku Faktörü (TF), Trombin (IIa)", "Fibrin Ağı (Sağlam pıhtı)"],
                    ["4. Basamak", "Stabilizasyon ve Sınırlama", "Faktör XIIIa, t-PA, Trombomodulin", "Çapraz bağlı kalıcı pıhtı ve fibrinoliz"]
                ]
            ),
            make_chain(
                "Hemostazın Büyük Dörtlü Akışı",
                [
                    "1. Vazokonstriksiyon: Endotelin ve refleks ile kan akımı yavaşlatılır.",
                    "2. Primer Tıkaç: Trombositler vWF ve fibrinojenle toplanıp tıkacı kurar.",
                    "3. Fibrin Polimeri: Doku faktörü ve trombin ile tıkacın üzerine fibrin örülür.",
                    "4. Stabilizasyon: Faktör XIIIa kovalent bağ kurar, t-PA pıhtıyı sınırlar."
                ]
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-20-s10",
        "title": "Bölüm Özeti: Hemostaz Evrelerinden Trombosit Biyolojisine Geçiş",
        "content": "Bölüm 1 boyunca hemostaz ve trombozun tanımlarını, dört temel evreyi ve kanama paterni ayrımlarını inceledik:\n\n- **Özet:** Hemostaz vazokonstriksiyon $\\to$ primer tıkaç $\\to$ sekonder fibrin $\\to$ konsolidasyon sıralamasıyla ilerler; bu dengenin bozulması ölümcül kanamalara veya tromboza yol açar.\n- **Sonraki Bölüm (Bölüm 2):** Primer hemostazın asıl hücresel aktörü olan **trombositlerin biyolojisini, alfa ve yoğun granüllerini, membran fosfolipidlerini ve Bernard-Soulier, Glanzmann ile von Willebrand hastalıklarını** detaylarıyla ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Hemostazın ikinci basamağında trombositlerin subendotelyal kollajen ve vWF'ye yapışmasını sağlayan primer yüzey reseptörü hangisidir?",
                "Glikoprotein Ib (GpIb)",
                "Eksikliğinde Bernard-Soulier sendromu görülen trombosit reseptörü"
            ),
            make_quiz(
                "Damar yaralanması sonrasında ilk dakikalarda kanamayı azaltan ancak geçici olan vazomotor yanıtın temel kimyasal aracısı hangisidir?",
                [
                    {"key": "A", "text": "Endotelin-1", "isCorrect": True, "explanation": "Doğru cevap A'dır: Endotelin-1 hasarlı endotelden salgılanarak erken arteriyel vazokonstriksiyonu sağlar."},
                    {"key": "B", "text": "Prostasiklin (PGI2)", "isCorrect": False, "explanation": "PGI2 vazodilatasyon yapar."},
                    {"key": "C", "text": "Nitrik Oksit (NO)", "isCorrect": False, "explanation": "NO damarları genişletir."},
                    {"key": "D", "text": "Heparin", "isCorrect": False, "explanation": "Heparin antikoagülandır, vazomotor etkisi yoktur."}
                ]
            )
        ]
    })

    return slides
