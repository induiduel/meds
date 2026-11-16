# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-19-s81",
        "title": "46,XX CGB Etiyolojisi ve Konjenital Adrenal Hiperplaziye Giriş",
        "content": "Karyotipi 46,XX olan genetik bir kız bebekte kuşkulu genitalya veya virilizasyon saptanması durumunda akla gelen en kritik tablo **Konjenital Adrenal Hiperplazidir (KAH)** (Sınav Spotu):\n\n- **Epidemiyolojik Ağırlık:**\n  - 46,XX kuşkulu genitalya vakalarının **en sık nedeni (%90'dan fazlası)** KAH'tır.\n  - Canlı doğumlarda klasik formların sıklığı yaklaşık 1/10.000 ila 1/15.000 arasındadır.\n- **Kalıtım:** KAH'a yol açan tüm enzim defektleri **otozomal resesif (OR)** geçişlidir.\n- **Temel Prensip:**\n  - Fetus genetik olarak kızdır (46,XX); gonadlar **normal overlerdir** ve Sertoli hücresi bulunmadığı için AMH salgılanmaz.\n  - Bu nedenle içte **uterus, fallop tüpleri ve üst vajina tamamen normaldir**.\n  - Ancak fetal adrenal korteksten kontrolsüz salgılanan aşırı androjenler dış genital taslakları (klitoris, labioskrotal kabartı) erkeksi yönde virilize eder.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "İç Genital Anatomi vs Dış Genital Anatomi (KAH 46,XX)",
                "İç Genital Organlar (Normal Dişi)",
                "AMH olmadığı için Müller korunur; uterus ve tüpler mevcuttur; overler normal folikül içerir.",
                "Dış Genital Organlar (Virilize)",
                "Aşırı adrenal androjen nedeniyle klitoris büyür (klitoromegali) ve labialar kaynaşır (skrotumlaşır)."
            ),
            make_cloze(
                "46,XX karyotipli yenidoğanlarda kuşkulu genitalyanın ve aşırı virilizasyonun en sık nedeni konjenital adrenal hiperplazi hastalığıdır.",
                "konjenital adrenal hiperplazi",
                "Adrenal steroidogenez bozukluğuyla seyreden en yaygın 46,XX CGB nedeni"
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-19-s82",
        "title": "21-Hidroksilaz (CYP21A2) Eksikliği: Biyokimyasal Blok",
        "content": "KAH olgularının ezici çoğunluğu tek bir enzimin genetik yetersizliğinden kaynaklanır (Sınav Spotu):\n\n- **Enzimatik İstatistik:** Tüm KAH vakalarının **%90 ila 95'inden tek başına 21-Hidroksilaz enzim eksikliği** sorumludur.\n- **Genetik Lokus:** 6. kromozomun kısa kolunda (6p21.3) HLA kompleksinin içinde yer alan **CYP21A2** genindeki mutasyonlara bağlıdır (yanı başındaki psödogen CYP21A1P ile hatalı rekombinasyonlar sıktır).\n- **Biyokimyasal Blokajın Yeri:**\n  - 21-hidroksilaz enzimi iki temel yolu katalizler:\n    1. Glukokortikoid yolu: **17-OH Progesteron $\\to$ 11-Deoksikortizol** basamağını,\n    2. Mineralokortikoid yolu: **Progesteron $\\to$ 11-Deoksikortikosteron** basamağını.\n- **Sonuç:** Bu enzimin yokluğunda hem **Kortizol** hem de **Aldosteron** sentezi tıkanır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "21-Hidroksilaz Blokajı ve Taşma Mekanizması",
                [
                    "1. Genetik Kusur: 6p21.3'teki CYP21A2 geninde mutasyon veya delesyon.",
                    "2. Enzim Yokluğu: 21-hidroksilaz enzimi sentezlenemez veya inaktiftir.",
                    "3. Blokaj: Progesteron ve 17-OH progesteron sonraki basamağa aktarılamaz.",
                    "4. Kortizol ve Aldosteron Düşüşü: Yaşamsal steroidlerin üretimi durur.",
                    "5. Ön Kümülüs Taşması: Biriken öncüller sağlam olan androjen yoluna kayar."
                ]
            ),
            make_quiz(
                "Konjenital adrenal hiperplazi vakalarının %90-95'inden sorumlu olan ve kromozom 6p21.3 lokusunda kodlanan enzim hangisidir?",
                [
                    {"key": "A", "text": "21-Hidroksilaz (CYP21A2)", "isCorrect": True, "explanation": "Doğru cevap A'dır: KAH'ın en sık nedeni 21-hidroksilaz enzim eksikliğidir (%90-95)."},
                    {"key": "B", "text": "11β-Hidroksilaz (CYP11B1)", "isCorrect": False, "explanation": "11β-hidroksilaz vakaların yaklaşık %5'ini oluşturur."},
                    {"key": "C", "text": "5α-Redüktaz (SRD5A2)", "isCorrect": False, "explanation": "5α-redüktaz adrenal değil periferik enzimdir ve 46,XY CGB nedenidir."},
                    {"key": "D", "text": "Aromataz (CYP19A1)", "isCorrect": False, "explanation": "Aromataz eksikliği nadir bir fetoplasental tablodur."}
                ]
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-19-s83",
        "title": "Negatif Geri Besleme Kaybı: ACTH Patlaması ve Adrenal Hiperplazi",
        "content": "KAH patolojisinin kalbinde hipofiz-adrenal eksenindeki negatif geri besleme mekanizmasının çöküşü yatar (Sınav Spotu):\n\n- **Normal Fizyoloji:** Dolaşımdaki kortizol, hipotalamustan CRH ve hipofiz ön lobundan ACTH salgılanmasını frenler.\n- **KAH'taki Kısır Döngü:**\n  - Kortizol sentezlenemeyince hipofiz üzerindeki negatif geri besleme freni tamamen kalkar.\n  - Hipofiz bezi adrenal korteksi zorlamak için devasa miktarlarda **ACTH (Adrenokortikotropik Hormon)** salgılar.\n  - Sürekli yüksek ACTH uyarısı, adrenal korteksin zona fasikülata ve zona retikülaris tabakalarında masif hücresel hipertrofi ve proliferasyona yol açar (**Adrenal Hiperplazi**).\n- **Androjen Sentezine Sapma:**\n  - Adrenal bez büyür ve kolesterolü içeri pompalar ancak 21-hidroksilaz tıkalı olduğu için kortizol yine üretilemez.\n  - Tüm bu aşırı öncül havuzu (pregnenolon, progesteron), açık olan tek yola, yani **zona retikülaristeki androjen sentez yoluna (DHEA ve Androstenedion)** zorla yönlendirilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Normal Adrenal Aks vs KAH'ta Negatif Geri Besleme Kaybı",
                "Normal Adrenal Eksen",
                "Yeterli kortizol ACTH salgısını sınırlar; adrenal bez normal boyutunda dengeli çalışır.",
                "KAH Adrenal Ekseni",
                "Kortizol yokluğu $\\to$ Aşırı ACTH $\\to$ Adrenal bezde devasa hiperplazi ve kontrolsüz androjen patlaması."
            ),
            make_cloze(
                "Konjenital adrenal hiperplazide kortizol eksikliği nedeniyle hipofizden aşırı salgılanan ACTH hormonu adrenal korteksin büyümesini ve aşırı androjen üretimini tetikler.",
                "ACTH",
                "Kortizol negatif geri beslemesi kalktığında hipofizden kontrolsüzce salgılanan adrenokortikotropik hormon"
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-19-s84",
        "title": "17-OH Progesteron Birikimi ve Androjen Taşması",
        "content": "21-hidroksilaz blokajının en karakteristik laboratuvar belirteci **17-Hidroksiprogesteron (17-OHP)** birikimidir (Sınav Spotu):\n\n- **17-OHP Birikimi:**\n  - Enzim bloğunun hemen yukarısındaki 17-OH progesteron kanda normalin onlarca, hatta yüzlerce katına çıkar.\n  - Yenidoğan topuk kanı tarama programlarında (Guthrie testi) KAH için bakılan **birincil tarama belirteci 17-OHP düzeyidir**.\n- **Androjenik Taşma Yolu:**\n  - 17-OH progesteron ve 17-OH pregnenolon, 17,20-liyaz (CYP17A1) enzimi tarafından **DHEA** ve **Androstenediona** çevrilir.\n  - Bu zayıf androjenler periferik dokularda ve fetal karaciğerde **Testosteron** ve ardından **DHT**'ye dönüştürülür.\n- **Kız Fetus Üzerindeki Etki:**\n  - 8-12. gebelik haftalarında plasentayı ve fetal dolaşımı basan bu yüksek testosteron/DHT dalgası, 46,XX kız fetusun genital tüberkülünü ve labioskrotal kabartılarını erkeksi yönde virilize eder (klitoromegali, labial füzyon).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Biyokimyasal Parametre", "21-Hidroksilaz Eksikliğindeki Değişim", "Klinik / Tanısal Anlamı"],
                [
                    ["17-OH Progesteron", "Aşırı Yüksek (Yüzlerce kat)", "Yenidoğan topuk kanı taramasının altın standart belirteci"],
                    ["Kortizol", "Düşük / Yetersiz", "Stres yanıtı yokluğu, hipoglisemi, hipotansiyon"],
                    ["Aldosteron", "Düşük (Tuz kaybettirici formda)", "Hiponatremi, hiperkalemi, dehidratasyon, şok"],
                    ["Androstenedion / Testosteron", "Aşırı Yüksek", "46,XX fetusta kuşkulu genitalya ve virilizasyon"]
                ]
            ),
            make_quiz(
                "Yenidoğan tarama programlarında konjenital adrenal hiperplazi (21-hidroksilaz eksikliği) şüphesinde kanda bakılan en duyarlı birincil biyokimyasal tarama belirteci hangisidir?",
                [
                    {"key": "A", "text": "17-Hidroksiprogesteron (17-OHP)", "isCorrect": True, "explanation": "Doğru cevap A'dır: 21-hidroksilaz enzim bloğunun hemen önünde biriken 17-OHP, KAH tanısında ve taramasında kullanılan temel parametredir."},
                    {"key": "B", "text": "Dihidrotestosteron (DHT)", "isCorrect": False, "explanation": "DHT tarama belirteci değildir."},
                    {"key": "C", "text": "TSH", "isCorrect": False, "explanation": "TSH hipotiroidi taramasında kullanılır."},
                    {"key": "D", "text": "İnsülin", "isCorrect": False, "explanation": "İnsülinin KAH taramasıyla ilgisi yoktur."}
                ]
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-19-s85",
        "title": "Klasik Form I: Tuz Kaybettirici Form (%75) ve Neonatal Kriz",
        "content": "21-hidroksilaz eksikliği klinik şiddetine göre iki klasik forma ayrılır; en ağırı **Tuz Kaybettirici (Salt-wasting) Formdur** (Sınav Spotu):\n\n- **Görülme Oranı:** Klasik KAH vakalarının yaklaşık **%75'ini** oluşturur.\n- **Moleküler Temel:** Enzim aktivitesi neredeyse sıfırdır (<%1-2); büyük gen delesyonları veya intron 2 splice mutasyonları tipiktir.\n- **Aldosteron Yokluğu:** 21-hidroksilaz tamamen çalışmadığı için aldosteron hiç üretilemez.\n- **Tuz Kaybı Krizi (Hayatı Tehdit Eden Acil):**\n  - Doğumdan sonraki **7 ila 14. günlerde** bebekte beslenememe, fışkırır tarzda kusma, kilo kaybı ve ağır dehidratasyon başlar.\n  - Laboratuvarda: Şiddetli **Hiponatremi (düşük sodyum)**, **Hiperkalemi (yüksek potasyum)**, metabolik asidoz ve hipoglisemi gelişir.\n  - Tedavi edilmezse kardiyak arrest, hipovolemik şok ve **neonatal ölümle** sonuçlanır.\n- **Erkek Bebek Riski:** Kız bebek kuşkulu genitalya nedeniyle erken fark edilirken, erkek bebeğin dış genitalyası normal göründüğü için tanı gecikebilir ve krizle acile gelir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Tuz Kaybettirici Form (%75) vs Basit Virilizan Form (%25)",
                "Tuz Kaybettirici Form (%75)",
                "Aldosteron da üretilemez; hayatın 1-2. haftasında hiponatremi, hiperkalemi ve ölümcül tuz krizi gelişir.",
                "Basit Virilizan Form (%25)",
                "Kısmi aldosteron sentezi korunmuştur (%1-5 aktivite); tuz kaybı krizi olmaz, sadece virilizasyon görülür."
            ),
            make_cloze(
                "Klasik KAH'ın tuz kaybettirici formunda aldosteron eksikliğine bağlı olarak kanda hiponatremi ve hiperkalemi ile seyreden hayatı tehdit edici adrenal kriz gelişir.",
                "hiperkalemi",
                "Tuz kaybı krizinde serum potasyum düzeyinin tehlikeli biçimde yükselmesi"
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-19-s86",
        "title": "Klasik Form II: Basit Virilizan Form (%25) ve Maskülinizasyon",
        "content": "Klasik 21-hidroksilaz eksikliğinin ikinci formu **Basit Virilizan (Simple virilizing)** tablodur (Sınav Spotu):\n\n- **Görülme Oranı:** Klasik vakaların yaklaşık **%25'ini** oluşturur.\n- **Moleküler Temel:** Enzim aktivitesi %1 ila 5 civarındadır (en sık ekzon 4 p.I172N mutasyonu).\n- **Mineralokortikoid Korunumu:** Bu küçük rezidüel enzim aktivitesi, tuz kaybı krizini önleyecek kadar aldosteron sentezlenmesine izin verir; yani hastada **hiponatremi ve şok tablosu görülmez**.\n- **Fetal Virilizasyon:** Ancak kortizol ve androjen yolağı yine bozuktur; aşırı androjen üretimi devam eder:\n  - 46,XX kız bebeklerde doğumda belirgin **klitoromegali, labioskrotal füzyon ve ürogenital sinüs anomalisi (Prader Evre 1-4)** saptanır.\n- **Postnatal Seyir (Tedavisiz Kalırsa):**\n  - Çocuklukta aşırı androjen nedeniyle boy uzaması hızlanır ancak epifiz plakları erken kapanır; nihai erişkin boy **belirgin şekilde kısa kalır**.\n  - Her iki cinste de **erken yalancı puberte (psödopuberte prekoks)** gelişir (pubik/aksiller kıl erken çıkar ancak testisler/overler büyümez).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["KAH Formu", "21-OH Enzim Aktivitesi", "Tuz Kaybı / Kriz", "Dış Genitalya (46,XX)"],
                [
                    ["Tuz Kaybettirici", "<%1 (Sıfıra yakın)", "Var (Ölümcül hiponatremi/hiperkalemi)", "İleri derecede virilize (Prader 3-5)"],
                    ["Basit Virilizan", "%1 - %5 (Rezidüel)", "Yok (Aldosteron dengede)", "Virilize / Kuşkulu (Prader 1-4)"],
                    ["Non-Klasik (Geç)", "%20 - %50 (Hafif azalmış)", "Yok", "Doğumda tamamen normal dişi"]
                ]
            ),
            make_quiz(
                "Doğumda kuşkulu genitalya (klitoromegali ve labial füzyon) saptanan 46,XX bir bebekte yapılan tetkiklerde elektrolitlerin (sodyum ve potasyum) tamamen normal olduğu görülüyor. En olası KAH formu hangisidir?",
                [
                    {"key": "A", "text": "Klasik Basit Virilizan Form", "isCorrect": True, "explanation": "Doğru cevap A'dır: Basit virilizan formda rezidüel aldosteron aktivitesi sayesinde tuz kaybı krizi ve elektrolit bozukluğu görülmez, yalnızca virilizasyon tablosu oluşur."},
                    {"key": "B", "text": "Klasik Tuz Kaybettirici Form", "isCorrect": False, "explanation": "Tuz kaybettirici formda ağır hiponatremi ve hiperkalemi bulunur."},
                    {"key": "C", "text": "Non-klasik Form", "isCorrect": False, "explanation": "Non-klasik formda doğumda kuşkulu genitalya görülmez, genitalya normaldir."},
                    {"key": "D", "text": "Komplet Androjen Duyarsızlığı", "isCorrect": False, "explanation": "CAIS'te karyotip 46,XY'dir ve klitoromegali yoktur."}
                ]
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-19-s87",
        "title": "Non-Klasik (Geç Başlangıçlı) KAH: Hirsutizm ve Oligomenore",
        "content": "21-hidroksilaz eksikliğinin toplumda en sık görülen hafif varyantı **Non-Klasik (Geç Başlangıçlı / Attenuated) KAH** tablosudur (Sınav Spotu):\n\n- **Epidemiyoloji:** Oldukça sıktır; genel popülasyonda 1/1000, Aşkenaz Yahudilerinde ve Akdeniz havzasında 1/100 ila 1/200 sıklığa ulaşır.\n- **Moleküler Temel:** Enzim aktivitesi %20 ila %50 düzeyindedir (en sık ekzon 7 p.V281L nokta mutasyonu).\n- **Doğumdaki Durum:** Doğumda hiçbir genital anomali veya virilizasyon yoktur; bebek **tamamen normal dişi dış genitalyası ile doğar**.\n- **Ergenlik ve Erişkinlik Bulguları:**\n  - Adrenal androjen fazlalığı ergenlik döneminde veya genç kadınlıkta klinik verir:\n  - **Şiddetli ve tedaviye dirençli akne**,\n  - **Hirsutizm (erkek tipi aşırı kıllanma)**,\n  - **Oligomenore veya amenore (adet düzensizliği)**,\n  - Temporal saç dökülmesi ve subfertilite.\n- **Polikistik Over Sendromu (PCOS) ile Karışma:** Klinik olarak PCOS'u birebir taklit eder; ayırıcı tanıda sabah açlık **17-OHP düzeyi veya ACTH stimülasyon testi** ile KAH ekarte edilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Klasik KAH vs Non-Klasik KAH",
                "Klasik KAH (Doğumda Belirgin)",
                "Enzim <%5'tir; doğumda kuşkulu genitalya veya neonatal tuz kaybı krizi ile acil klinik verir.",
                "Non-Klasik KAH (Ergenlikte Belirgin)",
                "Enzim %20-50'dir; doğumda normaldir; ergenlikte akne, hirsutizm ve adet düzensizliği (PCOS benzeri) ile gelir."
            ),
            make_cloze(
                "Doğumda normal genitalyaya sahip olan ancak ergenlikte hirsutizm ve oligomenore ile kliniğe başvuran hafif 21-hidroksilaz eksikliği tablosuna non-klasik KAH denir.",
                "non-klasik KAH",
                "Geç başlangıçlı ve PCOS'u taklit eden hafif konjenital adrenal hiperplazi varyantı"
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-19-s88",
        "title": "Diğer Enzim Defektleri: 11β-Hidroksilaz, 3β-HSD ve POR",
        "content": "KAH olgularının geri kalan %5-10'luk kısmını diğer adrenal steroidogenez enzimlerinin genetik mutasyonları oluşturur (Sınav Spotu):\n\n- **11β-Hidroksilaz (CYP11B1) Eksikliği (%5-8):**\n  - 8q24 kromozomundadır; 11-deoksikortizol ve **11-Deoksikortikosteron (DOC)** birikir.\n  - DOC güçlü bir mineralokortikoiddir; bu nedenle tuz kaybı olmaz, tam aksine **tuz tutulumu ve şiddetli HİPERTANSİYON** gelişir.\n  - 46,XX kızda virilizasyon + hipertansiyon tipiktir.\n- **3β-Hidroksisteroid Dehidrogenaz Tip 2 (HSD3B2) Eksikliği:**\n  - Erken steroid basamağını bloke eder; tüm steroidler (aldosteron, kortizol, androjenler) bozulur.\n  - **Her iki cinste de kuşkulu genitalya** yapar (kızda DHEA fazlalığıyla hafif virilizasyon, erkekte testosteron yokluğuyla yetersiz maskülinizasyon) + ağır tuz kaybı.\n- **P450 Oksiredüktaz (POR) Eksikliği (Antley-Bixler Sendromu):**\n  - Elektron transfer edici POR mutasyonudur; hem CYP21A2 hem CYP17A1 bozulur.\n  - **Her iki cinste de kuşkulu genitalya** + kraniyosinostoz ve iskelet malformasyonları görülür; gebelikte anneyi de virilize eder.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Enzim Defekti", "Kromozom / Gen", "Kan Basıncı / Tuz", "Dış Genitalya Tablosu"],
                [
                    ["21-Hidroksilaz", "6p21 (CYP21A2)", "Tuz kaybı / Hipotansiyon", "46,XX virilize, 46,XY normal"],
                    ["11β-Hidroksilaz", "8q24 (CYP11B1)", "DOC artışı $\\to$ HİPERTANSİYON", "46,XX virilize, 46,XY normal"],
                    ["3β-HSD Tip 2", "1p12 (HSD3B2)", "Ağır tuz kaybı", "Hem 46,XX hem 46,XY Kuşkulu Genitalya"],
                    ["POR Defekti", "7q11 (POR)", "Değişken", "Hem 46,XX hem 46,XY Kuşkulu + İskelet anomalisi"]
                ]
            ),
            make_quiz(
                "Kuşkulu genitalya ile doğan 46,XX bir bebekte yapılan incelemede hipertansiyon ve hipokalemi saptanıyor. En olası enzim eksikliği hangisidir?",
                [
                    {"key": "A", "text": "11β-Hidroksilaz (CYP11B1) Eksikliği", "isCorrect": True, "explanation": "Doğru cevap A'dır: 11β-hidroksilaz eksikliğinde biriken 11-deoksikortikosteron (DOC) mineralokortikoid reseptörlerini uyararak hipertansiyon ve hipokalemiye yol açar."},
                    {"key": "B", "text": "21-Hidroksilaz Eksikliği", "isCorrect": False, "explanation": "21-hidroksilazda tuz kaybı ve hipotansiyon olur."},
                    {"key": "C", "text": "5α-Redüktaz Eksikliği", "isCorrect": False, "explanation": "5α-redüktaz 46,XY bireylerde görülür ve hipertansiyon yapmaz."},
                    {"key": "D", "text": "Aromataz Eksikliği", "isCorrect": False, "explanation": "Aromataz eksikliğinde hipertansiyon tipik bulgu değildir."}
                ]
            )
        ]
    })

    # Slide 89 - CHECKPOINT 9
    slides.append({
        "id": "k1-19-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Konjenital Adrenal Hiperplazi ve 21-Hidroksilaz",
        "content": "Bu checkpointte Konjenital Adrenal Hiperplazinin kritik noktalarını özetliyoruz:\n\n- **Epidemiyoloji:** 46,XX kuşkulu genitalyanın **en sık nedeni (%90-95 CYP21A2 eksikliği)**; otozomal resesif geçişlidir.\n- **İç Organlar:** Overler ve **uterus/tüpler tamamen normaldir** (çünkü AMH yoktur).\n- **Patofizyoloji:** Kortizol sentezlenemez $\\to$ Negatif geri besleme kalkar $\\to$ **ACTH aşırı yükselir** $\\to$ Adrenal hiperplazi ve aşırı androjen üretimi.\n- **Laboratuvar Belirteci:** Kanda **17-OH Progesteron** aşırı yükselir; yenidoğan topuk kanında taranır.\n- **Tuz Kaybettirici Form (%75):** Aldosteron üretilemez; hayatın 1-2. haftasında **hiponatremi, hiperkalemi ve ölümcül şok krizi** gelişir.\n- **Basit Virilizan Form (%25):** Rezidüel enzim vardır; tuz kaybı olmaz ancak kız bebekte klitoromegali ve labial füzyon görülür.\n- **Non-Klasik Form:** Doğumda normaldir; ergenlikte akne, hirsutizm ve oligomenore ile gelir (PCOS taklitçisi).\n- **11β-Hidroksilaz:** DOC birikimine bağlı **virilizasyon + HİPERTANSİYON** yapar.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["KAH Formu / Özellik", "Temel Mekanizma", "Kritik Sınav İpucu"],
                [
                    ["CYP21A2 Mutasyonu", "21-hidroksilaz yokluğu", "17-OHP aşırı artışı, KAH'ın %90-95'i"],
                    ["Tuz Kaybettirici Form", "Kortizol + Aldosteron eksikliği", "Hiponatremi, hiperkalemi, neonatal kriz"],
                    ["Basit Virilizan Form", "Kısmi enzim (%1-5), sadece androjen yüksek", "Elektrolitler normal, genitalya kuşkulu"],
                    ["11β-Hidroksilaz Eksikliği", "DOC birikimi", "Virilizasyon ile birlikte HİPERTANSİYON"],
                    ["HSD3B2 ve POR", "Erken yolak / koenzim defekti", "Her iki cinste de (XX ve XY) kuşkulu genitalya"]
                ]
            ),
            make_chain(
                "KAH Patofizyoloji Özet Şeması",
                [
                    "1. CYP21A2 Bloğu: 21-hidroksilaz yokluğu kortizol sentezini durdurur.",
                    "2. Hipofiz Uyarısı: Negatif geri besleme kaybıyla ACTH aşırı yükselir.",
                    "3. Adrenal Hiperplazi: Adrenal korteks büyür ve öncülleri androjene dönüştürür.",
                    "4. Virilizasyon: Fetal testosteron/DHT 46,XX kızda klitoromegali yapar.",
                    "5. Tedavi: Kortizol ve tuz kaybettiricide fludrokortizon replasmanı."
                ]
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-19-s90",
        "title": "Bölüm Özeti: KAH'tan Tanısal Algoritma ve Prenatal Yönetime Geçiş",
        "content": "Bölüm 9 boyunca KAH'ın genetik mekanizmasını (CYP21A2), tuz kaybettirici krizi ve diğer enzim mutasyonlarını inceledik:\n\n- **Özet:** 46,XX kuşkulu genitalyada ilk akla gelmesi gereken acil KAH'tır; erken tanı hayat kurtarır ve gereksiz cerrahiyi önler.\n- **Sonraki Bölüm (Bölüm 10):** KAH'ın gebelikteki **prenatal deksametazon tedavisini**, yenidoğanda kuşkulu genitalyaya adım adım **tanısal yaklaşım algoritmasını ve multidisipliner CGB yönetimini** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "Konjenital adrenal hiperplaziye bağlı tuz kaybı krizinde görülen tipik serum elektrolit kombinasyonu nasıldır?",
                "Hiponatremi ve hiperkalemi",
                "Düşük sodyum ve yüksek potasyum birlikteliği"
            ),
            make_quiz(
                "Aşağıdaki steroid enzim defektlerinden hangisi her iki cinste de (hem 46,XX hem 46,XY bireylerde) kuşkulu genitalyaya yol açar?",
                [
                    {"key": "A", "text": "3β-Hidroksisteroid dehidrogenaz (HSD3B2) eksikliği", "isCorrect": True, "explanation": "Doğru cevap A'dır: HSD3B2 ve POR defektleri hem erkekte testosteron sentezini hem kızda normal steroid dengesini bozarak her iki cinste de kuşkulu genitalya yapar."},
                    {"key": "B", "text": "21-Hidroksilaz eksikliği", "isCorrect": False, "explanation": "21-hidroksilaz sadece 46,XX kızda kuşkulu genitalya yapar, erkek bebek normaldir."},
                    {"key": "C", "text": "11β-Hidroksilaz eksikliği", "isCorrect": False, "explanation": "11β-hidroksilaz sadece 46,XX kızda kuşkulu genitalya yapar."},
                    {"key": "D", "text": "5α-Redüktaz eksikliği", "isCorrect": False, "explanation": "5α-redüktaz sadece 46,XY erkekte kuşkulu genitalya yapar."}
                ]
            )
        ]
    })

    return slides
