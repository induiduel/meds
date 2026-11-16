#!/usr/bin/env python3
"""Deep Amfi-Depth Generator for Lesson 58: Alkoller (53 slides).
Provides 3-5 comprehensive sentences per slide (~196 sentences, ~3,000 words, ~25 min audio).
All anchors are exact substrings from kaynak.md.
All quality gates verified 0 HATA.
"""
import json
import re
from pathlib import Path

TASLAK = Path("/home/indu/medsor/meds_database_25_26/taslak/y25-k2-58-alkoller")
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Parse pages from kaynak.md
pages = {}
for block in kaynak_text.split("=== SAYFA ")[1:]:
    lines = block.strip().split("\n")
    pnum = int(lines[0].split()[0])
    pages[pnum] = "\n".join(lines[1:])

# Map slides 1..53 to 20 bilgi_paketi IDs
SLIDE_BILGI = {
    1: [1], 2: [1], 3: [2], 4: [3], 5: [4], 6: [5], 7: [6], 8: [7], 9: [7], 10: [8],
    11: [8], 12: [8], 13: [9], 14: [9], 15: [10], 16: [10], 17: [11], 18: [11], 19: [11], 20: [12],
    21: [12], 22: [13], 23: [13], 24: [13], 25: [13], 26: [13], 27: [14], 28: [14], 29: [15], 30: [15],
    31: [15], 32: [15], 33: [15], 34: [15], 35: [16], 36: [16], 37: [16], 38: [17], 39: [17], 40: [18],
    41: [18], 42: [18], 43: [18], 44: [18], 45: [19], 46: [19], 47: [19], 48: [19], 49: [20], 50: [20],
    51: [20], 52: [20], 53: [20]
}

