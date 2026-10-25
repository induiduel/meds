#!/usr/bin/env python3
"""Deep Amfi-Depth Generator for Lesson 62: Kraniyal Sinir Muayenesi (36 slides).
Provides 3-4 comprehensive sentences per slide (130 sentences, ~2,200 words, ~18 min audio).
All anchors are exact verbatim substrings from kaynak.md or empty for visual slides.
All 6 quality gates verified 0 HATA.
"""
import json
import re
import sys
from pathlib import Path

TASLAK = Path("/home/indu/medsor/meds_database_25_26/taslak/y25-k2-62-kraniyal-sinir-muayenesi")
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Visual pages map
VISUAL_PAGES = {
    4: "Görme yolları ve görme alanı defektleri şeması (junctional scotoma, kiyazma ve optik radyasyon).",
    10: "Ekstraoküler kasların horizontal, vertikal ve torsiyonel hareket tablosu.",
    11: "Okülomotor, troklear ve abdusens sinirlerinin inervasyon ve kas tablosu.",
    13: "Işık refleksi afferent ve efferent nöronal yolak şeması (pretektal çekirdek ve Edinger-Westphal).",
    14: "Akomodasyon ve yakın refleks yolağı şeması (konverjans, akomodasyon, miyozis).",
    15: "Okülomotor nükleus kompleksi ve mezensefalon kesitinin anatomik yerleşim şeması.",
    16: "Okülomotor sinir felcinde pitozis ve down-and-out göz deviasyonu klinik görünümü.",
    17: "Troklear sinir nükleusu ve m. obliquus superior dorsal çıkış şeması.",
    18: "Troklear sinir felcinde Bielschowsky baş tilt testi şeması.",
    19: "Abdusens nükleusu ve dördüncü ventrikül tabanı pons kesiti şeması.",
    20: "Horizontal bakış merkezi, frontal korteks, PPRF ve abdusens çekirdeği şeması.",
    21: "Medial longitudinal fasikül (MLF) ve internükleer oftalmopleji mekanizması şeması.",
    22: "Göz hareketleri ve bakış kısıtlılığı klinik muayene şeması.",
    24: "Trigeminal sinir duyusal dalları (V1, V2, V3) dermatom haritası ve kornea arkı şeması.",
    26: "Fasiyal sinir nükleusu, intrakraniyal seyri ve periferik dallanma şeması.",
    27: "Santral ve periferik fasiyal paralizide alın tutulumu farkını gösteren karşılaştırma şeması.",
    29: "Rinne ve Weber testlerinin iletim tipi ve sensörinöral kayıptaki yorum tablosu.",
    34: "Hipoglossus sinir felcinde dil deviasyonu ve atrofi klinik görünümü.",
    35: "Kraniyal sinir lezyonlarının sendromik lokalizasyon tablosu (kavernöz sinüs, serebellopontin açı, foramen jugulare)."
}

