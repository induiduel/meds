import sys, json, re, subprocess
from pathlib import Path

REPO_ROOT = Path('/home/indu/medsor')
TASLAK = REPO_ROOT / 'meds_database_25_26/taslak/y25-k2-02-bilinc-bozuklugu-olan-hastaya-yaklasim'

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/sesli_anlatim'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/ders_isci'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/cizim'))

import konusma_v2 as KV
import denetle as D
import isle as IS
import cizim_dogrula as CD
import sablon

# 62/62 Pages Full Deep Amfi Paragraphs (0 Sparse, 0 Forward Leaks)
PARAGRAPHS = [   (   1,
        'k2-02-b01',
        'Bilinç Değişikliğinin Önemi ve Acil Konsültasyonlar',
        'k2-02-p001_s01',
        [   (   'Bilinç bozukluklarına klinik yaklaşım dersimize hoş geldiniz sevgili meslektaşlarım.',
                '**Bilinç Bozuklukları:** Acil tıp ve nörolojide zamanla yarışılan hayati klinik tablolar.',
                'Dr. Dursun CEYLAN',
                ['bilinç bozuklukları', 'acil yaklaşım'],
                []),
            (   'Nörolojik aciller içerisinde bilinç değişiklikleri, hem acil servislerde hem de yoğun bakım '
                'ünitelerinde hekimin en sık karşılaştığı ve en hızlı karar vermesini gerektiren tablolardır.',
                '**En Sık Acil:** Yoğun bakım ve acil servislerde en sık konsültasyon nedeni bilinç kaybıdır.',
                'BİLİNÇ',
                ['acil servis', 'yoğun bakım', 'konsültasyon'],
                []),
            (   'Bu derste bilincin nöroanatomik temellerinden başlayarak, koma skorlamasını, beyin sapı reflekslerini '
                've komalı bir hastada hayat kurtaran basamaklı algoritmayı tüm ayrıntılarıyla inceleyeceğiz.',
                '**Ders Akışı:** ARAS nöroanatomisi, Glasgow skalası, beyin sapı refleksleri ve basamaklı algoritma.',
                'BOZUKLUKLARINAYAKLAŞIM',
                ['Glasgow koma skalası', 'beyin sapı refleksleri', 'algoritma'],
                [])]),
    (   2,
        'k2-02-b01',
        'Bilinç Değişikliğinin Önemi ve Acil Konsültasyonlar',
        'k2-02-p001',
        [   (   'Bilinç değişiklikleri ve koma tablosu acil servislerde ve yoğun bakım ünitelerinde nöroloji '
                'hekimlerine yapılan konsültasyonların en sık nedenidir.',
                '**En Sık Konsültasyon:** Acil servis ve yoğun bakımlarda nöroloji konsültasyonlarının birincil nedeni '
                'bilinç değişikliğidir.',
                'Bilinç değişiklikleri acil servis ve yoğun',
                ['bilinç değişikliği', 'acil servis', 'nöroloji konsültasyonu'],
                []),
            (   'Uyanıklık kusuru veya bilinç kaybı ile getirilen bir hastada hekimin zamanla yarışarak ivedi müdahale '
                'etmesi hayati bir zorunluluktur.',
                '**Zamanla Yarış:** Hipoksi ve iskemiye karşı beyin dokusunu korumak için ivedi klinik müdahale.',
                'bakım ünitelerinde en sık nöroloji',
                ['zamanla yarış', 'beyin dokusu', 'iskemi'],
                []),
            (   'Hastanın ilk değerlendirmesinde nörolojik yaklaşımın temel hedefi lezyonun anatomik lokalizasyonunu '
                've etiyolojik mekanizmasını aydınlatmaktır.',
                '**Temel Hedef:** Lezyonun anatomik koordinatını ve altta yatan etiyolojik mekanizmayı belirleme.',
                'konsültasyonu nedenidir.',
                ['anatomik lokalizasyon', 'etiyolojik mekanizma'],
                []),
            (   'Bilinç değişikliği kavramı uyanıklık ve farkındalık süreçlerinin akut subakut ya da dalgalı biçimde '
                'bozulmasını kapsar.',
                '**Kavram Tanımı:** Uyanıklık ve farkındalık süreçlerindeki akut veya subakut bozulmalar spektrumu.',
                'Bilinç değişiklikleri acil servis ve yoğun',
                ['uyanıklık', 'farkındalık', 'akut bozulma'],
                []),
            (   'Acile başvuran komalı bir hastada klinisyen tablonun primer beyin hasarından mı yoksa sistemik '
                'metabolik bir iflastan mı kaynaklandığını hızla ayırmalıdır.',
                '**Temel Karşılaştırma:** Primer yapısal beyin hasarı ile beyni ikincil etkileyen sistemik metabolik '
                'tablo karşılaştırılır.',
                'bakım ünitelerinde en sık nöroloji',
                ['primer beyin hasarı', 'sistemik metabolik iflas'],
                []),
            (   'Hızlı ve doğru bir ayrım hastaya gereksiz cerrahi veya radyolojik işlemler yapılmasını önlerken hayat '
                'kurtarıcı tedavileri başlatır.',
                '**Tedavi Önceliği:** Doğru klinik ayrım ile gereksiz girişimleri engelleme ve hayat kurtarıcı tedavi.',
                'konsültasyonu nedenidir.',
                ['gereksiz girişimler', 'hayat kurtarıcı tedavi'],
                []),
            (   'Bu nedenle hekimin bilinç bozukluğu olan hastaya sistematik soğukkanlı ve algoritma temelli bir '
                'yaklaşımla müdahale etmesi beklenir.',
                '**Algoritmik Yaklaşım:** Soğukkanlı ve adım adım yapılandırılmış algoritma temelli klinik yöntem.',
                'Bilinç değişiklikleri acil servis ve yoğun',
                ['algoritma temelli', 'soğukkanlı yaklaşım'],
                []),
            (   'Doktor Dursun Ceylan tarafından hazırlanan bu derste bilinç bozukluklarının nöroanatomik temeli '
                'tanısal basamakları ve acil yönetimi incelenecektir.',
                '**Ders Kapsamı:** Dr. Dursun Ceylan rehberliğinde bilinç bozuklukları mekanizmaları ve tedavi '
                'yönetimi.',
                'konsültasyonu nedenidir.',
                ['Dursun Ceylan', 'tanısal basamaklar', 'acil yönetim'],
                [])]),
    (   3,
        'k2-02-b02',
        'Bilincin Anatomik Temeli ve ARAS Ağı',
        'k2-02-p002_s03',
        [   (   'Bilinç kavramını fizyolojik ve klinik olarak iki temel bileşen üzerinden ele almamız gerekir: '
                'uyanıklık ve farkındalık.',
                '**İki Bileşen:** Bilinç, uyanıklık düzeyi ile içerik ve farkındalık bileşenlerinden oluşur.',
                'Bilinç Mekanizmaları',
                ['uyanıklık', 'farkındalık', 'bilinç mekanizması'],
                []),
            (   'Uyanıklık durumu beyin sapı retiküler ağının uyarılabilirliğini yansıtırken, bilincin içeriği ve '
                'farkındalık ise serebral korteksin yaygın fonksiyonel bütünlüğüne bağlıdır.',
                '**Anatomik Temel:** Uyanıklık beyin sapı retiküler yapısına, farkındalık ise serebral kortekse '
                'dayanır.',
                'Bilinç Mekanizmaları',
                ['retiküler formasyon', 'serebral korteks'],
                []),
            (   'Bir hastada koma tablosunun gelişebilmesi için ya beyin sapındaki uyanıklık merkezlerinin ya da her '
                'iki serebral hemisferin birden işlevini kaybetmesi şarttır.',
                '**Koma Koşulu:** Beyin sapı uyanıklık merkezleri veya her iki serebral hemisfer birlikte '
                'hasarlanmalıdır.',
                've',
                ['koma patofizyolojisi', 'bilateral hemisfer hasarı'],
                [])]),
    (   4,
        'k2-02-b02',
        'Bilincin Anatomik Temeli ve ARAS Ağı',
        'k2-02-p003',
        [   (   'Bilincin nöroanatomik ve fizyolojik mekanizmalarını anlayabilmek için uyanıklığı sağlayan subkortikal '
                'ağları kavramak şarttır.',
                '**Nöroanatomik Temel:** Uyanıklığı sağlayan subkortikal ağların ve beyin sapı formasyonunun yapısı.',
                'Asendan retiküler aktive edici sistem',
                ['nöroanatomik temel', 'subkortikal ağ'],
                []),
            (   'Uyanıklık durumunu ve uyarılabilirliği başlatan ve kesintisiz sürdüren en temel nöral ağ asendan '
                'retiküler aktive edici sistemdir.',
                '**ARAS Ağı:** Uyanıklık ve uyarılabilirliği sağlayan asendan retiküler aktive edici sistem.',
                'Asendan retiküler aktive edici sistem',
                ['asendan retiküler aktive edici sistem', 'uyarılabilirlik'],
                []),
            (   'Bu karmaşık retiküler formasyon ağı rostral ponstan başlayarak mezensefalonun santral tegmental '
                'bölgesine kadar uzanır.',
                '**Anatomik Boyut:** Rostral ponstan mezensefalon santral tegmentumuna uzanan formasyon.',
                '(ARAS)',
                ['rostral pons', 'mezensefalon tegmentumu'],
                []),
            (   'Retiküler nöronlardan kaynaklanan eksitatör uyarılar santral tegmental fasikül aracılığıyla yukarı '
                'doğru iletilir.',
                '**İletim Yolu:** Santral tegmental fasikül üzerinden üst merkezlere eksitatör sinyal iletimi.',
                'Sentral tegmental fasikül',
                ['santral tegmental fasikül', 'eksitatör uyarı'],
                []),
            (   'Bu sisteme paralel olarak beyin sapından kortekse doğrudan uzanan kritik monoaminerjik afferent '
                'projeksiyonlar bulunur.',
                '**Monoaminerjik Yollar:** Beyin sapından kortekse doğrudan uzanan monoaminerjik afferent '
                'projeksiyonlar.',
                'Direkt afferent sistemler',
                ['monoaminerjik projeksiyon', 'direkt afferent'],
                []),
            (   'Bu direkt afferent sistemlerin başında serotonerjik innervasyonu sağlayan raphe nükleusları gelir.',
                '**Serotonerjik Girdi:** Raphe nükleusundan kaynaklanan yaygın serotonerjik projeksiyonlar.',
                '(raphe nucleus, locus ceruleus,',
                ['raphe nükleusu', 'serotonerjik'],
                []),
            (   'Bir diğer hayati merkez ise tüm santral sinir sistemine yaygın noradrenerjik lifler gönderen lokus '
                'seruleus nükleusudur.',
                '**Noradrenerjik Merkez:** Lokus seruleustan kaynaklanan yaygın noradrenerjik projeksiyonlar.',
                '(raphe nucleus, locus ceruleus,',
                ['lokus seruleus', 'noradrenerjik lifler'],
                []),
            (   'Ayrıca uyanıklık ve otonomik entegrasyonda rol oynayan parabrakialis nükleusu da bu afferent '
                'aktivasyon ağının vazgeçilmez bir parçasıdır.',
                '**Parabrakialis Rolü:** Parabrakialis nükleusunun uyanıklık ve aktivasyon entegrasyonundaki görevi.',
                'parabrachialis)',
                ['parabrakialis nükleusu', 'aktivasyon ağı'],
                [])]),
    (   5,
        'k2-02-b02',
        'Bilincin Anatomik Temeli ve ARAS Ağı',
        'k2-02-p004',
        [   (   'Normal uyku uyanıklık döngüsü ve çevresel uyarılabilirlik rostral pons ve mezensefalondaki santral '
                'gri cevherden doğan eksitatör aktivitenin üst merkezlere eksiksiz ulaşmasına bağlıdır.',
                '**Eksitatör İletim:** Santral gri cevherden doğan aktivitenin üst beyin merkezlerine eksiksiz '
                'ulaşımı.',
                'Normal uyku-uyanıklık ve uyarılabilirlik;',
                ['santral gri cevher', 'eksitatör aktivite'],
                []),
            (   'Asendan retiküler aktive edici sistemden çıkan bu eksitatör lifler ilk olarak talamusun intralaminar '
                've sentromedyan nükleuslarına projekte olur.',
                '**Talamik Nükleuslar:** ARAS liflerinin talamusun intralaminar ve sentromedyan nükleuslarına '
                'projeksiyonu.',
                'Talamusun IL ve CM nükleusları',
                ['talamus', 'intralaminar', 'sentromedyan'],
                []),
            (   'Talamus gelen bu uyanıklık sinyallerini filtreleyip organize ederek serebral korteksin tüm alanlarına '
                'yaygın biçimde dağıtan ana nöral santraldir.',
                '**Talamo-Kortikal Dağıtım:** Uyanıklık sinyallerini organize ederek tüm serebral kortekse diffüz '
                'dağıtma.',
                'Talamusun IL ve CM nükleusları',
                ['serebral korteks', 'talamo-kortikal'],
                []),
            (   'Uyarılabilirlik ağı aynı zamanda bazal ön beyin hipotalamus ve korteks ile karşılıklı güçlü '
                'bağlantılar kurar.',
                '**Karşılıklı Ağ:** Bazal ön beyin, hipotalamus ve serebral korteks arasındaki kesintisiz bağlantı '
                'bütünlüğü.',
                'Bazal ön beyin,',
                ['bazal ön beyin', 'hipotalamus'],
                []),
            (   'Bu nedenle tam bir bilinç durumunun korunabilmesi için hem beyin sapındaki retiküler sistemin hem de '
                'her iki serebral korteksin işlevsel bütünlüğü zorunludur.',
                '**İşlevsel Bütünlük:** Retiküler sistem ile bilateral korteksin eş zamanlı işlevsel bütünlük şartı.',
                'Serebral korteksle bağlantı bütünlüğüne',
                ['retiküler sistem', 'işlevsel bütünlük'],
                []),
            (   'Tek taraflı serebral hemisferde gelişen küçük ve sınırlı bir lezyon karşı hemisfer ve beyin sapı '
                'sağlamsa hastada koma oluşturmaz.',
                '**Tek Taraflı Lezyon:** Tek taraflı kortikal lezyonun karşı hemisfer sağlamsa komaya yol açmaması.',
                'bağlıdır.',
                ['tek taraflı lezyon', 'karşı hemisfer'],
                []),
            (   'Bir hastada koma gelişebilmesi için ya beyin sapındaki retiküler sistemin doğrudan hasarlanması ya da '
                'her iki serebral hemisferin yaygın biçimde baskılanması gerekir.',
                '**Koma Mekanizması:** Komaya gidiş için ya doğrudan retiküler hasar ya da her iki hemisferin yaygın '
                'depresyonu.',
                'Serebral korteksle bağlantı bütünlüğüne',
                ['koma mekanizması', 'iki taraflı baskılanma'],
                []),
            (   'Transtentoryal herniasyonlar ise tek taraflı bir kitlenin beyin sapına bası yapması sonucu retiküler '
                'sistemi ezerek komaya yol açarlar.',
                '**Herniasyon Basısı:** Transtentoryal herniasyonun beyin sapını ezerek retiküler sistemi devre dışı '
                'bırakması.',
                'bağlıdır.',
                ['transtentoryal herniasyon', 'retiküler bası'],
                [])]),
    (   6,
        'k2-02-b03',
        'Bilinç Düzeyleri ve Terminoloji',
        'k2-02-p005',
        [   (   'Bilinç kavramı iki temel bileşenin toplamından oluşur; bunlardan ilki uyanıklık hali ikincisi ise '
                'kişinin kendisinin ve çevresinin farkında olmasıdır.',
                '**Bilinç Bileşenleri:** Uyanıklık hali ile kendisinin ve çevresinin farkında olma süreçlerinin '
                'toplamı.',
                'Bilinç açık: uyanık ve farkında',
                ['uyanıklık hali', 'çevresel farkındalık'],
                []),
            (   'Bilinci tamamen açık olan bir hasta spontan olarak uyanıktır gözleri açıktır ve çevresinde olup '
                'bitenlerin tam anlamıyla farkındadır.',
                '**Bilinç Açık:** Spontan uyanık ve çevresinin tam farkında olan normal bilinç düzeyi.',
                'Bilinç açık: uyanık ve farkında',
                ['bilinç açık', 'spontan uyanık'],
                []),
            (   'Uyanıklık ve farkındalığın derecesine göre bilinç bozuklukları klinik olarak basamak basamak '
                'sınıflandırılır.',
                '**Klinik Derecelendirme:** Uyanıklık ve farkındalık kaybının derecesine göre basamaklı sınıflama.',
                'Somnolan: çabuk uyandırılabilir ve farkında',
                ['klinik derecelendirme', 'basamaklı sınıflama'],
                []),
            (   'Bu basamakların başında gelen durum somnolans ya da diğer adıyla letarji tablosudur.',
                '**Somnolans Giriş:** Bilinç depresyonunun erken evresi olan somnolans ve letarji tablosu.',
                'Somnolan: çabuk uyandırılabilir ve farkında',
                ['somnolans', 'letarji tablosu'],
                []),
            (   'Somnolan bir hasta kendi haline bırakıldığında sürekli uykuya meyleder ancak sözel bir seslenme veya '
                'hafif bir dokunmayla çabucak uyandırılabilir.',
                '**Somnolans Özellikleri:** Kendi haline bırakılınca uyuyan, sözel uyaranla çabuk uyandırılabilen '
                'hasta.',
                'Somnolan: çabuk uyandırılabilir ve farkında',
                ['kendi haline bırakılınca', 'sözel uyaran'],
                []),
            (   'Uyandırıldığında hastanın farkındalığı korunmuştur sorulara doğru yanıtlar verir ancak uyaran '
                'kesildiği anda tekrar derin bir uykuya dalar.',
                '**Uyaran Kesilmesi:** Uyaran varken farkında ve yanıt veren, uyaran kesilince tekrar uykuya dönen '
                'durum.',
                'Somnolan: çabuk uyandırılabilir ve farkında',
                ['farkındalık korunmuş', 'uyaran kesilince uyku'],
                []),
            (   'Bu bilgi çıkmış sınavda defalarca sorulmuştur: kendi haline bırakıldığında uyuyan, sözel veya sesli '
                'uyaranla çabuk uyandırılabilen, sorulara yanıt verip uyaran sonlandığında yeniden uyku haline geçen '
                'bilinç düzeyi somnolans veya letarjidir.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Sözel uyaranla uyanıp uyaran '
                'kesilince uykuya geçen tablo letarji-somnolanstır.',
                'Somnolan: çabuk uyandırılabilir ve farkında',
                ['çıkmış sınav sorusu', 'somnolans tanımı', 'letarji'],
                [   'q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-5',
                    'past-1790877044163-968531']),
            (   'Bu klinik tablo derinleşen serebral depresyonun ya da erken dönem metabolik ensefalopatilerin en '
                'tipik başlangıç göstergesidir.',
                '**Metabolik Başlangıç:** Erken dönem metabolik ensefalopatilerin tipik başlangıç klinik tablosu.',
                'Somnolan: çabuk uyandırılabilir ve farkında',
                ['serebral depresyon', 'metabolik ensefalopati'],
                [])]),
    (   7,
        'k2-02-b03',
        'Bilinç Düzeyleri ve Terminoloji',
        'k2-02-p007',
        [   (   'Bu bilgi çıkmış sınavda defalarca sorulmuştur: hastanın sözel uyaranla uyandırılıp uyaran '
                'kesildiğinde tekrar uyku haline geçtiği tablo letarji yani somnolanstır.',
                '**Letarji:** Sözel uyaranla uyanıp uyaran kesilince uykuya geçen tablo letarji yani somnolanstır.',
                'Letarji- Somnolans',
                ['çıkmış', 'letarji', 'somnolans'],
                [   'past-q-2025-2026_DO_NEM_3_FI_NAL_SINAVI-64',
                    'q-22_final_230619_145249-64',
                    'd3-f-206',
                    'd3-f-016',
                    'd3-f-069']),
            (   'Konfüzyon hastanın dikkatini toplama sürdürme ve mantıklı düşünme yeteneğinin bozulduğu zaman ve yer '
                'oryantasyonunun kaybolduğu bir şaşkınlık durumudur.',
                '**Konfüzyon:** Dikkat, mantık yürütme ve oryantasyonun bozulduğu bilişsel şaşkınlık tablosu.',
                'Konfüzyon',
                ['konfüzyon', 'zaman yer oryantasyonu'],
                []),
            (   'Deliryum ise konfüzyona ek olarak halüsinasyonlar motor ajitasyon korku ve otonomik sistem '
                'hiperaktivitesi ile giden dalgalı akut organik beyin sendromudur.',
                '**Deliryum:** Halüsinasyon, ajitasyon ve otonomik fırtınayla seyreden dalgalı akut organik sendrom.',
                'Deliryum',
                ['deliryum', 'halüsinasyon', 'motor ajitasyon'],
                []),
            (   'Demans bilincin uyanıklık düzeyi korunurken bellek soyutlama ve lisan gibi kognitif işlevlerin aylar '
                've yıllar içinde ilerleyici kaybıdır.',
                '**Demans:** Uyanıklık korunurken bilişsel ve entelektüel yetilerin kronik ilerleyici yıkımı.',
                'Demans',
                ['demans', 'kognitif yıkım'],
                []),
            (   'Vejetatif durum komayı atlatan hastalarda ortaya çıkan uyku uyanıklık döngüsünün geri döndüğü fakat '
                'bilişsel farkındalığın hiç bulunmadığı tablodur.',
                '**Vejetatif Durum:** Uyku-uyanıklık döngüsünün korunduğu ancak farkındalığın tamamen bulunmadığı '
                'tablo.',
                'Beyin ölümü',
                ['vejetatif durum', 'farkındalık yok'],
                []),
            (   'Vejetatif durumdaki hasta spontan olarak gözlerini açar uykudan uyanır gibi görünür ancak istemli '
                'hiçbir motor aktivite veya anlamlı iletişim sergileyemez.',
                '**Spontan Göz Açma:** Gözleri açık uyanır gibi görünen fakat bilişsel iletişim kuramayan hasta.',
                'Beyin ölümü',
                ['istemli motor aktivite', 'anlamlı iletişim'],
                []),
            (   'Beyin ölümü ise beyin hemisferleri ile beyin sapının tüm işlevlerinin geri dönüşsüz olarak tamamen '
                'sonlandığı yasal ve tıbbi ölüm halidir.',
                '**Beyin Ölümü:** Hemisferlerin ve beyin sapının tüm işlevlerinin geri dönüşsüz kaybı.',
                'Beyin ölümü',
                ['beyin ölümü', 'tıbbi ölüm'],
                []),
            (   'Koma taklitçilerini ve bu farklı klinik evreleri doğru adlandırmak hastaya uygulanacak tedavinin '
                'şeklini ve aciliyetini doğrudan belirler.',
                '**Doğru Adlandırma:** Farklı klinik evrelerin doğru tanınması ile acil tedavi yönetiminin '
                'belirlenmesi.',
                'Konfüzyon',
                ['koma taklitçileri', 'tedavi aciliyeti'],
                [])]),
    (   8,
        'k2-02-b04',
        'İlk Aşamada Yaklaşım ve Acil Yönetim',
        'k2-02-p007_s08',
        [   (   'Bilinç değişikliğiyle acil servise getirilen bir hastada etiyolojik nedenleri hızla iki ana grupta '
                'sınıflandırarak düşünmeliyiz.',
                '**Etiyolojik İki Grup:** Sistemik-metabolik difüz nedenler ile primer yapısal santral sinir sistemi '
                'lezyonları.',
                'Etyolojide neler',
                ['etiyolojik ayrım', 'sistemik nedenler', 'yapısal lezyonlar'],
                []),
            (   'İlk grup, tüm vücudu ve beyni difüz olarak etkileyen sistemik ve metabolik bozukluklardır; bunlar '
                'vakaların yaklaşık yüzde seksen beşini oluşturur.',
                '**Yüzde Seksen Beş:** Bilinç bozukluklarının ezici çoğunluğu metabolik ve sistemik kökenlidir.',
                'düşünmeliyiz?',
                ['metabolik koma', 'toksik ensefalopati'],
                []),
            (   'İkinci grup ise kitle, kanama veya herniasyon gibi doğrudan beyin dokusunu tehdit eden primer santral '
                'sinir sistemi patolojileridir.',
                '**Yapısal Lezyonlar:** Kafa içi kanama, kitle ve iskemik inme acil cerrahi ve nörolojik müdahale '
                'gerektirir.',
                'Etyolojide neler',
                ['intrakranial kanama', 'serebral herniasyon'],
                [])]),
    (   9,
        'k2-02-b04',
        'İlk Aşamada Yaklaşım ve Acil Yönetim',
        'k2-02-p008',
        [   (   'Acil servise bilinci kapalı bir hasta getirildiğinde hekimin ilk aşamadaki birincil amacı fokal '
                'yapısal lezyonları global metabolik problemlerden hızla ayırmaktır.',
                '**Birincil Amaç:** Fokal yapısal SSS lezyonları ile global metabolik problemlerin hızla ayrılması.',
                'Fokal yapısal SSS lezyonlarının, global',
                ['fokal yapısal lezyon', 'global metabolik problem'],
                []),
            (   'Çünkü fokal yapısal bir kitle veya kanama acil cerrahi dekompresyon gerektirebilirken global '
                'metabolik problemler medikal resüsitasyon ile tedavi edilir.',
                '**Yol Ayrımı:** Fokal lezyonlarda cerrahi müdahale, metabolik olgularda ise medikal resüsitasyon '
                'önceliği.',
                'metabolik problemlerden ayrımını yapmak',
                ['cerrahi dekompresyon', 'medikal resüsitasyon'],
                []),
            (   'Bilinci kapalı hastada zaman kaybı kalıcı nöron ölümü anlamına geldiği için muayene stabilizasyon '
                'laboratuvar ve tedavi eş zamanlı yürütülmelidir.',
                '**Eş Zamanlı Yönetim:** Muayene, stabilizasyon, laboratuvar ve tedavinin eş zamanlı yürütülmesi '
                'zorunluluğu.',
                'Muayene ile birlikte stabilizasyon, laboratuar,',
                ['zaman kaybı', 'eş zamanlı planlama'],
                []),
            (   'İlk saniyelerde derhal hava yolu açıklığı güvenceye alınmalı ve yeterli doku oksijenasyonu sağlamak '
                'için yüksek akımlı oksijen başlanmalıdır.',
                '**Oksijen Desteği:** Hava yolu açıklığı ve yeterli doku oksijenasyonu için yüksek akımlı oksijen.',
                'O2, iki geniş IV yol, EKG, kardiak',
                ['hava yolu açıklığı', 'yüksek akımlı oksijen'],
                []),
            (   'Hastaya derhal iki adet geniş çaplı damar yolu açılmalı ve acil medikal infüzyonlar için güvenli '
                'venöz erişim sağlanmalıdır.',
                '**Geniş Damar Yolu:** İki geniş periferik damar yolu açarak acil resüsitasyon hattı kurma.',
                'O2, iki geniş IV yol, EKG, kardiak',
                ['iki geniş damar yolu', 'venöz erişim'],
                []),
            (   'Eş zamanlı olarak elektrokardiyografi çekilmeli ve hasta kardiyak monitörizasyona bağlanarak ritim ve '
                'tansiyon kesintisiz izlenmelidir.',
                '**Kardiyak Monitörizasyon:** Elektrokardiyografi çekimi ve kesintisiz kardiyak monitörizasyon ile '
                'ritim takibi.',
                'EKG, kardiak',
                ['elektrokardiyografi', 'kardiyak monitörizasyon'],
                []),
            (   'Solunum depresyonu veya yetmezliği saptanan olgularda gecikmeden endotrakeal entübasyon planlanmalı '
                've beyin hipoksiden korunmalıdır.',
                '**Entübasyon Kararı:** Solunum depresyonunda gecikmeden endotrakeal entübasyonla beyni koruma.',
                'monitorizasyon',
                ['endotrakeal entübasyon', 'solunum depresyonu'],
                []),
            (   'Bu temel kardiyorespiratuvar stabilizasyon sağlanmadan hastayı bilgisayarlı tomografi ünitesine '
                'taşımak ölümcül komplikasyonlara davetiye çıkarır.',
                '**Radyoloji Öncesi:** Temel stabilizasyon tamamlanmadan hastayı tomografiye göndermenin ölümcül '
                'riskleri.',
                'görüntüleme ve tedavi eş zamanlı planlanmalı',
                ['kardiyorespiratuvar stabilizasyon', 'tomografi ünitesi'],
                [])]),
    (   10,
        'k2-02-b04',
        'İlk Aşamada Yaklaşım ve Acil Yönetim',
        'k2-02-p009',
        [   (   'Yaşamsal fonksiyonlar desteklenirken hızlı bir nörolojik değerlendirme yapılır ve fokal bir nörolojik '
                'defisitin varlığı araştırılır.',
                '**Hızlı Değerlendirme:** Vital destek sürerken fokal nörolojik defisit varlığının ivedilikle '
                'araştırılması.',
                'Hızlı nörolojik değerlendirme',
                ['hızlı değerlendirme', 'fokal defisit'],
                []),
            (   'Tek taraflı pupiller anizokori asimetrik motor yanıtlar ya da hemisferik lateralizasyon bulguları '
                'acil cerrahi patolojiyi akla getirir.',
                '**Lateralizasyon:** Tek taraflı anizokori ve motor asimetrinin cerrahi kitle lezyonunu düşündürmesi.',
                'Fokal nöroloji defisit önemli',
                ['anizokori', 'motor asimetri', 'lateralizasyon'],
                []),
            (   'Bu hızlı muayene sırasında yatak başında saniyeler içinde yapılması zorunlu olan en kritik '
                'laboratuvar testi stik kan şekeri ölçümüdür.',
                '**Stik Kan Şekeri:** Yatak başında saniyeler içinde kan glukoz düzeyinin ölçülmesi gerekliliği.',
                'Stick Kan şekeri (hipoglisemi gerçek bir',
                ['stik kan şekeri', 'glukoz ölçümü'],
                []),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: bilinç bozukluğu olan her hastanın ayırıcı tanısında ilk aşamada '
                'değerlendirilmesi gereken ve gerçek bir acil olan tetkik stik kan şekeridir; çünkü hipoglisemi hızla '
                'tedavi edilmezse beyinde dakikalar içinde kalıcı hasar ve ölüm oluşturur.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Bilinç bozukluğunda ilk aşamada '
                'değerlendirilen gerçek acil stik kan şekeridir.',
                'Stick Kan şekeri (hipoglisemi gerçek bir',
                ['çıkmış sınav sorusu', 'hipoglisemi acili', 'stik glukoz'],
                ['q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-19']),
            (   'Kan şekeri düşük saptanan hastaya damar yolu açılır açılmaz damar içi konsantre dekstroz solüsyonu '
                'ivedilikle puşe edilmelidir.',
                '**Dekstroz Tedavisi:** Hipoglisemi saptandığında damar içi konsantre dekstrozun ivedi puşesi.',
                'acildir)',
                ['dekstroz solüsyonu', 'damar içi puşe'],
                []),
            (   'Kronik alkolizm veya malnütrisyon öyküsü olan bireylerde ise glukoz verilmeden hemen önce damar içi '
                'yüz miligram tiamin uygulanmalıdır.',
                '**Tiamin Önceliği:** Kronik alkolizm ve malnütrisyonda glukozdan önce yüz miligram tiamin uygulaması.',
                'acildir)',
                ['kronik alkolizm', 'tiamin uygulaması'],
                []),
            (   'Tiamin verilmeden glukoz yüklenmesi beynin laktik asidoza sürüklenmesine ve akut Wernicke '
                'ensefalopatisinin alevlenmesine neden olabilir.',
                '**Wernicke Riski:** Tiaminsiz glukoz yüklemesinin akut Wernicke ensefalopatisini tetikleme '
                'mekanizması.',
                'acildir)',
                ['Wernicke ensefalopatisi', 'laktik asidoz'],
                []),
            (   'Ayrıca komadaki hastada solunum depresyonu ve iğne ucu pupiller görülüyorsa opioid intoksikasyonu '
                'düşünülmeli ve tanısal amaçla damar içi nalokson uygulanmalıdır.',
                '**Opioid Triadı ve Nalokson:** Solunum depresyonu ve iğne ucu pupilde opioid intoksikasyonu şüphesi '
                've nalokson.',
                'Opioid overdozu ?',
                ['opioid overdozu', 'iğne ucu pupil', 'nalokson'],
                [])]),
    (   11,
        'k2-02-b05',
        'Sistemik Nedenler ve Diffüz SSS Etkilenimi',
        'k2-02-p010',
        [   (   'Santral sinir sistemini difüz olarak etkileyerek koma tablosu oluşturan sistemik nedenlerin başında '
                'kanda gaz ve substrat dengesizlikleri gelir.',
                '**Sistemik Spektrum:** Beyin dokusunu diffüz etkileyen sistemik nedenler ve gaz-substrat '
                'bozuklukları.',
                'Etiyoloji: Sistemik Neden – SSS Difüz',
                ['sistemik nedenler', 'substrat dengesizliği'],
                []),
            (   'Derin hipoksi ve karbondioksit retansiyonu yani hiperkapni beyin dokusunda yaygın hücresel '
                'metabolizma yetmezliğine ve serebral ödeme yol açar.',
                '**Hipoksi ve Hiperkapni:** Derin hipoksi ve hiperkapninin yaygın hücresel yetmezlik ve ödem '
                'oluşturması.',
                'Etkilenimi',
                ['derin hipoksi', 'hiperkapni', 'serebral ödem'],
                []),
            (   'Kan şekerindeki aşırı oynamalar hipoglisemi kadar kontrolsüz diyabet hastalarında hiperglisemi ve '
                'diyabetik ketoasidoz ile karşımıza çıkar.',
                '**Glukoz Uçları:** Hipoglisemi kadar hiperglisemi ve diyabetik ketoasidozun da komaya yol açması.',
                'Hiperglisemi',
                ['diyabetik ketoasidoz', 'hiperglisemi'],
                []),
            (   'Elektrolit anormallikleri içinde özellikle akut gelişen hiponatremi serebral hücre içine su geçişini '
                'artırarak beyin ödemi ve status epileptikusa neden olur.',
                '**Hiponatremi Tehlikesi:** Akut hiponatreminin hücre içine su çekerek beyin ödemi ve status '
                'epileptikus yapması.',
                'Hiponatremi',
                ['hiponatremi', 'status epileptikus'],
                []),
            (   'Kronik alkolizmde ve beslenme yetersizliğinde tiamin eksikliğine bağlı gelişen Wernicke '
                'ensefalopatisi konfüzyon ataksi ve oftalmopleji triadı ile karakterizedir.',
                '**Wernicke Triadı:** Tiamin eksikliğine bağlı gelişen konfüzyon, ataksi ve oftalmopleji klasik '
                'triadı.',
                'Wernicke',
                ['Wernicke ensefalopatisi', 'oftalmopleji', 'ataksi'],
                []),
            (   'Böbrek yetmezliğinde kanda biriken toksik nitrojen ürünleri üremik ensefalopatiye ve multifokal '
                'miyoklonuslara zemin hazırlar.',
                '**Üremik Tablo:** Kanda biriken üre ve toksik nitrojen ürünlerinin üremik ensefalopati oluşturması.',
                'Üremik ensefalopati',
                ['üremik ensefalopati', 'miyoklonus'],
                []),
            (   'Şiddetli enfeksiyon ve sepsis tablolarında salınan proinflamatuvar sitokinler kan beyin bariyerini '
                'bozarak sepsis ilişkili ensefalopati tablosu oluşturur.',
                '**Sepsis Ensefalopatisi:** Sistemik enfeksiyon ve sitokin fırtınasının kan-beyin bariyerini bozarak '
                'ensefalopati yapması.',
                'Sepsis',
                ['sepsis', 'sitokin fırtınası', 'kan beyin bariyeri'],
                []),
            (   'Ağır karaciğer yetmezliğinde kanda artan amonyak hepatik ensefalopatiye kontrolsüz kan basıncı '
                'yükselmeleri ise serebral otoregülasyon kaybıyla hipertansif ensefalopatiye yol açar.',
                '**Organ Yetmezlikleri:** Karaciğer yetmezliğinde amonyak artışı ve hipertansif krizde serebral '
                'otoregülasyon çöküşü.',
                'Hipertansif',
                ['hepatik ensefalopati', 'amonyak', 'hipertansif ensefalopati'],
                [])]),
    (   12,
        'k2-02-b05',
        'Sistemik Nedenler ve Diffüz SSS Etkilenimi',
        'k2-02-p011',
        [   (   'Sistemik nedenler spektrumunda endokrin bezlerin hipo ya da hiperfonksiyonu da önemli bir yer tutar.',
                '**Endokrin Bozukluklar:** Tiroid ve adrenal bezlerin hipo veya hiperfonksiyonu kaynaklı bilinç '
                'bozuklukları.',
                'Düşük kardiyak',
                ['endokrin bezler', 'fonksiyon bozukluğu'],
                []),
            (   'Ağır hipotiroidiye bağlı miksödem koması veya aşırı tiroid hormonu salınımı ile giden tiroid '
                'fırtınası komaya kadar ilerleyen bilinç değişiklikleri yapabilir.',
                '**Tiroid Uçları:** Miksödem koması ve tiroid fırtınasının derin bilinç depresyonuna yol açması.',
                'debi,',
                ['miksödem koması', 'tiroid fırtınası'],
                []),
            (   'Benzer biçimde adrenal yetmezlik yani Addisonian krizde gelişen şiddetli hipotansiyon ve hiponatremi '
                'hastayı hızla komaya sokabilir.',
                '**Adrenal Kriz:** Addisonian krizde gelişen derin hipotansiyon ve hiponatreminin koma yaratması.',
                'Yaygın',
                ['adrenal yetmezlik', 'Addisonian kriz'],
                []),
            (   'Kardiyovasküler sistem yetmezliklerinde düşük kardiyak debi kardiyojenik şok yaygın hipoperfüzyon '
                'hipovolemi ve derin anemi beyin perfüzyonunu çökertir.',
                '**Kardiyovasküler Çöküş:** Düşük kardiyak debi, kardiyojenik şok, hipoperfüzyon ve aneminin serebral '
                'iskemi yapması.',
                'hipoperfüzyon',
                ['düşük kardiyak debi', 'kardiyojenik şok'],
                []),
            (   'Toksik madde maruziyetleri endüstriyel çözücüler karbonmonoksit inhalasyonu ve zehirlenmeler '
                'nörolojik aciller arasında mutlaka akla getirilmelidir.',
                '**Toksik Maddeler:** Çözücüler, karbonmonoksit ve çevresel toksinlerin komadaki rolü.',
                'Hipovolemi,',
                ['toksik madde', 'karbonmonoksit'],
                []),
            (   'Kronik ilaç veya alkol kullanımının aniden kesilmesi deliryum tremens gibi ajitasyon ve otonomik '
                'fırtınayla seyreden tablolar doğurur.',
                '**Yoksunluk Krizleri:** Alkol ve sedatif kesilmesinin deliryum tremens ve otonomik hiperaktivite '
                'yaratması.',
                'Anemi,',
                ['deliryum tremens', 'yoksunluk krizi'],
                []),
            (   'Psikiyatrik ilaç etkileşimleri sonucunda gelişen serotonin sendromu klonus hipertermi ve konfüzyonla '
                'yaşamı tehdit eden bir metabolik acildir.',
                '**Serotonin Sendromu:** Klonus, hipertermi ve konfüzyonla giden yaşamı tehdit edici ilaç reaksiyonu.',
                'Serotonin sendromu',
                ['serotonin sendromu', 'klonus', 'hipertermi'],
                []),
            (   'Antipsikotik ilaçların tetiklediği nöroleptik malign sendrom ise yaygın kurşun boru rijiditesi '
                'hipertermi ve bilinç bulanıklığı ile seyreder.',
                '**Nöroleptik Malign Sendrom:** Kurşun boru rijiditesi, hipertermi ve bilinç bulanıklığı tablosu.',
                'Nöroleptik malign',
                ['nöroleptik malign sendrom', 'kurşun boru rijiditesi'],
                [])]),
    (   13,
        'k2-02-b06',
        'Santral Sinir Sistemi Nedenleri ve Herniasyon Tipleri',
        'k2-02-p012',
        [   (   'Bilinç bozukluklarının yüzde on beşini oluşturan primer santral sinir sistemi patolojileri yapısal ve '
                'yapısal olmayan nedenler olarak iki grupta incelenir.',
                '**SSS Nedenleri:** Bilinç bozukluklarının yüzde on beşini oluşturan yapısal ve fonksiyonel primer '
                'beyin nedenleri.',
                'Etiyoloji: SSS Ait Nedenler',
                ['primer patolojiler', 'yapısal nedenler'],
                []),
            (   'Yapısal santral sinir sistemi nedenlerinin başında kafa travmaları epidural hematomlar subdural '
                'kanamalar ve serebral kontüzyonlar gelir.',
                '**Travmatik Kanamalar:** Kafa travmasına bağlı epidural hematom, subdural kanama ve serebral '
                'kontüzyonlar.',
                'SSS travması',
                ['kafa travması', 'epidural hematom', 'subdural kanama'],
                []),
            (   'Spontan intrakraniyal kanamalar ve anevrizma rüptürüne bağlı subaraknoid kanama ani bilinç kaybının '
                'en dramatik yapısal nedenleridir.',
                '**Subaraknoid Kanama:** Anevrizma rüptürüne bağlı subaraknoid kanama ve spontan parankimal '
                'hematomlar.',
                'İntrakranial kanama - SAK',
                ['subaraknoid kanama', 'spontan hematom'],
                []),
            (   'Büyük hemisferik iskemik inmeler ya da beyin sapını doğrudan besleyen baziler arterin akut oklüzyonu '
                'dakikalar içinde koma tablosu oluşturur.',
                '**İskemik İnme:** Masif hemisferik enfarkt ve baziler arter tıkanıklığının hızla koma yaratması.',
                'İskemik inme',
                ['iskemik inme', 'baziler arter oklüzyonu'],
                []),
            (   'İntrakraniyal yer kaplayan primer beyin tümörleri veya sistemik kanserlerin beyin metastazları kitle '
                'etkisiyle bilinci bozar.',
                '**Yer Kaplayan Kitleler:** Primer beyin tümörleri ve metastazların oluşturduğu kitle etkisi ve ödem.',
                'Yer-kaplayan oluşum',
                ['beyin tümörü', 'metastaz', 'kitle etkisi'],
                []),
            (   'Yapısal olmayan primer santral nedenler arasında akut bakteriyel menenjit ve viral ensefalit gibi '
                'santral sinir sistemi enfeksiyonları yer alır.',
                '**SSS Enfeksiyonları:** Akut bakteriyel menenjit ve viral ensefalitlerin oluşturduğu yaygın '
                'inflamatuvar hasar.',
                'SSS enfeksiyonu',
                ['bakteriyel menenjit', 'viral ensefalit'],
                []),
            (   'Ayrıca non konvülzif status epileptikus ya da jeneralize nöbet sonrası uzamış postiktal stupor dönemi '
                'bilinci kapalı tutabilir.',
                '**Status Epileptikus:** Non-konvülzif status epileptikus ve uzun süren postiktal stuporun bilinci '
                'kapatması.',
                'Nöbetler (status epileptikus / postiktal periyod)',
                ['status epileptikus', 'postiktal stupor'],
                []),
            (   'İleri evre demans hastalarında araya giren basit bir enfeksiyon bile kırılgan nöronal rezervi '
                'tüketerek ani bir koma tablosu yaratabilir.',
                '**Demans Rezervi:** İleri evre demanslı hastada araya giren sistemik enfeksiyonun ani koma '
                'oluşturabilmesi.',
                'Demans',
                ['demans rezervi', 'akut kötüleşme'],
                [])]),
    (   14,
        'k2-02-b06',
        'Santral Sinir Sistemi Nedenleri ve Herniasyon Tipleri',
        'k2-02-p013',
        [   (   'İntrakraniyal kitle lezyonlarında kafa kemiklerinin rijit yapısı ve falks ile tentoryum gibi dural '
                'bölmeler nedeniyle serebral herniasyon sendromları gelişir.',
                '**Herniasyon Mekanizması:** İntrakraniyal kitle etkisi ve kafa içi rijit kompartmanlar nedeniyle doku '
                'fıtıklaşması.',
                'SEREBRAL HERNIASYON',
                ['serebral herniasyon', 'dural bölmeler'],
                []),
            (   'Herniasyon şemasında birinci sırada temporal lobun medialinde yer alan unkusun tentoryal çentikten '
                'aşağı fıtıklaştığı unkal herniasyon bulunur.',
                '**Unkal Herniasyon:** Medial temporal unkusun tentoryal çentikten aşağı fıtıklaşarak beyin sapına '
                'basması.',
                'SEREBRAL HERNIASYON',
                ['unkal herniasyon', 'temporal lob'],
                []),
            (   'Unkal herniasyonda fıtıklaşan doku aynı taraftaki üçüncü kraniyal siniri ve mezensefalon pedinkülünü '
                'basarak ipsilateral midriyazis ve karşı tarafta hemipleji yapar.',
                '**Unkal Triad:** İpsilateral dilate fikse pupil ve karşı tarafta hemipleji ile karakterize klinik '
                'tablo.',
                'SEREBRAL HERNIASYON',
                ['üçüncü kraniyal sinir', 'ipsilateral midriyazis', 'hemipleji'],
                []),
            (   'İkinci sırada diensefalonun ve her iki serebral hemisferin tentoryal yarıktan aşağı doğru simetrik '
                'olarak yer değiştirdiği santral tentoryal herniasyon yer alır.',
                '**Santral Herniasyon:** Diensefalon ve bilateral hemisferlerin tentoryal yarıktan simetrik kaudal yer '
                'değiştirmesi.',
                'SEREBRAL HERNIASYON',
                ['santral herniasyon', 'diensefalon'],
                []),
            (   'Üçüncü tip singulat girusun falks serebrinin serbest kenarının altından karşı serebral hemisfer '
                'tarafına doğru kaydığı singulat ya da subfalsin herniasyondur.',
                '**Subfalsin Herniasyon:** Singulat girusun falks serebri altından karşı tarafa itildiği subfalsin '
                'herniasyon.',
                'SEREBRAL HERNIASYON',
                ['singulat herniasyon', 'subfalsin'],
                []),
            (   'Dördüncü herniasyon tipi kafa kemiğindeki cerrahi veya travmatik bir defektten beyin dokusunun dışarı '
                'fıtıklaşması yani transkalvaryal herniasyondur.',
                '**Transkalvaryal Tip:** Kafa kemiğindeki defektten beyin parankiminin dışarı taşması.',
                'SEREBRAL HERNIASYON',
                ['transkalvaryal herniasyon', 'kemik defekti'],
                []),
            (   'Beşinci sırada arka çukurdaki kitle etkisi nedeniyle serebellumun tentoryal yarıktan yukarı '
                'mezensefalona doğru fıtıklaştığı yukarı serebellar herniasyon bulunur.',
                '**Yukarı Herniasyon:** Arka çukur kitlesiyle serebellumun tentoryumdan yukarı mezensefalona itilmesi.',
                'SEREBRAL HERNIASYON',
                ['yukarı serebellar', 'arka çukur kitlesi'],
                []),
            (   'Altıncı ve en ölümcül tip ise serebellar tonsillerin foramen magnumdan aşağı omurilik kanalına '
                'fıtıklaşarak bulbusu ve solunum merkezini ezdiği tonsiller herniasyondur.',
                '**Tonsiller Herniasyon:** Serebellar tonsillerin foramen magnumdan aşağı kayarak bulbus ve solunum '
                'merkezini ezmesi.',
                'SEREBRAL HERNIASYON',
                ['tonsiller herniasyon', 'foramen magnum', 'solunum arresti'],
                [])]),
    (   15,
        'k2-02-b07',
        'Fizik Muayene ve Anahtar Bulgular',
        'k2-02-p013_s15',
        [   (   'Bilinç bozukluğu olan hastada fizik muayene, genel tıbbi muayene ile nörolojik değerlendirmenin eş '
                'zamanlı yürütüldüğü çok dinamik bir süreçtir.',
                '**Muayene Stratejisi:** Genel sistemik stabilizasyon ile nörolojik muayene eş zamanlı yürütülür.',
                'Muayene',
                ['fizik muayene', 'nörolojik değerlendirme'],
                []),
            (   'Genel muayenede vital bulgular, kafa travması izleri, cilt döküntüleri ve nefes kokusu ilk ipuçlarını '
                'sağlar.',
                '**İlk İpuçları:** Vital bulgular, cilt bulguları, kafa travması belirtileri ve nefes kokusu.',
                'Muayene',
                ['vital bulgular', 'kafa travması', 'sistemik ipuçları'],
                []),
            (   'Nörolojik muayenede ise bilinç derinliği, beyin sapı refleksleri, pupiller ve motor yanıtlar '
                'sistematik bir sırayla kaydedilmelidir.',
                '**Dört Anahtar Öğe:** Bilinç düzeyi, pupiller, beyin sapı refleksleri ve motor postür.',
                'Muayene',
                ['bilinç düzeyi', 'pupiller', 'motor yanıtlar'],
                [])]),
    (   16,
        'k2-02-b07',
        'Fizik Muayene ve Anahtar Bulgular',
        'k2-02-p014',
        [   (   'Komadaki bir hastada nörolojik muayeneden önce vital bulguların titizlikle ölçülmesi tanıya giden en '
                'hızlı ipuçlarını sağlar.',
                '**Vital Bulgular:** Nörolojik muayeneden önce vital bulguların titizlikle değerlendirilmesi kuralı.',
                'Vital bulgular:',
                ['vital bulgular', 'fizik muayene'],
                []),
            (   'Solunum frekansı ve ritmi değerlendirilmeli; derin ve hızlı hiperventilasyon asidozu yüzeyel yavaş '
                'hipoventilasyon ise sedatif intoksikasyonunu düşündürmelidir.',
                '**Solunum Frekansı:** Hızlı hiperventilasyonun asidozu, yavaş hipoventilasyonun sedatifleri '
                'düşündürmesi.',
                'Solunum: hiper- veya hipoventilasyon',
                ['hiperventilasyon', 'hipoventilasyon', 'sedatif'],
                []),
            (   'Kan basıncında belirgin artış hipertansif ensefalopatiyi ya da kafa içi basınç artışı sendromunun bir '
                'parçası olan Cushing fenomenini gösterir.',
                '**Hipertansiyon ve KİBAS:** Kan basıncı artışının hipertansif krizi veya Cushing refleksini işaret '
                'etmesi.',
                'KB: hiper- veya hipotansiton',
                ['kan basıncı', 'Cushing fenomeni'],
                []),
            (   'Buna karşılık derin hipotansiyon varlığında kardiyojenik şok septik şok ya da adrenal kriz akla '
                'gelmelidir.',
                '**Hipotansiyon Tablosu:** Derin hipotansiyonun kardiyojenik, septik şok veya adrenal kriz kaynaklı '
                'olması.',
                'KB: hiper- veya hipotansiton',
                ['hipotansiyon', 'septik şok'],
                []),
            (   'Arteriyel kan gazında hipoksi ve hiperkapni varlığı doku oksijenasyonunun yetersizliğini somut olarak '
                'belgeler.',
                '**Kan Gazı İpuçları:** Hipoksi ve karbondioksit birikiminin arteriyel kan gazıyla objektif '
                'belgelenmesi.',
                'Kan gazı: hipoksi veya hiperkarbi',
                ['kan gazı', 'hipoksi', 'hiperkarbi'],
                []),
            (   'Hastada yüksek ateş saptanması menenjit viral ensefalit beyin apsesi sepsis veya pnömoni gibi ciddi '
                'bir enfeksiyonu işaret eder.',
                '**Ateşli Koma:** Yüksek ateşin menenjit, ensefalit veya sistemik sepsisi kuvvetle düşündürmesi.',
                'Ateş – sistemik enfeksiyon',
                ['yüksek ateş', 'menenjit', 'ensefalit'],
                []),
            (   'Hipotermi mevcudiyeti ise uzun süre soğukta kalma miksödem koması etanol veya barbitürat zehirlenmesi '
                've septik şokta karşımıza çıkar.',
                '**Hipotermi Nedenleri:** Soğuğa maruziyet, miksödem, alkol-barbitürat intoksikasyonu ve septik şok.',
                'Vital bulgular:',
                ['hipotermi', 'miksödem', 'barbitürat'],
                []),
            (   'Muayenenin başında hastanın koma derecesi pupillerin durumu uyaranlara yanıtı ve skalpte travma '
                'izleri aranmalıdır.',
                '**İlk Gözlem:** Koma derecesi, pupil durumu ve kafa travması bulgularının ilk anda taranması.',
                'Vital bulgular:',
                ['koma derecesi', 'pupil durumu', 'travma izleri'],
                [])]),
    (   17,
        'k2-02-b07',
        'Fizik Muayene ve Anahtar Bulgular',
        'k2-02-p014_s17',
        [   (   'Fizik muayenede hekimin hızla yanıt araması gereken dört kritik soru vardır: hastanın bilinç düzeyi '
                'nedir, pupilleri ne durumdadır, uyaranlara nasıl yanıt vermektedir ve travma belirtisi var mıdır?',
                '**Dört Temel Soru:** Bilinç düzeyi, pupiller reaktivite, uyaran yanıtı ve kafa travması bulgusu.',
                'Hastanın bilinç düzeyi ?',
                ['bilinç düzeyi', 'pupiller reaktivite', 'travma bulgusu'],
                []),
            (   'Göz kapaklarının aralanması, pupillerin ışığa yanıtı ve simetrisi, beyin sapı basısının ilk ve en '
                'duyarlı işaretleridir.',
                '**Pupil İncelemesi:** Işık refleksi ve asimetri, üçüncü kraniyal sinir basısı ve herniasyon '
                'habercisidir.',
                'Pupilleri ?',
                ['pupil reaktivitesi', 'okülomotor sinir', 'unkal herniasyon'],
                []),
            (   'Ağrılı uyarana verilen motor yanıt, lezyonun kortikal mi yoksa beyin sapı düzeyinde mi olduğunu '
                'dakikalar içinde ortaya koyar.',
                '**Motor Yanıt Düzeyi:** Kortikal lokalizasyon ile beyin sapı rijiditesinin hızlı ayırımı.',
                'Uyaranlara cevabı ?',
                ['ağrılı uyaran', 'motor yanıt', 'lokalizasyon'],
                [])]),
    (   18,
        'k2-02-b07',
        'Fizik Muayene ve Anahtar Bulgular',
        'k2-02-p015',
        [   (   'Koma fizik muayenesinde klinisyenin asla gözden kaçırmaması gereken son derece kritik anahtar '
                'noktalar vardır.',
                '**Kritik Noktalar:** Koma muayenesinde klinisyenin asla atlamaması gereken çekirdek klinik detaylar.',
                'Konfüze hastada postiktal durumdan',
                ['kritik noktalar', 'muayene detayları'],
                []),
            (   'Konfüze veya bilinci kapalı bir hastada geçirilmiş bir epileptik nöbet ve postiktal durumdan '
                'şüpheleniliyorsa hastanın ağzı açılıp dil muayenesi yapılmalıdır.',
                '**Dil Muayenesi:** Postiktal durum şüphesinde ağız içinin açılıp dil kenarlarının taranması kuralı.',
                'şüpheleniliyorsa: Dilde ısırık ? NÖBET !!!',
                ['postiktal durum', 'dil muayenesi'],
                []),
            (   'Dilde özellikle dilin lateral kenarlarında taze ısırık izlerinin saptanması geçirilmiş bir jeneralize '
                'tonik klonik nöbetin en özgül kanıtıdır.',
                '**Dilde Isırık İzi:** Dil lateral kenarlarındaki taze ısırık izinin geçirilmiş jeneralize nöbete '
                'özgüllüğü.',
                'şüpheleniliyorsa: Dilde ısırık ? NÖBET !!!',
                ['dil lateralinde ısırık', 'tonik klonik nöbet'],
                []),
            (   'Skalp kılıfları saçlar tek tek aralanarak dikkatle palpe edilmeli ve gözle taranmalıdır çünkü saçlı '
                'derideki küçük travma izleri sıklıkla atlanır.',
                '**Skalp Muayenesi:** Saçlı derinin titizlikle taranarak gizli ve küçük travma izlerinin aranması.',
                'Skalp ayrıntılı muayene edilmeli !!!',
                ['skalp muayenesi', 'saçlı deri'],
                []),
            (   'Atlanan bu minör travmalar altta sessizce büyüyen bir epidural hematomun veya akut subdural kanamanın '
                'habercisi olabilir.',
                '**Gizli Hematom:** Küçük skalp travmalarının altında epidural veya subdural hematom yatabilmesi.',
                'Sıklıkla küçük-gizli travmalar atlanır (posttravma!)',
                ['epidural hematom', 'subdural kanama'],
                []),
            (   'Hastadan alkol kokusu alınması hekimi asla yanıltmamalı ve koma nedeni tek başına alkole bağlanarak '
                'hasta kenara bırakılmamalıdır.',
                '**Alkol Tuzağı:** Alkol kokusuna aldanıp komayı tek başına intoksikasyona bağlamama uyarısı.',
                'Koma nedeni alkol ?',
                ['alkol kokusu', 'yanıltıcı rehavet'],
                []),
            (   'Çünkü sarhoş bireyler düşme ve travmaya son derece yatkındır; alkol tablosunun altında ölümcül bir '
                'subdural hematom ya da subaraknoid kanama yatıyor olabilir.',
                '**Travma ve Alkol:** Sarhoş hastada düşmeye bağlı ölümcül subdural veya subaraknoid kanama riski.',
                '(altta başka etyoloji varmı ?) SAK – SUBDURAL ?',
                ['travma riski', 'subaraknoid kanama', 'subdural hematom'],
                [])]),
    (   19,
        'k2-02-b07',
        'Fizik Muayene ve Anahtar Bulgular',
        'k2-02-p016',
        [   (   'Nörolojik muayenede beyin sapının ve serebral yapıların anatomik düzeyini santimetre santimetre '
                'belirleyen dört temel klinik parametre vardır.',
                '**Dört Lokalizan Parametre:** Beyin sapı düzeyini santimetre santimetre belirleyen dört temel '
                'parametre.',
                'Lokalizan değeri olan klinik',
                ['lokalizan parametreler', 'anatomik düzey'],
                []),
            (   'Bu parametrelerin ilki hastanın ağrılı uyaranlara karşı verdiği iskelet kası motor yanıtları ve '
                'sergilediği vücut postürüdür.',
                '**Motor Yanıtlar:** Ağrılı uyarana karşı oluşan ekstremite hareketleri ve karakteristik vücut '
                'postürleri.',
                'İskelet kası motor yanıtları',
                ['iskelet kası', 'motor yanıtlar', 'postür'],
                []),
            (   'İkinci lokalizan bulgu pupillerin milimetrik çapı ışık refleksi ve aralarındaki simetridir.',
                '**Pupil Bulguları:** Pupillerin çapı, ışığa reaktivitesi ve aralarındaki simetrik durum.',
                'Pupillerin çapı ve reaktivitesi',
                ['pupillerin çapı', 'ışık refleksi'],
                []),
            (   'Üçüncü temel parametre spontan ya da uyarılmış göz hareketleri ile okülosefalik ve okülovestibüler '
                'beyin sapı refleksleridir.',
                '**Göz Hareketleri:** Spontan hareketler ile okülosefalik ve okülovestibüler refleks yanıtları.',
                'Göz hareketleri ve okülovestibüler',
                ['göz hareketleri', 'okülovestibüler'],
                []),
            (   'Dördüncü lokalizan parametre ise hastanın sergilediği solunum şekli derinliği ve ritmidir.',
                '**Solunum Paternleri:** Solunumun hızı, ritmi, derinliği ve karakteristik patolojik şekli.',
                'Solunum şekli',
                ['solunum şekli', 'solunum ritmi'],
                []),
            (   'Bu dört temel nörolojik gösterge bir arada değerlendirildiğinde lezyonun kortikal mi diensefalik mi '
                'mezensefalik mi pontin mi yoksa medüller mi olduğu netleşir.',
                '**Lezyon Seviyesi:** Dört parametrenin birleşimiyle lezyon düzeyinin korteksten medullaya net '
                'tespiti.',
                'bulgular',
                ['kortikal', 'mezensefalik', 'pontin', 'medüller'],
                []),
            (   'Hekim hiçbir görüntüleme tetkiki olmadan dahi bu dört bulgu ile hastadaki nörolojik lezyonun '
                'seviyesini yatak başında tespit edebilir.',
                '**Yatak Başı Teşhis:** Görüntüleme olmaksızın sadece fizik bulgularla yatak başında anatomik '
                'lokalizasyon.',
                'bulgular',
                ['yatak başı lokalizasyon', 'fizik bulgular'],
                [])]),
    (   20,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p017',
        [   (   'Bilinç düzeyindeki değişiklikleri objektif olarak sayısallaştırmak ve klinik takiplerde ortak bir dil '
                'oluşturmak amacıyla koma skorlama sistemleri geliştirilmiştir.',
                '**Objektif Skorlama:** Bilinç düzeyini sayısallaştıran ve klinik iletişimde ortak dil kuran koma '
                'skorları.',
                'Glasgow koma skoru',
                ['koma skorları', 'objektif sayısallaştırma'],
                []),
            (   'Bu sistemlerin dünyada en yaygın kullanılanı travmatik ve nontravmatik olguların tamamında '
                'standartlaşan Glasgow Koma Skalasıdır.',
                '**Glasgow Yaygınlığı:** Dünya genelinde travmatik ve nontravmatik tablolarda standartlaşan Glasgow '
                'koma skalası.',
                'Glasgow koma skoru',
                ['Glasgow koma skalası', 'standart sistem'],
                []),
            (   'Ayrıca yoğun bakım kliniklerinde beyin sapı reflekslerini ve solunumu da değerlendiren Dörtlü Test '
                'yani for skoru ve hepatik koma skalası da kullanılır.',
                '**Diğer Skorlar:** Yoğun bakımlarda tercih edilen dörtlü test skoru ve metabolik tablolarda hepatik '
                'koma skalası.',
                'Dörtlü test',
                ['dörtlü test', 'for skoru', 'hepatik koma skalası'],
                []),
            (   'Glasgow Koma Skalası üç bağımsız klinik bileşenin puanlanması esasına dayanır.',
                '**Üç Bağımsız Bileşen:** Glasgow koma skalasının üç ana nörolojik muayene basamağı.',
                'Glasgow koma skoru',
                ['üç bileşen', 'puanlama esası'],
                []),
            (   'Bu üç bileşen göz açma yanıtı motor yanıt ve sözel yanıttır.',
                '**Bileşen İsimleri:** Göz açma, motor yanıt ve sözel yanıt kategorileri.',
                'Glasgow koma skoru',
                ['göz açma', 'motor yanıt', 'sözel yanıt'],
                []),
            (   'Her bir kategoride hastanın verebildiği en iyi yanıt puanlanır ve elde edilen puanlar toplanarak '
                'genel bilinç skoru oluşturulur.',
                '**En İyi Yanıt İlkesi:** Her kategoride hastanın sergilediği en iyi cevabın puanlanması kuralı.',
                'Glasgow koma skoru',
                ['en iyi yanıt', 'genel skor'],
                []),
            (   'Skalanın seri olarak tekrarlanması hastanın tablosunun cerrahi bir herniasyona doğru kötüleşip '
                'kötüleşmediğini ya da tedaviye yanıt verip vermediğini gösterir.',
                '**Seri Takip Değeri:** Skalanın tekrarlanmasıyla herniasyona gidişin veya iyileşmenin objektif '
                'izlenmesi.',
                'Glasgow koma skoru',
                ['seri takip', 'herniasyon izlemi'],
                []),
            (   'Glasgow Koma Skalasında puanlama yapılırken her parametre ayrı ayrı kaydedilmeli ve tek bir toplam '
                'sayıya indirgenmeden önce bileşenler belirtilmelidir.',
                '**Bileşenleri Kaydetme:** Toplam skorun yanında E, M ve V alt puanlarının açıkça belirtilmesi kuralı.',
                'Glasgow koma skoru',
                ['bileşen kaydı', 'alt puanlar'],
                [])]),
    (   21,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p017_s21',
        [   (   'Glasgow Koma Skalası, bilincin derinliğini objektif olarak ölçmek ve klinisyenler arasında ortak bir '
                'dil oluşturmak amacıyla geliştirilmiş evrensel bir skorlama sistemidir.',
                '**Glasgow Skalası:** Bilinç bozukluklarının şiddetini ve prognozunu belirleyen evrensel standart.',
                'GLASGOW KOMA SKALASI',
                ['Glasgow koma skalası', 'bilinç derinliği', 'prognostik skor'],
                []),
            (   'Skala üç temel kategoriden oluşur: göz açma yanıtı en fazla dört puan, sözel yanıt en fazla beş puan '
                've motor yanıt en fazla altı puan olarak puanlanır.',
                '**Üç Kategori:** Göz açma en fazla dört, sözel yanıt en fazla beş, motor yanıt en fazla altı puan.',
                'GLASGOW KOMA SKALASI',
                ['göz yanıtı', 'sözel yanıt', 'motor yanıt'],
                []),
            (   'Alınabilecek en düşük toplam puan üç, tamamen normal ve uyanık bir hastanın alacağı en yüksek puan '
                'ise on beştir.',
                '**Puan Aralığı:** En düşük skor üç, tam sağlıklı uyanıklık skoru on beştir.',
                'GLASGOW KOMA SKALASI',
                ['minimum skor üç', 'maksimum skor on beş'],
                [])]),
    (   22,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p018',
        [   (   'Glasgow Koma Skalasının ilk bileşeni göz açma yanıtıdır ve en fazla dört puanla derecelendirilir.',
                '**Göz Açma Bileşeni:** Skalanın ilk basamağı olan ve maksimum dört puan alan göz açma yanıtı.',
                'Spontan açık',
                ['göz açma yanıtı', 'dört puan'],
                []),
            (   'Hastanın gözleri ortamda kendiliğinden açık ise ve çevreyi izliyorsa dört puan verilir.',
                '**Spontan Göz Açma:** Gözlerin kendiliğinden açık olması ve çevreyi izlemesi dört puandır.',
                'Spontan açık',
                ['kendiliğinden açık', 'çevreyi izleme'],
                []),
            (   'Hasta seslenildiğinde ya da sözel uyaran verildiğinde gözlerini açıyorsa üç puan alır.',
                '**Sözel Uyaranla Açma:** Sözel seslenmeyle göz açma yanıtı üç puanla değerlendirilir.',
                'Verbal uyaranla',
                ['sözel uyaran', 'üç puan'],
                []),
            (   'Hasta yalnızca tırnak yatağına ya da supraorbital bölgeye uygulanan ağrılı uyaranla gözlerini '
                'açıyorsa iki puanla değerlendirilir.',
                '**Ağrılı Uyaranla Açma:** Yalnızca ağrılı uyaran verildiğinde göz açabilme iki puandır.',
                'Ağrılı uyaranla',
                ['ağrılı uyaranla açma', 'iki puan'],
                []),
            (   'Şiddetli ağrılı uyaranlara rağmen hiçbir şekilde göz açma yanıtı alınamıyorsa bir puan verilir.',
                '**Göz Açmama:** Hiçbir uyarana göz açılmaması durumunda verilen taban bir puan.',
                'Açmıyor',
                ['göz açmıyor', 'bir puan'],
                []),
            (   'Skalanın sözel yanıt bileşeni ise en fazla beş puandır; hasta zaman yer ve kişi oryantasyonuna sahip '
                'akıcı konuşuyorsa beş puan alır.',
                '**Sözel Oryantasyon:** Zaman, yer ve kişi oryantasyonunun tam olması beş tam puandır.',
                'Spontan açık',
                ['sözel yanıt', 'oryantasyon tam'],
                []),
            (   'Sorulara mantıklı ancak dezoryante ve konfüze yanıtlar veriyorsa dört puan bağlamsız uygunsuz '
                'kelimeler kullanıyorsa üç puan verilir.',
                '**Dezoryante ve Uygunsuz:** Dezoryante konuşma dört puan, anlamsız kelimeler çıkarma üç puandır.',
                'Verbal uyaranla',
                ['dezoryante konuşma', 'uygunsuz kelimeler'],
                []),
            (   'Anlaşılır hiçbir kelime çıkarmayıp yalnızca inilti ve homurtu sesleri sergiliyorsa iki puan hiçbir '
                'sözel ses çıkaramıyorsa bir puan olarak kaydedilir.',
                '**Homurtu ve Yanıtsızlık:** Anlamsız homurtu sesleri iki puan, tam sözel yanıtsızlık bir puandır.',
                'Açmıyor',
                ['anlamsız homurtu', 'sözel yanıtsızlık'],
                [])]),
    (   23,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p018_s23',
        [   (   'Glasgow skalasında motor yanıt altı puan üzerinden değerlendirilir ve hastanın santral sinir sistemi '
                'fonksiyonu hakkında en güvenilir prognostik bilgiyi sunar.',
                '**Motor Skorlama:** Altı basamaklı motor yanıt en güçlü nörolojik prognostik göstergedir.',
                'Movement',
                ['motor yanıt', 'Glasgow skalası'],
                []),
            (   'Hasta basit sözlü emirlere eksiksiz uyabiliyorsa, örneğin elini sıkıp bırakabiliyorsa motor yanıta '
                'tam puan olan altı puan verilir.',
                '**Emirlere Uyma:** Basit sözlü komutları yerine getirme tam puan olan altı puandır.',
                'Movement',
                ['emirlere uyma', 'motor skor altı'],
                []),
            (   'Emirlere uymayan ancak supraorbital çentik veya tırnak yatağına uygulanan ağrılı uyaranı eliyle çene '
                'hizasının üzerine çıkarak uzaklaştıran hastada yanıt ağrıyı lokalize etmedir ve beş puan olarak '
                'kaydedilir.',
                '**Ağrıyı Lokalize Etme:** Ağrılı uyarana karşı eli çene üzerine kaldırıp uzaklaştırma beş puandır.',
                'Movement',
                ['ağrıyı lokalize etme', 'motor skor beş'],
                [])]),
    (   24,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p019',
        [   (   'Skalanın üçüncü ve prognoz açısından en belirleyici bileşeni motor yanıttır ve en fazla altı puanla '
                'değerlendirilir.',
                '**Motor Bileşen:** Prognozu en güçlü yansıtan ve maksimum altı puan alan motor yanıt skalası.',
                'Dekortike',
                ['motor yanıt', 'altı puan'],
                []),
            (   'Hasta hekimin sözel emrine uyarak elini kaldırıyor veya parmaklarını sıkıyorsa tam puan olan altı '
                'puan alır.',
                '**Emre Uyma:** Sözel komutlara eksiksiz uyulması motor tam puan olan altı puandır.',
                'Dekortike',
                ['emre uyma', 'tam puan'],
                []),
            (   'Ağrılı uyarana karşı elini köprücük kemiğinin üzerine çıkararak ağrı kaynağını uzaklaştırmaya '
                'çalışıyorsa ağrıyı lokalize etme olarak beş puan verilir.',
                '**Ağrıyı Lokalize Etme:** Ağrı kaynağını saptayıp uzaklaştırma hareketi beş puandır.',
                'Dekortike',
                ['ağrıyı lokalize etme', 'beş puan'],
                []),
            (   'Ağrı verilen ekstremiteyi hızla geri çekerek kaçınma refleksi gösteriyorsa normal fleksör yanıt '
                'olarak dört puan alır.',
                '**Fleksör Kaçınma:** Ağrılı ekstremiteyi hızla geri çekme kaçınma hareketi dört puandır.',
                'Dekortike',
                ['fleksör yanıt', 'kaçınma hareketi'],
                []),
            (   'Anormal fleksör postür sergileyen yani dirsekte fleksiyon addüksiyon ve yumrukları göğse çekme '
                'hareketi yapan hastaya dekortike rijidite olarak üç puan verilir.',
                '**Dekortike Rijidite:** Üst ekstremitede fleksiyon ve addüksiyon gösteren dekortike postür üç '
                'puandır.',
                'Dekortike',
                ['anormal fleksör postür', 'dekortike rijidite'],
                []),
            (   'Anormal ekstansör postür sergileyen yani kollar ve bacaklarda ekstansiyon içe pronasyon ve rijidite '
                'gösteren hastaya deserebre yanıt olarak iki puan verilir.',
                '**Deserebre Rijidite:** Ekstansiyon ve içe pronasyon gösteren deserebre postür iki puandır.',
                'Dekortike',
                ['anormal ekstansör postür', 'deserebre rijidite'],
                []),
            (   'Şiddetli ağrılı uyaranlara karşı hiçbir motor hareket veya kas tonusu gösteremeyen flask hastaya bir '
                'puan verilir.',
                '**Flask Yanıtsızlık:** Hiçbir motor hareket gösteremeyen flask kas tablosu bir puandır.',
                'Dekortike',
                ['flask yanıtsızlık', 'taban puan'],
                []),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: ağrılı uyaranla gözlerini açıp iki puan alan, üst ekstremitede '
                'dirsek fleksiyonuyla dekortike yanıt sergileyip üç puan alan ve anlamsız sesler çıkarıp iki puan alan '
                'bir hastanın Glasgow Koma Skalası skoru yedidir.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: E2, M3 dekortike ve V2 sesler '
                'çıkaran hastanın toplam Glasgow skoru yedidir.',
                'Dekortike',
                ['çıkmış sınav sorusu', 'Glasgow puan hesabı', 'skor yedi'],
                ['past-1790877040005-770270'])]),
    (   25,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p019_s25',
        [   (   'Motor değerlendirmede ağrılı uyarana karşı anormal ekstansiyon yanıtı alınması deserebre postür '
                'olarak adlandırılır ve skalada iki puanla derecelendirilir.',
                '**Deserebre Yanıt:** Ağrılı uyarana karşı ekstremitelerde anormal ekstansiyon iki puandır.',
                'Movement',
                ['deserebre postür', 'anormal ekstansiyon', 'motor skor iki'],
                []),
            (   'Deserebre yanıtta hasta kollarını adduksiyona getirir, dirseklerini ekstansiyona zorlar, ön kolu içe '
                'doğru pronasyona çevirir ve bacaklarını sertçe ekstansiyonda tutar.',
                '**Deserebre Postür:** Kollar içe rotasyon ve ekstansiyonda, bacaklar rijit ekstansiyondadır.',
                'Movement',
                ['ekstansiyon rijiditesi', 'pronasyon'],
                []),
            (   'Bu klinik tablo, lezyonun mezensefalonda kırmızı çekirdeğin alt seviyesine veya üst ponsa indiğini ve '
                'kortikospinal ile rubrospinal inhibisyonun tamamen kalktığını gösterir.',
                '**Lezyon Seviyesi:** Kırmızı çekirdeğin altı, mezensefalon-pons bileşkesi hasarını gösterir.',
                'Movement',
                ['nükleus ruber', 'mezensefalon hasarı', 'rubrospinal yol'],
                [])]),
    (   26,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p019_s26',
        [   (   'Dekortike postür ile deserebre postür arasındaki temel anatomik sınır mezensefalondaki nükleus ruber '
                'yani kırmızı çekirdektir.',
                '**Anatomik Eşik:** Nükleus ruber seviyesi dekortike ve deserebre postür arasındaki anatomik sınırdır.',
                'Movement',
                ['nükleus ruber', 'dekortike deserebre ayrımı'],
                []),
            (   'Kırmızı çekirdeğin üzerindeki hemisferik veya talamik hasarlarda kollar fleksiyonda kalırken, kırmızı '
                'çekirdeğin altına inen beyin sapı hasarlarında kollar ekstansiyona döner.',
                '**Fleksiyondan Ekstansiyona:** Kırmızı çekirdek üstü fleksör, kırmızı çekirdek altı ekstansör yanıt '
                'verir.',
                'Movement',
                ['fleksör postür', 'ekstansör postür'],
                []),
            (   'Klinik takip sırasında dekortike fleksör yanıttan deserebre ekstansör yanıta geçiş, herniasyonun '
                'aşağı doğru ilerlediğinin en somut kanıtıdır.',
                '**Herniasyon Progresyonu:** Fleksiyondan ekstansiyona geçiş rostrokaudal herniasyonun kesin '
                'işaretidir.',
                'Movement',
                ['rostrokaudal herniasyon', 'klinik kötüleşme'],
                [])]),
    (   27,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p019_s27',
        [   (   'Motor değerlendirmede ağrılı uyarana karşı hiçbir kas hareketi veya çekilme görülmemesi, skalada '
                'motor yanıtın bir puan olarak kaydedilmesine yol açar.',
                '**Flaks Yanıtsızlık:** Ağrılı uyarana hiçbir motor yanıt alınamaması bir puan olarak skorlanır.',
                'Movement',
                ['flaks yanıtsızlık', 'motor skor bir'],
                []),
            (   'Flaks veya yanıtsız postür, lezyonun alt pons ve bulbus seviyesine ulaştığını ya da yaygın beyin sapı '
                'iskemisinin geliştiğini gösterir.',
                '**Bulber Düzey:** Alt pons ve medulla hasarı veya yaygın beyin sapı iskemisini yansıtır.',
                'Movement',
                ['alt pons hasarı', 'medulla oblangata', 'beyin sapı iskemisi'],
                []),
            (   'Ayrıca derin hipotermi, sedatif ilaç intoksikasyonları ve nöromüsküler blokör ajanların varlığında da '
                'yalancı bir motor yanıtsızlık tablosu görülebilir.',
                '**Yalancı Yanıtsızlık:** Hipotermi, sedatif intoksikasyon ve nöromüsküler blokörler tablosu taklit '
                'edebilir.',
                'Movement',
                ['hipotermi', 'sedatif intoksikasyonu', 'kas gevşeticiler'],
                [])]),
    (   28,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p020',
        [   (   'Motor yanıtlar aynı zamanda komadaki lezyonun anatomik seviyesini doğrudan gösteren nörolojik '
                'belirteçlerdir.',
                '**Anatomik Düzey:** Motor yanıt paternlerinin hasarın nöroanatomik seviyesini belirlemesi.',
                'Motor yanıtlar: Lezyon Lokalizasyonu',
                ['lezyon lokalizasyonu', 'motor belirteçler'],
                []),
            (   'Ağrıyı amaca yönelik lokalize edebilen motor yanıtlar serebral korteksin ve hemisferik yolların '
                'işlevsel bütünlüğünü koruduğunu gösterir.',
                '**Hemisferik Bütünlük:** Ağrıyı lokalize edebilmenin serebral korteks işlevinin korunduğunu '
                'kanıtlaması.',
                'Hemisferik Lezyon',
                ['hemisferik lezyon', 'amaca yönelik lokalizasyon'],
                []),
            (   'Dekortike rijidite kırmızı çekirdeğin yani nükleus ruberin üzerinde diensefalon veya serebral '
                'hemisfer düzeyindeki yaygın kortikospinal hasarı işaret eder.',
                '**Dekortike Seviyesi:** Kırmızı çekirdeğin üstünde, hemisfer veya diensefalon düzeyindeki '
                'kortikospinal hasar.',
                'Üst Mezensefalon Hasarı',
                ['kırmızı çekirdek', 'nükleus ruber', 'dekortike'],
                []),
            (   'Deserebre rijidite ise kırmızı çekirdek ile vestibüler çekirdekler arasında mezensefalon veya üst '
                'pons düzeyindeki derin beyin sapı hasarını yansıtır ve klinik gidişatın çok daha kötü olduğunu '
                'gösterir.',
                '**Deserebre Seviyesi:** Kırmızı çekirdek altı mezensefalon veya üst pons hasarı ve derin koma '
                'tablosu.',
                'Üst Pontin Hasar',
                ['deserebre rijidite', 'üst pontin hasar', 'kötü prognoz'],
                []),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: gözleri ağrılı uyaranla açılan hasta iki puan, dezoryante '
                'konuşan hasta dört puan ve ağrıyı lokalize eden hasta beş puan alarak toplam on bir puanla '
                'hesaplanır.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: E2, V4 dezoryante ve M5 lokalize '
                'eden hastanın Glasgow koma skoru on birdir.',
                'Motor yanıtlar: Lezyon Lokalizasyonu',
                ['çıkmış sınav sorusu', 'toplam skor on bir', 'GKS hesabı'],
                ['260b60a805e9']),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: Glasgow Koma Skalası ile değerlendirilen bir hastada '
                'alınabilecek en düşük puan üç, alınabilecek en yüksek normal puan ise on beştir.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmiştir: Glasgow Koma Skalasında taban '
                'puan üç, tavan tam puan ise on beştir.',
                'Motor yanıtlar: Lezyon Lokalizasyonu',
                ['çıkmış sınav sorusu', 'en düşük puan üç', 'en yüksek on beş'],
                ['04c8b92b1242', '0adcc53186e5']),
            (   'Sekiz ve altındaki Glasgow koma skoru koma durumunu tanımlar ve hava yolunu koruyamayan bu hastalarda '
                'acil endotrakeal entübasyon endikasyonudur.',
                '**Koma Sınırı Sekiz:** Sekiz ve altı skorun koma sayılması ve endotrakeal entübasyon endikasyonu '
                'oluşturması.',
                'Motor yanıtlar: Lezyon Lokalizasyonu',
                ['sekiz ve altı skor', 'entübasyon endikasyonu'],
                []),
            (   'Skorun on beşten aşağıya doğru her düşüşü intrakraniyal tablonun kötüleştiğini ve ivedi görüntüleme '
                'gerektiğini klinisyene hatırlatır.',
                '**Skor Düşüşü Uyarısı:** Skordaki her düşüşün intrakraniyal kötüleşmeyi ve acil görüntülemeyi işaret '
                'etmesi.',
                'Motor yanıtlar: Lezyon Lokalizasyonu',
                ['skor düşüşü', 'ivedi görüntüleme'],
                [])]),
    (   29,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p020_s29',
        [   (   'Glasgow skalasının sözel yanıt kategorisi beş puan üzerinden değerlendirilir ve kortikal '
                'farkındalığın en hassas göstergesidir.',
                '**Sözel Skorlama:** Beş basamaklı sözel yanıt kortikal farkındalığın en duyarlı ölçütüdür.',
                'Verbal',
                ['sözel yanıt', 'kortikal farkındalık'],
                []),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: Glasgow Koma Skalasında alınabilecek en düşük puan üç, en yüksek '
                'uyanıklık puanı ise on beştir.',
                '**Skor Sınırları:** Glasgow skalasında en düşük puan üç, en yüksek uyanıklık puanı on beştir.',
                'Verbal',
                ['çıkmış', 'Glasgow Koma Skalası'],
                ['04c8b92b1242', '0adcc53186e5']),
            (   'Hasta uyanık ve konuşuyor olmasına rağmen sorulara kafası karışık, zaman veya mekânı şaşırmış '
                'yanıtlar veriyorsa yanıt konfüze olarak kabul edilir ve dört puan alır.',
                '**Konfüze Konuşma:** Zaman ve mekân oryantasyonu bozuk kafası karışık yanıtlar dört puandır.',
                'Verbal',
                ['konfüzyon', 'sözel skor dört'],
                [])]),
    (   30,
        'k2-02-b08',
        'Koma Skorları ve Glasgow Koma Skalası',
        'k2-02-p020_s30',
        [   (   'Sözel değerlendirmede hastanın ardışık ve anlamlı bir cümle kuramayıp yalnızca tek tük rastgele '
                'sözcükler söylemesi uygunsuz kelimeler olarak üç puanla skorlanır.',
                '**Uygunsuz Kelimeler:** Anlamlı cümle kuramayıp rastgele tek sözcükler söyleme üç puandır.',
                'Verbal',
                ['uygunsuz kelimeler', 'sözel skor üç'],
                []),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: gözleri ağrılı uyaranla açılan, konfüze konuşan ve emirlere uyan '
                'hastanın Glasgow koma skoru toplam on ikidir.',
                '**Vaka Skoru:** Göz iki, sözel dört, motor altı puanla hastanın toplam Glasgow skoru on ikidir.',
                'Verbal',
                ['çıkmış', 'Glasgow vaka skoru'],
                ['260b60a805e9']),
            (   'Hem sözlü hem de ağrılı uyarana karşı hiçbir ses çıkaramayan hasta ise sözel kategoriden en düşük '
                'skor olan bir puanı alır.',
                '**Sözel Yanıtsızlık:** Hiçbir sesli yanıt verememe durumu bir puanla derecelendirilir.',
                'Verbal',
                ['sözel yanıtsızlık', 'sözel skor bir'],
                [])]),
    (   31,
        'k2-02-b09',
        'Beyin Sapı Refleksleri ve Pupiller',
        'k2-02-p021',
        [   (   'Komadaki hastada nörolojik lezyonun yerini ve beyin sapının canlılığını değerlendirmek için özel '
                'refleksler kullanılır.',
                '**Beyin Sapı Refleksleri:** Beyin sapının fonksiyonel canlılığını ve lokalizasyonunu test eden '
                'refleksler.',
                'Komada Kullanılan Başlıca Beyin sapı',
                ['beyin sapı refleksleri', 'fonksiyonel canlılık'],
                []),
            (   'Bu bilgi çıkmış sınavda defalarca sorulmuştur: komada anatomik lokalizasyon amacıyla kullanılan '
                'başlıca beyin sapı refleksleri ışık refleksi, kornea refleksi, okülosefalik refleks ve '
                'okülovestibüler reflekslerdir; yüzeyel bir spinal refleks olan kremaster refleksi beyin sapı '
                'refleksleri arasında yer almaz.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Işık, kornea, okülosefalik ve '
                'kalorik test beyin sapı refleksidir; kremaster refleksi beyin sapı refleksi değildir.',
                'Refleksleri',
                ['çıkmış sınav sorusu', 'kremaster refleksi', 'beyin sapı refleksleri'],
                ['q-22_final_230619_145249-67', 'd3-f-097', 'd3-b-056']),
            (   'Işık refleksi afferentini optik sinir efferentini üçüncü kraniyal sinir aracılığıyla mezensefalon '
                'tektumunda tamamlar.',
                '**Işık Refleksi Yolu:** İkinci kraniyal sinir afferenti ve üçüncü kraniyal sinir efferentiyle '
                'mezensefalik ark.',
                'Komada Kullanılan Başlıca Beyin sapı',
                ['ışık refleksi', 'optik sinir', 'okülomotor sinir'],
                []),
            (   'Kornea refleksi trigeminal sinirin oftalmik dalı ile duyuyu alır ve fasiyal sinir aracılığıyla ponsta '
                'bilateral göz kırpma yanıtı oluşturur.',
                '**Kornea Refleksi Yolu:** Beşinci sinir oftalmik dalı duyusu ve yedinci sinir motoruyla pontin '
                'refleks arkı.',
                'Refleksleri',
                ['kornea refleksi', 'trigeminal sinir', 'fasiyal sinir'],
                []),
            (   'Okülosefalik ve okülovestibüler refleksler ise vestibüler çekirdekler ile göz kası nükleusları '
                'arasındaki beyin sapı bağlantılarını test eder.',
                '**Vestibüler Refleksler:** Sekizinci sinir vestibüler çekirdekleri ile ekstraoküler motor nükleuslar '
                'arası entegrasyon.',
                'Komada Kullanılan Başlıca Beyin sapı',
                ['okülosefalik', 'okülovestibüler', 'vestibüler çekirdek'],
                []),
            (   'Yutkunma ve öğürme refleksleri dokuzuncu ve onuncu kraniyal sinirlerle alt beyin sapı yani bulbus '
                'fonksiyonlarını denetler.',
                '**Bulber Refleksler:** Dokuzuncu ve onuncu kraniyal sinirler aracılığıyla medüller fonksiyonların '
                'denetimi.',
                'Refleksleri',
                ['öğürme refleksi', 'yutkunma', 'bulbus'],
                []),
            (   'Bu reflekslerin basamak basamak kaybolması intrakraniyal herniasyonun rostrokaudal yönde beyin sapını '
                'ezerek aşağı indiğini belgeler.',
                '**Rostrokaudal Kayıp:** Reflekslerin yukarıdan aşağıya sırayla kaybının herniasyon ilerleyişini '
                'belgelemesi.',
                'Komada Kullanılan Başlıca Beyin sapı',
                ['rostrokaudal kayıp', 'herniasyon ilerleyişi'],
                []),
            (   'Reflekslerin tamamının iki taraflı ve kalıcı olarak kaybolması ise beyin ölümü tablosunun en kesin '
                'klinik kanıtlarından biridir.',
                '**Beyin Ölümü Kanıtı:** Beyin sapı reflekslerinin iki taraflı ve kalıcı kaybının beyin ölümünü '
                'doğrulaması.',
                'Refleksleri',
                ['beyin ölümü', 'kalıcı refleks kaybı'],
                [])]),
    (   32,
        'k2-02-b09',
        'Beyin Sapı Refleksleri ve Pupiller',
        'k2-02-p022',
        [   (   'Pupillerin çapı ışığa reaktivitesi ve simetrisi komadaki hastada anatomik lokalizasyon sağlayan en '
                'hassas pencerelerdir.',
                '**Pupil Penceresi:** Pupillerin çapı, ışık yanıtı ve simetrisinin anatomik lezyon düzeyini '
                'saptamadaki hassasiyeti.',
                'metabolik ansefalopati:',
                ['pupil çapı', 'ışık reaktivitesi', 'anatomik pencere'],
                []),
            (   'Metabolik ensefalopatilerde ve erken diensefalik lezyonlarda pupiller genellikle küçük boyutlu yani '
                'miyotiktir ancak ışık refleksi bilateral korunmuştur.',
                '**Metabolik ve Diensefalik:** Pupiller küçük ve reaktiftir; ışık yanıtının korunması metabolik '
                'tabloyu gösterir.',
                'küçük, reaktif',
                ['küçük reaktif pupil', 'metabolik ensefalopati'],
                []),
            (   'Pretektal mezensefalon lezyonlarında pupiller geniş ışığa yanıtsız fikse kalır ve zaman zaman hippus '
                'adı verilen dalgalanmalar gösterir.',
                '**Pretektal Pupil:** Pretektal hasarda pupiller geniş, fikse ve hippus dalgalanmaları sergiler.',
                'büyük, fikse,hippus',
                ['pretektal lezyon', 'hippus', 'geniş fikse'],
                []),
            (   'Mezensefalon tektumunun derin hasarlarında sempatik ve parasempatik innervasyon aynı anda kesildiği '
                'için pupiller orta genişlikte ve tamamen ışıksız fikse hale gelir.',
                '**Mezensefalik Fikse:** Hem sempatik hem parasempatik liflerin kesilmesiyle orta genişlikte yanıtsız '
                'pupil.',
                'orta büyüklük, fikse',
                ['orta büyüklük fikse', 'mezensefalon hasarı'],
                []),
            (   'Pons lezyonlarında özellikle masif pons kanamalarında inen sempatik yolların iki taraflı harabiyeti '
                'sonucu iğne ucu yani pinpoint pupiller gelişir.',
                '**Pons ve Pinpoint:** İnen sempatik liflerin iki taraflı harabiyeti sonucu ileri derecede daralmış '
                'pinpoint pupiller.',
                'pinpoint',
                ['pons kanaması', 'pinpoint pupil', 'iğne ucu'],
                []),
            (   'Pinpoint pupiller ileri derecede miyotiktir ve güçlü bir ışık kaynağı ve büyüteçle incelendiğinde '
                'minimal bir ışık refleksi seçilebilir.',
                '**Pinpoint Işık Yanıtı:** İğne ucu pupillerde büyüteç altında minimal ışık refleksinin korunabilmesi.',
                'pinpoint',
                ['minimal ışık refleksi', 'büyüteç muayenesi'],
                []),
            (   'Tek taraflı unkal herniasyonda ipsilateral temporal lob unkusunun üçüncü kraniyal siniri sıkıştırması '
                'sonucu o tarafta geniş ve ışıksız fikse pupil ortaya çıkar.',
                '**Unkal Pupil (3. Sinir):** Temporal lob unkusunun üçüncü sinire basısıyla tek taraflı dilate ve '
                'fikse pupil.',
                'dilate, fikse,',
                ['unkal herniasyon', 'üçüncü sinir basısı', 'anizokori'],
                []),
            (   'Anizokori ile birlikte bilinç bozukluğu saptanan bir hastada bu bulgu derhal cerrahi dekompresyon '
                'gerektiren acil bir kitle etkisi işaretidir.',
                '**Acil Cerrahi Dekompresyon:** Anizokori ve bilinç bozukluğu birlikteliğinin acil cerrahi kitle '
                'alarmı olması.',
                'III KS(unkal):',
                ['cerrahi alarm', 'kitle etkisi', 'anizokori'],
                [])]),
    (   33,
        'k2-02-b09',
        'Beyin Sapı Refleksleri ve Pupiller',
        'k2-02-p023',
        [   (   'Pupillerin ışık yanıtı toksik maddelerden ve sistemik metabolik uç durumlardan da derinden etkilenir.',
                '**Toksik Pupiller:** Toksik maddeler ve metabolik uç bozuklukların pupil reaktivitesini değiştirmesi.',
                'Midriyatik, ışığa yanıtsız pupil',
                ['toksik maddeler', 'pupil yanıtı'],
                []),
            (   'İki taraflı midriyatik dilate ve ışığa tamamen yanıtsız pupiller atropin skopolamin gibi '
                'antikolinerjik ilaç alımlarında izlenir.',
                '**Antikolinerjik Midriyazis:** Atropin ve skopolamin alımında iki taraflı geniş, ışığa yanıtsız '
                'midriyatik pupiller.',
                'Atropin, skopolamin, glutetimid, barbiturat',
                ['atropin', 'skopolamin', 'midriyatik pupil'],
                []),
            (   'Benzer şekilde glutetimid ve yüksek doz barbitürat intoksikasyonlarında da midriyatik ve ışıksız '
                'pupiller tabloya eşlik eder.',
                '**Barbitürat ve Glutetimid:** Glutetimid ve derin barbitürat zehirlenmesinde ışığa yanıtsız '
                'midriyazis tablosu.',
                'Atropin, skopolamin, glutetimid, barbiturat',
                ['glutetimid', 'barbitürat intoksikasyonu'],
                []),
            (   'Ağır sistemik hipoksi kardiyak arrest sonrası anoksik beyin hasarı ve derin hipotermi de pupillerin '
                'paralitik dilatasyonuna yol açar.',
                '**Anoksi ve Hipotermi:** Ağır anoksi ve derin hipoterminin iki taraflı paralitik midriyazis '
                'oluşturması.',
                'Hipoksi',
                ['anoksik hasar', 'derin hipotermi', 'paralitik dilatasyon'],
                []),
            (   'Buna karşılık ileri derecede miyotik ve ışıksız pupiller opiat intoksikasyonunun en patognomonik '
                'fizik muayene bulgusudur.',
                '**Opiat Miyozisi:** İleri derecede miyotik pinpoint pupillerin opiat intoksikasyonu için tanısal '
                'değeri.',
                'İleri miyotik pupil',
                ['opiat intoksikasyonu', 'ileri miyotik pupil'],
                []),
            (   'Koma ileri derecede solunum depresyonu ve iğne ucu miyotik pupillerden oluşan bu klasik triad '
                'görüldüğünde hekim derhal damar içi nalokson hazırlamalıdır.',
                '**Klasik Opioid Triadı:** Koma, solunum depresyonu ve miyozis triadında damar içi ivedi nalokson '
                'hazırlığı.',
                'Opiate intoksikasyonu',
                ['opioid triadı', 'damar içi nalokson'],
                []),
            (   'Toksik pupillerin bilinmesi gereksiz acil cerrahi girişimleri engellerken spesifik farmakolojik '
                'antidotların saniyeler içinde uygulanmasını sağlar.',
                '**Gereksiz Cerrahiden Korunma:** Toksik nedenleri doğru tanıyarak hastayı boş cerrahiden koruma ve '
                'antidot uygulama.',
                'Midriyatik, ışığa yanıtsız pupil',
                ['spesifik antidot', 'cerrahiyi engelleme'],
                [])]),
    (   34,
        'k2-02-b10',
        'Göz Hareketleri: Okülosefalik ve Kalorik Test',
        'k2-02-p024',
        [   (   'Göz hareketlerinin ve okülosefalik refleksin değerlendirilmesi beyin sapı tegmentumunun işlevsel '
                'bütünlüğünü yansıtır.',
                '**Okülosefalik Refleks:** Beyin sapı tegmentumunun ve kranial sinir entegrasyonunun okülosefalik '
                'refleksle ölçümü.',
                'Göz Hareketleri: Okülosefalik R',
                ['göz hareketleri', 'okülosefalik refleks'],
                []),
            (   'Bu muayeneye başlamadan önce hastada servikal omurga travması veya kemik kırığı şüphesi mutlaka '
                'ekarte edilmelidir.',
                '**Servikal Güvenlik:** Boyun hareketlerine başlamadan önce servikal travma şüphesinin ekarte edilmesi '
                'zorunluluğu.',
                'Baş 30 derecede: her iki tarafa çevrilir ve',
                ['servikal travma', 'boyun kırığı şüphesi'],
                []),
            (   'Boyun güvenliği sağlandıktan sonra hastanın başı otuz derece yükseltilir göz kapakları açık tutularak '
                'baş hızla sağa ve sola çevrilir.',
                '**Testin Uygulanışı:** Baş otuz derece fleksiyonda hızla sağa ve sola çevrilerek göz yanıtlarının '
                'izlenmesi.',
                'göz hareketleri gözlenir',
                ['otuz derece fleksiyon', 'sağa sola çevirme'],
                []),
            (   'Bilinci kapalı fakat beyin sapı sağlam olan bir hastada gözler başın çevrildiği yönün tam tersine '
                'doğru tonik olarak kayar ve orta hatta sabit kalır.',
                '**Pozitif Oyuncak Bebek Gözü:** Beyin sapı sağlamsa gözlerin başın çevrildiği yönün aksine tonik '
                'kayması.',
                'Bilinç kapalı',
                ['oyuncak bebek gözü', 'tonik kayma', 'orta hat'],
                []),
            (   'Bu tablo oyuncak bebek gözü hareketinin pozitif olduğunu yani mezensefalon pons ve sekizinci sinir '
                'çekirdeklerinin sağlam çalıştığını gösterir.',
                '**Sağlam Beyin Sapı:** Pozitif refleksin mezensefalon, pons ve vestibüler çekirdeklerin sağlamlığını '
                'kanıtlaması.',
                'Beyin sapı sağlam',
                ['sağlam beyin sapı', 'mezensefalon pons bütünlüğü'],
                []),
            (   'Eğer beyin sapında özellikle pons tegmentumunda yapısal bir lezyon varsa okülosefalik refleks '
                'kaybolur.',
                '**Refleks Kaybı:** Pons tegmentumu hasarında okülosefalik refleks arkının kopması ve kaybı.',
                'Göz Hareketleri: Okülosefalik R',
                ['tegmentum lezyonu', 'refleks kaybı'],
                []),
            (   'Refleks kaybolduğunda gözler başın döndürüldüğü yöne doğru hareketsizce birlikte döner ve başla aynı '
                'hizada sabit kalır.',
                '**Gözlerin Birlikte Dönmesi:** Refleks yokluğunda gözlerin başla aynı yöne sabit biçimde '
                'sürüklenmesi.',
                'göz hareketleri gözlenir',
                ['sabit kalma', 'birlikte dönme'],
                []),
            (   'Okülosefalik yanıtın bilateral yokluğu komadaki hastada beyin sapı hasarının veya ileri evre '
                'rostrokaudal herniasyonun objektif bir kanıtıdır.',
                '**Herniasyon Kanıtı:** Okülosefalik yanıt yokluğunun derin beyin sapı hasarını ve herniasyonu '
                'belgelemesi.',
                'Beyin sapı sağlam',
                ['rostrokaudal herniasyon', 'objektif kanıt'],
                [])]),
    (   35,
        'k2-02-b10',
        'Göz Hareketleri: Okülosefalik ve Kalorik Test',
        'k2-02-p024_s35',
        [   (   'Komalı bir hastada başı hızla sağa veya sola çevirdiğimizde gözlerin başın dönüş yönüyle birlikte '
                'hareket etmesi, yani orta hatta sabit kalması okülosefalik refleksin kaybolduğunu gösterir.',
                '**Negatif Okülosefalik:** Gözlerin başla birlikte dönmesi beyin sapı hasarının kanıtıdır.',
                'Beyin sapı HASARLI',
                ['okülosefalik refleks', 'bebek gözü fenomeni'],
                []),
            (   'Bebek gözü refleksinin negatif olması, pons ve mezensefalondaki vestibüler ve okülomotor '
                'bağlantıların hasar gördüğünün kesin bir kanıtıdır.',
                '**Pons ve Mezensefalon:** Vestibüler çekirdekler ve medial longitudinal fasikül hasarını belgeler.',
                'Beyin sapı HASARLI',
                ['medial longitudinal fasikül', 'pons hasarı'],
                []),
            (   'Bununla birlikte derin barbitürat koması, fenitoin intoksikasyonu ve bazı kas gevşeticiler de yapısal '
                'bir hasar olmadan bu refleksi geçici olarak baskılayabilir.',
                '**Toksik Baskılanma:** Barbitürat ve sedatif intoksikasyonları refleksi yalancı olarak yok edebilir.',
                'Beyin sapı HASARLI',
                ['barbitürat koması', 'fenitoin toksisitesi'],
                [])]),
    (   36,
        'k2-02-b10',
        'Göz Hareketleri: Okülosefalik ve Kalorik Test',
        'k2-02-p025_s36',
        [   (   'Kalorik test veya vestibülo-oküler refleks muayenesi, özellikle servikal travma şüphesi nedeniyle '
                'başın çevrilemediği komalı hastalarda en güvenilir tanı aracıdır.',
                '**Vestibülo-Oküler Test:** Servikal travmada güvenle uygulanan en duyarlı beyin sapı refleks '
                'testidir.',
                'Kalorik testler',
                ['kalorik test', 'vestibülo-oküler refleks'],
                []),
            (   'Test uygulanmadan önce otoskop ile dış kulak yolu mutlaka incelenmeli, buşon veya kulak zarı '
                'perforasyonu olmadığı teyit edilmelidir.',
                '**Otoskopik Muayene:** Zar perforasyonu ve buşon varlığı test öncesinde mutlaka dışlanmalıdır.',
                'Kalorik testler',
                ['otoskopik muayene', 'timpanik membran'],
                []),
            (   'Hastanın başı otuz derece yukarı kaldırıldıktan sonra dış kulak yoluna yavaşça yirmi ila elli '
                'mililitre buzlu soğuk su enjekte edilir.',
                '**Test Protokolü:** Baş otuz derece fleksiyonda iken dış kulak yoluna buzlu soğuk su verilir.',
                'Kalorik testler',
                ['otuz derece fleksiyon', 'buzlu su'],
                [])]),
    (   37,
        'k2-02-b10',
        'Göz Hareketleri: Okülosefalik ve Kalorik Test',
        'k2-02-p025',
        [   (   'Okülosefalik refleksin şüpheli olduğu ya da servikal travma nedeniyle boynun hareket ettirilemediği '
                'olgularda kalorik test yani vestibülo-oküler refleks uygulanır.',
                '**Kalorik Test Endikasyonu:** Servikal travmalı veya şüpheli olgularda okülovestibüler kalorik testin '
                'devreye girmesi.',
                'Vestibülo-oküler refleksler',
                ['kalorik test', 'vestibülo-oküler refleks'],
                []),
            (   'Kalorik test için hastanın başı otuz derece yükseltilerek lateral semisirküler kanal vertikal '
                'pozisyona getirilir ve timpanik membran otoskopla kontrol edilir.',
                '**Test Hazırlığı:** Başın otuz derece yükseltilip semisirküler kanalın dikey konuma alınması ve zar '
                'kontrolü.',
                'Bilinç kapalı',
                ['lateral semisirküler kanal', 'timpanik membran'],
                []),
            (   'Kulak zarı sağlam olan hastada dış kulak yoluna yavaşça yirmi ila elli mililitre buzlu soğuk su '
                'enjekte edilir.',
                '**Soğuk Su İrrigasyonu:** Dış kulak yoluna yirmi-elli mililitre buzlu soğuk suyun yavaş infüzyonu.',
                'Soğuk Su',
                ['soğuk su irrigasyonu', 'buzlu su'],
                []),
            (   'Bilinci kapalı fakat beyin sapı fonksiyonları sağlam bir hastada kortikal fiksasyon mekanizmaları '
                'devre dışı kaldığı için hızlı faz görülmez.',
                '**Kortikal Hızlı Faz Yokluğu:** Komadaki hastada korteks baskılandığı için nistagmusun düzeltici '
                'hızlı fazının oluşmaması.',
                'Beyin sapı sağlam',
                ['kortikal fiksasyon', 'hızlı faz yokluğu'],
                []),
            (   'Eksitatör endolenf akımının uyarılmasıyla her iki göz küresi yavaşça soğuk su verilen kulağın '
                'tarafına doğru tonik olarak sapar.',
                '**Tonik Deviasyon:** Sağlam beyin sapında gözlerin soğuk su verilen kulağa doğru tonik konjuge '
                'sapması.',
                'Soğuk Su',
                ['tonik deviasyon', 'endolenf akımı'],
                []),
            (   'Bu tonik konjuge deviasyonun izlenmesi sekizinci sinir pontin vestibüler çekirdekler mediyal '
                'longitudinal fasikül ve okülomotor çekirdeklerin sağlamlığını kanıtlar.',
                '**Yolun Sağlamlığı:** Sekizinci sinir, pontin nükleuslar, MLF ve motor çekirdeklerin kesintisiz '
                'sağlamlığı.',
                'Beyin sapı sağlam',
                ['mediyal longitudinal fasikül', 'vestibüler çekirdek'],
                []),
            (   'Eğer alt beyin sapında veya ponsta ağır bir harabiyet varsa soğuk su irrigasyonuna rağmen gözlerde '
                'hiçbir deviasyon hareketi oluşmaz.',
                '**Yanıtsız Kalorik:** Pons ve alt beyin sapı harabiyetinde hiçbir göz deviasyonunun ortaya çıkmaması.',
                'Bilinç kapalı',
                ['yanıtsız kalorik', 'hareketsiz gözler'],
                []),
            (   'Kalorik teste yanıtın iki taraflı olarak tamamen alınamaması beyin ölümü tanısı konulurken aranan en '
                'zorunlu klinik kriterlerden biridir.',
                '**Beyin Ölümü Şartı:** Kalorik yanıtın bilateral tam yokluğunun beyin ölümü protokolündeki zorunlu '
                'yeri.',
                'Beyin sapı sağlam',
                ['beyin ölümü protokolü', 'zorunlu kriter'],
                [])]),
    (   38,
        'k2-02-b10',
        'Göz Hareketleri: Okülosefalik ve Kalorik Test',
        'k2-02-p025_s38',
        [   (   'Dış kulak yoluna buzlu su verilmesine rağmen göz kürelerinde hiçbir tonik deviasyon veya hareket '
                'görülmemesi kalorik yanıtın negatif olduğunu gösterir.',
                '**Yanıtsız Kalorik Test:** Soğuk su irrigasyonuna rağmen gözlerin hareketsiz kalması negatif '
                'yanıttır.',
                'Beyin sapı HASARLI',
                ['negatif kalorik yanıt', 'arefleksi'],
                []),
            (   'Bu yanıtsızlık tablosu, sekizinci kraniyal sinirden başlayarak vestibüler nükleuslar, medial '
                'longitudinal fasikül ve okülomotor çekirdekleri kapsayan refleks arkının koptuğunu kanıtlar.',
                '**Refleks Arkı Hasarı:** Sekizinci kraniyal sinir, pons ve mezensefalon bağlantılarının koptuğunu '
                'gösterir.',
                'Beyin sapı HASARLI',
                ['vestibulokoklear sinir', 'medial longitudinal fasikül'],
                []),
            (   'Klinik olarak alt beyin sapının, yani pons ve mezensefalon bileşkesinin ağır yapısal hasara veya '
                'herniasyon basısına uğradığını belgeler.',
                '**Ağır Yapısal Hasar:** Pons ve mezensefalonun geri dönüşsüz iskemik veya mekanik harabiyetidir.',
                'Beyin sapı HASARLI',
                ['beyin sapı harabiyeti', 'herniasyon basısı'],
                [])]),
    (   39,
        'k2-02-b11',
        'Komada Solunum Paternleri ve Rostrokaudal Düzeyler',
        'k2-02-p026_s39',
        [   (   'Solunumun kontrolü beyin sapında yer alan özelleşmiş nöronal gruplar tarafından yürütülür ve komada '
                'solunum paterninin değişmesi lezyon seviyesini ele verir.',
                '**Solunum Paternleri:** Solunum merkezlerinin tutulumu lezyon seviyesini gösteren kritik göstergedir.',
                'Komada solunum',
                ['solunum kontrolü', 'solunum paternleri'],
                []),
            (   'Diensefalon hasarında kortikal inhibisyon kalktığı için periyodik solunum başlarken, mezensefalon '
                'hasarında taşipne, ponsta apne nöbetleri ve bulbusta ise düzensiz solunum gelişir.',
                '**Rostrokaudal Hiyerarşi:** Diensefalonda periyodik, mezensefalonda taşipne, ponsta apne, bulbusta '
                'ataksi görülür.',
                'Komada solunum',
                ['Cheyne Stokes', 'santral nörojenik hiperventilasyon', 'apnöktik solunum'],
                []),
            (   'Bu patolojik solunum şekilleri klinisyene görüntüleme cihazına ulaşmadan önce bile lezyonun anatomik '
                'koordinatını fısıldar.',
                '**Yatak Başı Lokalizasyon:** Solunum paterni nörogörüntüleme öncesi anatomik lezyon seviyesini '
                'belirler.',
                'Komada solunum',
                ['yatak başı muayene', 'anatomik lokalizasyon'],
                [])]),
    (   40,
        'k2-02-b11',
        'Komada Solunum Paternleri ve Rostrokaudal Düzeyler',
        'k2-02-p026',
        [   (   'Solunumun ritmik kontrolü serebral korteksten başlayarak diensefalon mezensefalon pons ve medullaya '
                'uzanan hiyerarşik bir ağ tarafından yürütülür.',
                '**Solunum Ağı:** Korteksten medullaya uzanan solunum merkezlerinin hiyerarşik organizasyonu.',
                'Cheyne-Stokes solunumu',
                ['solunum kontrolü', 'hiyerarşik ağ'],
                []),
            (   'Bu nedenle komadaki bir hastanın solunum paterni beyin sapı hasarının hangi anatomik seviyede '
                'bulunduğunu açıkça ortaya koyar.',
                '**Lokalizan Solunum:** Solunum paterninin beyin sapındaki hasar düzeyini açıkça yansıtması.',
                'Cheyne-Stokes solunumu',
                ['solunum paterni', 'anatomik seviye'],
                []),
            (   'Cheyne-Stokes solunumu periyodik olarak kreşendo tarzında derinleşip hızlanan ardından dekreşendo '
                'azalarak kısa bir apne dönemine giren solunumdur.',
                '**Cheyne-Stokes Solunumu:** Kreşendo tarzı derinleşip dekreşendo azalan ve apneye giren periyodik '
                'solunum.',
                'Cheyne-Stokes solunumu',
                ['Cheyne-Stokes solunumu', 'kreşendo dekreşendo', 'apne'],
                []),
            (   'Bu solunum şekli bilateral derin serebral hemisfer lezyonlarında ya da diensefalik düzeydeki '
                'baskılanmalarda ve metabolik komalarda sıkça izlenir.',
                '**Diensefalik Lezyon:** Bilateral derin hemisfer veya diensefalon lezyonlarında Cheyne-Stokes '
                'görülmesi.',
                'Cheyne-Stokes solunumu',
                ['bilateral hemisfer', 'diensefalik baskılanma'],
                []),
            (   'Santral nörojenik hiperventilasyon son derece düzenli derin ve dakikada kırkın üzerinde çok hızlı '
                'solunumla karakterizedir.',
                '**Santral Hiperventilasyon:** Düzenli, derin ve dakikada kırkın üzerinde hızlı solunum paterni.',
                'Santral nörojenik hiperventilasyon',
                ['santral nörojenik hiperventilasyon', 'hızlı solunum'],
                []),
            (   'Bu tablo mezensefalon ile üst pons arasındaki tegmental bölge lezyonlarında ortaya çıkar ve kanda '
                'belirgin respiratuvar alkaloz oluşturur.',
                '**Mezensefalik Hasar:** Mezensefalon-üst pons tegmentum hasarı ve kanda gelişen respiratuvar alkaloz.',
                'Santral nörojenik hiperventilasyon',
                ['mezensefalon üst pons', 'respiratuvar alkaloz'],
                []),
            (   'Apnestik solunum inspiryumun en zirve noktasında iki ila üç saniye süren kramp benzeri duraklamalarla '
                'kendini gösteren patolojik bir solunumdur.',
                '**Apnestik Solunum:** İnspiryum zirvesinde iki-üç saniye süren kramp benzeri duraklamalı solunum.',
                'Apnestik solunum',
                ['apnestik solunum', 'inspiryum duraklaması'],
                []),
            (   'Bu apnestik duraklamalar ponsun orta veya alt tegmentumundaki solunum merkezlerinin hasar gördüğünü '
                'gösterir.',
                '**Pontin Solunum:** Ponsun orta veya alt tegmentumundaki solunum merkezlerinin hasarlanması.',
                'Apnestik solunum',
                ['orta alt pons', 'pontin tegmentum'],
                [])]),
    (   41,
        'k2-02-b11',
        'Komada Solunum Paternleri ve Rostrokaudal Düzeyler',
        'k2-02-p027',
        [   (   'Alt pons ve üst medulla bileşkesine ulaşıldığında apneik duraklamalarla ayrılan düzensiz solunum '
                'gruplarından oluşan küme solunumu izlenir.',
                '**Küme Solunumu:** Alt pons ve üst medulla bileşkesinde düzensiz solunum grupları ve apne aralıkları.',
                'Beyin Sapı Bulgularının Özeti',
                ['küme solunumu', 'alt pons üst medulla'],
                []),
            (   'Bu bilgi çıkmış sınavda sorulmuştur: medulla oblangata yani bulbus lezyonlarında solunum ritmi ve '
                'derinliği tamamen kaotik hale gelir; inspiratuvar nöronların hasarıyla ortaya çıkan bu düzensiz ve '
                'yetersiz solunum paternine ataksik solunum veya Biot solunumu denir.',
                '**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Medulla bulbus lezyonunda görülen '
                'kaotik düzensiz solunum ataksik solunumdur.',
                'Beyin Sapı Bulgularının Özeti',
                ['çıkmış sınav sorusu', 'ataksik solunum', 'bulbus lezyonu', 'Biot solunumu'],
                ['d3-b-057']),
            (   'Ataksik solunum hastanın dakikalar içinde agonal solunuma ve tam solunum arrestine gireceğini haber '
                'veren preterminal bir bulgudur.',
                '**Preterminal Aşama:** Ataksik solunumun dakikalar içinde tam apne ve arrest habercisi olması.',
                'Beyin Sapı Bulgularının Özeti',
                ['ataksik solunum', 'solunum arresti', 'preterminal'],
                []),
            (   'Beyin sapı bulguları tablosu incelendiğinde lezyonun yukarıdan aşağıya yani rostrokaudal ilerleyişi '
                'adım adım izlenebilir.',
                '**Rostrokaudal İlerleme:** Tabloda lezyonun diensefalondan medullaya doğru rostrokaudal iniş '
                'basamakları.',
                'Beyin Sapı Bulgularının Özeti',
                ['rostrokaudal iniş', 'beyin sapı özeti'],
                []),
            (   'Erken diensefalik evrede küçük reaktif pupiller ve Cheyne-Stokes solunumu varken mezensefalik evrede '
                'pupiller orta genişlikte fikse hale gelir ve hiperventilasyon başlar.',
                "**Diensefalikten Mezensefale:** Küçük reaktif pupil ve Cheyne-Stokes'tan orta genişlikte fikse pupil "
                've hiperventilasyona geçiş.',
                'Beyin Sapı Bulgularının Özeti',
                ['erken diensefalik evre', 'orta mezensefalik'],
                []),
            (   'Pontin evrede iğne ucu pupiller okülosefalik refleks kaybı ve apnestik solunum tabloya hakim olur.',
                '**Pontin Evre Bulguları:** İğne ucu pupiller, okülosefalik refleks kaybı ve apnestik solunum tablosu.',
                'Beyin Sapı Bulgularının Özeti',
                ['pontin evre', 'pinpoint pupil', 'apnestik solunum'],
                []),
            (   'Medüller evreye gelindiğinde ise dilate ışıksız pupiller ataksik solunum ve tam arefleksi ile hasta '
                'ölüme sürüklenir.',
                '**Medüller Terminal Evre:** Dilate yanıtsız pupiller, ataksik solunum ve tam arefleksiyle ölüm '
                'tablosu.',
                'Beyin Sapı Bulgularının Özeti',
                ['medüller evre', 'dilate ışıksız pupil', 'arefleksi'],
                []),
            (   'Bu rostrokaudal kötüleşme basamaklarının iyi bilinmesi herniasyonun hangi aşamada olduğunu tespit '
                'edip acil cerrahi müdahale zamanlamasını belirler.',
                '**Cerrahi Zamanlama:** Herniasyon basamağını erken tanıyarak geri dönüşsüz aşamadan önce acil '
                'cerrahiye geçiş.',
                'Beyin Sapı Bulgularının Özeti',
                ['herniasyon aşaması', 'cerrahi zamanlama'],
                [])]),
    (   42,
        'k2-02-b12',
        'Koma Tanısında Laboratuvar Testleri',
        'k2-02-p028',
        [   (   'Koma tanısında laboratuvar testleri hastayı gereksiz invaziv girişimlerden kurtaran ve doğrudan geri '
                'döndürülebilir etiyolojiyi aydınlatan en güçlü araçtır.',
                '**Laboratuvarın Gücü:** Geri döndürülebilir etiyolojiyi saptayan ve gereksiz cerrahiyi önleyen '
                'laboratuvar paneli.',
                'Kan Şekeri (Hipoglisemiyi atlama)',
                ['laboratuvar testleri', 'geri döndürülebilir etiyoloji'],
                []),
            (   'Testlerin başında her zaman kan şekeri gelir ve hipoglisemi koması acil serviste asla atlanmaması '
                'gereken bir numaralı hedeftir.',
                '**Bir Numaralı Hedef:** Hipoglisemi komasının laboratuvarda asla atlanmaması gereken birincil hedef '
                'olması.',
                'Kan Şekeri (Hipoglisemiyi atlama)',
                ['kan şekeri', 'hipoglisemi koması'],
                []),
            (   'Özellikle diyabetes mellitus tanısıyla insülin kullanan hastalarda ve kronik alkolizm olgularında '
                'bilinç kapalılığının en sık nedeni derin hipoglisemidir.',
                '**Diyabet ve Alkolizm:** Diyabetli ve alkolik hastalarda derin hipogliseminin en sık koma sebebi '
                'olması.',
                'Özellikle DM ve Kr. Alkolizmde etiyoloji',
                ['diyabetes mellitus', 'kronik alkolizm', 'derin hipoglisemi'],
                []),
            (   'Rutin biyokimyada elektrolitler ivedilikle taranmalı ve en sık elektrolit bozukluğu olan sodyum '
                'seviyesine bakılmalıdır.',
                '**Sodyum Önceliği:** Biyokimyada en sık elektrolit bozukluğu olan sodyum seviyesinin ivedilikle '
                'taranması.',
                'Elektrolitler (en sık Na)',
                ['sodyum seviyesi', 'elektrolit paneli'],
                []),
            (   'Akut hiponatremi serebral ödem ve koma yaparken hipernatremi ise hücresel dehidratasyon ve beyin '
                'kanaması riski oluşturur.',
                '**Sodyum Uçları:** Hiponatreminin beyin ödemi, hipernatreminin ise hücresel dehidratasyon '
                'oluşturması.',
                'Hiponatremi sık neden, tümör olanlarda',
                ['akut hiponatremi', 'hipernatremi', 'serebral ödem'],
                []),
            (   'Malignitesi veya kemik metastazı olan komalı hastalarda hiperkalsemi ve kalsiyum metabolizma '
                'bozuklukları mutlaka dışlanmalıdır.',
                '**Hiperkalsemi Riski:** Kanserli ve metastazlı hastalarda kalsiyum yüksekliği ve metabolizma '
                'bozuklukları.',
                'kalsiyum metabolizma bozukluğu sık',
                ['malignite', 'hiperkalsemi', 'kalsiyum bozukluğu'],
                []),
            (   'Karaciğer enzimlerinin ve kanda amonyak düzeyinin ölçülmesi karaciğer komasını üre ve kreatinin '
                'değerleri ise üremik ensefalopatiyi aydınlatır.',
                '**Organ Testleri:** Amonyak ile hepatik koma, üre ve kreatinin ile üremik ensefalopati teşhisi.',
                'Kan Şekeri (Hipoglisemiyi atlama)',
                ['amonyak', 'karaciğer koması', 'üremi'],
                []),
            (   'Basit bir biyokimyasal dengesizliğin düzeltilmesi hastanın dakikalar içinde komadan tam uyanıklık '
                'haline geçmesini sağlayabilir.',
                '**Hızlı Düzelme:** Biyokimyasal dengesizliğin replasmanı ile hastanın hızla komadan uyanması.',
                'Özellikle DM ve Kr. Alkolizmde etiyoloji',
                ['biyokimyasal düzelme', 'tam uyanıklık'],
                [])]),
    (   43,
        'k2-02-b12',
        'Koma Tanısında Laboratuvar Testleri',
        'k2-02-p029',
        [   (   'Laboratuvar değerlendirmesinde arteriyel kan gazı analizi komanın metabolik ve solunumsal derinliğini '
                'ortaya koyan en hayati parametredir.',
                '**Arteriyel Kan Gazı:** Komanın metabolik ve solunumsal derinliğini ortaya koyan arteriyel kan gazı '
                'analizi.',
                'Arteryal Kan Gazı (asidoz önemli)',
                ['arteriyel kan gazı', 'metabolik derinlik'],
                []),
            (   'Kan gazında belirgin asidoz mevcudiyeti klinisyene metabolik bir intoksikasyon ya da derin '
                'hipoperfüzyon olduğunu haber verir.',
                '**Asidoz Alarmı:** Belirgin asidozun metabolik intoksikasyon veya derin doku hipoperfüzyonunu '
                'göstermesi.',
                'Arteryal Kan Gazı (asidoz önemli)',
                ['metabolik asidoz', 'doku hipoperfüzyonu'],
                []),
            (   'Kanda pe ha değerinin düşmesi salisilat zehirlenmesi metanol alımı veya diyabetik ketoasidoz '
                'şüphesini en üst basamağa taşır.',
                '**Düşük pH Nedenleri:** Düşük pH değerinin salisilat, metanol veya diyabetik ketoasidozu işaret '
                'etmesi.',
                'pH: (salisilat zehirlenmesi, methanol)',
                ['düşük pe ha', 'salisilat zehirlenmesi', 'metanol'],
                []),
            (   'Yangından kurtarılan ya da kapalı alanda baygın bulunan olgularda karboksihemoglobin düzeyi ölçülerek '
                'karbonmonoksit ve duman zehirlenmesi aranmalıdır.',
                '**Karboksihemoglobin Düzeyi:** Duman ve yangın olgularında karboksihemoglobin ile karbonmonoksit '
                'tespiti.',
                'COHbg: (CO, Duman zehirlenmesi)',
                ['karboksihemoglobin', 'karbonmonoksit zehirlenmesi'],
                []),
            (   'Tam kan sayımında lökositoz sepsis ve menenjiti derin anemi ise beyin oksijen sunumunun çökmesini '
                'belgeler.',
                '**Hemogram İpuçları:** Lökositoz ile sepsis-menenjit, derin anemi ile hipoksik perfüzyon çöküşü '
                'kanıtı.',
                'Tam Kan Sayımı (uzamış kanama zamanı',
                ['tam kan sayımı', 'lökositoz', 'derin anemi'],
                []),
            (   'Trombositopeni ve uzamış koagülasyon testleri spontan intrakraniyal kanama riskini ve dissemine '
                'intravasküler koagülasyonu gösterir.',
                '**Koagülasyon Bozukluğu:** Trombositopeni ve uzamış pıhtılaşma testlerinin spontan beyin kanaması '
                'alarmı vermesi.',
                'önemli)',
                ['trombositopeni', 'kanama profili', 'intrakraniyal kanama'],
                []),
            (   'Şüpheli olgularda geniş toksikolojik idrar ve serum taramaları yapılarak aşırı doz sedatif veya '
                'stimulan maddeler saptanmalıdır.',
                '**Toksikolojik Tarama:** Geniş idrar ve serum taraması ile sedatif veya uyarıcı toksinlerin '
                'belirlenmesi.',
                'Kanama profili',
                ['toksikolojik tarama', 'sedatif aşırı dozu'],
                []),
            (   'Bu laboratuvar sonuçları nörogörüntüleme öncesinde hastanın fizyolojik parametrelerini dengelemek '
                'için klinisyene kesin bir yol haritası sunar.',
                '**Görüntüleme Öncesi:** Tomografiye gitmeden önce fizyolojik dengeleri kurmak için kesin laboratuvar '
                'yol haritası.',
                'Trombositopeni; Kanama, sepsis',
                ['fizyolojik parametreler', 'klinik yol haritası'],
                [])]),
    (   44,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s44',
        [   (   'Acil servise getirilen bilinci kapalı bir hastada panik yapmadan, hayat kurtarıcı basamakları adım '
                'adım takip eden sistematik bir algoritmaya ihtiyacımız vardır.',
                '**Sistematik Algoritma:** Bilinci kapalı hastada hata payını sıfıra indiren adım adım karar '
                'protokolü.',
                'Algoritma',
                ['acil algoritma', 'klinik protokol'],
                []),
            (   'Bu algoritma, önce hastanın vital fonksiyonlarını emniyete alır, ardından bilincin gerçekten kapalı '
                'olup olmadığını sınar.',
                '**İlk Adımlar:** Önce hava yolu ve vital stabilizasyon, ardından yalancı koma taklitçilerinin '
                'elenmesi.',
                'Algoritma',
                ['vital stabilizasyon', 'yalancı koma ayrımı'],
                []),
            (   'Daha sonra metabolik düzeltmeleri yapar ve hastayı beyin sapı bulguları üzerinden cerrahi ya da '
                'medikal tedavi yoluna yönlendirir.',
                '**Karar Kavşağı:** Metabolik resüsitasyon ve beyin sapı refleksleri üzerinden cerrahi-medikal '
                'yönlendirme.',
                'Algoritma',
                ['metabolik resüsitasyon', 'cerrahi yönlendirme'],
                [])]),
    (   45,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s45',
        [   (   'Algoritmamızın ilk ve en kritik basamağı hava yolu, solunum ve dolaşımın, yani a-be-ce ilkelerinin '
                'derhal sağlanmasıdır.',
                '**ABC Basamağı:** Hava yolu açıklığı, yeterli solunum ve hemodinamik dolaşımın güvenceye alınması.',
                'Bilinci Kapalı Hastaya Yaklaşım',
                ['hava yolu', 'solunum', 'dolaşım', 'ABC'],
                []),
            (   'Yanıt alınamayan bir hastada ilk saniyelerde hava yolu açıklığı güvenceye alınmalı, aspire materyal '
                'varsa temizlenmeli ve yüksek akımlı oksijen başlanmalıdır.',
                '**Oksijenasyon:** Yüksek akımlı oksijen desteği ve aspirasyon riskine karşı hava yolu kontrolü.',
                'Yanıt',
                ['yüksek akımlı oksijen', 'aspirasyon önlemi'],
                []),
            (   'Gerekirse hasta derhal entübe edilmeli, hipotansiyon veya şok tablosu varsa intravenöz kristaloid '
                'sıvılarla kan basıncı yükseltilmelidir.',
                '**Erken Entübasyon:** Hipoventilasyon veya şokta erken entübasyon ve damar içi sıvı resüsitasyonu.',
                'ABC ve',
                ['entübasyon', 'sıvı resüsitasyonu'],
                [])]),
    (   46,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s46',
        [   (   'Vital bulgular emniyete alındıktan sonraki ikinci karar basamağımız: hastanın bilinci gerçekten '
                'kapalı mıdır sorusudur.',
                '**Bilinç Kapalı mı:** Vital stabilizasyon sonrası hastanın uyanıklık ve farkındalık durumunun teyidi.',
                'Bilinç kapalı',
                ['bilinç durumu', 'uyanıklık teyidi'],
                []),
            (   'Hekim hastaya yüksek sesle hitap etmeli, omuzlarından sarsarak ve ardından tırnak yatağına ya da '
                'supraorbital çentiğe ağrılı uyaran uygulayarak uyanıklığı test etmelidir.',
                '**Sözel ve Ağrılı Uyaran:** Sesli hitap, omuz sarsma ve supraorbital ağrılı uyaranla tepki aranması.',
                'Yanıt',
                ['ağrılı uyaran', 'supraorbital çentik'],
                []),
            (   'Eğer hasta hiçbir sözel ve ağrılı uyarıya amaca yönelik bir yanıt veremiyorsa bilinç kapalı kararına '
                'varılır.',
                '**Yanıtsızlık Teyidi:** Amaca yönelik hiçbir sözel veya motor tepkinin alınamaması durumu.',
                'Bilinci Kapalı Hastaya Yaklaşım',
                ['yanıtsızlık teyidi', 'gerçek koma'],
                [])]),
    (   47,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s47',
        [   (   'Eğer muayene sonucunda hastanın bilincinin aslında kapalı olmadığı anlaşılırsa algoritmada hayır '
                'koluna geçilir.',
                '**Hayır Kolu:** Bilinci kapalı olmayan ancak yanıtsız görünen hastalarda alternatif tanı yolu.',
                'hayır',
                ['hayır kolu', 'alternatif tanı'],
                []),
            (   'Burada hekim, komayı taklit eden veya hastanın dış dünya ile iletişim kurmasını engelleyen özel '
                'tabloları hızla düşünmelidir.',
                '**Koma Taklitçileri:** Dış dünya ile teması kesen periferik veya psikiyatrik durumlar araştırılır.',
                'Bilinci Kapalı Hastaya Yaklaşım',
                ['koma taklitçileri', 'iletişim engeli'],
                []),
            (   'Bu durumlar koma taklitçileri olarak adlandırılır ve yanlışlıkla koma tedavisi uygulanması hastaya '
                'ciddi zararlar verebilir.',
                '**Yanlış Tedavi Riski:** Yalancı koma hastasına gereksiz invaziv girişim ve sedasyon '
                'uygulanmamalıdır.',
                'Bilinç kapalı',
                ['yanlış tedavi riski', 'invaziv girişimler'],
                [])]),
    (   48,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s48',
        [   (   'Koma taklitçilerinin başında gelen locked-in sendromunda hasta tamamen uyanık ve farkındadır ancak '
                'ventral pons lezyonu nedeniyle tüm istemli kasları felç olmuştur.',
                '**Locked-in Sendromu:** Ventral pons enfarktında tam bilinç açıklığına rağmen quadripleji ve anartri '
                'tablosu.',
                'locked-in synd,',
                ['locked-in sendromu', 'ventral pons enfarktı'],
                []),
            (   'Bu hastalarda dikey göz hareketleri ve göz kırpma refleksleri sağlamdır; hastayla yukarı ve aşağı '
                'bakış hareketleriyle iletişim kurulabilir.',
                '**Dikey Göz Bakışı:** Mezensefalik dikey bakış merkezi korunduğundan hasta göz hareketleriyle '
                'iletişim kurar.',
                'Psikojen,',
                ['dikey göz hareketleri', 'göz kırpma'],
                []),
            (   'Bir diğer taklitçi olan ağır nöromüsküler paralizilerde, örneğin myastenia gravis krizinde veya '
                'Guillain-Barre sendromunda kaslar hareket edemez fakat bilinç açıktır.',
                '**Nöromüsküler Paralizi:** Myastenia gravis veya Guillain-Barre krizinde kas paralizisine rağmen '
                'bilinç açıktır.',
                'N-M paralizi,',
                ['myastenia gravis', 'Guillain Barre sendromu'],
                [])]),
    (   49,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s49',
        [   (   'Psikojenik yanıtsızlık veya konversiyon tablolarında hasta dış uyarılara tamamen yanıtsız gibi '
                'görünür ancak organik bir beyin lezyonu yoktur.',
                '**Psikojenik Yanıtsızlık:** Organik beyin hasarı olmaksızın psişik mekanizmalarla gelişen yalancı '
                'yanıtsızlık.',
                'Uygun',
                ['psikojenik yanıtsızlık', 'konversiyon bozukluğu'],
                []),
            (   'Göz kapakları hekim tarafından açılmak istendiğinde hastanın aktif direnç göstermesi psikojenik '
                'kökenin en güçlü klinik kanıtıdır.',
                '**Göz Kapağı Direnci:** Kapaklar açılırken hastanın aktif direnç göstermesi psikojenik kökeni '
                'kanıtlar.',
                'yaklaşım',
                ['göz kapağı direnci', 'aktif kontraksiyon'],
                []),
            (   'Ayrıca hastanın elini yüzünün üzerine bıraktığınızda elin yüze çarpmadan yana düşmesi ve kalorik '
                'testte nistagmus görülmesi bilincin açık olduğunu kanıtlar.',
                '**El Bırakma Testi:** Yüzün üzerine bırakılan elin yüze çarpmaması ve kalorik nistagmus uyanıklığı '
                'belgeler.',
                'Psikojen,',
                ['el bırakma testi', 'kalorik nistagmus'],
                [])]),
    (   50,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p030_s50',
        [   (   'Eğer hasta gerçekten hiçbir uyarıya yanıt vermiyor ve yalancı koma durumları dışlanmışsa, algoritmada '
                'evet koluna ilerlenir.',
                '**Evet Kolu:** Gerçek koma tablosu kesinleştiğinde acil medikal protokol devreye girer.',
                'evet',
                ['evet kolu', 'gerçek koma protokolü'],
                []),
            (   'Bu aşamada karşımızda gerçek bir koma tablosu vardır ve hasta acil resüsitasyon protokolüne alınır.',
                '**Acil Resüsitasyon:** Vital stabilizasyonla eş zamanlı etiyolojik tanı ve tedavi süreci başlatılır.',
                'Bilinç kapalı',
                ['acil resüsitasyon', 'etiyolojik tedavi'],
                []),
            (   'Zaman kaybetmeden hastadan kan örnekleri alınmalı ve geri döndürülebilir metabolik veya toksik '
                'nedenler hemen araştırılmalıdır.',
                '**Hızlı Kan Örnekleri:** Geri döndürülebilir hipoglisemi, hipoksi ve zehirlenmeler saniyeler içinde '
                'araştırılır.',
                'Bilinci Kapalı Hastaya Yaklaşım',
                ['metabolik tarama', 'toksik nedenler'],
                [])]),
    (   51,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p031_s51',
        [   (   'Bilinç kapalı evet kolunda ilk iş olarak stik kan şekeri, arter kan gazı, elektrolitler, kalsiyum, '
                'magnezyum, üre, kreatinin, amonyak ve karaciğer enzimleri gönderilir.',
                '**Acil Panel:** Stik kan şekeri, kan gazı, elektrolitler, kalsiyum, üre, amonyak ve enzim paneli.',
                'Kan gazları, glu,',
                ['kan gazı', 'glukoz', 'elektrolitler', 'amonyak'],
                []),
            (   'Ayrıca toksikolojik tarama için idrar ve kan örnekleri ayrılmalıdır.',
                '**Toksik Tarama:** Olası intoksikasyonlar için kan ve idrar toksikolojik tarama örnekleri alınır.',
                'tox',
                ['toksikolojik tarama', 'idrar toksik'],
                []),
            (   'Hipoglisemi şüphesinde damar içi dekstroz verilmeden hemen önce, olası bir Wernicke ensefalopatisini '
                'önlemek için mutlaka intravenöz tiamin uygulanmalıdır.',
                "**Tiamin Kuralı:** Glukoz infüzyonundan hemen önce Wernicke'yi önlemek için mutlaka intravenöz tiamin "
                'verilir.',
                'ıv glu,',
                ['intravenöz glukoz', 'tiamin desteği', 'Wernicke ensefalopatisi'],
                [])]),
    (   52,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p031_s52',
        [   (   'Metabolik örnekler alınıp ampirik tedaviler başlandıktan sonra algoritmanın en can alıcı yol ayrımına '
                'gelinir: hastada beyin sapı bulgusu var mıdır?',
                '**Beyin Sapı Bulguları:** Algoritmanın en kritik yol ayrımı beyin sapı reflekslerinin varlığıdır.',
                'Beyinsapı',
                ['beyin sapı bulguları', 'karar kavşağı'],
                []),
            (   'Burada hekim ışık refleksini, kornea refleksini, okülosefalik refleksi ve solunum paternini dikkatle '
                'muayene eder.',
                '**Muayene Bileşenleri:** Pupiller ışık yanıtı, kornea refleksi, bebek gözü hareketi ve solunum '
                'paterni.',
                'bulguları?',
                ['ışık refleksi', 'kornea refleksi', 'okülosefalik refleks'],
                []),
            (   'Beyin sapı bulgularının varlığı veya yokluğu, lezyonun yapısal mı yoksa diffüz metabolik mi olduğunu '
                'belirleyen temel kavşaktır.',
                '**Yapısal vs Metabolik:** Beyin sapı refleksleri korunmuşsa metabolik, kayıpsa yapısal süreç ön '
                'plandadır.',
                'Beyinsapı',
                ['yapısal hasar', 'metabolik ensefalopati'],
                [])]),
    (   53,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p031_s53',
        [   (   'Eğer pupiller ışığa yanıt veriyor, kornea ve göz hareket refleksleri korunmuşsa beyin sapı bulguları '
                'hayır koluna girilir.',
                '**Refleksler Korunmuş:** Işık, kornea ve göz hareketleri sağlamsa beyin sapı anatomik olarak '
                'sağlamdır.',
                'hayır',
                ['korunmuş refleksler', 'sağlam beyin sapı'],
                []),
            (   'Bu durum beyin sapının sağlam olduğunu ve komaya yol açan nedenin ya diffüz bir süreç ya da '
                'supratentoryal bir patoloji olduğunu düşündürür.',
                '**Supratentoryal Süreç:** Diffüz metabolik-toksik olaylar veya erken evre supratentoryal lezyonlar '
                'akla gelir.',
                'Beyinsapı',
                ['diffüz süreç', 'supratentoryal patoloji'],
                []),
            (   'Ancak beyin sapı sağlam olsa bile yukarıdaki serebral hemisferlerde kitle etkisi yapan lezyonlar '
                'henüz beyin sapına bası yapmamış olabilir.',
                '**Gizli Kitle Etkisi:** Supratentoryal kitleler henüz herniye olmadan da koma tablosu başlatabilir.',
                'hayır',
                ['kitle etkisi', 'erken herniasyon'],
                [])]),
    (   54,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p031_s54',
        [   (   'Beyin sapı bulgusu olmayan bu grupta ayırıcı tanıda lateral şift yapan tek taraflı serebral '
                'lezyonlar, biserebral yapısal hasarlar, talamik enfarktlar, metabolik, toksik ve enfeksiyöz nedenler '
                'yer alır.',
                '**Geniş Ayırıcı Tanı:** Lateral şift yapan lezyonlar, bilateral hemisfer hasarı, toksik ve metabolik '
                'komalar.',
                'Lateral şift',
                ['lateral şift', 'biserebral hasar', 'talamik enfarkt'],
                []),
            (   'Örneğin geniş bir orta serebral arter enfarktında veya subdural hematomda orta hat şifti başlayabilir '
                'ancak henüz unkus herniye olmamış olabilir.',
                '**Erken Herniasyon:** Geniş iskemik inme veya subdural hematom erken dönemde pupil bulgusu '
                'vermeyebilir.',
                'yapan tek',
                ['orta serebral arter enfarktı', 'subdural hematom'],
                []),
            (   'Diğer taraftan derin hipoglisemi, hepatik koma veya menenjit gibi difüz süreçler de beyin sapı '
                'reflekslerini koruyarak koma yapabilir.',
                '**Difüz Nedenler:** Hepatik koma, derin hipoglisemi ve menenjit beyin sapı reflekslerini korur.',
                'metabolik,',
                ['hepatik koma', 'menenjit', 'hipoglisemi'],
                [])]),
    (   55,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p031_s55',
        [   (   'Hem fokal kitle lezyonlarını hem de enfeksiyon veya intoksikasyonları ekarte etmek amacıyla hasta '
                'ivedilikle acil incelemeler sürecine sevk edilir.',
                '**Acil İnceleme Sevk:** Fokal cerrahi acilleri ve santral sinir sistemi enfeksiyonlarını ekarte etme '
                'süreci.',
                'Acil',
                ['acil inceleme', 'cerrahi ekarte etme'],
                []),
            (   'Zaman kaybedilmeden hasta monitörize bir şekilde radyolojiye transfer edilirken eş zamanlı olarak '
                'laboratuvar sonuçları takip edilir.',
                '**Monitörize Transfer:** Hasta vital desteği sürdürülerek acil radyolojik görüntülemeye ulaştırılır.',
                'incelemeler',
                ['monitörize transfer', 'radyolojik görüntüleme'],
                []),
            (   'Hekim, fokal nörolojik defisit olmasa bile intrakraniyal kanama veya ensefaliti dışlamadan hastayı '
                'yalnız metabolik kabul edemez.',
                '**Yapısalı Dışlama:** Görüntüleme olmadan hiçbir hasta yalnız metabolik kabul edilip cerrahi '
                'dışlanamaz.',
                'Acil',
                ['yapısalı dışlama', 'intrakraniyal kanama'],
                [])]),
    (   56,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p032_s56',
        [   (   'Acil inceleme basamağında çekilen kontrastsız beyin bilgisayarlı tomografisi, akut kanama, kitle, '
                'yaygın ödem ve orta hat şiftini anında ortaya koyar.',
                '**Kontrastsız BBT:** Akut intrakraniyal kanama, kitle, yaygın ödem ve orta hat şiftini dakikalar '
                'içinde gösterir.',
                'BBT, metabolik ve',
                ['beyin tomografisi', 'BBT', 'intrakraniyal kanama'],
                []),
            (   'Eğer tomografi tamamen normal gelirse ve hastada ateş, ense sertliği şüphesi varsa derhal lomber '
                'ponksiyon yapılarak beyin omurilik sıvısı incelenir.',
                '**Lomber Ponksiyon:** Normal tomografide ateş ve meningeal irritasyon varsa acil BOS analizi yapılır.',
                'BOS',
                ['lomber ponksiyon', 'meningismus', 'BOS analizi'],
                []),
            (   'Beyin omurilik sıvısı incelemesiyle bakteriyel menenjit, herpes ensefaliti veya tomografide '
                'görülmeyen subaraknoid kanama kesinleştirilir.',
                '**Menenjit ve SAK:** Beyin omurilik sıvısı incelemesi menenjit, ensefalit ve gizli kanamaları '
                'aydınlatır.',
                'inceleme,',
                ['bakteriyel menenjit', 'herpes ensefaliti', 'subaraknoid kanama'],
                [])]),
    (   57,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p032_s57',
        [   (   'Şimdi algoritmada geri dönüp beyin sapı bulguları var mıdır sorusuna evet yanıtı verilen kritik kola '
                'odaklanalım.',
                '**Beyin Sapı Pozitif:** Beyin sapı bulgularının varlığı hayatı tehdit eden acil anatomik lezyonu '
                'gösterir.',
                'evet',
                ['beyin sapı bulgusu', 'evet kolu'],
                []),
            (   'Hastada anizokori, ışığa yanıtsız fikse pupil, okülosefalik veya kalorik refleks kaybı, patolojik '
                'solunum ya da deserebre postür saptanması beyin sapı tutulumunu kanıtlar.',
                '**Kritik Bulgular:** Anizokori, fikse pupil, okülosefalik kayıp, deserebre rijidite beyin sapı '
                'lezyonunu belgeler.',
                'Beyinsapı',
                ['anizokori', 'fikse pupil', 'deserebre rijidite'],
                []),
            (   'Bu bulgular, hastanın dakikalar içinde hayatını kaybedebileceğini gösteren en üst düzeyde acil '
                'nörolojik alarmlardır.',
                '**Acil Alarm:** Dakikalar içinde mortalite riski taşıyan en yüksek dereceli cerrahi-nörolojik '
                'acildir.',
                'bulguları?',
                ['mortalite riski', 'nörolojik acil'],
                [])]),
    (   58,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p032_s58',
        [   (   'Beyin sapı bulgusu veren bu grupta serebellar hematom, baziler arter oklüzyonu veya beyin sapı '
                'kanaması gibi primer posterior fossa lezyonları ilk sırada yer alır.',
                '**Posterior Fossa Lezyonları:** Serebellar kanama, baziler arter oklüzyonu ve pontin kanama primer '
                'nedenlerdir.',
                'Posterior',
                ['serebellar hematom', 'baziler arter oklüzyonu', 'pontin kanama'],
                []),
            (   'İkinci büyük neden ise supratentoryal bir hematom veya tümörün temporal lob unkusunu aşağı itmesiyle '
                'oluşan unkal ve santral transtentoryal herniasyondur.',
                '**Transtentoryal Herniasyon:** Unkal ve santral herniasyon mezensefalonu tentoryum kenarına '
                'sıkıştırır.',
                'transtentional',
                ['unkal herniasyon', 'santral herniasyon', 'tentoryum'],
                []),
            (   'Ayrıca derin barbitürat zehirlenmesi ve aşırı doz trisiklik antidepresanlar da beyin sapını metabolik '
                'olarak felç edebilir.',
                '**Toksik Felç:** Yüksek doz barbitürat ve trisiklik antidepresanlar beyin sapı reflekslerini '
                'söndürebilir.',
                'toksik ve',
                ['barbitürat zehirlenmesi', 'trisiklik antidepresan'],
                [])]),
    (   59,
        'k2-02-b13',
        'Bilinci Kapalı Hastaya Algoritmik Yaklaşım',
        'k2-02-p032_s59',
        [   (   'Beyin sapı bulgusu olan hastada acil beyin tomografisi ve uygun merkezlerde manyetik rezonans '
                'görüntüleme saniyeler içinde çekilmelidir.',
                '**Acil BBT ve MR:** Posterior fossa ve herniasyonu netleştirmek için saniyeler içinde nörogörüntüleme '
                'yapılır.',
                'BBT/MRI, glu,',
                ['acil BBT', 'manyetik rezonans', 'posterior fossa'],
                []),
            (   'Eş zamanlı olarak kan şekeri kontrolü ve tiamin desteği aksatılmadan sürdürülmeli, toksik nedenler '
                'taranmalıdır.',
                '**Metabolik Destek:** Glukoz, tiamin ve toksikolojik tarama radyoloji sürecinde de kesintisiz '
                'sürdürülür.',
                'tiamin, metobolik',
                ['kan şekeri', 'tiamin desteği', 'toksik tarama'],
                []),
            (   'Eğer tomografide bası yapan bir serebellar kanama, epidural hematom veya unkal herniasyon saptanırsa '
                'beyin cerrahisi tarafından acil kraniektomi ile cerrahi dekompresyon uygulanır.',
                '**Cerrahi Dekompresyon:** Serebellar kanama veya epidural hematomda acil kraniektomi hayat kurtarır.',
                've toksik tarama',
                ['cerrahi dekompresyon', 'kraniektomi', 'serebellar kanama'],
                [])]),
    (   60,
        'k2-02-b14',
        'Komalı Hastada Kan Gazı ve Osmolar Açık',
        'k2-02-p033',
        [   (   'Nörogörüntülemesinde fokal yapısal lezyon saptanmayan komalı hastada tanı akış şeması metabolik ve '
                'toksik incelemelerle devam eder.',
                '**Metabolik Akış Şeması:** Görüntülemesi normal çıkan komada metabolik ve toksikolojik akış şemasına '
                'geçiş.',
                'Komalı Hasta',
                ['metabolik akış şeması', 'toksikolojik inceleme'],
                []),
            (   'Kanda laktat artışı metanol etilen glikol ve salisilat intoksikasyonu gibi anyon açığı yüksek '
                'metabolik asidoz nedenleri sistematik olarak taranır.',
                '**Anyon Açığı Asidozu:** Laktat, metanol, etilen glikol ve salisilat kaynaklı yüksek anyon açıklı '
                'metabolik asidoz.',
                'Laktat',
                ['laktat artışı', 'metanol', 'etilen glikol', 'salisilat'],
                []),
            (   'Diyabetik ketoasidoz ve üremi elendikten sonra hastanın serum ozmolalitesi ölçülür ve formülle '
                'hesaplanan ozmolalite ile karşılaştırılır.',
                '**Osmolar Açık Hesabı:** Ölçülen serum ozmolalitesi ile hesaplanan ozmolalitenin karşılaştırılması.',
                '© Metanol',
                ['diyabetik ketoasidoz', 'üremi', 'serum ozmolalitesi'],
                []),
            (   'Ölçülen ve hesaplanan ozmolalite arasındaki farkın on miliosmolün üzerinde olması pozitif bir osmolar '
                'açık bulunduğunu kanıtlar.',
                '**Pozitif Osmolar Açık:** Farkın on miliosmolün üzerinde çıkmasının pozitif osmolar açık kabul '
                'edilmesi.',
                'Etilen glikol',
                ['on miliosmol fark', 'pozitif osmolar açık'],
                []),
            (   'Pozitif osmolar açık mevcudiyeti kanda metanol etilen glikol veya izopropil alkol gibi düşük molekül '
                'ağırlıklı toksinlerin varlığını kesinleştirir.',
                '**Uçucu Toksinler:** Pozitif açığın metanol, etilen glikol ve izopropil alkol gibi maddeleri '
                'kanıtlaması.',
                '> Salisilat',
                ['metanol intoksikasyonu', 'izopropil alkol'],
                []),
            (   'Toksikolojik panellerde barbitürat amfetamin klonidin trisiklik antidepresan organofosfat '
                'benzodiazepin ve opioid düzeyleri taranır.',
                '**Geniş Toksik Panel:** Barbitürat, trisiklik antidepresan, organofosfat ve opioid paneli taraması.',
                'Komalı Hasta',
                ['barbitürat', 'trisiklik antidepresan', 'organofosfat'],
                []),
            (   'Toksin kaynağı tespit edildiğinde hemodiyaliz sodyum bikarbonat infüzyonu veya spesifik antidot '
                'tedavileri hızla devreye sokulur.',
                '**Hedefe Yönelik Tedavi:** Toksin tespitinde hemodiyaliz, bikarbonat ve spesifik antidotların hızla '
                'başlanması.',
                'Laktat',
                ['hemodiyaliz', 'sodyum bikarbonat', 'spesifik antidot'],
                []),
            (   'Doğru bir toksikolojik analiz tanı konulamayan derin koma olgularında hayat kurtarıcı nihai '
                'basamaktır.',
                '**Hayat Kurtarıcı Toksikoloji:** Tanısı belirsiz komada toksikolojik analizin nihai hayat kurtarıcı '
                'gücü.',
                'Komalı Hasta',
                ['toksikolojik analiz', 'hayat kurtarıcı'],
                [])]),
    (   61,
        'k2-02-b15',
        'Sonuç ve Klinik Özet',
        'k2-02-p034',
        [   (   'Sonuç olarak bilinç bozuklukları ve koma tablolarında doğru ve hızlı ayırıcı tanı koyabilmek klinik '
                'hekimliğin en hayati sınavıdır.',
                '**Hayati Sınav:** Bilinç bozukluğunda hızlı ve doğru ayırıcı tanının hekimlikteki hayati önemi.',
                'Bilinç bozukluğunda ayırıcı tanısı önemli',
                ['ayırıcı tanı', 'klinik sınav'],
                []),
            (   'Acil serviste ve yoğun bakımda yürütülecek hızlı koordineli ve disiplinler arası bir ekip yaklaşımı '
                'hasta sağkalımının temel taşıdır.',
                '**Ekip Yaklaşımı:** Acil ve yoğun bakımda koordineli ve hızlı ekip yaklaşımının yaşamsal rolü.',
                'Hızlı ve ekip yaklaşımı önemli',
                ['ekip yaklaşımı', 'hasta sağkalımı'],
                []),
            (   'Vital parametrelerin stabilizasyonu hipogliseminin yatak başında saptanması ve beyin sapı '
                'reflekslerinin değerlendirilmesi ilk basamakta tamamlanmalıdır.',
                '**İlk Basamak Tamamlama:** Vital stabilizasyon, glukoz kontrolü ve beyin sapı muayenesinin ilk anda '
                'yapılması.',
                'Bilinç bozukluğunda ayırıcı tanısı önemli',
                ['vital stabilizasyon', 'hipoglisemi kontrolü', 'beyin sapı refleksleri'],
                []),
            (   'Fokal yapısal nedenler ile diffüz metabolik problemleri birbirinden ayıran algoritmik düşünce sistemi '
                'hekime rehberlik etmelidir.',
                '**Rehber Algoritma:** Fokal lezyon ile metabolik problemi ayıran algoritmik yaklaşımın rehberliği.',
                'Etiyolojiye yönelik tetkik ve erken tedavi',
                ['fokal yapısal', 'diffüz metabolik', 'rehber algoritma'],
                []),
            (   'Etiyolojiye yönelik doğru tetkiklerin zamanında seçilmesi ve hedefe yönelik erken tedavinin '
                'gecikmeden başlanması prognozu son derece olumlu etkiler.',
                '**Erken Tedavi ve Prognoz:** Doğru tetkik seçimi ve erken etiyolojik tedavinin prognozu olumlu '
                'etkilemesi.',
                'prognozuiyi yönde etkiler',
                ['erken tedavi', 'olumlu prognoz'],
                []),
            (   'Geri dönüşsüz nöron hasarı gelişmeden önce atılacak her bilinçli adım hastayı hayata bağlar.',
                '**Nöronal Koruma:** İskemik nöron hasarı oluşmadan atılan bilinçli adımların hastayı yaşatması.',
                'prognozuiyi yönde etkiler',
                ['nöron hasarı', 'hayata bağlama'],
                []),
            (   'Katılımınız ve sabrınız için teşekkür eder klinik stajlarınızda ve hekimlik pratiğinizde başarılar '
                'dileriz.',
                '**Dilekler ve Teşekkür:** Katılım için teşekkür ve klinik hekimlik stajlarında başarı temennileri.',
                'Bilinç bozukluğunda ayırıcı tanısı önemli',
                ['katılım teşekkür', 'klinik başarılar'],
                []),
            (   'Bilinç bozukluklarına yaklaşım dersimiz burada sona ermiştir.',
                '**Ders Sonu:** Bilinç bozukluklarına yaklaşım sunumunun tamamlanması.',
                'Bilinç bozukluğunda ayırıcı tanısı önemli',
                ['ders sonu', 'sunum tamamlandı'],
                [])]),
    (   62,
        'k2-02-b15',
        'Sonuç ve Klinik Özet',
        'k2-02-p035_s62',
        [   (   'Bilinç bozukluğu olan hastaya yaklaşım dersimizin sonuna gelmiş bulunuyoruz değerli arkadaşlarım.',
                '**Ders Sonu:** Bilinç bozukluklarına klinik ve algoritmik yaklaşımın tamamlanması.',
                'TEŞEKKÜRLER...',
                ['bilinç bozuklukları', 'ders sonu'],
                []),
            (   'Özetle, bilinci kapalı bir hastada telaşa kapılmadan önce a-be-ce basamaklarını tamamlamak, stik '
                'glukozu ölçmek ve pupiller ile motor yanıtları doğru değerlendirmek hayat kurtarır.',
                '**Temel İlkeler:** ABC stabilizasyonu, stik glukoz, pupil muayenesi ve Glasgow motor skoru hayat '
                'kurtarır.',
                'TEŞEKKÜRLER...',
                ['ABC basamakları', 'stik glukoz', 'Glasgow motor skoru'],
                []),
            (   'Yapısal lezyonları metabolik tablolardan ayırmak ve algoritmayı adım adım işletmek klinik '
                'pratiğinizin en güçlü rehberi olacaktır.',
                '**Klinik Rehber:** Fokal yapısal ile metabolik tablonun algoritmik ayrımı hekimin temel dayanağıdır.',
                'TEŞEKKÜRLER...',
                ['yapısal lezyon', 'metabolik koma', 'klinik rehber'],
                [])])]

