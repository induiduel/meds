# -*- coding: utf-8 -*-
"""
Rebuild Nefritik Sendrom Deck with High-Quality Medical Standards
learn-glomeruler-hastaliklar-nefritik (24 Slayt)
Prof. Dr. Hikmet Keleş & Robbins Pathology
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

def make_slide(slide_num, title, subtitle, narrative, spots, practice_q):
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "content": narrative,
        "synthesisNarrative": narrative,
        "spots": spots,
        "spotPearls": spots,
        "relatedQuestions": [practice_q],
        "practiceQuestion": practice_q
    }

nefritik_slides = [
    make_slide(
        1,
        "Nefritik Sendrom: Klinik Tanım ve Kardinal Bulgular",
        "Dismorfik Hematüri, Oligüri, Azotemi ve Hipertansiyon Tetradı",
        """Nefritik sendrom, glomerül kapiller duvarlarında gelişen akut enflamatuar hasar ve hücresel proliferasyon sonucunda glomerüler filtrasyon bariyerinin bozulmasıyla karakterize klinik tablodur. Nefrotik sendromdan farklı olarak burada primer patolojik olay podosit ayaksı çıkıntılarının kaybı değil; kapiller lümeni daraltan hücresel reaksiyon, lökosit infiltrasyonu ve kapiller duvar yırtılmalarıdır.

