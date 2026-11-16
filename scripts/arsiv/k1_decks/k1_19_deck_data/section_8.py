# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-19-s71",
        "title": "Androjen Duyarsızlık Sendromu: AR Geni ve X'e Bağlı Kalıtım",
        "content": "46,XY CGB vakalarının en sık görülen nedenlerinden biri, eski adıyla 'testiküler feminizasyon' olarak bilinen **Androjen Duyarsızlık Sendromudur (ADS)** (Sınav Spotu):\n\n- **Genetik Lokus ve Kalıtım:**\n  - X kromozomunun uzun kolunda (Xq11-12) yer alan **AR (Androjen Reseptörü)** genindeki mutasyonlara bağlıdır.\n  - Kalıtım şekli **X'e bağlı resesiftir (X-linked recessive)**; anneler taşıyıcıdır, etkilenen bireyler 46,XY genetik erkeklerdir (ailede teyze/kız kardeşlerde benzer öykü sık görülür).\n- **Reseptör Yapısı ve Mutasyon Çeşitliliği:**\n  - AR, nükleer steroid reseptör süper ailesine aittir; N-terminal transaktivasyon, çinko parmaklı DNA bağlayıcı ve C-terminal ligand bağlayıcı (LBD) domenlerinden oluşur.\n  - AR geninde 500'den fazla farklı nokta mutasyonu, delesyon ve trinükleotid tekrar polimorfizmi tanımlanmıştır.\n- **Temel Patoloji:** Testosteron ve DHT sentezi tamamen normaldir; ancak hedef hücrelerdeki androjen reseptörü hormonu bağlayamaz veya çekirdeğe sinyal iletemez (uç organ direnci).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Özellik", "Androjen Reseptörü (AR)", "Klinik Yansıması"],
                [
                    ["Kromozom Lokusu", "Xq11-12", "X'e bağlı resesif kalıtım; taşıyıcı annelerden 46,XY çocuklara aktarılır"],
                    ["Domenler", "Ligand Bağlayıcı, DNA Bağlayıcı, N-terminal", "Mutasyonun yerine göre tam (CAIS) veya kısmi (PAIS) direnç"],
                    ["Hormon Düzeyi", "Testosteron ve DHT Normal veya Yüksek", "Sorun hormon eksikliği değil, hücre içi reseptör yanıtsızlığıdır"]
                ]
            ),
            make_cloze(
                "Androjen duyarsızlık sendromuna yol açan ve Xq11-12 bölgesinde yer alan AR geni X'e bağlı resesif kalıtım modeli gösterir.",
                "X'e bağlı resesif",
                "Hastalığın anneden erkek çocuklara aktarılmasını belirleyen kalıtım paterni"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-19-s72",
        "title": "Komplet Androjen Duyarsızlık Sendromu (CAIS): Tam Kadın Fenotipi",
        "content": "AR reseptörünün fonksiyonunun tamamen sıfırlandığı duruma **Komplet Androjen Duyarsızlığı (CAIS)** adı verilir (Sınav Spotu):\n\n- **Dış Genital Görünüm:**\n  - Fetal dönemde androjen sinyali hiç algılanamadığı için dış genital taslaklar tamamen dişi varsayılan yönünde gelişir.\n  - Doğumda bu bebekler **kusursuz bir kız bebek** görünümündedir; labia majörler, labia minörler ve klitoris tamamen normal dişi anatomisindedir.\n  - Bu nedenle çocukluk dönemi boyunca hiçbir şüphe duyulmaz ve hasta kız çocuğu olarak yetiştirilir.\n- **Ergenlikte Başvuru:**\n  - Hastalar genellikle 16-18 yaşlarında **sekonder seks karakterleri (meme) gelişmesine rağmen hiç adet görmeme (Primer Amenore)** şikayetiyle jinekolojiye başvururlar.\n  - Diğer bir başvuru şekli ise çocuklukta kasık fıtığı onarımı sırasında herni kesesi içinde testis saptanmasıdır (hernia uteri/inguinalis).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "CAIS Klinik Başvuru ve Fark Edilme Akışı",
                [
                    "1. Doğum: Tamamen normal dişi dış genitalya ile kız olarak kaydedilir.",
                    "2. Çocukluk: Büyüme ve gelişme normal kız çocuğu olarak devam eder.",
                    "3. Olası Erken İpucu: İnguinal fıtık kesesinde ele gelen kitle (testis).",
                    "4. Puberte: Normal meme gelişimi tamamlanır ancak menstrüasyon başlamaz.",
                    "5. Tanı: Primer amenore tetkikinde 46,XY karyotip ve kör vajen saptanır."
                ]
            ),
            make_quiz(
                "16 yaşında göğüs gelişimi tamamlanmış ancak hiç menstrüasyon görmemiş (primer amenore) bir genç kızda pelvik muayenede kör bir vajen saptanıyor ve karyotipi 46,XY geliyor. En olası tanı hangisidir?",
                [
                    {"key": "A", "text": "Komplet Androjen Duyarsızlık Sendromu (CAIS)", "isCorrect": True, "explanation": "Doğru cevap A'dır: 46,XY karyotipi, mükemmel kadın dış genitalyası, gelişmiş memeler, primer amenore ve kör vajen klasik CAIS tablosudur."},
                    {"key": "B", "text": "Turner Sendromu", "isCorrect": False, "explanation": "Turner sendromunda meme gelişmez ve karyotip 45,X'tir."},
                    {"key": "C", "text": "5α-Redüktaz Eksikliği", "isCorrect": False, "explanation": "5α-redüktaz eksikliğinde pubertede virilizasyon ve penis gelişimi olur, meme gelişmez."},
                    {"key": "D", "text": "Konjenital Adrenal Hiperplazi", "isCorrect": False, "explanation": "KAH'ta karyotip 46,XX'tir ve klitoromegali görülür."}
                ]
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-19-s73",
        "title": "CAIS'te İç Genital Anatomi: Kör Vajen ve Müller Yokluğu",
        "content": "CAIS olgularında iç genital anatomiyi anlamak fetal endokrinolojinin en temel kuralını kavramayı gerektirir (Sınav Spotu):\n\n- **Müller Kanalları Yoktur:**\n  - Fetal testisteki Sertoli hücreleri normaldir ve **AMH salgılar**.\n  - AMH'nin etki mekanizması androjen reseptörüne değil, kendi spesifik reseptörüne (AMHR2) bağlıdır.\n  - Bu nedenle Müller kanalları normal erkekte olduğu gibi başarıyla erir; hastada **uterus, fallop tüpleri ve vajinanın üst 1/3 kısmı KESİNLİKLE YOKTUR**.\n- **Kör Vajen:** Vajinanın alt 2/3'lük kısmı ürogenital sinüsten gelişir ve dışa açıktır ancak yukarıda serviks ve uterus olmadığı için kör bir cep şeklinde (kısa kör vajen) sonlanır.\n- **Wolff Kanalları da Yoktur:**\n  - Wolff kanallarının gelişimi testosterona bağımlıdır.\n  - Reseptör (AR) çalışmadığı için testosteron Wolff kanallarını kurtaramaz ve Wolff kanalları da dejenere olur (vas deferens ve epididim gelişmez).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Müller Yapıları (AMH) vs Wolff Yapıları (Testosteron / AR)",
                "Müller Kanalları (AMH Etkisi)",
                "AMH salgısı normal olduğu için Müller erir; hastada uterus ve fallop tüpleri bulunmaz.",
                "Wolff Kanalları (Androjen Direnci)",
                "AR reseptörü çalışmadığı için yüksek testosterona rağmen Wolff kanalları erir; vas deferens yoktur."
            ),
            make_cloze(
                "Komplet androjen duyarsızlık sendromunda Sertoli hücrelerinden salgılanan AMH nedeniyle uterus ve fallop tüpleri kesinlikle bulunmaz.",
                "uterus",
                "Müller kanal regresyonu nedeniyle CAIS hastalarında bulunmayan temel dişi üreme organı"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-19-s74",
        "title": "Pubertede Feminizasyon: Aromatizasyon ve Meme Gelişimi",
        "content": "CAIS hastalarında ergenlik döneminde kadın sekonder seks karakterlerinin (meme ve kadınsı yağ dağılımı) nasıl geliştiği büyüleyici bir biyokimyasal mekanizmadır (Sınav Spotu):\n\n- **Androjenlerin Aromatizasyonu:**\n  - Pubertede LH uyarısıyla testislerden yüksek miktarda testosteron salgılanır.\n  - Reseptör direnci nedeniyle testosteron hipofizdeki LH salgısını baskılayamaz; LH sürekli yüksek kalarak testosteron sentezini daha da kamçılar.\n  - Kanda aşırı biriken testosteron, periferik yağ ve glandüler dokulardaki **P450 Aromataz (CYP19A1)** enzimi tarafından yoğun şekilde **Östradiole (E2)** dönüştürülür.\n- **Karşılanmamış Östrojen Etkisi:**\n  - Normal kadınlarda östrojenin meme büyütücü etkisi androjenler tarafından dengelenir.\n  - CAIS hastalarında androjen reseptörü sıfır olduğu için **östrojen etkisi tamamen karşılanmamış (unopposed) kalır**.\n  - Sonuçta memeler mükemmel ve dolgun gelişir; kalça ve uyluklarda kadın tipi yumuşak yağ dağılımı ve pürüzsüz kadın cildi oluşur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "CAIS'te Feminizasyon Biyokimyası",
                [
                    "1. Yüksek LH Salgısı: Hipofiz androjen direncini algılayıp aşırı LH salgılar.",
                    "2. Yüksek Testosteron: Testisler erişkin erkek düzeyinde testosteron üretir.",
                    "3. Periferik Aromataz: P450 aromataz enzimi testosteronu östradiole çevirir.",
                    "4. Karşılanmamış Östrojen: Androjen freni olmadığı için östrojen reseptörleri aktive olur.",
                    "5. Kusursuz Meme Gelişimi: Tanner Evre 5 düzeyinde dolgun kadın memesi şekillenir."
                ]
            ),
            make_cloze(
                "CAIS hastalarında pubertede meme gelişimini sağlayan östrojen hormonu yüksek testosteronun periferik dokularda aromataz enzimi ile dönüştürülmesiyle elde edilir.",
                "aromataz",
                "Androjenleri östrojene çeviren sitokrom P450 süper ailesi enzimi"
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-19-s75",
        "title": "Pubik ve Aksiller Kıllanma Yokluğu: Androjen Direncinin İpucu",
        "content": "CAIS olgularını normal kadınlardan veya Müller agenezisinden (MRKH sendromu) ayıran en tipik klinik ipucu vücut kıllanmasıdır (Sınav Spotu):\n\n- **Kıllanmanın Biyolojik Kontrolü:**\n  - İnsan vücudunda meme gelişimi östrojene bağlıyken, **pubik ve aksiller (koltuk altı) kıllanmanın başlaması (adrenarş/pubarş) tamamen androjenlere bağımlıdır**.\n  - Kıl foliküllerindeki dermal papillada androjen reseptörleri testosteron/DHT sinyalini alarak terminal kıl üretimini başlatır.\n- **CAIS'te Kıllanma Tablosu:**\n  - AR reseptörü çalışmadığı için CAIS hastalarında pubertede **pubik ve aksiller kıllanma ya tamamen yoktur ya da son derece seyrektir (Tanner Evre 1-2)**.\n- **MRKH ile Ayırıcı Tanı:**\n  - Mayer-Rokitansky-Küster-Hauser (MRKH) sendromunda da 46,XX kadında uterus yoktur ve vajen kördür ancak overler ve androjen reseptörleri normal olduğu için **pubik ve aksiller kıllanma tamamen normaldir**.\n  - CAIS'te ise kıl yokluğu androjen direncini haykıran altın standart fizik muayene bulgusudur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "CAIS (46,XY) vs MRKH Sendromu (46,XX)",
                "CAIS (Androjen Direnci)",
                "Karyotip 46,XY; gonad testistir; testosteron erkek düzeyindedir; pubik ve aksiller kıl tamamen yoktur.",
                "MRKH Sendromu (Müller Agenezisi)",
                "Karyotip 46,XX; gonad overdir; hormonlar kadın düzeyindedir; pubik ve aksiller kıllanma tamamen normaldir."
            ),
            make_quiz(
                "Primer amenore ve kör vajen saptanan iki hastadan birincisinde pubik kıllanma tamamen normal iken, ikincisinde pubik ve aksiller kıllanmanın hiç olmadığı görülüyor. İkinci hastada öncelikle düşünülmesi gereken durum hangisidir?",
                [
                    {"key": "A", "text": "Komplet Androjen Duyarsızlık Sendromu (CAIS)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kıllanmanın hiç olmaması kıl foliküllerinin androjene yanıtsızlığını (androjen reseptör direnci - CAIS) gösterir; normal kıllanması olan hasta ise 46,XX MRKH sendromudur."},
                    {"key": "B", "text": "Mayer-Rokitansky-Küster-Hauser (MRKH) Sendromu", "isCorrect": False, "explanation": "MRKH'de kıllanma normaldir (birinci hasta)."},
                    {"key": "C", "text": "Konjenital Adrenal Hiperplazi", "isCorrect": False, "explanation": "KAH'ta aşırı kıllanma (hirsutizm) olur."},
                    {"key": "D", "text": "Turner Sendromu", "isCorrect": False, "explanation": "Turner'da meme gelişimi de olmaz ve boy kısadır."}
                ]
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-19-s76",
        "title": "Parsiyel ADS (PAIS / Reifenstein): Ambigus Genitalya Yelpazesi",
        "content": "AR genindeki mutasyon reseptör işlevini tamamen sıfırlamayıp kısmen korumuşsa tablo **Parsiyel Androjen Duyarsızlığı (PAIS)** adını alır (Sınav Spotu):\n\n- **Eski Eponim:** Klasik formu literatürde **Reifenstein Sendromu** olarak bilinir.\n- **Geniş Klinik Yelpaze:**\n  - **Dişi Baskın Fenotip:** Klitoromegali ve hafif labial füzyon ile başvuran kuşkulu genitalya.\n  - **Ambigus Fenotip:** Belirgin mikrofallus (<1.5-2 cm), psödohermafrodit dış görünüm, perineoskrotal hipospadias, bifid skrotum ve inmemiş testisler.\n  - **Erkek Baskın Fenotip:** Normal görünümlü ancak küçük penis, izole hipospadias ve pubertede belirgin **jinekomasti (erkekte meme büyümesi)** ile seyreden tablo.\n- **Klinik Tanı Zorluğu:** PAIS olgularında androjen direncinin derecesini kestirmek güçtür; bu durum cinsiyet ataması ve cerrahi kararlarda multidisipliner değerlendirmeyi zorunlu kılar.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["ADS Formu", "Reseptör Fonksiyonu", "Dış Genital Görünüm", "Pubertede Göğüs / Kıl Durumu"],
                [
                    ["Komplet ADS (CAIS)", "Tamamen sıfır", "Kusursuz normal kadın dış genitalyası", "Meme tam gelişir, pubik kıl yoktur"],
                    ["Parsiyel ADS (PAIS)", "Kısmen korunmuş", "Ambigus genitalya, mikrofallus, hipospadias", "Jinekomasti gelişir, kıl seyrektir"],
                    ["Hafif ADS (MAIS)", "Hafif azalmış", "Normal erkek dış genitalyası", "Pubertede jinekomasti veya izole infertilite"]
                ]
            ),
            make_cloze(
                "Androjen reseptörünün kısmi işlev gördüğü ve mikrofallus, perineal hipospadias ile jinekomastiye yol açan tabloya Reifenstein sendromu veya parsiyel androjen duyarsızlığı denir.",
                "Reifenstein sendromu",
                "Parsiyel androjen duyarsızlığının klasik tarihsel eponim adı"
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-19-s77",
        "title": "Hafif ADS (MAIS): Erkek Fenotipi ve İzole İnfertilite",
        "content": "Androjen duyarsızlık spektrumunun en ılımlı ucu **Hafif Androjen Duyarsızlığıdır (MAIS)** (Sınav Spotu):\n\n- **Fenotip:**\n  - Bireyler tamamen normal erkek iç ve dış genital organlarına sahiptir.\n  - Doğumda veya çocuklukta hiçbir şüphe uyandırmazlar.\n- **Klinik Başvuru:**\n  - Ergenlik döneminde hafif veya orta derecede **jinekomasti** gelişebilir.\n  - Sakal ve vücut kıllanmasında hafif seyreklik, tiz ses tonu bulunabilir.\n  - En sık başvuru nedeni erişkin yaşta **açıklanamayan erkek infertilitesidir (oligospermi veya azospermi)**.\n- **Genetik Temel:** AR genindeki CAG trinükleotid tekrar sayısının artışı (polimorfik uzama) reseptörün transaktivasyon kapasitesini hafifçe zayıflatarak spermatogenezi olumsuz etkileyebilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_quiz(
                "Dış genital muayenesi tamamen normal bir erkekte pubertede jinekomasti ve erişkin yaşta sperm azlığına bağlı infertilite saptanıyor. Androjen düzeyleri yüksek/normal bulunan bu olguda en olası hafif reseptör kusuru hangisidir?",
                [
                    {"key": "A", "text": "Hafif Androjen Duyarsızlığı (MAIS)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Normal erkek fenotipine eşlik eden jinekomasti ve izole infertilite hafif androjen duyarsızlığının (MAIS) tipik tablosudur."},
                    {"key": "B", "text": "Komplet Androjen Duyarsızlığı (CAIS)", "isCorrect": False, "explanation": "CAIS'te fenotip tamamen kadındır."},
                    {"key": "C", "text": "Turner Sendromu", "isCorrect": False, "explanation": "Turner sendromu 45,X kadındır."},
                    {"key": "D", "text": "5α-Redüktaz Eksikliği", "isCorrect": False, "explanation": "5α-redüktaz eksikliğinde mikrofallus ve hipospadias tipiktir."}
                ]
            ),
            make_recall(
                "Normal erkek dış genitalyasına sahip bireylerde izole oligospermi ve infertiliteye yol açabilen androjen reseptör polimorfizmi nedir?",
                "CAG trinükleotid tekrar artışı",
                "AR geni ekzon 1 bölgesindeki poliglutamin zincir uzaması"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-19-s78",
        "title": "İntraabdominal Testisler, Malignite Riski ve Gonadektomi Zamanı",
        "content": "CAIS hastalarında intraabdominal veya inguinal yerleşimli testisler önemli bir onkolojik takip gerektirir (Sınav Spotu):\n\n- **Testislerin Yerleşimi:**\n  - Testisler skrotum olmadığı için batın içinde, iç halkada veya inguinal kanal içinde (labia majörlerin üst kutbunda) kalır.\n  - Histolojisinde Sertoli hücreleri ve Leydig hücreleri mevcuttur ancak spermatogenez duraklamıştır.\n- **Malignite Riski (Kanserleşme):**\n  - İnmemiş testislerde **seminom, gonadoblastom ve malign embriyonal karsinom** gelişme riski mevcuttur.\n  - Ancak CAIS'te bu risk prepübertal dönemde son derece düşüktür (%1-2); asıl risk **25-30 yaşlarından sonra %15-30'lara çıkar**.\n- **Gonadektomi Zamanlaması (Önemli Konsensüs):**\n  - Testisler ergenlikte testosteron üreterek bunun östrojene dönüşmesi sayesinde **doğal meme gelişimini ve kemik mineralizasyonunu sağlar**.\n  - Bu nedenle ameliyat prepübertal dönemde YAPILMAZ; **puberte ve doğal meme gelişimi tamamlandıktan sonra (18-20 yaş civarında) bilateral gonadektomi yapılır**.\n  - Cerrahi sonrasında hastaya ömür boyu östrojen replasman tedavisi (osteoporozu önlemek için) başlanır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Erken Çocuklukta Ameliyat vs Puberte Sonrası Ameliyat (CAIS)",
                "Erken Çocuklukta Gonadektomi (Önerilmez)",
                "Çocuğun doğal östrojen kaynağı kesilir; ergenlikte yapay hormon verilmek zorunda kalınır ve meme gelişimi zayıf kalır.",
                "Puberte Sonrası Gonadektomi (Önerilen)",
                "Testislerin aromatizasyonu ile doğal meme ve kemik gelişimi tamamlanır; ardından kanser riski için çıkarılır."
            ),
            make_cloze(
                "CAIS hastalarında testislerin puberte öncesi çıkarılmayıp ergenlik sonrasına ertelenmesinin temel nedeni kendi hormonlarıyla doğal meme gelişiminin tamamlanmasını sağlamaktır.",
                "meme gelişiminin",
                "Karşılanmamış östrojen etkisiyle pubertede tamamlanan ikincil kadın cinsiyet karakteri"
            )
        ]
    })

    # Slide 79 - CHECKPOINT 8
    slides.append({
        "id": "k1-19-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Androjen Duyarsızlık Sendromu Spektrumu",
        "content": "Bu checkpointte androjen duyarsızlık spektrumunun kilit unsurlarını özetliyoruz:\n\n- **Gen ve Kalıtım:** Xq11-12 lokusundaki **AR (Androjen Reseptörü)** gen mutasyonuna bağlı X'e bağlı resesif geçiş.\n- **Temel Kusur:** Hormon azlığı değil, hücre içi reseptör direnci. Kanda testosteron ve LH normal veya yüksektir.\n- **CAIS Fenotipi:** Dış genitalya kusursuz dişi; ergenlikte **primer amenore** ile başvurur.\n- **İç Genitalya:** Sertoli AMH'si nedeniyle **uterus ve tüpler kesinlikle yoktur**; AR çalışmadığı için **vas deferens de yoktur**; vajina kör bir cep şeklindedir.\n- **Pubertede Feminizasyon:** Aşırı testosteron **P450 aromataz** ile östrojene çevrilir; karşılanmamış östrojen sayesinde dolgun kadın memeleri oluşur.\n- **Kıllanma:** Androjen direncinin en tipik fiziksel kanıtı olarak **pubik ve aksiller kıl tamamen yoktur veya çok seyrektir**.\n- **Malignite ve Cerrahi:** Testislerde ileri yaşta kanser riski vardır; ameliyat (gonadektomi) **doğal meme gelişimi bittikten sonra (puberte sonrası)** yapılır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Özellik", "CAIS (Komplet)", "PAIS (Reifenstein)", "MAIS (Hafif)"],
                [
                    ["Reseptör Durumu", "Tam inaktif", "Kısmi inaktif", "Hafif defektif"],
                    ["Dış Genitalya", "Kusursuz dişi", "Ambigus / Hipospadias", "Normal erkek"],
                    ["Uterus / Tüp", "Yok (AMH var)", "Yok (AMH var)", "Yok (AMH var)"],
                    ["Pubik Kıl", "Yok / Çok seyrek", "Seyrek", "Normal"],
                    ["Primer Şikayet", "Primer amenore", "Kuşkulu genitalya", "İnfertilite"]
                ]
            ),
            make_chain(
                "CAIS Patofizyolojik Özet Zinciri",
                [
                    "1. Genetik Kusur: Xq11-12'deki AR geninde fonksiyon kaybı mutasyonu oluşur.",
                    "2. Fetal Dönem: Testosteron algılanamaz; dış genitalya dişi yönünde gelişir.",
                    "3. Müller Gerilemesi: Normal AMH üretimi uterus ve tüpleri tamamen eritir.",
                    "4. Ergenlikte Aromatizasyon: Yüksek testosteron östrojene dönerek memeleri büyütür.",
                    "5. Klinik Tanı: Primer amenore, pubik kılsızlık ve kör vajen ile tanı konur."
                ]
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-19-s80",
        "title": "Bölüm Özeti: Androjen Direncinden 46,XX CGB ve KAH'a Geçiş",
        "content": "Bölüm 8 boyunca androjen reseptör defektlerini (CAIS, PAIS, MAIS), kör vajen tablosunu ve pubertal aromatizasyon mekanizmasını inceledik:\n\n- **Özet:** CAIS'te genetik erkek (46,XY) birey, tam androjen direnci nedeniyle dış görünüş olarak tamamen kadındır ancak uterus ve pubik kılı yoktur.\n- **Sonraki Bölüm (Bölüm 9):** Tam tersi bir tablo olan; 46,XX genetik kız fetusun aşırı adrenal androjen maruziyetiyle virilize olmasına yol açan ve yenidoğan acili olabilen **Konjenital Adrenal Hiperplaziyi (KAH - 21-hidroksilaz eksikliği, CYP21A2) ve tuz kaybettirici krizi** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "CAIS hastalarında intraabdominal testislerin cerrahi olarak çıkarılmasının (gonadektomi) puberte sonrasına ertelenmesinin gerekçesi nedir?",
                "Doğal meme ve kemik gelişiminin tamamlanmasını sağlamak",
                "Aromatizasyonla üretilen endojen östrojenin sağladığı ergenlik gelişimi"
            ),
            make_quiz(
                "CAIS tanısı konan 17 yaşındaki bir hastada aşağıdaki anatomik yapılardan hangisinin varlığı KESİNLİKLE BEKLENMEZ?",
                [
                    {"key": "A", "text": "Uterus ve fallop tüpleri", "isCorrect": True, "explanation": "Doğru cevap A'dır: Testis Sertoli hücreleri normal AMH salgıladığı için CAIS hastalarında uterus ve fallop tüpleri kesinlikle gelişemez."},
                    {"key": "B", "text": "Meme dokusu", "isCorrect": False, "explanation": "Aromatizasyon sayesinde meme dokusu gelişmiştir."},
                    {"key": "C", "text": "Kör vajen", "isCorrect": False, "explanation": "Vajinanın alt 2/3'ü mevcuttur ve kör sonlanır."},
                    {"key": "D", "text": "İntraabdominal testisler", "isCorrect": False, "explanation": "Hastada testisler mevcuttur."}
                ]
            )
        ]
    })

    return slides
