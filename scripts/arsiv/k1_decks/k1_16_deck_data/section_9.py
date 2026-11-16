# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-16-s81",
        "title": "Kanamanın Morfolojik Tipleri ve Boyut Sınıflandırması",
        "content": "Doku içine veya yüzeylere olan kanamalar, kanama odağının milimetrik çapına, morfolojisine ve derinliğine göre kesin sınıflara ayrılır (Sınav Spotu):\n\n- **Boyut Basamakları:**\n  1. **Peteşi:** Çapı **1 ila 2 mm** olan minik, iğne ucu büyüklüğünde punktat kanama odaklarıdır.\n  2. **Purpura:** Çapı **3 ila 5 mm** olan orta büyüklükte kanama lezyonlarıdır.\n  3. **Ekimoz:** Çapı **1 ila 2 cm (veya daha büyük)** olan geniş deri altı hematomlarıdır (halk arasındaki 'morluk').\n  4. **Hematom:** Doku içinde kanın birikerek kitle (tümör benzeri şişlik) oluşturmasıdır.\n  5. **Seröz Boşluk Kanamaları:** Plevra (hemotoraks), perikard (hemoperikardiyum), periton (hemoperiton) ve eklem içi (hemartroz).\n- **Klinik Değer:** Kanamanın boyutu ve dağılımı hekime altta yatan hastalığın türü (trombosit, damar, koagülasyon faktörü) hakkında doğrudan ipucu sağlar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kanama Tipi", "Karakteristik Boyut", "Tipik Anatomik Yerleşim", "Başlıca Patoloji"],
                [
                    ["Peteşi", "1 - 2 mm (noktasal)", "Deri, mukoza, seröz membranlar", "Trombositopeni, C vitamini eksikliği"],
                    ["Purpura", "3 - 5 mm", "Deri, eklemler çevresi", "Vaskülit, artmış vasküler frajilite, travma"],
                    ["Ekimoz", "1 - 2 cm ve üzeri", "Deri altı gevşek bağ dokusu", "Travma, koagülopati, antikoagülan kullanımı"],
                    ["Hematom", "Değişken (kitle oluşturan)", "Kas içi, retroperiton, subkutan", "Majör damar rüptürü, kemik kırığı, hemofili"]
                ]
            ),
            make_quiz(
                "Deri, mukoza veya seröz yüzeylerde izlenen 1-2 mm çapındaki küçük noktasal kanama odaklarına patolojide ne ad verilir?",
                [
                    {"key": "A", "text": "Ekimoz", "isCorrect": False, "explanation": "Ekimoz 1-2 cm çapındaki morluklardır."},
                    {"key": "B", "text": "Peteşi", "isCorrect": True, "explanation": "Doğru cevap B'dir: 1-2 mm çaplı noktasal kanamalara peteşi denir."},
                    {"key": "C", "text": "Hematom", "isCorrect": False, "explanation": "Hematom kitle oluşturan geniş kan birikimidir."},
                    {"key": "D", "text": "Purpura", "isCorrect": False, "explanation": "Purpura 3-5 mm çaplı odaklardır."}
                ]
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-16-s82",
        "title": "Peteşi: 1-2 mm Punktat Kanama Odakları ve Klinik Nedenleri",
        "content": "Peteşiler mikrovasküler kapiller hasarın en doğrudan görsel göstergesidir (Sınav Spotu):\n\n- **Morfoloji:** Çapları 1-2 mm arasında değişen, yuvarlak, basmakla solmayan kırmızı-mor noktasal lezyonlardır.\n- **Tipik Yerleşim:** Deride (özellikle alt bacaklar), ağız mukozasında, konjonktivada ve organların seröz yüzeylerinde (epikard, plevra) yaygın görülür.\n- **Etiyolojik Mekanizmalar:**\n  1. **Trombositopeni (Trombosit Sayı Azlığı):** Sayı <20.000/μL altına indiğinde kapiller endotel aralıkları trombosit tıkacıyla kapatılamaz.\n  2. **Trombosit Fonksiyon Bozuklukları:** Trombositopeni olmasa da agregasyon kusurlarında.\n  3. **C Vitamini Eksikliği (Skorbüt):** Kollajen yetersizliği nedeniyle kapiller duvarı kırılır.\n  4. **Lokal İntravasküler Basınç Patlamaları:** Şiddetli öksürük, kusma veya boğulma sırasında yüz ve boyun kapillerlerinin aniden patlamasıyla periorbital peteşiler oluşur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Peteşi Oluşum Basamakları",
                [
                    "1. Kapiller Zayıflık veya Trombosit Eksikliği: Endotel bariyeri mikro-açılma gösterir.",
                    "2. Eritrositlerin Damar Dışına Sızması: Mikro-diapedez ile interstisyuma eritrosit kaçar.",
                    "3. 1-2 mm Punktat Odak: Doku içinde mikroskopik eritrosit kümesi oluşur.",
                    "4. Basmakla Solmayan Kırmızı Nokta: Cilt muayenesinde kalıcı peteşi saptanır."
                ]
            ),
            make_cloze(
                "Deri ve mukozalarda 1-2 mm çapında punktat kanamalara peteşi denir ve trombositopenide tipiktir.",
                "peteşi",
                "1-2 mm çaplı noktasal kanama odağının tıbbi adı"
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-16-s83",
        "title": "Purpura: 3-5 mm Kanama Lezyonları ve Vaskülit Ayrımı",
        "content": "Purpuralar peteşilerden daha geniş, ekimozlardan daha sınırlı kanama alanlarıdır:\n\n- **Boyut:** Çapları tipik olarak **3 ila 5 mm** arasındadır.\n- **Oluşum Nedenleri:** Peteşi yapan tüm nedenler (trombositopeni, trombositopatiler) purpura da yapabilir; ayrıca travma, vasküler frajilite ve vaskülitler başroldedir.\n- **Klinik Muayenede Kritik Ayrım: Palpabl vs Non-Palpabl Purpura (Sınav Spotu):**\n  - **Non-Palpabl Purpura (Düz Purpura):** Parmakla dokunulduğunda deriden kabarık değildir; tamamen düzdür. Trombositopeni ve koagülasyon bozukluklarında görülür.\n  - **Palpabl Purpura (Ele Gelen Kabarık Purpura):** Parmakla dokunulduğunda lezyon deriden belirgin şekilde kabarıktır. **Lökositoklastik vaskülitin (ör. Henoch-Schönlein purpurası / IgA vasküliti)** patognomonik bulgusudur; damar duvarındaki yoğun nötrofil infiltrasyonu ve fibrinoid nekroz lezyonu kabartır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Non-Palpabl Purpura (Trombositopeni) vs Palpabl Purpura (Vaskülit)",
                "Non-Palpabl Purpura",
                "Lezyon deri seviyesindedir, ele gelmez; saf eritrosit kaçağına bağlıdır (ITP, travma).",
                "Palpabl Purpura",
                "Lezyon ciltten kabarıktır, ele gelir; damar duvarında lökositoklastik vaskülit ve nekrozu gösterir."
            ),
            make_quiz(
                "Cilt muayenesinde alt ekstremitelerde 3-5 mm çapında 'ele gelen kabarık' (palpabl) purpuralar saptanan bir hastada öncelikle hangi patolojik süreç düşünülmelidir?",
                [
                    {"key": "A", "text": "Damar duvarında yangı ve nekrozla seyreden lökositoklastik vaskülit", "isCorrect": True, "explanation": "Doğru cevap A'dır: Palpabl purpura vaskülitin (Henoch-Schönlein vb.) klasik bulgusudur; damar enflamasyonu lezyonu kabartır."},
                    {"key": "B", "text": "İzole C vitamini fazlalığı", "isCorrect": False, "explanation": "C vitamini palpabl lezyon yapmaz."},
                    {"key": "C", "text": "Yalnızca basit güneş çarpması", "isCorrect": False, "explanation": "Güneş çarpması vaskülitik purpura yapmaz."},
                    {"key": "D", "text": "Akut arteriyel tromboz", "isCorrect": False, "explanation": "Büyük arter trombozu solukluk ve gangren yapar."}
                ]
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-16-s84",
        "title": "Ekimoz: 1-2 cm Deri Altı Hematomları ('Morarma')",
        "content": "Ekimoz, halk arasında 'morarma' veya 'çürük' olarak adlandırılan geniş deri altı kanamalarıdır:\n\n- **Boyut:** Çapları tipik olarak **1 ila 2 cm ve üzerindedir**.\n- **Yerleşim ve Yayılım:** Subkutan gevşek bağ dokusu içine bol miktarda eritrositin dökülmesiyle oluşur; doku planları boyunca yerçekimiyle yayılabilir.\n- **Etiyoloji:** En sık künt travmalar (çarpmalar, darbeler) sonucu gelişir. Ancak ileri yaş (senil purpura/ekimoz), kortikosteroid kullanımı, antikoagülan (warfarin, heparin) tedavisi veya pıhtılaşma faktör eksikliklerinde minimal temasla bile dev ekimozlar oluşabilir.\n- **Klinik Takip:** Ekimozun en büyüleyici patolojik özelliği, günbegün değişen ve adli tıpta lezyonun yaşını tayin etmeye yarayan **enzimatik renk dönüşümüdür**.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Parametre", "Peteşi", "Purpura", "Ekimoz"],
                [
                    ["Çap", "1 - 2 mm", "3 - 5 mm", "1 - 2 cm ve üzeri"],
                    ["Ele Gelme", "Ele gelmez (düz)", "Vaskülitte ele gelir (palpabl)", "Hafif ödemli / düz"],
                    ["Derinlik", "Yüzeyel dermis / mukoza", "Dermis kılcal damarları", "Deri altı bağ dokusu (subkutan)"],
                    ["Renk Evrimi", "Genellikle solar", "Zamanla kahverengileşir", "Kırmızı $\\to$ Mavi-yeşil $\\to$ Sarı-kahverengi"]
                ]
            ),
            make_cloze(
                "Deri altı dokusuna kanama sonucu oluşan 1-2 cm çapındaki geniş morluklara patolojide ekimoz adı verilir.",
                "ekimoz",
                "1-2 cm büyüklüğündeki cilt altı morarma lezyonu"
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-16-s85",
        "title": "Ekimozun Enzimatik Renk Döngüsü: Mor $\\to$ Yeşil $\\to$ Sarı",
        "content": "Bir ekimozun günler içinde geçirdiği renk evrimi, hemoglobinin doku makrofajları tarafından aşamalı olarak parçalanmasını yansıtır (Sınav Spotu):\n\n- **1. Aşama: Kırmızı - Mavi - Mor Renk (İlk 1-2 Gün):**\n  - Dokudaki taze eritrositlerin içerdiği **hemoglobin (oksihemoglobin ve deoksihemoglobin)** rengidir.\n- **2. Aşama: Mavi - Yeşil Renk (3-5. Günler):**\n  - Makrofajların lizozomlarındaki **hem oksijenaz** enzimi hem grubunu parçalar; demir ayrılır ve porfirin halkası yeşil renkli **biliverdine (ve bilirubine)** dönüştürülür.\n- **3. Aşama: Altın Sarısı - Kahverengi Renk (5-10. Günler):**\n  - Serbest kalan demir apoferritinle birleşerek **hemosiderin** granüllerine çevrilir. Hemosiderin dokuya sarı-kahverengi renk verir.\n- **4. Aşama: Tam Rezorpsiyon:** Makrofajlar tüm pigmenti drene ettikten sonra deri normal rengine döner.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Erken Ekimoz Rengi vs İyileşen Ekimoz Rengi",
                "Erken Dönem (1-2. Gün)",
                "Hemoglobin molekülü hakimdir; lezyon koyu kırmızı, mor ve mavimsi renktedir.",
                "İyileşme Dönemi (5-7. Gün)",
                "Bilirubin ve hemosiderin pigmentleri hakimdir; lezyon yeşil, sarı ve açık kahverengiye döner."
            ),
            make_quiz(
                "Bir darbe sonrası gelişen ekimozun birkaç gün sonra yeşil-mavi renk almasını sağlayan hemoglobin yıkım ürünü pigment hangisidir?",
                [
                    {"key": "A", "text": "Melanin", "isCorrect": False, "explanation": "Melanin melanositlerce üretilen kahverengi-siyah pigmenttir."},
                    {"key": "B", "text": "Bilirubin (ve biliverdin)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Hem halkasının parçalanmasıyla oluşan biliverdin ve bilirubin yeşil-mavi rengi oluşturur."},
                    {"key": "C", "text": "Lipofuskin", "isCorrect": False, "explanation": "Lipofuskin yaşlanma ve aşınma pigmentidir."},
                    {"key": "D", "text": "Homogentisik asit", "isCorrect": False, "explanation": "Alkaptonüride biriken pigmenttir."}
                ]
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-16-s86",
        "title": "Biyokimyasal Yıkım: Makrofajlar ve Enzimatik Kaskad",
        "content": "Ekimoz alanındaki renk değişiminin hücresel fabrikası doku makrofajlarıdır:\n\n- **Fagositoz:** Damar dışına kaçan milyonlarca eritrosit makrofajlar tarafından yabancı cisim gibi tanınır ve fagozomlara alınır.\n- **Lizozomal Lizis:** Eritrosit zarı eritilir ve hemoglobin serbest kalır.\n- **Hem Oksijenaz Enzimi:** Hem halkasını açar; demiri Fe2+ olarak açığa çıkarır, karbonmonoksit salar ve biliverdin üretir.\n- **Biliverdin Redüktaz:** Biliverdini sarı renkli bilirubine indirger.\n- **Ferritin ve Hemosiderin Sentezi:** Açığa çıkan toksik serbest demir iyonları apoferritin protein kılıfı içine hapsedilerek hemosiderin agregatlarına dönüştürülür.\n- **Klinik Önem:** Büyük bir iç hematom rezorbe olurken kana aşırı miktarda bilirubin salınabilir ve hastada hafif sarılık (sarılık/ikter) gelişebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hemoglobin Parçalanmasının Enzimatik Adımları",
                [
                    "1. Makrofaj Fagositozu: Dokuya sızan ekstravaze eritrositler yutulur.",
                    "2. Hem Parçalanması: Hem oksijenaz enzimi demiri ayırıp biliverdin üretir.",
                    "3. Bilirubin Oluşumu: Biliverdin redüktaz biliverdini sarı-yeşil bilirubine çevirir.",
                    "4. Hemosiderin Depolanması: Demir apoferritin ile bağlanıp altın-kahverengi hemosiderin olur."
                ]
            ),
            make_cloze(
                "Ekimozun son evresinde sarı-kahverengi rengi oluşturan demir depolama kompleksine hemosiderin denir.",
                "hemosiderin",
                "Demir içeren altın-kahverengi doku pigmenti"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-16-s87",
        "title": "Hematom: Doku İçi Kan Kitlesi ve Boyut Yelpazesi",
        "content": "Hematom, kanın doku planları arasına yayılarak kitle etkisi oluşturan birikimidir:\n\n- **Boyut Yelpazesi:** Küçük, önemsiz bir tırnak altı hematomundan (subungual hematom); hastanın ölümüne yol açabilecek 2-3 litrelik dev bir retroperitoneal hematoma kadar uzanır.\n- **Kitle Etkisi (Mass Effect):**\n  - Hematom çevre dokuları sıkıştırır (kompresyon).\n  - Kas içi hematomlarda fasyal kılıf içindeki basınç artışı **kompartman sendromuna** ve kas nekrozuna yol açabilir.\n- **İntrakraniyal Hematomlar (Hayati Aciller - Sınav Spotu):**\n  - **Epidural Hematom:** Travma sonucu arteria meningea media rüptürü; dura ile kafatası arasında arteriyel kan birikimi; ani bilinç kaybı ve herniasyon.\n  - **Subdural Hematom:** Köprü venlerinin (bridging veins) yırtılması; dura ile araknoid arasında venöz kan birikimi; yaşlılarda minör travmayla sinsi gelişebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Epidural Hematom vs Subdural Hematom",
                "Epidural Hematom",
                "Arteria meningea media yırtığıdır; arteriyel yüksek basınçlıdır; saatler içinde hızla herniasyon yapar.",
                "Subdural Hematom",
                "Köprü venlerinin yırtığıdır; venöz yavaş akımlıdır; günler veya haftalar içinde sinsi büyüyebilir."
            ),
            make_quiz(
                "Kafatası travması sonrası temporal kemik kırığına eşlik eden arteria meningea media rüptürü sonucu dura mater ile kafatası kemiği arasında gelişen hematom hangisidir?",
                [
                    {"key": "A", "text": "Subaraknoid kanama", "isCorrect": False, "explanation": "Subaraknoid kanama anevrizma rüptürüyle BOS boşluğuna kanamadır."},
                    {"key": "B", "text": "Epidural hematom", "isCorrect": True, "explanation": "Doğru cevap B'dir: Arteria meningea media yırtığı epidural hematoma neden olur."},
                    {"key": "C", "text": "Kronik subdural hematom", "isCorrect": False, "explanation": "Subdural hematom köprü venlerinin yırtılmasıdır."},
                    {"key": "D", "text": "İntraserebral apse", "isCorrect": False, "explanation": "Enfeksiyöz lezyondur, akut arteriyel hematom değildir."}
                ]
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-16-s88",
        "title": "Vücut Boşluklarına Kanamalar: Hemotoraks, Hemoperikardiyum",
        "content": "Kanamanın vücudun doğal seröz boşluklarına olması mekanik kompresyonla hayatı tehdit eder:\n\n- **1. Hemotoraks:**\n  - Plevral boşluğa kan birikmesidir (aort rüptürü, kot kırığı, toraks travması).\n  - Litrelerce kan plevrada toplanarak akciğeri çökertebilir (kompresyon atelektazisi) ve masif hipovolemik şok yapabilir.\n- **2. Hemoperikardiyum ve Kardiyak Tamponad (Sınav Spotu):**\n  - Perikardiyal keseye kan dolmasıdır (miyokard enfarktüsü sonrası serbest duvar rüptürü, aort diseksiyonu, delici kalp yaralanması).\n  - Perikard esnemeyen fibröz bir kılıftır; içine hızla 150-250 ml kan dolduğunda kalbin diyastolde genişlemesini tamamen engeller (kardiyak tamponad); kalp kan pompalayamaz ve dakikalar içinde ölüm gerçekleşir.\n- **3. Hemoperiton:** Batın boşluğuna kanama (dalak veya karaciğer rüptürü, dış gebelik rüptürü).\n- **4. Hemartroz:** Eklem boşluğuna kanama (hemofili, travma).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Boşluk Kanaması", "Anatomik Alan", "Tipik Neden", "Ölümcül Mekanizma"],
                [
                    ["Hemoperikardiyum", "Perikard boşluğu", "Miyokard rüptürü, aort diseksiyonu", "Kardiyak tamponad ve ani diyastolik arrest"],
                    ["Hemotoraks", "Plevral kavite", "Toraks travması, interkostal arter yırtığı", "Akciğer kompresyonu ve masif kan kaybı"],
                    ["Hemoperiton", "Periton boşluğu", "Dalak laserasyonu, rüptüre ektopik gebelik", "Batın içi gizli masif kanama ve hemorajik şok"],
                    ["Hemartroz", "Sinovyal eklem kavitesi", "Hemofili A/B, eklem içi kırık", "Kronik eklem deformitesi ve ankiloz"]
                ]
            ),
            make_quiz(
                "Akut miyokard enfarktüsünün 5. gününde ventrikül duvarının rüptüre olması sonucu perikard boşluğuna kan dolması ve kalbin sıkışması tablosuna ne ad verilir?",
                [
                    {"key": "A", "text": "Hemoperikardiyum ve kardiyak tamponad", "isCorrect": True, "explanation": "Doğru cevap A'dır: Perikarda kan dolması (hemoperikardiyum) diyastolik dolumu engelleyerek ölümcül kardiyak tamponad oluşturur."},
                    {"key": "B", "text": "Akut plevrit", "isCorrect": False, "explanation": "Plevrit plevra iltihabıdır."},
                    {"key": "C", "text": "Pnömotoraks", "isCorrect": False, "explanation": "Pnömotoraks plevraya hava dolmasıdır."},
                    {"key": "D", "text": "Konjenital aort koarktasyonu", "isCorrect": False, "explanation": "Doğuştan aort darlığıdır."}
                ]
            )
        ]
    })

    # Slide 89 - CHECKPOINT 9
    slides.append({
        "id": "k1-16-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Kanama Tipleri ve Ekimozun Renk Döngüsü",
        "content": "Bu checkpointte kanamanın boyut sınıflamasını, morfolojik tiplerini ve ekimozun enzimatik renk evrimini özetliyoruz:\n\n- **Boyut Skalası:**\n  - Peteşi: 1-2 mm (trombositopeni, C vitamini eksikliği).\n  - Purpura: 3-5 mm (vaskülit, artmış frajilite). Palpabl purpura vaskülit için patognomoniktir.\n  - Ekimoz: 1-2 cm ve üzeri deri altı hematomu ('morluk').\n  - Hematom: Doku içi kitle oluşturan kan göllenmesi.\n- **Ekimozun Renk Basamakları (Enzimatik Parçalanma):**\n  1. Kırmızı-Mavi-Mor: Taze hemoglobin.\n  2. Mavi-Yeşil: Biliverdin ve bilirubin (hem oksijenaz kaskadı).\n  3. Altın Sarısı-Kahverengi: Hemosiderin (demir birikimi).\n- **Hayati Boşluk Kanamaları:** Hemoperikardiyum $\\to$ 200 ml kanla bile kardiyak tamponad ve ani ölüm; Hemotoraks $\\to$ masif kan kaybı ve atelektazi.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Aşama", "Renk", "Sorumlu Molekül / Pigment", "Enzimatik Süreç"],
                [
                    ["1. Gün", "Kırmızı - Mavi - Mor", "Oksihemoglobin ve Deoksihemoglobin", "Eritrositlerin damar dışına çıkışı"],
                    ["3 - 5. Gün", "Mavi - Yeşil", "Biliverdin ve Bilirubin", "Hem oksijenaz ile porfirin halkasının açılması"],
                    ["5 - 10. Gün", "Sarı - Altın Kahverengi", "Hemosiderin", "Demirin apoferritin ile bağlanıp depolanması"]
                ]
            ),
            make_chain(
                "Kanama Boyut ve Renk Döngüsü Özeti",
                [
                    "1. Peteşi (1-2 mm): İğne ucu kanamalar $\\to$ Trombositopeni göstergesi.",
                    "2. Purpura (3-5 mm): Palpabl ise lökositoklastik vaskülit.",
                    "3. Ekimoz (1-2 cm): Subkutan yayılım $\\to$ Hemoglobin $\\to$ Bilirubin $\\to$ Hemosiderin.",
                    "4. Boşluk Kanaması: Hemoperikardiyumda tamponad riski."
                ]
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-16-s90",
        "title": "Bölüm Özeti: Kanama Tiplerinden Klinik Sonuçlara Geçiş",
        "content": "Bölüm 9 boyunca kanamanın boyut tiplerini (peteşi, purpura, ekimoz), makrofaj metabolizmasını ve seröz boşluk kanamalarını tamamladık:\n\n- **Adli ve Patolojik Önem:** Ekimoz renklerinin sırası yaralanmanın gününü saptamada, kanamanın boyutu ise primer hemostaz ile sekonder hemostazı ayırt etmede paha biçilmezdir.\n- **Sonraki Bölüm:** Final bölümümüzde kanama miktarının (%20 kuralı), kanama lokalizasyonunun (deri altı vs beyin) önemini ve **dış kanama ile iç hematom arasındaki demir farkını** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Deri ve mukozalardaki 3-5 mm çapındaki kanama lezyonlarına ne ad verilir?",
                "Purpura",
                "Peteşi ile ekimoz arasındaki orta boy kanama odağı"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi ekimozun enzimatik renk değişiminde rol oynayan ilk kilit enzimdir?",
                [
                    {"key": "A", "text": "Hem oksijenaz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hem oksijenaz hem halkasını açarak demiri ayırır ve biliverdin üretir."},
                    {"key": "B", "text": "Amilaz", "isCorrect": False, "explanation": "Karbonhidrat sindirim enzimidir."},
                    {"key": "C", "text": "Pepsin", "isCorrect": False, "explanation": "Mide proteazıdır."},
                    {"key": "D", "text": "DNA polimeraz", "isCorrect": False, "explanation": "Replikasyon enzimidir."}
                ]
            )
        ]
    })

    return slides
