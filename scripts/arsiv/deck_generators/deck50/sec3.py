from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec3():
    slides = []

    # Slide 21
    slides.append(make_slide(
        title="Sekonder Sifilizde Genel Lenfadenopati",
        narrative="""Sekonder sifiliz evresinde spiroketlerin tüm vücuda yayılması sonucunda immün sistem yoğun bir yanıt oluşturur ve yaygın lenfadenopati (LAP) gelişir. Hastaların %50 ila %85'inde görülen bu bulgu, sistemik inflamasyonun önemli bir yansımasıdır.

Büyüyen lenf nodlarının klinik özellikleri şöyledir:
* **Yaygın dağılım:** Servikal, aksiller, inguinal ve femoral bölgeler başta olmak üzere birden fazla lenf nodu istasyonu eş zamanlı olarak etkilenir.
* **Ağrısız karakter:** Lenf nodları tipik olarak büyüktür, sert veya lastik kıvamındadır ancak palpe edildiklerinde ağrıya neden olmazlar.
* **Fiksasyon eksikliği:** Çevre dokulara yapışık değillerdir, serbestçe hareket edebilirler.

> Yaygın, ağrısız ve hareketli lenfadenopati varlığında, özellikle eşlik eden makülopapüler döküntü veya genital ülser öyküsü varsa, sekonder sifiliz mutlak surette akla gelmelidir. Bu durum, sistemik spiroketeminin net bir göstergesidir.""",
        elements=[
            make_cloze("Sekonder sifilizde hastaların %50-85'inde görülen ve spiroketlerin sistemik yayılımını yansıtan lenf nodu bulgusu yaygın {{lenfadenopatidir}} (LAP)."),
            make_cloze("Sekonder sifilizdeki lenfadenopatiler tipik olarak palpe edildiklerinde {{ağrısızdır}}."),
            make_table(
                headers=["Lenfadenopati Özelliği", "Klinik Açıklama"],
                rows=[
                    ["Lokalizasyon", "Yaygın (servikal, aksiller, inguinal vb. tüm bölgeler)"],
                    ["Ağrı Durumu", "Ağrısız (palpasyonda hassasiyet yok)"],
                    ["Mobilite", "Hareketli (çevre dokulara yapışık değil)"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Sifilizde LAP Karakteristikleri",
                [
                    {"text": "Sekonder sifilizde lenf nodları büyümüş ancak ağrısızdır.", "isLie": False, "explanation": "Doğru, sifilitik lenfadenopati tipik olarak ağrısız seyir gösterir."},
                    {"text": "Lenf nodları çevre dokulara sıkıca fiksedir ve hareket ettirilemez.", "isLie": True, "explanation": "Yanlış! Sifilizdeki lenf nodları çevre dokulara yapışık (fikse) değildir, serbestçe hareket edebilirler."},
                    {"text": "Servikal, aksiller ve inguinal bölgeler yaygın olarak tutulabilir.", "isLie": False, "explanation": "Doğru, lenfadenopati tek bir bölgeyle sınırlı kalmayıp jeneralize karakterdedir."}
                ]
            ),
            make_quiz(
                question="Sekonder sifilizde görülen lenfadenopatinin (LAP) en belirgin muayene bulgularından biri aşağıdakilerden hangisidir?",
                options=[
                    "Sıcak, kızarık ve aşırı ağrılı olması",
                    "Çevre dokulara yapışık, hareketsiz kitle şeklinde olması",
                    "Sadece sol supraklaviküler bölgede tekil olarak izlenmesi",
                    "Yaygın dağılımlı, ağrısız ve hareketli olması",
                    "Hızlıca kazeifiye olup fistülize olması"
                ],
                answer="Yaygın dağılımlı, ağrısız ve hareketli olması",
                explanation="Sekonder sifiliz LAP'ı yaygın, ağrısız (lastik kıvamında) ve çevre dokulara fikse olmayan (hareketli) bir karakter sergiler."
            )
        ]
    ))

    # Slide 22
    slides.append(make_slide(
        title="Sekonder Sifilizin Patognomonik Bulgusu: Epitroklear LAP",
        narrative="""Sekonder sifilizde jeneralize lenfadenopati sık görülmesine rağmen, spesifik bir bölgedeki lenf nodu büyümesi hastalığın tanısında kilit bir rol oynar. Dirsek bölgesinde yer alan epitroklear lenf nodlarının büyümesi, sekonder sifiliz için neredeyse patognomonik bir bulgu olarak kabul edilir.

Epitroklear lenfadenopati ile ilgili önemli noktalar:
* **Nadir tutulum:** Normal şartlarda enfeksiyonlarda epitroklear lenf nodları nadiren belirginleşir. Bu bölgenin şişmesi, spesifik enfeksiyonlar (özellikle sifiliz) açısından kuvvetli bir uyarıcıdır.
* **Tanısal değer:** Makülopapüler döküntü (özellikle el ayası-ayak tabanı tutulumlu) ile birlikte epitroklear LAP saptanması, aksi kanıtlanana kadar sifilizi işaret eder.
* **Fizik muayene kuralı:** Şüpheli döküntüsü olan hastalarda, kolların dirsek üstü iç kısımlarının dikkatlice palpe edilmesi zorunludur.

> Epitroklear lenfadenopati, sekonder sifilizin en özgün fizik muayene bulgularından biridir. Hekimler, sebebi açıklanamayan jeneralize LAP veya atipik deri döküntüsü olan her hastada epitroklear bölgeyi rutin olarak kontrol etmelidir.""",
        elements=[
            make_cloze("Sekonder sifiliz için neredeyse patognomonik (tanı koydurucu) kabul edilen lenf nodu büyümesi, dirsekte izlenen {{epitroklear}} LAP'tır."),
            make_cloze("Genel enfeksiyonlarda nadir şişen ancak sekonder sifilizde büyüyerek önemli tanısal ipucu sağlayan bölge {{epitroklear}} lenf nodlarıdır."),
            make_chain(
                "Epitroklear LAP ve Sifiliz İlişkisi",
                "Hangi bölgedeki LAP, sekonder sifiliz için çok tipiktir?",
                "Epitroklear lenf nodu",
                "Epitroklear LAP'a ek olarak hangi döküntü eşlik ederse sifiliz tanısı kesinleşir gibi olur?",
                "El ayası ve ayak tabanı tutulumu olan makülopapüler döküntü"
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Epitroklear Lenfadenopati",
                [
                    {"text": "Epitroklear lenfadenopati, sekonder sifiliz tanısı için güçlü ve özgün (patognomonik) bir fizik muayene bulgusudur.", "isLie": False, "explanation": "Doğru, dirsek bölgesindeki bu LAP sifiliz için çok tipiktir."},
                    {"text": "Epitroklear lenf nodları sıradan üst solunum yolu enfeksiyonlarında en sık büyüyen lenf nodlarıdır.", "isLie": True, "explanation": "Yanlış! Epitroklear nodlar rutin enfeksiyonlarda nadiren büyür; büyümeleri sifiliz gibi spesifik durumları akla getirmelidir."},
                    {"text": "Palmar-plantar döküntüsü olan bir hastada epitroklear LAP bulunması sekonder sifiliz ihtimalini oldukça güçlendirir.", "isLie": False, "explanation": "Doğru, bu kombinasyon sifiliz için klasik ve çok değerlidir."}
                ]
            ),
            make_quiz(
                question="Bir hastada gövdede döküntü, avuç içi ve ayak tabanlarında lezyonlar saptanıyor. Fizik muayenede sekonder sifiliz tanısını destekleyecek en patognomonik lenf nodu bölgesi neresidir?",
                options=[
                    "Submental",
                    "Popliteal",
                    "Epitroklear",
                    "Paraaortik",
                    "Oksipital"
                ],
                answer="Epitroklear",
                explanation="Epitroklear bölgedeki (dirsek iç kısmı) lenfadenopati, sekonder sifiliz için klasik ve son derece yönlendirici, neredeyse patognomonik bir bulgudur."
            )
        ]
    ))

    # Slide 23
    slides.append(make_slide(
        title="Sekonder Sifilizde Sistemik Semptomlar (Ateş, Kırgınlık, Kilo Kaybı, Farenjit)",
        narrative="""Sekonder sifiliz, spiroketlerin kan dolaşımı yoluyla yayılmasına (spiroketemi) bağlı olarak sistemik, influenza (grip) benzeri semptomlarla kendini gösterir. Bu dönemde deri lezyonlarına eşlik eden genel bir 'hasta olma' hali (konstitüsyonel semptomlar) mevcuttur. Hastalar sıklıkla enfeksiyöz bir sürecin genel bulgularını yaşarlar.

En sık karşılaşılan sistemik semptomlar:
* **Hafif veya orta dereceli ateş:** Genellikle çok yüksek değildir ancak inatçı olabilir.
* **Halsizlik ve kırgınlık (Malaise):** Hastanın günlük aktivitelerini kısıtlayabilen yaygın bir yorgunluk halidir.
* **İştahsızlık ve kilo kaybı:** Metabolik stres ve inflamasyon sonucu ortaya çıkar.
* **Kas ve baş ağrıları:** Yaygın miyalji ve künt baş ağrısı bildirebilirler.
* **Farenjit:** Boğaz ağrısı ve yutkunma zorluğu, mukozal tutuluma sekonder sık görülür.

> Sekonder sifiliz, spesifik döküntüler ortaya çıkmadan önce sadece grip benzeri sistemik bir hastalık gibi davranabilir. Bu nedenle 'Büyük Taklitçi' ünvanının bir parçası olarak, atipik uzamış ateş ve kırgınlık tablolarında sifiliz ayrıcı tanıda düşünülmelidir.""",
        elements=[
            make_cloze("Sekonder sifilizin başlangıcında spiroketemiye bağlı olarak halsizlik, ateş ve baş ağrısı gibi {{influenza}} benzeri (grip benzeri) semptomlar görülebilir."),
            make_cloze("Sistemik tutulumun mukozal bir göstergesi olarak sekonder sifilizli hastalarda boğaz ağrısı ve {{farenjit}} sıkça izlenir."),
            make_table(
                headers=["Konstitüsyonel Semptom", "Klinik Özellik"],
                rows=[
                    ["Ateş", "Hafif-orta dereceli, bazen inatçı"],
                    ["Kırgınlık (Malaise)", "Yaygın yorgunluk ve kas ağrısı (miyalji)"],
                    ["Farenjit", "Boğaz ağrısı, mukozal tutuluma bağlı"],
                    ["Metabolik", "İştahsızlık ve açıklanamayan kilo kaybı"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Sifilizde Sistemik Semptomlar",
                [
                    {"text": "Sekonder sifilizde spiroketemiye bağlı grip benzeri konstitüsyonel semptomlar izlenir.", "isLie": False, "explanation": "Doğru, ateş, miyalji ve halsizlik çok tipiktir."},
                    {"text": "Sekonder sifilizde ateş genellikle çok şiddetlidir ve her hastada mutlaka septik şok tablosuna ilerler.", "isLie": True, "explanation": "Yanlış! Ateş genellikle hafif-orta derecelidir ve septik şok gibi ağır ve fulminan tablolar sekonder sifilizde beklenmez."},
                    {"text": "Hastalar kilo kaybı, iştahsızlık ve boğaz ağrısı (farenjit) gibi spesifik olmayan şikayetlerle başvurabilir.", "isLie": False, "explanation": "Doğru, bu nedenle hastalık diğer viral/bakteriyel enfeksiyonları taklit edebilir."}
                ]
            ),
            make_quiz(
                question="Aşağıdakilerden hangisi sekonder sifilizde izlenen sistemik (konstitüsyonel) semptomlardan biri değildir?",
                options=[
                    "Hafif-orta dereceli ateş",
                    "Yaygın lenfadenopati",
                    "Farenjit",
                    "Ani başlangıçlı, şiddetli ve massif hemoptizi",
                    "İştahsızlık ve kilo kaybı"
                ],
                answer="Ani başlangıçlı, şiddetli ve massif hemoptizi",
                explanation="Hemoptizi (kan tükürme) sekonder sifilizin klasik bir sistemik semptomu değildir. Ateş, farenjit, kilo kaybı ve halsizlik beklenen sistemik bulgulardır."
            )
        ]
    ))

    # Slide 24
    slides.append(make_slide(
        title="Sekonder Sifilizde İskelet Sistemi: Sinovit, Artralji ve Osteit",
        narrative="""Sekonder sifilizdeki spiroket yayılımı iskelet sistemini de etkileyerek eklem ve kemik patolojilerine yol açabilir. Eklem şikayetleri hastaların %10-20'sinde görülürken, kemik tutulumu nadir ancak oldukça ağrılıdır.

İskelet sistemi tutulumunun temel klinik formları:
* **Artralji ve Poliartrit:** Genellikle diz, ayak bileği ve el bileği gibi büyük eklemleri tutan simetrik veya asimetrik eklem ağrılarıdır. Bazen sinovit (eklem zarı iltihabı) eşlik edebilir.
* **Osteit ve Periosteit:** Kemik ve kemik zarının inflamasyonudur. En sık uzun kemiklerde (tibia) ve kafatasında (kraniyum) izlenir.
* **Gece Ağrıları:** Sifilitik kemik ağrılarının (ostealji) en belirgin özelliği, ağrının geceleri dinlenme halindeyken (yatak sıcaklığında) şiddetlenmesidir.

> Kemik tutulumu, hastanın gece uykusundan uyanmasına neden olacak kadar şiddetli, oyan-sızlayan tarzda kemik ağrılarıyla (osteokopik ağrı) karakterizedir. Açıklanamayan gece kemik ağrısı olan hastalarda sekonder sifiliz mutlaka ekarte edilmelidir.""",
        elements=[
            make_cloze("Sekonder sifilizde eklem zarı iltihaplanmasına bağlı olarak büyük eklemlerde {{sinovit}} ve artralji gelişebilir."),
            make_cloze("Sifilitik periosteit ve osteit nedeniyle oluşan şiddetli kemik ağrıları tipik olarak {{gece}} saatlerinde, hasta yatakta yatarken artış gösterir."),
            make_chain(
                "Sifiliz ve İskelet Sistemi",
                "Sekonder sifilizde eklemlerde en sık hangi semptom görülür?",
                "Artralji ve poliartrit",
                "Kemik zarının iltihaplanmasına ne ad verilir ve sifilizde görülebilir mi?",
                "Periosteit, evet görülebilir",
                "Sifilitik kemik ağrısının en tipik zamanlama özelliği nedir?",
                "Geceleri şiddetlenmesi"
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Sifilizde Kemik/Eklem Tutulumu",
                [
                    {"text": "Sekonder sifiliz hastalarında diz ve ayak bileği gibi büyük eklemlerde artralji ve sinovit görülebilir.", "isLie": False, "explanation": "Doğru, iskelet sistemi tutulumunun bir parçası olarak eklem şikayetleri sıktır."},
                    {"text": "Osteit ve periosteit kaynaklı kemik ağrıları tipik olarak hastanın hareketli olduğu gündüz saatlerinde artar, gece ise tamamen kaybolur.", "isLie": True, "explanation": "Yanlış! Sifilitik kemik ağrıları (osteokopik ağrı) klasik olarak *geceleri* şiddetlenir ve dinlenme halindeyken daha rahatsız edicidir."},
                    {"text": "Tibia ve kraniyum sekonder sifiliz periosteitinde sık tutulan kemikler arasındadır.", "isLie": False, "explanation": "Doğru, uzun kemikler ve kafatası tutuluma yatkındır."}
                ]
            ),
            make_quiz(
                question="Sekonder sifiliz şüphesi olan 30 yaşında bir erkek hasta, bacaklarında şiddetli ağrılardan şikayet etmektedir. Ağrının karakteri sorgulandığında, hekimin sifilitik periosteit düşünmesini sağlayacak en spesifik özellik aşağıdakilerden hangisidir?",
                options=[
                    "Ağrının sadece merdiven inip çıkarken oluşması",
                    "Ağrının tipik olarak geceleri ve yatakta dinlenirken şiddetlenmesi",
                    "Ağrının yürüdükçe azalan ancak sabah tutukluğu ile başlaması",
                    "Ağrılı bölgede krepitasyon alınması",
                    "Ağrının yemeklerden hemen sonra ortaya çıkması"
                ],
                answer="Ağrının tipik olarak geceleri ve yatakta dinlenirken şiddetlenmesi",
                explanation="Sifilizdeki kemik ağrılarının klasik özelliği geceleri şiddetlenmesi ve hastayı uykudan uyandırmasıdır."
            )
        ]
    ))

    # Slide 25
    slides.append(make_slide(
        title="Sekonder Sifilizde Karaciğer Tutulumu: Sifilitik Hepatit",
        narrative="""Spiroketlerin yayılımı karaciğeri etkileyerek sekonder sifiliz hastalarının %1-10'unda 'Sifilitik Hepatit' tablosuna yol açabilir. Genellikle asemptomatiktir veya çok hafif belirtiler verir, ancak laboratuvar testlerinde karakteristik bir enzim profili çizer.

Sifilitik hepatitin klinik ve laboratuvar bulguları:
* **Alkalen Fosfataz (ALP) Yüksekliği:** En belirgin laboratuvar bulgusudur. ALP düzeyleri normalin çok üzerine çıkarken (kolestatik patern), transaminazlar (ALT, AST) genellikle orantısız şekilde sadece hafif yükselir.
* **Hepatomegali:** Fizik muayenede karaciğer büyük ve hassas olarak palpe edilebilir.
* **Sarılık:** Nadiren belirgin klinik sarılık (ikter) izlenebilir.

> Sifilitik hepatit, karaciğer biyopsisinde spesifik bir bulgu olmaksızın portal inflamasyonla karakterizedir. Karaciğer enzimlerinde sebebi açıklanamayan, belirgin ALP yüksekliği ve hafif AST/ALT yüksekliği olan hastalarda, özellikle deride makülopapüler lezyonlar varsa sekonder sifiliz araştırılmalıdır.""",
        elements=[
            make_cloze("Sekonder sifilize bağlı gelişen sifilitik hepatitte tipik laboratuvar bulgusu, transaminazlara kıyasla çok daha orantısız ve yüksek olan {{Alkalen Fosfataz}} (ALP) düzeyidir."),
            make_cloze("Sifilitik hepatitli hastalarda fizik muayenede karaciğer büyümesi olan {{hepatomegali}} saptanabilir."),
            make_table(
                headers=["Laboratuvar/Klinik Bulgu", "Sifilitik Hepatitteki Durumu"],
                rows=[
                    ["Alkalen Fosfataz (ALP)", "Orantısız, belirgin düzeyde yüksek (kolestatik patern)"],
                    ["ALT ve AST", "Hafif veya ılımlı artış"],
                    ["Fizik Muayene", "Hepatomegali (büyük karaciğer)"],
                    ["Klinik Sarılık", "Nadir görülür ancak olasılık dahilindedir"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilitik Hepatit",
                [
                    {"text": "Sifilitik hepatitte Alkalen Fosfataz (ALP) düzeyinde belirgin bir artış görülmesi tipiktir.", "isLie": False, "explanation": "Doğru, kolestatik enzim profili sifilitik karaciğer tutulumunun karakteristik bulgusudur."},
                    {"text": "Hastaların fizik muayenesinde sıklıkla hepatomegali saptanır.", "isLie": False, "explanation": "Doğru, karaciğer boyutunda artış izlenebilir."},
                    {"text": "Sifilitik hepatitin patognomonik laboratuvar bulgusu, ALP normal seyrederken ALT'nin 10.000 U/L üzerine çıkmasıdır (fulminan hepatit profili).", "isLie": True, "explanation": "Yanlış! Sifilitik hepatitte tablo tam tersidir; ALT/AST hafif artarken asıl orantısız yükselen enzim ALP'dir. Fulminan hepatit tablosu yaratmaz."}
                ]
            ),
            make_quiz(
                question="Yaygın makülopapüler döküntü şikayetiyle başvuran sekonder sifilizli bir hastanın rutin kan tetkiklerinde karaciğer tutulumu saptanmıştır. Bu hastada 'sifilitik hepatit' tanısını en çok destekleyen laboratuvar profili aşağıdakilerden hangisidir?",
                options=[
                    "Normal ALP, aşırı yüksek ALT ve AST (2000 U/L üzeri)",
                    "Sadece bilirubinlerin yüksekliği, normal ALT, AST, ALP",
                    "Orantısız ve belirgin yüksek Alkalen Fosfataz (ALP) ve hafif artmış ALT/AST",
                    "Masif hipoalbüminemi ve uzamış PT, normal enzimler",
                    "Sıfıra inmiş ALP ve yüksek amilaz"
                ],
                answer="Orantısız ve belirgin yüksek Alkalen Fosfataz (ALP) ve hafif artmış ALT/AST",
                explanation="Sifilitik hepatit klasik olarak kolestatik bir enzim profiline neden olur. ALP çok yüksekken, transaminazlar (ALT, AST) nispeten hafif yüksektir."
            )
        ]
    ))

    # Slide 26
    slides.append(make_slide(
        title="Sekonder Sifilizde Oküler Tutulum: Üveit ve Görme Değişiklikleri",
        narrative="""Sifiliz, 'büyük taklitçi' olarak gözün hemen her tabakasını tutabilir. Ancak sekonder evrede en sık karşılaşılan oküler manifestasyon **üveit**'tir (gözün uvea tabakasının iltihabı). Göz tutulumu hızlıca tanınmalı ve tedavi edilmelidir, aksi takdirde kalıcı görme kaybı riski taşır.

Sekonder sifiliz oküler tutulumunda öne çıkanlar:
* **Ön ve Arka Üveit:** En sık tutulan alanlardır. Hastalar gözde kızarıklık, ağrı, ışığa hassasiyet (fotofobi) ve bulanık görme şikayetiyle başvurur.
* **Optik Nörit ve Retinit:** Daha az sıklıkta görülse de görme sinirinin veya retinanın doğrudan spiroket invazyonu görme keskinliğinde ani düşüşlere yol açar.
* **Nörosifiliz İlişkisi:** Oküler sifiliz saptanan hastaların önemli bir kısmında, klinik veya asemptomatik nörosifiliz birlikteliği (BOS anormallikleri) bulunur.

> Herhangi bir evredeki oküler sifiliz, merkezi sinir sistemi (SSS) tutulumu gibi ele alınmalı ve agresif intravenöz penisilin tedavisi (nörosifiliz dozunda) uygulanmalıdır.""",
        elements=[
            make_cloze("Sekonder sifilizde gözün uvea tabakasının inflamasyonuna bağlı olarak göz ağrısı, fotofobi ve bulanık görme ile seyreden oküler tutuluma {{üveit}} denir."),
            make_cloze("Oküler sifiliz saptanan her vakada tedavi rejimi, {{nörosifiliz}} ile eşdeğer kabul edilerek agresif (intravenöz penisilin) şekilde uygulanmalıdır."),
            make_table(
                headers=["Oküler Semptom", "Açıklama"],
                rows=[
                    ["Bulanık Görme / Görme Kaybı", "Üveit, retinit veya optik nörit kaynaklı olabilir"],
                    ["Fotofobi", "Işığa karşı aşırı hassasiyet (özellikle ön üveitte)"],
                    ["Göz Ağrısı ve Kızarıklık", "Aktif inflamasyonu (üveiti) işaret eder"],
                    ["Klinik Yönetim", "Sıradan sekonder sifiliz değil, SSS/Nörosifiliz gibi tedavi edilir"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Sifilizde Göz Tutulumu",
                [
                    {"text": "Sekonder evrede gözde en sık üveit tablosu görülür ve fotofobiye yol açabilir.", "isLie": False, "explanation": "Doğru, üveit sekonder sifilizin klasik oküler bulgusudur."},
                    {"text": "Oküler sifiliz tespit edildiğinde, SSS tutulumu riskinden dolayı nörosifiliz tedavi rejimleri kullanılır.", "isLie": False, "explanation": "Doğru, oküler ve otik tutulumlar nörosifiliz gibi yönetilir."},
                    {"text": "Göz tutulumu sekonder sifilizde lokal bir olay kabul edildiği için tedavisinde sadece topikal göz damlaları yeterlidir.", "isLie": True, "explanation": "Yanlış! Oküler sifiliz sistemik ve agresif bir durumdur; topikal tedavi yetmez, yüksek doz intravenöz penisilin (nörosifiliz tedavisi) şarttır."}
                ]
            ),
            make_quiz(
                question="Sekonder sifiliz tedavisi gören 40 yaşında bir hasta yeni başlayan göz ağrısı, kızarıklık ve ışığa hassasiyet (fotofobi) şikayetleriyle başvuruyor. Yapılan muayenede ön üveit saptanıyor. Bu hastanın tedavi yönetimi açısından en doğru yaklaşım aşağıdakilerden hangisidir?",
                options=[
                    "Tedaviyi kesip sadece kortikosteroid damla başlamak",
                    "Hastalığın seyrine bırakıp 6 ay sonra kontrole çağırmak",
                    "Sadece oral antihistaminik vermek",
                    "Hastayı nörosifiliz gibi kabul edip yüksek doz intravenöz (IV) penisilin tedavisi planlamak",
                    "Deri döküntüleri geçene kadar göz tedavisi uygulamamak"
                ],
                answer="Hastayı nörosifiliz gibi kabul edip yüksek doz intravenöz (IV) penisilin tedavisi planlamak",
                explanation="Oküler sifiliz (üveit, optik nörit vb.), evresi ne olursa olsun nörosifiliz eşdeğeri olarak kabul edilir ve IV penisilin tedavisi gerektirir."
            )
        ]
    ))

    # Slide 27
    slides.append(make_slide(
        title="Sekonder Sifilizde Böbrek Tutulumu: İmmün Kompleks Glomerülonefriti",
        narrative="""Sekonder sifiliz, renal dokulara doğrudan spiroket invazyonundan ziyade, immün mekanizmalar üzerinden böbrek tutulumuna neden olur. Temel patofizyoloji, antijen-antikor (immün) komplekslerinin böbrek glomerüllerinde birikmesiyle karakterizedir.

Böbrek tutulumunun klinik yansımaları:
* **Membranöz Nefropati:** Sifilize bağlı böbrek tutulumunun en sık görülen histopatolojik formudur.
* **Nefrotik Sendrom:** Glomerüler hasar sonucunda masif proteinüri (>3.5 g/gün), hipoalbüminemi ve jeneralize ödem gelişebilir.
* **Geri Dönüşümlülük:** Sifilize sekonder nefrotik sendromun en iyi özelliği, enfeksiyonun penisilin ile başarılı bir şekilde tedavi edilmesinin ardından böbrek fonksiyonlarının hızla normale dönmesidir (geri dönüşümlü nefropati).

> Sebebi açıklanamayan nefrotik sendrom (özellikle membranöz nefropati paterni ile) saptanan erişkin hastalarda, sekonder sifiliz nadir ancak tamamen tedavi edilebilir bir sekonder neden olarak akılda tutulmalıdır.""",
        elements=[
            make_cloze("Sekonder sifilizdeki böbrek hasarı genellikle antijen-antikor yapılarının böbrekte çökmesine bağlı gelişen {{immün kompleks}} glomerülonefriti mekanizmasıyla oluşur."),
            make_cloze("Sifilitik böbrek tutulumu sıklıkla masif proteinüri ve ödemle seyreden {{nefrotik}} sendrom tablosuna yol açar."),
            make_chain(
                "Sifiliz ve Renal Sistem",
                "Sekonder sifilizde böbrek hasarı hangi mekanizmayla oluşur?",
                "İmmün kompleks birikimi",
                "Bu birikim en sık hangi sendroma yol açar?",
                "Nefrotik sendrom",
                "Sifilitik nefrotik sendromun histopatolojik tipi genellikle nedir?",
                "Membranöz nefropati"
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilize Bağlı Böbrek Tutulumu",
                [
                    {"text": "Sekonder sifilizde antijen-antikor komplekslerinin birikimiyle membranöz nefropati gelişebilir.", "isLie": False, "explanation": "Doğru, immün kompleks birikimi membranöz paterne yol açar."},
                    {"text": "Sifilitik böbrek tutulumunda masif proteinüri ve ödem ile karakterize nefrotik sendrom tablosu oluşabilir.", "isLie": False, "explanation": "Doğru, immün kompleks birikimi nefrit yerine daha çok nefrotik tablo yapar."},
                    {"text": "Sifilize bağlı nefrotik sendrom geri dönüşümsüzdür; sifiliz tedavi edilse bile hasta mutlaka ömür boyu diyalize girer.", "isLie": True, "explanation": "Yanlış! Sifiliz tedavisi sonrası nefrotik sendrom tablosu büyük oranda geriler ve böbrekler normale döner (geri dönüşümlüdür)."}
                ]
            ),
            make_quiz(
                question="Sekonder sifiliz nedeniyle oluşan böbrek patolojisinin alt yatan en olası immünolojik mekanizması aşağıdakilerden hangisidir?",
                options=[
                    "Böbrekteki bazal membranlara karşı gelişen otoantikorlar (Anti-GBM)",
                    "Treponema pallidum'un böbrek pelvisine doğrudan kitlesel invazyonu",
                    "Dolaşımdaki immün komplekslerin böbrek glomerüllerinde birikmesi (Tip 3 Aşırı Duyarlılık)",
                    "T hücrelerinin doğrudan renal tübüllere saldırması (Hücresel red benzeri)",
                    "Böbrekte amiloid proteinlerinin aşırı sekresyonu"
                ],
                answer="Dolaşımdaki immün komplekslerin böbrek glomerüllerinde birikmesi (Tip 3 Aşırı Duyarlılık)",
                explanation="Sifilizdeki böbrek tutulumu (membranöz nefropati/nefrotik sendrom), spiroket antijenleri ile antikorların oluşturduğu komplekslerin glomerüllerde birikmesi sonucu inflamasyon yaratmasıyla oluşur."
            )
        ]
    ))

    # Slide 28
    slides.append(make_slide(
        title="Sekonder Dönemde Erken SSS Tutulumu: Akut Nörosifiliz (Aseptik Menenjit)",
        narrative="""Nörosifiliz genellikle geç (tersiyer) bir komplikasyon olarak bilinse de, spiroketler hastalığın çok erken evrelerinde (primer ve sekonder dönemde) beyin omurilik sıvısına (BOS) geçerler. Bu geçiş, sekonder evrede 'Erken Nörosifiliz' veya 'Akut Sifilitik Menenjit' formunda semptomatik hale gelebilir.

Sekonder dönemdeki akut menenjitin özellikleri:
* **Meningeal İritasyon Bulguları:** Şiddetli baş ağrısı, ense sertliği ve fotofobi ile prezente olur.
* **Kranial Sinir Tutulumları:** Menenjite bağlı bazal yapıların etkilenmesi sonucu Kranial Sinir 2 (optik), 7 (fasiyal) ve 8 (akustik) en sık etkilenen sinirlerdir. İşitme kaybı, vertigo ve fasiyal paralizi görülebilir.
* **BOS Bulguları:** Lomber ponksiyonda (LP) aseptik menenjit tablosu izlenir; mononükleer hücre artışı (pleositoz), protein yüksekliği ve normal glikoz seviyeleri bulunur. BOS'ta VDRL pozitifliği tanıyı kesinleştirir.

> Erken dönem nörosifiliz, sıklıkla bakteriyel olmayan (aseptik) menenjit kliniği verir. Döküntüsü olan ve aynı zamanda ense sertliği ya da kranial sinir felci geliştiren hastalarda, sifilitik menenjit derhal tedavi edilmelidir.""",
        elements=[
            make_cloze("Sekonder sifiliz döneminde spiroketlerin BOS'u invaze etmesi sonucunda şiddetli baş ağrısı ve ense sertliği ile karakterize akut sifilitik {{menenjit}} tablosu gelişebilir."),
            make_cloze("Akut sifilitik menenjitte bazal inflamasyon nedeniyle özellikle kranial sinir felçleri görülebilir; en sık etkilenen kranial sinirler 2, {{7}} ve 8'dir."),
            make_table(
                headers=["BOS Bulgu Parametresi", "Akut Sifilitik Menenjitteki Durum"],
                rows=[
                    ["Hücre Sayısı (Pleositoz)", "Artmış (genellikle lenfosit/mononükleer ağırlıklı)"],
                    ["Protein Düzeyi", "Artmış (hafif-orta derece)"],
                    ["Glikoz Düzeyi", "Genellikle normal sınırlar içinde"],
                    ["Seroloji (Örn. VDRL)", "BOS'ta reaktif (pozitif) saptanabilir"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erken Nörosifiliz / Akut Menenjit",
                [
                    {"text": "Akut sifilitik menenjit baş ağrısı, ense sertliği ve kraniyal sinir tutulumları (özellikle 2, 7 ve 8) ile ortaya çıkabilir.", "isLie": False, "explanation": "Doğru, sekonder sifilizin klasik SSS tutulumudur."},
                    {"text": "Nörosifiliz sadece hastalığın tersiyer (geç) evresinde, bulaştan 20 yıl sonra ortaya çıkan bir tablodur; sekonder evrede SSS asla tutulmaz.", "isLie": True, "explanation": "Yanlış! Nörosifiliz hastalığın HERHANGİ bir evresinde oluşabilir. Primer veya sekonder evrede 'erken nörosifiliz' (akut menenjit) şeklinde ortaya çıkabilir."},
                    {"text": "BOS incelemesinde aseptik menenjit profili (lenfositik pleositoz, normal glikoz, artmış protein) saptanır.", "isLie": False, "explanation": "Doğru, sifilitik menenjit piyojenik değil aseptik profil çizer."}
                ]
            ),
            make_quiz(
                question="Sekonder sifiliz tanısıyla izlenen bir hastada ani gelişen yüzün bir yarısında felç (fasiyal paralizi) ve işitme kaybı ortaya çıkmıştır. Bu durum aşağıdakilerden hangisi ile en iyi açıklanır?",
                options=[
                    "Böbrek yetmezliğine bağlı üremik ensefalopati",
                    "Erken nörosifiliz (Akut sifilitik menenjit) kaynaklı kranial sinir tutulumu",
                    "İmmün komplekslerin doğrudan temporal kemiği eritmesi (Osteit)",
                    "Sifilitik hepatit komasına girmesi",
                    "Sifilitik alopesinin iç kulağı etkilemesi"
                ],
                answer="Erken nörosifiliz (Akut sifilitik menenjit) kaynaklı kranial sinir tutulumu",
                explanation="Erken nörosifiliz (menenjit), beynin bazal kısmını etkileyerek oradan geçen 7. (fasiyal) ve 8. (işitme/denge) kraniyal sinirlerde felç ve fonksiyon kaybına neden olur."
            )
        ]
    ))

    # Slide 29
    slides.append(make_slide(
        title="Sekonder Sifiliz Bulgularının Spontan Rezolüsyonu (Haftalar/Aylar İçinde Gerileme)",
        narrative="""Sekonder sifilizin en ilginç ve klinik olarak yanıltıcı özelliklerinden biri, immün sistemin geçici başarısına bağlı olarak lezyonların tedavisiz bile iyileşebilmesidir. Sistemik spiroketemi evresi sonsuza dek sürmez.

Doğal seyrin dinamikleri:
* **Spontan Gerileme:** Sekonder döneme ait makülopapüler döküntüler, kondiloma lata, jeneralize lenfadenopati ve sistemik semptomlar (ateş, kırgınlık) genellikle 3 ila 12 hafta içinde tıbbi müdahale olmaksızın kendi kendine (spontan) tamamen kaybolur.
* **Yanıltıcı İyileşme:** Hasta ve bazen hekim, bu spontan gerilemeyi 'iyileşme' olarak yanlış yorumlayabilir. Oysa enfeksiyon vücuttan atılmamış, spiroketler dokulara yerleşerek bağışıklık sisteminden saklanmaya başlamıştır.
* **Latent Döneme Geçiş:** Belirtilerin tamamen ortadan kalkmasıyla sekonder evre son bulur ve hastalık, klinik belirti vermeyen ancak serolojinin pozitif kaldığı **Latent Sifiliz** evresine giriş yapar.

> Sekonder sifiliz lezyonları tedavi edilmese bile aylarca sürmez, kendiliğinden iyileşir. Bu 'yalancı iyileşme', hastalığın tanınmasını geciktiren ve gizli (latent) hasar dönemine geçişi sağlayan kritik bir adımdır.""",
        elements=[
            make_cloze("Sekonder sifiliz belirtileri (döküntüler, LAP) tedavi verilmese dahi birkaç hafta veya ay içinde {{spontan}} (kendi kendine) gerileyerek kaybolur."),
            make_cloze("Sekonder bulguların tamamen ortadan kalkmasıyla hastalık iyileşmez, klinik olarak sessiz ancak serolojik olarak aktif olan {{Latent}} sifiliz evresine geçer."),
            make_table(
                headers=["Klinik Durum", "Doğal Seyir (Tedavisiz)"],
                rows=[
                    ["Primer Şankr", "Birkaç hafta içinde spontan iyileşir, skarsız veya ince bir skar bırakır"],
                    ["Sekonder Lezyonlar", "3-12 hafta içinde tamamen kaybolur, iz bırakmaz"],
                    ["Sonraki Aşama", "Asemptomatik (Latent) evre başlar, spiroketler dokularda saklanır"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Sifilizin Doğal Seyri",
                [
                    {"text": "Sekonder sifilize ait döküntü ve lenfadenopatiler, penisilin verilmese de haftalar/aylar içinde kendiliğinden düzelir.", "isLie": False, "explanation": "Doğru, immün kontrol mekanizmaları bulguları geçici olarak baskılar."},
                    {"text": "Bulguların spontan gerilemesi, vücudun T. pallidum'u tamamen temizlediği ve enfeksiyonun tamamen bittiği anlamına gelir.", "isLie": True, "explanation": "Yanlış! Bulguların kaybolması 'iyileşme' değil, klinik olarak sessiz olan 'Latent' evreye geçiştir. Bakteri hala vücuttadır."},
                    {"text": "Sekonder bulguların sönmesiyle hastalık klinik belirti vermeyen ancak kanda antikorların saptandığı latent döneme girer.", "isLie": False, "explanation": "Doğru, latent evrenin tanımı tam olarak budur."}
                ]
            ),
            make_quiz(
                question="Sekonder sifilizin klasik makülopapüler döküntüleri olan bir hasta doktora gitmemiş ve antibiyotik kullanmamıştır. Yaklaşık 2 ay sonra döküntülerin tamamen geçtiği görülmüştür. Bu hastanın mevcut durumu için en doğru tıbbi değerlendirme nedir?",
                options=[
                    "Bağışıklık sistemi bakteriyi tamamen yok etmiştir, hasta artık sağlıklıdır",
                    "Hastalık artık bulaştırıcı olamaz ve hiçbir organına zarar vermez",
                    "Enfeksiyon spontan gerileme göstermiş olup Latent Sifiliz evresine geçiş yapmıştır",
                    "Kanda hiçbir sifiliz antikoru (VDRL/TPHA) tespit edilemez hale gelmiştir",
                    "Bir hafta içinde döküntüler eskisinden 10 kat daha şiddetli olarak kalıcı şekilde geri döner"
                ],
                answer="Enfeksiyon spontan gerileme göstermiş olup Latent Sifiliz evresine geçiş yapmıştır",
                explanation="Sekonder sifiliz lezyonları tedavisiz iyileşme eğilimindedir, bu da enfeksiyonun bir sonraki (sessiz/latent) aşamaya geçtiğini gösterir, hastalık sonlanmış sayılmaz."
            )
        ]
    ))

    # Slide 30
    slides.append(make_slide(
        title="[TEKRAR SAYFASI - CHECKPOINT 3] Sekonder Sifilizin Sistemik ve Organ Tutulumları",
        narrative="""Sekonder sifilizin sistemik ve organ tutulumlarını gözden geçirelim:

* **Lenfatik Sistem:** Yaygın, ağrısız lenfadenopati görülür. Özellikle dirsekteki **epitroklear LAP**, sekonder sifiliz için neredeyse patognomoniktir.
* **Sistemik Semptomlar:** Ateş, kırgınlık, farenjit ve kilo kaybı gibi non-spesifik influenza benzeri belirtiler sıktır.
* **İskelet Sistemi:** Eklemlerde artralji, kemiklerde osteit ve periosteit yapar. Şiddetli kemik ağrıları tipik olarak geceleri (uykuda) artar.
* **Karaciğer (Sifilitik Hepatit):** Asemptomatik olabilse de, transaminazlara oranla izole veya belirgin şekilde aşırı yüksek **Alkalen Fosfataz (ALP)** ile karakterizedir.
* **Göz Tutulumu:** En sık üveit yapar. Fotofobi ve görme kaybına neden olabilir; agresif SSS (nörosifiliz) tedavisi gerektirir.
* **Böbrek Tutulumu:** İmmün kompleks birikimine (membranöz nefropati) bağlı geri dönüşümlü **nefrotik sendrom** oluşturur.
* **Merkezi Sinir Sistemi (Erken Nörosifiliz):** Akut aseptik menenjit kliniği verir. Ense sertliği ve Kranial sinir (özellikle 2, 7, 8) felçlerine yol açar.
* **Doğal Seyir:** Tüm bu yaygın klinik tablo, tedavi edilmese bile 3-12 hafta içinde spontan geriler ve hastalık sessiz 'Latent' evreye geçer.""",
        elements=[
            make_cloze("Dirsek bölgesindeki lenf nodlarının büyümesi olan {{epitroklear}} LAP, sekonder sifiliz tanısında oldukça değerlidir."),
            make_cloze("Sifilitik hepatitin laboratuvar yansımasında transaminazlara kıyasla en belirgin yükselen enzim {{Alkalen Fosfataz}}'dır (ALP)."),
            make_table(
                headers=["Organ / Sistem", "Sekonder Sifilizdeki Klasik Tutulumu"],
                rows=[
                    ["Lenf Nodları", "Yaygın ağrısız LAP, Epitroklear LAP"],
                    ["Kemik", "Periosteit (geceleri artan kemik ağrısı)"],
                    ["Böbrek", "İmmün kompleks nefriti, Nefrotik Sendrom"],
                    ["Göz", "Üveit (Bulanık görme, fotofobi)"],
                    ["Merkezi Sinir Sistemi", "Akut aseptik menenjit ve kraniyal sinir felçleri"]
                ]
            ),
            make_recall(
                "Sekonder sifiliz tedavisi verilmeyen bir hastada mevcut yaygın döküntüler ve sistemik bulgular yıllarca sürmeye devam eder mi?",
                "Hayır, etmez. Bulgular tıbbi tedavi verilmese bile 3 ila 12 hafta içinde spontan olarak (kendi kendine) kaybolur ve hastalık latent evreye geçer."
            ),
            make_quiz(
                question="Sekonder sifiliz ile ilişkili organ tutulumları hakkındaki eşleştirmelerden hangisi yanlıştır?",
                options=[
                    "Kemik tutulumu - Geceleri artan osteokopik ağrı",
                    "Göz tutulumu - Sadece basit konjonktivit, tedavi gerektirmez",
                    "Karaciğer tutulumu - ALP yüksekliği ile giden sifilitik hepatit",
                    "Böbrek tutulumu - İmmün kompleks birikimli nefrotik sendrom",
                    "BOS tutulumu - 7. ve 8. kraniyal sinirleri etkileyen aseptik menenjit"
                ],
                answer="Göz tutulumu - Sadece basit konjonktivit, tedavi gerektirmez",
                explanation="Göz tutulumu genellikle basit bir konjonktivit değil, üveit, optik nörit veya retinit tablosudur ve mutlaka nörosifiliz eşdeğeri olarak yüksek doz IV penisilin ile tedavi edilmelidir."
            )
        ]
    ))

    return slides
