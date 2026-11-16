# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 10: Amiloidoz Tipleri, Organ Morfolojisi, Robbins Spotları ve Büyük Sentez (Slayt 91-100)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: Transtiretin (ATTR) ve Diğer Amiloid Tipleri
    slides.append({
        "id": "k1-25-s91",
        "title": "Transtiretin (ATTR) ve Diğer Amiloid Tipleri",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 91,
        "narrative": (
            "AL ve AA amiloidozunun ötesinde, klinik pratikte hayati öneme sahip diğer amiloid formları şunlardır: "
            "1. **Transtiretin (ATTR) Amiloidozu:** Karaciğerden sentezlenen, tiroksin ve retinol bağlayıcı proteindir. "
            "İki temel formu mevcuttur: "
            "- **Yabanıl (Wild-type) ATTR (Senil Sistemik Amiloidoz):** Genetik mutasyon yoktur; normal yapıdaki protein "
            "70-80 yaş üstü yaşlı erkeklerin kalbinde yavaşça birikir (**senil kardiyak amiloidoz**). Prognozu AL amiloidozuna göre "
            "çok daha iyidir. "
            "- **Mutant ATTR (Ailesel Amiloidoz):** Nokta mutasyonları sonucu periferik sinirlerde ve kalpte birikerek "
            "**ailesel amiloid polinöropatisi** ve kardiyomiyopatisi yapar. "
            "2. **Beta-2 Mikroglobulin ($A\\beta_2M$):** MHC Sınıf I molekülünün hafif zinciridir. Böbrek yetmezliğinde kanda "
            "yükselir ve standart hemodiyaliz membranlarından geçemez. Uzun süreli (>10 yıl) hemodiyaliz hastalarında sinovyum, "
            "eklemler ve tendon kılıflarında birikerek **karpal tünel sendromu** ve diyaliz amiloidozuna yol açar. "
            "3. **Beta-Amiloid ($A\\beta$):** Amiloid prekürsör proteinden (APP) köken alır; Alzheimer hastalığında serebral "
            "kortekste senil plakları ve serebral kan damarlarında amiloid anjiyopatisini oluşturur. "
            "4. **Endokrin Amiloidler:** Medüller tiroid karsinomunda kalsitonin türevi, Tip 2 DM pankreas Langerhans adacıklarında "
            "ise amilin (IAPP) birikintileri izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Özgül Amiloid Proteinleri ve Klinik Tabloları",
                ["Amiloid Proteini", "Öncül Molekül", "Temel Hastalık / Organ Tutulumu"],
                [
                    ["ATTR (Yabanıl / Wild-type)", "Normal Transtiretin", "Senil kardiyak amiloidoz (yaşlı erkekler, kalp yetmezliği)"],
                    ["ATTR (Mutant)", "Mutant Transtiretin", "Ailesel amiloid polinöropatisi ve ailesel kardiyomiyopati"],
                    [
                        "Abeta2M",
                        "Beta-2 Mikroglobulin",
                        {"text": "Kronik hemodiyaliz hastalarında karpal tünel sendromu", "isMasked": True, "hint": "Diyaliz membranından süzülemeyen MHC hafif zincirinin fleksör retinakulumda tuzaklanması"}
                    ],
                    ["Abeta (A-beta)", "Amiloid Prekürsör Protein (APP)", "Alzheimer hastalığı (senil plaklar ve serebral anjiyopati)"],
                    ["A-Cal (Prokalsitonin)", "Prokalsitonin", "Medüller tiroid karsinoması stroması"]
                ]
            ),
            make_micro_quiz(
                "Sekiz yıldır kronik hemodiyaliz tedavisi gören bir son dönem böbrek yetmezliği hastasında her iki el bileğinde uyuşma ve karpal tünel sendromu saptanmıştır. Bu hastanın tendon kılıfı biyopsisinde amiloidoz tespit edilirse, biriken amiloidin öncül proteini aşağıdakilerden hangisidir?",
                {
                    "A": "Beta-2 mikroglobulin",
                    "B": "Monoklonal lambda hafif zinciri",
                    "C": "Serum Amiloid A (SAA)",
                    "D": "Amiloid prekürsör proteini (APP)",
                    "E": "Normal yabanıl transtiretin"
                },
                "A",
                {
                    "A": "Doğrudur; diyaliz filtrelerinden geçemeyen beta-2 mikroglobulin fleksör tendon kılıflarında birikerek karpal tünel sendromuna neden olur.",
                    "B": "Yanlış; bu AL amiloidozudur (miyelom).",
                    "C": "Yanlış; bu AA amiloidozudur (kronik inflamasyon).",
                    "D": "Yanlış; bu Alzheimer hastalığıdır.",
                    "E": "Yanlış; bu senil kardiyak amiloidozdur."
                }
            )
        ]
    })

    # Slayt 92: Organ Amiloidozu 1: Amiloid Böbreği
    slides.append({
        "id": "k1-25-s92",
        "title": "Organ Amiloidozu 1: Amiloid Böbreği",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 92,
        "narrative": (
            "Böbrek, hem AL hem de AA sistemik amiloidozunda en sık ve klinik seyir açısından en ölümcül organdır: "
            "1. **Makroskopi:** Erken dönemde böbrekler normal veya hafif büyüktür; ileri dönemde amiloid birikimi "
            "vasküler lümenleri daraltıp iskemiye yol açtıkça böbrekler büzüşür, sertleşir, soluk gri-sarı balmumu kıvamı alır. "
            "2. **Mikroskopi ve Glomerüler Tutulum:** "
            "- Amiloid ilk olarak glomerül **mezangiyal matrikste** pembe, amorf, asellüler odaklar halinde çöker. "
            "- Birikim arttıkça kılcal bazal membranlara yayılır, kılcal duvarları kalınlaştırır ve kapiller lümenleri tıkar. "
            "- Son evrede glomerül yumağı tamamen asellüler, camsı bir amiloid kitlesine dönüşür (**glomerül skleroz/obliterasyon**). "
            "3. **Tübüler ve İnterstisyel Tutulum:** Tübül bazal membranlarında biriken amiloid tübüler atrofiye yol açar; "
            "lümenlerde pembe amiloid silendirleri görülebilir. "
            "4. **Klinik Tablo:** Erken evrede asemptomatik mikroalbüminüri, ardından masif proteinüri (>3.5 g/gün), "
            "ağır **nefrotik sendrom**, hipoalbüminemi, anazarka ödem ve nihayetinde son dönem üremi."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Böbrek Amiloidozunda Nefrotik Sendrom Mekanizması",
                [
                    "1. Mezangiyal Çökme: Dolaşımdaki öncül fibrillerin mezangiyal matrikste birikmesi",
                    "2. Bazal Membran Disrüpsiyonu: Amiloidin kapiller bazal membran mimarisini bozarak negatif yük bariyerini yok etmesi",
                    "3. Masif Protein Kaçağı: Günde 3.5 gramın üzerinde masif albüminüri ve nefrotik sendrom gelişimi",
                    "4. Glomerüler Skleroz: Kapiller lümenlerin tıkanması ve üremiyle son dönem böbrek yetmezliği"
                ]
            ),
            make_cloze(
                "Böbrek amiloidozunda amiloid birikiminin ilk başladığı ve ardından tüm glomerülü tıkayan histolojik bölge glomerül mezangiyumudur.",
                "mezangiyumudur",
                "Glomerül kapiller yumakları arasındaki destek matriks dokusu"
            )
        ]
    })

    # Slayt 93: Organ Amiloidozu 2: Amiloid Dalağı (Sago vs Lardaceous)
    slides.append({
        "id": "k1-25-s93",
        "title": "Organ Amiloidozu 2: Amiloid Dalağı (Sago vs Lardaceous)",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 93,
        "narrative": (
            "Dalak tutulumu sistemik amiloidozun en klasik patolojik modellerinden biridir ve makroskopik olarak "
            "iki belirgin patern sergiler: "
            "1. **Sago Dalağı (Folliküler Tip):** "
            "- Amiloid birikimi dalak **Malpighi cisimcikleri (splenik lenfoid foliküller - beyaz pulpa)** ile kesin olarak sınırlıdır. "
            "- Kırmızı pulpa korunmuştur. "
            "- Dalağın kesit yüzeyinde koyu kırmızı fon üzerinde yarı saydam, grimsi-beyaz, parlak nişasta taneciklerine "
            "(tapiyoka / sago taneleri) benzeyen 1-2 mm'lik nodüller seçilir. Dalak boyutu genellikle belirgin büyümez. "
            "2. **Lardaceous (Yağlı / Harita) Dalak (Diffüz Tip):** "
            "- Amiloid birikimi folikülleri değil, **kırmızı pulpanın venöz sinüzoid duvarlarını ve retiküler bağ dokusu liflerini** tutar. "
            "- Foliküller amiloid kütlesi tarafından ezilerek atrofiye uğrar ve silinir. "
            "- Dalak masif olarak büyür (bazen 1-2 kg'a ulaşan splenomegali). Kesit yüzeyi domuz yağına (lard) veya balmumuna "
            "benzeyen geniş, parlak, sert ve alacalı harita benzeri amiloid adacıkları gösterir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Sago Dalağı vs Lardaceous Dalak Karşılaştırması",
                "Sago Dalağı (Folliküler Form)",
                "Birikim beyaz pulpa Malpighi foliküllerine sınırlıdır; tapiyoka incisi gibi parlak 1-2 mm tanecikler oluşturur",
                "Lardaceous Dalak (Diffüz Form)",
                "Birikim kırmızı pulpa sinüzoidlerini tutar; masif splenomegali ve balmumu/domuz yağı benzeri geniş harita plakları yapar"
            ),
            make_active_recall(
                "Amiloid birikiminin dalağın beyaz pulpasında yer alan Malpighi folikülleriyle sınırlı kaldığı ve kesit yüzeyinde tapiyoka tanecikleri görünümü veren dalak tutulum paterni hangisidir?",
                "Sago dalağıdır.",
                "Beyaz pulpa lenfoid folikül lokalizasyonlu amiloid morfolojisi"
            )
        ]
    })

    # Slayt 94: Organ Amiloidozu 3: Kalp ve Karaciğer Tutulumu
    slides.append({
        "id": "k1-25-s94",
        "title": "Organ Amiloidozu 3: Kalp ve Karaciğer Tutulumu",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 94,
        "narrative": (
            "Kalp ve karaciğer, amiloidozun morbidite ve mortalitesinde kritik rol oynayan diğer hayati organlardır: "
            "1. **Amiloid Kalbi (Kardiyak Amiloidoz):** "
            "- Hem AL amiloidozunda hem de ATTR (senil ve mutant) formlarında sık görülür. "
            "- Amiloid miyofibriller arasında (intersellüler) yaygın olarak çöker; endokard altında ve koroner damar duvarlarında "
            "damla şeklinde nodüller yapar. "
            "- Miyositler amiloid kütlesinin mekanik baskısıyla bası atrofisine uğrar. Kalp ventrikülleri sertleşir, diyastolde "
            "genişleyemez (**restriktif kardiyomiyopati**). "
            "- **Klinik Paradoks:** Ventrikül duvarları amiloidle kalınlaştığı halde EKG'de **düşük voltajlı QRS kompleksleri** "
            "görülür. İleti sistemi liflerinin tutulmasıyla ölümcül aritmiler ortaya çıkar. "
            "2. **Amiloid Karaciğeri (Hepatik Amiloidoz):** "
            "- Amiloid ilk olarak endotel ile hepatositler arasındaki **Disse aralığında** birikir. "
            "- Genişleyen amiloid hepatosit kordonlarını sıkıştırıp atrofiye sokar; sinüzoidleri daraltır. "
            "- Karaciğer dev boyutlara ulaşabilir (masif hepatomegali), kıvamı son derece sert ve kenarları keskindir. "
            "Parankim kaybına rağmen karaciğer enzimleri uzun süre şaşırtıcı şekilde normal veya hafif yüksek kalabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kalp ve Karaciğerde Amiloid Tutulumunun Patolojik Özellikleri",
                ["Organ", "Başlıca Amiloid Tipi", "Mikroskobik Yerleşim", "Klinik / EKG Tablosu"],
                [
                    ["Kalp", "AL ve ATTR (senil/mutant)", "Miyositler arası interstisyum, subendokard", "Restriktif kardiyomiyopati, düşük voltajlı EKG, aritmi"],
                    [
                        "Karaciğer",
                        "AL ve AA",
                        {"text": "Disse aralığı ve sinüzoid çevreleri", "isMasked": True, "hint": "Hepatosit bazal yüzeyi ile endotel arasındaki dar mikroskobik perisinüzoidal boşluk"},
                        "Masif hepatomegali, sert kıvam, göreceli korunan fonksiyon"
                    ]
                ]
            ),
            make_branching_logic(
                "74 yaşında erkek hasta efor dispnesi ve bacaklarda ödem şikayetiyle başvuruyor. Ekokardiyografide konsantrik sol ventrikül hipertrofisi ve restriktif diyastolik doluş paterni izleniyor. Ancak EKG'de ventriküler hipertrofi yerine tam tersine diffüz düşük voltajlı QRS kompleksleri saptanıyor. Biyopside amiloidoz doğrulanıyor.",
                "Bu hastada kardiyak kalınlaşmaya rağmen EKG'de düşük voltaj görülmesinin patofizyolojik nedeni nedir?",
                [
                    {
                        "text": "Ventrikül kalınlaşmasının canlı miyosit hipertrofisinden değil, miyositler arasına elektriksel olarak sessiz amiloid protein kütlesi çökmesinden kaynaklanması",
                        "isCorrect": True,
                        "explanation": "Doğrudur; duvar kalınlaşmasını sağlayan doku elektriksel aktivitesi olmayan asellüler amiloiddir; bu durum miyosit atrofisiyle birleştiğinde tipik düşük voltaj oluşturur."
                    },
                    {
                        "text": "Hastanın koroner arterlerinin tamamen tıkalı olması ve miyokardın tam kat nekroza uğraması",
                        "isCorrect": False,
                        "explanation": "Yanlış; bu durum akut miyokard enfarktüsü ve ST elevasyonu tablosudur."
                    },
                    {
                        "text": "Kalp kası hücrelerinin aşırı miktarda glikojen depolaması ve elektriksel iletimi hızlandırması",
                        "isCorrect": False,
                        "explanation": "Yanlış; bu Pompe hastalığıdır ve voltaj düşüklüğü değil yüksek voltaj yapar."
                    }
                ]
            )
        ]
    })

    # Slayt 95: Amiloidoz Klinik Tanısı ve Biyopsi Stratejisi
    slides.append({
        "id": "k1-25-s95",
        "title": "Amiloidoz Klinik Tanısı ve Biyopsi Stratejisi",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 95,
        "narrative": (
            "Sistemik amiloidoz kuşkusu olan bir hastada kesin tanı doku biyopsisi ile amiloid birikiminin kanıtlanmasıdır: "
            "1. **Biyopsi Yerinin Seçimi ve Riskler:** "
            "- Amiloid tutulumu olan organlar (böbrek, kalp, karaciğer) vasküler amiloid infiltrasyonuna bağlı olarak "
            "kanamaya çok meyillidir. Bu nedenle doğrudan organ biyopsisi ilk basamakta tercih edilmez. "
            "2. **Minimal İnvaziv Tarama Biyopsileri:** "
            "- **Abdominal Yağ Dokusu Aspirasyonu (Fat Pad Biopsy):** Göbek çevresinden ince iğne aspirasyonu ile subkütan "
            "yağ dokusu alınır. Güvenli, ağrısız ve sistemik amiloidoz vakalarında **%70-80 oranında pozitiftir**. İlk basamak seçenektir. "
            "- **Rektal Mukoza Biyopsisi:** Mukozal ve submukozal damar duvarlarındaki amiloid birikintilerini yakalamada "
            "%75-80 duyarlıdır. "
            "- Gingival (diş eti) ve minör tükürük bezi biyopsileri de alternatif güvenli alanlardır. "
            "3. **Histopatolojik Doğrulama Protokolü:** "
            "- Alınan örnek Kongo kırmızısı ile boyanır. "
            "- Polarize ışık mikroskobunda karakteristik **elma yeşili çift kırıcılık** saptanır. "
            "- İmmünohistokimya veya kütle spektrometrisi (proteomik analiz) yapılarak amiloidin tipi (AL, AA, ATTR) belirlenir; "
            "çünkü AL için miyelom kemoterapisi, AA için inflamasyon kontrolü, ATTR için ise TTR stabilizatörleri (tafamidis) gereklidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Amiloidoz Tanısal Biyopsi ve Tipleme Algoritması",
                [
                    "1. Şüphe: Nefrotik sendrom, restriktif kardiyomiyopati veya hepatomegali ile sistemik amiloidoz kuşkusu",
                    "2. Minimal İnvaziv Girişim: Kanama riskli organ yerine abdominal yağ dokusu aspirasyonu yapılması",
                    "3. Kongo Kırmızısı ve Polarizasyon: Kesitlerin polarize ışık mikroskobunda elma yeşili çift kırıcılık vermesi",
                    "4. Tip Spesifikasyonu: İmmünohistokimya veya kütle spektrometrisi ile AL / AA / ATTR ayrımının yapılması"
                ]
            ),
            make_cloze(
                "Sistemik amiloidoz şüphesinde majör organ kanama riskinden kaçınmak için ilk tercih edilen minimal invaziv doku örneklemesi abdominal yağ dokusu aspirasyonudur.",
                "abdominal yağ",
                "Göbek çevresi cilt altı stromal dokudan iğneyle yapılan güvenli örnekleme alanı"
            )
        ]
    })

    # Slayt 96: Aşırı Duyarlılık, Otoimmünite ve Amiloidoz Karşılaştırmalı Tablosu
    slides.append({
        "id": "k1-25-s96",
        "title": "Aşırı Duyarlılık, Otoimmünite ve Amiloidoz Karşılaştırmalı Tablosu",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 96,
        "narrative": (
            "Ders boyunca işlenen tüm majör immünopatolojik mekanizmaların ve klinik tabloların genel sentezi: "
            "1. **Tip I Hipersensitivite:** IgE ve mast hücre/bazofil degranülasyonu; histamin, LTC4, LTD4; anafilaksi, astım, ürtiker. "
            "2. **Tip II Hipersensitivite:** Sabit hücre veya doku antijenlerine bağlanan IgG/IgM; kompleman litik hasarı, opsonizasyon "
            "ve fagositoz, ADCC veya reseptör fonksiyon bozukluğu; Goodpasture, Myastenia Gravis, Graves, Pemfigus Vulgaris. "
            "3. **Tip III Hipersensitivite:** Dolaşan çözünür antijen-antikor immün komplekslerinin damar duvarına çökmesi; "
            "akut nekrotizan vaskülit, fibrinoid nekroz, nötrofilik infiltrasyon; SLE nefriti, Serum hastalığı, Arthus reaksiyonu. "
            "4. **Tip IV Hipersensitivite:** Antikor bağımsız, duyarlı T lenfositler (CD4+ Th1/Th17 ve CD8+ sitotoksik); "
            "granülomatöz inflamasyon (epiteloid histiyositler ve dev hücreler); Tüberküloz, Tip 1 DM, temas dermatiti. "
            "5. **Otoimmünite:** Santral ve periferik toleransın (Aujeszky, AIRE, FoxP3, Fas/FasL) kırılması; SLE, Sjögren, Sistemik Skleroz. "
            "6. **Amiloidoz:** Proteolitik yıkıma dirençli çapraz beta-tabakalı fibriller proteinlerin hücre dışı birikimi ve bası atrofisi."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İmmünopatoloji ve Doku Hasarı Mekanizmaları Karşılaştırma Matrisi",
                ["Patoloji Sınıfı", "Ana İmmün Mediyatör", "Tipik Morfolojik / Histolojik Lezyon", "Prototip Klinik Hastalık"],
                [
                    ["Tip I Hipersensitivite", "IgE + Mast hücre histamin ve lökotrienleri", "Vazodilatasyon, ödem, düz kas spazmı", "Anafilaktik şok, bronşiyal astım"],
                    ["Tip II Hipersensitivite", "IgG / IgM ve Doku Antijeni (Kompleman/ADCC)", "Fagositoz, hücresel lizis, reseptör blokajı", "Goodpasture, Myastenia Gravis, Pemfigus"],
                    ["Tip III Hipersensitivite", "Dolaşan İmmün Kompleksler (Ag-Ab)", "Damar duvarında fibrinoid nekroz ve vaskülit", "Sistemik Lupus Eritematozus, Arthus"],
                    [
                        "Tip IV Hipersensitivite",
                        "CD4+ Th1/Th17 ve CD8+ CTL Hücreleri",
                        {"text": "Kazeifiye granülomatöz inflamasyon veya apoptoz", "isMasked": True, "hint": "Epiteloid histiyositler ve Langhans dev hücreleri içeren hücresel lezyon"},
                        "Tüberküloz, Tip 1 DM, Temas dermatiti"
                    ],
                    ["Sistemik Amiloidoz", "Çapraz beta-tabakalı protein fibrilleri", "Kongo kırmızısı ile elma yeşili çift kırıcılık", "AL (Miyelom) ve AA (Kronik İnflamasyon)"]
                ]
            ),
            make_micro_quiz(
                "Damar duvarlarında fibrinoid nekroz, nötrofilik infiltrasyon ve nükleer toz (lökositoklazi) ile karakterize doku hasarı modeli, Coombs ve Gell sınıflamasına göre hangi aşırı duyarlılık tipinin klasik histopatolojik göstergesidir?",
                {
                    "A": "Tip III (İmmün kompleks aracılı) aşırı duyarlılık",
                    "B": "Tip I (IgE aracılı) aşırı duyarlılık",
                    "C": "Tip II (Antikor bağımlı sitotoksik) aşırı duyarlılık",
                    "D": "Tip IV (Gecikmiş tip hücresel) aşırı duyarlılık",
                    "E": "Tip V (Uyarıcı antikor) aşırı duyarlılık"
                },
                "A",
                {
                    "A": "Doğrudur; dolaşan antijen-antikor komplekslerinin damar duvarına çökmesi komplemanı aktive eder ve fibrinoid nekrozlu Tip III vaskülit tablosunu oluşturur.",
                    "B": "Yanlış; Tip I'de vazodilatasyon ve ödem vardır, nekroz yoktur.",
                    "C": "Yanlış; Tip II hücresel hedef antijenlere yöneliktir.",
                    "D": "Yanlış; Tip IV granülomatöz veya T hücre aracılı sitotoksisitedir.",
                    "E": "Yanlış; Tip V eski bir kavramdır ve Graves hastalığını tanımlar."
                }
            )
        ]
    })

    # Slayt 97: Robbins Patoloji Temelli Altın Sınav Spotları
    slides.append({
        "id": "k1-25-s97",
        "title": "Robbins Patoloji Temelli Altın Sınav Spotları",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 97,
        "narrative": (
            "Patoloji kurul ve TUS sınavlarında en yüksek soru değeri taşıyan kritik Robbins spotları: "
            "1. **Antijenik Hedefler:** Goodpasture Tip IV kollajenin alfa-3 zincirine; Pemfigus desmoglein-3'e; "
            "Büllöz pemfigoid BP180/BP230 hemidesmozomuna karşıdır. "
            "2. **Lupus Nefriti Altın Ayrımı:** En sık ve prognozu en kötü olan **Sınıf IV Diffüz Lupus Nefritidir** "
            "(ışık mikroskobunda tel halka - wire loop lezyonları; elektron mikroskobunda masif subendotelyal birikimler). "
            "3. **Otoantikor Spesifiteleri:** "
            "- Anti-Smith (anti-Sm) ve anti-dsDNA: SLE için yüksek derecede **spesifiktir** (anti-dsDNA nefrit ve hastalık aktivitesiyle koreledir). "
            "- Anti-SSA (Ro) ve Anti-SSB (La): Sjögren sendromu ve yenidoğan konjenital kalp bloğu. "
            "- Anti-Scl-70 (DNA topoizomeraz I): Diffüz sistemik skleroz (ağır interstisyel akciğer fibrozu). "
            "- Anti-Sentromer: Sınırlı sistemik skleroz (CREST sendromu). "
            "- Anti-Jo-1 (histidil-tRNA sentetaz): Polimiyozit / Dermatomiyozit (interstisyel akciğer hastalığı eşlikli). "
            "4. **Amiloidoz Fibril Çapı:** Elektron mikroskobunda **7.5 - 10 nm dallanmayan düz fibriller**; "
            "Kongo kırmızısı ile polarize ışıkta **elma yeşili çift kırıcılık**."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Sistemik Sklerozda Antikor ve Klinik Tutulum Zıtlığı",
                "Diffüz Sistemik Skleroz (Anti-Scl-70)",
                "Erken visseral tutulum, yaygın cilt kalınlaşması, yüksek mortalite ve ölümcül akciğer fibrozu",
                "Sınırlı Sistemik Skleroz / CREST (Anti-Sentromer)",
                "Distal cilt tutulumu, kalsinozis, Raynaud, özofagus dismotilitesi, sklerodaktili ve geç pulmoner hipertansiyon"
            ),
            make_active_recall(
                "Sistemik Lupus Eritematozus tanısında sensitivitesi düşük olmasına rağmen SLE için tanısal özgüllüğü (spesifitesi) en yüksek olan iki antikor hangisidir?",
                "Anti-dsDNA ve Anti-Smith (Anti-Sm) antikorlarıdır.",
                "Biri lupus nefriti aktivitesini takip eden, diğeri nükleer ribonükleoprotein hedefli antikor ikilisi"
            )
        ]
    })

    # Slayt 98: Çıkmış Kurul ve TUS Soru Tiplerinin Patolojik Analizi
    slides.append({
        "id": "k1-25-s98",
        "title": "Çıkmış Kurul ve TUS Soru Tiplerinin Patolojik Analizi",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 98,
        "narrative": (
            "Patoloji sınavlarında klinik senaryolar üzerinden sorulan tipik vaka kurguları ve ipuçları: "
            "1. **Vaka 1 (SLE Nefriti):** 24 yaşında kadın hasta, yüzde güneşle artan döküntü (kelebek raş), poliartralji "
            "ve idrar tahlilinde 4 g/gün proteinüri. Biyopside glomerül kapiller duvarlarında tel halka (wire loop) manzarası "
            "ve immünfloresanda IgG, IgM, IgA, C3, C1q tutulumu (**tam ev / full-house patern**). Tanı: Sınıf IV Diffüz Proliferatif Lupus Nefriti. "
            "2. **Vaka 2 (Sjögren Sendromu):** 52 yaşında kadın hasta, gözlerde yanma, kuruluk, ağız kuruluğu ve bilateral parotis bezinde büyüme. "
            "Schirmer testi pozitif. Dudak biyopsisinde minör tükürük bezlerinde periduktal lenfositik infiltrasyon. Bu hastaların en korkulan "
            "uzun dönem malign komplikasyonu nedir? Cevap: **B hücreli non-Hodgkin marjinal zon (MALT) lenfoma** (40 kat risk artışı). "
            "3. **Vaka 3 (AL Amiloidozu):** 65 yaşında multipl miyelom tanılı erkek hasta, dilde aşırı büyüme (makroglossi), periorbital morluklar "
            "(rakun gözü) ve restriktif kalp yetmezliği tablosu ile başvuruyor. Tanı: Monoklonal immünoglobulin lambda hafif zincir kökenli AL amiloidozu. "
            "4. **Vaka 4 (Tip IV Temas Dermatiti):** Nikel içeren kolye taktıktan 48 saat sonra boyunda kaşıntılı, eritemli ve veziküler döküntü. "
            "Mekanizma: Duyarlı CD4+ Th1 lenfositler ve makrofaj aracılı gecikmiş tip aşırı duyarlılık."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "48 yaşında bir kadın hasta son 6 aydır gözlerinde kum varmış hissi, ağız kuruluğu ve yutma güçlüğü ile başvuruyor. Muayenede her iki tarafta parotis bezleri ağrısız olarak büyümüş saptanıyor. Laboratuvarda ANA pozitif, Anti-SSA ve Anti-SSB antikorları yüksek bulunuyor. Dudak biyopsisinde tükürük bezi asinüsleri çevresinde yoğun CD4+ T ve B lenfosit odakları (>50 hücrelik fokus skoru) izleniyor.",
                "Bu hastanın takibinde malignite gelişimi açısından en yüksek risk taşıyan ve düzenli taranması gereken neoplazi hangisidir?",
                [
                    {
                        "text": "B hücreli Non-Hodgkin Lenfoma (özellikle tükürük bezinin MALT / marjinal zon lenfoması)",
                        "isCorrect": True,
                        "explanation": "Doğrudur; Sjögren hastalarında persistan B lenfosit hiperaktivitesi nedeniyle lenfoma riski normal topluma göre yaklaşık 40 kat artmıştır."
                    },
                    {
                        "text": "Tükürük bezi mukoepidermoid karsinomu",
                        "isCorrect": False,
                        "explanation": "Yanlış; tükürük bezinin en sık malign epitelyal tümörü olsa da Sjögren ile doğrudan ilişkili artış göstermez."
                    },
                    {
                        "text": "Akut miyeloblastik lösemi (AML)",
                        "isCorrect": False,
                        "explanation": "Yanlış; miyeloid lösemiler romatolojik zeminle ilişkili primer lenfoid malignite grubu değildir."
                    }
                ]
            ),
            make_micro_quiz(
                "Renal biyopsisinde tüm immünoglobulinler (IgG, IgM, IgA) ve kompleman bileşenleri (C3, C1q) ile granüler floresans ışıması saptanan ('full-house' immünfloresans paterni) bir hastada en olası primer tanı hangisidir?",
                {
                    "A": "Sistemik Lupus Eritematozus (Lupus Nefriti)",
                    "B": "Goodpasture Sendromu",
                    "C": "Poststreptokoksik Glomerülonefrit",
                    "D": "Minimal Değişiklik Hastalığı",
                    "E": "Diyabetik Nefropati"
                },
                "A",
                {
                    "A": "Doğrudur; glomerülde tüm immünoglobulin ve komplemanların birlikte çöktüğü 'full-house' manzarası lupus nefriti için son derece karakteristiktir.",
                    "B": "Yanlış; Goodpasture'da lineer IgG tutulumu vardır.",
                    "C": "Yanlış; poststreptokoksikte subepitelyal hörgüç şeklinde C3 ve IgG vardır.",
                    "D": "Yanlış; minimal değişiklikte immün depolanma izlenmez.",
                    "E": "Yanlış; diyabette immün kompleks birikimi yoktur."
                }
            )
        ]
    })

    # Slayt 99: Birinci Basamak ve Klinik Pratikte Romatolojik/İmmünolojik Olgu Yönetimi
    slides.append({
        "id": "k1-25-s99",
        "title": "Birinci Basamak ve Klinik Pratikte Romatolojik/İmmünolojik Olgu Yönetimi",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 99,
        "narrative": (
            "Genel hekimlik ve klinik yaklaşım açısından romatolojik ve aşırı duyarlılık olgularında kritik ilkeler: "
            "1. **Anafilaksi Acili:** Akut hipersensitivite tablosunda ilk ve en hayati basamak gecikmeksizin "
            "**intramusküler (İM) adrenalin (epinefrin)** uygulanmasıdır; antihistaminikler veya steroidler asla adrenalinin yerini tutamaz. "
            "2. **ANA Testinin Akılcı Kullanımı:** ANA testi aşırı duyarlıdır ancak spesifik değildir; sağlıklı toplumun %10-15'inde "
            "düşük titrede pozitif çıkabilir. Klinik semptomu (artrit, raş, serözit) olmayan hastaya sadece genel tarama amacıyla ANA istenmemelidir. "
            "3. **Lupus Hastasında İdrar Takibi:** Bilinen SLE hastalarında sessiz ilerleyen Sınıf IV lupus nefritini erken yakalamak için "
            "her kontrolde rutin tam idrar tahlili (proteinüri, hematüri ve eritrosit silendirleri) mutlaka incelenmelidir. "
            "4. **Kronik Hastalıklarda Amiloid Profılaksisi:** FMF hastalarında düzenli **kolşisin** tedavisi peritonit ataklarını önlemenin "
            "ötesinde, ölümcül AA amiloidozu gelişimini sıfıra indirir; tedavinin aksatılması nefrotik sendroma davetiye çıkarır. "
            "5. **Amiloidozda Organ Korunması:** Amiloidoz düşünülen hastalarda invaziv organ biyopsisinden önce abdominal yağ aspirasyonu "
            "yapılmalı, vasküler frajilite nedeniyle gereksiz organ travmasından kaçınılmalıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Klinik Pratikte Akut Anafilaktik Acil Yönetim Basamakları",
                [
                    "1. Erken Tanı: Havayolu ödemi, hipotansiyon veya yaygın ürtikerin hızla tanınması",
                    "2. Birinci Seçenek Müdahale: Vakit kaybetmeden uyluk anterolateraline İM Adrenalin enjeksiyonu",
                    "3. Pozisyon ve Oksijen: Hastanın sırtüstü yatırılıp bacaklarının kaldırılması ve yüksek akımlı oksijen verilmesi",
                    "4. Destekleyici Tedavi: Damar yolu açılarak izotonik sıvı infüzyonu ve ikincil antihistaminik/steroid eklenmesi"
                ]
            ),
            make_cloze(
                "Akut sistemik anafilaksi şokunda havayolu kollapsını ve vazodilatasyonu geri çevirmek için derhal uygulanması gereken ilk basamak hayat kurtarıcı ilaç intramusküler adrenalindir.",
                "adrenalindir",
                "Alfa ve beta adrenerjik reseptörleri eşzamanlı uyararak laringeal ödemi ve hipotansiyonu durduran acil hormon"
            )
        ]
    })

    # Slayt 100: Checkpoint 10 / Büyük Kapanış
    slides.append({
        "id": "k1-25-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Aşırı Duyarlılık, Otoimmünite ve Amiloidoz Büyük Özeti",
        "section": "Organ Amiloidozu ve Büyük Sentez",
        "slideNumber": 100,
        "narrative": (
            "Ders 25'in bu final kontrol noktasında, 100 slaytlık dev immünopatoloji maratonunu özetliyoruz: "
            "1. **Dört Aşırı Duyarlılık Tipi:** Tip I (IgE, mast), Tip II (doku antijeni, sitotoksisite/disfonksiyon), "
            "Tip III (immün kompleks, fibrinoid nekrozlu vaskülit), Tip IV (CD4/CD8 T hücreleri, granülom). "
            "2. **Otoimmünite Temelleri:** Santral tolerans (negatif seleksiyon, AIRE), periferik tolerans (anerji, Treg FoxP3, apoptoz Fas/FasL). "
            "3. **Büyük Romatolojik Sendromlar:** "
            "- SLE: Anti-dsDNA, anti-Smith, tam ev / full-house nefrit, tel halka (wire loop). "
            "- Sjögren: Kuru göz (keratokonjonktivit sikka), kuru ağız (kserostomi), anti-SSA/SSB, 40 kat B hücreli lenfoma riski. "
            "- Sistemik Skleroz: Endotel hasarı, PDGF/TGF-beta hiperaktivitesi, aşırı kollajen depolanması; anti-Scl-70 (diffüz), anti-sentromer (CREST). "
            "4. **İmmün Yetmezlikler:** XLA (Bruton, BTK yok, B hücresi yok), DiGeorge (22q11, timus aplazisi, T hücresi yok), SCID (ADA/gama-c mutasyonu), HIV (gp120/CD4/CCR5, <200 AIDS). "
            "5. **Amiloidoz:** Çapraz beta-tabaka; Kongo kırmızısında elma yeşili çift kırıcılık; AL (miyelom hafif zincir), AA (kronik inflamasyon SAA); böbrekte nefrotik sendrom, dalakta sago/lardaceous formlar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s100-1",
                "Amiloid birikiminin dalakta yalnızca Malpighi folikülleriyle (beyaz pulpa) sınırlı kaldığı ve kesit yüzeyinde tapiyoka tanecikleri görüntüsü veren makroskopik form hangisidir?",
                "Dalak Malpighi folikülleridir (beyaz pulpa).",
                "Splenik lenfoid nodüllerinin lenfosit zengin mikroçevresi",
                "Sago Dalağı"
            ),
            make_flashcard(
                "k1-25-fc-s100-2",
                "Sistemik amiloidoz şüphesinde majör organ kanama riskinden kaçınmak amacıyla ilk tercih edilen minimal invaziv tanısal tarama yöntemi nedir?",
                "Abdominal yağ dokusu aspirasyonudur.",
                "Göbek çevresinden iğneyle subkütan stromal materyal çekilmesi",
                "Amiloidoz Biyopsisi"
            ),
            make_flashcard(
                "k1-25-fc-s100-3",
                "Yaşlı erkeklerin kalbinde yavaşça birikerek izole senil kardiyak amiloidoza yol açan ve genetik mutasyon içermeyen normal plazma proteini nedir?",
                "Yabanıl transtiretin proteinidir.",
                "Tiroksin ve A vitamini taşıyan karaciğer sentezli wild-type plazma globulini",
                "Transtiretin (ATTR)"
            )
        ],
        "interactiveElements": [
            make_table(
                "Ders 25: İmmünopatoloji ve Amiloidoz Büyük Kapanış Matrisi",
                ["Ana Başlık", "Temel Patofizyolojik Mekanizma", "Spesifik Patolojik Belirteç", "Primer Klinik Sonuç"],
                [
                    ["Hipersensitivite Tip I-IV", "IgE, sitotoksik antikor, immün kompleks, T hücresi", "Fibrinoid nekroz, granülom, degranülasyon", "Anafilaksi, lupus nefriti, tüberküloz"],
                    ["Sistemik Lupus Eritematozus", "Nükleer antijenlere tolerans kaybı ve immün kompleksler", "Anti-dsDNA, anti-Smith, wire-loop, full-house", "Malar raş, nefrotik sendrom, vaskülit"],
                    ["Sjögren Sendromu", "Ekzokrin bezlerin lenfositik destrüksiyonu", "Anti-SSA (Ro), Anti-SSB (La)", "Keratokonjonktivit sikka, kserostomi, lenfoma"],
                    [
                        "Sistemik Skleroz",
                        "Mikrovasküler endotel hasarı ve TGF-beta fibrozu",
                        {"text": "Anti-Scl-70 (diffüz) ve Anti-sentromer (sınırlı)", "isMasked": True, "hint": "Sistemik sklerozun visseral fibroz veya CREST alt tiplerini ayıran antikorlar"},
                        "Sklerodaktili, Raynaud, disfaji, pulmoner fibroz"
                    ],
                    ["Amiloidoz", "Çözünmeyen çapraz beta-kırmalı fibriller birikimi", "Kongo kırmızısı ile elma yeşili çift kırıcılık", "Nefrotik böbrek, restriktif kalp, sago dalak"]
                ]
            ),
            make_micro_quiz(
                "Tüm Ders 25 boyunca incelenen immünopatolojik tablolar göz önüne alındığında, aşağıdaki eşleştirmelerden hangisi tamamen DOĞRUDUR?",
                {
                    "A": "Sjögren sendromu - Tükürük bezi MALT lenfoması gelişme riski",
                    "B": "Goodpasture sendromu - Dolaşan immün komplekslerin damarda birikmesi (Tip III)",
                    "C": "Bruton hastalığı - Timus aplazisi ve konjenital hipokalsemi",
                    "D": "AL amiloidozu - Kronik enfeksiyonlarda karaciğerden sentezlenen SAA proteini",
                    "E": "CREST sendromu - Anti-dsDNA antikoru pozitifliği ve diffüz kutanöz fibroz"
                },
                "A",
                {
                    "A": "Doğrudur; Sjögren sendromunda persistan B lenfosit uyarısı nedeniyle MALT / marjinal zon lenfoma riski 40 kat artmıştır.",
                    "B": "Yanlış; Goodpasture Tip II hipersensitivitedir (bazal membran otoantikoru).",
                    "C": "Yanlış; Bruton'da BTK mutasyonu vardır; timus aplazisi DiGeorge'dur.",
                    "D": "Yanlış; SAA'dan köken alan AA amiloidozudur; AL monoklonal hafif zincirdir.",
                    "E": "Yanlış; CREST'te anti-sentromer pozitiftir; anti-dsDNA SLE'dedir."
                }
            )
        ]
    })

    return slides
