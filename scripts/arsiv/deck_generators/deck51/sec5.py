# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec5():
    slides = []

    # Slide 41: Komplike Üriner Sistem Enfeksiyonu Temel Tanımı
    s41_narrative = (
        "Komplike üriner sistem enfeksiyonu, standart antibiyotik tedavisine yanıtın geciktiği, tedavi "
        "başarısızlığı veya nüks riskinin yüksek olduğu ve dokusal harabiyet ihtimalinin arttığı klinik durumdur.\n\n"
        "- **Temel Belirleyici:** Enfeksiyonun basit bir mukozal tutulumdan çıkıp komplike hale gelmesi, "
        "konağa ait yapısal, fonksiyonel veya sistemik faktörlerin eşlik etmesine bağlıdır.\n"
        "- **Erkeklerdeki Durum:** Erkek cinsiyette gelişen tüm ÜSE'ler anatomik yapı ve gençlikteki "
        "düşük insidans nedeniyle **aksi ispatlanmadıkça komplike kabul edilir**.\n"
        "- **Semptom Şiddeti:** Komplike ÜSE'lerde semptomlar sıklıkla daha alevlidir; ancak yaşlı veya "
        "düşkün hastalarda tek semptomun sadece genel durum bozukluğu olabileceği unutulmamalıdır.\n\n"
        "> [!NOTE]\n"
        "> Komplike ÜSE, hastada enfeksiyonun yayılmasını kolaylaştıran veya eradikasyonunu zorlaştıran bir ek risk faktörünün varlığı ile tanımlanır."
    )
    s41_bullets = [
        "Tedavi başarısızlığı ve komplikasyon riski yüksek enfeksiyonlardır.",
        "Erkeklerde aksi ispatlanmadıkça tüm ÜSE'ler komplike kabul edilir.",
        "Yaşlılarda alevli semptom yerine izole genel durum bozukluğu görülebilir."
    ]
    s41_elements = [
        make_cloze("Erkek hastalarda ortaya çıkan üriner enfeksiyonlar aksi ispatlanmadıkça komplike kabul edilmektedir.", "komplike", "Yüksek riskli ve yapısal faktör içeren enfeksiyon sınıfı"),
        make_table("Komplike ÜSE Karakteristikleri", ["Özellik", "Komplike Olmayan ÜSE", "Komplike ÜSE"], [
            {"cells": [{"text": "Hasta Popülasyonu", "isMasked": False}, {"text": "Sağlıklı, gebe olmayan premenopozal kadın", "isMasked": False}, {"text": "Erkekler, gebeler, diyabetikler, yaşlılar", "isMasked": True, "hint": "riskli ve metabolik hasta grubu"}]},
            {"cells": [{"text": "Üriner Sistem Yapısı", "isMasked": False}, {"text": "Normal anatomi ve fonksiyon", "isMasked": False}, {"text": "Taş, kateter, darlık, VUR veya staz", "isMasked": True, "hint": "tıkanıklık veya yabancı cisim"}]},
            {"cells": [{"text": "Tedavi Yanıtı", "isMasked": False}, {"text": "Kısa sürede hızlı kür", "isMasked": False}, {"text": "Dirençli, uzun tedavi gerektiren seyir", "isMasked": False}]}
        ]),
        make_chain("Komplike Enfeksiyon Gelişim Zinciri", [
            "1. Zemin: Hastada anatomik (taş) veya metabolik (diyabet) bir anomali vardır.",
            "2. Bakteriyel Tutulum: Fırsatçı veya dirençli patojenler dokuya girer.",
            "3. Eradikasyon Güçlüğü: Yabancı cisim veya staz nedeniyle antibiyotikler yetersiz kalır.",
            "4. Doku Harabiyeti: Enfeksiyon parankime yayılarak abse ve sepsis riski yaratır."
        ]),
        make_recall("Komplike ÜSE'yi komplike olmayan formdan ayıran temel patofizyolojik zemin nedir?", "Hastada yapısal, fonksiyonel veya sistemik komplike edici bir faktörün (taş, kateter, diyabet, gebelik, erkek cinsiyet) bulunmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komplike ÜSE Tanımı", [
            {"text": "Erkeklerde aksi ispatlanmadıkça gelişen ÜSE komplike kabul edilir.", "isLie": False, "explanation": "Doğru. Temel klinik kuraldır."},
            {"text": "Komplike ÜSE'de semptomlar genellikle daha alevli seyreder.", "isLie": False, "explanation": "Doğru. Doku tutulumu fazladır."},
            {"text": "Komplike ÜSE sadece 1 günlük tek doz aspirinle tamamen iyileşen en basit hastalıktır.", "isLie": True, "explanation": "Tuzak! Komplike ÜSE tedavi başarısızlığı riski yüksek, uzun süreli antibiyotik gerektiren ciddi bir tablodur."},
            {"text": "Yaşlı hastalarda ÜSE'nin tek semptomu genel durum bozukluğu olabilir.", "isLie": False, "explanation": "Doğru. Atipik klinik sıktır."}
        ]),
        make_quiz("Klinik pratikte erkek bir hastada idrar yolu enfeksiyonu saptandığında aksi ispatlanmadıkça hangi sınıfa dahil edilir?", [
            {"key": "A", "text": "Komplike üriner sistem enfeksiyonu", "isCorrect": True, "explanation": "Ders notunda erkeklerde gelişen ÜSE'lerin aksi ispatlanmadıkça komplike kabul edildiği açıkça belirtilmiştir."},
            {"key": "B", "text": "Fizyolojik idrar değişimi", "isCorrect": False, "explanation": "Enfeksiyon fizyolojik değildir."},
            {"key": "C", "text": "Zararsız basit balayı sistiti", "isCorrect": False, "explanation": "Erkekte balayı sistiti tanımlanmaz."},
            {"key": "D", "text": "Yalnızca deri döküntüsü", "isCorrect": False, "explanation": "Üriner enfeksiyondur."}
        ])
    ]
    slides.append(make_slide(41, "Komplike Üriner Sistem Enfeksiyonu Temel Tanımı", "Komplike ÜSE kriterleri, erkeklerde komplike kabulü ve semptom şiddeti", "Komplike ÜSE", s41_narrative, s41_bullets, s41_elements))

    # Slide 42: Ateşin Rolü: Komplike Edici Faktör Değil, Klinik Bulgudur!
    s42_narrative = (
        "Tıp fakültesi sınavlarında ve klinik sınıflamalarda en sık karıştırılan ve öğrencilerin "
        "tuzağa düştüğü en kritik kavram ateştir.\n\n"
        "- **Klinik Bulgu İlkesi:** Ateş yüksekliği, konağın bakteriyel pirojenlere karşı geliştirdiği "
        "sistemik bir enflamatuar yanıttır; yani **ateş bir klinik bulgudur**.\n"
        "- **Komplike Faktör Ayrımı:** Komplike edici faktörler ise enfeksiyonun ortaya çıkmasına veya "
        "tedavinin güçleşmesine neden olan **zemin hazırlayıcı anatomik, fonksiyonel veya fizyolojik koşullardır**.\n"
        "- **Sınavın Altın Kuralı:** Erkek cinsiyet, gebelik, kontrolsüz DM, nörojenik mesane ve nefrolitiazis "
        "komplike edici birer faktördür; ancak **ateş yüksekliği komplike edici faktör DEĞİLDİR!**\n\n"
        "> [!WARNING]\n"
        "> [ÇIKMIŞ SORU UYARISI] 'Ateş yüksekliği' bir komplikasyon nedeni veya komplike edici faktör değildir; enfeksiyonun bir klinik bulgusudur (piyelonefrit göstergesidir)!"
    )
    s42_bullets = [
        "Ateş yüksekliği komplike edici bir faktör DEĞİL, klinik bir bulgudur.",
        "Komplike edici faktörler zemin hazırlayan anatomik/sistemik durumlardır.",
        "Erkek cinsiyet, gebelik, DM, taş ve nörojenik mesane gerçek komplike edici faktörlerdir."
    ]
    s42_elements = [
        make_cloze("Sınavların klasik sorusu: Ateş yüksekliği komplike edici faktör olmayıp enfeksiyonun bir klinik bulgusudur.", "klinik bulgusudur", "Hastalığın semptom ve muayene işareti"),
        make_table("Klinik Bulgu ve Komplike Faktör Ayrımı", ["Kavram", "Tanısal Niteliği", "Tıbbi Örnekler"], [
            {"cells": [{"text": "Ateş Yüksekliği", "isMasked": False}, {"text": "Enfeksiyonun KLİNİK BULGUSUDUR", "isMasked": True, "hint": "hastanın muayene bulgusu"}, {"text": "Pirojenlerin termoregülasyon merkezini uyarması"}]},
            {"cells": [{"text": "Komplike Edici Faktör", "isMasked": False}, {"text": "Altta yatan RİSK FAKTÖRÜ / ZEMİNDİR", "isMasked": False}, {"text": "Gebelik, erkek cinsiyet, kontrolsüz DM, taş, kateter", "isMasked": True, "hint": "anatomik veya metabolik zemin"}]}
        ]),
        make_chain("Ateşin Fizyopatolojik Yeri", [
            "1. Zemin: Hastada nefrolitiazis (komplike edici faktör) mevcuttur.",
            "2. İnvazyon: Bakteri böbrek parankimini enfekte eder.",
            "3. Sitokin Salınımı: İnterlökin-1 ve TNF-alfa hipotalamusu uyarır.",
            "4. Klinik Bulgu: Ateş yükselir (bu bir zemin değil, tablonun klinik sonucudur)."
        ]),
        make_recall("Tıp sınavlarının en klasik sorusu: 'Ateş yüksekliği' ÜSE için komplike edici bir faktör müdür?", "HAYIR! Ateş yüksekliği komplike edici bir faktör değil, enfeksiyonun sistemik bir klinik bulgusudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ateş ve Komplike Faktör", [
            {"text": "Ateş yüksekliği ÜSE için komplike edici bir faktör değil, klinik bir bulgudur.", "isLie": False, "explanation": "Doğru. En kritik sınav ayrımıdır."},
            {"text": "Erkek cinsiyet, gebelik ve kontrolsüz DM komplike edici faktörlerdendir.", "isLie": False, "explanation": "Doğru. Gerçek zemin hazırlayıcılardır."},
            {"text": "Ateş yüksekliği bir anatomi bozukluğu olup hastayı otomatikman ameliyatlık eder.", "isLie": True, "explanation": "Tuzak! Ateş sistemik enflamatuar bir bulgudur, tek başına anatomik cerrahi faktör değildir."},
            {"text": "Nefrolitiazis (böbrek taşı) yapısal bir komplike edici faktördür.", "isLie": False, "explanation": "Doğru. Mekanik tıkanıklık yapar."}
        ]),
        make_quiz("Aşağıdakilerden hangisi üriner sistem enfeksiyonu (ÜSE) için komplike edici faktörlerden biri DEĞİLDİR?", [
            {"key": "A", "text": "Ateş yüksekliği olması", "isCorrect": True, "explanation": "Ateş yüksekliği komplike edici bir faktör değil, enfeksiyonun klinik bir bulgusudur (Kurul 1 çıkmış sorusudur)."},
            {"key": "B", "text": "Erkek cinsiyet", "isCorrect": False, "explanation": "Komplike edici faktördür."},
            {"key": "C", "text": "Nefrolitiazis (böbrek taşı)", "isCorrect": False, "explanation": "Komplike edici faktördür."},
            {"key": "D", "text": "Nörojenik mesane ve kontrolsüz DM", "isCorrect": False, "explanation": "Komplike edici faktörlerdir."}
        ])
    ]
    slides.append(make_slide(42, "Ateşin Rolü: Komplike Edici Faktör Değil, Klinik Bulgudur!", "Ateşin klinik bulgu olması, komplike edici faktörler (DM, taş, gebelik, erkek)", "Komplike ÜSE", s42_narrative, s42_bullets, s42_elements))

    # Slide 43: Sistemik Komplike Edici Faktörler: Gebelik, Kontrolsüz DM, İmmünsupresyon
    s43_narrative = (
        "Sistemik faktörler, konağın tüm dokularındaki hücresel immün yanıtı zayıflatan veya gebelik "
        "gibi fizyolojik adaptasyonlarla üriner staz yaratan durumlardır.\n\n"
        "- **Gebelik:** Progesteron hormonunun etkisiyle üreter düz kaslarında gevşeme ve dilatasyon (hidroüreter), "
        "büyüyen uterusun mekanik basısı ve immün tolerans nedeniyle ÜSE'ler hızla pyelonefrite ilerler.\n"
        "- **Kontrolsüz Diabetes Mellitus:** Glukozüri bakteri proliferasyonunu uyarırken, lökosit "
        "fagositoz yetersizliği ve diyabetik nöropati enfeksiyonun dokuda derinleşmesine yol açar.\n"
        "- **İmmünsupresif Durumlar ve Nozokomiyal Enfeksiyonlar:** Kemoterapi, kortikosteroid kullanımı, "
        "organ nakli ve hastane kaynaklı enfeksiyonlar çoklu dirençli üropatojenlerle seyreder.\n\n"
        "> [!IMPORTANT]\n"
        "> Gebe veya kontrolsüz diyabetik bir kadında sistit semptomu dahi olsa tablo 'komplike ÜSE' olarak yönetilmelidir."
    )
    s43_bullets = [
        "Gebelik progesteron aracılı üreter gevşemesi ve bası ile staz yaratır.",
        "Kontrolsüz DM lökosit felci ve glukozüri ile tabloyu ağırlaştırır.",
        "İmmünsupresyon ve hastane kaynaklı enfeksiyonlar dirençli patojenleri barındırır."
    ]
    s43_elements = [
        make_cloze("Gebelikte progesteron etkisiyle üreterlerde dilatasyon gelişmesi enfeksiyonu komplike hale getiren fizyolojik bir faktördür.", "progesteron", "Gebelikte üreter kaslarını gevşeten hormon"),
        make_table("Sistemik Komplike Edici Faktörler", ["Faktör", "Fizyopatolojik Süreç", "Klinik Risk"], [
            {"cells": [{"text": "Gebelik", "isMasked": False}, {"text": "Progesterona bağlı dilatasyon ve bası", "isMasked": True, "hint": "üreter genişlemesi ve mekanik baskı"}, {"text": "Hızla pyelonefrit ve preterm eylem riski"}]},
            {"cells": [{"text": "Kontrolsüz DM", "isMasked": False}, {"text": "Glukozüri ve nörojenik mesane", "isMasked": False}, {"text": "Amfizematöz pyelonefrit ve renal abse", "isMasked": True, "hint": "gazlı böbrek iltihabı riski"}]},
            {"cells": [{"text": "İmmünsupresyon", "isMasked": False}, {"text": "Fagositik ve lenfoid baskılanma", "isMasked": False}, {"text": "Dirençli ve fırsatçı patojenler", "isMasked": False}]}
        ]),
        make_chain("Gebelikte Komplike Seyir Zinciri", [
            "1. Hormonal Etki: Progesteron üreter peristaltizmini gevşetir.",
            "2. Mekanik Bası: Büyüyen uterus üreterleri sıkıştırarak staz oluşturur.",
            "3. Bakteri Tırmanışı: Basit mesane bakterileri rahatça böbreğe ulaşır.",
            "4. Pyelonefrit Riski: Gebelikte tedavi edilmeyen sistitlerin %40'ı pyelonefrite döner."
        ]),
        make_recall("Gebelikte basit bir idrar yolu enfeksiyonunun hızla komplike pyelonefrite dönüşmesine yol açan temel hormonal faktör nedir?", "Progesteron hormonunun üreter düz kaslarını gevşeterek dilatasyon ve staz yaratmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sistemik Faktörler", [
            {"text": "Gebelik ÜSE için en önemli sistemik komplike edici faktörlerdendir.", "isLie": False, "explanation": "Doğru. Fetal ve maternal risk taşır."},
            {"text": "Kontrolsüz diyabet lökosit fonksiyonlarını baskılayarak enfeksiyonu derinleştirir.", "isLie": False, "explanation": "Doğru. Glukozüri de besiyeri sunar."},
            {"text": "Gebelikte idrar yolları taş gibi sertleşir ve hiçbir mikrop içeri giremez.", "isLie": True, "explanation": "Tuzak! Gebelikte progesteron etkisiyle üreterler gevşer, genişler ve staz nedeniyle enfeksiyon riski katlanır."},
            {"text": "Hastane kaynaklı (nozokomiyal) enfeksiyonlar komplike faktör sayılır.", "isLie": False, "explanation": "Doğru. Dirençli suşlar rol oynar."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'yi 'komplike' kılan sistemik durumlardan biri DEĞİLDİR?", [
            {"key": "A", "text": "Gebelik", "isCorrect": False, "explanation": "Sistemik komplike edici faktördür."},
            {"key": "B", "text": "Kontrolsüz Diabetes Mellitus", "isCorrect": False, "explanation": "Sistemik komplike edici faktördür."},
            {"key": "C", "text": "Sağlıklı, gebe olmayan 22 yaşında premenopozal kadın", "isCorrect": True, "explanation": "Sağlıklı, gebe olmayan premenopozal kadın komplike olmayan (basit) sistitin prototipik hastasıdır."},
            {"key": "D", "text": "Organ nakli sonrası immünsupresif tedavi alan hasta", "isCorrect": False, "explanation": "Sistemik komplike faktördür."}
        ])
    ]
    slides.append(make_slide(43, "Sistemik Komplike Edici Faktörler: Gebelik, Kontrolsüz DM, İmmünsupresyon", "Gebelik fizyolojisi, kontrolsüz DM, immünsupresyon ve hastane kaynaklı enfeksiyonlar", "Komplike ÜSE", s43_narrative, s43_bullets, s43_elements))

    # Slide 44: Fonksiyonel Komplike Edici Faktörler: Nörojenik Mesane, VUR, Kateterler
    s44_narrative = (
        "Üriner traktusun nöromusküler koordinasyonunu bozan fonksiyonel anomaliler, idrarın normal "
        "yönde dinamik akışını imkansız hale getirerek enfeksiyonu kronikleştirir.\n\n"
        "- **Vezikoüreteral Reflü (VUR):** Mesane ile üreter arasındaki valvüler mekanizmanın bozulması "
        "sonucu, miksiyon sırasında mesane idrarının üreterlere ve böbreğe geri kaçmasıdır.\n"
        "- **Spinal Kord Hasarı ve Nörojenik Mesane:** Omurilik yaralanmaları veya spina bifida gibi "
        "lezyonlarda detrüsör-sfinkter dissinerjisi oluşur; mesane basıncı aşırı yükselir ve staz kalıcılaşır.\n"
        "- **Eksternal Kateter Varlığı:** Üretral kateter, suprapubik sistostomi veya perkütan "
        "nefrostomi tüpleri bakterilerin vücut dışından doğrudan üriner lümene tırmandığı açık kapılardır.\n\n"
        "> [!IMPORTANT]\n"
        "> VUR, çocukluk çağında tekrarlayan pyelonefrit ataklarına ve kalıcı renal skar (reflü nefropatisi) gelişimine yol açan en tehlikeli fonksiyonel anomalidir."
    )
    s44_bullets = [
        "VUR mesane idrarının retrograd böbreğe kaçması ve pyelonefrit nedenidir.",
        "Spinal kord hasarı detrüsör sfinkter koordinasyonunu felç ederek staz yapar.",
        "Üretral, suprapubik veya nefrostomi kateterleri kalıcı yabancı cisim kapısıdır."
    ]
    s44_elements = [
        make_cloze("Mesane idrarının miksiyon esnasında geriye böbreğe kaçması vezikoüreteral reflü olarak tanımlanır.", "vezikoüreteral reflü", "İdrarın üretere geri kaçış anomalisi"),
        make_table("Fonksiyonel Komplike Faktörler", ["Anomali", "Fizyopatolojik Mekanizma", "Klinik Yansıması"], [
            {"cells": [{"text": "Vezikoüreteral Reflü (VUR)", "isMasked": False}, {"text": "Üreterovezikal bileşke yetersizliği", "isMasked": True, "hint": "mesane-üreter kapakçık bozukluğu"}, {"text": "İdrarın böbreğe geri pompalanması ve renal skar"}]},
            {"cells": [{"text": "Nörojenik Mesane", "isMasked": False}, {"text": "Spinal kord hasarı / detrüsör atoni", "isMasked": False}, {"text": "Yüksek intravezikal basınç ve boşalamama", "isMasked": True, "hint": "idrarı dışarı atamama"}]},
            {"cells": [{"text": "Eksternal Kateterler", "isMasked": False}, {"text": "Üretral, suprapubik veya nefrostomi", "isMasked": False}, {"text": "Dış ortamdan lümene sürekli bakteriyel geçiş", "isMasked": False}]}
        ]),
        make_chain("VUR ve Böbrek Hasarı Zinciri", [
            "1. Valv Yetersizliği: Üreterovezikal kapakçık kapanmaz.",
            "2. Reflü: Mesane kasıldığında enfekte idrar üreterden renal papillaya fışkırır.",
            "3. İntrarenal Reflü: Bakteriler tübüllere ve parankime zorla enjekte edilir.",
            "4. Kronik Skarlaşma: Her atakta renal doku kaybı ve hipertansiyon gelişir."
        ]),
        make_recall("Üriner sistemde fonksiyonel komplike faktörler arasında sayılan üç temel klinik durum nedir?", "Vezikoüreteral reflü (VUR), spinal kord hasarı / nörojenik mesane ve eksternal kateter (üretral, suprapubik, nefrostomi) varlığıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fonksiyonel Faktörler", [
            {"text": "VUR enfekte idrarın böbreğe kaçmasına yol açan fonksiyonel bir faktördür.", "isLie": False, "explanation": "Doğru. Reflü pyelonefriti tetikler."},
            {"text": "Nörojenik mesane yüksek rezidüel idrar bırakarak enfeksiyonu komplike kılar.", "isLie": False, "explanation": "Doğru. Staz ve yüksek basınç oluşturur."},
            {"text": "Suprapubik kateter varlığı hastayı mikroplara karşı %100 koruyan kapalı bir zırhtır.", "isLie": True, "explanation": "Tuzak! Kateterler yabancı cisimdir ve dışarıdan lümene bakteri göçünü kolaylaştıran risklerdir."},
            {"text": "Spinal kord hasarı mesane boşalma dinamiğini bozar.", "isLie": False, "explanation": "Doğru. Fonksiyonel risk faktörüdür."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'yi komplike kılan FONKSİYONEL anomalilerden biridir?", [
            {"key": "A", "text": "Vezikoüreteral reflü (VUR) ve nörojenik mesane", "isCorrect": True, "explanation": "Ders notunda fonksiyonel anomaliler VUR, spinal kord hasarı, nörojenik mesane ve kateter varlığı olarak sayılmıştır."},
            {"key": "B", "text": "Böbrek taşının lümeni tıkaması", "isCorrect": False, "explanation": "Bu yapısal anomalidir."},
            {"key": "C", "text": "Polikistik böbrek hastalığı", "isCorrect": False, "explanation": "Bu yapısal kistik anomalidir."},
            {"key": "D", "text": "Amfizematöz pyelonefrit", "isCorrect": False, "explanation": "Bu yapısal doku hasarıdır."}
        ])
    ]
    slides.append(make_slide(44, "Fonksiyonel Komplike Edici Faktörler: Nörojenik Mesane, VUR, Kateterler", "Vezikoüreteral reflü, spinal kord hasarı, nörojenik mesane ve eksternal kateterler", "Komplike ÜSE", s44_narrative, s44_bullets, s44_elements))

    # Slide 45: Yapısal Komplike Edici Faktörler: Nefrolitiazis, Obstrüksiyon, Polikistik Böbrek
    s45_narrative = (
        "Üriner traktusun anatomik mimarisini bozan, kitle etkisi yaratan veya idrar kanalını tıkayan "
        "yapısal lezyonlar komplike ÜSE'nin cerrahi ve mekanik temelini oluşturur.\n\n"
        "- **Üriner Obstrüksiyon ve Nefrolitiazis:** Böbrek taşı (nefrolitiazis), üreter taşı veya "
        "ürotelyal tümörler akımı mekanik olarak bloke eder; obstrüksiyon arkasında gelişen enfeksiyon "
        "acil dekompresyon gerektiren ürosepsis tablosuna dönüşür.\n"
        "- **Polikistik Böbrek Hastalığı (PKBH):** Parankimi dolduran kistlerin enfekte olması "
        "(kist enfeksiyonu), kist duvarına antibiyotiklerin penetre olamaması nedeniyle tedaviyi aşırı güçleştirir.\n"
        "- **Amfizematöz Değişiklikler:** Parankimde gaz toplanmasıyla seyreden yapısal harabiyettir; "
        "bu yapısal faktörler cerrahi müdahale veya drenaj olmaksızın medikal olarak iyileşemez.\n\n"
        "> [!IMPORTANT]\n"
        "> Obstrüksiyonla birlikte seyreden pyelonefrit bir ürolojik acildir; acil stent veya nefrostomi ile idrar drenajı sağlanmalıdır."
    )
    s45_bullets = [
        "Taş veya tümör obstrüksiyonu akımı keserek enfeksiyonu hapseder.",
        "Polikistik böbrek hastalığında kist içi enfeksiyonlar antibiyotik penetrasyonunu engeller.",
        "Yapısal anomaliler cerrahi/girişimsel düzeltme gerektiren durumlardır."
    ]
    s45_elements = [
        make_cloze("Üriner sistemde mekanik tıkanıklık yaratan taş ve tümörler yapısal komplike edici faktörlerin başında gelir.", "yapısal", "Anatomik mimariyi ve kanalı bozan faktör sınıfı"),
        make_table("Yapısal Komplike Edici Faktörler", ["Yapısal Faktör", "Patolojik Özellik", "Klinik Tehlike"], [
            {"cells": [{"text": "Nefrolitiazis (Taş)", "isMasked": False}, {"text": "Lümen obstrüksiyonu ve biyofilm", "isMasked": True, "hint": "idrar kanalını tıkama ve mikrop yuvası"}, {"text": "Tıkanma + enfeksiyon = Piyonefroz / Sepsis"}]},
            {"cells": [{"text": "Polikistik Böbrek (PKBH)", "isMasked": False}, {"text": "Kist içi enfeksiyon odakları", "isMasked": False}, {"text": "Antibiyotik penetrasyon yetersizliği", "isMasked": True, "hint": "ilacın kist sıvısına geçememesi"}]},
            {"cells": [{"text": "Amfizematöz Değişiklikler", "isMasked": False}, {"text": "Doku içinde gaz formasyonu", "isMasked": False}, {"text": "Fulminan parankim nekrozu", "isMasked": False}]}
        ]),
        make_chain("Obstrüktif Piyonefroz Zinciri", [
            "1. Tıkanma: Üreter taşı lümeni tam tıkar.",
            "2. Hapsolma: Böbrek pelvisinde enfekte idrar yüksek basınç altında göllenir.",
            "3. Piyonefroz: Toplayıcı sistem püy ile dolarak gerilir.",
            "4. Sepsis Patlaması: Basınçla bakteriler renal venöz dolaşıma fırlar (acil drenaj şarttır)."
        ]),
        make_recall("Üriner sistemde yapısal komplike edici faktörler arasında sayılan üç majör durum nedir?", "Üriner obstrüksiyon (taş, tümör vb.), polikistik böbrek hastalığı ve amfizematöz pyelonefrittir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Yapısal Faktörler", [
            {"text": "Nefrolitiazis (böbrek taşı) ÜSE için yapısal bir komplike edici faktördür.", "isLie": False, "explanation": "Doğru. Mekanik obstrüksiyon yapar."},
            {"text": "Polikistik böbrek hastalığında kist enfeksiyonları tedaviyi zorlaştırır.", "isLie": False, "explanation": "Doğru. İlaç penetrasyonu düşüktür."},
            {"text": "Taş ile tıkanmış böbrekte enfeksiyon varsa hiçbir şey yapmadan 2 ay evde dinlenilir.", "isLie": True, "explanation": "Tuzak! Obstrükte enfekte böbrek (piyonefroz) acil ürolojik girişim (drenaj/stent) gerektiren hayatı tehdit edici bir durumdur."},
            {"text": "Amfizematöz pyelonefrit dokuda gaz toplanmasıyla giden yapısal bir tablodur.", "isLie": False, "explanation": "Doğru. Ağır nekrozdur."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'yi komplike kılan YAPISAL (anatomik) faktörlerden biridir?", [
            {"key": "A", "text": "Üriner sistemde obstrüksiyon (taş, tümör) ve polikistik böbrek hastalığı", "isCorrect": True, "explanation": "Ders notunda yapısal anomaliler: amfizematöz pyelonefrit, polikistik böbrek hastalığı ve üriner sistemde obstrüksiyon (taş, tümör) olarak verilmiştir."},
            {"key": "B", "text": "Yalnızca cinsel ilişki sıklığı", "isCorrect": False, "explanation": "Bu davranışsal faktördür."},
            {"key": "C", "text": "Vitamin C eksikliği", "isCorrect": False, "explanation": "Yapısal faktör değildir."},
            {"key": "D", "text": "Hafif nezle hali", "isCorrect": False, "explanation": "Üriner patoloji değildir."}
        ])
    ]
    slides.append(make_slide(45, "Yapısal Komplike Edici Faktörler: Nefrolitiazis, Obstrüksiyon, Polikistik Böbrek", "Taş obstrüksiyonu, tümörler, polikistik böbrek hastalığı ve yapısal hasarlar", "Komplike ÜSE", s45_narrative, s45_bullets, s45_elements))

    # Slide 46: Amfizematöz Pyelonefrit ve Nefrektomi Endikasyonu
    s46_narrative = (
        "Amfizematöz pyelonefrit, renal parankimde ve perirenal dokularda gaz oluşumu ile karakterize, "
        "komplike ÜSE'nin en ölümcül ve fulminan varyantıdır.\n\n"
        "- **Hedef Popülasyon:** Olguların ezici çoğunluğu **kontrolsüz Diabetes Mellitus** hastalarıdır; "
        "yüksek doku glukozu anaerobik/fakültatif gaz üreten bakteriler için substrat sağlar.\n"
        "- **Gaz Üretimi:** E. coli ve Klebsiella suşları glukozu fermente ederek karbondioksit ve hidrojen "
        "gazı açığa çıkarır; radyolojide böbrek lojunda çizgisel gaz paternleri izlenir.\n"
        "- **Acil Tedavi Yaklaşımı:** Mortalitesi son derece yüksek bir tablodur; agresif parenteral "
        "antibiyoterapiye rağmen kontrol altına alınamayan olgularda hayat kurtarıcı kesin tedavi **acil nefrektomidir**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Amfizematöz pyelonefrit diyabetiklerde görülür, gaz oluşturan bakterilerle seyreder ve yüksek mortalitesi nedeniyle acil cerrahi nefrektomi gerektirir."
    )
    s46_bullets = [
        "Kontrolsüz diyabetik hastalarda gaz üreten bakterilerle gelişir.",
        "Renal parankim ve perirenal alanda doku nekrozu ve gaz toplanır.",
        "Yüksek mortaliteye sahiptir; acil yaklaşım cerrahi nefrektomidir."
    ]
    s46_elements = [
        make_cloze("Diyabetiklerde yüksek mortaliteyle seyreden amfizematöz pyelonefrit tablosunda definitif cerrahi tedavi nefrektomi uygulanmasıdır.", "nefrektomi", "Böbreğin cerrahi olarak tamamen çıkarılması"),
        make_table("Amfizematöz Pyelonefrit Profili", ["Klinik Özellik", "Patolojik Bulgu", "Klinik Karar"], [
            {"cells": [{"text": "Hasta Popülasyonu", "isMasked": False}, {"text": "Kontrolsüz Diabetes Mellitus (%90+)", "isMasked": True, "hint": "yüksek kan şekerli diyabetikler"}, {"text": "Dokuda yüksek glukoz fermentasyonu"}]},
            {"cells": [{"text": "Radyolojik Belirti", "isMasked": False}, {"text": "Böbrek parankiminde gaz toplanması", "isMasked": False}, {"text": "Direkt grafi ve BT'de gaz gölgeleri", "isMasked": True, "hint": "parankimde hava varlığı"}]},
            {"cells": [{"text": "Cerrahi Tedavi", "isMasked": False}, {"text": "Acil cerrahi nefrektomi", "isMasked": True, "hint": "etkilenen böbreğin alınması"}, {"text": "Fulminan septik ölümü önleme"}]}
        ]),
        make_chain("Amfizematöz Yıkım Zinciri", [
            "1. İskemi ve Glukoz: Diyabetik böbrekte mikroanjiyopati ve yoğun doku şekeri birikir.",
            "2. Gazlı Fermentasyon: E. coli glukozu fermente ederek dokuda gaz kabarcıkları örer.",
            "3. Nekroz: Gaz ve toksinler renal parankimi süratle eriterek kangrenleştirir.",
            "4. Acil Nefrektomi: Organ çıkarılmazsa hasta saatler içinde septik şoktan kaybedilir."
        ]),
        make_recall("Diyabetik hastalarda gaz oluşturan bakterilerle gelişen, yüksek mortaliteli amfizematöz pyelonefritte uygulanan cerrahi yöntem nedir?", "Nefrektomidir (etkilenen böbreğin cerrahi olarak çıkarılması)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Amfizematöz Pyelonefrit", [
            {"text": "Amfizematöz pyelonefrit sıklıkla kontrolsüz diyabetik hastalarda görülür.", "isLie": False, "explanation": "Doğru. Glukoz fermentasyonu vardır."},
            {"text": "Parankimde ve perirenal alanda gaz toplanması ile karakterizedir.", "isLie": False, "explanation": "Doğru. Adını buradan alır."},
            {"text": "Amfizematöz pyelonefrit tamamen zararsız bir gaz birikimidir ve gazoz içerek düzelir.", "isLie": True, "explanation": "Tuzak! Amfizematöz pyelonefrit mortalitesi aşırı yüksek fulminan bir nekrozdur ve acil nefrektomi gerektirir."},
            {"text": "Tedaviye dirençli ağır vakalarda nefrektomi hayat kurtarıcıdır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("Diyabetik bir hastada böbrek parankiminde gaz oluşumu ile seyreden, mortalitesi yüksek amfizematöz pyelonefrit tablosunda temel cerrahi yaklaşım nedir?", [
            {"key": "A", "text": "Nefrektomi uygulanması", "isCorrect": True, "explanation": "Ders notunda 'amfizematöz pyelonefrit (diyabetiklerde görülür ve mortalitesi yüksektir) için nefrektomi uygulanır' açıkça ifade edilmiştir."},
            {"key": "B", "text": "Yalnızca böbreğe masaj yapılması", "isCorrect": False, "explanation": "Tıbbi değeri yoktur."},
            {"key": "C", "text": "Böbreğin içine hava üflenmesi", "isCorrect": False, "explanation": "Durumu daha da kötüleştirir."},
            {"key": "D", "text": "Sadece B vitamini takviyesi verilmesi", "isCorrect": False, "explanation": "Yetersizdir."}
        ])
    ]
    slides.append(make_slide(46, "Amfizematöz Pyelonefrit ve Nefrektomi Endikasyonu", "Diyabet ilişkisi, gaz fermentasyonu, yüksek mortalite ve nefrektomi", "Komplike ÜSE", s46_narrative, s46_bullets, s46_elements))

    # Slide 47: Renal ve Perirenal Abse Gelişimi ve Drenaj
    s47_narrative = (
        "Komplike pyelonefritin en tehlikeli fokal süpüratif komplikasyonları böbrek parankimi içinde "
        "koleksiyon oluşturan renal apseler ve Gerota fasyası içine yayılan perirenal apselerdir.\n\n"
        "- **Oluşum Dinamikleri:** Asendan yolla tıkanmış bir böbrekte bakterilerin parankimi eritmesiyle "
        "veya hematojen yolla (özellikle S. aureus bakteriyemisi) kortekste mikroapselerin birleşmesiyle doğar.\n"
        "- **Klinik Şüphe:** Uygun parenteral antibiyotik tedavisine rağmen **tedavinin 3-4. gününde "
        "ateşi düşmeyen** pyelonefrit hastalarında mutlaka renal/perirenal abse şüphelenilmelidir.\n"
        "- **Drenajın Zorunluluğu:** Abse püy dolu kapalı bir kavitedir; antibiyotikler avasküler püy içine "
        "penetre olamaz. Bu nedenle temel tedavi **perkütan drenaj veya cerrahi drenajdır**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Antibiyotik tedavisine rağmen 72 saatte (3-4. günde) ateşi düşmeyen pyelonefritte USG/BT ile renal/perirenal abse aranmalı ve cerrahi/perkütanöz drenaj yapılmalıdır."
    )
    s47_bullets = [
        "Renal/perirenal abse parankimal nekroz ve püy koleksiyonudur.",
        "Antibiyotik tedavisinin 3-4. gününde düşmeyen ateşte abse aranmalıdır.",
        "Tedavide temel kural perkütan veya cerrahi drenaj uygulanmasıdır."
    ]
    s47_elements = [
        make_cloze("Renal ve perirenal apselerin tedavisinde antibiyotiklerin yanı sıra temel yaklaşım cerrahi ya da perkütanöz drenaj uygulanmasıdır.", "drenaj", "Koleksiyonun iğne veya ameliyatla boşaltılması"),
        make_table("Renal / Perirenal Abse Yönetimi", ["Aşama", "Klinik Kriter", "Gereken Girişim"], [
            {"cells": [{"text": "Şüphe Eşiği", "isMasked": False}, {"text": "Tedavinin 3-4. gününde devam eden ateş", "isMasked": True, "hint": "72 saat sonra düşmeyen vücut ısısı"}, {"text": "Acil renal ultrasonografi veya kontrastlı BT"}]},
            {"cells": [{"text": "Görüntüleme", "isMasked": False}, {"text": "Parankimde sınırları belirgin sıvı koleksiyonu", "isMasked": False}, {"text": "Abse tanısının kesinleştirilmesi", "isMasked": True, "hint": "püy odağının radyolojik kanıtı"}]},
            {"cells": [{"text": "Girişimsel Tedavi", "isMasked": False}, {"text": "Perkütanöz drenaj / Cerrahi drenaj", "isMasked": True, "hint": "kateterle püyün boşaltılması"}, {"text": "Basıncın düşürülmesi ve enfeksiyon odağının tahliyesi"}]}
        ]),
        make_chain("Tedaviye Dirençli Ateş ve Abse Algoritması", [
            "1. İntravenöz Tedavi: Akut pyelonefritli hastaya damardan antibiyotik başlanır.",
            "2. Yanıtsızlık: 3. ve 4. günde hastanın ateşi hala 39°C'de seyreder.",
            "3. Tomografi: Acil BT çekilir ve renal parankimde 5 cm'lik abse görülür.",
            "4. Drenaj: USG veya BT eşliğinde perkütan kateter yerleştirilerek abse boşaltılır."
        ]),
        make_recall("Uygun antibiyotik tedavisine rağmen 3-4. günlerde ateşi düşmeyen pyelonefritli bir hastada akla gelmesi gereken komplikasyon ve yapılması gereken nedir?", "Renal veya perirenal abse (ya da obstrüksiyon) düşünülmeli; USG/BT çekilerek perkütan veya cerrahi drenaj uygulanmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Renal Abse ve Drenaj", [
            {"text": "Renal ve perirenal apse cerrahi ya da perkutanöz drenaj gerektirir.", "isLie": False, "explanation": "Doğru. Püy boşaltılmalıdır."},
            {"text": "Tedavinin 3-4. gününde ateş devam ediyorsa abse veya tıkanıklık araştırılmalıdır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Abse püyü antibiyotiklerle 2 dakikada kendiliğinden gaza dönüşüp havaya uçar.", "isLie": True, "explanation": "Tuzak! Apseler avasküler kapalı kavitedir; antibiyotik penetre olamaz, mutlaka mekanik drenaj gerekir."},
            {"text": "Ultrasonografi ve bilgisayarlı tomografi abse tanısında temel radyolojik yöntemlerdir.", "isLie": False, "explanation": "Doğru. Koleksiyonu gösterirler."}
        ]),
        make_quiz("Akut pyelonefrit tedavisi alan bir hastada tedavinin 3-4. gününde ateşin düşmemesi durumunda en olası komplikasyon ve tedavi hangisidir?", [
            {"key": "A", "text": "Renal/perirenal abse — Cerrahi veya perkutanöz drenaj", "isCorrect": True, "explanation": "Ders notunda tedavinin 3-4. gününde ateş devam ediyorsa abse şüphelenileceği ve abseye cerrahi/perkütan drenaj yapılacağı açıkça belirtilmiştir."},
            {"key": "B", "text": "Diş çürüğü — Diş çekimi", "isCorrect": False, "explanation": "Böbrek enfeksiyonuyla ilgisizdir."},
            {"key": "C", "text": "Basit sistit — İlacın derhal kesilmesi", "isCorrect": False, "explanation": "Tablo pyelonefrit komplikasyonudur."},
            {"key": "D", "text": "Akut apandisit — Appendektomi", "isCorrect": False, "explanation": "Primer patoloji üriner apsedir."}
        ])
    ]
    slides.append(make_slide(47, "Renal ve Perirenal Abse Gelişimi ve Drenaj", "Renal/perirenal abse, 3-4. gün düşmeyen ateş şüphesi ve cerrahi/perkütan drenaj", "Komplike ÜSE", s47_narrative, s47_bullets, s47_elements))

    # Slide 48: Komplike ÜSE'de Tedavi Süresi ve Radyolojik Konsültasyon
    s48_narrative = (
        "Komplike üriner sistem enfeksiyonları, altta yatan yapısal ve fonksiyonel engeller nedeniyle "
        "komplike olmayan sistitteki 3 günlük kısa rejimlerle ASLA tedavi edilemez.\n\n"
        "- **Minimum Tedavi Süresi:** Komplike İYE olgularında antibiyotik tedavi süresi **en az 2 haftadır "
        "(14 gün)**; komplike edici faktörün ağırlığına göre bu süre **4-6 haftaya kadar** uzatılabilir.\n"
        "- **Radyolojik Değerlendirme:** Tüm komplike olgularda üriner sistemde taş, abse, hidroüreter "
        "veya obstrüksiyonu ekarte etmek amacıyla acil **radyolojik görüntüleme (USG veya Kontrastsız BT)** yapılmalıdır.\n"
        "- **Üroloji Konsültasyonu:** Obstrüksiyonun mekanik dekompresyonu (JJ stent, nefrostomi) veya cerrahi "
        "müdahale gerekebileceğinden mutlaka **üroloji konsültasyonu** istenmelidir.\n\n"
        "> [!IMPORTANT]\n"
        "> Komplike ÜSE'de tedavi süresi en az 2 haftadır (4-6 haftaya uzayabilir); medikal tedaviye mutlaka radyolojik inceleme ve ürolojik değerlendirme eşlik eder."
    )
    s48_bullets = [
        "Komplike İYE'de antibiyotik tedavi süresi en az 2 haftadır (14 gün).",
        "Komplike faktöre bağlı olarak tedavi 4-6 haftaya kadar uzatılabilir.",
        "Radyolojik görüntüleme ve üroloji konsültasyonu rutin olarak uygulanmalıdır."
    ]
    s48_elements = [
        make_cloze("Komplike idrar yolu enfeksiyonlarında önerilen antibiyotik tedavi süresi en az 2 haftadır.", "en az 2 haftadır", "Minimum on dört günlük parenteral/oral tedavi süresi"),
        make_table("Komplike ÜSE Yönetim Protokolü", ["Basamak", "Standart Uygulama", "Gerekçe"], [
            {"cells": [{"text": "Tedavi Süresi", "isMasked": False}, {"text": "En az 2 hafta (4-6 haftaya kadar)", "isMasked": True, "hint": "minimum on dört gün"}, {"text": "Biyofilm ve derin doku kolonizasyonunun temizlenmesi"}]},
            {"cells": [{"text": "Görüntüleme", "isMasked": False}, {"text": "Ultrasonografi veya Bilgisayarlı Tomografi", "isMasked": False}, {"text": "Taş, kitle, abse ve hidroüreterin saptanması", "isMasked": True, "hint": "tıkanıklık ve koleksiyonun dışlanması"}]},
            {"cells": [{"text": "Konsültasyon", "isMasked": False}, {"text": "Üroloji konsültasyonu", "isMasked": False}, {"text": "Girişimsel drenaj ve cerrahi planlama", "isMasked": False}]}
        ]),
        make_chain("Komplike ÜSE Tedavi Akış Şeması", [
            "1. Tanı: Erkek, diyabetik veya taşlı hastada ÜSE saptanır.",
            "2. Görüntüleme: USG veya BT ile obstrüksiyon ve abse taranır.",
            "3. Konsültasyon: Üroloji ekibiyle dekompresyon ihtiyacı değerlendirilir.",
            "4. Uzun Süreli Tedavi: En az 14 gün (gerekirse 4-6 hafta) antibiyoterapi verilir."
        ]),
        make_recall("Komplike idrar yolu enfeksiyonlarında antibiyotik tedavi süresi en az kaç haftadır?", "En az 2 haftadır (komplike edici faktörün durumuna göre 4-6 haftaya kadar uzayabilir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komplike ÜSE Tedavisi", [
            {"text": "Komplike İYE tedavisinde süre en az 2 haftadır.", "isLie": False, "explanation": "Doğru. Minimum 14 gündür."},
            {"text": "Faktöre bağlı olarak süre 4-6 haftaya kadar uzatılabilir.", "isLie": False, "explanation": "Doğru. Ağır vakalarda uzatılır."},
            {"text": "Komplike İYE'de hastaya sadece 1 saatlik tek doz hap verilip taburcu edilir.", "isLie": True, "explanation": "Tuzak! Komplike İYE kısa süreli rejimlerle tedavi edilemez; en az 2 hafta tedavi şarttır."},
            {"text": "Radyolojik görüntüleme ve üroloji konsültasyonu yapılmalıdır.", "isLie": False, "explanation": "Doğru. Odak araştırması esastır."}
        ]),
        make_quiz("Komplike üriner sistem enfeksiyonu tanısı alan bir hastada antibiyotik tedavi süresi kural olarak en az ne kadar olmalıdır?", [
            {"key": "A", "text": "En az 2 hafta (komplike edici faktöre bağlı 4-6 hafta)", "isCorrect": True, "explanation": "Ders notunda komplike İYE için 'tedavi süresi en az 2 haftadır (komplike edici faktöre bağlı 4-6 hafta)' kuralı yer almaktadır."},
            {"key": "B", "text": "Sadece 12 saat", "isCorrect": False, "explanation": "Yetersizdir."},
            {"key": "C", "text": "Tam 10 yıl kesintisiz", "isCorrect": False, "explanation": "Gereksiz aşırı süredir."},
            {"key": "D", "text": "3 gün", "isCorrect": False, "explanation": "3 gün komplike olmayan sistit süresidir."},
        ])
    ]
    slides.append(make_slide(48, "Komplike ÜSE'de Tedavi Süresi ve Radyolojik Konsültasyon", "En az 2 hafta (4-6 hafta) tedavi, USG/BT görüntüleme ve üroloji konsültasyonu", "Komplike ÜSE", s48_narrative, s48_bullets, s48_elements))

    # Slide 49: Beşinci Bölüm Özeti: Komplike ÜSE ve Ayırıcı Kriterler
    s49_narrative = (
        "Komplike üriner sistem enfeksiyonları, altta yatan sistemik direnç kaybı veya anatomik-fonksiyonel "
        "engeller nedeniyle morbiditesi yüksek ve cerrahi disiplin gerektiren süreçlerdir.\n\n"
        "- **Kardinal Sınav Kuralı:** Ateş yüksekliği komplike edici bir faktör DEĞİL, enfeksiyonun sistemik "
        "klinik bulgusudur; erkek cinsiyet, gebelik, kontrolsüz DM, taş ve VUR ise gerçek komplike faktörlerdir.\n"
        "- **Ağır Tablolar:** Diyabetiklerde gaz oluşumuyla giden amfizematöz pyelonefritte **nefrektomi**; "
        "3-4. günde düşmeyen ateşte renal/perirenal absede ise **perkütan/cerrahi drenaj** uygulanır.\n"
        "- **Tedavi İlkesi:** Kısa süreli rejimler kontrendikedir; tedavi süresi **en az 2 haftadır (4-6 hafta)** "
        "ve radyolojik görüntüleme ile üroloji konsültasyonu zorunludur.\n\n"
        "> [!IMPORTANT]\n"
        "> Komplike ÜSE'de antibiyotik kadar altta yatan obstrüksiyonun drenajı ve anatomik odağın cerrahi çözümü hayati önem taşır."
    )
    s49_bullets = [
        "Ateş bir klinik bulgudur; komplike edici faktör DEĞİLDİR.",
        "Amfizematöz pyelonefritte nefrektomi; renal absede drenaj uygulanır.",
        "Komplike ÜSE tedavisi en az 2 haftadır; radyoloji ve üroloji şarttır."
    ]
    s49_elements = [
        make_cloze("Amfizematöz pyelonefritte cerrahi nefrektomi uygulanırken renal abse olgularında drenaj esastır.", "nefrektomi", "Böbreğin operasyonla çıkarılması"),
        make_table("Komplike ÜSE Cerrahi ve Süre Özeti", ["Durum / Patoloji", "Temel Kriter / Süre", "Tıbbi / Cerrahi Karar"], [
            {"cells": [{"text": "Ateşin Sınıflamadaki Rolü", "isMasked": False}, {"text": "Enfeksiyonun klinik bulgusudur", "isMasked": True, "hint": "komplike edici faktör olmaması"}, {"text": "Komplike edici faktör olarak kabul edilmez"}]},
            {"cells": [{"text": "Amfizematöz Pyelonefrit", "isMasked": False}, {"text": "Diyabetiklerde gazlı doku nekrozu", "isMasked": False}, {"text": "Acil cerrahi nefrektomi", "isMasked": True, "hint": "böbreğin acil alınması"}]},
            {"cells": [{"text": "Komplike İYE Tedavisi", "isMasked": False}, {"text": "En az 2 hafta (4-6 hafta)", "isMasked": True, "hint": "minimum tedavi periyodu"}, {"text": "Radyoloji ve üroloji konsültasyonu"}]}
        ]),
        make_recall("Amfizematöz pyelonefrit ile renal perirenal abse tablolarının temel cerrahi girişim farkı nedir?", "Amfizematöz pyelonefritte nefrektomi uygulanırken, renal/perirenal absede perkütan veya cerrahi drenaj uygulanır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komplike ÜSE Özeti", [
            {"text": "Ateş yüksekliği komplike edici faktör değil, klinik bir bulgudur.", "isLie": False, "explanation": "Doğru. Klasik sınav sorusu kuralıdır."},
            {"text": "Amfizematöz pyelonefrit için cerrahi nefrektomi uygulanır.", "isLie": False, "explanation": "Doğru. Fulminan seyirlidir."},
            {"text": "Renal ve perirenal apselerde cerrahi veya perkütanöz drenaj yapılır.", "isLie": False, "explanation": "Doğru. Püy boşaltılmalıdır."},
            {"text": "Komplike ÜSE tedavisinde 1 günlük antibiyotik tamamen yeterlidir ve radyoloji yasaktır.", "isLie": True, "explanation": "Tuzak! Komplike ÜSE tedavisi en az 2 hafta sürer ve radyolojik görüntüleme zorunludur."}
        ]),
        make_quiz("Aşağıdakilerden hangisi komplike üriner sistem enfeksiyonları ile ilgili DOĞRU bir ilkedir?", [
            {"key": "A", "text": "Tedavi süresi en az 2 haftadır (komplike faktöre bağlı 4-6 hafta)", "isCorrect": True, "explanation": "Ders notunda belirtilen standart süredir."},
            {"key": "B", "text": "Ateş yüksekliği en önemli komplike edici faktördür", "isCorrect": False, "explanation": "Ateş komplike edici faktör değil klinik bulgudur."},
            {"key": "C", "text": "Amfizematöz pyelonefritte nefrektomi kesinlikle kontrendikedir", "isCorrect": False, "explanation": "Aksine definitif tedavi nefrektomidir."},
            {"key": "D", "text": "Erkeklerdeki ÜSE'ler her zaman komplike olmayan basit sistittir", "isCorrect": False, "explanation": "Erkekteki ÜSE aksi kanıtlanana kadar komplikedir."}
        ])
    ]
    slides.append(make_slide(49, "Beşinci Bölüm Özeti: Komplike ÜSE ve Ayırıcı Kriterler", "Ateşin klinik bulgu olması, amfizematöz nefrektomi, abse drenajı ve süre", "Konsolidasyon", s49_narrative, s49_bullets, s49_elements))

    # Slide 50: [TEKRAR SAYFASI - CHECKPOINT 5] Komplike ÜSE ve Ateşin Rolü
    s50_narrative = (
        "Bu tekrar sayfasında 5. Bölümde işlenen komplike ÜSE dinamiklerini, ateşin tanısal yerini, "
        "sistemik/fonksiyonel/yapısal faktörleri ve cerrahi kararları konsolide ediyoruz.\n\n"
        "- **Büyük Sınav Tuzağı:** Ateş yüksekliği bir komplikasyon faktörü DEĞİL, enfeksiyonun sistemik "
        "**klinik bulgusudur**! Komplike edici faktörler ise erkek cinsiyet, gebelik, kontrolsüz DM, taş, "
        "VUR ve kateter gibi anatomik/fizyolojik zeminlerdir.\n"
        "- **Cerrahi Kararlar:** Diyabetiklerde mortal seyreden amfizematöz pyelonefritte **nefrektomi**; "
        "3-4. günde düşmeyen ateşte renal/perirenal absede **cerrahi/perkütan drenaj** uygulanır.\n"
        "- **Tedavi Prensibi:** Komplike olgularda tedavi süresi **en az 2 haftadır (4-6 hafta)**; "
        "radyolojik görüntüleme ve üroloji konsültasyonu ayrılmaz parçadır.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] 1) Ateş = Klinik bulgu! 2) Erkek/DM/Gebe/Taş = Komplike faktör! 3) Amfizematöz = Nefrektomi! 4) Abse = Drenaj! 5) Süre = En az 2 hafta!"
    )
    s50_bullets = [
        "Ateş bir klinik bulgudur; komplike faktör DEĞİLDİR (Kurul 1 çıkmış sorusu).",
        "Amfizematöz pyelonefrit nefrektomi; renal/perirenal abse drenaj gerektirir.",
        "Komplike ÜSE antibiyotik tedavi süresi en az 2 haftadır (4-6 haftaya uzayabilir)."
    ]
    s50_elements = [
        make_cloze("Dersin en önemli çıkmış sorusu: Ateş yüksekliği komplike edici bir faktör değil, enfeksiyonun klinik bir bulgusudur.", "klinik bir bulgusudur", "Hastalığın seyrini yansıtan fiziksel işaret"),
        make_table("5. Bölüm Büyük Tekrar Tablosu", ["Kavram", "Doğru Tıbbi Kabul", "Tuzak ve Kritik Hata"], [
            {"cells": [{"text": "Ateş Yüksekliği", "isMasked": False}, {"text": "Enfeksiyonun KLİNİK BULGUSUDUR", "isMasked": True, "hint": "hastanın vücut ısısı yanıtı"}, {"text": "Tuzak: Komplike edici faktör olarak işaretlemek"}]},
            {"cells": [{"text": "Amfizematöz Pyelonefrit", "isMasked": False}, {"text": "Cerrahi nefrektomi endikasyonudur", "isMasked": True, "hint": "organın tamamen çıkarılması"}, {"text": "Tuzak: Sadece oral antibiyotikle izlemek"}]},
            {"cells": [{"text": "Renal / Perirenal Abse", "isMasked": False}, {"text": "Cerrahi / perkütanöz drenaj şarttır", "isMasked": False}, {"text": "Tuzak: 3-4. gün düşmeyen ateşi göz ardı etmek", "isMasked": True, "hint": "abseyi atlamak"}]},
            {"cells": [{"text": "Komplike İYE Süresi", "isMasked": False}, {"text": "En az 2 hafta (4-6 hafta)", "isMasked": False}, {"text": "Tuzak: 3 günlük sistit rejimi vermek", "isMasked": False}]}
        ]),
        make_chain("5. Bölüm Klinik Yönetim Zinciri", [
            "1. Ayırıcı Tanı: Ateşin klinik bulgu olduğu, taş/DM/gebelik/erkekliğin komplike faktör olduğu belirlenir.",
            "2. Görüntüleme: Komplike hastaya derhal USG veya BT yapılır.",
            "3. Amfizem Tespiti: Gaz saptanırsa acil nefrektomi organize edilir.",
            "4. Abse Tespiti: Koleksiyon varsa perkütan drenaj takılır ve 14+ gün antibiyotik verilir."
        ]),
        make_recall("Çıkmış sınav sorusunun kesin yanıtı: Aşağıdakilerden hangisi ÜSE için komplike edici faktörlerden değildir?", "Ateş yüksekliği olmasıdır (çünkü ateş komplike edici faktör değil, klinik bulgudur)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 5. Bölüm Konsolidasyonu", [
            {"text": "Ateş yüksekliği ÜSE için komplike edici faktör değil, klinik bir bulgudur.", "isLie": False, "explanation": "Doğru. Kesin sınav kuralıdır."},
            {"text": "Erkek cinsiyet, nefrolitiazis ve kontrolsüz DM komplike edici faktörlerdir.", "isLie": False, "explanation": "Doğru. Gerçek komplike faktörlerdir."},
            {"text": "Amfizematöz pyelonefritte böbreğe dokunulmaz, hasta sadece sıcak su torbasıyla bekletilir.", "isLie": True, "explanation": "Tuzak! Amfizematöz pyelonefrit mortalitesi çok yüksek fulminan bir tablodur ve nefrektomi gerektirir."},
            {"text": "Renal ve perirenal apselerde temel tedavi cerrahi ya da perkütanöz drenajdır.", "isLie": False, "explanation": "Doğru. Drenaj şarttır."}
        ]),
        make_quiz("5. Bölümün temel kazanımlarına göre aşağıdaki ifadelerden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Ateş yüksekliği ÜSE'de en sık görülen yapısal komplike edici faktördür", "isCorrect": True, "explanation": "Kesinlikle yanlış! Ateş bir komplike edici faktör DEĞİLDİR, enfeksiyonun sistemik klinik bir bulgusudur (Kurul 1 çıkmış sorusu)."},
            {"key": "B", "text": "Amfizematöz pyelonefrit diyabetiklerde görülür ve nefrektomi uygulanır", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Renal ve perirenal apseler cerrahi veya perkütan drenaj gerektirir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Komplike İYE olgularında antibiyotik tedavi süresi en az 2 haftadır", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(50, "[TEKRAR SAYFASI - CHECKPOINT 5] Komplike ÜSE ve Ateşin Rolü", "5. Bölümün kapsamlı pekiştirmesi: komplike kriterler, ateşin bulgu olması, nefrektomi ve abse drenajı", "Bölüm Tekrarı", s50_narrative, s50_bullets, s50_elements))

    return slides
