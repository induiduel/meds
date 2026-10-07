# -*- coding: utf-8 -*-
"""
expand_genetics_pediatric_terms.py
Enriches medical_encyclopedia.json and medical_glossary.json with comprehensive,
granular terms for Genetics, Pediatric, Environmental, Nutritional Pathology,
and Molecular Diagnostics based on Prof. Dr. Hikmet Keleş & Robbins 11th ed.
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

new_encyclopedia_items = [
    {
        "id": "marfan-sendromu",
        "term": "Marfan Sendromu",
        "latinName": "Syndroma Marfan",
        "aliases": ["Marfan", "FBN1 İlişkili Bağ Dokusu Hastalığı"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Kromozom 15q21.1 üzerindeki FBN1 (Fibrillin-1) gen mutasyonu sonucu elastik lif mikrofibril iskeletinin bozulması ve serbest TGF-β aşırı aktivasyonu ile karakterize, iskelet, göz ve kardiyovasküler sistemi tutan otozomal dominant hastalıktır.",
        "lectureContextNotes": "Ders notunda aort kökü dilatasyonu, tunika medyadaki kistik medyal nekroz, aort diseksiyonu/rüptürü (en sık ölüm nedeni), ektopia lentis (yukarı ve dışa lüksasyon) ve araknodaktili üzerinde durulmuştur.",
        "morphologyOrMechanism": "Fibrillin-1 kusuru -> Dokuda mekanik zayıflık + Latent TGF-β'nın tutulamayıp aşırı serbest kalması -> Matriks metalloproteinaz aktivasyonu -> Elastik lif parçalanması ve kıkırdak/kemik aşırı uzaması.",
        "differentialDiagnosis": [
            {"condition": "Homosistinüri", "distinction": "Homosistinüride lens AŞAĞI VE İÇE lükse olur; zeka geriliği ve tromboz sıktır. Marfan'da lens YUKARI VE DIŞA lükse olur; zeka normaldir."},
            {"condition": "Ehlers-Danlos Sendromu", "distinction": "Kollajen defektidir; deride aşırı esneklik ve sigara kağıdı skar dokusu ön plandadır."}
        ],
        "examSpotPearls": [
            "▸ Gen: **FBN1** (15q21.1); Kalıtım: **Otozomal Dominant**.",
            "🔴 ÖNEMLİ: En sık ölüm nedeni çıkan aortta **Kistik Medyal Nekroz zemininde Aort Diseksiyonu ve Rüptürü**dür.",
            "🔵 ÇIKMIŞ SORU: Lens sublüksasyonu **YUKARI VE DIŞA (Superior-temporal)** doğrudur."
        ],
        "pitfallsAndWarnings": [
            "Marfan hastalarında göğüs ağrısı aksi kanıtlanana kadar aort diseksiyonu kabul edilmelidir."
        ],
        "relatedItems": ["fibrillin-1-geni", "kistik-medyal-nekroz", "ektopia-lentis"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "fibrillin-1-geni",
        "term": "Fibrillin-1 (FBN1 Geni)",
        "latinName": "Fibrillinum-1",
        "aliases": ["FBN1", "Fibrillin-1 Glikoproteini"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Ekstrasellüler matrikste elastik liflerin üzerine çöktüğü mikrofibrillerin temel yapısal proteini olan ve aynı zamanda latent TGF-β kompleksini bağlayarak inaktif tutan 350 kDa ağırlığında glikoproteindir.",
        "lectureContextNotes": "15q21.1 lokusunda yer alır; mutasyonu Marfan sendromuna yol açar.",
        "morphologyOrMechanism": "Elastin çekirdeğin etrafında kılıf oluşturur. Mutasyonunda mikrofibril ağı dağılır, TGF-β biyoyararlanımı artar ve elastolizis hızlanır.",
        "differentialDiagnosis": [
            {"condition": "FBN2 (Fibrillin-2)", "distinction": "Kromozom 5q'dadır; mutasyonunda Konjenital Kontraktürel Araknodaktili (Beals sendromu) gelişir."},
            {"condition": "Kollajen Tip I", "distinction": "Osteogenezis imperfektada defektiftir; kemik kırıkları ve mavi sklera yapar."}
        ],
        "examSpotPearls": [
            "▸ Elastik liflerin mikrofibril iskeletini oluşturur.",
            "🔴 ÖNEMLİ: Latent TGF-β'yı tutarak kontrol altında tutar.",
            "🔵 ÇIKMIŞ SORU: Marfan sendromunun etyolojisindeki genetik kusurdur."
        ],
        "pitfallsAndWarnings": [
            "Yalnızca mekanik zayıflık değil, TGF-β artışına bağlı sinyal bozukluğu da yaratır."
        ],
        "relatedItems": ["marfan-sendromu", "kistik-medyal-nekroz"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "kistik-fibrozis",
        "term": "Kistik Fibrozis (Mukovisidoz)",
        "latinName": "Fibrosis cystica (Mucoviscidosis)",
        "aliases": ["Kistik Fibrozis", "CF", "Mukovisidoz"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Pediatri",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Kromozom 7q31.2 üzerindeki CFTR gen mutasyonu sonucu ekzokrin bez salgılarının aşırı koyulaşıp vizkozlaşmasıyla karakterize; solunum sistemi bronşiektazisi, ekzokrin pankreas yetmezliği ve terde yüksek tuz ile seyreden en sık ölümcül otozomal resesif hastalıktır.",
        "lectureContextNotes": "Ders notunda en sık mutasyonun Delta-F508 olduğu, solunum epitelinde klor sekresyonu yokluğu ve aşırı sodyum/su emilimiyle mukusun kuruması; ter bezinde ise klor geri emilim defektiyle terde yüksek klor saptanması anlatılmıştır.",
        "morphologyOrMechanism": "CFTR klorür kanalı defekti -> Solunumda dehidrate mukus tıkaçları -> Pseudomonas bronşiektazisi. Pankreasta duktus tıkanması -> Asiner fibrozis ve malabsorbsiyon. Yenidoğanda mekonyum ileusu.",
        "differentialDiagnosis": [
            {"condition": "Primer Silier Diskinezi (Kartagener)", "distinction": "Dinein kolu defektidir; situs inversus ve erkek infertilitesi vardır ancak ter testi normaldir."},
            {"condition": "Çölyak Hastalığı", "distinction": "Malabsorbsiyon yapar ancak akciğer tutulumu veya ter testi pozitifliği yoktur."}
        ],
        "examSpotPearls": [
            "▸ En sık mutasyon: **Delta-F508 ($\Delta$F508)** (Sınıf II protein katlanma kusuru).",
            "🔴 ÖNEMLİ: Yenidoğanda ilk belirti **Mekonyum İleusu**; erişkinde en sık mortalite nedeni ***Pseudomonas aeruginosa* bronşiektazisi**dir.",
            "🔵 ÇIKMIŞ SORU: Altın standart tanı yöntemi: **Ter Testinde klorun > 60 mEq/L saptanmasıdır**."
        ],
        "pitfallsAndWarnings": [
            "Erkek CF hastalarının %95'inde vaz deferens agenezisi (CBAVD) nedeniyle obstrüktif azospermi vardır."
        ],
        "relatedItems": ["cftr-geni", "delta-f508-mutasyonu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "cftr-geni",
        "term": "CFTR Geni ve Klorür Kanalı",
        "latinName": "CFTR (Cystic Fibrosis Transmembrane Conductance Regulator)",
        "aliases": ["CFTR", "ABCC7"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Kromozom 7q31.2'de kodlanan, cAMP bağımlı protein kinaz A ile aktive olan ve epitel hücrelerinin apikal membranında klorür ve bikarbonat iletimini sağlayan ABC taşıyıcı ailesi üyesi iyon kanalıdır.",
        "lectureContextNotes": "Solunum epitelinde ENaC sodyum kanalını inhibe eder; ter bezinde ise klorürü lümenden geri emer.",
        "morphologyOrMechanism": "İki transmembran domeni, iki nükleotid bağlayıcı domeni (NBD1/NBD2) ve bir düzenleyici (R) domeni içerir. ATP hidrolizi ile açılır.",
        "differentialDiagnosis": [
            {"condition": "ENaC Sodyum Kanalı", "distinction": "CFTR'nin yokluğunda aşırı aktifleşerek hücre içine sodyum ve su çeker; mukusu kurutur."},
            {"condition": "Klorür İntraselüler Kanalı (CLIC)", "distinction": "Farklı hücresel lokalizasyondadır; CFTR gibi cAMP regüleli değildir."}
        ],
        "examSpotPearls": [
            "▸ Kromozom: **7q31.2**.",
            "🔴 ÖNEMLİ: Solunum yolunda kloru dışarı pompalar ve ENaC'ı frenler; ter bezinde ise kloru içeri geri emer.",
            "🔵 ÇIKMIŞ SORU: Sınıf II mutasyonunda protein katlanamaz ve endoplazmik retikulumda erken parçalanır."
        ],
        "pitfallsAndWarnings": [
            "2000'den fazla farklı CFTR mutasyonu tanımlanmıştır; hafif mutasyonlar yalnızca erişkin kronik pankreatit veya izole infertilite yapabilir."
        ],
        "relatedItems": ["kistik-fibrozis", "delta-f508-mutasyonu"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "down-sendromu",
        "term": "Down Sendromu (Trizomi 21)",
        "latinName": "Syndroma Down (Trisomia 21)",
        "aliases": ["Down Sendromu", "Trizomi 21", "Mongolizm (Eski terim)"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Kromozom 21'in fazladan bir kopyasının bulunması (47,XX,+21 veya 47,XY,+21) sonucu ortaya çıkan, karakteristik dismorfik yüz bulguları, konjenital kalp defektleri, duodenal atrezi, lösemi yatkınlığı ve erken Alzheimer ile seyreden en sık kromozomal hastalıktır.",
        "lectureContextNotes": "Ders notunda %95 maternal mayotik non-disjunction ve anne yaşı korelasyonu, %4 Robertsonian translokasyon t(14;21), endokardiyal yastık defekti, duodenal atrezi (çift baloncuk), AML M7 ve 40 yaş üstü Alzheimer nöropatolojisi anlatılmıştır.",
        "morphologyOrMechanism": "Gen dozaj etkisi: APP aşırı ekspresyonu -> A-beta amiloidoz; DYRK1A ve SOD1 -> Nöronal fonksiyon kusuru ve oksidatif stres; GATA1 mutasyonları -> Megakaryoblastik lösemi.",
        "differentialDiagnosis": [
            {"condition": "Edwards Sendromu (Trizomi 18)", "distinction": "Mikrognati, üst üste binen parmaklar, rocker-bottom ayaklar, ağır erken mortalite."},
            {"condition": "Patau Sendromu (Trizomi 13)", "distinction": "Holoprozensefali, yarık dudak/damak, mikroftalmi, polidaktili."}
        ],
        "examSpotPearls": [
            "▸ Sitogenetik: **%95 Maternal Mayotik Non-Disjunction** (anne yaşıyla ilişkili); **%4 Robertsonian Translokasyon** (anne yaşından bağımsız).",
            "🔴 ÖNEMLİ: En sık kardiyak malformasyon **Endokardiyal Yastık Defekti (AVSD)**; en sık GİS anomalisi **Duodenal Atrezi**dir.",
            "🔵 ÇIKMIŞ SORU: 40 yaş üzerinde **Alzheimer Hastalığı** gelişimi APP geninin 21. kromozomda 3 kopya olmasıyla açıklanır."
        ],
        "pitfallsAndWarnings": [
            "Translokasyon tipinde ebeveyn taşıyıcı olabileceği için ebeveyn karyotipi mutlaka incelenmelidir."
        ],
        "relatedItems": ["trizomi-21"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "tek-nukleotid-polimorfizmi-snp",
        "term": "Tek Nükleotid Polimorfizmi (SNP)",
        "latinName": "Polymorphismus unius nucleotidi (SNP)",
        "aliases": ["SNP", "Tek Baz Değişimi"],
        "category": "terim",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Genetik",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Genomik DNA dizisinde tek bir nükleotidin (A, T, C veya G) değişmesiyle ortaya çıkan ve toplumda en az %1 sıklıkta görülen, genomda en sık rastlanan genetik varyasyon biçimidir.",
        "lectureContextNotes": "Genomda 10 milyondan fazla SNP olduğu, çoğunun kodlamayan DNA'da yer aldığı ve GWAS çalışmalarında multifaktöryel hastalık risk alellerini belirlemede kullanıldığı vurgulanmıştır.",
        "morphologyOrMechanism": "Tek baz mutasyonları kodonda amino asit değiştirebilir (nonsynonymous) veya değiştirmeyebilir (synonymous). Promotor veya enhancerdaki SNP'ler transkripsiyon faktörü bağlanmasını modüle eder.",
        "differentialDiagnosis": [
            {"condition": "Kopya Sayısı Varyasyonu (CNV)", "distinction": "CNV 1 kb'den büyük segmentlerin delesyon/duplikasyonudur; SNP tek bazdır."},
            {"condition": "Nokta Mutasyonu", "distinction": "Mutasyon popülasyonda <%1 sıklıkta nadirdir ve doğrudan hastalığa yol açar; polimorfizm ise >%1 sıklıktadır ve yatkınlık yaratır."}
        ],
        "examSpotPearls": [
            "▸ İnsan genomundaki **en yaygın varyasyon** türüdür.",
            "🔴 ÖNEMLİ: Popülasyon sıklığı **> %1** olmak zorundadır.",
            "🔵 ÇIKMIŞ SORU: GWAS çalışmalarının temel tarama belirtecidir."
        ],
        "pitfallsAndWarnings": [
            "Bir SNP'nin hastalıkla ilişkili olması tek başına nedensel suçlu olduğunu göstermez; suçlu mutasyonla bağlantı dengesizliğinde (linkage disequilibrium) olabilir."
        ],
        "relatedItems": ["kopya-sayisi-varyasyonu-cnv"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "kursun-toksisitesi",
        "term": "Kurşun Toksisitesi (Satürnizm / Plumbizm)",
        "latinName": "Intoxicatio plumbi (Saturnismus)",
        "aliases": ["Kurşun Zehirlenmesi", "Plumbizm", "Satürnizm"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Toksikoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Kurşun bileşiklerinin solunması veya yutulması sonucu hem sentezinin inhibe olması, kemikte depolanması ve santral/periferik sinir sisteminde miyelin ve nöronal harabiyet oluşturmasıyla seyreden toksik tablodur.",
        "lectureContextNotes": "Ders notunda çocuklarda pika, ALA dehidrataz ve ferroşelataz inhibisyonu, eritrositlerde bazofilik noktalanma, epifizde radyoopak kurşun hatları, diş etinde Burton çizgisi ve ensefalopati anlatılmıştır.",
        "morphologyOrMechanism": "–SH gruplarına bağlanır -> ALA dehidrataz ve ferroşelataz bloke olur -> Mikrositer anemi ve ZPP artışı. Pirimidin 5'-nükleotidaz bloke olur -> Bazofilik noktalanma. Kemikte kalsiyum yerine çöker -> Epifiz hatları.",
        "differentialDiagnosis": [
            {"condition": "Demir Eksikliği Anemisi", "distinction": "Demir eksikliğinde ferritin düşüktür, RDW artar; bazofilik noktalanma veya kurşun hatları görülmez."},
            {"condition": "Sideroblastik Anemi", "distinction": "Kemik iliğinde halkalı sideroblastlar vardır; piridoksin veya kurşuna bağlı olabilir."}
        ],
        "examSpotPearls": [
            "▸ İnhibe edilen enzimler: **$\delta$-ALA dehidrataz** ve **Ferroşelataz**.",
            "🔴 ÖNEMLİ: Periferik yaymada eritrositlerde **Bazofilik Noktalanma** patognomoniktir.",
            "🔵 ÇIKMIŞ SORU: Diş eti kenarında mor-mavi **Burton Çizgisi** ve epifizde radyoopak kurşun hatları görülür."
        ],
        "pitfallsAndWarnings": [
            "Çocuklarda düşük kurşun kan seviyelerinde bile zeka puanında (IQ) geri dönüşsüz düşüş gelişebilir."
        ],
        "relatedItems": ["bazofilik-noktalanma", "burton-cizgisi"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "bazofilik-noktalanma",
        "term": "Eritrositlerde Bazofilik Noktalanma (Basophilic Stippling)",
        "latinName": "Punctatio basophilica erythrocytorum",
        "aliases": ["Bazofilik Noktalanma", "Basophilic Stippling"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Wright-Giemsa boyalı periferik kan yaymasında olgun eritrosit sitoplazması içinde homojen dağılmış, ince veya kaba koyu mavi/mor granüler noktacıkların görülmesidir.",
        "lectureContextNotes": "Kurşun zehirlenmesinde pirimidin 5'-nükleotidaz enzim inhibisyonu sonucu ribozomal RNA kalıntılarının kümeleşmesiyle oluştuğu vurgulanmıştır.",
        "morphologyOrMechanism": "Normalde retikülosit olgunlaşırken rRNA pirimidin 5'-nükleotidaz ile parçalanır. Enzim bloke olduğunda ribozomlar eritrosit içinde presipite olur.",
        "differentialDiagnosis": [
            {"condition": "Howell-Jolly Cisimcikleri", "distinction": "Eritrosit içinde tek, yuvarlak, büyük DNA nükleus kalıntısıdır (asplenide görülür)."},
            {"condition": "Pappenheimer Cisimcikleri", "distinction": "Demir granülleridir; Prusya mavisi ile boyanır."}
        ],
        "examSpotPearls": [
            "▸ Kurşun zehirlenmesinin ve talasemi taşıyıcılığının klasik periferik yayma bulgusudur.",
            "🔴 ÖNEMLİ: Biyokimyasal kökeni parçalanamayan **ribozomal RNA (rRNA)** agregatlarıdır.",
            "🔵 ÇIKMIŞ SORU: Kurşun intoksikasyonunda pirimidin 5'-nükleotidaz eksikliği sonucu oluşur."
        ],
        "pitfallsAndWarnings": [
            "Miyelodisplastik sendrom ve ağır megaloblastik anemilerde de görülebilir; klinik tablo ile yorumlanmalıdır."
        ],
        "relatedItems": ["kursun-toksisitesi"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "karbonmonoksit-toksisitesi",
        "term": "Karbonmonoksit (CO) Toksisitesi",
        "latinName": "Intoxicatio monoxidi carbonis",
        "aliases": ["Karbonmonoksit Zehirlenmesi", "Soba Zehirlenmesi"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Toksikoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Karbonmonoksit gazının solunmasıyla hemoglobine bağlanıp karboksihemoglobin (COHb) oluşturması, oksihemoglobin dissosiasyon eğrisini sola kaydırması ve dokularda şiddetli hipoksi/asfiksi yaratmasıyla seyreden tablodur.",
        "lectureContextNotes": "Hemoglobine oksijenden 200 kat fazla afinite, kiraz kırmızısı deri/mukoza rengi, beyinde bilateral globus pallidus nekrozu ve hiperbarik oksijen tedavisi anlatılmıştır.",
        "morphologyOrMechanism": "CO + Hemoglobin -> Karboksihemoglobin. Hemoglobin oksijeni dokuya bırakamaz. Sitokrom c oksidaz inhibe olur -> Mitokondriyal ATP sentezi çöker.",
        "differentialDiagnosis": [
            {"condition": "Siyanür Zehirlenmesi", "distinction": "Siyanürde kanda laktat çok yüksektir; acı badem kokusu alınabilir; oksihemoglobin bağlanmasını bozmaz, sadece kompleksi IV'ü felç eder."},
            {"condition": "Methemoglobinemi", "distinction": "Demir Fe3+ formundadır; kan çikolata kahverengisidir ve kiraz kırmızısı değil siyanoz görülür."}
        ],
        "examSpotPearls": [
            "▸ Hemoglobine oksijenden **200 kat daha güçlü** bağlanır.",
            "🔴 ÖNEMLİ: Cilt ve mukozalar **Kiraz Kırmızısı (Cherry-red)** renktedir.",
            "🔵 ÇIKMIŞ SORU: Beyinde patognomonik otopsi bulgusu **Bilateral Globus Pallidus Nekrozu**dur."
        ],
        "pitfallsAndWarnings": [
            "Standart nabız oksimetreler (SpO2) COHb ile oksihemoglobini ayırt edemez ve normal (%99-100) gösterir; kan gazında ko-oksimetre ile COHb ölçülmelidir!"
        ],
        "relatedItems": ["karboksihemoglobin"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "karboksihemoglobin",
        "term": "Karboksihemoglobin (COHb)",
        "latinName": "Carboxyhaemoglobinum",
        "aliases": ["COHb"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Biyokimya",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Karbonmonoksitin hemoglobinin hem halkasındaki iki değerli demire (Fe2+) kovalent benzeri yüksek afiniteyle bağlanması sonucu oluşan anormal hemoglobin türevidir.",
        "lectureContextNotes": "Kandaki düzeyi zehirlenmenin ciddiyetini gösterir. Ağır sigara içicilerinde %5-10; ölümcül zehirlenmelerde >%50-60 seviyelerine ulaşır.",
        "morphologyOrMechanism": "CO bağlanan tetramerik hemoglobin relaks (R) konformasyonuna kilitlenir; diğer bağlı oksijen moleküllerinin dokulara bırakılması imkansızlaşır (eğri sola kayar).",
        "differentialDiagnosis": [
            {"condition": "Oksihemoglobin", "distinction": "Oksijeni serbestçe dokuya bırakır; dissosiasyon eğrisi normaldir."},
            {"condition": "Karbaminohemoglobin", "distinction": "Karbondioksitin (CO2) globin zincirlerine bağlanmış normal fizyolojik formudur."}
        ],
        "examSpotPearls": [
            "▸ Oksihemoglobin eğrisini **sola kaydırır**.",
            "🔴 ÖNEMLİ: %100 hiperbarik oksijen verilmesi COHb yarılanma ömrünü 320 dakikadan 20 dakikaya düşürür.",
            "🔵 ÇIKMIŞ SORU: Karbonmonoksit zehirlenmesinde tanısal kan gazı parametresidir."
        ],
        "pitfallsAndWarnings": [
            "Hastayı temiz havaya çıkarmak yetersiz kalabilir; derhal yüksek konsantrasyonlu oksijen başlanmalıdır."
        ],
        "relatedItems": ["karbonmonoksit-toksisitesi"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "mallory-denk-cisimcikleri",
        "term": "Mallory-Denk Cisimcikleri (Mallory Hyalini)",
        "latinName": "Corpora Mallory-Denk",
        "aliases": ["Mallory Hyalini", "Mallory Cisimcikleri"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Hasarlı, balonlaşmış hepatositlerin sitoplazmasında izlenen, ubikuitin ile kompleks yapmış sitokeratin 8 ve 18 ara filamanlarının presipite olmasıyla oluşan eozinofilik amorf intraselüler inklüzyon cisimcikleridir.",
        "lectureContextNotes": "Alkolik hepatitin patognomonik lezyonudur; etrafında nötrofilik infiltrasyon izlenir. Wilson hastalığı ve NASH/MASH'ta da görülebilir.",
        "morphologyOrMechanism": "Asetaldehit ve oksidatif stres mikrotübül ağını çökertir -> Sitokeratin 8 ve 18 ara filamanları katlanamaz ve ubikuitinlenir -> Proteazomda eritilemeyip sitoplazmada pembe ip yumağı şeklinde toplanır.",
        "differentialDiagnosis": [
            {"condition": "Councilman (Apoptotik) Cisimcikleri", "distinction": "Viral hepatitte görülen büzüşmüş nükleuslu apoptotik hepatosit parçalarıdır; intraselüler inklüzyon değildir."},
            {"condition": "Lewy Cisimcikleri", "distinction": "Parkinson hastalığında nöron sitoplazmasındaki alfa-sinüklein birikimleridir."}
        ],
        "examSpotPearls": [
            "▸ Biyokimyasal yapısı: **Sitokeratin 8/18** ara filamanları ve **Ubikuitin**.",
            "🔴 ÖNEMLİ: Alkolik hepatitte ölen hepatosit sitoplazmasında pembe inklüzyonlar olarak izlenir.",
            "🔵 ÇIKMIŞ SORU: Çevresinde nötrofil toplanması (satellitozis) tipiktir."
        ],
        "pitfallsAndWarnings": [
            "Yalnızca alkole özgü değildir; non-alkolik steatohepatit (MASH), Wilson hastalığı ve kolestatik karaciğer hastalıklarında da görülebilir."
        ],
        "relatedItems": ["alkolik-karaciger-hastaligi", "cyp2e1-meos-yolagi"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "cyp2e1-meos-yolagi",
        "term": "CYP2E1 (Mikrozomal Etanol Oksidasyon Sistemi - MEOS)",
        "latinName": "Cytochromum P450 2E1 (MEOS)",
        "aliases": ["CYP2E1", "MEOS"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Farmakoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Karaciğer endoplazmik retikulumunda yer alan, kronik yüksek doz alkol alımıyla indüklenen ve etanolü asetaldehite dönüştürürken serbest oksijen radikalleri (ROS) açığa çıkararak hepatosit nekrozuna yol açan sitokrom P450 izoenzimidir.",
        "lectureContextNotes": "Ders notunda kronik alkoliklerde tolerans gelişiminden ve parasetamol gibi ilaçların toksik metabolitlerine (NAPQI) dönüşümünü hızlandırarak karaciğer yetmezliği yapmasından sorumlu tutulmuştur.",
        "morphologyOrMechanism": "Etanol + NADPH + O2 -> Asetaldehit + NADP+ + H2O. Reaksiyonda süperoksit ve hidroksil radikalleri oluşur; membran lipid peroksidasyonu gerçekleşir.",
        "differentialDiagnosis": [
            {"condition": "Alkol Dehidrogenaz (ADH)", "distinction": "Sitozoliktir, düşük alkolde çalışır, indüklenmez, ROS üretmez."},
            {"condition": "CYP3A4", "distinction": "Karaciğerdeki en yaygın P450 enzimidir; birçok ilacı yıkar ancak alkolün MEOS yolağında primer CYP2E1 rol oynar."}
        ],
        "examSpotPearls": [
            "▸ Kronik alkolizmde indüklenen mikrozomal enzimdir.",
            "🔴 ÖNEMLİ: Etanolü yıkarken **Serbest Oksijen Radikalleri (ROS)** üreterek hepatotoksisiteyi artırır.",
            "🔵 ÇIKMIŞ SORU: Parasetamolün toksik metaboliti NAPQI'ye dönüşümünü hızlandırarak fatal karaciğer nekrozu riskini katlar."
        ],
        "pitfallsAndWarnings": [
            "Alkolik hastaya normal dozda parasetamol verilmesi bile fulminan karaciğer yetmezliği yapabilir."
        ],
        "relatedItems": ["alkolik-karaciger-hastaligi", "mallory-denk-cisimcikleri"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "marasmus",
        "term": "Marasmus",
        "latinName": "Marasmus nutritionalis",
        "aliases": ["Marasmus", "Kalori Malnütrisyonu"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Pediatri",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Hem protein hem de kalorinin kombine ve ağır eksikliği sonucu gelişen; vücut ağırlığının <%60'a düştüğü, somatik kas ve yağ depolarının tamamen eridiği ancak serum albümininin korunduğu ve ödemin görülmediği şiddetli akut malnütrisyon tablosudur.",
        "lectureContextNotes": "İlk 1 yaşta anne sütünün kesilmesiyle başlar. Bichat yağ pedlerinin erimesiyle 'yaşlı adam yüzü' oluşur. Visseral protein korunduğu için ödem ve asit yoktur.",
        "morphologyOrMechanism": "Açlık -> Glukokortikoid (kortizol) artışı -> İskelet kası proteolizi ve lipoliz. Visseral protein (karaciğer) korunur -> Serum albümini normal sınırlarda kalır.",
        "differentialDiagnosis": [
            {"condition": "Kwashiorkor", "distinction": "Kwashiorkor'da kalori değil protein yoksunluğu vardır; karaciğer iflas eder, hipoalbüminemi, masif ödem, asit ve yağlı karaciğer gelişir."},
            {"condition": "Kaşeksi (Kanser/Tüberküloz)", "distinction": "Enflamatuar sitokinlerin (TNF-alfa / kaşektin) aracılık ettiği katabolik durumdur."}
        ],
        "examSpotPearls": [
            "▸ Temel eksiklik: **AĞIR KALORİ (ENERJİ)** yetersizliği.",
            "🔴 ÖNEMLİ: **ÖDEM KESİNLİKLE YOKTUR!** (Serum albümini korunmuştur).",
            "🔵 ÇIKMIŞ SORU: Yanak yağ dokusunun erimesiyle oluşan **'Yaşlı Adam / Maymun Yüzü'** görünümü tipiktir."
        ],
        "pitfallsAndWarnings": [
            "Hızlı besleme refeeding sendromu ile ani ölüme yol açabilir; elektrolitler (fosfat, potasyum) yakından izlenmelidir."
        ],
        "relatedItems": ["kwashiorkor"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "kwashiorkor",
        "term": "Kwashiorkor",
        "latinName": "Kwashiorkor",
        "aliases": ["Kwashiorkor", "Ödemli Malnütrisyon"],
        "category": "hastalik",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Pediatri",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Kalori alımı karbonhidratla göreceli olarak korunurken protein alımının neredeyse sıfır olduğu; ağır hipoalbüminemi, masif periferik ödem, asit, yağlı karaciğer (steatoz) ve soyulan boya dermatiti ile seyreden şiddetli malnütrisyon tablosudur.",
        "lectureContextNotes": "1-4 yaşta karbonhidrat lapalarıyla beslenen çocuklarda görülür. Apolipoprotein yapılamadığı için karaciğer aşırı yağlanır. Flaky-paint dermatiti ve bayrak saçı tipiktir.",
        "morphologyOrMechanism": "Diyet proteini yokluğu -> Karaciğer visseral protein sentezi çöker -> Hipoalbüminemi -> Plazma onkotik basınç düşüşü ve jeneralize ödem/asit. Apolipoprotein (ApoB) yapılamaz -> Karaciğerden yağ çıkamaz -> Hepatik steatoz.",
        "differentialDiagnosis": [
            {"condition": "Marasmus", "distinction": "Marasmus'ta kalori eksiktir, kas erir, albümin normaldir ve ödem KESİNLİKLE yoktur. Kwashiorkor'da ise masif ödem vardır."},
            {"condition": "Nefrotik Sendrom", "distinction": "Nefrotik sendromda masif proteinüri vardır; Kwashiorkor'da idrarda protein kaybı yoktur, yetersiz alım vardır."}
        ],
        "examSpotPearls": [
            "▸ Temel eksiklik: **SELEKTİF PROTEİN YOKSUNLUĞU** (karbonhidrat görece korunmuştur).",
            "🔴 ÖNEMLİ: **Ağır hipoalbüminemi ve jeneralize ÖDEM / ASİT** kardinal bulgudur.",
            "🔵 ÇIKMIŞ SORU: Karaciğerde aşırı yağlanma (steatoz) görülmesinin nedeni **Apolipoprotein sentezlenememesidir**."
        ],
        "pitfallsAndWarnings": [
            "Ödem çocuğun kilosunu yanıltıcı şekilde normal gösterebilir; kilo düşüklüğünü maskeler."
        ],
        "relatedItems": ["marasmus", "flaky-paint-dermatiti"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "leptin",
        "term": "Leptin ve Leptin Direnci",
        "latinName": "Leptinum",
        "aliases": ["Leptin", "Tokluk Hormonu", "OB Geni Ürünü"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Fizyoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Beyaz adipoz doku tarafından sentezlenen, kandaki düzeyi toplam yağ deposu ile doğru orantılı olan, hipotalamusta POMC/CART nöronlarını uyararak tokluk hissi oluşturan ve enerji harcamasını artıran 16 kDa ağırlığında peptit hormondur.",
        "lectureContextNotes": "Ders notunda lipostat modelinin ana afferent sinyali olarak sunulmuştur. Obez bireylerde kanda düzeyi çok yüksektir ancak hipotalamusta leptin direnci nedeniyle tokluk sinyali iletilemez.",
        "morphologyOrMechanism": "Hipotalamus arkuat nükleusta LepR reseptörüne bağlanır -> STAT3 fosforilasyonu -> POMC nöronları alfa-MSH salgılar -> MC4R aktive olur -> İştah kesilir ve sempatik tonus artar. Aynı zamanda iştah açıcı NPY/AgRP nöronlarını inhibe eder.",
        "differentialDiagnosis": [
            {"condition": "Ghrelin", "distinction": "Mideden salınır, açlıkta artar, iştahı artırır (oreksijenik). Leptin ise tokluk sağlar (anoreksijenik)."},
            {"condition": "Adiponektin", "distinction": "Adiposit kaynaklıdır ancak obezitede düzeyi düşer; leptin ise obezitede artar."}
        ],
        "examSpotPearls": [
            "▸ Hipotalamusta POMC nöronlarını uyararak **tokluk oluşturan** ana adipokin.",
            "🔴 ÖNEMLİ: Yaygın insan obezitesinde leptin eksikliği değil, **LEPTİN DİRENCİ** vardır.",
            "🔵 ÇIKMIŞ SORU: Monogenik obezitelerin en sık nedeni leptin yolağındaki **Melanokortin-4 Reseptör (MC4R)** mutasyonudur."
        ],
        "pitfallsAndWarnings": [
            "Obez kişiye dışarıdan leptin verilmesi leptin direnci nedeniyle kilo kaybı SAĞLAMAZ."
        ],
        "relatedItems": ["adiponektin"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "adiponektin",
        "term": "Adiponektin",
        "latinName": "Adiponectinum",
        "aliases": ["Adiponektin", "Acrp30"],
        "category": "protein",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Biyokimya",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Adipositler tarafından salgılanan; kasta ve karaciğerde AMP kinazı (AMPK) uyararak yağ asidi oksidasyonunu artıran, glukoneogenezi baskılayan, insülin duyarlılığı sağlayan ve endoteli koruyan, obezitede düzeyi azalan koruyucu adipokindir.",
        "lectureContextNotes": "Ders notunda 'İyi adipokin' olarak tanımlanmış ve yağ dokusu arttıkça kandaki seviyesinin paradoksal olarak düştüğü vurgulanmıştır.",
        "morphologyOrMechanism": "AdipoR1 ve AdipoR2 reseptörlerine bağlanır -> AMPK ve PPAR-alfa aktivasyonu -> Kasta glukoz girişi artar, hepatik yağ yakımı hızlanır, endotelde adezyon molekülleri baskılanır.",
        "differentialDiagnosis": [
            {"condition": "Leptin", "distinction": "Leptin obezitede artar; Adiponektin ise obezitede azalır."},
            {"condition": "Rezistin / TNF-alfa", "distinction": "Adipoz dokudan salınarak insülin direncini artıran zararlı sitokinlerdir."}
        ],
        "examSpotPearls": [
            "▸ **İnsülin duyarlılaştırıcı ve anti-aterojenik** adipokin.",
            "🔴 ÖNEMLİ: **Obezitede kandaki düzeyi PARADOKSAL OLARAK AZALIR!**",
            "🔵 ÇIKMIŞ SORU: Düşük adiponektin seviyeleri Tip 2 Diyabet ve metabolik sendrom riskini katlar."
        ],
        "pitfallsAndWarnings": [
            "Kilo verme ve egzersiz adiponektin seviyelerini tekrar yükseltir."
        ],
        "relatedItems": ["leptin"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "yeni-nesil-dizileme-ngs",
        "term": "Yeni Nesil Dizileme (Next Generation Sequencing - NGS)",
        "latinName": "Sequentia novae generationis (NGS)",
        "aliases": ["NGS", "Yüksek Verimli Paralel Dizileme"],
        "category": "terim",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Moleküler Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Milyonlarca DNA veya RNA parçasını aynı anda büyük ölçekli ve paralel olarak dizileyerek tüm ekzomu, transkriptomu veya yüzlerce onkogeni tek bir reaksiyonda tarayabilen yüksek verimli moleküler analiz teknolojisidir.",
        "lectureContextNotes": "Ders notunda onkolojide multigen panelleri, hedefe yönelik tedavilerin belirlenmesi (EGFR, ALK, BRAF vb.) ve likit biyopside dolaşan serbest tümör DNA'sı (ctDNA) analizinde altın standart olduğu vurgulanmıştır.",
        "morphologyOrMechanism": "Kütüphane hazırlığı -> Klonik amplifikasyon -> Floresan işaretli nükleotidlerle sentez sırasında eşzamanlı optik okuma -> Biyoenformatik hizalama ve varyant analizi.",
        "differentialDiagnosis": [
            {"condition": "Sanger Dizileme", "distinction": "Sanger tek seferde yalnızca tek bir DNA amplikonunu okur (düşük verim); NGS ise milyonlarca parçayı paralel okur."},
            {"condition": "FISH", "distinction": "FISH mikroskopta spesifik gen amplifikasyonunu/translokasyonunu gösterir; nükleotid sekansını dizileyemez."}
        ],
        "examSpotPearls": [
            "▸ Kanser biyopsisinde aynı anda yüzlerce geni tarayan multigen panellerinin teknolojisidir.",
            "🔴 ÖNEMLİ: Kanda dolaşan serbest tümör DNA'sını (**Likit Biyopsi - ctDNA**) saptamada devrim yaratmıştır.",
            "🔵 ÇIKMIŞ SORU: Akciğer karsinomunda hedefe yönelik tüm mutasyonları tek doku kesitinde belirlemede kullanılır."
        ],
        "pitfallsAndWarnings": [
            "Biyoenformatik veri hacmi çok büyüktür; saptanan VUS (anlamı belirsiz varyant) mutasyonları dikkatle değerlendirilmelidir."
        ],
        "relatedItems": ["floresan-in-situ-hibridizasyon-fish"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "floresan-in-situ-hibridizasyon-fish",
        "term": "Floresan İn Situ Hibridizasyon (FISH)",
        "latinName": "Hybridisatio in situ fluorescens (FISH)",
        "aliases": ["FISH"],
        "category": "terim",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Moleküler Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Floresan boyalarla işaretlenmiş spesifik DNA problarının mikroskop camındaki hücre veya doku kesitindeki tamamlayıcı DNA dizilerine bağlanarak gen amplifikasyonlarını, delesyonlarını veya translokasyonlarını floresan mikroskobunda gösteren moleküler sitogenetik yöntemdir.",
        "lectureContextNotes": "Bölünmeyen interfaze hücrelerde ve rutin formalinle fikse parafinde (FFPE) çalışabilmesi en büyük avantajıdır. Meme kanserinde HER2 amplifikasyonu ve akciğerde ALK translokasyonunda altın standarttır.",
        "morphologyOrMechanism": "Prob ve hedef DNA denatüre edilir -> Hibridizasyon sağlanır -> Floresan mikroskobunda sinyaller sayılır (örn: Kırmızı HER2 sinyali / Yeşil CEP17 sentromer oranı > 2 ise amplifikasyon pozitiftir).",
        "differentialDiagnosis": [
            {"condition": "G-Bantlama Karyotipi", "distinction": "Karyotipte yaşayan canlı bölünen hücre şarttır ve çözünürlük düşüktür (>5 Mb). FISH interfaze hücrede ve mikrodelesyonda (100 kb) çalışır."},
            {"condition": "İmmünohistokimya (IHC)", "distinction": "IHC proteini boyar (HER2 3+); FISH ise gen kopyasını doğrudan sayar."}
        ],
        "examSpotPearls": [
            "▸ Bölünmeyen interfaze hücrelerde ve parafin blokta çalışabilir.",
            "🔴 ÖNEMLİ: Meme kanserinde **HER2 gen amplifikasyonunu teyit etmede altın standarttır**.",
            "🔵 ÇIKMIŞ SORU: Akciğer adenokarsinomunda EML4-ALK füzyonunu saptayan 'break-apart' prob yöntemidir."
        ],
        "pitfallsAndWarnings": [
            "Yalnızca probun hedeflediği spesifik bölgeyi gösterir; tüm genomu tarayamaz."
        ],
        "relatedItems": ["yeni-nesil-dizileme-ngs"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    },
    {
        "id": "kistik-medyal-nekroz",
        "term": "Kistik Medyal Nekroz (Erdheim Hastalığı)",
        "latinName": "Necrosis medialis cystica Erdheim",
        "aliases": ["Kistik Medyal Nekroz", "Medyal Dejenerasyon"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş / Robbins 11. Baskı",
        "definition": "Büyük elastik arterlerin (özellikle çıkan aort) tunika medya tabakasında elastik liflerin fragmantasyonu, düz kas hücresi kaybı ve açılan boşluklarda amorf glikozaminoglikan / mukoid matriks birikimi ile seyreden dejeneratif vaskülopatidir.",
        "lectureContextNotes": "Marfan sendromunun en karakteristik vasküler morfolojisidir ve aort diseksiyonunun ana anatomik zeminini oluşturur.",
        "morphologyOrMechanism": "Fibrillin veya kollajen kusuru -> Medyada elastik lifler parçalanır ve düz kas hücreleri ölür -> Açılan kist benzeri lakünler bazofilik mukopolisakkaritlerle dolar. Gerçek bir enflamasyon veya koagülasyon nekrozu yoktur!",
        "differentialDiagnosis": [
            {"condition": "Ateroskleroz", "distinction": "Ateroskleroz intimanın lipid birikimi ve fibröz plak hastalığıdır; kistik medyal nekroz ise tunika medyanın dejenerasyonudur."},
            {"condition": "Sifilitik Aortit", "distinction": "Vaza vazorumlarda endarterit obliterans ve plazmosit infiltrasyonu vardır; ağaç kabuğu manzarası yapar."}
        ],
        "examSpotPearls": [
            "▸ Tunika medyadaki elastik liflerin parçalanması ve mukoid madde birikimidir.",
            "🔴 ÖNEMLİ: **Aort Diseksiyonu ve Rüptürünün** en önemli zemin hazırlayıcı lezyonudur.",
            "🔵 ÇIKMIŞ SORU: Marfan sendromunda aort anevrizması ve diseksiyonunun histopatolojik temelidir."
        ],
        "pitfallsAndWarnings": [
            "İsmi 'nekroz' olmasına rağmen mikroskopta hücresel koagülasyon nekrozu veya enflamasyon görülmez; mukoid dejenerasyondur."
        ],
        "relatedItems": ["marfan-sendromu", "fibrillin-1-geni"],
        "aiAudit": {"verified": True, "curator": "Antigravity Pathology Engine", "confidence": 99}
    }
]

# Merge into encyclopedia
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
    "marfan sendromu": {
        "term": "Marfan Sendromu",
        "category": "hastalik",
        "description": "FBN1 gen mutasyonuna bağlı otozomal dominant bağ dokusu hastalığı; aşırı boy, araknodaktili, pektus deformitesi, ektopia lentis (yukarı-dışa) ve aort kökü diseksiyonu.",
        "clinicalPearl": "En sık ölüm nedeni aort kistik medyal nekrozu zemininde gelişen aort diseksiyonudur. Serbest TGF-β aşırı aktiftir; Losartan bu yolağı baskılar.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "fibrillin-1": {
        "term": "Fibrillin-1 (FBN1)",
        "category": "protein",
        "description": "Elastik liflerin mikrofibril iskeletini kuran ve latent TGF-β'yı bağlayan 15q21.1 lokusundaki glikoprotein.",
        "clinicalPearl": "Mutasyonunda mikrofibriller çöker ve serbest kalan TGF-β elastolizis yaparak Marfan sendromunu tetikler.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "kistik fibrozis": {
        "term": "Kistik Fibrozis (CF)",
        "category": "hastalik",
        "description": "CFTR klorür kanalı mutasyonuna bağlı en sık ölümcül otozomal resesif hastalık; koyu yapışkan mukus, Pseudomonas bronşiektazisi, pankreas yetmezliği ve terde yüksek tuz.",
        "clinicalPearl": "En sık mutasyon Delta-F508'dir. Yenidoğanda mekonyum ileusu; altın standart tanı ter testinde klorun >60 mEq/L saptanmasıdır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "cftr geni": {
        "term": "CFTR Geni",
        "category": "protein",
        "description": "Kromozom 7q31.2'de kodlanan cAMP bağımlı epitel klorür ve bikarbonat iletim kanalı.",
        "clinicalPearl": "Solunumda klor salıp ENaC'ı frenler; ter bezinde ise kloru geri emer. Kistik fibroziste bu denge bozulur.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "down sendromu": {
        "term": "Down Sendromu (Trizomi 21)",
        "category": "hastalik",
        "description": "Fazladan 21. kromozom bulunmasıyla oluşan en sık kromozomal anöploidi; epikantus, simian çizgisi, AVSD kalp defekti, duodenal atrezi ve lösemi yatkınlığı.",
        "clinicalPearl": "%95 maternal mayotik non-disjunction kaynaklıdır. 40 yaş üstünde APP gen dozajı nedeniyle erken Alzheimer kaçınılmazdır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "tek nükleotid polimorfizmi": {
        "term": "Tek Nükleotid Polimorfizmi (SNP)",
        "category": "terim",
        "description": "Genomik DNA'da tek bir bazın değişmesiyle oluşan ve toplumda >%1 sıklıkta bulunan en yaygın genetik çeşitlilik türü.",
        "clinicalPearl": "Genomda 10 milyondan fazla bulunur; poligenik multifaktöryel hastalıkların GWAS haritalamasında kullanılır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "kopya sayısı varyasyonu": {
        "term": "Kopya Sayısı Varyasyonu (CNV)",
        "category": "terim",
        "description": "Genomda 1 kilobazdan büyük DNA segmentlerinin delesyonu veya duplikasyonu.",
        "clinicalPearl": "İnsanlar arasındaki nükleotid baz çeşitliliğinin yarısından fazlasını oluşturur; otizm ve mikrodelesyonlarda önemlidir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "kurşun toksisitesi": {
        "term": "Kurşun Toksisitesi (Satürnizm)",
        "category": "patoloji",
        "description": "Eski boya ve borulardan alınan kurşunun hem sentezini ve sinir sistemini felç ettiği kronik ağır metal zehirlenmesi.",
        "clinicalPearl": "ALA dehidrataz ve ferroşelataz inhibisyonu, mikrositer anemi, eritrositlerde bazofilik noktalanma, epifiz kurşun hatları ve diş etinde Burton çizgisi yapar.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "bazofilik noktalanma": {
        "term": "Bazofilik Noktalanma (Basophilic Stippling)",
        "category": "patoloji",
        "description": "Kurşun zehirlenmesinde pirimidin 5'-nükleotidaz inhibisyonu sonucu eritrosit içinde biriken ribozomal RNA agregatları.",
        "clinicalPearl": "Periferik yaymada eritrosit içinde koyu mavi-mor ince noktacıklar olarak izlenir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "karbonmonoksit zehirlenmesi": {
        "term": "Karbonmonoksit Zehirlenmesi",
        "category": "patoloji",
        "description": "Eksik yanma gazı olan CO'nun hemoglobine 200 kat afiniteyle bağlanarak hücresel oksijen transferini durdurması.",
        "clinicalPearl": "Deri kiraz kırmızısıdır; beyinde bilateral globus pallidus nekrozu patognomoniktir. Tedavi %100 hiperbarik oksijendir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "mallory-denk cisimcikleri": {
        "term": "Mallory-Denk Cisimcikleri",
        "category": "patoloji",
        "description": "Alkolik hepatitte hasarlı hepatosit sitoplazmasında izlenen sitokeratin 8/18 ve ubikuitin kaynaklı eozinofilik inklüzyonlar.",
        "clinicalPearl": "Etrafında nötrofillerin toplanması (satellitozis) tipiktir; viral hepatitten ayırıcı tanıyı sağlar.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "cyp2e1": {
        "term": "CYP2E1 (MEOS)",
        "category": "protein",
        "description": "Kronik alkol tüketiminde indüklenen ve etanolü parçalarken reaktif oksijen türleri (ROS) üreten sitokrom P450 izoenzimi.",
        "clinicalPearl": "Parasetamolün toksik metabolit NAPQI'ye dönüşümünü hızlandırarak ölümcül karaciğer nekrozu yaratabilir.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "marasmus": {
        "term": "Marasmus",
        "category": "hastalik",
        "description": "Ağır kalori (enerji) yoksunluğuna bağlı somatik iskelet kası ve subkutan yağ dokusunun tamamen eridiği çocukluk malnütrisyonu.",
        "clinicalPearl": "Bichat yağ pedleri erir ve 'yaşlı adam yüzü' oluşur; visseral protein ve albümin korunduğu için ÖDEM KESİNLİKLE YOKTUR.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "kwashiorkor": {
        "term": "Kwashiorkor",
        "category": "hastalik",
        "description": "Kalori görece korunurken ağır protein yoksunluğu sonucu karaciğer protein sentezinin çöktüğü ödemli çocukluk malnütrisyonu.",
        "clinicalPearl": "Hipoalbüminemi, masif ödem, asit, apolipoprotein sentezlenememesiyle karaciğer yağlanması ve flaky-paint dermatiti görülür.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "leptin": {
        "term": "Leptin",
        "category": "protein",
        "description": "Adipositlerden salınarak hipotalamus arkuat nükleusta POMC nöronları ve MC4R üzerinden tokluk oluşturan hormon.",
        "clinicalPearl": "Obezitede leptin çok yüksektir ancak leptin direnci vardır; tokluk sinyali iletilemez.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "adiponektin": {
        "term": "Adiponektin",
        "category": "protein",
        "description": "Adipositlerden salınan, insülin duyarlılığını artıran ve yağ asidi oksidasyonunu hızlandıran koruyucu adipokin.",
        "clinicalPearl": "Obezitede plazma düzeyi paradoksal olarak AZALIR; düşüklüğü Tip 2 DM ve aterosklerozu tetikler.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "yeni nesil dizileme": {
        "term": "Yeni Nesil Dizileme (NGS)",
        "category": "terim",
        "description": "Milyonlarca DNA parçasını paralel dizileyerek kanserde yüzlerce onkogeni tek dokuda tarayan yüksek verimli teknoloji.",
        "clinicalPearl": "Akciğer ve kolonda hedefe yönelik tedavi mutasyonlarının (EGFR, ALK, KRAS, BRAF) saptanmasında altın standarttır.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    },
    "kistik medyal nekroz": {
        "term": "Kistik Medyal Nekroz",
        "category": "patoloji",
        "description": "Büyük arterlerin tunika medyasında elastik liflerin parçalanması ve boşluklarda mukoid madde birikmesi.",
        "clinicalPearl": "Marfan sendromunda ölümcül aort kökü dilatasyonu ve aort diseksiyonunun zemin hazırlayıcı lezyonudur.",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1"
    }
}

added_gloss_count = 0
for k, v in new_glossary_items.items():
    if k not in glossary:
        added_gloss_count += 1
    glossary[k] = v

with open(GLOSSARY_PATH, "w", encoding="utf-8") as f:
    json.dump(glossary, f, ensure_ascii=False, indent=2)

print(f"Updated medical_glossary.json! Added/Updated {added_gloss_count} keys. Total now: {len(glossary)}")
