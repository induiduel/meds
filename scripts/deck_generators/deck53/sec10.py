# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec10():
    slides = []

    # Slide 91: Endometrium Karsinomu Epidemiyolojisi ve İki Ana Tip
    s91_narrative = (
        "Endometrium karsinomu, gelişmiş toplumlarda kadın sağlığını tehdit eden en yaygın jinekolojik malignitedir.\n\n"
        "- **En Sık Kanser:** Birleşik Devletler ve birçok Batı ülkesinde **kadın genital sisteminin "
        "en sık izlenen tümörü endometrium karsinomudur**.\n"
        "- **Pik Yaş Grubu:** Genellikle **55-65 yaş arasında** görülür ve 40 yaşın altında oldukça nadirdir.\n"
        "- **İki Önemli Alt Tip:** Histolojik, moleküler ve klinik davranış açısından birbirinden tamamen "
        "farklı iki ana kategoriye ayrılır: **Tip I (Endometrioid) ve Tip II (Seröz ve berrak hücreli) karsinom**.\n"
        "- **Patogenetik Farklılık:** Tip I östrojen bağımlı hiperplastik bir yolda ilerlerken; Tip II "
        "östrojenden bağımsız atrofik bir zemin üzerinde gelişir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kadın genital sisteminin en sık izlenen malign tümörü endometrium karsinomudur; genellikle 55-65 yaş arasında görülür; iki tipi endometrioid ve seröz karsinomdur."
    )
    s91_bullets = [
        "Kadın genital sisteminin en sık izlenen tümörü endometrium karsinomudur.",
        "Genellikle 55-65 yaş arasında görülür; 40 yaş altında nadirdir.",
        "İki ana alt tipi vardır: endometrioid (Tip I) ve seröz (Tip II) karsinom."
    ]
    s91_elements = [
        make_cloze("Birleşik Devletler ve birçok Batı ülkesinde kadın genital sisteminin en sık izlenen tümörü endometrium karsinomudur.", "endometrium karsinomudur", "Kadın genital sisteminin en sık tümörü"),
        make_table("Endometrium Karsinomu Temel Epidemiyolojisi", ["Parametre", "Değer / Durum", "Klinik Önemi"], [
            {"cells": [{"text": "Görülme Sıklığı", "isMasked": False}, {"text": "Kadın genital sisteminin en sık tümörü", "isMasked": True, "hint": "en yaygın genital malignite"}, {"text": "Serviks ve over kanserinden daha sık"}]},
            {"cells": [{"text": "Pik Görülme Yaşı", "isMasked": False}, {"text": "55-65 yaş arası", "isMasked": False}, {"text": "Postmenopozal dönem", "isMasked": True, "hint": "elli beş altmış beş yaş"}]},
            {"cells": [{"text": "Ana Alt Tipleri", "isMasked": False}, {"text": "Tip I (Endometrioid) ve Tip II (Seröz)", "isMasked": False}, {"text": "Farklı patogenetik yolaklar"}]}
        ]),
        make_chain("Endometrium Karsinomu Epidemiyolojik Çerçeve", [
            "1. Demografik Dağılım: Genellikle 55-65 yaş grubundaki kadınlarda saptanır.",
            "2. En Yüksek İnsidans: Batı toplumlarında en sık görülen kadın genital kanseridir.",
            "3. İkili Sınıflama: Patolojik ve moleküler olarak Tip I ve Tip II ayrımı yapılır.",
            "4. Erken Semptom: Hastaların çoğu postmenopozal kanama ile erken evrede yakalanır."
        ]),
        make_recall("Kadın genital sisteminin en sık görülen malign tümörü hangisidir ve genellikle hangi yaş aralığında ortaya çıkar?", "Endometrium karsinomudur; genellikle 55-65 yaş arasında görülür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrium Kanseri Epidemiyolojisi", [
            {"text": "Kadın genital sisteminin en sık izlenen tümörü endometrium karsinomudur.", "isLie": False, "explanation": "Doğru. Batı ülkelerinde 1. sıradadır."},
            {"text": "Genellikle 55-65 yaş arasında görülür.", "isLie": False, "explanation": "Doğru. Pik yaşıdır."},
            {"text": "Endometrium karsinomu sadece 10 yaşındaki çocuklarda görülür, 50 yaş üzerinde kesinlikle imkansızdır.", "isLie": True, "explanation": "Tuzak! 40 yaş altında nadirdir; hastaların ezici çoğunluğu 55-65 yaş aralığındaki postmenopozal kadınlardır."},
            {"text": "Endometrioid ve seröz olmak üzere iki önemli alt tipi vardır.", "isLie": False, "explanation": "Doğru. İkili sınıflamadır."}
        ]),
        make_quiz("Kadın genital sisteminin en sık izlenen malign tümörü ve en sık görüldüğü yaş grubu hangisidir?", [
            {"key": "A", "text": "Endometrium karsinomu; genellikle 55-65 yaş arası", "isCorrect": True, "explanation": "Ders notunda açıkça: 'kadın genital sisteminin en sık izlenen tümörü endometrium karsinomudur; genellikle 55-65 yaş arasında görülür' denmektedir."},
            {"key": "B", "text": "Serviks karsinomu; genellikle 15-20 yaş arası", "isCorrect": False, "explanation": "En sık olan endometrium karsinomudur."},
            {"key": "C", "text": "Over disgerminomu; sadece 80 yaş üstü", "isCorrect": False, "explanation": "Genç yaş tümörüdür."},
            {"key": "D", "text": "Vajina sarkomu; 0-5 yaş arası", "isCorrect": False, "explanation": "Çok nadir bir tümördür."}
        ])
    ]
    slides.append(make_slide(91, "Endometrium Karsinomu Epidemiyolojisi ve İki Ana Tip", "En sık kadın genital tümörü, 55-65 yaş zirvesi ve Tip I endometrioid vs Tip II seröz sınıflaması", "Onkoloji", s91_narrative, s91_bullets, s91_elements))

    # Slide 92: Tip 1 ve Tip 2 Karsinom Karşılaştırma Tablosu
    s92_narrative = (
        "Endometrium karsinomunun Tip I ve Tip II ayrımı, tümörün biyolojik davranışını ve tedavisini belirler.\n\n"
        "- **Tip I (Endometrioid):** **Dengelenmemiş östrojen** etkisi altındadır; **pre- ve perimenopozal** "
        "kadınlarda izlenir; öncü lezyonu **atipik hiperplazi**dir; tümör derecesi genellikle **düşük**tür; "
        "miyometrial invazyon sıklıkla minimaldir; seyri **yavaş (indolent)**tir; PTEN, mikrosatellit "
        "instabilite (MMR) ve K-ras mutasyonları içerir.\n"
        "- **Tip II (Seröz ve Berrak Hücreli):** Dengelenmemiş östrojenle **ilişkisizdir**; **postmenopozal** "
        "daha yaşlı kadınlarda görülür; öncü lezyonu **seröz endometrial intraepitelyal karsinom (SEIC)**dur; "
        "tümör derecesi **yüksek**tir; miyometrial invazyon sıklıkla derindir; seyri son derece **agresif**tir; "
        "mutasyonel profili **TP53 mutasyonu** ile karakterizedir.\n\n"
        "> [!IMPORTANT]\n"
        "> [KRİTİK KARŞILAŞTIRMA] Tip I: östrojen bağımlı, atipik hiperplazi öncüllü, indolent, PTEN/MMR; Tip II: östrojensiz atrofi zeminli, SEIC öncüllü, yüksek dereceli, agresif, TP53 mutasyonlu."
    )
    s92_bullets = [
        "Tip I: dengelenmemiş östrojen var, öncü atipik hiperplazi, düşük derece, indolent, PTEN/MMR/K-ras.",
        "Tip II: östrojen yok (atrofi zemininde), öncü SEIC, yüksek derece, agresif, TP53 mutasyonu.",
        "Tip I pre/perimenopozda, Tip II daha yaşlı postmenopozal kadınlarda gelişir."
    ]
    s92_elements = [
        make_cloze("Tip I karsinomda öncü lezyon atipik hiperplazi iken Tip II karsinomda seröz endometrial intraepitelyal karsinomdur.", "atipik hiperplazi", "Tip I endometrioid karsinomun öncü lezyonu"),
        make_table("Tip I ve Tip II Endometrium Karsinomu Karşılaştırması", ["Özellik", "Tip I (Endometrioid)", "Tip II (Seröz)"], [
            {"cells": [{"text": "Dengelenmemiş Östrojen", "isMasked": False}, {"text": "Var", "isMasked": False}, {"text": "Yok (Atrofi zemininde)", "isMasked": True, "hint": "hormonsuz zemin"}]},
            {"cells": [{"text": "Öncü Lezyon", "isMasked": False}, {"text": "Atipik hiperplazi", "isMasked": True, "hint": "atipili hiperplazi"}, {"text": "SEIC (Seröz intraepitelyal karsinom)"}]},
            {"cells": [{"text": "Tümör Derecesi ve Seyir", "isMasked": False}, {"text": "Düşük derece, yavaş (indolent)", "isMasked": False}, {"text": "Yüksek derece, agresif", "isMasked": True, "hint": "kötü huylu ve hızlı"}]},
            {"cells": [{"text": "Temel Genetik Mutasyon", "isMasked": False}, {"text": "PTEN, MMR instabilite, K-ras", "isMasked": False}, {"text": "TP53 mutasyonu", "isMasked": True, "hint": "tümör baskılayıcı p53"}]}
        ]),
        make_chain("İkili Karsinogenez Yolağı", [
            "1. Tip I Yolu: Hiperöstrojenizm → Atipik Hiperplazi → PTEN mutasyonu → Düşük dereceli adenokarsinom.",
            "2. Tip II Yolu: Endometrial Atrofi → TP53 mutasyonu → SEIC → Agresif seröz karsinom.",
            "3. Davranış Farkı: Tip I indolent ve minimal invaziv seyrederken Tip II derin invazyon yapar.",
            "4. Klinik Sonuç: Tip II olguları daha erken metastaz ve kötü prognozla sonlanır."
        ]),
        make_recall("Tip I ve Tip II endometrium karsinomunun öncü lezyonları ve temel genetik mutasyonları nelerdir?", "Tip I: öncü lezyon atipik hiperplazi, mutasyonlar PTEN/MMR/K-ras; Tip II: öncü lezyon SEIC (seröz intraepitelyal karsinom), mutasyon TP53'tür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tip I vs Tip II Karsinom", [
            {"text": "Tip I karsinom dengelenmemiş östrojen maruziyeti ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Tip I zeminidir."},
            {"text": "Tip II seröz karsinomlarda TP53 mutasyonları baskındır.", "isLie": False, "explanation": "Doğru. Karakteristik genetiğidir."},
            {"text": "Tip II karsinom her zaman düşük dereceli ve tamamen selim bir siğildir.", "isLie": True, "explanation": "Tuzak! Tip II seröz karsinom yüksek dereceli, agresif ve mortalitesi yüksek bir kanserdir."},
            {"text": "Tip I karsinomun öncü lezyonu atipik hiperplazidir.", "isLie": False, "explanation": "Doğru. Ders notu tablosu verisidir."}
        ]),
        make_quiz("Tip I (endometrioid) ve Tip II (seröz) endometrium karsinomunun genetik mutasyon profili hangisinde DOĞRU verilmiştir?", [
            {"key": "A", "text": "Tip I: PTEN, mikrosatellit instabilite, K-ras | Tip II: TP53 mutasyonu", "isCorrect": True, "explanation": "Ders notu karşılaştırma tablosunda genetik değişiklikler tam olarak bu şekilde verilmiştir."},
            {"key": "B", "text": "Tip I: Sadece TP53 | Tip II: Hiçbir mutasyon içermez", "isCorrect": False, "explanation": "Ters ve hatalıdır."},
            {"key": "C", "text": "Her iki tipte de yalnızca BCR-ABL füzyonu görülür", "isCorrect": False, "explanation": "KML translokasyonudur."},
            {"key": "D", "text": "Tip I ve Tip II tamamen aynı genetik mutasyonlara sahiptir", "isCorrect": False, "explanation": "Moleküler olarak apayrı yollardır."}
        ])
    ]
    slides.append(make_slide(92, "Tip 1 ve Tip 2 Karsinom Karşılaştırma Tablosu", "Östrojen bağımlılığı, menopoz durumu, öncü lezyonlar (atipik hiperplazi vs SEIC) ve genetik mutasyonlar", "Onkoloji ve Patoloji", s92_narrative, s92_bullets, s92_elements))

    # Slide 93: Tip 1 Endometrioid Karsinom (%80) ve Hiperöstrojenizm
    s93_narrative = (
        "Tip 1 endometrioid karsinom, tüm endometrium kanserlerinin ezici çoğunluğunu oluşturur.\n\n"
        "- **İnsidans Oranı:** **Endometrium karsinomlarının %80'i endometrioid tipten oluşmaktadır**.\n"
        "- **İsim Kökeni:** Histolojik olarak normal endometrium gland yapılarına benzemelerinden "
        "dolayı **endometrioid** olarak adlandırılırlar.\n"
        "- **Risk Zeminleri:** En önemli risk faktörü **dengelenmemiş östrojen maruziyeti**dir; "
        "uzun süreli östrojen replasman tedavisi, östrojen salgılayan over tümörleri, obezite ve PCOS riski artırır.\n"
        "- **Meme Kanseri Birlikteliği:** Meme kanseri de östrojen bağımlı bir tümör olduğundan, "
        "**meme kanserli kadınlarda endometrium kanseri daha sık gelişir**.\n"
        "- **Klinik Seyir:** Perimenopozal dönemde atipik hiperplazi zemininde gelişir; genellikle "
        "yavaş seyirli olup erken evrede anormal kanama verir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometrium kanserlerinin %80'i endometrioid tiptir; östrojen fazlalığı ve hiperplazi zemininde gelişir; meme kanserli kadınlarda risk artmıştır."
    )
    s93_bullets = [
        "Endometrium karsinomlarının %80'i endometrioid tipten oluşur.",
        "Normal endometrial bez yapılarına benzerliği nedeniyle endometrioid denir.",
        "Dengelenmemiş östrojen ana nedendir; meme kanserli kadınlarda daha sık gelişir."
    ]
    s93_elements = [
        make_cloze("Endometrium karsinomlarının %80'i endometrioid tipten oluşmaktadır ve dengelenmemiş östrojen maruziyetiyle ilişkilidir.", "%80'i", "Endometrioid karsinomun tüm kanserler içindeki oranı"),
        make_table("Tip 1 Endometrioid Karsinom Profili", ["Parametre", "Özellik / Oran", "Klinik Yansıması"], [
            {"cells": [{"text": "Tüm Kanserlerdeki Payı", "isMasked": False}, {"text": "%80 (ezici çoğunluk)", "isMasked": True, "hint": "yüzde seksenlik oran"}, {"text": "En sık karşılaşılan tip"}]},
            {"cells": [{"text": "Tetikleyici Zemin", "isMasked": False}, {"text": "Dengelenmemiş östrojen ve hiperplazi", "isMasked": False}, {"text": "Hormon bağımlı karsinogenez", "isMasked": True, "hint": "karşılanmamış hormon"}]},
            {"cells": [{"text": "İlişkili Neoplazi", "isMasked": False}, {"text": "Meme kanseri birlikteliği", "isMasked": False}, {"text": "Ortak östrojen bağımlı patogenez"}]}
        ]),
        make_chain("Endometrioid Karsinom Gelişim Aşamaları", [
            "1. Kronik Östrojen: Obezite veya anovulasyonla karşılanmamış östrojen birikir.",
            "2. Atipik Hiperplazi: Endometriumda preneoplastik glandüler proliferasyon başlar.",
            "3. Malign Dönüşüm: Endometrioid karsinom (%80 sıklık) gelişir.",
            "4. Postmenopozal Kanama: Erken evrede kanama vererek kliniğe başvuruyu sağlar."
        ]),
        make_recall("Endometrium kanserlerinin yüzde kaçı endometrioid tipten oluşur ve hangi kansere sahip kadınlarda daha sık gelişir?", "%80'i endometrioid tipten oluşur; östrojen bağımlı olduğu için meme kanserli kadınlarda daha sık gelişir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrioid Karsinom", [
            {"text": "Endometrium karsinomlarının %80'i endometrioid tipten oluşmaktadır.", "isLie": False, "explanation": "Doğru. Ezici çoğunluktur."},
            {"text": "Dengelenmemiş östrojen maruziyeti en önemli risk faktörüdür.", "isLie": False, "explanation": "Doğru. Tip I zeminidir."},
            {"text": "Endometrioid karsinom sadece erkeklerde görülen bir karaciğer kanseridir.", "isLie": True, "explanation": "Tuzak! Kadınlarda uterus mukozasının en sık malign tümörüdür."},
            {"text": "Meme kanserli kadınlarda endometrium kanseri daha sık gelişir.", "isLie": False, "explanation": "Doğru. Ortak hormonal zemindir."}
        ]),
        make_quiz("Endometrium karsinomlarının yaklaşık yüzde kaçını endometrioid tip oluşturur ve hangi malignite ile sık birliktelik gösterir?", [
            {"key": "A", "text": "%80'ini oluşturur; meme kanseri ile birliktelik gösterir", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'endometrium karsinomlarının %80'i endometrioid tipten oluşmaktadır... ek olarak meme kanseri endometrium kanserli kadınlarda daha sık gelişir' denmektedir."},
            {"key": "B", "text": "%1'ini oluşturur; sadece glioblastoma ile birliktedir", "isCorrect": False, "explanation": "Oran %80'dir."},
            {"key": "C", "text": "%100'ünü oluşturur; akciğer kanseri ile birliktedir", "isCorrect": False, "explanation": "Seröz tip %15'tir."},
            {"key": "D", "text": "Yalnızca %5'ini oluşturur; hiçbir hastalıkla ilişkisizdir", "isCorrect": False, "explanation": "En sık tiptir."}
        ])
    ]
    slides.append(make_slide(93, "Tip 1 Endometrioid Karsinom (%80) ve Hiperöstrojenizm", "%80 prevalans, bez benzerliği, dengelenmemiş östrojen maruziyeti ve meme kanseri birlikteliği", "Onkoloji", s93_narrative, s93_bullets, s93_elements))

    # Slide 94: Moleküler Genetik: PTEN, Mismatch Repair (Lynch) ve Cowden
    s94_narrative = (
        "Tip 1 endometrioid karsinom patogenezinde özgül tümör baskılayıcı ve DNA onarım genleri erken aşamada devre dışı kalır.\n\n"
        "- **Erken Dönem Olayları:** Endometrioid karsinomun adım adım gelişiminde **uyuşmazlık tamir "
        "(mismatch repair - MMR) genleri ile tümör baskılayıcı PTEN geninde izlenen mutasyonlar erken dönem olaylarıdır**.\n"
        "- **PTEN ve Cowden Sendromu:** PTEN geninde germline (kalıtsal) mutasyon içeren **Cowden sendromlu** "
        "kadınlarda endometrial karsinom riski belirgin şekilde yüksektir.\n"
        "- **MMR ve Lynch Sendromu:** DNA uyuşmazlık tamir genlerinde (MLH1, MSH2, MSH6, PMS2) "
        "germline değişiklikler olan **Lynch sendromlu (HNPCC)** kadınlarda endometrial kanser riski dramatik artmıştır.\n"
        "- **K-ras ve Geç P53:** Ek olarak K-ras mutasyonları sık izlenirken; TP53 mutasyonları nadirdir "
        "ve patogenezin geç döneminde ortaya çıkar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] PTEN ve mismatch repair (MMR) mutasyonları erken dönem olaylarıdır; Cowden (PTEN) ve Lynch (MMR) sendromlarında risk çok yüksektir; K-ras da eşlik eder."
    )
    s94_bullets = [
        "Uyuşmazlık tamir (MMR) genleri ve PTEN mutasyonları erken dönem olaylarıdır.",
        "PTEN germline mutasyonu olan Cowden sendromunda risk yüksektir.",
        "MMR germline mutasyonu olan Lynch sendromunda risk yüksektir; K-ras mutasyonu da eşlik eder."
    ]
    s94_elements = [
        make_cloze("Endometrioid karsinom gelişiminde uyuşmazlık tamir genleri ile tümör baskılayıcı PTEN geninde izlenen mutasyonlar erken dönem olaylarıdır.", "erken dönem olaylarıdır", "PTEN ve MMR mutasyonlarının gelişimdeki zamanı"),
        make_table("Endometrioid Karsinom Moleküler Genetiği", ["Gen / Yolak", "İlişkili Herediter Sendrom", "Biyolojik Etki"], [
            {"cells": [{"text": "PTEN Tümör Baskılayıcı", "isMasked": False}, {"text": "Cowden sendromu", "isMasked": True, "hint": "PTEN germline sendromu"}, {"text": "PI3K/AKT yolağının aşırı aktivasyonu"}]},
            {"cells": [{"text": "Uyuşmazlık Tamir (MMR)", "isMasked": False}, {"text": "Lynch sendromu (HNPCC)", "isMasked": False}, {"text": "Mikrosatellit instabilite (MSI)", "isMasked": True, "hint": "DNA tamir defekti"}]},
            {"cells": [{"text": "K-ras Onkogeni", "isMasked": False}, {"text": "Sporadik olgular", "isMasked": False}, {"text": "MAPK proliferasyon sinyali"}]}
        ]),
        make_chain("Moleküler Karsinogenez Basamakları", [
            "1. Erken İkinci Vuruş: Endometrial bezlerde PTEN inaktivasyonu gerçekleşir.",
            "2. MMR Defekti: DNA replikasyon hataları düzeltilemez ve mikrosatellit instabilite oluşur.",
            "3. K-ras Aktivasyonu: Hücresel çoğalma otonom hale gelir.",
            "4. Malignite: İnvaziv endometrioid adenokarsinom fenotipi şekillenir."
        ]),
        make_recall("Endometrioid karsinom patogenezinde erken dönemde rol oynayan iki temel genetik mekanizma ve ilişkili herediter sendromlar nelerdir?", "Uyuşmazlık tamir (MMR) gen mutasyonları (Lynch sendromu) ve PTEN gen mutasyonlarıdır (Cowden sendromu)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Moleküler Genetik", [
            {"text": "MMR genleri ve PTEN mutasyonları erken dönem olaylarıdır.", "isLie": False, "explanation": "Doğru. Tip I erken adımlarıdır."},
            {"text": "Cowden sendromlu kadınlarda karsinom gelişim riski daha yüksektir.", "isLie": False, "explanation": "Doğru. PTEN mutasyonudur."},
            {"text": "Lynch sendromlu kadınlarda endometrial kanser gelişme riski tamamen sıfırdır.", "isLie": True, "explanation": "Tuzak! Lynch sendromlu kadınlarda kolorektal kanserden sonra en sık görülen tümör endometrium kanseridir ve risk çok yüksektir."},
            {"text": "TP53 mutasyonları endometrioid karsinomda geç dönemde ortaya çıkar.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Tip 1 endometrioid karsinomun adım adım gelişiminde erken dönemde mutasyona uğrayan genler ve ilişkili sendromlar hangileridir?", [
            {"key": "A", "text": "PTEN (Cowden sendromu) ve Mismatch Repair / MMR (Lynch sendromu)", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'uyuşmazlık tamir genleri ile PTEN geninde izlenen mutasyonlar erken dönem olaylarıdır; Cowden ve Lynch sendromlarında risk yüksektir' denmektedir."},
            {"key": "B", "text": "BRCA1 (Down sendromu)", "isCorrect": False, "explanation": "Eşleşme yanlıştır."},
            {"key": "C", "text": "Yalnızca distrofin geni (Duchenne)", "isCorrect": False, "explanation": "Kas distrofisi genidir."},
            {"key": "D", "text": "Sadece insülin reseptör geni", "isCorrect": False, "explanation": "Diyabetle ilgilidir."}
        ])
    ]
    slides.append(make_slide(94, "Moleküler Genetik: PTEN, Mismatch Repair (Lynch) ve Cowden", "PTEN inaktivasyonu, Cowden sendromu, DNA uyuşmazlık tamiri (Lynch sendromu) ve K-ras mutasyonları", "Moleküler Patoloji", s94_narrative, s94_bullets, s94_elements))

    # Slide 95: Tip 2 Seröz Karsinom (%15), Atrofi Zemini ve Agresif Seyir
    s95_narrative = (
        "Tip 2 seröz karsinom, endometrium kanserlerinin daha az rastlanan fakat klinik olarak en ölümcül alt tipidir.\n\n"
        "- **Sıklık ve Agresiflik:** Endometrium karsinomlarının **yaklaşık %15'ini oluşturur, nadir "
        "olmasına karşın çok daha agresiftir**.\n"
        "- **Hormonsuz Zemin:** Dengelenmemiş östrojen ya da endometrial hiperplazi ile kesinlikle "
        "**ilişkili değildir**.\n"
        "- **Atrofik Zemin:** Postmenopozal dönemdeki daha yaşlı kadınlarda **endometrial atrofi "
        "zemininde** gelişir.\n"
        "- **Derin Yayılım:** Erken evrede bile lenfovasküler invazyon, derin miyometrial tutulum "
        "ve peritoneal ekim yapma potansiyeli taşır.\n"
        "- **Mortalite:** Tüm endometrium kanseri ölümlerinin yarısından fazlasından bu küçük seröz grup sorumludur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Seröz karsinom yaklaşık %15 oranında görülür; östrojen ve hiperplazi ile ilişkisizdir; yaşlı kadınlarda atrofi zemininde gelişir ve çok agresiftir."
    )
    s95_bullets = [
        "Nadir olup yaklaşık %15 oranında görülür, çok daha agresiftir.",
        "Dengelenmemiş östrojen ya da endometrial hiperplazi ile ilişkili değildir.",
        "Postmenopozal yaşlı kadınlarda endometrial atrofi zemininde gelişir."
    ]
    s95_elements = [
        make_cloze("Seröz karsinom nadir olup yaklaşık %15 oranında görülür, atrofi zemininde gelişir ve çok daha agresiftir.", "çok daha agresiftir", "Seröz karsinomun klinik seyir niteliği"),
        make_table("Tip 2 Seröz Karsinom Temel Özellikleri", ["Kriter", "Özellik", "Klinik Yansıması"], [
            {"cells": [{"text": "Görülme Oranı", "isMasked": False}, {"text": "Yaklaşık %15", "isMasked": True, "hint": "yüzde on beş"}, {"text": "Azınlıkta fakat ölümcül"}]},
            {"cells": [{"text": "Hormonal Bağımlılık", "isMasked": False}, {"text": "Östrojen ile ilişkili değildir", "isMasked": False}, {"text": "Karşılanmamış hormon yok"}]},
            {"cells": [{"text": "Zemin Endometrium", "isMasked": False}, {"text": "Endometrial atrofi", "isMasked": True, "hint": "incelmiş yaşlı mukoza"}, {"text": "İleri yaşlı postmenopozal kadınlar"}]}
        ]),
        make_chain("Seröz Karsinogenez Akışı", [
            "1. İleri Yaş ve Atrofi: Endometrium atrofik, hormonsuz durumdadır.",
            "2. Genetik Hasar: Atrofik epitelde de novo mutasyonlar başlar.",
            "3. İntraepitelyal Faz: Yüzeyde yayılmadan önce atipik hücreler ürer.",
            "4. Erken Metastaz: Tümör kütle yapmadan derin miyometrium ve peritona yayılır."
        ]),
        make_recall("Seröz tip endometrium karsinomu hangi sıklıkta görülür, hangi doku zemininde gelişir ve klinik seyri nasıldır?", "Yaklaşık %15 oranında görülür; östrojenle ilişkisiz olup endometrial atrofi zemininde gelişir ve çok daha agresiftir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Seröz Karsinom Özellikleri", [
            {"text": "Seröz karsinom yaklaşık %15 oranında görülür.", "isLie": False, "explanation": "Doğru. Sıklık oranıdır."},
            {"text": "Çok daha agresiftir.", "isLie": False, "explanation": "Doğru. Yüksek derecelidir."},
            {"text": "Seröz karsinom aşırı östrojen salgısı ve devasa endometrial hiperplazi zemininde gelişir.", "isLie": True, "explanation": "Tuzak! Seröz karsinom östrojen veya hiperplazi ile ilişkili DEĞİLDİR; yaşlı kadınlarda endometrial ATROFİ zemininde gelişir."},
            {"text": "Postmenopozal dönemdeki yaşlı kadınlarda izlenir.", "isLie": False, "explanation": "Doğru. Yaş grubudur."}
        ]),
        make_quiz("Tip 2 seröz karsinomun görülme oranı, zemin durumu ve klinik davranışı ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Yaklaşık %15 oranında görülür; östrojenle ilişkisizdir, atrofi zemininde gelişir ve çok agresiftir", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'nadir olup yaklaşık %15 oranında görülür, çok daha agresiftir; dengelenmemiş östrojen ya da endometrial hiperplazi ile ilişkili değildir; endometrial atrofi zemininde gelişir' denmektedir."},
            {"key": "B", "text": "%80 oranında görülür; genç kızlarda ovulasyonla iyileşir", "isCorrect": False, "explanation": "Bu endometrioid tip oranıdır."},
            {"key": "C", "text": "Tamamen selim bir kıkırdak lezyonudur", "isCorrect": False, "explanation": "Malign karsinomdur."},
            {"key": "D", "text": "Yalnızca gebelik sırasında ortaya çıkar", "isCorrect": False, "explanation": "İleri yaşta görülür."}
        ])
    ]
    slides.append(make_slide(95, "Tip 2 Seröz Karsinom (%15), Atrofi Zemini ve Agresif Seyir", "%15 oran, östrojenden bağımsızlık, atrofik zemin, erken invazyon ve agresif klinik seyir", "Onkoloji", s95_narrative, s95_bullets, s95_elements))

    # Slide 96: TP53 Mutasyonu, Diffüz p53 Boyanması ve SEIC Öncülü
    s96_narrative = (
        "Tip 2 seröz karsinomun ayırt edici moleküler ve morfolojik özellikleri oldukça belirgindir.\n\n"
        "- **TP53 Hakimiyeti:** Olguların **tama yakınında TP53 tümör baskılayıcı gen mutasyonları saptanır**; "
        "buna karşılık MMR ve PTEN mutasyonları seyrektir.\n"
        "- **Öncü Lezyon (SEIC):** Seröz karsinomların **seröz endometrial intraepitelyal karsinom (SEIC)** "
        "olarak tanımlanan bir öncü lezyonu vardır; SEIC'te TP53 mutasyonunun saptanması, bu olayın "
        "patogenezde **erken dönemde** yer aldığını gösterir.\n"
        "- **İHK Diffüz p53:** İmmünohistokimyasal boyamada seröz karsinom hücrelerinde **genellikle "
        "diffüz ve kuvvetli p53 boyanması** izlenir.\n"
        "- **Boyanma Mekanizması:** Missense mutasyona uğrayan mutant p53 proteini degrade edilemeyip "
        "çekirdekte biriktiği için immün boyama ile kolayca ve güçlü şekilde saptanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Seröz karsinomda tama yakınında TP53 mutasyonu vardır; öncü lezyonu SEIC'tir; İHK'da diffüz ve kuvvetli p53 boyanması gösterir."
    )
    s96_bullets = [
        "Olguların tama yakınında TP53 tümör baskılayıcı gen mutasyonu saptanır.",
        "Öncü lezyonu seröz endometrial intraepitelyal karsinomdur (SEIC).",
        "İmmünohistokimyada genellikle diffüz ve kuvvetli p53 boyanması gösterir."
    ]
    s96_elements = [
        make_cloze("Seröz karsinomların seröz endometrial intraepitelyal karsinom (SEIC) olarak tanımlanan öncüsü olup tama yakınında TP53 mutasyonları saptanır.", "TP53 mutasyonları", "Seröz karsinomda tama yakınında saptanan genetik defekt"),
        make_table("Seröz Karsinom Moleküler ve İHK Belirteçleri", ["Parametre", "Bulgu", "Klinik Önemi"], [
            {"cells": [{"text": "Primer Gen Mutasyonu", "isMasked": False}, {"text": "TP53 gen mutasyonu (tama yakınında)", "isMasked": True, "hint": "p53 geninde hasar"}, {"text": "Genomik instabilite ve agresiflik"}]},
            {"cells": [{"text": "Öncü Lezyon", "isMasked": False}, {"text": "SEIC (seröz intraepitelyal karsinom)", "isMasked": False}, {"text": "Atrofik yüzeyde erken evre", "isMasked": True, "hint": "karsinom öncülü epitel"}]},
            {"cells": [{"text": "İHK Boyanma Paterni", "isMasked": False}, {"text": "Diffüz ve kuvvetli nükleer p53 pozitifliği", "isMasked": False}, {"text": "Tanısal patolojik teyit"}]}
        ]),
        make_chain("TP53 ve SEIC Karsinogenez Zinciri", [
            "1. Atrofik Epitel: Atrofik hücrelerde TP53 mutasyonu ortaya çıkar.",
            "2. SEIC Gelişimi: Yüzey epitelinde SEIC öncü lezyonu şekillenir.",
            "3. Mutant p53 Birikimi: Hücre nükleuslarında p53 aşırı birikir.",
            "4. Agresif Seröz Karsinom: Papiller yapılar ve derin invazyon ile tümör yayılır."
        ]),
        make_recall("Seröz tip endometrium karsinomunda olguların tama yakınında görülen mutasyon, öncü lezyonunun adı ve İHK boyanma özelliği nedir?", "TP53 mutasyonudur; öncü lezyonu SEIC'tir (seröz endometrial intraepitelyal karsinom); İHK'da diffüz ve kuvvetli p53 boyanması gösterir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: TP53 ve SEIC", [
            {"text": "Seröz karsinomların tama yakınında TP53 mutasyonları saptanır.", "isLie": False, "explanation": "Doğru. Moleküler imzasıdır."},
            {"text": "Öncü lezyonu seröz endometrial intraepitelyal karsinomdur (SEIC).", "isLie": False, "explanation": "Doğru. Prekürsörüdür."},
            {"text": "Seröz karsinomlarda p53 immün boyaması her zaman kesinlikle sıfırdır, asla boyanmaz.", "isLie": True, "explanation": "Tuzak! Seröz karsinomlarda mutant p53 biriktiği için genellikle DİFFÜZ ve KUVVETLİ p53 boyanması gösterir."},
            {"text": "DNA uyuşmazlık tamir genleri ve PTEN mutasyonları seröz karsinomda seyrektir.", "isLie": False, "explanation": "Doğru. Tip I'den farkıdır."}
        ]),
        make_quiz("Seröz karsinomun öncü lezyonu, temel gen mutasyonu ve immünohistokimyasal özelliği hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Öncü lezyon SEIC; TP53 mutasyonu; diffüz ve kuvvetli p53 boyanması", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'olguların tama yakınında TP53 mutasyonları saptanır... SEIC olarak tanımlanan bir öncü lezyonu vardır... diffüz ve kuvvetli p53 boyanması gösterir' denmektedir."},
            {"key": "B", "text": "Öncü lezyon basit polip; mutasyon yok; p53 negatif", "isCorrect": False, "explanation": "Polip SEIC değildir."},
            {"key": "C", "text": "Öncü lezyon kistik atrofi; APC mutasyonu; CDX2 pozitif", "isCorrect": False, "explanation": "Kolon kanseri profilidir."},
            {"key": "D", "text": "Öncü lezyon leydig hücresi; testosteron boyanması", "isCorrect": False, "explanation": "Testis patolojisidir."}
        ])
    ]
    slides.append(make_slide(96, "TP53 Mutasyonu, Diffüz p53 Boyanması ve SEIC Öncülü", "TP53 inaktivasyonu, seröz intraepitelyal karsinom (SEIC) ve diffüz nükleer p53 pozitifliği", "Moleküler Patoloji", s96_narrative, s96_bullets, s96_elements))

    # Slide 97: Morfolojik Özellikler: Glandüler Diferansiasyon vs Papiller Yapılar
    s97_narrative = (
        "Endometrioid ve seröz karsinomların mikroskopik mimarisi ve diferansiasyon paternleri birbirinden belirgin hatlarla ayrılır.\n\n"
        "- **Endometrioid Morfoloji:** Endometrioid karsinomlar **normal endometriuma benzer**; "
        "ekzofitik polipoid ya da derine infiltratif olabilirler.\n"
        "- **Farklı Diferansiasyonlar:** Endometrioid tümör dokusu içinde **müsinöz, tubal (silyalı) "
        "ve skuamöz (bazen adenoskuamöz)** diferansiasyon alanları sıkça izlenir.\n"
        "- **Seröz Morfoloji:** Seröz karsinomlarda endometrioid karsinomda izlenen düzgün tübüler "
        "glandlardan farklı olarak **papiller yapılar, psammom cisimcikleri ve küçük kümelenmeler** izlenir.\n"
        "- **Sitolojik Derece:** Seröz karsinomlarda sitolojik atipi çok belirgindir (pleomorfik dev çekirdekler); "
        "bu nedenle mimarisine bakılmaksızın **agresif davranırlar ve daima yüksek dereceli (High Grade)** kabul edilirler.\n\n"
        "> [!NOTE]\n"
        "> Endometrioid karsinomlar bez yapıları yapar; müsinöz, tubal ve skuamöz diferansiasyon gösterir. Seröz karsinomlar papiller yapılar yapar, sitolojik atipi çok belirgindir ve daima yüksek derecelidir."
    )
    s97_bullets = [
        "Endometrioid karsinom normal endometriuma benzer; müsinöz, tubal ve skuamöz diferansiasyon gösterebilir.",
        "Seröz karsinomda bezler yerine papiller yapılar ve küçük kümelenmeler izlenir.",
        "Seröz karsinomda sitolojik atipi çok belirgindir; agresiftir ve daima yüksek derecelidir."
    ]
    s97_elements = [
        make_cloze("Seröz karsinomlarda papiller yapılar ve küçük kümelenmeler izlenir, sitolojik atipi çok belirgindir ve yüksek dereceli kabul edilirler.", "yüksek dereceli", "Seröz karsinomların mutlak prognostik derecesi"),
        make_table("Endometrioid vs Seröz Morfolojik Karşılaştırma", ["Parametre", "Endometrioid Karsinom", "Seröz Karsinom"], [
            {"cells": [{"text": "Baskın Mimari", "isMasked": False}, {"text": "Tübüler bezler (glandlar)", "isMasked": True, "hint": "bez yapıları"}, {"text": "Papiller yapılar ve küçük kümeler"}]},
            {"cells": [{"text": "Eşlik Eden Diferansiasyon", "isMasked": False}, {"text": "Skuamöz, müsinöz, tubal", "isMasked": False}, {"text": "Psammom cisimcikleri eşlik edebilir", "isMasked": True, "hint": "kalsifiye cisimler"}]},
            {"cells": [{"text": "Sitolojik Atipi ve Derece", "isMasked": False}, {"text": "I ile III arası derecelendirilir", "isMasked": False}, {"text": "Daima belirgin atipili ve yüksek dereceli"}]}
        ]),
        make_chain("Mikroskopik Ayrım Algoritması", [
            "1. Düşük Büyütme: Tümör tübüler gland mı yoksa papiller yapılar mı yapıyor?",
            "2. Glandüler Görünüm: Bezler normal endometriuma benziyorsa Endometrioid tip düşünülür.",
            "3. Papiller ve Aşırı Atipi: Papiller çatılar ve pleomorfik dev nükleuslar varsa Seröz tip düşünülür.",
            "4. Derecelendirme: Endometrioid FIGO ile derecelendirilirken, seröz doğrudan High Grade atanır."
        ]),
        make_recall("Endometrioid karsinomda görülebilen farklı histolojik diferansiasyon tipleri nelerdir ve seröz karsinomun mimari yapısı nasıldır?", "Endometrioid tipte müsinöz, tubal ve skuamöz diferansiasyon görülür; seröz tipte ise papiller yapılar, küçük kümelenmeler ve belirgin sitolojik atipi (yüksek derece) izlenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Morfolojik Özellikler", [
            {"text": "Endometrioid karsinomlar müsinöz, tubal ve skuamöz diferansiasyon gösterebilir.", "isLie": False, "explanation": "Doğru. Morfolojik spektrumdur."},
            {"text": "Seröz karsinomlarda papiller yapılar ve belirgin sitolojik atipi izlenir.", "isLie": False, "explanation": "Doğru. Seröz paterndir."},
            {"text": "Seröz karsinomlar daima en masum, düşük dereceli ve hiç tedavi gerektirmeyen selim kistlerdir.", "isLie": True, "explanation": "Tuzak! Seröz karsinomlar agresif davranırlar ve daima YÜKSEK DERECELİ olarak değerlendirilirler."},
            {"text": "Endometrioid karsinomlar normal endometriuma benzer bezler oluşturur.", "isLie": False, "explanation": "Doğru. İsim kaynağıdır."}
        ]),
        make_quiz("Seröz karsinomun mikroskopik mimarisi ve sitolojik derecesi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Papiller yapılar ve küçük kümelenmeler izlenir, sitolojik atipi çok belirgindir ve yüksek derecelidir", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'seröz karsinomlarda papiller yapılar ve küçük kümelenmeler izlenir, ayrıca sitolojik atipi çok belirgindir; agresif davranırlar ve yüksek dereceli olarak değerlendirilirler' denmektedir."},
            {"key": "B", "text": "Tamamen düz tübüler bezlerden oluşur ve Grade 0'dır", "isCorrect": False, "explanation": "Papiller yapıdadır."},
            {"key": "C", "text": "Hiçbir zaman nükleer atipi içermez", "isCorrect": False, "explanation": "Atipi çok belirgindir."},
            {"key": "D", "text": "Sadece yağ hücrelerinden oluşan benign bir lipomdur", "isCorrect": False, "explanation": "Malign karsinomdur."}
        ])
    ]
    slides.append(make_slide(97, "Morfolojik Özellikler: Glandüler Diferansiasyon vs Papiller Yapılar", "Endometrioid bezler, skuamöz diferansiasyon, seröz papiller yapılar ve yüksek dereceli sitoloji", "Histopatoloji", s97_narrative, s97_bullets, s97_elements))

    # Slide 98: FIGO Mimari Derecelendirme (Grade 1, 2, 3 ve Solid Alanlar)
    s98_narrative = (
        "Endometrioid karsinomların prognostik sınıflandırmasında Uluslararası Jinekoloji ve Obstetrik "
        "Federasyonu (FIGO) mimari derecelendirme sistemi kullanılır.\n\n"
        "- **Derecelendirme İlkesi:** Endometrioid karsinomlar diferansiasyon derecesi temel alınarak "
        "**FIGO'ya göre I'den III'e kadar derecelendirilirler**.\n"
        "- **Kriter: Solid Büyüme Oranı:** Bu derecelendirmede skuamöz olmayan **solid tümör adalarının "
        "toplam tümör alanına oranı** esas alınır:\n"
        "- **FIGO Grade 1:** Tümörün **%5'inden fazlası solid kitlelerden oluşmaz** (≤%5 solid alan, "
        "iyi diferansiye glandüler tümör).\n"
        "- **FIGO Grade 2:** Solid kitle oranı **Grade 1 ile Grade 3 arasıdır (%6-50 arası solid alan)**.\n"
        "- **FIGO Grade 3:** Tümörün **%50'sinden fazlası solid kitlelerden oluşur** (>%50 solid, "
        "kötü diferansiye tümör).\n"
        "- **Nükleer Yükseltme Kuralı:** Belirgin nükleer atipi varlığında tümör derecesi bir derece yukarı kaydırılabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] FIGO Mimari Derecelendirme: Grade 1 ≤%5 solid alan; Grade 2 %6-50 solid alan; Grade 3 >%50 solid kitle."
    )
    s98_bullets = [
        "Endometrioid karsinomlar diferansiasyon derecesine göre FIGO I - III olarak derecelendirilir.",
        "Grade 1: Tümörün %5'inden fazlası solid kitlelerden oluşmaz (≤%5 solid).",
        "Grade 2: Grade 1 ile 3 arası (%6-50 solid); Grade 3: Tümörün %50'sinden fazlası solid kitlelerden oluşur (>%50 solid)."
    ]
    s98_elements = [
        make_cloze("FIGO derecelendirmesine göre Grade 1 tümörün %5'inden fazlası solid olmazken Grade 3'te tümörün %50'sinden fazlası solid kitlelerden oluşur.", "%50'sinden fazlası", "Grade 3 karsinomun solid kitle eşiği"),
        make_table("FIGO Mimari Derecelendirme Tablosu", ["FIGO Derecesi", "Solid Kitle Oranı", "Diferansiasyon Düzeyi"], [
            {"cells": [{"text": "Grade 1", "isMasked": False}, {"text": "≤ %5 solid kitle", "isMasked": True, "hint": "yüzde beşi aşmayan solid alan"}, {"text": "İyi diferansiye (glandüler baskın)"}]},
            {"cells": [{"text": "Grade 2", "isMasked": False}, {"text": "%6 - 50 arası solid kitle", "isMasked": False}, {"text": "Orta diferansiye", "isMasked": True, "hint": "ara derece"}]},
            {"cells": [{"text": "Grade 3", "isMasked": False}, {"text": "> %50 solid kitle", "isMasked": True, "hint": "yarıdan fazlası solid"}, {"text": "Kötü diferansiye (agresif)"}]}
        ]),
        make_chain("FIGO Derecelendirme Süreci", [
            "1. Solid Alanların Hesabı: Skuamöz adacıklar dışlanarak katı tümör oranı taranır.",
            "2. ≤%5 Eşiği: Solid alan %5 altındaysa Grade 1 atanır.",
            "3. %6-50 Eşiği: Solid alan bu aralıkta ise Grade 2 atanır.",
            "4. >%50 Eşiği: Solid kitle %50'yi aşıyorsa Grade 3 (kötü diferansiye) olarak raporlanır."
        ]),
        make_recall("FIGO mimari derecelendirmesine göre endometrioid karsinomda Grade 1 ve Grade 3 solid alan oranları nasıldır?", "Grade 1: tümörün %5'inden fazlası solid kitlelerden oluşmaz (≤%5); Grade 3: tümörün %50'sinden fazlası solid kitlelerden oluşur (>%50)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: FIGO Derecelendirme", [
            {"text": "FIGO Grade 1'de tümörün %5'inden fazlası solid kitlelerden oluşmaz.", "isLie": False, "explanation": "Doğru. Ders notu tablosu verisidir."},
            {"text": "FIGO Grade 2, Grade 1 ile Grade 3 arasındadır (%6-50).", "isLie": False, "explanation": "Doğru. Ara gruptur."},
            {"text": "FIGO Grade 3 olabilmesi için tümörün en az %99.99'unun saf su olması gerekir.", "isLie": True, "explanation": "Tuzak! FIGO Grade 3 kriteri: tümörün %50'sinden fazlasının solid kitlelerden oluşmasıdır."},
            {"text": "Derecelendirme diferansiasyon derecesi temel alınarak yapılır.", "isLie": False, "explanation": "Doğru. Mimari prensiptir."}
        ]),
        make_quiz("FIGO mimari derecelendirme sistemine göre endometrioid karsinomda Grade 3 tanısı için gereken solid kitle oranı nedir?", [
            {"key": "A", "text": "Tümörün %50'sinden fazlasının solid kitlelerden oluşması", "isCorrect": True, "explanation": "Ders notu tablosunda harfiyen: 'Grade 3: tümörün %50'sinden fazlası solid kitlelerden oluşur' denmektedir."},
            {"key": "B", "text": "Tümörün tam olarak %0 solid olması", "isCorrect": False, "explanation": "Bu Grade 1'e girer."},
            {"key": "C", "text": "Solid alanın sadece %2 olması", "isCorrect": False, "explanation": "Grade 1'dir."},
            {"key": "D", "text": "Tümörde hiç hücre bulunmaması", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."}
        ])
    ]
    slides.append(make_slide(98, "FIGO Mimari Derecelendirme (Grade 1, 2, 3 ve Solid Alanlar)", "FIGO mimari derecelendirmesi, Grade 1 (≤%5), Grade 2 (%6-50) ve Grade 3 (>%50) solid alan eşikleri", "Patoloji", s98_narrative, s98_bullets, s98_elements))

    # Slide 99: En Önemli Prognostik Faktör Olarak Evre (FIGO Evreleme)
    s99_narrative = (
        "Endometrium karsinomlu bir hastanın klinik geleceğini ve sağkalımını belirleyen nihai parametre cerrahi ve patolojik evredir.\n\n"
        "- **En Önemli Faktör: EVRE:** Klinik ve moleküler tip ne olursa olsun, **her iki tipte de "
        "(Tip 1 ve Tip 2) yaşam süresini belirleyen en önemli faktör EVREDİR**.\n"
        "- **Evre Kapsamı:** Evreleme; tümörün miyometriyal invazyon derinliğini, servikal stromal "
        "tutulumu, adneksiyal yayılımı, peritoneal sitolojiyi ve bölgesel lenf nodu metastazını içerir.\n"
        "- **Seröz Tipin Prognoz Dezavantajı:** Seröz tümörler biyolojik olarak daha erken ve agresif "
        "şekilde **uterus dışı tutulumlar (evre III ve IV) ile saptandıkları için**, endometrioid "
        "karsinomlara göre prognozları belirgin şekilde daha kötüdür.\n"
        "- **Klinik Kür Şansı:** Erken evrede (Evre I) yakalanan endometrioid kanserlerde 5 yıllık "
        "sağkalım %90'ın üzerindedir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Her iki tip endometrium karsinomunda da yaşam süresini belirleyen EN ÖNEMLİ FAKTÖR EVREDİR; seröz tümörler uterus dışı tutulumla saptandığından prognozu daha kötüdür."
    )
    s99_bullets = [
        "Her iki tipte de yaşam süresini belirleyen en önemli faktör EVREDİR.",
        "Seröz tümörler sıklıkla uterus dışı tutulumla saptandıkları için prognozları daha kötüdür.",
        "Miyometrial invazyon derinliği ve lenf nodu tutulumu evrelemenin temel taşlarıdır."
    ]
    s99_elements = [
        make_cloze("Her iki tip endometrium karsinomunda da yaşam süresini belirleyen en önemli faktör evredir.", "en önemli faktör evredir", "Kanser sağkalımını belirleyen nihai parametre"),
        make_table("Prognostik Faktörlerin Hiyerarşisi", ["Prognostik Parametre", "Klinik Rolü", "Sağkalıma Etkisi"], [
            {"cells": [{"text": "Cerrahi / Patolojik Evre", "isMasked": False}, {"text": "En önemli prognostik faktör", "isMasked": True, "hint": "birinci sıradaki faktör"}, {"text": "Sağkalımı doğrudan belirler"}]},
            {"cells": [{"text": "Histolojik Tip (Tip 1 vs 2)", "isMasked": False}, {"text": "Biyolojik agresiflik göstergesi", "isMasked": False}, {"text": "Seröz tipte kötü prognoz", "isMasked": True, "hint": "seröz tümör dezavantajı"}]},
            {"cells": [{"text": "FIGO Derecesi (Grade)", "isMasked": False}, {"text": "Solid alan oranı (Grade 1-3)", "isMasked": False}, {"text": "Lokal invazyon riski"}]}
        ]),
        make_chain("Evreleme ve Prognoz Belirleme Zinciri", [
            "1. Histerektomi ve Lenf Disseksiyonu: Uterus ve bölgesel lenf nodları çıkarılır.",
            "2. Patolojik İnceleme: Miyometriyal invazyon ve lenf nodu tutulumu değerlendirilir.",
            "3. Evre Tespiti: Evre I (uterusa sınırlı) ile Evre IV (uzak metastaz) arası evre verilir.",
            "4. Prognoz: Hastanın sağkalımını en güçlü şekilde belirleyen evre raporlanır."
        ]),
        make_recall("Endometrium karsinomunda (hem Tip 1 hem Tip 2'de) yaşam süresini ve prognozu belirleyen en önemli faktör nedir?", "Hastalığın EVRESİDİR (cerrahi ve patolojik evre)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Evre ve Prognoz", [
            {"text": "Her iki tipte de yaşam süresini belirleyen en önemli faktör evredir.", "isLie": False, "explanation": "Doğru. Ders notunun altın spotudur."},
            {"text": "Seröz tümörler sıklıkla uterus dışı tutulumlar ile saptanırlar.", "isLie": False, "explanation": "Doğru. Agresif yayılımdır."},
            {"text": "Endometrium kanserinde evrelemenin sağkalıma hiçbir etkisi yoktur, tek önemli faktör hastanın boyudur.", "isLie": True, "explanation": "Tuzak! Yaşam süresini belirleyen EN ÖNEMLİ faktör evredir."},
            {"text": "Seröz tümörlerin prognozu endometrioid karsinomlara göre daha kötüdür.", "isLie": False, "explanation": "Doğru. Karşılaştırma kuralıdır."}
        ]),
        make_quiz("Endometrium karsinomunda (Tip 1 ve Tip 2) hastanın yaşam süresini ve prognozunu belirleyen EN ÖNEMLİ FAKTÖR aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Hastalığın evresi", "isCorrect": True, "explanation": "Ders notunun özet ve spot bölümlerinde harfiyen: 'her iki tipte de yaşam süresini belirleyen en önemli faktör evredir' vurgulanmıştır."},
            {"key": "B", "text": "Hastanın göz rengi", "isCorrect": False, "explanation": "Tıbbi parametre değildir."},
            {"key": "C", "text": "Yalnızca tümörün ağırlığı", "isCorrect": False, "explanation": "Ağırlık değil evre belirleyicidir."},
            {"key": "D", "text": "Hastanın sigortasının olup olmaması", "isCorrect": False, "explanation": "Biyolojik faktör değildir."}
        ])
    ]
    slides.append(make_slide(99, "En Önemli Prognostik Faktör Olarak Evre (FIGO Evreleme)", "En önemli prognostik belirteç olarak evre, seröz tümörlerin uterus dışı yayılımı ve prognoz", "Onkoloji", s99_narrative, s99_bullets, s99_elements))

    # Slide 100: [TEKRAR SAYFASI - CHECKPOINT 10] Endometrium Karsinomu ve FIGO Evreleme
    s100_narrative = (
        "Bu final tekrar sayfasında 10. Bölümde ve tüm ders boyunca işlenen endometrium karsinomu "
        "epidemiyolojisini, Tip 1 vs Tip 2 ayrımını, moleküler mutasyonları, FIGO derecelerini ve evre prognostik gücünü konsolide ediyoruz.\n\n"
        "- **Epidemiyoloji:** Kadın genital sisteminin en sık tümörü; genellikle 55-65 yaşta izlenir.\n"
        "- **Tip 1 Endometrioid (%80):** Östrojen fazlalığı ve hiperplazi zemininde; PTEN, mismatch repair "
        "(Lynch), Cowden ve K-ras mutasyonları; yavaş seyirli, prognozu iyi.\n"
        "- **Tip 2 Seröz (%15):** Atrofi zemininde, östrojensiz; TP53 mutasyonu (diffüz p53); SEIC öncülü; "
        "papiller mimari, yüksek dereceli ve çok agresif.\n"
        "- **FIGO Derecelendirme:** Grade 1 ≤%5 solid; Grade 2 %6-50 solid; Grade 3 >%50 solid kitle.\n"
        "- **En Önemli Prognostik Faktör:** Her iki tipte de yaşam süresini belirleyen EN ÖNEMLİ FAKTÖR EVREDİR; "
        "seröz karsinomlar uterus dışı tutulumla saptandığından prognozu daha kötüdür.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] En sık kadın genital tümörü; Tip 1 (%80, östrojen, PTEN, Lynch, atipik hiperplazi) vs Tip 2 (%15, atrofi, TP53, SEIC, agresif); FIGO Grade 1 (≤%5), 2 (%6-50), 3 (>%50); En önemli prognostik faktör EVREDİR."
    )
    s100_bullets = [
        "Kadın genital sisteminin en sık tümörü; 55-65 yaş zirvesi.",
        "Tip 1 (%80): östrojen fazlalığı, hiperplazi, PTEN, MMR (Lynch); Tip 2 (%15): atrofi, TP53, SEIC, agresif.",
        "FIGO: Grade 1 ≤%5 solid, Grade 2 %6-50 solid, Grade 3 >%50 solid; En önemli prognostik faktör EVREDİR."
    ]
    s100_elements = [
        make_cloze("Endometrium karsinomunda Tip 1 PTEN ve Lynch ilişkili iken her iki tipte de yaşam süresini belirleyen en önemli faktör evredir.", "en önemli faktör evredir", "Endometrium kanserinde nihai sağkalım belirteci"),
        make_table("10. Bölüm Büyük Karsinom Konsolidasyon Tablosu", ["Karsinom Tipi / Parametre", "Zemin ve Moleküler Genetik", "FIGO / Prognoz Kriteri"], [
            {"cells": [{"text": "Tip 1 Endometrioid (%80)", "isMasked": False}, {"text": "Östrojen, atipik hiperplazi, PTEN, MMR (Lynch)", "isMasked": True, "hint": "östrojen ve PTEN mutasyonu"}, {"text": "FIGO Grade 1-3 (solid alan oranına göre)"}]},
            {"cells": [{"text": "Tip 2 Seröz (%15)", "isMasked": False}, {"text": "Atrofi zemini, TP53 mutasyonu, SEIC öncülü", "isMasked": True, "hint": "p53 ve atrofik zemin"}, {"text": "Daima yüksek dereceli, agresif seyir"}]},
            {"cells": [{"text": "FIGO Grade Eşikleri", "isMasked": False}, {"text": "Grade 1: ≤%5 | Grade 2: %6-50 | Grade 3: >%50", "isMasked": False}, {"text": "Solid kitle oranına göre sınıflama", "isMasked": True, "hint": "solid alan kriteri"}]},
            {"cells": [{"text": "Sağkalım Belirteci", "isMasked": False}, {"text": "En önemli faktör EVREDİR", "isMasked": False}, {"text": "Uterus dışı yayılım prognozu bozar"}]}
        ]),
        make_chain("Tüm Ders Final Sentez Zinciri", [
            "1. Siklus ve Hormon: Östrojen 11-12. günde, LH 36 saat sonra pik yapar; progesteron luteal faz ortasındadır.",
            "2. Fazlar ve Histoloji: Proliferatif faz 2-3 mm iken sekretuar faz subnükleer vakuollerle 5 mm'ye ulaşır.",
            "3. Risk ve Metaplazi: Tek başına östrojen %15-30 hiperplazi yapar; en sık skuamöz metaplazi görülür.",
            "4. Polip ve Endometrit: Polip bazalis hiperplazisidir; kronik endometrit için plazma hücresi şarttır.",
            "5. Adeno vs Endometriozis: Adenomyozis kanamaz; endometriozis siklik kanar ve çikolata kisti yapar.",
            "6. Karsinom Zirvesi: Tip 1 (%80, PTEN) vs Tip 2 (%15, TP53); prognozu belirleyen en önemli faktör EVREDİR."
        ]),
        make_recall("Endometrium karsinomunun iki tipinin temel farkları nelerdir ve hastanın sağkalımını belirleyen en önemli faktör nedir?", "Tip 1: %80 oran, östrojen fazlalığı, hiperplazi zemini, PTEN/MMR mutasyonları; Tip 2: %15 oran, atrofi zemini, TP53 mutasyonu, SEIC öncülü ve agresif seyir. Yaşam süresini belirleyen en önemli faktör EVREDİR."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 10. Bölüm Konsolidasyonu", [
            {"text": "Kadın genital sisteminin en sık izlenen tümörü endometrium karsinomudur.", "isLie": False, "explanation": "Doğru. Batı ülkelerinde 1. sıradadır."},
            {"text": "Tip 1 endometrioid karsinom olguların %80'ini oluşturur ve PTEN mutasyonu içerir.", "isLie": False, "explanation": "Doğru. Tip 1 profilidir."},
            {"text": "Tip 2 seröz karsinomlar sadece östrojen fazlalığında gelişir ve TP53 mutasyonu asla görülmez.", "isLie": True, "explanation": "Tuzak! Seröz karsinomlar östrojenle ilişkisiz olup atrofi zemininde gelişir ve tama yakınında TP53 mutasyonu taşır."},
            {"text": "Her iki tipte de yaşam süresini belirleyen en önemli faktör evredir.", "isLie": False, "explanation": "Doğru. Altın prognostik kuraldır."}
        ]),
        make_quiz("Endometriyal karsinomlar ve FIGO derecelendirmesi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Tip 1 %80 oranında PTEN/Lynch zemininde, Tip 2 %15 oranında TP53 zeminindedir; en önemli prognostik faktör evredir", "isCorrect": True, "explanation": "Ders notundaki tüm karsinom ve prognoz bilgilerini eksiksiz özetleyen doğru seçenektir."},
            {"key": "B", "text": "Endometrium karsinomu kadınlarda en nadir görülen kanserdir ve her zaman 20 yaşında başlar", "isCorrect": False, "explanation": "En sık görülen tümördür ve 55-65 yaş zirvesidir."},
            {"key": "C", "text": "FIGO Grade 1 tümörlerin %90'ından fazlası solid kitlelerden oluşur", "isCorrect": False, "explanation": "Grade 1 ≤%5 solid alandır."},
            {"key": "D", "text": "Evrelemenin sağkalıma hiçbir etkisi yoktur", "isCorrect": False, "explanation": "En önemli faktör evredir."}
        ])
    ]
    slides.append(make_slide(100, "[TEKRAR SAYFASI - CHECKPOINT 10] Endometrium Karsinomu ve FIGO Evreleme", "10. Bölümün konsolidasyonu: Tip 1 (%80, östrojen, PTEN) vs Tip 2 (%15, TP53, SEIC), FIGO dereceleri ve evre prognostik gücü", "Bölüm Tekrarı", s100_narrative, s100_bullets, s100_elements))

    return slides
