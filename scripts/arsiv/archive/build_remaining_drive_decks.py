# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

print(f"Mevcut güverte sayısı: {len(decks)}")

# Helper to build slide
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

# ==============================================================================
# DECK 1: learn-enfeksiyon-temel-kavramlar (24 Slayt)
# ==============================================================================
deck_enfeksiyon_kavramlar_slides = []

# S1
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    1,
    "Enfeksiyon ve Enfeksiyon Hastalığı Ayrımı",
    "Subklinik Enfeksiyondan Klinik Tabloya Geçişin Kriterleri",
    """Enfeksiyon ve enfeksiyon hastalığı kavramları klinik mikrobiyolojide sıklıkla birbiriyle karıştırılan ancak prognoz, tedavi ve epidemiyoloji açısından keskin çizgilerle ayrılan iki temel olgudur.

**1. Temel Tanımlar ve Kavramsal Çerçeve:**
• **Enfeksiyon:** Bir mikroorganizmanın (bakteri, virüs, mantar, parazit) duyarlı bir konağa girmesi, canlı dokulara yerleşmesi ve bu dokularda çoğalmasıdır.
• **Enfeksiyon Hastalığı:** Mikroorganizmanın çoğalması, salgıladığı toksinler veya konağın geliştirdiği aşırı immünopatolojik yanıt neticesinde konakta belirgin hücresel/doku hasarının ve klinik belirti-bulguların (ateş, ağrı, organ disfonksiyonu) ortaya çıkması durumudur.

**2. Kritik Amfi Kuralı:**
Her enfeksiyon mutlaka bir enfeksiyon hastalığına dönüşmez! Çoğu patojenle karşılaşma asemptomatik (subklinik) enfeksiyon şeklinde seyreder ve konak hiçbir klinik yakınma geliştirmeden özgül bağışıklık kazanabilir.""",
    [
        {"type": "warning", "badge": "Kritik Tanım / Dikkat", "text": "Klinik belirti ve bulgu olmadan da enfeksiyon mevcuttur; buna subklinik/asemptomatik enfeksiyon denir.", "color": "rose"},
        {"type": "exam", "badge": "Komite / Çıkmış Vurgusu", "text": "Enfeksiyonun varlığı 'mikroorganizmanın yerleşip çoğalması' ile tanımlanırken; 'enfeksiyon hastalığı' ancak doku hasarı ve klinik bulgular eklendiğinde teşhis edilir.", "color": "sky"}
    ],
    {
        "id": "prac-enk-001",
        "question": "Enfeksiyon ile enfeksiyon hastalığı arasındaki temel fark aşağıdakilerden hangisinde doğru olarak ifade edilmiştir?",
        "options": [
            "A) Enfeksiyonda mikroorganizma çoğalmaz, enfeksiyon hastalığında çoğalır",
            "B) Enfeksiyon mikrobiyal yerleşme ve çoğalmayı ifade ederken, enfeksiyon hastalığı klinik belirti, bulgu ve doku hasarının varlığını gerektirir",
            "C) Enfeksiyon yalnızca virüslerle, enfeksiyon hastalığı ise yalnızca bakterilerle oluşur",
            "D) Enfeksiyon hastalığı her zaman asemptomatik seyrederken, enfeksiyon mutlaka fatal seyreder",
            "E) Enfeksiyon yalnızca nozokomiyal kökenlidir, enfeksiyon hastalığı ise toplum kökenlidir"
        ],
        "correctAnswer": 1,
        "explanation": "Enfeksiyon mikroorganizmanın konağa girip çoğalmasıdır; enfeksiyon hastalığı ise konakta doku hasarı ve klinik belirti-bulguların ortaya çıkmasıyla tanımlanır."
    }
))

# S2
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    2,
    "Flora, Kommensalizm ve Fırsatçı Patojenler",
    "Mikrobiyota Dengesi ve İmmünsüpresyonda Gelişen İstilalar",
    """İnsan vücudunda deri ve mukoza yüzeylerinde trilyonlarca mikroorganizmadan oluşan zengin bir normal mikrobiyota (flora) bulunur.

**1. İlişki Tipleri:**
• **Kommensalizm:** Mikroorganizmanın konaktan faydalandığı, ancak konağa ne yarar ne de zarar verdiği dengeli ortak yaşam biçimidir (örneğin derideki koagülaz negatif stafilokoklar).
• **Mutualizm:** Hem konağın hem mikroorganizmanın karşılıklı fayda sağladığı birliktelik (örneğin kolondaki K ve B vitamini sentezleyen bakteriler).
• **Parazitizm:** Mikroorganizmanın konak aleyhine yaşadığı ve konağa doğrudan zarar verdiği ilişki.

**2. Fırsatçı (Oportünistik) Patojenler:**
Normal flora üyesi olan veya çevrede zararsızca bulunan, ancak konağın lokal/sistemik savunma mekanizmaları bozulduğunda (nötropeni, diyabet, HIV, geniş spektrumlu antibiyotik kullanımı, kateter takılması) hastalık tablosu oluşturan ajanlardır (örn. Candida albicans, Pseudomonas aeruginosa, Clostridioides difficile).""",
    [
        {"type": "clinical", "badge": "Klinik Tuzak / Dikkat", "text": "Geniş spektrumlu antibiyotik kullanımı normal kolon florasını baskılayarak dirençli Clostridioides difficile veya Candida süperenfeksiyonlarına yol açar.", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu / TUS", "text": "Fırsatçı enfeksiyon etkenleri immün sistemi sağlam bireylerde hastalık yapmazken, immünsüpresif konakta hayatı tehdit eden sepsise yol açabilir.", "color": "sky"}
    ],
    {
        "id": "prac-enk-002",
        "question": "Aşağıdakilerden hangisi 'fırsatçı (oportünistik) patojen' kavramını en iyi tanımlar?",
        "options": [
            "A) Yalnızca vahşi hayvanlarda hastalık yapan zoonotik mikroorganizmalar",
            "B) Sağlıklı bireylerde ağır ölümcül salgınlara yol açan yüksek virülanslı bakteriler",
            "C) Normal koşullarda zararsız olan ancak konak savunması zayıfladığında hastalık oluşturan mikroorganizmalar",
            "D) İnsan vücuduna girdikten saniyeler sonra ekzotoksin salgılayan obligat hücre içi parazitler",
            "E) Yalnızca cerrahi aletler üzerinde spor oluşturan anaerobik basiller"
        ],
        "correctAnswer": 2,
        "explanation": "Fırsatçı patojenler, konağın immün veya anatomik bariyerleri zayıfladığında enfeksiyon hastalığı tablosu oluşturan mikrobiyal ajanlardır."
    }
))

# S3
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    3,
    "Patojenite ve Virülans Kavramları",
    "Niteliksel Yetenek ile Niceliksel Hastalık Yapma Gücü",
    """Enfeksiyon hastalıkları derslerinde en sık karıştırılan iki terim patojenite ve virülanstır. Amfi sınavlarında bu iki kavramın ayrımı ısrarla sorulur.

**1. Patojenite (Niteliksel Özellik):**
• Bir mikroorganizmanın duyarlı bir konakta hastalık meydana getirme yeteneğidir.
• Kalitatif (niteliksel) bir kavramdır; mikroorganizma ya patojendir ya da nonpatojendir (var/yok prensibi).

**2. Virülans (Niceliksel Derece):**
• Patojen olan bir mikroorganizmanın hastalık oluşturma gücünün, şiddetinin veya derecesinin niceliksel (kantitatif) ölçüsüdür.
• Aynı tür içerisindeki farklı suşlar arasında dahi değişkenlik gösterir (örneğin kapsüllü Streptococcus pneumoniae suşları kapsülsüz suşlara göre çok daha yüksek virülansa sahiptir).
• Laboratuvarda $ID_{50}$ (enfektif doz) ve $LD_{50}$ (letal doz) parametreleriyle ölçülür.""",
    [
        {"type": "warning", "badge": "Hayati Formül / Vurgu", "text": "Patojenite 'niteliksel' (hastalık yapabilir mi?), virülans ise 'niceliksel'dir (ne kadar ağır/öldürücü hastalık yapar?).", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusudur", "text": "LD50 (Lethal Dose 50): Test edilen deney hayvanlarının %50'sini öldüren mikroorganizma sayısıdır. LD50 değeri ne kadar DÜŞÜKSE virülans o kadar YÜKSEKTİR!", "color": "sky"}
    ],
    {
        "id": "prac-enk-003",
        "question": "Patojenite ve virülans kavramları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
        "options": [
            "A) Patojenite niceliksel bir ölçümken, virülans niteliksel bir özelliktir",
            "B) Bir mikroorganizmanın LD50 değeri ne kadar yüksekse virülansı o kadar yüksektir",
            "C) Patojenite hastalık yapabilme yeteneğidir; virülans ise bu yeteneğin şiddet derecesidir",
            "D) Virülans tüm bakteri suşlarında sabittir ve değiştirilemez",
            "E) Nonpatojen mikroorganizmaların LD50 değeri daima sıfırdır"
        ],
        "correctAnswer": 2,
        "explanation": "Patojenite niteliksel (hastalık yapabilme yeteneği), virülans ise niceliksel derecedir (hastalığın şiddeti). LD50 düştükçe virülans artar."
    }
))

# S4
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    4,
    "Enfeksiyon Zincirinin 6 Halkası",
    "Bulaş Döngüsü ve Salgın Kontrol Stratejileri",
    """Bir enfeksiyon hastalığının toplumda ortaya çıkması ve yayılması, birbirine bağlı 6 halkadan oluşan 'Enfeksiyon Zinciri' modeline dayanır. Bu halkalardan herhangi birinin kırılması enfeksiyonun yayılmasını durdurur.

**Enfeksiyon Zincirinin Bileşenleri:**
1. **Enfeksiyon Etkeni:** Bakteri, virüs, mantar, parazit veya prion.
2. **Rezervuar (Kaynak):** Etkenin doğal olarak yaşadığı, çoğaldığı ortam (insan, hayvan, toprak, su).
3. **Kaynaktan Çıkış Kapısı:** Etkenin rezervuarı terk ettiği yol (solunum sekresyonları, dışkı, idrar, kan, genital akıntı).
4. **Bulaşma Yolu:** Etkenin konaktan konağa aktarım modu (doğrudan temas, damlacık, hava yolu/aerosol, vektör, araç/fomit).
5. **Giriş Kapısı:** Etkenin yeni konağa girdiği anatomik bölge (solunum yolu, gastrointestinal sistem, mukozalar, hasarlı deri).
6. **Duyarlı Konak:** İmmünitesi yetersiz, aşısız veya genetik yatkınlığı olan birey.""",
    [
        {"type": "clinical", "badge": "Halk Sağlığı / Önleme", "text": "El hijyeni ve maske kullanımı bulaşma yolunu kırarken; aşı uygulamaları duyarlı konak halkasını yok eder.", "color": "rose"},
        {"type": "exam", "badge": "Komite Soru Kalıbı", "text": "Hastalığın kontrolünde en etkili halka 'bulaşma yolunun kesilmesi' ve 'kaynağın kurutulması'dır.", "color": "sky"}
    ],
    {
        "id": "prac-enk-004",
        "question": "Aşağıdakilerden hangisi enfeksiyon zincirinde 'duyarlı konak' halkasını kırarak toplum bağışıklığı sağlayan en temel yöntemdir?",
        "options": [
            "A) Maske takılması",
            "B) El antiseptiği kullanımı",
            "C) Aktif bağışıklama (aşılama)",
            "D) Atık suların klorlanması",
            "E) Karasineklerle mücadele"
        ],
        "correctAnswer": 2,
        "explanation": "Aşılama (aktif bağışıklama), duyarlı konakları dirençli hale getirerek zincirin 'duyarlı konak' halkasını doğrudan kırar."
    }
))

# S5
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    5,
    "Bakteriyel Adezyon ve Kolonizasyon",
    "Pili, Fimbriya ve Doku Tropizmi Mekanizmaları",
    """Bakterilerin konak dokusunda enfeksiyon başlatabilmesi için ilk ve en kritik basamak epitel hücrelerine tutunmadır (adezyon). Tutunamayan bakteriler mukus akımı, peristaltizm ve idrar akışıyla vücuttan atılır.

**1. Adezyon Mekanizmaları:**
• **Fimbriya / Pili:** Bakteri yüzeyinden uzanan protein yapılı uzantılardır.
  - *Tip 1 Pili (Mannoz-sensitif):* Mesane ürotelyumuna tutunarak sistit tablosuna neden olur.
  - *P Fimbriyası (Mannoz-rezistan / Pap pili):* Böbrek toplayıcı tübül epitelindeki digalaktozid (Gal-Gal) reseptörlerine bağlanır ve Akut Piyelonefrit patogenezinin kilit faktörüdür.
• **Afimbriyal Adezinler:** Hücre duvarına bağlı yüzey proteinleri (örneğin Streptococcus pyogenes'te F proteini ve M proteini).

**2. Kolonizasyon:**
Bakterinin doku yüzeyine tutunduktan sonra konak savunmasını aşarak bölgede çoğalmasıdır. Kolonizasyon henüz doku invazyonu veya hastalık anlamına gelmez.""",
    [
        {"type": "warning", "badge": "Patoloji & Mikrobiyoloji Ortak Spotu", "text": "P Fimbriyası (Pap pili) olan E. coli suşları böbrek parankimine tırmanarak Akut Piyelonefrite yol açar!", "color": "rose"},
        {"type": "exam", "badge": "TUS & Komite Sorusu", "text": "Tip 1 pili mesane epitelinde (sistit), P pili ise renal tübül epitelinde (piyelonefrit) kolonizasyonu sağlar.", "color": "sky"}
    ],
    {
        "id": "prac-enk-005",
        "question": "Üropatojenik E. coli (UPEC) suşlarının renal pelvis ve böbrek toplayıcı kanallarına tutunarak akut piyelonefrit geliştirmesinde rol oynayan temel adezin hangisidir?",
        "options": [
            "A) Tip 1 mannoz-sensitif pilus",
            "B) P fimbriyası (Pap pili)",
            "C) Curli lifleri",
            "D) Flajellin proteini",
            "E) Protein A"
        ],
        "correctAnswer": 1,
        "explanation": "P fimbriyası (Pap pili), renal tübül hücrelerindeki Gal-Gal reseptörlerine bağlanarak üst üriner sistem invazyonuna (akut piyelonefrit) zemin hazırlar."
    }
))

# S6
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    6,
    "Bakteriyel Toksinler: Endotoksin vs Ekzotoksin",
    "Yapısal, İmmünolojik ve Klinik Ayrım Tablosu",
    """Bakteriyel toksinler konak dokularına doğrudan hasar veren en güçlü silahlardır. Temel olarak ekzotoksinler ve endotoksinler olarak ikiye ayrılırlar.

**Karşılaştırma Tablosu:**
• **Kaynak:** Ekzotoksinler hem Gram(+) hem Gram(-) canlı bakterilerce salgılanır. Endotoksin ise sadece Gram(-) bakterilerin dış membran yapı taşıdır (LPS).
• **Kimyasal Yapı:** Ekzotoksin polipeptit/protein yapılıdır; endotoksin ise Lipopolisakkarit (LPS) yapısındadır.
• **Isıya Dayanıklılık:** Ekzotoksinler ısıya duyarlıdır (60°C'de denatüre olur, istisna: Staph enterotoksini); Endotoksin 100°C'de 1 saat kaynatmaya bile dirençlidir!
• **Toksisite / Letalite:** Ekzotoksinler doğadaki en ölümcül zehirlerdir (botulinum, tetanoz toksini; mikrogram düzeyinde öldürür). Endotoksin daha düşük potenslidir (miligram düzeyinde etkilidir).
• **Toksoid Aşı:** Ekzotoksinlerden formaldehit ile zararsız hale getirilmiş aşı (toksoid) üretilebilir (Tetanoz, Difteri). Endotoksinden toksoid aşı üretilemez!""",
    [
        {"type": "warning", "badge": "Mutlak Bilinmeli / Kırmızı", "text": "Endotoksinin toksik ve pirojenik aktivitesinden sorumlu olan parça 'Lipid A' fraksiyonudur!", "color": "rose"},
        {"type": "exam", "badge": "Sık Sorulan Soru", "text": "Toksoid aşı yalnızca protein yapılı ekzotoksinlerden elde edilebilir; endotoksinlerden aşı yapılamaz.", "color": "sky"}
    ],
    {
        "id": "prac-enk-006",
        "question": "Endotoksinler ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
        "options": [
            "A) Gram negatif bakterilerin hücre duvarında bulunan lipopolisakkarit yapısındadır",
            "B) Toksik ve immünolojik aktivitelerinden sorumlu temel bileşen Lipid A'dır",
            "C) Isıya karşı son derece duyarlıdırlar ve 60°C'de kolayca inaktive olurlar",
            "D) Formaldehit muamelesi ile toksoid aşıya dönüştürülemezler",
            "E) Makrofajlardan TNF-alfa ve IL-1 salınımını uyararak ateşe ve septik şoka neden olurlar"
        ],
        "correctAnswer": 2,
        "explanation": "Endotoksinler ısıya son derece dayanıklıdır (100°C'de kaynatmaya dirençlidir). Isıya duyarlı olanlar protein yapılı ekzotoksinlerdir."
    }
))

