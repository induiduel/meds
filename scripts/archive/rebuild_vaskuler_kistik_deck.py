# -*- coding: utf-8 -*-
"""
Rebuild Vascular & Cystic Kidney Diseases Deck with High-Quality Medical Standards
learn-vaskuler-kistik-bobrek-hastaliklari (24 Slayt)
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

vaskuler_kistik_slides = [
    make_slide(
        1,
        "Vasküler Böbrek Hastalıkları: Genel Giriş ve Patofizyolojik Çerçeve",
        "Renal Kan Akımı, İntrasküler Basınç ve Damar Yatağı Hasarının Sonuçları",
        """Böbrekler kardiyak debinin yaklaşık %20-25'ini alan, vücudun en zengin vaskülarize organlarından biridir. Bu yüksek perfüzyon böbrek damar yatağını sistemik hemodinamik bozukluklara, endotel hasarına ve trombotik süreçlere karşı son derece duyarlı kılar.

**1. Vasküler Patolojilerin Sınıflanması:**
• **Büyük Damar Hastalıkları:** Renal arter darlığı (ateroskleroz, fibromusküler displazi), renal arter tromboembolisi, renal ven trombozu.
• **Arteriyol ve Küçük Damar Hastalıkları:** Benign nefroskleroz (hyalen arteriyoloskleroz), malign hipertansif nefroskleroz (hiperplastik arteriyoloskleroz ve fibrinoid nekroz).
• **Mikrovasküler Trombotik Süreçler:** Trombotik Mikroanjiyopatiler (TMA: HÜS, TTP).

**2. Klinik Sonuçlar:**
Vasküler lümen daralması renal iskemiye, tübüler atrofiye ve glomerüler skleroza yol açarak hipertansiyonun derinleşmesine ve ilerleyici kronik böbrek yetmezliğine neden olur.""",
        [
            {"type": "warning", "badge": "🔴 PATOFİZYOLOJİK DÖNGÜ", "text": "Renal vasküler daralma renin salgısını uyararak sistemik hipertansiyona; hipertansiyon ise böbrek damarlarında sklerozu artırarak böbrek yetmezliğine yol açan kısır bir döngü oluşturur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE SPOTU", "text": "Böbrek vasküler lezyonlarında afferent arteriyol lümen daralması tübüllerde iskemik atrofiye ve interstisyel fibrozise yol açar.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-001",
            "question": "Renal damar yatağının primer lezyonları sonucunda gelişen parankimal hasarda glomerüllerden önce etkilenen ve iskemik atrofiye en duyarlı renal kompartman hangisidir?",
            "options": [
                "A) Podosit slit diyaframları",
                "B) Proksimal tübüller ve Henle çıkan kalın kolu",
                "C) Bowman kapsülü parietali",
                "D) Mesane boynu",
                "E) Renal pelvis mukozası"
            ],
            "correctAnswer": 1,
            "explanation": "Tübül epitel hücreleri yüksek metabolik ve aktif transport gereksinimleri nedeniyle renal vasküler iskemiye en duyarlı yapılardır."
        }
    ),
    make_slide(
        2,
        "Benign Nefroskleroz: Hyalen Arteriyoloskleroz ve 'Deri Manzarası' Böbrek",
        "Kronik Esansiyel Hipertansiyon, Afferent Arteriyol Daralması ve İnce Granüler Yüzey",
        """Benign nefroskleroz, uzun süreli hafif veya orta dereceli esansiyel hipertansiyona ikincil olarak böbrek arter ve arteriyollerinde gelişen vasküler skleroz tablosudur. İleri yaş ve zenci ırkta sıklığı ve şiddeti belirgin artar.

**1. Mikroskobik Morfoloji (Hyalen Arteriyoloskleroz):**
• Karakteristik lezyon küçük arterler ve **afferent arteriyollerde** izlenir.
• Kronik yüksek intralüminal basınç endotel geçirgenliğini artırır; plazma proteinleri damar duvarına sızar ve düz kas hücreleri ekstraselüler matriks sentezler.
• Damar duvarında homojen, pembe, camsı bir kalınlaşma (**hyalen arteriyoloskleroz**) meydana gelir. Lümen ileri derecede daralır.
• İskemi sonucu glomerüllerde kapiller kollaps, GBM kalınlaşması ve global skleroz gelişir. Tübüller atrofiye uğrar, interstisyumda fibrozis oluşur.

