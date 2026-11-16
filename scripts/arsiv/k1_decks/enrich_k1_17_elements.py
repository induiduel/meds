# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 (hedef %10-20) oranına ulaşmasını sağlar.
"""

from scripts.k1_17_deck_data.helpers import (
    make_branching_logic, make_active_recall
)

def get_extra_branching():
    """Branching logic (klinik ve farmakoterapötik karar verme) oranını artırmak için eklenecek ögeler."""
    return {
        2: make_branching_logic(
            "Üretral akıntı şikayetiyle başvuran 24 yaşındaki erkek hastanın yayma preparatında lökositler içinde Gram negatif fasulye tanesi şeklinde diplokoklar görülüyor.",
            "Bu hastada antibiyotik direnci ve mikrobiyolojik etkenler dikkate alındığında hekimin vermesi gereken en uygun ampirik tedavi kararı nedir?",
            [
                {
                    "text": "Sadece tek doz oral amoksisilin verilerek hasta taburcu edilmelidir.",
                    "outcome": "Hatalı yaklaşım: Gonokoklar beta-laktamaz üretir, amoksisiline yüksek oranda dirençlidir.",
                    "isCorrect": False
                },
                {
                    "text": "Gonoreyi ve sıklıkla eşlik eden klamidyayı kapsamak üzere Seftriakson 250 mg İM tek doz + Azitromisin 1 g oral tek doz kombine verilmelidir.",
                    "outcome": "Kusursuz klinik karar: Gonokok ve klamidya eşzamanlı hedeflenir ve sefalosporin direncinin gelişimi engellenir.",
                    "isCorrect": True
                },
                {
                    "text": "İlaçsız izlem yapılmalı, hastaya sadece bol su içmesi söylenmelidir.",
                    "outcome": "Enfeksiyonun asendan yayılımına ve epididimite yol açacak ihmal.",
                    "isCorrect": False
                }
            ]
        ),
        4: make_branching_logic(
            "26 yaşındaki kadın hasta kötü kokulu, homojen gri-beyaz vajinal akıntı şikayetiyle başvuruyor. Spekülumda servikste eritem yok, vajinal pH 5.2 ölçülüyor ve KOH damlatıldığında balık kokusu yayılıyor.",
            "Vajinal yaymada clue cell (ipucu hücresi) saptanan bu hastada en uygun klinik yönetim kararı nedir?",
            [
                {
                    "text": "Bakteriyel vajinozis tanısıyla Metronidazol 500 mg oral 2x1 (7 gün) veya intravajinal jel başlanmalıdır; partner tedavisi gerekmez.",
                    "outcome": "Kusursuz klinik karar: Amsel kriterleri ile BV doğrulanır, anaerop florayı baskılamak için metronidazol verilir, partner tedavisi gerekmez.",
                    "isCorrect": True
                },
                {
                    "text": "Oral flukonazol 150 mg tek doz verilmeli ve cinsel partneri hastaneye yatırılmalıdır.",
                    "outcome": "Hatalı tedavi: Flukonazol mantar ilacıdır, BV bakteriyel/anaerop disbyozistir.",
                    "isCorrect": False
                },
                {
                    "text": "Yalnızca vajinal duş önerilmeli, antibiyotik verilmemelidir.",
                    "outcome": "Vajinal duş laktobasilleri daha da yok ederek disbyozisi şiddetlendirir.",
                    "isCorrect": False
                }
            ]
        ),
        6: make_branching_logic(
            "Bol sarı-yeşil renkli, köpüklü, kötü kokulu akıntı ve vulvar yanma şikayeti olan hastanın muayenesinde serviks üzerinde çilek manzarası (kolpitis makülaris) görülüyor.",
            "Islak preparatta hareketli kamçılı mikroorganizmalar görülen hastada tedavi ve partner yönetimi nasıl olmalıdır?",
            [
                {
                    "text": "Hastaya tek başına topikal nistatin krem verilmeli, partner bilgilendirilmemelidir.",
                    "outcome": "Hatalı yaklaşım: Trikomoniyazis paraziter bir enfeksiyondur ve mutlaka sistemik tedavi ve partner tedavisi gerektirir.",
                    "isCorrect": False
                },
                {
                    "text": "Trikomoniyazis tanısıyla hastaya Metronidazol 2 g oral tek doz verilmeli, cinsel partner de semptomsuz olsa bile eşzamanlı tedaviye alınmalı ve 7 gün cinsel perhiz uygulanmalıdır.",
                    "outcome": "Kusursuz klinik karar: Parazit sistemik metronidazol ile eradike edilir, ping-pong reenfeksiyonu önlenir.",
                    "isCorrect": True
                },
                {
                    "text": "Hasta derhal ameliyata alınarak servikal konizasyon yapılmalıdır.",
                    "outcome": "Paraziter enfeksiyonda gereksiz ve zararlı cerrahi girişim.",
                    "isCorrect": False
                }
            ]
        ),
        8: make_branching_logic(
            "Şiddetli vulvar kaşıntı ve beyaz süt kesiği kıvamında kokusuz akıntı ile başvuran hastanın vajinal pH'sı 4.2 bulunuyor. Islak preparatta tomurcuklanan mayalar ve psödohifler saptanıyor.",
            "Bu hastada etiyolojiye yönelik en rasyonel farmakolojik tedavi kararı nedir?",
            [
                {
                    "text": "Candida albicans vajiniti tanısıyla Flukonazol 150 mg oral tek doz (veya topikal azol ovül) verilmelidir; partner tedavisi rutin önerilmez.",
                    "outcome": "Kusursuz mikolojik yaklaşım: Normal asidik pH ve psödohif varlığında kandidiyazis doğru tedavi edilir.",
                    "isCorrect": True
                },
                {
                    "text": "Anaeropları öldürmek için Metronidazol 2 g tek doz verilmelidir.",
                    "outcome": "Metronidazol mantarlara etkisizdir.",
                    "isCorrect": False
                },
                {
                    "text": "Damar içi geniş spektrumlu karbapenem tedavisi başlanmalıdır.",
                    "outcome": "Aşırı ve endikasyonsuz antibiyotik kullanımı laktobasilleri öldürerek mantarı azdırır.",
                    "isCorrect": False
                }
            ]
        ),
        12: make_branching_logic(
            "Acil servise sarı pürülan üretral akıntı ve idrar yaparken şiddetli yanma ile başvuran 20 yaşındaki erkek hastada laboratuvarda Gram boyama sonucu hemen çıkmayacaktır.",
            "Sonuç beklenirken hastanın tedavisinde izlenmesi gereken ampirik protokol ne olmalıdır?",
            [
                {
                    "text": "Laboratuvar sonucu 3 gün sonra çıkana kadar hiçbir tedavi verilmemelidir.",
                    "outcome": "Hatalı erteleme: Akıntılı üretritte komplikasyon ve bulaşı önlemek için hemen sendromik tedavi başlanmalıdır.",
                    "isCorrect": False
                },
                {
                    "text": "Sendromik yaklaşım gereği hem gonoreyi hem klamidyayı kapsayacak şekilde Seftriakson 250 mg İM + Azitromisin 1 g oral tek doz derhal verilmelidir.",
                    "outcome": "Kusursuz acil tıp kararı: Hem N. gonorrhoeae hem C. trachomatis ampirik olarak güvenle kapsanır.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca idrar söktürücü çaylar verilerek hasta evine gönderilmelidir.",
                    "outcome": "Bakteriyel yayılıma ve epididimite zemin hazırlar.",
                    "isCorrect": False
                }
            ]
        ),
        15: make_branching_logic(
            "Şeffaf-mukoid üretral akıntısı olan erkek hastanın Gram yaymasında nötrofiller görülüyor ancak Gram negatif intraselüler diplokok saptanmıyor (Nongonokokal üretrit).",
            "Nongonokokal üretritin (NGU) en sık etkeni olan Chlamydia trachomatis'e yönelik ilk tercih tedavi kararı ne olmalıdır?",
            [
                {
                    "text": "Doksisiklin 100 mg oral 2x1 (7 gün) VEYA Azitromisin 1 g oral tek doz verilmelidir.",
                    "outcome": "Kusursuz farmakoterapötik karar: Klamidyaya karşı hücre içine penetre olan doksisiklin veya azitromisin birinci tercihtir.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca tek doz penisilin G enjeksiyonu yapılmalıdır.",
                    "outcome": "Klamidya hücre duvarında klasik peptidoglikan içermez, penisilin monoterapisine yanıtsızdır.",
                    "isCorrect": False
                },
                {
                    "text": "Amfoterisin B infüzyonu başlanmalıdır.",
                    "outcome": "Antifungal ajandır, bakteriyel üretritte yeri yoktur.",
                    "isCorrect": False
                }
            ]
        ),
        22: make_branching_logic(
            "Nongonokokal üretrit nedeniyle 7 gün doksisiklin ve ardından tek doz azitromisin kullanan ancak akıntı ve dizüri şikayeti nükseden 28 yaşındaki erkek hastada NAAT ile Mycoplasma genitalium saptanıyor.",
            "Makrolid direnci yüksek olan Mycoplasma genitalium için en uygun ikinci basamak tedavi kararı nedir?",
            [
                {
                    "text": "Hücre duvarı sentezini inhibe etmek için yüksek doz vankomisin verilmelidir.",
                    "outcome": "Mikoplazmaların hücre duvarı yoktur, vankomisin tamamen etkisizdir.",
                    "isCorrect": False
                },
                {
                    "text": "Dirençli olgularda florokinolon grubu Moksifloksasin 400 mg oral 1x1 (7-14 gün) başlanmalıdır.",
                    "outcome": "Kusursuz enfeksiyon yönetimi: Makrolid dirençli M. genitalium'da moksifloksasin kurtarma tedavisidir.",
                    "isCorrect": True
                },
                {
                    "text": "Tedavi tamamen kesilmeli ve cerrahi üretral dilatasyon yapılmalıdır.",
                    "outcome": "İatrojenik üretral darlık ve travma riski taşır.",
                    "isCorrect": False
                }
            ]
        ),
        25: make_branching_logic(
            "Genital akıntıdan izole edilen Ureaplasma urealyticum için antibiyotik duyarlılığı ve tedavi planlaması yapılıyor.",
            "Ureaplasma türlerinin hücre duvarı bulunmaması ve metabolik özellikleri göz önüne alındığında hangi antibiyotik sınıfı KESİNLİKLE etkisiz kalacaktır?",
            [
                {
                    "text": "Tetrasiklinler ve makrolidler",
                    "outcome": "Hatalı bilgi: Ureaplasma tedavisinde doksisiklin ve azitromisin etkilidir.",
                    "isCorrect": False
                },
                {
                    "text": "Beta-laktam antibiyotikler (penisilinler ve sefalosporinler) çünkü bakterinin peptidoglikan hücre duvarı yoktur.",
                    "outcome": "Kusursuz mikrobiyolojik çıkarım: Hücre duvarı olmayan mikroorganizmalarda beta-laktamlar hedefsizdir ve sıfır etkinlik gösterir.",
                    "isCorrect": True
                },
                {
                    "text": "Florokinolonlar",
                    "outcome": "Kinolonlar DNA girazı hedefler, Ureaplasma'da etkilidir.",
                    "isCorrect": False
                }
            ]
        ),
        32: make_branching_logic(
            "Rutin jinekolojik kontrolde vajinal akıntısında Trichomonas vaginalis trofozoitleri saptanan evli bir kadın hasta tedavi ediliyor. Eşinin hiçbir idrar veya genital şikayeti bulunmuyor.",
            "Asemptomatik eşin yönetimi konusunda hekimin vermesi gereken en doğru karar nedir?",
            [
                {
                    "text": "Eş semptomsuz olduğu için test veya tedaviye gerek yoktur.",
                    "outcome": "Ping-pong reenfeksiyonuna yol açacak ölümcül klinik hata! Erkeklerin %70'i asemptomatik taşıyıcıdır.",
                    "isCorrect": False
                },
                {
                    "text": "Eş semptomsuz olsa dahi prostat ve üretrasında trofozoit barındırabileceği için eşzamanlı olarak Metronidazol 2 g oral tek doz ile tedavi edilmeli ve 7 gün cinsel perhiz verilmelidir.",
                    "outcome": "Kusursuz epidemiyolojik karar: Asemptomatik partner mutlaka eşzamanlı tedavi edilerek bulaş zinciri kırılır.",
                    "isCorrect": True
                },
                {
                    "text": "Eşe yalnızca profilaktik idrar kültürü yapılmalı, üreme olursa 6 ay sonra tedavi verilmelidir.",
                    "outcome": "Gereksiz gecikme reenfeksiyonla sonuçlanır.",
                    "isCorrect": False
                }
            ]
        ),
        35: make_branching_logic(
            "Trikomoniyazis nedeniyle tek doz 2 g metronidazol alan bir hasta, ilacı aldıktan 4 saat sonra arkadaşlarıyla kutlamada 2 kadeh şarap içiyor. Yarım saat sonra şiddetli bulantı, kusma, göğüste çarpıntı ve yüzde kızarma ile acile geliyor.",
            "Acil hekiminin bu klinik tabloyu değerlendirmesi ve yaklaşımı ne olmalıdır?",
            [
                {
                    "text": "Hastada akut miyokard enfarktüsü gelişmiştir, hemen anjiyoya alınmalıdır.",
                    "outcome": "Hatalı teşhis: Tablo metronidazol-alkol etkileşimine bağlıdır.",
                    "isCorrect": False
                },
                {
                    "text": "Metronidazolün aldehit dehidrogenaz inhibisyonuna bağlı disülfiram benzeri reaksiyon gelişmiştir; hasta hidrate edilip semptomatik tedavi verilmeli ve metronidazol bittikten sonra en az 48 saat alkol almaması gerektiği vurgulanmalıdır.",
                    "outcome": "Kusursuz toksikolojik yaklaşım: Disülfiram reaksiyonu ve farmakokinetik etkileşim doğru yönetilir.",
                    "isCorrect": True
                },
                {
                    "text": "Alkol ilacın etkisini sıfırladığı için hastaya hemen 2 g metronidazol daha içirilmelidir.",
                    "outcome": "Zehirlenmeyi ve reaksiyonu daha da ölümcül hale getirecek vahim hata.",
                    "isCorrect": False
                }
            ]
        ),
        42: make_branching_logic(
            "Cinsel aktif 21 yaşındaki asemptomatik bir kadında rutin tarama testinde servikal NAAT ile Chlamydia trachomatis pozitif saptanıyor. Hasta şikayeti olmadığını belirterek ilaç almak istemiyor.",
            "Hekimin hastayı ikna etmek ve komplikasyonları önlemek için sunması gereken tıbbi gerekçe ne olmalıdır?",
            [
                {
                    "text": "Tedavi verilmeyip kendiliğinden geçmesi beklenmelidir.",
                    "outcome": "Klamidya sessizce asendan yayılarak pelvik enflamatuar hastalık ve tübal infertiliteye yol açar.",
                    "isCorrect": False
                },
                {
                    "text": "Klamidya kadınlarda %80-90 asemptomatik seyreder; tedavi edilmezse endometrit, salpenjit, pelvik abse, ektopik gebelik ve kalıcı tubal infertiliteye yol açtığı için tek doz azitromisin veya doksisiklin ile mutlaka tedavi edilmelidir.",
                    "outcome": "Kusursuz hasta eğitimi ve koruyucu hekimlik: Asendan tubal hasarın önlenmesi hayati önem taşır.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca gebelik planladığı ay antibiyotik alması gerektiği söylenmelidir.",
                    "outcome": "O zamana kadar tüpler tıkandığı için hasta infertil kalacaktır.",
                    "isCorrect": False
                }
            ]
        ),
        46: make_branching_logic(
            "Tropikal bölge seyahatinden dönen 32 yaşındaki erkekte kasıkta ağrılı lenfadenit ve Poupart ligamanının üstünde ve altında iki boğumlu lenf bezi büyümesi (Oluk belirtisi - Groove sign) saptanıyor.",
            "Chlamydia trachomatis L1-L3 serovarlarına bağlı Lenfogranüloma Venereum (LGV) şüphesinde tedavi süresi nasıl planlanmalıdır?",
            [
                {
                    "text": "Standart klamidya gibi sadece 1 gün tek doz azitromisin verilmesi yeterlidir.",
                    "outcome": "LGV lenfatik ve derin doku invazyonu yapar; tek doz tedavi kesinlikle yetersizdir.",
                    "isCorrect": False
                },
                {
                    "text": "LGV lenfatik invazyon gösterdiğinden Doksisiklin 100 mg oral 2x1 en az 21 gün (3 hafta) süreyle kesintisiz uygulanmalıdır.",
                    "outcome": "Kusursuz klinik karar: Lenfogranüloma venereumda 21 günlük tam doksisiklin kürü uygulanır.",
                    "isCorrect": True
                },
                {
                    "text": "Hemen cerrahi olarak tüm kasık lenf nodları çıkarılmalı, antibiyotik verilmemelidir.",
                    "outcome": "Lenfödem ve kalıcı fistüllere yol açacak gereksiz cerrahi.",
                    "isCorrect": False
                }
            ]
        ),
        52: make_branching_logic(
            "Kültürde saptanan Neisseria gonorrhoeae izolatının penisilinaz ürettiği ve siprofloksasine dirençli olduğu tespit ediliyor.",
            "Antibiyotik duyarlılık paternleri ve küresel direnç kılavuzları ışığında hastaya başlanacak rejim ne olmalıdır?",
            [
                {
                    "text": "Oral amoksisilin-klavulanat 1000 mg günde 2 kez 14 gün verilmelidir.",
                    "outcome": "Gonorede oral penisilin türevleri birinci basamakta önerilmez.",
                    "isCorrect": False
                },
                {
                    "text": "Seftriakson 250 mg İM tek doz + Azitromisin 1 g oral tek doz verilmelidir.",
                    "outcome": "Kusursuz kılavuz uyumu: 3. kuşak sefalosporin ve makrolid kombinasyonu ile direnç aşılır.",
                    "isCorrect": True
                },
                {
                    "text": "Yüksek doz oral siprofloksasin verilmelidir.",
                    "outcome": "Dirençli izolatta kinolon tedavisi başarısızlıkla sonuçlanır.",
                    "isCorrect": False
                }
            ]
        ),
        56: make_branching_logic(
            "24 yaşındaki kadın hasta yüksek ateş, el ve ayak bileklerinde gezici artrit, tenosinovit ve parmak uçlarında hemorajik püstüllerle acile başvuruyor (Dissemine Gonokokal Enfeksiyon - DGE).",
            "DGE düşünülen bu hastanın yatış ve parenteral tedavi kararı nasıl şekillenmelidir?",
            [
                {
                    "text": "Hasta ayaktan tek doz oral azitromisin verilerek evine gönderilmelidir.",
                    "outcome": "Dissemine gonore sepsise ve kalıcı eklem destruksiyonuna yol açabilir, ayaktan takip edilemez.",
                    "isCorrect": False
                },
                {
                    "text": "Hasta hastaneye yatırılmalı; Seftriakson 1 g IV/İM günde bir kez parenteral olarak başlanmalı ve klinik düzelmeden sonra oral tedaviye geçilerek toplam 7 gün tamamlanmalıdır.",
                    "outcome": "Kusursuz yataklı servis yönetimi: Dissemine gonorede parenteral seftriakson ile sepsis ve endokardit önlenir.",
                    "isCorrect": True
                },
                {
                    "text": "Tüm eklemleri ameliyatla protez ile değiştirilmelidir.",
                    "outcome": "Akut septik durumda kabul edilemez cerrahi girişim.",
                    "isCorrect": False
                }
            ]
        ),
        62: make_branching_logic(
            "Genç kadın hasta alt karın ağrısı, vajinal akıntı ve disparoni ile başvuruyor. Bimanuel muayenede belirgin servikal hareket hassasiyeti (frenk kelebeği / chandelier bulgusu) saptanıyor. Ateş 37.8°C, peritonit veya apse bulgusu yok.",
            "Hafif-orta şiddetteki bu ayaktan Pelvik Enflamatuar Hastalık (PİH) vakasında en uygun tedavi protokolü nedir?",
            [
                {
                    "text": "Seftriakson 250 mg İM tek doz + Doksisiklin 100 mg oral 2x1 (14 gün) ve anaeropları kapsamak üzere Metronidazol 500 mg oral 2x1 (14 gün) verilmelidir.",
                    "outcome": "Kusursuz PİH rejimi: Gonokok, klamidya ve anaerop florayı tam 14 gün boyunca kapsayan standart rejimdir.",
                    "isCorrect": True
                },
                {
                    "text": "Sadece tek bir ağrı kesici verilip hasta eve gönderilmelidir.",
                    "outcome": "Enfeksiyon ilerleyerek tuboovaryen apse ve sepsise dönüşür.",
                    "isCorrect": False
                },
                {
                    "text": "Yalnızca oral nistatin damla verilmelidir.",
                    "outcome": "PİH'te hiçbir etkinliği yoktur.",
                    "isCorrect": False
                }
            ]
        ),
        65: make_branching_logic(
            "PİH tanısı konulan bir hastanın pelvik ultrasonografisinde adneksiyal alanda 6 cm boyutunda kalın duvarlı, içi septalı kistik kitle (Tuboovaryan Apse) saptanıyor. Hastada yüksek ateş ve lökositoz mevcut.",
            "Tuboovaryan apse saptanan bu hastada hastaneye yatış ve parenteral antibiyotik seçimi nasıl olmalıdır?",
            [
                {
                    "text": "Hasta eve gönderilmeli, ayaktan günde bir kez azitromisin içmelidir.",
                    "outcome": "Apse rüptürü ve septik şokla ölümcül sonuçlanabilir.",
                    "isCorrect": False
                },
                {
                    "text": "Hasta derhal hastaneye yatırılmalı; IV Sefoksitin 2 g (6 saatte bir) + Doksisiklin 100 mg oral/IV (12 saatte bir) VEYA Klindamisin 900 mg IV + Gentamisin IV rejimlerinden biri başlanmalıdır.",
                    "outcome": "Kusursuz yoğun bakım/yataklı servis kararı: Tuboovaryen apsede anaerop kapsayıcılığı yüksek klindamisinli veya sefoksitinli parenteral rejim şarttır.",
                    "isCorrect": True
                },
                {
                    "text": "Hasta ameliyatsız ve antibiyotiksiz sadece buz tatbiki ile takip edilmelidir.",
                    "outcome": "Tıbbi tedavi standardına tamamen aykırıdır.",
                    "isCorrect": False
                }
            ]
        ),
        68: make_branching_logic(
            "26 yaşındaki cinsel aktif erkek hasta sağ testiste ani gelişen şiddetli ağrı, şişlik ve kızarıklık ile başvuruyor. Testis elevasyonu ile ağrı azalıyor (Prehn belirtisi pozitif). İdrar tahlilinde piyüri saptanıyor.",
            "35 yaş altı genç erkekte akut epididimitin en olası etkenleri ve ampirik tedavi kararı ne olmalıdır?",
            [
                {
                    "text": "C. trachomatis ve N. gonorrhoeae hedeflenerek Seftriakson 250 mg İM tek doz + Doksisiklin 100 mg oral 2x1 (10 gün) verilmelidir.",
                    "outcome": "Kusursuz ürolojik karar: 35 yaş altı cinsel aktif erkekte epididimitin başlıca etkenleri klamidya ve gonokoktur.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca tüberküloz ilacı verilmelidir.",
                    "outcome": "Akut başlangıçlı tabloda öncelikle bakteriyel CYBE hedeflenmelidir.",
                    "isCorrect": False
                },
                {
                    "text": "Testis derhal orşiektomi ile ameliyatla alınmalıdır.",
                    "outcome": "Antibiyotikle tam düzelen enfeksiyonda testisin gereksiz kaybı.",
                    "isCorrect": False
                }
            ]
        ),
        72: make_branching_logic(
            "Genital muayenede penis gövdesinde kenarları düzensiz, tabanı sarı-gri pürülan cerahatle kaplı, dokunulduğunda aşırı ağrılı yumuşak bir ülser ve sol kasıkta 4 cm'lik fluktuan bubon saptanan hastada Haemophilus ducreyi (Şankroid) düşünülüyor.",
            "Bu hastada antibiyotik tedavisi ve fluktuan bubonun yönetimi nasıl olmalıdır?",
            [
                {
                    "text": "Bubon neşterle kesilip açık bırakılmalı ve hiçbir antibiyotik verilmemelidir.",
                    "outcome": "Bubon insizyonu kronik fistül ve kalıcı ülserasyon yapar, kesinlikle yasaktır.",
                    "isCorrect": False
                },
                {
                    "text": "Azitromisin 1 g oral tek doz (veya Seftriakson 250 mg İM tek doz) verilmeli; fluktuan bubon kesilmemeli, gerekirse kalın uçlu iğne ile aspire edilmelidir.",
                    "outcome": "Kusursuz klinik ve cerrahi yaklaşım: Şankroid tek dozla kürlenir ve iğne aspirasyonu ile fistülleşme önlenir.",
                    "isCorrect": True
                },
                {
                    "text": "Hasta 1 yıl boyunca her gün penisilin iğnesi vurulmalıdır.",
                    "outcome": "H. ducreyi penisiline yanıtsızdır ve gereksiz uzun süredir.",
                    "isCorrect": False
                }
            ]
        ),
        76: make_branching_logic(
            "Genital bölgesinde 10 gün önce fark ettiği, kenarları ve tabanı kıkırdak gibi sert (endüre), yüzeyi temiz ve parlak, tamamen ağrısız tek bir ülser ve bilateral ağrısız sert kasık LAP'ı olan 30 yaşındaki hastada Primer Sifilis düşünülüyor.",
            "Tanı karanlık saha mikroskopisinde spiroketlerin görülmesiyle doğrulandığında ilk tercih tedavi kararı nedir?",
            [
                {
                    "text": "Oral siprofloksasin 500 mg tek doz verilmelidir.",
                    "outcome": "Kinolonlar sifiliste etkisizdir.",
                    "isCorrect": False
                },
                {
                    "text": "Benzatin Penisilin G 2.4 milyon ünite İM tek doz derin gluteal enjeksiyon olarak uygulanmalıdır.",
                    "outcome": "Kusursuz venerolojik karar: Erken sifilisin tartışmasız altın standart tedavisi tek doz Benzatin Penisilin G'dir.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca lezyon üzerine alkollü pamuk basılmalıdır.",
                    "outcome": "Sistemik spiroket yayılımını engelleyemez, sekonder ve nörosifilise yol açar.",
                    "isCorrect": False
                }
            ]
        ),
        82: make_branching_logic(
            "Genital bölgesinde kırmızı zemin üzerinde yeni çıkmış çok sayıda berrak su dolu vezikül ve patlamış ağrılı sığ ülserlerle başvuran hastada ateş ve kas ağrısı eşlik ediyor (Primer Genital Herpes).",
            "Bu hastada semptomların hafifletilmesi ve lezyonların iyileşmesi için hekimin vermesi gereken antiviral karar nedir?",
            [
                {
                    "text": "Antiviral verilmemeli, lezyonlar kendi haline bırakılmalıdır.",
                    "outcome": "Primer atak 3 hafta sürer ve şiddetli ağrı yapar; tedavi semptomları ve süreyi belirgin kısaltır.",
                    "isCorrect": False
                },
                {
                    "text": "Valasiklovir 1000 mg oral 2x1 (7-10 gün) VEYA Asiklovir 400 mg oral 3x1 (7-10 gün) başlanmalı; ilacın latent virüsü yok etmeyeceği hastaya anlatılmalıdır.",
                    "outcome": "Kusursuz farmakoterapi ve danışmanlık: Primer atakta nükleozid analoğu iyileşmeyi hızlandırır, hasta gerçekçi bilgilendirilir.",
                    "isCorrect": True
                },
                {
                    "text": "Hastalık kalıcı olarak yok edilsin diye hastaya 1 yıl aralıksız antibiyotik verilmelidir.",
                    "outcome": "Antiviraller latent virüsü eradike edemez ve antibiyotik virüse etki etmez.",
                    "isCorrect": False
                }
            ]
        ),
        86: make_branching_logic(
            "Son 1 yıl içinde 8 kez genital herpes atağı geçiren, her atakta şiddetli iş gücü kaybı ve psikoseksüel sıkıntı yaşayan 34 yaşındaki hastanın uzun dönemli yönetimi planlanıyor.",
            "Bu hastada atak sıklığını ve asemptomatik viral saçılımı baskılamak için en uygun strateji nedir?",
            [
                {
                    "text": "Yalnızca atak anında ağrı kesici jel kullanması söylenmelidir.",
                    "outcome": "Sık rekürrenste yaşam kalitesini düzeltmez ve partner bulaşını önlemez.",
                    "isCorrect": False
                },
                {
                    "text": "Kronik günlük süpresif tedavi endikasyonu vardır; Valasiklovir 500-1000 mg oral günde 1 kez kesintisiz başlanmalı ve 1 yıl sonra atak sıklığı tekrar değerlendirilmelidir.",
                    "outcome": "Kusursuz enfeksiyon kararı: Yılda 6 ve üzeri atakta günlük süpresyon atakları %75 azaltır ve partnere geçişi yarı yarıya düşürür.",
                    "isCorrect": True
                },
                {
                    "text": "Genital bölgedeki tüm sinirler cerrahi olarak kesilmelidir.",
                    "outcome": "Kalıcı paralizi ve duyu kaybı yaratacak sakatlayıcı uygulama.",
                    "isCorrect": False
                }
            ]
        ),
        88: make_branching_logic(
            "Vulvasında karnabahar görünümünde ağrısız siğilleri (kondiloma akuminata) olan 24 haftalık gebe hasta tedavi edilmek isteniyor.",
            "Gebelikte fetal güvenlilik göz önüne alındığında hekimin tedavi seçimi nasıl olmalıdır?",
            [
                {
                    "text": "Podofilotoksin çözeltisi reçete edilerek hastaya evde sürmesi söylenmelidir.",
                    "outcome": "Ölümcül hata: Podofilotoksin mikrotübül zehiridir ve gebelerde kesinlikle KONTRENDİKEDİR (teratojendir).",
                    "isCorrect": False
                },
                {
                    "text": "Podofilotoksin gibi teratojenlerden kaçınılmalı; gebelikte güvenli olan Kriyoterapi (sıvı azot) veya Triklorasetik asit (TCA %80-90) gibi hekim uygulamalı yöntemler tercih edilmelidir.",
                    "outcome": "Kusursuz obstetrik karar: Kriyoterapi ve TCA gebelikte sistemik toksisite yapmadan siğili güvenle temizler.",
                    "isCorrect": True
                },
                {
                    "text": "Gebelik boyunca hiçbir müdahale yapılmamalı, hasta lohusalık bitene kadar izole edilmelidir.",
                    "outcome": "Siğiller hızla büyüyüp kanama yapabilir; güvenli yöntemlerle tedavi edilmelidir.",
                    "isCorrect": False
                }
            ]
        ),
        92: make_branching_logic(
            "Üretrit tanısıyla Azitromisin 1 g tek doz alan bir erkek hasta, 'İlacımı bugün içtim, akşam nişanlımla ilişkiye girebilir miyim?' diye soruyor.",
            "Hekimin hastaya vermesi gereken en net ve bilimsel yanıt nedir?",
            [
                {
                    "text": "İlaç hemen kana karıştığı için ilişkiye girmesinde hiçbir sakınca yoktur.",
                    "outcome": "Vahim yanılgı: Mukozal saçılım günlerce devam eder ve nişanlısına bulaştırır.",
                    "isCorrect": False
                },
                {
                    "text": "Tek doz ilaç alınsa dahi dokulardan mikroorganizma temizlenene ve partnerinin de tedavisi tamamlanana kadar tam 7 gün boyunca kesinlikle cinsel ilişkide bulunmamalıdır.",
                    "outcome": "Kusursuz koruyucu hekimlik: 7 gün kuralı reenfeksiyonu ve enfeksiyon yayılımını önler.",
                    "isCorrect": True
                },
                {
                    "text": "Sadece gündüzleri ilişkiye girebilir, geceleri yasaktır.",
                    "outcome": "Tıbbi mantıktan uzak batıl inanç.",
                    "isCorrect": False
                }
            ]
        ),
        94: make_branching_logic(
            "18 haftalık gebe bir kadında Chlamydia trachomatis servikal enfeksiyonu saptanıyor. Normal şartlarda doksisiklin birinci tercihken gebelik söz konusudur.",
            "Bu gebe hastada hekimin yazması gereken birinci basamak güvenli tedavi rejimi hangisidir?",
            [
                {
                    "text": "Doksisiklin 100 mg 2x1 7 gün.",
                    "outcome": "Doksisiklin gebede kontrendikedir; fetal diş diskolorasyonu ve kemik hipoplazisi yapar.",
                    "isCorrect": False
                },
                {
                    "text": "Azitromisin 1 g oral tek doz (veya alternatif olarak Amoksisilin 500 mg oral 3x1 7 gün) verilmeli ve 3-4 hafta sonra NAAT ile kür testi yapılmalıdır.",
                    "outcome": "Kusursuz perinatal karar: Azitromisin gebelikte güvenlidir, doksisiklinin yerini alır ve kür testi ile teyit edilir.",
                    "isCorrect": True
                },
                {
                    "text": "Siprofloksasin 500 mg 2x1 14 gün.",
                    "outcome": "Kinolonlar gebede kıkırdak hasarı riski taşır, kontrendikedir.",
                    "isCorrect": False
                }
            ]
        ),
        96: make_branching_logic(
            "39 haftalık gebe kadında doğum sancıları başlıyor. Doğum kanalının muayenesinde vulva ve vajina girişinde çok sayıda yeni patlamış, ağrılı, aktif Herpes Simpleks vezikül ve ülserleri görülüyor.",
            "Neonatal herpes enfeksiyonunu ve yenidoğan ensefalitini önlemek için obstetrik ekibin alması gereken karar nedir?",
            [
                {
                    "text": "Normal vajinal doğum beklenmeli, bebeğin gözlerine su serpilmelidir.",
                    "outcome": "Bebek doğum kanalından geçerken herpes kapar; %50 mortaliteye sahip neonatal ensefalit gelişir.",
                    "isCorrect": False
                },
                {
                    "text": "Aktif lezyon varlığında doğum kanalından bulaşı engellemek için ACİLEN SEZARYEN DOĞUM yapılmalıdır.",
                    "outcome": "Kusursuz hayat kurtarıcı karar: Aktif genital herpes varlığında acil sezaryen mutlak endikasyondur.",
                    "isCorrect": True
                },
                {
                    "text": "Doğum 1 ay sonraya ertelenmelidir.",
                    "outcome": "Doğum eylemi başlamıştır, ertelenemez.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_recalls():
    """Active recall soru sayısını 25'e çıkararak çeşitliliği dengeleyen ögeler."""
    return {
        10: make_active_recall(
            "Gonokok enfeksiyonunun kesin tanısında şüpheli materyalin ekildiği ve %10 karbondioksitli ortamda inkübe edilen zenginleştirilmiş besiyerinin adı nedir?",
            "Thayer-Martin besiyeri (veya çukulata agar)",
            "Neisseria gonorrhoeae için seçici antibiyotikli besiyeri"
        ),
        16: make_active_recall(
            "Chlamydia trachomatis'in konak hücresi dışında enfeksiyöz olan ve hücre içine fagositozla giren metabolik olarak inaktif formuna ne ad verilir?",
            "Elementer cisimcik (EB - Elementary body)",
            "Klamidyanın hücre dışı bulaşıcı formu"
        ),
        18: make_active_recall(
            "Klamidyanın konak hücresi içinde çoğalan, metabolik olarak aktif ancak enfeksiyöz olmayan formuna ne ad verilir?",
            "Retiküler cisimcik (RB - Reticulate body)",
            "Klamidyanın hücre içi replikasyon formu"
        ),
        26: make_active_recall(
            "Hücre duvarı bulunmadığı için beta-laktam antibiyotiklere doğal olarak dirençli olan ve üreaz enzimiyle üreyi yıkarak enerji üreten mikoplazma türü hangisidir?",
            "Ureaplasma urealyticum",
            "Üreaz pozitif hücre duvarsız genital bakteri"
        ),
        36: make_active_recall(
            "Metronidazol tedavisi sırasında ve tedavi bitiminden sonraki 48 saat boyunca alkol alındığında ortaya çıkan şiddetli intolerans reaksiyonuna ne ad verilir?",
            "Disülfiram benzeri reaksiyon",
            "Asetaldehit birikimiyle oluşan taşikardi ve kusma tablosu"
        ),
        44: make_active_recall(
            "Genç kadınlarda Chlamydia trachomatis veya N. gonorrhoeae enfeksiyonunun karın içine yayılarak karaciğer kapsülünde 'keman teli' benzeri yapışıklıklar yapmasıyla karakterize perihepatit tablosuna ne ad verilir?",
            "Fitz-Hugh-Curtis sendromu",
            "PİH komplikasyonu olan keman teli perihepatiti"
        ),
        54: make_active_recall(
            "Neisseria gonorrhoeae'nin penisilinlere karşı gösterdiği direncin temelinde yatan ve ilacın beta-laktam halkasını parçalayan enzimin adı nedir?",
            "Beta-laktamaz (Penisilinaz)",
            "Beta-laktam halkasını hidrolize eden enzim"
        ),
        64: make_active_recall(
            "Bimanuel pelvik muayenede serviksin sağa-sola hareket ettirilmesiyle hastanın şiddetli ağrı duyarak zıplamasına neden olan patognomonik PİH bulgusuna ne ad verilir?",
            "Servikal hareket hassasiyeti (Chandelier bulgusu)",
            "Frenk kelebeği veya avize belirtisi"
        ),
        70: make_active_recall(
            "Akut epididimit ile testis torsiyonunu ayırt etmede kullanılan ve testisin yukarı kaldırılmasıyla epididimit ağrısının azalması bulgusuna ne ad verilir?",
            "Prehn belirtisi (pozitif Prehn)",
            "Testis elevasyonunda ağrının hafiflemesi"
        ),
        78: make_active_recall(
            "Sifilis tanısında kullanılan ve kardiyolipin antijenine karşı oluşan antikorları saptayan non-treponemal tarama testlerinin başlıcaları nelerdir?",
            "VDRL ve RPR",
            "Sifiliste tedavi takibinde titre düşüşü izlenen non-treponemal testler"
        ),
        84: make_active_recall(
            "Taze herpes vezikül tabanından kazıntı yapılarak hazırlanan ve multinükleer dev hücrelerin görüldüğü hızlı sitolojik boyama testine ne ad verilir?",
            "Tzanck yayması (Tzanck testi)",
            "Herpesvirüs sitopatolojisini gösteren boyama"
        ),
        90: make_active_recall(
            "Anogenital bölgede karnabahar benzeri ağrısız siğillerin (kondiloma akuminata) yüzde doksanından fazlasına neden olan düşük riskli HPV tipleri hangileridir?",
            "HPV tip 6 ve HPV tip 11",
            "Benign genital siğil etkeni HPV serotipleri"
        ),
        94: make_active_recall(
            "Gebelikte Chlamydia trachomatis enfeksiyonunun tedavisinde doksisiklin kontrendike olduğu için birinci tercih olarak kullanılan makrolid antibiyotik hangisidir?",
            "Azitromisin (tek doz 1 gram)",
            "Gebede güvenli tek doz klamidya ilacı"
        ),
        96: make_active_recall(
            "Yenidoğan bebeklerde doğum kanalından bulaşarak ilk 2-5 günde gelişen hiperakut pürülan konjonktiviti önlemek için doğumda göze sürülen pomadın etken maddesi nedir?",
            "Eritromisin (%0.5 oftalmik pomat)",
            "Doğumda uygulanan rutin göz profilaksisi"
        ),
        98: make_active_recall(
            "Cinsel yolla bulaşan bir enfeksiyon saptandığında hastada mutlaka eşzamanlı taranması gereken en kritik üç sistemik viral/bakteriyel enfeksiyon hangileridir?",
            "HIV, Sifilis ve Hepatit B (HBV)",
            "CYBE zemininde bulaş riski katlanan üçlü tarama paketi"
        ),
        100: make_active_recall(
            "CYBE tedavisi tamamlanan hem kadın hem erkek hastalara reenfeksiyonu ve ping-pong döngüsünü engellemek için önerilen zorunlu cinsel perhiz süresi kaç gündür?",
            "7 gün (bir hafta cinsel perhiz)",
            "Tek doz veya çoklu doz tedavi sonrası uyulması gereken perhiz süresi"
        )
    }

def apply_enrichment(slides):
    """Slayt listesine branching logic ve active recall ögelerini entegre eder."""
    extra_branching = get_extra_branching()
    extra_recalls = get_extra_recalls()
    
    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        if slide_num in extra_branching:
            slide.setdefault("elements", []).append(extra_branching[slide_num])
        if slide_num in extra_recalls:
            slide.setdefault("elements", []).append(extra_recalls[slide_num])
            
    return slides
