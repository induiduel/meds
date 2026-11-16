# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-19-s91",
        "title": "KAH'ta Prenatal Tanı ve Tedavi: 6-8. Haftada Deksametazon",
        "content": "Daha önce KAH'lı çocuk öyküsü bulunan riskli ailelerde, yeni gebelikte kız fetusun virilizasyonunu önlemek için eşsiz bir prenatal farmakoterapi protokolü uygulanır (Sınav Spotu):\n\n- **Tedavi Başlama Zamanı:** Dış genital farklılaşma 8-9. haftalarda başladığı için, tedavi gebelik öğrenilir öğrenilmez, en geç **6. ila 8. gebelik haftasında** başlanmalıdır.\n- **İlaç Seçimi (Deksametazon):**\n  - Plasentada bulunan 11β-HSD2 enzimi normalde hidrokortizonu ve prednizolonu yıkarak inaktive eder.\n  - Ancak **Deksametazon plasental 11β-HSD2 tarafından inaktive edilemez**; plasentayı serbestçe aşarak fetal hipofize ulaşır.\n  - Fetal hipofizde ACTH salgısını baskılar; böylece fetal adrenal korteksten androjen salınımı durdurulur ve kız fetusta virilizasyon (klitoromegali, labial füzyon) tamamen engellenir.\n- **Zamanlama Kritiktir:** 9. haftadan sonra başlanan tedavi virilizasyonu geri döndüremez.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Prenatal Deksametazon Tedavi Protokolü",
                [
                    "1. Risk Tespiti: KAH öykülü ailede gebelik fark edilir edilmez genetik danışma verilir.",
                    "2. Erken Başlangıç: 6-8. gebelik haftasında anneye deksametazon başlanır.",
                    "3. Plasental Geçiş: 11β-HSD2 enzimini aşan deksametazon fetal dolaşıma geçer.",
                    "4. ACTH Baskılanması: Fetal adrenal hiperplazi ve androjen fırtınası önlenir.",
                    "5. Normal Anatomi: Etkilenmiş 46,XX kız bebek normal dişi genitalyası ile doğar."
                ]
            ),
            make_cloze(
                "KAH riskli gebeliklerde plasental 11β-HSD2 enzimi tarafından inaktive edilmeden fetusa geçebilen deksametazon tedavisi en geç 6-8. haftada başlanmalıdır.",
                "deksametazon",
                "Plasentayı geçerek fetal ACTH'yi baskılayan sentetik glukokortikoid"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-19-s92",
        "title": "CVS / Amniyosentez ile Doğrulama ve Tedaviyi Kesme Kriterleri",
        "content": "Prenatal deksametazon tedavisi körlemesine başlandığı için fetüsün genetik durumu netleşir netleşmez yeniden değerlendirilir (Sınav Spotu):\n\n- **10-12. Haftada Koryon Villus Örneklemesi (CVS):**\n  - Fetal DNA elde edilerek iki temel parametreye bakılır:\n    1. **Genetik Cinsiyet (SRY/karyotip):** Fetus XX mi yoksa XY mi?\n    2. **CYP21A2 Mutasyon Analizi:** Fetus homozigot/compound heterozigot hasta mı, yoksa taşıyıcı/sağlıklı mı?\n- **Tedavinin Kesilme Kriterleri (Çok Önemli):**\n  - Fetus **46,XY erkek ise** tedavi DERHAL KESİLİR (erkek fetusta virilizasyon bir patoloji değildir, gereksiz steroid maruziyeti engellenir).\n  - Fetus **46,XX kız ancak sağlıklı veya heterozigot taşıyıcı ise** tedavi DERHAL KESİLİR.\n- **Tedavinin Devam Kriteri:** Yalnızca fetus **46,XX genetik kız VE CYP21A2 mutasyonu açısından etkilenmiş (hasta) ise** tedavi doğuma kadar sürdürülür (riskli gebeliklerin 1/8'i).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Fetusun Genetik Durumu", "Cinsiyet ve Mutasyon", "Prenatal Deksametazon Kararı"],
                [
                    ["Etkilenmiş Kız Fetus", "46,XX ve Homozigot/Bileşik Mutasyon", "Tedavi DOĞUMA KADAR DEVAM EDER (Virilizasyon önlenir)"],
                    ["Etkilenmemiş / Taşıyıcı Kız", "46,XX ve Normal/Heterozigot", "Tedavi HEMEN KESİLİR"],
                    ["Erkek Fetus (Hasta veya Sağlıklı)", "46,XY (Herhangi bir genotip)", "Tedavi HEMEN KESİLİR (Gereksiz steroid önlenir)"]
                ]
            ),
            make_quiz(
                "KAH riski nedeniyle 7. haftada anneye deksametazon başlanan bir gebelikte 11. haftada yapılan CVS sonucunda fetusun '46,XY' karyotipli ve homozigot CYP21A2 mutasyonu taşıdığı saptanıyor. En doğru klinik yaklaşım hangisidir?",
                [
                    {"key": "A", "text": "Fetus erkek olduğu için anneye verilen deksametazon tedavisi hemen kesilmelidir", "isCorrect": True, "explanation": "Doğru cevap A'dır: Fetus erkek (46,XY) olduğunda androjen virilizasyonu zaten beklenen fizyolojik bir süreçtir; genital anomali riski yoktur, bu nedenle fetusu steroid toksisitesinden korumak için tedavi derhal kesilir."},
                    {"key": "B", "text": "Deksametazon dozu iki katına çıkarılmalıdır", "isCorrect": False, "explanation": "Erkek fetusta tedavi sürdürülmez."},
                    {"key": "C", "text": "Doğuma kadar aynı dozda devam edilmelidir", "isCorrect": False, "explanation": "Tedavi yalnızca etkilenmiş 46,XX kız bebeklerde doğuma kadar sürer."},
                    {"key": "D", "text": "Gebelik hemen sonlandırılmalıdır", "isCorrect": False, "explanation": "KAH tedavi edilebilir bir hastalıktır, terminasyon endikasyonu değildir."}
                ]
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-19-s93",
        "title": "Kuşkulu Genitalya Algoritması Adım 1: Palpabl Gonad Muayenesi",
        "content": "Yenidoğan bir bebekte kuşkulu (ambigus) genitalya saptandığında fizik muayenenin ilk ve en kritik adımı gonadların palpasyonudur (Sınav Spotu):\n\n- **Altın Muayene Kuralı:** Hekim dikkatli parmak hareketleriyle inguinal kanalları, labia majörleri/skrotumu palpe etmelidir.\n- **İki Taraflı Gonad Palpe Edilemiyorsa (Bilateral Non-palpabl Gonad):**\n  - Aksi kanıtlanana kadar bebek **46,XX Konjenital Adrenal Hiperplazi (KAH)** kabul edilmelidir!\n  - Çünkü overler batın içindedir ve asla ele gelmez; bu bebekler potansiyel ölümcül tuz kaybettirici kriz riski altındadır.\n- **En Az Bir Gonad Palpe Ediliyorsa:**\n  - Ele gelen doku over olamaz (over fıtık kesesi hariç inmez).\n  - Palpe edilen gonad hemen her zaman bir **testis veya ovotestistir**.\n  - Bu durumda tanı öncelikle **46,XY CGB** (5α-redüktaz eksikliği, PAIS), miks gonadal disgenezi veya ovotestiküler CGB yönüne kayar.\n- **Asimetrik Palpasyon:** Bir tarafta gonad var diğer tarafta yoksa Miks Gonadal Disgenezi (45,X/46,XY) düşünülmelidir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Gonad Palpe Edilemiyor vs En Az Bir Gonad Palpe Ediliyor",
                "Gonad Palpe Edilemiyor (Bilateral Yok)",
                "Öncelikle 46,XX KAH düşünülür; overler batındadır; acil elektrolit takibi ve 17-OHP istenir.",
                "En Az Bir Gonad Palpe Ediliyor",
                "Gonad testistir; 46,XY CGB (androjen sentez/direnç defekti) veya miks gonadal disgenezi düşünülür."
            ),
            make_cloze(
                "Kuşkulu genitalya ile doğan bir bebekte bilateral gonadların palpe edilememesi durumunda aksi kanıtlanana kadar 46,XX konjenital adrenal hiperplazi düşünülmelidir.",
                "konjenital adrenal hiperplazi",
                "Gonadların ele gelmediği durumda ilk ekarte edilmesi gereken hayati 46,XX acili"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-19-s94",
        "title": "Algoritma Adım 2: Hızlı Genetik Değerlendirme (Karyotip, QF-PCR, FISH)",
        "content": "Fizik muayenenin ardından tanı akışını yönetecek en temel rehber genetik cinsiyetin belirlenmesidir (Sınav Spotu):\n\n- **Hızlı Moleküler Testler (24-48 Saat):**\n  - Ailenin cinsiyet belirsizliğinden kaynaklanan derin kaygısını hafifletmek ve acil algoritmayı yönlendirmek için **QF-PCR (Kantitatif Floresan PCR)** veya **FISH** uygulanır.\n  - X ve Y spesifik tekrarlar (SRY, Xq/Yq probları) taranarak bebeğin 46,XX mi, 46,XY mi yoksa sayısal seks anöploidisi (45,X veya 47,XXY) mi taşıdığı hızla belirlenir.\n- **Klasik Sitogenetik Karyotip Analizi (Altın Standart):**\n  - Hızlı testler harika bir ön bilgi verse de **asla klasik karyotip analizinin yerini tutmaz**.\n  - Klasik G-bantlama karyotip analizi mozaiklikleri (örn. 45,X/46,XY), translokasyonları (SRY taşıyan X) ve yapısal delesyonları kesin olarak gösterir.\n- **Kritik Kural:** Karyotip sonucu çıkana kadar çocuğa cinsiyet ataması yapılmamalı ve nüfus kaydı bekletilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Genetik Yöntem", "Hız / Süre", "Tespit Ettiği Temel Durum", "Kısıtlılığı"],
                [
                    ["QF-PCR", "24-48 saat", "X, Y, 13, 18, 21 kopya sayıları ve SRY varlığı", "Düşük düzeyli mozaikliği ve translokasyonları atlayabilir"],
                    ["FISH", "24-48 saat", "X, Y ve SRY problarıyla hedef kromozom varlığı", "Yapısal tüm genomu göstermez"],
                    ["G-Bant Karyotip", "7-14 gün", "Tüm genomik yapı, anöploidi ve mozaisizm (Altın Standart)", "Hücre kültürüne ihtiyaç duyar, yavaştır"]
                ]
            ),
            make_quiz(
                "Kuşkulu genitalya ile doğan bir yenidoğanda acil cinsiyet ve SRY varlığını belirlemek amacıyla ilk 24-48 saatte başvurulan en hızlı moleküler genetik yöntem hangisidir?",
                [
                    {"key": "A", "text": "QF-PCR veya FISH analizi", "isCorrect": True, "explanation": "Doğru cevap A'dır: QF-PCR ve FISH hücre kültürü gerektirmediği için 24-48 saatte hızlıca X, Y ve SRY sonucunu verir."},
                    {"key": "B", "text": "Klasik G-bantlama karyotipi", "isCorrect": False, "explanation": "Klasik karyotip altın standarttır ancak kültür nedeniyle 1-2 hafta sürer."},
                    {"key": "C", "text": "Tüm ekzom dizileme (WES)", "isCorrect": False, "explanation": "WES haftalar/aylar süren pahalı bir ileri testtir."},
                    {"key": "D", "text": "Western blot", "isCorrect": False, "explanation": "Western blot protein analizidir, genetik tayinde kullanılmaz."}
                ]
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-19-s95",
        "title": "Algoritma Adım 3: Pelvik USG ile Uterus ve Gonad Taraması",
        "content": "Karyotip ile paralel olarak acil yapılması gereken görüntüleme tetkiki **Yüksek Çözünürlüklü Pelvik Ultrasonografidir** (Sınav Spotu):\n\n- **Uterus Varlığı / Yokluğu (Kritik Kavşak):**\n  - **Uterus Varsa:** Fetal yaşamda Sertoli hücresi ve **AMH etkisi OLMADIĞINI** gösterir.\n    - Karyotip 46,XX ise $\\to$ **Konjenital Adrenal Hiperplazi (KAH)**,\n    - Karyotip 46,XY ise $\\to$ **Persistan Müller Kanalı Sendromu (PMDS)** veya tam gonadal disgenezi (Swyer).\n  - **Uterus Yoksa:** Fetal yaşamda fonksiyonel Sertoli hücreleri tarafından **AMH salgılandığını ve Müller kanalının geriletildiğini** gösterir.\n    - Karyotip 46,XY ise $\\to$ **Androjen Duyarsızlık Sendromu (ADS)** veya **5α-Redüktaz Eksikliği**.\n- **Gonadların Lokalizasyonu:** Batın içi, inguinal kanal veya skrotal kabartılarda gonadın anatomik yerleşimi, ekojenitesi ve olası ovotestis görünümü taranır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "USG'de Uterus Mevcut vs USG'de Uterus Yok",
                "USG'de Uterus Mevcut (AMH Yok)",
                "Sertoli AMH'si çalışmamıştır; 46,XX'te en sık KAH; 46,XY'de Swyer sendromu veya PMDS düşünülür.",
                "USG'de Uterus Yok (AMH Var)",
                "Sertoli AMH'si çalışmıştır; testis dokusu vardır; 46,XY'de Androjen Duyarsızlığı (CAIS) veya 5α-Redüktaz düşünülür."
            ),
            make_cloze(
                "Kuşkulu genitalyalı bir bebekte pelvik ultrasonografide uterusun saptanması embriyolojik dönemde AMH etkisinin olmadığını gösterir.",
                "AMH",
                "Müller kanallarını gerileten ve yokluğunda uterusun geliştiği Sertoli hormonu"
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-19-s96",
        "title": "Algoritma Adım 4: Hormonal Profil ve Biyokimyasal Analiz",
        "content": "Genetik ve ultrasonografi bulguları eşliğinde kapsamlı bir endokrin profil çıkarılır (Sınav Spotu):\n\n- **1. Adrenal Hormonlar ve Elektrolitler:**\n  - **Serum 17-OH Progesteron (17-OHP):** KAH taramasında ilk istenecek testtir; aşırı yüksekse 21-hidroksilaz eksikliğini gösterir.\n  - **Elektrolitler (Na, K):** Özellikle 7-14. günlerde tuz kaybı krizini (hiponatremi, hiperkalemi) yakalamak için seri takip edilir.\n  - Kortizol, ACTH, Renin ve Aldosteron düzeyleri.\n- **2. Gonadal Hormonlar (Mini-Puberte Penceresi):**\n  - Doğumdan sonraki ilk 1-3 ayda bebekte 'mini-puberte' evresi yaşanır; LH, FSH, Testosteron ve AMH fizyolojik olarak yükselir.\n  - **Testosteron / DHT Oranı:** >30 ise 5α-redüktaz eksikliği.\n  - **AMH ve İnhibin B:** Testiste fonksiyonel Sertoli hücresi varlığını kanıtlar.\n  - **hCG Stimülasyon Testi:** Prepübertal dönemde Leydig hücre rezervini test etmek için testosteron yanıtı ölçülür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Ölçülen Hormon", "Normal / Yüksek Olması", "Düşük Olması"],
                [
                    ["17-OH Progesteron", "KAH (21-OH eksikliği) kanıtı", "21-OH eksikliği dışlanır"],
                    ["AMH / İnhibin B", "Fonksiyonel testis Sertoli dokusu var", "Gonadal agenezi / disgenezi veya dişi over"],
                    ["Testosteron / DHT", ">30 ise 5α-redüktaz eksikliği", "<20 ise normal dönüşüm veya reseptör defekti"],
                    ["Sodyum / Potasyum", "Normal ise basit virilizan form", "Hiponatremi + hiperkalemi: Tuz kaybettirici KAH krizi"]
                ]
            ),
            make_quiz(
                "Yenidoğan döneminde kuşkulu genitalya ile başvuran bir bebekte mini-puberte evresinde bakılan serum AMH düzeyinin yüksek saptanması aşağıdakilerden hangisini KESİN OLARAK kanıtlar?",
                [
                    {"key": "A", "text": "Vücutta fonksiyonel Sertoli hücrelerine sahip testis dokusunun bulunduğunu", "isCorrect": True, "explanation": "Doğru cevap A'dır: AMH yalnızca fonksiyonel Sertoli hücreleri (testis dokusu) tarafından üretilir; yüksek AMH testis varlığının kesin kanıtıdır."},
                    {"key": "B", "text": "Uterusun tamamen normal olduğunu", "isCorrect": False, "explanation": "AMH yüksekse uterus geriler, bulunmaz."},
                    {"key": "C", "text": "Bebeğin Turner sendromu olduğunu", "isCorrect": False, "explanation": "Turner sendromunda streak over vardır, AMH saptanamaz."},
                    {"key": "D", "text": "CYP21A2 mutasyonu olduğunu", "isCorrect": False, "explanation": "KAH'ta gonad overdir, AMH erkek düzeyinde yüksek olmaz."}
                ]
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-19-s97",
        "title": "Moleküler Genetik Paneller: NGS ve Açıklanamayan %20-25 Grup",
        "content": "Karyotip ve biyokimya ile aydınlatılamayan olgularda Yeni Nesil Dizileme (NGS) teknolojileri devreye girer (Sınav Spotu):\n\n- **Hedefe Yönelik CGB Gen Panelleri:**\n  - İçinde 50 ila 100 genin (SRY, SOX9, NR5A1, WT1, AR, SRD5A2, CYP21A2, WNT4, FOXL2 vb.) bulunduğu NGS panelleri ile tek seferde tüm olası mutasyonlar taranır.\n  - Moleküler tanı başarı oranı 46,XX CGB'de çok yüksektir (%90-95, çünkü çoğunluğu KAH'tır).\n- **46,XY CGB'deki Tanı Zorluğu (Sınav Spotu):**\n  - Tüm gelişmiş moleküler genetik yöntemlere (Karyotip, Array-CGH, NGS panel, Ekzom Dizileme - WES) rağmen, **46,XY CGB vakalarının yaklaşık %20 ila %25'inde altta yatan genetik neden bulunamaz**.\n  - Bu açıklanamayan grubun henüz tanımlanmamış yeni genlerden, nekodlayıcı promoter/enhancer mutasyonlarından, epigenetik değişikliklerden veya oligojenik etkileşimlerden kaynaklandığı düşünülmektedir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "46,XX CGB Genetik Aydınlatma vs 46,XY CGB Genetik Aydınlatma",
                "46,XX CGB (Tanı Başarısı Yüksek)",
                "Olguların %90-95'inde CYP21A2 veya bilinen KAH gen mutasyonu saptanır; tanı oranı çok yüksektir.",
                "46,XY CGB (Tanı Zorluğu)",
                "Tüm NGS ve ekzom analizlerine rağmen vakaların %20-25'inde hiçbir moleküler genetik neden saptanamaz."
            ),
            make_cloze(
                "Modern genetik yöntemlere rağmen 46,XY CGB tanısı alan olguların yaklaşık yüzde yirmi beşinde altta yatan spesifik genetik mutasyon saptanamamaktadır.",
                "yüzde yirmi beşinde",
                "Moleküler olarak aydınlatılamayan 46,XY CGB olgularının oranı"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-19-s98",
        "title": "Multidisipliner CGB Konseyi: Cinsiyet Ataması ve Etik İlkeler",
        "content": "CGB yönetimi tek bir hekimin bireysel inisiyatifine bırakılamaz; geniş katılımlı bir konsey tarafından yürütülmelidir (Sınav Spotu):\n\n- **Multidisipliner Ekip Üyeleri:**\n  - Çocuk Endokrinoloğu,\n  - Tıbbi Genetik Uzmanı,\n  - Çocuk Üroloğu / Çocuk Cerrahı,\n  - Çocuk Psikiyatristi / Klinik Psikolog,\n  - Yenidoğan Uzmanı ve Tıbbi Etik Uzmanı.\n- **Cinsiyet Atama Kararı İlkeleri:**\n  - Cinsiyet kararı aceleye getirilmemelidir; aileye 'bebeğin cinsel organlarının henüz olgunlaşmadığı ve tetkiklerin sürdüğü' şeffafça anlatılmalıdır.\n  - Kararda: Karyotip, iç genital organların durumu, fertilite potansiyeli, cerrahi rekonstrüksiyon olanakları ve beyin maskülinizasyonu dikkate alınır.\n- **Erken Cerrahiye Yaklaşım Değişimi:**\n  - Güncel tıp etiği kılavuzları, hayati acil durumlar (tuz krizi, idrar yolu obstrüksiyonu) hariç, salt kozmetik amaçlı geri dönüşsüz genital küçültme cerrahilerinin **bireyin kendi rızasını (özerklik ilkesi) verebileceği yaşa kadar ertelenmesini** kuvvetle tavsiye etmektedir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "CGB Multidisipliner Yönetim Akışı",
                [
                    "1. İlk Bildirim: Aileye acele edilmeden durum dürüstçe açıklanır; kayıt bekletilir.",
                    "2. Acil Tıbbi Güvenlik: Tuz kaybı ve idrar çıkışı açısından bebek stabilize edilir.",
                    "3. Kurul Toplantısı: Genetik, endokrin ve cerrahi uzmanları verileri birleştirir.",
                    "4. Bilgilendirilmiş Karar: Aile ve kurul ortaklaşa en uygun cinsiyet rolünü belirler.",
                    "5. Uzun Vadeli Destek: Ergenlik ve erişkinlikte psikolojik ve cinsel takip sürdürülür."
                ]
            ),
            make_quiz(
                "Kuşkulu genitalya ile doğan bir bebekte cinsiyet ataması ve uzun dönem yönetim planı yapılırken benimsenmesi gereken en doğru etik ve klinik yaklaşım hangisidir?",
                [
                    {"key": "A", "text": "Çocuk endokrinolojisi, tıbbi genetik, çocuk cerrahisi ve psikiyatri uzmanlarından oluşan multidisipliner bir konsey tarafından ailenin katılımıyla karar verilmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Modern CGB yönetimi multidisipliner uzman konseyi ve ailenin şeffaf ortaklığı ile yürütülür."},
                    {"key": "B", "text": "Doğumu yaptıran hekimin ilk gün bebeğin dış görünüşüne göre karar vermesi", "isCorrect": False, "explanation": "Tek hekimin dış görünüşe göre anında karar vermesi kabul edilemez bir hatadır."},
                    {"key": "C", "text": "Test sonuçları beklenmeden hemen ilk 24 saatte kadınlaştırma cerrahisi yapılması", "isCorrect": False, "explanation": "Geri dönüşsüz erken kozmetik cerrahi güncel etik kurallara aykırıdır."},
                    {"key": "D", "text": "Ailenin durumdan haberdar edilmeyip gizli tutulması", "isCorrect": False, "explanation": "Tıbbi etik şeffaflık ve aydınlatılmış onam gerektirir."}
                ]
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-19-s99",
        "title": "Doğumsal Genital Anomalilerde Gelecek Perspektifi ve Destek",
        "content": "Moleküler biyoloji ve hücresel tedavilerdeki baş döndürücü gelişmeler CGB alanına umut verici yenilikler getirmektedir (Sınav Spotu):\n\n- **Hücresiz Fetal DNA (cfDNA) ile Erken Tanı:**\n  - Anne kanından fetal cfDNA analizi ile gebeliğin 7-8. haftasında koryon villus biyopsisi bile yapılmadan fetal cinsiyet ve CYP21A2 mutasyonları taranabilmektedir.\n  - Bu sayede gereksiz deksametazon kullanımı ortadan kalkacaktır.\n- **Kök Hücre ve Organoid Teknolojisi:**\n  - Hastanın kendi uyarılmış pluripotent kök hücrelerinden (iPSC) Sertoli ve Leydig benzeri hücreler veya steroid üreten adrenal organoidler geliştirilmektedir.\n- **Psikososyal Bütünleşme:**\n  - Tıbbi tedavinin başarısı yalnızca anatomik düzeltmeyle değil; bireyin toplum içinde damgalanmadan, sağlıklı bir cinsel kimlik ve benlik saygısıyla yaşamasını sağlamakla ölçülür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Geleneksel CGB Yaklaşımı vs Modern / Gelecek CGB Yaklaşımı",
                "Geleneksel Yaklaşım (Tarihsel)",
                "Aceleci cerrahi düzeltmeler, damgalayıcı terminoloji ve biyolojik gerçeklerin gizlenmesi mevcuttu.",
                "Modern ve Gelecek Yaklaşım",
                "Erken non-invaziv genetik tanı, özerklik ilkesine saygı, multidisipliner kurul ve yaşam boyu psikososyal destek."
            ),
            make_cloze(
                "Gebelikte anne kanından hücresiz fetal DNA analizi yapılarak erken haftalarda KAH tanısı konabilmekte ve gereksiz deksametazon kullanımı önlenebilmektedir.",
                "fetal DNA",
                "Anne plazmasında dolaşan ve non-invaziv prenatal tanı sağlayan genetik materyal"
            )
        ]
    })

    # Slide 100 - CHECKPOINT 10
    slides.append({
        "id": "k1-19-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Cinsiyet Gelişim Bozuklukları Büyük Özeti",
        "content": "Bu büyük checkpointte Ders 19'un tüm anahtar noktalarını 10 maddede özetliyoruz:\n\n1. **Genetik Cinsiyet:** Y kromozomu üzerindeki SRY (Yp11.3) 41. günde pik yapar ve otozomal anahtar gen **SOX9'u (17q24)** açar; SOX9 duplikasyonu tek başına erkek gelişimi sağlar, heterozigot kaybı **Kampomelik Displazi** yapar.\n2. **Over Genleri:** Dişi yönü aktif bir yoldur; **RSPO1, WNT4, CTNNB1 (β-katenin) ve FOXL2 (BPES sendromu)** pregranüloza hücrelerinde SOX9 ve FGF9'u baskılar.\n3. **DAX1 (Xp21):** Çift dozu (duplikasyonu) **46,XY cinsiyet tersinmesi** yapar; inaktivasyonu **X'e bağlı adrenal hipoplazi** ile gider.\n4. **Kanallar ve Hormonlar:** Sertoli AMH'si Müller'i eritir. Leydig testosteronu Wolff'u geliştirir. **5α-redüktaz (SRD5A2)** testosteronu DHT'ye çevirerek penil üretra ve skrotumu oluşturur. INSL3 ise transabdominal testis inişini sağlar.\n5. **Seks Kromozom CGB:** **Klinefelter (47,XXY)** 1/500 erkek, küçük sert testis, azospermi, jinekomasti, 1 Barr. **Turner (45,X)** 1/2500 kız, kısa boy (SHOX), streak over, aort koarktasyonu, 0 Barr. **Miks Gonadal Disgenezi (45,X/46,XY)** bir yanda testis diğer yanda streak over, gonadoblastom riski.\n6. **5α-Redüktaz Eksikliği (SRD5A2):** 46,XY otozomal resesif. Testosteron yüksek, DHT düşük (T/DHT >30). Doğumda kuşkulu/kız görünüm; **pubertede güçlü virilizasyon ve erkek kimliğine geçiş**.\n7. **Komplet Androjen Duyarsızlığı (CAIS):** 46,XY X'e bağlı AR mutasyonu. Tam kadın dış genitalyası, kör vajen, **uterus yok (AMH var)**, **pubik kıl yok**, pubertede aromataz ile dolgun meme gelişimi.\n8. **KAH (21-Hidroksilaz Eksikliği):** 46,XX kuşkulu genitalyanın en sık nedeni (%90-95 CYP21A2). Kortizol yok $\\to$ **ACTH aşırı artar** $\\to$ Adrenal hiperplazi ve aşırı androjen. **Tuz kaybettirici form (%75)** neonatal hiponatremi ve hiperkalemi ile ölümcül kriz yapar.\n9. **Prenatal Deksametazon:** KAH riskli gebelikte anneye **6-8. haftada** başlanır; CVS'te fetus 46,XY veya etkilenmemişse kesilir, etkilenmiş 46,XX ise doğuma kadar sürdürülür.\n10. **Klinik Algoritma:** Bilateral gonad yoksa $\\to$ **46,XX KAH**. En az bir gonad varsa $\\to$ Testis (46,XY CGB). İlk test hızlı QF-PCR/FISH ve klasik karyotiptir. Yönetim multidisiplinerdir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Hastalık Tablosu", "Karyotip", "Gonad", "İç Genital Kanallar", "Dış Genital Görünüm"],
                [
                    ["Klinefelter Sendromu", "47,XXY", "Küçük atrofik testis", "Wolff var, Müller yok", "Normal erkek + jinekomasti"],
                    ["Turner Sendromu", "45,X", "Bilateral streak over", "Uterus ve tubalar var", "Kız (Kısa boy, yele boyun)"],
                    ["5α-Redüktaz Eksikliği", "46,XY", "Testisler mevcut", "Vas deferens var, uterus yok", "Doğumda kuşkulu/kız $\\to$ Pubertede erkek"],
                    ["CAIS (Testiküler Fem.)", "46,XY", "İntraabdominal testis", "Uterus yok, vas deferens yok", "Kusursuz dişi, pubik kıl yok"],
                    ["KAH (21-Hidroksilaz)", "46,XX", "Normal overler", "Uterus ve tubalar var", "Virilize / Kuşkulu (Prader 1-5)"]
                ]
            ),
            make_chain(
                "Ders 19 Büyük Bütüncül Akış",
                [
                    "1. Genetik Belirlenme: SRY ve SOX9 ile testis, WNT4 ve FOXL2 ile over açılır.",
                    "2. Hormonal Düzenleme: AMH Müller'i eritir, testosteron Wolff'u, DHT penisi yapar.",
                    "3. Anöploidi Sapmaları: 47,XXY ve 45,X primer gonadal yetmezlik ve infertilite yapar.",
                    "4. Enzim ve Reseptör Defektleri: 5α-redüktaz, AR ve CYP21A2 klasik CGB tablolarını oluşturur.",
                    "5. Tanı ve Yaşam: Karyotip, USG, hormonlar ve multidisipliner kurul ile yönetim tamamlanır."
                ]
            )
        ]
    })

    return slides
