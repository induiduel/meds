# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-19-s51",
        "title": "Seks Kromozomu Sayısal Anomalilerine Genel Bakış ve Fenotipik Ilımlılık",
        "content": "Seks kromozomlarındaki sayısal anöploidiler (trizomiler ve monozomiler), otozomal anöploidilere kıyasla çok daha ılımlı klinik tablolar oluşturur (Sınav Spotu):\n\n- **Fenotipik Ilımlılığın İki Biyolojik Nedeni:**\n  1. **X İnaktivasyonu (Lionizasyon):** Hücrede birden fazla X kromozomu olsa dahi biri hariç diğer tüm X kromozomları interfazda yoğunlaşarak inaktive olur (Barr cisimciği).\n  2. **Y Kromozomunun Gen Fakirliği:** Y kromozomu çok az sayıda fonksiyonel gen (yaklaşık 70-80 gen) taşır; ekstra kopyaları hücre metabolizmasını yıkıcı düzeyde bozmaz.\n- **Genel Kural:** Hücrede en az bir adet fonksiyonel Y kromozomu (SRY geni) bulunuyorsa, X kromozomlarının sayısı ne olursa olsun (47,XXY, 48,XXXY, 49,XXXXY) embriyo **erkek yönünde farklılaşır**.\n- **Kromozom Artışı ile Zeka İlişkisi:** Her ilave ekstra X veya Y kromozomu IQ puanında ortalama 10-15 puanlık düşüşe ve konuşma/öğrenme gecikmelerine yol açar.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Otozomal Trizomi vs Seks Kromozomu Trizomisi",
                "Otozomal Trizomi (Örn: Trizomi 18/13)",
                "Yüzlerce aktif gen dozu değişir; çoklu ağır organ malformasyonları ve erken bebeklikte ölüm görülür.",
                "Seks Kromozom Trizomisi (Örn: XXY, XYY)",
                "X inaktivasyonu ve Y'nin gen azlığı sayesinde çoğu birey erişkin yaşa ulaşır; fenotip oldukça ılımlıdır."
            ),
            make_cloze(
                "Seks kromozomu trizomilerinde kliniğin otozomlara göre çok daha hafif olmasının temel nedeni fazla X kromozomlarının inaktive olarak Barr cisimciğine dönüşmesidir.",
                "Barr cisimciğine",
                "İnterfaz çekirdeğinde yoğunlaşan inaktif X kromatini"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-19-s52",
        "title": "Klinefelter Sendromu (47,XXY): Hipogonadizm ve Jinekomasti",
        "content": "Erkeklerde en sık görülen seks kromozomu anöploidisi **Klinefelter Sendromudur** (Sınav Spotu):\n\n- **Sıklık ve Genetik:** Canlı erkek doğumların yaklaşık **1/500 ila 1/600'ünde** görülür. Vakaların yaklaşık %80'i klasik **47,XXY** karyotipidir; %20'si mozaik (46,XY/47,XXY) veya polisomik formlardır.\n- **Gonadal Patoloji ve İnfertilite:**\n  - Puberteye kadar testisler normal görünebilir ancak pubertede seminifer tübüllerde ilerleyici hyalinizasyon ve fibrozis başlar.\n  - Sertoli ve germ hücreleri yok olur; **azospermi ve primer infertilite** kalıcıdır.\n  - Testisler küçük, sert ve atrofiktir (1-2 ml hacminde).\n- **Endokrin ve Fiziksel Bulgular:**\n  - Leydig hücre disfonksiyonu sonucu testosteron düşer, negatif geri besleme kalktığı için **LH ve FSH aşırı yükselir (hipergonadotropik hipogonadizm)**.\n  - Östrojen/androjen oranının artmasına bağlı olarak olguların %50'sinde belirgin **jinekomasti (meme büyümesi)** gelişir (meme kanseri riski 20-50 kat artar).\n  - SHOX geni aşırı dozu nedeniyle **uzun boy ve uzun bacaklar (öストrojenik/öunukoid gövde yapısı)** karakteristiktir.\n- **Tedavi:** Puberteden itibaren düzenli testosteron replasman tedavisi uygulanır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Klinefelter Klinik Özelliği", "Biyolojik Mekanizma", "Klinik Yansıması"],
                [
                    ["Küçük Sert Testisler", "Seminifer tübül hyalinizasyonu ve fibrozis", "Azospermi ve infertilite"],
                    ["Yüksek LH ve FSH", "Düşük testosteron ve inhibin B geri besleme kaybı", "Hipergonadotropik hipogonadizm"],
                    ["Jinekomasti", "Östrojen / Testosteron dengesizliği", "Meme dokusu gelişimi, artmış meme kanseri riski"],
                    ["Uzun Boy / Önokoid Yapı", "Psödootozomal bölgedeki SHOX geninin 3 kopyası", "Gövdeye oranla uzun alt ekstremiteler"]
                ]
            ),
            make_quiz(
                "İnfertilite araştırması yapılan 22 yaşındaki bir erkekte uzun boy, jinekomasti, bilateral küçük sert testisler, serumda yüksek LH/FSH ve düşük testosteron saptanıyor. Bukkal mukozada 1 adet Barr cisimciği izleniyor. En olası karyotip hangisidir?",
                [
                    {"key": "A", "text": "47,XXY (Klinefelter Sendromu)", "isCorrect": True, "explanation": "Doğru cevap A'dır: 47,XXY Klinefelter sendromu klasik olarak uzun boy, küçük testisler, jinekomasti, hipergonadotropik hipogonadizm ve 1 Barr cisimciği (2 X - 1 = 1) ile seyreder."},
                    {"key": "B", "text": "45,X (Turner Sendromu)", "isCorrect": False, "explanation": "Turner sendromu 45,X kızlarda görülür, Barr cisimciği 0'dır."},
                    {"key": "C", "text": "47,XYY", "isCorrect": False, "explanation": "47,XYY bireylerde Barr cisimciği 0'dır, testisler normaldir."},
                    {"key": "D", "text": "46,XY", "isCorrect": False, "explanation": "Normal erkekte Barr cisimciği bulunmaz."}
                ]
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-19-s53",
        "title": "Klinefelter Varyantları (48,XXXY, 49,XXXXY) ve 46,XX Erkekler",
        "content": "Seks kromozomu polisomileri ve translokasyonlar Klinefelter tablosunu ağırlaştırabilir veya taklit edebilir (Sınav Spotu):\n\n- **Polisomik Varyantlar (48,XXXY, 49,XXXXY):**\n  - Eklenen her ekstra X kromozomu ile birlikte klinik dramatik olarak ağırlaşır.\n  - 49,XXXXY bireylerde klasik Klinefelter bulgularına ek olarak **şiddetli zihinsel yetersizlik**, belirgin yüz dismorfizmi (epikantus, hipertelorizm), hipoplastik penis/skrotum ve **radyoulnar sinostoz** eşlik eder.\n  - Barr cisimciği sayısı (X kromozomu sayısı - 1) kuralına göre 49,XXXXY'de çekirdek başına **3 adet Barr cisimciği** görülür.\n- **46,XX Testiküler CGB (46,XX Erkek Sendromu):**\n  - Sıklığı yaklaşık 1/20.000 erkektir.\n  - Olguların %85'inde babanın spermogenezi sırasındaki hatalı mayotik krossing-over ile **SRY geni Y'den X kromozomuna aktarılmıştır**.\n  - Bu hastalar normal erkek dış genitalyasına, normal penis boyutuna sahiptir ancak Klinefelter gibi küçük testisler, azospermi ve infertilite ile başvururlar; ancak boyları Klinefelter'in aksine genellikle **kısa veya normaldir** (çünkü ekstra SHOX kopyası yoktur).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Klasik Klinefelter (47,XXY) vs 46,XX Erkek",
                "47,XXY Klinefelter",
                "Ekstra X nedeniyle 3 kopya SHOX geni vardır; hasta uzun boyludur; 1 Barr cisimciği taşır.",
                "46,XX Erkek (SRY+)",
                "Normal 2 kopya SHOX vardır; boy normal veya kısadır; azospermi ve küçük testis mevcuttur."
            ),
            make_cloze(
                "49,XXXXY karyotipine sahip bir bireyin interfaz çekirdeklerinde Lyon hipotezine göre tam olarak üç adet Barr cisimciği gözlenir.",
                "üç adet",
                "4 X kromozomu taşıyan hücredeki inaktif X kromatini sayısı"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-19-s54",
        "title": "Turner Sendromu (45,X): Fetal Kayıp ve Kısa Boy (SHOX)",
        "content": "Kadınlarda en sık karşılaşılan monozomi tablosu **Turner Sendromudur** (Sınav Spotu):\n\n- **Epidemiyoloji ve İntrauterin Seleksiyon:**\n  - Canlı doğan kız bebeklerde görülme sıklığı yaklaşık **1/2500**'dür.\n  - Ancak spontan abortusların (düşüklerin) yaklaşık **%10'unu tek başına 45,X embriyoları oluşturur**; konseptus aşamasındaki 45,X fetüslerin **%98-99'u doğumdan önce kaybedilir**.\n  - Canlı doğanların yaklaşık %50'si saf 45,X, %20-30'u mozaik (45,X/46,XX), geri kalanı yapısal anomalidir (izokromozom Xq, halka X).\n- **SHOX Haployetersizliği ve Kısa Boy:**\n  - X ve Y kromozomlarının psödootozomal bölgesinde (PAR1) yer alan **SHOX** (Short Stature Homeobox) geni iskelet büyümesini kontrol eder.\n  - Normal kadın ve erkeklerde 2 kopya SHOX aktiftir (X inaktivasyonundan kaçar).\n  - Turner sendromunda tek X olduğu için tek kopya SHOX bulunur; bu **haployetersizlik tüm Turner hastalarında görülen boy kısalığının ve Madelung deformitesinin temel nedenidir**.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Turner Sendromunda Boy Kısalığı Mekanizması",
                [
                    "1. Monozomi: Fertilizasyonda paternal seks kromozomu kaybıyla 45,X zigotu oluşur.",
                    "2. Tek PAR1 Bölgesi: Psödootozomal bölgedeki genler tek kopya olarak kalır.",
                    "3. SHOX Haployetersizliği: Kemik büyüme plaklarındaki kondrosit proliferasyonu azalır.",
                    "4. İskelet Kusurları: Kısa 4. metakarp, kubitus valgus ve Madelung deformitesi gelişir.",
                    "5. Kısa Boy: Tedavi edilmezse nihai erişkin boy ortalama 140-143 cm civarında kalır."
                ]
            ),
            make_cloze(
                "Turner sendromlu hastalarda görülen boy kısalığından psödootozomal bölgede yer alan SHOX geninin haployetersizliği sorumludur.",
                "SHOX",
                "İskelet boy uzamasını yöneten homeobox gen ailesi üyesi"
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-19-s55",
        "title": "Turner Sendromu Klinik Tablosu: Yele Boyun, Aort Koarktasyonu ve Streak Over",
        "content": "Turner sendromu multisistemik klinik bulgularla karakterize zengin bir tablo sergiler (Sınav Spotu):\n\n- **Dismorfik İskelet ve Deri Bulguları:**\n  - **Yele Boyun (Pterygium colli):** Fetal lenfatik kistik higromanın gerilemesiyle boyun yanlarında kalan deri katlantılarıdır.\n  - Ense saç çizgisinin düşük olması, kalkan göğüs (geniş aralıklı meme başları), kubitus valgus ve kısa 4. metakarp kemiği.\n- **Kardiyovasküler Anomaliler (%30-50):**\n  - En sık konjenital kardiyak defekt **Biküspit Aort Kapağı** (%30) ve **Aort Koarktasyonudur** (%10-15); aort diseksiyonu riski yüksektir.\n- **Gonadal Disgenezi ve İnfertilite:**\n  - Fetal dönemde oositler hızla apoptozise uğrar ve gonadlar germ hücresiz **bilateral streak gonada** döner.\n  - Östrojen yokluğu nedeniyle primer amenore ve sekonder seks karakterlerinin gelişmemesi görülür.\n- **Barr Cisimciği:** 45,X karyotipinde inaktive olacak ikinci bir X bulunmadığı için hücrelerde **0 (sıfır) Barr cisimciği** saptanır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Organ Sistemi", "Turner Sendromu Bulgusu", "Klinik Önem"],
                [
                    ["Kardiyovasküler", "Biküspit aort kapağı, Aort koarktasyonu", "Aort anevrizması ve diseksiyon riski"],
                    ["Gonad / Endokrin", "Bilateral streak over, primer amenore", "Hipergonadotropik hipogonadizm ve infertilite"],
                    ["Lenfatik / Cilt", "Kistik higroma kalıntısı (Yele boyun), düşük saç çizgisi", "Yenidoğanda el-ayak sırtında lenfödem"],
                    ["Renal", "At nalı böbrek, çift toplayıcı sistem", "İdrar yolu enfeksiyonu ve hipertansiyon"]
                ]
            ),
            make_quiz(
                "15 yaşında primer amenore ve boy kısalığı şikayetiyle getirilen bir kız çocuğunun muayenesinde yele boyun, kalkan göğüs ve femoral nabızlarda zayıflama (aort koarktasyonu şüphesi) saptanıyor. Yapılan bukkal yaymada hiç Barr cisimciği görülmüyor. En olası tanı hangisidir?",
                [
                    {"key": "A", "text": "Turner Sendromu (45,X)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kısa boy, yele boyun, aort koarktasyonu, primer amenore ve 0 Barr cisimciği klasik Turner sendromu bulgularıdır."},
                    {"key": "B", "text": "Klinefelter Sendromu", "isCorrect": False, "explanation": "Klinefelter 47,XXY erkektir, 1 Barr cisimciği vardır."},
                    {"key": "C", "text": "Trizomi X (47,XXX)", "isCorrect": False, "explanation": "47,XXX olgularında 2 Barr cisimciği bulunur."},
                    {"key": "D", "text": "Swyer Sendromu", "isCorrect": False, "explanation": "Swyer sendromunda yele boyun ve aort koarktasyonu beklenmez, boy uzundur."}
                ]
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-19-s56",
        "title": "47,XYY Sendromu (Jakob Sendromu): Uzun Boy, Normal Fertilite ve Davranış",
        "content": "Erkeklerde ekstra Y kromozomu ile karakterize durum **47,XYY Sendromudur** (Sınav Spotu):\n\n- **Epidemiyoloji ve Oluşum Mekanizması:**\n  - Yaklaşık **1/1000 canlı erkek doğumda** görülür.\n  - Hata daima babanın **2. mayoz bölünmesindeki Y kromozomu non-disjunction (ayrılamama)** hatasından kaynaklanır (YY taşıyan sperm).\n- **Fiziksel Özellikler:**\n  - Çocukluktan itibaren belirgin **uzun boy** (SHOX geninin 2 aktif kopyası) dikkati çeker.\n  - Ergenlik döneminde şiddetli kistik akne görülebilir.\n  - Dış genitalya ve testis gelişimi tamamen normaldir.\n- **Fertilite ve Kalıtım:**\n  - 47,XYY erkeklerin çok büyük çoğunluğu **tamamen fertildir**; spermatogenez sırasında ekstra Y kromozomu genellikle elenir, bu nedenle çocuklarının da 47,XYY olma riski çok düşüktür.\n- **Bilişsel ve Davranışsal Profil:**\n  - Zeka genellikle normal sınırlardadır ancak dil gelişiminde hafif gecikme, dikkat eksikliği ve hiperaktivite (DEHB) sıklığı artmıştır. Eski suç eğilimi mitleri bilimsel olarak çürütülmüştür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Klinefelter (47,XXY) vs Jakob Sendromu (47,XYY)",
                "47,XXY (Klinefelter)",
                "Testisler küçüktür, testosteron düşüktür, azospermi ve kalıcı infertilite vardır; 1 Barr cisimciği içerir.",
                "47,XYY (Jakob Sendromu)",
                "Testisler ve sperm parametreleri normaldir; fertilite korunmuştur; 0 Barr cisimciği içerir."
            ),
            make_cloze(
                "47,XYY karyotipine sahip bireylerde genetik hata daima babanın ikinci mayoz bölünmesindeki ayrılamama hatasından kaynaklanır.",
                "ikinci mayoz",
                "Ekstra Y kromozomunun sperm hücresine aktarıldığı mayotik evre"
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-19-s57",
        "title": "47,XXX Sendromu (Trizomi X): İki Barr Cisimciği ve Bilişsel Profil",
        "content": "Kadınlarda görülen seks kromozomu trizomisi **47,XXX (Trizomi X / Triple X)** tablosudur (Sınav Spotu):\n\n- **Epidemiyoloji:** Yaklaşık **1/1000 canlı kız doğumda** görülür; ileri anne yaşı riski artırır.\n- **Lionizasyon ve Barr Cisimciği:**\n  - Hücrede 3 adet X kromozomu bulunur.\n  - X inaktivasyonu kuralına göre 2 adet X kromozomu heterokromatine dönüşür; bu nedenle periferik yaymada hücre çekirdeklerinde **tam 2 adet Barr cisimciği** saptanır.\n- **Fiziksel Fenotip ve Fertilite:**\n  - Genellikle belirgin bir majör fiziksel anomaliye yol açmaz.\n  - Ekstra SHOX dozu nedeniyle akranlarına göre **daha uzun boylu** olabilirler.\n  - Cinsel gelişim, menstrüel döngü ve **fertilite genellikle tamamen normaldir**; çoğu kadın tanı almadan yaşamını sürdürür.\n- **Nörogelişimsel Özellikler:**\n  - Konuşma ve lisan becerilerinde hafif gecikmeler, motor koordinasyon güçlükleri, öğrenme güçlüğü ve duygusal olgunlaşmada hafif geri kalma görülebilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Karyotip", "Cinsiyet", "Barr Cisimciği Sayısı", "Fertilite Durumu"],
                [
                    ["45,X (Turner)", "Kadın", "0 adet", "İnfertil (Streak over)"],
                    ["46,XX (Normal Kadın)", "Kadın", "1 adet", "Normal Fertil"],
                    ["47,XXX (Trizomi X)", "Kadın", "2 adet", "Genellikle Normal Fertil"],
                    ["47,XXY (Klinefelter)", "Erkek", "1 adet", "İnfertil (Azospermi)"],
                    ["47,XYY", "Erkek", "0 adet", "Normal Fertil"]
                ]
            ),
            make_quiz(
                "Karyotipi 47,XXX olan bir kadının interfaz çekirdeklerinde saptanması beklenen Barr cisimciği sayısı kaçtır?",
                [
                    {"key": "A", "text": "2 adet", "isCorrect": True, "explanation": "Doğru cevap A'dır: Barr cisimciği sayısı (X sayısı - 1) formülüyle bulunur; 3 - 1 = 2 adet Barr cisimciği saptanır."},
                    {"key": "B", "text": "0 adet", "isCorrect": False, "explanation": "0 Barr cisimciği 45,X Turner veya normal erkekte görülür."},
                    {"key": "C", "text": "1 adet", "isCorrect": False, "explanation": "1 Barr cisimciği 46,XX veya 47,XXY'de görülür."},
                    {"key": "D", "text": "3 adet", "isCorrect": False, "explanation": "3 Barr cisimciği 48,XXXX veya 49,XXXXY'de görülür."}
                ]
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-19-s58",
        "title": "Miks Gonadal Disgenezi (45,X/46,XY): Asimetrik Gonadlar ve Kanser",
        "content": "Seks kromozom mozaisizminin en dramatik klinik tablosu **45,X/46,XY Miks Gonadal Disgenezi (MGD)** tablosudur (Sınav Spotu):\n\n- **Karyotip ve Patogenez:** Erken embriyonik mitoz sırasında Y kromozomunun bir hücre soyunda kaybolmasıyla (anaphase lag) **45,X/46,XY mozaisizmi** oluşur.\n- **Karakteristik Asimetrik Gonad Yapısı:**\n  - En tipik patolojik bulgu: **Bir tarafta disgenetik bir testis, karşı tarafta ise fibröz bir streak gonad** bulunmasıdır.\n  - Testisin bulunduğu tarafta Wolff kanalı gelişirken, streak gonadın bulunduğu tarafta Müller kanalı korunur (tek taraflı uterus boynuzu ve fallop tüpü).\n- **Fenotipik Yelpaze:** Turner sendromu benzeri kız görünümünden, kuşkulu (ambigus) genitalyaya veya hafif hipospadiaslı erkek görünümüne kadar çok geniştir.\n- **Kanser Riski ve Cerrahi:**\n  - Y kromozomu taşıyan disgenetik dokularda **%15-25 oranında gonadoblastom ve malign seminom/disgerminom** gelişir.\n  - Bu nedenle özellikle streak gonad ve inmemiş disgenetik testisler çocukluk çağında cerrahi olarak çıkarılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Miks Gonadal Disgenezi (45,X/46,XY) vs Saf Turner (45,X)",
                "Miks Gonadal Disgenezi (45,X/46,XY)",
                "Asimetrik gonadlar vardır (bir yanda disgenetik testis, diğerde streak); Y materyali nedeniyle yüksek kanser riski taşır.",
                "Saf Turner Sendromu (45,X)",
                "Bilateral simetrik streak gonad vardır; Y materyali içermediği için gonadoblastom riski taşımaz."
            ),
            make_cloze(
                "Karyotipi 45,X/46,XY olan miks gonadal disgenezide en karakteristik patolojik bulgu bir tarafta disgenetik testis, diğer tarafta streak gonad bulunmasıdır.",
                "disgenetik testis",
                "Miks gonadal disgenezide streak gonadın karşısındaki asimetrik gonadal yapı"
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-19-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Seks Kromozomu Sayısal Bozuklukları",
        "content": "Bu checkpointte seks kromozomu anöploidilerini ve klinik farklarını özetliyoruz:\n\n- **Klinefelter (47,XXY):** 1/500 erkek. Küçük sert testisler, hyalinizasyon, azospermi, jinekomasti, uzun boy (SHOX 3 kopya) ve **1 Barr cisimciği**.\n- **Turner (45,X):** 1/2500 canlı kız (%98 abortus). Kısa boy (SHOX tek kopya), yele boyun, biküspit aort kapağı, aort koarktasyonu, bilateral streak gonad ve **0 Barr cisimciği**.\n- **47,XYY (Jakob):** Babanın 2. mayoz ayrılmama hatası. Uzun boy, kistik akne, **normal testis ve normal fertilite**, 0 Barr cisimciği.\n- **47,XXX (Trizomi X):** Uzun boy, hafif öğrenme sorunları, **normal fertilite ve 2 Barr cisimciği**.\n- **Miks Gonadal Disgenezi (45,X/46,XY):** Bir tarafta disgenetik testis, diğer tarafta streak gonad (asimetrik); **yüksek gonadoblastom riski** taşır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Sendrom", "Karyotip", "Sıklık", "Gonad Durumu", "Fertilite"],
                [
                    ["Klinefelter", "47,XXY", "1/500 Erkek", "Küçük atrofik testis", "Steril (Azospermi)"],
                    ["Turner", "45,X", "1/2500 Kız", "Bilateral streak over", "Steril (Primer amenore)"],
                    ["Jakob", "47,XYY", "1/1000 Erkek", "Normal testisler", "Tamamen Fertil"],
                    ["Trizomi X", "47,XXX", "1/1000 Kız", "Normal overler", "Genellikle Fertil"],
                    ["Miks Disgenezi", "45,X/46,XY", "Nadir", "Disgenetik testis + streak", "İnfertil / Kanser riski"]
                ]
            ),
            make_chain(
                "Seks Kromozom Sayısal Bozuklukları Tanı Akışı",
                [
                    "1. Klinik İpucu: Boy anomalisi (kısa veya uzun) ve pubertal gecikme görülür.",
                    "2. Sitolojik Tarama: Bukkal yaymada Barr cisimciği sayısı (X-1) kontrol edilir.",
                    "3. Kesin Karyotip: Klasik sitogenetik bantlama ve QF-PCR ile anöploidi teyit edilir.",
                    "4. Organ Taraması: Turner'da ekokardiyografi, MGD'de gonadal USG ve biyopsi planlanır."
                ]
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-19-s60",
        "title": "Bölüm Özeti: Kromozom Sayısal Bozukluklarından 46,XY CGB'ye Geçiş",
        "content": "Bölüm 6 boyunca seks kromozomlarının sayısal dengesizliklerini ve fenotipik sonuçlarını inceledik:\n\n- **Özet:** Klinefelter ve Turner primer gonadal yetmezlik ve infertilite yaparken, 47,XYY ve 47,XXX genellikle fertil seyirlidir.\n- **Sonraki Bölüm (Bölüm 7):** Normal 46,XY karyotipine sahip olmasına rağmen periferik dönüşüm kusuru nedeniyle ortaya çıkan en klasik 46,XY CGB modelini, **5-Alfa Redüktaz 2 Eksikliğini (SRD5A2) ve pubertedeki dramatik virilizasyon sürecini** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "Bir tarafında disgenetik testis, diğer tarafında streak gonad bulunan ve yüksek gonadoblastom riski taşıyan mozaik karyotip hangisidir?",
                "45,X/46,XY (Miks gonadal disgenezi)",
                "Asimetrik gonadal disgeneziye yol açan seks kromozomu mozaisizmi"
            ),
            make_quiz(
                "Aşağıdaki seks kromozomu anöploidilerinin hangisinde spermatogenez ve erkek fertilitesi genellikle tamamen korunmuştur?",
                [
                    {"key": "A", "text": "47,XYY Sendromu", "isCorrect": True, "explanation": "Doğru cevap A'dır: 47,XYY erkeklerde ekstra Y kromozomu genellikle spermogenezde kaybolur ve fertilite tamamen normaldir."},
                    {"key": "B", "text": "47,XXY Klinefelter Sendromu", "isCorrect": False, "explanation": "Klinefelter'de seminifer tübül fibrozisi ve kalıcı azospermi vardır."},
                    {"key": "C", "text": "48,XXXY Sendromu", "isCorrect": False, "explanation": "Ağır gonadal atrofi ve azospermi görülür."},
                    {"key": "D", "text": "45,X/46,XY Miks Gonadal Disgenezi", "isCorrect": False, "explanation": "Disgenetik gonadlar nedeniyle fertilite bozuktur."}
                ]
            )
        ]
    })

    return slides
