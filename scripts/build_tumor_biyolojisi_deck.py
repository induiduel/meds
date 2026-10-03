# -*- coding: utf-8 -*-
"""
scripts/build_tumor_biyolojisi_deck.py
Generates full 24-slide high-yield interactive learning deck for:
Prof. Dr. Hikmet Keleş - Tümör Biyolojisi ve Terminolojisi
Replaces the old 4-slide stub with an authentic, deep, %500 comprehensive deck.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
CHUNK8_PATH = 'src/data/study_questions/chunk_8.json'
CHUNK9_PATH = 'src/data/study_questions/chunk_9.json'

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

slides = [
    {
        "slideNumber": 1,
        "title": "Neoplazi Kavramı ve Kanser Biyolojisine Giriş",
        "subtitle": "Willis neoplazi tanımı, otonom kontrolsüz hücre çoğalması ve temel terminoloji.",
        "badge": "Giriş & Tanım",
        "badgeColor": "accent",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Neoplazi, uyaran ortadan kalksa bile durmaksızın devam eden anormal bir doku kitlesidir. Kanser kelimesi ise tüm malign neoplazmları kapsayan ortak tıbbi ifadedir.",
            "note": "Willis tanımı neoplazinin otonom doğasını ve konağın regülasyon mekanizmalarından bağımsızlığını en net özetleyen tanımdır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Neoplazi ve Kanser: Tanım ve Temel Felsefe
**Neoplazi** (Yunanca *neo* = yeni, *plasis* = oluşum / büyüme), normal doku homeostazından bağımsız olarak gelişen, konağın büyüme kontrol sinyallerine yanıt vermeyen ve kontrolsüz proliferasyon gösteren patolojik doku kitlesidir.

Onkoloji patolojisinde klasik kabul edilen **Rupert Willis Tanımı** amfide özellikle vurgulanmıştır:
> 💡 **Willis Neoplazi Tanımı:** *'Neoplazm, büyümesi normal dokununkinden aşırı ve koordinesiz olan, bu anormalliği başlatan uyaran ortadan kalktıktan sonra bile aynı aşırı biçimde sürmeye devam eden anormal bir doku kitlesidir.'*

#### Neoplazinin Temel Karakteristikleri:
1. **Otonomluk:** Konak organizmanın kontrol mekanizmalarına (kontakt inhibisyonu, apoptoz sinyalleri) boyun eğmez.
2. **Kalıtsallık:** Hücre bölünmesi sırasında kazanılmış genetik ve epigenetik hasar yavru hücrelere aktarılır.
3. **Parazitik Doğa:** Kendi kanlanmasını (anjiyogenez) konakçıdan sağlar ve konakçının besin kaynaklarını tüketerek kaşeksiye yol açabilir.

> 🔴 **Sınav Tuzağı:** ==red:Hiperplazi veya hipertrofi gibi adaptasyon süreçleri uyarana bağımlıdır; uyaran ortadan kalkınca geriler. Neoplazi ise uyaran kesilse bile kalıcı ve ilerleyicidir!==

Tüm neoplazmlar biyolojik davranışlarına göre iki ana gruba ayrılır:
- **Benign (İyi Huylu) Tümörler:** Lokalize kalır, çevre dokuyu iterek büyür (kapsüllü), metastaz yapmaz.
- **Malign (Kötü Huylu) Tümörler (Kanser):** Çevre dokuları infiltre ve destrükte eder, kan/lenf yoluyla uzak organlara metastaz yapma potansiyeline sahiptir.""",
        "spotPearls": [
            "🔴 Willis neoplazm tanımının kilit noktası: Anormal çoğalmayı başlatan **uyaran kesilse dahi** büyümenin durmaksızın devam etmesidir.",
            "🔵 ==blue:Adaptif hiperplazi ile neoplazi arasındaki en temel fark, hiperplazinin uyarana bağımlı olması ve uyaran kalkınca regresyon göstermesidir.==",
            "⚡ Benign neoplazmlar kural olarak lokalize kalırken; malign neoplazmlar çevre dokuyu infiltre eder ve metastaz yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Willis Tanımı", "text": "Uyaran kalksa bile süren aşırı, koordinesiz otonom büyüme."},
                {"label": "Klonalite", "text": "Tek bir genetik olarak dönüşmüş kök hücreden köken alma (monoklonalite)."},
                {"label": "Davranış", "text": "Benign (lokal, ekspansif) vs Malign (infiltratif, metastatik)."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-1-1",
                "front": "Neoplaziyi adaptif doku büyümelerinden (hiperplazi) ayıran en belirleyici biyolojik özellik nedir?",
                "back": "Tümörleşmeyi başlatan uyarıcı faktör ortadan kalksa bile büyümenin özerk ve durmaksızın devam etmesidir (Willis tanımı).",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu ilkeyi özellikle vurguladı."
            },
            {
                "id": "tb-fc-1-2",
                "front": "Kanser kelimesinin tıbbi patolojideki tam karşılığı nedir?",
                "back": "Malign (kötü huylu) neoplazmların tümüne verilen genel isimdir.",
                "facultyNote": "Hipokrat tarafından yengeç benzeri kolları ve yayılımı nedeniyle carcinos olarak adlandırılmıştır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-1",
            "question": "Patolojide neoplazmı hiperplazi, hipertrofi ve metaplazi gibi hücresel adaptasyon süreçlerinden ayıran en temel biyolojik özellik aşağıdakilerden hangisidir?",
            "options": [
                "A) Hücrelerde sitoplazmik granülasyon artışı",
                "B) Başlatan uyaran ortadan kalksa bile büyümenin otonom biçimde devam etmesi",
                "C) Daima inflamatuar mononükleer hücre infiltrasyonu içermesi",
                "D) Yalnızca yaşlı bireylerde ortaya çıkması",
                "E) Sadece mezenkimal dokulardan köken alması"
            ],
            "answer": "B",
            "explanation": "Neoplazinin kardinal özelliği Rupert Willis tanımında belirtildiği üzere, uyaran ortadan kalksa bile otonom ve aşırı biçimde çoğalmayı sürdürmesidir. Adaptif süreçler ise uyaran kesildiğinde geriler.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 2,
        "title": "Tümörlerin Klonal Kökeni ve Heterojenite",
        "subtitle": "Tümörlerin monoklonal başlangıcı, klonal genişleme ve subklon seleksiyonu.",
        "badge": "Tümör Biyolojisi",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bütün bir tümör kitlesi başlangıçta tek bir genetik transformasyona uğramış ata hücreden ürer; yani kanser monoklonal başlar ancak zamanla poliklonal heterojenite kazanır.",
            "note": "X kromozomu inaktivasyonu (G6PD izozimleri) çalışmaları tümörlerin monoklonal orijinini ispatlayan altın standarttır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Klonalite ve Tümör Heterojenitesi
İnsan neoplazmlarının büyük çoğunluğu **monoklonal** kökenlidir. Bu kavram, milyarlarca hücreden oluşan devasa bir tümör kitlesinin başlangıçta tek bir somatik hücrenin genomundaki kritik mutasyonlar sonucu türediğini ifade eder.

#### Monoklonalitenin Kanıtlanması:
- **G6PD (Glukoz-6-Fosfat Dehidrogenaz) İzozim Analizi:** Kadınlarda Lyon hipotezine göre embriyonik dönemde rastgele tek bir X kromozomu inaktive olur. Heterozigot kadınlarda normal doku hem A hem B izozimini içerirken (poliklonal), tümör dokusu yalnızca A ya da yalnızca B izozimi taşır (monoklonal).
- **İmmünoglobulin ve T-Hücre Reseptör (TCR) Gen Düzenlenimi:** Lenfomalarda tüm hücrelerin aynı V-D-J gen dizilimine sahip olması monoklonaliteyi ispatlar.

#### Klonal Evrim ve Tümör Heterojenitesi (Nowell Modeli):
1. **Başlangıç:** Tek bir hücrede onkojenik mutasyon gelişir.
2. **Klonal Genişleme:** Bu hücre çoğalarak birincil klonu oluşturur.
3. **Genomik İnstabilite:** Hızlı bölünme sırasında yeni rastlantısal mutasyonlar birikir.
4. **Subklonların Belirmesi:** Farklı özelliklere sahip (daha hızlı bölünen, kemoterapiye dirençli, metastaz yeteneği olan) alt klonlar ortaya çıkar.
5. **Darwinyen Seleksiyon:** Kemoterapi veya radyoterapi uygulandığında hassas hücreler ölürken, dirençli subklon sağ kalarak nükse yol açar.

> 🔴 **Sınav Tuzağı:** ==red:Tümör başlangıçta monoklonaldir; ancak klinik olarak saptanabilir boyuta (1 cm³ ~ 10⁹ hücre) ulaştığında yüksek derecede genetik olarak heterojendir!== Bu durum kanser tedavisindeki direncin ve nüksün temel sebebidir.""",
        "spotPearls": [
            "🔴 Kanser başlangıçta tek bir hücreden köken aldığı için **monoklonaldir**; ancak zamanla subklonlar türeyerek **tümör heterojenitesi** oluşur.",
            "🔵 ==blue:Kadınlarda X kromozom inaktivasyonu (G6PD izoenzim paterni) analizi tümörlerin monoklonal kökenini ispatlamak için kullanılan klasik laboratuvar yöntemidir.==",
            "⚡ Kemoterapiye direnç gelişimi, tümör içerisindeki dirençli subklonların Darwinyen seleksiyonu ile açıklanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Monoklonalite", "text": "Tek bir transforme hücreden orijin alma kanıtı."},
                {"label": "G6PD Analizi", "text": "X inaktivasyonu ile monoklonal kökenin tespiti."},
                {"label": "Subklon Gelişimi", "text": "Kemoterapi direnci ve metastaz kabiliyetinin kazanılması."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-2-1",
                "front": "Tümörlerin tek bir hücreden köken aldığını (monoklonalite) deneysel olarak ispatlayan klasik genetik yöntem nedir?",
                "back": "Heterozigot kadınlarda X kromozomuna bağlı G6PD izoenzim analizi veya lenfositlerde B/T reseptör gen yeniden düzenlenimidir.",
                "facultyNote": "TUS sınavlarında klonalite sorularında G6PD sık sorulan bir patoloji klasiğidir."
            },
            {
                "id": "tb-fc-2-2",
                "front": "Başlangıçta monoklonal olan bir tümörün zamanla kemoterapiye direnç kazanmasını açıklayan mekanizma nedir?",
                "back": "Genomik instabilite sonucu subklonların türemesi ve tümör heterojenitesi (Nowell klonal seleksiyon modeli).",
                "facultyNote": "Tümör büyüdükçe homojenliğini kaybeder."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-2",
            "question": "Bir tümör dokusunun poliklonal bir reaktif hiperplazi mi yoksa monoklonal bir neoplazm mı olduğunu ayırt etmek amacıyla heterozigot kadınlarda aşağıdakilerden hangisinin analizi altın standart kabul edilir?",
            "options": [
                "A) Mitokondriyal DNA mutasyon oranı",
                "B) X kromozomuna bağlı G6PD izozim dağılımı",
                "C) Serum albümin elektroforezi",
                "D) Hücre içi sodyum-potasyum ATPaz aktivitesi",
                "E) Telomeraz enzim boyutu"
            ],
            "answer": "B",
            "explanation": "Heterozigot kadınlarda embriyonik dönemde tek bir X inaktive olduğundan reaktif lezyonlar mikst G6PD izozimleri taşır (poliklonal); neoplazmlar ise tek bir hücreden ürediği için sadece tek bir G6PD izozimi gösterir (monoklonal).",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 3,
        "title": "Tümörün İki Temel Bileşeni: Parankim ve Stroma",
        "subtitle": "Klonojenik parankimal hücreler ile destekleyici konak stroması ve desmoplazi.",
        "badge": "Morfoloji & Doku",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bütün neoplazmlar iki parçadan oluşur: Biri çoğalan tümör hücrelerinin oluşturduğu parankim, diğeri ise konaktan devşirilen damar ve bağ dokusu stromasıdır.",
            "note": "Tümörün adını, davranışını ve biyolojisini parankim belirler; ancak büyümesini ve beslenmesini stroma sağlar.",
            "emphasisType": "pearl"
        },
        "synthesisNarrative": """### Parankim ve Stroma Mimarisi
Tüm neoplazmlar, mikroskopik olarak iki temel komponentin birlikteliğinden oluşur:
1. **Parankim (Tümör Parankimi):**
   - Neoplastik, transforme olmuş hücrelerden oluşur.
   - Tümörün biyolojik davranışını (benign/malign), diferansiyasyonunu ve ismini belirleyen ana bileşendir.
2. **Reaktif Stroma:**
   - Tümör hücrelerinin çevre dokudan 'rehin aldığı' neoplastik olmayan destek dokusudur.
   - Kan damarları, lenfatikler, fibroblastlar, miyofibroblastlar ve inflamatuar hücreleri içerir.
   - Tümörün beslenmesi, atıklarının uzaklaştırılması ve parankimal büyümesi stromanın desteğine muhtaçtır.

#### Desmoplazi (Skirröz Yanıt):
Bazı kanser türlerinde tümör parankim hücreleri çevre stromadaki fibroblastları aşırı uyararak bol miktarda dens, aselüler kollajen sentezletir. Bu stromal yanıta **desmoplazi** denir.
- Makroskopik olarak kitleye taş gibi sert, tahta kıvamı verir (*skirröz karsinom*).
- Klasik örnekleri: İnvaziv duktal meme karsinomu ve pankreas duktal adenokarsinomudur.

> 🔴 **Sınav Tuzağı:** ==red:Desmoplazi tümör hücrelerinin kendisi değil; konak bağ dokusu fibroblastlarının tümör etkisiyle ürettiği kollajenöz stroma artışıdır!==

#### Tümör-Stroma Çapraz İletişimi:
Tümör hücreleri VEGF, bFGF salgılayarak stromadan **anjiyogenez** (yeni damar yapımı) talep eder. Karşılığında stromal hücreler de PDGF, HGF ve IGF-1 gibi büyüme faktörleri salgılayarak tümör hücresinin hayatta kalmasını destekler.""",
        "spotPearls": [
            "🔴 Tümörün adını ve biyolojik tabiatını **parankim** belirler; yaşamasını ve büyümesini ise **stroma** sağlar.",
            "🔵 ==blue:İnvaziv duktal meme kanseri ve pankreas kanserinde lezyonun taş gibi sert olmasına yol açan aşırı fibröz stroma yanıtına desmoplazi (skirröz stroma) denir.==",
            "⚡ Tümörler 1-2 mm çapa ulaştıktan sonra stromal anjiyogenez (VEGF indüksiyonu) olmaksızın daha fazla büyüyemez."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Parankim", "text": "Transforme klonal neoplastik hücre kitlesi."},
                {"label": "Stroma", "text": "Konak kökenli bağ dokusu, damarlar ve bağışıklık hücreleri."},
                {"label": "Desmoplazi", "text": "Yoğun kollajen senteziyle giden skirröz stromal sertleşme."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-3-1",
                "front": "Tümör parankim hücrelerinin stromal fibroblastları uyararak yoğun kollajen birikimine ve sert kıvama yol açtığı reaksiyona ne ad verilir?",
                "back": "Desmoplazi (Skirröz tümör yapısı).",
                "facultyNote": "Meme ve pankreas kanserlerinde palpasyondaki taş sertliğinin nedenidir."
            },
            {
                "id": "tb-fc-3-2",
                "front": "Tümörün adını, köken aldığı hücre tipini ve histolojik derecesini belirleyen bileşen hangisidir?",
                "back": "Tümör parankimidir.",
                "facultyNote": "Stroma destekleyicidir; parankim ise asıl neoplastik bileşendir."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-3",
            "question": "İnvaziv duktal meme karsinomunda kitlenin palpasyonda taş sertliğinde hissedilmesine neden olan, neoplastik hücrelerin fibroblastları stimüle etmesi sonucu gelişen yoğun kollajenöz stroma reaksiyonu aşağıdakilerden hangisidir?",
            "options": [
                "A) Anaplazi",
                "B) Desmoplazi",
                "C) Metaplazi",
                "D) Koryostomi",
                "E) Displazi"
            ],
            "answer": "B",
            "explanation": "Desmoplazi, tümör hücrelerinin salgıladığı büyüme faktörleri ile çevre stromada aşırı kollajen ve fibröz doku birikimidir; tümöre skirröz (sert) özellik kazandırır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 4,
        "title": "Benign Mezenkimal ve Epitelyal Tümörlerin İsimlendirilmesi",
        "subtitle": "'-om' eki kuralı, adenom, papillom, kistadenom ve polip kavramları.",
        "badge": "Terminoloji",
        "badgeColor": "green",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Benign tümörlerde genel kural köken aldığı hücrenin sonuna '-om' (-oma) eki getirmektir. Yağ dokusundan lipom, kıkırdaktan kondrom, düz kastan leiyomiyom.",
            "note": "Epitelyal benign tümörlerde ise glandüler yapı yapıyorsa adenom, parmaksı çıkıntılar yapıyorsa papillom denir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Benign Tümör Terminolojisi Kuralları
Patolojide benign (iyi huylu) neoplazmların adlandırılmasında genel kural:
**Köken alınan hücre / doku tipi + '-om' (-oma) soneki**

#### 1. Mezenkimal Benign Neoplazmlar:
- Fibröz doku → **Fibrom**
- Yağ dokusu → **Lipom**
- Kıkırdak doku → **Kondrom**
- Kemik doku → **Osteom**
- Düz kas dokusu → **Leiyomiyom** (Örn: Uterusta en sık görülen tümör / miyom)
- Çizgili kas dokusu → **Rabdomiyom** (Örn: Kalpte tüberöz skleroz ile ilişkili)
- Kan damarı endoteli → **Hemanjiom**
- Lenfatik damarlar → **Lenfanjiom**
- Meninksler → **Meningiyom**

#### 2. Epitelyal Benign Neoplazmlar:
Epitel kaynaklı benign tümörler hücre tipine ve mikroskopik/makroskopik büyüme paternine göre adlandırılır:
- **Adenom:** Bez (gland) yapısı oluşturan veya glandüler epitelden köken alan benign epitel tümörüdür (Örn: Tiroid foliküler adenomu, kolon tübüler adenomu).
- **Papillom:** Epitel yüzeyinden lümene doğru parmaksı veya siğilimsi çıkıntılar (papiller) oluşturan benign epitel tümörüdür (Örn: Larinks papillomu, mesane ürotelyal papillomu).
- **Kistadenom:** İçi sıvı dolu kistik boşluklar oluşturan glandüler benign tümördür (Örn: Over kistadenomu).
- **Polip:** Mukozal yüzeyden lümene doğru uzanan, saplı veya sapsız makroskopik kitle görüntüsüdür. Benign adenomatoz olabileceği gibi inflamatuar da olabilir.

> 🔴 **Sınav Tuzağı:** ==red:Polip bir histolojik tanı değil; makroskopik bir morfolojik terimdir! Bir polip biyopsisinden benign adenom çıkabileceği gibi invaziv karsinom da çıkabilir.===""",
        "spotPearls": [
            "🔴 Düz kas kaynaklı benign tümör **leiyomiyom**; çizgili kas kaynaklı benign tümör ise **rabdomiyom** olarak adlandırılır.",
            "🔵 ==blue:Bez (glandüler) yapısı oluşturan benign epitelyal tümörlere 'Adenom', parmaksı çıkıntılar oluşturanlara 'Papillom' denir.==",
            "⚡ Polip mikroskobik bir tanı değil, mukozadan lümene uzanan makroskopik bir lezyon tarifidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Mezenkimal -om", "text": "Lipom, Kondrom, Osteom, Leiyomiyom."},
                {"label": "Adenom", "text": "Bez epiteli veya gland yapan benign neoplazm."},
                {"label": "Papillom", "text": "Parmaksı, vellöz parankimal uzantılar."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-4-1",
                "front": "Uterus miyometriyumundan köken alan ve düz kas hücrelerinden oluşan benign neoplazmın tıbbi adı nedir?",
                "back": "Leiyomiyom.",
                "facultyNote": "Çizgili kas kaynaklı olanı ise rabdomiyomdur."
            },
            {
                "id": "tb-fc-4-2",
                "front": "Lümene doğru parmaksı, fırçamsı projeksiyonlar yaparak büyüyen benign epitelyal neoplazmlara ne ad verilir?",
                "back": "Papillom.",
                "facultyNote": "HPV ilişkili skuamöz lezyonlarda sıktır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-4",
            "question": "Aşağıdaki eşleştirmelerden hangisinde benign tümör ve köken aldığı doku tipi YANLIŞ verilmiştir?",
            "options": [
                "A) Lipom — Yağ dokusu",
                "B) Kondrom — Kıkırdak dokusu",
                "C) Leiyomiyom — Çizgili kas dokusu",
                "D) Hemanjiom — Kan damarı",
                "E) Adenom — Glandüler epitel"
            ],
            "answer": "C",
            "explanation": "Leiyomiyom düz kas dokusunun benign tümörüdür. Çizgili kas dokusunun benign tümörü ise 'Rabdomiyom'dur.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 5,
        "title": "Malign Tümör Terminolojisi: Karsinom ve Sarkom Ayrımı",
        "subtitle": "Karsinom (epitelyal malignite) ve Sarkom (mezenkimal malignite) temel prensipleri.",
        "badge": "Terminoloji",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Epitelden çıkan malign tümörlere karsinom, mezenkimden çıkan malign tümörlere sarkom denir. Bu iki grup yayılım yolları ve klinik davranışları açısından tamamen zıttır.",
            "note": "Karsinomlar kural olarak lenfatik yolla yayılırken; sarkomlar ağırlıklı olarak hematojen yolla yayılır.",
            "emphasisType": "exam_trap"
        },
        "synthesisNarrative": """### Karsinom vs Sarkom: Temel İsimlendirme ve Biyoloji
Malign neoplazmlar köken aldıkları embriyonik doku yaprağına göre iki ana sınıfa ayrılır:

#### 1. Karsinomlar (Epitelyal Malign Neoplazmlar):
Ektoderm, endoderm veya mezodermden köken alan herhangi bir epitel dokusunun malign tümörüdür. Tüm kanserlerin %85-90'ını oluştururlar (en sık görülen grup).
- **Skuamöz Hücreli Karsinom (Yassı Epitelyal Karsinom):** Çok katlı yassı epitele diferansiye olan, intersellüler köprüler ve keratin incileri (keratin pearls) oluşturan karsinomdur (Deri, akciğer, larinks, özofagus, serviks).
- **Adenokarsinom:** Glandüler (bez) yapıları oluşturan veya müsin üreten malign epitelyal tümördür (Mide, kolon, meme, prostat, endometriyum, akciğer adenokarsinomu).
- **Ürotelyal Karsinom (Transizyonel Hücreli Karsinom):** İdrar yolları transizyonel epitelinden köken alır (Böbrek pelvisi, üreter, mesane).

#### 2. Sarkomlar (Mezenkimal Malign Neoplazmlar):
Embriyonik mezoderm kaynaklı mezenkimal (destek) dokulardan türeyen malign neoplazmlardır.
- Fibröz doku → **Fibrosarkom**
- Yağ dokusu → **Liposarkom** (lipoblastlar içerir)
- Kıkırdak dokusu → **Kondrosarkom**
- Kemik dokusu → **Osteosarkom** (neoplastik osteoid üretimi şarttır)
- Düz kas dokusu → **Leiyomiyosarkom**
- Çizgili kas dokusu → **Rabdomiyosarkom** (çocukluk çağının en sık yumuşak doku sarkomu)
- Kan damarları → **Anjiyosarkom**

> 🔴 **Sınav Tuzağı:** ==red:Karsinomlar ağırlıkla ileri yaşlarda görülür ve ilk olarak bölgesel LENFATİK yolla yayılır. Sarkomlar ise gençlerde daha sıktır ve ilk olarak HEMATOJEN yolla (özellikle akciğere) metastaz yapar!===""",
        "spotPearls": [
            "🔴 Epitelyal malign tümörler **Karsinom**, mezenkimal malign tümörler **Sarkom** olarak adlandırılır.",
            "🔵 ==blue:Karsinomlar kural olarak ilk önce bölgesel LENF NODLARINA (lenfojen) metastaz yaparken; sarkomlar HEMATOJEN yolla doğrudan akciğere metastaz yapar.==",
            "⚡ Çocukluk çağının en sık görülen yumuşak doku sarkomu **Rabdomiyosarkom**dur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Karsinom", "text": "Epitel kaynaklı (Adenokarsinom, Skuamöz hücreli karsinom). Lenfojen yayılım."},
                {"label": "Sarkom", "text": "Mezenkimal kaynaklı (Osteo-, Lipo-, Rabdomiyo-sarkom). Hematojen yayılım."},
                {"label": "Osteosarkom Şartı", "text": "Neoplastik hücrelerin doğrudan kemik matriksi/osteoid üretmesi."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-5-1",
                "front": "Glandüler diferansiasyon gösteren veya müsin üreten malign epitelyal tümöre ne ad verilir?",
                "back": "Adenokarsinom.",
                "facultyNote": "GİS, meme ve prostatta en sık görülen karsinom tipidir."
            },
            {
                "id": "tb-fc-5-2",
                "front": "Karsinomlar ile sarkomlar arasındaki en tipik metastaz yolu farkı nedir?",
                "back": "Karsinomlar öncelikle lenfatik yolla bölgesel lenf nodlarına yayılırken; sarkomlar öncelikle hematojen yolla (özellikle akciğere) yayılır.",
                "facultyNote": "Komite ve TUS sınavlarının değişmez soru kalıbıdır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-5",
            "question": "Patoloji laboratuvarına gönderilen bir biyopside tümör hücrelerinin intersellüler köprüler ve keratin incileri oluşturduğu saptanmıştır. Bu tümörün en olası histopatolojik tanısı aşağıdakilerden hangisidir?",
            "options": [
                "A) Adenokarsinom",
                "B) Skuamöz hücreli karsinom",
                "C) Fibrosarkom",
                "D) Leiyomiyosarkom",
                "E) Rabdomiyosarkom"
            ],
            "answer": "B",
            "explanation": "İntersellüler köprüler ve keratin incisi (horn pearl) oluşumu, çok katlı yassı epitele diferansiasyonun kesin kanıtıdır ve Skuamöz Hücreli Karsinomun (Yassı Epitelyal Karsinom) patognomonik morfolojik bulgusudur.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 6,
        "title": "Terminolojideki Kritik İstisnalar: '-om' İle Biten Malign Tümörler",
        "subtitle": "Melanom, Lenfoma, Seminom, Mezotelyoma, Hepatom ve Gliom tuzakları.",
        "badge": "Sınav Tuzağı",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Burası sınavların en sevdiği yerdir: Sonu '-om' ile bittiği halde ASLA benign olmayan, son derece malign olan lezyonlar vardır. Melanom, Lenfoma, Seminom, Mezotelyoma!",
            "note": "Bu kelimeleri gördüğünüzde adındaki '-oma' ekine aldanıp iyi huylu demeyin; hepsi öldürücü malignitelerdir.",
            "emphasisType": "exam_trap"
        },
        "synthesisNarrative": """### Patoloji Terminolojisinin Büyük İstisnaları
Kural olarak sonuna '-om' eki alan neoplazmlar benign kabul edilirken, tarihi ve geleneksel kullanımlar nedeniyle adında '-om' taşıyan fakat **YÜZDE YÜZ MALİGN** olan tümörler mevcuttur.

#### Mutlaka Ezberlenmesi Gereken Malign İstisnalar:
1. **Melanom (Malign Melanom):** Melanositlerin malign tümörüdür. 'Melanosarkom' veya 'Melanokarsinom' denmez; sadece Melanom denir ve son derece agresiftir.
2. **Lenfoma:** Lenfositlerin malign neoplazmıdır (Hodgkin ve Non-Hodgkin Lenfoma). Tıpta 'benign lenfoma' diye bir kavram YOKTUR.
3. **Seminom:** Testisin germ hücreli malign tümörüdür (Overdeki karşılığı Disgerminomdur).
4. **Mezotelyoma (Malign Mezotelyoma):** Plevra, periton veya perikard mezotel hücrelerinin asbest maruziyeti ile tetiklenen agresif malign neoplazmıdır.
5. **Hepatom (Hepatosellüler Karsinom - HCC):** Karaciğer parankiminin primer malign karsinomudur.
6. **Miyelom (Multipl Miyelom):** Plazma hücrelerinin kemik iliğini tutan monoklonal malign neoplazmıdır.
7. **Gliom / Glioblastom:** Santral sinir sisteminin nöroglial maligniteleridir.

#### Diğer Karıştırılan Kavramlar:
- **Lösemi:** Kanda ve kemik iliğinde blast artışı ile seyreden hematopoetik malignitedir.
- **Karsinoid Tümör (Nöroendokrin Tümör):** Eskiden 'kanserimsi/yavaş ilerleyen' anlamında karsinoid dense de günümüzde potansiyel olarak malign nöroendokrin neoplazm kabul edilir.

> 🔴 **Sınav Tuzağı:** ==red:Sınavda 'Aşağıdakilerden hangisi benign bir tümördür?' sorusunda seçeneklere Melanom, Lenfoma, Seminom veya Mezotelyoma konulur. Bunların hiçbiri benign DEĞİLDİR!===""",
        "spotPearls": [
            "🔴 **Melanom, Lenfoma, Seminom, Mezotelyoma ve Hepatom** isimleri '-om' ile bitmesine rağmen **TAMAMI MALİGNDİR!**",
            "🔵 ==blue:Tıpta 'benign lenfoma' veya 'benign seminom' diye bir varlık yoktur; lenfoma ve seminom terimleri doğası gereği malign neoplazmları ifade eder.==",
            "⚡ Asbest maruziyeti ile plevrada gelişen ve '-om' ile biten malign tümör **Mezotelyoma**dır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Melanom", "text": "Melanositlerin malignitesi; 'benign melanom' yoktur (benign olanı Nevüstür)."},
                {"label": "Lenfoma", "text": "Lenfoid sistemin malignitesi."},
                {"label": "Seminom", "text": "Testis germ hücreli malign tümörü."},
                {"label": "Mezotelyoma", "text": "Seröz zarların asbest ilişkili malignitesi."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-6-1",
                "front": "Soneki '-om' olmasına rağmen biyolojik olarak son derece malign olan 4 klasik tümör örneği veriniz.",
                "back": "1) Melanom, 2) Lenfoma, 3) Seminom, 4) Mezotelyoma (ayrıca Hepatom / Multipl Miyelom).",
                "facultyNote": "TUS sınavlarında en sık sorulan terminoloji tuzağıdır."
            },
            {
                "id": "tb-fc-6-2",
                "front": "Melanositlerin benign neoplazmına ne ad verilir?",
                "back": "Melanositik Nevüs (Benign Nevüs / Ben).",
                "facultyNote": "Melanom denildiğinde ise doğrudan malign neoplazm anlaşılır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-6",
            "question": "Aşağıdaki neoplazmlardan hangisi isimlendirmesinde '-om' eki taşımasına rağmen biyolojik davranış açısından daima MALİGN bir tümördür?",
            "options": [
                "A) Adenom",
                "B) Fibrom",
                "C) Seminom",
                "D) Lipom",
                "E) Kondrom"
            ],
            "answer": "C",
            "explanation": "Seminom, testis germ hücrelerinden köken alan malign bir neoplazmdır. Adenom, fibrom, lipom ve kondrom ise benign neoplazmlardır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Write generator that produces all 24 slides dynamically with faculty-grounded content
# Add remaining slides 7 to 24 with high clinical accuracy
remaining_slides = [
    {
        "slideNumber": 7,
        "title": "Mikst (Karma) Tümörler ve Teratomlar",
        "subtitle": "Diverjan diferansiasyon, pleomorfik adenom ve totipotent germ hücresi tümörleri.",
        "badge": "Özel Neoplazmlar",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Mikst tümör tek bir germ yaprağından köken alıp iki farklı yöne diferansiye olur; Teratom ise totipotent hücreden çıkıp 3 germ yaprağını birden üretir.",
            "note": "Tükürük bezinin pleomorfik adenomu mikst tümörün; overin dermoid kisti teratomun en klasik örneğidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Mikst Tümörler ve Teratomların Biyolojisi
Çoğu neoplazm tek bir hücre tipine diferansiye olurken, bazı tümörler birden fazla doku elemanı içerir:

#### 1. Mikst Tümörler (Karma Tümörler):
- **Köken:** Tek bir germ yaprağına ait transforme klonal progenitör hücreden kaynaklanır; ancak hücreler **diverjan diferansiasyon** göstererek hem epitelyal hem mezenkimal elemanlar üretir.
- **En Klasik Örnek:** Tükürük bezinin **Pleomorfik Adenomu (Mikst Tümörü):**
  - Epitelyal kanallar, miyoepitelyal hücreler ile birlikte miksomatöz kıkırdak ve kemik benzeri mezenkimal stroma içerir.
  - Benigndir; ancak yetersiz cerrahide nüks edebilir veya nadiren malignleşebilir (*Karsinoma ex pleomorfik adenom*).
- **Malign Örnek:** Uterusun Malign Mikst Müllerian Tümörü (MMMT / Karsinosarkom).

#### 2. Teratomlar:
- **Köken:** Totipotent kök hücrelerden (genellikle gonadlardaki germ hücreleri veya orta hat embriyonik kalıntılar) kaynaklanır.
- **Tanımlayıcı Özellik:** Her üç germ yaprağına (**Ektoderm, Mezoderm, Endoderm**) ait doku elemanlarını kaotik bir biçimde bir arada içerir!
- İçinde deri, saç folikülleri, yağ dokusu, kıkırdak, kemik, diş, solunum epiteli ve tiroid dokusu bulunabilir.
- **Sınıflama:**
  - **Matür Teratom (Benign):** Doku elemanları tamamen olgunlaşmıştır. Örn: Overin *Dermoid Kisti* (Matür Kistik Teratom).
  - **İmmatür Teratom (Malign):** Olgunlaşmamış embriyonik dokular (özellikle nöroepitelyal doku / nöroektoderm) içerir; agresiftir.""",
        "spotPearls": [
            "🔴 **Mikst tümör** tek bir germ yaprağından çıkarak diverjan diferansiasyon gösterir (Örn: Parotiste Pleomorfik Adenom).",
            "🔵 ==blue:Her üç germ yaprağından (ektoderm, mezoderm, endoderm) doku elemanları içeren ve overde dermoid kist oluşturan tümör Teratomdur.==",
            "⚡ Teratomun malign kabul edilmesini sağlayan en kritik histopatolojik bileşen **immatür nöroepitelyal (nöroektodermal) doku** varlığıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Pleomorfik Adenom", "text": "Tükürük bezinin en sık tümörü. Epitel + kondromiksoid stroma."},
                {"label": "Teratom", "text": "Totipotent germ hücresi. Ektoderm, mezoderm, endoderm içerir."},
                {"label": "Dermoid Kist", "text": "Overin benign matür kistik teratomu (kıl, diş, yağ birikimi)."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-7-1",
                "front": "Tek bir germ yaprağından kaynaklanan klonun hem epitelyal hem kıkırdaksı mezenkimal elemanlara ayrıştığı parotis tümörü nedir?",
                "back": "Pleomorfik Adenom (Tükürük bezinin mikst tümörü).",
                "facultyNote": "Tükürük bezinin en sık görülen benign tümörüdür."
            },
            {
                "id": "tb-fc-7-2",
                "front": "Bir teratomun histolojik incelemesinde malignite derecesini (grade) belirleyen ana histolojik yapı nedir?",
                "back": "İmmatür nöroepitelyal (nöroektodermal) dokunun miktarıdır.",
                "facultyNote": "İmmatür teratom malign davranır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-7",
            "question": "Yirmi beş yaşında bir kadında overde saptanan kistik kitle rezeke ediliyor. Makroskopisinde kist içinde sebum, kıl yumakları ve bir adet diş izleniyor. Mikroskopisinde ise matür skuamöz epitel, yağ dokusu, kıkırdak ve bronş epitali saptanıyor. Bu lezyonun en olası patolojik tanısı nedir?",
            "options": [
                "A) Pleomorfik adenom",
                "B) Matür kistik teratom (Dermoid kist)",
                "C) Hamartom",
                "D) Koristom",
                "E) Fibrosarkom"
            ],
            "answer": "B",
            "explanation": "Her üç germ yaprağına (ektoderm: deri/kıl, mezoderm: kıkırdak/yağ, endoderm: bronş epiteli) ait matür dokuların bir arada bulunduğu over kistik kitlesi matür kistik teratomdur (Dermoid kist).",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 8,
        "title": "Hamartom ve Koristom: Neoplazm Taklitçileri",
        "subtitle": "Hamartom (yerinde dağınık doku) ve Koristom (ektopik normal doku) ayrımı.",
        "badge": "Lezyon Ayrımı",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Hamartom ve Koristom gerçek neoplazm değildir! Hamartom o organa ait dokunun dağınık kütlesidir; Koristom ise tamamen yabancı bir organ dokusunun yanlış yerde bulunmasıdır.",
            "note": "Akciğerde kıkırdak ve bronş epiteli kitlesi hamartomdur; midede pankreas adacıkları koristomdur.",
            "emphasisType": "exam_trap"
        },
        "synthesisNarrative": """### Hamartom ve Koristom: Biyolojik Farklar
Radyolojik veya klinik olarak kitle (tümör) görünümü verip gerçekte neoplazi olmayan iki gelişimsel lezyon:

#### 1. Hamartom:
- **Tanım:** Bulunduğu **organa normalde ait olan** matür hücre ve doku elemanlarının, yapısal organizasyonu kaybetmiş, kaotik ve düzensiz bir küme halinde büyümesidir.
- **En Klasik Örnek:** **Akciğer Pulmoner Kondroid Hamartomu:**
  - Akciğerde kıkırdak, fibröz doku, yağ ve kleft benzeri bronş epitelinden oluşan kitle. Radyolojide düzgün sınırlı, patlamış mısır (popcorn) kalsifikasyonu gösterir.
- **Bile Duct Hamartomu (von Meyenburg Kompleksi):** Karaciğerde kistik safra kanalları kümesi.

#### 2. Koristom (Heterotopi / Ektopi):
- **Tanım:** Mikroskopik olarak tamamen **normal görünen bir dokunun, normalde bulunmaması gereken ektopik bir anatomik bölgede** kitle oluşturmasıdır.
- **Klasik Örnekler:**
  - Mide submukozasında veya Meckel divertikülünde **Ektopik Pankreas Dokusu**.
  - Dil kökünde **Lingual Tiroid Dokusu**.
  - Adrenal bez kalıntılarının over veya testis çevresinde saptanması.

> 🔴 **Sınav Tuzağı:** ==red:Hamartom = Yerinde ama dağınık doku; Koristom = Başka organa ait normal dokunun ektopik/yanlış yerde olması!== İkisi de malignleşme potansiyeli taşımayan benign gelişimsel anomalilerdir.""",
        "spotPearls": [
            "🔴 **Hamartom:** Bulunduğu yere ait dokuların kaotik kümelenmesidir (Örn: Akciğerde kıkırdak + yağ + epitel içeren kondroid hamartom).",
            "🔵 ==blue:Tamamen normal bir dokunun bulunmaması gereken başka bir organda kitle yapmasına Koristom (Heterotopi/Ektopi) denir (Örn: Midede ektopik pankreas).==",
            "⚡ Hem hamartom hem koristom gerçek birer neoplazm değildir; ancak klinik ve radyolojik olarak maligniteyi taklit edebilirler."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Hamartom", "text": "Yerli dokuların düzensiz organizasyonu (Akciğer hamartomu)."},
                {"label": "Koristom", "text": "Yabancı/ektopik normal doku yuvası (Midede pankreas adacığı)."},
                {"label": "Neoplastik Değildir", "text": "Gelişimsel doku organizasyon defektleridir."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-8-1",
                "front": "Akciğer grafisinde soliter pulmoner nodül saptanan hastada biyopside matür kıkırdak, yağ ve yarık benzeri epitel içeren lezyon nedir?",
                "back": "Pulmoner Kondroid Hamartom.",
                "facultyNote": "Akciğerin en sık benign lezyonudur; popcorn kalsifikasyonu tipiktir."
            },
            {
                "id": "tb-fc-8-2",
                "front": "Mide antrum submukozasında asemptomatik olarak saptanan ve histolojisinde normal asiner yapılar ile Langerhans adacıkları izlenen lezyon nedir?",
                "back": "Koristom (Heterotopik / Ektopik Pankreas).",
                "facultyNote": "Doku normaldir ancak bulunduğu yer yanlıştır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-8",
            "question": "Endoskopide mide duodenum bileşkesinde 1.5 cm'lik submukozal polipoid lezyon saptanan hastanın biyopsisinde normal yapıda pankreatik asinuslar ve Langerhans adacıkları izlenmiştir. Bu patolojik durumun en doğru tanımı aşağıdakilerden hangisidir?",
            "options": [
                "A) Hamartom",
                "B) Koristom (Heterotopi)",
                "C) Pleomorfik adenom",
                "D) Karsinoma in situ",
                "E) Teratom"
            ],
            "answer": "B",
            "explanation": "Normal histolojik yapıdaki bir dokunun normalde bulunmaması gereken anatomik bir lokalizasyonda (midede pankreas dokusu) bulunmasına Koristom (Heterotopi / Ektopi) denir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 9,
        "title": "Diferansiyasyon ve Anaplazi Kavramları",
        "subtitle": "Hücresel olgunlaşma derecesi, anaplazi ve diferansiyasyon kaybı.",
        "badge": "Morfoloji & Grade",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Diferansiyasyon, tümör hücresinin kaynaklandığı normal hücreye ne kadar benzediğidir. Benign tümörler mükemmel diferansiyedir; Anaplazi ise diferansiyasyonun tamamen kaybolmasıdır ve kanserin damgasıdır.",
            "note": "Anaplazik bir tümöre baktığınızda onun yağdan mı, kastan mı yoksa epitelden mi çıktığını rutin boyalarla anlayamazsınız.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Diferansiyasyon Spektrumu ve Anaplazi
**Diferansiyasyon (Farklılaşma):** Neoplastik parankim hücrelerinin, köken aldıkları normal matür hücrelere morfolojik ve fonksiyonel açıdan ne derecede benzediğini ifade eder.

#### Diferansiyasyon Dereceleri:
- **İyi Diferansiye (Well-Differentiated / Grade 1):** Tümör hücreleri normal doku hücrelerine çok benzer, düzenli glandlar veya bol keratin üretir.
- **Orta Diferansiye (Moderately Differentiated / Grade 2):** Yapısal düzen kısmen korunmuş ancak nükleer atipi ve mitoz artmıştır.
- **Kötü Diferansiye (Poorly Differentiated / Grade 3):** Normal doku yapısı büyük oranda silinmiş, hücreler matür özelliklerini kaybetmiştir.
- **Andiferansiye / Anaplazik (Undifferentiated):** Diferansiyasyon tamamen kaybolmuştur.

#### Anaplazi (Geriye Dönüş / Biçimsizlik):
Yunanca *ana* (geriye) ve *plasis* (oluşum) kelimelerinden gelir. Diferansiasyonun tam yokluğudur.
> 💡 **Temel Kural:** Bütün benign tümörler iyi diferansiyedir (örneğin bir lipom hücresi normal adipositten neredeyse ayırt edilemez). **Anaplazi ise yalnızca MALİGN neoplazmlarda görülür ve malignitenin kesin göstergesidir (hallmark).**

Anaplazik tümörlerde kaynak dokunun özgül fonksiyonları kaybolur. Örneğin anaplazik tiroid karsinomu tiroid hormonu üretemez, iyot tutamaz ve son derece ölümcüldür.""",
        "spotPearls": [
            "🔴 Benign tümörler kural olarak **iyi diferansiyedir**; **Anaplazi** (diferansiyasyon kaybı) ise yalnızca **malign** tümörlerde saptanır.",
            "🔵 ==blue:Bir tümörün köken aldığı normal dokuya morfolojik ve fonksiyonel olarak benzeme derecesine 'Diferansiyasyon' denir.==",
            "⚡ Diferansiyasyon azaldıkça (Grade yükseldikçe) tümörün büyüme hızı, invazyon ve metastaz potansiyeli artar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Diferansiyasyon", "text": "Kaynak dokuya benzeme derecesi."},
                {"label": "Anaplazi", "text": "Farklılaşmanın tam kaybı; malignitenin morfolojik kanıtı."},
                {"label": "Grade Korelasyonu", "text": "İyi diferansiye = Düşük grade; Anaplazik = Yüksek grade."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-9-1",
                "front": "Neoplastik hücrelerin kaynak dokusuna morfolojik ve fonksiyonel benzerliğini tamamen yitirmesi durumuna ne ad verilir?",
                "back": "Anaplazi (Andiferansiasyon).",
                "facultyNote": "Malignitenin güvenilir kardinal göstergesidir."
            },
            {
                "id": "tb-fc-9-2",
                "front": "Benign tümörlerin diferansiyasyon durumu nasıldır?",
                "back": "Benign tümörler istisnasız iyi diferansiyedir ve kaynaklandığı dokuya çok benzer.",
                "facultyNote": "Lipom hücreleri normal yağ hücrelerine mikroskopta ikiz gibi benzer."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-9",
            "question": "Patolojide neoplastik parankim hücrelerinin kaynaklandığı matür dokuya benzerliğini tamamen kaybetmesi, primitif ve ilkel bir hücresel morfoloji kazanması durumuna ne ad verilir?",
            "options": [
                "A) Metaplazi",
                "B) Desmoplazi",
                "C) Hipertrofi",
                "D) Anaplazi",
                "E) Heterotopi"
            ],
            "answer": "D",
            "explanation": "Diferansiasyonun tam kaybına 'Anaplazi' denir. Malign tümörlerin temel morfolojik ayırt edici özelliğidir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 10,
        "title": "Anaplazinin Morfolojik Kriterleri",
        "subtitle": "Pleomorfizm, nükleer hiperkromazi, atipik mitozlar ve tümör dev hücreleri.",
        "badge": "Mikroskopi",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Mikroskop altında bir hücreye malign dedirten anaplazi bulgularını tek tek sayabilmelisiniz: Pleomorfizm, yüksek N/C oranı, hiperkromazi, kaba kromatin, belirgin nükleol ve en önemlisi ATİPİK MİTOZLARDIR!",
            "note": "Tripolar veya kuadripolar anormal mitotik figürler (üç köşeli / dört köşeli iğ iplikleri) malignitenin kesin kanıtıdır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Mikroskopta Anaplazinin Kardinal Bulguları
Bir patoloğun biyopside malignite tanısı koymasını sağlayan anaplazik hücresel ve nükleer değişiklikler:

#### 1. Pleomorfizm (Boyut ve Şekil Değişkenliği):
Hücreler ve nükleuslar arasında belirgin boyut ve şekil varyasyonu vardır. Aynı alanda küçük ilkel hücrelerin yanında devasa canavar hücreler (*tümör dev hücreleri*) bir arada görülür.

#### 2. Anormal Nükleer Morfoloji:
- **Yüksek Çekirdek/Sitoplazma (N/C) Oranı:** Normal hücrede N/C oranı 1:4 ile 1:6 arasındayken; anaplazik hücrede çekirdek sitoplazmayı doldurarak oran **1:1'e yaklaşır!**
- **Nükleer Hiperkromazi:** Çekirdekler bol DNA içerdiğinden hematoksilen ile koyu mavi-mor boyanır. Kromatin kaba, topaklanmış ve nükleer zar boyunca kümelenmiştir.
- **Büyük Belirgin Nükleoller:** Aktif RNA ve ribozom sentezini yansıtan iri, belirgin nükleoller (çekirdekçikler) mevcuttur.

#### 3. Mitoz Artışı ve Atipik Mitotik Figürler:
- Sadece mitoz sayısının artması malignite kanıtı değildir (rejenerasyonda da mitoz artabilir).
- **Asıl malignite kriteri ATİPİK, BİZAR MİTOZLARDIR!** Normal bipolar iğ ipliği yerine tripolar (üç köşeli Mercedes amblemi gibi), kuadripolar veya çok kutuplu anormal mitozlar görülür.

#### 4. Polarite Kaybı ve Mimari Düzensizlik:
Hücrelerin bazal membranla ve birbirleriyle olan oryantasyonu tamamen bozulur; anarşik levhalar halinde büyürler.

#### 5. İskemik Tümör Nekrozu:
Tümör damarlarının hızlı çoğalan kitleyi besleyememesi sonucu santral kavitasyon ve koagülasyon nekrozu gelişir.""",
        "spotPearls": [
            "🔴 Yüksek N/C oranı (1:1'e yaklaşması), nükleer hiperkromazi ve pleomorfizm temel anaplazi kriterleridir.",
            "🔵 ==blue:Normal mitoz sayısı hızlı çoğalan benign lezyonlarda da artabilir; ancak TRİPOLAR/KUADRİPOLAR ATİPİK MİTOZ figürleri kesin MALİGNİTE kanıtıdır!== ",
            "⚡ Tümör dev hücreleri (anaplazik tek veya çok çekirdekli dev hücreler), yabancı cisim veya Langhans gibi inflamatuar dev hücrelerle karıştırılmamalıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Pleomorfizm", "text": "Hücre ve çekirdek boy/şekil anomalileri."},
                {"label": "N/C Oranı", "text": "Normalde 1:4-1:6 iken 1:1'e kayması."},
                {"label": "Atipik Mitoz", "text": "Tripolar, asimetrik mitotik iğ iplikleri (malignite imzası)."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-10-1",
                "front": "Normal dokularda 1:4 ile 1:6 olan Çekirdek/Sitoplazma (N/C) oranı anaplazik malign hücrelerde kaça yaklaşır?",
                "back": "1:1 oranına yaklaşır (nükleomegali).",
                "facultyNote": "Çekirdek devasa boyutlara ulaşır ve sitoplazmayı kaplar."
            },
            {
                "id": "tb-fc-10-2",
                "front": "Işık mikroskobunda maligniteyi reaktif doku rejenerasyonundan kesin olarak ayıran mitotik bulgu nedir?",
                "back": "Tripolar veya kuadripolar atipik/bizar mitotik figürlerin varlığıdır.",
                "facultyNote": "Mitoz sayısı yanıltabilir; mitozun atipik şekli kesin kanıttır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-10",
            "question": "Bir doku biyopsisinde saptanan aşağıdaki mikroskopik bulgulardan hangisi, lezyonun kesin olarak MALİGN olduğunu gösteren en güvenilir anaplazi kriteridir?",
            "options": [
                "A) Sitoplazmada glikojen birikimi",
                "B) Bipolar simetrik mitotik figürlerin sayısında hafif artış",
                "C) Tripolar ve kuadripolar atipik mitotik figürler",
                "D) Hücreler arası lenfosit infiltrasyonu",
                "E) Fibroblast proliferasyonu"
            ],
            "answer": "C",
            "explanation": "Bipolar mitozlar benign rejeneratif durumlarda da sıkça görülebilir; ancak tripolar, kuadripolar veya çok kutuplu asimetrik atipik mitotik figürler malignitenin kesin patolojik kanıtıdır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 11,
        "title": "Displazi ve Karsinoma İn Situ (CIS)",
        "subtitle": "Pre-invaziv epitelyal neoplazi, epitel içi polarite kaybı ve bazal membran bariyeri.",
        "badge": "Prekanseröz",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Karsinoma in situ, karsinomun tüm hücresel atipisine sahiptir; epitelin tabanından tavanına kadar her kat anaplazik hücrelerle doludur AMA bazal membran sağlamdır! Bazal membran aşılmadığı sürece metastaz riski sıfırdır.",
            "note": "Serviks kanseri taramasındaki Pap-smear testinin mantığı CIS aşamasında lezyonu yakalayıp invaziv karsinoma dönüşmeden tedavi etmektir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Displazi ve Karsinoma İn Situ Spektrumu
**Displazi (Düzensiz Büyüme):** Yalnızca epitel dokusunda görülen, hücresel tekdüzeliğin ve yapısal mimari organizasyonun kaybı ile karakterize prekanseröz (kanser öncülü) lezyondur.
- Pleomorfizm, hiperkromazi, mitoz artışı ve bazal tabakadan yüzeye doğru maturasyon kaybı içerir.
- **Hafif ve Orta Displazi:** Epitelin alt 1/3 veya 2/3'ünü tutar; uyaran (örneğin sigara, HPV, kronik irritasyon) ortadan kalktığında geri dönebilir (reversibldir).

#### Karsinoma İn Situ (CIS / Şiddetli Displazi):
- Displastik hücreler epitelin **tüm kalınlığını (full-thickness / tabandan tavana kadar)** doldurmuştur.
- Morfolojik olarak invaziv karsinom hücrelerinden hiçbir farkı yoktur.
- **Kritik Ayrım Noktası:** ==red:BAZAL MEMBRAN TAMAMEN SAĞLAMDIR!==
- Bazal membran bir kılıf gibi tümörü sarar; epitel içinde kan ve lenf damarı bulunmadığından **CIS AŞAMASINDA METASTAZ RİSKİ KESİNLİKLE SIFIRDIR!**

#### İnvaziv Karsinoma İlerleme:
Tümör hücreleri matriks metalloproteinazlar (MMP-2, MMP-9) salgılayarak tip IV kollajenden zengin bazal membranı delip subepitelyal stromaya geçtiği an **İnvaziv Karsinom** adını alır ve metastaz yeteneği kazanır.""",
        "spotPearls": [
            "🔴 Karsinoma in situ'da displastik atipik hücreler epitelin **tüm katlarını** doldurur; ancak **bazal membran intakttır**.",
            "🔵 ==blue:Karsinoma in situ aşamasında lezyonun metastaz yapma olasılığı SIFIRDIR; çünkü epitel vasküler değildir ve bazal membran aşılmamıştır.==",
            "⚡ Hafif displaziler reversibl iken; bazal membranı aşan lezyonlar artık geri dönüşsüz invaziv karsinomdur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Displazi", "text": "Epitel içi mimari ve hücresel atipi; prekanseröz lezyon."},
                {"label": "Karsinoma İn Situ", "text": "Tam kat epitelyal atipi + Sağlam bazal membran."},
                {"label": "Metastaz Riski", "text": "CIS'te sıfır; bazal membran delinince invaziv karsinom başlar."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-11-1",
                "front": "Karsinoma in situ (CIS) lezyonunu invaziv karsinomdan ayıran en kritik histolojik sınır nedir?",
                "back": "Bazal membranın intakt (delinmemiş / sağlam) olmasıdır.",
                "facultyNote": "Bazal membran aşılmadığı sürece tümör damarlarla temas edemez."
            },
            {
                "id": "tb-fc-11-2",
                "front": "Karsinoma in situ tanısı alan bir serviks lezyonunda lenf nodu metastazı beklenir mi?",
                "back": "Hayır, kesinlikle beklenmez (metastaz riski sıfırdır).",
                "facultyNote": "Epitel avaskülerdir; lenfatikler bazal membranın altındaki stromadadır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-11",
            "question": "Uterus serviks biyopsisinde skuamöz epitelin tüm katlarını dolduran pleomorfik, hiperkromatik hücreler izlenmiş, ancak bazal membranın tamamen sağlam olduğu ve stromaya geçiş olmadığı saptanmıştır. Bu lezyonun evresi ve metastaz riski için aşağıdakilerden hangisi doğrudur?",
            "options": [
                "A) İnvaziv karsinom — Yüksek lenf nodu metastaz riski",
                "B) Hafif displazi — Tamamen selim lezyon",
                "C) Karsinoma in situ — Sıfır metastaz riski",
                "D) Mikroinvaziv karsinom — Hematojen metastaz riski",
                "E) Metaplazi — Malignite riski yok"
            ],
            "answer": "C",
            "explanation": "Epitelin tüm katlarını tutan ancak bazal membranı aşmamış lezyon Karsinoma in situ'dur (CIS). Bazal membran sağlam olduğu için lenfatik veya kan damarlarına erişim yoktur ve metastaz riski sıfırdır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 12,
        "title": "Lokal Büyüme ve İnvazyon: Kapsül Mimarisi",
        "subtitle": "Benign ekspansif büyüme vs Malign infiltratif lokal invazyon mekanizmaları.",
        "badge": "İnvazyon",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Benign tümör çevre dokuyu iter ve bir fibröz kapsül oluşturarak sınırlarını korur, enükleasyonla kolayca çıkarılır. Malign tümör ise kapsülsüzdür; yengeç gibi çevre dokunun içine sızarak onu yok eder.",
            "note": "Kapsül varlığı benignliğin güçlü bir göstergesidir; ancak istisnalar (hemanjiom, leiomyom) unutulmamalıdır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Lokal Büyüme Paternleri: İtme vs Sızma
Bir tümörün primer çıktığı odakta çevre konak doku ile ilişkisi benign ve malign ayrımında metastazdan sonraki en güvenilir ikinci kriterdir:

#### 1. Benign Tümörlerde Lokal Büyüme:
- **Ekspansif (İtici) Büyüme:** Yavaş büyür, çevre dokuyu komprese ederek iter.
- **Fibröz Kapsül:** Komprese olan çevre konak doku stromasından ve tümör fibroblastlarından oluşan belirgin bir fibröz psödokapsül/kapsül ile çevrilidir.
- **Cerrahi Kolaylık:** Düzgün sınırlı olduğu için çevre normal dokuya zarar vermeden bir bütün olarak çıkarılabilir (*enükleasyon*).
- **Kapsülsüz Benign İstisnalar:** Hemanjiomlar kapsülsüzdür (çevreye sünger gibi yayılır), uterin leiyomiyomlar çevre miyometriyumun sıkışmasıyla yalancı kapsül oluşturur.

#### 2. Malign Tümörlerde Lokal İnvazyon:
- **İnfiltratif (Sızıcı / Yıkıcı) Büyüme:** Hızlı ve koordinesiz çoğalır. Çevre doku aralıklarına, sinir kılıflarına (perinöral invazyon), kas lifleri arasına kök salarak ilerler.
- **Kapsül Yokluğu:** Gerçek bir kapsülleri yoktur. Bazen yalancı kapsül oluştursalar da mikroskopik incelemede tümör hücrelerinin bu kapsülü delip çevreye taştığı görülür.
- **Cerrahi Rezeksiyon Marjı:** Malign tümörler yalnızca görünen kitle olarak çıkarılamaz; çevre mikroskobik infiltrasyonu temizlemek için mutlaka 'geniş cerrahi sınır (salim sınır)' ile rezeke edilmelidir.""",
        "spotPearls": [
            "🔴 Benign tümörler çevre dokuyu **iterek (ekspansif)** büyür ve fibröz **kapsül** oluşturur; cerrahi enükleasyona uygundur.",
            "🔵 ==blue:Malign neoplazmlar çevre dokuyu infiltre ve destrükte ederek sınırları belirsiz, infiltratif biçimde büyürler; kapsülleri yoktur.==",
            "⚡ Hemanjiom benign olmasına rağmen kapsülsüzdür; infiltratif büyüme taklidi yapabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Benign Büyüme", "text": "Ekspansif, kapsüllü, düzgün sınırlı, hareketli."},
                {"label": "Malign İnvazyon", "text": "İnfiltratif, kapsülsüz, çevreye fikse, yıkıcı."},
                {"label": "Perinöral İnvazyon", "text": "Sinir kılıfları boyunca yayılım (ağrı ve nüks sebebi)."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-12-1",
                "front": "Benign neoplazmların cerrahi olarak çevre dokudan kolayca soyularak (enükleasyon) çıkarılabilmesini sağlayan yapı nedir?",
                "back": "Tümörü çevreleyen fibröz kapsül varlığı ve ekspansif (itici) büyüme paterni.",
                "facultyNote": "Malign tümörlerde ise sınır belirsizdir, geniş rezeksiyon gerekir."
            },
            {
                "id": "tb-fc-12-2",
                "front": "Benign bir neoplazm olmasına rağmen kapsül içermeyen ve infiltratif görünüm veren klasik damar tümörü nedir?",
                "back": "Hemanjiom.",
                "facultyNote": "Kapsül yokluğu her zaman malignite anlamına gelmez."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-12",
            "question": "Aşağıdaki histopatolojik özelliklerden hangisi bir tümörün BENİGN olduğunu destekleyen en güçlü bulgudur?",
            "options": [
                "A) Kapsülü delerek çevre yağ dokusuna uzanması",
                "B) Belirgin fibröz bir kapsülle çevrili olup ekspansif büyümesi",
                "C) Perinöral lenfatik boşluklarda tümör embolileri içermesi",
                "D) Çevredeki kas liflerini destrükte etmesi",
                "E) Geniş koagülasyon nekrozu alanları barındırması"
            ],
            "answer": "B",
            "explanation": "Belirgin fibröz bir kapsül varlığı ve tümörün çevre dokuyu tahrip etmeksizin iterek (ekspansif) büyümesi benign neoplazmların en karakteristik özelliğidir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Generate remaining slides 13 to 24 with rich faculty notes
# Slide 13: Metastaz Tanımı ve Yolları
# Slide 14: Lenfatik Yayılım ve Sentinel Lenf Nodu
# Slide 15: Hematojen Yayılım ve Organ Hedefleri
# Slide 16: Vücut Boşluklarına Ekim (Transçölomik Yayılım)
# Slide 17: Benign ve Malign Karşılaştırma Matrisi (Büyük Özet Tablosu)
# Slide 18: Kanser Epidemiyolojisi ve İnsidans / Mortalite
# Slide 19: Çevresel ve Mesleki Karsinojenler (Asbest, Aflatoksin vb.)
# Slide 20: Kalıtsal Kanser Sendromları (BRCA, Lynch, FAP, Li-Fraumeni)
# Slide 21: Prekanseröz Lezyonlar ve Kronik İnflamasyon
# Slide 22: Tümör İmmünitesi ve İmmün Kaçış
# Slide 23: Paraneoplastik Sendromlar
# Slide 24: Tümör Belirteçleri ve Patolojik Tanı Yöntemleri (Özet)

more_slides = [
    {
        "slideNumber": 13,
        "title": "Metastaz: Malignitenin Tartışmasız Kanıtı",
        "subtitle": "Metastaz tanımı, biyolojik önemi ve metastaz yapmayan malignite istisnaları.",
        "badge": "Metastaz",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Metastaz bir tümörün kesin olarak malign olduğunu gösteren TEK tartışmasız kriterdir. Ancak iki istisna vardır ki son derece malign olmalarına rağmen hemen hiç metastaz yapmazlar: Bazal Hücreli Karsinom ve Glioblastom!",
            "note": "Primer odakla hiçbir anatomik devamlılığı olmayan ikincil tümör odaklarının ortaya çıkması metastazdır.",
            "emphasisType": "exam_trap"
        },
        "synthesisNarrative": """### Metastazın Tanımı ve Biyolojik Gücü
**Metastaz:** Tümör hücrelerinin primer çıktığı odaktan ayrılarak, primer tümörle hiçbir anatomik devamlılığı olmayan uzak bir organ veya dokuya göç edip orada sekonder tümör kolonileri kurmasıdır.

> 🔴 **Altın Kural:** ==red:METASTAZ, BİR TÜMÖRÜN MALİGN OLDUĞUNU KANITLAYAN EN GÜVENİLİR VE TARTIŞMASIZ KRİTERDİR!== Benign tümörler KESİNLİKLE metastaz yapmazlar.

Kanser ölümlerinin %90'ından fazlası primer kitleden değil; metastazların yol açtığı organ yetmezliklerinden (akciğer, karaciğer, beyin, kemik metastazları) kaynaklanır.

#### Neredeyse Hiç Metastaz Yapmayan Malign İstisnalar:
Bazı tümörler son derece malign ve lokal olarak çok agresif/destrüktif olmalarına rağmen uzak organ metastazı yapmazlar (veya son derece nadirdir):
1. **Derinin Bazal Hücreli Karsinomu (BCC):**
   - İnsan vücudunun en sık görülen kanseridir.
   - Lokal olarak çevre dokuyu, kıkırdağı ve kemiği kemirircesine yıkar (*Ulcus rodens*); ancak metastaz oranı %0.1'in altındadır.
2. **Santral Sinir Sisteminin Glioblastomu (GBM):**
   - Beynin en öldürücü primer malign tümörüdür.
   - Beyin parankimini hızla harap eder; ancak kan-beyin bariyeri ve lenfatik eksikliği nedeniyle vücudun diğer organlarına (ekstrakranyal) hemen hiç metastaz yapmaz.""",
        "spotPearls": [
            "🔴 **Metastaz**, bir neoplazmın kesin olarak **malign** olduğunu kanıtlayan en güvenilir tek kriterdir.",
            "🔵 ==blue:Lokal olarak son derece destrüktif büyüyen ancak uzak metastaz yapma olasılığı neredeyse sıfır olan deri kanseri Bazal Hücreli Karsinomdur (BCC).==",
            "⚡ Beynin en malign tümörü olan Glioblastom (GBM), kranyum dışına (ekstrakranyal) kural olarak metastaz yapmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Metastaz", "text": "Primer kitleyle bağlantısız uzak sekonder odak oluşumu."},
                {"label": "Kesin Malignite", "text": "Metastaz varsa lezyon istisnasız maligndir."},
                {"label": "BCC ve GBM İstisnası", "text": "Lokal agresif maligniteler olmasına rağmen uzak metastaz yapmazlar."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-13-1",
                "front": "Bir neoplazmın malign olduğunu kanıtlayan en kesin ve tartışmasız biyolojik özellik nedir?",
                "back": "Metastaz yapmasıdır.",
                "facultyNote": "Metastaz varlığı lezyonun tartışmasız malign olduğunu gösterir."
            },
            {
                "id": "tb-fc-13-2",
                "front": "Lokal invazyonu çok agresif olan fakat metastaz yeteneği neredeyse bulunmayan en sık deri kanseri nedir?",
                "back": "Bazal Hücreli Karsinom (BCC).",
                "facultyNote": "Klinikte 'Ulcus rodens' olarak da adlandırılır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-13",
            "question": "Aşağıdaki neoplazmlardan hangisi lokal olarak son derece invaziv ve destrüktif büyümesine rağmen, uzak organlara metastaz yapma potansiyeli hemen hemen HİÇ bulunmayan bir malign tümördür?",
            "options": [
                "A) Malign melanom",
                "B) Derinin bazal hücreli karsinomu (BCC)",
                "C) Osteosarkom",
                "D) Akciğer adenokarsinomu",
                "E) Meme duktal karsinomu"
            ],
            "answer": "B",
            "explanation": "Bazal hücreli karsinom (BCC) lokal olarak kıkırdak ve kemiği tahrip edebilen agresif bir malignite olmasına rağmen metastaz oranı <%0.1 düzeyindedir; pratik olarak uzak metastaz yapmaz kabul edilir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 14,
        "title": "Lenfatik Yayılım Yolu ve Sentinel Lenf Nodu",
        "subtitle": "Karsinomların yayılımı, lenfatik drenaj haritalaması ve biyopsi prensipleri.",
        "badge": "Metastaz Yolu",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Karsinomlar lenfatik yolu sever. Bir tümörün ilk boşaldığı lenf noduna Sentinel Lenf Nodu denir. Ameliyatta sentinel nod temizse bütün aksillayı boşaltmaya gerek kalmaz!",
            "note": "Sentinel lenf nodu kavramı meme kanseri ve melanom cerrahisinde morbiditeyi devrim niteliğinde azaltmıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Lenfatik Yayılım ve Sentinel Nod Biyopsisi
Karsinomların en tipik yayılım yolu **lenfatik sistemdir** (lenfojen yayılım). Lenfatik damarların bazal membranları zayıf ve geçirgen olduğundan tümör hücreleri lenf kanallarına kolayca sızar.

#### Lenfatik Yayılım Basamakları:
1. Tümör hücreleri interstisyel lenfatik kapillerlere invaze olur.
2. Lenf akımıyla bölgesel lenf nodlarına sürüklenir.
3. Lenf nodunun subkapsüler sinüsüne yerleşir, prolifere olur ve lenf nodunu tamamen doldurur.
4. Sıradaki lenf nodu zincirine atlar ve en sonunda duktus torasikus aracılığıyla kan dolaşımına dökülür.

#### Sentinel Lenf Nodu (Nöbetçi Lenf Nodu):
- **Tanım:** Bir primer tümörün lenfatik drenaj havzasında lenf sıvısının **ilk ulaştığı** lenf nodudur.
- **Klinik Uygulama (Meme Kanseri ve Melanom):**
  - Tümör çevresine radyoaktif kolloid veya mavi boya (İzosülfan mavisi) enjekte edilir.
  - İlk boyanan/radyoaktivite tutan lenf nodu cerrahi sırasında çıkarılır ve frozen incelemeye yollanır.
  - **Sentinel nodda tümör YOKSA:** Diğer lenf nodlarının da temiz olduğu kabul edilir ve gereksiz aksiller diseksiyondan (lenfödem komplikasyonundan) kaçınılır.
  - **Sentinel nodda tümör VARSA:** Aksiller lenf nodu diseksiyonu tamamlanır.

> 🔴 **Sınav Tuzağı:** ==red:Tümörün büyüklüğü ile lenf nodu metastazı her zaman paralel gitmez; 1 cm'lik küçük bir tümör bile sentinel noda metastaz yapmış olabilir.===""",
        "spotPearls": [
            "🔴 **Karsinomlar** kural olarak ilk önce bölgesel **lenfatik damarlar** yoluyla lenf nodlarına yayılır.",
            "🔵 ==blue:Primer tümörün drene olduğu ilk lenf noduna Sentinel (Nöbetçi) Lenf Nodu denir; sentinel nod negatifse aksiller diseksiyon gerekmez.==",
            "⚡ Lenf nodunda metastaz ilk olarak **subkapsüler sinüste** belirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Lenfojen Yayılım", "text": "Karsinomların en sık kullandığı primer metastaz yolu."},
                {"label": "Subkapsüler Sinüs", "text": "Lenf nodunda metastazın ilk yerleştiği anatomik zon."},
                {"label": "Sentinel Nod", "text": "Meme ve melanomda cerrahiyi yönlendiren ilk lenf nodu."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-14-1",
                "front": "Bir primer tümörün lenfatik drenaj yolundaki ilk lenf noduna ne ad verilir?",
                "back": "Sentinel (Nöbetçi) Lenf Nodu.",
                "facultyNote": "Meme kanseri ve malign melanomda rutin klinik standarttır."
            },
            {
                "id": "tb-fc-14-2",
                "front": "Lenfatik metastazda tümör hücreleri lenf nodunun ilk olarak hangi anatomik bölgesine oturur?",
                "back": "Subkapsüler (marjinal) sinüse oturur.",
                "facultyNote": "Patologlar frozenda ilk olarak subkapsüler alana bakar."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-14",
            "question": "Meme karsinomu operasyonu sırasında tümör çevresine verilen mavi boyanın tutunduğu ilk lenf nodu rezeke edilmiş ve patolojik incelemede metastaz saptanmamıştır. Bu lenf nodunun adı ve cerrahi yaklaşım için aşağıdakilerden hangisi doğrudur?",
            "options": [
                "A) Virchow nodu — Tam aksiller diseksiyon yapılır",
                "B) Sentinel lenf nodu — Diğer aksiller lenf nodlarının diseksiyonuna gerek yoktur",
                "C) Sister Mary Joseph nodu — Kemoterapiye geçilir",
                "D) Kruklen nodu — Karşı meme de rezeke edilir",
                "E) Cloquet nodu — İnvaziv karsinom dışlanır"
            ],
            "answer": "B",
            "explanation": "Tümör lenfatik akımının ulaştığı ilk nod Sentinel Lenf Nodudur. Sentinel nodun metastaz açısından negatif olması durumunda aksiller lenf nodu diseksiyonu yapılmaz ve hasta morbiditeden korunur.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 15,
        "title": "Hematojen Yayılım Yolu ve Organ Tercihleri",
        "subtitle": "Sarkomların yayılımı, venöz invazyon ve akciğer/karaciğer kapiller filtreleri.",
        "badge": "Metastaz Yolu",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Sarkomlar hematojen yayılır; ancak 4 karsinom vardır ki sarkom gibi kan damarlarını işgal eder: Renal hücreli karsinom, Hepatosellüler karsinom, Foliküler tiroid karsinomu ve Koryokarsinom!",
            "note": "Renal ven invazyonu yapıp sağ atriyuma kadar uzanan böbrek kanseri hematojen invazyonun amfideki en meşhur örneğidir.",
            "emphasisType": "exam_trap"
        },
        "synthesisNarrative": """### Hematojen Yayılım Mekanizmaları
Tümör hücrelerinin kan damarlarına (özellikle ince duvarlı venüllere ve venlere) invaze olarak dolaşıma katılmasıdır. Arter duvarları kalın ve elastik olduğundan venöz invazyon çok daha kolaydır.
- **Sarkomların** tipik primer metastaz yoludur.

#### Kan Dolaşımının İki Büyük Filtresi:
1. **Karaciğer:** Gastrointestinal sistemden (mide, kolon, pankreas) dökülen venöz kan portal ven yoluyla ilk olarak karaciğere ulaşır. Bu nedenle GİS kanserlerinin en sık hematojen metastaz yeri **Karaciğerdir**.
2. **Akciğer:** Sistemik venöz kan vena kava yoluyla sağ kalbe ve oradan pulmoner kapiller yatağa dökülür. Tüm sarkomların ve sistemik kanserlerin en sık hematojen metastaz durağı **Akciğerdir**.

#### Damar İnvazyonu Yapan 4 Kritik Karsinom (Ezber Kuralı: 'RH-FK'):
Karsinomlar genel kural olarak lenfojen yayılırken, bu dört karsinom doğrudan venöz invazyon ve hematojen metastaz yapma eğilimindedir:
1. **R**enal Hücreli Karsinom (RHK): Renal veni ve Vena Cava İnferior'u (VCI) doldurarak sağ atriyuma kadar ilerler.
2. **H**epatosellüler Karsinom (HCC): Portal ven ve hepatik ven invazyonu sıktır.
3. **F**oliküler Tiroid Karsinomu: Papiller tiroid lenfojen yayılırken; Foliküler tiroid kural olarak kan damarlarını tutar ve kemik/akciğere metastaz yapar.
4. **K**oryokarsinom: Plasental trofoblast tümörüdür; aşırı anjiyoinvaziftir, erken dönemde akciğer ve beyne kanla yayılır.""",
        "spotPearls": [
            "🔴 Sarkomlar kural olarak **hematojen** yolla yayılır ve en sık **akciğere** metastaz yaparlar.",
            "🔵 ==blue:Lenfojen değil ağırlıkla HEMATOJEN yolla yayılan 4 karsinom: Renal hücreli karsinom, Hepatosellüler karsinom, Foliküler tiroid karsinomu ve Koryokarsinomdur.==",
            "⚡ Renal hücreli karsinom (RHK), renal ven ve vena kava inferior yoluyla sağ atriyuma kadar uzanan tümör trombüsü yapabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Hematojen Yol", "text": "Sarkomların ve geç evre karsinomların yayılım yolu."},
                {"label": "Kapiller Filtreler", "text": "Akciğer (sistemik venöz) ve Karaciğer (portal venöz)."},
                {"label": "Anjiyoinvazif Karsinomlar", "text": "Renal, Hepatosellüler, Foliküler tiroid ve Koryokarsinom."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-15-1",
                "front": "GİS (kolon, mide, pankreas) karsinomlarının en sık hematojen metastaz yaptığı ilk organ hangisidir?",
                "back": "Karaciğerdir (portal venöz drenaj nedeniyle).",
                "facultyNote": "Sistemik venöz dolaşımın ilk filtresi ise akciğerdir."
            },
            {
                "id": "tb-fc-15-2",
                "front": "Tiroid kanserlerinden hangisi lenfojen değil, kan damarlarını (hematojen) tutarak kemik ve akciğere yayılır?",
                "back": "Foliküler Tiroid Karsinomu.",
                "facultyNote": "Papiller tiroid karsinomu ise lenf nodlarına yayılır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-15",
            "question": "Aşağıdaki malign epitelyal tümörlerden (karsinomlardan) hangisi lenfatik yayılımdan ziyade belirgin şekilde KAN DAMARI (hematojen) invazyonu göstererek kemik ve akciğere metastaz yapmasıyla bilinir?",
            "options": [
                "A) Tiroid papiller karsinomu",
                "B) Tiroid foliküler karsinomu",
                "C) Meme invaziv duktal karsinomu",
                "D) Deri skuamöz hücreli karsinomu",
                "E) Kolon adenokarsinomu"
            ],
            "answer": "B",
            "explanation": "Tiroid papiller karsinomu lenfatik yolla servikal lenf nodlarına metastaz yaparken; Foliküler tiroid karsinomu kapsül ve kan damarı invazyonu yaparak hematojen yolla kemik ve akciğere metastaz yapar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 16,
        "title": "Vücut Boşluklarına Ekim (Transçölomik Yayılım)",
        "subtitle": "Periton, plevra ve subaraknoid boşluk ekimleri, Krukenberg ve Psödömiksoma.",
        "badge": "Metastaz Yolu",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Tümör bir vücut boşluğuna ulaştığında tohum gibi serpişir. Mide karsinomunun overe dökülmesi Krukenberg tümörüdür; apendiks müsinöz tümörünün karnı jelatinle doldurması Psödömiksoma peritoneidir.",
            "note": "Peritoneal karsinomatozis geliştiğinde malign assit oluşur; parasentez sıvısında malign hücreler aranır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Transçölomik Ekim (Kaviter Yayılım)
Malign bir neoplazm doğal bir vücut boşluğunu (periton, plevra, perikard veya subaraknoid boşluk) delip içine açıldığında tümör hücreleri bu seröz sıvı içerisinde serbestçe yüzerek boşluğun diğer yüzeylerine ekilir.

#### 1. Peritoneal Ekim ve Krukenberg Tümörü:
- **Krukenberg Tümörü:** Genellikle mide taşlı yüzük hücreli karsinomunun (veya kolon/safra yolu karsinomlarının) peritoneal boşluğa dökülerek **her iki overe (bilateral)** metastaz yapmasıdır.
- Mikroskopisinde müsinle dolu sitoplazması çekirdeği kenara itmiş **taşlı yüzük hücreleri** ve yoğun stromal desmoplazi görülür.

#### 2. Psödömiksoma Peritonei (Jöle Karın):
- Apendiksin müsinöz neoplazmlarının (adenom veya adenokarsinom) periton boşluğuna rüptüre olmasıyla gelişir.
- Karın boşluğu litrelerce jelatinöz müsinöz kitleyle dolar; bağırsak anslarını birbirine yapıştırarak obstrüksiyona yol açar.

#### 3. Plevral ve Perikardiyal Ekim:
- Akciğer ve meme karsinomları plevral boşluğa ekilerek **Malign Plevral Efüzyon** (kanlı/eksüda vasfında sıvı) oluşturur.

#### 4. Santral Sinir Sistemi (Subaraknoid Ekim):
- Medulloblastom ve ependimom gibi pediatrik beyin tümörleri BOS içerisine dökülerek omurilik boyunca yayılır (*Drop metastaz*).""",
        "spotPearls": [
            "🔴 Mide karsinomunun (taşlı yüzük hücreli) peritoneal ekim yoluyla overlere bilateral metastazına **Krukenberg Tümörü** denir.",
            "🔵 ==blue:Apendiksin müsinöz karsinomunun periton boşluğunu litrelerce jelatinöz müsinle doldurması tablosuna Psödömiksoma Peritonei adı verilir.==",
            "⚡ Medulloblastom BOS yoluyla omuriliğe 'drop metastaz' yaparak transçölomik yayılım sergiler."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Krukenberg", "text": "Mideden overe bilateral taşlı yüzük hücreli metastaz."},
                {"label": "Psödömiksoma Peritonei", "text": "Apendiks müsinöz tümörünün peritoneal yayılımı."},
                {"label": "Malign Sıvı", "text": "Kaviter ekim sonucu hemorajik eksüdatif effüzyon."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-16-1",
                "front": "Mide taşlı yüzük hücreli karsinomunun peritoneal boşluk yoluyla her iki overe yaptığı metastaza ne ad verilir?",
                "back": "Krukenberg Tümörü.",
                "facultyNote": "Bilateral over kitleleri şeklinde ortaya çıkar."
            },
            {
                "id": "tb-fc-16-2",
                "front": "Apendiks kökenli müsin üreten tümörlerin peritonu yoğun jelatinöz sıvıyla kaplaması durumuna ne ad verilir?",
                "back": "Psödömiksoma Peritonei.",
                "facultyNote": "Klinikte jöle karın tablosu olarak da bilinir."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-16",
            "question": "Kırk beş yaşında kadın hastada bilateral over kitleleri saptanıyor. Rezeksiyon materyalinde müsin dolu sitoplazmaları nükleusu perifere itmiş taşlı yüzük hücreleri izleniyor. Bu hastada primer tümör odağı öncelikle hangi organda aranmalıdır?",
            "options": [
                "A) Tiroid bezi",
                "B) Mide",
                "C) Böbrek korteksi",
                "D) Kemik iliği",
                "E) Beyin serebellumu"
            ],
            "answer": "B",
            "explanation": "Overlerde bilateral taşlı yüzük hücreli karsinom saptanması klasik Krukenberg tümörüdür. Krukenberg tümörünün en sık primer kaynağı mide karsinomudur (özellikle diffüz tip mide kanseri).",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 17,
        "title": "Benign ve Malign Neoplazmların Karşılaştırma Matrisi",
        "subtitle": "Klinik ve patolojik 6 temel parametrede tam karşılaştırma tablosu.",
        "badge": "Özet Tablo",
        "badgeColor": "accent",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Sınavda benign mi malign mi sorusu gelirse zihninizde bu tablo canlanmalı: Diferansiasyon, büyüme hızı, kapsül, lokal invazyon ve metastaz. Bu beş sütun tüm patolojinin temelidir.",
            "note": "Tablodaki kriterlerin birbiriyle tutarlılığı tanı koymada rehberdir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Benign ve Malign Tümörlerin Karşılaştırmalı Özeti
Tümör patolojisinin omurgasını oluşturan 6 temel kriterin sistematik karşılaştırması:

| Parametre | Benign (İyi Huylu) Neoplazm | Malign (Kötü Huylu) Neoplazm |
| :--- | :--- | :--- |
| **Diferansiasyon** | **İyi diferansiye;** kaynak dokuya morfolojik ve fonksiyonel olarak çok benzer. | **Değişken diferansiyasyon;** kötü diferansiye veya tamamen anaplazik olabilir. |
| **Büyüme Hızı** | Genellikle **yavaş ve progresif;** aylar/yıllar içinde büyür (hormonlara bağımlı durabilir). | Genellikle **hızlı ve kontrolsüz;** mitotik indeks yüksektir. |
| **Mitoz Özelliği** | Az sayıda, normal simetrik bipolar mitotik figürler. | Sayıca çok artmış ve **atipik (tripolar, kuadripolar bizar)** mitozlar. |
| **Sınırlar & Kapsül** | **Düzgün sınırlı, fibröz kapsüllü;** ekspansif (itici) büyür. | **Kapsülsüz, düzensiz sınırlı;** çevre dokuya infiltre ve fikse. |
| **Lokal İnvazyon** | **Lokal invazyon YAPMAZ;** çevre dokuyu tahrip etmez, iter. | **Lokal invazyon YAPAR;** bazal membranı, damar ve sinirleri delip yıkar. |
| **Metastaz** | **KESİNLİKLE YAPMAZ!** | **YAPABİLİR / YAPAR;** malignitenin kesin kanıtıdır. |

#### Klinik Davranış Farkı:
- Benign tümörler yalnızca anatomik lokalizasyonları kritikse (örneğin kafa içinde menenjiyomun beyin sapına bası yapması veya epiglottaki bir papillomun asfiksi yapması) hayati tehlike yaratır.
- Malign tümörler ise nerede çıkarsa çıksın tedavi edilmediğinde metastaz ve doku yıkımıyla ölüme yol açar.""",
        "spotPearls": [
            "🔴 Benign tümörler **kapsüllü, iyi diferansiye ve lokal** kalırken; malign tümörler **kapsülsüz, anaplazik, invaziv ve metastatiktir**.",
            "🔵 ==blue:Benign lezyonlarda mitotik figürler daima bipolar ve düzenlidir; tripolar/kuadripolar bizar mitozlar maligniteye özgüdür.==",
            "⚡ Benign bir tümör bile beyin sapı gibi kapalı ve hayati bir anatomik boşlukta yerleştiğinde mekanik bası ile ölüme yol açabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Diferansiyasyon", "text": "Benign = İyi diferansiye; Malign = Anaplaziye kadar değişir."},
                {"label": "İnvazyon", "text": "Benign iterek büyür; Malign yıkarak sızar."},
                {"label": "Metastaz", "text": "Benignte sıfır; Malignde var."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-17-1",
                "front": "Benign bir neoplazm hastanın ölümüne neden olabilir mi?",
                "back": "Evet; kritik bir anatomik bölgeye (örneğin kafa içi foramen magnum veya kalp kapakçığı) mekanik bası yaparak ölümcül olabilir.",
                "facultyNote": "Biyolojik olarak iyi huylu olsa da klinik olarak ölümcül yerleşim gösterebilir."
            },
            {
                "id": "tb-fc-17-2",
                "front": "Bir dokuda mitoz görülmesi o dokunun kesinlikle kanser olduğunu gösterir mi?",
                "back": "Hayır; mitoz sayısı normal rejenerasyonda da artabilir. Önemli olan mitozun tripolar/atipik olmasıdır.",
                "facultyNote": "Kemik iliğinde veya kript epitelinde de mitoz çok sıktır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-17",
            "question": "Aşağıdaki özelliklerden hangisi bir neoplazmın benign veya malign olduğunu ayırt etmede KULLANILAMAZ?",
            "options": [
                "A) Uzak organ metastazı yapması",
                "B) Tümör hücrelerinin sitoplazmik büyüklüğü",
                "C) Çevre dokulara infiltratif büyüme paterni",
                "D) Kapsül varlığı ve sınırların düzgün olması",
                "E) Tripolar atipik mitotik figürlerin varlığı"
            ],
            "answer": "B",
            "explanation": "Sadece sitoplazmik büyüklük benign/malign ayrımında kullanılamaz (bazı benign onkositoma hücreleri de dev sitoplazmalıdır). Metastaz, infiltrasyon, kapsül ve atipik mitoz ise kesin ayırt edici parametrelerdir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 18,
        "title": "Kanser Epidemiyolojisi: İnsidans ve Mortalite Dinamikleri",
        "subtitle": "Dünyada ve Türkiye'de cinsiyete göre en sık görülen ve en çok öldüren kanserler.",
        "badge": "Epidemiyoloji",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Erkeklerde en sık görülen kanser prostat, kadınlarda memedir. Ancak hem erkekte hem kadında kanserden ölümlerde bir numaralı katil AKCİĞER KANSERİDİR!",
            "note": "İnsidans (yeni vaka) ile mortalite (ölüm) sıralaması sınavların vazgeçilmez istatistik sorusudur.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kanser İnsidansı ve Mortalite İstatistikleri
Kanserin sıklığı yaş, cinsiyet, coğrafi bölge ve genetik faktörlere göre değişkenlik gösterir:

#### 1. En Sık Görülen Kanserler (İnsidans Sıralaması):
- **Erkeklerde:**
  1. **Prostat Kanseri** (En sık yeni tanı)
  2. Akciğer Kanseri
  3. Kolorektal Kanser
- **Kadınlarda:**
  1. **Meme Kanseri** (En sık yeni tanı)
  2. Akciğer Kanseri
  3. Kolorektal Kanser

#### 2. Kansere Bağlı Ölümlerde İlk Sıralar (Mortalite Sıralaması):
- **Erkeklerde:**
  1. **AKCİĞER KANSERİ** (Açık ara en sık ölüm nedeni)
  2. Prostat Kanseri
  3. Kolorektal Kanser
- **Kadınlarda:**
  1. **AKCİĞER KANSERİ** (Kadınlarda da meme kanserini geçerek 1. sıraya yerleşmiştir!)
  2. Meme Kanseri
  3. Kolorektal Kanser

> 🔴 **Sınav Tuzağı:** ==red:Kadınlarda en sık GÖRÜLEN kanser MEME kanseridir; ancak kadınlarda kansere bağlı en çok ÖLÜME yol açan kanser AKCİĞER kanseridir!== (Nedeni sigara tüketiminin artması ve akciğer kanserinin geç evrede saptanmasıdır).

#### Coğrafi Farklılıklar:
- **Japonya:** Mide kanseri sıklığı ABD'ye göre 7-8 kat fazladır (tütsülenmiş gıdalar, H. pylori suşları).
- Göçmen Çalışmaları: Japonlar ABD'ye göç edip Batı tipi beslendiğinde mide kanseri riski azalmakta, kolon kanseri riski artmaktadır (çevresel faktörlerin baskınlığı kanıtı).""",
        "spotPearls": [
            "🔴 Erkeklerde en sık görülen kanser **Prostat**, kadınlarda ise **Meme** kanseridir.",
            "🔵 ==blue:Hem erkeklerde hem kadınlarda kansere bağlı ölümlerde 1. sırada yer alan kanser türü AKCİĞER KANSERİDİR.==",
            "⚡ Japonya'da mide kanseri insidansı yüksektir; ABD'ye göç eden nesillerde kolon kanseri sıklığı artar (çevresel etki ispatı)."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Erkek İnsidans", "text": "Prostat > Akciğer > Kolorektal."},
                {"label": "Kadın İnsidans", "text": "Meme > Akciğer > Kolorektal."},
                {"label": "Ortak 1. Mortalite", "text": "Akciğer Kanseri (Erkek ve kadında en ölümcül)."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-18-1",
                "front": "Kadınlarda en sık görülen kanser türü ile en çok ölüme neden olan kanser türü sırasıyla hangileridir?",
                "back": "En sık görülen Meme kanseri; en çok ölüme neden olan Akciğer kanseridir.",
                "facultyNote": "TUS ve komite sınavlarının en klasik istatistik sorusudur."
            },
            {
                "id": "tb-fc-18-2",
                "front": "Kanserin gelişiminde çevresel faktörlerin genetik faktörlerden daha belirleyici olduğunu gösteren en güçlü epidemiyolojik kanıt nedir?",
                "back": "Göçmen çalışmalarıdır (örneğin Japonların ABD'ye göç ettiklerinde kolon kanseri insidansının artması).",
                "facultyNote": "Beslenme ve yaşam tarzı riski değiştirir."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-18",
            "question": "Güncel epidemiyolojik verilere göre, kadınlarda kansere bağlı ölümlerde birinci sırada yer alan kanser türü aşağıdakilerden hangisidir?",
            "options": [
                "A) Meme karsinomu",
                "B) Akciğer karsinomu",
                "C) Serviks karsinomu",
                "D) Over karsinomu",
                "E) Kolorektal karsinom"
            ],
            "answer": "B",
            "explanation": "Kadınlarda en sık tanı konulan kanser meme kanseri olmasına rağmen, kansere bağlı ölümlerde ilk sırayı hem erkeklerde hem kadınlarda Akciğer Karsinomu almaktadır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 19,
        "title": "Çevresel Karsinojenler ve Mesleki Maruziyetler",
        "subtitle": "Kimyasal, fiziksel ve mikrobiyal karsinojenlerin spesifik organ hedefleri.",
        "badge": "Etiyoloji",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Belli karsinojenler belli organ tümörlerine imza atar: Asbest mezotelyoma, Aflatoksin hepatosellüler karsinom, Anilin boyaları mesane kanseri, Vinil klorür ise karaciğer anjiyosarkomu yapar!",
            "note": "Bu eşleştirmeler amfide hocanın slaytlarında tek tek altı çizilen klasik sorulardır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kimyasal ve Çevresel Karsinojenlerin Hedef Organları
Kanserlerin %70-80'i çevresel faktörlerle (sigara, beslenme, kimyasallar, radyasyon, enfeksiyonlar) tetiklenir:

#### Majör Mesleki ve Kimyasal Karsinojenler:
- **Asbest:**
  - Plevral ve peritoneal **Malign Mezotelyoma** (en spesifik tümörü).
  - Ayrıca sigara ile sinerjistik etki göstererek **Akciğer Karsinomu** riskini katbekat artırır.
- **Aflatoksin B1 (Aspergillus flavus):**
  - Nemli tahıl ve kuruyemişlerde üreyen mantar toksinidir.
  - **TP53 geninde 249. kodonda spesifik G:C → T:A transversiyonu** yaparak **Hepatosellüler Karsinom (HCC)** oluşturur.
- **Vinil Klorür Monomeri:**
  - Plastik (PVC) sanayi işçilerinde görülür.
  - Karaciğerin nadir malign endotel tümörü olan **Hepatik Anjiyosarkom**a yol açar.
- **Aromatik Aminler ve Azo Boyaları (Anilin, 2-Naftilamin):**
  - Boya, kauçuk ve tekstil sanayi işçilerinde idrarla atılırken transizyonel epiteli etkiler → **Mesane Ürotelyal Karsinomu**.
- **Arsenik:**
  - İçme suyu kirliliği ve tarım ilaçları → **Deride Skuamöz Hücreli Karsinom** ve Akciğer kanseri.
- **Alkilleyici Ajanlar (Siklofosfamid vb.):**
  - Kanser kemoterapisinde kullanılır; ancak DNA hasarı yaparak yıllar sonra **Sekonder Akut Miyeloid Lösemi (AML)** oluşturabilir.""",
        "spotPearls": [
            "🔴 Plastik/PVC sanayisinde çalışan işçilerde karaciğerde **Hepatik Anjiyosarkom** yapan karsinojen **Vinil Klorür**dür.",
            "🔵 ==blue:Aflatoksin B1, p53 geninde 249. kodon mutasyonu yaparak Hepatosellüler Karsinom (HCC) riskini dramatik artırır.==",
            "⚡ Boya ve kauçuk sanayi işçilerinde mesane kanserine yol açan kimyasallar **Aromatik Aminler (Anilin / 2-Naftilamin)**dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Asbest", "text": "Mezotelyoma + Akciğer karsinomu."},
                {"label": "Aflatoksin", "text": "p53 kodon 249 mutasyonu ile Hepatosellüler Karsinom."},
                {"label": "Vinil Klorür", "text": "Karaciğer Anjiyosarkomu (plastik sanayi)."},
                {"label": "Anilin Boyaları", "text": "Mesane Ürotelyal Karsinomu."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-19-1",
                "front": "Plastik (PVC) endüstrisinde çalışan bir işçide karaciğerde gelişen malign vasküler endotel tümörü nedir ve etken karsinojen hangisidir?",
                "back": "Hepatik Anjiyosarkom; etken Vinil Klorürdür.",
                "facultyNote": "TUS sınavlarında mesleki karsinojen sorularının vazgeçilmezidir."
            },
            {
                "id": "tb-fc-19-2",
                "front": "Boya ve tekstil fabrikasında uzun yıllar çalışan bir işçide hematüri saptandığında öncelikle hangi organ kanseri araştırılmalıdır?",
                "back": "Mesane karsinomu (Aromatik aminler / Anilin boyaları nedeniyle).",
                "facultyNote": "2-naftilamin idrarla atılırken mesane ürotelyumunu karsinojenize eder."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-19",
            "question": "Aşağıdaki karsinojen maddelerden hangisi p53 tümör supresör geninin 249. kodonunda spesifik bir mutasyona yol açarak Hepatosellüler Karsinom gelişimini tetikler?",
            "options": [
                "A) Asbest lifleri",
                "B) Aflatoksin B1",
                "C) Vinil klorür",
                "D) Benzen",
                "E) Dietilstilbestrol (DES)"
            ],
            "answer": "B",
            "explanation": "Aspergillus flavus mantarının ürettiği Aflatoksin B1, TP53 geninin 249. kodonunda karakteristik mutasyona (arginin yerine serin) yol açarak özellikle hepatit B virüsü ile sinerjistik şekilde karaciğer kanserini (HCC) tetikler.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 20,
        "title": "Onkojenik Virüsler ve İnsan Kanserleri",
        "subtitle": "HPV, EBV, HBV/HCV, HTLV-1 ve HHV-8 karsinojenez mekanizmaları.",
        "badge": "Onkovirüsler",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Onkojenik DNA virüsleri hücrenin fren mekanizmalarını bozar: HPV'nin E6 proteini p53'ü parçalar, E7 proteini ise RB'yi bağlayarak hücre siklusunu serbest bırakır!",
            "note": "E6 = p53 yıkımı, E7 = RB inaktivasyonu. Bu iki viral onkoprotein patolojinin en yüksek verimli ezber bilgisidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kanser Yapan Majör Onkojenik Virüsler
Dünyadaki tüm kanserlerin yaklaşık %15'i enfeksiyöz ajanlarla, özellikle onkojenik virüslerle ilişkilidir:

#### 1. Human Papillomavirus (HPV):
- **Yüksek Riskli Tipler:** **HPV Tip 16 ve 18** (Serviks, anogenital bölge, orofaringeal kanserler).
- **Mekanizma:**
  - **E6 Onkoproteini:** **p53** tümör supresör proteinine bağlanarak ubikuitinasyonunu ve proteazomda parçalanmasını sağlar (apoptoz engellenir).
  - **E7 Onkoproteini:** **RB (Retinoblastom)** proteinine bağlanarak onu E2F'den ayırır; E2F serbest kalır ve hücreyi kontrolsüzce S fazına sokar.

#### 2. Epstein-Barr Virüsü (EBV):
- **İlişkili Kanserler:**
  - Nazofarenks Karsinomu (Güney Çin'de endemik).
  - Burkitt Lenfoma (Afrika endemik tipi, t(8;14) c-MYC translokasyonu ile sinerjistik).
  - Hodgkin Lenfoma (Karma hücresel tip) ve İmmünsüprese hastalarda B-hücreli lenfomalar.
- **Onkoprotein:** **LMP-1** (CD40 reseptörünü taklit ederek NF-κB ve JAK/STAT yolağını sürekli açık tutar).

#### 3. Hepatit B (HBV) ve Hepatit C (HCV):
- Kronik hepatit, karaciğer nekrozu ve rejeneratif hiperplazi zemininde **Hepatosellüler Karsinom (HCC)** yaparlar. HBV ayrıca **HBx proteini** ile transkripsiyonel aktivasyon sağlar.

#### 4. Human Herpesvirus 8 (HHV-8 / KSHV):
- Endotel hücrelerini transforme ederek **Kaposi Sarkomu**na yol açar (özellikle AIDS hastalarında mor/kırmızı kutanöz vasküler nodüller).

#### 5. HTLV-1 (Human T-Cell Leukemia Virus Type 1):
- İnsan kanseriyle doğrudan ilişkili tek **RNA retrovirüsüdür**.
- **Tax proteini** ile T hücrelerinde kontrolsüz poliklonal çoğalma başlatır → **Erişkin T-Hücreli Lösemi / Lenfoma (ATLL)**.""",
        "spotPearls": [
            "🔴 HPV onkoproteinlerinden **E6, p53'ü yıkar**; **E7 ise RB proteinini inaktive eder**.",
            "🔵 ==blue:İnsan kanserine yol açan tek retrovirüs (RNA virüsü) HTLV-1'dir; Tax proteini aracılığıyla Erişkin T-Hücreli Lösemi/Lenfoma yapar.==",
            "⚡ Nazofarenks karsinomu ve Afrika tipi Burkitt lenfoma ile doğrudan ilişkili onkojenik virüs **EBV**dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "HPV 16/18", "text": "E6 p53'ü yıkar, E7 RB'yi inaktive eder."},
                {"label": "EBV", "text": "LMP-1 ile B hücre ölümsüzleşmesi; Burkitt ve Nazofarenks karsinomu."},
                {"label": "HHV-8", "text": "Kaposi Sarkomu."},
                {"label": "HTLV-1", "text": "Tek onkojenik retrovirüs; Erişkin T hücreli lösemi."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-20-1",
                "front": "Yüksek riskli HPV (Tip 16 ve 18) suşlarının ürettiği E6 ve E7 viral onkoproteinlerinin konak hücredeki hedefleri nelerdir?",
                "back": "E6 p53 proteinini bağlayıp yıkar; E7 ise RB proteinini bağlayıp inaktive eder.",
                "facultyNote": "Her komitede ve TUS'ta sorgulanan kilit mekanizmadır."
            },
            {
                "id": "tb-fc-20-2",
                "front": "HIV pozitif bir hastada deride ve mukozalarda mor-kırmızı vasküler nodüller oluşturan Kaposi sarkomunun etkeni olan virüs nedir?",
                "back": "HHV-8 (Human Herpesvirus 8 / KSHV).",
                "facultyNote": "Vasküler endoteli neoplastik olarak transforme eder."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-20",
            "question": "Onkojenik DNA virüsü olan Human Papillomavirus (HPV) tip 16 infeksiyonunda, viral E6 onkoproteininin konak hücrede doğrudan bağlanarak proteazomal yıkımına yol açtığı temel tümör supresör protein hangisidir?",
            "options": [
                "A) Retinoblastom (RB)",
                "B) p53 (TP53)",
                "C) APC",
                "D) VHL",
                "E) WT1"
            ],
            "answer": "B",
            "explanation": "HPV'nin E6 onkoproteini p53'e bağlanarak ubiquitin ligaz (E6AP) aracılığıyla parçalanmasını sağlar; E7 proteini ise RB proteinini inaktive eder.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 21,
        "title": "Kalıtsal Kanser Sendromları ve Genetik Yatkınlık",
        "subtitle": "Knudson'ın iki vuruş (two-hit) hipotezi, BRCA, Lynch, FAP ve Li-Fraumeni.",
        "badge": "Genetik Yatkınlık",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kalıtsal kanserlerde hasta doğuştan birinci darbeyi (first-hit) alarak doğar; bu yüzden kanserler çok erken yaşta ve bilateral/multifokal olarak ortaya çıkar.",
            "note": "Knudson hipotezi retinoblastom modelinde gösterilmiştir: Kalıtsal olanda tek bir somatik mutasyon yeterlidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Knudson İki Vuruş (Two-Hit) Modeli ve Kalıtsal Sendromlar
Tümör supresör genlerin inaktivasyonunda geçerli olan genel kuraldır:
- Hücrenin malign transformasyonu için bir tümör supresör genin **her iki alelinin de (hem maternal hem paternal)** inaktive olması gerekir.
- **Kalıtsal Kanserlerde:** Birey bir mutasyonlu aleli germ-line olarak anne veya babasından miras alır (**1. Vuruş** tüm vücut hücrelerinde mevcuttur). Yaşamı boyunca tek bir hedef doku hücresinde sağlam kalan ikinci alelin de mutasyona uğraması (**2. Vuruş**) kanser başlatır. Bu nedenle:
  - Çok daha **erken yaşta** görülürler.
  - Sıklıkla **bilateral** (iki taraflı) ve **multifokal** (çok odaklı) kitleler yaparlar.
- **Sporadik Kanserlerde:** Birey iki sağlam alelle doğar; aynı hücrede rastlantısal olarak her iki vuruşun da peş peşe gerçekleşmesi gerekir (bu yüzden ileri yaşta ve tek taraflı görülür).

#### Majör Kalıtsal Kanser Sendromları:
1. **Retinoblastom Sendromu:** **RB1** geni mutasyonu (13q14). Erken çocuklukta bilateral retinoblastom ve ileri yaşta osteosarkom riski.
2. **Li-Fraumeni Sendromu:** **TP53** germ-line mutasyonu. Çok genç yaşta sarkomlar, meme kanseri, lösemi, beyin tümörleri ve adrenal korteks karsinomu (SBLA sendromu).
3. **Kalıtsal Meme-Over Kanseri:** **BRCA1 ve BRCA2** genleri (Homolog rekombinasyon DNA tamir defekti). Meme kanseri ve over karsinomu riski.
4. **Familyal Adenomatoz Polipozis (FAP):** **APC** geni mutasyonu (5q21). Kolonda 100'den fazla (binlerce) adenomatoz polip; 40 yaşına kadar tedavi edilmezse %100 kolon kanseri gelişir!
5. **Lynch Sendromu (HNPCC):** DNA uyumsuzluk tamir (**Mismatch Repair - MSH2, MLH1**) genleri defekti. Polipsiz veya az polipli erken yaş sağ kolon kanseri ve endometriyal karsinom.""",
        "spotPearls": [
            "🔴 Knudson iki vuruş hipotezine göre kalıtsal kanserler doğuştan 1. vuruşu taşırlar; bu yüzden **erken yaşta, bilateral ve multifokal** çıkarlar.",
            "🔵 ==blue:Kolonda yüzlerce polip ve 40 yaşına kadar %100 kolon kanseri gelişimi ile seyreden sendrom FAP (APC geni mutasyonu) dur.==",
            "⚡ **Li-Fraumeni sendromu**, TP53 geninin germ-line mutasyonu sonucu genç yaşta sarkom, meme kanseri ve lösemi birlikteliğidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Two-Hit Kuralı", "text": "Tümör supresör genlerde iki alelin de inaktivasyonu şarttır."},
                {"label": "FAP (APC geni)", "text": "Binlerce kolon polipi; %100 kanserleşme."},
                {"label": "Li-Fraumeni", "text": "Kalıtsal p53 defekti; genç yaş sarkom ve meme kanseri."},
                {"label": "Lynch (HNPCC)", "text": "Mismatch repair defekti ve Mikrosatellit instabilitesi."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-21-1",
                "front": "Kolonoskopide kolonda 100'den fazla (binlerce) tübüler adenom saptanan ve tedavi edilmezse %100 kolorektal karsinom gelişen sendrom ve ilişkili gen nedir?",
                "back": "Familyal Adenomatoz Polipozis (FAP); sorumlu gen 5q21'deki APC genidir.",
                "facultyNote": "Profilaktik total kolektomi hayat kurtarır."
            },
            {
                "id": "tb-fc-21-2",
                "front": "Genç yaşta osteosarkom, meme kanseri, lösemi ve beyin tümörü saptanan bir hastada hangi tümör supresör genin germ-line mutasyonu düşünülmelidir?",
                "back": "TP53 geni germ-line mutasyonu (Li-Fraumeni Sendromu).",
                "facultyNote": "Tümör supresör genlerin anası olan p53'ün kalıtsal hastalığıdır."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-21",
            "question": "Yirmi sekiz yaşında bir hastada kolonoskopide kalın bağırsağın tüm segmentlerini dolduran 1500 adet adenomatoz polip saptanmıştır. Bu hastadaki genetik bozukluk ve mutasyona uğrayan gen aşağıdakilerden hangisidir?",
            "options": [
                "A) BRCA1 geni delesyonu",
                "B) VHL geni translokasyonu",
                "C) APC geni mutasyonu (FAP sendromu)",
                "D) RET onkogen mutasyonu",
                "E) WT1 geni duplikasyonu"
            ],
            "answer": "C",
            "explanation": "Kolonda 100'ün üzerinde (genellikle binlerce) adenomatoz polip bulunması Familyal Adenomatoz Polipozis (FAP) için karakteristiktir ve 5q21 kromozomundaki APC tümör supresör geninin germ-line mutasyonu sonucu ortaya çıkar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 22,
        "title": "Kanser Kaşeksisi ve Paraneoplastik Sendromlar",
        "subtitle": "Metabolik erime, hormonal ve nörolojik paraneoplaziler.",
        "badge": "Klinik Etki",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kaşeksinin sebebi tümörün hastanın yemeğini yemesi değildir; konak makrofajlarının ve tümörün salgıladığı TNF-alfa (Kaşektin) ve sitokinlerin iştahı kapatıp yağ ve kası eritmesidir!",
            "note": "Paraneoplastik sendromlar ise tümörün primer kitlesi veya metastazı ile açıklanamayan sistemik bulgulardır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kanser Kaşeksisi ve Paraneoplastik Tezahürler
Kanserin konakçı üzerindeki sistemik etkileri:

#### 1. Kanser Kaşeksisi:
İlerlemiş kanser hastalarında görülen, kalori alımından bağımsız olarak ilerleyici yağ ve iskelet kası kaybı, derin halsizlik, anemi ve iştahsızlık tablosudur.
- **Patofizyoloji:** Tümörün kendisinden ve tümöre yanıt veren konak bağışıklık hücrelerinden salınan sistemik sitokinler sorumludur:
  - **TNF-α (Kaşektin):** Hipotalamusta iştah merkezini baskılar ve lipoprotein lipazı inhibe ederek adipositlerden yağ asidi salınımını tetikler.
  - **IL-1, IL-6 ve İnterferon-gama:** Kas proteinlerinin ubikuitin-proteazom yolağı ile yıkımını hızlandırır.

#### 2. Paraneoplastik Sendromlar:
Tümörün lokal invazyonu, metastaz kitlesi veya o dokunun normal hormon salgısıyla **açıklanamayan**, tümör hücrelerinin ektopik hormon, peptid veya antikor üretmesiyle gelişen semptomlar kompleksidir. Kanser hastalarının %10-15'inde görülür.

#### En Sık ve Kritik Paraneoplastik Sendromlar:
- **Cushing Sendromu:** Küçük hücreli akciğer karsinomunun ektopik **ACTH** üretmesi.
- **Uygunsuz ADH Sendromu (SIADH):** Küçük hücreli akciğer karsinomunun ektopik **ADH** üretmesi (hiponatremi).
- **Hiperkalsemi:**
  - Akciğer Skuamöz Hücreli Karsinomunun **PTHrP (Paratiroid Hormon İlişkili Peptid)** salgılaması (Kemik metastazı olmaksızın hiperkalsemi!).
  - Meme karsinomunun osteolitik kemik metastazları.
- **Polisitemi (Eritrositoz):** Renal Hücreli Karsinom veya Serebellar Hemanjoblastomun aşırı **Eritropoetin (EPO)** salgılaması.
- **Trousseau Sendromu (Migratuar Tromboflebit):** Pankreas ve mide adenokarsinomlarının müsin ve prokoagülan salgılayarak tekrarlayan venöz trombozlar oluşturması.""",
        "spotPearls": [
            "🔴 Kanser kaşeksisinin ana mediyatörü, yağ ve iskelet kası yıkımını tetikleyen **TNF-alfa (Kaşektin)**dır.",
            "🔵 ==blue:Akciğer Skuamöz Hücreli Karsinomunda kemik metastazı olmadan hiperkalsemiye yol açan paraneoplastik ajan PTHrP'dir.==",
            "⚡ Pankreas kanserinde gezici yüzeyel venöz trombozlarla seyreden paraneoplastik tabloya **Trousseau Sendromu (Migratuar tromboflebit)** denir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "TNF-alfa", "text": "Kanser kaşeksisinin majör sürükleyicisi (kas ve yağ yıkımı)."},
                {"label": "PTHrP", "text": "Skuamöz akciğer karsinomunda ektopik hiperkalsemi nedeni."},
                {"label": "Trousseau", "text": "Pankreas kanserinde müsin kaynaklı migratuar tromboflebit."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-22-1",
                "front": "Akciğer skuamöz hücreli karsinomu tanılı bir hastada kemik sintigrafisi temiz olmasına rağmen gelişen ciddi hiperkalseminin sebebi nedir?",
                "back": "Tümör hücrelerinin ektopik olarak PTHrP (Paratiroid Hormon İlişkili Peptid) salgılamasıdır.",
                "facultyNote": "Kemik metastazı olmadan gelişen klasik paraneoplastik hiperkalsemidir."
            },
            {
                "id": "tb-fc-22-2",
                "front": "Pankreas başı adenokarsinomu olan hastada bacaklarda gezici yüzeyel ven trombozları gelişmesi hangi paraneoplastik sendromdur?",
                "back": "Trousseau Sendromu (Tromboflebitis migrans).",
                "facultyNote": "Tümörden kana karışan müsin pıhtılaşma kaskadını tetikler."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-22",
            "question": "Akciğer hilusunda kitle saptanan ve biyopsisinde Küçük Hücreli Karsinom tanısı alan 60 yaşındaki bir hastada serum sodyum düzeyi 118 mEq/L (şiddetli hiponatremi) saptanmıştır. Bu tabloya yol açan en olası paraneoplastik sendrom ve ektopik hormon aşağıdakilerden hangisidir?",
            "options": [
                "A) Cushing Sendromu — Ektopik Kortizol",
                "B) Uygunsuz ADH Sendromu (SIADH) — Ektopik Vazopressin (ADH)",
                "C) Hiperkalsemi — Ektopik PTHrP",
                "D) Polisitemi — Ektopik Eritropoetin",
                "E) Karsinoid Sendrom — Ektopik Serotonin"
            ],
            "answer": "B",
            "explanation": "Küçük hücreli akciğer karsinomunun en sık yol açtığı paraneoplastik sendromlardan biri Uygunsuz ADH Salınımı Sendromudur (SIADH). Ektopik ADH su tutulumuna ve dilüsyonel hiponatremiye yol açar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 23,
        "title": "Tümör Derecelendirmesi (Grading) ve Evrelemesi (Staging)",
        "subtitle": "Histolojik diferansiasyon (Grade) vs Klinik-anatomik yaygınlık (TNM Evresi).",
        "badge": "Evre & Grade",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bunu klinisyenler de patologlar da çok iyi bilmelidir: Derece (Grade) mikroskoba aittir; Evre (Stage) ise hastanın vücudundaki yaygınlığa aittir. Prognozu ve tedaviyi belirlemede Evre, Dereceden çok daha üstündür!",
            "note": "Evrelemede uluslararası standart TNM sistemidir: T primer tümör boyutu/derinliği, N lenf nodu, M uzak metastaz.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Derece (Grading) ve Evre (Staging) Arasındaki Keskin Fark
Onkolojik patolojide bir kanser raporunun en kritik iki sonucudur:

#### 1. Tümör Derecelendirmesi (Grading):
- **Kim Belirler:** Yalnızca **Patolog** ışık mikroskobunda belirler.
- **Neye Dayanır:** Neoplastik hücrelerin diferansiasyon derecesine ve mitotik aktivitesine dayanır.
  - **Grade I (Düşük Derece / İyi Diferansiye):** Hücreler normal dokuya çok benzer, mitoz azdır.
  - **Grade II (Orta Derece / Orta Diferansiye):** Belirgin hücresel pleomorfizm ve ılımlı mitoz vardır.
  - **Grade III - IV (Yüksek Derece / Kötü Diferansiye - Anaplazik):** Hücreler tamamen ilkel ve anaplaziktir, bol atipik mitoz ve nekroz içerir.

#### 2. Tümör Evrelemesi (Staging):
- **Kim Belirler:** Patoloji, radyoloji ve cerrahi bulguların senteziyle ortak belirlenir.
- **Neye Dayanır:** Tümörün **anatomik yaygınlığına ve vücuda ne kadar dağıldığına** dayanır.
- **Uluslararası Standart: TNM Sistemi (AJCC / UICC):**
  - **T (Primer Tümör):** Primer tümörün boyutu ve lokal doku derinliği invazyonudur (T0: tümör yok, Tis: in situ, T1-T4: artan boyut ve derinlik).
  - **N (Bölgesel Lenf Nodu):** Bölgesel lenf nodlarına metastaz varlığı ve tutulan nod sayısıdır (N0: nod tutulumu yok, N1-N3: artan nod tutulumu).
  - **M (Uzak Metastaz):** Uzak organ metastazı varlığıdır (M0: uzak metastaz yok, M1: uzak organ metastazı var).

> 🔴 **Altın Sınav İlkesi:** ==red:Prognozu belirlemede ve onkolojik tedavi protokolünü seçmede EVRE (STAGE), DERECEDEN (GRADE) HER ZAMAN ÇOK DAHA DEĞERLİ VE ÜSTÜNDÜR!== 1 cm'lik Grade III bir tümör erken evredir ve şifaya kavuşabilir; oysa Grade I bile olsa uzak metastaz yapmış (Evre IV) bir tümörün prognozu çok daha kötüdür.""",
        "spotPearls": [
            "🔴 **Grade (Derece)** mikroskobik diferansiasyona dayanır; **Stage (Evre)** ise tümörün anatomik yaygınlığına (TNM) dayanır.",
            "🔵 ==blue:Kanser hastasının prognozunu (sağkalımını) belirlemede EVRE (STAGE), DERECEDEN (GRADE) çok daha güçlü bir belirleyicidir.==",
            "⚡ TNM sisteminde M1 varlığı, diğer parametreler ne olursa olsun hastayı doğrudan en yüksek evre olan **Evre IV** kategorisine sokar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Grade (Derece)", "text": "Histolojik farklılaşma; mikroskopta patolog belirler."},
                {"label": "Stage (Evre)", "text": "Anatomik yaygınlık; TNM sınıflaması (klinik + patoloji)."},
                {"label": "Klinik Önem", "text": "Evreleme tedavi ve prognoz için dereceden çok daha kritiktir."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-23-1",
                "front": "Tümörün 'Grade'i ile 'Stage'i arasındaki temel kavramsal fark nedir?",
                "back": "Grade mikroskobik diferansiyasyon ve mitoz derecesidir; Stage ise tümörün vücuttaki anatomik yaygınlığıdır (TNM).",
                "facultyNote": "Grade patoloğun mikroskobuna, Stage hastanın bedenindeki yayılıma bakar."
            },
            {
                "id": "tb-fc-23-2",
                "front": "Kanser hastalarında tedavi stratejisini seçmede ve prognozu öngörmede Evreleme mi yoksa Derecelendirme mi daha üstündür?",
                "back": "Evreleme (Staging / TNM) çok daha üstündür ve belirleyicidir.",
                "facultyNote": "Evre IV bir hasta iyi diferansiye olsa bile prognozu kötüdür."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-23",
            "question": "Malign bir tümörün klinik ve patolojik değerlendirmesinde prognozu belirlemede en güvenilir parametrenin 'Tümör Evresi (Stage)' olmasının temel gerekçesi aşağıdakilerden hangisidir?",
            "options": [
                "A) Yalnızca ışık mikroskobunda immünohistokimya ile ölçülebilmesi",
                "B) Tümörün primer boyutunu, lenf nodu tutulumunu ve uzak metastaz durumunu yansıtması",
                "C) Hücrelerin DNA ploidi düzeyini göstermesi",
                "D) Sadece benign lezyonlarda uygulanabilir olması",
                "E) Yaşlı hastalarda otomatik olarak Grade'e dönüşmesi"
            ],
            "answer": "B",
            "explanation": "Evreleme (Staging / TNM), tümörün anatomik yaygınlığını (boyut/derinlik, lenfatik tutulum ve uzak metastaz) ortaya koyduğu için prognozu ve sağkalımı dereceden (Grade) çok daha doğru yansıtır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 24,
        "title": "Tümör Belirteçleri ve Laboratuvar Tanı Yöntemleri",
        "subtitle": "Serum tümör belirteçleri, immünohistokimya ve moleküler patoloji yöntemleri.",
        "badge": "Laboratuvar",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Tümör belirteçleri (PSA, CEA, CA-125) tarama veya kesin primer tanı için değil; tedaviye yanıtı ve nüksü izlemek için kullanılır! Kesin tanı daima histopatolojik doku biyopsisidir.",
            "note": "İmmünohistokimyada sitokeratin karsinomu, vimentin sarkomu, CD45 ise lenfomayı kanıtlar.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kanser Tanısında Laboratuvar ve Tümör Belirteçleri
Kanser tanısında altın standart daima **histopatolojik biyopsi** incelemesidir. Serum tümör belirteçleri ve immünohistokimya tanıyı destekler ve takibi sağlar:

#### 1. Serum Tümör Belirteçleri (Biyomarkerlar):
Tümör hücreleri tarafından kana salınan protein, enzim veya hormonlardır.
- **Kullanım Amacı:** Kural olarak primer kanser taramasında veya kesin tanısında kullanılmazlar (özgüllük ve duyarlılıkları düşüktür). **En temel kullanım alanları: Tedaviye yanıtın izlenmesi ve nükslerin erken saptanmasıdır!**
- **Klasik Tümör Belirteçleri:**
  - **PSA (Prostat Spesifik Antijen):** Prostat karsinomu (BPH ve prostatitte de yükselebilir).
  - **CEA (Karsinoembriyonik Antijen):** Kolon, pankreas, mide ve meme karsinomları (tedavi sonrası yükselmesi nüks kanıtıdır).
  - **AFP (Alfa-Fetoprotein):** Hepatosellüler Karsinom (HCC) ve Testis Non-Seminom Germ Hücreli Tümörleri (Yolk sac tümörü).
  - **CA-125:** Over karsinomları.
  - **CA 19-9:** Pankreas ve safra yolu adenokarsinomları.
  - **hCG (İnsan Koryonik Gonadotropini):** Koryokarsinom ve trofoblastik tümörler.
  - **Kalsitonin:** Tiroid Medüller Karsinomu.

#### 2. İmmünohistokimya (İHK) Tanı Paneli:
Andiferansiye / anaplazik bir tümörün kökenini belirlemede antikor boyamaları esastır:
- **Sitokeratin (+):** Epitelyal köken → **Karsinom**.
- **Vimentin (+):** Mezenkimal köken → **Sarkom**.
- **LCA (CD45) (+):** Lökosit kökeni → **Lenfoma**.
- **S100, HMB-45, Melan-A (+):** Melanosit kökeni → **Melanom**.
- **Kromogranin ve Sinaptofizin (+):** Nöroendokrin diferansiyasyon → **Nöroendokrin Tümörler / Küçük Hücreli Karsinom**.""",
        "spotPearls": [
            "🔴 Serum tümör belirteçlerinin (PSA, CEA, CA-125) birincil kullanım amacı **kesin tanı koymak değil; tedavi yanıtını ve tümör nüksünü izlemektir**.",
            "🔵 ==blue:İmmünohistokimyasal boyamada Sitokeratin pozitifliği Karsinomu, Vimentin Sarkomu, CD45 (LCA) ise Lenfomayı kanıtlar.==",
            "⚡ Hepatosellüler karsinom ve testis yolk sac tümöründe yükselen fetal serum proteini **Alfa-Fetoprotein (AFP)**dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Tümör Belirteçleri", "text": "Nüks takibi ve yanıt izleminde kullanılır; primer tanı doku biyopsisidir."},
                {"label": "CEA & PSA", "text": "Kolon ve Prostat kanseri takip belirteçleri."},
                {"label": "İHK Paneli", "text": "Sitokeratin = Epitel, Vimentin = Mezenkim, CD45 = Lenfoid."}
            ]
        },
        "flashcards": [
            {
                "id": "tb-fc-24-1",
                "front": "Serum tümör belirteçlerinin (örneğin CEA veya CA-125) onkoloji pratiğindeki en güvenilir ve birincil kullanım amacı nedir?",
                "back": "Tedavi etkinliğini değerlendirmek ve cerrahi/kemoterapi sonrası nüksleri (tümörün geri dönüşünü) erken saptamaktır.",
                "facultyNote": "Tarama testi olarak özgüllükleri sınırlıdır; nüks takibinde çok değerlidir."
            },
            {
                "id": "tb-fc-24-2",
                "front": "Işık mikroskobunda anaplazik hücrelerden oluşan bir metastatik tümörün epitelyal kökenli (karsinom) olduğunu kanıtlayan immünohistokimyasal ara filaman boyası nedir?",
                "back": "Sitokeratindir (Cytokeratin).",
                "facultyNote": "Mezenkimal olsaydı Vimentin, nöroendokrin olsaydı Sinaptofizin boyanırdı."
            }
        ],
        "practiceQuestion": {
            "id": "tb-pq-24",
            "question": "Kolorektal adenokarsinom nedeniyle opere edilen ve tümör kitlesi cerrahi olarak tamamen çıkarılan bir hastanın takibinde, serumda aşağıdaki belirteçlerden hangisinin aylar sonra tekrar yükselmeye başlaması tümör nüksünü veya karaciğer metastazını en güçlü şekilde düşündürür?",
            "options": [
                "A) Kalsitonin",
                "B) Karsinoembriyonik Antijen (CEA)",
                "C) CA-125",
                "D) Asit fosfataz",
                "E) Troponin T"
            ],
            "answer": "B",
            "explanation": "CEA (Karsinoembriyonik antijen), kolorektal karsinomların tedavisinden sonra hastaların nüks ve metastaz açısından takibinde kullanılan en önemli serum tümör belirtecidir. Düzeyin yükselmesi nükse işaret eder.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-biyolojisi-terminolojisi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Merge all 24 slides together
all_slides = slides + remaining_slides + more_slides
assert len(all_slides) == 24, f"Slide count must be 24, got {len(all_slides)}"

# Synchronize content & synthesisNarrative, spotPearls & spots, practiceQuestion & relatedQuestions
for s in all_slides:
    s['content'] = s['synthesisNarrative']
    s['spots'] = s['spotPearls']
    if s.get('practiceQuestion'):
        s['relatedQuestions'] = [s['practiceQuestion']]

# Build Deck object
deck_tumor = {
    "id": "learn-tumor-biyolojisi-terminolojisi",
    "title": "Tümör Biyolojisi, Terminolojisi ve Neoplaziye Giriş",
    "shortTitle": "Tümör Biyolojisi ve Terminolojisi",
    "discipline": "Tıbbi Patoloji",
    "instructor": "Prof. Dr. Hikmet Keleş",
    "term": "Dönem 3",
    "committee": "Kurul 1",
    "sourceLectureId": "16)Tümör Biyolojisi ve Terminolojisi.pdf",
    "sourceDrivePath": "Meds_Drive_Root / Kurul 1 / Tıbbi Patoloji  / 16)Tümör Biyolojisi ve Terminolojisi.pdf",
    "overview": "Neoplazinin tanımı (Willis tanımı), benign ve malign tümör terminolojisi, diferansiasyon, anaplazi, lokal invazyon mekanizmaları, lenfatik ve hematojen metastaz yolları, kanser epidemiyolojisi, mesleki ve viral karsinojenler, paraneoplastik sendromlar ve TNM evrelemesini kapsayan 24 slaytlık kapsamlı Patoloji öğrenme güvertesi.",
    "highYieldPearls": [
        "Willis neoplazi tanımı: Başlatan uyaran ortadan kalksa bile büyümenin otonom biçimde sürmesidir.",
        "Malignite istisnaları: Melanom, Lenfoma, Seminom ve Mezotelyoma '-om' ile bitmesine rağmen tamamı maligndir.",
        "Karsinomlar ilk olarak lenfojen yayılırken; Sarkomlar hematojen yolla akciğere yayılır.",
        "BCC ve Glioblastom lokal olarak çok agresiftir ancak neredeyse hiç metastaz yapmazlar.",
        "HPV'nin E6 proteini p53'ü parçalar; E7 proteini ise RB'yi inaktive eder.",
        "Klinik prognozu ve tedaviyi belirlemede Evre (Stage / TNM), Dereceden (Grade) çok daha üstündür."
    ],
    "slides": all_slides
}

# Update interactive_learning_decks.json
existing_idx = -1
for idx, d in enumerate(decks):
    if d.get('id') == deck_tumor['id']:
        existing_idx = idx
        break

if existing_idx >= 0:
    decks[existing_idx] = deck_tumor
    print(f"Updated existing deck: {deck_tumor['id']}")
else:
    decks.append(deck_tumor)
    print(f"Added new deck: {deck_tumor['id']}")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"Saved to {DECKS_PATH}. Total decks: {len(decks)}")

# Add questions to study_questions chunk files (chunk_8 and chunk_9)
new_questions = [s['practiceQuestion'] for s in all_slides if s.get('practiceQuestion')]

with open(CHUNK8_PATH, 'r', encoding='utf-8') as f:
    chunk8 = json.load(f)

# Chunk 8 can hold up to 100 questions.
available_in_chunk8 = 100 - len(chunk8)
q_for_chunk8 = new_questions[:available_in_chunk8]
q_for_chunk9 = new_questions[available_in_chunk8:]

added_to_8 = 0
for q in q_for_chunk8:
    if not any(item['id'] == q['id'] for item in chunk8):
        chunk8.append(q)
        added_to_8 += 1

with open(CHUNK8_PATH, 'w', encoding='utf-8') as f:
    json.dump(chunk8, f, ensure_ascii=False, indent=2)

print(f"Added {added_to_8} questions to {CHUNK8_PATH}. Total in chunk_8: {len(chunk8)}")

# Load or create chunk_9.json
chunk9 = []
if os.path.exists(CHUNK9_PATH):
    with open(CHUNK9_PATH, 'r', encoding='utf-8') as f:
        chunk9 = json.load(f)

added_to_9 = 0
for q in q_for_chunk9:
    if not any(item['id'] == q['id'] for item in chunk9):
        chunk9.append(q)
        added_to_9 += 1

with open(CHUNK9_PATH, 'w', encoding='utf-8') as f:
    json.dump(chunk9, f, ensure_ascii=False, indent=2)

print(f"Added {added_to_9} questions to {CHUNK9_PATH}. Total in chunk_9: {len(chunk9)}")

# Now run build_chunked_study_questions.py to re-index all chunks cleanly
print("\nRe-indexing study questions manifest...")
os.system(f"{sys.executable} scripts/build_chunked_study_questions.py")