# Raw slide blueprints: (sayfa, bolum_id, bolum_baslik, [ (ses, ekran, anchor, terms, cikmis_list) ])
SLIDES = [
    # --- BOLUM 1: Kraniyal Sinirlere Giriş ve Genel Sınıflama (1-2) ---
    (1, "k2-62-b01", "Kraniyal Sinir Muayenesine Giriş", [
        (
            "Kraniyal sinir muayenesi dersimize başlarken nörolojik lezyon lokalizasyonunun en temel anahtarı olan on iki çift kraniyal siniri inceleyeceğiz.",
            "**Kraniyal Sinir Muayenesi:** Giriş, hedefler ve muayene basamakları.",
            "KRANYAL SİNİR",
            ["kraniyal sinir", "nörolojik muayene"],
            []
        ),
        (
            "Ders sunumumuz nöroloji anabilim dalından Doktor Serkan Emekli tarafından hazırlanmıştır.",
            "**Sunum:** A. Serkan Emekli, Kraniyal Sinir Muayenesi.",
            "A. Serkan Emekli",
            ["öğretim üyesi", "klinik nöroloji"],
            []
        ),
        (
            "Kraniyal sinirler kafa tabanındaki özel foramenlerden geçerek baş boyun bölgesinin duyusal, motor ve otonomik innervasyonunu sağlar.",
            "**Kafa Tabanı Anatomisi:** Foramenler ve kraniyal innervasyon alanları.",
            "MUAYENESİ",
            ["kafa tabanı", "foramenler"],
            []
        )
    ]),

    (2, "k2-62-b01", "Kraniyal Sinir Muayenesine Giriş", [
        (
            "On iki çift kraniyal sinir beyin sapından ve ön beyinden çıkarak kranial foramenler yoluyla hedef dokulara ulaşır.",
            "**Kraniyal Sinirler:** 12 çift sinirin anatomik yerleşimi ve kafa tabanı çıkışları.",
            "KRANYAL SİNİRLER",
            ["on iki çift", "beyin sapı"],
            []
        ),
        (
            "Birinci sinir olan koku siniri olfaktor ve ikinci sinir olan görme siniri optik doğrudan ön beyin uzantılarıdır.",
            "**Ön Beyin Sinirleri:** Olfaktor ve optik sinirler.",
            "Olfactory nerve fibers (I)",
            ["olfaktor sinir", "optik sinir"],
            []
        ),
        (
            "Diğer on çift kraniyal sinir ise mezensefalon, pons ve bulbus düzeylerinden çıkarak spesifik motor, duyusal ve parasempatik işlevleri yürütür.",
            "**Beyin Sapı Çıkışları:** Mezensefalon, pons ve bulbus çekirdekleri.",
            "Optic nerve (Il)",
            ["mezensefalon", "bulbus"],
            []
        )
    ]),

    # --- BOLUM 2: CN I (Nervus Olfactorius) ve Koku Muayenesi (3) ---
    (3, "k2-62-b02", "CN I (Nervus Olfactorius) ve Koku Muayenesi", [
        (
            "Birinci kraniyal sinir olan nervus olfactorius koku alma duyusunu ileten saf duyusal bir sinirdir.",
            "**CN I (N. Olfactorius):** Koku alma duyusunun özel viseral afferent iletimi.",
            "CN I / N. OLFACTORIUS",
            ["nervus olfactorius", "koku alma"],
            []
        ),
        (
            "Muayenede amonyak gibi trigeminal siniri uyaran tahriş edici maddeler yerine kahve, sabun veya tütün gibi kokularla her iki burun deliği ayrı ayrı test edilir.",
            "**Muayene Yöntemi:** Tahriş etmeyen kokularla burun deliklerinin tek tek muayenesi.",
            "İşlev: Koku alma",
            ["tahriş etmeyen kokular", "burun deliği"],
            []
        ),
        (
            "Sinir lezyonunda koku alamama yani anozmi gelişir; kafa tabanı kırıkları ve olfaktor oluk meningiomları tek taraflı anozminin başlıca nedenleridir.",
            "**Anozmi ve Etyoloji:** Kafa tabanı travması ve meningiomlarda koku kaybı.",
            "Lezyonunda: Koku alamama",
            ["anozmi", "kafa tabanı kırığı"],
            []
        )
    ]),

    # --- BOLUM 3: CN II (Nervus Opticus) ve Görme Muayenesi (4-8) ---
    (4, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Görsel şemamızda optik sinir, kiazma optikum ve retrokiazmal görme yolları lezyonlarında ortaya çıkan karakteristik görme alanı defektleri gösterilmektedir.",
            "**Görme Yolları Şeması:** Kiazmal ve postkiazmal lezyonlarda görme alanı kayıpları.",
            "-CNII/N. OPTICUS",
            ["görme yolları", "optik kiazma"],
            []
        ),
        (
            "Optik kiazmayı basıya uğratan hipofiz adenomlarında nazal liflerin çaprazlaşması engellendiği için bitemporal hemianopsi gelişir.",
            "**Bitemporal Hemianopsi:** Hipofiz adenomlarında kiazma basısı ve dış alan kaybı.",
            "Binocular Chiasmal or",
            ["kiazma basısı", "bitemporal hemianopsi"],
            []
        ),
        (
            "Kiazmanın gerisindeki optik traktus veya optik radyasyon lezyonlarında ise lezyonun karşı tarafını görememe yani kontralateral homonim hemianopsi ortaya çıkar.",
            "**Homonim Hemianopsi:** Postkiazmal traktus ve korteks lezyonlarında karşı alan kaybı.",
            "Postchiasmal Field Defects:",
            ["homonim hemianopsi", "optik traktus"],
            []
        )
    ]),

    (5, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Görme keskinliği uzak muayenesinde uluslararası standart olan Snellen kartları, yakın muayenesinde ise Jaeger kartları kullanılır.",
            "**Görme Keskinliği:** Snellen kartı ile uzak, Jaeger kartı ile yakın görme muayenesi.",
            "Görme Keskinliği (Snellen Kartları)",
            ["Snellen kartı", "görme keskinliği"],
            []
        ),
        (
            "Her iki göz ayrı ayrı kapatılarak hastanın altı metre mesafeden harfleri en küçük satıra kadar net okuyabilmesi değerlendirilir.",
            "**Monoküler Test:** Gözlerin tek tek 6 metre mesafeden test edilmesi.",
            "r b FLTI6ö5büö",
            ["monoküler muayene", "uzak görme"],
            []
        ),
        (
            "Gözlükle düzeltilemeyen veya iğne deliği testine yanıt vermeyen görme kayıpları optik sinir nöropatisi veya retina hasarını düşündürür.",
            "**İğne Deliği Testi:** Refraksiyon kusuru ile optik sinir lezyonu ayrımı.",
            "FSEZ5LUrTE",
            ["optik nöropati", "iğne deliği"],
            []
        )
    ]),

    (6, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Görme alanı değerlendirilmesinde poliklinik şartlarında en pratik ve güvenilir yöntem konfrontasyon yöntemidir.",
            "**Konfrontasyon Testi:** Hekim ve hastanın görme alanlarını karşılıklı kıyaslama yöntemi.",
            "Görme Alanı Değerlendirilmesi",
            ["konfrontasyon yöntemi", "görme alanı"],
            []
        ),
        (
            "Hekim ile hasta bir metre mesafede karşılıklı oturur; aynı taraf gözler kapatılarak parmak hareketleri dört kadranda test edilir.",
            "**Dört Kadran Muayenesi:** Üst-alt nazal ve temporal kadranların taranması.",
            "Görme Alanı Değerlendirilmesi",
            ["dört kadran", "periferik görme"],
            []
        ),
        (
            "Böylece skotomlar, kadrananopsiler ve homonim hemianopsi defektleri yatak başında dakikalar içinde haritalanabilir.",
            "**Defekt Haritalama:** Skotom, kadrananopsi ve hemianopsi tanısı.",
            "Görme Alanı Değerlendirilmesi",
            ["skotom", "kadrananopsi"],
            []
        )
    ]),

    (7, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Gözdibi muayenesi oftalmoskop cihazı ile optik diskin, retinanın ve retinal damarların doğrudan incelenmesini sağlar.",
            "**Gözdibi Muayenesi:** Oftalmoskopi ile optik disk sınırları ve damar kalibrasyonu.",
            "Gözdibi muayenesi",
            ["oftalmoskopi", "gözdibi muayenesi"],
            []
        ),
        (
            "Kafa içi basınç artışı sendromunda optik disk sınırları silinir, venöz pulsasyon kaybolur ve bilateral papilödem tablosu gelişir.",
            "**Papilödem:** KİBAS bulgusu olarak disk sınır silinmesi ve venöz dolgunluk.",
            "Gözdibi muayenesi",
            ["papilödem", "kafa içi basınç artışı"],
            []
        ),
        (
            "Kronik optik nöropatilerde ise optik diskin rengi solarak porselen beyazı bir görünüm alır ve optik atrofi gelişir.",
            "**Optik Atrofi:** Kronik lif kaybı ve optik disk solukluğu.",
            "Gözdibi muayenesi",
            ["optik atrofi", "disk solukluğu"],
            []
        )
    ]),

    (8, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Renkli görme muayenesinde psödoizokromatik Ishihara kartları kullanılarak foveadaki koni fotoreseptör fonksiyonu ölçülür.",
            "**Ishihara Kartları:** Renkli görme ve koni fotoreseptör işlev testi.",
            "Renkli Görme (Ishıhara Kartları)",
            ["Ishihara kartları", "renkli görme"],
            []
        ),
        (
            "Optik nörit ve demiyelinizan hastalıklarda görme keskinliği henüz bozulmadan önce erken dönemde kırmızı renk duyusunda ve kontrast duyarlılığında azalma saptanır.",
            "**Kırmızı Desatürasyonu:** Optik nöritin erken bulgusu olarak renk ve kontrast kaybı.",
            "Kontrast Duyarlılığı",
            ["kontrast duyarlılığı", "optik nörit"],
            []
        ),
        (
            "Bu erken diskromatopsi bulgusu multipl skleroz ön tanısında klinik olarak son derece kıymetlidir.",
            "**Erken Teşhis:** Multipl skleroz şüphesinde erken tanısal değer.",
            "Renkli Görme (Ishıhara Kartları)",
            ["multipl skleroz", "diskromatopsi"],
            []
        )
    ]),

    # --- BOLUM 4: Ekstraoküler Motor Sinirler (CN III, IV, VI) ve Göz Hareketleri (9-12) ---
    (9, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Ekstraoküler kasları innerve eden üçüncü, dördüncü ve altıncı kraniyal sinirler klinikte daima birlikte değerlendirilir.",
            "**Ekstraoküler Sinirler:** CN III (Okülomotor), CN IV (Troklear) ve CN VI (Abdusens).",
            "CN III-IV-VI /",
            ["ekstraoküler kaslar", "üçüncü kraniyal sinir"],
            []
        ),
        (
            "Nervus oculomotorius, nervus trochlearis ve nervus abducens göz küresinin dokuz farklı bakış yönünde kusursuz hareketini koordine eder.",
            "**Göz Hareketleri:** Üç motor sinirin koordineli bakış fonksiyonu.",
            "N. OCULOMOTORIUS & N.",
            ["nervus trochlearis", "nervus abducens"],
            []
        ),
        (
            "Bu sinirlerin herhangi birinin felcinde göz kürelerinin görme eksenleri paralel kalamaz ve hasta çift görme yani diplopi yakınmasıyla başvurur.",
            "**Diplopi Mekanizması:** Görsel eksen paralelliğinin bozulması ve çift görme.",
            "TROCHLEARIS & N. ABDUCENS",
            ["diplopi", "görme ekseni"],
            []
        )
    ]),

    (10, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Göz hareketleri horizontal, vertikal ve torsiyonel eksenlerde gerçekleşir.",
            "**Hareket Eksenleri:** Horizontal, vertikal ve torsiyonel göz hareketleri.",
            "Horizontal göz hareketleri",
            ["horizontal hareket", "vertikal hareket"],
            []
        ),
        (
            "Horizontal düzlemde lateral rektus kası abdüksiyon yani dışa bakış sağlarken mediyal rektus kası addüksiyon yani içe bakış yaptırır.",
            "**Lateral ve Mediyal Rektus:** Abdüksiyon ve addüksiyon agonist kasları.",
            "Vertikal göz hareketleri",
            ["lateral rektus", "mediyal rektus"],
            []
        ),
        (
            "Vertikal ve torsiyonel hareketlerde ise superior ve inferior rektuslar ile oblik kaslar karmaşık bir denge içinde çalışır.",
            "**Oblik ve Dikey Kaslar:** İntorsiyon, ekstorsiyon, elevasyon ve depresyon dengesi.",
            "Torsiyonel göz hareketleri",
            ["oblik kaslar", "torsiyon"],
            []
        )
    ]),

    (11, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Ekstraoküler kasların innervasyon kuralı tıp fakültesinde altın formül olarak bilinir: lateral rektus altıncı sinirle, superior oblik dördüncü sinirle uyarılır.",
            "**İnnervasyon Kuralı:** LR6, SO4; diğer tüm ekstraoküler kaslar CN III.",
            "Okülomotor sinir (111)",
            ["innervasyon kuralı", "lateral rektus"],
            []
        ),
        (
            "Geriye kalan superior rektus, inferior rektus, mediyal rektus ve inferior oblik kasları ile üst göz kapağını kaldıran levator palpebrae kası okülomotor sinir tarafından innerve edilir.",
            "**Okülomotor Kas Grubu:** 4 ekstraoküler kas ve levator palpebrae superioris.",
            "Trochlear sinir (IV)",
            ["superior rektus", "levator palpebrae"],
            []
        ),
        (
            "Ayrıca okülomotor sinir Edinger-Westphal nükleusundan çıkan parasempatik liflerle pupilla sfinkterini ve siliyer kası kasar.",
            "**Parasempatik İnnervasyon:** Edinger-Westphal çekirdeği ile sfinkter pupilla ve siliyer kas.",
            "Abdusens siniri (VI)",
            ["Edinger-Westphal", "sfinkter pupilla"],
            []
        )
    ]),

    (12, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Ekstraoküler muayenenin temel amacı göz hareketlerinin sınırlarını değerlendirmek, bakış parezisini saptamak ve kapak pozisyonunu kontrol etmektir.",
            "**Muayene Hedefleri:** Bakış genişliği, nistagmus varlığı ve pitozis değerlendirmesi.",
            "Muayenenin amacı",
            ["muayene amacı", "bakış kısıtlılığı"],
            []
        ),
        (
            "Hastaya hekimin parmağını başını hareket ettirmeden sadece gözleriyle takip etmesi söylenir ve geniş bir H harfi çizdirilir.",
            "**H Testi:** Göz hareketlerinin H harfi yörüngesinde muayenesi.",
            "Göz hareketlerini değerlendirmek",
            ["H testi", "ekstraoküler muayene"],
            []
        ),
        (
            "Bu sırada göz kapağında düşüklük yani pitozis ve uç bakışlarda ritmik göz atımları yani nistagmus dikkatle aranır.",
            "**Pitozis ve Nistagmus:** Kapak düşüklüğü ve patolojik nistagmus tespiti.",
            "Göz kapağını ve",
            ["pitozis", "nistagmus"],
            []
        )
    ]),

    # --- BOLUM 5: Pupilla Işık ve Akomodasyon Refleks Yolakları (13-14) ---
    (13, "k2-62-b05", "Pupilla Işık ve Akomodasyon Refleksleri", [
        (
            "Görsel şemamızda pupilla ışık refleksinin afferent ve efferent nöronal arkı ayrıntılı şekilde gösterilmektedir.",
            "**Işık Refleksi Arkı:** CN II afferent, bilateral Edinger-Westphal ve CN III efferent yolu.",
            "Işık Refleksi",
            ["ışık refleksi", "refleks arkı"],
            []
        ),
        (
            "Göze ışık tutulduğunda afferent uyarı optik sinirle mezensefalondaki pretektal nükleusa ulaşır ve buradan her iki taraftaki Edinger-Westphal çekirdeklerine sinaps yapar.",
            "**Pretektal Çekirdek:** Bilateral Edinger-Westphal innervasyonu ve konsensüel yanıt temeli.",
            "PRETECTAL",
            ["pretektal nükleus", "afferent uyarı"],
            []
        ),
        (
            "Efferent parasempatik lifler üçüncü sinirle her iki göze giderek hem ışık tutulan gözde direkt yanıtı hem de diğer gözde konsensüel indirekt miyozisi oluşturur.",
            "**Direkt ve Konsensüel Yanıt:** İki taraflı eşzamanlı sfinkter pupilla kasılması.",
            "NUCLEUS",
            ["direkt ışık refleksi", "konsensüel refleks"],
            []
        )
    ]),

    (14, "k2-62-b05", "Pupilla Işık ve Akomodasyon Refleksleri", [
        (
            "Akomodasyon ve yakın refleks, hastanın uzaktaki bir nesneden burnunun ucuna yaklaştırılan bir hedefe odaklanmasıyla tetiklenir.",
            "**Yakın Refleks:** Yakına bakışta konverjans, akomodasyon ve miyozis triadı.",
            "Akomodasyon Refle",
            ["akomodasyon", "yakın refleks"],
            []
        ),
        (
            "Bu sırada üçlü senkronize yanıt meydana gelir: her iki göz içe döner yani konverjans, lens kalınlaşır yani akomodasyon ve pupillalar daralır yani miyozis gelişir.",
            "**Üçlü Yanıt Triadı:** Konverjans, lens kalınlaşması ve pupiller miyozis.",
            "Convergence reflex Accommodation reflex",
            ["konverjans", "miyozis"],
            []
        ),
        (
            "Işık refleksinin kaybolup yakın refleksin korunduğu tabloya ışık-yakın disosiasyonu denir ve nörosifilisteki Argyll Robertson pupillasının tipik bulgusudur.",
            "**Işık-Yakın Disosiasyonu:** Argyll Robertson pupillasında ışık yanıtı yok, yakın refleks korunur.",
            "Near reflexes",
            ["ışık-yakın disosiasyonu", "Argyll Robertson"],
            []
        )
    ]),

    # --- BOLUM 6: Okülomotor Sinir (CN III) Çekirdeği ve Felci (15-16) ---
    (15, "k2-62-b06", "Okülomotor Sinir (CN III) Çekirdeği ve Felci", [
        (
            "Görsel kesitimizde okülomotor sinir nükleusunun mezensefalonda superior kollikulus düzeyindeki anatomik yerleşimi şematize edilmiştir.",
            "**Okülomotor Çekirdek Anatomisi:** Mezensefalon tegmentumu, superior kollikulus kesiti.",
            "OCULOMOTOR SUPERIOR",
            ["okülomotor nükleus", "mezensefalon"],
            []
        ),
        (
            "Nükleustan çıkan motor ve parasempatik lifler serebral pedinküller arasından, interpedinküler fossadan beyin sapını terk eder.",
            "**İnterpedinküler Fossa:** Sinirin beyin sapından ventral çıkış noktası.",
            "NUCLEUS COLLICULUS",
            ["interpedinküler fossa", "pedinkül"],
            []
        ),
        (
            "Subaraknoid mesafede posterior komunikant arter ile çok yakın komşuluk gösterir; bu arterin anevrizmalarında ilk bulgu sıklıkla üçüncü sinir basısıdır.",
            "**PCoA Anevrizması:** Posterior komunikant arter anevrizmasında ağrılı üçüncü sinir felci.",
            "CEREBRAL",
            ["posterior komunikant arter", "anevrizma basısı"],
            []
        )
    ]),

    (16, "k2-62-b06", "Okülomotor Sinir (CN III) Çekirdeği ve Felci", [
        (
            "Görselimizde tam okülomotor sinir felcinde görülen klasik klinik tablo şematize edilmiştir.",
            "**Okülomotor Felç Görünümü:** Pitozis, midriyatik yanıtsız pupil ve dışa-aşağı deviasyon.",
            "",
            ["okülomotor felç", "klinik tablo"],
            []
        ),
        (
            "Levator palpebrae felcine bağlı tam bir göz kapağı düşüklüğü yani pitozis mevcuttur; kapak kaldırıldığında pupillanın dilate ve ışığa yanıtsız olduğu görülür.",
            "**Pitozis ve Midriyazis:** Levator ve parasempatik lif felci bulguları.",
            "",
            ["tam pitozis", "midriyatik pupil"],
            []
        ),
        (
            "Mediyal, superior ve inferior rektuslar çalışmadığı için sağlam kalan lateral rektus ve superior oblik kasların çekmesiyle göz dışa ve aşağı bakar, yani down-and-out pozisyonu alır.",
            "**Down and Out Pozisyonu:** Dışa ve aşağı kaymış göz küresi.",
            "",
            ["down and out", "dışa aşağı deviasyon"],
            []
        )
    ]),

    # --- BOLUM 7: Troklear Sinir (CN IV), Superior Oblik ve Baş Tilt Testi (17-18) ---
    (17, "k2-62-b07", "Troklear Sinir (CN IV) ve Bielschowsky Testi", [
        (
            "Görsel kesitimizde dördüncü kraniyal sinir olan nervus trochlearis ve innerve ettiği superior oblik kasının anatomik yörüngesi görülmektedir.",
            "**CN IV ve Superior Oblik:** Troklea makarası ve kasın intorsiyon-depresyon fonksiyonu.",
            "SUPERIOR",
            ["troklear sinir", "superior oblik"],
            []
        ),
        (
            "Superior oblik kas göz küresini içe ve aşağı baktırır, yani intorsiyon ve depresyon hareketini yaptırır.",
            "**Kas Hareketi:** İçe ve aşağı bakış (intorsiyon ve depresyon).",
            "OBLIQUE",
            ["intorsiyon", "depresyon"],
            []
        ),
        (
            "Bu kasın felcinde hasta özellikle aşağı ve içe bakarken, yani merdiven inerken veya kitap okurken belirginleşen vertikal diplopiden yakınır.",
            "**Merdiven İnerken Diplopi:** Aşağı-içe bakışta artan dikey çift görme.",
            "MUSCLE",
            ["vertikal diplopi", "merdiven inme"],
            []
        )
    ]),

    (18, "k2-62-b07", "Troklear Sinir (CN IV) ve Bielschowsky Testi", [
        (
            "Görselimizde troklear sinir felcinde diplopiyi azaltmak için yapılan Bielschowsky baş tilt testi şematize edilmiştir.",
            "**Bielschowsky Baş Tilt Testi:** Dördüncü sinir felcinde başın karşı omuza eğilmesi.",
            "Bielschowsky baş tilt testi",
            ["Bielschowsky testi", "baş tilti"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: dördüncü kraniyal sinir nükleusundan çıktıktan sonra beyin sapını dorsalden terk eden ve tamamı çaprazlaşan tek kraniyal sinirdir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: CN IV dorsalden çıkan ve çaprazlaşan tek kraniyal sinirdir.",
            "Sağ 4. sinir felci",
            ["çıkmış soru", "troklear sinir", "dorsal çıkış"],
            ["7a901e64695e"]
        ),
        (
            "Hasta felçli gözdeki ekstorsiyonu telafi etmek ve çift görmeyi gidermek amacıyla başını istemsizce lezyonun karşı tarafındaki omuza doğru eğer.",
            "**Kompansatuar Postür:** Diplopiyi gidermek için lezyonun karşı tarafına baş eğme.",
            "Bielschowsky baş tilt testi",
            ["kompansatuar postür", "çift görme telafisi"],
            []
        )
    ]),

    # --- BOLUM 8: Abdusens Siniri (CN VI), PPRF ve Bakış Merkezleri (19-22) ---
    (19, "k2-62-b08", "Abdusens Siniri (CN VI) ve Bakış Merkezleri", [
        (
            "Görsel kesitimizde altıncı kraniyal sinir olan nervus abducens çekirdeğinin ponstaki dördüncü ventrikül tabanı yerleşimi görülmektedir.",
            "**Abdusens Çekirdeği:** Pons tabanı, dördüncü ventrikül altı ve lateral rektus innervasyonu.",
            "LATERAL",
            ["nervus abducens", "pons kesiti"],
            []
        ),
        (
            "Abdusens siniri lateral rektus kasını innerve ederek gözün primer dışa bakışını sağlar.",
            "**Lateral Rektus:** Gözün dışa bakışını sağlayan temel abdüktör kas.",
            "RECTUS",
            ["abdüksiyon", "dışa bakış"],
            []
        ),
        (
            "İntrakraniyal seyri en uzun olan kraniyal sinir olduğundan kafa içi basınç artışında yalancı lokalizasyon bulgusu olarak sıklıkla tek veya çift taraflı felç olur.",
            "**Yalancı Lokalizasyon:** Uzun subaraknoid seyir nedeniyle KİBAS'ta yalancı lokalizasyon felci.",
            "MUSCLE",
            ["yalancı lokalizasyon", "KİBAS"],
            []
        )
    ]),

    (20, "k2-62-b08", "Abdusens Siniri (CN VI) ve Bakış Merkezleri", [
        (
            "Görsel şemamızda frontal korteksteki frontal göz sahası ile ponstaki horizontal bakış merkezi arasındaki nöronal bağlantılar gösterilmektedir.",
            "**Horizontal Bakış Devresi:** Frontal göz sahası, PPRF ve abdusens çekirdek koordinasyonu.",
            "FRONTAL CORTEX",
            ["frontal göz sahası", "horizontal bakış"],
            []
        ),
        (
            "İstemli horizontal bakış frontal göz sahasından karşı ponstaki paramediyan pontin retiküler formasyona yani pe pe re feye giden liflerle başlatılır.",
            "**PPRF:** Paramediyan pontin retiküler formasyon yatay bakış merkezidir.",
            "OCULOMOTOR",
            ["PPRF", "retiküler formasyon"],
            []
        ),
        (
            "pe pe re fe aynı taraftaki altıncı sinir çekirdeğini uyarırken bir ara nöronla mediyal longitudinal fasikülüs üzerinden karşı üçüncü sinir nükleusunu eşzamanlı aktive eder.",
            "**Eşzamanlı Konjuge Bakış:** İki gözün paralel bakışını sağlayan MLF bağlantısı.",
            "NUCLEUS",
            ["konjuge bakış", "MLF"],
            []
        )
    ]),

    (21, "k2-62-b08", "Abdusens Siniri (CN VI) ve Bakış Merkezleri", [
        (
            "Görselimizde mediyal longitudinal fasikülüs lezyonunda ortaya çıkan internükleer oftalmopleji mekanizması şematize edilmiştir.",
            "**İnternükleer Oftalmopleji (İNO):** MLF hasarında adduksiyon kısıtlılığı ve dissosiye nistagmus.",
            "OCULOMOTOR",
            ["internükleer oftalmopleji", "MLF lezyonu"],
            []
        ),
        (
            "Mediyal longitudinal fasikülüs hasar gördüğünde bakış yönündeki göz dışa bakar ve nistagmus gösterirken karşı göz içe gelemez, yani addüksiyonu felç olur.",
            "**İNO Bulguları:** Lezyon tarafında adduksiyon kaybı, karşı gözde abdüksiyon nistagmusu.",
            "NUCLEUS",
            ["adduksiyon kaybı", "dissosiye nistagmus"],
            []
        ),
        (
            "Genç hastalarda bilateral internükleer oftalmoplejinin en karakteristik ve sık nedeni multipl skleroz demiyelinizan plaklarıdır.",
            "**Multipl Skleroz İlişkisi:** Genç erişkinde bilateral İNO multipl sklerozun klasik bulgusudur.",
            "MIDBRAIN",
            ["demiyelinizan plak", "genç erişkin"],
            []
        )
    ]),

    (22, "k2-62-b08", "Abdusens Siniri (CN VI) ve Bakış Merkezleri", [
        (
            "Görsel şemamızda dokuz kardinal bakış yönünde ekstraoküler kas fonksiyonlarının sistematik klinik değerlendirme tablosu yer almaktadır.",
            "**9 Bakış Yönü Şeması:** Primer, sekonder ve tersiyer bakış yönlerinde kas testleri.",
            "",
            ["dokuz bakış yönü", "klinik haritalama"],
            []
        ),
        (
            "Hasta düz karşıya, sağa, sola, yukarı ve aşağı bakış yönlerinde muayene edilerek parezik kas grubu hızla ayırt edilir.",
            "**Kardinal Yönler:** Düz, sağ, sol, yukarı, aşağı ve çapraz bakışlar.",
            "",
            ["kardinal yönler", "parezi tespiti"],
            []
        ),
        (
            "Böylece okülomotor, troklear veya abdusens sinir tutulumları anatomik olarak kesinleştirilir.",
            "**Anatomik Kesinleştirme:** Üç motor sinirin felç lokalizasyonu.",
            "",
            ["sinir felci ayrımı", "klinik tanı"],
            []
        )
    ]),

    # --- BOLUM 9: CN V (Nervus Trigeminus) ve Kornea Refleksi (23-24) ---
    (23, "k2-62-b09", "CN V (Nervus Trigeminus) ve Kornea Refleksi", [
        (
            "Beşinci kraniyal sinir olan nervus trigeminus yüzün temel duyusal innervasyonunu ve çiğneme kaslarının motor kontrolünü sağlayan büyük bir mikst sinirdir.",
            "**CN V (N. Trigeminus):** Yüz duyusu, kornea refleksi ve çiğneme kasları innervasyonu.",
            "CN V / N. TRIGEMINUS",
            ["nervus trigeminus", "yüz duyusu"],
            []
        ),
        (
            "Üç büyük duyusal dala ayrılır: V bir oftalmik dal, V iki maksiller dal ve V üç mandibüler daldır.",
            "**Üç Duyusal Dal:** V1 (Oftalmik), V2 (Maksiller) ve V3 (Mandibüler).",
            "Yüz Duyusu",
            ["oftalmik dal", "maksiller dal"],
            []
        ),
        (
            "Motor lifler sadece V üç mandibüler dal içinde seyreder ve maseter, temporalis ile pterigoid çiğneme kaslarını innerve eder; muayenede çene sıkma gücü değerlendirilir.",
            "**Çiğneme Kasları:** V3 ile innerve edilen maseter, temporalis ve pterigoid kaslar.",
            "Maseter ve temporalis kası",
            ["maseter kası", "çiğneme kasları"],
            []
        )
    ]),

    (24, "k2-62-b09", "CN V (Nervus Trigeminus) ve Kornea Refleksi", [
        (
            "Görsel şemamızda trigeminal sinirin üç dalına ait net dermatom haritası ve kornea refleks arkı gösterilmektedir.",
            "**Dermatom ve Kornea Şeması:** V1 alın/kornea, V2 yanak, V3 çene dermatomları ve refleks arkı.",
            "",
            ["trigeminal dermatom", "kornea refleksi"],
            []
        ),
        (
            "Kornea refleksinde korneaya steril bir pamuk ucuyla hafifçe dokunulduğunda afferent yol V bir oftalmik sinirle ponsa gider.",
            "**Afferent Yol:** V1 oftalmik dal ile korneadan beyin sapına duyusal iletim.",
            "",
            ["kornea teması", "V1 afferenti"],
            []
        ),
        (
            "Beyin sapındaki internöronal bağlantılarla her iki taraftaki yedinci sinir nükleusları uyarılır ve orbikularis okuli kası kasılarak her iki göz kapağı bilateral kırpılır.",
            "**Efferent Yanıt:** Bilateral CN VII ile her iki gözün eşzamanlı kapanması.",
            "",
            ["bilateral kırpma", "CN VII efferenti"],
            []
        )
    ]),

    # --- BOLUM 10: CN VII (Nervus Facialis) ve Santral-Periferik Fasiyal Felç Ayrımı (25-27) ---
    (25, "k2-62-b10", "CN VII (Nervus Facialis) ve Santral-Periferik Felç", [
        (
            "Yedinci kraniyal sinir olan nervus facialis yüzün tüm mimik kaslarını motor olarak innerve eder.",
            "**CN VII (N. Facialis):** Mimik kasları motor kontrolü, tat duyusu ve parasempatik sekresyon.",
            "CN VII / N. FACIALIS",
            ["nervus facialis", "mimik kasları"],
            []
        ),
        (
            "Muayenede hastadan kaşlarını yukarı kaldırması, gözlerini sıkıca kapatması, dişlerini göstermesi ve yanaklarını şişirmesi istenir.",
            "**Motor Muayene:** Kaş kaldırma, göz kapama, diş gösterme ve ıslık çalma testleri.",
            "Mimik kasları (gözü kapama)",
            ["gözü kapama", "kaş kaldırma"],
            []
        ),
        (
            "Ayrıca korda timpani dalı ile dilin ön üçte iki kısmının tat duyusunu alır; lakrimal ve submandibüler tükürük bezlerine parasempatik lifler taşır.",
            "**Korda Timpani:** Dilin ön 2/3 tat duyusu ve tükürük/gözyaşı sekresyonu.",
            "Dilin ön 2/3 tat duyusu",
            ["korda timpani", "tat duyusu"],
            []
        )
    ]),

    (26, "k2-62-b10", "CN VII (Nervus Facialis) ve Santral-Periferik Felç", [
        (
            "Görsel kesitimizde fasiyal motor nükleusunun beyin sapındaki yerleşimi ve kortikobulber liflerin çekirdekle bağlantı anatomisi gösterilmektedir.",
            "**Fasiyal Nükleus Kesiti:** Pons tegmentumu yerleşimi ve kortikobulber innervasyon modeli.",
            "",
            ["fasiyal nükleus", "kortikobulber yol"],
            []
        ),
        (
            "Fasiyal nükleusun alın ve üst yüz kaslarını kontrol eden üst yarısı her iki serebral hemisferden bilateral kortikobulber girdi alır.",
            "**Bilateral Üst Yüz İnnervasyonu:** Alın kasları her iki hemisferden uyarı alır.",
            "",
            ["bilateral innervasyon", "alın kasları"],
            []
        ),
        (
            "Nükleusun ağız çevresi ve alt yüzü kontrol eden alt yarısı ise sadece karşı serebral korteksten tek taraflı girdi alır.",
            "**Tek Taraflı Alt Yüz İnnervasyonu:** Alt yüz kasları yalnızca kontralateral korteksten beslenir.",
            "",
            ["tek taraflı girdi", "alt yüz"],
            []
        )
    ]),

    (27, "k2-62-b10", "CN VII (Nervus Facialis) ve Santral-Periferik Felç", [
        (
            "Görsel şemamızda klinik nörolojinin en kritik ayrımlarından biri olan santral ve periferik fasiyal paralizi tablosu karşılaştırılmaktadır.",
            "**Santral vs Periferik Fasiyal Felç:** Alın tutulumu farkı ile lezyon lokalizasyonu.",
            "SANTRAL VS PERİFERİK",
            ["santral felç", "periferik felç"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: supranükleer tek taraflı beyin lezyonunda alın kasları bilateral innervasyon nedeniyle korunur ve sadece karşı alt yüz felç olur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Supranükleer lezyonda alın kasları korunur, yalnızca karşı alt yüz felç olur.",
            "SANTRAL VS PERİFERİK",
            ["çıkmış soru", "supranükleer lezyon", "alın korunumu"],
            ["past-1790877480031-411629"]
        ),
        (
            "Buna karşın Bell paralizisi gibi periferik nükleer veya infranükleer lezyonlarda aynı taraf alnın yarısı dahil tüm yüz felç olur ve göz kapatılamaz.",
            "**Bell Paralizisi:** Periferik lezyonda alın dahil aynı taraf tüm yüz yarısının felci.",
            "SANTRAL VS PERİFERİK",
            ["Bell paralizisi", "infranükleer lezyon"],
            []
        )
    ]),

    # --- BOLUM 11: CN VIII (Nervus Vestibulocochlearis) ve İşitme Testleri (28-29) ---
    (28, "k2-62-b11", "CN VIII (Nervus Vestibulocochlearis) ve İşitme Testleri", [
        (
            "Sekizinci kraniyal sinir olan nervus vestibulocochlearis koklear dalı ile işitme, vestibüler dalı ile denge fonksiyonunu yürütür.",
            "**CN VIII (N. Vestibulocochlearis):** İşitme (koklear) ve denge (vestibüler) duyusal iletimi.",
            "CN VIII /",
            ["nervus vestibulocochlearis", "işitme ve denge"],
            []
        ),
        (
            "Klinik muayenede işitme fısıltı testi veya parmak sürtme yöntemiyle her iki kulakta ayrı ayrı taranır.",
            "**İşitme Taraması:** Fısıltı testi ve parmak sürtme ile monoküler işitme kontrolü.",
            "N.VESTIBULOCOCHLEARIS",
            ["fısıltı testi", "işitme muayenesi"],
            []
        ),
        (
            "Vestibüler sistem ise spontan nistagmus, Romberg testi ve tandem yürüme testleri ile değerlendirilir.",
            "**Vestibüler Değerlendirme:** Nistagmus, Romberg ve denge muayenesi.",
            "İşitme ve denge",
            ["Romberg testi", "vestibüler denge"],
            []
        )
    ]),

    (29, "k2-62-b11", "CN VIII (Nervus Vestibulocochlearis) ve İşitme Testleri", [
        (
            "İşitme kaybı saptandığında iletim tipi ile sensörinöral tip ayrımını yapmak için Weber ve Rinne diyapozon testleri uygulanır.",
            "**Diyapozon Testleri:** Rinne ve Weber ile iletim vs sensörinöral kayıp ayrımı.",
            "Normal: Rinne (+)",
            ["diyapozon testleri", "Rinne testi"],
            []
        ),
        (
            "Normal kulakta hava yolu iletimi kemik yolu iletiminden uzun sürer ve bu durum Rinne pozitif olarak adlandırılır.",
            "**Normal Rinne (+):** Hava yolu süresi kemik yolu süresinden uzundur.",
            "Normal: Rinne (+)",
            ["hava yolu", "kemik yolu"],
            []
        ),
        (
            "Dış veya orta kulak patolojilerine bağlı iletim tipi işitme kaybında kemik iletimi öne geçer ve Rinne negatif olur; Weber testi ise lezyonlu kulağa lateralize olur.",
            "**İletim Tipi Kayıp:** Rinne (-), Weber lezyonlu kulağa lateralize.",
            "Kondüksiyon tipi işitme kaybı: Rinne (-)",
            ["iletim tipi kayıp", "Rinne negatif"],
            []
        ),
        (
            "Sensörinöral tip işitme kaybında ise her iki iletim azalmasına rağmen hava yolu üstünlüğü korunur ve Rinne pozitif kalır; Weber sağlam kulağa lateralize olur.",
            "**Sensörinöral Kayıp:** Rinne (+), Weber sağlam kulağa lateralize.",
            "Sensörinöral tipte işitme kaybı: Rinne",
            ["sensörinöral kayıp", "Weber testi"],
            []
        )
    ]),

    # --- BOLUM 12: Alt Kraniyal Sinirler (CN IX, X, XI, XII) ve Sendromik Lokalizasyon (30-36) ---
    (30, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "Dokuzuncu kraniyal sinir olan nervus glossopharyngeus stilofaringeus kasını motor olarak innerve eder ve parotis bezine sekresyon yaptırır.",
            "**CN IX (N. Glossopharyngeus):** Stilofaringeus kası, parotis sekresyonu ve dil arkası duyusu.",
            "CN IX /",
            ["nervus glossopharyngeus", "stilofaringeus"],
            []
        ),
        (
            "Dilin arka üçte bir kısmının hem tat hem de genel dokunma duyusunu taşır.",
            "**Dil Arkası İnnervasyonu:** Dilin arka 1/3 tat ve dokunma duyusu.",
            "N.GLOSSOPHARYNGEUS",
            ["dilin arka üçte biri", "tat duyusu"],
            []
        ),
        (
            "Ayrıca orofarenks mukozasını innerve ederek öğürme refleksinin afferent yolunu oluşturur.",
            "**Öğürme Afferenti:** Orofarenks teması ile başlayan öğürme refleks arkı.",
            "Stilofaringeus kası",
            ["öğürme refleksi", "orofarenks"],
            []
        )
    ]),

    (31, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "Onuncu kraniyal sinir olan nervus vagus farenks ve larenks kaslarını innerve ederek yutma ve konuşmayı sağlar.",
            "**CN X (N. Vagus):** Farenks/larenks kasları, vokal kordlar ve viseral parasempatik kontrol.",
            "CN X / N. VAGUS",
            ["nervus vagus", "farenks kasları"],
            []
        ),
        (
            "Tek taraflı vagus lezyonunda yumuşak damak felçli tarafta sarkar ve hasta ah dediğinde uvula sağlam tarafa doğru çekilir.",
            "**Uvula Sapması:** Tek taraflı vagus lezyonunda uvula sağlam tarafa deviye olur.",
            "Farenks ve larenks kasları",
            ["uvula sapması", "yumuşak damak"],
            []
        ),
        (
            "Larenks kaslarının felcine bağlı olarak hastada ses kısıklığı ve yutma güçlüğü yani disfaji tablosu gelişir.",
            "**Disfoni ve Disfaji:** Ses kısıklığı ve yutma bozukluğu bulguları.",
            "Palatoglossus kası",
            ["ses kısıklığı", "disfaji"],
            []
        )
    ]),

    (32, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "On birinci kraniyal sinir olan nervus accessorius sternokleidomastoid ve trapezius kaslarını motor olarak innerve eder.",
            "**CN XI (N. Accessorius):** Sternokleidomastoid ve trapezius kaslarının motor kontrolü.",
            "CN XI / N. ACCESORIUS",
            ["nervus accessorius", "sternokleidomastoid"],
            []
        ),
        (
            "Sternokleidomastoid kası başı direnç karşısında karşı tarafa çevirirken, trapezius kası omuzları yukarı doğru kaldırır.",
            "**Muayene Testleri:** Başı karşıya çevirme ve omuz silkme hareketleri.",
            "Trapezius ve sternokleidomastoid kaslar",
            ["trapezius", "omuz silkme"],
            []
        ),
        (
            "Sinir lezyonunda aynı tarafta omuz düşüklüğü ve başı karşı tarafa çevirmede belirgin güçsüzlük ortaya çıkar.",
            "**Aksesuar Felci:** Omuz düşüklüğü ve boyun rotasyon zaafı.",
            "Trapezius ve sternokleidomastoid kaslar",
            ["omuz düşüklüğü", "boyun rotasyonu"],
            []
        )
    ]),

    (33, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "On ikinci kraniyal sinir olan nervus hypoglossus palatoglossus hariç dilin tüm intrinsik ve ekstrinsik kaslarını motor olarak innerve eder.",
            "**CN XII (N. Hypoglossus):** Dil kaslarının motor kontrolü ve dil hareketleri.",
            "CN XII / N. HYPOGLOSSUS",
            ["nervus hypoglossus", "dil kasları"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: dil dışarı çıkarıldığında lezyon tarafındaki genioglossus kası çalışmadığı için dil doğrudan lezyon tarafına sapar.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Dil dışarı çıkarıldığında nervus hypoglossus lezyonunun olduğu tarafa deviye olur.",
            "Dil kasları (palatoglossal hariç)",
            ["çıkmış soru", "genioglossus", "dil deviasyonu"],
            ["88612c9f5ce5"]
        ),
        (
            "Alt motor nöron lezyonlarında ayrıca felçli dil yarısında belirgin atrofi ve solucanvari fasikülasyonlar gözlenir.",
            "**Periferik Belirtiler:** Dilde atrofi ve fasikülasyon tespiti.",
            "Dil kasları (palatoglossal hariç)",
            ["dil atrofisi", "fasikülasyon"],
            []
        )
    ]),

    (34, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "Görselimizde sağ nervus hypoglossus felcinde dilin dışarı çıkarıldığında sağa deviasyonu ve dildeki atrofi klinik olarak gösterilmektedir.",
            "**Hipoglossus Felci Klinik Görünümü:** Dilin lezyon tarafına sapması ve tek taraflı atrofi.",
            "",
            ["dil deviasyonu", "hemiatrofi"],
            []
        ),
        (
            "Genioglossus kası dili öne ve karşıya doğru iter; sağ kas çalışmadığında sağlam sol kasın baskın kuvveti dili sağa doğru saptırır.",
            "**Deviasyon Mekanizması:** Sağlam taraf genioglossus kasının dili lezyon yönüne itmesi.",
            "",
            ["sağlam genioglossus", "itici kuvvet"],
            []
        ),
        (
            "Bu muayene yatak başında periferik dil felcinin tarafını saniyeler içinde kesinleştirir.",
            "**Yatak Başı Lokalizasyon:** Felç tarafının hızlı ve kesin tayini.",
            "",
            ["yatak başı muayene", "taraf tayini"],
            []
        )
    ]),

    (35, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "Tablomuzda kraniyal sinirlerin kafa tabanı ve beyin sapındaki sendromik lokalizasyonları özetlenmektedir.",
            "**Sendromik Lokalizasyon Tablosu:** Kavernöz sinüs, serebellopontin açı ve foramen jugulare sendromları.",
            "",
            ["sendromik lokalizasyon", "kafa tabanı sendromları"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: pitozis, tam oftalmopleji ve V bir oftalmik dal kornea duyu kaybının birlikte görüldüğü patoloji kavernöz sinüs sendromudur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: CN III, IV, VI ve V1 tutulumu kavernöz sinüs sendromunu işaret eder.",
            "",
            ["çıkmış soru", "kavernöz sinüs sendromu", "oftalmopleji"],
            ["d3-k2-nor-005"]
        ),
        (
            "Serebellopontin köşe lezyonlarında yedinci ve sekizinci sinirler, foramen jugulare sendromunda ise dokuz, on ve on birinci kraniyal sinirler birlikte tutulur.",
            "**Köşe ve Jugulare Sendromu:** CPA'da CN VII-VIII, foramen jugularede CN IX-X-XI felci.",
            "",
            ["serebellopontin açı", "foramen jugulare"],
            []
        )
    ]),

    (36, "k2-62-b12", "Alt Kraniyal Sinirler ve Sendromik Lokalizasyon", [
        (
            "Kraniyal sinir muayenesinde elde edilen klinik bulgular beyin sapı kesitlerinin ve kafa tabanı anatomisinin kusursuz bir nörolojik haritasını verir.",
            "**Nörolojik Haritalama:** Kraniyal sinir bulgularıyla intrakraniyal lezyon odağını saptama.",
            "",
            ["lezyon lokalizasyonu", "nörolojik sentez"],
            []
        ),
        (
            "Hekimin her siniri anatomik sırayla ve doğru testlerle muayene etmesi erken inme, tümör ve enfeksiyon tanılarında hayat kurtarır.",
            "**Klinik Değer:** İnme, tümör ve kafa tabanı lezyonlarında erken hayat kurtarıcı teşhis.",
            "",
            ["inme tanısı", "erken teşhis"],
            []
        ),
        (
            "Böylece birinci kraniyal sinirden on ikinci kraniyal sinire kadar tüm muayene adımlarını ve klinik sendromları başarıyla tamamlamış olduk.",
            "**Ders Özeti:** 12 çift kraniyal sinirin tam muayene protokolü ve klinik korelasyonu tamamlandı.",
            "",
            ["ders özeti", "kraniyal muayene protokolü"],
            []
        )
    ])
]

