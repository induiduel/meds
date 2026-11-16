# -*- coding: utf-8 -*-
"""
Rebuild Nephrology Glomerular & Tubulointerstitial Decks with High-Quality Medical Standards
1. learn-glomeruler-hastaliklar-nefrotik (24 Slayt)
2. learn-glomeruler-hastaliklar-nefritik (24 Slayt)
3. learn-tubulointerstisyel-hastaliklar (24 Slayt)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

print(f"Başlangıç güverte sayısı: {len(decks)}")

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
# 1. NEFROTİK SENDROM PATOLOJİSİ (24 SLAYT)
# ==============================================================================
nefrotik_slides = [
    make_slide(
        1,
        "Nefrotik Sendrom: Klinik Tanım ve Kardinal Bulgular",
        "Ağır Proteinüri, Hipoalbüminemi, Yaygın Ödem ve Lipidüri Tetradı",
        """Nefrotik sendrom, glomerüler filtrasyon bariyerinin plazma proteinlerine karşı seçici geçirgenliğini kaybetmesi sonucu ortaya çıkan ağır bir klinik tablodur. Bu sendrom tek başına bir hastalık olmayıp, glomerül kapiller duvarını hasarlayan çeşitli primer veya sekonder böbrek hastalıklarının ortak klinik tezahürüdür.

