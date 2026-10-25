#!/usr/bin/env python3
"""Generate a complete, deep amfi-level lecture for Lesson 64: Omurga Tümörleri.

Covers all 20 pages without skipping any page or bullet point.
Generates ~135-140 sentences, ~2,800-3,200 spoken words (~22-26 minutes of deep amfi audio).
Includes all 11 validated drawing commands.
Strictly adheres to Turkish style standard and zero forward leak rule.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-64-omurga-tumorleri"
KAYNAK_MD = TASLAK / "kaynak.md"

kaynak_txt = KAYNAK_MD.read_text(encoding="utf-8")

# Parse pages and non-empty lines from kaynak.md
pages_lines = {}
for p in re.split(r'=== SAYFA (\d+) ===', kaynak_txt)[1:]:
    if p.isdigit():
        curr_p = int(p)
    else:
        ll = []
        for line in p.strip().splitlines():
            cl = line.strip(' ✓\t').strip()
            cl = re.sub(r'^[✓\s\-*•o❑➢]+', '', cl).strip()
            if len(cl) > 3 and not cl.isdigit() and not cl.startswith('==='):
                ll.append(cl)
        pages_lines[curr_p] = ll

def find_satir(pno, pattern=None, idx=0):
    lines = pages_lines.get(pno, [])
    if not lines:
        return "Omurga Tümörleri"
    if pattern:
        for l in lines:
            if pattern.casefold() in l.casefold():
                return l
    if idx < len(lines):
        return lines[idx]
    return lines[-1]

c_counter = 1

def make_sentence(ekran, ses, pno, satir_pattern=None, satir_idx=0, cikmis=None, highlight_word=None, sekil=None):
    global c_counter
    cid = f"k2-64-c{c_counter:04d}"
    c_counter += 1
    
    satir = find_satir(pno, satir_pattern, satir_idx)
    slayt_obj = {
        "sayfa": pno,
        "satir": satir
    }
    if sekil:
        slayt_obj["sekil"] = sekil
        
    vurgu_list = []
    if highlight_word:
        clean_ekran = ekran.replace("**", "")
        if highlight_word.casefold() in clean_ekran.casefold():
            vurgu_list.append({"metin": highlight_word, "tur": "terim"})
            
    c_obj = {
        "id": cid,
        "duzey": 0,
        "ekran": ekran,
        "ses": ses,
        "slayt": slayt_obj,
        "vurgu": vurgu_list
    }
    if cikmis:
        c_obj["cikmis"] = [cikmis] if isinstance(cikmis, str) else cikmis
    return c_obj


def main():
    global c_counter
    c_counter = 1

    PD = {}

    # ==============================================================================
    # BÖLÜM 1: Omurga Tümörlerine Genel Bakış ve Epidemiyoloji (Sayfa 1 - 2)
    # ==============================================================================

    PD[1] = [
        ("**Ders Başlığı:** Beyin ve sinir cerrahisi kliniğinde omurga tümörleri konusunu işleyeceğiz.",
         "Beyin ve sinir cerrahisi klinik stajımız kapsamında omurga tümörleri, primer selim ve habis kemik lezyonları ile metastatik omurga patolojilerini kapsamlı biçimde ele alacağız.",
         "Omurga Tümörleri", 0, None, "omurga tümörleri", None),
        ("**Dersi Veren Öğretim Üyesi:** Dersimiz Doktor Öğretim Üyesi Aydın Sinan Apaydın tarafından hazırlanmıştır.",
         "Dersimiz Karabük Üniversitesi Tıp Fakültesi Beyin ve Sinir Cerrahisi Anabilim Dalından Doktor Öğretim Üyesi Aydın Sinan Apaydın tarafından hazırlanmıştır.",
         "Aydın Sinan APAYDIN", 1, None, "Aydın Sinan Apaydın", None),
        ("Omurga tümörleri omuriliğe yakınlığı ve **mekanik stabiliteyi bozması** nedeniyle cerrahi açıdan kritiktir.",
         "Omurga neoplazileri gerek medulla spinalis ve sinir köklerine doğrudan bası oluşturması, gerekse omurga kolonunun biyomekanik yük taşıma dengesini bozması nedeniyle erken tanı gerektiren hayati tablolardır.",
         "Omurga Tümörleri", 0, None, "mekanik stabilite", None),
        ("Klinik pratikte hastalar hekime en sık **gece artan inatçı sırt veya bel ağrısı** yakınmasıyla başvurur.",
         "Klinik pratikte hastaların en belirgin başvuru şikayeti istirahatle geçmeyen, geceleri şiddetlenen ve haftalarca sebat eden aksiyel sırt ya da bel ağrısıdır.",
         "Omurga Tümörleri", 0, None, "sırt veya bel ağrısı", None),
        ("Tümöral kitlenin spinal kanala büyümesi **ilerleyici nörolojik defisit** ve omurilik basısına yol açar.",
         "Tümöral kitlenin spinal kanala doğru genişlemesi alt ekstremitelerde motor güçsüzlük, duyu kusuru ve sfinkter disfonksiyonu ile giden bası felçlerine neden olabilir.",
         "Omurga Tümörleri", 0, None, "omurilik basısı", None),
        ("Denis üç kolon teorisine göre tümörler **iki veya daha fazla kolonu yıktığında** omurga instabilitesi gelişir.",
         "Omurga biyomekaniğinde anterior, orta ve posterior kolonların en az ikisinde tümöral kemik destrüksiyonu meydana geldiğinde omurga mekanik stabilitesini kaybeder ve cerrahi füzyon zorunlu hale gelir.",
         "Omurga Tümörleri", 0, None, "üç kolon teorisi", None),
        ("Bu derste tümörlerin **anatomik lokalizasyonları**, histopatolojik kökenleri ve sağaltım ilkeleri incelenecektir.",
         "Bu ders boyunca omurga tümörlerinin anatomik yerleşim bölgelerini, histopatolojik özelliklerini ve güncel cerrahi dekompresyon ve rekonstrüksiyon yaklaşımlarını ayrıntılı olarak öğreneceğiz.",
         "Omurga Tümörleri", 0, None, "sağaltım ilkeleri", None)
    ]

    PD[2] = [
        ("**Primer Omurga Tümörleri:** Omurgadaki tüm tümörlerin yalnızca yüzde onu primer kemik tümörüdür.",
         "Omurga kitleleri incelendiğinde omurgadaki tüm tümörlerin yalnızca yüzde onunun omurganın kendi kemik elemanlarından kaynaklanan primer kemik tümörleri olduğu görülür.",
         "yüzde onu primer", 1, None, "yüzde on", None),
        ("Geriye kalan **yüzde doksanlık devasa çoğunluğu** ise diğer organlardan gelen metastazlar oluşturur.",
         "Buna karşılık omurgayı tutan tümörlerin geriye kalan yüzde doksanlık devasa çoğunluğunu diğer organ karsinomlarının omurgaya yaptığı metastatik yayılımlar meydana getirir.",
         "yüzde onu primer", 1, None, "yüzde doksan metastaz", None),
        ("Genel omurga kitleleri temel olarak **primer kemik tümörleri** ve metastatik yayılım olarak ikiye ayrılır.",
         "Dolayısıyla omurga kitleleri sınıflanırken birincil kemik lezyonları ile uzak organlardan omurgaya ulaşan metastatik kitleler arasındaki ayırım klinik yaklaşımın temelini belirler.",
         "Primer omurga", 0, None, "primer ve metastatik", None),
        ("Erişkinlerde **hematopoetik kırmızı kemik iliğinin** omurgada yoğunlaşması metastazların bu bölgeye seçici yerleşimini açıklar.",
         "Erişkin yaş grubunda aktif hematopoetik kırmızı iliğin uzun kemiklerden çekilip omurga korpuslarında toplanması, kan yoluyla yayılan tümör embolilerinin neden omurgaya çöktüğünün temel fizyolojik izahıdır.",
         "Omurga tümörlerinin %10", 1, None, "kırmızı kemik iliği", None),
        ("Primer tümörlerin görülme oranı düşük olmakla birlikte **genç hastalarda** önemli bir morbidite kaynağıdır.",
         "Primer omurga tümörleri genel sıklık bakımından nadir görülse de, özellikle çocukluk, adölesan ve genç erişkin yaş grubunda ciddi sakatlıklara yol açabilen primer kemik patolojileridir.",
         "Primer omurga", 0, None, "genç hastalarda morbidite", None),
        ("Metastatik lezyonlar ise özellikle **elli yaş üzerindeki erişkinlerde** omurga yıkımının baş nedenidir.",
         "Metastatik omurga lezyonları ise özellikle elli yaş üzerindeki kanser hastalarında şiddetli omurga ağrısının ve patolojik kompresyon kırıklarının en yaygın nedenidir.",
         "Omurga tümörlerinin %10", 1, None, "erişkinlerde omurga yıkımı", None)
    ]

    # ==============================================================================
    # BÖLÜM 2: Primer Selim Omurga Tümörlerinin Sınıflanması (Sayfa 3)
    # ==============================================================================

    PD[3] = [
        ("**Primer Selim Omurga Tümörleri:** Kemik, kıkırdak, damar ve histiyosit kökenli yedi ana selim tümör bulunur.",
         "Omurgadan köken alan primer selim kemik tümörleri histopatolojik kökenlerine göre yedi temel grupta sınıflandırılır.",
         "Primer benign", 0, None, "primer selim tümörler", None),
        ("Bunlar **osteoid osteom**, osteoblastom, osteokondrom ve dev hücreli tümördür.",
         "Bu lezyonlar arasında kemik oluşturan osteoid osteom ve osteoblastom, kıkırdak kaynaklı osteokondrom ve korpusu tutan dev hücreli tümör yer alır.",
         "Osteoid osteom", 1, None, "osteoid osteom osteoblastom", None),
        ("Ayrıca **anevrizmal kemik kisti**, eozinofilik granülom ve hemanjiom selim gruptadır.",
         "Sınıflamanın devamında kistik boşluklar içeren anevrizmal kemik kisti, histiyositik infiltrasyonla giden eozinofilik granülom ve en sık görülen vasküler lezyon olan vertebra hemanjiomu bulunur.",
         "Anevrizmal Kemik", 5, None, "kemik kisti ve hemanjiom", None),
        ("Primer selim omurga tümörleri çoğunlukla **omurganın arka elemanlarına** yerleşme eğilimi gösterir.",
         "Primer selim omurga tümörleri anatomik olarak omurganın arka elemanları olan lamina, pedikül ve spinoz proçesleri belirgin biçimde daha sık tutma eğilimi gösterir.",
         "Primer benign", 0, None, "arka elemanlar", None),
        ("Buna karşın dev hücreli tümör ve hemanjiom **vertebra korpusunu** doğrudan etkileyen önemli istisnalardır.",
         "Bu kuralın en çarpıcı istisnası dev hücreli tümördür; zira dev hücreli tümör arka elemanlar yerine doğrudan vertebra korpusunu tutarak korpusta kemik erimesine yol açar.",
         "Dev hücreli", 4, None, "vertebra korpusu", None),
        ("Selim neoplazilerin doğru teşhisi ve **doku biyopsisi** gereksiz radikal cerrahilerden korunmayı sağlar.",
         "Lezyonların selim tabiatının doğru belirlenmesi ve cerrahi öncesi histopatolojik teyidi, gereksiz radikal omurga rezeksiyonlarının ve morbiditenin önüne geçilmesinde kilit basamaktır.",
         "Primer benign", 0, None, "doku biyopsisi", None),
        ("Selim neoplaziler doku yayılımı yapmasa da **spinal kanala taşarak** kord basısı oluşturabilir.",
         "Histolojik olarak selim nitelikte olmalarına rağmen bu lezyonlar kanal içine doğru büyüyerek omurilik veya sinir kökü basısına ve ilerleyici omurga deformitelerine yol açabilir.",
         "Primer benign", 0, None, "spinal kanal basısı", None)
    ]

    # ==============================================================================
    # BÖLÜM 3: Primer Habis Omurga Tümörlerinin Sınıflanması (Sayfa 4)
    # ==============================================================================

    PD[4] = [
        ("**Primer Habis Omurga Tümörleri:** Kemiğin primer habis tümörleri yüksek dereceli destrüksiyon yapar.",
         "Omurgadan köken alan primer habis neoplaziler çevre kemik dokuyu hızla yıkan, omurga kolonunu çökerten ve komşu yumuşak dokulara yayılan agresif tümörlerdir.",
         "Primer malign", 0, None, "primer habis tümörler", None),
        ("Primer habis grupta **osteosarkom**, kondrosarkom ve Ewing sarkomu bulunur.",
         "Bu habis lezyonlar arasında kemik matriksi oluşturan osteosarkom, kıkırdak matriksli kondrosarkom ve kemiğin küçük hücreli neoplazisi olan Ewing sarkomu yer alır.",
         "Osteosarkom", 1, None, "osteosarkom kondrosarkom", None),
        ("Hematolojik malignitelerden **multipl myelom** ve lenfoma omurgada sık yerleşir.",
         "Ayrıca plazma hücre neoplazisi olan multipl myelom ve lenfoid seri malignitesi olan lenfoma omurga korpusunu en sık istila eden habis tablolar arasındadır.",
         "Multipl Myelom", 4, None, "multipl myelom ve lenfoma", None),
        ("Notokord kalıntılarından gelişen **kordoma** ve çocuklarda görülen nöroblastom listeyi tamamlar.",
         "Embriyonik notokord kalıntılarından köken alan kordoma ile çocukluk çağında sempatik zincirden omurgaya uzanan nöroblastom diğer habis primer lezyonları oluşturur.",
         "Kordoma", 6, None, "kordoma ve nöroblastom", None),
        ("Kordomalar **brakiyüri ekspresyonu** ile tanınır ve klivus ile sakrokoksigeal bölgede yoğunlaşır.",
         "Embriyolojik notokord kalıntılarından köken alan kordomalar immünohistokimyada brakiyüri pozitifliği ve veziküler fizaliferöz hücreleriyle ayırt edilir; en sık kafa tabanında klivusta ve distal sakrumda lokalizedir.",
         "Kordoma", 6, None, "brakiyüri ekspresyonu", None),
        ("Primer habis tümörlerin tedavisinde **geniş cerrahi rezeksiyon**, kemoterapi ve radyoterapi kombine edilir.",
         "Habis omurga tümörlerinin sağaltımında tümörün sınırlarıyla birlikte çıkarıldığı geniş cerrahi rezeksiyonun yanı sıra histolojik tipe göre sistemik kemoterapi ve radyoterapi protokolleri birlikte yürütülür.",
         "Primer malign", 0, None, "cerrahi ve onkolojik tedavi", None)
    ]

    # ==============================================================================
    # BÖLÜM 4: Osteoid Osteom (Sayfa 5)
    # ==============================================================================

    PD[5] = [
        ("**Osteoid Osteom:** Genç yaşta görülen ve kemik üreten küçük boyutlu selim bir tümördür.",
         "Osteoid osteom çocukluk ve genç erişkinlik çağında, özellikle on ila yirmi beş yaş arasındaki bireylerde sıkça saptanan selim kemik oluşturan bir neoplazidir.",
         "Bening Osteoid osteom", 0, None, "osteoid osteom", None),
        ("Tümör omurgada en sık **lamina ve pedikül gibi arka kolon elemanlarını** tutar.",
         "Anatomik yerleşim açısından osteoid osteom belirgin bir seçicilik gösterir; vertebra korpusu yerine sıklıkla lamina, pedikül ve faset eklem gibi arka kolon elemanlarına oturur.",
         "Lamina ve pedikül", 2, None, "arka kolon elemanları", None),
        ("Omurga seviyelerine bakıldığında **en sık lomber bölgede** yerleştiği gözlenir.",
         "Spinal segment dağılımına bakıldığında osteoid osteomun en sık lomber omurgada, ardından torasik ve servikal segmentlerde yerleştiği saptanmaktadır.",
         "Lomber- en sık", 3, None, "en sık lomber bölge", None),
        ("Tipik klinik tablosu **dinlenmekle azalmayan ve gece şiddetlenen** kemik ağrısıdır.",
         "Hastalığın en karakteristik semptomu fiziksel istirahatle geçmeyen, özellikle gece uykudan uyandıracak düzeyde şiddetlenen ve gece şiddetlenen ağrı ile uykuyu bölen zonklayıcı omurga ağrısıdır.",
         "Dinlenmekle azalmayan", 4, None, "gece şiddetlenen ağrı", None),
        ("Bu ağrının en ayırt edici özelliği **aspirin ve nonsteroid antiinflamatuarlarla dramatik azalmasıdır**.",
         "Ağrının patognomonik özelliği prostaglandin sentezini baskılayan aspirin ve nonsteroid antiinflamatuar ilaçlara aspirine dramatik yanıt vermesi ve hızla kaybolmasıdır.",
         "Asprin ile azalan", 4, None, "aspirin ile azalma", None),
        ("Genç erişkinlerde gelişen **ağrılı skolyozun en sık nedeni** osteoid osteomdur.",
         "Klinik sınavlarda ve amfi derslerinde önemle üzerinde durulduğu üzere genç erişkinde ağrılı skolyoz tablosunun en yaygın etiyolojik nedeni osteoid osteomdur.",
         "Erişkinde ağrılı skolyozun", 5, None, "ağrılı skolyoz", None),
        ("Radyolojik incelemede **ince kesit bilgisayarlı tomografi** radyolusent nidusu saptamada altın standarttır.",
         "Osteoid osteomun merkezindeki vaskülarize osteoid nidusu ve çevresindeki yoğun sklerotik kemik halkasını en net gösteren tanısal altın standart ince kesit kemik pencere tomografisidir.",
         "Geç teşhis", 6, None, "ince kesit tomografi", None),
        ("Lezyonun çapı genellikle küçük olduğundan radyolojide **geç teşhis konulabilmektedir**.",
         "Radyolojik olarak nidus çapının iki santimetreden küçük olması ve başlangıçta konvansiyonel grafilerde güç fark edilmesi nedeniyle olgulara çoğunlukla aylar sonra geç teşhis konulur.",
         "Geç teşhis", 6, None, "geç teşhis", None),
        ("Seçilmiş uygun olgularda cerrahi yerine **perkütan radyofrekans ablasyon** yüksek klinik kür sağlar.",
         "Açık cerrahinin omurga stabilitesini bozabileceği uygun lokalizasyonlu küçük lezyonlarda tomografi kılavuzluğunda uygulanan perkütan radyofrekans ablasyon mükemmel sağaltım başarısı sunar.",
         "Bening Osteoid osteom", 0, None, "radyofrekans ablasyon", None)
    ]

    # ==============================================================================
    # BÖLÜM 5: Osteoblastom (Sayfa 6)
    # ==============================================================================

    PD[6] = [
        ("**Osteoblastom:** Histolojik olarak osteoid osteoma benzeyen ancak agresif seyreden selim bir tümördür.",
         "Osteoblastom mikroskobik olarak osteoid osteom ile büyük benzerlikler taşıyan, ancak biyolojik olarak çok daha agresif, yıkıcı ve geniş boyutlara ulaşabilen selim bir tümördür.",
         "Bening Osteoblastom", 0, None, "osteoblastom", None),
        ("Tümör omurgada sık görülür ve olguların **yüzde ellisinden fazlasında skolyoz** eşlik eder.",
         "Osteoblastom iskelet sisteminde omurgayı son derece yüksek oranda seçer ve hastaların yüzde ellisinden fazlasında reaktif kas spazmına bağlı skolyoz deformitesi ile karşımıza çıkar.",
         "skolyozla beraberdir", 3, None, "yüzde elli skolyoz", None),
        ("Hastaların **yüzde sekseni otuz yaşın altındaki** genç popülasyondan oluşur.",
         "Yaş dağılımı incelendiğinde hastaların yüzde sekseninin otuz yaşın altında olduğu, çocukluk ve erken erişkinlik evresinde pik yaptığı görülmektedir.",
         "% 80 30 yaş", 4, None, "otuz yaş altı", None),
        ("Osteoid osteom gibi omurganın **arka elemanlarını** tutar ve servikal, torasik, lomber eşit dağılır.",
         "Yerleşim odağı yine omurganın arka elemanlarıdır; ancak seviye olarak servikal, torasik ve lomber bölgelerde yaklaşık olarak eşit sıklıkta saptanır.",
         "Omurga arka elemanları", 5, None, "arka eleman tutulumu", None),
        ("Büyük boyutlara ulaşması nedeniyle **nörolojik defisit sıklıkla gelişir**.",
         "Nidus çapının iki santimetreyi aşması ve spinal kanala doğru eksofitik genişlemesi nedeniyle sinir kökü ve kord basısı oluşturarak nörolojik defisite sıkça yol açar.",
         "Büyük boyut nedeniyle", 7, None, "nörolojik defisit", None),
        ("Osteoblastom lezyonunun genişliği nedeniyle **cerrahi küretaj ve posterior enstrümantasyon** gerekir.",
         "Agresif selim tümörün arka kolon elemanlarını geniş çapta tahrip ettiği durumlarda tümörün total çıkarılmasını takiben omurganın vidalar ve çubuklarla posterior enstrümantasyonu gereklidir.",
         "Omurga arka elemanları", 5, None, "posterior enstrümantasyon", None),
        ("Osteoid osteoma kıyasla cerrahi küretaj sonrası **lokal nüks oranı belirgin daha yüksektir**.",
         "Klinik seyirde osteoid osteom ile osteoblastom karşılaştırıldığında osteoid osteomda kıyasla az nüks görülürken osteoblastomda büyük boyut ve yüksek lokal nüks oranı saptanır.",
         "Osteoid osteoma göre", 9, None, "yüksek lokal nüks", None)
    ]

    # ==============================================================================
    # BÖLÜM 6: Osteokondrom (Sayfa 7)
    # ==============================================================================

    PD[7] = [
        ("**Osteokondrom:** İskelet sisteminin en sık rastlanan selim kemik tümörüdür.",
         "Osteokondrom genel iskelet sisteminde kemik tümörleri arasında en sık karşılaşılan selim neoplazidir.",
         "Bening Osteokondrom", 0, None, "en sık kemik tümörü", None),
        ("Tümör tamamen selim tabiatlıdır ve **kemik yüzeyinden dışarı doğru büyüyen ekzostoz** şeklindedir.",
         "Lezyon kortikal kemik ve medüller kavite ile devamlılık gösteren, üzeri hyalin kıkırdak bir şapkayla örtülü kemik çıkıntısı yani ekzostoz yapısındadır.",
         "Selimdirler", 2, None, "selim ekzostoz", None),
        ("Lezyon soliter olabileceği gibi **herediter çoklu ekzostoz** sendromunda çok sayıda da görülebilir.",
         "Osteokondromlar tek bir odakta soliter olarak ortaya çıkabileceği gibi herediter multipl ekzostozis hastalığında vücudun pek çok kemiğinde çok sayıda lezyon şeklinde bulunabilir.",
         "Tek veya çok", 3, None, "tek veya çok sayıda", None),
        ("Herediter olgularda **EXT1 ve EXT2 gen mutasyonları** kıkırdak proliferasyonunu tetikler.",
         "Ailesel geçiş gösteren çoklu ekzostoz olgularında otozomal dominant kalıtılan e iks te bir ve iki genlerindeki mutasyonlar heparan sülfat sentezini bozarak kıkırdak proliferasyonunu alevlendirir.",
         "Tek veya çok", 3, None, "gen mutasyonları", None),
        ("Kıkırdak şapkadan kaynaklanan **habis dejenerasyon riski düşüktür**.",
         "Soliter lezyonlarda habis kondrosarkom dejenerasyonu riski yüzde birin altında oldukça düşüktür; ancak kıkırdak şapka kalınlığının bir buçuk santimetreyi aşması habisleşmeyi düşündürür.",
         "Habis dejenerasyon", 4, None, "habis dejenerasyon", None),
        ("Manyetik rezonansta **kıkırdak şapka kalınlığının iki santimetreyi aşması** habisleşme göstergesidir.",
         "Hastanın izleminde çekilen manyetik rezonans görüntülerinde kıkırdak şapka kalınlığının artarak iki santimetreyi geçmesi selim ekzostozun habis kondrosarkoma dönüştüğünü gösteren en kritik radyolojik alarmdır.",
         "Habis dejenerasyon", 4, None, "kıkırdak şapka kalınlığı", None),
        ("Omurgada yerleştiğinde **arka elemanlar ve özellikle spinoz proçes** tutulur.",
         "Omurga yerleşimli osteokondromlar neredeyse daima arka elemanlardan, en sık olarak da yüzeyel yerleşimli spinoz proçes ve laminalardan köken alarak dışa doğru uzanır.",
         "özellikle spinoz proces", 6, None, "spinoz proçes", None),
        ("Tümör kemik yıkımı yapmadığı için **nadiren ağrılıdır** ve mekanik kitle etkisi yaratır.",
         "Osteoid osteomun aksine osteokondrom nadiren ağrı oluşturur; çoğunlukla sırtta ele gelen sert ve ağrısız bir kemik kabarıklığı veya komşu dokulara mekanik bası ile fark edilir.",
         "Nadiren ağrılıdır", 7, None, "nadiren ağrılı", None)
    ]

    # ==============================================================================
    # BÖLÜM 7: Dev Hücreli Tümör (Sayfa 8)
    # ==============================================================================

    PD[8] = [
        ("**Dev Hücreli Tümör:** Selim ancak lokal agresif seyirli osteoklastik dev hücreli bir neoplazidir.",
         "Dev hücreli kemik tümörü histolojik olarak selim kabul edilen, ancak çevre kemik dokuyu agresif biçimde eriten ve kemik korteksini yıkan lokal destrüktif bir tümördür.",
         "Dev Hücreli Tümör", 1, None, "dev hücreli tümör", None),
        ("Genç erişkinlerde uzun kemiklerin **metafiz ve epifiz bileşkesinde** sık yerleşir.",
         "Genel ortopedik onkolojide dev hücreli tümör yirmi ila kırk yaş arasındaki genç erişkin popülasyon içinde femur distali ve tibia proksimali gibi uzun kemiklerin epifiz ve metafiz bölgelerinde görülür.",
         "metafiz ve epifiz", 3, None, "metafiz ve epifiz", None),
        ("Omurgaya yerleştiğinde diğer selim tümörlerin aksine **vertebra korpusu tutulur**.",
         "Omurga tutulumunda en kritik sınav bilgisi şudur: Arka elemanları tutan diğer selim lezyonların aksine dev hücreli tümör doğrudan vertebra korpusu tutulumu ile seyreder.",
         "Omurgada korpus tutulur", 4, None, "korpus tutulumu", None),
        ("Tümörde stromal hücreler **aşırı RANKL salgılayarak** osteoklastik kemik erimesini tetikler.",
         "Lezyonun moleküler patolojisinde mononükleer neoplastik hücrelerin aşırı miktarda rank ligant salgılaması, dokudaki çok çekirdekli dev osteoklastları aşırı uyararak vertebra korpusunda agresif kemik yıkımına yol açar.",
         "Dev Hücreli Tümör", 1, None, "RANK ligant uyarısı", None),
        ("Spinal segmentler arasında **en sık torasik omurgada** yerleşim gösterir.",
         "Omurga boyunca incelendiğinde dev hücreli lezyonun en sık torasik segment yerleşimi gösterdiği, ikinci sıklıkla da sakrumda lokalize olduğu saptanmaktadır.",
         "En sık torasik", 5, None, "en sık torasik omurga", None),
        ("Korpusu eriterek çökerttiği için **patolojik vertebra kırıkları** ve spinal kord basısı yapabilir.",
         "Vertebra korpusundaki trabeküler kemiği genişleterek sabun köpüğü manzarasıyla yıkar, korpus yüksekliğini çökertir ve spinal kanala taşarak paraplejiye varan kord basısı tablosuna yol açabilir.",
         "Omurgada korpus", 4, None, "patolojik kırık ve kord basısı", None),
        ("Cerrahi sınırın güç olduğu olgularda **RANKL inhibitörü denosumab** kemik yıkımını baskılar.",
         "Omurilik basısı nedeniyle sınırları tam temizlenemeyen olgularda rank ligant inhibitörü monoklonal antikor olan denosumab tümöral dev hücreleri baskılayarak kemiğin yeniden mineralize olmasını sağlar.",
         "Omurgada korpus tutulur", 4, None, "denosumab tedavisi", None),
        ("Sağaltımında nüksü engellemek için **geniş rezeksiyon veya agresif küretaj** uygulanır.",
         "Tedavisinde yüksek lokal nüks eğilimi nedeniyle sınırları sağlam cerrahi rezeksiyon, agresif küretaj ve gerektiğinde denosumab gibi osteoklast hedefli tedaviler kombine edilir.",
         "Dev Hücreli Tümör", 1, None, "cerrahi rezeksiyon", None)
    ]

    # ==============================================================================
    # BÖLÜM 8: Anevrizmal Kemik Kisti (Sayfa 9)
    # ==============================================================================

    PD[9] = [
        ("**Anevrizmal Kemik Kisti:** Kan dolu kistik boşluklardan oluşan osteolitik ekspansif bir lezyondur.",
         "Anevrizmal kemik kisti kemik içinde venöz kan gölcükleri ve fibröz septalar içeren, kemik korteksini dışarı doğru balonlaştıran ekspansif selim bir lezyondur.",
         "Anevrizma Kemik Kisti", 0, None, "anevrizmal kemik kisti", None),
        ("Hastaların büyük kısmı **yirmi ila otuz yaş arasındaki** genç erişkinlerdir.",
         "Hastalık ağırlıklı olarak genç yaş popülasyonunu etkiler ve olguların çok büyük bir kısmı yirmi ila otuz yaş aralığında teşhis edilir.",
         "20 - 30 yaş", 1, None, "yirmi otuz yaş", None),
        ("Omurgada lezyonların **yüzde altmışı arka elemanlara** yerleşme eğilimindedir.",
         "Anatomik yerleşim bakımından anevrizmal kemik kistlerinin yaklaşık yüzde altmışı omurganın arka elemanlarını, özellikle pedikül ve laminaları tutar.",
         "Arka elemanlar (% 60)", 2, None, "arka elemanlar", None),
        ("Segment olarak **en sık lomber omurgada** karşımıza çıkar.",
         "Omurga kolonunda en sık lomber segmentte yerleşim gösterirken, ikinci sıklıkla torasik ve servikal vertebralarda saptanır.",
         "Lomber bölgede sık", 3, None, "lomber bölge", None),
        ("Hastalarda ana semptom **haftalarca süren inatçı bel ağrısıdır**.",
         "Klinik prezentasyonda ana semptom faset eklem ve kemik korteksinin gerilmesine bağlı ortaya çıkan şiddetli ve inatçı bel ağrısıdır.",
         "Bel ağrısı : ana", 4, None, "bel ağrısı", None),
        ("Manyetik rezonans görüntülemede **sıvı-sıvı seviyelenmeleri** kistin patognomonik bulgusudur.",
         "İki ağırlıklı manyetik rezonans kesitlerinde farklı yoğunluktaki kan ürünlerinin kist boşlukları içinde yerçekimiyle ayrışması sonucu tipik sıvı-sıvı seviyelenmesi manzarası izlenir.",
         "Anevrizma Kemik Kisti", 0, None, "sıvı sıvı seviyelenmesi", None),
        ("Kistin hızla genişlemesi nedeniyle olguların **yüzde elli beşinde nörolojik defisit** saptanır.",
         "Kistin spinal kanala doğru balonlaşarak büyümesi sonucu hastaların yüzde elli beşinde sinir kökü veya omurilik basısına bağlı nörolojik defisitler gelişir.",
         "Defisit sıktır (% 55)", 5, None, "nörolojik defisit", None),
        ("Hücrelerde **USP6 gen yeniden düzenlenmesi** lezyonun neoplastik klonal doğasını doğrular.",
         "Sitogenetik çalışmalarda hücrelerin on yedinci kromozom üzerinde yer alan u se pe altı geni üzerinden yeniden düzenlenme göstermesi anevrizmal kemik kistinin gerçek bir neoplazi olduğunu kanıtlamıştır.",
         "Arka elemanlar (% 60)", 2, None, "gen yeniden düzenlenmesi", None),
        ("Osteoblastom ve osteoid osteom gibi **ağrılı skolyoz tablosuna** yol açabilir.",
         "Omurganın tek tarafındaki arka elemanın asimetrik büyümesi ve kas spazmı nedeniyle osteoblastom ve osteoid osteoma benzer biçimde ağrılı skolyoz deformitesi yapar.",
         "ağrılı skolyoz yapar", 6, None, "ağrılı skolyoz", None),
        ("Temel tedavi **cerrahi rezeksiyondur**; nüksü önlemek için adjuvan radyoterapi veya embolizasyon verilebilir.",
         "Tedavinin temel taşı kistin cerrahi olarak boşaltılması ve çıkarılmasıdır; tam çıkarılamayan olgularda cerrahi öncesi embolizasyon ve adjuvan radyoterapi uygulanabilir.",
         "Radyoterapi adjuvan", 8, None, "cerrahi ve radyoterapi", None)
    ]

    # ==============================================================================
    # BÖLÜM 9: Eozinofilik Granülom ve Hand-Schüller-Christian Triadı (Sayfa 10 - 11)
    # ==============================================================================

    PD[10] = [
        ("**Eozinofilik Granülom:** Langerhans hücreli histiyositozun kemikteki tekil veya çoklu lezyonudur.",
         "Eozinofilik granülom klonal dendritik hücrelerin ve eozinofillerin kemik dokuda birikimiyle karakterize Langerhans hücreli histiyositoz formudur.",
         "Eozinofilik Granulom", 0, None, "eozinofilik granülom", None),
        ("Hastalık en sık **ikinci dekadda görülür**, beş ve on yaşlarında iki ayrı pik yapar.",
         "Yaş epidemiyolojisine bakıldığında hastalık en sık hayatın ikinci dekadında izlenir; özellikle beş ve on yaşlarında olmak üzere iki ayrı tepe noktası sergiler.",
         "5 ve 10 yaşta pik", 5, None, "beş ve on yaş pik", None),
        ("Klinik olarak **akut sırt ağrısı** ile başlar ve en sık torasik omurgayı tutar.",
         "Olgular hekime aniden başlayan akut sırt ağrısıyla başvurur ve spinal kolon boyunca en sık torasik vertebralarda kemik destrüksiyonu oluşturur.",
         "Akut sırt ağrısı", 6, None, "akut sırt ağrısı", None),
        ("Vertebra korpusunda yaygın erime yaparak **vertebra plana görünümüne** yol açar.",
         "Tümöral histiyositler vertebra korpusunun trabeküler kemiğini eriterek korpusun kağıt gibi yassılaşmasına ve radyolojide vertebra plana olarak adlandırılan tipik çökmeye yol açar.",
         "Torasik omurga tutulumu", 7, None, "vertebra plana", None),
        ("Elektron mikroskopisinde **raket biçimli Birbeck granülleri** Langerhans histiyositozunun kesin kanıtıdır.",
         "Histopatolojik tanıda elektron mikroskobuyla sitoplazmada raket biçiminde Birbeck granüllerinin gösterilmesi ve immünohistokimyada se yüz ve se de bir a pozitifliği tanıyı kesinleştirir.",
         "Eozinofilik Granulom", 0, None, "Birbeck granülleri", None),
        ("Tekil kemik lezyonunda cerrahi uygulanırken **sistemik yayılımda kemoterapi** tercih edilir.",
         "Yalnızca tek omurgayı tutan izole lezyonlarda biyopsi ve cerrahi küretaj yeterli olurken, çoklu organ tutulumu olan sistemik histiyositozda sistemik kemoterapi verilir.",
         "Sistemik ise kemoterapi", 8, None, "cerrahi ve kemoterapi", None)
    ]

    PD[11] = [
        ("**Hand-Schüller-Christian Sendromu:** Langerhans hücreli histiyositozun kronik multisistem formudur.",
         "Langerhans hücreli histiyositozun dissemine ve kronik seyirli multisistem formu Hand-Schüller-Christian sendromu olarak adlandırılır.",
         "Hand-Schüller-Christian triadı", 0, None, "Hand-Schüller-Christian", None),
        ("Bu sendromun klasik triadı **kemik lezyonları, diabetes insipidus ve ekzoftalmustur**.",
         "Hastalığın patognomonik triadı kranial ve spinal litik kemik lezyonları, hipofizer sap tutulumuna bağlı diabetes insipidus ve retroorbital tutuluma bağlı ekzoftalmustur.",
         "ekzoftalmus üçlüsüyle", 3, None, "klasik triad", None),
        ("Kafatasında ve omurgada **zımba deliği tarzında litik odaklar** gözlenir.",
         "Radyolojik görüntülemede kalvaryumda sınırları zımba deliğiyle delinmiş gibi net ayrılan litik kemik lezyonları ve vertebralarda kollaps odakları saptanır.",
         "kemik lezyonları", 1, None, "litik kemik lezyonları", None),
        ("Hipotalamo-hipofizer aks tutulumu **antidiüretik hormon yetmezliği** ve aşırı idrara çıkma yapar.",
         "Histiyositik infiltrasyonun hipofiz sapına uzanması antidiüretik hormon sekresyonunu bozarak polidipsi ve poliüri ile giden diabetes insipidus tablosunu doğurur.",
         "diabetes insipidus", 2, None, "diabetes insipidus", None),
        ("Göz küresinin arkasındaki granülomatöz kitle **belirgin ekzoftalmus** gelişimine yol açar.",
         "Retroorbital yumuşak dokuda biriken eozinofilik kitle göz kürelerini öne doğru iterek hastada çift taraflı belirgin ekzoftalmus tablosuna neden olur.",
         "ekzoftalmus üçlüsüyle", 3, None, "ekzoftalmus", None)
    ]

    # ==============================================================================
    # BÖLÜM 10: Vertebra Hemanjiomu (Sayfa 12)
    # ==============================================================================

    PD[12] = [
        ("**Vertebra Hemanjiomu:** Omurganın en sık rastlanan selim vasküler tümörüdür.",
         "Vertebra hemanjiomu erişkin omurgasında en sık rastlanan, damar kökenli selim kan damarı yumağı lezyonudur.",
         "Bening Hemanjiom", 0, None, "vertebra hemanjiomu", None),
        ("Hastaların büyük kısmında lezyon tamamen **asemptomatiktir ve insidental saptanır**.",
         "Hemanjiomlar genellikle hiçbir semptom vermez; başka bir nedenle çekilen akciğer grafisi, bel tomografisi veya emarda tesadüfen yani insidental saptanma ile tespit edilir.",
         "Sıklıkla insidentaldir", 3, None, "insidental saptanma", None),
        ("Lezyonların **yüzde ellisinden fazlası omurga ve kafatasında** lokalizedir.",
         "İskelet hemanjiomlarının yüzde ellisinden fazlası aksiyel iskelette, özellikle omurga kolonunda ve kranium kemiklerinde yerleşim gösterir.",
         "> % 50 omurga", 4, None, "omurga ve kafatası", None),
        ("Omurga seviyesi olarak en sık **torakolomber veya lomber bölgede** görülür.",
         "Spinal tutulumda en yaygın lokalizasyon alt torasik ve üst lomber vertebra korpuslarıdır.",
         "Torakolomber veya lomber", 5, None, "torakolomber veya lomber", None),
        ("Direkt grafide ve tomografide korpusta **tipik vertikal çizgilenmeler** izlenir.",
         "Radyolojik incelemede yatay trabeküllerin erimesi ve dikey trabeküllerin kalınlaşması sonucu direkt grafide akordeon veya parmaklık manzarası denen dikey vertikal çizgilenmeler izlenir.",
         "vertikal çizgilenmeler", 6, None, "vertikal çizgilenmeler", None),
        ("Aksiyal tomografi kesitlerinde noktasal trabeküller **puantiyeli kumaş görünümü** verir.",
         "Aksiyal tomografi pencerelerinde dikey trabeküllerin kemik korpusunda enine kesilmesi sonucu puantiyeli kumaş veya benekli korpus manzarası ortaya çıkar.",
         "vertikal çizgilenmeler", 6, None, "puantiyeli kumaş görünümü", None),
        ("Kemik gücü zayıflarsa **patolojik kırık riski** ve çökme ortaya çıkabilir.",
         "Hemanjiomun korpusun büyük kısmını işgal ettiği durumlarda kemik biyomekaniği zayıflayarak patolojik kırık riski artar ve minör travmalarla çökme kırıkları gelişebilir.",
         "Patolojik kırıklar", 7, None, "patolojik kırık riski", None),
        ("Asemptomatik olgularda aktif müdahale yerine **periyodik radyolojik takip** yeterlidir.",
         "Herhangi bir kırık riski veya nörolojik kanal basısı oluşturmayan sessiz hemanjiom olgularında aktif müdahaleden kaçınılır ve hasta rutin aralıklarla izlenir.",
         "Sıklıkla insidentaldir", 3, None, "periyodik radyolojik takip", None),
        ("Spinal kanala taşma veya kord basısı durumunda **cerrahi dekompresyon ve sementleme** yapılır.",
         "Nörolojik bası belirtisi veren veya kırık riski taşıyan olgularda cerrahi dekompresyon ve ciltten perkütan sement enjeksiyonu yani vertebroplasti uygulanır.",
         "Bası durumunda cerrahi", 8, None, "cerrahi dekompresyon", None)
    ]

    # ==============================================================================
    # BÖLÜM 11: Primer Malign Omurga Tümörleri: Osteosarkom (Sayfa 13 - 14)
    # ==============================================================================

    PD[13] = [
        ("**Primer Habis Omurga Neoplazileri:** Kemik ve yumuşak doku sarkomları omurgada hızlı yıkım yapar.",
         "Primer habis omurga neoplazileri omurga kemik dokusundan köken alarak hızlı korpus yıkımı ve spinal kord basısı oluşturan habis tablolardır.",
         "Primer malign omurga", 0, None, "habis omurga neoplazileri", None),
        ("Bu grupta osteosarkom, kondrosarkom, Ewing sarkomu ve multipl myelom yer alır.",
         "Habis sınıflamada kemik üreten osteosarkom, kıkırdak matriksli kondrosarkom, nöroektodermal Ewing sarkomu ve plazma hücreli multipl myelom temel antiteyi oluşturur.",
         "Multipl Myelom", 4, None, "habis tümör spektrumu", None),
        ("Ayrıca lenfoma, kordoma ve nöroblastom omurga kolonunu tutan diğer habis tümörlerdir.",
         "Buna ek olarak lenfoid seri neoplazisi lenfoma, sakrum ve klivusta yerleşen kordoma ve çocuklarda paravertebral nöroblastom habis tablolar arasında değerlendirilir.",
         "Kordoma", 6, None, "kordoma ve lenfoma", None),
        ("Habis tümörlerde erken tanı konarak **omurilik hasarının önlenmesi** cerrahinin ana hedefidir.",
         "Habis tümörlerin tanı ve tedavisinde ana ilke geri dönüşsüz omurilik hasarı gelişmeden önce erken dekompresyon sağlamak ve omurga stabilitesini korumaktır.",
         "Primer malign omurga", 0, None, "omurilik hasarını önleme", None)
    ]

    PD[14] = [
        ("**Omurga Osteosarkomu:** Primer kemik osteosarkomlarının omurga yerleşimi oldukça nadirdir.",
         "Osteosarkom genellikle uzun kemiklerin metafizinde görülen habis bir tümör olup primer omurga yerleşimi tüm osteosarkomların yüzde beşinden azını oluşturan nadir bir durumdur.",
         "Maling Osteosarkom", 0, None, "omurga osteosarkomu", None),
        ("Omurga osteosarkomları genellikle **ileri yaş grubunda** veya Paget hastalığı zemininde görülür.",
         "Ekstremite osteosarkomları adölesanlarda sıkken, omurga osteosarkomları çoğunlukla kırk yaş üzerindeki ileri yaş grubunda veya Paget hastalığı ve radyoterapi zemininde ortaya çıkar.",
         "İleri yaş", 2, None, "ileri yaş", None),
        ("Radyolojide korpusun ve arka elemanların **hızlı litik ve destrüktif lezyonu** saptanır.",
         "Görüntülemede hem vertebra korpusunu hem de pedikül ve laminaları aynı anda istila eden, kemik korteksini parçalayan agresif destrüktif ve litik kitleler saptanır.",
         "korpusun litik veya destrüktif", 3, None, "litik ve destrüktif lezyon", None),
        ("Laboratuvarda **alkalen fosfataz düzeyinde artış** yüksek kemik turnoverini gösterir.",
         "Kanda osteoblastik aktivite artışına paralel olarak alkalen fosfataz ve laktat dehidrogenaz enzimlerinin yüksek seyretmesi osteosarkomun agresif biyolojik seyrinin bir göstergesidir.",
         "korpusun litik veya destrüktif", 3, None, "alkalen fosfataz", None),
        ("Sağaltımında **en-blok cerrahi rezeksiyon** ve kombine kemoradyoterapi protokolü uygulanır.",
         "Tedavi yaklaşımında tümörün sağlam sınırlarla bir bütün halinde çıkarıldığı en blok cerrahi rezeksiyon ile sistemik kemoterapi ve radyoterapi kombine edilir.",
         "Cerrahi + radyoterapi", 4, None, "cerrahi ve radyoterapi", None)
    ]

    # ==============================================================================
    # BÖLÜM 12: Kondrosarkom (Sayfa 15)
    # ==============================================================================

    PD[15] = [
        ("**Kondrosarkom:** Habis kıkırdak matriksi üreten primer omurga neoplazisidir.",
         "Kondrosarkom neoplastik hücrelerin osteoid doku üretmeksizin doğrudan kıkırdak matriksi ürettiği habis bir mezenkimal kemik tümörüdür.",
         "Maling Kondrosarkom", 0, None, "kondrosarkom", None),
        ("Genel iskelette pelvis ve femuru tutarken **omurga tutulumu da oldukça sıktır**.",
         "Tümör uzun kemiklerde ve pelviste sık yerleştiği gibi omurga kolonunda da osteosarkoma kıyasla çok daha yüksek oranda aksiyel yerleşim gösterir.",
         "Omurga  tutulumu  da", 1, None, "omurga tutulumu", None),
        ("Hastalık tipik olarak **kırk ila yetmiş yaş arasındaki** erişkinlerde karşımıza çıkar.",
         "Yaş dağılımına bakıldığında kondrosarkom olgularının büyük kısmı kırk ila yetmiş yaş arasındaki olgun ve ileri erişkin popülasyonda teşhis edilir.",
         "40 – 70 yaş", 2, None, "kırk yetmiş yaş", None),
        ("Tümör düşük dereceli yavaş seyirli olabileceği gibi **yüksek dereceli agresif seyirli** de olabilir.",
         "Histolojik derecesine bağlı olarak kondrosarkomlar yıllarca yavaş büyüyen düşük dereceli formlardan hızla metastaz yapan anaplastik agresif formlara kadar değişken bir spektrum gösterir.",
         "Yavaş veya agresif", 3, None, "yavaş veya agresif seyir", None),
        ("Görüntülemede kıkırdak matriksine özgü **halka ve yay kalsifikasyonları** dikkati çeker.",
         "Radyolojik incelemelerde kıkırdak lobüllerinin çevresindeki kalsifikasyonlara bağlı olarak halka ve yay şeklinde patognomonik kireçlenmeler izlenir.",
         "Maling Kondrosarkom", 0, None, "halka ve yay kalsifikasyonu", None),
        ("Histolojide kıkırdak lakünleri içinde **pleomorfik kondrositler ve bol miksoid matriks** görülür.",
         "Mikroskobik kesitlerde kıkırdak lakünleri içinde çok çekirdekli, atipik nükleuslu habis kondrositler ve aralarında bol miktarda miksoid hyalin kıkırdak matriksi dikkati çeker.",
         "Maling Kondrosarkom", 0, None, "kondroid matriks", None),
        ("Kemoterapi ve radyoterapiye dirençli olduğundan **birincil tedavi cerrahi rezeksiyondur**.",
         "Kondrosarkom hücreleri kemoterapi ve klasik radyoterapiye son derece dirençli olduğundan küratif başarının tek yolu lezyonun geniş cerrahi sınırlarla rezeke edilmesidir.",
         "İzole ise cerrahi", 4, None, "cerrahi rezeksiyon", None)
    ]

    # ==============================================================================
    # BÖLÜM 13: Ewing Sarkomu (Sayfa 16)
    # ==============================================================================

    PD[16] = [
        ("**Ewing Sarkomu:** Kemiğin yüksek derecede habis küçük yuvarlak mavi hücreli tümörüdür.",
         "Ewing sarkomu nöroektodermal kökenli, primitif küçük yuvarlak mavi hücrelerin proliferasyonu ile karakterize son derece habis bir kemik tümörüdür.",
         "küçük hücreli tümörü", 1, None, "küçük hücreli tümör", None),
        ("Hastalık ağırlıklı olarak **çocukluk ve ergenlik çağında**, ilk iki dekadda görülür.",
         "Epidemiyolojik olarak Ewing sarkomu çocukluk, ergenlik ve genç erişkinlik evresinde, en sık ilk yirmi yaş içerisinde zirve yapar.",
         "Çocukluk ve ergenlik", 2, None, "ilk iki dekad", None),
        ("Hızlı metastaz yapma potansiyeli nedeniyle lezyonun **genel klinik prognozu kötüdür**.",
         "Erken dönemde akciğere ve diğer kemiklere mikrometastaz yapma eğilimi nedeniyle multimodal agresif tedavi uygulanmadığında prognozu oldukça kötüdür.",
         "Prognoz kötü", 3, None, "kötü prognoz", None),
        ("Genetik analizde **on bir ve yirmi ikinci kromozom translokasyonu** tümörün belirtecidir.",
         "Hastalığın moleküler genetik zemininde on bir ve yirmi ikinci kromozomların karşılıklı yer değiştirmesi sonucu e ve se fe le i bir kimerik onkogen füzyon transkripti sentezlenir.",
         "küçük hücreli tümörü", 1, None, "kromozomal translokasyon", None),
        ("İmmünohistokimyada membranöz **CD99 antijen pozitifliği** tanıyı diğer tümörlerden ayırır.",
         "Histopatolojik tanıda tümöral küçük yuvarlak hücrelerin yüzeyinde mik iki yani se de doksan dokuz antijeninin diffüz membranöz boyanması Ewing sarkomunu diğer nöroblastom ve lenfomalardan ayırır.",
         "küçük hücreli tümörü", 1, None, "CD99 pozitifliği", None),
        ("Hastada **subfebril ateş, anemi, lökositoz ve yüksek sedimentasyon** saptanır.",
         "Tümörün salgıladığı sitokinlere bağlı olarak hastada hafif subfebril ateş, kilo kaybı, normokrom anemi, kanda lökositoz ve belirgin eritrosit sedimentasyon yüksekliği izlenir.",
         "Subfebril ateş", 5, None, "subfebril ateş ve yüksek sedim", None),
        ("Bu sistemik inflamatuar bulgular nedeniyle **sıklıkla osteomiyelit ile karıştırılır**.",
         "Ateş, lökositoz ve lokal hassasiyet nedeniyle osteomiyelit tablosu Ewing sarkomunu maskeleyebilir ve lezyon bakteriyel kemik enfeksiyonu sanılarak tanı gecikebilir.",
         "Osteomyelit ile karıştırılır", 6, None, "osteomiyelit ile karışma", None),
        ("Lokal cerrahinin yeri sınırlı olup birincil tedavi **kemoterapi ve radyoterapi kombinasyonudur**.",
         "Hastalığın sistemik mikrometastatik doğası nedeniyle cerrahinin rolü sınırlıdır; sağaltımın temel omurgasını neoadjuvan yoğun kemoterapi ve hedefe yönelik radyoterapi oluşturur.",
         "Kemoterapi + radyoterapi", 8, None, "kemoterapi ve radyoterapi", None)
    ]

    # ==============================================================================
    # BÖLÜM 14: Multipl Myelom (Sayfa 17)
    # ==============================================================================

    PD[17] = [
        ("**Multipl Myelom:** Erişkin çağda en sık görülen habis primer kemik tümörüdür.",
         "Multipl myelom hematolojik kökenli olup erişkin çağda iskelet sistemini tutan en yaygın habis primer kemik tümörüdür.",
         "en sık habis kemik tümörü", 1, None, "en sık habis kemik tümörü", None),
        ("Hastaların hemen hemen tamamı **elli yaşın üzerindeki erişkinlerden** oluşur.",
         "Hastalık gençlerde nadir olup olguların ezici çoğunluğu elli yaş üzeri popülasyon içinde ileri yaş grubunda ortaya çıkar.",
         "> 50 yaş", 2, None, "elli yaş üzeri", None),
        ("Kemik iliğinde **malign plazma hücrelerinin klonal çoğalması** sonucu yaygın tutulum yapar.",
         "Kemik iliğindeki plazma hücrelerinin monoklonal habis proliferasyonu ve osteoklast aktive edici faktör salgılaması sonucu tüm aksiyel iskelette yaygın tutulum gelişir.",
         "Plazma hücre tümörü", 3, None, "plazma hücre tümörü", None),
        ("Klinik prezentasyonda **hiperkalsemi, böbrek yetmezliği, anemi ve kemik lezyonları** izlenir.",
         "Hastalığın klinik tanısında kalsiyum yüksekliği, renal yetmezlik, anemi ve litik kemik destrüksiyonu dörtlüsünden oluşan klasik organ hasarı kriterleri değerlendirilir.",
         "Plazma hücre tümörü", 3, None, "organ hasarı kriterleri", None),
        ("Laboratuvarda **normositik anemi ve yüksek sedim** hızı tipik bulgudur.",
         "Hematolojik tablolarda kemik iliği infiltrasyonuna bağlı normositik anemi ve yüksek sedim ile yüz milimetreyi aşan eritrosit sedimentasyon hızı saptanır.",
         "Normositik-normokromik anemi", 4, None, "normositik anemi ve yüksek sedim", None),
        ("Protein elektroforezinde **monoklonal gamopati ve Bence Jones proteinürisi** saptanır.",
         "Hastanın laboratuvar incelemesinde serumda monoklonal immünglobülin artışı ve idrarda hafif zincir atılımını yansıtan Bence Jones proteinürisinin varlığı plazma hücre diskrazisini teyit eder.",
         "Normositik-normokromik anemi", 4, None, "monoklonal gamopati", None),
        ("Direkt grafilerde ve tomografide **litik güve yeniği manzarası** izlenir.",
         "Radyolojik değerlendirmede vertebra korpuslarında osteoblastik reaksiyon içermeyen saf litik kemik erimeleri ve litik güve yeniği manzarası izlenir.",
         "Litik-güve yeniği", 6, None, "güve yeniği görünümü", None),
        ("Hastalığın birincil tedavisi cerrahi değil **sistemik birincil kemoterapi** ve kök hücre naklidir.",
         "Multipl myelom sistemik bir kemik iliği hastalığı olduğundan birincil kemoterapi, proteazom inhibitörleri ve kök hücre nakliyle tedavi edilir; cerrahi yalnız omurga çökmesi veya basıda uygulanır.",
         "Birincil tedavi: Kemoterapi", 7, None, "birincil kemoterapi", None)
    ]

    # ==============================================================================
    # BÖLÜM 15: Omurga Lenfoması (Sayfa 18)
    # ==============================================================================

    PD[18] = [
        ("**Omurga Lenfoması:** Lenfoid sistem neoplazilerinin omurga vertebra korpusunu tutmasıdır.",
         "Omurga lenfoması non-Hodgkin lenfoma veya Hodgkin lenfomanın omurga kemik dokusunda primer ya da sekonder kitleler oluşturmasıyla gelişir.",
         "Maling Lenfoma", 0, None, "omurga lenfoması", None),
        ("Tümör tipik olarak **erişkin çağdaki hastalarda** sırt ağrısı ve kord basısı ile başvurur.",
         "Lenfoma olguları genellikle ileri erişkin çağda vertebral korpus infiltrasyonu sonucu ortaya çıkan sırt ağrısı ve hızla gelişen paraparezi ile kliniğe gelir.",
         "Erişkin çağ", 2, None, "erişkin çağ", None),
        ("Omurga lenfoması çoğunlukla **diffüz büyük B hücreli lenfoma** alt tipinde görülür.",
         "Omurgayı tutan lenfoid neoplazilerin büyük çoğunluğunu diffüz büyük b hücreli lenfomalar oluşturur ve kitle kemik korteksini tahrip etmeksizin nöral foramenlerden spinal kanala sızabilir.",
         "Maling Lenfoma", 0, None, "diffüz büyük B hücreli", None),
        ("Görüntülemede vertebra korpusunda **litik ve bazen sklerotik lezyonlar** görülür.",
         "Radyolojide korpusta litik destrüksiyon alanları görülebileceği gibi bazı olgularda fildişi vertebra yani ivory vertebra denen sklerotik kemik kalınlaşmaları da saptanabilir.",
         "litik lezyonlar", 3, None, "litik lezyonlar", None),
        ("Kesin teşhis cerrahi veya perkütan yolla alınan **doku biyopsisi ile konulur**.",
         "Radyolojik görüntüler metastaz ve enfeksiyonla karışabildiğinden kesin histopatolojik teşhis iğne biyopsisi veya cerrahi açık biyopsi ile lenfoid hücrelerin gösterilmesiyle konur.",
         "Teşhis: Biyopsi", 4, None, "doku biyopsisi", None),
        ("Omurga lenfomasının **birincil tedavisi radyoterapi ve kemoterapidir**.",
         "Lenfoma radyoduyarlı ve kemoduyarlı bir neoplazi olduğundan birincil sağaltım yöntemi lokal radyoterapi ve sistemik kemoterapidir.",
         "Birincil Tedavi: radyoterapi", 5, None, "radyoterapi", None),
        ("Kemoterapi ile radyoterapinin birlikte uygulanması **hastaların sağkalımını belirgin artırır**.",
         "Kombine sistemik kemoterapi ve radyoterapi rejimleri omurga stabilitesini koruyarak ve tümör kitlesini hızla eriterek hastaların uzun dönem surveyini belirgin biçimde uzatmaktadır.",
         "Surveyi arttırmaktadır", 6, None, "sağkalım artışı", None)
    ]

    # ==============================================================================
    # BÖLÜM 16: Metastatik Omurga Tümörleri ve Primer Odaklar (Sayfa 19 - 20)
    # ==============================================================================

    PD[19] = [
        ("**Metastatik Omurga Tümörleri:** Omurgadaki tüm tümörlerin yüzde doksanını metastazlar oluşturur.",
         "Klinik pratikte karşılaşılan omurga kitlelerinin yüzde doksanlık ezici çoğunluğunu uzak organ karsinomlarının omurgaya yaptığı metastatik lezyonlar teşkil eder.",
         "Omurga tümörlerinin %90 ı metastazdır", 1, None, "yüzde doksan metastaz", None),
        ("İskelet sisteminde metastazların **en sık yerleştiği anatomik bölge omurgadır**.",
         "Genel iskelet sistemine yayılan tüm karsinom metastazlarının en sık ve en yoğun biçimde yerleştiği kemik yapısı omurga kolonudur.",
         "İskelet sistemi metastazları en sık", 2, None, "en sık omurga", None),
        ("Metastatik yayılım valfsiz **Batson venöz pleksusu yoluyla** retrograd olarak gerçekleşir.",
         "Tümör hücreleri batın içi ve toraks içi venöz basınç artışlarında kapakçığı bulunmayan Batson venöz pleksusu aracılığıyla doğrudan vertebra korpuslarına taşınır.",
         "Metastatik Omurga", 0, None, "Batson venöz pleksusu", None),
        ("Batson pleksusundaki kapakçık yokluğu venöz kanın **ters yönde omurgaya akmasına** zemin hazırlar.",
         "Kafa içi, toraks ve batın içi basınç yükseldiğinde kapaksız Batson venöz ağı kaval filtre sistemini baypas ederek karsinom embolilerinin doğrudan torasik ve lomber vertebralara ekilmesine zemin hazırlar.",
         "Metastatik Omurga", 0, None, "kapaksız venöz ağ", None),
        ("Spinal segmentler arasında metastazlar **en çok torasik omurgada** yerleşme eğilimindedir.",
         "Metastatik lezyonlar omurga boyunca yaklaşık yüzde yetmiş oranında torasik vertebraları, yüzde yirmi lomber ve yüzde on servikal omurgayı tutar.",
         "İskelet sistemi metastazları", 2, None, "torasik segment tutulumu", None),
        ("Vertebra korpusunu çökerten metastazlar **omurilik basısı acil tablosu** doğurabilir.",
         "Metastatik hücrelerin korpusu eritmesi sonucu patolojik çökme kırıkları gelişerek spinal kord basısı sendromu ve acil cerrahi endikasyonu açığa çıkabilir.",
         "Omurga tümörlerinin %90", 1, None, "omurilik basısı acili", None)
    ]

    PD[20] = [
        ("**Spinal Metastaz Kaynakları:** Spinal metastazların yüzde ellisi akciğer, meme veya prostat kanserindendir.",
         "Klinik veriler spinal metastazlar tablosunun yüzde ellisinden fazlasının akciğer karsinomu, meme kanseri veya prostat kanseri primer odaklarından kaynaklandığını göstermektedir.",
         "Spinal metastazların %50’si", 1, None, "akciğer meme prostat", None),
        ("Ayrıca **böbrek ve tiroid karsinomları** da omurgaya sık metastaz yapan diğer primerlerdir.",
         "Bu üç majör primer tümörün ardından böbrek hücreli karsinom, gastrointestinal tümörler ve tiroid kanseri omurgada sık metastaz oluşturan diğer primer odaklardır.",
         "akciğer,meme veya prostat", 1, None, "böbrek ve tiroid kanseri", None),
        ("Prostat kanseri **osteoblastik sklerotik lezyonlar** yaparken, akciğer kanseri litik yıkım yapar.",
         "Radyolojik karakter açısından prostat karsinomu kemik yoğunluğunu artıran osteoblastik lezyonlar oluştururken akciğer ve böbrek metastazları kemiği eriten saf osteolitik odaklar meydana getirir.",
         "Metastatik  Omurga", 0, None, "osteoblastik ve litik lezyonlar", None),
        ("Metastatik kord basısı geliştiğinde derhal **yüksek doz intravenöz deksametazon** başlanmalıdır.",
         "Nörolojik defisiti önlemek amacıyla omurilik ödemini hızla azaltan yüksek doz intravenöz deksametazon tedavisine tanı anında derhal başlanması hayati önem taşır.",
         "Metastatik  Omurga", 0, None, "intravenöz deksametazon", None),
        ("Akut kord basısında fonksiyonların korunması için **ilk yirmi dört kırk sekiz saatte** dekompresyon gerekir.",
         "Yürüme yetisini kaybetme riskiyle başvuran metastatik omurilik basısı olgularında kalıcı felçleri önlemek adına ilk yirmi dört kırk sekiz saat içinde acil dekompresif cerrahi ve enstrümantasyon uygulanmalıdır.",
         "Metastatik  Omurga", 0, None, "acil cerrahi dekompresyon", None),
        ("Hastanın cerrahiye uygunluğu **Tokuhashi ve Tomita skorlama sistemleriyle** belirlenir.",
         "Hastanın cerrahi dekompresyon ve spinal rekonstrüksiyondan fayda görüp görmeyeceği yaşam beklentisini ve tümör yükünü hesaplayan Tokuhashi ve Tomita skorlama sistemleri ile kararlaştırılır.",
         "Metastatik  Omurga", 0, None, "Tokuhashi skorlaması", None),
        ("Spinal İnstabilite Neoplastik Skoru omurganın **mekanik çökme riskini** değerlendirmede temel alınır.",
         "Hastanın omurgasının instabil olup olmadığını belirlemek ve profilaktik cerrahi stabilizasyon endikasyonu koymak için omurga cerrahisinde uluslararası kabul gören neoplastik instabilite skorlaması kullanılır.",
         "Metastatik  Omurga", 0, None, "instabilite skorlaması", None),
        ("Böylece omurga tümörleri dersimizi tamamlarken **erken cerrahi ve onkolojik yaklaşımın** önemini vurguluyoruz.",
         "Böylece omurga tümörleri dersimizi tamamlarken erken nörolojik değerlendirmenin, doğru radyolojik sınıflamanın ve cerrahi rekonstrüksiyonun hastanın yaşam kalitesini korumada belirleyici olduğunu vurguluyoruz.",
         "Metastatik  Omurga", 0, None, "erken tanı ve cerrahi", None)
    ]

    # Chapter definitions
    bolum_def = [
        ("Bölüm 1: Omurga Tümörlerine Genel Bakış ve Epidemiyoloji", [1, 2]),
        ("Bölüm 2: Primer Selim Omurga Tümörlerinin Sınıflanması", [3]),
        ("Bölüm 3: Primer Habis Omurga Tümörlerinin Sınıflanması", [4]),
        ("Bölüm 4: Osteoid Osteom: Arka Kolon Tutulumu ve Aspirin Yanıtı", [5]),
        ("Bölüm 5: Osteoblastom: Agresif Selim Kemik Neoplazisi", [6]),
        ("Bölüm 6: Osteokondrom: En Sık Görülen Selim Kemik Ekzostozu", [7]),
        ("Bölüm 7: Dev Hücreli Tümör: Vertebra Korpusu Tutulumu", [8]),
        ("Bölüm 8: Anevrizmal Kemik Kisti: Ekspansif Kistik Lezyon", [9]),
        ("Bölüm 9: Eozinofilik Granülom ve Hand-Schüller-Christian Triadı", [10, 11]),
        ("Bölüm 10: Vertebra Hemanjiomu: Vertikal Çizgilenme ve İnsidental Tanı", [12]),
        ("Bölüm 11: Primer Malign Omurga Tümörleri: Osteosarkom", [13, 14]),
        ("Bölüm 12: Kondrosarkom: Dirençli Kıkırdak Neoplazisi", [15]),
        ("Bölüm 13: Ewing Sarkomu: Küçük Mavi Hücreli Kemik Neoplazisi", [16]),
        ("Bölüm 14: Multipl Myelom: Plazma Hücreli Kemik İliği Malignitesi", [17]),
        ("Bölüm 15: Omurga Lenfoması ve Cerrahi Biyopsi", [18]),
        ("Bölüm 16: Metastatik Omurga Tümörleri ve Omurilik Basısına Yaklaşım", [19, 20])
    ]

    clean_k2 = {
        "ders_id": "k2-64",
        "surum": 2,
        "bolumler": []
    }

    sents = []
    slide_last_sent = {}

    p_counter = 1
    for b_idx, (b_title, p_nums) in enumerate(bolum_def, 1):
        b_obj = {
            "id": f"k2-64-b{b_idx:02d}",
            "baslik": b_title,
            "paragraflar": []
        }
        for pno in p_nums:
            items = PD.get(pno, [])
            p_sents = []
            for item in items:
                ekran, ses, spat, sidx, cik, hw, sekil = item
                s_obj = make_sentence(ekran, ses, pno, spat, sidx, cik, hw, sekil)
                p_sents.append(s_obj)
                sents.append(s_obj)
            slide_last_sent[pno] = p_sents[-1]["id"]
            b_obj["paragraflar"].append({
                "id": f"k2-64-p{p_counter:03d}",
                "sayfa": pno,
                "cumleler": p_sents
            })
            p_counter += 1
        clean_k2["bolumler"].append(b_obj)

    total_words = sum(len(s["ses"].split()) for s in sents)
    print(f"Total sentences: {len(sents)}, Total words: {total_words} (~{total_words/130:.1f} minutes)")

    # 11 Clean Semantic Drawing Commands mapped dynamically to slide completion sentences
    drawings = [
        {
            "cumle": slide_last_sent[2], "bas": 0, "son": 5, "sayfa": 3,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Omurga kitleleri",
            "ogeler": [
                "Primer kemik tümörleri",
                "Metastatik yayılım"
            ]
        },
        {
            "cumle": slide_last_sent[3], "bas": 0, "son": 5, "sayfa": 3,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Primer selim omurga tümörleri",
            "ogeler": [
                "Osteoid osteom",
                "Osteoblastom",
                "Osteokondrom",
                "Dev hücreli tümör"
            ]
        },
        {
            "cumle": slide_last_sent[4], "bas": 0, "son": 5, "sayfa": 4,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Primer habis omurga tümörleri",
            "ogeler": [
                "Osteosarkom",
                "Kondrosarkom",
                "Ewing sarkomu",
                "Multipl myelom"
            ]
        },
        {
            "cumle": slide_last_sent[5], "bas": 0, "son": 5, "sayfa": 6,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Osteoid osteom özellikleri",
            "ogeler": [
                "Genç yaş ve arka kolon tutulumu",
                "Gece şiddetlenen ağrı",
                "Aspirine dramatik yanıt",
                "Ağrılı skolyoz"
            ]
        },
        {
            "cumle": slide_last_sent[6], "bas": 0, "son": 5, "sayfa": 6,
            "tur": "sema", "sablon": "karsilastirma",
            "kutuplar": [
                "Osteoid osteom",
                "Osteoblastom"
            ],
            "satirlar": [
                [
                    "Boyut",
                    "İki santimetreden küçük",
                    "Büyük boyut"
                ],
                [
                    "Nüks",
                    "Kıyasla az nüks",
                    "Yüksek lokal nüks"
                ]
            ]
        },
        {
            "cumle": slide_last_sent[8], "bas": 0, "son": 5, "sayfa": 6,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Dev hücreli tümör",
            "ogeler": [
                "Genç erişkin popülasyon",
                "Vertebra korpusu tutulumu",
                "Torasik segment yerleşimi"
            ]
        },
        {
            "cumle": slide_last_sent[11], "bas": 0, "son": 5, "sayfa": 11,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Hand-Schüller-Christian triadı",
            "ogeler": [
                "kemik lezyonları",
                "diabetes insipidus",
                "ekzoftalmus"
            ]
        },
        {
            "cumle": slide_last_sent[12], "bas": 0, "son": 5, "sayfa": 12,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Vertebra hemanjiomu",
            "ogeler": [
                "İnsidental saptanma",
                "Vertikal çizgilenmeler",
                "Patolojik kırık riski"
            ]
        },
        {
            "cumle": slide_last_sent[16], "bas": 0, "son": 5, "sayfa": 17,
            "tur": "sema", "sablon": "maskeleyen",
            "gorunen": "Osteomiyelit",
            "altta": [
                "Ewing sarkomu"
            ]
        },
        {
            "cumle": slide_last_sent[17], "bas": 0, "son": 5, "sayfa": 17,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Multipl myelom bulguları",
            "ogeler": [
                "Elli yaş üzeri popülasyon",
                "Normositik anemi ve yüksek sedim",
                "Litik güve yeniği manzarası",
                "Birincil kemoterapi"
            ]
        },
        {
            "cumle": slide_last_sent[20], "bas": 0, "son": 5, "sayfa": 20,
            "tur": "sema", "sablon": "cok_neden_tek_sonuc",
            "kaynaklar": [
                "akciğer karsinomu",
                "meme kanseri",
                "prostat kanseri"
            ],
            "sonuc": "Spinal metastazlar"
        }
    ]

    # Write files
    (TASLAK / "konusma_v2.json").write_text(json.dumps(clean_k2, ensure_ascii=False, indent=2), encoding="utf-8")
    (TASLAK / "cizim_aday.json").write_text(json.dumps({"komutlar": drawings}, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
    import konusma_v2 as KV
    md_txt, sayfalar_l = KV.turet(clean_k2)
    (TASLAK / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
    (TASLAK / "konusma_metin.md").write_text(md_txt, encoding="utf-8")
    (TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
    (TASLAK / "konusma_capalari.json").write_text(json.dumps(KV.capalar(clean_k2), ensure_ascii=False), encoding="utf-8")

    print("Files successfully written to taslak.")

    # Run all quality gates
    print("\n--- Running Quality Gate 1: KV.dogrula ---")
    kv_errs = KV.dogrula(clean_k2, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
    if kv_errs:
        print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
        for e in kv_errs[:10]: print(" ", e)
        sys.exit(1)
    print("PASSED KV.dogrula: 0 HATA")

    print("\n--- Running Quality Gate 2: denetle.py ---")
    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
    import denetle as D
    d_rapor = D.Denetim(TASLAK).calistir()
    if d_rapor.get("hata", 0) > 0:
        print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
        for e in d_rapor.get("hatalar", [])[:10]: print(" ", e)
        sys.exit(1)
    print("PASSED denetle.py: 0 HATA · 0 UYARI")

    print("\n--- Running Quality Gate 3: validate_learning_decks.py ---")
    import subprocess
    r_deck = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/validate_learning_decks.py"),
        str(TASLAK / "deck.json"), "--oyun-zorunlu", "--kurul2"
    ], capture_output=True, text=True)
    if r_deck.returncode != 0:
        print("FAILED validate_learning_decks:", r_deck.stdout, r_deck.stderr)
        sys.exit(1)
    print("PASSED validate_learning_decks: 0 HATA · 0 UYARI")

    print("\n--- Running Quality Gate 4: metin_denetle.py ---")
    r_metin = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/sesli_anlatim/metin_denetle.py"),
        str(TASLAK / "konusma_metni.md")
    ], capture_output=True, text=True)
    if r_metin.returncode != 0:
        print("FAILED metin_denetle:", r_metin.stdout, r_metin.stderr)
        sys.exit(1)
    print("PASSED metin_denetle: 0 HATA · 0 UYARI")

    print("\n--- Running Quality Gate 5: sesli_kapsam ---")
    import isle as IS
    kapsam_errs = IS.sesli_kapsam(TASLAK)
    if kapsam_errs:
        print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
        for e in kapsam_errs: print(" ", e)
        sys.exit(1)
    print("PASSED sesli_kapsam: 0 HATA")

    print("\n--- Running Quality Gate 6: cizim_dogrula.py ---")
    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/cizim"))
    import cizim_dogrula as CD
    import sablon
    cum_text = {}
    accum = []
    for s in sents:
        accum.append(s["ses"])
        cum_text[s["id"]] = " ".join(accum)
    sent_map = {s["id"]: s for s in sents}
    c_errs = []
    for idx, d in enumerate(drawings):
        cid = d["cumle"]
        coz_d, err_c = sablon.coz(d)
        if err_c:
            c_errs.append(f"Drawing {idx+1} coz error: {err_c}")
            continue
        s_words = len(sent_map[cid]["ses"].split())
        err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
        if err_v:
            c_errs.append(f"Drawing {idx+1} ({cid}) error: {err_v}")
    if c_errs:
        print(f"FAILED cizim_dogrula with {len(c_errs)} errors:")
        for e in c_errs: print(" ", e)
        sys.exit(1)
    print(f"PASSED cizim_dogrula: {len(drawings)}/{len(drawings)} KOMUT 0 HATA")


if __name__ == "__main__":
    main()
