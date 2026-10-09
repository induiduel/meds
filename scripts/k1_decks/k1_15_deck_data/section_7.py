# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-15-s61",
        "title": "ECM Yeniden Şekillenmesi (Remodeling): Skarın Olgunlaşması",
        "content": "Yara iyileşmesinin en uzun süren evresi olan yeniden şekillenme (remodeling), yaranın 2-3. haftasında başlar ve aylarca, hatta yıllarca sürer:\n\n- **Neden Remodeling Gereklidir?**\n  - Proliferasyon evresinde üretilen granülasyon dokusu kaotiktir; damardan çok zengin, gevşek ve mekanik olarak dayanıksızdır.\n  - Bu dokunun kalıcı, sağlam ve fonksiyonel bir skara dönüşmesi için gereksiz bileşenlerin ayıklanması ve kollajen liflerinin stres çizgileri boyunca hizalanması şarttır.\n- **Sentez ve Yıkım Dengesi (Sınav Spotu):**\n  - Remodeling evresinde kollajen sentezi ile kollajen yıkımı arasında hassas bir denge kurulur.\n  - Matriks metalloproteinazlar (MMP'ler) eski ve dağınık Tip III kollajenleri eritirken, fibroblastlar paralel demetler halinde güçlü Tip I kollajen üretir.\n- **Sonuç:** Granülasyon dokusu geriler; damarlar kurur ve yara beyaz, sert, avasküler bir skar dokusuna dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Genç Granülasyon Dokusu vs Remodeling Geçirmiş Olgun Skar",
                "2. Hafta (Genç Granülasyon)",
                "Kırmızı, yumuşak, aşırı damarlı, bol hücreli ve dağınık Tip III kollajen içerir.",
                "3. Ay (Olgun Skar)",
                "Soluk beyaz, sert, avasküler, az hücreli ve gerilim çizgilerine paralel Tip I kollajen demetleri içerir."
            ),
            make_cloze(
                "Yara iyileşmesinde ECM'nin olgunlaşmasını ve Tip III kollajenin Tip I kollajene dönüşmesini sağlayan evreye remodeling evresi denir.",
                "remodeling",
                "Yeniden şekillenme evresinin bilimsel adı"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-15-s62",
        "title": "Matriks Metalloproteinazlar (MMP'ler) ve Çinko ($Zn^{2+}$) Bağımlılığı",
        "content": "Ekstrasellüler matriksin heykeltıraşları **Matriks Metalloproteinazlar (MMP'ler)** adı verilen özel bir enzim ailesidir:\n\n- **Çinko Bağımlılığı (Sınav Sorusu):**\n  - Bu enzimlerin katalitik merkezinde mutlaka bir **Çinko ($Zn^{2+}$) iyonu** bulunması zorunludur.\n  - Çinko eksikliğinde MMP'ler çalışamaz; bu nedenle çinko eksikliği olan hastalarda yara iyileşmesi ve remodeling ağır şekilde bozulur!\n- **Zimojen Salınımı ve Aktivasyon:**\n  - Fibroblastlar, makrofajlar ve nötrofiller tarafından **inaktif pro-enzimler (pro-MMP)** olarak salgılanırlar.\n  - Yara yatağında doku plazmini veya serbest oksijen radikalleri (ROS) tarafından inaktif parça kesilerek aktive edilirler.\n- **Önemi:** MMP'ler olmasaydı eski matriks eritilemez, yeni damarlar dokuya sızamaz ve skar dokusu kontrolsüzce büyüyerek devasa kitlelere dönüşürdü.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Enzim Grubu", "Temel Kofaktör", "Salınım Şekli", "Aktivasyon Mekanizması"],
                [
                    ["MMP Ailesi", "Çinko ($Zn^{2+}$)", "İnaktif pro-MMP", "Plazmin veya ROS ile proteolitik kesim"],
                    ["Lizil Oksidaz", "Bakır ($Cu^{2+}$)", "Aktif salınım", "Kollajen çapraz bağlanması"],
                    ["Prolil Hidroksilaz", "C Vitamini + $Fe^{2+}$", "Hücre içi aktif", "Prolin/lizin hidroksilasyonu"]
                ]
            ),
            make_quiz(
                "Yara iyileşmesinde ekstrasellüler matriks bileşenlerini yıkarak yeniden şekillenmeyi sağlayan Matriks Metalloproteinaz (MMP) enzimlerinin katalitik aktivitesi için mutlak gerekli metal kofaktörü hangisidir?",
                [
                    {"key": "A", "text": "Magnezyum", "isCorrect": False, "explanation": "Magnezyum nükleik asit metabolizmasında kofaktördür."},
                    {"key": "B", "text": "Çinko (Zn2+)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Matriks metalloproteinazlar çinko bağımlı endopeptidazlardır; adlarındaki 'metallo' terimi çinkodan gelir."},
                    {"key": "C", "text": "Krom", "isCorrect": False, "explanation": "Krom insülin sinyalinde rol oynar."},
                    {"key": "D", "text": "Kobalt", "isCorrect": False, "explanation": "Kobalt B12 vitamininin yapısındadır."}
                ]
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-15-s63",
        "title": "MMP Sınıfları ve Özgül Matriks Substratları",
        "content": "MMP ailesi yıktıkları ekstrasellüler matriks proteinlerine göre 3 majör sınıfa ayrılır (Sınav Spotu):\n\n- **1. İnterstisyel Kollajenazlar (MMP-1, MMP-2, MMP-3, MMP-8):**\n  - Sağlam fibriler kollajenleri (Tip I, Tip II ve Tip III) tanıyan ve üçlü heliksin ortasından spesifik olarak kesen yegane enzimlerdir.\n  - MMP-8 nötrofil kaynaklıdır; akut iltihapta hızla devreye girer.\n- **2. Jelatinazlar (MMP-2 ve MMP-9):**\n  - Kollajenazlar tarafından kesilip açılmış amorf kollajen parçalarını (jelatin) ve özellikle **Tip IV bazal membran kollajenini** parçalarlar.\n  - Anjiyogenezde endotelin bazal membranı delip geçmesini sağlarlar.\n- **3. Stromelisinler (MMP-3, MMP-10, MMP-11):**\n  - Fibronektin, laminin, elastin, proteoglikanlar ve amorf glikoproteinleri parçalarlar; ayrıca diğer pro-MMP'leri aktive ederler.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["MMP Sınıfı", "Önemli Enzimler", "Hedef Substratlar", "Doku Onarımındaki Rolü"],
                [
                    ["Kollajenazlar", "MMP-1, MMP-8, MMP-13", "Fibriler Tip I, II, III kollajen", "Sert kollajen demetlerinin kesilmesi"],
                    ["Jelatinazlar", "MMP-2, MMP-9", "Denatüre kollajen, Tip IV kollajen", "Bazal membran erimesi ve anjiyogenez"],
                    ["Stromelisinler", "MMP-3, MMP-10", "Fibronektin, laminin, proteoglikan", "Geçici matriksin ve jellerin temizlenmesi"]
                ]
            ),
            make_cloze(
                "İnterstisyel kollajenazlar tarafından kesilen kollajen parçalarını ve bazal membran Tip IV kollajenini yıkan MMP grubu jelatinazlardır.",
                "jelatinazlardır",
                "MMP-2 ve MMP-9 enzimlerinin ait olduğu sınıf"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-15-s64",
        "title": "TIMP'ler: Doku Metalloproteinaz İnhibitörleri ve Denge",
        "content": "MMP'ler kontrolsüz kalırsa dokuyu tamamen sindirip yarayı devasa bir krater haline getirebilir; bu yıkımı frenleyen kalkan **TIMP'lerdir**:\n\n- **TIMP Tanımı (Sınav Spotu):** Mezenkimal hücreler ve makrofajlar tarafından salgılanan, aktif MMP enzimlerine 1:1 stokiometrik oranla bağlanarak onları tamamen inaktive eden **Doku Metalloproteinaz İnhibitörleridir (Tissue Inhibitors of Metalloproteinases)**.\n- **Kritik Biyolojik Denge:**\n  - **MMP > TIMP Durumu:** Aşırı matriks yıkımı gerçekleşir; yara kenarları erir, dikişler tutmaz ve **kronik iyileşmeyen ülserler veya yara dehisensi** gelişir.\n  - **TIMP > MMP Durumu:** Matriks yıkılamaz; sentezlenen kollajen birikir, birikir ve sonuçta **hipertrofik skar, keloid veya organ fibrozisi (siroz)** gelişir.\n- **TGF-β'nın Rolü:** Hatırlanacağı üzere TGF-β, TIMP sentezini artırıp MMP'yi baskılayarak dengeyi daima 'kollajen birikimi' tarafına büker.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "MMP Üstünlüğü (Aşırı Yıkım) vs TIMP Üstünlüğü (Aşırı Skar)",
                "MMP > TIMP (Yetersiz Skar / Doku Erimesi)",
                "Kollajen kontrolsüzce sindirilir; yara dudakları birleşemez, kronik dehisens ve ülserasyon kalır.",
                "TIMP > MMP (Aşırı Skar / Fibrozis)",
                "Yıkım durdurulur; aşırı kollajen birikerek sert keloid kitlelerine veya organ fibrozisine yol açar."
            ),
            make_quiz(
                "Matriks metalloproteinazların (MMP) doku yıkım aktivitesini spesifik olarak bağlayarak inhibe eden ve kontrolsüz yara erimesini engelleyen fizyolojik protein ailesi hangisidir?",
                [
                    {"key": "A", "text": "TIMP (Doku Metalloproteinaz İnhibitörleri)", "isCorrect": True, "explanation": "Doğru cevap A'dır: TIMP'ler MMP'leri inhibe ederek matriks sentez-yıkım dengesini sağlayan temel düzenleyicilerdir."},
                    {"key": "B", "text": "Antitrombin III", "isCorrect": False, "explanation": "Pıhtılaşma inhibitörüdür."},
                    {"key": "C", "text": "Alfa-1 antitripsin", "isCorrect": False, "explanation": "Nötrofil elastazını inhibe eder."},
                    {"key": "D", "text": "Kompleman Faktör H", "isCorrect": False, "explanation": "Kompleman inhibitörüdür."}
                ]
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-15-s65",
        "title": "Yara Gerilme Kuvveti (Tensile Strength) Dinamikleri",
        "content": "Bir cerrah dikişleri ne zaman almalıdır? Hasta ne zaman ağır kaldırabilir? Bu kararların tümü yara gerilme kuvvetinin zaman çizgisine dayanır (Sınavların Klasik Sorusu):\n\n- **1. Hafta (Dikişlerin Alındığı An - Kritik Eşik):**\n  - Cerrahi sütürler genellikle 7-10. günlerde alınır.\n  - Bu anda yaranın gerilme gücü normal sağlam derinin **yalnızca %10'u kadardır!**\n  - Yara henüz sadece gevşek granülasyon dokusu ve zayıf Tip III kollajenle tutunmaktadır; hastanın ani gerilme hareketlerinden kaçınması şarttır.\n- **4. Hafta (1. Ay):**\n  - Tip I kollajen sentezi ve çapraz bağlanma artar; gerilme gücü hızla yükselerek normalin **yaklaşık %50 - 60'ına** ulaşır.\n- **3. Ay (Plato Düzeyi - Altın Kural):**\n  - Remodeling doruğa çıkar; yara gücü normal dokunun **yaklaşık %70 ila %80'ine** ulaşır ve bu seviyede plato çizer.\n- **Unutulmaz Patoloji Kuralı:** İyileşen bir yara dokusu **ASLA normal sağlam dokunun %100 gücüne geri dönemez!** Maksimum güç %70-80 bandında kalır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Zaman", "Normal Güce Oranı", "Hakim Biyolojik Durum", "Klinik Uyarı"],
                [
                    ["1. Hafta", "%10", "Dikişler yeni alınmış, Tip III kollajen baskın", "En küçük travmada yara kolayca açılabilir"],
                    ["1. Ay", "%50 – %60", "Tip I kollajen geçişi ve kovalent çapraz bağlar", "Orta derece mekanik yüklere dirençli"],
                    ["3. Ay ve Sonrası", "%70 – %80 (Plato)", "Maksimum remodeling ve olgun fibröz skar", "Nihai güç sınırıdır; asla %100 olamaz"]
                ]
            ),
            make_quiz(
                "Temiz bir cerrahi keside dikişlerin alındığı birinci haftanın sonunda ve remodelingin tamamlandığı üçüncü ayın sonunda yara gerilme kuvveti (tensile strength) sağlam derinin yaklaşık yüzde kaçı kadardır?",
                [
                    {"key": "A", "text": "1. haftada %50, 3. ayda %100", "isCorrect": False, "explanation": "1. haftada %50 çok yüksektir ve hiçbir yara %100'e ulaşamaz."},
                    {"key": "B", "text": "1. haftada %10, 3. ayda %70-80", "isCorrect": True, "explanation": "Doğru cevap B'dir: 1. haftada dikişler alındığında güç ancak %10'dur; 3. ay sonunda maksimum %70-80 seviyesinde plato çizer."},
                    {"key": "C", "text": "1. haftada %1, 3. ayda %20", "isCorrect": False, "explanation": "Çok düşüktür."},
                    {"key": "D", "text": "Her iki dönemde de %100'dür", "isCorrect": False, "explanation": "Skar dokusu asla orijinal dokunun gücüne tam ulaşamaz."}
                ]
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-15-s66",
        "title": "Kollajen Çapraz Bağlanması ve Gerilme Gücünün Moleküler Temeli",
        "content": "Yara gücünün 1. haftadaki %10'dan 3. aydaki %80'e fırlamasını sağlayan şey sadece kollajen miktarı değil, kollajen liflerinin **fiziksel düzeni ve kovalent kenetlenmesidir**:\n\n- **Miktar Artışı vs Kalite Artışı:**\n  - Yara iyileşmesinde kollajen miktarı 2. ay civarında sabitlenir; ancak yaranın gerilme gücü artmaya devam eder!\n- **Bunun Sırrı İki Mekanizmadır (Sınav Spotu):**\n  1. **Çapraz Bağlanma (Cross-linking):** Bakır bağımlı **lizil oksidaz** enzimi sayesinde fibriller arasında kovalent bağlar kurulur; lifler birbirine kenetlenmiş çelik halatlara döner.\n  2. **Yönelim (Alignment):** Başlangıçta rastgele ve dağınık duran kollajen lifleri, dokunun maruz kaldığı mekanik gerilim vektörleri boyunca **birbirine paralel demetler** halinde dizilir.\n- **Sonuç:** Dağınık bir ip yumağı yerine, gerilime dirençli bir çelik kafes yapısı kurulur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Erken Dağınık Fibriller vs Olgun Çapraz Bağlı Kollajen Demeti",
                "2. Hafta (Dağınık Lifler)",
                "Kollajen lifleri rastgele saçılmıştır; aralarında kovalent çapraz bağlar azdır, kolay kopar.",
                "3. Ay (Paralel Çapraz Bağlı Demetler)",
                "Kollajen lifleri gerilim çizgilerine paralel hizalanmış ve lizil oksidazla kenetlenmiştir; yırtılmaya dirençlidir."
            ),
            make_recall(
                "Yara iyileşmesinin 2. ayından sonra toplam kollajen miktarı artmadığı halde yara gerilme kuvvetinin artmaya devam etmesinin nedeni nedir?",
                "Kollajen lifleri arasında lizil oksidaz aracılığıyla kurulan kovalent çapraz bağların artması ve liflerin gerilim çizgilerine paralel olarak yeniden dizilmesidir (remodeling)."
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-15-s67",
        "title": "Avaskülerleşme ve Skarın Soluklaşması Mekanizması",
        "content": "Granülasyon dokusunun ilk haftalardaki parlak kırmızı rengi aylar içinde nasıl olur da soluk beyaz bir çizgiye dönüşür?\n\n- **Oksijen İhtiyacının Bitmesi:** Granülasyon dokusunda fibroblastlar işlerini tamamlayıp kollajeni ördükten sonra dokunun metabolik aktivitesi hızla düşer.\n- **Endotel Apoptozu (Sınav Spotu):**\n  - Artık aşırı kan akımına ihtiyaç kalmadığı için VEGF sinyali kesilir.\n  - Yeni oluşmuş yüzlerce kılcal damarın endotel hücreleri programlı hücre ölümüne (apoptoz) girer.\n  - Kapiller lümenler çöker, perisitler dağılır ve damar yoğunluğu dramatik biçimde azalır.\n- **Fibroblastların Dinlenmeye Çekilmesi:** Aktif miyofibroblastlar da apoptoza uğrar veya inaktif yassı **fibrositlere** dönüşür.\n- **Makroskopik Sonuç:** Doku tamamen avasküler, asellüler, yoğun kollajenden ibaret **beyaz kalıcı skar (cicatrix)** halini alır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kırmızı Granülasyondan Beyaz Skara Dönüşüm Zinciri",
                [
                    "1. Kollajen Ağının Tamamlanması: Fibroblastlar yeterli Tip I kollajeni üretir.",
                    "2. VEGF Sinyalinin Kesilmesi: Hipoksi biter ve anjiyogenik uyarı durdurulur.",
                    "3. Endotel Apoptozu: Fazla kılcal damarlar apoptozla gerileyip lümenlerini kapatır.",
                    "4. Hücreselliğin Azalması: Miyofibroblastlar apoptoza gider veya durağan fibrosite döner.",
                    "5. Beyaz Skar Oluşumu: Doku avasküler, asellüler soluk fibröz bir hatta döner."
                ]
            ),
            make_cloze(
                "İyileşen bir yaranın kırmızı granülasyon dokusundan soluk beyaz bir skara dönüşmesi damarların apoptoz ile gerilemesi sonucu gerçekleşir.",
                "apoptoz",
                "Damarların programlı hücre ölümüyle yok olma süreci"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-15-s68",
        "title": "Kontraktürler: Miyofibroblastların Patolojik Aşırılığı",
        "content": "Yara kontraksiyonu defekti küçültmek için gereklidir; ancak sınır aşıldığında hayatı kabusa çeviren bir deformiteye dönüşür:\n\n- **Kontraktür Tanımı (Sınav Spotu):** Yara iyileşmesi sırasında miyofibroblastların aşırı ve kontrolsüz kasılması sonucu yara dokusunun ve çevresindeki eklemlerin **patolojik olarak büzüşmesi, sertleşmesi ve hareket kabiliyetini kaybetmesidir**.\n- **En Sık Görüldüğü Durumlar:**\n  - **Geniş Cilt Yanıkları:** Özellikle avuç içi, boyun, aksilla ve dirsek fleksura bölgelerinde derin 2. ve 3. derece yanıklardan sonra.\n  - **Palmar Fibromatozis (Dupuytren Kontraktürü):** Avuç içi aponevrozunun nodüler kalınlaşması ve parmakların bükülü kalması.\n- **Fonksiyonel Sakatlık:** Boyun yanığı olan bir hastanın çenesi göğsüne yapışabilir veya dirsek eklemi 90 derecede kilitlenip bir daha açılamayabilir.\n- **Tedavi:** Cerrahi skar eksizyonu, Z-plasti operasyonları ve deri greftlemeleridir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Fizyolojik Yara Kontraksiyonu vs Patolojik Kontraktür",
                "Fizyolojik Kontraksiyon (Faydalı)",
                "Açık yara alanını %70 oranında daraltarak epitelin üzerini kolayca kapatmasını sağlar.",
                "Patolojik Kontraktür (Deforme Edici)",
                "Aşırı büzüşmeyle eklemleri kilitler, uzuv hareketlerini engeller ve kalıcı sakatlık bırakır."
            ),
            make_quiz(
                "Geniş vücut yanıkları sonrasında özellikle eklem ve boyun bölgelerinde miyofibroblastların aşırı kasılması sonucu eklem hareketlerini kısıtlayan sert büzüşme deformitesine ne ad verilir?",
                [
                    {"key": "A", "text": "Keloid", "isCorrect": False, "explanation": "Keloid aşırı kollajen tümörüdür, eklem kontraksiyonu değildir."},
                    {"key": "B", "text": "Kontraktür", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kontraktürler, özellikle yanık skarlarında miyofibroblastların aşırı kasılmasıyla eklemleri kilitleyen patolojik büzülmelerdir."},
                    {"key": "C", "text": "Eksüberan granülasyon", "isCorrect": False, "explanation": "Bu yüzeyden taşan genç damar dokusudur."},
                    {"key": "D", "text": "Dehisens", "isCorrect": False, "explanation": "Dehisens yaranın açılmasıdır, büzülmesi değil."}
                ]
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-15-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] ECM Yeniden Şekillenmesi, MMP'ler ve Yara Gücü",
        "content": "Bu checkpointte yara iyileşmesinin remodeling evresini ve yara gücü dinamiklerini pekiştiriyoruz:\n\n- **Remodeling:** Tip III kollajenin Tip I kollajene dönüşmesi ve damarların gerilemesi.\n- **MMP'ler:** Çinko ($Zn^{2+}$) bağımlı enzimler. İnaktif pro-MMP olarak salınır, plazminle aktive olurlar.\n  - Kollajenazlar (MMP-1, 8): Tip I, II, III fibriler kollajeni keser.\n  - Jelatinazlar (MMP-2, 9): Denatüre kollajen ve Tip IV bazal membranı yıkar.\n  - Stromelisinler (MMP-3): Fibronektin ve proteoglikanları yıkar.\n- **TIMP'ler:** MMP doku inhibitörleridir; denge skar veya ülser yönünü belirler.\n- **Yara Gücü (Tensile Strength):**\n  - 1. hafta dikişler alındığında: Normal derinin **yalnızca %10'u**.\n  - 3. ay sonunda plato: Normal derinin **en fazla %70–80'i** (Asla %100 olamaz!).\n- **Kollajen Çapraz Bağları:** Bakır bağımlı lizil oksidaz ile kovalent kenetlenme.\n- **Kontraktür:** Miyofibroblastların aşırı kasılmasıyla eklemlerin büzüşüp kilitlenmesi (yanık komplikasyonu).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Parametre / Enzim", "Kofaktör / Eşik", "Temel Biyolojik Görev"],
                [
                    ["MMP Enzimleri", "Çinko ($Zn^{2+}$)", "Kollajen ve ECM'nin proteolitik yıkımı"],
                    ["Lizil Oksidaz", "Bakır ($Cu^{2+}$)", "Kollajen lifleri arasında kovalent çapraz bağlar"],
                    ["1. Hafta Yara Gücü", "%10", "Dikişler alındığında sahip olunan asgari güç"],
                    ["3. Ay Yara Gücü", "%70 – %80 (Maksimum)", "Remodelingin ulaştığı nihai plato gücü"]
                ]
            ),
            make_chain(
                "Remodeling ve Skar Olgunlaşma Akışı",
                [
                    "1. Pro-MMP Aktivasyonu: Plazmin çinko bağımlı kollajenazları aktive eder.",
                    "2. Tip III Kollajen Sindirimi: Gevşek erken lifler eritilir.",
                    "3. Tip I Kollajen Birikimi: Fibroblastlar kalın fibriler Tip I kollajen sentezler.",
                    "4. Çapraz Kenetlenme: Lizil oksidaz ile lifler çelik halat gibi birbirine bağlanır.",
                    "5. Damarların Çekilmesi: Endotel apoptozuyla kırmızı yara soluk beyaz skara döner."
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-15-s70",
        "title": "Mini Vaka: Çinko Eksikliği Olan Hastada İyileşmeyen Kronik Yara",
        "content": "Uzun süredir kronik alkolizm ve malnütrisyonu olan 45 yaşındaki bir hastaya fıtık onarımı yapılıyor:\n\n- **Ameliyat Sonrası 4. Hafta:** İnsizyon hattı hala kırmızı, ödemli, yer yer kabuklu kalıyor ve hiç gerilme gücü kazanamıyor. Yara kenarları en ufak dokunmada kolayca ayrılıyor.\n- **Laboratuvar İncelemesi:** Hastada şiddetli serum **Çinko ($Zn^{2+}$) eksikliği** saptanıyor.\n- **Patofizyolojik Mekanizma:**\n  - Çinko, Matriks Metalloproteinazların (MMP'lerin) çalışabilmesi için zorunlu kofaktördür.\n  - Çinko eksikliğinde eski matriks eritilip yeniden düzenlenemez (remodeling durur); epitel göçü ve fibroblast fonksiyonları bloke olur.\n- **Tedavi:** Hastaya oral çinko sülfat takviyesi ve protein desteği başlandıktan sonraki 2 hafta içinde yara hızla olgunlaşarak sağlam bir skar dokusuyla kapanıyor.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Çinko Eksikliği Olan Hastada Yara Bakımı",
                "Hastanın yarasının 1 aydır kaynamaması üzerine cerrahi polikliniğinde ne yapılması gerektiği tartışılıyor. En rasyonel patolojik ve metabolik yaklaşım hangisidir?",
                [
                    {
                        "text": "'Yarayı hemen tekrar kesip daha sıkı bağlayalım, beslenmeyle vakit kaybetmeyelim.'",
                        "outcome": "Hatalı yaklaşım: Çinko eksikliği sürdükçe yeni dikişler de tutmaz ve doku nekroza gider.",
                        "isCorrect": False
                    },
                    {
                        "text": "Hastadaki çinko ve beslenme eksikliğini derhal replase etmek, yara yatağını nemli ve temiz tutarak remodeling mekanizmasını moleküler düzeyde desteklemek",
                        "outcome": "Mükemmel klinik karar: MMP'ler ve epitel göçü aktive olur, yara hızla gücünü kazanır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Yarayı hastanın kendi haline bırakıp alkol almaya devam etmesini söylemek.'",
                        "outcome": "Tıbbi ihmal.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada çinko eksikliğinin yara iyileşmesini ve remodeling evresini doğrudan engellemesinin temel biyokimyasal nedeni nedir?",
                [
                    {"key": "A", "text": "Matriks metalloproteinazların (MMP) çalışabilmesi için çinkonun zorunlu kofaktör olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: MMP enzimlerinin katalitik bölgesinde çinko iyonu yer alır; çinko eksikliğinde ECM remodelingi gerçekleşemez."},
                    {"key": "B", "text": "Kanda trombositlerin tamamen yok olması", "isCorrect": False, "explanation": "Çinko eksikliği trombositopeni yapmaz."},
                    {"key": "C", "text": "Mide asidinin aşırı yükselmesi", "isCorrect": False, "explanation": "Konuyla ilgisi yoktur."},
                    {"key": "D", "text": "Tümör nekroz faktörünün sıfırlanması", "isCorrect": False, "explanation": "Temel mekanizma MMP disfonksiyonudur."}
                ]
            )
        ]
    })

    return slides
