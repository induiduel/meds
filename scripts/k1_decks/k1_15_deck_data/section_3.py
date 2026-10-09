# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-15-s21",
        "title": "Skarla Onarımın Dört Temel Evresi",
        "content": "Doku hasarı rejenerasyon sınırlarını aştığında, organizma hasarlı bölgeyi bağ dokusu ile onarmak için dinamik ve örtüşen 4 evreli bir program başlatır (Sınav Spotu):\n\n- **1. Hemostaz Evresi (İlk Dakikalar):** Kanamanın durdurulması, trombosit agregasyonu ve yara boşluğunu dolduran geçici fibrin pıhtısının oluşması.\n- **2. Enflamasyon Evresi (0 - 48 Saat):** Önce nötrofillerin, ardından makrofajların yara yatağına akması; bakterilerin ve nekrotik doku artıklarının fagosite edilmesi.\n- **3. Proliferasyon Evresi (3 - 10 Gün):** Granülasyon dokusunun kurulması; yoğun anjiyogenez, fibroblast göçü ve proliferasyonu, gevşek ECM sentezi ve re-epitelizasyon.\n- **4. Remodeling / Yeniden Şekillenme Evresi (2-3. Hafta - Aylar):** ECM'nin olgunlaşması, Tip III kollajenin yerini güçlü Tip I kollajene bırakması, yara kontraksiyonu ve skarın avaskülerleşmesi.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Evre Adı", "Zaman Aralığı", "Baskın Hücre Tipi", "Temel Biyolojik Olay"],
                [
                    ["1. Hemostaz", "İlk dakikalar - saatler", "Trombositler", "Fibrin pıhtısı ve geçici matriks oluşumu"],
                    ["2. Enflamasyon", "İlk 6 - 48 saat", "Nötrofil ve Makrofajlar", "Enkaz temizliği ve büyüme faktörü salınımı"],
                    ["3. Proliferasyon", "3 - 10. günler", "Endotel ve Fibroblastlar", "Granülasyon dokusu ve anjiyogenez"],
                    ["4. Remodeling", "2. haftadan aylara", "Miyofibroblast ve Fibrosit", "Kollajen çapraz bağlanması ve skar kontraksiyonu"]
                ]
            ),
            make_cloze(
                "Skarla onarımın aşamaları hemostaz, enflamasyon, proliferasyon ve remodeling olmak üzere dört evrede gerçekleşir.",
                "remodeling",
                "Matriksin yeniden şekillendiği son evre adı"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-15-s22",
        "title": "İlk Dakikalar: Hemostaz, Trombosit Tıkacı ve Fibrin Pıhtısı",
        "content": "Bir damar kesildiğinde veya doku yırtıldığında onarımın ilk acil hamlesi kan kaybını durdurmaktır:\n\n- **Damar Vazokonstriksiyonu:** Endotelin ve refleks nörojenik uyarıyla hasarlı arteriyoller saniyeler içinde kasılır.\n- **Primer Hemostaz (Trombosit Tıkacı):**\n  - Açığa çıkan subendotelyal kollajen ve von Willebrand faktörüne (vWF) trombositler yapışır (adezyon).\n  - Trombositler aktive olarak granüllerini boşaltır (ADP, Tromboksan A2); yeni trombositler kümelenir.\n- **Sekonder Hemostaz (Koagülasyon Kaskadı):**\n  - Doku faktörü (Faktör III) ekstrinsek yolu tetikler; trombin üretilir.\n  - Trombin, kanda çözünür haldeki fibrinojeni çözünmeyen **fibrin liflerine** çevirir.\n- **Sonuç:** Trombositler ve alyuvarlar fibrin ağının içine hapsolarak yarayı kapatan geçici bir mühür oluşturur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Yaralanma Anında Hemostazın Tetiklenme Zinciri",
                [
                    "1. Vasküler Hasar: Damar yırtılır ve subendotelyal bazal membran açığa çıkar.",
                    "2. Trombosit Adezyonu: Trombositler vWF aracılığıyla kollajene tutunur ve şekil değiştirir.",
                    "3. Granül Salınımı: Trombositlerden ADP, TxA2, PDGF ve TGF-beta boşalır.",
                    "4. Trombin Aktivasyonu: Koagülasyon kaskadı ile protrombin trombine dönüşür.",
                    "5. Fibrin Ağı Örülmesi: Fibrinojen fibrine polimerize olarak pıhtıyı stabilize eder."
                ]
            ),
            make_quiz(
                "Yaralanmanın hemen ardından yara alanında oluşan ve kanamayı durdurmanın yanı sıra hücrelerin göçü için geçici bir iskelet sağlayan ilk yapı aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Olgun Tip I kollajen skarı", "isCorrect": False, "explanation": "Tip I kollajen haftalar sonra oluşan nihai skar yapısıdır."},
                    {"key": "B", "text": "Fibrin pıhtısı ve trombosit tıkacı", "isCorrect": True, "explanation": "Doğru cevap B'dir: Yaralanmanın ilk dakikalarında kanamayı durduran ve geçici matriks görevi gören yapı fibrin pıhtısıdır."},
                    {"key": "C", "text": "Kazeöz nekroz odağı", "isCorrect": False, "explanation": "Kazeöz nekroz tüberkülozda görülen patolojik doku ölümüdür."},
                    {"key": "D", "text": "Miyofibroblast demeti", "isCorrect": False, "explanation": "Miyofibroblastlar ikinci haftada yara kontraksiyonunu sağlar."}
                ]
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-15-s23",
        "title": "Pıhtının İskelet Görevi: Fibronektin ve Geçici Matriks",
        "content": "Oluşan fibrin pıhtısı sadece bir 'tıkaç' değildir; onarım hücreleri için hayati bir 'köprü iskelesi'dir:\n\n- **Geçici Matriks (Provisional Matrix):** Fibrin lifleri, plazma fibronektini ve vitronektinden zengin bu geçici yapı, yara boşluğunu doldurur.\n- **Kılavuz Yollar:** Lökositler, endotel hücreleri ve fibroblastlar boşlukta uçamaz! Bu hücrelerin yara merkezine doğru hareket edebilmesi için integrin reseptörleriyle fibrin ve fibronektin ipliklerine tutunmaları gerekir.\n- **Büyüme Faktörü Deposu (Sınav Spotu):**\n  - Trombositlerin alfa granülleri patladığında yüksek konsantrasyonda **Trombosit Kaynaklı Büyüme Faktörü (PDGF)**, **Transforming Büyüme Faktörü-beta (TGF-β)** ve **FGF** pıhtı içine salınır.\n  - Bu büyüme faktörleri çevre dokulardaki makrofajları ve fibroblastları yaralanma merkezine çeken en güçlü kemotaktik sinyallerdir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sadece Kan Durdurucu Tıkaç vs Biyolojik Kılavuz Geçici Matriks",
                "Mekanik Tıkaç Algısı",
                "Pıhtının sadece kanamayı durduran pasif bir pıhtılaşma kabuğu olduğu düşünülür.",
                "Biyolojik Kılavuz (Geçici Matriks)",
                "Fibronektin ve PDGF/TGF-beta rezervuarı sayesinde lökosit ve fibroblastları alana çeken aktif bir otoyoldur."
            ),
            make_cloze(
                "Yara pıhtısında hücrelerin göçüne kılavuzluk eden ve integrinlerle bağlanan anahtar glikoprotein fibronektindir.",
                "fibronektindir",
                "Geçici matriksteki yapışkan hücre adezyon proteini"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-15-s24",
        "title": "İlk 24 Saat: Akut Enflamasyon ve Nötrofil Dalgası",
        "content": "Pıhtı oluştuktan hemen sonra yaralanma alanına ulaşan ilk savunma ordusu nötrofillerdir (Sınav Spotu):\n\n- **İlk 6 - 24 Saat:** Nötrofiller kandan yara dokusuna masif şekilde ekstravaze olur. 24. saatte yara kenarlarında en baskın hücre tipidir.\n- **Temel Görevleri: 'Saha Temizliği ve Sanitasyon':**\n  - Kesilen deriden giren bakterileri fagositozla öldürmek.\n  - Salgıladıkları elastaz ve proteolitik enzimlerle nekrotik hücre enkazını eritip temizlemek.\n- **Ömürleri Kısadır:** Nötrofiller görevlerini tamamladıktan sonra 24-48 saat içinde hızla apoptoza uğrar ve ölürler.\n- **Klinik Gerçek (Steril Yara Paradoksu):**\n  - Temiz cerrahi insizyonlarda enfeksiyon yoksa nötrofillerin varlığı yara iyileşmesi için mutlak zorunlu değildir; deney hayvanlarında nötrofiller tüketilse dahi yara iyileşebilir.\n  - Ancak makrofajlar yok edilirse yara iyileşmesi **tamamen durur!**",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Cerrahi bir deri kesisinden sonraki ilk 24 saat içinde yara kenarlarında ve pıhtı altında en yoğun görülen iltihabi hücre tipi hangisidir?",
                [
                    {"key": "A", "text": "Plazma hücreleri", "isCorrect": False, "explanation": "Plazma hücreleri kronik enflamasyonda haftalar sonra görülür."},
                    {"key": "B", "text": "Nötrofiller", "isCorrect": True, "explanation": "Doğru cevap B'dir: Akut hasardan sonraki ilk 24 saatte yara yatağını istila eden ilk ve en baskın hücreler nötrofillerdir."},
                    {"key": "C", "text": "Miyofibroblastlar", "isCorrect": False, "explanation": "Miyofibroblastlar 1-2 hafta sonra yara kontraksiyonunda ortaya çıkar."},
                    {"key": "D", "text": "Mast hücreleri", "isCorrect": False, "explanation": "Mast hücreleri ilk dakikalarda degranüle olur ancak yara infiltratını oluşturmaz."}
                ]
            ),
            make_recall(
                "Nötrofil eksikliğinde yara iyileşmesi gecikse de devam edebilirken, makrofaj eksikliğinde yara iyileşmesi neden tamamen çöker?",
                "Çünkü makrofajlar sadece enkaz temizlemez; granülasyon dokusunu, anjiyogenezi ve fibroblast aktivasyonunu yöneten temel büyüme faktörlerini (TGF-beta, VEGF, FGF) üreten orkestra şefidir."
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-15-s25",
        "title": "48–72. Saatler: Monosit Göçü ve Makrofaj Devrimi",
        "content": "Yaralanmanın 48. saatinden itibaren sahne nötrofillerden makrofajlara devredilir; bu onarımın dönüm noktasıdır:\n\n- **Monositlerin Çağrılması:** Kanda dolaşan monositler, trombositlerden ve nötrofillerden salınan kemokinlerin (MCP-1 / CCL2) çekimiyle damar dışına çıkar ve **doku makrofajına** dönüşür.\n- **48 - 72. Saat Baskınlığı (Sınav Spotu):** 48. saatten itibaren yara alanındaki en baskın hücre grubu makrofajlardır.\n- **İki Aşamalı Büyük Misyon:**\n  1. **Enkaz Kaldırma:** Apoptoza gitmiş nötrofilleri, nekrotik hücre artıklarını ve fibrin kalıntılarını yutarak ortamı sterilize etmek.\n  2. **Onarımı Başlatma (Büyüme Faktörü Fabrikası):** Granülasyon dokusunun kurulması için endotel hücrelerini ve fibroblastları uyaran büyüme faktörlerini salgılamak.\n- **Sonuç:** Makrofaj olmadan granülasyon dokusu kurulamaz ve yara iyileşemez.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Monositten Doku Makrofajına Dönüşüm ve Onarım Başlatma",
                [
                    "1. Kemokin Çağrısı: Yara alanından MCP-1 ve fragmanlar kanda monositleri uyarır.",
                    "2. Damar Dışına Göç: Monositler marjinasyon ve transmigrasyonla dokuya sızar.",
                    "3. Doku Makrofajı Olma: Hücre büyür, fagozomlarını ve lizozomlarını genişletir.",
                    "4. Ölü Nötrofilleri Yutma (Eferositoz): Apoptotik nötrofillerin fagositozu onarım genlerini açar.",
                    "5. Büyüme Faktörü Salınımı: VEGF, FGF ve TGF-beta salınarak proliferasyon evresi başlatılır."
                ]
            ),
            make_cloze(
                "Yara iyileşmesinin 48 ve 72. saatlerinden itibaren yara yatağında nötrofillerin yerini alan ve onarımı yöneten temel hücre makrofajdır.",
                "makrofajdır",
                "Doku mononükleer fagositer hücresi"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-15-s26",
        "title": "Makrofaj Polarizasyonu: M1 (Savaşçı) vs M2 (Onarıcı)",
        "content": "Makrofajlar tek tip hücreler değildir; mikroçevrenin sinyallerine göre iki zıt fenotipe bürünürler (Sınav Spotu):\n\n- **1. M1 Makrofajlar (Klasik Aktive - 'Savaşçı ve Yıkıcı'):**\n  - **Uyaran:** Bakteriyel endotoksinler (LPS) ve Th1 sitokini olan İnterferon-gama (IFN-γ).\n  - **İşlevi:** Yüksek oranda iNOS (nitrik oksit sentaz), serbest oksijen radikalleri (ROS) ve pro-enflamatuar sitokinler (IL-1, TNF, IL-6) üretirler. Mikropları öldürür ve doku nekrozunu temizlerler.\n- **2. M2 Makrofajlar (Alternatif Aktive - 'Onarıcı ve Yapıcı'):**\n  - **Uyaran:** Th2 sitokinleri olan **IL-4 ve IL-13**.\n  - **İşlevi:** Enflamasyonu söndürürler (IL-10 ve TGF-β salarlar). Arginaz-1 üzerinden prolin/kollajen sentezini uyarır, anjiyogenezi tetikler ve granülasyon dokusunu kurarlar.\n- **Hayati Geçiş:** Başarılı bir yara iyileşmesinde ilk 24-48 saatte M1 baskınken, 3. günden itibaren **M2 fenotipine geçiş (fenotipik shift)** zorunludur! Geçiş olmazsa yara kronikleşir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "M1 Makrofaj (Klasik / Yangısal) vs M2 Makrofaj (Alternatif / Onarıcı)",
                "M1 Fenotipi (IFN-γ / LPS ile Uyarılır)",
                "Pro-enflamatuardır; ROS, NO, TNF salarak mikropları öldürür ve nekrotik enkazı eritir.",
                "M2 Fenotipi (IL-4 / IL-13 ile Uyarılır)",
                "Anti-enflamatuardır; TGF-beta, VEGF, PDGF salarak anjiyogenezi, kollajen sentezini ve skarı kurar."
            ),
            make_quiz(
                "Doku onarımında enflamasyonu sonlandırıp fibroblast aktivasyonunu ve anjiyogenezi başlatan 'alternatif aktive (M2)' makrofajları uyaran temel sitokinler hangileridir?",
                [
                    {"key": "A", "text": "İnterferon-gama ve TNF-alfa", "isCorrect": False, "explanation": "Bunlar klasik M1 makrofaj yolunu uyarır."},
                    {"key": "B", "text": "IL-4 ve IL-13", "isCorrect": True, "explanation": "Doğru cevap B'dir: Th2 kaynaklı IL-4 ve IL-13 alternatif aktive M2 onarım makrofajlarını indükler."},
                    {"key": "C", "text": "Histamin ve Bradikinin", "isCorrect": False, "explanation": "Vazoaktif mediyatörlerdir."},
                    {"key": "D", "text": "İnterlökin-1 ve İnterlökin-6", "isCorrect": False, "explanation": "Pro-enflamatuar akut faz sitokinleridir."}
                ]
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-15-s27",
        "title": "M2 Makrofajın Salgıladığı Büyüme Faktörleri",
        "content": "M2 makrofajlar, proliferasyon evresindeki tüm hücreleri mobilize eden devasa bir büyüme faktörü fabrikasıdır:\n\n- **1. TGF-β (Transforming Büyüme Faktörü-beta):** Fibroblastları yara yatağına çeker, kollajen sentezini uyarır ve matriks yıkımını durdurur (**en güçlü fibrogenik faktör**).\n- **2. PDGF (Trombosit Kaynaklı Büyüme Faktörü):** Fibroblastların ve düz kas hücrelerinin göçünü ve mitozunu sağlar.\n- **3. VEGF (Vasküler Endotel Büyüme Faktörü):** Damar endotelini uyararak yeni kılcal damar tomurcuklanmasını (anjiyogenezi) başlatır.\n- **4. FGF-2 (Temel Fibroblast Büyüme Faktörü - bFGF):** Hem anjiyogenezi hem de fibroblast proliferasyonunu uyarır.\n- **5. EGF (Epidermal Büyüme Faktörü):** Yüzeydeki keratinositlerin çoğalarak yarayı örtmesini (re-epitelizasyon) tetikler.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Büyüme Faktörü", "Makrofaj Salgısı", "Hedef Hücre", "Temel Biyolojik Yanıt"],
                [
                    ["TGF-beta", "En yüksek oranda", "Fibroblastlar", "Aşırı kollajen üretimi ve fibrozis"],
                    ["VEGF", "Yoğun salgılanır", "Endotel hücreleri", "Yeni kapiller tomurcuklanması"],
                    ["PDGF", "Trombosit + Makrofaj", "Fibroblast / Düz kas", "Hücre göçü ve proliferasyon"],
                    ["FGF-2 (bFGF)", "Makrofaj + Endotel", "Endotel / Fibroblast", "Anjiyogenez ve doku onarımı"],
                    ["EGF", "Makrofaj + Trombosit", "Keratinositler", "Yara yüzeyinin epitel ile kapanması"]
                ]
            ),
            make_cloze(
                "M2 makrofajlar tarafından salgılanan ve yara iyileşmesinde yeni damar oluşumunu uyaran temel faktör vasküler endotel büyüme faktörüdür.",
                "endotel",
                "VEGF kısaltmasındaki damar iç döşemesi kelimesi"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-15-s28",
        "title": "Enflamasyonun Rezolüsyonu ve Skara Geçiş Köprüsü",
        "content": "Onarımın başlayabilmesi için yangının (enflamasyonun) aktif olarak söndürülmesi gerekir; rezolüsyon pasif bir süreç değildir:\n\n- **Aktif Söndürme Mekanizması:** Enflamasyon kendiliğinden sönmez; pro-enflamatuar mediyatörlerin yerini aktif çözücü (pro-resolving) moleküller alır.\n- **Lipid Mediyatör Dönüşümü (Class Switching):** Nötrofil ve makrofajlar lökotrien üretmeyi bırakıp araşidonik asitten **lipoksinler (LXA4, LXB4)**, omega-3 yağ asitlerinden ise **rezolvinler**, **protektinler** ve **maresinler** üretmeye başlar.\n- **Rezolüsyonun Hücresel Etkileri:**\n  - Nötrofil kemotaksisi ve damar geçirgenliği anında kesilir.\n  - Apoptoza giden nötrofiller M2 makrofajlar tarafından temizlenir (eferositoz).\n  - Dokuda anti-enflamatuar sitokinler (IL-10, TGF-β) yükselir.\n- **Patolojik Kural:** Enflamasyon vaktinde sonlanmazsa, doku kronik enflamasyona kayar ve yara iyileşmesi yerine kronik ülser veya aşırı parankimal fibrozis gelişir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Süregelen Yangı (Kronikleşme) vs Zamanında Rezolüsyon",
                "Süregelen Yangı (Kronik Ülser / Doku Yıkımı)",
                "Nötrofiller ve M1 makrofajlar proteaz salmaya devam eder; granülasyon dokusu kurulamaz ve yara kapanmaz.",
                "Zamanında Rezolüsyon (Lipoksin / Rezolvin)",
                "Yangı söndürülür, M2 makrofajlar kontrolü devralır ve fibroblastlar hızla granülasyon dokusunu kurar."
            ),
            make_recall(
                "Akut enflamasyonun sonlanmasını ve onarım evresine geçişi sağlayan aktif lipid aracıları hangileridir?",
                "Lipoksinler (araşidonik asit kaynaklı) ile rezolvinler, protektinler ve maresinlerdir (omega-3 yağ asidi kaynaklı)."
            )
        ]
    })

    # Slide 29 - CHECKPOINT 3
    slides.append({
        "id": "k1-15-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Skarla Onarımın Evreleri ve Hemostaz / Enflamasyon",
        "content": "Bu checkpointte skarla onarımın ilk iki evresini ve hücresel geçişleri pekiştiriyoruz:\n\n- **Dört Evre:** Hemostaz -> Enflamasyon -> Proliferasyon -> Remodeling.\n- **Hemostaz:** Damar vazokonstriksiyonu, trombosit tıkacı ve fibrin pıhtısı oluşumu. Pıhtı hem kanamayı durdurur hem hücre göçü için geçici matriks (fibronektin) sağlar.\n- **İlk 24 Saat:** Nötrofiller yara yatağını istila eder; bakterileri öldürür ve enkazı temizler.\n- **48–72. Saat:** Monositler dokuya sızarak makrofajlara dönüşür ve en baskın hücre haline gelir.\n- **M1 vs M2 Makrofaj:**\n  - M1 (IFN-γ/LPS): Klasik aktive, mikrop öldürücü, yıkıcı, pro-enflamatuar.\n  - M2 (IL-4/IL-13): Alternatif aktive, onarıcı, TGF-β, VEGF ve PDGF salarak granülasyon dokusunu kuran orkestra şefi.\n- **Rezolüsyon:** Lipoksin ve rezolvinlerle yangının söndürülmesi onarımın ön koşuludur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Yaranın İlk 72 Saatlik Hücresel Değişim Kronolojisi",
                [
                    "1. 0. Dakika: Trombositler toplanır ve fibrin pıhtısı yara yatağını örter.",
                    "2. 6 - 24. Saat: Nötrofil akını zirve yapar; fagositoz ve proteolitik temizlik yürütülür.",
                    "3. 24 - 48. Saat: Nötrofiller apoptoza gider; kandan monosit göçü hızlanır.",
                    "4. 48 - 72. Saat: Makrofajlar sahneyi devralır ve M1'den M2 fenotipine geçiş başlar.",
                    "5. 3. Gün ve Sonrası: M2 makrofajlar büyüme faktörleriyle granülasyon dokusunu başlatır."
                ]
            ),
            make_table(
                ["Hücre Türü", "Zirve Yaptığı Zaman", "Tetikleyici Molekül", "Kritik Onarım Rolü"],
                [
                    ["Trombosit", "İlk dakikalar", "Kollajen ve vWF", "Hemostaz ve geçici fibrin iskelesi"],
                    ["Nötrofil", "24. saat", "C5a, LTB4, kemokinler", "Bakteri itlafı ve ilk debridman"],
                    ["M1 Makrofaj", "24 - 48. saat", "IFN-gama, LPS", "Nötrofil enkazını temizleme"],
                    ["M2 Makrofaj", "48 - 72. saat", "IL-4, IL-13", "Büyüme faktörleri salarak onarım"]
                ]
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-15-s30",
        "title": "Mini Vaka: Cerrahi İnsizyonun İlk 3 Günlük Patolojik Takibi",
        "content": "Genel cerrahi servisinde apandisit ameliyatı olan 24 yaşındaki hastanın McBurney insizyonu gün gün takip ediliyor:\n\n- **Ameliyat Anı:** Cerrahi kesi sonrası damarlar hızla pıhtılaşarak fibrin tıkacıyla mühürleniyor; yara dudakları sütürlerle birbirine yaklaştırılıyor.\n- **24. Saat:** Yara kenarlarında hafif eritem izleniyor. Biyopside insizyon hattında nötrofil yoğunluğu izleniyor; epitel bazal tabakası kesi kenarlarından fibrin ağı üzerine doğru göç etmeye başlıyor.\n- **48-72. Saat:** Nötrofiller yerini doku makrofajlarına bırakıyor. Makrofajlar M2 fenotipine dönerek VEGF ve TGF-beta salgılamaya başlıyor.\n- **3. Gün:** Yara tabanında mikroskopik düzeyde ilk anjiyogenez tomurcukları ve fibroblast göçü (granülasyon dokusunun ilk adımları) saptanıyor.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Ameliyatın 48. Saatinde Yara Pansumanı",
                "Hastanın cerrahi pansumanı açıldığında yara kenarlarında hafif kızarıklık görülüyor, ancak akıntı, püy veya yüksek ateş yok. Çömez stajyer 'Hemen yüksek doz intravenöz antibiyotik başlayalım' diyor. Cerrah olarak yaklaşımınız ne olmalıdır?",
                [
                    {
                        "text": "'Haklısın, yara kızardıysa kesinlikle dirençli MRSA enfeksiyonu vardır, üçlü antibiyotik başlayalım.'",
                        "outcome": "Gereksiz ve zararlı antibiyotik kullanımı; normal fizyolojik akut enflamasyon yanlış yorumlanmıştır.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Hayır, bu ameliyatın 48. saatindeki normal fizyolojik enflamatuar ve makrofajik fazdır; püy ve ateş yoksa antibiyotik gerekmez, steril pansumanla izlem yeterlidir.'",
                        "outcome": "Kusursuz cerrahi ve patolojik karar: İyileşmenin doğal enflamatuar evresi doğru teşhis edilir.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Yarayı hemen ameliyathanede tekrar kesip açalım.'",
                        "outcome": "Cerrahi hata ve hastaya zarar.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu cerrahi vakada 3. günden itibaren yara tabanında yeni kılcal damarların tomurcuklanmasını ve fibroblastların çoğalmasını başlatan anahtar hücre grubu hangisidir?",
                [
                    {"key": "A", "text": "M2 fenotipindeki doku makrofajları", "isCorrect": True, "explanation": "Doğru cevap A'dır: 3. günden itibaren M2 makrofajlar salgıladıkları VEGF, FGF ve TGF-beta ile granülasyon dokusunun temelini atar."},
                    {"key": "B", "text": "Apoptoza gitmiş nötrofiller", "isCorrect": False, "explanation": "Apoptotik nötrofiller ölü hücrelerdir, büyüme faktörü salgılamazlar."},
                    {"key": "C", "text": "Kırmızı kan hücreleri (eritrositler)", "isCorrect": False, "explanation": "Eritrositler gaz taşır, onarımı yönetmez."},
                    {"key": "D", "text": "Osteoklastlar", "isCorrect": False, "explanation": "Osteoklastlar kemik yıkan hücrelerdir."}
                ]
            )
        ]
    })

    return slides