**2. Makroskobik Görünüm:**
• Her iki böbrek simetrik olarak hafif veya orta derecede küçülmüştür.
• Böbreğin subkapsüler dış yüzeyi düzgünlüğünü kaybetmiş, kaba granüller yerine **ince granüler ('tabaklanmış deri' / leather grain manzarası)** bir görünüm almıştır. Kapsül parankimden zor soyulur.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Benign nefrosklerozda hyalen arteriyoloskleroz tipik olarak afferent arteriyolü tutar; böbrek yüzeyinde 'tabaklanmış deri' (leather-grain) benzeri ince granüler görünüm oluşturur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Benign hipertansiyonun böbrekteki temel histopatolojik karşılığı 'hyalen arteriyoloskleroz'dur; glomerüllerde iskemik kollaps ve interstisyel fibrozis eşlik eder.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-002",
            "question": "25 yıldır esansiyel hipertansiyonu olan 65 yaşındaki hastanın otopside böbrek yüzeyinde ince granüler 'tabaklanmış deri' (leather grain) görünümü izleniyor. Mikroskopta afferent arteriyollerde saptanması beklenen karakteristik vasküler lezyon hangisidir?",
            "options": [
                "A) Fibrinoid nekroz ve tromboz",
                "B) Hyalen arteriyoloskleroz",
                "C) Konsantrik soğan zarı hiperplazisi",
                "D) Nekrotizan vaskülit ve lökositoklazi",
                "E) Amiloid depolanması"
            ],
            "correctAnswer": 1,
            "explanation": "Kronik benign hipertansiyonda afferent arteriyol duvarında plazma proteini sızıntısı ve matriks artışıyla karakterize 'hyalen arteriyoloskleroz' gelişir."
        }
    ),
    make_slide(
        3,
        "Malign Hipertansiyon ve Malign Nefroskleroz: Fibrinoid Nekroz ve Soğan Zarı",
        "Diastolik >120 mmHg, Papilödem, Peteşiyel 'Pire Isırığı' (Flea-Bitten) Böbrek",
        """Malign hipertansiyon, kan basıncının aniden aşırı yükselmesi (genellikle sistolik >200 mmHg, diastolik >120 mmHg), bilateral papilödem, ensefalopati, kardiyak yetmezlik ve akut ilerleyici böbrek hasarı ile karakterize tıbbi bir acildir.

**1. Patogenez ve Hasar Döngüsü:**
Ani ve şiddetli kan basıncı artışı arteriyol endotelinde doğrudan yırtılmaya, plazma proteinlerinin ve fibrinojenin damar duvarına hücum etmesine ve trombosit agregasyonuna yol açar.

**2. Karakteristik Mikroskobik Lezyonlar:**
• **Fibrinoid Nekroz:** Küçük arter ve arteriyol duvarında lökosit infiltrasyonu ve eozinofilik aselüler fibrin birikimi izlenir; damar duvarı nekroze olur ve lümende mikrotrombuslar oluşur.
• **Hiperplastik Arteriyoloskleroz ('Soğan Zarı' / Onion-Skinning Manzarası):** İntralobüler arter ve arteriyollerde intimadaki düz kas hücreleri ve miyofibroblastlar konsantrik laminer tabakalar halinde çoğalarak damar lümenini neredeyse tamamen kapatır.

**3. Makroskobik Görünüm ('Pire Isırığı' / Flea-Bitten):**
Arteriyollerin yırtılması ve kapiller rüptürler sonucu böbrek subkapsüler korteks yüzeyinde nokta şeklinde çok sayıda kırmızı peteşiyel kanama odağı izlenir; bu görünüme **'pire ısırığı böbrek' (flea-bitten kidney)** denir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Böbrek korteksinde peteşiyel kanamalarla karakterize 'pire ısırığı' (flea-bitten) görünümü ve mikroskopta damarlarda 'soğan zarı' hiperplazisi Malign Nefroskleroz için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Malign nefrosklerozun iki histopatolojik imzası: Arteriyollerde 'fibrinoid nekroz' ve intimal proliferasyona bağlı konsantrik laminer 'soğan zarı' (hyperplastic arteriolosclerosis) lezyonudur.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-003",
            "question": "Kan basıncı 220/130 mmHg ölçülen, papilödem ve akut oligürik böbrek yetmezliği gelişen hastanın böbrek kesitinde kortekste 'pire ısırığı' tarzı peteşiyel kanamalar, biyopside ise arteriyollerde konsantrik laminer 'soğan zarı' lezyonu ve fibrinoid nekroz saptanıyor. Tanı nedir?",
            "options": [
                "A) Benign nefroskleroz",
                "B) Malign nefroskleroz",
                "C) Minimal değişiklik hastalığı",
                "D) Alport sendromu",
                "E) Akut interstisyel nefrit"
            ],
            "correctAnswer": 1,
            "explanation": "Diyastolik >120 mmHg, papilödem, pire ısırığı peteşileri, fibrinoid nekroz ve damarlarda konsantrik soğan zarı lezyonu Malign Nefrosklerozun klasik göstergeleridir."
        }
    ),
    make_slide(
        4,
        "Renal Arter Stenozu ve Renovasküler Hipertansiyon",
        "Ateroskleroz vs Fibromusküler Displazi, 'Goldblatt Böbreği' ve Asimetri",
        """Renal arter stenozu (RAS), böbrek ana arterinin daralması sonucu renal perfüzyonun düşmesi ve buna bağlı olarak gelişen renin-bağımlı sekonder hipertansiyondur (Renovasküler Hipertansiyon). Düzeltilebilir hipertansiyon nedenlerinin başında gelir.

**1. İki Ana Etyolojik Tip:**
• **Ateroskleroz (%70-80):** Yaşlı erkeklerde, sigara içenlerde ve yaygın damar sertliği olanlarda görülür. Darlık tipik olarak **renal arterin aortadan çıkış noktasında (ostiumda) veya proksimal üçte birinde** yerleşir.
• **Fibromusküler Displazi (FMD) (%20-30):** Genç kadınlarda (20-40 yaş) görülür. Arter duvarının medial tabakasında fibröz ve musküler displazi vardır. Darlık **renal arterin orta veya distal segmentlerini** tutar. Anjiyografide tipik **'tespih tanesi' (string of beads)** görünümü izlenir.

**2. Patofizyoloji ve Organ Asimetrisi ('Goldblatt Mekanizması'):**
• Darlık tarafındaki böbrek sürekli hipoperfüzyon algılar -> Jukstaglomerüler aparattan masif **renin salgılanır** -> Anjiyotensin II ve aldosteron yükselerek sistemik vazokonstriksiyon ve hipertansiyon yapar.
• **İki Böbreğin Çelişkili Morfolojisi:**
  - *Darlık Olan Böbrek:* İskemiye bağlı atrofiye uğrar, küçülür. Ancak stenoz yüksek sistemik basınca karşı bir kalkan oluşturduğu için bu böbrek **hipertansif arteriyolosklerozdan KORUNUR!**
  - *Karşı Sağlam Böbrek:* Aşırı yüksek sistemik basınca doğrudan maruz kalır; kompanse etmek için büyür (hipertrofi) ancak ağır **hipertansif nefroskleroz** geliştirir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK PARADOKS", "text": "Renal arter darlığında stenozlu böbrek iskemik atrofiye uğrar ama hipertansif damar hasarından korunur; karşı taraftaki sağlam böbrek ise yüksek basınca maruz kalarak ağır hipertansif arteriyoloskleroz geliştirir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Genç kadında dirençli hipertansiyon ve anjiyografide 'tespih tanesi' (string of beads) manzarası Fibromusküler Displazidir (media fibroplazisi).", "color": "sky"}
        ],
        {
            "id": "prac-vsk-004",
            "question": "28 yaşındaki bir kadında aniden başlayan dirençli hipertansiyon araştırılırken renal anjiyografide sağ renal arterin orta segmentinde tipik 'tespih tanesi' (string of beads) görünümü saptanıyor. En olası tanı hangisidir?",
            "options": [
                "A) Aterosklerotik renal arter stenozu",
                "B) Fibromusküler displazi",
                "C) Poliarteritis nodoza",
                "D) Renal ven trombozu",
                "E) Malign nefroskleroz"
            ],
            "correctAnswer": 1,
            "explanation": "Genç kadınlarda renal arterin orta-distalinde 'tespih tanesi' görüntüsü oluşturan darlık Fibromusküler Displaziye (özellikle medial fibroplazi) bağlıdır."
        }
    ),
    make_slide(
        5,
        "Trombotik Mikroanjiyopatiler (TMA): HÜS ve TTP Patogenezi",
        "Mikrovasküler Trombüsler, Mikroanjiyopatik Hemolitik Anemi ve Trombositopeni Triadı",
        """Trombotik Mikroanjiyopati (TMA), glomerül kapillerleri ve arteriyollerde yaygın endotel hasarı, mikrovasküler trombüs oluşumu, lümen daralması ve buna bağlı organ iskemisi ile karakterize bir klinikopatolojik sendromdur.

**1. Klinik ve Laboratuvar Kardinal Triadı:**
1. **Mikroanjiyopatik Hemolitik Anemi (MAHA):** Trombüslerle daralan kapillerlerden geçerken parçalanan eritrositler -> Periferik yaymada **şistositler (miğfer hücreleri)**, yüksek LDH, indirekt bilirubin artışı ve düşük haptoglobulin.
2. **Tüketim Trombositopenisi:** Trombüs oluşumunda tüketilen trombositler sonucu trombositopeni.
3. **Akut İlerleyici Böbrek Hasarı / Nörolojik Bulgular.**

**2. İki Ana Antite:**
• **Hemolitik Üremik Sendrom (HÜS):**
  - *Tipik HÜS (Shiga Toksini İlişkili - STEC-HÜS):* Çocuklarda çiğ et veya kontamine gıdalarla bulaşan **E. coli O157:H7** veya *Shigella dysenteriae* suşlarının salgıladığı **Shiga benzeri toksin (Stx)** nedeniyledir. Kanlı ishal sonrası başlar; endotel Gb3 reseptörüne bağlanarak endotel nekrozu ve glomerüler mikrotromboz yapar. Böbrek tutulumu ön plandadır.
  - *Atipik HÜS (aHÜS):* Alternatif kompleman regülatör proteinlerinin (Faktör H, Faktör I, CD46) genetik mutasyonlarına bağlıdır; kompleman sürekli aşırı aktif kalarak endoteli tahrip eder. Eculizumab (anti-C5) tedavide çığır açmıştır.
• **Trombotik Trombositopenik Purpura (TTP):**
  - von Willebrand faktörünü (vWF) parçalayan plazma metalloproteazı olan **ADAMTS13 enzim eksikliği** veya otoantikorları sonucu gelişir. Dev vWF multimerleri spontan trombosit agregasyonu yapar. Nörolojik semptomlar ve ateş baskındır.""",
        [
            {"type": "warning", "badge": "🔴 HEMATOLOJİK İMZA", "text": "TMA'da periferik yaymada parçalanmış eritrositler olan 'Şistositler' (kask/miğfer hücreleri) tanı koydurucudur; koagülasyon testleri (PT, aPTT) DİK'ten farklı olarak NORMALDİR.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Tipik çocukluk çağı HÜS'ü Shiga toksini üreten E. coli O157:H7 kanlı ishali sonrası gelişir; Atipik HÜS alternatif kompleman (Faktör H) defektine bağlıdır; TTP ise ADAMTS13 eksikliğidir.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-005",
            "question": "Kanlı ishal atağından 5 gün sonra solukluk, anüri ve hematüri gelişen 4 yaşındaki bir çocuğun periferik yaymasında çok sayıda şistosit (miğfer hücresi) ve trombositopeni saptanıyor. Bu tabloda endotel hasarını başlatan en olası patojen ve toksin hangisidir?",
            "options": [
                "A) Clostridium difficile enterotoksini",
                "B) Shiga toksini üreten Escherichia coli O157:H7",
                "C) Salmonella typhi endotoksini",
                "D) Vibrio cholerae kolera toksini",
                "E) Staphylococcus aureus enterotoksin B"
            ],
            "correctAnswer": 1,
            "explanation": "Kanlı ishal sonrası gelişen tipik HÜS tablosunun en sık nedeni E. coli O157:H7 suşunun salgıladığı Shiga toksinidir (STEC)."
        }
    ),
    make_slide(
        6,
        "Kistik Böbrek Hastalıkları: Genel Giriş ve Sınıflama",
        "Kortikal, Medüller, Genetik ve Edinsel Kistlerin Klinik Yelpazesi",
        """Kistik böbrek hastalıkları, renal parankimde sıvı dolu epitelyal boşlukların gelişmesiyle karakterize, genetik, gelişimsel veya edinsel kökenli geniş bir yelpazedir.

**1. Kistik Hastalıkların Klinik Önemi:**
• Genetik kistik hastalıklar (özellikle ADPKD ve Nefronofitizis) çocukluk ve erişkin çağında son dönem böbrek yetmezliğinin en sık kalıtsal nedenleridir.
• Kistler bazen renal hücreli karsinomla karışabilir veya maligniteye zemin hazırlayabilir (diyaliz ilişkili kistler gibi).

**2. Başlıca Sınıflama:**
• **Basit Renal Kistler:** En sık görülen edinsel kistler; yaşla sıklığı artar, genellikle benign ve asemptomatiktir.
• **Otozomal Dominant Polikistik Böbrek Hastalığı (ADPKD):** Erişkinde bilateral dev kistler, hipertansiyon, intrakraniyal anevrizmalar.
• **Otozomal Resesif Polikistik Böbrek Hastalığı (ARPKD):** İnfantil/yenidoğan, fuziform toplayıcı kanal dilatasyonları, konjenital hepatik fibrozis.
• **Medüller Kistik Hastalıklar:** Medüller sünger böbrek, Nefronofitizis / Medüller Kistik Böbrek Hastalığı kompleksi.
• **Edinsel (Diyaliz İlişkili) Kistik Hastalık:** Kronik diyaliz hastalarında gelişen kistler ve artmış RCC riski.""",
        [
            {"type": "clinical", "badge": "🔴 SINIFLAMA KURALI", "text": "Erişkinde bilateral devasa kistler ADPKD; yenidoğanda bilateral simetrik süngerimsi fuziform kistler + karaciğer fibrozisi ARPKD'dir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Diyaliz ilişkili edinsel kistik böbrek hastalığında renal hücreli karsinom (özellikle papiller varyant) gelişme riski normal topluma göre belirgin artmıştır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-006",
            "question": "Aşağıdaki kistik böbrek hastalıklarından hangisi uzun süreli hemodiyaliz tedavisi gören kronik son dönem böbrek yetmezliği hastalarında sekonder olarak gelişir ve renal karsinom riskini artırır?",
            "options": [
                "A) Otozomal dominant polikistik böbrek hastalığı",
                "B) Medüller sünger böbrek",
                "C) Edinsel (diyaliz ilişkili) kistik böbrek hastalığı",
                "D) Nefronofitizis",
                "E) Basit kortikal kist"
            ],
            "correctAnswer": 2,
            "explanation": "Yıllarca hemodiyaliz alan son dönem böbrek hastalarında edinsel kistler gelişir ve bu kistlerin epitelinden RCC gelişme riski yükselir."
        }
    ),
    make_slide(
        7,
        "Otozomal Dominant Polikistik Böbrek Hastalığı (ADPKD): Genetik ve Patogenez",
        "PKD1 (Polisistin-1, 16p13) ve PKD2 (Polisistin-2, 4q21), Primer Siliya Disfonksiyonu",
        """ADPKD, toplumda yaklaşık 1/400 ila 1/1000 sıklıkla görülen, her iki böbrekte sayısız kist gelişimi ve ilerleyici böbrek yetmezliği ile karakterize en yaygın kalıtsal monogenik hastalıklardan biridir.

**1. Genetik Mutasyonlar:**
• **PKD1 Geni (%85):** Kromozom **16p13.3** üzerinde yer alır ve **Polisistin-1** proteinini kodlar. PKD1 mutasyonları çok daha agresif seyreder; son dönem böbrek yetmezliği ortalama 50'li yaşların başında gelişir.
• **PKD2 Geni (%15):** Kromozom **4q21** üzerinde yer alır ve **Polisistin-2** proteinini kodlar. Klinik seyir daha hafiftir; son dönem böbrek yetmezliği ortalama 70'li yaşlarda ortaya çıkar.

**2. Patogenez ve Siliya Hipotezi:**
• Polisistin-1 ve Polisistin-2 proteinleri tubulus epitel hücrelerinin yüzeyindeki **primer siliyalarda** (mekanosensör organel) bir kompleks oluşturur.
• İdrar akımının siliyayı bükmesi normalde hücre içine kalsiyum girişini uyarır. Polisistin kompleksinin bozulması intraselüler kalsiyumu düşürür, intraselüler cAMP düzeyini artırır.
• Aşırı cAMP; tübül epitel hücrelerinde kontrolsüz proliferasyona ve lümene aşırı klor/sıvı sekresyonuna yol açarak kistlerin genişlemesini sağlar.
• **Kist Kökeni:** Nefronun her segmentinden (Bowman kapsülü, proksimal tübül, Henle, distal tübül, toplayıcı kanal) kist gelişebilir.""",
        [
            {"type": "warning", "badge": "🔴 GENETİK KODLAMA", "text": "ADPKD olgularının %85'inden sorumlu gen PKD1 (Kromozom 16 - Polisistin-1); %15'inden sorumlu gen PKD2'dir (Kromozom 4 - Polisistin-2).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Polisistin proteinleri primer siliyada yer alır; ADPKD patogenezindeki temel moleküler anormallik primer siliya disfonksiyonu ve intraselüler cAMP artışıdır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-007",
            "question": "Otozomal Dominant Polikistik Böbrek Hastalığının (ADPKD) en sık görülen ve son dönem böbrek yetmezliğine daha erken yaşta ilerleyen formundan sorumlu gen ve kromozom lokalizasyonu hangisidir?",
            "options": [
                "A) PKHD1 — Kromozom 6",
                "B) PKD1 — Kromozom 16",
                "C) PKD2 — Kromozom 4",
                "D) VHL — Kromozom 3",
                "E) WT1 — Kromozom 11"
            ],
            "correctAnswer": 1,
            "explanation": "ADPKD olgularının %85'inden sorumlu olan ve erken böbrek yetmezliğine yol açan mutasyon kromozom 16'daki PKD1 genindedir (Polisistin-1)."
        }
    ),
    make_slide(
        8,
        "ADPKD Morfolojisi: Devasa Böbrekler ve Kistlerin Yayılımı",
        "Kilolarca Ağırlıkta Böbrekler, Kist İçi Kanamalar ve Parankim Bası Atrofisi",
        """ADPKD'de böbreklerin makroskobik görünümü patolojinin en çarpıcı manzaralarından biridir.

**1. Makroskobik Morfoloji:**
• Her iki böbrek bilateral olarak devasa boyutlara ulaşır. Normalde 150 gram olan bir böbreğin ağırlığı **1 ila 4 kilograma** kadar çıkabilir; karın boşluğunu tamamen doldurabilir.
• Dış yüzeyden ve kesit yüzeyinden bakıldığında böbrek adeta birbirine bitişik yüzlerce kist yığını halindedir; normal parankim dokusu kistler arasında bası atrofisine uğramış ince fibröz bantlar şeklinde kalmıştır.
• Kistlerin çapı birkaç milimetreden birkaç santimetreye kadar değişir.
• **Kist İçeriği:** Kist sıvısı berrak sarımtırak olabileceği gibi, kist içi kanama veya enfeksiyon nedeniyle çikolata renginde, bulanık, pürülan veya hemorajik olabilir.

**2. Mikroskobik Bulgular:**
• Kistlerin iç yüzeyi tek katlı basık veya kübik tübüler epitel ile döşelidir.
• Kistler arasındaki sağlam kalan glomerül ve tübüllerde bası atrofisi, interstisyel fibrozis ve sekonder hipertansiyona bağlı arteriyoloskleroz izlenir.""",
        [
            {"type": "warning", "badge": "🔴 MAKROSKOBİK ÖZELLİK", "text": "ADPKD'de böbrekler bilateral dev boyutlara ulaşır; kist içi kanamalar ani yan ağrısı ve makroskopik hematürinin en sık nedenidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "ADPKD'de kistler nefronun HERHANGİ BİR segmentinden gelişebilir (proksimal, distal, toplayıcı vb.); bu yönüyle toplayıcı kanala sınırlı ARPKD'den ayrılır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-008",
            "question": "Otopside her iki böbreğin 3'er kilogram ağırlığa ulaştığı, tüm nefron segmentlerinden köken alan sayısız kistle kaplı olduğu ve kistler arasında parankimin bası atrofisine uğradığı saptanıyor. Tanı nedir?",
            "options": [
                "A) Medüller sünger böbrek",
                "B) Otozomal dominant polikistik böbrek hastalığı",
                "C) Otozomal resesif polikistik böbrek hastalığı",
                "D) Nefronofitizis",
                "E) Bilateral renal onkositoma"
            ],
            "correctAnswer": 1,
            "explanation": "Bilateral kilogramlarca ağırlığa ulaşan devasa kistik böbrekler Otozomal Dominant Polikistik Böbrek Hastalığının (ADPKD) klasik makroskobik görünümüdür."
        }
    ),
    make_slide(
        9,
        "ADPKD Ekstrarenal Bulguları: Anevrizmalar ve Kistler",
        "Willis Poligonu Berry Anevrizmaları, Polikistik Karaciğer ve Mitral Kapak Prolapsusu",
        """ADPKD sadece böbreklerle sınırlı kalmayan, yaygın ekstrarenal organ tutulumları ve vasküler anormalliklerle seyreden sistemik bir hastalıktır.

**1. İntrakraniyal Berry (Sakküler) Anevrizmaları:**
• Hastaların **%10-20'sinde** beyin tabanındaki Willis poligonu damarlarında (özellikle anterior komünikan arter) **sakküler (berry) anevrizmalar** bulunur. Ailede anevrizma öyküsü olanlarda risk %20-30'a çıkar.
• Anevrizma rüptürü ölümcül **Subaraknoid Kanamaya (SAK)** yol açar; ADPKD hastalarında böbrek dışı mortalitenin en sık nedenlerinden biridir.

**2. Polikistik Karaciğer Hastalığı:**
• En sık ekstrarenal kist lokalizasyonudur; hastaların **%40-50'sinde** karaciğerde safra kanalı kaynaklı epitelyal kistler izlenir. Karaciğer fonksiyon testleri genellikle normal kalır; kitle etkisi yapabilir.

**3. Kardiyovasküler ve Diğer Tutulumlar:**
• **Mitral Kapak Prolapsusu (MVP):** Hastaların %20-25'inde izlenir; miksomatöz kapak dejenerasyonu. Aort kökü dilatasyonu ve diseksiyon riski.
• **Kolon Divertikülleri:** Kolon duvar bağ dokusu zayıflığına bağlı asemptomatik veya rüptüre divertikülozis.
• Pankreas, dalak ve seminal vezikül kistleri.""",
        [
            {"type": "warning", "badge": "🔴 HAYATİ TEHLİKE", "text": "ADPKD hastasında ani başlayan şiddetli 'hayatımın en kötü baş ağrısı' Willis poligonundaki Berry anevrizması rüptürünü ve Subaraknoid Kanamayı (SAK) işaret eder!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "ADPKD'nin en sık ekstrarenal tutulumu karaciğer kistleri (%40); en ölümcül ekstrarenal komplikasyonu ise intrakraniyal berry anevrizması rüptürüdür.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-009",
            "question": "Bilateral polikistik böbrek hastalığı tanısıyla izlenen 42 yaşındaki bir hastada ani gelişen senkop ve şiddetli ense sertliği ile seyreden baş ağrısı tablosunda en olası serebrovasküler komplikasyon hangisidir?",
            "options": [
                "A) İntraserebral hematom",
                "B) Willis poligonu Berry anevrizma rüptürüne bağlı subaraknoid kanama",
                "C) Karotis arter diseksiyonu",
                "D) Sagittal sinüs trombozu",
                "E) Epidural hematom"
            ],
            "correctAnswer": 1,
            "explanation": "ADPKD'li hastaların %10-20'sinde intrakraniyal berry anevrizması bulunur ve rüptürü klasik olarak subaraknoid kanama tablosu oluşturur."
        }
    ),
    make_slide(
        10,
        "Otozomal Resesif Polikistik Böbrek Hastalığı (ARPKD): Genetik ve Patogenez",
        "PKHD1 Geni (Fibrosistin, 6p12), İnfantil Form ve Ektazik Toplayıcı Kanallar",
        """ARPKD (İnfantil Polikistik Böbrek Hastalığı), çocukluk çağında görülen, otozomal resesif kalıtımlı, bilateral simetrik böbrek tutulumu ve zorunlu karaciğer fibrozu ile karakterize nadir fakat ağır bir hastalıktır (1/20.000 doğum).

**1. Genetik Mutasyon:**
• Kromozom **6p12** üzerinde yer alan **PKHD1** genindeki mutasyonlardan kaynaklanır.
• Bu gen **Fibrosistin** (veya Poliduktin) proteinini kodlar. Fibrosistin renal toplayıcı kanal ve hepatik safra duktus epitellerinin primer siliyasında yer alır.

**2. Kistlerin Karakteristik Kökeni:**
• ADPKD'nin aksine kistler tüm nefrona yayılmaz; **sadece ve sadece medüller ve kortikal TOPLAYICI KANALLARIN (collecting ducts) dilatasyonundan** kaynaklanır.
• İdrar üretiminin intrauterin dönemde bozulması ağır **oligohidramniyos** tablosuna yol açar.
• **Potter Sekansı:** Oligohidramniyos nedeniyle uterus fetus üzerine bası yapar; pulmoner hipoplazi (en sık ölüm nedeni), tipik basık Potter yüzü (düzleşmiş burun, mikrognati, düşük kulaklar) ve ekstremite deformiteleri gelişir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK AYRIM", "text": "ADPKD kistleri tüm nefron segmentlerinden gelişirken; ARPKD kistleri YALNIZCA toplayıcı kanalların ektazisinden köken alır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS SPOTU", "text": "ARPKD'den sorumlu gen PKHD1 olup kodladığı protein Fibrosistindir; yenidoğanda en sık ölüm nedeni oligohidramniyosa bağlı gelişen Pulmoner Hipoplazidir.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-010",
            "question": "Otozomal resesif polikistik böbrek hastalığında (ARPKD) kistik dilatasyonlar nefronun hangi anatomik segmentine sınırlıdır?",
            "options": [
                "A) Proksimal konvolüt tübüller",
                "B) Henle kulpunun inen ince kolu",
                "C) Toplayıcı kanallar (collecting ducts)",
                "D) Yalnızca Bowman kapsülü",
                "E) Afferent arteriyoller"
            ],
            "correctAnswer": 2,
            "explanation": "ARPKD'de kistler seçici olarak kortikal ve medüller toplayıcı kanalların fuziform dilatasyonundan meydana gelir."
        }
    ),
    make_slide(
        11,
        "ARPKD Morfolojisi ve Konjenital Hepatik Fibrozis Birlikteliği",
        "Korteksten Medullaya Dik Fuziform Kistler, 'Süngerimsi Kesit' ve Safra Kanalı Disgenezi",
        """ARPKD'nin makroskobik kesiti ve karaciğer patolojisi tanı için belirleyicidir.

**1. Makroskobik ve Mikroskobik Görünüm:**
• Böbrekler bilateral simetrik olarak ileri derecede büyümüştür ancak fetal lobülasyon hatlarını korur. Dış yüzey genellikle düzgündür (ADPKD gibi kaba yumrulu değildir).
• **Kortikomedüller Kesit Yüzeyi:** Böbrek kesildiğinde korteksten başlayıp medullaya ve papillaya dik uzanan **radyal yerleşimli, fuziform veya silindirik ektazik kanallar** izlenir. Kesit yüzeyi sünger veya delikli peynir manzarası sergiler.
• Mikroskopta bu kanalların toplayıcı kanal epiteli ile döşeli olduğu görülür.

**2. Karaciğer Tutulumu — Konjenital Hepatik Fibrozis:**
• ARPKD'li tüm hastalarda karaciğer tutulumu **ZORUNLUDUR**.
• Portal alanlarda belirgin genişleme, yoğun safra duktusu proliferasyonu (duktal tabak malformasyonu) ve kalın kollajen bantları (**konjenital hepatik fibrozis**) izlenir.
• İleri çocukluk çağında hayatta kalan çocuklarda karaciğer sirozuna benzer şekilde **portal hipertansiyon, splenomegali ve özofagus varis kanamaları** en önemli klinik problem haline gelir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BİRLİKTELİK", "text": "Bilateral simetrik radyal fuziform böbrek kistleri ile Konjenital Hepatik Fibrozis birlikteliği ARPKD için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "ARPKD'de bebeklik dönemini atlatan çocuklarda en önemli klinik morbidite konjenital hepatik fibrozise bağlı portal hipertansiyon ve özofagus varis kanamalarıdır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-011",
            "question": "Yenidoğan döneminde bilateral simetrik büyümüş böbrek kesitinde korteksten medullaya dik fuziform silindirik kistler izlenen ve karaciğer biyopsisinde safra duktus proliferasyonu ile konjenital hepatik fibrozis saptanan olguda tanı nedir?",
            "options": [
                "A) Otozomal dominant polikistik böbrek",
                "B) Otozomal resesif polikistik böbrek (ARPKD)",
                "C) Medüller sünger böbrek",
                "D) Alport sendromu",
                "E) Renal hücreli karsinom"
            ],
            "correctAnswer": 1,
            "explanation": "Korteksten medullaya dik fuziform kistler ve karaciğerde konjenital hepatik fibrozis ARPKD'nin patognomonik tablosudur."
        }
    ),
    make_slide(
        12,
        "ADPKD vs ARPKD: Karşılaştırmalı Büyük Klinikopatolojik Tablo",
        "Genetik, Kalıtım, Kist Dağılımı ve Ekstrarenal Tutulumların Karşılaştırılması",
        """Kalıtsal polikistik böbrek hastalıklarının temel patolojik karşılaştırma matrisi:

| Özellik | Otozomal Dominant (ADPKD) | Otozomal Resesif (ARPKD) |
| :--- | :--- | :--- |
| **Kalıtım Şekli** | Otozomal Dominant (%100 penetrans) | Otozomal Resesif |
| **Sorumlu Genler** | *PKD1* (16p13, %85), *PKD2* (4q21, %15) | *PKHD1* (6p12) |
| **Kodlanan Protein** | Polisistin-1, Polisistin-2 | Fibrosistin (Poliduktin) |
| **Başvuru Yaşı** | Erişkin (30-50 yaş) | Yenidoğan, infant veya erken çocukluk |
| **Böbrek Boyutu** | Bilateral asimetrik devasa (kilolarca) | Bilateral simetrik büyümüş, düzgün yüzeyli |
| **Kistlerin Kökeni** | **Tüm nefron segmentleri** | **Yalnızca toplayıcı kanallar** |
| **Kist Morfolojisi** | Yuvarlak, değişken çaplı kist yığını | Radyal fuziform, silindirik ektazik kanallar |
| **Karaciğer Tutulumu** | Epitelyal kistler (%40, fibrozis yok) | **Konjenital Hepatik Fibrozis** (zorunlu) |
| **Serebral Lezyon** | **Berry anevrizmaları** (SAK riski) | Anevrizma görülmez |
| **Ölüm Nedeni** | Üremi, koroner arter hastalığı, SAK | Pulmoner hipoplazi (bebekte), Portal HT (çocukta) |""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK AYIRICI TANI", "text": "ADPKD karaciğerde kist yapar (fibrozis yapmaz), beyinde berry anevrizması yapar; ARPKD ise karaciğerde doğrudan konjenital hepatik fibrozis ve portal hipertansiyon yapar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV TABLOSU", "text": "Bu tablo komite ve TUS sınavlarında polikistik böbrek hastalıkları sorularının doğrudan çözüm anahtarıdır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-012",
            "question": "Aşağıdakilerden hangisi Otozomal Dominant Polikistik Böbrek Hastalığını (ADPKD) Otozomal Resesif formdan (ARPKD) ayıran temel özelliklerden biridir?",
            "options": [
                "A) Kistlerin sadece toplayıcı kanallarla sınırlı olması",
                "B) Karaciğerde konjenital hepatik fibrozis bulunması",
                "C) İntrakraniyal Willis poligonunda sakküler (Berry) anevrizmaların eşlik edebilmesi",
                "D) Doğumda pulmoner hipoplaziye yol açması",
                "E) Kromozom 6p mutasyonuna bağlı olması"
            ],
            "correctAnswer": 2,
            "explanation": "Berry anevrizmaları ve subaraknoid kanama riski sadece ADPKD'ye özgüdür; ARPKD'de anevrizma izlenmez."
        }
    ),
    make_slide(
        13,
        "Medüller Sünger Böbrek ve Medüller Kistik Böbrek Hastalıkları",
        "Papiller Duktus Ektazisi vs Nefronofitizis (NPHP) ve Kortikomedüller Kistler",
        """Böbrek medullasını tutan kistik hastalıklar prognoz ve patogenez açısından birbirine zıt iki gruptur.

**1. Medüller Sünger Böbrek (Medullary Sponge Kidney):**
• Genellikle sporadik ve edinsel kabul edilen, asemptomatik benign bir tablodur.
• Renal piramitlerin içindeki toplayıcı kanallarda (Bellini kanalları) kistik dilatasyonlar mevcuttur.
• Kistler içinde idrar stazına bağlı olarak kalsiyum okzalat/fosfat taşları ve rekürren enfeksiyonlar gelişir.
• **En Önemli Klinik Özellik:** Böbrek fonksiyonları tamamen korunur; son dönem böbrek yetmezliğine **asla ilerlemez!**

**2. Nefronofitizis ve Medüller Kistik Böbrek Hastalığı (ADTKD) Kompleksi:**
• **Nefronofitizis (NPHP):** Otozomal resesif kalıtılır (NPHP1-11 gen mutasyonları). Çocukluk ve adölesan çağında **son dönem böbrek yetmezliğinin en sık genetik nedenidir**. Ekstrarenal bulgular: Retinitisf pigmentoza (Senior-Løken sendromu), serebellar ataksi (Joubert sendromu).
• **Otozomal Dominant Tübülointerstisyel Böbrek Hastalığı (ADTKD / MCKD):** Otozomal dominant kalıtılır (*UMOD* veya *MUC1* gen mutasyonları); erişkinde böbrek yetmezliği yapar.
• **Ortak Morfoloji:** Böbrekler ADPKD'nin aksine **küçülmüş ve büzüşmüştür**. Kistler kortekste değil, sadece **kortikomedüller bileşkede** yerleşen küçük (0.1 - 1 cm) kistlerdir. Şiddetli tübülointerstisyel fibrozis ve tübül bazal membran kalınlaşması vardır.""",
        [
            {"type": "warning", "badge": "🔴 MORFOLOJİK KURAL", "text": "Polikistik böbrekte böbrekler devasa iken; Nefronofitizis / Medüller Kistik Böbrek Hastalığında böbrekler büzüşmüş ve küçüktür; kistler kortikomedüller bileşkede sınırlıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Çocukluk çağında kronik böbrek yetmezliğinin en sık kalıtsal nedeni Nefronofitizistir; medüller sünger böbrek ise benign seyreder ve böbrek yetmezliği yapmaz.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-013",
            "question": "12 yaşındaki bir çocukta poliüri, büyüme geriliği ve ilerleyici böbrek yetmezliği saptanıyor. Ultrasonografide her iki böbreğin küçülmüş olduğu ve sadece kortikomedüller bileşkede küçük kistlerin yer aldığı izleniyor. Çocukluk çağında bu tablonun en sık genetik nedeni hangisidir?",
            "options": [
                "A) Medüller sünger böbrek",
                "B) Nefronofitizis (NPHP)",
                "C) Otozomal dominant polikistik böbrek",
                "D) Von Hippel-Lindau sendromu",
                "E) Basit kortikal kist"
            ],
            "correctAnswer": 1,
            "explanation": "Çocuklarda küçülmüş böbrekler, kortikomedüller kistler ve erken böbrek yetmezliği ile seyreden en sık genetik antite Nefronofitizistir."
        }
    ),
    make_slide(
        14,
        "Basit Böbrek Kistleri ve Bosniak Radyolojik Sınıflaması",
        "Kortikal Şeffaf Kistler, İnce Duvar ve Malignite Risk Kriterleri",
        """Basit böbrek kistleri, insan böbreğinde en sık saptanan edinsel kistik lezyonlardır. 50 yaş üzerindeki bireylerin yaklaşık %50'sinde en az bir adet basit kist bulunur; yaşla sıklığı artar.

**1. Morfolojik Özellikler:**
• Genellikle tek taraflı, kortekste yerleşen, tek veya birkaç adet kisttir. Çapları 1-5 cm arasındadır.
• Kist duvarı son derece ince, pürüzsüz ve yarı şeffaftır. İçerisinde berrak seröz saman sarısı bir sıvı bulunur.
• Mikroskopta tek katlı yassı veya kübik epitel ile döşelidir.

**2. Bosniak Kist Sınıflaması (Malignite Ayrımı):**
• **Kategori I:** Basit kist; ince saç teli gibi duvar, kalsifikasyon yok, septa yok, kontrast tutulumu yok (%0 kanser riski -> Takip gereksiz).
• **Kategori II:** Minimal komplike kist; ince septalar, duvarda ince kalsifikasyonlar, kontrast tutulumu yok (%0 kanser riski -> Benign).
• **Kategori IIF:** Takip gerektiren kist (F = Follow-up); kalın kalsifikasyon, çok sayıda ince septa (%5 kanser riski -> Radyolojik takip).
• **Kategori III:** Şüpheli kist; düzensiz kalın septalar, kontrast tutan kalın duvarlar (%50 kanser riski -> Cerrahi rezeksiyon).
• **Kategori IV:** Malign kist; kist duvarında kontrast tutan solid nodüler komponentler (%90-100 kistik Renal Hücreli Karsinom -> Parsiyel/Radikal Nefrektomi).""",
        [
            {"type": "clinical", "badge": "🔴 RADYOLOJİK KURAL", "text": "Bosniak Kategori I ve II kistler tamamen benigndir; Kategori III ve IV kistler ise kistik renal hücreli karsinom şüphesiyle cerrahi olarak çıkarılmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Basit böbrek kistleri yaşla sıklığı artan edinsel lezyonlardır; kist içinde kontrast tutan solid nodül varlığı Bosniak IV (kistik karsinom) kriteridir.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-014",
            "question": "Rutin batın ultrasonografisinde sol böbrek korteksinde 3 cm çapında, ince duvarlı, içerisinde septa veya solid nodül içermeyen, arkasında akustik güçlenme oluşturan anekoik kistik lezyon saptanan 55 yaşındaki asemptomatik hastada yaklaşım ne olmalıdır?",
            "options": [
                "A) Acil radikal nefrektomi",
                "B) Lezyonun basit kist (Bosniak I) kabul edilerek ek tetkik ve tedaviye gerek duyulmaması",
                "C) Böbrek biyopsisi ile kist duvarının örneklenmesi",
                "D) Diyaliz hazırlığına başlanması",
                "E) Yüksek doz kemoterapi verilmesi"
            ],
            "correctAnswer": 1,
            "explanation": "İnce duvarlı, içeriksiz ve akustik güçlenme veren anekoik kistler klasik benign basit böbrek kistleridir (Bosniak I); ek tedavi veya cerrahi gerektirmez."
        }
    ),
    make_slide(
        15,
        "Renal İnfarktüs ve Ateroembolik Böbrek Hastalığı",
        "Beyaz (Soluk) Kama Şekilli İnfarkt ve Kolesterol Kleftleri (İğsi Yarıklar)",
        """Böbrek arterleri uç arterler (end-artery) olduğu için kan akımının kesilmesi kollateral dolaşımın bulunmaması nedeniyle doğrudan koagülasyon nekrozuna (iskemik infarktüs) yol açar.

**1. Renal İnfarktüs:**
• **Etyoloji:** En sık sol atriyal veya ventriküler mural tromboemboliler (Atriyal fibrilasyon, miyokard infarktüsü sonrası) ve infektif endokardit vejetasyonlarıdır.
• **Makroskopi:** Tipik olarak **soluk, beyaz-gri renkli kama şeklinde (wedge-shaped)** infarkt alanıdır. Kamanın tabanı böbreğin dış korteks kapsülüne oturur; tepesi ise tıkalı damarın bulunduğu medullaya yöneliktir. Etrafı hiperemik kırmızı bir zonla çevrilidir.
• **Mikroskopi:** Klasik 'hayalet hücre' (ghost cells) görünümü veren **koagülasyon nekrozu**. Subkapsüler alandaki glomerüller kapsüler damarlardan beslendiği için korunur.

**2. Ateroembolik Renal Hastalık (Kolesterol Embolisi):**
• Karın aortasındaki aterosklerotik plakların yırtılması (anjiyografi, koroner anjiyo veya vasküler cerrahi sonrasında) sonucu kolesterol kristallerinin böbrek arteriyollerini tıkamasıdır.
• **Patognomonik Mikroskopi:** Küçük interlobüler arter ve arteriyol lümenlerinde doku takibi sırasında eriyerek yerinde boşluk bırakan **bikonveks iğsi kolesterol yarıkları (cholesterol clefts)** ve çevresinde yabancı cisim dev hücre reaksiyonu izlenir.
• Hastada livedo retikularis, periferik eozinofili ve akut böbrek yetmezliği gelişir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Anjiyografi sonrası gelişen böbrek yetmezliğinde arter lümenlerinde 'iğsi kolesterol kleftleri' (cholesterol clefts) görülmesi Ateroembolik Böbrek Hastalığı için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Böbrek infarktları uç arter dolaşımı nedeniyle soluk (beyaz) ve kama şekillidir; tabanı kapsüle, tepesi medullaya bakar.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-015",
            "question": "Koroner anjiyografi işleminden 2 gün sonra ayak parmaklarında morarma (mavi parmak sendromu), periferik kanda eozinofili ve akut böbrek yetmezliği gelişen hastanın böbrek biyopsisinde interlobüler arter lümenlerinde ne görülmesi beklenir?",
            "options": [
                "A) Bakteriyel vejetasyon tıkaçları",
                "B) Bikonveks iğsi kolesterol yarıkları (kleftleri) ve dev hücre reaksiyonu",
                "C) Amiloid fibrilleri",
                "D) Konsantrik soğan zarı hiperplazisi",
                "E) Fibrin başlığı lezyonları"
            ],
            "correctAnswer": 1,
            "explanation": "Aortik girişimler sonrası ateroembolik böbrek hastalığı gelişir; küçük arteriyollerde bikonveks kolesterol kristalleri yarıkları (cholesterol clefts) patognomoniktir."
        }
    ),
    make_slide(
        16,
        "Renal Kortikal Nekroz: Şok ve Obstetrik Felaketlerin Ağır Sonucu",
        "Bilateral Diffüz Kortikal İskemi, Abruptio Placentae ve DİK Zemininde Gelişim",
        """Diffüz Renal Kortikal Nekroz, böbrek korteksinin neredeyse tamamının bilateral ve simetrik olarak iskemik nekroza uğradığı, katastrofik ve geri dönüşsüz bir akut böbrek yetmezliği formudur.

**1. Etyolojik Nedenler:**
• Olguların **%50'sinden fazlası majör obstetrik komplikasyonlar** zemininde gelişir:
  - **Ablasyo Plasenta (Abruptio placentae - plasentanın erken ayrılması):** 1 numaralı neden.
  - Ağır preeklampsi / eklampsi,
  - Septik abortus ve amniyon sıvı embolisi.
• Non-obstetrik nedenler: Ağır septik şok, masif travma, yaygın Dissemine İntravasküler Koagülasyon (DİK), yılan sokması.

**2. Patoloji ve Morfoloji:**
• Yaygın endotel hasarı ve masif mikrovasküler vazokonstriksiyon/tromboz korteks kan akımını sıfırlar.
• **Makroskopi:** Her iki böbrekte korteks tamamen sarı-beyaz, yumuşamış, nekrotik bir kitle halindedir; medullaya kadar keskin bir sınırla ayrılır. Medulla ve subkapsüler ince bir korteks şeridi göreceli olarak korunabilir.
• **Mikroskopi:** Korteksteki tüm glomerül, tübül ve damarlar yaygın iskemik koagülasyon nekrozuna uğramıştır; glomerüllerde yaygın mikrotrombuslar izlenir.
• **Prognoz:** Geri dönüşümsüzdür; hastalar kalıcı diyaliz veya böbrek nakline bağımlı kalır.""",
        [
            {"type": "warning", "badge": "🔴 OBSTETRİK FELAKET", "text": "Ablasyo plasenta ve ağır obstetrik kanamalar sonrası ani anüri gelişen kadın hastada en korkulan ve geri dönüşsüz tablo Bilateral Renal Kortikal Nekrozdur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Renal kortikal nekrozda nekroz sadece korteksle sınırlıdır; medulla korunur. Olguların yarıdan fazlası ablasyo plasenta gibi gebelik komplikasyonlarına bağlıdır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-016",
            "question": "Ablasyo plasenta nedeniyle acil sezaryene alınan ve masif kanama geçiren 34 yaşındaki kadında doğum sonrası tam anüri gelişiyor. Otopside her iki böbrek korteksinin diffüz sarı-beyaz koagülasyon nekrozuna uğradığı, medullanın ise korunduğu saptanıyor. Tanı nedir?",
            "options": [
                "A) Akut piyelonefrit",
                "B) Diffüz renal kortikal nekroz",
                "C) Akut interstisyel nefrit",
                "D) Malign nefroskleroz",
                "E) Fokal segmental glomerüloskleroz"
            ],
            "correctAnswer": 1,
            "explanation": "Ablasyo plasenta ve DİK zemininde gelişen bilateral kortikal iskemik harabiyet Diffüz Renal Kortikal Nekrozun patognomonik kliniğidir."
        }
    ),
    make_slide(
        17,
        "Orak Hücreli Anemi Nefropatisi: Medüller Hipoksi ve Papiller Hasar",
        "Düşük Oksijen ve Hipertonisitede Oraklaşma, Mikroenfarktüsler ve Hipostenüri",
        """Orak Hücreli Anemi (HbSS) ve hatta Orak Hücreli Taşıyıcılık (HbAS), böbreğin kendine has mikromimarisi nedeniyle karakteristik bir tübülointerstisyel ve vasküler nefropatiye yol açar.

**1. Patofizyolojik Zemin (Neden Böbrek Medullası?):**
• Böbrek medullası vücudun fizyolojik olarak en derin **hipoksiye**, **asidoza** ve **hiperosmolariteye (hipertonisiteye)** sahip bölgesidir.
• Bu üç faktör (hipoksi, asidoz, hipertonisite) anormal hemoglobin S moleküllerinin polimerizasyonunu ve eritrositlerin **oraklaşmasını (sickling)** maksimum düzeyde tetikler.
• Vasa rekta kılcallarında oraklaşan eritrositler agregat oluşturarak mikrodolaşımı tıkar.

**2. Karakteristik Klinikopatolojik Bulgular:**
• **Hipostenüri / İzostenüri:** Medüller vasa rektaların tıkanması ve hipertonik medüller gradiyentin bozulması sonucu idrar konsantre edilemez; çocuklukta en erken bulgu noktüri ve enürezisdir.
• **Renal Papiller Nekroz:** Medüller iskeminin derinleşmesiyle papillalar nekroze olup dökülür; ağrısız makroskopik hematürinin sık nedenidir.
• **Glomerülomegali ve Sekonder FSGS:** Kronik anemiye bağlı hiperfiltrasyon glomerülleri büyütür ve zamanla fokal segmental glomerüloskleroz ile nefrotik proteinüriye yol açar.""",
        [
            {"type": "clinical", "badge": "🔴 PATOFİZYOLOJİK ZEMİN", "text": "Böbrek medullasındaki hipoksi, asidoz ve hiperosmolarite vasa rektalarda eritrosit oraklaşmasını tetikleyerek en erken bulgu olan konsantrasyon kusuruna (hipostenüri) ve papiller nekroza yol açar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Orak hücreli nefropatide medüller hasar hipostenüri ve papiller nekroza yol açarken; glomerüllerde hiperfiltrasyona bağlı FSGS gelişir.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-017",
            "question": "Orak hücreli anemi hastalarında vasa rekta damarlarında eritrositlerin kolayca oraklaşarak mikrovasküler tıkanıklık ve papiller nekroz oluşturmasına zemin hazırlayan renal medüller ortam özelliği hangisidir?",
            "options": [
                "A) Yüksek oksijen basıncı ve alkaloz",
                "B) Derin hipoksi, asidoz ve hiperosmolarite",
                "C) Aşırı lenfatik akım",
                "D) Hipotonik interstisyel sıvı",
                "E) Yüksek perfüzyon basıncı"
            ],
            "correctAnswer": 1,
            "explanation": "Böbrek medullasının düşük oksijen satürasyonu, asidik pH'sı ve yüksek osmolaritesi HbS polimerizasyonunu ve oraklaşmayı doğrudan tetikler."
        }
    ),
    make_slide(
        18,
        "Vasküler Böbrek Hastalıklarında Radyolojik ve Patolojik Görüntüleme",
        "Renal Doppler USG, BT Anjiyo ve Parankim İncelemelerinin Rolü",
        """Vasküler ve kistik böbrek hastalıklarının teşhisinde radyolojik modalitelerin patolojik korelasyonu kritik öneme sahiptir.

**1. Renal Doppler Ultrasonografi:**
• Renal arter stenozu taramasında ilk basamak testtir; darlık bölgesinde pik sistolik hızın (PSV) >180-200 cm/sn olması ve renal/aortik hız oranının (RAR) >3.5 olması anlamlı darlığı gösterir.
• Direnç İndeksi (RI): Parankimal vasküler sklerozun ve kronik hasarın derecesini yansıtır.

**2. Manyetik Rezonans ve Bilgisayarlı Tomografi Anjiyografi (BTA/MRA):**
• Aterosklerotik ostial darlıkları ve Fibromusküler Displazinin 'tespih tanesi' görünümünü kesin olarak anatomik düzeyde haritalar.
• Kontrast Nefropatisi Riski: eGFR <30 mL/dk olan hastalarda iyotlu BT kontrast maddeleri akut tübüler hasarı, gadolinyum ise Nefrojenik Sistemik Fibrozisi tetikleyebilir.

**3. Kist Değerlendirmesinde USG ve Kontrastlı BT/MRG:**
• USG basit kist ile polikistik böbrek ayrımında tarama yöntemidir (ADPKD için yaşa göre kist sayısı kriterleri: 15-39 yaşta her böbrekte en az 3 kist tanısaldır).
• Bosniak sınıflaması kontrastlı BT veya dinamik MRG ile yapılır.""",
        [
            {"type": "clinical", "badge": "🔴 KLİNİK KRİTER", "text": "Pozitif aile öyküsü olan 15-39 yaş arası bireyde ultrasonda her iki böbrekte toplam en az 3 kist görülmesi ADPKD tanısı için yeterlidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Fibromusküler displazi anjiyografide 'tespih tanesi' (string of beads) verirken; aterosklerotik darlık aortadan çıkış noktasında (ostiumda) yerleşir.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-018",
            "question": "Ailesinde ADPKD öyküsü olan 25 yaşındaki asemptomatik bir bireyde ultrasonografi ile kesin ADPKD tanısı koyabilmek için her iki böbrekte toplamda en az kaç adet kist saptanmalıdır?",
            "options": [
                "A) En az 1 kist",
                "B) En az 3 kist (tek veya bilateral)",
                "C) En az 10 kist",
                "D) En az 20 kist",
                "E) Yalnızca karaciğerde kist olması yeterlidir"
            ],
            "correctAnswer": 1,
            "explanation": "Ravine kriterlerine göre 15-39 yaş grubunda aile öyküsü olan bireyde her iki böbrekte toplam en az 3 kistin saptanması ADPKD için tanı koydurucudur."
        }
    ),
    make_slide(
        19,
        "Vasküler Böbrek Lezyonlarının Mikroskobik Atlası",
        "Hyalen vs Hiperplastik Arteriyoloskleroz, Fibrinoid Nekroz ve Kolesterol Kleftleri",
        """Vasküler patolojilerin mikroskobik lezyonları, renal biyopsinin en karakteristik görsel paternleridir.

**1. Hyalen Arteriyoloskleroz:**
• Homojen, eozinofilik, camsı PAS-pozitif subendotelyal birikim.
• Afferent arteriyol duvarında kalınlaşma ve lümende simetrik daralma.
• *İlişkili durumlar:* Benign esansiyel hipertansiyon, Diabetes Mellitus, ileri yaş.

**2. Hiperplastik Arteriyoloskleroz ('Soğan Zarı'):**
• Düz kas hücreleri ve kollajenin konsantrik laminer proliferasyonu.
• *İlişkili durum:* Malign hipertansiyon.

**3. Fibrinoid Nekroz:**
• Damar duvarında pembe parlak amorf fibrin birikimi, nükleer parçalanma (karyoreksis) ve lümende trombosit tıkaçları.
• *İlişkili durumlar:* Malign hipertansiyon, ANCA vaskülitleri, sistemik skleroz krizi.

**4. Kolesterol Ateroembolisi:**
• Arteriyol lümenini dolduran bikonveks, iğsi boşluklar (kolesterol kristalleri) ve çevresinde yabancı cisim multinükleer dev hücreleri.
• *İlişkili durum:* Aortik anjiyografi/kateterizasyon sonrası embolizasyon.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Hyalen = Benign HT/Diyabet; Soğan zarı ve Fibrinoid nekroz = Malign HT; İğsi kleftler = Kolesterol embolisi.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu 4 vasküler lezyonun patolojik tanımı nefroloji ve patoloji komitelerinde doğrudan lezyon eşleştirme sorusu olarak sorulur.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-019",
            "question": "Malign hipertansiyon tanılı bir hastanın böbrek biyopsisinde interlobüler arterlerde izlenen düz kas hücrelerinin konsantrik laminer proliferasyonu ile karakterize lezyon aşağıdakilerden hangisidir?",
            "options": [
                "A) Hyalen arteriyoloskleroz",
                "B) Hiperplastik arteriyoloskleroz (soğan zarı)",
                "C) Mönckeberg medial kalsinozisi",
                "D) Amiloid anjiyopatisi",
                "E) Anevrizma diseksiyonu"
            ],
            "correctAnswer": 1,
            "explanation": "Konsantrik laminer intimal düz kas proliferasyonu 'Hiperplastik arteriyoloskleroz' (soğan zarı lezyonu) olarak adlandırılır ve Malign Hipertansiyonun klasik bulgusudur."
        }
    ),
    make_slide(
        20,
        "Kistik Hastalıkların Genetik ve Moleküler Haritası",
        "Siliya Biyolojisi, Siliyopatiler ve cAMP Sinyal Yolağı Hedefleri",
        """Kistik böbrek hastalıklarının hemen tamamı hücresel düzeyde 'Siliyopatiler' (primer siliya bozuklukları) başlığı altında toplanır.

**1. Primer Siliya Kompleksi:**
• Tübül epitel hücresinin apikal yüzeyinde lümene uzanan tekil, hareketsiz bir siliyadır.
• İdrar akımının oluşturduğu mekanik sürtünme siliyayı eğer; bu bükülme Polisistin-1/2 ve Fibrosistin kompleksini aktive eder.
• Normal fonksiyonda hücre içine kalsiyum girer ve hücre içi kalsiyum düzeyi regüle edilir.

**2. Kist Gelişiminde cAMP ve Terapötik Hedef:**
• Siliya defektinde kalsiyum girişi bozulur; adenilil siklaz aşırı aktive olarak hücre içi **cAMP** düzeyini katlar.
• Yüksek cAMP -> Raf/MEK/ERK sinyal yolağını uyararak epitel proliferasyonunu tetikler.
• Aynı zamanda CFTR klor kanalını uyararak lümene sıvı salgılanmasına neden olur.
• **Tolvaptan (V2 Reseptör Antagonisti):** Bazal membrandaki vazopressin V2 reseptörlerini bloke ederek hücre içi cAMP üretimini engeller; ADPKD'de kist büyümesini ve böbrek fonksiyon kaybını yavaşlatan FDA onaylı ilk spesifik ilaçtır.""",
        [
            {"type": "clinical", "badge": "🔴 HEDEFE YÖNELİK TEDAVİ", "text": "ADPKD'de kistlerin büyümesini yavaşlatmak için kullanılan Tolvaptan, vazopressin V2 reseptör blokajı yaparak hücre içi cAMP düzeyini düşürür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Kistik böbrek hastalıklarının ortak hücresel organeli 'primer siliya'dır; bu nedenle genetik kistik böbrek hastalıkları 'siliyopati' olarak sınıflandırılır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-020",
            "question": "Otozomal Dominant Polikistik Böbrek Hastalığında (ADPKD) kist büyümesini ve böbrek hacim artışını yavaşlatmak amacıyla kullanılan ve vazopressin V2 reseptörlerini bloke eden ilaç hangisidir?",
            "options": [
                "A) Spironolakton",
                "B) Tolvaptan",
                "C) Furosemid",
                "D) Siklosporin",
                "E) Eculizumab"
            ],
            "correctAnswer": 1,
            "explanation": "Tolvaptan selektif bir vazopressin V2 reseptör antagonistidir; tübül hücresinde cAMP üretimini baskılayarak ADPKD'de kist büyümesini yavaşlatır."
        }
    ),
    make_slide(
        21,
        "Vasküler ve Kistik Hastalıklarda Klinik Yaklaşım ve Tarama Protokolleri",
        "Hipertansiyon Kontrolü, Aile Taramaları ve İntrakraniyal Anevrizma Taraması",
        """Klinik pratikte vasküler veya kistik böbrek hastalığı saptanan hastada ve ailesinde izlenecek stratejik adımlar:

**1. ADPKD Hastasında ve Ailesinde İzlem:**
• **Kan Basıncı Hedefi:** Hipertansiyon kist büyümesini ve kardiyovasküler mortaliteyi hızlandırır. İlk tercih **ACE inhibitörleri veya ARB'lerdir**; hedef TA <120/80 mmHg olmalıdır.
• **Anevrizma Taraması:** Tüm ADPKD hastalarına rutin anjiyografi gerekmez! Ancak:
  - Ailede SAK veya intrakraniyal anevrizma öyküsü olanlar,
  - Pilot, cerrah, otobüs şoförü gibi yüksek riskli meslek sahipleri,
  - Şiddetli veya yeni başlayan atipik baş ağrısı olanlarda **Manyetik Rezonans Anjiyografi (MRA)** ile tarama zorunludur.

**2. Renal Arter Stenozunda Girişim Endikasyonları:**
• Tıbbi tedaviye dirençli hipertansiyon, tekrarlayan 'flash' pulmoner ödem veya ACE inhibitörü başlandıktan sonra kreatininde >%30 ani artış olması durumunda perkütan renal anjiyoplasti ve stentleme düşünülür.""",
        [
            {"type": "clinical", "badge": "🔴 KRİTİK KLİNİK İPUCU", "text": "Bir hipertansiyon hastasında ACE inhibitörü başlandıktan sonra serum kreatinini hızla >%30 yükselirse akla derhal 'Bilateral Renal Arter Stenozu' gelmelidir!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Bilateral renal arter stenozunda ACE inhibitörleri eferent arteriyol dilatasyonu yaparak glomerüler filtrasyon basıncını sıfırlar ve akut böbrek yetmezliğini tetikler.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-021",
            "question": "Hipertansiyon tedavisi için enalapril (ACE inhibitörü) başlanan 62 yaşındaki bir hastada 1 hafta sonra kreatinin değerinin 1.2 mg/dL'den 3.2 mg/dL'ye yükseldiği görülüyor. Bu hastada şüphelenilmesi gereken en olası vasküler tanı hangisidir?",
            "options": [
                "A) Tek taraflı basit kist rüptürü",
                "B) İki taraflı (bilateral) renal arter stenozu",
                "C) Benign nefroskleroz",
                "D) Minimal değişiklik hastalığı",
                "E) Renal ven trombozu"
            ],
            "correctAnswer": 1,
            "explanation": "Bilateral renal arter darlığında glomerül filtrasyonu eferent arteriyolün vazokonstriksiyonu ile korunur; ACE inhibitörü verilince eferent arteriyol gevşer ve akut anürik böbrek yetmezliği gelişir."
        }
    ),
    make_slide(
        22,
        "Vasküler Böbrek Hastalıkları Büyük Karşılaştırma Matrisi",
        "Etyoloji, Damar Tutulumu, Histopatoloji ve Klinik Bulguların Özeti",
        """Vasküler böbrek hastalıklarının karşılaştırmalı patoloji tablosu:

| Hastalık | Tutulan Damar | Temel Histopatolojik Lezyon | Makroskobik Görünüm | Klinik Özellik |
| :--- | :--- | :--- | :--- | :--- |
| **Benign Nefroskleroz** | Afferent arteriyol, küçük arter | **Hyalen arteriyoloskleroz**, tübüler atrofi | İnce granüler **'Tabaklanmış Deri'** (leather grain) | Uzun süreli esansiyel HT, sinsi böbrek yetmezliği |
| **Malign Nefroskleroz** | Arteriyol ve interlobüler arter | **Fibrinoid nekroz** ve **'Soğan Zarı'** hiperplazi | Kortekste peteşiyel **'Pire Isırığı'** (flea-bitten) | TA >200/120 mmHg, papilödem, akut oligürik kriz |
| **Renal Arter Stenozu** | Ana renal arter (ostium veya orta) | Darlık böbreğinde iskemik atrofi; karşıda nefroskleroz | Darlık tarafı küçülmüş; karşı böbrek hipertrofik | Dirençli HT, karında üfürüm, FMD'de tespih tanesi |
| **HÜS / TTP (TMA)** | Glomerül kapillerleri, arteriyol | Mikrovasküler trombüsler, endotel şişmesi | Şiş, soluk, peteşiyel korteks | Şistositler (MAHA), trombositopeni, kanlı ishal (HÜS) |
| **Ateroemboli** | Küçük interlobüler arterler | Bikonveks **iğsi kolesterol yarıkları (kleftleri)** | Yama tarzı iskemik solukluk | Anjiyo sonrası livedo retikularis, eozinofili |
| **Kortikal Nekroz** | Tüm kortikal mikrodolaşım | Diffüz iskemik koagülasyon nekrozu | Korteks tamamen sarı-beyaz nekrotik | Gebelik (Ablasyo plasenta), DİK, tam anüri |""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Tabaklanmış deri = Benign HT; Pire ısırığı = Malign HT; Kolesterol klefti = Ateroemboli; Sarı nekrotik korteks = Kortikal nekroz.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu matris tüm vasküler böbrek patolojilerini tek bakışta özetleyen temel referans tablodur.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-022",
            "question": "Aşağıdaki vasküler böbrek hastalığı ve karakteristik histopatolojik lezyon eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) Benign nefroskleroz — Hyalen arteriyoloskleroz",
                "B) Malign nefroskleroz — Konsantrik soğan zarı hiperplazisi ve fibrinoid nekroz",
                "C) Ateroembolik böbrek hastalığı — Bikonveks iğsi kolesterol yarıkları",
                "D) Renal kortikal nekroz — Glomerüllerde podosit ayaksı çıkıntı silinmesi",
                "E) HÜS / TTP — Glomerül kapillerlerinde mikrovasküler trombüsler"
            ],
            "correctAnswer": 3,
            "explanation": "Renal kortikal nekrozda podosit silinmesi değil; tüm kortikal glomerül ve tübüllerin diffüz iskemik koagülasyon nekrozu izlenir."
        }
    ),
    make_slide(
        23,
        "Kistik Böbrek Hastalıkları Büyük Karşılaştırma Matrisi",
        "Kist Dağılımı, Genetik, Mikroskopi ve Ekstrarenal Tutulumların Özeti",
        """Kistik böbrek hastalıklarının Robbins patoloji kriterlerine göre büyük ayırıcı tanı matrisi:

| Hastalık | Genetik / Kalıtım | Kist Lokalizasyonu ve Görünümü | Böbrek Boyutu | Karaciğer ve Ekstrarenal Tutulum | Prognoz / Seyir |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ADPKD** | *PKD1* (16p), *PKD2* (4q) / Otozomal Dominant | **Tüm nefron segmentleri**, yuvarlak büyük kistler | Bilateral **Devasa** (kilolarca) | Karaciğer kistleri (%40), **Berry anevrizması** (%10-20), MVP | 50-70 yaşta SDBY |
| **ARPKD** | *PKHD1* (6p) / Otozomal Resesif | **Yalnızca toplayıcı kanallar**, radyal fuziform | Bilateral simetrik büyümüş | **Konjenital Hepatik Fibrozis** (zorunlu), Potter sekansı | Bebekte pulmoner hipoplazi ölümü |
| **Medüller Sünger** | Sporadik / Edinsel | Papiller toplayıcı kanallar (Bellini) | Normal boyut | Yok | Benign, taş ve enfeksiyon riski |
| **Nefronofitizis** | *NPHP* genleri / Otozomal Resesif | **Kortikomedüller bileşke** kistleri | **Küçülmüş / Büzüşmüş** | Retinitis pigmentoza, ataksi | Çocukta SDBY'nin en sık genetik nedeni |
| **Diyaliz İlişkili** | Edinsel (Kronik diyaliz) | Korteks ve medulla kistleri | Küçülmüş son dönem böbrek | Yok | **RCC (Renal karsinom)** riski artar |""",
        [
            {"type": "warning", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "ADPKD = Devasa böbrek + Berry anevrizması; ARPKD = Fuziform kist + Karaciğer fibrozu; Nefronofitizis = Küçük böbrek + Kortikomedüller kistler.", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN MATRİS", "text": "Bu tablo komite ve TUS sınavlarında kistik böbrek hastalıkları sorularının doğrudan çözüm anahtarıdır.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-023",
            "question": "Aşağıdaki kistik böbrek hastalıklarından hangisinde böbrek boyutları devasa büyümek yerine simetrik olarak KÜÇÜLMÜŞTÜR ve kistler sadece kortikomedüller bileşkede yerleşir?",
            "options": [
                "A) Otozomal dominant polikistik böbrek",
                "B) Nefronofitizis",
                "C) Otozomal resesif polikistik böbrek",
                "D) Basit kortikal kist",
                "E) Medüller sünger böbrek"
            ],
            "correctAnswer": 1,
            "explanation": "Nefronofitizis / Medüller Kistik Böbrek Hastalığında böbrekler ileri derecede büzüşmüş ve küçülmüştür; kistler karakteristik olarak kortikomedüller bileşkede sınırlıdır."
        }
    ),
    make_slide(
        24,
        "Ders 23 Kapsamlı Sentezi: Vasküler ve Kistik Patolojinin Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Prof. Dr. Hikmet Keleş'in Vasküler ve Kistik Böbrek Hastalıkları dersinin en kritik sınav ve klinik özeti:

**1. Vasküler ve Kistik Patolojinin 10 Altın Kuralı:**
1. *Benign Nefroskleroz:* Afferent arteriyolde hyalen arteriyoloskleroz; böbrek yüzeyinde ince granüler 'tabaklanmış deri' (leather grain) görünümü.
2. *Malign Nefroskleroz:* TA >200/120 mmHg, papilödem; arteriyollerde fibrinoid nekroz ve 'soğan zarı' (hiperplastik) lezyonu; kortekste 'pire ısırığı' peteşileri.
3. *Renal Arter Stenozu:* Yaşlı erkekte ateroskleroz (ostial); genç kadında Fibromusküler Displazi (orta arterde tespih tanesi). Darlık böbreği korunur, karşı böbrek nefroskleroz geliştirir.
4. *ACE İnhibitörü Tuzağı:* Bilateral renal arter darlığında ACE inhibitörü başlanırsa akut anürik böbrek yetmezliği gelişir.
5. *TMA (HÜS ve TTP):* Şistositler (MAHA) + Trombositopeni + Böbrek hasarı; HÜS'te E. coli O157:H7 Shiga toksini; TTP'de ADAMTS13 eksikliği.
6. *ADPKD:* PKD1 (16p - Polisistin-1, %85) ve PKD2 (4q - Polisistin-2); bilateral devasa kistler (tüm nefron); karaciğer kistleri (%40) ve Willis Berry anevrizmaları (SAK).
7. *ARPKD:* PKHD1 (6p - Fibrosistin); toplayıcı kanallarda fuziform radyal ektazi; Konjenital Hepatik Fibrozis zorunludur; bebekte pulmoner hipoplazi ölümü.
8. *Medüller Sünger Böbrek:* Papiller toplayıcı kanallarda ektazi; benign seyreder, böbrek yetmezliği yapmaz.
9. *Nefronofitizis:* Çocukta SDBY'nin en sık genetik nedeni; böbrekler küçüktür, kistler kortikomedüller bileşkededir.
10. *Ateroembolik Böbrek:* Anjiyografi sonrası interlobüler arterlerde iğsi kolesterol yarıkları (clefts).""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Klinikte dirençli hipertansiyonu olan genç kadında FMD; devasa kistleri ve baş ağrısı olan hastada ADPKD + Berry anevrizması akla gelmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta listelenen 10 kural vasküler ve kistik böbrek hastalıkları konusundaki tüm komite ve TUS sorularını eksiksiz kapsar.", "color": "sky"}
        ],
        {
            "id": "prac-vsk-024",
            "question": "Aşağıdaki klinik tablolardan hangisinde bilateral dev böbrekler, karaciğer kistleri ve intrakraniyal berry anevrizması rüptürü riski bir arada bulunur?",
            "options": [
                "A) Otozomal dominant polikistik böbrek hastalığı (ADPKD)",
                "B) Otozomal resesif polikistik böbrek hastalığı (ARPKD)",
                "C) Medüller sünger böbrek",
                "D) Nefronofitizis",
                "E) Malign hipertansif nefroskleroz"
            ],
            "correctAnswer": 0,
            "explanation": "Bilateral dev polikistik böbrekler, polikistik karaciğer ve intrakraniyal berry anevrizmaları Otozomal Dominant Polikistik Böbrek Hastalığının (ADPKD) klasik triadıdır."
        }
    )
]

print("Vasküler ve Kistik Hastalıklar 24 slayt başarıyla tanımlandı.")

target_id = 'learn-vaskuler-kistik-bobrek-hastaliklari'
for d in decks:
    if d.get('id') == target_id:
        d['title'] = "Vasküler ve Kistik Böbrek Hastalıkları Patolojisi"
        d['shortTitle'] = "Vasküler ve Kistik Patoloji"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Benign ve malign nefroskleroz (hyalen vs soğan zarı, pire ısırığı), Renal arter stenozu (FMD, tespih tanesi), TMA (HÜS ve TTP), Ateroemboli (kolesterol kleftleri), Kortikal nekroz, ADPKD (Polisistin, Berry anevrizmaları), ARPKD (Fibrosistin, hepatik fibrozis), Nefronofitizis ve Bosniak kist sınıflaması."
        d['slides'] = vaskuler_kistik_slides
        print(f"'{target_id}' güvertesi 24 yüksek kaliteli slaytla güncellendi.")
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("Vasküler ve Kistik Hastalıklar güncellemesi tamamlandı.")
