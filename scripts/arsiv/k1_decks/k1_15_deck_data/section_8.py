# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-15-s71",
        "title": "Primer Niyetle İyileşme (İntensiyo Prima / Primary Union)",
        "content": "Cerrahi pratiğin altın standardı olan primer niyetle iyileşme (birincil iyileşme), doku hasarının ve kaybının minimum olduğu durumlarda gerçekleşir:\n\n- **Tanımı ve Koşulları (Sınav Spotu):**\n  - Temiz, enfekte olmamış, cerrahi bir insizyon kesisidir.\n  - Yara kenarları cerrahi sütürler, zımbalar (stapler) veya bantlarla **birbirine sıkıca yaklaştırılmıştır (koapte edilmiştir)**.\n  - Yalnızca fokal bazal membran ve birkaç epitel/bağ dokusu hücresi ölmüştür; doku kaybı yok denecek kadar azdır.\n- **İyileşme Dinamiği:**\n  - İki yara kenarı arasındaki mesafe mikroskopik düzeydedir.\n  - Epitel hücreleri ilk 24-48 saatte karşıdan karşıya hızla geçerek yüzeyi mühürler.\n  - Aradaki dar yarık minimal miktarda granülasyon dokusuyla dolar.\n- **Sonuç:** Çok az skar dokusu oluşur; yara ince, düzgün ve estetik bir çizgi halinde iyileşir. Yara kontraksiyonuna neredeyse hiç ihtiyaç duyulmaz.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Primer İyileşme (Cerrahi Dikiş) vs Sekonder İyileşme (Açık Yara)",
                "Primer İyileşme (Kenarlar Yaklaştırılmış)",
                "Minimum doku kaybı, minimal granülasyon dokusu, neredeyse sıfır kontraksiyon ve incecik çizgi skar.",
                "Sekonder İyileşme (Açık Geniş Defekt)",
                "Geniş doku kaybı, devasa granülasyon dokusu, güçlü miyofibroblast kontraksiyonu ve kaba geniş skar."
            ),
            make_cloze(
                "Temiz ve kenarları sütürlerle birbirine yaklaştırılmış cerrahi bir insizyonun iyileşmesine primer niyetle iyileşme denir.",
                "primer",
                "Birincil cerrahi iyileşme tipi adı"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-15-s72",
        "title": "Primer İyileşmenin 24 Saatten 1. Aya Kronolojisi",
        "content": "Temiz bir cerrahi kesinin gün gün histopatolojik takibi patolojinin en kusursuz saat mekanizmalarından biridir (Sınav Sorusu):\n\n- **İlk 24 Saat:** Kesi hattı fibrin pıhtısıyla dolar; nötrofiller insizyon sınırlarına göç eder. Epidermis bazal hücreleri kesi kenarlarından fibrin altına doğru göç etmeye başlar.\n- **24 - 48. Saat (İki Gün):** İki taraftan gelen epitel hücreleri ortada birleşir (re-epitelizasyon tamamlanır, temas inhibisyonu).\n- **3. Gün:** Nötrofillerin yerini makrofajlar alır. Granülasyon dokusu insizyon boşluğuna sızar; ilk ince Tip III kollajen lifleri görülür.\n- **5. Gün:** Granülasyon dokusu insizyon aralığını tamamen doldurur; anjiyogenez zirvededir. Epidermis kalınlaşarak normal katmanlarına kavuşur.\n- **2. Hafta:** Kollajen birikimi devam eder; damarlar ve ödem gerilemeye başlar.\n- **1. Ay:** Yara tamamen avasküler, asellüler, Tip I kollajenden zengin ve üzeri normal epidermis ile örtülü ince bir skar dokusuna dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Primer Cerrahi Yara İyileşmesinin Kronolojik Akışı",
                [
                    "1. 24. Saat: Nötrofil infiltrasyonu ve bazal epitel hücrelerinin göç başlangıcı.",
                    "2. 48. Saat: Epitel hücrelerinin yara ortasında birleşerek yüzeyi kapatması.",
                    "3. 3. Gün: Makrofajların sahneye çıkması ve granülasyon dokusu tomurcuklanması.",
                    "4. 5. Gün: Anjiyogenezin zirveye ulaşması ve insizyon boşluğunun dolması.",
                    "5. 2. Hafta: Kollajen demetlerinin artması, ödemin ve kılcalların gerilemesi."
                ]
            ),
            make_quiz(
                "Temiz, kenarları yaklaştırılmış cerrahi bir insizyonda re-epitelizasyonun (epitel hücrelerinin yara ortasında birleşerek yüzeyi kapatması) genellikle tamamlandığı zaman dilimi hangisidir?",
                [
                    {"key": "A", "text": "İlk 24 ila 48 saat içinde", "isCorrect": True, "explanation": "Doğru cevap A'dır: Primer iyileşmede kesi kenarları birbirine çok yakın olduğu için epitel hücreleri 24-48 saat içinde karşıdan karşıya geçerek yüzeyi mühürler."},
                    {"key": "B", "text": "2. ayın sonunda", "isCorrect": False, "explanation": "2. ayda remodeling sürer, epitelizasyon çoktan bitmiştir."},
                    {"key": "C", "text": "6. saatte", "isCorrect": False, "explanation": "6. saatte henüz nötrofiller yeni göç etmektedir."},
                    {"key": "D", "text": "1. yılda", "isCorrect": False, "explanation": "Bu kadar uzun sürmez."}
                ]
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-15-s73",
        "title": "Sekonder Niyetle İyileşme (İntensiyo Sekunda / Secondary Union)",
        "content": "Doku kaybının büyük olduğu, yara dudaklarının birleştirilemediği veya enfekte yaralarda sekonder iyileşme devreye girer:\n\n- **Hangi Durumlarda Görülür? (Sınav Spotu):**\n  - Geniş cilt yanıkları ve travmatik ezilme yaralanmaları.\n  - Bacak ve bası ülserleri (dekübitus ülseri).\n  - İçi boşaltılmış geniş apse kaviteleri veya enfekte cerrahi yaralar.\n  - Miyokard enfarktüsü veya organ enfarktüsleri.\n- **Sekonder İyileşmenin Temel Biyolojisi:**\n  - Doku kaybı çok büyüktür; yara kenarları açık kalır.\n  - Ortamda devasa miktarda nekrotik enkaz, fibrin ve iltihabi eksuda vardır; temizlenmesi günler sürer.\n  - Bu devasa kraterin kapanabilmesi için **çok büyük miktarda granülasyon dokusunun** alttan yukarıya doğru yavaş yavaş üremesi gerekir.\n- **Sonuç:** Skar kaçınılmaz olarak geniş, çökük veya kabarık, düzensiz ve belirgindir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Klinik Durum", "İyileşme Tipi", "Granülasyon Dokusu Miktarı", "Skarın Özelliği"],
                [
                    ["Temiz Apandisit Kesisı", "Primer İyileşme", "Minimal (dar bir çizgi)", "İncecik estetik skar"],
                    ["Bası Ülseri (Dekübit)", "Sekonder İyileşme", "Çok yoğun (krateri doldurur)", "Geniş, çökük fibröz skar"],
                    ["Derin Kaynar Su Yanığı", "Sekonder İyileşme", "Masif granülasyon yatağı", "Kontraktür ve geniş skar riski"],
                    ["Drene Edilmiş Karaciğer Apsesi", "Sekonder İyileşme", "Boşluğu dolduran bağ dokusu", "Parankimal fibröz skar"]
                ]
            ),
            make_cloze(
                "Geniş doku kaybı olan, enfekte veya kenarları yaklaştırılamayan açık yaraların granülasyonla dolmasına sekonder niyetle iyileşme denir.",
                "sekonder",
                "İkincil açık yara iyileşme tipi adı"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-15-s74",
        "title": "Primer ve Sekonder İyileşme Arasındaki Üç Temel Fark",
        "content": "Sekonder iyileşmeyi primer iyileşmeden ayıran ve patoloji sınavlarında mutlaka sorulan 3 majör biyolojik fark şunlardır (Sınavların Klasiği):\n\n- **1. Enflamatuar Reaksiyonun Şiddeti ve Süresi:**\n  - Sekonder iyileşmede doku kaybı ve nekroz çok daha fazla olduğu için nötrofil ve makrofaj akını katbekat büyüktür; enflamasyon haftalarca sürebilir.\n- **2. Granülasyon Dokusunun Miktarı:**\n  - Primer iyileşmede dar bir aralık doldurulurken; sekonder iyileşmede devasa bir krater tabandan tavana kadar doldurulmak zorundadır. Bu nedenle granülasyon dokusu çok daha bol miktarda üretilir.\n- **3. Yara Kontraksiyonu (Miyofibroblastların Rolü - En Kritik Fark):**\n  - Primer iyileşmede yara kenarları zaten dikişle birleştirildiği için kontraksiyon önemsizdir.\n  - Sekonder iyileşmede ise yara tabanındaki **miyofibroblastlar** güçlü bir şekilde kasılarak açık yara yüzeyini **%70-80 oranında büzüştürür**.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Primer İyileşme vs Sekonder İyileşme (3 Temel Fark)",
                "Primer İyileşme (Dikişli / Temiz)",
                "Hafif enflamasyon, minimal granülasyon dokusu, neredeyse sıfır yara kontraksiyonu.",
                "Sekonder İyileşme (Açık / Defektli)",
                "Şiddetli ve uzun enflamasyon, devasa granülasyon dokusu ve belirgin (%70-80) miyofibroblast kontraksiyonu."
            ),
            make_quiz(
                "Aşağıdakilerden hangisi sekonder niyetle iyileşmeyi primer niyetle iyileşmeden ayıran en karakteristik özelliklerden biridir?",
                [
                    {"key": "A", "text": "Sekonder iyileşmede hiçbir zaman fibroblastların çoğalmaması", "isCorrect": False, "explanation": "Sekonder iyileşmede fibroblastlar çok daha yoğun prolifere olur."},
                    {"key": "B", "text": "Miyofibroblastlar aracılığıyla belirgin yara kontraksiyonunun (büzülmesinin) görülmesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Sekonder iyileşmenin en ayırt edici mekanizması, açık yara alanını küçültmek için gerçekleşen belirgin yara kontraksiyonudur."},
                    {"key": "C", "text": "Sekonder iyileşmenin daima 24 saatte tamamlanması", "isCorrect": False, "explanation": "Sekonder iyileşme haftalar ve aylar sürer."},
                    {"key": "D", "text": "Sekonder iyileşmede hiç kollajen sentezlenmemesi", "isCorrect": False, "explanation": "Aksine devasa miktarda kollajen sentezlenir."}
                ]
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-15-s75",
        "title": "Tersiyer İyileşme (Gecikmiş Primer Kapatma / Delayed Primary Closure)",
        "content": "Askeri cerrahi, travma ve acil cerrahide hayat kurtaran üçüncü bir onarım stratejisi vardır: **Tersiyer İyileşme**:\n\n- **Tanımı ve Gerekçesi (Sınav Spotu):**\n  - Ağır kontamine olmuş, kirli, toprak bulaşmış savaş/trafik yaraları veya patlamış apandisit peritoniti durumlarında **yara hemen kapatılmaz!**\n  - Yara hemen dikilirse içeride kalan anaerobik bakteriler kapalı alanda çoğalarak flegmon, apse veya gazlı kangrene yol açar.\n- **Klinik Protokol Adımları:**\n  1. Yara debride edilir, yıkanır ve **4 ila 7 gün boyunca açık bırakılarak** steril pansumanlarla takip edilir.\n  2. Bu sürede yara tabanında sağlıklı granülasyon dokusu oluşur, enfeksiyon temizlenir ve lökositler bakterileri yok eder.\n  3. Yara temizlendiğinde (3-7. günlerde), cerrah yara dudaklarını ameliyathanede dikişlerle **gecikmiş olarak kapatır (delayed primary closure)**.\n- **Sonuç:** Enfeksiyon riski ortadan kaldırılırken, sekonder iyileşmenin yaratacağı devasa kaba skar yerine kontrollü bir primer skar elde edilir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Tersiyer (Gecikmiş Primer) İyileşme Protokolü",
                [
                    "1. İlk Müdahale: Kontamine yara yıkanır, ölü dokular temizlenir ancak yara dikilmez.",
                    "2. Açık Takip (3-5 Gün): Islak pansumanlarla granülasyon dokusunun tabanda belirmesi beklenir.",
                    "3. Enfeksiyon Kontrolü: Yara kültürleri negatifleşir ve bakteriyel yük düşer.",
                    "4. Cerrahi Kapatma: Temizlenen yara kenarları ameliyathanede sütürlerle birleştirilir.",
                    "5. Güvenli İyileşme: Derin apse riski önlenerek estetik ve fonksiyonel kapatma sağlanır."
                ]
            ),
            make_cloze(
                "Enfeksiyon riski yüksek kirli yaraların önce açık bırakılıp granülasyon oluştuktan sonra dikişle kapatılmasına tersiyer iyileşme denir.",
                "tersiyer",
                "Gecikmiş primer iyileşmenin diğer adı"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-15-s76",
        "title": "Üç İyileşme Tipinin Karşılaştırmalı Matrisi",
        "content": "Klinik pratikte bir yarayı değerlendirirken bu üç stratejinin parametrelerini net bir matrisle bilmek gerekir:\n\n- **Doku Kaybı:** Primerde minimal; Sekonderde çok geniş; Tersiyerde orta/geniş.\n- **Enfeksiyon Durumu:** Primerde kesinlikle steril/temiz; Sekonderde sıklıkla kontamine/enfekte; Tersiyerde başlangıçta kirli/enfekte, sonradan steril.\n- **Granülasyon İhtiyacı:** Primerde çok az; Sekonderde devasa; Tersiyerde orta düzeyde.\n- **Yara Kontraksiyonu:** Primerde yok; Sekonderde çok belirgin (%70-80); Tersiyerde kısmi.\n- **İyileşme Süresi:** Primerde hızlı (7-14 gün); Sekonderde çok yavaş (aylar); Tersiyerde orta (2-4 hafta).\n- **Skar Kalitesi:** Primerde ince lineer estetik; Sekonderde geniş ve biçimsiz; Tersiyerde kabul edilebilir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Primer İyileşme", "Sekonder İyileşme", "Tersiyer İyileşme"],
                [
                    ["Yara Kenarları", "Sütürle yaklaştırılmış", "Açık ve birbirinden uzak", "Önce açık, 4-5 gün sonra dikişli"],
                    ["Doku Kaybı", "Çok az (minimal)", "Çok geniş ve derin", "Değişken (kontamine/nekrotik)"],
                    ["Granülasyon Dokusu", "Çok az (dar yarıkta)", "Devasa (krateri doldurur)", "Orta düzeyde (tabanda sağlıklı)"],
                    ["Yara Kontraksiyonu", "Neredeyse hiç yok", "Çok belirgin (%70-80)", "Kısmen var"],
                    ["Nihai Skar", "İnce, estetik çizgi", "Geniş, kaba, düzensiz", "Orta derecede estetik çizgi"]
                ]
            ),
            make_recall(
                "Hangi klinik durumlarda cerrah yaranın primer kapatılmasından kesinlikle kaçınmalı ve sekonder veya tersiyer iyileşmeyi seçmelidir?",
                "Yara enfekte ise, yoğun yabancı cisim ve toprak bulaşı varsa, üzerinden 8-12 saatten fazla zaman geçmiş kirli travmatik yaralanmalarda primer kapatma yapılmamalıdır."
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-15-s77",
        "title": "Miyofibroblast Kontraksiyonunun Biyomekaniği",
        "content": "Sekonder iyileşmede açık yarayı büzüştürerek kapatan miyofibroblastların kasılma biyomekaniği kendine özgüdür:\n\n- **Fibroblasttan Miyofibroblasta Dönüşüm:**\n  - Yara tabanında yüksek konsantrasyonda bulunan **TGF-β** ve mekanik gerilim sinyalleri, fibroblastların DNA'sında **alfa-düz kas aktini (α-SMA)** genini açar.\n- **Fibronektin 'Bağlantı Plakları' (Fibronexus):**\n  - Miyofibroblastın içindeki aktin mikroflamanları, hücre zarındaki integrinler üzerinden dışarıdaki fibronektin ve kollajen liflerine bağlanır.\n  - Bu özelleşmiş hücre-matriks bağlantısına **fibroneksus** denir.\n- **Adım Adım Büzüşme:**\n  - Miyofibroblastlar kasıldığında bu mekanik güç kollajen liflerine aktarılır.\n  - Hücreler gevşediğinde geriye kaymazlar; matriks yeni pozisyonunda MMP ve TIMP dengesiyle yeniden sabitlenir.\n  - Bu cırcır (ratchet) mekanizmasıyla açık yara defekti her gün milimetre milimetre küçülür.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Miyofibroblast Kasılma ve Yara Büzülme Döngüsü",
                [
                    "1. α-SMA İndüksiyonu: TGF-beta etkisiyle fibroblast aktin flamanlarıyla donanır.",
                    "2. Fibroneksus Bağlantısı: Hücre içi aktin, integrinler üzerinden dış kollajene kenetlenir.",
                    "3. Kasılma Hamlesi: Aktin-miyozin kaymasıyla hücre kollajen liflerini kendine çeker.",
                    "4. Kollajen Yeniden Sabitlenmesi: Matriks yeni daralmış pozisyonunda çapraz bağlanır.",
                    "5. Defektin Küçülmesi: Yara yüzey alanı her gün küçülerek re-epitelizasyona zemin hazırlar."
                ]
            ),
            make_cloze(
                "Miyofibroblastların hücre içi aktin flamanlarını dış ortamdaki kollajene bağlayan özel integrin yapısına fibroneksus denir.",
                "fibroneksus",
                "Hücre-matriks kasılma köprüsü adı"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-15-s78",
        "title": "Açık Yara Bakımında Negatif Basınçlı Yara Tedavisi (NPWT / VAC)",
        "content": "Modern cerrahi ve doku onarımında sekonder iyileşmeyi hızlandıran en büyük biyomühendislik devrimlerinden biri **Vakum Yardımlı Kapama (VAC / NPWT)** yöntemidir:\n\n- **Çalışma Prensibi (Sınav Spotu):**\n  - Açık yara yatağına steril poliüretan sünger yerleştirilir ve üzeri hava geçirmez şeffaf filmle örtülür.\n  - Bir pompa aracılığıyla yaraya kontrollü **negatif basınç (-125 mmHg)** uygulanır.\n- **Doku Onarımını Nasıl Hızlandırır?**\n  1. **Mikrodeformasyon:** Süngerin gözenekleri yara tabanındaki hücreleri mekanik olarak gerer; bu gerilim integrinleri uyararak **hücre proliferasyonunu ve anjiyogenezi 3-4 kat artırır**.\n  2. **Ödem ve Eksuda Drenajı:** Doku aralığındaki proteaz dolu aşırı sıvıyı emerek kompresyonu ve kompartıman basıncını düşürür; mikrosirkülasyonu rahatlatır.\n  3. **Bakteriyel Yükün Azalması:** Yaranın steril ve kapalı kalmasını sağlar.\n- **Sonuç:** Normalde 2 ayda dolmayacak devasa yara boşlukları 1-2 haftada sağlıklı pembe granülasyon dokusuyla kaplanır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Geleneksel Islak Gazlı Bez Pansumanı vs Negatif Basınçlı Tedavi (VAC)",
                "Klasik Pansuman (Pasif)",
                "Yara ödemli kalır, bakteriler birikir, granülasyon dokusu çok yavaş ve zayıf gelişir.",
                "Negatif Basınç / VAC (Aktif Biyomekanik)",
                "Ödem emilir, mekanik gerilimle granülasyon dokusu fışkırır ve yara hızla küçülür."
            ),
            make_quiz(
                "Geniş doku kaybı olan açık yaralarda negatif basınçlı yara tedavisinin (VAC) granülasyon dokusu oluşumunu hızlandırmasındaki temel mekanizma nedir?",
                [
                    {"key": "A", "text": "Hücrelerde mekanik deformasyon ve gerilim yaratarak anjiyogenezi ve mitozu uyarmak, doku ödemini azaltmak", "isCorrect": True, "explanation": "Doğru cevap A'dır: NPWT/VAC mikrodeformasyon ile hücre bölünmesini ve damarlanmayı uyarırken, aşırı ödem ve eksudayı drene eder."},
                    {"key": "B", "text": "Yaraya doğrudan saf oksijen gazı basarak bakterileri yakmak", "isCorrect": False, "explanation": "VAC oksijen basmaz, negatif vakum uygular."},
                    {"key": "C", "text": "Deri kök hücrelerini tamamen yok etmek", "isCorrect": False, "explanation": "Kök hücreleri yok etmez, çoğalmasını uyarır."},
                    {"key": "D", "text": "Yaranın sıcaklığını 45 dereceye çıkarmak", "isCorrect": False, "explanation": "Termal bir tedavi değildir."}
                ]
            )
        ]
    })

    # Slide 79 - CHECKPOINT 8
    slides.append({
        "id": "k1-15-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Primer, Sekonder ve Tersiyer Yara İyileşmesi",
        "content": "Bu checkpointte üç cerrahi onarım biçimini ve biyolojik mekanizmalarını pekiştiriyoruz:\n\n- **Primer İyileşme:** Temiz, kenarları sütürle yaklaştırılmış kesi. Minimal doku kaybı, minimal granülasyon, hızlı re-epitelizasyon (24-48 saat), neredeyse sıfır kontraksiyon, ince estetik çizgi skar.\n- **Sekonder İyileşme:** Geniş doku kaybı, açık yara, ülser/yanık/apse. Yoğun nekroz ve uzun enflamasyon, devasa granülasyon dokusu, **belirgin miyofibroblast yara kontraksiyonu (%70-80)**, geniş kaba skar.\n- **Tersiyer İyileşme (Gecikmiş Primer):** Kontamine/kirli yaranın önce 3-5 gün açık bırakılıp granülasyon ve enfeksiyon kontrolü sağlandıktan sonra cerrahi olarak dikilmesi.\n- **Miyofibroblastlar:** α-SMA içeren ve fibroneksusla kollajene tutunup kasılan onarım hücreleri.\n- **VAC / NPWT:** Negatif basınçla ödemi azaltıp granülasyonu patlatan biyomekanik yara bakım yöntemi.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İyileşme Türü", "Klinik Örnek", "Yara Kontraksiyonu", "Granülasyon Miktarı"],
                [
                    ["Primer", "Temiz cerrahi dikiş", "Yok denecek kadar az", "Minimal"],
                    ["Sekonder", "Dekübit ülseri, geniş yanık", "Çok belirgin (%70-80)", "Devasa"],
                    ["Tersiyer", "Kirli travma yarası (gecikmiş sütür)", "Kısmi", "Orta"]
                ]
            ),
            make_chain(
                "Yaranın Durumuna Göre Cerrahi Karar Akışı",
                [
                    "1. Yaranın Değerlendirilmesi: Temiz cerrahi kesi ise hemen primer dikilir.",
                    "2. Kontamine/Kirli İse: Enfeksiyon riski varsa primer kapatılmaz, yara açık tutulur.",
                    "3. Granülasyon Gelişimi: Taban temizlenip sağlıklı granülasyon çıkınca 4. günde dikilir (tersiyer).",
                    "4. Kapatılamayacak Kadar Genişse: Sekonder iyileşmeye bırakılır veya greftlenir."
                ]
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-15-s80",
        "title": "Mini Vaka: Perfore Apandisitte Cerrahi Kapatma Kararı",
        "content": "Akut apandisiti patlamış (perfore) ve batın içi yoğun püy ile kaplı 35 yaşındaki hastaya acil apandektomi yapılıyor:\n\n- **Ameliyat Sonu İkilemi:** Cerrah peritonu ve fasyayı dikiyor; ancak cilt ve cilt altı dokuda yoğun dışkı ve püy bulaşı bulunuyor.\n- **Hatalı Seçenek (Primer Kapama):** Eğer cilt hemen sıkıca dikilirse, 3 gün sonra dikişlerin altında devasa bir yara apsesi gelişecek, dikişler patlayacak ve yara dehisensi oluşacaktır.\n- **Doğru Cerrahi Karar (Tersiyer Kapama / Gecikmiş Primer):**\n  - Cerrah cilt ve cilt altını açık bırakıyor; yara içine serum fizyolojikli ıslak gazlı bez yerleştiriyor.\n  - 4 gün boyunca pansuman yapılıyor; antibiyotikle sistemik enfeksiyon geriliyor ve yara tabanında tertemiz, kırmızı granülasyon dokusu beliriyor.\n  - 5. günde hasta pansuman odasında lokal anesteziyle dikişleri atılarak gecikmiş primer (tersiyer) olarak kapatılıyor.\n- **Sonuç:** Hasta apse komplikasyonu yaşamadan, minimum skar ile sorunsuz iyileşiyor.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Perfore Kirli Karın Kesisine Yaklaşım",
                "Patlamış apandisit ameliyatında asistan cerrah 'Hocam cildi hemen dikip kapatalım, hasta taburcu olsun' diyor. Kıdemli uzman cerrahın patofizyolojik gerekçeyle vermesi gereken en doğru karar nedir?",
                [
                    {
                        "text": "'Haklısın, yara ne kadar kirli olursa olsun hemen dikilmelidir.'",
                        "outcome": "Ağır cerrahi komplikasyon: 3 gün sonra yara içi apseyle patlar ve nekrotizan fasiit gelişebilir.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Hayır, bu yara ağır kontaminedir; cildi kapatırsak yara apsesi gelişir. Fasyayı kapatıp cildi açık bırakacağız; 4 gün sonra temiz granülasyon dokusu oluşunca gecikmiş primer (tersiyer) kapatacağız.'",
                        "outcome": "Kusursuz cerrahi ve patolojik karar: Enfeksiyon önlenir, güvenli onarım sağlanır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Cildi açık bırakıp bir daha ömür boyu hiç dikmeyelim.'",
                        "outcome": "Gereksiz yere sekonder iyileşmeye bırakarak hastayı aylarca açık yarayla yaşatmak.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu perfore apandisit vakasında cerrahın cildi hemen dikmeyip 4 gün sonra temiz granülasyon gelişince kapatması hangi iyileşme türünün klasik örneğidir?",
                [
                    {"key": "A", "text": "Tersiyer niyetle iyileşme (Gecikmiş primer kapama)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kirli yaranın enfeksiyon geçene kadar açık bırakılıp birkaç gün sonra dikilmesi tersiyer iyileşmedir."},
                    {"key": "B", "text": "Morfogenetik uzuv rejenerasyonu", "isCorrect": False, "explanation": "Uzuv çıkmasıyla ilgisi yoktur."},
                    {"key": "C", "text": "Yalnızca kemik iliği hematopoezi", "isCorrect": False, "explanation": "Konuyla ilgisi yoktur."},
                    {"key": "D", "text": "Primer niyetle anında kapatma", "isCorrect": False, "explanation": "Anında kapatılmamıştır."}
                ]
            )
        ]
    })

    return slides
