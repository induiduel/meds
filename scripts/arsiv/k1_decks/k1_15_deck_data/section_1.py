# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-15-s01",
        "title": "Doku Onarımına Giriş: Biyolojik Bütünlüğün Yeniden Kurulması",
        "content": "Doku onarımı (repair), doku hasarı oluştuktan sonra organizmanın hayatta kalabilmek için anatomik bütünlüğü ve işlevi yeniden kazanma çabasıdır:\n\n- **Biyolojik Savunmanın Devamı:** Akut enflamasyon zararlı etkeni ortadan kaldırıp nekrotik enkazı temizledikten hemen sonra onarım süreci devreye girer.\n- **İki Temel Bileşenin Etkileşimi:** Onarım süreci parankim hücreleri ile ekstrasellüler matriks (ECM) arasındaki sıkı biyokimyasal diyaloğa dayanır.\n- **Klinik Hedef:** İdeal olan, hasar gören dokunun orijinal mimarisine ve işlevine tam olarak geri dönmesidir (restitutio ad integrum).\n- **Hasarın Boyutu:** Eğer hasar çok derinse veya dokunun çoğalma yeteneği yoksa, organizma kusursuz restorasyon yerine dokuyu fibröz bir bağ dokusu yamasıyla (skar) kapatmak zorunda kalır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İdeal Doku Onarımı vs Fibröz Yama Onarımı",
                "İdeal Onarım (Restitutio ad Integrum)",
                "Orijinal hücreler çoğalarak doku mimarisini ve fizyolojik fonksiyonunu eksiksiz biçimde geri kazandırır.",
                "Fibröz Yama Onarımı (Skar Dokusu)",
                "Ölü hücrelerin yerini kollajen bağ dokusu alır; anatomik bütünlük sağlanır ancak özgül işlev kaybolur."
            ),
            make_cloze(
                "Hasar gören bir dokunun orijinal mimarisine ve işlevine tamamen geri dönmesine tam rejenerasyon denir.",
                "rejenerasyon",
                "Doku hücresel yenilenme terimi"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-15-s02",
        "title": "İki Temel Onarım Yolu: Rejenerasyon vs Skarla Onarım (Fibrozis)",
        "content": "Patolojide doku onarımı iki temel fizyopatolojik mekanizma üzerinden yürütülür (Sınav Spotu):\n\n- **1. Rejenerasyon (Restorasyon):**\n  - Hasar gören hücrelerin, geride kalan sağlam aynı tip hücrelerin çoğalması veya kök hücrelerin farklılaşmasıyla yenilenmesidir.\n  - **Ön Şartı:** Dokunun bölünme yeteneğinde olması ve **ekstrasellüler matriks (ECM) çatısının (özellikle bazal membranın) sağlam kalmasıdır**.\n  - Örnek: Karaciğer rezeksiyonu sonrası büyüme, bağırsak epitel erozyonunun iyileşmesi.\n- **2. Skarla Onarım (Bağ Dokusu Depolanması / Fibrozis):**\n  - Hasar çok genişse, ECM çatısı yıkılmışsa veya hücreler bölünemiyorsa parankimin yerini fibröz bağ dokusu (kollajen) alır.\n  - Skar dokusu yapısal bir yama görevi görür; çekme kuvveti sağlar ancak salgı veya kasılma yapamaz.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Rejenerasyon", "Skarla Onarım (Fibrozis)"],
                [
                    ["Hücre Çoğalma Tipi", "Orijinal parankim veya kök hücreler", "Fibroblastlar ve vasküler endotel"],
                    ["ECM / İskelet Durumu", "Bazal membran ve çatı kesinlikle SAĞLAM", "ECM çatısı hasarlı veya tamamen PARÇALANMIŞ"],
                    ["Nihai Doku Yapısı", "Normal orijinal doku mimarisi", "Avasküler yoğun kollajen skar dokusu"],
                    ["Fonksiyonel Kapasite", "Tam veya tama yakın korunur", "Kayıptır (yalnızca mekanik destek sağlar)"]
                ]
            ),
            make_quiz(
                "Hasar gören bir dokunun fibröz skar bırakmadan tamamen 'rejenerasyon' yoluyla iyileşebilmesi için aşağıdakilerden hangisi mutlak bir ön koşuldur?",
                [
                    {"key": "A", "text": "Dokuda nötrofillerin en az 3 ay boyunca canlı kalması", "isCorrect": False, "explanation": "Nötrofillerin uzun süre kalması kronik doku yıkımına ve fibrozise yol açar."},
                    {"key": "B", "text": "Hasar gören hücrelerin bölünme yeteneğinde olması ve ekstrasellüler matriks (ECM) iskeletinin sağlam kalması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Rejenerasyon için hücrelerin çoğalabilmesi VE çoğalan hücrelere yol gösteren ECM/bazal membran çatısının sağlam olması şarttır."},
                    {"key": "C", "text": "Yaralanan bölgede kan damarlarının tamamen tıkanması", "isCorrect": False, "explanation": "Damarların tıkanması iskemik nekroza neden olur."},
                    {"key": "D", "text": "Kollajen sentezinin tamamen engellenmesi", "isCorrect": False, "explanation": "Kollajen her onarımda temel yapıtaşıdır."}
                ]
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-15-s03",
        "title": "Hücre Çoğalma Kapasitesine Göre Dokuların Sınıflandırılması",
        "content": "Vücuttaki dokuların hasara karşı rejenerasyon yeteneği, hücrelerin hücre döngüsündeki (hücre siklusu) durumuna göre belirlenir:\n\n- **Tarihi Sınıflandırma (Bizzozero Sınıflaması - Sınav Spotu):**\n  1. **Labil (Sürekli Bölünen) Dokular:** Hücre döngüsünde sürekli G1-S-G2-M fazlarında aktif olarak dolaşan dokulardır.\n  2. **Stabil (Sessiz / Koşullu Bölünen) Dokular:** Normalde dinlenme fazında (G0) sessizce bekleyen, ancak hasar veya büyüme faktörü uyarısıyla hızla G1 fazına girip bölünen dokulardır.\n  3. **Kalıcı (Non-Proliferatif / Permanant) Dokular:** Embriyonik gelişimden sonra hücre döngüsünü tamamen terk etmiş (post-mitotik), çoğalma yeteneği olmayan dokulardır.\n- **Klinik Yansıma:** Bir enfarktüs karaciğerde veya deride olursa rejenerasyon şansı yüksektir; ancak kalpte veya beyinde olursa mutlaka kalıcı skar kalır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Labil Doku vs Kalıcı (Permanant) Doku Davranışı",
                "Labil Doku (Kemik İliği / Deri)",
                "Hücre döngüsünde sürekli aktiftir; kök hücrelerden her saniye milyonlarca yeni hücre üretilir.",
                "Kalıcı Doku (Kalp Kası / Nöron)",
                "Hücre döngüsünden kalıcı olarak çıkmıştır; hasar gördüğünde bölünüp yenilenemez, fibröz skarla dolar."
            ),
            make_cloze(
                "Normalde G0 fazında dinlenen ancak doku kaybı uyarısıyla hücre döngüsüne girip bölünebilen dokulara stabil dokular denir.",
                "stabil",
                "Koşullu bölünen doku grubu terimi"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-15-s04",
        "title": "Labil (Sürekli Bölünen) Dokular ve Stem Cell Kompartımanı",
        "content": "Labil dokularda yaşam boyu sürekli fizyolojik bir hücre kaybı ve bunun eşzamanlı yenilenmesi söz konusudur:\n\n- **Hücre Döngüsü:** Hücreler döngüden hiç çıkmaz; sürekli prolifere olur.\n- **Labil Doku Örnekleri (Sınav Sorusu):**\n  - **Hematopoetik Sistem:** Kemik iliğindeki hematopoetik kök hücreler (alyuvar, akyuvar, trombosit üretimi).\n  - **Çok Katlı Yassı Epitel:** Deri epidermisi, ağız boşluğu, farinks, özofagus, vajina ve serviks epiteli.\n  - **Kübik/Silindirik Epitel:** Gastrointestinal sistem mukozası (mide, ince ve kalın bağırsak epiteli), safra yolları, uterus ve fallop tüpü epiteli.\n  - **Transizyonel Epitel (Ürotelyum):** Mesane, üreter ve böbrek pelvisi epiteli.\n- **Kök Hücre Bağımlılığı:** Yüzeydeki dökülen yaşlı hücrelerin yerini bazal tabakada yer alan erişkin kök hücrelerin bölünmesiyle oluşan yeni hücreler alır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Labil Doku Türü", "Örnek Organ / Bölge", "Kök Hücre Rezervi"],
                [
                    ["Kemik İliği", "Hematopoetik sistem", "CD34+ Hematopoetik kök hücreler"],
                    ["Çok Katlı Skuamöz Epitel", "Epidermis, ağız içi, özofagus", "Stratum basale (bazal tabaka) hücreleri"],
                    ["Silindirik Epitel", "İnce ve kalın bağırsak mukozası", "Kript tabanındaki Lgr5+ kök hücreler"],
                    ["Transizyonel Epitel", "Mesane, üreter (ürotelyum)", "Bazal ürotelyal kompartıman"]
                ]
            ),
            make_quiz(
                "Aşağıdaki dokulardan hangisi sürekli bölünen (labil) dokular sınıfında yer alır?",
                [
                    {"key": "A", "text": "Miyokard (kalp kası)", "isCorrect": False, "explanation": "Miyokard kalıcı (permanant) dokudur."},
                    {"key": "B", "text": "Beyin korteks nöronları", "isCorrect": False, "explanation": "Nöronlar kalıcı (permanant) hücrelerdir."},
                    {"key": "C", "text": "Gastrointestinal sistem mukoza epiteli", "isCorrect": True, "explanation": "Doğru cevap C'dir: Mide ve bağırsak epitel hücreleri birkaç günde bir dökülüp yenilenen klasik labil dokudur."},
                    {"key": "D", "text": "Karaciğer parankim hepatositleri", "isCorrect": False, "explanation": "Hepatositler stabil (sessiz) dokudur."}
                ]
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-15-s05",
        "title": "Stabil (Sessiz / G0) Dokular: Koşullu Çoğalan Hücreler",
        "content": "Stabil dokular vücudun metabolik fabrikalarıdır; rutin koşullarda hücre bölünme hızı çok düşüktür ancak muazzam bir yedek çoğalma potansiyeline sahiptirler:\n\n- **Hücre Döngüsü:** Normalde **G0 (dinlenme) fazında** bulunurlar. Doku kaybı, cerrahi rezeksiyon veya toksik hasar meydana geldiğinde büyüme faktörlerinin uyarısıyla hızla G1 fazına girip mitoza başlarlar.\n- **Stabil Doku Örnekleri (Sınav Spotu):**\n  - **Parankimal Organlar:** **Karaciğer (hepatositler)**, **böbrek (tübül epitel hücreleri)** ve **pankreas (asiner ve adacık hücreleri)**.\n  - **Mezenkimal Hücreler:** Fibroblastlar, miyofibroblastlar ve düz kas hücreleri.\n  - **Vasküler Endotel:** Damar endotel hücreleri (anjiyogenez için hızla uyarılır).\n  - **Kondrosit ve Osteositler:** Kıkırdak ve kemik hücreleri (kırık onarımı).\n- **Kritik Kural:** Stabil dokularda rejenerasyon olabilmesi için **ECM iskeletinin sağlam olması** şarttır. Örneğin viral hepatitte retikülin çatısı sağlamsa karaciğer tam iyileşir; çatı çökerse siroz (skar) gelişir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Stabil Hücrenin Hasar Sonrası Aktivasyon Döngüsü",
                [
                    "1. Sessiz Faz (G0): Hepatosit veya tübül hücresi metabolik görevini yapar, bölünmez.",
                    "2. Hasar Sinyali: Sitokinler (TNF, IL-6) ve büyüme faktörleri (HGF, EGF) reseptörlere bağlanır.",
                    "3. G0'dan G1'e Geçiş (Priming): Hücre döngüsü inhibitörleri kalkar, siklin D ekspresyonu artar.",
                    "4. DNA Replikasyonu (S Fazı): Hücre genetik materyalini kopyalar ve mitoza (M fazı) girer.",
                    "5. Doku Bütünlüğü ve Stop: Hedef kütleye ulaşılınca TGF-beta etkisiyle tekrar G0'a döner."
                ]
            ),
            make_cloze(
                "Karaciğer parankimi ve böbrek tübül epiteli normalde G0 fazında bekleyen stabil doku örnekleridir.",
                "tübül",
                "Böbrekteki sessiz bölünebilir epitel yapısı"
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-15-s06",
        "title": "Kalıcı (Non-Proliferatif / Post-Mitotik) Dokular",
        "content": "Kalıcı dokular embriyogenez ve erken postnatal dönemde son farklılaşmasını tamamlamış ve mitoz yeteneğini tamamen kaybetmiş hücrelerden oluşur:\n\n- **Hücre Döngüsü:** Hücre döngüsünü kesin olarak terk etmişlerdir (post-mitotik). Hasar gördüklerinde yerlerine yenisi yapılamaz.\n- **Kalıcı Doku Örnekleri (Sınav Sorusu):**\n  - **Santral Sinir Sistemi Nöronları:** Beyin ve omurilik nöronları öldüğünde bölünerek çoğalamaz; oluşan nekroz alanı astrositlerin çoğalmasıyla **glial skar (gliozis)** ile onarılır.\n  - **Kardiyak Miyositler (Miyokard):** Kalp kası hücreleri öldüğünde (miyokard enfarktüsü) bölünüp kalbi yenileyemez; nekroz alanı tamamen **kollajenöz fibröz skar** dokusuna dönüşür.\n  - **Çizgili İskelet Kası:** Büyük oranda kalıcıdır; ancak kılıfları altında bulunan az sayıdaki **satellit hücre** sayesinde çok sınırlı bir rejenerasyon potansiyeli gösterir.\n- **Klinik Sonuç:** Miyokard enfarktüsü veya inme (stroke) geçiren bir hastada hasar daima kalıcı bir kayıp ve skar ile sonlanır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Aşağıdaki hücre tiplerinden hangisi hasar gördüğünde çoğalarak dokuyu rejenere edemeyen 'kalıcı (permanant)' hücreler grubundadır?",
                [
                    {"key": "A", "text": "Deri bazal tabaka keratinositleri", "isCorrect": False, "explanation": "Keratinositler labil hücrelerdir, hızla çoğalırlar."},
                    {"key": "B", "text": "Karaciğer hepatositleri", "isCorrect": False, "explanation": "Hepatositler stabil hücrelerdir, bölünebilirler."},
                    {"key": "C", "text": "Vasküler endotel hücreleri", "isCorrect": False, "explanation": "Endotel hücreleri stabil hücrelerdir; anjiyogenezde prolifere olurlar."},
                    {"key": "D", "text": "Kardiyak miyositler (kalp kası hücreleri)", "isCorrect": True, "explanation": "Doğru cevap D'dir: Kardiyak miyositler ve nöronlar post-mitotik kalıcı hücrelerdir; enfarktüs sonrası yerlerini fibröz skar dokusu alır."}
                ]
            ),
            make_recall(
                "Miyokard enfarktüsü geçiren bir hastanın kalp kasında hasarlı bölgenin iyileşmesi neden daima bir fibröz skar dokusu ile sonuçlanır?",
                "Çünkü kardiyak miyositler post-mitotik kalıcı hücrelerdir; mitoz yetenekleri olmadığı için ölen kas liflerinin yerini fibroblastlar ve kollajen bağ dokusu yaması doldurur."
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-15-s07",
        "title": "Ekstrasellüler Matriksin (ECM) Kritik Bütünlüğü",
        "content": "Rejenerasyon ile skarla iyileşme arasındaki kavşak noktasını belirleyen en hayati faktör **ekstrasellüler matriksin (ECM) fiziksel ve biyokimyasal bütünlüğüdür**:\n\n- **ECM Bir 'Harç' Değil, Bir 'Orkestra Şefidir':** ECM yalnızca hücreleri bir arada tutan pasif bir dolgu maddesi değildir; hücre çoğalmasını, kutuplaşmasını (polarite), göçünü ve farklılaşmasını kontrol eden dinamik bir kılavuzdur.\n- **İskelet Görevi:** Bölünen hücrelerin dokunun orijinal 3 boyutlu mimarisini yeniden oluşturabilmesi için bir kalıp/iskelet (scaffold) olarak ECM bazal membranına tutunmaları şarttır.\n- **İki Temel ECM Formu:**\n  1. **İnterstisyel Matriks:** Fibriler kollajen (Tip I, III), elastin ve fibronektinden zengin gevşek ağ.\n  2. **Bazal Membran:** Epitel ve endotelin oturduğu Tip IV kollajen, laminin ve proteoglikanlardan oluşan sıkı bariyer.\n- **Sonuç:** Bazal membran parçalandığında, çoğalan parankim hücreleri yönünü kaybeder, düzensiz prolifere olur ve alan fibroblastlar tarafından skarla doldurulur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "ECM İskeleti Sağlamken vs ECM İskeleti Parçalanmışken Onarım",
                "ECM / Bazal Membran Sağlam (Erozyon)",
                "Prolifere olan epitel hücreleri bazal membrana tutunarak dokuyu orijinal mimarisine kavuşturur; skar kalmaz.",
                "ECM / Bazal Membran Yıkılmış (Derin Ülser / Nekroz)",
                "Kılavuz iskelet yok olduğu için parankim organize olamaz; alan yoğun granülasyon dokusu ve skarla dolar."
            ),
            make_cloze(
                "Rejenerasyonun kusursuz gerçekleşebilmesi için bölünen hücrelere kılavuzluk eden bazal membran çatısının sağlam kalması şarttır.",
                "membran",
                "Epitelin oturduğu sınır tabakası kelimesi"
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-15-s08",
        "title": "Hasarın Şiddeti ve İyileşme Yolunun Belirlenmesi",
        "content": "Aynı organda dahi hasarın derinliği ve süresi onarımın sonucunu doğrudan tayin eder:\n\n- **Yüzeysel Epitel Hasarı (Erozyon):**\n  - Yalnızca epitel hücreleri dökülmüştür; alttaki bazal membran ve dermis/submukoza sağlamdır.\n  - Komşu sağlam epitel hücreleri hızla bazal membran üzerinde kayarak (re-epitelizasyon) açığı kapatır. **Skar oluşmaz, tam rejenerasyon gerçekleşir**.\n- **Derin Hasar (Ülser ve Nekroz):**\n  - Bazal membran parçalanmış, dermis veya bağ dokusu stroma yatağı tahrip olmuştur.\n  - Sadece epitel çoğalması yetmez; açılan derin kraterin önce **granülasyon dokusu** ile doldurulması gerekir. **Kalıcı skar dokusu oluşur**.\n- **Kronik İnflamasyon:** Hasar aralıksız sürerse (ör. kronik hepatit, kronik peptik ülser) devam eden sitokin salınımı aşırı fibroblast aktivasyonuna ve yaygın fibrozise (organ sertleşmesine) yol açar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hasar Tipi", "Tutulan Katmanlar", "ECM Durumu", "Onarım Sonucu"],
                [
                    ["Erozyon (Yüzeysel)", "Sadece epitel katmanı", "Bazal membran SAĞLAM", "Tam Rejenerasyon (Skar yok)"],
                    ["Ülser (Derin)", "Epitel + Bazal membran + Stroma", "Bazal membran PARÇALANMIŞ", "Granülasyon Dokusu ve Skar"],
                    ["Apse / Geniş Nekroz", "Tüm doku mimarisi erimiş", "Tamamen tahrip", "Yoğun Kollajen Skar ve Büzülme"],
                    ["Kronik Toksik Hasar", "Tekrarlayan parankim ölümü", "Sürekli kollajen birikimi", "Parankimal Organ Fibrozisi (Siroz)"]
                ]
            ),
            make_quiz(
                "Mide mukozasında sadece yüzey epitelini tutan ve bazal membranı aşmayan bir hasar (erozyon) ile muskularis mukozayı aşan derin bir peptik ülserin iyileşmesi arasındaki temel fark nedir?",
                [
                    {"key": "A", "text": "Erozyonda granülasyon dokusu oluşurken, ülser hiçbir iz bırakmadan rejenere olur", "isCorrect": False, "explanation": "Tam tersidir; granülasyon dokusu ve skar derine inen ülserde oluşur."},
                    {"key": "B", "text": "Erozyon bazal membran sağlam olduğu için skarsız tam rejenere olur; derin ülser ise granülasyon dokusu ve fibröz skarla iyileşir", "isCorrect": True, "explanation": "Doğru cevap B'dir: Bazal membran sağlam kaldığında epitel skarsız rejenere olur; derin ülserde ECM parçalandığı için fibröz skar oluşur."},
                    {"key": "C", "text": "Her iki lezyon da zorunlu olarak mide kanserine dönüşür", "isCorrect": False, "explanation": "Onarım fizyolojik bir süreçtir, doğrudan malign transformasyon değildir."},
                    {"key": "D", "text": "Midede hiçbir hasar türü iyileşemez", "isCorrect": False, "explanation": "Mide mukozası son derece hızlı iyileşen bir labil dokudur."}
                ]
            )
        ]
    })

    # Slide 9 - CHECKPOINT 1
    slides.append({
        "id": "k1-15-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Doku Onarımı Temelleri, Rejenerasyon ve Hücre Döngüsü",
        "content": "Bu checkpointte doku onarımının temel kurallarını ve hücre sınıflamasını pekiştiriyoruz:\n\n- **İki Yol:** Rejenerasyon (orijinal hücre çoğalması) vs Skarla Onarım (kollajen yama).\n- **Rejenerasyonun 2 Şartı:** Hücrelerin bölünebilmesi VE ekstrasellüler matriks (ECM) iskeletinin sağlam kalması.\n- **Labil Dokular:** Sürekli bölünenler (Kemik iliği, deri epidermisi, GIS mukoza epiteli, ürotelyum).\n- **Stabil Dokular:** Normalde G0'da bekleyen, uyarılınca G1'e girenler (Karaciğer hepatositleri, böbrek tübülleri, pankreas, vasküler endotel, fibroblastlar).\n- **Kalıcı (Permanant) Dokular:** Post-mitotik, çoğalamayanlar (Nöronlar, kardiyak miyositler). Hasarları daima fibröz skar ile onarılır.\n- **Hasar Derinliği:** Yüzeysel erozyon skarsız tam rejenere olurken; bazal membranı yıkan derin ülser ve nekrozlar skarla onarılır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Doku Onarım Yolunun Belirlenme Algoritması",
                [
                    "1. Doku Hasarı Oluşumu: İskemi, travma, enfeksiyon veya toksin dokuyu zedeler.",
                    "2. Hücre Tipinin Değerlendirilmesi: Hasar gören hücre kalıcı ise doğrudan skar yoluna girilir.",
                    "3. ECM İskeletinin Kontrolü: Labil/stabil hücrede bazal membran sağlamsa rejenerasyon başlar.",
                    "4. Çatı Yıkılmışsa Skar: ECM parçalanmışsa fibroblastlar alana girer ve kollajen skar üretilir."
                ]
            ),
            make_table(
                ["Doku Sınıfı", "Hücre Siklusu Durumu", "Tipik Örnek Organ", "Hasar Sonucu"],
                [
                    ["Labil", "Sürekli G1-S-G2-M aktif", "Bağırsak epiteli, epidermis, kemik iliği", "Hızlı tam rejenerasyon"],
                    ["Stabil", "G0 fazında sessiz, koşullu aktif", "Karaciğer parankimi, böbrek tübülü", "ECM sağlamsa rejenerasyon"],
                    ["Kalıcı", "Post-mitotik (siklus dışı)", "Kalp kası (miyokard), beyin nöronları", "Daima kalıcı skar dokusu"]
                ]
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-15-s10",
        "title": "Mini Vaka: Miyokard İnfarktüsü vs Deri Sıyrığında Hücresel Onarım Karşılaştırması",
        "content": "Acil servise iki hasta başvuruyor: Birincisi bisikletten düşüp dizinde geniş bir deri sıyrığı (erozyon) olan 8 yaşında bir çocuk; ikincisi koroner arter tıkanıklığı nedeniyle sol ventrikül ön duvarında transmural enfarktüs gelişen 58 yaşında bir yetişkin:\n\n- **Hasta 1 (Çocuk - Deri Sıyrığı):**\n  - Epidermis labil hücrelerden oluşur; bazal membran ve kıl folikülü kök hücreleri sağlam kalmıştır.\n  - 7 gün içinde keratinositler prolifere olarak sıyrığı tamamen örter; **deride hiçbir skar dokusu kalmaz**.\n- **Hasta 2 (Yetişkin - Miyokard Enfarktüsü):**\n  - Kardiyak miyositler kalıcı (post-mitotik) hücrelerdir; iskemiyle ölen kas hücreleri bölünemez.\n  - Alan nötrofil ve makrofajlarca temizlendikten sonra granülasyon dokusu gelişir ve 6-8 hafta içinde **yoğun kollajen fibröz skarla** yer değiştirir.\n  - Skar alanı kasılamaz; sol ventrikülde ejeksiyon fraksiyonu düşer ve kalp yetmezliği gelişir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Miyokard Enfarktüsü Sonrası İyileşme Beklentisi",
                "Enfarktüs geçiren hastanın oğlu, 'Babamın ölen kalp kasları zamanla çoğalıp kendini yeniler mi, eski gücüne kavuşur mu?' diye soruyor. Patofizyolojik gerçeklere dayalı en doğru hekim cevabı hangisidir?",
                [
                    {
                        "text": "'Evet, kalp kası labil bir dokudur; 1 ay içinde bölünen yeni kas hücreleriyle kalp tamamen orijinal haline döner.'",
                        "outcome": "Ölümcül tıbbi yanılgı: Kalp kası kalıcı dokudur, asla bu şekilde rejenere olamaz.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Maalesef ölen kalp kası hücreleri bölünme yeteneğine sahip değildir; hasarlı bölge kalıcı bir bağ dokusu (skar) ile iyileşir ve kasılma fonksiyonunu kaybeder, bu yüzden kalbi koruyucu ilaçlar kullanacağız.'",
                        "outcome": "Kusursuz patolojik ve klinik bilgilendirme: Kalıcı doku gerçeği ve skar oluşumu doğru anlatılır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Kalp kası ölmez, sadece uyur; aspirin verince hemen uyanıp kasılacaktır.'",
                        "outcome": "Bilim dışı açıklama.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada çocuğun dizindeki deri sıyrığının skarsız iyileşmesini sağlayan temel biyolojik faktör nedir?",
                [
                    {"key": "A", "text": "Epidermisin labil doku olması ve kök hücre kompartımanının korunmuş olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Epidermis labil dokudur; bazal membran ve kök hücreler sağlamsa hızla rejenere olur ve skar bırakmaz."},
                    {"key": "B", "text": "Çocuğun aşılarının eksiksiz olması", "isCorrect": False, "explanation": "Aşılar enfeksiyonu önler, doku rejenerasyon sınıfını belirlemez."},
                    {"key": "C", "text": "Diz ekleminin kalıcı hücrelerden oluşması", "isCorrect": False, "explanation": "Deri labil hücrelerden oluşur."},
                    {"key": "D", "text": "Kollajen sentezinin tamamen sıfır olması", "isCorrect": False, "explanation": "Kollajen her dokuda vardır."}
                ]
            )
        ]
    })

    return slides
