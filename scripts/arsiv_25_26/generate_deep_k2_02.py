import sys, json, re, subprocess
from pathlib import Path

REPO_ROOT = Path('/home/indu/medsor')
TASLAK = REPO_ROOT / 'meds_database_25_26/taslak/y25-k2-02-bilinc-bozuklugu-olan-hastaya-yaklasim'

sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/sesli_anlatim'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/ders_isci'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/cizim'))

import konusma_v2 as KV
import denetle as D
import isle as IS
import cizim_dogrula as CD
import sablon

with open(TASLAK / 'kaynak.md') as f:
    text = f.read()

page_dict = {}
for p in text.split('=== SAYFA ')[1:]:
    lines = p.split('\n')
    pnum = int(lines[0].split(' ')[0])
    page_dict[pnum] = '\n'.join(lines[1:])

PARAGRAPHS = [
    # BOLUM 1: Bilinç değişikliğinin önemi
    (2, "k2-02-b01", "Bilinç Değişikliğinin Önemi ve Acil Konsültasyonlar", "k2-02-p001", [
        (
            "Bilinç değişiklikleri ve koma tablosu acil servislerde ve yoğun bakım ünitelerinde nöroloji hekimlerine yapılan konsültasyonların en sık nedenidir.",
            "**En Sık Konsültasyon:** Acil servis ve yoğun bakımlarda nöroloji konsültasyonlarının birincil nedeni bilinç değişikliğidir.",
            "Bilinç değişiklikleri acil servis ve yoğun",
            ["bilinç değişikliği", "acil servis", "nöroloji konsültasyonu"],
            []
        ),
        (
            "Uyanıklık kusuru veya bilinç kaybı ile getirilen bir hastada hekimin zamanla yarışarak ivedi müdahale etmesi hayati bir zorunluluktur.",
            "**Zamanla Yarış:** Hipoksi ve iskemiye karşı beyin dokusunu korumak için ivedi klinik müdahale.",
            "bakım ünitelerinde en sık nöroloji",
            ["zamanla yarış", "beyin dokusu", "iskemi"],
            []
        ),
        (
            "Hastanın ilk değerlendirmesinde nörolojik yaklaşımın temel hedefi lezyonun anatomik lokalizasyonunu ve etiyolojik mekanizmasını aydınlatmaktır.",
            "**Temel Hedef:** Lezyonun anatomik koordinatını ve altta yatan etiyolojik mekanizmayı belirleme.",
            "konsültasyonu nedenidir.",
            ["anatomik lokalizasyon", "etiyolojik mekanizma"],
            []
        ),
        (
            "Bilinç değişikliği kavramı uyanıklık ve farkındalık süreçlerinin akut subakut ya da dalgalı biçimde bozulmasını kapsar.",
            "**Kavram Tanımı:** Uyanıklık ve farkındalık süreçlerindeki akut veya subakut bozulmalar spektrumu.",
            "Bilinç değişiklikleri acil servis ve yoğun",
            ["uyanıklık", "farkındalık", "akut bozulma"],
            []
        ),
        (
            "Acile başvuran komalı bir hastada klinisyen tablonun primer beyin hasarından mı yoksa sistemik metabolik bir iflastan mı kaynaklandığını hızla ayırmalıdır.",
            "**Temel Karşılaştırma:** Primer yapısal beyin hasarı ile beyni ikincil etkileyen sistemik metabolik tablo karşılaştırılır.",
            "bakım ünitelerinde en sık nöroloji",
            ["primer beyin hasarı", "sistemik metabolik iflas"],
            []
        ),
        (
            "Hızlı ve doğru bir ayrım hastaya gereksiz cerrahi veya radyolojik işlemler yapılmasını önlerken hayat kurtarıcı tedavileri başlatır.",
            "**Tedavi Önceliği:** Doğru klinik ayrım ile gereksiz girişimleri engelleme ve hayat kurtarıcı tedavi.",
            "konsültasyonu nedenidir.",
            ["gereksiz girişimler", "hayat kurtarıcı tedavi"],
            []
        ),
        (
            "Bu nedenle hekimin bilinç bozukluğu olan hastaya sistematik soğukkanlı ve algoritma temelli bir yaklaşımla müdahale etmesi beklenir.",
            "**Algoritmik Yaklaşım:** Soğukkanlı ve adım adım yapılandırılmış algoritma temelli klinik yöntem.",
            "Bilinç değişiklikleri acil servis ve yoğun",
            ["algoritma temelli", "soğukkanlı yaklaşım"],
            []
        ),
        (
            "Doktor Dursun Ceylan tarafından hazırlanan bu derste bilinç bozukluklarının nöroanatomik temeli tanısal basamakları ve acil yönetimi incelenecektir.",
            "**Ders Kapsamı:** Dr. Dursun Ceylan rehberliğinde bilinç bozuklukları mekanizmaları ve tedavi yönetimi.",
            "konsültasyonu nedenidir.",
            ["Dursun Ceylan", "tanısal basamaklar", "acil yönetim"],
            []
        )
    ]),

    (2, "k2-02-b01", "Bilinç Değişikliğinin Önemi ve Acil Konsültasyonlar", "k2-02-p002", [
        (
            "Bilinç değişikliği ile acil servise başvuran hastaların etiyolojik dağılımı incelendiğinde vakaların yüzde seksen beşinin metabolik ve sistemik nedenlere bağlı olduğu görülür.",
            "**Etiyolojik Dağılım:** Vakaların yüzde seksen beşi metabolik ve sistemik nedenlerden kaynaklanır.",
            "% 85 metabolik ve sistemik neden",
            ["yüzde seksen beş", "metabolik neden", "sistemik neden"],
            []
        ),
        (
            "Buna karşılık primer olarak santral sinir sistemine ait yapısal patolojiler olguların yalnızca yüzde on beşini oluşturmaktadır.",
            "**Santral Neden Payı:** Primer santral sinir sistemi patolojileri olguların yalnızca yüzde on beşidir.",
            "% 15 SSS ait neden",
            ["santral sinir sistemi", "yüzde on beş"],
            []
        ),
        (
            "Bu epidemiyolojik gerçeklik acil hekiminin diagnostik stratejisini ve reflekslerini belirleyen en temel klinik kılavuzdur.",
            "**Diagnostik Strateji:** Acil hekiminin tanısal yaklaşımını belirleyen en temel epidemiyolojik oran.",
            "% 85 metabolik ve sistemik neden",
            ["epidemiyolojik gerçeklik", "diagnostik strateji"],
            []
        ),
        (
            "Çünkü bilinci kapalı bir hasta görüldüğünde akla ilk olarak masif bir kafa travması gelse de altta yatan neden ezici çoğunlukla sistemik bir metabolizma bozukluğudur.",
            "**Metabolik Ağırlık:** Koma tablosunda primer travmadan ziyade altta yatan metabolik bozulmanın baskınlığı.",
            "% 85 metabolik ve sistemik neden",
            ["metabolizma bozukluğu", "koma tablosu"],
            []
        ),
        (
            "Ağır hipoglisemi septik şok elektrolit dengesizliği üremi ya da akut karaciğer yetmezliği serebral hemisferleri yaygın baskılayarak derin koma yaratabilir.",
            "**Yaygın Baskılanma:** Hipoglisemi, üremi ve septik şokun serebral korteksi bilateral baskılaması.",
            "% 85 metabolik ve sistemik neden",
            ["hipoglisemi", "üremi", "septik şok"],
            []
        ),
        (
            "Bu nedenle hastayı kabul eder etmez hemen bilgisayarlı tomografiye göndermek yerine önce yatak başı vital stabilizasyon sağlanmalıdır.",
            "**Önce Stabilizasyon:** Radyolojiye gitmeden önce yatak başı yaşamsal fonksiyonları güvenceye alma.",
            "% 15 SSS ait neden",
            ["bilgisayarlı tomografi", "vital stabilizasyon"],
            []
        ),
        (
            "Yüzde seksen beşlik metabolik nedenlerin büyük kısmı erken müdahale ve doğru replasman tedavileri ile tamamen geri döndürülebilir niteliktedir.",
            "**Geri Döndürülebilirlik:** Erken müdahale ile metabolik nedenlerin tamamen tedavi edilebilirliği.",
            "% 85 metabolik ve sistemik neden",
            ["metabolik nedenler", "geri döndürülebilir"],
            []
        ),
        (
            "Buna karşın tanıda gecikilen ya da atlanan bir metabolik bozukluk beynin dakikalar içinde geri dönüşsüz hipoksik iskemik hasara uğramasına yol açacaktır.",
            "**Geri Dönüşsüz Hasar:** Atlanan metabolik tablonun nöronlarda kalıcı iskemik hasar oluşturma riski.",
            "% 15 SSS ait neden",
            ["gecikilen tanı", "hipoksik hasar"],
            []
        )
    ]),

    # BOLUM 2: Bilincin anatomik temeli
    (4, "k2-02-b02", "Bilincin Anatomik Temeli ve ARAS Ağı", "k2-02-p003", [
        (
            "Bilincin nöroanatomik ve fizyolojik mekanizmalarını anlayabilmek için uyanıklığı sağlayan subkortikal ağları kavramak şarttır.",
            "**Nöroanatomik Temel:** Uyanıklığı sağlayan subkortikal ağların ve beyin sapı formasyonunun yapısı.",
            "Asendan retiküler aktive edici sistem",
            ["nöroanatomik temel", "subkortikal ağ"],
            []
        ),
        (
            "Uyanıklık durumunu ve uyarılabilirliği başlatan ve kesintisiz sürdüren en temel nöral ağ asendan retiküler aktive edici sistemdir.",
            "**ARAS Ağı:** Uyanıklık ve uyarılabilirliği sağlayan asendan retiküler aktive edici sistem.",
            "Asendan retiküler aktive edici sistem",
            ["asendan retiküler aktive edici sistem", "uyarılabilirlik"],
            []
        ),
        (
            "Bu karmaşık retiküler formasyon ağı rostral ponstan başlayarak mezensefalonun santral tegmental bölgesine kadar uzanır.",
            "**Anatomik Boyut:** Rostral ponstan mezensefalon santral tegmentumuna uzanan formasyon.",
            "(ARAS)",
            ["rostral pons", "mezensefalon tegmentumu"],
            []
        ),
        (
            "Retiküler nöronlardan kaynaklanan eksitatör uyarılar santral tegmental fasikül aracılığıyla yukarı doğru iletilir.",
            "**İletim Yolu:** Santral tegmental fasikül üzerinden üst merkezlere eksitatör sinyal iletimi.",
            "Sentral tegmental fasikül",
            ["santral tegmental fasikül", "eksitatör uyarı"],
            []
        ),
        (
            "Bu sisteme paralel olarak beyin sapından kortekse doğrudan uzanan kritik monoaminerjik afferent projeksiyonlar bulunur.",
            "**Monoaminerjik Yollar:** Beyin sapından kortekse doğrudan uzanan monoaminerjik afferent projeksiyonlar.",
            "Direkt afferent sistemler",
            ["monoaminerjik projeksiyon", "direkt afferent"],
            []
        ),
        (
            "Bu direkt afferent sistemlerin başında serotonerjik innervasyonu sağlayan raphe nükleusları gelir.",
            "**Serotonerjik Girdi:** Raphe nükleusundan kaynaklanan yaygın serotonerjik projeksiyonlar.",
            "(raphe nucleus, locus ceruleus,",
            ["raphe nükleusu", "serotonerjik"],
            []
        ),
        (
            "Bir diğer hayati merkez ise tüm santral sinir sistemine yaygın noradrenerjik lifler gönderen lokus seruleus nükleusudur.",
            "**Noradrenerjik Merkez:** Lokus seruleustan kaynaklanan yaygın noradrenerjik projeksiyonlar.",
            "(raphe nucleus, locus ceruleus,",
            ["lokus seruleus", "noradrenerjik lifler"],
            []
        ),
        (
            "Ayrıca uyanıklık ve otonomik entegrasyonda rol oynayan parabrakialis nükleusu da bu afferent aktivasyon ağının vazgeçilmez bir parçasıdır.",
            "**Parabrakialis Rolü:** Parabrakialis nükleusunun uyanıklık ve aktivasyon entegrasyonundaki görevi.",
            "parabrachialis)",
            ["parabrakialis nükleusu", "aktivasyon ağı"],
            []
        )
    ]),

    (5, "k2-02-b02", "Bilincin Anatomik Temeli ve ARAS Ağı", "k2-02-p004", [
        (
            "Normal uyku uyanıklık döngüsü ve çevresel uyarılabilirlik rostral pons ve mezensefalondaki santral gri cevherden doğan eksitatör aktivitenin üst merkezlere eksiksiz ulaşmasına bağlıdır.",
            "**Eksitatör İletim:** Santral gri cevherden doğan aktivitenin üst beyin merkezlerine eksiksiz ulaşımı.",
            "Normal uyku-uyanıklık ve uyarılabilirlik;",
            ["santral gri cevher", "eksitatör aktivite"],
            []
        ),
        (
            "Asendan retiküler aktive edici sistemden çıkan bu eksitatör lifler ilk olarak talamusun intralaminar ve sentromedyan nükleuslarına projekte olur.",
            "**Talamik Nükleuslar:** ARAS liflerinin talamusun intralaminar ve sentromedyan nükleuslarına projeksiyonu.",
            "Talamusun IL ve CM nükleusları",
            ["talamus", "intralaminar", "sentromedyan"],
            []
        ),
        (
            "Talamus gelen bu uyanıklık sinyallerini filtreleyip organize ederek serebral korteksin tüm alanlarına yaygın biçimde dağıtan ana nöral santraldir.",
            "**Talamo-Kortikal Dağıtım:** Uyanıklık sinyallerini organize ederek tüm serebral kortekse diffüz dağıtma.",
            "Talamusun IL ve CM nükleusları",
            ["serebral korteks", "talamo-kortikal"],
            []
        ),
        (
            "Uyarılabilirlik ağı aynı zamanda bazal ön beyin hipotalamus ve korteks ile karşılıklı güçlü bağlantılar kurar.",
            "**Karşılıklı Ağ:** Bazal ön beyin, hipotalamus ve serebral korteks arasındaki kesintisiz bağlantı bütünlüğü.",
            "Bazal ön beyin,",
            ["bazal ön beyin", "hipotalamus"],
            []
        ),
        (
            "Bu nedenle tam bir bilinç durumunun korunabilmesi için hem beyin sapındaki retiküler sistemin hem de her iki serebral korteksin işlevsel bütünlüğü zorunludur.",
            "**İşlevsel Bütünlük:** Retiküler sistem ile bilateral korteksin eş zamanlı işlevsel bütünlük şartı.",
            "Serebral korteksle bağlantı bütünlüğüne",
            ["retiküler sistem", "işlevsel bütünlük"],
            []
        ),
        (
            "Tek taraflı serebral hemisferde gelişen küçük ve sınırlı bir lezyon karşı hemisfer ve beyin sapı sağlamsa hastada koma oluşturmaz.",
            "**Tek Taraflı Lezyon:** Tek taraflı kortikal lezyonun karşı hemisfer sağlamsa komaya yol açmaması.",
            "bağlıdır.",
            ["tek taraflı lezyon", "karşı hemisfer"],
            []
        ),
        (
            "Bir hastada koma gelişebilmesi için ya beyin sapındaki retiküler sistemin doğrudan hasarlanması ya da her iki serebral hemisferin yaygın biçimde baskılanması gerekir.",
            "**Koma Mekanizması:** Komaya gidiş için ya doğrudan retiküler hasar ya da her iki hemisferin yaygın depresyonu.",
            "Serebral korteksle bağlantı bütünlüğüne",
            ["koma mekanizması", "iki taraflı baskılanma"],
            []
        ),
        (
            "Transtentoryal herniasyonlar ise tek taraflı bir kitlenin beyin sapına bası yapması sonucu retiküler sistemi ezerek komaya yol açarlar.",
            "**Herniasyon Basısı:** Transtentoryal herniasyonun beyin sapını ezerek retiküler sistemi devre dışı bırakması.",
            "bağlıdır.",
            ["transtentoryal herniasyon", "retiküler bası"],
            []
        )
    ]),

    # BOLUM 3: Bilinç düzeyleri ve tanımlar
    (6, "k2-02-b03", "Bilinç Düzeyleri ve Terminoloji", "k2-02-p005", [
        (
            "Bilinç kavramı iki temel bileşenin toplamından oluşur; bunlardan ilki uyanıklık hali ikincisi ise kişinin kendisinin ve çevresinin farkında olmasıdır.",
            "**Bilinç Bileşenleri:** Uyanıklık hali ile kendisinin ve çevresinin farkında olma süreçlerinin toplamı.",
            "Bilinç açık: uyanık ve farkında",
            ["uyanıklık hali", "çevresel farkındalık"],
            []
        ),
        (
            "Bilinci tamamen açık olan bir hasta spontan olarak uyanıktır gözleri açıktır ve çevresinde olup bitenlerin tam anlamıyla farkındadır.",
            "**Bilinç Açık:** Spontan uyanık ve çevresinin tam farkında olan normal bilinç düzeyi.",
            "Bilinç açık: uyanık ve farkında",
            ["bilinç açık", "spontan uyanık"],
            []
        ),
        (
            "Uyanıklık ve farkındalığın derecesine göre bilinç bozuklukları klinik olarak basamak basamak sınıflandırılır.",
            "**Klinik Derecelendirme:** Uyanıklık ve farkındalık kaybının derecesine göre basamaklı sınıflama.",
            "Somnolan: çabuk uyandırılabilir ve farkında",
            ["klinik derecelendirme", "basamaklı sınıflama"],
            []
        ),
        (
            "Bu basamakların başında gelen durum somnolans ya da diğer adıyla letarji tablosudur.",
            "**Somnolans Giriş:** Bilinç depresyonunun erken evresi olan somnolans ve letarji tablosu.",
            "Somnolan: çabuk uyandırılabilir ve farkında",
            ["somnolans", "letarji tablosu"],
            []
        ),
        (
            "Somnolan bir hasta kendi haline bırakıldığında sürekli uykuya meyleder ancak sözel bir seslenme veya hafif bir dokunmayla çabucak uyandırılabilir.",
            "**Somnolans Özellikleri:** Kendi haline bırakılınca uyuyan, sözel uyaranla çabuk uyandırılabilen hasta.",
            "Somnolan: çabuk uyandırılabilir ve farkında",
            ["kendi haline bırakılınca", "sözel uyaran"],
            []
        ),
        (
            "Uyandırıldığında hastanın farkındalığı korunmuştur sorulara doğru yanıtlar verir ancak uyaran kesildiği anda tekrar derin bir uykuya dalar.",
            "**Uyaran Kesilmesi:** Uyaran varken farkında ve yanıt veren, uyaran kesilince tekrar uykuya dönen durum.",
            "Somnolan: çabuk uyandırılabilir ve farkında",
            ["farkındalık korunmuş", "uyaran kesilince uyku"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda defalarca sorulmuştur: kendi haline bırakıldığında uyuyan, sözel veya sesli uyaranla çabuk uyandırılabilen, sorulara yanıt verip uyaran sonlandığında yeniden uyku haline geçen bilinç düzeyi somnolans veya letarjidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Sözel uyaranla uyanıp uyaran kesilince uykuya geçen tablo letarji-somnolanstır.",
            "Somnolan: çabuk uyandırılabilir ve farkında",
            ["çıkmış sınav sorusu", "somnolans tanımı", "letarji"],
            [
                "q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-5",
                "past-1790877044163-968531",
                "past-q-2025-2026_DO_NEM_3_FI_NAL_SINAVI-64",
                "q-22_final_230619_145249-64",
                "d3-f-206",
                "d3-f-016",
                "d3-f-069"
            ]
        ),
        (
            "Bu klinik tablo derinleşen serebral depresyonun ya da erken dönem metabolik ensefalopatilerin en tipik başlangıç göstergesidir.",
            "**Metabolik Başlangıç:** Erken dönem metabolik ensefalopatilerin tipik başlangıç klinik tablosu.",
            "Somnolan: çabuk uyandırılabilir ve farkında",
            ["serebral depresyon", "metabolik ensefalopati"],
            []
        )
    ]),

    (6, "k2-02-b03", "Bilinç Düzeyleri ve Terminoloji", "k2-02-p006", [
        (
            "Bilinç depresyonu daha da ilerlediğinde hasta stupor evresine girer.",
            "**Stupor Evresi:** Bilinç baskılanmasının derinleşmesiyle ortaya çıkan stupor dönemi.",
            "Stupor: zorlukla uyandırılabiliyor ve farkındalık",
            ["stupor evresi", "derin baskılanma"],
            []
        ),
        (
            "Stupordaki hasta sesli uyaranlara yanıt vermez ancak kuvvetli ve tekrarlayan ağrılı uyaranlarla zorlukla uyandırılabilir.",
            "**Zorlukla Uyandırılma:** Sesli uyarana yanıtsız, ancak şiddetli ağrılı uyaranla zorlukla uyandırılabilme.",
            "Stupor: zorlukla uyandırılabiliyor ve farkındalık",
            ["ağrılı uyaran", "zorlukla uyandırma"],
            []
        ),
        (
            "Uyandırıldığında hastanın farkındalığı belirgin olarak azalmıştır anlamsız birkaç kelime mırıldanabilir ya da ağrıdan kaçınma hareketi yapar.",
            "**Azalmış Farkındalık:** Farkındalığın ileri derecede kısıtlanması ve amaca yönelik olmayan yanıtlar.",
            "azalmış",
            ["azalmış farkındalık", "kaçınma hareketi"],
            []
        ),
        (
            "Ağrılı uyaran sonlandırıldığı anda hasta derhal yeniden yanıtsızlık ve derin uyku durumuna geri döner.",
            "**Yanıtsızlığa Dönüş:** Ağrılı uyaran biter bitmez derhal derin yanıtsızlık durumuna geri çekilme.",
            "Stupor: zorlukla uyandırılabiliyor ve farkındalık",
            ["uyaran sonlandırılması", "derin yanıtsızlık"],
            []
        ),
        (
            "Koma ise bilinç depresyonunun en ileri basamağıdır komadaki hasta hiçbir sözel fiziksel ya da şiddetli ağrılı uyaranla uyandırılamaz.",
            "**Koma Tanımı:** Hiçbir sözel veya şiddetli ağrılı uyaranla uyandırılamayan derin bilinçsizlik hali.",
            "Koma: uyandırılamıyor ve farkında değil",
            ["koma tanımı", "uyandırılamaz"],
            []
        ),
        (
            "Komada hasta gözlerini açmaz anlamlı hiçbir sözel veya motor yanıt vermez ve çevresiyle olan tüm farkındalık bağı kopmuştur.",
            "**Göz Açmama:** Gözlerin açılmadığı ve farkındalığın tamamen kaybolduğu mutlak yanıtsızlık.",
            "Koma: uyandırılamıyor ve farkında değil",
            ["göz açmaz", "farkındalık bağı kopmuş"],
            []
        ),
        (
            "Stupor ile koma arasındaki bu net sınır hastanın ağrılı uyaranla dahi olsa gözünü açıp açamaması ve çevreyle minimal temas kurabilmesi üzerinden ayırt edilir.",
            "**Stupor-Koma Sınırı:** Ağrılı uyaranla minimal göz açma ve temas kurabilme yeteneği üzerinden ayırıcı tanı.",
            "Koma: uyandırılamıyor ve farkında değil",
            ["ayırıcı sınır", "minimal temas"],
            []
        )
    ]),

    (7, "k2-02-b03", "Bilinç Düzeyleri ve Terminoloji", "k2-02-p007", [
        (
            "Bilinç bozukluklarının ayırıcı tanısında yer alan diğer klinik tablolar ve terminoloji de doğru bir muayene için eksiksiz bilinmelidir.",
            "**Klinik Terminoloji:** Bilinç bozukluklarında ayırıcı tanıya giren diğer kavramlar ve doğru terminoloji.",
            "Konfüzyon",
            ["klinik terminoloji", "doğru muayene"],
            []
        ),
        (
            "Konfüzyon hastanın dikkatini toplama sürdürme ve mantıklı düşünme yeteneğinin bozulduğu zaman ve yer oryantasyonunun kaybolduğu bir şaşkınlık durumudur.",
            "**Konfüzyon:** Dikkat, mantık yürütme ve oryantasyonun bozulduğu bilişsel şaşkınlık tablosu.",
            "Konfüzyon",
            ["konfüzyon", "zaman yer oryantasyonu"],
            []
        ),
        (
            "Deliryum ise konfüzyona ek olarak halüsinasyonlar motor ajitasyon korku ve otonomik sistem hiperaktivitesi ile giden dalgalı akut organik beyin sendromudur.",
            "**Deliryum:** Halüsinasyon, ajitasyon ve otonomik fırtınayla seyreden dalgalı akut organik sendrom.",
            "Deliryum",
            ["deliryum", "halüsinasyon", "motor ajitasyon"],
            []
        ),
        (
            "Demans bilincin uyanıklık düzeyi korunurken bellek soyutlama ve lisan gibi kognitif işlevlerin aylar ve yıllar içinde ilerleyici kaybıdır.",
            "**Demans:** Uyanıklık korunurken bilişsel ve entelektüel yetilerin kronik ilerleyici yıkımı.",
            "Demans",
            ["demans", "kognitif yıkım"],
            []
        ),
        (
            "Vejetatif durum komayı atlatan hastalarda ortaya çıkan uyku uyanıklık döngüsünün geri döndüğü fakat bilişsel farkındalığın hiç bulunmadığı tablodur.",
            "**Vejetatif Durum:** Uyku-uyanıklık döngüsünün korunduğu ancak farkındalığın tamamen bulunmadığı tablo.",
            "Beyin ölümü",
            ["vejetatif durum", "farkındalık yok"],
            []
        ),
        (
            "Vejetatif durumdaki hasta spontan olarak gözlerini açar uykudan uyanır gibi görünür ancak istemli hiçbir motor aktivite veya anlamlı iletişim sergileyemez.",
            "**Spontan Göz Açma:** Gözleri açık uyanır gibi görünen fakat bilişsel iletişim kuramayan hasta.",
            "Beyin ölümü",
            ["istemli motor aktivite", "anlamlı iletişim"],
            []
        ),
        (
            "Beyin ölümü ise beyin hemisferleri ile beyin sapının tüm işlevlerinin geri dönüşsüz olarak tamamen sonlandığı yasal ve tıbbi ölüm halidir.",
            "**Beyin Ölümü:** Hemisferlerin ve beyin sapının tüm işlevlerinin geri dönüşsüz kaybı.",
            "Beyin ölümü",
            ["beyin ölümü", "tıbbi ölüm"],
            []
        ),
        (
            "Koma taklitçilerini ve bu farklı klinik evreleri doğru adlandırmak hastaya uygulanacak tedavinin şeklini ve aciliyetini doğrudan belirler.",
            "**Doğru Adlandırma:** Farklı klinik evrelerin doğru tanınması ile acil tedavi yönetiminin belirlenmesi.",
            "Konfüzyon",
            ["koma taklitçileri", "tedavi aciliyeti"],
            []
        )
    ]),

    # BOLUM 4: İlk aşamada yaklaşım
    (9, "k2-02-b04", "İlk Aşamada Yaklaşım ve Acil Yönetim", "k2-02-p008", [
        (
            "Acil servise bilinci kapalı bir hasta getirildiğinde hekimin ilk aşamadaki birincil amacı fokal yapısal lezyonları global metabolik problemlerden hızla ayırmaktır.",
            "**Birincil Amaç:** Fokal yapısal SSS lezyonları ile global metabolik problemlerin hızla ayrılması.",
            "Fokal yapısal SSS lezyonlarının, global",
            ["fokal yapısal lezyon", "global metabolik problem"],
            []
        ),
        (
            "Çünkü fokal yapısal bir kitle veya kanama acil cerrahi dekompresyon gerektirebilirken global metabolik problemler medikal resüsitasyon ile tedavi edilir.",
            "**Yol Ayrımı:** Fokal lezyonlarda cerrahi müdahale, metabolik olgularda ise medikal resüsitasyon önceliği.",
            "metabolik problemlerden ayrımını yapmak",
            ["cerrahi dekompresyon", "medikal resüsitasyon"],
            []
        ),
        (
            "Bilinci kapalı hastada zaman kaybı kalıcı nöron ölümü anlamına geldiği için muayene stabilizasyon laboratuvar ve tedavi eş zamanlı yürütülmelidir.",
            "**Eş Zamanlı Yönetim:** Muayene, stabilizasyon, laboratuvar ve tedavinin eş zamanlı yürütülmesi zorunluluğu.",
            "Muayene ile birlikte stabilizasyon, laboratuar,",
            ["zaman kaybı", "eş zamanlı planlama"],
            []
        ),
        (
            "İlk saniyelerde derhal hava yolu açıklığı güvenceye alınmalı ve yeterli doku oksijenasyonu sağlamak için yüksek akımlı oksijen başlanmalıdır.",
            "**Oksijen Desteği:** Hava yolu açıklığı ve yeterli doku oksijenasyonu için yüksek akımlı oksijen.",
            "O2, iki geniş IV yol, EKG, kardiak",
            ["hava yolu açıklığı", "yüksek akımlı oksijen"],
            []
        ),
        (
            "Hastaya derhal iki adet geniş çaplı damar yolu açılmalı ve acil medikal infüzyonlar için güvenli venöz erişim sağlanmalıdır.",
            "**Geniş Damar Yolu:** İki geniş periferik damar yolu açarak acil resüsitasyon hattı kurma.",
            "O2, iki geniş IV yol, EKG, kardiak",
            ["iki geniş damar yolu", "venöz erişim"],
            []
        ),
        (
            "Eş zamanlı olarak elektrokardiyografi çekilmeli ve hasta kardiyak monitörizasyona bağlanarak ritim ve tansiyon kesintisiz izlenmelidir.",
            "**Kardiyak Monitörizasyon:** Elektrokardiyografi çekimi ve kesintisiz kardiyak monitörizasyon ile ritim takibi.",
            "EKG, kardiak",
            ["elektrokardiyografi", "kardiyak monitörizasyon"],
            []
        ),
        (
            "Solunum depresyonu veya yetmezliği saptanan olgularda gecikmeden endotrakeal entübasyon planlanmalı ve beyin hipoksiden korunmalıdır.",
            "**Entübasyon Kararı:** Solunum depresyonunda gecikmeden endotrakeal entübasyonla beyni koruma.",
            "monitorizasyon",
            ["endotrakeal entübasyon", "solunum depresyonu"],
            []
        ),
        (
            "Bu temel kardiyorespiratuvar stabilizasyon sağlanmadan hastayı bilgisayarlı tomografi ünitesine taşımak ölümcül komplikasyonlara davetiye çıkarır.",
            "**Radyoloji Öncesi:** Temel stabilizasyon tamamlanmadan hastayı tomografiye göndermenin ölümcül riskleri.",
            "görüntüleme ve tedavi eş zamanlı planlanmalı",
            ["kardiyorespiratuvar stabilizasyon", "tomografi ünitesi"],
            []
        )
    ]),

    (10, "k2-02-b04", "İlk Aşamada Yaklaşım ve Acil Yönetim", "k2-02-p009", [
        (
            "Yaşamsal fonksiyonlar desteklenirken hızlı bir nörolojik değerlendirme yapılır ve fokal bir nörolojik defisitin varlığı araştırılır.",
            "**Hızlı Değerlendirme:** Vital destek sürerken fokal nörolojik defisit varlığının ivedilikle araştırılması.",
            "Hızlı nörolojik değerlendirme",
            ["hızlı değerlendirme", "fokal defisit"],
            []
        ),
        (
            "Tek taraflı pupiller anizokori asimetrik motor yanıtlar ya da hemisferik lateralizasyon bulguları acil cerrahi patolojiyi akla getirir.",
            "**Lateralizasyon:** Tek taraflı anizokori ve motor asimetrinin cerrahi kitle lezyonunu düşündürmesi.",
            "Fokal nöroloji defisit önemli",
            ["anizokori", "motor asimetri", "lateralizasyon"],
            []
        ),
        (
            "Bu hızlı muayene sırasında yatak başında saniyeler içinde yapılması zorunlu olan en kritik laboratuvar testi stik kan şekeri ölçümüdür.",
            "**Stik Kan Şekeri:** Yatak başında saniyeler içinde kan glukoz düzeyinin ölçülmesi gerekliliği.",
            "Stick Kan şekeri (hipoglisemi gerçek bir",
            ["stik kan şekeri", "glukoz ölçümü"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: bilinç bozukluğu olan her hastanın ayırıcı tanısında ilk aşamada değerlendirilmesi gereken ve gerçek bir acil olan tetkik stik kan şekeridir; çünkü hipoglisemi hızla tedavi edilmezse beyinde dakikalar içinde kalıcı hasar ve ölüm oluşturur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Bilinç bozukluğunda ilk aşamada değerlendirilen gerçek acil stik kan şekeridir.",
            "Stick Kan şekeri (hipoglisemi gerçek bir",
            ["çıkmış sınav sorusu", "hipoglisemi acili", "stik glukoz"],
            ["q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-19"]
        ),
        (
            "Kan şekeri düşük saptanan hastaya damar yolu açılır açılmaz damar içi konsantre dekstroz solüsyonu ivedilikle puşe edilmelidir.",
            "**Dekstroz Tedavisi:** Hipoglisemi saptandığında damar içi konsantre dekstrozun ivedi puşesi.",
            "acildir)",
            ["dekstroz solüsyonu", "damar içi puşe"],
            []
        ),
        (
            "Kronik alkolizm veya malnütrisyon öyküsü olan bireylerde ise glukoz verilmeden hemen önce damar içi yüz miligram tiamin uygulanmalıdır.",
            "**Tiamin Önceliği:** Kronik alkolizm ve malnütrisyonda glukozdan önce yüz miligram tiamin uygulaması.",
            "acildir)",
            ["kronik alkolizm", "tiamin uygulaması"],
            []
        ),
        (
            "Tiamin verilmeden glukoz yüklenmesi beynin laktik asidoza sürüklenmesine ve akut Wernicke ensefalopatisinin alevlenmesine neden olabilir.",
            "**Wernicke Riski:** Tiaminsiz glukoz yüklemesinin akut Wernicke ensefalopatisini tetikleme mekanizması.",
            "acildir)",
            ["Wernicke ensefalopatisi", "laktik asidoz"],
            []
        ),
        (
            "Ayrıca komadaki hastada solunum depresyonu ve iğne ucu pupiller görülüyorsa opioid intoksikasyonu düşünülmeli ve tanısal amaçla damar içi nalokson uygulanmalıdır.",
            "**Opioid Triadı ve Nalokson:** Solunum depresyonu ve iğne ucu pupilde opioid intoksikasyonu şüphesi ve nalokson.",
            "Opioid overdozu ?",
            ["opioid overdozu", "iğne ucu pupil", "nalokson"],
            []
        )
    ]),

    # BOLUM 5: Sistemik nedenler
    (11, "k2-02-b05", "Sistemik Nedenler ve Diffüz SSS Etkilenimi", "k2-02-p010", [
        (
            "Santral sinir sistemini difüz olarak etkileyerek koma tablosu oluşturan sistemik nedenlerin başında kanda gaz ve substrat dengesizlikleri gelir.",
            "**Sistemik Spektrum:** Beyin dokusunu diffüz etkileyen sistemik nedenler ve gaz-substrat bozuklukları.",
            "Etiyoloji: Sistemik Neden – SSS Difüz",
            ["sistemik nedenler", "substrat dengesizliği"],
            []
        ),
        (
            "Derin hipoksi ve karbondioksit retansiyonu yani hiperkapni beyin dokusunda yaygın hücresel metabolizma yetmezliğine ve serebral ödeme yol açar.",
            "**Hipoksi ve Hiperkapni:** Derin hipoksi ve hiperkapninin yaygın hücresel yetmezlik ve ödem oluşturması.",
            "Etkilenimi",
            ["derin hipoksi", "hiperkapni", "serebral ödem"],
            []
        ),
        (
            "Kan şekerindeki aşırı oynamalar hipoglisemi kadar kontrolsüz diyabet hastalarında hiperglisemi ve diyabetik ketoasidoz ile karşımıza çıkar.",
            "**Glukoz Uçları:** Hipoglisemi kadar hiperglisemi ve diyabetik ketoasidozun da komaya yol açması.",
            "Hiperglisemi",
            ["diyabetik ketoasidoz", "hiperglisemi"],
            []
        ),
        (
            "Elektrolit anormallikleri içinde özellikle akut gelişen hiponatremi serebral hücre içine su geçişini artırarak beyin ödemi ve status epileptikusa neden olur.",
            "**Hiponatremi Tehlikesi:** Akut hiponatreminin hücre içine su çekerek beyin ödemi ve status epileptikus yapması.",
            "Hiponatremi",
            ["hiponatremi", "status epileptikus"],
            []
        ),
        (
            "Kronik alkolizmde ve beslenme yetersizliğinde tiamin eksikliğine bağlı gelişen Wernicke ensefalopatisi konfüzyon ataksi ve oftalmopleji triadı ile karakterizedir.",
            "**Wernicke Triadı:** Tiamin eksikliğine bağlı gelişen konfüzyon, ataksi ve oftalmopleji klasik triadı.",
            "Wernicke",
            ["Wernicke ensefalopatisi", "oftalmopleji", "ataksi"],
            []
        ),
        (
            "Böbrek yetmezliğinde kanda biriken toksik nitrojen ürünleri üremik ensefalopatiye ve multifokal miyoklonuslara zemin hazırlar.",
            "**Üremik Tablo:** Kanda biriken üre ve toksik nitrojen ürünlerinin üremik ensefalopati oluşturması.",
            "Üremik ensefalopati",
            ["üremik ensefalopati", "miyoklonus"],
            []
        ),
        (
            "Şiddetli enfeksiyon ve sepsis tablolarında salınan proinflamatuvar sitokinler kan beyin bariyerini bozarak sepsis ilişkili ensefalopati tablosu oluşturur.",
            "**Sepsis Ensefalopatisi:** Sistemik enfeksiyon ve sitokin fırtınasının kan-beyin bariyerini bozarak ensefalopati yapması.",
            "Sepsis",
            ["sepsis", "sitokin fırtınası", "kan beyin bariyeri"],
            []
        ),
        (
            "Ağır karaciğer yetmezliğinde kanda artan amonyak hepatik ensefalopatiye kontrolsüz kan basıncı yükselmeleri ise serebral otoregülasyon kaybıyla hipertansif ensefalopatiye yol açar.",
            "**Organ Yetmezlikleri:** Karaciğer yetmezliğinde amonyak artışı ve hipertansif krizde serebral otoregülasyon çöküşü.",
            "Hipertansif",
            ["hepatik ensefalopati", "amonyak", "hipertansif ensefalopati"],
            []
        )
    ]),

    (12, "k2-02-b05", "Sistemik Nedenler ve Diffüz SSS Etkilenimi", "k2-02-p011", [
        (
            "Sistemik nedenler spektrumunda endokrin bezlerin hipo ya da hiperfonksiyonu da önemli bir yer tutar.",
            "**Endokrin Bozukluklar:** Tiroid ve adrenal bezlerin hipo veya hiperfonksiyonu kaynaklı bilinç bozuklukları.",
            "Düşük kardiyak",
            ["endokrin bezler", "fonksiyon bozukluğu"],
            []
        ),
        (
            "Ağır hipotiroidiye bağlı miksödem koması veya aşırı tiroid hormonu salınımı ile giden tiroid fırtınası komaya kadar ilerleyen bilinç değişiklikleri yapabilir.",
            "**Tiroid Uçları:** Miksödem koması ve tiroid fırtınasının derin bilinç depresyonuna yol açması.",
            "debi,",
            ["miksödem koması", "tiroid fırtınası"],
            []
        ),
        (
            "Benzer biçimde adrenal yetmezlik yani Addisonian krizde gelişen şiddetli hipotansiyon ve hiponatremi hastayı hızla komaya sokabilir.",
            "**Adrenal Kriz:** Addisonian krizde gelişen derin hipotansiyon ve hiponatreminin koma yaratması.",
            "Yaygın",
            ["adrenal yetmezlik", "Addisonian kriz"],
            []
        ),
        (
            "Kardiyovasküler sistem yetmezliklerinde düşük kardiyak debi kardiyojenik şok yaygın hipoperfüzyon hipovolemi ve derin anemi beyin perfüzyonunu çökertir.",
            "**Kardiyovasküler Çöküş:** Düşük kardiyak debi, kardiyojenik şok, hipoperfüzyon ve aneminin serebral iskemi yapması.",
            "hipoperfüzyon",
            ["düşük kardiyak debi", "kardiyojenik şok"],
            []
        ),
        (
            "Toksik madde maruziyetleri endüstriyel çözücüler karbonmonoksit inhalasyonu ve zehirlenmeler nörolojik aciller arasında mutlaka akla getirilmelidir.",
            "**Toksik Maddeler:** Çözücüler, karbonmonoksit ve çevresel toksinlerin komadaki rolü.",
            "Hipovolemi,",
            ["toksik madde", "karbonmonoksit"],
            []
        ),
        (
            "Kronik ilaç veya alkol kullanımının aniden kesilmesi deliryum tremens gibi ajitasyon ve otonomik fırtınayla seyreden tablolar doğurur.",
            "**Yoksunluk Krizleri:** Alkol ve sedatif kesilmesinin deliryum tremens ve otonomik hiperaktivite yaratması.",
            "Anemi,",
            ["deliryum tremens", "yoksunluk krizi"],
            []
        ),
        (
            "Psikiyatrik ilaç etkileşimleri sonucunda gelişen serotonin sendromu klonus hipertermi ve konfüzyonla yaşamı tehdit eden bir metabolik acildir.",
            "**Serotonin Sendromu:** Klonus, hipertermi ve konfüzyonla giden yaşamı tehdit edici ilaç reaksiyonu.",
            "Serotonin sendromu",
            ["serotonin sendromu", "klonus", "hipertermi"],
            []
        ),
        (
            "Antipsikotik ilaçların tetiklediği nöroleptik malign sendrom ise yaygın kurşun boru rijiditesi hipertermi ve bilinç bulanıklığı ile seyreder.",
            "**Nöroleptik Malign Sendrom:** Kurşun boru rijiditesi, hipertermi ve bilinç bulanıklığı tablosu.",
            "Nöroleptik malign",
            ["nöroleptik malign sendrom", "kurşun boru rijiditesi"],
            []
        )
    ]),

    # BOLUM 6: Santral sinir sistemine ait nedenler ve herniasyon
    (13, "k2-02-b06", "Santral Sinir Sistemi Nedenleri ve Herniasyon Tipleri", "k2-02-p012", [
        (
            "Bilinç bozukluklarının yüzde on beşini oluşturan primer santral sinir sistemi patolojileri yapısal ve yapısal olmayan nedenler olarak iki grupta incelenir.",
            "**SSS Nedenleri:** Bilinç bozukluklarının yüzde on beşini oluşturan yapısal ve fonksiyonel primer beyin nedenleri.",
            "Etiyoloji: SSS Ait Nedenler",
            ["primer patolojiler", "yapısal nedenler"],
            []
        ),
        (
            "Yapısal santral sinir sistemi nedenlerinin başında kafa travmaları epidural hematomlar subdural kanamalar ve serebral kontüzyonlar gelir.",
            "**Travmatik Kanamalar:** Kafa travmasına bağlı epidural hematom, subdural kanama ve serebral kontüzyonlar.",
            "SSS travması",
            ["kafa travması", "epidural hematom", "subdural kanama"],
            []
        ),
        (
            "Spontan intrakraniyal kanamalar ve anevrizma rüptürüne bağlı subaraknoid kanama ani bilinç kaybının en dramatik yapısal nedenleridir.",
            "**Subaraknoid Kanama:** Anevrizma rüptürüne bağlı subaraknoid kanama ve spontan parankimal hematomlar.",
            "İntrakranial kanama - SAK",
            ["subaraknoid kanama", "spontan hematom"],
            []
        ),
        (
            "Büyük hemisferik iskemik inmeler ya da beyin sapını doğrudan besleyen baziler arterin akut oklüzyonu dakikalar içinde koma tablosu oluşturur.",
            "**İskemik İnme:** Masif hemisferik enfarkt ve baziler arter tıkanıklığının hızla koma yaratması.",
            "İskemik inme",
            ["iskemik inme", "baziler arter oklüzyonu"],
            []
        ),
        (
            "İntrakraniyal yer kaplayan primer beyin tümörleri veya sistemik kanserlerin beyin metastazları kitle etkisiyle bilinci bozar.",
            "**Yer Kaplayan Kitleler:** Primer beyin tümörleri ve metastazların oluşturduğu kitle etkisi ve ödem.",
            "Yer-kaplayan oluşum",
            ["beyin tümörü", "metastaz", "kitle etkisi"],
            []
        ),
        (
            "Yapısal olmayan primer santral nedenler arasında akut bakteriyel menenjit ve viral ensefalit gibi santral sinir sistemi enfeksiyonları yer alır.",
            "**SSS Enfeksiyonları:** Akut bakteriyel menenjit ve viral ensefalitlerin oluşturduğu yaygın inflamatuvar hasar.",
            "SSS enfeksiyonu",
            ["bakteriyel menenjit", "viral ensefalit"],
            []
        ),
        (
            "Ayrıca non konvülzif status epileptikus ya da jeneralize nöbet sonrası uzamış postiktal stupor dönemi bilinci kapalı tutabilir.",
            "**Status Epileptikus:** Non-konvülzif status epileptikus ve uzun süren postiktal stuporun bilinci kapatması.",
            "Nöbetler (status epileptikus / postiktal periyod)",
            ["status epileptikus", "postiktal stupor"],
            []
        ),
        (
            "İleri evre demans hastalarında araya giren basit bir enfeksiyon bile kırılgan nöronal rezervi tüketerek ani bir koma tablosu yaratabilir.",
            "**Demans Rezervi:** İleri evre demanslı hastada araya giren sistemik enfeksiyonun ani koma oluşturabilmesi.",
            "Demans",
            ["demans rezervi", "akut kötüleşme"],
            []
        )
    ]),

    (14, "k2-02-b06", "Santral Sinir Sistemi Nedenleri ve Herniasyon Tipleri", "k2-02-p013", [
        (
            "İntrakraniyal kitle lezyonlarında kafa kemiklerinin rijit yapısı ve falks ile tentoryum gibi dural bölmeler nedeniyle serebral herniasyon sendromları gelişir.",
            "**Herniasyon Mekanizması:** İntrakraniyal kitle etkisi ve kafa içi rijit kompartmanlar nedeniyle doku fıtıklaşması.",
            "SEREBRAL HERNIASYON",
            ["serebral herniasyon", "dural bölmeler"],
            []
        ),
        (
            "Herniasyon şemasında birinci sırada temporal lobun medialinde yer alan unkusun tentoryal çentikten aşağı fıtıklaştığı unkal herniasyon bulunur.",
            "**Unkal Herniasyon:** Medial temporal unkusun tentoryal çentikten aşağı fıtıklaşarak beyin sapına basması.",
            "SEREBRAL HERNIASYON",
            ["unkal herniasyon", "temporal lob"],
            []
        ),
        (
            "Unkal herniasyonda fıtıklaşan doku aynı taraftaki üçüncü kraniyal siniri ve mezensefalon pedinkülünü basarak ipsilateral midriyazis ve karşı tarafta hemipleji yapar.",
            "**Unkal Triad:** İpsilateral dilate fikse pupil ve karşı tarafta hemipleji ile karakterize klinik tablo.",
            "SEREBRAL HERNIASYON",
            ["üçüncü kraniyal sinir", "ipsilateral midriyazis", "hemipleji"],
            []
        ),
        (
            "İkinci sırada diensefalonun ve her iki serebral hemisferin tentoryal yarıktan aşağı doğru simetrik olarak yer değiştirdiği santral tentoryal herniasyon yer alır.",
            "**Santral Herniasyon:** Diensefalon ve bilateral hemisferlerin tentoryal yarıktan simetrik kaudal yer değiştirmesi.",
            "SEREBRAL HERNIASYON",
            ["santral herniasyon", "diensefalon"],
            []
        ),
        (
            "Üçüncü tip singulat girusun falks serebrinin serbest kenarının altından karşı serebral hemisfer tarafına doğru kaydığı singulat ya da subfalsin herniasyondur.",
            "**Subfalsin Herniasyon:** Singulat girusun falks serebri altından karşı tarafa itildiği subfalsin herniasyon.",
            "SEREBRAL HERNIASYON",
            ["singulat herniasyon", "subfalsin"],
            []
        ),
        (
            "Dördüncü herniasyon tipi kafa kemiğindeki cerrahi veya travmatik bir defektten beyin dokusunun dışarı fıtıklaşması yani transkalvaryal herniasyondur.",
            "**Transkalvaryal Tip:** Kafa kemiğindeki defektten beyin parankiminin dışarı taşması.",
            "SEREBRAL HERNIASYON",
            ["transkalvaryal herniasyon", "kemik defekti"],
            []
        ),
        (
            "Beşinci sırada arka çukurdaki kitle etkisi nedeniyle serebellumun tentoryal yarıktan yukarı mezensefalona doğru fıtıklaştığı yukarı serebellar herniasyon bulunur.",
            "**Yukarı Herniasyon:** Arka çukur kitlesiyle serebellumun tentoryumdan yukarı mezensefalona itilmesi.",
            "SEREBRAL HERNIASYON",
            ["yukarı serebellar", "arka çukur kitlesi"],
            []
        ),
        (
            "Altıncı ve en ölümcül tip ise serebellar tonsillerin foramen magnumdan aşağı omurilik kanalına fıtıklaşarak bulbusu ve solunum merkezini ezdiği tonsiller herniasyondur.",
            "**Tonsiller Herniasyon:** Serebellar tonsillerin foramen magnumdan aşağı kayarak bulbus ve solunum merkezini ezmesi.",
            "SEREBRAL HERNIASYON",
            ["tonsiller herniasyon", "foramen magnum", "solunum arresti"],
            []
        )
    ]),

    # BOLUM 7: Fizik muayene ve anahtar noktalar
    (16, "k2-02-b07", "Fizik Muayene ve Anahtar Bulgular", "k2-02-p014", [
        (
            "Komadaki bir hastada nörolojik muayeneden önce vital bulguların titizlikle ölçülmesi tanıya giden en hızlı ipuçlarını sağlar.",
            "**Vital Bulgular:** Nörolojik muayeneden önce vital bulguların titizlikle değerlendirilmesi kuralı.",
            "Vital bulgular:",
            ["vital bulgular", "fizik muayene"],
            []
        ),
        (
            "Solunum frekansı ve ritmi değerlendirilmeli; derin ve hızlı hiperventilasyon asidozu yüzeyel yavaş hipoventilasyon ise sedatif intoksikasyonunu düşündürmelidir.",
            "**Solunum Frekansı:** Hızlı hiperventilasyonun asidozu, yavaş hipoventilasyonun sedatifleri düşündürmesi.",
            "Solunum: hiper- veya hipoventilasyon",
            ["hiperventilasyon", "hipoventilasyon", "sedatif"],
            []
        ),
        (
            "Kan basıncında belirgin artış hipertansif ensefalopatiyi ya da kafa içi basınç artışı sendromunun bir parçası olan Cushing fenomenini gösterir.",
            "**Hipertansiyon ve KİBAS:** Kan basıncı artışının hipertansif krizi veya Cushing refleksini işaret etmesi.",
            "KB: hiper- veya hipotansiton",
            ["kan basıncı", "Cushing fenomeni"],
            []
        ),
        (
            "Buna karşılık derin hipotansiyon varlığında kardiyojenik şok septik şok ya da adrenal kriz akla gelmelidir.",
            "**Hipotansiyon Tablosu:** Derin hipotansiyonun kardiyojenik, septik şok veya adrenal kriz kaynaklı olması.",
            "KB: hiper- veya hipotansiton",
            ["hipotansiyon", "septik şok"],
            []
        ),
        (
            "Arteriyel kan gazında hipoksi ve hiperkapni varlığı doku oksijenasyonunun yetersizliğini somut olarak belgeler.",
            "**Kan Gazı İpuçları:** Hipoksi ve karbondioksit birikiminin arteriyel kan gazıyla objektif belgelenmesi.",
            "Kan gazı: hipoksi veya hiperkarbi",
            ["kan gazı", "hipoksi", "hiperkarbi"],
            []
        ),
        (
            "Hastada yüksek ateş saptanması menenjit viral ensefalit beyin apsesi sepsis veya pnömoni gibi ciddi bir enfeksiyonu işaret eder.",
            "**Ateşli Koma:** Yüksek ateşin menenjit, ensefalit veya sistemik sepsisi kuvvetle düşündürmesi.",
            "Ateş – sistemik enfeksiyon",
            ["yüksek ateş", "menenjit", "ensefalit"],
            []
        ),
        (
            "Hipotermi mevcudiyeti ise uzun süre soğukta kalma miksödem koması etanol veya barbitürat zehirlenmesi ve septik şokta karşımıza çıkar.",
            "**Hipotermi Nedenleri:** Soğuğa maruziyet, miksödem, alkol-barbitürat intoksikasyonu ve septik şok.",
            "Vital bulgular:",
            ["hipotermi", "miksödem", "barbitürat"],
            []
        ),
        (
            "Muayenenin başında hastanın koma derecesi pupillerin durumu uyaranlara yanıtı ve skalpte travma izleri aranmalıdır.",
            "**İlk Gözlem:** Koma derecesi, pupil durumu ve kafa travması bulgularının ilk anda taranması.",
            "Vital bulgular:",
            ["koma derecesi", "pupil durumu", "travma izleri"],
            []
        )
    ]),

    (18, "k2-02-b07", "Fizik Muayene ve Anahtar Bulgular", "k2-02-p015", [
        (
            "Koma fizik muayenesinde klinisyenin asla gözden kaçırmaması gereken son derece kritik anahtar noktalar vardır.",
            "**Kritik Noktalar:** Koma muayenesinde klinisyenin asla atlamaması gereken çekirdek klinik detaylar.",
            "Konfüze hastada postiktal durumdan",
            ["kritik noktalar", "muayene detayları"],
            []
        ),
        (
            "Konfüze veya bilinci kapalı bir hastada geçirilmiş bir epileptik nöbet ve postiktal durumdan şüpheleniliyorsa hastanın ağzı açılıp dil muayenesi yapılmalıdır.",
            "**Dil Muayenesi:** Postiktal durum şüphesinde ağız içinin açılıp dil kenarlarının taranması kuralı.",
            "şüpheleniliyorsa: Dilde ısırık ? NÖBET !!!",
            ["postiktal durum", "dil muayenesi"],
            []
        ),
        (
            "Dilde özellikle dilin lateral kenarlarında taze ısırık izlerinin saptanması geçirilmiş bir jeneralize tonik klonik nöbetin en özgül kanıtıdır.",
            "**Dilde Isırık İzi:** Dil lateral kenarlarındaki taze ısırık izinin geçirilmiş jeneralize nöbete özgüllüğü.",
            "şüpheleniliyorsa: Dilde ısırık ? NÖBET !!!",
            ["dil lateralinde ısırık", "tonik klonik nöbet"],
            []
        ),
        (
            "Skalp kılıfları saçlar tek tek aralanarak dikkatle palpe edilmeli ve gözle taranmalıdır çünkü saçlı derideki küçük travma izleri sıklıkla atlanır.",
            "**Skalp Muayenesi:** Saçlı derinin titizlikle taranarak gizli ve küçük travma izlerinin aranması.",
            "Skalp ayrıntılı muayene edilmeli !!!",
            ["skalp muayenesi", "saçlı deri"],
            []
        ),
        (
            "Atlanan bu minör travmalar altta sessizce büyüyen bir epidural hematomun veya akut subdural kanamanın habercisi olabilir.",
            "**Gizli Hematom:** Küçük skalp travmalarının altında epidural veya subdural hematom yatabilmesi.",
            "Sıklıkla küçük-gizli travmalar atlanır (posttravma!)",
            ["epidural hematom", "subdural kanama"],
            []
        ),
        (
            "Hastadan alkol kokusu alınması hekimi asla yanıltmamalı ve koma nedeni tek başına alkole bağlanarak hasta kenara bırakılmamalıdır.",
            "**Alkol Tuzağı:** Alkol kokusuna aldanıp komayı tek başına intoksikasyona bağlamama uyarısı.",
            "Koma nedeni alkol ?",
            ["alkol kokusu", "yanıltıcı rehavet"],
            []
        ),
        (
            "Çünkü sarhoş bireyler düşme ve travmaya son derece yatkındır; alkol tablosunun altında ölümcül bir subdural hematom ya da subaraknoid kanama yatıyor olabilir.",
            "**Travma ve Alkol:** Sarhoş hastada düşmeye bağlı ölümcül subdural veya subaraknoid kanama riski.",
            "(altta başka etyoloji varmı ?) SAK – SUBDURAL ?",
            ["travma riski", "subaraknoid kanama", "subdural hematom"],
            []
        )
    ]),

    (19, "k2-02-b07", "Fizik Muayene ve Anahtar Bulgular", "k2-02-p016", [
        (
            "Nörolojik muayenede beyin sapının ve serebral yapıların anatomik düzeyini santimetre santimetre belirleyen dört temel klinik parametre vardır.",
            "**Dört Lokalizan Parametre:** Beyin sapı düzeyini santimetre santimetre belirleyen dört temel parametre.",
            "Lokalizan değeri olan klinik",
            ["lokalizan parametreler", "anatomik düzey"],
            []
        ),
        (
            "Bu parametrelerin ilki hastanın ağrılı uyaranlara karşı verdiği iskelet kası motor yanıtları ve sergilediği vücut postürüdür.",
            "**Motor Yanıtlar:** Ağrılı uyarana karşı oluşan ekstremite hareketleri ve karakteristik vücut postürleri.",
            "İskelet kası motor yanıtları",
            ["iskelet kası", "motor yanıtlar", "postür"],
            []
        ),
        (
            "İkinci lokalizan bulgu pupillerin milimetrik çapı ışık refleksi ve aralarındaki simetridir.",
            "**Pupil Bulguları:** Pupillerin çapı, ışığa reaktivitesi ve aralarındaki simetrik durum.",
            "Pupillerin çapı ve reaktivitesi",
            ["pupillerin çapı", "ışık refleksi"],
            []
        ),
        (
            "Üçüncü temel parametre spontan ya da uyarılmış göz hareketleri ile okülosefalik ve okülovestibüler beyin sapı refleksleridir.",
            "**Göz Hareketleri:** Spontan hareketler ile okülosefalik ve okülovestibüler refleks yanıtları.",
            "Göz hareketleri ve okülovestibüler",
            ["göz hareketleri", "okülovestibüler"],
            []
        ),
        (
            "Dördüncü lokalizan parametre ise hastanın sergilediği solunum şekli derinliği ve ritmidir.",
            "**Solunum Paternleri:** Solunumun hızı, ritmi, derinliği ve karakteristik patolojik şekli.",
            "Solunum şekli",
            ["solunum şekli", "solunum ritmi"],
            []
        ),
        (
            "Bu dört temel nörolojik gösterge bir arada değerlendirildiğinde lezyonun kortikal mi diensefalik mi mezensefalik mi pontin mi yoksa medüller mi olduğu netleşir.",
            "**Lezyon Seviyesi:** Dört parametrenin birleşimiyle lezyon düzeyinin korteksten medullaya net tespiti.",
            "bulgular",
            ["kortikal", "mezensefalik", "pontin", "medüller"],
            []
        ),
        (
            "Hekim hiçbir görüntüleme tetkiki olmadan dahi bu dört bulgu ile hastadaki nörolojik lezyonun seviyesini yatak başında tespit edebilir.",
            "**Yatak Başı Teşhis:** Görüntüleme olmaksızın sadece fizik bulgularla yatak başında anatomik lokalizasyon.",
            "bulgular",
            ["yatak başı lokalizasyon", "fizik bulgular"],
            []
        )
    ]),

    # BOLUM 8: Koma skorları ve Glasgow koma skalası
    (20, "k2-02-b08", "Koma Skorları ve Glasgow Koma Skalası", "k2-02-p017", [
        (
            "Bilinç düzeyindeki değişiklikleri objektif olarak sayısallaştırmak ve klinik takiplerde ortak bir dil oluşturmak amacıyla koma skorlama sistemleri geliştirilmiştir.",
            "**Objektif Skorlama:** Bilinç düzeyini sayısallaştıran ve klinik iletişimde ortak dil kuran koma skorları.",
            "Glasgow koma skoru",
            ["koma skorları", "objektif sayısallaştırma"],
            []
        ),
        (
            "Bu sistemlerin dünyada en yaygın kullanılanı travmatik ve nontravmatik olguların tamamında standartlaşan Glasgow Koma Skalasıdır.",
            "**Glasgow Yaygınlığı:** Dünya genelinde travmatik ve nontravmatik tablolarda standartlaşan Glasgow koma skalası.",
            "Glasgow koma skoru",
            ["Glasgow koma skalası", "standart sistem"],
            []
        ),
        (
            "Ayrıca yoğun bakım kliniklerinde beyin sapı reflekslerini ve solunumu da değerlendiren Dörtlü Test yani for skoru ve hepatik koma skalası da kullanılır.",
            "**Diğer Skorlar:** Yoğun bakımlarda tercih edilen dörtlü test skoru ve metabolik tablolarda hepatik koma skalası.",
            "Dörtlü test",
            ["dörtlü test", "for skoru", "hepatik koma skalası"],
            []
        ),
        (
            "Glasgow Koma Skalası üç bağımsız klinik bileşenin puanlanması esasına dayanır.",
            "**Üç Bağımsız Bileşen:** Glasgow koma skalasının üç ana nörolojik muayene basamağı.",
            "Glasgow koma skoru",
            ["üç bileşen", "puanlama esası"],
            []
        ),
        (
            "Bu üç bileşen göz açma yanıtı motor yanıt ve sözel yanıttır.",
            "**Bileşen İsimleri:** Göz açma, motor yanıt ve sözel yanıt kategorileri.",
            "Glasgow koma skoru",
            ["göz açma", "motor yanıt", "sözel yanıt"],
            []
        ),
        (
            "Her bir kategoride hastanın verebildiği en iyi yanıt puanlanır ve elde edilen puanlar toplanarak genel bilinç skoru oluşturulur.",
            "**En İyi Yanıt İlkesi:** Her kategoride hastanın sergilediği en iyi cevabın puanlanması kuralı.",
            "Glasgow koma skoru",
            ["en iyi yanıt", "genel skor"],
            []
        ),
        (
            "Skalanın seri olarak tekrarlanması hastanın tablosunun cerrahi bir herniasyona doğru kötüleşip kötüleşmediğini ya da tedaviye yanıt verip vermediğini gösterir.",
            "**Seri Takip Değeri:** Skalanın tekrarlanmasıyla herniasyona gidişin veya iyileşmenin objektif izlenmesi.",
            "Glasgow koma skoru",
            ["seri takip", "herniasyon izlemi"],
            []
        ),
        (
            "Glasgow Koma Skalasında puanlama yapılırken her parametre ayrı ayrı kaydedilmeli ve tek bir toplam sayıya indirgenmeden önce bileşenler belirtilmelidir.",
            "**Bileşenleri Kaydetme:** Toplam skorun yanında E, M ve V alt puanlarının açıkça belirtilmesi kuralı.",
            "Glasgow koma skoru",
            ["bileşen kaydı", "alt puanlar"],
            []
        )
    ]),

    (22, "k2-02-b08", "Koma Skorları ve Glasgow Koma Skalası", "k2-02-p018", [
        (
            "Glasgow Koma Skalasının ilk bileşeni göz açma yanıtıdır ve en fazla dört puanla derecelendirilir.",
            "**Göz Açma Bileşeni:** Skalanın ilk basamağı olan ve maksimum dört puan alan göz açma yanıtı.",
            "Spontan açık",
            ["göz açma yanıtı", "dört puan"],
            []
        ),
        (
            "Hastanın gözleri ortamda kendiliğinden açık ise ve çevreyi izliyorsa dört puan verilir.",
            "**Spontan Göz Açma:** Gözlerin kendiliğinden açık olması ve çevreyi izlemesi dört puandır.",
            "Spontan açık",
            ["kendiliğinden açık", "çevreyi izleme"],
            []
        ),
        (
            "Hasta seslenildiğinde ya da sözel uyaran verildiğinde gözlerini açıyorsa üç puan alır.",
            "**Sözel Uyaranla Açma:** Sözel seslenmeyle göz açma yanıtı üç puanla değerlendirilir.",
            "Verbal uyaranla",
            ["sözel uyaran", "üç puan"],
            []
        ),
        (
            "Hasta yalnızca tırnak yatağına ya da supraorbital bölgeye uygulanan ağrılı uyaranla gözlerini açıyorsa iki puanla değerlendirilir.",
            "**Ağrılı Uyaranla Açma:** Yalnızca ağrılı uyaran verildiğinde göz açabilme iki puandır.",
            "Ağrılı uyaranla",
            ["ağrılı uyaranla açma", "iki puan"],
            []
        ),
        (
            "Şiddetli ağrılı uyaranlara rağmen hiçbir şekilde göz açma yanıtı alınamıyorsa bir puan verilir.",
            "**Göz Açmama:** Hiçbir uyarana göz açılmaması durumunda verilen taban bir puan.",
            "Açmıyor",
            ["göz açmıyor", "bir puan"],
            []
        ),
        (
            "Skalanın sözel yanıt bileşeni ise en fazla beş puandır; hasta zaman yer ve kişi oryantasyonuna sahip akıcı konuşuyorsa beş puan alır.",
            "**Sözel Oryantasyon:** Zaman, yer ve kişi oryantasyonunun tam olması beş tam puandır.",
            "Spontan açık",
            ["sözel yanıt", "oryantasyon tam"],
            []
        ),
        (
            "Sorulara mantıklı ancak dezoryante ve konfüze yanıtlar veriyorsa dört puan bağlamsız uygunsuz kelimeler kullanıyorsa üç puan verilir.",
            "**Dezoryante ve Uygunsuz:** Dezoryante konuşma dört puan, anlamsız kelimeler çıkarma üç puandır.",
            "Verbal uyaranla",
            ["dezoryante konuşma", "uygunsuz kelimeler"],
            []
        ),
        (
            "Anlaşılır hiçbir kelime çıkarmayıp yalnızca inilti ve homurtu sesleri sergiliyorsa iki puan hiçbir sözel ses çıkaramıyorsa bir puan olarak kaydedilir.",
            "**Homurtu ve Yanıtsızlık:** Anlamsız homurtu sesleri iki puan, tam sözel yanıtsızlık bir puandır.",
            "Açmıyor",
            ["anlamsız homurtu", "sözel yanıtsızlık"],
            []
        )
    ]),

    (24, "k2-02-b08", "Koma Skorları ve Glasgow Koma Skalası", "k2-02-p019", [
        (
            "Skalanın üçüncü ve prognoz açısından en belirleyici bileşeni motor yanıttır ve en fazla altı puanla değerlendirilir.",
            "**Motor Bileşen:** Prognozu en güçlü yansıtan ve maksimum altı puan alan motor yanıt skalası.",
            "Dekortike",
            ["motor yanıt", "altı puan"],
            []
        ),
        (
            "Hasta hekimin sözel emrine uyarak elini kaldırıyor veya parmaklarını sıkıyorsa tam puan olan altı puan alır.",
            "**Emre Uyma:** Sözel komutlara eksiksiz uyulması motor tam puan olan altı puandır.",
            "Dekortike",
            ["emre uyma", "tam puan"],
            []
        ),
        (
            "Ağrılı uyarana karşı elini köprücük kemiğinin üzerine çıkararak ağrı kaynağını uzaklaştırmaya çalışıyorsa ağrıyı lokalize etme olarak beş puan verilir.",
            "**Ağrıyı Lokalize Etme:** Ağrı kaynağını saptayıp uzaklaştırma hareketi beş puandır.",
            "Dekortike",
            ["ağrıyı lokalize etme", "beş puan"],
            []
        ),
        (
            "Ağrı verilen ekstremiteyi hızla geri çekerek kaçınma refleksi gösteriyorsa normal fleksör yanıt olarak dört puan alır.",
            "**Fleksör Kaçınma:** Ağrılı ekstremiteyi hızla geri çekme kaçınma hareketi dört puandır.",
            "Dekortike",
            ["fleksör yanıt", "kaçınma hareketi"],
            []
        ),
        (
            "Anormal fleksör postür sergileyen yani dirsekte fleksiyon addüksiyon ve yumrukları göğse çekme hareketi yapan hastaya dekortike rijidite olarak üç puan verilir.",
            "**Dekortike Rijidite:** Üst ekstremitede fleksiyon ve addüksiyon gösteren dekortike postür üç puandır.",
            "Dekortike",
            ["anormal fleksör postür", "dekortike rijidite"],
            []
        ),
        (
            "Anormal ekstansör postür sergileyen yani kollar ve bacaklarda ekstansiyon içe pronasyon ve rijidite gösteren hastaya deserebre yanıt olarak iki puan verilir.",
            "**Deserebre Rijidite:** Ekstansiyon ve içe pronasyon gösteren deserebre postür iki puandır.",
            "Dekortike",
            ["anormal ekstansör postür", "deserebre rijidite"],
            []
        ),
        (
            "Şiddetli ağrılı uyaranlara karşı hiçbir motor hareket veya kas tonusu gösteremeyen flask hastaya bir puan verilir.",
            "**Flask Yanıtsızlık:** Hiçbir motor hareket gösteremeyen flask kas tablosu bir puandır.",
            "Dekortike",
            ["flask yanıtsızlık", "taban puan"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: ağrılı uyaranla gözlerini açıp iki puan alan, üst ekstremitede dirsek fleksiyonuyla dekortike yanıt sergileyip üç puan alan ve anlamsız sesler çıkarıp iki puan alan bir hastanın Glasgow Koma Skalası skoru yedidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: E2, M3 dekortike ve V2 sesler çıkaran hastanın toplam Glasgow skoru yedidir.",
            "Dekortike",
            ["çıkmış sınav sorusu", "Glasgow puan hesabı", "skor yedi"],
            ["past-1790877040005-770270"]
        )
    ]),

    (28, "k2-02-b08", "Koma Skorları ve Glasgow Koma Skalası", "k2-02-p020", [
        (
            "Motor yanıtlar aynı zamanda komadaki lezyonun anatomik seviyesini doğrudan gösteren nörolojik belirteçlerdir.",
            "**Anatomik Düzey:** Motor yanıt paternlerinin hasarın nöroanatomik seviyesini belirlemesi.",
            "Motor yanıtlar: Lezyon Lokalizasyonu",
            ["lezyon lokalizasyonu", "motor belirteçler"],
            []
        ),
        (
            "Ağrıyı amaca yönelik lokalize edebilen motor yanıtlar serebral korteksin ve hemisferik yolların işlevsel bütünlüğünü koruduğunu gösterir.",
            "**Hemisferik Bütünlük:** Ağrıyı lokalize edebilmenin serebral korteks işlevinin korunduğunu kanıtlaması.",
            "Hemisferik Lezyon",
            ["hemisferik lezyon", "amaca yönelik lokalizasyon"],
            []
        ),
        (
            "Dekortike rijidite kırmızı çekirdeğin yani nükleus ruberin üzerinde diensefalon veya serebral hemisfer düzeyindeki yaygın kortikospinal hasarı işaret eder.",
            "**Dekortike Seviyesi:** Kırmızı çekirdeğin üstünde, hemisfer veya diensefalon düzeyindeki kortikospinal hasar.",
            "Üst Mezensefalon Hasarı",
            ["kırmızı çekirdek", "nükleus ruber", "dekortike"],
            []
        ),
        (
            "Deserebre rijidite ise kırmızı çekirdek ile vestibüler çekirdekler arasında mezensefalon veya üst pons düzeyindeki derin beyin sapı hasarını yansıtır ve klinik gidişatın çok daha kötü olduğunu gösterir.",
            "**Deserebre Seviyesi:** Kırmızı çekirdek altı mezensefalon veya üst pons hasarı ve derin koma tablosu.",
            "Üst Pontin Hasar",
            ["deserebre rijidite", "üst pontin hasar", "kötü prognoz"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: gözleri ağrılı uyaranla açılan hasta iki puan, dezoryante konuşan hasta dört puan ve ağrıyı lokalize eden hasta beş puan alarak toplam on bir puanla hesaplanır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: E2, V4 dezoryante ve M5 lokalize eden hastanın Glasgow koma skoru on birdir.",
            "Motor yanıtlar: Lezyon Lokalizasyonu",
            ["çıkmış sınav sorusu", "toplam skor on bir", "GKS hesabı"],
            ["260b60a805e9"]
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: Glasgow Koma Skalası ile değerlendirilen bir hastada alınabilecek en düşük puan üç, alınabilecek en yüksek normal puan ise on beştir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmiştir: Glasgow Koma Skalasında taban puan üç, tavan tam puan ise on beştir.",
            "Motor yanıtlar: Lezyon Lokalizasyonu",
            ["çıkmış sınav sorusu", "en düşük puan üç", "en yüksek on beş"],
            [
                "04c8b92b1242",
                "0adcc53186e5"
            ]
        ),
        (
            "Sekiz ve altındaki Glasgow koma skoru koma durumunu tanımlar ve hava yolunu koruyamayan bu hastalarda acil endotrakeal entübasyon endikasyonudur.",
            "**Koma Sınırı Sekiz:** Sekiz ve altı skorun koma sayılması ve endotrakeal entübasyon endikasyonu oluşturması.",
            "Motor yanıtlar: Lezyon Lokalizasyonu",
            ["sekiz ve altı skor", "entübasyon endikasyonu"],
            []
        ),
        (
            "Skorun on beşten aşağıya doğru her düşüşü intrakraniyal tablonun kötüleştiğini ve ivedi görüntüleme gerektiğini klinisyene hatırlatır.",
            "**Skor Düşüşü Uyarısı:** Skordaki her düşüşün intrakraniyal kötüleşmeyi ve acil görüntülemeyi işaret etmesi.",
            "Motor yanıtlar: Lezyon Lokalizasyonu",
            ["skor düşüşü", "ivedi görüntüleme"],
            []
        )
    ]),

    # BOLUM 9: Beyin sapı refleksleri ve pupiller
    (31, "k2-02-b09", "Beyin Sapı Refleksleri ve Pupiller", "k2-02-p021", [
        (
            "Komadaki hastada nörolojik lezyonun yerini ve beyin sapının canlılığını değerlendirmek için özel refleksler kullanılır.",
            "**Beyin Sapı Refleksleri:** Beyin sapının fonksiyonel canlılığını ve lokalizasyonunu test eden refleksler.",
            "Komada Kullanılan Başlıca Beyin sapı",
            ["beyin sapı refleksleri", "fonksiyonel canlılık"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda defalarca sorulmuştur: komada anatomik lokalizasyon amacıyla kullanılan başlıca beyin sapı refleksleri ışık refleksi, kornea refleksi, okülosefalik refleks ve okülovestibüler reflekslerdir; yüzeyel bir spinal refleks olan kremaster refleksi beyin sapı refleksleri arasında yer almaz.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Işık, kornea, okülosefalik ve kalorik test beyin sapı refleksidir; kremaster refleksi beyin sapı refleksi değildir.",
            "Refleksleri",
            ["çıkmış sınav sorusu", "kremaster refleksi", "beyin sapı refleksleri"],
            [
                "q-22_final_230619_145249-67",
                "d3-f-097",
                "d3-b-056"
            ]
        ),
        (
            "Işık refleksi afferentini optik sinir efferentini üçüncü kraniyal sinir aracılığıyla mezensefalon tektumunda tamamlar.",
            "**Işık Refleksi Yolu:** İkinci kraniyal sinir afferenti ve üçüncü kraniyal sinir efferentiyle mezensefalik ark.",
            "Komada Kullanılan Başlıca Beyin sapı",
            ["ışık refleksi", "optik sinir", "okülomotor sinir"],
            []
        ),
        (
            "Kornea refleksi trigeminal sinirin oftalmik dalı ile duyuyu alır ve fasiyal sinir aracılığıyla ponsta bilateral göz kırpma yanıtı oluşturur.",
            "**Kornea Refleksi Yolu:** Beşinci sinir oftalmik dalı duyusu ve yedinci sinir motoruyla pontin refleks arkı.",
            "Refleksleri",
            ["kornea refleksi", "trigeminal sinir", "fasiyal sinir"],
            []
        ),
        (
            "Okülosefalik ve okülovestibüler refleksler ise vestibüler çekirdekler ile göz kası nükleusları arasındaki beyin sapı bağlantılarını test eder.",
            "**Vestibüler Refleksler:** Sekizinci sinir vestibüler çekirdekleri ile ekstraoküler motor nükleuslar arası entegrasyon.",
            "Komada Kullanılan Başlıca Beyin sapı",
            ["okülosefalik", "okülovestibüler", "vestibüler çekirdek"],
            []
        ),
        (
            "Yutkunma ve öğürme refleksleri dokuzuncu ve onuncu kraniyal sinirlerle alt beyin sapı yani bulbus fonksiyonlarını denetler.",
            "**Bulber Refleksler:** Dokuzuncu ve onuncu kraniyal sinirler aracılığıyla medüller fonksiyonların denetimi.",
            "Refleksleri",
            ["öğürme refleksi", "yutkunma", "bulbus"],
            []
        ),
        (
            "Bu reflekslerin basamak basamak kaybolması intrakraniyal herniasyonun rostrokaudal yönde beyin sapını ezerek aşağı indiğini belgeler.",
            "**Rostrokaudal Kayıp:** Reflekslerin yukarıdan aşağıya sırayla kaybının herniasyon ilerleyişini belgelemesi.",
            "Komada Kullanılan Başlıca Beyin sapı",
            ["rostrokaudal kayıp", "herniasyon ilerleyişi"],
            []
        ),
        (
            "Reflekslerin tamamının iki taraflı ve kalıcı olarak kaybolması ise beyin ölümü tablosunun en kesin klinik kanıtlarından biridir.",
            "**Beyin Ölümü Kanıtı:** Beyin sapı reflekslerinin iki taraflı ve kalıcı kaybının beyin ölümünü doğrulaması.",
            "Refleksleri",
            ["beyin ölümü", "kalıcı refleks kaybı"],
            []
        )
    ]),

    (32, "k2-02-b09", "Beyin Sapı Refleksleri ve Pupiller", "k2-02-p022", [
        (
            "Pupillerin çapı ışığa reaktivitesi ve simetrisi komadaki hastada anatomik lokalizasyon sağlayan en hassas pencerelerdir.",
            "**Pupil Penceresi:** Pupillerin çapı, ışık yanıtı ve simetrisinin anatomik lezyon düzeyini saptamadaki hassasiyeti.",
            "metabolik ansefalopati:",
            ["pupil çapı", "ışık reaktivitesi", "anatomik pencere"],
            []
        ),
        (
            "Metabolik ensefalopatilerde ve erken diensefalik lezyonlarda pupiller genellikle küçük boyutlu yani miyotiktir ancak ışık refleksi bilateral korunmuştur.",
            "**Metabolik ve Diensefalik:** Pupiller küçük ve reaktiftir; ışık yanıtının korunması metabolik tabloyu gösterir.",
            "küçük, reaktif",
            ["küçük reaktif pupil", "metabolik ensefalopati"],
            []
        ),
        (
            "Pretektal mezensefalon lezyonlarında pupiller geniş ışığa yanıtsız fikse kalır ve zaman zaman hippus adı verilen dalgalanmalar gösterir.",
            "**Pretektal Pupil:** Pretektal hasarda pupiller geniş, fikse ve hippus dalgalanmaları sergiler.",
            "büyük, fikse,hippus",
            ["pretektal lezyon", "hippus", "geniş fikse"],
            []
        ),
        (
            "Mezensefalon tektumunun derin hasarlarında sempatik ve parasempatik innervasyon aynı anda kesildiği için pupiller orta genişlikte ve tamamen ışıksız fikse hale gelir.",
            "**Mezensefalik Fikse:** Hem sempatik hem parasempatik liflerin kesilmesiyle orta genişlikte yanıtsız pupil.",
            "orta büyüklük, fikse",
            ["orta büyüklük fikse", "mezensefalon hasarı"],
            []
        ),
        (
            "Pons lezyonlarında özellikle masif pons kanamalarında inen sempatik yolların iki taraflı harabiyeti sonucu iğne ucu yani pinpoint pupiller gelişir.",
            "**Pons ve Pinpoint:** İnen sempatik liflerin iki taraflı harabiyeti sonucu ileri derecede daralmış pinpoint pupiller.",
            "pinpoint",
            ["pons kanaması", "pinpoint pupil", "iğne ucu"],
            []
        ),
        (
            "Pinpoint pupiller ileri derecede miyotiktir ve güçlü bir ışık kaynağı ve büyüteçle incelendiğinde minimal bir ışık refleksi seçilebilir.",
            "**Pinpoint Işık Yanıtı:** İğne ucu pupillerde büyüteç altında minimal ışık refleksinin korunabilmesi.",
            "pinpoint",
            ["minimal ışık refleksi", "büyüteç muayenesi"],
            []
        ),
        (
            "Tek taraflı unkal herniasyonda ipsilateral temporal lob unkusunun üçüncü kraniyal siniri sıkıştırması sonucu o tarafta geniş ve ışıksız fikse pupil ortaya çıkar.",
            "**Unkal Pupil (3. Sinir):** Temporal lob unkusunun üçüncü sinire basısıyla tek taraflı dilate ve fikse pupil.",
            "dilate, fikse,",
            ["unkal herniasyon", "üçüncü sinir basısı", "anizokori"],
            []
        ),
        (
            "Anizokori ile birlikte bilinç bozukluğu saptanan bir hastada bu bulgu derhal cerrahi dekompresyon gerektiren acil bir kitle etkisi işaretidir.",
            "**Acil Cerrahi Dekompresyon:** Anizokori ve bilinç bozukluğu birlikteliğinin acil cerrahi kitle alarmı olması.",
            "III KS(unkal):",
            ["cerrahi alarm", "kitle etkisi", "anizokori"],
            []
        )
    ]),

    (33, "k2-02-b09", "Beyin Sapı Refleksleri ve Pupiller", "k2-02-p023", [
        (
            "Pupillerin ışık yanıtı toksik maddelerden ve sistemik metabolik uç durumlardan da derinden etkilenir.",
            "**Toksik Pupiller:** Toksik maddeler ve metabolik uç bozuklukların pupil reaktivitesini değiştirmesi.",
            "Midriyatik, ışığa yanıtsız pupil",
            ["toksik maddeler", "pupil yanıtı"],
            []
        ),
        (
            "İki taraflı midriyatik dilate ve ışığa tamamen yanıtsız pupiller atropin skopolamin gibi antikolinerjik ilaç alımlarında izlenir.",
            "**Antikolinerjik Midriyazis:** Atropin ve skopolamin alımında iki taraflı geniş, ışığa yanıtsız midriyatik pupiller.",
            "Atropin, skopolamin, glutetimid, barbiturat",
            ["atropin", "skopolamin", "midriyatik pupil"],
            []
        ),
        (
            "Benzer şekilde glutetimid ve yüksek doz barbitürat intoksikasyonlarında da midriyatik ve ışıksız pupiller tabloya eşlik eder.",
            "**Barbitürat ve Glutetimid:** Glutetimid ve derin barbitürat zehirlenmesinde ışığa yanıtsız midriyazis tablosu.",
            "Atropin, skopolamin, glutetimid, barbiturat",
            ["glutetimid", "barbitürat intoksikasyonu"],
            []
        ),
        (
            "Ağır sistemik hipoksi kardiyak arrest sonrası anoksik beyin hasarı ve derin hipotermi de pupillerin paralitik dilatasyonuna yol açar.",
            "**Anoksi ve Hipotermi:** Ağır anoksi ve derin hipoterminin iki taraflı paralitik midriyazis oluşturması.",
            "Hipoksi",
            ["anoksik hasar", "derin hipotermi", "paralitik dilatasyon"],
            []
        ),
        (
            "Buna karşılık ileri derecede miyotik ve ışıksız pupiller opiat intoksikasyonunun en patognomonik fizik muayene bulgusudur.",
            "**Opiat Miyozisi:** İleri derecede miyotik pinpoint pupillerin opiat intoksikasyonu için tanısal değeri.",
            "İleri miyotik pupil",
            ["opiat intoksikasyonu", "ileri miyotik pupil"],
            []
        ),
        (
            "Koma ileri derecede solunum depresyonu ve iğne ucu miyotik pupillerden oluşan bu klasik triad görüldüğünde hekim derhal damar içi nalokson hazırlamalıdır.",
            "**Klasik Opioid Triadı:** Koma, solunum depresyonu ve miyozis triadında damar içi ivedi nalokson hazırlığı.",
            "Opiate intoksikasyonu",
            ["opioid triadı", "damar içi nalokson"],
            []
        ),
        (
            "Toksik pupillerin bilinmesi gereksiz acil cerrahi girişimleri engellerken spesifik farmakolojik antidotların saniyeler içinde uygulanmasını sağlar.",
            "**Gereksiz Cerrahiden Korunma:** Toksik nedenleri doğru tanıyarak hastayı boş cerrahiden koruma ve antidot uygulama.",
            "Midriyatik, ışığa yanıtsız pupil",
            ["spesifik antidot", "cerrahiyi engelleme"],
            []
        )
    ]),

    # BOLUM 10: Göz hareketleri: okülosefalik ve kalorik test
    (34, "k2-02-b10", "Göz Hareketleri: Okülosefalik ve Kalorik Test", "k2-02-p024", [
        (
            "Göz hareketlerinin ve okülosefalik refleksin değerlendirilmesi beyin sapı tegmentumunun işlevsel bütünlüğünü yansıtır.",
            "**Okülosefalik Refleks:** Beyin sapı tegmentumunun ve kranial sinir entegrasyonunun okülosefalik refleksle ölçümü.",
            "Göz Hareketleri: Okülosefalik R",
            ["göz hareketleri", "okülosefalik refleks"],
            []
        ),
        (
            "Bu muayeneye başlamadan önce hastada servikal omurga travması veya kemik kırığı şüphesi mutlaka ekarte edilmelidir.",
            "**Servikal Güvenlik:** Boyun hareketlerine başlamadan önce servikal travma şüphesinin ekarte edilmesi zorunluluğu.",
            "Baş 30 derecede: her iki tarafa çevrilir ve",
            ["servikal travma", "boyun kırığı şüphesi"],
            []
        ),
        (
            "Boyun güvenliği sağlandıktan sonra hastanın başı otuz derece yükseltilir göz kapakları açık tutularak baş hızla sağa ve sola çevrilir.",
            "**Testin Uygulanışı:** Baş otuz derece fleksiyonda hızla sağa ve sola çevrilerek göz yanıtlarının izlenmesi.",
            "göz hareketleri gözlenir",
            ["otuz derece fleksiyon", "sağa sola çevirme"],
            []
        ),
        (
            "Bilinci kapalı fakat beyin sapı sağlam olan bir hastada gözler başın çevrildiği yönün tam tersine doğru tonik olarak kayar ve orta hatta sabit kalır.",
            "**Pozitif Oyuncak Bebek Gözü:** Beyin sapı sağlamsa gözlerin başın çevrildiği yönün aksine tonik kayması.",
            "Bilinç kapalı",
            ["oyuncak bebek gözü", "tonik kayma", "orta hat"],
            []
        ),
        (
            "Bu tablo oyuncak bebek gözü hareketinin pozitif olduğunu yani mezensefalon pons ve sekizinci sinir çekirdeklerinin sağlam çalıştığını gösterir.",
            "**Sağlam Beyin Sapı:** Pozitif refleksin mezensefalon, pons ve vestibüler çekirdeklerin sağlamlığını kanıtlaması.",
            "Beyin sapı sağlam",
            ["sağlam beyin sapı", "mezensefalon pons bütünlüğü"],
            []
        ),
        (
            "Eğer beyin sapında özellikle pons tegmentumunda yapısal bir lezyon varsa okülosefalik refleks kaybolur.",
            "**Refleks Kaybı:** Pons tegmentumu hasarında okülosefalik refleks arkının kopması ve kaybı.",
            "Göz Hareketleri: Okülosefalik R",
            ["tegmentum lezyonu", "refleks kaybı"],
            []
        ),
        (
            "Refleks kaybolduğunda gözler başın döndürüldüğü yöne doğru hareketsizce birlikte döner ve başla aynı hizada sabit kalır.",
            "**Gözlerin Birlikte Dönmesi:** Refleks yokluğunda gözlerin başla aynı yöne sabit biçimde sürüklenmesi.",
            "göz hareketleri gözlenir",
            ["sabit kalma", "birlikte dönme"],
            []
        ),
        (
            "Okülosefalik yanıtın bilateral yokluğu komadaki hastada beyin sapı hasarının veya ileri evre rostrokaudal herniasyonun objektif bir kanıtıdır.",
            "**Herniasyon Kanıtı:** Okülosefalik yanıt yokluğunun derin beyin sapı hasarını ve herniasyonu belgelemesi.",
            "Beyin sapı sağlam",
            ["rostrokaudal herniasyon", "objektif kanıt"],
            []
        )
    ]),

    (37, "k2-02-b10", "Göz Hareketleri: Okülosefalik ve Kalorik Test", "k2-02-p025", [
        (
            "Okülosefalik refleksin şüpheli olduğu ya da servikal travma nedeniyle boynun hareket ettirilemediği olgularda kalorik test yani vestibülo-oküler refleks uygulanır.",
            "**Kalorik Test Endikasyonu:** Servikal travmalı veya şüpheli olgularda okülovestibüler kalorik testin devreye girmesi.",
            "Vestibülo-oküler refleksler",
            ["kalorik test", "vestibülo-oküler refleks"],
            []
        ),
        (
            "Kalorik test için hastanın başı otuz derece yükseltilerek lateral semisirküler kanal vertikal pozisyona getirilir ve timpanik membran otoskopla kontrol edilir.",
            "**Test Hazırlığı:** Başın otuz derece yükseltilip semisirküler kanalın dikey konuma alınması ve zar kontrolü.",
            "Bilinç kapalı",
            ["lateral semisirküler kanal", "timpanik membran"],
            []
        ),
        (
            "Kulak zarı sağlam olan hastada dış kulak yoluna yavaşça yirmi ila elli mililitre buzlu soğuk su enjekte edilir.",
            "**Soğuk Su İrrigasyonu:** Dış kulak yoluna yirmi-elli mililitre buzlu soğuk suyun yavaş infüzyonu.",
            "Soğuk Su",
            ["soğuk su irrigasyonu", "buzlu su"],
            []
        ),
        (
            "Bilinci kapalı fakat beyin sapı fonksiyonları sağlam bir hastada kortikal fiksasyon mekanizmaları devre dışı kaldığı için hızlı faz görülmez.",
            "**Kortikal Hızlı Faz Yokluğu:** Komadaki hastada korteks baskılandığı için nistagmusun düzeltici hızlı fazının oluşmaması.",
            "Beyin sapı sağlam",
            ["kortikal fiksasyon", "hızlı faz yokluğu"],
            []
        ),
        (
            "Eksitatör endolenf akımının uyarılmasıyla her iki göz küresi yavaşça soğuk su verilen kulağın tarafına doğru tonik olarak sapar.",
            "**Tonik Deviasyon:** Sağlam beyin sapında gözlerin soğuk su verilen kulağa doğru tonik konjuge sapması.",
            "Soğuk Su",
            ["tonik deviasyon", "endolenf akımı"],
            []
        ),
        (
            "Bu tonik konjuge deviasyonun izlenmesi sekizinci sinir pontin vestibüler çekirdekler mediyal longitudinal fasikül ve okülomotor çekirdeklerin sağlamlığını kanıtlar.",
            "**Yolun Sağlamlığı:** Sekizinci sinir, pontin nükleuslar, MLF ve motor çekirdeklerin kesintisiz sağlamlığı.",
            "Beyin sapı sağlam",
            ["mediyal longitudinal fasikül", "vestibüler çekirdek"],
            []
        ),
        (
            "Eğer alt beyin sapında veya ponsta ağır bir harabiyet varsa soğuk su irrigasyonuna rağmen gözlerde hiçbir deviasyon hareketi oluşmaz.",
            "**Yanıtsız Kalorik:** Pons ve alt beyin sapı harabiyetinde hiçbir göz deviasyonunun ortaya çıkmaması.",
            "Bilinç kapalı",
            ["yanıtsız kalorik", "hareketsiz gözler"],
            []
        ),
        (
            "Kalorik teste yanıtın iki taraflı olarak tamamen alınamaması beyin ölümü tanısı konulurken aranan en zorunlu klinik kriterlerden biridir.",
            "**Beyin Ölümü Şartı:** Kalorik yanıtın bilateral tam yokluğunun beyin ölümü protokolündeki zorunlu yeri.",
            "Beyin sapı sağlam",
            ["beyin ölümü protokolü", "zorunlu kriter"],
            []
        )
    ]),

    # BOLUM 11: Komada solunum
    (40, "k2-02-b11", "Komada Solunum Paternleri ve Rostrokaudal Düzeyler", "k2-02-p026", [
        (
            "Solunumun ritmik kontrolü serebral korteksten başlayarak diensefalon mezensefalon pons ve medullaya uzanan hiyerarşik bir ağ tarafından yürütülür.",
            "**Solunum Ağı:** Korteksten medullaya uzanan solunum merkezlerinin hiyerarşik organizasyonu.",
            "Cheyne-Stokes solunumu",
            ["solunum kontrolü", "hiyerarşik ağ"],
            []
        ),
        (
            "Bu nedenle komadaki bir hastanın solunum paterni beyin sapı hasarının hangi anatomik seviyede bulunduğunu açıkça ortaya koyar.",
            "**Lokalizan Solunum:** Solunum paterninin beyin sapındaki hasar düzeyini açıkça yansıtması.",
            "Cheyne-Stokes solunumu",
            ["solunum paterni", "anatomik seviye"],
            []
        ),
        (
            "Cheyne-Stokes solunumu periyodik olarak kreşendo tarzında derinleşip hızlanan ardından dekreşendo azalarak kısa bir apne dönemine giren solunumdur.",
            "**Cheyne-Stokes Solunumu:** Kreşendo tarzı derinleşip dekreşendo azalan ve apneye giren periyodik solunum.",
            "Cheyne-Stokes solunumu",
            ["Cheyne-Stokes solunumu", "kreşendo dekreşendo", "apne"],
            []
        ),
        (
            "Bu solunum şekli bilateral derin serebral hemisfer lezyonlarında ya da diensefalik düzeydeki baskılanmalarda ve metabolik komalarda sıkça izlenir.",
            "**Diensefalik Lezyon:** Bilateral derin hemisfer veya diensefalon lezyonlarında Cheyne-Stokes görülmesi.",
            "Cheyne-Stokes solunumu",
            ["bilateral hemisfer", "diensefalik baskılanma"],
            []
        ),
        (
            "Santral nörojenik hiperventilasyon son derece düzenli derin ve dakikada kırkın üzerinde çok hızlı solunumla karakterizedir.",
            "**Santral Hiperventilasyon:** Düzenli, derin ve dakikada kırkın üzerinde hızlı solunum paterni.",
            "Santral nörojenik hiperventilasyon",
            ["santral nörojenik hiperventilasyon", "hızlı solunum"],
            []
        ),
        (
            "Bu tablo mezensefalon ile üst pons arasındaki tegmental bölge lezyonlarında ortaya çıkar ve kanda belirgin respiratuvar alkaloz oluşturur.",
            "**Mezensefalik Hasar:** Mezensefalon-üst pons tegmentum hasarı ve kanda gelişen respiratuvar alkaloz.",
            "Santral nörojenik hiperventilasyon",
            ["mezensefalon üst pons", "respiratuvar alkaloz"],
            []
        ),
        (
            "Apnestik solunum inspiryumun en zirve noktasında iki ila üç saniye süren kramp benzeri duraklamalarla kendini gösteren patolojik bir solunumdur.",
            "**Apnestik Solunum:** İnspiryum zirvesinde iki-üç saniye süren kramp benzeri duraklamalı solunum.",
            "Apnestik solunum",
            ["apnestik solunum", "inspiryum duraklaması"],
            []
        ),
        (
            "Bu apnestik duraklamalar ponsun orta veya alt tegmentumundaki solunum merkezlerinin hasar gördüğünü gösterir.",
            "**Pontin Solunum:** Ponsun orta veya alt tegmentumundaki solunum merkezlerinin hasarlanması.",
            "Apnestik solunum",
            ["orta alt pons", "pontin tegmentum"],
            []
        )
    ]),

    (41, "k2-02-b11", "Komada Solunum Paternleri ve Rostrokaudal Düzeyler", "k2-02-p027", [
        (
            "Alt pons ve üst medulla bileşkesine ulaşıldığında apneik duraklamalarla ayrılan düzensiz solunum gruplarından oluşan küme solunumu izlenir.",
            "**Küme Solunumu:** Alt pons ve üst medulla bileşkesinde düzensiz solunum grupları ve apne aralıkları.",
            "Beyin Sapı Bulgularının Özeti",
            ["küme solunumu", "alt pons üst medulla"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: medulla oblangata yani bulbus lezyonlarında solunum ritmi ve derinliği tamamen kaotik hale gelir; inspiratuvar nöronların hasarıyla ortaya çıkan bu düzensiz ve yetersiz solunum paternine ataksik solunum veya Biot solunumu denir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Medulla bulbus lezyonunda görülen kaotik düzensiz solunum ataksik solunumdur.",
            "Beyin Sapı Bulgularının Özeti",
            ["çıkmış sınav sorusu", "ataksik solunum", "bulbus lezyonu", "Biot solunumu"],
            ["d3-b-057"]
        ),
        (
            "Ataksik solunum hastanın dakikalar içinde agonal solunuma ve tam solunum arrestine gireceğini haber veren preterminal bir bulgudur.",
            "**Preterminal Aşama:** Ataksik solunumun dakikalar içinde tam apne ve arrest habercisi olması.",
            "Beyin Sapı Bulgularının Özeti",
            ["ataksik solunum", "solunum arresti", "preterminal"],
            []
        ),
        (
            "Beyin sapı bulguları tablosu incelendiğinde lezyonun yukarıdan aşağıya yani rostrokaudal ilerleyişi adım adım izlenebilir.",
            "**Rostrokaudal İlerleme:** Tabloda lezyonun diensefalondan medullaya doğru rostrokaudal iniş basamakları.",
            "Beyin Sapı Bulgularının Özeti",
            ["rostrokaudal iniş", "beyin sapı özeti"],
            []
        ),
        (
            "Erken diensefalik evrede küçük reaktif pupiller ve Cheyne-Stokes solunumu varken mezensefalik evrede pupiller orta genişlikte fikse hale gelir ve hiperventilasyon başlar.",
            "**Diensefalikten Mezensefale:** Küçük reaktif pupil ve Cheyne-Stokes'tan orta genişlikte fikse pupil ve hiperventilasyona geçiş.",
            "Beyin Sapı Bulgularının Özeti",
            ["erken diensefalik evre", "orta mezensefalik"],
            []
        ),
        (
            "Pontin evrede iğne ucu pupiller okülosefalik refleks kaybı ve apnestik solunum tabloya hakim olur.",
            "**Pontin Evre Bulguları:** İğne ucu pupiller, okülosefalik refleks kaybı ve apnestik solunum tablosu.",
            "Beyin Sapı Bulgularının Özeti",
            ["pontin evre", "pinpoint pupil", "apnestik solunum"],
            []
        ),
        (
            "Medüller evreye gelindiğinde ise dilate ışıksız pupiller ataksik solunum ve tam arefleksi ile hasta ölüme sürüklenir.",
            "**Medüller Terminal Evre:** Dilate yanıtsız pupiller, ataksik solunum ve tam arefleksiyle ölüm tablosu.",
            "Beyin Sapı Bulgularının Özeti",
            ["medüller evre", "dilate ışıksız pupil", "arefleksi"],
            []
        ),
        (
            "Bu rostrokaudal kötüleşme basamaklarının iyi bilinmesi herniasyonun hangi aşamada olduğunu tespit edip acil cerrahi müdahale zamanlamasını belirler.",
            "**Cerrahi Zamanlama:** Herniasyon basamağını erken tanıyarak geri dönüşsüz aşamadan önce acil cerrahiye geçiş.",
            "Beyin Sapı Bulgularının Özeti",
            ["herniasyon aşaması", "cerrahi zamanlama"],
            []
        )
    ]),

    # BOLUM 12: Laboratuvar testleri
    (42, "k2-02-b12", "Koma Tanısında Laboratuvar Testleri", "k2-02-p028", [
        (
            "Koma tanısında laboratuvar testleri hastayı gereksiz invaziv girişimlerden kurtaran ve doğrudan geri döndürülebilir etiyolojiyi aydınlatan en güçlü araçtır.",
            "**Laboratuvarın Gücü:** Geri döndürülebilir etiyolojiyi saptayan ve gereksiz cerrahiyi önleyen laboratuvar paneli.",
            "Kan Şekeri (Hipoglisemiyi atlama)",
            ["laboratuvar testleri", "geri döndürülebilir etiyoloji"],
            []
        ),
        (
            "Testlerin başında her zaman kan şekeri gelir ve hipoglisemi koması acil serviste asla atlanmaması gereken bir numaralı hedeftir.",
            "**Bir Numaralı Hedef:** Hipoglisemi komasının laboratuvarda asla atlanmaması gereken birincil hedef olması.",
            "Kan Şekeri (Hipoglisemiyi atlama)",
            ["kan şekeri", "hipoglisemi koması"],
            []
        ),
        (
            "Özellikle diyabetes mellitus tanısıyla insülin kullanan hastalarda ve kronik alkolizm olgularında bilinç kapalılığının en sık nedeni derin hipoglisemidir.",
            "**Diyabet ve Alkolizm:** Diyabetli ve alkolik hastalarda derin hipogliseminin en sık koma sebebi olması.",
            "Özellikle DM ve Kr. Alkolizmde etiyoloji",
            ["diyabetes mellitus", "kronik alkolizm", "derin hipoglisemi"],
            []
        ),
        (
            "Rutin biyokimyada elektrolitler ivedilikle taranmalı ve en sık elektrolit bozukluğu olan sodyum seviyesine bakılmalıdır.",
            "**Sodyum Önceliği:** Biyokimyada en sık elektrolit bozukluğu olan sodyum seviyesinin ivedilikle taranması.",
            "Elektrolitler (en sık Na)",
            ["sodyum seviyesi", "elektrolit paneli"],
            []
        ),
        (
            "Akut hiponatremi serebral ödem ve koma yaparken hipernatremi ise hücresel dehidratasyon ve beyin kanaması riski oluşturur.",
            "**Sodyum Uçları:** Hiponatreminin beyin ödemi, hipernatreminin ise hücresel dehidratasyon oluşturması.",
            "Hiponatremi sık neden, tümör olanlarda",
            ["akut hiponatremi", "hipernatremi", "serebral ödem"],
            []
        ),
        (
            "Malignitesi veya kemik metastazı olan komalı hastalarda hiperkalsemi ve kalsiyum metabolizma bozuklukları mutlaka dışlanmalıdır.",
            "**Hiperkalsemi Riski:** Kanserli ve metastazlı hastalarda kalsiyum yüksekliği ve metabolizma bozuklukları.",
            "kalsiyum metabolizma bozukluğu sık",
            ["malignite", "hiperkalsemi", "kalsiyum bozukluğu"],
            []
        ),
        (
            "Karaciğer enzimlerinin ve kanda amonyak düzeyinin ölçülmesi karaciğer komasını üre ve kreatinin değerleri ise üremik ensefalopatiyi aydınlatır.",
            "**Organ Testleri:** Amonyak ile hepatik koma, üre ve kreatinin ile üremik ensefalopati teşhisi.",
            "Kan Şekeri (Hipoglisemiyi atlama)",
            ["amonyak", "karaciğer koması", "üremi"],
            []
        ),
        (
            "Basit bir biyokimyasal dengesizliğin düzeltilmesi hastanın dakikalar içinde komadan tam uyanıklık haline geçmesini sağlayabilir.",
            "**Hızlı Düzelme:** Biyokimyasal dengesizliğin replasmanı ile hastanın hızla komadan uyanması.",
            "Özellikle DM ve Kr. Alkolizmde etiyoloji",
            ["biyokimyasal düzelme", "tam uyanıklık"],
            []
        )
    ]),

    (43, "k2-02-b12", "Koma Tanısında Laboratuvar Testleri", "k2-02-p029", [
        (
            "Laboratuvar değerlendirmesinde arteriyel kan gazı analizi komanın metabolik ve solunumsal derinliğini ortaya koyan en hayati parametredir.",
            "**Arteriyel Kan Gazı:** Komanın metabolik ve solunumsal derinliğini ortaya koyan arteriyel kan gazı analizi.",
            "Arteryal Kan Gazı (asidoz önemli)",
            ["arteriyel kan gazı", "metabolik derinlik"],
            []
        ),
        (
            "Kan gazında belirgin asidoz mevcudiyeti klinisyene metabolik bir intoksikasyon ya da derin hipoperfüzyon olduğunu haber verir.",
            "**Asidoz Alarmı:** Belirgin asidozun metabolik intoksikasyon veya derin doku hipoperfüzyonunu göstermesi.",
            "Arteryal Kan Gazı (asidoz önemli)",
            ["metabolik asidoz", "doku hipoperfüzyonu"],
            []
        ),
        (
            "Kanda pe ha değerinin düşmesi salisilat zehirlenmesi metanol alımı veya diyabetik ketoasidoz şüphesini en üst basamağa taşır.",
            "**Düşük pH Nedenleri:** Düşük pH değerinin salisilat, metanol veya diyabetik ketoasidozu işaret etmesi.",
            "pH: (salisilat zehirlenmesi, methanol)",
            ["düşük pe ha", "salisilat zehirlenmesi", "metanol"],
            []
        ),
        (
            "Yangından kurtarılan ya da kapalı alanda baygın bulunan olgularda karboksihemoglobin düzeyi ölçülerek karbonmonoksit ve duman zehirlenmesi aranmalıdır.",
            "**Karboksihemoglobin Düzeyi:** Duman ve yangın olgularında karboksihemoglobin ile karbonmonoksit tespiti.",
            "COHbg: (CO, Duman zehirlenmesi)",
            ["karboksihemoglobin", "karbonmonoksit zehirlenmesi"],
            []
        ),
        (
            "Tam kan sayımında lökositoz sepsis ve menenjiti derin anemi ise beyin oksijen sunumunun çökmesini belgeler.",
            "**Hemogram İpuçları:** Lökositoz ile sepsis-menenjit, derin anemi ile hipoksik perfüzyon çöküşü kanıtı.",
            "Tam Kan Sayımı (uzamış kanama zamanı",
            ["tam kan sayımı", "lökositoz", "derin anemi"],
            []
        ),
        (
            "Trombositopeni ve uzamış koagülasyon testleri spontan intrakraniyal kanama riskini ve dissemine intravasküler koagülasyonu gösterir.",
            "**Koagülasyon Bozukluğu:** Trombositopeni ve uzamış pıhtılaşma testlerinin spontan beyin kanaması alarmı vermesi.",
            "önemli)",
            ["trombositopeni", "kanama profili", "intrakraniyal kanama"],
            []
        ),
        (
            "Şüpheli olgularda geniş toksikolojik idrar ve serum taramaları yapılarak aşırı doz sedatif veya stimulan maddeler saptanmalıdır.",
            "**Toksikolojik Tarama:** Geniş idrar ve serum taraması ile sedatif veya uyarıcı toksinlerin belirlenmesi.",
            "Kanama profili",
            ["toksikolojik tarama", "sedatif aşırı dozu"],
            []
        ),
        (
            "Bu laboratuvar sonuçları nörogörüntüleme öncesinde hastanın fizyolojik parametrelerini dengelemek için klinisyene kesin bir yol haritası sunar.",
            "**Görüntüleme Öncesi:** Tomografiye gitmeden önce fizyolojik dengeleri kurmak için kesin laboratuvar yol haritası.",
            "Trombositopeni; Kanama, sepsis",
            ["fizyolojik parametreler", "klinik yol haritası"],
            []
        )
    ]),

    # BOLUM 13: Bilinci kapalı hastaya yaklaşım algoritması
    (45, "k2-02-b13", "Bilinci Kapalı Hastaya Algoritmik Yaklaşım", "k2-02-p030", [
        (
            "Bilinci kapalı hastaya yaklaşım algoritmasında ilk basamak temel yaşam desteği ilkeleri uyarınca hava yolu solunum ve dolaşımın güvenceye alınmasıdır.",
            "**Temel Yaşam Desteği:** Hava yolu, solunum ve dolaşımın güvenceye alınması ile algoritmanın başlaması.",
            "Bilinci Kapalı Hastaya Yaklaşım",
            ["temel yaşam desteği", "hava yolu solunum dolaşım"],
            []
        ),
        (
            "Yeterli oksijenasyon sağlandıktan sonra yanıt alınamayan hastada son derece kritik bir soru sorulur.",
            "**Kritik Soru:** Oksijenasyon sonrası yanıtsız hastada algoritmayı yönlendiren temel soru.",
            "ABC ve",
            ["oksijenasyon", "yanıt alınamayan hasta"],
            []
        ),
        (
            "Bu soru hastanın bilincinin gerçekten kapalı olup olmadığıdır ve algoritmayı iki temel dala ayırır.",
            "**Gerçek Koma mı?:** Bilincin gerçekten kapalı olup olmadığını sorgulayarak iki ana kola ayrılma.",
            "oksijenasyon",
            ["gerçek koma mı", "iki ana kol"],
            []
        ),
        (
            "Eğer bu soruya verilen yanıt hayır ise hasta gerçek bir komada değildir ve koma taklitçisi tablolardan birine sahiptir.",
            "**Koma Taklitçileri Kolu:** Bilinç kapalı değil yanıtında koma taklitçisi tabloların araştırılması.",
            "Yanıt",
            ["koma taklitçileri", "yanıt hayır"],
            []
        ),
        (
            "Koma taklitçilerinin başında locked-in sendromu gelir; baziler arter oklüzyonuna bağlı ventral pons enfarktında hasta tamamen uyanık ve farkındadır ancak vertikal göz hareketleri dışında tüm vücudu felçtir.",
            "**Locked-in Sendromu:** Ventral pons enfarktında hastanın uyanık ve farkında olup vertikal göz hariç tam felçli olması.",
            "alınamayan",
            ["locked-in sendromu", "ventral pons enfarktı", "vertikal göz hareketi"],
            []
        ),
        (
            "İkinci taklitçi psikojenik yanıtsızlık ve katatoni durumlarıdır bu hastalarda göz kapağı direnci ve normal elektroensefalografi mevcuttur.",
            "**Psikojenik Yanıtsızlık:** Psikojen yanıtsızlık ve katatonide göz kapağı direnci ve normal elektroensefalografi.",
            "hasta",
            ["psikojenik yanıtsızlık", "katatoni", "elektroensefalografi"],
            []
        ),
        (
            "Üçüncü taklitçi grup ağır periferik nöromüsküler paraliziler ve rijiditelerdir bu durumlarda hastaya uygun spesifik klinik yaklaşım uygulanır.",
            "**Nöromüsküler Paralizi:** Ağır periferik paraliziler ve rijiditelerde özgül destek tedavisi uygulanması.",
            "Bilinci Kapalı Hastaya Yaklaşım",
            ["nöromüsküler paralizi", "rijidite"],
            []
        ),
        (
            "Koma taklitçileri dışlandıktan sonra algoritmanın gerçek koma dalı açılarak ileri diagnostik basamaklara geçilir.",
            "**Gerçek Koma Dalı:** Taklitçiler dışlandıktan sonra algoritmanın gerçek koma koluna geçişi.",
            "Bilinci Kapalı Hastaya Yaklaşım",
            ["gerçek koma kolu", "ileri basamaklar"],
            []
        )
    ]),

    (51, "k2-02-b13", "Bilinci Kapalı Hastaya Algoritmik Yaklaşım", "k2-02-p031", [
        (
            "Bilincin gerçekten kapalı olduğu doğrulandığında algoritmanın evet dalı devreye girer ve geniş bir metabolik panel başlatılır.",
            "**Geniş Metabolik Panel:** Bilinç gerçekten kapalı dalında derhal geniş biyokimya ve toksikoloji paneli başlatılması.",
            "Kan gazları, glu,",
            ["gerçek koma evet", "geniş metabolik panel"],
            []
        ),
        (
            "Kan gazları glukoz elektrolitler kalsiyum magnezyum üre kreatinin amonyak karaciğer enzimleri ve toksikolojik tarama için kan örnekleri alınır.",
            "**Gereken Kan Testleri:** Kan gazı, glukoz, elektrolitler, amonyak, kalsiyum ve toksikoloji örnekleri.",
            "elektrolitler, Ca,",
            ["glukoz", "elektrolitler", "amonyak", "toksikoloji"],
            []
        ),
        (
            "Laboratuvar sonuçları beklenirken eş zamanlı olarak ampirik antidot tedavileri uygulanır.",
            "**Ampirik Tedavi:** Sonuçlar beklenirken gecikmeden ampirik farmakolojik kokteylin uygulanması.",
            "Mg, üre, Cre,",
            ["ampirik tedavi", "antidot kokteyli"],
            []
        ),
        (
            "Damar içi glukoz puşe edilirken Wernicke ensefalopatisini tetiklememek için öncesinde mutlaka damar içi tiamin verilmelidir.",
            "**Glukoz ve Tiamin:** Dekstroz öncesinde mutlaka tiamin verilerek Wernicke tablosunun önlenmesi.",
            "NH3, AST, tox",
            ["damar içi glukoz", "tiamin önceliği"],
            []
        ),
        (
            "Solunum depresyonu ve miyozis varlığında opioid aşırı dozu için damar içi nalokson enjekte edilir.",
            "**Nalokson Enjeksiyonu:** Solunum depresyonu ve miyoziste damar içi naloksonun tanısal ve terapötik enjeksiyonu.",
            "tarama, ıv glu,",
            ["damar içi nalokson", "opioid antidotu"],
            []
        ),
        (
            "Bilinen benzodiazepin aşırı alımlarında ise solunumu izlenerek kontrollü biçimde damar içi flumazenil verilebilir.",
            "**Flumazenil Uygulaması:** Kanıtlanmış benzodiazepin zehirlenmesinde kontrollü flumazenil kullanımı.",
            "naloksan,",
            ["benzodiazepin", "flumazenil"],
            []
        ),
        (
            "Bu ampirik müdahalelerin ardından algoritmadaki ikinci anahtar soru sorulur; hastada fokal beyin sapı bulguları var mıdır?",
            "**İkinci Anahtar Soru:** Beyin sapı refleksleri ve fokal beyin sapı bulguları var mı sorusu.",
            "flumazenil",
            ["beyin sapı bulguları", "anahtar soru"],
            []
        ),
        (
            "Beyin sapı bulgusunun varlığı veya yokluğu hastanın supratentoryal mi yoksa infratentoryal bir patolojiye mi sahip olduğunu netleştirir.",
            "**Tentoryal Seviye Belirleme:** Beyin sapı bulgusuyla supratentoryal ve infratentoryal düzey kesinleşir.",
            "flumazenil",
            ["supratentoryal", "infratentoryal ayrım"],
            []
        )
    ]),

    (54, "k2-02-b13", "Bilinci Kapalı Hastaya Algoritmik Yaklaşım", "k2-02-p032", [
        (
            "Muayenede beyin sapı refleksleri normalse ve beyin sapı bulgusu yoksa algoritmanın supratentoryal ve diffüz nedenler dalı açılır.",
            "**Beyin Sapı Bulgusu Yok Dalı:** Refleksler normalse supratentoryal ve diffüz metabolik nedenler koluna geçiş.",
            "Lateral şift",
            ["beyin sapı bulgusu yok", "supratentoryal dal"],
            []
        ),
        (
            "Bu dalda lateral şift yapan tek taraflı serebral lezyonlar iki taraflı yaygın hemisferik hasarlar talamik enfarktlar ve enfeksiyöz süreçler düşünülür.",
            "**Supratentoryal Nedenler:** Lateral şift yapan tek lezyon, biserebral yapısal hasar, talamik veya enfeksiyöz patolojiler.",
            "yapan tek",
            ["lateral şift", "biserebral hasar", "talamik lezyon"],
            []
        ),
        (
            "Bu nedenlerin aydınlatılması için acil incelemeler planlanır ve hasta derhal kontrastsız beyin bilgisayarlı tomografisine yönlendirilir.",
            "**Acil Tomografi:** Supratentoryal hasarı saptamak için acil kontrastsız bilgisayarlı tomografi çekimi.",
            "serebral lezyon,",
            ["kontrastsız tomografi", "acil incelemeler"],
            []
        ),
        (
            "Bilgisayarlı tomografide akut kanama kitle ya da orta hat şifti saptanmazsa enfeksiyon şüphesiyle acil lomber ponksiyon yapılarak beyin omurilik sıvısı incelenir.",
            "**Lomber Ponksiyon:** Tomografi normal çıktığında menenjit şüphesiyle beyin omurilik sıvısı incelemesi.",
            "biserebral",
            ["lomber ponksiyon", "beyin omurilik sıvısı"],
            []
        ),
        (
            "Eğer hastada belirgin beyin sapı bulguları mevcutsa algoritmanın arka çukur ve herniasyon dalı devreye girer.",
            "**Beyin Sapı Bulgusu Var Dalı:** Beyin sapı bulgusu varlığında arka çukur lezyonu ve herniasyon koluna geçiş.",
            "yapısal,",
            ["beyin sapı bulgusu var", "arka çukur lezyonu"],
            []
        ),
        (
            "Bu dalda posterior fossada yer kaplayan kitle lezyonları serebellar kanama baziler arter trombozu ve transtentoryal herniasyonlar ön plandadır.",
            "**Arka Çukur Patolojileri:** Posterior fossa kitlesi, serebellar kanama, baziler tromboz ve transtentoryal herniasyon.",
            "talamik,",
            ["posterior fossa kitlesi", "serebellar kanama", "baziler tromboz"],
            []
        ),
        (
            "Arka çukur patolojilerinde dakikalar içinde tonsiller herniasyon ve solunum arresti gelişebileceği için acil beyin cerrahisi konsültasyonu zorunludur.",
            "**Cerrahi Alarm:** Tonsiller herniasyon ve solunum durması riskine karşı acil beyin cerrahisi müdahalesi.",
            "metabolik,",
            ["tonsiller herniasyon", "beyin cerrahisi konsültasyonu"],
            []
        ),
        (
            "Bilgisayarlı tomografi ve manyetik rezonans görüntüleme ile lezyon doğrulanarak ivedi cerrahi dekompresyon uygulanır.",
            "**İvedi Dekompresyon:** Tomografi ve manyetik rezonans ile kanıtlanan lezyonda ivedi cerrahi dekompresyon.",
            "toksik,",
            ["manyetik rezonans", "cerrahi dekompresyon"],
            []
        )
    ]),

    # BOLUM 14: Komalı hastada kan gazı ve osmolar açık
    (60, "k2-02-b14", "Komalı Hastada Kan Gazı ve Osmolar Açık", "k2-02-p033", [
        (
            "Nörogörüntülemesinde fokal yapısal lezyon saptanmayan komalı hastada tanı akış şeması metabolik ve toksik incelemelerle devam eder.",
            "**Metabolik Akış Şeması:** Görüntülemesi normal çıkan komada metabolik ve toksikolojik akış şemasına geçiş.",
            "Komalı Hasta",
            ["metabolik akış şeması", "toksikolojik inceleme"],
            []
        ),
        (
            "Kanda laktat artışı metanol etilen glikol ve salisilat intoksikasyonu gibi anyon açığı yüksek metabolik asidoz nedenleri sistematik olarak taranır.",
            "**Anyon Açığı Asidozu:** Laktat, metanol, etilen glikol ve salisilat kaynaklı yüksek anyon açıklı metabolik asidoz.",
            "Laktat",
            ["laktat artışı", "metanol", "etilen glikol", "salisilat"],
            []
        ),
        (
            "Diyabetik ketoasidoz ve üremi elendikten sonra hastanın serum ozmolalitesi ölçülür ve formülle hesaplanan ozmolalite ile karşılaştırılır.",
            "**Osmolar Açık Hesabı:** Ölçülen serum ozmolalitesi ile hesaplanan ozmolalitenin karşılaştırılması.",
            "© Metanol",
            ["diyabetik ketoasidoz", "üremi", "serum ozmolalitesi"],
            []
        ),
        (
            "Ölçülen ve hesaplanan ozmolalite arasındaki farkın on miliosmolün üzerinde olması pozitif bir osmolar açık bulunduğunu kanıtlar.",
            "**Pozitif Osmolar Açık:** Farkın on miliosmolün üzerinde çıkmasının pozitif osmolar açık kabul edilmesi.",
            "Etilen glikol",
            ["on miliosmol fark", "pozitif osmolar açık"],
            []
        ),
        (
            "Pozitif osmolar açık mevcudiyeti kanda metanol etilen glikol veya izopropil alkol gibi düşük molekül ağırlıklı toksinlerin varlığını kesinleştirir.",
            "**Uçucu Toksinler:** Pozitif açığın metanol, etilen glikol ve izopropil alkol gibi maddeleri kanıtlaması.",
            "> Salisilat",
            ["metanol intoksikasyonu", "izopropil alkol"],
            []
        ),
        (
            "Toksikolojik panellerde barbitürat amfetamin klonidin trisiklik antidepresan organofosfat benzodiazepin ve opioid düzeyleri taranır.",
            "**Geniş Toksik Panel:** Barbitürat, trisiklik antidepresan, organofosfat ve opioid paneli taraması.",
            "Komalı Hasta",
            ["barbitürat", "trisiklik antidepresan", "organofosfat"],
            []
        ),
        (
            "Toksin kaynağı tespit edildiğinde hemodiyaliz sodyum bikarbonat infüzyonu veya spesifik antidot tedavileri hızla devreye sokulur.",
            "**Hedefe Yönelik Tedavi:** Toksin tespitinde hemodiyaliz, bikarbonat ve spesifik antidotların hızla başlanması.",
            "Laktat",
            ["hemodiyaliz", "sodyum bikarbonat", "spesifik antidot"],
            []
        ),
        (
            "Doğru bir toksikolojik analiz tanı konulamayan derin koma olgularında hayat kurtarıcı nihai basamaktır.",
            "**Hayat Kurtarıcı Toksikoloji:** Tanısı belirsiz komada toksikolojik analizin nihai hayat kurtarıcı gücü.",
            "Komalı Hasta",
            ["toksikolojik analiz", "hayat kurtarıcı"],
            []
        )
    ]),

    # BOLUM 15: Sonuç
    (61, "k2-02-b15", "Sonuç ve Klinik Özet", "k2-02-p034", [
        (
            "Sonuç olarak bilinç bozuklukları ve koma tablolarında doğru ve hızlı ayırıcı tanı koyabilmek klinik hekimliğin en hayati sınavıdır.",
            "**Hayati Sınav:** Bilinç bozukluğunda hızlı ve doğru ayırıcı tanının hekimlikteki hayati önemi.",
            "Bilinç bozukluğunda ayırıcı tanısı önemli",
            ["ayırıcı tanı", "klinik sınav"],
            []
        ),
        (
            "Acil serviste ve yoğun bakımda yürütülecek hızlı koordineli ve disiplinler arası bir ekip yaklaşımı hasta sağkalımının temel taşıdır.",
            "**Ekip Yaklaşımı:** Acil ve yoğun bakımda koordineli ve hızlı ekip yaklaşımının yaşamsal rolü.",
            "Hızlı ve ekip yaklaşımı önemli",
            ["ekip yaklaşımı", "hasta sağkalımı"],
            []
        ),
        (
            "Vital parametrelerin stabilizasyonu hipogliseminin yatak başında saptanması ve beyin sapı reflekslerinin değerlendirilmesi ilk basamakta tamamlanmalıdır.",
            "**İlk Basamak Tamamlama:** Vital stabilizasyon, glukoz kontrolü ve beyin sapı muayenesinin ilk anda yapılması.",
            "Bilinç bozukluğunda ayırıcı tanısı önemli",
            ["vital stabilizasyon", "hipoglisemi kontrolü", "beyin sapı refleksleri"],
            []
        ),
        (
            "Fokal yapısal nedenler ile diffüz metabolik problemleri birbirinden ayıran algoritmik düşünce sistemi hekime rehberlik etmelidir.",
            "**Rehber Algoritma:** Fokal lezyon ile metabolik problemi ayıran algoritmik yaklaşımın rehberliği.",
            "Etiyolojiye yönelik tetkik ve erken tedavi",
            ["fokal yapısal", "diffüz metabolik", "rehber algoritma"],
            []
        ),
        (
            "Etiyolojiye yönelik doğru tetkiklerin zamanında seçilmesi ve hedefe yönelik erken tedavinin gecikmeden başlanması prognozu son derece olumlu etkiler.",
            "**Erken Tedavi ve Prognoz:** Doğru tetkik seçimi ve erken etiyolojik tedavinin prognozu olumlu etkilemesi.",
            "prognozuiyi yönde etkiler",
            ["erken tedavi", "olumlu prognoz"],
            []
        ),
        (
            "Geri dönüşsüz nöron hasarı gelişmeden önce atılacak her bilinçli adım hastayı hayata bağlar.",
            "**Nöronal Koruma:** İskemik nöron hasarı oluşmadan atılan bilinçli adımların hastayı yaşatması.",
            "prognozuiyi yönde etkiler",
            ["nöron hasarı", "hayata bağlama"],
            []
        ),
        (
            "Katılımınız ve sabrınız için teşekkür eder klinik stajlarınızda ve hekimlik pratiğinizde başarılar dileriz.",
            "**Dilekler ve Teşekkür:** Katılım için teşekkür ve klinik hekimlik stajlarında başarı temennileri.",
            "Bilinç bozukluğunda ayırıcı tanısı önemli",
            ["katılım teşekkür", "klinik başarılar"],
            []
        ),
        (
            "Bilinç bozukluklarına yaklaşım dersimiz burada sona ermiştir.",
            "**Ders Sonu:** Bilinç bozukluklarına yaklaşım sunumunun tamamlanması.",
            "Bilinç bozukluğunda ayırıcı tanısı önemli",
            ["ders sonu", "sunum tamamlandı"],
            []
        )
    ])
]

print("--- Verifying anchors against kaynak.md ---")
with open(TASLAK / "sayfa_haritasi.json") as f:
    sh = json.load(f)

fig_map = {}
for sp in sh["sayfalar"]:
    n = int(sp.get("sayfa") or 0)
    tur = sp.get("tur")
    if tur not in ("icerik", "sekil", "tablo") or "tekrar" in str(sp.get("ne_anlatiliyor", "")).lower():
        continue
    sek = [x for x in sp.get("sekiller") or [] if "süs" not in x.lower()]
    has_sek = bool(tur in ("sekil", "tablo") or sek)
    if has_sek:
        fig_map[n] = (sek or [sp.get("ne_anlatiliyor", "")])[0]

overrides = {}

# p013: page 14 (all 8 on 14, s0 gets sekil)
for i in range(8):
    overrides[("k2-02-p013", i)] = (14, None, fig_map[14] if i == 0 else None)

# p014: s0..s5 on 16, s6..s7 on 17
for i in range(6):
    overrides[("k2-02-p014", i)] = (16, None, None)
overrides[("k2-02-p014", 6)] = (17, "Hastanın bilinç düzeyi ?", None)
overrides[("k2-02-p014", 7)] = (17, "Fizik Muayene", None)

# p017: s0..s3 on 20, s4..s7 on 21 (s4 gets sekil)
for i in range(4):
    overrides[("k2-02-p017", i)] = (20, "Glasgow koma skoru", None)
for i in range(4, 8):
    overrides[("k2-02-p017", i)] = (21, "GLASGOW KOMA SKALASI", fig_map[21] if i == 4 else None)

# p018: s0..s3 on 22, s4..s7 on 23
for i in range(4):
    overrides[("k2-02-p018", i)] = (22, "Eye", None)
for i in range(4, 8):
    overrides[("k2-02-p018", i)] = (23, "Movement", None)

# p019: s0..s3 on 24 (s0 gets sekil), s4..s7 on 26 (s4 gets sekil)
for i in range(4):
    overrides[("k2-02-p019", i)] = (24, "Dekortike", fig_map[24] if i == 0 else None)
for i in range(4, 8):
    overrides[("k2-02-p019", i)] = (26, "Dekortike", fig_map[26] if i == 4 else None)

# p020: s0..s3 on 28 (s0 gets sekil), s4..s5 on 29, s6..s7 on 30
for i in range(4):
    overrides[("k2-02-p020", i)] = (28, "Hemisferik Lezyon", fig_map[28] if i == 0 else None)
overrides[("k2-02-p020", 4)] = (29, "Verbal", None)
overrides[("k2-02-p020", 5)] = (29, "Verbal", None)
overrides[("k2-02-p020", 6)] = (30, "5-Orien", None)
overrides[("k2-02-p020", 7)] = (30, "5-Orien", None)

# p021: page 31 (s0 gets sekil)
for i in range(8):
    overrides[("k2-02-p021", i)] = (31, None, fig_map[31] if i == 0 else None)

# p022: page 32 (s0 gets sekil)
for i in range(8):
    overrides[("k2-02-p022", i)] = (32, None, fig_map[32] if i == 0 else None)

# p024: s0..s3 on 34 (s0 gets sekil), s4..s7 on 35 (s4 gets sekil)
for i in range(4):
    overrides[("k2-02-p024", i)] = (34, "Beyin sapı sağlam", fig_map[34] if i == 0 else None)
for i in range(4, 8):
    overrides[("k2-02-p024", i)] = (35, "Beyin sapı HASARLI", fig_map[35] if i == 4 else None)

# p025: s0..s2 on 36 (s0 gets sekil), s3..s5 on 37 (s3 gets sekil), s6..s7 on 38 (s6 gets sekil)
for i in range(3):
    overrides[("k2-02-p025", i)] = (36, "Kalorik testler", fig_map[36] if i == 0 else None)
for i in range(3, 6):
    overrides[("k2-02-p025", i)] = (37, "Beyin sapı sağlam", fig_map[37] if i == 3 else None)
for i in range(6, 8):
    overrides[("k2-02-p025", i)] = (38, "Beyin sapı HASARLI", fig_map[38] if i == 6 else None)

# p026: s0..s2 on 39 (s0 gets sekil), s3..s7 on 40 (s3 gets sekil)
for i in range(3):
    overrides[("k2-02-p026", i)] = (39, "Komada solunum", fig_map[39] if i == 0 else None)
for i in range(3, 8):
    overrides[("k2-02-p026", i)] = (40, "Cheyne-Stokes solunumu", fig_map[40] if i == 3 else None)

# p027: page 41 (s0 gets sekil)
for i in range(8):
    overrides[("k2-02-p027", i)] = (41, None, fig_map[41] if i == 0 else None)

# p030: s0 on 45, s1..s2 on 46, s3 on 47, s4 on 48, s5..s6 on 49, s7 on 50
overrides[("k2-02-p030", 0)] = (45, "Bilinci Kapalı Hastaya Yaklaşım", None)
overrides[("k2-02-p030", 1)] = (46, "Bilinç kapalı", None)
overrides[("k2-02-p030", 2)] = (46, "Bilinç kapalı", None)
overrides[("k2-02-p030", 3)] = (47, "hayır", None)
overrides[("k2-02-p030", 4)] = (48, "locked-in synd,", None)
overrides[("k2-02-p030", 5)] = (49, "Uygun", None)
overrides[("k2-02-p030", 6)] = (49, "Uygun", None)
overrides[("k2-02-p030", 7)] = (50, "evet", None)

# p031: s0..s1 on 51, s2 on 52, s3..s4 on 53, s5 on 54, s6..s7 on 55
overrides[("k2-02-p031", 0)] = (51, "Kan gazları, glu,", None)
overrides[("k2-02-p031", 1)] = (51, "elektrolitler, Ca,", None)
overrides[("k2-02-p031", 2)] = (52, "bulguları?", None)
overrides[("k2-02-p031", 3)] = (53, "hayır", None)
overrides[("k2-02-p031", 4)] = (53, "hayır", None)
overrides[("k2-02-p031", 5)] = (54, "Lateral şift", None)
overrides[("k2-02-p031", 6)] = (55, "Acil", None)
overrides[("k2-02-p031", 7)] = (55, "Acil", None)

# p032: s0 on 56, s1..s2 on 57, s3 on 58, s4..s7 on 59
overrides[("k2-02-p032", 0)] = (56, "BBT, metabolik ve", None)
overrides[("k2-02-p032", 1)] = (57, "evet", None)
overrides[("k2-02-p032", 2)] = (57, "evet", None)
overrides[("k2-02-p032", 3)] = (58, "herniasyon,", None)
for i in range(4, 8):
    overrides[("k2-02-p032", i)] = (59, "BBT/MRI, glu,", None)

# p033: page 60 (s0 gets sekil)
for i in range(8):
    overrides[("k2-02-p033", i)] = (60, None, fig_map[60] if i == 0 else None)

# p034: page 61 (s0 gets sekil)
for i in range(8):
    overrides[("k2-02-p034", i)] = (61, None, fig_map[61] if i == 0 else None)

for sayfa, bid, bname, pid, sents in PARAGRAPHS:
    for s_idx, (ses, yazi, capa, spots, cikmis) in enumerate(sents):
        c_sayfa = sayfa
        c_capa = capa
        if (pid, s_idx) in overrides:
            ov_sy, ov_st, _ = overrides[(pid, s_idx)]
            if ov_sy is not None: c_sayfa = ov_sy
            if ov_st is not None: c_capa = ov_st
        ptext = page_dict.get(c_sayfa, "")
        if c_capa not in ptext:
            print(f"ERROR: Anchor not found in page {c_sayfa} for {pid} sentence {s_idx}: {c_capa}")
            sys.exit(1)
print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Global sentence counter
cid_counter = 1
para_last_sent = {}
bolum_map = {}
total_words = 0

for sayfa, bid, bname, pid, sents in PARAGRAPHS:
    if bid not in bolum_map:
        b_idx = len(bolum_map) + 1
        bolum_map[bid] = {
            "id": bid,
            "bolumIndex": b_idx,
            "baslik": bname,
            "paragraflar": []
        }
    
    p_cumleler = []
    for s_idx, (ses, yazi, capa, spots, cikmis) in enumerate(sents):
        cid = f"k2-02-c{cid_counter:04d}"
        cid_counter += 1
        total_words += len(ses.split())
        
        c_sayfa = sayfa
        c_capa = capa
        c_sekil = None
        if (pid, s_idx) in overrides:
            ov_sy, ov_st, ov_sk = overrides[(pid, s_idx)]
            if ov_sy is not None: c_sayfa = ov_sy
            if ov_st is not None: c_capa = ov_st
            if ov_sk is not None: c_sekil = ov_sk
        
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": yazi,
            "slayt": {
                "sayfa": c_sayfa,
                "satir": c_capa
            },
            "etiketler": spots,
            "cikmis": cikmis
        }
        if c_sekil:
            c_obj["slayt"]["sekil"] = c_sekil
        p_cumleler.append(c_obj)
    
    para_last_sent[pid] = p_cumleler[-1]["id"]
    
    p_obj = {
        "id": pid,
        "sayfa": sayfa,
        "slayt": {"sayfa": sayfa},
        "cumleler": p_cumleler
    }
    bolum_map[bid]["paragraflar"].append(p_obj)

bolumler_list = list(bolum_map.values())
konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-02",
    "anahtar": "y25-k2-02-bilinc-bozuklugu-olan-hastaya-yaklasim",
    "bolumler": bolumler_list
}

total_bolum = len(bolumler_list)
total_paras = sum(len(b["paragraflar"]) for b in bolumler_list)
total_sents = sum(len(p["cumleler"]) for b in bolumler_list for p in b["paragraflar"])

print(f"Total Bolumler: {total_bolum}")
print(f"Total Paragraphs: {total_paras}")
print(f"Total Sentences: {total_sents}")
print(f"Total Words: {total_words} (~{total_words/125:.1f} minutes of audio)")

(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Derive metin.md and konusma_metni.md using KV.turet
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Bilinç Bozukluklarına Yaklaşım"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
(TASLAK / "konusma_metni.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md and konusma_metni.md")

# Derive capalar
capa_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        for c in p["cumleler"]:
            capa_list.append({
                "cumle_id": c["id"],
                "sayfa": p["sayfa"],
                "capa": c["slayt"]["satir"]
            })
(TASLAK / "konusma_capalari.json").write_text(json.dumps(capa_list, ensure_ascii=False, indent=2), encoding="utf-8")

sayfa_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        sayfa_list.append({
            "paragraf_id": p["id"],
            "sayfa": p["sayfa"]
        })
(TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfa_list, ensure_ascii=False, indent=2), encoding="utf-8")

# Live semantic drawing commands
cizim_komutlari = [
    {
        "cumle": para_last_sent["k2-02-p001"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Bilinç Değişiklikleri ve Acil Servis",
        "ogeler": [
            "Acil servis ve yoğun bakımda en sık konsültasyon",
            "Anatomik lokalizasyon ve etiyolojik mekanizma",
            "Sistematik ve algoritma temelli yaklaşım"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p002"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Etiyolojik Dağılım Oranları",
        "ogeler": [
            "Yüzde seksen beş metabolik ve sistemik neden",
            "Yalnızca yüzde on beş santral sinir sistemi",
            "Önce yatak başı vital stabilizasyon"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p003"],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Asendan Retiküler Aktive Edici Sistem",
        "ogeler": [
            "Rostral ponstan mezensefalon tegmentumuna uzanır",
            "Serotonerjik raphe ve noradrenerjik lokus seruleus",
            "Uyanıklık ve uyarılabilirliği sürdüren ana ağ"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p004"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Talamo Kortikal Projeksiyonlar",
        "ogeler": [
            "Talamusun intralaminar ve sentromedyan nükleusları",
            "Her iki serebral korteksin işlevsel bütünlüğü",
            "Koma için retiküler hasar veya bilateral baskılanma"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p005"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Bilinç Düzeyleri ve Somnolans",
        "ogeler": [
            "Bilinç açık: Spontan uyanık ve tam farkında",
            "Somnolans: Kendi haline bırakılınca uykuya meyil",
            "Sözel uyaranla çabuk uyanır ve farkındalık korunur"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p006"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Stupor ve Koma Ayrımı",
        "ogeler": [
            "Stupor: Şiddetli ağrılı uyaranla zorlukla uyanır",
            "Farkındalık belirgin azalmış ve kaçınma yanıtı",
            "Koma: Hiçbir sözel veya ağrılı uyaranla uyandırılamaz"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p007"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Bilinç Bozuklukları Terminolojisi",
        "ogeler": [
            "Konfüzyon: Dikkat bozukluğu ve şaşkınlık",
            "Deliryum: Halüsinasyon ve otonomik hiperaktivite",
            "Vejetatif durum: Uyanıklık var ancak farkındalık yok"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p008"],
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "İlk Aşamada Acil Stabilizasyon",
        "ogeler": [
            "Fokal yapısal ile global metabolik ayrımı",
            "Hava yolu ve yüksek akımlı oksijen desteği",
            "İki geniş damar yolu ve kardiyak monitörizasyon"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p009"],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Hızlı Değerlendirme ve Stik Glukoz",
        "ogeler": [
            "Stik kan şekeri: İlk aşamadaki gerçek acil tetkik",
            "Damar içi dekstroz ve tiamin desteği",
            "Opioid şüphesinde iğne ucu pupil ve nalokson"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p010"],
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Difüz Metabolik Sistemik Nedenler",
        "ogeler": [
            "Derin hipoksi, hiperkapni ve diyabetik ketoasidoz",
            "Akut hiponatremi ve serebral ödem tablosu",
            "Wernicke ensefalopatisi ve üremik ensefalopati"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p012"],
        "bas": 0, "son": 4,
        "sayfa": 13,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Santral Sinir Sistemi Nedenleri",
        "ogeler": [
            "Kafa travması: Epidural ve subdural hematom",
            "Spontan subaraknoid kanama ve iskemik inme",
            "Bakteriyel menenjit ve status epileptikus"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p013"],
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Serebral Herniasyon Tipleri",
        "ogeler": [
            "Unkal herniasyon: Üçüncü sinir basısı ve midriyazis",
            "Santral tentoryal ve singulat subfalsin herniasyon",
            "Tonsiller herniasyon: Foramen magnum ve bulbus basısı"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p015"],
        "bas": 0, "son": 4,
        "sayfa": 18,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Fizik Muayenede Anahtar Bulgular",
        "ogeler": [
            "Dilde taze ısırık izi ve jeneralize nöbet",
            "Saçlı deride atlanan minör skalp travması",
            "Travmatik subdural hematom şüphesi"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p016"],
        "bas": 0, "son": 4,
        "sayfa": 19,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Lokalizan Değeri Olan Dört Bulgular",
        "ogeler": [
            "İskelet kası motor yanıtları ve vücut postürü",
            "Pupillerin milimetrik çapı ve ışık refleksi",
            "Göz hareketleri ve patolojik solunum şekli"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p019"],
        "bas": 0, "son": 4,
        "sayfa": 24,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Glasgow Koma Skalası Motor Yanıt",
        "ogeler": [
            "Ağrıyı lokalize etme beş puan",
            "Dekortike fleksör yanıt üç puan",
            "Deserebre ekstansör yanıt iki puan, yanıtsız bir"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p020"],
        "bas": 0, "son": 4,
        "sayfa": 28,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Motor Postür ve Lezyon Seviyesi",
        "ogeler": [
            "Dekortike rijidite: Kırmızı çekirdek üstü kortikospinal",
            "Deserebre rijidite: Mezensefalon üst pons hasarı",
            "En düşük puan üç, en yüksek normal puan on beş"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p021"],
        "bas": 0, "son": 4,
        "sayfa": 31,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Başlıca Beyin Sapı Refleksleri",
        "ogeler": [
            "Işık refleksi, kornea refleksi ve kalorik test",
            "Okülosefalik ve okülovestibüler refleksler",
            "Kremaster refleksi beyin sapı refleksi değildir"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p022"],
        "bas": 0, "son": 4,
        "sayfa": 32,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Pupil Çapı ve Işık Reaktivitesi",
        "ogeler": [
            "Metabolik ensefalopati: Küçük ve reaktif pupil",
            "Unkal herniasyon: Tek taraflı dilate fikse pupil",
            "Pons lezyonları: İleri miyotik pinpoint pupil"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p025"],
        "bas": 0, "son": 4,
        "sayfa": 37,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Okülovestibüler Kalorik Test",
        "ogeler": [
            "Dış kulak yoluna yirmi-elli mililitre buzlu soğuk su",
            "Bilinç kapalı sağlam beyin sapında tonik deviasyon",
            "Yanıt yokluğu alt beyin sapı hasarı ve beyin ölümü"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p027"],
        "bas": 0, "son": 4,
        "sayfa": 41,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Rostrokaudal Solunum Paternleri",
        "ogeler": [
            "Diensefalik: Cheyne-Stokes solunumu",
            "Mezensefalik: Santral nörojenik hiperventilasyon",
            "Medulla bulbus lezyonu: Düzensiz ataksik solunum"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p030"],
        "bas": 0, "son": 4,
        "sayfa": 45,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Koma Taklitçilerinin Ayrımı",
        "ogeler": [
            "Locked-in sendromu: Ventral pons enfarktında uyanık",
            "Psikojenik yanıtsızlık ve katatoni tabloları",
            "Nöromüsküler paralizi ve ağır rijidite"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p033"],
        "bas": 0, "son": 4,
        "sayfa": 60,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Metabolik Asidoz ve Pozitif Osmolar Açık",
        "ogeler": [
            "Laktat, metanol, etilen glikol ve salisilat",
            "On miliosmol üzeri fark pozitif osmolar açık",
            "Uçucu toksinler ve hedefe yönelik hemodiyaliz"
        ]
    }
]

cizim_aday = {"komutlar": cizim_komutlari}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(cizim_komutlari)} commands.")

# Run all 6 quality gates
print("\n--- Running Quality Gate 1: KV.dogrula ---")
kv_errs = KV.dogrula(konusma_v2, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
if kv_errs:
    print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
    for e in kv_errs[:10]: print(" ", e)
    sys.exit(1)
print("PASSED KV.dogrula: 0 HATA")

print("\n--- Running Quality Gate 2: denetle.py ---")
d_rapor = D.Denetim(TASLAK).calistir()
if d_rapor.get("hata", 0) > 0:
    print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
    for e in d_rapor.get("hatalar", [])[:10]: print(" ", e)
    sys.exit(1)
print(f"PASSED denetle.py: 0 HATA · {d_rapor.get('uyari', 0)} UYARI")

print("\n--- Running Quality Gate 3: validate_learning_decks.py ---")
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
    str(TASLAK / "metin.md")
], capture_output=True, text=True)
if r_metin.returncode != 0:
    print("FAILED metin_denetle:", r_metin.stdout, r_metin.stderr)
    sys.exit(1)
print("PASSED metin_denetle: 0 HATA · 0 UYARI")

print("\n--- Running Quality Gate 5: sesli_kapsam ---")
kapsam_errs = IS.sesli_kapsam(TASLAK)
if kapsam_errs:
    print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
    for e in kapsam_errs: print(" ", e)
    sys.exit(1)
print("PASSED sesli_kapsam: 0 HATA")

print("\n--- Running Quality Gate 6: cizim_dogrula.py ---")
sents = []
for b in konusma_v2["bolumler"]:
    for p in b["paragraflar"]:
        for c in p["cumleler"]:
            sents.append(c)

sent_map = {s["id"]: s for s in sents}
cum_text = {}
accum = []
for s in sents:
    accum.append(s["ses"])
    cum_text[s["id"]] = " ".join(accum)

c_errs = []
for idx, d in enumerate(cizim_komutlari):
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
print(f"PASSED cizim_dogrula: {len(cizim_komutlari)}/{len(cizim_komutlari)} KOMUT 0 HATA")