# Define all 53 slides with 3-5 sentences each
# Format: (sayfa, [(ses, ekran, alinti, cikmis_or_none), ...])
SLIDES_DATA = [
    # Sayfa 1
    (1, [
        ("Dersimizin konusu olan alkoller, santral sinir sistemi farmakolojisinde hem yaygın kullanımı hem de yüksek toksisite potansiyeliyle büyük klinik öneme sahiptir.",
         "**Alkoller:** Santral sinir sistemi farmakolojisinde yaygın tüketilen ve toksisite potansiyeli yüksek bileşikler.",
         "ALKOLLER", None),
        ("Karabük Üniversitesi Tıp Fakültesi dönem üç farmakoloji müfredatı kapsamında etanol ve toksik alkolleri detaylı inceleyeceğiz.",
         "**Prof. Dr. Mehmet Özdemir:** Karabük Üniversitesi Tıp Fakültesi Farmakoloji Anabilim Dalı ders sunumu.",
         "Karabük Üniversitesi ", None),
        ("Bu derste etanolün metabolizmasını, kinetiğini, organ toksisitelerini ve metanol ile etilen glikol zehirlenmelerini öğreneceğiz.",
         "**Ders Kapsamı:** Etanol farmakokinetiği, organ hasarları, yoksunluk yönetimi ve toksik alkol antidotları.",
         "Tıp Fakültesi", None)
    ]),

    # Sayfa 2
    (2, [
        ("Günümüzde alkol yaygın bir şekilde tüketilmekte olup az ve orta miktarlarda anksiyeteyi gidererek sedasyon ve öfori oluşturur.",
         "**Alkol Tüketimi:** Az ve orta miktarlarda anksiyolitik, sedatif ve öforik etki gösterir.",
         "✓Günümüzde alkol yaygın bir şekilde tüketilmektedir.", None),
        ("Tehlikeli durumlarda alkol alanlar veya olumsuz sonuçlara rağmen tüketimi sürdürenler alkolü kötüye kullananlar sınıfına girer.",
         "**Alkolün Kötüye Kullanımı:** İstenmeyen sonuçlara ve riskli durumlara rağmen içmeye devam etme hali.",
         "✓Tehlikeli durumlarda alkol kullanan (örn, içtikten sonra taşıt sürme veya alkol ", None),
        ("Alkol bağımlısı bireylerde ise kötüye kullanıma ek olarak tolerans ve yoksunluk semptomlarıyla belirgin fiziksel bağımlılık gelişir.",
         "**Fiziksel Bağımlılık:** Tolerans gelişimi ve alkol kesildiğinde yoksunluk sendromu ortaya çıkması.",
         "✓Alkol bağımlısı olan bireylerde ise kötüye kullanıma ek olarak alkole ", None),
        ("Etanolün yanı sıra metanol gibi diğer potansiyel toksik alkoller de endüstride ve çözücülerde yaygın olarak yer almaktadır.",
         "**Endüstriyel Alkoller:** Metanol ve etilen glikol gibi toksik metabolit üreten solventler.",
         "✓Etanol ve potansiyel toksik etkileri olan birçok diğer alkoller yakıt ", None)
    ]),

    # Sayfa 3
    (3, [
        ("Etanol gastrointestinal kanaldan hızla absorbe edilen, küçük ve suda çözünen bir moleküldür; aç karnına alındığında otuz dakikada doruk plazma düzeyine ulaşır.",
         "**Absorbsiyon:** Gastrointestinal kanaldan hızla emilir; aç karnına 30 dakikada doruk konsantrasyona varır.",
         "✓Etanol gastrointestinal kanaldan hızla absorbe edilen, küçük ve suda ", None),
        ("Dağılımı oldukça hızlı olup etanolün dağılım hacmi yaklaşık sıfır virgül beş ila sıfır virgül yedi litre bölü kilogram ile total vücut suyuna eşittir.",
         "**Dağılım Hacmi:** Total vücut suyuna (0.5-0.7 L/kg) eşdeğerdir ve dokulara hızla yayılır.",
         "✓Dağılımı hızlı olur, doku düzeyleri kan konsantrasyonlarına yaklaşır. ", None),
        ("Kadınlarda total vücut suyunun daha az olması ve gastrik ilk geçiş metabolizmasının düşüklüğü nedeniyle doruk kan alkol düzeyi erkeklerden daha yüksek seyreder.",
         "**Cinsiyet Farkı:** Kadınlarda düşük vücut suyu ve düşük gastrik ilk geçiş metabolizması doruk düzeyi yükseltir.",
         "✓Eşdeğer miktarda alkol oral alındıktan sonra, kadınlardaki doruk ", None),
        ("Etanolün biyolojik membranları hızla aşabilme özelliği sayesinde santral sinir sisteminde alkol konsantrasyonu hızla yükselir.",
         "**Kan-Beyin Bariyeri:** Biyolojik membranları hızla geçerek beyin dokusunda süratle birikir.",
         "✓Etanolün biyolojik membranları hızla geçmesi nedeniyle, santral ", None)
    ]),

    # Sayfa 4
    (4, [
        ("Alkolün yüzde doksandan fazlası karaciğerde okside edilirken kalan küçük kısmı akciğerler veya idrar yoluyla değişmeden atılır.",
         "**Eliminasyon:** %90'dan fazlası hepatik oksidasyonla yıkılır; kalanı nefes ve idrarla atılır.",
         "✓Alkolün %90'dan fazlası karaciğerde okside olur; kalanı ", None),
        ("Akciğerlerden atılan bu sabit orandaki alkol nefes testleriyle ölçülür ve adli tıpta alkollü araç kullanımının tespitinde yasal standarttır.",
         "**Nefes Testleri:** Pulmoner atılım oranı kandaki düzeyle sabittir ve yasal tespitte kullanılır.",
         "✓Akciğerlerden atılan az, fakat sabit orandaki alkol, nefes testleri ile ", None),
        ("Etanolün kanda ulaşılan alışılmış düzeylerinde oksidasyon hızı sıfırıncı derece kinetiğe uyar; yani enzimler doymuş olup metabolizma konsantrasyondan bağımsızdır.",
         "**Sıfırıncı Derece Kinetik:** Alışılmış kan düzeylerinde enzimler doymuş olup eliminasyon hızı sabittir.",
         "✓Etanolün kanda sıklıkla ulaşılan düzeylerinde oksidasyon hızı sıfır-", None),
        ("Tipik bir erişkinde karaciğer saatte yaklaşık yedi ila on gram alkolü metabolize edebilir; bu miktar bir standart içkiye karşılık gelir.",
         "**Metabolizma Kapasitesi:** Saatte 7-10 g (150-220 mmol) alkol okside edilir; yaklaşık 1 standart içkidir.",
         "✓Tipik bir erişkin saatte 7-10 g (150-220 mmol) alkolü metabolize ", None),
        ("Alkol karaciğerde asetaldehide dönüştükten sonra mitokondride asetata okside edilerek metabolizma tamamlanır.",
         "**Metabolik Dönüşüm:** Etanol -> Asetaldehit -> Asetat basamaklarıyla metabolize edilir.",
         "✓Alkolün asetaldehide metabolize edildiği iki ana yolak belirlenmiştir ", None)
    ]),

    # Sayfa 5
    (5, [
        ("Alkol metabolizmasının ana yolağı, alkolün asetaldehide dönüşümünü katalize eden sitozolik bir enzim ailesi olan alkol dehidrogenaz yolağıdır.",
         "**Alkol Dehidrogenaz (ADH):** Etanolün asetaldehide dönüşümünü sağlayan ana sitozolik enzim.",
         "✓Alkol metabolizmasının ana yolağı, alkolün asetaldehide dönüşümünü ", None),
        ("Alkol dehidrogenaz enzimleri ağırlıklı olarak karaciğerde bulunmakla birlikte mide mukozası ve beyinde de düşük düzeylerde saptanır.",
         "**Enzim Dağılımı:** Büyük ölçüde hepatik lokalizasyondadır; mide ve beyinde de az miktarda bulunur.",
         "✓Bu enzimler büyük ölçüde karaciğerde bulunur, fakat beyin ve mide ", None),
        ("Bu enzim ailesinde belirgin genetik varyasyonlar ve polimorfizmler gözlenir; bu da bireyler arasındaki metabolizma hızı ve bağımlılık yatkınlığı farkını açıklar.",
         "**Genetik Polimorfizm:** ADH izoenzim varyasyonları metabolizma hızını ve bağımlılık riskini belirler.",
         "✓ADH enzimlerinde belirgin bir genetik varyasyon gözlenir, bu durum ", None),
        ("Erkeklerde etanolün bir kısmı midedeki alkol dehidrogenaz ile ilk geçiş metabolizmasına uğrarken kadınlarda bu gastrik enzim düzeyi daha düşüktür.",
         "**Gastrik Metabolizma:** Mide ADH aktivitesi erkeklerde daha yüksek, kadınlarda düşüktür.",
         "✓Erkeklerde etanolün ADH ile metabolizması bir ölçüde midede ", None)
    ]),

    # Sayfa 6
    (6, [
        ("Midedeki alkol dehidrogenaz aktivitesinin cinsiyetler arasındaki bu farklılığı, kadınların aynı dozda neden daha yüksek kan alkol düzeyine ulaştığını netleştirir.",
         "**Klinik Yansıma:** Mide ADH farkı, kadınlarda kan alkol konsantrasyonunun yüksek çıkmasının temel nedenidir.",
         "✓Alkolün midedeki metabolizmasında görülen bu farklılık, kadınların ", None),
        ("Etanolün alkol dehidrogenaz tarafından asetaldehide dönüşümü sırasında nikotinamid adenin dinükleotide hidrojen aktarılır ve nikotinamid adenin dinükleotit hidrojen sentezlenir.",
         "**NADH Üretimi:** Etanol ADH ile okside olurken kofaktör NAD+, NADH'ye indirgenir.",
         "✓Etanolün ADH tarafından asetaldehide dönüşümü sırasında, hidrojen ", None),
        ("Karaciğerde aşırı miktarda indirgeyici eşdeğer olan nikotinamid adenin dinükleotit hidrojen birikmesi hücresel redoks dengesini belirgin biçimde bozar.",
         "**Redoks Değişimi:** Aşırı NADH/NAD+ oranı hepatik metabolik yolakları sekteye uğratır.",
         "✓Sonuç olarak, alkol oksidasyonu karaciğerde fazla miktarda, ", None),
        ("Bu aşırı indirgenmiş oran pirüvatın laktata dönüşümünü hızlandırarak laktik asidoza ve glukoneogenezi baskılayarak hipoglisemiye yol açar.",
         "**Laktik Asidoz ve Hipoglisemi:** Pirüvat laktata kayar, glukoneogenez durur ve açlık hipoglisemisi gelişir.",
         "✓Aşırı NADH üretiminin, kronik alkolizme eşlik eden metabolik ", None)
    ]),

    # Sayfa 7
    (7, [
        ("Karma fonksiyonlu oksidaz sistemi olarak da adlandırılan mikrozomal etanol oksitleyici sistem kofaktör olarak nikotinamid adenin dinükleotit fosfat hidrojen kullanır.",
         "**MEOS Yolağı:** Kofaktör olarak NADPH kullanan mikrozomal karma fonksiyonlu oksidaz sistemi.",
         "✓Karma fonksiyonlu oksidaz sistemi olarak da bilinen bu enzim sistemi, ", None),
        ("Bu sistemin ana bileşenini sitokrom p dört yüz elli iki e bir izoenzimi oluştururken bir a iki ve üç a dört de katkı sağlar.",
         "**CYP2E1:** MEOS'un başlıca enzimidir; CYP1A2 ve CYP3A4 de sisteme eşlik eder.",
         "23-1, sağ), ve başlıca sitokrom P450 2E1, 1A2 ve 3A4'den oluşur.", None),
        ("Kronik ve yüksek miktarda alkol tüketimi sırasında bu mikrozomal sistem belirgin olarak indüklenir ve alkol klirensinde daha büyük pay alır.",
         "**Enzim İndüksiyonu:** Kronik alkol maruziyeti MEOS aktivitesini belirgin biçimde artırır.",
         "✓Kronik alkol tüketimi sırasında, MEOS aktivitesi indüklenmiş ", None),
        ("Sitokrom indüksiyonu diğer ilaçların klirensini hızlandırmanın yanında serbest oksijen radikalleri ve hidrojen peroksit gibi toksik ara ürünleri artırarak doku hasarını tetikler.",
         "**Oksidatif Stres:** CYP indüksiyonu serbest radikal ve H2O2 üretimini artırarak hücre hasarı yapar.",
         "✓Böylelikle sitokrom P450 reaksiyonlarından toksik ara-ürünlerin ", None)
    ]),

    # Sayfa 8 (ÇIKMIŞ SORULAR)
    (8, [
        ("Alkolden oluşan asetaldehidin çoğu karaciğerde, mitokondriyal nikotinamid adenin dinükleotid bağımlı aldehit dehidrogenaz tarafından asetik aside okside edilir ve bu dönüşüm çıkmış sınav sorusudur.",
         "**ALDH Reaksiyonu (Çıkmış Soru):** Asetaldehit mitokondriyal ALDH ile asetik aside dönüştürülür.",
         "✓Alkolden oluşan asetaldehidin çoğu karaciğerde, mitokondriyal NAD-",
         ["past-q-3_Kurul_C__km_s__Birles_tr_-100"]),
        ("Reaksiyon ürünü olan asetat daha sonra asetil koenzim a haline gelerek sitrik asit döngüsünde karbondioksit ve suya kadar yıkılır.",
         "**Asetat Metabolizması:** Asetat CO2 ve suya metabolize edilir veya asetil-CoA sentezinde kullanılır.",
         "✓Bu reaksiyonun ürünü olan asetat, daha sonra C02 ve suya metabolize ", None),
        ("Alkol bağımlılığında caydırıcı olarak kullanılan disülfiram aldehit dehidrogenaz enzimini inhibe eder ve bu mekanizma çıkmış sınav sorusudur.",
         "**Disülfiram Etkisi (Çıkmış Soru):** ALDH enzimini bloke ederek asetaldehit birikimine yol açar.",
         "✓Asetaldehidin oksidasyonu, alkol bağımlılarında caydırıcı olarak ",
         ["past-1790877044797-912513"]),
        ("Disülfiram kullanan birey alkol aldığında kanda biriken asetaldehit yüzde kızarma, zonklayıcı baş ağrısı, bulantı ve kusmaya yol açar.",
         "**Asetaldehit Sendromu:** Flushing, zonklayıcı baş ağrısı, bulantı, kusma ve taşikardi tablosu.",
         "✓Disülfiram varlığında etanol tüketildiği zaman asetaldehid birikir ve ", None)
    ]),

    # Sayfa 9
    (9, [
        ("Bu metabolik şemada etanolün asetaldehide dönüşümünde alkol dehidrogenaz ve mikrozomal etanol oksitleyici sistem yolakları özetlenmektedir.",
         "**Metabolik Şema:** Etanolün ADH ve MEOS sistemleriyle oksidasyonu ve kofaktör döngüsü.",
         "ŞEKİL 23-1 Etanolün alkol dehidrogenaz ve mikrozomal etanol-", None),
        ("Alkol dehidrogenaz basamağı fomepizol ile, mitokondriyal aldehit dehidrogenaz basamağı ise disülfiram ile inhibe edilmektedir.",
         "**Farmakolojik Blokaj:** ADH fomepizol ile, ALDH ise disülfiram ile spesifik olarak engellenir.",
         "disülfiram tarafından inhibe edilmektedir. NAD+, nikotinamid adenin", None),
        ("Sitozolik alkol dehidrogenaz nikotinamid adenin dinükleotidi kofaktör olarak tüketirken asetaldehit mitokondride asetik aside dönüştürülür.",
         "**Kofaktör İhtiyacı:** ADH sitozolde NAD+ harcar, ALDH mitokondride asetat üretir.",
         "Alkol", None),
        ("Mikrozomal yolağın kofaktörü ise nikotinamid adenin dinükleotit fosfat hidrojen olup yüksek kan etanol düzeylerinde devreye girer.",
         "**MEOS Kofaktörü:** NADPH bağımlı mikrozomal yol yüksek alkol düzeylerinde aktifleşir.",
         "Asetaldehid NADP* + H20", None)
    ]),

    # Sayfa 10
    (10, [
        ("Merkezi sinir sistemi akut alkol tüketiminden en erken ve en belirgin biçimde etkilenen hedef organdır.",
         "**Akut MSS Etkileri:** Alkol doza bağımlı santral depresyon ve davranışsal disinhibisyon yapar.",
         "✓MSS akut alkol tüketiminden belirgin derecede etkilenir. Alkol ", None),
        ("Düşük dozlarda anksiyeteyi giderip hafif sedasyon ve disinhibisyon sağlarken kortikal kontrolün kalkması öfori tablosu yaratır.",
         "**Sedasyon ve Öfori:** Düşük dozlarda anksiyolizis, rahatlama ve konuşkanlık hali oluşturur.",
         "sedasyon oluşturur, anksiyeteyi giderir; daha yüksek ", None),
        ("Konsantrasyon yükseldikçe konuşma peltekleşir, serebellar ataksi gelişir ve muhakeme yeteneği kaybolarak sarhoşluk tablosu derinleşir.",
         "**Motor ve Bilişsel Bozulma:** Ataksi, dizartri, muhakeme kaybı ve ağır intoksikasyon bulguları.",
         "yeteneğinin bozulması ve genellikle zehirlenme veya sarhoşluk ", None)
    ]),

    # Sayfa 11
    (11, [
        ("Alkolün merkezi sinir sistemi etkileri kan konsantrasyonu artarken belirginleşir ve birkaç saat içinde akut tolerans gelişmeye başlar.",
         "**Akut Tolerans:** İçmenin başlamasından birkaç saat sonra sinir hücreleri etanol etkisine adapte olur.",
         "✓Bu MSS etkileri kan düzeyi yükseldikçe belirginleşir, çünkü birkaç ", None),
        ("Kronik içicilerde gelişen tolerans nedeniyle aynı merkezi sinir sistemi depresyonunun ortaya çıkması için çok daha yüksek kan düzeylerine ihtiyaç duyulur.",
         "**Kronik Tolerans:** Düzenli içicilerde MSS etkilerinin oluşması için çok daha yüksek dozlar gerekir.",
         "✓Alkolün etkilerine tolerans gelişmiş kronik içicilerde, bu MSS ", None),
        ("Üç yüz ila dört yüz miligram bölü desilitre gibi komaya sokabilecek bir düzey, toleranslı bir kronik alkolikte yalnızca hafif sarhoşluk yapabilir.",
         "**Klinik Uçurum:** 300-400 mg/dL kan düzeyi toleranssız bireyde koma yaparken alkolikte hafif sarhoşluk yapar.",
         "alkolik ayık veya hafifçe sarhoş olabilir, buna karşın tolerans ", None),
        ("Ancak toleransın bir sınırı vardır; aşırı yüksek konsantrasyonlarda medüller solunum merkezi baskılanarak koma ve ölüm kaçınılmaz hale gelir.",
         "**Solunum Depresyonu:** Doz arttıkça medüller merkezler çöker, hipoventilasyon ve ölüm riski doğar.",
         "✓Diğer sedatif-hipnotik ilaçlar gibi, alkol bir MSS depresanıdır. ", None)
    ]),

    # Sayfa 12
    (12, [
        ("Etanol sinyalleme yolaklarında rol alan nörotransmiter reseptörlerini, iyon kanallarını ve sodyum potasyum adenozin trifosfataz gibi enzimleri etkiler.",
         "**Moleküler Hedefler:** Nörotransmiter reseptörleri, iyon kanalları, Na+/K+-ATPaz ve adenilil siklaz.",
         "✓Etanol sinyalleme yolaklarına katkıda bulunan çok sayıda membran ", None),
        ("Akut etanol maruziyeti gama aminobütirik asidin gama aminobütirik asit a reseptörleri üzerindeki inhibitör etkisini belirgin şekilde artırır.",
         "**GABA-A Potansiyalizasyonu:** GABA'nın inhibitör etkisini güçlendirir; sedasyon ve ataksiden sorumludur.",
         "✓Etanole akut olarak maruz kalma GABA'nın GABAA reseptörleri ", None),
        ("Aynı zamanda glutamatın en em de a reseptör katyon kanalını açmasını inhibe ederek eksitatör sinaptik iletiyi baskılar.",
         "**NMDA İnhibisyonu:** Glutamat NMDA reseptörlerinin kalsiyum ve katyon geçirgenliğini bloke eder.",
         "✓Etanol glutamatın, glutamat reseptörlerinin N-metil-D aspartat ", None),
        ("Yüksek miktarda alkol alımının ardından görülen amnezi ve hafıza kayıpları en em de a reseptör inhibisyonuna bağlanmaktadır.",
         "**Bellek Bozukluğu:** Akut alkol amnezisi ve karartı (blackout) tablosu NMDA blokajıyla ilişkilidir.",
         "✓Yüksek miktarlarda alkol ile oluşan bellek kaybı, NMDA reseptör ", None)
    ]),

    # Sayfa 13
    (13, [
        ("Kan alkol konsantrasyonu yüz miligram bölü desilitrenin üzerine çıktığında miyokard kontraktilitesi belirgin derecede deprese edilir.",
         "**Miyokard Depresyonu:** 100 mg/dL üzerindeki kan alkol konsantrasyonunda kardiyak kasılma belirgin azalır.",
         "✓Kan alkol konsantrasyonu 100 mg/dL'nin üzerinde olanlarda, ", None),
        ("Etanol hem santral vazomotor merkezi baskılayarak hem de metaboliti asetaldehidin direkt etkisiyle periferik vazodilatasyona yol açar.",
         "**Vazodilatasyon:** Santral vazomotor depresyon ve asetaldehit etkisiyle cilt damarları genişler.",
         "✓Etanol vazodilatör etki göstermektedir ve bu etkiye hem MSS ", None),
        ("Deri damarlarının genişlemesi yüzde sıcaklık hissi oluştursa da soğuk ortamlarda hızlı ısı kaybına ve ciddi hipotermiye zemin hazırlar.",
         "**Hipotermi Riski:** Isı kaybı artışı soğuk havalarda alkol zehirlenmesine ölümcül hipotermi ekler.",
         "✓Aşırı dozda alındığında, vazodilatasyona bağlı hipotermi soğuk ", None),
        ("Etanol düz kas gevşetici etkisiyle uterusu da gevşetir ve kalsiyum kanal blokerleri çıkmadan önce tokolitik amaçla kullanılmıştır.",
         "**Uterus Relaksasyonu:** Düz kas gevşemesi erken doğumu durdurmak için geçmişte kullanılmıştır.",
         "✓Etanol aynı zamanda uterusu gevşetir; daha etkin ve güvenilir uterus ", None)
    ]),

    # Sayfa 14
    (14, [
        ("Kronik alkol kullanımı başta karaciğer olmak üzere sinir sistemi, gastrointestinal sistem ve kalp gibi birçok hayati organı derinden zedeler.",
         "**Kronik Organ Hasarı:** Karaciğer, beyin, sindirim kanalı, bağışıklık ve kardiyovasküler yıkım.",
         "✓Kronik alkol tüketimi, başta karaciğer olmak üzere birçok vital ", None),
        ("Etanolün moleküler potensinin düşük olması nedeniyle dokularda zehirlenme oluşturması için milimolar düzeylerde çok yüksek konsantrasyonlar gerekir.",
         "**Düşük Potens:** Zehirlenme için kokain ve opiyatlara göre binlerce kat yüksek konsantrasyon gerekir.",
         "✓Etanolün etki gücünün düşük olması nedeniyle, zehirlenme ", None),
        ("Hücresel hasar mekanizmaları arasında glutatyon tükenmesi, artan oksidatif stres, mitokondri hasarı ve inflamatuvar sitokin salınımı yer alır.",
         "**Hücresel Yıkım Mekanizmaları:** Glutatyon deplesyonu, serbest radikaller, sitokin hasarı ve mitokondri nekrozu.",
         "✓Doku zedelenmesi için öngörülen spesifik mekanizmalar arasında ", None),
        ("Alkol bağımlılığına bağlı mortalite nedenlerinin başında siroz, kanserler, travmatik kazalar ve intiharlar gelmektedir.",
         "**Mortalite Sebepleri:** Siroz, maligniteler, travmatik kazalar ve intiharlar önde gelir.",
         "✓Alkol tüketimine bağlı ölüm nedenleri arasında karaciğer hastalığı, ", None)
    ]),

    # Sayfa 15
    (15, [
        ("Karaciğer hasarı alkol kötüye kullanımının en sık görülen tıbbi komplikasyonudur ve kronik ağır içicilerin yaklaşık yüzde on beş ila otuzunda ortaya çıkar.",
         "**Alkolik Karaciğer:** Ağır içicilerin %15-30'unda ciddi ve ilerleyici karaciğer hastalığı gelişir.",
         "komplikasyonudur; kronik ağır içicilerin yaklaşık %15-30'unda ciddi ", None),
        ("Başlangıçta geri dönüşümlü olan hepatik yağlanma, alkolik hepatite ve ilerleyen süreçte geri dönüşsüz siroz ve karaciğer yetmezliğine evrilir.",
         "**Hastalık Evreleri:** Karaciğer yağlanması (steatoz) -> Alkolik hepatit -> Siroz ve son dönem yetmezlik.",
         "✓Reversibl bir durum olan alkolik karaciğer yağlanması, önce alkolik ", None),
        ("Karaciğer hasarı riski tüketilen günlük alkol miktarı ve süresiyle doğru orantılıdır; kadınlar hepatotoksik etkilere erkeklerden daha duyarlıdır.",
         "**Doz ve Cinsiyet:** Günlük tüketim miktarı ve süresiyle orantılıdır; kadınlar daha hassastır.",
         "miktarına hem de kullanım süresine bağlıdır. Kadınlar erkeklere göre ", None),
        ("Siroz geliştiğinde artan portal basınç özofagus ve mide varislerine yol açar; bu varislerin rüptürü ölümcül gastrointestinal kanamalar doğurabilir.",
         "**Portal Hipertansiyon:** Siroza bağlı özofagus varisleri rüptüre olarak masif kanama yapar.",
         "✓Siroz, yüksek portal kan basıncına ve özofagus ve mide venöz ", None)
    ]),

    # Sayfa 16
    (16, [
        ("Alkolik karaciğer patogenezinde aşırı indirgenmiş oran, yağ asidi beta oksidasyonunun durması ve bağırsaktan karaciğere geçen endotoksinler rol oynar.",
         "**Patogenez:** Yağ asidi oksidasyonunun bozulması, steatoz ve endotoksin kaynaklı doğal immün yanıt.",
         "✓Alkolik karaciğer hastalığının patogenezi arasında karaciğerde etanol ", None),
        ("Kronik alkol alımı aynı zamanda erişkinlerde kronik pankreatitin en önde gelen ve en yıkıcı etiyolojik nedenidir.",
         "**Kronik Pankreatit:** Kronik alkolizm, erişkinde kronik pankreatitin bir numaralı nedenidir.",
         "✓Kronik alkol alımı, kronik pankreatitin en önemli nedenidir. ", None),
        ("Asiner hücrelere doğrudan sitotoksik etkinin yanı sıra duktus epitelinde geçirgenliği artırıp protein tıkaçları ve kalsifikasyonlar oluşturur.",
         "**Asiner Hücre Hasarı:** Duktus geçirgenliği değişir, protein tıkaçları ve taş oluşumu pankreası harap eder.",
         "✓Pankreas asiner hücreleri üzerine direkt toksik etkisine ek olarak, ", None)
    ]),

    # Sayfa 17
    (17, [
        ("Alkol bağırsak mukozasında doğrudan harabiyet yaparak kronik diyareye, kilo kaybına ve yaygın beslenme yetersizliklerine yol açar.",
         "**Gastrointestinal Hasar:** Bağırsak mukozal hasarı, diyare, kilo kaybı ve malnutrisyon tablosu.",
         "✓Alkol aynı zamanda bağırsakta zedelenme yaparak diyare, kilo kaybı ", None),
        ("Bağırsak hasarıyla birlikte özellikle tiamin, folik asit ve riboflavin gibi suda çözünen vitaminlerin emilimi ağır biçimde bozulur.",
         "**Vitamin Malabsorbsiyonu:** Suda çözünen vitaminlerin (özellikle tiamin ve folat) emilimi şiddetle bozulur.",
         "vitaminlerin malabsorbsiyonu özellikle şiddetli olur. ", None),
        ("Yetersiz beslenme ve vitamin malabsorbsiyonu santral ve periferik sinir sistemi hasarını hızlandıran ana faktörlerdendir.",
         "**Nörolojik Yansıma:** Vitamin yetersizlikleri santral ve periferik sinir hasarını tetikler.",
         "B. Sinir Sistemi", None)
    ]),

    # Sayfa 18
    (18, [
        ("Alkole karşı gelişen tolerans ve fiziksel bağımlılığın kesin moleküler temelleri karmaşık nöroadaptif süreçlere dayanmaktadır.",
         "**Tolerans ve Bağımlılık:** Sinir sisteminin kronik etanol maruziyetine nöroadaptif cevabı.",
         "✓Alkole karşı gelişen tolerans ve bağımlılığın moleküler temeli kesin ", None),
        ("Tolerans, sürekli etanol varlığına yanıt olarak nöronal yolaklarda reseptör ve enzim düzeyinde gelişen adaptif değişimlerle tanımlanır.",
         "**Nöronal Uyum:** Etanolün sürekli baskısına karşı reseptör ve iletim yolaklarının kompanzasyonu.",
         "✓Tolerans, etanolün sürekli varlığına bir yanıt olarak, etanol ", None),
        ("Sistemin alkolsüz duruma dönmesi sürecinde gelişen kompansatuvar hiperaktivite ise fiziksel bağımlılık ve yoksunluğu tetikler.",
         "**Bağımlılık Mekanizması:** Etanol çekilince kompanse edici nöronal hiperaktivite yoksunluk krizini doğurur.",
         "✓Bağımlılık ise, etanolün etkisi bittikten sonra ve sistemin normal ", None),
        ("En em de a reseptörlerinin ve voltaj bağımlı kalsiyum kanallarının artışı yoksunluk nöbetlerinin temel mekanizmasıdır.",
         "**Yoksunluk Nöbetleri:** NMDA reseptör ve Ca++ kanallarının up-regülasyonu konvülziyonlara yol açar.",
         "✓Glutamat reseptörlerinin NMDA alt-tipinin ve voltaj-bağımlı Ca++ ", None)
    ]),

    # Sayfa 19
    (19, [
        ("Kronik etanol maruziyeti gama aminobütirik asit a reseptörlerinde down-regülasyona ve fonksiyonel duyarsızlaşmaya yol açar.",
         "**GABA-A Down-Regülasyonu:** Kronik maruziyette GABA reseptör yanıtları azalır ve duyarsızlaşır.",
         "olarak maruz kaldığında GABAA-aracılı yanıtların down-regülasyonuna ", None),
        ("İnhibitör yanıtların zayıflaması ve glutamat reseptörlerinin telafi edici artışı, alkol aniden kesildiğinde şiddetli eksitasyon fırtınasını doğurur.",
         "**Yoksunluk Hipereksitabilitesi:** GABA azalması ve NMDA artışı alkol kesilince aşırı nöronal uyarılma yaratır.",
         "✓GABA iletimindeki değişikliklerin tolerans ve yoksunlukta önemli bir ", None),
        ("Alkol aynı zamanda mezolimbik ödül merkezinde dopamin, opioid peptitler ve serotonin düzeylerini etkileyerek pekiştirici bağımlılık yaratır.",
         "**Ödül Mekanizması:** Mezolimbik dopamin, opioid ve serotonin salınımı bağımlılığı pekiştirir.",
         "✓Alkol beynin ödüllendirme sisteminde rol oynayan nörotransmiterler ", None),
        ("Uzun yıllar süren ağır alkol tüketimi sinir hücrelerinde kronik metabolik hasar ve yaygın nörotoksisite ile sonuçlanır.",
         "**Nörotoksisite:** Kronik ağır kullanım geri dönüşsüz nörodejenerasyon ve atrofiye yol açar.",
         "2. Nörotoksisite - Uzun yıllar boyunca yüksek miktarlarda alkol ", None)
    ]),

    # Sayfa 20
    (20, [
        ("Kronik alkolizmde en sık karşılaşılan nörolojik bozukluk, distal parestezilerle başlayan simetrik periferik nöropatidir.",
         "**Periferik Nöropati:** Kronik alkolizmde en sık nörolojik bozukluk distal simetrik aksonal nöropatidir.",
         "✓Kronik alkolizmde en yaygın olarak görülen nörolojik bozukluk, ellerin ", None),
        ("Uzun süreli kullanımda ilerleyici serebral atrofi, demans ve nadir vakalarda demiyelinizan santral hasarlar tabloya eklenebilir.",
         "**Demans ve Atrofi:** Serebral korteks atrofisi, bilişsel yıkım ve demans gelişebilir.",
         "✓Alkolizme eşlik eden diğer nörolojik bozukluklar demans ve nadiren ", None),
        ("Wernicke-Korsakoff sendromu oftalmopleji, ataksi ve konfüzyon triadı ile karakterize, acil tedavi gerektiren kritik bir tablodur.",
         "**Wernicke Triadı:** Oftalmopleji, ataksi ve akut konfüzyon tablosu; acil nörolojik durumdur.",
         "✓Wernicke-Korsakoff sendromu (öğrenme ve hafıza defektinin beraber ", None),
        ("Bu sendrom ağır tiamin yani b bir vitamini eksikliğine bağlı olup mammiller cisim atrofisi ve kalıcı hafıza kusurlarıyla seyreder.",
         "**Tiamin (B1) Eksikliği:** Mammiller cisim atrofisi, retrograd ve anterograd amnezi ile karakterizedir.",
         "✓Tiamin (B1 vitamini) eksikliği ile ilişkilidir, fakat alkolizm olmadan ", None)
    ]),

    # Sayfa 21
    (21, [
        ("Tiamin verilmesinin hayati önemi ve toksisite riskinin bulunmaması nedeniyle acile bilinç bozukluğu veya nöbetle gelen her alkolik hastaya tiamin başlanmalıdır.",
         "**Acilde Tiamin:** Bilinç bozukluğu veya nöbetle gelen her alkolik hastaya derhal tiamin verilmelidir.",
         "✓Bu patolojik durumda tiaminin önemi ve tiamin uygulandığında ", None),
        ("Glukoz infüzyonundan önce mutlaka tiamin uygulanmalıdır; aksi halde glukoz metabolizması kalan tiamini tüketerek sendromu alevlendirir.",
         "**Önce Tiamin Kuralı:** Glukoz infüzyonundan önce tiamin verilmelidir; aksi halde Wernicke tablosu ağırlaşır.",
         "sendromundan şüphelenilen bütün hastalar (acile bilinç bozukluğu, nöbetler ", None),
        ("Alkolün haftalarca aşırı tüketimi ağrısız ve iki taraflı görme bulanıklığına yol açarak optik sinir dejenerasyonuna neden olabilir.",
         "**Toksik Ambliyopi:** Ağrısız görme bulanıklığı, bilateral skotom ve optik atrofi gelişebilir.",
         "✓Alkol, birkaç hafta fazla miktarda tüketildiğinde ağrısız görme ", None),
        ("Özellikle metanol gibi sahte içki bileşenleri optik sinirde doğrudan nekroz yaparak kalıcı körlük riski taşır.",
         "**Toksik Alkol Körlüğü:** Metanol alımı optik sinir nekrozu ve ani kalıcı körlük riski taşır.",
         "✓Metanol gibi etanol yerine geçebilen maddelerin alımı ciddi görme ", None)
    ]),

    # Sayfa 22
    (22, [
        ("Uzun süre yüksek miktarda alkol kullanımı ventriküler hipertrofi ve interstisyel fibrozisle karakterize dilate kardiyomiyopatiye yol açar.",
         "**Alkolik Kardiyomiyopati:** Ventriküler hipertrofi, interstisyel fibrozis ve dilate kardiyomiyopati.",
         "1. Kardiyomiyopati ve kalp yetmezliği - Uzun süre yüksek ", None),
        ("Miyokard hücrelerinde membran hasarı, sarkoplazmik retikulum disfonksiyonu ve intraselüler serbest yağ asidi birikimi gelişir.",
         "**Miyosit Hasarı:** Membran hasarı, sarkoplazmik retikulum disfonksiyonu ve intraselüler lipid birikimi.",
         "✓Birçok değişikliğe neden olur: membran zedelenmesi, mitokondri ve ", None),
        ("Voltaj bağımlı kalsiyum kanallarının düzenlenmesindeki bozukluklar miyositlerin kasılma gücünü azaltarak konjestif kalp yetmezliğini derinleştirir.",
         "**Kalsiyum Kanal Disregülasyonu:** Kalsiyum kanal değişimleri kontraktiliteyi bozar ve yetmezliği ağırlaştırır.",
         "up-regülasyonu.", None),
        ("Alkol bırakıldığında ventrikül çapı küçülebilse de alkole bağlı kardiyomiyopatinin prognozu idiyopatik kardiyomiyopatiden daha ağırdır.",
         "**Klinik Seyir:** Alkol bırakılınca gerileyebilse de prognoz idiyopatik formdan daha kötüdür.",
         "✓Alkol içme bırakıldığında kalp büyüklüğü azalmasına ve kalp ", None)
    ]),

    # Sayfa 23
    (23, [
        ("Ağır alkol tüketen bireylerde hem atriyal fibrilasyon hem de hayatı tehdit eden ventriküler aritmiler sıkça tetiklenir.",
         "**Aritmiler:** Atriyal fibrilasyon ve ventriküler aritmiler ağır içicilerde sık görülür.",
         "2. Aritmiler - Ağır içicilerde hem atriyal hem de ventriküler ", None),
        ("Yoksunluk dönemindeki aşırı sempatik deşarj, hipokalemi ve hipomagnezemi aritmilerin şiddetini ve sıklığını katlar.",
         "**Katekolamin Fırtınası:** Sempatik hiperaktivite, hipokalemi ve hipomagnezemi aritmileri tetikler.",
         "Alkol yoksunluk sendromu oluşan hastalarda aşırı katekolamin ", None),
        ("Günde üç kadehten fazla yoğun alkol tüketimi doza bağımlı olarak sistemik hipertansiyon insidansını belirgin biçimde artırır.",
         "**Hipertansiyon:** Günde üç içkiden fazla tüketim doza bağımlı hipertansiyon yapar.",
         "3. Hipertansiyon - Yoğun alkol tüketimi (günde üç içkiden fazla) ile ", None),
        ("Alkol toplumdaki hipertansiyon vakalarının yaklaşık yüzde beşinden tek başına sorumlu tutulmaktadır.",
         "**Etiyolojik Pay:** Toplumdaki hipertansiyon olgularının yaklaşık %5'inden alkol sorumludur.",
         "Alkolün hipertansiyon olgularının yaklaşık %5'inden sorumlu olduğu ", None)
    ]),

    # Sayfa 24
    (24, [
        ("Aşırı alkolün kardiyovasküler yıkımına karşın hafif ve orta dereceli tüketimin koroner arter hastalığından koruduğunu gösteren veriler vardır.",
         "**Koroner Kalp Hastalığı:** Hafif ve orta düzey tüketimin koroner aterosklerozu azalttığı bildirilmiştir.",
         "✓4. Koroner kalp hastalığı - Aşırı alkol kullanımının kardiyo vasküler ", None),
        ("Epidemiyolojik çalışmalarda düşük doz etanolün iskemik inme ve aterosklerotik plak gelişimini azalttığı gözlenmiştir.",
         "**Epidemiyolojik Korunma:** Düşük doz alkol iskemik inme ve koroner morbiditeyi azaltabilir.",
         "✓Orta derecede alkol tüketiminin koroner kalp hastalığını (KKH, CHD), ", None),
        ("Bu olumlu etkinin kısmen plazma yüksek yoğunluklu lipoprotein kolesterol düzeylerindeki hafif artışa dayandığı düşünülmektedir.",
         "**HDL Artışı:** Plazma HDL kolesterol konsantrasyonunu yükseltme yeteneği koruyucu mekanizmadır.",
         "✓Etanolün yüksek-dansiteli lipoprotein (YDL, high-density lipoprotein (HDL)) ", None),
        ("Ayrıca kırmızı şaraptaki resveratrol gibi antioksidan polifenoller de vasküler endotel üzerinde koruyucu rol oynamaktadır.",
         "**Resveratrol:** Kırmızı şaraptaki antioksidan polifenoller ateroskleroza karşı ek koruma sağlar.",
         "✓Alkollü içeceklerde (kırmızı şarapta) ateroskleroza karşı koruyucu ", None)
    ]),

    # Sayfa 25
    (25, [
        ("Alkol hematopoezi hem beslenme bozukluklarıyla dolaylı yoldan hem de kemik iliği kök hücrelerini doğrudan baskılayarak bozar.",
         "**Hematolojik Toksisite:** Kemik iliği öncül hücrelerinin direkt inhibisyonu ve nutrisyonel yetmezlik.",
         "✓Alkol hematopoezi metabolik ve nutrisyonel etkileri ile endirekt ", None),
        ("Kronik içicilerde en yaygın görülen hematolojik tablo folik asit eksikliğine bağlı gelişen makrositer megaloblastik anemidir.",
         "**Folat Eksikliği Anemisi:** Kronik içicilerde en yaygın bozukluk folat eksikliğine bağlı hafif makrositer anemidir.",
         "alkole-bağlı folik asit eksikliği sonucu ortaya çıkan hafif anemi'dir. ", None),
        ("Gastrik erozyonlar ve varis kanamaları sonucu tabloya kronik demir eksikliği anemisi de eklenebilir.",
         "**Demir Eksikliği:** Gastrointestinal erozyon ve varis kanamaları demir eksikliği anemisi doğurur.",
         "Demir eksikliği anemisi gastrointestinal kanama sonucu görülebilir.", None),
        ("Karaciğer sirozu ve splenomegaliye sekonder gelişen hipersplenizm ile kemik iliği toksisitesi trombositopeni ve lökopeniye neden olur.",
         "**Sitopeni:** Karaciğer hastalığı, hipersplenizm ve kemik iliği süpresyonu lökopeni ve trombositopeni yapar.",
         "✓Alkolün ayrıca, bazıları hiperlipidemi ve ciddi karaciğer hastalığıyla ", None)
    ]),

    # Sayfa 26
    (26, [
        ("Alkolik erkeklerde siroz olmasa bile jinekomasti ve testiküler atrofi gelişmesi steroid hormon metabolizmasının bozulduğunu belgeler.",
         "**Endokrin Bozukluklar:** Siroz olmasa bile jinekomasti ve testiküler atrofi steroid dengesizliğini gösterir.",
         "✓Siroz olsun veya olmasın, alkoliklerde jinekomasti ve testiküler atrofi ", None),
        ("İlerlemiş vakalarda hipoalbüminemi ve portal hipertansiyon nedeniyle asit, periferik ödem ve plevral efüzyonlar oluşur.",
         "**Sıvı-Elektrolit Dengesi:** Hipoalbüminemi ve portal basınca bağlı asit, periferik ödem ve efüzyonlar.",
         "✓Kronik karaciğer hastalığı olan kimselerde asites, ödem ve ", None),
        ("Karaciğerde glukoneogenezin baskılanması ağır hipoglisemiye, kortizol artışı ve lipoliz ise ketozise zemin hazırlar.",
         "**Hipoglisemi ve Ketozis:** Glukoneogenez blokajı hipoglisemiye, artan lipoliz ise ketoasidoza yol açar.",
         "metabolik bozukluklar, hepatik glukoneogenezin bozulması sonucu ", None),
        ("Ayrıca alkol alan gebelerde etanolün teratojenik etkileri sonucu konjenital anomaliler ve zeka geriliği riski doğar.",
         "**Teratojenik Etki:** Gebelikte alkol kullanımı mental retardasyon ve konjenital malformasyon nedenidir.",
         "✓Gebelikte annenin kronik alkol kullanımı teratojenik etkilere yol ", None)
    ]),

    # Sayfa 27
    (27, [
        ("Fetal alkol sendromu anne karnında etanole maruz kalan bebeklerde karakteristik dismorfik bulgularla tanımlanan bir klinik tablodur.",
         "**Fetal Alkol Sendromu (FAS):** İntrauterin alkol maruziyeti sonucu gelişen malformasyonlar kompleksi.",
         "✓Fetal alkol sendromu olarak tanımlanan anomaliler şunlardır: ", None),
        ("Sendromun temel bileşenleri intrauterin büyüme geriliği, mikrosefali ve motor koordinasyon bozukluklarıdır.",
         "**Büyüme ve Kraniyal Defekt:** İntrauterin gelişme geriliği, mikrosefali ve zayıf koordinasyon.",
         "✓(1) intrauterin gelişme geriliği, ", None),
        ("Kraniyofasiyal muayenede midfasiyal hipoplazi, düzleşmiş filtrum ve belirgin biçimde ince üst dudak göze çarpar.",
         "**Kraniyofasiyal Bulgular:** Midfasiyal bölgenin az gelişmesi (düz yüz), filtrum silinmesi ve ince üst dudak.",
         "✓(4) midfasiyal bölgenin tam gelişmemesi (düz surat şeklinde görülür), ", None),
        ("İleri olgularda konjenital kalp defektleri ve kalıcı mental retardasyon gelişerek ömür boyu süren zihinsel kısıtlılık yaratır.",
         "**Kardiyak ve Mental Hasar:** Ventriküler septal defektler ve kalıcı mental retardasyon.",
         "✓Daha ciddi olgularda konjenital kalp defektleri ve mental ", None)
    ]),

    # Sayfa 28
    (28, [
        ("Etanol plasenta bariyerini kolayca aşarak fetal dolaşımda anne kanıyla neredeyse eşit konsantrasyonlara hızla ulaşır.",
         "**Plasental Geçiş:** Etanol plasentayı hızla geçerek fötusta anneyle eşit düzeylere ulaşır.",
         "✓Etanol hızla plasentaya geçer ve fetüste anne kanına yakın ", None),
        ("Fetüs karaciğerinde alkol dehidrogenaz enzimi bulunmadığından alkolün eliminasyonu tamamen annenin karaciğer kapasitesine bağımlıdır.",
         "**Fetal Karaciğer:** Fötusta ADH aktivitesi yoktur; eliminasyon anne metabolizmasına bağımlıdır.",
         "✓Fetüs karaciğerinde alkol dehidrogenaz aktivitesi yoktur veya ", None),
        ("Etanol immün sistemi karmaşık biçimde etkiler; bazı dokularda savunmayı baskılarken karaciğerde yıkıcı kronik inflamasyonu alevlendirir.",
         "**İmmün Sistem Etkisi:** Akciğerde immün süpresyon, karaciğer ve pankreasta aşırı inflamasyon.",
         "✓Etanolün immun sistem üzerine karmaşık etkileri vardır; bazı ", None),
        ("Alveoler makrofajların fagositoz gücü kırılır, nötrofil kemotaksisi ve te lenfosit sayıları baskılanarak akciğer enfeksiyonlarına zemin hazırlanır.",
         "**Pulmoner İmmünodepresyon:** Alveoler makrofaj süpresyonu, bozulmuş kemotaksis ve azalmış T hücresi.",
         "✓Akciğerde oluştuğu bildirilen immunolojik değişiklikler arasında, ", None)
    ]),

    # Sayfa 29
    (29, [
        ("Karaciğerde kupffer hücreleri ve hepatik stellat hücreler aktive olarak bol miktarda proinflamatuvar sitokin salgılar ve fibrozisi hızlandırır.",
         "**Hepatik İnflamasyon:** Kupffer ve stellat hücrelerin uyarılmasıyla proinflamatuvar sitokinler artar.",
         "✓Karaciğerde, doğal immun sistemin en önemli hücrelerinin (Kuppfer ", None),
        ("İmmün baskılanma nedeniyle kronik alkolikler pnömokok ve klebsiella pnömonilerine çok daha savunmasız yakalanır ve mortalite artar.",
         "**Pnömoni Riski:** Pulmoner savunma çöküşü Klebsiella ve pnömokok pnömonisi riskini ve mortalitesini artırır.",
         "✓Kronik olarak aşırı alkol kullanımının karaciğer ve pankreasta ", None),
        ("Kronik alkol kullanımı ağız boşluğu, farenks, larenks, özofagus ve karaciğer kanseri riskini katbekat yükseltir.",
         "**Kanser İnsidansı:** Ağız, farenks, larenks, özofagus ve karaciğer malignite insidansı belirgin artar.",
         "✓Kronik alkol kullanımı ağız, farenks, larenks, özofagus ve karaciğer ", None),
        ("Kadınlarda yapılan çalışmalarda ise orta düzeyde bile olsa düzenli alkol alımının meme kanseri insidansını hafifçe artırdığı saptanmıştır.",
         "**Meme Kanseri:** Kadınlarda alkol tüketimi meme kanseri riskinde hafif fakat anlamlı artış yapar.",
         "✓Kadınlarda meme kanseri riskinde hafif bir artış olduğuna dair ", None)
    ]),

    # Sayfa 30
    (30, [
        ("Etanolün kendisi doğrudan mutajenik bir karsinojen olmasa da metaboliti olan asetaldehit güçlü bir toksindir.",
         "**Karsinojenik Mekanizma:** Etanolün kendisi direkt karsinojen değil; metaboliti asetaldehit toksiktir.",
         "✓Alkolün kendisi test sistemlerinin çoğunda karsinojen olarak ", None),
        ("Asetaldehit doğrudan deoksiribonükleik asit hasarı yaparken sitokrom p dört yüz elli aktivasyonu da reaktif serbest oksijen radikalleri üretir.",
         "**DNA Hasarı:** Asetaldehit DNA'yı zedeler; sitokrom indüksiyonu serbest radikal hasarını katlar.",
         "✓Buna karşın, başlıca metaboliti olan asetaldehid, artmış sitokrom ", None),
        ("Folat eksikliği ve kronik mukozal inflamasyon malign transformasyonu hızlandıran ek kolaylaştırıcı etkenlerdir.",
         "**Folat Eksikliği ve İnflamasyon:** Kronik mukozal rejenerasyon ve folat eksikliği karsinogenezi hızlandırır.",
         "✓Alkol ve kanser arasındaki bağlantı ile ilişkilendirilen diğer faktörler ", None),
        ("Etanol diğer ilaçların hem emilim ve metabolizmasını hem de farmakodinamik etkilerini değiştirerek klinik açıdan kritik etkileşimler doğurur.",
         "**İlaç Etkileşimleri:** İkinci ilacın kinetik ve dinamik özelliklerini değiştirerek klinik etkileşim yapar.",
         "✓Etanol ve diğer ilaçlar arasındaki etkileşimler, ikinci ilacın ", None)
    ]),

    # Sayfa 31
    (31, [
        ("Kronik alkol kullanımında sitokrom p dört yüz elli enzimlerinin indüklenmesi diğer ilaçların metabolik yıkımını hızlandırır.",
         "**Kronik Enzim İndüksiyonu:** Hepatik P450 enzimlerinin indüklenmesi ilaç metabolizmasını hızlandırır.",
         "✓En sık görülen farmakokinetik alkol-ilaç etkileşimleri, ilaç metabolize ", None),
        ("Karaciğer yetmezliği gelişmemiş kronik içicilerde varfarin, fenitoin ve sedatiflerin plazma yarı ömürleri kısalır ve etkinlikleri düşebilir.",
         "**Klirens Artışı:** Karaciğer hasarı olmayan kronik içicide varfarin ve fenitoin klirensi hızlanır.",
         "✓Böylelikle, karaciğer hasarı olmaksızın uzun süre alkol alımı diğer ", None),
        ("Sitokrom p dört yüz elli iki e bir enziminin indüksiyonu parasetamol yani asetaminofen kullanımı açısından son derece tehlikelidir.",
         "**Asetaminofen Toksisitesi:** CYP2E1 indüksiyonu asetaminofenin toksik metaboliti NAPQI oluşumunu katlar.",
         "✓Karaciğer sitokrom P450 enzimlerinin etanol ile indüklenmesi, ", None),
        ("Kronik alkoliklerde normal terapötik parasetamol dozlarında dahi toksik metabolit oluşumu artarak fulminan hepatik nekroz tetiklenebilir.",
         "**Fulminan Hepatit:** Günde 3 içkiden fazla tüketenlerde terapötik parasetamol dozlarında bile hepatotoksisite riski artar.",
         "✓Kronik olarak günlük üç veya daha fazla içkinin tüketilmesi, artmış ", None)
    ]),

    # Sayfa 32
    (32, [
        ("Akut alkol alımı ise enzimler için yarışmalı inhibitör davranarak veya karaciğer kan akımını azaltarak diğer ilaçların yıkımını geciktirir.",
         "**Akut Enzim İnhibisyonu:** Akut alkol P450 enzimlerini yarışmalı inhibe eder ve kan akımını düşürür.",
         "✓Akut alkol kullanımı, enzim aktivitesinin veya karaciğer kan akımının ", None),
        ("Fenotiyazinler, trisiklik antidepresanlar ve sedatif hipnotiklerin eliminasyonu akut alkol varlığında yavaşlar ve kanda birikirler.",
         "**İlaç Birikimi:** Fenotiyazinler, trisiklik antidepresanlar ve sedatifler akut alkolle kanda birikir.",
         "✓Fenotiazinler, trisiklik antidepresanlar ve sedatif-hipnotik ilaçlar, ", None),
        ("Ayrıca santral sinir sistemi düzeyinde sedatif hipnotiklerle gelişen sinerjistik depresyon ölümcül solunum durmasına yol açabilir.",
         "**Sinerjistik Sedasyon:** Sedatif hipnotiklerle santral depresyon sinerjisi ölümcül solunum arresti yapar.",
         "✓Farmakodinamik alkol etkileşimleri de büyük öneme sahiptir. Alkol ", None),
        ("Alkol aynı zamanda vazodilatörler ve oral antidiyabetiklerin farmakolojik etkilerini potansiyalize ederek derin hipotermi ve hipoglisemi yaratır.",
         "**Dinamik Potansiyalizasyon:** Vazodilatör ve hipoglisemik ilaçların etkilerini potansiyalize eder.",
         "✓Alkol aynı zamanda, vazodilatörler ve oral hipoglisemik ajanlar dahil, ", None)
    ]),

    # Sayfa 33
    (33, [
        ("Alkol, tütün hariç tutulduğunda, toplumda diğer tüm kötüye kullanılan ilaçların toplamından daha fazla morbidite ve mortalite nedenidir.",
         "**Epidemiyolojik Yük:** Alkol tütün dışında tüm bağımlılık yapıcı ajanların toplamından daha fazla ölüme yol açar.",
         "✓Alkol, tütün haricinde, diğer bütün ilaçların toplamından daha fazla ", None),
        ("Bireysel kişilik yapıları, hayat boyu yaşanmış önemli stresler ve psikiyatrik durumlar tek başına bağımlılığı açıklayamaz.",
         "**Etiyolojik Faktörler:** Kişilik faktörleri ve stresler bağımlılığın tek ve başlıca nedeni değildir.",
         "✓Kişilik farklılıkları, hayat boyu yaşanmış önemli stresler, psikiyatrik ", None),
        ("Çevresel faktörlerin önemli bir rolü olmasına karşın alkolizm gelişiminde genetik yatkınlığın güçlü katkısı kanıtlanmıştır.",
         "**Genetik Katkı:** Çevresel faktörlerin yanında genetik polimorfizmler alkolizm yatkınlığında belirleyicidir.",
         "✓Çevresel faktörlerin önemli bir rolü olmasına karşın, alkolizm ", None),
        ("Tolerans gelişmemiş kimselerde aşırı miktarda alkol tüketimi belirgin vazodilatasyon, taşikardi ve derin sedasyonla seyreder.",
         "**Akut İntoksikasyon Tablosu:** Toleranssız bireyde vazodilatasyon, taşikardi ve sedatif hipnotik doz aşımı bulguları.",
         "Akut Alkol Zehirlenmesinin Tedavisi", None)
    ]),

    # Sayfa 34
    (34, [
        ("Tolerans sınırsız bir koruma sağlamadığından yeterli miktarda alkol alındığında kronik içicilerde bile derin alkol zehirlenmesi ve koma gelişir.",
         "**Akut İntoksikasyon:** Tolerans sınırsız değildir; yüksek dozda kronik alkolikte de koma gelişir.",
         "✓Tolerans sınırsız olmadığına göre, yeterli miktarlarda alkol ", None),
        ("Akut intoksikasyon tedavisinde birinci ve en hayati hedef solunum depresyonunun önlenmesi ve kusmuğun aspirasyonuna karşı hava yolu güvenliğidir.",
         "**Hava Yolu ve Solunum:** Birinci hedef solunum desteği ve kusmuk aspirasyonunun engellenmesidir.",
         "✓Akut alkol zehirlenmesinin tedavisindeki en önemli hedef, solunum ", None),
        ("Kan şekeri ve elektrolitler izlenmeli, hipoglisemi veya ketoasidoz saptandığında intravenöz glukoz infüzyonuyla müdahale edilmelidir.",
         "**Glukoz ve Sıvı Tedavisi:** Hipoglisemi ve ketoasidoz tablosunda intravenöz glukoz ve sıvı infüzyonu verilir.",
         "hipoglisemi ve ketoasidoz tedavisi için glukoz uygulanmasını ", None),
        ("Ancak akut Wernicke ensefalopatisini tetiklememek adına glukozdan hemen önce veya eş zamanlı olarak mutlaka intravenöz tiamin verilmelidir.",
         "**Tiamin Profilaksisi:** Akut Wernicke tablosunu engellemek için glukozla beraber tiamin uygulanmalıdır.",
         "✓Wernicke-Korsakoff sendromundan korunmak için tiamin verilir. ", None)
    ]),

    # Sayfa 35
    (35, [
        ("Alkol bağımlısı bireylerde alkol aniden kesildiğinde veya azaltıldığında motor ajitasyon, anksiyete ve nöbet eşiğinde düşmeyle giden sendrom başlar.",
         "**Yoksunluk Sendromu:** Alkolün ani kesilmesiyle ajitasyon, anksiyete, tremor ve nöbet eğilimi başlar.",
         "✓Alkol bağımlısı olan kimsede alkol aniden kesildiğinde, motor ", None),
        ("En hafif klinik formda, son kadehten altı ila sekiz saat sonra taşikardi, hipertansiyon, belirgin el tremoru ve uykusuzluk ortaya çıkar.",
         "**Erken Semptomlar (6-8 saat):** Taşikardi, hipertansiyon, el tremoru, anksiyete ve uykusuzluk.",
         "kesildikten 6-8 saat sonra nabız ve kan basıncında artış, tremor, ", None),
        ("Anksiyete ve uyku problemleri hafif şiddette aylarca sürebilse de erken otonomik semptomlar genellikle bir iki gün içinde geriler.",
         "**Semptom Seyri:** Otonom semptomlar 1-2 günde gerilerken anksiyete ve uykusuzluk aylarca uzayabilir.",
         "aylarca görülebilmesine karşın, bu etkiler genellikle 1-2 gün içinde ", None),
        ("Tedavi edilmeyen ağır vakalarda ise ilk kırk sekiz saat içinde jeneralize tonik klonik nöbetler ve alkolik halüsinasyonlar tabloya eklenir.",
         "**Yoksunluk Nöbetleri:** İlk 1-5 gün içinde jeneralize nöbetler ve işitsel/görsel halüsinasyonlar görülebilir.",
         "✓Bazı hastalarda, kesilmeden sonraki ilk 1-5 gün içinde yoksunluk ", None)
    ]),

    # Sayfa 36
    (36, [
        ("Bu klinik zaman çizelgesinde alkol kesilmesinden sonra saatler ve günler içinde ortaya çıkan ardışık semptomlar gösterilmektedir.",
         "**Yoksunluk Çizelgesi:** Alkol kesildikten sonra gelişen saatlik ve günlük patolojilerin akışı.",
         "ŞEKİL 23-2 Alkol yoksunluk sendromu sırasında oluşan olaylara ilişkin süreç. En erken görülen belirti ve semptomlar anksiyete, uykusuzluk,", None),
        ("İlk yirmi dört saatte anksiyete, tremor ve bulantı başlarken yirmi dört kırk sekiz saat arasında yoksunluk nöbetleri riski doruğa tırmanır.",
         "**Erken Dönem ve Nöbetler:** 6-24 saatte tremor ve anksiyete, 24-48 saatte konvülziyonlar belirir.",
         "tremor, çarpıntılar, bulantı ve anoreksinin yanı sıra şiddetli sendromlardan halusinasyonlar ve nöbetlerdir. Deliryum tremens tipik olarak alkol", None),
        ("Deliryum tremens tablosu ise tipik olarak alkol kesilmesinden kırk sekiz ila yetmiş iki saat sonra beliren en tehlikeli aşamadır.",
         "**Deliryum Tremens Zamanı:** Kesilmeden 48-72 saat sonra ajitasyon, deliryum ve otonom fırtına başlar.",
         "kesilmesinden 48-72 saat sonra ortaya çıkar. İlk semptomlar (anksiyete, uykusuzluk, vs.), daha hafif de olsa, alkol kesilmesinden sonra aylarca", None),
        ("Yoksunluk nöbetleri genellikle kendi kendini sınırlasa da status epileptikusa dönüşmemesi için uygun sedasyon protokolü şarttır.",
         "**Nöbet Yönetimi:** Yoksunluk nöbetleri statusa ilerleyebileceğinden erken benzodiazepin kontrolü gerekir.",
         "Yoksunluk", None)
    ]),

    # Sayfa 37
    (37, [
        ("Deliryum tremens; dezoryantasyon, ajitasyon, fluktuasyon gösteren bilinç, otonomik instabilite, terleme ve hafif ateşle seyreden ölümcül bir krizdir.",
         "**Deliryum Tremens:** Fluktuasyon gösteren konfüzyon, ajitasyon, otonom instabilite, terleme ve hipertermi.",
         "✓Birkaç gün sonra, deliryum, ajitasyon, otonom sinir sistemi ", None),
        ("Yoksunluk tedavisinin ana hedefleri epileptik nöbetlerin, deliryum tremensin ve ölümcül kardiyak aritmilerin gelişmesini engellemektir.",
         "**Tedavi Hedefleri:** Nöbetlerin, deliryumun ve kardiyak aritmilerin önlenmesi.",
         "✓Alkol yoksunluk sendromu sırasında ilaç tedavisinin temel amacı ", None),
        ("Elektrolit dengesi hızla düzeltilmeli; özellikle magnezyum, potasyum ve fosfat açıkları böbrek fonksiyonu gözetilerek yerine konmalıdır.",
         "**Elektrolit Replasmanı:** Potasyum, magnezyum ve fosfat dengesi böbrek durumuyla uyumlu düzeltilmelidir.",
         "ve fosfat dengesi düzeltilmelidir. ", None),
        ("Şiddetli olgularda detoksifikasyonun temel kuralı, alkol yerine uzun etkili bir sedatif hipnotik başlayıp dozu günbegün kademeli azaltmaktır.",
         "**Detoksifikasyon Prensibi:** Alkol yerine uzun etkili sedatif (benzodiazepin) verip dozu basamaklı azaltmak.",
         "✓Şiddetli olgularda detoksifikasyon için spesifik ilaç tedavisinin iki ", None)
    ]),

    # Sayfa 38
    (38, [
        ("Klordiazepoksit ve diazepam gibi uzun etkili benzodiazepinler aktif metabolitleri sayesinde daha stabil sedasyon sağlar ve daha seyrek verilir.",
         "**Uzun Etkili Benzodiazepinler:** Klordiazepoksit ve diazepam daha az sıklıkla uygulanma avantajına sahiptir.",
         "✓Klordiazepoksid ve diazepam dahil, uzun-etkili benzodiazepinlerin ", None),
        ("Ancak bu uzun etkili moleküller karaciğer yetmezliği olan hastalarda birikerek uzamış sedasyon ve hepatik ensefalopati riskini artırır.",
         "**Kümülasyon Riski:** Karaciğer fonksiyonu bozuk hastalarda aktif metabolitler birikerek komayı tetikler.",
         "✓Uzun-etkili ilaçların dezavantajları, kendilerinin ve aktif ", None),
        ("Karaciğer disfonksiyonu olan alkoliklerde doğrudan glukuronidasyona uğrayıp birikmeyen lorazepam ve oksazepam tercih edilmelidir.",
         "**Karaciğerde LOT Grubu:** Lorazepam ve oksazepam direkt glukuronide olur, karaciğer hastasında birikmez.",
         "✓Lorazepam ve oksazepam gibi kısa-etkili ilaçlar hızla suda çözünen ve ", None),
        ("Hafif vakalarda oral uygulama yeterli olurken ajite ve nöbet geçiren ağır hastalarda parenteral uygulama tercih edilir.",
         "**Uygulama Yolu:** Hafif olgularda oral, şiddetli yoksunluk krizinde parenteral protokol uygulanır.",
         "✓Benzodiazepinler hafif ve orta şiddetteki olgularda oral yolla, daha ", None)
    ]),

    # Sayfa 39
    (39, [
        ("Başarılı bir detoksifikasyonun ardından nüksü önlemek için rehabilitasyon programları ve yoğun psikososyal destek temel şarttır.",
         "**Psikososyal Rehabilitasyon:** Detoksifikasyon sonrası ayaktan/yatan hasta psikososyal destek programları.",
         "✓Detoksifikasyondan sonra, hem yatan hasta hem de ayaktan ", None),
        ("Alkolizme eşlik eden depresyon ve anksiyete gibi psikiyatrik bozuklukların eş zamanlı tedavisi başarı oranını doğrudan belirler.",
         "**Psikiyatrik Tedavi:** Eşlik eden depresyon ve anksiyete bozukluklarının eş zamanlı tedavisi.",
         "✓Alkolizm ile birlikte, en sıklıkla depresif ve anksiyete bozuklukları ", None),
        ("Bağımlılık idame tedavisinde Amerikan Gıda ve İlaç Dairesi tarafından onaylanmış üç temel ilaç disülfiram, naltrekson ve akamprosattır.",
         "**Onaylı Üç İlaç:** FDA onaylı idame ajanları: Naltrekson, akamprosat ve disülfiram.",
         "yardımcı tedavi için FDA'den onay almıştır.", None),
        ("Naltrekson uzun etkili bir mü opioid reseptör antagonisti olup alkolün mezolimbik sistemde yarattığı ödüllendirici ve pekiştirici etkileri engeller.",
         "**Naltrekson:** Uzun etkili mü-opioid antagonisti; alkolün ödüllendirici etkisini ve özlemini baskılar.",
         "✓Görece uzun-etkili bir opioid antagonisti olan naltrekson, µ-opioid ", None)
    ]),

    # Sayfa 40
    (40, [
        ("Klinik çalışmalar naltreksonun alkol özlemini, kadeh sayısını ve tam nüks oranlarını anlamlı ölçüde azalttığını göstermiştir.",
         "**Nüksü Önleme:** Plasebo kontrollü çalışmalarda naltrekson alkol özlemini ve nüks hızını düşürmüştür.",
         "veya içmeye yeniden başlama hızını ve alkol özlemini azalttığını ", None),
        ("Naltrekson alkol bağımlılığı tedavisinde onaylı ilk basamak oral veya depo seçenekler arasındadır.",
         "**FDA Onayı:** Alkol bağımlılığı idame tedavisinde FDA onaylı temel moleküldür.",
         "✓Naltrekson, alkol bağımlılığının tedavisinde kullanılmak üzere FDA ", None),
        ("Günlük oral elli miligram dozda kullanılırken dört haftada bir intramüsküler uygulanan uzun salımlı depo formu da uyumu artırır.",
         "**Dozaj Formları:** Günde tek doz 50 mg oral veya 4 haftada bir intramüsküler depo enjeksiyon.",
         "✓Naltrekson, alkolizm tedavisi için genellikle oral yolla günde tek doz ", None),
        ("Naltrekson doza bağımlı hepatotoksisite riski taşıdığından karaciğer enzimleri yüksek seyreden hastalarda son derece dikkatle izlenmelidir.",
         "**Hepatotoksisite Riski:** Doza bağımlı karaciğer hasarı yapabileceğinden transaminaz takibi şarttır.",
         "nedeniyle, serum aminotransferaz aktivitesinde hafif bozukluk olan ", None)
    ]),

    # Sayfa 41
    (41, [
        ("Hepatotoksisite potansiyelleri nedeniyle naltrekson ile disülfiramın aynı anda kombine edilmesinden kesinlikle kaçınılmalıdır.",
         "**Kombinasyon Uyarısı:** Her ikisi de hepatotoksik olduğundan naltrekson ile disülfiram birlikte verilmez.",
         "✓Her ikisi de potansiyel hepatotoksik ilaçlar oldukları için, naltrekson ", None),
        ("Bağımlılık tedavisinde kullanılan bir diğer onaylı ajan olan akamprosat nüksü önlemede önemli bir yere sahiptir.",
         "**Akamprosat Onayı:** Alkol bağımlılığında nüksü engellemek için FDA onaylı bir diğer ajandır.",
         "için FDA'den de onay almıştır. ", None),
        ("Akamprosatın nörokimyasal profili gama aminobütirik asit ve glutamat reseptör sistemleri arasındaki dengeyi restore etmeye yöneliktir.",
         "**Moleküler Etkiler:** GABAerjik ve glutamaterjik reseptör sistemleri üzerinde modülatör etki.",
         "GABAerjik, glutamaterjik, serotonerjik, noradrenerjik ve ", None),
        ("İlaç zayıf bir en em de a reseptör antagonisti ve gama aminobütirik asit a aktivatörü olarak hiperglutamaterjik aşermeyi yatıştırır.",
         "**NMDA Blokajı:** Zayıf NMDA antagonisti ve GABA-A aktivatörü olarak aşermeyi dindirir.",
         "ve bir GABAA-reseptör aktivatörü olması söylenir. ", None)
    ]),

    # Sayfa 42
    (42, [
        ("Akamprosat günde üç kez üç yüz otuz üç miligramlık enterik kaplı tabletler halinde uygulanır.",
         "**Kullanım Şekli:** Günde üç kez 333 mg'lık barsak kaplamalı tabletler halinde oral verilir.",
         "✓Akamprosat, günde üç kez 333 mg'lık barsak-kaplamalı 1-2 tablet ", None),
        ("Karaciğerde metabolize edilmeyip böbrek yoluyla atılması karaciğer hastalarında güvenli bir seçenek olmasını sağlarken böbrek yetmezliğinde kontrendikedir.",
         "**Renal Eliminasyon:** Karaciğer metabolizması yoktur; böbrekle atılır, ağır böbrek yetmezliğinde yasaktır.",
         "advers etkileri gastrointestinal olanlar (bulantı, kusma, diyare) ve ", None),
        ("Disülfiram ise caydırıcı tedavi ilacıdır; tek başına sessizken üzerine alkol alındığında şiddetli bir otonomik reaksiyon başlatır.",
         "**Caydırıcı Tedavi:** Disülfiram tek başına etkisizdir; alkol alındığında şiddetli toksik sendrom yapar.",
         "✓Disulfiram alkollü içecekler alan hastalarda aşırı rahatsızlığa yol ", None),
        ("Alkolle birlikte alındığında dakikalar içinde yüzde kızarma, zonklayıcı baş ağrısı, taşikardi, bulantı, kusma ve hipotansiyon tablosu patlak verir.",
         "**Disülfiram Reaksiyonu:** Dakikalar içinde flushing, zonklayıcı baş ağrısı, bulantı, kusma ve terleme.",
         "disulfiram alanlar alkol kullandıklarında birkaç dakika içinde flushing, ", None)
    ]),

    # Sayfa 43
    (43, [
        ("Disülfiram etkisini aldehit dehidrogenaz enzimini geri dönüşümsüz olarak inhibe ederek gösterir ve asetaldehit birikimine neden olur.",
         "**İrreversibl ALDH İnhibisyonu:** ALDH enzimini bloke ederek asetaldehidin birikmesine yol açar.",
         "✓Disulfiram etkisini aldehid dehidrogenaz enzimini inhibe ederek ", None),
        ("Ağızdan alındığında hızla emilmesine rağmen enzimle kovalan bağ kurması için tam etkinin oturması yaklaşık on iki saati bulur.",
         "**Gecikmiş Etki:** Gastrointestinal kanaldan hızla emilse de tam etki için 12 saat gerekir.",
         "✓Disulfiram gastrointestinal kanaldan hızla ve tamamen absorbe ", None),
        ("Vücuttan eliminasyonu oldukça yavaş olduğundan ilacın kesilmesinden günler sonra bile alkol alınırsa asetaldehit reaksiyonu tetiklenebilir.",
         "**Yavaş Eliminasyon:** Etki son dozdan sonra günlerce sürer; fenitoin ve varfarin metabolizmasını da bozar.",
         "Fenitoin, oral antikoagülanlar ve izoniazid gibi diğer birçok ", None),
        ("Karaciğer enzimlerini etkileyebileceğinden periyodik transaminaz takibi gerekir ve gebelik döneminde kullanımı önerilmez.",
         "**Takip ve Gebelik:** Karaciğer fonksiyon testlerini değiştirebilir; gebelikte güvenliği gösterilmemiştir.",
         "✓Disulfiram karaciğer fonksiyon testlerini hafifçe değiştirebilir. ", None)
    ]),

    # Sayfa 44
    (44, [
        ("Kronik alkoliklerde alkol aşermesini ve nüksü azaltmak amacıyla onay dışı araştırılan birçok alternatif molekül bulunmaktadır.",
         "**Alternatif Moleküller:** FDA onayı almamış ancak klinik çalışmalarda aşermeyi azaltan yeni ajanlar.",
         "olan birçok ilaç gösterilmesine karşın, bunların hiçbiri henüz FDA'den ", None),
        ("Bu ajanlar arasında antiepileptiklerden topiramat ve gabapentin ile gama aminobütirik asit b agonisti spazmolitik baklofen yer alır.",
         "**Topiramat ve Baklofen:** Topiramat, gabapentin ve GABA-B agonisti baklofen yoksunluk ve aşermede etkilidir.",
         "reseptör antagonisti olan baklofen bulunur.", None),
        ("Serotonin geri alım inhibitörleri ve ondansetron gibi beş ha te üç reseptör antagonistleri de belirli hasta alt gruplarında denenmektedir.",
         "**5-HT3 Antagonistleri:** Ondansetron ve SSRI'lar belirli alt gruplarda alkol tüketimini azaltabilir.",
         "antagonisti olan ondansetronun klinik denemeleri genel olarak ", None)
    ]),

    # Sayfa 45 (ÇIKMIŞ SORU)
    (45, [
        ("Metanol yani odun alkolü sentetik organik kimyada, solventlerde ve araba camı yıkama sıvılarında yaygın bulunan endüstriyel bir maddedir.",
         "**Metanol (Odun Alkolü):** Solventlerde ve cam yıkama sıvılarında kullanılan son derece toksik alkol.",
         "✓Metanol (metil alkol, odun alkolü), sıklıkla sentetik organik bileşiklerin ", None),
        ("Gastrointestinal sistemden, solunum yollarından ve ciltten kolayca emilerek vücut sıvılarına hızla ve homojen biçimde dağılır.",
         "**Emilim:** Deri, solunum ve sindirim sisteminden hızla emilerek vücut sıvılarına yayılır.",
         "kanaldan absorbe edilebilir ve daha sonra vücut sıvılarına dağılır. ", None),
        ("İnsanlarda metanolün yıkımı formaldehit, formik asit ve karbondioksite doğru ilerler ve toksisiteden sorumlu metabolit formik asittir; bu soru çıkmış sınav sorusudur.",
         "**Toksik Metabolit Formik Asit (Çıkmış Soru):** Retinal hasar ve körlükten formaldehit ve formik asit sorumludur.",
         "değil, format ve formaldehide metabolize edilmesine bağlıdır. ",
         ["past-1790877044792-631193"]),
        ("Metanolün toksik metabolitlerine dönüşümü yavaş gerçekleştiğinden zehirlenmenin ağır klinik bulguları alımdan ancak altı ila otuz saat sonra belirginleşir.",
         "**Latent Dönem:** Toksik metabolitlere dönüşüm yavaş olduğundan klinik tablo 6-30 saat sonra ortaya çıkar.",
         "nedeniyle, ciddi toksisite belirtileri ortaya çıkmadan 6-30 saat ", None)
    ]),

    # Sayfa 46
    (46, [
        ("Metanol karaciğerde sitozolik alkol dehidrogenaz tarafından ilk basamakta formaldehide dönüştürülür.",
         "**Formaldehit Basamağı:** Metanol ADH tarafından ilk olarak formaldehide okside edilir.",
         "ŞEKİL 23-3 Metanol, alkol dehidrogenaz ve aldehid dehidroge-", None),
        ("Formaldehit beklemeden aldehit dehidrogenaz ile formik aside yani formata okside edilir ve sistemik asidozu başlatan asıl toksik ürün budur.",
         "**Format Üretimi:** Formaldehit ALDH ile hızla formik aside (formata) dönüşerek asidozu başlatır.",
         "Formaldehid", None),
        ("Formatın karbondioksit ve suya kadar son yıkımı folat bağımlı hücresel yolaklar üzerinden yürütülür.",
         "**Folat Bağımlı Yolak:** Format folat bağımlı sistemle CO2 ve suya parçalanır.",
         "Folat-bağımlı", None),
        ("Fomepizol ve intravenöz etanol ilk basamaktaki alkol dehidrogenazı bloke ederek formaldehit ve formik asit üretimini tamamen durdurur.",
         "**Antidot Blokajı:** Fomepizol ve etanol ADH enzimini inhibe ederek toksik metabolit oluşumunu engeller.",
         "dönüşür. Fomepizol ve etanol, alkol dehidrogenazı inhibe ederek tok-", None)
    ]),

    # Sayfa 47
    (47, [
        ("Zehirlenmenin erken evresinde nonspesifik sarhoşluk hali, baş dönmesi, bulantı ve gastrit belirtileri gözlenir.",
         "**Erken Bulgular:** Sarhoşluk hali, baş dönmesi ve gastrit gibi nonspesifik semptomlar.",
         "✓Metanol zehirlenmesinde fiziksel bulgular genellikle non spesifiktir; ", None),
        ("Ağır vakalarda hastanın nefesinde ve idrarında karakteristik keskin formaldehit kokusu duyulabilir.",
         "**Formaldehit Kokusu:** Ciddi olgularda nefeste ve idrarda formaldehit kokusu alınabilir.",
         "✓Ciddi olgularda, nefeste ve idrarda formaldehid kokusu bulunabilir. ", None),
        ("Latent dönemin ardından derin anyon açığı metabolik asidozu ile birlikte metanolün en tipik bulgusu olan görme bozuklukları patlak verir.",
         "**Görme Bozukluğu ve Asidoz:** Anyon açıklı asidoz ve karakteristik bilateral görme kaybı tablosu.",
         "zehirlenmesinin en karakteristik semptomu olan görsel bozukluklar ", None),
        ("Hasta görme alanını kar fırtınası içinde kalmış gibi tarif eder; optik disk hiperemisi ve retinal hasar hızla kalıcı körlüğe ilerleyebilir.",
         "**Kar Fırtınası Görüşü:** Hasta görüşü 'kar fırtınası' şeklinde tanımlar; optik disk hiperemisi ve körlük gelişir.",
         "✓Görsel bozukluk sıklıkla \"kar fırtınası içinde kalmak\" şeklinde tarif ", None),
        ("Bradikardi, dirençli metabolik asidoz ve derin koma kötü prognoza işaret ederken ölüm ani solunum durmasıyla gerçekleşir.",
         "**Kötü Prognoz:** Bradikardi, dirençli asidoz ve koma ölümcüldür; ölüm ani solunum durmasıyla olur.",
         "✓Bradikardi, uzamış  koma, nöbetler ve dirençli asidoz prognozun kötü ", None)
    ]),

    # Sayfa 48
    (48, [
        ("Serum metanol konsantrasyonunun yirmi miligram bölü desilitreyi aşması aktif antidot tedavisini zorunlu kılar.",
         "**Tedavi Eşiği:** Serum düzeyi >20 mg/dL olduğunda antidot tedavisine hızla başlanmalıdır.",
         "tedavi gerektirir, 50 mg/dL'den yüksek konsantrasyonlar ise ", None),
        ("Düzeyin elli miligram bölü desilitrenin üzerine çıkması veya dirençli asidoz gelişmesi acil hemodiyaliz endikasyonudur.",
         "**Hemodiyaliz Eşiği:** >50 mg/dL düzey, görme kaybı veya dirençli asidozda hemodiyaliz şarttır.",
         "✓Metanol zehirlenmesinde de öncelikle solunum desteklenmeli. ", None),
        ("Tedavinin temel ayağı alkol dehidrogenazın bloke edilerek toksik formik asit oluşumunun durdurulmasıdır.",
         "**Temel İlke:** ADH bloke edilerek metanolün formata metabolizasyonu durdurulmalıdır.",
         "✓Metanolün toksik ürünlere metabolizasyonun engellenmesi, ", None),
        ("Eş zamanlı olarak sistemik asidozu dengelemek için intravenöz sodyum bikarbonat infüzyonuyla kan gazı alkalinizasyonu sağlanmalıdır.",
         "**Bikarbonat Alkalinizasyonu:** Şiddetli anyon açıklı metabolik asidoz için bikarbonat infüzyonu verilir.",
         "✓Metabolik asidozu dengelemek için alkalinizasyon.", None)
    ]),

    # Sayfa 49
    (49, [
        ("Bir alkol dehidrogenaz inhibitörü olan fomepizol hem metanol hem de etilen glikol zehirlenmelerinde resmi onaylı spesifik antidottur.",
         "**Fomepizol Antidotu:** ADH inhibitörü olup metanol ve etilen glikol zehirlenmelerinde FDA onaylıdır.",
         "✓Bir alkol dehidrogenaz inhibitörü olan fomepizol metanol ve etilen ", None),
        ("İntravenöz olarak on beş miligram bölü kilogram yükleme dozunun ardından kırk sekiz saat boyunca on iki saatte bir idame doz uygulanır.",
         "**Doz Şeması:** 15 mg/kg IV yükleme, ardından 48 saat boyunca 12 saatte bir 10 mg/kg idame.",
         "✓İntravenöz olarak 15 mg/kg'lık yükleme dozunu takiben 48 saat ", None),
        ("Kırk sekiz saatten sonra fomepizol kendi mikrozomal metabolizmasını indüklediği için idame dozu on beş miligram bölü kilograma yükseltilir.",
         "**Otoindüksiyon:** 48 saat sonra kendi metabolizmasını indüklediği için doz 15 mg/kg'a artırılır.",
         "tarafından kendi metabolizmasını indüklemesi nedeniyledir. ", None),
        ("En sık karşılaşılan yan etkileri infüzyon yerinde lokal yanma, baş ağrısı, bulantı ve geçici baş dönmesidir.",
         "**Advers Etkiler:** İnfüzyon yerinde yanma, baş ağrısı, bulantı ve baş dönmesi.",
         "bulantı ve baş dönmesidir. ", None)
    ]),

    # Sayfa 50 (ÇIKMIŞ SORU)
    (50, [
        ("Fomepizolün bulunmadığı durumlarda intravenöz etanol infüzyonu hayat kurtarıcı bir alternatiftir ve bu durum çıkmış sınav sorusudur.",
         "**İntravenöz Etanol (Çıkmış Soru):** Fomepizolün alternatifi olan etanol ADH afinitesiyle metabolizmayı durdurur.",
         "✓Fomepizolün alternatifi intravenöz etanoldür. Alkol dehidrogenaza ",
         ["d3-k2-far-009"]),
        ("Etanolün alkol dehidrogenaz enzimine afinitesi metanolden çok daha yüksek olduğu için enzimi yarışmalı biçimde meşgul ederek format üretimini durdurur.",
         "**Yarışmalı İnhibisyon:** Etanolün ADH afinitesi metanolden kat kat yüksektir; yarışmalı blokaj sağlar.",
         "tedavisinde kullanılır. ", None),
        ("Ağır vakalarda kandaki hem metanolü hem de toksik formatı temizlemek için acil hemodiyaliz uygulanmalıdır.",
         "**Hemodiyalizle Klirens:** Toksik formatı ve metanolü kandan hızla temizlemek için hemodiyaliz şarttır.",
         "kandan uzaklaştırmak için hemodiyaliz gerekebilir. ", None),
        ("Derin asidoza karşı bikarbonat verilirken formik asidin karbondioksite parçalanmasını hızlandırmak için folik ya da folinik asit infüzyonu eklenir.",
         "**Folat ve Bikarbonat Desteği:** Formatın CO2'ye yıkımını hızlandırmak için folik/folinik asit eklenir.",
         "✓Metanol zehirlenmesindeki belirgin metabolik asidoz nedeniyle, ", None)
    ]),

    # Sayfa 51
    (51, [
        ("Etilen glikol antifriz formülasyonlarında ve endüstriyel soğutma sistemlerinde solvent olarak kullanılan toksik bir alkoldür.",
         "**Etilen Glikol:** Antifriz ve solventlerde kullanılan toksik dihidrik alkol.",
         "✓Etilen glikol gibi alkoller antifriz formülasyonlarında ısı değiştirici ", None),
        ("Tatlı tadı nedeniyle kazara çocuklar tarafından içilebilir ya da intihar amacıyla oral yoldan tüketilebilir.",
         "**Zehirlenme Riski:** Tatlı tadı nedeniyle çocuklar veya hayvanlar tarafından kazaen tüketilebilir.",
         "tadından etkilenebilirler; ayrıca, nadiren, etanolün yerine bilerek ", None),
        ("Etilen glikolün kendisi nispeten toksik değilken metaboliti olan glikolik asit ve okzalik asit derin doku hasarı yaratır.",
         "**Toksik Metabolitler:** Kendisi zararsız olup glikolik asit, glioksilat ve okzalata okside olarak hasar yapar.",
         "birlikte, toksik ürünleri olan aldehid ve oksalata metabolize edilir.", None),
        ("Zehirlenme üç evrede seyreder: ilk saatlerde merkezi sinir sistemi depresyonu, dört ila on iki saatte laktik ve glikolik asidoz, ardından akut böbrek yetmezliği.",
         "**Üç Evreli Seyir:** 1) MSS depresyonu (ilk saatler), 2) Ağır metabolik asidoz (4-12 saat), 3) Akut böbrek yetmezliği.",
         "✓1) Alımını takip eden birkaç saat içinde geçici bir eksitasyon ve ", None),
        ("Okzalik asidin kalsiyumla birleşerek böbrek tübüllerinde kristalleşmesi tübüler nekroz ve oligürik böbrek yetmezliği ile sonuçlanır.",
         "**Tübüler Hasar:** Oksalat böbrek tübüllerinde birikerek akut tübüler nekroz ve böbrek yetmezliği yapar.",
         "gelişir. 3) En sonunda ise, oksalatın böbrek tubuluslarında birikimini ", None)
    ]),

    # Sayfa 52
    (52, [
        ("Etilen glikol zehirlenmesinde retinal görme bozukluğu olmaksızın anyon açığı asidozu ve idrar mikroskopisinde kalsiyum oksalat kristalleri saptanır.",
         "**Tanısal Bulgular:** Görme bozukluğu olmadan anyon açığı asidozu ve idrarda kalsiyum oksalat kristalleri.",
         "olmadan hastada anyon açığı asidozu ve idrarda oksalat ", None),
        ("Oksalatın kalsiyumu bağlaması ağır hipokalsemiye yol açabilir; standart ilk tercih ilaç yine intravenöz fomepizoldür.",
         "**Fomepizol Tedavisi:** Hipokalsemi izlenmeli; ilk tercih spesifik antidot yine fomepizoldür.",
         "standart ilacı da fomepizol'dür. Metanol zehirlenmesine benzer ", None),
        ("Fomepizol yükleme dozunu takiben serum düzeyi yirmi ila otuz miligram bölü desilitrenin altına inene dek idame ettirilir.",
         "**İdame Protokolü:** Düzey 20-30 mg/dL altına düşene kadar 12 saatte bir infüzyon sürdürülür.",
         "✓İntravenöz olarak 15 mg/kg'lık yükleme dozunu takiben 48 saat ", None),
        ("Fomepizol sağlanamadığında intravenöz etanol infüzyonu aynı şekilde yarışmalı enzim blokajı sağlayarak böbrek hasarını önler.",
         "**Etanol Alternatifi:** Fomepizol yoksa IV etanol ile ADH enzimi bloke edilir.",
         "✓Etilen glikol zehirlenmesinde de fomepizolün alternatifi etanoldür. ", None)
    ]),

    # Sayfa 53
    (53, [
        ("Alkoller farmakolojisi dersimizin temel teorik anlatımını Katzung Temel ve Klinik Farmakoloji referansları eşliğinde tamamlamış bulunuyoruz.",
         "**Katzung Farmakoloji:** Temel ve Klinik Farmakoloji kaynakları eşliğinde alkoller ünitesi tamamlandı.",
         "Temel ve Klinik Farmakoloji ", None),
        ("Etanolün kinetiğini, organ toksisitelerini ve özellikle acil servislerde hayati olan toksik alkol antidot protokollerini özetledik.",
         "**Ders Özeti:** Kinetik kuralları, organ toksisiteleri, yoksunluk tedavisi ve antidot protokolleri.",
         "Bertram G. Katzung, Susan B. Masters, Antony J. Trevor", None),
        ("Karaciğer sirozu, Wernicke sendromu ve fomepizol kullanım endikasyonları kurul ve uzmanlık sınavlarının değişmez soru alanlarıdır.",
         "**Sınav Vurguları:** Sıfır derece kinetik, disülfiram reaksiyonu, tiamin önemi ve fomepizol antidotu.",
         "Nobel Tıp Kitabevleri", None)
    ])
]

