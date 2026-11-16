# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-16-s71",
        "title": "Kanama (Hemoraji) Tanımı ve Temel Mekanizmalar",
        "content": "Kanama (hemoraji), kanın damar sisteminin dışına çıkarak doku içine, vücut boşluklarına veya dış ortama sızmasıdır:\n\n- **İki Temel Patolojik Çıkış Yolu (Sınav Spotu):**\n  1. **Kanama per Rhexin (Rüptür / Yırtılma ile Kanama):** Damar duvarının tam kat mekanik olarak parçalanması veya yırtılmasıdır. Örnek: Bıçak yaralanması, aort anevrizması rüptürü, enfarktüs sonrası miyokard rüptürü.\n  2. **Kanama per Diapedesin (Geçirgenlik / Diapedez ile Kanama):** Damar duvarında makroskobik bir yırtık olmaksızın, kapiller ve venül endotel hücrelerinin aralıklarından eritrositlerin tek tek dokuya sızmasıdır. Örnek: Ağır konjesyon, sepsis, endotoksemi, vaskülit.\n- **Klinik Ağırlık:** Çıkan kanın hacmine, çıkış hızına ve kanamanın gerçekleştiği anatomik konuma bağlı olarak tamamen asemptomatikten dakikalar içinde ölümcül şoka kadar değişir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Rüptürle Kanama (per Rhexin) vs Diapedezle Kanama (per Diapedesin)",
                "Kanama per Rhexin",
                "Damar duvarında tam kat anatomik yırtık vardır; yüksek debili, fışkırıcı ve masif kanama gelişir.",
                "Kanama per Diapedesin",
                "Damar duvarı makroskopik olarak bütündür; endotel aralıklarından eritrositler tek tek dokuya sızar."
            ),
            make_cloze(
                "Damar duvarında makroskobik bir yırtık olmaksızın eritrositlerin endotel aralıklarından dokuya sızmasıyla oluşan kanamaya diapedez kanaması denir.",
                "diapedez",
                "Eritrositlerin endotel arasından mikro-kaçış mekanizması"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-16-s72",
        "title": "Kanamanın Etiyolojisi: Vasküler Hasar Nedenleri",
        "content": "Damar bütünlüğünü bozan etkenler mekanik, dejeneratif, enflamatuvar veya neoplastik olabilir:\n\n- **1. Mekanik Travma:** Kesici-delici alet yaralanmaları, kurşunlanma veya künt travmalar doğrudan damar lümenini açar.\n- **2. Ateroskleroz ve Anevrizmalar:** Aterom plakları elastik arteri zayıflatır; anevrizmatik genişleme (ör. abdominal aort veya Willis poligonu anevrizması) basınca dayanamayarak rüptüre olur.\n- **3. Enflamatuvar Vaskülitler:** ANCA ilişkili vaskülitler veya poliarteritis nodoza damar duvarında nekroz yaparak mikroanevrizmalara ve rüptüre yol açar.\n- **4. Neoplastik Erozyon:** Malign bir tümör (ör. akciğer skuamöz hücreli karsinomu) komşu pulmoner arteri infiltre edip çeperini eritirse masif ölümcül hemoptizi meydana gelir.\n- **5. Kronik Konjesyon ve İskemi:** Dokuda aşırı yükselen hidrostatik basınç zayıflamış mikrodamarları patlatır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Etiyolojik Kategori", "Damar Hasar Mekanizması", "Klasik Klinik Tablo", "Hayati Risk"],
                [
                    ["Anevrizma Rüptürü", "Elastik lamina kaybı ve yüksek basınç rüptürü", "Subaraknoid kanama veya masif retroperiton kanaması", "Çok yüksek (dakikalar içinde şok)"],
                    ["Tümör Erozyonu", "Malign hücrelerin damar duvarını eritmesi", "Akciğer kanserinde masif hemoptizi", "Boğulma ve asfiksi riski"],
                    ["Nekrotizan Vaskülit", "İmmün kompleks veya ANCA kökenli damar nekrozu", "Ciltte nekrotik purpura ve alveolar kanama", "Böbrek ve solunum yetmezliği"],
                    ["Mekanik Travma", "Doğrudan laserasyon ve transeksiyon", "Açık arteriyel kanama", "Hipovolemik şok"]
                ]
            ),
            make_quiz(
                "Aşağıdakilerden hangisi damar duvarının tümör tarafından istila edilip eritilmesi sonucu ortaya çıkan kanama tipine örnektir?",
                [
                    {"key": "A", "text": "Bronş karsinomunun pulmoner arter dalını erozyona uğratmasıyla gelişen masif hemoptizi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tümörlerin komşu damar duvarını eritmesi (erozyon) masif kanamalara neden olur."},
                    {"key": "B", "text": "Tırnak batması sonucu gelişen minimal kızarıklık", "isCorrect": False, "explanation": "Neoplastik damar erozyonu değildir."},
                    {"key": "C", "text": "Güneşte yanınca derinin kızarması", "isCorrect": False, "explanation": "Bu durum hiperemidir, tümöral kanama değildir."},
                    {"key": "D", "text": "Aspirin alınca baş ağrısının geçmesi", "isCorrect": False, "explanation": "Tıbbi tedavi yanıtıdır."}
                ]
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-16-s73",
        "title": "Hemorajik Diyatez: Kanama Eğiliminin Üç Temel Sacayağı",
        "content": "Hemorajik diyatez (kanama eğilimi), minimal bir travmayla veya kendiliğinden (spontan) anormal kanamaların geliştiği klinik durumlar grubudur (Sınav Spotu):\n\n- **Normal Hemostazın Üç Sacayağı:**\n  - Sağlıklı bir hemostatik tıkaç için **damar duvarı (endotel ve bağ dokusu)**, **trombositler** ve **plazma pıhtılaşma faktörleri** kusursuz bir koordinasyonla çalışmalıdır.\n- **Diyatez Sınıflaması:**\n  1. **Damar Duvarı Kırılganlığı Bozuklukları:** Trombosit sayısı ve pıhtılaşma testleri normaldir; sorun damarın mekanik direncindedir.\n  2. **Trombosit Bozuklukları:** Trombosit sayısının düşmesi (kantitatif / trombositopeni) veya trombosit işlevinin bozulması (kalitatif / trombositopati).\n  3. **Koagülasyon Bozuklukları:** Plazmadaki pıhtılaşma faktörlerinin doğuştan veya edinsel eksikliği (hemofililer, K vitamini eksikliği, siroz).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hemorajik Diyatezin Üç Temel Sacayağı",
                [
                    "1. Damar Duvarı: Endotel altı kollajen sağlam olmalı ve damar kasılabilmelidir.",
                    "2. Trombositler: Yeterli sayıda olmalı, yapışmalı (adezyon) ve kümelenmelidir (agregasyon).",
                    "3. Koagülasyon Kaskadı: Fibrinojeni çözünmeyen fibrin ağına çeviren faktörler tam olmalıdır.",
                    "4. Diyatez Kliniği: Bu üçayaktan birinin çökmesi spontan kanama eğilimi yaratır."
                ]
            ),
            make_cloze(
                "Minimal travmayla veya kendiliğinden anormal kanamaya yatkınlık yaratan hastalıklar grubuna hemorajik diyatez denir.",
                "hemorajik diyatez",
                "Klinik kanama eğilimini niteleyen tıbbi şemsiye terim"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-16-s74",
        "title": "Damar Duvarı Kırılganlığı: Skorbüt, Yaşlılık ve Vaskülit",
        "content": "Trombosit ve pıhtılaşma testleri tamamen normal olduğu halde damarın çatlamasıyla kanama gelişen durumlar:\n\n- **1. C Vitamini Eksikliği (Skorbüt - Sınav Spotu):**\n  - Askorbik asit (C vitamini), prokollajen sentezinde prolin ve lizin aminoasitlerinin hidroksilasyonu için zorunlu kofaktördür.\n  - Eksikliğinde kollajen çapraz bağları kurulamaz; kapiller bazal membranı ve perivasküler bağ dokusu aşırı derecede kırılgan hale gelir.\n  - Bulgular: Diş eti kanamaları, perifoliküler peteşiler, tırnak altı kıymık kanamaları (splinter hemoraji).\n- **2. Senil Purpura:** Yaşlılarda dermisteki kollajen ve elastik liflerin atrofisi nedeniyle ellerde ve kollarda minik çarpmalarla geniş morluklar oluşur.\n- **3. Kronik Kortikosteroid Kullanımı (Cushing):** Protein yıkımını artırarak damar duvarını inceltir ve kolay ekimozlara yol açar.\n- **4. İmmün Vaskülitler (Henoch-Schönlein):** Damar duvarında IgA çökmesi ve nekroz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Sağlam Damar Çeperi vs C Vitamini Eksikliği (Skorbüt)",
                "Sağlam Kollojenli Damar",
                "Kollajen lifleri endoteli sıkıca sarar; normal tansiyon veya hafif darbede damar yırtılmaz.",
                "Skorbütlü Kırılgan Damar",
                "Hidroksilasyon kusuru nedeniyle kollajen zayıftır; kapillerler en ufak bası ile çatlar ve kanar."
            ),
            make_quiz(
                "Diş etlerinde kanama ve kıl folikülleri çevresinde noktasal peteşilerle başvuran bir hastada kollajen hidroksilasyon kusuruna bağlı vasküler frajilite saptanıyor. Tanı nedir?",
                [
                    {"key": "A", "text": "Hemofili A", "isCorrect": False, "explanation": "Hemofili A Faktör VIII eksikliğidir, derin eklem kanaması yapar."},
                    {"key": "B", "text": "C vitamini eksikliği (Skorbüt)", "isCorrect": True, "explanation": "Doğru cevap B'dir: C vitamini eksikliği kollajen sentezini bozarak vasküler kırılganlığa ve skorbüte yol açar."},
                    {"key": "C", "text": "Glanzmann trombastenisi", "isCorrect": False, "explanation": "Trombosit agregasyon kusurudur."},
                    {"key": "D", "text": "K vitamini fazlalığı", "isCorrect": False, "explanation": "K vitamini fazlalığı bu tabloyu yapmaz."}
                ]
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-16-s75",
        "title": "Trombositopeni: Sayı Azlığı ve Spontan Kanama Eşiği",
        "content": "Trombositopeni, kanda dolaşan trombosit sayısının 150.000/μL'nin altına düşmesidir:\n\n- **Kritik Eşik Değerleri (Sınav Spotu):**\n  - **50.000 - 100.000/μL:** Ciddi bir travma sonrası kanama süresi uzar; spontan kanama nadirdir.\n  - **20.000 - 50.000/μL:** Minör travmalarla bile belirgin cilt altı morlukları ve kanamalar oluşur.\n  - **< 20.000/μL (Kritik Eşik):** Hiçbir travma olmaksızın **kendiliğinden (spontan) kanamalar** başlar. Deride yaygın peteşi ve purpura, diş eti kanaması ve en tehlikelisi ölümcül **intrakraniyal (beyin) kanama** riski mevcuttur.\n- **Temel Nedenler:**\n  - **Üretim Azlığı:** Aplastik anemi, lösemi, kemik iliği metastazı, B12/folat eksikliği.\n  - **Artmış Yıkım (İmmün):** İmmün Trombositopenik Purpura (ITP - otoantikorlarla dalakta fagositoz), SLE, ilaçlara bağlı yıkım.\n  - **Artmış Tüketim:** Dissemine İntravasküler Koagülasyon (DIC), Trombotik Trombositopenik Purpura (TTP).\n  - **Dalakta Sekestrasyon:** Hipersplenizm (büyümüş dalak trombositlerin %90'ını hapseder).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Trombosit Sayısı", "Klinik Kanama Eğilimi", "Kritik Risk"],
                [
                    ["> 150.000/μL", "Normal hemostaz", "Risk yok"],
                    ["50.000 - 100.000/μL", "Yalnızca majör cerrahi veya ağır travmada artmış kanama", "Düşük risk"],
                    ["20.000 - 50.000/μL", "Hafif çarpmalarda ekimoz, mukoza kanaması", "Orta risk"],
                    ["< 20.000/μL", "Spontan peteşi, purpura, serözal ve mukozal kanama", "Ölümcül intrakraniyal kanama riski"]
                ]
            ),
            make_cloze(
                "Trombosit sayısı 20.000/μL altına indiğinde travma olmaksızın kendiliğinden başlayan kanamalara spontan kanama denir.",
                "spontan",
                "Dış etken veya darbe olmaksızın kendiliğinden gelişen durum"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-16-s76",
        "title": "Trombosit Fonksiyon Bozuklukları (Trombositopatiler)",
        "content": "Kanda trombosit sayısı normal olduğu halde trombositlerin işlev görememesi de aynı kanama tablosunu yaratır:\n\n- **1. Adezyon (Yapışma) Kusuru:**\n  - **Bernard-Soulier Sendromu (Sınav Spotu):** Trombosit yüzeyinde von Willebrand faktörüne (vWF) bağlanan **Glikoprotein Ib (GpIb)** reseptörünün doğuştan eksikliğidir. Trombosit açıkta kalan endotel altı kollajene yapışamaz.\n- **2. Agregasyon (Kümelenme) Kusuru:**\n  - **Glanzmann Trombastenisi (Sınav Spotu):** Trombositlerin birbirine fibrinojen köprüleriyle bağlanmasını sağlayan **Glikoprotein IIb/IIIa (GpIIb/IIIa)** kompleksinin doğuştan eksikliğidir. Tıkaç kümelenemez.\n- **3. Edinsel Trombosit Kusurları:**\n  - **Aspirin Kullanımı:** Siklooksijenaz-1 (COX-1) enzimini geri dönüşümsüz inhibe ederek trombositin tromboksan A2 (TXA2) üretimini bloke eder (trombosit ömrü olan 7-10 gün boyunca kanama zamanı uzar).\n  - **Üremi:** Kronik böbrek yetmezliğinde kanda biriken üremik toksinler trombosit fonksiyonlarını felç eder.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hastalık / İlaç", "Eksik / Bloke Olan Reseptör/Enzim", "Bozulan Trombosit İşlevi", "Klinik Özellik"],
                [
                    ["Bernard-Soulier Sendromu", "Glikoprotein Ib (GpIb) reseptörü", "Endotel altı vWF'ye yapışma (adezyon)", "Dev trombositler, kanama zamanı uzamış"],
                    ["Glanzmann Trombastenisi", "Glikoprotein IIb/IIIa kompleksi", "Trombositlerin birbirine bağlanması (agregasyon)", "Normal trombosit morfolojisi, kümelenme yok"],
                    ["Aspirin", "Siklooksijenaz (COX-1) enzimi", "Tromboksan A2 (TXA2) sentezi", "Geri dönüşümsüz trombosit agregasyon inhibisyonu"],
                    ["Üremi", "Üremik toksin birikimi", "Granül salınımı ve agregasyon", "Diyalizle düzelen edinsel disfonksiyon"]
                ]
            ),
            make_quiz(
                "Trombosit yüzeyindeki Glikoprotein IIb/IIIa (GpIIb/IIIa) kompleksinin konjenital eksikliği sonucu trombositlerin birbirine bağlanamadığı (agregasyon kusuru) kalıtsal hastalık hangisidir?",
                [
                    {"key": "A", "text": "Bernard-Soulier sendromu", "isCorrect": False, "explanation": "Bernard-Soulier GpIb eksikliği ve adezyon bozukluğudur."},
                    {"key": "B", "text": "Glanzmann trombastenisi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Glanzmann trombastenisi GpIIb/IIIa eksikliğine bağlı agregasyon kusurudur."},
                    {"key": "C", "text": "Hemofili A", "isCorrect": False, "explanation": "Faktör VIII eksikliğidir."},
                    {"key": "D", "text": "Von Willebrand hastalığı", "isCorrect": False, "explanation": "vWF eksikliğidir."}
                ]
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-16-s77",
        "title": "Koagülasyon Faktör Eksiklikleri: Hemofililer ve vWH",
        "content": "Pıhtılaşma faktörlerinin eksikliğinde primer trombosit tıkacı oluşur ancak fibrinle sağlamlaştırılamaz (sekonder hemostaz bozukluğu):\n\n- **Trombosit vs Faktör Kanaması Farkı (Sınav Spotu):**\n  - Trombosit kusurları cilt ve mukozada yüzeyel peteşi, purpura ve burun kanaması yaparken;\n  - Faktör eksiklikleri derin dokularda, kas içi hematomlarda ve eklem boşluklarında (**hemartroz**) masif gecikmiş kanamalara yol açar.\n- **Kalıtsal Faktör Bozuklukları:**\n  - **Hemofili A (Klasik Hemofili):** X'e bağlı resesif kalıtılır; **Faktör VIII** eksikliğidir. Erkek çocuklarda spontan diz/dirsek eklem kanamaları (hemartroz) tipiktir.\n  - **Hemofili B (Christmas Hastalığı):** X'e bağlı resesif kalıtılır; **Faktör IX** eksikliğidir; kliniği Hemofili A ile aynıdır.\n  - **Von Willebrand Hastalığı (vWH):** En sık görülen kalıtsal kanama bozukluğudur (otozomal dominant). vWF hem trombosit adezyonunu sağlar hem de Faktör VIII'i kanda stabilize eder; eksikliğinde hem mukozal hem derin kanama görülebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Trombosit Kanaması (Peteşi/Purpura) vs Pıhtılaşma Faktör Kanaması (Hemartroz)",
                "Trombosit Tipi Kanama",
                "Deri ve mukozada 1-2 mm peteşiler, diş eti kanaması, epistaksis; kesi sonrası anında kanar.",
                "Faktör Tipi Kanama (Hemofili)",
                "Derin eklem içi kanamalar (hemartroz), retroperitoneal hematomlar; kesi sonrası kanama saatler sonra başlar."
            ),
            make_cloze(
                "Hemofili A ve B hastalarında özellikle diz gibi büyük eklem boşluklarına kan toplanması tablosuna hemartroz denir.",
                "hemartroz",
                "Eklem içi kanama tıbbi terimi"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-16-s78",
        "title": "Karaciğer Yetmezliği ve K Vitamini Eksikliği: Edinsel Koagülopati",
        "content": "Pıhtılaşma faktör eksikliklerinin büyük çoğunluğu edinseldir ve karaciğerle doğrudan ilişkilidir:\n\n- **Karaciğerin Fabrika Rolü:** Faktör VIII (kısmen endotelde sentezlenir) hariç neredeyse tüm pıhtılaşma faktörleri (Faktör I, II, V, VII, IX, X, XI, XII) karaciğer parankiminde üretilir.\n- **Sirozda Koagülopati:** İleri evre karaciğer yetmezliğinde faktör sentezi durur; protrombin zamanı (PT/INR) ve aPTT belirgin biçimde uzar.\n- **K Vitamini Bağımlı Faktörler (Sınav Spotu):**\n  - Karaciğerde **Faktör II (Protrombin), VII, IX, X** ve antikoagülan Protein C ile Protein S'in aktifleşebilmesi (gama-karboksilasyon) için **K Vitamini** zorunludur.\n  - Yağ malabsorpsiyonunda (safra kanalı tıkanıklığı, çölyak), uzun süreli geniş spektrumlu antibiyotik kullanımında (bağırsak florası ölünce) veya warfarin (Coumadin) tedavisinde K vitamini yetersiz kalır ve hızla kanama eğilimi gelişir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["K Vitamini Bağımlı Pıhtılaşma Proteini", "Fonksiyonu", "Eksikliğinde Sonuç"],
                [
                    ["Faktör II (Protrombin)", "Trombine dönüşerek fibrini oluşturan anahtar enzim", "Koagülasyonun durması"],
                    ["Faktör VII", "Doku faktörü ile birleşen ekstrinsik yolak başlatıcısı", "PT/INR testinde belirgin uzama"],
                    ["Faktör IX", "İntrinsik yolakta Faktör VIII ile tenaz kompleksi kurucusu", "aPTT testinde uzama"],
                    ["Faktör X", "Ortak yolağı başlatan majör faktör", "Fibrin oluşumunun tamamen kilitlenmesi"],
                    ["Protein C ve Protein S", "Faktör Va ve VIIIa'yı inaktive eden doğal antikoagülanlar", "Başlangıçta paradoksal tromboz riski"]
                ]
            ),
            make_quiz(
                "Aşağıdaki koagülasyon faktörlerinden hangisinin karaciğerde fonksiyonel olarak sentezlenebilmesi için K vitamini zorunlu bir kofaktördür?",
                [
                    {"key": "A", "text": "Faktör VII", "isCorrect": True, "explanation": "Doğru cevap A'dır: K vitamini bağımlı faktörler Faktör II, VII, IX ve X'dur (kodlama: 1972)."},
                    {"key": "B", "text": "Faktör VIII", "isCorrect": False, "explanation": "Faktör VIII endotelde sentezlenir, K vitaminine bağımlı değildir."},
                    {"key": "C", "text": "Faktör XIII", "isCorrect": False, "explanation": "K vitamini bağımlı değildir."},
                    {"key": "D", "text": "Fibrinojen (Faktör I)", "isCorrect": False, "explanation": "K vitamini bağımlı değildir."}
                ]
            )
        ]
    })

    # Slide 79 - CHECKPOINT 8
    slides.append({
        "id": "k1-16-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Hemoraji Etiyolojisi ve Kanama Diyatezleri",
        "content": "Bu checkpointte kanama mekanizmalarını, etiyolojik nedenleri ve hemorajik diyatez sınıflamasını özetliyoruz:\n\n- **Mekanizma:** Rüptürle kanama (per rhexin) tam kat damar yırtığıdır; diapedezle kanama (per diapedesin) mikrovasküler sızıntıdır.\n- **Damar Kırılganlığı:** C vitamini eksikliği (skorbüt - kollajen hidroksilasyon kusuru), senil purpura, vaskülitler.\n- **Trombositopeni:** Trombosit <20.000/μL altına inince spontan peteşi, purpura ve intrakraniyal kanama riski doğar.\n- **Trombositopatiler:** Bernard-Soulier (GpIb eksikliği / adezyon kusuru), Glanzmann (GpIIb/IIIa eksikliği / agregasyon kusuru), Aspirin (COX-1 inhibisyonu).\n- **Koagülasyon Bozuklukları:** Hemofili A (Faktör VIII), Hemofili B (Faktör IX) derin kas/eklem kanamaları (hemartroz) yapar.\n- **K Vitamini Bağımlı:** Faktör II, VII, IX, X, Protein C/S. Karaciğer yetmezliğinde veya safra tıkanıklığında çöker.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Bozukluk Grubu", "Klasik Hastalık", "Temel Kusur", "Karakteristik Kanama Tipi"],
                [
                    ["Vasküler Frajilite", "Skorbüt (C Vitamini Eksikliği)", "Kollajen hidroksilasyon defekti", "Perifoliküler peteşiler, diş eti kanaması"],
                    ["Trombositopeni", "İmmün Trombositopeni (ITP)", "Trombosit sayısında kritik düşüş (<20.000)", "Spontan peteşi, purpura, mukoza kanaması"],
                    ["Trombositopati", "Glanzmann Trombastenisi", "GpIIb/IIIa agregasyon kusuru", "Kanama zamanı uzamış, mukokutanöz kanama"],
                    ["Koagülopati", "Hemofili A (Faktör VIII Eksikliği)", "Fibrin oluşum yetersizliği", "Derin eklem içi kanamalar (hemartroz)"]
                ]
            ),
            make_chain(
                "Hemostaz Bozukluğundan Kliniğe Gidiş Basamakları",
                [
                    "1. Bozukluğun Tipi: Vasküler, trombositer veya koagülasyon faktör kökenli.",
                    "2. Trombosit Defekti: Yüzeyel kapiller kaçak $\\to$ Peteşi ve purpura.",
                    "3. Koagülasyon Defekti: Fibrin çatısının kurulamaması $\\to$ Masif hematom ve hemartroz.",
                    "4. Ağır Tablo: İntrakraniyal kanama veya masif iç kanamayla hipovolemik şok."
                ]
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-16-s80",
        "title": "Bölüm Özeti: Kanama Nedenlerinden Morfolojik Tiplere Geçiş",
        "content": "Bölüm 8'de kanamanın vasküler rüptür ve diapedez yollarını, trombosit ve faktör eksikliklerini inceledik:\n\n- **Kritik Kural:** Peteşi ve purpura öncelikle damar veya trombosit sorununu düşündürürken; hemartroz ve derin hematomlar pıhtılaşma faktör kusurlarını işaret eder.\n- **Sonraki Bölüm:** Bir sonraki bölümde kanamanın klinik ve patolojik boyut sınıflamasını — **peteşi (1-2 mm), purpura (3-5 mm), ekimoz (1-2 cm) ve ekimozun enzimatik renk evrimini** — inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Trombosit yüzeyinde bulunan ve endotel altı von Willebrand faktörüne yapışmayı (adezyon) sağlayan Glikoprotein reseptörü hangisidir?",
                "Glikoprotein Ib (GpIb)",
                "Bernard-Soulier sendromunda eksik olan adezyon reseptörü"
            ),
            make_quiz(
                "Diz ekleminde travma olmaksızın spontan masif kanama (hemartroz) gelişen 7 yaşındaki erkek çocukta öncelikle hangi patoloji düşünülmelidir?",
                [
                    {"key": "A", "text": "Faktör VIII eksikliği (Hemofili A)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Erkek çocukta spontan hemartroz Hemofili A veya B'nin klasik prezentasyonudur."},
                    {"key": "B", "text": "Aşırı A vitamini tüketimi", "isCorrect": False, "explanation": "A vitamini hemofili yapmaz."},
                    {"key": "C", "text": "Dizde basit güneş yanığı", "isCorrect": False, "explanation": "Güneş yanığı hemartroz yapmaz."},
                    {"key": "D", "text": "Eritrositlerin aşırı çoğalması (Polisitemi)", "isCorrect": False, "explanation": "Polisitemi primer hemartroz nedeni değildir."}
                ]
            )
        ]
    })

    return slides
