# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec4():
    slides = []

    # Slide 31: ÜSE Etiyolojisini Belirleyen Faktörler
    s31_narrative = (
        "Üriner sistem enfeksiyonuna yol açan mikroorganizmaların dağılımı, hastanın klinik "
        "özelliklerine, eşlik eden hastalıklara ve maruz kaldığı tıbbi işlemlere göre değişir.\n\n"
        "- **Etkili Faktörler:** Etiyolojiyi belirleyen temel faktörler **yaş, diyabet varlığı, "
        "nörolojik komorbiditeler ve kateterizasyon**dur.\n"
        "- **Klinik Ortam:** Genç, sağlıklı ve toplum kökenli bireylerde etken spektrumu son derece "
        "dar iken; yaşlı, diyabetik veya hastanede yatan hastalarda çok daha çeşitli ve dirençli etkenler görülür.\n"
        "- **Komorbidite Etkisi:** Örneğin diyabet immüniteyi baskılarken, nörolojik hastalıklar "
        "mesane boşalımını bozarak farklı fırsatçı patojenlerin üremesine zemin hazırlar.\n\n"
        "> [!NOTE]\n"
        "> ÜSE etiyolojisini belirleyen temel konak faktörleri: Yaş, diyabet varlığı, nörolojik komorbiditeler ve kateterizasyondur."
    )
    s31_bullets = [
        "Etiyolojide etkili faktörler: Yaş, diyabet varlığı, nörolojik komorbiditeler, kateterizasyon.",
        "Sağlıklı genç bireyler ile komorbiditesi olan hastalar farklı mikrobiyal spektruma sahiptir.",
        "Kateterizasyon ve nörolojik disfonksiyon fırsatçı ve polimikrobiyal üremeyi kolaylaştırır."
    ]
    s31_elements = [
        make_cloze("Üriner sistem enfeksiyonu etiyolojisinde yaş, diyabet varlığı, nörolojik komorbiditeler ve kateterizasyon etkili faktörlerdir.", "kateterizasyon", "İdrar yoluna yabancı cisim yerleştirilmesi işlemi"),
        make_table("Etiyolojiyi Belirleyen Konak ve Girişim Faktörleri", ["Faktör", "Fizyopatolojik Etki", "Mikrobiyolojik Yansıma"], [
            {"cells": [{"text": "Yaş ve Diyabet", "isMasked": False}, {"text": "Hücresel immün yetmezlik ve glukozüri", "isMasked": True, "hint": "bağışıklık düşüşü ve idrarda şeker"}, {"text": "Daha geniş patojen spektrumu"}]},
            {"cells": [{"text": "Kateterizasyon", "isMasked": False}, {"text": "Biyofilm ve intraluminal giriş yolu", "isMasked": False}, {"text": "Dirençli ve polimikrobiyal etkenler", "isMasked": True, "hint": "çoklu ilaç dirençli bakteriler"}]}
        ]),
        make_chain("Etiyolojik Dağılımı Belirleyen Süreç", [
            "1. Konak Durumu: Yaş, diyabet veya nörolojik hastalığın varlığı.",
            "2. İnvaziv Girişim: Mesane kateterizasyonu uygulanması.",
            "3. Savunma Zafiyeti: Doğal mekanik ve immün engellerin zayıflaması.",
            "4. Patojen Çeşitlenmesi: Fırsatçı ve dirençli bakterilerin sahneye çıkması."
        ]),
        make_recall("Ders notuna göre ÜSE etiyolojisinde etkili olan dört temel faktör nedir?", "Yaş, diyabet varlığı, nörolojik komorbiditeler ve kateterizasyondur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Etiyolojik Faktörler", [
            {"text": "Yaş ve diyabet varlığı ÜSE etiyolojisinde etkili faktörlerdir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Nörolojik komorbiditeler ve kateterizasyon patojen spektrumunu değiştirir.", "isLie": False, "explanation": "Doğru. Fırsatçı etkenleri artırır."},
            {"text": "Diyabetik olmak ve kateter takılması bakterileri korkutup üriner sistemi steril tutar.", "isLie": True, "explanation": "Tuzak! Tam aksine diyabet ve kateterizasyon enfeksiyon ve dirençli patojen riskini katlar."},
            {"text": "Farklı hasta gruplarında etken mikroorganizmalar değişkenlik gösterir.", "isLie": False, "explanation": "Doğru. Klinik tabloya göre değişir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarında etiyolojik ajanların dağılımında etkili faktörler arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Yaş, diyabet varlığı, nörolojik komorbiditeler ve kateterizasyon", "isCorrect": True, "explanation": "Ders notunda 'Etiyoloji: yaş, diyabet varlığı, nörolojik komorbiditeler ve kateterizasyon etkili faktörlerdir' şeklinde açıkça belirtilmiştir."},
            {"key": "B", "text": "Yalnızca saç rengi ve göz rengi", "isCorrect": False, "explanation": "Etiyoloji ile ilgisiz genetik özelliklerdir."},
            {"key": "C", "text": "Kişinin kan grubunun Rh pozitif olması", "isCorrect": False, "explanation": "Ders notunda yer almaz."},
            {"key": "D", "text": "Sadece deniz seviyesinde yaşamak", "isCorrect": False, "explanation": "Etiyolojiyi belirleyen bir faktör değildir."}
        ])
    ]
    slides.append(make_slide(31, "ÜSE Etiyolojisini Belirleyen Faktörler", "Yaş, diyabet, nörolojik komorbidite ve kateterizasyonun etiyolojiye etkisi", "Etiyoloji", s31_narrative, s31_bullets, s31_elements))

    # Slide 32: Escherichia coli: Açık Ara En Sık Etken
    s32_narrative = (
        "Gerek toplumda gerekse hastane ortamında gelişen üriner sistem enfeksiyonlarında tek bir "
        "mikroorganizma mutlak bir epidemiyolojik hakimiyete sahiptir.\n\n"
        "- **En Sık Etken:** **E. coli en sık etkendir** ve tüm ÜSE formlarının merkezinde yer alır.\n"
        "- **Görüldüğü Gruplar:** E. coli; **toplum kökenli, sağlık bakımı ilişkili, diyabetik hastalar "
        "ve tüm yaş gruplarında** en sık izole edilen bakteridir.\n"
        "- **Üropatojenik Donanım:** E. coli'nin bağırsak florasında dominant olması, taşıdığı zengin "
        "fimbriya tipleri (Tip 1 ve P fimbriya) ve ürotelyal tropizmi onu birinci sıraya taşır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] E. coli en sık etkendir; toplum kökenli, sağlık bakımı ilişkili, diyabetik hastalar ve tüm yaş gruplarında birinci sıradadır."
    )
    s32_bullets = [
        "E. coli en sık etkendir.",
        "Toplum kökenli, sağlık bakımı ilişkili ve diyabetik tüm gruplarda görülür.",
        "Tüm yaş gruplarında ÜSE etiyolojisinin tartışmasız lideridir."
    ]
    s32_elements = [
        make_cloze("Tüm yaş gruplarında ve hasta kategorilerinde üriner sistem enfeksiyonlarının en sık etkeni E. coli bakterisidir.", "E. coli", "ÜSE'de açık ara birinci sırada izole edilen Gram negatif basil"),
        make_table("E. coli'nin Klinik Gruplara Göre Dağılımı", ["Klinik Hasta Grubu", "İzolasyon Durumu", "Klinik Özellik"], [
            {"cells": [{"text": "Toplum Kökenli ÜSE", "isMasked": False}, {"text": "En sık etken (lider)", "isMasked": True, "hint": "birinci sıradaki mikrop"}, {"text": "Akut sistit ve piyelonefritlerin çoğunluğu"}]},
            {"cells": [{"text": "Sağlık Bakımı İlişkili", "isMasked": False}, {"text": "En sık etken (lider)", "isMasked": False}, {"text": "Dirençli suşlarla kolonizasyon", "isMasked": True, "hint": "hastane kökenli E. coli direnci"}]},
            {"cells": [{"text": "Diyabetik ve Tüm Yaşlar", "isMasked": False}, {"text": "En sık etken (lider)", "isMasked": True, "hint": "tüm gruplarda birinci"}, {"text": "Her hasta grubunda baskın görülme"}]}
        ]),
        make_chain("E. coli Epidemiyolojik Baskınlık Zinciri", [
            "1. Fekal Rezervuar: Bağırsak florasında milyarlarca E. coli bulunması.",
            "2. Perineal Kolonizasyon: Anüs çevresinden introitusa yayılım.",
            "3. Ürotelyal Tropizm: Fimbriyalarla mesane mannoz reseptörlerine yapışma.",
            "4. Lider Etken: Toplumdan hastaneye tüm gruplarda en sık enfeksiyon yapma."
        ]),
        make_recall("Toplum kökenli, sağlık bakımı ilişkili, diyabetik ve tüm yaş gruplarında en sık görülen ÜSE etkeni nedir?", "Escherichia coli'dir (E. coli)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: E. coli", [
            {"text": "E. coli üriner sistem enfeksiyonlarında en sık etkendir.", "isLie": False, "explanation": "Doğru. Ders notunun en temel spotudur."},
            {"text": "E. coli toplum kökenli ve sağlık bakımı ilişkili tüm gruplarda sık görülür.", "isLie": False, "explanation": "Doğru. Her grupta liderdir."},
            {"text": "E. coli yalnızca kutup ayılarında üriner enfeksiyon yapar, insanlarda hiçbir zaman görülmez.", "isLie": True, "explanation": "Tuzak! E. coli insanlarda en sık görülen ÜSE etkenidir."},
            {"text": "Diyabetik hastalarda da en sık etken E. coli'dir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Toplum kökenli, sağlık bakımı ilişkili, diyabetik hastalar ve tüm yaş gruplarında ÜSE'nin EN SIK etkeni aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "E. coli", "isCorrect": True, "explanation": "Ders notunda 'E. coli en sık etkendir; toplum kökenli, sağlık bakımı ilişkili, diyabetik hastalar ve tüm yaş gruplarında görülür' denmektedir."},
            {"key": "B", "text": "Staphylococcus epidermidis", "isCorrect": False, "explanation": "Deri florası elemanıdır, en sık etken değildir."},
            {"key": "C", "text": "Clostridium tetani", "isCorrect": False, "explanation": "Tetanos etkenidir, ÜSE yapmaz."},
            {"key": "D", "text": "Streptococcus pneumoniae", "isCorrect": False, "explanation": "Pnömokok solunum yolu etkenidir."}
        ])
    ]
    slides.append(make_slide(32, "En Sık Etken: Escherichia coli", "Toplum kökenli, sağlık bakımı ilişkili, diyabetik ve tüm yaşlarda E. coli hakimiyeti", "Etiyoloji", s32_narrative, s32_bullets, s32_elements))

    # Slide 33: Genç Kadınlarda Akut Sistit: Staphylococcus saprophyticus
    s33_narrative = (
        "Genç ve cinsel aktif kadınlarda ortaya çıkan akut sistit olgularında, enterik Gram negatif "
        "basillerin dışında çok karakteristik bir Gram pozitif kok etkeni dikkat çeker.\n\n"
        "- **Spesifik Etken:** **Staphylococcus saprophyticus**, genç-orta yaş kadınlarda akut sistitin "
        "E. coli'den sonraki en önemli etkenidir.\n"
        "- **Biyolojik Özellik:** Koagülaz-negatif bir stafilokok olan S. saprophyticus, novobiosine "
        "doğal dirençlidir ve üroepitele tutunmayı sağlayan özel adezinlere sahiptir.\n"
        "- **Epidemiyolojik Dağılım:** Yaşlı erkeklerde veya hastanede yatan hastalarda nadirken, "
        "özellikle genç-orta yaş poliklinik hastalarında belirgin bir yoğunluk gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Staphylococcus saprophyticus: Genç-orta yaş kadınlarda akut sistitin karakteristik etkenidir."
    )
    s33_bullets = [
        "Staphylococcus saprophyticus: Genç-orta yaş kadınlarda akut sistit etkenidir.",
        "Koagülaz-negatif stafilokok olup novobiosine dirençlidir.",
        "Genç kadın popülasyonunda E. coli'den sonra ikinci sıklıkta izole edilir."
    ]
    s33_elements = [
        make_cloze("Genç ve orta yaş kadınlarda akut sistit tablosuna yol açan stafilokok türü Staphylococcus saprophyticus bakterisidir.", "Staphylococcus saprophyticus", "Genç kadınlarda akut sistit yapan koagülaz negatif stafilokok"),
        make_table("S. saprophyticus Klinik Profili", ["Klinik Özellik", "Tanımlayıcı Bilgi", "Laboratuvar / Ayırıcı Özellik"], [
            {"cells": [{"text": "Hedef Popülasyon", "isMasked": False}, {"text": "Genç-orta yaş kadınlar", "isMasked": True, "hint": "cinsel aktif kadın kitle"}, {"text": "Poliklinik akut sistit başvurusu"}]},
            {"cells": [{"text": "Mikrobiyoloji", "isMasked": False}, {"text": "Koagülaz negatif stafilokok", "isMasked": False}, {"text": "Novobiosine dirençli olması", "isMasked": True, "hint": "laboratuvardaki ayırt edici antibiyotik direnci"}]}
        ]),
        make_chain("S. saprophyticus Sistit Zinciri", [
            "1. Kolonizasyon: Genç kadında periüretral ve vajinal alanda bulunma.",
            "2. Cinsel Aktivite: Mekanik hareketle üretraya geçiş.",
            "3. Mukozal Kilitlenme: Üroepitel hücrelerine özgül adezinlerle tutunma.",
            "4. Akut Sistit: Dizüri, sık idrara çıkma ve piyüri tablosu."
        ]),
        make_recall("Genç-orta yaş kadınlarda akut sistite yol açan karakteristik koagülaz negatif stafilokok hangisidir?", "Staphylococcus saprophyticus'tur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: S. saprophyticus", [
            {"text": "Staphylococcus saprophyticus genç-orta yaş kadınlarda akut sistit etkenidir.", "isLie": False, "explanation": "Doğru. Ders notundaki net bilgidir."},
            {"text": "S. saprophyticus koagülaz negatif stafilokoklar sınıfındadır.", "isLie": False, "explanation": "Doğru. Mikrobiyolojik özelliğidir."},
            {"text": "S. saprophyticus yalnızca 95 yaşındaki erkeklerde prostatit yapar, kadınlarda asla görülmez.", "isLie": True, "explanation": "Tuzak! Tam aksine genç-orta yaş kadınlarda akut sistitin tipik etkenidir."},
            {"text": "Genç kadınlarda sistit olgularında E. coli'den sonra akla gelmelidir.", "isLie": False, "explanation": "Doğru. Klasik ikinci etkendir."}
        ]),
        make_quiz("Genç-orta yaş kadınlarda akut sistit etkeni olarak ders notunda özellikle vurgulanan mikroorganizma aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Staphylococcus saprophyticus", "isCorrect": True, "explanation": "Ders notunda 'Staphylococcus saprophyticus: genç-orta yaş kadınlarda akut sistit' şeklinde açıkça belirtilmiştir."},
            {"key": "B", "text": "Streptococcus agalactiae", "isCorrect": False, "explanation": "Grup B streptokoktur, akut sistitin bu tipik etkeni değildir."},
            {"key": "C", "text": "Listeria monocytogenes", "isCorrect": False, "explanation": "Menenjit ve besin zehirlenmesi etkenidir."},
            {"key": "D", "text": "Bacillus anthracis", "isCorrect": False, "explanation": "Şarbon etkenidir, sistitle ilgisizdir."}
        ])
    ]
    slides.append(make_slide(33, "Genç Kadınlarda Akut Sistit: S. saprophyticus", "Staphylococcus saprophyticus'un genç-orta yaş kadınlardaki önemi", "Etiyoloji", s33_narrative, s33_bullets, s33_elements))

    # Slide 34: Komplike ve Sağlık Bakımı İlişkili Etkenler: Klebsiella, Proteus, Pseudomonas
    s34_narrative = (
        "Hastane ortamında yatan, kateter uygulanan veya altta yatan yapısal/metabolik bozukluğu "
        "bulunan hastalarda etken mikroorganizmalar belirgin biçimde farklılaşır.\n\n"
        "- **Komplike Patojenler:** **Klebsiella spp., Proteus spp., Pseudomonas spp., Enterococcus spp. "
        "ve Enterobacter spp.**; sağlık bakımı ilişkili, komplike ÜSE, diyabetik hastalar ve tekrarlayan ÜSE'de sık görülür.\n"
        "- **Sağlık Bakımı İlişkisi:** Bu bakteriler hastane ortamındaki selektif antibiyotik baskısı "
        "altında çoğalarak çoklu ilaç direnci (ÇİD) geliştirir.\n"
        "- **Diyabet ve Nüks:** Bozulmuş konak immünitesi ve sık antibiyotik kullanımı bu patojenlerin "
        "kalıcı kolonizasyonuna ve tekrarlayan ataklara yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> Klebsiella, Proteus, Pseudomonas, Enterococcus ve Enterobacter: Sağlık bakımı ilişkili, komplike ÜSE, diyabetik ve tekrarlayan ÜSE hastalarında ön plana çıkar."
    )
    s34_bullets = [
        "Etkenler: Klebsiella, Proteus, Pseudomonas, Enterococcus, Enterobacter.",
        "Sağlık bakımı ilişkili ve komplike üriner sistem enfeksiyonlarında sık izole edilir.",
        "Diyabetik hastalarda ve tekrarlayan ÜSE olgularında görülme sıklığı artar."
    ]
    s34_elements = [
        make_cloze("Klebsiella, Proteus, Pseudomonas ve Enterococcus türleri sağlık bakımı ilişkili ve komplike ÜSE olgularında sık izole edilir.", "komplike ÜSE", "Altta yatan yapısal, fonksiyonel veya metabolik risk faktörü olan enfeksiyon"),
        make_table("Komplike ve Nozokomiyal Patojenler", ["Patojen Grubu", "Klinik Özellik", "Görüldüğü Hasta Profili"], [
            {"cells": [{"text": "Klebsiella ve Enterobacter", "isMasked": False}, {"text": "GSBL ve çoklu ilaç direnci", "isMasked": True, "hint": "beta laktam direnç enzimleri"}, {"text": "Hastanede yatan ve diyabetik hastalar"}]},
            {"cells": [{"text": "Proteus spp.", "isMasked": False}, {"text": "Üreaz enzimi ile idrarı alkalileştirme", "isMasked": False}, {"text": "Struvit taşları ve tekrarlayan ÜSE", "isMasked": True, "hint": "enfeksiyon taşı oluşumu"}]},
            {"cells": [{"text": "Pseudomonas ve Enterococcus", "isMasked": False}, {"text": "İntrensek direnç ve enstrümantasyon", "isMasked": True, "hint": "kateter ve doğal antibiyotik direnci"}, {"text": "Sağlık bakımı ilişkili ve kateterli olgular"}]}
        ]),
        make_chain("Komplike Enfeksiyon Gelişim Zinciri", [
            "1. Hastaneye Yatış / Diyabet: Konak savunmasının bozulması.",
            "2. Enstrümantasyon: Kateter veya cerrahi girişim uygulanması.",
            "3. Nozokomiyal Kolonizasyon: Klebsiella, Proteus veya Pseudomonas girişi.",
            "4. Komplike ÜSE: Çoklu dirençli etkenlerle inatçı enfeksiyon."
        ]),
        make_recall("Sağlık bakımı ilişkili, komplike ÜSE, diyabetik ve tekrarlayan ÜSE olgularında sık görülen beş etken grubu nedir?", "Klebsiella spp., Proteus spp., Pseudomonas spp., Enterococcus spp. ve Enterobacter spp.'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komplike Etkenler", [
            {"text": "Klebsiella, Proteus ve Pseudomonas sağlık bakımı ilişkili ÜSE'de sık görülür.", "isLie": False, "explanation": "Doğru. Ders notu listesidir."},
            {"text": "Diyabetik hastalarda ve tekrarlayan ÜSE'de Enterococcus ve Enterobacter izole edilebilir.", "isLie": False, "explanation": "Doğru. Komplike etkenlerdir."},
            {"text": "Pseudomonas yalnızca taze sıkılmış portakal suyunda ürer, insanda asla bulunmaz.", "isLie": True, "explanation": "Tuzak! Pseudomonas hastane ortamında ve komplike ÜSE'de çok önemli bir patojendir."},
            {"text": "Proteus üreaz üreterek taş oluşumuna zemin hazırlayabilir.", "isLie": False, "explanation": "Doğru. Önemli bir klinik özelliğidir."}
        ]),
        make_quiz("Sağlık bakımı ilişkili, komplike ÜSE, diyabetik hastalar ve tekrarlayan ÜSE'de sık görülen etkenler arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Klebsiella spp., Proteus spp., Pseudomonas spp., Enterococcus spp., Enterobacter spp.", "isCorrect": True, "explanation": "Ders notunda birebir bu liste komplike ve sağlık bakımı ilişkili etkenler olarak verilmiştir."},
            {"key": "B", "text": "Yalnızca Rickettsia ve Chlamydia", "isCorrect": False, "explanation": "Klasik komplike bakteriyel ÜSE etkenleri değildir."},
            {"key": "C", "text": "Sadece Treponema pallidum", "isCorrect": False, "explanation": "Sifiliz etkenidir."},
            {"key": "D", "text": "Bordetella pertussis", "isCorrect": False, "explanation": "Boğmaca etkenidir."}
        ])
    ]
    slides.append(make_slide(34, "Komplike ve Nozokomiyal Etkenler: Klebsiella, Proteus, Pseudomonas", "Sağlık bakımı ilişkili, diyabetik ve komplike olgularda izole edilen bakteriler", "Etiyoloji", s34_narrative, s34_bullets, s34_elements))

    # Slide 35: Candida Türleri: Kateter ve Antibiyotik Kullanımı
    s35_narrative = (
        "Üriner sistemde mantar enfeksiyonları sağlıklı bireylerde neredeyse hiç görülmezken, "
        "belirli iyatrojenik girişimler sonrasında hızla ortaya çıkar.\n\n"
        "- **Candida spp. Etiyolojisi:** Üriner sistemde Candida türlerinin üremesi doğrudan **üriner "
        "kateterizasyon ve antibiyotik kullanımı** ile ilişkilidir.\n"
        "- **Flora Baskılanması:** Geniş spektrumlu antibiyotiklerin uzun süreli kullanımı, perineal "
        "ve ürogenital bölgedeki koruyucu bakteriyel florayı ortadan kaldırarak mantarların aşırı çoğalmasına yol açar.\n"
        "- **Kateter Biyofilmi:** Üriner kateterlerin plastik yüzeyleri Candida için mükemmel bir biyofilm "
        "tutunma alanı sağlayarak kolonizasyon ve kandidüriye zemin hazırlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Candida spp. etiyolojisindeki iki temel tetikleyici faktör: Üriner kateterizasyon ve antibiyotik kullanımıdır."
    )
    s35_bullets = [
        "Candida spp.: Üriner kateterizasyon ve antibiyotik kullanımı ile ilişkilidir.",
        "Antibiyotikler koruyucu bakteriyel florayı yok ederek mantar üremesine alan açar.",
        "Kateter yüzeyleri Candida biyofilmi için zemin hazırlar."
    ]
    s35_elements = [
        make_cloze("Üriner sistemde Candida spp. üremesini tetikleyen en önemli iki faktör üriner kateterizasyon ve antibiyotik kullanımıdır.", "üriner kateterizasyon ve antibiyotik kullanımı", "Kandidüriye zemin hazırlayan iki temel iyatrojenik faktör"),
        make_table("Candida Üremesinde Risk Faktörleri", ["Risk Faktörü", "Biyolojik Mekanizma", "Klinik Yansıması"], [
            {"cells": [{"text": "Geniş Spektrumlu Antibiyotikler", "isMasked": False}, {"text": "Bakteriyel floranın baskılanması", "isMasked": True, "hint": "koruyucu mikropların ölmesi"}, {"text": "Fırsatçı Candida kolonizasyonu"}]},
            {"cells": [{"text": "Üriner Kateterizasyon", "isMasked": False}, {"text": "Yabancı cisim yüzeyinde biyofilm", "isMasked": False}, {"text": "Kandidüri ve kateter mantar enfeksiyonu", "isMasked": True, "hint": "idrarda mantar saptanması"}]}
        ]),
        make_chain("Candida İnvazyon Zinciri", [
            "1. Geniş Spektrumlu Antibiyotik: Bakteriyel dengenin bozulması.",
            "2. Kateter Takılması: Mesaneye yabancı cisim yerleştirilmesi.",
            "3. Biyofilm Oluşumu: Candida mayalarının kateter lümenine yapışması.",
            "4. Kandidüri Gelişimi: İdrarda Candida üremesi saptanması."
        ]),
        make_recall("Ders notuna göre Candida türlerinin üriner sistemde ortaya çıkmasına zemin hazırlayan iki temel faktör nedir?", "Üriner kateterizasyon ve antibiyotik kullanımıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Candida Türleri", [
            {"text": "Candida spp. üriner kateterizasyon ve antibiyotik kullanımı ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Geniş spektrumlu antibiyotikler mantarların aşırı çoğalmasına fırsat yaratır.", "isLie": False, "explanation": "Doğru. Bakteri florasını yok eder."},
            {"text": "Candida sağlıklı genç sporcularda her gün kendiliğinden oluşan doğal idrar vitaminidir.", "isLie": True, "explanation": "Tuzak! Candida bir maya mantarıdır, kateter ve antibiyotik kullanımıyla ortaya çıkan fırsatçı bir etkendir."},
            {"text": "Kateter yüzeyleri Candida biyofilmi için uygun ortamdır.", "isLie": False, "explanation": "Doğru. Katetere kolay tutunur."}
        ]),
        make_quiz("Üriner sistemde Candida spp. enfeksiyonu ve kandidüri gelişiminde rol oynayan temel etiyolojik faktörler aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Üriner kateterizasyon ve antibiyotik kullanımı", "isCorrect": True, "explanation": "Ders notunda 'Candida spp.: üriner kateterizasyon ve antibiyotik kullanımı' şeklinde net olarak verilmiştir."},
            {"key": "B", "text": "Yalnızca aşırı havuç ve ıspanak tüketimi", "isCorrect": False, "explanation": "Beslenme ile kandidüri ilişkisi yoktur."},
            {"key": "C", "text": "Çocukluk aşılarının tam yapılmış olması", "isCorrect": False, "explanation": "Aşılar kandidüri yapmaz."},
            {"key": "D", "text": "Günde 3 litre su içilmesi", "isCorrect": False, "explanation": "Hidrasyon koruyucudur, mantar nedeni değildir."}
        ])
    ]
    slides.append(make_slide(35, "Fırsatçı Mantar Etkenleri: Candida Türleri", "Üriner kateterizasyon ve antibiyotik kullanımının kandidüriye yol açması", "Etiyoloji", s35_narrative, s35_bullets, s35_elements))

    # Slide 36: Diyabetik Hastalarda Etiyolojik Farklılıklar
    s36_narrative = (
        "Diabetes mellitus, oluşturduğu metabolik bozukluklar ve immün disfonksiyon nedeniyle "
        "üriner sistem enfeksiyonu etiyolojisinde özel bir yere sahiptir.\n\n"
        "- **Baskın Etken:** Diyabetik hastalarda da **E. coli en sık etken** olmaya devam eder; "
        "ancak diyabetik olmayanlara göre spektrum belirgin biçimde genişlemiştir.\n"
        "- **Komplike ve Dirençli Patojenler:** Diyabetlilerde Klebsiella, Proteus, Enterobacter, "
        "Pseudomonas ve Enterococcus türleri ile enfeksiyon riski çok daha yüksektir.\n"
        "- **Mantar Yatkınlığı:** Glukozüri (idrarda şeker bulunması) ve nörojen mesane stazı, "
        "Candida türlerinin üremesini ve amfizematöz sistit/piyelonefrit gelişimini kolaylaştırır.\n\n"
        "> [!NOTE]\n"
        "> Diyabetik hastalarda E. coli en sık etken olmayı sürdürür; ancak Klebsiella, Proteus, Pseudomonas, Enterococcus ve Candida gibi komplike etkenler belirgin şekilde artar."
    )
    s36_bullets = [
        "Diyabetik hastalarda E. coli en sık etken olmayı sürdürür.",
        "Klebsiella, Proteus, Enterobacter, Pseudomonas ve Enterococcus sıklığı artmıştır.",
        "Glukozüri ve immün baskılanma Candida üremesi için zemin hazırlar."
    ]
    s36_elements = [
        make_cloze("Diyabetik hastalarda E. coli en sık etken olmakla birlikte komplike patojenler ve Candida türleri daha sık görülür.", "Candida", "Diyabetiklerde glukozüri ile kolaylaşan fırsatçı maya mantarı"),
        make_table("Diyabette ÜSE Etiyolojik Dağılımı", ["Patojen Kategorisi", "Görülme Durumu", "Diyabetik Zemin"], [
            {"cells": [{"text": "E. coli", "isMasked": False}, {"text": "En sık etken (lider)", "isMasked": True, "hint": "yine birinci sırada"}, {"text": "Tüm gruplarda olduğu gibi baskın"}]},
            {"cells": [{"text": "Klebsiella, Proteus, Pseudomonas", "isMasked": False}, {"text": "Sıklığı belirgin artmış", "isMasked": False}, {"text": "Tekrarlayan ve komplike enfeksiyon", "isMasked": True, "hint": "dirençli bakteriyel çeşitlilik"}]},
            {"cells": [{"text": "Candida Türleri", "isMasked": False}, {"text": "Yüksek risk", "isMasked": True, "hint": "mantar enfeksiyonu artışı"}, {"text": "Glukozüri ve immün yetmezlik"}]}
        ]),
        make_chain("Diyabette Patojen Değişim Zinciri", [
            "1. Hiperglisemi ve Glukozüri: İdrarda şeker bulunması.",
            "2. Nörojen Mesane: Boşalma bozukluğu ve rezidüel idrar stazı.",
            "3. İmmün Baskılanma: Lökosit fagositoz fonksiyonlarında zayıflama.",
            "4. Komplike Patojenler: Klebsiella, Pseudomonas ve Candida'nın yerleşmesi."
        ]),
        make_recall("Diyabetik hastalarda en sık görülen etken nedir ve spektrumda hangi mikroorganizmalar artış gösterir?", "En sık etken yine E. coli'dir; ancak Klebsiella, Proteus, Pseudomonas, Enterococcus ve Candida sıklığı artmıştır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Diyabette Etiyoloji", [
            {"text": "Diyabetik hastalarda E. coli en sık etkenler arasında yer alır.", "isLie": False, "explanation": "Doğru. Liderliğini sürdürür."},
            {"text": "Klebsiella ve Proteus diyabetik hastalarda daha sık izole edilir.", "isLie": False, "explanation": "Doğru. Komplike etkenlerdir."},
            {"text": "Diyabetik hastalarda idrarda şeker olması bakterilerin ve mantarların yaşamını tamamen sonlandırır.", "isLie": True, "explanation": "Tuzak! Glukozüri bakteriler ve Candida için zengin bir besiyeridir, üremeyi hızlandırır."},
            {"text": "Diyabetli hastalarda Candida türlerine bağlı enfeksiyonlar görülebilir.", "isLie": False, "explanation": "Doğru. Fırsatçı mantar riskidir."}
        ]),
        make_quiz("Diyabetik hastalarda üriner sistem enfeksiyonu etiyolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "E. coli en sık etken olmayı sürdürür; ayrıca Klebsiella, Proteus, Pseudomonas ve Candida sıklığı artmıştır", "isCorrect": True, "explanation": "Ders notunda E. coli'nin diyabette de en sık olduğu ve bu diğer etkenlerin diyabetiklerde sık görüldüğü belirtilmiştir."},
            {"key": "B", "text": "Diyabetlilerde hiçbir zaman bakteri üremez, sadece virüsler ürer", "isCorrect": False, "explanation": "Bakteriyel enfeksiyonlar çok sıktır."},
            {"key": "C", "text": "En sık etken Salmonella typhi'dir", "isCorrect": False, "explanation": "Salmonella nadirdir."},
            {"key": "D", "text": "Diyabetik hastalarda antibiyotik kullanılması yasaktır", "isCorrect": False, "explanation": "Uygun antibiyotik mutlaka verilir."}
        ])
    ]
    slides.append(make_slide(36, "Diyabetik Hastalarda Etiyolojik Profil", "Diyabette E. coli liderliği, komplike bakteriler ve Candida sıklığı", "Etiyoloji", s36_narrative, s36_bullets, s36_elements))

    # Slide 37: Proteus Türleri ve Üreaz Bağıntısı
    s37_narrative = (
        "Enterobacteriaceae ailesinin hareketli üyesi olan Proteus türleri (özellikle Proteus mirabilis), "
        "üriner sistemde taş oluşumu ile doğrudan nedensel ilişkiye sahiptir.\n\n"
        "- **Üreaz Aktivitesi:** Proteus türleri güçlü bir **üreaz enzimi** üretirler.\n"
        "- **Alkalileşme ve Presipitasyon:** Üreaz enzimi idrardaki üreyi amonyak ve karbondioksite "
        "parçalayarak idrar pH'sını aşırı alkali düzeye (>8.0) yükseltir.\n"
        "- **Struvit Taşları:** Bu yüksek alkali ortamda magnezyum amonyum fosfat (struvit) ve apatit "
        "kristalleri çöker ve boynuz şeklinde dev kalsiyum enfeksiyon taşları (geyik boynuzu / staghorn taşlar) oluşur.\n\n"
        "> [!IMPORTANT]\n"
        "> Proteus türleri üreaz enzimi ile üreyi parçalayarak idrarı alkalileştirir ve enfeksiyon taşlarının (struvit) oluşumuna yol açar."
    )
    s37_bullets = [
        "Proteus türleri güçlü üreaz enzimi üretir.",
        "Üreyi amonyağa yıkarak idrar pH'sını alkali hale getirir.",
        "Alkali idrarda magnezyum amonyum fosfat (struvit) enfeksiyon taşları çöker."
    ]
    s37_elements = [
        make_cloze("Proteus türlerinin ürettiği üreaz enzimi idrarı alkalileştirerek struvit taşlarının oluşumuna yol açar.", "üreaz", "Üreyi amonyağa parçalayan bakteriyel enzim"),
        make_table("Proteus ve Taş Oluşum Patolojisi", ["Basamak", "Biyokimyasal Reaksiyon", "Klinik Patoloji"], [
            {"cells": [{"text": "Enzim Salınımı", "isMasked": False}, {"text": "Üreaz üretimi", "isMasked": True, "hint": "bakterinin salgıladığı enzim"}, {"text": "Ürenin amonyak ve CO2'ye hidrolizi"}]},
            {"cells": [{"text": "pH Değişimi", "isMasked": False}, {"text": "İdrar pH'sının belirgin yükselmesi (>8)", "isMasked": False}, {"text": "Alkali idrar ortamı", "isMasked": True, "hint": "asitliğin kaybolması"}]},
            {"cells": [{"text": "Kristal Çökmesi", "isMasked": False}, {"text": "Magnezyum amonyum fosfat presipitasyonu", "isMasked": True, "hint": "struvit kristal çöküntüsü"}, {"text": "Struvit / geyik boynuzu taş oluşumu"}]}
        ]),
        make_chain("Proteus Taş Oluşum Zinciri", [
            "1. Kolonizasyon: Proteus'un üriner sisteme asendan girişi.",
            "2. Üreaz Salınımı: Enzimin üreyi amonyağa dönüştürmesi.",
            "3. Alkali pH: Amonyak nedeniyle idrar pH'sının 8'in üzerine çıkması.",
            "4. Taş Presipitasyonu: Struvit kristallerinin birleşerek taş yapması."
        ]),
        make_recall("Proteus türlerinin idrarda taş oluşumuna yol açmasını sağlayan temel enzimatik mekanizma nedir?", "Üreaz enzimi salgılayarak üreyi amonyağa parçalaması ve idrarı alkalileştirerek struvit taşlarını çökeltmesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Proteus ve Üreaz", [
            {"text": "Proteus türleri üreaz enzimi üretebilir.", "isLie": False, "explanation": "Doğru. Tipik mikrobiyolojik özelliğidir."},
            {"text": "Üreaz enzimi idrar pH'sını alkalileştirir.", "isLie": False, "explanation": "Doğru. Amonyak açığa çıkar."},
            {"text": "Proteus idrarı öyle bir asitleştirir ki tüm böbrekler eriyip sıvılaşır.", "isLie": True, "explanation": "Tuzak! Proteus üreaz ile idrarı asitleştirmez, tam tersine alkalileştirir ve taş oluşturur."},
            {"text": "Alkali idrarda magnezyum amonyum fosfat (struvit) taşları gelişir.", "isLie": False, "explanation": "Doğru. Enfeksiyon taşıdır."}
        ]),
        make_quiz("İdrarda üreaz enzimi salgılayarak idrarı alkalileştiren ve enfeksiyon taşlarına (struvit) yol açan klasik bakteri aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Proteus mirabilis", "isCorrect": True, "explanation": "Proteus türleri üreaz enzimi üreterek idrarı alkalileştiren ve taş oluşturan klasik etkendir."},
            {"key": "B", "text": "Streptococcus pneumoniae", "isCorrect": False, "explanation": "Pnömokok solunum patojenidir."},
            {"key": "C", "text": "Treponema pallidum", "isCorrect": False, "explanation": "Sifiliz spiroketidir."},
            {"key": "D", "text": "Neisseria meningitidis", "isCorrect": False, "explanation": "Menenjit etkenidir."}
        ])
    ]
    slides.append(make_slide(37, "Proteus Türleri: Üreaz Aktivitesi ve Taş Oluşumu", "Proteus'un üreaz salgısı, idrar alkalinizasyonu ve struvit taşları ilişkisi", "Etiyoloji", s37_narrative, s37_bullets, s37_elements))

    # Slide 38: Pseudomonas aeruginosa: Dirençli Hastane Patojeni
    s38_narrative = (
        "Pseudomonas aeruginosa, özellikle hastanede yatan, enstrümantasyon uygulanan ve yoğun "
        "antibiyotik geçmişi bulunan hastalarda üriner traktusu enfekte eden en agresif patojenlerdendir.\n\n"
        "- **Nozokomiyal Karakter:** Sağlık bakımı ilişkili, kateterli ve komplike ÜSE olgularında "
        "izole edilen **Pseudomonas spp.**, doğal olarak birçok antibiyotiğe dirençlidir.\n"
        "- **Biyofilm Yeteneği:** Kateter ve ürolojik stent yüzeylerinde yoğun alginat biyofilmi oluşturarak "
        "hem konak fagositozundan hem de antibiyotik penetrasyonundan korunur.\n"
        "- **Klinik Tehdit:** Pseudomonas enfeksiyonları ürosepsise ilerleme eğilimindedir ve ampirik "
        "tedavide antipseudomonal ajanların (meropenem, piperasilin-tazobaktam vb.) seçilmesini gerektirir.\n\n"
        "> [!NOTE]\n"
        "> Pseudomonas aeruginosa, sağlık bakımı ilişkili ve kateterli hastalarda biyofilm oluşturan ve antipseudomonal tedavi gerektiren önemli bir patojendir."
    )
    s38_bullets = [
        "Pseudomonas spp.: Sağlık bakımı ilişkili ve komplike ÜSE etkenidir.",
        "Kateter ve yabancı cisimler üzerinde güçlü biyofilm oluşturur.",
        "İntrensek dirençleri nedeniyle antipseudomonal özel rejimler gerektirir."
    ]
    s38_elements = [
        make_cloze("Sağlık bakımı ilişkili ve kateterli hastalarda izole edilen Pseudomonas türleri antipseudomonal antibiyotik tedavisi gerektirir.", "Pseudomonas", "Kateter biyofilmi oluşturan dirençli Gram negatif non-fermentatif basil"),
        make_table("Pseudomonas Klinik Özellikleri", ["Klinik Özellik", "Tanımlayıcı Bilgi", "Tedavi Yaklaşımı"], [
            {"cells": [{"text": "Patojen Türü", "isMasked": False}, {"text": "Non-fermentatif Gram negatif basil", "isMasked": True, "hint": "oksidaz pozitif çomak"}, {"text": "Nozokomiyal ortama yüksek uyum"}]},
            {"cells": [{"text": "Direnç Profili", "isMasked": False}, {"text": "Geniş intrensek antibiyotik direnci", "isMasked": False}, {"text": "Antipseudomonal karbapenem / penisilin", "isMasked": True, "hint": "spesifik pseudomonas ilaçları"}]}
        ]),
        make_chain("Pseudomonas Nozokomiyal Enfeksiyonu", [
            "1. Hastanede Yatış: Yoğun antibiyotik kullanımı ve kateterizasyon.",
            "2. Katetere Tutunma: Alginat salgısıyla biyofilm üretimi.",
            "3. Biyofilmde Çoğalma: Antibiyotiklerin içeri sızamaması.",
            "4. Sistemik Yayılım: Ürosepsis tablosu gelişimi."
        ]),
        make_recall("Pseudomonas türlerinin üriner sistemde enfeksiyon oluşturduğu tipik hasta grubu nedir?", "Sağlık bakımı ilişkili, kateterize edilmiş ve komplike ÜSE'si olan hastalardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Pseudomonas", [
            {"text": "Pseudomonas sağlık bakımı ilişkili ve komplike ÜSE etkenlerindendir.", "isLie": False, "explanation": "Doğru. Ders notu sınıflamasıdır."},
            {"text": "Pseudomonas kateterlerde biyofilm oluşturabilir.", "isLie": False, "explanation": "Doğru. Biyofilm ustasıdır."},
            {"text": "Pseudomonas tek bir doz bebek pudrası sürülerek tamamen yok edilir.", "isLie": True, "explanation": "Tuzak! Pseudomonas çok dirençli bir hastane patojenidir, antipseudomonal parenteral antibiyotikler gerektirir."},
            {"text": "Pseudomonas enfeksiyonları ürosepsise yol açabilir.", "isLie": False, "explanation": "Doğru. Ağır klinik tablodur."}
        ]),
        make_quiz("Hastanede yatan, kateterli ve komplike ÜSE olgularında sık izole edilen ve antipseudomonal tedavi gerektiren patojen aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Pseudomonas aeruginosa", "isCorrect": True, "explanation": "Ders notunda sağlık bakımı ilişkili ve komplike ÜSE etkenleri arasında Pseudomonas açıkça sayılmıştır."},
            {"key": "B", "text": "Corynebacterium diphtheriae", "isCorrect": False, "explanation": "Difteri etkenidir, ÜSE yapmaz."},
            {"key": "C", "text": "Helicobacter pylori", "isCorrect": False, "explanation": "Mide ülseri etkenidir."},
            {"key": "D", "text": "Bacillus cereus", "isCorrect": False, "explanation": "Gıda zehirlenmesi etkenidir."}
        ])
    ]
    slides.append(make_slide(38, "Sağlık Bakımı İlişkili Patojen: Pseudomonas aeruginosa", "Pseudomonas'ın nozokomiyal karakteri, biyofilm üretimi ve direnç dinamikleri", "Etiyoloji", s38_narrative, s38_bullets, s38_elements))

    # Slide 39: Dördüncü Bölüm Özeti: Patojen Yelpazesi
    s39_narrative = (
        "Üriner sistem enfeksiyonlarında izole edilen etkenler hasta profiline göre net "
        "kategorilere ayrılarak akılcı ampirik tedavinin temelini oluşturur.\n\n"
        "- **En Sık Etken:** **E. coli**, toplum kökenli, sağlık bakımı ilişkili, diyabetik ve tüm yaş "
        "gruplarında açık ara en sık izole edilen bakteridir.\n"
        "- **Genç Kadın:** Genç-orta yaş kadınlarda akut sistitin karakteristik Gram pozitif etkeni "
        "**Staphylococcus saprophyticus**tur.\n"
        "- **Komplike ve Mantar:** Klebsiella, Proteus, Pseudomonas, Enterococcus ve Enterobacter "
        "sağlık bakımı ilişkili/komplike ÜSE'de; **Candida spp.** ise kateter ve antibiyotik kullananlarda öne çıkar.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] E. coli her grupta en sıktır; S. saprophyticus genç kadında sistit yapar; Klebsiella/Proteus/Pseudomonas komplike/hastane olgularında, Candida ise kateter ve antibiyotik zemininde belirir."
    )
    s39_bullets = [
        "E. coli: Tüm gruplarda en sık etkendir (toplum, hastane, diyabet, tüm yaşlar).",
        "S. saprophyticus: Genç-orta yaş kadınlarda akut sistit etkenidir.",
        "Klebsiella, Proteus, Pseudomonas: Sağlık bakımı ilişkili ve komplike ÜSE.",
        "Candida spp.: Üriner kateterizasyon ve antibiyotik kullanımı ile ilişkilidir."
    ]
    s39_elements = [
        make_cloze("Genç-orta yaş kadınlarda akut sistitin en önemli stafilokok etkeni Staphylococcus saprophyticus iken tüm gruplarda lider etken E. coli'dir.", "Staphylococcus saprophyticus", "Genç kadın akut sistitinde ikinci sık etken"),
        make_table("Etiyolojik Dağılım Büyük Özeti", ["Patojen", "En Sık Görüldüğü Popülasyon", "Klinik Özellik"], [
            {"cells": [{"text": "E. coli", "isMasked": False}, {"text": "Tüm gruplar ve yaşlar", "isMasked": True, "hint": "evrensel lider"}, {"text": "Açık ara en sık etken"}]},
            {"cells": [{"text": "S. saprophyticus", "isMasked": False}, {"text": "Genç-orta yaş kadınlar", "isMasked": False}, {"text": "Akut sistit tablosu", "isMasked": True, "hint": "cinsel aktif kadında sistit"}]},
            {"cells": [{"text": "Klebsiella, Proteus, Pseudomonas", "isMasked": False}, {"text": "Komplike ve sağlık bakımı ilişkili", "isMasked": True, "hint": "hastane ve komorbid grup"}, {"text": "Çoklu direnç ve taş oluşumu"}]},
            {"cells": [{"text": "Candida spp.", "isMasked": False}, {"text": "Kateter ve antibiyotik alanlar", "isMasked": False}, {"text": "Fırsatçı kandidüri", "isMasked": True, "hint": "mantar kolonizasyonu"}]}
        ]),
        make_chain("Etiyolojik Karar Ağacı", [
            "1. Sağlıklı Genç Kadın Sistiti: E. coli veya S. saprophyticus düşün.",
            "2. Komplike / Diyabetik Hasta: E. coli, Klebsiella, Proteus araştır.",
            "3. Sağlık Bakımı İlişkili / Kateter: Pseudomonas ve dirençli etkenler.",
            "4. Kateter + Uzun Antibiyotik: Candida türleri için tetkik et."
        ]),
        make_recall("Dördüncü bölümün temel kazanımı olarak E. coli, S. saprophyticus ve Candida'nın tipik hasta profilleri nedir?", "E. coli tüm gruplarda en sık; S. saprophyticus genç-orta yaş kadınlarda akut sistit; Candida ise kateter ve antibiyotik kullananlardadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Etiyoloji Özeti", [
            {"text": "E. coli tüm yaş gruplarında ve diyabetiklerde en sık etkendir.", "isLie": False, "explanation": "Doğru. Genel liderdir."},
            {"text": "S. saprophyticus genç-orta yaş kadınlarda sistit yapar.", "isLie": False, "explanation": "Doğru. Tipik popülasyondur."},
            {"text": "Candida türleri yalnızca anne sütüyle beslenen 1 günlük sağlıklı bebeklerde görülür.", "isLie": True, "explanation": "Tuzak! Candida üriner kateterizasyon ve geniş antibiyotik kullanımı olan hastalarda ortaya çıkar."},
            {"text": "Klebsiella ve Proteus komplike ÜSE'de sık izole edilir.", "isLie": False, "explanation": "Doğru. Nozokomiyal/komplike etkenlerdir."}
        ]),
        make_quiz("Dördüncü bölümdeki etiyolojik sınıflama değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Candida spp. yalnızca sağlıklı genç kadınların balayı sistitinde görülür", "isCorrect": True, "explanation": "Yanlış! Balayı sistitinde E. coli ve S. saprophyticus görülür; Candida ise üriner kateterizasyon ve antibiyotik kullanımında ortaya çıkar."},
            {"key": "B", "text": "E. coli toplum kökenli ve sağlık bakımı ilişkili tüm gruplarda en sık etkendir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Staphylococcus saprophyticus genç-orta yaş kadınlarda akut sistit etkenidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Pseudomonas ve Proteus komplike ÜSE ve diyabetiklerde sık izole edilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(39, "Dördüncü Bölüm Özeti: Patojen Yelpazesi", "E. coli, S. saprophyticus, komplike bakteriler ve Candida profillerinin özeti", "Bölüm Özeti", s39_narrative, s39_bullets, s39_elements))

    # Slide 40: [TEKRAR SAYFASI - CHECKPOINT 4] Etiyolojik Ajanlar
    s40_narrative = (
        "Bu tekrar sayfasında 4. Bölümde işlenen tüm etiyolojik mikroorganizmaları, hedef hasta gruplarını "
        "ve patolojik özelliklerini kapsamlı olarak pekiştiriyoruz.\n\n"
        "- **Genel Lider:** **E. coli en sık etkendir**; toplum kökenli, sağlık bakımı ilişkili, diyabetik "
        "hastalar ve tüm yaş gruplarında ilk sıradadır.\n"
        "- **Genç Kadın Sistiti:** **Staphylococcus saprophyticus**, genç-orta yaş kadınlarda akut sistitin "
        "karakteristik koagülaz-negatif stafilokok etkenidir.\n"
        "- **Komplike ve Mantar Etkenleri:** **Klebsiella, Proteus, Pseudomonas, Enterococcus, Enterobacter** "
        "komplike/sağlık bakımı ilişkili olgularda; **Candida spp.** ise kateter ve antibiyotik zemininde gelişir.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 4] E. coli tüm gruplarda en sık etkendir; S. saprophyticus genç kadın akut sistitinde, Klebsiella/Proteus/Pseudomonas komplike/sağlık bakımı olgularında, Candida ise kateter ve antibiyotik kullanımında görülür."
    )
    s40_bullets = [
        "E. coli: En sık etken (toplum, sağlık bakımı, diyabet, tüm yaş grupları).",
        "S. saprophyticus: Genç-orta yaş kadınlarda akut sistit etkenidir.",
        "Klebsiella, Proteus, Pseudomonas, Enterococcus, Enterobacter: Sağlık bakımı, komplike, diyabet.",
        "Candida spp.: Üriner kateterizasyon ve antibiyotik kullanımı ile ilişkilidir."
    ]
    s40_elements = [
        make_cloze("Tüm yaş gruplarında ve diyabetiklerde ÜSE'nin en sık etkeni E. coli iken genç kadınlarda S. saprophyticus akut sistit yapar.", "E. coli", "ÜSE'de mutlak lider üropatojen bakteri"),
        make_table("4. Bölüm Büyük Tekrar Tablosu", ["Mikroorganizma", "Temel Hasta Grubu", "Spesifik Klinik Özellik"], [
            {"cells": [{"text": "E. coli", "isMasked": False}, {"text": "Tüm gruplar (toplum, hastane, diyabet)", "isMasked": True, "hint": "evrensel en sık etken"}, {"text": "Açık ara en sık görülen etken"}]},
            {"cells": [{"text": "S. saprophyticus", "isMasked": False}, {"text": "Genç-orta yaş kadınlar", "isMasked": False}, {"text": "Akut sistit (novobiosine dirençli)", "isMasked": True, "hint": "genç kadın sistiti"}]},
            {"cells": [{"text": "Proteus spp.", "isMasked": False}, {"text": "Komplike ve taş hastaları", "isMasked": True, "hint": "taş yapan mikrop"}, {"text": "Üreaz üretimi ve struvit taşları"}]},
            {"cells": [{"text": "Candida spp.", "isMasked": False}, {"text": "Kateter ve antibiyotik alanlar", "isMasked": False}, {"text": "Fırsatçı kandidüri", "isMasked": True, "hint": "iyatrojenik mantar üremesi"}]}
        ]),
        make_chain("Bölüm 4 Patojen Sınıflama Özeti", [
            "1. Evrensel Etken: E. coli (toplum, hastane, diyabet, her yaş).",
            "2. Genç Kadın Etkeni: S. saprophyticus (akut sistit).",
            "3. Nozokomiyal/Komplike: Klebsiella, Proteus, Pseudomonas, Enterobacter.",
            "4. İyatrojenik Fırsatçı: Candida spp. (kateter + antibiyotik)."
        ]),
        make_recall("Checkpoint 4: E. coli'nin görüldüğü gruplar nelerdir ve Candida hangi iki klinik faktör varlığında ortaya çıkar?", "E. coli toplum kökenli, sağlık bakımı ilişkili, diyabetik hastalar ve tüm yaş gruplarında görülür; Candida ise üriner kateterizasyon ve antibiyotik kullanımı durumunda ortaya çıkar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 4 Konsolidasyonu", [
            {"text": "E. coli tüm yaş gruplarında ve diyabetiklerde en sık etkendir.", "isLie": False, "explanation": "Doğru. 4. bölümün ana kuralıdır."},
            {"text": "S. saprophyticus genç-orta yaş kadınlarda akut sistite yol açar.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Pseudomonas ve Klebsiella sadece yenidoğan bebeklerin göbek kordonunda ürer.", "isLie": True, "explanation": "Tuzak! Klebsiella ve Pseudomonas sağlık bakımı ilişkili ve komplike ÜSE'de sık görülen patojenlerdir."},
            {"text": "Candida türleri üriner kateterizasyon ve antibiyotik kullanımı ile ilişkilidir.", "isLie": False, "explanation": "Doğru. İyatrojenik tetikleyicilerdir."}
        ]),
        make_quiz("4. Bölümün tamamı (Etiyolojik Ajanlar) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "E. coli yalnızca sağlıklı genç erkeklerde görülür, diyabetiklerde ve yaşlılarda asla izole edilemez", "isCorrect": True, "explanation": "Yanlış! E. coli toplum kökenli, sağlık bakımı ilişkili, diyabetik hastalar ve tüm yaş gruplarında en sık etkendir."},
            {"key": "B", "text": "Staphylococcus saprophyticus genç-orta yaş kadınlarda akut sistit etkenidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Proteus türleri üreaz enzimi ile idrarı alkalileştirerek taş oluşumuna yol açar", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Candida spp. üriner kateterizasyon ve antibiyotik kullanımı zemininde ortaya çıkar", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(40, "[TEKRAR SAYFASI - CHECKPOINT 4] Etiyolojik Ajanlar", "4. Bölümün kapsamlı pekiştirmesi: E. coli, S. saprophyticus, komplike patojenler ve Candida", "Bölüm Tekrarı", s40_narrative, s40_bullets, s40_elements))

    return slides