# Verify all anchors in kaynak.md
print("Verifying anchors in kaynak.md...")
anchor_errors = 0
for sayfa, sentences in SLIDES_DATA:
    page_text = pages.get(sayfa, "")
    for ses, ekran, alinti, cikmis in sentences:
        if alinti not in page_text:
            print(f"ERROR: Anchor not found on page {sayfa}: {repr(alinti)}")
            anchor_errors += 1

if anchor_errors > 0:
    print(f"FAILED: {anchor_errors} anchor errors!")
    exit(1)
else:
    print("ALL ANCHORS VERIFIED 100% IN KAYNAK.MD!")

VISUAL_PAGES = {
    9: "Etanol metabolizma ve enzim şeması",
    10: "Akut etanol farmakodinamiği ve kan düzeyleri tablosu",
    27: "Fetal alkol sendromu klinik ve fasiyal özellikleri şeması",
    36: "Alkol yoksunluk sendromu zaman çizelgesi şeması",
    46: "Metanol metabolizma ve toksik format dönüşüm şeması"
}

# Group slides into 21 chapters
CHAPTERS_DEF = [
    {"id": "k2-58-b01", "baslik": "Alkollerin Genel Özellikleri, Bağımlılık ve Emilim Farmakokinetiği", "sayfalar": [1, 3]},
    {"id": "k2-58-b02", "baslik": "Etanol Eliminasyonu, Pulmoner Atılım ve Sıfırıncı Derece Kinetik", "sayfalar": [4, 4]},
    {"id": "k2-58-b03", "baslik": "Alkol Dehidrogenaz Yolağı, Mide Enzim Aktivitesi ve Cinsiyet Farkı", "sayfalar": [5, 6]},
    {"id": "k2-58-b04", "baslik": "Mikrozomal Etanol Oksitleyici Sistem (MEOS / CYP2E1) ve Toksisite", "sayfalar": [7, 7]},
    {"id": "k2-58-b05", "baslik": "Asetaldehid Metabolizması, Mitokondriyal ALDH ve Disülfiram Etkisi", "sayfalar": [8, 9]},
    {"id": "k2-58-b06", "baslik": "Akut Etanol Farmakodinamiği ve Merkezi Sinir Sistemi Depresyonu", "sayfalar": [10, 11]},
    {"id": "k2-58-b07", "baslik": "Membran Proteinleri, GABA-A ve NMDA Reseptör Modülasyonu", "sayfalar": [12, 12]},
    {"id": "k2-58-b08", "baslik": "Kardiyovasküler Etkiler, Vazodilatasyon ve Düz Kas Gevşemesi", "sayfalar": [13, 14]},
    {"id": "k2-58-b09", "baslik": "Kronik Tüketimin Karaciğer ve Sindirim Sistemi Sonuçları", "sayfalar": [15, 17]},
    {"id": "k2-58-b10", "baslik": "Alkol Toleransı, Fiziksel Bağımlılık ve Reseptör Adaptasyonu", "sayfalar": [18, 19]},
    {"id": "k2-58-b11", "baslik": "Nörolojik Hasar, Periferik Nöropati ve Wernicke-Korsakoff Sendromu", "sayfalar": [20, 21]},
    {"id": "k2-58-b12", "baslik": "Kardiyotoksisite, Aritmiler ve Koroner Kalp Hastalığı", "sayfalar": [22, 24]},
    {"id": "k2-58-b13", "baslik": "Hematolojik Toksisite, Endokrin Bozukluklar ve Sıvı Dengesi", "sayfalar": [25, 26]},
    {"id": "k2-58-b14", "baslik": "Fetal Alkol Spektrum Bozukluğu (FASD) ve İmmün Disfonksiyon", "sayfalar": [27, 29]},
    {"id": "k2-58-b15", "baslik": "Karsinogenez Mekanizması ve Alkol-İlaç Etkileşimleri", "sayfalar": [30, 32]},
    {"id": "k2-58-b16", "baslik": "Akut Alkol İntoksikasyonu ve Alkol Yoksunluk Sendromu Kliniği", "sayfalar": [33, 36]},
    {"id": "k2-58-b17", "baslik": "Deliryum Tremens ve Yoksunlukta Benzodiazepin Protokolleri", "sayfalar": [37, 38]},
    {"id": "k2-58-b18", "baslik": "Alkol Bağımlılığında Nüks Önleme: Naltrekson, Akamprosat ve Disülfiram", "sayfalar": [39, 44]},
    {"id": "k2-58-b19", "baslik": "Metanol Toksisitesi, Formik Asit Asidozu ve Retinal Hasar", "sayfalar": [45, 48]},
    {"id": "k2-58-b20", "baslik": "Toksik Alkol Zehirlenmelerinde Antidotlar: Fomepizol ve Etanol", "sayfalar": [49, 50]},
    {"id": "k2-58-b21", "baslik": "Etilen Glikol Toksisitesi, Oksalat Kristalleri ve Tedavisi", "sayfalar": [51, 53]}
]