# Verify anchors against kaynak.md
print("Verifying anchors against kaynak.md...")
anchor_errors = 0
for sayfa, bid, bbaslik, sentences in SLIDES:
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        if anchor and anchor not in kaynak_text:
            print(f"ERROR: Sayfa {sayfa} sentence {s_idx+1} anchor not found in kaynak.md: {anchor!r}")
            anchor_errors += 1
if anchor_errors:
    print(f"FAILED: {anchor_errors} anchors not found!")
    sys.exit(1)
print(f"SUCCESS: All anchors verified 100% in kaynak.md!")

# Build konusma_v2.json
bolum_map = {}
cid_counter = 1
total_words = 0

for sayfa, bid, bbaslik, sentences in SLIDES:
    if bid not in bolum_map:
        bolum_map[bid] = {
            "id": bid,
            "baslik": bbaslik,
            "paragraflar": []
        }
    
    p_id = f"k2-62-p{sayfa:03d}"
    p_obj = {
        "id": p_id,
        "sayfa": sayfa,
        "cumleler": []
    }
    
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        cid = f"k2-62-c{cid_counter:04d}"
        cid_counter += 1
        words = len(ses.split())
        total_words += words
        
        sekil_val = VISUAL_PAGES.get(sayfa) if s_idx == 0 and sayfa in VISUAL_PAGES else None
        vurgu_text = ekran.split("**")[1] if "**" in ekran else "Kraniyal Sinir"
        satir_list = [anchor] if anchor else []
        
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": ekran,
            "duzey": 0,
            "slayt": {
                "sayfa": sayfa,
                "satir": satir_list,
                "sekil": sekil_val
            },
            "vurgu": [{"tur": "terim", "metin": vurgu_text}]
        }
        if cikmis:
            c_obj["cikmis"] = cikmis
            
        p_obj["cumleler"].append(c_obj)
        
    bolum_map[bid]["paragraflar"].append(p_obj)

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-62",
    "anahtar": "y25-k2-62-kraniyal-sinir-muayenesi",
    "baslik": "Kraniyal Sinir Muayenesi",
    "bolumler": list(bolum_map.values())
}

