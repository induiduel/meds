# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-16-s21",
        "title": "Organ Konjesyonuna Giriş: Hedef Organ Morfolojisi",
        "content": "Sistemik venöz ve pulmoner dolaşım bozukluklarının en belirgin vurduğu iki kilit hayati organ akciğer ve karaciğerdir:\n\n- **Makroskopiye Genel Bakış:** Konjesyone bir organ kesildiğinde yüzeyi ıslak, koyu kırmızı-bordo renkte ve yoğun kan sızdıran bir özellik gösterir.\n- **Mikroskopik Temel:** Histopatolojik incelemede kapillerler, venüller ve sinüzoidler aşırı derecede genişlemiş ve sıkışık eritrosit kitleleriyle dolmuştur.\n- **Zaman Faktörü (Akut vs Kronik):**\n  - **Akut Dönemde:** Esas bulgu damarlarda aşırı ani dolgunluk ve interstisyel seröz ödemdir; henüz hücre ölümü veya bağ dokusu gelişmemiştir.\n  - **Kronik Dönemde:** Süregelen hipoksi parankim hücrelerini öldürür; yerini yoğun fibrozise bırakır ve parçalanan eritrositlerden dolayı hemosiderin pigmenti birikir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Akut Organ Konjesyonu vs Kronik Organ Konjesyonu",
                "Akut Konjesyon Morfolojisi",
                "Damarlar tıkabasa eritrositle doludur; interstisyumda hafif ödem vardır, henüz skar ve pigment oluşmamıştır.",
                "Kronik Konjesyon Morfolojisi",
                "Parankim hücreleri ölmüştür; dokuda belirgin fibrozis ve hemosiderin yüklü makrofajlar hakimdir."
            ),
            make_cloze(
                "Konjesyona uğramış organların taze kesit yüzü makroskopik olarak ıslak görünümde olup yoğun venöz kan sızdırır.",
                "kan sızdırır",
                "Organ kesit yüzünden dışarı süzülen sıvı içeriği"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-16-s22",
        "title": "Akut Pulmoner Konjesyon: Patoloji ve Mikroskopik Bulgular",
        "content": "Akut pulmoner konjesyon, sol ventrikülün aniden yetersiz kalması (akut miyokard enfarktüsü veya akut kapak yetmezliği) sonucu gelişir:\n\n- **Patofizyoloji:** Sol ventrikül kanı aortaya pompalayamayınca sol atriyum ve pulmoner venlerde basınç aniden yükselir. Bu basınç geriye doğru akciğer kapillerlerine yansır.\n- **Mikroskopik Görünüm:**\n  - Alveoler kapillerler tıkabasa kanla dolmuş ve genişlemiştir (vasküler ektazi).\n  - Alveoler septalarda belirgin interstisyel ödem meydana gelir; septalar kalınlaşır.\n  - Bazı kapillerlerin patlamasıyla alveol boşluklarına küçük odaksal kanamalar (intraalveoler hemoraji) sızar.\n- **Klinik Yansıma:** Akut nefes darlığı (dispne), taşipne ve hastanın yatar pozisyonda boğulma hissi yaşaması (ortopne).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Akut Pulmoner Konjesyonun Gelişim Zinciri",
                [
                    "1. Sol Ventrikül Disfonksiyonu: Akut iskemi sol ventrikül ejeksiyon debisini düşürür.",
                    "2. Pulmoner Venöz Hipertansiyon: Geriye doğru sol atriyum ve pulmoner venlerde basınç birikir.",
                    "3. Alveoler Kapiller Tıkanıklığı: Kılcal damarlar genişler ve eritrosit kitleleriyle tıkanır.",
                    "4. Septal Ödem ve Mikro-Kanama: Yüksek basınç interstisyel sıvı kaçağına ve kanamaya yol açar."
                ]
            ),
            make_quiz(
                "Akut pulmoner konjesyonun histopatolojik incelemesinde aşağıdaki mikroskopik bulgulardan hangisi öncelikle saptanır?",
                [
                    {"key": "A", "text": "Alveol duvarlarında yoğun kalsiyum kristalleri ve kemikleşme", "isCorrect": False, "explanation": "Kalsifikasyon konjesyonun birincil bulgusu değildir."},
                    {"key": "B", "text": "Kanla dolu alveoler kapillerler, septal ödem ve odaksal intraalveoler kanama alanları", "isCorrect": True, "explanation": "Doğru cevap B'dir: Akut tabloda kapiller dolgunluk, interstisyel ödem ve mikro-kanamalar tipiktir."},
                    {"key": "C", "text": "Alveol boşluklarını dolduran yaygın kazeöz nekroz", "isCorrect": False, "explanation": "Kazeöz nekroz tüberküloza özgüdür."},
                    {"key": "D", "text": "Akciğer dokusunun tamamen yağ dokusuna dönüşmesi", "isCorrect": False, "explanation": "Yağ metaplazisi konjesyonda görülmez."}
                ]
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-16-s23",
        "title": "Kronik Pulmoner Konjesyon ve Kahverengi Endürasyon",
        "content": "Sol kalp yetmezliğinin kronikleştiği (ör. mitral darlığı veya kronik iskemik kardiyomiyopati) hastalarda akciğerde kalıcı yapısal yıkım gelişir:\n\n- **Septal Fibrozis:** Alveol duvarları süreğen ödem ve hipoksiye yanıt olarak fibroblastlarca üretilen kollajenle kalınlaşır ve sertleşir.\n- **Gaz Değişim Engeli:** Kalınlaşan ve fibrotik hale gelen septalar oksijen difüzyon mesafesini uzatır; hasta kronik hipoksemiye girer.\n- **Hemosiderin Çöküşü:** Alveol boşluklarına sürekli sızan eritrositler parçalanır ve yoğun hemosiderin pigmenti depolanır.\n- **Kahverengi Endürasyon (Brown Induration - Sınav Spotu):**\n  - Makroskopik olarak akciğerler normal süngerimsi elastikiyetini kaybeder; sertleşir (endürasyon) ve biriken yoğun demir pigmenti nedeniyle **pas rengi / koyu kahverengi** bir renk alır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Akciğer vs Kahverengi Endürasyonlu Akciğer",
                "Normal Akciğer",
                "Hafif, süngerimsi elastik pembe yapıda, incecik alveoler septalara sahiptir.",
                "Kahverengi Endürasyon",
                "Ağır, sertleşmiş (fibrotik), hemosiderin pigmentiyle pas rengi-kahverengi renk almıştır."
            ),
            make_cloze(
                "Kronik pulmoner konjesyonda septal fibrozis ve hemosiderin birikimi sonucu akciğerin sert ve pas rengi almasına kahverengi endürasyon denir.",
                "kahverengi endürasyon",
                "Kronik konjestif akciğerin patolojik sertleşme ve renk terimi"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-16-s24",
        "title": "Kalp Yetmezliği Hücreleri (Siderofajlar): Tanım ve Klinik Önemi",
        "content": "Kronik akciğer konjesyonunun en karakteristik histopatolojik ve sitolojik bulgusu 'kalp yetmezliği hücreleri'dir (Sınav Spotu):\n\n- **Kimlik:** Kalp yetmezliği hücreleri (heart failure cells), sitoplazmalarında fagositoz sonucu yoğun **hemosiderin granülleri** biriktirmiş olan alveoler makrofajlardır.\n- **Oluşum Mekanizması:**\n  1. Yüksek kapiller basınçla alveol içine eritrositler sızar (mikro-diapedez).\n  2. Alveoler makrofajlar bu dökülen eritrositleri yutar ve sindirir.\n  3. Eritrosit hemoglobini parçalanarak ferritine ve altın-kahverengi hemosiderine dönüştürülür.\n- **Özel Boyama:** Prusya mavisi (Perls) boyası ile bu makrofajların sitoplazmasındaki hemosiderin parlak mavi renge boyanır.\n- **Klinik Tanı:** Kronik kalp yetmezliği hastasının balgamında (sputum) bu hücrelerin saptanması sol ventrikül yetmezliğinin güçlü bir sitolojik kanıtıdır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hücre Özelliği", "Kalp Yetmezliği Hücresi (Siderofaj)"],
                [
                    ["Hücrenin Kökeni", "Alveoler makrofaj (akciğer mononükleer fagositik sistemi)"],
                    ["İçerdiği Pigment", "Hemosiderin (eritrosit hemoglobin yıkım ürünü)"],
                    ["Mikroskopik Renk", "Standart H&E boyasında kaba altın-kahverengi granüller"],
                    ["Özel Histokimyasal Boya", "Prusya mavisi (Perls histokimyası) ile parlak mavi reaksiyon"],
                    ["Klinik Anlamı", "Kronik sol kalp yetmezliği ve kronik pulmoner konjesyon"]
                ]
            ),
            make_quiz(
                "Kronik sol kalp yetmezliği olan bir hastanın balgam yaymasında ve akciğer biyopsisinde görülen 'kalp yetmezliği hücreleri' gerçekte hangi hücre tipidir?",
                [
                    {"key": "A", "text": "Miyokard hücrelerinin akciğere metastaz yapmış öncülleri", "isCorrect": False, "explanation": "Miyokard hücreleri metastaz yapmaz."},
                    {"key": "B", "text": "Sitoplazmasında hemosiderin pigmenti depolamış alveoler makrofajlar (siderofajlar)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kalp yetmezliği hücreleri eritrositleri yutan hemosiderin yüklü alveoler makrofajlardır."},
                    {"key": "C", "text": "Yüzey aktif surfaktan salgılayan Tip II pnömositler", "isCorrect": False, "explanation": "Tip II pnömositler surfaktan salgılar, siderofaj değildir."},
                    {"key": "D", "text": "Bronş epitelindeki siliyalı silindirik hücreler", "isCorrect": False, "explanation": "Silindirik epitel hücreleri siderofaj değildir."}
                ]
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-16-s25",
        "title": "Akut Hepatik Konjesyon: Santral Ven ve Sinüzoid Patolojisi",
        "content": "Akut hepatik konjesyon, sağ ventrikül yetmezliği, triküspit yetersizliği veya hepatik venlerin ani tıkanması (Budd-Chiari sendromu) sonucu ortaya çıkar:\n\n- **Makroskopi:** Karaciğer hızla büyür (akut hepatomegali), kapsülü gerilir ve palpasyonda ağrılıdır; kesit yüzünden bol koyu venöz kan akar.\n- **Mikroskopik Morfoloji:**\n  - Her karaciğer lobülünün ortasında yer alan **santral ven (vena centralis)** ve buraya drene olan **sinüzoidler** aşırı genişlemiş ve eritrositle dolmuştur.\n  - **Sentrilobüler Hepatosit Nekrozu:** Lobül merkezindeki hepatositler arteriyel kandan en uzak bölgede (Zon 3) yer aldığından akut konjesyonun yarattığı hipoksiye ilk kurban gider ve iskemik nekroza uğrar.\n  - **Periportal Alanlar (Zon 1):** Hepatik artere yakın oldukları için oksijenlenmeleri kısmen korunur ve yalnızca hafif yağlanma (steatoz) gösterebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Akut Karaciğer Konjesyonunda Zonal Hasar Aşamaları",
                [
                    "1. Sağ Kalp Yetmezliği: Sistemik venöz basınç vena kava inferior yoluyla karaciğere iletilir.",
                    "2. Santral Ven Tıkanıklığı: Vena sentralis ve komşu sinüzoidler pasif olarak genişler.",
                    "3. Sentrilobüler Hipoksi (Zon 3): Arteriyole en uzak olan lobül merkezi oksijensiz kalır.",
                    "4. Sentrilobüler Nekroz: Zon 3 hepatositleri ölürken periferdeki Zon 1 hepatositleri canlı kalır."
                ]
            ),
            make_cloze(
                "Akut karaciğer konjesyonunda kanın ilk göllendiği ve hipoksiye bağlı ilk hepatosit nekrozunun görüldüğü lobül bölgesi santral ven çevresidir.",
                "santral ven",
                "Karaciğer lobülünün merkezindeki toplayıcı damar"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-16-s26",
        "title": "Kronik Pasif Karaciğer Konjesyonu ve 'Muskat Karaciğer'",
        "content": "Kronik sağ kalp yetmezliğinde karaciğerin kesit yüzü patolojinin en klasik görüntülerinden birini sergiler:\n\n- **Muskat Karaciğer (Nutmeg Liver - Sınav Spotu):**\n  - Hint cevizi (muskat) tohumunun alacalı kesitine benzediği için bu adı almıştır.\n- **Makroskobik Görünümün Patofizyolojik Temeli:**\n  1. **Kırmızı-Kahverengi ve Çökük Alanlar:** Lobüllerin merkezi (Zon 3); konjesyone venler, ölü nekrotik hepatositler ve hücre kaybına bağlı doku çöküntüsünü temsil eder.\n  2. **Açık Sarı-Kahverengi Alanlar:** Lobülün periferik kısımları (Zon 1 - periportal alan); göreceli olarak daha iyi oksijenlendiği için canlı kalmış ancak subletal hipoksi nedeniyle **yağlanmış (steatoz)** hepatositleri temsil eder.\n- **Klinik Yansıma:** Kronik konjesyonda karaciğer fonksiyon testleri (AST, ALT, Bilirubin) hafif-orta derecede yükselir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Bölge", "Makroskobik Renk ve Doku", "Mikroskopik Karşılığı", "Patofizyolojik Neden"],
                [
                    ["Lobül Merkezi (Zon 3)", "Kırmızı-kahverengi ve hafif çökük", "Genişlemiş sinüzoidler, nekroze hepatositler", "Şiddetli hipoksi ve mekanik venöz bası"],
                    ["Lobül Periferi (Zon 1)", "Açık sarı-kahverengi, kabarık", "Canlı hepatositler, belirgin steatoz (yağlanma)", "Hepatik artere yakınlık, kısmi oksijenlenme"]
                ]
            ),
            make_quiz(
                "Kronik sağ kalp yetmezliği olan bir hastanın otopsisinde karaciğer kesitinde saptanan 'muskat karaciğer' görünümünün kırmızı-kahverengi çökük alanları neyi ifade eder?",
                [
                    {"key": "A", "text": "Hepatik arter dallarında primer aterosklerotik kalsifikasyonları", "isCorrect": False, "explanation": "Ateroskleroz karaciğer lobül merkezinde kırmızı çöküntü yapmaz."},
                    {"key": "B", "text": "Konjesyone santral ven çevresindeki sinüzoid dolgunluğunu ve sentrilobüler hepatosit nekrozunu", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kırmızı alanlar kan dolu santral sinüzoidler ve iskemik nekroza uğramış sentrilobüler hepatositlerdir."},
                    {"key": "C", "text": "Safra kanallarının parazitler tarafından tıkanmasını", "isCorrect": False, "explanation": "Kolanjit veya paraziter tıkanma muskat tablosu oluşturmaz."},
                    {"key": "D", "text": "Sadece tamamen normal canlı karaciğer hücre adacıklarını", "isCorrect": False, "explanation": "Normal hücreler açık renkli periportal alanlardadır."}
                ]
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-16-s27",
        "title": "Sentrilobüler Hipoksinin Zonal Dağılımı: Rappaport Asinüsü",
        "content": "Karaciğer parankiminin konjesyona karşı geliştirdiği hasar Rappaport asinüs mimarisi üzerinden anlaşılır:\n\n- **Asinüs Zon 1 (Periportal Bölge):**\n  - Portal alanın hemen komşusudur; hepatik arter ve portal venden zengin oksijenli kanı ilk alan bölgedir.\n  - İskemiye ve konjesyona en dayanıklı zondur; toksinlere ise ilk maruz kalan bölgedir.\n- **Asinüs Zon 2 (Orta Zon):** Geçiş bölgesidir; orta derecede etkilenir.\n- **Asinüs Zon 3 (Sentrilobüler Bölge - Sınav Spotu):**\n  - Kan santral vene ulaşana kadar oksijenini kaybettiği için bazal koşullarda bile en düşük pO2 düzeyine sahiptir.\n  - Venöz konjesyon veya sistemik hipotansiyon geliştiğinde **iskemiye ilk ve en ağır yenilen bölge Zon 3'tür**.\n  - Sonuç: Ağır şok veya kalp yetmezliğinde izole **sentrilobüler hemorajik nekroz** tablosu ortaya çıkar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Asinüs Zon 1 (Periportal) vs Zon 3 (Sentrilobüler) İskemiye Duyarlılık",
                "Zon 1 (Periportal)",
                "Oksijenden en zengin bölgedir; venöz konjesyon ve hipotansif iskemiye karşı en dirençli zondur.",
                "Zon 3 (Sentrilobüler)",
                "Oksijen saturasyonu en düşüktür; konjesyon ve hipotansiyonda ilk nekroza giden en duyarlı zondur."
            ),
            make_cloze(
                "Karaciğer asinüsünde venöz konjesyon ve hipoksiye karşı en duyarlı olan ve ilk nekroze olan alan Zon 3 sentrilobüler bölgesidir.",
                "Zon 3",
                "Lobül merkezindeki en duyarlı metabolik asinüs zonu"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-16-s28",
        "title": "Kardiyak Siroz (Kardiyak Skleroz): Kronikleşmenin Sonu",
        "content": "Yıllar süren tedavi edilmemiş ağır sağ kalp yetmezliği veya konstriktif perikardit karaciğerde son evre bağ dokusu artışına yol açar:\n\n- **Kardiyak Fibrozis:** Sentrilobüler nekroz alanları sürekli olarak kollajen sentezleyen hepatik stellat hücreler (İto hücreleri) tarafından fibrotik bağ dokusuyla doldurulur.\n- **Santralden Santrale Köprüleşme:** Fibrozis santral venden komşu santral vene doğru bantlar uzatır (sentrosantral köprüleşme fibrozisi).\n- **Kardiyak Siroz (Kardiyak Skleroz):**\n  - Klasik viral hepatit veya alkolik sirozdan farklı olarak portal alanlar başlangıçta korunur; hasar merkezden yayılır.\n  - Karaciğer sert, nodüler ve küçülmüş bir hal alır; karaciğer sentez kapasitesi düşer ve portal hipertansiyon daha da derinleşir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kardiyak Siroz Gelişim Aşamaları",
                [
                    "1. Kronik Sağ Kalp Yetmezliği: Karaciğerde uzun süreli venöz basınç yüksekliği sürer.",
                    "2. Tekrarlayan Sentrilobüler Nekroz: Zon 3 hepatositleri sürekli ölür ve dökülür.",
                    "3. Stellat Hücre Aktivasyonu: İto hücreleri miyofibroblasta dönüşerek Tip I kollajen üretir.",
                    "4. Kardiyak Siroz Tablosu: Sentrosantral fibröz köprüler oluşarak mikronodüler skar gelişir."
                ]
            ),
            make_quiz(
                "Kronik sağ kalp yetmezliğine ikincil olarak karaciğerde gelişen ve santral ven çevresinden köken alan yaygın fibrozis tablosuna ne ad verilir?",
                [
                    {"key": "A", "text": "Primer biliyer kolanjit", "isCorrect": False, "explanation": "Otoimmün safra kanalı yıkımıdır."},
                    {"key": "B", "text": "Kardiyak siroz (kardiyak skleroz)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Uzun süreli konjestif kalp yetmezliğine bağlı karaciğer fibrozisine kardiyak siroz denir."},
                    {"key": "C", "text": "Wilson hastalığı", "isCorrect": False, "explanation": "Bakır birikim hastalığıdır."},
                    {"key": "D", "text": "Akut flegmonöz hepatit", "isCorrect": False, "explanation": "Bakteriyel akut piyojenik enfeksiyondur."}
                ]
            )
        ]
    })

    # Slide 29 - CHECKPOINT 3
    slides.append({
        "id": "k1-16-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Organ Konjesyonu ve Morfolojik Bulgular",
        "content": "Bu checkpointte akut ve kronik organ konjesyonunun histopatolojik damga bulgularını özetliyoruz:\n\n- **Akut Pulmoner Konjesyon:** Kanla dolu alveoler kapillerler, septal ödem ve mikro-kanama odakları.\n- **Kronik Pulmoner Konjesyon:** Kalınlaşmış fibrotik septalar ve alveol lümeninde hemosiderin yüklü makrofajlar (kalp yetmezliği hücreleri / siderofajlar); akciğer sert ve kahverengidir (kahverengi endürasyon).\n- **Akut Karaciğer Konjesyonu:** Santral ven ve sinüzoid dilatasyonu, Zon 3 sentrilobüler hepatosit nekrozu.\n- **Kronik Karaciğer Konjesyonu (Muskat Karaciğer):** Lobül merkezinde kırmızı-kahverengi nekroz ve konjesyon; lobül periferinde açık sarı-kahverengi yağlanmış (steatoz) hepatositler.\n- **Kardiyak Siroz:** Kronik venöz hipertansiyon zemininde sentrosantral fibröz köprüleşme ve nodül oluşumu.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Organ", "Akut Konjesyon Bulgusu", "Kronik Konjesyon Patognomonik Bulgusu"],
                [
                    ["Akciğer", "Genişlemiş kapillerler, septal ödem, eritrosit sızıntısı", "Hemosiderin yüklü makrofajlar ('Kalp yetmezliği hücreleri') ve 'Kahverengi endürasyon'"],
                    ["Karaciğer", "Santral ven dilatasyonu ve sentrilobüler (Zon 3) nekroz", "'Muskat karaciğer' görünümü ve uzun dönemde 'Kardiyak siroz'"]
                ]
            ),
            make_chain(
                "Siderofaj ve Muskat Karaciğer Eşleşme Özeti",
                [
                    "1. Sol Kalp Bozukluğu: Pulmoner venöz hipertansiyon $\\to$ Alveolde siderofajlar.",
                    "2. Sağ Kalp Bozukluğu: Sistemik vena kava hipertansiyonu $\\to$ Sinüzoidal staz.",
                    "3. Zonal Karaciğer Hasarı: Zon 3 nekrozu ve Zon 1 steatozu $\\to$ Muskat manzarası.",
                    "4. Kalıcı Hasar: Akciğerde kahverengi endürasyon, karaciğerde kardiyak siroz."
                ]
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-16-s30",
        "title": "Bölüm Özeti: Organ Hasarından Genel Ödem Patolojisine Geçiş",
        "content": "Bölüm 3'te kalp yetmezliğinin hedef organlarda (akciğer ve karaciğer) yol açtığı akut ve kronik morfolojik değişiklikleri inceledik:\n\n- **Anahtar Kavramlar:** Kalp yetmezliği hücreleri (siderofajlar), kahverengi endürasyon, Zon 3 duyarlılığı ve muskat karaciğer patolojinin vazgeçilmez sınav spotlarıdır.\n- **Sonraki Bölüm:** Bir sonraki bölümde ödemin 5 temel mekanizmasından birincisi olan **artmış hidrostatik basınç** ve bu kapsamda **konjestif kalp yetmezliğinde sıvı birikimi döngüsünü** ayrıntılandıracağız.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Kronik sol ventrikül yetmezliğinde alveol lümeninde biriken hemosiderin yüklü alveoler makrofajlara verilen özel isim nedir?",
                "Kalp yetmezliği hücreleri (veya siderofajlar)",
                "Akciğerde kronik konjesyonun hücresel göstergesi"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi kronik akciğer konjesyonunda akciğerin kahverengi endürasyon almasına katkıda bulunan iki temel histolojik bulgudur?",
                [
                    {"key": "A", "text": "Alveollerde amiloid proteini ve kazeöz nekroz", "isCorrect": False, "explanation": "Amiloidoz ve kazeöz nekroz konjesyon bulgusu değildir."},
                    {"key": "B", "text": "Alveoler septalarda belirgin fibrozis ve makrofajlarda hemosiderin pigment birikimi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Septal fibrozis sertleşmeyi (endürasyon), hemosiderin ise pas-kahverengi rengi oluşturur."},
                    {"key": "C", "text": "Tüm alveollerin kist hidatik parazitiyle dolması", "isCorrect": False, "explanation": "Paraziter kist hastalığıdır."},
                    {"key": "D", "text": "Plevra yapraklarında kemik dokusu gelişimi", "isCorrect": False, "explanation": "Kemik metaplazisi konjesyona özgü değildir."}
                ]
            )
        ]
    })

    return slides