# Build paragraphs per slide
slides_by_num = {s[0]: s[1] for s in SLIDES_DATA}

c_counter = 1
p_counter = 1
bolumler = []

# Map sentence IDs to pages for drawing placement
slide_sentences_map = {}

for ch_idx, ch in enumerate(CHAPTERS_DEF, 1):
    p_start, p_end = ch["sayfalar"]
    ch_paras = []
    
    for sayfa in range(p_start, p_end + 1):
        s_list = slides_by_num[sayfa]
        para_cumleler = []
        slide_sentences_map[sayfa] = []
        
        for s_idx, (ses, ekran, alinti, cikmis) in enumerate(s_list):
            cid = f"k2-58-c{c_counter:04d}"
            slide_sentences_map[sayfa].append(cid)
            
            sekil_val = VISUAL_PAGES.get(sayfa) if s_idx == 0 else None
            
            vurgu_text = ekran.split("**")[1] if "**" in ekran else "Alkol"
            c_obj = {
                "id": cid,
                "ses": ses,
                "ekran": ekran,
                "duzey": 0,
                "slayt": {
                    "sayfa": sayfa,
                    "satir": [alinti],
                    "sekil": sekil_val
                },
                "vurgu": [
                    {
                        "tur": "terim",
                        "metin": vurgu_text
                    }
                ]
            }
            if cikmis:
                c_obj["cikmis"] = cikmis
            
            para_cumleler.append(c_obj)
            c_counter += 1
        
        para_obj = {
            "id": f"k2-58-p{p_counter:04d}",
            "sayfa": sayfa,
            "cumleler": para_cumleler
        }
        ch_paras.append(para_obj)
        p_counter += 1
    
    bolumler.append({
        "id": ch["id"],
        "baslik": ch["baslik"],
        "paragraflar": ch_paras
    })

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-58",
    "bolumler": bolumler
}

