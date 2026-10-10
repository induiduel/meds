# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec1():
    slides = []

    # Slide 1: Üriner Sistem Enfeksiyonu (ÜSE) Temel Tanımı
    s1_narrative = (
        "Üriner sistem enfeksiyonu (ÜSE), insan vücudunda en sık karşılaşılan bakteriyel enfeksiyon "
        "tablolarından biri olup geniş bir klinik alanı kapsar.\n\n"
        "- **Anatomik Tanım:** Üriner sistem enfeksiyonu, üriner sistemin üretradan böbreğe kadar "
        "herhangi bir dokusunun enfeksiyonudur.\n"
        "- **Doku Tutulumu:** Enfeksiyon alt üriner traktusta üretra veya mesaneyle sınırlı kalabileceği "
        "gibi, üst üriner traktusta üreter ve böbrek parankimini de tutabilir.\n"
        "- **Hastalık Skalası:** Biyolojik süreç asemptomatik bakteriüriden sepsisle seyreden akut "
        "piyelonefrite kadar çok geniş bir klinik skala gösterir.\n\n"
        "> [!NOTE]\n"
        "> ÜSE tek bir homojen hastalık tablosu olmayıp, üretradan böbrek parankimine kadar tüm üriner dokuları kapsayan bir enfeksiyon spektrumudur."
    )
    s1_bullets = [
        "ÜSE, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur.",
        "Alt veya üst üriner traktus dokuları tek başına ya da birlikte etkilenebilir.",
        "Asemptomatik bakteriüriden sepsise kadar geniş bir klinik skala sergiler."
    ]
    s1_elements = [
        make_cloze("Üriner sistem enfeksiyonu, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur.", "üretradan böbreğe kadar", "Üriner traktusun en distalinden en proksimaline uzanan anatomik sınır"),
        make_table("Üriner Sistem Enfeksiyonunun Temel Anatomik Tanımı", ["Anatomik Segment", "Tutulan Dokular", "Temel Tanısal Kavram"], [
            {"cells": [{"text": "Alt Üriner Traktus", "isMasked": False}, {"text": "Üretra ve mesane dokusu", "isMasked": True, "hint": "distal üriner kanallar"}, {"text": "Lokalize üriner enfeksiyon"}]},
            {"cells": [{"text": "Üst Üriner Traktus", "isMasked": False}, {"text": "Üreter ve böbrek parankimi", "isMasked": False}, {"text": "Sistemik tutulum potansiyeli", "isMasked": True, "hint": "parankimal organ yayılımı"}]}
        ]),
        make_chain("ÜSE Anatomik Tutulum Sırası", [
            "1. Üretra Tutulumu: Distal orifisten başlayan üretrit tablosu.",
            "2. Mesane İnvazyonu: Ürotelyum kolonizasyonu ve sistit gelişimi.",
            "3. Üreter Geçişi: Üreteral lümenden asendan ilerleyiş.",
            "4. Böbrek Parankimi: Renal pelvise ve böbreğe invazyon."
        ]),
        make_recall("Üriner sistem enfeksiyonunun (ÜSE) ders notundaki resmi anatomik tanımı nedir?", "Üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ÜSE Temel Tanımı", [
            {"text": "ÜSE, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur.", "isLie": False, "explanation": "Doğru. Ders notundaki resmi tanımdır."},
            {"text": "Enfeksiyon asemptomatik bakteriüriden ağır sepsise kadar geniş bir skalada seyreder.", "isLie": False, "explanation": "Doğru. Klinik şiddeti çok değişkendir."},
            {"text": "ÜSE tanısı koyabilmek için enfeksiyonun mutlaka yalnız böbrek parankimiyle sınırlı olması şarttır.", "isLie": True, "explanation": "Tuzak! ÜSE üretradan böbreğe kadar herhangi bir üriner dokunun enfeksiyonudur, yalnızca böbrekle sınırlı değildir."},
            {"text": "Alt ve üst üriner traktus dokuları bu enfeksiyon sürecine dahil olabilir.", "isLie": False, "explanation": "Doğru. Spektrum tüm üriner anatomiyi içerir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonunun (ÜSE) genel klinik ve anatomik tanımıyla ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur", "isCorrect": True, "explanation": "Ders notunda verilen net ve eksiksiz tanımdır."},
            {"key": "B", "text": "Yalnızca glomerül yumağının otoimmün enflamasyonunu tanımlayan bir tablodur", "isCorrect": False, "explanation": "Bu glomerülonefrittir, enfeksiyon tanımı değildir."},
            {"key": "C", "text": "Sadece mesane kanserli hastalarda görülen cerrahi bir komplikasyondur", "isCorrect": False, "explanation": "Tüm toplumu ilgilendiren yaygın bir enfeksiyon spektrumudur."},
            {"key": "D", "text": "Üriner sistemde enfeksiyon gelişebilmesi için mutlaka taş varlığı zorunludur", "isCorrect": False, "explanation": "Taş olmaksızın da enfeksiyon gelişebilir."}
        ])
    ]
    slides.append(make_slide(1, "Üriner Sistem Enfeksiyonu: Tanım ve Kapsam", "ÜSE'nin anatomik doku sınırları ve temel klinik spektrumu", "Genel Tanımlar", s1_narrative, s1_bullets, s1_elements))

    # Slide 2: ÜSE'nin Geniş Klinik Spektrumu
    s2_narrative = (
        "Üriner sistem enfeksiyonları, klinik tablonun ağırlığı bakımından tekdüze bir seyir göstermez; "
        "hastalar çok farklı klinik tablolarla hekime başvurabilirler.\n\n"
        "- **Sessiz Enfeksiyon:** Spektrumun en hafif ucunda hiçbir semptomu olmayan asemptomatik "
        "bakteriüri (ABU) olguları yer alır.\n"
        "- **Lokal Semptomatik Tablo:** Mesane ve üretra tutulumu dizüri, pollaküri ve sıkışma hissi ile "
        "karakterize lokal akut sistit tablosunu oluşturur.\n"
        "- **Ağır Sistemik Yayılım:** Spektrumun en ağır ucunda ise yüksek ateş, kostavertebral açı "
        "hassasiyeti, sepsisle seyreden akut piyelonefrit ve septik şok yer alır.\n\n"
        "> [!IMPORTANT]\n"
        "> ÜSE spektrumu asemptomatik bakteriüriden sepsisle seyreden akut piyelonefrite kadar uzanır; her basamak farklı tanı ve tedavi yaklaşımı gerektirir."
    )
    s2_bullets = [
        "Klinik tablo asemptomatik bakteriüriden sepsise kadar geniş bir skala gösterir.",
        "Lokalize formlar mesane mukozası ile sınırlıyken, sistemik formlar böbreği tutar.",
        "Sepsisle seyreden akut piyelonefrit spektrumun en ağır tablosudur."
    ]
    s2_elements = [
        make_cloze("Üriner sistem enfeksiyonu, asemptomatik bakteriüriden sepsisle seyreden akut piyelonefrite kadar geniş bir klinik skala gösterir.", "akut piyelonefrite", "Sepsisle seyreden üst üriner traktus parankimal enfeksiyonu"),
        make_table("ÜSE Klinik Skalasının Uç Noktaları", ["Klinik Form", "Semptom Varlığı", "Organ Düzeyindeki Şiddet"], [
            {"cells": [{"text": "Asemptomatik Bakteriüri", "isMasked": False}, {"text": "Üriner semptom bulunmaz", "isMasked": True, "hint": "şikayetsiz seyir"}, {"text": "Lokal kolonizasyon"}]},
            {"cells": [{"text": "Akut Piyelonefrit ve Sepsis", "isMasked": False}, {"text": "Sistemik ateş ve toksisite", "isMasked": False}, {"text": "Hayati organ disfonksiyon riski", "isMasked": True, "hint": "sistemik yetmezlik tablosu"}]}
        ]),
        make_chain("Klinik Spektrumun Derecelendirilmesi", [
            "1. Asemptomatik Bakteriüri: Klinik şikayet olmaksızın üreme.",
            "2. Akut Sistit: Lokal alt üriner sistem semptomları.",
            "3. Komplike Piyelonefrit: Böbrek parankim tutulumu ve ateş.",
            "4. Ürosepsis: Sistemik enflamasyon ve organ yetmezliği."
        ]),
        make_recall("ÜSE spektrumunun en hafif ve en ağır uçlarını hangi klinik tablolar temsil eder?", "En hafif ucunu asemptomatik bakteriüri, en ağır ucunu ise sepsisle seyreden akut piyelonefrit temsil eder."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Klinik Spektrum", [
            {"text": "Üriner sistem enfeksiyonları asemptomatik bakteriüriden sepsise kadar geniş bir skala gösterir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Asemptomatik bakteriüride hastada klasik idrar yolu semptomları bulunmaz.", "isLie": False, "explanation": "Doğru. Klinik olarak sessiz seyreder."},
            {"text": "Tüm ÜSE vakaları istisnasız olarak ilk günden itibaren septik şokla başlar.", "isLie": True, "explanation": "Tuzak! Vakaların çoğu lokalize ve hafif seyreder, septik şok spektrumun en ağır ucudur."},
            {"text": "Akut piyelonefrit sistemik belirtiler ve sepsisle seyredebilir.", "isLie": False, "explanation": "Doğru. Böbrek parankim tutulumu sistemik yanıt doğurur."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarının klinik spektrumu değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Hastalık her zaman asemptomatik seyreder ve asla sistemik sepsise ilerlemez", "isCorrect": True, "explanation": "Yanlış! ÜSE sepsisle seyreden akut piyelonefrite kadar ilerleyebilen geniş bir spektruma sahiptir."},
            {"key": "B", "text": "Spektrumun bir ucunda asemptomatik bakteriüri yer alır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Akut sistit lokalize alt üriner traktus enfeksiyonudur", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Akut piyelonefrit spektrumun ağır formları arasında yer alır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(2, "Klinik Spektrum: Asemptomatik Bakteriüriden Sepsise", "ÜSE'nin sessiz tablodan ağır hayatı tehdit eden sepsise uzanan yelpazesi", "Klinik Spektrum", s2_narrative, s2_bullets, s2_elements))

    # Slide 3: Epidemiyolojik Önemi ve Global Vaka Yükü
    s3_narrative = (
        "Üriner sistem enfeksiyonları gerek ülkemizde gerekse dünya genelinde birinci basamak ve "
        "hastane başvurularının en yaygın nedenleri arasında yer almaktadır.\n\n"
        "- **Türkiye'deki Durum:** İdrar yolu enfeksiyonu ülkemizde en sık görülen enfeksiyonlardan "
        "biridir ve poliklinik başvurularında ön sıralardadır.\n"
        "- **Global ve ABD Verileri:** Amerika Birleşik Devletleri'nde ÜSE nedeniyle yıllık vaka "
        "sayısı **yedi milyondan fazladır**.\n"
        "- **Sağlık Sistemi Yükü:** Bu muazzam vaka yükü, yüksek oranda iş gücü kaybına, yoğun "
        "antibiyotik tüketimine ve acil servis yoğunluğuna yol açmaktadır.\n\n"
        "> [!NOTE]\n"
        "> İdrar yolu enfeksiyonu ülkemizde en sık görülen enfeksiyonlar arasındadır; ABD'de yılda 7 milyondan fazla olgu kaydedilmektedir."
    )
    s3_bullets = [
        "İdrar yolu enfeksiyonu ülkemizde en sık görülen enfeksiyonlardan biridir.",
        "Amerika Birleşik Devletleri'nde yıllık vaka sayısı yedi milyondan fazladır.",
        "Poliklinik ve acil servis başvurularında önemli bir sağlık sistemi yükü oluşturur."
    ]
    s3_elements = [
        make_cloze("Amerika Birleşik Devletleri'nde idrar yolu enfeksiyonu nedeniyle yıllık vaka sayısı yedi milyondan fazladır.", "yedi milyondan fazladır", "Yedi milyonu aşan vaka sayısı"),
        make_table("ÜSE Epidemiyolojik Yükü", ["Bölge / Ülke", "Görülme Profili", "Sağlık Sistemine Etkisi"], [
            {"cells": [{"text": "Türkiye", "isMasked": False}, {"text": "En sık görülen enfeksiyonlardan biri", "isMasked": True, "hint": "ülkemizdeki yaygınlık düzeyi"}, {"text": "Birinci basamak başvurularında lider"}]},
            {"cells": [{"text": "Amerika Birleşik Devletleri", "isMasked": False}, {"text": "Yıllık >7 milyon vaka", "isMasked": False}, {"text": "Yüksek tanı ve antibiyotik maliyeti", "isMasked": True, "hint": "ekonomik ve farmakolojik yük"}]}
        ]),
        make_recall("Amerika Birleşik Devletleri'nde ÜSE nedeniyle yıllık vaka sayısı yaklaşık ne kadardır?", "Yıllık yedi milyondan (7.000.000) fazladır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Epidemiyolojik Yük", [
            {"text": "İdrar yolu enfeksiyonu ülkemizde en sık görülen enfeksiyonlardan biridir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "ABD'de yıllık ÜSE vaka sayısı yedi milyondan fazladır.", "isLie": False, "explanation": "Doğru. Net epidemiyolojik istatistiktir."},
            {"text": "Üriner sistem enfeksiyonları yalnızca tropikal ülkelerde görülen çok nadir bir hastalıktır.", "isLie": True, "explanation": "Tuzak! ÜSE tüm dünyada ve ülkemizde en sık görülen enfeksiyonlardandır."},
            {"text": "Yüksek vaka sayısı acil servis ve poliklinik başvurularını artırır.", "isLie": False, "explanation": "Doğru. Önemli bir başvuru nedenidir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarının epidemiyolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "ABD'de yıllık vaka sayısı yedi milyondan fazladır ve ülkemizde en sık görülen enfeksiyonlardandır", "isCorrect": True, "explanation": "Ders notundaki iki temel epidemiyolojik saptamadır."},
            {"key": "B", "text": "Dünya genelinde yılda toplam sadece 500 vaka görülür", "isCorrect": False, "explanation": "Milyonlarca vaka görülmektedir."},
            {"key": "C", "text": "Yalnızca yoğun bakım ünitelerinde yatan hastalarda ortaya çıkar", "isCorrect": False, "explanation": "Toplumda çok yaygın bir enfeksiyondur."},
            {"key": "D", "text": "Ülkemizde görülme sıklığı sıfıra yakındır", "isCorrect": False, "explanation": "Ülkemizde en sık görülen enfeksiyonlardandır."}
        ])
    ]
    slides.append(make_slide(3, "Epidemiyoloji: Vaka Yükü ve Prevalans", "ÜSE'nin Türkiye ve dünyadaki sıklığı, yıllık vaka istatistikleri", "Epidemiyoloji", s3_narrative, s3_bullets, s3_elements))

    # Slide 4: Kadınlarda ÜSE Eğilimi ve Risk Faktörleri
    s4_narrative = (
        "Üriner sistem enfeksiyonları genel popülasyonda kadın cinsiyette erkeklere oranla çok daha "
        "yüksek bir sıklıkta gözlenmektedir.\n\n"
        "- **Cinsiyet Farkı:** Üriner sistem enfeksiyonu kadınlarda erkeklere kıyasla belirgin şekilde "
        "daha sık ortaya çıkmaktadır.\n"
        "- **Anatomik Temel:** Kadın üretrasının erkek üretrasına göre belirgin derecede kısa olması ve "
        "eksternal meatusun rektum ile vajinaya anatomik yakınlığı mikroorganizma geçişini kolaylaştırır.\n"
        "- **Kolonizasyon:** Rektal ve perineal florada bulunan enterik bakteriler kısa üretral mesafeyi "
        "kolayca aşarak mesaneye ulaşır.\n\n"
        "> [!NOTE]\n"
        "> Kadınlarda ÜSE sıklığının yüksek olmasının en temel belirleyicisi üretra boyunun kısalığı ve perineal floraya olan yakın anatomik komşuluktur."
    )
    s4_bullets = [
        "Üriner sistem enfeksiyonu kadınlarda erkeklere oranla çok daha sıktır.",
        "Kısa üretra boyu bakterilerin mesaneye erişimini kolaylaştırır.",
        "Üretral meatusun rektal ve vajinal floraya yakınlığı kolonizasyon riskini artırır."
    ]
    s4_elements = [
        make_cloze("Kadınlarda üriner sistem enfeksiyonunun erkeklere göre daha sık görülmesinin temel nedeni anatomik farklılık ve kısa üretra yapısıdır.", "kısa üretra", "Kadın anatomisindeki mesafe avantajını azaltan yapı"),
        make_table("Cinsiyete Göre Anatomik Savunma Karşılaştırması", ["Özellik", "Kadın Anatomisi", "Erkek Anatomisi"], [
            {"cells": [{"text": "Üretra Uzunluğu", "isMasked": False}, {"text": "Kısa (yaklaşık 4 cm)", "isMasked": True, "hint": "kadındaki santimetre mesafesi"}, {"text": "Uzun (yaklaşık 20 cm)"}]},
            {"cells": [{"text": "Rektal Floraya Yakınlık", "isMasked": False}, {"text": "Çok yakın perineal komşuluk", "isMasked": False}, {"text": "Belirgin anatomik uzaklık", "isMasked": True, "hint": "erkekteki perineal mesafe"}]}
        ]),
        make_chain("Kadında Bakteriyel Giriş Mekanizması", [
            "1. Enterik Kolonizasyon: Perineal ve periüretral alanda enterik bakteri birikimi.",
            "2. Kısa Üretral Yol: Bakterinin kısa üretral kanaldan retrograd hareketi.",
            "3. Mesane İntrakaviter Girişi: Asendan göçle lümene ulaşma.",
            "4. Ürotelyal Tutunma: Mesane yüzeyinde mukozal adezyon."
        ]),
        make_recall("Kadınlarda ÜSE sıklığının erkeklerden belirgin şekilde yüksek olmasını sağlayan temel anatomik faktör nedir?", "Kadın üretrasının erkek üretrasına kıyasla belirgin derecede kısa olması ve perineal floraya yakınlığıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kadınlarda ÜSE Eğilimi", [
            {"text": "Üriner sistem enfeksiyonu kadınlarda erkeklere kıyasla daha sıktır.", "isLie": False, "explanation": "Doğru. Belirgin kadın baskınlığı vardır."},
            {"text": "Kadın ve erkekteki anatomik farklılıklar sıklığı belirleyen temel unsurdur.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Kadın üretrası erkek üretrasından 5 kat daha uzundur ve bakterilerin geçişini tamamen engeller.", "isLie": True, "explanation": "Tuzak! Kadın üretrası çok daha kısadır (~4 cm vs ~20 cm), bu nedenle enfeksiyon daha sıktır."},
            {"text": "Üretral orifisin anüse yakınlığı asendan kolonizasyon riskini artırır.", "isLie": False, "explanation": "Doğru. Anatomik komşuluk risk faktörüdür."}
        ]),
        make_quiz("Kadınlarda ÜSE görülme sıklığının erkeklerden daha yüksek olmasının temel nedeni aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Kadın ve erkekteki anatomik farklılıklar ve kadın üretrasının kısa olması", "isCorrect": True, "explanation": "Ders notuna göre anatomik farklılık sıklığı belirleyen temel unsurdur."},
            {"key": "B", "text": "Kadınlarda idrarın pH değerinin sürekli aşırı alkali olması", "isCorrect": False, "explanation": "İdrar pH'sı cinsiyete bağlı olarak alkaliye sabitlenmez."},
            {"key": "C", "text": "Kadınlarda Tamm-Horsfall proteininin hiç üretilmemesi", "isCorrect": False, "explanation": "Tamm-Horsfall proteini her iki cinsiyette de tübüllerden üretilir."},
            {"key": "D", "text": "Kadınlarda glomerüler filtrasyon hızının her zaman sıfır olması", "isCorrect": False, "explanation": "Fizyolojik olarak anlamsız bir seçenektir."}
        ])
    ]
    slides.append(make_slide(4, "Kadınlarda ÜSE Eğilimi ve Anatomik Nedenler", "Kadınlarda yüksek ÜSE sıklığının anatomik ve fizyolojik gerekçeleri", "Epidemiyoloji", s4_narrative, s4_bullets, s4_elements))

    # Slide 5: Kadınlarda Yaş Dağılımı ve 18-24 Yaş Piki
    s5_narrative = (
        "Kadın popülasyonu içinde ÜSE insidansı yaş gruplarına göre belirgin farklılıklar göstermektedir "
        "ve belirli bir dönemde zirveye ulaşmaktadır.\n\n"
        "- **İnsidans Piki:** Kadınlarda üriner sistem enfeksiyonu **18-24 yaş arası cinsel aktif kadınlarda "
        "pik yapmaktadır**.\n"
        "- **Mekanik Kolonizasyon:** Cinsel aktivite sırasında oluşan mekanik travma ve masaj etkisi, "
        "periüretral bakterilerin üretra yoluyla mesaneye itilmesini kolaylaştırır.\n"
        "- **Hormonal Faktörler:** Bu yaş grubundaki reprodüktif dönem özellikleri ve bariyer yöntemler "
        "de üropatojen kolonizasyonunu destekleyebilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kadınlarda ÜSE insidansı 18-24 yaş arasındaki cinsel aktif dönemde pik yapmaktadır."
    )
    s5_bullets = [
        "Kadınlarda ÜSE insidansı 18-24 yaş grubunda pik yapar.",
        "Cinsel aktif dönemde mekanik etki ile bakterilerin mesaneye geçişi kolaylaşır.",
        "Bu pik reprodüktif çağın erken evresindeki en belirgin epidemiyolojik özelliktir."
    ]
    s5_elements = [
        make_cloze("Kadınlarda üriner sistem enfeksiyonu 18-24 yaş arası cinsel aktif kadınlarda pik yapmaktadır.", "18-24 yaş arası", "İnsidansın zirve yaptığı genç erişkin yaş aralığı"),
        make_table("Kadınlarda Yaş ve ÜSE Zirve Noktası", ["Yaş Grubu", "İnsidans Özelliği", "Tetikleyici Dinamik"], [
            {"cells": [{"text": "18-24 Yaş", "isMasked": False}, {"text": "İnsidansın pik yaptığı dönem", "isMasked": True, "hint": "zirve yaptığı aralık"}, {"text": "Cinsel aktivite ve mekanik itilme"}]},
            {"cells": [{"text": "Çocukluk Çağı", "isMasked": False}, {"text": "Daha düşük insidans", "isMasked": False}, {"text": "Konjenital anomali varlığında artış", "isMasked": True, "hint": "yapısal bozukluk riski"}]}
        ]),
        make_chain("Cinsel Aktivite ile ÜSE Gelişim Zinciri", [
            "1. Cinsel Aktivite: Periüretral bölgeye mekanik basınç uygulanması.",
            "2. Bakteriyel İtilme: İntroitustaki bakterilerin üretral lümene itilmesi.",
            "3. Mesaneye İlerleme: Bakterilerin kısa üretrayı aşarak mesaneye varması.",
            "4. Akut Sistit Gelişimi: Ürotelyuma tutunma ve semptomların başlaması."
        ]),
        make_recall("Kadınlarda ÜSE insidansı hangi yaş grubunda pik yapmaktadır?", "18-24 yaş arası cinsel aktif kadınlarda pik yapmaktadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 18-24 Yaş Piki", [
            {"text": "Kadınlarda ÜSE 18-24 yaş arası cinsel aktif kadınlarda pik yapar.", "isLie": False, "explanation": "Doğru. Ders notu spot bilgisidir."},
            {"text": "Cinsel aktivite bakterilerin üretraya geçişini kolaylaştıran bir faktördür.", "isLie": False, "explanation": "Doğru. Mekanik etki ile geçiş kolaylaşır."},
            {"text": "Kadınlarda ÜSE yalnızca 85 yaşından sonra başlar, genç kadınlarda görülme sıklığı sıfırdır.", "isLie": True, "explanation": "Tuzak! ÜSE genç kadınlarda çok sıktır ve 18-24 yaş arasında pik yapar."},
            {"text": "18-24 yaş grubundaki kadınlarda akut sistit tablosuna sık rastlanır.", "isLie": False, "explanation": "Doğru. Pik dönemi klinik tablosudur."}
        ]),
        make_quiz("Kadınlarda üriner sistem enfeksiyonunun insidans piki yaptığı yaş grubu aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "18-24 yaş arası cinsel aktif dönem", "isCorrect": True, "explanation": "Ders notunda açıkça 18-24 yaş arası cinsel aktif kadınlarda pik yaptığı belirtilmiştir."},
            {"key": "B", "text": "1-3 yaş arası süt çocukluğu dönemi", "isCorrect": False, "explanation": "Bu dönem pik dönemi değildir."},
            {"key": "C", "text": "50-55 yaş arası menopoz geçiş dönemi", "isCorrect": False, "explanation": "Menopozda risk artmakla birlikte genç erişkin piki 18-24 yaştır."},
            {"key": "D", "text": "Yalnızca 90 yaş ve üzeri yatağa bağımlı dönem", "isCorrect": False, "explanation": "Pik dönemi genç erişkinliktedir."}
        ])
    ]
    slides.append(make_slide(5, "Epidemiyolojik Pik: 18-24 Yaş Arası Kadınlar", "Genç ve cinsel aktif kadınlarda ÜSE sıklığının zirve yapması", "Epidemiyoloji", s5_narrative, s5_bullets, s5_elements))

    # Slide 6: Kadınlarda Yaşam Boyu Risk ve Tekrarlama Oranı
    s6_narrative = (
        "Kadın popülasyonunda ÜSE geçirme riski yalnızca belirli bir yaşla sınırlı kalmayıp "
        "tüm yaşam süresine yayılan çok yüksek bir oran sergiler.\n\n"
        "- **Yaşam Boyu İnsidans:** Kadınların **%60'ında** yaşamları boyunca en az bir kez semptomatik "
        "üriner sistem enfeksiyonu görülür.\n"
        "- **Tekrarlama Sıklığı:** ÜSE geçiren kadınların **%10'unda** ise enfeksiyon her yıl en az "
        "bir kez tekrarlamaktadır.\n"
        "- **Klinik Süreç:** Bu yüksek nüks oranı, kadınların ürogenital florasındaki mikroorganizma "
        "dinamikleri ve anatomik yatkınlıkla yakından ilişkilidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kadınların %60'ında yaşam boyu en az bir kez semptomatik ÜSE görülür; kadınların %10'unda ise enfeksiyon her yıl en az bir kez tekrarlar."
    )
    s6_bullets = [
        "Kadınların %60'ında yaşam boyu en az bir kez semptomatik ÜSE gelişir.",
        "Kadınların %10'unda enfeksiyon her yıl en az bir kez tekrarlar.",
        "Yüksek nüks oranı klinik izlem ve koruyucu yaklaşımların önemini artırır."
    ]
    s6_elements = [
        make_cloze("Kadınların %60'ında en az bir kez semptomatik üriner sistem enfeksiyonu görülürken %10'unda her yıl tekrarlar.", "%60'ında", "Kadınların yaşam boyu semptomatik ÜSE geçirme oranı"),
        make_table("Kadınlarda ÜSE İstatistiksel Dağılımı", ["Klinik Durum", "Kadınlardaki Oran", "Klinik Anlamı"], [
            {"cells": [{"text": "En Az Bir Kez Semptomatik ÜSE", "isMasked": False}, {"text": "%60", "isMasked": True, "hint": "yüzde altmışlık kitle"}, {"text": "Popülasyonun yarıdan fazlası etkilenir"}]},
            {"cells": [{"text": "Her Yıl Tekrarlayan ÜSE", "isMasked": False}, {"text": "%10", "isMasked": False}, {"text": "Kronik takip ve profilaksi ihtiyacı", "isMasked": True, "hint": "yıllık yineleme yükü"}]}
        ]),
        make_recall("Kadınların yüzde kaçında yaşam boyu en az bir kez semptomatik ÜSE görülür ve yüzde kaçında her yıl tekrarlar?", "Kadınların %60'ında en az bir kez semptomatik ÜSE görülür; %10'unda ise her yıl en az bir kez tekrarlar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kadınlarda Yaşam Boyu Risk", [
            {"text": "Kadınların %60'ında en az bir kez semptomatik üriner sistem enfeksiyonu görülür.", "isLie": False, "explanation": "Doğru. Ders notundaki net veridir."},
            {"text": "Kadınların %10'unda enfeksiyon her yıl en az bir kez tekrarlar.", "isLie": False, "explanation": "Doğru. Tekrarlama oranı %10'dur."},
            {"text": "Kadınların yalnızca %0,01'i yaşam boyu ÜSE geçirir, toplumda görülmesi imkansızdır.", "isLie": True, "explanation": "Tuzak! Kadınların %60'ı gibi devasa bir oranda semptomatik ÜSE görülür."},
            {"text": "Tekrarlayan enfeksiyonlar kadınlarda yaşam kalitesini önemli ölçüde etkiler.", "isLie": False, "explanation": "Doğru. Klinik izlem gerektirir."}
        ]),
        make_quiz("Kadınlarda semptomatik üriner sistem enfeksiyonunun yaşam boyu görülme oranı ve yıllık tekrarlama sıklığı aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Yaşam boyu %60; her yıl en az bir kez tekrarlama %10", "isCorrect": True, "explanation": "Ders notu verisine göre kadınların %60'ında en az bir kez görülür, %10'unda her yıl tekrarlar."},
            {"key": "B", "text": "Yaşam boyu %1; her yıl en az bir kez tekrarlama %0,1", "isCorrect": False, "explanation": "Bu oranlar gerçeğin çok altındadır."},
            {"key": "C", "text": "Yaşam boyu %100; her yıl en az bir kez tekrarlama %100", "isCorrect": False, "explanation": "Tüm kadınlarda her yıl tekrarlamaz."},
            {"key": "D", "text": "Yaşam boyu %10; her yıl en az bir kez tekrarlama %60", "isCorrect": False, "explanation": "Rakamlar ters verilmiştir."}
        ])
    ]
    slides.append(make_slide(6, "Kadınlarda Yaşam Boyu Risk ve Nüks Dinamikleri", "Kadınların %60'ında semptomatik ÜSE ve %10'unda yıllık tekrarlama sıklığı", "Epidemiyoloji", s6_narrative, s6_bullets, s6_elements))

    # Slide 7: Erkeklerde ÜSE: 1-50 Yaş Arası Düşük Sıklık
    s7_narrative = (
        "Erkek popülasyonunda genç ve orta yaş döneminde üriner sistem enfeksiyonu görülme sıklığı "
        "kadınlara oranla dramatik şekilde düşüktür.\n\n"
        "- **Düşük Prevalans:** Erkeklerde 1-50 yaş arasında ÜSE sıklığı **%1'in altındadır**.\n"
        "- **Erkek Anatomik Bariyeri:** Erkek üretrasının uzun olması (yaklaşık 18-20 cm) bakterilerin "
        "mesaneye kadar olan yolculuğunu mekanik olarak zorlaştırır.\n"
        "- **Kimyasal Koruma:** Prostat bezinden salgılanan prostat sıvısı, içerdiği çinko ve özel "
        "antibakteriyel faktörlerle güçlü bakterisidal etki göstererek bakteriyel çoğalmayı durdurur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] 1-50 yaş arası erkeklerde ÜSE görülme sıklığı %1'in altındadır; bu yaş grubunda ÜSE saptanırsa mutlaka yapısal anomali araştırılmalıdır."
    )
    s7_bullets = [
        "Erkeklerde 1-50 yaş arasında ÜSE sıklığı %1'in altındadır.",
        "Uzun üretra anatomisi bakterilerin asendan yayılımını engeller.",
        "Prostat sıvısının bakterisidal etkisi ürofloranın korunmasını sağlar."
    ]
    s7_elements = [
        make_cloze("Erkeklerde 1-50 yaş arasında üriner sistem enfeksiyonu görülme sıklığı %1'in altındadır.", "%1'in altındadır", "Genç-orta yaş erkekteki binde birden az sıklık oranı"),
        make_table("Erkeklerde 1-50 Yaş Savunma Mekanizmaları", ["Savunma Bileşeni", "Etki Mekanizması", "Koruyucu Sonuç"], [
            {"cells": [{"text": "Üretra Uzunluğu", "isMasked": False}, {"text": "Fiziksel mesafe engeli (~20 cm)", "isMasked": True, "hint": "yaklaşık yirmi santimetrelik uzunluk"}, {"text": "Mesaneye retrograd ulaşım engellenir"}]},
            {"cells": [{"text": "Prostat Salgısı", "isMasked": False}, {"text": "Bakterisidal antibakteriyel faktörler", "isMasked": False}, {"text": "İntraüretral bakteri lizisi", "isMasked": True, "hint": "mikroorganizma parçalanması"}]}
        ]),
        make_chain("Genç Erkekte Koruyucu Bariyer Zinciri", [
            "1. Perineal Mesafe: Üretra ağzının rektumdan belirgin uzaklığı.",
            "2. Üretra Boyu: Bakterinin aşması gereken yaklaşık 20 cm'lik hat.",
            "3. Prostat Salgısı: Bakterisidal salgının lümene verilmesi.",
            "4. Normal İşeme: Kalan mikroorganizmaların idrar akımıyla atılması."
        ]),
        make_recall("1-50 yaş arasındaki erkeklerde ÜSE görülme sıklığı nedir ve bu düşüklüğün temel nedenleri nelerdir?", "Görülme sıklığı %1'in altındadır; uzun üretra anatomisi ve prostat sıvısının bakterisidal etkisi nedeniyle düşüktür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 1-50 Yaş Erkek", [
            {"text": "Erkeklerde 1-50 yaş arasında ÜSE görülme sıklığı %1'in altındadır.", "isLie": False, "explanation": "Doğru. Ders notu temel verisidir."},
            {"text": "Prostat salgısındaki bakterisidal etki erkeklerde koruyucu bir unsurdur.", "isLie": False, "explanation": "Doğru. Kimyasal savunma sağlar."},
            {"text": "1-50 yaş arası erkeklerin %90'ında her ay düzenli olarak sistit gelişir.", "isLie": True, "explanation": "Tuzak! Bu yaş grubunda sıklık %1'in altındadır, erkeklerde sistit çok nadirdir."},
            {"text": "Genç erkekte ÜSE saptanması altta yatan anomali araştırılmasını gerektirir.", "isLie": False, "explanation": "Doğru. Nadir olduğu için araştırılmalıdır."}
        ]),
        make_quiz("Erkeklerde 1-50 yaş arasında üriner sistem enfeksiyonu görülme sıklığı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "%1'in altındadır", "isCorrect": True, "explanation": "Ders notunda 1-50 yaş erkeklerde sıklığın %1'in altında olduğu açıkça belirtilmiştir."},
            {"key": "B", "text": "%60 civarındadır", "isCorrect": False, "explanation": "%60 kadınların yaşam boyu oranıdır."},
            {"key": "C", "text": "%10'dur", "isCorrect": False, "explanation": "%10 kadınlardaki yıllık nüks oranıdır."},
            {"key": "D", "text": "%80'in üzerindedir", "isCorrect": False, "explanation": "Genç erkekte ÜSE son derece nadirdir."}
        ])
    ]
    slides.append(make_slide(7, "Erkeklerde ÜSE: 1-50 Yaş Arası Görülme Sıklığı", "Genç ve orta yaş erkeklerde %1'in altındaki insidans ve koruyucu faktörler", "Epidemiyoloji", s7_narrative, s7_bullets, s7_elements))

    # Slide 8: İleri Yaş Erkeklerde ÜSE ve Risk Faktörleri (>65 Yaş)
    s8_narrative = (
        "Genç erkeklerdeki koruyucu mekanizmalar yaşlanma ile birlikte zayıflar ve ileri yaş grubunda "
        "erkeklerde ÜSE insidansında belirgin bir yükselme kaydedilir.\n\n"
        "- **Yaşla Artış:** Erkeklerde yaş arttıkça üriner sistem enfeksiyonu sıklığı belirgin olarak "
        "artış gösterir; özellikle **>65 yaşta sıklık artar**.\n"
        "- **Obstrüktif Üropati:** Prostat bezindeki büyümeye (benign prostat hiperplazisi - BPH) bağlı "
        "obstrüktif üropati gelişmesi mesanede rezidüel idrar birikmesine yol açar.\n"
        "- **Savunmanın Zayıflaması:** İleri yaşta artmış enstrümantasyon ve mesane kateteri kullanımı "
        "ile prostat salgısındaki bakterisidal etkinin azalması riski dramatik olarak artırır.\n\n"
        "> [!IMPORTANT]\n"
        "> İleri yaş erkeklerde (>65 yaş) ÜSE riskini artıran 3 temel faktör: 1) Enstrümantasyon ve kateter, 2) BPH'ya bağlı obstrüksiyon, 3) Prostat salgısının bakterisidal gücünün azalmasıdır."
    )
    s8_bullets = [
        "Erkeklerde yaş arttıkça sıklık artar, özellikle >65 yaşta belirgin yükselir.",
        "Prostat büyümesine bağlı obstrüktif üropati idrar stazına neden olur.",
        "Artmış kateter kullanımı ve prostat salgısının bakterisidal etkisinin azalması riski artırır."
    ]
    s8_elements = [
        make_cloze("Erkeklerde prostat bezindeki büyümeye bağlı obstrüktif üropati ve kateter kullanımı nedeniyle >65 yaşta sıklık artar.", ">65 yaşta", "Erkeklerde ÜSE sıklığının belirgin yükseldiği ileri yaş eşiği"),
        make_table("İleri Yaş Erkekte ÜSE Riskini Artıran Faktörler", ["Faktör Grubu", "Fizyopatolojik Değişim", "Klinik Sonuç"], [
            {"cells": [{"text": "Prostat Büyümesi", "isMasked": False}, {"text": "Obstrüktif üropati ve idrar stazı", "isMasked": True, "hint": "idrar akım engeli"}, {"text": "Bakteriyel çoğalma için zemin"}]},
            {"cells": [{"text": "Enstrümantasyon", "isMasked": False}, {"text": "Mesane kateteri uygulamaları", "isMasked": False}, {"text": "İatrojenik bakteri girişi", "isMasked": True, "hint": "tıbbi aletle bulaş"}]},
            {"cells": [{"text": "Salgı Değişimi", "isMasked": False}, {"text": "Prostat sıvısı bakterisidal etkisinde azalma", "isMasked": True, "hint": "salgının koruma gücü düşüşü"}, {"text": "Lokal kimyasal korumanın kaybı"}]}
        ]),
        make_chain("İleri Yaş Erkekte Patogenez Zinciri", [
            "1. BPH Gelişimi: Prostat dokusunda benign büyüme.",
            "2. Obstrüktif Üropati: Üretra lümeninde mekanik daralma.",
            "3. Rezidüel İdrar: Mesane tam boşalamaz ve idrar göllenir.",
            "4. Kateter Uygulaması: Akut retansiyonda kateter takılması.",
            "5. Enfeksiyon Gelişimi: Staz ve kateter üzerinden ÜSE atağı."
        ]),
        make_recall("İleri yaş erkeklerde (>65 yaş) ÜSE riskini artıran ders notunda belirtilen üç temel faktör nedir?", "1) Artmış enstrümantasyon ve mesane kateteri kullanımı, 2) Prostat büyümesine bağlı obstrüktif üropati, 3) Prostat salgısındaki bakterisidal etkinin azalmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İleri Yaş Erkekler", [
            {"text": "Erkeklerde yaş arttıkça üriner sistem enfeksiyonu sıklığı artar.", "isLie": False, "explanation": "Doğru. İleri yaşta insidans yükselir."},
            {"text": "Prostat bezindeki büyüme obstrüktif üropatiye yol açarak riski artırır.", "isLie": False, "explanation": "Doğru. İdrar stazı enfeksiyon zeminidir."},
            {"text": "İleri yaş erkeklerde prostat salgısının bakterisidal gücü gençlikten 100 kat daha güçlü hale gelir.", "isLie": True, "explanation": "Tuzak! Tam aksine ileri yaşta prostat salgısındaki bakterisidal etki azalır."},
            {"text": ">65 yaş erkeklerde enstrümantasyon ve mesane kateteri kullanımı riski yükseltir.", "isLie": False, "explanation": "Doğru. Önemli bir risk faktörüdür."}
        ]),
        make_quiz("İleri yaş erkeklerde (>65 yaş) üriner sistem enfeksiyonu sıklığının artmasında aşağıdakilerden hangisi ROL OYNAMAZ?", [
            {"key": "A", "text": "Prostat salgısındaki bakterisidal etkinin gençlere göre katlanarak artması", "isCorrect": True, "explanation": "Yanlış/Rol oynamaz! İleri yaşta prostat sıvısının bakterisidal etkisi azalır, artmaz."},
            {"key": "B", "text": "Prostat bezindeki büyümeye bağlı obstrüktif üropati gelişmesi", "isCorrect": False, "explanation": "Bu önemli bir risk faktörüdür."},
            {"key": "C", "text": "Artmış enstrümantasyon ve mesane kateteri kullanımı", "isCorrect": False, "explanation": "Bu önemli bir risk faktörüdür."},
            {"key": "D", "text": "Mesane çıkım obstrüksiyonuna bağlı rezidüel idrar kalması", "isCorrect": False, "explanation": "Bu staza yol açarak riski artırır."}
        ])
    ]
    slides.append(make_slide(8, "İleri Yaş Erkeklerde ÜSE ve Risk Faktörleri", "BPH obstrüktif üropatisi, kateterizasyon ve azalan bakterisidal prostat salgısı", "Epidemiyoloji", s8_narrative, s8_bullets, s8_elements))

    # Slide 9: Birinci Bölüm Özeti: Tanım ve Epidemiyolojik Profil
    s9_narrative = (
        "Üriner sistem enfeksiyonları tanım, klinik skala ve epidemiyolojik dağılım dinamikleri ile "
        "birinci bölümün temel kazanımlarını oluşturur.\n\n"
        "- **Kapsam:** ÜSE, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur; "
        "asemptomatik bakteriüriden sepsise kadar uzanır.\n"
        "- **Kadın Dinamikleri:** İnsidans 18-24 yaş cinsel aktif kadınlarda pik yapar; kadınların %60'ı "
        "yaşam boyu en az bir kez semptomatik ÜSE geçirirken %10'unda her yıl tekrarlar.\n"
        "- **Erkek Dinamikleri:** 1-50 yaş arası erkekte insidans <%1'dir; ancak >65 yaşta BPH'ya bağlı "
        "obstrüksiyon, kateterler ve azalan prostat bakterisidal aktivitesi nedeniyle sıklık artar.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] Üriner enfeksiyonlar üretradan böbreğe tüm traktusu tutabilir; genç erişkinde kadın ezici üstünlüğe sahipken, ileri yaşta erkekte obstrüksiyonla insidans artar."
    )
    s9_bullets = [
        "ÜSE üretradan böbreğe tüm dokuların enfeksiyonudur; skala ABU'dan sepsise uzanır.",
        "Kadınlarda 18-24 yaşta pik yapar; %60 yaşam boyu risk, %10 yıllık tekrarlama vardır.",
        "Erkekte 1-50 yaşta <%1 iken, >65 yaşta BPH ve kateterlerle sıklık artar."
    ]
    s9_elements = [
        make_cloze("Kadınlarda ÜSE 18-24 yaş grubunda pik yaparken erkeklerde 1-50 yaş arasında sıklık %1'in altındadır.", "%1'in altındadır", "Genç erkeklerdeki düşük sıklık eşiği"),
        make_table("Epidemiyolojik Karşılaştırma Matrisi", ["Grup", "Temel İstatistik", "Baskın Risk / Mekanizma"], [
            {"cells": [{"text": "Genç Kadın (18-24 yaş)", "isMasked": False}, {"text": "İnsidans piki, %60 yaşam boyu", "isMasked": True, "hint": "genç kadın pik verisi"}, {"text": "Kısa üretra ve cinsel aktivite"}]},
            {"cells": [{"text": "Genç Erkek (1-50 yaş)", "isMasked": False}, {"text": "<%1 sıklık", "isMasked": False}, {"text": "Uzun üretra ve bakterisidal prostat sıvısı", "isMasked": True, "hint": "genç erkekteki koruma"}]},
            {"cells": [{"text": "İleri Yaş Erkek (>65 yaş)", "isMasked": False}, {"text": "Belirgin sıklık artışı", "isMasked": True, "hint": "yaşlı erkekte artış"}, {"text": "BPH obstrüktif üropatisi ve kateter"}]}
        ]),
        make_recall("Birinci bölümdeki temel epidemiyolojik verilere göre kadınların yaşam boyu ÜSE riski ve genç erkekteki sıklık nedir?", "Kadınların yaşam boyu riski %60 iken, 1-50 yaş erkeklerde sıklık %1'in altındadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm Özeti", [
            {"text": "ÜSE üretradan böbreğe kadar herhangi bir dokunun enfeksiyonudur.", "isLie": False, "explanation": "Doğru. Temel tanımdır."},
            {"text": "Kadınlarda insidans 18-24 yaş arası cinsel aktif dönemde pik yapar.", "isLie": False, "explanation": "Doğru. İnsidans pikidir."},
            {"text": "1-50 yaş arası erkeklerde ÜSE kadınlardan 20 kat daha sıktır ve insidansı %85'tir.", "isLie": True, "explanation": "Tuzak! 1-50 yaş erkeklerde sıklık %1'in altındadır, kadınlarda ise çok daha sıktır."},
            {"text": "Kadınların %10'unda ÜSE her yıl en az bir kez tekrarlar.", "isLie": False, "explanation": "Doğru. Yıllık nüks oranıdır."}
        ]),
        make_quiz("Birinci bölümde işlenen epidemiyolojik verilerle ilgili aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "1-50 yaş arası erkeklerde ÜSE sıklığı %60 olup kadınlardan daha yüksektir", "isCorrect": True, "explanation": "Yanlış! 1-50 yaş erkekte sıklık <%1'dir; %60 olan oran kadınların yaşam boyu riskidir."},
            {"key": "B", "text": "Kadınlarda 18-24 yaş grubunda ÜSE insidansı pik yapar", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Kadınların %10'unda her yıl en az bir kez ÜSE tekrarlar", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "İleri yaş erkeklerde prostat büyümesi ve kateterizasyon riski artırır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(9, "Birinci Bölüm Özeti: Tanım ve Epidemiyolojik Profil", "ÜSE tanımı, spektrumu, kadın ve erkek epidemiyolojisinin konsolidasyonu", "Bölüm Özeti", s9_narrative, s9_bullets, s9_elements))

    # Slide 10: [TEKRAR SAYFASI - CHECKPOINT 1] Giriş, Tanımlar ve Epidemiyoloji
    s10_narrative = (
        "Bu tekrar sayfasında 1. Bölümde işlenen ÜSE tanımı, klinik skala, kadın ve erkeklerdeki "
        "epidemiyolojik farklılıkları kapsamlı olarak pekiştiriyoruz.\n\n"
        "- **Tanım ve Kapsam:** ÜSE, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun "
        "enfeksiyonudur ve asemptomatik bakteriüriden sepsise uzanan bir skala gösterir.\n"
        "- **Kadın Epidemiyolojisi:** 18-24 yaş cinsel aktif kadınlarda pik yapar; kadınların %60'ında "
        "yaşam boyu en az bir kez görülür, %10'unda her yıl tekrarlar.\n"
        "- **Erkek Epidemiyolojisi:** 1-50 yaş erkekte sıklık <%1 iken, >65 yaşta BPH'ya bağlı obstrüktif "
        "üropati, kateterizasyon ve bakterisidal prostat sıvısı azalması ile sıklık artar.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 1] ÜSE üretradan böbreğe kadar tüm üriner traktusu tutabilen geniş bir skaladır; kadınlarda %60 yaşam boyu risk ve 18-24 yaş piki varken, erkekte gençlikte <%1, ileri yaşta artış görülür."
    )
    s10_bullets = [
        "ÜSE: Üretradan böbreğe herhangi bir dokunun enfeksiyonudur (ABU'dan sepsise skala).",
        "Kadınlar: 18-24 yaş piki, %60 yaşam boyu risk, %10 yıllık tekrarlama.",
        "Erkekler: 1-50 yaş <%1; >65 yaşta BPH, kateter ve azalan prostat salgısıyla artış."
    ]
    s10_elements = [
        make_cloze("Üriner sistem enfeksiyonu, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur.", "üretradan böbreğe kadar", "Enfeksiyonun anatomik sınırları"),
        make_table("1. Bölüm Büyük Tekrar Tablosu", ["Parametre", "Tanımlayıcı Değer / Kriter", "Klinik Özellik"], [
            {"cells": [{"text": "ÜSE Tanımı", "isMasked": False}, {"text": "Üretradan böbreğe doku enfeksiyonu", "isMasked": True, "hint": "tüm traktusu kapsayan tanım"}, {"text": "ABU'dan sepsise geniş skala"}]},
            {"cells": [{"text": "Kadın Yaşam Boyu Risk", "isMasked": False}, {"text": "%60 semptomatik ÜSE", "isMasked": False}, {"text": "Kadınların çoğunluğu etkilenir", "isMasked": True, "hint": "popülasyondaki yaygınlık"}]},
            {"cells": [{"text": "Kadın İnsidans Piki", "isMasked": False}, {"text": "18-24 yaş cinsel aktif dönem", "isMasked": True, "hint": "genç kadın yaş aralığı"}, {"text": "Mekanik bakteriyel geçiş"}]},
            {"cells": [{"text": "Genç Erkek (1-50 yaş)", "isMasked": False}, {"text": "<%1 sıklık", "isMasked": False}, {"text": "Uzun üretra ve prostatik savunma", "isMasked": True, "hint": "erkek koruma bariyerleri"}]}
        ]),
        make_chain("Klinik Skala ve İlerleme Hiyerarşisi", [
            "1. Asemptomatik Bakteriüri: Semptomsuz üreme.",
            "2. Akut Sistit: Lokal alt üriner traktus enfeksiyonu.",
            "3. Akut Piyelonefrit: Böbrek parankim tutulumu ve ateş.",
            "4. Ürosepsis: Sistemik yayılım ve organ disfonksiyonu."
        ]),
        make_recall("Checkpoint 1: Kadınlarda ÜSE insidans piki hangi yaşta görülür ve 1-50 yaş arası erkekte sıklık nedir?", "Kadınlarda 18-24 yaş arasında pik yapar; 1-50 yaş arası erkeklerde sıklık %1'in altındadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 1 Konsolidasyonu", [
            {"text": "ÜSE, üriner sistemin üretradan böbreğe kadar herhangi bir dokusunun enfeksiyonudur.", "isLie": False, "explanation": "Doğru. 1. bölümün temel tanımıdır."},
            {"text": "Kadınların %60'ında en az bir kez semptomatik ÜSE görülür ve %10'unda her yıl tekrarlar.", "isLie": False, "explanation": "Doğru. Kadın epidemiyoloji verisidir."},
            {"text": "Erkeklerde ÜSE sıklığı 1-50 yaş arasında %80 iken 65 yaşından sonra tamamen sıfırlanır.", "isLie": True, "explanation": "Tuzak! Tam tersine 1-50 yaş erkekte <%1'dir, >65 yaşta ise BPH ve kateterlerle sıklık artar."},
            {"text": "Klinik spektrum asemptomatik bakteriüriden sepsise kadar uzanır.", "isLie": False, "explanation": "Doğru. Geniş skala mevcuttur."}
        ]),
        make_quiz("1. Bölümün tamamı (Giriş, Tanımlar ve Epidemiyoloji) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Erkeklerde 1-50 yaş arasında ÜSE görülme sıklığı kadınlardan belirgin olarak yüksektir ve %75 civarındadır", "isCorrect": True, "explanation": "Yanlış! 1-50 yaş erkekte sıklık <%1'dir; kadınlarda ise 18-24 yaşta pik yapar ve çok daha sıktır."},
            {"key": "B", "text": "Üriner sistem enfeksiyonu üretradan böbreğe kadar herhangi bir dokunun enfeksiyonudur", "isCorrect": False, "explanation": "Doğru bir tanımdır."},
            {"key": "C", "text": "Kadınların %60'ında en az bir kez semptomatik ÜSE görülür", "isCorrect": False, "explanation": "Doğru bir epidemiyolojik veridir."},
            {"key": "D", "text": "İleri yaş erkeklerde BPH'ya bağlı obstrüktif üropati riski artıran temel faktörlerdendir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(10, "[TEKRAR SAYFASI - CHECKPOINT 1] Giriş, Tanımlar ve Klinik Spektrum", "1. Bölümün kapsamlı pekiştirmesi: tanım, klinik skala, kadın ve erkek epidemiyolojisi", "Bölüm Tekrarı", s10_narrative, s10_bullets, s10_elements))

    return slides