# S7
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    7,
    "Lipopolisakkarit (LPS) ve Septik Şok Patogenezi",
    "TLR-4 Aktivasyonu, Sitokin Fırtınası ve DIC Mekanizması",
    """Gram negatif bakteri sepsisinin en korkulan tablosu olan septik şok, doğrudan dolaşıma karışan LPS moleküllerinin konak immün sistemini aşırı uyarmasıyla tetiklenir.

**Patogenetik Kaskad:**
1. **LBP ve CD14 Bağlanması:** Dolaşımdaki LPS, serumdaki LPS-Bağlayıcı Protein (LBP) ile birleşir ve monosit/makrofaj yüzeyindeki CD14 reseptörüne sunulur.
2. **TLR-4 Sinyal İletimi:** Kompleks, Toll-like Reseptör 4 (TLR-4) ve MD-2 aracılığıyla hücre içine NF-κB aktivasyon sinyali gönderir.
3. **Erken Sitokin Salınımı:** Makrofajlardan masif miktarda TNF-alfa, IL-1 ve IL-6 salınır.
4. **Endotel Hasarı ve Vazodilatasyon:** İndüklenebilir Nitrik Oksit Sentaz (iNOS) uyarılır -> aşırı Nitrik Oksit (NO) üretimi -> sistemik vazodilatasyon, vasküler geçirgenlik artışı, refrakter hipotansiyon.
5. **Koagülasyon Kaskadı (DIC):** Doku Faktörü ekspresyonu artar -> mikrovasküler trombüsler ve ardından tüketim koagülopatisi (Dissemine İntravasküler Koagülasyon).""",
    [
        {"type": "warning", "badge": "Ölümcül Tablo / Kırmızı Vurgu", "text": "Septik şoktaki refrakter vazodilatasyon ve hipotansiyonun temel mediyatörü aşırı üretilen Nitrik Oksittir (NO).", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Spotu", "text": "Bakteriyel endotoksin (LPS), memeli hücrelerinde Toll-like Reseptör 4 (TLR-4) tarafından tanınır.", "color": "sky"}
    ],
    {
        "id": "prac-enk-007",
        "question": "Gram negatif bakteriyel enfeksiyonlarda endotoksinin (LPS) makrofajlar tarafından tanınmasında ve hücre içine proenflamatuar sinyal iletilmesinde rol oynayan temel reseptör hangisidir?",
        "options": [
            "A) TLR-2",
            "B) TLR-3",
            "C) TLR-4",
            "D) TLR-7",
            "E) TLR-9"
        ],
        "correctAnswer": 2,
        "explanation": "LPS ve lipid A, monosit ve makrofajlarda Toll-like Reseptör 4 (TLR-4) ve koreseptörü MD-2 tarafından tanınır."
    }
))

# S8
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    8,
    "Biyofilm Oluşumu ve Kronik Enfeksiyonlar",
    "Glikokaliks Matriksi, Quorum Sensing ve Antibiyotik Direnci",
    """Biyofilm, mikroorganizmaların canlı veya cansız bir yüzeye yapışarak kendi ürettikleri ekstraselüler polimerik matriks (glikokaliks / balçık tabakası) içerisine gömüldükleri organize bakteri topluluğudur.

**1. Oluşum Aşamaları:**
• Yüzeye geri dönüşümlü tutunma -> Geri dönüşümsüz adezyon -> Ekzopolisakkarit üretimi -> Biyofilm maturasyonu (mantar şeklinde kuleler ve su kanalları) -> Dağılma/yayılma (planktonik forma dönüş).
• **Quorum Sensing (Çoğunluk Algısı):** Bakterilerin salgıladıkları otoindükleyici sinyal molekülleri aracılığıyla popülasyon yoğunluğunu algılayıp gen ekspresyonlarını senkronize etmeleridir.

**2. Klinik Önemi:**
• Yabancı cisim enfeksiyonlarının (üriner kateterler, protez eklemler, santral venöz kateterler, kalp kapakları) %80'inden sorumludur.
• Matriks difüzyon bariyeri oluşturur ve metabolik hız düşer; bu nedenle biyofilm içindeki bakteriler antibiyotiklere planktonik formlarına göre **100-1000 kat daha dirençlidir!**""",
    [
        {"type": "clinical", "badge": "Klinik Kural / Önemli", "text": "Biyofilm yerleşmiş bir yabancı cisim enfeksiyonunda (örn. enfekte protez veya kateter) implant çıkarılmadıkça medikal antibiyotik tedavisi tek başına başarı sağlayamaz!", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu", "text": "Pseudomonas aeruginosa (kistik fibrozis akciğerinde aljinat biyofilmi) ve Staphylococcus epidermidis (protez ve kateterlerde biyofilm) tipik örneklerdir.", "color": "sky"}
    ],
    {
        "id": "prac-enk-008",
        "question": "Bakterilerin biyofilm formu ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
        "options": [
            "A) Biyofilm içerisindeki bakteriler serbest yüzen (planktonik) bakterilere göre antibiyotiklere çok daha duyarlıdır",
            "B) Bakteriler arasındaki koordinasyonu ve biyofilm oluşumunu sağlayan hücreler arası iletişim sistemi 'Quorum Sensing'dir",
            "C) Biyofilm yalnızca Gram pozitif bakteriler tarafından oluşturulabilir",
            "D) Kateter enfeksiyonlarında biyofilm oluşturan en sık etken Streptococcus pneumoniae'dir",
            "E) Biyofilm matriksi tamamen antikorlardan meydana gelen bir konak savunma ürünüdür"
        ],
        "correctAnswer": 1,
        "explanation": "Bakterilerin yoğunluk algılayarak biyofilm oluşturmasını ve gen ifadesini yönetmesini sağlayan moleküler iletişim sistemine 'Quorum Sensing' denir."
    }
))

# S9
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    9,
    "Enfeksiyonların Klinik Seyir Dönemleri",
    "İnkübasyon, Prodrom, Akut Hastalık ve Konvalesans Evreleri",
    """Tipik bir akut enfeksiyon hastalığının klinik seyri dört ana evrede incelenir:

**1. İnkübasyon (Kuluçka) Dönemi:**
• Patojenin konağa girişinden ilk klinik belirti veya bulguların ortaya çıkmasına kadar geçen süredir.
• Süre patojene, inokülüm miktarına ve konak immünitesine göre değişir (Gıda zehirlenmesinde saatler, leprada yıllar).
• Bu dönemde kişi çoğunlukla asemptomatiktir ancak bazı hastalıklarda (örneğin kızamık, suçiçeği) bulaştırıcı olabilir!

**2. Prodromal Dönem:**
• Özgül olmayan (non-spesifik) genel semptomların (halsizlik, hafif ateş, baş ağrısı, iştahsızlık) görüldüğü kısa evredir.

**3. Akut Hastalık (Hastalık / Akme) Dönemi:**
• Hastalığa özgü tipik klinik bulguların (örn. sarılık, tipik döküntü, meninks irritasyon bulguları) zirve yaptığı dönemdir.

**4. Konvalesans (İyileşme) Dönemi:**
• Belirtilerin gerilediği, doku onarımının başladığı ve antikor titresinin yükseldiği evredir.""",
    [
        {"type": "warning", "badge": "Epidemiyoloji Vurgusu", "text": "Hastalık bulaştırıcılığı bazı enfeksiyonlarda henüz inkübasyonun son günlerinde başlar; bu durum salgın kontrolünü zorlaştırır.", "color": "rose"},
        {"type": "exam", "badge": "Komite Klasik Sorusu", "text": "Non-spesifik genel belirtilerin (kırgınlık, hafif ateş) olduğu ve henüz tanı koydurucu spesifik bulguların çıkmadığı evre: Prodrom Dönemi.", "color": "sky"}
    ],
    {
        "id": "prac-enk-009",
        "question": "Bir enfeksiyon hastalığında halsizlik, iştahsızlık ve yaygın kas ağrısı gibi özgül olmayan genel semptomların görüldüğü, ancak hastalığa özgü tipik tablonun henüz yerleşmediği evre aşağıdakilerden hangisidir?",
        "options": [
            "A) İnkübasyon dönemi",
            "B) Prodrom dönemi",
            "C) Akut hastalık (akme) dönemi",
            "D) Konvalesan dönemi",
            "E) Kronikleşme dönemi"
        ],
        "correctAnswer": 1,
        "explanation": "Hastalığa özgü olmayan silik, genel ön belirtilerin görüldüğü evre 'Prodromal Dönem'dir."
    }
))

# S10
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    10,
    "Portörlük (Taşıyıcılık) Tipleri ve Bulaştırıcılık",
    "Asemptomatik, İnkübasyon, Konvalesan ve Kronik Portörler",
    """Klinik olarak hastalık belirtisi göstermediği halde patojen mikroorganizmayı vücudunda barındıran ve çevreye saçarak bulaştıran bireylere 'Taşıyıcı (Portör)' adı verilir.

**Taşıyıcılık Sınıflandırması:**
• **1. Asemptomatik Portör:** Enfeksiyonu tamamen subklinik geçirir; hiçbir zaman belirti vermez ama bulaştırıcıdır (örn. Menengokok taşıyıcılığı).
• **2. İnkübasyon Portörü:** Hastalık belirtileri başlamadan önceki kuluçka evresinde etkeni saçan kişi (örn. Hepatit B, HIV, Kızamık).
• **3. Konvalesan Portör:** Klinik olarak iyileşmiş olmasına rağmen nekahat döneminde etkeni saçmaya devam eden kişi (örn. Kolera, Shigella).
• **4. Kronik Portör:** İyileşmeden sonra etkeni aylarca veya yıllarca saçmayı sürdüren birey. En klasik örnek: **Salmonella Typhi** taşıyıcıları (bakteri safra kesesine yerleşir ve dışkıyla sürekli atılır - Tifo Mary vakası).""",
    [
        {"type": "clinical", "badge": "Klinik Tuzak / Soru Değeri", "text": "Kronik Salmonella Typhi taşıyıcılarında bakteri safra kesesinde kolonize olur ve safra taşları üzerinde biyofilm oluşturur.", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu", "text": "Halk sağlığında en tehlikeli bulaş kaynağı, hasta olduğunu bilmeyen ve toplumda serbestçe dolaşan 'Asemptomatik Portörler'dir.", "color": "sky"}
    ],
    {
        "id": "prac-enk-010",
        "question": "Tifo (Salmonella Typhi) hastalığını geçirdikten sonra asemptomatik kronik taşıyıcı haline gelen bireylerde bakterinin yerleştiği en karakteristik anatomik odak neresidir?",
        "options": [
            "A) Kemik iliği",
            "B) Dalak parankimi",
            "C) Safra kesesi",
            "D) Akciğer alveolleri",
            "E) Tiroid bezi"
        ],
        "correctAnswer": 2,
        "explanation": "Salmonella Typhi kronik taşıyıcılarında bakteri safra kesesinde (özellikle safra taşları üzerinde) süresiz olarak kolonize kalır ve dışkıyla saçılır."
    }
))

# S11-S24 (Populating full remaining slides for Deck 1)
# S11: Nozokomiyal (Hastane) Enfeksiyonları Tanımı (48 saat kuralı)
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    11,
    "Nozokomiyal (Sağlık Hizmeti İlişkili) Enfeksiyonlar",
    "48 Saat Kuralı, Risk Faktörleri ve İnvaziv Girişimler",
    """Hastaneye yatış sırasında inkübasyon döneminde olmayan ve hastaneye yattıktan en az 48-72 saat sonra ortaya çıkan enfeksiyonlara Nozokomiyal Enfeksiyon (Sağlık Hizmeti İlişkili Enfeksiyon) denir.

**Kriterler ve Özellikler:**
• Taburculuk sonrası ilk 10 gün (cerrahi alan enfeksiyonlarında protez yoksa 30 gün, implant varsa 1 yıl) içinde gelişen enfeksiyonlar da nozokomiyal kabul edilir.
• En sık görülen 4 temel nozokomiyal enfeksiyon tipi:
  1. Kateter ilişkili üriner sistem enfeksiyonları (%30-40, en sık)
  2. Ventilatör ilişkili pnömoni (VİP, mortalitesi en yüksek)
  3. Santral venöz kateter ilişkili kan dolaşımı enfeksiyonları
  4. Cerrahi alan enfeksiyonları.""",
    [
        {"type": "warning", "badge": "Sınavın Altın Kuralı / Kırmızı", "text": "Hastaneye yattıktan sonraki İLK 48 SAAT içinde çıkan enfeksiyonlar toplum kökenli kabul edilir!", "color": "rose"},
        {"type": "exam", "badge": "TUS & Komite Sorusu", "text": "Hastanede en sık görülen nozokomiyal enfeksiyon üriner kateter enfeksiyonudur; en ölümcül olanı ise ventilatör ilişkili pnömonidir.", "color": "sky"}
    ],
    {
        "id": "prac-enk-011",
        "question": "Hastaneye yatırılan bir hastada gelişen bir enfeksiyonun 'nozokomiyal (hastane kökenli)' kabul edilebilmesi için yatıştan en az ne kadar süre sonra ortaya çıkması gerekir?",
        "options": [
            "A) 6 saat",
            "B) 12 saat",
            "C) 24 saat",
            "D) 48 saat",
            "E) 7 gün"
        ],
        "correctAnswer": 3,
        "explanation": "Hastaneye yatışta inkübasyon döneminde olmayan ve yatıştan en az 48 saat sonra gelişen enfeksiyonlar sağlık hizmeti ilişkili (nozokomiyal) kabul edilir."
    }
))

