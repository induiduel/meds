#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/enrich_spot_pearls_structure.py
Upgrades all spotPearls in 'learn-enflamasyon-kimyasal-mediyatorleri' to multi-tier structured format:
- Üst madde & alt madde (indented sub-bullets)
- 🔴 Kırmızı (Önemli / Kritik / Hayati)
- 🔵 Mavi (Sorulmuş / Çıkmış Komite & TUS Sınav Sorusu)
- Bold, italic, and marker highlights (==vurgu==)
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

deck_idx = next((i for i, d in enumerate(decks) if d.get('id') == 'learn-enflamasyon-kimyasal-mediyatorleri'), -1)
if deck_idx < 0:
    print("Error: Deck not found.")
    sys.exit(1)

deck = decks[deck_idx]

# Structured spot pearls for each of the 22 slides
structured_spots = {
    1: [
        "🔴 **Önemli (Kritik İlke):** Mediyatörlerin Biyolojik Ömrü ve Hasar Potansiyeli\n  • **Üst Madde: Kısa Yarı Ömür**\n    - *Mekanizma:* Çoğu mediyatör saniyeler veya dakikalar içinde enzimatik yıkıma uğrar.\n    - *Fizyolojik Amaç:* Yangının çevre sağlam dokulara taşmasını önlemek ve kendi kendini sınırlamasını sağlamak.\n  • **Üst Madde: Doku Hasarı Riski**\n    - *Patoloji:* Mediyatörlerin ==aşırı veya kontrolsüz üretimi== septik şok ve otoimmün hasarın primer nedenidir.",
        "🔵 **Çıkmış Soru (Komite & TUS):** Plazma Kaynaklı Mediyatörlerin Sentez Fabrikası\n  • **Soru:** \"Enflamasyonun plazma kaynaklı mediyatörleri (kompleman, kinin, pıhtılaşma faktörleri) nerede sentezlenir?\"\n    - *Doğru Cevap:* ==Karaciğer== (Hepatositler tarafından inaktif zimojen olarak dolaşıma verilirler).\n    - *Tuzak:* Trombosit veya mast hücresi değil; plazma proteinlerinin ana kaynağı daima karaciğerdir.",
        "⚡ **Spot Sentez:** Hücre kaynaklı mediyatörlerin salınım formları:\n  • **Önceden Depolanmış:** Mast hücre granüllerinde hazır bekleyen ==Histamin==.\n  • **De Novo (Yeni) Sentezlenen:** Yangı uyarısıyla üretilen ==Prostaglandinler, Lökotrienler ve Sitokinler==."
    ],
    2: [
        "🔴 **Önemli (Vasküler Patoloji):** Histaminin Mikrosirkülasyon Üzerindeki Seçici Etkileri\n  • **Üst Madde: Damar Yatağına Göre Zıt Yanıt**\n    - *Arterioller:* Düz kas gevşemesi ile ==Vazodilatasyon== yapar (rubor ve calor).\n    - *Postkapiller Venüller:* Endotel kasılması (kontraksiyon) ile ==Vasküler Geçirgenlik Artışı== yapar (ödem / tumor).\n  • **Üst Madde: Süre Kısıtı**\n    - *Karakter:* 'Erken geçici yanıt' olarak bilinir, 15-30 dakika içinde sonlanır.",
        "🔵 **Çıkmış Soru (Komite):** Mast Hücresi Degranülasyonunu Tetikleyen Kompleman Ajanları\n  • **Soru:** \"Tip 1 aşırı duyarlılık dışında mast hücrelerinden histamin degranülasyonunu tetikleyen en güçlü kompleman anafilatoksinleri hangileridir?\"\n    - *Doğru Cevap:* ==C3a ve C5a== (özellikle C5a).\n    - *Sınav Tuzağı:* C3b opsonindir, degranülasyon tetiklemez; anafilatoksin olanlar 'a' fragmanlarıdır (C3a, C5a).",
        "⚡ **Spot Klinik:** Histaminin yangısal vasküler etkileri ==H1 histamin reseptörleri== aracılığıyla yürütülür; klasik antihistaminikler H1 reseptörlerini bloke ederek ödem ve ürtikeri engeller."
    ],
    3: [
        "🔴 **Önemli (Tür Ayrımı):** İnsanda Serotonin Kaynağı ve Vasküler Etkisi\n  • **Üst Madde: İnsandaki Depolanma Yeri**\n    - *Doğru Hücre:* Dolaşımdaki ==Trombositlerin yoğun (delta) granülleri== ve GIS enterokromaffin hücreleri.\n    - *Patoloji Uyarısı:* Kemirgenlerin aksine, insanda mast hücrelerinde serotonin bulunmaz!\n  • **Üst Madde: Vasküler Tonus**\n    - *Etki:* Histamin vazodilatatör iken, serotonin temelde ==Vazokonstriktördür== (hemostazı destekler).",
        "🔵 **Çıkmış Soru (TUS):** Trombosit Yoğun Granül İçeriği ve Vazoaktif Amin\n  • **Soru:** \"Trombosit agregasyonu sırasında yoğun granüllerden salınarak hemostatik vazokonstriksiyonu başlatan vazoaktif amin hangisidir?\"\n    - *Doğru Cevap:* ==Serotonin (5-HT)==.\n    - *Klinik İlgi:* Karsinoid tümörlerde aşırı salınarak flushing, ishal ve sağ kalp kapak fibrozu yapar.",
        "⚡ **Spot Bilgi:** Trombosit agregasyonunda serotonin vazokonstriksiyon yaparak kan kaybını azaltırken lökosit-endotel temasını artırır."
    ],
    4: [
        "🔴 **Önemli (Kritik Hız Kısıtlayıcı Basamak):** Fosfolipaz A2 ve Steroid Engeli\n  • **Üst Madde: Eikozanoidlerin Çıkış Noktası**\n    - *Substrat:* Hücre zarı fosfolipidlerinden 20 karbonlu serbest ==Araşidonik Asit== koparılmasıdır.\n    - *Ana Enzim:* ==Fosfolipaz A2 (PLA2)== kalsiyuma bağımlı olarak aktive olur.\n  • **Üst Madde: Kortikosteroidlerin Kökten İnhibisyonu**\n    - *Mekanizma:* Glukokortikoidler ==Anneksin A1 (Lipokortin-1)== sentezini indükleyerek PLA2'yi durdurur.\n    - *Klinik Sonuç:* Hem prostaglandinler hem lökotrienler aynı anda bloke edilir.",
        "🔵 **Çıkmış Soru (Komite & Farmakoloji):** Kortikosteroidlerin Çift Yollu Blokajı\n  • **Soru:** \"Kortikosteroidlerin hem siklooksijenaz hem de lipoksijenaz ürünlerinin sentezini eş zamanlı baskılayabilmesinin temel sebebi nedir?\"\n    - *Doğru Cevap:* ==Anneksin A1 (Lipokortin) ile Fosfolipaz A2 enziminin inhibe edilmesidir==.\n    - *Çeldirici:* 5-LOX veya COX'un direkt inhibisyonu değildir; en üst basamak olan araşidonik asit salınımını keserler.",
        "⚡ **Spot Sentez:** Tüm eikozanoidler sinyal iletiminde ==G-protein kenetli reseptörleri (GPCR)== kullanır."
    ],
    5: [
        "🔴 **Önemli (Tromboz Tuzağı):** Selektif COX-2 İnhibitörleri Neden Tromboz Yapar?\n  • **Üst Madde: İzoenzimlerin Görev Dağılımı**\n    - *COX-1 (Yapısal/Konstitütif):* Mide mukozasını korur, böbrek perfüzyonunu sağlar, trombositte TXA2 üretir.\n    - *COX-2 (İndüklenebilir):* Yangı odağında sitokinlerle (IL-1, TNF) uyarılır, endotelde PGI2 üretir.\n  • **Üst Madde: Selektif COX-2 Blokajının Tehlikesi**\n    - *Mekanizma:* Endoteldeki antitrombotik ==PGI2 sentezi kesilir==; ancak trombositteki COX-1'e dokunulmadığı için ==TXA2 aynen kalır==.\n    - *Sonuç:* PGI2/TXA2 dengesi protrombotik TXA2 yönüne kayar; ==MI ve İnme riski== belirgin artar!",
        "🔵 **Çıkmış Soru (Patoloji & Farmakoloji):** Konstitütif vs. İndüklenebilir Enzim\n  • **Soru:** \"İnflamatuar sitokinler (IL-1, TNF) ve bakteriyel endotoksin tarafından dokularda süratle indüklenen siklooksijenaz izoformu hangisidir?\"\n    - *Doğru Cevap:* ==Siklooksijenaz-2 (COX-2)==.\n    - *Tuzak:* COX-1 konstitütiftir; bazal fizyolojik homeostazı korur.",
        "⚡ **Spot Klinik:** Non-selektif NSAİİ'ların (Aspirin, İbuprofen) peptik ülser yapma nedeni mide koruyucu ==COX-1 enzimini== inhibe etmeleridir."
    ],
    6: [
        "🔴 **Önemli (Patofizyoloji):** PGE2 ve PGD2 Arasındaki Klinik Ayrım\n  • **Üst Madde: Prostaglandin E2 (PGE2) - Ateş ve Hiperaljezi**\n    - *Ateş:* Hipotalamusta cAMP'yi artırarak sıcaklık termostat ayar noktasını yükseltir.\n    - *Ağrı:* Tek başına ağrı yapmaz; nosiseptörleri bradikinin ve histamin gibi ağrı yapıcı ajanlara ==duyarlı kılar (hiperaljezi)==.\n  • **Üst Madde: Prostaglandin D2 (PGD2) - Mast Hücre İmzası**\n    - *Kaynak:* Dokudaki ==mast hücrelerinin temel COX ürünüdür==.\n    - *Etki:* Vazodilatasyon ve ödeme yol açar, nötrofilleri yangı odağına çeker.",
        "🔵 **Çıkmış Soru (Komite Sınavı):** Ateş Patogenezinde Hipotalamik Mediyatör\n  • **Soru:** \"Endojen pirojenler (IL-1, TNF) etkisiyle hipotalamusta sentezlenerek termoregülasyon ayar noktasını yükselten eikozanoid hangisidir?\"\n    - *Doğru Cevap:* ==Prostaglandin E2 (PGE2)==.\n    - *İlaç Etkisi:* Parasetamol ve aspirin hipotalamusta PGE2 sentezini keserek antipiretik etki gösterir.",
        "⚡ **Spot Sentez:** Prostaglandinler (PGI2, PGE2, PGD2) genel olarak ==güçlü vazodilatatördür== ve diğer mediyatörlerin ödem yapıcı etkisini potansiyalize eder."
    ],
    7: [
        "🔴 **Önemli (Damar İçi Denge):** PGI2 vs. TXA2 Zıt Kardeşler Matrisi\n  • **Üst Madde: Prostasiklin (PGI2 - Endotel Dostu)**\n    - *Vasküler Etki:* ==Vazodilatasyon== yapar.\n    - *Trombosit Etkisi:* ==Agregasyonu kuvvetle inhibe eder== (Antitrombotik).\n  • **Üst Madde: Tromboksan A2 (TXA2 - Pıhtı Dostu)**\n    - *Vasküler Etki:* ==Vazokonstriksiyon== yapar.\n    - *Trombosit Etkisi:* ==Agregasyon ve tıkaç oluşumunu tetikler== (Protrombotik).",
        "🔵 **Çıkmış Soru (TUS & Komite):** Düşük Doz Aspirinin Neden Antitrombotik Olduğu\n  • **Soru:** \"Düşük doz aspirinin (81-100 mg) antitrombotik etki göstermesinin hücresel nedeni nedir?\"\n    - *Doğru Cevap:* ==Trombositlerin çekirdeksiz olması nedeniyle asetillenen COX-1'i yenileyememesi==, buna karşın çekirdekli endotelin COX enzimini yeniden sentezleyerek PGI2 üretmeye devam etmesidir.\n    - *Sonuç:* Denge PGI2 lehine (antitrombotik) kayar.",
        "⚡ **Spot Hatırlatma:** TXA2 trombositte COX-1 ve Tromboksan Sentaz ile üretilir; ömrü yalnızca 30 saniyedir."
    ],
    8: [
        "🔴 **Önemli (Enzim Yolu):** 5-Lipoksijenaz Yolu ve Hücresel Dağılımı\n  • **Üst Madde: 5-LOX Enziminin Özgüllüğü**\n    - *Lokasyon:* COX gibi her hücrede bulunmaz; sadece ==nötrofil, eozinofil, mast hücresi ve monositlerde== aktiftir.\n    - *İlk Ürün:* Kararsız ara metabolit olan ==Lökotrien A4 (LTA4)== oluşur.\n  • **Üst Madde: İki Farklı Kol**\n    - *Nötrofil Kolu:* LTA4 ➔ ==Lökotrien B4 (LTB4)== kemoatraktanına döner.\n    - *Mast/Eozinofil Kolu:* LTA4 ➔ ==Sisteinil lökotrienlere (LTC4, LTD4, LTE4)== döner.",
        "🔵 **Çıkmış Soru (Farmakoloji & Patoloji):** 5-Lipoksijenaz Enzim İnhibitörü\n  • **Soru:** \"Astım tedavisinde araşidonik asitten lökotrien sentezinin ilk basamağını (5-LOX) doğrudan inhibe eden ilaç hangisidir?\"\n    - *Doğru Cevap:* ==Zileuton==.\n    - *Tuzak:* Montelukast enzimi değil, reseptörü (CysLT1) bloke eder; 5-LOX enzimini inhibe eden Zileuton'dur.",
        "⚡ **Spot Bilgi:** LTA4 hidrolaz enzimi nötrofillerde boldur ve kemotaksiden sorumlu LTB4'ü üretir."
    ],
    9: [
        "🔴 **Önemli (Sınavın Altın Kuralı):** Nötrofil Kemotaksisinin Dört Büyük Mimarı\n  • **Üst Madde: Dört Altın Kemoatraktan Molekül**\n    - 1. ==Lökotrien B4 (LTB4)== (Lipid türevi)\n    - 2. ==Kompleman C5a parçası== (Peptid anafilatoksin)\n    - 3. ==İnterlökin-8 (IL-8 / CXCL8)== (Kemokin ailesi)\n    - 4. ==Bakteriyel N-formil-metionil peptidler==\n  • **Üst Madde: LTB4'ün Ek Etkileri**\n    - *İntegrin Aktivasyonu:* Nötrofillerdeki β2 integrinlerin afinitesini artırarak endotelyal ICAM-1'e sıkı tutunmayı sağlar.\n    - *Degranülasyon:* Nötrofillerin lizozomal enzim salmasını ve ROS üretimini tetikler.",
        "🔵 **Çıkmış Soru (Patoloji Klasiği):** Lökosit Kemotaksisinde Görev Alan Eikozanoid\n  • **Soru:** \"Aşağıdaki araşidonik asit türevlerinden hangisi nötrofillerin yangı odağına kemotaksisini sağlayan en güçlü mediyatördür?\"\n    - *Doğru Cevap:* ==Lökotrien B4 (LTB4)==.\n    - *Çeldirici:* LTC4 bronkospazm yapar, LTB4 ise kemotaksi yapar.",
        "⚡ **Spot Sentez:** LTB4 BLT1 ve BLT2 reseptörleri üzerinden sinyal iletir."
    ],
    10: [
        "🔴 **Önemli (Astım Patogenezi):** Sisteinil Lökotrienler (LTC4, LTD4, LTE4)\n  • **Üst Madde: Güç Derecesi (SRS-A)**\n    - *Bronkospazm:* Bronş düz kaslarını ==histaminden yaklaşık 1000 kat daha güçlü== ve kalıcı kasar.\n    - *Permeabilite:* Postkapiller venüllerde şiddetli endotel kontraksiyonu ile mukozal ödeme yol açar.\n    - *Mukus:* Hava yollarında koyu ve tıkacı andıran aşırı mukus salgısını indükler.\n  • **Üst Madde: İlaç Hedefi**\n    - *CysLT1 Reseptörü:* ==Montelukast ve Zafirlukast== bu reseptörü antagonize eder.",
        "🔵 **Çıkmış Soru (Göğüs Hastalıkları & Farmakoloji):** Sisteinil Lökotrien Reseptör Blokeri\n  • **Soru:** \"Astım profilaksisinde kullanılan Montelukast adlı ilacın primer hedef aldığı reseptör hangisidir?\"\n    - *Doğru Cevap:* ==CysLT1 (Sisteinil Lökotrien Reseptörü)==.\n    - *Klinik İpucu:* Aspirine duyarlı astımı olan hastalarda lökotrien yolunun aşırı çalışmasını bu ilaçlar frenler.",
        "⚡ **Spot Hatırlatma:** LTC4, LTD4 ve LTE4 yapılarında sistein aminoasiti içerdikleri için 'sisteinil' ön adını alırlar."
    ],
    11: [
        "🔴 **Önemli (Yangının İtfaiyecisi):** Lipoksinler Neden Anti-İnflamatuardır?\n  • **Üst Madde: Transsellüler Biyosentez (İki Hücrenin İşbirliği)**\n    - *Nötrofil:* 5-LOX ile ara metabolitleri üretir.\n    - *Trombosit:* 12-LOX ile ara ürünü alıp aktif ==Lipoksin A4 ve B4'e== dönüştürür.\n  • **Üst Madde: Çözünme (Rezolüsyon) Etkileri**\n    - *Nötrofil Freni:* ==Nötrofil kemotaksisini ve adezyonunu durdurur==.\n    - *Eferositoz:* Ölü nötrofilleri temizlemek üzere non-inflamatuar monositleri bölgeye davet eder.",
        "🔵 **Çıkmış Soru (Patoloji & İmmünoloji):** Enflamasyonun Rezolüsyonunu Sağlayan Eikozanoid\n  • **Soru:** \"Lökosit-trombosit etkileşimiyle üretilen ve diğer tüm eikozanoidlerin aksine nötrofil göçünü baskılayarak yangıyı sonlandıran lipid mediyatör hangisidir?\"\n    - *Doğru Cevap:* ==Lipoksinler (LXA4, LXB4)==.\n    - *Tuzak:* Tüm lökotrienler ve prostaglandinler yangıyı alevlendirirken, lipoksinler söndürür.",
        "⚡ **Spot Sentez:** Aspirin asetillediği COX-2 enzimi aracılığıyla 'Aspirin-Tetikli Lipoksinler (15-epi-lipoksinler / ATL)' sentezletir; bu durum aspirinin ek bir anti-inflamatuar mekanizmasıdır."
    ],
    12: [
        "🔴 **Önemli (Farmakoloji Düğüm Noktaları):** İlaç - Enzim Eşleştirme Rehberi\n  • **Üst Madde: Basamak Basamak Blokaj Haritası**\n    - 1. ==Kortikosteroidler:== Fosfolipaz A2 (PLA2) enzimini inhibe eder (Anneksin A1 yoluyla).\n    - 2. ==Aspirin:== COX-1 ve COX-2'yi kovalan asetille irreversibl bloke eder.\n    - 3. ==Selekoksib:== Sadece indüklenebilir COX-2'yi seçici bloke eder.\n    - 4. ==Zileuton:== 5-Lipoksijenaz (5-LOX) enzimini direkt inhibe eder.\n    - 5. ==Montelukast:== CysLT1 lökotrien reseptörünü bloke eder.",
        "🔵 **Çıkmış Soru (Komite Klasiği):** Glukokortikoidlerin Hücresel Hedefi\n  • **Soru:** \"Kortikosteroidlerin araşidonik asit yolundaki primer etki mekanizması hangisidir?\"\n    - *Doğru Cevap:* ==Lipokortin-1 (Anneksin-1) sentezini artırarak Fosfolipaz A2'yi inhibe etmek==.\n    - *Sınav Tuzağı:* Doğrudan COX enzimini parçalamazlar; PLA2'yi durdurarak kaskadın hammaddesini keserler.",
        "⚡ **Spot Klinik:** NSAİİ kullanan astımlı hastalarda siklooksijenaz yolu kesilince tüm araşidonik asit 5-LOX yoluna kayar (Lökotrien şantı); bu durum ==bronkospazm krizine (Aspirin Astımı)== yol açar."
    ],
    13: [
        "🔴 **Önemli (Orkestra Şefleri):** TNF ve IL-1'in Makrofajdan Doğuşu\n  • **Üst Madde: Temel Üretim Merkezi**\n    - *Hücre:* Doku ==aktive makrofajları== ve dendritik hücrelerdir.\n    - *Tetikleyici:* Bakteriyel LPS (endotoksin), TLR aktivasyonu, nekrotik DAMP ürünleri.\n  • **Üst Madde: İnflamazom ve Kaspaz-1 Zorunluluğu**\n    - *Pro-form:* IL-1 hücrede önce inaktif pro-IL-1β olarak bulunur.\n    - *Aktivasyon:* ==NLRP3 inflamazom== aktive olur ➔ ==Kaspaz-1== enzimini uyarır ➔ pro-IL-1β kesilerek aktif IL-1'e dönüşür.",
        "🔵 **Çıkmış Soru (Patoloji & Romatoloji):** Gut Artritinde İnflamazom Aktivasyonu\n  • **Soru:** \"Gut hastalarında monosodyum ürat kristallerinin makrofajlarda uyardığı ve Kaspaz-1 aracılığıyla aktif IL-1 salınımına yol açan sitozolik kompleks hangisidir?\"\n    - *Doğru Cevap:* ==NLRP3 İnflamazom Kompleksi==.\n    - *Klinik İlgi:* Anti-IL-1 biyolojik ilaçları (Anakinra, Kanakinumab) dirençli gut ataklarında hayat kurtarır.",
        "⚡ **Spot Sentez:** TNF ayrıca T lenfositler tarafından da salınır; granülom oluşumunda ve devamlılığında zorunludur."
    ],
    14: [
        "🔴 **Önemli (Endotel Aktivasyonu):** TNF ve IL-1'in Lökositer Adezyon Zinciri\n  • **Üst Madde: Damar Duvarının Hazırlanması**\n    - *Rolling (Yuvarlanma):* Endotel yüzeyinde ==E-selektin== ekspresyonunu ve P-selektin taşınmasını artırır.\n    - *Firm Adhesion (Sıkı Tutunma):* İntegrin ligandları olan ==ICAM-1 ve VCAM-1== ekspresyonunu kat kat artırır.\n  • **Üst Madde: Prokoagülan Dönüşüm**\n    - *Etki:* Endotelde Doku Faktörü (TF) ekspresyonunu artırırken trombomodulini azaltır; yangı odağını çevreleyen mikrovasküler fibrin ağı ördürür.",
        "🔵 **Çıkmış Soru (Patoloji):** Endotelde ICAM-1 ve E-Selektin İndüksiyonu\n  • **Soru:** \"Postkapiller venül endotelinde E-selektin ve ICAM-1 adezyon moleküllerinin ekspresyonunu indükleyerek lökosit göçünü başlatan temel sitokin çifti hangisidir?\"\n    - *Doğru Cevap:* ==TNF ve İnterlökin-1 (IL-1)==.\n    - *Tuzak:* IL-10 ve TGF-beta anti-inflamatuardır, bu adezyon moleküllerini baskılar.",
        "⚡ **Spot Bilgi:** Anti-TNF tedavisi (İnfliksimab, Etanersept) alan hastalarda granülomlar dağılacağı için ==latent Tüberküloz reaktivasyonu== riski çok yüksektir; tedavi öncesi PPD/QuantiFERON şarttır."
    ],
    15: [
        "🔴 **Önemli (Sistemik Toksisite):** TNF ve IL-1'in Septik Şok ve Kaşeksi Yüzü\n  • **Üst Madde: Yüksek Doz Sistemik Patoloji**\n    - *Miyokard Depresyonu:* Kalp kasının kasılma gücünü (kontraktilitesini) belirgin düşürür.\n    - *Vasküler Kollaps:* Yaygın vazodilatasyon ve endotel geçirgenliği ile dirençli hipotansiyon (Septik Şok).\n    - *DİK Tablosu:* Mikrovasküler trombozlar ve tüketim koagülopatisi.\n  • **Üst Madde: Kaşektin Etkisi**\n    - *Kaşeksi:* İştah merkezini baskılar, lipoprotein lipazı inhibe eder; kronik enfeksiyon ve kanserlerde ==derin zayıflama (kaşeksi)== yapar.",
        "🔵 **Çıkmış Soru (Komite Klasiği):** Akut Faz Yanıtı ve Kaşeksiye Yol Açan Sitokin\n  • **Soru:** \"Tümör kaşeksisinde yağ ve kas dokusu kaybından sorumlu olan, eski adı 'kaşektin' olan sitokin hangisidir?\"\n    - *Doğru Cevap:* ==Tümör Nekroz Faktörü-alfa (TNF-α)==.\n    - *Klinik İlgi:* Tüberküloz ve ileri evre kanserlerdeki erime tablosunun ana sorumlusudur.",
        "⚡ **Spot Sentez:** Karaciğerde CRP ve fibrinojen üretimini uyararak sedimentasyon hızını (ESH) yükseltirler."
    ],
    16: [
        "🔴 **Önemli (Akut Faz ve Nötrofil):** IL-6 ve IL-17 İkilisi\n  • **Üst Madde: İnterlökin-6 (IL-6) - Akut Fazın Kralı**\n    - *Karaciğer:* Hepatositlerde ==C-Reaktif Protein (CRP)== sentezini en güçlü indükleyen sitokindir.\n    - *Kemik İliği:* Trombositozu uyarır (enfeksiyonlarda reaktif trombosit yüksekliği).\n  • **Üst Madde: İnterlökin-17 (IL-17) - Nötrofil Çağırıcısı**\n    - *Kaynak:* ==Th17 hücreleri== tarafından üretilir.\n    - *Etki:* Epitel ve fibroblastlardan kemokin salgılatarak dokuya nötrofil yığar; ==Psöriyazis ve Romatoid Artrit== patogenezindedir.",
        "🔵 **Çıkmış Soru (Biyokimya & Patoloji):** Karaciğerden CRP Sentezini En Güçlü Uyaran Sitokin\n  • **Soru:** \"Akut faz yanıtında karaciğerden C-Reaktif Protein (CRP) sentezini doğrudan ve en güçlü şekilde uyaran interlökin hangisidir?\"\n    - *Doğru Cevap:* ==İnterlökin-6 (IL-6)==.\n    - *İlaç:* Tosilizumab (IL-6 reseptör blokeri) sitokin fırtınası tedavisinde kullanılır.",
        "⚡ **Spot Bilgi:** IL-17 inhibitörü olan ==Sekukinumab==, dirençli plak psöriyazisi ve ankilozan spondilit tedavisinde onaylıdır."
    ],
    17: [
        "🔴 **Önemli (Kemokin Aileleri):** C-X-C vs. C-C Seçicilik Kuralı\n  • **Üst Madde: C-X-C Kemokinler (α Kemokinler)**\n    - *Temsilci:* ==İnterlökin-8 (CXCL8)==.\n    - *Hedef:* Başlıca ==Nötrofilleri== çeker ve aktive eder.\n  • **Üst Madde: C-C Kemokinler (β Kemokinler)**\n    - *Temsilciler:* ==MCP-1 (CCL2), Eotaksin (CCL11), RANTES==.\n    - *Hedef:* ==Monositleri, lenfositleri ve eozinofilleri== çeker.\n    - *Kritik Kural:* C-C kemokinleri nötrofillere ETKİ ETMEZ!",
        "🔵 **Çıkmış Soru (Mikrobiyoloji & Patoloji):** HIV Girişinde Kemokin Reseptörleri\n  • **Soru:** \"HIV-1 virüsünün CD4+ T hücrelerine ve makrofajlara girişte koreseptör olarak kullandığı kemokin reseptörleri hangileridir?\"\n    - *Doğru Cevap:* ==CCR5 (makrofaj-tropik) ve CXCR4 (T-tropik)==.\n    - *Genetik:* CCR5-Δ32 homozigot delesyonu olan bireyler HIV enfeksiyonuna dirençlidir.",
        "⚡ **Spot Sentez:** Kemokinler doku matriksindeki heparan sülfat proteoglikanlarına tutunarak lökositlere yön gösteren kimyasal bir yol çizerler."
    ],
    18: [
        "🔴 **Önemli (Kavşak Noktası):** Kompleman Sisteminin 3 Aktivasyon Yolu\n  • **Üst Madde: Yolların Tetiklenme Mekanizmaları**\n    - *1. Klasik Yol:* Antijene bağlanmış ==IgM veya IgG (IgG1, IgG3)== ile C1 fiksasyonu.\n    - *2. Lektin Yolu:* ==Mannoz Bağlayıcı Lektinin (MBL)== bakteri mannozuna bağlanması (antikor gerektirmez).\n    - *3. Alternatif Yol:* Doğrudan mikrop yüzey molekülleri (LPS, polisakkarit) ve Faktör B/D.\n  • **Üst Madde: Ortak Kesişme Basamağı**\n    - *Enzim:* Her 3 yol da ==C3 Konvertaz== enzim kompleksini oluşturur ve C3'ü parçalar.",
        "🔵 **Çıkmış Soru (İmmünoloji & Patoloji):** Klasik Yol C3 Konvertaz Kompleksi\n  • **Soru:** \"Kompleman sisteminin klasik aktivasyon yolunda C3 konvertaz enzimini oluşturan protein kompleksi hangisidir?\"\n    - *Doğru Cevap:* ==C4b2a==.\n    - *Alternatif Yol Karşılaştırması:* Alternatif yol C3 konvertazı ise ==C3bBb== kompleksidir.",
        "⚡ **Spot Bilgi:** Klasik yolu aktive etmede tek bir IgM molekülü yeterliyken, IgG'nin C1q bağlayabilmesi için en az iki molekülünün yan yana gelmesi gerekir."
    ],
    19: [
        "🔴 **Önemli (Efektör Üçlü):** Opsonin, Anafilatoksin ve Litik Por\n  • **Üst Madde: Fonksiyonların Paylaşımı**\n    - *1. Opsonizasyon:* ==C3b ve iC3b== mikrobu kaplar; fagositlerin CR1 (CD35) reseptörüne bağlanarak fagositozu uçurur.\n    - *2. Anafilatoksin ve Kemotaksi:* ==C5a== (en güçlüsü) ve C3a; mast hücresini patlatır, C5a nötrofili olay yerine çağırır.\n    - *3. Hücre Lizisi:* ==C5b-9 Membran Atak Kompleksi (MAC)==; hedef zarı delerek mikrobu osmotik şokla patlatır.",
        "🔵 **Çıkmış Soru (Sınavların Vazgeçilmezi):** Terminal Kompleman (MAC) Eksikliği\n  • **Soru:** \"C5, C6, C7, C8 veya C9 (Membran Atak Kompleksi) genetik eksikliği olan bireylerde özellikle hangi bakteri enfeksiyonlarına yatkınlık görülür?\"\n    - *Doğru Cevap:* ==Neisseria türleri (Neisseria meningitidis ve Neisseria gonorrhoeae)==.\n    - *Patolojik Neden:* Neisseria'nın ince hücre duvarı lizis için mutlaka fonksiyonel MAC gerektirir.",
        "⚡ **Spot Sentez:** En güçlü opsonin C3b, en güçlü anafilatoksin C5a'dır."
    ],
    20: [
        "🔴 **Önemli (Klinik Tablolar):** Kompleman Düzenleyicileri ve Hastalıklar\n  • **Üst Madde: C1 İnhibitörü (C1-INH) Eksikliği**\n    - *Hastalık:* ==Herediter Anjiyoödem (HAE)==.\n    - *Mekanizma:* C1 ve Kallikrein baskılanamaz; kontrolsüz ==Bradikinin birikir==, asfiksiye yol açabilen laringeal ödem atakları gelişir.\n  • **Üst Madde: DAF (CD55) ve CD59 (Protectin) Eksikliği**\n    - *Hastalık:* ==Paroksismal Noktürnal Hemoglobinüri (PNH)==.\n    - *Mekanizma:* *PIGA gen mutasyonu* sonucu GPI çıpası yapılamaz; eritrositler CD55 ve CD59'dan yoksun kalıp komplemanla parçalanır (intravasküler hemoliz).",
        "🔵 **Çıkmış Soru (Hematoloji & Patoloji):** PNH Patogenezindeki Temel Defekt\n  • **Soru:** \"Paroksismal noktürnal hemoglobinüride eritrositlerin kompleman litik saldırısına duyarlı hale gelmesinin temel moleküler nedeni nedir?\"\n    - *Doğru Cevap:* ==GPI çıpa sentez defektine (PIGA mutasyonu) bağlı olarak eritrosit zarında CD55 (DAF) ve CD59 bulunamamasıdır==.\n    - *Tedavi:* Eculizumab (Anti-C5 monoklonal antikoru) MAC oluşumunu keserek hemolizi durdurur.",
        "⚡ **Spot Bilgi:** Faktör H mutasyonları Atipik Hemolitik Üremik Sendrom (aHÜS) gelişimine yol açar."
    ],
    21: [
        "🔴 **Önemli (Ağrının Kaynağı):** Kallikrein-Kinin Sistemi ve Bradikinin\n  • **Üst Madde: Aktivasyon Kaskadı**\n    - *Tetikleyici:* Negatif yüzeylere temas eden ==Faktör XII (Hageman Faktörü)== aktive olur (FXIIa).\n    - *Ara Basamak:* FXIIa plazma prekallikreinini ==Kallikreine== çevirir.\n    - *Son Ürün:* Kallikrein HMWK'den 9 aminoasitlik ==Bradikinin== peptidini koparır.\n  • **Üst Madde: Bradikinin Etkileri**\n    - *Ağrı:* C-liflerindeki B2 reseptörlerine bağlanarak doğrudan ==ağrı (dolor)== oluşturur.\n    - *Vasküler:* Venüllerde histaminden bile güçlü geçirgenlik artışı ve vazodilatasyon yapar.",
        "🔵 **Çıkmış Soru (Farmakoloji & Dahiliye):** ACE İnhibitörü Öksürüğü ve Anjiyoödem\n  • **Soru:** \"Hipertansiyon nedeniyle Enalapril başlanan hastada gelişen inatçı kuru öksürük ve anjiyoödemden sorumlu biriken mediyatör hangisidir?\"\n    - *Doğru Cevap:* ==Bradikinin== (ACE aynı zamanda Kininaz II enzimidir; ilacın ACE'yi bloke etmesi bradikinin yıkımını durdurur).\n    - *Klinik Çözüm:* İlaç kesilip bradikinini etkilemeyen ARB (Anjiyotensin Reseptör Blokeri) başlanır.",
        "⚡ **Spot Sentez:** Enflamasyonda ağrıyı doğrudan başlatan Bradikinin ve Substans P iken; ağrı eşiğini düşürerek duyarlılaştıran Prostaglandin E2'dir."
    ],
    22: [
        "🔴 **Önemli (Büyük Matris):** Robbins Tablo 2.8 Enflamasyon Kardinal Bulguları\n  • **Üst Madde: Vazodilatasyon Yapanlar**\n    - ==Histamin, Prostaglandinler (PGI2, PGE2, PGD2), Nitrik Oksit (NO)==.\n  • **Üst Madde: Vasküler Geçirgenliği Artıranlar (Ödem)**\n    - ==Histamin, Bradikinin, Sisteinil Lökotrienler (LTC4/D4/E4), C3a ve C5a, PAF==.\n  • **Üst Madde: Kemotaksi ve Lökosit Aktivasyonu Yapanlar**\n    - ==LTB4, C5a, Kemokinler (IL-8), TNF, IL-1, Bakteriyel ürünler==.\n  • **Üst Madde: Ateş Yapanlar**\n    - ==IL-1, TNF, IL-6, Prostaglandin E2 (PGE2)==.\n  • **Üst Madde: Ağrı Yapanlar**\n    - ==Bradikinin, Prostaglandinler (PGE2), Substans P==.",
        "🔵 **Çıkmış Soru (Komite & TUS Şampiyonu):** Enflamasyon Mediyatörleri Büyük Eşleştirme\n  • **Soru:** \"Aşağıdaki yangısal fonksiyon - primer kimyasal mediyatör eşleştirmelerinden hangisi YANLIŞTIR?\"\n    - *A) Ateş — Prostaglandin E2*\n    - *B) Nötrofil kemotaksisi — Lökotrien B4*\n    - *C) Ağrı oluşumu — Bradikinin*\n    - *D) Opsonizasyon — Kompleman C3b*\n    - *E) Trombosit agregasyon inhibisyonu — Tromboksan A2* ❌ (Doğrusu Prostasiklin'dir; TXA2 agregasyonu tetikler!).",
        "⚡ **Spot Sentez:** PAF son derece düşük dozlarda histaminden 10.000 kat daha güçlü vazodilatasyon ve venüler geçirgenlik artışı yapabilen güçlü bir fosfolipid türevidir."
    ]
}

