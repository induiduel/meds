# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-14-s81",
        "title": "Temel Üreme Sayısı (R0) ve Efektif Üreme Sayısı (Rt)",
        "content": "Salgın matematiğinin ve aşılama hedeflerinin merkezinde üreme sayıları yer alır:\n\n- **Temel Üreme Sayısı (R0 - Sınav Spotu):** Tamamen duyarlı (bağışık olmayan) bir toplumda, enfekte tek bir vakanın bulaştırıcılık süresi boyunca doğrudan enfekte ettiği ortalama ikincil vaka sayısıdır.\n  - Biyolojik ve çevresel bir sabittir (Kızamık için 12-18, Çiçek için 5-7, İnfluenza için 1.3-1.8).\n- **Efektif Üreme Sayısı (Rt / Re):** Toplumda aşılananlar, hastalığı geçirip bağışıklık kazananlar ve alınan tedbirler (maske, mesafe) devreye girdikten sonra **herhangi bir t anındaki gerçek bulaş hızıdır**.\n- **Kritik Eşik:**\n  - **Rt > 1:** Salgın katlanarak büyür (eksponansiyel yayılım).\n  - **Rt = 1:** Salgın sabit/endemik seyreder.\n  - **Rt < 1:** Salgın sönmeye başlar ve yok olur. Aşılama ve müdahalelerin nihai hedefi Rt değerini hızla 1'in altına indirmektir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "R0 (Teorik Potansiyel) vs Rt (Gerçek Zamanlı Durum)",
                "R0 (Doğal Bulaş Gücü)",
                "Patojenin hiçbir tedbir ve bağışıklık olmayan bakir toplumdaki saf yayılma potansiyelidir (Kızamık: 12-18).",
                "Rt (Müdahaleler Sonrası Bulaş)",
                "Aşı, karantina ve maske sonrası bir vakanın enfekte ettiği anlık kişi sayısıdır; 1'in altına inerse salgın biter."
            ),
            make_cloze(
                "Bir salgının sönümlenmesi ve kontrol altına alınabilmesi için efektif üreme sayısının birin altına düşürülmesi şarttır.",
                "birin",
                "Rt katsayısının inmesi gereken kritik eşik değer"
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-14-s82",
        "title": "Sürü Bağışıklığı Eşiği (Herd Immunity Threshold) ve Korunma Mekanizması",
        "content": "Aşılar sadece aşılanan bireyi değil, tüm toplumu koruyan biyolojik bir kalkan oluşturur:\n\n- **Sürü Bağışıklığı Eşiği (HIT):** Bir toplumda salgının kendiliğinden yayılmasını durdurmak için bağışık olması gereken minimum nüfus oranıdır.\n- **Matematiksel Formül (Sınav Spotu):** $$H = 1 - \\frac{1}{R_0}$$\n  - R0 ne kadar yüksekse, gereken aşı kapsayıcılığı o kadar yüksek olur!\n  - Örneğin R0 = 2 olan bir hastalıkta: $1 - 1/2 = 0.50$ (%50 bağışıklık yeterlidir).\n  - Ancak kızamık gibi R0 = 18 olan bir virüste: $1 - 1/18 \\approx 0.944$ (**en az %95 bağışıklık şarttır!**)\n- **Dolaylı Koruma:** Kanser tedavisi gören çocuklar, organ nakilliler veya aşı yapılamayan yenidoğan bebekler, etraflarındaki herkes aşılandığı için virüsle karşılaşmaz ve korunmuş olurlar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Hastalık", "R0 Değeri", "Sürü Bağışıklığı Eşiği (HIT)", "Aşılama Hedefi"],
                [
                    ["Kızamık", "12 – 18", "%92 – %95", "%95 üzerinde iki doz aşı"],
                    ["Boğmaca (Pertussis)", "12 – 17", "%92 – %94", "DTP ile %90 üzeri"],
                    ["Çocuk Felci (Polio)", "5 – 7", "%80 – %86", "OPV/IPV ile %85 üzeri"],
                    ["Kabakulak", "4 – 7", "%75 – %86", "KKK ile %85 üzeri"],
                    ["Mevsimsel Grip", "1.3 – 1.6", "%30 – %40", "Yıllık risk grubu aşılaması"]
                ]
            ),
            make_quiz(
                "Temel üreme sayısı (R0) 5 olan bir patojenin toplumda salgın yapmasını engellemek için teorik olarak nüfusun en az yüzde kaçının bağışık olması gerekir?",
                [
                    {"key": "A", "text": "%50", "isCorrect": False, "explanation": "%50, R0=2 için yeterlidir."},
                    {"key": "B", "text": "%80", "isCorrect": True, "explanation": "Doğru cevap B'dir: H = 1 - 1/R0 formülü uygulandığında; 1 - 1/5 = 4/5 = %80 olarak hesaplanır."},
                    {"key": "C", "text": "%95", "isCorrect": False, "explanation": "%95, R0=18 civarında olan kızamık için gerekir."},
                    {"key": "D", "text": "%20", "isCorrect": False, "explanation": "%20 hiçbir salgında sürü bağışıklığı sağlayamaz."}
                ]
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-14-s83",
        "title": "Salgında Aşılama Stratejileri: Kitlesel vs Halka Aşılama (Ring Vaccination)",
        "content": "Salgın anında aşı stoğu, zaman ve insan gücü sınırlı olduğunda iki farklı stratejik model uygulanır:\n\n- **1. Kitlesel Aşılama (Mass Vaccination):**\n  - Tüm ülkedeki veya şehirdeki hedef yaş grubunun tamamını aynı anda aşılamayı hedefler.\n  - Çok yüksek kaynak, milyonlarca doz aşı ve devasa lojistik gerektirir; rutin ulusal aşı takvimlerinde ve büyük pandemilerde uygulanır.\n- **2. Halka Aşılama (Ring Vaccination - Sınav Spotu):**\n  - Bir vaka tespit edildiğinde, hastanın etrafında konsantrik bir 'koruma halkası' oluşturulur.\n  - Hastanın birinci derece tüm temaslıları (aile, iş arkadaşları) ve onların da temaslıları (ikinci halka) hızla aşılanır.\n  - Patojenin yayılacağı tüm duyarlı konaklar kalkan altına alınarak virüs hapsedilir.\n- **Avantajı:** Çok daha az aşı dozuyla ve az personelle salgını odakta boğmayı sağlar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Kitlesel Aşılama vs Halka Aşılama (Ring Vaccination)",
                "Kitlesel Aşılama (Geniş Tabanlı)",
                "Tüm kenti veya ülkeyi aşılar; yüksek aşı stoku ve aylar süren lojistik gerektirir.",
                "Halka Aşılama (Nokta Atışı Hedefli)",
                "Vakanın temaslılarını ve onların temaslılarını hızla aşılayarak virüsün etrafına biyolojik duvar örer."
            ),
            make_cloze(
                "Salgınlarda vakanın doğrudan ve dolaylı temaslılarını aşılayarak bulaşı odakta sınırlandırma stratejisine halka aşılama denir.",
                "halka",
                "Ring vaccination teriminin Türkçe karşılığı"
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-14-s84",
        "title": "Çiçek Hastalığının Eradikasyonunda Halka Aşılamanın Rolü",
        "content": "Tıp tarihinin en büyük zaferi olan çiçek hastalığının yok edilmesinde anahtar strateji halka aşılama olmuştur:\n\n- **Tarihi Kriz:** 1960'larda DSÖ dünya çapında tüm insanları aşılayarak çiçeği bitirmeye çalışmış, ancak Hindistan ve Afrika'da devasa nüfuslar nedeniyle kitlesel aşılama başarısız olmuştur.\n- **Strateji Değişikliği (Surveillance-Containment):**\n  - DSÖ, tüm dünyayı aşılamak yerine 'Gözetim ve Sınırlama' stratejisine geçti.\n  - Her bir çiçek vakası ödül karşılığı ihbar ettirildi.\n  - Vakanın bulunduğu köyün etrafına derhal filyasyon ekipleri sevk edildi ve vakanın temas ettiği herkes (halka aşılama) aşılandı.\n- **Tarihi Sonuç:** Virüs gidecek başka duyarlı insan bulamadı ve zincir kırıldı; 1977'de Somali'deki son doğal vakadan sonra çiçek yeryüzünden silindi.\n- **Modern Uygulama:** Günümüzde Ebola ve Maymun Çiçeği (Mpox) salgınlarında da halka aşılama en kritik araçtır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Çiçek Hastalığını Bitiren Halka Aşılama Döngüsü",
                [
                    "1. Hızlı Vaka Bildirimi: Köydeki döküntülü şüpheli hasta sürveyans ağına bildirilir.",
                    "2. Filyasyon ve Temas Haritası: Hastanın son 14 günde temas ettiği tüm komşu ve akrabalar listelenir.",
                    "3. Birinci Halka Aşılaması: Hastanın doğrudan temaslıları ilk 4 gün içinde aşılanır.",
                    "4. İkinci Halka Aşılaması: Birinci halkanın temas edebileceği çevre haneler de aşılanır.",
                    "5. Biyolojik Karantina: Virüsün çevreye sıçraması engellenir ve salgın odağı söndürülür."
                ]
            ),
            make_quiz(
                "Dünya Sağlık Örgütü'nün çiçek hastalığını küresel olarak eradike etmesinde kitlesel aşılamadan daha etkili olan temel strateji hangisidir?",
                [
                    {"key": "A", "text": "Halka aşılama ve temaslı sınırlaması (Surveillance-containment)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Çiçeğin sonunu getiren hamle, vakaların hızla tespit edilip etrafındaki temaslıların halka aşılama ile korunmasıdır."},
                    {"key": "B", "text": "Tüm dünyadaki hastaneleri kapatıp hastaları evde bırakmak", "isCorrect": False, "explanation": "Bu salgını bitirmez, ölümleri artırır."},
                    {"key": "C", "text": "Antibiyotik üretimine ağırlık vermek", "isCorrect": False, "explanation": "Çiçek viraldir, antibiyotik virüse etki etmez."},
                    {"key": "D", "text": "Sadece 65 yaş üstü kişileri aşılamak", "isCorrect": False, "explanation": "Çiçek tüm yaş gruplarını vuran bir hastalıktır."}
                ]
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-14-s85",
        "title": "Aşı Teknolojileri ve Salgın Yanıtındaki Rolleri",
        "content": "Farklı aşı platformları salgın durumlarında hız, güvenlik ve etkinlik açısından farklı üstünlüklere sahiptir:\n\n- **1. Canlı Attenüe Aşılar (KKK, Suçiçeği, Sarı Humma, OPV):**\n  - Güçlü, uzun ömürlü hücresel ve humoral bağışıklık sağlar; genellikle tek veya iki doz yeterlidir.\n  - Kısıtlılık: İmmün yetmezliği olanlara ve gebelere uygulanamaz; soğuk zincire çok hassastır.\n- **2. İnaktif Aşılar (Hepatit A, Kuduz, IPV):**\n  - Patojen öldürülmüştür; güvenlidir, immün yetmezliği olanlara yapılabilir.\n  - Kısıtlılık: Daha zayıf bağışıklık oluşturur, rapel (pekiştirme) dozları gerektirir.\n- **3. mRNA Aşıları (COVID-19 - BNT162b2, mRNA-1273):**\n  - **Salgın Avantajı (Sınav Spotu):** Genom sekansı belirlendikten sonra **haftalar içinde** laboratuvarda tasarlanıp üretilebilir; salgın hızına yetişen en esnek platformdur.\n  - Kısıtlılık: Ultra-soğuk zincir (-70°C) gereksinimi.\n- **4. Rekombinant ve Protein Subunit Aşılar (Hepatit B, HPV):**\n  - Yüksek güvenlik profili ve standart buzdolabı (+2°C ila +8°C) uyumu.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Aşı Türü", "Örnekler", "Salgındaki Temel Avantajı", "Lojistik/Klinik Zorluğu"],
                [
                    ["Canlı Attenüe", "KKK, Sarı Humma, Suçiçeği", "Hızlı ve ömür boyu güçlü bağışıklık", "Gebelere ve immün yetmezliğe yapılamaz"],
                    ["İnaktif", "Hepatit A, Kuduz, CoronaVac", "Çok yüksek güvenlik profili", "Çoklu doz ve adjuvan gereksinimi"],
                    ["mRNA", "COVID-19 Comirnaty/Spikevax", "En hızlı tasarlanan ve üretilen platform", "Ultra-soğuk zincir (-70°C) gereksinimi"],
                    ["Viral Vektör", "Ebola rVSV, AstraZeneca", "Güçlü T-hücre yanıtı tetikleme", "Vektöre karşı önceden var olan antikor riski"]
                ]
            ),
            make_cloze(
                "Yeni ortaya çıkan patojenlerde genom dizisi çıktıktan sonra haftalar içinde hızla tasarlanabilen aşı platformu mRNA aşılarıdır.",
                "mRNA",
                "Hızlı sentezlenen nükleik asit aşı türü"
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-14-s86",
        "title": "Soğuk Zincir Yönetimi (Cold Chain): Biyolojik Güvenliğin Temeli",
        "content": "Bir aşı fabrikada ne kadar mükemmel üretilirse üretilsin, hedef kola ulaşana kadar soğuk zincir bozulursa suya dönüşür:\n\n- **Soğuk Zincir Tanımı (Sınav Spotu):** Bir aşının üretim aşamasından kişiye uygulanma anına kadar etkinliğini ve biyolojik gücünü kaybetmemesi için gereken **kesintisiz sıcaklık kontrolü sistemidir**.\n- **Standart Sıcaklık Aralığı:** Çoğu rutin aşı (KKK, DaBT, Hepatit B) **+2°C ile +8°C arasında** saklanmalı ve taşınmalıdır. Asla dondurulmamalı veya ısıya maruz bırakılmamalıdır.\n- **Ultra-Soğuk Zincir:** Bazı yeni nesil mRNA aşıları **-70°C ile -80°C** derin dondurucu ve kuru buz lojistiği gerektirir.\n- **İzleme Araçları:** Aşı flakon izleyicileri (VVM - Vaccine Vial Monitor), dijital sıcaklık kayıt cihazları (data logger).\n- **Soğuk Zincir Kırılırsa:** Aşı denatüre olur, antijenik yapısını kaybeder; hastaya uygulandığında bağışıklık sağlamaz ve sahte bir güven duygusu yaratır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Standart Soğuk Zincir (+2°C / +8°C) vs Ultra-Soğuk Zincir (-70°C)",
                "Standart Soğuk Zincir (+2°C ila +8°C)",
                "Rutin aşı buzdolapları, aşı nakil kapları ve buz aküleriyle köylere kadar kolayca ulaştırılır.",
                "Ultra-Soğuk Zincir (-70°C ila -80°C)",
                "Kuru buz ve özel ultra dondurucular gerektirir; elektrik kesintisi olan kırsal bölgelerde lojistiği zordur."
            ),
            make_quiz(
                "Rutin çocukluk çağı aşılarının büyük çoğunluğunun bozulmadan saklanması ve taşınması gereken standart sıcaklık aralığı hangisidir?",
                [
                    {"key": "A", "text": "-20°C ile -40°C arası", "isCorrect": False, "explanation": "Bu dondurucu sıcaklığıdır; inaktif aşılar donarsa çöker ve bozulur."},
                    {"key": "B", "text": "+2°C ile +8°C arası", "isCorrect": True, "explanation": "Doğru cevap B'dir: Standart rutin aşı soğuk zincir aralığı +2°C ile +8°C arasındadır."},
                    {"key": "C", "text": "+15°C ile +25°C arası (oda sıcaklığı)", "isCorrect": False, "explanation": "Oda sıcaklığında aşı proteinleri günler içinde denatüre olur."},
                    {"key": "D", "text": "+37°C vücut sıcaklığı", "isCorrect": False, "explanation": "Bu sıcaklıkta aşılar saatler içinde inaktive olur."}
                ]
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-14-s87",
        "title": "Aşı Tereddüdü, Aşı Reddi ve Toplumsal Bağışıklık Duvarının Çökmesi",
        "content": "DSÖ tarafından küresel sağlığı tehdit eden 10 temel tehlikeden biri olarak tanımlanan olgu biyolojik değil psikolojiktir: **Aşı Tereddüdü (Vaccine Hesitancy)**:\n\n- **Aşı Karşıtlığının Anatomisi:** Aşıların güvenliğine, yan etkilerine veya arkasındaki ilaç firmalarına/devlete duyulan şüphe sonucu aşı yaptırmakta tereddüt etme veya tamamen reddetme durumudur.\n- **Eşik Değerin Altına Düşüş:** Bir toplumda aşılama oranı sürü bağışıklığı eşiğinin (örneğin kızamık için %95) altına düştüğünde, patojen duyarlı cepler (clusters) bularak yeniden epidemilere yol açar.\n- **Son Yıllardaki Kızamık Patlamaları:** Avrupa ve Amerika'da aşı reddi nedeniyle binlerce çocukta yeniden kızamık salgınları ve buna bağlı subakut sklerozan panensefalit (SSPE) vakaları görülmüştür.\n- **Çözüm:** Aşıyı zorunlu kılmaktan ziyade, aile hekimlerinin birebir şefkatli iletişimi ve bilimsel şeffaflıktır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Halk Sağlığı Stratejisi: Aşı Tereddüdünün Yükseldiği Bir İlçe",
                "Bir ilçede zengin ve eğitim düzeyi yüksek ailelerin yaşadığı sitelerde KKK aşısı yaptırma oranı %96'dan %82'ye geriledi. İlçe Sağlık Müdürü olarak ne yaparsınız?",
                [
                    {
                        "text": "Aşı yaptırmayan tüm aileleri televizyonda afişe edip para cezası kesmek",
                        "outcome": "Ters teper: Aileler davalar açar, mağduriyet algısı yaratılır ve yeraltı aşı karşıtı grupları güçlenir.",
                        "isCorrect": False
                    },
                    {
                        "text": "İlçedeki çocuk hekimleri ve pedagoglarla birlikte sitelerde interaktif seminerler düzenlemek, aşı güvenliği verilerini şeffafça paylaşmak ve endişeli anneleri dinlemek",
                        "outcome": "En başarılı halk sağlığı iletişimi: Bilgi kirliliği temizlenir, güven tazelenir ve aşılama oranı tekrar %95'in üzerine çıkar.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Nasılsa toplumun geri kalanı aşılı' diyerek durumu görmezden gelmek",
                        "outcome": "Epidemiyolojik felaket: O sitelerdeki okullarda 6 ay içinde kızamık salgını patlar.",
                        "isCorrect": False
                    }
                ]
            ),
            make_cloze(
                "Toplumda aşılama oranının sürü bağışıklığı eşiğinin altına inmesi kızamık gibi virüslerin yeniden salgın yapmasına zemin hazırlar.",
                "bağışıklığı",
                "Toplumu kolektif olarak koruyan bağışıklık türü"
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-14-s88",
        "title": "Küresel Aşı Eşitliği ve COVAX: 'Kimse Güvende Değilse Hiç Kimse Güvende Değildir'",
        "content": "Pandemiler sınır tanımaz; zengin ülkelerin tüm nüfusunu aşılaması küresel salgını tek başına sonlandıramaz:\n\n- **Aşı Milliyetçiliği Tehdidi:** Zengin ülkelerin aşı stoklarını kapatıp ihtiyaçlarının katbekat fazlasını depolaması, yoksul ülkelerdeki sağlık çalışanlarının dahi aşısız kalmasına yol açmıştır.\n- **Yeni Varyant Fabrikası:** Afrika veya Asya'da aşıya erişemeyen milyarlarca insan enfekte oldukça, virüs kontrolsüzce çoğalır ve aşıdan kaçan yeni mutant varyantlar (Delta, Omicron) türetir. Bu varyantlar eninde sonunda dönüp zengin ülkeleri de vurur!\n- **COVAX Girişimi (DSÖ):** Dünyadaki her ülkenin, ekonomik gücüne bakılmaksızın aşıya eşit erişimini sağlamak için kurulan küresel aşı paylaşım platformudur.\n- **Halk Sağlığının Küresel Kuralı:** Bir salgında yeryüzündeki son insan güvende olana kadar, hiç kimse tamamen güvende değildir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Aşı Milliyetçiliği vs Küresel Aşı Eşitliği (COVAX)",
                "Aşı Milliyetçiliği (Kısa Vadeli Bencillik)",
                "Zengin ülkeler aşıyı depolar; aşısız bölgelerde yeni ölümcül varyantlar ürer ve aşıların etkinliğini kırar.",
                "Küresel Aşı Eşitliği (Sürdürülebilir Güvenlik)",
                "Dünyadaki tüm risk grupları ve sağlıkçılar eş zamanlı aşılanır; varyant üretimi durdurularak pandemi sonlandırılır."
            ),
            make_recall(
                "Aşı dağıtımındaki küresel adaletsizlik neden aşılanmış gelişmiş ülkeleri de doğrudan tehdit eder?",
                "Çünkü aşısız yoksul nüfuslarda virüs serbestçe replike olarak aşı antikorlarından kaçabilen yeni mutant varyantlar geliştirir ve tüm dünyaya yayılır."
            )
        ]
    })

    # Slide 89 - CHECKPOINT 9
    slides.append({
        "id": "k1-14-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Aşılar, İmmünizasyon Programları ve Salgın Kontrolü",
        "content": "Bu checkpointte salgın matematiğini, aşı stratejilerini ve soğuk zincir lojistiğini özetliyoruz:\n\n- **R0 ve Rt:** R0 doğal bulaş potansiyelidir; Rt müdahalelerle 1'in altına indirilmelidir.\n- **Sürü Bağışıklığı Eşiği:** $H = 1 - 1/R_0$; kızamık gibi yüksek R0 patojenlerde en az %95 aşılama gerekir.\n- **Halka Aşılama (Ring Vaccination):** Vakanın etrafındaki doğrudan ve dolaylı temaslıların aşılanması; çiçek hastalığını tarihten silen anahtar stratejidir.\n- **Aşı Teknolojileri:** mRNA aşıları salgında en hızlı tasarlanan ve üretilen platformdur.\n- **Soğuk Zincir:** Standart aşılar için **+2°C ile +8°C**; soğuk zincir bozulursa aşı inaktive olur ve bağışıklık bırakmaz.\n- **Aşı Tereddüdü:** Güven kaybı sürü bağışıklığını deler.\n- **COVAX ve Eşitlik:** Küresel aşı adaleti sağlanmadan pandemiler sona erdirilemez.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Aşıyla Salgın Kontrolünün 4 Aşaması",
                [
                    "1. Genomik Belirleme ve Hızlı Üretim: Patojenin antijeni saptanır ve aşı haftalar içinde üretilir.",
                    "2. Kusursuz Soğuk Zincir Lojistiği: Aşılar +2°C ile +8°C arasında korunarak sahaya taşınır.",
                    "3. Hedefli ve Halka Aşılama: Odak bölgelerde ve temaslı halkalarında yüksek kapsayıcılık sağlanır.",
                    "4. Sürü Bağışıklığı ve Sönümlenme: Rt katsayısı 1'in altına düşer ve bulaş zinciri kırılır."
                ]
            ),
            make_table(
                ["Parametre", "Standart Değer / Kural", "Salgındaki Önemi"],
                [
                    ["Sürü Bağışıklığı (Kızamık)", "≥ %95 kapsayıcılık", "Duyarlı cepleri kapatarak salgını önleme"],
                    ["Standart Soğuk Zincir", "+2°C ile +8°C", "Antijenik yapıyı ve aşı etkinliğini koruma"],
                    ["Ring Vaccination", "Temaslıları ve çevrelerini aşılama", "Kısıtlı aşı stokuyla vaka odağını boğma"]
                ]
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-14-s90",
        "title": "Mini Vaka: Yatılı Bölge Okulunda Kızamık Salgını ve Halka Aşılama",
        "content": "500 öğrencinin kaldığı bir yatılı bölge ortaokulunda, aşı karnesi eksik olan 11 yaşında bir çocukta yüksek ateş, burun akıntısı, Koplik lekeleri ve yüzden başlayan makülopapüler döküntü görülüyor:\n\n- **Epidemiyolog Teşhisi:** Klinik olarak kızamık tanısı konuyor. Kızamığın R0 değerinin 15 olduğu ve havada asılı aerosollerle hızla yayılacağı biliniyor.\n- **Acil Müdahale Adımları:**\n  1. Hasta çocuk derhal tek kişilik negatif basınçlı/havalandırılan odaya alınıyor.\n  2. Filyasyon ekibi tüm okulun aşı kayıtlarını 2 saat içinde inceliyor; 42 öğrencinin aşısız veya tek doz aşılı olduğu saptanıyor.\n  3. **Halka Aşılama:** İlçe Sağlık Müdürlüğü'nden +2°C / +8°C soğuk zincirle getirilen KKK aşıları, temasın ilk 72 saati içinde bu 42 öğrenciye ve tüm okul personeline uygulanıyor.\n- **Sonuç:** Bulaş odağı halka aşılamayla kapatılıyor; okulda ikinci bir vaka dahi çıkmadan salgın önleniyor.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Klinik Karar: Kızamık Temaslısında Acil Profilaksi",
                "Okulda lösemi tedavisi nedeniyle kemoterapi alan ve canlı aşı yapılması kesinlikle kontrendike olan 12 yaşında bir öğrencinin de kızamıklı çocukla aynı yatakhanede kaldığı anlaşılıyor. Bu çocuğa yaklaşımınız ne olmalıdır?",
                [
                    {
                        "text": "'Aşı takvimi kuralı bozulamaz' diyerek çocuğa canlı KKK aşısı yapmak",
                        "outcome": "Ölümcül hata: İmmün yetmezlikli çocukta canlı aşı virüsü yaygın ensefalit ve ölüme yol açar.",
                        "isCorrect": False
                    },
                    {
                        "text": "Canlı aşı yerine derhal ilk 6 gün içinde Kızamık İmmünglobulini (IVIG) uygulayarak pasif koruma sağlamak",
                        "outcome": "Mükemmel klinik karar: Pasif antikorlar çocuğu kızamıktan korur ve immün yetmezlik riski bertaraf edilir.",
                        "isCorrect": True
                    },
                    {
                        "text": "Çocuğu hiçbir şey yapmadan evine göndermek",
                        "outcome": "Ağır ihmal: Çocuk ölümcül kızamık pnömonisi veya ensefaliti geliştirir.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu okul vakasında filyasyon ekibinin kızamıklı öğrencinin temaslılarını tespit edip ilk 72 saatte aşılaması hangi stratejinin doğrudan örneğidir?",
                [
                    {"key": "A", "text": "Halka aşılama (Ring vaccination)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Vakanın etrafındaki temaslıların hızla aşılanarak bulaşın kesilmesi 'halka aşılama' yöntemidir."},
                    {"key": "B", "text": "Küresel çiçek eradikasyonu", "isCorrect": False, "explanation": "Çiçek zaten eradike edilmiştir."},
                    {"key": "C", "text": "Vektör larvasit mücadelesi", "isCorrect": False, "explanation": "Kızamık sivrisinekle bulaşmaz."},
                    {"key": "D", "text": "Sadece palyatif sedasyon", "isCorrect": False, "explanation": "Konuyla ilgisi yoktur."}
                ]
            )
        ]
    })

    return slides
