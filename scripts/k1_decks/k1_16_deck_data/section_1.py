# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-16-s01",
        "title": "Hemodinamik Dengeye Giriş: Sıvı Homeostazı ve Vasküler Bütünlük",
        "content": "Hücre ve dokuların canlılığı, devamlı olarak oksijen ve besin maddelerini getiren ve metabolik atıkları uzaklaştıran dengeli bir kan dolaşımına bağlıdır:\n\n- **Dolaşım ve Perfüzyon:** Kardiyovasküler sistem, doku perfüzyonunu sabit tutmak için damar içi hidrostatik ve onkotik basınçları hassas bir dengede yönetir.\n- **Kılcal Damar Değişimi:** Mikrosirkülasyonda kılcal damar çeperi yarı geçirgen bir filtre gibi davranarak interstisyel aralıkla sürekli sıvı ve solüt alışverişi yürütür.\n- **Denge Bozulmasının Sonuçları:** Vasküler tonus, kapiller basınçlar veya pıhtılaşma hemostazı bozulduğunda ödem, hiperemi, konjesyon ve kanama gibi patolojik süreçler ortaya çıkar.\n- **Klinik Yelpaze:** Bu bozukluklar göz kapağındaki zararsız hafif bir şişlikten, ani kardiyak tamponada veya ölümcül hipovolemik şoka kadar uzanır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Fizyolojik Hemodinamik Denge vs Patolojik Dengesizlik",
                "Fizyolojik Denge",
                "Starling kuvvetleri dengededir, lenfatikler sızan sıvıyı drene eder, doku perfüzyonu ve oksijenlenmesi korunur.",
                "Patolojik Dengesizlik",
                "Hidrostatik basınç artışı veya onkotik azalma sıvıyı interstisyuma iter, perfüzyon bozulur ve iskemi gelişir."
            ),
            make_cloze(
                "Hücrelerin oksijenlenmesi ve atıkların temizlenmesi için mikrosirkülasyonda korunan sıvı dengesine hemodinamik homeostaz denir.",
                "hemodinamik",
                "Kan akımı ve vasküler basınç dengesini niteleyen kavram"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-16-s02",
        "title": "Vücut Sıvı Kompartmanları: Dağılım Oranları ve Dinamikleri",
        "content": "İnsan vücudundaki toplam su miktarı ve kompartmanlara dağılımı fizyopatolojik mekanizmaları anlamanın temelidir:\n\n- **Toplam Vücut Suyu:** Sağlıklı bir yetişkinde yağsız vücut ağırlığının yaklaşık %60'ı sudur.\n- **İntrasellüler Kompartman (Hücre İçi):** Toplam vücut suyunun üçte ikisi (2/3) hücrelerimizin içinde yer alır ve sitozolik metabolizmayı yürütür.\n- **Ekstrasellüler Kompartman (Hücre Dışı):** Toplam suyun kalan üçte biri (1/3) hücre dışındadır. Bu bölüm iki ana alt gruba ayrılır:\n  1. **İnterstisyel Sıvı:** Hücre dışı sıvının yaklaşık %80'ini oluşturur; hücreleri çevreleyen mikroskopik doku aralığıdır.\n  2. **İntravasküler Plazma:** Hücre dışı sıvının yaklaşık %20'si (toplam vücut ağırlığının ~%5'i) kan dolaşımındaki damar içi plazma hacmidir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Sıvı Kompartmanı", "Toplam Suya Oranı", "Fizyolojik Görevi", "Patolojik Birikim Yeri"],
                [
                    ["İntrasellüler (Hücre İçi)", "Toplam suyun 2/3'ü (~%67)", "Hücre organelleri ve metabolik enzim ortamı", "Hücresel şişme (hidropik dejenerasyon)"],
                    ["İnterstisyel (Doku Aralığı)", "Ekstrasellüler sıvının ~%80'i", "Hücreler arası besin-oksijen difüzyon yolu", "Dokuda klinik ödem tablosu"],
                    ["İntravasküler Plazma", "Ekstrasellüler sıvının ~%20'si", "Dolaşım hacmi ve kan basıncının korunması", "Hipervolemi veya vasküler konjesyon"]
                ]
            ),
            make_quiz(
                "Sağlıklı bir insanda toplam vücut suyunun kompartmanlara dağılımı ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                [
                    {"key": "A", "text": "Suyun büyük kısmı (%90) damar içinde plazma olarak dolaşır", "isCorrect": False, "explanation": "Plazma toplam vücut ağırlığının yalnızca yaklaşık %5'ini, ekstrasellüler sıvının %20'sini oluşturur."},
                    {"key": "B", "text": "Toplam vücut suyunun yaklaşık 2/3'ü hücre içi (intrasellüler), 1/3'ü ise hücre dışı (ekstrasellüler) alandadır", "isCorrect": True, "explanation": "Doğru cevap B'dir: Vücut suyunun 2/3'ü intrasellüler, 1/3'ü ekstrasellüler kompartmanda yer alır."},
                    {"key": "C", "text": "Hücre içi sıvı miktarı hücre dışı sıvıdan daima daha azdır", "isCorrect": False, "explanation": "Hücre içi sıvı hücre dışı sıvının iki katıdır."},
                    {"key": "D", "text": "İnterstisyel sıvı damar içi plazmadan daha küçük bir hacme sahiptir", "isCorrect": False, "explanation": "İnterstisyel sıvı hücre dışı sıvının büyük bölümünü oluşturur."}
                ]
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-16-s03",
        "title": "Starling Hipotezi ve Mikrosirkülasyondaki Denge Kuvvetleri",
        "content": "Kılcal damar lümeni ile interstisyel doku arasındaki sıvı hareketi Starling kuvvetleri adı verilen dört karşıt vektör tarafından yönetilir:\n\n- **1. Kapiller Hidrostatik Basınç (Pc):** Kanın damar duvarına yaptığı fiziksel itici basınçtır; sıvıyı damardan interstisyuma doğru iter.\n- **2. Plazma Kolloid Ozmotik (Onkotik) Basıncı (πc):** Plazma proteinlerinin (başta albümin) oluşturduğu çekici güçtür; sıvıyı damar içinde tutar ve geri çeker.\n- **3. İnterstisyel Hidrostatik Basınç (Pi):** Doku aralığındaki sıvının oluşturduğu karşı basınçtır (normalde sıfıra yakın veya hafif negatiftir).\n- **4. İnterstisyel Onkotik Basınç (πi):** İnterstisyuma kaçan az miktardaki proteinin oluşturduğu çekim gücüdür.\n- **Net Filtrasyon:** Arteriyol ucunda hidrostatik basınç onkotik basınçtan yüksektir, venül ucunda ise onkotik basınç hidrostatik basıncı aşar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kılcal Damar Boyunca Sıvı Hareketi Basamakları",
                [
                    "1. Arteriyol Ucu: Yüksek kapiller hidrostatik basınç (yaklaşık 35 mmHg) sıvıyı interstisyuma iter.",
                    "2. Doku Boşluğunda Dağılım: Süzülen sıvı hücreler arasındaki interstisyel aralıkta besin maddelerini dağıtır.",
                    "3. Venül Ucu: Düşen hidrostatik basınca karşılık onkotik basınç (yaklaşık 25 mmHg) sıvının %90'ını damara geri çeker.",
                    "4. Lenfatik Drenaj: Geri emilemeyen küçük net sıvı fazlası lenf damarları tarafından toplanır."
                ]
            ),
            make_cloze(
                "Plazma proteinlerinin, özellikle albüminin damar lümeni içinde suyu tutmasını sağlayan çekim gücüne kolloid ozmotik basınç denir.",
                "kolloid ozmotik",
                "Proteinlerin yarattığı onkotik çekim kuvveti"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-16-s04",
        "title": "Arteriyoler Filtrasyon ve Venüler Geri Emilim Dinamikleri",
        "content": "Mikrosirkülasyonda kılcal damar boyunca basınç profili dinamik bir değişim gösterir:\n\n- **Arteriyol Ucunda Durum:**\n  - Kapiller hidrostatik basınç (~32-35 mmHg), plazma onkotik basıncından (~25-26 mmHg) belirgin şekilde yüksektir.\n  - Sonuç: Dışarıya doğru net bir itici filtrasyon basıncı oluşur; su, elektrolitler ve küçük besin molekülleri doku aralığına süzülür.\n- **Venül Ucunda Durum:**\n  - Kan kılcal yataktan geçerken hidrostatik basınç ~12-15 mmHg seviyesine kadar düşer.\n  - Ancak plazma proteinleri damar içinde kaldığı için onkotik basınç (~25 mmHg) değişmez.\n  - Sonuç: İçeriye doğru net bir çekici emilim basıncı oluşur; interstisyel sıvının büyük kısmı tekrar venöz dolaşıma katılır.\n- **Doku Kuruluğu:** Bu hassas denge sayesinde sağlıklı bir dokunun interstisyel aralığı daima 'kuruya yakın' bir durumda tutulur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kapiller Arteriyol Ucu vs Venül Ucu Hemodinamik Profili",
                "Arteriyol Ucu",
                "Hidrostatik basınç onkotik basıncı yener; dokuya doğru net sıvı süzülmesi (filtrasyon) gerçekleşir.",
                "Venül Ucu",
                "Onkotik basınç hidrostatik basıncı yener; dokudan damara doğru net sıvı emilimi (rezorpsiyon) gerçekleşir."
            ),
            make_quiz(
                "Kılcal damarların venöz ucunda interstisyel sıvının damar içine geri emilmesini sağlayan temel kuvvet hangisidir?",
                [
                    {"key": "A", "text": "Dokudaki interstisyel hidrostatik basıncın aşırı yükselmesi", "isCorrect": False, "explanation": "İnterstisyel basınç normalde çok düşüktür."},
                    {"key": "B", "text": "Plazma kolloid ozmotik (onkotik) basıncının lokal hidrostatik basınçtan yüksek olması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Venüler uçta hidrostatik basınç düştüğünden plazma proteinlerinin onkotik çekim kuvveti sıvıyı lümene çeker."},
                    {"key": "C", "text": "Ven duvarındaki düz kasların ritmik kasılması", "isCorrect": False, "explanation": "Venüller mikrosirkülasyonda pasif Starling dengesiyle çalışır."},
                    {"key": "D", "text": "Eritrositlerin damar dışına göç etmesi", "isCorrect": False, "explanation": "Eritrositler fizyolojik olarak damar dışına çıkmaz."}
                ]
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-16-s05",
        "title": "Lenfatik Dolaşımın Emniyet Supabı Rolü ve Sıvı Klirensi",
        "content": "Kılcal damar yatağında Starling dengesi mutlak bir sıfır eşitliğinde değildir:\n\n- **Küçük Net Fazlalık:** Gün boyunca arteriyel uçtan filtrelenen sıvı miktarı, venöz uçtan geri emilen miktardan hafifçe daha fazladır (günde yaklaşık 2-4 litre net interstisyel sıvı).\n- **Lenfatik Drenaj:** Bu küçük net sıvı fazlası ve interstisyuma kaçan az miktardaki makromoleküller/proteinler lenfatik kapillerler tarafından toplanır.\n- **Torasik Kanal ve Venöz Dönüş:** Toplanan lenf sıvısı lenf düğümlerinden süzüldükten sonra duktus torasikus ve sağ lenfatik kanal aracılığıyla sol ve sağ subklavyen venlere boşaltılır.\n- **Ödem Eşiği:** İnterstisyel sıvı oluşumu lenfatiklerin maksimum pompalama kapasitesini aştığında veya lenf yolları tıkandığında aralıkta sıvı göllenir ve klinik ödem ortaya çıkar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Lenfatik Sıvı Drenajı ve Dolaşıma Geri Dönüş Rotası",
                [
                    "1. İnterstisyel Artık Sıvı: Filtrasyonun geri emilemeyen küçük net fazlası dokuda kalır.",
                    "2. Lenfatik Kapiller Alımı: Tek yönlü kapakçıklara sahip lenfatik endotel sıvıyı lümene alır.",
                    "3. Lenf Düğümleri Filtresi: Sıvı lenf nodlarından geçerek antijenik ve hücresel kontrolden geçer.",
                    "4. Büyük Lenfatik Kanallar: Duktus torasikus toplanan lenfi subklavyen venöz sisteme aktarır."
                ]
            ),
            make_cloze(
                "Günde filtrelenen ve venöz uçta emilemeyen net doku sıvısını venöz sisteme taşıyan ana lenfatik toplayıcı kanal duktus torasikus yapısıdır.",
                "duktus torasikus",
                "Vücudun ana lenf toplayıcı gövdesi"
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-16-s06",
        "title": "Ödem ve Efüzyon Tanımları: Terminolojik Farklar",
        "content": "Patolojide dokularda veya boşluklarda anormal sıvı toplanması yerleşim yerine göre farklı terimlerle adlandırılır:\n\n- **Ödem (Edema):** Dokuların hücreler arası interstisyel boşluğunda aşırı miktarda seröz sıvı birikmesidir. Organın hacmi ve ağırlığı artar.\n- **Efüzyon (Sıvı Toplanması):** Sıvının doku aralığında değil, vücudun anatomik seröz boşluklarında birikmesidir.\n  - **Hidrotoraks:** Plevral boşlukta aşırı seröz sıvı toplanması (plevral efüzyon).\n  - **Hidroperikardiyum:** Perikard kesesinde seröz sıvı toplanması (perikardiyal efüzyon).\n  - **Hidroperiton (Asit):** Periton boşluğunda seröz sıvı toplanması.\n- **Klinik Önem:** Efüzyonlar akciğeri çökertebilir (atelektazi), perikardda birikerek kalbi sıkıştırabilir (tamponad) veya karında diyaframı yukarı iterek solunumu zorlaştırabilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Patolojik Durum", "Sıvının Biriktiği Anatomik Alan", "Tipik Klinik Belirti", "Acil Komplikasyon"],
                [
                    ["Ödem", "İnterstisyel doku aralığı", "Bacakta çukur bırakan şişlik", "Doku nekrozu, yara açılması"],
                    ["Hidrotoraks", "Plevra yaprakları arası boşluk", "Solunum seslerinde azalma, matite", "Kompresyon atelektazisi, dispne"],
                    ["Hidroperikardiyum", "Perikard yaprakları arası", "Kalp seslerinin derinden gelmesi", "Kardiyak tamponad ve şok"],
                    ["Hidroperiton (Asit)", "Peritoneal boşluk", "Karında distansiyon ve dalgalanma", "Spontan bakteriyel peritonit"]
                ]
            ),
            make_quiz(
                "Periton boşluğunda aşırı miktarda seröz sıvı toplanması klinik patolojide hangi özel terimle ifade edilir?",
                [
                    {"key": "A", "text": "Hidrotoraks", "isCorrect": False, "explanation": "Hidrotoraks plevral boşlukta sıvı birikimidir."},
                    {"key": "B", "text": "Hidroperiton (Asit)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Periton boşluğunda seröz sıvı toplanmasına hidroperiton veya asit denir."},
                    {"key": "C", "text": "Hidroperikardiyum", "isCorrect": False, "explanation": "Hidroperikardiyum perikard boşluğundaki sıvıdır."},
                    {"key": "D", "text": "Hemartroz", "isCorrect": False, "explanation": "Hemartroz eklem içine kanama demektir."}
                ]
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-16-s07",
        "title": "Anasarka: Genel Masif Ödem Tablosu ve Sistemik Dağılım",
        "content": "Sıvı dengesizliğinin en uç ve ağır klinik tablosu anasarka olarak bilinir:\n\n- **Anasarka Tanımı (Sınav Spotu):** Deri altı dokularda aşırı yaygın şişlik ile birlikte vücudun seröz boşluklarında (plevra, perikard, periton) eş zamanlı masif sıvı toplanmasıyla karakterize genel ödem halidir.\n- **Patofizyolojik Ciddiyet:** Lokal bir ven tıkanıklığı sadece tek bir ekstremitede ödem yaparken; anasarka tüm vücudu ilgilendiren ağır sistemik bir yetersizliğin göstergesidir.\n- **En Sık Nedenler:**\n  1. **Ağır Konjestif Kalp Yetmezliği:** Kalp debisinin ileri derecede çökmesi ve masif hidrostatik basınç artışı.\n  2. **Nefrotik Sendrom:** Masif proteinüri nedeniyle plazma albümininin kritik eşiğin altına düşmesi.\n  3. **Son Dönem Karaciğer Sirozu:** Ağır protein sentez kusuru ve yaygın vazodilatasyon.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Lokalize Ödem vs Yaygın Masif Ödem (Anasarka)",
                "Lokalize Ödem",
                "Tek bir uzuvda ven trombozu veya lenfatik hasara bağlıdır; sistemik boşluk tutulumu görülmez.",
                "Anasarka (Genel Masif Ödem)",
                "Tüm deri altı yaygın şiştir; plevra, periton ve perikard boşluklarında eş zamanlı masif sıvı toplanır."
            ),
            make_cloze(
                "Vücudun tüm deri altı dokularında aşırı yaygın şişlik ve seröz boşluklarda sıvı birikimiyle seyreden ağır genel ödeme anasarka denir.",
                "anasarka",
                "Ağır yaygın sistemik ödem tablosuna verilen özel tıbbi isim"
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-16-s08",
        "title": "Transuda ve Eksuda Ayrımı: Protein ve Hücresel İçerik Kriterleri",
        "content": "İnterstisyumda veya boşluklarda biriken sıvının laboratuvar analizi altta yatan patolojiyi ayırt etmede altın standarttır:\n\n- **Transuda (Non-İnflamatuvar Sıvı):**\n  - Vasküler endotel geçirgenliği normaldir; artmış hidrostatik basınç veya azalmış onkotik basınç nedeniyle plazmanın ultrafiltratıdır.\n  - Protein içeriği çok düşüktür (<3 g/dL), dansitesi düşüktür (<1.012) ve hücresel eleman barındırmaz.\n  - Örnek: Kalp yetmezliği veya siroza bağlı ödem ve asit sıvısı.\n- **Eksuda (İnflamatuvar Sıvı):**\n  - Enflamatuvar mediyatörlerin etkisiyle damar geçirgenliği ileri derecede artmıştır.\n  - Plazma proteinlerinden ve fibrin ve nötrofil gibi yangı hücrelerinden son derece zengindir (>3 g/dL protein, dansite >1.020).\n  - Örnek: Bakteriyel plörit, pürülan menenjit, abse içeriği.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Transuda Sıvısı", "Eksuda Sıvısı"],
                [
                    ["Temel Mekanizma", "Hidrostatik basınç ↑ veya onkotik basınç ↓", "Enflamasyona bağlı artmış vasküler geçirgenlik"],
                    ["Endotel Bütünlüğü", "İntakt (sağlam endotel bariyeri)", "Hasarlı / aralıkları açılmış endotel"],
                    ["Protein Düzeyi", "Düşük (< 3 g/dL, albümin ağırlıklı)", "Yüksek (> 3 g/dL, zengin fibrinojen ve immünoglobulin)"],
                    ["Dansite (Özgül Ağırlık)", "Düşük (< 1.012)", "Yüksek (> 1.020)"],
                    ["Hücresel İçerik", "Hücreden fakir (nadir dökülmüş mezotel)", "Çok zengin (nötrofiller, makrofajlar, hücresel enkaz)"]
                ]
            ),
            make_quiz(
                "Plevra boşluğundan alınan sıvının analizinde protein düzeyinin <1.5 g/dL ve dansitesinin 1.008 olduğu saptanıyor. Bu sıvı için hangisi doğrudur?",
                [
                    {"key": "A", "text": "Bakteriyel enfeksiyona bağlı gelişmiş tipik bir pürülan eksudadır", "isCorrect": False, "explanation": "Bakteriyel enfeksiyonlarda protein >3 g/dL ve dansite >1.020 olan eksuda görülür."},
                    {"key": "B", "text": "Damar geçirgenliği artışına bağlı değil, hidrostatik veya onkotik dengesizliğe bağlı gelişen transudadır", "isCorrect": True, "explanation": "Doğru cevap B'dir: Düşük protein ve düşük dansite sıvının transuda olduğunu kanıtlar."},
                    {"key": "C", "text": "Malign plevral mezotelyoma için patognomonik eksudadır", "isCorrect": False, "explanation": "Malign sıvılar kural olarak yüksek proteinli eksudadır."},
                    {"key": "D", "text": "Yoğun fibrin ve nötrofil kümesi içerir", "isCorrect": False, "explanation": "Transuda hücresel elemandan fakirdir."}
                ]
            )
        ]
    })

    # Slide 9 - CHECKPOINT 1
    slides.append({
        "id": "k1-16-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Hemodinamik Denge ve Sıvı Kompartmanları",
        "content": "Bu checkpointte hemodinamik dengenin temellerini, sıvı kompartmanlarını ve Starling kanununu pekiştiriyoruz:\n\n- **Sıvı Dağılımı:** Yağsız ağırlığın %60'ı su; bunun 2/3'ü hücre içi (intrasellüler), 1/3'ü hücre dışı (ekstrasellüler: %80 interstisyel, %20 plazma).\n- **Starling Kuvvetleri:** Arteriyol ucunda hidrostatik basınç (filtrasyon), venül ucunda onkotik basınç (rezorpsiyon) hakimdir.\n- **Lenfatik Emniyet:** Net küçük filtrasyon fazlası lenf damarlarıyla toplanıp duktus torasikus üzerinden venöz sisteme aktarılır.\n- **Ödem vs Efüzyon:** Ödem interstisyumda, efüzyon seröz boşluklarda (hidrotoraks, hidroperikardiyum, asit) sıvı birikmesidir.\n- **Anasarka:** Ağır kalp, böbrek veya karaciğer yetmezliğinde görülen yaygın masif deri altı ve boşluk ödemidir.\n- **Transuda vs Eksuda:** Transudada damar intakttır (düşük protein, düşük dansite); eksudada damar geçirgenliği artmıştır (yüksek protein, lökosit zenginliği).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hemodinamik Sıvı Dengesizliği ve Anasarka Gelişim Basamakları",
                [
                    "1. Sistemik Hastalık Başlangıcı: İleri kalp, böbrek veya karaciğer disfonksiyonu gelişir.",
                    "2. Starling Bozulması: Hidrostatik basınç artar veya plazma albümin sentezi düşer.",
                    "3. İnterstisyel Kaçış: Sıvı dokulara süzülür ve lenfatik drenaj kapasitesi aşılır.",
                    "4. Anasarka Tablosu: Deri altı dokulardan sonra plevra, perikard ve peritonda masif sıvı toplanır."
                ]
            ),
            make_table(
                ["Parametre", "Transuda", "Eksuda"],
                [
                    ["Protein Seviyesi", "< 3.0 g/dL", "> 3.0 g/dL"],
                    ["Dansite", "< 1.012", "> 1.020"],
                    ["Hücresel Eleman", "Eritrosit ve lökosit yok denecek kadar az", "Bol nötrofil, makrofaj ve hücresel debris"],
                    ["Etiyoloji", "Kalp yetmezliği, siroz, nefrotik sendrom", "Pnömoni, enfeksiyon, peritonit, vaskülit"]
                ]
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-16-s10",
        "title": "Bölüm Özeti: Sıvı Homeostazı ve Klinik Yansımalar",
        "content": "Bölüm 1 boyunca Starling dengesinin bileşenlerini ve sıvı kompartmanlarının anatomik dağılımını inceledik:\n\n- **Bütünleşik Bakış:** Kapiller hidrostatik basınç, kolloid ozmotik basınç ve lenfatik klirens doku kuruluğunu kusursuz bir uyumla idame ettirir.\n- **Klinik Geçiş:** Bir sonraki bölümde dokudaki bölgesel kan hacmi artışlarını temsil eden iki zıt hemodinamik olguyu — aktif bir süreç olan **hiperemi** ile pasif bir süreç olan **konjesyonu** — derinlemesine karşılaştıracağız.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Doku aralığındaki net sıvı fazlasını toplayarak venöz dolaşıma aktaran ve ödem oluşumunu engelleyen vasküler sistem hangisidir?",
                "Lenfatik sistem (ve duktus torasikus)",
                "Dolaşıma yardımcı tek yönlü kapakçıklı damar ağı"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi transuda oluşumuna yol açan primer mekanizmalardan biridir?",
                [
                    {"key": "A", "text": "Bakteriyel toksinlere bağlı endotel hasarı ve vasküler permeabilite artışı", "isCorrect": False, "explanation": "Endotel geçirgenlik artışı eksudaya yol açar."},
                    {"key": "B", "text": "Plazma kolloid ozmotik basıncının belirgin düşmesi veya venöz hidrostatik basıncın artması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Transudalar endotel sağlamken hidrostatik artış veya onkotik düşüşle meydana gelir."},
                    {"key": "C", "text": "Yoğun nötrofil infiltrasyonu ve proteaz salgılanması", "isCorrect": False, "explanation": "Bu enflamatuvar eksuda tablosudur."},
                    {"key": "D", "text": "Damar duvarında fibrin birikimi ve nekroz", "isCorrect": False, "explanation": "Fibrinoid nekroz eksudatif süreçlerle ilişkilidir."}
                ]
            )
        ]
    })

    return slides