**1. Kardinal Tanı Kriterleri:**
• **Hematüri:** Hem makroskopik (çay veya kola rengi idrar) hem de mikroskopik olabilir. İdrarda glomerülden sızan eritrositler mekanik ve ozmotik travma nedeniyle şekil değiştirir (**dismorfik eritrositler / akantositler**). Tubulus lümeninde Tamm-Horsfall mukoproteini ile birleşen eritrositler **eritrosit silindirleri** oluşturur; bu bulgu hematürinin glomerüler kökenli olduğunun kesin kanıtıdır.
• **Oligüri ve Azotemi:** Glomerül kapiller lümenlerinin endotel hiperplazisi ve nötrofillerle tıkanması filtrasyon yüzeyini daraltır; glomerüler filtrasyon hızı (GFR) hızla düşer. Serumda üre ve kreatinin yükselir (azotemi).
• **Hipertansiyon ve Ödem:** Düşen GFR nedeniyle böbrekten sodyum ve su atılamaz (volüm yüklenmesi). Gelişen hipervolemi hipertansiyona ve özellikle sabahları belirginleşen periorbital ödeme yol açar.
• **Subnefrotik Proteinüri:** Genellikle günlük <3.0 gram (çoğunlukla 1-2 g/gün) düzeyindedir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "İdrar sedimentinde dismorfik eritrositler ve eritrosit silindirlerinin (RBC casts) görülmesi hematürinin alt idrar yollarından değil, glomerülden kaynaklandığını kanıtlar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Nefritik sendrom klasik olarak hematüri (kola renkli idrar), oligüri, azotemi ve hipertansiyon tetradıyla seyreder; proteinüri nefrotik düzeye ulaşmaz.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-001",
            "question": "Aşağıdaki idrar sedimenti bulgularından hangisi bir hematürinin alt idrar yolu kaynaklı (taş/tümör) değil, kesinlikle glomerüler enflamasyona (nefritik sendrom) bağlı olduğunu kanıtlar?",
            "options": [
                "A) Çok sayıda lökosit ve bakteri",
                "B) İzosellüler taze eritrositler",
                "C) Dismorfik eritrositler ve eritrosit silindirleri",
                "D) Ürik asit kristalleri",
                "E) Oval yağ cisimcikleri"
            ],
            "correctAnswer": 2,
            "explanation": "Dismorfik eritrositler ve eritrosit silindirleri kanamanın glomerül filtrasyon bariyerinden ve tubulus lümeninden kaynaklandığını gösteren patognomonik nefritik sendrom bulgularıdır."
        }
    ),
    make_slide(
        2,
        "Nefritik Sendrom Patofizyolojisi: Enflamasyon ve GFR Çöküşü",
        "Endokapiller Proliferasyon, Nötrofil Kemotaksisi ve Renal Hemodinamik Bozulma",
        """Nefritik sendromun gelişimindeki temel fizyopatolojik basamaklar glomerül endotel ve mezangiyal kompartmanında tetiklenen immün yanıta dayanır.

**1. Hücresel ve Moleküler Mekanizmalar:**
• İmmün kompleks birikimi veya antikor bağlanması klasik/lektin kompleman yolunu aktive ederek güçlü kemotaktik ajanlar olan C3a ve C5a üretir.
• Glomerül kapillerlerine göç eden nötrofiller ve monositler endotel hücrelerini hasarlar ve proteolitik enzimler salgılar.
• Glomerül içi endotel ve mezangiyal hücreler çoğalarak (endokapiller proliferasyon) kapiller lümenleri tıkar.

**2. Hemodinamik Sonuçlar:**
• Kapiller lümenlerin tıkanması ve filtrasyon katsayısının (Kf) düşmesi glomerüler filtrasyon hızını (GFR) dramatik biçimde azaltır.
• Düşen GFR'ye yanıt olarak makula densa uyarılır, sempatik tonus artar ve afferent vazokonstriksiyon gelişir.
• Distal nefrondan sodyum ve su geri emilimi artarak intravasküler volüm genişler; renin salgısı genellikle sekonder olarak baskılanır ancak volüm aşırı yükü sistolik ve diyastolik kan basıncını yükseltir.""",
        [
            {"type": "clinical", "badge": "🔴 PATOFİZYOLOJİK AYRIM", "text": "Nefrotik sendromdaki ödem hipoalbüminemiye bağlı onkotik basınç düşüklüğünden kaynaklanırken, nefritik sendromdaki ödem ve hipertansiyon doğrudan primer renal sodyum-su retansiyonuna ve volüm yüklenmesine bağlıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Nefritik sendromda oligürinin temel nedeni glomerül endotel proliferasyonu ve lökosit infiltrasyonu sonucu kapiller lümenlerin daralması ve Kf katsayısının düşmesidir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-002",
            "question": "Nefritik sendromda hipertansiyon ve ödem gelişimindeki primer patofizyolojik mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Hipoalbüminemiye bağlı plazma onkotik basıncının çökmesi",
                "B) GFR düşüşüne bağlı gelişen primer renal sodyum ve su retansiyonu",
                "C) Renal arter darlığına bağlı malign renin deşarjı",
                "D) İzole aldosteron salgılayan adenom varlığı",
                "E) İdrarla yüksek oranda albümin kaybı"
            ],
            "correctAnswer": 1,
            "explanation": "Nefritik sendromda GFR'nin ani düşmesi sonucu böbreklerden tuz ve su atılamaz; gelişen primer hipervolemi hipertansiyon ve periorbital ödeme yol açar."
        }
    ),
    make_slide(
        3,
        "Akut Poststreptokokkal Glomerülonefrit (APSGN): Etyopatogenez ve Latent Periyot",
        "A Grubu Beta-Hemolitik Streptokoklar, SpeB Antijeni ve 1-4 Haftalık Kuluçka Süresi",
        """Akut Poststreptokokkal Glomerülonefrit (APSGN), çocukluk çağında nefritik sendromun en prototipik ve en sık nedenidir. Genellikle 5-15 yaş arasındaki çocuklarda görülür.

**1. Etyolojik Ajan ve Nefritojenik Suşlar:**
• Etken, A grubu beta-hemolitik streptokoklardır (**Streptococcus pyogenes**).
• Her streptokok suşu nefrit yapmaz; M proteini tiplemesine göre **nefritojenik suşlar** sorumludur:
  - Farenjit sonrası nefrit: En sık **M tipi 12** (ayrıca 1, 4).
  - Cilt enfeksiyonu (piyodermi / impetigo) sonrası nefrit: En sık **M tipi 49** (ayrıca 2, 42, 57, 60).
• Başlıca nefritojenik antijenler: **SpeB** (streptokokkal pirojenik ekzotoksin B) ve GAPDH (streptokokkal gliseraldehit-3-fosfat dehidrogenaz). Bu katyonik antijenler glomerül bazal membranına oturur ve dolaşımdaki antikorlar in situ kompleks oluşturur.

**2. Kritik Latent Dönem:**
• **Farenjit sonrası:** Boğaz enfeksiyonundan **1 ila 2 hafta** sonra nefrit başlar.
• **Cilt enfeksiyonu (İmpetigo) sonrası:** Deri lezyonlarından **2 ila 6 hafta** sonra nefrit başlar.
• Bu latent süre antijenik maruziyet sonrası IgG tipi antikorların üretilmesi ve immün komplekslerin oluşması için şarttır.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK AYIRICI TANI", "text": "Üst solunum yolu enfeksiyonu sırasında veya 1-2 gün içinde hematüri başlarsa bu APSGN değil IgA Nefropatisidir! APSGN için farenjitten sonra en az 1-2 haftalık latent süre geçmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Farenjit sonrası nefritojenik M tipi 12 iken; impetigo/cilt enfeksiyonu sonrası nefritojenik M tipi 49'dur. Latent süre cilt enfeksiyonlarında daha uzundur (2-4 hafta).", "color": "sky"}
        ],
        {
            "id": "prac-nefr-003",
            "question": "8 yaşındaki bir erkek çocukta streptokokkal boğaz enfeksiyonundan 12 gün sonra koyu renkli idrar, periorbital ödem ve tansiyon yüksekliği gelişiyor. Bu tabloda sorumlu en olası nefritojenik streptokok M serotipi hangisidir?",
            "options": [
                "A) M tipi 12",
                "B) M tipi 49",
                "C) M tipi 2",
                "D) M tipi 57",
                "E) M tipi 60"
            ],
            "correctAnswer": 0,
            "explanation": "Streptokokkal farenjit sonrası gelişen akut glomerülonefritte en sık sorumlu nefritojenik serotip M tipi 12'dir. M tipi 49 ise cilt enfeksiyonları (impetigo) sonrası nefritten sorumludur."
        }
    ),
    make_slide(
        4,
        "APSGN Morfolojisi: Diffüz Proliferatif Eksüdatif Glomerülonefrit",
        "Büyük Hiperselüler Glomerüller, Endotelyal-Mezangiyal Proliferasyon ve Nötrofil Tıkacı",
        """APSGN'de böbreğin histopatolojik görünümü, immün aracılı akut glomerüler yangının en klasik tablosunu sergiler.

**1. Işık Mikroskopisi (LM):**
• **Diffüz Proliferatif Glomerülonefrit:** Biyopside incelenen tüm glomerüller (diffüz) tutulmuştur. Glomerüller ileri derecede genişlemiş ve aşırı derecede hiperselülerdir.
• Hücre artışı üç kaynaktan gelir:
  1. Glomerül içi kapiller endotel hücre proliferasyonu,
  2. Mezangiyal hücre proliferasyonu ve matriks artışı,
  3. Bowman aralığına ve kapiller lümene hücum eden nötrofil lökositler ve monositler.
• Glomerül kapiller lümenleri bu hücre tıkaçlarıyla tamamen sıkışmış ve lümensiz görünüm kazanmıştır. Çok sayıda nötrofil içermesi nedeniyle **akut eksüdatif glomerülonefrit** olarak da adlandırılır. Ağır olgularda fokal nekroz ve nadiren hilaller eşlik edebilir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "APSGN'de ışık mikroskobunda glomerüllerin tümü tutulmuştur (diffüz); kapiller lümenler nötrofil ve proliferatif hücrelerce tıkandığı için glomerüller avasküler ve hiperhücresel görünür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Akut poststreptokokkal GN'nin ışık mikroskobu tanısı 'Diffüz Proliferatif ve Eksüdatif Glomerülonefrit'tir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-004",
            "question": "Akut poststreptokokkal glomerülonefrit tanılı bir çocuğun böbrek biyopsisinde ışık mikroskobunda beklenen karakteristik histopatolojik lezyon aşağıdakilerden hangisidir?",
            "options": [
                "A) Glomerüllerin normal izlendiği podosit silinmesi",
                "B) Diffüz endokapiller proliferasyon ve lökosit infiltrasyonu ile karakterize hiperselülarite",
                "C) Kapiller duvarda diffüz spike and dome kalınlaşması",
                "D) Bowman aralığını tamamen dolduran fibröz hilaller",
                "E) Sadece afferent arteriyolde hyalinozis"
            ],
            "correctAnswer": 1,
            "explanation": "APSGN'nin ışık mikroskobu bulgusu endotel ve mezangiyal proliferasyonun yanı sıra yoğun nötrofil infiltrasyonu içeren diffüz proliferatif (eksüdatif) glomerülonefrittir."
        }
    ),
    make_slide(
        5,
        "APSGN: İmmünofloresan ('Yıldızlı Gökyüzü') ve Elektron Mikroskobu ('Hörgüçler')",
        "Kaba Granüler C3/IgG ve Subepitelyal Hörgüç (Subepithelial Humps) Patognomonisi",
        """APSGN'de immünofloresan ve elektron mikroskopisi bulguları patoloji sınavlarının en vazgeçilmez temel soru kaynaklarıdır.

**1. İmmünofloresan Mikroskopi (İF):**
Glomerül kapiller duvarı boyunca ve mezangiyumda kaba taneli, düzensiz **granüler IgG, IgM ve baskın C3** depolanması izlenir. Bu kaba granüler floresan deseni karanlık alanda gökyüzündeki yıldızları andırdığı için klasik olarak **'Yıldızlı Gökyüzü' (Starry-sky pattern)** veya 'çelenk benzeri' (garland pattern) manzara olarak tanımlanır.

**2. Elektron Mikroskopisi (EM):**
• Hastalığın en patognomonik morfolojik özelliği glomerüler bazal membranın epitel tarafında (subepitelyal) yerleşmiş dev kubbe benzeri depozitlerdir: **Subepitelyal Hörgüçler (Subepithelial Humps)**.
• Bu hörgüçler streptokokkal SpeB antijen-antikor komplekslerinin podosit tabanı ile GBM arasında birikmesiyle oluşur.
• Ayrıca subendotelyal ve mezangiyal alanda da daha küçük immün kompleksler izlenebilir; haftalar içinde hörgüçler lizise uğrayarak kaybolur.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Elektron mikroskobunda izlenen büyük kubbe biçimli 'Subepitelyal Hörgüçler' (Humps) APSGN için tanı koydurucudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SORUSU", "text": "İmmünofloresanda kaba granüler 'yıldızlı gökyüzü' C3 boyanması ve elektron mikroskobunda 'subepitelyal hörgüç' (humps) görülen hastalık Akut Poststreptokokkal GN'dir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-005",
            "question": "Nefritik sendromlu bir çocukta yapılan renal biyopside immünofloresanda tipik 'yıldızlı gökyüzü' paterni ve elektron mikroskobunda GBM üzerinde kubbe şeklinde 'subepitelyal hörgüçler' (humps) izleniyor. Tanı nedir?",
            "options": [
                "A) Akut poststreptokokkal glomerülonefrit",
                "B) Membranöz nefropati",
                "C) Goodpasture sendromu",
                "D) Alport sendromu",
                "E) Fokal segmental glomerüloskleroz"
            ],
            "correctAnswer": 0,
            "explanation": "Kaba granüler C3 yıldızlı gökyüzü paterni ve EM'deki subepitelyal hörgüçler (humps) akut poststreptokokkal glomerülonefritin patognomonik ikilisidir."
        }
    ),
    make_slide(
        6,
        "APSGN: Serolojik Tanı, Kompleman Dinamiği ve Prognoz",
        "ASO, Anti-DNAse B, Geçici C3 Hipokomplementemisi ve %95 Tam İyileşme",
        """APSGN tanısı klinik tablo, geçirilmiş streptokok enfeksiyonu kanıtı ve kompleman profiliyle doğrulanır; tipik çocuk olgularında biyopsi gereksizdir.

**1. Serolojik Testler:**
• **Anti-Streptolizin O (ASO):** Farenjit sonrası olguların %90'ında yükselir; ancak cilt enfeksiyonlarında (impetigo) deri lipidleri streptolizini inaktive ettiği için ASO genellikle yükselmez!
• **Anti-DNAse B:** Cilt enfeksiyonu (impetigo) sonrası nefrit tanısında en sensitif ve güvenilir streptokokkal serolojik göstergedir.

**2. Serum Kompleman Dinamiği:**
• Klasik ve alternatif yol aktivasyonu ile serum **C3 ve CH50 aşırı düşer**; C4 düzeyi genellikle normal veya hafif düşüktür.
• **Kritik Süre Kuralı:** Serum C3 düşüklüğü geçicidir; enfeksiyondan **6 ila 8 hafta sonra mutlaka normale dönmelidir**. 8 haftayı aşan C3 düşüklüğünde MPGN, Lupus veya C3 Glomerülopatisi düşünülmelidir.

**3. Prognoz:**
• Çocuklarda prognoz mükemmeldir; %95'ten fazlası konservatif tedaviyle (tuz kısıtlaması, diüretik) hiçbir sekel kalmadan tam iyileşir.
• Erişkinlerde seyir daha ciddidir; olguların %1-2'si RPGN'ye, %10-20'si kronik glomerülonefrite ve son dönem böbrek yetmezliğine ilerleyebilir.""",
        [
            {"type": "clinical", "badge": "🔴 SEROLOJİK KURAL", "text": "İmpetigo / cilt enfeksiyonu sonrası nefrit şüphesinde ASO güvenilmezdir; tanıyı doğrulayan serolojik test Anti-DNAse B'dir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "APSGN'de serum C3 düzeyi 6-8 hafta içinde normale döner. 8 haftadan uzun süren C3 düşüklüğü biyopsi endikasyonudur ve MPGN'yi düşündürür.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-006",
            "question": "Bacaklarındaki impetigo lezyonlarından 3 hafta sonra nefritik sendrom tablosuyla başvuran bir çocukta streptokok enfeksiyonunu kanıtlamak için en duyarlı serolojik test hangisidir?",
            "options": [
                "A) Anti-Streptolizin O (ASO)",
                "B) Anti-DNAse B",
                "C) C-reaktif protein",
                "D) Anti-kardiyolipin antikorları",
                "E) Romatoid faktör"
            ],
            "correctAnswer": 1,
            "explanation": "Cilt enfeksiyonlarında (impetigo) kolesterol streptolizini bağlayarak ASO yanıtını baskılar; bu nedenle cilt kaynaklı APSGN'de en güvenilir test Anti-DNAse B'dir."
        }
    ),
    make_slide(
        7,
        "Hızlı İlerleyen Glomerülonefrit (RPGN) ve Kresent (Hilal) Patolojisi",
        "Bowman Boşluğunda Fibrin Kaçağı, Pariyetal Epitel Proliferasyonu ve Hilal Oluşumu",
        """Hızlı İlerleyen Glomerülonefrit (Rapidly Progressive Glomerulonephritis - RPGN), günler veya haftalar içinde GFR'de ani ve dramatik bir düşüşle akut böbrek yetmezliğine ve anüriye ilerleyen en agresif nefritik sendrom tablosudur. Tedavi edilmediğinde aylar içinde ölümle veya kalıcı diyaliz bağımlılığıyla sonuçlanır.

**1. Kresent (Hilal) Oluşumunun Patogenezi:**
• Şiddetli glomerüler nekroz kapiller duvar bütünlüğünü bozar ve kapiller duvarda büyük çatlaklar/yırtıklar oluşur.
• Plazma proteinleri ve özellikle **fibrinojen / fibrin** Bowman aralığına sızar.
• Bowman aralığındaki doku faktörü ve fibrin, Bowman kapsülünün **pariyetal epitel hücrelerini** güçlü şekilde uyararak çoğalmaya sevk eder; eş zamanlı olarak monositler ve makrofajlar bölgeye göç eder.
• Çoğalan pariyetal epitel hücreleri ve makrofajlar Bowman kapsülü lümenini yarım ay biçiminde doldurarak kapiller yumağı sıkıştırır; buna **Kresent (Hilal)** denir.

**2. Patolojik Eşik:**
Bir glomerülonefrite RPGN (Kresentik GN) tanısı konabilmesi için böbrek biyopsisindeki glomerüllerin **en az %50'sinde** kresent oluşumu izlenmelidir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Hilal (kresent) yapısının temelini Bowman kapsülünün PARİYETAL epitel hücrelerinin proliferasyonu ve makrofaj göçü oluşturur; tetikleyici molekül Bowman aralığına sızan fibrindir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Kresentik glomerülonefrit tanısı için glomerüllerin en az %50'sinde hilal bulunmalıdır; erken dönemde hücresel olan hilaller zamanla fibröz hilallere dönüşerek geri dönüşsüz skleroza yol açar.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-007",
            "question": "Hızlı ilerleyen glomerülonefritte (RPGN) Bowman aralığında izlenen kresentlerin (hilallerin) hücresel yapısını oluşturan temel hücre grubu aşağıdakilerden hangisidir?",
            "options": [
                "A) Podositler (visseral epitel hücreleri)",
                "B) Pariyetal epitel hücreleri ve makrofajlar",
                "C) Glomerül endotel hücreleri",
                "D) Mezangiyal matriks miyofibroblastları",
                "E) Proksimal tubulus epitel hücreleri"
            ],
            "correctAnswer": 1,
            "explanation": "Hilaller fibrin sızıntısına yanıt olarak çoğalan Bowman kapsülü pariyetal epitel hücreleri ve bölgeye göç eden makrofajlardan meydana gelir."
        }
    ),
    make_slide(
        8,
        "RPGN Tip I: Anti-GBM Hastalığı ve Goodpasture Sendromu",
        "Tip IV Kollajen Alfa-3 Zinciri, Lineer IgG Birikimi ve Alveoler Hemoraji",
        """RPGN Tip I (Anti-GBM Glomerülonefriti), glomerüler bazal membrana karşı doğrudan otoantikorların gelişmesiyle oluşan en yıkıcı nefropatilerden biridir.

**1. Antijenik Hedef ve İmmünopatogenez:**
• Otoantikorlar tip IV kollajenin non-kollajenöz domainine (**NC1 domain of alpha-3 chain of Type IV collagen**) karşı gelişir.
• Bu spesifik alfa-3 zinciri vücutta sadece glomerüler bazal membranda ve akciğer alveol bazal membranında yoğun olarak eksprese edilir.
• **Goodpasture Sendromu:** Anti-GBM antikorlarının hem glomerülü hem de alveolleri hedef alması sonucu gelişen **nekrotizan glomerülonefrit + pulmoner kanama (hemoptizi)** tablosudur. Sigara dumanı ve solvent maruziyeti alveol endotel geçirgenliğini artırarak antikorların akciğer bazal membranına ulaşmasını kolaylaştırır.
• Sadece böbrek tutulduğunda 'Anti-GBM glomerülonefriti' adını alır.

**2. İmmünofloresan Mikroskopi (İF):**
Glomerül bazal membranı boyunca kesintisiz, pürüzsüz ve homojen **çizgisel (LİNEER) IgG ve C3** birikimi izlenir. Bu görünüm hastalığın en karakteristik patolojik imzasıdır.

**3. Tedavi:**
Acil plazmaferez (dolaşımdaki antikorları uzaklaştırmak için) + yüksek doz steroid ve siklofosfamid.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "İmmünofloresanda glomerül bazal membranı boyunca 'LİNEER IgG' birikimi Anti-GBM / Goodpasture hastalığı için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Goodpasture sendromunda hedef antijen Tip IV kollajenin alfa-3 zincirinin NC1 alanıdır; klinik tablo nekrotizan kresentik nefrit ve hemoptizidir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-008",
            "question": "Hemoptizi ve akut oligürik böbrek yetmezliği ile başvuran 24 yaşındaki erkek hastanın böbrek biyopsisinde immünofloresan mikroskopisinde glomerül kapiller duvarlarında kesintisiz lineer IgG pozitifliği saptanıyor. Bu antikorların hedef aldığı moleküler yapı hangisidir?",
            "options": [
                "A) Podosit nefrin proteini",
                "B) Tip IV kollajen alfa-3 zincirinin NC1 domaini",
                "C) M-tipi fosfolipaz A2 reseptörü",
                "D) Streptokokkal SpeB antijeni",
                "E) Nötrofil sitoplazmik miyeloperoksidaz"
            ],
            "correctAnswer": 1,
            "explanation": "Goodpasture sendromu Tip IV kollajenin alfa-3 zincirine (NC1 domain) karşı gelişen otoantikorlara bağlıdır ve İF'de tipik lineer IgG deseni verir."
        }
    ),
    make_slide(
        9,
        "RPGN Tip II: İmmün Kompleks Aracılı Hilal Gelişimi",
        "SLE, Postenfeksiyöz GN, IgA Nefropatisi Zemininde Gelişen Granüler Depozitler",
        """RPGN Tip II, bilinen bir immün kompleks glomerülonefritinin aşırı alevlenmesi ve kapiller yırtılmalar sonucu kresentik forma dönüşmesiyle karakterizedir.

**1. Etyolojik Nedenler:**
• **Sistemik Lupus Eritematozus (SLE Sınıf IV):** Lupus nefritinin diffüz proliferatif formu kresentlerle komplike olabilir.
• **Akut Postenfeksiyöz Glomerülonefrit:** Olguların %1-2'sinde aşırı enflamasyon hilallere yol açar.
• **IgA Nefropatisi ve Henoch-Schönlein Purpurası.**
• **Membranoproliferatif Glomerülonefrit (MPGN).**

**2. Patoloji ve İmmünofloresan:**
• Işık mikroskobunda glomerüllerde hem altta yatan immün kompleks hastalığının özellikleri (mezangiyal proliferasyon, subendotelyal depozitler vb.) hem de belirgin hücresel hilaller izlenir.
• **İmmünofloresan (İF):** Tip I'deki düzgün lineer paternin aksine, tipik **kaba GRANÜLER immünglobulin ve kompleman** birikimi görülür.
• Serumda kompleman düzeyleri (C3, C4) altta yatan primer hastalığa bağlı olarak genellikle düşüktür.""",
        [
            {"type": "clinical", "badge": "🔴 İMMÜNOLOJİK AYRIM", "text": "RPGN Tip I'de İF lineer iken; RPGN Tip II'de İF daima granülerdir (immün kompleks kökenli).", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Poststreptokokkal GN veya Lupus Nefriti zemininde gelişen kresentik böbrek yetmezliği RPGN Tip II (immün kompleks aracılı) sınıfına girer.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-009",
            "question": "Aşağıdaki kresentik glomerülonefrit (RPGN) tiplerinden hangisinin biyopsisinde immünofloresan incelemede granüler immün kompleks birikimi izlenmesi beklenir?",
            "options": [
                "A) Granülomatöz polianjiyitis (Wegener)",
                "B) Goodpasture hastalığı",
                "C) Lupus Nefriti Sınıf IV zemininde gelişen kresentik GN (RPGN Tip II)",
                "D) Mikroskopik polianjiyitis",
                "E) İzole Anti-GBM glomerülonefriti"
            ],
            "correctAnswer": 2,
            "explanation": "RPGN Tip II immün kompleks aracılıdır (Lupus, Poststreptokokkal vb.) ve İF'de granüler depozitler içerir. Tip I lineer, Tip III ise pauci-immündür."
        }
    ),
    make_slide(
        10,
        "RPGN Tip III: Pauci-İmmün / ANCA Pozitif Glomerülonefrit",
        "Granülomatozisli Polianjiyitis (Wegener), Mikroskopik Polianjiyitis ve c-ANCA/p-ANCA",
        """RPGN Tip III (Pauci-İmmün Glomerülonefrit), glomerülde anlamlı immün kompleks veya antikor birikimi bulunmayan (pauci = fakir/az), ancak olguların %85-90'ında kanda **Anti-Nötrofil Sitoplazmik Antikorların (ANCA)** pozitif olduğu sistemik küçük damar vaskülitlerinin böbrek tutulumudur. Yaşlı erişkinlerde en sık görülen RPGN tipidir.

**1. Vaskülit Tipleri ve ANCA Özgüllüğü:**
• **Granülomatöz Polianjiyitis (GPA / Wegener Granülomatozu):**
  - Üst solunum yolu (sinüzit, nazal septum perforasyonu / eyer burun), alt solunum yolu (akciğerde kavitasyonlu granülomatöz nodüller) ve nekrotizan kresentik glomerülonefrit triadı.
  - Serolojide **c-ANCA (PR3-ANCA, Proteinaz-3)** %95 pozitiftir.
• **Mikroskopik Polianjiyitis (MPA):**
  - Akciğerde granülom veya kavitasyon yapmaz; nekrotizan vaskülit ve kresentik GN ile seyreder.
  - Serolojide **p-ANCA (MPO-ANCA, Miyeloperoksidaz)** baskındır.
• **Eozinofilik Granülomatöz Polianjiyitis (EGPA / Churg-Strauss):** Astım, periferik eozinofili, granülomlar ve p-ANCA pozitifliği.

**2. Morfolojik Özellikler:**
• Glomerüllerde segmental fibrinoid nekroz ve yaygın kresent oluşumu.
• **İF İncelemesi:** Floresan boyamada anlamlı immünglobulin veya kompleman birikimi izlenmez (**Pauci-İmmün**).""",
        [
            {"type": "warning", "badge": "🔴 SEROLOJİK / KLİNİK BAĞLANTI", "text": "Sinüzit, akciğerde kavitasyonlu nodüller ve kresentik böbrek yetmezliği triadı GPA (Wegener) düşündürmelidir; tanısal serolojik test c-ANCA'dır (PR3-ANCA).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Böbrek biyopsisinde glomerüllerde kresentler izlenen ancak immünofloresan mikroskopisi NEGATİF (pauci-immün) olan hastada kanda ANCA antikorları aranmalıdır.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-010",
            "question": "Kronik pürülan sinüzit, akciğer grafisinde bilateral kaviteli nodüller ve hızlı ilerleyen böbrek yetmezliği olan 55 yaşındaki hastanın biyopsisinde nekrotizan kresentik GN saptanıyor, İF negatif geliyor. Bu hastada hangi serolojik belirtecin pozitif olması beklenir?",
            "options": [
                "A) Anti-dsDNA",
                "B) c-ANCA (Anti-PR3)",
                "C) Anti-GBM",
                "D) Anti-Sm",
                "E) Anti-PLA2R"
            ],
            "correctAnswer": 1,
            "explanation": "Üst-alt solunum yolu granülomları ve pauci-immün kresentik nefrit Granülomatöz Polianjiyitisin (Wegener) klasik tablosudur ve c-ANCA (PR3-ANCA) pozitifliği ile karakterizedir."
        }
    ),
    make_slide(
        11,
        "Lupus Nefriti: Etyopatogenez ve DSÖ / ISN-RPS Sınıflaması",
        "Anti-dsDNA İmmün Kompleksleri, Sınıf I'den Sınıf VI'ya Morfolojik Yelpaze",
        """Sistemik Lupus Eritematozus (SLE), multipl organ tutulumuyla seyreden prototipik bir otoimmün hastalıktır; böbrek tutulumu (Lupus Nefriti) hastaların %50'sinde gelişir ve majör morbidite/mortalite nedenidir.

**1. Patogenez:**
Nükleer antijenlere (özellikle çift sarmallı DNA / dsDNA) karşı oluşan otoantikorlar dolaşımda immün kompleksler oluşturur veya doğrudan glomerüldeki nükleer antijenlere bağlanır. Kompleman aktivasyonu ağır bir doku hasarı başlatır.

**2. ISN-RPS (Uluslararası Nefroloji Derneği) Sınıflaması:**
• **Sınıf I — Minimal Mezangiyal Lupus Nefriti:** LM normaldir; sadece İF ve EM'de mezangiyal immün birikimler vardır.
• **Sınıf II — Mezangiyal Proliferatif Lupus Nefriti:** Mezangiyal hücre proliferasyonu ve matriks artışı vardır; prognozu çok iyidir, hafif proteinüri/hematüri yapar.
• **Sınıf III — Fokal Lupus Nefriti:** Glomerüllerin **<%50'si** tutulmuştur. Endokapiller ve mezangiyal proliferasyon, segmental nekroz izlenir.
• **Sınıf IV — Diffüz Lupus Nefriti:** Glomerüllerin **≥%50'si** tutulmuştur. En sık, en ağır ve en tahrip edici formdur.
• **Sınıf V — Membranöz Lupus Nefriti:** Diffüz subepitelyal depozitler ve GBM kalınlaşması; saf nefrotik sendrom tablosu yapar.
• **Sınıf VI — İlerlemiş Sklerozan Lupus Nefriti:** Glomerüllerin >%90'ı sklerozedir (son dönem böbrek).""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK SINIFLAMA KURALI", "text": "Lupus nefritinde Fokal (Sınıf III) ile Diffüz (Sınıf IV) arasındaki temel morfolojik sınır 'Glomerüllerin %50'sinin tutulup tutulmamasıdır'.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Lupus nefritinde en sık görülen, en ağır seyreden ve son dönem böbrek yetmezliğine en sık götüren tip Sınıf IV Diffüz Lupus Nefritidir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-011",
            "question": "Lupus nefriti sınıflamasında glomerüllerin %50 veya daha fazlasının tutulduğu, en ağır seyirli ve agresif immünsüpresif tedavi gerektiren form hangisidir?",
            "options": [
                "A) Sınıf I Minimal mezangiyal",
                "B) Sınıf II Mezangiyal proliferatif",
                "C) Sınıf III Fokal lupus nefriti",
                "D) Sınıf IV Diffüz proliferatif lupus nefriti",
                "E) Sınıf V Membranöz lupus nefriti"
            ],
            "correctAnswer": 3,
            "explanation": "Glomerüllerin %50'sinden fazlasının tutulduğu Sınıf IV Diffüz Lupus Nefriti en sık ve prognozu en kötü olan formdur."
        }
    ),
    make_slide(
        12,
        "Diffüz Lupus Nefriti (Sınıf IV): Tel Halka Lezyonları ve 'Full-House' İF Deseni",
        "Subendotelyal Dev Birikimler, Mikrotrombuslar ve Tübüloretiküler İnklüzyonlar",
        """Sınıf IV Lupus Nefriti, glomerüler patolojinin en zengin ve karmaşık morfolojik bulgularını barındırır.

**1. Işık Mikroskopisi (LM):**
• Glomerüller aşırı hiperselülerdir (endokapiller ve mezangiyal proliferasyon). Belirgin nötrofilik infiltrasyon ve kresentler sıktır.
• **Tel Halka (Wire-Loop) Lezyonları:** Glomerül kapiller duvarlarında aşırı subendotelyal immün kompleks birikimine bağlı olarak kapiller kıvrımların ışık mikroskobunda sert, rijit, kalın bir halka şeklinde görünmesidir. Lupus nefriti için son derece karakteristiktir.
• Kapiller lümenlerde fibrinoid nekroz ve hyalen mikrotrombuslar izlenebilir.

**2. İmmünofloresan (İF) — 'Full-House' Paterni:**
Lupus nefritinin İF incelemesinde glomerülde incelenen tüm immünglobulinler ve komplemanlar kuvvetli pozitif boyanır: **IgG, IgA, IgM, C3, C1q**. Bu çoklu boyanmaya **'Full-House' (Ful Ev) deseni** denir ve SLE nefriti için neredeyse tanı koydurucudur.

**3. Elektron Mikroskopisi (EM):**
Subendotelyal dev depozitler ve endotel hücresi sitoplazmasında yüksek interferon alfa düzeyine bağlı oluşan **tübüloretiküler inklüzyonlar** (retiküler cisimcikler) görülür.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "İmmünofloresanda IgG, IgA, IgM, C3 ve C1q'nun hep birlikte pozitif boyanması 'Full-House' paterni olarak adlandırılır ve SLE için karakteristiktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / KOMİTE KLASİĞİ", "text": "Işık mikroskobunda kapiller duvarlarda sertleşme ve kalınlaşma gösteren 'Wire-Loop' (Tel Halka) manzarası Sınıf IV Diffüz Lupus Nefritine özgüdür.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-012",
            "question": "SLE tanılı bir hastanın böbrek biyopsisinde ışık mikroskobunda kapiller duvarda belirgin 'wire-loop' (tel halka) lezyonları, İF'de ise IgG, IgA, IgM, C3 ve C1q'nun tümünün pozitif boyandığı 'Full-House' paterni izleniyor. Bu hasta hangi lupus nefriti sınıfındadır?",
            "options": [
                "A) Sınıf I",
                "B) Sınıf II",
                "C) Sınıf IV",
                "D) Sınıf V",
                "E) Sınıf VI"
            ],
            "correctAnswer": 2,
            "explanation": "Tel halka (wire-loop) lezyonları ve Full-House immünofloresan paterni en karakteristik olarak Sınıf IV Diffüz Proliferatif Lupus Nefritinde izlenir."
        }
    ),
    make_slide(
        13,
        "IgA Nefropatisi (Berger Hastalığı): Etyopatogenez ve Epidemiyoloji",
        "Dünyada En Sık Görülen Primer Glomerülonefrit ve Galaktoz Eksik IgA1 Patolojisi",
        """IgA Nefropatisi (Berger Hastalığı), tüm dünyada (özellikle Doğu Asya ve Akdeniz kuşağında) biyopsi ile kanıtlanan **en sık primer glomerülonefrittir**. En sık 15-30 yaş arası genç erkeklerde saptanır.

**1. Çok Basamaklı (Multi-Hit) Patogenez:**
• **Hit 1 (Genetik/Mukozal Tetik):** Mukozal bağışıklık sistemindeki disregülasyon sonucu kemik iliğinde menteşe bölgesindeki O-glikanlarında galaktoz molekülü bulunmayan anormal bir immünglobulin üretilir: **Galaktoz Eksikliği Olan IgA1 (Gd-IgA1)**.
• **Hit 2 (Otoantikor Oluşumu):** Dolaşımdaki bu anormal Gd-IgA1 molekülüne karşı vücut tarafından otoantikorlar (özellikle anti-glikan IgG veya IgA) üretilir.
• **Hit 3 (İmmün Kompleks Teşekkülü):** Gd-IgA1 ile IgG molekülleri dolaşımda stabil immün kompleksler oluşturur.
• **Hit 4 (Mezangiyal Depolanma ve Hasar):** Bu kompleksler glomerül mezangiyal hücrelerindeki reseptörlere bağlanarak mezangiyuma çöker. Mezangiyal hücre proliferasyonunu uyarır, komplemanın alternatif ve lektin yolunu aktive eder.""",
        [
            {"type": "warning", "badge": "🔴 EPİDEMİYOLOJİK GERÇEK", "text": "Dünya genelinde renal biyopsi yapılan olgularda en sık saptanan primer glomerülonefrit IgA Nefropatisidir (Berger Hastalığı).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "IgA nefropatisinin patogenezinde rol oynayan temel moleküler anormallik menteşe bölgesinde 'galaktoz eksikliği olan IgA1' (Galactose-deficient IgA1) üretimidir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-013",
            "question": "Primer glomerüler hastalıklar arasında dünya çapında en sık görülen ve patogenezinde anormal galaktoz-eksik IgA1 moleküllerinin mezangiyumda birikmesi rol oynayan antite hangisidir?",
            "options": [
                "A) Minimal değişiklik hastalığı",
                "B) Membranöz nefropati",
                "C) IgA nefropatisi (Berger)",
                "D) Poststreptokokkal GN",
                "E) FSGS"
            ],
            "correctAnswer": 2,
            "explanation": "Dünyada en sık görülen primer glomerülonefrit IgA nefropatisidir (Berger Hastalığı)."
        }
    ),
    make_slide(
        14,
        "IgA Nefropatisi: Klinik Tablo, 'Senfaranjitik Hematüri' ve Tanı",
        "ÜSYE ile Eş Zamanlı (1-2 Gün İçinde) Makroskopik Hematüri ve Normal Kompleman",
        """IgA nefropatisinin klinik tablosu çok tipik epizodlarla kendini gösterir.

**1. Senfaranjitik Makroskopik Hematüri:**
• Hastaların %40-50'sinde en klasik klinik sunum; bir üst solunum yolu enfeksiyonu (veya gastrointestinal sistem enfeksiyonu, ağır egzersiz) başladıktan **1 ila 2 gün sonra** aniden makroskopik (çay veya et suyu rengi) hematüri atağının ortaya çıkmasıdır.
• Hematüri enfeksiyonla adeta eş zamanlı seyreder (**senfaranjitik hematüri**). Enfeksiyon yatışınca hematüri birkaç gün içinde mikroskopik düzeye geriler; ancak sonraki enfeksiyonlarda tekrar alevlenir.
• **APSGN'den Keskin Fark:** Poststreptokokkal GN'de enfeksiyon ile hematüri arasında 1-3 haftalık latent dönem varken, IgA nefropatisinde latent dönem yoktur veya 1-2 günü geçmez!

**2. Asemptomatik Mikroskopik Hematüri:**
Olguların diğer %30-40'ı genç bireylerde rutin taramalarda tesadüfen saptanan izole mikroskopik hematüri ve hafif proteinüri ile prezante olur.

**3. Laboratuvar:**
Serum C3 ve C4 kompleman düzeyleri olguların >%90'ında **tamamen normaldir** (APSGN'deki gibi hipokomplementemi izlenmez). Serum IgA düzeyi hastaların sadece %50'sinde yüksek bulunur, bu nedenle tanısal değildir.""",
        [
            {"type": "clinical", "badge": "🔴 KRİTİK AYIRICI TANI", "text": "Farenjit geçiren genç bir hastada 24-48 saat içinde ani hematüri başlaması ve serum C3 düzeyinin normal olması doğrudan IgA Nefropatisini işaret eder.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS KLASİĞİ", "text": "Senfaranjitik hematüri (enfeksiyonla eş zamanlı hematüri) IgA nefropatisine özgüdür. Serum kompleman seviyeleri daima normaldir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-014",
            "question": "20 yaşındaki bir üniversite öğrencisi boğaz ağrısı ve ateş şikayetinin başladığı günün ertesi sabahı (24 saat sonra) idrarının çay renginde olduğunu fark ediyor. Tansiyonu normal, serum C3 düzeyi normal saptanıyor. En olası tanı hangisidir?",
            "options": [
                "A) Akut poststreptokokkal glomerülonefrit",
                "B) IgA nefropatisi (Berger)",
                "C) Alport sendromu",
                "D) C3 glomerulopatisi",
                "E) Membranöz nefropati"
            ],
            "correctAnswer": 1,
            "explanation": "Üst solunum yolu enfeksiyonundan sadece 1 gün sonra ortaya çıkan makroskopik hematüri ve normal C3 düzeyi senfaranjitik hematüriyi ve IgA nefropatisini gösterir."
        }
    ),
    make_slide(
        15,
        "IgA Nefropatisi ve Henoch-Schönlein Purpurası (IgA Vasküliti) Morfolojisi",
        "Mezangiyal Genişleme, Baskın Mezangiyal IgA Birikimi ve Oxford (MEST-C) Skoru",
        """IgA nefropatisinde kesin tanı böbrek biyopsisinde mezangiyal IgA depolanmasının gösterilmesiyle konur.

**1. Işık Mikroskopisi (LM):**
• En sık izlenen patern **mezangiyoproliferatif glomerülonefrittir** (mezangiyal hücre sayısında artış ve matriks genişlemesi).
• Oxford Sınıflaması (**MEST-C Skoru**):
  - **M:** Mezangiyal hiperselülarite,
  - **E:** Endokapiller hiperselülarite,
  - **S:** Segmental skleroz,
  - **T:** Tübüler atrofi ve interstisyel fibrozis (en güçlü prognostik faktör),
  - **C:** Kresent (hilal) varlığı.

**2. İmmünofloresan (İF) — Kesin Tanı:**
Glomerül **mezangiyumunda baskın veya eş-baskın granüler IgA birikimi** saptanır. Çoğu olguda C3 ve bazen IgG eşlik eder ancak C1q negatiftir.

**3. Henoch-Schönlein Purpurası (IgA Vasküliti):**
• Çocuklarda görülen sistemik bir lökositoklastik vaskülittir.
• Klinik tetrad: Alt ekstremitede yerçekimiyle artan **palpeabl purpura**, kolik tarzı **karın ağrısı / GİS kanaması**, **artralji/artrit** ve **böbrek tutulumu**.
• Böbrek biyopsisi morfolojik ve immünofloresan olarak IgA nefropatisi ile **birebir aynıdır** (mezangiyal IgA depozitleri).""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK EŞDEĞERLİK", "text": "Henoch-Schönlein Purpurasının böbrek tutulumu histopatolojik ve immünofloresan olarak IgA nefropatisinden ayırt edilemez; fark HSP'deki sistemik vaskülit bulgularıdır (purpura, GİS, artrit).", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "IgA nefropatisinde altın standart tanı kriteri immünofloresanda mezangiyumda diffüz granüler IgA depolanmasının gösterilmesidir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-015",
            "question": "7 yaşındaki bir çocukta kalçalarda ve bacaklarda basmakla solmayan döküntüler (palpeabl purpura), karın ağrısı ve makroskopik hematüri gelişiyor. Yapılan böbrek biyopsisinde immünofloresan incelemede hangi birikimin izlenmesi beklenir?",
            "options": [
                "A) GBM boyunca lineer IgG",
                "B) Mezangiyumda granüler IgA",
                "C) Subepitelyal alanda granüler IgG4",
                "D) Kapiller duvarda kaba C3",
                "E) Subendotelyal Full-House birikim"
            ],
            "correctAnswer": 1,
            "explanation": "Henoch-Schönlein purpurasında (IgA vasküliti) böbrek biyopsisinde mezangiyal granüler IgA depozitleri izlenir."
        }
    ),
    make_slide(
        16,
        "Alport Sendromu: Genetik, Patogenez ve Klinik Triad",
        "Tip IV Kollajen Alfa-5 Zinciri (COL4A5), Nefrit, İşitme Kaybı ve Oküler Lezyonlar",
        """Alport sendromu, bazal membran tip IV kollajen moleküllerinin genetik defekti sonucu gelişen, ilerleyici kalıtsal bir nefrittir.

**1. Genetik Geçiş ve Mutasyonlar:**
• **X'e Bağlı Dominant (%85):** En sık formdur. X kromozomu (Xq22) üzerindeki **COL4A5** geninde mutasyon vardır. Erkekler tam klinik tablo geliştirir ve erken yaşta son dönem böbrek yetmezliğine girer; heterozigot kadınlar ise genellikle asemptomatik mikroskopik hematüri ile seyreder.
• **Otozomal Resesif (%15):** *COL4A3* veya *COL4A4* gen mutasyonları; hem kadın hem erkek ağır etkilenir.

**2. Klasik Klinik Triad:**
1. **İlerleyici Hematürik Nefrit:** Çocuklukta mikroskopik hematüri ile başlar; zamanla proteinüri, hipertansiyon ve 20-30'lu yaşlarda son dönem böbrek yetmezliği gelişir.
2. **Sensörinöral İşitme Kaybı:** Kokleanın baziler membranındaki kollajen defektine bağlıdır; yüksek frekanslı sesleri (tiz sesler) etkileyen bilateral ilerleyici işitme kaybıdır.
3. **Oküler Bozukluklar:** Göz merceği kapsülünün incelmesine bağlı **anterior lentikonus** (merceğin öne doğru konik çıkıntı yapması) ve retinada maküler beneklenme (flecks). Anterior lentikonus Alport sendromu için **patognomoniktir**.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Anterior lentikonus göz muayenesinde saptandığında Alport sendromu tanısı için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Alport sendromu triadı: İlerleyici nefrit (hematüri/böbrek yetmezliği) + Çift taraflı sensörinöral işitme kaybı + Oküler lezyonlar (anterior lentikonus). En sık X'e bağlı COL4A5 mutasyonudur.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-016",
            "question": "Tekrarlayan hematürisi olan 18 yaşındaki bir erkek hastada yapılan muayenede bilateral sensörinöral işitme kaybı ve gözde anterior lentikonus saptanıyor. Bu hastada mutasyona uğramış gen hangisidir?",
            "options": [
                "A) COL4A5",
                "B) NPHS1",
                "C) PKD1",
                "D) VHL",
                "E) WT1"
            ],
            "correctAnswer": 0,
            "explanation": "Alport sendromunun X'e bağlı formundan sorumlu gen Tip IV kollajen alfa-5 zincirini kodlayan COL4A5 genidir."
        }
    ),
    make_slide(
        17,
        "Alport Sendromu ve İnce Bazal Membran Hastalığı Morfolojisi",
        "EM'de 'Sepet Örgüsü' (Basket-Weave) Ayrılması ve İzole Diffüz GBM İncelmesi",
        """Kalıtsal nefritlerde kesin morfolojik ayrım elektron mikroskopisi (EM) ile yapılır; zira ışık mikroskobu erken dönemde tamamen normaldir.

**1. Alport Sendromu Morfolojisi:**
• Erken dönemde GBM incelmiştir. Zamanla bazal membranda ilerleyici bir yapısal dağılma başlar.
• **Elektron Mikroskopisi (EM):** Glomerüler bazal membranın lamina densasında düzensiz kalınlaşma, incelme, çatallanma ve lamellere ayrılma (**'Sepet Örgüsü' / Basket-Weave deseni**) izlenir. Lamellerin arasında granüler elektron-yoğun artıklar birikir. Bu görünüm Alport sendromunun histopatolojik imzasıdır.
• İnterstisyumda nötral yağ ve mukopolisakkarit yüklü **köpüksü hücreler (foam cells)** sıktır.

**2. İnce Bazal Membran Hastalığı (Benign Ailesel Hematüri):**
• Otozomal dominant kalıtılır (*COL4A3* veya *COL4A4* heterozigot mutasyonu).
• **Elektron Mikroskopisi (EM):** GBM yapısı tamamen homojen ve intaktır ancak lamina densa aşırı derecede incelmiştir. Normal erişkinde 300-400 nm olan GBM kalınlığı **150-250 nm** seviyesine düşmüştür.
• **Klinik Önem:** Asemptomatik kalıcı mikroskopik hematüri ile seyreder. Böbrek yetmezliği, işitme kaybı veya görme kusuru **asla gelişmez!** Prognoz mükemmeldir, tedavi gerektirmez.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK AYRIM", "text": "EM'de sepet örgüsü (basket-weave) lamelleşme Alport sendromunu; homojen kesintisiz aşırı incelme (<250 nm) ise İnce Bazal Membran Hastalığını kanıtlar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "İnce bazal membran hastalığında izole mikroskopik hematüri vardır; böbrek fonksiyonları daima normal kalır ve prognoz tamamen benign seyreder.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-017",
            "question": "Ailesinde birçok kişide mikroskopik hematüri bulunan ancak hiçbirinde böbrek yetmezliği gelişmeyen 22 yaşındaki hastanın renal biyopsisinde elektron mikroskobunda GBM kalınlığının difüz olarak 180 nm'ye inceldiği, ancak lamelleşme veya sepet örgüsü bulunmadığı saptanıyor. Tanı nedir?",
            "options": [
                "A) Alport sendromu",
                "B) İnce bazal membran hastalığı (Benign ailesel hematüri)",
                "C) Minimal değişiklik hastalığı",
                "D) IgA nefropatisi",
                "E) Poststreptokokkal GN"
            ],
            "correctAnswer": 1,
            "explanation": "Homojen ve difüz GBM incelmesi (<250 nm) ve benign seyir İnce Bazal Membran Hastalığının (Benign ailesel hematüri) patognomonik tablosudur."
        }
    ),
    make_slide(
        18,
        "Nefritik Sendromda Kompleman Düzeylerine Göre Ayırıcı Tanı",
        "Hipokomplementemik vs Normokomplementemik Glomerülonefritler",
        """Nefritik sendrom ile başvuran bir hastada ayırıcı tanının en kritik ve en hızlı laboratuvar basamağı **serum C3 ve C4 kompleman düzeylerinin ölçümüdür**.

**1. Düşük Komplemanlı (Hipokomplementemik) Nefritler:**
• **Akut Poststreptokokkal Glomerülonefrit (APSGN):** C3 aşırı düşük, C4 genellikle normal/hafif düşük. (6-8 haftada C3 normale döner).
• **Lupus Nefriti (Özellikle Sınıf IV):** Klasik yol tükenir; hem **C3 hem C4 belirgin derecede düşüktür**. Anti-dsDNA yüksekliği eşlik eder.
• **Membranoproliferatif Glomerülonefrit (MPGN Tip I):** Hem C3 hem C4 düşüktür; kalıcıdır.
• **C3 Glomerülopatisi (Yoğun Birikim Hastalığı):** Alternatif yol tükenir; **izole C3 aşırı düşüktür, C4 tamamen normaldir**.
• **Subakut Bakteriyel Endokardit ve Şant Nefriti:** C3 ve C4 düşüktür.

**2. Normal Komplemanlı (Normokomplementemik) Nefritler:**
• **IgA Nefropatisi (Berger Hastalığı):** C3 ve C4 daima normaldir.
• **Henoch-Schönlein Purpurası (IgA Vasküliti):** Normaldir.
• **Pauci-İmmün Kresentik GN (GPA / MPA - ANCA Pozitif Vaskülitler):** Normaldir.
• **Anti-GBM Hastalığı (Goodpasture):** Normaldir.
• **Alport Sendromu ve İnce Bazal Membran Hastalığı:** Normaldir.""",
        [
            {"type": "clinical", "badge": "🔴 TANI MATRİSİ", "text": "Hematürisi olan hastada C3 düşükse: APSGN, Lupus, MPGN veya Endokardit düşünülür. C3 normalse: IgA Nefropatisi, ANCA vasküliti veya Anti-GBM düşünülür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV TABLOSU", "text": "IgA nefropatisi ve ANCA ilişkili vaskülitlerde kompleman düzeyleri NORMALDİR; APSGN ve Lupusta ise kompleman DÜŞÜKTÜR.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-018",
            "question": "Aşağıdaki nefritik sendrom nedenlerinden hangisinde serum C3 ve C4 kompleman düzeylerinin normal olması beklenir?",
            "options": [
                "A) Akut poststreptokokkal glomerülonefrit",
                "B) Diffüz proliferatif lupus nefriti",
                "C) IgA nefropatisi (Berger)",
                "D) MPGN Tip I",
                "E) Subakut bakteriyel endokardit ilişkili nefrit"
            ],
            "correctAnswer": 2,
            "explanation": "IgA nefropatisinde serum kompleman düzeyleri (C3 ve C4) normal sınırlardadır. Diğer tüm seçeneklerde belirgin kompleman tüketimi ve hipokomplementemi izlenir."
        }
    ),
    make_slide(
        19,
        "Kronik Glomerülonefrit: Son Dönem Böbrek Yetmezliğinin Nihai Morfolojisi",
        "Büzüşmüş Böbrekler, Sklerotik Hiyalin Glomerüller, Fibrozis ve Üremik Toksisite",
        """Kronik glomerülonefrit bağımsız bir primer antite olmayıp, tedavi edilmemiş veya tedaviye yanıtsız kalmış çeşitli glomerülonefritlerin (özellikle RPGN, FSGS, MPGN, Membranöz ve IgA nefropatisi) son durağıdır.

**1. Makroskobik Morfoloji:**
• Her iki böbrek simetrik olarak küçülmüş ve büzüşmüştür (ağırlıkları 50-80 grama kadar düşebilir).
• Böbrek yüzeyi granüler, pürtüklü ve soluk renklidir. Kapsül zor soyulur.
• Kesit yüzeyinde korteks aşırı derecede incelmiş (bazen 1-2 mm), kortikomedüller ayrım silinmiştir. Peripelvik yağ dokusu artmıştır.

**2. Mikroskobik Morfoloji:**
• **Glomerüler Skleroz:** Glomerüller hücresiz, aselüler, pembe PAS pozitif kollajen kitlelerine (**hyalinize glomerüller**) dönüşmüştür.
• **Tübüler Değişiklikler:** Tubulusların büyük kısmı atrofiye uğramış ve kaybolmuştur; kalan bazı tubuluslar genişlemiş ve içleri eozinofilik silindirlerle dolmuştur (**tiroidizasyon**).
• **İnterstisyel Fibrozis:** Yaygın bağ dokusu artışı ve kronik mononükleer enflamatuar infiltrat (lenfosit ve plazma hücreleri).
• **Vasküler Skleroz:** İkincil hipertansiyona bağlı arter ve arteriyollerde kalınlaşma ve hyalinozis.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK GERÇEK", "text": "Kronik böbrek yetmezliğine giren büzüşmüş bir böbrekte yapılan biyopside primer başlangıç hastalığını teşhis etmek imkansızdır; tüm lezyonlar non-spesifik glomerüloskleroz ve interstisyel fibrozisle sonlanır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Kronik glomerülonefritte böbrekler simetrik küçülmüş, yüzeyleri ince granüler ve korteksleri ileri derecede incelmiştir.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-019",
            "question": "Son dönem böbrek yetmezliğine ilerlemiş kronik glomerülonefrit olgusunda otopside beklenen karakteristik makroskobik böbrek bulgusu hangisidir?",
            "options": [
                "A) Asimetrik devasa boyutta kistik böbrekler",
                "B) İki taraflı simetrik büzüşmüş, soluk renkli, ince granüler yüzeyli ve korteksi aşırı incelmiş böbrekler",
                "C) Yalnızca sol böbrekte hidronefrotik büyüme",
                "D) Pariyetal subkapsüler kanama odakları içeren devasa böbrekler",
                "E) Kortikomedüller ayrımın keskinleştiği hiperemik böbrekler"
            ],
            "correctAnswer": 1,
            "explanation": "Kronik glomerülonefritte her iki böbrek simetrik olarak küçülür, yüzeyi ince granüler hal alır ve parankim (özellikle korteks) ileri derecede incelir."
        }
    ),
    make_slide(
        20,
        "Glomerülonefritlerde İmmünofloresan Paternlerinin Karşılaştırmalı Atlası",
        "Lineer, Granüler ve Pauci-İmmün Floresan İmzaları",
        """İmmünofloresan (İF) mikroskopisi böbrek biyopsisinde immünopatogenetik mekanizmayı doğrudan ortaya koyan en değerli teşhis yöntemidir.

**1. Temel İF Paternleri:**
• **Lineer (Çizgisel) Patern:**
  - Kapiller duvar boyunca kesintisiz, pürüzsüz, cetvelle çizilmiş gibi düzgün floresan.
  - *Hastalık:* Anti-GBM Glomerülonefriti ve Goodpasture Sendromu (Lineer IgG).
• **Granüler (Taneli) Patern:**
  - İmmün komplekslerin birikmesiyle oluşur; irili ufaklı tanecikli, benekli floresan.
  - *Kaba Granüler / Yıldızlı Gökyüzü:* Akut Poststreptokokkal GN (C3 ve IgG).
  - *Diffüz İnce Granüler (Subepitelyal):* Membranöz Nefropati (IgG ve C3).
  - *Lobüler / Çift Hat Granüler (Subendotelyal):* MPGN Tip I (IgG, C3).
  - *Baskın Mezangiyal Granüler:* IgA Nefropatisi ve Henoch-Schönlein (IgA).
  - *Full-House Granüler:* Lupus Nefriti Sınıf IV (IgG, IgA, IgM, C3, C1q).
  - *İzole Aşırı Parlak Granüler C3:* Yoğun Birikim Hastalığı / C3 Glomerülopatisi.
• **Pauci-İmmün (Negatif veya Önemsiz Düzeyde Boyanma):**
  - İF'de anlamlı immünglobulin ve kompleman saptanmaz.
  - *Hastalıklar:* ANCA Pozitif Vaskülitler (GPA / Wegener, MPA, EGPA).""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Lineer = Goodpasture; Yıldızlı Gökyüzü = APSGN; Mezangiyal IgA = Berger; Full-House = Lupus; Negatif İF = ANCA Vasküliti.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SORUSU", "text": "Bu slaytta özetlenen 5 immünofloresan deseni tıbbi patoloji ve nefroloji komite sınavlarının en garanti soru havuzudur.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-020",
            "question": "Böbrek biyopsisinde immünofloresan mikroskobunda glomerül kapiller duvarı boyunca kesintisiz lineer IgG boyanması aşağıdaki hastalıkların hangisi için patognomoniktir?",
            "options": [
                "A) Akut poststreptokokkal GN",
                "B) Goodpasture sendromu (Anti-GBM hastalığı)",
                "C) Membranöz nefropati",
                "D) Lupus nefriti Sınıf IV",
                "E) Granülomatöz polianjiyitis"
            ],
            "correctAnswer": 1,
            "explanation": "Lineer IgG boyanması GBM'ye doğrudan bağlanan otoantikorları gösterir ve Goodpasture sendromu / Anti-GBM hastalığı için patognomoniktir."
        }
    ),
    make_slide(
        21,
        "Nefritik Sendromlu Hastaya Klinik ve Laboratuvar Yaklaşımı",
        "İdrar Sedimentinden Biyopsi Kararına Basamaklı Algoritma",
        """Klinik pratikte nefritik sendrom şüphesi olan bir hastada adım adım izlenecek yönetim protokolü:

**1. Basamak 1 — İdrar ve Sediment Değerlendirmesi:**
• Taze sabah idrarında santrifüj sonrası faz-kontrast mikroskopisi: Dismorfik eritrositlerin oranı >%80 ve eritrosit silindirleri görülürse nefritik tablo doğrulanır.
• Günlük proteinüri tayini (genellikle subnefrotik düzeydedir).

**2. Basamak 2 — Kompleman ve Seroloji:**
• Serum C3 ve C4 düzeyleri istenir:
  - C3 Düşük ise: ASO ve Anti-DNAse B (APSGN), ANA ve anti-dsDNA (Lupus), Anti-HCV (MPGN).
  - C3 Normal ise: ANCA paneli (c-ANCA, p-ANCA), Anti-GBM antikoru, Serum IgA düzeyi.

**3. Basamak 3 — Biyopsi Kararı ve Aciliyet:**
• Tipik çocukluk çağı poststreptokokkal nefritinde biyopsi yapılmaz; izlenir.
• **Acil Renal Biyopsi Endikasyonları:**
  - Hızlı bozulan böbrek fonksiyonu (RPGN şüphesi),
  - Cilt döküntüsü, pulmoner kanama gibi sistemik vaskülit bulguları,
  - 8 haftadan uzun süren hipokomplementemi,
  - Etyolojisi aydınlatılamayan tüm erişkin nefritik tablolar.""",
        [
            {"type": "clinical", "badge": "🔴 ACİL KLİNİK YAKLAŞIM", "text": "Nefritik sendromlu bir hastada kreatinin her gün yükseliyorsa kresentik glomerülonefrit (RPGN) şüphesiyle 24 saat içinde acil renal biyopsi planlanmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ BİLGİ", "text": "Poststreptokokkal GN'de biyopsi kural dışıdır; ancak oligüri 2 haftayı geçerse veya C3 düzeyi 8 haftada normale dönmezse renal biyopsi zorunludur.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-021",
            "question": "Aşağıdaki klinik durumların hangisinde renal biyopsi yapılması kesinlikle endike DEĞİLDİR?",
            "options": [
                "A) Streptokokkal farenjitten 10 gün sonra tipik hafif nefritik sendrom geliştiren ve düzelme eğiliminde olan 7 yaşındaki çocuk",
                "B) Akut nefrit tablosuna hemoptizinin eşlik ettiği 25 yaşındaki genç",
                "C) Poststreptokokkal GN tanısı konan ancak 10 haftadır serum C3 düzeyi düşük seyreden hasta",
                "D) Günler içinde kreatinini 1 mg/dL'den 4 mg/dL'ye yükselen 50 yaşındaki hasta",
                "E) Sistemik lupus eritematozus tanılı hastada yeni başlayan proteinüri ve hematüri"
            ],
            "correctAnswer": 0,
            "explanation": "Tipik klinik ve laboratuvarla seyreden çocukluk çağı APSGN olgularında prognoz %95 tam iyileşme olduğundan biyopsi endikasyonu yoktur."
        }
    ),
    make_slide(
        22,
        "Nefrotik ve Nefritik Sendromların Karşılaştırmalı Büyük Klinik Matrisi",
        "Klinik, İdrar Sedimenti, Proteinüri Düzeyi ve Temel Patolojilerin Karşılaştırılması",
        """Tıbbi patoloji ve nefrolojinin iki temel büyük sendromunun karşılaştırmalı matrisi:

| Özellik | Nefrotik Sendrom | Nefritik Sendrom |
| :--- | :--- | :--- |
| **Primer Patoloji** | Podosit ve slit diyafram hasarı | Glomerül içi enflamasyon ve endotel/mezangiyal proliferasyon |
| **Proteinüri Düzeyi** | Masif (>3.5 g/gün/1.73 m²) | Hafif-orta (Genellikle <3 g/gün) |
| **Hematüri** | Yok veya hafif mikroskopik | Belirgin makroskopik (çay/kola renkli) veya mikroskopik |
| **İdrar Sedimenti** | Hücresiz (bland), oval yağ cisimcikleri, lipid damlacıkları | Dismorfik eritrositler, eritrosit silindirleri, lökositler |
| **Ödem Mekanizması** | Hipoalbüminemi ve plazma onkotik basınç düşüşü | Primer GFR düşüşü ve renal sodyum-su retansiyonu (hipervolemi) |
| **Kan Basıncı** | Genellikle normal (erken evrede) | Karakteristik olarak YÜKSEK (Hipertansiyon) |
| **Serum Albümini** | Ağır derecede DÜŞÜK (<3.0 g/dL) | Genellikle normal veya hafif düşük |
| **Hiperlipidemi** | Belirgin (Kolesterol ve trigliserid yüksek) | Genellikle yok |
| **Prototipik Hastalıklar** | MDH, FSGS, Membranöz Nefropati | APSGN, RPGN, IgA Nefropatisi, ANCA vasküliti |""",
        [
            {"type": "warning", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "Nefrotik sendromun imzası hücresiz bland sedimentte lipidüri ve masif proteinüri; Nefritik sendromun imzası ise eritrosit silindirleri ve hipertansiyondur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV MATRİSİ", "text": "Bu tablo hem Dönem 3 patoloji komitesinde hem de TUS Klinik Nefroloji bölümünde soruların doğrudan referans noktasıdır.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-022",
            "question": "Aşağıdaki özelliklerden hangisi nefritik sendromu nefrotik sendromdan ayıran en güvenilir klinikopatolojik bulgudur?",
            "options": [
                "A) 24 saatlik idrarda 4 gram albümin bulunması",
                "B) İdrar sedimentinde eritrosit silindirlerinin ve dismorfik eritrositlerin saptanması",
                "C) Serum albümin düzeyinin 2.2 g/dL olması",
                "D) Pretibial gode bırakan yaygın ödem varlığı",
                "E) Serumda total kolesterol ve trigliserid yüksekliği"
            ],
            "correctAnswer": 1,
            "explanation": "Eritrosit silindirleri glomerül kapiller duvarındaki aktif nekrotizan ve proliferatif enflamasyonun (nefritik sendrom) doğrudan kanıtıdır."
        }
    ),
    make_slide(
        23,
        "Nefritik Sendrom: Ayırıcı Tanı ve Patoloji Karşılaştırma Tablosu",
        "APSGN, RPGN Tipleri, Lupus Sınıf IV ve IgA Nefropatisinin Mikroskobik Özeti",
        """Başlıca nefritik sendrom nedenlerinin histopatolojik, immünofloresan ve elektron mikroskopisi tablosu:

| Hastalık | Işık Mikroskobu (LM) | İmmünofloresan (İF) | Elektron Mikroskobu (EM) | Kompleman (C3) | Klinik İpucu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **APSGN** | Diffüz proliferatif ve eksüdatif GN (nötrofiller) | Kaba granüler C3 ve IgG ('Yıldızlı Gökyüzü') | Büyük subepitelyal hörgüçler (**Humps**) | C3 aşırı düşük (6-8 haftada döner) | Farenjitten 1-2 hf sonra kola idrar, ASO/DNAse B+ |
| **RPGN Tip I (Anti-GBM)** | Glomerüllerin >%50'sinde Kresent (hilal), nekroz | Kesintisiz **Lineer IgG** ve C3 | Depozit yok, GBM yırtıkları | Normal | Hemoptizi + Nefrit (Goodpasture) |
| **RPGN Tip II (İmmün Kompleks)** | Kresentler + altta yatan GN lezyonu | **Granüler** IgG, C3 birikimi | Subendotelyal veya mezangiyal depozitler | Genellikle Düşük | SLE, APSGN veya MPGN alevlenmesi |
| **RPGN Tip III (Pauci-İmmün)** | Kresentler, segmental fibrinoid nekroz | **Negatif** veya çok zayıf (Pauci-İmmün) | Depozit yok, kapiller tromboz | Normal | ANCA pozitifliği (c-ANCA: Wegener, p-ANCA: MPA) |
| **Lupus Nefriti (Sınıf IV)** | Endokapiller proliferasyon, **Tel Halka** (wire-loop) | **Full-House** (IgG, IgA, IgM, C3, C1q) | Subendotelyal dev depozitler, tübüloretiküler | C3 ve C4 aşırı düşük | ANA+, anti-dsDNA+, genç kadın |
| **IgA Nefropatisi (Berger)** | Mezangiyoproliferatif GN | Mezangiyumda diffüz granüler **IgA** ve C3 | Mezangiyal elektron-yoğun depozitler | Normal | ÜSYE ile eş zamanlı (1-2 gün) hematüri |""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Subepitelyal Hump = APSGN; Lineer IgG = Anti-GBM; Pauci-immün = ANCA vasküliti; Full-house = Lupus; Mezangiyal IgA = Berger.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu matristeki morfolojik eşleştirmeler patoloji ve dahiliye sınavlarında doğrudan soru getiren temel kalıptır.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-023",
            "question": "Aşağıdaki glomerüler hastalık ve elektron mikroskobundaki karakteristik bulgu eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) Akut poststreptokokkal GN — Subepitelyal hörgüçler (humps)",
                "B) Membranöz nefropati — Subepitelyal depozitler ve spike-dome",
                "C) Alport sendromu — GBM lamina densasında 'sepet örgüsü' (basket-weave)",
                "D) IgA nefropatisi — Yaygın subendotelyal tel halka depozitleri",
                "E) Minimal değişiklik hastalığı — Podosit ayaksı çıkıntılarında silinme"
            ],
            "correctAnswer": 3,
            "explanation": "IgA nefropatisinde depozitler subendotelyal değil, MEZANGİYAL yerleşimlidir. Subendotelyal tel halka depozitleri Sınıf IV Lupus Nefritine özgüdür."
        }
    ),
    make_slide(
        24,
        "Ders 20 Kapsamlı Sentezi: Nefritik Sendrom Patolojisinin Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Nefritik Sendrom dersinin komite ve klinik pratik için akılda kalması gereken 10 altın kuralı:

**1. Nefritik Patolojinin 10 Altın Kuralı:**
1. *Nefritik Tetrad:* Hematüri (dismorfik eritrosit + eritrosit silindiri), oligüri, azotemi ve hipertansiyon.
2. *APSGN:* Farenjitten 1-2 hafta, cilt enfeksiyonundan 2-4 hafta sonra başlar. Nefritojenik suşlar M12 ve M49'dur.
3. *APSGN Morfoloji:* LM'de diffüz proliferatif/eksüdatif GN; İF'de kaba granüler yıldızlı gökyüzü; EM'de subepitelyal hörgüçler (humps).
4. *APSGN Kompleman:* Serum C3 aşırı düşüktür; 6-8 haftada mutlaka normale dönmelidir.
5. *RPGN (Kresentik GN):* Glomerüllerin ≥%50'sinde kresent vardır; kresentleri oluşturan pariyetal epitel hücreleri ve makrofajlardır (uyaran fibrindir).
6. *RPGN Sınıflaması:* Tip I = Lineer IgG (Anti-GBM / Goodpasture); Tip II = Granüler (SLE, APSGN); Tip III = Pauci-İmmün (ANCA pozitif vaskülitler).
7. *Lupus Nefriti Sınıf IV:* En sık ve en ağır tip; LM'de Tel Halka (Wire-Loop), İF'de Full-House paterni (IgG, IgA, IgM, C3, C1q).
8. *IgA Nefropatisi (Berger):* Dünyada en sık primer GN; ÜSYE'den 1-2 gün sonra senfaranjitik hematüri ile başlar; kompleman daima normaldir; İF'de mezangiyal IgA pozitiftir.
9. *Alport Sendromu:* X'e bağlı COL4A5 mutasyonu; nefrit + işitme kaybı + anterior lentikonus; EM'de sepet örgüsü (basket-weave).
10. *İnce Bazal Membran Hastalığı:* Benign ailesel hematüri; izole GBM incelmesi (<250 nm); prognoz mükemmeldir.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Klinikte kola renkli idrarla gelen hastada ÜSYE ile zaman ilişkisi anahtardır: 1-2 gün sonraysa IgA nefropatisi; 1-2 hafta sonraysa poststreptokokkal GN'dir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta yer alan 10 altın kural nefritik sendrom komite ve TUS sorularının tamamını kapsamaktadır.", "color": "sky"}
        ],
        {
            "id": "prac-nefr-024",
            "question": "Aşağıdaki klinik tablolardan hangisinde hastada kompleman düzeyinin (C3) DÜŞÜK olması ve farenjitten sonraki latent periyodun 10-14 gün olması beklenir?",
            "options": [
                "A) Akut poststreptokokkal glomerülonefrit",
                "B) IgA nefropatisi (Berger)",
                "C) Granülomatöz polianjiyitis (Wegener)",
                "D) Goodpasture sendromu",
                "E) Alport sendromu"
            ],
            "correctAnswer": 0,
            "explanation": "Farenjitten 10-14 gün sonra başlayan nefrit ve serum C3 düşüklüğü Akut Poststreptokokkal Glomerülonefritin (APSGN) klasik tablosudur."
        }
    )
]

print("Nefritik Sendrom 24 slayt başarıyla tanımlandı.")

target_id = 'learn-glomeruler-hastaliklar-nefritik'
for d in decks:
    if d.get('id') == target_id:
        d['title'] = "Glomerüler Hastalıklar: Nefritik Sendrom Patolojisi"
        d['shortTitle'] = "Nefritik Sendrom Patolojisi"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Akut nefritik sendrom klinik tetradı, Poststreptokokkal GN (SpeB, subepitelyal hörgüçler, yıldızlı gökyüzü), RPGN kresent patolojisi (Tip I Lineer, Tip II Granüler, Tip III Pauci-İmmün/ANCA), Lupus Nefriti (Tel halka, Full-House), IgA Nefropatisi (Senfaranjitik hematüri) ve Alport sendromu."
        d['slides'] = nefritik_slides
        print(f"'{target_id}' güvertesi 24 yüksek kaliteli slaytla güncellendi.")
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("Nefritik Sendrom güncellemesi tamamlandı.")