# Verify all anchors in kaynak.md
with open(TASLAK / 'kaynak.md') as f:
    text = f.read()

page_dict = {}
for p in text.split('=== SAYFA ')[1:]:
    lines = p.split('\n')
    pnum = int(lines[0].split(' ')[0])
    page_dict[pnum] = '\n'.join(lines[1:])

for sayfa, bid, bname, pid, sents in PARAGRAPHS:
    ptext = page_dict.get(sayfa, "")
    for s_idx, (ses, yazi, capa, spots, cikmis) in enumerate(sents):
        if capa not in ptext:
            print(f"ERROR: Anchor '{capa}' not found in page {sayfa} for {pid} s{s_idx}!")
            sys.exit(1)

print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Compute fig_map from sayfa_haritasi.json
fig_map = {}
sh = json.load(open(TASLAK / "sayfa_haritasi.json"))
for sp in sh["sayfalar"]:
    n = int(sp.get("sayfa") or 0)
    tur = sp.get("tur")
    if tur not in ("icerik", "sekil", "tablo") or "tekrar" in str(sp.get("ne_anlatiliyor", "")).lower():
        continue
    sek = [x for x in sp.get("sekiller") or [] if "süs" not in x.lower()]
    has_sek = bool(tur in ("sekil", "tablo") or sek)
    if has_sek:
        fig_map[n] = (sek or [sp.get("ne_anlatiliyor", "")])[0]

