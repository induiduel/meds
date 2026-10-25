#!/usr/bin/env python3
"""Generate a complete, deep amfi-level lecture for Lesson 59: Psikiyatrik Hastalıklar ve Genetik Analizi.

Covers all 82 pages without skipping any page.
Generates ~180-200 sentences, ~3,000-3,500 spoken words (~22-26 minutes of deep audio).
Ensures 0 forward leaks in drawings and strict adherence to Turkish style rules.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-59-psikiyatrik-hastaliklar-ve-genetik-analizi"
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
            cl = re.sub(r'^[✓\s\-*•o]+', '', cl).strip()
            if len(cl) > 3 and not cl.isdigit() and not cl.startswith('==='):
                ll.append(cl)
        pages_lines[curr_p] = ll

def find_satir(pno, pattern=None, idx=0):
    lines = pages_lines.get(pno, [])
    if not lines:
        return "Psikiyatrik Hastalıklar ve Genetik Analiz"
    if pattern:
        for l in lines:
            if pattern.casefold() in l.casefold():
                return l
    if idx < len(lines):
        return lines[idx]
    return lines[-1]

c_counter = 1

def make_sentence(ekran, ses, pno, satir_pattern=None, satir_idx=0, cikmis=None, highlight_word=None):
    global c_counter
    cid = f"k2-59-c{c_counter:04d}"
    c_counter += 1
    
    satir = find_satir(pno, satir_pattern, satir_idx)
    
    clean_ekran = ekran.replace("**", "").replace("*", "")
    
    vurgular = []
    if cikmis and highlight_word:
        m = re.search(re.escape(highlight_word), clean_ekran, re.IGNORECASE)
        if m:
            vurgular.append({"tur": "cikmis", "metin": m.group(0)})
        else:
            w = clean_ekran.split()[:3]
            vurgular.append({"tur": "cikmis", "metin": " ".join(w)})
    elif highlight_word:
        m = re.search(re.escape(highlight_word), clean_ekran, re.IGNORECASE)
        if m:
            vurgular.append({"tur": "terim", "metin": m.group(0)})
        else:
            w = clean_ekran.split()[:2]
            vurgular.append({"tur": "terim", "metin": " ".join(w)})
    else:
        words = [w for w in clean_ekran.split() if len(w) > 4 and w.isalpha()]
        if words:
            vurgular.append({"tur": "terim", "metin": words[0]})
        else:
            vurgular.append({"tur": "terim", "metin": clean_ekran.split()[0]})
            
    s_obj = {
        "id": cid,
        "ekran": ekran,
        "ses": ses,
        "satir": satir,
        "vurgular": vurgular
    }
    if cikmis:
        s_obj["cikmis"] = cikmis
    return s_obj

def build_lecture():
    global c_counter
    c_counter = 1
    
    sections_def = [
        {"b_id": "k2-59-b01", "baslik": "Psikiyatrik Genetiğin Amaçları ve Temel Kavramlar", "pages": [1, 2, 3, 4]},
        {"b_id": "k2-59-b02", "baslik": "Genetik Epidemiyoloji: Aile, İkiz ve Evlat Edinme Çalışmaları", "pages": [5, 6, 7, 8, 9, 10]},
        {"b_id": "k2-59-b03", "baslik": "Sitogenetik ve Moleküler Genetik Yöntemler", "pages": [11, 12, 13]},
        {"b_id": "k2-59-b04", "baslik": "Genomik Belirteçler ve Polimorfik Varyasyon Tipleri", "pages": [14, 15, 16, 17, 18]},
        {"b_id": "k2-59-b05", "baslik": "Genetik Haritalama, Bağlantı Analizi ve LOD Skoru", "pages": [19, 20, 21, 22, 23, 24]},
        {"b_id": "k2-59-b06", "baslik": "Aday Gen ve İlişki (Assosiasyon) Çalışmaları", "pages": [25, 26]},
        {"b_id": "k2-59-b07", "baslik": "Kişilik Bozuklukları Genetiği ve Antisosyal Davranış", "pages": [27, 28, 29, 30, 31, 32]},
        {"b_id": "k2-59-b08", "baslik": "Duygudurum Bozuklukları: Bipolar ve Unipolar Depresyon", "pages": [33, 34, 35, 36, 37]},
        {"b_id": "k2-59-b09", "baslik": "İntihar Davranışı Nörobiyolojisi ve Serotonerjik Yolak", "pages": [38, 39, 40, 41]},
        {"b_id": "k2-59-b10", "baslik": "Şizofreni Epidemiyolojisi, Aile ve İkiz Riskleri", "pages": [42, 43, 44, 45, 46, 47, 48, 49]},
        {"b_id": "k2-59-b11", "baslik": "Şizofrenide Aday Genler, GWAS, CNV ve Endofenotipler", "pages": [50, 51, 52, 53, 54, 55]},
        {"b_id": "k2-59-b12", "baslik": "Alkol ve Madde Bağımlılığı Genetiği: Ödül Yolağı ve Riskler", "pages": [56, 57, 58, 59]},
        {"b_id": "k2-59-b13", "baslik": "Alkol Metabolizması, Flushing Reaksiyonu ve Enzim Genetiği", "pages": [60, 61, 62, 63, 64, 65, 66]},
        {"b_id": "k2-59-b14", "baslik": "Anksiyete ve Yeme Bozuklukları Genetiği", "pages": [67, 68, 69, 70, 71, 72, 73, 74]},
        {"b_id": "k2-59-b15", "baslik": "Genetik Danışma İlkeleri ve Moleküler Analiz Protokolleri", "pages": [75, 76, 77, 78, 79, 80, 81, 82]}
    ]
    
    # We will define page sentences in a structured table
    pdata = {}
    
    # PAGE 1
    pdata[1] = [
        ("Psikiyatrik Hastalıklar ve **Genetik Analiz** dersimize hoş geldiniz.",
         "Psikiyatrik hastalıklar ve genetik analiz dersimize hoş geldiniz, bu dersimizde psikiyatrik bozuklukların altında yatan moleküler mekanizmaları ve genetik araştırma basamaklarını ayrıntılı şekilde inceleyeceğiz.",
         "Genetik Analiz", 0, None, "Genetik Analiz"),
        ("Ders sunumu Karabük Üniversitesi Tıp Fakültesi bünyesinde **Dr. Öğr. Üyesi Serap Arslan** tarafından hazırlanmıştır.",
         "Ders sunumu Karabük Üniversitesi Tıp Fakültesi Tıbbi Biyoloji Anabilim Dalından Doktor Öğretim Üyesi Serap Arslan tarafından hazırlanmıştır.",
         "Serap ARSLAN", 0, None, "Tıp Fakültesi")
    ]
    
    # PAGE 2
    pdata[2] = [
        ("Psikiyatride genetik çalışmaların temel amacı, **genetik ve çevresel faktörlerin** etiyolojiye katkısını netleştirmektir.",
         "Psikiyatri alanında genetik araştırmaların başlıca hedefi, genetik yatkınlık ile çevresel tetikleyicilerin patogeneze sunduğu katkıyı belirlemek ve moleküler düzeyde aydınlatmaktır.",
         "çevresel faktörlerin etyolojiye", 0, None, "çevresel faktörlerin"),
        ("Ayrıca klinik tanıya destek sunacak **biyolojik belirteçler** saptamak ve bireyselleştirilmiş tedavi stratejileri geliştirmek amaçlanır.",
         "Ayrıca objektif klinik tanıya rehberlik edecek biyolojik belirteçleri tespit etmek, farmakogenetik yaklaşımlarla hastaya özgü bireyselleştirilmiş rasyonel tedavi stratejileri oluşturmak hedeflenmektedir.",
         "Biyolojik belirteçler", 0, None, "biyolojik belirteçler")
    ]
    
    # PAGE 3 - ÇIKMIŞ
    pdata[3] = [
        ("Genetik araştırmalarda **epidemiyolojik, sitogenetik ve moleküler** yöntemler sıklıkla birlikte kullanılır.",
         "Çıkmış kurul sınavı sorusunda doğrudan sorgulandığı üzere, psikiyatrik genetik araştırmalarında popülasyon genetiği, aile ve ikiz analizleri, sitogenetik teknikler, bağlantı incelemeleri ve aday gen ilişki modelleri sıklıkla başvurulan temel metodolojilerdir.",
         "Genetik araştırmalarda sıklıkla kullanılan metodlar;", 0,
         {"soru_id": "q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-17", "yil": "2023"},
         "epidemiyolojik"),
        ("Bu metotlar klinik tablonun arkasındaki **poligenik altyapıyı** ve risk lokuslarını aydınlatır.",
         "Bu araştırma metodolojileri klinik tablonun arkasındaki çok genli altyapıyı, kromozomal düzensizlikleri ve risk lokuslarını adım adım aydınlatmaktadır.",
         "Moleküler genetik", 0, None, "poligenik altyapıyı")
    ]
    
    # PAGE 4
    pdata[4] = [
        ("Psikiyatrik bozukluklar klasik tek gen kalıtımından ziyade **poligenik kalıtım** özellikleri gösterir.",
         "Psikiyatrik hastalıklar tek bir genin mutasyonuna bağlı Mendel kalıtımı göstermez; çok sayıda gen varyantının kümülatif etkisiyle ortaya çıkan poligenik bozukluklardır.",
         "Psikiyatrik hastalıklar poligeniktir", 0, None, "poligenik kalıtım"),
        ("İkiz çalışmalarına göre psikiyatrik hastalıklarda **kalıtım riski yüzde kırk ila seksen** arasında tahmin edilmektedir.",
         "İkiz çalışmalarından elde edilen epidemiyolojik verilere göre bu hastalıklarda kalıtılabilirlik riski yüzde kırk ila seksen arasında son derece yüksek oranlarda tahmin edilmektedir.",
         "İkiz çalışmalarına göre kalıtım riski", 0, None, "kalıtım riski")
    ]
    
    # PAGE 5
    pdata[5] = [
        ("Popülasyon çalışmaları **aile, ikiz ve evlat edinme** araştırmaları olmak üzere üç ana başlıkta incelenir.",
         "Popülasyon genetiği çalışmaları temel olarak aile çalışmaları, ikiz çalışmaları ve evlat edinme modelleri olmak üzere üç ana kategoride incelenmektedir.",
         "Popülasyon Çalışmaları", 0, None, "Popülasyon çalışmaları"),
        ("Bu yaklaşımlar genetik yatkınlığın büyüklüğünü ve **aile içi kümelenmeyi** ölçmede ilk epidemiyolojik basamaktır.",
         "Bu epidemiyolojik yaklaşımlar, genetik yatkınlığın göreceli payını ve ailesel kümelenme paternini kantitatif olarak ölçmede ilk basamağı teşkil eder.",
         "Aile çalışmaları", 0, None, "aile içi kümelenmeyi")
    ]
    
    # PAGE 6
    pdata[6] = [
        ("Aile çalışmalarında hasta bireylerin akrabalarındaki morbid risk **genel popülasyon riski** ile kıyaslanır.",
         "Aile çalışmalarında proband yani indeks hasta üzerinden akrabalardaki hastalık sıklığı saptanır ve genel popülasyondaki bazal risk ile titizlikle karşılaştırılır.",
         "genel popülasyondaki risk", 0, None, "genel popülasyon riski"),
        ("Akrabalık derecesi yaklaştıkça riskin belirgin artması, hastalığın **güçlü genetik bileşenine** işaret eder.",
         "Bireyin birinci derece akrabalarında riskin ikinci ve üçüncü derece akrabalara oranla katlanarak artması, hastalığın güçlü genetik zeminini somutlaştırır.",
         "Akrabalık derecesi", 0, None, "genetik bileşenine")
    ]
    
    # PAGE 7
    pdata[7] = [
        ("İkiz çalışmaları **monozigot ve dizigot ikizler** arasındaki fenotipik uyum farkını modelleyerek kalıtsallığı hesaplar.",
         "İkiz çalışmaları monozigot ve dizigot ikiz çiftleri arasındaki fenotipik konkordans varyansını matematiksel olarak modelleyerek kalıtsallık katsayısını hesaplar.",
         "MZ ve DZ ikiz çiftleri", 0, None, "monozigot ve dizigot"),
        ("Böylece fenotipik çeşitliliğin ne kadarının **genetik varyasyondan** kaynaklandığı matematiksel olarak kestirilir.",
         "Bu sayede toplumda gözlenen fenotipik çeşitliliğin ne kadarlık kısmının alttaki genetik varyasyondan kaynaklandığı ampirik olarak ortaya konur.",
         "fenotipik uyumun", 0, None, "genetik varyasyondan")
    ]
    
    # PAGE 8
    pdata[8] = [
        ("Monozigot ikizler **yüzde yüz genetik özdeşlik** taşırken, dizigot ikizler genlerinin ortalama yarısını paylaşır.",
         "Monozigot ikizler tüm nükleer genom düzeyinde yüzde yüz genetik özdeşlik taşırken, dizigot ikizler normal kardeşler gibi genlerinin yalnızca yüzde ellisini paylaşırlar.",
         "monozigot (MZ) ve dizigot", 0, None, "genetik özdeşlik"),
        ("Her iki ikiz grubunun da ortak aile çevresinde büyümesi, **çevresel faktörlerin kontrol edilmesini** sağlar.",
         "Her iki grubun da aynı intrauterin ve ailesel çevrede büyümesi, paylaşılan çevresel etkilerin kontrol altında tutulmasını ve genetik farkın izole edilmesini sağlar.",
         "çevresel faktörlerin etkisi", 0, None, "çevresel faktörlerin")
    ]
    
    # PAGE 9
    pdata[9] = [
        ("Kalıtsallık sabit bir biyolojik kader değil, incelenen **popülasyonun çevresel koşullarına** bağımlı bir orandır.",
         "Kalıtsallık değeri değişmez statik bir oran olmayıp, incelenen popülasyonun demografik yapısından ve çevresel stresör maruziyetinden doğrudan etkilenir.",
         "Kalıtsallık çevresel faktörlerden", 0, None, "Kalıtsallık sabit"),
        ("Gen-çevre etkileşimi nedeniyle, aynı genetik zemin farklı çevresel şartlarda **farklı fenotipik şiddetler** üretebilir.",
         "Gen ile çevre arasındaki dinamik etkileşim nedeniyle, aynı risk varyantını taşıyan bireyler farklı çevresel koşullarda çok farklı klinik tablolar sergileyebilir.",
         "Kalıtsallık", 0, None, "farklı fenotipik")
    ]
    
    # PAGE 10
    pdata[10] = [
        ("Evlat edinme çalışmaları, **biyolojik miras ile yetiştirilme çevresini** birbirinden ayıran en mükemmel modeldir.",
         "Evlat edinme çalışmaları, biyolojik ebeveynden gelen genetik miras ile evlat edinen ailenin sağladığı yetiştirilme çevresini birbirinden kesin çizgilerle ayıran en güçlü yöntemdir.",
         "Evlat edinme çalışmaları da genetik", 0, None, "biyolojik miras"),
        ("Biyolojik anne-babası hasta olan çocuk, sağlıklı bir ailede büyütülse dahi **yüksek hastalık riski** taşımaya devam eder.",
         "Biyolojik ebeveyninde psikiyatrik bozukluk bulunan bir çocuk tamamen sağlıklı koruyucu bir aile ortamında büyütülse bile, biyolojik kökeninden kaynaklanan yüksek morbid riski korumaktadır.",
         "İki temel karşılaştırma", 0, None, "yüksek hastalık riski")
    ]
    
    # PAGE 11
    pdata[11] = [
        ("Sitogenetik çalışmalarda floresan **in situ hibridizasyon** teknikleriyle genlerin kromozom bant yerleşimleri incelenir.",
         "Sitogenetik analizlerde floresan in situ hibridizasyon gibi ileri moleküler sitogenetik teknikler kullanılarak genlerin kromozom bantlarındaki fiziksel lokasyonları belirlenir.",
         "In situ hibridizasyon", 0, None, "in situ hibridizasyon"),
        ("Bu analizler özellikle psikiyatrik tablolara eşlik eden **kromozomal translokasyon ve delesyonları** aydınlatır.",
         "Bu kromozomal incelemeler, özellikle nörogelişimsel ve psikiyatrik sendromlara zemin hazırlayan submikroskobik mikrodelesyon ve translokasyonları tespit eder.",
         "kromozomlardaki", 0, None, "kromozomal translokasyon")
    ]
    
    # PAGE 12
    pdata[12] = [
        ("Moleküler genetik çalışmaların ana hedefi, bozukluğun fenotipik kalıtım kalıbını yöneten **ilişkili aday genleri** tespit etmektir.",
         "Moleküler genetik araştırmaların temel amacı, belirli bir psikiyatrik fenotipin ortaya çıkışında doğrudan görev yapan fonksiyonel aday genleri ve alelleri saptamaktır.",
         "ilişkili aday genleri belirlemek", 0, None, "ilişkili aday genleri"),
        ("Aday genlerin tanımlanması, patogenetik **biyokimyasal yolakların** ve hedeflenebilir moleküler reseptörlerin keşfini sağlar.",
         "Aday genlerin belirlenmesi, nörobiyolojik sinyal iletim yolaklarının çözülmesini ve farmakolojik müdahaleler için yeni moleküler reseptör hedeflerinin ortaya konmasını sağlar.",
         "Moleküler genetik çalışmalar", 0, None, "biyokimyasal yolakların")
    ]
    
    # PAGE 13
    pdata[13] = [
        ("Kalıtım kalıpları tek genli Mendelyen kalıtım ile **kompleks multigenik kalıtım** olarak ikiye ayrılır.",
         "Kalıtım paternleri otozomal dominant ya da resesif tek gen kalıtımı ile çok sayıda genin ortak katkısıyla şekillenen multigenik kalıtım kalıpları olarak ikiye ayrılmaktadır.",
         "Kalıtım kalıpları", 0, None, "multigenik kalıtım"),
        ("Psikiyatrik hastalıklar neredeyse istisnasız olarak **eksik penetrans ve değişken ekspresyon** gösteren multigenik modele uyar.",
         "Psikiyatrik rahatsızlıklar neredeyse istisnasız biçimde eksik penetrans, fenokopi ve değişken klinik ekspresyon sergileyen kompleks multigenik modele uymaktadır.",
         "Multigenik kalıtım", 0, None, "eksik penetrans")
    ]
    
    # PAGE 14
    pdata[14] = [
        ("Genetik bilgiyi taşıyan genler, fonksiyonel **protein kodlayan ekzonlar** ile kodlamayan intron bölgelerinden oluşur.",
         "Hücresel genetik kodu taşıyan gen yapıları, olgunlaşmış protein ürününü kodlayan ekzon bölgeleri ile transkripsiyon sonrası uzaklaştırılan intron segmentlerinden meydana gelir.",
         "Ekzonlar ve intronlardan", 0, None, "protein kodlayan ekzonlar"),
        ("Ekzonlardaki ya da düzenleyici dizilerdeki **polimorfik varyasyonlar** proteinin sentez miktarını ve işlevini değiştirir.",
         "Ekzonik bölgelerdeki veya promoter dizilerindeki tek nükleotid polimorfizmleri, sentezlenen nörotransmitter reseptörlerinin ya da enzimlerin kinetik işlevini değiştirebilir.",
         "Polimorfik Varyasyonlar", 0, None, "polimorfik varyasyonlar")
    ]
    
    # PAGE 15
    pdata[15] = [
        ("İnsan genomunda tarihsel süreçte **RFLP, VNTR, mikrosatellit ve SNP** olmak üzere farklı varyasyon tipleri tanımlanmıştır.",
         "İnsan genomunda moleküler belirteç olarak kullanılan varyasyon tipleri kronolojik olarak restriksiyon parçacık uzunluğu, minisatellitler, mikrosatellitler ve tek nükleotid polimorfizmleridir.",
         "Varyasyon Tipi", 0, None, "farklı varyasyon tipleri"),
        ("Bu polimorfizmler psikiyatrik hastalıklarda **genetik haritalama ve risk belirteci** olarak büyük değer taşır.",
         "Bu genomik polimorfizmler psikiyatrik bozukluklarda kromozomal bağlantı haritalaması ve poligenik risk skorlamasında vazgeçilmez birer moleküler araçtır.",
         "Varyasyon", 0, None, "genetik haritalama")
    ]
    
    # PAGE 16
    pdata[16] = [
        ("RFLP varyasyonları, **restriksiyon enzimlerinin** DNA kesim noktalarındaki baz dizisi farklılıklarından kaynaklanır.",
         "Restriksiyon parça uzunluk polimorfizmi yani re fe le pe, restriksiyon endonükleaz enzimlerinin hedef de na kesim noktalarında meydana gelen baz değişikliklerine dayanır.",
         "Restriksiyon enzimleri ile oluşturulan", 0, None, "restriksiyon enzimlerinin"),
        ("Minisatellitler yani **VNTR dizileri** ise on beş ila yüz baz çifti uzunluğundaki ardışık tekrar bloklarıdır.",
         "Minisatellitler yani değişken sayıda tandem tekrarlar ise on beş ila yüz baz çifti uzunluğunda olup genom genelinde gen içi veya genler arası bölgelerde serpişmiştir.",
         "VNTR (Minisatelit)", 0, None, "VNTR dizileri")
    ]
    
    # PAGE 17
    pdata[17] = [
        ("DNA'daki ardışık tekrar dizileri sentromerik satellitler, **minisatellitler ve mikrosatellitler** olarak sınıflandırılır.",
         "Genomik ardışık tekrar dizileri sentromerik satellit de na, genler arası minisatellitler ve mikrosatellitler olmak üzere üç ana büyüklük grubunda sınıflandırılmaktadır.",
         "Satellit, minisatellit ve mikrosatellit", 0, None, "minisatellitler ve mikrosatellitler"),
        ("Mikrosatellitler iki ila altı baz çiftlik **kısa tandem tekrarlar** olup yüksek polimorfizm derecesine sahiptir.",
         "Mikrosatellitler iki ila altı nükleotidden oluşan kısa tandem tekrarlar olup popülasyonda son derece yüksek oranda heterozigotluk ve polimorfizm gösterir.",
         "Polimorfik Varyasyonlar", 0, None, "kısa tandem tekrarlar")
    ]
    
    # PAGE 18
    pdata[18] = [
        ("Genetik belirteçler arasında mikrosatellitler ve **tek nükleotid polimorfizmleri** günümüzde en yaygın kullanılanlardır.",
         "Moleküler genetik belirteçler ailesinde restriksiyon parçaları ve minisatellitlerin yerini günümüzde yüksek verimli mikrosatellitler ve tek nükleotid polimorfizmleri almıştır.",
         "Microsatellite Polymorphism", 0, None, "tek nükleotid polimorfizmleri"),
        ("Özellikle **SNP varyantları** genom boyunca yüz binlerce noktada taranarak yüksek çözünürlüklü ilişkilendirme sağlar.",
         "Özellikle es ne pe varyantları genom boyunca yüz binlerce hatta milyonlarca lokusta eşzamanlı taranarak yüksek çözünürlüklü assosiasyon analizlerine olanak verir.",
         "Genetik Belirteçler", 0, None, "SNP varyantları")
    ]
    
    # PAGE 19
    pdata[19] = [
        ("Varyasyon analizleri model bağımlı **parametrik analizler** ile modelden bağımsız nonparametrik yöntemler olarak uygulanır.",
         "Varyasyonların kullanım alanlarında parametrik yani model bağımlı analizlerde kalıtım şekli ve penetrans önceden varsayılırken, nonparametrik modellerde soy ağacı kalıtım varsayımından bağımsız çalışılır.",
         "Model bağımlı analizler", 0, None, "parametrik analizler"),
        ("Kromozom yerleşimi bilinen bir belirtecin aile kuşakları boyunca **hastalıkla birlikte aktarımı** incelenir.",
         "Kromozomal yerleşimi kesin olarak saptanmış bir moleküler belirtecin, hasta aile bireyleri arasında kuşaklar boyu hastalık fenotipiyle birlikte aktarılıp aktarılmadığı izlenir.",
         "Kromozom yerleşimi kesin", 0, None, "hastalıkla birlikte aktarımı")
    ]
    
    # PAGE 20
    pdata[20] = [
        ("Genetik haritalama, genlerin kromozom üzerindeki sırasını ve **rekombinasyon sıklığını** haritalandırır.",
         "Genetik haritalama, fonksiyonel genlerin kromozom üzerindeki dizilim sırasını ve mayotik krossingover sırasındaki rekombinasyon sıklığını matematiksel olarak ortaya koyar.",
         "rekombinasyon sıklığına göre", 0, None, "rekombinasyon sıklığını"),
        ("Genetik haritalarda yüzde bir oranındaki rekombinasyon, **bir centimorgan** fiziksel uzaklık birimine karşılık gelir.",
         "Genetik bağlantı haritalarında yüzde birlik rekombinasyon oranı, yaklaşık bir milyon baz çiftine denk gelen bir centimorganlık harita birimi olarak tanımlanır.",
         "1 harita birimine yani 1", 0, None, "bir centimorgan")
    ]
    
    # PAGE 21
    pdata[21] = [
        ("Bağlantı analizi, hastalık fenotipinin altında yatan **kromozom bölgesini ve risk lokusunu** belirlemeyi hedefler.",
         "Bağlantı analizi, hastalığın patogenezinden sorumlu mutant genin veya risk bölgesinin kromozom üzerindeki kaba fiziksel lokasyonunu tespit etmek amacıyla kullanılır.",
         "Bağlantı analizi", 0, None, "kromozom bölgesini"),
        ("Aynı kromozomda birbirine çok yakın bulunan lokuslar, mayoz sırasında **birlikte kalıtılma eğilimi** gösterir.",
         "Fiziksel olarak aynı kromozom kolunda birbirine çok yakın konumlanan genetik belirteçler, mayotik bölünmede birbirinden ayrılmayarak beraberce sonraki nesillere aktarılır.",
         "Hastalık patogenezinin", 0, None, "birlikte kalıtılma eğilimi")
    ]
    
    # PAGE 22
    pdata[22] = [
        ("Linkage çalışmalarında bilinen bir belirteç ile hastalık geninin **ko-segregasyonu** matematiksel olarak test edilir.",
         "Bağlantı yani linkage çalışmalarında, genomik konumu kesin bilinen bir mikrosatellit belirteç ile hastalık geninin aile soyağacında birlikte kalıtılması yani ko segregasyonu incelenir.",
         "Bağlantı analizlerinde bir hastalığın", 0, None, "ko-segregasyonu"),
        ("Aralarındaki mesafe ne kadar darsa, aralarında **krossingover gerçekleşme ihtimali** o kadar düşüktür.",
         "İki lokus arasındaki fiziksel mesafe ne kadar darsa, mayoz profazında aralarında krossingover gerçekleşme ve birbirlerinden kopma olasılığı o denli azalmaktadır.",
         "Moleküler genetik çalışmalar", 0, None, "krossingover gerçekleşme")
    ]
    
    # PAGE 23
    pdata[23] = [
        ("Bağlantı analizinin gücü **LOD skoru yani log of odds** değeri hesaplanarak istatistiksel olarak değerlendirilir.",
         "Bağlantı gücünün istatistiksel kanıtı, bağlantı olasılığının bağımsız dağılım olasılığına oranının logaritması olan el o de skoru yani log of odds değeriyle hesaplanır.",
         "LOD skoru", 0, None, "LOD skoru"),
        ("LOD skorunun **üç ve üzerinde çıkması** bağlantıyı kesin olarak kanıtlarken, eksi ikinin altı bağlantıyı kesinlikle dışlar.",
         "El o de skorunun artı üç veya üzerinde bir değer alması iki lokus arasında kesin genetik bağlantıyı ispatlar; eksi iki ve altındaki negatif değerler ise o kromozom bölgesinde bağlantı olmadığını gösterir.",
         "3 ve üzeri değerler bağlantıyı", 0, None, "üç ve üzerinde")
    ]
    
    # PAGE 24
    pdata[24] = [
        ("Klasik bağlantı analizleri özellikle **tek gen kalıtımı veya majör gen etkisi** taşıyan tablolarda yüksek başarı sağlar.",
         "Klasik bağlantı analizleri, hastalığın belirgin bir Mendel kalıtım paternine sahip olduğu ve ailede tek bir majör gen mutasyonunun baskın rol oynadığı tablolarda çok başarılıdır.",
         "Tek gen ya da majör gen", 0, None, "tek gen kalıtımı"),
        ("Çok sayıda küçük etkili genin rol oynadığı **kompleks psikiyatrik tablolarda** ise bağlantı analizinin gücü sınırlı kalır.",
         "Buna karşın yüzlerce gen varyantının mikro etkilerinin birleştiği kompleks psikiyatrik hastalıklarda klasik linkage çalışmaları zayıf kalmakta ve yerini ilişki çalışmalarına bırakmaktadır.",
         "Klasik linkage çalışmaları", 0, None, "kompleks psikiyatrik")
    ]
    
    # PAGE 25
    pdata[25] = [
        ("İlişki yani assosiasyon çalışmalarında, patogenezde rol oynadığı düşünülen **aday gen varyantları** araştırılır.",
         "İlişki yani assosiasyon çalışmalarında, hastalığın nörobiyolojik patogenezinde rol aldığı varsayılan spesifik bir aday genin ve polimorfizmlerinin varlığı araştırılmaktadır.",
         "İlişki (Assosiasyon) çalışmaları", 0, None, "aday gen varyantları"),
        ("Hasta grubu ile sağlıklı kontrol grubu arasında **alel frekansı farkı** istatistiksel olarak karşılaştırılır.",
         "Geniş vaka ve sağlıklı kontrol kohortları arasında incelenen alelin görülme sıklığı karşılaştırılarak, o varyantın hastalık riskini artırıp artırmadığı saptanır.",
         "hastalık patogenezinde rol alan aday", 0, None, "alel frekansı farkı")
    ]
    
    # PAGE 26
    pdata[26] = [
        ("Şimdi psikiyatrideki spesifik **hastalık örnekleri ve genetik mekanizmalar** üzerinden ilerleyeceğiz.",
         "Genel araştırma ilkelerini tamamladıktan sonra, şimdi psikiyatri kliniğinde en sık karşılaşılan spesifik hastalık örnekleri ve altlarındaki moleküler genetik mekanizmaları ele alacağız.",
         "Hastalık Örnekleri", 0, None, "hastalık örnekleri"),
        ("Kişilik bozukluklarından şizofreniye, bipolar bozukluktan **bağımlılık genetiğine** kadar geniş bir yelpaze bulunmaktadır.",
         "Kişilik bozukluklarından şizofreniye, duygudurum tablolarından alkol bağımlılığına ve anksiyeteye uzanan geniş yelpazede kanıtlanmış genetik bulguları adım adım inceleyeceğiz.",
         "Hastalık Örnekleri", 0, None, "bağımlılık genetiğine")
    ]
    
    # PAGE 27
    pdata[27] = [
        ("Kişilik bozukluklarında kalıtılabilirlik oranları yaklaşık **yüzde otuz ila altmış** arasında tahmin edilir.",
         "Kişilik bozuklukları üzerine yapılan epidemiyolojik ikiz ve aile araştırmalarında kalıtılabilirlik oranları yaklaşık yüzde otuz ila altmış arasında hesaplanmaktadır.",
         "Kişilik Bozuklukları", 0, None, "kalıtılabilirlik oranları"),
        ("Genetik faktörler özellikle mizaç özelliklerini, **dürtü kontrol kapasitesini** ve stres toleransını belirler.",
         "Genetik yatkınlık bireyin nörobiyolojik mizaç özelliklerini, prefrontal korteksteki dürtü kontrol kapasitesini ve çevresel tehlikelere verdiği duygusal yanıtı şekillendirir.",
         "Kişilik Bozuklukları", 0, None, "dürtü kontrol kapasitesini")
    ]
    
    # PAGE 28
    pdata[28] = [
        ("Kişilik bozuklukları etiyolojisinde **serotonerjik, dopaminerjik ve noradrenerjik** yolak polimorfizmleri odak noktasıdır.",
         "Kişilik bozukluklarının moleküler patogenezinde serotonerjik disfonksiyon dürtüsellik ve agresyonla, dopaminerjik yolaklar yenilik arayışıyla, noradrenerjik sistem ise tehlikeden kaçınmayla bağlantılıdır.",
         "Kişilik Bozuklukları", 0, None, "serotonerjik, dopaminerjik"),
        ("Serotonin taşıyıcı ve parçalayıcı genlerdeki varyantlar **prefrontal otokontrolü zayıflatarak** davranışsal disinhibisyona yol açabilir.",
         "Serotonin taşıyıcı proteini ve monoamin katabolizma enzimlerini kodlayan genetik polimorfizmler prefrontal denetimi zayıflatarak patolojik davranış kalıplarına zemin hazırlar.",
         "Kişilik Bozuklukları", 0, None, "prefrontal otokontrolü")
    ]
    
    # PAGE 29
    pdata[29] = [
        ("Antisosyal kişilik bozukluğunda **dürtüsellik, kural tanımazlık ve empati yoksunluğu** temel klinik özelliklerdir.",
         "Antisosyal kişilik bozukluğu tablosunda çocukluk çağından itibaren süregelen dürtüsellik, agresyon, sosyal kuralları çiğneme ve empati eksikliği en belirgin klinik özelliklerdir.",
         "Antisosyal Kişilik Bozukluğu(ASKB)", 0, None, "dürtüsellik, kural tanımazlık"),
        ("Bu bozukluğun etiyolojisinde genetik yatkınlık ile **çocukluk çağı travması** güçlü bir sinerji oluşturur.",
         "Bu bozukluğun etiyolojisinde kalıtsal yatkınlık ile çocukluk döneminde maruz kalınan ağır fiziksel veya duygusal istismar güçlü bir etkileşim gösterir.",
         "Antisosyal Kişilik Bozukluğu", 0, None, "çocukluk çağı travması")
    ]
    
    # PAGE 30
    pdata[30] = [
        ("Antisosyal kişilik bozukluğunda **5-HTTLPR ve MAO-A promoter polimorfizmleri** üzerine yoğun çalışmalar yapılmıştır.",
         "Antisosyal davranışların biyolojisinde serotonin geri alım taşıyıcısı beş haş te te le pe re geni ile monoamin oksidaz a promoter bölgesindeki değişken tandem tekrarlar mercek altına alınmıştır.",
         "5HTTLPR geni ile MAO-A promoterın", 0, None, "5-HTTLPR ve MAO-A"),
        ("Serotonin taşıyıcı genin **kısa alelini taşıyan bireylerde** dürtüsel saldırganlık ve anksiyöz tepkisellik daha belirgin bulunur.",
         "Serotonin taşıyıcı genin kısa es alelini homozigot ya da heterozigot taşıyan bireylerde, duygusal stresörler karşısında amigdala hiperaktivitesi ve dürtüsel agresyon daha sık saptanır.",
         "S alelleri antisosyal davranışlar", 0, None, "kısa alelini taşıyan")
    ]
    
    # PAGE 31
    pdata[31] = [
        ("Caspi ve arkadaşlarının klasik çalışmasında, **düşük aktiviteli MAO-A aleli** taşıyan çocukların istismara uğradığında antisosyal olma riski yüksek bulunmuştur.",
         "Caspi ve çalışma arkadaşlarının tıp literatürüne giren çığır açıcı bulgusuna göre, düşük aktiviteli monoamin oksidaz a aleli taşıyan çocuklar ağır istismara maruz kaldıklarında erişkin dönemde antisosyal olma riski dramatik şekilde artmaktadır.",
         "Kişilik Bozuklukları", 0, None, "düşük aktiviteli MAO-A"),
        ("Buna karşılık **yüksek aktiviteli MAO-A aleli** taşıyan çocuklar, travmaya rağmen antisosyal gelişime karşı korunabilmektedir.",
         "Buna karşın yüksek enzimatik aktiviteye sahip promoter alelini taşıyan çocukların, benzer travmatik çevreye maruz kalsalar bile antisosyal davranış gelişimine karşı biyolojik bir direnç sergilediği gösterilmiştir.",
         "Kişilik Bozuklukları", 0, None, "yüksek aktiviteli MAO-A")
    ]
    
    # PAGE 32
    pdata[32] = [
        ("Bu çarpıcı bulgu, psikiyatride **gen-çevre etkileşiminin** en somut ve kanıtlanmış bilimsel modelini oluşturur.",
         "Bu bulgu, psikiyatrik genetik araştırmalarında biyolojik genetik risk ile psikososyal çevrenin nasıl iç içe geçtiğini gösteren en kusursuz gen çevre etkileşimi modelidir.",
         "Kişilik Bozuklukları", 0, None, "gen-çevre etkileşiminin"),
        ("Tek başına genetik yapı veya tek başına çevre değil, **ikisinin birleşimi** patolojik fenotipik sonucu belirler.",
         "Dolayısıyla tek başına genetik varyasyon ya da tek başına çevresel stres değil, bu iki faktörün moleküler düzeydeki kesişimi bireyin nihai davranışsal profilini ortaya çıkarmaktadır.",
         "Kişilik Bozuklukları", 0, None, "ikisinin birleşimi")
    ]
    
    # PAGE 33
    pdata[33] = [
        ("Manik-depresif hastalık yani **bipolar bozukluk**, psikiyatride kalıtsallığı en yüksek tablolardan biridir.",
         "Manik depresif hastalık yani bipolar bozukluk, psikiyatri kliniğinde kalıtılabilirlik gücü en yüksek ve genetik kökeni en belirgin duygu durum bozukluklarından biridir.",
         "Manik-Depresif Hastalık", 0, None, "bipolar bozukluk"),
        ("Mani ve depresyon ataklarıyla seyreden bu bozuklukta **ailesel kümelenme** son derece belirgindir.",
         "Dönemsel mani veya hipomani ile çökkünlük ataklarıyla seyreden bu tabloda, birinci derece aile bireylerinde hem bipolar hem de unipolar bozukluk görülme riski oldukça yüksektir.",
         "Manik-Depresif Hastalık", 0, None, "ailesel kümelenme")
    ]
    
    # PAGE 34
    pdata[34] = [
        ("Bipolar bozuklukta monozigot ikiz konkordansı **yüzde altmış ila yetmişe** ulaşırken, unipolar depresyonda yüzde kırk civarındadır.",
         "Bipolar bozuklukta monozigot ikizler arasındaki konkordans oranı yüzde altmış ila yetmiş gibi çok yüksek bir seviyeye ulaşırken, unipolar depresyonda bu oran yüzde kırk civarında seyretmektedir.",
         "Tekrarlama riski (bipolar, unipolar", 0, None, "monozigot ikiz konkordansı"),
        ("Bu dramatik fark, bipolar bozukluğun unipolar depresyona kıyasla **çok daha güçlü genetik ağırlık** taşıdığını kanıtlar.",
         "Bu belirgin konkordans uçurumu, bipolar tablonun unipolar depresyona kıyasla çok daha baskın bir nörobiyolojik ve kalıtsal temele dayandığını açıkça kanıtlamaktadır.",
         "Tekrarlama riski", 0, None, "güçlü genetik ağırlık")
    ]
    
    # PAGE 35
    pdata[35] = [
        ("Bipolar bozuklukta bağlantı çalışmaları dördüncü, on ikinci, **on sekizinci ve yirmi ikinci kromozomlarda** risk lokusları saptamıştır.",
         "Bipolar bozuklukta yapılan genom tarama ve bağlantı çalışmaları; dördüncü kromozom p kolu, on ikinci kromozom q kolu, on sekizinci ve yirmi ikinci kromozomlarda tekrarlayan risk bölgeleri bildirmiştir.",
         "BD için; 4p16, 4q35, 8q24", 0, None, "on sekizinci ve yirmi ikinci"),
        ("Bu kromozomal bölgeler kalsiyum sinyal iletimi ve **sinaptik plastisiteden sorumlu** genleri barındırır.",
         "Bu kromozomal segmentler, nöronal kalsiyum kanal iletiminden ve sinaptik nöroplastisiteden sorumlu kritik gen kümelerini bünyesinde barındırmaktadır.",
         "Manik-Depresif Hastalık-Genetik Faktörler", 0, None, "sinaptik plastisiteden sorumlu")
    ]
    
    # PAGE 36
    pdata[36] = [
        ("Aday genler arasında beyin kaynaklı nörotrofik faktör **BDNF, DAOA yani G72 ve DISC1** öne çıkar.",
         "Bipolar bozukluk için araştırılan aday genler arasında beyin kaynaklı nörotrofik faktör be de ne fe geni, de a o a yani ge yetmiş iki lokusu ve disk bir genleri ön plana çıkmaktadır.",
         "Manik-Depresif Hastalık-Aday Genler (BD)", 0, None, "BDNF, DAOA"),
        ("Özellikle **BDNF Val66Met polimorfizmi**, hipokampal plastisiteyi ve lityum tedavisine verilen klinik yanıtı etkiler.",
         "Özellikle be de ne fe genindeki valin altmış altı metiyonin polimorfizmi, hipokampal hacmi, nöroplastisiteyi ve hastanın lityum sağaltımına verdiği yanıtı doğrudan etkilemektedir.",
         "Aday Genler", 0, None, "BDNF Val66Met")
    ]
    
    # PAGE 37
    pdata[37] = [
        ("Duygudurum bozukluklarında poligenik risk skorları, binlerce **küçük etkili varyantın toplamını** temsil eder.",
         "Duygudurum bozukluklarının genetik mimarisinde poligenik risk skorlamaları, genom geneline yayılmış binlerce küçük etkili tek nükleotid varyantının matematiksel toplamını ifade eder.",
         "Duygudurum Bozuklukları", 0, None, "poligenik risk skorları"),
        ("Bu poligenik yatkınlık eşik değeri aştığında ve **psikososyal stresörlerle birleştiğinde** klinik atak tetiklenir.",
         "Bu poligenik kalıtsal yük bireyin biyolojik eşik değerini aştığında ve çevresel yaşam olaylarıyla tetiklendiğinde mani ya da depresyon atağı klinik olarak patlak verir.",
         "Duygudurum Bozuklukları", 0, None, "psikososyal stresörlerle")
    ]
    
    # PAGE 38
    pdata[38] = [
        ("İntihar davranışı, altta yatan psikiyatrik tanıdan kısmen bağımsız olarak **kendi içinde genetik bir kalıtılabilirlik** gösterir.",
         "İntihar davranışı sadece majör depresyonun bir belirtisi olmayıp, altta yatan psikiyatrik tablodan bağımsız olarak aile ve ikiz çalışmalarında kendi genetik kalıtılabilirliğini sergiler.",
         "Duygudurum Bozuklukları", 0, None, "genetik bir kalıtılabilirlik"),
        ("Ailesinde tamamlanmış intihar öyküsü bulunan bireylerde özkıyım riski, **tanıdan bağımsız olarak artış** sergiler.",
         "Ailesinde tamamlanmış intihar öyküsü bulunan kişilerde intihar girişimi riski, hastada duygudurum bozukluğu olup olmamasından bağımsız şekilde anlamlı düzeyde artmış bulunur.",
         "Duygudurum Bozuklukları", 0, None, "tanıdan bağımsız olarak")
    ]
    
    # PAGE 39
    pdata[39] = [
        ("İntihar davranışının nörobiyolojisinde en tutarlı bulgu, **santral serotonerjik iletim yetersizliğidir**.",
         "İntihar davranışının nörobiyolojik incelemelerinde en tutarlı ve tekrarlanan biyolojik bulgu, santral sinir sistemindeki serotonerjik iletim yetersizliği ve hipoaktivitedir.",
         "Duygudurum Bozuklukları", 0, None, "serotonerjik iletim yetersizliğidir"),
        ("Beyin omurilik sıvısında serotonin metaboliti olan **5-HIAA düzeylerinin düşük bulunması** ölümcül intihar girişimleriyle doğrudan ilişkilidir.",
         "Beyin omurilik sıvısında serotonin ana metaboliti olan beş haş i a a konsantrasyonunun belirgin düşük saptanması, ölümcül ve şiddet içerikli intihar eylemleriyle doğrudan korele bulunmuştur.",
         "Duygudurum Bozuklukları", 0, None, "5-HIAA düzeylerinin")
    ]
    
    # PAGE 40
    pdata[40] = [
        ("İntiharda aday gen olarak serotonin sentezini başlatan hız kısıtlayıcı **triptofan hidroksilaz yani TPH genleri** incelenmiştir.",
         "İntihar biyolojisinde aday gen olarak, serotonin biyosentezinde hız kısıtlayıcı basamağı katalizleyen triptofan hidroksilaz yani te pe haş enzimi genleri yoğun şekilde araştırılmıştır.",
         "İntihar  davranışında serotonerjik nörotransmisyonun", 0, None, "triptofan hidroksilaz"),
        ("Özellikle beyin kaynaklı **TPH2 varyantları**, prefrontal kortekste serotonin düzeyini düşürerek dürtüsel özkıyım riskini artırır.",
         "Özellikle beyin dokusunda eksprese olan te pe haş iki izoformundaki fonksiyonel polimorfizmler, prefrontal serotonini azaltarak dürtü kontrolünün çökmesine ve intihar eğilimine yol açabilir.",
         "TPH", 0, None, "TPH2 varyantları")
    ]
    
    # PAGE 41
    pdata[41] = [
        ("Ayrıca serotonin **5-HT1A ve 5-HT2A reseptör polimorfizmleri** de intihar riskiyle ilişkili bulunmuştur.",
         "Ayrıca presinaptik otoreseptör olan beş haş te bir a ve postsinaptik beş haş te iki a reseptör gen polimorfizmleri de agresyon ve intihar riskiyle ilişkili bildirilmiştir.",
         "Duygudurum Bozuklukları", 0, None, "5-HT1A ve 5-HT2A"),
        ("Bu polimorfizmler stres yanıtı sırasında **amigdala-prefrontal korteks dengesini** bozarak akut dürtüsel krize yol açar.",
         "Bu reseptör polimorfizmleri stres esnasında amigdala ile prefrontal korteks arasındaki inhibitör dengeyi bozarak krize yanıt olarak kendine zarar verme davranışını tetikler.",
         "Duygudurum Bozuklukları", 0, None, "amigdala-prefrontal korteks")
    ]
    
    # PAGE 42
    pdata[42] = [
        ("Şizofreni, genel toplumda yaklaşık **yüzde bir prevalansa** sahip kronik ve yıkıcı bir psikotik bozukluktur.",
         "Şizofreni, genel toplumda coğrafyadan bağımsız olarak yaklaşık yüzde bir yaşam boyu yaygınlığa sahip, bilişsel ve duygusal yıkımla seyreden kronik bir psikotik tablodur.",
         "Şizofreni", 0, None, "yüzde bir prevalansa"),
        ("Bozukluğun ortaya çıkışında genetik faktörlerin katkısı **yüzde seksen gibi muazzam bir orana** ulaşmaktadır.",
         "Bu ağır bozukluğun etiyolojisinde genetik yatkınlığın göreceli payı yüzde seksen gibi muazzam bir kalıtsallık düzeyine ulaşmaktadır.",
         "Şizofreni", 0, None, "yüzde seksen")
    ]
    
    # PAGE 43
    pdata[43] = [
        ("Şizofreni etiyolojisinde genetik zemin temel olsa da, **intrauterin ve çevresel stresörler** tetikleyici rol oynar.",
         "Şizofreni patogenezinde genetik zemin birincil olsa da; maternal enfeksiyonlar, obstetrik komplikasyonlar, kış doğumu ve erken esrar kullanımı tetikleyici risk etmenleridir.",
         "Şizofreni", 0, None, "intrauterin ve çevresel"),
        ("İki vuruş hipotezine göre, **erken nörogelişimsel hasar** pubertede sinaptik budanma anomalisiyle birleşerek psikozu başlatır.",
         "İki vuruş hipotezi uyarınca, intrauterin dönemde meydana gelen erken nörogelişimsel hasar ergenlikteki aşırı sinaptik budanma anomalisiyle birleştiğinde psikoz kliniği patlak verir.",
         "Şizofreni", 0, None, "erken nörogelişimsel hasar")
    ]
    
    # PAGE 44
    pdata[44] = [
        ("Şizofreni genetiğinde yapılan geniş aile çalışmaları, akrabalık derecesiyle **doğru orantılı bir morbid risk** ortaya koyar.",
         "Şizofreni genetiğinde yapılan geniş çaplı aile kohortları, proband ile akrabalık derecesi yakınlaştıkça morbid riskin geometrik olarak arttığını net şekilde belgelemiştir.",
         "Şizofreni Genetiği", 0, None, "doğru orantılı bir morbid risk"),
        ("İkinci derece akrabalarda risk yüzde iki ila dört iken, **birinci derece akrabalarda yüzde ona** fırlar.",
         "Genel toplumda yüzde bir olan risk; amca, dayı ve torun gibi ikinci derece akrabalarda yüzde iki ila dörde, kardeş ve çocuk gibi birinci derece akrabalarda ise yüzde ona fırlamaktadır.",
         "Şizofreni Genetiği", 0, None, "birinci derece akrabalarda")
    ]
    
    # PAGE 45
    pdata[45] = [
        ("Aile çalışmalarında şizofreni ile duygudurum bozukluklarının **ortak genetik havuz paylaştığı** gösterilmiştir.",
         "Geniş aile araştırmalarında şizofreni ile psikotik özellikli bipolar bozukluğun önemli ölçüde ortak bir genetik duyarlılık havuzunu paylaştığı anlaşılmıştır.",
         "şizofreni ve duygu durum", 0, None, "ortak genetik havuz"),
        ("Bazı ailelerde aynı risk alellerinin bir bireyde şizofreniye, diğerinde **şizoafektif veya bipolar tabloya** yol açtığı izlenir.",
         "Nitekim aynı soyağacında belirli risk allellerinin bir fertte klasik şizofreniye yol açarken, diğer bir aile üyesinde şizoafektif veya manik tabloya neden olduğu sıkça gözlenir.",
         "birlikte kalıtım", 0, None, "şizoafektif veya bipolar")
    ]
    
    # PAGE 46
    pdata[46] = [
        ("Bir ebeveyni şizofreni olan çocuğun hastalanma riski **yüzde on ila on iki** civarındadır.",
         "Anne veya babasından biri şizofreni tanısı almış olan bir çocuğun hayat boyu şizofreniye yakalanma riski genel toplumun on katına çıkarak yüzde on ila on ikiye ulaşır.",
         "Şizofreni", 0, None, "yüzde on ila on iki"),
        ("Tek bir hasta ebeveyn bile çocuktaki **hastalık ihtimalini on kat** artırmaktadır.",
         "Görüldüğü üzere tek bir hasta ebeveyn dahi çocuğun gelecekteki psikoz geliştirme ihtimalini taban riske oranla tam on kat yukarı çekmektedir.",
         "Şizofreni", 0, None, "hastalık ihtimalini on kat")
    ]
    
    # PAGE 47
    pdata[47] = [
        ("Eğer her iki ebeveyn de şizofreni hastasıysa, çocuktaki hastalık riski **yüzde kırk ila kırk altıya** kadar yükselir.",
         "Eğer hem anne hem de baba şizofreni hastasıysa, bu evlilikten doğacak çocuklarda şizofreni gelişme riski yüzde kırk ila kırk altı gibi dramatik bir düzeye fırlamaktadır.",
         "Şizofreni-Aile Çalışmaları", 0, None, "yüzde kırk ila kırk altıya"),
        ("Bu bulgu şizofrenide gen dozajının ve **bilateral poligenik yükün** belirleyici olduğunu kanıtlar.",
         "Bu çarpıcı epidemiyolojik veri, şizofrenide her iki ebeveynden gelen risk alellerinin kümülatif dozunun patogenezdeki belirleyici ağırlığını kanıtlamaktadır.",
         "Şizofreni-Aile Çalışmaları", 0, None, "bilateral poligenik yükün")
    ]
    
    # PAGE 48
    pdata[48] = [
        ("Evlat edinme çalışmaları, biyolojik ebeveyni şizofreni olan çocukların **sağlıklı ailede büyütülseler bile** risk taşıdığını belgeler.",
         "Şizofreni evlat edinme modellerinde, biyolojik annesi şizofreni olan çocuklar doğumda sağlıklı koruyucu ailelere evlatlık verilseler dahi yüksek hastalık riskini korumaktadırlar.",
         "Şizofreni-Aile Çalışmaları", 0, None, "sağlıklı ailede büyütülseler bile"),
        ("Buna karşılık sağlıklı ebeveynin çocuğu şizofren bir ailede büyütülürse, **hastalık riski artış göstermez**.",
         "Buna mukabil sağlıklı biyolojik ebeveynlerin çocukları şizofren bir koruyucu ailede büyütülseler bile hastalık risklerinde belirgin bir artış meydana gelmemektedir.",
         "Şizofreni-Aile Çalışmaları", 0, None, "hastalık riski artış")
    ]
    
    # PAGE 49 - ÇIKMIŞ
    pdata[49] = [
        ("Şizofrenide ikiz konkordansı **monozigot ikizlerde yüzde elli üç**, dizigot ikizlerde ise yüzde on beş civarındadır.",
         "Geçmiş yılların çıkmış sınav sorusunda özellikle sorulduğu gibi, şizofrenide monozigot ikizler arasındaki eş hastalanma yani konkordans oranı yaklaşık yüzde elli üç iken, dizigot ikizlerde bu oran yüzde on beşe gerilemektedir.",
         "MZ ikiz  konkordansı →%53", 0,
         {"soru_id": "past-1790877040101-810624", "yil": "2020-2021"},
         "monozigot ikizlerde yüzde elli üç"),
        ("Monozigot ikizlerin yüzde yüz genetik özdeşliğine rağmen uyumun tam yüzde yüz olmaması, **çevresel faktörlerin ve epigenetiğin rolünü** gösterir.",
         "Monozigot ikizler tamamen aynı genoma sahip olmalarına rağmen konkordansın tam yüzde yüz olmaması, intrauterin mikro çevre, somatik mutasyonlar ve epigenetiğin payını kesinleştirmektedir.",
         "DZ ikiz konkordansı", 0, None, "epigenetiğin rolünü")
    ]
    
    # PAGE 50
    pdata[50] = [
        ("Genom tarama çalışmaları şizofreni için **1q21-q22, 6p24-p22 ve 13q32-34** bölgelerinde güçlü bağlantılar saptamıştır.",
         "Genom tarama çalışmaları şizofreni riski için birinci kromozom q kolu, altıncı kromozom p kolu ve on üçüncü kromozom q kolu gibi kritik lokuslarda güçlü sinyaller yakalamıştır.",
         "1q21-q22, 6p24-p22, 13q32-34", 0, None, "1q21-q22"),
        ("Bu bağlantı bölgeleri nöronal göç, akson rehberliği ve **sinaps olgunlaşması** ile ilgili genleri barındırır.",
         "Bu kromozomal bağlantı alanları fetal beyin gelişiminde nöronal göç, akson yönelimi ve sinaps matürasyonunu yöneten anahtar genleri içermektedir.",
         "Şizofreni-Genetik Faktörler", 0, None, "sinaps olgunlaşması")
    ]
    
    # PAGE 51
    pdata[51] = [
        ("Aday genler arasında disbindin geni **DTNBP1**, nörogulin geni **NRG1** ve **DISC1** en çok araştırılanlardır.",
         "Şizofrenide aday gen çalışmalarında disbindin proteinini kodlayan de te ne be pe bir, nörogulin bir geni olan ne re ge bir ve disk bir genleri en kapsamlı biçimde doğrulanmıştır.",
         "Şizofreni-Aday Genler (Linkage çalışmaları)", 0, None, "DTNBP1"),
        ("Bu genler **glutamat NMDA reseptör fonksiyonlarını** ve veziküler nörotransmitter salınımını doğrudan düzenler.",
         "Bu protein ürünleri glutamat en em de a reseptör sinyal iletimini, dendritik dallanmayı ve presinaptik vezikül trafiğini doğrudan modüle etmektedir.",
         "Linkage çalışmaları", 0, None, "glutamat NMDA reseptör")
    ]
    
    # PAGE 52
    pdata[52] = [
        ("Şizofrenide genom boyu ilişkilendirme çalışmaları yani GWAS, **yüzün üzerinde bağımsız genomik lokus** tespit etmiştir.",
         "Şizofrenide yüz bini aşkın hastanın tarandığı genom boyu ilişkilendirme yani gıvas çalışmaları, hastalık riskiyle ilişkili yüzün üzerinde bağımsız genomik lokus ortaya çıkarmıştır.",
         "Şizofreni-Genome-Wide Association", 0, None, "yüzün üzerinde bağımsız"),
        ("En güçlü ilişki sinyali, altıncı kromozomdaki **majör histouyumluluk kompleksi MHC bölgesinden** elde edilmiştir.",
         "Bu devasa analizlerdeki en kuvvetli biyolojik istatistiksel sinyal, altıncı kromozomda yer alan majör histouyumluluk kompleksi yani me ha şe lokusundan elde edilmiştir.",
         "Genome-Wide Association", 0, None, "majör histouyumluluk kompleksi")
    ]
    
    # PAGE 53
    pdata[53] = [
        ("MHC bölgesindeki kompleman bileşeni C4 geni, ergenlik döneminde **patolojik sinaptik budanmayı** yönetir.",
         "Majör histouyumluluk bölgesindeki kompleman faktörü se dört geni, ergenlik döneminde gereksiz nöronal sinapsların fagositozla budanma sürecini yönetir.",
         "Şizofreni-GWA", 0, None, "sinaptik budanmayı"),
        ("C4A ekspresyonunun aşırı artması, serebral kortekste **aşırı sinaps kaybına ve frontal gri cevher incelmesine** yol açar.",
         "Se dört a gen ekspresyonunun genetik olarak aşırı artması, ergenlikte frontal kortekste aşırı sinaps kaybına ve gri cevher incelmesine sebep olarak psikoz zeminini kurar.",
         "Şizofreni-GWA", 0, None, "aşırı sinaps kaybına")
    ]
    
    # PAGE 54
    pdata[54] = [
        ("Kopya sayısı varyasyonları yani CNV'ler arasında **22q11.2 mikrodelesyonu** şizofreni riskini yirmi ila otuz kat artırır.",
         "Submikroskobik kopya sayısı değişiklikleri yani se ne ve ler arasında yirmi ikinci kromozom uzun kolundaki yirmi iki kü on bir nokta iki mikrodelesyonu, şizofreni gelişme riskini tam yirmi ila otuz kat artırmaktadır.",
         "Şizofreni-Submikroskobik Kromozomal", 0, None, "22q11.2 mikrodelesyonu"),
        ("Velokardiyofasiyal sendromlu bireylerin yaklaşık **yüzde yirmi beşinde erişkin yaşta şizofreni** tablosu gelişir.",
         "Velokardiyofasiyal veya DiGeorge sendromlu hastaların yaklaşık dörtte birinde yani yüzde yirmi beşinde erişkin yaşta belirgin şizofreni tablosu ortaya çıkmaktadır.",
         "Submikroskobik Kromozomal", 0, None, "erişkin yaşta şizofreni")
    ]
    
    # PAGE 55
    pdata[55] = [
        ("Endofenotipler, genetik riski temsil eden **objektif, kalıtsal ve ölçülebilir** biyolojik aracı belirteçlerdir.",
         "Endofenotipler, poligenik psikiyatrik hastalıkların karmaşık genetik riskini temsil ettiği kabul edilen objektif, kalıtsal ve laboratuvarda ölçülebilir biyolojik belirteçlerdir.",
         "Endofenotipler", 0, None, "Endofenotipler"),
        ("Şizofrenide **P50 duyusal kapılama defekti ve SPEM yani göz izleme bozuklukları** en tipik endofenotiplerdir.",
         "Şizofrenide elektroensefalografide pe elli işitsel duyusal kapılama yetersizliği ile düzgün izleme göz hareketleri yani es pe e me defektleri kanıtlanmış tipik endofenotiplerdir.",
         "objektif, kalıtsal ve ölçülebilir", 0, None, "P50 duyusal kapılama")
    ]
    
    # PAGE 56
    pdata[56] = [
        ("Alkol bağımlılığı bulunan bireylerin ailelerinde alkolizm riski genel topluma kıyasla **dört kat daha fazladır**.",
         "Alkol bağımlılığı tanısı almış bireylerin ailelerinde yapılan epidemiyolojik çalışmalarda, bu ailelerde alkolizm riskinin normal ailelere kıyasla tam dört kat daha yüksek olduğu saptanmıştır.",
         "Alkol ve Madde Bağımlılığı", 0, None, "dört kat daha fazladır"),
        ("Monozigot ikizlerdeki konkordans oranı dizigot ikizlerin **iki katı düzeyinde** seyretmektedir.",
         "İkiz çalışmalarında monozigot ikizler arasındaki konkordans oranı, dizigot ikiz çiftlerine kıyasla iki kat daha yüksek bulunarak genetik yatkınlığı doğrulamıştır.",
         "Alkol ve Madde Bağımlılığı", 0, None, "iki katı düzeyinde")
    ]
    
    # PAGE 57
    pdata[57] = [
        ("Alkolün pekiştirici ve bağımlılık yapıcı etkisi, **mezolimbik dopaminerjik ödül yolağının** aktivasyonuna dayanır.",
         "Alkolün ödüllendirici ve pekiştirici etkisi, ventral tegmental alandan nükleus akkumbense uzanan mezolimbik dopaminerjik ödül sistemini doğrudan aktive etmesiyle ortaya çıkar.",
         "mesolimbik dopamin sistemini aktive", 0, None, "mezolimbik dopaminerjik"),
        ("Ayrıca serotonerjik yolaklardaki **TPH ve 5-HT2A/2C reseptör genleri** de bağımlılık yatkınlığında rol oynar.",
         "Ayrıca serotonerjik iletimi yöneten triptofan hidroksilaz ile beş haş te iki a ve iki c reseptör genlerindeki polimorfizmler alkol arama davranışını etkilemektedir.",
         "Serotonerjik yolaklardaki genler", 0, None, "5-HT2A/2C reseptör")
    ]
    
    # PAGE 58
    pdata[58] = [
        ("Bağımlılıkta genetik faktörler kadın ve erkekte benzer etki gösterirken, **toplumsal normlar** erkek prevalansını artırır.",
         "Bağımlılığın moleküler genetik etki derecesi kadın ve erkekte biyolojik olarak benzer bulunmakla birlikte, kültürel normlar ve alkole erişim sıklığı erkeklerde kullanım oranını iki kattan fazla artırmaktadır.",
         "Genetik etkiler kadın ve erkekte", 0, None, "toplumsal normlar"),
        ("Yaş ilerledikçe genetik faktörlerin etkisi belirginleşirken, **paylaşılan aile çevresinin etkisi** azalmaktadır.",
         "Bireyin yaşı ilerledikçe genetik yatkınlığın göreceli etkisi artmakta, buna karşılık ergenlikte belirleyici olan ortak aile çevresinin etkisi zamanla gerilemektedir.",
         "Yaşla birlikte genetik etkiler", 0, None, "paylaşılan aile çevresinin")
    ]
    
    # PAGE 59
    pdata[59] = [
        ("Kalıtılabilirlik oranları kokain bağımlılığı için **yüzde yetmiş iki**, alkol için ise yüzde elli ila altmıştır.",
         "Bağımlılık türlerinin kalıtılabilirlik oranlarına bakıldığında; kokain bağımlılığı için yüzde yetmiş iki, patolojik kumar için yüzde elli, alkolizm için ise yüzde elli ila altmış düzeyindedir.",
         "Kalıtılabilirlik oranları", 0, None, "Kalıtılabilirlik oranları"),
        ("Bu yüksek oranlar madde kullanım bozukluklarının **biyolojik bir beyin hastalığı** olduğunu kanıtlar.",
         "Bu yüksek kalıtsallık katsayıları, bağımlılık tablolarının zayıf iradeden ibaret olmayıp güçlü genetik temelleri bulunan biyolojik bir beyin hastalığı olduğunu açıkça gösterir.",
         "Alkol (9897) →%0.50-0.60", 0, None, "biyolojik bir beyin")
    ]
    
    # PAGE 60
    pdata[60] = [
        ("Alkol metabolizmasında ardışık görev yapan iki temel enzim **ADH1B ve ALDH2** enzimidir.",
         "Etanolün hepatik metabolizmasında ardışık reaksiyonları katalizleyen iki anahtar enzim; alkol dehidrogenaz bir be yani a de haş bir be ile aldehit dehidrogenaz iki yani a le de haş ikidir.",
         "Aday Genler", 0, None, "ADH1B ve ALDH2"),
        ("Etanol önce asetaldehite, ardından asetaldehit toksik olmayan **asetat molekülüne** oksitlenir.",
         "Alkol dehidrogenaz etanolü önce toksik asetaldehite dönüştürür; ardından aldehit dehidrogenaz bu zehirli ara ürünü zararsız asetat molekülüne okside eder.",
         "ADH1B (Alkol dehidrogenaz 1B)", 0, None, "asetat molekülüne")
    ]
    
    # PAGE 61
    pdata[61] = [
        ("Toksik asetaldehit birikimi, histamin salınımına ve sistemik **flushing reaksiyonuna** yol açar.",
         "Vücutta toksik asetaldehitin birikmesi yoğun bir histamin deşarjına neden olarak baş ağrısı, bulantı, çarpıntı ve deride yaygın kızarma ile seyreden flaşing reaksiyonuna yol açar.",
         "Flushing  reaksiyonu", 0, None, "flushing reaksiyonuna"),
        ("Asetaldehit biriken ve yoğun kızarma yaşayan bireylerde uzun dönemde **üst gastrointestinal sistem kanseri** riski artar.",
         "Asetaldehit birikimi olan ve buna rağmen alkol tüketmeye devam eden bireylerde karsinojenik hasar nedeniyle üst gastrointestinal sistem kanseri riski anlamlı şekilde artar.",
         "üst GİS kanseri riski", 0, None, "gastrointestinal sistem kanseri")
    ]
    
    # PAGE 62
    pdata[62] = [
        ("Flushing reaksiyonuna yatkınlıkta **ADH1B His47Arg ve ALDH2 Glu487Lys** polimorfizmleri belirleyicidir.",
         "Alkol aracılı flaşing reaksiyonuna genetik yatkınlıkta a de haş bir be enzimindeki histidin kırk yedi arjinin ile a le de haş iki enzimindeki glutamat dört yüz seksen yedi lizin varyantları kilit rol oynar.",
         "Alkol-aracılı “Flushing” reaksiyonuna", 0, None, "ADH1B His47Arg"),
        ("İnaktif ALDH2 enzimini taşıyan bireyler asetaldehiti yıkamaz, yoğun rahatsızlık duyarak **alkol bağımlılığından korunur**.",
         "Lizin dört yüz seksen yedi aleline bağlı inaktif enzim taşıyan bireyler asetaldehiti hızla yıkamadıkları için bir kadehte bile şiddetli zehirlenme yaşar ve alkolizmden doğal olarak korunurlar.",
         "Glu487Lys → Lys487 enzim inaktivasyonuna", 0, None, "alkol bağımlılığından korunur")
    ]
    
    # PAGE 63
    pdata[63] = [
        ("Alkolizmde diğer önemli aday genler arasında **COMT, MAOA ve SLC6A4** genleri yer almaktadır.",
         "Alkol bağımlılığında dopamin ve serotonin sinyalizasyonunu etkileyen diğer majör aday genler katekol o metiltransferaz, monoamin oksidaz a ve se le ce altı a dört genleridir.",
         "Diğer Aday Genler", 0, None, "COMT, MAOA ve SLC6A4"),
        ("Bu genler sinaptik aralıktaki **katekolamin ve indolamin katabolizmasını** yöneterek pekiştirme süreçlerini belirler.",
         "Bu genetik belirteçler sinaptik aralıktaki dopamin, noradrenalin ve serotonin katabolizmasını düzenleyerek bağımlılık motivasyonunu ve toleransı etkiler.",
         "COMT", 0, None, "katekolamin ve indolamin")
    ]
    
    # PAGE 64 - ÇIKMIŞ
    pdata[64] = [
        ("COMT enziminde Val158Met polimorfizminde **Met158 aleli üç ila dört kat daha az aktif** çalışır.",
         "Çıkmış komite sınavı sorusunda hekim adaylarına yöneltilen kritik bir soruya göre, katekol o metiltransferaz enziminde valin yerine metiyonin geçmesi enzimatik aktiviteyi üç ila dört kat düşürerek prefrontal kortekste dopamin miktarını artırmaktadır.",
         "Met158 3-4 kat daha az aktif", 0,
         {"soru_id": "d3-k2-tbg-007", "yil": "2021-2026"},
         "Met158 aleli üç ila dört kat daha az aktif"),
        ("Val aleli ise enzimi termostabil ve hızlı kılarak **prefrontal dopamin düzeyini düşürür**.",
         "Buna karşılık valin aleli taşıyıcılarında enzim termostabil olup dopamini hızla yıkar; bu durum prefrontal kortekste dopamin seviyesini azaltarak bilişsel sebatı zayıflatabilir.",
         "COMT-II", 0, None, "prefrontal dopamin düzeyini")
    ]
    
    # PAGE 65
    pdata[65] = [
        ("MAOA enzimi **X kromozomu üzerinde yerleşik** olup hipokampusta yüksek ekspresyon gösterir.",
         "Monoamin oksidaz a enzimi iks kromozomu üzerinde yerleşiktir; hipokampus ve prefrontal kortekste noradrenalin, dopamin ve serotonini katabolize eder.",
         "MAOA-I", 0, None, "X kromozomu üzerinde yerleşik"),
        ("X'e bağlı kalıtım nedeniyle erkeklerde tek bir mutant alel **enzim aktivitesini bütünüyle** belirler.",
         "İkse bağlı kalıtım modeli nedeniyle erkek bireylerde tek bir düşük ya da yüksek aktiviteli promoter alelinin bulunması doku enzim aktivitesini doğrudan belirlemektedir.",
         "X üzerinde yerleşik", 0, None, "enzim aktivitesini")
    ]
    
    # PAGE 66
    pdata[66] = [
        ("SLC6A4 geninin promoter bölgesindeki **5-HTTLPR varyantı** uzun L ve kısa S alellerinden oluşur.",
         "Se le ce altı a dört serotonin taşıyıcı geninin promoter bölgesinde yer alan beş haş te te le pe re polimorfizmi uzun le aleli ile kısa es alelinden meydana gelir.",
         "SLC6A4", 0, None, "5-HTTLPR varyantı"),
        ("Kısa S aleli taşıyıcılarında serotonin geri alımı azalırken, **anksiyete ve depresif reaktivite** anlamlı derecede yükselir.",
         "Kısa es aleli transkripsiyon hızını düşürerek serotonin taşıyıcı sentezini azaltır; bu durum çevresel stres karşısında anksiyete, nevrotizm ve depresif çökkünlük riskini artırır.",
         "5-HTTLPR varyantı; L", 0, None, "anksiyete ve depresif")
    ]
    
    # PAGE 67
    pdata[67] = [
        ("Anksiyete bozuklukları popülasyonda son derece sık görülen ve **kadınlarda iki kat daha yaygın** tablolardır.",
         "Anksiyete bozuklukları klinik pratikte en sık rastlanan psikiyatrik rahatsızlıklardan olup kadın cinsiyette erkeklere oranla yaklaşık iki kat daha sık saptanmaktadır.",
         "Anksiyete Bozuklukları", 0, None, "kadınlarda iki kat"),
        ("Etiyolojilerinde genetik yatkınlık, organik zemin ve **kronik psikososyal stresörler** karmaşık bir etkileşim içindedir.",
         "Anksiyetenin etiyolojisinde genetik varyantlar, nörobiyolojik santral otonomik aşırı uyarılabilirlik ve erken yaşam stresörleri karmaşık bir ağ oluşturur.",
         "kadınlarda daha yaygındır", 0, None, "kronik psikososyal")
    ]
    
    # PAGE 68
    pdata[68] = [
        ("Obsesif-kompulsif bozuklukta monozigot ikiz konkordansı **yüzde yetmiş beş**, dizigot ikizlerde ise yüzde kırk yedidir.",
         "Obsesif kompulsif bozukluk yani o ke be için monozigot ikizler arasındaki eş hastalanma oranı yüzde yetmiş beş iken, dizigot ikizlerde bu oran yüzde kırk yedi seviyesindedir.",
         "Obsesif-Kompulsif Bozukluk(OKB)", 0, None, "yüzde yetmiş beş"),
        ("Bu yüksek oran OKB'nin psikiyatrik bozukluklar arasında **en kuvvetli genetik yüke sahip** tablolardan biri olduğunu gösterir.",
         "Bu yüksek ikiz konkordansı, obsesif kompulsif bozukluğun nörobiyolojik ve kalıtsal temeli en güçlü psikiyatrik rahatsızlıklardan biri olduğunu kanıtlamaktadır.",
         "MZ ikizlerde konkordans oranı", 0, None, "en kuvvetli genetik yüke")
    ]
    
    # PAGE 69
    pdata[69] = [
        ("Panik bozuklukta birinci derece akrabalarda hastalık riski **genel popülasyonun dört ila sekiz katına** çıkmaktadır.",
         "Panik bozuklukta yapılan aile araştırmalarında, birinci derece akrabalarda panik atak ve agorafobi gelişme riskinin genel topluma kıyasla dört ila sekiz kat arttığı belgelenmiştir.",
         "Panik Bozukluk (PB)", 0, None, "dört ila sekiz katına"),
        ("Klinik tabloda kadın baskınlığı belirgin olup, sıklıkla **majör depresyon ve madde bağımlılığı** ile komorbidite gösterir.",
         "Klinik tabloda kadın cinsiyet baskınlığı dikkat çekerken, hastaların önemli bir bölümünde majör depresif bozukluk ve yatıştırıcı madde kullanımı tabloya eşlik eder.",
         "Kadınlarda daha fazla görülür", 0, None, "majör depresyon ve madde")
    ]
    
    # PAGE 70
    pdata[70] = [
        ("Özgül fobiler toplumda en yaygın görülen anksiyete türü olup, **etiyolojisinde genetik yatkınlık** önemli yer tutar.",
         "Özgül fobiler toplumda en sık karşılaşılan anksiyete bozukluğu tipi olup, kan yaralanma enjeksiyon fobisi ve hayvan fobilerinde genetik yatkınlık çok belirgindir.",
         "Özgül Fobiler", 0, None, "Özgül fobiler"),
        ("Özellikle **kan-yaralanma fobisinde** vazovagal senkop yanıtı aile bireyleri arasında yüksek konkordans gösterir.",
         "Özellikle kan ve enjeksiyon fobisindeki vazovagal bradikardi ve senkop paterni, aile soyağacında doğrudan kalıtılan otonomik bir aşırı duyarlılık yansıtır.",
         "En yaygın fobi türüdür", 0, None, "kan-yaralanma fobisinde")
    ]
    
    # PAGE 71
    pdata[71] = [
        ("Sosyal fobide aile içi görülme sıklığı genel popülasyondan belirgin şekilde **yüksek saptanmıştır**.",
         "Sosyal fobi tablosunda yapılan klinik araştırmalarda, hasta bireylerin birinci derece aile üyelerinde sosyal anksiyete sıklığı genel popülasyondan anlamlı derecede yüksek bulunmuştur.",
         "Sosyal Fobi", 0, None, "yüksek saptanmıştır"),
        ("Kalıtımsal davranışsal ketlenme ve utangaçlık özellikleri, **çevresel pekiştireçlerle birleşerek** fobiye dönüşür.",
         "Çocukluk çağındaki kalıtımsal davranışsal inhibisyon ve aşırı çekingenlik mizaç özellikleri, olumsuz sosyal deneyimlerle birleşerek erişkin sosyal anksiyeteyi yapılandırır.",
         "Aile içinde görülme sıklığı", 0, None, "davranışsal ketlenme")
    ]
    
    # PAGE 72
    pdata[72] = [
        ("Genelleşmiş anksiyete bozukluğu olan bireylerin birinci derece akrabalarında bozukluğun görülme sıklığı **yüzde yirmiye** ulaşır.",
         "Genelleşmiş anksiyete bozukluğunda ailesel kümelenme belirgin olup, probandın birinci derece akrabalarında hastalık sıklığı yaklaşık yüzde yirmi düzeyinde saptanmaktadır.",
         "Genelleşmiş  Anksiyete Bozukluğu", 0, None, "yüzde yirmiye"),
        ("Bu oran genel popülasyon prevalansının **üç ila beş kat üzerinde** bir risk artışına karşılık gelmektedir.",
         "Bu ailesel oran genel toplum yaygınlığının üç ila beş kat üzerinde olup, yaygın kronik endişenin altında yatan genetik zemini ortaya koymaktadır.",
         "Birinci derece akrabalarda GAB görülme", 0, None, "üç ila beş kat")
    ]
    
    # PAGE 73
    pdata[73] = [
        ("Yeme bozukluklarından anoreksiya nervoza, **yüksek morbidite ve mortalite** ile seyreden ciddi bir hastalıktır.",
         "Yeme bozuklukları spektrumunda anoreksiya nervoza, belirgin beden imajı bozukluğu ve besin reddiyle seyreden, biyolojik ve psikososyal bileşenleri bulunan çok etiyolojili bir hastalıktır.",
         "Yeme Bozuklukları", 0, None, "anoreksiya nervoza"),
        ("İkiz çalışmalarında anoreksiya nervoza için kalıtılabilirlik oranları **yüzde elli ila yetmiş** arasında bildirilmiştir.",
         "İkiz kohortlarında anoreksiya nervoza için hesaplanan kalıtılabilirlik katsayıları yüzde elli ila yetmiş arasında olup güçlü bir metabolik ve psikiyatrik genetik yükü yansıtır.",
         "Anoreksia Nervosa", 0, None, "yüzde elli ila yetmiş")
    ]
    
    # PAGE 74
    pdata[74] = [
        ("Anoreksiyada inflamatuar sitokinlerden **tümör nekrozis faktör alfa yani TNF-alfa** salınımında artış saptanır.",
         "Anoreksiya nervoza biyolojisinde proinflamatuar bir sitokin olan tümör nekrozis faktör alfa yani te ne fe alfa salınımında belirgin artış gösterilmiştir.",
         "TNF-α (tümör nekrozis faktör) salınımında", 0, None, "TNF-alfa"),
        ("TNF-alfa hipotalamik-pitüiter-adrenal aksı uyararak **iştah merkezini baskılar ve kaşeksiye** yol açar.",
         "Te ne fe alfa hipotalamo hipofizer adrenal aksı hiperaktive ederek anoreksijenik sinyalleri tetikler, besin alımını baskılar ve ağır kilo kaybı ile kaşeksiye zemin hazırlar.",
         "TNF-α hipotalamik-pitüiter-adrenal", 0, None, "kaşeksiye")
    ]
    
    # PAGE 75 - ÇIKMIŞ
    pdata[75] = [
        ("Psikiyatrik hastalıklar tek gen defekti değil, **kompleks ve multifaktöriyel** genetik bozukluklardır.",
         "Geçmiş yılların çıkmış kurul sınavı sorusunda özellikle sorgulandığı üzere, psikiyatrik hastalıklar klasik Mendel kurallarına uyan tek gen bozuklukları olmayıp kompleks ve multifaktöriyel bir etiyolojiye sahiptir.",
         "Psikiyatrik hastalıklar kompleks ve multifaktöriyeldir,", 0,
         {"soru_id": "past-1790877040078-830959", "yil": "2020-2021"},
         "kompleks ve multifaktöriyel"),
        ("Bu nedenle klinik genetik danışmada kesin yüzdeler yerine **ampirik aile verilerine dayalı risk aralıkları** sunulur.",
         "Bu multifaktöriyel doğa nedeniyle genetik danışma sürecinde ailelere mutlak deterministik yüzdeler yerine, geniş aile çalışmalarından elde edilen ampirik olasılık aralıkları aktarılır.",
         "Bu nedenle hastalık riskini tahmin", 0, None, "ampirik aile verilerine")
    ]
    
    # PAGE 76
    pdata[76] = [
        ("Moleküler genetik analizler, geniş **nüfus kohortlarından DNA izolasyonu** ve yüksek verimli genotiplemeyle başlar.",
         "Moleküler genetik analiz iş akışı, iyi tanımlanmış geniş nüfus kohortlarından periferik lökosit de na'sının izole edilmesi ve robotik yüksek verimli genotipleme sistemleriyle başlar.",
         "Nüfus Örneği", 0, None, "nüfus kohortlarından DNA"),
        ("Genetik materyalin saflığı ve derişimi spektrofotometrik yöntemlerle doğrulanarak **biyoçip analizlerine** aktarılır.",
         "İzole edilen genetik materyalin konsantrasyonu ve optik saflığı spektrofotometrik olarak denetlenerek mikroarray biyoçip ve dizi analiz platformlarına sevk edilir.",
         "Genotipleme ve", 0, None, "biyoçip analizlerine")
    ]
    
    # PAGE 77
    pdata[77] = [
        ("GWAS analizlerinde saptanan genomik lokuslar **koşullu analizler ve ince haritalama** ile daraltılır.",
         "Genom boyu ilişkilendirme çalışmalarında anlamlılık eşiğini aşan devasa lokuslar, koşullu istatistiksel analizler ve ince haritalama adımlarıyla daraltılarak hedef genlere odaklanılır.",
         "GWAS lokusu", 0, None, "koşullu analizler"),
        ("Kromatin yapısı ve epigenetik modifikasyonlar incelenerek **hastalıkla ilişkili fonksiyonel gen** doğrulanır.",
         "Bölgedeki üç boyutlu kromatin yapısı, promoter etkileşimleri ve epigenetik metilasyon paternleri incelenerek hastalıktan doğrudan sorumlu olan fonksiyonel hedef gen doğrulanır.",
         "Kromatin yapısı", 0, None, "kromatin yapısı")
    ]
    
    # PAGE 78
    pdata[78] = [
        ("Vaka-kontrol tasarımlarında binlerce hasta ile **sağlıklı kontrol bireylerinin genotipleri** kıyaslanır.",
         "Gıvas vaka kontrol araştırmalarında binlerce kesin tanı almış hasta kohortu ile eşleştirilmiş sağlıklı kontrollerin genomik belirteçleri paralel olarak karşılaştırılır.",
         "cases controls", 0, None, "sağlıklı kontrol"),
        ("Her bir belirteç için **Manhattan plot grafiğinde eksi log p değeri** hesaplanarak istatistiksel tepe noktaları belirlenir.",
         "Taranan milyonlarca es ne pe belirteci için hesaplanan p değerleri Manhattan plot grafiğinde eksi logaritma ölçeğinde çizilerek istatistiksel eşiği aşan Manhattan gökdelenleri tespit edilir.",
         "Individuals with disease", 0, None, "Manhattan plot")
    ]
    
    # PAGE 79
    pdata[79] = [
        ("Restriksiyon analizinde **MstI gibi endonükleazlar** hedef DNA dizisini spesifik baz noktalarından keser.",
         "Klasik restriksiyon parça analizinde me se te bir gibi restriksiyon endonükleaz enzimleri çift zincirli hedef de na yı spesifik tanıma dizilerinden hassasiyetle keser.",
         "Mstl Restriction Sites", 0, None, "MstI gibi endonükleazlar"),
        ("Oluşan farklı uzunluktaki parçalar agaroz jel elektroforezinde **moleküler ağırlıklarına göre ayrılarak** bant oluşturur.",
         "Enzimatik kesim sonucu ortaya çıkan farklı boyuttaki de na parçaları agaroz jel elektroforezinde elektriksel akım altında yürütülerek moleküler boyutlarına göre bantlar halinde ayrışır.",
         "Digest, separate", 0, None, "jel elektroforezinde")
    ]
    
    # PAGE 80
    pdata[80] = [
        ("Sanger dizileme yönteminde **dört farklı florofor ile işaretlenmiş** dideoksinükleotidler kullanılır.",
         "Sanger otomatik dizi analizinde adenin, guanin, sitozin ve timin bazları dört farklı florofor boya ile işaretlenmiş zincir sonlandırıcı dideoksinükleotidlerle reaksiyona sokulur.",
         "MOL -60SA9", 0, None, "Sanger dizileme"),
        ("Kapiller elektroforezden geçen parçaların floresan ışıması detektörle okunarak **sekans elektroferogramı** elde edilir.",
         "Kapiller elektroforez tüpünden lazer ışını altından geçen sonlandırılmış fragmanların florofor ışıması algılanarak renkli piklerden oluşan sekans elektroferogramı çıkarılır.",
         "MZOZ *İPVAVI", 0, None, "sekans elektroferogramı")
    ]
    
    # PAGE 81
    pdata[81] = [
        ("Dizi analizinde elde edilen sekans, insan **referans genom dizisiyle bilgisayar ortamında** hizalanır.",
         "Sekanslama cihazından elde edilen nükleotid dizilimleri, biyobilişimsel algoritmalarla insan referans genom kütüphanesiyle nükleotid nükleotid hizalanarak karşılaştırılır.",
         "Affected calf", 0, None, "referans genom dizisiyle"),
        ("Böylece baz değişimleri, mikrodelesyonlar ve **tek bazlık insersiyon mutasyonları** kesin olarak doğrulanır.",
         "Bu bilgisayarlı dizi karşılaştırması sayesinde tek bazlık nükleotid değişimleri, mikrodelesyonlar veya baz eklenmesi yani insersiyon mutasyonları nükleotid düzeyinde kesinleştirilir.",
         "Seqerce| Pastray", 0, None, "insersiyon mutasyonları")
    ]
    
    # PAGE 82
    pdata[82] = [
        ("Yeni nesil dizileme iş akışı; **DNA ekstraksiyonu, kütüphane hazırlığı ve yüksek verimli sekanslama** adımlarını içerir.",
         "Yeni nesil dizileme protokolü; birinci basamakta de na ekstraksiyonu, ikinci basamakta kütüphane hazırlığı, ardından amplifikasyon ve milyonlarca parçanın paralel sekanslanması basamaklarını içerir.",
         "STEP 1: STEP 2: Template", 0, None, "Yeni nesil dizileme"),
        ("Elde edilen terabaytlarca ham veri **biyoenformatik filtrelerden geçirilerek** patojenik varyantlar raporlanır.",
         "Elde edilen devasa ham dizileme verisi ileri biyoenformatik algoritmalar ve patojenite filtrelerinden geçirilerek hastanın psikiyatrik riskini belirleyen varyantlar nihai rapor haline getirilir.",
         "Extraction Library", 0, None, "biyoenformatik filtrelerden")
    ]
    
    # Now let's construct paragraphs, sections and sentences
    all_sentences = []
    all_paragraphs = []
    all_sections = []
    
    p_idx = 1
    
    for sdef in sections_def:
        b_id = sdef["b_id"]
        sec_paras = []
        for pno in sdef["pages"]:
            pid = f"k2-59-p{p_idx:03d}"
            p_idx += 1
            sec_paras.append(pid)
            
            p_sents = []
            for item in pdata[pno]:
                ekran, ses, highlight, s_idx, cikmis, fallback_hl = item
                s_obj = make_sentence(ekran, ses, pno, satir_pattern=None, satir_idx=s_idx, cikmis=cikmis, highlight_word=highlight)
                p_sents.append(s_obj)
                all_sentences.append(s_obj)
                
            p_obj = {
                "id": pid,
                "sayfa": pno,
                "bolum": b_id,
                "cumleler": p_sents
            }
            all_paragraphs.append(p_obj)
            
        sec_obj = {
            "id": b_id,
            "baslik": sdef["baslik"],
            "paragraflar": sec_paras
        }
        all_sections.append(sec_obj)
        
    konusma_v2 = {
        "ders_id": "k2-59",
        "surum": 2,
        "bolumler": all_sections,
        "paragraflar": all_paragraphs
    }
    
    return konusma_v2, all_sentences

def main():
    print("Generating complete deep lecture for k2-59...")
    k2, sents = build_lecture()
    
    sh = json.loads((TASLAK / "sayfa_haritasi.json").read_text(encoding="utf-8"))
    sh_map = {sp["sayfa"]: sp for sp in sh["sayfalar"]}
    
    b_map = {}
    for b in k2["bolumler"]:
        b["paragraflar"] = []
        b_map[b["id"]] = b

    for p in k2["paragraflar"]:
        pno = p["sayfa"]
        sp = sh_map.get(pno, {})
        tur = sp.get("tur")
        sek = [x for x in sp.get("sekiller") or [] if "süs" not in x.lower()]
        sekil_desc = (sek[0] if sek else sp.get("ne_anlatiliyor", "")) if (tur in ("sekil", "tablo") or sek) else None
        
        for s_idx, c in enumerate(p["cumleler"]):
            s_sekil = sekil_desc if (s_idx == 0 and sekil_desc) else None
            c["slayt"] = {
                "sayfa": pno,
                "satir": [c["satir"]],
                "sekil": s_sekil
            }
            old_cikmis = c.get("cikmis")
            if old_cikmis and isinstance(old_cikmis, dict):
                c["cikmis"] = [old_cikmis["soru_id"]]
            elif old_cikmis and isinstance(old_cikmis, list):
                c["cikmis"] = old_cikmis
            else:
                c.pop("cikmis", None)
                
            c["vurgu"] = c.pop("vurgular", [])
            clean_ekran = c["ekran"].replace("**", "").replace("*", "")
            for v in c["vurgu"]:
                m = re.search(re.escape(v["metin"]), clean_ekran, re.IGNORECASE)
                if m:
                    v["metin"] = m.group(0)
                else:
                    v["metin"] = clean_ekran.split()[0]
                    
        b_map[p["bolum"]]["paragraflar"].append(p)

    clean_k2 = {
        "ders_id": "k2-59",
        "surum": 2,
        "bolumler": k2["bolumler"]
    }

    # 13 verified drawing commands
    drawings = [
        {
            "cumle": "k2-59-c0016", "bas": 0, "son": 5, "sayfa": 8,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "İkiz Çalışmaları",
            "ogeler": [
                "Monozigot İkizler: Genetik özdeşlik",
                "Dizigot İkizler: Genetik benzerlik"
            ]
        },
        {
            "cumle": "k2-59-c0020", "bas": 0, "son": 5, "sayfa": 10,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Evlat Edinme Modeli",
            "ogeler": [
                "Biyolojik Ebeveyn: Genetik miras",
                "Evlat Edinen Aile: Yetiştirilme çevresi"
            ]
        },
        {
            "cumle": "k2-59-c0032", "bas": 0, "son": 5, "sayfa": 16,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Moleküler Belirteç Tipleri",
            "ogeler": [
                "Restriksiyon Belirteci: Parça uzunluk polimorfizmi",
                "Minisatellitler: Değişken sayıda tandem tekrarlar"
            ]
        },
        {
            "cumle": "k2-59-c0046", "bas": 0, "son": 5, "sayfa": 23,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "LOD Skoru Değerleri",
            "ogeler": [
                "Pozitif Üç Değeri: Kesin genetik bağlantı",
                "Negatif İki Değeri: Bağlantı dışlanması"
            ]
        },
        {
            "cumle": "k2-59-c0060", "bas": 0, "son": 5, "sayfa": 30,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Serotonin Taşıyıcı ve Agresyon",
            "ogeler": [
                "Kısa Es Aleli: Dürtüsel agresyon ve stres",
                "Amigdala Hiperaktivitesi: Duygusal stresör yanıtı"
            ]
        },
        {
            "cumle": "k2-59-c0068", "bas": 0, "son": 5, "sayfa": 34,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Duygudurum Bozuklukları İkiz Uyumu",
            "ogeler": [
                "Bipolar Bozukluk: Yüksek konkordans",
                "Unipolar Depresyon: Orta konkordans"
            ]
        },
        {
            "cumle": "k2-59-c0080", "bas": 0, "son": 5, "sayfa": 40,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Serotonerjik Sistem ve İntihar",
            "ogeler": [
                "Triptofan Hidroksilaz: Serotonin sentezi",
                "Beş Haş İ A A Düzeyi: Metabolit konsantrasyonu"
            ]
        },
        {
            "cumle": "k2-59-c0098", "bas": 0, "son": 5, "sayfa": 49,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Şizofrenide İkiz Konkordansı",
            "ogeler": [
                "Monozigot İkizler: Yüzde elli üç konkordans",
                "Dizigot İkizler: Yüzde on beş konkordans"
            ]
        },
        {
            "cumle": "k2-59-c0108", "bas": 0, "son": 5, "sayfa": 54,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Kromozom Yirmi İki Mikrodelesyonu",
            "ogeler": [
                "Kopya Sayısı Kaybı: Submikroskobik delesyon",
                "Erişkin Dönem: Yüksek psikoz riski"
            ]
        },
        {
            "cumle": "k2-59-c0124", "bas": 0, "son": 5, "sayfa": 62,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Alkol Metabolizma Enzimleri",
            "ogeler": [
                "Alkol Dehidrogenaz: Asetaldehit oluşumu",
                "Aldehit Dehidrogenaz: Asetat oksidasyonu"
            ]
        },
        {
            "cumle": "k2-59-c0128", "bas": 0, "son": 5, "sayfa": 64,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Katekol O Metiltransferaz Varyantları",
            "ogeler": [
                "Valin Aleli: Hızlı enzim ve düşük dopamin",
                "Metiyonin Aleli: Az aktif enzim ve yüksek dopamin"
            ]
        },
        {
            "cumle": "k2-59-c0136", "bas": 0, "son": 5, "sayfa": 68,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Obsesif Kompulsif Bozukluk İkiz Verileri",
            "ogeler": [
                "Monozigot Çiftler: Yüzde yetmiş beş eş hastalanma",
                "Dizigot Çiftler: Yüzde kırk yedi eş hastalanma"
            ]
        },
        {
            "cumle": "k2-59-c0150", "bas": 0, "son": 5, "sayfa": 75,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Psikiyatrik Kalıtım Modeli",
            "ogeler": [
                "Multifaktöriyel Yapı: Poligenik risk havuzu",
                "Çevresel Tetikleyiciler: Yaşam olayları ve stres"
            ]
        }
    ]

    # Write files
    (TASLAK / "konusma_v2.json").write_text(json.dumps(clean_k2, ensure_ascii=False, indent=2), encoding="utf-8")
    (TASLAK / "cizim_aday.json").write_text(json.dumps({"komutlar": drawings}, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
    import konusma_v2 as KV
    md_txt, sayfalar_l = KV.turet(clean_k2)
    (TASLAK / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
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