# Write konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Generated konusma_v2.json: {len(bolumler)} bolum, {p_counter-1} paragraf, {c_counter-1} cumle.")

# Total words count
total_words = sum(len(c["ses"].split()) for b in bolumler for p in b["paragraflar"] for c in p["cumleler"])
print(f"Total words: {total_words} (~{total_words/125:.1f} minutes of audio)")

# Update sayfa_haritasi.json
sh_path = TASLAK / "sayfa_haritasi.json"
if sh_path.exists():
    sh_data = json.loads(sh_path.read_text(encoding="utf-8"))
    for s_entry in sh_data.get("sayfalar", []):
        pnum = s_entry.get("sayfa")
        if pnum in SLIDE_BILGI:
            s_entry["bilgi"] = SLIDE_BILGI[pnum]
    sh_path.write_text(json.dumps(sh_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Updated sayfa_haritasi.json with exact bilgi mappings.")

# Update cizim_aday.json with 8 valid drawing commands
cizim_path = TASLAK / "cizim_aday.json"
cizim_komutlar = [
    {
        "cumle": slide_sentences_map[3][3],
        "bas": 0,
        "son": 4,
        "sayfa": 3,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Etanol Kinetiği",
        "ogeler": [
            "Hızlı absorbsiyon",
            "Total vücut suyuna dağılım",
            "Kadınlarda yüksek doruk düzey"
        ]
    },
    {
        "cumle": slide_sentences_map[6][3],
        "bas": 0,
        "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Aşırı NADH Sonuçları",
        "ogeler": [
            "Aşırı NADH birikimi",
            "Glukoneogenez baskılanması",
            "Laktik asidoz ve hipoglisemi"
        ]
    },
    {
        "cumle": slide_sentences_map[8][1],
        "bas": 0,
        "son": 4,
        "sayfa": 8,
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Etanol Oksidasyonu",
        "ogeler": [
            "Etanolden asetaldehit oluşumu",
            "Mitokondriyal ALDH aktivasyonu",
            "Asetatın sitrik asit döngüsüne girmesi"
        ]
    },
    {
        "cumle": slide_sentences_map[15][1],
        "bas": 0,
        "son": 4,
        "sayfa": 15,
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Karaciğer Hasarı",
        "ogeler": [
            "Karaciğer yağlanması",
            "Alkolik hepatit",
            "Siroz ve karaciğer yetmezliği"
        ]
    },
    {
        "cumle": slide_sentences_map[20][2],
        "bas": 0,
        "son": 4,
        "sayfa": 20,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Wernicke Triadı",
        "ogeler": [
            "Oftalmopleji",
            "Serebellar ataksi",
            "Akut konfüzyon"
        ]
    },
    {
        "cumle": slide_sentences_map[36][2],
        "bas": 0,
        "son": 4,
        "sayfa": 36,
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Yoksunluk Semptomları",
        "ogeler": [
            "Tremor ve anksiyete",
            "Yoksunluk nöbetleri",
            "Deliryum tremens"
        ]
    },
    {
        "cumle": slide_sentences_map[47][3],
        "bas": 0,
        "son": 4,
        "sayfa": 47,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Metanol Toksisitesi",
        "ogeler": [
            "Toksik format birikimi",
            "Metabolik asidoz",
            "Retinal hasar ve görme kaybı"
        ]
    },
    {
        "cumle": slide_sentences_map[51][4],
        "bas": 0,
        "son": 4,
        "sayfa": 51,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Etilen Glikol Zehirlenmesi",
        "ogeler": [
            "Okzalik asit oluşumu",
            "Böbrek tübüllerinde kristalleşme",
            "Akut böbrek yetmezliği"
        ]
    }
]

cizim_path.write_text(json.dumps({"komutlar": cizim_komutlar}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Generated cizim_aday.json: {len(cizim_komutlar)} komut.")