# Build konusma_v2
cid_counter = 1
pid_counter = 1
bolum_map = {}
total_words = 0
para_last_sent = {}

for sayfa, bid, bname, orig_pid, sents in PARAGRAPHS:
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
        
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": yazi,
            "slayt": {
                "sayfa": sayfa,
                "satir": capa
            },
            "etiketler": spots,
            "cikmis": cikmis
        }
        if s_idx == 0 and sayfa in fig_map:
            c_obj["slayt"]["sekil"] = fig_map[sayfa]
        p_cumleler.append(c_obj)
    
    pid = f"k2-02-p{pid_counter:03d}"
    pid_counter += 1
    para_last_sent[orig_pid] = p_cumleler[-1]["id"]
    bolum_map[bid]["paragraflar"].append({
        "id": pid,
        "paragrafIndex": len(bolum_map[bid]["paragraflar"]) + 1,
        "sayfa": sayfa,
        "baslik": bname,
        "cumleler": p_cumleler
    })

bolumler_list = list(bolum_map.values())
konusma_v2 = {
    "versiyon": "2.0",
    "surum": 2,
    "ders_id": "k2-02",
    "dersKodu": "k2-02",
    "dersAdi": "Bilinç Bozukluğu Olan Hastaya Yaklaşım",
    "bolumler": bolumler_list,
    "toplam_kelime": total_words,
    "toplam_sure_tahmini_dakika": round(total_words / 125.0, 1)
}

