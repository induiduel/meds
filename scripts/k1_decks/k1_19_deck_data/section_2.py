# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-19-s11",
        "title": "SRY Geni: Yp11.3, Presertoli Ekspresyonu ve 41. Gün Piki",
        "content": "Testis gelişimini başlatan ana genetik anahtar, Y kromozomunun kısa kolunda (Yp11.3) yer alan **SRY** (Sex-determining Region Y) genidir (Sınav Spotu):\n\n- **Moleküler Yapı ve TDF:** SRY geni, HMG (High Mobility Group) DNA-bağlayıcı motife sahip bir transkripsiyon faktörüdür ve klasik olarak Testis Belirleyici Faktör (TDF) olarak bilinir.\n- **Hücresel Köken ve Zamanlama:** SRY, bipotansiyel gonadın yalnızca **presertoli hücrelerinde** çok dar bir zaman penceresinde eksprese edilir; fertilizasyondan sonraki **41. günde (yaklaşık 6. hafta) ekspresyonu pik yapar** ve ardından hızla geriler.\n- **Etki Mekanizması:** SRY doğrudan yapısal testis proteinlerini sentezletmez; görevi birincil olarak otozomal bir gen olan **SOX9 genini aktive etmek** ve testis kaskadını tetiklemektir.\n- **Klinik Önemi:** SRY'nin varlığı bipotansiyel gonadın Sertoli hücrelerine farklılaşmasını sağlar; Sertoli hücreleri de Leydig hücrelerinin gelişimini ve AMH salgısını koordine eder.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_cloze(
                "Y kromozomunun kısa kolunda bulunan SRY geni fertilizasyondan sonraki kırk birinci günde pik yaparak presertoli hücrelerinde SOX9 aktivasyonunu tetikler.",
                "kırk birinci günde",
                "SRY gen ekspresyonunun presertoli hücrelerinde en yüksek düzeye ulaştığı post-konsepsiyonel gün"
            ),
            make_chain(
                "SRY Geni ile Testis Başlatma Mekanizması",
                [
                    "1. Yp11.3 Lokasyonu: Y kromozomunun kısa kolundaki SRY geni transkribe edilir.",
                    "2. 41. Gün Piki: Presertoli hücrelerinde dar bir zaman aralığında en yüksek seviyeye ulaşır.",
                    "3. HMG Kutusu ile Bağlanma: SRY proteini DNA'yı bükerek hedef promoter bölgelerini açar.",
                    "4. SOX9 Aktivasyonu: TESCO enhancer bölgesi üzerinden SOX9 transkripsiyonu başlatılır.",
                    "5. Sertoli Farklılaşması: Primitif kordonlar testis kordonlarına ve Sertoli hücrelerine dönüşür."
                ]
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-19-s12",
        "title": "SRY Mutasyonları ve Translokasyonları: 46,XY Dişi ve 46,XX Erkek",
        "content": "SRY geninin kaybı veya yer değiştirmesi, genetik cinsiyet ile gonadal cinsiyet arasında dramatik uyumsuzluklara yol açar (Sınav Spotu):\n\n- **46,XY Saf Gonadal Disgenezi (Swyer Sendromu):**\n  - 46,XY CGB vakalarının yaklaşık **%10-15'inde SRY geninde inaktive edici nokta mutasyonları veya delesyonlar** saptanır.\n  - SRY işlev görmediğinde SOX9 aktive edilemez; bipotansiyel gonad testise dönemez ve germ hücresinden yoksun **streak gonad (ipliksi gonad)** olarak kalır.\n  - Testosteron ve AMH üretilemediği için iç genital kanallar Müller yönünde gelişir (uterus ve tüpler mevcuttur), dış görünüş kızdır.\n- **46,XX Testiküler CGB (46,XX Erkek):**\n  - Mayoz bölünme sırasında X ve Y kromozomlarının psödootozomal bölgesindeki hatalı krossing-over sonucu SRY geni X kromozomuna transloke olur.\n  - 46,XX karyotipli birey SRY taşıdığı için testis dokusu gelişir; fenotip erkektir ancak spermatogenez genleri (AZF) bulunmadığından infertildir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "46,XY SRY Mutasyonu vs 46,XX SRY Translokasyonu",
                "46,XY SRY Defekti (Swyer)",
                "SRY inaktiftir; testis gelişemez, streak gonad kalır, AMH yokluğunda uterus ve tüpler gelişir; fenotip kadındır.",
                "46,XX SRY+ (46,XX Erkek)",
                "SRY X kromozomuna geçmiştir; testis dokusu ve erkek dış genitalya gelişir; Y azospermi faktörleri olmadığı için infertildir."
            ),
            make_quiz(
                "Karyotipi 46,XY olan ancak SRY geninde fonksiyon kaybı mutasyonu saptanan bir hastada beklenen iç ve dış genital yapı bulgusu hangisidir?",
                [
                    {"key": "A", "text": "Streak gonad, uterus ve tubalar mevcut, kadın dış genitalyası", "isCorrect": True, "explanation": "Doğru cevap A'dır: SRY yokluğunda testis oluşmaz (streak gonad); AMH salgılanamadığı için Müller kanalları gerilemez (uterus ve tüpler gelişir), testosteron ve DHT olmadığı için kadın dış genitalyası oluşur."},
                    {"key": "B", "text": "Normal testisler, vas deferens mevcut, normal erkek dış genitalyası", "isCorrect": False, "explanation": "SRY inaktif olduğunda normal testis oluşamaz."},
                    {"key": "C", "text": "Over dokusu, skrotum içinde yerleşmiş testisler", "isCorrect": False, "explanation": "Bu durum ovotestiküler CGB tablosudur."},
                    {"key": "D", "text": "Uterus yokluğu, bilateral normal epididim ve penis", "isCorrect": False, "explanation": "AMH ve testosteron olmadığı için Wolff geriler, Müller korunur."}
                ]
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-19-s13",
        "title": "SOX9 Geni: 17q24, TESCO Enhancer ve Testis Belirleyici",
        "content": "Testis gelişiminin asıl anahtar transkripsiyon faktörü 17. kromozomda (17q24) yer alan **SOX9** genidir (Sınav Spotu):\n\n- **Otozomal Testis Belirleyici:** SOX9, SRY ile yüksek dizi benzerliğine (HMG kutusu) sahip otozomal bir gendir.\n- **Kritik Kural:** SRY'nin temel görevi SOX9 ekspresyonunu başlatmaktır. Deneysel ve klinik olarak kanıtlanmıştır ki, **SRY hiç olmasa dahi ekstra SOX9 kopyası (duplikasyon) erkek gelişimini tek başına sağlayabilir** (46,XX bireyde erkek fenotip).\n- **TESCO Enhancer:** SOX9 geninin düzenleyici bölgesi olan TESCO (Testis-specific Enhancer Core) elemanına **SRY ve SF1 birlikte bağlanarak** SOX9 transkripsiyonunu dramatik olarak artırır.\n- **SOX9 Hedefleri:** SOX9 doğrudan **AMH (Anti-Müllerian Hormon)** gen promoterine bağlanarak AMH sentezini başlatır ve FGF9 ile otokrin/parakrin pozitif geri besleme döngüsü kurar.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Gen ve Düzenleyici", "Kromozom Konumu", "Testis Farklılaşmasındaki Rolü"],
                [
                    ["SRY", "Yp11.3", "Presertoli hücrelerinde dar aralıkta ekspresyon; SOX9'u tetikler"],
                    ["SOX9", "17q24", "Asıl testis belirleyici otozomal faktör; AMH transkripsiyonunu açar"],
                    ["TESCO Enhancer", "17q24 upstream", "SRY ve SF1 proteinlerinin bağlanarak SOX9'u açtığı çekirdek bölge"],
                    ["FGF9", "4p16", "SOX9 düzeyini yüksek tutan ve WNT4'ü baskılayan büyüme faktörü"]
                ]
            ),
            make_cloze(
                "Otozomal bir gen olan SOX9 geninin duplikasyonu halinde ortamda SRY geni bulunmasa dahi erkek yönünde gelişim tetiklenir.",
                "SOX9",
                "17q24 lokalizasyonlu otozomal testis belirleyici ana transkripsiyon faktörü"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-19-s14",
        "title": "Kampomelik Displazi: SOX9 Mutasyonu, İskelet Anomalisi ve Cinsiyet Tersinmesi",
        "content": "SOX9 geninin heterozigot fonksiyon kaybı mutasyonları veya delesyonları ölümcül bir sendrom olan **Kampomelik Displaziye** yol açar (Sınav Spotu):\n\n- **İskelet Bulguları:** SOX9 kondrosit farklılaşması ve kıkırdak/kemik gelişimi için vazgeçilmezdir. Mutasyonunda uzun kemiklerde eğrilik (kampomeli - özellikle tibia ve femurda yaylanma), hipoplastik skapula, 11 çift kosta, mikrognati ve yarık damak görülür.\n- **46,XY Cinsiyet Tersinmesi (Sex Reversal):**\n  - SOX9 mutasyonu taşıyan 46,XY bireylerin yaklaşık **%75'inde gonadal disgenezi ve tam/kısmi dişi fenotip** gelişir.\n  - Bu durum otozomal bir gen mutasyonunun cinsiyet tersinmesine yol açmasının en klasik tıbbi genetik örneğidir.\n- **Solunum Yetmezliği:** Hipoplastik trakeal kıkırdaklar ve dar toraks nedeniyle hastalar genellikle neonatal dönemde asfiksi ve solunum yetmezliğiyle kaybedilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_quiz(
                "Uzun kemiklerde eğrilik, hipoplastik toraks ve solunum sıkıntısı ile doğan bir yenidoğanın karyotipinin 46,XY olmasına rağmen dış genitalyasının kız olduğu saptanıyor. En olası gen mutasyonu hangisidir?",
                [
                    {"key": "A", "text": "SOX9 (Kampomelik Displazi)", "isCorrect": True, "explanation": "Doğru cevap A'dır: SOX9 mutasyonu hem iskelet anomalileriyle seyreden Kampomelik Displaziye hem de 46,XY bireylerde cinsiyet tersinmesine yol açar."},
                    {"key": "B", "text": "CYP21A2", "isCorrect": False, "explanation": "CYP21A2 46,XX bireyde virilizasyon yapar, iskelet displazisi yapmaz."},
                    {"key": "C", "text": "Androjen Reseptörü (AR)", "isCorrect": False, "explanation": "Androjen duyarsızlığında kemik eğriliği ve hipoplastik toraks görülmez."},
                    {"key": "D", "text": "SRD5A2", "isCorrect": False, "explanation": "5a-redüktaz eksikliğinde iskelet displazisi yoktur."}
                ]
            ),
            make_recall(
                "SOX9 geninin heterozigot mutasyonunda kıkırdak displazisi ile birlikte 46,XY bireylerde dişi fenotipe yol açan klinik tablonun adı nedir?",
                "Kampomelik Displazi",
                "Uzun kemiklerde eğrilik ve cinsiyet tersinmesiyle giden sendrom"
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-19-s15",
        "title": "SF1 (NR5A1): Bipotansiyel Gonad, Steroidogenez ve AMH Transkripsiyonu",
        "content": "Nükleer reseptör süper ailesine ait bir transkripsiyon faktörü olan **SF1 (Steroidogenic Factor 1 / NR5A1)**, ürogenital sistemin mimarıdır (Sınav Spotu):\n\n- **Bipotansiyel Gonad Gelişimi:** SF1, embriyonik ürogenital katlantının ve indiferan gonad taslağının oluşması için ilk basamaktan itibaren zorunludur; SF1 yokluğunda gonadlar hiç oluşamaz (gonadal agenezi).\n- **Hipotalamo-Hipofizer-Steroid Aks:** Adrenal korteks ve gonadlardaki steroid sentez eden hücrelerde (Leydig ve teka/granüloza) steroidogenik enzimlerin (StAR, CYP11A1, CYP17A1) transkripsiyonunu kontrol eder.\n- **AMH Sentezinde SOX9 ile İşbirliği:** SF1, SOX9 proteini ile doğrudan fiziksel etkileşime girerek **AMH promoterini güçlü şekilde aktive eder**.\n- **Mutasyon Sonuçları:** NR5A1 mutasyonları 46,XY CGB (gonadal disgenezi, mikrofallus, hipospadias) ve beraberinde adrenal yetmezlik tablosuna yol açabilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "SF1 Geninin Cinsiyet ve Steroid Yolundaki Görevleri",
                [
                    "1. Katlantı Oluşumu: Ürogenital katlantı ve bipotansiyel gonad taslağını kurar.",
                    "2. TESCO Aktivasyonu: SRY ile birlikte SOX9 enhancer bölgesine bağlanır.",
                    "3. AMH Desteği: SOX9 ile kompleks oluşturarak Sertoli hücrelerinden AMH salgılatır.",
                    "4. Steroidogenez: Adrenal ve Leydig hücrelerinde testosteron sentez enzimlerini uyarır."
                ]
            ),
            make_cloze(
                "Adrenal korteks ve gonad gelişimini yöneten SF1 transkripsiyon faktörü, SOX9 ile birlikte Sertoli hücrelerinden AMH sentezini uyarır.",
                "SF1",
                "NR5A1 adıyla da bilinen nükleer reseptör ailesi transkripsiyon faktörü"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-19-s16",
        "title": "WT1 (Wilms Tümörü 1): Böbrek ve Gonad Gelişimi, Frasier ve Denys-Drash",
        "content": "11p13 kromozomunda yer alan **WT1** (Wilms Tumor 1) geni, çinko parmaklı transkripsiyon faktörüdür ve hem böbrek hem gonad gelişiminde kilit rol oynar (Sınav Spotu):\n\n- **Böbrek ve Gonad Ortak Kökeni:** WT1, ürogenital katlantıdan hem metanefrik böbreğin hem de bipotansiyel gonadın gelişimi için zorunludur; 46,XY CGB vakalarının yaklaşık %3-4'ünden sorumludur.\n- **Denys-Drash Sendromu:**\n  - WT1 geninin ekzon 8-9'undaki (çinko parmak bölgesi) missense mutasyonlarına bağlıdır.\n  - Üçlü bulgu: Erken başlangıçlı diffüz mezanjiyal skleroz (erken böbrek yetmezliği), **Wilms tümörü** riski ve 46,XY bireylerde gonadal disgenezi (dişi/ambigus dış genitalya).\n- **Frasier Sendromu:**\n  - İntron 9'daki splice bölgesi (KTS motifi) mutasyonudur (+KTS/-KTS izoform dengesi bozulur).\n  - Yavaş ilerleyen fokal segmental glomerüloskleroz (FSGS), 46,XY tam gonadal disgenezi (kadın fenotip) ve yüksek **gonadoblastom** riski ile seyreder (Wilms tümörü riski düşüktür).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Sendrom Adı", "WT1 Mutasyon Tipi", "Böbrek Patolojisi", "Genital ve Tümör Tablosu"],
                [
                    ["Denys-Drash", "Ekzon 8-9 Missense mutasyonu", "Diffüz mezanjiyal skleroz", "46,XY gonadal disgenezi + Yüksek Wilms tümörü riski"],
                    ["Frasier Sendromu", "İntron 9 Splice mutasyonu (KTS kaybı)", "Fokal segmental glomerüloskleroz (FSGS)", "46,XY kadın fenotip (streak gonad) + Yüksek Gonadoblastom riski"]
                ]
            ),
            make_quiz(
                "Böbrek yetmezliği tablosu ile takip edilen 46,XY karyotipli bir kız çocuğunda WT1 geni intron 9 bölgesinde splice mutasyonu saptanıyor. Bu hastada en olası tanı ve gelişebilecek gonadal tümör hangisidir?",
                [
                    {"key": "A", "text": "Frasier Sendromu - Gonadoblastom", "isCorrect": True, "explanation": "Doğru cevap A'dır: WT1 intron 9 splice mutasyonu Frasier sendromuna neden olur; 46,XY pür gonadal disgenezi ve gonadoblastom riski mevcuttur."},
                    {"key": "B", "text": "Denys-Drash Sendromu - Feokromositoma", "isCorrect": False, "explanation": "Denys-Drash'ta missense mutasyon ve Wilms tümörü tipiktir."},
                    {"key": "C", "text": "Swyer Sendromu - Seminom", "isCorrect": False, "explanation": "Swyer sendromu WT1 değil SRY mutasyonudur."},
                    {"key": "D", "text": "Klinefelter Sendromu - Teratom", "isCorrect": False, "explanation": "Klinefelter 47,XXY karyotipidir."}
                ]
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-19-s17",
        "title": "FGF9 ve PGD2: SOX9 Düzeyinin Korunması ve WNT4 Antagonizması",
        "content": "Testis gelişiminde SRY ekspresyonu 41. günden sonra hızla söner. Bu noktadan sonra testis yolunun devamlılığı otokrin faktörlere devredilir (Sınav Spotu):\n\n- **FGF9 (Fibroblast Growth Factor 9):**\n  - SOX9 tarafından doğrudan aktive edilen bir büyüme faktörüdür.\n  - Sertoli hücrelerinden salgılanarak komşu mezenkimal hücrelere etki eder ve **SOX9 ekspresyonunu yüksek tutan bir pozitif geri besleme döngüsü** oluşturur.\n  - En kritik görevi, over yönünü tetikleyen **WNT4 sinyal yolunu aktif olarak baskılamaktır**; FGF9 yokluğunda XY embriyolarda dahi over benzeri yapılar belirir.\n- **PGD2 (Prostaglandin D2):**\n  - Sertoli hücrelerinde lipokalin tipi PGD2 sentaz ile üretilir.\n  - Hücre içi SOX9 proteininin çekirdeğe translokasyonunu ve kritik eşiğin üzerinde kalmasını destekler.\n- **Sonuç:** Testis oluşumu, SOX9-FGF9-PGD2 üçlüsünün WNT4/β-katenin over kaskadını ezmesiyle garantiye alınır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Erkek Yönü (SOX9 / FGF9) vs Dişi Yönü (WNT4 / β-Katenin)",
                "Erkek Yönü (Testis Hakimiyeti)",
                "SOX9 ve FGF9 yüksek eksprese edilir; FGF9 WNT4'ü bloke eder; kordonlar testise farklılaşır.",
                "Dişi Yönü (Over Hakimiyeti)",
                "SRY yoktur; WNT4 ve RSPO1 aktive olur; β-katenin SOX9 ve FGF9'u bloke ederek over yönünü açar."
            ),
            make_cloze(
                "Sertoli hücrelerinde SOX9 düzeyini sürekli yüksek tutan ve dişi belirleyici WNT4 yolunu aktif olarak baskılayan parakrin faktör FGF9 faktörüdür.",
                "FGF9",
                "Testis kaskadında SOX9 ile pozitif döngü kuran fibroblast büyüme faktörü"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-19-s18",
        "title": "DMRT1 ve Ürogenital Katlantı Genleri: PAX2, EMX2, LHX9",
        "content": "Gonadal gelişimin daha erken ve geç aşamalarında görev yapan tamamlayıcı genetik faktörler mevcuttur (Sınav Spotu):\n\n- **DMRT1 (9p24.3):**\n  - Kromozom 9'un kısa kolunda yer alan DMRT1, geç seks determinasyonunda ve erken testis kordonlarının korunmasında görev alır.\n  - 9p delesyonu olan 46,XY bireylerde gonadal disgenezi ve ambigus genitalya saptanması bu genin önemini gösterir.\n- **Ürogenital Katlantı (Ridge) Genleri:**\n  - Bipotansiyel gonadın üzerinde oturacağı ürogenital katlantı taslağının kurulması için **SF1, WT1, PAX2, EMX2 ve LHX9** genleri gereklidir.\n  - Katlantı aşamasındaki defektler hem gonadları hem de böbrek taslaklarını (nefrik sistem) tamamen yok eder.\n  - EMX2 ve LHX9 genlerinin insan mutasyonları tanımlanmamıştır; embriyonik dönemde tam yokluklarının yaşamla bağdaşmadığı kabul edilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Katlantı ve Diferansiyasyon Geni", "Görevi", "İnsan Patolojisi"],
                [
                    ["DMRT1 (9p24.3)", "Testis kordonlarının devamlılığı", "9p delesyonunda 46,XY CGB ve ambigus genitalya"],
                    ["PAX2", "Ürogenital katlantı ve böbrek gelişimi", "Renal-kolobom sendromu, böbrek hipoplazisi"],
                    ["EMX2 / LHX9", "Erken ürogenital kabartı oluşumu", "İnsanda tanımlı mutasyonu yok (letal)"]
                ]
            ),
            make_quiz(
                "Kromozom 9p delesyonu saptanan 46,XY bir çocukta testis disgenezisi ve ambigus genitalya görülmesinden sorumlu olan gen hangisidir?",
                [
                    {"key": "A", "text": "DMRT1", "isCorrect": True, "explanation": "Doğru cevap A'dır: 9p24.3 bölgesinde yer alan DMRT1 geninin kaybı 46,XY gonadal disgeneziye yol açar."},
                    {"key": "B", "text": "DAX1", "isCorrect": False, "explanation": "DAX1 X kromozomundadır (Xp21)."},
                    {"key": "C", "text": "SOX9", "isCorrect": False, "explanation": "SOX9 17. kromozomdadır (17q24)."},
                    {"key": "D", "text": "SRY", "isCorrect": False, "explanation": "SRY Y kromozomundadır (Yp11.3)."}
                ]
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-19-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Testis Farklılaşmasının Genetik Düzenleyicileri",
        "content": "Bu checkpointte testis gelişimini başlatan ve yöneten gen ağını özetliyoruz:\n\n- **SRY (Yp11.3):** Presertoli hücrelerinde **41. günde pik** yapar; ana görevi SOX9'u aktive etmektir. 46,XY CGB'nin %10-15'inden sorumludur.\n- **46,XX Erkek:** SRY'nin X kromozomuna translokasyonu sonucu oluşur; AZF genleri olmadığı için hasta azospermiktir.\n- **SOX9 (17q24):** Otozomal testis belirleyicidir. SRY olmasa bile duplikasyonu erkek gelişimi sağlar; heterozigot mutasyonu **Kampomelik Displazi ve 46,XY cinsiyet tersinmesine** yol açar.\n- **TESCO Enhancer:** SRY ve SF1'in SOX9'u transkribe etmek için bağlandığı düzenleyici kutudur.\n- **SF1 (NR5A1):** Bipotansiyel gonad, adrenal steroidogenez ve SOX9 ile birlikte **AMH salgısı** için şarttır.\n- **WT1 (11p13):** Böbrek ve gonad gelişimini yönetir; ekzon 8-9 missense mutasyonu **Denys-Drash** (Wilms tümörü), intron 9 splice mutasyonu **Frasier Sendromu** (FSGS, gonadoblastom) yapar.\n- **FGF9 ve PGD2:** SOX9'u yüksek tutup dişi belirleyici **WNT4'ü baskılar**.\n- **DMRT1 (9p24.3):** Delesyonunda 46,XY gonadal disgenezi görülür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Testis Geni", "Lokalizasyon", "Mutasyon veya Değişim Sonucu"],
                [
                    ["SRY", "Yp11.3", "Nokta mutasyonunda 46,XY Swyer sendromu; translokasyonda 46,XX erkek"],
                    ["SOX9", "17q24", "Heterozigot kayıpta Kampomelik displazi + 46,XY dişi fenotip"],
                    ["SF1 (NR5A1)", "9q33", "Gonadal agenezi/disgenezi + adrenal yetmezlik"],
                    ["WT1", "11p13", "Denys-Drash (Wilms) ve Frasier sendromu (gonadoblastom)"],
                    ["DMRT1", "9p24.3", "9p delesyonunda 46,XY CGB ve ambigus genitalya"]
                ]
            ),
            make_chain(
                "Testis Genetik Sinyal Kaskadı Özeti",
                [
                    "1. Giriş: 41. günde presertoli hücrelerinde SRY pik yapar.",
                    "2. Enhancer Bağlanması: SRY ve SF1, SOX9 geninin TESCO bölgesine bağlanır.",
                    "3. SOX9 Artışı: SOX9 transkripsiyonu başlar ve AMH genini aktive eder.",
                    "4. Parakrin Döngü: FGF9 ve PGD2 salgılanarak SOX9 yüksek tutulur ve WNT4 susturulur.",
                    "5. Testis Organizasyonu: Testis kordonları, Sertoli ve Leydig hücreleri şekillenir."
                ]
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-19-s20",
        "title": "Bölüm Özeti: Testis Yolundan Over Farklılaşma Genlerine Geçiş",
        "content": "Bölüm 2 boyunca testis farklılaşmasında rol oynayan kritik genleri ve sendromları inceledik:\n\n- **Özet:** Erkek cinsiyet gelişimi SRY $\\to$ SOX9 $\\to$ FGF9/AMH aksıyla yürütülür; bu yoldaki bozukluklar Kampomelik displazi, Swyer, Denys-Drash ve Frasier tablolarına yol açar.\n- **Sonraki Bölüm (Bölüm 3):** Over gelişiminin 'pasif bir varsayılan yol' olmadığını, **WNT4, RSPO1, CTNNB1 (β-katenin), FOXL2 (BPES sendromu) ve DAX1 (Xp21 kopya sayısı artışı)** gibi aktif genetik mekanizmalarla yönetildiğini inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "SRY geni bulunmasa dahi tek başına duplikasyonu 46,XX bireyde erkek gelişimini sağlayabilen otozomal gen hangisidir?",
                "SOX9",
                "17q24 kromozomunda yer alan ve TESCO enhancer ile kontrol edilen gen"
            ),
            make_quiz(
                "İntron 9 splice bölgesi mutasyonu sonucu fokal segmental glomerüloskleroz, 46,XY tam gonadal disgenezi ve yüksek gonadoblastom riski ile karakterize klinik tablo hangisidir?",
                [
                    {"key": "A", "text": "Frasier Sendromu", "isCorrect": True, "explanation": "Doğru cevap A'dır: WT1 geninin intron 9 splice mutasyonu Frasier sendromunun genetik temelidir."},
                    {"key": "B", "text": "Denys-Drash Sendromu", "isCorrect": False, "explanation": "Denys-Drash ekzon 8-9 missense mutasyonudur ve Wilms tümörü ile seyreder."},
                    {"key": "C", "text": "Swyer Sendromu", "isCorrect": False, "explanation": "Swyer SRY gen mutasyonuna bağlıdır."},
                    {"key": "D", "text": "Kampomelik Displazi", "isCorrect": False, "explanation": "Kampomelik displazi SOX9 mutasyonudur."}
                ]
            )
        ]
    })

    return slides
