# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-20-s51",
        "title": "Hiperkoagülabilite (Trombofili) Kavramı ve Kalıtsal Nedenler",
        "content": "Virchow üçlüsünün üçüncü ayağı olan **Hiperkoagülabilite (Trombofili)**, kanın pıhtı oluşturma eğiliminin anormal derecede artmasıdır (Sınav Spotu):\n\n- **Venöz Tromboz ile Güçlü İlişki:** Hiperkoagülabilite, arteriyel trombozdan ziyade özellikle **venöz tromboz (DVT ve Pulmoner Emboli)** patogenezinde birincil belirleyicidir.\n- **Primer (Kalıtsal / Genetik) Trombofililer:**\n  - Pıhtılaşma faktörlerinin veya antikoagülan proteinlerin genlerindeki mutasyonlara bağlı doğumsal durumlardır.\n  - **Sık Görülenler (>%1):**\n    1. **Faktör V Leiden mutasyonu** (Kafkas ırkında %2-15),\n    2. **Protrombin G20210A mutasyonu** (toplumda %1-3),\n    3. Faktör VIII, IX, XI veya fibrinojen düzeyinde polijenik artışlar.\n  - **Nadir Görülenler (<%0.1 ama Ağır):**\n    1. **Antitrombin III (ATIII) eksikliği**,\n    2. **Protein C eksikliği**,\n    3. **Protein S eksikliği**.\n  - **Çok Nadir:** Homozigot homosistinüri ve fibrinoliz defektleri.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kalıtsal Trombofili", "Popülasyon Sıklığı", "Mekanizma", "Tromboz Riski"],
                [
                    ["Faktör V Leiden", "%2 - %15 (En sık)", "Faktör Va'nın APC ile yıkılamaması (Direnç)", "Heterozigotta 3-5 kat, homozigotta 50 kat"],
                    ["Protrombin G20210A", "%1 - %3", "3' UTR mutasyonuyla aşırı protrombin yapımı", "Venöz tromboz riski yaklaşık 3 kat artar"],
                    ["Antitrombin III Eksikliği", "1 / 2000 - 5000 (Nadir)", "Trombin ve Xa'yı frenleyecek serpin yokluğu", "Yüksek tromboz riski; heparin direnci"],
                    ["Protein C / S Eksikliği", "1 / 500 - 1000 (Nadir)", "Faktör Va ve VIIIa inaktivasyonunda yetersizlik", "Genç yaşta tekrarlayan DVT; Varfarin nekrozu"]
                ]
            ),
            make_cloze(
                "Kafkas ırkında en sık görülen kalıtsal trombofili nedeni Faktör V genindeki nokta mutasyonuna bağlı Faktör V Leiden mutasyonudur.",
                "Faktör V Leiden",
                "Aktive Protein C direncine yol açan en yaygın genetik trombofili"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-20-s52",
        "title": "Genetik Trombofili Test Endikasyonları: Kimler Taranmalı?",
        "content": "Her tromboz hastasında genetik trombofili paneli bakmak hem maliyetli hem de gereksizdir; testin istenmesi gereken spesifik klinik senaryolar tanımlanmıştır (Sınav Spotu):\n\n- **Kimlerde Genetik Trombofili Taranmalıdır? (Kılavuz Endikasyonları):**\n  1. **Genç Yaşta Tromboz:** 50 yaşın altında açıklanamayan veya spontan (provoke edilmemiş) venöz tromboz geçiren bireyler.\n  2. **Tekrarlayan (Rekürren) Tromboz:** Hayatında birden fazla kez DVT veya pulmoner emboli atağı geçirenler.\n  3. **Güçlü Aile Öyküsü:** Birinci derece akrabalarında (anne, baba, kardeş) genç yaşta tromboemboli öyküsü bulunanlar.\n  4. **Atipik / Sıra Dışı Yerleşimli Tromboz:** Mezenterik ven, portal ven, splenik ven veya serebral dural sinüs trombozu geçiren hastalar.\n  5. **Tekrarlayan Gebelik Kayıpları:** Açıklanamayan 3 veya daha fazla erken düşük veya intrauterin fetal kayıp öyküsü olan kadınlar.\n- **Kritik Kural:** İleri yaşta, kanser veya kalça protezi ameliyatı gibi ağır edinsel risk faktörü olan bir hastada rutin genetik tarama endike değildir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Trombofili Taraması Endike vs Trombofili Taraması Gereksiz",
                "Trombofili Testi Endike Olanlar",
                "<50 yaş spontan DVT, rekürren tromboz, atipik venöz tromboz (portal/serebral), güçlü aile öyküsü.",
                "Trombofili Testi Gereksiz Olanlar",
                ">65 yaş, ileri evre kanser, majör ortopedik cerrahi sonrası tek bir provake DVT atağı."
            ),
            make_quiz(
                "Aşağıdaki klinik tablolardan hangisinde hastada kalıtsal trombofili paneli (Faktör V Leiden, Protrombin G20210A vb.) taranması EN UYGUNDUR?",
                [
                    {"key": "A", "text": "28 yaşında hiçbir provoke edici faktör yokken derin ven trombozu geçiren ve babasında genç yaşta DVT öyküsü olan genç hasta", "isCorrect": True, "explanation": "Doğru cevap A'dır: 50 yaş altı, provoke edilmemiş spontan venöz tromboz ve güçlü aile öyküsü genetik trombofili taramasının birincil endikasyonudur."},
                    {"key": "B", "text": "75 yaşında pankreas kanseri tanısı olan bir hastada gelişen bacak ödemi", "isCorrect": False, "explanation": "Kanser açık bir edinsel risk faktörüdür (Trousseau sendromu)."},
                    {"key": "C", "text": "Kalça kırığı ameliyatı sonrası 5. günde gelişen izole DVT", "isCorrect": False, "explanation": "Cerrahi provokasyon mevcuttur."},
                    {"key": "D", "text": "Grip enfeksiyonu sırasında burun kanaması geçiren çocuk", "isCorrect": False, "explanation": "Kanama semptomudur, trombofili aranmaz."}
                ]
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-20-s53",
        "title": "Faktör V Leiden (Arg506Gln): Aktive Protein C Direnci",
        "content": "Kalıtsal trombofililerin tartışmasız en sık karşılaşılan formu **Faktör V Leiden mutasyonudur** (Sınav Spotu):\n\n- **Moleküler Genetik Kusur:**\n  - Faktör V geninin ekzon 10 bölgesinde tek bir nükleotid değişimi (**1691 G $\\to$ A missense mutasyonu**) gerçekleşir.\n  - Bu değişim Faktör V proteininin 506. pozisyonundaki amino asidi değiştirir: **Arjinin yerine Glutamin geçer (Arg506Gln / R506Q)**.\n- **Aktive Protein C (APC) Direnci:**\n  - Normalde Aktive Protein C (APC), aktif Faktör Va'yı tam da bu 506. pozisyondaki arjinin noktasından keserek parçalar.\n  - Glutamin geldiğinde APC enzimi kesim bölgesini tanıyamaz; **Faktör Va'yı proteolitik olarak parçalayamaz**.\n- **Sonuç:** Faktör Va protrombinaz kompleksinde uzun süre aktif kalmaya devam eder; trombin üretimi durdurulamaz ve kan sürekli pıhtılaşma eğiliminde kalır.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Faktör V Leiden Patogenez Kaskadı",
                [
                    "1. Nokta Mutasyonu: 1691 G->A değişimi ile 506. amino asit Arg->Gln olur.",
                    "2. Kesim Bölgesi Kaybı: APC enziminin Faktör Va'ya bağlanma bölgesi bozulur.",
                    "3. APC Direnci: Aktive Protein C Faktör Va'yı parçalayamaz.",
                    "4. Uzamış Protrombinaz: Faktör Va kofaktörlüğü kesintisiz devam eder.",
                    "5. Trombin Taşması: Protrombin sürekli trombine çevrilerek tromboz tetiklenir."
                ]
            ),
            make_cloze(
                "Faktör V Leiden mutasyonunda 506. pozisyondaki arjinin amino asidinin glutamine dönüşmesi sonucu Aktive Protein C direnci gelişir.",
                "Aktive Protein C direnci",
                "Faktör Va'nın APC tarafından parçalanamaması sonucu ortaya çıkan patofizyolojik durum"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-20-s54",
        "title": "Faktör V Leiden Klinik Riski: Heterozigot vs Homozigot",
        "content": "Faktör V Leiden mutasyonunun yarattığı tromboz riski, genetik dozaj (heterozigot veya homozigot olma) durumuna göre dramatik fark gösterir (Sınav Spotu):\n\n- **Heterozigot Bireyler:**\n  - Kafkas ırkı popülasyonunun yaklaşık **%2 ila %5'i (bazı Akdeniz izolatörlerinde %10-15)** heterozigot taşıyıcıdır.\n  - Hayat boyu venöz tromboz riski normal popülasyona göre **3 ila 5 kat artmıştır**.\n  - Tek başına heterozigotluk genellikle asemptomatiktir; ancak gebelik, oral kontraseptif kullanımı, cerrahi veya uzun uçak yolculuğu gibi edinsel bir risk eklendiğinde tromboz patlak verir.\n- **Homozigot Bireyler:**\n  - Toplumda yaklaşık 1/1000 oranında görülür.\n  - Venöz tromboz riski normal bireylere göre **yaklaşık 50 kat (25 ila 50 kat)** artmıştır!\n  - Bu bireylerde genç yaşta spontan tekrarlayan DVT ve pulmoner emboli görülür; sıklıkla ömür boyu profilaktik antikoagülasyon gerektirirler.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Faktör V Leiden Heterozigot vs Homozigot",
                "Heterozigot Taşıyıcı (Sık Görülür)",
                "Toplumda %2-5 sıklıktadır; venöz tromboz riski 3-5 kat artar; genellikle edinsel tetikleyiciyle klinik verir.",
                "Homozigot Hasta (Nadir ve Ağır)",
                "Toplumda 1/1000'dir; venöz tromboz riski tam 50 kat artar; genç yaşta spontan DVT'ler kaçınılmazdır."
            ),
            make_quiz(
                "Faktör V Leiden mutasyonunu homozigot olarak taşıyan bir bireyde venöz tromboz gelişme riski normal popülasyona kıyasla yaklaşık ne kadar artmıştır?",
                [
                    {"key": "A", "text": "Yaklaşık 50 kat (25-50 kat)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Faktör V Leiden homozigotlarında venöz tromboz riski yaklaşık 50 kat artarken, heterozigotlarda 3-5 kat civarındadır."},
                    {"key": "B", "text": "Yalnızca 1.2 kat", "isCorrect": False, "explanation": "Bu oran ihmal edilebilir bir risktir."},
                    {"key": "C", "text": "1000 kat", "isCorrect": False, "explanation": "50 kat klasik patoloji ders kitabı değeridir."},
                    {"key": "D", "text": "Risk artışı yoktur", "isCorrect": False, "explanation": "Homozigotluk çok ağır bir risk artışı yaratır."}
                ]
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-20-s55",
        "title": "Protrombin G20210A Mutasyonu: 3' UTR Polimorfizmi",
        "content": "Kalıtsal trombofililerin en sık ikinci nedeni, Protrombin (Faktör II) genindeki bir düzenleyici bölge mutasyonudur (Sınav Spotu):\n\n- **Genetik Değişim:**\n  - Protrombin geninin kodlayan bölgesinde değil, **3' Transkribe Edilmeyen Bölgesinde (3' UTR)** yer alan 20210. nükleotidde Guanin yerine Adenin geçer (**G20210A mutasyonu**).\n  - Protein yapısında hiçbir amino asit değişikliği olmaz (anormal protein üretilmez).\n- **Moleküler Mekanizma:**\n  - 3' UTR mutasyonu, protrombin mRNA'sının hücre içinde yıkılmasını zorlaştırır ve stabilitesini artırır; ayrıca poliadenilasyon sinyalini güçlendirir.\n  - Sonuçta karaciğer hücrelerinde **protrombin mRNA translasyonu hızlanır**.\n- **Klinik Tablo:**\n  - Kanda dolaşan fonksiyonel Protrombin (Faktör II) düzeyi **%30 ila %50 oranında artar**.\n  - Yüksek protrombin substratı, trombin oluşum hızını artırarak venöz tromboz riskini **yaklaşık 2 ila 3 kat** yükseltir; Kafkas ırkında sıklığı %1-3'tür.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Parametre", "Faktör V Leiden", "Protrombin G20210A"],
                [
                    ["Mutasyon Bölgesi", "Kodlayan bölge (Ekzon 10 - Arg506Gln)", "Kodlamayan bölge (3' UTR - 20210 G->A)"],
                    ["Etki Mekanizması", "Protein APC'ye direnç kazanır (inaktivasyon kaybı)", "mRNA stabilitesi artar $\\to$ Protrombin düzeyi %30-50 artar"],
                    ["Toplum Sıklığı", "Kafkaslarda %2 - %5", "Kafkaslarda %1 - %3"],
                    ["Venöz Tromboz Riski", "Heterozigotta 3-5 kat", "Heterozigotta 2-3 kat"]
                ]
            ),
            make_cloze(
                "Protrombin geninin 3' UTR bölgesindeki G20210A mutasyonu mRNA stabilitesini artırarak kanda protrombin düzeyini yükseltir.",
                "3' UTR",
                "Protrombin G20210A mutasyonunun yer aldığı transkribe edilmeyen kontrol bölgesi"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-20-s56",
        "title": "Antitrombin III Eksikliği: Heparin Direnci ve Ağır Tromboz",
        "content": "Kalıtsal trombofililer içinde en nadir (<%0.1) ancak trombüs oluşturma gücü en yüksek olan defekt **Antitrombin III (ATIII) Eksikliğidir** (Sınav Spotu):\n\n- **Genetik Temel:** Kromozom 1q25 lokusundaki **SERPINC1** genindeki mutasyonlara bağlı otozomal dominant bir hastalıktır; homozigotluk yaşamla bağdaşmaz (intrauterin letal).\n- **Patofizyoloji:** Dolaşımda serbest trombin ve Faktör Xa'yı intihar substratı gibi kitleyen temel serpin inhibitörü yarı yarıya azalmıştır.\n- **Klinik Seyir:** Hastaların %80'inden fazlası 20-30'lu yaşlarda spontan, masif ve tekrarlayan derin ven trombozları ve ölümcül pulmoner emboliler geçirir.\n- **Heparin Direnci (Kritik Farmakolojik İpucu):**\n  - Standart heparin, antikoagülan etkisini bizzat Antitrombin III'ü 1000 kat aktive ederek gösterir.\n  - ATIII eksikliği olan bir hastaya yüksek doz intravenöz heparin verilse dahi bağlanacak ATIII bulunmadığı için **hastanın aPTT'si uzamaz ve heparin etkisiz kalır (Heparin Direnci)**.\n  - Tedavide plazma kaynaklı ATIII konsantresi verilmeli veya direkt trombin inhibitörlerine (Argatroban/Bivalirudin) geçilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Antitrombin III Eksikliğinde Heparin Direnci",
                [
                    "1. Genetik Kusur: SERPINC1 mutasyonuyla plazma ATIII düzeyi <%50'ye iner.",
                    "2. Trombüs Gelişimi: Trombin ve Xa nötralize edilemeyip masif DVT yapar.",
                    "3. Heparin Uygulaması: Hastaya standart intravenöz heparin başlanır.",
                    "4. Reseptörsüzlük: Heparin bağlanıp aktive edecek ATIII molekülü bulamaz.",
                    "5. Tedavisizlik: aPTT uzamaz; klinik tromboz heparine rağmen ilerler."
                ]
            ),
            make_quiz(
                "Masif derin ven trombozu nedeniyle terapötik dozda intravenöz fraksiyone olmayan heparin başlanan bir hastada aPTT süresinin hiç uzamadığı ve heparine tam direnç geliştiği saptanıyor. En olası kalıtsal defekt hangisidir?",
                [
                    {"key": "A", "text": "Antitrombin III (ATIII) Eksikliği", "isCorrect": True, "explanation": "Doğru cevap A'dır: Heparin antikoagülan etkisini ATIII üzerinden gösterir; ATIII eksikliğinde heparine direnç gelişir ve aPTT uzamaz."},
                    {"key": "B", "text": "Faktör V Leiden mutasyonu", "isCorrect": False, "explanation": "Faktör V Leiden heparine değil, Aktive Protein C'ye direnç yapar."},
                    {"key": "C", "text": "von Willebrand Hastalığı", "isCorrect": False, "explanation": "vWH bir kanama bozukluğudur."},
                    {"key": "D", "text": "Hemofili A", "isCorrect": False, "explanation": "Hemofili A'da aPTT zaten baştan uzundur."}
                ]
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-20-s57",
        "title": "Protein C ve Protein S Eksiklikleri: Varfarin Nekrozu",
        "content": "K vitamini bağımlı doğal antikoagülanlar olan Protein C ve Protein S eksiklikleri iki eşsiz klinik tabloyla kendini gösterir (Sınav Spotu):\n\n- **1. Varfarin Kaynaklı Deri Nekrozu (Coumadin Nekrozu):**\n  - Protein C'nin plazma yarı ömrü çok kısadır (**yaklaşık 6 saat**); pıhtılaşma faktörlerinin (Faktör X ve Protrombin) yarı ömrü ise çok daha uzundur (40-60 saat).\n  - Protein C eksikliği olan bir hastaya koruyucu heparin verilmeden doğrudan yüksek doz **Varfarin** başlanırsa:\n    - İlk 24 saatte hızla tükenen Protein C sıfırlanır ancak pıhtılaşma faktörleri kanda aktif kalmaya devam eder.\n    - Bu durum paradoksal geçici bir **aşırı hiperkoagülabilite penceresi** yaratır.\n    - Deri ve meme altı mikrovasküler yatakta yaygın trombozlar, damar tıkanıklıkları ve **masif hemorajik deri nekrozu (gangren)** gelişir.\n- **2. Neonatal Purpura Fulminans:**\n  - Homozigot Protein C veya S eksikliği ile doğan yenidoğanlarda doğumdan hemen sonra mikrovasküler yaygın trombozlar, cilt nekrozları ve ölümcül DİK tablosu gelişir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Varfarin Başlangıcı vs Protein C Eksikliğinde Varfarin",
                "Normal Hastada Varfarin (Heparin Köprüsüyle)",
                "Heparin antikoagülasyonu sağlarken Varfarin faktörleri yavaşça düşürür; güvenlidir.",
                "Protein C Eksikliğinde Monoterapi Varfarin",
                "Protein C ilk 6 saatte sıfırlanır; pıhtılaşma faktörleri yüksek kalır $\\to$ Masif cilt nekrozu gelişir."
            ),
            make_cloze(
                "Protein C eksikliği olan bir hastada heparin köprüsü kurulmadan tek başına yüksek doz varfarin başlanması durumunda mikrovasküler tromboza bağlı varfarin nekrozu gelişebilir.",
                "varfarin nekrozu",
                "Protein C'nin kısa yarı ömrü nedeniyle oluşan paradoksal hemorajik cilt kangreni"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-20-s58",
        "title": "Homosistinüri ve Hiperhomosisteinemi: Damar Hasarı",
        "content": "Metabolik genetik bozukluklar da endotel toksisitesi üzerinden ağır trombofilik tablolar oluşturabilir (Sınav Spotu):\n\n- **Homosistinüri (Sistatyonin β-Sentaz Eksikliği):**\n  - Metiyonin metabolizmasında görevli **Sistatyonin β-sentaz (CBS)** enziminin otozomal resesif eksikliğidir.\n  - Kanda ve idrarda devasa miktarlarda homosistein ve homosistin birikir.\n  - Klinik Özellikler: Marfan benzeri uzun parmaklar (marfanoid yapı), lens subluksasyonu (aşağı-içe doğru luksasyon), osteoporoz ve zihinsel yetersizlik.\n- **Vasküler ve Trombotik Yıkım:**\n  - Aşırı homosistein doğrudan endotel hücrelerinde oksidatif stres, apoptoz ve endotelyal nitrik oksit kaybına yol açar.\n  - Hem **arteriyel** (erken yaşta inme ve miyokard enfarktüsü) hem de **venöz** (tekrarlayan DVT ve pulmoner emboli) tromboz riskini onlarca kat artırır.\n  - Bu hastaların yaklaşık %50'si 30 yaşından önce tromboembolik bir vasküler olay geçirir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Homosistinüri (CBS Eksikliği)", "Marfan Sendromu"],
                [
                    ["Genetik Defekt", "Sistatyonin β-sentaz (Metabolik enzim)", "Fibrillin-1 (FBN1 / Yapısal protein)"],
                    ["Lens Dislokasyonu", "Aşağı ve içe doğru (Aşağı subluksasyon)", "Yukarı ve dışa doğru (Yukarı subluksasyon)"],
                    ["Zihinsel Durum", "Sıklıkla zihinsel yetersizlik eşlik eder", "Zeka tamamen normaldir"],
                    ["Tromboz Riski", "Hem arteriyel hem venöz masif tromboz riski", "Aort anevrizması ve diseksiyon riski"]
                ]
            ),
            make_quiz(
                "Marfanoid gövde yapısı, zihinsel gerilik, lensin aşağı-içe subluksasyonu ile birlikte genç yaşta hem arteriyel hem venöz tromboz geçiren bir hastada en olası metabolik enzim eksikliği hangisidir?",
                [
                    {"key": "A", "text": "Sistatyonin β-sentaz (Homosistinüri)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sistatyonin beta-sentaz eksikliğinde homosistein aşırı birikir; marfanoid yapı, lens subluksasyonu ve ağır arteriyel/venöz trombozlar görülür."},
                    {"key": "B", "text": "Fenilalanin hidroksilaz", "isCorrect": False, "explanation": "Fenilketonüri yapar, tromboz yapmaz."},
                    {"key": "C", "text": "Tirozinaz", "isCorrect": False, "explanation": "Albinizm yapar."},
                    {"key": "D", "text": "Glikoz-6-fosfataz", "isCorrect": False, "explanation": "Tip 1 glikojenoz yapar."}
                ]
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-20-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Kalıtsal Hiperkoagülabilite Bozuklukları",
        "content": "Bu checkpointte primer kalıtsal trombofilileri ve patofizyolojik mekanizmalarını özetliyoruz:\n\n- **Faktör V Leiden (Arg506Gln):** En sık kalıtsal trombofili (%2-15). Ekzon 10'da 1691 G $\\to$ A; APC kesim bölgesi bozulur; **Aktive Protein C direnci** gelişir; heterozigotta 3-5 kat, **homozigotta 50 kat DVT riski**.\n- **Protrombin G20210A:** En sık 2. trombofili (%1-3). **3' UTR mutasyonudur**; mRNA stabilitesi artar; kanda protrombin düzeyi %30-50 yükselir; DVT riski 2-3 kat artar.\n- **Antitrombin III (ATIII) Eksikliği:** Nadir ama çok ağır. Serbest trombin ve Xa frenlenemez; **Heparin verildiğinde aPTT uzamaz (Heparin Direnci)**.\n- **Protein C ve S Eksiklikleri:** Faktör Va ve VIIIa inaktive edilemez; Varfarin başlandığında kısa ömürlü Protein C hızla sıfırlanır $\\to$ **Varfarin Deri Nekrozu**.\n- **Homosistinüri (CBS Eksikliği):** Aşırı homosistein endotel hasarı yapar; hem **arteriyel** hem **venöz** tromboz riski vardır; marfanoid yapı ve lens subluksasyonu eşlik eder.\n- **Test Endikasyonu:** <50 yaş, spontan tromboz, rekürren DVT, aile öyküsü ve atipik venöz yerleşimlerde genetik panel istenir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kalıtsal Trombofili", "Mutasyon Lokusu", "Patofizyolojik Sonuç", "En Tipik Klinik İpucu"],
                [
                    ["Faktör V Leiden", "Ekzon 10 (Arg506Gln)", "Aktive Protein C direnci", "En sık kalıtsal DVT nedeni, homozigotta 50 kat risk"],
                    ["Protrombin G20210A", "3' UTR bölgesi", "Protrombin aşırı üretimi", "En sık ikinci trombofili, kanda Faktör II yüksekliği"],
                    ["Antitrombin III Eksikliği", "SERPINC1 (1q25)", "Trombin/Xa kilitlenemez", "Heparin direnci (heparinle aPTT uzamaz)"],
                    ["Protein C / S Eksikliği", "PROC / PROS1 genleri", "Va ve VIIIa inaktive edilemez", "Varfarin nekrozu, neonatal purpura fulminans"],
                    ["Homosistinüri", "CBS geni (21q22)", "Endotel toksisitesi", "Arteriyel + Venöz tromboz, marfanoid yapı"]
                ]
            ),
            make_chain(
                "Kalıtsal Trombofililer Tanı Akışı",
                [
                    "1. Şüpheli Klinik: 50 yaş altı genç bireyde spontan DVT veya atipik tromboz görülür.",
                    "2. Aile Öyküsü: Birinci derece akrabalarda genç yaşta emboli varlığı sorgulanır.",
                    "3. Fonksiyonel Testler: APC direnci testi, ATIII, Protein C ve Protein S düzeyleri ölçülür.",
                    "4. Moleküler Doğrulama: DNA dizi analiziyle Faktör V Leiden ve G20210A mutasyonları saptanır."
                ]
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-20-s60",
        "title": "Bölüm Özeti: Kalıtsal Trombofililerden Edinsel Trombofililere Geçiş",
        "content": "Bölüm 6 boyunca doğumsal genetik trombofilileri (Faktör V Leiden, Protrombin, ATIII, Protein C/S ve CBS) inceledik:\n\n- **Özet:** Kalıtsal trombofililer özellikle venöz sistemde kontrolsüz pıhtılaşmaya yol açar; homozigot formlar yaşamı tehdit eden tekrarlayan trombozlarla seyreder.\n- **Sonraki Bölüm (Bölüm 7):** Yaşamın ilerleyen dönemlerinde ortaya çıkan, kanserle ilişkili **Trousseau sendromunu**, heparinin paradoksal bir komplikasyonu olan **Heparine Bağlı Trombositopeniyi (HIT)** ve klinik triada sahip **Antifosfolipid Antikor Sendromunu (APS)** detaylarıyla ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Kafkas ırkında en sık görülen ve Faktör V proteininde 506. amino asidin arjininden glutamine değişmesiyle oluşan kalıtsal trombofili hangisidir?",
                "Faktör V Leiden mutasyonu",
                "Aktive Protein C direncine neden olan nokta mutasyonu"
            ),
            make_quiz(
                "Protrombin G20210A mutasyonunun pıhtılaşma sisteminde yarattığı temel patofizyolojik değişiklik hangisidir?",
                [
                    {"key": "A", "text": "3' UTR mutasyonu ile mRNA stabilitesinin artması ve kanda protrombin düzeyinin yükselmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: G20210A mutasyonu 3' UTR bölgesindedir ve kanda protrombin (Faktör II) düzeyini %30-50 artırarak tromboza yol açar."},
                    {"key": "B", "text": "Protrombinin Aktive Protein C'ye dirençli hale gelmesi", "isCorrect": False, "explanation": "APC direnci Faktör V Leiden'e aittir."},
                    {"key": "C", "text": "Kanda Antitrombin III düzeyinin sıfırlanması", "isCorrect": False, "explanation": "ATIII eksikliği farklı bir gen mutasyonudur."},
                    {"key": "D", "text": "Trombosit GpIb reseptörünün parçalanması", "isCorrect": False, "explanation": "Bu durum Bernard-Soulier sendromudur."}
                ]
            )
        ]
    })

    return slides