# S12: Zoonozlar
deck_enfeksiyon_kavramlar_slides.append(make_slide(
    12,
    "Zoonotik Enfeksiyonlar ve Rezervuarlar",
    "Omurgalı Hayvanlardan İnsana Bulaşan Kritik Enfeksiyonlar",
    """Doğal koşullarda omurgalı hayvanlardan insanlara bulaşan enfeksiyon hastalıklarına 'Zoonoz' denir. İnsanlar çoğu zoonozda 'çıkmaz konak' (dead-end host) durumundadır.

**Önemli Zoonoz Örnekleri:**
• **Bruselloz (Malta Humması):** Çiğ süt ve taze peynir tüketimiyle bulaşır; dalgalı ateş, sakroileit ve terleme yapar.
• **Şarbon (Bacillus anthracis):** Otçul hayvanlardan temas, solunum veya sindirimle bulaşır; ağrısız siyah eskar (kutanöz şarbon).
• **Kuduz (Rabies virüs):** Enfekte hayvan ısırığı ile periferik sinirlerden retrograd aksonal taşınma ile SSS'ye ulaşır; fatal ensefalit.
• **Kırım-Kongo Kanamalı Ateşi (KKKA):** Hyalomma cinsi kenelerle bulaşan Nairovirüs etkeni; trombositopeni ve masif kanamalar.
• **Tularemi (Francisella tularensis):** Kemiriciler, av hayvanları ve kontamine sularla bulaşır.""",
    [
        {"type": "clinical", "badge": "Klinik Tuzak / Önemli", "text": "Zoonotik enfeksiyonların çoğunda insandan insana bulaşma olmaz (Kuduz, Şarbon, Bruselloz çıkmaz konaktır). İstisna: KKKA'da hastane personeline kanla bulaşabilir!", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu", "text": "Brusellozun en tipik laboratuvar bulgusu dalgalı ateşle beraber kemik iliği tutulumu ve lökopeni/pansitopenidir.", "color": "sky"}
    ],
    {
        "id": "prac-enk-012",
        "question": "Aşağıdaki enfeksiyon hastalıklarından hangisi enfekte hayvanların pastörize edilmemiş süt ve süt ürünlerinin (taze peynir) tüketilmesiyle bulaşan klasik bir zoonozdur?",
        "options": [
            "A) Şarbon",
            "B) Bruselloz",
            "C) Kuduz",
            "D) Tetanoz",
            "E) Lejyoner hastalığı"
        ],
        "correctAnswer": 1,
        "explanation": "Bruselloz, enfekte koyun, keçi ve sığırların pastörize edilmemiş süt ve taze köy peynirlerinin tüketilmesiyle bulaşan klasik bir zoonozdur."
    }
))

# S13-S24 (Enfeksiyon temel kavramlar geri kalan slaytlar)
topics_enk = [
    ("Enfeksiyon Kaynakları ve Rezervuarlar", "İnsan, Hayvan ve Çevresel Kaynaklar Arasındaki Epidemiyolojik Farklar", "Rezervuar, patojenin hayatta kaldığı birincil habitatıdır. İnsan kaynaklı patojenler genellikle konağa daha adapte olup kronik seyir gösterebilir.", "İnsan rezervuarlı hastalıkların (örn. Çiçek, Polio) aşıyla eradikasyonu mümkündür; çevresel rezervuarlı (Tetanoz) hastalıklar eradike edilemez!"),
    ("Bulaşma Yolları: Doğrudan ve Dolaylı Bulaş", "Temas, Damlacık, Hava Yolu, Vektör ve Fomit Kavramları", "Doğrudan temas cilt-cilde veya cinsel yolla gerçekleşirken; dolaylı bulaş fomitler (cansız eşyalar), hava veya biyolojik vektörlerle gerçekleşir.", "Damlacık (>5 mikron) yerçekimiyle 1-2 metrede çöker; hava yolu aerosolleri (<5 mikron) saatlerce asılı kalır ve N95 maske gerektirir."),
    ("Konağın İmmün Savunma Mekanizmaları", "Doğal (Doğuştan) Bariyerler ve Edinsel Özgül Yanıt", "Deri epiteli, mide asiditesi, mukosilier klirens, lizozim ve normal flora doğal anatomik bariyerleri oluşturur. Fagositoz ve kompleman hücresel doğal savunmadır.", "Mide asiditesinin antiasitlerle baskılanması Salmonella ve Kolera enfeksiyonu riskini dramatik artırır."),
    ("Fagositoz ve Opsonizasyon Mekanizması", "Nötrofil ve Makrofajların Patojen Yok Etme Adımları", "Fagositoz: Kemotaksis -> Tanıma ve Adezyon -> Yutma (Fagozom) -> Fagozom-Lizozom Füzyonu -> İntraselüler Öldürme (Oksidatif Patlama).", "En güçlü opsoninler IgG antikorunun Fc parçası ve kompleman C3b fragmanıdır."),
    ("Enfeksiyon İmmünopatolojisi ve Sitokin Yanıtı", "Ateş, Akut Faz Reaktanları ve CRP Artışı", "Makrofaj kaynaklı pirojenik sitokinler (IL-1, TNF-alfa, IL-6) hipotalamusta PGE2 sentezini uyararak termostat ayar noktasını yükseltir ve ateşe neden olur.", "Karaciğerden CRP, Prokalsitonin, Fibrinojen ve Ferritin sentezi akut faz yanıtında artar."),
    ("Latent Enfeksiyon ve Reaktivasyon", "Hücre İçinde Sessiz Kalan Virüsler ve İmmünsüpresyon Riski", "Latent enfeksiyonlarda viral genom konak hücresinde kalır ancak aktif viral replikasyon ve klinik bulgu yoktur (örn. HSV duyusal gangliyonlarda, VZV arka kök gangliyonunda).", "İmmünsüpresyonda VZV reaktivasyonu dermatom boyunca ağrılı veziküllerle karakterize Zona (Herpes Zoster) tablosuna yol açar."),
    ("Persistan ve Yavaş Virüs Enfeksiyonları", "Hepatit B, C, HIV ve Prion Hastalıkları Dinamiği", "Akut dönemden sonra etkenin vücuttan tam temizlenemeyip düşük düzeyde çoğalmaya devam ettiği durumlar persistan enfeksiyondur. Prionlar immün yanıt tetiklemeden süngerimsi ensefalopati yapar.", "Prionlar konvansiyonel otoklav ve dezenfeksiyon yöntemlerine olağanüstü dirençlidir."),
    ("Mikrobiyal Genetik Değişimler: Mutasyon ve Rekombinasyon", "Antijenik Sapma (Drift) ve Antijenik Kayma (Shift)", "İnfluenza virüsünde nokta mutasyonları ile oluşan küçük antijenik değişikliklere 'Antijenik Drift' (mevsimsel salgınlar); iki farklı suşun genetik segment değişimiyle oluşan radikal değişikliğe 'Antijenik Shift' (pandemiler) denir.", "Antijenik Shift yalnızca segmented genomu olan İnfluenza A virüsünde görülür; İnfluenza B pandemik shift yapamaz!"),
    ("Antibiyotik Direnç Mekanizmaları", "Enzimatik İnaktivasyon, Hedef Değişimi, Efluks ve Porin Kaybı", "Direnç mekanizmaları: Beta-laktamaz üretimi (enzimatik), PBP2a değişimi (MRSA hedef modifikasyonu), membran porinlerinin kapatılması (Pseudomonas) ve aktif pompa sistemleri (Efluks).", "MRSA direnci mecA geninin kodladığı PBP2a proteininden kaynaklanır ve tüm klasik beta-laktamları etkisiz kılar."),
    ("Dezenfeksiyon, Antisepsi ve Sterilizasyon", "Tanımlar, Seviyeler ve Uygulama Alanları", "Sterilizasyon sporlar dahil tüm mikroorganizmaların yok edilmesidir. Dezenfeksiyon cansız yüzeylerdeki patojenlerin eliminasyonudur. Antisepsi canlı dokulara uygulanan kimyasal temizliktir.", "Canlı dokuya dezenfektan uygulanmaz, antiseptik uygulanır! Otoklav standart sterilizasyon aracıdır (121°C'de 15-20 dk)."),
    ("Enfeksiyon Hastalıklarında Laboratuvar Tanı Yöntemleri", "Direkt Mikroskopi, Kültür, Seroloji ve Moleküler Testler (PCR)", "Tanı hiyerarşisi: 1. Gram ve Giemsa boyama (hızlı), 2. Kültür ve antibiyogram (altın standart), 3. Seroloji (IgM erken, IgG geç), 4. Moleküler yöntemler (PCR, hızlı ve sensitif).", "Tek bir serum örneğinde yüksek IgM pozitifliği taze/akut enfeksiyonu; çift serum örneğinde IgG titresinde 4 kat artış serokonversiyonu kanıtlar."),
    ("Enfeksiyon Hastalıklarında Tedavi İlkeleri ve Akılcı Antibiyotik", "Ampirik Tedaviden Hedefe Yönelik Tedaviye Geçiş", "Acil durumlarda (menenjit, sepsis) kültür alındıktan hemen sonra ampirik geniş spektrumlu tedavi başlanır; etken üreyip antibiyogram çıktığında spektrum derhal daraltılır (de-eskalasyon).", "Kültür alınmadan antibiyotik başlanması üreme şansını yok eder ve tanısal körlüğe yol açar.")
]

for idx, (t, sub, narr, spot) in enumerate(topics_enk, start=13):
    deck_enfeksiyon_kavramlar_slides.append(make_slide(
        idx,
        t,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Amfi Spotu / Kırmızı", "text": spot, "color": "rose"},
            {"type": "exam", "badge": "Komite Bilgisi / Mavi", "text": f"{t} konusunda amfide hocanın özellikle vurguladığı çekirdek kazanım noktasıdır.", "color": "sky"}
        ],
        {
            "id": f"prac-enk-{idx:03d}",
            "question": f"{t} bağlamında aşağıdakilerden hangisi en doğru klinik yaklaşımdır?",
            "options": [
                f"A) {t} sürecinde ilk basamak daima ampirik müdahaledir",
                f"B) {spot}",
                f"C) Tüm mikroorganizmalar {t} karşısında tamamen savunmasızdır",
                f"D) Bu süreç yalnızca virüsler için geçerlidir",
                f"E) Tedaviye yanıt alınamazsa teşhis otomatik olarak dışlanır"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru yanıt: {spot}"
        }
    ))

print(f"Deck 1 (Enfeksiyon Temel Kavramlar) üretildi: {len(deck_enfeksiyon_kavramlar_slides)} slayt")

# ==============================================================================
# DECK 2: learn-enfeksiyon-epidemiyoloji (24 Slayt)
# ==============================================================================
deck_enfeksiyon_epidemiyoloji_slides = []
topics_epi = [
    ("Enfeksiyon Epidemiyolojisine Giriş ve Tarihsel Boyut", "Kitlesel Salgınlar, Veba, Kolera ve Medeniyetlerin Çöküşü", "Epidemiyoloji toplumda hastalıkların dağılımını, sıklığını ve belirleyicilerini inceleyen bilim dalıdır. Enfeksiyon epidemiyolojisi ise etken, konak ve çevre üçgeninde bulaş dinamiğini araştırır.", "Enfeksiyon epidemiyolojisinde birincil amaç yalnızca tek hastayı tedavi etmek değil, tüm toplumdaki bulaş zincirini kırmaktır."),
    ("Epidemiyolojik Dağılım Tipleri: Endemi, Epidemi, Pandemi", "Hastalık Görülme Sıklığının Coğrafi ve Zamansal Sınıflandırması", "Endemi: Bir hastalığın belirli bir bölgede veya toplumda beklenen normal sıklıkta sürekli görülmesidir. Epidemi (Salgın): Beklenen vaka sayısının belirgin şekilde üzerine çıkılmasıdır. Pandemi: Kıtalararası küresel yayılımdır.", "Grip kış aylarında endemik iken, yeni bir antijenik shift ile küresel yayıldığında pandemi adını alır."),
    ("Sporadi ve Hiperendemi Kavramları", "Tek Tük Vakalar ve Yüksek Taban Çizgisi Dinamikleri", "Sporadik: Birbirinden zamansal ve mekansal olarak bağımsız, tek tük, düzensiz aralıklarla görülen vakalardır (örn. kuduz vakaları). Hiperendemi: Hastalığın toplumda sürekli olarak çok yüksek düzeyde seyretmesidir.", "Sporadik vakalar salgın oluşturmaz ancak rezervuarın varlığını kanıtlar."),
    ("Temel Üreme Katsayısı (R0) ve Dinamiği", "Bulaştırıcılığın Matematiksel Ölçüsü ve Salgın Eşiği", "R0 (Basic Reproduction Number): Tamamen duyarlı bir popülasyonda enfekte bir bireyin doğrudan enfekte ettiği ortalama ikincil vaka sayısıdır.", "R0 > 1 ise vaka sayısı katlanarak artar ve salgın büyür. R0 = 1 ise hastalık endemik kalır. R0 < 1 ise enfeksiyon sönümlenir ve yok olur."),
    ("Sürü Bağışıklığı Eşiği (Herd Immunity Threshold)", "Toplum Bağışıklığının Matematiksel Formülü: HIT = 1 - (1 / R0)", "Sürü bağışıklığı, toplumun belirli bir oranı aşı veya geçirilmiş enfeksiyonla bağışık hale geldiğinde, bağışık olmayan bireylerin de korunmasıdır. Eşik formülü: HIT = 1 - (1 / R0).", "Kızamık R0 değeri 12-18 olan en bulaşıcı virüstür; bu nedenle kızamıkta sürü bağışıklığı için toplumun en az %95'i aşılanmalıdır!"),
    ("İnkübasyon Süresi ve Epidemiyolojik Önemi", "Karantina Süresinin Belirlenmesi ve Kaynak Araştırması", "İnkübasyon süresi karantina süresinin sınırlarını çizer. Temaslı bireyler maksimum inkübasyon süresi boyunca izole veya karantinaya alınır.", "Bir temaslının karantina süresi, o hastalığın 'en uzun (maksimum) inkübasyon süresi' kadar olmalıdır."),
    ("Bulaştırıcılık Süresi ve İndeks Vaka", "Primer Vaka, İndeks Vaka ve Sekonder Atak Hızı", "İndeks Vaka: Sağlık otoritesinin dikkatini çeken, kayıtlara geçen ilk vakadır (Primer vaka gerçek ilk bulaşandır ancak her zaman saptanamayabilir).", "Sekonder Atak Hızı: İndeks vaka ile temas eden duyarlı kişiler arasında hastalığı kapanların oranıdır (bulaşıcılık gücünü gösterir)."),
    ("Bulaşma Yolları 1: Doğrudan ve Dolaylı Temas", "El Hijyeni, Fomitler ve Nozokomiyal Aktarım", "Temas yolu hastanelerde en sık görülen bulaş biçimidir. Sağlık çalışanlarının kontamine elleri patojenlerin hastadan hastaya taşınmasında 1 numaralı araçtır.", "Nozokomiyal enfeksiyonların önlenmesinde en ucuz, en basit ve en etkili yöntem el hijyenidir."),
    ("Bulaşma Yolları 2: Damlacık ve Aerosol Ayrımı", "5 Mikron Sınırı, Havalandırma ve İzolasyon Önlemleri", "Damlacık: >5 mikron partiküller; öksürme/hapşırma ile 1-2 metre mesafeye fırlar ve çöker (Meningokok, İnfluenza). Hava yolu (Aerosol): <5 mikron partiküller; havada asılı kalır, mesafeden bağımsız yayılır (Tüberküloz, Kızamık, Suçiçeği).", "Aerosol bulaşında standart cerrahi maske yetersizdir; negatif basınçlı oda ve N95/FFP2 maske zorunludur!"),
    ("Bulaşma Yolları 3: Vektör Aracılı Bulaş", "Biyolojik ve Mekanik Vektörlerin Epidemiyolojik Farkları", "Mekanik Vektör: Etken vektörün vücudunda çoğalmaz veya evrim geçirmez, sadece ayakları/gövdesi ile taşınır (Karasinek ve amip kistleri). Biyolojik Vektör: Etken vektörün vücudunda zorunlu gelişim veya çoğalma evresi geçirir (Anofel sivrisineği ve Plazmodium).", "Biyolojik vektörün ortadan kaldırılması enfeksiyonun yaşam döngüsünü tamamen kırar."),
    ("Bulaşma Yolları 4: Su ve Gıda Kökenli (Fekal-Oral) Salgınlar", "Ortak Kaynaklı Salgın Eğrileri ve Su Klorlaması", "Ortak bir kaynaktan (kontamine su şebekesi, bozulmuş düğün yemeği) kısa sürede çok sayıda insanın enfekte olması ortak kaynaklı salgındır. Salgın eğrisi aniden dik yükselir ve zirve yapar.", "Fekal-oral salgınlarda en etkin halk sağlığı müdahalesi su kaynaklarının klorlanması ve gıda hijyenidir."),
    ("Salgın İncelemesi Basamakları", "Salgın Tanısından Kontrol Önlemlerine 10 Temel Adım", "1. Salgının varlığının doğrulanması, 2. Tanının doğrulanması, 3. Vaka tanımının yapılması, 4. Vakaların bulunması ve kaydedilmesi, 5. Tanımlayıcı epidemiyoloji (Kişi, Yer, Zaman analizi), 6. Hipotez geliştirme, 7. Analitik çalışmalarla test etme, 8. Kontrol önlemlerinin uygulanması.", "Salgın kontrol önlemleri analitik çalışmaların bitmesi beklenmeden, şüphelenilen ilk andan itibaren hemen başlatılmalıdır!"),
    ("Epidemik Eğriler (Epi-Curve) ve Yorumlanması", "Nokta Kaynaklı, Sürekli Kaynaklı ve Kişiden Kişiye Yayılan Eğriler", "Nokta kaynaklı salgında tüm vakalar bir inkübasyon süresi içinde dik bir tepe yapar. Kişiden kişiye yayılan (propaje) salgında ise aralıklı dalgalar ve basamaklı yükselişler görülür.", "Grip ve kızamık salgınları klasik propaje (dalgalı ve yayılan) epidemik eğri sergiler."),
    ("Filyasyon ve Temaslı Takibi", "Bulaş Haritalandırması ve Saha Epidemiyolojisi", "Filyasyon, bulaşıcı hastalık tanısı konan kişinin temas ettiği tüm duyarlı bireyleri geriye ve ileriye dönük tarayarak bulma ve izole etme çalışmasıdır.", "Filyasyonun amacı hastalığın toplumda serbest dolaşımını ve ikincil bulaşları engellemektir."),
    ("İzolasyon ve Karantina Arasındaki Keskin Fark", "Hasta Birey ile Sağlam Temaslının Ayrımı", "İzolasyon (Soyutlama): Tanı konmuş HASTA bireyin bulaştırıcılık süresi boyunca sağlıklı insanlardan ayrılmasıdır. Karantina: Bulaşıcı bir hastalıkla TEMAS ETMİŞ ancak henüz hasta olmamış SAĞLAM bireylerin hareketlerinin sınırlandırılmasıdır.", "İzolasyon hastaya, karantina sağlam temaslıya uygulanır; komitelerde bu iki kavramın zıtlığı mutlaka sorulur!"),
    ("Sürveyans Sistemleri: Aktif ve Pasif Sürveyans", "Bildirimi Zorunlu Bulaşıcı Hastalıklar Ağı", "Pasif Sürveyans: Sağlık kuruluşlarının rutin olarak vakaları merkeze bildirmesidir (en yaygın ama eksik bildirim riski yüksek). Aktif Sürveyans: Sağlık otoritesinin bizzat sahaya inerek, laboratuvarları ve hastaneleri dolaşarak vaka aramasıdır.", "Salgın durumlarında pasif sürveyans yetersiz kalır; derhal aktif sürveyansa geçilir."),
    ("Bildirimi Zorunlu Bulaşıcı Hastalıklar Grupları", "A, B, C ve D Grupları Bildirim Protokolleri", "Kuduz, Şarbon, Kolera, Kızamık, Polio, Sıtma gibi hastalıklar halk sağlığı acil durumu oluşturduğu için derhal (ilk 24 saatte) bildirimi zorunlu hastalıklardır.", "Uluslararası Sağlık Tüzüğü (IHR) gereğince Çiçek, Polio, İnsan İnfluenzası (yeni alt tip) ve SARS Dünya Sağlık Örgütü'ne anında bildirilmelidir."),
    ("Gelişmekte Olan ve Yeniden Önem Kazanan Enfeksiyonlar", "Emerging and Re-emerging Infections Dinamikleri", "Yeniden önem kazanan (re-emerging) enfeksiyonlar: Tüberküloz (MDR-TB), Difteri, Kızamık (aşı reddi nedeniyle). Yeni ortaya çıkan (emerging): COVID-19, MERS, SARS, Ebola.", "Aşı karşıtlığı ve aşı kararsızlığı, eliminasyon aşamasına gelmiş kızamık gibi re-emerging salgınların temel nedenidir."),
    ("Hastane Epidemiyolojisi ve İnfeksiyon Kontrol Komitesi", "Sürveyans Hızları ve El Hijyeni Uyum Oranları", "Hastanelerde enfeksiyon kontrol hekimi ve hemşiresinden oluşan komite, antibiyotik direnç profillerini ve invaziv alet kullanım oranlarını izler.", "Ventilatör ilişkili pnömoni ve santral hat enfeksiyonu sürveyansında '1000 alet günü' paydası kullanılır."),
    ("Genişlemiş Bağışıklama Programı (GBP)", "Türkiye Ulusal Aşı Takvimi ve Aşı ile Korunabilir Hastalıklar", "Türkiye'de çocukluk çağında 13 enfeksiyon etkenine karşı (BCG, DaBT-İPA-Hib, KKK, KPA, Suçiçeği, HepB, HepA) ücretsiz rutin aşılama uygulanır.", "Canlı atenüe aşılar (KKK, BCG, Suçiçeği) konjenital veya edinsel immün yetmezliği olanlara ve gebelere kontrendikedir!"),
    ("Soğuk Zincir Yönetimi ve Aşı Güvenliği", "+2°C ile +8°C Arası Sıcaklık İzlemi", "Aşıların üretimden uygulama anına kadar biyolojik potensini kaybetmemesi için +2°C ile +8°C arasında korunması zorunludur. Dondurulmaması gereken aşılar (DTP, HepB) donarsa 'çalkalama testi' yapılır.", "Çalkalama testinde aşı bulanıklığı hızla dibe çöküyorsa aşı donmuş ve bozulmuştur; kesinlikle imha edilir!"),
    ("Seyahat Sağlığı ve Uluslararası Bulaş Dinamiği", "Sarıhumma, Menengokok Aşısı ve Profilaktik Önlemler", "Sarıhumma endemik bölgelerine seyahatte uluslararası aşı sertifikası zorunludur. Hac ve umre ziyaretçilerine kuadrivalan meningokok aşısı şart koşulur.", "Tropikal bölgelere seyahatte sıtma profilaksisi seyahatten önce başlatılmalı ve dönüşten sonra da sürdürülmelidir."),
    ("Biyoterrorizm ve Kategori A Biyolojik Ajanlar", "Şarbon, Çiçek, Veba, Botulizm, Tularemi ve Viral Kanamalı Ateşler", "Kategori A ajanlar: Kolayca yayılabilen, insandan insana bulaşabilen, yüksek mortaliteye sahip ve kitlesel paniğe yol açan en tehlikeli biyolojik silahlardır.", "Kategori A biyolojik ajanlar: Bacillus anthracis (Şarbon), Variola major (Çiçek), Yersinia pestis (Veba), Clostridium botulinum (Botulizm)."),
    ("Epidemiyolojik Araştırma Yöntemleri ve Enfeksiyon Çalışmaları", "Kohort, Vaka-Kontrol ve Salgın Atak Hızı Analizleri", "Gıda zehirlenmesi salgınlarında tüketilen her bir gıda maddesi için 'gıda atak hızı' hesaplanır. Atak hızı farkı en yüksek olan gıda etken kaynak olarak belirlenir.", "Relatif Risk (RR) kohort çalışmalarında, Odds Oranı (OR) vaka-kontrol çalışmalarında hesaplanır.")
]

for idx, (t, sub, narr, spot) in enumerate(topics_epi, start=1):
    deck_enfeksiyon_epidemiyoloji_slides.append(make_slide(
        idx,
        t,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Epidemiyoloji Kuralı / Kırmızı", "text": spot, "color": "rose"},
            {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": f"{t} konusunun amfi sınavlarında en çok sorgulanan ayırt edici mekanizmasıdır.", "color": "sky"}
        ],
        {
            "id": f"prac-epi-{idx:03d}",
            "question": f"{t} ile ilgili aşağıdaki epidemiyolojik ifadelerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {t} yalnızca gelişmiş ülkelerde araştırılır",
                f"B) {spot}",
                f"C) Bu süreçte temel üreme katsayısı hiçbir rol oynamaz",
                f"D) Tüm salgınlar nokta kaynaklıdır ve insandan insana yayılmaz",
                f"E) Karantina yalnızca hasta kişilere uygulanırken, izolasyon sağlam kişilere uygulanır"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru yanıt: {spot}"
        }
    ))

print(f"Deck 2 (Enfeksiyon Epidemiyolojisi) üretildi: {len(deck_enfeksiyon_epidemiyoloji_slides)} slayt")

# ==============================================================================
# DECK 3: learn-halk-sagligi-tarihcesi-ve (8 slayttan 24 slayta genişletme)
# ==============================================================================
deck_halk_sagligi_slides = []
topics_hs = [
    ("Halk Sağlığı Tanımı ve Temel Felsefesi", "Winslow (1920) Tanımı ve Toplumun Sağlığını Koruma Sanatı", "Halk sağlığı; organize edilmiş toplum çalışmaları sonunda çevre sağlık koşullarını düzelterek, bulaşıcı hastalıkları önleyerek, bireylere sağlık bilgisi vererek, erken tanı ve tedaviyi sağlayarak yaşamı uzatan, beden ve ruh sağlığını geliştiren bir bilim ve sanattır (C.E.A. Winslow, 1920).", "Halk sağlığında odak tek tek bireyler değil, 'tüm toplum' ve 'koruyucu hekimlik'tir."),
    ("İlk Çağlarda Sağlık Anlayışı ve Mezopotamya", "Gılgamış Destanı, Hammurabi Kanunları ve Hijyen Kuralları", "MÖ 3000'lerde Gılgamış ölümsüzlüğü aramıştır. Hammurabi Kanunları hekimlerin sorumluluklarını ve tıbbi uygulamaları yasal kurallara bağlayan tarihteki ilk metinlerdendir.", "Hammurabi Kanunları tıbbi kusurlara cezai yaptırımlar getirerek hekimlik pratiğini denetleyen ilk yasal belgedir."),
    ("Eski Mısır ve Hijyen Pratikleri", "Drenaj Kanalları, Beslenme Hijyeni ve Mumyalama Tıbbı", "Mısırlılar paraziter ve bulaşıcı hastalıklardan korunmak için beden temizliğine, içme suyu kaynaklarının korunmasına ve tahıl depolarının hijyenine büyük önem vermişlerdir.", "Mumyalama teknikleri insan anatomisinin ve patolojisinin ilk kez sistematik gözlemlenmesini sağlamıştır."),
    ("Eski Yunan ve Hipokratik Tıp", "Dört Sıvı (Hümoral Patoloji) Teorisi ve Çevre Sağlığı", "Hipokrat, hastalıkları doğaüstü güçlerden ayırıp biyolojik ve çevresel nedenlere dayandıran ilk hekimdir. 'Hava, Su ve Mekanlar Üzerine' adlı eseri tarihin ilk çevre sağlığı ve epidemiyoloji kitabıdır.", "Hipokrat'ın Dört Hümor Teorisi: Kan, Balgam, Sarı Safra, Kara Safra dengesizliği hastalık oluşturur."),
    ("Roma İmparatorluğu ve Kamu Sağlığı Mühendisliği", "Su Kemerleri (Akuadükler), Hamamlar ve Kloaka Maksima", "Romalılar bataklıkların sıtma yaptığını fark etmiş, şehirlere kilometrelerce öteden temiz su getiren akuadükler ve kanalizasyon sistemi (Cloaca Maxima) inşa etmişlerdir.", "Romalılar tedavi edici hekimlikten ziyade hijyen altyapısı ve kamu sağlığı mühendisliği ile öne çıkmıştır."),
    ("Ortaçağ Avrupası ve Büyük Salgınlar", "Kara Veba (Yersinia pestis), Cüzzam (Lepra) ve Karantina Doğuşu", "1347-1351 yılları arasında Avrupa nüfusunun üçte birini yok eden Kara Veba, hijyenin çöktüğü Ortaçağ'da patlak vermiştir. Venedik'te gemilerin limana girmeden 40 gün açıkta bekletilmesiyle 'Karantina' (quaranta giorni) terimi doğmuştur.", "Karantina terimi Venedik İtalyancasında 40 gün anlamına gelen 'quaranta' kelimesinden türemiştir."),
    ("Rönesans ve Modern Tıbbın Şafağı", "Fracastoro (Bulaş Teorisi), Vesalius (Anatomi) ve Ramazzini (İş Sağlığı)", "Girolamo Fracastoro (1546) enfeksiyonların gözle görülmeyen tohumcuklarla (seminaria) insandan insana bulaştığını savunmuştur. Bernardino Ramazzini ise ilk iş sağlığı kitabını yazmıştır.", "Bernardino Ramazzini: Hastaya 'Ne iş yapıyorsun?' sorusunu soran ilk hekim olup İş Sağlığının babasıdır."),
    ("John Snow ve 1854 Londra Kolera Salgını", "Modern Epidemiyolojinin Doğuşu ve Broad Street Tulumbası", "Dr. John Snow, koleranın havadaki kötü kokulardan (Miasma) değil, suyla bulaştığını harita üzerinde vakaları işaretleyerek kanıtlamış ve Broad Street'teki tulumbanın kolunu söktürerek salgını durdurmuştur.", "John Snow, etken henüz mikroskopta bilinmiyorken epidemiyolojik yöntemle salgını durduran modern epidemiyolojinin babasıdır."),
    ("Sanitasyon Hareketi ve Edwin Chadwick", "Sosyal Reformlar, Yoksulluk ve 1848 İngiliz Kamu Sağlığı Yasası", "Edwin Chadwick, İngiltere'de işçi sınıfının sağlıksız yaşam koşullarını raporlamış ve temiz su temini, kanalizasyon yapımı ile ortalama yaşam süresinin uzatılabileceğini savunmuştur.", "1848 Public Health Act (Kamu Sağlığı Yasası), modern devletin vatandaşın sağlığını koruma yükümlülüğünü kabul ettiği ilk yasadır."),
    ("Bakteriyoloji Çağı: Pasteur ve Koch", "Spontan Jenerasyonun Çöküşü, Mikrop Teorisi ve Koch Postulatları", "Louis Pasteur fermantasyon ve kuduza karşı aşı geliştirmiş; Robert Koch ise Şarbon, Tüberküloz ve Kolera basillerini izole ederek bir etkenin hastalık yaptığını kanıtlayan 4 kuralı (Koch Postulatları) tanımlamıştır.", "Koch Postulatları: Etken her hastada bulunmalı, saf kültürde üretilmeli, sağlıklı deneğe verildiğinde hastalık yapmalı ve tekrar izole edilmelidir."),
    ("20. Yüzyıl Başları ve Winslow'dan WHO'ya", "1948 Dünya Sağlık Örgütü Kuruluşu ve Sağlık Tanımı", "Dünya Sağlık Örgütü (WHO) 7 Nisan 1948'de kurulmuştur. Sağlık tanımı: 'Sağlık; yalnızca hastalık veya sakatlığın olmayışı değil, bedence, ruhça ve sosyal yönden tam bir iyilik halidir.'", "WHO'nun sağlık tanımı sosyal ve ruhsal boyutları da kapsayan bütüncül (holistik) bir tanımdır."),
    ("Alma-Ata Bildirgesi (1978) ve Temel Sağlık Hizmetleri", "'Herkes İçin Sağlık 2000' Hedefi ve TSH Prensipleri", "Kazakistan'ın Alma-Ata şehrinde toplanan konferansta, pahalı hastane tıbbı yerine eşitlikçi, toplum katılımlı, koruyucu odaklı 'Temel Sağlık Hizmetleri (TSH)' modeli kabul edilmiştir.", "Temel Sağlık Hizmetlerinin ana felsefesi: Sağlıkta eşitlik, toplum katılımı, sektörler arası işbirliği ve uygun teknolojidir."),
    ("Ottawa Şartı (1986) ve Sağlığın Geliştirilmesi", "Health Promotion: Sağlığı Etkileyen Sosyal Belirleyiciler", "Ottawa Konferansı, sağlığı sadece korumayı değil, bireylerin kendi sağlıkları üzerindeki kontrolünü artırmayı (Sağlığı Geliştirme - Health Promotion) hedeflemiştir.", "Sağlığın ön koşulları: Barış, barınma, eğitim, gıda, gelir, sürdürülebilir çevre ve sosyal adalettir."),
    ("Osmanlı Döneminde Sağlık Hizmetleri", "Darüşşifalar, Karantina Teşkilatı (1838) ve Mekteb-i Tıbbiye-i Şahane", "Osmanlı'da darüşşifalar vakıf sistemiyle hizmet vermiştir. II. Mahmud döneminde 1838'de Meclis-i Tahaffuz (Karantina İdaresi) kurulmuş ve modern tıp eğitimi 14 Mart 1839'da Mekteb-i Tıbbiye ile başlamıştır.", "14 Mart Tıp Bayramı, 1839'da Mekteb-i Tıbbiye-i Şahane'nin açılış gününden gelmektedir."),
    ("Cumhuriyet Dönemi ve Dr. Refik Saydam", "Hıfzıssıhha Enstitüsü, Trahom ve Verem Savaş Seferberlikleri", "Cumhuriyetin ilk Sağlık Bakanı Dr. Refik Saydam, koruyucu hekimliği devlet politikası haline getirmiş; 1928'de Hıfzıssıhha Enstitüsü'nü kurarak serum ve aşı üretimini Türkiye'de başlatmıştır.", "1930 tarihli 1593 sayılı Umumi Hıfzıssıhha Kanunu, bugün dahi halk sağlığının temel yasal omurgasını oluşturur."),
    ("224 Sayılı Sosyalizasyon Kanunu (1961)", "Prof. Dr. Nusret Fişek ve Sağlık Ocakları Devrimi", "1961 yılında çıkarılan 224 sayılı 'Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun' ile kırsal alanlardan başlayarak tüm Türkiye Sağlık Ocakları ağıyla örülmüştür.", "Nusret Fişek modelinde: Entegre sağlık hizmeti (koruyucu + tedavi edici aynı çatı altında), bölge tabanlı çalışma ve sevk zinciri esastır."),
    ("Sağlıkta Dönüşüm Programı ve Aile Hekimliği", "2003 Sonrası Reformlar ve Birinci Basamağın Yeniden Yapılanması", "2003 yılında başlatılan Sağlıkta Dönüşüm Programı ile Sağlık Ocakları modeli yerine kişiye yönelik koruyucu ve birinci basamak tedavi hizmeti veren 'Aile Hekimliği' sistemine geçilmiştir.", "Aile hekimliğinde hekim başına kayıtlı nüfus esastır; çevre sağlığı ve adli tıp gibi hizmetler Toplum Sağlığı Merkezlerine (TSM/İSM) devredilmiştir."),
    ("Koruyucu Hekimlik Basamakları: Primordial ve Primer Koruma", "Risk Faktörlerinin Oluşmasını Engelleme ve Aşılama", "Primordial Koruma: Toplumda risk faktörlerinin henüz ortaya çıkmasını engellemeye yönelik makro politikalar (örn. tütün vergileri, hava kirliliği yasaları). Primer Koruma: Risk faktörü olan bireyde hastalığın çıkmasını önleme (örn. aşılama, sigara bıraktırma).", "Aşılama ve kemoprofilaksi en klasik Primer Koruma örnekleridir."),
    ("Sekonder Koruma: Erken Tanı ve Taramalar", "Kanser Taramaları, Yenidoğan Taramaları ve Tedavi", "Hastalığın asemptomatik veya subklinik evresinde yakalanarak ilerlemesinin durdurulmasıdır. KETEM kanser taramaları (Mamografi, Pap smear, GGK) ve topuk kanı taraması sekonder korumadır.", "Tarama testleri (Screening) ve asemptomatik evrede erken tanı sekonder korumanın temelidir."),
    ("Tersiyer ve Kuaterner Koruma", "Rehabilitasyon, Sakatlık Önleme ve Aşırı Tıbbileştirmeyi Engelleme", "Tersiyer Koruma: Klinik tablo yerleştikten sonra komplikasyonları ve kalıcı sakatlıkları önleme, rehabilitasyon sağlama (örn. diyabetlide ayak bakımı, inme sonrası fizyoterapi). Kuaterner Koruma: Hastayı aşırı tıbbi müdahaleden, gereksiz tetkik ve polifarmasiden koruma.", "Kuaterner korumanın ana ilkesi Hipokrat'ın 'Primum non nocere' (Önce zarar verme) prensibidir."),
    ("Sağlık Düzeyi Göstergeleri: Bebek ve Anne Ölüm Hızları", "Bir Toplumun Gelişmişlik Düzeyinin En Hassas Aynası", "Bebek Ölüm Hızı (BÖH): Bir yılda 1 yaşını doldurmadan ölen bebeklerin canlı doğum sayısına oranıdır (Binde olarak ifade edilir). Anne Ölüm Oranı (AÖO): Yüz binde canlı doğum başına gebelik/doğum nedenli anne ölümleridir.", "Bebek Ölüm Hızı, bir ülkenin sosyoekonomik ve sağlık gelişmişlik düzeyini gösteren en hassas göstergedir."),
    ("Halk Sağlığında Çevre ve İş Sağlığı Boyutu", "Hava, Su, Katı Atıklar ve Meslek Hastalıkları", "Çevre sağlığı biyolojik, kimyasal ve fiziksel dış etkenlerin insan sağlığı üzerindeki olumsuz etkilerini kontrol altına alır. Temiz su temini ve katı atık yönetimi kolera, tifo gibi salgınları kökten önler.", "Meslek hastalıkları doğrudan çalışma ortamındaki fiziksel/kimyasal/biyolojik maruziyet sonucu gelişen ve %100 önlenebilir hastalıklardır."),
    ("Afetlerde Halk Sağlığı Yönetimi", "Deprem, Sel ve Kriz Dönemlerinde Çadırkent Hijyeni ve Salgın Kontrolü", "Afetlerde halk sağlığının ilk önceliği: Güvenli içme suyu temini, geçici barınma hijyeni, katı/sıvı atıkların bertarafı ve salgın gözetimidir (sürveyans).", "Afet sonrası ilk haftalarda en sık görülen salgınlar fekal-oral (ishal) ve solunum yolu enfeksiyonlarıdır."),
    ("21. Yüzyılda Küresel Halk Sağlığı Sorunları", "Bulaşıcı Olmayan Kronik Hastalıklar, Yaşlanan Nüfus ve İklim Krizi", "Günümüzde ölüm nedenlerinin %70'inden fazlası bulaşıcı olmayan hastalıklardır (Kardiyovasküler, Kanser, Diyabet, KOAH). İklim krizi ve küresel ısınma ise vektör kaynaklı hastalıkların kuzeye yayılmasına yol açmaktadır.", "Bulaşıcı olmayan kronik hastalıkların ortak önlenebilir 4 risk faktörü: Tütün, sağlıksız beslenme, hareketsizlik ve alkoldür.")
]

for idx, (t, sub, narr, spot) in enumerate(topics_hs, start=1):
    deck_halk_sagligi_slides.append(make_slide(
        idx,
        t,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Halk Sağlığı İlkesi / Kırmızı", "text": spot, "color": "rose"},
            {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": f"{t} konusunun tıp fakültesi komite sınavlarında en sık sorulan soru eksenidir.", "color": "sky"}
        ],
        {
            "id": f"prac-hs-{idx:03d}",
            "question": f"{t} kapsamında aşağıdakilerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {t} yalnızca bireysel cerrahi tedavileri kapsar",
                f"B) {spot}",
                f"C) Koruyucu hekimlik sağlık harcamalarını artırır ve gereksizdir",
                f"D) Bu kavram tarihte ilk kez 21. yüzyılda ortaya çıkmıştır",
                f"E) Bebek ölüm hızı bir toplumun gelişmişliği ile hiçbir korelasyon göstermez"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru yanıt: {spot}"
        }
    ))

print(f"Deck 3 (Halk Sağlığı Tarihçesi) genişletildi: {len(deck_halk_sagligi_slides)} slayt")

# ==============================================================================
# DECK 4: learn-uriner-sistem-enfeksiyonlari-epidemiyoloji (24 Slayt)
# ==============================================================================
deck_use_epi_slides = []
topics_use = [
    ("Üriner Sistem Enfeksiyonlarının Tanımı ve Sınıflaması", "Ürotelyumun Bakteriyel İnvazyonu, Anatomik ve Klinik Ayrım", "Üriner Sistem Enfeksiyonu (ÜSE), patojen mikroorganizmaların idrar yollarına yerleşmesi, çoğalması ve ürotelyumda enflamatuar doku yanıtı oluşturmasıdır. Anatomik olarak Alt ÜSE (Sistit, Üretrit, Prostatit) ve Üst ÜSE (Piyelonefrit) olarak ikiye ayrılır.", "Alt ÜSE'de sistemik bulgu (ateş, titreme) yokken; Üst ÜSE'de (Piyelonefrit) yüksek ateş, yan ağrısı ve kostovertebral açı hassasiyeti (KVAH) esastır."),
    ("Bakteriüri ve Piyüri Tanımları", "Lökosit Esteraz, Santrifüjsüz İdrar İncelemesi ve Yalancı Pozitiflikler", "Bakteriüri: İdrarda bakteri bulunmasıdır. Piyüri: İdrarda lökosit varlığıdır (Santrifüj edilmemiş idrarda milimetreküpte $\ge 10$ lökosit veya santrifüjlü idrarda büyük büyütme alanında $>5$ lökosit).", "Piyüri tek başına enfeksiyon kanıtı değildir (steril piyüri olabilir); ancak semptomatik ÜSE'de piyüri olmaması tanıyı ciddi şekilde sorgulatır!"),
    ("İdrar Kültüründe Anlamlı Bakteriüri Eşikleri (Kass Kriterleri)", "Orta Akım, Kateter ve Suprapubik Aspirasyon Eşikleri", "Kass Kriterleri: Asemptomatik kadınlarda 2 ardışık orta akım idrarında $\ge 10^5$ cfu/mL aynı tür bakteri; Akut sistitli kadında koliform bakteriler için $\ge 10^2$ cfu/mL; Erkeklerde $\ge 10^3$ cfu/mL; Suprapubik aspirasyonda ise $>0$ (HERHANGİ BİR ÜREME) anlamlıdır!", "Suprapubik mesane aspirasyonunda üreyen TEK BİR bakteri kolonisi dahi kesin anlamlı kabul edilir!"),
    ("Asemptomatik Bakteriüri (ASB) ve Tedavi Endikasyonları", "Gereksiz Antibiyotik Tedavisinin Önlenmesi ve 2 Kesin Endikasyon", "ASB: Üriner yakınması olmayan bireyin idrar kültüründe $\ge 10^5$ cfu/mL bakteri üremesidir. Çoğu hastada (yaşlılar, diyabetikler, spinal yaralanmalılar) tedavi EDİLMEZ!", "ASB'nin kesin tedavi edilmesi gereken 2 mutlak durumu: 1. GEBELER, 2. Kanama riski olan mukoza invaziv ürolojik girişim yapılacak hastalar."),
    ("Komplike vs Komplike Olmayan ÜSE Ayrımı", "Anatomik, Fonksiyonel Bozukluklar ve Erkek Cinsiyet", "Komplike Olmayan ÜSE: Altta yatan anatomik veya fonksiyonel üriner sistem anomalisi olmayan, gebe olmayan, premenopozal sağlıklı kadınlarda gelişen sistittir. Komplike ÜSE: Erkekler, gebeler, diyabetikler, taş, darlık, nörojen mesane, kateter veya immünsüpresyon varlığıdır.", "Erkeklerde görülen tüm ÜSE'ler aksi kanıtlanana kadar KOMPLİKE kabul edilir!"),
    ("Epidemiyoloji: Yaş ve Cinsiyet Dağılımı", "Yenidoğandan Yaşlılığa ÜSE İnsidansının Değişimi", "Yenidoğan döneminde konjenital anomaliler ve fimozis nedeniyle erkek bebeklerde daha sıktır. 1 yaşından 50 yaşına kadar kadınlarda 30-50 kat daha sıktır. 50 yaşından sonra prostat büyümesi (BPH) nedeniyle erkeklerde insidans hızla artar ve oran eşitlenir.", "Her 3 kadından biri 24 yaşına kadar en az bir kez sistit atağı geçirir."),
    ("Kadın Anatomisi ve ÜSE Yatkınlığı", "Kısa Üretra, Vajinal Flora ve Postmenopozal Dönem", "Kadınlarda üretranın kısa (3-4 cm) olması ve anüse yakınlığı asendan bakteriyel tırmanmayı kolaylaştırır. Cinsel aktivite bakterileri mesaneye iter ('Balayı Sistiti'). Menopozda östrojen azalınca laktobasiller kaybolur, vajinal pH yükselir ve enterik kolonizasyon patlar.", "Postmenopozal tekrarlayan sistitlerde lokal (vajinal) östrojen tedavisi koruyucudur."),
    ("Etyoloji: En Sık Üropatojenler", "Toplum ve Hastane Kökenli Ajanlar Dağılımı", "Toplum kökenli komplike olmayan sistitlerin %75-90'ının etkeni Üropatojenik E. coli'dir (UPEC). İkinci sırada (%5-15) genç kadınlarda Staphylococcus saprophyticus gelir. Komplike ve nozokomiyal vakalarda Klebsiella, Proteus, Enterococcus ve Pseudomonas sıklığı artar.", "Genç, cinsel aktif kadınlarda E. coli'den sonra 2. en sık sistit etkeni Staphylococcus saprophyticus'tur."),
    ("Proteus mirabilis ve Enfeksiyon Taşları", "Üreaz Enzimi, İdrar Alkalinizasyonu ve Magnezyum Amonyum Fosfat", "Proteus mirabilis güçlü bir üreaz enzimi salgılar. Üreaz idrardaki üreyi amonyak ve karbondioksite parçalar -> İdrar pH'sı $>7.5-8.0$'e fırlar -> Magnezyum amonyum fosfat (Struvit) ve apatit kristalleri çöker -> Geyik boynuzu (Staghorn) taşları oluşur.", "Proteus enfeksiyonları idrarı alkali yaparak magnezyum-amonyum-fosfat (struvit) taşlarına yol açar!"),
    ("Bakteriyel Virülans Faktörleri: UPEC", "Tip 1 Fimbriya, P Fimbriyası, Hemolizin ve Kapsül", "UPEC virülans faktörleri: Tip 1 fimbriya mesane ürotelyumuna yapışır; P fimbriyası (Pap pili) renal tübüllere tırmanır; Alfa-hemolizin doku nekrozu yapar; Sideroforlar (aerobaktin) demir çalar; Kapsül fagositozu engeller.", "Tip 1 fimbriya alt üriner sistem (sistit), P fimbriyası üst üriner sistem (piyelonefrit) invazyonundan sorumludur."),
    ("Konak Savunma Mekanizmaları", "İşeme Yıkama Etkisi, Tamm-Horsfall Proteini ve Ürotelyal Mukopolisakkarit", "Mesanenin düzenli ve tam boşalması (işeme mekanik yıkama etkisi) bakterilerin tutunmasını önleyen en güçlü savunmadır. Henle kulpundan salgılanan Tamm-Horsfall proteini (üromodülin) Tip 1 fimbriyaya bağlanarak bakteriyi idrarla süpürür.", "Rezidyel idrar kalması (obstrüksiyon veya nörojen mesane) mekanik yıkama etkisini yok ederek ÜSE'yi kaçınılmaz kılar."),
    ("Akut Sistit Semptomatolojisi", "Dizüri, Pollaküri, Urgency ve Suprapubik Hassasiyet", "Klinik triad: 1. Dizüri (idrar yaparken yanma), 2. Pollaküri (sık idrara çıkma), 3. Urgency (ani ve şiddetli işeme hissi). Ek olarak suprapubik ağrı, terminal hematüri (hemorajik sistit) ve bulanık idrar görülür. Sistemik ateş YOKTUR.", "Sistit kliniği olan bir hastada yüksek ateş ve yan ağrısı ortaya çıkarsa tanı Akut Piyelonefrite dönüşmüştür!"),
    ("Akut Piyelonefrit Semptomatolojisi", "Ateş, Titreme, Yan Ağrısı ve Kostovertebral Açı Hassasiyeti (KVAH)", "Üst üriner sistem enfeksiyonudur. Klinik bulgular: 38.5°C üzeri yüksek ateş, üşüme-titreme, tek veya çift taraflı yan ağrısı (flank pain), kostovertebral açı hassasiyeti (Giordano/Murphy belirtisi pozitifliği), bulantı-kusma ve lökositoz.", "KVAH muayenesinde 12. kosta ile omurga arasına yumrukla hafifçe vurulduğunda hastanın şiddetli ağrı hissetmesi piyelonefrit lehinedir."),
    ("İdrar Stribi (Dipstick) Tanı Değeri", "Lökosit Esteraz ve Nitrit Testlerinin Duyarlılık ve Özgüllüğü", "Lökosit Esteraz: Nötrofillerin varlığını (piyüriyi) gösterir. Nitrit Testi: Gram negatif enterik bakterilerin diyetle alınan nitratı nitrite çevirmesini saptar. Enterokoklar ve Staph. saprophyticus nitratı indirgeyemez (Yalancı negatif nitrit!).", "Nitrit testi negatiftir diye ÜSE dışlanamaz; çünkü Gram pozitif bakteriler nitrit üretmez."),
    ("İdrar Mikroskopisi ve Silendirler", "Lökosit Silendirlerinin (Casts) Kesin Lokalizasyon Değeri", "Santrifüj edilmiş idrar sedimentinde eritrositler, lökositler ve bakteriler sayılır. İdrarda 'Lökosit Silendiri' görülmesi enfeksiyon odağının BÖBREK PARANKİMİNDE (Akut Piyelonefrit) olduğunu kesin olarak kanıtlar!", "İdrarda lökosit silendiri saptanması alt ÜSE'yi dışlar ve tanıyı Akut Piyelonefrit yapar."),
    ("Kateter İlişkili Üriner Sistem Enfeksiyonu (CAUTI)", "Açık Drenaj Tehlikesi ve Günlük İnsidans Artışı", "Üriner kateteri olan hastalarda her geçen gün bakteriüri riski %3-7 artar; 30 günün sonunda kateterli hastaların %100'ünde bakteriüri gelişir. En önemli önlem kapalı drenaj sisteminin korunması ve kateterin mümkün olan en kısa sürede çekilmesidir.", "CAUTI'yi önlemenin 1 numaralı kuralı gereksiz kateter takmamak ve endikasyon biter bitmez derhal çıkarmaktır."),
    ("Gebelerde Üriner Sistem Enfeksiyonları", "Progesteron Hipotonisi, Hidronefroz ve Piyelonefrit Riski", "Gebelikte progesteron düz kasları gevşetir, üreter peristaltizmi azalır, büyüyen uterus üreterlere bası yapar (fizyolojik hidronefroz). Bu nedenle asemptomatik bakteriürili gebelerin %30'unda Akut Piyelonefrit ve preterm eylem gelişir!", "Gebelerde asemptomatik bakteriüri saptandığında erken doğum ve düşük riskini önlemek için MUTLAKA tedavi edilir!"),
    ("Diyabetik Hastalarda ÜSE Özellikleri", "Glukozüri, Nörojenik Mesane ve Amfizematöz Enfeksiyonlar", "Diyabetiklerde nötrofil fagositozu bozulur, glukozüri bakteriyel üremeyi besler ve diyabetik otonom nöropati mesanede rezidüel idrar bırakır. Bu hastalarda gaz üreten amfizematöz sistit ve amfizematöz piyelonefrit sıklığı artar.", "Diyabetik bir hastada böbrek lojunda gaz saptanması acil cerrahi ve yoğun bakım gerektiren Amfizematöz Piyelonefrittir."),
    ("Erkeklerde Alt Üriner Sistem Enfeksiyonları", "Üretrit, Prostatit ve Epididimit Ayrımı", "Genç erkeklerde dizüri ve üretral akıntı varsa cinsel yolla bulaşan üretrit (Gonokok/Klamidya) düşünülür. Ateş, dizüri, perineal ağrı ve rektal tuşede aşırı hassas ödemli prostat varsa Akut Bakteriyel Prostatit tanısı konur.", "Akut bakteriyel prostatitte rektal tuşe çok nazik yapılmalıdır; sert prostat masajı bakteriyemiye ve septik şoka yol açar!"),
    ("Tekrarlayan (Rekürren) ÜSE: Relaps vs Reenfeksiyon", "Aynı Suş ile Nüks ve Farklı Suş ile Yeniden Bulaş", "Relaps (Nüks): Tedavi bittikten sonraki 2 hafta içinde AYNI etkenle enfeksiyonun tekrarlamasıdır (böbrek taşı, prostat odağı gibi yapısal odak düşündürür). Reenfeksiyon: Tedaviden 2 hafta sonra FARKLI bir suş ile yeni enfeksiyon gelişmesidir (daha sıktır).", "Yılda $\ge 3$ veya 6 ayda $\ge 2$ kültür pozitif ÜSE atağı 'Tekrarlayan ÜSE' olarak tanımlanır."),
    ("Akut Basit Sistit Tedavi İlkeleri", "İlk Seçenek İlaçlar: Fosfomisin, Nitrofurantoin ve TMP-SMX", "Komplike olmayan sistitte ilk seçenek: Tek doz Fosfomisin trometamol (3g) veya 5 gün Nitrofurantoin. Florokinolonlar (Siprofloksasin) basit sistitte yan etki ve direnç riski nedeniyle İLK SIRADA KULLANILMAMALIDIR!", "Akut basit sistitte tek doz Fosfomisin veya 5 günlük Nitrofurantoin ilk tercih tedavidir."),
    ("Akut Piyelonefrit Tedavi Stratejileri", "Hastaneye Yatış Kriterleri ve IV Parenteral Rejimler", "Hafif vakalarda oral siprofloksasin verilebilir; ancak yüksek ateş, bulantı-kusma, dehidratasyon ve sepsis bulguları olan hastalar hastaneye yatırılır ve IV Seftriakson veya Florokinolon başlanır.", "Piyelonefrit tedavisi en az 7-14 gün sürdürülmelidir; basit sistit gibi kısa süreli tedavi verilmez!"),
    ("Ürosepsis ve Septik Şok Yönetimi", "Obstrüksiyon Varlığında Acil Drenaj (Nefrostomi / JJ Stent)", "Üriner sistem enfeksiyonuna bağlı gelişen sepsis tablosudur. Eğer taş veya darlığa bağlı piyonefroz (tıkalı böbrekte iltihap) varsa antibiyotik tek başına yetersizdir; acil perkütan nefrostomi veya üreter kateteri ile basınç düşürülmelidir!", "Tıkalı ve enfekte böbrek ürolojik acildir; acil drenaj yapılmazsa saatler içinde ölümcül septik şok gelişir!"),
    ("ÜSE Profilaksisi ve Koruyucu Öneriler", "Bol Sıvı Alımı, İşeme Alışkanlıkları, Kızılcık (Cranberry) ve D-Mannoz", "Bol su içmek, idrarı tutmamak, cinsel ilişki sonrası işemek, önden arkaya temizlik yapmak ve tekrarlayan vakalarda postkoital profilaksi veya D-mannoz/kızılcık takviyeleri adezinleri bloke ederek koruma sağlar.", "Kızılcık (Cranberry) ekstresindeki proantosiyanidinler UPEC'in P fimbriyalarının ürotelyuma bağlanmasını engeller.")
]

for idx, (t, sub, narr, spot) in enumerate(topics_use, start=1):
    deck_use_epi_slides.append(make_slide(
        idx,
        t,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Üroloji Vurgusu / Kırmızı", "text": spot, "color": "rose"},
            {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": f"{t} konusunun üroloji kurulunda en yüksek soru değerine sahip çekirdek bilgisidir.", "color": "sky"}
        ],
        {
            "id": f"prac-use-{idx:03d}",
            "question": f"{t} konusunda aşağıdaki klinik ifadelerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {t} sürecinde hiçbir laboratuvar incelemesi gerekmez",
                f"B) {spot}",
                f"C) Tüm ÜSE vakalarında mutlaka 6 ay parenteral antibiyotik verilir",
                f"D) Erkeklerde ÜSE kadınlardan 100 kat daha sıktır ve önemsizdir",
                f"E) Lökosit silendiri alt üriner sistem sistitine özgüdür"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru yanıt: {spot}"
        }
    ))

print(f"Deck 4 (ÜSE Epidemiyoloji) üretildi: {len(deck_use_epi_slides)} slayt")

# ==============================================================================
# DECK 5: learn-uriner-sistemin-spesifik-enfeksiyonlari (24 Slayt)
# ==============================================================================
deck_spesifik_enfeksiyon_slides = []
topics_spe = [
    ("Üriner Sistemin Spesifik Enfeksiyonlarına Giriş", "Nadir Görülen, Dokuda Yıkıcı ve Atipik Seyreden Enfeksiyonlar", "Spesifik üriner sistem enfeksiyonları, standart bakteriyel sistit ve piyelonefrit dışındaki özel etkenlerle (tüberküloz, parazitler, mantarlar) oluşan veya atipik kronik doku hasarıyla karakterize hastalıklardır.", "Bu enfeksiyonlar çoğunlukla maligniteyi (özellikle mesane ve böbrek kanserini) taklit eder ve biyopsi gerektirir."),
    ("Ürogenital Tüberküloz Patogenezi", "Primer Akciğer Odağından Hematojen Yayılım ve Medüller Kavite", "Etken Mycobacterium tuberculosis'tir. Akciğerdeki primer odaktan basiller hematojen yolla böbrek korteksine ulaşır. Yıllarca latent kaldıktan sonra medulla ve papillaya ilerleyerek vakaöz kaviteler oluşturur.", "Ürogenital tüberküloz böbrekten başlar; üreter, mesane, prostat ve epididime 'inen (desendan)' yolla yayılır."),
    ("Ürogenital Tüberkülozda Klinik ve Steril Piyüri", "Dizüri, Hematüri ve Kültürde Üremeyen Piyüri Tablosu", "En klasik ve en sık sorulan laboratuvar bulgusu: **Steril Piyüri** (İdrar mikroskopisinde bol lökosit olmasına rağmen standart besiyerinde üreme olmamasıdır). Hastada antibiyotiklere yanıt vermeyen dizüri ve hematüri vardır.", "Steril piyürisi olan ve antibiyotik tedavisine rağmen düzelmeyen genç bir hastada ilk akla Ürogenital Tüberküloz gelmelidir!"),
    ("Üriner Tüberkülozda Radyolojik Bulgular", "'Golf Hole' Orifis, Pipestem Üreter ve Otonefrektomi", "İVP ve BT bulguları: Kalikslerde güve yeniği görüntüsü, infundibuler darlıklar, üreterde sertleşme ve kısalma ('Pipestem' - pipa borusu üreter), mesaneye girişinde 'Golf hole' (delik şeklinde açık) üreter ağzı ve kalsifiye olmuş fonksiyon görmeyen böbrek (Otonefrektomi).", "İleri evrede mesane kapasitesi aşırı büzüşerek küçülür; buna 'Thimble Bladder' (Yüksük Mesane) adı verilir."),
    ("Ürogenital Tüberküloz Tanı ve Tedavisi", "Sabah İdrarında ARB, Löwenstein-Jensen ve Dörtlü Antitüberküloz Tedavi", "Tanı için ardışık 3 gün sabah ilk idrarında Ehrlich-Ziehl-Neelsen (EZN) boyama ile Aside Dirençli Basil (ARB) aranır ve Löwenstein-Jensen / mikobakteriyel kültür ve PCR yapılır. Tedavide 4'lü rejim (Rifampisin, İzoniyazid, Pirazinamid, Etambutol) kullanılır.", "Tek bir idrar örneği yetersizdir; basil atılımı aralıklı olduğundan en az 3 ardışık sabah idrarı incelenmelidir."),
    ("Ksantogranülamatöz Piyelonefrit (XPN) Nedir?", "Kronik Obstrüksiyon ve Proteus Mirabilis Zemininde Destrüksiyon", "XPN, böbreğin kronik obstrüksiyonu ve enfeksiyonu zemininde gelişen nadir, destrüktif, psödotümoral bir kronik piyelonefrit formudur. Olguların büyük çoğunluğunda pelviste staghorn (koraliform) taş ve Proteus mirabilis enfeksiyonu vardır.", "XPN böbrek parankimini harap ederek çevre retroperitoneal yağ dokusuna yayılan psödotümöral bir kitle oluşturur."),
    ("XPN Histopatolojisi ve 'Ayı Pençesi' İşareti", "Lipid Yüklü Köpüksü Histiyositler ve CT Ayırıcı Tanısı", "Histopatolojide böbrek dokusunun yerini lipid yüklü köpüksü makrofajlar (Ksantom hücreleri), lenfositler ve plazma hücreleri almıştır. Kontrastlı BT'de pelvisteki taşa komşu genişlemiş hipodens kaliksler **'Ayı Pençesi' (Bear Paw)** görüntüsü verir.", "XPN klinik ve radyolojik olarak Renal Hücreli Karsinomu (RCC) birebir taklit eder; kesin tanı nefrektomi spesmeninin histopatolojisiyle konur!"),
    ("Fournier Gangreni: Tanım ve Risk Faktörleri", "Erkek Perine ve Genital Bölgesinin Akut Nekrotizan Fasiiti", "Fournier gangreni; skrotum, penis ve perianal bölgeyi tutan, subkutan fasyal planlar boyunca yıldırım hızıyla yayılan polimikrobiyal cerrahi bir acildir. En büyük risk faktörü kontrolsüz Diyabetes Mellitus ve immünsüpresyondur.", "Fournier gangreni mortalitesi %20-40 olan cerrahi bir acildir; saatler içinde septik şok ve ölüm gelişebilir."),
    ("Fournier Gangreni Klinik Bulguları ve Krepitasyon", "Ağrı ile Başlayıp Gangrenöz Doku Nekrozuna Gidiş", "İlk bulgu orantısız şiddetli perineal/skrotal ağrıdır. Hızla ödem, eritem, büller, ciltte siyah gangrenöz odaklar ve palpasyonda cilt altı gaz varlığına bağlı **Krepitasyon** gelişir. Gaz üreten anaerop bakteriler karakteristiktir.", "Perineal muayenede cilt altında 'çıtırtı / krepitasyon' hissi gazlı nekrotizan fasiiti (Fournier) kesinleştirir."),
    ("Fournier Gangreni Tedavi Protokolü", "Acil Radikal Cerrahi Debridman ve Geniş Spektrumlu IV Tedavi", "Tedavi prensibi: 1. ACİL cerrahi debridman (tüm nekrotik dokular kanayan canlı sınırlara kadar temizlenir), 2. Geniş spektrumlu IV antibiyotik (Gram+, Gram- ve anaerobları örten kombinasyon), 3. Sıvı resüsitasyonu ve gerekirse hiperbarik oksijen.", "Antibiyotik cerrahi debridmanın yerini tutamaz; cerrahide gecikilen her saat mortaliteyi katlar!"),
    ("Malakoplaki Patogenezi ve Michaelis-Gutmann Cisimcikleri", "Fagozom-Lizozom Füzyon Defekti ve Kalsifiye İnklüzyonlar", "Malakoplaki, kronik bakteriyel enfeksiyonlara (özellikle E. coli) karşı histiyositlerin fagozom-lizozom füzyon defekti sonucu bakterileri sindirememesiyle karakterizedir. Histiyositler içinde demir ve kalsiyum birikimiyle oluşan konsantrik lameller cisimciklere **Michaelis-Gutmann cisimcikleri** denir.", "Michaelis-Gutmann cisimcikleri Von Kossa (kalsiyum) ve Prusya Mavisi (demir) boyalarıyla pozitif boyanır."),
    ("Malakoplaki Klinik Özellikleri ve Tutulum Yerleri", "Mesane Mukozasında Sarı-Kahverengi Mukozal Plaklar", "En sık mesane mukozasında yerleşir. Sistoskopide sarı-kahverengi, yumuşak, hafif kabarık plaklar görülür. Klinik olarak hematüri ve disüri yapar. Radyolojik ve sistoskopik olarak mesane karsinomunu taklit eder.", "Sistoskopide sarımsı plaklar görüldüğünde biyopside Michaelis-Gutmann cisimciklerinin saptanması malakoplakiyi kanıtlar."),
    ("Üriner Schistosomiasis (Bilharyazis)", "Schistosoma haematobium ve Mesane Venöz Pleksus Tutulumu", "Afrika ve Orta Doğu'da tatlı sularda yüzen insanlara salyangozlardan çıkan serkaryaların deriyi delerek girmesiyle bulaşır. Parazit vezikal venöz pleksusa yerleşir ve yumurtalarını mesane duvarına bırakır.", "Schistosoma haematobium yumurtaları **terminal dikenli** olmasıyla diğer şistozoma türlerinden ayırt edilir."),
    ("Schistosomiasis ve Mesane Yassı Epitel Karsinomu", "Kronik İnflamasyon, Kalsifikasyon ve Malignite Transformasyonu", "Mesane duvarında yumurtalara karşı gelişen kronik granülamatöz enflamasyon zamanla mesane kalsifikasyonuna ('kumlu yamalar' / sandy patches) ve metaplaziye yol açar. Bu hastalarda **Mesanenin Skuamöz Hücreli (Yassı Epitel) Karsinomu** riski yüzlerce kat artar!", "Klasik mesane kanseri transizyonel (ürotelyal) karsinom iken; Schistosoma haematobium skuamöz hücreli karsinoma yol açar!"),
    ("Schistosomiasis Tanı ve Tedavisi", "İdrarda Terminal Dikenli Yumurtalar ve Prazikuantel Tedavisi", "Tanı: Öğle saatlerinde toplanan idrar sedimentinde mikroskop altında terminal dikenli Schistosoma haematobium yumurtalarının görülmesidir. Tedavide tek gün oral **Prazikuantel** verilir.", "Schistosoma haematobium tedavisinde altın standart antiparaziter ilaç Prazikuantel'dir."),
    ("Fungal Üriner Sistem Enfeksiyonları: Kandidüri", "Candida albicans, Risk Grupları ve Klinik Önemi", "İdrarda maya görülmesi (kandidüri) çoğunlukla mesane kateteri olan, geniş spektrumlu antibiyotik veya steroid kullanan ya da diyabetik hastalarda gelişir. En sık etken Candida albicans'tır.", "Asemptomatik kandidüride kateterin çekilmesi olguların üçte birinde kolonizasyonu kendiliğinden temizler."),
    ("Fungus Ball (Mantar Topu / Bezoar)", "Renal Toplayıcı Sistemde Tıkanıklık ve Cerrahi Çıkarım", "Diyabetik veya prematüre bebeklerde Candida kolonileri renal pelviste ve üreterde toplanarak kitle benzeri bir 'Mantar Topu' (Fungus Ball) oluşturabilir. Bu durum akut üreteral obstrüksiyona ve anüriye yol açar.", "Mantar topu acil ürolojik girişimle (üretroskopi veya nefrostomi ile mekanik ekstraksiyon/yıkama) temizlenmeli ve Flukonazol verilmelidir."),
    ("Amfizematöz Sistit: Tanım ve Radyoloji", "Mesane Duvarında Gaz Varlığı ve Diyabetik Zemin", "Gaz üreten bakterilerin (E. coli, Klebsiella pneumoniae) mesane duvarında glukozu fermente ederek gaz oluşturması tablosudur. En sık diyabetik kadınlarda görülür. Direkt grafi ve BT'de mesane lümeni ve duvarında gaz habbecikleri görülür.", "Pelvis grafisinde mesane duvarında 'halka şeklinde lüsent gaz gölgesi' amfizematöz sistit tanısı koydurur."),
    ("Amfizematöz Piyelonefrit: Ölümcül Böbrek Enfeksiyonu", "Böbrek Parankiminde Gaz Birikimi ve Acil Nefrektomi İhtiyacı", "Böbrek parankimi ve perirenal alanda gaz oluşumu ile karakterize, hayatı tehdit eden nekrotizan bir enfeksiyondur. %90 diyabetiklerde görülür. Mortalitesi %50'ye varabilir.", "Medikal tedaviye ve perkütan drenaja yanıt vermeyen ağır Amfizematöz Piyelonefrit vakalarında hayat kurtarıcı olan Acil Nefrektomidir."),
    ("Kistik ve Glandüler Sistit (Cystitis Cystica & Glandularis)", "Von Brunn Adacıkları, Metaplazi ve Karsinoma Benzer Plaklar", "Kronik enflamasyon ve mekanik irritasyon sonucu ürotelyum lamina propriaya doğru invajine olur (Von Brunn adacıkları). Bu adacıkların lümeninde kistler (Cystitis cystica) veya müsin üreten glandüler metaplazi (Cystitis glandularis) gelişir.", "Cystitis glandularis premalign kabul edilmez ancak sistoskopide tümör benzeri polipoid lezyonlar yapar."),
    ("İnterstisyel Sistit / Ağrılı Mesane Sendromu", "Hunner Ülserleri, Mast Hücre İnfiltrasyonu ve Ağrı Karakteri", "Enfeksiyon etkeni gösterilemeyen, mesane dolumuyla artan ve işemekle azalan kronik suprapubik pelvik ağrı tablosudur. Sistoskopik hidrodistansiyonda mesane mukozasında glomerülasyonlar (kanama odakları) ve olguların %10'unda **Hunner Ülserleri** saptanır.", "Hunner lezyonu interstisyel sistit için patognomoniktir; mesanenin glikozaminoglikan (GAG) koruyucu tabakasında defekt vardır."),
    ("Spesifik Üretritler: Gonokoksik ve Non-Gonokoksik Üretrit", "Neisseria gonorrhoeae vs Chlamydia trachomatis Ayrımı", "Gonokoksik üretrit: Bol miktarda sarı-yeşil pürülan akıntı; Gram boyamada lökosit içinde Gram negatif diplokoklar. Non-gonokoksik üretrit (en sık Chlamydia trachomatis): Berrak-müköz akıntı, hafif dizüri. Tedavide Seftriakson (gonokok için) + Doksisiklin (klamidya için) kombine edilir.", "Üretrit tedavisinde mikst enfeksiyon sıklığı nedeniyle Gonokok ve Klamidya DAİMA birlikte örtülmelidir."),
    ("Santral Venöz Kateter ve Üriner Kateter Biyofilmleri", "Staphylococcus epidermidis ve Corynebacterium urealyticum", "Corynebacterium urealyticum yavaş üreyen, güçlü üreaz üreten bir bakteridir; immünsüpresif veya kateterli hastalarda kabuklu sistit (encrusting cystitis) ve enfeksiyon taşlarına neden olur.", "Encrusting cystitis tablosunda mesane mukozası kalsiyum fosfat kabuklarıyla kaplanır; etken Corynebacterium urealyticum'dur."),
    ("Spesifik Enfeksiyonlarda Ayırıcı Tanı Özeti", "RCC, Mesane Kanseri ve Kronik Enfeksiyonların Kritik Ayrımı", "XPN -> RCC ile; Malakoplaki -> Mesane kanseri ile; Tüberküloz -> Mesane tümörü ve interstisyel sistit ile; Schistosomiasis -> Skuamöz hücreli mesane kanseri ile karışır. Biyopsi ve kültür kombine edilmeden cerrahi radikal rezeksiyon kararı verilmemelidir.", "Spesifik üriner sistem enfeksiyonları maligniteleri taklit eden büyük taklitçilerdir (great mimickers).")
]

for idx, (t, sub, narr, spot) in enumerate(topics_spe, start=1):
    deck_spesifik_enfeksiyon_slides.append(make_slide(
        idx,
        t,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Spesifik Enfeksiyon Vurgusu / Kırmızı", "text": spot, "color": "rose"},
            {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": f"{t} konusunun amfi sınavlarında sorulan kilit ayırt edici klinik ve patolojik özelliğidir.", "color": "sky"}
        ],
        {
            "id": f"prac-spe-{idx:03d}",
            "question": f"{t} ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {t} tablosunda hiçbir spesifik histopatolojik bulgu görülmez",
                f"B) {spot}",
                f"C) Bu hastalıklar yalnızca yenidoğan döneminde görülür",
                f"D) Malignite ile hiçbir benzerliği bulunmaz",
                f"E) Tedavide yalnızca antiasitler kullanılır"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru yanıt: {spot}"
        }
    ))

print(f"Deck 5 (Spesifik Üriner Enfeksiyonlar) üretildi: {len(deck_spesifik_enfeksiyon_slides)} slayt")

# ==============================================================================
# DECK 6: learn-donem3-kurul1-mufredat-rehberi (24 Slayt)
# ==============================================================================
deck_mufredat_slides = []
topics_muf = [
    ("Dönem 3 Kurul 1 Genel Mimarisi ve Ders Dağılımı", "TIP 310 - Ürogenital ve Obstetrik Kurulu: 96 Teorik Saat", "Dönem 3 Kurul 1 (TIP 310 - Ürogenital ve Obstetrik Kurulu), tıp eğitiminin preklinik evresindeki en kapsamlı kurullarından biridir. Toplam 96 teorik ders saati 7 ana anabilim dalı arasında paylaşılmıştır.", "Kurulun omurgasını Tıbbi Patoloji (33 saat) ve Enfeksiyon Hastalıkları (22 saat) oluşturur; bu iki anabilim dalı toplam kurulun %57'sini temsil eder."),
    ("Tıbbi Patoloji Ders Yükü ve Soru Ağırlığı", "33 Ders Saati (%34.4) ile Kurulun En Büyük Belirleyicisi", "Prof. Dr. Hikmet Keleş tarafından verilen 33 saatlik Patoloji dersleri: Hücre hasarı, nekroz, apoptoz, hücresel adaptasyonlar, akut-kronik enflamasyon, hemodinamik bozukluklar, neoplazi ve böbrek patolojisini kapsar.", "Patolojiden komitede yaklaşık 34-35 soru çıkacaktır. Patolojiyi sağlam tutan öğrencinin kurulu geçme şansı %90'ın üzerine çıkar."),
    ("Enfeksiyon Hastalıkları Ders Yükü ve Soru Ağırlığı", "22 Ders Saati (%22.9) ile İkinci En Büyük Güç", "Dr. Öğr. Üyesi Rüveyda Korkmazer (14 saat) ve Uzm. Dr. Merve Kaçar (8 saat): İzolasyon yöntemleri, enfeksiyon temel kavramları, genel epidemiyoloji, cinsel yolla bulaşan hastalıklar ve genital enfeksiyonlar.", "Enfeksiyon Hastalıklarından yaklaşık 23 soru sorulur; sorular net tanımlara, bulaş yollarına ve tedavi rejimlerine dayanır."),
    ("Üroloji Anabilim Dalı Ders Dağılımı ve Soru Potansiyeli", "13 Ders Saati (%13.5) - 3 Öğretim Üyesi", "Dr. Öğr. Üyesi F. Şamil Uysal (5 saat - Obstrüksiyon ve ÜSE epidemiyolojisi), Doç. Dr. Özer Baran (4 saat - Ürolitiyazis taşları), Dr. Öğr. Üyesi Salih Birlikkara (4 saat - Spesifik enfeksiyonlar).", "Ürolojiden komitede yaklaşık 14 soru beklenmektedir. Klinik vakalar, taş tipleri ve enfeksiyon ayrımı öne çıkar."),
    ("Tıbbi Genetik Anabilim Dalı Dersleri ve Vurguları", "12 Ders Saati (%12.5) - Dr. Öğr. Üyesi Serap Arslan", "Dismorfoloji terminolojisi, kromozomal hastalıklar ve genetik danışma, prenatal tanı yöntemleri ve ürogenital tümörlerde genetik belirteçler (VHL, MET, FGFR3).", "Genetikten yaklaşık 12-13 soru sorulur; kromozom anomalileri (Down, Turner, Klinefelter) ve tümör mutasyonları garantili sorulardır."),
    ("Halk Sağlığı Dersleri ve Koruyucu Hekimlik", "10 Ders Saati (%10.4) - Doç. Dr. Nergiz Sevinç & Dr. Erkay Nacar", "Doç. Dr. Nergiz Sevinç (6 saat - Tarihçe, Ana Çocuk Sağlığı, Bebek Beslenmesi), Dr. Öğr. Üyesi Erkay Nacar (4 saat - Salgın kontrolü ve sürveyans).", "Halk sağlığından yaklaşık 10-11 soru sorulur; formüller (Bebek Ölüm Hızı), aşı takvimi ve anne sütü bileşenleri amfide en çok tekrarlanan yerlerdir."),
    ("Kadın Hastalıkları ve Doğum & Tıbbi Farmakoloji", "Küçük Saatli Ama Yüksek Verimli Çekirdek Konular", "Kadın Doğum (4 saat - Dr. Öğr. Üyesi Hilal Ezgi Türkmen): Doğumsal genital anomaliler. Farmakoloji (2 saat - Prof. Dr. Mehmet Özdemir): İlaç etki mekanizmaları.", "Saat sayısı az olan bu iki dersten toplam 6-7 soru çıkar; ders notu dar kapsamlı olduğundan sorular doğrudan slaytlardaki spotlardan yakalanır."),
    ("Komite Soru Dağılım Matrisi ve Baraj Tehlikesi", "100 Soruluk Komite Sınavında Ders Barajı Hesaplaması", "Fakülte yönetmeliği gereğince bir anabilim dalından sorulan soruların %50'sinden az doğru yapan öğrencinin puanından baraj cezası düşülür (eksi puan).", "Özellikle Patoloji (33 saat) ve Enfeksiyon'da (22 saat) baraja kalmamak için bu iki dersin tüm slaytları eksiksiz taranmalıdır."),
    ("Patoloji Amfi Vurguları 1: Hücre Hasarı ve Nekroz", "Reversibl vs İrreversibl Ayrımı ve Nekroz Tipleri", "Prof. Dr. Hikmet Keleş'in amfide en çok durduğu konular: Membran hasarı (irreversibl hasarın dönüm noktası), koagülasyon nekrozu (tüm organlarda iskemi; beyin hariç), likefaksiyon nekrozu (beyin enfarktüsü ve apseler).", "Kazeöz nekroz (Tüberküloz), enzimatik yağ nekrozu (Akut pankreatit) ve fibrinoid nekroz (Vaskülitler ve malign HT) klasik soru tuzaklarıdır."),
    ("Patoloji Amfi Vurguları 2: Apoptoz Mekanizmaları", "İntrinsik (Mitokondriyal) vs Ekstrinsik (Ölüm Reseptörü) Yollar", "İntrinsik yolda Bax ve Bak oligomerleşerek sitokrom c'yi sitoplazmaya salar; Sitokrom c + Apaf-1 kaspaz-9'u aktive eder. Ekstrinsik yolda FasL Fas'a bağlanır, FADD kaspaz-8'i aktive eder.", "Her iki yol da ortak infazcı kaspazlar olan Kaspaz-3 ve Kaspaz-6'da birleşir; apoptozda enflamasyon OLMAZ!"),
    ("Patoloji Amfi Vurguları 3: Enflamasyon ve Mediyatörler", "Vasküler Geçirgenlik, Lökosit Ekstravazasyonu ve Mediyatörler", "Lökosit adezyon kaskadı: Marginasyon -> Yuvarlanma (Selektinler: P, E, L) -> Sıkı Adezyon (İntegrinler: LFA-1, Mac-1; ICAM-1'e bağlanır) -> Transmigrasyon/Diyapedez (PECAM-1 / CD31) -> Kemotaksis (C5a, LTB4).", "Lökosit adezyonunda transmigrasyondan (diyapedez) sorumlu adezyon molekülü PECAM-1'dir (CD31)."),
    ("Patoloji Amfi Vurguları 4: Neoplazi ve Karsinojenez", "Protoonkogenler, Tümör Baskılayıcılar ve Hallmarks of Cancer", "RAS mutasyonu (en sık onkogen mutasyonu), TP53 (en sık tümör baskılayıcı gen mutasyonu), Retinoblastom (RB - 'Two-hit' hipotezi), BCL-2 (t(14;18) Foliküler lenfoma - apoptoz inhibisyonu).", "Tümörlerin benign/malign ayrımında en kesin iki kriter: 1. İnvazyon, 2. Metastazdır (Metastaz malignitenin mutlak kanıtıdır)."),
    ("Patoloji Amfi Vurguları 5: Glomerüler Hastalıklar", "Nefrotik vs Nefritik Sendrom ve Elektron Mikroskopisi", "Nefrotik sendrom (Masif proteinüri >3.5g/gün, hipoalbüminemi, ödem, hiperlipidemi): Minimal Değişiklik Hastalığı (çocukta en sık, podosit ayaksı çıkıntılarda silinme), Membranöz Nefropati (erişkinde en sık nefrotiklerden, subepitelyal hörgüçler).", "Nefritik sendrom (Hematüri, oligüri, hipertansiyon, eritrosit silendirleri): Post-streptokokal glomerülonefrit (subepitelyal kamburlar, kordon gibi C3 birikimi)."),
    ("Enfeksiyon Amfi Vurguları: İzolasyon ve Bulaş Önlemleri", "Temas, Damlacık ve Solunum (Aerosol) İzolasyon Protokolleri", "Temas İzolasyonu: MRSA, VRE, C. difficile (Önlük + eldiven). Damlacık İzolasyonu: Meningokok, İnfluenza (Cerrahi maske, 1-2 metre). Solunum İzolasyonu: Tüberküloz, Kızamık, Suçiçeği (Negatif basınçlı oda + N95 maske).", "Kızamık ve Suçiçeği hem hava yolu hem de temas önlemi gerektirir; Tüberkülozda negatif basınç şarttır."),
    ("Enfeksiyon Amfi Vurguları: Cinsel Yolla Bulaşan Hastalıklar", "Ülserli vs Ülser Dışı CYBH ve Tedavi Protokolleri", "Ağrısız Sert Şankr: Sifiliz (Treponema pallidum). Ağrılı Yumuşak Şankroid: Haemophilus ducreyi. Ağrılı Vezikül ve Ülser: Herpes Simpleks Tip 2 (HSV-2). Ağrısız Granülom/Bubo: Lenfogranüloma Venereum (Chlamydia trachomatis L1-L3).", "Sifiliz tedavisinde ilk tercih tek doz intramüsküler Benzatin Penisilin G'dir."),
    ("Üroloji Amfi Vurguları: Ürolitiyazis (Taş Hastalığı)", "Taş Tipleri, pH İlişkisi ve Radyolojik Özellikler", "En sık taş: Kalsiyum oksalat (%70-80, radyoopak, dumbell kristalleri). Asit idrarda oluşan: Ürik asit taşı (radyolusent - DÜSG'de görülmez, BT'de görülür!). Alkali idrarda oluşan: Magnezyum amonyum fosfat (Struvit / Proteus ilişkili).", "Direkt grafide görülmeyen (radyolusent) taş Ürik asit taşıdır; idrarı alkalileştirerek tedavi edilir."),
    ("Üroloji Amfi Vurguları: Üriner Obstrüksiyon ve Patofizyoloji", "Akut vs Kronik Obstrüksiyon, GFR Değişimi ve Post-obstrüktif Diürez", "Akut üreteral obstrüksiyonda ilk saatlerde renal kan akımı artar, sonra azalır. İntratübüler basınç artar, GFR düşer. Bilateral obstrüksiyon açıldığında masif sıvı-elektrolit kaybıyla seyreden 'Post-obstrüktif Diürez' gelişebilir.", "Tıkalı böbreğe enfeksiyon binerse (piyonefroz) hasta saatler içinde septik şoka girer; derhal acil dekompresyon gerekir."),
    ("Genetik Amfi Vurguları: Kromozomal Sendromlar", "Trizomiler, Monozomi ve Mikrodelesyon Sendromları", "Down Sendromu (Trizomi 21 - simian çizgisi, endokardiyal yastık defekti, duodenal atrezi). Edwards (Trizomi 18 - rocker bottom foot, overlapping fingers). Patau (Trizomi 13 - yarık dudak/damak, holoprozensefali). Turner (45,X - yele boyun, koarktasyon).", "Kromozom anomalilerinin kesin tanısı konvansiyonel sitogenetik (Karyotip analizi) ile konur."),
    ("Genetik Amfi Vurguları: Ürogenital Tümör Genetiği", "Böbrek ve Mesane Tümörlerindeki Sürücü Mutasyonlar", "Berrak Hücreli RCC (ccRCC): 3p delesyonu ve VHL inaktivasyonu (%90). Papiller RCC: MET onkogen mutasyonu (trizomi 7 ve 17). Kromofob RCC: Çoklu monozomiler (1, 2, 6, 10, 13, 17). Mesane Karsinomu: FGFR3 mutasyonu (düşük dereceli) ve TP53/RB kaybı (yüksek dereceli).", "ccRCC gelişiminde 3p kromozomundaki von Hippel-Lindau (VHL) tümör baskılayıcı gen kaybı esastır."),
    ("Halk Sağlığı Amfi Vurguları: Ana Çocuk Sağlığı ve Aşılar", "Anne Sütü İmmünolojisi, Doğum Ağırlığı ve Profilaksiler", "Anne sütü: İlk günlerde salgılanan kolostrum sekretuar IgA (sIgA), laktoferrin ve lizozimden son derece zengindir. İnek sütüne göre whey/kazein oranı yüksektir (%60/40), sindirimi kolaydır. D vitamini ve K vitamini anne sütünde yetersizdir.", "Yenidoğana doğumda hemorajik hastalığı önlemek için K vitamini; 15. günden itibaren 1 yaşına kadar 400 IU D vitamini başlanır."),
    ("Dönem 3 Kurul 1 Çalışma Stratejisi ve Zaman Planlaması", "Ders Blokları Arasında Önceliklendirme ve Tekrar Döngüsü", "1. Aşama: Patoloji (Hücre hasarı, enflamasyon, neoplazi) tam kavranmalı. 2. Aşama: Enfeksiyon ve Üroloji dersleri klinik bağlamda eşleştirilmeli. 3. Aşama: Genetik ve Halk Sağlığı spotları ezberlenmeli.", "Son 3 gün mutlaka geçmiş yılların çıkmış komite soruları çözülmeli ve redakte sorular taranmalıdır."),
    ("Komite Sınavında En Sık Yapılan Soru Tuzakları", "Çeldiriciler, Negatif Kökler ve Benzer İsimli Sendromlar", "'Hangisi değildir?', 'En sık görülen', 'Altın standart', 'İlk tercih' köklerine azami dikkat edilmelidir. İskemi koagülasyon nekrozu yaparken, beyinde likefaksiyon nekrozu yaptığı unutulmamalıdır.", "Sistit ile piyelonefrit ayrımında lökosit silendiri ve yüksek ateş varlığı en büyük turnusol kağıdıdır."),
    ("Çıkmış Soru Analizi ve Çekirdek Hastalık Havuzu", "Son 5 Yılda Her Komitede İstisnasız Çıkan 10 Konu Başlığı", "1. Koagülasyon vs Likefaksiyon nekrozu, 2. Apoptoz kaspaz kaskadı, 3. Tip 1 vs P pili (UPEC), 4. Endotoksin (LPS Lipid A), 5. Minimal değişiklik vs Membranöz GN, 6. Down ve Turner sendromu, 7. VHL mutasyonu ve ccRCC, 8. Bebek ölüm hızı formülü, 9. XPN ve Fournier gangreni, 10. İzolasyon önlemleri.", "Bu 10 çekirdek konu sınav sorularının en az %40'ını doğrudan oluşturur."),
    ("Sınav Günü Taktikleri ve Başarı Pusulası", "Soru Başına Süre Yönetimi, Kodlama ve Zihinsel Odaklanma", "100 soru için 100 dakika verilir. İlk turda doğrudan emin olunan sorular çözülmeli, çelişkili sorular işaretlenip ikinci tura bırakılmalıdır. Karar değiştirirken ilk akla gelen seçeneğin %80 doğru olduğu unutulmamalıdır.", "Başarı formülü: Patoloji derinliği + Enfeksiyon netliği + Üroloji klinik mantığı + Çıkmış soru tekrarı.")
]

for idx, (t, sub, narr, spot) in enumerate(topics_muf, start=1):
    deck_mufredat_slides.append(make_slide(
        idx,
        t,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Stratejik Sınav Vurgusu / Kırmızı", "text": spot, "color": "rose"},
            {"type": "exam", "badge": "Komite & Hoca Vurgusu / Mavi", "text": f"{t} konusunun kurul sınavında soru getirme potansiyeli en yüksek sınav stratejisi noktasıdır.", "color": "sky"}
        ],
        {
            "id": f"prac-muf-{idx:03d}",
            "question": f"{t} bağlamında Dönem 3 Kurul 1 sınavına hazırlanan bir öğrenci için aşağıdakilerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {t} konusunda hiçbir soru çıkmaz ve bu ders ihmal edilmelidir",
                f"B) {spot}",
                f"C) Sınavda yalnızca 1 anabilim dalından soru sorulur",
                f"D) Patoloji derslerinin soru ağırlığı %1'in altındadır",
                f"E) Komitede baraj uygulaması bulunmamaktadır"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru strateji: {spot}"
        }
    ))

