# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec10():
    slides = []

    # Slide 91: Trimetoprim-Sulfametoksazol (TMP-SMX) Farmakolojisi ve Kontrendikasyonları
    s91_narrative = (
        "Trimetoprim-Sulfametoksazol (TMP-SMX / Ko-trimoksazol), bakteriyel folik asit sentez yolağındaki "
        "ardışık iki basamağı inhibe eden klasik bir antibakteriyel kombinasyondur.\n\n"
        "- **Sinerjistik Etki:** Trimetoprime sulfametoksazol eklenmesi **sinerjistik etki** yaratarak "
        "bakterisidal güç kazandırır ve direnç gelişme riskini belirgin şekilde azaltır; Enterococcus "
        "ve Pseudomonas dışındaki çoğu üropatojene etkilidir.\n"
        "- **Üstünlükleri:** Maliyetinin son derece ucuz olması ve bağırsak ile vajina florasına özgü "
        "ekolojik yan hasarının az olması en büyük klinik avantajlarıdır.\n"
        "- **Mutlak Kontrendikasyonlar:** Teratojenik folat antagonizması ve yenidoğanda kernikterus "
        "riski nedeniyle **GEBELERDE**, ayrıca metabolik etkileşimle kanama riskini artıran **WARFARİN "
        "kullanan hastalarda KESİNLİKLE KULLANILMAMALIDIR**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] TMP-SMX sinerjistik etkilidir; GEBELERDE ve WARFARİN kullanan hastalarda KESİNLİKLE KULLANILMAZ!"
    )
    s91_bullets = [
        "TMP ve SMX folat yolağında sinerjistik bakterisidal etki gösterir.",
        "Maliyeti ucuzdur ve bağırsak florasına yan etkisi minimaldir.",
        "Gebelerde ve warfarin kullanan hastalarda KESİNLİKLE KONTRENDİKEDİR."
    ]
    s91_elements = [
        make_cloze("Trimetoprim-Sulfametoksazol (TMP-SMX) teratojenite ve etkileşim nedeniyle gebelerde ve warfarin kullananlarda kontrendikedir.", "warfarin", "Oral antikoagülan kan sulandırıcı ilaç"),
        make_table("TMP-SMX Klinik Farmakolojisi", ["Özellik", "Farmakolojik Mekanizma", "Klinik Yansıması"], [
            {"cells": [{"text": "Etki Mekanizması", "isMasked": False}, {"text": "Ardışık folik asit sentez blokajı", "isMasked": True, "hint": "çifte folat inhibisyonu"}, {"text": "Güçlü sinerjistik bakterisidal etki"}]},
            {"cells": [{"text": "Dirençli Türler", "isMasked": False}, {"text": "Enterokoklar ve Pseudomonas türleri", "isMasked": False}, {"text": "Doğal direnç nedeniyle etkisizdir", "isMasked": True, "hint": "ilacın etki etmediği bakteriler"}]},
            {"cells": [{"text": "Kontrendikasyon", "isMasked": False}, {"text": "Gebelik ve Warfarin kullanımı", "isMasked": True, "hint": "iki yasaklı hasta grubu"}, {"text": "Folat antagonizması ve kanama riski"}]}
        ]),
        make_chain("TMP-SMX Etki ve Toksisite Zinciri", [
            "1. Sentez Blokajı: Dihidropteroat sentaz ve dihidrofolat redüktaz bloke edilir.",
            "2. DNA Sentez Durması: Bakteriyel timidin ve pürin üretimi durur.",
            "3. Warfarin Etkileşimi: Karaciğerde CYP2C9'u inhibe ederek INR'yi fırlatır.",
            "4. Klinik Kural: Gebede ve warfarin kullanan hastada asla reçete edilmez."
        ]),
        make_recall("TMP-SMX'in kullanımının kesinlikle kontrendike olduğu iki önemli hasta grubu hangisidir?", "Gebeler ve warfarin kullanan hastalardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: TMP-SMX Farmakolojisi", [
            {"text": "TMP'e SMX eklenmesi sinerjistik etki yaparak direnç riskini azaltır.", "isLie": False, "explanation": "Doğru. Çifte folat blokajıdır."},
            {"text": "Maliyetinin ucuz olması ve bağırsak florasını koruması üstünlüğüdür.", "isLie": False, "explanation": "Doğru. Klinik avantajıdır."},
            {"text": "TMP-SMX tüm gebelerde ve warfarin kullananlarda en güvenli birinci tercihtir.", "isLie": True, "explanation": "Tuzak! TMP-SMX GEBELERDE ve WARFARİN KULLANANLARDA KESİNLİKLE KULLANILMAMALIDIR (kontrendikedir)."},
            {"text": "Enterokoklar ve Pseudomonas türleri TMP-SMX'e dirençlidir.", "isLie": False, "explanation": "Doğru. Doğal direnç gösterirler."}
        ]),
        make_quiz("Trimetoprim-Sulfametoksazol (TMP-SMX) aşağıdaki hasta gruplarından hangisinde KESİNLİKLE KULLANILMAMALIDIR?", [
            {"key": "A", "text": "Gebelerde ve warfarin kullanan hastalarda", "isCorrect": True, "explanation": "Ders notunda 'Gebelerde ve warfarin kullanan hastalarda kullanılmamalıdır' uyarısı açıkça yer almaktadır."},
            {"key": "B", "text": "Sağlıklı genç erkeklerde", "isCorrect": False, "explanation": "Kullanılabilir."},
            {"key": "C", "text": "Sadece gözlük takan insanlarda", "isCorrect": False, "explanation": "Tıbbi kısıtlama değildir."},
            {"key": "D", "text": "Ateşi olmayan kadınlarda", "isCorrect": False, "explanation": "Sistitte kullanılır."}
        ])
    ]
    slides.append(make_slide(91, "Trimetoprim-Sulfametoksazol (TMP-SMX) Farmakolojisi ve Kontrendikasyonları", "TMP-SMX sinerjizmi, maliyet üstünlüğü; gebelikte ve warfarinde kontrendikasyon", "Antibakteriyel Ajanlar", s91_narrative, s91_bullets, s91_elements))

    # Slide 92: Nitrofurantoin: Doku Penetrasyonu Kısıtlılığı ve Toksisite Profili
    s92_narrative = (
        "Nitrofurantoin, kırk yılı aşkın süredir basit sistit tedavisinde ve profilaksisinde güvenle "
        "kullanılan, ancak doku dağılımı son derece özelleşmiş bir üriner antiseptiktir.\n\n"
        "- **Doku Konsantrasyonu Kısıtlılığı:** Ağızdan alındıktan sonra idrardan son derece hızlı "
        "itrah edilir; kandaki ve böbrek parankimindeki seviyesi neredeyse sıfırdır. Bu nedenle **komplike "
        "idrar yolu enfeksiyonlarında ve ÜST SİSTEMDE (akut pyelonefrit) ASLA KULLANILMAZ**.\n"
        "- **Kreatinin Klirensi Sınırı:** İdrara geçebilmesi için böbrek fonksiyonu şarttır; kreatinin "
        "klirensi **50 ml/dk'dan düşük olan hastalarda** idrarda terapötik düzeye ulaşamaz ve toksisite artar.\n"
        "- **Kardinal Toksisiteler:** G6PD eksikliği olanlarda **akut hemoliz**; kronik kullanımda "
        "**pulmoner hipersensitivite/fibrozis** ve özellikle böbrek yetmezliği olanlarda **periferik nöropati** yapar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Nitrofurantoin komplike ÜSE ve pyelonefritte KULLANILMAZ; CrCl <50 ml/dk'da kontrendikedir; G6PD eksikliğinde hemoliz ve pulmoner reaksiyon yapar."
    )
    s92_bullets = [
        "Komplike İYE ve üst üriner sistemde (pyelonefrit) KESİNLİKLE KULLANILMAZ.",
        "Kreatinin klirensi <50 ml/dk olan hastalarda yetersiz konsantrasyon nedeniyle verilmez.",
        "G6PD eksikliğinde hemoliz, periferik nöropati ve pulmoner reaksiyon yapabilir."
    ]
    s92_elements = [
        make_cloze("Nitrofurantoin böbrek parankiminde terapötik konsantrasyona ulaşamadığı için pyelonefrit ve üst sistemde kullanılmaz.", "üst sistemde", "Böbrek ve üreterleri içeren anatomik bölge"),
        make_table("Nitrofurantoin Kullanım Kısıtlılıkları", ["Kısıtlılık / Toksisite", "Eşik Değer / Risk Grubu", "Klinik Mekanizma"], [
            {"cells": [{"text": "Anatomik Yasak", "isMasked": False}, {"text": "Üst sistem ve pyelonefrit", "isMasked": True, "hint": "böbrek iltihabı yasağı"}, {"text": "Doku düzeyinde terapötik seviyeye ulaşamaması"}]},
            {"cells": [{"text": "Renal Eşik", "isMasked": False}, {"text": "Kreatinin klirensi <50 ml/dk", "isMasked": True, "hint": "elli mililitre dakika altı"}, {"text": "İdrara atılamama ve kanda toksik birikim"}]},
            {"cells": [{"text": "Hematolojik Toksisite", "isMasked": False}, {"text": "G6PD eksikliği olan hastalar", "isMasked": False}, {"text": "Glutatyon yetersizliğine bağlı eritrosit hemolizi", "isMasked": True, "hint": "alyuvarların parçalanması"}]}
        ]),
        make_chain("Nitrofurantoin Toksisite ve Kısıtlama Zinciri", [
            "1. Hızlı İtrah: İlaç emilir emilmez idrara atılır, doku konsantrasyonu oluşmaz.",
            "2. Pyelonefrit Başarısızlığı: Böbreğe ulaşamadığından pyelonefritte bakteriyi öldüremez.",
            "3. Renal Fonksiyon Düşüşü: CrCl <50 olunca lümene geçemez ve sinir dokusunda birikir.",
            "4. Yan Etki: Periferik nöropati ve G6PD hastasında masif hemoliz gelişir."
        ]),
        make_recall("Nitrofurantoin'in akut pyelonefritte kullanılamamasının temel farmakolojik nedeni nedir?", "İdrardan çok hızlı atıldığı ve böbrek dokusunda terapötik konsantrasyona ulaşamadığı içindir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Nitrofurantoin", [
            {"text": "Nitrofurantoin komplike enfeksiyonlarda ve üst sistemde kullanılmamalıdır.", "isLie": False, "explanation": "Doğru. Doku penetrasyonu yoktur."},
            {"text": "Kreatinin klirensi 50 ml/dk'dan düşük hastalarda kullanılmamalıdır.", "isLie": False, "explanation": "Doğru. İdrara geçemez."},
            {"text": "Nitrofurantoin ağır pyelonefrit ve sepsis için dünyadaki en güçlü damar içi ilaçtır.", "isLie": True, "explanation": "Tuzak! Nitrofurantoin üst sistemde ve pyelonefritte KESİNLİKLE KULLANILMAZ; sadece alt sistem sistit ilacıdır."},
            {"text": "G6PD eksikliği olan hastalarda hemolitik anemiye yol açabilir.", "isLie": False, "explanation": "Doğru. Oksidan strestir."}
        ]),
        make_quiz("Nitrofurantoin kullanımı ile ilgili aşağıdaki klinik ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Akut pyelonefrit ve komplike üst üriner sistem enfeksiyonlarında ilk tercihtir", "isCorrect": True, "explanation": "Kesinlikle yanlış! Ders notunda 'Komplike idrar yolu enfeksiyonları ve üst sistemde kullanılmamalıdır' uyarısı açıkça yer almaktadır."},
            {"key": "B", "text": "Kreatinin klirensi <50 ml/dk olan hastalarda kullanılmamalıdır", "isCorrect": False, "explanation": "Doğru bir kuraldır."},
            {"key": "C", "text": "G6PD eksikliği olan hastalarda hemoliz yapabilir", "isCorrect": False, "explanation": "Doğru bir kuraldır."},
            {"key": "D", "text": "Barsak ve vajinal floraya etkisi minimaldir", "isCorrect": False, "explanation": "Doğru bir kuraldır."}
        ])
    ]
    slides.append(make_slide(92, "Nitrofurantoin: Doku Penetrasyonu Kısıtlılığı ve Toksisite Profili", "Nitrofurantoin, üst sistemde/pyelonefritte kullanılmama kuralı, CrCl <50 sınırı ve G6PD hemolizi", "Antibakteriyel Ajanlar", s92_narrative, s92_bullets, s92_elements))

    # Slide 93: Sefalosporinler ve Aminopenisilinler: Gebelik Güvenliği ve Direnç
    s93_narrative = (
        "Beta-laktam grubu antibiyotikler, özellikle sefalosporinler ve aminopenisilinler, ÜSE "
        "tedavisinde gebelik güvenliği ve artan direnç oranları açısından iki zıt ucu temsil eder.\n\n"
        "- **Sefalosporinlerin Spektrumu ve Güvenliği:** Enterobacteriaceae türlerine oldukça etkilidir; "
        "ancak **enterokoklara karşı kesinlikle etkisizdirler**. En büyük üstünlükleri **gebelikte "
        "kullanımlarının son derece güvenli olmasıdır**; penisilin alerjisi olanlarda çapraz reaktivite riski taşırlar.\n"
        "- **Aminopenisilinlerin Çöküşü:** Ampisilin ve amoksisilin gibi aminopenisilinlere karşı "
        "günümüzde **%40-60 arasında küresel direnç gelişmiştir**.\n"
        "- **Ekolojik Yan Hasar:** Aminopenisilinler vajina ve bağırsak florasını tahrip ederek "
        "dirençli türlerin kolonizasyonuna ve kandida vajinitine yol açtığından tek başlarına kullanılmazlar.\n\n"
        "> [!IMPORTANT]\n"
        "> Sefalosporinler gebelikte güvenlidir fakat enterokoklara etkisizdir; aminopenisilinler ise %40-60 direnç ve ekolojik yan hasar nedeniyle tek başına önerilmez."
    )
    s93_bullets = [
        "Sefalosporinler gebelikte son derece güvenlidir; enterokoklara karşı etkisizdir.",
        "Aminopenisilinlere (ampisilin/amoksisilin) karşı %40-60 direnç gelişmiştir.",
        "Florayı bozarak kandida vajiniti ve dirençli suş kolonizasyonu yaratırlar."
    ]
    s93_elements = [
        make_cloze("Tüm sefalosporinler Enterobacteriaceae türlerine etkili iken enterokoklara karşı zayıf ve etkisizdir.", "enterokoklara", "Ampisilin duyarlı Gram pozitif koklar"),
        make_table("Beta-Laktamların ÜSE Özellikleri", ["Antibiyotik Grubu", "Temel Avantajı / Durumu", "Kısıtlılığı / Direnç"], [
            {"cells": [{"text": "Sefalosporinler", "isMasked": False}, {"text": "Gebelikte kullanımı son derece güvenlidir", "isMasked": True, "hint": "hamilelikte ilk tercih"}, {"text": "Enterokoklara kesinlikle etkisizdir; alerji riski"}]},
            {"cells": [{"text": "Aminopenisilinler", "isMasked": False}, {"text": "Geçmişte yaygın kullanım", "isMasked": False}, {"text": "%40-60 direnç gelişimi; tek başına önerilmez", "isMasked": True, "hint": "yüzde kırk altmış direnç çöküşü"}]},
            {"cells": [{"text": "3. Kuşak Sefalosporinler", "isMasked": False}, {"text": "Geniş spektrum, parenteral pyelonefrit", "isMasked": False}, {"text": "Standart dirençli suşlarda kısıtlıdır", "isMasked": False}]}
        ]),
        make_chain("Beta-Laktam Seçim Algoritması", [
            "1. Hasta Durumu: Gebe kadında komplike sistit veya pyelonefrit saptanır.",
            "2. İlaç Seçimi: Fetal toksisiteyi önlemek için sefalosporin tercih edilir.",
            "3. Etken Uyarısı: İdrarda Enterokok ürerse sefalosporin derhal kesilir (etkisizdir).",
            "4. Aminopenisilin Yasağı: %40-60 direnç nedeniyle tek başına ampisilin verilmez."
        ]),
        make_recall("Sefalosporinlerin gebelikteki güvenilirlik durumu ve doğal olarak etkisiz oldukları Gram pozitif bakteri grubu nedir?", "Gebelikte kullanımları son derece güvenlidir; ancak enterokoklara karşı doğal olarak etkisizdirler."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sefalosporin ve Aminopenisilin", [
            {"text": "Sefalosporinlerin gebelikte kullanımı güvenlidir.", "isLie": False, "explanation": "Doğru. Teratojenik değildir."},
            {"text": "Sefalosporinler enterokoklara karşı zayıf ve etkisizdir.", "isLie": False, "explanation": "Doğru. Doğal direnç vardır."},
            {"text": "Aminopenisilinlere karşı hiçbir direnç yoktur, %100 başarıyla tüm bakterileri yok eder.", "isLie": True, "explanation": "Tuzak! Aminopenisilinlere karşı %40-60 arasında yüksek direnç vardır; tek başlarına kullanılmazlar."},
            {"text": "Penisilin alerjisi olan hastalarda sefalosporin kullanımında dikkatli olunmalıdır.", "isLie": False, "explanation": "Doğru. Çapraz alerji riski vardır."}
        ]),
        make_quiz("Sefalosporin grubu antibiyotiklerin üriner sistem enfeksiyonlarındaki etkinliği ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Gebelikte kullanımı güvenlidir ancak enterokoklara karşı etkisizdir", "isCorrect": True, "explanation": "Ders notunda 'Enterobacteria türüne oldukça etkinken enterokoklara zayıf etkilidir; gebelikte kullanımı güvenlidir' ifadesi yer almaktadır."},
            {"key": "B", "text": "Gebelikte kesinlikle ölümcüldür ve yasaktır", "isCorrect": False, "explanation": "Gebelikte en güvenli gruptur."},
            {"key": "C", "text": "Sadece enterokokları öldürür, E. coli'ye hiç etki etmez", "isCorrect": False, "explanation": "Tam tersidir."},
            {"key": "D", "text": "Asla idrara geçmeyen bir antibiyotiktir", "isCorrect": False, "explanation": "İdrar atılımı yüksektir."}
        ])
    ]
    slides.append(make_slide(93, "Sefalosporinler ve Aminopenisilinler: Gebelik Güvenliği ve Direnç", "Sefalosporin gebelik güvenliği, enterokok etkisizliği ve aminopenisilinlerde %40-60 direnç", "Antibakteriyel Ajanlar", s93_narrative, s93_bullets, s93_elements))

    # Slide 94: Florokinolonlar ve Aminoglikozidler: Kıkırdak Toksisitesi ve Nefrotoksisite
    s94_narrative = (
        "Florokinolonlar ve aminoglikozidler, yüksek doku penetrasyonları ile piyelonefrit ve ürosepsiste "
        "hayat kurtaran ancak özgül organ toksisiteleri barındıran güçlü ajanlardır.\n\n"
        "- **Florokinolonlar (Siprofloksasin / Levofloksasin):** Enterobacteriaceae ve Pseudomonas'a "
        "karşı son derece etkilidir. En kritik kontrendikasyon: Büyümekte olan eklem kıkırdağına zarar "
        "verdiği için **ÇOCUKLARDA VE GEBELERDE KESİNLİKLE KULLANILMAMALIDIR**; epilepside nöbet eşiğini düşürür; "
        "antiasit ve demir emilimini bozar.\n"
        "- **Aminoglikozidler (Gentamisin / Amikasin):** Ateşli ağır enfeksiyonlarda ve sepsis kombinasyonlarında "
        "kullanılır; **nefrotoksik (nonoligurik azotemi) ve ototoksik (işitme/vestibüler hasar)** yan etkileri vardır.\n"
        "- **Tek Doz Uygulaması:** Aminoglikozidlerin nefrotoksisitesini azaltmak ve post-antibiyotik "
        "etkisini artırmak için günlük dozun **tek seferde (günde tek doz)** verilmesi önerilmektedir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Florokinolonlar çocuklar ve gebelerde kıkırdak hasarı nedeniyle kontrendikedir! Aminoglikozidler nefrotoksik ve ototoksiktir; toksisiteyi azaltmak için günde tek doz önerilir."
    )
    s94_bullets = [
        "Florokinolonlar çocuklar ve gebelerde kıkırdak gelişimi hasarı nedeniyle KONTRENDİKEDİR.",
        "Epilepsi hastalarında nöbet eşiğini düşürür; antiasit ve demirle emilimi bozulur.",
        "Aminoglikozidler nefrotoksik ve ototoksiktir; toksisiteyi azaltmak için günde tek doz verilir."
    ]
    s94_elements = [
        make_cloze("Florokinolon grubu antibiyotikler kıkırdak gelişimini olumsuz etkilediğinden çocuklar ve gebelerde kullanılmamalıdır.", "kıkırdak gelişimini", "Büyüyen eklem ve kıkırdak dokusu"),
        make_table("Kinolon ve Aminoglikozid Toksisite Profili", ["İlaç Grubu", "Temel Toksisite / Kontrendikasyon", "Önlem / Uygulama Kuralı"], [
            {"cells": [{"text": "Florokinolonlar", "isMasked": False}, {"text": "Kıkırdak hasarı, artropati, epilepsi nöbeti", "isMasked": True, "hint": "çocukta kıkırdak toksisitesi"}, {"text": "Çocuklar ve gebelerde kesinlikle kullanılmaz"}]},
            {"cells": [{"text": "Aminoglikozidler", "isMasked": False}, {"text": "Nefrotoksisite ve Ototoksisite", "isMasked": True, "hint": "böbrek ve kulak hasarı"}, {"text": "Toksisiteyi azaltmak için günde tek doz uygulama"}]}
        ]),
        make_chain("Toksisite ve İlaç Kısıtlama Mekanizması", [
            "1. Kinolon İntrauterin Geçiş: Florokinolon plasentayı geçer veya süte dökülür.",
            "2. Kondrosit Nekrozu: Fetal eklem kıkırdağında kondrosit apoptozu ve kıkırdak erozyonu yapar.",
            "3. Çocukta Kontrendikasyon: Büyüme kıkırdakları kapanana kadar kullanımı yasaklanır.",
            "4. Aminoglikozid Renal Toksisite: Tübül hücrelerinde birikerek nonoligurik akut böbrek hasarı yapar."
        ]),
        make_recall("Florokinolonların çocuklar ve gebe kadınlarda kullanılmasının kesinlikle yasak (kontrendike) olmasının temel nedeni nedir?", "Büyümekte olan eklem kıkırdağı gelişimini olumsuz etkilemesi (kondrotoksisite ve artropati) nedeniyledir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kinolon ve Aminoglikozid", [
            {"text": "Florokinolonlar çocuklar ve gebelerde kıkırdak gelişimi nedeniyle kontrendikedir.", "isLie": False, "explanation": "Doğru. Kesin sınav kuralıdır."},
            {"text": "Aminoglikozidlerin nefrotoksik ve ototoksik yan etkileri vardır.", "isLie": False, "explanation": "Doğru. Tübüler ve koklear hasar yapar."},
            {"text": "Florokinolonlar 1 günlük yeni doğmuş prematüre bebeklerde birinci tercih vitamin ilacıdır.", "isLie": True, "explanation": "Tuzak! Florokinolonlar çocuklarda ve bebeklerde kıkırdak toksisitesi nedeniyle KESİNLİKLE KULLANILMAZ."},
            {"text": "Aminoglikozidlerde günde tek doz uygulama nefrotoksisiteyi azaltır.", "isLie": False, "explanation": "Doğru. Ders notu ilkesidir."}
        ]),
        make_quiz("Florokinolon grubu antibiyotiklerin çocuklar ve gebe kadınlarda kullanılmasının kontrendike olmasının temel patolojik gerekçesi nedir?", [
            {"key": "A", "text": "Eklem kıkırdağı gelişimini olumsuz etkilemesi", "isCorrect": True, "explanation": "Ders notunda 'Çocuklar ve gebelerde kıkırdak gelişimini olumsuz etkilediğinden kullanılmamalıdır' kuralı yer almaktadır."},
            {"key": "B", "text": "Hastanın saçlarının anında dökülmesi", "isCorrect": False, "explanation": "Alakasızdır."},
            {"key": "C", "text": "Göz rengini yeşile çevirmesi", "isCorrect": False, "explanation": "Tıbbi temeli yoktur."},
            {"key": "D", "text": "Kalp kasını kemiğe dönüştürmesi", "isCorrect": False, "explanation": "Tıbbi saçmalıktır."}
        ])
    ]
    slides.append(make_slide(94, "Florokinolonlar ve Aminoglikozidler: Kıkırdak Toksisitesi ve Nefrotoksisite", "Florokinolon çocuk/gebe kıkırdak kontrendikasyonu, aminoglikozid nefrotoksisite ve tek doz", "Antibakteriyel Ajanlar", s94_narrative, s94_bullets, s94_elements))

    # Slide 95: Fosfomisin Trometamol ve Korunma İlkeleri
    s95_narrative = (
        "Fosfomisin trometamol, özgün etki mekanizması ve tek dozluk kullanım kolaylığı ile basit "
        "sistit tedavisinde yüksek hasta uyumu sağlayan modern bir antibiyotiktir.\n\n"
        "- **Bakteri Duvar Sentezi İnhibisyonu:** Fosfonik asit türevi olup, peptidoglikan sentezinin "
        "en erken basamağında yer alan fosfoenolpiruvat transferaz (MurA) enzimini geri dönüşümsüz inhibe eder.\n"
        "- **Kullanım Dozu ve Gebelik:** Komplike olmayan İYE'de **3 gramlık saşe formunda oral TEK DOZ** "
        "olarak kullanılır; gebelik kategorisi **B'dir** (gebelikte güvenle verilebilir).\n"
        "- **Korunma İlkeleri:** Cinsel aktif kadınlarda **ilişki sonrası miksiyon (idrar yapma)** "
        "ve postmenopozal kadınlarda vajinal laktobasilleri yeniden canlandıran **vajinal östrojen "
        "kullanımı** enfeksiyon rekürrensini belirgin şekilde önler.\n\n"
        "> [!IMPORTANT]\n"
        "> Fosfomisin 3 g tek doz saşedir ve gebelikte (Kategori B) güvenlidir; korunmada ilişki sonrası miksiyon ve vajinal östrojen esastır."
    )
    s95_bullets = [
        "Fosfomisin bakteri hücre duvar sentezini erken aşamada inhibe eder.",
        "Komplike olmayan sistitte 3 g tek doz saşe kullanılır; gebelik kategorisi B'dir.",
        "Korunmada cinsel ilişki sonrası miksiyon ve vajinal östrojen kullanımı önerilir."
    ]
    s95_elements = [
        make_cloze("Fosfomisin trometamolün gebelikte güvenli olduğunu gösteren gebelik kategorisi B'dir.", "B'dir", "Gebelikte güvenle kullanılabileceğini gösteren kategori"),
        make_table("Fosfomisin ve Korunma Stratejisi", ["Parametre", "Klinik Özellik / Yaklaşım", "Klinik Amaç"], [
            {"cells": [{"text": "Fosfomisin Dozu", "isMasked": False}, {"text": "3 gramlık tek doz saşe (oral)", "isMasked": True, "hint": "tek kullanımlık saşe"}, {"text": "Hızlı mesane konsantrasyonu ve hasta uyumu"}]},
            {"cells": [{"text": "Gebelik Kategorisi", "isMasked": False}, {"text": "Kategori B (güvenli)", "isMasked": False}, {"text": "Gebelerde komplike olmayan sistitte güvenle kullanım", "isMasked": True, "hint": "gebede güvenli profil"}]},
            {"cells": [{"text": "Davranışsal Korunma", "isMasked": False}, {"text": "İlişki sonrası miksiyon ve vajinal östrojen", "isMasked": False}, {"text": "Üretral bakteriyel yıkama ve laktobasil restorasyonu", "isMasked": False}]}
        ]),
        make_chain("Korunma ve Direnç Önleme Zinciri", [
            "1. İlaç Alımı: Fosfomisin 3 g saşe gece yatarken aç karnına içilir.",
            "2. Yüksek İdrar Düzeyi: İlaç idrarda 48 saat boyunca MİK değerinin çok üzerinde kalır.",
            "3. Davranışsal Destek: Kadına koitus sonrası hemen idrar yapması öğretilir.",
            "4. Hormonal Destek: Postmenopozal hastaya vajinal östrojen verilerek laktobasiller diriltilir."
        ]),
        make_recall("Fosfomisin trometamolün komplike olmayan sistitteki standart kullanım şekli, dozu ve gebelik kategorisi nedir?", "Oral 3 gram tek doz saşe olarak kullanılır; gebelik kategorisi B'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fosfomisin ve Korunma", [
            {"text": "Fosfomisin bakteri duvar sentezini inhibe eden bir antibiyotiktir.", "isLie": False, "explanation": "Doğru. MurA enzimini inhibe eder."},
            {"text": "Gebelikte kullanılabilen bir ilaç olup gebelik kategorisi B'dir.", "isLie": False, "explanation": "Doğru. Ders notu bilgisidir."},
            {"text": "Cinsel ilişki sonrası miksiyon yapılması idrar yollarını mikropla doldurup kesin sistit yapar.", "isLie": True, "explanation": "Tuzak! Koitus sonrası miksiyon bakterileri mekanik olarak dışarı süpürerek sistiti ÖNLER (koruyucudur)."},
            {"text": "Postmenopozal kadınlarda vajinal östrojen kullanımı rekürrensi önler.", "isLie": False, "explanation": "Doğru. Florayı yeniler."}
        ]),
        make_quiz("Fosfomisin trometamolün etki mekanizması ve klinik özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Bakteri duvar sentezini inhibe eder, 3 g tek doz saşe olarak kullanılır ve gebelik kategorisi B'dir", "isCorrect": True, "explanation": "Ders notunda Fosfomisin için bu özellikler birebir vurgulanmıştır."},
            {"key": "B", "text": "Bakterilerin DNA'sını değil sadece tırnaklarını boyar", "isCorrect": False, "explanation": "Tıbbi saçmalıktır."},
            {"key": "C", "text": "Gebelikte kullanıldığında kesinlikle bebeği zehirler", "isCorrect": False, "explanation": "Kategori B'dir, güvenlidir."},
            {"key": "D", "text": "Sadece 10 yıl kesintisiz içilerek etki eder", "isCorrect": False, "explanation": "Tek doz saşedir."}
        ])
    ]
    slides.append(make_slide(95, "Fosfomisin Trometamol ve Korunma İlkeleri", "Fosfomisin etki mekanizması, 3 g tek doz, Kategori B ve koit sonrası miksiyon", "Antibakteriyel Ajanlar", s95_narrative, s95_bullets, s95_elements))

    # Slide 96: Tekrarlayan ÜSE'de Bağışıklama: Uro-Vaxom ve Diğer Aşılar
    s96_narrative = (
        "Tekrarlayan sistit atakları geçiren kadınlarda sürekli antibiyotik kullanımının doğurduğu "
        "direnç riskini engellemek amacıyla immünomodülatör bağışıklama aşıları geliştirilmiştir.\n\n"
        "- **Kullanım Endikasyonu:** Bağışıklama ajanları, **yılda 3'ten fazla atak (yılda >3 atak)** "
        "geçiren, altta anatomik anomali bulunmayan komplike olmayan tekrarlayan ÜSE'li hastalarda endikedir.\n"
        "- **Uro-Vaxom (OM-89):** En yaygın ve kanıta dayalı oral aşıdır; **18 farklı E. coli suşunun** "
        "bakteriyel lizatından elde edilir; aç karnına günde 1 kapsül şeklinde 3 ay süreyle kullanılır.\n"
        "- **Diğer Bağışıklama Formları:** **Urovac** (vajinal aşı; 6 E. coli serotipi ve Proteus/Klebsiella "
        "içerir) ve **Uromune** (sublingual sprey; E. coli, Proteus, Klebsiella ve E. faecalis içerir).\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Uro-Vaxom (OM-89), 18 farklı E. coli suşunun liyofilize lizatını içeren oral aşıdır; yılda >3 atak geçiren tekrarlayan ÜSE'de kullanılır."
    )
    s96_bullets = [
        "Bağışıklama yılda >3 atak geçiren komplike olmayan tekrarlayan ÜSE'de kullanılır.",
        "Uro-Vaxom (OM-89) 18 E. coli suşu içeren oral liyofilize bakteriyel lizattır.",
        "Urovac vajinal, Uromune ise sublingual (dil altı) bağışıklama preparatlarıdır."
    ]
    s96_elements = [
        make_cloze("Tekrarlayan ÜSE profilaksisinde kullanılan oral bağışıklama ilacı Uro-Vaxom 18 farklı E. coli suşu lizatı içerir.", "Uro-Vaxom", "OM-89 oral bakteriyel lizat aşısı"),
        make_table("Üriner Sistem Bağışıklama Aşıları", ["Preparat Adı", "Uygulama Yolu", "İçerdiği Mikroorganizmalar"], [
            {"cells": [{"text": "Uro-Vaxom (OM-89)", "isMasked": False}, {"text": "Oral kapsül (aç karnına)", "isMasked": True, "hint": "ağızdan alınan form"}, {"text": "18 E. coli suşu lizatı"}]},
            {"cells": [{"text": "Uromune", "isMasked": False}, {"text": "Sublingual sprey (dil altı)", "isMasked": True, "hint": "dil altından emilen sprey"}, {"text": "E. coli, Proteus, Klebsiella, Enterokok"}]},
            {"cells": [{"text": "Urovac", "isMasked": False}, {"text": "Vajinal supozituvar", "isMasked": False}, {"text": "6 E. coli serotipi, P. vulgaris, K. pneumoniae", "isMasked": False}]}
        ]),
        make_chain("Uro-Vaxom Mukozal İmmün Yanıt Zinciri", [
            "1. Yutma: Kapsül aç karnına alınır ve Peyer plaklarına ulaşır.",
            "2. Antijen Sunumu: 18 E. coli antijeni bağırsak dendritik hücrelerince tanınır.",
            "3. Mukozal Göç: Aktive olan B lenfositler üriner traktus ürotelyumuna göç eder.",
            "4. Salgısal IgA Artışı: Mesanede salgısal IgA üretimi artarak bakteriyel tutunmayı bloke eder."
        ]),
        make_recall("Tekrarlayan ÜSE'de kullanılan oral bakteriyel lizat aşısı Uro-Vaxom (OM-89) kaç farklı E. coli suşunun lizatını içerir?", "18 farklı E. coli suşunun liyofilize lizatını içerir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bağışıklama ve Aşılar", [
            {"text": "Uro-Vaxom 18 E. coli suşunun liyofilize lizatını içeren oral bir aşıdır.", "isLie": False, "explanation": "Doğru. OM-89 içeriğidir."},
            {"text": "Bağışıklama yılda >3 atak geçiren tekrarlayan ÜSE'lerde kullanılır.", "isLie": False, "explanation": "Doğru. Temel endikasyondur."},
            {"text": "Uro-Vaxom içildiğinde hastanın mesanesi tamamen patlar ve hasta komaya girer.", "isLie": True, "explanation": "Tuzak! Uro-Vaxom son derece güvenli bir immünomodülatör aşıdır; mukozal IgA'yı artırır."},
            {"text": "Uromune dil altı (sublingual) uygulanan bir bakteriyel aşıdır.", "isLie": False, "explanation": "Doğru. Sublingual formdur."}
        ]),
        make_quiz("Yılda 3'ten fazla sistit atağı geçiren kadınlarda profilaksi amacıyla kullanılan ve 18 farklı E. coli suşu içeren oral bakteriyel aşı hangisidir?", [
            {"key": "A", "text": "Uro-Vaxom (OM-89)", "isCorrect": True, "explanation": "Ders notunda 'Uro-Vaxom (OM-89) (oral) (18 E. coli suşu)' açıkça belirtilmiştir."},
            {"key": "B", "text": "BCG aşısı", "isCorrect": False, "explanation": "Tüberküloz ve mesane kanseri aşısıdır."},
            {"key": "C", "text": "Kuduz aşısı", "isCorrect": False, "explanation": "Kuduz virüsüne yöneliktir."},
            {"key": "D", "text": "Tetanoz toksoidi", "isCorrect": False, "explanation": "Tetanoz toksinine yöneliktir."}
        ])
    ]
    slides.append(make_slide(96, "Tekrarlayan ÜSE'de Bağışıklama: Uro-Vaxom ve Diğer Aşılar", "Uro-Vaxom (OM-89), 18 E. coli suşu, yılda >3 atak endikasyonu ve Uromune/Urovac", "Bağışıklama", s96_narrative, s96_bullets, s96_elements))

    # Slide 97: Tıp Fakültesi Sınav Spotları: Etiyolojiden Laboratuvara
    s97_narrative = (
        "Dönem 3 Kurul 1 sınavlarında ve mezuniyet sonrası TUS'ta sorulan ÜSE sorularının temel "
        "omurgasını oluşturan birinci grup yüksek verimli spot bilgileri özetliyoruz.\n\n"
        "- **Tanım ve En Sık Etken:** ÜSE = İdrarda bakteri + konak enflamatuar reaksiyonu (piyüri). "
        "Vakaların %95'inde tek bakteri izole edilir; **en sık etken %70-90 ile Escherichia coli'dir**.\n"
        "- **Bulaş ve Yayılım:** Asendan yol **%99 ile ezici çoğunluktur**; hematojen yol (<%2) ise "
        "S. aureus, Salmonella, Candida ve Tbc ile renal kortikal apseler yapar.\n"
        "- **Kadın ve Erkek Dinamikleri:** 1-50 yaş erkekte insidans <%1'dir (uzun üretra ve prostat sıvısı korur). "
        "Neonatal dönem ise ÜSE'nin erkeklerde kızlardan sık görüldüğü tek dönemdir (E/K: 1,5/1).\n"
        "- **Laboratuvar Triadı:** **Lökosit esteraz → Piyüriyi; Nitrit → Bakteriüriyi; Lökosit silendiri → Böbrek hasarını** gösterir!\n\n"
        "> [!IMPORTANT]\n"
        "> [BÜYÜK SINAV SPOTU] E. coli %70-90; Asendan %99; Genç erkekte <%1; LE=Piyüri, Nitrit=Bakteriüri, Silendir=Böbrek hasarı!"
    )
    s97_bullets = [
        "En sık etken %70-90 E. coli; en sık yol %99 asendan yoldur.",
        "1-50 yaş erkekte <%1; neonatal dönemde E/K: 1,5/1 oranı vardır.",
        "LE = Piyüri, Nitrit = Bakteriüri, Lökosit silendiri = Böbrek hasarı."
    ]
    s97_elements = [
        make_cloze("Sınavların değişmez spotu: İdrarda lökosit silendiri görülmesi akut pyelonefrit ve böbrek hasarı kanıtıdır.", "böbrek hasarı", "Renal parankimal enflamasyon hasarı"),
        make_table("Tıp Fakültesi Sınav Spotları Paneli 1", ["Soru Konusu", "Doğru Sınav Cevabı", "Klasik Sınav Çeldiricisi"], [
            {"cells": [{"text": "En Sık Üropatojen", "isMasked": False}, {"text": "Escherichia coli (%70-90)", "isMasked": True, "hint": "açık ara birinci bakteri"}, {"text": "Pseudomonas veya Proteus"}]},
            {"cells": [{"text": "En Sık Yayılım Yolu", "isMasked": False}, {"text": "Asendan yol (%99)", "isMasked": False}, {"text": "Hematojen yol (çeldirici)", "isMasked": True, "hint": "hematojen sadece <%2'dir"}]},
            {"cells": [{"text": "Piyüriyi Gösteren Test", "isMasked": False}, {"text": "Lökosit esteraz testi", "isMasked": True, "hint": "piyüri belirteci"}, {"text": "Nitrit testi (bakteriüriyi gösterir)"}]}
        ]),
        make_chain("Sınav Soru Çözüm Akışı", [
            "1. Soru Kökü: 'Piyüriyi gösteren test hangisidir?'",
            "2. Çeldirici Analizi: Nitrit bakteriüriyi, silendir tübülü gösterir.",
            "3. Doğru Hamle: Lökosit esteraz işaretlenir (tam puan).",
            "4. Doğrulama: Normal idrarda negatif olduğu hatırlanır."
        ]),
        make_recall("Tıp fakültesi kurul sınavlarının en klasik sorusu: İdrar analizinde piyüriyi gösteren test hangisidir?", "Lökosit esteraz testidir (nitrit ise bakteriüriyi gösterir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sınav Spotları 1", [
            {"text": "ÜSE'lerde en sık izole edilen üropatojen %70-90 ile E. coli'dir.", "isLie": False, "explanation": "Doğru. Kesin sınav spotudur."},
            {"text": "Lökosit silendirleri böbrek hasarını gösterir.", "isLie": False, "explanation": "Doğru. Pyelonefrit bulgusudur."},
            {"text": "İdrar yolu enfeksiyonu erkeklerde kadınlardan 50 kat daha sıktır.", "isLie": True, "explanation": "Tuzak! Kadınlarda çok daha sıktır; olguların %67,5'i kadındır ve yaşam boyu risk %50'dir."},
            {"text": "Asendan yol enfeksiyonların %99'unu oluşturur.", "isLie": False, "explanation": "Doğru. Temel yoldur."}
        ]),
        make_quiz("Tıp fakültesi kurul sınavlarında sıkça sorulan aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Lökosit esteraz → Piyüri | E. coli → En sık etken | Asendan yol → %99", "isCorrect": True, "explanation": "Ders notundaki tüm kardinal sınav spotlarını içeren mükemmel eşleştirmedir."},
            {"key": "B", "text": "Nitrit → Piyüri | S. aureus → En sık etken", "isCorrect": False, "explanation": "Tamamen hatalıdır."},
            {"key": "C", "text": "Asendan yol → Sadece %0,01", "isCorrect": False, "explanation": "%99'dur."},
            {"key": "D", "text": "Genç erkekte ÜSE sıklığı → %99", "isCorrect": False, "explanation": "<%1'dir."}
        ])
    ]
    slides.append(make_slide(97, "Tıp Fakültesi Sınav Spotları: Etiyolojiden Laboratuvara", "E. coli %70-90, asendan %99, genç erkekte <%1, LE piyüri ve lökosit silendiri", "Sınav Spotları", s97_narrative, s97_bullets, s97_elements))

    # Slide 98: Tıp Fakültesi Sınav Spotları: Klinik ve Tedavi Kuralları
    s98_narrative = (
        "Dönem 3 Kurul 1 ve TUS sınavlarında tedavi ve klinik ayırıcı tanı konusunda sorulan "
        "ikinci grup yüksek verimli spot kuralları özetliyoruz.\n\n"
        "- **Büyük Ateş Tuzağı:** Ateş yüksekliği bir komplike edici faktör DEĞİL, enfeksiyonun sistemik "
        "**klinik bulgusudur** (Kurul 1 çıkmış sorusu).\n"
        "- **Kadında Risk Tuzağı:** Kadınlarda postmenopozal risk faktörü östrojen fazlalığı değil, "
        "**östrojen EKSİKLİĞİDİR** (Kurul 1 çıkmış sorusu).\n"
        "- **Cerrahi Kararlar:** Diyabetik amfizematöz pyelonefritte **nefrektomi**; 3-4. günde ateşi "
        "düşmeyen renal absede **drenaj** uygulanır.\n"
        "- **İlaç Yasakları:** TMP-SMX gebelerde ve warfarinde; Nitrofurantoin komplike/üst sistemde "
        "ve CrCl <50'de; Florokinolonlar ise çocuklar ve gebelerde kıkırdak hasarı nedeniyle kontrendikedir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÜYÜK SINAV SPOTU] Ateş = Klinik bulgu! Postmenopozal risk = Östrojen eksikliği! Amfizematöz = Nefrektomi! Kinolon çocukta = Kıkırdak hasarı!"
    )
    s98_bullets = [
        "Ateş bir klinik bulgudur; komplike edici faktör DEĞİLDİR.",
        "Kadında risk faktörü östrojen fazlalığı değil, ÖSTROJEN EKSİKLİĞİDİR.",
        "Amfizematöz pyelonefritte nefrektomi; florokinolonlar çocukta kontrendikedir."
    ]
    s98_elements = [
        make_cloze("Sınavların kardinal kuralı: Kadınlarda ÜSE risk faktörü olan durum östrojen eksikliği olup östrojen fazlalığı değildir.", "östrojen eksikliği", "Menopozal laktobasil kaybı yaratan hormon yetersizliği"),
        make_table("Tıp Fakültesi Sınav Spotları Paneli 2", ["Sınav Sorusu Odak", "Doğru Tıbbi Kabul", "Klasik Sınav Çeldiricisi"], [
            {"cells": [{"text": "Komplike Faktör Olmayan", "isMasked": False}, {"text": "Ateş yüksekliği olması (Klinik bulgudur)", "isMasked": True, "hint": "komplike edici olmayan seçenek"}, {"text": "Erkek cinsiyet veya böbrek taşı"}]},
            {"cells": [{"text": "Kadında Risk Faktörü Olmayan", "isMasked": False}, {"text": "Östrojen fazlalığı (Doğrusu eksikliktir)", "isMasked": True, "hint": "risk faktörü olmayan hormonal durum"}, {"text": "Üretranın kısa olması veya gebelik"}]},
            {"cells": [{"text": "Amfizematöz Cerrahi", "isMasked": False}, {"text": "Nefrektomi uygulanması", "isMasked": False}, {"text": "Sadece 3 günlük oral şurup", "isMasked": True, "hint": "yetersiz medikal çeldirici"}]}
        ]),
        make_chain("Sınav Çıkmış Soru Mantığı", [
            "1. Soru: 'Aşağıdakilerden hangisi komplike edici faktör değildir?'",
            "2. Şıklar: Erkek, gebe, taş, diyabet, ateş.",
            "3. Analiz: İlk dördü zemin faktörüdür; ateş ise hastalığın sonucudur.",
            "4. Doğru Cevap: 'Ateş yüksekliği' işaretlenir."
        ]),
        make_recall("Kurul 1 çıkmış sorularında geçen 'ÜSE için komplike edici faktör olmayan durum' ile 'kadında risk faktörü olmayan hormonal durum' nedir?", "Komplike edici olmayan durum: Ateş yüksekliği (klinik bulgudur); Risk faktörü olmayan durum: Östrojen fazlalığıdır (doğrusu östrojen eksikliğidir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sınav Spotları 2", [
            {"text": "Ateş yüksekliği komplike edici faktör değil, klinik bir bulgudur.", "isLie": False, "explanation": "Doğru. Çıkmış sınav sorusudur."},
            {"text": "Kadınlarda ÜSE için risk faktörü östrojen fazlalığı değil, östrojen eksikliğidir.", "isLie": False, "explanation": "Doğru. Çıkmış sınav sorusudur."},
            {"text": "Amfizematöz pyelonefritte hiçbir şey yapılmaz, böbrek asla ameliyat edilmez.", "isLie": True, "explanation": "Tuzak! Amfizematöz pyelonefritte definitif cerrahi tedavi nefrektomidir."},
            {"text": "Florokinolonlar kıkırdak hasarı nedeniyle çocuklar ve gebelerde kontrendikedir.", "isLie": False, "explanation": "Doğru. Temel farmakolojik kuraldır."}
        ]),
        make_quiz("Dönem 3 Kurul 1 çıkmış sorularına göre aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Ateş yüksekliği komplike edici faktör değil klinik bulgudur; kadında risk faktörü ise östrojen eksikliğidir", "isCorrect": True, "explanation": "Kurul 1 çıkmış iki ayrı sorusunun birleştirilmiş kesin doğru analizidir."},
            {"key": "B", "text": "Ateş yüksekliği en önemli yapısal anatomik anomalidir", "isCorrect": False, "explanation": "Ateş bulgudur, anomali değildir."},
            {"key": "C", "text": "Östrojen fazlalığı menopozdaki kadınların %100'ünde sistit yapar", "isCorrect": False, "explanation": "Menopozda östrojen eksiktir."},
            {"key": "D", "text": "Piyüriyi nitrit testi gösterir", "isCorrect": False, "explanation": "Piyüriyi lökosit esteraz gösterir."}
        ])
    ]
    slides.append(make_slide(98, "Tıp Fakültesi Sınav Spotları: Klinik ve Tedavi Kuralları", "Ateşin bulgu olması, östrojen eksikliği, amfizematöz nefrektomi ve ilaç kontrendikasyonları", "Sınav Spotları", s98_narrative, s98_bullets, s98_elements))

    # Slide 99: Çıkmış Sınav Soruları Analizi (Kurul 1)
    s99_narrative = (
        "Ders notunun sonunda yer alan ve amfi sınavlarında birebir sorulmuş resmi tıp fakültesi "
        "sorularının pedagojik mekanizmalarını çözümlüyoruz.\n\n"
        "- **Çıkmış Soru 1 (Kadında Risk Faktörleri):** Kadınlarda asendan yol üretranın kısa olması, "
        "anüse yakınlık ve prostat sıvısının olmamasıyla kolaylaşır. Premenopozal dönemde gebelik ve "
        "düşük sosyoekonomik durum risktir. Postmenopozal dönemde risk faktörü **östrojen eksikliğidir** "
        "(laktobasil kaybı); **ÖSTROJEN FAZLALIĞI RİSK FAKTÖRÜ DEĞİLDİR** (Doğru Cevap: A).\n"
        "- **Çıkmış Soru 2 (Komplike Edici Faktörler):** Erkek cinsiyet, kontrolsüz DM, nörojenik "
        "mesane ve nefrolitiazis komplike faktörlerdir. **ATEŞ YÜKSEKLİĞİ komplike edici faktör değil, "
        "enfeksiyonun bir klinik bulgusudur** (Doğru Cevap: A).\n"
        "- **Çıkmış Soru 3 (Piyüri Belirteci):** İdrar analizinde lökosit varlığını (piyüriyi) gösteren "
        "dipstik testi **LÖKOSİT ESTERAZ TESTİDİR**; nitrit bakteriüriyi gösterir (Doğru Cevap: A).\n"
        "- **Çıkmış Soru 4 (Tüberküloz İlacı Olmayan):** Pirazinamid, etambutol, izoniazid ve streptomisin "
        "tüberküloz ilacıdır; **MİSOPROSTOL tüberküloz ilacı değildir** (prostaglandin analoğudur) (Doğru Cevap: C).\n\n"
        "> [!IMPORTANT]\n"
        "> Kurul 1 çıkmış sorularında 4 soru 4 net: 1) Kadında risk olmayan = Östrojen fazlalığı! 2) Komplike edici olmayan = Ateş yüksekliği! 3) Piyüriyi gösteren = Lökosit esteraz! 4) Tbc ilacı olmayan = Misoprostol!"
    )
    s99_bullets = [
        "Soru 1: Kadında risk faktörü olmayan → Östrojen fazlalığı (doğrusu eksikliktir).",
        "Soru 2: Komplike edici faktör olmayan → Ateş yüksekliği (klinik bulgudur).",
        "Soru 3: Piyüriyi gösteren dipstik testi → Lökosit esteraz testi.",
        "Soru 4: Tüberküloz tedavisinde kullanılmayan ilaç → Misoprostol."
    ]
    s99_elements = [
        make_cloze("Kurul 1 çıkmış sorusu: Tüberküloz tedavisinde kullanılmayan ilaç misoprostol olarak sorulmuştur.", "misoprostol", "Prostaglandin analoğu mide ve doğum ilacı"),
        make_table("Kurul 1 Çıkmış Sorular Çözüm Tablosu", ["Soru Konusu", "Doğru Cevap", "Patofizyolojik Gerekçe"], [
            {"cells": [{"text": "Kadında Risk Faktörü Olmayan", "isMasked": False}, {"text": "Östrojen fazlalığı", "isMasked": True, "hint": "hormon fazlalığı şıkkı"}, {"text": "Risk yaratan durum postmenopozal östrojen EKSİKLİĞİDİR"}]},
            {"cells": [{"text": "Komplike Edici Faktör Olmayan", "isMasked": False}, {"text": "Ateş yüksekliği olması", "isMasked": True, "hint": "klinik bulgu olan şık"}, {"text": "Ateş bir zemin faktörü değil, sistemik klinik bulgudur"}]},
            {"cells": [{"text": "Piyüriyi Gösteren Test", "isMasked": False}, {"text": "Lökosit esteraz testi", "isMasked": True, "hint": "piyüri testi şıkkı"}, {"text": "Nötrofil enzimini saptar; nitrit bakteriüriyi gösterir"}]},
            {"cells": [{"text": "Tbc İlacı Olmayan Ajan", "isMasked": False}, {"text": "Misoprostol", "isMasked": False}, {"text": "PGE1 analoğudur, antitüberküloz aktivitesi yoktur", "isMasked": False}]}
        ]),
        make_chain("Dört Çıkmış Soru Çözüm Analizi", [
            "1. Soru 1: 'Kadında risk faktörü değildir?' → Östrojen fazlalığı (eksiklik olmalıydı).",
            "2. Soru 2: 'Komplike edici faktör değildir?' → Ateş yüksekliği (bu bir bulgudur).",
            "3. Soru 3: 'Piyüriyi gösteren parametre?' → Lökosit esteraz (LE=piyüri).",
            "4. Soru 4: 'Tüberküloz ilacı değildir?' → Misoprostol (prostaglandindir)."
        ]),
        make_recall("Dönem 3 Kurul 1 çıkmış sınav sorularında yer alan 4 kardinal cevap hangileridir?", "1) Östrojen fazlalığı (risk değildir), 2) Ateş yüksekliği (komplike faktör değildir), 3) Lökosit esteraz (piyüriyi gösterir), 4) Misoprostol (Tbc ilacı değildir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Çıkmış Soru Analizi", [
            {"text": "Kadınlarda östrojen fazlalığı ÜSE için risk faktörü değildir (eksiklik risktir).", "isLie": False, "explanation": "Doğru. Çıkmış soru 1."},
            {"text": "Ateş yüksekliği komplike edici faktör değil, klinik bir bulgudur.", "isLie": False, "explanation": "Doğru. Çıkmış soru 2."},
            {"text": "Lökosit esteraz testi idrarda şeker ve protein miktarını ölçen bir testtir.", "isLie": True, "explanation": "Tuzak! Lökosit esteraz testi idrarda PİYÜRİYİ (lökosit varlığını) gösterir (Çıkmış soru 3)."},
            {"text": "Misoprostol bir tüberküloz ilacı değildir.", "isLie": False, "explanation": "Doğru. Çıkmış soru 4."}
        ]),
        make_quiz("Aşağıdaki seçeneklerden hangisi Dönem 3 Kurul 1 çıkmış sorularının doğru cevaplarıyla BİREBİR örtüşür?", [
            {"key": "A", "text": "Risk olmayan: Östrojen fazlalığı | Komplike olmayan: Ateş | Piyüriyi gösteren: Lökosit esteraz", "isCorrect": True, "explanation": "Ders notundaki çıkmış soruların resmi ve kesin çözümleridir."},
            {"key": "B", "text": "Risk olmayan: Kısa üretra | Komplike olmayan: Böbrek taşı", "isCorrect": False, "explanation": "Kısa üretra ve taş gerçek risklerdir."},
            {"key": "C", "text": "Piyüriyi gösteren: İdrarın kokusu", "isCorrect": False, "explanation": "Piyüriyi lökosit esteraz gösterir."},
            {"key": "D", "text": "Komplike edici olmayan: Erkek cinsiyet", "isCorrect": False, "explanation": "Erkek cinsiyet komplike faktördür."}
        ])
    ]
    slides.append(make_slide(99, "Çıkmış Sınav Soruları Analizi (Kurul 1)", "Çıkmış 4 soru analizi: Östrojen fazlalığı, ateş yüksekliği, lökosit esteraz ve misoprostol", "Sınav Soruları", s99_narrative, s99_bullets, s99_elements))

    # Slide 100: [TEKRAR SAYFASI - CHECKPOINT 10] Deste 51 Büyük Final Tekrarı ve Konsolidasyon
    s100_narrative = (
        "Tebrikler! 100 slaytlık TIP 310 Üriner Sistem Enfeksiyonları: Laboratuvar Bulguları ve Tedavi "
        "destesini başarıyla tamamladınız. Bu büyük final checkpoint'inde destenin tüm omurgasını özetliyoruz.\n\n"
        "- **Bölüm 1-3 (Tanım, Riskler ve Bulaş):** ÜSE = Bakteri + Enflamatuar reaksiyon (piyüri). "
        "Vakaların %99'u asendan yolla oluşur (kadında kısa üretra, anüse yakınlık). Hematojen yol (<%2) "
        "S. aureus, Salmonella, Tbc ve Candida ile ilişkilidir. Genç erkekte <%1; postmenopozda risk östrojen eksikliğidir.\n"
        "- **Bölüm 4-6 (Etkenler, Komplike ÜSE ve Relaps):** En sık etken %70-90 E. coli; Proteus üreazla "
        "struvit taşı yapar; Adenovirus 11 çocukta hemorajik sistit yapar. Ateş bir klinik bulgudur! "
        "Amfizematözde nefrektomi; absede drenaj uygulanır. Relaps (≤2 hafta, aynı bakteri) en az 4 hafta "
        "tedavi edilir; ASB genel kural olarak tedavi edilmez (gebeler ve cerrahi mutlak istisnadır).\n"
        "- **Bölüm 7-10 (Tanı, Laboratuvar ve Antibiyotikler):** Suprapubik aspirasyon altın standarttır. "
        "Nitrit için mesanede en az 4 saat bekleme gerekir. LE = Piyüri, Nitrit = Bakteriüri, Lökosit "
        "silendiri = Böbrek hasarı! Sistit 3 gün/tek doz (Fosfomisin); Komplike sistit 7 gün; Pyelonefrit "
        "kinolonla 7 gün, kinolon dışıyla 14 gündür. TMP-SMX gebede/warfarinde; Kinolon çocukta kıkırdak hasarı nedeniyle kontrendikedir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÜYÜK FİNAL KONSOLİDASYONU] Deste 51'in 100 adımlık tıbbi akışı: Patogenezden laboratuvara, ayırıcı tanıdan farmakolojiye tam ve eksiksiz amfi standardında tamamlanmıştır!"
    )
    s100_bullets = [
        "E. coli %70-90; Asendan yol %99; Genç erkekte <%1; Postmenopozda risk östrojen eksikliğidir.",
        "Ateş bir klinik bulgudur; amfizematözde nefrektomi; relapsta en az 4 hafta tedavi verilir.",
        "Suprapubik aspirasyon altın standart; LE=Piyüri, Nitrit=Bakteriüri, Silendir=Böbrek hasarıdır.",
        "Süreler: Sistit 3 gün/tek doz | Komplike sistit 7 gün | Pyelonefrit 7-14 gün | Relaps 4 haftadır."
    ]
    s100_elements = [
        make_cloze("Deste 51 Final Özeti: İdrar analizinde piyüriyi lökosit esteraz gösterirken böbrek hasarını lökosit silendirleri kanıtlar.", "lökosit silendirleri", "Tübüllerde oluşan proteinöz lökosit kalıpları"),
        make_table("Deste 51 Büyük Final Tablosu", ["Alan / Parametre", "Kardinal Tıbbi Veri", "Kesin Sınav Kararı"], [
            {"cells": [{"text": "Etiyoloji ve Bulaş", "isMasked": False}, {"text": "E. coli (%70-90) ve Asendan yol (%99)", "isMasked": True, "hint": "en sık mikrop ve en sık yol"}, {"text": "Monomikrobiyal fekal kolonizasyon"}]},
            {"cells": [{"text": "Laboratuvar Triadı", "isMasked": False}, {"text": "LE=Piyüri | Nitrit=Bakteriüri | Silendir=Hasar", "isMasked": True, "hint": "üç büyük laboratuvar karşılığı"}, {"text": "İkisi negatifse İYE'den uzaklaşılır"}]},
            {"cells": [{"text": "Cerrahi Kararlar", "isMasked": False}, {"text": "Amfizem=Nefrektomi | Abse=Drenaj", "isMasked": False}, {"text": "Mortaliteyi önleyici acil girişimler", "isMasked": True, "hint": "cerrahi kurtarma müdahaleleri"}]},
            {"cells": [{"text": "Tedavi Süreleri", "isMasked": False}, {"text": "Sistit 3g/tek doz | Komplike 7g | Pyelo 14g | Relaps 4hf", "isMasked": False}, {"text": "Endikasyona göre basamaklı süre kuralı", "isMasked": False}]}
        ]),
        make_chain("100 Adımlık Büyük Klinik Akış", [
            "1. Bulaş: Fekal E. coli kısa kadın üretrasından asendan yolla tırmanır.",
            "2. Tanı: İdrar analizinde lökosit esteraz ve nitrit pozitifliği ile mm³'de >10 lökosit saptanır.",
            "3. Ayrım: Ateş yoksa sistit (Fosfomisin 3 g); ateş ve KVAH varsa pyelonefrit (14 gün) teşhis edilir.",
            "4. Cerrahi ve Takip: Gaz varsa nefrektomi; relapsta 4 hafta tedavi ve odak temizliği yapılır."
        ]),
        make_recall("Deste 51'in en kritik 3 sayısal kuralı nedir? (E. coli oranı, asendan yayılım oranı ve komplike sistit süresi)", "E. coli oranı %70-90; asendan yayılım oranı %99; komplike sistit tedavi süresi ise 7 gündür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Deste 51 Final Özeti", [
            {"text": "ÜSE olgularında en sık etken %70-90 ile E. coli ve en sık yol %99 ile asendan yoldur.", "isLie": False, "explanation": "Doğru. Deste omurgasıdır."},
            {"text": "Ateş yüksekliği bir komplike edici faktör değil, enfeksiyonun klinik bir bulgusudur.", "isLie": False, "explanation": "Doğru. En klasik sınav kuralıdır."},
            {"text": "Florokinolonlar 1 günlük bebeklerde ve gebelerde en güvenli ilk tercihtir.", "isLie": True, "explanation": "Tuzak! Florokinolonlar çocuklar ve gebelerde kıkırdak hasarı nedeniyle KESİNLİKLE KONTRENDİKEDİR."},
            {"text": "Lökosit silendirleri böbrek parankim hasarını kanıtlar.", "isLie": False, "explanation": "Doğru. Pyelonefrit göstergesidir."}
        ]),
        make_quiz("Deste 51'in tamamını özetleyen aşağıdaki ifadelerden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Akut pyelonefritte kinolon dışı ilaçlarla tedavi süresi sadece 1 gündür ve ateş bir anatomik anomalidir", "isCorrect": True, "explanation": "Kesinlikle yanlış! Pyelonefritte kinolon dışı tedavi süresi 14 gündür ve ateş anatomik anomali veya komplike faktör değil, sistemik bir klinik bulgudur."},
            {"key": "B", "text": "Suprapubik aspirasyon idrar kültürü için kontaminasyonsuz altın standarttır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Asemptomatik bakteriüri sadece gebelerde ve invaziv cerrahi planlananlarda tedavi edilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Lökosit esteraz piyüriyi, nitrit ise bakteriüriyi gösterir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(100, "[TEKRAR SAYFASI - CHECKPOINT 10] Deste 51 Büyük Final Tekrarı ve Konsolidasyon", "Deste 51'in 100 slaytlık büyük konsolidasyonu: etiyoloji, tanı, laboratuvar, tedavi ve sınav spotları", "Büyük Final Tekrarı", s100_narrative, s100_bullets, s100_elements))

    return slides
