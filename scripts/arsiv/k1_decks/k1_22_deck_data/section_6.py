# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 6: Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları (Slayt 51 - 60)
Checkpoint 6: Slayt 59
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_6_slides():
    slides = []

    # Slayt 51: Kolostrum (Ağız Sütü): İlk Aşının Özellikleri
    slides.append({
        "id": "k1-22-s51",
        "title": "Kolostrum (Ağız Sütü): İlk Aşının Özellikleri",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 51,
        "narrative": (
            "Doğumdan sonraki **ilk 4-5 gün boyunca** meme bezlerinden salgılanan koyu kıvamlı, "
            "sarımsı renkli süte **Kolostrum (Ağız Sütü)** adı verilir. "
            "Kolostrum, yenidoğanın rahim dışı dünyaya adaptasyonu için tasarlanmış mucizevi bir konsantredir: "
            "1. **Bileşim:** İlerleyen günlerdeki olgun süte kıyasla **daha az yağ ve daha az laktoz (karbonhidrat)** içerir. "
            "Buna karşın **protein, sodyum, potasyum, klor, çinko, A ve E vitamini** konsantrasyonu çok daha yüksektir. "
            "2. **İmmünolojik Zirve:** Sekretuvar IgA, laktoferrin ve canlı akyuvarlar (makrofajlar) en yüksek konsantrasyondadır; "
            "adeta bebeğin hayatındaki **'ilk aşı'** görevini görür. "
            "3. **Laksatif Etki:** Hafif müshil etkisiyle ilk günlerde bebeğin bağırsaklarındaki yapışkan koyu dışkının "
            "(mekonyum) hızla atılmasını sağlar; bu sayede bilirubin emilimini durdurarak **yenidoğan sarılığı riskini belirgin azaltır**."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Doğumdan sonraki ilk 5 günde salgılanan ve yüksek protein ile sIgA içeren sarımsı ilk süte kolostrum adı verilir.",
                "kolostrum",
                "Bebeğin ilk aşısı niteliğindeki ağız sıvısı"
            ),
            make_table(
                "Kolostrum ile Olgun Sütün Karşılaştırmalı Biyokimyasal Tablosu",
                ["Bileşen / Özellik", "Kolostrum (İlk 5 Gün)", "Olgun Süt (15. Günden Sonra)", "Fizyolojik Amacı"],
                [
                    ["Protein Düzeyi", "Çok Yüksek (~2 - 3 g/100 ml)", "Düşük (~1 g/100 ml)", "Mukozal zırh ve antikor inşası"],
                    ["Yağ ve Karbonhidrat", "Düşük", "Yüksek", "İlk günlerde minik mideyi yormamak"],
                    [
                        "İmmünolojik Faktörler",
                        {"text": "Zirve noktada (sIgA, laktoferrin)", "isMasked": True, "hint": "Antikor ve fagositer hücrelerin maksimum yoğunluğu"},
                        "Daha dengeli / stabil düzeyde",
                        "Dış ortam patojenlerine karşı anında koruma"
                    ],
                    ["Gastrointestinal Etki", "Laksatif (Mekonyum atıcı)", "Besleyici / Büyütücü", "Bilirubin klerensi ve sarılık önleme"]
                ]
            ),
            make_micro_quiz(
                "Doğumdan sonraki ilk günlerde salgılanan kolostrum (ağız sütü) ile ilgili aşağıdakilerden hangisi yanlıştır?",
                {
                    "A": "Olgun süte göre proteinden ve sIgA antikorlarından çok daha zengindir",
                    "B": "Olgun süte göre yağ ve laktoz konsantrasyonu daha düşüktür",
                    "C": "Hafif laksatif etkisiyle mekonyumun atılmasını sağlayarak sarılığı azaltır",
                    "D": "Besleyici değeri olmadığı için sağılıp çöpe dökülmeli ve bebeğe verilmemelidir",
                    "E": "A ve E vitamini gibi yağda eriyen koruyucu vitaminler açısından zengindir"
                },
                "D",
                "Doğru cevap D'dir: Kolostrumun dökülmesi veya çöpe atılması halk sağlığında en ölümcül cehalet hatalarındandır; kolostrum bebeğin ilk aşısıdır, her damlası altın değerindedir ve mutlaka ilk dakikalarda bebeğe verilmelidir."
            )
        ]
    })

    # Slayt 52: Geçiş Sütü ve Olgun Sütün Dinamik Evrimi
    slides.append({
        "id": "k1-22-s52",
        "title": "Geçiş Sütü ve Olgun Sütün Dinamik Evrimi",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 52,
        "narrative": (
            "Anne sütü doğum sonrası günlere göre üç temel evreden geçer: "
            "1. **Kolostrum:** 1. ila 5. günler arası (protein ve antikor zengini, düşük kalori). "
            "2. **Geçiş Sütü (Transitional Milk):** 6. ila 15. günler arası. "
            "Bu ara evrede memelerdeki dolgunluk artar; protein ve immünglobulin konsantrasyonu kademeli olarak azalırken, "
            "yağ, laktoz ve toplam kalori içeriği hızla yükselir. "
            "3. **Olgun Süt (Mature Milk):** 15. günden sütten kesilene kadar süren kalıcı evredir. "
            "Olgun sütün yaklaşık %87'si su, %3.8'i yağ, %7'si laktoz ve %0.9-1.0'ı proteindir. "
            "Olgun süt bebeğin büyümesi için gereken optimal kaloriyi (67 kcal/100 ml) sağlarken, "
            "böbrek solüt yükünü en düşük seviyede tutacak fizyolojik kompozisyona kilitlenir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Doğumdan sonraki 6-15. günler arasında salgılanan ve yağ ile kalorisi artan süte geçiş sütü denir.",
                "geçiş sütü",
                "Kolostrum ile olgun süt arasındaki ara dönem salgısı"
            ),
            make_causal_chain(
                "Anne Sütünün Günler İçindeki Evrim Kaskadı",
                [
                    "1. 1-5. Günler: Kolostrum ile steril bağırsak patojenlere karşı zırhla kaplanır.",
                    "2. 6-15. Günler: Geçiş sütüyle protein düşerken kalori ve yağ katlanarak artar.",
                    "3. 15. Günden İtibaren: Olgun süt ideal %87 su, %3.8 yağ ve %7 laktoz dengesine oturur.",
                    "4. Aylar Boyunca: Süt miktarı bebeğin emme gücüne paralel olarak günde 750-1000 ml'ye ulaşır."
                ]
            ),
            make_active_recall(
                "Kolostrumdan olgun süte geçiş sürecinde sütün temel makro besin ögelerindeki (protein, yağ, laktoz) değişim yönü nasıldır?",
                "Protein konsantrasyonu belirgin şekilde düşerken; yağ, laktoz ve toplam kalori miktarı belirgin şekilde artar.",
                "Protein azalması ile yağ-şeker artışı yönü"
            )
        ]
    })

    # Slayt 53: Ön Süt (Foremilk) ile Son Süt (Hindmilk) Ayrımı
    slides.append({
        "id": "k1-22-s53",
        "title": "Ön Süt (Foremilk) ile Son Süt (Hindmilk) Ayrımı",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 53,
        "narrative": (
            "Anne sütü yalnızca günler içinde değil, **tek bir emzirme seansının dakikaları içinde bile** radikal biçimde değişir: "
            "- **Ön Süt (Foremilk):** Emzirmenin başında memeden ilk gelen süttür. "
            "Daha mavimsi ve sulu bir görünümdedir. "
            "Protein, laktoz, su ve minerallerden zengindir; bebeğin susuzluğunu giderir ve kan şekerini hızla yükseltir. "
            "- **Son Süt (Hindmilk):** Bebek memeyi emmeye devam ettikçe, alveol duvarlarına yapışmış yağ globülleri sütün içine dökülür. "
            "Emzirmenin sonuna doğru sütün **yağ içeriği 4 ila 5 kat, protein içeriği ise %50 oranında artar**! "
            "Son süt kremamsı, beyaz ve son derece kalorilidir; bebeğe tokluk hissi verir ve kilo alımını sağlar. "
            "**Pratik Klinik İlke:** Bebek bir memeyi tamamen boşaltmadan diğer memeye geçirilirse, "
            "yalnızca ön sütü (şekerli suyu) emer; son sütü alamadığı için doyamaz, gaz sancısı çeker ve kilo alamaz!"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Emzirmenin sonuna doğru gelen son sütte yağ oranı dört ila beş kat artarak bebeğe tokluk ve kilo alımı sağlar.",
                "dört ila beş kat",
                "Emzirme seansı sonunda lipit konsantrasyonundaki katlanma oranı"
            ),
            make_before_after(
                "Ön Süt ile Son Sütün Fizyolojik Nitelikleri",
                "Ön Süt (Emzirme Başı)",
                "Suludur, laktoz zenginidir; bebeğin susuzluğunu dindirir, ilk açlığı bastırır ancak çabuk acıktırır.",
                "Son Süt (Emzirme Sonu)",
                "Kremamsıdır, yağ 4-5 kat fazladır; kolesistokinin salgılatarak tokluk hissi yaratır ve kilo aldırır.",
                "Susuzluğu gideren ön süt ile kalori ve tokluk sağlayan son sütün fonksiyonel farkı"
            ),
            make_micro_quiz(
                "Bebeğin emzirilmesi sırasında her iki memeden de sadece 5'er dakika emzirilip memenin tam boşaltılmamasının en olası sonucu nedir?",
                {
                    "A": "Bebek aşırı kilo alarak obeziteye girer",
                    "B": "Bebek sadece yağlı son sütü aldığı için kabızlık gelişir",
                    "C": "Bebek yağdan zengin son sütü alamayarak doyamaz, kilo alımı duraklar ve laktoz yüküyle gaz sancısı çeker",
                    "D": "Memede süt yapımı iki katına çıkar",
                    "E": "Bebekte D vitamini zehirlenmesi gelişir"
                },
                "C",
                "Doğru cevap C'dir: Memeyi tam boşaltmayan bebek sadece karbonhidratlı ön sütü alır; yağlı son sütü alamadığı için tokluk hissi oluşmaz, kilo alamaz ve kolona geçen fazla laktoz fermantasyonla aşırı gaz ve yeşil köpüklü ishale yol açar."
            )
        ]
    })

    # Slayt 54: Prematüre Anne Sütü: Bebeğe Özel Biyolojik Uyarlama
    slides.append({
        "id": "k1-22-s54",
        "title": "Prematüre Anne Sütü: Bebeğe Özel Biyolojik Uyarlama",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 54,
        "narrative": (
            "Anne vücudu gebeliğin kaçıncı haftasında doğum gerçekleşirse, sütünü tam olarak o haftanın "
            "ihtiyaçlarına göre formüle eder! "
            "Erken doğum yapan (prematüre doğuran) bir annenin sütü (**Prematüre Anne Sütü**), "
            "zamanında doğuran bir annenin sütünden belirgin farklılıklar gösterir: "
            "1. **Yüksek Protein:** Prematüre bebeğin hızlı yakalama büyümesi (catch-up growth) için protein içeriği çok daha yüksektir. "
            "2. **Yüksek Sodyum ve Klor:** Prematüre böbrek tübülleri sodyumu geri ememez (tübüler immatürite); "
            "prematüre sütü yüksek sodyum ve klor içeriğiyle hiponatremi gelişimini önler. "
            "3. **Düşük Laktoz:** Prematüre bağırsakta laktaz aktivitesi düşüktür; sütteki laktoz oranı term süte göre daha düşüktür. "
            "4. **Yüksek sIgA, Laktoferrin ve Büyüme Faktörü (EGF):** Prematüreyi nekrotizan enterokolit (NEK) "
            "ve hastane sepsisi gibi ölümcül tablolardan korumak için koruyucu etmenler tavan yapmıştır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Prematüre doğuran annelerin sütü term süte göre protein, sodyum ve klor açısından daha zengin, laktoz açısından daha düşüktür.",
                "protein, sodyum ve klor",
                "Erken doğan bebeğin böbrek kaybını ve büyüme ihtiyacını karşılayan zengin maddeler"
            ),
            make_table(
                "Prematüre Anne Sütü ile Term Anne Sütünün Karşılaştırması",
                ["Biyokimyasal Parametre", "Prematüre Anne Sütü", "Term Anne Sütü", "Prematüreye Sağlanan Üstünlük"],
                [
                    ["Protein Yoğunluğu", "Belirgin Yüksek", "Standart (~1 g/100 ml)", "Hızlı doku inşası ve yakalama büyümesi"],
                    [
                        "Sodyum ve Klor Düzeyi",
                        {"text": "Daha yüksektir", "isMasked": True, "hint": "İmmatür böbreğin idrarla tuz kaybını telafi eden düzey"},
                        "Daha düşüktür",
                        "Tübüler tuz kaybına bağlı hiponatremiyi önleme"
                    ],
                    ["Laktoz Konsantrasyonu", "Daha düşüktür", "Yüksek (%7)", "İmmatür laktaz enzimine aşırı yük bindirmeme"],
                    ["EGF ve İmmün Faktörler", "Maksimum düzeyde", "Yüksek", "Nekrotizan enterokolit (NEK) koruması"]
                ]
            ),
            make_active_recall(
                "Prematüre bir bebeğe term anne sütü veya inek sütü yerine kendi öz annesinin sütünün verilmesinin en kritik nefrolojik gerekçesi nedir?",
                "Prematüre bebeğin böbreklerinden idrarla tuz kaybetmesi nedeniyle, kendi annesinin sütünün yüksek sodyum ve klor içermesi ve hiponatremiyi engellemesidir.",
                "Tübüler tuz kaybı ve sodyum dengesi"
            )
        ]
    })

    # Slayt 55: Emzirmenin Anne Sağlığına Faydaları I: Uterus İnvolüsyonu
    slides.append({
        "id": "k1-22-s55",
        "title": "Emzirmenin Anne Sağlığına Faydaları I: Uterus İnvolüsyonu",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 55,
        "narrative": (
            "Emzirme yalnızca bebeği besleyen bir eylem değil, aynı zamanda **annenin lohusalık iyileşmesini yöneten nöroendokrin bir mekanizmadır**: "
            "1. **Oksitosin Salınımı ve Uterus İnvolüsyonu:** "
            "Bebek meme ucunu emdikçe, duyusal sinirler hipotalamusu uyarır ve arka hipofizden bol miktarda **Oksitosin** salgılanır. "
            "Oksitosin hem meme alveollerindeki miyoepitelyal hücreleri kasarak sütü fışkırtır (let-down refleksi), "
            "hem de uterustaki miyometriyum kas liflerini güçlü şekilde kasar. "
            "Bu kasılmalar plasenta yatağındaki açık kan damarlarını mekanik olarak sıkar ve **postpartum hemorajiyi (doğum sonu kanamayı) durdurur**. "
            "Uterusun eski gebelik öncesi boyutuna hızla küçülmesini (involüsyon) sağlar. "
            "2. **Hızlı Kilo Kaybı:** Süt üretimi günde yaklaşık 500-600 ek kalori yakar; "
            "emziren anne gebelikte depoladığı yağları hızla eriterek eski kilosuna çok daha çabuk döner."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Emzirme sırasında arka hipofizden salgılanan oksitosin uterusu kasarak doğum sonu kanamayı durdurur ve involüsyonu hızlandırır.",
                "oksitosin",
                "Miyometriyum kasılmasını ve süt fışkırtmasını sağlayan nörohormon"
            ),
            make_causal_chain(
                "Meme Uyarımından Postpartum Kanama Kontrolüne Nöroendokrin Zincir",
                [
                    "1. Meme Başı Uyarımı: Bebeğin emme hareketi meme areolasındaki mekanoreseptörleri tetikler.",
                    "2. Nöral İleti: Uyarı medulla spinalis üzerinden hipotalamus supraoptik/paraventriküler çekirdeklere ulaşır.",
                    "3. Oksitosin Deşarjı: Arka hipofizden pulsatil oksitosin dolaşıma dökülür.",
                    "4. Miyometriyum Kasılması: Uterus kas lifleri plasenta arterlerini boğarak kanamayı durdurur."
                ]
            ),
            make_active_recall(
                "Doğumdan hemen sonra bebeğin memeye tutulmasının maternal kanama kontrolündeki temel farmakolojik/fizyolojik etkisi nedir?",
                "Oksitosin salınımını tetikleyerek uterus miyometriyumunu kasması ve plasenta ayrılma yüzeyindeki kan damarlarını mekanik olarak sıkıştırıp kanamayı kesmesidir.",
                "Endojen oksitosin ve hemostaz mekanizması"
            )
        ]
    })

    # Slayt 56: Emzirmenin Anne Sağlığına Faydaları II: Meme ve Over Kanseri Koruması
    slides.append({
        "id": "k1-22-s56",
        "title": "Emzirmenin Anne Sağlığına Faydaları II: Meme ve Over Kanseri Koruması",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 56,
        "narrative": (
            "Emzirmenin kadın sağlığı üzerindeki en çarpıcı onkolojik koruyuculuğu meme ve over kanserinde belgelenmiştir: "
            "- **Meme Kanseri Riskinin Azalması:** "
            "Bir kadının yaşamı boyunca toplam emzirdiği her 12 ay, meme kanseri gelişme riskini kümülatif olarak **%4.3 oranında azaltır**! "
            "Laktasyon sırasında meme epitel hücreleri tam terminal diferansiyasyona (olgunlaşmaya) uğrar; "
            "diferansiye hücrelerin karsinojenik mutasyonlara direnci çok daha yüksektir. "
            "- **Over (Yumurtalık) Kanseri Riskinin Azalması:** "
            "Uzun süreli emzirme yapan kadınlarda **over kanseri riski yaklaşık %30 oranında azalır**! "
            "Emzirme prolaktini yükseltip GnRH salınımını baskılayarak ovulasyonu (yumurtlamayı) durdurur (Laktasyonel Amenore). "
            "Yumurtalık yüzey epitelinin her ay çatlayıp tamir olma döngüsü (inatçı ovulasyon hipotezi) baskılandığı için over kanseri engellenir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Uzun süreli emzirme yumurtlama döngüsünü baskılayarak annede over kanseri riskinde yaklaşık yüzde otuz azalma sağlar.",
                "yüzde otuz azalma",
                "Laktasyonun epitelyal over tümörlerine karşı koruma yüzdesi"
            ),
            make_before_after(
                "Emziren ve Emzirmeyen Kadınların Onkolojik Risk Kıyaslaması",
                "Uzun Süre Emziren Kadın",
                "Meme epiteli tam diferansiyedir; ovulasyon baskılandığı için meme ve over kanseri riski belirgin düşüktür.",
                "Emzirmeyen Kadın",
                "Diferansiyasyon eksiktir; kesintisiz ovulatuar mikrotravmalar nedeniyle over ve meme kanseri riski anlamlı yüksektir.",
                "Laktasyonun meme ve over kanserine karşı sunduğu onkolojik koruma ayrımı"
            ),
            make_active_recall(
                "Emzirmenin over (yumurtalık) kanseri riskini yaklaşık %30 oranında azaltmasının altında yatan temel endokrin mekanizma nedir?",
                "Prolaktin yüksekliğinin GnRH ve gonadotropinleri baskılayarak ovulasyonu (yumurtlamayı) durdurması ve yumurtalık yüzey epitelinin çatlama travmasını engellemesidir.",
                "İnatçı ovulasyonun baskılanması ve over koruması"
            )
        ]
    })

    # Slayt 57: Anne İçin Metabolik ve Ruhsal Koruma: Depresyon ve Diyabet
    slides.append({
        "id": "k1-22-s57",
        "title": "Anne İçin Metabolik ve Ruhsal Koruma: Depresyon ve Diyabet",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 57,
        "narrative": (
            "Emzirmenin anneye faydaları sadece üreme organlarıyla sınırlı değildir; ruh sağlığı ve metabolizmayı da kapsar: "
            "1. **Postpartum Depresyonun Azalması:** "
            "Emzirme sırasında pulsatil olarak salgılanan oksitosin ve prolaktin hormonları, annenin limbik sisteminde "
            "anksiyeteyi yatıştırır, kortizol stres yanıtını baskılar, sedasyon ve huzur hissi sağlar. "
            "Emziren annelerde doğum sonu hüzün (baby blues) ve klinik **Postpartum Depresyon anlamlı derecede daha az görülür**. "
            "2. **Metabolik Koruma ve Tip 2 Diyabet:** "
            "Laktasyon insülin duyarlılığını artırır ve glikoz toleransını iyileştirir. "
            "Gebelikte gestasyonel diyabet geçirmiş kadınlarda, bebeğini emzirmek ileriki yıllarda kalıcı **Tip 2 Diyabet gelişme riskini %50'ye varan oranda azaltır**. "
            "Ayrıca romatoid artrit ve hipertansiyon riskini de düşürür."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Emzirme sırasında salgılanan prolaktin ve oksitosin annede anksiyeteyi düşürerek postpartum depresyon riskini belirgin azaltır.",
                "postpartum depresyon",
                "Doğum sonrası annede gelişebilen klinik çökkünlük tablosu"
            ),
            make_table(
                "Emzirmenin Anne Sağlığına Kanıtlanmış Sistemik Faydaları",
                ["Maternal Sistem / Organ", "Emzirme ile Sağlanan Koruma", "Temel Biyolojik Mekanizma"],
                [
                    ["Uterus (Rahim)", "İnvolüsyon ve kanama kontrolü", "Oksitosin ile miyometriyum kasılması"],
                    ["Meme Dokusu", "Meme kanseri riskinde azalma", "Epitel hücrelerinin terminal diferansiyasyonu"],
                    [
                        "Overler (Yumurtalık)",
                        "%30 kanser riski azalması",
                        {"text": "Ovulasyonun laktasyonel baskılanması", "isMasked": True, "hint": "Aylık yumurta çatlamasının prolaktinle durdurulması"}
                    ],
                    ["Ruh Sağlığı", "Postpartum depresyonda azalma", "Oksitosin aracılı anksiyoliz ve bağlanma"],
                    ["Metabolizma", "Tip 2 DM riskinde %50 azalma", "Gelişmiş insülin duyarlılığı ve yağ mobilizasyonu"]
                ]
            ),
            make_active_recall(
                "Gebelikte gestasyonel diyabet geçirmiş bir annenin doğum sonrasında bebeğini uzun süre emzirmesinin en büyük metabolik faydası nedir?",
                "İnsülin duyarlılığını artırarak kadının ileriki yaşamında kalıcı Tip 2 Diyabet geliştirme riskini yaklaşık %50 oranında azaltmasıdır.",
                "Tip 2 diyabete karşı uzun vadeli koruma"
            )
        ]
    })

    # Slayt 58: Anne Sütü İçeriğini Değiştiren Maternal Faktörler
    slides.append({
        "id": "k1-22-s58",
        "title": "Anne Sütü İçeriğini Değiştiren Maternal Faktörler",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 58,
        "narrative": (
            "Anne sütü mükemmel bir biyolojik kompozisyona sahip olmakla birlikte, bazı maternal ve çevresel faktörlerden etkilenir: "
            "1. **Maternal Yaş:** İdeal emzirme yaşı 18 ila 35 yaş arasıdır. 18 yaş altı adölesan gebeliklerde ve 35 yaş üstü ileri maternal yaşta "
            "beslenme depoları ve süt verimi olumsuz etkilenebilir. "
            "2. **Annenin Vücut Depoları ve Beslenmesi:** Annenin yetersiz beslenmesi sütün makro besinlerini (protein, yağ, laktoz) "
            "kolay kolay bozmaz (anne kendi vücut depolarını eriterek sütü korur); fakat **B grubu vitaminler, C vitamini, A vitamini ve iyot** "
            "doğrudan maternal diyetten etkilenir. "
            "3. **Emzirme Döneminde Yeniden Gebelik:** Süt miktarını ve tadını (tuzlu hale gelmesi) değiştirebilir. "
            "4. **İlaçlar ve Toksinler:** Sigara süt hacmini düşürür ve nikotin süte geçer; alkol oksitosin refleksini felç eder; "
            "kemoterapötikler, radyoaktif maddeler ve bazı psikiyatrik ilaçlar emzirmede kontrendikedir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütünün makro besin bileşimi maternal yetersizlikte korunurken suda eriyen vitaminler doğrudan annenin günlük beslenmesini yansıtır.",
                "suda eriyen vitaminler",
                "B ve C grubu annenin diyetine birebir bağımlı bileşikler"
            ),
            make_before_after(
                "Makro Besinler ile Vitaminlerin Maternal Beslenmeye Bağımlılığı",
                "Makro Besinler (Protein, Yağ, Laktoz)",
                "Anne yetersiz beslense bile kendi kemik ve kas depolarını feda ederek sütün kalorisini sabit tutar.",
                "Suda Eriyen Vitaminler (B, C) ve İyot",
                "Depolanamaz; annenin günlük diyet alımını birebir yansıtır; eksiklik doğrudan süte yansır.",
                "Sabit tutulan makro besin kalitesi ile diyete bağımlı mikro besin düzeyleri ayrımı"
            ),
            make_micro_quiz(
                "Anne sütü içeriğini etkileyen faktörler ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Maternal yaşın 18'in altında veya 35'in üstünde olması süt verimini etkileyebilir",
                    "B": "Anne az beslense bile sütündeki protein ve laktoz konsantrasyonu uzun süre sabit tutulur",
                    "C": "Anne sütündeki C ve B grubu vitaminler annenin günlük diyetindeki vitamin alımına bağımlıdır",
                    "D": "Sigara içmek süt miktarını azaltır ve nikotin doğrudan süte geçerek bebeği etkiler",
                    "E": "Annenin beslenmesi bir gün bile aksasa sütteki kalsiyum ve protein tamamen sıfırlanır"
                },
                "E",
                "Doğru cevap E'dir: Anne yetersiz beslendiğinde vücut kendi iskelet ve kas rezervlerini kullanarak sütün temel protein, kalsiyum ve yağ içeriğini bebeği korumak adına sabit tutar; asla bir günde sıfırlanmaz. Diğer seçenekler tamamen doğrudur."
            )
        ]
    })

    # Slayt 59: [TEKRAR SAYFASI - CHECKPOINT 6] Anne Sütünün Evreleri ve Anne Sağlığı
    slides.append({
        "id": "k1-22-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Anne Sütünün Evreleri ve Anne Sağlığı",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 59,
        "narrative": (
            "Bu altıncı checkpoint sayfasında, sütün evrelerini, ön/son süt dinamiklerini ve "
            "emzirmenin anneye sağladığı mucizevi faydaları kilitliyoruz: "
            "1. **Kolostrum (Ağız Sütü):** İlk 5 gün salgılanır; protein, sIgA, laktoferrin ve akyuvar zenginidir; mekonyumu attırarak sarılığı önler. "
            "2. **Geçiş ve Olgun Süt:** 6-15. gün geçiş sütü, 15. günden sonra olgun süt (%87 su, %3.8 yağ, %7 laktoz, %1 protein). "
            "3. **Ön ve Son Süt:** Ön süt susuzluğu giderir; son sütte yağ 4-5 kat artarak tokluk hissi verir ve kilo aldırır. "
            "4. **Prematüre Sütü:** Term süte göre protein, sodyum ve klor zenginidir; tübüler tuz kaybını telafi eder. "
            "5. **Anneye Faydaları:** Oksitosin ile uterus involüsyonu ve kanama kontrolü; meme kanseri azalması; over kanseri riskinde %30 azalma; postpartum depresyonun gerilemesi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "k1-22-fc-16",
                "Doğumdan sonraki ilk 5 günde salgılanan, olgun süte göre proteinden, sIgA'dan ve minerallerden zengin ancak yağ ve şekerden fakir olan ilk süte ne ad verilir?",
                "Kolostrum (Ağız sütü)",
                "Yeni doğan bebeğin ilk aşısı niteliğindeki konsantre sarımsı salgı",
                "Süt Evreleri"
            ),
            make_flashcard(
                "k1-22-fc-17",
                "Bir emzirme seansının sonunda gelen, emzirmenin başına göre yağı 4-5 kat artarak bebeğe tokluk hissi veren süte ne denir?",
                "Son süt (Hindmilk)",
                "Memenin tamamen boşalmasıyla salgılanan kalorili lipid zengini fraksiyon",
                "Süt Evreleri"
            ),
            make_flashcard(
                "k1-22-fc-18",
                "Emzirmenin anne sağlığı üzerindeki onkolojik koruyucu etkilerinde over kanseri riskindeki kanıtlanmış azalma oranı yaklaşık yüzde kaçtır?",
                "Yaklaşık yüzde 30 azalma",
                "Uzun süreli laktasyonun yumurtalık neoplazisine karşı sağladığı gerileme payı",
                "Anne Sağlığı"
            )
        ]
    })

    # Slayt 60: Bölüm Özeti: Süt Evrelerinden İnek Sütü Karşılaştırmasına Geçiş
    slides.append({
        "id": "k1-22-s60",
        "title": "Bölüm Özeti: Süt Evrelerinden İnek Sütü Karşılaştırmasına Geçiş",
        "section": "Anne Sütünün Evreleri, Dinamik Bileşimi ve Anneye Faydaları",
        "slideNumber": 60,
        "narrative": (
            "Anne sütünün kolostrumdan son süte kadar sergilediği bu dinamik zarafet, "
            "başka hiçbir hayvan sütünün insan yavrusu için uygun olmadığını açıkça göstermektedir. "
            "Buna rağmen tarihte ve günümüzde inek sütü bebeklere en çok içirilen ve en çok zarar veren besin olmuştur. "
            "İnek sütü hızla kilo alan, kemikleri kaba, beyni küçük bir buzağıyı büyütmek için tasarlanmıştır; "
            "insan sütü ise yavaş büyüyen, narin böbreklere sahip ve muazzam bir beyin geliştiren insan bebeği içindir. "
            "Yedinci bölümümüzde, anne sütü ile inek sütünün protein profili (whey vs kazein), alerjen beta-laktoglobulin, "
            "taurin konsantrasyonu, demir emilimi ve ozmolarite farkları moleküler düzeyde kıyaslanacaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İnek sütü buzağının hızlı kas ve kemik büyümesine göre programlanmışken insan sütü insan yavrusunun beyin gelişimine odaklanmıştır.",
                "beyin gelişimine",
                "İnsan yavrusunun merkezi sinir sistemi olgunlaşması hedefi"
            ),
            make_causal_chain(
                "Türlere Özgü Süt Biyolojisinin Karşılaştırma Mantığı",
                [
                    "1. Buzağı İhtiyacı: 1 ayda ağırlığını ikiye katlamak için devasa kazein ve kalsiyum gereklidir.",
                    "2. Bebek İhtiyacı: Yavaş büyüyen beden, narin böbrek ve devasa serebral korteks inşası esastır.",
                    "3. Uyumsuzluk: İnek sütü bebeğe verilirse protein ve fosfor böbreği boğar; demir mikrokanamayla kaybolur.",
                    "4. Kesin Yasak: Bu radikal biyolojik uçurum nedeniyle 1 yaşından önce inek sütü verilmesi yasaklanmıştır."
                ]
            ),
            make_active_recall(
                "İnek sütünün biyolojik evrimsel tasarımı ile insan sütünün tasarımı arasındaki en temel felsefi ve anatomik fark nedir?",
                "İnek sütü buzağının hızlı kas ve iskelet büyümesine odaklanmışken (yüksek kazein ve kalsiyum); insan sütü insan bebeğinin beyin ve nörogelişimine odaklanmıştır (yüksek laktoz, whey ve esansiyel yağlar).",
                "İskelet büyümesi ile serebral korteks gelişimi odağı farkı"
            )
        ]
    })

    return slides
