import sys, json, re, subprocess
from pathlib import Path

REPO_ROOT = Path('/home/indu/medsor')
TASLAK = REPO_ROOT / 'meds_database_25_26/taslak/y25-k2-01-norolojik-hastaya-yaklasim'

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
    # BOLUM 1: Sayfa 1
    (1, "k2-01-b01", "Nörolojik Yaklaşımın Temel İlkeleri ve Klinik Yöntem", "k2-01-p001", [
        (
            "Nörolojik hastaya klinik yaklaşım, sinir sisteminin karmaşık anatomik ve işlevsel hiyerarşisini adım adım çözümleyen sistematik bir tanı sürecidir.",
            "**Sistematik Tanı Süreci:** Sinir sistemi hiyerarşisini klinik verilerle adım adım çözümleme.",
            "NÖROLOJİK HASTAYA",
            ["nörolojik yaklaşım", "sistematik tanı", "anatomik hiyerarşi"],
            []
        ),
        (
            "Klinik nörolojide hekimin temel amacı iki ana soruya doğru yanıt bulmaktır; bunlardan birincisi lezyonun sinir sisteminin neresinde olduğu yani anatomik lokalizasyondur.",
            "**Birinci Temel Soru:** Lezyon sinir sisteminin neresinde? Anatomik lokalizasyon.",
            "YAKLAŞIM",
            ["temel amaç", "anatomik lokalizasyon", "lezyon yeri"],
            []
        ),
        (
            "İkinci temel soru ise bu bozukluğa yol açan patolojik sürecin ne olduğu yani lezyonun natürü ve etiyolojisidir.",
            "**İkinci Temel Soru:** Patolojik süreç ne? Lezyonun natürü ve etiyolojisi.",
            "NÖROLOJİK HASTAYA",
            ["patolojik süreç", "lezyonun natürü", "etiyoloji"],
            []
        ),
        (
            "Sinir sistemi serebral korteksten beyin sapına, medulla spinalisten spinal köklere, periferik sinirlere ve nöromüsküler kavşağa kadar uzanan kesintisiz bir anatomik ağ oluşturur.",
            "**Kesintisiz Ağ:** Korteksten kas kavşağına kadar uzanan anatomik hiyerarşi.",
            "YAKLAŞIM",
            ["serebral korteks", "medulla spinalis", "periferik sinir"],
            []
        ),
        (
            "Bu anatomik hiyerarşinin her bir düzeyi kendine özgü fizyolojik görevler üstlendiği için, ortaya çıkan nörolojik kayıp doğrudan hasarlanan bölgeyi işaret eder.",
            "**Fizyolojik Görev:** Her anatomik düzeyin kendine özgü klinik kayıp tablosu.",
            "NÖROLOJİK HASTAYA",
            ["fizyolojik düzey", "nörolojik kayıp"],
            []
        ),
        (
            "Örneğin serebral korteks hasarlarında fokal bilişsel ve lisan kayıpları görülürken, ön boynuz motor nöron lezyonlarında fasikülasyon ve arefleksi gibi alt motor nöron bulguları ortaya çıkar.",
            "**Hiyerarşik Kayıplar:** Kortikal hasarda lisan kaybı, ön boynuz lezyonunda fasikülasyon ve arefleksi.",
            "NÖROLOJİK HASTAYA",
            ["kortikal hasar", "ön boynuz", "fasikülasyon"],
            []
        ),
        (
            "Bu nedenle nörolojik değerlendirme ayrıntılı bir anamnez ile başlar ve bulguları birleştiren dikkatli bir nörolojik muayene ile devam eder.",
            "**Değerlendirme Akışı:** Ayrıntılı anamnez ile başlayıp nörolojik muayene ile devam eden süreç.",
            "Dr. İrfan YAVAŞ",
            ["anamnez", "nörolojik muayene"],
            []
        ),
        (
            "Elde edilen klinik veriler sendromik bir bütünlüğe oturtulduktan sonra, en uygun laboratuvar ve görüntüleme yöntemleri seçilerek kesin tanıya ulaşılır.",
            "**Sendromik Bütünlük:** Verilerin sendroma oturtulması ve hedefe yönelik tetkik seçimi.",
            "NÖROLOJİK HASTAYA",
            ["sendromik bütünlük", "tetkik seçimi"],
            []
        ),
        (
            "Hiçbir modern teknolojik tetkik, hastayı dinleyerek ve muayene ederek kurulan klinik muhakemenin yerini tutamaz ve plansız tetkik istemi tanı sürecinde yalnızca zaman kaybettirir.",
            "**Klinik Muhakeme:** Plansız teknolojik tetkiklerin klinik muhakemenin yerini tutamayacağı ilkesi.",
            "YAKLAŞIM",
            ["klinik muhakeme", "teknolojik tetkik"],
            []
        )
    ]),

    # BOLUM 2: Sayfa 2 (1. Paragraf)
    (2, "k2-01-b02", "Nörolojide Anamnezin Önemi ve Yakınmaların Sorgulanması", "k2-01-p002", [
        (
            "Ünlü nörolog Merritt, hastayı dinledikten sonra nesi olduğunu anlamadıysanız muayene ettikten sonra da anlamayacaksınız diyerek öykünün tanıdaki belirleyici yerini ortaya koymuştur.",
            "**Merritt İlkesi:** Hastayı dinledikten sonra anlamadıysanız muayenede de anlamayacaksınız.",
            "«Hastayı dinledikten sonra nesi olduğunu anlamadıysanız",
            ["Merritt", "öykünün önemi", "anamnez ilkesi"],
            []
        ),
        (
            "Gerçekten de iyi alınan bir anamnez, hekime hastanın sorunu hakkında doğru bir yönelim ve rasyonel bir klinik yaklaşım sağlar.",
            "**Doğru Yönelim:** İyi anamnezin sağladığı tanısal yönelim ve klinik yaklaşım.",
            "• İyi bir anamnez doğru bir yönelim ve yaklaşım sağlar",
            ["iyi anamnez", "doğru yönelim"],
            []
        ),
        (
            "Hastanın temel yakınması, belirtilerin başlangıç şekli ve zaman içindeki kronolojik gidişi, anatomik lokalizasyon ve etiyoloji yönünden problemi büyük ölçüde aydınlatır.",
            "**Kronolojik Gidiş:** Başlangıç şekli ve zaman çizelgesinin lokalizasyon ve etiyolojideki rolü.",
            "• Hastanın yakınması, belirtilerin başlangıç şekli, kronolojik gidişi anatomik",
            ["başlangıç şekli", "kronolojik gidiş"],
            []
        ),
        (
            "Örneğin saniyeler içinde gelişen bir belirti damarsal bir oklüzyonu ya da elektriksel bir deşarjı düşündürürken, aylara yayılan ilerleyici bir tablo büyüyen bir kitleyi veya nörodejenerasyonu işaret eder.",
            "**Zamanlama İpucu:** Saniyeler içinde damarsal olay, aylara yayılan kitle lezyonu.",
            "lokalizasyon ve etyoloji yönünden problemi büyük ölçüde aydınlatır",
            ["damarsal olay", "kitle lezyonu"],
            []
        ),
        (
            "Hastanın öyküsü alınırken kullandığı kelimelerle gerçekte neyi kastettiğini anlamak tanı açısından kritik bir gerekliliktir.",
            "**Kelime Anlamı:** Hastanın kullandığı kelimelerle neyi kastettiğini tam anlama zorunluluğu.",
            "• Hastanın öyküsü alınırken kullandığı kelimelerle neyi kasdettiğini anlamak çok",
            ["hasta dili", "kelime anlamı"],
            []
        ),
        (
            "Çünkü hastalar tıbbi kavramları günlük dildeki alışkanlıklarıyla çok farklı anlamlarda kullanabilirler ve bu ifadeler derinlemesine sorgulanmadan kayda geçirilirse hekimi yanlış bir anatomik lokalizasyona götürebilir.",
            "**Yanıltıcı İfadeler:** Günlük dil alışkanlıklarının hekimi yanlış lokalizasyona götürme riski.",
            "önemli.",
            ["günlük dil", "yanlış lokalizasyon"],
            []
        ),
        (
            "Somut bir örnek olarak, hastanın kolumda veya bacağımda uyuşma var demesi gerçek bir duyu kusuru olabileceği gibi aslında motor bir kuvvet kaybını da anlatıyor olabilir.",
            "**Uyuşma Ayrımı:** Uyuşma ifadesinin duyu kusuru veya motor kuvvet kaybı olabilmesi.",
            "• «Uyuşma» duyu kusuru olabilir ya da kuvvet kaybını anlatıyor olabilir",
            ["uyuşma", "duyu kusuru", "kuvvet kaybı"],
            []
        ),
        (
            "Bu ayrımı netleştirmek için hastaya dokunulanı mı hissetmediği, yoksa elindeki bardağı tutmakta veya merdiven çıkarken ayağını kaldırmakta mı güçlük çektiği somut sorularla açıkça sorgulanmalıdır.",
            "**Netleştirici Sorular:** Hissizlik mi yoksa bardağı tutamama gibi motor güçsüzlük mü?",
            "• «Uyuşma» duyu kusuru olabilir ya da kuvvet kaybını anlatıyor olabilir",
            ["dokunma hissi", "motor güçsüzlük"],
            []
        )
    ]),

    # BOLUM 2: Sayfa 2 (2. Paragraf)
    (2, "k2-01-b02", "Nörolojide Anamnezin Önemi ve Yakınmaların Sorgulanması", "k2-01-p003", [
        (
            "Benzer biçimde ağrı tamamen sübjektif bir yakınmadır ve yönlendirici olmayan dikkatli sorularla tüm nitelikleri tek tek ortaya konmalıdır.",
            "**Sübjektif Ağrı:** Yönlendirici olmayan sorularla ağrının niteliklerinin ortaya konması.",
            "• Ağrı sübjektif, sorularla nitelikleri ortaya konmalı",
            ["sübjektif ağrı", "ağrı niteliği"],
            []
        ),
        (
            "Ağrının anatomik lokalizasyonu, yayılım trasesi, zonklayıcı veya şimşek çakar tarzda oluşu, süresi ve tetikleyici faktörleri sorgulanarak spesifik ağrı sendromları birbirinden ayırt edilir.",
            "**Ağrı Karakteri:** Lokalizasyon, yayılım, zonklayıcı veya şimşek çakar karakter ve tetikleyiciler.",
            "• Ağrı sübjektif, sorularla nitelikleri ortaya konmalı",
            ["zonklayıcı ağrı", "şimşek çakar ağrı"],
            []
        ),
        (
            "Özellikle hastanın yaşamındaki en şiddetli baş ağrısı şeklinde tanımladığı ani patlayıcı gök gürültüsü ağrısında rüptüre anevrizmaya bağlı subaraknoid kanama mutlaka ilk sırada düşünülmelidir.",
            "**En Şiddetli Ağrı:** Hayatın en şiddetli baş ağrısı tanımında subaraknoid kanama önceliği.",
            "• Ağrı sübjektif, sorularla nitelikleri ortaya konmalı",
            ["en şiddetli ağrı", "subaraknoid kanama"],
            []
        ),
        (
            "Hekim, hastanın esas sıkıntısının ne olduğunu ve ne söylemek istediğini tam olarak anlamadan nörolojik muayeneye geçmemelidir.",
            "**Sıkıntıyı Anlama:** Hastanın esas derdini anlamadan fizik muayeneye geçmeme kuralı.",
            "• Hekim hastanın «sıkıntı»sının ne olduğunu, ne söylemek istediğini anlamadan",
            ["hastanın sıkıntısı", "muayeneye geçiş"],
            []
        ),
        (
            "Çünkü öyküden elde edilen ön tanı hipotezleri, muayene sırasında hangi nörolojik sistemin daha derinlemesine inceleneceğini doğrudan belirler.",
            "**Hedefe Yönelik Muayene:** Anamnez hipotezlerinin muayene derinliğini belirlemesi.",
            "muayeneye geçmemelidir.",
            ["hedefe yönelik muayene", "ön tanı hipotezi"],
            []
        ),
        (
            "Ayrıca hekim ile hastanın ortak bir zeminde buluşması, hastanın beklentilerinin ve duygularının anlaşılması tanısal doğruluğu ve tedaviye uyumu büyük ölçüde artırır.",
            "**Hasta Uyumu:** Ortak zeminde buluşmanın tanısal doğruluğu ve hasta uyumunu artırması.",
            "• Hekim hastanın «sıkıntı»sının ne olduğunu, ne söylemek istediğini anlamadan",
            ["hasta uyumu", "ortak zemin"],
            []
        ),
        (
            "Eğer hasta bilinçsiz ise ya da afazi gibi ağır bir konuşma bozukluğu varsa, anamnez mutlaka hastanın yakınından ya da onu hastaneye getiren kişiden alınmalıdır.",
            "**Yakınından Öykü:** Bilinçsiz veya afazik hastada refakatçiden ve getiren kişiden anamnez alma.",
            "• Hasta bilinçsiz, ya da konuşma bozukluğu varsa yakını ya da getiren kişiden",
            ["bilinçsiz hasta", "afazi", "refakatçi öyküsü"],
            []
        ),
        (
            "Epileptik nöbet, senkop veya akut konfüzyon gibi hastanın atak anını hatırlayamadığı durumlarda da olaya tanıklık eden kişilerin gözlemleri doğru teşhis için vazgeçilmezdir.",
            "**Tanık Gözlemi:** Nöbet veya senkopta olaya tanıklık edenlerin gözlemlerinin vazgeçilmezliği.",
            "• Hasta bilinçsiz, ya da konuşma bozukluğu varsa yakını ya da getiren kişiden",
            ["tanık gözlemi", "epileptik nöbet", "senkop"],
            []
        )
    ]),

    # BOLUM 3: Sayfa 3 (1. Paragraf)
    (3, "k2-01-b03", "Hastalıklarda Başlangıç Şekli, Doğal Gidiş ve Öyküyle Tanı", "k2-01-p004", [
        (
            "Nörolojik hastalıklarda belirtilerin başlayış şekli ve zaman içindeki doğal gidişi etiyolojik tanının en kilit belirleyicisidir.",
            "**Başlayış Şekli:** Belirtilerin başlangıç hızı ve doğal seyrinin etiyolojik belirleyiciliği.",
            "Nörolojik Hastalıklarda Başlayış Şekli ve Doğal Gidiş",
            ["başlayış şekli", "doğal gidiş"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: akut başlangıçlı nörolojik hastalıklar dakikalar veya saatler içinde hızla yerleşir ve bunun en tipik klinik örneği serebrovasküler tıkanıklığa bağlı hemiplejidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Dakika veya saat içinde akut yerleşen tablo hemiplejidir.",
            "• Akut başlangıç. Dakika veya saat içinde. Örneğin hemipleji.",
            ["çıkmış sınav sorusu", "akut başlangıç", "hemipleji"],
            ["q-2__kurul_-1"]
        ),
        (
            "Dakikalar içinde aniden ortaya çıkan motor defisit veya konuşma kaybı, serebral damar tıkanıklığını, kanamayı veya fokal epileptik deşarjı doğrudan yansıtır.",
            "**Hiperakut Olaylar:** Vasküler oklüzyon ve rüptürün dakikalar içinde motor defisit oluşturması.",
            "• Akut başlangıç. Dakika veya saat içinde. Örneğin hemipleji.",
            ["vasküler oklüzyon", "motor defisit"],
            []
        ),
        (
            "Buna karşılık bazı nörolojik hastalıklar son derece sinsi başlar ve belirtiler haftalar, aylar hatta yıllar içinde yavaş yavaş yerleşir.",
            "**Sinsi Başlangıç:** Haftalar, aylar ve yıllar içinde yavaş yerleşen nörolojik patolojiler.",
            "• Bazı hastalıklar sinsi başlar. Haftalar, aylar, yıllar içinde yerleşir. Beyin tümörü,",
            ["sinsi başlangıç", "kronik seyir"],
            []
        ),
        (
            "Haftalar veya aylar içinde basamaklı ya da sürekli ilerleyen nörolojik kayıplarda primer beyin tümörleri veya kronik subdural hematom gibi yer kaplayıcı lezyonlar akla gelmelidir.",
            "**Tümör Seyri:** Haftalar-aylar içinde ilerleyen yer kaplayıcı kitle lezyonları.",
            "dejeneratif hastalıklar gibi",
            ["beyin tümörü", "yer kaplayıcı lezyon"],
            []
        ),
        (
            "Yıllar boyunca yavaş ve kesintisiz kötüleşen sinsi klinik tablolar ise Alzheimer veya Parkinson hastalığı gibi nörodejeneratif süreçleri işaret eder.",
            "**Nörodejeneratif Süreç:** Yıllara yayılan ilerleyici dejeneratif hastalıklar.",
            "dejeneratif hastalıklar gibi",
            ["nörodejeneratif hastalık", "Alzheimer", "Parkinson"],
            []
        ),
        (
            "Nörolojide bir diğer temel seyir tipi, kötüleşme ve iyileşme dönemlerinin birbirini izlediği dalgalı gidiştir.",
            "**Dalgalı Gidiş:** Kötüleşme ve iyileşme dönemlerinin birbirini izlediği klinik seyir.",
            "• Dalgalı gidiş. Kötüleşme ve iyileşme dönemleri vardır. Relapsing-remitting MS",
            ["dalgalı gidiş", "remisyon", "atak"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: kötüleşme ve iyileşme dönemleri gösteren bu dalgalı gidişin klinikteki en klasik örneği yineleyici düzelen multipl sklerozdur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Atak ve iyileşmelerle dalgalı giden tablo relapsing-remitting multipl sklerozdur.",
            "• Dalgalı gidiş. Kötüleşme ve iyileşme dönemleri vardır. Relapsing-remitting MS",
            ["çıkmış sınav sorusu", "multipl skleroz", "dalgalı seyir"],
            ["4c4eb178b88b", "4ba07c308e35"]
        )
    ]),

    # BOLUM 3: Sayfa 3 (2. Paragraf)
    (3, "k2-01-b03", "Hastalıklarda Başlangıç Şekli, Doğal Gidiş ve Öyküyle Tanı", "k2-01-p005", [
        (
            "Hastalığın doğal gidişini doğru anlamak, sadece tanı koymak açısından değil, uygulanan tedavi sonuçlarının değerlendirilmesi bakımından da son derece önemlidir.",
            "**Tedavi Değerlendirmesi:** Doğal seyrin tedavi etkinliğini ölçmedeki belirleyici rolü.",
            "• Hastalığın doğal gidişi tanı yönünden olduğu kadar tedavi sonuçlarının",
            ["tedavi sonuçları", "doğal gidiş"],
            []
        ),
        (
            "Çünkü tedavi başlanan bir hastada görülen klinik düzelmenin, ilacın farmakolojik etkisine mi bağlı olduğu yoksa hastalığın kendi doğal seyrindeki remisyona mı ait olduğu titizlikle ayırt edilmelidir.",
            "**Tedavi mi Doğal Seyir mi?:** Klinik düzelmenin ilaca mı yoksa spontan remisyona mı bağlı olduğunun ayrımı.",
            "değerlendirilmesi bakımından da önemlidir",
            ["ilaç etkisi", "spontan remisyon"],
            []
        ),
        (
            "Örneğin multipl skleroz atağı geçiren bir hasta tedavi verilmese dahi haftalar içinde spontan bir remisyona girip kısmen veya tamamen düzelebilir.",
            "**Spontan İyileşme:** Multipl skleroz ataklarında tedavisiz spontan remisyon eğilimi.",
            "• Düzelme uygulanan tedaviye mi bağlı yoksa doğal seyrine mi?",
            ["multipl skleroz", "spontan düzelme"],
            []
        ),
        (
            "Eğer hekim hastalığın bu doğal remisyon eğilimini bilmezse, hastaya verilen herhangi bir ilacın veya deneysel uygulamanın mucizevi bir iyileşme sağladığı yanılgısına düşebilir.",
            "**Plasebo ve Yanılgı:** Doğal remisyonu bilmeyen hekimin ilaca haksız başarı atfetme yanılgısı.",
            "• Düzelme uygulanan tedaviye mi bağlı yoksa doğal seyrine mi?",
            ["ilaç yanılgısı", "tedavi etkinliği"],
            []
        ),
        (
            "Aynı şekilde periferik fasiyal paralizi olan Bell felcinde de hastaların büyük çoğunluğu steroid tedavisi alsın veya almasın ilk üç haftada belirgin klinik düzelme gösterir.",
            "**Bell Felci Seyri:** Periferik fasiyal paralizide ilk üç haftadaki yüksek spontan iyileşme oranı.",
            "• Düzelme uygulanan tedaviye mi bağlı yoksa doğal seyrine mi?",
            ["Bell felci", "fasiyal paralizi"],
            []
        ),
        (
            "Dolayısıyla bir tedavinin gerçek etkinliğini kanıtlamak için, hastalığın tedavi edilmeyen kontrol grubundaki doğal seyriyle karşılaştırılması bilimsel bir zorunluluktur.",
            "**Bilimsel Karşılaştırma:** Tedavi grubunun tedavi edilmeyen doğal seyir kontrolü ile kıyaslanması.",
            "• Hastalığın doğal gidişi tanı yönünden olduğu kadar tedavi sonuçlarının",
            ["kontrol grubu", "bilimsel kanıt"],
            []
        ),
        (
            "Tedaviye verilen yanıtın objektif parametrelerle ölçülmesi, gereksiz ve toksik ilaçların uzun süre kullanımını önlemede hekime yol gösterir.",
            "**Toksisiteyi Önleme:** Objektif değerlendirme ile etkisiz ve toksik ilaç kullanımını engelleme.",
            "değerlendirilmesi bakımından da önemlidir",
            ["objektif parametre", "ilaç toksisitesi"],
            []
        ),
        (
            "Hastalığın gidişatını öngörebilen bir hekim, hem hasta ve ailesine doğru bir prognoz verebilir hem de gerçekçi tedavi hedefleri koyabilir.",
            "**Gerçekçi Prognoz:** Hastalığın seyrini bilerek gerçekçi tedavi ve prognoz hedefleri belirleme.",
            "• Hastalığın doğal gidişi tanı yönünden olduğu kadar tedavi sonuçlarının",
            ["prognoz", "tedavi hedefleri"],
            []
        )
    ]),

    # BOLUM 4: Sayfa 4
    (4, "k2-01-b04", "Tanısı Öyküye Dayanan Nörolojik Hastalıklar", "k2-01-p006", [
        (
            "Klinik nörolojide bazı hastalıklar vardır ki, bunların tanısı tamamen ve sadece hastadan alınan ayrıntılı öyküye dayanır.",
            "**Öykü Tanısı:** Tanısı tamamen ve sadece hastadan alınan anamneze dayanan hastalıklar.",
            "Tanısı Öyküye Dayanan Nörolojik Hastalıklar",
            ["öykü tanısı", "anamnez"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: tanısı esas olarak hastadan alınan klinik öyküye dayanan hastalıkların başında migren ve trigeminal nevralji gelmektedir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Tanısı esas olarak anamneze dayanan hastalık migrendir.",
            "• Migren",
            ["çıkmış sınav sorusu", "migren", "trigeminal nevralji"],
            ["past-1790877039274-141162"]
        ),
        (
            "Migren hastasında ataklar arasında yapılan fizik muayenede, rutin laboratuvar testlerinde ve beyin görüntülemelerinde hiçbir patolojik bulguya rastlanmaz.",
            "**Ataklar Arası Normallik:** Migrende fizik muayene, laboratuvar ve radyolojinin tamamen normal olması.",
            "• Nörolojik belirti, lab. bulgusu yoktur",
            ["migren muayenesi", "normal bulgular"],
            []
        ),
        (
            "Benzer şekilde trigeminal nevraljide de hastanın yüzünde elektrik çarpması benzeri paroksismal ağrı tariflenmesine rağmen nörolojik duyu muayenesi tamamen normaldir.",
            "**Trigeminal Nevralji:** Yüzde şimşek çakar ağrıya rağmen nörolojik duyu kaybının bulunmaması.",
            "• Trigeminal nevralji",
            ["trigeminal nevralji", "elektrik çarpması"],
            []
        ),
        (
            "Bu hastalıklarda çekilen beyin bilgisayarlı tomografisi veya manyetik rezonans görüntüleme, tanı koymaktan ziyade sekonder yapısal nedenleri dışlamak için istenir.",
            "**Dışlama Amaçlı Görüntüleme:** BT ve MRG'nin tanı koymaktan çok sekonder etiyolojiyi ekarte etme rolü.",
            "• BT, MR tanının doğru olduğunu göstermek için çekilir",
            ["bilgisayarlı tomografi", "manyetik rezonans"],
            []
        ),
        (
            "Epilepsi de temel olarak bir klinik öykü tanısıdır; hastanın elektroensefalografisinin normal bulunması epilepsi tanısını kesinlikle dışlamaz.",
            "**Epilepside Klinik Tanı:** Normal EEG bulgusunun klinik epilepsi tanısını dışlayamayacağı kuralı.",
            "• Epilepsi de klinik tanıdır. EEG normal olması tanıdan uzaklaştırmaz",
            ["epilepsi", "elektroensefalografi"],
            []
        ),
        (
            "Çünkü interiktal dönemde çekilen rutin bir elektroensefalografide hastaların yaklaşık yarısında epileptiform anormallik saptanamayabilir.",
            "**İnteriktal EEG Sınırı:** Rutin elektroensefalografide hastaların yarısında anormallik görülmeyebilmesi.",
            "• Epilepsi de klinik tanıdır. EEG normal olması tanıdan uzaklaştırmaz",
            ["interiktal EEG", "epileptiform anormallik"],
            []
        ),
        (
            "Büyük hekim Gordon Holmes'un dediği gibi, hasta karşınızda bir muamma gibi duruyorsa onu ikinci kez dinleyiniz; bilmeceyi çözme şansınız bütün araştırma yöntemlerinden daha büyük olacaktır.",
            "**Gordon Holmes Özdeyişi:** Hasta muamma gibi duruyorsa ikinci kez dinleyiniz; bilmeceyi çözme şansı artar.",
            "• «Hasta karşınızda bir muamma gibi duruyorsa onu ikinci kez dinleyiniz.",
            ["Gordon Holmes", "ikinci kez dinleme"],
            []
        )
    ]),

    # BOLUM 5: Sayfa 5 (1. Paragraf)
    (5, "k2-01-b05", "Nörolojik Muayenede İlk İzlenim, Postür ve Yürüyüş", "k2-01-p007", [
        (
            "Nörolojik muayene hasta muayene masasına yatırıldığında değil, poliklinik odasının kapısından içeri adım attığı ilk anda başlar.",
            "**Kapıda Başlayan Muayene:** Nörolojik muayenenin odanın kapısından girildiği an başlaması.",
            "Nörolojik Muayene",
            ["ilk izlenim", "muayene başlangıcı"],
            []
        ),
        (
            "Hastanın odaya girerken yürüyüşü, karşınıza oturduğunda yüz ifadesi, bakışları, ses tonu ve spontan hareketleri hekime sayısız tanısal ipucu verir.",
            "**İlk İpuçları:** Yürüyüş, yüz ifadesi, bakışlar, ses tonu ve spontan duruşun tanısal gücü.",
            "• Odaya girerken yürümesi, karşınıza oturduğunda yüzü, bakışları, ses tonu,",
            ["yüz ifadesi", "ses tonu", "bakışlar"],
            []
        ),
        (
            "Örneğin hemiplejik bir hastada etkilenen kol dirsekten fleksiyonda ve gövdeye yapışık dururken, yürürken parezik bacağını dizden bükemeden dışa doğru oraklar tarzda savurur.",
            "**Hemiplejik Yürüyüş:** Gövdeye yapışık fleksiyonda kol ve bacakta oraklama fenomeni.",
            "• Hemiplejik kolun gövdeye yapışık olması, yürürken bacağını oraklaması",
            ["oraklama yürüyüşü", "hemipleji postürü"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: Parkinson hastalığında mimiklerin kaybolduğu donuk bir maske yüz, alçak sesli monoton konuşma, ağız kenarından salya akması, yürürken kolları sallamama ve vücudun öne eğik fleksör postürü odaya girişte derhal fark edilir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Parkinson hastalığında maske yüz, monoton konuşma, salya akması ve kolların sallanmaması görülür.",
            "• Parkinson H. maske yüz, monoton konuşma, salya akması, yürürken kollarını",
            ["çıkmış sınav sorusu", "Parkinson", "maske yüz", "monoton konuşma"],
            ["804e82ac79db", "5e72fc758888"]
        ),
        (
            "Proksimal kas güçsüzlüğü ile seyreden kas distrofilerinde ise hasta pelvik kuşağını sabitleyemediği için karın önde, iki yana sallanarak ördek yürüyüşü yapar.",
            "**Ördek Yürüyüşü:** Pelvik kuşak zaafında karın önde iki yana sallanarak badi badi yürüyüşü.",
            "• Kas distrofisinde karın önde «badi-badi» yürüyüşü ördeğe benzer",
            ["kas distrofisi", "ördek yürüyüşü", "badi badi"],
            []
        ),
        (
            "Bu karakteristik sallantılı yürüyüş klinikte badi badi yürüyüşü olarak adlandırılır ve iki taraflı gluteus medius kas yetersizliğini yansıtan Trendelenburg belirtisine dayanır.",
            "**Trendelenburg Temeli:** İki taraflı gluteus medius zaafı sonucu oluşan sallantılı yürüyüş.",
            "• Kas distrofisinde karın önde «badi-badi» yürüyüşü ördeğe benzer",
            ["Trendelenburg", "gluteus medius"],
            []
        ),
        (
            "Serebellar ataksisi olan bir hasta ise dengesini koruyabilmek için ayaklarını geniş açarak sarhoşvari ve sendeleme tarzında geniş tabanlı yürür.",
            "**Serebellar Ataksi:** Denge kaybını telafi etmek için geniş tabanlı ve sarhoşvari yürüyüş.",
            "• İlk izlenim bile tanıya yardımcı olur",
            ["serebellar ataksi", "geniş tabanlı yürüyüş"],
            []
        ),
        (
            "Böylece hekim henüz elini hastaya sürmeden ve refleks çekicini eline almadan önce, sadece dikkatli bir görsel gözlem ile sendromik ön tanısını zihninde kurmuş olur.",
            "**Gözlemle Ön Tanı:** Muayene araçlarına geçmeden sadece görsel gözlemle sendromik tabloyu kavrama.",
            "• İlk izlenim bile tanıya yardımcı olur",
            ["gözlemsel tanı", "sendromik tanı"],
            []
        )
    ]),

    # BOLUM 5: Sayfa 5 (2. Paragraf)
    (5, "k2-01-b05", "Nörolojik Muayenede İlk İzlenim, Postür ve Yürüyüş", "k2-01-p008", [
        (
            "İlk izlenim sırasında hastanın konuşma niteliği dikkatle dinlenmeli, konuşmanın motor telaffuzu ile kortikal lisan içeriği birbirinden titizlikle ayırt edilmelidir.",
            "**Konuşma Analizi:** Motor telaffuz ile kortikal lisan içeriğinin birbirinden ayrılması.",
            "• Dizartri, afazi hemen farkedilir",
            ["motor telaffuz", "lisan içeriği"],
            []
        ),
        (
            "Hastanın sözcükleri peltek, yuvarlayarak veya sarhoşvari çıkarması ancak doğru sözcükleri seçip tam olarak anlaması dizartri tablosudur.",
            "**Dizartri Tablosu:** Sözcüklerin peltek ve sarhoşvari telaffuzu; anlamanın tam korunması.",
            "• Dizartri, afazi hemen farkedilir",
            ["dizartri", "telaffuz kusuru"],
            []
        ),
        (
            "Dizartri dil, dudak, damak ve larinks kaslarının motor innervasyon bozukluğuna veya serebellar koordinasyon kaybına bağlı mekanik bir telaffuz kusurudur.",
            "**Dizartri Mekanizması:** Kraniyal motor sinirler veya serebellar koordinasyon bozukluğunun telaffuzdaki yansıması.",
            "• Dizartri, afazi hemen farkedilir",
            ["motor innervasyon", "serebellar koordinasyon"],
            []
        ),
        (
            "Buna karşılık sözcük bulamama, anlamsız sözcük üretme veya söyleneni anlayamama lisan merkezlerinin kortikal hasarını gösteren afazi tablosudur.",
            "**Afazi Tablosu:** Sözcük bulamama ve anlama kaybı ile seyreden kortikal lisan hasarı.",
            "• Dizartri, afazi hemen farkedilir",
            ["afazi", "kortikal lisan"],
            []
        ),
        (
            "Hastanın şikayetini anlatırken kelimeleri nasıl telaffuz ettiği ve hekimin yönergelerini anlayıp anlamadığı ilk dakikalarda kendiliğinden ortaya çıkar.",
            "**İlk Dakikalarda Belirme:** Konuşma ve anlama düzeyinin poliklinik görüşmesinde hemen belirmesi.",
            "• Dizartri, afazi hemen farkedilir",
            ["yönerge anlama", "klinik belirme"],
            []
        ),
        (
            "Göz kapaklarında tek taraflı pitozis veya yüzde asimetri görülmesi kraniyal sinir felçlerini ilk bakışta hekimin dikkatine sunar.",
            "**Fasiyal Asimetri ve Pitozis:** Tek taraflı kapak düşüklüğü ve yüz felcinin ilk bakışta saptanması.",
            "• Odaya girerken yürümesi, karşınıza oturduğunda yüzü, bakışları, ses tonu,",
            ["pitozis", "fasiyal asimetri"],
            []
        ),
        (
            "Ayrıca istirahat halinde ellerde para sayar tarzda titreme izlenmesi Parkinsoniyen sendromların en klasik objektif dış bulgusudur.",
            "**İstirahat Tremoru:** İstirahatte ellerde para sayar tarzda titreme bulgusu.",
            "sallamaması, vücudun fleksör postürü",
            ["istirahat tremoru", "para sayma tremoru"],
            []
        ),
        (
            "Bu sistematik ilk gözlem süreci, nörolojik muayenenin geri kalan adımlarının çok daha odaklanmış ve amaca yönelik yapılmasını mümkün kılar.",
            "**Odaklanmış Muayene:** Başlangıç gözlemlerinin geri kalan muayeneyi hedefe kilitlemesi.",
            "• İlk izlenim bile tanıya yardımcı olur",
            ["odaklanmış muayene", "hedefe yönelik yaklaşım"],
            []
        )
    ]),

    # BOLUM 6: Sayfa 6 (1. Paragraf)
    (6, "k2-01-b06", "Nörolojik Lokalizasyon ve Klasik Anatomik Sendromlar", "k2-01-p009", [
        (
            "Nörolojik muayenede elde edilen objektif bulgular tek tek değil, birbirini tamamlayan bir klinik sendrom olarak ele alınmalıdır.",
            "**Sendromik Düşünce:** Muayene bulgularının tek tek değil klinik bir sendrom olarak birleştirilmesi.",
            "• Elde edilen bulguların bir araya gelmesiyle bir sendrom ortaya çıkar. Hemipleji",
            ["sendromik düşünce", "klinik sendrom"],
            []
        ),
        (
            "Bazen bulgular birbirini o derece kusursuz tamamlar ki, sinir sisteminde sadece ve sadece tek bir anatomik bölgeye karşılık gelir.",
            "**Tek Bölgeye Karşılık Gelme:** Birbirini tamamlayan bulguların tek bir anatomik odağı işaret etmesi.",
            "• Bazen bulgular birbirini o derece tamamlar ki sadece bir bölgeye karşılık gelir",
            ["anatomik odak", "tek bölge"],
            []
        ),
        (
            "Klasik lokalizasyon örneklerinden birincisinde afazi ile birlikte sağ hemipleji tablosunun bulunmasıdır.",
            "**Birinci Lokalizasyon:** Afazi ile sağ hemiplejinin birlikte saptanması.",
            "1. Afazi+ sağ hemipleji            piramidal yolu+ konuşma alanı. Sol hemisferde lezyon",
            ["afazi", "sağ hemipleji", "sol hemisfer"],
            []
        ),
        (
            "Bu tabloda piramidal motor yol ile motor veya duyusal konuşma alanı birlikte etkilenmiştir ve lezyon kesinlikle sol serebral hemisferdedir.",
            "**Sol Hemisfer Lezyonu:** Piramidal yol ile Broca-Wernicke lisan alanlarının sol hemisferde hasarlanması.",
            "1. Afazi+ sağ hemipleji            piramidal yolu+ konuşma alanı. Sol hemisferde lezyon",
            ["piramidal yol", "konuşma alanı", "sol hemisfer"],
            []
        ),
        (
            "İkinci klasik lokalizasyon örneği diplopi, vertigo, piramidal bulgular ve serebellar bulguların aynı anda bir arada bulunmasıdır.",
            "**İkinci Lokalizasyon:** Çift görme, baş dönmesi, piramidal ve serebellar bulguların birlikteliği.",
            "2. Diplopi+ vertigo+ piramidal bulgu+serebellar bulgu             lezyon beyin sapında",
            ["diplopi", "vertigo", "serebellar bulgu"],
            []
        ),
        (
            "Bu dört temel bulgunun birlikteliği, kraniyal sinir çekirdekleri ile uzun çıkan ve inen yolların sıkışık biçimde komşu olduğu beyin sapı lezyonunu kesin olarak gösterir.",
            "**Beyin Sapı Odağı:** Kraniyal çekirdekler, piramidal yol ve serebellar liflerin beyin sapında sıkışık birlikteliği.",
            "2. Diplopi+ vertigo+ piramidal bulgu+serebellar bulgu             lezyon beyin sapında",
            ["beyin sapı", "kraniyal çekirdek", "uzun yollar"],
            []
        ),
        (
            "Çünkü başka hiçbir anatomik alanda vestibüler çekirdekler, göz kaslarını innerve eden sinirler, piramidal yol ve serebellar bağlantılar bu kadar dar bir alanda birleşemez.",
            "**Anatomik Kesişim:** Vestibüler, okülomotor, kortikospinal ve serebellar yolların beyin sapı kesişimi.",
            "2. Diplopi+ vertigo+ piramidal bulgu+serebellar bulgu             lezyon beyin sapında",
            ["vestibüler çekirdek", "okülomotor", "kortikospinal"],
            []
        ),
        (
            "Böylece hekim bulguların kesişim kümesini bularak lezyonun santral sinir sistemindeki koordinatını milimetrik düzeyde saptar.",
            "**Milimetrik Koordinat:** Bulguların kesişim kümesiyle lezyon koordinatını kesinleme.",
            "Nörolojik Lokalizasyon",
            ["lezyon koordinatı", "kesişim kümesi"],
            []
        )
    ]),

    # BOLUM 6: Sayfa 6 (2. Paragraf)
    (6, "k2-01-b06", "Nörolojik Lokalizasyon ve Klasik Anatomik Sendromlar", "k2-01-p010", [
        (
            "Üçüncü klasik anatomik lokalizasyon örneği her iki bacakta motor güçsüzlük yani parapleji, gövdede seviye veren duyu kaybı ve sfinkter bozukluğu birlikteliğidir.",
            "**Üçüncü Lokalizasyon:** Parapleji, seviye veren duyu kaybı ve sfinkter bozukluğu triadı.",
            "3. Parapleji+ gövdede seviye veren duyu kaybı+ sfinkter boz.          Medulla spinalis",
            ["parapleji", "seviye veren duyu kaybı", "sfinkter bozukluğu"],
            []
        ),
        (
            "Bu klinik triad, lezyonun medulla spinaliste yer aldığını ve o duyu seviyesindeki spinal segmentin hasarlandığını tartışmasız biçimde kanıtlar.",
            "**Medulla Spinalis Lezyonu:** Seviye veren duyu kusuru ve sfinkter kaybının omurilik hasarını kanıtlaması.",
            "3. Parapleji+ gövdede seviye veren duyu kaybı+ sfinkter boz.          Medulla spinalis",
            ["medulla spinalis", "spinal segment"],
            []
        ),
        (
            "Örneğin meme başı hizasında duyu seviyesi dördüncü torakal segmenti, göbek hizasındaki seviye ise onuncu torakal segmenti işaret eder.",
            "**Dermatomal Seviyeler:** T4 meme başı ve T10 göbek dermatomal duyu seviyeleri.",
            "3. Parapleji+ gövdede seviye veren duyu kaybı+ sfinkter boz.          Medulla spinalis",
            ["dermatomal seviye", "torakal segment"],
            []
        ),
        (
            "Sfinkter kontrolünün bozulması ve seviye veren duyu kusuru, spinal kordun transvers lezyonunu periferik polinöropatilerden kesin olarak ayırır.",
            "**Transvers Kord Ayrımı:** Sfinkter ve seviye veren duyu kaybının periferik nöropatiden ayrımı.",
            "3. Parapleji+ gövdede seviye veren duyu kaybı+ sfinkter boz.          Medulla spinalis",
            ["transvers kord", "polinöropati ayrımı"],
            []
        ),
        (
            "Dördüncü klasik lokalizasyon örneği ise belden bacak arkasına yayılan radiküler ağrı ile birlikte aşil refleksinin alınamaması tablosudur.",
            "**Dördüncü Lokalizasyon:** Bel-bacak arkası ağrısı ve aşil refleksi kaybı tablosu.",
            "4. Bel ve bacak arkasına vuran ağrı+ aşil refleksi alınamıyorsa            1. sakral radiks",
            ["aşil refleksi", "radiküler ağrı", "sakral radiks"],
            []
        ),
        (
            "Bu klinik tablo birinci sakral spinal radiksin yani se bir kökünün lumbosakral disk hernisi veya osteofit ile basılandığını gösterir.",
            "**Birinci Sakral Radiks (S1):** Lumbosakral disk hernisinde S1 kök basısı ve aşil kaybı.",
            "4. Bel ve bacak arkasına vuran ağrı+ aşil refleksi alınamıyorsa            1. sakral radiks",
            ["S1 radiks", "disk hernisi"],
            []
        ),
        (
            "Aşil refleksi doğrudan birinci sakral segmentin refleks arkını test ettiği için, refleks kaybı kök basısının en güvenilir objektif motor kanıtıdır.",
            "**S1 Refleks Arkı:** Aşil refleksinin doğrudan birinci sakral segment refleks arkını temsil etmesi.",
            "4. Bel ve bacak arkasına vuran ağrı+ aşil refleksi alınamıyorsa            1. sakral radiks",
            ["refleks arkı", "kök basısı"],
            []
        ),
        (
            "Bu sendromik düşünce sistemi sayesinde hekim, semptomların karmaşası içinde kaybolmadan doğrudan sorumlu nöroanatomik odağa kilitlenir.",
            "**Nöroanatomik Odak:** Sendromik düşünce ile sorumlu anatomik odağa doğrudan kilitlenme.",
            "Nörolojik Lokalizasyon",
            ["nöroanatomik odak", "sendromik analiz"],
            []
        )
    ]),

    # BOLUM 7: Sayfa 7 (1. Paragraf)
    (7, "k2-01-b07", "Lezyonun Natürü (Etiyolojik Yaklaşım)", "k2-01-p011", [
        (
            "Lezyonun anatomik lokalizasyonu kesinleştirildikten sonra hekimin yanıtlaması gereken ikinci hayati soru, lezyonun natürü yani etiyolojisidir.",
            "**Lezyonun Natürü Sorusu:** Lokalizasyondan sonra yanıtlanması gereken ikinci soru: Etyoloji ne?",
            "Lezyonun Natürü",
            ["lezyonun natürü", "etiyolojik soru"],
            []
        ),
        (
            "Aynı anatomik sendromu oluşturan hastalıklar, hastanın özgeçmişine, yaşına ve lezyonun yerleşim hızına göre bambaşka patolojik süreçlerden kaynaklanabilir.",
            "**Farklı Patolojiler:** Aynı anatomik sendromun arka plandaki farklı patolojik süreçleri.",
            "Lezyonun Natürü",
            ["patolojik süreçler", "klinik arka plan"],
            []
        ),
        (
            "Örneğin hemipleji sendromu olan bir hastada hipertansiyon ve diyabet öyküsü varsa, ilk sırada damarsal etiyoloji yani serebrovasküler olay düşünülür.",
            "**Vasküler Hemipleji:** Hipertansiyon ve diyabet varlığında ilk sırada serebrovasküler olay.",
            "• Hemipleji          HT+DM ilk sırada damarsal etyoloji",
            ["hipertansiyon", "diyabet", "serebrovasküler olay"],
            []
        ),
        (
            "Eğer hemipleji tablosu dakikalar içinde değil de haftalar veya aylar içinde yavaş yavaş yerleşmiş ve giderek ağırlaşmışsa, primer beyin tümörü gibi yer kaplayan lezyonlar akla gelmelidir.",
            "**Yer Kaplayan Lezyon:** Yavaş yerleşip giderek ağırlaşan hemiplejide tümör şüphesi.",
            "yavaş yerleşmişse, giderek ağırlaşıyorsa YKL",
            ["yer kaplayan lezyon", "beyin tümörü"],
            []
        ),
        (
            "Hastada bilinen bir akciğer veya meme kanseri gibi sistemik malignite öyküsü bulunuyorsa, yeni gelişen nörolojik kayıpta ilk akla gelmesi gereken olasılık beyin metastazıdır.",
            "**Metastaz Olasılığı:** Sistemik malignite öyküsünde yeni gelişen defisitte beyin metastazı önceliği.",
            "malignite öyküsü +  metastaz",
            ["malignite öyküsü", "beyin metastazı"],
            []
        ),
        (
            "Metastatik kitleler genellikle gri-beyaz cevher bileşkesine yerleşerek etrafında yoğun vazojenik ödem oluşturur ve hızla kafa içi basınç artışına yol açar.",
            "**Vazojenik Ödem:** Metastazların gri-beyaz bileşke yerleşimi ve vazojenik ödem oluşturması.",
            "malignite öyküsü +  metastaz",
            ["gri-beyaz bileşke", "vazojenik ödem"],
            []
        ),
        (
            "Dolayısıyla hemiplejinin klinik tablosu aynı kalsa bile, hastanın klinik arka planı hekimi vasküler, tümöral veya metastatik tanılara yönlendirir.",
            "**Klinik Arka Plan:** Semptom aynı olsa bile arka planın hekimi vasküler, tümör veya metastaza yönlendirmesi.",
            "• Hemipleji          HT+DM ilk sırada damarsal etyoloji",
            ["etiyolojik yönelim", "vasküler tümör metastaz"],
            []
        ),
        (
            "Bu ayrım yapılmaksızın doğru tedavi protokolünü belirlemek ve cerrahi ya da medikal kararı vermek asla mümkün değildir.",
            "**Tedavi Kararı:** Natür ayrımı yapılmadan doğru cerrahi veya medikal kararın verilemeyeceği gerçeği.",
            "Lezyonun Natürü",
            ["tedavi kararı", "cerrahi medikal"],
            []
        )
    ]),

    # BOLUM 7: Sayfa 7 (2. Paragraf)
    (7, "k2-01-b07", "Lezyonun Natürü (Etiyolojik Yaklaşım)", "k2-01-p012", [
        (
            "Beyin sapı lokalizasyonunda etiyolojik ayrım hastanın yaşı ve geçmiş atak öyküsü üzerinden kurulur.",
            "**Beyin Sapında Etyoloji:** Yaş ve geçmiş epizod öyküsü üzerinden etiyolojik ayrım.",
            "• Beyin sapı lokalizasyonu       genç hasta, kısa zamanda gelişmiş, öyküsünde sinir",
            ["beyin sapı etiyolojisi", "yaş faktörü"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: genç bir hastada beyin sapı bulguları kısa zamanda gelişmişse ve öyküsünde sinir sisteminin farklı bölgelerinin etkilendiği, zamanla düzelen atak epizodları varsa en olası tanı multipl sklerozdur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Genç hasta, beyin sapı bulguları ve düzelen epizodlar Multipl Skleroz (MS) tanısını gösterir.",
            "sisteminin farklı bölgelerinin etkilendiği epizodlar geçirip düzelmişse            MS",
            ["çıkmış sınav sorusu", "multipl skleroz", "beyin sapı lezyonu", "epizodik ataklar"],
            ["4c4eb178b88b", "4ba07c308e35"]
        ),
        (
            "Multipl skleroz santral sinir sisteminde zaman ve mekan içinde dissemine olan otoimmün demiyelinizan plaklarla karakterizedir.",
            "**Zaman ve Mekan Disseminasyonu:** Multipl sklerozun zaman ve mekanda yayılım gösteren demiyelinizasyonu.",
            "sisteminin farklı bölgelerinin etkilendiği epizodlar geçirip düzelmişse            MS",
            ["zaman ve mekan disseminasyonu", "demiyelinizan plak"],
            []
        ),
        (
            "Buna karşılık benzer beyin sapı bulguları ileri yaşta ve ateroskleroz ile hipertansiyon zemininde aniden ortaya çıktığında, vertebrobaziler sistemde bir serebrovasküler olay düşünülür.",
            "**Vertebrobaziler İskemi:** İleri yaş ve ateroskleroz zemininde ani beyin sapı bulgularında SVO.",
            "Yaşlı hasta+ ateroskleroz          SVO",
            ["ateroskleroz", "serebrovasküler olay", "vertebrobaziler sistem"],
            []
        ),
        (
            "Parapleji sendromunda da sinsi başlangıç ve ilerleyici seyir omuriliği dıştan basılayan bir spinal tümör veya servikal spondilotik miyelopatiyi işaret eder.",
            "**Spinal Bası:** Sinsi başlangıç ve ilerleyici seyirde medulla spinalis kompresyonu.",
            "• Parapleji              sinsi başlangıç, ilerleyici seyir           medulla spinalis basısı",
            ["spinal tümör", "medulla spinalis basısı"],
            []
        ),
        (
            "Buna karşın parapleji yakın zamanda geçirilmiş bir aşılama veya viral enfeksiyonu takiben akut gelişmişse, post enfeksiyöz transvers miyelit düşünülmelidir.",
            "**Post-İnfeksiyöz Miyelit:** Aşı veya viral enfeksiyon sonrası gelişen akut transvers miyelit.",
            "aşı ya da viral enf +             post-infeksiyöz miyelit",
            ["viral enfeksiyon", "aşı", "post-infeksiyöz miyelit"],
            []
        ),
        (
            "Post enfeksiyöz miyelitte otoimmün çapraz reaksiyon sonucu omurilikte diffüz inflamasyon ve iletim bloğu meydana gelir.",
            "**Miyelit Patofizyolojisi:** İmmün çapraz reaksiyonla omurilikte gelişen inflamasyon ve iletim bloğu.",
            "aşı ya da viral enf +             post-infeksiyöz miyelit",
            ["otoimmün reaksiyon", "iletim bloğu"],
            []
        ),
        (
            "Böylece hekim anatomik koordinat ile klinik natürü birleştirerek hastasına tam ve eksiksiz bir nörolojik tanı koymuş olur.",
            "**Tam Tanı:** Anatomik lokalizasyon ile natürün sentezlenerek kesin tanıya ulaşılması.",
            "Lezyonun Natürü",
            ["tam tanı", "klinik sentez"],
            []
        )
    ]),

    # BOLUM 8: Sayfa 8
    (8, "k2-01-b08", "Laboratuvar İncelemeleri ve Nörogörüntüleme", "k2-01-p013", [
        (
            "Klinik muayene ve lezyon natürü hipotezleri oluşturulduktan sonra, tanıyı doğrulamak için genel metodlar ve spesifik nörolojik incelemelerden yararlanılır.",
            "**Laboratuvar Basamakları:** Genel laboratuvar metodları ve spesifik nörolojik incelemeler.",
            "Laboratuvar İncelemeleri",
            ["laboratuvar incelemeleri", "spesifik yöntemler"],
            []
        ),
        (
            "Genel metodlar arasında yer alan rutin biyokimya ve bakteriyolojik incelemeler; elektrolit bozuklukları, üremi, karaciğer yetmezliği ve sistemik enfeksiyonları aydınlatır.",
            "**Genel Metodlar:** Biyokimya ve bakteriyoloji ile metabolik-enfeksiyöz nedenlerin taranması.",
            "• Genel metodlar: biyokimya, bakteriyolojik metodlar g.b",
            ["rutin biyokimya", "bakteriyoloji", "metabolik nedenler"],
            []
        ),
        (
            "Spesifik incelemelerin başında gelen beyin omurilik sıvısı incelemesi, menenjit, ensefalit, subaraknoid kanama ve multipl sklerozdaki oligoklonal bantların saptanmasında altın standarttır.",
            "**BOS İncelemesi:** Menenjit, ensefalit, SAK ve oligoklonal bantlar için altın standart BOS.",
            "• Spesifik: BOS incelemesi",
            ["beyin omurilik sıvısı", "menenjit", "oligoklonal bant"],
            []
        ),
        (
            "Elektroensefalografi beynin kortikal elektriksel aktivitesini kaydederek epileptik odakları ve metabolik ensefalopatileri inceler.",
            "**Elektroensefalografi:** Kortikal elektriksel aktivite, epileptik odaklar ve ensefalopati.",
            "• EEG",
            ["elektroensefalografi", "epileptik odak"],
            []
        ),
        (
            "Elektromiyografi ve sinir ileti çalışmaları ise periferik nöropatiler, radikülopatiler ve kas hastalıklarının ayrımında vazgeçilmez elektrofizyolojik yöntemlerdir.",
            "**Elektromiyografi:** Periferik sinir, radiks ve kas hastalıklarında EMG ve ileti çalışmaları.",
            "• EMG",
            ["elektromiyografi", "sinir ileti çalışması"],
            []
        ),
        (
            "Uyarılmış potansiyeller görsel, işitsel ve somatosensoriyel yolların subklinik demiyelinizan iletim gecikmelerini yüksek duyarlılıkla ortaya koyar.",
            "**Uyarılmış Potansiyeller (EP):** Görsel, işitsel ve duyusal yollarda subklinik iletim gecikmelerinin tespiti.",
            "• Uyarılmış potansiyeller- EP evoked potentials",
            ["uyarılmış potansiyeller", "iletim gecikmesi"],
            []
        ),
        (
            "Nörogörüntülemede beyin bilgisayarlı tomografisi akut kanama, kemik kırığı ve herniasyon acillerinde dakikalar içinde hayat kurtarır.",
            "**Acil Beyin Tomografisi:** Akut intrakraniyal kanama ve kemik kırıklarında hayat kurtarıcı BT.",
            "• BBT",
            ["bilgisayarlı tomografi", "akut kanama"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: hipertansiyon öyküsü olan, ani hemipleji ve dizartri ile acile başvuran inme şüpheli hastada damarsal etiyolojiyi doğrulamak ve kanama ile iskemiyi ayırt etmek için ilk tercih kontrastsız bilgisayarlı tomografi ve difüzyon manyetik rezonanstır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Akut inme ve hemiplejide ilk tercih görüntüleme BBT ve difüzyon beyin MRI'dır.",
            "• beyin MRI",
            ["çıkmış sınav sorusu", "bilgisayarlı tomografi", "manyetik rezonans", "inme"],
            ["3807e9b207c5"]
        )
    ]),

    # BOLUM 9: Sayfa 9
    (9, "k2-01-b09", "Özel Acil Durumlar ve Sevk İlkeleri", "k2-01-p014", [
        (
            "Acil nörolojide bazı özel klinik durumlar vardır; acile getirilen hasta bilinçsiz, stupor halinde ya da afazik olabilir ve getiren kişinin hastanın geçmişi hakkında hiçbir bilgisi bulunmayabilir.",
            "**Özel Acil Durumlar:** Bilinçsiz veya afazik hastada refakatçinin bilgi sahibi olamaması.",
            "• Acil olarak getirilen hasta bilinçsiz ya da afazik olabilir. Getiren kişi bilgi sahibi",
            ["özel acil durumlar", "bilinçsiz hasta", "afazi"],
            []
        ),
        (
            "Böyle bir durumda geri dönüşü olmayan kalıcı nöronal hasar gelişmeden önce ivedi müdahale etmek gerekir; çünkü zaman hastanın ve hekimin aleyhine işler.",
            "**Zaman Aleyhe İşler:** Geri dönüşsüz hasar gelişmeden önce acil müdahale zorunluluğu.",
            "müdahale etmek gerekiyor. Zaman hastanın ve hekimin aleyhine işler.",
            ["ivedi müdahale", "zaman aleyhe işler"],
            []
        ),
        (
            "Nörolojik acillerde bu hayati ilke zaman beyindir kuralı ile özetlenir; iskemik inmede her geçen dakika yaklaşık iki milyon nöron geri dönüşsüz olarak ölür.",
            "**Zaman=Beyin:** İskemide her dakika iki milyon nöronun öldüğü gerçeği ve zaman beyindir ilkesi.",
            "Zaman=beyin",
            ["zaman beyindir", "nöron ölümü", "iskemi"],
            []
        ),
        (
            "Hızlı bir şekilde öykü toplanırken eş zamanlı olarak tedaviye başlanmalı; hava yolu açık tutulmalı, oksijenasyon sağlanmalı ve devam eden epileptik nöbetler hızla durdurulmalıdır.",
            "**Eş Zamanlı Stabilizasyon:** Bilgi toplarken hava yolunu açık tutma, oksijenasyon ve nöbet kontrolü.",
            "• Hızlı bir şekilde bilgi toplarken tedaviye de başlanır. Vital bulguları stabil hale",
            ["vital bulgular", "hava yolu", "nöbet kontrolü"],
            []
        ),
        (
            "İlk gören hekim hastanın nörolojik durumunun giderek kapandığını ve tablonun progrese olduğunu fark ettiğinde, tanı konulamayan hastayı derhal donanımlı bir nöroloji merkezine sevk etmelidir.",
            "**Progresyonun Fark Edilmesi:** Bilincin kapandığını fark etme ve sevk kararının gecikmeden alınması.",
            "• İlk gören hekim hastanın giderek kapandığını, progrese olduğunu farketmeli. Tanı",
            ["progresyon", "bilinç kapanması", "sevk kararı"],
            []
        ),
        (
            "Sevk sırasında hastanın öykü ve muayene bulguları açık, anlaşılır ve objektif ifadelerle kaydedilmeli; yanıltıcı olabilecek anlaşılmaz tıbbi kısaltmalardan kesinlikle kaçınılmalıdır.",
            "**Sevk Notu Standartları:** Açık, anlaşılır ve kısaltmasız objektif sevk notu yazımı.",
            "• Gönderirken öykü ve muayene bulgularını açık, anlaşılır bir şekilde yazmalı.",
            ["sevk notu", "kısaltma yasağı"],
            []
        ),
        (
            "Ayrıca hekim epilepsi, miyokloni veya kore gibi tanısal deyimler yazmak yerine doğrudan gözlemlediği hareketleri tarif etmeli; bilinç düzeyini, muayene saatini ve pupil büyüklükleri ile ışık refleksini mutlaka kaydetmelidir.",
            "**Gözlemin Doğrudan Tarifi:** Tanısal etiket yerine gözlenen hareket, pupil boyutu ve saatin kaydı.",
            "yerine gördüğünü yazmalı. Bilinç düzeyini , saatini, pupil büyüklüklerini",
            ["pupil büyüklüğü", "ışık refleksi", "doğrudan tarif"],
            []
        ),
        (
            "Hemiparezi varlığı kaydedilirken sağ bacağını yerçekimine karşı kaldıramıyor ancak yatak içinde çekebiliyor şeklinde objektif kas gücü derecelendirmesi açıkça belirtilmelidir.",
            "**Objektif Kas Gücü:** Bacağını kaldıramıyor yatak içinde çekebiliyor şeklinde açık tarif.",
            "kaydetmeli. Hemiparezi açıklamalı ( bacağını kaldıramıyor yatak içinde çekebiliyor)",
            ["hemiparezi tarifi", "kas gücü"],
            []
        )
    ])
]

# Verify anchors
print("--- Verifying anchors against kaynak.md ---")
anchor_errors = []
for p_sayfa, bid, bbaslik, pid, sents in PARAGRAPHS:
    ptext = page_dict.get(p_sayfa, "")
    for s_idx, (ses, ekran, satir, etiketler, cikmis) in enumerate(sents):
        if satir not in ptext:
            anchor_errors.append(f"Page {p_sayfa} ({pid} snt {s_idx+1}): anchor '{satir}' NOT FOUND in page {p_sayfa}")

if anchor_errors:
    print(f"FAILED: {len(anchor_errors)} anchor errors:")
    for e in anchor_errors: print(" ", e)
    sys.exit(1)
print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Build bolum map
bolum_map = {}
cid_counter = 1
para_last_sent = {}
total_words = 0

for p_sayfa, bid, bbaslik, pid, sents in PARAGRAPHS:
    if bid not in bolum_map:
        b_idx = len(bolum_map) + 1
        bolum_map[bid] = {
            "id": bid,
            "bolumIndex": b_idx,
            "baslik": bbaslik,
            "paragraflar": []
        }
    
    cumleler = []
    for ses, ekran, satir, etiketler, cikmis in sents:
        cid = f"k2-01-c{cid_counter:04d}"
        cumleler.append({
            "id": cid,
            "ses": ses,
            "ekran": ekran,
            "slayt": {
                "sayfa": p_sayfa,
                "satir": satir
            },
            "etiketler": etiketler,
            "cikmis": cikmis
        })
        cid_counter += 1
        total_words += len(ses.split())
    
    para_last_sent[pid] = cumleler[-1]["id"]
    bolum_map[bid]["paragraflar"].append({
        "id": pid,
        "sayfa": p_sayfa,
        "slayt": {"sayfa": p_sayfa},
        "cumleler": cumleler
    })

bolumler_list = list(bolum_map.values())

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-01",
    "anahtar": "y25-k2-01-norolojik-hastaya-yaklasim",
    "bolumler": bolumler_list
}

print(f"Total Bolumler: {len(bolumler_list)}")
print(f"Total Paragraphs: {len(PARAGRAPHS)}")
print(f"Total Sentences: {cid_counter - 1}")
print(f"Total Words: {total_words} (~{total_words / 125:.1f} minutes of audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Generate and save metin.md and konusma_metni.md
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Nörolojik Hastaya Yaklaşım"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
(TASLAK / "konusma_metni.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md and konusma_metni.md")

# Update sayfa_haritasi.json
harita = json.load(open(TASLAK / "sayfa_haritasi.json"))
harita_items = []
for sayfa, bid, bbaslik, pid, sentences in PARAGRAPHS:
    harita_items.append({
        "sayfa": sayfa,
        "paragraf": pid,
        "bolum_id": bid,
        "bolum_baslik": bbaslik,
        "cumle_sayisi": len(sentences)
    })
harita["harita"] = harita_items
(TASLAK / "sayfa_haritasi.json").write_text(json.dumps(harita, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated sayfa_haritasi.json with 14 distinct paragraphs.")

# 14 Drawing commands matching cum_text exactly
cizim_komutlari = [
    {
        "cumle": para_last_sent["k2-01-p001"],
        "bas": 0, "son": 4,
        "sayfa": 1,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nörolojik Yaklaşımın Temel Soruları",
        "ogeler": [
            "Anatomik lokalizasyon: Lezyon nerede?",
            "Patolojik süreç ve etiyoloji: Natür ne?",
            "Ayrıntılı anamnez ve klinik muayene"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p002"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nörolojik Anamnez İlkeleri",
        "ogeler": [
            "Merritt: Hastayı dinledikten sonra muayene etmek",
            "Uyuşma ifadesi: Duyu kusuru veya motor kayıp",
            "Ayrıntılı sorgulama ile klinik yönelim"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p003"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Ağrı ve Bilinçsiz Hasta",
        "ogeler": [
            "Ağrının sübjektif nitelikleri ve lokalizasyonu",
            "Hayatın en şiddetli ağrısı ve subaraknoid kanama",
            "Bilinçsiz hastada yakından anamnez alınmalıdır"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p004"],
        "bas": 0, "son": 4,
        "sayfa": 3,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Başlayış Şekli ve Klinik Seyir",
        "ogeler": [
            "Akut başlangıç: Dakikalar içinde hemipleji",
            "Sinsi başlangıç: Aylar içinde tümör veya dejenerasyon",
            "Dalgalı gidiş: Atak ve düzelmelerle seyreden multipl skleroz"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p005"],
        "bas": 0, "son": 4,
        "sayfa": 3,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Hastalığın Doğal Seyri ve Tedavi Değerlendirmesi",
        "ogeler": [
            "Düzelme uygulanan tedaviye mi bağlı?",
            "Yoksa hastalığın kendi doğal seyrine mi bağlı?",
            "Tedavi etkinliğini objektif değerlendirme"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p006"],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Tanısı Öyküye Dayanan Hastalıklar",
        "ogeler": [
            "Migren: Öykü ile tanı konan primer baş ağrısı",
            "Trigeminal nevralji: Paroksismal şimşek çakar ağrı",
            "Epilepsi: Klinik tanı ve normal elektroensefalografi"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p007"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nörolojik Muayenede İlk İzlenim",
        "ogeler": [
            "Hemipleji: Gövdeye yapışık kol ve oraklama yürüyüşü",
            "Parkinson hastalığı: Maske yüz ve monoton konuşma",
            "Kas distrofisi: Karın önde ördek yürüyüşü"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p008"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Konuşma Bozuklukları ve Gözlem",
        "ogeler": [
            "Dizartri: Telaffuz ve motor konuşma bozukluğu",
            "Afazi: Dil ve anlama merkezi hasarı",
            "Odaya girişteki ilk ipuçlarının tanısal değeri"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p009"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Klasik Anatomik Sendromlar",
        "ogeler": [
            "Afazi ve sağ hemipleji: Sol serebral hemisfer",
            "Diplopi, vertigo ve piramidal bulgu: Beyin sapı",
            "Bulguların bir araya gelmesiyle sendromik tanı"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p010"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kord ve Radiks Lezyonları",
        "ogeler": [
            "Parapleji ve seviye veren duyu kaybı: Medulla spinalis",
            "Bel ve bacak arkası ağrısı: Birinci sakral radiks",
            "Aşil refleksi kaybı ile kök basısı kanıtı"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p011"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Lezyonun Natürü ve Etyolojik Ayrım",
        "ogeler": [
            "Hemipleji ve hipertansiyon: Vasküler serebrovasküler olay",
            "Yavaş ilerleyen hemipleji: Yer kaplayan lezyon veya tümör",
            "Malignite öyküsü varlığında beyin metastazı"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p012"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Spinal ve Beyin Sapı Etyolojileri",
        "ogeler": [
            "Genç hastada atak ve düzelmeler: Multipl skleroz",
            "Aterosklerotik yaşlı hastada: Serebrovasküler olay",
            "Aşı veya viral enfeksiyon: Post enfeksiyöz miyelit"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p013"],
        "bas": 0, "son": 4,
        "sayfa": 8,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Laboratuvar ve Görüntüleme",
        "ogeler": [
            "Genel metodlar: Biyokimya ve metabolik tarama",
            "Spesifik inceleme: Beyin omurilik sıvısı ve EMG",
            "Nörogörüntüleme: Bilgisayarlı tomografi ve MR"
        ]
    },
    {
        "cumle": para_last_sent["k2-01-p014"],
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Acil Nöroloji ve Sevk Kuralları",
        "ogeler": [
            "Zaman beyindir ilkesi ve ivedi müdahale",
            "Hızlı bilgi toplarken solunum yolu ve nöbet kontrolü",
            "Açık ve objektif sevk notu yazma kuralları"
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
