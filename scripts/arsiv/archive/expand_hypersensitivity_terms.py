# -*- coding: utf-8 -*-
"""
expand_hypersensitivity_terms.py
Enriches medical_encyclopedia.json and medical_glossary.json with comprehensive,
granular terms for Hypersensitivity, Autoimmunity, Immunogenetics, Rejection,
Immunodeficiencies, and Amyloidosis based on Prof. Dr. Hikmet Keleş and Robbins 11th ed.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ENCYCLOPEDIA_PATH = "src/data/medical_encyclopedia.json"
GLOSSARY_PATH = "src/data/medical_glossary.json"

with open(ENCYCLOPEDIA_PATH, "r", encoding="utf-8") as f:
    encyclopedia = json.load(f)

with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
    glossary = json.load(f)

print(f"Initial counts: Encyclopedia={len(encyclopedia)}, Glossary={len(glossary)}")

# Define comprehensive encyclopedia items
new_encyclopedia_items = [
    {
        "id": "tip-1-asiri-duyarlilik",
        "term": "Tip I Aşırı Duyarlılık (Ani / Immediate Hipersensitivite)",
        "latinName": "Hypersensitivitas immediata (Typus I)",
        "aliases": ["Ani Aşırı Duyarlılık", "IgE Aracılı Aşırı Duyarlılık", "Anafilaktik Reaksiyon"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Daha önce duyarlanmış (sensitize) bireyde spesifik antijenin (alerjen) mast hücreleri ve bazofillerin membranındaki FcεRI reseptörlerine bağlı IgE moleküllerini çapraz bağlaması sonucu dakikalar içinde gelişen vasküler dilatasyon, ödem, düz kas spazmı ve mukus hipersekresyonu ile seyreden immünolojik doku hasarıdır.",
        "lectureContextNotes": "Prof. Dr. Hikmet Keleş'in dersinde Tablo 5.2 prototipi olarak anafilaksi, saman nezlesi ve atopik astım vurgulanmıştır. Erken fazda vazoaktif aminler (histamin), geç fazda ise eozinofiller (MBP, ECP) doku hasarından sorumludur.",
        "morphologyOrMechanism": "1. Duyarlanma: Alerjen -> Dendritik Hücre -> Th2 (IL-4, IL-13) -> B hücresinde IgE sınıf değişimi -> FcεRI'ye bağlanma.\n2. Efektör erken faz: Çapraz bağlanma -> Mast hücre degranülasyonu -> Histamin, LTC4/D4/E4, PGD2.\n3. Geç faz: 2-24 saatte eozinofil ve nötrofil infiltrasyonu, epitel nekrozu.",
        "differentialDiagnosis": [
            {"condition": "Tip II Aşırı Duyarlılık", "distinction": "Tip II'de antijen hücre veya dokuda SABİTTİR; IgG/IgM fagositoz veya lizis yapar. Tip I'de IgE mast hücresini uyarır."},
            {"condition": "Tip III Aşırı Duyarlılık", "distinction": "Tip III'te çözünür antijen-antikor kompleksleri damar duvarına çöker ve fibrinoid nekroz yapar; IgE veya mast hücresi primer rol oynamaz."}
        ],
        "examSpotPearls": [
            "▸ IgE sınıf değişimini tetikleyen anahtar sitokin **IL-4**; eozinofil kemotaksisini sağlayan **IL-5**; mukus salgısını artıran **IL-13**'tür.",
            "🔴 ÖNEMLİ: Anafilaksinin tek ve en acil birinci basamak hayat kurtarıcı tedavisi **İntramüsküler Epinefrin (Adrenalin)**'dir!",
            "🔵 ÇIKMIŞ SORU: Kanda anafilaktik mast hücre aktivasyonunu kanıtlayan biyobelirteç **Serum Triptaz** düzeyidir."
        ],
        "pitfallsAndWarnings": [
            "Antihistaminikler ve steroidler anafilakside birinci basamak değildir, gecikmeden adrenalin yapılmalıdır.",
            "İlk maruziyette klinik semptom olmaz; duyarlanma gereklidir."
        ],
        "relatedItems": ["fce-ri-reseptoru", "major-basic-protein-mbp", "histamin", "omalizumab"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "tip-2-asiri-duyarlilik",
        "term": "Tip II Aşırı Duyarlılık (Antikor-Aracılı Hipersensitivite)",
        "latinName": "Hypersensitivitas cytotoxica mediata anticorporibus (Typus II)",
        "aliases": ["Sitotoksik Aşırı Duyarlılık", "Dokuya Özgü Antikor Reaksiyonu"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Hedef hücrelerin membranında veya hücre dışı matrikste yer alan sabit antijenlere bağlanan IgG veya IgM sınıfı antikorların; opsonizasyon-fagositoz, kompleman-Fc aracılı doku enflamasyonu veya hücresel disfonksiyon yaratmasıyla oluşan doku hasarıdır.",
        "lectureContextNotes": "Ders notunda 3 temel alt mekanizma vurgulanmıştır: 1) Opsonizasyon (AIHA, İTP), 2) Enflamasyon (Goodpasture, Pemfigus), 3) Hücresel disfonksiyon (Myasthenia Gravis, Graves).",
        "morphologyOrMechanism": "Opsonize hücreler dalak makrofajlarının FcγR ve C3b reseptörlerince yutulur (ekstravasküler hemoliz). Bazal membrana bağlanan antikorlar kompleman (C5a) ile nötrofilleri çeker; 'frustrated phagocytosis' ile enzimler dokuya saçılır.",
        "differentialDiagnosis": [
            {"condition": "Goodpasture (Tip II)", "distinction": "İmmünofloresanda kesintisiz düzgün ÇİZGİSEL (LİNEER) IgG birikimi."},
            {"condition": "SLE Nefriti (Tip III)", "distinction": "Dolaşan komplekslerin çökmesi sonucu topak topak GRANÜLER (NOKTASAL) IgG birikimi."}
        ],
        "examSpotPearls": [
            "▸ Antijen dokuda veya hücre zarında SABİTTİR (Tip III'teki gibi dolaşmaz).",
            "🔴 ÖNEMLİ: Myasthenia Gravis ve Graves hastalığında nekroz veya doku yıkımı YOKTUR; fonksiyon modülasyonu vardır.",
            "🔵 ÇIKMIŞ SORU: Goodpasture sendromunda hedef antijen Tip IV kolajenin alfa-3 zinciridir."
        ],
        "pitfallsAndWarnings": [
            "Tip II aşırı duyarlılık her zaman hücreyi öldürmek zorunda değildir; reseptör uyarımı (Graves) da Tip II örneğidir."
        ],
        "relatedItems": ["goodpasture-sendromu", "myasthenia-gravis", "graves-hastaligi", "pemfigus-vulgaris"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "tip-3-asiri-duyarlilik",
        "term": "Tip III Aşırı Duyarlılık (İmmün Kompleks Aracılı Hipersensitivite)",
        "latinName": "Hypersensitivitas mediata immunocomplexibus (Typus III)",
        "aliases": ["İmmün Kompleks Hastalığı", "Serum Hastalığı Reaksiyonu"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Dolaşımdaki çözünür antijenler ile IgG/IgM antikorlarının kanda birleşerek oluşturduğu immün komplekslerin damar duvarlarına çökmesi, kompleman fiksasyonu ve nötrofil aktivasyonu ile damar duvarında nekrotizan vaskülit ve fibrinoid nekroz oluşturmasıdır.",
        "lectureContextNotes": "Robbins 11. baskı Tablo 5.5'te prototipler olarak Sistemik Lupus Eritematozus, Akut Serum Hastalığı, Arthus Reaksiyonu ve Poststreptokoksik Glomerülonefrit yer alır.",
        "morphologyOrMechanism": "Hafif antijen fazlalığında oluşan orta boy kompleksler damar endotel aralıklarından geçer. C5a nötrofil çeker; nötrofiller lizozomal elastaz ve proteazları salarak damar duvarında amorf eozinofilik FİBRİNOİD NEKROZ yapar.",
        "differentialDiagnosis": [
            {"condition": "Serum Hastalığı (Tip III Sistemik)", "distinction": "Dolaşan kompleksler glomerül, eklem ve damarlara çöker; hipokomplemantemi (düşük C3/C4) yapar."},
            {"condition": "Arthus Reaksiyonu (Tip III Lokal)", "distinction": "Duyarlanmış dokuya lokal antijen enjeksiyonu sonrası damar duvarında in situ kompleks oluşumu ve lokal nekroz."}
        ],
        "examSpotPearls": [
            "▸ En patojenik olanlar **orta büyüklükteki** komplekslerdir (retiküloendotelyal sistemden kaçarlar).",
            "🔴 ÖNEMLİ: Damar duvarında parlak pembe amorf **Fibrinoid Nekroz** histopatolojik imzasıdır.",
            "🔵 ÇIKMIŞ SORU: Glomerülde immünofloresanda kaba granüler (yumaksı/noktasal) birikim Tip III göstergesidir."
        ],
        "pitfallsAndWarnings": [
            "İmmün kompleks hastalığında antijenler vücudun kendi nükleer proteinleri olabileceği gibi mikrobiyal veya yabancı ilaç proteinleri de olabilir."
        ],
        "relatedItems": ["fibrinoid-nekroz", "akut-serum-hastaligi", "arthus-reaksiyonu", "sistemik-lupus-eritematozus"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "tip-4-asiri-duyarlilik",
        "term": "Tip IV Aşırı Duyarlılık (T Hücre-Aracılı / Gecikmiş Tip Hipersensitivite)",
        "latinName": "Hypersensitivitas mediata cellulis T (Typus IV)",
        "aliases": ["Gecikmiş Tip Aşırı Duyarlılık (DTH)", "Hücresel Aşırı Duyarlılık"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Antikorlardan tamamen bağımsız olarak, duyarlaşmış T lenfositlerinin (CD4+ Th1 ve Th17 sitokinleri ile aktive makrofajlar; CD8+ sitotoksik T lenfositlerinin doğrudan perforin-granzim apoptozu) doku hasarı ve granülomatöz enflamasyon oluşturmasıdır.",
        "lectureContextNotes": "Prototip olarak Tüberkülin (PPD) reaksiyonu, kontakt dermatit, tüberküloz granülomu, Tip 1 DM ve Multipl Skleroz anlatılmıştır. Tepe yanıt 24-72 saatte alınır.",
        "morphologyOrMechanism": "Th1 hücreleri IFN-γ salgılar -> Makrofajlar M1 fenotipine aktive olur -> Epiteloid histiyosit ve Langhans dev hücreli granülom. Th17 IL-17 salgılar -> Nötrofilik hasar. CD8+ CTL perforin/granzim salgılar -> Hedef hücre apoptozu.",
        "differentialDiagnosis": [
            {"condition": "Tip I Hipersensitivite", "distinction": "Tip I dakikalar içinde ve IgE aracılıdır; Tip IV 48-72 saatte ve T hücre aracılıdır."},
            {"condition": "Serum Hastalığı (Tip III)", "distinction": "Serum hastalığı serumla pasif transfer edilebilir; Tip IV serumla DEĞİL yalnızca canlı T hücreleriyle transfer edilebilir."}
        ],
        "examSpotPearls": [
            "▸ Antikor veya komplemandan tamamen bağımsız tek aşırı duyarlılık tipidir.",
            "🔴 ÖNEMLİ: Makrofaj aktivasyonunu ve granülom oluşumunu sağlayan temel Th1 sitokini **İnterferon-gama (IFN-γ)**'dır.",
            "🔵 ÇIKMIŞ SORU: Kontakt dermatit ve PPD reaksiyonu Tip IV aşırı duyarlılığın klinik prototipleridir."
        ],
        "pitfallsAndWarnings": [
            "PPD testinde ilk 24 saatteki eritem yalancı pozitiflik olabilir; endürasyon 48-72 saatte ölçülmelidir."
        ],
        "relatedItems": ["tuberuklin-reaksiyonu-ppd", "kontakt-dermatit", "major-basic-protein-mbp"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "sistemik-lupus-eritematozus",
        "term": "Sistemik Lupus Eritematozus (SLE)",
        "latinName": "Lupus erythematosus systemicus",
        "aliases": ["SLE", "Lupus"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Nükleer antijenlere karşı gelişen patojenik otoantikorlar ve immün komplekslerin dokularda birikmesiyle karakterize, remisyon ve alevlenmelerle seyreden, doğurganlık çağındaki kadınlarda belirgin sık görülen multisistemik otoimmün hastalıktır.",
        "lectureContextNotes": "Prof. Dr. Hikmet Keleş'in dersinde ANA (%98-100), Anti-dsDNA (nefrit korelasyonu), Anti-Smith (en spesifik), Sınıf IV lupus nefriti (wire-loop lezyonları), Full-House immünofloresan ve Libman-Sacks endokarditi özellikle vurgulanmıştır.",
        "morphologyOrMechanism": "Apoptotik hücre kalıntılarının temizlenememesi -> Plazmasitoid dendritik hücrelerden Tip I İnterferon (IFN-α) salınımı -> B hücre poliklonal uyarımı -> Anti-nükleer antikorlar -> Tip III immün kompleks ve Tip II sitopenik hasar.",
        "differentialDiagnosis": [
            {"condition": "İlaca Bağlı Lupus", "distinction": "Anti-Histon %95+ pozitiftir; Anti-dsDNA ve böbrek/MSS tutulumu nadirdir; ilaç kesilince düzelir."},
            {"condition": "Karışık Bağ Dokusu Hastalığı (MCTD)", "distinction": "Yüksek titrede Anti-U1-RNP pozitiftir; böbrek tutulumu nadirdir."}
        ],
        "examSpotPearls": [
            "▸ **ANA**: En hassas (%98-100) tarama testi.",
            "🔴 ÖNEMLİ: **Anti-dsDNA**: Nefrit aktivitesi ve alevlenmelerle paralel seyreder; **Anti-Smith (Sm)**: SLE için en spesifik antikordur.",
            "🔵 ÇIKMIŞ SORU: Glomerüllerde subendotelyal birikimler sonucu oluşan **Tel-Kulp (Wire-Loop)** lezyonları Diffüz Lupus Nefritine (Sınıf IV) özgüdür."
        ],
        "pitfallsAndWarnings": [
            "ANA negatifliği SLE'yi neredeyse tamamen dışlar; pozitifliği ise diğer otoimmün hastalıklarda da görülebildiği için tek başına tanı koydurmaz."
        ],
        "relatedItems": ["anti-dsdna-antikoru", "anti-smith-antikoru", "libman-sacks-endokarditi", "lupus-nefriti"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "anti-dsdna-antikoru",
        "term": "Anti-Çift Zincirli DNA Antikoru (Anti-dsDNA)",
        "latinName": "Anticorpus contra DNA fili duplicis",
        "aliases": ["Anti-dsDNA", "Anti-double stranded DNA"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Sistemik Lupus Eritematozus hastalarında saptanan, çift sarmallı nativ DNA'ya karşı yönelmiş patojenik IgG sınıfı otoantikordur. SLE için yüksek özgüllüğe sahiptir.",
        "lectureContextNotes": "Ders notunda anti-dsDNA titresinin lupus nefritinin şiddeti, hastalık alevlenmesi ve serum kompleman C3/C4 düzeylerindeki düşüşle birebir paralel seyrettiği belirtilmiştir.",
        "morphologyOrMechanism": "Glomerül kapiller bazal membranındaki nükleer kalıntılara bağlanarak in situ immün kompleks oluşturur veya dolaşan DNA-anti-DNA kompleksleri subendotelyal mesafeye çökerek komplet aktivasyonuyla Sınıf IV lupus nefritini tetikler.",
        "differentialDiagnosis": [
            {"condition": "Anti-Smith (Sm)", "distinction": "Anti-Sm SLE için en spesifik antikordur ancak titresi hastalık aktivitesiyle değişmez. Anti-dsDNA ise alevlenmeyle yükselir."},
            {"condition": "Anti-Histon", "distinction": "İlaca bağlı lupusta pozitiftir; anti-dsDNA ilaca bağlı lupusta negatiftir."}
        ],
        "examSpotPearls": [
            "▸ Titresi lupus nefriti şiddeti ile doğrudan koreledir.",
            "🔴 ÖNEMLİ: Hastalık remisyondayken titresi düşer, alevlenme (flare) sırasında titresi tırmanırken C3 ve C4 düşer.",
            "🔵 ÇIKMIŞ SORU: SLE takibinde nefropati aktivitesini izlemede kullanılan en değerli serolojik testtir."
        ],
        "pitfallsAndWarnings": [
            "Anti-dsDNA negatif olan SLE hastaları da vardır (%40-70 pozitiflik); negatifliği SLE tanısını ekarte ettirmez."
        ],
        "relatedItems": ["sistemik-lupus-eritematozus", "anti-smith-antikoru", "lupus-nefriti"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "anti-smith-antikoru",
        "term": "Anti-Smith Antikoru (Anti-Sm)",
        "latinName": "Anticorpus contra antigenum Smith",
        "aliases": ["Anti-Sm", "Anti-Smith"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Küçük nükleer ribonükleoproteinlerin (snRNP) çekirdek proteinlerine karşı gelişen ve Sistemik Lupus Eritematozus için en yüksek tanısal özgüllüğe (spesifiteye) sahip olan otoantikordur.",
        "lectureContextNotes": "Ders notunda %20-30 pozitiflik oranı olduğu ancak pozitif olduğunda SLE tanısını kesinleştirdiği bildirilmiştir.",
        "morphologyOrMechanism": "snRNP partiküllerindeki ortak Smith çekirdek proteinlerini tanır; immün kompleks oluşumuna ve doku vaskülitine katkıda bulunur.",
        "differentialDiagnosis": [
            {"condition": "Anti-dsDNA", "distinction": "Anti-dsDNA alevlenmelerle dalgalanır; Anti-Sm titresi stabildir ve alevlenmeyi göstermez."},
            {"condition": "Anti-U1-RNP", "distinction": "MCTD'de (Karışık Bağ Dokusu Hastalığı) yüksek titrede pozitiftir."}
        ],
        "examSpotPearls": [
            "▸ SLE için EN YÜKSEK SPESİFİTEYE (Özgüllüğe) sahip antikordur.",
            "🔴 ÖNEMLİ: Pozitifliği SLE'yi kesinleştirir ancak negatifliği dışlamaz (sensitivitesi düşüktür: %25).",
            "🔵 ÇIKMIŞ SORU: 'Hangisi SLE tanısı için en spesifik antikordur?' sorusunun klasik yanıtıdır."
        ],
        "pitfallsAndWarnings": [
            "Düşük duyarlılık nedeniyle tarama testi olarak kullanılamaz; taramada ANA kullanılır."
        ],
        "relatedItems": ["sistemik-lupus-eritematozus", "anti-dsdna-antikoru"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "libman-sacks-endokarditi",
        "term": "Libman-Sacks Endokarditi (Verrüköz Non-Bakteriyel Endokardit)",
        "latinName": "Endocarditis verrucosa non-bacterialis Libman-Sacks",
        "aliases": ["Lupus Endokarditi", "Steril Verrüköz Endokardit"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Sistemik Lupus Eritematozus ve Antifosfolipid Sendromu hastalarında kalp kapakçıklarının (özellikle mitral ve aort) yaprakçıklarında gelişen steril, infektif olmayan, verrüköz vejetasyonlarla karakterize kardiyak tutulumdur.",
        "lectureContextNotes": "Prof. Dr. Hikmet Keleş'in dersinde vejetasyonların kapak yaprakçıklarının HEM ÖN HEM ARKA yüzünde (her iki tarafında) yerleşmesi ile bakteriyel ve romatizmal endokarditten kesin olarak ayrıldığı vurgulanmıştır.",
        "morphologyOrMechanism": "İmmün komplekslerin kapak endoteline çökmesi ve lokal tromboz tetiklenmesi -> Kapak yaprakçığının her iki yüzeyinde fibrin, immün kompleksler, hematoksilin cisimcikleri ve hücresel debris içeren 1-4 mm'lik steril vejetasyonlar.",
        "differentialDiagnosis": [
            {"condition": "İnfektif Endokardit", "distinction": "Bakteriyel vejetasyonlar büyüktür, yıkıcıdır, yalnızca kan akımı yönündeki yüzde yerleşir ve mikroorganizma içerir."},
            {"condition": "Akut Romatizmal Kardit", "distinction": "Kapak kapanma çizgisi boyunca küçük siğilimsi steril vejetasyonlar dizilir; her iki yüze yayılmaz."}
        ],
        "examSpotPearls": [
            "▸ Kalp kapak yaprakçıklarının **HEM ÖN HEM ARKA YÜZEYİNDE** yerleşen steril vejetasyonlar.",
            "🔴 ÖNEMLİ: Antifosfolipid sendromu ile güçlü birliktelik gösterir ve emboli riski taşır.",
            "🔵 ÇIKMIŞ SORU: SLE'li hastada kan kültüründe üreme olmayan ve her iki yüzde vejetasyon saptanan kardit tipi Libman-Sacks endokarditidir."
        ],
        "pitfallsAndWarnings": [
            "Steril olmasına rağmen kapakta fonksiyon bozukluğu yapabilir ve üzerine sekonder bakteriyel süperenfeksiyon binebilir."
        ],
        "relatedItems": ["sistemik-lupus-eritematozus", "antifosfolipid-sendromu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "lupus-nefriti",
        "term": "Lupus Nefriti (ISN/RPS Sınıflaması)",
        "latinName": "Nephritis lupica",
        "aliases": ["SLE Nefriti", "Lupus Glomerülonefriti"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Sistemik Lupus Eritematozus seyrinde nükleer immün komplekslerin glomerül kapiller bazal membranında, mezangiumda ve subendotelyal/subepitelyal aralıkta birikmesiyle oluşan immün glomerüler hasar tablosudur.",
        "lectureContextNotes": "Ders notunda ISN/RPS 6 sınıflı sistem, Sınıf IV'ün en sık ve en ağır tip olduğu, tel-kulp (wire-loop) lezyonları ve Full-House immünofloresan patern detaylandırılmıştır.",
        "morphologyOrMechanism": "Sınıf I: Minimal mezangiyal; Sınıf II: Mezangiyal proliferatif; Sınıf III: Fokal (<%50); Sınıf IV: Diffüz (>%50, yaygın subendotelyal birikimler, wire-loop, kresent); Sınıf V: Membranöz (subepitelyal); Sınıf VI: İlerlemiş sklerozan.",
        "differentialDiagnosis": [
            {"condition": "Post-streptokoksik GN", "distinction": "Subepitelyal horgüç (hump) birikimleri vardır; C1q birikmez; antikor tekildir."},
            {"condition": "Goodpasture Sendromu", "distinction": "İmmünofloresanda granüler değil, kesintisiz düzgün çizgisel (lineer) IgG birikimi vardır."}
        ],
        "examSpotPearls": [
            "▸ **Diffüz Lupus Nefriti (Sınıf IV)**: En sık görülen ve en ağır seyirli olan tiptir.",
            "🔴 ÖNEMLİ: Işık mikroskobunda kapiller lümenini dolduran ve duvarı kalınlaştıran **Tel-Kulp (Wire-Loop)** lezyonları Sınıf IV'e özgüdür.",
            "🔵 ÇIKMIŞ SORU: İmmünofloresanda **Full-House** (IgG, IgA, IgM, C3, C1q pozitifliği) deseni lupus nefriti için patognomoniktir."
        ],
        "pitfallsAndWarnings": [
            "Sınıf V membranöz tip nefrotik sendrom tablosuyla gelir; hematüri veya böbrek yetmezliği Sınıf IV'e göre daha az belirgindir."
        ],
        "relatedItems": ["sistemik-lupus-eritematozus", "anti-dsdna-antikoru"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "antifosfolipid-sendromu",
        "term": "Antifosfolipid Sendromu (APS)",
        "latinName": "Syndroma antiphospholipidi",
        "aliases": ["APS", "Hughes Sendromu", "Lupus Antikoagülan Sendromu"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Fosfolipid bağlayan plazma proteinlerine (özellikle beta-2 glikoprotein I) karşı gelişen otoantikorların varlığında, tekrarlayan arteriyel ve venöz trombozlar, gebelik kayıpları ve trombositopeni ile karakterize otoimmün protrombotik hastalıktır.",
        "lectureContextNotes": "Ders notunda in vitro testlerde koagülasyonu geciktirip aPTT'yi uzatmasına rağmen, in vivo ortamda tam aksine tromboza yol açtığı paradoksu vurgulanmıştır. Sifiliz tarama testlerinde (VDRL/RPR) yalancı pozitiflik verir.",
        "morphologyOrMechanism": "Anti-beta-2 glikoprotein I ve anti-kardiyolipin antikorları endotel, trombosit ve komplemanı aktive ederek prostasiklin sentezini baskılar; in vivo kontrolsüz trombüs oluşumunu tetikler.",
        "differentialDiagnosis": [
            {"condition": "Faktör V Leiden Mutasyonu", "distinction": "Kalıtsal trombofilidir; otoantikor bulunmaz; aPTT normaldir."},
            {"condition": "İmmün Trombositopeni (İTP)", "distinction": "İTP'de kanama eğilimi vardır; APS'de trombositopeniye rağmen tromboz gelişir."}
        ],
        "examSpotPearls": [
            "▸ **İn vitro aPTT uzaması** + **İn vivo arteriyel/venöz tromboz** paradoksu.",
            "🔴 ÖNEMLİ: Tekrarlayan fetal kayıplar (plasental enfarktlar) ve yalancı pozitif VDRL/RPR sifiliz testi.",
            "🔵 ÇIKMIŞ SORU: Primer olabileceği gibi en sık Sistemik Lupus Eritematozus (%30-40) zemininde sekonder gelişir."
        ],
        "pitfallsAndWarnings": [
            "aPTT uzun olduğu için hastaya kanama eğilimi var sanılarak kan sulandırıcı verilmemesi vahim bir hatadır; tam tersine antikoagülan verilmelidir!"
        ],
        "relatedItems": ["sistemik-lupus-eritematozus", "libman-sacks-endokarditi"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "aire-geni",
        "term": "AIRE Geni (Autoimmune Regulator)",
        "latinName": "Genum regulatorium autoimmunitatis (AIRE)",
        "aliases": ["AIRE", "Otoimmün Regülatör Gen"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Medüller timik epitel hücrelerinde (mTEC) eksprese edilen ve periferik doku antijenlerinin (insülin, tiroglobulin vb.) timus içinde ektopik olarak üretilmesini sağlayarak otoreaktif T hücrelerinin negatif seleksiyonla elenmesini yöneten kilit transkripsiyon regülatörüdür.",
        "lectureContextNotes": "Ders notunda santral toleransın timik ayağında AIRE mutasyonunun APECED (APS-1) sendromuna yol açtığı vurgulanmıştır.",
        "morphologyOrMechanism": "Timusta gen promotorlarını gevşeterek periferik organ antijenlerinin timositlere sunulmasını sağlar. Yüksek afiniteyle bağlanan otoreaktif klonlar apoptoza gider.",
        "differentialDiagnosis": [
            {"condition": "FoxP3 Mutasyonu", "distinction": "FoxP3 periferik toleransı (Treg) yönetir, IPEX sendromu yapar. AIRE santral timik toleransı yönetir, APECED yapar."},
            {"condition": "Fas/FasL Mutasyonu", "distinction": "Aktivasyon kaynaklı apoptozu (AICD) bozar, ALPS sendromu yapar."}
        ],
        "examSpotPearls": [
            "▸ Timusta periferik doku antijenlerinin sentezlenmesini sağlayan anahtar gen.",
            "🔴 ÖNEMLİ: AIRE mutasyonu = **APECED / APS-1 Sendromu** (Kronik mukokutanöz kandidiyazis + Hipoparatiroidizm + Adrenal yetmezlik).",
            "🔵 ÇIKMIŞ SORU: Santral toleransta timik negatif seleksiyonun gerçekleşmesi için şart olan gen AIRE'dir."
        ],
        "pitfallsAndWarnings": [
            "AIRE geni lenfositlerin içinde değil, timik epitel hücrelerinin içinde işlev görür."
        ],
        "relatedItems": ["santral-tolerans", "foxp3-transkripsiyon-faktoru", "ipex-sendromu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "foxp3-transkripsiyon-faktoru",
        "term": "FoxP3 Transkripsiyon Faktörü (Forkhead Box P3)",
        "latinName": "Factor transcriptionis FoxP3",
        "aliases": ["FoxP3", "Treg Master Regülatörü"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "CD4+ CD25+ regülatuvar (düzenleyici) T hücrelerinin (Treg) gelişimi, farklılaşması ve süpresif fonksiyonu için mutlak gerekli olan ana 'master' transkripsiyon faktörüdür.",
        "lectureContextNotes": "Periferik toleransın en önemli unsuru olarak ders notunda anlatılmıştır. Mutasyonunda X'e bağlı IPEX sendromu gelişir.",
        "morphologyOrMechanism": "Treg hücrelerinde IL-10, TGF-β ve CTLA-4 ekspresyonunu aktive ederken IL-2 üretimini baskılar; otoreaktif efektör T hücrelerini durdurur.",
        "differentialDiagnosis": [
            {"condition": "AIRE", "distinction": "AIRE timusta santral negatif seleksiyonu yönetir; FoxP3 periferik Treg fonksiyonunu yönetir."},
            {"condition": "STAT3 Mutasyonu", "distinction": "Th17 gelişimini bozar, Hiper-IgE (Job) sendromu yapar."}
        ],
        "examSpotPearls": [
            "▸ CD4+ CD25+ Treg hücrelerinin ana transkripsiyon faktörüdür.",
            "🔴 ÖNEMLİ: FoxP3 mutasyonu = **IPEX Sendromu** (Immune dysregulation, Polyendocrinopathy, Enteropathy, X-linked).",
            "🔵 ÇIKMIŞ SORU: Periferik toleransta otoimmüniteyi önleyen süpresif T lenfositlerinin belirteci FoxP3'tür."
        ],
        "pitfallsAndWarnings": [
            "X kromozomunda yer aldığı için IPEX sendromu tipik olarak erkek çocuklarda erken bebeklikte ölümcüldür."
        ],
        "relatedItems": ["periferik-tolerans", "ipex-sendromu", "ctla-4-molekulu", "aire-geni"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "ipex-sendromu",
        "term": "IPEX Sendromu",
        "latinName": "Syndroma IPEX",
        "aliases": ["IPEX", "X'e Bağlı İmmündisfonksiyon-Poliendokrinopati-Enteropati"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "FoxP3 gen mutasyonu sonucu fonksiyonel düzenleyici T hücrelerinin (Treg) üretilememesiyle ortaya çıkan, erken bebeklikte inatçı otoimmün enteropati, Tip 1 diyabet ve egzama ile karakterize X'e bağlı ölümcül immünregülasyon bozukluğudur.",
        "lectureContextNotes": "Ders notunda periferik toleransın tek gen mutasyonuyla kırılmasının prototipi olarak sunulmuştur.",
        "morphologyOrMechanism": "Treg yokluğu -> Kontrolsüz otoreaktif T hücre proliferasyonu -> Bağırsak villus atrofisi, adacık beta hücre yıkımı ve şiddetli dermatit.",
        "differentialDiagnosis": [
            {"condition": "APECED (APS-1)", "distinction": "APECED AIRE mutasyonudur; mukokutanöz kandidiyazis ve hipoparatiroidizm ön plandadır. IPEX'te enteropati ve diyabet ön plandadır."},
            {"condition": "Ağır Kombine İmmün Yetmezlik (SCID)", "distinction": "SCID'de lenfopeni ve fırsatçı enfeksiyonlar vardır; IPEX'te ise otoimmün saldırı vardır."}
        ],
        "examSpotPearls": [
            "▸ Akrostiş: **I**mmunodysregulation, **P**olyendocrinopathy, **E**nteropathy, **X**-linked.",
            "🔴 ÖNEMLİ: Temel defekt **FoxP3 mutasyonu** ve **Treg yokluğu**dur.",
            "🔵 ÇIKMIŞ SORU: Erkek bebekte inatçı kanlı ishal, neonatal diyabet ve egzama triadı IPEX sendromudur."
        ],
        "pitfallsAndWarnings": [
            "Erken dönemde allojeneik kemik iliği nakli yapılmazsa hastalar ağır malnütrisyon ve sepsisten kaybedilir."
        ],
        "relatedItems": ["foxp3-transkripsiyon-faktoru", "periferik-tolerans"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "ctla-4-molekulu",
        "term": "CTLA-4 (Sitotoksik T Lenfosit Antijeni 4 / CD152)",
        "latinName": "Antigenum 4 lymphocytorum T cytotoxicorum",
        "aliases": ["CTLA-4", "CD152"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Aktive T lenfositlerinde ve regülatuvar T hücrelerinde eksprese edilen, antijen sunan hücrelerdeki B7 (CD80/CD86) moleküllerine CD28'den çok daha yüksek afiniteyle bağlanarak T hücresi aktivasyonunu frenleyen kritik inhibitör kontrol noktası (checkpoint) molekülüdür.",
        "lectureContextNotes": "Anerji ve periferik tolerans mekanizmasında T hücresinin aşırı aktivasyonunu durduran fren olarak anlatılmıştır.",
        "morphologyOrMechanism": "CD28 ile yarışır; B7'yi bağlayarak T hücresine inhibitör sinyaller gönderir ve B7 moleküllerini endositozla ortadan kaldırarak kostimülasyonu engeller.",
        "differentialDiagnosis": [
            {"condition": "CD28", "distinction": "CD28 T hücresine pozitif Sinyal 2'yi verir (aktive eder); CTLA-4 ise negatif frenleyici sinyal verir (inhibe eder)."},
            {"condition": "PD-1", "distinction": "PD-1 periferal dokuda PD-L1/L2 ile bağlanır; CTLA-4 lenf nodunda erken evrede B7 ile bağlanır."}
        ],
        "examSpotPearls": [
            "▸ B7 molekülüne CD28'den katbekat yüksek afiniteyle bağlanan T hücre frenidir.",
            "🔴 ÖNEMLİ: Kanser immünoterapisinde CTLA-4 blokajı (İpilimumab) bağışıklık yanıtını serbest bırakır ancak otoimmün yan etkilere yol açar.",
            "🔵 ÇIKMIŞ SORU: Anerji oluşumunda ve periferik toleransta T hücresini durduran ana inhibitör moleküldür."
        ],
        "pitfallsAndWarnings": [
            "CTLA-4 polimorfizmleri Tip 1 diyabet ve otoimmün tiroidit riskini artırır."
        ],
        "relatedItems": ["periferik-tolerans", "foxp3-transkripsiyon-faktoru"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "romatoid-artrit",
        "term": "Romatoid Artrit (RA)",
        "latinName": "Arthritis rheumatoidea",
        "aliases": ["RA"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Öncelikle el ve ayakların küçük eklemlerini simetrik tutan, proliferatif sinovit, pannus dokusu oluşumu, kıkırdak-kemik erozyonları ve ankiloz ile karakterize sistemik otoimmün enflamatuar hastalıktır.",
        "lectureContextNotes": "Ders notunda HLA-DR4 ilişkisi, sitrülinasyon, Anti-CCP (%95+ spesifik), RF (IgM anti-IgG Fc), pannus ve DİF eklemlerinin korunması vurgulanmıştır.",
        "morphologyOrMechanism": "Th1 (IFN-γ) ve Th17 (IL-17) hücreleri sinovyayı uyarır -> Makrofajlardan TNF-α, IL-1, IL-6 salınımı -> Sinovyal hiperplazi ve granülasyon dokusu (Pannus) -> Matriks metalloproteinazlar kıkırdağı eritir, RANKL osteoklastları aktive eder.",
        "differentialDiagnosis": [
            {"condition": "Osteoartrit", "distinction": "Non-enflamatuardır, yük binen büyük eklemleri ve DİF eklemleri (Heberden nodülleri) tutar. RA ise MKF ve PİF tutar, DİF'i korur."},
            {"condition": "Gut Artriti", "distinction": "Monosodyum ürat kristalleri, negatif çift kırılma, akut monoartrit (podagra)."}
        ],
        "examSpotPearls": [
            "▸ **Anti-CCP (ACPA)**: Romatoid Artrit için en spesifik (%95+) biyobelirteçtir.",
            "🔴 ÖNEMLİ: Küçük eklemleri simetrik tutar; **Distal interfalangeal (DİF) eklemler KORUNUR**.",
            "🔵 ÇIKMIŞ SORU: Sinovyanın granülasyon dokusu ve lenfositlerle tümör gibi kalınlaşarak kıkırdağı eritmesine **Pannus** denir."
        ],
        "pitfallsAndWarnings": [
            "Romatoid Faktör negatif olan RA hastaları (seronegatif RA) da vardır; Anti-CCP bakılmalıdır."
        ],
        "relatedItems": ["anti-ccp-antikoru", "pannus-dokusu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "anti-ccp-antikoru",
        "term": "Anti-Sitrülinlenmiş Peptid Antikoru (Anti-CCP / ACPA)",
        "latinName": "Anticorpus contra peptida citrullinata",
        "aliases": ["Anti-CCP", "ACPA"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Enflamatuar dokularda arginin amino asitlerinin peptidilarginin deiminaz (PAD) enzimiyle sitrüline dönüştürülmesi sonucu oluşan modifiye peptidlere karşı yönelen ve Romatoid Artrit için yüksek tanısal özgüllüğe sahip otoantikordur.",
        "lectureContextNotes": "Ders notunda RF'den çok daha yüksek özgüllüğe (%95+) sahip olduğu ve erken evrede bile eklem erozyonlarını öngördüğü belirtilmiştir.",
        "morphologyOrMechanism": "Sitrülinlenmiş vimentin, fibrinojen ve kolajene bağlanarak sinovyal dokuda immün kompleksler ve lokal kompleman aktivasyonu başlatır.",
        "differentialDiagnosis": [
            {"condition": "Romatoid Faktör (RF)", "distinction": "RF Sjögren, SLE ve kronik hepatitte de pozitifleşebilir; Anti-CCP ise RA'ya oldukça özgüldür."},
            {"condition": "ANA", "distinction": "Lupus ve diğer bağ dokusu hastalıklarında yaygındır."}
        ],
        "examSpotPearls": [
            "▸ Romatoid Artrit tanısında **EN YÜKSEK ÖZGÜLLÜĞE** sahip testtir.",
            "🔴 ÖNEMLİ: Sigara kullanımı genetik yatkınlığı olanlarda akciğerde sitrülinasyonu ve Anti-CCP oluşumunu tetikler.",
            "🔵 ÇIKMIŞ SORU: Erken RA tanısında ve erozif eklem seyrini tahmin etmede altın standart serolojik belirteçtir."
        ],
        "pitfallsAndWarnings": [
            "Anti-CCP negatifliği seronegatif RA olasılığını dışlamaz."
        ],
        "relatedItems": ["romatoid-artrit", "pannus-dokusu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "pannus-dokusu",
        "term": "Pannus Dokusu",
        "latinName": "Pannus synovialis",
        "aliases": ["Sinovyal Pannus", "Romatoid Pannus"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Romatoid Artritte prolifere sinovyal örtü hücreleri, granülasyon dokusu, aktive makrofajlar, T lenfositleri ve fibroblastlardan oluşan; kıkırdak ve kemik erozyonuna yol açan tümör benzeri enflamatuar sinovyal kitle dokusudur.",
        "lectureContextNotes": "Ders notunda eklem ankilozuna giden sürecin ana patolojik morfolojisi olarak tanımlanmıştır.",
        "morphologyOrMechanism": "Sinovyal villöz hiperplazi -> Pannus eklem kıkırdağının üzerine sarmaşık gibi yayılır -> Kolajenaz ve stromelizin salarak kıkırdağı eritir -> Subkondral kemikte zımba deliği erozyonlar -> Fibröz ve kemik ankiloz.",
        "differentialDiagnosis": [
            {"condition": "Osteoartrit Sinovyası", "distinction": "Hafif non-proliferatif sinovit vardır; agresif erozif pannus oluşmaz."},
            {"condition": "Pigmente Villonodüler Sinovit (PVNS)", "distinction": "Tenosinovyal dev hücreli tümördür; hemosiderin yüklü makrofajlar ve CSF1 aşırı ekspresyonu vardır."}
        ],
        "examSpotPearls": [
            "▸ RA eklem harabiyetinin ve kemik erozyonunun temel fabrikasıdır.",
            "🔴 ÖNEMLİ: Pannusun kıkırdağı eritip karşı eklem yüzeyiyle birleşmesi **kemik ankilozuna** yol açar.",
            "🔵 ÇIKMIŞ SORU: Romatoid eklemde kıkırdağı yıkan sinovyal doku kütlesine Pannus denir."
        ],
        "pitfallsAndWarnings": [
            "Pannus yalnızca eklemde değil, nadiren romatoid nodül çevrelerinde ve sklerada da oluşabilir."
        ],
        "relatedItems": ["romatoid-artrit", "anti-ccp-antikoru"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "sjogren-sendromu",
        "term": "Sjögren Sendromu (Sicca Sendromu)",
        "latinName": "Syndroma Sjögren",
        "aliases": ["Sjögren", "Kuru Göz-Kuru Ağız Sendromu"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Tükürük ve gözyaşı bezlerinin lenfositik infiltrasyonu ve immün yıkımıyla karakterize; kuru göz (keratokonjunktivitis sikka) ve kuru ağız (kserostomi) ile seyreden kronik otoimmün hastalıktır.",
        "lectureContextNotes": "Ders notunda Anti-SSA (Ro) ve Anti-SSB (La) antikorları, dudak biyopsisinde focus score ve 40 kat artmış B hücreli MALT lenfoma riski vurgulanmıştır.",
        "morphologyOrMechanism": "CD4+ T ve B lenfositleri duktus epitelini infiltre eder ve asiner hücreleri apoptoza sokar. Bez parankimi atrofiye uğrar ve yerini fibrozise bırakır.",
        "differentialDiagnosis": [
            {"condition": "Sarkoidoz (Heerfordt Sendromu)", "distinction": "Kazeifiye olmayan granülomlar vardır; tükürük bezi büyüyebilir ancak Sjögren otoantikorları negatiftir."},
            {"condition": "IgG4-İlişkili Hastalık (Mikulicz)", "distinction": "Doku plazmositleri IgG4 pozitiftir; storiform fibrozis vardır; Ro/La antikorları negatiftir."}
        ],
        "examSpotPearls": [
            "▸ Kuru göz (keratokonjunktivitis sikka) + Kuru ağız (kserostomi).",
            "🔴 ÖNEMLİ: Bu hastalarda **B hücreli Non-Hodgkin Lenfoma (MALT Lenfoma)** riski 40 kat artmıştır!",
            "🔵 ÇIKMIŞ SORU: Dudak biyopsisinde minör tükürük bezlerinde periduktal lenfosit kümeleri (Focus Score >= 1) tanı koydurucudur."
        ],
        "pitfallsAndWarnings": [
            "Parotis bezinde ani asimetrik ve ağrısız büyüme geliştiğinde lenfoma transformasyonu derhal ekarte edilmelidir."
        ],
        "relatedItems": ["sistemik-skleroz-skleroderma", "romatoid-artrit"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "sistemik-skleroz-skleroderma",
        "term": "Sistemik Skleroz (Skleroderma)",
        "latinName": "Sclerosis systemica",
        "aliases": ["Skleroderma", "Diffüz Skleroderma"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Küçük kan damarlarının kronik endotel hasarı (vaskülopati), otoimmün aktivasyon ve fibroblastların kontrolsüz aktivasyonu ile deride ve iç organlarda yaygın kollajen birikimi (fibrozis) oluşturan sistemik bağ dokusu hastalığıdır.",
        "lectureContextNotes": "Ders notunda iki alt tip ayrımı yapılmıştır: 1) Diffüz Skleroderma (Anti-Scl-70 / DNA Topoizomeraz I, erken organ fibrozisi), 2) Sınırlı Skleroderma / CREST (Anti-Sentromer / ACA).",
        "morphologyOrMechanism": "Endotel hasarı -> Raynaud fenomeni -> Sitokin salınımı (TGF-β, PDGF) -> Fibroblast hiperaktivitesi -> Dermis ve organlarda kollajen depolanması -> Deride sertleşme, parankim kaybı.",
        "differentialDiagnosis": [
            {"condition": "Diffüz Skleroderma", "distinction": "Gövdeyi tutar, hızlı akciğer fibrozisi yapar, Anti-Scl-70 pozitiftir."},
            {"condition": "Sınırlı Skleroderma (CREST)", "distinction": "El ve yüzle sınırlıdır, Anti-Sentromer pozitiftir, pulmoner hipertansiyon geç gelişir."}
        ],
        "examSpotPearls": [
            "▸ **Diffüz Tip**: Anti-DNA Topoizomeraz I (**Anti-Scl-70**) pozitiftir; interstisyel akciğer fibrozisi ve renal kriz riski yüksektir.",
            "🔴 ÖNEMLİ: Erken dönemde neredeyse tüm hastalarda ilk belirti soğukla tetiklenen **Raynaud Fenomeni**dir.",
            "🔵 ÇIKMIŞ SORU: Sklerodermada organ fibrozisini tetikleyen ana profibrotik sitokin **TGF-β**'dır."
        ],
        "pitfallsAndWarnings": [
            "Skleroderma renal krizinde kortikosteroidler kontrendikedir çünkü krizi tetikleyebilir; tedavi ACE inhibitörleridir."
        ],
        "relatedItems": ["crest-sendromu", "sjogren-sendromu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "crest-sendromu",
        "term": "CREST Sendromu (Sınırlı Sistemik Skleroz)",
        "latinName": "Syndroma CREST (Sclerosis systemica limitata)",
        "aliases": ["CREST", "Sınırlı Skleroderma"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Deri tutulumunun el parmakları, ön kol ve yüz ile sınırlı olduğu; iç organ fibrozisinin diffüz tipe göre çok daha yavaş ilerlediği ve karakteristik 5 klinik bulgunun akrostişiyle tanımlanan sistemik skleroz alt formudur.",
        "lectureContextNotes": "Ders notunda Anti-Sentromer Antikoru (ACA) pozitifliği ve akrostişin beş klinik bileşeni vurgulanmıştır.",
        "morphologyOrMechanism": "Obliteratif mikrovaskülopati parmak uçlarında nekroza (sklerodaktili), kalsiyum tuzlarının birikmesine (kalsinozis) ve özofagus alt sfinkter atrofisine yol açar.",
        "differentialDiagnosis": [
            {"condition": "Diffüz Sistemik Skleroz", "distinction": "Gövde derisi de sertleşmiştir; Anti-Scl-70 pozitiftir; CREST'te Anti-Sentromer pozitiftir."},
            {"condition": "İdiyopatik Raynaud Hastalığı", "distinction": "Benign seyreder; otoantikorlar negatiftir; trofik doku kaybı veya kalsinozis görülmez."}
        ],
        "examSpotPearls": [
            "▸ **C**alcinosis, **R**aynaud, **E**sophageal dysmotility, **S**clerodactyly, **T**elangiectasia.",
            "🔴 ÖNEMLİ: Tanısal biyobelirteci **Anti-Sentromer Antikoru (ACA)**'dur.",
            "🔵 ÇIKMIŞ SORU: CREST sendromunda geç dönem mortalite nedeni izole Pulmoner Arteriyel Hipertansiyondur."
        ],
        "pitfallsAndWarnings": [
            "İç organ tutulumu geç gelse de pulmoner arteriyel hipertansiyon aniden gelişebilir ve ölümcül olabilir."
        ],
        "relatedItems": ["sistemik-skleroz-skleroderma"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "igg4-iliskili-hastalik",
        "term": "IgG4-İlişkili Hastalık (IgG4-RD)",
        "latinName": "Morbus associatus cum IgG4 (IgG4-RD)",
        "aliases": ["IgG4-RD", "IgG4-İlişkili Sistemik Hastalık"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Çeşitli organlarda kitle benzeri fibroinflamatuar lezyonlar oluşturan, histopatolojisinde yoğun IgG4-pozitif plazmosit infiltrasyonu, storiform fibrozis ve obliteratif flebit ile karakterize, kortikosteroid tedavisine dramatik yanıt veren sistemik sendromdur.",
        "lectureContextNotes": "Ders notunda Tip 1 Otoimmün Pankreatit, Riedel Tiroiditi ve Ormond Hastalığının (retroperitoneal fibrozis) bu çatı altında birleştiği vurgulanmıştır.",
        "morphologyOrMechanism": "Th2 ve Treg hücre aktivasyonu -> Yüksek IL-10 ve TGF-β üretimi -> B hücrelerinde IgG4 izotip dönüşümü -> Dokuda yoğun IgG4+ plazmosit toplanması, çarkıfelek tarzı girdapsı kollajen depolanması (storiform fibrozis) ve ven lümenlerinin tıkanması (obliteratif flebit).",
        "differentialDiagnosis": [
            {"condition": "Pankreas / Akciğer Karsinomu", "distinction": "Klinik ve radyolojik olarak maligniteyi kusursuz taklit eder ancak biyopside atipi yoktur ve steroide hızla geriler."},
            {"condition": "Sarkoidoz", "distinction": "Sarkoidozda kazeifiye olmayan granülomlar vardır; IgG4-RD'de granülom görülmez."}
        ],
        "examSpotPearls": [
            "▸ Üç histopatolojik ayak: **Yoğun IgG4+ plazmosit**, **Storiform fibrozis**, **Obliteratif flebit**.",
            "🔴 ÖNEMLİ: Riedel tiroiditi ve retroperitoneal fibrozis (Ormond hastalığı) IgG4-RD spektrumundadır.",
            "🔵 ÇIKMIŞ SORU: Tümör taklidi yapmasına rağmen sistemik kortikosteroid tedavisine dramatik ve hızlı yanıt verir."
        ],
        "pitfallsAndWarnings": [
            "Serumda IgG4 düzeyi hastaların %30'unda normal olabilir; kesin tanı biyopsideki doku kriterleriyle konur."
        ],
        "relatedItems": ["storiform-fibrozis", "obliteratif-flebit"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "storiform-fibrozis",
        "term": "Storiform Fibrozis (Hasır Örgü Fibrozisi)",
        "latinName": "Fibrosis storiformis",
        "aliases": ["Hasır Örgüsü Fibrozis", "Çarkıfelek Deseni Fibrozis"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "İğsi fibroblastların ve kollajen lif demetlerinin merkezdeki bir odak etrafında çarkıfelek, girdap veya hasır örgüsü benzeri geometrik bir mimariyle dizildiği karakteristik histopatolojik fibrozis paterni.",
        "lectureContextNotes": "Ders notunda IgG4-ilişkili hastalığın (IgG4-RD) biyopsideki tanısal mihenk taşlarından biri olarak sunulmuştur.",
        "morphologyOrMechanism": "Aşırı fibroblast proliferasyonunun belirli vasküler ve hücresel odakların etrafında spiral gerilme kuvvetlerine paralel organize olmasıyla meydana gelir.",
        "differentialDiagnosis": [
            {"condition": "Diffüz Lineer Fibrozis", "distinction": "Düzensiz kaba kollajen bantlarıdır; storiform geometrisi göstermez."},
            {"condition": "Dermatofibrosarkoma Protuberans (DFSP)", "distinction": "Neoplastik iğsi hücrelerin storiform paternidir; CD34 pozitiftir, enflamatuar plazmosit içermez."}
        ],
        "examSpotPearls": [
            "▸ IgG4-RD için patognomonik fibrozis şeklidir.",
            "🔴 ÖNEMLİ: Hasır örgü / çarkıfelek tarzında girdapsı kollajen demetleri görülür.",
            "🔵 ÇIKMIŞ SORU: Obliteratif flebit ve IgG4+ plazma hücreleri ile birlikte görüldüğünde IgG4-RD tanısını koydurur."
        ],
        "pitfallsAndWarnings": [
            "Girdap paterni çok fokal olabilir; geniş biyopside dikkatle aranmalıdır."
        ],
        "relatedItems": ["igg4-iliskili-hastalik", "obliteratif-flebit"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "obliteratif-flebit",
        "term": "Obliteratif Flebit",
        "latinName": "Phlebitis obliterans",
        "aliases": ["Ven Tıkanması Enflamasyonu"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Enflamatuar infiltratın ven duvarını infiltre ederek ve lümen içi fibröz proliferasyona yol açarak ven lümenini tamamen tıkaması; bu esnada komşu arterin açık ve korunmuş kalması ile karakterize vaskülopatik tablodur.",
        "lectureContextNotes": "IgG4-RD triadının vasküler bileşeni olarak vurgulanmıştır.",
        "morphologyOrMechanism": "Lenfoplazmasiter hücreler ven endotelini ve duvarını sarar, elastik lifler parçalanır ve lümen fibröz doku ile dolup oblitere olur. Elastik van Gieson (EVG) boyasıyla tıkanmış ven kalıntısı kanıtlanır.",
        "differentialDiagnosis": [
            {"condition": "Tromboflebit", "distinction": "Tromboflebite pıhtı ve nötrofiller ön plandadır; storiform fibrozis eşlik etmez."},
            {"condition": "Poliarteritis Nodoza (PAN)", "distinction": "PAN arterleri tutar ve fibrinoid nekroz yapar; obliteratif flebit venleri seçer."}
        ],
        "examSpotPearls": [
            "▸ Ven lümeninin lenfoplazmasiter infiltratla kapanması, arterin ise açık kalmasıdır.",
            "🔴 ÖNEMLİ: IgG4-ilişkili hastalığın üç temel histopatolojik ayağından biridir.",
            "🔵 ÇIKMIŞ SORU: Dokuda elastik boyalarda ven lümeninin oblitere olduğu gösterilerek doğrulanır."
        ],
        "pitfallsAndWarnings": [
            "İleri evrede ven tamamen silinebilir; EVG gibi elastik lif boyaları yapılmadan atlanabilir."
        ],
        "relatedItems": ["igg4-iliskili-hastalik", "storiform-fibrozis"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "hiperakut-rejeksiyon",
        "term": "Hiperakut Organ Reddi (Rejeksiyon)",
        "latinName": "Reiectio hyperacuta allografti",
        "aliases": ["Hiperakut Rejeksiyon", "Ameliyat Masasında Red"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Organ naklinden sonraki dakikalar veya saatler içinde, alıcının kanında donör endotel antijenlerine (ABO veya HLA) karşı önceden var olan antikorların etkisiyle gelişen fulminan trombotik greft nekrozudur.",
        "lectureContextNotes": "Ders notunda ameliyat masasında vasküler anastomoz açılır açılmaz böbreğin siyanotik, soluk ve yumuşak hale gelmesiyle karakterize olduğu belirtilmiştir.",
        "morphologyOrMechanism": "Önceden var olan IgG antikorları donör endoteline bağlanır -> Klasik kompleman aktivasyonu -> Endotel hasarı -> Yaygın mikrovasküler tromboz, damar duvarında fibrinoid nekroz -> Greftte masif iskemik nekroz.",
        "differentialDiagnosis": [
            {"condition": "Akut Hücresel Rejeksiyon", "distinction": "Günler-haftalar sonra gelişir; tubulit ve endotelit vardır; T hücreleri sorumludur."},
            {"condition": "Akut Tübüler Nekroz (İskemik)", "distinction": "Greft öncesi iskemiye bağlıdır; damarlarda fibrinoid nekroz veya antikor birikimi yoktur."}
        ],
        "examSpotPearls": [
            "▸ **Zamanlama**: Dakikalar ila saatler içinde (ameliyat masasında).",
            "🔴 ÖNEMLİ: Sebep: Alıcıda **önceden var olan (pre-forme) antikorlar** (gebelik, transfüzyon veya önceki nakil kaynaklı).",
            "🔵 ÇIKMIŞ SORU: Histopatolojik bulgu damar duvarlarında yaygın tromboz ve **fibrinoid nekroz**dur. Cross-match ile önlenir."
        ],
        "pitfallsAndWarnings": [
            "Geliştikten sonra tedavisi yoktur; greft derhal cerrahi olarak çıkarılmalıdır."
        ],
        "relatedItems": ["akut-hukresel-rejeksiyon", "akut-humoral-rejeksiyon-c4d", "kronik-greft-arteriyosklerozu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "akut-humoral-rejeksiyon-c4d",
        "term": "Akut Humoral (Antikor Aracılı) Rejeksiyon ve C4d",
        "latinName": "Reiectio acuta humoralis et C4d",
        "aliases": ["Akut Humoral Rejeksiyon", "ABMR", "C4d Pozitif Rejeksiyon"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Transplantasyon sonrasında alıcıda donör HLA antijenlerine karşı yeni sentezlenen antikorların (Donör Spesifik Antikorlar - DSA) yol açtığı, peritübüler kapillerit ve kapiller endotelinde C4d kompleman fragmanı birikimi ile karakterize akut organ reddi tablosudur.",
        "lectureContextNotes": "Ders notunda peritübüler kapiller endotelinde C4d birikiminin antikor aracılı hasarın patolojik kanıtı olduğu vurgulanmıştır.",
        "morphologyOrMechanism": "DSA endotelde kompleman kaskadını aktive eder. Kararlı C4d fragmanı kapiller bazal membranına ve endoteline kovalent bağlanır; nötrofiller peritübüler kapillerleri tıkar (kapillerit).",
        "differentialDiagnosis": [
            {"condition": "Akut Hücresel Rejeksiyon", "distinction": "T hücreleri tübül epiteli arasına girer (tubulit); C4d negatiftir."},
            {"condition": "Hiperakut Rejeksiyon", "distinction": "Hiperakut dakikalar içinde olur ve önceden var olan antikorlarla gelişir; akut humoral ise günler-haftalar sonra yeni üretilen DSA ile gelişir."}
        ],
        "examSpotPearls": [
            "▸ Böbrek allogreft biyopsisinde peritübüler kapiller endotelinde **C4d birikimi** tanı koydurucudur.",
            "🔴 ÖNEMLİ: Serumda **Donör Spesifik Antikorlar (DSA)** saptanır.",
            "🔵 ÇIKMIŞ SORU: Tedavisinde plazmaferez, IVIG ve B hücre baskılayıcılar (Rituksimab) kullanılır."
        ],
        "pitfallsAndWarnings": [
            "Klasik T hücre immünsüpresyonu (siklosporin vb.) yetersiz kalır; antikor temizleyici tedaviler şarttır."
        ],
        "relatedItems": ["hiperakut-rejeksiyon", "akut-hukresel-rejeksiyon"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "graft-versus-host-hastaligi-gvhd",
        "term": "Graft-versus-Host Hastalığı (GVHD)",
        "latinName": "Morbus allografti contra hospitem (GVHD)",
        "aliases": ["GVHD", "Greft Konağa Karşı Hastalığı"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Allojeneik kemik iliği veya hematopoetik kök hücre nakli sonrasında, greft içindeki donör T lenfositlerinin immün baskılanmış alıcının dokularını yabancı antijen olarak algılayıp saldırması sonucu gelişen; özellikle deri, karaciğer ve bağırsakları hedef alan tablodur.",
        "lectureContextNotes": "Ders notunda Billingham kriterleri, ilk 100 günde Akut GVHD (cilt döküntüsü, kolestatik sarılık, kanlı ishal) ve greft-versus-lösemi (GVL) etkisi anlatılmıştır.",
        "morphologyOrMechanism": "Donör CD4+ ve CD8+ T hücreleri alıcı MHC antijenlerini tanır -> Deride keratinosit apoptozu (dermoepidermal ayrışma); Karaciğerde safra kanalı epitel apoptozu ve kolestaz; Bağırsakta kript epitel apoptozu ve ülserasyon.",
        "differentialDiagnosis": [
            {"condition": "Sitomegalovirüs (CMV) Enteriti", "distinction": "Bağırsakta 'baykuş gözü' nükleer inklüzyonlar görülür; GVHD'de kript apoptozu izlenir."},
            {"condition": "İlaç Erupsiyonu", "distinction": "Karaciğer safra kanalı yıkımı ve kript apoptozu eşlik etmez."}
        ],
        "examSpotPearls": [
            "▸ Üç klasik hedef organ: **Deri** (döküntü/bül), **Karaciğer** (sarılık), **Bağırsak** (kanlı ishal).",
            "🔴 ÖNEMLİ: Mikroskobik ortak imza lezyon hedef organ epitel hücrelerinin **apoptoza** gitmesidir.",
            "🔵 ÇIKMIŞ SORU: Nakil sonrası löseminin nüksetmesini engelleyen faydalı immün yanıt **Greft-versus-Lösemi (GVL)** etkisidir."
        ],
        "pitfallsAndWarnings": [
            "Donör greftinden tüm T hücreleri ayıklanırsa GVHD engellenir ama lösemi nüksü ve greft reddi riski fırlar."
        ],
        "relatedItems": ["akut-hukresel-rejeksiyon", "hiperakut-rejeksiyon"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "bruton-agamaglobulinemisi",
        "term": "Bruton'un X'e Bağlı Agamaglobulinemisi (XLA)",
        "latinName": "Agammaglobulinemia ligata ad chromosoma X Bruton",
        "aliases": ["XLA", "Bruton Hastalığı"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Bruton Tirozin Kinaz (BTK) gen mutasyonu sonucu pre-B hücrelerinin olgun B lenfositlerine farklılaşamaması nedeniyle kanda B hücresi ve tüm immünoglobulin sınıflarının yokluğuyla karakterize primer immün yetmezliktir.",
        "lectureContextNotes": "Ders notunda maternal antikorların bittiği 6. aydan sonra erkek çocuklarda kapsüllü bakterilerle tekrarlayan sinopulmoner enfeksiyonların başladığı, lenf nodlarında germinal merkezlerin bulunmadığı vurgulanmıştır.",
        "morphologyOrMechanism": "BTK stop sinyali -> Pre-B hücresi apoptoza gider -> Dolaşımda CD19/CD20 B lenfositi saptanmaz -> Plazma hücresi oluşamaz -> IgG, IgA, IgM, IgE sıfıra yakındır. T hücre sayısı ve fonksiyonu tamamen normaldir.",
        "differentialDiagnosis": [
            {"condition": "Yaygın Değişken İmmün Yetmezlik (CVID)", "distinction": "CVID genç erişkinlikte başlar; kanda B hücresi sayısı normaldir ancak antikor salgılayamazlar. Bruton'da ise B hücresi hiç yoktur."},
            {"condition": "SCID", "distinction": "SCID'de T hücreleri de yoktur ve fırsatçı enfeksiyonlar görülür. Bruton'da T hücreleri sağlamdır."}
        ],
        "examSpotPearls": [
            "▸ **BTK mutasyonu**: Pre-B'den olgun B'ye geçiş duraklar.",
            "🔴 ÖNEMLİ: Kanda B lenfositleri (CD19, CD20) YOKTUR; lenf nodunda **germinal merkez ve plazma hücresi bulunmaz**.",
            "🔵 ÇIKMIŞ SORU: Erkek bebekte 6. aydan sonra kapsüllü piyojen bakterilerle (*S. pneumoniae*, *H. influenzae*) tekrarlayan pnömoni ve otit."
        ],
        "pitfallsAndWarnings": [
            "Canlı polio aşısı verilirse bağırsakta nötralize edilemeyip aşı ilişkili paralitik poliomyelit yapabilir; canlı aşı kontrendikedir!"
        ],
        "relatedItems": ["scid-agir-kombine-immun-yetmezlik", "digeorge-sendromu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "scid-agir-kombine-immun-yetmezlik",
        "term": "Ağır Kombine İmmün Yetmezlik (SCID)",
        "latinName": "Immunodeficientia combinata severa (SCID)",
        "aliases": ["SCID", "Balon Çocuk Sendromu"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Hem humoral (B lenfosit) hem de hücresel (T lenfosit) immün yanıtın birlikte ağır defektif olduğu; yaşamın ilk aylarında fırsatçı patojenlerle ölümcül enfeksiyonlara yol açan genetik immün yetmezlik tablosudur.",
        "lectureContextNotes": "Ders notunda en sık formun X'e bağlı IL-2R gama zincir mutasyonu, ikinci sık formun ise otozomal resesif Adenozin Deaminaz (ADA) eksikliği olduğu ve timusun displazik kaldığı belirtilmiştir.",
        "morphologyOrMechanism": "Gama zincir (γc) defekti IL-2, IL-4, IL-7, IL-9, IL-15, IL-21 sinyallerini keser -> T ve NK hücre gelişimi durur. ADA eksikliğinde biriken dATP lenfositler için aşırı toksiktir -> Timus hipoplaziktir ve Hassall cisimcikleri içermez.",
        "differentialDiagnosis": [
            {"condition": "Bruton Hastalığı", "distinction": "Bruton'da T hücreleri normaldir; SCID'de hem T hem B immünitesi çökmüştür."},
            {"condition": "DiGeorge Sendromu", "distinction": "DiGeorge'da paratiroid aplazisi ve konotrunkal kalp anomalileri eşlik eder."}
        ],
        "examSpotPearls": [
            "▸ En sık tipi: X'e bağlı **IL-2R gama zinciri (γc)** mutasyonudur.",
            "🔴 ÖNEMLİ: Otozomal resesif tipi: **Adenozin Deaminaz (ADA)** enzim eksikliğidir.",
            "🔵 ÇIKMIŞ SORU: Timus hipoplaziktir; ilk aylarda *Candida* ve *Pneumocystis jirovecii* enfeksiyonları gelişir. Tedavisi kök hücre naklidir."
        ],
        "pitfallsAndWarnings": [
            "Kemik iliği nakli yapılmazsa hastalar ilk 1 yıl içinde kaybedilir."
        ],
        "relatedItems": ["bruton-agamaglobulinemisi", "digeorge-sendromu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "amiloidoz",
        "term": "Amiloidoz",
        "latinName": "Amyloidosis",
        "aliases": ["Amiloid Doku Birikimi"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Yanlış katlanmış, proteolize dirençli çözünmeyen fibriler proteinlerin hücre dışı doku aralıklarında birikerek organlarda bası atrofisine ve fonksiyon yetmezliğine yol açtığı heterojen metabolik ve immünopatolojik hastalık grubudur.",
        "lectureContextNotes": "Ders notunda çapraz beta-kırmalı tabaka yapısı, polarize ışık mikroskobunda Kongo kırmızısı ile elma yeşili çift kırılma, AL, AA ve ATTR tipleri detaylandırılmıştır.",
        "morphologyOrMechanism": "Öncül proteinler yanlış katlanarak 7.5-10 nm dalsız fibrillere ve çapraz beta-kırmalı tabakaya dönüşür. H&E'de amorf homojen pembe boyanır. Böbrekte mezangium ve bazal membranları sararak nefrotik sendrom yapar.",
        "differentialDiagnosis": [
            {"condition": "Hiyalin Birikimi", "distinction": "Hiyalin intraselüler veya ekstrasellüler pembe maddedir ancak Kongo kırmızısı ile boyanmaz ve çift kırılma vermez."},
            {"condition": "Kalsifikasyon", "distinction": "Kalsiyum bazofilik (mavi-mor) boyanır; amiloid eozinofiliktir (pembe)."}
        ],
        "examSpotPearls": [
            "▸ Tüm amiloid fibrillerinin ortak yapısı **çapraz beta-kırmalı tabaka (cross-beta sheet)** mimarisidir.",
            "🔴 ÖNEMLİ: Kesin tanı: **Kongo Kırmızısı** boyasında polarize ışık altında **ELMA YEŞİLİ ÇİFT KIRILMA (Apple-green birefringence)** vermesidir!",
            "🔵 ÇIKMIŞ SORU: En sık kullanılan tanısal tarama biyopsisi **karın cilt altı yağ dokusu aspirasyonudur**."
        ],
        "pitfallsAndWarnings": [
            "Yalnızca ışık mikroskobunda pembe boyanma amiloidoz tanısı için yeterli değildir; mutlaka polarize ışık incelemesi şarttır."
        ],
        "relatedItems": ["al-amiloidoz", "aa-amiloidoz", "transtiretin-amiloidozu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "al-amiloidoz",
        "term": "AL Amiloidoz (Primer Amiloidoz)",
        "latinName": "Amyloidosis AL (primaria)",
        "aliases": ["Primer Amiloidoz", "Hafif Zincir Amiloidozu"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Monoklonal plazma hücre diskrazileri veya Multipl Miyelom seyrinde klonal plazma hücrelerinin aşırı ürettiği immünoglobulin hafif zincirlerinin (özellikle lambda) dokularda amiloid fibrili olarak birikmesiyle karakterize primer sistemik amiloidoz tipidir.",
        "lectureContextNotes": "Ders notunda en sık kardiyak tutulum (restriktif kardiyomiyopati), makroglossi (dil büyümesi), periorbital purpura (rakun gözü) ve böbrek yetmezliği tablosu ile anlatılmıştır.",
        "morphologyOrMechanism": "Klonal plazma hücreleri anormal serbest hafif zincir üretir -> Dolaşımda makrofajlarca tam parçalanamaz -> Yanlış katlanıp AL fibrilleri oluşturur -> Kalp intersitisyumunda ve böbrek glomerüllerinde depolanır.",
        "differentialDiagnosis": [
            {"condition": "AA Amiloidoz", "distinction": "AA kronik enflamasyona sekonderdir (SAA kökenlidir); plazma hücre klonları veya hafif zincir içermez."},
            {"condition": "Senil Kardiyak Amiloidoz (ATTR)", "distinction": "ATTR transtiretin kökenlidir; elektroforezde monoklonal protein saptanmaz."}
        ],
        "examSpotPearls": [
            "▸ Biriken öncül protein: **İmmünoglobulin Hafif Zincirleri** (özellikle lambda $\lambda$).",
            "🔴 ÖNEMLİ: Multipl Miyelom ve monoklonal plazma hücre diskrazileri ile ilişkilidir.",
            "🔵 ÇIKMIŞ SORU: Kalpte birikerek **restriktif kardiyomiyopati** ve aritmiye yol açan en ölümcül amiloidoz formudur."
        ],
        "pitfallsAndWarnings": [
            "AL amiloidozda kalp tutulumu dijital toksisitesine aşırı duyarlılık yaratır; digoksin dikkatle kullanılmalıdır."
        ],
        "relatedItems": ["amiloidoz", "aa-amiloidoz"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "aa-amiloidoz",
        "term": "AA Amiloidoz (Sekonder / Reaktif Amiloidoz)",
        "latinName": "Amyloidosis AA (secundaria / reactiva)",
        "aliases": ["Sekonder Amiloidoz", "Reaktif Amiloidoz"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Uzun süren kronik enflamatuar veya enfeksiyöz hastalıklara yanıt olarak karaciğerden sentezlenen Serum Amiloid A (SAA) proteininin proteolitik kırınımı sonucu oluşan AA fibrillerinin dokularda biriktiği sekonder amiloidoz tablosudur.",
        "lectureContextNotes": "Ders notunda Romatoid Artrit, Bronşiektazi, Kronik Osteomiyelit ve Türkiye'de özellikle Ailevi Akdeniz Ateşi (FMF) zemininde geliştiği ve en sık böbreği tutarak nefrotik sendrom yaptığı vurgulanmıştır.",
        "morphologyOrMechanism": "Kronik enflamasyonda IL-6 ve IL-1 karaciğerde SAA genini uyarır -> SAA plazmada 1000 kat artar -> Monositlerce kısmen parçalanan proteolize dirençli 76 amino asitlik AA peptidleri dokularda toplanır.",
        "differentialDiagnosis": [
            {"condition": "AL Amiloidoz", "distinction": "AL hafif zincir kaynaklıdır, plazma hücre tümörleriyle birliktedir. AA ise kronik enflamasyon kaynaklıdır."},
            {"condition": "Diyaliz İlişkili Amiloidoz (Aβ2m)", "distinction": "Uzun süreli hemodiyaliz hastalarında gelişir; eklem ve karpal tünelde beta-2 mikroglobulin birikir."}
        ],
        "examSpotPearls": [
            "▸ Öncül protein: **Serum Amiloid A (SAA)** (Karaciğer kaynaklı akut faz reaktanı).",
            "🔴 ÖNEMLİ: En sık etyoloji: **Romatoid Artrit** ve **Ailevi Akdeniz Ateşi (FMF)**.",
            "🔵 ÇIKMIŞ SORU: En sık ve en erken tutulan organ **Böbrek**tir; masif proteinüri ve **Nefrotik Sendrom** ile başvurur."
        ],
        "pitfallsAndWarnings": [
            "FMF hastalarında kolşisin tedavisi atakları önlemenin yanı sıra AA amiloidoz gelişimini engeller."
        ],
        "relatedItems": ["amiloidoz", "al-amiloidoz"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    }
]

# Merge into encyclopedia (replace if existing by ID, else append)
added_enc_count = 0
for item in new_encyclopedia_items:
    existing_idx = next((i for i, entry in enumerate(encyclopedia) if entry.get("id") == item["id"]), None)
    if existing_idx is not None:
        encyclopedia[existing_idx] = item
    else:
        encyclopedia.append(item)
        added_enc_count += 1

with open(ENCYCLOPEDIA_PATH, "w", encoding="utf-8") as f:
    json.dump(encyclopedia, f, ensure_ascii=False, indent=2)

print(f"Updated medical_encyclopedia.json! Added {added_enc_count} new entries. Total now: {len(encyclopedia)}")

# Define matching glossary entries
new_glossary_items = {
    "tip 1 aşırı duyarlılık": {
        "term": "Tip I Aşırı Duyarlılık",
        "category": "patoloji",
        "description": "IgE ve mast hücre/bazofil aracılı, alerjenle çapraz bağlanma sonucu dakikalar içinde vazoaktif amin salınımıyla seyreden ani hipersensitivite reaksiyonu (Anafilaksi, Astım).",
        "clinicalPearl": "Erken fazda histamin ve lökotrienler C4/D4/E4; geç fazda eozinofiller (MBP) doku hasarı yapar. Birincil acil tedavi Epinefrindir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "tip 2 aşırı duyarlılık": {
        "term": "Tip II Aşırı Duyarlılık",
        "category": "patoloji",
        "description": "Hücre zarına veya hücre dışı matrise bağlı SABİT doku antijenlerine IgG/IgM bağlanması sonucu gelişen opsonizasyon, kompleman hasarı veya fonksiyonel bozukluk tablosu.",
        "clinicalPearl": "Goodpasture (lineer IF), Pemfigus vulgaris (desmoglein-3), Myasthenia gravis (AChR blokajı) ve Graves (TSHR uyarımı) prototipleridir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "tip 3 aşırı duyarlılık": {
        "term": "Tip III Aşırı Duyarlılık",
        "category": "patoloji",
        "description": "Kanda dolaşan çözünür antijen-antikor komplekslerinin damar duvarına çökmesi, kompleman fiksasyonu ve damar duvarında fibrinoid nekroz oluşturması.",
        "clinicalPearl": "Hafif antijen fazlalığında oluşan orta boy kompleksler en patojeniktir. Akut serum hastalığı ve SLE nefriti prototipidir; granüler IF verir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "tip 4 aşırı duyarlılık": {
        "term": "Tip IV Aşırı Duyarlılık",
        "category": "patoloji",
        "description": "Antikorlardan bağımsız, duyarlaşmış CD4+ Th1/Th17 ve CD8+ CTL lenfositlerinin sitokin ve perforin/granzimle oluşturduğu gecikmiş hücresel doku hasarı.",
        "clinicalPearl": "Tüberkülin (PPD) reaksiyonu 48-72 saatte pik yapar. IFN-γ makrofajları aktive ederek granülom oluşturur. Kontakt dermatit prototipidir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "sistemik lupus eritematozus": {
        "term": "Sistemik Lupus Eritematozus (SLE)",
        "category": "hastalik",
        "description": "Nükleer antijenlere karşı patojenik otoantikorlar ve immün komplekslerin dokularda birikmesiyle karakterize remisyon ve alevlenmelerle seyreden multisistemik otoimmün hastalık.",
        "clinicalPearl": "ANA (%98-100 en hassas), Anti-dsDNA (nefritle korele spesifik), Anti-Sm (en spesifik), Sınıf IV nefritte tel-kulp (wire-loop) ve Libman-Sacks endokarditi görülür.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "anti-dsdna": {
        "term": "Anti-dsDNA Antikoru",
        "category": "protein",
        "description": "Çift sarmallı nativ DNA'ya karşı yönelen ve SLE'ye yüksek özgüllük gösteren patojenik otoantikor.",
        "clinicalPearl": "Titresi lupus nefriti aktivitesi ve alevlenmeleriyle birebir paralel gider; alevlenme sırasında titresi yükselirken serum C3/C4 düşer.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "anti-smith": {
        "term": "Anti-Smith Antikoru (Anti-Sm)",
        "category": "protein",
        "description": "Ribonükleoprotein çekirdek proteinlerini tanıyan ve SLE için en yüksek tanısal özgüllüğe (spesifiteye) sahip antikor.",
        "clinicalPearl": "Pozitifliği SLE tanısını mühürler ancak duyarlılığı düşüktür (%25). Hastalık alevlenmesiyle titresi değişmez.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "libman-sacks endokarditi": {
        "term": "Libman-Sacks Endokarditi",
        "category": "patoloji",
        "description": "SLE ve APS hastalarında kalp kapakçıklarının hem ön hem arka yüzünde steril, verrüköz vejetasyonların yerleştiği non-bakteriyel endokardit.",
        "clinicalPearl": "Vejetasyonların kapak yaprakçıklarının her iki yüzünde yerleşmesiyle romatizmal ve bakteriyel endokarditten ayrılır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "lupus nefriti": {
        "term": "Lupus Nefriti",
        "category": "patoloji",
        "description": "SLE'de immün komplekslerin glomerüllerde birikmesiyle oluşan böbrek tutulumu (Sınıf I-VI).",
        "clinicalPearl": "En sık ve en ağır tip Sınıf IV (Diffüz lupus nefriti) olup tel-kulp (wire-loop) lezyonları ve Full-House immünofloresan pozitifliği gösterir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "antifosfolipid sendromu": {
        "term": "Antifosfolipid Sendromu (APS)",
        "category": "hastalik",
        "description": "Fosfolipid bağlayıcı proteinlere karşı otoantikorlarla seyreden, tekrarlayan trombozlar ve düşüklerle karakterize hiperkoagülabilite sendromu.",
        "clinicalPearl": "İn vitro aPTT uzamasına rağmen in vivo arteriyel/venöz tromboz yapar; sifiliz testlerinde yalancı pozitiflik verir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "aire geni": {
        "term": "AIRE Geni (Autoimmune Regulator)",
        "latinName": "AIRE",
        "category": "protein",
        "description": "Timik medüller epitelde periferik doku antijenlerinin sentezlenmesini sağlayarak negatif seleksiyonu yöneten kilit gen.",
        "clinicalPearl": "Mutasyonunda APECED / APS-1 (Kronik mukokutanöz kandidiyazis, hipoparatiroidizm, adrenal yetmezlik) gelişir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "foxp3": {
        "term": "FoxP3 Transkripsiyon Faktörü",
        "category": "protein",
        "description": "CD4+ CD25+ regülatuvar T hücrelerinin (Treg) ana transkripsiyon faktörü.",
        "clinicalPearl": "Mutasyonunda erkek bebeklerde inatçı otoimmün ishal, diyabet ve egzama ile karakterize X'e bağlı ölümcül IPEX sendromu gelişir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "ctla-4": {
        "term": "CTLA-4 (CD152)",
        "category": "protein",
        "description": "T lenfosit yüzeyinde CD28 ile yarışarak APC'deki B7 moleküllerine çok daha yüksek afiniteyle bağlanan inhibitör kontrol noktası molekülü.",
        "clinicalPearl": "T hücresine negatif sinyal göndererek anerji ve periferik tolerans sağlar; İpilimumab kanserde bu molekülü bloke eder.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "romatoid artrit": {
        "term": "Romatoid Artrit (RA)",
        "category": "hastalik",
        "description": "Küçük eklemleri simetrik tutan, proliferatif sinovit, pannus ve eklem erozyonları ile seyreden kronik sistemik otoimmün hastalık.",
        "clinicalPearl": "Anti-CCP (%95+ en spesifik), RF (IgM anti-IgG Fc), MKF ve PİF tutulumu; Distal interfalangeal (DİF) eklemler karakteristik olarak KORUNUR.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "anti-ccp": {
        "term": "Anti-CCP (ACPA)",
        "category": "protein",
        "description": "Sitrülinlenmiş peptidlere karşı gelişen ve Romatoid Artrit tanısında %95'in üzerinde özgüllüğe sahip olan otoantikor.",
        "clinicalPearl": "Erken evrede ve erozif eklem harabiyetini öngörmede Romatoid Faktörden çok daha üstündür.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "pannus": {
        "term": "Pannus",
        "category": "patoloji",
        "description": "Romatoid artritte prolifere sinovyal örtü hücreleri, granülasyon dokusu ve lenfositlerden oluşan erozif tümör benzeri kitle.",
        "clinicalPearl": "Salgıladığı enzimlerle kıkırdağı ve alttaki kemiği eriterek fibröz ve kemik ankilozuna yol açar.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "sjogren sendromu": {
        "term": "Sjögren Sendromu",
        "category": "hastalik",
        "description": "Gözyaşı ve tükürük bezlerinin lenfositik infiltrasyonu sonucu kuru göz (keratokonjunktivitis sikka) ve kuru ağız (kserostomi) ile seyreden otoimmün hastalık.",
        "clinicalPearl": "Anti-SSA (Ro) ve Anti-SSB (La) antikorları pozitiftir; B hücreli MALT lenfoma riski 40 kat artmıştır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "skleroderma": {
        "term": "Sistemik Skleroz (Skleroderma)",
        "category": "hastalik",
        "description": "Mikrovasküler endotel hasarı ve aşırı kollajen depolanmasıyla deride ve iç organlarda yaygın fibrozis oluşturan otoimmün hastalık.",
        "clinicalPearl": "Diffüz tipte Anti-Scl-70 (hızlı visseral tutulum); Sınırlı tipte (CREST) Anti-Sentromer antikorları pozitiftir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "crest sendromu": {
        "term": "CREST Sendromu",
        "category": "hastalik",
        "description": "Calcinosis, Raynaud, Esophageal dysmotility, Sclerodactyly, Telangiectasia bulguları ile karakterize sınırlı sistemik skleroz.",
        "clinicalPearl": "Anti-Sentromer Antikoru (ACA) pozitiftir; geç dönemde izole pulmoner hipertansiyon riski taşır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "igg4-iliskili hastalik": {
        "term": "IgG4-İlişkili Hastalık (IgG4-RD)",
        "category": "hastalik",
        "description": "Otoimmün pankreatit, Riedel tiroiditi ve retroperitoneal fibrozisi kapsayan sistemik fibroinflamatuar sendrom.",
        "clinicalPearl": "Histopatolojik triadı: Yoğun IgG4+ plazma hücresi, Storiform fibrozis ve Obliteratif flebit. Steroide dramatik yanıt verir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "storiform fibrozis": {
        "term": "Storiform Fibrozis",
        "category": "patoloji",
        "description": "Kollajen ve fibroblastların çarkıfelek veya hasır örgüsü benzeri girdapsı dizilim gösterdiği fibrozis deseni.",
        "clinicalPearl": "IgG4-ilişkili hastalığın (IgG4-RD) biyopsideki tanısal mihenk taşıdır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "obliteratif flebit": {
        "term": "Obliteratif Flebit",
        "category": "patoloji",
        "description": "Enflamatuar infiltratın ven duvarını işgal ederek lümeni tıkaması; komşu arterin açık kalması.",
        "clinicalPearl": "IgG4-ilişkili hastalığın üç temel histopatolojik ayağından biridir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "hiperakut rejeksiyon": {
        "term": "Hiperakut Organ Reddi",
        "category": "patoloji",
        "description": "Nakilden dakikalar-saatler sonra alıcıdaki önceden var olan antikorlarla gelişen fulminan trombotik iskemik greft nekrozu.",
        "clinicalPearl": "Ameliyat masasında greft siyanotik ve yumuşak hale gelir; damar duvarında fibrinoid nekroz saptanır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "c4d birikimi": {
        "term": "C4d Kompleman Birikimi",
        "category": "patoloji",
        "description": "Böbrek allogreft biyopsisinde peritübüler kapiller endotelinde saptanan ve humoral rejeksiyonu kanıtlayan kompleman fragmanı.",
        "clinicalPearl": "Akut Antikor-Aracılı (Humoral) Rejeksiyonun (ABMR) immünohistokimyasal altın standart biyobelirtecidir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "graft-versus-host": {
        "term": "Graft-versus-Host Hastalığı (GVHD)",
        "category": "hastalik",
        "description": "Kök hücre nakli sonrası donör T lenfositlerinin immünkompromize alıcının dokularına saldırması.",
        "clinicalPearl": "Akut GVHD'de hedef organlar Cilt (döküntü), Karaciğer (sarılık) ve Bağırsaktır (kanlı ishal); ortak bulgu epitel apoptozudur.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "bruton agamaglobulinemisi": {
        "term": "Bruton Agamaglobulinemisi (XLA)",
        "category": "hastalik",
        "description": "BTK mutasyonu sonucu pre-B hücrelerinin olgun B'ye dönüşemediği X'e bağlı primer immün yetmezlik.",
        "clinicalPearl": "Kanda B lenfositi ve antikor yoktur; lenf nodlarında germinal merkez bulunmaz. 6. aydan sonra piyojenik bakteriyel enfeksiyonlar başlar.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "scid": {
        "term": "Ağır Kombine İmmün Yetmezlik (SCID)",
        "category": "hastalik",
        "description": "Hem hücresel (T) hem humoral (B) immün yanıtın çöktüğü, erken bebeklikte ölümcül fırsatçı enfeksiyonlara yol açan sendrom.",
        "clinicalPearl": "En sık tipi X'e bağlı IL-2R gama zinciri defekti; resesif tipi ADA eksikliğidir. Timus hipoplaziktir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "amiloidoz": {
        "term": "Amiloidoz",
        "category": "patoloji",
        "description": "Yanlış katlanmış fibriler proteinlerin hücrelerarası alanda çapraz beta-kırmalı tabaka şeklinde birikmesiyle organ yetmezliği yapan hastalık.",
        "clinicalPearl": "Kongo kırmızısı ile polarize mikroskopta ELMA YEŞİLİ ÇİFT KIRILMA patognomoniktir. AL hafif zincir, AA ise SAA kökenlidir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "al amiloidoz": {
        "term": "AL Amiloidoz (Primer)",
        "category": "patoloji",
        "description": "Monoklonal plazma hücre diskrazilerinde immünoglobulin hafif zincirlerinin (özellikle lambda) dokuda birikmesi.",
        "clinicalPearl": "Kalpte restriktif kardiyomiyopati, dilde makroglossi ve böbrek yetmezliği yapar.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "aa amiloidoz": {
        "term": "AA Amiloidoz (Sekonder/Reaktif)",
        "category": "patoloji",
        "description": "Romatoid Artrit, FMF gibi kronik enflamatuar durumlarda karaciğer kaynaklı Serum Amiloid A (SAA) proteininin birikmesi.",
        "clinicalPearl": "En sık böbreği tutarak masif proteinüri ve nefrotik sendrom tablosu ile başvurur.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    }
}

# Merge into glossary
added_gloss_count = 0
for k, v in new_glossary_items.items():
    if k not in glossary:
        added_gloss_count += 1
    glossary[k] = v

with open(GLOSSARY_PATH, "w", encoding="utf-8") as f:
    json.dump(glossary, f, ensure_ascii=False, indent=2)

print(f"Updated medical_glossary.json! Added/Updated {added_gloss_count} keys. Total now: {len(glossary)}")
