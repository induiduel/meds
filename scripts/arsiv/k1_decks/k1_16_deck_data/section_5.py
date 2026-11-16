# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-16-s41",
        "title": "Plazma Onkotik Basıncı ve Albüminin Biyolojik Önemi",
        "content": "Plazma kolloid ozmotik (onkotik) basıncı, damar lümeni içinde suyu tutan ve interstisyumdan geri çeken temel kuvvettir:\n\n- **Proteinlerin Katkısı:** Plazmada dolaşan proteinler mikrosirkülasyonda yaklaşık 25-28 mmHg'lik bir çekici onkotik güç üretir.\n- **Albüminin Hayati Rolü (Sınav Spotu):**\n  - Plazma proteinlerinin yaklaşık %50-60'ını tek başına **albümin** oluşturur.\n  - Albümin molekül ağırlığının küçüklüğü ve kanda yüksek molar konsantrasyonda bulunması sayesinde, **toplam plazma onkotik basıncının yaklaşık %70-80'ini tek başına sağlar**.\n  - Globulinler ve fibrinojen moleküler olarak daha büyüktür ve onkotik basınca katkıları albümine kıyasla çok daha düşüktür.\n- **Hipoalbüminemi Eşiği:** Serum albümin düzeyi normalde 3.5-5.0 g/dL'dir. Albümin düzeyi 2.5 g/dL'nin altına indiğinde plazma onkotik basıncı kritik eşiğin altına düşer ve yaygın ödem başlar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Serum Albümin Düzeyi vs Hipoalbüminemi",
                "Normal Albümin (>3.5 g/dL)",
                "Onkotik basınç 25 mmHg düzeyindedir; sıvı damar içinde tutulur ve venül ucunda etkin geri emilim sağlanır.",
                "Hipoalbüminemi (<2.5 g/dL)",
                "Onkotik çekim kuvveti çöker; hidrostatik basınç dengelenemez ve sıvı kontrolsüzce dokulara akar."
            ),
            make_cloze(
                "Plazma kolloid ozmotik basıncının yaklaşık yüzde 80'ini tek başına sağlayan majör plazma proteini albümin molekülüdür.",
                "albümin",
                "Karaciğerde üretilen ve onkotik basıncı belirleyen ana plazma proteini"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-16-s42",
        "title": "Hipoalbümineminin Temel Nedenleri ve Sınıflandırma",
        "content": "Kanda albümin düşüklüğü ve buna bağlı onkotik basınç azalması üç ana mekanizmayla gelişir (Sınav Spotu):\n\n- **1. Aşırı Protein Kaybı (Ekskresyon / Sızıntı):**\n  - **Nefrotik Sendrom:** Glomerüler geçirgenliğin bozulması sonucu idrarla masif albümin kaybı (>3.5 g/gün).\n  - **Protein Kaybettiren Gastroenteropati:** Ağır bağırsak hastalıklarında (çölyak, Crohn, intestinal lenfanjiektazi) bağırsak lümenine protein sızması.\n  - **Geniş Yanıklar:** Deri bariyerinin yok olmasıyla plazmanın yanık yüzeyinden dışarı akması.\n- **2. Azalmış Protein Sentezi (Üretim Kusuru):**\n  - **İleri Evre Karaciğer Hastalığı / Siroz:** Albümini üreten tek fabrika olan karaciğer parankiminin tükenmesi.\n- **3. Yetersiz Alım (Diyet Kusuru):**\n  - **Ağır Malnütrisyon (Kwashiorkor):** Diyette protein eksikliği nedeniyle karaciğerin aminoasit bulamaması.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Mekanizma Tipi", "Başlıca Patoloji", "Biyokimyasal Süreç", "Klinik Ödem Özelliği"],
                [
                    ["Renal Kayıp", "Nefrotik Sendrom", "Glomerüler podosit hasarı, masif proteinüri", "Erken periorbital ödem, anasarka"],
                    ["Hepatik Sentez Azlığı", "Karaciğer Sirozu", "Hepatosit yetersizliği, albümin sentezi ↓", "Ön planda asit (hidroperiton) ve bacak ödemi"],
                    ["Yetersiz Alım", "Kwashiorkor (Malnütrisyon)", "Diyette aminoasit yokluğu", "Karında şişlik (asit) ve genel doku ödemi"],
                    ["Gastrointestinal Kayıp", "Protein Kaybettiren Enteropati", "Mukoza erozyonundan lümene protein kaçağı", "Kronik ishal ve simetrik gode bırakan ödem"]
                ]
            ),
            make_quiz(
                "Aşağıdaki klinik tablolardan hangisi plazma kolloid ozmotik basıncını azaltarak ödem oluşturan primer nedenlerden biri DEĞİLDİR?",
                [
                    {"key": "A", "text": "Nefrotik sendrom", "isCorrect": False, "explanation": "Nefrotik sendrom ağır proteinüri ile onkotik basıncı düşürür."},
                    {"key": "B", "text": "İleri evre karaciğer sirozu", "isCorrect": False, "explanation": "Siroz albümin sentezini bozarak onkotik basıncı düşürür."},
                    {"key": "C", "text": "Ağır protein malnütrisyonu (kwashiorkor)", "isCorrect": False, "explanation": "Malnütrisyon hipoalbüminemi yapar."},
                    {"key": "D", "text": "Derin ven trombozu", "isCorrect": True, "explanation": "Doğru cevap D'dir: Derin ven trombozu onkotik basıncı düşürmez; lokal kapiller hidrostatik basıncı artırarak ödem yapar."}
                ]
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-16-s43",
        "title": "Nefrotik Sendrom Patofizyolojisi: Glomerüler Kaçak ve Masif Proteinüri",
        "content": "Nefrotik sendrom, böbreğin glomerüler filtrasyon bariyerinin geçirgenlik kontrolünü kaybetmesiyle karakterizedir:\n\n- **Filtrasyon Bariyeri:** Normalde podositlerin ayaksı çıkıntıları (slit diafram) ve negatif yüklü heparan sülfat proteoglikanları albüminin idrara kaçmasını engeller.\n- **Bariyer Yıkımı:** Membranöz nefropati, fokal segmental glomerüloskleroz (FSGS) veya minimal lezyon hastalığında bariyer bozulur.\n- **Masif Proteinüri:** Günde 3.5 gramdan fazla protein (çoğu albümin) idrarla atılır.\n- **Onkotik Çöküş:** Karaciğer kompansatris olarak albümin üretimini artırmaya çalışsa da renal kaybı karşılayamaz; serum albümini hızla <2.0 g/dL seviyelerine iner.\n- **Sonuç:** Vücuttaki tüm kapiller yataklarda venüler emilim gücü yok olur ve yaygın seröz sıvı dokulara boşalır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Nefrotik Sendromda Ödem Gelişim Zinciri",
                [
                    "1. Glomerüler Hasar: Podosit slit diyaframı ve negatif yük bariyeri parçalanır.",
                    "2. Masif Proteinüri: Günde 3.5 gramın üzerinde albümin idrarla kaybedilir.",
                    "3. Ağır Hipoalbüminemi: Serum albümin düzeyi kritik eşiğin altına geriler.",
                    "4. Onkotik Çöküş ve Ödem: Kılcal damarlardan doku aralığına kontrolsüz transuda kaçar."
                ]
            ),
            make_cloze(
                "Günde 3.5 gramın üzerinde albümin kaybı, hipoalbüminemi ve yaygın ödemle karakterize böbrek tablosuna nefrotik sendrom denir.",
                "nefrotik sendrom",
                "Masif proteinüri ile seyreden majör glomerüler klinik sendrom"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-16-s44",
        "title": "Nefrotik Sendromda Periorbital Ödem ve Anasarkaya İlerleme",
        "content": "Nefrotik ödemin vücutta ilk ortaya çıktığı yer anatomik bağ dokusu özellikleriyle doğrudan ilişkilidir (Sınav Spotu):\n\n- **Periorbital Ödem (Göz Çevresi Şişliği):**\n  - Göz kapakları ve periorbital alan vücudun en gevşek areolar bağ dokusuna sahiptir; interstisyel hidrostatik karşı basınç burada neredeyse sıfırdır.\n  - Onkotik basınç düştüğünde sıvı en kolay dirençsiz olan bu gevşek dokuya kaçar.\n  - **Sabah Belirginliği:** Gece boyunca yatay pozisyonda yatan hastada sabah uyandığında göz kapakları balon gibi şişmiştir (karakteristik sabah periorbital ödemi).\n- **Genelleşme (Anasarka):** Gün içinde yerçekimiyle sıvı bacaklara ve skrotum/labiumlara iner; hastalık ilerledikçe plevral, peritonel efüzyonlar eklenir ve tam bir anasarka tablosu gelişir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kardiyak Ödem Yerleşimi vs Nefrotik Ödem Başlangıcı",
                "Kardiyak Ödem Başlangıcı",
                "Yerçekimi bağımlıdır; öncelikle gün boyu ayakta duran hastanın bacak ve ayak bileklerinde belirir.",
                "Nefrotik Ödem Başlangıcı",
                "Gevşek bağ dokusu tercihlidir; sabahları göz kapaklarında ve yüzde (periorbital) belirginleşir."
            ),
            make_quiz(
                "Nefrotik sendromlu bir hastada ödemin erken evrede özellikle göz çevresinde (periorbital) belirgin olmasının nedeni nedir?",
                [
                    {"key": "A", "text": "Gözyaşı bezlerinin aşırı sodyum salgılaması", "isCorrect": False, "explanation": "Gözyaşı bezleriyle ilişkili değildir."},
                    {"key": "B", "text": "Periorbital bölgenin çok gevşek bağ dokusuna sahip olması ve sıvının dirençsiz kolay birikmesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Göz kapaklarındaki gevşek doku karşı direnç oluşturamaz ve onkotik basınç düşüşünde sıvı ilk buraya sızar."},
                    {"key": "C", "text": "Hastanın geceleri gözlerini sürekli açık tutması", "isCorrect": False, "explanation": "Göz kapağının açık kalmasıyla ilgisizdir."},
                    {"key": "D", "text": "Retina damarlarında primer arteriyel tromboz olması", "isCorrect": False, "explanation": "Retina trombozu periorbital ödem yapmaz."}
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-16-s45",
        "title": "İleri Karaciğer Hastalığı ve Sirozda Albümin Sentez Kusuru",
        "content": "Karaciğer vücuttaki tüm albümini sentezleyen yegane organdır:\n\n- **Hepatosit Fonksiyonel Kütle Kaybı:** Kronik hepatit B/C, alkolik karaciğer hastalığı veya yağlı karaciğer zemininde gelişen sirozda normal parankimin yerini fibröz nodüller alır.\n- **Sentez Kapasitesinin Çöküşü:** Canlı hepatosit sayısı azaldıkça günlük albümin üretimi durma noktasına gelir.\n- **Sirozda Hipoalbüminemi:** Serum albümin düzeyi düşer; bu durum tüm sistemik kılcal damarlarda plazma onkotik basıncını zayıflatır.\n- **İkili Patoloji:** Karaciğer sirozunda ödem yalnızca hipoalbüminemiye bağlı değildir; portal hipertansiyon ve splanknik arteriyoler vazodilatasyon tablosu ile birleşerek devasa sıvı birikimlerine yol açar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Sirozda Albümin Sentez Çöküşü ve Sıvı Kaçağı",
                [
                    "1. Parankimal Hasar: Kronik enflamasyon hepatosit kütlesini tahrip eder.",
                    "2. Fibröz Skarlaşma: Sağlam hepatosit sayısı kritik eşiğin altına iner.",
                    "3. Sentez Yetmezliği: Karaciğer dolaşıma yeterli albümin veremez.",
                    "4. Onkotik Yetersizlik: Kanda albümin düşer ve sistemik onkotik basınç azalır."
                ]
            ),
            make_cloze(
                "Vücuttaki plazma albüminini sentezleyen yegane organ olan karaciğerin sirozunda parankim kaybı ağır hipoalbüminemiye neden olur.",
                "karaciğerin",
                "Albümin sentezinin yapıldığı tek hayati organ"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-16-s46",
        "title": "Sirozda Portal Hipertansiyon ve Asit (Hidroperiton) Mekanizması",
        "content": "Karaciğer sirozunda karın boşluğunda litrelerce sıvı birikmesi (asit) iki majör mekanizmanın sinerjisiyle oluşur:\n\n- **1. Portal Hipertansiyon (Artmış Lokal Hidrostatik Basınç):**\n  - Fibröz skar dokusu ve rejenerasyon nodülleri intrahepatik portal ven dallarını sıkıştırır.\n  - Portal vende basınç yükselir; tüm mezenterik ve intestinal kapillerlerde hidrostatik basınç patlar.\n- **2. Azalmış Onkotik Basınç (Hipoalbüminemi):**\n  - Karaciğer yetmezliğine bağlı düşük albümin düzeyi damar içindeki çekim gücünü sıfırlar.\n- **Splanknik Vazodilatasyon:** Portal hipertansiyon endotelden aşırı Nitrik Oksit (NO) salınımına ve splanknik arteriyollerin genişlemesine yol açar.\n- **Asit Sıvısının Karına Sızması:** Karaciğer yüzeyinden ve bağırsak serozasından karın boşluğuna (peritona) adeta 'terleme' şeklinde transuda boşalır (asit / hidroperiton).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Patolojik Faktör", "Fizyopatolojik Rolü", "Asit Oluşumuna Katkısı"],
                [
                    ["Portal Hipertansiyon", "Mezenterik venlerde hidrostatik basınç artışı", "Bağırsak kapillerlerinden sıvı filtrasyonunu hızlandırır"],
                    ["Hipoalbüminemi", "Plazma kolloid ozmotik basıncının çökmesi", "Sıvının damar içine geri emilimini tamamen engeller"],
                    ["Splanknik Vazodilatasyon", "Lokal NO salınımı ile arteriyoler genişleme", "Portal yatağa giren kan akımını artırarak göllenmeyi derinleştirir"],
                    ["Hepatik Lenf Kaçağı", "Karaciğer lenf kanallarının aşırı dolması", "Karaciğer kapsülünden doğrudan periton boşluğuna sıvı sızması"]
                ]
            ),
            make_quiz(
                "Karaciğer sirozlu bir hastada masif asit (karında sıvı birikimi) gelişmesinde rol oynayan iki temel hemodinamik mekanizma hangisidir?",
                [
                    {"key": "A", "text": "Arteriyel hipertansiyon ve hiperalbüminemi", "isCorrect": False, "explanation": "Tam tersine hipotansiyon ve hipoalbüminemi vardır."},
                    {"key": "B", "text": "Portal venöz hidrostatik basınç artışı ile birlikte plazma onkotik basıncının (hipoalbüminemi) azalması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Portal hipertansiyon hidrostatik basıncı artırırken, siroza bağlı hipoalbüminemi onkotik basıncı düşürür."},
                    {"key": "C", "text": "Safra kesesinin aşırı kasılarak peritona safra boşaltması", "isCorrect": False, "explanation": "Safra peritoniti kolyasittir, transuda asiti değildir."},
                    {"key": "D", "text": "Böbreklerin aşırı miktarda albümin sentezlemesi", "isCorrect": False, "explanation": "Böbrekler albümin sentezlemez."}
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-16-s47",
        "title": "Protein Kaybettiren Enteropatiler ve Malnütrisyon (Kwashiorkor)",
        "content": "Beslenme bozukluğu veya bağırsak emilim yetersizliği de şiddetli onkotik basınç düşüşüne yol açar:\n\n- **Protein Kaybettiren Enteropati:**\n  - Crohn hastalığı, çölyak hastalığı veya intestinal lenfanjiektazide bağırsak mukozası hasarlanır veya lenfatikler lümene boşalır.\n  - Dolaşımdaki plazma proteinleri bağırsak boşluğuna sızarak dışkıyla kaybedilir.\n- **Kwashiorkor (Protein Malnütrisyonu - Sınav Spotu):**\n  - Kalorisi yeterli ancak proteini aşırı yetersiz (saf karbonhidrat ağırlıklı) beslenen çocuklarda görülür.\n  - Diyetle aminoasit alınamadığı için karaciğer albümin üretemez.\n  - **Klinik Fenotip:** Çocuğun kolları ve bacakları zayıf ve kaşektiktir; ancak hipoalbüminemiye bağlı olarak karnı masif asitli ve şiştir; deride yaygın ödem ve döküntüler mevcuttur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Marasmus (Genel Kalori Yetersizliği) vs Kwashiorkor (Protein Yetersizliği)",
                "Marasmus",
                "Hem kalori hem protein eksiktir; kas ve yağ dokusu tamamen erir, ancak ödem görülmez.",
                "Kwashiorkor",
                "Kalori var fakat protein sıfırdır; ağır hipoalbüminemi nedeniyle belirgin ödem ve asit gelişir."
            ),
            make_cloze(
                "Proteinden yoksun beslenme sonucu karaciğerde albümin sentezlenememesiyle gelişen ödemli malnütrisyon tablosuna kwashiorkor denir.",
                "kwashiorkor",
                "Çocuklarda protein eksikliğine bağlı ödemli beslenme hastalığı"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-16-s48",
        "title": "Hipoalbüminemide İntravasküler Hacim Azalması ve RAAS Yanıtı",
        "content": "Hipoalbüminemik ödemin en kritik ve tehlikeli fizyolojik paradoksu damar içinin susuz kalmasıdır:\n\n- **Efektif Dolaşan Hacmin Düşmesi:** Plazma onkotik basıncı yetersiz olduğu için damar içindeki su sürekli doku aralığına kaçar. Sonuçta damar içi hacim (intravasküler plazma) azalır (hipovolemi eğilimi).\n- **Böbreğin Yanlış Alarmı:** Böbrek glomerüllerine gelen kan akımı ve basıncı düşer. Böbrek vücudun toplam suyunun arttığını fark edemez; arteriyel hipoperfüzyon nedeniyle alarm verir.\n- **Sekonder Hiperaldosteronizm:** Jukstaglomerüler hücreler yoğun renin salgılar $\\to$ Aldosteron artar $\\to$ Böbrekler tuzu ve suyu tutar.\n- **Facianın Büyümesi:** Tutulan bu yeni su da damar içinde albümin olmadığı için damarda kalamaz; doğrudan interstisyuma kaçarak ödemi ve asiti daha da şişirir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hipoalbüminemide İntravasküler Hacim Paradoksu",
                [
                    "1. Onkotik Basınç Düşüşü: Plazma suyu damar dışına kontrolsüzce sızar.",
                    "2. İntravasküler Hipovolemi: Dolaşımdaki efektif plazma hacmi azalır.",
                    "3. Renal RAAS Uyarılması: Böbrek hipovolemiyi düzeltmek için tuz ve su tutar.",
                    "4. Ödemin Derinleşmesi: Yeni tutulan su da albüminsiz damardan dokuya kaçar."
                ]
            ),
            make_quiz(
                "Nefrotik sendrom veya sirozda toplam vücut sıvısı aşırı artmış olmasına rağmen böbreklerin sürekli sodyum ve su tutmasının temel nedeni nedir?",
                [
                    {"key": "A", "text": "Albüminin böbrek tübüllerini fiziksel olarak tıkaması", "isCorrect": False, "explanation": "Albümin tübülleri tıkamaz."},
                    {"key": "B", "text": "Damar içi sıvının interstisyuma kaçması nedeniyle efektik dolaşan plazma hacminin düşmesi ve RAAS'ın uyarılması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Onkotik basınç düşüklüğü sıvıyı dokuya kaçırır, damar içi hacim düşer ve böbrek hipoperfüzyon algısıyla RAAS'ı ateşler."},
                    {"key": "C", "text": "Böbreklerin aşırı miktarda insülin salgılaması", "isCorrect": False, "explanation": "İnsülin pankreastan salgılanır."},
                    {"key": "D", "text": "Kemik iliğinde eritrosit üretiminin durması", "isCorrect": False, "explanation": "Eritrosit üretimi sodyum tutulumunu doğrudan tetiklemez."}
                ]
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-16-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Onkotik Basınç Azalması ve Hipoalbüminemi",
        "content": "Bu checkpointte onkotik basınç çöküşü, hipoalbüminemi mekanizmaları ve klinik yansımalarını pekiştiriyoruz:\n\n- **Albümin Hakimiyeti:** Plazma proteinlerinin %50'si, onkotik basıncın ~%80'i albümine aittir. Albümin <2.5 g/dL altına inince ödem kaçınılmazdır.\n- **Üç Majör Neden:**\n  1. Protein Kaybı: Nefrotik sendrom (>3.5 g/gün proteinüri), yanıklar, protein kaybettiren enteropati.\n  2. Sentez Azlığı: İleri evre karaciğer hastalığı ve siroz.\n  3. Yetersiz Alım: Ağır malnütrisyon (Kwashiorkor).\n- **Nefrotik Karakter:** Sabahları göz çevresinde (periorbital) gevşek bağ dokusunda başlayan ödem, gün içinde ve ilerledikçe anasarkaya döner.\n- **Siroz ve Asit:** Portal hipertansiyon (hidrostatik ↑) + hipoalbüminemi (onkotik ↓) kombinasyonu masif asit (hidroperiton) oluşturur.\n- **Hipovolemi Paradoksu:** Sıvı dokuya kaçtığı için intravasküler hacim düşer; böbrek sekonder hiperaldosteronizm ile su tutarak ödemi daha da büyütür.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hastalık", "Temel Patoloji", "İlk / Belirgin Ödem Alanı", "Onkotik Düzey"],
                [
                    ["Nefrotik Sendrom", "Glomerüler masif protein kaçağı", "Periorbital (göz çevresi) ve anasarka", "Ağır düşük (<2.0 g/dL)"],
                    ["Karaciğer Sirozu", "Hepatosit sentez kusuru + portal HT", "Asit (periton) ve bilateral bacak ödemi", "Düşük"],
                    ["Kwashiorkor", "Saf protein diyet yetersizliği", "Asit ve yaygın doku ödemi", "Ağır düşük"],
                    ["Konjestif Kalp Yetmezliği", "Kardiyak pompa yetersizliği", "Bağımlı bölgeler (ayak bileği / sakrum)", "Normal veya hafif dilüsyone"]
                ]
            ),
            make_chain(
                "Hipoalbüminemik Ödemin 4 Adımlı Patofizyolojik Özeti",
                [
                    "1. Albümin Eksikliği: Renal kayıp veya hepatik sentez yetersizliği.",
                    "2. Starling Bozulması: Kolloid ozmotik çekim gücü 15 mmHg altına iner.",
                    "3. Gevşek Doku Şişmesi: Periorbital ve seröz boşluklarda sıvı toplanır.",
                    "4. Kompansatuvar Tuz Tutulumu: Renal hipoperfüzyonla ödem anasarkaya ilerler."
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-16-s50",
        "title": "Bölüm Özeti: Onkotik Çöküşten Lenfatik ve Renal Mekanizmalara Geçiş",
        "content": "Bölüm 5 boyunca plazma kolloid ozmotik basıncının çöküşüne yol açan hepatik, renal ve nutrisyonel nedenleri inceledik:\n\n- **Klinik Hatırlatma:** Hipoalbüminemi tüm vücudu ilgilendiren sistemik bir sorundur; dokularda yaygın sıvı birikimi yaratır.\n- **Sonraki Adım:** Bir sonraki bölümde ödemin diğer iki kritik mekanizmasını — doku drenajını felç eden **lenfatik obstrüksiyonu (lenfödem)** ve primer böbrek yetmezliğine bağlı **sodyum/su retansiyonunu** — inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Nefrotik sendromun tanısında erişkinde 24 saatlik idrarda saptanan protein miktarının alt sınırı nedir?",
                "3.5 gram/gün (günde 3.5 gram üzeri proteinüri)",
                "Nefrotik düzeyde proteinüri eşik değeri"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi kwashiorkorlu çocuklarda marasmuslu çocukların aksine belirgin ödem ve karında şişlik görülmesini açıklar?",
                [
                    {"key": "A", "text": "Diyette sadece aşırı protein bulunması", "isCorrect": False, "explanation": "Tam tersine protein tamamen eksiktir."},
                    {"key": "B", "text": "Diyetteki protein eksikliğinin ağır hipoalbüminemiye ve onkotik basınç düşüşüne yol açması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Proteinden yoksun beslenme albümin sentezini çökertir ve ödeme yol açar."},
                    {"key": "C", "text": "Çocuğun aşırı miktarda tuzlu su içmesi", "isCorrect": False, "explanation": "Tuz alımıyla doğrudan ilişkili değildir."},
                    {"key": "D", "text": "Kemik iliğinde lösemi gelişmesi", "isCorrect": False, "explanation": "Lösemi bu tablonun nedeni değildir."}
                ]
            )
        ]
    })

    return slides
