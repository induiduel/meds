# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-15-s81",
        "title": "Yara İyileşmesini Etkileyen Faktörler: Giriş ve Ayrım",
        "content": "Doku onarımı mükemmel bir biyolojik orkestrasyondur; ancak hem organizmanın genel sağlık durumu (sistemik faktörler) hem de yara bölgesinin yerel koşulları (lokal faktörler) bu süreci raydan çıkarabilir:\n\n- **İki Temel Faktör Kategorisi (Sınav Spotu):**\n  1. **Sistemik Faktörler:** Hastanın beslenme düzeyi, metabolik hastalıkları (diyabet), dolaşım durumu ve kullandığı ilaçlar (özellikle glukokortikoidler).\n  2. **Lokal Faktörler:** Doğrudan yara yerindeki enfeksiyon, mekanik stres, yabancı cisim mevcudiyeti ve yaranın anatomik konumu/kanlanması.\n- **Klinik Gerçek:** En mükemmel cerrahi dikiş atılsa dahi, altta yatan kontrolsüz bir diyabet veya lokal bir enfeksiyon varsa yara açılmaya veya kronikleşmeye mahkumdur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Faktör Türü", "En Kritik Örnekler", "Patolojik Etki Mekanizması"],
                [
                    ["Sistemik: Metabolik", "Diabetes Mellitus", "Mikroanjiyopati, glikozilasyon, fagositoz felci"],
                    ["Sistemik: İlaç", "Glukokortikoidler (Kortizon)", "TGF-beta baskılanması, kollajen sentez inhibisyonu"],
                    ["Sistemik: Beslenme", "C Vitamini, Çinko, Protein", "Kollajen hidroksilasyonu ve MMP aksaması"],
                    ["Lokal: Biyolojik", "Enfeksiyon (En Önemli)", "Kalıcı doku yıkımı ve aşırı proteaz salınımı"],
                    ["Lokal: Mekanik", "Gerilim, erken hareket, öksürük", "Granülasyon dokusunun yırtılması (dehisens)"]
                ]
            ),
            make_cloze(
                "Yara iyileşmesini geciktiren en önemli lokal faktör yara enfeksiyonudur.",
                "enfeksiyonudur",
                "Yara yerindeki mikrobiyal kolonizasyon terimi"
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-15-s82",
        "title": "Sistemik Faktör 1: Diabetes Mellitus ve Dolaşım Bozuklukları",
        "content": "Klinikte yara iyileşmesini bozan en sık ve en tehlikeli sistemik hastalık Diabetes Mellitus'tur (Sınav Sorusu):\n\n- **Diyabetteki Çok Katmanlı Yara Kusuru:**\n  - **Mikroanjiyopati ve Hipoksi:** Diyabetik damar duvarlarında bazal membran kalınlaşır ve arteriyoloskleroz gelişir; yara dokusuna yeterli oksijen ve lökosit ulaşamaz.\n  - **Nötrofil Disfonksiyonu:** Yüksek kan şekeri nötrofillerin kemotaksisini, adezyonunu ve fagositoz yeteneğini bozar; yara enfeksiyonlara karşı savunmasız kalır.\n  - **İleri Glikozilasyon Ürünleri (AGEs):** Kollajen liflerini anormal çapraz bağlayarak esnekliği ve remodelingi felç eder.\n  - **Diyabetik Nöropati:** Ağrı duyusunun kaybı nedeniyle hasta travmaları fark etmez; kronik bası ülserleri (mal perforant) gelişir.\n- **Dolaşım Bozuklukları:** Ateroskleroz (arteriyel iskemi) veya kronik venöz yetmezlik (varis ülserleri), dokunun oksijenlenmesini bozarak iyileşmeyi engeller.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normoglisemik Sağlıklı İyileşme vs Diyabetik Yara Yatağı",
                "Sağlıklı Doku (Normal Kan Şekeri)",
                "Güçlü nötrofil cevabı, zengin oksijenlenme, hızlı granülasyon dokusu ve sağlam skar.",
                "Diyabetik Doku (Hiperglisemi)",
                "Bozuk lökosit fonksiyonu, doku hipoksisi, kronik süpürasyon ve kapanmayan diyabetik ayak ülseri."
            ),
            make_quiz(
                "Diabetes mellituslu hastalarda yara iyileşmesinin gecikmesine ve kronik ayak ülserlerinin gelişmesine yol açan temel patolojik mekanizmalar arasında hangisi YER ALMAZ?",
                [
                    {"key": "A", "text": "Lökositlerin kemotaksis ve fagositoz yeteneklerinin bozulması", "isCorrect": False, "explanation": "Hiperglisemi lökosit fonksiyonlarını doğrudan bozar."},
                    {"key": "B", "text": "Mikroanjiyopatiye bağlı doku iskemisi ve yetersiz oksijenlenme", "isCorrect": False, "explanation": "Damar hasarı dokuyu hipoksik bırakır."},
                    {"key": "C", "text": "Duyu nöropatisi nedeniyle tekrarlayan travmaların hissedilmemesi", "isCorrect": False, "explanation": "Nöropati bası ülserlerinin ana nedenidir."},
                    {"key": "D", "text": "Kollajen sentezinin 100 kat hızlanarak yarayı anında kapatması", "isCorrect": True, "explanation": "Doğru cevap D'dir: Diyabette kollajen sentezi hızlanmaz, aksine bozulur ve yara kapanamaz."}
                ]
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-15-s83",
        "title": "Sistemik Faktör 2: Glukokortikoidler (Kortizon) ve İmmünsüpresyon",
        "content": "Klinikte otoimmün hastalıklarda, astımda veya organ nakillerinde hayat kurtaran kortikosteroidler, doku onarımının en büyük düşmanıdır (Sınav Spotu):\n\n- **Glukokortikoidlerin Onarıma Darbesi:**\n  - **TGF-β'yı Baskılama:** Fibroblastların ana yakıtı olan TGF-β ve PDGF ekspresyonunu gen düzeyinde bloke ederler.\n  - **Kollajen Sentezini Durdurma:** Fibroblast proliferasyonunu ve pro-kollajen transkripsiyonunu doğrudan inhibe ederler.\n  - **Anjiyogenezi Felç Etme:** Endotel hücrelerinin tomurcuklanmasını durdururlar; yara tabanında granülasyon dokusu gelişemez.\n  - **Enflamasyonu Aşırı Söndürme:** Monosit ve makrofaj göçünü keserek yaranın debridmanını ve sitokin desteğini yok ederler.\n- **Klinik Sonuç:** Uzun süreli kortizon kullanan (Cushingoid) hastalarda cerrahi yaraların gerilme gücü son derece zayıftır; dikişler kolayca patlar (dehisens) ve enfeksiyon riski çok yüksektir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal İyileşen Doku vs Glukokortikoid (Kortizon) Altındaki Doku",
                "Normal Doku (Fizyolojik Onarım)",
                "Zengin granülasyon dokusu, aktif kollajen sentezi ve sağlam yara gerilme gücü.",
                "Kortizon Alan Doku (Baskılanmış Onarım)",
                "Avasküler, soluk, granülasyonsuz yara yatağı, yetersiz kollajen ve patlamaya hazır dikişler."
            ),
            make_cloze(
                "Kortikosteroid ilaçlar TGF-beta salınımını ve kollajen sentezini baskılayarak yara skarının mekanik gücünü zayıflatır.",
                "kollajen",
                "Kortizonun sentezini engellediği temel lif proteini"
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-15-s84",
        "title": "Lokal Faktörler: Enfeksiyon, Yabancı Cisim ve Mekanik Güçler",
        "content": "Sistemik durum ne kadar mükemmel olursa olsun, yara bölgesindeki lokal engeller iyileşmeyi durdurabilir:\n\n- **1. Enfeksiyon (En Önemli Lokal Neden - Sınav Spotu):**\n  - Patojen mikroorganizmalar devam eden bir nötrofil akınına yol açar.\n  - Salınan proteazlar ve elastazlar yeni sentezlenen matriksi hızla eritir; yara granülasyon dokusu oluşturamaz ve doku nekroza gider.\n- **2. Yabancı Cisimler:**\n  - Yara içinde unutulan dikiş iplikleri, cam kırıkları, metal parçaları veya kıymıklar.\n  - Sürekli bir kronik yangı ve yabancı cisim granülomu odağı oluşturarak re-epitelizasyonu engeller.\n- **3. Mekanik Faktörler:**\n  - Ameliyat sonrası erken ayağa kalkma, aşırı gerilme veya şiddetli öksürük karın içi basıncını artırarak taze granülasyon dokusunu yırtar.\n- **4. Anatomik Konum ve Vaskülarizasyon:**\n  - Kanlanması mükemmel olan yüz yaraları 3-5 günde hızla iyileşirken; kan akımı zayıf olan ayak ve bacak yaraları çok daha geç kapanır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Lokal Faktör", "Klinik Örnek", "Yaraya Etkisi"],
                [
                    ["Enfeksiyon", "Stafilokok cerrahi alan enfeksiyonu", "Sürekli nekroz, kollajen erimesi ve püy"],
                    ["Yabancı Cisim", "Cilt altında kalan dikiş düğümü", "Yabancı cisim reaksiyonu ve kronik fistül"],
                    ["Mekanik Basınç", "KOAH hastasında ameliyat sonrası öksürük", "Karın fasyasının yırtılması ve fıtıklaşma"],
                    ["Vaskülarizasyon", "Yüz kesisine karşı pretibial kesi", "Yüzde hızlı skarsız; bacakta yavaş iyileşme"]
                ]
            ),
            make_recall(
                "Yara iyileşmesini geciktiren lokal faktörler içinde klinikte en sık karşılaşılan tek ve en önemli neden nedir?",
                "Yara yeri enfeksiyonudur (bakteriyel kolonizasyon ve persistan nötrofilik doku erimesi)."
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-15-s85",
        "title": "Anormal İyileşme Formu 1: Yara Dehisensi ve Ülserasyon",
        "content": "Yara iyileşmesindeki aksaklıklar iki zıt uçta patoloji üretir: Yetersiz onarım veya aşırı onarım:\n\n- **1. Yara Dehisensi (Wound Dehiscence / Yaranın Açılması - Sınav Spotu):**\n  - Cerrahi olarak dikilmiş bir yaranın dikiş hatlarından mekanik olarak ayrılması ve açılmasıdır.\n  - **En Sık Yerleşim:** Karın ön duvarı laparotomi kesileri (abdominal dehisens).\n  - **Risk Faktörleri:** Şiddetli öksürük (karın içi basınç artışı), kusma, paralitik ileus, yetersiz beslenme (hipoalbüminemi), enfeksiyon ve obezite.\n  - **Korkulan Komplikasyon: Evisserasyon:** Karın fasyasının açılıp bağırsakların dışarı fırlaması durumudur; acil cerrahi müdahale gerektirir.\n- **2. Ülserasyon (İyileşmeyen Kronik Yara):**\n  - Yetersiz damarlanma (arteriyel iskemi), nöropati veya sürekli bası nedeniyle epitelizasyonun tamamlanamaması ve doku kaybının sürmesidir (Örnek: Dekübitus ve diyabetik ayak ülseri).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sağlam İnsizyon Hattı vs Yara Dehisensi (Açılma)",
                "Sağlam İnsizyon Hattı",
                "Fasya ve cilt kollajenle birbirine kaynamıştır; öksürme ve gerilmeye karşı dirençlidir.",
                "Yara Dehisensi (Açılmış Yara)",
                "Kollajen köprüleri kurulamamıştır; öksürükle dikişler dokuyu yırtarak açılır ve organlar dışarı sarkar."
            ),
            make_quiz(
                "Abdominal cerrahi sonrası öksürük, kusma ve enfeksiyon gibi mekanik ve biyolojik stresler sonucunda dikiş hattının ayrılarak yaranın açılması durumuna ne ad verilir?",
                [
                    {"key": "A", "text": "Keloid", "isCorrect": False, "explanation": "Keloid aşırı kollajen kabarmasıdır."},
                    {"key": "B", "text": "Yara dehisensi (Dehiscence)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Yara dehisensi dikilmiş cerrahi yaranın açılmasıdır."},
                    {"key": "C", "text": "Kontraktür", "isCorrect": False, "explanation": "Kontraktür aşırı büzüşmedir."},
                    {"key": "D", "text": "Metaplazi", "isCorrect": False, "explanation": "Metaplazi hücre tipinin değişmesidir."}
                ]
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-15-s86",
        "title": "Anormal İyileşme Formu 2: Aşırı Skar Oluşumu (Hipertrofik Skar)",
        "content": "Onarım mekanizması 'dur' sinyalini zamanında alamazsa, aşırı kollajen birikimiyle anormal skarlar gelişir:\n\n- **Hipertrofik Skar Nedir? (Sınav Spotu):**\n  - Yara iyileşmesi sırasında aşırı miktarda granülasyon dokusu ve kollajen sentezlenmesi sonucu deriden kabarık, sert, kırmızımsı bir yara izi oluşmasıdır.\n  - **En Temel Ayırt Edici Özelliği (Sınavın Altın Kuralı):** Skar dokusu **ORİJİNAL YARA SINIRLARI İÇİNDE KALIR!** Kesinin veya yaranın dışına taşmaz.\n- **Kollajen Yapısı:** Ağırlıklı olarak **Tip III kollajen** içerir; lifler yüzeye paralel gevşek demetler halindedir.\n- **Klinik Seyir:**\n  - Genellikle derin termal yanıklardan veya cerrahi kesilerden sonraki 1-3 ay içinde gelişir.\n  - **Aylar veya yıllar içinde kendiliğinden gerileme (regresyon / küçülme) eğilimindedir!**",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Hipertrofik Skar", "Keloid"],
                [
                    ["Sınır Yayılımı", "Orijinal yara sınırları İÇİNDE kalır", "Yara sınırlarının DIŞINA taşar (invaziv)"],
                    ["Kollajen Tipi", "Baskın olarak Tip III kollajen", "Kalın, amorf Tip I kollajen demetleri"],
                    ["Kendiliğinden Gerileme", "Aylar içinde geriler (regrese olur)", "Kendiliğinden ASLA gerilemez (ilerler)"],
                    ["Cerrahi Eksizyon Sonucu", "Genellikle nüks etmez", "Çıkarılırsa daha büyük nüks eder"],
                    ["Genetik / Irk Eğilimi", "Belirgin ırk eğilimi yok (yanık ilişkili)", "Siyah ırk ve Asyalılar (genetik yatkınlık)"]
                ]
            ),
            make_cloze(
                "Aşırı kollajen birikimiyle oluşan ancak orijinal yara sınırları içinde kalan kabarık lezyona hipertrofik skar denir.",
                "hipertrofik",
                "Yara sınırını aşmayan aşırı skar türü adı"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-15-s87",
        "title": "Anormal İyileşme Formu 3: Keloid (Kanser Benzeri Skar)",
        "content": "Skar dokusunun en tehlikeli ve tedavisi en güç aşırı büyüme formu **Keloiddir**:\n\n- **Keloid Tanımı (Sınav Spotu):**\n  - Yara iyileşmesindeki denetim mekanizmalarının tamamen çökmesi sonucu, oluşan skar dokusunun **orijinal yara sınırlarını fersah fersah aşarak çevre sağlam deriye doğru bir yengeç kıskacı gibi büyümesidir**.\n- **Etiyoloji ve Genetik Yatkınlık:**\n  - Siyah ırkta ve Asyalı bireylerde beyaz ırka göre 15-20 kat daha sıktır.\n  - En sık yerleşim: Kulak memesi (kulak deldirme sonrası), omuz (deltoid bölgesi), sternum üzeri ve üst sırt.\n- **Histopatoloji:**\n  - Mikroskopta devasa, asellüler, camsı (hiyalinize), parlak pembe boyanan **kalın Tip I kollajen demetleri (keloidal kollajen)** izlenir.\n- **Klinik Kabus:**\n  - **Kendiliğinden ASLA gerilemez!**\n  - Bir cerrah keloidi kesip çıkarırsa, yeni cerrahi travma fibroblastları daha da çılgına çevirir ve lezyon **çok daha büyük olarak nüks eder!** Tedavide intralezyonel steroid enjeksiyonları ve silikon bası örtüleri tercih edilir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Hipertrofik Skar vs Keloid Davranışı",
                "Hipertrofik Skar (Sınırlı ve Uysal)",
                "Yara çizgisinde kabarır, sınırları aşmaz ve zamanla kendiliğinden solup küçülür.",
                "Keloid (Sınır Tanımaz ve Agresif)",
                "Sağlam deriye taşar, tümör gibi büyür, asla küçülmez ve ameliyat edilirse katlanarak nüks eder."
            ),
            make_quiz(
                "Kulak deldirme işleminden aylar sonra oluşan, orijinal yara sınırlarının belirgin şekilde dışına taşan, histolojisinde kalın hiyalinize Tip I kollajen demetleri içeren ve kendiliğinden gerilemeyen lezyon hangisidir?",
                [
                    {"key": "A", "text": "Hipertrofik skar", "isCorrect": False, "explanation": "Hipertrofik skar yara sınırları içinde kalır ve zamanla geriler."},
                    {"key": "B", "text": "Keloid", "isCorrect": True, "explanation": "Doğru cevap B'dir: Keloid orijinal yara sınırlarını aşan, kendiliğinden gerilemeyen ve nüks eğilimi çok yüksek aşırı skar dokusudur."},
                    {"key": "C", "text": "Granülasyon dokusu", "isCorrect": False, "explanation": "Granülasyon dokusu genç pembe onarım dokusudur."},
                    {"key": "D", "text": "Eksüberan granülasyon", "isCorrect": False, "explanation": "Eksüberan granülasyonda zengin damar vardır; keloid kalın kollajendir."}
                ]
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-15-s88",
        "title": "Desmoid Tümörler (Fibromatozis): Skar ile Neoplazi Sınırı",
        "content": "Onarım ile tümör biyolojisinin birbirine karıştığı en ilginç antite **Desmoid Tümörlerdir (Agresif Fibromatozis)**:\n\n- **Tanımı ve Doğası (Sınav Spotu):**\n  - Karın ön duvarında (rektus kası fasyasında) veya ekstremitelerde, sıklıkla **geçirilmiş cerrahi ameliyat veya gebelik travması alanında** gelişen lokal agresif fibroblastik proliferasyonlardır.\n  - Gerçek anlamda metastaz yapmazlar (benign/orta dereceli kabul edilirler).\n  - Ancak çevre kas ve yağ dokusunu bir kanser gibi parmak benzeri uzantılarla **infiltre ederler (lokal invazyon)** ve cerrahi sonrası nüks oranları çok yüksektir.\n- **Moleküler Mekanizma:**\n  - Vakaların büyük çoğunluğunda **Wnt / beta-katenin (CTNNB1)** yolağında mutasyon vardır.\n  - Sitoplazmada biriken beta-katenin çekirdeğe girerek fibroblastları sürekli çoğalma modunda kilitler.\n  - Ailesel Adenomatöz Polipozis (FAP) / Gardner sendromu hastalarında sık görülür.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Aşırı Fibröz Lezyon", "Biyolojik Doğası", "Sınır Özelliği", "Metastaz Riski"],
                [
                    ["Hipertrofik Skar", "Non-neoplastik reaktif", "Yara sınırları içinde", "Yok (kendiliğinden geriler)"],
                    ["Keloid", "Non-neoplastik aşırı", "Yara sınırları dışına taşar", "Yok (lokal ilerler)"],
                    ["Desmoid Tümör", "Monoklonal neoplazi (CTNNB1)", "Lokal infiltratif ve agresif", "Yok (fakat lokal nüks yüksek)"],
                    ["Fibrosarkom", "Malign mezenkimal kanser", "Destrüktif ve invaziv", "Yüksek (akciğer metastazı)"]
                ]
            ),
            make_cloze(
                "Cerrahi skar zemininde gelişebilen, metastaz yapmayan ancak lokal infiltratif büyüyen fibroblastik lezyona desmoid tümör denir.",
                "desmoid",
                "Agresif fibromatozisin diğer adı"
            )
        ]
    })

    # Slide 89 - CHECKPOINT 9
    slides.append({
        "id": "k1-15-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Yara İyileşmesini Etkileyen Faktörler ve Anormal İyileşme",
        "content": "Bu checkpointte yara iyileşmesini bozan faktörleri ve anormal skar tiplerini pekiştiriyoruz:\n\n- **En Sık Sistemik Neden:** Diabetes Mellitus (mikroanjiyopati, fagositoz felci, AGEs).\n- **En Önemli Lokal Neden:** Enfeksiyon (bakteriler persistan nötrofil akını ve doku erimesi yapar).\n- **Glukokortikoidler (Kortizon):** TGF-β'yı ve kollajen sentezini baskılar; granülasyonu ve yara gücünü felç eder.\n- **Beslenme:** C vitamini (hidroksilasyon), Çinko (MMP katalizi) ve Protein eksiklikleri iyileşmeyi durdurur.\n- **Yara Dehisensi:** Dikişlerin açılması; karında öksürük ve basınçla bağırsakların sarkması (evisserasyon).\n- **Hipertrofik Skar vs Keloid:**\n  - **Hipertrofik Skar:** Sınırları aşmaz, Tip III kollajen baskın, yanıklarda sık, aylar içinde kendiliğinden geriler.\n  - **Keloid:** Orijinal yara sınırlarını fersah fersah aşar, kalın Tip I kollajen demetleri içerir, Afrika ırkında sık, asla gerilemez, kesilirse katlanarak nüks eder.\n- **Desmoid Tümör:** Beta-katenin mutasyonu ile giden lokal agresif fibroblastik neoplazi.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Karşılaştırma Ölçütü", "Hipertrofik Skar", "Keloid"],
                [
                    ["Yara Sınırı İlişkisi", "Yara sınırları İÇİNDE kalır", "Yara sınırlarının DIŞINA taşar"],
                    ["Kendiliğinden Regresyon", "Genellikle var (zamanla solar)", "Kesinlikle YOK (ömür boyu sürer)"],
                    ["Hakim Kollajen", "Tip III kollajen", "Kalın asellüler Tip I kollajen demetleri"],
                    ["Cerrahi Eksizyon", "İyileşebilir", "Yüksek oranda daha büyük nüks eder"]
                ]
            ),
            make_chain(
                "Anormal İyileşme Spektrumu (Yetersizden Aşırıya)",
                [
                    "1. Yetersiz Onarım (Dehisens / Ülser): Yetersiz damarlanma ve kollajen erimesiyle yara açılır.",
                    "2. Eksüberan Granülasyon: Genç damar dokusu yüzeyden taşarak epitel göçünü tıkar.",
                    "3. Hipertrofik Skar: Fazla kollajen birikir ancak yara sınırları içinde hapis kalır.",
                    "4. Keloid: Kontrolsüz kollajen fırtınası sağlam deriye yayılır ve gerilemez.",
                    "5. Desmoid Tümör: Beta-katenin mutasyonuyla klonal lokal agresif neoplazi gelişir."
                ]
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-15-s90",
        "title": "Mini Vaka: Kulak Memesinde Keloid vs Sezaryen Skarında Hipertrofik Skar",
        "content": "Dermatoloji polikliniğine aynı gün iki farklı yara komplikasyonu başvuruyor:\n\n- **Hasta 1 (22 Yaşında Kadın - Kulak Memesi):**\n  - 6 ay önce kulak memesini deldirdikten sonra delik çevresinde başlayan sert kitle, deliğin çok ötesine geçerek tüm kulak memesini kaplayan 3 cm çapında devasa, lobüle, parlak pembe bir yumruya dönüşmüş.\n  - Biyopside: Kalın, hiyalinize, asellüler Tip I kollajen bantları izleniyor. **Tanı: Keloid**.\n- **Hasta 2 (30 Yaşında Kadın - Sezaryen Kesisı):**\n  - 4 ay önceki sezaryen dikiş hattında kabarık, kırmızı, kaşıntılı sert bir çizgi gelişmiş; ancak bu kabarıklık cerrahi insizyon sınırlarının kesinlikle dışına taşmamış.\n  - Biyopside: İnce Tip III kollajen demetleri izleniyor. **Tanı: Hipertrofik Skar**.\n- **Tedavi Farkı:** Hasta 2'ye zamanla gerileyeceği söylenip silikon jel verilirken; Hasta 1'e cerrahi eksizyondan kesinlikle kaçınılarak intralezyonel triamsinolon (kortizon) enjeksiyonu uygulanıyor.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Kulak Memesindeki Keloid Lezyonuna Cerrahi Yaklaşım",
                "Hasta 1'in kulak memesindeki devasa keloid kitlesini gören genel cerrahi asistanı 'Hemen lokal anesteziyle bu kitleyi neşterle kesip çıkaralım, kulak temizlensin' diyor. Dermatoloji ve patoloji uzmanı olarak tavrınız ne olmalıdır?",
                [
                    {
                        "text": "'Haklısın, hemen neşterle kesip atalım, başka tedaviye gerek yoktur.'",
                        "outcome": "Büyük klinik felaket: Cerrahi kesi yeni bir travma yaratır ve 6 ay sonra keloid iki katı büyüklükte nüks eder.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Kesinlikle cerrahi eksizyon tek başına yapılmamalıdır! Keloid cerrahi travmayla daha da azar ve nüks eder. Öncelikle intralezyonel kortikosteroid enjeksiyonu ve bası tedavisi uygulanmalı; cerrahi ancak adjuvan radyoterapi/steroid eşliğinde son çare düşünülmelidir.'",
                        "outcome": "Kusursuz klinik karar: Keloidin biyolojik doğasına uygun, nüksü önleyen doğru tedavi seçilir.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Kulak memesini komple ampute edelim.'",
                        "outcome": "Gereksiz aşırı mutilasyon.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu iki vaka karşılaştırıldığında Hasta 1'e 'Keloid', Hasta 2'ye 'Hipertrofik Skar' tanısı konulmasını sağlayan en temel klinik kriter nedir?",
                [
                    {"key": "A", "text": "Lezyonun orijinal yara sınırlarının dışına taşıp taşmaması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hipertrofik skar orijinal yara sınırları içinde kalırken; keloid yara sınırlarını aşarak çevre sağlam dokuya yayılır."},
                    {"key": "B", "text": "Hastaların vücut kitle indeksleri", "isCorrect": False, "explanation": "Obezite bu ayrımı belirlemez."},
                    {"key": "C", "text": "Lezyonun renginin mavi olması", "isCorrect": False, "explanation": "Keloid veya hipertrofik skar mavi olmaz."},
                    {"key": "D", "text": "Hastanın kan grubunun Rh pozitif olması", "isCorrect": False, "explanation": "Kan grubuyla ilgisi yoktur."}
                ]
            )
        ]
    })

    return slides
