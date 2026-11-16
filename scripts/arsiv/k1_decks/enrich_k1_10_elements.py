"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) İnteraktif Öğe Zenginleştirme Modülü.
Çeşitlilik kuralı gereğince tüm 7 türün her birinin >= %8.0 olmasını temin eder.
"""

from .k1_10_deck_data.helpers import (
    make_micro_quiz, make_branching_logic, make_causal_chain
)

def get_extra_branching():
    """Ekstra klinik karar senaryoları (branching_logic)."""
    return {
        4: make_branching_logic(
            "Birinci trimester spontan düşük materyalinde sitogenetik analizde 69,XXY karyotipi saptanıyor. Patoloji raporunda plasentada kistik hidropik villus dejenerasyonu ve belirgin trofoblastik hiperplazi izleniyor. Bu poliploidinin parental kökeni ve etiyolojik mekanizması nedir?",
            [
                {"text": "Babadan gelen iki spermle tek oositin döllenmesi (dispermi) sonucu oluşan diandrik triploididir; paternal genom plasental büyümeyi uyarır", "isCorrect": True, "feedback": "Kusursuz tıp ve sitogenetik muhakemesi! Parsiyel mol ve trofoblast hiperplazisi diandrik (baba kökenli) triploidinin patognomonik özelliğidir."},
                {"text": "Anneden gelen diploid oositin normal spermle döllenmesidir (digini); anne genomu plasentayı büyütür", "isCorrect": False, "feedback": "Diginik triploidide plasenta çok küçük ve fibrotik kalır; mol tablosu oluşmaz."},
                {"text": "Yalnızca mitotik bölünme sırasında sitoplazmanın bölünmemesi (sitokinez hatası) ile oluşur", "isCorrect": False, "feedback": "Triploidilerin %66'sı dispermi kaynaklıdır."}
            ]
        ),
        11: make_branching_logic(
            "Periferik kan karyotipinde 46,XX,del(5)(p15.2) saptanan bir bebeğin ailesine genetik danışmanlık veriyorsunuz. Aile bu delesyonun sonraki çocuklarında tekrarlama olasılığını soruyor. İlk olarak yapılması gereken en doğru genetik yaklaşım nedir?",
            [
                {"text": "Her iki ebeveynin de periferik kan karyotipini inceleyerek dengeli bir translokasyon veya inversiyon taşıyıcılığını ekarte etmek", "isCorrect": True, "feedback": "Mükemmel klinik genetik yaklaşımı! Olguların %10-15'inde ebeveynlerden birinde dengeli yapısal anomali bulunabilir ve rekürrens riskini belirleyen budur."},
                {"text": "Delesyonların %100'ü rastlantısaldır, ebeveyn testine gerek kalmadan riskin sıfır olduğunu söylemek", "isCorrect": False, "feedback": "Ebeveyn taşıyıcılığı %15'e varabilir; ebeveyn testi yapılmadan risk söylenemez."},
                {"text": "Annenin sonraki gebeliklerinde sadece demir ve folik asit almasının yeterli olduğunu belirtmek", "isCorrect": False, "feedback": "Sitogenetik anomali besinsel faktörlerle engellenemez."}
            ]
        ),
        13: make_branching_logic(
            "Pediatri servisinde izlenen 4 yaşında bir çocukta zihinsel gerilik, konjenital kalp defekti ve dismorfik yüz bulguları mevcuttur. Standart 550 bant G-bantlama karyotip analizi '46,XY (Normal Erkek)' olarak raporlanıyor. Genetik polikliniğinde bu hastaya yaklaşımınız ne olmalıdır?",
            [
                {"text": "Standart karyotipin göremediği submikroskobik delesyon ve duplikasyonları taramak amacıyla Kromozomal Mikroarray (CMA / aCGH) analizi istemek", "isCorrect": True, "feedback": "Harika klinik genetik kararı! Zihinsel gerilik ve çoklu anomalide normal karyotip mikrodelesyonu ekarte etmez; ilk basamak test CMA'dır."},
                {"text": "Karyotip normal çıktığı için hastanın genetik bir hastalığı olmadığını kabul edip genetik takibi sonlandırmak", "isCorrect": False, "feedback": "Standart karyotip çözünürlüğü düşüktür; mikrodelesyonları atlar."},
                {"text": "Sadece idrarda amino asit kromatografisi yaparak metabolik taramayla yetinmek", "isCorrect": False, "feedback": "Dismorfik ve yapısal defektli olguda mikroarray atlanamaz."}
            ]
        ),
        16: make_branching_logic(
            "Rutin prenatal taramada bir gebede perisentrik inversiyon 46,XX,inv(9)(p12q13) saptanıyor. Anne adayı aşırı endişeli olarak polikliniğe başvuruyor. Bu hastaya verilecek en doğru ve rahatlatıcı genetik bilgi nedir?",
            [
                {"text": "9. kromozomun heterokromatin bölgesini içeren perisentrik inversiyonun popülasyonda sık görülen selim bir normal polimorfizm olduğu ve fetüste anomaliye yol açmayacağı", "isCorrect": True, "feedback": "Kusursuz danışmanlık! inv(9)(p12q13) toplumda en sık görülen selim yapısal varyanttır (polimorfizm); hastalık yapmaz."},
                {"text": "Bu durumun mutlak bir trizomiye eşdeğer olduğu ve gebeliğin acilen sonlandırılması gerektiği", "isCorrect": False, "feedback": "inv(9) selim polimorfizmdir, terminasyon endikasyonu kesinlikle yoktur."},
                {"text": "Bebeğin doğar doğmaz açık kalp ameliyatına alınması gerektiği", "isCorrect": False, "feedback": "inv(9) kalp anomalisi riskini artırmaz."}
            ]
        ),
        23: make_branching_logic(
            "Fenotipik olarak tamamen sağlıklı 26 yaşında bir erkeğin evlilik öncesi taramasında karyotipi 45,XY,rob(13;14)(q10;q10) olarak raporlanıyor. Bu bireye üreme biyolojisi açısından yapılacak en doğru açıklama nedir?",
            [
                {"text": "Kendisinde 45 kromozom olmasına rağmen genetik materyal dengeli olduğu için sağlıklıdır; ancak çocuk sahibi olurken dengesiz gamet riski ve tekrarlayan düşük ihtimali açısından prenatal tanı ve PGT seçenekleri mevcuttur", "isCorrect": True, "feedback": "Kusursuz sitogenetik danışmanlık! Taşıyıcı dengelidir ancak mayotik trivalan ayrılması dengesiz gamet ve fetal kayıplara yol açabilir."},
                {"text": "45 kromozomu olduğu için kendisinde erken yaşta zekâ geriliği ve kas erimesi başlayacaktır", "isCorrect": False, "feedback": "Dengeli Robertsonian taşıyıcılarında somatik fenotipik bozulma beklenmez."},
                {"text": "Tüm çocukları istisnasız %100 Patau sendromlu doğacaktır", "isCorrect": False, "feedback": "rob(13;14)'te Patau riski %1'in bile altındadır; çoğu çocuk sağlıklı doğar."}
            ]
        ),
        25: make_branching_logic(
            "Bir ailede babanın homolog akrosentrik translokasyon olan rob(21;21) taşıyıcısı olduğu belirleniyor. Bu çiftin çocuk sahibi olma planları değerlendirilirken teorik ve pratik Down sendromu riski aileye nasıl açıklanmalıdır?",
            [
                {"text": "Canlı doğacak tüm çocuklarının istisnasız %100 Down sendromlu olacağı; çünkü spermlerin ya iki adet 21 taşıyacağı ya da hiç taşımayacağı (letal monozomi 21)", "isCorrect": True, "feedback": "Hayati ve kesin bilgi! Homolog rob(21;21) taşıyıcılarında normal gamet üretilemez; canlı doğumların %100'ü Down sendromlu olur."},
                {"text": "Down sendromu riskinin sadece %1 civarında olduğu", "isCorrect": False, "feedback": "Bu klasik serbest trizomi riskidir; rob(21;21)'de risk %100'dür."},
                {"text": "Erkek çocukların %100 sağlıklı, kız çocukların %100 hasta olacağı", "isCorrect": False, "feedback": "21. kromozom otozomdur, cinsiyet ayrımı yapmaz."}
            ]
        ),
        31: make_branching_logic(
            "38 yaşında primigravid bir gebeye ileri anne yaşı nedeniyle yapılan amniyosentez sonucunda fetal karyotip 47,XY,+21 olarak raporlanıyor. Anne ve babaya gebeliğin devamı ve Down sendromunun prognozu aktarılırken kalp hastalıkları ile ilgili verilecek en kritik bilgi nedir?",
            [
                {"text": "Canlı doğan Down sendromlu bebeklerin yaklaşık %40-50'sinde en sık AVSD (endokardiyal yastık defekti) olmak üzere kalp anomalisi görüldüğü ve doğum sonrası ilk haftalarda ekokardiyografi ile taranması gerektiği", "isCorrect": True, "feedback": "Kusursuz rehberlik! Konjenital kalp hastalıkları erken mortalitenin bir numaralı nedenidir ve ilk haftalarda cerrahi planlama hayat kurtarır."},
                {"text": "Down sendromunda kalp anomalisinin hiçbir zaman görülmediği", "isCorrect": False, "feedback": "Down sendromunda kalp defekti olguların neredeyse yarısında mevcuttur."},
                {"text": "Yalnızca Fallot tetralojisi görüldüğü ve ameliyat şansının hiç bulunmadığı", "isCorrect": False, "feedback": "En sık AVSD görülür ve cerrahi düzeltimle başarıyla tedavi edilir."}
            ]
        ),
        33: make_branching_logic(
            "Yeni doğan bir bebeğe klinik stigmaları nedeniyle Down sendromu ön tanısı koyuyorsunuz. Ailenin ilk çocuğu olan bu bebek için sitogenetik test planlarken izlenecek protokol nasıl olmalıdır?",
            [
                {"text": "Klinik tanı ne kadar net olursa olsun mutlaka periferik kandan karyotip analizi istenmeli; olgunun klasik serbest trizomi mi yoksa kalıtsal risk taşıyan bir translokasyon mu olduğu belirlenmelidir", "isCorrect": True, "feedback": "Doğru klinik genetik yaklaşımı! Karyotipik varyant belirlenmeden aileye sonraki gebelikler için rekürrens riski verilemez."},
                {"text": "Klinik tanı yeterlidir, genetik analize gerek duyulmadan sadece fizik tedaviye başlanmalıdır", "isCorrect": False, "feedback": "Karyotipik doğrulama yasal ve genetik açıdan zorunludur."},
                {"text": "Yalnızca idrarda metabolik tarama testi yapılması yeterlidir", "isCorrect": False, "feedback": "Down sendromu metabolik değil kromozomal bir anöploididir."}
            ]
        ),
        35: make_branching_logic(
            "Doğum odasında genel hipotonisi, brakisefalisi, yukarı çekik gözleri, Simian çizgisi ve sandal gap bulgusu olan bir bebeği muayene ediyorsunuz. Bebeğin batın muayenesinde doğumdan 4 saat sonra safralı kusma ve karın distansiyonu gelişiyor. Acil radyolojik değerlendirmede hangi anomali öncelikle aranmalıdır?",
            [
                {"text": "Ayakta direkt batın grafisinde 'çift kabarcık' (double bubble) manzarası veren duodenal atrezi veya duodenal stenoz", "isCorrect": True, "feedback": "Harika tıp muhakemesi! Down sendromunda safralı kusmanın bir numaralı cerrahi nedeni duodenal atrezidir ve çift kabarcık verir."},
                {"text": "Pilor stenozuna bağlı tek hava kabarcığı", "isCorrect": False, "feedback": "Pilor stenozunda kusma safrasızdır ve 3-4 haftalıkken başlar."},
                {"text": "Safra kesesi agenezisi", "isCorrect": False, "feedback": "Safra kesesi agenezisi akut safralı kusma tablosu yapmaz."}
            ]
        ),
        42: make_branching_logic(
            "Yenidoğan yoğun bakımda takip edilen bir kız bebekte belirgin oksiput çıkıntısı, clenched hand (2. ve 5. parmakların diğer parmaklar üzerine bindiği kenetlenmiş yumruk el) ve rocker-bottom ayak deformitesi saptanıyor. Nörolojik muayenede kas hipertonisitesi dikkati çekiyor. Bu hastanın ailesine prognoz hakkında nasıl bir bilgilendirme yapılmalıdır?",
            [
                {"text": "Klinik tablonun Trizomi 18 (Edwards sendromu) ile son derece uyumlu olduğu, olguların yaklaşık %50'sinin ilk hafta, %90'ının ise ilk bir yıl içinde kaybedildiği gerçeği empatik bir dille paylaşılmalıdır", "isCorrect": True, "feedback": "Doğru ve gerçekçi genetik bilgilendirme! Edwards sendromunda sağkalım son derece kısıtlıdır ve aile bu prognoza hazırlanmalıdır."},
                {"text": "Bebeğin tamamen sağlıklı olduğu ve birkaç gün içinde taburcu edileceği söylenmelidir", "isCorrect": False, "feedback": "Ağır malformasyonlar ve yüksek mortalite göz ardı edilemez."},
                {"text": "Bebeğin büyüyünce normal okula gidebileceği belirtilmelidir", "isCorrect": False, "feedback": "Edwards sendromunda derin mental retardasyon ve ağır mortalite mevcuttur."}
            ]
        ),
        45: make_branching_logic(
            "Obstetrik ultrasonda fetüste ön beynin iki hemisfere bölünemediği (holoprozensefali), mikroftalmi, bilateral yarık dudak/damak ve ellerde postaksiyel polidaktili saptanıyor. Bu karakteristik triad hangi otozomal trizominin varlığına işaret eder?",
            [
                {"text": "Trizomi 13 (Patau Sendromu); ön beyin bölünme kusuru ve karakteristik triad patognomoniktir", "isCorrect": True, "feedback": "Kusursuz tanı! Mikroftalmi + yarık damak + polidaktili triadı ve holoprozensefali Trizomi 13'ün klasik tablosudur."},
                {"text": "Trizomi 21 (Down Sendromu)", "isCorrect": False, "feedback": "Down sendromunda holoprozensefali veya mikroftalmi/polidaktili triadı beklenmez."},
                {"text": "Trizomi 18 (Edwards Sendromu)", "isCorrect": False, "feedback": "Edwards'ta clenched hand ve rocker-bottom ayak ön plandadır."}
            ]
        ),
        47: make_branching_logic(
            "Doğum sonrası muayenesinde saçlı deride parieto-oksipital bölgede zımba ile delinmiş gibi yuvarlak tam kat cilt defekti (kutis aplazi) ve göbek kordonu kökünde omfalosel saptanan bir bebekte alında alev hemanjiomları izleniyor. Bu kutanöz stigmalar hangi sendromu destekler?",
            [
                {"text": "Patau Sendromu (Trizomi 13); kutis aplazi ve omfalosel sendromun en spesifik ek bulgularındandır", "isCorrect": True, "feedback": "Harika klinik eşleştirme! Kutis aplazi ve omfalosel birlikteliği Trizomi 13 için son derece karakteristiktir."},
                {"text": "Turner Sendromu (45,X)", "isCorrect": False, "feedback": "Turner'da kutis aplazi veya omfalosel görülmez; yele boyun görülür."},
                {"text": "Klinefelter Sendromu (47,XXY)", "isCorrect": False, "feedback": "Klinefelter'da yenidoğanda cilt defekti olmaz."}
            ]
        ),
        53: make_branching_logic(
            "Yenidoğan polikliniğine getirilen 1 aylık bir kız bebeğin ağlamasının tıpkı aç bir kedi miyavlamasını andıran tiz ve monoton karakterde olduğu fark ediliyor. Muayenede belirgin mikrosefali ve yuvarlak 'ay yüz' saptanıyor. Bu bebeğin ebeveynlerine ağlama sesinin geleceği hakkında ne söylenmelidir?",
            [
                {"text": "Larinks kıkırdaklarının büyümesi ve olgunlaşmasıyla bu karakteristik kedi ağlaması sesinin çocukluk ve erişkinlik döneminde kaybolacağı", "isCorrect": True, "feedback": "Kusursuz tıp bilgisi! Cri du chat'daki tiz kedi miyavlaması sesi bebeklik dönemine özgüdür ve yaşla kaybolur."},
                {"text": "Bu sesin ömür boyu hiçbir değişikliğe uğramadan aynı tonda kalacağı", "isCorrect": False, "feedback": "Ağlama sesi yaşla birlikte mutlaka kaybolur ve ses kalınlaşır."},
                {"text": "Sesin derhal ameliyatla düzeltilmesi gerektiği, aksi halde çocuğun nefes alamayacağı", "isCorrect": False, "feedback": "Larinks hipoplazisi acil cerrahi gerektirmez; maturasyonla ses evrilir."}
            ]
        ),
        55: make_branching_logic(
            "Geniş burun köprüsünün alınla kesintisiz birleştiği 'Yunan savaşçı miğferi' (Greek warrior helmet) yüz görünümü sergileyen, balık ağzı deformitesi olan ve erken süt çocukluğunda inatçı epileptik nöbetler geçiren bir bebekte standart karyotip normal raporlanıyor. Klinisyenin bir sonraki adımı ne olmalıdır?",
            [
                {"text": "del(4)(p16.3) delesyonunu (Wolf-Hirschhorn sendromu) saptamak amacıyla 4p bölgesine yönelik FISH veya Kromozomal Mikroarray (CMA) analizi istemek", "isCorrect": True, "feedback": "Kusursuz genetik yönetim! Wolf-Hirschhorn delesyonu submikroskobik olabilir ve standart karyotipte gözden kaçabilir; FISH/CMA şarttır."},
                {"text": "Hastaya sadece antiepileptik ilaç başlayıp genetik incelemeyi kapatmak", "isCorrect": False, "feedback": "Etiyolojik sendrom aydınlatılmadan takip eksik kalır."},
                {"text": "Bebeğe acilen nazogastrik tüp takıp karyotipi tekrarlamak", "isCorrect": False, "feedback": "Karyotip yerine daha yüksek çözünürlüklü moleküler sitogenetik (FISH/CMA) gereklidir."}
            ]
        ),
        57: make_branching_logic(
            "Yenidoğan servisinde 3 günlük bir bebekte inatçı konvülsiyonlar gelişiyor; laboratuvarda ağır hipokalsemi (Ca: 5.8 mg/dL) ve parathormon düşüklüğü saptanıyor. Ekokardiyografide kesintili aort yayı ve Fallot tetralojisi bulunan bebekte timus gölgesi izlenemiyor. Bu hastada hangi genetik bozukluktan şüphelenilmelidir?",
            [
                {"text": "22q11.2 mikrodelesyonu (DiGeorge / Velokardiyofasiyal sendrom); paratiroid ve timus aplazisi ile konotrunkal kalp anomalisi CATCH-22 tablosudur", "isCorrect": True, "feedback": "Mükemmel klinik tanı! Paratiroid aplazisi (hipokalsemi), timus yokluğu ve konotrunkal kalp defekti DiGeorge sendromunun patognomonik tablosudur."},
                {"text": "Down Sendromu (Trizomi 21)", "isCorrect": False, "feedback": "Down sendromunda timus aplazisi veya konjenital hipokalsemi beklenmez."},
                {"text": "Turner Sendromu (45,X)", "isCorrect": False, "feedback": "Turner'da timus aplazisi ve hipokalsemik tetani görülmez."}
            ]
        ),
        58: make_branching_logic(
            "Pediatrik kardiyolojide Supravalvüler Aort Stenozu (SVAS) tanısı alan 6 yaşında bir kız çocuğunun muayenesinde peri yüzü (elfin facies), yıldızsı iris ve yabancılara karşı aşırı samimi, konuşkan bir 'kokteyl partisi kişiliği' sergilediği görülüyor. Bu hastada silinen kritik gen hangisidir?",
            [
                {"text": "7q11.23 bölgesinde yer alan ve vasküler elastikiyeti sağlayan Elastin (ELN) geni", "isCorrect": True, "feedback": "Kusursuz moleküler eşleştirme! Williams sendromundaki SVAS ve peri yüzü tablosu 7q11.23'teki Elastin (ELN) geni delesyonuna bağlıdır."},
                {"text": "22q11.2 bölgesindeki TBX1 geni", "isCorrect": False, "feedback": "TBX1 DiGeorge genidir, kokteyl kişiliği veya SVAS yapmaz."},
                {"text": "17p12 bölgesindeki PMP22 geni", "isCorrect": False, "feedback": "PMP22 periferik sinir miyelin genidir."}
            ]
        ),
        63: make_branching_logic(
            "30 yaşında uzun boylu, bacakları gövdesine göre orantısız uzun (önökoid), bilateral jinekomastisi olan ve 2 yıllık evlilikte çocuk sahibi olamayan bir erkeğin semen analizinde azospermi saptanıyor. Testis boyutları bilateral 2.5 ml ve sert kıvamda ölçülüyor. Bu hastada öncelikle hangi karyotipik anöploididen şüphelenilmelidir?",
            [
                {"text": "Klinefelter Sendromu (47,XXY); seminifer tübül hiyalinizasyonu, azospermi ve hipergonadotropik hipogonadizm klasik tablosudur", "isCorrect": True, "feedback": "Tam isabet! Önökoid uzun boy, küçük sert testis, azospermi ve jinekomasti Klinefelter sendromunun (47,XXY) prototipidir."},
                {"text": "47,XYY Sendromu", "isCorrect": False, "feedback": "47,XYY erkekleri genelde fertildir; testis boyutları normaldir ve jinekomasti görülmez."},
                {"text": "Turner Sendromu (45,X)", "isCorrect": False, "feedback": "Turner dişi fenotipindedir ve boy kısadır."}
            ]
        ),
        67: make_branching_logic(
            "Adölesan dönemde aşırı uzun boy ve hafif dikkat dağınıklığı nedeniyle incelenen 16 yaşında bir erkekte karyotip 47,XYY olarak raporlanıyor. Aile gelecekte çocuk sahibi olup olamayacağını soruyor. Verilecek en doğru bilimsel yanıt nedir?",
            [
                {"text": "Klinefelter sendromunun aksine 47,XYY erkeklerinin çoğunlukla fertil olduğu, normal sperm üretebildikleri ve doğal yolla sağlıklı çocuk sahibi olabilecekleri", "isCorrect": True, "feedback": "Kusursuz genetik danışmanlık! 47,XYY sendromunda testis fonksiyonu ve sperm üretimi genellikle tamamen normaldir."},
                {"text": "Hastanın mutlak kısır olduğu ve asla sperm üretemeyeceği", "isCorrect": False, "feedback": "Kalıcı azospermi ve kısırlık 47,XYY'de değil 47,XXY'de (Klinefelter) görülür."},
                {"text": "Doğacak tüm erkek çocuklarının iki başlı olacağı", "isCorrect": False, "feedback": "Tıbbi dayanağı olmayan gerçek dışı bir ifadedir."}
            ]
        ),
        71: make_branching_logic(
            "16 yaşında boy kısalığı (138 cm) ve henüz hiç adet görmeme (primer amenore) şikayetiyle başvuran bir genç kızın muayenesinde yele boyun kalıntısı, kalkan göğüs, kubitus valgus ve kolda yüksek tansiyon (155/95 mmHg) saptanıyor. Bu hastada kesin tanı için istenmesi gereken ilk sitogenetik test hangisidir?",
            [
                {"text": "Periferik kandan lenfosit kültürü ile Karyotip Analizi (45,X ve varyantlarını saptamak amacıyla)", "isCorrect": True, "feedback": "Kusursuz klinik karar! Kısa boy, primer amenore ve yele boyun klasik Turner sendromudur; kesin tanı periferik karyotip analiziyle konur."},
                {"text": "Sadece el bilek grafisi çekip kemik yaşı tayini yapmak", "isCorrect": False, "feedback": "Kemik yaşı gecikmeyi gösterir ancak etiyolojik sitogenetik tanıyı koyamaz."},
                {"text": "Doğrudan tanısal laparoskopiye almak", "isCorrect": False, "feedback": "Non-invaziv karyotip varken cerrahi laparoskopi tanı için yapılmaz."}
            ]
        ),
        75: make_branching_logic(
            "Turner sendromlu bir hastanın pelvik ultrasonografisinde overlerin yerinde fibröz beyaz bağ dokusu bantları (çizgi gonad) izleniyor. Laboratuvarında FSH: 98 mIU/ml, LH: 45 mIU/ml ve Östradiol: <10 pg/ml saptanıyor. Bu hastanın tedavisinde sekonder seks karakterlerini başlatmak için ilk tercih edilecek hormon hangisidir?",
            [
                {"text": "Düşük doz oral veya transdermal Östrojen tedavisi (meme gelişimini ve uterus büyümesini başlatmak amacıyla)", "isCorrect": True, "feedback": "Mükemmel endokrinolojik yönetim! Puberte indüksiyonu için ilk olarak tek başına östrojen başlanır; 2 yıl sonra progesteron eklenir."},
                {"text": "Doğrudan yüksek doz testosteron tedavisi", "isCorrect": False, "feedback": "Testosteron virilizasyona yol açar; dişi sekonder seks gelişiminde yeri yoktur."},
                {"text": "Yalnızca tiroid hormonu (L-tiroksin) verilmesi", "isCorrect": False, "feedback": "Tiroid hormonu hipogonadizmi düzeltemez."}
            ]
        ),
        80: make_branching_logic(
            "Turner sendromu fenotipiyle takip edilen 13 yaşında bir hastanın sitogenetik incelemesinde karyotip 45,X / 46,XY mozaik olarak raporlanıyor. Genetik konseyinde bu hasta için cerrahi açıdan tartışılması gereken en hayati öneri ne olmalıdır?",
            [
                {"text": "Disgenezik çizgi gonadda %20-30 oranında Gonadoblastom ve Disgerminom gelişme riski bulunduğundan profilaktik bilateral gonadektomi (gonadların cerrahi olarak çıkarılması) yapılması", "isCorrect": True, "feedback": "Hayat kurtaran onkogenetik karar! Y kromozomu taşıyan disgenezik gonadlarda gonadoblastom riski çok yüksektir; acil cerrahi gonadektomi endikedir."},
                {"text": "Y kromozomunun hiçbir zararı olmadığı için cerrahiden tamamen kaçınılması", "isCorrect": False, "feedback": "Malignite riski %30'a varır; cerrahi yapılmazsa tümör gelişir."},
                {"text": "Hastaya derhal yüksek doz kemoterapi başlanması", "isCorrect": False, "feedback": "Tümör gelişmeden kemoterapi verilmez; profilaktik cerrahi yeterlidir."}
            ]
        ),
        85: make_branching_logic(
            "Doğumda ağır hipotonisi ve emme güçlüğü olan, mikropenis saptanan bir erkek bebek 3 yaşına geldiğinde kilitli dolapları kırarak sürekli yemek arayan, doyumsuz bir iştah (hiperfaji) ve hızlı kilo alımı sergiliyor. Bu hastada kesin genetik tanı için ilk basamakta hangi moleküler test istenmelidir?",
            [
                {"text": "15q11-q13 bölgesine yönelik DNA Metilasyon Analizi (MS-PCR veya MS-MLPA; Prader-Willi sendromunun hem delesyon hem UPD olgularını %99 yakalar)", "isCorrect": True, "feedback": "Mükemmel tanısal algoritma! PWS şüphesinde ilk basamak test DNA metilasyon analizidir; epigenetik susturulmayı net gösterir."},
                {"text": "Yalnızca serum leptin ve ghrelin düzeylerinin ölçülmesi", "isCorrect": False, "feedback": "Hormon düzeyleri genetik tanıyı koyamaz."},
                {"text": "Rutin kranial tomografi çekilmesi", "isCorrect": False, "feedback": "Kranial BT genetik delesyonu veya imprintingi gösteremez."}
            ]
        ),
        87: make_branching_logic(
            "4 yaşında bir çocuk derin zihinsel yetersizlik, hiç konuşamama, kollarını dirsekten bükerek el çırpma hareketleri, kukla benzeri sarsak ataksi ve nedensiz kahkaha krizleri sergiliyor. Genetik analizde maternal 15q11-q13 delesyonu ve UBE3A kaybı saptanıyor. Aileye bu hastalığın Prader-Willi sendromundan farkı nasıl anlatılmalıdır?",
            [
                {"text": "Aynı kromozomal bölgenin (15q11-q13) kaybı babadan gelirse Prader-Willi sendromu, anneden gelirse Angelman sendromu geliştiği; bunun nedeninin genomik imprinting (ebeveynsel damgalama) olduğu", "isCorrect": True, "feedback": "Kusursuz genetik entegrasyon! 15q11 delesyonunun paternali Prader-Willi, maternali Angelman sendromu tablosunu doğurur."},
                {"text": "Prader-Willi ve Angelman'ın aynı sendrom olduğu ve tedavilerinin tamamen aynı olduğu", "isCorrect": False, "feedback": "Klinik tabloları ve genetik mekanizmaları tamamen zıttır."},
                {"text": "Angelman sendromunun yalnızca beslenme fazlalığından kaynaklandığı", "isCorrect": False, "feedback": "Angelman ağır bir nörogenetik tablodur, beslenmeyle ilişkisizdir."}
            ]
        )
    }

def get_extra_causal_chains():
    """Ekstra mekanizma zincirleri (causal_chain)."""
    return {
        6: make_causal_chain(
            "Triploidi Oluşum ve Fetal Seleksiyon Zinciri",
            [
                "1. Oosit iki ayrı sperm tarafından eş zamanlı döllenir (dispermi)",
                "2. Zigotta 3 tam haploid takım (69 kromozom) bir araya gelir",
                "3. Paternal ve maternal gen dozajı dengesi embriyonik dokularda çöker",
                "4. Ağır plasental veya fetal malformasyon nedeniyle konsepsiyonun %99'u 1. trimesterde spontan düşer"
            ]
        ),
        15: make_causal_chain(
            "Eşit Olmayan Krossing-Over (NAHR) Zinciri",
            [
                "1. Mayoz I'de homolog kromozomlardaki düşük kopya tekrarları (LCR) yanlış hizalanır",
                "2. Yanlış hizalanmış LCR dizileri arasında alelik olmayan krossing-over gerçekleşir",
                "3. Kromatitlerden biri çift segment alarak duplikasyonlu (parsiyel trizomi) hale gelir",
                "4. Diğer kromatit ilgili segmenti tamamen kaybederek delesyonlu (parsiyel monozomi) gamet üretir"
            ]
        ),
        26: make_causal_chain(
            "rob(14;21) Paternal Sperm Seleksiyon Zinciri",
            [
                "1. rob(14;21) taşıyıcısı erkekte mayoz sonucu disomik (14;21 türevli) spermler üretilir",
                "2. Anormal kromozomal yük taşıyan disomik spermatozoa morfolojik ve fonksiyonel stres yaşar",
                "3. Kadın genital traktusunda ve servikal mukusta motilite yarışında disomik spermler geride kalır",
                "4. Normal veya dengeli spermler oositi döllediğinden babadaki ampirik Down riski %4-5'e iner"
            ]
        ),
        36: make_causal_chain(
            "Down Sendromunda Lösemi Gelişim Zinciri",
            [
                "1. Fetal hematopoez sırasında 21. kromozomdaki DYRK1A ve ETS genleri aşırı ifade edilir",
                "2. Fetal karaciğerde megakaryositer progenitörlerde somatik GATA1 mutasyonu kazanılır",
                "3. Yenidoğanda geçici miyeloproliferatif hastalık (TMD / geçici lösemi) tablosu ortaya çıkar",
                "4. Ek genetik mutasyonların birikmesiyle ilk 3 yaşta Akut Megakaryoblastik Lösemiye (AML-M7) dönüşür"
            ]
        ),
        64: make_causal_chain(
            "Klinefelter Hipergonadotropik Hipogonadizm Zinciri",
            [
                "1. Pubertede seminifer tübüllerde aşırı X kromatini etkisiyle hiyalinizasyon ve skleroz başlar",
                "2. Sertoli hücreleri dejenere olur ve serum İnhibin B düzeyi saptanamayacak düzeye iner",
                "3. Hipofiz üzerindeki negatif geri bildirim kalkar ve pulsatil FSH deşarjı tavan yapar",
                "4. Leydig hücre hasarıyla testosteron düşer; aşırı yükselen LH ile hipergonadotropik hipogonadizm kurulur"
            ]
        ),
        76: make_causal_chain(
            "Turner Sendromunda Aort Diseksiyonu Zinciri",
            [
                "1. Embriyonik sol kalp akım defekti sonucu biküspit aort kapağı ve aort koarktasyonu gelişir",
                "2. Asendan aort duvarında elastik lif displazisi ve kistik medial dejenerasyon başlar",
                "3. Koarktasyon ve renal anomali zemininde kronik üst ekstremite hipertansiyonu eklenir",
                "4. İlerleyici aort dilatasyonu intima tabakasında yırtılmaya ve ölümcül aort diseksiyonuna yol açar"
            ]
        ),
        86: make_causal_chain(
            "Prader-Willi Sendromunda Morbid Obezite Zinciri",
            [
                "1. Paternal 15q11-q13 bölgesindeki snoRNA kümesinin (SNORD116) eksikliği gelişir",
                "2. Hipotalamus arkuat nükleusta tokluk sinyalleri (POMC/CART) baskılanır",
                "3. Mideden salgılanan primer açlık hormonu 'ghrelin' dolaşımda kronik olarak aşırı yükselir",
                "4. Doyumsuz hiperfaji başlar; kontrolsüz aşırı gıda alımıyla hızlı morbid obezite ve diyabet gelişir"
            ]
        ),
        96: make_causal_chain(
            "Translokasyon Down Ebeveyn Ayrılma Zinciri",
            [
                "1. Yenidoğanda rob(14;21) saptanır ve ebeveynlerden periferik kan karyotipi alınır",
                "2. Annenin 45,XX,rob(14;21) dengeli taşıyıcısı olduğu sitogenetik olarak doğrulanır",
                "3. Oogenez mayozunda trivalan kompleksi kurularak %15 oranında disomik 21 oosit üretilir",
                "4. Aileye sonraki gebelikler için %15 Down riski verilir ve IVF eşliğinde PGT-SR seçeneği sunulur"
            ]
        )
    }


def get_extra_sliders():
    """Ekstra önce-sonra / karşılaştırma kaydırıcıları (before_after_slider) - 12 adet"""
    return {
        7: make_before_after(
            "Diandri vs Digini Triploidi Karşılaştırması",
            "Diandri (Baba Kökenli Ekstra Takım)",
            [
                "Ekstra haploid kromozom takımı babadan gelir (dispermi)",
                "Büyük, ödemli ve kistik plasenta (parsiyel mol hidatiform)",
                "Fetüs orantılı büyüme geriliği gösterir veya mikrofetüstür",
                "Maternal kanda beta-hCG ve AFP düzeyleri aşırı yüksektir"
            ],
            "Digini (Anne Kökenli Ekstra Takım)",
            [
                "Ekstra haploid kromozom takımı anneden gelir (diploid oosit)",
                "Çok küçük, sert ve fibrotik non-molar plasenta",
                "Fetüste belirgin baş-gövde asimetrisi (büyük kafa, cılız gövde)",
                "Maternal kanda beta-hCG düzeyleri son derece düşüktür"
            ]
        ),
        14: make_before_after(
            "Mayoz I vs Mayoz II Ayrılma Hatalarının Genetik Çıktısı",
            "Mayoz I Ayrılamama Çıktısı",
            [
                "Homolog kromozom çifti ayrılamaz",
                "Oluşan gametlerin %100'ü anormaldir (2 adet n+1, 2 adet n-1)",
                "Gamet iki farklı parental homolog taşır (heterodizomi)",
                "Maternal Down sendromu olgularının %90'ından sorumludur"
            ],
            "Mayoz II Ayrılamama Çıktısı",
            [
                "Kardeş kromatitler birbirinden ayrılamaz",
                "Oluşan gametlerin %50'si normaldir (2 adet n, 1 adet n+1, 1 adet n-1)",
                "Gamet aynı ebeveynin özdeş kopyasını taşır (izodizomi)",
                "47,XYY sendromunun temel paternal mekanizmasıdır"
            ]
        ),
        24: make_before_after(
            "Cri du Chat vs Wolf-Hirschhorn Delesyon Sendromları",
            "Cri du Chat Sendromu [del(5p)]",
            [
                "5. kromozomun kısa kolunun terminal delesyonudur (5p15)",
                "Larenks hipoplazisine bağlı kedi miyavlaması tarzı ağlama",
                "Yuvarlak ay yüzü, mikrosefali ve hipertelorizm tipiktir",
                "Olguların çoğunda standart karyotipte delesyon çıplak gözle seçilir"
            ],
            "Wolf-Hirschhorn Sendromu [del(4p)]",
            [
                "4. kromozomun kısa kolunun terminal delesyonudur (4p16.3)",
                "Geniş glabella ve yüksek burun köküyle 'Yunan miğferi' yüzü",
                "Ağız köşelerinin aşağı baktığı karakteristik 'balık ağzı' görünümü",
                "Submikroskobik olabileceğinden tanıda FISH veya mikrodizi şarttır"
            ]
        ),
        34: make_before_after(
            "Resiprokal vs Robertsonian Translokasyon",
            "Resiprokal Translokasyon",
            [
                "Homolog olmayan herhangi iki kromozom arasında gerçekleşir",
                "Toplam kromozom sayısı genellikle 46 olarak korunur",
                "Mayoz profaz I'de haç şeklinde kuadrivalan yapısı kurulur",
                "Tüm genomda dengesiz gamet riski taşır"
            ],
            "Robertsonian Translokasyon",
            [
                "Yalnızca akrosentrik kromozomlar arasında (13, 14, 15, 21, 22) olur",
                "Sentrik füzyon sonrası toplam kromozom sayısı 45'e düşer",
                "Kısa kollardaki satellit ve rRNA genleri dökülerek kaybolur",
                "İnsan türündeki en yaygın yapısal kromozom anomalisidir"
            ]
        ),
        42: make_before_after(
            "Serbest Trizomi 21 vs Translokasyon Down Sendromu",
            "Serbest Trizomi 21 (%95)",
            [
                "Karyotip 47,XX,+21 veya 47,XY,+21'dir (ayrı bir serbest kromozom)",
                "İleri anne yaşı ile doğrudan ve eksponansiyel ilişkilidir",
                "Ekstra kromozom %90 anne Mayoz I ayrılamamasından kaynaklanır",
                "Tekrarlama riski genç annelerde yaklaşık %1 civarındadır"
            ],
            "Translokasyon Down (%4)",
            [
                "Karyotip 46 kromozomludur [der(14;21) veya der(21;21)]",
                "ANNE YAŞINDAN TAMAMEN BAĞIMSIZDIR",
                "Olguların yarısında ebeveynlerden biri dengeli taşıyıcıdır",
                "Anne taşıyıcıysa rekürrens riski %15, homologta %100'dür"
            ]
        ),
        52: make_before_after(
            "Down Sendromu vs Edwards Sendromu Nöromüsküler Tablosu",
            "Down Sendromu (Trizomi 21)",
            [
                "Belirgin genel hipotoni (floppy infant tablosu)",
                "Zayıf Moro refleksi ve yaygın eklem laksisitesi",
                "Düzleşmiş oksiput (brakisefali) ve yassı burun kökü",
                "El ayasında tek transvers palmar çizgi (simian çizgisi)"
            ],
            "Edwards Sendromu (Trizomi 18)",
            [
                "Belirgin genel hipertonisite ve fleksiyon kontraktürleri",
                "Sert ve rijid ekstremite postürü, zayıf emme refleksi",
                "Prominent (geriye doğru çıkıntılı) belirgin oksiput kemiği",
                "Parmakların üst üste bindiği sıkılı yumruk (clenched hand)"
            ]
        ),
        57: make_before_after(
            "Edwards Sendromu vs Patau Sendromu Klinik Triadları",
            "Edwards Sendromu Triadı (Trizomi 18)",
            [
                "Parmakların üst üste binmesi (Clenched hand: 2>3, 5>4)",
                "Kavisli beşik taban ayak deformitesi (Rocker-bottom ayak)",
                "Çıkıntılı oksiput ve aşırı küçük alt çene (mikrognati)",
                "Kısa sternum ve kardiyak septum defektleri (%90+ VSD/PDA)"
            ],
            "Patau Sendromu Triadı (Trizomi 13)",
            [
                "Göz küresinin ileri derecede küçük kalması (Mikroftalmi/Anoftalmi)",
                "Orta hatta geniş bilateral yarık dudak ve yarık damak",
                "Ellerde ve ayaklarda ilave parmak (Postaksiyel polidaktili)",
                "Ön beynin bölünememesi (Holoprozensefali) ve kutis aplazi"
            ]
        ),
        65: make_before_after(
            "Klinefelter Sendromu (47,XXY) vs Normal Erkek (46,XY)",
            "Klinefelter Sendromlu Erkek",
            [
                "Gecikmiş epifiz kapanması ve önokoid uzun kol-bacaklar",
                "Seminifer tübül hiyalinizasyonu ve mutlak azoospermi",
                "Küçük taş gibi sert testisler (<4 ml) ve jinekomasti (%50)",
                "Hipergonadotropik hipogonadizm (FSH/LH yüksek, testosteron düşük)"
            ],
            "Normal Karyotipli Erkek",
            [
                "Zamanında epifiz kapanması ve normal beden oranları",
                "Aktif spermatogenez ve normal sperm parametreleri",
                "Normal elastik kıvamda testis hacmi (>15-25 ml)",
                "Dengeli hipofiz-gonad aksı ve normal androjen düzeyleri"
            ]
        ),
        72: make_before_after(
            "Turner Sendromu (45,X) vs Klinefelter Sendromu (47,XXY)",
            "Turner Sendromu (45,X)",
            [
                "Kız fenotipinde gonozomal monozomidir (canlı doğan tek monozomi)",
                "SHOX kaybına bağlı belirgin boy kısalığı ve kubitus valgus",
                "Hızlanmış oosit atrezisine bağlı çizgi gonad ve primer amenore",
                "Biküspit aort kapağı, aort koarktasyonu ve at nalı böbrek"
            ],
            "Klinefelter Sendromu (47,XXY)",
            [
                "Erkek fenotipinde gonozomal trizomidir (ekstra X kromozomu)",
                "Uzun bacaklar, önokoid boy uzunluğu ve jinekomasti",
                "Tübüler hiyalinizasyona bağlı küçük sert testis ve azoospermi",
                "20-50 kat artmış meme kanseri ve mediastinal teratom riski"
            ]
        ),
        86: make_before_after(
            "Prader-Willi Sendromu vs Angelman Sendromu",
            "Prader-Willi Sendromu (PWS)",
            [
                "Paternal 15q11-q13 delesyonu (%70) veya Maternal UPD 15 (%30)",
                "İnfantta şiddetli hipotoni ve emme zayıflığı ile başlar",
                "Çocuklukta doymak bilmez hiperfaji ve morbid obezite gelişir",
                "Hipogonadizm, küçük el-ayaklar (akromikri) ve badem gözler tipiktir"
            ],
            "Angelman Sendromu (AS)",
            [
                "Maternal 15q11-q13 delesyonu (%70) veya Paternal UPD 15 (%5)",
                "Beyinde maternal aktif UBE3A geninin kaybı sonucu gelişir",
                "Uygunsuz paroksismal kahkahalar ve sürekli mutlu mizaç hakimdir",
                "Konuşma yokluğu (dilsizlik), ataksik sarsıntılı yürüyüş ve epilepsi"
            ]
        ),
        94: make_before_after(
            "cfDNA / NIPT Taraması vs Amniyosentez Tanısı",
            "Hücresiz Fetal DNA (cfDNA / NIPT)",
            [
                "Maternal koldan kan alınarak yapılan non-invaziv bir TARAMA testidir",
                "Kaynağı fetüsün kendisi değil, plasental trofoblast hücreleridir",
                "İşleme bağlı düşük riski kesinlikle sıfırdır",
                "Pozitif çıktığında terminasyon için mutlaka invaziv teyit gerektirir"
            ],
            "Amniyosentez (AS)",
            [
                "15-20. haftalarda amniyon sıvısının aspire edildiği İNVAZİV TANI testidir",
                "Doğrudan fetüsün dökülen amniyositleri incelendiğinden altındır",
                "Tecrübeli ellerde yaklaşık 1/500-1/1000 fetal kayıp riski taşır",
                "Sitogenetik sonucu kesin tanı koydurur, ilave teyit gerektirmez"
            ]
        ),
        96: make_before_after(
            "Konvansiyonel Karyotip vs Kromozomal Mikrodizi (CMA)",
            "Konvansiyonel Karyotip (G-Bantlama)",
            [
                "Çözünürlüğü düşüktür (>5-10 Mb büyüklüğündeki lezyonları görür)",
                "Dengeli translokasyon ve inversiyonları saptayabilen tek rutin yöntemdir",
                "Canlı hücre kültürü gerektirir (sonuç süresi 7-14 gündür)",
                "Submikroskobik mikrodelesyonları (>5 Mb altı) kesinlikle tespit edemez"
            ],
            "Kromozomal Mikrodizi (CMA / aCGH)",
            [
                "Çözünürlüğü çok yüksektir (>50-100 kb mikrodelesyonları yakalar)",
                "DENGELİ TRANSLOKASYONLARI VE İNVERSİYONLARI KESİNLİKLE GÖREMEZ",
                "Kültür gerektirmez, doğrudan DNA ekstraksiyonuyla 3-5 günde sonuçlanır",
                "Açıklanamayan zeka geriliği ve otizmde birinci basamak tetkiktir"
            ]
        )
    }
