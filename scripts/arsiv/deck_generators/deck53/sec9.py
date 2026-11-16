# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec9():
    slides = []

    # Slide 81: Adenomyozis Tanımı ve Bazal Tabaka İnvazyonu
    s81_narrative = (
        "Adenomyozis, endometrial dokunun uterus kas tabakası içine anormal yayılımı ile karakterize benign bir durumdur.\n\n"
        "- **Kesin Tanım:** Adenomyozis, **endometriumun bazal tabakasının myometrium içerisine "
        "doğru büyümesine** verilen isimdir.\n"
        "- **Mikroskopik Odaklar:** Myometriumun derin kısımlarında, düz kas demetleri arasında "
        "**endometrial stroma veya bezler ya da her ikisini içeren odaklar** bulunur.\n"
        "- **Devamlılık Gösterimi:** Seri kesitlerin bazılarında bu derin odaklar ile yüzey endometriumu "
        "arasında doğrudan anatomik bir devamlılık kanıtlanabilir.\n"
        "- **Köken Farkı:** İnvaze olan doku bazal tabaka olduğu için yüzeyel fonksiyonel tabaka "
        "karakteri taşımaz; bu durum lezyonun siklik yanıtını doğrudan belirler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Adenomyozis, endometriumun BAZAL tabakasının myometrium içerisine doğru büyümesidir; kas demetleri arasında stroma ve bezler bulunur."
    )
    s81_bullets = [
        "Adenomyozis: endometriumun bazal tabakasının myometrium içerisine büyümesidir.",
        "Myometrium kas demetleri arasında endometrial stroma, bezler ya da her ikisi bulunur.",
        "Bazı kesitlerde bu derin odaklar ile yüzey endometriumu arasında devamlılık izlenir."
    ]
    s81_elements = [
        make_cloze("Adenomyozis, endometriumun bazal tabakasının myometrium içerisine doğru büyümesine verilen isimdir.", "bazal tabakasının", "Adenomyoziste myometriuma büyüyen endometrial tabaka"),
        make_table("Adenomyozis Temel Tanı Kriterleri", ["Ölçüt", "Histolojik Nitelik", "Klinik Önemi"], [
            {"cells": [{"text": "Büyüyen Tabaka", "isMasked": False}, {"text": "Endometrium bazal tabakası", "isMasked": True, "hint": "derin yenileyici tabaka"}, {"text": "Fonksiyonel dökülme göstermez"}]},
            {"cells": [{"text": "Yerleşim Alanı", "isMasked": False}, {"text": "Myometrium kas demetleri arası", "isMasked": False}, {"text": "Reaktif myometrium hipertrofisi", "isMasked": True, "hint": "kas tabakası kalınlaşması"}]},
            {"cells": [{"text": "Yüzey İlişkisi", "isMasked": False}, {"text": "Bazı kesitlerde devamlılık izlenir", "isMasked": False}, {"text": "Aşağı doğru direkt invajinasyon"}]}
        ]),
        make_chain("Adenomyozis Oluşum Aşamaları", [
            "1. Endometriyal-Myometriyal Sınır Zayıflığı: Endometrium ile myometrium arasındaki bariyer bozulur.",
            "2. Bazal İstilası: Bazal tabaka hücreleri aşağıya myometriuma doğru uzanır.",
            "3. Kas İçi Odaklar: Kas lifleri arasında ektopik bez ve stroma adacıkları yerleşir.",
            "4. Duvar Kalınlaşması: Uterus diffüz olarak büyür ve adenomyozis tablosu oturur."
        ]),
        make_recall("Adenomyozis tam olarak nedir ve endometriumun hangi tabakasının nereye büyümesiyle oluşur?", "Endometriumun bazal tabakasının myometrium içerisine doğru büyümesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Adenomyozis Tanımı", [
            {"text": "Adenomyozis endometriumun bazal tabakasının myometrium içine büyümesidir.", "isLie": False, "explanation": "Doğru. Tanımıdır."},
            {"text": "Myometrium kas demetleri arasında endometrial stroma veya bezler bulunur.", "isLie": False, "explanation": "Doğru. Histolojik bulgudur."},
            {"text": "Adenomyozis sadece karaciğer lobülleri arasında görülen bir beyin tümörüdür.", "isLie": True, "explanation": "Tuzak! Adenomyozis endometrium bazal tabakasının UTERUS MYOMETRİUMUNA büyümesidir."},
            {"text": "Bazı kesitlerde yüzey endometriumu ile devamlılık saptanabilir.", "isLie": False, "explanation": "Doğru. İnvajinasyon kanıtıdır."}
        ]),
        make_quiz("Endometriumun bazal tabakasının myometrium içerisine doğru büyümesi ile karakterize lezyon hangisidir?", [
            {"key": "A", "text": "Adenomyozis", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'adenomyozis, endometriumun bazal tabakasının myometrium içerisine doğru büyümesine verilen isimdir' denmektedir."},
            {"key": "B", "text": "Endometrial polip", "isCorrect": False, "explanation": "Lümene doğru büyür."},
            {"key": "C", "text": "Karsinosarkom", "isCorrect": False, "explanation": "Malign mikst tümördür."},
            {"key": "D", "text": "Asherman sendromu", "isCorrect": False, "explanation": "İntrauterin yapışıklıktır."}
        ])
    ]
    slides.append(make_slide(81, "Adenomyozis Tanımı ve Bazal Tabaka İnvazyonu", "Bazal tabaka büyümesi, myometrium içi gland ve stroma odakları ve anatomik devamlılık", "Patoloji", s81_narrative, s81_bullets, s81_elements))

    # Slide 82: Adenomyoziste Uterus Büyümesi ve Siklik Kanama Yokluğu
    s82_narrative = (
        "Adenomyozisin patolojik anatomisi ve klinik semptomları, lezyonun bazalis kökeniyle doğrudan ilişkilidir.\n\n"
        "- **Reaktif Hipertrofi:** Uterus duvarı, kas demetleri arasına giren endometrial doku ve "
        "buna eşlik eden **reaktif myometrium hipertrofisi nedeni ile diffüz olarak kalınlaşmıştır** "
        "(globüler, simetrik büyük uterus).\n"
        "- **Siklik Kanama Yokluğu:** Adenomyozis odakları endometriumun bazal tabakasından köken "
        "aldığı için, endometriozisin aksine **bu odaklarda siklik menstrüel kanamalar İZLENMEZ**.\n"
        "- **Klinik Belirtiler:** Siklik kanama olmamasına rağmen miyometriyumun gerilmesi ve vasküler "
        "konjesyon nedeniyle **menoraji, dismenore ve menstruasyon öncesi pelvik ağrıya** neden olabilir.\n"
        "- **Ayırıcı Nüans:** Siklik kanamanın olmaması, adenomyozisi kistik kanama alanları oluşturan "
        "endometriozisten ayıran temel patofizyolojik özelliktir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Uterus reaktif myometrium hipertrofisiyle kalınlaşır; bazal tabaka kaynaklı olduğu için adenomyozis odaklarında menstrüel kanama izlenmez; menoraji ve dismenore yapar."
    )
    s82_bullets = [
        "Uterus duvarı endometrial doku ve reaktif myometrium hipertrofisi nedeniyle kalınlaşır.",
        "Adenomyozis odaklarında menstrüel kanamalar izlenmez (bazalis kökenlidir).",
        "Menoraji, dismenore ve menstruasyon öncesi pelvik ağrıya neden olabilir."
    ]
    s82_elements = [
        make_cloze("Uterus duvarı reaktif myometrium hipertrofisi ile kalınlaşır ve adenomyozis odaklarında menstrüel kanamalar izlenmez.", "menstrüel kanamalar izlenmez", "Adenomyozisin endometriozisten ayrılan kanama özelliği"),
        make_table("Adenomyozis Klinik ve Morfolojik Özellikleri", ["Özellik", "Adenomyozis Bulgusu", "Patofizyolojik Neden"], [
            {"cells": [{"text": "Uterus Boyutu", "isMasked": False}, {"text": "Diffüz kalınlaşmış ve büyümüş", "isMasked": True, "hint": "iri ve kalın duvarlı uterus"}, {"text": "Reaktif myometrium hipertrofisi"}]},
            {"cells": [{"text": "Odak İçi Kanama", "isMasked": False}, {"text": "Menstrüel kanama izlenmez", "isMasked": False}, {"text": "Bazal tabakanın siklusa yanıtsızlığı", "isMasked": True, "hint": "bazalis tabiatı"}]},
            {"cells": [{"text": "Klinik Semptomlar", "isMasked": False}, {"text": "Menoraji, dismenore, premenstrüel ağrı", "isMasked": False}, {"text": "Kas gerilmesi ve prostaglandin salınımı"}]}
        ]),
        make_chain("Adenomyozis Klinik Semptom Zinciri", [
            "1. Myometrium İnvazyonu: Bazal doku myometriuma yerleşir.",
            "2. Kas Hipertrofisi: Düz kas lifleri reaktif hipertrofiye uğrar.",
            "3. Kanama Yokluğu: Odaklar kanamaz ancak çevre kas dokusu sertleşir.",
            "4. Ağrı ve Menoraji: Uterus gevşeyemez; şiddetli dismenore ve menoraji gelişir."
        ]),
        make_recall("Adenomyozis odaklarında neden menstrüel siklik kanama izlenmez ve hastada hangi semptomlar görülür?", "Bazal tabaka kökenli olduğu için menstrüel kanama izlenmez; menoraji, dismenore ve menstruasyon öncesi pelvik ağrıya neden olur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Adenomyozis Kanama ve Semptomlar", [
            {"text": "Uterus duvarı reaktif myometrium hipertrofisi nedeni ile kalınlaşmıştır.", "isLie": False, "explanation": "Doğru. Makroskobik bulgudur."},
            {"text": "Adenomyozis odaklarında menstrüel kanamalar izlenmez.", "isLie": False, "explanation": "Doğru. Bazalis tabiatıdır."},
            {"text": "Adenomyozis odakları her ay 5 litre kan toplayarak devasa çikolata kistleri yapar.", "isLie": True, "explanation": "Tuzak! Adenomyozis odaklarında menstrüel kanama İZLENMEZ; çikolata kisti fonksiyonel endometrium içeren endometrioziste olur."},
            {"text": "Menoraji, dismenore ve menstruasyon öncesi pelvik ağrıya yol açabilir.", "isLie": False, "explanation": "Doğru. Klinik triyaddır."}
        ]),
        make_quiz("Adenomyozisin uterus duvarındaki morfolojik etkisi ve lezyon odaklarının siklik kanama durumu ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Reaktif myometrium hipertrofisi ile uterus kalınlaşır; odaklarda menstrüel kanama izlenmez", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'uterus duvarı endometrial doku ve reaktif myometrium hipertrofisi nedeni ile kalınlaşmıştır; menstrüel kanamalar izlenmez' denmektedir."},
            {"key": "B", "text": "Uterus tamamen küçülerek yok olur; odaklar sürekli fışkırır tarzda kanar", "isCorrect": False, "explanation": "Uterus büyür ve kanama olmaz."},
            {"key": "C", "text": "Sadece serviks mukozası kalınlaşır, myometrium etkilenmez", "isCorrect": False, "explanation": "Myometrium tutulur."},
            {"key": "D", "text": "Hastalık her zaman tamamen ağrısızdır ve kanama miktarını sıfırlar", "isCorrect": False, "explanation": "Dismenore ve menoraji yapar."}
        ])
    ]
    slides.append(make_slide(82, "Adenomyoziste Uterus Büyümesi ve Siklik Kanama Yokluğu", "Reaktif kas hipertrofisi, diffüz kalınlaşma, bazal tabiat nedeniyle kanamasız odaklar ve menoraji", "Patoloji", s82_narrative, s82_bullets, s82_elements))

    # Slide 83: Endometriozis Tanımı ve Epidemiyolojisi (%10 Kadın, %50 İnfertil)
    s83_narrative = (
        "Endometriozis, doğurganlık çağındaki kadınların yaşam kalitesini ve fertilitesini derinden etkileyen sistemik bir hastalıktır.\n\n"
        "- **Kesin Tanım:** Endometriozis, **endometrial bez yapıları ve stromasının endometriumun "
        "dışında farklı bir anatomik bölgede izlenmesi** ile karakterizedir.\n"
        "- **Toplum Sıklığı:** Reprodüktif dönemdeki **kadınların yaklaşık %10'unda** saptanır.\n"
        "- **İnfertilite Yükü:** İnfertilite (kısırlık) yakınması olan kadınların ise **yaklaşık %50'sinde** "
        "endometriozis mevcuttur.\n"
        "- **Klinik Tablo:** Dismenore (sancılı adet) ve kronik pelvik ağrının başlıca nedenidir.\n"
        "- **Ektopik Canlılık:** Uterus dışına yerleşen bu doku, normal fonksiyonel endometrium gibi "
        "hormonlara yanıt vererek her ay proliferasyon ve kanama döngüsünü sürdürür.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometriozis: endometrial gland ve stromanın uterus dışında olmasıdır; kadınların %10'unda, İNFERTİL kadınların %50'sinde izlenir."
    )
    s83_bullets = [
        "Endometrial bez ve stromanın endometrium dışında farklı bir bölgede izlenmesidir.",
        "Reprodüktif dönemdeki kadınların %10'unda görülür.",
        "İnfertilite yakınması olan kadınların %50'sinde izlenir; dismenore ve pelvik ağrı yapar."
    ]
    s83_elements = [
        make_cloze("Endometriozis kadınların yaklaşık %10'unda ve infertilite yakınması olanların %50'sinde izlenmektedir.", "%50'sinde", "İnfertil kadınlarda endometriozis görülme sıklığı"),
        make_table("Endometriozis Epidemiyolojik İstatistikleri", ["Popülasyon Grubu", "Görülme Sıklığı", "Klinik Yansıması"], [
            {"cells": [{"text": "Reprodüktif Çağdaki Kadınlar", "isMasked": False}, {"text": "%10", "isMasked": True, "hint": "yüzde on sıklık"}, {"text": "Toplumda yaygın jinekolojik sorun"}]},
            {"cells": [{"text": "İnfertilite Yakınması Olanlar", "isMasked": False}, {"text": "%50", "isMasked": False}, {"text": "Kısırlığın en önemli nedenlerinden biri", "isMasked": True, "hint": "hastaların yarısı"}]},
            {"cells": [{"text": "Kardinal Semptomlar", "isMasked": False}, {"text": "Dismenore ve kronik pelvik ağrı", "isMasked": False}, {"text": "Siklik lokal inflamasyon"}]}
        ]),
        make_chain("Endometriozis Patolojik Etki Akışı", [
            "1. Ektopik Yerleşim: Fonksiyonel endometrium over veya peritona yerleşir.",
            "2. Hormonal Yanıt: Östrojen ve progesteronla siklik olarak uyarılır.",
            "3. İnfertilite Tetikleme: Siklik kanama ve fibrozis sonucu tüpler ve overler hasarlanır.",
            "4. %50 İnfertilite: İnfertil kadınların yarısında bu tablo doğrulanır."
        ]),
        make_recall("Endometriozisin tıbbi tanımı nedir; reprodüktif dönem kadınlarında ve infertil kadınlarda görülme oranları kaçtır?", "Endometrial bez ve stromanın endometrium dışında izlenmesidir; reprodüktif kadınların %10'unda, infertil kadınların ise %50'sinde izlenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometriozis Epidemiyolojisi", [
            {"text": "Endometriozis endometrial bez ve stromanın uterus dışında izlenmesidir.", "isLie": False, "explanation": "Doğru. Tanımıdır."},
            {"text": "Reprodüktif dönemdeki kadınların yaklaşık %10'unda izlenir.", "isLie": False, "explanation": "Doğru. Toplum sıklığıdır."},
            {"text": "İnfertilite yakınması olan kadınlarda endometriozis görülme oranı sıfırdır, kısırlıkla hiçbir bağı yoktur.", "isLie": True, "explanation": "Tuzak! İnfertilite yakınması olan kadınların tam %50'sinde endometriozis saptanmaktadır."},
            {"text": "Dismenore ve pelvik ağrının başlıca nedenidir.", "isLie": False, "explanation": "Doğru. Kardinal semptomudur."}
        ]),
        make_quiz("Endometriozisin tanımı ve infertilite yakınması olan kadınlarda görülme sıklığı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Endometrial bez ve stromanın uterus dışında olmasıdır; infertil kadınların %50'sinde izlenir", "isCorrect": True, "explanation": "Ders notunda açıkça: 'endometrial bez yapıları ve stromasının endometriumun dışında izlenmesidir; reprodüktif kadınların %10'unda ve infertilite yakınması olanların %50'sinde izlenmektedir' denmektedir."},
            {"key": "B", "text": "Myometriumun kemiğe dönüşmesidir; infertil kadınlarda hiç görülmez", "isCorrect": False, "explanation": "Kemikleşme değildir."},
            {"key": "C", "text": "Sadece 80 yaş üstünde görülen benign bir poliptir", "isCorrect": False, "explanation": "Reprodüktif çağ hastalığıdır."},
            {"key": "D", "text": "Yalnızca akciğerde görülen bir tüberküloz kavitesidir", "isCorrect": False, "explanation": "Jinekolojik patolojidir."}
        ])
    ]
    slides.append(make_slide(83, "Endometriozis Tanımı ve Epidemiyolojisi (%10 Kadın, %50 İnfertil)", "Endometrial gland/stromanın ektopik yerleşimi, %10 toplum sıklığı ve infertil kadınlarda %50 prevalans", "Klinik Patoloji", s83_narrative, s83_bullets, s83_elements))

    # Slide 84: Anatomik Tutulum Yerleri ve Overde Çikolata Kisti
    s84_narrative = (
        "Endometriozis sıklıkla multifokal yerleşim gösteren ve pelvisten uzak organlara kadar yayılabilen bir hastalıktır.\n\n"
        "- **En Sık Pelvik Yerleşimler:** En sık pelvisteki dokuları tutar: **overler, fallop tüpleri, "
        "uterus ligamentleri (uterosakral ligamentler), Douglas boşluğu ve rektovajinal septum**.\n"
        "- **Nadir Uzak Yerleşimler:** Daha nadir olarak peritoneal kavitenin uzak bölgeleri, "
        "lenf bezleri, **akciğerler, kalp, çizgili kaslar ve kemikleri** tutabilir.\n"
        "- **Over Tutulumu ve Çikolata Kisti:** **Overler tutulduğunda lezyonlar içi dejenere eski kan "
        "ile dolu büyük kist halini alır ve 'çikolata kistlerine' (endometrioma) dönüşürler**.\n"
        "- **Kistik İçerik:** Her ay over dokusu içine kanayan fonksiyonel bezler, doku dışarı akamadığı "
        "için birikir; hemolize olan kan pıhtısı çikolata kıvamında kahverengi katranımsı bir sıvıya dönüşür.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] En sık yerleşim overlerdir; overler tutulduğunda içi dejenere kan ile dolu kistler 'çikolata kisti' (endometrioma) halini alır."
    )
    s84_bullets = [
        "En sık pelvisteki dokuları tutar: overler, tüpler, ligamentler, Douglas boşluğu.",
        "Nadir olarak akciğer, lenf bezi, kalp, kemik ve çizgili kasları tutabilir.",
        "Overler tutulduğunda içi dejenere kan dolu kistlere dönüşür: çikolata kisti (endometrioma)."
    ]
    s84_elements = [
        make_cloze("Overler tutulduğunda lezyonlar içi dejenere kan ile dolu büyük kist halini alır ve çikolata kistlerine dönüşürler.", "çikolata kistlerine", "Over endometriozisinin oluşturduğu dejenere kan kisti"),
        make_table("Endometriozis Anatomik Dağılımı", ["Bölge / Organ", "Tutulum Tipi", "Klinik Morfoloji"], [
            {"cells": [{"text": "Ovaryumlar (Overler)", "isMasked": False}, {"text": "En sık tutulum bölgesi", "isMasked": True, "hint": "en yaygın pelvik organ"}, {"text": "Çikolata kisti (endometrioma)"}]},
            {"cells": [{"text": "Pelvik Periton / Ligamentler", "isMasked": False}, {"text": "Douglas, uterosakral ligament", "isMasked": False}, {"text": "Kırmızı-mavi, barut yanığı nodüller", "isMasked": True, "hint": "pigmente peritoneal odaklar"}]},
            {"cells": [{"text": "Uzak Ekstrapelvik", "isMasked": False}, {"text": "Akciğer, plevra, lenf nodu, kemik", "isMasked": False}, {"text": "Katameniyal pnömotoraks / hemoptizi"}]}
        ]),
        make_chain("Çikolata Kisti Oluşum Zinciri", [
            "1. Ovaryal İmplantasyon: Fonksiyonel endometrial doku over korteksine yerleşir.",
            "2. Siklik Kanama: Her menstrüasyonda kist içine kanama gerçekleşir.",
            "3. Kan Hapsolması: Over parankiminde drenaj yolu olmadığı için kan birikir.",
            "4. Çikolata Kisti: Yıllar içinde dejenere kan katranlaşarak çikolata kistine dönüşür."
        ]),
        make_recall("Endometriozis en sık hangi organı tutar ve over tutulduğunda içi dejenere kanla dolu oluşan kistlere ne ad verilir?", "En sık overleri tutar; oluşan lezyonlara 'çikolata kisti' (endometrioma) adı verilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tutulum Yerleri ve Çikolata Kisti", [
            {"text": "Endometriozis en sık pelvisteki dokuları (overler, tüpler, ligamentler) tutar.", "isLie": False, "explanation": "Doğru. Tipik lokalizasyondur."},
            {"text": "Overler tutulduğunda dejenere kan dolu çikolata kistlerine dönüşür.", "isLie": False, "explanation": "Doğru. Endometrioma tanımıdır."},
            {"text": "Endometriozis akciğeri veya lenf bezlerini asla tutamaz, pelvis dışına çıkması fiziksel olarak imkansızdır.", "isLie": True, "explanation": "Tuzak! Endometriozis peritoneal boşluk dışında lenf bezleri, akciğerler, kalp, çizgili kas ve kemikleri de tutabilir."},
            {"text": "Douglas boşluğu pelviste sık tutulan alanlardandır.", "isLie": False, "explanation": "Doğru. Anatomik çukurluktur."}
        ]),
        make_quiz("Endometriozisin en sık tuttuğu organ ve burada içi dejenere eski kanla dolu oluşturduğu karakteristik kistik kitle hangisidir?", [
            {"key": "A", "text": "Over tutulumu; çikolata kisti", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'en sık pelvisteki dokuları (overler...) tutar; overler tutulduğunda lezyonlar içi dejenere kan ile dolu büyük kist halini alır ve çikolata kistlerine dönüşürler' denmektedir."},
            {"key": "B", "text": "Mide tutulumu; linitis plastika", "isCorrect": False, "explanation": "Mide karsinomudur."},
            {"key": "C", "text": "Karaciğer tutulumu; kist hidatik", "isCorrect": False, "explanation": "Ekinokok parazitidir."},
            {"key": "D", "text": "Böbrek tutulumu; polikistik böbrek", "isCorrect": False, "explanation": "Genetik hastalıktır."}
        ])
    ]
    slides.append(make_slide(84, "Anatomik Tutulum Yerleri ve Overde Çikolata Kisti", "Pelvik dağılım (over, tüp, ligament), uzak organ tutulumları ve overde çikolata kisti patolojisi", "Patoloji", s84_narrative, s84_bullets, s84_elements))

    # Slide 85: Köken Teorileri: Rejürjitasyon, Metaplastik ve Vasküler/Lenfatik
    s85_narrative = (
        "Endometrial dokunun uterus dışına nasıl ulaştığını açıklamak üzere üç ana patogenetik teori ileri sürülmüştür.\n\n"
        "- **1. Rejürjitasyon Teorisi (Sampson):** Son dönemde **en çok kabul gören teoridir**; "
        "menstruasyonda tüplerden **geriye akışı (retrograd menstrüasyon)** ve bunu izleyen peritoneal "
        "implantasyonu savunur; ancak lenf bezi ya da akciğerdeki lezyonları tek başına açıklayamaz.\n"
        "- **2. Metaplastik Teori (Meyer):** Endometriumun embriyolojik kökeni olarak kabul edilen "
        "**sölomik epitelin endometrium yönünde ayrımlaştığını (metaplazi)** ileri sürer; bu teori de "
        "akciğer ve lenf bezlerindeki uzak lezyonları açıklayamaz.\n"
        "- **3. Vasküler ya da Lenfatik Yayım Teorisi (Halban):** Pelvis dışı uzak organ (akciğer, kemik) "
        "ya da **intranodal (lenf nodu) yerleşimleri açıklamaya yöneliktir**; hücrelerin damar yoluyla taşındığını savunur.\n\n"
        "> [!NOTE]\n"
        "> Rejürjitasyon teorisi en çok kabul gören teoridir (geriye akış); Metaplastik teori sölomik epitel metaplazisidir; Vasküler/lenfatik teori pelvis dışı ve intranodal lezyonları açıklar."
    )
    s85_bullets = [
        "Rejürjitasyon teorisi: en çok kabul gören; menstrüel geriye akış ve implantasyonu savunur.",
        "Metaplastik teori: sölomik epitelin endometrium yönünde ayrımlaştığını ileri sürer.",
        "Vasküler/lenfatik yayım teorisi: pelvis dışı (akciğer) ve lenf bezi yerleşimlerini açıklar."
    ]
    s85_elements = [
        make_cloze("Endometrioziste son dönemde en çok kabul gören teori menstrüasyonda tüplerden geriye akışı savunan rejürjitasyon teorisidir.", "rejürjitasyon teorisi", "En çok kabul gören endometriozis teorisi"),
        make_table("Endometriozis Köken Teorileri Karşılaştırması", ["Teori Adı", "Öne Sürdüğü Mekanizma", "Açıklayamadığı / Açıkladığı Nokta"], [
            {"cells": [{"text": "Rejürjitasyon Teorisi", "isMasked": False}, {"text": "Tüplerden geriye akış (retrograd menstrüasyon)", "isMasked": True, "hint": "tüplerden peritoneal boşluğa dökülme"}, {"text": "En çok kabul gören; uzak organları açıklayamaz"}]},
            {"cells": [{"text": "Metaplastik Teori", "isMasked": False}, {"text": "Sölomik epitelin endometrial farklılaşması", "isMasked": False}, {"text": "Akciğer ve lenf bezi lezyonlarını açıklayamaz", "isMasked": True, "hint": "uzak yerleşim eksikliği"}]},
            {"cells": [{"text": "Vasküler / Lenfatik Yayım", "isMasked": False}, {"text": "Damarlar ve lenfatiklerle embolizasyon", "isMasked": False}, {"text": "Pelvis dışı ve lenf nodu yerleşimlerini açıklar"}]}
        ]),
        make_chain("Rejürjitasyon Patogenez Akışı", [
            "1. Menstruasyon: Kanamanın bir kısmı fallop tüplerinden peritona geri akar.",
            "2. Peritoneal Ekim: Dökülen canlı fonksiyonel hücreler over ve peritona yapışır.",
            "3. İmplantasyon ve Anjiyogenez: Ektopik hücreler kan damarları oluşturup yerleşir.",
            "4. Endometriozis Odağı: Her ay hormonlara yanıt veren aktif odaklar şekillenir."
        ]),
        make_recall("Endometriozisin patogenezinde en çok kabul gören teori hangisidir ve uzak organ tutulumunu hangi teori açıklar?", "En çok kabul gören rejürjitasyon teorisidir (retrograd menstrüasyon); uzak pelvis dışı ve intranodal tutulumları ise vasküler ya da lenfatik yayım teorisi açıklar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometriozis Teorileri", [
            {"text": "Rejürjitasyon teorisi son dönemde en çok kabul gören teoridir.", "isLie": False, "explanation": "Doğru. Sampson teorisidir."},
            {"text": "Metaplastik teori sölomik epitelin ayrımlaştığını ileri sürer.", "isLie": False, "explanation": "Doğru. Meyer teorisidir."},
            {"text": "Rejürjitasyon teorisi akciğer ve beyindeki lezyonları tek başına kusursuz şekilde açıklar.", "isLie": True, "explanation": "Tuzak! Ders notunda açıkça belirtildiği gibi: rejürjitasyon teorisi lenf bezi ya da akciğerdeki lezyonları AÇIKLAYAMAZ; bunu vasküler/lenfatik yayım teorisi açıklar."},
            {"text": "Vasküler/lenfatik yayım teorisi pelvis dışı ve intranodal yerleşimleri açıklamaya yöneliktir.", "isLie": False, "explanation": "Doğru. Halban teorisidir."}
        ]),
        make_quiz("Endometriozis patogenezinde en çok kabul gören teori ve uzak organ (akciğer, lenf nodu) tutulumunu açıklayan teori hangisidir?", [
            {"key": "A", "text": "En çok kabul gören: Rejürjitasyon teorisi | Uzak organları açıklayan: Vasküler/lenfatik yayım teorisi", "isCorrect": True, "explanation": "Ders notunda teoriler açıkça karşılaştırılmış ve bu ayrım vurgulanmıştır."},
            {"key": "B", "text": "En çok kabul gören: Hava yolu teorisi | Uzak organları açıklayan: Kuduz teorisi", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."},
            {"key": "C", "text": "Her iki durumu da tek başına sadece beslenme teorisi açıklar", "isCorrect": False, "explanation": "Diyet teorisi değildir."},
            {"key": "D", "text": "Endometriozis hiçbir teoriyle açıklanamayan uzay kaynaklı bir virüstür", "isCorrect": False, "explanation": "Biyolojik teoriler mevcuttur."}
        ])
    ]
    slides.append(make_slide(85, "Köken Teorileri: Rejürjitasyon, Metaplastik ve Vasküler/Lenfatik", "Rejürjitasyon (en kabul gören), metaplastik (sölomik epitel) ve vasküler/lenfatik (uzak organ) teorileri", "Patofizyoloji", s85_narrative, s85_bullets, s85_elements))

    # Slide 86: Siklik Kanama ve Makroskopi (Kırmızı-Maviden Sarı-Kahverengiye)
    s86_narrative = (
        "Endometriozis odakları, adenomyozisin aksine tam bir hormonal yanıt kabiliyetine sahiptir.\n\n"
        "- **Fonksiyonel Endometrium:** Adenomyozisin aksine, endometrioziste **hemen her zaman "
        "siklik kanama gösteren fonksiyonel bir endometrium** vardır.\n"
        "- **Makroskobik Renk Spektrumu:** Aberan odaklarda sürekli kan toplandığı için makroskobik "
        "olarak genellikle **kırmızı-maviden sarı-kahverengiye kadar değişen renklerde nodül ya da implantlar** "
        "(barut yanığı görünümlü) olarak izlenirler.\n"
        "- **Renklerin Patolojisi:** Taze kanama odakları kırmızı-mavi iken; eski kanamanın hemosiderine "
        "dönüşmesi ve makrofajlarca fagosite edilmesi nodüllere sarı-kahverengi rengini verir.\n"
        "- **Peritoneal Tebeşirlenme:** Yıllar içinde bu odaklar çevresinde yoğun fibrozis ve beyaz nedbe bantları oluşur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometrioziste siklik kanama gösteren fonksiyonel endometrium vardır; aberan odaklar kırmızı-maviden sarı-kahverengiye değişen nodül ve implantlar yapar."
    )
    s86_bullets = [
        "Adenomyozisin aksine hemen her zaman siklik kanama gösteren fonksiyonel endometrium vardır.",
        "Odaklarda kan toplandığı için kırmızı-maviden sarı-kahverengiye değişen renklerde görünür.",
        "Pelvik peritonda nodüller, implantlar ve barut yanığı lezyonları oluşturur."
    ]
    s86_elements = [
        make_cloze("Endometrioziste aberan odaklarda kan toplandığı için kırmızı-maviden sarı-kahverengiye kadar değişen renklerde nodül ya da implantlar görünür.", "sarı-kahverengiye", "Hemosiderin birikimiyle oluşan geç lezyon rengi"),
        make_table("Endometriozis Odaklarının Makroskobik Evrimi", ["Evre / Durum", "Makroskobik Renk", "Histolojik İçerik"], [
            {"cells": [{"text": "Taze / Erken Odak", "isMasked": False}, {"text": "Kırmızı - mavi renkli nodüller", "isMasked": True, "hint": "taze kan içeren lezyon"}, {"text": "Aktif fonksiyonel glandlar ve taze eritrositler"}]},
            {"cells": [{"text": "Eski / Kronik Odak", "isMasked": False}, {"text": "Sarı - kahverengi implantlar", "isMasked": False}, {"text": "Hemosiderin yüklü makrofajlar ve fibrozis", "isMasked": True, "hint": "demir pigmenti birikimi"}]},
            {"cells": [{"text": "İleri Evre Nedbe", "isMasked": False}, {"text": "Beyazımsı büzüşük yapışıklıklar", "isMasked": False}, {"text": "Organize skar dokusu"}]}
        ]),
        make_chain("Makroskobik Renk Dönüşüm Zinciri", [
            "1. Menstrüel Kanama: Ektopik odak periton boşluğuna kanar.",
            "2. Taze Hematom: Doku kırmızı-mavi nodül halini alır.",
            "3. Hemoglobin Yıkımı: Eritrositler parçalanır, hemosiderin açığa çıkar.",
            "4. Renk Değişimi: Makrofajlar pigmenti yutarak lezyonu sarı-kahverengiye boyar."
        ]),
        make_recall("Endometriozis odaklarının adenomyozisten temel fizyopatolojik farkı ve makroskobik renk skalası nasıldır?", "Endometrioziste siklik kanama gösteren fonksiyonel endometrium vardır; odaklar kırmızı-maviden sarı-kahverengiye kadar değişen renklerde nodül ya da implantlar şeklinde görünür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometriozis Makroskopisi", [
            {"text": "Endometrioziste hemen her zaman siklik kanama gösteren fonksiyonel bir endometrium vardır.", "isLie": False, "explanation": "Doğru. Adenomyozisten temel farkıdır."},
            {"text": "Aberan odaklarda kan toplandığı için kırmızı-maviden sarı-kahverengiye değişen renklerde nodüller görünür.", "isLie": False, "explanation": "Doğru. Renk spektrumudur."},
            {"text": "Endometriozis odakları parlak yeşil renktedir ve içinde saf klorofil pigmenti taşır.", "isLie": True, "explanation": "Tuzak! Endometriozis odakları kan ve hemosiderin içerdiğinden kırmızı-maviden sarı-kahverengiye değişen renklerdedir."},
            {"text": "Odaklar implant şeklinde peritona tutunur.", "isLie": False, "explanation": "Doğru. Makroskobik yerleşimdir."}
        ]),
        make_quiz("Endometriozis odaklarının kanama karakteri ve makroskobik renk görünümü ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Siklik kanama gösteren fonksiyonel endometrium içerir; kırmızı-maviden sarı-kahverengiye değişen nodüller yapar", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'endometrioziste hemen her zaman siklik kanama gösteren fonksiyonel bir endometrium vardır; aberan odaklarda kan toplandığı için kırmızı-maviden sarı-kahverengiye kadar değişen nodül ya da implantlar olarak görünürler' denmektedir."},
            {"key": "B", "text": "Hiçbir zaman kanama göstermez ve tamamen renksiz gaz baloncuklarıdır", "isCorrect": False, "explanation": "Kanama gösterir."},
            {"key": "C", "text": "Yalnızca menopozdan sonra taze kırmızı renk alır", "isCorrect": False, "explanation": "Reprodüktif dönemde aktiftir."},
            {"key": "D", "text": "Sadece bazal tabaka içerir ve kanama yapması imkansızdır", "isCorrect": False, "explanation": "Fonksiyonel tabaka içerir ve kanar."}
        ])
    ]
    slides.append(make_slide(86, "Siklik Kanama ve Makroskopi (Kırmızı-Maviden Sarı-Kahverengiye)", "Fonksiyonel endometrium, siklik kanama, kırmızı-mavi taze ve sarı-kahverengi eski lezyonlar", "Patoloji", s86_narrative, s86_bullets, s86_elements))

    # Slide 87: Fibrozis, Pelvik Yapışıklıklar ve Tubal Tıkanıklık
    s87_narrative = (
        "Endometriozisin yarattığı en ağır komplikasyonlar, tekrarlayan mikro-kanamaların tetiklediği organize fibrozisten kaynaklanır.\n\n"
        "- **Kronik İnflamasyon:** Ektopik odaklardan çevre periton boşluğuna kan sızması, "
        "yoğun kimyasal irritasyon ve kronik yabancı cisim reaksiyonu doğurur.\n"
        "- **Organize Fibrozis:** **Kanın sızması ve organizasyonu yaygın fibrozise ve pelvik "
        "yapılarda şiddetli yapışıklıklara (adezyonlara)** yol açar.\n"
        "- **Tubal ve Ovaryal Hasar:** Bu fibrotik yapışıklıklar, **tubaların fimbria uçlarının "
        "tıkanmasına ve overlerde ciddi şekil bozukluklarına** neden olur.\n"
        "- **Sterilitenin Anatomik Temeli:** Fimbrianın tıkanması ve overin pelvik duvara yapışması, "
        "ovulasyon anında atılan oositin tubaya alınmasını fiziksel olarak imkansız hale getirerek kısırlık (sterilite) yaratır.\n\n"
        "> [!NOTE]\n"
        "> Kanın sızması ve organizasyonu yaygın fibrozise, pelvik yapışıklıklara, tubaların fimbria uçlarının tıkanmasına ve over şekil bozukluklarına yol açar."
    )
    s87_bullets = [
        "Kanın sızması ve organizasyonu pelviste yaygın fibrozis ve yapışıklıklara yol açar.",
        "Tubaların fimbria uçları tıkanır ve overlerde şekil bozuklukları oluşur.",
        "Bu anatomik distorsiyon oosit alımını engelleyerek sterilite ve kronik pelvik ağrı yapar."
    ]
    s87_elements = [
        make_cloze("Kanın sızması ve organizasyonu yaygın fibrozise, pelvik yapılarda yapışıklıklara ve tubaların fimbria uçlarının tıkanmasına yol açar.", "fimbria uçlarının tıkanmasına", "Adezyonların tüplerde yol açtığı anatomik tıkanıklık"),
        make_table("Endometriozisin Yapısal Pelvik Komplikasyonları", ["Etkilenen Yapı", "Gelişen Patoloji", "Klinik Sonuç"], [
            {"cells": [{"text": "Pelvik Periton ve Boşluk", "isMasked": False}, {"text": "Yaygın fibrozis ve sert yapışıklıklar", "isMasked": True, "hint": "yoğun adezyonlar"}, {"text": "Kronik inatçı pelvik ağrı"}]},
            {"cells": [{"text": "Fallop Tüpleri (Tubalar)", "isMasked": False}, {"text": "Fimbria uçlarının tıkanması", "isMasked": False}, {"text": "Mekanik infertilite / sterilite", "isMasked": True, "hint": "tüplerin kapanması"}]},
            {"cells": [{"text": "Over Dokusu", "isMasked": False}, {"text": "Şekil bozuklukları ve yapışıklık", "isMasked": False}, {"text": "Fiks over sendromu"}]}
        ]),
        make_chain("Fibrozis ve İnfertilite Mekanizması", [
            "1. Peritoneal Kanama: Odaklardan her ay kan sızar.",
            "2. Fibrin Eksüdasyonu: Kan organize olarak fibroblast göçünü uyarır.",
            "3. Yaygın Adezyon: Pelvik organlar birbirine sıkıca yapışır.",
            "4. Tubal Obstrüksiyon: Fimbria uçları tıkanır ve kısırlık oturur."
        ]),
        make_recall("Endometrioziste kanın sızması ve organizasyonu pelvik organlarda hangi iki temel yapısal harabiyete yol açar?", "Tubaların fimbria uçlarının tıkanmasına ve overlerde şekil bozukluklarına (yaygın fibrozis ve yapışıklıklarla birlikte) yol açar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fibrozis ve Pelvik Yapışıklıklar", [
            {"text": "Kanın sızması ve organizasyonu yaygın fibrozise yol açar.", "isLie": False, "explanation": "Doğru. Patofizyolojik sonuçtur."},
            {"text": "Tubaların fimbria uçlarının tıkanmasına neden olabilir.", "isLie": False, "explanation": "Doğru. İnfertilite mekanizmasıdır."},
            {"text": "Endometriozis kanamaları pelviste tüm yapışıklıkları tamamen eriterek organları birbirinden uzaklaştırır.", "isLie": True, "explanation": "Tuzak! Kanın sızması ve organizasyonu pelvik yapılarda şiddetli YAPIŞIKLIKLARA ve tubal tıkanıklığa yol açar."},
            {"text": "Overlerde şekil bozuklukları oluşur.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Endometrioziste kanın peritona sızması ve organizasyonu sonucunda ortaya çıkan yapısal komplikasyonlar hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Yaygın fibrozis, pelvik yapışıklıklar, tubaların fimbria uçlarının tıkanması ve over şekil bozuklukları", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'kanın sızması ve organizasyonu yaygın fibrozise, pelvik yapılarda yapışıklıklara, tubaların fimbria uçlarının tıkanmasına ve overlerde şekil bozukluklarına yol açar' denmektedir."},
            {"key": "B", "text": "Tüm tüplerin kendi kendine genişleyip 10 metre olması", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."},
            {"key": "C", "text": "Peritonun saf yağa dönüşmesi", "isCorrect": False, "explanation": "Fibrozis bağ dokusudur."},
            {"key": "D", "text": "Kemik iliğinde hemoglobin tükenmesi", "isCorrect": False, "explanation": "Pelvik lezyonla doğrudan ilgisizdir."}
        ])
    ]
    slides.append(make_slide(87, "Fibrozis, Pelvik Yapışıklıklar ve Tubal Tıkanıklık", "Kronik kan sızması, organizasyon, yaygın pelvik adezyonlar, fimbria tıkanıklığı ve infertilite", "Patofizyoloji", s87_narrative, s87_bullets, s87_elements))

    # Slide 88: Histopatolojik Tanı Triyadı (3 Özellikten 2'si Kuralı)
    s88_narrative = (
        "Endometriozisin patoloji raporunda kesinleştirilebilmesi için uluslararası kabul görmüş histolojik tanı triyadı kullanılır.\n\n"
        "- **Kardinal Triyad Kuralı:** Tüm anatomik yerleşim yerlerinde **histolojik tanı üç özellikten "
        "en az ikisinin (2/3) gösterilmesine dayanır**.\n"
        "- **1. Bileşen: Endometrial Bezler:** Ektopik alanda kolumnar veya küboid epitel ile döşeli glandüler yapılar.\n"
        "- **2. Bileşen: Endometrial Stroma:** Bezlerin çevresinde yer alan karakteristik selüler endometrial stroma hücreleri.\n"
        "- **3. Bileşen: Hemosiderin Yüklü Makrofajlar:** Eski ve tekrarlayan kanamaların dokudaki "
        "kanıtı olan hemosiderofajlar (demir yüklü histiositler).\n"
        "- **Tanısal Esneklik:** Bazen bezler basınca bağlı basıklaşıp kaybolsa bile, stroma ve hemosiderin "
        "makrofajlarının birlikteliği (3'ten 2'si) kesin tanı için yeterlidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Histolojik tanı üç özellikten ikisinin (2/3) gösterilmesine dayanır: 1) Endometrial bezler, 2) Endometrial stroma, 3) Hemosiderin yüklü makrofajlar."
    )
    s88_bullets = [
        "Histolojik tanı üç özellikten ikisinin gösterilmesine dayanır.",
        "Üç tanısal kriter: 1) Endometrial bezler, 2) Stroma, 3) Hemosiderin yüklü makrofajlar.",
        "Bu üç özellikten en az ikisinin bulunması kesin endometriozis tanısını koydurur."
    ]
    s88_elements = [
        make_cloze("Endometrioziste histolojik tanı üç özellikten ikisinin gösterilmesine dayanır: endometrial bezler, stroma ve hemosiderin yüklü makrofajlar.", "üç özellikten ikisinin", "Endometriozis tanı kuralı oranı"),
        make_table("Endometriozis Histopatolojik Tanı Triyadı", ["Triyad Bileşeni", "Histolojik Karakter", "Tanıdaki Rolü"], [
            {"cells": [{"text": "1. Endometrial Bezler", "isMasked": False}, {"text": "Tubuler / kistik glandüler yapılar", "isMasked": True, "hint": "ektopik bezler"}, {"text": "Glandüler komponent"}]},
            {"cells": [{"text": "2. Endometrial Stroma", "isMasked": False}, {"text": "Kompakt, selüler endometrial stroma", "isMasked": False}, {"text": "Stromal matriks desteği", "isMasked": True, "hint": "özgül bağ dokusu"}]},
            {"cells": [{"text": "3. Hemosiderin Yüklü Makrofajlar", "isMasked": False}, {"text": "Kahverengi demir pigmentli fagositler", "isMasked": False}, {"text": "Geçirilmiş siklik kanama kanıtı"}]}
        ]),
        make_chain("Histolojik Tanı Karar Algoritması", [
            "1. Şüpheli Biyopsi: Pelvik kist veya periton biyopsisi incelenir.",
            "2. Triyad Araması: Bezler, stroma ve hemosiderin makrofajları taranır.",
            "3. 2/3 Kuralı Testi: Bu üç bileşenden en az ikisinin varlığı doğrulanır.",
            "4. Raporlama: 'Endometriozis ile uyumlu' kesin histopatolojik tanı verilir."
        ]),
        make_recall("Endometriozisin kesin histopatolojik tanısı hangi üç özellikten en az ikisinin gösterilmesine dayanır?", "1) Endometrial bezler, 2) Endometrial stroma, 3) Hemosiderin yüklü makrofajlar (bu 3 özellikten en az 2'si şarttır)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometriozis Tanı Triyadı", [
            {"text": "Histolojik tanı üç özellikten ikisinin gösterilmesine dayanır.", "isLie": False, "explanation": "Doğru. Altın kuraldır."},
            {"text": "Endometrial bezler ve stroma bu özellikler arasındadır.", "isLie": False, "explanation": "Doğru. İki temel dokudur."},
            {"text": "Endometriozis tanısı için mutlaka canlı bir böbrek glomerülü görülmesi şarttır.", "isLie": True, "explanation": "Tuzak! Endometriozis tanı triyadı: endometrial bezler, stroma ve hemosiderin yüklü makrofajlardır; böbrek dokusuyla ilgisi yoktur."},
            {"text": "Hemosiderin yüklü makrofajlar triyadın üçüncü bileşenidir.", "isLie": False, "explanation": "Doğru. Kanama kanıtıdır."}
        ]),
        make_quiz("Endometriozisin histopatolojik tanısının konulabilmesi için aşağıdaki üç özellikten en az ikisinin gösterilmesi gerekir?", [
            {"key": "A", "text": "Endometrial bezler, stroma ve hemosiderin yüklü makrofajlar", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'tüm yerleşim yerlerinde histolojik tanı üç özellikten ikisinin gösterilmesine dayanır: endometrial bezler, stroma ve hemosiderin yüklü makrofajlar' denmektedir."},
            {"key": "B", "text": "Nöronlar, miyelin kılıf ve astrositler", "isCorrect": False, "explanation": "Beyin dokusudur."},
            {"key": "C", "text": "Osteositler, kondrositler ve safra kristalleri", "isCorrect": False, "explanation": "İlgisiz dokulardır."},
            {"key": "D", "text": "Sadece keratin incileri ve amyloid plakları", "isCorrect": False, "explanation": "Kanser ve dejenerasyon bulgularıdır."}
        ])
    ]
    slides.append(make_slide(88, "Histopatolojik Tanı Triyadı (3 Özellikten 2'si Kuralı)", "Gland, stroma ve hemosiderofaj üçlüsü ve 3 özellikten en az 2'sinin bulunması kuralı", "Histopatoloji", s88_narrative, s88_bullets, s88_elements))

    # Slide 89: Klinik Belirtiler ve Tutulum Yerine Göre Semptomlar
    s89_narrative = (
        "Endometriozisin klinik semptomları, ektopik odakların pelviste hangi anatomik yapıları infiltre ettiğine birebir bağlıdır.\n\n"
        "- **Pelvik Rahatsızlık ve Sterilite:** Ovidukt (tüpler) ve overlerin aşırı nedbeleşmesi "
        "**alt kadranlarda kronik rahatsızlıklar oluşturur ve steriliteye (kısırlık) neden olur**.\n"
        "- **Rektal Duvar Tutulumu:** Ektopik odakların rektovajinal septumu ve rektum serozasını tutması, "
        "hastalarda **dışkılama sırasında şiddetli ağrıya (diskezi)** yol açar.\n"
        "- **Uterus ve Mesane Tutulumu:** Uterus serozası tutulduğunda **disparoni (ağrılı cinsel ilişki)**; "
        "mesane serozası ve duvarı tutulduğunda ise **dizüri (ağrılı idrar yapma)** izlenir.\n"
        "- **Ağır Dismenore:** Çevresindeki yoğun fibrotik yapışıklıklar ve prostaglandin salınımı "
        "nedeniyle hastalarda **ağır bir dismenore ve pelvik ağrı** tablosu hakimdir.\n\n"
        "> [!IMPORTANT]\n"
        "> [KLİNİK BAĞLANTI] Dışkılamada ağrı → rektal duvar; Disparoni → uterus serozası; Dizüri → mesane serozası; Ovidukt/over nedbesi → sterilite ve alt kadran ağrısı."
    )
    s89_bullets = [
        "Ovidukt ve over nedbeleşmesi alt kadran rahatsızlığı ve sterilite yapar.",
        "Dışkılama sırasında ağrı rektal duvar tutulumunu gösterir.",
        "Disparoni ve dizüri sırasıyla uterus ve mesane serozasının tutulduğunu gösterir; ağır dismenore izlenir."
    ]
    s89_elements = [
        make_cloze("Endometrioziste dışkılama sırasında ağrı rektal duvarın, disparoni ve dizüri ise uterus ve mesane serozasının tutulduğunu gösterir.", "rektal duvarın", "Dışkılamada ağrıya yol açan tutulum yeri"),
        make_table("Endometriozis Tutulum Yeri ve Semptom Eşleşmesi", ["Semptom", "Tutulan Anatomik Yapı", "Fizyopatolojik Mekanizma"], [
            {"cells": [{"text": "Dışkılamada Ağrı (Diskezi)", "isMasked": False}, {"text": "Rektal duvar ve rektovajinal septum", "isMasked": True, "hint": "bağırsak duvarı tutulumu"}, {"text": "Dışkı geçerken serozal çekilme"}]},
            {"cells": [{"text": "Disparoni (Ağrılı İlişki)", "isMasked": False}, {"text": "Uterus serozası ve uterosakral ligament", "isMasked": False}, {"text": "Pelvik taban gerilmesi", "isMasked": True, "hint": "uterin serozal ağrı"}]},
            {"cells": [{"text": "Dizüri (Ağrılı İdrar)", "isMasked": False}, {"text": "Mesane serozası", "isMasked": True, "hint": "idrar torbası dış zarı"}, {"text": "Mesane dolumu ve miksiyon ağrısı"}]},
            {"cells": [{"text": "Sterilite (Kısırlık)", "isMasked": False}, {"text": "Ovidukt ve over aşırı nedbeleşmesi", "isMasked": False}, {"text": "Fimbrial tıkanıklık ve oosit alım engeli"}]}
        ]),
        make_chain("Semptom Odaklı Lokalizasyon Zinciri", [
            "1. Anamnez: Hasta diskezi, disparoni veya dizüri şikayetini ifade eder.",
            "2. Rektal Ağrı: Defekasyonda ağrı varsa rektal duvar invazyonu düşünülür.",
            "3. Cinsel ve Üriner Ağrı: Disparonide uterus serozası, dizüride mesane serozası taranır.",
            "4. İnfertilite Tetkiki: Ovidukt ve over nedbeleşmesi laparoskopi ile teyit edilir."
        ]),
        make_recall("Endometrioziste dışkılama sırasında ağrı, disparoni ve dizüri sırasıyla hangi anatomik yapıların tutulduğunu gösterir?", "Dışkılama sırasında ağrı rektal duvarın; disparoni uterus serozasının; dizüri ise mesane serozasının tutulduğunu gösterir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometriozis Semptomları", [
            {"text": "Dışkılama sırasında ağrı rektal duvarın tutulduğunu gösterir.", "isLie": False, "explanation": "Doğru. Ders notu eşleşmesidir."},
            {"text": "Disparoni ve dizüri sırasıyla uterus ve mesane serozasının tutulduğunu gösterir.", "isLie": False, "explanation": "Doğru. Klinik semptomlardır."},
            {"text": "Endometriozisli hastalar cinsel ilişki veya dışkılamada hiçbir zaman en ufak bir ağrı hissetmezler.", "isLie": True, "explanation": "Tuzak! Rektal tutulumda dışkılamada ağrı, uterus serozasında disparoni, mesanede dizüri ve ağır dismenore görülür."},
            {"text": "Ovidukt ve overlerin aşırı nedbeleşmesi steriliteye neden olur.", "isLie": False, "explanation": "Doğru. Kısırlık mekanizmasıdır."}
        ]),
        make_quiz("Endometriozisli bir kadında dışkılama sırasında ağrı (diskezi) olması öncelikle hangi anatomik yapının tutulduğunu gösterir?", [
            {"key": "A", "text": "Rektal duvarın tutulduğunu", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'dışkılama sırasında ağrı rektal duvarın tutulduğunu gösterir' denmektedir."},
            {"key": "B", "text": "Beyincik korteksinin tutulduğunu", "isCorrect": False, "explanation": "Santral sinir sistemidir."},
            {"key": "C", "text": "Dalak kapsülünün tutulduğunu", "isCorrect": False, "explanation": "Sol üst kadrandır."},
            {"key": "D", "text": "Sadece kulak zarının tutulduğunu", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."}
        ])
    ]
    slides.append(make_slide(89, "Klinik Belirtiler ve Tutulum Yerine Göre Semptomlar", "Rektal duvar (diskezi), uterus serozası (disparoni), mesane serozası (dizüri) ve ovidukt nedbesi (sterilite)", "Klinik Patoloji", s89_narrative, s89_bullets, s89_elements))

    # Slide 90: [TEKRAR SAYFASI - CHECKPOINT 9] Adenomyozis ve Endometriozis
    s90_narrative = (
        "Bu tekrar sayfasında 9. Bölümde ele aldığımız adenomyozis ve endometriozis arasındaki "
        "anatomik, fizyopatolojik, histolojik ve klinik farkları konsolide ediyoruz.\n\n"
        "- **Adenomyozis:** Endometriumun bazal tabakasının myometrium içine büyümesidir; uterus "
        "reaktif kas hipertrofisiyle diffüz büyür; bazalis kökenli olduğu için menstrüel kanama izlenmez; "
        "menoraji ve dismenore yapar.\n"
        "- **Endometriozis:** Endometrial dokunun uterus dışında olmasıdır; kadınların %10'unda, "
        "infertil kadınların %50'sinde izlenir; en sık overdedir (içi dejenere kan dolu 'çikolata kisti').\n"
        "- **Fizyopatoloji ve Makroskopi:** Endometriozis siklik kanayan fonksiyonel tabakadır; odaklarda "
        "kırmızı-maviden sarı-kahverengiye nodüller görülür; kan sızması yaygın fibrozis ve fimbria tıkanıklığı yapar.\n"
        "- **Histolojik Tanı Triyadı (3'ten 2'si):** Endometrial bezler, stroma ve hemosiderin yüklü makrofajlar.\n"
        "- **Semptom Eşleşmesi:** Dışkılamada ağrı (rektal duvar), disparoni (uterus serozası), dizüri (mesane serozası).\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Adenomyozis: bazal tabaka, myometrium içi, kanamaz; Endometriozis: uterus dışı, siklik kanar, %50 infertilite, çikolata kisti, 3'ten 2'si kuralı (bez, stroma, hemosiderofaj)."
    )
    s90_bullets = [
        "Adenomyozis: bazal tabaka myometriumda, siklik kanamaz, reaktif hipertrofi ile kalınlaşmış uterus.",
        "Endometriozis: fonksiyonel doku uterus dışında, siklik kanar, kadınların %10'unda, infertil kadınların %50'sinde, overde çikolata kisti.",
        "Histolojik tanı (3'ten 2'si): bezler, stroma, hemosiderin makrofajları; dışkılamada ağrı = rektal duvar."
    ]
    s90_elements = [
        make_cloze("Endometriozis histolojik tanısı üç özellikten ikisinin gösterilmesine dayanır: endometrial bezler, stroma ve hemosiderin yüklü makrofajlar.", "hemosiderin yüklü makrofajlar", "Endometriozis tanı triyadının demir pigmentli hücresi"),
        make_table("9. Bölüm Büyük Adenomyozis vs Endometriozis Tablosu", ["Özellik", "Adenomyozis", "Endometriozis"], [
            {"cells": [{"text": "Köken Doku", "isMasked": False}, {"text": "Endometrium bazal tabakası", "isMasked": True, "hint": "derin bazalis"}, {"text": "Fonksiyonel endometrium (ektopik)"}]},
            {"cells": [{"text": "Siklik Kanama", "isMasked": False}, {"text": "Menstrüel kanama izlenmez", "isMasked": False}, {"text": "Siklik kanar (çikolata kisti)", "isMasked": True, "hint": "düzenli kanama özelliği"}]},
            {"cells": [{"text": "Uterus Morfolojisi", "isMasked": False}, {"text": "Diffüz kalınlaşmış ve büyümüş", "isMasked": False}, {"text": "Uterus normal boyutlu olabilir"}]},
            {"cells": [{"text": "Tanısal Kriter", "isMasked": False}, {"text": "Myometriumda gland ve stroma", "isMasked": False}, {"text": "3'ten 2'si: bez, stroma, hemosiderofaj", "isMasked": True, "hint": "üç özellikten ikisi kuralı"}]}
        ]),
        make_chain("Bölüm 9 Konsolidasyon Akışı", [
            "1. Adenomyozis: Bazalis myometriuma dalar → kas hipertrofisi → kanamasız odaklar → menoraji.",
            "2. Endometriozis: Fonksiyonel doku overe/peritona yerleşir → siklik kanar → çikolata kisti.",
            "3. Fibrozis ve Kısırlık: Kan sızması fimbriaları tıkar → %50 infertilite gelişir.",
            "4. Patolojik Rapor: Biyopside gland, stroma ve hemosiderin makrofajlarından 2'si kanıtlanır."
        ]),
        make_recall("9. Bölümün iki kardinal kuralı: Adenomyozis ile endometriozisin siklik kanama farkı nedir ve endometriozis tanı triyadı nedir?", "Adenomyozis odaklarında siklik kanama İZLENMEZ (bazalis kökenli); endometriozis ise siklik kanar. Tanı triyadı (3'ten 2'si): endometrial bezler, stroma ve hemosiderin yüklü makrofajlardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 9. Bölüm Konsolidasyonu", [
            {"text": "Adenomyozis odaklarında menstrüel kanamalar izlenmez.", "isLie": False, "explanation": "Doğru. Bazalis karakteridir."},
            {"text": "Endometriozis overde çikolata kistlerine dönüşebilir.", "isLie": False, "explanation": "Doğru. Tipik kisttir."},
            {"text": "Endometriozis tanısı için mutlaka kıkırdak ve kemik hücresi bulunması şarttır.", "isLie": True, "explanation": "Tuzak! Endometriozis tanısı bez, stroma ve hemosiderin yüklü makrofajlardan en az ikisinin gösterilmesine dayanır."},
            {"text": "Dışkılama sırasında ağrı rektal duvar tutulumunu gösterir.", "isLie": False, "explanation": "Doğru. Klinik semptomdur."}
        ]),
        make_quiz("Adenomyozis ve endometriozis ile ilgili aşağıdaki karşılaştırmalardan hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Adenomyoziste menstrüel kanama izlenmez; endometrioziste fonksiyonel doku siklik kanar ve tanıda 3 özellikten 2'si aranır", "isCorrect": True, "explanation": "Ders notunun tüm temel ilkelerini eksiksiz ve doğru özetleyen seçenektir."},
            {"key": "B", "text": "Adenomyozis sadece karaciğerde, endometriozis ise sadece beyinde görülür", "isCorrect": False, "explanation": "Uterus ve pelvik lezyonlardır."},
            {"key": "C", "text": "Endometriozis infertil kadınların hiçbirinde görülmez", "isCorrect": False, "explanation": "İnfertil kadınların %50'sinde görülür."},
            {"key": "D", "text": "Çikolata kisti sadece adenomyoziste görülür, endometrioziste kist olmaz", "isCorrect": False, "explanation": "Çikolata kisti over endometriozisinde olur."}
        ])
    ]
    slides.append(make_slide(90, "[TEKRAR SAYFASI - CHECKPOINT 9] Adenomyozis ve Endometriozis", "9. Bölümün konsolidasyonu: adenomyozis (bazalis, kanamasız), endometriozis (%50 infertil, çikolata kisti), 3'ten 2'si kuralı ve diskezi", "Bölüm Tekrarı", s90_narrative, s90_bullets, s90_elements))

    return slides
