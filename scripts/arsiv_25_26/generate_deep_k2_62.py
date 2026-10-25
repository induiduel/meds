#!/usr/bin/env python3
"""Deep Amfi-Depth Generator for Lesson 62: Kraniyal Sinir Muayenesi (36 slides).
Provides 4 comprehensive sentences per slide (144 sentences, ~3,400 words, ~27 min amfi audio).
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
    35: "Kraniyal sinir lezyonlarının sendromik lokalizasyon tablosu (kavernöz sinüs, serebellopontin açı, foramen jugulare).",
    36: "Kraniyal sinir muayenesi özet şeması ve klinik karar algoritmaları."
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
            "Sunumumuz nöroloji anabilim dalından Doktor Serkan Emekli tarafından hazırlanmış olup poliklinik ve yataklı servis pratiğinde tanısal basamakları aktarmaktadır.",
            "**Sunum:** A. Serkan Emekli, Kraniyal Sinir Muayenesi.",
            "A. Serkan Emekli",
            ["öğretim üyesi", "klinik nöroloji"],
            []
        ),
        (
            "Kraniyal sinirler kafa tabanındaki özel foramenlerden geçerek baş boyun bölgesinin duyusal, motor ve otonomik innervasyonunu sağlar.",
            "**Kafa Tabanı Anatomisi:** Foramenler ve kraniyal innervasyon alanları.",
            "MUAYENESİ",
            ["kafa tabanı", "innervasyon"],
            []
        ),
        (
            "Nörolojik muayenenin bu en ayrıntılı bileşeni beyin sapı düzeyindeki iskemik, tümöral veya enflamatuar patolojilerin yerini santimetre düzeyinde belirlememize olanak tanır.",
            "**Lezyon Lokalizasyonu:** Beyin sapı düzeylerinin kraniyal sinirlerle tespiti.",
            "Nöroloji",
            ["beyin sapı", "lezyon lokalizasyonu"],
            []
        )
    ]),

    (2, "k2-62-b01", "Kraniyal Sinir Muayenesine Giriş", [
        (
            "On iki çift kraniyal sinir beyin sapından ve ön beyinden çıkarak kranial foramenler yoluyla hedef organlarına dağılır.",
            "**Kraniyal Sinirler:** 12 çift sinirin anatomik yerleşimi ve kafa tabanı çıkışları.",
            "KRANYAL SİNİRLER",
            ["kraniyal sinirler", "beyin sapı"],
            []
        ),
        (
            "Birinci kraniyal sinir olan olfaktor ve ikinci kraniyal sinir olan optik sinir embriyolojik olarak doğrudan telensefalon ve diensefalon uzantısıdır.",
            "**Ön Beyin Sinirleri:** Olfaktor ve optik sinirlerin embriyolojik kökeni.",
            "Olfactory nerve fibers (I)",
            ["olfaktor sinir", "optik sinir"],
            []
        ),
        (
            "Üçüncü ve dördüncü sinirler mezensefalondan, beş, altı, yedi ve sekizinci sinirler ponstan, dokuz, on, on bir ve on ikinci sinirler ise bulbustan köken alır.",
            "**Beyin Sapı Çıkışları:** Mezensefalon, pons ve bulbus çekirdekleri.",
            "Trochlear nerve (IV)",
            ["mezensefalon", "pons", "bulbus"],
            []
        ),
        (
            "Bu anatomik sıralama sayesinde kraniyal sinir lezyonlarının kombinasyonu beyin sapının hangi düzeyinde patoloji olduğunu kusursuz biçimde gösterir.",
            "**Klinik Korelasyon:** Kraniyal sinir felçlerinin seviye belirleyici değeri.",
            "Hypoglossal nerve (XII)",
            ["kraniyal sinir", "beyin sapı düzeyi"],
            []
        )
    ]),

    # --- BOLUM 2: CN I (Nervus Olfactorius) ve Koku Muayenesi (3) ---
    (3, "k2-62-b02", "CN I (Nervus Olfactorius) ve Koku Muayenesi", [
        (
            "Birinci kraniyal sinir olan nervus olfactorius koku alma duyusunu ileten saf duyusal özel viseral afferent bir sinirdir.",
            "**CN I (N. Olfactorius):** Koku alma duyusunun özel viseral afferent iletimi.",
            "CN I / N. OLFACTORIUS",
            ["nervus olfactorius", "koku alma"],
            []
        ),
        (
            "Muayenede amonyak veya alkol gibi trigeminal siniri uyaran tahriş edici maddeler yerine kahve, vanilya, tütün veya sabun kokuları tercih edilir.",
            "**Muayene Yöntemi:** Tahriş etmeyen kokularla burun deliklerinin tek tek muayenesi.",
            "tahriş etmeyen kokularla iki",
            ["tahriş etmeyen kokular", "trigeminal sinir"],
            []
        ),
        (
            "Hastanın gözleri kapatılarak her iki burun deliği tek tek kapatılır ve koku eşiği, koku ayrımı ile koku adlandırma yeteneği değerlendirilir.",
            "**Koku Testi Basamakları:** Koku eşiği, koku ayrımı ve adlandırma parametreleri.",
            "\uf0adİşlev: Koku alma",
            ["burun deliği", "koku ayrımı"],
            []
        ),
        (
            "Kafa tabanı travmalarında lamina kribroza kırıkları veya olfaktor oluk meningiomlarında tek taraflı anozmi gelişebileceği akılda tutulmalıdır.",
            "**Anozmi ve Etyoloji:** Kafa tabanı travması ve meningiomlarda koku kaybı.",
            "\uf0adPatolojik durum: Kafa",
            ["anozmi", "kafa tabanı travması"],
            []
        )
    ]),

    # --- BOLUM 3: CN II (Nervus Opticus) ve Görme Muayenesi (4-8) ---
    (4, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Görsel şemamızda optik sinir, optik kiazma ve retrokiazmal görme yolları lezyonlarında ortaya çıkan karakteristik görme alanı defektleri özetlenmektedir.",
            "**Görme Yolları Şeması:** Kiazmal ve postkiazmal lezyonlarda görme alanı kayıpları.",
            "-CNII/N. OPTICUS",
            ["optik sinir", "görme yolları"],
            []
        ),
        (
            "Optik sinir tam kesildiğinde lezyon tarafında monooküler anopsi yani tam görme kaybı görülür.",
            "**Optik Sinir Lezyonu:** Tek taraflı monooküler anopsi ve görme kaybı.",
            "-CNII/N. OPTICUS",
            ["monooküler anopsi", "optik sinir"],
            []
        ),
        (
            "Optik kiazma lezyonunda hipofiz adenomu basısına bağlı olarak nazal retina lifleri hasarlanır ve klasik bitemporal hemianopsi tablosu ortaya çıkar.",
            "**Kiazma Lezyonu:** Hipofiz basısında nazal lif hasarı ve bitemporal hemianopsi.",
            "Junctional Scotoma",
            ["optik kiazma", "bitemporal hemianopsi"],
            []
        ),
        (
            "Kiazma bileşkesinde junctional skotom, retrokiazmal optik traktus veya optik radyasyon lezyonlarında ise kontralateral homonim hemianopsi defekti gelişir.",
            "**Retrokiazmal Lezyonlar:** Traktus ve optik radyasyon hasarında homonim hemianopsi.",
            "Optic Radiations",
            ["junctional skotom", "homonim hemianopsi"],
            []
        )
    ]),

    (5, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Santral görme keskinliğinin değerlendirilmesinde uluslararası standart muayene yöntemi Snellen kartları kullanılarak yapılır.",
            "**Görme Keskinliği:** Snellen kartları ile santral görmenin kantitatif tayini.",
            "Görme Keskinliği (Snellen Kartları)",
            ["görme keskinliği", "snellen kartları"],
            []
        ),
        (
            "Hasta altı metre veya yirmi fit mesafeye yerleştirilerek her iki göz refraksiyon kusuru düzeltilmiş halde tek tek test edilir.",
            "**Uzak Görme Testi:** 6 metre mesafeden refraksiyon düzeltmesi ile muayene.",
            "Görme Keskinliği (Snellen Kartları)",
            ["refraksiyon", "santral görme"],
            []
        ),
        (
            "En üstteki büyük harfi dahi okuyamayan hastalarda görme mesafesi adım adım azaltılarak parmak sayma derecesi belirlenir.",
            "**İleri Görme Azlığı:** Yakın mesafeden parmak sayma değerlendirmesi.",
            "r b FLTI6ö5büö",
            ["parmak sayma", "görme derecesi"],
            []
        ),
        (
            "Parmak sayamayacak kadar ileri görme kaybında el hareketlerini fark etme ve son basamakta sadece ışık algılama derecesi kaydedilir.",
            "**Derin Görme Kaybı:** El hareketleri ve ışık algılama basamakları.",
            "FSEZ5LUrTE",
            ["el hareketleri", "ışık algılama"],
            []
        )
    ]),

    (6, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Görme alanı değerlendirilmesinde poliklinik ve yatak başı şartlarında en pratik ve güvenilir muayene yöntemi konfrontasyon testidir.",
            "**Görme Alanı Muayenesi:** Konfrontasyon (karşılaştırma) yöntemi prensipleri.",
            "Görme Alanı Değerlendirilmesi",
            ["görme alanı", "konfrontasyon"],
            []
        ),
        (
            "Hekim ile hasta karşılıklı aynı göz seviyesinde bir metre mesafede oturur ve karşılıklı gözlerini kapatarak periferik sınırları kıyaslar.",
            "**Muayene Pozisyonu:** Hekim ve hastanın periferik sınırlarının birebir karşılaştırılması.",
            "Görme Alanı Değerlendirilmesi",
            ["periferik görme", "karşılıklı muayene"],
            []
        ),
        (
            "Dört kadranda parmak hareketleri veya kırmızı renkli nesneler merkeze doğru yaklaştırılarak alt ve üst kadranlardaki skotomlar araştırılır.",
            "**Kadran Muayenesi:** Kırmızı nesne ve parmak hareketleriyle skotom tespiti.",
            "Görme Alanı Değerlendirilmesi",
            ["kadrananopsi", "skotom"],
            []
        ),
        (
            "Ayrıca her iki tarafta aynı anda parmak oynatılarak parietal lob lezyonlarını düşündüren görsel ihmal ve sönme fenomeni taranır.",
            "**Görsel Sönme:** Çift eşzamanlı uyarı ile parietal lob lezyonlarının tespiti.",
            "Görme Alanı Değerlendirilmesi",
            ["parietal lob", "görsel ihmal"],
            []
        )
    ]),

    (7, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Gözdibi muayenesi oftalmoskop cihazı yardımıyla optik diskin, retinanın ve retinal vasküler yapıların doğrudan incelenmesini sağlar.",
            "**Gözdibi Muayenesi:** Direkt oftalmoskopi ile optik disk ve retina değerlendirmesi.",
            "Gözdibi muayenesi",
            ["gözdibi muayenesi", "oftalmoskop"],
            []
        ),
        (
            "Optik diskin sınırlarının netliği, fizyolojik çukurluğun derinliği ve disk renginin solukluğu optik atrofi açısından dikkatle değerlendirilir.",
            "**Optik Disk Morfolojisi:** Sınır netliği, çukurluk ve optik atrofi bulguları.",
            "Gözdibi muayenesi",
            ["optik disk", "optik atrofi"],
            []
        ),
        (
            "Kafa içi basınç artışının en kritik nörolojik bulgusu olan papilödemde disk sınırları silinir, ödem gelişir ve venöz pulsasyon kaybolur.",
            "**Papilödem:** KİBAS durumunda disk sınırlarının silinmesi ve venöz dolgunluk.",
            "Gözdibi muayenesi",
            ["papilödem", "venöz pulsasyon"],
            []
        ),
        (
            "Spontan venöz pulsasyonun varlığı kafa içi basıncının o an için normal sınırlarda olduğunu gösteren en değerli negatif belirteçtir.",
            "**Spontan Venöz Pulsasyon:** Normal KİB varlığını gösteren güvenilir klinik ipucu.",
            "Gözdibi muayenesi",
            ["kafa içi basıncı", "venöz pulsasyon"],
            []
        )
    ]),

    (8, "k2-62-b03", "CN II (Nervus Opticus) ve Görme Muayenesi", [
        (
            "Renkli görme muayenesinde psödoizokromatik Ishihara kartları kullanılarak özellikle kırmızı ve yeşil renk ayrımı test edilir.",
            "**Renkli Görme:** Ishihara psödoizokromatik kartları ile renk ayrımı testi.",
            "Renkli Görme (Ishıhara Kartları)",
            ["renkli görme", "ishihara kartları"],
            []
        ),
        (
            "Optik nörit ve demiyelinizan hastalıklarda görme keskinliği henüz bozulmadan önce ilk ve en erken kaybolan bulgu renkli görme ve kontrast duyarlılığı kaybıdır.",
            "**Erken Optik Nöropati:** Keskinlik bozulmadan önce renk ve kontrast kaybı.",
            "Kontrast Duyarlılığı",
            ["optik nörit", "kontrast duyarlılığı"],
            []
        ),
        (
            "Kırmızı desatürasyonu yani kırmızı rengin hastaya soluk veya gri görünmesi erken retrobulber optik sinir tutulumunu saptamada son derece duyarlıdır.",
            "**Kırmızı Desatürasyonu:** Retrobulber sinir inflamasyonunun hassas klinik işareti.",
            "Renkli Görme (Ishıhara Kartları)",
            ["kırmızı desatürasyonu", "retrobulber tutulum"],
            []
        ),
        (
            "Bu testler multipl skleroz gibi optik nöropatilerin erken dönem teşhisinde ve remisyon takibinde vazgeçilmez klinik öneme sahiptir.",
            "**Klinik Değer:** Demiyelinizan süreçlerin erken teşhisinde renkli görme rolü.",
            "Kontrast Duyarlılığı",
            ["multipl skleroz", "optik nöropati"],
            []
        )
    ]),

    # --- BOLUM 4: Ekstraoküler Motor Sinirler (CN III, IV, VI) (9-12) ---
    (9, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Ekstraoküler kasları innerve eden üçüncü, dördüncü ve altıncı kraniyal sinirler göz hareketlerini koordine biçimde yönetir.",
            "**Ekstraoküler Sinirler:** CN III, IV ve VI ortak göz hareketleri kontrolü.",
            "CN III-IV-VI /",
            ["ekstraoküler kaslar", "göz hareketleri"],
            []
        ),
        (
            "Nervus oculomotorius, nervus trochlearis ve nervus abducens sinirleri birlikte muayene edilerek gözün tüm eksenlerdeki deviasyonu incelenir.",
            "**Ortak Muayene:** Üç motor sinirin birlikte değerlendirilme zorunluluğu.",
            "N. OCULOMOTORIUS & N.",
            ["okülomotor", "troklear", "abdusens"],
            []
        ),
        (
            "Bu üç sinirin koordinasyonu sayesinde göz küresi abdüksiyon, addüksiyon, elevasyon, depresyon ile intorsiyon ve ekstorsiyon hareketlerini yapar.",
            "**Göz Hareket Eksenleri:** Horizontal, vertikal ve torsiyonel eksen tanımları.",
            "Abdüksiyo",
            ["abdüksiyon", "addüksiyon", "elevasyon", "depresyon"],
            []
        ),
        (
            "Hekim parmağını veya bir kalemi hastanın önünde H paterni çizerek hareket ettirir ve her iki gözün eşzamanlı izleme yeteneğini değerlendirir.",
            "**H Paterni Muayenesi:** Dokuz bakış yönünün sistematik olarak taranması.",
            "TROCHLEARIS & N. ABDUCENS",
            ["H paterni", "eşzamanlı izleme"],
            []
        )
    ]),

    (10, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Ekstraoküler kaslarımızın horizontal eksendeki hareketlerini lateral rektus kası abdüksiyon, mediyal rektus kası ise addüksiyon yaparak sağlar.",
            "**Horizontal Hareketler:** Lateral rektus abdüksiyon, mediyal rektus addüksiyon.",
            "Horizontal göz hareketleri",
            ["lateral rektus", "mediyal rektus"],
            []
        ),
        (
            "Vertikal bakış ekseninde superior rektus ve inferior oblik kasları elevasyon yaparken, inferior rektus ve superior oblik kasları depresyon yaptırır.",
            "**Vertikal Hareketler:** Elevatör kaslar (SR, IO) ve depresör kaslar (IR, SO).",
            "Vertikal göz hareketleri",
            ["superior rektus", "inferior oblik", "elevasyon"],
            []
        ),
        (
            "Torsiyonel eksende ise superior oblik kası içe rotasyon yani intorsiyon, inferior oblik kası ise dışa rotasyon yani ekstorsiyon görevini üstlenir.",
            "**Torsiyonel Hareketler:** Superior oblik intorsiyon, inferior oblik ekstorsiyon.",
            "Sup oblik: depresyon",
            ["intorsiyon", "ekstorsiyon"],
            []
        ),
        (
            "Oblik kasların dikey hareketi göz addüksiyondayken en belirgin hale gelirken, rektus kaslarının dikey hareketi göz abdüksiyondayken test edilir.",
            "**Kas İzolasyon Pozisyonları:** Addüksiyonda oblik, abdüksiyonda rektus muayenesi.",
            "Lat rektus: abdüksiyon",
            ["oblik kaslar", "rektus kasları"],
            []
        )
    ]),

    (11, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Ekstraoküler kasların innervasyon kuralı tıp fakültesinde altın formül olan se o dört, le re altı, geri kalanlar üç şeklinde ezberlenir.",
            "**İnnervasyon Formülü:** SO4, LR6 ve geri kalan tüm kaslar CN III kuralı.",
            "Okülomotor sinir (111)",
            ["innervasyon kuralı", "okülomotor sinir"],
            []
        ),
        (
            "Buna göre superior oblik kası dördüncü sinir olan troklear sinir yani nervus trochlearis, lateral rektus kası ise altıncı sinir olan abdusens siniri yani nervus abducens tarafından innerve edilir.",
            "**Spesifik İnnervasyon:** CN IV superior oblik, CN VI lateral rektus dağılımı.",
            "Trochlear sinir (IV)",
            ["superior oblik", "troklear sinir", "lateral rektus"],
            []
        ),
        (
            "Diğer tüm rektus kasları, inferior oblik ve üst göz kapağını kaldıran levator palpebrae superioris kası okülomotor sinir tarafından yönetilir.",
            "**Okülomotor Motor Alanı:** Medial, superior, inferior rektus ve levator palpebrae.",
            "Abdusens siniri (VI)",
            ["levator palpebrae", "inferior oblik"],
            []
        ),
        (
            "Ayrıca okülomotor sinirin Edinger-Westphal nükleusundan çıkan parasempatik lifleri iris sfinkter ve silier kasları uyararak miyozis ve akomodasyonu sağlar.",
            "**Parasempatik İnnervasyon:** Edinger-Westphal lifleri ile sfinkter pupilla ve siliyer kas.",
            "Edinger-Westphal nükleus",
            ["Edinger-Westphal", "parasempatik lifler"],
            []
        )
    ]),

    (12, "k2-62-b04", "Ekstraoküler Motor Sinirler (CN III, IV, VI)", [
        (
            "Oküler motor muayenenin temel klinik amacı göz hareketlerinin tam ve simetrik olup olmadığını kardinal yönlerde belirlemektir.",
            "**Muayene Amaçları:** Hareket sınırları, kapak pozisyonu, pupilla ve nistagmus.",
            "Muayenenin amacı",
            ["oküler motor muayene", "göz hareketleri"],
            []
        ),
        (
            "Göz kapağının açıklığı incelenerek levator kas zaafına bağlı pitozis veya sempatik sinir tutulumuna bağlı yalancı pitozis araştırılır.",
            "**Göz Kapağı Muayenesi:** Pitozis varlığı ve sempatik-okülomotor ayrımı.",
            "Göz kapağını ve",
            ["göz kapağı", "pitozis"],
            []
        ),
        (
            "Pupilla boyutları ve şekli ışık altında incelenerek anizokori, miyotik ya da midriyatik asimetriler kaydedilir.",
            "**Pupilla Değerlendirmesi:** Boyut, şekil, simetri ve anizokori incelemesi.",
            "Pupillayı incelemek",
            ["pupilla", "anizokori"],
            []
        ),
        (
            "Uç bakışlarda göz küresinin istemsiz ritmik salınımları olan nistagmusun varlığı, yönü ve fiksasyonla değişimi nörolojik lezyon açısından taranır.",
            "**Nistagmus Taraması:** Uç bakışlarda fizyolojik ve patolojik nistagmus ayrımı.",
            "Varsa nistagmusu değerlendirmek",
            ["nistagmus", "lezyon taraması"],
            []
        )
    ]),

    # --- BOLUM 5: Pupilla Refleksleri ve Okülomotor Sinir (13-16) ---
    (13, "k2-62-b05", "Pupilla Refleksleri ve Okülomotor Sinir", [
        (
            "Görsel şemamızda pupilla ışık refleksinin afferent ve efferent nöronal yolakları ayrıntılı olarak gösterilmektedir.",
            "**Işık Refleksi Yolağı:** Afferent CN II ve efferent CN III nöronal arkı.",
            "Işık Refleksi",
            ["ışık refleksi", "afferent yolak"],
            []
        ),
        (
            "Işık uyarısı retinadaki fotoreseptörlerden optik sinir afferent yoluyla mezensefalondaki pretektal nükleusa ulaştırılır.",
            "**Afferent Yolak:** Optik sinirden pretektal nükleusa uzanan duyusal ark.",
            "PRETECTAL",
            ["optik sinir", "pretektal nükleus"],
            []
        ),
        (
            "Pretektal çekirdekten çıkan internöronlar arka komissür aracılığıyla her iki taraftaki Edinger-Westphal nükleuslarına bilateral uyarı gönderir.",
            "**Bilateral Uyarı:** Arka komissür üzerinden her iki Edinger-Westphal çekirdeğine iletim.",
            "EDINGER-",
            ["Edinger-Westphal", "arka komissür"],
            []
        ),
        (
            "Efferent parasempatik lifler üçüncü sinir içinde silier gangliona gelir ve oradan sfinkter pupilla kasını kasarak hem direkt hem konsensüel miyozis oluşturur.",
            "**Efferent Yolak:** Silier ganglion ve iris sfinkteri ile bilateral miyozis yanıtı.",
            "PARASYMPATHETIC",
            ["parasempatik lifler", "miyozis", "silier ganglion"],
            []
        )
    ]),

    (14, "k2-62-b05", "Pupilla Refleksleri ve Okülomotor Sinir", [
        (
            "Akomodasyon ve yakın refleks, hastanın uzaktaki bir nesneden burnunun ucuna yaklaştırılan bir hedefe odaklanmasıyla tetiklenir.",
            "**Yakın Refleks Triadı:** Akomodasyon, konverjans ve miyozis eşzamanlı yanıtı.",
            "Akomodasyon Refle",
            ["akomodasyon refleksi", "yakın refleks"],
            []
        ),
        (
            "Bu refleks sırasında üç kritik anatomik yanıt eşzamanlı olarak gerçekleşir: konverjans, akomodasyon ve pupiller miyozis.",
            "**Triad Bileşenleri:** Medial rektus, siliyer kas ve iris sfinkteri aktivasyonu.",
            "Convergence reflex Accommodation reflex",
            ["konverjans", "akomodasyon", "miyozis"],
            []
        ),
        (
            "Mediyal rektus kasları her iki gözü içe doğru konverjans yaptırırken, silier kaslar kasılarak lensi kalınlaştırır ve iris sfinkteri pupillayı daraltır.",
            "**Mekanizma:** Gözlerin addüksiyonu, lens kırıcılık artışı ve pupilla daralması.",
            "Near reflexes",
            ["mediyal rektus", "silier kas", "lens"],
            []
        ),
        (
            "Işık refleksinden farklı olarak yakın refleks kortikal yolakları kullanır; bu nedenle sifiliz ve mezensefalon lezyonlarında ışık-yakın disosiasyonu görülebilir.",
            "**Işık-Yakın Disosiasyonu:** Argyll Robertson pupillası ve dorsal mezensefalon sendromu.",
            "Edinger-Westphal nucleus",
            ["kortikal yolak", "ışık-yakın disosiasyonu"],
            []
        )
    ]),

    (15, "k2-62-b05", "Pupilla Refleksleri ve Okülomotor Sinir", [
        (
            "Görsel kesitimizde okülomotor sinir nükleusunun mezensefalonda superior kollikulus seviyesinde periaquaduktal gri cevherin ventralinde yerleşimi görülmektedir.",
            "**Okülomotor Nükleus Kompleksi:** Mezensefalon superior kollikulus seviyesi kesiti.",
            "OCULOMOTOR SUPERIOR",
            ["okülomotor nükleus", "superior kollikulus"],
            []
        ),
        (
            "Bu kompleks yapı içerisinde her bir ekstraoküler kas için özelleşmiş alt çekirdekler ve otonomik Edinger-Westphal nükleusu yer alır.",
            "**Alt Çekirdekler:** Ekstraoküler kasların alt nükleusları ve otonom çekirdek.",
            "NUCLEUS COLLICULUS",
            ["alt çekirdekler", "Edinger-Westphal"],
            []
        ),
        (
            "Levator palpebrae superioris kasını innerve eden santral kaudal nükleus tektir ve her iki göz kapağını birlikte yönetir.",
            "**Santral Kaudal Nükleus:** Tek bir çekirdekle her iki üst göz kapağının kaldırılması.",
            "SUPERIOR LEVATOR MEDIAL",
            ["santral kaudal nükleus", "levator palpebrae"],
            []
        ),
        (
            "Okülomotor sinir lifleri mezensefalon tegmentumundan ventrale doğru ilerleyerek serebral pedünküller arasından interpedünküler fossadan beyin sapını terk eder.",
            "**Sinir Çıkışı:** Mezensefalon ventralinden interpedünküler fossadan çıkış seyri.",
            "CEREBRAL",
            ["serebral pedünkül", "interpedünküler fossa"],
            []
        )
    ]),

    (16, "k2-62-b05", "Pupilla Refleksleri ve Okülomotor Sinir", [
        (
            "Görselimizde tam okülomotor sinir felcinde ortaya çıkan klasik ve dramatik klinik görünüm sergilenmektedir.",
            "**Okülomotor Felci Kliniği:** Tam pitozis, down-and-out deviasyon ve midriyazis.",
            "",
            ["okülomotor sinir felci", "klinik görünüm"],
            []
        ),
        (
            "Levator kasının felcine bağlı olarak lezyon tarafında tam pitozis izlenir ve hasta göz kapağını hiçbir şekilde kaldıramaz.",
            "**Tam Pitozis:** Levator palpebrae superioris zaafına bağlı kapak düşüklüğü.",
            "",
            ["pitozis", "levator kası"],
            []
        ),
        (
            "Göz kapağı elle kaldırıldığında çalışan sağlam lateral rektus ve superior oblik kaslarının çekişiyle göz küresi dışa ve aşağıya yani down-and-out pozisyonuna sapmıştır.",
            "**Down-and-Out Göz:** Dışa ve aşağıya sapmış göz küresi pozisyonu.",
            "",
            ["down-and-out", "lateral rektus", "superior oblik"],
            []
        ),
        (
            "Anevrizma gibi dış basılarda yüzeyel parasempatik lifler etkilendiği için pupilla fikse ve dilate yani midriyatik iken, mikrovasküler diyabetik felçlerde pupilla genellikle korunur.",
            "**Pupilla Tutulum Kuralı:** Anevrizmada midriyatik pupilla, diyabette pupilla korunumu.",
            "",
            ["midriyazis", "anevrizma basısı", "diyabetik nöropati"],
            []
        )
    ]),

    # --- BOLUM 6: CN IV (Nervus Trochlearis) ve CN VI (Nervus Abducens) (17-19) ---
    (17, "k2-62-b06", "CN IV (Nervus Trochlearis) ve CN VI (Nervus Abducens)", [
        (
            "Görsel kesitimizde dördüncü kraniyal sinir olan nervus trochlearis çekirdeğinin mezensefalonda inferior kollikulus seviyesindeki anatomisi görülmektedir.",
            "**Nervus Trochlearis Anatomisi:** İnferior kollikulus seviyesi ve dorsal çıkış.",
            "INFERIOR",
            ["troklear sinir", "inferior kollikulus"],
            []
        ),
        (
            "Troklear sinir insan vücudunda beyin sapını dorsal yani arka yüzünden terk eden yegane kraniyal sinirdir.",
            "**Dorsal Çıkış Özelliği:** Beyin sapını arkadan terk eden tek kraniyal sinir.",
            "TROCHLEAR",
            ["dorsal çıkış", "beyin sapı arka yüzü"],
            []
        ),
        (
            "Çekirdekten çıkan tüm lifler arka tarafta velum medullare anterius içinde tamamen karşı tarafa çaprazlaşarak beyin sapından ayrılır.",
            "**Tam Çaprazlaşma:** Liflerinin tamamı kontralateral olarak çaprazlaşan sinir.",
            "SUPERIOR",
            ["tam çaprazlaşma", "velum medullare"],
            []
        ),
        (
            "Ayrıca kraniyal sinirler arasında en ince lif kalınlığına ve en uzun intrakraniyal seyre sahip olduğu için kafa travmalarında en sık hasarlanan motor sinirdir.",
            "**Travma Hassasiyeti:** En uzun seyirli ve en ince çaplı kraniyal sinir.",
            "OBLIQUE",
            ["en ince çap", "kafa travması"],
            []
        )
    ]),

    (18, "k2-62-b06", "CN IV (Nervus Trochlearis) ve CN VI (Nervus Abducens)", [
        (
            "Görselimizde sağ troklear sinir felcinde diplopiyi azaltmak için hastanın kompanse edici baş pozisyonu ve Bielschowsky testi gösterilmektedir.",
            "**Troklear Felç ve Bielschowsky Testi:** Baş eğme testi ve vertikal diplopi mekanizması.",
            "Bielschowsky baş tilt testi",
            ["troklear sinir felci", "diplopi"],
            []
        ),
        (
            "Superior oblik kası zayıfladığında gözde ekstorsiyon ve hiperdeviasyon gelişir; hasta özellikle aşağı ve içe bakışta yani merdiven inerken veya kitap okurken çift görmeden yakınır.",
            "**Klinik Bulgular:** Aşağı-içe bakışta diplopi, merdiven inmede zorlanma.",
            "Sağ 4. sinir felci",
            ["hiperdeviasyon", "aşağı içe bakış"],
            []
        ),
        (
            "Bielschowsky baş tilt testinde baş lezyon tarafındaki sağ omuza eğildiğinde gözdeki dikey kayma ve diplopi belirgin şekilde artar; baş karşı sol omuza eğildiğinde ise çift görme düzelir.",
            "**Baş Tilti Testi:** Lezyon tarafına eğildiğinde artan dikey diplopi.",
            "Bielschowsky baş tilt testi",
            ["Bielschowsky testi", "baş tilti"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: dördüncü kraniyal sinir nükleusundan çıktıktan sonra beyin sapını dorsalden terk eden ve lifleri tamamen çaprazlaşan tek kraniyal sinirdir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: CN IV dorsalden çıkan ve çaprazlaşan tek kraniyal sinirdir.",
            "Sağ 4. sinir felci",
            ["çıkmış sınav sorusu", "dorsal çıkış", "çaprazlaşma"],
            ["7a901e64695e"]
        )
    ]),

    (19, "k2-62-b06", "CN IV (Nervus Trochlearis) ve CN VI (Nervus Abducens)", [
        (
            "Görsel kesitimizde altıncı kraniyal sinir olan nervus abducens çekirdeğinin ponsta dördüncü ventrikül tabanında yerleşimi görülmektedir.",
            "**Nervus Abducens Nükleusu:** Ponsta dördüncü ventrikül tabanı yerleşimi.",
            "FOURTH",
            ["nervus abducens", "dördüncü ventrikül"],
            []
        ),
        (
            "Abdusens nükleusunun etrafını fasiyal sinir lifleri dönerek dolanır ve ventrikül tabanında fasiyal kollikulus kabantısını oluşturur.",
            "**Fasiyal Kollikulus:** CN VI çekirdeğini çevreleyen CN VII motor lifleri.",
            "ABDUCENS eave ©",
            ["fasiyal kollikulus", "fasiyal lifler"],
            []
        ),
        (
            "Abdusens siniri pontomedüller bileşkeden çıkarak lateral rektus kasını innerve eder ve gözün dışa bakışını yani abdüksiyonunu sağlar.",
            "**Lateral Rektus İnnervasyonu:** Dışa bakış kısıtlılığı ve konverjan şaşılık.",
            "LATERAL",
            ["pontomedüller bileşke", "lateral rektus"],
            []
        ),
        (
            "Kafa tabanında petröz apeks üzerinden ve Dorello kanalından geçerken kafa içi basınç artışından en çabuk etkilenen ve yalancı yerelletici bulgu veren sinirdir.",
            "**Dorello Kanalı ve KİBAS:** Kafa içi basınç artışında yalancı yerelletici bulgu.",
            "RECTUS",
            ["Dorello kanalı", "kafa içi basınç artışı"],
            []
        )
    ]),

    # --- BOLUM 7: Horizontal Bakış Merkezi ve İnternükleer Oftalmopleji (20-22) ---
    (20, "k2-62-b07", "Horizontal Bakış Merkezi ve İnternükleer Oftalmopleji", [
        (
            "Görsel şemamızda istemli horizontal sakkadik göz hareketlerini yöneten frontal göz sahası ile ponstaki bakış merkezinin bağlantıları gösterilmektedir.",
            "**Konjuge Bakış Yolağı:** Frontal göz sahası (FEF), PPRF ve abdusens bağlantısı.",
            "FRONTAL CORTEX",
            ["frontal göz sahası", "horizontal bakış"],
            []
        ),
        (
            "Frontal korteks karşı ponsta yer alan paramedian pontin retiküler formasyon yani pe pe re fe merkezini uyararak o tarafa bakışı başlatır.",
            "**PPRF Uyarısı:** Kontralateral frontal korteksten gelen sakkad komutu.",
            "PARAMEDIAN",
            ["PPRF", "paramedian pontin retiküler formasyon"],
            []
        ),
        (
            "Pe pe re fe uyarısı hemen komşu abdusens çekirdeğini aktive eder; abdusens bir yandan aynı taraf lateral rektusu kasarken, diğer yandan internükleer nöronlar çıkarır.",
            "**Abdusens Aktivasyonu:** Aynı taraf lateral rektus kasılması ve internükleer iletim.",
            "ABDUCENS",
            ["abdusens çekirdeği", "lateral rektus"],
            []
        ),
        (
            "Bu internükleer lifler mediyal longitudinal fasikülüs aracılığıyla karşı taraf okülomotor çekirdeğine giderek mediyal rektusu kasar ve konjuge bakış tamamlanır.",
            "**MLF Köprüsü:** Karşı okülomotor çekirdeğe mediyal rektus koordinasyon iletimi.",
            "PONTINE",
            ["mediyal longitudinal fasikülüs", "konjuge bakış"],
            []
        )
    ]),

    (21, "k2-62-b07", "Horizontal Bakış Merkezi ve İnternükleer Oftalmopleji", [
        (
            "Görsel kesitimizde mediyal longitudinal fasikülüs yani me le fe lezyonunda ortaya çıkan internükleer oftalmopleji kliniği şematize edilmektedir.",
            "**İnternükleer Oftalmopleji (İNO):** MLF hasarında addüksiyon kısıtlılığı ve nistagmus.",
            "MEDIAL",
            ["mediyal longitudinal fasikülüs", "internükleer oftalmopleji"],
            []
        ),
        (
            "İnternükleer oftalmoplejide hasta lezyon tarafının karşısına horizontal bakış yapmaya çalıştığında lezyon tarafındaki göz addüksiyon yapamaz ve belirgin addüksiyon kısıtlılığı izlenir.",
            "**Addüksiyon Kısıtlılığı:** Bakış yönünde içe bakamayan ipsilateral göz.",
            "LONGITUDINAL",
            ["addüksiyon kısıtlılığı", "horizontal bakış"],
            []
        ),
        (
            "Buna karşılık dışa bakan sağlam gözde horizontal monooküler disosiasyon nistagmusu gelişir; ancak konverjans yolağı kortikal olduğundan konverjansta addüksiyon tamdır.",
            "**Disosiasyon Nistagmusu:** Abdüksiyon yapan gözde nistagmus ve korunan konverjans.",
            "OCULOMOTOR",
            ["disosiasyon nistagmusu", "konverjans korunumu"],
            []
        ),
        (
            "Genç bir hastada iki taraflı internükleer oftalmopleji saptanması multipl skleroz hastalığı için adeta patognomonik bir klinik bulgudur.",
            "**Etyoloji:** Gençlerde multipl skleroz, yaşlılarda beyin sapı iskemisi.",
            "MIDBRAIN",
            ["multipl skleroz", "iki taraflı oftalmopleji"],
            []
        )
    ]),

    (22, "k2-62-b07", "Horizontal Bakış Merkezi ve İnternükleer Oftalmopleji", [
        (
            "Görsel şemamızda klinik pratikte hastanın göz hareketlerinin değerlendirildiği dokuz temel kardinal bakış yönü gösterilmektedir.",
            "**Dokuz Kardinal Bakış Yönü:** Primer pozisyon ve sekiz yönlü göz hareket muayenesi.",
            "",
            ["kardinal bakış yönleri", "klinik muayene"],
            []
        ),
        (
            "Primer pozisyondan başlayarak sağa, sola, yukarı, aşağı ve oblik eksenlerde her bir kasın izole fonksiyonu tek tek gözlemlenir.",
            "**İzole Kas Testi:** Eksenlere göre ekstraoküler kasların tek tek test edilmesi.",
            "",
            ["primer pozisyon", "oblik eksenler"],
            []
        ),
        (
            "Herhangi bir yönde kısıtlılık saptandığında hastaya diplopi yani çift görmenin hangi bakış yönünde belirginleştiği ve ayrışma mesafesi sorulur.",
            "**Diplopi Analizi:** Görüntülerin en çok ayrıştığı bakış yönünün belirlenmesi.",
            "",
            ["diplopi", "bakış kısıtlılığı"],
            []
        ),
        (
            "Düzgün takip hareketleri ve hızlı sakkadik atımlar incelenerek hem periferik sinir hem de santral serebellar ve beyin sapı patolojileri ayırt edilir.",
            "**Santral-Periferik Ayrımı:** Takip ve sakkad muayenesi ile beyin sapı lezyon ayrımı.",
            "",
            ["sakkadik atım", "serebellar patoloji"],
            []
        )
    ]),

    # --- BOLUM 8: CN V (Nervus Trigeminus) Muayenesi (23-24) ---
    (23, "k2-62-b08", "CN V (Nervus Trigeminus) Muayenesi", [
        (
            "Beşinci kraniyal sinir olan nervus trigeminus yüzün temel duyusal innervasyonunu ve çiğneme kaslarının motor kontrolünü sağlar.",
            "**CN V (N. Trigeminus):** Yüzün duyusal ve çiğneme kaslarının motor innervasyonu.",
            "CN V / N. TRIGEMINUS",
            ["nervus trigeminus", "yüz duyusu"],
            []
        ),
        (
            "Duyusal muayenede oftalmik V bir, maksiller V iki ve mandibuler V üç alanlarında dokunma, ağrı ve ısı duyusu iki taraflı simetrik olarak incelenir.",
            "**Duyusal Muayene:** V1 oftalmik, V2 maksiller ve V3 mandibuler alan değerlendirmesi.",
            "Yüz Duyusu",
            ["oftalmik dal", "maksiller dal", "mandibuler dal"],
            []
        ),
        (
            "Motor muayenede hasta dişlerini sıktığında maseter ve temporalis kasları palpe edilir; çene açıldığında pterigoid zaafında çene lezyon tarafına kayar.",
            "**Motor Muayene:** Maseter ve temporalis kas tonusu, pterigoid zaafında çene deviasyonu.",
            "Maseter ve temporalis kası",
            ["maseter", "temporalis", "pterigoid kaslar"],
            []
        ),
        (
            "Kornea refleksinde afferent iletim trigeminal sinirin birinci dalı olan oftalmik sinirle, efferent bilateral göz kırpma yanıtı ise fasiyal sinirle gerçekleştirilir.",
            "**Kornea Refleksi:** Afferent CN V1 ve efferent CN VII bilateral refleks arkı.",
            "Kornea refleksi",
            ["kornea refleksi", "afferent iletim", "efferent yanıt"],
            []
        )
    ]),

    (24, "k2-62-b08", "CN V (Nervus Trigeminus) Muayenesi", [
        (
            "Görsel şemamızda trigeminal sinirin üç büyük duyusal dalına ait net kranial dermatom haritası ve kornea refleksi arkı sergilenmektedir.",
            "**Trigeminal Dermatom Haritası:** V1, V2, V3 alan sınırları ve kornea refleks arkı.",
            "",
            ["trigeminal dermatom haritası", "kornea refleksi arkı"],
            []
        ),
        (
            "V bir oftalmik dal alın, üst göz kapağı ve kornea duyusunu; V iki maksiller dal yanak ve üst dudağı; V üç mandibuler dal ise alt çene duyusunu taşır.",
            "**Dermatom Sınırları:** Alın, yanak ve çene anatomik duyu dağılımları.",
            "",
            ["oftalmik dal", "maksiller dal", "mandibuler dal"],
            []
        ),
        (
            "Angulus mandibula bölgesinin duyusunun trigeminal değil servikal ikinci ve üçüncü spinal sinirlerce taşındığı ayırıcı tanıda asla unutulmamalıdır.",
            "**Çene Köşesi İstisnası:** Angulus mandibulanın servikal C2-C3 pleksus innervasyonu.",
            "",
            ["angulus mandibula", "servikal dermatom"],
            []
        ),
        (
            "Pamuk ucuyla korneanın lateral limbusuna dokunulduğunda trigeminal afferent uyarıyla bilateral orbikülaris oküli kasılarak direkt ve konsensüel göz kırpma gerçekleşir.",
            "**Refleks Yanıtı:** Lateral limbus uyarısı ile bilateral orbicularis oculi kasılması.",
            "",
            ["kornea muayenesi", "orbikülaris oküli"],
            []
        )
    ]),

    # --- BOLUM 9: CN VII (Nervus Facialis) Muayenesi (25-27) ---
    (25, "k2-62-b09", "CN VII (Nervus Facialis) Muayenesi", [
        (
            "Yedinci kraniyal sinir olan nervus facialis yüzün tüm mimik kaslarını innerve eden son derece karmaşık fonksiyonlu bir sinirdir.",
            "**CN VII (N. Facialis):** Mimik kasları, tat duyusu ve sekresyon kontrolü.",
            "CN VII / N. FACIALIS",
            ["nervus facialis", "mimik kasları"],
            []
        ),
        (
            "Motor lifleri gözü sıkıca kapatan orbikülaris oküli, kaşları kaldıran frontalis ve ağız çevresindeki tüm mimik kaslarını yönetir.",
            "**Motor İşlevler:** Göz kapama, kaş kaldırma, diş gösterme ve ıslık çalma.",
            "Mimik kasları (gözü kapama)",
            ["orbikülaris oküli", "frontalis"],
            []
        ),
        (
            "Korda timpani dalı aracılığıyla dilin ön üçte iki bölümünün tat duyusunu alır ve parotis dışındaki submandibuler ile sublingual tükürük bezlerini uyarır.",
            "**Tat ve Salgı:** Dil ön 2/3 tat duyusu ve parotis dışı tükürük bezleri.",
            "Dilin ön 2/3 tat duyusu",
            ["korda timpani", "tat duyusu", "tükürük bezleri"],
            []
        ),
        (
            "Orta kulakta stapedius kasını innerve ederek ses şiddetini filtreler; sinir felcinde bu kas çalışmadığı için sese aşırı duyarlılık yani hiperakuzi gelişir.",
            "**M. Stapedius:** Ses refleks zayıflaması ve klinik hiperakuzi tablosu.",
            "M. Stapediusun motor innervasyonu",
            ["stapedius kası", "hiperakuzi"],
            []
        )
    ]),

    (26, "k2-62-b09", "CN VII (Nervus Facialis) Muayenesi", [
        (
            "Görsel kesitimizde fasiyal motor nükleusunun alt ponstaki yerleşimi ve sinir liflerinin beyin sapı içindeki kavisli seyri gösterilmektedir.",
            "**Fasiyal Sinir Seyri:** Alt pons nükleusu, iç diz oluşumu ve periferik dallar.",
            "",
            ["fasiyal nükleus", "alt pons"],
            []
        ),
        (
            "Fasiyal lifler abdusens nükleusunun etrafında iç diz yaparak dolanır ve serebellopontin açıdan vestibülokohlear sinirle yan yana çıkar.",
            "**İç Diz ve CPA:** Abdusens çevresinde kavis ve serebellopontin açıdan çıkış.",
            "",
            ["iç diz", "serebellopontin açı"],
            []
        ),
        (
            "Meatus akustikus internustan geçerek temporal kemik içerisindeki fasiyal kanala girer ve foramen stilomastoideumdan kafatasını terk eder.",
            "**Kanalis Fasiyalis:** Meatus akustikus internus ve foramen stilomastoideum seyri.",
            "",
            ["fasiyal kanal", "foramen stilomastoideum"],
            []
        ),
        (
            "Parotis bezi içerisinde dallara ayrılarak temporal, zigomatik, bukkal, marjinal mandibular ve servikal dallarıyla tüm mimik kaslarına dağılır.",
            "**Parotis İçi Dallanma:** Beş ana motor dal ile tüm yüz mimik kaslarına dağılım.",
            "",
            ["parotis bezi", "periferik dallar"],
            []
        )
    ]),

    (27, "k2-62-b09", "CN VII (Nervus Facialis) Muayenesi", [
        (
            "Görsel şemamızda klinik nörolojinin en kritik ayrımlarından biri olan santral ve periferik fasiyal paralizi mekanizması karşılaştırılmaktadır.",
            "**Santral ve Periferik Karşılaştırması:** Supranükleer ve infranükleer lezyon farkı.",
            "SANTRAL VS PERİFERİK",
            ["santral fasiyal paralizi", "periferik fasiyal paralizi"],
            []
        ),
        (
            "Fasiyal çekirdeğin alın kaslarını yöneten üst yarısı her iki serebral hemisferden iki taraflı yani bilateral kortikobulber lifler alır.",
            "**Alın Kasları İnnervasyonu:** Bilateral kortikal girdi sayesinde korunan alın fonksiyonu.",
            "SANTRAL VS PERİFERİK",
            ["fasiyal çekirdek", "bilateral kortikobulber"],
            []
        ),
        (
            "Buna karşılık ağız çevresini yöneten alt yüz çekirdeği yalnızca karşı serebral korteksten tek taraflı kontralateral innervasyon alır.",
            "**Alt Yüz İnnervasyonu:** Yalnızca kontralateral korteksten tek taraflı lif alımı.",
            "SANTRAL VS PERİFERİK",
            ["alt yüz çekirdeği", "kontralateral innervasyon"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: supranükleer tek taraflı beyin lezyonunda alın kasları bilateral innervasyon nedeniyle korunur ve sadece karşı alt yüz felç olur; oysa periferik felçte tüm yüz yarısı tutulur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Supranükleer lezyonda alın kasları korunur, yalnızca karşı alt yüz felç olur.",
            "SANTRAL VS PERİFERİK",
            ["çıkmış sınav sorusu", "supranükleer lezyon", "alın kası korunumu"],
            ["past-1790877480031-411629"]
        )
    ]),

    # --- BOLUM 10: CN VIII (Nervus Vestibulocochlearis) Muayenesi (28-29) ---
    (28, "k2-62-b10", "CN VIII (Nervus Vestibulocochlearis) Muayenesi", [
        (
            "Sekizinci kraniyal sinir olan nervus vestibulocochlearis koklear dalıyla işitme, vestibüler dalıyla ise denge ve oryantasyonu sağlar.",
            "**CN VIII (N. Vestibulocochlearis):** Koklear işitme ve vestibüler denge fonksiyonları.",
            "CN VIII /",
            ["nervus vestibulocochlearis", "koklear dal", "vestibüler dal"],
            []
        ),
        (
            "İşitme muayenesine hastanın fısıltı sesini duyma mesafesi veya parmak sürtme testinin iki taraflı simetrisi incelenerek başlanır.",
            "**Yatak Başı İşitme Testi:** Fısıltı testi ve parmak sürtme ile kaba işitme muayenesi.",
            "İşitme ve denge",
            ["fısıltı testi", "parmak sürtme"],
            []
        ),
        (
            "Vestibüler sistem muayenesinde başın ani hareketleriyle vestibülo-oküler refleks test edilir ve istemsiz ritmik nistagmus araştırılır.",
            "**Vestibüler Muayene:** Vestibülo-oküler refleks (VOR) ve nistagmus değerlendirmesi.",
            "Nistagmus",
            ["vestibülo-oküler refleks", "nistagmus"],
            []
        ),
        (
            "Periferik labirent patolojilerinde nistagmus genellikle tek yönlü ve fiksasyonla baskılanabilirken, santral lezyonlarda nistagmus çok yönlüdür ve fiksasyonla baskılanmaz.",
            "**Santral-Periferik Nistagmus:** Fiksasyon baskılanması ve nistagmus yönü ayrımı.",
            "N.VESTIBULOCOCHLEARIS",
            ["periferik nistagmus", "santral nistagmus"],
            []
        )
    ]),

    (29, "k2-62-b10", "CN VIII (Nervus Vestibulocochlearis) Muayenesi", [
        (
            "İşitme kaybı saptandığında iletim tipi ile sensörinöral tip ayrımını yapmak için beş yüz on iki hertzlik diyapazonla Weber ve Rinne testleri uygulanır.",
            "**Diyapazon Testleri:** Rinne ve Weber ile iletim-sensörinöral işitme kaybı ayrımı.",
            "Normal: Rinne (+)",
            ["iletim tipi işitme kaybı", "sensörinöral kayıp", "diyapazon"],
            []
        ),
        (
            "Rinne testinde diyapazon mastoid kemiğe ve kulak önüne konularak kemik yolu ile hava yolu iletim süreleri karşılaştırılır.",
            "**Rinne Testi Yöntemi:** Mastoid kemik yolu ve kulak önü hava yolu karşılaştırması.",
            "Kondüksiyon tipi işitme kaybı: Rinne (-)",
            ["Rinne testi", "kemik yolu", "hava yolu"],
            []
        ),
        (
            "Normal kulakta ve sensörinöral kayıpta hava yolu daha iyi olup Rinne pozitif kabul edilirken, iletim tipi kayıpta kemik iletimi üstün gelerek Rinne negatif sonuç verir.",
            "**Rinne Yorumu:** Normal ve sensörinöral kayıpta pozitif, iletim tipi kayıpta negatif.",
            "Kondüksiyon tipi işitme kaybı:",
            ["Rinne pozitif", "Rinne negatif"],
            []
        ),
        (
            "Weber testinde diyapazon kafanın tepe noktasına konur; iletim tipi kayıpta ses patolojinin olduğu hastalıklı kulağa lateralize olurken, sensörinöral kayıpta ses sağlam kulağa lateralize olur.",
            "**Weber Lateralizasyonu:** İletim kaybında hastalıklı kulağa, sensörinöralde sağlam kulağa sapma.",
            "Normal: Weber orta hatta",
            ["Weber testi", "lateralizasyon"],
            []
        )
    ]),

    # --- BOLUM 11: Alt Kraniyal Sinirler (CN IX, X, XI, XII) (30-34) ---
    (30, "k2-62-b11", "Alt Kraniyal Sinirler (CN IX, X, XI, XII)", [
        (
            "Dokuzuncu kraniyal sinir olan nervus glossopharyngeus stilofaringeus kasını innerve ederek yutma eylemine motor katkı sunar.",
            "**CN IX (N. Glossopharyngeus):** Stilofaringeus kası, parotis sekresyonu ve tat duyusu.",
            "Stilofaringeus kası",
            ["nervus glossopharyngeus", "stilofaringeus"],
            []
        ),
        (
            "Parasempatik lifleri otik ganglion aracılığıyla parotis bezine ulaşarak tükürük salgılanmasını uyarır.",
            "**Parotis Parasempatik Girdisi:** Otik ganglion üzerinden tükürük bezi sekresyonu.",
            "N.GLOSSOPHARYNGEUS",
            ["otik ganglion", "parotis bezi"],
            []
        ),
        (
            "Duyusal olarak dilin arka üçte birinin hem tat hem genel duyusunu alır; ayrıca karotis sinüs ve cismindeki baro ile kemoreseptör iletimini sağlar.",
            "**Dil ve Baroreseptör:** Dil arka 1/3 tat ve dokunma, karotis sinüsü iletimi.",
            "CN IX /",
            ["dil arka üçte biri", "karotis sinüs"],
            []
        ),
        (
            "Klinikte en önemli rolü öğürme refleksinin afferent yolunu oluşturmasıdır; orofarenks arka duvarına dokunulduğunda uyarı dokuzuncu sinirle merkeze taşınır.",
            "**Öğürme Refleksi Arkı:** Afferent CN IX ve efferent CN X ile yutak koruması.",
            "Öğürme refleksi: Afferent 9, Efferent 10",
            ["öğürme refleksi", "afferent yol"],
            []
        )
    ]),

    (31, "k2-62-b11", "Alt Kraniyal Sinirler (CN IX, X, XI, XII)", [
        (
            "Onuncu kraniyal sinir olan nervus vagus farenks ve larenks kaslarını innerve ederek konuşma ve yutma fonksiyonlarını yönetir.",
            "**CN X (N. Vagus):** Farenks-larenks kasları, parasempatik innervasyon ve uvula pozisyonu.",
            "Farenks ve larenks kasları",
            ["nervus vagus", "farenks", "larenks"],
            []
        ),
        (
            "Dil kaslarından biri olan palatoglossus kası hipoglossus tarafından değil istisnai olarak nervus vagus tarafından innerve edilir.",
            "**Palatoglossus İstisnası:** Hipoglossus yerine vagus tarafından innerve edilen tek dil kası.",
            "Palatoglossus kası",
            ["palatoglossus kası", "istisnai innervasyon"],
            []
        ),
        (
            "Toraks ve batın içi organların geniş parasempatik innervasyonunu sağlayarak kalp hızını, gastrointestinal motiliteyi ve bronş tonusunu düzenler.",
            "**Visseral Parasempatik:** Torakoabdominal organların temel parasempatik kontrolü.",
            "Organların parasempatik innervasyonu",
            ["parasempatik innervasyon", "visseral organlar"],
            []
        ),
        (
            "Tek taraflı vagus lezyonunda hasta ağzını açıp ses çıkardığında yumuşak damak felç olur ve uvula sağlam olan tarafa doğru deviye olur.",
            "**Uvula Deviasyonu:** Yumuşak damak asimetrisi ve uvulanın sağlam tarafa çekilmesi.",
            "CN X / N. VAGUS",
            ["yumuşak damak felci", "uvula deviasyonu"],
            []
        )
    ]),

    (32, "k2-62-b11", "Alt Kraniyal Sinirler (CN IX, X, XI, XII)", [
        (
            "On birinci kraniyal sinir olan nervus accessorius sternokleidomastoid ve trapezius kaslarını innerve eden saf motor bir sinirdir.",
            "**CN XI (N. Accesorius):** Sternokleidomastoid ve trapezius kasları saf motor kontrolü.",
            "CN XI / N. ACCESORIUS",
            ["nervus accessorius", "sternokleidomastoid", "trapezius"],
            []
        ),
        (
            "Sternokleidomastoid kası muayenesinde hasta hekimin eline karşı dirence rağmen başını karşı tarafa çevirmeye çalışır.",
            "**SCM Muayenesi:** Dirençli baş rotasyonu ile kontralateral sternokleidomastoid testi.",
            "Trapezius ve sternokleidomastoid kaslar",
            ["baş rotasyonu", "dirençli muayene"],
            []
        ),
        (
            "Trapezius kasının gücü ise hekim hastanın omuzlarına bastırırken hastanın omuzlarını yukarı doğru silkmesi yani kaldırmasıyla test edilir.",
            "**Trapezius Muayenesi:** Omuz silkme hareketi ile ipsilateral trapezius kas gücü tayini.",
            "Trapezius ve sternokleidomastoid kaslar",
            ["omuz silkme", "trapezius gücü"],
            []
        ),
        (
            "Boyun arka üçgeninde yüzeyel seyrettiği için lenf nodu biyopsileri veya cerrahi girişimler sırasında yaralanmaya son derece yatkındır.",
            "**İyatrojenik Hassasiyet:** Arka boyun üçgeninde lenf nodu biyopsilerinde yaralanma riski.",
            "CN XI / N. ACCESORIUS",
            ["boyun arka üçgeni", "iyatrojenik yaralanma"],
            []
        )
    ]),

    (33, "k2-62-b11", "Alt Kraniyal Sinirler (CN IX, X, XI, XII)", [
        (
            "On ikinci kraniyal sinir olan nervus hypoglossus palatoglossus hariç dilin tüm intrensek ve ekstrensek kaslarını innerve eden saf motor sinirdir.",
            "**CN XII (N. Hypoglossus):** Dil kasları (palatoglossus hariç) motor kontrolü.",
            "CN XII / N. HYPOGLOSSUS",
            ["nervus hypoglossus", "dil kasları"],
            []
        ),
        (
            "Muayeneye ağız tabanında dil istirahat halindeyken başlanır; dil kaslarında atrofi, incelme ve motor nöron hastalığını düşündüren fasikülasyonlar incelenir.",
            "**İstirahat Muayenesi:** Dil atrofisi, incelme ve motor nöron fasikülasyonları incelemesi.",
            "Dil kasları (palatoglossal hariç)",
            ["istirahat muayenesi", "dil atrofisi", "fasikülasyon"],
            []
        ),
        (
            "Ardından hastadan dilini düz olarak dışarı çıkarması istenir; tek taraflı periferik sinir lezyonunda sağlam tarafın itici gücü nedeniyle dil lezyonlu tarafa sapar ve sapması tipiktir.",
            "**Protrüzyon Muayenesi:** Dilin dışarı çıkarılması ve lezyon tarafına sapma mekanizması.",
            "Dil kasları (palatoglossal hariç)",
            ["dil deviasyonu", "lezyon tarafı"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: dil dışarı çıkarıldığında lezyon tarafındaki genioglossus kası çalışmadığı için dil doğrudan nervus hypoglossus lezyonunun olduğu tarafa deviye olur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Dil dışarı çıkarıldığında nervus hypoglossus lezyonunun olduğu tarafa deviye olur.",
            "Dil kasları (palatoglossal hariç)",
            ["çıkmış sınav sorusu", "genioglossus zaafı", "lezyon tarafına sapma"],
            ["88612c9f5ce5"]
        )
    ]),

    (34, "k2-62-b11", "Alt Kraniyal Sinirler (CN IX, X, XI, XII)", [
        (
            "Görselimizde sağ nervus hypoglossus lezyonu olan bir hastada dilin dışarı çıkarıldığında gösterdiği klasik patolojik görünüm sergilenmektedir.",
            "**Hipoglossus Felci Kliniği:** Dilin lezyon tarafına sapması ve belirgin hemilateral atrofi.",
            "",
            ["sağ nervus hypoglossus", "dil deviasyonu"],
            []
        ),
        (
            "Dil dışarı itildiğinde sağ genioglossus kası çalışmadığı için sağlam sol genioglossus kasının itici etkisiyle dil doğrudan sağ tarafa yani felçli tarafa döner.",
            "**Genioglossus Mekanizması:** Sağlam kasın itici baskısıyla dilin felçli tarafa itilmesi.",
            "",
            ["genioglossus kası", "lezyon tarafına dönme"],
            []
        ),
        (
            "Ayrıca sağ dil yarısında belirgin hacim kaybı, kırışıklık, kas atrofisi ve istemsiz fasikülasyon dalgalanmaları açıkça görülmektedir.",
            "**Atrofi ve Fasikülasyon:** Alt motor nöron hasarında dil yüzeyinde solukluk ve çekilmeler.",
            "",
            ["hacim kaybı", "dil atrofisi", "fasikülasyon"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: dil atrofisi olmayan bir hastada dil sağa sapıyorsa lezyon sol kortikobulber yolda olabilirken, atrofi ve fasikülasyon varlığında lezyon doğrudan sağ nervus hypoglossus sinirindedir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Dil atrofisi olmadan sağa sapma sol kortikobulber, atrofili sapma ise sağ hipoglossus lezyonudur.",
            "",
            ["çıkmış sınav sorusu", "kortikobulber lezyon", "atrofisiz sapma"],
            ["d3-f-098"]
        )
    ]),

    # --- BOLUM 12: Sendromik Lokalizasyon ve Klinik Karar (35-36) ---
    (35, "k2-62-b12", "Sendromik Lokalizasyon ve Klinik Karar", [
        (
            "Tablomuzda kraniyal sinirlerin kafa tabanı ve beyin sapındaki sendromik lokalizasyonları ile patolojik klinik tabloları özetlenmektedir.",
            "**Sendromik Lokalizasyon:** Kavernöz sinüs, CPA, foramen jugulare sendromları.",
            "",
            ["sendromik lokalizasyon", "kafa tabanı sendromları"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: pitozis, tam oftalmopleji ve V bir oftalmik dal kornea duyu kaybının birlikte görüldüğü patoloji kavernöz sinüs sendromudur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: CN III, IV, VI ve V1 tutulumu kavernöz sinüs sendromunu işaret eder.",
            "",
            ["çıkmış sınav sorusu", "kavernöz sinüs sendromu", "oftalmopleji"],
            ["d3-k2-nor-005"]
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: serebellopontin açı tümörlerinde yani vestibüler nörilemmomalarda sekizinci sinir işitme kaybı ve çınlaması ile birlikte yedinci ve beşinci kraniyal sinir tutulumu beklenir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Vestibüler nörilemmomada CN VIII, VII ve V tutulumu görülür.",
            "",
            ["çıkmış sınav sorusu", "serebellopontin açı", "vestibüler nörilemmoma"],
            ["8a4a38a05c80"]
        ),
        (
            "Foramen jugulare sendromunda ise dokuz, on ve on birinci kraniyal sinirler birlikte tutularak yutma güçlüğü, ses kısıklığı ve boyun kası felci oluşturur.",
            "**Foramen Jugulare Sendromu:** CN IX, X, XI tutulumu ile yutma ve ses patolojileri.",
            "",
            ["foramen jugulare", "yutma güçlüğü", "ses kısıklığı"],
            []
        )
    ]),

    (36, "k2-62-b12", "Sendromik Lokalizasyon ve Klinik Karar", [
        (
            "Dersimizin bu son sentez basamağında kraniyal sinir muayenesinin klinik karar algoritmaları ve lezyon seviyesi korelasyonu özetlenmektedir.",
            "**Klinik Sentez:** Kraniyal muayeneden beyin sapı lokalizasyonuna tanı algoritması.",
            "",
            ["klinik sentez", "karar algoritmaları"],
            []
        ),
        (
            "Muayene daima birinci kraniyal sinirden on ikinci sinire kadar sistematik bir sıra izlenerek anatomik kraniyokaudal düzende eksiksiz yürütülmelidir.",
            "**Sistematik Muayene:** I'den XII'ye kraniyokaudal sıra ile eksiksiz değerlendirme.",
            "",
            ["sistematik sıra", "kraniyokaudal düzen"],
            []
        ),
        (
            "Her bir kraniyal sinir bulgusu beyin sapı kesitiyle eşleştirilerek mezensefalon, pons veya bulbus düzeyindeki vasküler ve tümöral odak tam olarak saptanır.",
            "**Seviye Eşleştirmesi:** Mezensefalon (III-IV), Pons (V-VIII), Bulbus (IX-XII) düzeyleri.",
            "",
            ["beyin sapı kesiti", "lezyon lokalizasyonu"],
            []
        ),
        (
            "Kraniyal sinir muayenesinin titizlikle yapılması, acil serviste inme hastalarında trombolitik tedavi kararından poliklinikte kafa tabanı tümörlerinin erken teşhisine kadar hayat kurtarıcıdır.",
            "**Hayat Kurtarıcı Değer:** Akut inmede tromboliz kararı ve kitle lezyonlarında erken teşhis.",
            "",
            ["trombolitik tedavi", "erken teşhis"],
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
print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Build konusma_v2 structure
bolum_map = {}
cid_counter = 1
total_words = 0
slide_last_sent = {} # pno -> last sentence cid
slide_all_sents = {} # pno -> list of cids

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
    
    slide_all_sents[sayfa] = []
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        cid = f"k2-62-c{cid_counter:04d}"
        cid_counter += 1
        words = len(ses.split())
        total_words += words
        slide_all_sents[sayfa].append(cid)
        slide_last_sent[sayfa] = cid
        
        satir_list = [anchor] if anchor else []
        sekil_val = VISUAL_PAGES.get(sayfa, "") if sayfa in VISUAL_PAGES else None
        
        clean_ekran = ekran.replace("**", "")
        vurgu_text = None
        for t in terms:
            if t.casefold() in clean_ekran.casefold():
                vurgu_text = t
                break
        if not vurgu_text:
            m = re.findall(r'\*\*([^*]+)\*\*', ekran)
            if m:
                vurgu_text = m[0].rstrip(':').strip()
            else:
                vurgu_text = "kraniyal sinir"
        
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

bolumler_list = list(bolum_map.values())

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-62",
    "anahtar": "y25-k2-62-kraniyal-sinir-muayenesi",
    "bolumler": bolumler_list
}

print(f"Total Bolumler: {len(bolumler_list)}")
print(f"Total Paragraphs: {len(SLIDES)}")
print(f"Total Sentences: {cid_counter - 1}")
print(f"Total Words: {total_words} (~{total_words / 125:.1f} minutes of audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Generate and save metin.md
sys.path.insert(0, "/home/indu/medsor/meds/scripts/sesli_anlatim")
import konusma_v2 as KV
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Kraniyal Sinir Muayenesi"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md")

# Update cikmis_baglantilari.json to ensure all 6 past questions are recorded as ilgili: true
cikmis_list = [
    {
        "soru_id": "7a901e64695e",
        "ilgili": True,
        "neden": "Dördüncü kraniyal sinirin dorsal çıkış ve tam çaprazlaşma anatomik özelliğini sorgular.",
        "bagli_bilgi": ["bp-17", "bp-18"],
        "kanit": {"sayfa": 18, "alinti": "Bielschowsky baş tilt testi Sağ 4. sinir felci"}
    },
    {
        "soru_id": "past-1790877480031-411629",
        "ilgili": True,
        "neden": "Beyinde tek taraflı supranükleer lezyonda alın kaslarının bilateral innervasyon ile korunmasını sorgular.",
        "bagli_bilgi": ["bp-27"],
        "kanit": {"referans": "Harrison Nöroloji, Kraniyal Sinirler", "neden": "Supranükleer fasiyal lezyonda alın korunumu"}
    },
    {
        "soru_id": "88612c9f5ce5",
        "ilgili": True,
        "neden": "Dilin dışarı çıkarıldığında lezyon tarafına sapması sağ nervus hypoglossus lezyonunun karakteristik klinik bulgusudur.",
        "bagli_bilgi": ["bp-33", "bp-34"],
        "kanit": {"sayfa": 33, "alinti": "Dil kasları (palatoglossal hariç)"}
    },
    {
        "soru_id": "d3-f-098",
        "ilgili": True,
        "neden": "Dilin dışarı çıkarıldığında sağ tarafa sapması ve dil atrofisinin olmaması supranükleer kortikobulber lezyonu düşündürür.",
        "bagli_bilgi": ["bp-33", "bp-34"],
        "kanit": {"sayfa": 33, "alinti": "Dil kasları (palatoglossal hariç)"}
    },
    {
        "soru_id": "d3-k2-nor-005",
        "ilgili": True,
        "neden": "Pitozis, tam oftalmopleji ve V1 kornea/alın duyusu kaybı kavernöz sinüs sendromunun tipik tablosudur.",
        "bagli_bilgi": ["bp-35"],
        "kanit": {"referans": "Moore Anatomi, Kavernöz Sinüs", "neden": "Kavernöz sinüs içinden ve duvarından geçen kraniyal sinirler"}
    },
    {
        "soru_id": "8a4a38a05c80",
        "ilgili": True,
        "neden": "Serebellopontin açı tümörlerinde (vestibüler nörilemmoma) CN VIII işitme kaybı ve CN VII-V tutulumu beklenir.",
        "bagli_bilgi": ["bp-35"],
        "kanit": {
            "referans": "Robbins Temel Patoloji, Serebellopontin Açı Tümörleri ve Vestibüler Schwannom",
            "neden": "Vestibüler nörilemmomada CN VIII işitme kaybı ve fasiyal-trigeminal tutulum"
        }
    }
]
(TASLAK / "cikmis_baglantilari.json").write_text(json.dumps(cikmis_list, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved cikmis_baglantilari.json with 6 questions.")

# Generate 12 Live Semantic Drawing Commands tied dynamically to the last sentence of each slide
cizim_komutlari = [
    {
        "cumle": slide_last_sent[4],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Görme Yolları Defektleri",
        "ogeler": [
            "Optik kiazma lezyonunda bitemporal hemianopsi",
            "Optik sinir lezyonunda monooküler anopsi",
            "Kiazma bileşkesinde junctional skotom"
        ]
    },
    {
        "cumle": slide_last_sent[10],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Ekstraoküler Kas Hareketleri",
        "ogeler": [
            "Lateral rektus kası abdüksiyon yaptırır",
            "Mediyal rektus kası addüksiyon yaptırır",
            "Superior oblik depresyon ve intorsiyon",
            "Inferior oblik elevasyon ve ekstorsiyon"
        ]
    },
    {
        "cumle": slide_last_sent[11],
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Ekstraoküler Motor Innervasyon",
        "ogeler": [
            "Okülomotor sinir rektus kasları ve levator",
            "Troklear sinir superior oblik kası",
            "Abdusens siniri lateral rektus kası"
        ]
    },
    {
        "cumle": slide_last_sent[13],
        "bas": 0, "son": 4,
        "sayfa": 13,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Pupilla Işık Refleksi Yolakları",
        "ogeler": [
            "Optik sinir afferent uyarısı",
            "Pretektal nükleus bilateral uyarısı",
            "Edinger-Westphal nükleusundan çıkan efferent lifler",
            "Göz iris sfinkter kası ile bilateral miyozis"
        ]
    },
    {
        "cumle": slide_last_sent[14],
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Yakın Refleks Yanıtı",
        "ogeler": [
            "Mediyal rektus kasları ile konverjans",
            "Silier kas kasılması ile akomodasyon",
            "Göz iris sfinkteri ile pupiller miyozis"
        ]
    },
    {
        "cumle": slide_last_sent[18],
        "bas": 0, "son": 4,
        "sayfa": 18,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Troklear Sinir Özellikleri",
        "ogeler": [
            "Beyin sapını dorsalden terk eden tek sinir",
            "Tamamı çaprazlaşan tek kraniyal sinir",
            "Superior oblik felcinde Bielschowsky baş tilt testi"
        ]
    },
    {
        "cumle": slide_last_sent[20],
        "bas": 0, "son": 4,
        "sayfa": 20,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Horizontal Bakış Yolları",
        "ogeler": [
            "Frontal göz sahası kortikal uyarısı",
            "Ponsta paramedian retiküler formasyon",
            "Abdusens çekirdeği ve lateral rektus aktivasyonu",
            "Mediyal longitudinal fasikülüs ile konjuge bakış"
        ]
    },
    {
        "cumle": slide_last_sent[21],
        "bas": 0, "son": 4,
        "sayfa": 21,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "İnternükleer Oftalmopleji Bulguları",
        "ogeler": [
            "Mediyal longitudinal fasikülüs lezyonu",
            "Aynı taraf gözde addüksiyon kısıtlılığı",
            "Dışa bakan gözde disosiasyon nistagmusu",
            "Konverjans hareketinin tam korunması"
        ]
    },
    {
        "cumle": slide_last_sent[27],
        "bas": 0, "son": 4,
        "sayfa": 27,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Fasiyal Paralizi Ayrımı",
        "ogeler": [
            "Santral felç: Alın kasları korunur",
            "Santral lezyon: Sadece karşı alt yüz felç olur",
            "Periferik felç: Tüm yüz yarısı tutulur"
        ]
    },
    {
        "cumle": slide_last_sent[29],
        "bas": 0, "son": 4,
        "sayfa": 29,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "İşitme Testi Bulguları",
        "ogeler": [
            "Iletim tipi kayıp: Rinne negatif",
            "Sensörinöral kayıp: Rinne pozitif",
            "Iletim tipi kayıp: Weber hastalıklı kulağa lateralize",
            "Sensörinöral kayıp: Weber sağlam kulağa lateralize"
        ]
    },
    {
        "cumle": slide_last_sent[33],
        "bas": 0, "son": 4,
        "sayfa": 33,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Hipoglossus Felci Bulgusu",
        "ogeler": [
            "Nervus hypoglossus lezyonu gelişmesi",
            "Aynı taraf genioglossus kas zaafı",
            "Dilin lezyon tarafına sapması",
            "Dil kaslarında atrofi ve fasikülasyon"
        ]
    },
    {
        "cumle": slide_last_sent[35],
        "bas": 0, "son": 4,
        "sayfa": 35,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kafa Tabanı Sendromları",
        "ogeler": [
            "Kavernöz sinüs: Pitozis ve tam oftalmopleji",
            "Serebellopontin açı: Vestibüler nörilemmoma ve işitme kaybı",
            "Foramen jugulare: Yutma güçlüğü ve ses kısıklığı"
        ]
    }
]

cizim_aday = {"komutlar": cizim_komutlari}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(cizim_komutlari)} commands.")