**1. Kardinal Tanı Kriterleri:**
• **Ağır Proteinüri:** Erişkinde >3.5 g/gün/1.73 m² veya çocuklarda >40 mg/saat/m² protein kaçağı mevcuttur. Filtrasyon bariyerindeki negatif yük kaybı veya yapısal gözenek genişlemesi nedeniyle plazma proteinleri idrara sızar.
• **Hipoalbüminemi:** Karaciğerin albümin sentez kapasitesinin idrarla atılan miktarı karşılayamaması sonucu serum albümin düzeyi <3.0 g/dL (genellikle <2.5 g/dL) seviyesine geriler.
• **Yaygın Ödem (Anazarka):** Azalan plazma onkotik basıncı sıvının interstisyuma kaçmasına yol açar; efektif arteriyel kan hacmi düşerek renin-anjiyotensin-aldosteron (RAAS) sistemini aktive eder ve sekonder sodyum-su retansiyonu ödemi şiddetlendirir.
• **Hiperlipidemi ve Lipidüri:** Hipoalbüminemi karaciğerde apolipoprotein B sentezini uyarır; eş zamanlı lipoprotein lipaz klirensi bozulur. İdrarda serbest lipid damlacıkları ve tubuler hücrelerce yutulan oval yağ cisimcikleri (Maltese cross polarizasyonu) görülür.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK KLİNİK EŞİK", "text": "Nefrotik düzeyde proteinüri erişkinde günlük >3.5 gramdır; bu düzeyin altındaki proteinüriler nefrotik sendrom tanısı için yetersizdir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV VURGUSU", "text": "Hipoalbüminemiye bağlı azalan onkotik basınç ve RAAS aktivasyonu periorbital ödemden başlayarak anazarka tipi jeneralize ödeme neden olur; idrarda Maltese cross veren oval yağ cisimcikleri patognomoniktir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-001",
            "question": "Aşağıdakilerden hangisi nefrotik sendromun klasik tanı kriterleri arasında yer almaz?",
            "options": [
                "A) Günlük 3.5 gramı aşan ağır proteinüri",
                "B) Serum albümin düzeyinin 3 g/dL altına düşmesi",
                "C) Belirgin dismorfik eritrositler ve eritrosit silindirleri içeren idrar sedimenti",
                "D) Karaciğerde kompansatuar sentez artışına bağlı hiperkolesterolemi",
                "E) Polarize ışık altında Maltese haçı görüntüsü veren oval yağ cisimcikleri"
            ],
            "correctAnswer": 2,
            "explanation": "Dismorfik eritrositler ve eritrosit silindirleri nefritik sendromun ayırt edici bulgusudur. Nefrotik sendromda idrar sedimenti genellikle hücresiz (bland) olup lipid damlacıkları ve hiyalen silindirler içerir."
        }
    ),
    make_slide(
        2,
        "Glomerüler Filtrasyon Bariyeri ve Podosit Biyolojisi",
        "Podosit Ayaksı Çıkıntıları, Slit Diyaframı ve Negatif Yük Bariyeri",
        """Glomerüler kapiller duvarı üç katmandan oluşan moleküler bir elek işlevi görür: pencereli (fenestre) endotel, glomerüler bazal membran (GBM) ve visseral epitel hücreleri (podositler).

**1. Glomerüler Bazal Membran (GBM):**
Tip IV kollajen, laminin, nidogen ve heparan sülfat proteoglikanlarından zengindir. İçerdiği zengin polianyonik heparan sülfat zincirleri sayesinde güçlü bir negatif elektriksel yük taşır ve albümin gibi negatif yüklü molekülleri elektrostatik olarak iter (yük seçiciliği).

**2. Podositler ve Slit Diyafram:**
Podositlerin birbiri içine geçen primer ve sekonder ayaksı çıkıntıları (pediseller) GBM üzerine oturur. Pediseller arasındaki filtrasyon yarıklarını nefrin, podosin ve CD2AP proteinlerinden oluşan 'slit diyafram' kapatır. Nefrin molekülleri podosit hücre içi aktin iskeletine podosin üzerinden bağlanarak yarık bütünlüğünü korur. Nefrotik sendromların büyük çoğunluğunda temel patolojik ortak payda slit diyafram mimarisinin dağılması ve podosit ayaksı çıkıntılarının silinmesidir (effacement).""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK GENETİK / MOLEKÜL", "text": "Konjenital nefrotik sendrom (Fin tipi) NPHS1 geni mutasyonuna (Nefrin eksikliği), steroid dirençli nefrotik sendrom ise NPHS2 mutasyonuna (Podosin eksikliği) bağlıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE SPOTU", "text": "Filtrasyon bariyerinde albüminin geçişini engelleyen en önemli faktörler slit diyaframın boyutsal gözenekleri ve heparan sülfatın oluşturduğu negatif yük bariyeridir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-002",
            "question": "Konjenital Fin tipi nefrotik sendromda primer defekt olan ve slit diyaframın ana iskeletini oluşturan protein aşağıdakilerden hangisidir?",
            "options": [
                "A) Podosin",
                "B) Nefrin",
                "C) Alfa-aktinin-4",
                "D) Tip IV kollajen alfa-5 zinciri",
                "E) Laminin beta-2"
            ],
            "correctAnswer": 1,
            "explanation": "Fin tipi konjenital nefrotik sendrom NPHS1 geninde mutasyon sonucu nefrin proteininin sentezlenememesiyle oluşur ve doğumdan itibaren masif proteinüri ile seyreder."
        }
    ),
    make_slide(
        3,
        "Nefrotik Sendromun Komplikasyonları ve Tromboemboli Riski",
        "Antitrombin III Kaybı, Enfeksiyon Yatkınlığı ve Protein Malnütrisyonu",
        """Nefrotik sendromda idrarla yalnızca albümin değil, birçok regülatör ve koruyucu plazma proteini de kaybedilir. Bu durum hayatı tehdit eden sistemik komplikasyonların gelişmesine zemin hazırlar.

**1. Hiperkoagülabilite ve Tromboemboli:**
• Karaciğerde fibrinojen ve Faktör V, VII, VIII sentezi artarken, molekül ağırlığı albümine yakın olan Antitrombin III (AT-III), Protein C ve Protein S idrarla kaybedilir.
• Trombosit agregasyonunda belirgin artış ve hipovolemiye bağlı hemokonsantrasyon hiperkoagülabiliteyi tetikler.
• **Renal Ven Trombozu:** Özellikle membranöz nefropati ve membranoproliferatif glomerülonefritte en sık görülen vasküler komplikasyondur; ani yan ağrısı ve makroskopik hematüri ile kendini gösterebilir. Derin ven trombozu ve pulmoner emboli mortalitenin başlıca nedenlerindendir.

**2. Enfeksiyon Yatkınlığı:**
İdrarla IgG ve komplemanın alternatif yol bileşeni Faktör B'nin kaybı, opsonizasyon kusuruna neden olur. Özellikle Streptococcus pneumoniae gibi kapsüllü bakterilere bağlı spontan bakteriyel peritonit ve pnömoni riski çocuklarda dramatik biçimde artar.""",
        [
            {"type": "warning", "badge": "🔴 HAYATİ KOMPLİKASYON", "text": "Nefrotik sendromlu hastada ani yan ağrısı, gross hematüri ve böbrek fonksiyonunda hızlı bozulma görüldüğünde akla ilk olarak Renal Ven Trombozu gelmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS BİLGİSİ", "text": "Nefrotik sendromda tromboz eğiliminin en önemli nedeni idrarla Antitrombin III kaybı ve hepatik fibrinojen sentezinin artmasıdır.", "color": "sky"}
        ],
        {
            "id": "prac-nef-003",
            "question": "Membranöz nefropatili bir hastada gelişen ani sol yan ağrısı ve makroskopik hematüride en olası tromboembolik komplikasyon aşağıdakilerden hangisidir?",
            "options": [
                "A) Splenik ven trombozu",
                "B) Renal ven trombozu",
                "C) Portal ven trombozu",
                "D) Mezenterik arter embolisi",
                "E) İntrakraniyal sinüs trombozu"
            ],
            "correctAnswer": 1,
            "explanation": "Nefrotik sendromda (özellikle Membranöz Nefropatide) AT-III kaybına bağlı hiperkoagülabilite sonucu en karakteristik komplikasyon renal ven trombozudur; akut yan ağrısı ve hematüriyle belirir."
        }
    ),
    make_slide(
        4,
        "Minimal Değişiklik Hastalığı (MDH): Etyopatogenez ve Epidemiyoloji",
        "Çocukluk Çağı Nefrotik Sendromunun 1 Numaralı Nedeni ve T Hücre Disfonksiyonu",
        """Minimal Değişiklik Hastalığı (Minimal Change Disease - Nil Disease), çocukluk çağındaki nefrotik sendrom olgularının %85-90'ından, erişkin olguların ise %10-15'inden sorumlu olan primer bir glomerülopatidir. En sık 2-6 yaş aralığında pik yapar.

**1. Patogenetik Mekanizma:**
• Klasik olarak bir T hücresi immün disregülasyon hastalığı kabul edilir. T lenfositlerden salgılanan dolaşımdaki permeabilite faktörleri (örneğin sitokinler, IL-13) podositlerin yüzey glikoproteinlerini ve GBM heparan sülfat yükünü hasarlar.
• Hodgkin lenfoma ve diğer lenfoproliferatif hastalıklarla güçlü bir birlikteliği vardır; ayrıca solunum yolu enfeksiyonları ve aşılanma sonrası tetiklenebilir.
• Histopatolojik olarak immün kompleks birikimi bulunmaz; ne kompleman tüketimi ne de antikor aracılı litik hasar izlenir.""",
        [
            {"type": "warning", "badge": "🔴 ETYOLOJİK BİRLİKTELİK", "text": "Erişkin bir hastada minimal değişiklik hastalığı saptandığında gizli bir Hodgkin Lenfoma varlığı mutlaka araştırılmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV SPOTU", "text": "MDH çocukluk çağı nefrotik sendromunun en sık nedenidir; kompleman düzeyleri (C3, C4) tamamen normaldir ve immün kompleks içermez.", "color": "sky"}
        ],
        {
            "id": "prac-nef-004",
            "question": "Çocukluk çağında ani başlayan yaygın ödem ve ağır proteinüri ile başvuran 4 yaşındaki hastada en olası primer glomerüler tanı aşağıdakilerden hangisidir?",
            "options": [
                "A) Membranöz nefropati",
                "B) Fokal segmental glomerüloskleroz",
                "C) Minimal değişiklik hastalığı",
                "D) Membranoproliferatif glomerülonefrit tip I",
                "E) IgA nefropatisi"
            ],
            "correctAnswer": 2,
            "explanation": "2-6 yaş grubu çocuklarda nefrotik sendromun en sık nedeni (%90) Minimal Değişiklik Hastalığıdır."
        }
    ),
    make_slide(
        5,
        "Minimal Değişiklik Hastalığı: Morfoloji ve Mikroskobik Ayrım",
        "Işık Mikroskobunda Normal Glomerül, Elektron Mikroskobunda Ayaksı Çıkıntı Silinmesi",
        """Minimal değişiklik hastalığının adı, ışık mikroskobunda glomerüllerin tamamen 'normal' veya normale çok yakın görünmesinden ileri gelir. Kesin tanı elektron mikroskopisi ile konur.

**1. Işık Mikroskopisi (LM):**
Glomerüllerde hiposelülarite veya belirgin proliferasyon yoktur. Kapiller lümenler açıktır, GBM kalınlaşması izlenmez. Tek ışık mikroskobu bulgusu, tubulus epitel hücrelerinde geri emilen lipid ve protein damlacıklarının birikmesidir; bu nedenle tarihsel olarak 'Lipoid Nefroz' adını almıştır.

**2. İmmünofloresan Mikroskopi (İF):**
Tamamen negatiftir; glomerülde immünglobulin (IgG, IgA, IgM) veya kompleman (C3, C1q) depolanması izlenmez.

**3. Elektron Mikroskopisi (EM):**
Hastalığın patognomonik morfolojik bulgusu visseral epitel hücrelerinin ayaksı çıkıntılarının (pedisellerinin) diffüz olarak silinmesi ve basıklaşmasıdır (effacement). GBM yapısı, bazal lamina kalınlığı ve endotel pencereleri tamamen intaktır.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "MDH tanısı için Işık Mikroskobu ve İmmünofloresan mikroskobu NEGATİF / NORMAL olmalı, patoloji sadece Elektron Mikroskobunda podosit pedisellerinin silinmesiyle gösterilmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KLASİK TUS SORUSU", "text": "Işık mikroskobunda glomerülleri tamamen normal görünen, immünofloresanda birikim saptanmayan, elektron mikroskobunda podosit ayaksı çıkıntılarında yaygın silinme izlenen hastalık Minimal Değişiklik Hastalığıdır.", "color": "sky"}
        ],
        {
            "id": "prac-nef-005",
            "question": "Böbrek biyopsisinde ışık ve immünofloresan mikroskobunda belirgin patoloji izlenmeyen, ancak elektron mikroskobunda visseral epitel hücrelerinin ayaksı çıkıntılarında yaygın silinme saptanan hastada tanı nedir?",
            "options": [
                "A) Erken evre Membranöz nefropati",
                "B) Minimal değişiklik hastalığı",
                "C) Alport sendromu",
                "D) Fokal segmental glomerüloskleroz hücresel varyant",
                "E) C3 glomerulopatisi"
            ],
            "correctAnswer": 1,
            "explanation": "LM ve İF tamamen normal iken EM'de podosit ayaksı çıkıntılarının silinmesi Minimal Değişiklik Hastalığı için tanı koydurucudur."
        }
    ),
    make_slide(
        6,
        "Minimal Değişiklik Hastalığı: Proteinüri Selektivitesi ve Tedavi Yanıtı",
        "Yüksek Selektif Albüminüri ve Steroid Tedavisine Dramatik Dramatik Yanıt",
        """Minimal değişiklik hastalığı klinik ve terapötik açıdan diğer nefrotik sendrom nedenlerinden çok belirgin özellikleriyle ayrılır.

**1. Selektif Proteinüri:**
Filtrasyon bariyerindeki hasar yapısal bir delinmeden ziyade heparan sülfat kaynaklı negatif yük bariyerinin kaybına dayandığı için idrarla kaybedilen proteinlerin %90'ından fazlası düşük molekül ağırlıklı albümindir. Büyük molekül ağırlıklı proteinler (örneğin IgG, alfa-2 makroglobulin) idrara geçemez. Bu tabloya 'yüksek derecede selektif proteinüri' denir.

**2. Klinik Seyir ve Steroid Yanıtı:**
• Çocuklarda kortikosteroid tedavisine (prednizon) yanıt oranı %90'ın üzerindedir; proteinüri genellikle ilk 2-4 hafta içinde tamamen geriler.
• Hastalarda hipertansiyon, hematüri ve azotemi son derece nadirdir. Renal fonksiyonlar korunur ve son dönem böbrek yetmezliğine (SDBY) gidiş %5'in altındadır.
• En önemli klinik problem sık relapslardır; relapslar steroid dozunun azaltılması veya kesilmesiyle tetiklenebilir ancak steroid duyarlılığı genellikle devam eder.""",
        [
            {"type": "clinical", "badge": "🔴 TERAPÖTİK ÖNEM", "text": "Steroid tedavisine dramatik yanıt MDH'nin klinik imzasıdır; steroid tedavisine direnç gelişmesi tanının FSGS yönünde revize edilmesini gerektirir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Selektif proteinüri (idrarda sadece albümin atılımı, IgG atılmaması) Minimal Değişiklik Hastalığına özgüdür; diğer nefrotik tablolarda proteinüri non-selektiftir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-006",
            "question": "Minimal Değişiklik Hastalığı ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Proteinüri yüksek oranda selektiftir ve baskın olarak albüminden oluşur",
                "B) Çocuk hastalarda kortikosteroid tedavisine yanıt mükemmeldir (%90+)",
                "C) Serum kompleman düzeyleri (C3 ve C4) belirgin derecede düşüktür",
                "D) İlerleyici son dönem böbrek yetmezliği gelişimi son derece nadirdir",
                "E) Sık relapslar görülebilmesine rağmen uzun dönem prognozu çok iyidir"
            ],
            "correctAnswer": 2,
            "explanation": "Minimal Değişiklik Hastalığında kompleman aktivasyonu ve tüketimi gerçekleşmez; serum C3 ve C4 düzeyleri tamamen normaldir."
        }
    ),
    make_slide(
        7,
        "Fokal Segmental Glomerüloskleroz (FSGS): Tanım ve Sınıflama",
        "Erişkinde Nefrotik Sendromun En Sık Primer Nedeni ve Podosit Hasarı",
        """Fokal Segmental Glomerüloskleroz (FSGS), bazı glomerüllerin (fokal) sadece bir kısmında (segmental) kapiller lümenlerin kollapsı, hyalinozis ve skleroz ile karakterize ilerleyici bir glomerülopatidir. Günümüzde Amerika ve birçok gelişmiş ülkede erişkinlerde nefrotik sendromun en sık primer nedenidir.

**1. Sınıflandırma ve Etyoloji:**
• **Primer (İdiyopatik) FSGS:** Dolaşımdaki henüz tam tanımlanamamış permeabilite faktörlerine bağlı gelişir; ani başlangıçlı nefrotik sendrom tablosuyla gelir.
• **Genetik (Kalıtsal) FSGS:** Podosit iskelet ve slit diyafram proteinlerini kodlayan gen mutasyonları: *NPHS2* (podosin), *ACTN4* (alfa-aktinin-4), *TRPC6* ve *INF2*. Steroid tedavisine tamamen dirençlidir.
• **Sekonder FSGS:**
  1. *Glomerüler Hiperfiltrasyon ve Aşırı Yük:* Renal ablasyon, tek böbrek, vezikoüreteral reflü (reflü nefropatisi), morbid obezite ve orak hücreli anemi.
  2. *Viral Enfeksiyonlar:* HIV (özellikle kollaps varyant), Parvovirus B19, CMV.
  3. *İlaç ve Toksinler:* Pamidronat, interferon tedavisi, eroin kullanımı (eroin nefropatisi).""",
        [
            {"type": "warning", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "FSGS fokal bir lezyondur; biyopside medullaya yakın jukstamedüller glomerüller erken dönemde tutulduğundan, yüzeyel kortikal biyopsilerde lezyon atlanıp yanlışlıkla MDH tanısı konabilir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Morbid obezite, vezikoüreteral reflü, tek böbrek hiperfiltrasyonu ve HIV enfeksiyonu sekonder FSGS'nin en karakteristik nedenleridir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-007",
            "question": "Aşağıdakilerden hangisi Fokal Segmental Glomerüloskleroz (FSGS) gelişimine yol açan genetik mutasyonlardan biri değildir?",
            "options": [
                "A) NPHS2 (Podosin)",
                "B) ACTN4 (Alfa-aktinin-4)",
                "C) TRPC6",
                "D) PLA2R1 (Fosfolipaz A2 reseptörü)",
                "E) INF2"
            ],
            "correctAnswer": 3,
            "explanation": "PLA2R1 mutasyonu değil, PLA2R antijenine karşı otoantikor gelişimi Primer Membranöz Nefropatinin patogenezinde rol oynar. Diğerleri FSGS ile ilişkili podosit genleridir."
        }
    ),
    make_slide(
        8,
        "FSGS: Morfolojik Özellikler ve Histopatolojik Varyantlar",
        "Skleroz, Hyalinozis, Köpüksü Hücreler ve Columbia Sınıflaması",
        """FSGS morfolojik olarak podosit hasarının geri dönüşsüz bir skleroz evresine ilerlemesini yansıtır.

**1. Işık Mikroskopisi (LM):**
• Tutulan glomerüllerde kapiller yumak kollabe olur, ekstraselüler matriks artışı (skleroz) görülür.
• Plazma proteinlerinin hasarlı damar duvarında birikmesiyle eozinofilik aselüler kitleler (**hyalinozis**) oluşur. Lipid yüklü makrofajlar (**köpüksü hücreler**) sklerotik segmentlerde sıkça izlenir.
• Biyopside lezyon jukstamedüller bölgeden başlar.

**2. İmmünofloresan (İF):**
Sklerotik ve hyalinize segmentlerde non-spesifik IgM ve C3 tuzaklanması (trapping) izlenir. Gerçek bir immün kompleks depolanması yoktur.

**3. Elektron Mikroskopisi (EM):**
Sklerotik olmayan alanlarda bile podosit ayaksı çıkıntılarında yaygın silinme izlenir; podositlerin bazal membrandan ayrıldığı (denudasyon) alanlar sklerozun başlangıç noktasını oluşturur.

**4. Columbia Morfolojik Varyantları:**
1. *NOS (Not Otherwise Specified):* En sık tip.
2. *Kollaps Varyant:* Glomerül kapiller yumağının büzüşmesi ve podosit hiperplazisi; HIV ilişkili nefropatinin (HIVAN) tipik bulgusudur, en kötü prognoza sahiptir.
3. *Tip Varyant:* Tubul çıkış kutbunda lezyon; en iyi prognoza sahiptir.
4. *Selüler Varyant:* Endokapiller hiperhücresellik.
5. *Perihiler Varyant:* Sekonder hiperfiltrasyon formlarında baskındır.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Kollaps varyant FSGS; glomerül kapillerlerinin tamamen çökmesi ve podositlerin psödohilal şeklinde çoğalmasıyla seyreder; HIVAN'ın klasik tablosudur ve hızla diyalize götürür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / KOMİTE SORUSU", "text": "FSGS varyantları içinde prognozu en iyi olan Tip varyant; en agresif ve böbrek yetmezliğine en hızlı ilerleyen ise Kollaps varyanttır.", "color": "sky"}
        ],
        {
            "id": "prac-nef-008",
            "question": "HIV pozitif bir hastada hızlı ilerleyen nefrotik sendrom ve böbrek yetmezliği saptanıyor. Biyopside glomerül kapillerlerinin kollabe olduğu ve podosit proliferasyonu izlendiğinde en olası FSGS morfolojik varyantı hangisidir?",
            "options": [
                "A) Tip varyant",
                "B) Perihiler varyant",
                "C) Kollaps varyant",
                "D) Hücresel varyant",
                "E) NOS varyant"
            ],
            "correctAnswer": 2,
            "explanation": "HIV ilişkili nefropatide (HIVAN) en karakteristik histolojik form kapiller kollaps ve belirgin podosit hipertrofisi/hiperplazisi ile seyreden Kollaps varyant FSGS'dir."
        }
    ),
    make_slide(
        9,
        "FSGS: Klinik Özellikler, Steroid Direnci ve Transplant Nüksü",
        "Non-Selektif Proteinüri, Hipertansiyon ve %25-50 Renal Allogreft Nüksü",
        """FSGS klinik tablosu, tedavi yanıtı ve uzun dönem akıbetiyle Minimal Değişiklik Hastalığından radikal biçimde farklılaşır.

**1. Klinik Belirtiler:**
• MDH'den farklı olarak proteinüri **non-selektiftir** (idrarda albüminin yanı sıra yüksek moleküler ağırlıklı immünglobulinler de atılır).
• Hastaların %50'sinde mikroskopik hematüri, hipertansiyon ve başvuru anında azalmış glomerüler filtrasyon hızı (azotemi) mevcuttur.

**2. Tedavi Yanıtı ve Prognoz:**
• Primer FSGS kortikosteroid tedavisine zayıf yanıt verir; hastaların %50'sinden fazlası steroid dirençlidir. Kalsinörin inhibitörleri veya immünsüpresif kombinasyonlar gerekir.
• Olguların en az %50'si 10 yıl içinde son dönem böbrek yetmezliğine (SDBY) ilerler.

**3. Renal Transplantasyon ve Nüks Riski:**
Primer FSGS tanısıyla böbrek nakli yapılan hastaların **%25-50'sinde** hastalık nakledilen böbrekte (allogreft) nüks eder. Bazı hastalarda nakilden saatler veya günler sonra masif proteinüri başlaması, kanda dolaşan toksik bir permeabilite faktörünün (örneğin suPAR, kardiyotrofin benzeri sitokin-1) varlığını kesin olarak kanıtlar.""",
        [
            {"type": "clinical", "badge": "🔴 KRİTİK NÜKS RİSKİ", "text": "Primer FSGS'de böbrek nakli sonrası allogreftte nüks oranı %25-50'dir; nüks eden olgularda plazmaferez ile dolaşımdaki permeabilite faktörünün temizlenmesi hedeflenir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV SPOTU", "text": "MDH ile FSGS ayrımında: FSGS'de proteinüri non-selektiftir, hipertansiyon ve hematüri sıktır, steroide yanıt kötüdür ve böbrek yetmezliği gelişir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-009",
            "question": "Primer FSGS nedeniyle son dönem böbrek yetmezliğine girerek böbrek nakli yapılan bir hastada nakilden 48 saat sonra ağır nefrotik proteinüri başlamasını en iyi açıklayan patofizyolojik mekanizma hangisidir?",
            "options": [
                "A) Akut hücresel doku reddi (rejeksiyon)",
                "B) Dolaşımdaki podosit toksik permeabilite faktörünün allogrefte hasar vermesi",
                "C) Siklosporin toksisitesine bağlı tubuler nekroz",
                "D) Vericide var olan asemptomatik nefrit",
                "E) Sitomegalovirüs enfeksiyonu"
            ],
            "correctAnswer": 1,
            "explanation": "Primer FSGS'nin nakil sonrası saatler-günler içinde allogreftte hızla nüks etmesi, dolaşımda podosit slit diyaframını bozan dolaşan bir permeabilite faktörünün varlığıyla açıklanır."
        }
    ),
    make_slide(
        10,
        "Membranöz Nefropati: Patogenez ve Otoantikorlar",
        "Erişkinlerde İmmün Kompleks Nefrotik Sendromu ve Anti-PLA2R Otoantikoru",
        """Membranöz Nefropati (MN), glomerül kapiller duvarının subepitelyal yüzeyinde immün kompleks birikimi ve GBM'nin diffüz kalınlaşması ile karakterize primer bir nefrotik sendrom nedenidir. İleri yaş ve beyaz ırkta erişkin nefrotik sendromun en sık nedenlerindendir.

**1. Primer (İdiyopatik) Membranöz Nefropati (%75-85):**
Otoimmün bir hastalıktır. Olguların %70-80'inde podosit yüzeyinde bulunan **M-tipi Fosfolipaz A2 Reseptörüne (PLA2R)** karşı gelişen otoantikorlar (özellikle IgG4 alt sınıfı) saptanır. İkinci en sık saptanan antijen ise **THSD7A**'dır (trombospondin tip 1 domain içeren 7A). Antikorlar dolaşımdaki antijenle değil, doğrudan podosit yüzeyindeki bu hedeflere bağlanarak in situ immün kompleksler oluşturur. Kompleman aktivasyonu (C5b-9 membran atak kompleksi) podosit hasarına yol açar.

**2. Sekonder Membranöz Nefropati (%15-25):**
• Maligniteler: Akciğer, kolon, mide karsinomları (özellikle 60 yaş üstünde gizli kanser habercisidir).
• Sistemik Enfeksiyonlar: Kronik Hepatit B, Hepatit C, Sifilis.
• Otoimmün Hastalıklar: Sistemik Lupus Eritematozus (SLE Sınıf V).
• İlaçlar: NSAİİ, penisilamin, altın tuzları, kaptopril.""",
        [
            {"type": "warning", "badge": "🔴 ONKOLOJİK ALARM", "text": "60 yaş üstünde anti-PLA2R negatif saptanan membranöz nefropatili bir hastada akciğer ve gastrointestinal sistem maligniteleri mutlaka taranmalıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS BİLGİSİ", "text": "Primer membranöz nefropatide podosite karşı oluşan spesifik otoantikor anti-PLA2R (M-tipi fosfolipaz A2 reseptörü) antikorudur ve hastalığın aktivitesiyle koreledir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-010",
            "question": "Erişkin bir hastada primer membranöz nefropati patogenezinde podosit yüzeyindeki hangi endojen antijene karşı gelişen otoantikorlar majör rol oynar?",
            "options": [
                "A) Megalin",
                "B) M-tipi Fosfolipaz A2 Reseptörü (PLA2R)",
                "C) Nefrin",
                "D) Podokaliksin",
                "E) Glomerüler bazal membran tip IV kollajen alfa-3 zinciri"
            ],
            "correctAnswer": 1,
            "explanation": "Primer membranöz nefropatili olguların yaklaşık %70-80'inde podosit M-tipi fosfolipaz A2 reseptörüne (PLA2R) karşı otoantikorlar saptanır."
        }
    ),
    make_slide(
        11,
        "Membranöz Nefropati: Morfoloji, 'Spike and Dome' ve Gümüşleme",
        "Diffüz Subepitelyal Birikimler ve Bazal Membran Dikenleşmesi",
        """Membranöz nefropatinin morfolojisi immün komplekslerin subepitelyal alana yerleşmesi ve bazal membranın bu birikimlere verdiği reaksiyonla şekillenir.

**1. Işık Mikroskopisi (LM):**
• Glomerüllerde hücresel proliferasyon izlenmez (normoselülerdir).
• Glomerül kapiller duvarlarında diffüz ve homojen bir kalınlaşma mevcuttur.
• **Gümüşleme Boyası (Jones / PASM):** GBM'den subepitelyal depozitlerin arasına doğru uzanan matriks uzantıları **'diken' (spike)** görünümü oluşturur. Zamanla birikimlerin üzeri GBM materyaliyle örtülerek **'kubbe' (dome)** görünümü meydana gelir (**'Spike and Dome' deseni**).

**2. İmmünofloresan (İF):**
Glomerül kapiller duvarları boyunca tipik **diffüz granüler IgG ve C3** birikimi izlenir.

**3. Elektron Mikroskopisi (EM):**
GBM ile podosit arasında **subepitelyal elektron-yoğun birikimler (depozitler)** mevcuttur. Podosit ayaksı çıkıntılarında yaygın silinme görülür. Zamanla depozitler GBM içine gömülür ve rezorbe olarak arkalarında güve yeniği görünümü bırakır.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Gümüş boyamada izlenen 'Spike and Dome' (Diken ve Kubbe) manzarası Membranöz Nefropati için patognomoniktir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE KLASİĞİ", "text": "Membranöz nefropatide immün kompleksler podositin altında (SUBEPİTELYAL) yerleşir ve İF'de diffüz granüler IgG/C3 paterni verir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-011",
            "question": "Nefrotik sendromlu bir hastanın böbrek biyopsisinde gümüşleme boyamasında glomerül bazal membranında tipik 'spike and dome' (diken ve kubbe) manzarası ve İF'de kapiller duvarda granüler IgG birikimi saptanıyor. Tanı nedir?",
            "options": [
                "A) Poststreptokokkal glomerülonefrit",
                "B) Membranöz nefropati",
                "C) Membranoproliferatif glomerülonefrit tip I",
                "D) Goodpasture hastalığı",
                "E) Minimal değişiklik hastalığı"
            ],
            "correctAnswer": 1,
            "explanation": "Gümüşleme boyasında 'spike and dome' görüntüsü ve granüler subepitelyal IgG birikimi Membranöz Nefropatinin patognomonik morfolojik bulgusudur."
        }
    ),
    make_slide(
        12,
        "Membranöz Nefropati: Klinik Seyir ve 'Üçte Bir' Kuralı",
        "Sinsi Başlangıç, Renal Ven Trombozu ve Spontan Remisyon Olasılığı",
        """Membranöz nefropati sinsi seyirli, yavaş ilerleyen bir klinik tablodur.

**1. Klinik Özellikler:**
• Hastalar genellikle yavaş gelişen bacak ödemi ve halsizlikle başvurur. Proteinüri masif ve non-selektiftir; mikroskopik hematüri %30-40 olguda eşlik eder ancak belirgin nefritik bulgular (eritrosit silindiri, oligüri) görülmez.
• Glomerülonefritler içinde tromboembolik komplikasyon (özellikle **Renal Ven Trombozu**) sıklığının en yüksek olduğu hastalıktır.

**2. Doğal Seyir ('Üçte Bir' Kuralı):**
• **%30-35:** Hastalık hiçbir tedavi almadan kendiliğinden (spontan) tam veya kısmi remisyona girer.
• **%30-35:** Proteinüri kalıcı olarak devam eder ancak renal fonksiyonlar yıllarca stabil kalır.
• **%30-35:** 10-20 yıllık süreçte yavaş ve ilerleyici olarak son dönem böbrek yetmezliğine (SDBY) ilerler.

**3. Tedavi Yaklaşımı:**
Kendiliğinden remisyon olasılığı nedeniyle ilk 6 ay konservatif tedavi (ACEI/ARB ile proteinüri azaltılması, tansiyon kontrolü) uygulanır. Ağır veya ilerleyici olgularda immünsüpresif rejimler (Ponticelli protokolü: siklofosfamid + steroid veya Rituksimab) tercih edilir.""",
        [
            {"type": "clinical", "badge": "🔴 KLİNİK KURAL", "text": "Membranöz nefropatide spontan remisyon oranı yaklaşık %33 olduğu için hemen agresif immünsüpresyon başlanmaz; ilk 6 ay ACE inhibitörleri ile konservatif izlem yapılır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Nefrotik sendromlar arasında renal ven trombozunun en sık eşlik ettiği antite Membranöz Nefropatidir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-012",
            "question": "Membranöz nefropatinin klinik seyri ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Hastaların tümü ilk 1 yıl içinde hızla son dönem böbrek yetmezliğine girer",
                "B) Olguların yaklaşık üçte birinde kendiliğinden spontan remisyon görülebilir",
                "C) Steroid monoterapisine çocuklardaki MDH gibi %90 yanıt verir",
                "D) Proteinüri daima yüksek selektif albüminüriden ibarettir",
                "E) Tromboembolik komplikasyonlar bu hastalıkta hiç görülmez"
            ],
            "correctAnswer": 1,
            "explanation": "Membranöz nefropatide kabaca üçte bir kuralı geçerlidir; hastaların yaklaşık 1/3'ünde hastalık kendiliğinden remisyona girer."
        }
    ),
    make_slide(
        13,
        "Membranoproliferatif Glomerülonefrit (MPGN) Tip I: Klasik İmmün Kompleks Yolu",
        "Subendotelyal İmmün Kompleksler, Mezangiyokapiller Proliferasyon ve Hepatit C",
        """Membranoproliferatif Glomerülonefrit (MPGN), glomerüllerde hem mezangiyal hücre proliferasyonu hem de kapiller duvar kalınlaşması ile karakterize, miks nefrotik-nefritik tablo oluşturan bir glomerülopatidir.

**1. MPGN Tip I Patogenezi:**
• Klasik kompleman yolunun aktivasyonu ile seyreder. Dolaşımdaki çözünür antijen-antikor kompleksleri glomerül kapiller duvarının endotel altına (**subendotelyal**) ve mezangiyuma oturur.
• En sık sekonder neden **Kronik Hepatit C virüsü (HCV)** enfeksiyonu ve buna bağlı gelişen tip II mikst kriyoglobulinemidir. Diğer nedenler Sistemik Lupus Eritematozus (SLE), Hepatit B ve subakut bakteriyel endokardittir.

**2. Laboratuvar Bulgusu:**
Klasik kompleman yolunun tükenmesine bağlı olarak serumda hem **C3** hem de **C4** düzeyleri belirgin derecede düşüktür.""",
        [
            {"type": "warning", "badge": "🔴 VİRAL İLİŞKİ", "text": "Hepatit C pozitif, purpura, artralji ve mikst nefrotik/nefritik tablosu olan hastada ilk akla gelmesi gereken tanı MPGN Tip I ve Kriyoglobulinemidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "MPGN Tip I'de immün kompleksler SUBENDOTELYAL yerleşimlidir; hem C3 hem C4 seviyeleri düşüktür.", "color": "sky"}
        ],
        {
            "id": "prac-nef-013",
            "question": "Kronik Hepatit C enfeksiyonu olan bir hastada bacaklarda purpura, eklem ağrısı ve mikst nefrotik sendrom tablosu gelişiyor. Biyopside subendotelyal immün kompleksler saptanıyor. En olası tanı hangisidir?",
            "options": [
                "A) Membranöz nefropati",
                "B) MPGN Tip I (Kriyoglobulinemik GN)",
                "C) Minimal değişiklik hastalığı",
                "D) Poststreptokokkal GN",
                "E) Dens depozit hastalığı"
            ],
            "correctAnswer": 1,
            "explanation": "Hepatit C ve kriyoglobulinemi ile en kuvvetli ilişkisi olan glomerüler patoloji subendotelyal birikimlerle giden MPGN Tip I'dir."
        }
    ),
    make_slide(
        14,
        "MPGN Morfolojisi: Çift Kontur ('Tram-Track') Görünümü ve Lobüler Patern",
        "Mezangiyal İnterpozisyon, Hücresel İnfiltrasyon ve Lobülasyon",
        """MPGN'nin histopatolojik görünümü glomerülün en dramatik biçimde yeniden modellendiği lezyonlardan biridir.

**1. Işık Mikroskopisi (LM):**
• **Lobüler Glomerül Mimarisi:** Glomerüller ileri derecede büyümüştür; mezangiyal hücre proliferasyonu ve matriks artışı glomerül yumaklarına belirgin bir lobüler ('karnabahar' benzeri) hat kazandırır. Endokapiller lökosit infiltrasyonu lümenleri daraltır.
• **Çift Kontur / Tram-Track (Tren Rayı) Manzarası:** Mezangiyal hücre sitoplazmik uzantıları bazal membran ile endotel arasına doğru uzanır (**mezangiyal interpozisyon**). Bu süreçte yeni bazal membran materyali sentezlenir ve gümüşleme (Jones) boyamasında kapiller duvarda iki paralel hat (**tram-track**) şeklinde çift kontur görünümü oluşur.

**2. İmmünofloresan (İF):**
Kapiller duvar boyunca ve mezangiyumda granüler IgG, IgM ve C3 birikimi izlenir.

**3. Elektron Mikroskopisi (EM):**
Subendotelyal elektron-yoğun depozitler ve araya girmiş mezangiyal hücre uzantıları (interpozisyon) kesin olarak gösterilir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KOD", "text": "Gümüşleme boyasında izlenen 'Tram-Track' (tren rayı / çift kontur) görünümü MPGN Tip I ve mezangiyal interpozisyonun klasik göstergesidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 TUS / KOMİTE SORUSU", "text": "Tram-track görünümünün oluşumundaki temel hücresel mekanizma 'mezangiyal hücrelerin endotel altına doğru interpozisyonu ve yeni GBM sentezlemesi'dir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-014",
            "question": "Böbrek biyopsisinde glomerüllerde belirgin lobülasyon, mezangiyal interpozisyon ve gümüş boyamada kapiller duvarda 'tram-track' (tren rayı / çift kontur) görünümü saptanan hastada en olası tanı nedir?",
            "options": [
                "A) Membranöz nefropati",
                "B) Membranoproliferatif glomerülonefrit Tip I",
                "C) Minimal değişiklik hastalığı",
                "D) Fokal segmental glomerüloskleroz",
                "E) İnce bazal membran hastalığı"
            ],
            "correctAnswer": 1,
            "explanation": "Glomerülde lobüler mimari, mezangiyal interpozisyon ve gümüş boyamada 'tram-track' (çift kontur) görünümü MPGN Tip I'in ayırt edici morfolojisidir."
        }
    ),
    make_slide(
        15,
        "C3 Glomerülopatisi ve Yoğun Birikim Hastalığı (Dense Deposit Disease)",
        "Alternatif Kompleman Yolu Disregülasyonu, C3 Nefritik Faktör ve İntramembranöz Kurdele",
        """C3 Glomerülopatisi, eski sınıflamadaki MPGN Tip II'yi de içine alan, immünglobulinlerden bağımsız olarak alternatif kompleman yolunun kontrolsüz aktivasyonu ile karakterize özel bir hastalıktır.

**1. Patogenetik Mekanizma:**
• Klasik yol değil, **Alternatif kompleman yolu** aşırı aktiftir.
• **C3 Nefritik Faktör (C3NeF):** Hastaların %80'inde bulunan bir otoantikordur. Alternatif yolun C3 konvertaz enzimini (C3bBb) bağlayarak stabilize eder; enzimin Faktör H tarafından inaktivasyonunu engeller. Böylece C3 sürekli parçalanır ve tükenir.
• Faktör H, Faktör I veya CD46 gen mutasyonları da aynı disregülasyona yol açar.
• Serumda **C3 aşırı düşüktür**, ancak klasik yol etkilenmediği için **C4 düzeyi tamamen normaldir**.

**2. Morfolojik Alt Tipler:**
• **Yoğun Birikim Hastalığı (Dense Deposit Disease - DDD):** Elektron mikroskobunda GBM laminasında aşırı yoğun, kurdele benzeri (ribbon-like) kesintisiz intramembranöz depozitler izlenir.
• **C3 Glomerülonefriti (C3GN):** Depozitler daha düzensiz olup subendotelyal, mezangiyal ve subepitelyal alana dağılmıştır.
• İF'de yalnızca parlak C3 pozitifliği vardır; IgG ve immünglobulinler tamamen negatiftir.""",
        [
            {"type": "warning", "badge": "🔴 SEROLOJİK AYRIM", "text": "C3 düzeyinin çok düşük, ancak C4 düzeyinin normal olduğu durumlarda alternatif yol disregülasyonu (C3 Nefritik Faktör / C3 Glomerülopatisi) düşünülmelidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "EM'de glomerüler bazal membranın lamina densasında homojen, kurdele benzeri aşırı elektron-yoğun birikim izlenen hastalık Yoğun Birikim Hastalığıdır (eski MPGN Tip II).", "color": "sky"}
        ],
        {
            "id": "prac-nef-015",
            "question": "Serum C3 düzeyi aşırı düşük, C4 düzeyi normal saptanan bir hastanın böbrek biyopsisinde elektron mikroskobunda GBM laminasında kurdele şeklinde kesintisiz yoğun birikimler ve İF'de izole C3 pozitifliği saptanıyor. Bu tabloda sorumlu otoantikor hangisidir?",
            "options": [
                "A) Anti-PLA2R",
                "B) C3 Nefritik Faktör (C3NeF)",
                "C) Anti-GBM antikorları",
                "D) c-ANCA (PR3-ANCA)",
                "E) Anti-dsDNA"
            ],
            "correctAnswer": 1,
            "explanation": "C3 Nefritik Faktör (C3NeF), C3 konvertazı stabilize ederek kontrolsüz alternatif yol aktivasyonuna yol açar ve Yoğun Birikim Hastalığının (DDD) temel patogenetik nedenidir."
        }
    ),
    make_slide(
        16,
        "Diyabetik Nefropati: Patogenez, Nodüler Skleroz (Kimmelstiel-Wilson) ve Mikroalbüminüri",
        "AGE Ürünleri, Glomerüler Hiperfiltrasyon, Kapsüler Damla ve Fibrin Başlığı",
        """Diyabetik nefropati, dünyada ve ülkemizde son dönem böbrek yetmezliğine (diyaliz ve nakil ihtiyacı) yol açan **1 numaralı nedendir**. Diyabetik mikroanjiyopatinin böbrek tutulumudur.

**1. Patogenez:**
• Kronik hiperglisemi dokularda **İleri Glikozilasyon Son Ürünleri (AGE)** oluşturur. AGE reseptörleri (RAGE) üzerinden TGF-beta salınarak mezangiyal matriks sentezi ve GBM kollajen üretimi artar.
• Glukoz kaynaklı eferent arteriyol vazokonstriksiyonu intraglomerüler intrakapiller hidrostatik basıncı artırarak hiperfiltrasyon hasarına yol açar.

**2. Morfolojik Özellikler:**
• **Diffüz Mezangiyal Skleroz:** En sık görülen lezyondur; tüm glomerüllerde PAS pozitif matriks artışı ve GBM diffüz kalınlaşması izlenir.
• **Nodüler Glomerüloskleroz (Kimmelstiel-Wilson Lezyonları):** Glomerül lobüllerinin merkezinde ovoid, aselüler, laminasyon gösteren eozinofilik PAS-pozitif nodüllerdir. Diyabetik nefropati için **patognomoniktir**.
• **Eksüdatif Lezyonlar:** Bowman kapsülünün iç yüzeyinde 'kapsüler damla' (capsular drop) ve glomerül kapiller lümeninde biriken eozinofilik 'fibrin başlığı' (fibrin cap).
• **Arteriyoloskleroz:** Hem afferent hem de eferent arteriyolde hyalen kalınlaşma (hyalen arteriyoloskleroz) görülmesi diyabete son derece özgüdür.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Kimmelstiel-Wilson nodülleri (nodüler glomerüloskleroz) diyabetik nefropati için patognomoniktir; nodüller PAS pozitif olup merkezinde hücre barındırmaz.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SORUSU", "text": "Hem afferent hem de eferent arteriyolde birlikte hyalen arteriyoloskleroz saptanması en tipik olarak Diabetes Mellitus'ta görülür (Hipertansiyonda sadece afferent tutulur).", "color": "sky"}
        ],
        {
            "id": "prac-nef-016",
            "question": "20 yıldır tip 2 diyabet tanısı olan hastanın böbrek biyopsisinde glomerüllerde PAS pozitif ovoid aselüler nodüler skleroz (Kimmelstiel-Wilson) ve hem afferent hem eferent arteriyolde hyalinozis izleniyor. Bu tablonun erken klinik habercisi hangisidir?",
            "options": [
                "A) Makroskopik ağrısız hematüri",
                "B) Mikroalbüminüri (30-300 mg/gün albümin atılımı)",
                "C) İdrarda lökosit silindirleri",
                "D) Akut oligüri ve anüri",
                "E) Serum C3 kompleman düşüklüğü"
            ],
            "correctAnswer": 1,
            "explanation": "Diyabetik nefropatinin en erken klinik göstergesi mikroalbüminüridir (30-300 mg/gün albümin atılımı); erken evrede ACE inhibitörleri ile hasar geri döndürülebilir."
        }
    ),
    make_slide(
        17,
        "Renal Amiloidoz: Patoloji, Kongo Kırmızısı ve Polarizasyon",
        "Amiloid Fibrilleri, Mezangiyal Genişleme ve Yeşil Refleks (Apple-Green Birefringence)",
        """Amiloidoz, anormal katlanmış çözünmeyen fibriler proteinlerin hücre dışı dokularda depolanmasıyla giden sistemik veya lokalize bir hastalıktır. Böbrek, sistemik amiloidozun en sık ve en ağır tutulduğu organdır.

**1. Başlıca Amiloid Tipleri:**
• **AL Amiloidoz:** Plazma hücre diskrazileri (Multipl Miyelom) sonucu immünglobulin hafif zincirlerinin (özellikle lambda) üretilip birikmesidir.
• **AA Amiloidoz:** Kronik enflamatuar hastalıklar (Ailevi Akdeniz Ateşi - FMF, Romatoid Artrit, Bronşektazi, Osteomiyelit) sırasında karaciğerden sentezlenen Serum Amiloid A (SAA) proteininin birikmesidir.

**2. Morfolojik Özellikler ve Tanı Yöntemleri:**
• **Işık Mikroskopisi (H&E):** Glomerüllerde mezangiyumdan başlayarak kapiller duvarları daraltan amorf, aselüler, homojen pembe (eozinofilik) madde birikimi izlenir. Glomerüller devleşir ancak tamamen avasküler ve aselüler hale gelir.
• **Kongo Kırmızısı (Congo Red) Boyası:** Amiloid depozitleri ışık mikroskobunda pembe-turuncu boyanır.
• **Polarize Mikroskopi:** Kongo kırmızısı ile boyanmış kesitler polarize ışık altında incelendiğinde amiloid fibrillerinin beta-kırmalı yapısı nedeniyle **karakteristik elma yeşili çift kırılma (apple-green birefringence)** gösterir. Bu bulgu amiloidoz için altın standart tanı kriteridir.
• **Elektron Mikroskopisi:** Dalsız, rastgele dizilmiş 7.5 - 10 nm çapında ince fibriller izlenir.""",
        [
            {"type": "warning", "badge": "🔴 ALTIN STANDART TANI", "text": "Kongo kırmızısı boyasında polarize ışık altında 'elma yeşili çift kırılma' (apple-green birefringence) görülmesi amiloid birikiminin kesin kanıtıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ KOMİTE BİLGİSİ", "text": "Ülkemizde renal AA amiloidozun en sık genetik nedeni Ailevi Akdeniz Ateşidir (FMF / MEFV gen mutasyonu); amiloid fibrillerinin çapı 7.5-10 nm'dir.", "color": "sky"}
        ],
        {
            "id": "prac-nef-017",
            "question": "Tekrarlayan karın ağrısı ve ateş atakları olan FMF hastasında gelişen nefrotik sendrom nedeniyle yapılan böbrek biyopsisinde, amorf aselüler eozinofilik birikimlerin amiloid olduğunu kesinleştiren yöntem hangisidir?",
            "options": [
                "A) PAS boyasında bazal membranın kalınlaşması",
                "B) Gümüşleme boyasında tram-track çift kontur izlenmesi",
                "C) Kongo kırmızısı boyaması sonrası polarize mikroskopta elma yeşili çift kırılma saptanması",
                "D) İmmünofloresanda granüler IgG pozitifliği",
                "E) Ziehl-Neelsen boyasında asido-rezistan basillerin görülmesi"
            ],
            "correctAnswer": 2,
            "explanation": "Kongo kırmızısı boyası sonrası polarize mikroskopta elma yeşili çift kırılma (apple-green birefringence) amiloidozun patognomonik altın standart mikroskobik kanıtıdır."
        }
    ),
    make_slide(
        18,
        "Nefrotik Sendromda Biyopsi Endikasyonları ve Ayırıcı Tanı Algoritması",
        "Çocukta Steroid Direnci, Erişkinde Rutin Biyopsi ve Laboratuvar Karşılaştırması",
        """Nefrotik sendrom klinik tablosuyla gelen hastada biyopsi kararı yaşa ve klinik seyre göre kesin protokollere bağlıdır.

**1. Yaş Gruplarına Göre Biyopsi Yaklaşımı:**
• **Çocuklar (1-10 Yaş):** Olguların %90'ı MDH olduğu için başlangıçta böbrek biyopsisi **yapılmaz!** Doğrudan ampirik oral kortikosteroid tedavisi başlanır. Ancak:
  - Steroid tedavisine 4-8 haftada yanıt alınamazsa (steroid direnci),
  - Başvuru anında makroskopik hematüri, hipertansiyon veya kalıcı hipokomplementemi (C3 düşüklüğü) varsa,
  - 1 yaş altı (konjenital nefrotik) veya 12 yaş üstü başlangıç söz konusuysa renal biyopsi endikedir.
• **Erişkinler:** Erişkinde etyolojik spektrum çok geniştir (FSGS, Membranöz, Amiloidoz, Diyabet). Bu nedenle kontrendikasyon yoksa **tüm erişkin nefrotik sendrom olgularına tanı ve tedavi planı için renal biyopsi yapılır.**

**2. Kompleman Düzeylerine Göre Ayırıcı Tanı:**
• **Normal Kompleman (C3 / C4 Normal):** Minimal Değişiklik Hastalığı, FSGS, Membranöz Nefropati, Diyabetik Nefropati, Amiloidoz.
• **Düşük Kompleman (Hipokomplementemi):** MPGN Tip I (C3 ve C4 düşük), C3 Glomerülopatisi (izole C3 düşük), Lupus Nefriti Sınıf IV (C3 ve C4 düşük).""",
        [
            {"type": "clinical", "badge": "🔴 PEDİATRİK KURAL", "text": "Tipik bir çocukluk çağı nefrotik sendromunda biyopsi endikasyonu yoktur; ilk basamak steroid tedavisidir. Erişkinde ise biyopsi kuraldır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV SPOTU", "text": "MDH, FSGS ve primer Membranöz nefropatide serum C3 ve C4 kompleman düzeyleri NORMALDİR; kompleman düşüklüğü MPGN, Lupus ve Poststreptokokkal GN'yi işaret eder.", "color": "sky"}
        ],
        {
            "id": "prac-nef-018",
            "question": "Aşağıdaki nefrotik sendrom nedenlerinin hangisinde serum C3 kompleman düzeyinin belirgin olarak düşmesi beklenir?",
            "options": [
                "A) Minimal değişiklik hastalığı",
                "B) Membranöz nefropati",
                "C) Membranoproliferatif glomerülonefrit Tip I",
                "D) Primer Fokal segmental glomerüloskleroz",
                "E) Renal amiloidoz"
            ],
            "correctAnswer": 2,
            "explanation": "MPGN Tip I klasik kompleman yolunu aktive ederek C3 ve C4 düşüklüğüne yol açar. MDH, FSGS, Membranöz ve Amiloidozda kompleman düzeyleri normaldir."
        }
    ),
    make_slide(
        19,
        "Konjenital ve İnfantil Nefrotik Sendromlar: Genetik Defektler",
        "NPHS1 (Nefrin), NPHS2 (Podosin) ve WT1 Mutasyonları (Denys-Drash / Frasier)",
        """Yaşamın ilk 3 ayında başlayan nefrotik sendrom 'konjenital', 3-12 ay arasında başlayan ise 'infantil' nefrotik sendrom olarak tanımlanır. Bu tablolar neredeyse daima podosit yapısal proteinlerinin genetik defektlerine bağlıdır ve immünsüpresif tedaviye yanıtsızdır.

**1. Fin Tipi Konjenital Nefrotik Sendrom (CNF):**
• *NPHS1* geni mutasyonu (kromozom 19q13) sonucu **Nefrin** proteini eksiktir. İntrauterin dönemde başlar; plasenta dev boyutlardadır ve amniyon sıvısında alfa-fetoprotein (AFP) aşırı yüksektir.
• Çocuklar doğumdan itibaren masif proteinüri ile doğar; histolojide belirgin mikrokistik tubuler dilatasyon ('mikrokistik hastalık') izlenir. Küratif tek tedavi nefrektomi ve renal transplantasyondur.

**2. Steroid Dirençli Konjenital/İnfantil Nefrotik Sendrom:**
• *NPHS2* geni mutasyonu: **Podosin** defekti; otozomal resesif kalıtılır ve histolojide erken FSGS lezyonları yapar.
• *WT1* (Wilms Tümör 1) Mutasyonları:
  - **Denys-Drash Sendromu:** Erken başlangıçlı nefrotik sendrom (diffüz mezangiyal skleroz), Wilms tümörü ve erkek psödohermafroditizmi (XY disgenezi).
  - **Frasier Sendromu:** FSGS, gonadoblastom ve kadın fenotipi gösteren XY cinsiyet gelişim bozukluğu.""",
        [
            {"type": "warning", "badge": "🔴 GENETİK TÜMÖR SENDROMU", "text": "Erken başlangıçlı nefrotik sendrom, Wilms tümörü ve ambigus genitalya/psödohermafroditizm triadı Denys-Drash sendromudur (WT1 mutasyonu).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS BİLGİSİ", "text": "Fin tipi konjenital nefrotik sendromda defektif protein Nefrin (NPHS1); histopatolojik bulgu ise kortikal tubuluslarda mikrokistik dilatasyondur.", "color": "sky"}
        ],
        {
            "id": "prac-nef-019",
            "question": "Doğumdan itibaren masif proteinürisi olan, dev plasenta öyküsü bulunan ve biyopsisinde tubuluslarda mikrokistik genişlemeler izlenen konjenital nefrotik sendromlu bebekte mutasyon hangi gendedir?",
            "options": [
                "A) NPHS1 (Nefrin)",
                "B) NPHS2 (Podosin)",
                "C) ACTN4",
                "D) COL4A5",
                "E) GLA"
            ],
            "correctAnswer": 0,
            "explanation": "Fin tipi konjenital nefrotik sendrom NPHS1 geni mutasyonuna bağlı nefrin eksikliği sonucu gelişir; mikrokistik tubuler dilatasyon karakteristiktir."
        }
    ),
    make_slide(
        20,
        "Podositopatilerde Elektron Mikroskobunun Rolü ve Morfolojik Özeti",
        "Subepitelyal, Subendotelyal, İntramembranöz ve Mezangiyal Depozit Haritası",
        """Glomerüler hastalıkların ayırıcı tanısında immün depozitlerin bazal membran katmanlarına göre yerleşimi patolojinin en temel sınav ve tanı matrisini oluşturur.

**1. İmmün Depozit Yerleşim Haritası:**
• **Subepitelyal Depozitler (Podosit Altı):**
  - *Membranöz Nefropati:* Diffüz homojen subepitelyal depozitler ve 'spike-dome' oluşumu.
  - *Poststreptokokkal GN:* Büyük, kubbe şeklinde subepitelyal hörgüçler (**humps**).
• **Subendotelyal Depozitler (Endotel Altı):**
  - *MPGN Tip I:* Subendotelyal depozitler ve mezangiyal interpozisyon.
  - *Diffüz Proliferatif Lupus Nefriti (Sınıf IV):* Subendotelyal 'tel halka' (wire-loop) depozitleri.
• **İntramembranöz Depozitler (GBM İçi):**
  - *Yoğun Birikim Hastalığı (DDD / C3G):* GBM laminasında kesintisiz kurdele benzeri aşırı yoğun depozitler.
• **Mezangiyal Depozitler:**
  - *IgA Nefropatisi (Berger):* Saf veya baskın mezangiyal IgA depolanması.
  - *Henoch-Schönlein Purpurası (IgA Vasküliti).*
• **Depozitsiz Podosit Hasarı (İmmün Kompleks Yok):**
  - *Minimal Değişiklik Hastalığı:* Yalnızca podosit ayaksı çıkıntılarında yaygın silinme; depozit izlenmez.
  - *FSGS:* Podosit silinmesi ve fokal segmental skleroz; immün kompleks depoziti yoktur.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Depozit yerleşimi doğrudan klinik tabloyu belirler: Subepitelyal birikimler (podosit hasarı) baskın NEFROTİK tablo yaparken; subendotelyal ve mezangiyal birikimler (enflamasyon) baskın NEFRİTİK tablo yapar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV MATRİSİ", "text": "Subepitelyal hörgüç: Poststreptokokkal GN; Subepitelyal spike-dome: Membranöz; Subendotelyal tram-track: MPGN Tip I; İntramembranöz kurdele: DDD (MPGN Tip II).", "color": "sky"}
        ],
        {
            "id": "prac-nef-020",
            "question": "Glomerülopatiler ve elektron mikroskobundaki tipik immün depozit lokalizasyonu eşleştirmelerinden hangisi yanlıştır?",
            "options": [
                "A) Membranöz nefropati — Subepitelyal depozitler",
                "B) Poststreptokokkal GN — Subepitelyal 'hörgüç' (humps)",
                "C) MPGN Tip I — Subendotelyal depozitler",
                "D) Yoğun birikim hastalığı (DDD) — İntramembranöz kurdele birikim",
                "E) Minimal değişiklik hastalığı — Belirgin mezangiyal yoğun depozitler"
            ],
            "correctAnswer": 4,
            "explanation": "Minimal Değişiklik Hastalığında hiçbir lokalizasyonda immün kompleks depoziti bulunmaz; elektron mikroskobundaki tek bulgu podosit ayaksı çıkıntılarının silinmesidir."
        }
    ),
    make_slide(
        21,
        "Nefrotik Sendromda Tubulointerstisyel Hasar ve Lipoid Nefroz Özellikleri",
        "Protein Yükü Toksisitesi, Proksimal Tubulus Vakuolizasyonu ve İnterstisyel Fibrozis",
        """Nefrotik sendrom primer olarak glomerülü tutsa da, hastalığın uzun dönem prognozunu ve son dönem böbrek yetmezliğine gidiş hızını belirleyen en kritik patolojik parametre **tubulointerstisyel hasarın derecesidir**.

**1. Proteinüri Tubulotoksisitesi:**
• Ağır proteinüride aşırı miktarda albümin, immünglobulin ve kompleman proksimal tubulus lümenine filtre olur.
• Tubulus epitel hücreleri bu proteinleri endositoz yoluyla geri emmeye çalışır. Aşırı protein yüklenmesi lizozomları tüketir ve tubuler hücreleri aktive ederek enflamatuar sitokinlerin (MCP-1, TGF-beta) salınmasına yol açar.
• Bu sitokinler interstisyel alana makrofaj ve fibroblast göçünü tetikleyerek tübüler atrofi ve geri dönüşsüz interstisyel fibrozis sürecini başlatır.

**2. Lipoid Nefroz Morfolojisi:**
Filtre olan lipoproteinler proksimal tübül epitel hücreleri tarafından pinositozla yutulur. Hücre sitoplazmasında nötral yağlar ve kolesterol esterleri birikir; ışık mikroskobunda tübül hücreleri vakuollü ve köpüksü görünüm kazanır. İdrar sedimentine dökülen bu tübül hücreleri **oval yağ cisimcikleri** olarak adlandırılır.""",
        [
            {"type": "clinical", "badge": "🔴 PROGNOSTİK GÖSTERGE", "text": "Tüm glomerülopatilerde böbrek sağkalımını belirleyen en güvenilir histolojik parametre glomerüler skleroz yüzdesi değil, tübüler atrofi ve interstisyel fibrozis derecesidir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Nefrotik sendromda idrarda görülen oval yağ cisimcikleri tübül epitel hücrelerinin filtre olan lipidleri sitoplazmalarında depolayıp dökülmesiyle oluşur.", "color": "sky"}
        ],
        {
            "id": "prac-nef-021",
            "question": "Kronik glomerüler hastalıklarda böbrek yetmezliğine ilerlemeyi ve uzun dönem prognozu en güçlü tahmin ettiren histopatolojik lezyon aşağıdakilerden hangisidir?",
            "options": [
                "A) Glomerüllerdeki podosit hipertrofisi",
                "B) Tübülointerstisyel atrofi ve fibrozisin yaygınlığı",
                "C) Bowman kapsülünün kalınlaşması",
                "D) Kapiller lümendeki trombosit agregasyonu",
                "E) Yalnızca mezangiyal hücre sayısı"
            ],
            "correctAnswer": 1,
            "explanation": "Nefrolojik patolojide tübülointerstisyel hasar, atrofi ve fibrozisin derecesi, glomerüler lezyonun tipinden bağımsız olarak son dönem böbrek yetmezliğine gidişin en güçlü prognostik göstergesidir."
        }
    ),
    make_slide(
        22,
        "Nefrotik Sendromlu Hastaya Genel Yaklaşım ve Özet Akış Şeması",
        "Tanı, Tedavi Basamakları, Biyopsi Zamanlaması ve Takip İlkeleri",
        """Nefrotik sendrom şüphesi olan bir hastada izlenecek klinik algoritma hastanın yaşına ve risk faktörlerine göre yapılandırılır.

**1. Tanı Basamakları:**
1. *Proteinüri Teyidi:* 24 saatlik idrarda >3.5 g/gün protein veya spot idrarda protein/kreatinin oranı >3.5 mg/mg.
2. *Serolojik Tarama:* Serum albümin, total kolesterol, trigliserid; böbrek fonksiyon testleri (üre, kreatinin, eGFR).
3. *Sekonder Nedenlerin Taranması:* Açlık kan şekeri, HbA1c (Diyabet), ANA, anti-dsDNA (Lupus), HBsAg, Anti-HCV (Hepatit B/C), Serum serbest hafif zincirleri ve protein elektroforezi (Miyelom/Amiloidoz), Anti-PLA2R (Membranöz).
4. *Kompleman Düzeyleri:* C3 ve C4 ölçümü.

**2. Biyopsi Kararı:**
• Çocukta tipik prezentasyon: Ampirik steroid başla; biyopsi yapma.
• Erişkinde: Kesin kontrendikasyon yoksa renal biyopsi planla.

**3. Genel Destek Tedavisi:**
• Proteinüriyi azaltmak ve intraglomerüler basıncı düşürmek için birinci basamakta **ACE inhibitörü veya ARB**.
• Ödem kontrolü için loop diüretikleri (Furosemid) ve tuz kısıtlaması (<2 g/gün sodyum).
• Hiperlipidemi için Statin tedavisi.
• Derin hipoalbüminemide (<2 g/dL) tromboemboli profilaksisi (antikoagülasyon).""",
        [
            {"type": "clinical", "badge": "🔴 TEDAVİ PRENSİBİ", "text": "Etyolojiden bağımsız olarak tüm nefrotik sendromlu hastalarda intraglomerüler kapiller basıncı ve proteinüriyi azaltmak için ilk tercih edilecek antihipertansifler ACE inhibitörleri veya ARB'lerdir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "ACE inhibitörleri eferent arteriyolü genişleterek intraglomerüler glomerül içi filtrasyon basıncını düşürür ve nefrotik proteinüriyi belirgin azaltır.", "color": "sky"}
        ],
        {
            "id": "prac-nef-022",
            "question": "Nefrotik sendromlu bir hastada intraglomerüler hidrostatik basıncı ve proteinüriyi azaltmak amacıyla başlanan ACE inhibitörlerinin temel renal hemodinamik etki mekanizması hangisidir?",
            "options": [
                "A) Afferent arteriyolü daraltmak",
                "B) Eferent arteriyolde vazodilatasyon sağlamak",
                "C) Glomerüler bazal membranın negatif yükünü artırmak",
                "D) Podosit slit diyaframlarını mekanik olarak kapatmak",
                "E) Proksimal tubulustan albümin geri emilimini inhibe etmek"
            ],
            "correctAnswer": 1,
            "explanation": "ACE inhibitörleri anjiyotensin II'yi baskılayarak eferent arteriyolü dilate eder; bu sayede glomerül içi kapiller hidrostatik basınç düşer ve protein kaçağı azalır."
        }
    ),
    make_slide(
        23,
        "Nefrotik Sendrom: Ayırıcı Tanı ve Büyük Karşılaştırma Tablosu",
        "MDH, FSGS, Membranöz, MPGN Tip I ve DDD Karşılaştırmalı Matrisi",
        """Nefrotik sendrom oluşturan primer glomerülopatilerin Robbins Patoloji temel kriterlerine göre toplu özeti:

| Hastalık | Yaş / Risk Grubu | Işık Mikroskobu (LM) | İmmünofloresan (İF) | Elektron Mikroskobu (EM) | Kompleman (C3) | Steroid Yanıtı / Seyir |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MDH** | 2-6 Yaş çocuk | Normal glomerül | Negatif | Podosit ayaksı çıkıntılarında silinme | Normal | Mükemmel (%90+), relaps sık |
| **FSGS** | Erişkin (Zenci ırk, obezite, HIV) | Fokal segmental skleroz, hyalinozis | Negatif (sklerozda non-spesifik IgM/C3) | Yaygın podosit silinmesi, denudasyon | Normal | Dirençli (%50+), SDBY riski yüksek |
| **Membranöz** | 30-50 Yaş erişkin, malignite | Diffüz GBM kalınlaşması, 'Spike-Dome' | Granüler IgG ve C3 | Subepitelyal elektron-yoğun depozitler | Normal | 1/3 spontan remisyon, 1/3 SDBY |
| **MPGN Tip I** | Genç erişkin, Hepatit C | Lobülasyon, 'Tram-Track' çift kontur | Granüler IgG, IgM ve C3 | Subendotelyal depozitler, interpozisyon | Düşük (C3 ve C4) | Yavaş ilerler, nakilde nüks sık |
| **DDD (C3G)** | Çocuk ve genç erişkin | MPGN veya mezangiyoproliferatif | İzole C3 pozitif (IgG negatif) | İntramembranöz kesintisiz kurdele depozit | Aşırı Düşük (C4 normal) | Kötü, allogreftte %100'e yakın nüks |""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK MATRİS", "text": "MDH, FSGS ve Membranözde kompleman normal iken; MPGN Tip I'de C3+C4 düşük, C3 Glomerülopatisinde (DDD) ise izole C3 düşüktür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE SPOTU", "text": "TUS ve komitelerde en sık sorulan soru kalıbı: 'Spike-dome = Membranöz', 'Tram-track = MPGN Tip I', 'Podosit silinmesi + normal LM = MDH', 'Kurdele depozit = DDD'.", "color": "sky"}
        ],
        {
            "id": "prac-nef-023",
            "question": "Aşağıdaki eşleştirmelerden hangisinde glomerüler hastalık ile serum kompleman düzeyi ve patolojik bulgusu doğru verilmiştir?",
            "options": [
                "A) Minimal Değişiklik Hastalığı — Düşük C3 — Subendotelyal depozit",
                "B) Membranöz Nefropati — Normal C3 — Subepitelyal 'spike and dome' depozit",
                "C) MPGN Tip I — Normal C3 ve C4 — Yalnızca podosit ayaksı çıkıntı silinmesi",
                "D) Yoğun Birikim Hastalığı (DDD) — Yüksek C3 — Subepitelyal hörgüç",
                "E) FSGS — Düşük C4 — İntramembranöz kurdele depozit"
            ],
            "correctAnswer": 1,
            "explanation": "Membranöz nefropatide serum kompleman düzeyi normaldir ve histopatolojide subepitelyal depozitlerle birlikte 'spike and dome' görünümü karakteristiktir."
        }
    ),
    make_slide(
        24,
        "Ders 19 Kapsamlı Sentezi: Nefrotik Sendrom Patolojisinin Klinik Kodları",
        "Amfi Dersinin En Kritik Sınav İncileri ve Akılda Kalması Gereken 10 Emir",
        """Prof. Dr. Hikmet Keleş'in Nefrotik Sendrom patolojisi dersinin en kritik sınav ve klinik özeti:

**1. Patolojinin 10 Altın Kuralı:**
1. *Nefrotik Sendrom:* >3.5 g/gün proteinüri, hipoalbüminemi (<3 g/dL), yaygın ödem ve lipidüri.
2. *Çocukluk çağı:* 1 numara Minimal Değişiklik Hastalığı (LM normal, EM podosit ayaksı çıkıntı silinmesi, selektif albüminüri, steroid yanıtı mükemmel).
3. *Erişkin:* 1 numara FSGS (Amerika ve genel) / Membranöz nefropati.
4. *FSGS:* Non-selektif proteinüri, steroide dirençli, nakil sonrası %25-50 nüks, HIV'de kollaps varyant.
5. *Membranöz Nefropati:* Anti-PLA2R otoantikorları, subepitelyal depozitler, gümüş boyada 'Spike and Dome', en yüksek renal ven trombozu riski.
6. *MPGN Tip I:* Subendotelyal depozitler, mezangiyal interpozisyon, gümüş boyada 'Tram-Track' çift kontur, Hepatit C ilişkisi, C3 ve C4 düşük.
7. *Yoğun Birikim Hastalığı (DDD):* Alternatif yol aktivasyonu, C3NeF otoantikoru, izole C3 aşırı düşük, EM'de intramembranöz kurdele birikim.
8. *Diyabetik Nefropati:* Nodüler glomerüloskleroz (Kimmelstiel-Wilson nodülleri), afferent ve eferent arteriyoloskleroz, mikroalbüminüri ilk klinik bulgu.
9. *Amiloidoz:* Kongo kırmızısı ile polarize mikroskopta elma yeşili çift kırılma, 7.5-10 nm dalsız fibriller.
10. *Tübülointerstisyel Fibrozis:* Glomerül hasarının tipi ne olursa olsun son dönem böbrek yetmezliğine gidişi belirleyen nihai histolojik gösterge.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Klinik pratikte nefrotik sendromlu bir çocuk geldiğinde ilk yapılacak iş steroid başlamaktır; erişkin geldiğinde ise ilk yapılacak iş renal biyopsi planlamaktır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta listelenen 10 altın kural komite ve TUS sınavlarında nefrotik sendrom başlığından gelen soruların %95'ini çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-nef-024",
            "question": "Aşağıdaki klinik tablolardan hangisinde hastaya doğrudan ampirik kortikosteroid başlanması gerekirken biyopsi endikasyonu bulunmaz?",
            "options": [
                "A) Bacaklarında ödem ve 4 g/gün proteinüri ile başvuran 45 yaşındaki erkek",
                "B) Tip 2 diyabeti ve 5 g/gün proteinürisi olan 55 yaşındaki kadın",
                "C) Ani başlayan yaygın ödem ve 4 g/gün selektif proteinürisi olan, mikroskopik hematürisi bulunmayan 3 yaşındaki çocuk",
                "D) Ani başlayan nefrotik sendrom ve anti-PLA2R negatifliği olan 65 yaşındaki erkek",
                "E) Hepatit C pozitifliği, purpura ve mikst nefrotik tablosu olan 40 yaşındaki hasta"
            ],
            "correctAnswer": 2,
            "explanation": "3 yaşındaki çocukta tipik prezentasyonla gelen nefrotik sendromun %90 nedeni Minimal Değişiklik Hastalığı olduğundan doğrudan steroid başlanır, böbrek biyopsisi yapılmaz."
        }
    )
]

print("Nefrotik Sendrom 24 slayt başarıyla tanımlandı.")

# ==============================================================================
# HEDEF GÜVERTEYİ GÜNCELLE
# ==============================================================================
target_id = 'learn-glomeruler-hastaliklar-nefrotik'
for d in decks:
    if d.get('id') == target_id:
        d['title'] = "Glomerüler Hastalıklar: Nefrotik Sendrom Patolojisi"
        d['shortTitle'] = "Nefrotik Sendrom Patolojisi"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Glomerüler filtrasyon bariyeri, podosit biyolojisi, Minimal Değişiklik Hastalığı, FSGS varyantları, Membranöz Nefropati (anti-PLA2R), MPGN Tip I, C3 Glomerülopatisi, Diyabetik nefropati ve Amiloidoz patolojisi."
        d['slides'] = nefrotik_slides
        print(f"'{target_id}' güvertesi 24 yüksek kaliteli slaytla güncellendi.")
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("İşlem tamamlandı.")
