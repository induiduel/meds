# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec2():
    slides = []

    # Slide 11: Genel Risk Faktörleri ve İntrensek/Ekstrensek Yatkınlık
    s11_narrative = (
        "Üriner sistem enfeksiyonunun gelişimi, konağın anatomik bütünlüğünü ve fizyolojik idrar "
        "akımını bozan intrensek veya iyatrojenik faktörlerle doğrudan ilişkilidir.\n\n"
        "- **İyatrojenik Girişimler:** Üretral kateterizasyon, ürolojik enstrümantasyon (sistoskopi vb.) "
        "ve cerrahi girişimler steril üriner lümene dışarıdan bakteri inokülasyonuna yol açar.\n"
        "- **Mekanik Engeller:** Üriner traktusta gelişen taş (nefrolitiazis) veya tümöral obstrüksiyonlar "
        "akımı bloke ederek mikroorganizmaların yıkanıp atılmasını engeller.\n"
        "- **Nörolojik ve Konjenital Nedenler:** Nörojenik mesane, vezikoüreteral reflü (VUR) ve böbrek nakli "
        "gibi durumlar genel risk faktörlerinin en ağır anatomik ve fonksiyonel bileşenleridir.\n\n"
        "> [!NOTE]\n"
        "> Üriner sistemde serbest ve laminar idrar akımını bozan her türlü yabancı cisim veya obstrüksiyon ÜSE riskini katlar."
    )
    s11_bullets = [
        "Kateterizasyon ve ürolojik girişimler dışarıdan inokülasyon riskidir.",
        "Taş ve tümör gibi obstrüksiyonlar idrar akımını kesintiye uğratır.",
        "Nörojenik mesane, VUR ve böbrek nakli majör genel predispozan durumlardır."
    ]
    s11_elements = [
        make_cloze("Üriner sistemde obstrüksiyon yaratan taş ve tümörler idrar stazı oluşturarak ÜSE riskini belirgin artırır.", "obstrüksiyon", "İdrar yollarında mekanik tıkanıklık oluşumu"),
        make_table("Genel ÜSE Risk Faktörleri", ["Kategori", "Örnek Faktörler", "Patojenik Etki"], [
            {"cells": [{"text": "İyatrojenik / Girişimsel", "isMasked": False}, {"text": "Üretral kateterizasyon, sistoskopi", "isMasked": True, "hint": "sonda ve aletli müdahaleler"}, {"text": "Üretral bariyerin aşılması ve bakteriyel giriş"}]},
            {"cells": [{"text": "Mekanik Obstrüksiyon", "isMasked": False}, {"text": "Nefrolitiazis (taş), tümör", "isMasked": False}, {"text": "İdrar akımının durması ve staz", "isMasked": True, "hint": "idrarın göllenmesi ve boşalamaması"}]},
            {"cells": [{"text": "Fonksiyonel / İmmün", "isMasked": False}, {"text": "Nörojenik mesane, VUR, böbrek nakli", "isMasked": False}, {"text": "Rezistans kaybı ve reflü ile yukarı yayılım", "isMasked": True, "hint": "idrarın böbreğe geri kaçması"}]}
        ]),
        make_chain("Obstrüksiyon Kaynaklı ÜSE Mekanizması", [
            "1. Tıkanıklık: Üriner kanalda taş veya kitle idrar lümenini daraltır.",
            "2. Hidrostatik Basınç Artışı: Proksimalde idrar birikir ve staz gelişir.",
            "3. Yıkama Kaybı: İdrarın laminar akışı ile bakterilerin atılması durur.",
            "4. Kolonizasyon ve İnvazyon: Bakteriler hızla çoğalarak ürotelyumu infiltre eder."
        ]),
        make_recall("ÜSE gelişiminde rol oynayan başlıca genel ve iyatrojenik risk faktörleri nelerdir?", "Üretral kateterizasyon, taş ve tümör gibi obstrüksiyonlar, ürolojik enstrümantasyon, nörolojik mesane, VUR ve böbrek naklidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Genel Risk Faktörleri", [
            {"text": "Üretral kateterizasyon ÜSE için önemli bir iyatrojenik risk faktörüdür.", "isLie": False, "explanation": "Doğru. En sık kateter ilişkili enfeksiyon nedenidir."},
            {"text": "Üriner sistemde taş ve tümör gibi obstrüksiyonlar enfeksiyon riskini artırır.", "isLie": False, "explanation": "Doğru. Staz ve bakteri çoğalması yaratır."},
            {"text": "Vezikoüreteral reflü (VUR) idrarı tamamen sterilize ederek ÜSE'yi imkansız kılar.", "isLie": True, "explanation": "Tuzak! VUR, enfekte idrarın böbreğe geri kaçmasını sağlayarak pyelonefrit ve hasar riskini katlar."},
            {"text": "Böbrek nakli yapılmış immünsuprese hastalarda ÜSE riski yüksektir.", "isLie": False, "explanation": "Doğru. Nakil hastaları yüksek risklidir."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE gelişiminde tanımlanan genel risk faktörlerinden biri DEĞİLDİR?", [
            {"key": "A", "text": "Üretral kateterizasyon ve ürolojik girişimler", "isCorrect": False, "explanation": "Majör genel risk faktörüdür."},
            {"key": "B", "text": "Üriner sistemde obstrüksiyon oluşturan taş veya tümör", "isCorrect": False, "explanation": "Majör genel risk faktörüdür."},
            {"key": "C", "text": "Düzenli ve kesintisiz laminar idrar akımı bulunması", "isCorrect": True, "explanation": "Laminar ve kesintisiz idrar akımı bir risk faktörü değil, en güçlü doğal koruyucu konak savunmasıdır."},
            {"key": "D", "text": "Nörojenik mesane ve vezikoüreteral reflü", "isCorrect": False, "explanation": "Majör genel risk faktörüdür."}
        ])
    ]
    slides.append(make_slide(11, "Genel Risk Faktörleri ve İntrensek/Ekstrensek Yatkınlık", "Kateterizasyon, obstrüksiyon, taş, nörojenik mesane ve VUR", "Risk Faktörleri", s11_narrative, s11_bullets, s11_elements))

    # Slide 12: Sistemik ve Lokal Predispozan Faktörler
    s12_narrative = (
        "ÜSE yatkınlığı, konak dokusunun hücresel ve immünolojik direncini kıran sistemik hastalıklar "
        "ile üriner traktusun lokal mekanik patolojilerinin etkileşimiyle belirlenir.\n\n"
        "- **Sistemik Predispozan Faktörler:** En başta **Diabetes Mellitus (DM)** gelir; glukozüri "
        "bakteri çoğalmasını hızlandırırken nöropati mesane boşalmasını bozar. İmmünosüpresyon ve malnütrisyon "
        "lökosit fagositozunu baskılar.\n"
        "- **Lokal Predispozan Faktörler:** Organik veya fonksiyonel obstrüksiyon, **üriner staz**, "
        "yabancı cisimler (kateter, taş), tümör, nekrotik doku odakları ve travmadır.\n"
        "- **Biyolojik Sonuç:** Lokal bariyerin bozulması ve staz, sistemik immün yanıtsızlıkla birleştiğinde "
        "komplike ve dirençli enfeksiyonların gelişimine zemin hazırlar.\n\n"
        "> [!IMPORTANT]\n"
        "> Sistemik faktörlerin başında Diabetes Mellitus (glukozüri + nöropati); lokal faktörlerin başında ise üriner staz ve yabancı cisim gelir."
    )
    s12_bullets = [
        "Sistemik faktörler: DM, immünosüpresyon ve malnütrisyon.",
        "Lokal faktörler: Üriner staz, obstrüksiyon, yabancı cisim (kateter/taş), tümör ve travma.",
        "Diyabette glukozüri ve nörojenik mesane çifte yatkınlık yaratır."
    ]
    s12_elements = [
        make_cloze("Sistemik predispozan faktörler arasında en sık görülen endokrin patoloji Diabetes Mellitus olup enfeksiyon riskini katlar.", "Diabetes Mellitus", "Şeker hastalığı"),
        make_table("Sistemik ve Lokal Predispozan Faktör Ayrımı", ["Predispozan Sınıf", "Öne Çıkan Faktörler", "Fizyopatolojik Mekanizma"], [
            {"cells": [{"text": "Sistemik Faktörler", "isMasked": False}, {"text": "DM, immünosüpresyon, malnütrisyon", "isMasked": True, "hint": "vücut genelini etkileyen hastalıklar"}, {"text": "Hücresel immün yetersizlik, nöropati, glukozüri"}]},
            {"cells": [{"text": "Lokal Faktörler", "isMasked": False}, {"text": "Staz, VUR, yabancı cisim (kateter, taş)", "isMasked": False}, {"text": "Mekanik temizlenmenin engellenmesi", "isMasked": True, "hint": "yerel yıkama fonksiyonunun bozulması"}]}
        ]),
        make_recall("ÜSE'ye zemin hazırlayan sistemik ve lokal faktörlere üçer örnek veriniz.", "Sistemik: DM, immünosüpresyon, malnütrisyon. Lokal: Üriner staz, yabancı cisim (taş/kateter), organik/fonksiyonel obstrüksiyon."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sistemik ve Lokal Faktörler", [
            {"text": "Diabetes Mellitus, ÜSE için en önemli sistemik predispozan faktörlerdendir.", "isLie": False, "explanation": "Doğru. Nöropati ve glukozüri ile riski artırır."},
            {"text": "Üriner staz ve yabancı cisim (taş/kateter) lokal predispozan faktörlerdendir.", "isLie": False, "explanation": "Doğru. Bakteri üremesini kolaylaştırır."},
            {"text": "İmmünosüpresyon ve malnütrisyon hastayı ÜSE'ye karşı tam dirençli ve bağışık kılar.", "isLie": True, "explanation": "Tuzak! İmmünosüpresyon lökosit yanıtını felç ederek enfeksiyona yatkınlık yaratır."},
            {"text": "Vezikoüreteral reflü lokal bir faktör olarak üst sisteme yayılımı kolaylaştırır.", "isLie": False, "explanation": "Doğru. Reflü lokal predispozandır."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE gelişimine zemin hazırlayan SİSTEMİK predispozan faktörlerden biridir?", [
            {"key": "A", "text": "Diabetes Mellitus (DM)", "isCorrect": True, "explanation": "DM, immünosüpresyon ve malnütrisyon sistemik faktörlerdir; taş, staz ve kateter ise lokal faktörlerdir."},
            {"key": "B", "text": "Mesane taşı (kalkül)", "isCorrect": False, "explanation": "Lokal predispozan faktördür."},
            {"key": "C", "text": "Üretral foley kateter varlığı", "isCorrect": False, "explanation": "Lokal yabancı cisimdir."},
            {"key": "D", "text": "Vezikoüreteral reflü (VUR)", "isCorrect": False, "explanation": "Lokal anatomik patolojidir."}
        ])
    ]
    slides.append(make_slide(12, "Sistemik ve Lokal Predispozan Faktörler", "DM, immünosüpresyon, malnütrisyon, staz, taş ve kateter mekanizmaları", "Risk Faktörleri", s12_narrative, s12_bullets, s12_elements))

    # Slide 13: Premenopozal Kadınlarda Risk Faktörleri
    s13_narrative = (
        "Doğurganlık çağındaki premenopozal kadınlarda ÜSE sıklığını artıran faktörler ağırlıklı olarak "
        "davranışsal, cinsel ve genetik unsurlardan kaynaklanır.\n\n"
        "- **Cinsel Aktivite ve Alışkanlıklar:** Sık cinsel ilişki (balayı sistiti), yeni cinsel eş ve "
        "en önemlisi **cinsel ilişki sonrası miksiyon yapılmaması**, periüretral bakterilerin içeri itilmesini kolaylaştırır.\n"
        "- **Bariyer Yöntemleri:** **Spermisid ve diyafram kullanımı**, vajinal normal florayı bozarak "
        "üropatojen E. coli kolonizasyonunu dramatik ölçüde artırır.\n"
        "- **Diğer Unsurlar:** Genetik yatkınlık (Lewis kan grubu non-sekretuar fenotip), geçirilmiş ÜSE öyküsü, "
        "gebelik, düşük sosyoekonomik durum ve Diabetes Mellitus premenopozal dönem riskleridir.\n\n"
        "> [!IMPORTANT]\n"
        "> Premenopozal kadınlarda spermisid kullanımı ve koit sonrası idrar yapmama en kritik önlenebilir davranışsal risk faktörleridir."
    )
    s13_bullets = [
        "Sık cinsel ilişki, yeni eş ve ilişki sonrası miksiyon yapılmaması riski artırır.",
        "Spermisid ve diyafram kullanımı vajinal üropatojen kolonizasyonunu tetikler.",
        "Genetik yatkınlık, geçirilmiş ÜSE, gebelik ve DM ek risklerdir."
    ]
    s13_elements = [
        make_cloze("Premenopozal kadınlarda spermisid ve diyafram kullanımı vajende üropatojen kolonizasyonunu artırarak sistite yol açar.", "spermisid", "Sperm öldürücü kimyasal kontraseptif ajan"),
        make_table("Premenopozal Dönem Risk Bileşenleri", ["Risk Kategorisi", "Spesifik Faktör", "Etki Mekanizması"], [
            {"cells": [{"text": "Davranışsal / Cinsel", "isMasked": False}, {"text": "Koit sonrası miksiyon yapılmaması", "isMasked": True, "hint": "ilişki sonrası idrar çıkarmama"}, {"text": "Üretraya itilen bakterilerin mekanik yıkanamaması"}]},
            {"cells": [{"text": "Kontraseptif Yöntem", "isMasked": False}, {"text": "Spermisid ve diyafram kullanımı", "isMasked": False}, {"text": "Vajinal floranın bozulması ve E. coli kolonizasyonu", "isMasked": True, "hint": "koruyucu laktobasil kaybı"}]},
            {"cells": [{"text": "Fizyolojik / Sistemik", "isMasked": False}, {"text": "Hamilelik, genetik yatkınlık, DM", "isMasked": False}, {"text": "Üriner staz ve artmış glukozüri", "isMasked": False}]}
        ]),
        make_chain("Koital Sistit Gelişim Zinciri", [
            "1. Mekanik Sürtünme: Cinsel ilişki sırasında perineal bakteriler üretraya doğru itilir.",
            "2. Floranın Bozulması: Spermisid kullanımı laktobasilleri azaltarak E. coli'yi artırır.",
            "3. Miksiyon Eksikliği: İlişki sonrası idrar yapılmadığında bakteriler lümende kalır.",
            "4. Asendan Tırmanış: Bakteriler mesaneye ulaşarak akut sistit oluşturur."
        ]),
        make_recall("Premenopozal kadınlarda ÜSE'ye yol açan en önemli iki kontraseptif ve davranışsal risk faktörü nedir?", "Spermisid/diyafram kullanımı (floranın bozulması) ve cinsel ilişki sonrası miksiyon yapılmamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Premenopozal Riskler", [
            {"text": "Spermisid ve diyafram kullanımı vajinal üropatojen kolonizasyonunu artırır.", "isLie": False, "explanation": "Doğru. Laktobasil florasını bozar."},
            {"text": "Cinsel ilişki sonrası hemen miksiyon yapılması bakterileri mekanik olarak temizler.", "isLie": False, "explanation": "Doğru. Koruyucu bir davranıştır."},
            {"text": "Premenopozal kadınlarda cinsel aktivite ÜSE riskini tamamen sıfırlayan koruyucu bir durumdur.", "isLie": True, "explanation": "Tuzak! Cinsel aktivite, özellikle yeni eş ve sık koit, premenopozal sistitin en yaygın tetikleyicisidir."},
            {"text": "Hamilelik ve geçirilmiş ÜSE öyküsü premenopozal ek risk faktörlerindendir.", "isLie": False, "explanation": "Doğru. Ders notu tablosu verisidir."}
        ]),
        make_quiz("Premenopozal bir kadında vajende üropatojen kolonizasyonunu artırarak ÜSE riskini tetikleyen kontraseptif yöntem hangisidir?", [
            {"key": "A", "text": "Spermisid ve diyafram kullanımı", "isCorrect": True, "explanation": "Ders notunda spermisid ve diyafram kullanımının vajinal üropatojen kolonizasyonuna yol açtığı açıkça vurgulanmıştır."},
            {"key": "B", "text": "Tüp ligasyonu yapılması", "isCorrect": False, "explanation": "Florayı etkilemez."},
            {"key": "C", "text": "Doğal takvim yöntemi", "isCorrect": False, "explanation": "Kimyasal ajan içermez."},
            {"key": "D", "text": "Yalnızca vazektomi yapılmış partner", "isCorrect": False, "explanation": "Vajen florasını bozmaz."}
        ])
    ]
    slides.append(make_slide(13, "Premenopozal Kadınlarda Risk Faktörleri", "Cinsel aktivite, ilişki sonrası miksiyon, spermisid, diyafram ve gebelik", "Risk Faktörleri", s13_narrative, s13_bullets, s13_elements))

    # Slide 14: Postmenopozal Kadınlarda Östrojen Eksikliği ve Anatomik Değişimler
    s14_narrative = (
        "Menopoz sonrasında over fonksiyonlarının sona ermesi, kadın ürogenital traktusunda köklü "
        "hormonal ve anatomik değişimlere yol açarak ÜSE zeminini hazırlar.\n\n"
        "- **Östrojen Eksikliği ve Floranın Kaybı:** Östrojenin azalmasıyla vajinal epitel incelir, "
        "glikojen üretimi durur; bunun sonucunda koruyucu **laktobasiller kaybolur** ve vajinal pH yükselir.\n"
        "- **Üropatojen Kolonizasyonu:** Laktobasillerin asidik korumasından yoksun kalan vajen ve periüretral bölge, "
        "fekal kaynaklı Enterobacteriaceae (özellikle E. coli) ile yoğun biçimde kolonize olur.\n"
        "- **Anatomik ve Fonksiyonel Bozukluklar:** Pelvik taban zayıflığı sonucu gelişen **sistosel, rektosel, "
        "mesane divertikülü** rezidüel idrar bırakır; mental bozukluklar ve gaita inkontinansı riski katlar.\n\n"
        "> [!WARNING]\n"
        "> [ÇIKMIŞ SORU TUZAĞI] Postmenopozal dönemde ÜSE risk faktörü 'östrojen fazlalığı' DEĞİL, 'östrojen EKSİKLİĞİ'dir (laktobasil kaybı)."
    )
    s14_bullets = [
        "Östrojen eksikliği vajinal epitelde incelme ve laktobasil kaybına yol açar.",
        "Asidik koruma kalkınca vajende E. coli kolonizasyonu patlar.",
        "Sistosel, rektosel ve mesane divertikülü rezidü idrar ve staz oluşturur."
    ]
    s14_elements = [
        make_cloze("Postmenopozal dönemde ÜSE riskini artıran temel hormonal mekanizma östrojen eksikliği ve laktobasil kaybıdır.", "östrojen eksikliği", "Menopozla gelen kadınlık hormonu yetersizliği"),
        make_table("Postmenopozal Risk Mekanizmaları", ["Patoloji", "Hücresel / Anatomik Değişim", "Klinik Yansıması"], [
            {"cells": [{"text": "Hormonal Çöküş", "isMasked": False}, {"text": "Östrojen eksikliği (laktobasil kaybı)", "isMasked": True, "hint": "vajinal floranın asitliğini kaybetmesi"}, {"text": "pH artışı ve E. coli süperkolonizasyonu"}]},
            {"cells": [{"text": "Pelvik Prolapsus", "isMasked": False}, {"text": "Sistosel, rektosel, mesane divertikülü", "isMasked": False}, {"text": "Tam boşalamama ve rezidüel idrar stazı", "isMasked": True, "hint": "işeme sonrası idrar kalması"}]},
            {"cells": [{"text": "Fonksiyonel Bozukluk", "isMasked": False}, {"text": "Gaita inkontinansı, mental gerileme", "isMasked": False}, {"text": "Sürekli perineal fekal kontaminasyon", "isMasked": False}]}
        ]),
        make_chain("Östrojen Eksikliği - Sistit Patogenez Zinciri", [
            "1. Menopoz: Overlerden östrojen salgılanması durur.",
            "2. Glikojen Azalması: Vajinal skuamöz epitel atrofiye uğrar ve glikojen içeriği düşer.",
            "3. Laktobasil Ölümü: Laktik asit üreten laktobasiller ortamdan silinir, pH 4.5'in üzerine çıkar.",
            "4. Fekal Kolonizasyon: Fekal E. coli vajene yerleşir ve kısa üretradan mesaneye tırmanır."
        ]),
        make_recall("Postmenopozal dönemde vajinal laktobasillerin yok olmasına ve ÜSE riskinin artmasına yol açan primer endokrin faktör nedir?", "Östrojen eksikliğidir (atrofi ve glikojen kaybı sonucu laktobasiller yaşayamaz)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Postmenopozal Riskler", [
            {"text": "Postmenopozal dönemde östrojen eksikliği vajinal laktobasil kaybına neden olur.", "isLie": False, "explanation": "Doğru. Kardinal patofizyolojik mekanizmadır."},
            {"text": "Sistosel ve rektosel pelvik staz yaratarak enfeksiyon riskini artırır.", "isLie": False, "explanation": "Doğru. Tam boşalmayı engeller."},
            {"text": "Postmenopozal kadınlarda aşırı östrojen fazlalığı ÜSE'nin en sık nedenidir.", "isLie": True, "explanation": "Tuzak! Postmenopozal risk nedeni östrojen fazlalığı değil, östrojen EKSİKLİĞİDİR."},
            {"text": "Gaita inkontinansı periüretral fekal kontaminasyonu artırır.", "isLie": False, "explanation": "Doğru. Bakteri inokülasyonu sağlar."}
        ]),
        make_quiz("Aşağıdakilerden hangisi postmenopozal kadınlarda ÜSE gelişimi için bir risk faktörü DEĞİLDİR?", [
            {"key": "A", "text": "Östrojen fazlalığı", "isCorrect": True, "explanation": "Östrojen fazlalığı değil, tam tersine östrojen EKSİKLİĞİ (laktobasil kaybı) bir risk faktörüdür (Çıkmış sınav sorusudur)."},
            {"key": "B", "text": "Östrojen eksikliğine bağlı laktobasil kaybı", "isCorrect": False, "explanation": "Gerçek risk faktörüdür."},
            {"key": "C", "text": "Sistosel ve rektosel varlığı", "isCorrect": False, "explanation": "Staz yaratan risk faktörüdür."},
            {"key": "D", "text": "Gaita inkontinansı ve mental bozukluk", "isCorrect": False, "explanation": "Gerçek risk faktörüdür."}
        ])
    ]
    slides.append(make_slide(14, "Postmenopozal Kadınlarda Östrojen Eksikliği ve Anatomik Değişimler", "Östrojen eksikliği, laktobasil kaybı, sistosel, rektosel ve mesane divertikülü", "Risk Faktörleri", s14_narrative, s14_bullets, s14_elements))

    # Slide 15: Genç Erkeklerde Risk Faktörleri (<50 Yaş)
    s15_narrative = (
        "Daha önce belirtildiği gibi 50 yaşın altındaki erkeklerde ÜSE görülme sıklığı %1'in altındadır. "
        "Bu yaş grubunda enfeksiyon saptandığında özgül predispozan durumlar aranmalıdır.\n\n"
        "- **Sünnet Durumu:** Sünnetsiz erkeklerde prepisyum (sünnet derisi) altında biriken smegma ve nemli "
        "ortam, üropatojen bakterilerin kolonizasyonunu belirgin şekilde kolaylaştırır.\n"
        "- **Cinsel Yönelim ve İlişki:** Homoseksüel ilişki (anal ilişki) rektal floranın üretraya "
        "doğrudan inokülasyonuna yol açar; cinsel eşte vajinal E. coli kolonizasyonu olması riski tetikler.\n"
        "- **İmmün Yetmezlik:** HIV/AIDS enfeksiyonu hücresel immüniteyi çökerttiğinden genç erkekte "
        "atipik ve ağır üriner enfeksiyonların gelişimine zemin hazırlar.\n\n"
        "> [!NOTE]\n"
        "> 50 yaş altındaki bir erkekte ÜSE saptandığında mutlaka altta yatan anatomik anomali, sünnetsizlik, cinsel öykü veya immünsupresyon sorgulanmalıdır."
    )
    s15_bullets = [
        "Sünnet olmama prepisyum altında üropatojen kolonizasyonunu artırır.",
        "Homoseksüel anal ilişki fekal mikroorganizmaların doğrudan inokülasyonudur.",
        "AIDS ve eşte vajinal E. coli kolonizasyonu genç erkekte ek risklerdir."
    ]
    s15_elements = [
        make_cloze("50 yaş altı erkeklerde sünnet olmama durumu prepisyum altında bakteri kolonizasyonunu artırarak ÜSE riskini yükseltir.", "sünnet olmama", "Prepisyum derisinin cerrahi olarak alınmamış olması"),
        make_table("Genç Erkeklerde (<50 Yaş) Risk Faktörleri", ["Risk Faktörü", "Klinik Özellik", "Patojenik Mekanizma"], [
            {"cells": [{"text": "Sünnetsizlik", "isMasked": False}, {"text": "Prepisyum altında smegma birikimi", "isMasked": True, "hint": "sünnet derisi altındaki rezervuar"}, {"text": "Üropatojen E. coli rezervuarı oluşturma"}]},
            {"cells": [{"text": "Homoseksüel İlişki", "isMasked": False}, {"text": "Anal koit öyküsü", "isMasked": False}, {"text": "Doğrudan yüksek inokulumlu fekal temas", "isMasked": True, "hint": "rektal floranın üretraya bulaşması"}]},
            {"cells": [{"text": "AIDS / İmmünsupresyon", "isMasked": False}, {"text": "CD4 T lenfosit çöküşü", "isMasked": False}, {"text": "Fırsatçı ve ağır enfeksiyon yatkınlığı", "isMasked": False}]}
        ]),
        make_recall("50 yaşın altındaki erkeklerde ÜSE gelişimini tetikleyen üç temel ek risk faktörü nedir?", "Sünnet olmama, homoseksüel ilişki (anal koit) ve AIDS (veya eşte vajinal E. coli kolonizasyonu)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Genç Erkek Riskleri", [
            {"text": "50 yaş altı erkeklerde sünnetsizlik ÜSE için risk faktörüdür.", "isLie": False, "explanation": "Doğru. Prepisyum bakteri kolonizasyonunu artırır."},
            {"text": "Homoseksüel anal ilişki rektal floranın doğrudan üretraya bulaşmasına yol açar.", "isLie": False, "explanation": "Doğru. Yüksek inokulum riskidir."},
            {"text": "Genç erkeklerde ÜSE o kadar doğaldır ki hiçbir risk faktörü olmadan toplumun %80'inde görülür.", "isLie": True, "explanation": "Tuzak! 1-50 yaş erkekte ÜSE <%1'dir ve saptandığında mutlaka bir risk faktörü aranır."},
            {"text": "AIDS hastalarında immün yetmezlik nedeniyle ÜSE riski artar.", "isLie": False, "explanation": "Doğru. Sistemik immün kayıp vardır."}
        ]),
        make_quiz("50 yaş altındaki erkeklerde ÜSE riskini artıran durumlar arasında aşağıdakilerden hangisi YER ALMAZ?", [
            {"key": "A", "text": "Sünnet olmama durumu", "isCorrect": False, "explanation": "Ders notunda belirtilen risk faktörüdür."},
            {"key": "B", "text": "Homoseksüel ilişki öyküsü", "isCorrect": False, "explanation": "Ders notunda belirtilen risk faktörüdür."},
            {"key": "C", "text": "AIDS varlığı", "isCorrect": False, "explanation": "Ders notunda belirtilen risk faktörüdür."},
            {"key": "D", "text": "Benign prostat hiperplazisine (BPH) bağlı ileri derece mesane çıkım obstrüksiyonu", "isCorrect": True, "explanation": "BPH 50 yaş altı değil, tipik olarak 50 yaş ÜSTÜ (>50 yaş) erkeklerin risk faktörüdür."}
        ])
    ]
    slides.append(make_slide(15, "Genç Erkeklerde Risk Faktörleri (<50 Yaş)", "Sünnetsizlik, homoseksüel ilişki, AIDS ve vajinal E. coli kolonizasyonu", "Risk Faktörleri", s15_narrative, s15_bullets, s15_elements))

    # Slide 16: İleri Yaş Erkeklerde Risk Faktörleri (>50 Yaş)
    s16_narrative = (
        "50 yaşın üzerindeki erkek popülasyonda ÜSE insidansı, gençlikteki <%1 düzeyini terk ederek "
        "hızla tırmanışa geçer ve yaşlı kadınların oranlarına yaklaşır.\n\n"
        "- **Prostat Hipertrofisi (BPH):** Yaşlanmayla birlikte prostat bezinin büyümesi mesane çıkımını "
        "tıkar, tam boşalmayı önler ve mesanede rezidüel idrar stazı yaratır.\n"
        "- **Prostatik Salgının Bozulması:** Prostat dokusunun glandüler atrofisi sonucu, sıvının "
        "bakterisidal özelliği ve çinko konsantrasyonu belirgin biçimde azalır.\n"
        "- **Kateterizasyon ve Nörolojik Bozulma:** İnkontinans için prezervatif sonda veya foley kateter "
        "kullanımı üretrayı kolonize eder; mental bozukluklar ve gaita inkontinansı tabloyu ağırlaştırır.\n\n"
        "> [!IMPORTANT]\n"
        "> 50 yaş üstü erkekte ÜSE'nin bir numaralı anatomik motoru prostat hipertrofisi ve buna bağlı rezidü idrar birikimidir."
    )
    s16_bullets = [
        "Prostat hipertrofisi (BPH) mesane çıkım obstrüksiyonu ve staz yapar.",
        "Prostat sekresyonunun azalması bakterisidal korumayı zayıflatır.",
        "Prezervatif sonda kullanımı ve gaita inkontinansı üretral kolonizasyon oluşturur."
    ]
    s16_elements = [
        make_cloze("50 yaş üstü erkeklerde ÜSE riskini en çok artıran obstrüktif patoloji prostat hipertrofisi ve stazdır.", "prostat hipertrofisi", "İyi huylu prostat büyümesi (BPH)"),
        make_table("İleri Yaş Erkek (>50 Yaş) Risk Bileşenleri", ["Faktör", "Fizyopatolojik Değişim", "Enfeksiyöz Sonuç"], [
            {"cells": [{"text": "Prostat Hipertrofisi", "isMasked": False}, {"text": "Mesane çıkım darlığı ve rezidü idrar", "isMasked": True, "hint": "idrar torbasının tam boşalamaması"}, {"text": "Mesanede bakteri çoğalması için staz havuzu"}]},
            {"cells": [{"text": "Prostat Sıvısı Kaybı", "isMasked": False}, {"text": "Bakterisidal sekresyonun azalması", "isMasked": False}, {"text": "Kimyasal sterilizasyon gücünün düşmesi", "isMasked": True, "hint": "antibakteriyel korumanın çöküşü"}]},
            {"cells": [{"text": "Prezervatif Sonda", "isMasked": False}, {"text": "Üretral meatusun sürekli nemli kalması", "isMasked": False}, {"text": "Yoğun üretral kolonizasyon", "isMasked": False}]}
        ]),
        make_chain("Yaşlı Erkekte ÜSE Patogenez Zinciri", [
            "1. Adenom Gelişimi: Prostat dokusu hipertrofiye uğrar (BPH).",
            "2. Obstrüksiyon: Prostatik üretra sıkışır ve işeme zorlaşır.",
            "3. Rezidü İdrar: Mesane tabanında her miksiyon sonrası 100-200 ml idrar kalır.",
            "4. Bakterisidal Kayıp: Koruyucu prostat sıvısı azalır ve stazda bakteriler patlar."
        ]),
        make_recall("50 yaş üstündeki erkeklerde ÜSE gelişiminde rol oynayan en önemli anatomik ve sekresyonel faktörler nelerdir?", "Prostat hipertrofisi (mesane çıkım obstrüksiyonu/staz) ve prostat sekresyonunun bakterisidal aktivitesinin azalmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İleri Yaş Erkek Riskleri", [
            {"text": "50 yaş üstü erkeklerde prostat hipertrofisi en önemli risk faktörlerindendir.", "isLie": False, "explanation": "Doğru. Staz ve obstrüksiyon yapar."},
            {"text": "Prostat sıvısının bakterisidal aktivitesinin azalması enfeksiyon riskini artırır.", "isLie": False, "explanation": "Doğru. Kimyasal koruma azalır."},
            {"text": "Prezervatif sonda kullanımı üretrayı tamamen steril tutarak enfeksiyonu kesinlikle önler.", "isLie": True, "explanation": "Tuzak! Prezervatif sonda nem ve cilt temasıyla üretral kolonizasyon ve ÜSE riskini belirgin artırır."},
            {"text": "Fonksiyonel ve mental bozukluklar ileri yaş erkekte ÜSE yatkınlığı yaratır.", "isLie": False, "explanation": "Doğru. Hijyen bozulur ve staz artar."}
        ]),
        make_quiz("50 yaş üstü erkeklerde ÜSE görülme sıklığının artmasına neden olan temel patoloji hangisidir?", [
            {"key": "A", "text": "Prostat hipertrofisi ve prostat sekresyonunun azalması", "isCorrect": True, "explanation": "Ders notunda >50 yaş erkekler için temel risk faktörleri prostat hipertrofisi ve prostat sekresyonunun azalması olarak belirtilmiştir."},
            {"key": "B", "text": "Üretranın aniden 50 santimetreye uzaması", "isCorrect": False, "explanation": "Üretra boyu değişmez."},
            {"key": "C", "text": "Östrojen hormonunun aşırı üretilmesi", "isCorrect": False, "explanation": "Erkek patolojisi bu değildir."},
            {"key": "D", "text": "Böbreklerin idrar üretimini tamamen durdurması", "isCorrect": False, "explanation": "Anüri enfeksiyon nedeni değildir."}
        ])
    ]
    slides.append(make_slide(16, "İleri Yaş Erkeklerde Risk Faktörleri (>50 Yaş)", "Prostat hipertrofisi, bakterisidal prostat sıvısı kaybı ve prezervatif sonda", "Risk Faktörleri", s16_narrative, s16_bullets, s16_elements))

    # Slide 17: Diyabetik Hastalarda ÜSE Yatkınlığı ve Patofizyolojisi
    s17_narrative = (
        "Diabetes Mellitus (DM), hem hücresel düzeyde immün felç hem de nörolojik ve metabolik "
        "komplikasyonları ile ÜSE riskini katbekat artıran en kritik sistemik hastalıktır.\n\n"
        "- **Glukozüri ve Besiyeri Ortamı:** Kontrolsüz diyabette böbrek eşiğini aşan kan şekeri idrara "
        "dökülür; glukozdan zengin idrar üropatojen bakteriler için mükemmel bir zenginleştirilmiş besiyeridir.\n"
        "- **Otonom Nöropati (Nörojenik Mesane):** Diyabetik mikrovasküler hasar mesane innervasyonunu bozar; "
        "duyu kaybı ve detrüsör atonisi sonucu hasta mesanesini tam boşaltamaz ve kronik staz gelişir.\n"
        "- **Fagositoz Yetmezliği:** Hiperglisemi nötrofillerin kemotaksisini, adherensini ve intrasellüler "
        "bakterisidal öldürme mekanizmalarını (solunumsal patlama) inhibe eder.\n\n"
        "> [!IMPORTANT]\n"
        "> Diyabetik hastalarda gelişen ÜSE'ler her zaman 'komplike ÜSE' kabul edilir ve amfizematöz komplikasyon riski yüksektir."
    )
    s17_bullets = [
        "Glukozüri bakteriler için zengin bir büyüme besiyeri ortamı sunar.",
        "Diyabetik otonom nöropati nörojenik mesane ve kronik idrar stazı yaratır.",
        "Nötrofil kemotaksisi ve fagositoz fonksiyonları hiperglisemide bozulur."
    ]
    s17_elements = [
        make_cloze("Diyabetik hastalarda glukozüri bakteriler için besiyeri oluştururken otonom nöropati nörojenik mesane ve staza yol açar.", "nörojenik mesane", "Sinir hasarına bağlı çalışmayan mesane"),
        make_table("Diyabette ÜSE Yatkınlık Triadı", ["Mekanizma", "Diyabete Özgü Süreç", "Klinik Yansıması"], [
            {"cells": [{"text": "Metabolik", "isMasked": False}, {"text": "Glukozüri (şekerli idrar)", "isMasked": True, "hint": "idrarda glukoz bulunması"}, {"text": "Bakterilerin logaritmik hızla üremesi"}]},
            {"cells": [{"text": "Nörolojik", "isMasked": False}, {"text": "Diyabetik sistopati / nörojenik mesane", "isMasked": False}, {"text": "Atoni ve yüksek rezidüel idrar stazı", "isMasked": True, "hint": "mesanede kronik idrar birikimi"}]},
            {"cells": [{"text": "İmmünolojik", "isMasked": False}, {"text": "Lökosit kemotaksis ve fagositoz defekti", "isMasked": False}, {"text": "Doku invazyonuna karşı yanıtsızlık", "isMasked": False}]}
        ]),
        make_chain("Diyabette Komplike ÜSE Zinciri", [
            "1. Hiperglisemi: Kan şekeri yükselir ve glukozüri başlar.",
            "2. Nöropati: Mesane otonom sinirleri hasarlanır ve hissiz atonik mesane oluşur.",
            "3. Lökosit Felci: Glukoz ortamında nötrofillerin fagositoz gücü kırılır.",
            "4. Ağır Enfeksiyon: Bakteriler süratle ürer, dokuyu harap eder ve amfizematöz pyelonefrit riski doğar."
        ]),
        make_recall("Diabetes Mellitus'un ÜSE'ye zemin hazırlayan üç temel patofizyolojik bileşeni nedir?", "1) Glukozüri (bakteri besiyeri), 2) Otonom nöropati / nörojenik mesane (üriner staz), 3) Nötrofil fagositoz ve kemotaksis bozukluğudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Diyabet ve ÜSE", [
            {"text": "Diyabette glukozüri bakterilerin çoğalmasını kolaylaştıran bir besiyeri ortamı sunar.", "isLie": False, "explanation": "Doğru. Bakteri proliferasyonunu hızlandırır."},
            {"text": "Diyabetik nöropati nörojenik mesaneye ve idrar stazına yol açar.", "isLie": False, "explanation": "Doğru. Atonik mesane gelişir."},
            {"text": "Diyabetik hastalarda gelişen ÜSE'ler son derece hafif seyreder ve asla komplike kabul edilmez.", "isLie": True, "explanation": "Tuzak! Diyabetli hastaların ÜSE'leri daima KOMPLİKE ÜSE kabul edilir ve ağır seyredebilir."},
            {"text": "Hiperglisemi polimorfonükleer lökositlerin fagositoz yeteneğini bozar.", "isLie": False, "explanation": "Doğru. İmmün fonksiyonlar baskılanır."}
        ]),
        make_quiz("Diyabetik hastalarda üriner sistem enfeksiyonlarına yatkınlık oluşmasında aşağıdakilerden hangisi rol OYNAMAZ?", [
            {"key": "A", "text": "Glukozürinin bakteriler için zengin bir büyüme ortamı sağlaması", "isCorrect": False, "explanation": "Yatkınlık mekanizmasıdır."},
            {"key": "B", "text": "Otonom nöropatiye bağlı nörojenik mesane ve staz gelişimi", "isCorrect": False, "explanation": "Yatkınlık mekanizmasıdır."},
            {"key": "C", "text": "Nötrofillerin fagositoz ve kemotaksis fonksiyonlarının bozulması", "isCorrect": False, "explanation": "Yatkınlık mekanizmasıdır."},
            {"key": "D", "text": "Prostat bezinin tamamen yok olması ve üretrasının 1 santimetreye düşmesi", "isCorrect": True, "explanation": "Diyabette prostat yok olmaz veya erkek üretrası kısalmaz; bu tamamen kurgusal bir ifadedir."}
        ])
    ]
    slides.append(make_slide(17, "Diyabetik Hastalarda ÜSE Yatkınlığı ve Patofizyolojisi", "Glukozüri, nörojenik mesane, lökosit fagositoz bozukluğu ve komplike seyir", "Risk Faktörleri", s17_narrative, s17_bullets, s17_elements))

    # Slide 18: Üriner Staz, Obstrüksiyon ve Yabancı Cisimler
    s18_narrative = (
        "Sağlıklı bir üriner sistemde bakteriyel kolonizasyonu önleyen en dinamik mekanizma, düzenli "
        "aralıklarla gerçekleşen miksiyon ve hidrostatik idrar akımı ile sağlanan mekanik yıkamadır.\n\n"
        "- **Stazın Patolojisi:** Akımı durduran organik (kalkül, üretral darlık, tümör) veya fonksiyonel "
        "(VUR, nörojenik mesane) nedenler **üriner staz** oluşturur; durgun idrarda bakteriler katlanarak ürer.\n"
        "- **Yabancı Cisimler (Taş ve Kateter):** Mesane taşı veya foley sonda yüzeyi, bakterilerin "
        "konak immünitesinden ve antibiyotiklerden saklandığı kalın bir **biyofilm tabakası** ile kaplanır.\n"
        "- **Eradikasyon İmkansızlığı:** Yabancı cisim çıkarılmadığı veya obstrüksiyon giderilmediği sürece "
        "en güçlü parenteral antibiyotikler dahi enfeksiyonu kalıcı olarak tedavi edemez.\n\n"
        "> [!IMPORTANT]\n"
        "> İdrar yolu taşı veya kateter varlığında bakteriler biyofilm içine gömülür; mekanik kaynak temizlenmeden kür sağlanamaz."
    )
    s18_bullets = [
        "Normal idrar akımı bakterileri dışarı atan dinamik yıkama mekanizmasıdır.",
        "Obstrüksiyon ve staz bakterilerin katlanarak çoğalmasına yol açar.",
        "Taş ve kateterler bakteriyel biyofilm oluşturarak antibiyotik penetrasyonunu engeller."
    ]
    s18_elements = [
        make_cloze("Taş ve kateter gibi yabancı cisimler üzerinde bakterilerin oluşturduğu biyofilm tabakası antibiyotiklerin etkinliğini engeller.", "biyofilm", "Bakterilerin oluşturduğu koruyucu matriks zırhı"),
        make_table("Lokal Faktörlerin Enfeksiyon Etkileşimi", ["Faktör Tipi", "Klinik Örnek", "Yarattığı Temel Sorun"], [
            {"cells": [{"text": "Yabancı Cisim", "isMasked": False}, {"text": "Üriner kateter, böbrek taşı", "isMasked": True, "hint": "sonda ve mineral kristalize kitleler"}, {"text": "Biyofilm zırhı ve dirençli mikroorganizma kolonizasyonu"}]},
            {"cells": [{"text": "Dinamik Staz", "isMasked": False}, {"text": "Vezikoüreteral reflü (VUR)", "isMasked": False}, {"text": "İdrarın böbreğe geri kaçması ve piyelonefrit", "isMasked": True, "hint": "idrarın geriye kaçak yapması"}]},
            {"cells": [{"text": "Yapısal Darlık", "isMasked": False}, {"text": "Üretra darlığı, tümör obstrüksiyonu", "isMasked": False}, {"text": "İntralüminal basınç artışı ve doku iskemisi", "isMasked": False}]}
        ]),
        make_chain("Biyofilm ve Dirençli Enfeksiyon Zinciri", [
            "1. Yüzey Teması: Bakteriler kateter veya taş yüzeyine yapışır.",
            "2. Matriks Üretimi: Ekstraselüler polisakkarit salgılayarak biyofilm oluştururlar.",
            "3. Korunma: Biyofilm içindeki bakteriler lökositlerden ve antibiyotikten korunur.",
            "4. Kronikleşme: Antibiyotik kesildiğinde biyofilmden dökülen bakteriler relaps yaratır."
        ]),
        make_recall("Üriner sistemde kateter veya taş varlığında antibiyotik tedavisinin başarısız olmasının ve relaps gelişmesinin nedeni nedir?", "Bakterilerin bu yabancı cisimler üzerinde antimikrobiyallere ve fagositoza dirençli biyofilm tabakası oluşturmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Staz ve Yabancı Cisim", [
            {"text": "Normal idrar akımının mekanik yıkama etkisi en önemli doğal konak savunmasıdır.", "isLie": False, "explanation": "Doğru. Bakterilerin atılmasını sağlar."},
            {"text": "Üriner staz bakteriyel proliferasyonu hızlandıran lokal bir predispozandır.", "isLie": False, "explanation": "Doğru. Durgun idrarda mikroplar çoğalır."},
            {"text": "Kateter üzerinde oluşan biyofilm antibiyotiklerin bakteriye ulaşmasını 1000 kat kolaylaştırır.", "isLie": True, "explanation": "Tuzak! Biyofilm antibiyotik penetrasyonunu ve immün fagositozu engelleyen koruyucu bir bariyerdir."},
            {"text": "Nefrolitiazis (taş) komplike edici bir faktör olarak relapslara yol açabilir.", "isLie": False, "explanation": "Doğru. Enfekte taş odağı relaps nedenidir."}
        ]),
        make_quiz("Üriner kateter veya taş varlığında enfeksiyonun kalıcı olarak kür edilememesinin ve antibiyotiklere yanıtsızlığın temel nedeni nedir?", [
            {"key": "A", "text": "Bakterilerin yabancı cisim yüzeyinde koruyucu biyofilm tabakası oluşturması", "isCorrect": True, "explanation": "Biyofilm, antibiyotiklerin ve immün hücrelerin bakterilere penetre olmasını engeller."},
            {"key": "B", "text": "Bakterilerin aniden ökaryotik mantarlara dönüşmesi", "isCorrect": False, "explanation": "Bakteri tür değiştirmez."},
            {"key": "C", "text": "Kateterin idrarı tamamen gaza dönüştürmesi", "isCorrect": False, "explanation": "Böyle bir mekanizma yoktur."},
            {"key": "D", "text": "Böbreklerin antibiyotiği yok etmesi", "isCorrect": False, "explanation": "Sorun yabancı cisim biyofilmidir."}
        ])
    ]
    slides.append(make_slide(18, "Üriner Staz, Obstrüksiyon ve Yabancı Cisimler", "İdrar stazı, mekanik yıkama kaybı, kateter, taş ve biyofilm oluşumu", "Risk Faktörleri", s18_narrative, s18_bullets, s18_elements))

    # Slide 19: İkinci Bölüm Özeti: Risk Faktörleri Spektrumu
    s19_narrative = (
        "ÜSE risk faktörleri tablosu incelendiğinde, hastanın yaşı, cinsiyeti ve anatomik koşullarına "
        "göre değişen çok yönlü bir predispozan faktörler ağı ile karşılaşılır.\n\n"
        "- **Sistemik vs Lokal:** DM, immünsupresyon ve malnütrisyon sistemik direnci çözerken; staz, "
        "taş, kateter ve obstrüksiyon lokal bariyerleri yıkar.\n"
        "- **Kadınlardaki Dinamik:** Premenopozal kadında cinsel aktivite, ilişki sonrası miksiyon "
        "yapmama ve spermisid kullanımı; postmenopozal kadında ise **östrojen eksikliği** ve pelvik organ prolapsusları belirleyicidir.\n"
        "- **Erkeklerdeki Dinamik:** 50 yaş altında sünnetsizlik, anal koit ve HIV riski artırırken; 50 yaş "
        "üstünde **prostat hipertrofisi** ve bakterisidal prostat sıvısı kaybı tabloya hakim olur.\n\n"
        "> [!IMPORTANT]\n"
        "> Yaş ve cinsiyete göre risk faktörlerini doğru ayrıştırmak, hem ayırıcı tanıda hem de etiyolojiye yönelik koruyucu tedavide esastır."
    )
    s19_bullets = [
        "Sistemik: DM, immünosüpresyon | Lokal: Staz, yabancı cisim, obstrüksiyon.",
        "Kadında: Premenopozal spermisid/koit | Postmenopozal östrojen eksikliği.",
        "Erkekte: <50 yaş sünnetsizlik/koit | >50 yaş prostat hipertrofisi."
    ]
    s19_elements = [
        make_cloze("Risk faktörleri analizinde postmenopozal kadında östrojen eksikliği, ileri yaş erkekte ise prostat hipertrofisi ön plandadır.", "prostat hipertrofisi", "Yaşlı erkeklerdeki mesane çıkım darlığı"),
        make_table("Cinsiyet ve Yaş Dönemlerine Göre Kardinal Riskler", ["Popülasyon", "En Kritik Risk Faktörü", "Altta Yatan Mekanizma"], [
            {"cells": [{"text": "Premenopozal Kadın", "isMasked": False}, {"text": "Spermisid / koit sonrası miksiyon yapmama", "isMasked": True, "hint": "davranışsal ve kontraseptif risk"}, {"text": "Floranın bozulması ve asendan itilme"}]},
            {"cells": [{"text": "Postmenopozal Kadın", "isMasked": False}, {"text": "Östrojen eksikliği (laktobasil kaybı)", "isMasked": False}, {"text": "Vajinal pH artışı ve E. coli kolonizasyonu", "isMasked": True, "hint": "asidik koruyucu ortamın çökmesi"}]},
            {"cells": [{"text": "İleri Yaş Erkek (>50)", "isMasked": False}, {"text": "Prostat hipertrofisi ve sekresyon azalması", "isMasked": False}, {"text": "Mesane çıkım obstrüksiyonu ve staz", "isMasked": False}]}
        ]),
        make_recall("Kadınlarda premenopozal ve postmenopozal dönemdeki en temel iki farklı risk faktörü nedir?", "Premenopozal dönemde spermisid kullanımı ve cinsel aktivite; postmenopozal dönemde ise östrojen eksikliği (laktobasil kaybı) ve pelvik relaksasyondur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Risk Spektrumu", [
            {"text": "Sistemik faktörler arasında Diabetes Mellitus ve immünosüpresyon yer alır.", "isLie": False, "explanation": "Doğru. Vücut direncini düşürür."},
            {"text": "Postmenopozal kadınlarda risk faktörü östrojen fazlalığı değil östrojen eksikliğidir.", "isLie": False, "explanation": "Doğru. Kritik sınav ayrımıdır."},
            {"text": "İleri yaş erkeklerde prostat hipertrofisi staz yaratarak ÜSE riskini artırır.", "isLie": False, "explanation": "Doğru. Mesane çıkımını tıkar."},
            {"text": "Spermisid kullanımı vajinal laktobasilleri koruyarak ÜSE'yi kesin olarak engeller.", "isLie": True, "explanation": "Tuzak! Spermisid laktobasilleri yok ederek üropatojen kolonizasyonunu artırır."}
        ]),
        make_quiz("Aşağıdaki eşleştirmelerden hangisi yaş ve cinsiyete özgü ÜSE risk faktörleri açısından DOĞRUDUR?", [
            {"key": "A", "text": "Postmenopozal kadın: Östrojen eksikliği | İleri yaş erkek: Prostat hipertrofisi", "isCorrect": True, "explanation": "Ders notu tablolarında belirtilen kesin ve doğru eşleştirmedir."},
            {"key": "B", "text": "Postmenopozal kadın: Östrojen fazlalığı | İleri yaş erkek: Sünnetsizlik", "isCorrect": False, "explanation": "Östrojen fazlalığı risk değildir; sünnetsizlik genç erkektedir."},
            {"key": "C", "text": "Premenopozal kadın: Prostat büyümesi", "isCorrect": False, "explanation": "Kadında prostat bulunmaz."},
            {"key": "D", "text": "Genç erkek: Vajinal atrofi", "isCorrect": False, "explanation": "Erkekte vajen bulunmaz."}
        ])
    ]
    slides.append(make_slide(19, "İkinci Bölüm Özeti: Risk Faktörleri Spektrumu", "Sistemik, lokal, premenopozal, postmenopozal ve erkek risk faktörlerinin özeti", "Konsolidasyon", s19_narrative, s19_bullets, s19_elements))

    # Slide 20: [TEKRAR SAYFASI - CHECKPOINT 2] Risk Faktörleri ve Predispozan Durumlar
    s20_narrative = (
        "Bu tekrar sayfasında 2. Bölümde detaylandırılan sistemik ve lokal zemin hazırlayıcı faktörleri, "
        "kadın ve erkek popülasyonlarındaki spesifik riskleri pekiştiriyoruz.\n\n"
        "- **Sistemik ve Lokal:** DM'de glukozüri ve nörojenik mesane; lokalde ise taş, kateter ve "
        "obstrüksiyonun oluşturduğu staz ve biyofilm tabakası ÜSE zeminini hazırlar.\n"
        "- **Kadınlarda Dönemsel Fark:** Doğurganlık çağında spermisid, diyafram ve koit sonrası idrar "
        "yapmama öne çıkarken; menopoz sonrasında **östrojen eksikliği** laktobasilleri silerek E. coli'ye yol açar.\n"
        "- **Erkeklerde Dönemsel Fark:** Genç erkekte sünnetsizlik ve anal koit; 50 yaş üstünde ise "
        "**prostat hipertrofisi** ve bakterisidal prostat sıvısı kaybı temel belirleyicidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] ÜSE risk faktörlerinde sınavların en klasik tuzağı: Postmenopozal dönemde risk östrojen fazlalığı değil, ÖSTROJEN EKSİKLİĞİDİR!"
    )
    s20_bullets = [
        "DM (glukozüri + nöropati) ve staz (taş, kateter) majör predispozandır.",
        "Postmenopozal kadında kardinal risk faktörü ÖSTROJEN EKSİKLİĞİDİR.",
        ">50 yaş erkekte prostat hipertrofisi ve prostat sıvısı kaybı esastır."
    ]
    s20_elements = [
        make_cloze("Sınavların klasik sorusu: Kadınlarda ÜSE risk faktörü olan hormonal durum östrojen eksikliği olup östrojen fazlalığı değildir.", "östrojen eksikliği", "Menopozal hormon yetersizliği"),
        make_table("2. Bölüm Büyük Tekrar Tablosu", ["Risk Grubu", "Temel Risk Faktörleri", "Patofizyolojik Sonuç"], [
            {"cells": [{"text": "Sistemik Zemin", "isMasked": False}, {"text": "DM, immünosüpresyon, malnütrisyon", "isMasked": True, "hint": "genel direnç kaybı yaratanlar"}, {"text": "Glukozüri ve fagositoz bozukluğu"}]},
            {"cells": [{"text": "Premenopozal Kadın", "isMasked": False}, {"text": "Spermisid, diyafram, koit sonrası miksiyon yapmama", "isMasked": False}, {"text": "Vajinal kolonizasyon ve asendan tırmanış", "isMasked": True, "hint": "idrar yolu boyunca yukarı ilerleme"}]},
            {"cells": [{"text": "Postmenopozal Kadın", "isMasked": False}, {"text": "Östrojen eksikliği, laktobasil kaybı, sistosel", "isMasked": True, "hint": "hormon kaybı ve prolapsus"}, {"text": "Vajinal pH artışı ve rezidüel idrar"}]},
            {"cells": [{"text": "İleri Yaş Erkek (>50)", "isMasked": False}, {"text": "Prostat hipertrofisi, bakterisidal sıvı kaybı", "isMasked": False}, {"text": "Mesane çıkım darlığı ve staz", "isMasked": False}]}
        ]),
        make_chain("Risk Faktöründen Kliniğe İlerleme", [
            "1. Predispozisyon: Östrojen eksikliği veya prostat büyümesi staz/kolonizasyon yaratır.",
            "2. Yabancı Cisim / Biyofilm: Taş veya kateter bakterileri immüniteden gizler.",
            "3. İmmün Yetersizlik: DM gibi sistemik faktörler lökosit cevabını köreltir.",
            "4. Ağır Tablo: Komplike ÜSE tablosu yerleşir ve tedavi güçleşir."
        ]),
        make_recall("Kadınlarda idrar yolu enfeksiyonu için risk faktörü OLMAYAN ancak sınavda sıkça çeldirici yapılan hormonal durum nedir?", "Östrojen fazlalığıdır (kadında risk faktörü olan durum östrojen EKSİKLİĞİDİR)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 2. Bölüm Konsolidasyonu", [
            {"text": "Postmenopozal dönemde östrojen eksikliği vajinal laktobasilleri yok ederek riski artırır.", "isLie": False, "explanation": "Doğru. En kritik sınav spotudur."},
            {"text": "Spermisid kullanımı vajinal pH ve florayı bozarak E. coli yerleşimini kolaylaştırır.", "isLie": False, "explanation": "Doğru. Premenopozal risktir."},
            {"text": "Kadınlarda östrojen fazlalığı ÜSE riskini katbekat artıran en yaygın patolojidir.", "isLie": True, "explanation": "Tuzak! Kadınlarda ÜSE için risk faktörü östrojen fazlalığı değil, östrojen EKSİKLİĞİDİR (Çıkmış sınav sorusu)."},
            {"text": "50 yaş üstü erkeklerde BPH'ya bağlı mesane çıkım obstrüksiyonu staz yaratır.", "isLie": False, "explanation": "Doğru. İleri yaş erkek mekanizmasıdır."}
        ]),
        make_quiz("2. Bölümün temel kazanımlarına göre aşağıdaki risk faktörü ifadelerinden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Kadınlarda östrojen fazlalığı ÜSE için en önemli predispozan faktördür", "isCorrect": True, "explanation": "Yanlış! Kadınlarda predispozan olan durum östrojen fazlalığı değil, postmenopozal ÖSTROJEN EKSİKLİĞİDİR (Kurul 1 çıkmış sorusu)."},
            {"key": "B", "text": "Diabetes Mellitus glukozüri ve otonom nöropati üzerinden ÜSE riskini artırır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Premenopozal kadınlarda spermisid ve diyafram kullanımı vajinal florayı bozar", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Taş ve kateter gibi yabancı cisimler bakteriyel biyofilm oluşturarak eradikasyonu zorlaştırır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(20, "[TEKRAR SAYFASI - CHECKPOINT 2] Risk Faktörleri ve Predispozan Durumlar", "2. Bölümün kapsamlı pekiştirmesi: sistemik, lokal, yaş ve cinsiyete özgü riskler", "Bölüm Tekrarı", s20_narrative, s20_bullets, s20_elements))

    return slides
