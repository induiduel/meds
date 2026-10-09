# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-19-s31",
        "title": "İki Kanal Sistemi: Mezonefrik (Wolff) ve Paramezonefrik (Müller) Taslakları",
        "content": "Embriyonik gelişimin 6. haftasında indiferan bir fetusta yan yana uzanan iki çift genital kanal sistemi bulunur (Sınav Spotu):\n\n- **Mezonefrik (Wolff) Kanalları:**\n  - İlkel böbrek taslağı olan mezonefrozun boşaltım kanallarıdır.\n  - Erkek iç üreme yollarının öncülüdür.\n  - Gelişimi ve korunması doğrudan Leydig hücrelerinden salgılanan yüksek konsantrasyondaki **lokal testosterona** bağımlıdır; testosteron yoksa dejenere olarak apoptozise uğrar.\n- **Paramezonefrik (Müller) Kanalları:**\n  - Mezonefrik kanalın lateralinde sölomik epitelin invaginasyonu ile oluşur.\n  - Dişi iç üreme organlarının (fallop tüpleri, uterus, serviks ve üst 1/3 vajina) öncülüdür.\n  - Müller kanallarının gelişimi hiçbir hormonal uyarım gerektirmez (varsayılan yoldur); erkekte ise Sertoli hücrelerinden salgılanan **AMH tarafından aktif olarak geriletilir**.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Wolff Kanalı (Erkek) vs Müller Kanalı (Dişi)",
                "Wolff Kanalı (Mezonefrik)",
                "Leydig kaynaklı yüksek lokal testosterona bağımlıdır; epididim, vas deferens ve seminal veziküle dönüşür.",
                "Müller Kanalı (Paramezonefrik)",
                "Hormonsuz kendiliğinden gelişir; Sertoli kaynaklı AMH tarafından erkekte aktif olarak baskılanır."
            ),
            make_cloze(
                "Mezonefrik kanalların erkek iç genital organlarına farklılaşabilmesi için testis Leydig hücrelerinden salgılanan testosteron hormonunun lokal etkisi zorunludur.",
                "testosteron",
                "Wolff kanallarının korunmasını ve gelişimini sağlayan primer androjen hormon"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-19-s32",
        "title": "Sertoli Hücreleri ve AMH (MİF): Müller Kanallarının Gerilemesi",
        "content": "Testiste farklılaşan ilk hücre tipi Sertoli hücresidir ve salgıladığı en kritik protein **AMH** (Anti-Müllerian Hormon / Müller İnhibe Edici Madde - MIS/MİF) dir (Sınav Spotu):\n\n- **Biyokimyasal Yapı:** TGF-β süper ailesine ait bir glikoprotein dimeridir.\n- **Zamanlama ve Reseptör:** 7. haftada Sertoli hücrelerinden salgılanmaya başlar; Müller kanallarının mezenkimindeki tip 2 serin/treonin kinaz reseptörü olan **AMHR2** reseptörüne bağlanır.\n- **Mekanizma:** AMHR2 aktivasyonu, kanal epiteli ve çevre mezenkiminde apoptozisi tetikler; 8 ila 10. haftalar arasında Müller kanalları kranyal uçtan kaudale doğru tamamen geriler ve yok olur.\n- **Kalıntılar:** Erkekte gerileyen Müller kanalından geriye yalnızca kranyal uçta **apendiks testis** ve üretrada **utrikulus prostatikus** kalır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "AMH Aracılı Müller Regresyon Mekanizması",
                [
                    "1. Sertoli Sentezi: SOX9 ve SF1 uyarısıyla Sertoli hücrelerinde AMH salgılanır.",
                    "2. Parakrin Difüzyon: AMH proteini bitişik paramezonefrik kanal mezenkimine ulaşır.",
                    "3. Reseptör Bağlanması: Mezenkimal AMHR2 reseptörlerine bağlanarak Smad yolağını açar.",
                    "4. Mezenkimal Apoptoz: Çevre mezenkimal hücreler kanal epitelyumunun ölümünü tetikler.",
                    "5. Tam Regresyon: Müller kanalı erir; geriye yalnızca apendiks testis ve utrikulus kalır."
                ]
            ),
            make_quiz(
                "Fetal yaşamın 8-10. haftalarında testis Sertoli hücrelerinden salgılanarak Müller kanallarının apoptozisle gerilemesini sağlayan hormon hangisidir?",
                [
                    {"key": "A", "text": "AMH (Anti-Müllerian Hormon)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sertoli hücrelerinden üretilen AMH (MİF), Müller kanallarının erimesini ve yok olmasını sağlayan temel faktördür."},
                    {"key": "B", "text": "Dihidrotestosteron (DHT)", "isCorrect": False, "explanation": "DHT dış genitalyanın maskülinizasyonundan sorumludur."},
                    {"key": "C", "text": "İnsülin benzeri peptid 3 (INSL3)", "isCorrect": False, "explanation": "INSL3 testisin skrotuma inişinde rol oynar."},
                    {"key": "D", "text": "Östradiol", "isCorrect": False, "explanation": "Östradiol Müller gerilemesi yapmaz."}
                ]
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-19-s33",
        "title": "Persistan Müller Kanalı Sendromu (PMDS): AMH ve AMHR2 Mutasyonları",
        "content": "Erkek fetusta Müller kanalının gerileyememesi çok ilginç ve özel bir klinik tabloya yol açar (Sınav Spotu):\n\n- **Klinik Tanım:** Persistan Müller Kanalı Sendromu (PMDS), normal 46,XY karyotipli, normal erkek dış genitalyasına sahip bir erkekte **uterus ve fallop tüplerinin bulunmasıdır**.\n- **Etiyoloji ve Genetik:**\n  - Vakaların yaklaşık %45'inde **AMH gen mutasyonu** (Tip 1 PMDS).\n  - Yaklaşık %40'ında **AMHR2 reseptör gen mutasyonu** (Tip 2 PMDS) saptanır; otozomal resesif kalıtılır.\n- **Klinik Başvuru:** Dış genitalya tamamen normal erkek olduğu için çocuklukta fark edilmez. Genellikle fıtık onarımı sırasında skrotumda/kanal içinde uterus bulunması (hernia uteri inguinalis) veya kriptorşidizm araştırması sırasında rastlantısal olarak saptanır.\n- **Fertilite:** Testisler sıklıkla fallop tüplerine yapışık kalır; sperm yolları tıkanabileceğinden infertilite sık görülür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["PMDS Tipi", "Kusurlu Gen / Mekanizma", "Kalıtım", "Klinik Özellik"],
                [
                    ["Tip 1 PMDS", "AMH gen mutasyonu (Sertoli hormon üretemez)", "Otozomal Resesif", "46,XY erkek, normal penis/skrotum, inguinal kanalda uterus"],
                    ["Tip 2 PMDS", "AMHR2 reseptör mutasyonu (Müller kanalı yanıtsız)", "Otozomal Resesif", "Serum AMH normal/yüksek, herni kesesinde uterus ve tüp"]
                ]
            ),
            make_cloze(
                "Normal erkek dış genitalyasına sahip 46,XY bir bireyde fıtık kesesi içinde uterus ve fallop tüplerinin saptanması durumuna persistan Müller kanalı sendromu adı verilir.",
                "persistan Müller kanalı sendromu",
                "AMH veya AMHR2 gen mutasyonuna bağlı uterus kalıntısı tablosu"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-19-s34",
        "title": "Leydig Hücreleri ve Testosteron: Wolff Kanalından Erkek İç Organları",
        "content": "Testiste Sertoli hücrelerinin hemen ardından mezenkimden Leydig hücreleri farklılaşır ve steroid sentezi başlar (Sınav Spotu):\n\n- **hCG ve LH Uyarımı:** Erken dönemde plasental hCG, ilerleyen haftalarda fetal hipofiz kaynaklı LH uyarısıyla Leydig hücrelerinden yoğun şekilde **testosteron** salgılanır.\n- **Lokal Parakrin Etki:** Testosteron dolaşıma geçmeden önce doğrudan temas ettiği aynı taraftaki (ipsilateral) Wolff kanalını uyarır.\n- **Wolff Türevleri:** Testosteron etkisiyle mezonefrik kanal şu organlara dönüşür:\n  1. **Epididim** (baş, gövde, kuyruk),\n  2. **Duktus deferens (vas deferens)**,\n  3. **Seminal vezikül**,\n  4. **Duktus ejakulyatorius**.\n- **Kritik Kural:** Testosteron ipsilateral (aynı taraf) çalışır; bir tarafta testis çıkarılırsa sadece o taraftaki Wolff kanalı erir, diğer taraftaki gelişir (Alfred Jost deneyleri).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Genital Kanal", "Geliştirdiği Erkek Organları", "Gelişimi Sağlayan Faktör"],
                [
                    ["Mezonefrik (Wolff) Üst Kısım", "Duktuli efferentes ve Epididim", "Testis kaynaklı yüksek lokal Testosteron"],
                    ["Mezonefrik (Wolff) Orta Kısım", "Duktus (vas) deferens", "Testis kaynaklı yüksek lokal Testosteron"],
                    ["Mezonefrik (Wolff) Alt Kısım", "Seminal vezikül ve Ejakülatör kanal", "Testis kaynaklı yüksek lokal Testosteron"]
                ]
            ),
            make_quiz(
                "İnsan embriyosunda mezonefrik (Wolff) kanalının epididim, vas deferens ve seminal veziküle farklılaşmasını sağlayan birincil lokal endokrin faktör hangisidir?",
                [
                    {"key": "A", "text": "Leydig hücrelerinden salgılanan testosteron", "isCorrect": True, "explanation": "Doğru cevap A'dır: Wolff kanalının erkek iç genital yollarına gelişimi Leydig kaynaklı yüksek lokal testosteron konsantrasyonuna bağımlıdır."},
                    {"key": "B", "text": "Sertoli hücrelerinden salgılanan AMH", "isCorrect": False, "explanation": "AMH Müller kanalını geriletir, Wolff'u uyarmaz."},
                    {"key": "C", "text": "Periferik dokularda üretilen DHT", "isCorrect": False, "explanation": "DHT iç kanalları değil, dış genitalyayı ve prostatı geliştirir."},
                    {"key": "D", "text": "Plasental östrojen", "isCorrect": False, "explanation": "Östrojen Wolff kanalını geliştirmez."}
                ]
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-19-s35",
        "title": "5-Alfa Redüktaz ve DHT: Dış Genitalya Maskülinizasyonunun Güçlü Hormonu",
        "content": "Testosteron iç genital kanalları geliştirirken, dış genital organ taslakları testosterona doğrudan güçlü yanıt veremez (Sınav Spotu):\n\n- **Enzimatik Dönüşüm:** Hedef dış genital dokularda (genital tüberkül, labioskrotal kabartı) bulunan **5α-redüktaz tip 2 (SRD5A2)** enzimi, testosteronun A halkasını indirgeyerek çok daha güçlü bir androjen olan **Dihidrotestosteron (DHT)** molekülüne dönüştürür.\n- **Reseptör Afinitesi:** DHT, androjen reseptörüne (AR) testosterondan yaklaşık **5-10 kat daha yüksek afinite ile bağlanır** ve reseptör-DNA kompleksini çok daha stabil tutar.\n- **DHT'nin Görevleri:**\n  1. Genital tüberkülün uzayarak **penis glans ve korpusuna** dönüşmesi,\n  2. Ürogenital kıvrımların orta hatta kaynaşarak **penil üretrayı ve korpus spongiyozumu** kapatması,\n  3. Labioskrotal kabartıların kaynaşarak **skrotum kesesini** oluşturması,\n  4. Prostat bezinin ve bulbouretral bezlerin tomurcuklanması.\n- **Sonuç:** DHT yoksa veya reseptör algılayamazsa dış genitalya otomatik olarak dişi yönünde gelişir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Dış Genitalya Maskülinizasyon Kaskadı",
                [
                    "1. Steroid Salgısı: Leydig hücreleri dolaşıma testosteron verir.",
                    "2. Enzimatik Aktivasyon: Hedef dokudaki 5α-redüktaz enzimi testosteronu DHT'ye çevirir.",
                    "3. Yüksek Afinite Bağlanma: DHT androjen reseptörüne (AR) sıkıca kenetlenir.",
                    "4. Katlantı Kaynaşması: Ürogenital kıvrımlar penil üretrayı kapatmak üzere birleşir.",
                    "5. Skrotal Füzyon: Labioskrotal kabartılar orta hatta kaynaşarak skrotumu tamamlar."
                ]
            ),
            make_cloze(
                "Erkek fetusta genital tüberkülün penise, labioskrotal kabartıların skrotuma dönüşebilmesi için testosteronun 5α-redüktaz enzimi ile dihidrotestosteron molekülüne dönüştürülmesi şarttır.",
                "dihidrotestosteron",
                "Dış genitalyanın maskülinizasyonundan sorumlu yüksek afiniteli androjen metaboliti"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-19-s36",
        "title": "Embriyonik Taslakların Karşılaştırması: DHT Varlığı vs Yokluğu",
        "content": "İndiferan dönemdeki ortak embriyonik dış genital taslaklar, DHT sinyalinin varlığına veya yokluğuna göre iki zıt yöne farklılaşır (Sınav Spotu):\n\n- **1. Genital Tüberkül (Phallus taslağı):**\n  - DHT varlığında (Erkek) $\\to$ **Penis (Glans ve Korpus kavernozumlar)**\n  - DHT yokluğunda (Dişi) $\\to$ **Klitoris (Glans ve Korpus klitoridis)**\n- **2. Ürogenital Kıvrımlar (Uretra katlantıları):**\n  - DHT varlığında (Erkek) $\\to$ Orta hatta kaynaşarak **Penil üretra ve Korpus spongiyozum**\n  - DHT yokluğunda (Dişi) $\\to$ Açık kalarak **Labia minörler (Küçük dudaklar)**\n- **3. Labioskrotal Kabartılar (Genital kabartılar):**\n  - DHT varlığında (Erkek) $\\to$ Orta hatta birleşip skrotal rafeyi yaparak **Skrotum (Testis torbası)**\n  - DHT yokluğunda (Dişi) $\\to$ Kaynaşmadan açık kalarak **Labia majörler (Büyük dudaklar)**\n- **4. Ürogenital Sinüs:**\n  - Erkekte $\\to$ Prostat ve bulbouretral bezler\n  - Dişide $\\to$ Alt 2/3 vajina ve vestibüler bezler (Bartholin).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Embriyonik Ortak Taslak", "DHT Varlığında (Erkek Farklılaşması)", "DHT Yokluğunda (Dişi Farklılaşması)"],
                [
                    ["Genital Tüberkül", "Glans ve korpus penis", "Klitoris"],
                    ["Ürogenital Kıvrımlar", "Penil üretra ve korpus spongiyozum", "Labia minora (Küçük dudaklar)"],
                    ["Labioskrotal Kabartılar", "Skrotum (testis torbası)", "Labia majora (Büyük dudaklar)"],
                    ["Ürogenital Sinüs", "Prostat bezi ve prostatik üretra", "Alt 2/3 vajina ve vestibül"]
                ]
            ),
            make_quiz(
                "İnsan embriyogenezinde dişi bireyde labia minorayı (küçük dudakları) oluşturan embriyonik taslak, erkekte DHT etkisiyle hangi yapıya farklılaşır?",
                [
                    {"key": "A", "text": "Penil üretra ve ventral penis dokusu", "isCorrect": True, "explanation": "Doğru cevap A'dır: Ürogenital kıvrımlar erkekte penil üretrayı kapatırken, dişide açık kalarak labia minorayı oluşturur."},
                    {"key": "B", "text": "Skrotum", "isCorrect": False, "explanation": "Skrotum labioskrotal kabartılardan gelişir (dişide labia majöra)."},
                    {"key": "C", "text": "Glans penis", "isCorrect": False, "explanation": "Glans penis genital tüberkülden gelişir (dişide klitoris)."},
                    {"key": "D", "text": "Epididim", "isCorrect": False, "explanation": "Epididim dış genital taslak değil, Wolff kanalı türevidir."}
                ]
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-19-s37",
        "title": "Kolesterol Biyosentezi ve Smith-Lemli-Opitz Sendromu (DHCR7)",
        "content": "Testosteron ve türevi olan tüm seks steroidleri kolesterol iskeletinden sentezlenir. Bu nedenle kolesterol biyosentezindeki genetik aksaklıklar genital gelişim bozukluğu ile doğrudan ilişkilidir (Sınav Spotu):\n\n- **Smith-Lemli-Opitz Sendromu (SLOS):**\n  - Kromozom 11q13.4 bölgesinde yer alan **DHCR7 (7-dehidrokolesterol redüktaz)** genindeki mutasyonlara bağlı otozomal resesif bir hastalıktır.\n  - Enzim eksikliği sonucu kolesterol sentezinin son basamağı tıkanır; kanda ve dokularda kolesterol dramatik düşerken toksik öncül **7-dehidrokolesterol (7-DHC)** birikir.\n- **Klinik ve Genital Bulgular:**\n  - Fetal Leydig hücreleri kolesterol yetersizliği nedeniyle yeterli testosteron üretemez.\n  - 46,XY erkek fetusta **şiddetli genital hipoplazi, mikrofallus, perineoskrotal hipospadias veya tam dişi dış genitalya** (46,XY CGB) görülür.\n  - Tipik dismorfik bulgular: 2. ve 3. ayak parmaklarında sindaktili (Y-şekilli sindaktili), mikrosefali, pitozis, yarık damak ve konjenital kalp defektleridir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Hastalık", "Defektli Enzim / Gen", "Biyokimyasal Tablo", "Genital ve Sistemik Bulgular"],
                [
                    ["Smith-Lemli-Opitz (SLOS)", "DHCR7 (11q13.4)", "Kolesterol çok düşük, 7-dehidrokolesterol aşırı yüksek", "46,XY ambigus genitalya/hipospadias, 2-3 ayak sindaktilisi, mikrosefali"]
                ]
            ),
            make_cloze(
                "Kolesterol biyosentezinde 7-dehidrokolesterol redüktaz enzim eksikliği sonucu 46,XY kuşkulu genitalya ve 2-3 ayak parmak sindaktilisi yapan hastalık Smith-Lemli-Opitz sendromudur.",
                "Smith-Lemli-Opitz sendromu",
                "DHCR7 mutasyonuna bağlı kolesterol sentez kusuru sendromu"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-19-s38",
        "title": "INSL3 (İnsülin Benzeri Peptid 3) ve Testisin İnişi (Desensus Testis)",
        "content": "Testislerin abdominal kaviteden skrotuma inmesi (desensus testis) iki farklı hormonal fazda gerçekleşen karmaşık bir süreçtir (Sınav Spotu):\n\n- **1. Transabdominal Faz (10-15. Haftalar):**\n  - Testislerin böbrek altından inguinal halkaya kadar inmesidir.\n  - Bu faz testosterondan bağımsızdır; Leydig hücrelerinden salgılanan **INSL3 (İnsülin benzeri peptid 3 / RLF)** hormonu tarafından yönetilir.\n  - INSL3, gubernakulum mezenkimindeki **RXFP2 (LGR8)** reseptörüne bağlanarak gubernakulumun kalınlaşmasını, kısalmasını ve testisi kasığa çekmesini sağlar.\n- **2. İnguinoskrotal Faz (26-35. Haftalar):**\n  - Testisin kasık kanalından geçip skrotuma inmesidir.\n  - Bu faz doğrudan **androjenlere (testosteron ve DHT)** bağımlıdır; genitofemoral sinir aracılığıyla kalsitonin geni ilişkili peptidi (CGRP) uyarır.\n- **Klinik:** INSL3 veya RXFP2 gen mutasyonları **kriptorşidizmin (inmemiş testis)** önemli monogenik nedenlerindendir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Transabdominal Faz vs İnguinoskrotal Faz",
                "Transabdominal Faz (10-15. Hafta)",
                "INSL3 ve RXFP2 reseptörü yönetir; gubernakulum kalınlaşarak testisi inguinal halkaya kadar çeker.",
                "İnguinoskrotal Faz (26-35. Hafta)",
                "Androjenler (Testosteron ve DHT) yönetir; testis kasık kanalını aşarak skrotum torbasına yerleşir."
            ),
            make_quiz(
                "Testislerin intraabdominal bölgeden inguinal halkaya kadar inmesini (transabdominal faz) sağlayan ve gubernakulum ligamanını kalınlaştıran Leydig hormonu hangisidir?",
                [
                    {"key": "A", "text": "INSL3 (İnsülin benzeri peptid 3)", "isCorrect": True, "explanation": "Doğru cevap A'dır: INSL3 transabdominal fazın anahtar hormonudur; gubernakulumdaki RXFP2 reseptörüne bağlanarak ilk inişi sağlar."},
                    {"key": "B", "text": "AMH", "isCorrect": False, "explanation": "AMH Müller gerilemesi yapar, inişte rolü yoktur."},
                    {"key": "C", "text": "Dihidrotestosteron", "isCorrect": False, "explanation": "DHT ikinci inguinoskrotal fazda etkilidir."},
                    {"key": "D", "text": "Prolaktin", "isCorrect": False, "explanation": "Prolaktin testisin inişini yönetmez."}
                ]
            )
        ]
    })

    # Slide 39 - CHECKPOINT 4
    slides.append({
        "id": "k1-19-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Kanal Sistemleri ve Dış Genitalya Farklılaşması",
        "content": "Bu checkpointte kanal türevlerini ve hormonların cinsiyet morfolojisine etkisini özetliyoruz:\n\n- **Wolff (Mezonefrik):** Lokal testosteron ile epididim, vas deferens, seminal vezikül ve ejakülatör kanala gelişir.\n- **Müller (Paramezonefrik):** Hormonsuz tüp, uterus ve üst vajinaya dönüşür; erkekte Sertoli kaynaklı **AMH ile aktif olarak yok edilir**.\n- **PMDS (Persistan Müller):** AMH veya AMHR2 mutasyonunda 46,XY erkekte uterus ve fallop tüpü bulunur; fıtık kesesinde saptanabilir.\n- **5α-Redüktaz ve DHT:** Testosteronu DHT'ye çevirir; DHT genital tüberkülü penise, kabartıları skrotuma, ürogenital katlantıları penil üretraya dönüştürür.\n- **Smith-Lemli-Opitz (DHCR7):** Kolesterol sentez kusuru; 46,XY ambigus genitalya ve 2-3 ayak sindaktilisi yapar.\n- **Desensus Testis İki Faz:**\n  1. Transabdominal faz $\\to$ **INSL3 ve RXFP2** kontrolünde,\n  2. İnguinoskrotal faz $\\to$ **Androjenler (Testosteron / DHT)** kontrolünde tamamlanır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Hormon / Enzim", "Salgılandığı Yer", "Temel Embriyolojik Görevi", "Eksikliğinde Ne Olur?"],
                [
                    ["AMH (MIS)", "Sertoli Hücreleri", "Müller kanallarını geriletmek", "Erkekte uterus kalması (PMDS)"],
                    ["Testosteron", "Leydig Hücreleri", "Wolff kanalını erkek iç organlarına dönüştürmek", "Erkek iç genital kanal agenezisi"],
                    ["5α-Redüktaz (DHT)", "Hedef Dokular", "Dış genitalyayı penise ve skrotuma dönüştürmek", "Dişi/ambigus dış genitalya (SRD5A2)"],
                    ["INSL3", "Leydig Hücreleri", "Gubernakulumu kalınlaştırıp transabdominal iniş sağlamak", "Abdominal kriptorşidizm"]
                ]
            ),
            make_chain(
                "İç ve Dış Erkek Farklılaşma Akışı",
                [
                    "1. Sertoli AMH Salgılar: Paramezonefrik Müller kanalları geriler ve yok olur.",
                    "2. Leydig Testosteron Üretir: Mezonefrik Wolff kanalı epididim ve vas deferense döner.",
                    "3. 5α-Redüktaz DHT Yapar: Dış genital tüberkül ve katlantılar penil üretrayı kapatır.",
                    "4. INSL3 ve Androjenler: Testis önce kasığa sonra skrotum içine indirilir."
                ]
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-19-s40",
        "title": "Bölüm Özeti: Kanallardan Cinsiyet Gelişim Bozuklukları Sınıflamasına Geçiş",
        "content": "Bölüm 4 boyunca iç genital kanalların (Wolff/Müller), hormonların (AMH, Testosteron, DHT, INSL3) ve dış genital taslakların farklılaşmasını inceledik:\n\n- **Özet:** Erkek fenotipinin oluşması için AMH, Testosteron ve DHT üçlüsünün eksiksiz çalışması şarttır.\n- **Sonraki Bölüm (Bölüm 5):** Bu gelişimsel adımlardaki aksaklıkların klinik sınıflaması olan **Chicago Konsensüsü (2006) Cinsiyet Gelişim Bozuklukları (CGB) sınıflamasını, Prader evrelemesini ve hermafroditizm/interseks terminolojisini** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "46,XY karyotipli normal erkek dış genitalyasına sahip bir bireyde ameliyat sırasında fıtık kesesi içinde uterus bulunması durumuna ne ad verilir?",
                "Persistan Müller Kanalı Sendromu (PMDS)",
                "AMH veya AMHR2 reseptör gen mutasyonuna bağlı embriyolojik kalıntı sendromu"
            ),
            make_quiz(
                "Dış genital taslaklardan olan 'labioskrotal kabartılar' DHT hormonunun yokluğunda hangi dişi anatomik yapısına farklılaşır?",
                [
                    {"key": "A", "text": "Labia majörler (Büyük dudaklar)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Labioskrotal kabartılar DHT varlığında skrotumu, yokluğunda labia majörleri oluşturur."},
                    {"key": "B", "text": "Klitoris", "isCorrect": False, "explanation": "Klitoris genital tüberkülden gelişir."},
                    {"key": "C", "text": "Labia minörler", "isCorrect": False, "explanation": "Labia minörler ürogenital kıvrımlardan gelişir."},
                    {"key": "D", "text": "Hymen", "isCorrect": False, "explanation": "Hymen sinovajinal ampullerden gelişir."}
                ]
            )
        ]
    })

    return slides
