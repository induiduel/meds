# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec9():
    slides = []

    # Slide 81: Türkiye E. coli Direnç Verileri: Genel Bakış
    s81_narrative = (
        "Türkiye'de üriner sistem enfeksiyonu etkeni olan Escherichia coli suşlarında antibiyotik "
        "direnci, kontrolsüz antibiyotik kullanımı nedeniyle dünya ortalamasının oldukça üzerindedir.\n\n"
        "- **Ulusal Direnç Tablosu:** Türkiye'de ÜSE'de E. coli suşlarında direnç oranları: **ampisilin "
        "%62-64; amoksisilin/klavulanat %32-37; seftriakson %19-24; TMP/SMZ %23-47; gentamisin %17-18; "
        "siprofloksasin %30-39; nitrofurantoin %5-8** olarak saptanmıştır.\n"
        "- **Klinik Yansıması:** Bu yüksek direnç paternleri ampirik tedavi algoritmalarını doğrudan "
        "etkilemekte, ampisilin ve TMP-SXT gibi klasik ajanların ampirik kullanım alanını daraltmaktadır.\n"
        "- **Veri Temelli Karar:** Hekim, Türkiye verilerini bilerek ampirik reçete yazmalı ve direnç "
        "oranı kabul edilebilir sınırlar içinde kalan ajanları tercih etmelidir.\n\n"
        "> [!NOTE]\n"
        "> Türkiye'de ÜSE'de E. coli direnç oranları: Ampisilin %62-64, TMP/SMZ %23-47, siprofloksasin %30-39, seftriakson %19-24 ve nitrofurantoin %5-8'dir."
    )
    s81_bullets = [
        "Türkiye'de E. coli direnç oranları yüksek seyreder.",
        "Ampisilin %62-64, amoksisilin/klavulanat %32-37, TMP/SMZ %23-47.",
        "Seftriakson %19-24, gentamisin %17-18, siprofloksasin %30-39, nitrofurantoin %5-8."
    ]
    s81_elements = [
        make_cloze("Türkiye'de ÜSE'de E. coli suşlarında siprofloksasin direnç oranı %30-39 düzeyindedir.", "%30-39", "Türkiye'deki siprofloksasin direnç aralığı"),
        make_table("Türkiye'de E. coli Direnç Profili Özeti", ["Antibiyotik", "Direnç Yüzdesi", "Klinik Yorum"], [
            {"cells": [{"text": "Ampisilin", "isMasked": False}, {"text": "%62-64", "isMasked": True, "hint": "en yüksek direnç oranı"}, {"text": "Ampirik olarak kesinlikle kullanılamaz"}]},
            {"cells": [{"text": "Siprofloksasin", "isMasked": False}, {"text": "%30-39", "isMasked": False}, {"text": "Yüksek direnç; ampirik kullanımı kısıtlı", "isMasked": True, "hint": "kinolonların kısıtlanma nedeni"}]},
            {"cells": [{"text": "Nitrofurantoin", "isMasked": False}, {"text": "%5-8", "isMasked": True, "hint": "en düşük direnç oranı"}, {"text": "En güvenilir oral sistit ajanı"}]}
        ]),
        make_chain("Ulusal Direnç Veri Akışı", [
            "1. Sürveyans: Türkiye genelindeki idrar kültürlerinin taranması.",
            "2. E. coli Direnç Analizi: Ampisilinde %60+, florokinolonda %30+ direnç tespiti.",
            "3. En Düşük Direnç: Nitrofurantoinin %5-8 ile lider kalması.",
            "4. Kılavuz Güncellemesi: Ampirik rejimlerin bu verilere göre revize edilmesi."
        ]),
        make_recall("Türkiye'de ÜSE'de E. coli suşlarında siprofloksasin ve seftriakson direnç oranları nedir?", "Siprofloksasin direnci %30-39; seftriakson direnci %19-24'tür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Türkiye Direnç Verileri", [
            {"text": "Türkiye'de E. coli suşlarında ampisilin direnci %62-64'tür.", "isLie": False, "explanation": "Doğru. En yüksek dirençtir."},
            {"text": "Siprofloksasin direnci %30-39 aralığındadır.", "isLie": False, "explanation": "Doğru. Ders notu verisidir."},
            {"text": "Türkiye'de tüm antibiyotiklerin direnç oranı tam olarak %0,0001'dir ve hiçbir direnç yoktur.", "isLie": True, "explanation": "Tuzak! Türkiye'de direnç oranları çok yüksektir (ampisilin %62-64, siprofloksasin %30-39 vb.)."},
            {"text": "Gentamisin direnci %17-18 düzeyindedir.", "isLie": False, "explanation": "Doğru. Ders notu oranıdır."}
        ]),
        make_quiz("Türkiye'de üriner sistem enfeksiyonu etkeni olan E. coli suşlarında 'siprofloksasin' direnç oranı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "%30-39", "isCorrect": True, "explanation": "Ders notundaki Türkiye direnç listesinde 'siprofloksasin %30-39' olarak açıkça verilmiştir."},
            {"key": "B", "text": "%0-1", "isCorrect": False, "explanation": "Direnç bu kadar düşük değildir."},
            {"key": "C", "text": "%99-100", "isCorrect": False, "explanation": "Bu oran tam dirençtir."},
            {"key": "D", "text": "%5-8", "isCorrect": False, "explanation": "%5-8 nitrofurantoinin direncidir."}
        ])
    ]
    slides.append(make_slide(81, "Türkiye E. coli Direnç Verileri: Genel Bakış", "Türkiye'de E. coli suşlarında temel antibiyotik direnç oranları", "Direnç Profili", s81_narrative, s81_bullets, s81_elements))

    # Slide 82: En Düşük ve En Yüksek Direnç: Nitrofurantoin (%5-8) vs Ampisilin (%62-64)
    s82_narrative = (
        "Türkiye direnç tablosunun iki uç noktasını oluşturan antibiyotikler, klinik başarı ve "
        "başarısızlığın sınırlarını net şekilde çizer.\n\n"
        "- **En Düşük Direnç:** Türkiye'de E. coli suşlarında direnç oranı en düşük olan antibiyotik "
        "**nitrofurantoin (%5-8)**dir.\n"
        "- **En Yüksek Direnç:** Direnç oranı en yüksek olan antibiyotik ise **ampisilin (%62-64)**dir.\n"
        "- **Klinik Anlam:** Nitrofurantoinin çoklu etki mekanizmasına sahip olması ve doku penetrasyonu "
        "olmayıp sadece idrarda yoğunlaşması direnç gelişimini baskılamıştır; bu nedenle akut sistitte en güvenilir oral seçenektir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Türkiye'de E. coli'de EN DÜŞÜK direnç: Nitrofurantoin (%5-8); EN YÜKSEK direnç: Ampisilin (%62-64) suşlarında saptanmıştır."
    )
    s82_bullets = [
        "En düşük direnç: Nitrofurantoin (%5-8).",
        "En yüksek direnç: Ampisilin (%62-64).",
        "Nitrofurantoin düşük direnç profili ile sistitte en güvenilir ajanlardan biridir."
    ]
    s82_elements = [
        make_cloze("Türkiye'de E. coli suşlarında en düşük direnç oranı %5-8 ile nitrofurantoin antibiyotiğinde görülür.", "nitrofurantoin", "Türkiye'de en düşük E. coli direncine sahip antibiyotik"),
        make_table("İki Uç Direnç Oranının Karşılaştırması", ["Antibiyotik", "Direnç Oranı", "Klinik Durumu"], [
            {"cells": [{"text": "Nitrofurantoin", "isMasked": False}, {"text": "%5-8 (EN DÜŞÜK)", "isMasked": True, "hint": "en düşük yüzde aralığı"}, {"text": "Sistitte en güvenilir ampirik oral ajan"}]},
            {"cells": [{"text": "Ampisilin", "isMasked": False}, {"text": "%62-64 (EN YÜKSEK)", "isMasked": True, "hint": "en yüksek yüzde aralığı"}, {"text": "Ampirik tedavide kesinlikle yeri yoktur"}]}
        ]),
        make_chain("Direnç Kutupları Mantığı", [
            "1. Ampisilin Tüketimi: Yıllarca aşırı kullanım → %62-64 dirençle listenin dibine çöküş.",
            "2. Nitrofurantoin Yapısı: Çoklu hedefli etki → direnç gelişiminin zorluğu.",
            "3. Güncel Veri: Nitrofurantoinin %5-8 ile zirvedeki duyarlılığı.",
            "4. Klinik Reçete: Sistitte nitrofurantoinin tercih edilmesi."
        ]),
        make_recall("Türkiye'de E. coli suşlarında en düşük ve en yüksek direnç oranına sahip antibiyotikler ve yüzdeleri nedir?", "En düşük direnç nitrofurantoin (%5-8); en yüksek direnç ampisilin (%62-64) suşlarındadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İki Uç Direnç", [
            {"text": "Türkiye'de nitrofurantoin direnci %5-8 olup en düşük oranlardan biridir.", "isLie": False, "explanation": "Doğru. En düşük dirençtir."},
            {"text": "Ampisilin direnci %62-64 olup en yüksek direnç oranlarındandır.", "isLie": False, "explanation": "Doğru. En yüksek dirençtir."},
            {"text": "Türkiye'de E. coli suşlarında nitrofurantoin direnci %100'dür ve ampisilin direnci sıfırdır.", "isLie": True, "explanation": "Tuzak! Tam tersine nitrofurantoin direnci en düşük (%5-8), ampisilin direnci en yüksektir (%62-64)."},
            {"text": "Nitrofurantoin sistitte ilk seçenek ajanlar arasında yer alır.", "isLie": False, "explanation": "Doğru. Düşük direnç nedeniyle etkilidir."}
        ]),
        make_quiz("Türkiye'de üriner sistem enfeksiyonu etkeni E. coli suşlarında direnç oranı EN DÜŞÜK (%5-8) olan antibiyotik aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Nitrofurantoin", "isCorrect": True, "explanation": "Ders notunda açıkça 'nitrofurantoin %5-8' olarak en düşük oranla belirtilmiştir."},
            {"key": "B", "text": "Ampisilin", "isCorrect": False, "explanation": "Ampisilin %62-64 ile en yüksek dirence sahiptir."},
            {"key": "C", "text": "Siprofloksasin", "isCorrect": False, "explanation": "Siprofloksasin direnci %30-39'dur."},
            {"key": "D", "text": "TMP/SMZ", "isCorrect": False, "explanation": "TMP/SMZ direnci %23-47'dir."}
        ])
    ]
    slides.append(make_slide(82, "Direnç Kutupları: Nitrofurantoin vs Ampisilin", "En düşük dirençli nitrofurantoin (%5-8) ve en yüksek dirençli ampisilin (%62-64)", "Direnç Profili", s82_narrative, s82_bullets, s82_elements))

    # Slide 83: Diğer Ajanların Direnç Oranları: Seftriakson, Amoksilav, TMP/SMZ, Gentamisin
    s83_narrative = (
        "Ulusal sürveyans verilerinde yer alan diğer antibiyotiklerin direnç oranları, ampirik parenteral "
        "ve oral tedavilerin planlanmasında klinisyene rehberlik eder.\n\n"
        "- **Geniş Spektrumlu Beta-Laktamlar:** **Amoksisilin/klavulanat direnci %32-37**, üçüncü kuşak "
        "parenteral sefalosporin olan **seftriakson direnci ise %19-24** düzeyindedir.\n"
        "- **Folat ve Aminoglikozid:** **TMP/SMZ direnci %23-47** arasında çok geniş ve yüksek bir "
        "aralık sergilerken, parenteral **gentamisin direnci %17-18** seviyesindedir.\n"
        "- **Klinik Çıkarım:** TMP-SXT direncinin %20'nin üzerinde (%23-47) olması, ülkemizde sistitte "
        "ampirik TMP-SXT başlanırken kültür sonucunun mutlaka beklenmesi gerektiğini gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> Türkiye direnç oranları: Seftriakson %19-24; Gentamisin %17-18; Amoksisilin/klavulanat %32-37; TMP/SMZ %23-47'dir."
    )
    s83_bullets = [
        "Seftriakson direnci: %19-24.",
        "Gentamisin direnci: %17-18.",
        "Amoksisilin/klavulanat direnci: %32-37; TMP/SMZ direnci: %23-47.",
        "TMP/SMZ'nin %20 eşiğini aşması ampirik kullanımını sınırlar."
    ]
    s83_elements = [
        make_cloze("Türkiye'de E. coli suşlarında seftriakson direnci %19-24 iken gentamisin direnci %17-18 düzeyindedir.", "%19-24", "Parenteral seftriakson direnç aralığı"),
        make_table("Parenteral ve Oral Ajanların Ulusal Direnç Oranları", ["Antibiyotik", "Türkiye Direnç Oranı", "Uygulama Yolu ve Klinik Rol"], [
            {"cells": [{"text": "Seftriakson", "isMasked": False}, {"text": "%19-24", "isMasked": True, "hint": "üçüncü kuşak sefalosporin direnci"}, {"text": "Parenteral piyelonefrit başlangıcı"}]},
            {"cells": [{"text": "Gentamisin", "isMasked": False}, {"text": "%17-18", "isMasked": False}, {"text": "Parenteral aminoglikozid alternatifi", "isMasked": True, "hint": "damar içi aminoglikozid seçeneği"}]},
            {"cells": [{"text": "Amoksisilin/klavulanat", "isMasked": False}, {"text": "%32-37", "isMasked": True, "hint": "ko-amoksilav direnç oranı"}, {"text": "Oral ampirik sistitte önerilmez"}]},
            {"cells": [{"text": "TMP/SMZ", "isMasked": False}, {"text": "%23-47", "isMasked": False}, {"text": "Geniş direnç aralığı (>%20 eşiği aşılmış)", "isMasked": True, "hint": "yüzde yirminin üzerinde seyir"}]}
        ]),
        make_chain("Ulusal Verilerin Tedaviye Yansıması", [
            "1. TMP-SXT Analizi: Direncin %23-47 olması → <%20 kuralının ihlali.",
            "2. Seftriakson ve Gentamisin: Direncin %20 civarında kalması.",
            "3. Piyelonefrit Kararı: Başlangıçta seftriakson/aminoglikozid tercihi.",
            "4. Kültür Takibi: Üreme sonucuna göre duyarla de-eskalasyon."
        ]),
        make_recall("Türkiye'de E. coli suşlarında seftriakson, gentamisin ve amoksisilin/klavulanat direnç oranları nedir?", "Seftriakson %19-24; gentamisin %17-18; amoksisilin/klavulanat %32-37'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ulusal Direnç Oranları", [
            {"text": "Seftriakson direnci %19-24 aralığındadır.", "isLie": False, "explanation": "Doğru. Ders notu oranıdır."},
            {"text": "Gentamisin direnci %17-18 düzeyindedir.", "isLie": False, "explanation": "Doğru. Ders notu oranıdır."},
            {"text": "TMP/SMZ direnci Türkiye'de %0,01 olup dünyadaki en duyarlı ilaçtır.", "isLie": True, "explanation": "Tuzak! TMP/SMZ direnci Türkiye'de %23-47 gibi çok yüksek bir düzeydedir."},
            {"text": "Amoksisilin/klavulanat direnci %32-37 aralığındadır.", "isLie": False, "explanation": "Doğru. Ders notu oranıdır."}
        ]),
        make_quiz("Türkiye'de üriner sistem enfeksiyonu etkeni E. coli suşlarında 'seftriakson' ve 'gentamisin' direnç oranları aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Seftriakson %19-24; Gentamisin %17-18", "isCorrect": True, "explanation": "Ders notundaki Türkiye direnç listesinde 'seftriakson %19-24; gentamisin %17-18' olarak açıkça yer almaktadır."},
            {"key": "B", "text": "Seftriakson %90; Gentamisin %95", "isCorrect": False, "explanation": "Bu oranlar aşırı yüksektir."},
            {"key": "C", "text": "Seftriakson %0; Gentamisin %0", "isCorrect": False, "explanation": "Direnç sıfır değildir."},
            {"key": "D", "text": "Seftriakson %62-64; Gentamisin %5-8", "isCorrect": False, "explanation": "Bu oranlar ampisilin ve nitrofurantoine aittir."}
        ])
    ]
    slides.append(make_slide(83, "Türkiye Direnç Verileri: Seftriakson ve Gentamisin", "Seftriakson (%19-24), gentamisin (%17-18), ko-amoksilav ve TMP/SMZ oranları", "Direnç Profili", s83_narrative, s83_bullets, s83_elements))

    # Slide 84: Dirençli Mikroorganizma Risk Faktörleri: 3 Ay Kuralı
    s84_narrative = (
        "Bir hastada gelişen üriner enfeksiyonun standart ajanlara dirençli bir mikroorganizma "
        "tarafından oluşturulup oluşturulmadığını öngörmede zaman pencereli risk faktörleri kullanılır.\n\n"
        "- **3 Ay Zaman Penceresi:** Dirençli mikroorganizma risk faktörleri içinde 3 aylık süreye "
        "bağlı iki temel klinik durum tanımlanmıştır.\n"
        "- **Antibiyotik Kullanımı:** **Son 3 ay içinde antibiyotik kullanımı**, bakteriyel florada "
        "selektif baskı yaratarak dirençli suşların seçilmesine yol açar.\n"
        "- **İmplant Uygulaması:** **Son 3 ay içinde cerrahi girişimle implant uygulanması (stent, "
        "nefrostomi)**, yabancı cisim üzerinde biyofilm oluşturan dirençli patojenlerin yerleşmesine zemin hazırlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Dirençli patojen risk faktörlerinde 3 ay kriteri: 1) Son 3 ay içinde antibiyotik kullanımı, 2) Son 3 ay içinde cerrahi girişimle implant uygulanması (stent, nefrostomi)."
    )
    s84_bullets = [
        "Son 3 ay içinde antibiyotik kullanımı dirençli patojen risk faktörüdür.",
        "Son 3 ay içinde cerrahi girişimle implant uygulanması (stent, nefrostomi) riski artırır.",
        "Bu iki durumda standart ampirik tedaviler yerine direnç spektrumu genişletilmelidir."
    ]
    s84_elements = [
        make_cloze("Dirençli mikroorganizma risk faktörleri arasında son 3 ay içinde antibiyotik kullanımı ve cerrahi girişimle implant uygulanması (stent, nefrostomi) yer alır.", "son 3 ay içinde", "Antibiyotik ve implant için geçerli kritik zaman eşiği"),
        make_table("Dirençli Patojen: 3 Ay Risk Faktörleri", ["Klinik Durum", "Zaman Penceresi", "Mekanizma / Nitelik"], [
            {"cells": [{"text": "Antibiyotik Kullanımı", "isMasked": False}, {"text": "Son 3 ay içinde", "isMasked": True, "hint": "üç aylık süre"}, {"text": "Dirençli bakteriyel flora seçilimi"}]},
            {"cells": [{"text": "İmplant Uygulanması", "isMasked": False}, {"text": "Son 3 ay içinde", "isMasked": False}, {"text": "Stent, nefrostomi ve biyofilm", "isMasked": True, "hint": "yabancı cisim uygulamaları"}]}
        ]),
        make_chain("3 Ay Kuralı ve Direnç Zinciri", [
            "1. Tıbbi Öykü: Hastanın son 3 aylık ilaç ve işlem anamnezi.",
            "2. Antibiyotik Tespiti: Son 3 ayda antibiyotik kullanıldığının öğrenilmesi.",
            "3. İmplant Tespiti: Son 3 ayda üreteral stent/nefrostomi takılması.",
            "4. Klinik Karar: Dirençli patojen şüphesiyle genişletilmiş tedavi seçimi."
        ]),
        make_recall("Dirençli mikroorganizma risk faktörleri içinde 'son 3 ay' kriterine sahip iki klinik durum nedir?", "1) Son 3 ay içinde antibiyotik kullanımı, 2) Son 3 ay içinde cerrahi girişimle implant uygulanmasıdır (stent, nefrostomi)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 3 Ay Kuralı", [
            {"text": "Son 3 ay içinde antibiyotik kullanımı dirençli patojen risk faktörüdür.", "isLie": False, "explanation": "Doğru. Ders notu risk faktörüdür."},
            {"text": "Son 3 ay içinde cerrahi girişimle implant uygulanması (stent, nefrostomi) riski artırır.", "isLie": False, "explanation": "Doğru. Çıkmış sınav sorusu bilgisidir."},
            {"text": "Son 3 ay içinde antibiyotik alan hastanın idrarı tamamen saf altın suyuna dönüşür ve bakteriler ölür.", "isLie": True, "explanation": "Tuzak! Antibiyotik kullanımı dirençli bakterilerin seçilmesine yol açarak enfeksiyon riskini artırır."},
            {"text": "Stent ve nefrostomi biyofilm oluşumuna zemin hazırlar.", "isLie": False, "explanation": "Doğru. Yabancı cisimlerdir."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'de dirençli mikroorganizma için 'son 3 ay' kriterine sahip risk faktörlerinden biridir?", [
            {"key": "A", "text": "Son 3 ay içinde cerrahi girişimle implant uygulanması (stent, nefrostomi)", "isCorrect": True, "explanation": "Ders notunda ve çıkmış kurul sorusunda açıkça 'Son 3 ay içinde cerrahi girişimle implant uygulanması (stent, nefrostomi)' olarak belirtilmiştir."},
            {"key": "B", "text": "Son 3 ay içinde saç kestirmek", "isCorrect": False, "explanation": "Tıbbi risk faktörü değildir."},
            {"key": "C", "text": "Son 3 ay içinde düzenli spor yapmak", "isCorrect": False, "explanation": "Direnç riski yaratmaz."},
            {"key": "D", "text": "Son 3 ay içinde grip aşısı olmak", "isCorrect": False, "explanation": "Dirençli ÜSE etkeni oluşturmaz."}
        ])
    ]
    slides.append(make_slide(84, "Dirençli Patojen Riskleri: 3 Ay Kriteri", "Son 3 ayda antibiyotik kullanımı ve cerrahi implant uygulanması (stent/nefrostomi)", "Direnç Risk Faktörleri", s84_narrative, s84_bullets, s84_elements))

    # Slide 85: Dirençli Mikroorganizma Risk Faktörleri: 1 Ay Kuralı ve Diyaliz
    s85_narrative = (
        "Hastane ortamı ve cerrahi travma, dirençli nozokomiyal patojenlerin konağa bulaşmasında "
        "çok daha kısa bir zaman penceresinde risk oluşturur.\n\n"
        "- **1 Ay Zaman Penceresi:** Dirençli patojen risk faktörleri içinde 1 aylık süreye bağlı "
        "durumlar: **son 1 ay içinde cerrahi girişim** ve **son 1 ay içinde hastane (özellikle yoğun bakım) "
        "yatış öyküsü**dür.\n"
        "- **Kronik Girişim (Diyaliz):** Zaman kısıtlamasından bağımsız olarak **diyaliz** tedavisi "
        "gören hastalar, sürekli sağlık merkezine giriş-çıkış ve immün disfonksiyon nedeniyle yüksek risklidir.\n"
        "- **Nozokomiyal İntikal:** Yoğun bakım yatışı ve cerrahi girişimler, GSBL üreten Klebsiella "
        "ve Pseudomonas gibi çoklu dirençli patojenlerin hastaya intikalini kolaylaştırır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Dirençli patojen risk faktörlerinde 1 ay kriteri ve diyaliz: Son 1 ay içinde cerrahi girişim, son 1 ay içinde hastane/yoğun bakım yatışı ve diyalizdir."
    )
    s85_bullets = [
        "Son 1 ay içinde cerrahi girişim dirençli patojen riskidir.",
        "Son 1 ay içinde hastane (özellikle yoğun bakım) yatış öyküsü riski belirgin artırır.",
        "Diyaliz hastaları dirençli mikroorganizma açısından yüksek risk grubundadır."
    ]
    s85_elements = [
        make_cloze("Dirençli mikroorganizma risk faktörleri arasında son 1 ay içinde cerrahi girişim, hastane yatışı ve diyaliz yer alır.", "diyaliz", "Kronik böbrek yetmezliğinde dirençli patojen riskini artıran renal replasman tedavisi"),
        make_table("Dirençli Patojen: 1 Ay ve Diyaliz Kriterleri", ["Klinik Durum", "Zaman Penceresi / Şart", "Klinik Tehlike"], [
            {"cells": [{"text": "Cerrahi Girişim", "isMasked": False}, {"text": "Son 1 ay içinde", "isMasked": True, "hint": "bir aylık cerrahi pencere"}, {"text": "Operatif nozokomiyal bulaş"}]},
            {"cells": [{"text": "Hastane / YBÜ Yatışı", "isMasked": False}, {"text": "Son 1 ay içinde", "isMasked": False}, {"text": "Yoğun bakım flora kolonizasyonu", "isMasked": True, "hint": "dirençli hastane bakterisi alımı"}]},
            {"cells": [{"text": "Diyaliz", "isMasked": False}, {"text": "Kronik hemodiyaliz / periton", "isMasked": True, "hint": "diyaliz tedavisi"}, {"text": "Sürekli enstrümantasyon ve immün yetmezlik"}]}
        ]),
        make_chain("1 Ay ve Diyaliz Risk Akışı", [
            "1. Hastaneye Giriş: Son 1 ayda yoğun bakıma yatış veya cerrahi operasyon.",
            "2. Nozokomiyal Kolonizasyon: ÇİD hastane suşlarının hastaya yerleşmesi.",
            "3. Diyaliz Katkısı: Kateter ve vasküler girişimlerle direnç riskinin katlanması.",
            "4. Dirençli Enfeksiyon: Tedavisi güç dirençli patojenle ÜSE tablosu."
        ]),
        make_recall("Dirençli patojen risk faktörleri içinde 'son 1 ay' kriterine sahip durumlar ve kronik girişim faktörü nedir?", "Son 1 ay içinde cerrahi girişim, son 1 ay içinde hastane (özellikle yoğun bakım) yatış öyküsü ve diyalizdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 1 Ay ve Diyaliz", [
            {"text": "Son 1 ay içinde cerrahi girişim dirençli patojen risk faktörüdür.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Son 1 ay içinde hastane (özellikle yoğun bakım) yatışı riski artırır.", "isLie": False, "explanation": "Doğru. Çıkmış soru verisidir."},
            {"text": "Diyaliz tedavisi görmek dirençli bakteri risk faktörleri arasındadır.", "isLie": False, "explanation": "Doğru. Ders notu maddesidir."},
            {"text": "Yoğun bakımda 1 ay kalan bir hastanın idrarında sadece anne sütü bakterileri ürer.", "isLie": True, "explanation": "Tuzak! Yoğun bakım yatışı çoklu dirençli nozokomiyal patojenlerin temel kaynağıdır."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'de dirençli mikroorganizma için 'son 1 ay' kriterine sahip risk faktörleri arasında yer alır?", [
            {"key": "A", "text": "Son 1 ay içinde cerrahi girişim veya hastane (özellikle yoğun bakım) yatış öyküsü", "isCorrect": True, "explanation": "Ders notunda açıkça 'Son 1 ay içinde cerrahi girişim; Son 1 ay içinde hastane (özellikle yoğun bakım) yatış öyküsü' olarak listelenmiştir."},
            {"key": "B", "text": "Son 1 ay içinde düzenli diş fırçalamak", "isCorrect": False, "explanation": "Tıbbi risk faktörü değildir."},
            {"key": "C", "text": "Son 1 ay içinde her gün 8 saat uyumak", "isCorrect": False, "explanation": "Direnç riski oluşturmaz."},
            {"key": "D", "text": "Son 1 ay içinde güneşlenmek", "isCorrect": False, "explanation": "Dirençle ilgisizdir."}
        ])
    ]
    slides.append(make_slide(85, "Dirençli Patojen Riskleri: 1 Ay Kriteri ve Diyaliz", "Son 1 ayda cerrahi girişim, hastane/YBÜ yatışı ve diyaliz riskleri", "Direnç Risk Faktörleri", s85_narrative, s85_bullets, s85_elements))

    # Slide 86: Dirençli Mikroorganizma Risk Faktörleri: Enfeksiyon ve Kolonizasyon Öyküsü
    s86_narrative = (
        "Zaman kısıtlamalı işlemlerin yanı sıra hastanın geçmiş enfeksiyon ve kolonizasyon öyküsü, "
        "bakteriyel rezervuarın direnç potansiyelini doğrudan ele verir.\n\n"
        "- **Tekrarlayan ÜSE Öyküsü:** **Son 6 ayda ≥2 veya son 1 yılda ≥3 atak geçirilmesi**, "
        "hastanın daha önce çok sayıda antibiyotiğe maruz kaldığını ve dirençli suş barındırdığını gösterir.\n"
        "- **Dirençli Bakteri Öyküsü:** **GSBL veya ÇİD olan mikroorganizma ile kolonizasyon veya "
        "enfeksiyon öyküsü** bulunması en güçlü bağımsız risk faktörüdür.\n"
        "- **Safra Yolu İlişkisi:** **Tekrarlayan safra yolu enfeksiyonu öyküsü**, enterik bakterilerin "
        "biliyer kanalda da direnç geliştirdiğini ve ürofloraya yansıdığını belgeler.\n\n"
        "> [!IMPORTANT]\n"
        "> Dirençli patojen risk faktörleri: Tekrarlayan ÜSE (6 ayda ≥2 veya yılda ≥3), GSBL/ÇİD kolonizasyon/enfeksiyon öyküsü ve tekrarlayan safra yolu enfeksiyonu öyküsüdür."
    )
    s86_bullets = [
        "Tekrarlayan ÜSE öyküsü (son 6 ayda ≥2 veya son 1 yılda ≥3 atak).",
        "GSBL veya ÇİD olan mikroorganizma ile kolonizasyon veya enfeksiyon öyküsü.",
        "Tekrarlayan safra yolu enfeksiyonu öyküsü direnç riskini artırır."
    ]
    s86_elements = [
        make_cloze("Dirençli mikroorganizma risk faktörleri arasında GSBL veya ÇİD olan mikroorganizma ile kolonizasyon veya enfeksiyon öyküsü yer alır.", "GSBL veya ÇİD", "Genişlemiş spektrumlu beta-laktamaz veya çok ilaca dirençli patojenler"),
        make_table("Enfeksiyon ve Kolonizasyon Risk Faktörleri", ["Risk Durumu", "Kriter / Tanım", "Klinik Anlamı"], [
            {"cells": [{"text": "Tekrarlayan ÜSE Öyküsü", "isMasked": False}, {"text": "Son 6 ayda ≥2 veya 1 yılda ≥3 atak", "isMasked": True, "hint": "sık atak öyküsü"}, {"text": "Sık antibiyotik maruziyeti"}]},
            {"cells": [{"text": "Dirençli Patojen Öyküsü", "isMasked": False}, {"text": "GSBL veya ÇİD kolonizasyonu", "isMasked": False}, {"text": "Aynı dirençli suşun alevlenmesi", "isMasked": True, "hint": "dirençli bakterinin vücutta barınması"}]},
            {"cells": [{"text": "Biliyer Sistem", "isMasked": False}, {"text": "Tekrarlayan safra yolu enfeksiyonu", "isMasked": True, "hint": "kolanjit ve biliyer ataklar"}, {"text": "Enterik direnç rezervuarı"}]}
        ]),
        make_chain("Öyküye Dayalı Direnç Değerlendirmesi", [
            "1. Anamnez Alma: Geçmiş enfeksiyon ve kolonizasyon kayıtlarının incelenmesi.",
            "2. Atak Sayımı: 6 ayda ≥2 veya yılda ≥3 ÜSE atağının doğrulanması.",
            "3. Kolonizasyon Tespiti: Eski kültürlerde GSBL/ÇİD pozitifliği bulunması.",
            "4. Ampirik Rejim: Standart sefalosporinlerin dışlanıp geniş spektruma geçilmesi."
        ]),
        make_recall("Ders notuna göre tekrarlayan ÜSE öyküsünde direnç riski doğuran atak sayısı eşiği nedir?", "Son 6 ayda ≥2 veya son 1 yılda ≥3 atak geçirilmesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kolonizasyon ve Öykü", [
            {"text": "GSBL veya ÇİD kolonizasyon öyküsü dirençli patojen risk faktörüdür.", "isLie": False, "explanation": "Doğru. Ders notu maddesidir."},
            {"text": "Son 6 ayda ≥2 veya 1 yılda ≥3 ÜSE atağı riski artırır.", "isLie": False, "explanation": "Doğru. Tekrarlayan ÜSE kriteridir."},
            {"text": "Tekrarlayan safra yolu enfeksiyonu öyküsü direnç riskini artırır.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Geçmişte GSBL üreten bir bakterisi olan hastada yeni enfeksiyon daima %100 penisiline duyarlıdır.", "isLie": True, "explanation": "Tuzak! GSBL kolonizasyon öyküsü yeni atağın da dirençli olma riskini katlar."}
        ]),
        make_quiz("ÜSE'de dirençli mikroorganizma risk faktörleri arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Tekrarlayan ÜSE öyküsü (son 6 ayda ≥2 veya son 1 yılda ≥3 atak) ve GSBL/ÇİD öyküsü", "isCorrect": True, "explanation": "Ders notunda dirençli mikroorganizma risk faktörlerinin ilk iki maddesidir."},
            {"key": "B", "text": "Yalnızca gözlük takıyor olmak", "isCorrect": False, "explanation": "Direnç faktörü değildir."},
            {"key": "C", "text": "Haftada 2 kez balık yemek", "isCorrect": False, "explanation": "Beslenme ile direnç faktörü değildir."},
            {"key": "D", "text": "Daha önce hiç antibiyotik kullanmamış olmak", "isCorrect": False, "explanation": "Duyarlılık göstergesidir, direnç riski değildir."}
        ])
    ]
    slides.append(make_slide(86, "Dirençli Patojen Riskleri: Kolonizasyon ve Öykü", "Tekrarlayan ÜSE, GSBL/ÇİD kolonizasyonu ve tekrarlayan safra yolu enfeksiyonu", "Direnç Risk Faktörleri", s86_narrative, s86_bullets, s86_elements))

    # Slide 87: Sınav Klasiği: Kontrolsüz Diyabet Direnç Riski midir?
    s87_narrative = (
        "Tıp fakültesi kurullarında ve uzmanlık sınavlarında en sık sorulan klasik çeldiricilerden "
        "biri diyabet ile dirençli patojen risk faktörleri arasındaki ayrımdır.\n\n"
        "- **Sınav Sorusu Analizi:** Çıkmış kurul sorusunda: *'Aşağıdakilerden hangisi ÜSE'de dirençli "
        "mikroorganizma için risk faktörlerinden değildir?'* sorusunun doğru cevabı **Kontrolsüz diyabet**tir.\n"
        "- **Kavramsal Ayrım:** Diyabet (şeker hastalığı), üriner sistem enfeksiyonu gelişimi ve "
        "komplike ÜSE için önemli bir konak risk faktörüdür; ancak **ders notundaki dirençli mikroorganizma "
        "risk faktörleri listesinde yer almamaktadır**.\n"
        "- **Klinik Mantık:** Diyabetik hastada da en sık etken standart E. coli'dir; diyabet tek "
        "başına antibiyotik direncini artıran bağımsız bir faktör olarak listelenmez.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kontrolsüz diyabet ÜSE sıklığını ve komplikasyon riskini artırır; ancak ders notundaki DİRENÇLİ MİKROORGANİZMA risk faktörleri listesinde yer almaz (Klasik Sınav Sorusu)!"
    )
    s87_bullets = [
        "Kontrolsüz diyabet, dirençli mikroorganizma risk faktörleri listesinde YER ALMAZ.",
        "Direnç riskleri: Son 3 ay antibiyotik/implant, son 1 ay cerrahi/yatış, diyaliz, nüks.",
        "Diyabet ÜSE gelişimi ve komplike enfeksiyon için risk faktörüdür, direnç için değil."
    ]
    s87_elements = [
        make_cloze("Kontrolsüz diyabet ÜSE'ye zemin hazırlamakla birlikte ders notundaki dirençli mikroorganizma risk faktörleri listesinde yer almaz.", "dirençli mikroorganizma", "Diyabetin risk faktörü listesinde yer almadığı kategori"),
        make_table("Çıkmış Sınav Sorusu Analiz Tablosu", ["Risk Faktörü Adayı", "Ders Notu Direnç Listesinde Var mı?", "Sınav Doğru / Yanlış Statüsü"], [
            {"cells": [{"text": "Son 3 ay içinde antibiyotik kullanımı", "isMasked": False}, {"text": "EVET, LİSTEDE VAR", "isMasked": False}, {"text": "Direnç risk faktörüdür"}]},
            {"cells": [{"text": "Son 3 ay içinde implant uygulanması", "isMasked": False}, {"text": "EVET, LİSTEDE VAR", "isMasked": False}, {"text": "Direnç risk faktörüdür"}]},
            {"cells": [{"text": "Diyaliz ve tekrarlayan ÜSE", "isMasked": False}, {"text": "EVET, LİSTEDE VAR", "isMasked": False}, {"text": "Direnç risk faktörüdür"}]},
            {"cells": [{"text": "Kontrolsüz Diyabet", "isMasked": False}, {"text": "HAYIR, LİSTEDE YOK", "isMasked": True, "hint": "listede bulunmayan şık"}, {"text": "Çıkmış sorunun DOĞRU CEVABI", "isMasked": True, "hint": "çeldirici analiz cevabı"}]}
        ]),
        make_chain("Sınav Sorusu Çözüm Mantığı", [
            "1. Soru Kökü: Dirençli mikroorganizma için risk faktörlerinden DEĞİLDİR?",
            "2. Şık Taraması: Son 3 ay ab/implant, son 1 ay cerrahi/yatış, diyaliz.",
            "3. Çeldirici Analizi: Kontrolsüz diyabetin listede olmadığının saptanması.",
            "4. Doğru Cevap: Kontrolsüz diyabet şıkkının işaretlenmesi."
        ]),
        make_recall("Çıkmış kurul sorusuna göre hangisi ÜSE'de dirençli mikroorganizma için risk faktörlerinden değildir?", "Kontrolsüz diyabettir (ders notundaki dirençli mikroorganizma risk faktörleri listesinde yer almaz)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kontrolsüz Diyabet Tuzağı", [
            {"text": "Son 3 ay içinde antibiyotik kullanımı dirençli patojen risk faktörüdür.", "isLie": False, "explanation": "Doğru. Listede vardır."},
            {"text": "Diyaliz dirençli mikroorganizma risk faktörlerindendir.", "isLie": False, "explanation": "Doğru. Listede vardır."},
            {"text": "Kontrolsüz diyabet ders notundaki dirençli mikroorganizma risk faktörleri listesinin en başında yer alır.", "isLie": True, "explanation": "Tuzak! Kontrolsüz diyabet dirençli mikroorganizma listesinde yer almaz (çıkmış sınav sorusudur)."},
            {"text": "Tekrarlayan ÜSE öyküsü direnç risk faktörüdür.", "isLie": False, "explanation": "Doğru. Listede yer alır."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'de dirençli mikroorganizma için risk faktörlerinden DEĞİLDİR? (Kurul 1 Çıkmış Soru)", [
            {"key": "A", "text": "Kontrolsüz diyabet", "isCorrect": True, "explanation": "Ders notu ve çıkmış kurul sorusu çözümüne göre: Dirençli mikroorganizma risk faktörleri arasında son 3 ay antibiyotik, son 3 ay implant, son 1 ay cerrahi/yatış, diyaliz ve tekrarlayan ÜSE yer alır; kontrolsüz diyabet bu listede yer almamaktadır."},
            {"key": "B", "text": "Son 3 ay içinde antibiyotik kullanımı", "isCorrect": False, "explanation": "Listede yer alan önemli bir risk faktörüdür."},
            {"key": "C", "text": "Son 3 ay içinde cerrahi girişim implant uygulanması", "isCorrect": False, "explanation": "Listede yer alan bir risk faktörüdür."},
            {"key": "D", "text": "Diyaliz", "isCorrect": False, "explanation": "Listede yer alan bir risk faktörüdür."}
        ])
    ]
    slides.append(make_slide(87, "Sınav Klasiği: Kontrolsüz Diyabet ve Direnç Ayrımı", "Çıkmış kurul sorusu analizi: Diyabetin dirençli patojen listesinde yer almaması", "Direnç Risk Faktörleri", s87_narrative, s87_bullets, s87_elements))

    # Slide 88: Hastaneye Yatış Kriterleri: Sistemik Toksisite ve Komplikasyon Riski
    s88_narrative = (
        "Üriner sistem enfeksiyonu tanısı alan bir hastanın ayaktan mı yoksa hastaneye yatırılarak "
        "parenteral tedaviyle mi yönetileceği hayati bir klinik karardır.\n\n"
        "- **Genel Durum Kriterleri:** **Yüksek ateşle birlikte ciddi hastalık tablosu, ağrı ve genel "
        "düşkünlük hali** ile **oral alım bozukluğu** (bulantı/kusma nedeniyle ilaç alamama) mutlak yatış gerektirir.\n"
        "- **Hasta Özellikleri:** **Gebelik** (piyelonefrit erken doğum ve sepsis riski taşır) ve **uyumsuz "
        "hasta** (tedaviye ve kontrole riayet edemeyecek sosyal/bilişsel durum).\n"
        "- **Enfeksiyon Dinamikleri:** **Tekrarlayan enfeksiyonlar, tekrarlarsa komplike olabilecek "
        "durumlar ve dirençli bakteri enfeksiyonları** hastaneye yatış kriterlerini oluşturur.\n\n"
        "> [!IMPORTANT]\n"
        "> Hastaneye yatış kriterleri: Yüksek ateşle ciddi hastalık tablosu, ağrı/düşkünlük, oral alım bozukluğu, gebelik, uyumsuz hasta, tekrarlayan enfeksiyonlar, komplike olabilecek durumlar ve dirençli bakterilerdir."
    )
    s88_bullets = [
        "Yüksek ateşle birlikte ciddi hastalık tablosu, ağrı ve genel düşkünlük hali.",
        "Oral alım bozukluğu (ilaç alamama), gebelik ve tedaviye uyumsuz hasta.",
        "Tekrarlayan enfeksiyonlar, komplike olabilecek durumlar ve dirençli bakteri enfeksiyonları."
    ]
    s88_elements = [
        make_cloze("ÜSE'de hastaneye yatış kriterleri arasında oral alım bozukluğu, gebelik, uyumsuz hasta ve dirençli bakteri enfeksiyonları yer alır.", "oral alım bozukluğu", "Hastanın hap içmesini engelleyen bulantı/kusma tablosu"),
        make_table("Hastaneye Yatış Kriterleri Sınıflaması", ["Kriter Kategorisi", "Klinik Durumlar", "Yatış Gerekçesi"], [
            {"cells": [{"text": "Toksisite ve Genel Durum", "isMasked": False}, {"text": "Yüksek ateş, ciddi hastalık, düşkünlük", "isMasked": True, "hint": "ağır sistemik belirtiler"}, {"text": "Sepsis ve şok riskini önleme"}]},
            {"cells": [{"text": "Fizyolojik / Özel Hasta", "isMasked": False}, {"text": "Oral alım bozukluğu, gebelik, uyumsuzluk", "isMasked": False}, {"text": "Parenteral hidrasyon ve yakın izlem", "isMasked": True, "hint": "damar içi tedavi zorunluluğu"}]},
            {"cells": [{"text": "Enfeksiyon ve Direnç", "isMasked": False}, {"text": "Dirençli bakteriler, tekrarlayan enfeksiyon", "isMasked": True, "hint": "tedavisi güç inatçı patojenler"}, {"text": "Geniş spektrumlu parenteral tedavi"}]}
        ]),
        make_chain("Yatış Karar Algoritması", [
            "1. Klinik Değerlendirme: Ateş, ağrı, düşkünlük ve oral alımın sorgulanması.",
            "2. Özel Durum Kontrolü: Gebelik veya uyumsuzluk varlığının tespiti.",
            "3. Mikrobiyolojik Risk: Dirençli bakteri veya nüks enfeksiyon saptanması.",
            "4. Yatış: Parenteral tedavi ve monitorizasyon için servise yatış."
        ]),
        make_recall("Ders notuna göre ÜSE'de hastaneye yatış kriterleri nelerdir?", "Yüksek ateşle birlikte ciddi hastalık tablosu, ağrı ve genel düşkünlük hali, oral alım bozukluğu, gebelik, uyumsuz hasta, tekrarlayan enfeksiyonlar, tekrarlarsa komplike olabilecek durumlar ve dirençli bakteri enfeksiyonlarıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hastaneye Yatış Kriterleri", [
            {"text": "Oral alım bozukluğu ve gebelik hastaneye yatış kriterlerindendir.", "isLie": False, "explanation": "Doğru. Ders notu kriterleridir."},
            {"text": "Yüksek ateşle ciddi hastalık tablosu ve düşkünlük yatış gerektirir.", "isLie": False, "explanation": "Doğru. Sistemik toksisite bulgusudur."},
            {"text": "Dirençli bakteri enfeksiyonu saptanan hastalar asla hastaneye kabul edilmeyip ormana bırakılmalıdır.", "isLie": True, "explanation": "Tuzak! Dirençli bakteri enfeksiyonları hastaneye yatış kriterleri arasında yer alır."},
            {"text": "Uyumsuz hastalar hastaneye yatırılarak tedavi edilmelidir.", "isLie": False, "explanation": "Doğru. Tedavi güvenliği için şarttır."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarında hastaneye yatış kriterleri arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Yüksek ateşle birlikte ciddi hastalık tablosu, oral alım bozukluğu, gebelik, dirençli bakteri enfeksiyonları", "isCorrect": True, "explanation": "Ders notunda 'Hastaneye yatış kriterleri: yüksek ateşle birlikte ciddi hastalık tablosu; ağrı ve genel düşkünlük hali; oral alım bozukluğu; gebelik; uyumsuz hasta; tekrarlayan enfeksiyonlar; tekrarlarsa komplike olabilecek durumlar; dirençli bakteri enfeksiyonları' olarak sayılmıştır."},
            {"key": "B", "text": "Yalnızca hafif dizürisi olan ve neşesi yerinde olan genç kadın", "isCorrect": False, "explanation": "Ayaktan tedavi edilir."},
            {"key": "C", "text": "Sadece saçında kepek olan hastalar", "isCorrect": False, "explanation": "ÜSE yatış kriteri değildir."},
            {"key": "D", "text": "Oral yoldan günde 5 litre su içebilen hafif sistit", "isCorrect": False, "explanation": "Ayaktan izlenir."}
        ])
    ]
    slides.append(make_slide(88, "Hastaneye Yatış Kriterleri", "Yüksek ateş, oral alım bozukluğu, gebelik, dirençli bakteri ve yatış endikasyonları", "Direnç Risk Faktörleri", s88_narrative, s88_bullets, s88_elements))

    # Slide 89: Dokuzuncu Bölüm Özeti: Direnç Verileri ve Riskler
    s89_narrative = (
        "Türkiye'nin güncel antibiyotik direnç haritası, dirençli patojen risk faktörleri ve hastaneye "
        "yatış kriterleri dokuzuncu bölümün temel sentezini oluşturur.\n\n"
        "- **Türkiye Direnç:** E. coli'de **ampisilin %62-64 (en yüksek)**, amoksilav %32-37, **seftriakson "
        "%19-24**, gentamisin %17-18, TMP/SMZ %23-47, siprofloksasin %30-39 ve **nitrofurantoin %5-8 (en düşük)**.\n"
        "- **Direnç Riskleri:** Son 3 ay antibiyotik/implant; son 1 ay cerrahi/hastane yatışı; diyaliz; "
        "nüks ÜSE; GSBL/ÇİD öyküsü (Kontrolsüz diyabet bu listede DEĞİLDİR).\n"
        "- **Yatış Kriterleri:** Ciddi hastalık/ateş, oral alım bozukluğu, gebelik, uyumsuz hasta, "
        "tekrarlayan durumlar ve dirençli bakterilerdir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] Nitrofurantoin %5-8 ile en düşük, ampisilin %62-64 ile en yüksek dirence sahiptir; direnç riskinde 3 ay (ab/implant) ve 1 ay (cerrahi/yatış) kritik olup diyabet listede yoktur; yatış kriterleri toksisite ve direnci kapsar."
    )
    s89_bullets = [
        "Türkiye E. coli direnci: Nitrofurantoin en düşük (%5-8); Ampisilin en yüksek (%62-64).",
        "Siprofloksasin %30-39; Seftriakson %19-24; TMP/SMZ %23-47.",
        "Direnç riskleri: Son 3 ay ab/implant, son 1 ay cerrahi/yatış, diyaliz (diyabet listede yoktur).",
        "Yatış: Yüksek ateş, oral alım bozukluğu, gebelik, uyumsuzluk, dirençli bakteri."
    ]
    s89_elements = [
        make_cloze("Türkiye'de E. coli direncinde en düşük oran %5-8 ile nitrofurantoin iken en yüksek oran %62-64 ile ampisilin suşlarındadır.", "ampisilin", "Türkiye'de en yüksek dirence sahip antibiyotik"),
        make_table("9. Bölüm Büyük Özet Matrisi", ["Kategori", "Temel Veri / Kriter", "Klinik Çıkarım"], [
            {"cells": [{"text": "En Düşük Direnç", "isMasked": False}, {"text": "Nitrofurantoin (%5-8)", "isMasked": True, "hint": "en güvenilir oral ajan"}, {"text": "Sistitte ilk tercih güvenilirliği"}]},
            {"cells": [{"text": "En Yüksek Direnç", "isMasked": False}, {"text": "Ampisilin (%62-64)", "isMasked": False}, {"text": "Ampirik kullanım dışı", "isMasked": True, "hint": "tedaviden çıkarılma nedeni"}]},
            {"cells": [{"text": "Direnç Riski (3 Ay)", "isMasked": False}, {"text": "Antibiyotik kullanımı ve implant", "isMasked": True, "hint": "üç aylık iki kriter"}, {"text": "Geniş spektrum gereksinimi"}]},
            {"cells": [{"text": "Listede Olmayan Faktör", "isMasked": False}, {"text": "Kontrolsüz diyabet", "isMasked": False}, {"text": "Sınav tuzağı (direnç listesinde yok)", "isMasked": True, "hint": "çıkmış soru çeldiricisi"}]}
        ]),
        make_chain("Klinik Değerlendirme Zinciri", [
            "1. Direnç Taraması: Türkiye oranlarının (nitrofurantoin %5-8, kinolon %30-39) bilinmesi.",
            "2. Risk Sorgusu: Son 3 ay ab/implant ve son 1 ay cerrahi/yatışın sorulması.",
            "3. Yatış Kararı: Oral alım bozukluğu, gebelik veya yüksek ateşle yatış kararı.",
            "4. Tedavi Başlangıcı: Direnç riskine uygun parenteral/oral planlama."
        ]),
        make_recall("Dokuzuncu bölümün temel kazanımı olarak Türkiye'de en düşük dirençli ilaç ve listede olmayan sınav çeldiricisi nedir?", "En düşük dirençli ilaç nitrofurantoin (%5-8) olup listede yer almayan sınav çeldiricisi kontrolsüz diyabettir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 9 Özeti", [
            {"text": "Türkiye'de nitrofurantoin direnci %5-8, siprofloksasin direnci %30-39'dur.", "isLie": False, "explanation": "Doğru. Ulusal sürveyans verisidir."},
            {"text": "Son 3 ay içinde antibiyotik kullanımı dirençli patojen risk faktörüdür.", "isLie": False, "explanation": "Doğru. 3 ay kuralıdır."},
            {"text": "Kontrolsüz diyabet ders notundaki dirençli mikroorganizma risk faktörleri listesindedir.", "isLie": True, "explanation": "Tuzak! Kontrolsüz diyabet bu listede yer almamaktadır (çıkmış sınav sorusudur)."},
            {"text": "Oral alım bozukluğu ve gebelik hastaneye yatış kriterleri arasındadır.", "isLie": False, "explanation": "Doğru. Yatış kriteridir."}
        ]),
        make_quiz("Dokuzuncu bölümde işlenen direnç verileri ve risk faktörleri değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Türkiye'de E. coli suşlarında direnç oranı en yüksek olan antibiyotik nitrofurantoindir (%95)", "isCorrect": True, "explanation": "Yanlış! Türkiye'de nitrofurantoin direnci en düşüktür (%5-8); en yüksek olan ampisilindir (%62-64)."},
            {"key": "B", "text": "Son 3 ay içinde cerrahi girişimle implant uygulanması dirençli patojen riskidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Son 1 ay içinde cerrahi girişim ve hastane yatışı dirençli patojen riskidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Yüksek ateşle birlikte ciddi hastalık tablosu hastaneye yatış kriteridir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(89, "Dokuzuncu Bölüm Özeti: Direnç Verileri ve Riskler", "Türkiye direnç profili, 3 ay/1 ay risk kuralları ve yatış kriterlerinin özeti", "Bölüm Özeti", s89_narrative, s89_bullets, s89_elements))

    # Slide 90: [TEKRAR SAYFASI - CHECKPOINT 9] Türkiye Direnç Verileri ve Risk Faktörleri
    s90_narrative = (
        "Bu tekrar sayfasında 9. Bölümde işlenen Türkiye E. coli direnç oranlarını, dirençli mikroorganizma "
        "risk faktörlerini (3 ay ve 1 ay kuralları) ve hastaneye yatış kriterlerini pekiştiriyoruz.\n\n"
        "- **Türkiye Direnç Oranları:** Ampisilin **%62-64 (en yüksek)**; Ko-amoksilav **%32-37**; "
        "Seftriakson **%19-24**; Gentamisin **%17-18**; TMP/SMZ **%23-47**; Siprofloksasin **%30-39**; "
        "Nitrofurantoin **%5-8 (en düşük)**.\n"
        "- **Direnç Riskleri:** Son 3 ay içinde **antibiyotik/implant**; Son 1 ay içinde **cerrahi/hastane "
        "yatışı**; **diyaliz**; nüks ÜSE; GSBL/ÇİD öyküsü (Kontrolsüz diyabet listede DEĞİLDİR).\n"
        "- **Yatış Kriterleri:** Ciddi hastalık tablosu/ateş, ağrı/düşkünlük, oral alım bozukluğu, "
        "gebelik, uyumsuz hasta, tekrarlayan durumlar, dirençli bakteriler.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 9] Nitrofurantoin en düşük (%5-8), ampisilin en yüksek (%62-64); direnç riskinde son 3 ay (ab/implant), son 1 ay (cerrahi/yatış) ve diyaliz esastır; kontrolsüz diyabet listede yoktur; yatış kriterleri toksisite ve direnci kapsar."
    )
    s90_bullets = [
        "Türkiye E. coli direnci: Nitrofurantoin en düşük (%5-8); Ampisilin en yüksek (%62-64).",
        "Siprofloksasin %30-39, Seftriakson %19-24, Gentamisin %17-18, TMP/SMZ %23-47.",
        "Direnç riskleri: Son 3 ay ab/implant, son 1 ay cerrahi/yatış, diyaliz (diyabet listede yoktur).",
        "Yatış: Yüksek ateş, oral alım bozukluğu, gebelik, uyumsuz hasta, dirençli bakteri."
    ]
    s90_elements = [
        make_cloze("Türkiye'de E. coli suşlarında siprofloksasin direnci %30-39 iken en düşük direnç %5-8 ile nitrofurantoin grubundadır.", "%5-8", "Nitrofurantoinin ulusal düşük direnç aralığı"),
        make_table("9. Bölüm Büyük Tekrar Tablosu", ["Parametre / Risk Grubu", "Sayısal Değer / Kriter", "Klinik Özellik"], [
            {"cells": [{"text": "En Düşük Direnç", "isMasked": False}, {"text": "Nitrofurantoin (%5-8)", "isMasked": True, "hint": "en düşük oran"}, {"text": "Oral sistitte güvenilir ilk basamak"}]},
            {"cells": [{"text": "En Yüksek Direnç", "isMasked": False}, {"text": "Ampisilin (%62-64)", "isMasked": False}, {"text": "Ampirik tedavide kesinlikle yeri yok", "isMasked": True, "hint": "uygunsuz ilaç"}]},
            {"cells": [{"text": "Kinolon ve Sefalosporin", "isMasked": False}, {"text": "Sipro %30-39; Seftriakson %19-24", "isMasked": True, "hint": "kinolon ve seftriakson yüzdeleri"}, {"text": "Kinolon kısıtlı, seftriakson parankimde"}]},
            {"cells": [{"text": "Direnç Riski (3 Ay)", "isMasked": False}, {"text": "Son 3 ayda antibiyotik ve implant", "isMasked": False}, {"text": "Selektif baskı ve biyofilm riski", "isMasked": True, "hint": "üç aylık iki risk"}]},
            {"cells": [{"text": "Direnç Riski (1 Ay)", "isMasked": False}, {"text": "Son 1 ayda cerrahi ve hastane yatışı", "isMasked": True, "hint": "bir aylık iki risk"}, {"text": "Nozokomiyal intikal riski"}]}
        ]),
        make_chain("9. Bölüm Sentez Zinciri", [
            "1. Ulusal Direnç Haritası: Nitrofurantoin (%5-8) vs Ampisilin (%62-64).",
            "2. 3 Ay Kuralı: Son 3 ayda antibiyotik kullanımı veya implant varlığı.",
            "3. 1 Ay Kuralı: Son 1 ayda cerrahi girişim veya hastane/YBÜ yatışı.",
            "4. Yatış Kararı: Yüksek ateş, oral alım bozukluğu veya gebelikte yatış."
        ]),
        make_recall("Checkpoint 9: Türkiye'de en düşük dirençli antibiyotik, son 3 ayın iki risk faktörü ve sınav sorusu çeldiricisi nedir?", "En düşük dirençli ilaç nitrofurantoin (%5-8); son 3 ay riskleri antibiyotik kullanımı ve implant uygulanması; listede yer almayan sınav çeldiricisi ise kontrolsüz diyabettir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 9 Konsolidasyonu", [
            {"text": "Türkiye'de E. coli'de en düşük direnç nitrofurantoinde (%5-8) görülür.", "isLie": False, "explanation": "Doğru. 9. bölüm temel kuralıdır."},
            {"text": "Son 3 ay içinde antibiyotik kullanımı dirençli patojen risk faktörüdür.", "isLie": False, "explanation": "Doğru. 3 ay kriteridir."},
            {"text": "Son 1 ay içinde cerrahi girişim direnç risk faktörleri arasındadır.", "isLie": False, "explanation": "Doğru. 1 ay kriteridir."},
            {"text": "Kontrolsüz diyabet ders notundaki dirençli mikroorganizma risk faktörleri listesindedir.", "isLie": True, "explanation": "Tuzak! Kontrolsüz diyabet bu listede yer almaz (çıkmış sınav sorusu anahtarıdır)."}
        ]),
        make_quiz("9. Bölümün tamamı (Türkiye Direnç Verileri ve Risk Faktörleri) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Kontrolsüz diyabet ders notundaki dirençli mikroorganizma risk faktörleri listesinde açıkça yer alır", "isCorrect": True, "explanation": "Yanlış! Kontrolsüz diyabet ders notundaki dirençli patojen risk faktörleri listesinde yer almamaktadır (çıkmış sınav sorusudur)."},
            {"key": "B", "text": "Türkiye'de E. coli suşlarında nitrofurantoin direnci %5-8 ile en düşük orandadır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Son 3 ay içinde antibiyotik kullanımı ve implant uygulanması dirençli patojen risk faktörüdür", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Oral alım bozukluğu ve gebelik hastaneye yatış kriterleri arasında yer alır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(90, "[TEKRAR SAYFASI - CHECKPOINT 9] Türkiye Direnç Verileri ve Dirençli Patojen Riskleri", "9. Bölümün kapsamlı pekiştirmesi: ulusal direnç, 3 ay/1 ay risk kuralları ve yatış kriterleri", "Bölüm Tekrarı", s90_narrative, s90_bullets, s90_elements))

    return slides