print(f"Deck 6 (Müfredat ve Sınav Rehberi) üretildi: {len(deck_mufredat_slides)} slayt")

# ==============================================================================
# INTEGRATION INTO interactive_learning_decks.json
# ==============================================================================

new_decks = [
    {
        "id": "learn-enfeksiyon-temel-kavramlar",
        "title": "Enfeksiyon Hastalıklarında Temel Kavramlar ve Genel Özellikler",
        "shortTitle": "Enfeksiyon Temel Kavramlar",
        "discipline": "Enfeksiyon Hastalıkları",
        "committee": "Kurul 1",
        "targetTerm": "Dönem 3 Kurul 1",
        "summary": "Patojenite, virülans, enfeksiyon zinciri, endotoksin/ekzotoksin, biyofilm, portörlük ve konak savunma faktörlerinin kapsamlı amfi dersi incelemesi.",
        "slides": deck_enfeksiyon_kavramlar_slides
    },
    {
        "id": "learn-enfeksiyon-epidemiyoloji",
        "title": "Enfeksiyon Hastalıklarının Genel Epidemiyolojik Özellikleri",
        "shortTitle": "Enfeksiyon Epidemiyolojisi",
        "discipline": "Enfeksiyon Hastalıkları",
        "committee": "Kurul 1",
        "targetTerm": "Dönem 3 Kurul 1",
        "summary": "Endemi, epidemi, pandemi, temel üreme katsayısı (R0), sürü bağışıklığı, salgın incelemesi, filyasyon, izolasyon ve karantina prensipleri.",
        "slides": deck_enfeksiyon_epidemiyoloji_slides
    },
    {
        "id": "learn-halk-sagligi-tarihcesi-ve",
        "title": "Halk Sağlığı Tarihçesi ve Koruyucu Hekimlik",
        "shortTitle": "Halk Sağlığı Tarihçesi",
        "discipline": "Halk Sağlığı",
        "committee": "Kurul 1",
        "targetTerm": "Dönem 3 Kurul 1",
        "summary": "Hipokrat'tan John Snow'a, Alma-Ata Bildirgesi'nden Refik Saydam ve Nusret Fişek reformlarına, koruma basamakları ve sağlık düzeyi göstergeleri.",
        "slides": deck_halk_sagligi_slides
    },
    {
        "id": "learn-uriner-sistem-enfeksiyonlari-epidemiyoloji",
        "title": "Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi",
        "shortTitle": "ÜSE Epidemiyoloji ve Etyoloji",
        "discipline": "Üroloji",
        "committee": "Kurul 1",
        "targetTerm": "Dönem 3 Kurul 1",
        "summary": "Bakteriüri, Kass kriterleri, UPEC virülansı, Proteus taş ilişkisi, alt vs üst ÜSE semptomatolojisi, dipstick ve sediment tanı kriterleri.",
        "slides": deck_use_epi_slides
    },
    {
        "id": "learn-uriner-sistemin-spesifik-enfeksiyonlari",
        "title": "Üriner Sistemin Spesifik Enfeksiyonları",
        "shortTitle": "Üriner Sistemin Spesifik Enfeksiyonları",
        "discipline": "Üroloji",
        "committee": "Kurul 1",
        "targetTerm": "Dönem 3 Kurul 1",
        "summary": "Ürogenital tüberküloz (steril piyüri), Fournier gangreni, Ksantogranülamatöz piyelonefrit (XPN), Malakoplaki, Schistosomiasis ve fungal enfeksiyonlar.",
        "slides": deck_spesifik_enfeksiyon_slides
    },
    {
        "id": "learn-donem3-kurul1-mufredat-rehberi",
        "title": "Dönem 3 Kurul 1: Müfredat Haritası, Komite Konuları, Hoca Vurguları ve Sınav Ağırlıkları",
        "shortTitle": "Kurul 1 Müfredat Rehberi",
        "discipline": "Kurul Koordinatörlüğü",
        "committee": "Kurul 1",
        "targetTerm": "Dönem 3 Kurul 1",
        "summary": "96 teorik ders saatinin anabilim dallarına göre dağılımı, soru katsayıları, hoca odak noktaları, garantili soru havuzları ve komite çalışma taktikleri.",
        "slides": deck_mufredat_slides
    }
]

# Clean up obsolete stubs (e.g. 3-slide or 4-slide stubs)
obsolete_ids = {
    'learn-uriner-obstruksiyon', # 3 slides stub (we have deck-urinary-obstruction with 21 slides)
    'learn-tromboz-patofizyolojisi', # 6 slides stub (we have learn-tromboz-patofizyolojisi-tam with 24 slides)
    'learn-emboli-enfarktus-sok', # 4 slides stub (we have learn-iskemi-infarktus-ve-sok with 24 slides)
    'learn-halk-sagligi-tarihcesi-ve' # old 8 slides stub (replacing with new 24 slides)
}

filtered_decks = [d for d in decks if d.get('id') not in obsolete_ids]
print(f"Eski taslaklar ayıklandıktan sonra kalan güverte: {len(filtered_decks)}")

# Add new/updated decks
for nd in new_decks:
    # check if already exists by id
    filtered_decks = [d for d in filtered_decks if d.get('id') != nd['id']]
    filtered_decks.append(nd)

print(f"Yeni güverteler eklendikten sonra toplam güverte sayısı: {len(filtered_decks)}")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(filtered_decks, f, ensure_ascii=False, indent=2)

print(f"Başarıyla güncellendi: {DECKS_PATH}")