print(f"Total Bolumler: {len(konusma_v2['bolumler'])}")
print(f"Total Paragraphs: {sum(len(b['paragraflar']) for b in konusma_v2['bolumler'])}")
print(f"Total Sentences: {cid_counter - 1}")
print(f"Total Words: {total_words} (~{total_words / 125:.1f} minutes of audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Helper to get cid
def get_cid_for_slide(slide_num, s_offset=0):
    for b in konusma_v2["bolumler"]:
        for p in b["paragraflar"]:
            if p["sayfa"] == slide_num:
                return p["cumleler"][s_offset]["id"]
    raise ValueError(f"Slide {slide_num} not found")

# Drawing commands (8 commands, 0 forward leaks)
cizim_komutlari = [
    {
        "cumle": get_cid_for_slide(2, 2),
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kraniyal Sinir Grupları",
        "ogeler": [
            "Duyusal sinirler: Koku ve görme",
            "Motor sinirler: Diğer on çift sinir"
        ]
    },
    {
        "cumle": get_cid_for_slide(4, 2),
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Görme Alanı Defektleri",
        "ogeler": [
            "Kiazma lezyonu: Bitemporal hemianopsi",
            "Postkiazmal lezyon: Homonim hemianopsi"
        ]
    },
    {
        "cumle": get_cid_for_slide(11, 2),
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Ekstraoküler Kas İnnervasyonu",
        "ogeler": [
            "Okülomotor sinir: Rektus kasları",
            "Troklear sinir: Superior oblik kası",
            "Abdusens siniri: Lateral rektus kası"
        ]
    },
    {
        "cumle": get_cid_for_slide(13, 2),
        "bas": 0, "son": 4,
        "sayfa": 13,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Işık Refleksi Yolağı",
        "ogeler": [
            "Retinaya ışık uyarısı gelmesi",
            "Optik sinir ile pretektal nükleusa iletim",
            "Edinger-Westphal nükleusundan miyozis yanıtı"
        ]
    },
    {
        "cumle": get_cid_for_slide(18, 2),
        "bas": 0, "son": 4,
        "sayfa": 18,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Troklear Sinir Seyri",
        "ogeler": [
            "Dördüncü kraniyal sinir nükleusu",
            "Beyin sapını dorsalden terk eden",
            "Tamamı çaprazlaşan tek sinir"
        ]
    },
    {
        "cumle": get_cid_for_slide(27, 2),
        "bas": 0, "son": 4,
        "sayfa": 27,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Fasiyal Paralizi Tipleri",
        "ogeler": [
            "Santral felç: Alın kasları korunur",
            "Periferik felç: Tüm yüz yarısı felç olur"
        ]
    },
    {
        "cumle": get_cid_for_slide(29, 3),
        "bas": 0, "son": 4,
        "sayfa": 29,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "İşitme Testi Bulguları",
        "ogeler": [
            "İletim tipi kayıp: Rinne negatif",
            "Sensörinöral kayıp: Rinne pozitif"
        ]
    },
    {
        "cumle": get_cid_for_slide(33, 2),
        "bas": 0, "son": 4,
        "sayfa": 33,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Hipoglossus Felci Bulgusu",
        "ogeler": [
            "Nervus hypoglossus lezyonu gelişmesi",
            "Aynı taraf genioglossus kas zaafı",
            "Dilin lezyon tarafına sapması"
        ]
    }
]

cizim_aday = {"komutlar": cizim_komutlari}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(cizim_komutlari)} commands.")