# Apply to all 22 slides
for slide in deck['slides']:
    s_num = slide.get('slideNumber')
    if s_num in structured_spots:
        slide['spotPearls'] = structured_spots[s_num]

# Also ensure deck highYieldPearls has red and blue indicators
deck['highYieldPearls'] = [
    "🔴 **Önemli:** Sisteinil lökotrienler (LTC4, LTD4, LTE4) bronş düz kaslarını histaminden 1000 kat daha güçlü kasar; Montelukast bunların CysLT1 reseptörünü bloke eder.",
    "🔵 **Çıkmış Soru:** Lökosit kemotaksisinin 4 majör ajanı: Lökotrien B4 (LTB4), Kompleman C5a, İnterlökin-8 (CXCL8) ve bakteriyel N-formil peptidlerdir.",
    "🔴 **Önemli:** C1 inhibitörü eksikliğinde bradikinin birikerek Herediter Anjiyoödeme; eritrosit zarında CD55 ve CD59 eksikliğinde PNH'ye (Paroksismal Noktürnal Hemoglobinüri) yol açar.",
    "🔵 **Çıkmış Soru:** Hipotalamik preoptik alanda vücut sıcaklık ayar noktasını yükselterek ateşe yol açan temel mediyatör Prostaglandin E2'dir (PGE2)."
]

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("✓ All 22 slides in 'learn-enflamasyon-kimyasal-mediyatorleri' successfully enriched with structured spot pearls!")
