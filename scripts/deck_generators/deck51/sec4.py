# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec4():
    slides = []

    # Slide 31: Üropatojen Mikroorganizmalar: E. coli ve Enterobacteriaceae Hakimiyeti
    s31_narrative = (
        "Üriner sistem enfeksiyonlarının mikrobiyolojik etiyolojisi incelendiğinde, toplum kökenli "
        "olgularda monomikrobiyal bir hakimiyet göze çarpar.\n\n"
        "- **Monomikrobiyal Karakter:** ÜSE olgularının **%95 kadarında tek bir bakteri türü** izole edilir; "
        "birden fazla bakterinin aynı anda saptanması genellikle kontaminasyonu düşündürür.\n"
        "- **Escherichia coli Hakimiyeti:** Hem komplike olmayan sistit hem de pyelonefrit tablolarında "
        "en sık izole edilen üropatojen **%70-90 ezici oranıyla E. coli'dir**.\n"
        "- **Diğer Enterik Basiller:** Geriye kalan olguların önemli bir kısmını Klebsiella pneumoniae, "
        "Proteus mirabilis ve Enterobacter türleri gibi diğer Enterobacteriaceae üyeleri oluşturur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] ÜSE'lerin %95'inde tek bakteri bulunur ve en sık izole edilen üropatojen %70-90 oranıyla Escherichia coli'dir."
    )
    s31_bullets = [
        "ÜSE olgularının %95 kadarında tek bir bakteri türü bulunur.",
        "En sık izole edilen üropatojen %70-90 sıklıkla E. coli'dir.",
        "Klebsiella ve Proteus diğer sık görülen Gram negatif üropatojenlerdir."
    ]
    s31_elements = [
        make_cloze("ÜSE olgularının %95'inde tek bakteri izole edilirken en sık etken %70-90 sıklıkla E. coli'dir.", "%70-90", "E. coli'nin ezici izolasyon sıklığı"),
        make_table("Üropatojen İzolasyon Dağılımı", ["Mikroorganizma", "Görülme Oranı", "Klinik Özellik"], [
            {"cells": [{"text": "Escherichia coli", "isMasked": False}, {"text": "%70-90 (en sık)", "isMasked": True, "hint": "yüzde yetmiş ile doksan arası"}, {"text": "Toplum kökenli sistit ve pyelonefritin bir numaralı etkeni"}]},
            {"cells": [{"text": "Klebsiella ve Proteus", "isMasked": False}, {"text": "%5-15", "isMasked": False}, {"text": "Komplike, taş ve hastane kaynaklı olgular", "isMasked": True, "hint": "yapısal bozukluk ve yatış ilişkili"}]},
            {"cells": [{"text": "Tek Bakteri İzolatı", "isMasked": False}, {"text": "%95 oranında tek tür", "isMasked": True, "hint": "vakaların yüzde doksan beşi"}, {"text": "Polimikrobiyal üreme kontaminasyon şüphesidir"}]}
        ]),
        make_chain("E. coli İzolasyon Zinciri", [
            "1. Bağırsak Rezervuarı: Normal fekal florada bol miktarda E. coli bulunur.",
            "2. Periüretral Kolonizasyon: Fekal bulaş ile üretra çevresine yerleşir.",
            "3. Monomikrobiyal İnvazyon: Tek bir virülan klon mesaneye girip çoğalır.",
            "4. Kültürde Saf Koloni: Kültür plağında %70-90 oranında saf E. coli ürer."
        ]),
        make_recall("Üriner sistem enfeksiyonlarında en sık izole edilen üropatojen bakteri ve görülme oranı nedir?", "Escherichia coli'dir; olguların yaklaşık %70-90'ından sorumludur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Üropatojen Etiyolojisi", [
            {"text": "ÜSE'lerin yaklaşık %95'inde tek bakteri türü bulunur.", "isLie": False, "explanation": "Doğru. Monomikrobiyaldir."},
            {"text": "En sık izole edilen üropatojen %70-90 oranıyla E. coli'dir.", "isLie": False, "explanation": "Doğru. Açık ara birinci etkendir."},
            {"text": "ÜSE olgularının %100'ünde aynı anda en az 10 farklı bakteri birlikte ürer.", "isLie": True, "explanation": "Tuzak! ÜSE tipik olarak monomikrobiyaldir (%95 tek bakteri); çoklu bakteri üremesi genellikle kontaminasyondur."},
            {"text": "Klebsiella ve Proteus diğer önemli Gram negatif üropatojenlerdir.", "isLie": False, "explanation": "Doğru. Enterobacteriaceae ailesindendir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarında en sık izole edilen üropatojen bakteri aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Escherichia coli (%70-90)", "isCorrect": True, "explanation": "Ders notunda en sık izole edilen üropatojenin %70-90 oranıyla E. coli olduğu belirtilmiştir."},
            {"key": "B", "text": "Pseudomonas aeruginosa (%90)", "isCorrect": False, "explanation": "Nozokomiyal ve dirençli vakalarda nadirdir."},
            {"key": "C", "text": "Streptococcus pneumoniae (%80)", "isCorrect": False, "explanation": "Pnömokok pnömoni ve menenjit etkenidir."},
            {"key": "D", "text": "Neisseria meningitidis", "isCorrect": False, "explanation": "Menenjit etkenidir."}
        ])
    ]
    slides.append(make_slide(31, "Üropatojen Mikroorganizmalar: E. coli ve Enterobacteriaceae Hakimiyeti", "Monomikrobiyal karakter (%95), E. coli (%70-90), Klebsiella ve Proteus", "Etiyoloji", s31_narrative, s31_bullets, s31_elements))

    # Slide 32: Proteus Türleri, Üreaz Enzimi ve Magnezyum Amonyum Fosfat Taşları
    s32_narrative = (
        "Proteus türleri (özellikle Proteus mirabilis), ürettikleri özgül enzimlerle idrarın biyokimyasal "
        "ortamını kökten değiştiren en tehlikeli taş yapıcı bakterilerdir.\n\n"
        "- **Üreaz Enzimi:** Proteus bakterileri yüksek miktarda **üreaz enzimi** salgılarlar; üreaz "
        "idrardaki üreyi parçalayarak amonyak ve karbondioksite dönüştürür.\n"
        "- **Alkali İdrar:** Açığa çıkan amonyak idrar pH'sını 8-9 gibi aşırı alkali seviyelere fırlatır; "
        "asidik ortamda çözünen mineraller bu alkali ortamda süratle çökmeye başlar.\n"
        "- **Struvit Taşları (Magnezyum Amonyum Fosfat):** Magnezyum, amonyum ve fosfat iyonları "
        "birleşerek **struvit (enfeksiyon) taşlarını** ve böbrek toplayıcı sistemini dolduran devasa "
        "**staghorn (geyik boynuzu) taşlarını** oluşturur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Proteus türleri üreaz enzimi salgılayarak idrarı alkalileştirir ve magnezyum amonyum fosfat (struvit / staghorn) taşlarına yol açar."
    )
    s32_bullets = [
        "Proteus mirabilis yüksek düzeyde üreaz enzimi salgılar.",
        "Ürenin amonyağa parçalanması idrar pH'sını belirgin şekilde alkalileştirir.",
        "Alkali idrarda magnezyum amonyum fosfat (struvit / staghorn) taşları çöker."
    ]
    s32_elements = [
        make_cloze("Proteus türlerinin salgıladığı üreaz enzimi idrarı alkalileştirerek magnezyum amonyum fosfat (struvit) taşlarını oluşturur.", "üreaz enzimi", "Üreyi amonyağa yıkan bakteriyel enzim"),
        make_table("Proteus ve Taş Oluşum Patofizyolojisi", ["Aşama", "Kimyasal Reaksiyon", "Klinik Yansıması"], [
            {"cells": [{"text": "Enzimatik Hidroliz", "isMasked": False}, {"text": "Üreaz ile ürenin parçalanması", "isMasked": True, "hint": "üre molekülünün hidrolizi"}, {"text": "Yoğun serbest amonyak açığa çıkması"}]},
            {"cells": [{"text": "pH Fırlaması", "isMasked": False}, {"text": "İdrarın aşırı alkalileşmesi (pH >8)", "isMasked": False}, {"text": "Kristalizasyon eşiğinin aşılması", "isMasked": True, "hint": "minerallerin çözünemeyip çökmesi"}]},
            {"cells": [{"text": "Taş Oluşumu", "isMasked": False}, {"text": "Magnezyum amonyum fosfat çökmesi", "isMasked": False}, {"text": "Struvit / Staghorn (geyik boynuzu) taşları", "isMasked": True, "hint": "bütün böbreği dolduran enfeksiyon taşı"}]}
        ]),
        make_chain("Proteus Kaynaklı Struvit Taşı Zinciri", [
            "1. Kolonizasyon: Proteus mirabilis üriner sisteme yerleşir.",
            "2. Üreaz Salınımı: Lümendeki üreyi amonyak ve CO2'ye hidrolize eder.",
            "3. Alkalinizasyon: Amonyak hidroksit oluşturarak idrar pH'sını alkaliye çevirir.",
            "4. Presipitasyon: Magnezyum, amonyum ve fosfat birleşerek struvit taşlarını örer."
        ]),
        make_recall("Proteus türlerinin idrarı alkalileştirerek oluşturduğu enfeksiyon taşlarının kimyasal adı nedir?", "Magnezyum amonyum fosfat (struvit) taşlarıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Proteus ve Üreaz", [
            {"text": "Proteus türleri üreaz enzimi üreterek üreyi parçalar.", "isLie": False, "explanation": "Doğru. Temel biyokimyasal özelliğidir."},
            {"text": "Açığa çıkan amonyak idrar pH'sını yükselterek alkali yapar.", "isLie": False, "explanation": "Doğru. pH >8 olur."},
            {"text": "Proteus enfeksiyonları idrarı saf asite çevirir ve kalsiyum okzalat taşlarını tamamen eritir.", "isLie": True, "explanation": "Tuzak! Proteus idrarı asit yapmaz, tam tersine ALKALİ yapar ve magnezyum amonyum fosfat taşlarını oluşturur."},
            {"text": "Magnezyum amonyum fosfat taşlarına struvit veya geyik boynuzu taşı denir.", "isLie": False, "explanation": "Doğru. Staghorn taşlarıdır."}
        ]),
        make_quiz("Üreaz enzimi salgılayarak idrar pH'sını alkalileştiren ve magnezyum amonyum fosfat (struvit) taşlarına yol açan mikroorganizma hangisidir?", [
            {"key": "A", "text": "Proteus türleri (Proteus mirabilis)", "isCorrect": True, "explanation": "Proteus üreaz pozitif klasik etken olup alkali idrarda struvit taşları oluşturur."},
            {"key": "B", "text": "Escherichia coli", "isCorrect": False, "explanation": "Üreaz üretmez, idrarı alkalileştirmez."},
            {"key": "C", "text": "Streptococcus pyogenes", "isCorrect": False, "explanation": "Üriner taş etkeni değildir."},
            {"key": "D", "text": "Treponema pallidum", "isCorrect": False, "explanation": "Sifiliz etkenidir, idrar taşı yapmaz."}
        ])
    ]
    slides.append(make_slide(32, "Proteus Türleri, Üreaz Enzimi ve Magnezyum Amonyum Fosfat Taşları", "Proteus, üreaz aktivitesi, idrar alkalinizasyonu ve struvit taşları", "Etiyoloji", s32_narrative, s32_bullets, s32_elements))

    # Slide 33: Staphylococcus saprophyticus: Genç Kadınlarda Akut Sistit
    s33_narrative = (
        "Staphylococcus saprophyticus, genç ve cinsel aktif kadın popülasyonunda E. coli'den sonra "
        "en sık izole edilen ikinci akut sistit etkeni olan Gram pozitif bir koktur.\n\n"
        "- **Koagülaz Negatif Stafilokok (KNS):** Koagülaz negatiftir ancak diğer KNS'lerden (ör. S. epidermidis) "
        "farklı olarak **novobiosin antibiyotiğine dirençlidir** (mikrobiyolojik tanı kriteri).\n"
        "- **Hedef Popülasyon:** Menopoz öncesi, özellikle 18-30 yaş arası genç ve cinsel yönden aktif "
        "kadınlarda yaz aylarında ve cinsel aktivite sonrasında pik yapar.\n"
        "- **Klinik Tablo:** Ağrılı dizüri, sıkışma, pollaküri ve sıklıkla mikroskopik hematüri ile "
        "seyreden tipik akut sistit kliniği oluşturur; böbreğe asendan tırmanışı nadirdir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Genç, cinsel aktif kadınlarda E. coli'den sonra ikinci en sık akut sistit etkeni Staphylococcus saprophyticus'tur (novobiosine dirençlidir)."
    )
    s33_bullets = [
        "Genç ve cinsel aktif kadınlarda E. coli'den sonra 2. en sık sistit etkenidir.",
        "Koagülaz negatiftir ve novobiosine dirençli olmasıyla ayırt edilir.",
        "Dizüri, sıkışma ve belirgin hematüri ile seyreden akut sistit yapar."
    ]
    s33_elements = [
        make_cloze("Genç cinsel aktif kadınlarda E. coli'den sonra ikinci en sık sistit etkeni Staphylococcus saprophyticus adlı Gram pozitif koktur.", "Staphylococcus saprophyticus", "Novobiosine dirençli koagülaz negatif stafilokok"),
        make_table("Staphylococcus saprophyticus Profili", ["Özellik", "Mikrobiyolojik Değer", "Klinik Yansıması"], [
            {"cells": [{"text": "Gram ve Morfoloji", "isMasked": False}, {"text": "Gram pozitif kok (kümeler)", "isMasked": True, "hint": "mor üzüm salkımı şeklinde kok"}, {"text": "İdrar mikroskopisinde Gram (+) koklar"}]},
            {"cells": [{"text": "Biyokimyasal Ayırım", "isMasked": False}, {"text": "Koagülaz (-), Novobiosine dirençli", "isMasked": False}, {"text": "S. epidermidis'ten laboratuvarda ayrılması", "isMasked": True, "hint": "novobiosin diski etrafında üreme"}]},
            {"cells": [{"text": "Hedef Popülasyon", "isMasked": False}, {"text": "Genç, cinsel aktif kadınlar", "isMasked": False}, {"text": "Akut balayı sistiti kliniği", "isMasked": False}]}
        ]),
        make_chain("S. saprophyticus Sistit Patogenezi", [
            "1. Kolonizasyon: Genitoüriner mukozaya ve perianal deriye yerleşir.",
            "2. Koital Bulaş: Cinsel aktivite ile kısa kadın üretrasından mesaneye girer.",
            "3. Üroepitelyal Adezyon: Özgül adezyon proteinleri ile mesane hücrelerine tutunur.",
            "4. Akut Sistit: Şiddetli dizüri, pollaküri ve piyüri tablosu geliştirir."
        ]),
        make_recall("Genç ve cinsel aktif kadınlarda E. coli'den sonra en sık görülen ikinci akut sistit etkeni olan Gram pozitif bakteri nedir?", "Staphylococcus saprophyticus'tur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: S. saprophyticus", [
            {"text": "S. saprophyticus genç cinsel aktif kadınlarda akut sistit etkenidir.", "isLie": False, "explanation": "Doğru. Bu grupta çok sıktır."},
            {"text": "Koagülaz negatif stafilokoklar arasında novobiosine dirençli olmasıyla tanınır.", "isLie": False, "explanation": "Doğru. Mikrobiyolojik kilit testtir."},
            {"text": "S. saprophyticus sadece 90 yaşındaki yatalak erkeklerin prostatında yaşar.", "isLie": True, "explanation": "Tuzak! Tipik olarak genç, reprodüktif çağdaki cinsel aktif kadınlarda görülür."},
            {"text": "Gram pozitif küme oluşturan kok morfolojisindedir.", "isLie": False, "explanation": "Doğru. Stafilokok morfolojisidir."}
        ]),
        make_quiz("Genç ve cinsel aktif bir kadında ani başlayan dizüri ve pollaküri tablosunda E. coli'den sonra akla gelmesi gereken en sık ikinci etken hangisidir?", [
            {"key": "A", "text": "Staphylococcus saprophyticus", "isCorrect": True, "explanation": "Ders notunda genç cinsel aktif kadınlarda S. saprophyticus'un önemli bir sistit etkeni olduğu belirtilmiştir."},
            {"key": "B", "text": "Clostridium difficile", "isCorrect": False, "explanation": "Psödomembranöz kolit etkenidir."},
            {"key": "C", "text": "Bacillus anthracis", "isCorrect": False, "explanation": "Şarbon etkenidir."},
            {"key": "D", "text": "Corynebacterium diphtheriae", "isCorrect": False, "explanation": "Kuşpalazı/difteri etkenidir."}
        ])
    ]
    slides.append(make_slide(33, "Staphylococcus saprophyticus: Genç Kadınlarda Akut Sistit", "S. saprophyticus, genç kadınlar, novobiosin direnci ve akut sistit", "Etiyoloji", s33_narrative, s33_bullets, s33_elements))

    # Slide 34: Adenovirus Tip 11 ve Çocukluk Çağı Hemorajik Sistiti
    s34_narrative = (
        "Üriner sistem enfeksiyonları hemen her zaman bakteriyel kökenli olmakla beraber, pediatrik "
        "popülasyonda dramatik kanama ile seyreden viral bir istisna mevcuttur.\n\n"
        "- **Hemorajik Sistit Tablosu:** Ani başlayan masif gros hematüri, disüri ve suprapubik "
        "kramp tarzı ağrılarla karakterize, idrarın adeta saf kan gibi gelmesi durumudur.\n"
        "- **Spesifik Viral Etken:** Çocuklarda görülen akut hemorajik sistitin klasik ve sınav "
        "klasiği etkeni **Adenovirus tip 11**'dir (bazen tip 21 de eşlik edebilir).\n"
        "- **Klinik Ayırıcı Özellik:** Bakteriyel kültürlerde hiçbir üreme olmaz; idrar sedimentinde bol "
        "eritrosit görülür; tablo genellikle 1-2 hafta içinde kendiliğinden gerileyen selim bir seyir gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Çocuklarda ani başlayan akut hemorajik sistitin en karakteristik viral etkeni Adenovirus tip 11'dir."
    )
    s34_bullets = [
        "Çocuklarda akut hemorajik sistit kliniği masif gros hematüri ile seyreder.",
        "Karakteristik etken Adenovirus tip 11'dir.",
        "İdrar kültürü steril kalır; genellikle kendini sınırlayan selim seyirlidir."
    ]
    s34_elements = [
        make_cloze("Çocuklarda ani başlayan hemorajik sistitin klasik viral etkeni Adenovirus tip 11 serotipidir.", "Adenovirus tip 11", "Çocuklarda kanamalı sistit yapan DNA virüsü"),
        make_table("Viral vs Bakteriyel Sistit Ayrımı", ["Özellik", "Adenovirus Tip 11", "Escherichia coli"], [
            {"cells": [{"text": "Etken Tipi", "isMasked": False}, {"text": "Çift sarmallı DNA virüsü", "isMasked": True, "hint": "viral genom yapısı"}, {"text": "Gram negatif basil"}]},
            {"cells": [{"text": "Klinik Belirti", "isMasked": False}, {"text": "Masif hemorajik sistit (kanlı idrar)", "isMasked": False}, {"text": "Dizüri, pollaküri, bulanık idrar", "isMasked": True, "hint": "klasik alt üriner semptomlar"}]},
            {"cells": [{"text": "Standart Kültür", "isMasked": False}, {"text": "Steril (bakteri üremez)", "isMasked": False}, {"text": "≥10⁵ KOB/ml E. coli ürer", "isMasked": False}]}
        ]),
        make_chain("Adenoviral Hemorajik Sistit Seyri", [
            "1. Viral İnokülasyon: Adenovirus tip 11 mesane ürotelyumuna invaze olur.",
            "2. Mukozal Nekroz: Viral replikasyon ile yüzeyel kılcal damarlar erode olur.",
            "3. Masif Hematüri: Çocuk ani başlayan pıhtılı/kanlı idrar yapar.",
            "4. Spontan Rezolüsyon: Bağışıklık yanıtı ile 7-10 günde kendiliğinden düzelir."
        ]),
        make_recall("Çocuklarda akut hemorajik sistite yol açan karakteristik viral etken nedir?", "Adenovirus tip 11'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hemorajik Sistit", [
            {"text": "Çocuklarda Adenovirus tip 11 hemorajik sistit yapar.", "isLie": False, "explanation": "Doğru. Kilit sınav spotudur."},
            {"text": "Hemorajik sistitte idrarda belirgin kanama ve eritrositler görülür.", "isLie": False, "explanation": "Doğru. Masif hematüri vardır."},
            {"text": "Adenovirus tip 11 sadece kemik iliği naklinde görülen ölümcül bir bakteridir.", "isLie": True, "explanation": "Tuzak! Adenovirus bir bakteri değil virüstür ve çocuklarda akut hemorajik sistit yapabilir."},
            {"text": "Viral sistitte standart bakteriyel besiyerlerinde bakteri üremez.", "isLie": False, "explanation": "Doğru. Kültür negatiftir."}
        ]),
        make_quiz("Çocuklarda akut hemorajik sistit tablosuna yol açan karakteristik viral etken aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Adenovirus tip 11", "isCorrect": True, "explanation": "Ders notunda çocuklarda hemorajik sistit etkeni olarak Adenovirus tip 11 açıkça belirtilmiştir."},
            {"key": "B", "text": "Hepatit B virüsü", "isCorrect": False, "explanation": "Karaciğer tutulumu yapar."},
            {"key": "C", "text": "Kuduz virüsü (Rabies)", "isCorrect": False, "explanation": "Santral sinir sistemi ensefaliti yapar."},
            {"key": "D", "text": "İnfluenza A virüsü", "isCorrect": False, "explanation": "Solunum yolu grip etkenidir."}
        ])
    ]
    slides.append(make_slide(34, "Adenovirus Tip 11 ve Çocukluk Çağı Hemorajik Sistiti", "Adenovirus tip 11, masif hematüri, pediatrik hemorajik sistit ve steril kültür", "Etiyoloji", s34_narrative, s34_bullets, s34_elements))

    # Slide 35: Özel Popülasyonlarda Fırsatçı Etkenler: Corynebacterium, S. epidermidis, Candida
    s35_narrative = (
        "Hastanede yatan, immünsupresif tedavi alan veya kalıcı üriner kateter taşıyan hastalarda "
        "klasik E. coli tablosunun yerini fırsatçı ve atipik mikroorganizmalar alır.\n\n"
        "- **Corynebacterium urealyticum (Grup D2):** Hastanede yatan, immünsupresif ve ürolojik girişim "
        "yapılmış hastalarda inkruste sistit ve alkali taş oluşumu ile seyreden dirençli bir basildir.\n"
        "- **Staphylococcus epidermidis:** Normalde üretra ve perine florasında kolonizedir; immünsupresif "
        "hastalarda ve ürolojik enstrümantasyon uygulanan yatan hastalarda yabancı cisme yapışarak enfeksiyon yapar.\n"
        "- **Candida Türleri:** Üriner kateteri olan ve uzun süreli geniş spektrumlu **antibiyotik tedavisi "
        "alan hastalarda** fungal sistit veya kandidüri tablosu oluşturur.\n\n"
        "> [!NOTE]\n"
        "> Kateterli ve antibiyotik kullanan hastada idrarda maya hücreleri (Candida); immünsuprese yatan hastada C. urealyticum ve S. epidermidis düşünülmelidir."
    )
    s35_bullets = [
        "C. urealyticum (Grup D2) yatan immünsupresif hastalarda inkruste sistit yapar.",
        "S. epidermidis perine florasından girişim ve enstrümantasyonla mesaneye girer.",
        "Candida türleri kateteri olan ve geniş spektrumlu antibiyotik alanlarda ürer."
    ]
    s35_elements = [
        make_cloze("Hastanede yatan ve antibiyotik tedavisi alan üriner kateterli hastalarda fungal enfeksiyon etkeni Candida türleridir.", "Candida", "Kateter ilişkili maya mantarı"),
        make_table("Fırsatçı ve Nozokomiyal Üropatojenler", ["Mikroorganizma", "Risk Grubu", "Patojenik Özellik"], [
            {"cells": [{"text": "Corynebacterium urealyticum", "isMasked": False}, {"text": "Hastanede yatan immünsupresifler", "isMasked": True, "hint": "Grup D2 korinebakteri"}, {"text": "Üreaz üretimi ve inkruste kalsifiye sistit"}]},
            {"cells": [{"text": "Staphylococcus epidermidis", "isMasked": False}, {"text": "Enstrümantasyon yapılan yatan hastalar", "isMasked": False}, {"text": "Kateter ve yabancı cisim biyofilm invazyonu", "isMasked": True, "hint": "plastik yüzeylere yapışma"}]},
            {"cells": [{"text": "Candida türleri", "isMasked": False}, {"text": "Üriner kateter + antibiyotik kullanımı", "isMasked": False}, {"text": "Bakteriyel floranın silinmesiyle fungal çoğalma", "isMasked": False}]}
        ]),
        make_chain("Fırsatçı Üropatojen Kolonizasyonu", [
            "1. Antibiyotik Baskısı: Geniş spektrumlu antibiyotik normal bakteriyel florayı yok eder.",
            "2. Kateter Varlığı: Kalıcı foley sonda fungal biyofilm için iskele oluşturur.",
            "3. Candida Çoğalması: Mantarlar lümende hızla üreyerek kandidüri yapar.",
            "4. Cerrahi İnvazyon: İmmünsupresif hastada fungal top (fungus ball) obstrüksiyonu gelişebilir."
        ]),
        make_recall("Üriner kateteri olan ve geniş spektrumlu antibiyotik tedavisi alan hastalarda idrarda en sık üreyen fırsatçı mantar grubu nedir?", "Candida türleridir (Candida albicans ve non-albicans türleri)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fırsatçı Etkenler", [
            {"text": "C. urealyticum hastanede yatan immünsupresif hastalarda etken olabilir.", "isLie": False, "explanation": "Doğru. Grup D2 nozokomiyal etkendir."},
            {"text": "Candida türleri kateterli ve antibiyotik kullanan hastalarda sık görülür.", "isLie": False, "explanation": "Doğru. Fırsatçı mantardır."},
            {"text": "S. epidermidis sadece uzay boşluğunda yaşayan ve insan vücuduna hiç girmeyen bir mikroptur.", "isLie": True, "explanation": "Tuzak! S. epidermidis perine ve üretrada normal kolonize olan ve girişimlerle enfeksiyon yapan bir bakteridir."},
            {"text": "Ürolojik enstrümantasyon yabancı cisim enfeksiyonlarını tetikleyebilir.", "isLie": False, "explanation": "Doğru. İyatrojenik risktir."}
        ]),
        make_quiz("Üriner kateteri bulunan ve uzun süredir geniş spektrumlu antibiyotik tedavisi almakta olan bir hastada idrar kültüründe üremesi en muhtemel fırsatçı mikroorganizma hangisidir?", [
            {"key": "A", "text": "Candida türleri", "isCorrect": True, "explanation": "Ders notunda Candida türlerinin üriner kateteri olan ve antibiyotik tedavisi alan hastalarda görüldüğü açıkça ifade edilmiştir."},
            {"key": "B", "text": "Bordetella pertussis", "isCorrect": False, "explanation": "Boğmaca etkenidir."},
            {"key": "C", "text": "Vibrio cholerae", "isCorrect": False, "explanation": "Kolera bağırsak etkenidir."},
            {"key": "D", "text": "Treponema pertenue", "isCorrect": False, "explanation": "Yaws etkenidir."}
        ])
    ]
    slides.append(make_slide(35, "Özel Popülasyonlarda Fırsatçı Etkenler: Corynebacterium, S. epidermidis, Candida", "C. urealyticum, S. epidermidis, kateter ilişkili Candida ve fırsatçı patogenez", "Etiyoloji", s35_narrative, s35_bullets, s35_elements))

    # Slide 36: Klinik Sınıflama: Akut Komplike Olmayan Sistit
    s36_narrative = (
        "Akut komplike olmayan sistit, altta yatan herhangi bir anatomik, fonksiyonel veya metabolik "
        "bozukluğu bulunmayan kadınlarda gelişen yüzeyel mesane mukozası enfeksiyonudur.\n\n"
        "- **Tipik Semptomlar:** Sık idrara çıkma (pollaküri), idrar yaparken yanma/ağrı (dizüri), "
        "acil sıkışma hissi (urgency), bulanık ve/veya kanlı idrar (hematüri) ve suprapubik dolgunluktur.\n"
        "- **Fizik Muayene:** Yalnızca suprapubik bölgede palpasyonla hassasiyet saptanır.\n"
        "- **Sistemik Ateşin Yokluğu:** En kritik tanısal ve ayırt edici kuraldır: **Akut sistitte KESİNLİKLE "
        "yüksek ateş ve kostavertebral açı hassasiyeti (KVAH) bulunmaz**; ateş varlığı sürecin böbreğe (pyelonefrite) sıçradığını kanıtlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Komplike olmayan sistitte ATEŞ SAPTANMAZ; fizik muayenede sadece suprapubik hassasiyet vardır; yaşlılarda asemptomatik seyredebilir."
    )
    s36_bullets = [
        "Sık idrara çıkma, ağrılı idrar yapma (dizüri), bulanık/kanlı idrar görülür.",
        "Fizik muayenede suprapubik hassasiyet vardır, sistemik ateş saptanmaz.",
        "Ateş veya böğür ağrısının eklenmesi tanıyı sistitten pyelonefrite çevirir."
    ]
    s36_elements = [
        make_cloze("Komplike olmayan sistit tablosunda fizik muayenede suprapubik hassasiyet varken kesinlikle ateş saptanmaz.", "ateş saptanmaz", "Sistemik vücut sıcaklığı artışının olmaması"),
        make_table("Akut Komplike Olmayan Sistit Bulguları", ["Bulgu Kategorisi", "Klinik Özellik", "Tanısal Önemi"], [
            {"cells": [{"text": "İşeme Semptomları", "isMasked": False}, {"text": "Dizüri, pollaküri, urgency", "isMasked": True, "hint": "yanma, sık çıkma, sıkışma"}, {"text": "Mesane mukozal irritasyonu"}]},
            {"cells": [{"text": "İdrar Görünümü", "isMasked": False}, {"text": "Bulanık idrar, bazen hematüri", "isMasked": False}, {"text": "Piyüri ve eritrosit varlığı", "isMasked": True, "hint": "iltihap ve kan dökülmesi"}]},
            {"cells": [{"text": "Sistemik Bulgular", "isMasked": False}, {"text": "Ateş YOK, KVAH YOK", "isMasked": True, "hint": "sistemik belirti bulunmaması"}, {"text": "Enfeksiyonun mesaneyle sınırlı olduğunun kanıtı"}]}
        ]),
        make_chain("Sistit Enflamasyon ve Ağrı Zinciri", [
            "1. İnvazyon: Bakteri mesane transizyonel epitelini infiltre eder.",
            "2. Sinir Uyarımı: Enflamasyon mesane submukozasındaki ağrı liflerini (C lifleri) uyarır.",
            "3. Detrüsör Spazmı: Mesane az idrarla dahi şiddetle kasılır (pollaküri ve urgency).",
            "4. Lokalizasyon: Süreç mesanede sınırlı kalır ve sistemik ateş yapmaz."
        ]),
        make_recall("Akut komplike olmayan sistit tablosunda fizik muayenede saptanması BEKLENMEYEN kardinal sistemik bulgu nedir?", "Yüksek ateştir (sistitte sistemik ateş bulunmaz; saptanırsa pyelonefrit veya komplike durum düşünülür)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komplike Olmayan Sistit", [
            {"text": "Komplike olmayan sistitte sık idrara çıkma ve dizüri görülür.", "isLie": False, "explanation": "Doğru. Tipik işeme semptomlarıdır."},
            {"text": "Fizik muayenede suprapubik hassasiyet bulunabilir.", "isLie": False, "explanation": "Doğru. Mesane üzerine basmakla ağrır."},
            {"text": "Komplike olmayan basit sistitin olmazsa olmaz şartı 41 derece titremeli yüksek ateştir.", "isLie": True, "explanation": "Tuzak! Komplike olmayan sistitte sistemik ateş SAPTANMAZ; ateş üst sistem tutulumunu (pyelonefrit) gösterir."},
            {"text": "Yaşlı hastalarda sistit asemptomatik veya atipik seyredebilir.", "isLie": False, "explanation": "Doğru. Genel durum bozukluğuyla gelebilir."}
        ]),
        make_quiz("Akut komplike olmayan sistit tanısı alan genç bir kadında aşağıdaki muayene veya klinik bulgulardan hangisinin bulunması BEKLENMEZ?", [
            {"key": "A", "text": "Yüksek ateş ve kostavertebral açı hassasiyeti", "isCorrect": True, "explanation": "Ders notunda 'fizik muayenede suprapubik hassasiyet, ateş saptanmaz' ifadesiyle açıkça vurgulanmıştır. Ateş ve KVAH pyelonefrite aittir."},
            {"key": "B", "text": "Dizüri (idrar yaparken yanma)", "isCorrect": False, "explanation": "Sistitin kardinal semptomudur."},
            {"key": "C", "text": "Pollaküri (sık idrara çıkma)", "isCorrect": False, "explanation": "Sistitin kardinal semptomudur."},
            {"key": "D", "text": "Suprapubik dolgunluk ve hassasiyet", "isCorrect": False, "explanation": "Sistitin tipik fizik bulgusudur."}
        ])
    ]
    slides.append(make_slide(36, "Klinik Sınıflama: Akut Komplike Olmayan Sistit", "Sistit semptomları, pollaküri, dizüri, hematüri ve ateşin bulunmaması kuralı", "Klinik Sınıflama", s36_narrative, s36_bullets, s36_elements))

    # Slide 37: Klinik Sınıflama: Akut Komplike Olmayan Pyelonefrit
    s37_narrative = (
        "Akut pyelonefrit, bakterilerin mesaneden üreterler yoluyla böbrek toplayıcı sistemine ve "
        "parankimine asendan tırmanmasıyla gelişen invaziv bir parankimal enfeksiyondur.\n\n"
        "- **Sistemik Triad:** Enfeksiyonun parankimi tutmasıyla birlikte **yüksek ateş (titreme ile)**, "
        "şiddetli bel veya böğür ağrısı, bulantı ve kusma tablosu ortaya çıkar.\n"
        "- **Kardinal Fizik Muayene:** Fizik muayenede böbrek lojuna uygulanan perküsyonla tek veya "
        "çift taraflı **kostavertebral açı hassasiyeti (KVAH - Giordano pozitifliği)** saptanır.\n"
        "- **Laboratuvar Reaktivitesi:** Lökositoz, sola kayma, belirgin eritrosit sedimantasyon hızı "
        "(ESR) artışı ve **C-reaktif protein (CRP) yüksekliği** eşlik eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ateş, böğür ağrısı ve kostavertebral açı hassasiyeti (KVAH) akut pyelonefritin kardinal triadıdır; sistit semptomları buna eşlik edebilir."
    )
    s37_bullets = [
        "Yüksek ateş, bel/böğür ağrısı, bulantı ve kusma ile karakterizedir.",
        "Kardinal fizik muayene bulgusu kostavertebral açı hassasiyetidir (KVAH).",
        "Laboratuvarda belirgin lökositoz, sedimantasyon ve CRP yüksekliği izlenir."
    ]
    s37_elements = [
        make_cloze("Akut pyelonefrit muayenesinde böbrek lojunda saptanan kardinal fizik muayene bulgusu kostavertebral açı hassasiyetidir.", "kostavertebral açı hassasiyeti", "Böğürde kostovertebral köşeye vurmakla oluşan şiddetli ağrı"),
        make_table("Sistit ve Pyelonefrit Klinik Karşılaştırması", ["Ölçüt", "Akut Sistit", "Akut Pyelonefrit"], [
            {"cells": [{"text": "Vücut Sıcaklığı", "isMasked": False}, {"text": "Ateş saptanmaz (normal)", "isMasked": True, "hint": "ateşin olmaması"}, {"text": "Yüksek ateş ve titreme", "isMasked": True, "hint": "sistemik sıcaklık fırlaması"}]},
            {"cells": [{"text": "Böğür Hassasiyeti", "isMasked": False}, {"text": "KVAH negatif", "isMasked": False}, {"text": "KVAH kuvvetle pozitif", "isMasked": True, "hint": "kostavertebral açı hassasiyeti"}]},
            {"cells": [{"text": "İnflamasyon Belirteçleri", "isMasked": False}, {"text": "CRP ve hemogram normal/hafif", "isMasked": False}, {"text": "Belirgin lökositoz ve yüksek CRP", "isMasked": False}]}
        ]),
        make_chain("Pyelonefrit İnflamasyon Zinciri", [
            "1. Tübüler İnvazyon: Bakteriler renal papilla yoluyla tübüllere ve interstisyuma yayılır.",
            "2. Renal Ödem: Parankimde nötrofil infiltrasyonu ve böbrek kapsülünde gerilme olur.",
            "3. KVAH Oluşumu: Kapsül gerilmesi perküsyonla kostavertebral açıda şiddetli ağrı yapar.",
            "4. Sistemik Sitokin Fırtınası: Pirojenler kana karışarak yüksek ateş ve CRP artışı tetikler."
        ]),
        make_recall("Akut pyelonefritin fizik muayenesinde böbrek tutulumunu gösteren en spesifik bulgu nedir?", "Kostavertebral açı hassasiyetidir (KVAH)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Akut Pyelonefrit", [
            {"text": "Akut pyelonefritte yüksek ateş ve titreme tipik sistemik bulgulardır.", "isLie": False, "explanation": "Doğru. Parankim tutulumunu gösterir."},
            {"text": "Fizik muayenede kostavertebral açı hassasiyeti (KVAH) saptanır.", "isLie": False, "explanation": "Doğru. Kardinal böbrek bulgusudur."},
            {"text": "Akut pyelonefrit hiçbir zaman ağrı veya ateş yapmaz, tamamen sağlıklı hissettirir.", "isLie": True, "explanation": "Tuzak! Akut pyelonefrit yüksek ateş, şiddetli böğür ağrısı, bulantı ve kusma ile acil başvuru gerektirir."},
            {"text": "Laboratuvarda belirgin lökositoz ve CRP yüksekliği eşlik eder.", "isLie": False, "explanation": "Doğru. Akut faz yanıtı oluşur."}
        ]),
        make_quiz("Genç bir kadında ani başlayan 39°C ateş, titreme, sağ böğür ağrısı ve muayenede sağ kostavertebral açı hassasiyeti saptanıyor. En olası klinik tanı hangisidir?", [
            {"key": "A", "text": "Akut komplike olmayan pyelonefrit", "isCorrect": True, "explanation": "Yüksek ateş, böğür ağrısı ve KVAH akut pyelonefritin klasik klinik triadıdır."},
            {"key": "B", "text": "Komplike olmayan akut sistit", "isCorrect": False, "explanation": "Sistitte yüksek ateş ve KVAH saptanmaz."},
            {"key": "C", "text": "Asemptomatik bakteriüri", "isCorrect": False, "explanation": "Asemptomatikte şikayet ve ateş olmaz."},
            {"key": "D", "text": "Primer sifiliz şankrı", "isCorrect": False, "explanation": "Ağrısız genital ülserdir, piyelonefrit yapmaz."}
        ])
    ]
    slides.append(make_slide(37, "Klinik Sınıflama: Akut Komplike Olmayan Pyelonefrit", "Yüksek ateş, böğür ağrısı, kostavertebral açı hassasiyeti (KVAH) ve lökositoz", "Klinik Sınıflama", s37_narrative, s37_bullets, s37_elements))

    # Slide 38: Klinik Sınıflamanın Diğer Formları: Erkeklerde ÜSE ve Tekrarlayan Olgular
    s38_narrative = (
        "ÜSE klinik sınıflama kılavuzlarında, kadınlardaki standart sistit ve pyelonefritin dışında "
        "özgün yönetim gerektiren özel alt kategoriler tanımlanmıştır.\n\n"
        "- **Erkeklerde ÜSE:** Erkek anatomisinde genç yaşta ÜSE görülme olasılığı %1'in altında olduğundan, "
        "**erkeklerde aksi ispatlanmadıkça gelişen her ÜSE komplike kabul edilir**.\n"
        "- **Asemptomatik Bakteriüri:** İdrarda anlamlı bakteri üremesine rağmen hastada dizüri veya "
        "ateş gibi hiçbir klinik semptomun bulunmaması durumudur.\n"
        "- **Tekrarlayan ÜSE (Relaps ve Reenfeksiyon):** Kısa sürede aynı veya farklı mikroorganizmalarla "
        "enfeksiyonun yeniden alevlenmesidir; altta yatan anatomik bozukluk veya kolonizasyon sorgulanmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> Erkek hastada gelişen bir idrar yolu enfeksiyonu aksi kanıtlanana kadar komplike ÜSE olarak değerlendirilir ve anatomik inceleme gerektirir."
    )
    s38_bullets = [
        "Erkeklerde gelişen ÜSE aksi kanıtlanmadıkça komplike kabul edilir.",
        "Asemptomatik bakteriüride hiçbir klinik şikayet bulunmaz.",
        "Tekrarlayan ÜSE relaps ve reenfeksiyon alt tiplerine ayrılır."
    ]
    s38_elements = [
        make_cloze("Erkek hastalarda gelişen üriner sistem enfeksiyonları aksi ispatlanmadıkça komplike kabul edilir.", "komplike", "Yapısal veya sistemik risk içeren enfeksiyon kategorisi"),
        make_table("Özel Klinik Sınıflama Kategorileri", ["Kategori", "Temel Tanım Kriteri", "Klinik Yaklaşım"], [
            {"cells": [{"text": "Erkeklerde ÜSE", "isMasked": False}, {"text": "Aksi ispatlanmadıkça komplike kabul edilir", "isMasked": True, "hint": "erkekteki tüm vakaların kategorisi"}, {"text": "Altta yatan anomali ve prostat araştırması"}]},
            {"cells": [{"text": "Asemptomatik Bakteriüri", "isMasked": False}, {"text": "Semptomsuz anlamlı bakteriüri", "isMasked": False}, {"text": "Özel durumlar hariç tedavi edilmez", "isMasked": True, "hint": "rutin antibiyotik verilmemesi"}]},
            {"cells": [{"text": "Tekrarlayan ÜSE", "isMasked": False}, {"text": "Relaps veya reenfeksiyon atakları", "isMasked": False}, {"text": "Profilaksi ve odak araştırması", "isMasked": False}]}
        ]),
        make_chain("Erkekte ÜSE Değerlendirme Algoritması", [
            "1. Başvuru: Erkek hasta dizüri veya ateş ile başvurur.",
            "2. Kural Hatırlama: Erkekte ÜSE nadirdir ve aksi kanıtlanana kadar komplikedir.",
            "3. Odak Sorgulama: Prostatit, taş, darlık veya kateter aranır.",
            "4. Tedavi Planı: Basit kısa süreli rejim yerine daha uzun ve hedefe yönelik tedavi verilir."
        ]),
        make_recall("Erkek hastalarda gelişen bir üriner sistem enfeksiyonunun sınıflamadaki temel kabulü nedir?", "Aksi ispatlanmadıkça komplike ÜSE kabul edilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Özel Sınıflama Formları", [
            {"text": "Erkeklerde aksi ispatlanmadıkça gelişen ÜSE komplike kabul edilir.", "isLie": False, "explanation": "Doğru. Anatomik araştırma gerektirir."},
            {"text": "Asemptomatik bakteriüride hastada enfeksiyona ait şikayet bulunmaz.", "isLie": False, "explanation": "Doğru. Semptomsuzdur."},
            {"text": "Erkeklerdeki tüm sistitler tamamen zararsızdır ve asla tetkik edilmeden aspirinle geçer.", "isLie": True, "explanation": "Tuzak! Erkekte ÜSE aksi ispatlanana kadar komplikedir ve mutlaka derinlemesine araştırılmalıdır."},
            {"text": "Tekrarlayan ÜSE relaps ve reenfeksiyon olarak ikiye ayrılır.", "isLie": False, "explanation": "Doğru. Mekanizmaları farklıdır."}
        ]),
        make_quiz("Erkek bir hastada idrar yolu enfeksiyonu saptandığında klinik sınıflama açısından temel prensip nedir?", [
            {"key": "A", "text": "Aksi ispatlanmadıkça komplike ÜSE kabul edilmesi", "isCorrect": True, "explanation": "Ders notunda 'erkeklerde aksi ispatlanmadıkça gelişen ÜSE komplike kabul edilir' kuralı yer almaktadır."},
            {"key": "B", "text": "Her zaman tamamen normal ve fizyolojik kabul edilmesi", "isCorrect": False, "explanation": "Erkekte ÜSE patolojiktir."},
            {"key": "C", "text": "Hastanın derhal ameliyata alınıp iki böbreğinin çıkarılması", "isCorrect": False, "explanation": "Gereksiz aşırı müdahaledir."},
            {"key": "D", "text": "Asla idrar kültürü alınmaması kuralı", "isCorrect": False, "explanation": "Erkekte kültür zorunludur."}
        ])
    ]
    slides.append(make_slide(38, "Klinik Sınıflamanın Diğer Formları: Erkeklerde ÜSE ve Tekrarlayan Olgular", "Erkekte komplike kabulü, asemptomatik bakteriüri ve tekrarlayan formlar", "Klinik Sınıflama", s38_narrative, s38_bullets, s38_elements))

    # Slide 39: Dördüncü Bölüm Özeti: Etkenler ve Klinik Tablolar
    s39_narrative = (
        "Üropatojen mikroorganizmalar ve klinik sınıflama arasındaki ilişki, tanısal algoritmanın ve "
        "tedavi yaklaşımının belirlenmesinde merkezi bir role sahiptir.\n\n"
        "- **Monomikrobiyal Baskınlık:** ÜSE olgularının %95'inde tek bakteri saptanır; ezici lider "
        "%70-90 oranıyla Escherichia coli'dir.\n"
        "- **Özel Etkenler:** Proteus türleri üreaz ile struvit taşları üretir; S. saprophyticus genç "
        "cinsel aktif kadınlarda ikinci sıradadır; Adenovirus tip 11 çocukta hemorajik sistit yapar; "
        "Candida ise kateterli ve antibiyotik alanlarda fırsatçıdır.\n"
        "- **Sınıflama Triadı:** Komplike olmayan sistitte ateş ve KVAH yoktur; pyelonefritte ise yüksek ateş, "
        "böğür ağrısı ve KVAH kardinaldir; erkeklerde gelişen ÜSE daima komplike kabul edilir.\n\n"
        "> [!IMPORTANT]\n"
        "> Ateş ve KVAH varlığı enfeksiyonun mesaneden böbreğe sıçradığını (pyelonefrit) kanıtlayan en temel sınıflama kriteridir."
    )
    s39_bullets = [
        "E. coli %70-90 ile en sık üropatojendir; olguların %95'i tektir.",
        "Proteus üreaz/struvit taşı; S. saprophyticus genç kadın; Adenovirus 11 kanamalı sistit etkenidir.",
        "Sistitte ateş saptanmaz; pyelonefritte ateş + KVAH kardinaldir."
    ]
    s39_elements = [
        make_cloze("Klinik sınıflamada akut pyelonefriti akut sistitten ayıran temel kardinal fizik bulgu kostavertebral açı hassasiyetidir.", "kostavertebral açı hassasiyeti", "Böğürde böbrek lojunda hassasiyet"),
        make_table("Etken ve Klinik Eşleştirme Özeti", ["Mikroorganizma", "En Sık Görüldüğü Durum", "Karakteristik Özellik"], [
            {"cells": [{"text": "Escherichia coli", "isMasked": False}, {"text": "Tüm toplum kökenli sistit ve pyelonefritler", "isMasked": True, "hint": "en yaygın üropatojen"}, {"text": "%70-90 ezici görülme sıklığı"}]},
            {"cells": [{"text": "Proteus mirabilis", "isMasked": False}, {"text": "Enfeksiyon taşları ve alkali idrar", "isMasked": False}, {"text": "Üreaz enzimi ile struvit taşları yapma", "isMasked": True, "hint": "magnezyum amonyum fosfat taşları"}]},
            {"cells": [{"text": "Staphylococcus saprophyticus", "isMasked": False}, {"text": "Genç, cinsel aktif kadınlar", "isMasked": False}, {"text": "Novobiosine dirençli koagülaz (-) kok", "isMasked": True, "hint": "genç kadında ikinci sık etken"}]}
        ]),
        make_recall("Genç kadında sistitte 2. en sık etken, çocukta hemorajik sistit etkeni ve taş yapan üreaz pozitif etken hangileridir?", "Genç kadında: S. saprophyticus; Çocukta: Adenovirus tip 11; Taş yapan: Proteus türleridir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Etken ve Tablo Özeti", [
            {"text": "E. coli %70-90 sıklıkla en sık izole edilen üropatojendir.", "isLie": False, "explanation": "Doğru. Açık ara birinci etkendir."},
            {"text": "Proteus türleri üreaz salgılayarak alkali idrar ve struvit taşları yapar.", "isLie": False, "explanation": "Doğru. Taş patofizyolojisidir."},
            {"text": "Akut pyelonefritte ateş asla yükselmez, hastanın vücut ısısı 32 dereceye düşer.", "isLie": True, "explanation": "Tuzak! Pyelonefrit yüksek ateş ve titreme ile seyreden sistemik bir enfeksiyondur."},
            {"text": "Erkeklerde gelişen ÜSE aksi kanıtlanmadıkça komplike kabul edilir.", "isLie": False, "explanation": "Doğru. Temel sınıflama kuralıdır."}
        ]),
        make_quiz("Aşağıdaki mikroorganizma ve klinik tablo eşleştirmelerinden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Adenovirus tip 11 — Çocuklarda akut hemorajik sistit", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "B", "text": "Proteus mirabilis — Üreaz salgısı ve struvit taşları", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "C", "text": "Staphylococcus saprophyticus — Genç cinsel aktif kadında sistit", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "D", "text": "Escherichia coli — Sadece erkek çocuklarda görülen ve asla kadında üremeyen mikrop", "isCorrect": True, "explanation": "Yanlış! E. coli her iki cinsiyette de ve özellikle kadınlarda %70-90 oranla en sık izole edilen üropatojendir."}
        ])
    ]
    slides.append(make_slide(39, "Dördüncü Bölüm Özeti: Etkenler ve Klinik Tablolar", "E. coli, Proteus, S. saprophyticus, Adenovirus 11 ve sistit vs pyelonefrit", "Konsolidasyon", s39_narrative, s39_bullets, s39_elements))

    # Slide 40: [TEKRAR SAYFASI - CHECKPOINT 4] Etkenler ve Klinik Sınıflama
    s40_narrative = (
        "Bu tekrar sayfasında 4. Bölümde detaylandırılan üropatojen mikroorganizmaların biyolojik "
        "özelliklerini ve klinik sınıflama basamaklarını konsolide ediyoruz.\n\n"
        "- **Patojenler Galerisi:** E. coli %70-90 ile tartışmasız liderdir. Proteus üreaz ile struvit "
        "taşları örer. S. saprophyticus genç cinsel aktif kadında ikinci sıradadır. Adenovirus tip 11 "
        "çocukta hemorajik sistit yapar. Candida ise kateterli antibiyotik alanlarda belirir.\n"
        "- **Sistit vs Pyelonefrit:** Akut sistitte sadece suprapubik hassasiyet vardır, ateş ve KVAH "
        "kesinlikle bulunmaz. Akut pyelonefritte ise yüksek ateş, böğür ağrısı ve KVAH kardinaldir.\n"
        "- **Erkek Kuralı:** Erkeklerde gelişen her ÜSE aksi kanıtlanana kadar komplike kabul edilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] E. coli (%70-90); Proteus (üreaz/taş); Adenovirus 11 (çocuk hemorajik); sistitte ateş YOK; pyelonefritte ateş + KVAH VAR!"
    )
    s40_bullets = [
        "E. coli (%70-90); Proteus (üreaz/struvit); S. saprophyticus (genç kadın).",
        "Adenovirus tip 11 çocuklarda akut hemorajik sistit etkenidir.",
        "Sistitte ateş YOKTUR; pyelonefritte yüksek ateş + KVAH KARDİNALDİR."
    ]
    s40_elements = [
        make_cloze("Klinik pratikte çocukluk çağında hemorajik sistit yapan virüs Adenovirus tip 11 olarak bilinir.", "Adenovirus tip 11", "Çocuklarda kanamalı sistit yapan viral serotip"),
        make_table("4. Bölüm Büyük Tekrar Tablosu", ["Konu", "Kardinal Bilgi", "Sınav Spotu"], [
            {"cells": [{"text": "En Sık Üropatojen", "isMasked": False}, {"text": "E. coli (%70-90)", "isMasked": True, "hint": "açık ara en sık etken"}, {"text": "Olguların %95'inde tek bakteri izole edilir"}]},
            {"cells": [{"text": "Taş Yapan Bakteri", "isMasked": False}, {"text": "Proteus mirabilis (üreaz pozitif)", "isMasked": False}, {"text": "Magnezyum amonyum fosfat (struvit) taşları", "isMasked": True, "hint": "alkali idrarda çöken taş"}]},
            {"cells": [{"text": "Sistit Ayırıcı Tanısı", "isMasked": False}, {"text": "Ateş ve KVAH saptanmaz", "isMasked": True, "hint": "sistitte olmayan bulgular"}, {"text": "Ateş varsa pyelonefrit veya komplike ÜSE'dir"}]},
            {"cells": [{"text": "Erkekte ÜSE Prensibi", "isMasked": False}, {"text": "Aksi ispatlanmadıkça komplike kabul", "isMasked": False}, {"text": "Anatomik anomali ve prostat araştırması şarttır", "isMasked": False}]}
        ]),
        make_chain("4. Bölüm Tanısal Karar Akışı", [
            "1. İdrar Şikayeti: Hasta yanma ve sık idrarla başvurur.",
            "2. Muayene ve Ateş Kontrolü: Ateş yok, KVAH yoksa → Akut sistit.",
            "3. Ateş Kontrolü: 39°C ateş ve KVAH pozitifse → Akut pyelonefrit.",
            "4. Cinsiyet Kontrolü: Hasta erkekse → Aksi ispatlanana kadar Komplike ÜSE."
        ]),
        make_recall("Akut sistit ile akut pyelonefriti birbirinden ayıran iki kardinal klinik muayene bulgusu nedir?", "Yüksek ateş ve kostavertebral açı hassasiyetidir (KVAH). Sistitte ikisi de yoktur, pyelonefritte ikisi de vardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 4. Bölüm Konsolidasyonu", [
            {"text": "E. coli %70-90 sıklıkla en sık izole edilen üropatojendir.", "isLie": False, "explanation": "Doğru. Açık ara birinci etkendir."},
            {"text": "Çocuklarda Adenovirus tip 11 hemorajik sistite yol açar.", "isLie": False, "explanation": "Doğru. Karakteristik viral etkendir."},
            {"text": "Komplike olmayan akut sistitte yüksek ateş ve kostavertebral açı hassasiyeti tipik bulgulardır.", "isLie": True, "explanation": "Tuzak! Komplike olmayan sistitte ateş ve KVAH KESİNLİKLE SAPTANMAZ; bunlar pyelonefrit bulgularıdır."},
            {"text": "Proteus türleri üreaz enzimi salgılayarak struvit taşları yapar.", "isLie": False, "explanation": "Doğru. Magnezyum amonyum fosfat taşlarıdır."}
        ]),
        make_quiz("4. Bölümün temel kazanımlarına göre aşağıdaki klinik ve etiyolojik eşleştirmelerden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Komplike olmayan sistit — 40°C titremeli yüksek ateş ve pozitif KVAH", "isCorrect": True, "explanation": "Kesinlikle yanlış! Sistitte sistemik ateş ve KVAH saptanmaz; bu bulgular akut pyelonefrite aittir."},
            {"key": "B", "text": "Escherichia coli — ÜSE'lerin %70-90'ından sorumlu en sık etken", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Proteus mirabilis — Üreaz aktivitesi ve magnezyum amonyum fosfat taşları", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Adenovirus tip 11 — Çocuklarda görülen akut hemorajik sistit", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(40, "[TEKRAR SAYFASI - CHECKPOINT 4] Etkenler ve Klinik Sınıflama", "4. Bölümün kapsamlı pekiştirmesi: üropatojenler, virülans, sistit ve pyelonefrit ayrımı", "Bölüm Tekrarı", s40_narrative, s40_bullets, s40_elements))

    return slides
