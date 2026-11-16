# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec6():
    slides = []

    # Slide 51: Düzensiz Proliferatif Endometrium: Tanım ve Morfoloji
    s51_narrative = (
        "Düzensiz proliferatif endometrium, normal proliferatif fazın düzenli mimarisinin bozulduğu "
        "fakat henüz hiperplazi eşiğine ulaşmadığı bir durumdur.\n\n"
        "- **Mimari Bozulma:** Normal proliferatif endometriumdaki uniform, düzenli tübüler görünüm "
        "kaybolmuştur; **bazıları dar çaplı, bazıları kistik genişlemiş, dallanmış bezler yoğun stroma "
        "içinde** dağınık yerleşim gösterir.\n"
        "- **Hücresel Görünüm:** Glandları döşeyen epitel hücreleri sitolojik olarak tamamen normal "
        "proliferatif faz karakterindedir; nükleer psödostratifikasyon ve mitotik figürler izlenir.\n"
        "- **Stroma Bütünlüğü:** Yoğun selüler stroma bezler arasında geniş alanlar kaplar.\n"
        "- **Tanı Kriteri:** Lezyonun temel mikroskopik özelliği, gland/stroma oranının belirgin "
        "şekilde artmamış olması ve mimari düzensizliğin fokal kalmasıdır.\n\n"
        "> [!NOTE]\n"
        "> Düzensiz proliferatif endometriumda uniform görünüm bozulmuştur; bazıları dar, bazıları kistik genişlemiş bezler yoğun stroma içindedir."
    )
    s51_bullets = [
        "Normal proliferatif endometriumdaki uniform görünüm bozulmuştur.",
        "Bazıları dar çaplı, bazıları kistik genişlemiş ve dallanmış bezler izlenir.",
        "Bu düzensiz bezler yoğun bir stroma içine yerleşmiştir; epitel proliferatiftir."
    ]
    s51_elements = [
        make_cloze("Düzensiz proliferatif endometriumda bazıları dar çaplı, bazıları kistik genişlemiş, dallanmış bezler yoğun stroma içinde yerleşmişlerdir.", "yoğun stroma", "Düzensiz bezleri çevreleyen bağ dokusu"),
        make_table("Düzensiz Proliferatif Endometrium Morfolojisi", ["Bileşen", "Mikroskopik Görünüm", "Ayırıcı Anlamı"], [
            {"cells": [{"text": "Endometrial Bezler", "isMasked": False}, {"text": "Bazıları dar, bazıları kistik dilate ve dallanmış", "isMasked": True, "hint": "düzensiz bez çapları"}, {"text": "Uniformitenin kaybolması"}]},
            {"cells": [{"text": "Bez/Stroma Oranı", "isMasked": False}, {"text": "Büyük ölçüde normal korunmuştur", "isMasked": False}, {"text": "Hiperplaziden ayıran temel kriter", "isMasked": True, "hint": "stroma miktarının korunması"}]},
            {"cells": [{"text": "Bez Epiteli", "isMasked": False}, {"text": "Normal proliferatif karakterde", "isMasked": False}, {"text": "Mitoz var, atipi yok"}]}
        ]),
        make_chain("Düzensiz Proliferasyon Morfolojik Oluşumu", [
            "1. Hormonal Asenkroni: Östrojen uyarımı kesintili ve düzensiz gelir.",
            "2. Asimetrik Büyüme: Bazı bezler dar kalırken komşu bezler kistik genişler.",
            "3. Dallanma: Bazı tübüllerde tomurcuklanma ve dallanmalar şekillenir.",
            "4. Düzensiz Tablo: Yoğun stroma içinde değişken çaplı bezler izlenir."
        ]),
        make_recall("Düzensiz proliferatif endometriumun mikroskopik incelemesinde bezlerin ve stromanın morfolojik görünümü nasıldır?", "Normal proliferatif uniformite bozulmuştur; bazıları dar çaplı, bazıları kistik genişlemiş, dallanmış bezler yoğun stroma içine yerleşmiştir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Düzensiz Proliferatif Endometrium", [
            {"text": "Normal proliferatif endometriumdaki uniform görünüm bozulmuştur.", "isLie": False, "explanation": "Doğru. Düzensizliğin tanımıdır."},
            {"text": "Bazıları dar çaplı, bazıları kistik genişlemiş bezler yoğun stroma içindedir.", "isLie": False, "explanation": "Doğru. Tipik histolojidir."},
            {"text": "Düzensiz proliferatif endometriumda stroma tamamen erimiştir ve bezler sırt sırta vererek invaziv karsinom oluşturmuştur.", "isLie": True, "explanation": "Tuzak! Düzensiz proliferasyonda yoğun stroma mevcuttur ve bez-stroma oranı büyük ölçüde normal korunmuştur."},
            {"text": "Gland epiteli proliferatif görünümdedir.", "isLie": False, "explanation": "Doğru. Mitoz izlenebilir."}
        ]),
        make_quiz("Düzensiz proliferatif endometriumun mikroskopik incelemesinde bezlerin ve stromanın mimarisi nasıldır?", [
            {"key": "A", "text": "Bazıları dar çaplı, bazıları kistik genişlemiş ve dallanmış bezler yoğun stroma içindedir", "isCorrect": True, "explanation": "Ders notunda açıkça: 'normal proliferatif endometriumdaki uniform görünüm bozulmuş olup bazıları dar çaplı, bazıları kistik genişlemiş, dallanmış bezler yoğun stroma içinde yerleşmişlerdir' denmektedir."},
            {"key": "B", "text": "Bezler tamamen kaybolmuş, sadece saf hyalin kıkırdak kalmıştır", "isCorrect": False, "explanation": "Kıkırdak dokusu değildir."},
            {"key": "C", "text": "Tüm bezler tek sıra halinde sıralanmış ve hiç lümen içermez", "isCorrect": False, "explanation": "Kistik genişlemeler vardır."},
            {"key": "D", "text": "Stroma hiç yoktur, sadece anaplastik dev tümör hücreleri vardır", "isCorrect": False, "explanation": "Benign bir proliferatif tablodur."}
        ])
    ]
    slides.append(make_slide(51, "Düzensiz Proliferatif Endometrium: Tanım ve Morfoloji", "Uniformitenin bozulması, dar ve kistik genişlemiş dallanmış bezler ve yoğun stroma", "Patoloji", s51_narrative, s51_bullets, s51_elements))

    # Slide 52: Anovulatuar Zemin ve Perimenopozal Kadınlar
    s52_narrative = (
        "Düzensiz proliferatif endometrium, over hormonlarındaki aksaklığa uterusun verdiği fizyolojik bir tepkidir.\n\n"
        "- **Anovulatuar Yanıt:** Düzensiz proliferasyonun, **endometriumun anovulatuar siklusa "
        "verdiği bir cevap** olduğu düşünülmektedir.\n"
        "- **Popülasyon Sıklığı:** Bu antite özellikle menopoz geçişindeki kadınlarda son derece yaygındır; "
        "**perimenapozal dönemdeki kadınların hemen hemen tümünde bulunmaktadır**.\n"
        "- **Etiyolojik Neden:** Tablo, progesteron ile dengelenmeyen **uzamış, karşılanmamış östrojen "
        "etkisine bağlı** olarak gelişir.\n"
        "- **Klinik Yansıma:** Perimenopozal kadında izlenen adet gecikmeleri ve ardından gelen yoğun "
        "kanamaların biyopsisinde en sık saptanan endometrial patern budur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Düzensiz proliferasyon endometriumun anovulatuar siklusa verdiği cevaptır; perimenapozal dönemdeki kadınların hemen hemen tümünde bulunur."
    )
    s52_bullets = [
        "Endometriumun anovulatuar siklusa verdiği cevap olarak kabul edilir.",
        "Perimenapozal dönemdeki kadınların hemen hemen tümünde bulunur.",
        "Uzamış, karşılanmamış (unopposed) östrojen etkisine bağlı gelişir."
    ]
    s52_elements = [
        make_cloze("Düzensiz proliferasyon, endometriumun anovulatuar siklusa verdiği cevap olup perimenapozal dönemdeki kadınların hemen hemen tümünde bulunmaktadır.", "perimenapozal dönemdeki", "Düzensiz proliferasyonun neredeyse tümünde görüldüğü yaş dönemi"),
        make_table("Düzensiz Proliferasyon Klinik Zemin", ["Özellik", "Klinik / Biyolojik Durum", "Açıklama"], [
            {"cells": [{"text": "Ovaryal Zemin", "isMasked": False}, {"text": "Anovulatuar siklus", "isMasked": True, "hint": "yumurtlamasız siklus"}, {"text": "Korpus luteum oluşamaz"}]},
            {"cells": [{"text": "Görüldüğü Yaş Grubu", "isMasked": False}, {"text": "Perimenapozal kadınların hemen tümü", "isMasked": False}, {"text": "Geçiş dönemi evrensel bulgusu", "isMasked": True, "hint": "neredeyse hepsinde bulunma"}]},
            {"cells": [{"text": "Hormonal Tetikleyici", "isMasked": False}, {"text": "Uzamış, karşılanmamış östrojen", "isMasked": False}, {"text": "Progesteron dengesinin yokluğu"}]}
        ]),
        make_chain("Perimenopozal Düzensizleşme Akışı", [
            "1. Perimenopozal Dönem: Over folikülleri azalır, anovulatuar döngüler başlar.",
            "2. Karşılanmamış Östrojen: Progesteron üretilemez, östrojenik etki uzar.",
            "3. Endometrial Cevap: Bezler uniformitesini kaybeder ve düzensiz prolifere olur.",
            "4. Evrensel Prevalans: Perimenopozal kadınların hemen hemen tamamında bu patern izlenir."
        ]),
        make_recall("Düzensiz proliferatif endometrium endometriumun hangi duruma verdiği cevaptır ve en sık hangi kadınlarda bulunur?", "Endometriumun anovulatuar siklusa verdiği cevaptır; perimenapozal dönemdeki kadınların hemen hemen tümünde bulunur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Düzensiz Proliferasyon Zemini", [
            {"text": "Düzensiz proliferasyon endometriumun anovulatuar siklusa verdiği cevaptır.", "isLie": False, "explanation": "Doğru. Patofizyolojik tanımdır."},
            {"text": "Perimenapozal dönemdeki kadınların hemen hemen tümünde bulunur.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Düzensiz proliferatif endometrium yalnızca 3 yaşındaki kız çocuklarında görülür, yetişkinlerde asla bulunmaz.", "isLie": True, "explanation": "Tuzak! Düzensiz proliferasyon anovulasyona bağlıdır ve perimenapozal kadınların neredeyse tamamında izlenir."},
            {"text": "Uzamış, karşılanmamış östrojen etkisine bağlı gelişir.", "isLie": False, "explanation": "Doğru. Hormonal temeldir."}
        ]),
        make_quiz("Düzensiz proliferatif endometriumun etiyolojik zemini ve en sık görüldüğü hasta grubu hangisidir?", [
            {"key": "A", "text": "Anovulatuar siklusa cevaptır; perimenapozal kadınların hemen hemen tümünde bulunur", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'düzensiz proliferasyonun, endometriumun anovulatuar siklusa verdiği cevap olduğu düşünülmektedir; perimenapozal dönemdeki kadınların hemen hemen tümünde bulunmaktadır' denmektedir."},
            {"key": "B", "text": "Gebelik hormonuna cevaptır; sadece 1. trimesterde görülür", "isCorrect": False, "explanation": "Gebelikte desidua olur."},
            {"key": "C", "text": "Aşırı progesteron cevabıdır; menopozdan 30 yıl sonra başlar", "isCorrect": False, "explanation": "Östrojen etkilidir."},
            {"key": "D", "text": "Genetik mutasyonla doğuştan gelen ölümcül bir anomalidir", "isCorrect": False, "explanation": "Fonksiyonel benign bir tablodur."}
        ])
    ]
    slides.append(make_slide(52, "Anovulatuar Zemin ve Perimenopozal Kadınlar", "Anovulatuar döngü yanıtı, perimenopozda evrensel sıklık ve uzamış karşılanmamış östrojen", "Patoloji", s52_narrative, s52_bullets, s52_elements))

    # Slide 53: Premalignite Durumu ve Basit Hiperplazi Ayrımı
    s53_narrative = (
        "Düzensiz proliferatif endometriumun klinik onkoloji ve patolojideki yeri net sınırlarla çizilmiştir.\n\n"
        "- **Premalignite Yokluğu:** Düzensiz proliferatif endometrium **gerçek bir premalign lezyon DEĞİLDİR**.\n"
        "- **Hormonal Risk:** Bununla birlikte anormal hormonal uyarının (karşılanmamış östrojen) "
        "yıllar boyu devam etmesi hâlinde, malignite gelişimi açısından hafif artmış bir risk söz konusudur.\n"
        "- **Basit Hiperplaziden Temel Fark:** Basit endometrial hiperplaziden en önemli farkı, "
        "**bez-stroma oranının nispeten normal korunmuş olmasıdır**.\n"
        "- **Glandüler Bozukluk Şiddeti:** Düzensiz proliferasyonda glandlardaki şekil bozuklukları "
        "basit hiperplaziye kıyasla çok daha hafiftir; stroma bezlerin arasına rahatça girer.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Düzensiz proliferatif endometrium gerçek premalign lezyon değildir; basit hiperplaziden en önemli farkı bez-stroma oranının nispeten normal olmasıdır."
    )
    s53_bullets = [
        "Gerçek bir premalign lezyon değildir; anormal uyarının sürmesi riski hafif artırabilir.",
        "Basit hiperplaziden farkı: bez-stroma oranının nispeten normal korunmuş olmasıdır.",
        "Glandlardaki şekil bozuklukları basit hiperplaziye kıyasla daha hafiftir."
    ]
    s53_elements = [
        make_cloze("Düzensiz proliferatif endometrium gerçek premalign lezyon değildir ve basit hiperplaziden bez-stroma oranının nispeten normal olmasıyla farklıdır.", "gerçek premalign lezyon değildir", "Düzensiz proliferasyonun onkolojik niteliği"),
        make_table("Düzensiz Proliferasyon vs Basit Hiperplazi", ["Kriter", "Düzensiz Proliferatif Endometrium", "Basit Hiperplazi"], [
            {"cells": [{"text": "Premalignite Durumu", "isMasked": False}, {"text": "Gerçek premalign lezyon değildir", "isMasked": True, "hint": "kanser öncülü olmama"}, {"text": "Preneoplastik potansiyel taşır"}]},
            {"cells": [{"text": "Bez/Stroma Oranı", "isMasked": False}, {"text": "Nispeten normal korunmuştur", "isMasked": False}, {"text": "Belirgin şekilde artmıştır (bez fazlalığı)", "isMasked": True, "hint": "stromanın azalması"}]},
            {"cells": [{"text": "Şekil Bozukluğu", "isMasked": False}, {"text": "Daha hafif ve dağınık", "isMasked": False}, {"text": "Daha yaygın ve belirgin kistik dilate"}]}
        ]),
        make_chain("Tanısal Ayrım Aşamaları", [
            "1. Biyopsi İncelemesi: Kistik ve dallanmış bezler tespit edilir.",
            "2. Bez-Stroma Oranı Değerlendirmesi: Stroma hacminin bezlere oranı incelenir.",
            "3. Oranın Korunduğunun Saptanması: Bez-stroma oranının normal olduğu görülür.",
            "4. Karar: Hiperplazi dışlanarak benign 'Düzensiz Proliferatif Endometrium' tanısı verilir."
        ]),
        make_recall("Düzensiz proliferatif endometrium premalign bir lezyon mudur ve basit hiperplaziden nasıl ayrılır?", "Gerçek bir premalign lezyon değildir; basit hiperplaziden bez-stroma oranının nispeten normal korunmuş olmasıyla ayrılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Premalignite ve Hiperplazi Ayrımı", [
            {"text": "Düzensiz proliferatif endometrium gerçek premalign lezyon değildir.", "isLie": False, "explanation": "Doğru. Ders notunun kritik vurgusudur."},
            {"text": "Basit hiperplaziden bez-stroma oranının nispeten normal olmasıyla farklıdır.", "isLie": False, "explanation": "Doğru. Tanısal ayrımdır."},
            {"text": "Düzensiz proliferatif endometrium en ölümcül premalign lezyondur ve hastaların %100'ünde 1 haftada karsinom gelişir.", "isLie": True, "explanation": "Tuzak! Gerçek premalign lezyon değildir; karsinom riski doğrudan taşımaz."},
            {"text": "Glandlardaki şekil bozuklukları basit hiperplaziden daha hafiftir.", "isLie": False, "explanation": "Doğru. Karşılaştırma kriteridir."}
        ]),
        make_quiz("Düzensiz proliferatif endometriumun premalign potansiyeli ve basit hiperplaziden temel farkı hangisidir?", [
            {"key": "A", "text": "Gerçek premalign lezyon değildir; basit hiperplaziden bez-stroma oranının nispeten normal olmasıyla ayrılır", "isCorrect": True, "explanation": "Ders notunda açıkça: 'gerçek premalign lezyon değildir; basit hiperplaziden bez-stroma oranının nispeten normal olmasıyla farklıdır' denmektedir."},
            {"key": "B", "text": "İleri evre premalign kanserdir ve stroma tamamen yok olmuştur", "isCorrect": False, "explanation": "Premalign değildir."},
            {"key": "C", "text": "Basit hiperplazi ile hiçbir farkı yoktur, tamamen aynı hastalıktır", "isCorrect": False, "explanation": "Bez-stroma oranı farklıdır."},
            {"key": "D", "text": "Yalnızca serviks kanserinin öncüsüdür", "isCorrect": False, "explanation": "Endometrium lezyonudur."}
        ])
    ]
    slides.append(make_slide(53, "Premalignite Durumu ve Basit Hiperplazi Ayrımı", "Gerçek premalign olmama durumu, bez-stroma oranının korunması ve hafif şekil bozukluğu", "Patoloji", s53_narrative, s53_bullets, s53_elements))

    # Slide 54: Gözlemciler Arası Uyum Düşüklüğü ve Kistik Atrofi Ayrımı
    s54_narrative = (
        "Düzensiz proliferatif endometrium tanısında patologlar arasında subjektif yorum farklılıkları sıkça yaşanır.\n\n"
        "- **Sınır Belirsizliği:** Hem düzensiz proliferatif endometrium hem de basit hiperplazi karşılanmamış "
        "östrojen etkisiyle geliştiğinden ve morfolojik bulguları arasında keskin bir sınır bulunmadığından "
        "**gözlemciler arası uyum düşüktür (inter-observer variability)**.\n"
        "- **Kistik Atrofi Ayrımı:** Düzensiz proliferasyon aynı zamanda **endometrial polip ve kistik "
        "atrofi** ile de dikkatle ayırt edilmelidir.\n"
        "- **Kistik Atrofinin Morfolojisi:** Kistik atrofide gland epiteli basık, incelmiş, **atrofik "
        "görünümdedir ve hücrelerde hiçbir proliferatif aktivite (mitoz) yoktur**.\n"
        "- **Proliferatif Fark:** Düzensiz proliferasyonda ise epitel yüksek prizmatiktir, psödostratifiye "
        "nükleuslar ve belirgin mitotik figürler mevcuttur.\n\n"
        "> [!NOTE]\n"
        "> Keskin sınır olmadığı için gözlemciler arası uyum düşüktür; kistik atrofide epitel basık/atrofiktir ve proliferatif aktivite yoktur."
    )
    s54_bullets = [
        "Basit hiperplazi ile arasında keskin sınır olmadığı için gözlemciler arası uyum düşüktür.",
        "Kistik atrofi ve endometrial polip ile de ayırıcı tanı yapılmalıdır.",
        "Kistik atrofide gland epiteli basık ve atrofiktir; proliferatif aktivite (mitoz) yoktur."
    ]
    s54_elements = [
        make_cloze("Morfolojik bulguları arasında keskin bir sınır olmadığı için patologlar arasında gözlemciler arası uyum düşüktür.", "gözlemciler arası uyum düşüktür", "Patolojik tanıda yaşanan uyumsuzluk"),
        make_table("Düzensiz Proliferasyon vs Kistik Atrofi", ["Özellik", "Düzensiz Proliferatif Endometrium", "Kistik Atrofi"], [
            {"cells": [{"text": "Epitel Hücre Morfolojisi", "isMasked": False}, {"text": "Yüksek prizmatik, proliferatif", "isMasked": True, "hint": "aktif epitel yapısı"}, {"text": "Basık, yassılaşmış, atrofik görünüm"}]},
            {"cells": [{"text": "Mitotik Aktivite", "isMasked": False}, {"text": "Mitoz mevcuttur", "isMasked": False}, {"text": "Proliferatif aktivite ve mitoz yoktur", "isMasked": True, "hint": "hücre bölünmesinin olmaması"}]},
            {"cells": [{"text": "Hormonal Etki", "isMasked": False}, {"text": "Karşılanmamış östrojen uyarımı", "isMasked": False}, {"text": "Östrojen yokluğu (senil zemin)"}]}
        ]),
        make_chain("Kistik Atrofi Ayırıcı Tanı Zinciri", [
            "1. Kistik Bezlerin Görülmesi: Lümeni genişlemiş kistik glandlar izlenir.",
            "2. Epitel İncelemesi: Bezleri döşeyen hücre tabakasının boyu değerlendirilir.",
            "3. Basıklık ve Mitoz Yokluğu: Epitelin basık olduğu ve mitoz içermediği saptanır.",
            "4. Ayırım: Aktif proliferatif epitel olmadığı için kistik atrofi tanısı netleşir."
        ]),
        make_recall("Düzensiz proliferatif endometrium ile kistik atrofi arasındaki temel mikroskopik fark nedir?", "Kistik atrofide gland epiteli basık, atrofik görünümdedir ve proliferatif aktivite (mitoz) yoktur; düzensiz proliferasyonda epitel proliferatiftir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Gözlemciler Arası Uyum ve Kistik Atrofi", [
            {"text": "Düzensiz proliferasyon ile basit hiperplazi arasında gözlemciler arası uyum düşüktür.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Kistik atrofide gland epiteli basık ve atrofik görünümdedir.", "isLie": False, "explanation": "Doğru. Epitel yapısıdır."},
            {"text": "Kistik atrofide nükleer mitozlar çılgınca artar ve epitel 10 kat kalınlaşır.", "isLie": True, "explanation": "Tuzak! Kistik atrofide proliferatif aktivite ve mitoz YOKTUR; epitel basıktır."},
            {"text": "Endometrial polip de ayırıcı tanıda yer alır.", "isLie": False, "explanation": "Doğru. Ayırıcı tanıdır."}
        ]),
        make_quiz("Düzensiz proliferatif endometrium ile kistik atrofi ayırıcı tanısında kistik atrofiyi destekleyen özellik hangisidir?", [
            {"key": "A", "text": "Gland epitelinin basık ve atrofik olması, proliferatif aktivitenin olmaması", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'kistik atrofide gland epiteli basık, atrofik görünümdedir ve proliferatif aktivite yoktur' denmektedir."},
            {"key": "B", "text": "Gland epitelinde aşırı mitoz ve invaziv tümör yuvaları olması", "isCorrect": False, "explanation": "Karsinom bulgusudur."},
            {"key": "C", "text": "Kemik iliğinde granülositlerin aşırı çoğalması", "isCorrect": False, "explanation": "Endometrium ile ilgisizdir."},
            {"key": "D", "text": "Lümende sadece canlı trofoblastların bulunması", "isCorrect": False, "explanation": "Gebelik bulgusudur."}
        ])
    ]
    slides.append(make_slide(54, "Gözlemciler Arası Uyum Düşüklüğü ve Kistik Atrofi Ayrımı", "Subjektif tanı zorluğu, düşük gözlemci uyumu ve basık/mitozsuz epitele sahip kistik atrofi ayrımı", "Patoloji", s54_narrative, s54_bullets, s54_elements))

    # Slide 55: Endometrial Polip: Tanım ve Bazalis Hiperplazisi
    s55_narrative = (
        "Endometrial polipler, kavite içine uzanan ve en sık karşılaşılan benign intrauterin kitlelerdir.\n\n"
        "- **Patolojik Köken:** Endometrial polip, **endometrium bazalisin lokalize hiperplazisi** "
        "ile oluşan, kavite içerisine doğru protrude olan ekzofitik lezyonlardır.\n"
        "- **Biyolojik Doğası:** Kesinlikle **benign** (iyi huylu) lezyonlardır; karsinomatöz transformasyon "
        "nadir olsa da semptomatik kanamalara yol açarlar.\n"
        "- **Morfolojik Çeşitlilik:** Boyutları birkaç milimetreden santimetrelere kadar değişken, "
        "tek ya da çok sayıda, ince saplı (pediküllü) ya da geniş tabanlı (sapsız/sesil) olabilir.\n"
        "- **Siklus Duyarsızlığı:** Bazalis kökenli oldukları için, çevre fonksiyonel tabaka menstruasyonla "
        "dökülürken polip dökülmeyip kavite içinde büyümeye devam eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometrial polip, endometrium bazalisin lokalize hiperplazisi ile oluşan, kavite içerisine protrude olan BENİGN lezyonlardır."
    )
    s55_bullets = [
        "Endometrium bazalisin lokalize hiperplazisi ile oluşur.",
        "Kavite içerisine protrude olan benign (iyi huylu) lezyonlardır.",
        "Boyutları değişken, tek ya da çok sayıda, saplı ya da sapsız olabilir."
    ]
    s55_elements = [
        make_cloze("Endometrial polip, endometrium bazalisin lokalize hiperplazisi ile oluşan kavite içerisine protrude olan benign lezyonlardır.", "endometrium bazalisin", "Polibin köken aldığı endometrial tabaka"),
        make_table("Endometrial Polibin Temel Nitelikleri", ["Özellik", "Nitelik", "Klinik Yansıması"], [
            {"cells": [{"text": "Köken Tabaka", "isMasked": False}, {"text": "Endometrium bazalis (derin tabaka)", "isMasked": True, "hint": "bazal katman kökeni"}, {"text": "Menstruasyonda dökülmez"}]},
            {"cells": [{"text": "Biyolojik Doğası", "isMasked": False}, {"text": "Benign (iyi huylu)", "isMasked": False}, {"text": "Malign potansiyel çok düşüktür", "isMasked": True, "hint": "kanser olmama durumu"}]},
            {"cells": [{"text": "Makroskopi", "isMasked": False}, {"text": "Kaviteye uzanan saplı/sapsız lezyon", "isMasked": False}, {"text": "Histeroskopide kolayca izlenir"}]}
        ]),
        make_chain("Endometrial Polip Oluşum Zinciri", [
            "1. Bazal Odak: Bazalis tabakasındaki gland ve stroma hücreleri otonom uyarılır.",
            "2. Lokalize Hiperplazi: Tek bir odakta bazal bezler ve damarlar aşırı çoğalır.",
            "3. Ekzofitik Büyüme: Kitle uterus kavitesi lümenine doğru sarkar.",
            "4. Polip Formasyonu: Üç tarafı epitel kaplı saplı veya sapsız polip şekillenir."
        ]),
        make_recall("Endometrial polip hangi tabakanın lokalize hiperplazisi ile oluşan nasıl bir lezyondur?", "Endometrium bazalisin lokalize hiperplazisi ile oluşan benign (iyi huylu) bir lezyondur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrial Polip Tanımı", [
            {"text": "Endometrial polip endometrium bazalisin lokalize hiperplazisi ile oluşur.", "isLie": False, "explanation": "Doğru. Köken tabakasıdır."},
            {"text": "Kavite içerisine protrude olan benign lezyonlardır.", "isLie": False, "explanation": "Doğru. Tanımıdır."},
            {"text": "Endometrial polip yüksek dereceli agresif bir kemik iliği sarkomudur.", "isLie": True, "explanation": "Tuzak! Endometrial polip endometrium bazalis kökenli BENİGN bir lezyondur."},
            {"text": "Boyutları değişken, tek ya da çok sayıda, saplı ya da sapsız olabilir.", "isLie": False, "explanation": "Doğru. Morfolojik değişkenliktir."}
        ]),
        make_quiz("Endometrial polibin dokusal kökeni ve biyolojik niteliği aşağıdakilerden hangisinde doğru tanımlanmıştır?", [
            {"key": "A", "text": "Endometrium bazalisin lokalize hiperplazisi ile oluşan benign lezyonlardır", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'endometrium bazalisin lokalize hiperplazisi ile oluşan, kavite içerisine protrude olan benign lezyonlardır' denmektedir."},
            {"key": "B", "text": "Myometrium kas tabakasının malign kanseridir", "isCorrect": False, "explanation": "Bu leiomyosarkomdur."},
            {"key": "C", "text": "Periton mezotelyumunun doğuştan yokluğudur", "isCorrect": False, "explanation": "İlgisizdir."},
            {"key": "D", "text": "Sadece plasental trofoblastlardan kaynaklanan bir koryokarsinomdur", "isCorrect": False, "explanation": "Trofoblastik tümör değildir."}
        ])
    ]
    slides.append(make_slide(55, "Endometrial Polip: Tanım ve Bazalis Hiperplazisi", "Endometrium bazalis kökeni, kaviter protrüzyon, benign karakter ve morfolojik varyasyonlar", "Patoloji", s55_narrative, s55_bullets, s55_elements))

    # Slide 56: Yaş Dağılımı ve Klinik Semptomlar
    s56_narrative = (
        "Endometrial polipler kadın üreme sisteminde sık rastlanan ve her yaşta ortaya çıkabilen lezyonlardır.\n\n"
        "- **Yaş Dağılımı:** Her yaşta görülebilmekle birlikte, **özellikle 4-5. dekatta (40-50'li yaşlar) "
        "en sık** izlenir.\n"
        "- **Klinik Tablo:** Hastalarda en sık başvuru semptomu **anormal uterin kanama**dır (menoraji, "
        "metroraji veya postmenopozal kanama); ancak hastaların önemli bir kısmı **tamamen asemptomatik** olabilir.\n"
        "- **Biyopsi Zorluğu:** Biyopsi ve küretaj örnekleri sıklıkla küçük ve fragmante olduğu için "
        "patolog açısından **tanı güçlüğü** yaratabilir.\n"
        "- **Rastlantısal Saptama:** İnfertilite araştırmalarında veya rutin pelvik ultrasonografide tesadüfen saptanabilir.\n\n"
        "> [!NOTE]\n"
        "> Her yaşta görülebilir, 4-5. dekatta sıktır; anormal kanama yapabilir ya da asemptomatik olabilir; fragmante küretajlarda tanı güçlüğü olabilir."
    )
    s56_bullets = [
        "Her yaşta görülebilir, en sık 4-5. dekatta (40-50 yaş) ortaya çıkar.",
        "Anormal uterin kanama yapabilir ya da tamamen asemptomatik seyredebilir.",
        "Küretaj materyalleri fragmante olduğu için tanıda güçlük yaşanabilir."
    ]
    s56_elements = [
        make_cloze("Endometrial polipler her yaşta görülebilir ancak en sık 4-5. dekatta izlenir.", "4-5. dekatta", "Polibin en sık görüldüğü yaşam dekatı"),
        make_table("Endometrial Polip Klinik Özellikleri", ["Parametre", "Klinik Dağılım", "Tanısal Durum"], [
            {"cells": [{"text": "Pik Yaş Dönemi", "isMasked": False}, {"text": "4-5. dekat (40-50 yaşlar)", "isMasked": True, "hint": "kırklı ellili yaşlar"}, {"text": "Perimenopoz öncesi sıklık"}]},
            {"cells": [{"text": "Semptom Profili", "isMasked": False}, {"text": "Anormal kanama veya asemptomatik", "isMasked": False}, {"text": "Gizli veya kanamalı seyir", "isMasked": True, "hint": "belirti verme veya vermeme"}]},
            {"cells": [{"text": "Biyopsi Özelliği", "isMasked": False}, {"text": "Küçük ve fragmante dokular", "isMasked": False}, {"text": "Tanı güçlüğü yaratabilir"}]}
        ]),
        make_chain("Polip Klinik Tanı Süreci", [
            "1. Başvuru: 45 yaşında hasta ara kanama veya menoraji ile başvurur.",
            "2. Ultrason: Endometrial kavitede polipoid kalınlaşma görülür.",
            "3. Küretaj / Histeroskopi: Doku parçalanarak patolojiye gönderilir.",
            "4. Mikroskobik Tanı: Fragmanlar arasından polip histolojik kriterleri ayıklanır."
        ]),
        make_recall("Endometrial polipler en sık hangi yaşam dekatında görülür ve klinik prezentasyonu nasıldır?", "En sık 4-5. dekatta görülür; anormal kanama yapabilir veya asemptomatik olabilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Polip Yaş ve Klinik", [
            {"text": "Endometrial polipler her yaşta görülebilir, 4-5. dekatta sıktır.", "isLie": False, "explanation": "Doğru. Yaş dağılımıdır."},
            {"text": "Anormal kanama yapabilir ya da asemptomatik olabilir.", "isLie": False, "explanation": "Doğru. Klinik spektrumdur."},
            {"text": "Endometrial polipler sadece 100 yaşın üzerindeki kadınlarda görülür, gençlerde asla rastlanmaz.", "isLie": True, "explanation": "Tuzak! Her yaşta görülebilir ve en sık 4-5. dekatta (40-50 yaş) saptanır."},
            {"text": "Biyopsi ve küretajlar küçük ve fragmante olduğu için tanı güçlüğü olabilir.", "isLie": False, "explanation": "Doğru. Patoloji pratiği gerçeğidir."}
        ]),
        make_quiz("Endometrial polipin en sık görüldüğü yaş grubu ve klinik seyri ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Her yaşta görülebilir, 4-5. dekatta sıktır; anormal kanama yapabilir ya da asemptomatiktir", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'her yaşta görülebilir, 4-5. dekatta sıktır; anormal kanama yapabilir ya da asemptomatik olabilir' denmektedir."},
            {"key": "B", "text": "Sadece 1. dekatta görülür ve her zaman ölümcül komaya sokar", "isCorrect": False, "explanation": "Çocuklukta nadirdir, benign lezyondur."},
            {"key": "C", "text": "Yalnızca erkek testislerinde izlenir", "isCorrect": False, "explanation": "Uterin patolojidir."},
            {"key": "D", "text": "Asla kanama yapmaz, her zaman sadece nefes darlığı oluşturur", "isCorrect": False, "explanation": "Anormal uterin kanama yapar."}
        ])
    ]
    slides.append(make_slide(56, "Yaş Dağılımı ve Klinik Semptomlar", "4-5. dekat sıklığı, anormal kanama, asemptomatik olgular ve fragmante küretaj güçlüğü", "Klinik", s56_narrative, s56_bullets, s56_elements))

    # Slide 57: Etiyoloji ve Tamoksifen İlişkisi
    s57_narrative = (
        "Endometrial polip gelişiminde hormonal uyarılar ve farmakolojik ajanlar belirleyici rol oynar.\n\n"
        "- **Hormonal Faktörler:** Östrojen fazlalığı veya kombine hormonal dengesizlikler polip oluşumunu tetikleyebilir.\n"
        "- **Klinik Birliktelikler:** İnfertilite ve endometriozis olgularında endometrial polip insidansı belirgin olarak artmıştır.\n"
        "- **Tamoksifen İlişkisi:** Meme kanseri tedavisinde kullanılan bir selektif östrojen reseptör modülatörü "
        "(SERM) olan **tamoksifen kullanımı, endometrial polip gelişimi ile çok güçlü bir ilişkiye sahiptir**.\n"
        "- **Tamoksifen Polipleri:** Tamoksifen alan kadınlarda gelişen polipler klasik poliplere göre "
        "**daha büyük, çok sayıda (multipl)** olma eğilimindedir ve stromal atipi içerebilir.\n"
        "- **Paradoksal Etki:** Tamoksifen memede anti-östrojenik etki gösterirken, postmenopozal "
        "uterus endometriumunda kısmi pro-östrojenik (agonist) etki göstererek polip büyümesini tetikler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Tamoksifen kullanımı endometrial polip gelişimi ile ilişkilidir; bu olgularda büyük ve çok sayıda (multipl) polipler izlenir."
    )
    s57_bullets = [
        "Hormonal faktörler (östrojen), infertilite ve endometriozis ile ilişkilidir.",
        "Tamoksifen kullanımı büyük ve çok sayıda polip gelişimiyle belirgin ilişkilidir.",
        "Tamoksifenin endometriumdaki parsiyel agonist östrojenik etkisi polipleri uyarır."
    ]
    s57_elements = [
        make_cloze("Hormonal faktörler ve tamoksifen kullanımı büyük ve çok sayıda endometrial polip gelişimi ile ilişkilidir.", "tamoksifen kullanımı", "Büyük ve multipl poliplerle ilişkili ilaç"),
        make_table("Polip Etyolojisi ve Tamoksifen", ["Faktör / İlaç", "Mekanizma", "Polip Morfolojisi"], [
            {"cells": [{"text": "Tamoksifen Tedavisi", "isMasked": False}, {"text": "Endometriumda parsiyel östrojenik agonizm", "isMasked": True, "hint": "SERM östrojen benzeri etkisi"}, {"text": "Büyük, multipl ve sık polipler"}]},
            {"cells": [{"text": "Hormonal Faktörler", "isMasked": False}, {"text": "Östrojenik stimülasyon", "isMasked": False}, {"text": "Lokalize bazalis hiperplazisi", "isMasked": True, "hint": "tekil veya çoklu hiperplazi"}]},
            {"cells": [{"text": "İnfertilite / Endometriozis", "isMasked": False}, {"text": "İnflamatuar ve endokrin zemin", "isMasked": False}, {"text": "Artmış polip sıklığı"}]}
        ]),
        make_chain("Tamoksifen ve Polip Gelişimi", [
            "1. Meme Kanseri Tedavisi: Hastaya oral tamoksifen başlanır.",
            "2. Uterin Agonizm: Tamoksifen endometrium östrojen reseptörlerini uyarır.",
            "3. Bazal Çoğalma: Bazalis tabakasında abartılı glandüler büyüme tetiklenir.",
            "4. Multipl Polip: Uterus kavitesinde çok sayıda ve büyük polipler gelişir."
        ]),
        make_recall("Hangi onkolojik ilacın kullanımı uterus kavitesinde büyük ve çok sayıda endometrial polip gelişimi ile ilişkilidir?", "Tamoksifen kullanımıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tamoksifen ve Polip", [
            {"text": "Tamoksifen kullanımı büyük ve çok sayıda polip gelişimi ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Klasik klinik tablodur."},
            {"text": "İnfertilite ve endometriozis ile polip birlikteliği olabilir.", "isLie": False, "explanation": "Doğru. Eşlik eden durumlardır."},
            {"text": "Tamoksifen alan hastalarda uterus derhal taşlaşır ve polip gelişimi tamamen imkansız hale gelir.", "isLie": True, "explanation": "Tuzak! Tamoksifen endometrial polip gelişimini tetikleyen en bilinen farmakolojik ajandır."},
            {"text": "Hormonal faktörler (östrojen veya kombine) polip gelişiminde rol oynar.", "isLie": False, "explanation": "Doğru. Etyolojik faktördür."}
        ]),
        make_quiz("Meme kanseri tedavisinde kullanılan ve endometrial kavitede büyük, çok sayıda polip gelişimiyle ilişkili olan ilaç hangisidir?", [
            {"key": "A", "text": "Tamoksifen", "isCorrect": True, "explanation": "Ders notunda açıkça: 'tamoksifen kullanımı (büyük ve çok sayıda polip), infertilite ve endometriozis ile ilişki olabilir' denmektedir."},
            {"key": "B", "text": "Parasetamol", "isCorrect": False, "explanation": "Basit analjeziktir."},
            {"key": "C", "text": "Penisilin", "isCorrect": False, "explanation": "Antibiyotiktir."},
            {"key": "D", "text": "İnsülin", "isCorrect": False, "explanation": "Diyabet ilacıdır."}
        ])
    ]
    slides.append(make_slide(57, "Etiyoloji ve Tamoksifen İlişkisi", "Östrojenik uyarım, infertilite birlikteliği, tamoksifen kullanımı ve multipl büyük polipler", "Klinik Patoloji", s57_narrative, s57_bullets, s57_elements))

    # Slide 58: Polip Histopatolojisi: Üç Kenarı Yüzey Epiteli
    s58_narrative = (
        "Endometrial polibin patolojik tanısı, fragmante biyopsi materyallerinde belirli kardinal mimari kriterlere dayanır.\n\n"
        "- **Çevre Endometriumdan Fark:** Polip dokusu, komşu çevre normal fonksiyonel endometriumdan "
        "farklı bir histolojik görünüm sergiler.\n"
        "- **Kardinal Kriter: Üç Kenarı Epitel:** Biyopsi kesitlerinde doku parçasının **3 kenarının "
        "yüzey epiteli ile çevrili olması**, biyopsinin bir polip apeksinden veya gövdesinden geçtiğinin patognomonik kanıtıdır.\n"
        "- **Büyük Fragmanlar:** Küretajda çevre fonksiyonel endometrium küçük döküntüler halindeyken, "
        "polip dokusu **büyük doku fragmanları** şeklinde ele gelir.\n"
        "- **Polipoid Şekil:** Kesitlerde düzensiz ve yuvarlak hatlı polipoid mimari net olarak izlenir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometrial polip tanısında mikroskopik olarak dokunun 3 kenarının yüzey epiteli ile çevrili olması kardinal tanı kriteridir."
    )
    s58_bullets = [
        "Çevre normal endometriumdan farklı görünüm ve büyük doku fragmanları izlenir.",
        "Dokunun 3 kenarının yüzey epiteli ile çevrili olması tanısal kriterdir.",
        "Polipoid şekilli büyük doku parçaları şeklinde kürete edilir."
    ]
    s58_elements = [
        make_cloze("Endometrial polip kesitlerinde dokunun 3 kenarı yüzey epiteli ile çevrili olup çevre normal endometriumdan farklıdır.", "3 kenarı yüzey epiteli", "Polibin biyopsideki kardinal epitel sınırı"),
        make_table("Polip Histopatolojik Mimari Kriterleri", ["Ölçüt", "Gözlenen Morfoloji", "Tanısal Değeri"], [
            {"cells": [{"text": "Yüzey Epiteli Örtüsü", "isMasked": False}, {"text": "Dokunun 3 kenarı yüzey epiteli ile çevrili", "isMasked": True, "hint": "üç tarafı epitel kaplı"}, {"text": "Kaviter polipoid çıkıntı kanıtı"}]},
            {"cells": [{"text": "Fragman Boyutu", "isMasked": False}, {"text": "Büyük doku fragmanları", "isMasked": False}, {"text": "Fragmente normal dokudan ayrım", "isMasked": True, "hint": "iri biyopsi parçası"}]},
            {"cells": [{"text": "Çevreyle Uyum", "isMasked": False}, {"text": "Çevre normal endometriumdan farklı", "isMasked": False}, {"text": "Otonom bazal lezyon"}]}
        ]),
        make_chain("Polip Tanısal Mikroskopi Zinciri", [
            "1. Fragman Taraması: Küretaj kesitinde iri bir doku parçası bulunur.",
            "2. Epitel Sınırının Takibi: Parçanın üç kenarı boyunca yüzey epiteli izlenir.",
            "3. 3 Kenar Kuralı: Üç tarafın epitel kaplı olduğu doğrulanır.",
            "4. Polip Onayı: Doku parçasının kaviteye uzanan bir polip olduğu tescillenir."
        ]),
        make_recall("Endometrial küretaj materyalinde dokunun kaç kenarının yüzey epiteli ile çevrili olması polip tanısını destekler?", "Dokunun 3 kenarının yüzey epiteli ile çevrili olması polip tanısı için kardinal bulgudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Polip Epitel Sınırları", [
            {"text": "Polip dokusu çevre normal endometriumdan farklı görünüm sergiler.", "isLie": False, "explanation": "Doğru. Siklus uyumsuzluğu vardır."},
            {"text": "Dokunun 3 kenarı yüzey epiteli ile çevrilidir.", "isLie": False, "explanation": "Doğru. Klasik patoloji kriteridir."},
            {"text": "Polip kesitlerinin hiçbir kenarında asla epitel bulunmaz, tüm kenarlar saf myometrium kasıdır.", "isLie": True, "explanation": "Tuzak! Polip kaviteye sarkan bir mukoza lezyonudur; dokunun 3 kenarı yüzey epiteli ile çevrilidir."},
            {"text": "Büyük doku fragmanları ve polipoid şekil karakteristiktir.", "isLie": False, "explanation": "Doğru. Makroskobik ve histolojik uyumdur."}
        ]),
        make_quiz("Endometrial küretaj materyalinde bir parçanın endometrial polip olduğunu gösteren karakteristik mikroskopik bulgu hangisidir?", [
            {"key": "A", "text": "Dokunun 3 kenarının yüzey epiteli ile çevrili olması ve çevre endometriumdan farklı görünmesi", "isCorrect": True, "explanation": "Ders notunda histolojik özellikler arasında: 'çevre normal endometriumdan farklı görünüm; büyük doku fragmanları; dokunun 3 kenarı yüzey epiteli ile çevrili' açıkça sayılmıştır."},
            {"key": "B", "text": "Dokunun 8 köşeli yıldız şeklinde olması ve içinde saf cıva bulunması", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."},
            {"key": "C", "text": "Tüm hücrelerin tek tek çekirdeksiz eritrosite dönüşmüş olması", "isCorrect": False, "explanation": "Bu kan pıhtısıdır."},
            {"key": "D", "text": "Yalnızca kemik iliği megakaryositlerinin birikmesi", "isCorrect": False, "explanation": "Hematolojik dokudur."}
        ])
    ]
    slides.append(make_slide(58, "Polip Histopatolojisi: Üç Kenarı Yüzey Epiteli", "Büyük fragmanlar, çevre endometriumdan farklılaşma ve 3 kenarı yüzey epiteli kuralı", "Histopatoloji", s58_narrative, s58_bullets, s58_elements))

    # Slide 59: Polipte Kalın Duvarlı Damarlar ve Fibröz Stroma
    s59_narrative = (
        "Endometrial polibin internal mimarisi, onu normal proliferatif veya hiperplastik endometriumdan ayıran özgül stroma ve vasküler yapılara sahiptir.\n\n"
        "- **Vasküler Özellik: Kalın Duvarlı Damarlar:** Polip stromasında, normal fonksiyonel endometriumda "
        "asla bulunmayan **kalın duvarlı kan damarları ya da ince duvarlı ektatik damar yumakları** izlenir.\n"
        "- **Köken Kanıtı:** Bu kalın kas tabakalı damarlar, lezyonun bazalis tabakasından kaynaklandığının "
        "en somut histopatolojik kanıtıdır.\n"
        "- **Stromal Yapı:** Polip stroması sıklıkla **fibröz stroma** karakterindedir (bazen atipik "
        "bizarre hücreler içerebilir), bazen dens ve sellüler de olabilir.\n"
        "- **Glandüler Mimari:** İçerisindeki bezler **düzensiz, kıvrıntılı ve dilate glandlar** "
        "şeklindedir; normal siklus faz bulguları göstermezler, hiperplastik veya kistik atrofik yapıda olabilirler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometrial polip stromasında kalın duvarlı damarlar, fibröz stroma ve düzensiz dilate bezler izlenir; normal siklus bulguları göstermez."
    )
    s59_bullets = [
        "Sıklıkla fibröz stroma (bazen atipik), dens ve sellüler stroma izlenir.",
        "Karakteristik özellik: kalın duvarlı damarlar ya da ince duvarlı ektatik damarlar bulunur.",
        "Düzensiz, kıvrıntılı, dilate glandlar içerir; normal siklus bulguları göstermez."
    ]
    s59_elements = [
        make_cloze("Endometrial polip stromasında kalın duvarlı damarlar ya da ince duvarlı ektatik damarlar ve fibröz stroma bulunur.", "kalın duvarlı damarlar", "Polibin ayırıcı vasküler yapısı"),
        make_table("Polip İnternal Histolojik Bileşenleri", ["Bileşen", "Histolojik Nitelik", "Klinik / Tanısal Anlamı"], [
            {"cells": [{"text": "Kan Damarları", "isMasked": False}, {"text": "Kalın duvarlı damarlar veya ektatik damar yumakları", "isMasked": True, "hint": "kas tabakalı kalın damarlar"}, {"text": "Bazalis kökeninin patognomonik kanıtı"}]},
            {"cells": [{"text": "Stroma", "isMasked": False}, {"text": "Fibröz stroma (bazen atipik/sellüler)", "isMasked": False}, {"text": "Sert bağ dokusu desteği", "isMasked": True, "hint": "kollajenize stroma"}]},
            {"cells": [{"text": "Glandlar", "isMasked": False}, {"text": "Düzensiz, kıvrıntılı, dilate bezler", "isMasked": False}, {"text": "Siklik faz uyumsuzluğu"}]}
        ]),
        make_chain("Polip Histolojik Teşhis Zinciri", [
            "1. Vasküler Arama: Stromada kalın kas tabakalı sklerotik damarlar aranır.",
            "2. Stroma Değerlendirmesi: Normal stroma yerine fibröz/yoğun bağ dokusu saptanır.",
            "3. Bezlerin İncelenmesi: Düzensiz ve kistik dilate bezler izlenir.",
            "4. Siklus Uyumsuzluğu: Bezlerin siklus gününe uymadığı görülerek polip kesinleşir."
        ]),
        make_recall("Endometrial polip stromasında izlenen ve bazalis kökenini kanıtlayan karakteristik damar yapısı nedir?", "Kalın duvarlı damarlar ya da ince duvarlı ektatik damarlardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Polip Vasküler ve Stromal Yapısı", [
            {"text": "Polip stromasında kalın duvarlı damarlar ya da ektatik damarlar bulunur.", "isLie": False, "explanation": "Doğru. Kardinal tanı kriteridir."},
            {"text": "Polipte sıklıkla fibröz stroma izlenir.", "isLie": False, "explanation": "Doğru. Tipik stromadır."},
            {"text": "Polipteki tüm bezler ve damarlar her ay kesinlikle siklus gününü mükemmel yansıtır.", "isLie": True, "explanation": "Tuzak! Polipte normal siklus bulguları yoktur; bezler siklusa uyumsuz, hiperplastik veya atrofiktir."},
            {"text": "Düzensiz, kıvrıntılı, dilate glandlar içerir.", "isLie": False, "explanation": "Doğru. Gland morfolojisidir."}
        ]),
        make_quiz("Endometrial polip mikroskopisinde izlenen stromal ve vasküler özellikler aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Fibröz stroma, kalın duvarlı damarlar ve düzensiz kıvrıntılı dilate glandlar", "isCorrect": True, "explanation": "Ders notunda polip histolojisi tam olarak: 'sıklıkla fibröz stroma; kalın duvarlı damarlar ya da ince duvarlı ektatik damarlar; düzensiz kıvrıntılı dilate glandlar; normal siklus bulguları yok' şeklinde özetlenmiştir."},
            {"key": "B", "text": "Tamamen avasküler kıkırdak zarı ve tek katlı siliyer hücreler", "isCorrect": False, "explanation": "Kıkırdak dokusu değildir."},
            {"key": "C", "text": "Yalnızca kapiller hemanjiom ve normal sekretuar bezler", "isCorrect": False, "explanation": "Polip tanımı değildir."},
            {"key": "D", "text": "Sadece çizgili kas demetleri ve lenfoid foliküller", "isCorrect": False, "explanation": "Histolojiye uymaz."}
        ])
    ]
    slides.append(make_slide(59, "Polipte Kalın Duvarlı Damarlar ve Fibröz Stroma", "Fibröz stroma, bazalis kökenli kalın duvarlı damarlar ve siklusa uyumsuz dilate bezler", "Histopatoloji", s59_narrative, s59_bullets, s59_elements))

    # Slide 60: [TEKRAR SAYFASI - CHECKPOINT 6] Düzensiz Proliferatif Endometrium ve Endometrial Polip
    s60_narrative = (
        "Bu tekrar sayfasında 6. Bölümde ele aldığımız düzensiz proliferatif endometriumu, "
        "onkolojik ve anovulatuar zeminini, endometrial polibin bazalis kökenini ve histolojik kriterlerini konsolide ediyoruz.\n\n"
        "- **Düzensiz Proliferatif Endometrium:** Anovulatuar siklus cevabıdır; perimenapozal kadınların "
        "hemen hepsinde bulunur; uzamış karşılanmamış östrojene bağlıdır; gerçek premalign lezyon DEĞİLDİR; "
        "basit hiperplaziden bez-stroma oranının nispeten normal olmasıyla ayrılır; kistik atrofide "
        "ise epitel basıktır ve proliferatif aktivite yoktur.\n"
        "- **Endometrial Polip:** Endometrium bazalisin lokalize hiperplazisidir; benigndir; 4-5. dekatta sıktır; "
        "tamoksifen kullanımıyla (büyük ve multipl) belirgin ilişkilidir.\n"
        "- **Polip Histopatolojisi:** Dokunun 3 kenarının yüzey epiteli ile çevrili olması; fibröz stroma; "
        "kalın duvarlı damarlar; düzensiz dilate bezler ve normal siklus bulgularının bulunmaması.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Düzensiz proliferatif: premalign değil, perimenopozda evrensel, bez-stroma oranı normal; Polip: bazalis hiperplazisi, benign, tamoksifen ilişkisi, 3 kenarı epitel kaplı, kalın duvarlı damarlar."
    )
    s60_bullets = [
        "Düzensiz proliferatif: premalign değil, perimenopozda hemen hepsinde var, bez-stroma oranı korunmuş.",
        "Endometrial polip: bazalisin lokalize hiperplazisi, benign, 4-5. dekat, tamoksifen ile büyük/multipl.",
        "Polip mikroskopisi: dokunun 3 kenarı yüzey epiteli ile çevrili, fibröz stroma, kalın duvarlı damarlar."
    ]
    s60_elements = [
        make_cloze("Düzensiz proliferatif endometrium gerçek premalign değilken endometrial polip dokusunun 3 kenarı yüzey epiteli ile çevrilidir.", "3 kenarı yüzey epiteli", "Polibin kardinal histolojik kriteri"),
        make_table("6. Bölüm Büyük Lezyon Karşılaştırma Tablosu", ["Patolojik Antite", "Köken / Temel Nitelik", "Kardinal Histolojik Kriter", "Klinik İlişki"], [
            {"cells": [{"text": "Düzensiz Proliferatif Endometrium", "isMasked": False}, {"text": "Anovulatuar östrojenik yanıt (premalign değil)", "isMasked": True, "hint": "iyi huylu proliferasyon"}, {"text": "Bez/stroma oranı normal, değişken bez çapları", "isMasked": False}, {"text": "Perimenapozal kadınların hemen tümü"}]},
            {"cells": [{"text": "Endometrial Polip", "isMasked": False}, {"text": "Endometrium bazalis hiperplazisi (benign)", "isMasked": False}, {"text": "3 kenarı yüzey epiteli, kalın duvarlı damarlar", "isMasked": True, "hint": "üç tarafı epitel ve damar"}, {"text": "4-5. dekat, tamoksifen kullanımı", "isMasked": True, "hint": "kırklı yaşlar ve SERM"}]}
        ]),
        make_chain("Bölüm 6 Konsolidasyon Akışı", [
            "1. Düzensiz Proliferasyon: Anovulasyonda bez-stroma oranı korunarak değişken bezler oluşur (premalign değil).",
            "2. Polip Oluşumu: Bazaliste lokalize büyüme ile kavite içine sarkan kitle meydana gelir (benign).",
            "3. Tamoksifen İtici Gücü: SERM kullanımı büyük ve çok sayıda polipi uyarır.",
            "4. Mikroskopik Doğrulama: 3 kenarı epitel örtülü ve kalın duvarlı damarlı yapı polip tanısını kesinleştirir."
        ]),
        make_recall("6. Bölümün iki kardinal kriteri: Düzensiz proliferatif endometrium premalign midir ve polipte hangi vasküler yapı görülür?", "Düzensiz proliferatif endometrium gerçek premalign lezyon DEĞİLDİR; polip stromasında ise bazalis kökenli 'kalın duvarlı damarlar' izlenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 6. Bölüm Konsolidasyonu", [
            {"text": "Düzensiz proliferatif endometrium gerçek premalign lezyon değildir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Endometrial polip endometrium bazalisin lokalize hiperplazisi ile oluşur.", "isLie": False, "explanation": "Doğru. Polip tanımıdır."},
            {"text": "Tamoksifen kullanımı endometrial polip gelişimini %100 engeller ve tüm polipleri anında eritir.", "isLie": True, "explanation": "Tuzak! Tamoksifen kullanımı büyük ve çok sayıda endometrial polip gelişimi ile ilişkilidir."},
            {"text": "Polip kesitlerinde dokunun 3 kenarı yüzey epiteli ile çevrilidir.", "isLie": False, "explanation": "Doğru. Kardinal kriterdir."}
        ]),
        make_quiz("Düzensiz proliferatif endometrium ve endometrial polip ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Düzensiz proliferatif endometrium gerçek premalign değildir; polip bazalis hiperplazisi olup 3 kenarı epitel kaplıdır", "isCorrect": True, "explanation": "Ders notundaki iki temel antitenin kardinal özellikleri eksiksiz ve doğru özetlenmiştir."},
            {"key": "B", "text": "Her iki lezyon da anaplastik yüksek dereceli sarkomdur", "isCorrect": False, "explanation": "Her ikisi de benigndir."},
            {"key": "C", "text": "Polip sadece 1. dekatta görülür, tamoksifenle hiçbir bağı yoktur", "isCorrect": False, "explanation": "4-5. dekatta sıktır ve tamoksifenle ilişkilidir."},
            {"key": "D", "text": "Düzensiz proliferatif endometriumda stroma tamamen kaybolur", "isCorrect": False, "explanation": "Bez-stroma oranı normal korunmuştur."}
        ])
    ]
    slides.append(make_slide(60, "[TEKRAR SAYFASI - CHECKPOINT 6] Düzensiz Proliferatif Endometrium ve Endometrial Polip", "6. Bölümün konsolidasyonu: düzensiz proliferasyon (premalign değil, perimenopoz), polip (bazalis, tamoksifen, 3 kenar kuralı, kalın damarlar)", "Bölüm Tekrarı", s60_narrative, s60_bullets, s60_elements))

    return slides