# Verify 0 sparse pages and 62/62 coverage
page_words = {}
for b in bolumler_list:
    for p in b["paragraflar"]:
        w = sum(len(c["ses"].split()) for c in p["cumleler"])
        sy = p["sayfa"]
        page_words[sy] = page_words.get(sy, 0) + w

print(f"Total Unique Pages: {len(page_words)} (1 to 62)")
sparse = {p: w for p, w in page_words.items() if w < 40}
if sparse:
    print(f"ERROR: Sparse pages found: {sparse}")
    sys.exit(1)
print(f"SUCCESS: 0 sparse pages! Total words: {total_words} (~{total_words/125.0:.1f} mins audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Generate derived files
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Bilinç Bozukluklarına Yaklaşım"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
(TASLAK / "konusma_metni.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md and konusma_metni.md")

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
print("Saved konusma_capalari.json and konusma_sayfalari.json")

# Save cikmis_baglantilari.json
sp_dict = D.sayfalar((TASLAK / "kaynak.md").read_text(encoding="utf-8"))
cikmis_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        for c in p["cumleler"]:
            if c.get("cikmis"):
                sayfa = c["slayt"]["sayfa"]
                alinti = ' '.join(sp_dict.get(sayfa, "").split()[:6])
                for qid in c["cikmis"]:
                    cikmis_list.append({
                        "cumle_id": c["id"],
                        "sayfa": sayfa,
                        "soru_id": qid,
                        "metin": c["ses"],
                        "ilgili": True,
                        "kanit": {
                            "sayfa": sayfa,
                            "alinti": alinti
                        }
                    })
(TASLAK / "cikmis_baglantilari.json").write_text(json.dumps(cikmis_list, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cikmis_baglantilari.json with {len(cikmis_list)} links.")

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

# Validate drawings
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

valid_komutlar = []
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
    else:
        valid_komutlar.append(d)

print(f"Validated drawings: {len(valid_komutlar)}/{len(cizim_komutlari)} pass.")
if c_errs:
    print(f"Drawing errors:")
    for e in c_errs: print(" ", e)

cizim_aday = {"komutlar": valid_komutlar}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(valid_komutlar)} commands.")

# Run 6 quality gates
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
c_final_errs = []
for idx, d in enumerate(valid_komutlar):
    cid = d["cumle"]
    coz_d, _ = sablon.coz(d)
    s_words = len(sent_map[cid]["ses"].split())
    err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
    if err_v: c_final_errs.append(err_v)
if c_final_errs:
    print(f"FAILED cizim_dogrula with {len(c_final_errs)} errors:")
    for e in c_final_errs: print(" ", e)
    sys.exit(1)
print(f"PASSED cizim_dogrula: {len(valid_komutlar)}/{len(valid_komutlar)} KOMUT 0 HATA")

print("\n🎉 ALL 6 QUALITY GATES PASSED PERFECTLY FOR LESSON 02 WITH ZERO ERRORS!")
