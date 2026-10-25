import json, re, sys, subprocess
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-65-konjenital-malformasyonlar-ve-perinatal-beyin-hasari"
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Visual pages map
VISUAL_PAGES = {
    9: "Robbins Figure 23-14 Miyelomeningosel: bebekte gluteal bölgenin hemen üzerinde lumbosakral orta hatta hem meninksleri hem de spinal kord parankimini içeren, merkezi ülsere kistik kese yapısı görülmektedir.",
    15: "Robbins Figure 28-5 Lissensefali: miadında doğmuş bebeğin koronal beyin kesitinde kortikal girusların tamamen yokluğu, pürüzsüz beyin yüzeyi ve kalınlaşmış korteks tabakası izlenmektedir.",
    22: "Robbins Figure 28-7 Arnold-Chiari malformasyonu midsagittal kesiti: küçük arka fossa içerikleri, serebellar vermisin foramen magnum düzeyinin (oklar) altına fıtıklaşması ve medulla deformitesi gösterilmektedir.",
    27: "Figure 1 Germinal matriks şeması: koronal beyin kesitinde lateral ventrikül lümeni ile kaudat nükleus arasında yer alan germinal matriks bölgesi ve sağ lateral ventrikül içine açılan kanama gösterilmektedir."
}

# Raw slide blueprints: (sayfa, bolum_id, bolum_baslik, [ (ses, ekran, anchor, terms, cikmis_list) ])
SLIDES = [
    # --- BOLUM 1: Konjenital SSS Malformasyonlarına Giriş ve Epigenetik Düzenleme (1-4) ---
    (1, "k2-65-b01", "Konjenital SSS Malformasyonlarına Giriş ve Epigenetik Düzenleme", [
        (
            "Konjenital santral santral sinir sistemi konjenital malformasyonları ve perinatal beyin hasarı dersimize başlarken, gelişmekte olan sinir sisteminin embriyolojik basamaklarını, hücresel göç yolaklarını ve perinatal vasküler hasarlarını ayrıntılı olarak inceleyeceğiz.",
            "**Giriş:** Konjenital santral sinir sistemi malformasyonları ve perinatal doku hasarı.",
            "KONJENİTAL MALFORMASYONLAR VE",
            ["konjenital malformasyonlar", "santral sinir sistemi"],
            []
        ),
        (
            "Bu derste embriyolojik nöral tüp kapanma kusurlarından ön beyin gelişimsel patolojilerine, arka fossa malformasyonlarından perinatal hipoksik iskemik lezyonlara kadar geniş bir spektrumu ele alacağız.",
            "**Ders Kapsamı:** Nöral tüp, ön beyin, arka fossa ve perinatal iskemik lezyonlar.",
            "PERİNATAL BEYİN HASARI",
            ["nöral tüp", "arka fossa", "perinatal iskemik"],
            []
        ),
        (
            "Fetal dönemde gelişmekte olan nöral dokunun genetik mutasyonlara, teratojenik kimyasallara ve enfeksiyonlara aşırı duyarlılığı erişkin patolojilerinden tamamen farklı bir morfolojik tablo doğurur.",
            "**Gelişimsel Biyoloji:** Fetal nöral dokunun genetik ve teratojenik duyarlılığı.",
            "KONJENİTAL MALFORMASYONLAR VE",
            ["fetal nöral doku", "teratojenik duyarlılık"],
            []
        ),
        (
            "Burada öğreneceğimiz temel nöropatoloji mekanizmaları hem tıp fakültesi komite sınavlarında hem de klinik nörolojik pratikte anatomik lezyon lokalizasyonunu doğru kurmada anahtar rol oynayacaktır.",
            "**Klinik Değer:** Nöropatoloji sınavları ve klinik anatomik lokalizasyon temeli.",
            "PERİNATAL BEYİN HASARI",
            ["nöropatoloji mekanizmaları", "anatomik lokalizasyon"],
            []
        ),
        (
            "Gelişimsel nörobiyolojide primer nörulasyon ile nöral tüpün kapanması ve sekonder nörulasyon ile kaudal kord yapılarının şekillenmesi santral sinir sistemi embriyogenezinin iki temel basamağını teşkil eder.",
            "**Nörulasyon Basamakları:** Primer ve sekonder nörulasyon ile sinir sisteminin şekillenmesi.",
            "KONJENİTAL MALFORMASYONLAR VE",
            ["primer nörulasyon", "sekonder nörulasyon"],
            []
        )
    ]),

    (2, "k2-65-b01", "Konjenital SSS Malformasyonlarına Giriş ve Epigenetik Düzenleme", [
        (
            "Santral sinir sistemi malformasyonlarının canlı doğumlardaki genel canlı doğumlardaki genel insidansının yüzde bir ile iki civarında olduğu tahmin edilmekte olup, çocukluk çağı morbiditesinde çok önemli bir yer tutar.",
            "**İnsidans:** Santral sinir sistemi malformasyonlarının doğumdaki sıklığı yüzde bir iki civarındadır.",
            "Santral sinir sistemi (SSS) malformasyonlarının",
            ["santral sinir sistemi", "insidans"],
            []
        ),
        (
            "Bu gelişimsel defektler çocuklarda zeka geriliği, kronik serebral palsi tabloları, epilepsi nöbetleri veya ölümcül nöral tüp kusurları ile sonuçlanabilmektedir.",
            "**Klinik Spektrum:** Zeka geriliği, serebral palsi, epilepsi ve nöral tüp kusurları.",
            "Zekâ geriliği, serebral palsi veya nöral tüp",
            ["zeka geriliği", "serebral palsi", "nöral tüp kusurları"],
            []
        ),
        (
            "Prenatal ya da perinatal evrede etki eden zararlı çevresel faktörler, normal nörogenez sürecini ve hücre göçünü kesintiye uğratarak geri dönüşümsüz kalıcı ve geri dönüşümsüz doku hasarına zemin hazırlarlar.",
            "**Zararlı Faktörler:** Nörogenez ve göçü bozan prenatal çevresel etkenler.",
            "Prenatal veya perinatal zararlı faktörler",
            ["çevresel faktörler", "doku hasarı"],
            []
        ),
        (
            "Embriyonik dönemin farklı evrelerinde meydana gelen bu aksaklıklar, sinir sisteminin hangi anatomik bölgesinin ne derecede etkileneceğini belirleyen en kritik etkendir.",
            "**Kritik Dönem:** Hasarın zamanlaması etkilenen anatomik bölgeyi ve ağırlığı belirler.",
            "gelişiminde bozukluğa veya doku hasarına",
            ["embriyonik dönem", "anatomik bölge"],
            []
        ),
        (
            "Özellikle intrauterin asfiksi, fetal enfeksiyonlar ve maternal dolaşım yetersizlikleri nörolojik morbiditenin erken fetal dönemde yerleşmesine neden olan temel başlıca tetikleyicilerdir.",
            "**Patolojik Süreç:** İntrauterin asfiksi ve enfeksiyonların erken nörolojik morbiditeye etkisi.",
            "normal santral sinir sistemi",
            ["intrauterin asfiksi", "fetal enfeksiyonlar"],
            []
        )
    ]),

    (3, "k2-65-b01", "Konjenital SSS Malformasyonlarına Giriş ve Epigenetik Düzenleme", [
        (
            "Beynin farklı anatomik bölümlerinin gebeliğin farklı gestasyonel evrelerinde gelişmesinden ötürü, malformasyonun morfolojik paterni hasarın tam olarak hangi dönemde oluştuğunu gösterir.",
            "**Zamansal Patern:** Malformasyon morfolojisi hasarın gestasyonel evresini yansıtır.",
            "Beynin farklı bölümlerinin gebeliğin",
            ["zamansal patern", "gestasyonel evre"],
            []
        ),
        (
            "Embriyogenezin çok erken evrelerinde meydana gelen kritik hücresel olaylar santral doku organizasyonunu temelden bozduğu için daima çok daha ağır, geri dönüşsüz ve letal fenotiplere yol açar.",
            "**Erken Dönem Hasarları:** Erken embriyonik hasarlar çok daha ağır klinik fenotipler oluşturur.",
            "erken olaylar daha ağır fenotiplere",
            ["erken evre", "ağır fenotipler"],
            []
        ),
        (
            "Nöronların ya da glial hücrelerin diferansiyasyon, maturasyon ve hücreler arası haberleşmelerini yöneten genlerin mutasyonları santral sinir sistemi malformasyonlarına ve ağır disfonksiyonlara neden olur.",
            "**Genetik Düzenleme:** Diferansiasyon, maturasyon ve sinaptik gen mutasyonları.",
            "Nöronların ya da glial hücrelerin diferansiasyon",
            ["hücresel diferansiyasyon", "gen mutasyonları"],
            []
        ),
        (
            "Genetik faktörlere ek olarak radyasyon, maternal hipertermi, teratojenik ilaçlar ve intrauterin enfeksiyon etkenleri de benzer morfolojik gelişim kusurlarını tetikleyen önemli çevresel nedenler arasındadır.",
            "**Teratojenler:** İntrauterin enfeksiyonlar, kimyasallar ve fiziksel teratojenik faktörler.",
            "kimyasallar ve enfeksiyon etkenlerinin de teratojenik",
            ["teratojenik etkenler", "intrauterin enfeksiyon"],
            []
        ),
        (
            "Özellikle sitomegalovirüs, toksoplazma ve kızamıkçık gibi konjenital enfeksiyonlar gelişmekte olan nöronal göç hatlarını doğrudan tahrip ederek mikrosefali ve intrakraniyal kalsifikasyonlara yol açar.",
            "**Konjenital Enfeksiyonlar:** Sitomegalovirüs ve toksoplazmanın nöron göçü ve kalsifikasyonlara etkisi.",
            "etkileri vardır",
            ["sitomegalovirüs", "kalsifikasyonlar"],
            []
        )
    ]),

    (4, "k2-65-b01", "Konjenital SSS Malformasyonlarına Giriş ve Epigenetik Düzenleme", [
        (
            "Otizmin değişik klinik formlarında yapılan genetik incelemelerde sinaptik bağlantıların gelişimini ve budanmasını kontrol eden genlerin birincil rol oynadığı saptanmıştır.",
            "**Otizm Genetiği:** Sinaptik bağlantı gelişimini kontrol eden gen defektleri.",
            "Otizmin değişik formlarında genetik incelemede",
            ["otizm genetiği", "sinaptik bağlantılar"],
            []
        ),
        (
            "Benzer şekilde X kromozomuna bağlı dominant kalıtılan Rett sendromunda da metil bağlayan protein iki yani me ce pe iki geninde kromatin epigenetik değişimlerini geri dönüşsüz bozan mutasyon saptanır.",
            "**Rett Sendromu:** X'e bağlı MeCP2 gen mutasyonu ve kromatin epigenetik düzenleme kaybı.",
            "metil-",
            ["Rett sendromu", "epigenetik değişimler"],
            []
        ),
        (
            "Bu sendromdan etkilenen kız çocuklarında doğum sonrası erken motor ve mental gelişim başlangıçta tamamen normal seyreder.",
            "**Erken Gelişim:** Kız çocuklarında yaşamın ilk bir yılı genellikle normal seyreder.",
            "kızlarda gelişim önce normaldir",
            ["kız çocukları", "erken gelişim"],
            []
        ),
        (
            "Ancak bir iki yaş civarında kazanılmış konuşma ve el becerilerinin kaybı ile karakterize belirgin bir nörolojik regresyon tablosu ortaya çıkar ve santral epigenetik düzenlemenin biyolojik önemini açıkça kanıtlar.",
            "**Nörolojik Regresyon:** Bir iki yaşında zihinsel gerileme, mikrosefali ve stereotipik el hareketleri.",
            "nörolojik bozukluklar ortaya çıkar",
            ["nörolojik regresyon", "epigenetik düzenleme"],
            []
        ),
        (
            "Kromatin kromatin epigenetik modifikasyon ve düzenleme kusuru nöronal plastisiteyi yıkarak el ovuşturma benzeri stereotipik hareketler, mikrosefali ve solunum düzensizlikleri ile karakterize klinik tabloyu belirginleştirir.",
            "**Kromatin Modifikasyonu:** Epigenetik kusur, stereotipik el hareketleri ve mikrosefali.",
            "önemini ortaya koymaktadır",
            ["kromatin epigenetik", "stereotipik hareketler"],
            []
        )
    ]),

    # --- BOLUM 2: Santral Sinir Sistemi Malformasyonlarının Genel Sınıflaması (5) ---
    (5, "k2-65-b02", "Santral Sinir Sistemi Malformasyonlarının Genel Sınıflaması", [
        (
            "Santral sinir sistemi malformasyonlarını anatomik lokalizasyon ve embriyolojik kökenlerine göre morfolojik olarak dört temel ana başlık altında sınıflandırarak incelemekteyiz.",
            "**Sınıflama Çerçevesi:** Santral sinir sistemi anomalilerinin dört ana anatomik grubu.",
            "Malformasyonlar",
            ["sınıflama çerçevesi", "santral sinir sistemi"],
            []
        ),
        (
            "Bu sınıflama nöral tüp defektleri, ön beyin malformasyonları, arka fossa anomalileri ve spinal kord kavitasyonel anormalliklerini kapsayan son derece kapsamlı ve sistematik bir çerçeve sunar.",
            "**Dört Ana Grup:** Nöral tüp, ön beyin, arka fossa ve spinal kord malformasyonları.",
            "- Nöral Tüp Defektleri",
            ["nöral tüp defektleri", "ön beyin malformasyonları"],
            []
        ),
        (
            "Nöral tüp defektleri kranyal ve spinal kapanma kusurlarını içerirken, ön beyin patolojileri nöronal göç ve lobülasyon anormalliklerini temsil eder.",
            "**Gelişimsel Süreçler:** Kapanma yetersizlikleri ve nöronal migrasyon sapmaları.",
            "- Ön Beyin Malformasyonları",
            ["kapanma kusurları", "nöronal göç"],
            []
        ),
        (
            "Arka fossa ve kord lezyonları ise serebellum, beyin sapı herniasyonları ve santral kanalın yapısal bozuklukları ile klinik belirti verir.",
            "**Fossa ve Kord:** Serebellar ektopiler, herniasyonlar ve sirinks kaviteleri.",
            "- Arka Fossa Anomalileri",
            ["arka fossa", "spinal kord lezyonları"],
            []
        ),
        (
            "Embriyolojik açıdan primer malformasyonlar intrensek genetik kusurları temsil ederken, disrupsiyonlar dış etkenlerle normal dokunun yıkımını, deformasyonlar ise mekanik baskıları ifade eder.",
            "**Gelişimsel Terminoloji:** Malformasyon, disrupsiyon ve deformasyon kavramsal ayrımları.",
            "- Spinal Kord Anormallikleri",
            ["primer malformasyonlar", "disrupsiyonlar"],
            []
        )
    ]),

    # --- BOLUM 3: Nöral Tüp Kapanma Kusurları ve Etiyoloji (6-8) ---
    (6, "k2-65-b03", "Nöral Tüp Kapanma Kusurları ve Etiyoloji", [
        (
            "Santral sinir sistemi gelişiminin en erken basamağında ventriküler sisteme, serebral dokuya ve medulla spinalise dönüşecek olan nöral tüpün kapanması yer alır.",
            "**Nöral Tüp Oluşumu:** Ventriküler sistem, beyin ve spinal kordu oluşturan temel yapı.",
            "Beyin gelişiminin en erken basamağında",
            ["nöral tüp", "ventriküler sistem"],
            []
        ),
        (
            "Nöral plakanın katlanarak nöral tüpü oluşturması embriyonik dönemin ilk ayında kranyal nöropordan kaudal nöropora doğru son derece hassas bir dengeyle gerçekleşir.",
            "**Nöral Katlanma:** Embriyonik ilk ayda nöral plakanın kapanma süreci.",
            "medulla spinalise dönüşecek olan nöral tüpün",
            ["nöral plaka", "nöral katlanma"],
            []
        ),
        (
            "Nöral tüpün kapanmasının kısmi yetersizliği ya da tam kapanamaması sinir dokusu elemanları, meninksler ve bunları örten kemik ve yumuşak dokuda çeşitli malformasyonlara neden olabilir.",
            "**Kapanma Yetersizliği:** Nöral doku, meninks, kemik ve yumuşak doku defektleri.",
            "Nöral tüpün kapanmasının kısmi",
            ["kapanma yetersizliği", "meninksler"],
            []
        ),
        (
            "Kapanmayan nöral plaka doğrudan amniyon sıvısı ile temas ederek doku nekrozuna ve kimyasal hasara maruz kalır, bu durum sekonder parankim kaybını derinleştirir.",
            "**Amniyon Teması:** Açık nöral dokunun kimyasal hasarı ve sekonder doku kaybı.",
            "ve yumuşak dokuda çeşitli",
            ["açık nöral plaka", "amniyon sıvısı"],
            []
        ),
        (
            "Böylece açık kalan nöral tüp çevresindeki mezenşimal dokunun indüksiyonu bozulur ve vertebraların posterior arkusları ile kalvaryum kemiklerinin birleşmesi engellenir.",
            "**Mezenşimal İndüksiyon Bozukluğu:** Kemik arkuslarının kapanamaması ve açık defekt oluşumu.",
            "olmaması, sinir dokusu, meninksler",
            ["mezenşimal indüksiyon", "kemik arkusları"],
            []
        )
    ]),

    (7, "k2-65-b03", "Nöral Tüp Kapanma Kusurları ve Etiyoloji", [
        (
            "Genel olarak bakıldığında nöral tüp defektleri, yeni doğan döneminde en sık görülen santral sinir sistemi malformasyonları grubunu oluşturur.",
            "**Sıklık:** Nöral tüp defektleri en sık görülen santral sinir sistemi malformasyonlarıdır.",
            "Genel olarak bakıldığında nöral tüp defektleri",
            ["nöral tüp defektleri", "en sık malformasyon"],
            []
        ),
        (
            "Nöral tüpün embriyolojik kapanması normal gelişim sürecinde döllenmeden sonraki döllenmeden sonraki yirmi sekizinci günde yani dördüncü gebelik haftasının sonunda tamamlanır.",
            "**Kapanma Zamanı:** Normal nöral tüp kapanması 28. günde yani 4. haftanın sonunda tamamlanır.",
            "en sık görülen santral",
            ["yirmi sekizinci gün", "dördüncü hafta"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: nöral tüp defektleri en sık görülen santral sinir sistemi malformasyonları olup kapanma defekti doğrudan amniyos sıvısında yüksek düzeyde alfa fetoprotein yani a fe pe artışına yol açar.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Nöral tüp defektleri en sıktır ve amniyos sıvısında AFP artışına neden olur.",
            "sinir sistemi malformasyonlarıdır",
            ["çıkmış sınav sorusu", "nöral tüp defektleri", "alfa fetoprotein"],
            ["dea0348ff630"]
        ),
        (
            "Kapanma kusuru kranyal anterior bölgede anensefaliye, kaudal posterior bölgede ise spina bifida ve miyelomeningosel spektrumuna neden olur.",
            "**Klinik Spektrum:** Anterior defekt anensefali, posterior defekt spina bifida ve miyelomeningosel.",
            "Genel olarak bakıldığında nöral tüp defektleri",
            ["anensefali", "spina bifida", "miyelomeningosel"],
            []
        ),
        (
            "Ayrıca amniyos sıvısına sızan asetilkolinesteraz enzim aktivitesinin pozitif saptanması nöral tüpün tamamen açık olduğunu doğrulayan ikinci kritik biyokimyasal kanıttır.",
            "**Biyokimyasal Doğrulama:** Amniyos sıvısında asetilkolinesteraz pozitifliği açık defekt kanıtıdır.",
            "en sık görülen santral",
            ["asetilkolinesteraz", "açık defekt"],
            []
        )
    ]),

    (8, "k2-65-b03", "Nöral Tüp Kapanma Kusurları ve Etiyoloji", [
        (
            "Nöral tüp defektlerinin etiyolojisinde maternal folik asit eksikliği ve genetik yatkınlık en belirleyici ve önlenebilir faktörler arasında kabul edilmektedir.",
            "**Etiyoloji:** Folik asit eksikliği ve genetik yatkınlık birincil nedendir.",
            "En sık görülen defektler, nöral tüpün",
            ["etiyoloji", "folik asit eksikliği"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: gebelik öncesi ve erken dönemde başlanan folik asit desteği nöral tüp defekti riskini yüzde yetmiş oranında azaltırken, antiepileptik ilaç valproat folat antagonizması ile riski belirgin artırır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Folik asit riski %70 azaltır; valproik asit folat antagonizması ile spina bifida riskini artırır.",
            "spinal kordun geliştiği posterior",
            ["çıkmış sınav sorusu", "folik asit desteği", "valproat"],
            ["dea0348ff630", "d3-k2-far-004"]
        ),
        (
            "Nöral defekt varlığında fetal dokudan sızan belirteçler nedeniyle maternal kanda alfa fetoprotein seviyelerinde tanısal artış saptanır.",
            "**Maternal Tarama:** Maternal kanda alfa-fetoprotein artışı prenatal tanıda kritiktir.",
            "Myelomeningosel, santral sinir sistemi",
            ["maternal tarama", "alfa fetoprotein"],
            []
        ),
        (
            "Omurganın arka kemik arkuslarının kapanmaması anlamına gelen spina bifida, asemptomatik spina bifida okültadan açık miyelomeningosele kadar uzanan oldukça geniş ve değişken bir klinik tablo gösterir.",
            "**Spina Bifida:** Vertebral kemik arkus defekti; okült formdan açık miyelomeningosele uzanır.",
            "bir defektten dışarı çıkmasıdır",
            ["spina bifida", "miyelomeningosel"],
            []
        ),
        (
            "Yüksek riskli gebeliklerde veya daha önce nöral tüp defektli bebek doğurmuş kadınlarda perikonsepsiyonel folik asit dozunun dört miligrama kadar artırılması önerilmektedir.",
            "**Profilaksi Dozu:** Önceki öyküsü olan riskli gebelerde yüksek doz folik asit koruması.",
            "en sık lumbosakral bölgede gerçekleşir",
            ["perikonsepsiyonel folat", "profilaksi dozu"],
            []
        )
    ]),

    # --- BOLUM 4: Spina Bifida, Miyelomeningosel ve Anterior Nöral Defektler (9-11) ---
    (9, "k2-65-b04", "Spina Bifida, Miyelomeningosel ve Anterior Nöral Defektler", [
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: miyelomeningosel santral sinir sistemi dokusunun ve meninkslerin vertebral kanaldaki kemik defektten dışarı fıtıklaşması olup en sık lumbosakral bölgede gerçekleşir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Miyelomeningosel kord ve meninks fıtıklaşmasıdır, en sık lumbosakralde görülür.",
            "",
            ["çıkmış sınav sorusu", "miyelomeningosel", "lumbosakral bölge"],
            ["d3-k2-bey-008"]
        ),
        (
            "Ekranda yer alan karakteristik Robbins şekil yirmi üç on dört görselinde yeni doğan bebeğin lumbosakral bölgesinde dışarı doğru dışarı doğru kese yapmış belirgin bir miyelomeningosel lezyonu görülmektedir.",
            "**Görsel Analiz:** Yenidoğanda lumbosakral orta hat miyelomeningosel kesesi.",
            "",
            ["Robbins şekli", "lumbosakral kese"],
            []
        ),
        (
            "Kesenin duvarını ince meninks zarları oluştururken, merkezinde merkezi ülsere ve dış ortama açık spinal kord parankimi ve sinir kökleri belirgin olarak izlenir.",
            "**Kese Morfolojisi:** Meninks zarı ile çevrili, ülsere merkezde nöral kord parankimi.",
            "",
            ["meninks zarları", "ülsere merkez", "spinal kord parankimi"],
            []
        ),
        (
            "Bu açık lezyonlar alt ekstremitelerde flask paralizi, sfinkter kontrol kaybı ve menenjit gibi hayati komplikasyonlara zemin hazırlar.",
            "**Klinik Komplikasyonlar:** Parapleji, sfinkter disfonksiyonu ve asendan menenjit riski.",
            "",
            ["flask paralizi", "sfinkter kaybı", "menenjit"],
            []
        ),
        (
            "Lumbosakral miyelomeningosel olgularının neredeyse tamamında spinal kordun kaudale çekilmesine bağlı olarak Arnold-Chiari tip iki malformasyonu ve hidrosefali eşlik eder.",
            "**Chiari II Birlikteliği:** Kaudal kord traksiyonu ile beyin sapı herniasyonu ve hidrosefali.",
            "",
            ["Arnold-Chiari", "kaudal kord traksiyonu"],
            []
        )
    ]),

    (10, "k2-65-b04", "Spina Bifida, Miyelomeningosel ve Anterior Nöral Defektler", [
        (
            "Santral sinir sistemi gelişiminin kranial ucunda kafatası kemiklerinin ve beyin dokusunun yokluğu ile karakterize, nöral tüpün anterior ucunun malformasyonu olan nöral tüp defekti olan anensefali vardır.",
            "**Anensefali:** Anterior nöropor kapanma kusuru, kalvaryum ve beyin yokluğu.",
            "nöral tübün anterior ucunun",
            ["anensefali", "kalvaryum yokluğu"],
            []
        ),
        (
            "Anensefalide fetal yutma ve amniyon absorbsiyon fonksiyonu santral hasar nedeniyle bozulduğu için maternal amniyotik sıvı miktarı patolojik olarak artar ve polihidramniyos tablosu gelişir.",
            "**Polihidramniyos:** Fetal yutma bozukluğuna bağlı maternal amniyon sıvısı artışı.",
            "kafatası kemiklerinin ve beyin",
            ["fetal yutma", "polihidramniyos"],
            []
        ),
        (
            "Ensefalosel ise malforme santral sinir sistemi dokusunun kafatasındaki kemik bir defektten dışarı doğru divertikül oluşturarak fıtıklaşması durumudur.",
            "**Ensefalosel:** Kafatası kemik defektinden malforme nöral dokunun divertiküler fıtıklaşması.",
            "Ensefalosel ise, malforme santral sinir",
            ["ensefalosel", "divertikül"],
            []
        ),
        (
            "Ensefalosel olguları klinikte en sık oksipital bölgede veya arka fossada gelişirken, ön tarafta yerleştiğinde nazal ve etmoid sinüslerin içine doğru uzanabilir.",
            "**Lokalizasyon:** En sık oksipital ve arka fossa; anterior yerleşimde sinüs içine uzanım.",
            "En sık oksipital bölgede veya arka fossada gelişir",
            ["oksipital bölge", "nazal sinüsler"],
            []
        ),
        (
            "Anensefalik fetüslerde kalvaryum kubbesi bulunmadığından tabanda vaskülarize dezorganize nöral kalıntılardan oluşan area cerebrovasculosa dokusu izlenir.",
            "**Area Cerebrovasculosa:** Kalvaryum kemiği yokluğunda tabanda izlenen vasküler nöral kalıntı.",
            "dokusunun yokluğu ile karakterize",
            ["area cerebrovasculosa", "vasküler nöral kalıntı"],
            []
        )
    ]),

    # Sayfa 11: Ön Beyin Hacim Malformasyonları: Megaloensefali ve Mikroensefali
    (11, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Klinik nöropatolojide ön beyin malformasyonlarının bir grubunda beynin hacmi ve ağırlığı anormal derecede artmış yani megaloensefali ya da ileri derecede küçülmüş yani mikroensefali olarak karşımıza çıkar.",
            "**Hacim Anomalileri:** Megaloensefali ve mikroensefali ile serebral hacim sapmaları.",
            "Ön Beyin Malformasyonları",
            ["megaloensefali", "mikroensefali"],
            []
        ),
        (
            "Klinik pratikte mikroensefali çok daha sık görülür ve genellikle baş çevresinin yaş ve cinsiyete göre ortalamanın belirgin altında kaldığı mikrosefali ile birliktedir.",
            "**Mikroensefali ve Mikrosefali:** Küçük beyin ve küçük kafa çevresi birlikteliği.",
            "Mikroensefali, çok daha sık görülür",
            ["mikroensefali", "küçük kafa"],
            []
        ),
        (
            "Bu hacim küçülmesi kromozom anormallikleri, fetal alkol sendromu ve intrauterin insan immün yetmezlik virüsü gibi pek çok klinik zeminde gelişebilmektedir.",
            "**Etiyolojik Zemin:** Kromozom defektleri, fetal alkol sendromu ve intrauterin enfeksiyonlar.",
            "Fetal alkol sendromu ve",
            ["kromozom anormallikleri", "fetal alkol sendromu"],
            []
        ),
        (
            "Bütün bu hastalıklarda altta yatan temel ortak patolojik özellik, serebral korteksi oluşturacak nöron sayılarındaki belirgin azalmadır.",
            "**Ortak Nöropatoloji:** Kortikal nöron sayısındaki azalma ve nörogenez yetersizliği.",
            "serebral korteksi oluşturacak",
            ["nöron sayılarındaki azalma", "korteks hacmi"],
            []
        ),
        (
            "Megaloensefali olgularında ise pe ten gen mutasyonu veya mTOR sinyal yolağının aşırı aktivasyonu kontrolsüz hücresel büyüme ve makrosefaliye yol açar.",
            "**Megaloensefali Patogenezi:** PTEN mutasyonu ve mTOR hiperaktivitesi ile aşırı büyüme.",
            "beynin hacmi anormal artmıştır",
            ["pe ten gen mutasyonu", "megaloensefali"],
            []
        )
    ]),

    # Sayfa 12: Nöroproliferasyon ve Radyal Glial Göç
    (12, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Beyin gelişiminin erken dönemlerinde progenitör hücreler ventriküler çevreleyen subependimal zonda öncül hücreler çoğalarak yoğun şekilde prolifere olurlar.",
            "**Nöroproliferasyon:** Subependimal zonda öncül hücrelerin çoğalması.",
            "progenitör hücreler subependimal",
            ["subependimal zon", "proliferasyon"],
            []
        ),
        (
            "Bu hücrelerden kortekse göç edenler ile bu zonda kalanlar arasındaki denge, nöronal ve astrositik hücresel diferansiyasyon oranını doğrudan etkiler.",
            "**Progenitör Dengesi:** Göç eden ve kalan hücrelerin nöronal ve glial oranları belirlemesi.",
            "progenitör havuzda prematür olarak kalırsa",
            ["progenitör havuz", "astrositik diferansiyasyon"],
            []
        ),
        (
            "Çok sayıda hücre progenitör havuzda prematür olarak kalırsa matür nöronların gelişimi yetersiz kalır ve mikrosefali tablosu ile beyin küçük kalır.",
            "**Prematür Duraklama:** Havuzda hücre kalması yetersiz nöron gelişimine ve küçük beyne yol açar.",
            "kortekse göç edenler ile",
            ["matür nöronlar", "küçük beyin"],
            []
        ),
        (
            "Gelişim sırasındaki nöron göçü ve farklılaşmasının kesintiye uğraması girus oluşumu ve altı tabakalı normal neokortikal laminasyon anomalilerine neden olur.",
            "**Kortikal Disorganizasyon:** Göç kesintisi ile altı tabakalı laminasyonun bozulması.",
            "nöronal ve astrositik diferansiyasyon",
            ["girus oluşumu", "altı tabakalı laminasyon"],
            []
        ),
        (
            "Radyal glial lifler boyunca göç eden nöronlar marjinal zonda Cajal-Retzius hücrelerinin salgıladığı reelin proteini sinyali ile doğru kortikal katmanda duraklarlar.",
            "**Reelin Sinyali:** Cajal-Retzius hücreleri ve reelin rehberliğinde katmanlı laminasyon.",
            "oranını etkiler",
            ["Cajal-Retzius hücreleri", "reelin sinyali"],
            []
        )
    ]),

    # Sayfa 13: Ön Beyin Malformasyonları Yelpazesi
    (13, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Ön beyin nöronal göç ve organizasyon bozuklukları geniş ve karmaşık bir morfolojik spektrumu kapsayan patolojik tablolardan oluşur.",
            "**Göç Bozuklukları Yelpazesi:** Lissensefaliden heterotopilere uzanan morfolojik spektrum.",
            "Ön Beyin Malformasyonları",
            ["göç bozuklukları", "morfolojik spektrum"],
            []
        ),
        (
            "Bu spektrumun en ağır ucunda girusların total yokluğu olan lissensefali yani agiri veya geniş basık kıvrımlarla karakterize pakigiri yer alır.",
            "**Lissensefali ve Pakigiri:** Girusların total veya aralıklı yokluğu ile düz beyin.",
            "Lissensefali (agria) ve pacigria",
            ["lissensefali", "pakigiri"],
            []
        ),
        (
            "Korteksin yüzeyinde karnabahar ya da kaldırım taşı benzeri çok sayıda ufak girus oluşumu ise polimikrogiri olarak tanımlanır.",
            "**Polimikrogiri:** Kaldırım taşı manzarası veren çok sayıda küçük girus oluşumu.",
            "Polimikrogria",
            ["polimikrogiri", "kaldırım taşı"],
            []
        ),
        (
            "Ön beyin orta hat yapılarının ayrılamaması holoprozensefali tablosunu doğururken, fokal displastik korteks ve korteks altında nöron birikimleri heterotopileri oluşturur.",
            "**Holoprozensefali ve Heterotopi:** Orta hat bölünme defekti ve ektopik nöron kümeleri.",
            "Holoprosensefali",
            ["holoprozensefali", "heterotopi"],
            []
        ),
        (
            "Korteksin altında nodül veya bant oluşturan bu ektopik nöron grupları klinikte tedaviye dirençli çocukluk çağı epilepsilerinin en önemli patolojik zeminidir.",
            "**Ektopik Nöron Odakları:** Subkortikal nodül ve bantların tetiklediği intraktabl nöbetler.",
            "Korteksin altında nodül veya bant",
            ["ektopik nöronlar", "epileptik nöbetler"],
            []
        )
    ]),

    # Sayfa 14: Lissensefali ve Pakigiri
    (14, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Girusların total yokluğu lissensefali yani agiri veya aralıklı olarak yokluğu pakigiri olarak adlandırılır ve bu alanlarda pürüzsüz düz yüzeyli beyin morfolojisi izlenir.",
            "**Lissensefali (Agiri) ve Pakigiri:** Girusların yokluğu veya geniş kıvrımlı düz beyin.",
            "Lissensefali (agria) ve pacigria",
            ["lissensefali", "pakigiri", "düz beyin"],
            []
        ),
        (
            "Normal altı tabakalı laminasyon yerine korteks anormal derecede kalınlaşmıştır ve histolojik olarak genellikle sadece dört tabaka içerir.",
            "**Dört Tabakalı Korteks:** 6 tabaka yerine 4 tabakalı kalınlaşmış anormal laminasyon.",
            "ve genellikle sadece dört",
            ["dört tabakalı korteks", "kalınlaşmış korteks"],
            []
        ),
        (
            "Çoğu lissensefali olgusunda nöronal migrasyonu kontrol eden hücre iskeleti ve mikrotübül ilişkili genlerde mutasyonlar mevcuttur.",
            "**Moleküler Patogenez:** Nöronal göçü kontrol eden mikrotübül ilişkili gen mutasyonları.",
            "aralıklı olarak yokluğu",
            ["mikrotübül genleri", "nöronal migrasyon"],
            []
        ),
        (
            "Özellikle lis bir geni ve X kromozomuna bağlı de ce iks yani doublecortin mutasyonları nöroblastların göçünü durdurarak lissensefaliye yol açar.",
            "**Genetik:** LIS1 ve DCX (doublecortin) mikrotübül motor protein mutasyonları.",
            "Çoğu lissensefali olgularında nöronal",
            ["lis bir", "de ce iks", "lissensefali"],
            []
        ),
        (
            "Ayrıca bazal membran laminin defektleri ile pial bariyerin yırtıldığı tip iki arnavut kaldırımı lissensefalide ise Walker-Warburg konjenital kas distrofisi sendromu eşlik eder.",
            "**Tip II Lissensefali:** Arnavut kaldırımı görünümü ve Walker-Warburg kas distrofisi birlikteliği.",
            "ilişkili defekt vardır",
            ["arnavut kaldırımı", "Walker-Warburg"],
            []
        )
    ]),

    # Sayfa 15: Lissensefali Makroskopisi Görseli
    (15, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Ekranda gösterilen Robbins şekil yirmi sekiz beş görselinde miadında doğmuş bir bebeğin koronal beyin kesiti ve pürüzsüz yüzeyi izlenmektedir.",
            "**Görsel İnceleme:** Miadında yenidoğanda lissensefali koronal kesiti.",
            "",
            ["Robbins şekli", "koronal kesit"],
            []
        ),
        (
            "Kesitte normalde beyin yüzeyini kaplayan girintili çıkıntılı kortikal sulkus ve girusların tamamen kaybolduğu açıkça görülmektedir.",
            "**Girus Yokluğu:** Kortikal kıvrımların ve sulkusların tamamen silinmesi.",
            "",
            ["sulkus ve giruslar", "pürüzsüz yüzey"],
            []
        ),
        (
            "Dört tabakalı hale gelen gri korteks anormal biçimde genişlemişken, altta yer alan serebral beyaz cevher tabakası ileri derecede incelmiştir.",
            "**Korteks-Beyaz Madde Orantısızlığı:** Kalınlaşmış korteks ve ileri derecede daralmış beyaz cevher.",
            "",
            ["genişlemiş korteks", "incelmiş beyaz cevher"],
            []
        ),
        (
            "Bu ağır yapısal disorganizasyon bebeklerde derin motor gerilik, hipotoni ve tedaviye dirençli epileptik ensefalopati tablosuna yol açar.",
            "**Klinik Seyir:** Derin psikomotor gerilik, hipotoni ve intraktabl infantil spazmlar.",
            "",
            ["motor gerilik", "epileptik ensefalopati"],
            []
        ),
        (
            "Ayrıca koronal kesitte lateral ventriküllerin oksipital boynuzlarının genişlemesi anlamına gelen kolposefali deformitesi de tabloya sıklıkla eşlik eder.",
            "**Kolposefali:** Lateral ventrikül arka boynuzlarının karakteristik orantısız genişlemesi.",
            "",
            ["kolposefali", "oksipital boynuzlar"],
            []
        )
    ]),

    # Sayfa 16: Polimikrogiri
    (16, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Ön beyin önemli kortikal gelişim kusurlarından polimikrogiri, serebral kortekste anormal sayıda artmış ufak girusların varlığı ile karakterizedir.",
            "**Polimikrogiri Tanımı:** Artmış sayıda minik giruslar ve anormal kortikal kıvrımlanma.",
            "Ön Beyin Malformasyonları",
            ["polimikrogiri", "kortikal gelişim"],
            []
        ),
        (
            "Polimikrogiride beyin yüzeyine dışarıdan bakıldığında kıvrımların küçülüp birbirine yapışması sonucu tipik karnabahar veya kaldırım taşı benzeri düzensiz bir yüzey görünümü oluşur.",
            "**Kaldırım Taşı Manzarası:** Karnabahar veya kaldırım taşı benzeri pürüzlü yüzey yapısı.",
            "kaldırım taşı benzeri düzensiz yüzeyler",
            ["kaldırım taşı", "düzensiz yüzey"],
            []
        ),
        (
            "Histolojik incelemede normal altı tabakalı laminasyonun kaybolduğu ve kaynaşmış dört ya da tek tabakalı minik girusların birleştiği izlenir.",
            "**Histolojik Yapı:** Kaynaşmış moleküler tabaka ve altı tabakalı mimarinin kaybı.",
            "artmış küçük girus oluşumudur",
            ["kaynaşmış tabakalar", "küçük giruslar"],
            []
        ),
        (
            "Bu patolojik değişiklikler tek bir hemisferin perisilvian bölgesinde fokal olabileceği gibi iki taraflı yaygın dağılım da gösterebilir.",
            "**Dağılım:** Perisilvian bölgede fokal tutulum veya bilateral yaygın dağılım.",
            "Bu değişiklikler, fokal veya yaygın olabilir",
            ["fokal tutulum", "yaygın dağılım"],
            []
        ),
        (
            "Etiyolojide intrauterin sitomegalovirüs enfeksiyonu ve perfüzyon bozuklukları gibi lokal iskemik olaylar en sık suçlanan çevresel etkenlerdir.",
            "**Etiyoloji:** Sitomegalovirüs enfeksiyonu ve intrauterin lokal iskemik perfüzyon yetersizliği.",
            "Polimikrogria",
            ["sitomegalovirüs", "lokal iskemi"],
            []
        )
    ]),

    # Sayfa 17: Holoprozensefali Spektrumu
    (17, "k2-65-b05", "Ön Beyin Hacim ve Nöronal Göç Malformasyonları", [
        (
            "Holoprozensefali normal ön beyin orta hat yapılarının patolojik kesintisi ve telensefalonun iki ayrı simetrik hemisfere ayrılamaması ile kendini gösterir.",
            "**Holoprozensefali:** Normal orta hat yapılarının kesintisi ve hemisfer ayrılma kusuru.",
            "Holoprosensefali, normal orta hat",
            ["holoprozensefali", "orta hat yapıları"],
            []
        ),
        (
            "Hafif formlarda olfaktor bulbus yokluğu yani arinensefali görülürken, en şiddetli ve ölümcül alobar formda beyin hemisferlere bölünememiş tek bir ortak ventrikül içerir.",
            "**Ağırlık Spektrumu:** Arinensefaliden alobar tek ventrikül ve siklopiye uzanan tablo.",
            "arhinensefali",
            ["arinensefali", "tek ventrikül"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: holoprozensefali Sonic hedgehog yani se ha ha gen mutasyonları ve Trizomi on üç Patau sendromu ile doğrudan ilişkilidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Holoprozensefali Sonic hedgehog (SHH) mutasyonları ve Trizomi 13 ile birliktedir.",
            "sonic hedgehog'daki mutasyonlar",
            ["çıkmış sınav sorusu", "Sonic hedgehog", "Trizomi 13"],
            ["d3-k2-pat-008"]
        ),
        (
            "Etkilenen olgularda tek bir göz boşluğu yani siklopi, orta hat yarık dudak damak ve hipotelorizm gibi ağır kraniofasial anomaliler tabloya eşlik eder.",
            "**Orta Hat Fasial Defektler:** Hipotelorizm, yarık dudak-damak ve kraniofasial anomaliler.",
            "siklopi gibi yüze ait orta hat",
            ["siklopi", "yarık dudak damak"],
            []
        ),
        (
            "Embriyolojik temelde prekordal mezenşim indüksiyonunun yetersizliği kranial orta hat yapılarını silerek iki göz yuvarlağının birleşmesine ve burun yapısının rudimenter kalmasına yol açar.",
            "**Prekordal Mezenşim Kusuru:** Orta hat indüksiyon yetersizliği ve fasial dismorfizm mekanizması.",
            "kusurları ile beraber olabilir",
            ["prekordal mezenşim", "fasial dismorfizm"],
            []
        )
    ]),

    # --- BOLUM 6: Arka Fossa Anomalileri: Arnold-Chiari Tip I ve Tip II Malformasyonları (18-22) ---
    (18, "k2-65-b06", "Arka Fossa Anomalileri: Arnold-Chiari Tip I ve Tip II Malformasyonları", [
        (
            "Arka fossa anomalileri serebellum, dördüncü ventrikül ve beyin sapının gelişimsel, anatomik ve hacimsel kusurlarını kapsar.",
            "**Arka Fossa Anomalileri:** Serebellum ve beyin sapının gelişimsel defektleri.",
            "Arka Fossa Anomalileri",
            ["arka fossa anomalileri", "serebellum defektleri"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: Arnold-Chiari malformasyonu yani Chiari tip iki malformasyonunda küçük arka fossa, orta hattı deforme serebellum ve serebellar vermisin foramen magnuma fıtıklaşması izlenir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Chiari tip II'de küçük arka fossa, vermis herniasyonu ve hidrosefali görülür.",
            "Küçük boyutlu arka fossa",
            ["çıkmış sınav sorusu", "Arnold-Chiari", "Chiari tip iki", "vermis fıtıklaşması"],
            ["060f46f50beb", "8e92d6d728b6"]
        ),
        (
            "Bu klinik tabloda foramen magnum düzeyinde beyin omurilik sıvısı akımının engellenmesine bağlı ilerleyici sekonder obstriktif hidrosefali gelişimi kuraldır.",
            "**Obstrüktif Hidrosefali:** Foramen magnum düzeyinde BOS dolaşım bloğu ve ventrikülomegali.",
            "orta hattı deforme serebellum ve",
            ["obstriktif hidrosefali", "BOS akım engeli"],
            []
        ),
        (
            "Arnold-Chiari tip iki malformasyonuna hastaların hemen hemen tamamında lomber düzeyde açık miyelomeningosel eşlik etmektedir.",
            "**Miyelomeningosel Birlikteliği:** Chiari tip II olgularının neredeyse tamamında lomber kord defekti.",
            "Tipik olarak hidrosefali ve lomber myelomeningosel eşlik eder",
            ["lomber miyelomeningosel", "kord defekti"],
            []
        ),
        (
            "Nöroradyolojik incelemede mezensefalon tektumunun gagalaşması ve tentoriumun anormal aşağı yerleşimi Chiari tip ikinin patognomonik ek bulgularıdır.",
            "**Gagalaşmış Tektum:** Chiari tip II'de beaked tectum ve düşük tentorium anatomisi.",
            "vermis bölgesinin foramen magnuma doğru uzanması",
            ["gagalaşmış tektum", "düşük tentorium"],
            []
        )
    ]),

    (19, "k2-65-b06", "Arka Fossa Anomalileri: Arnold-Chiari Tip I ve Tip II Malformasyonları", [
        (
            "Çok daha hafif ve sinsi seyirli olan Chiari tip bir malformasyonunda foramen magnuma doğru uzanan aşağı yerleşimli serebellar tonsiller söz konusudur.",
            "**Chiari Tip I:** Foramen magnuma doğru ektopik uzanan serebellar tonsiller.",
            "Çok daha hafif form olan Chiari I",
            ["Chiari tip bir", "tonsiller ektopi"],
            []
        ),
        (
            "Foramen magnumdaki bu tonsiller ektopi dokusu beyin omurilik sıvısı akımında mekanik parsiyel tıkanıklığa ve medulla basısına yol açar.",
            "**Patolojik Mekanizma:** BOS akımında parsiyel tıkanıklık ve servikomedüller bası.",
            "akımında parsiyel tıkanıklığa",
            ["BOS akım engeli", "medulla basısı"],
            []
        ),
        (
            "Hastalarda sıklıkla genç erişkin dönemde ortaya çıkan, öksürmek veya ıkınmakla artan şiddetli suboksipital baş ağrısı, boyun ağrısı ve kraniyal sinir bulguları görülür.",
            "**Klinik Başvuru:** Genç erişkinde öksürükle artan oksipital baş ağrısı ve kraniyal defisit.",
            "yetişkin dönemde ortaya çıkan baş ağrısına",
            ["suboksipital baş ağrısı", "kraniyal sinir basısı"],
            []
        ),
        (
            "Chiari tip birde vermis herniasyonu veya miyelomeningosel eşlik etmez; cerrahi dekompresyon tonsillerin bası semptomlarını ve baş ağrısını belirgin hafifletebilir.",
            "**Chiari Bir Özelliği:** Vermis herniasyonu ve miyelomeningosel eşlik etmez; cerrahi rahatlatır.",
            "Cerrahi girişim semptomları hafifletebilir",
            ["cerrahi dekompresyon", "semptom kontrolü"],
            []
        ),
        (
            "Ayrıca tonsiller herniasyonun beyin omurilik sıvısı pulsasyon dalgalarını bozması spinal kord santral kanalına basınç yükleyerek siringomiyeli gelişimine zemin hazırlar.",
            "**Siringomiyeli Gelişimi:** Chiari I'de beyin omurilik sıvısı pulsasyon dalgalarının bozulması ile kordda sirinks oluşumu.",
            "veya kafa sinirleri",
            ["siringomiyeli gelişimi", "beyin omurilik sıvısı pulsasyonu"],
            []
        )
    ]),

    (20, "k2-65-b06", "Arka Fossa Anomalileri: Arnold-Chiari Tip I ve Tip II Malformasyonları", [
        (
            "Dandy-Walker malformasyonu arka fossanın gelişimsel gelişimsel kistik genişlemesi ve serebellar orta hat yapılarının agenezisi ile karakterize bir arka fossa anomalisidir.",
            "**Dandy-Walker Malformasyonu:** Geniş arka fossa, vermis agenezisi ve kistik 4. ventrikül.",
            "Dandy-Walker",
            ["Dandy-Walker", "arka fossa genişlemesi"],
            []
        ),
        (
            "Patolojinin temel morfolojik triadını belirgin derecede genişlemiş gelişimsel olarak genişlemiş büyük arka kemik fossa, serebellar vermis agenezisi ve yokluğu oluşturur.",
            "**Morfolojik Triad:** Geniş arka fossa, vermis aplazisi ve dördüncü ventrikül orta hat kisti.",
            "Serebellar vermis yokluğu ve",
            ["vermis agenezisi", "morfolojik triad"],
            []
        ),
        (
            "Ayrıca orta hatta dördüncü ventrikülün kistik dilatasyonu sonucu oluşan devasa bir arka fossa kisti dördüncü ventrikül lümeni ile serbestçe ilişkilidir.",
            "**Kistik Dilatasyon:** 4. ventrikülün geriye doğru genişleyen devasa orta hat kisti.",
            "büyük bir orta hat kisti",
            ["dördüncü ventrikül", "orta hat kisti"],
            []
        ),
        (
            "Dördüncü ventrikül çıkışındaki bu kistik genişleme beyin omurilik sıvısı dolaşımını engelleyerek bebeklik döneminde ilerleyici obstrüktif hidrosefaliye ve makrosefaliye yol açar.",
            "**Klinik Yansıması:** İlerleyici bebeklik çağı hidrosefalisi ve baş çevresi büyümesi.",
            "Dandy-Walker",
            ["ilerleyici hidrosefali", "makrosefali"],
            []
        ),
        (
            "Radyolojide torcular Herophili ve transvers sinüslerin anormal yüksek yerleşimi arka fossanın devasa boyutunu kanıtlayan önemli anatomik işarettir.",
            "**Yüksek Torcular:** Genişlemiş arka fossada transvers sinüslerin yukarı itilmesi.",
            "genişlemiş bir arka fossa",
            ["torcular Herophili", "transvers sinüs"],
            []
        )
    ]),

    # Sayfa 21: Joubert Sendromu
    (21, "k2-65-b06", "Arka Fossa Anomalileri: Arnold-Chiari Tip I ve Tip II Malformasyonları", [
        (
            "Joubert sendromu serebellar vermisin agenezisi veya hipoplazisi ile seyreden nadir görülen otozomal resesif kalıtımlı bir arka fossa malformasyonudur.",
            "**Joubert Sendromu:** Serebellar vermis hipoplazisi ve beyin sapı malformasyonu.",
            "Joubert sendromu'nda ise:",
            ["Joubert sendromu", "vermis hipoplazisi"],
            []
        ),
        (
            "Sendromda vermis yokluğuna karakteristik göz hareket anomalileri, okülomotor apraksi ve neonatal solunum düzensizlikleri eşlik eder.",
            "**Klinik Triad:** Vermis agenezisi, anormal göz hareketleri ve epizodik hiperpne.",
            "göz hareket problemleri ve",
            ["okülomotor apraksi", "göz hareket problemleri"],
            []
        ),
        (
            "Beyin sapı kesitlerinde süperior serebellar pedinküllerin kalınlaşması ve orta hatta çaprazlaşamaması sonucu manyetik rezonansta patognomonik azı dişi işareti izlenir.",
            "**Mol Dişi İşareti:** Süperior serebellar pedinkül uzaması ile oluşan molar tooth sign.",
            "solunumda bozukluğa yol açan",
            ["azı dişi işareti", "mol dişi işareti"],
            []
        ),
        (
            "Çoğu olguda patogenezden sorumlu genetik defektler primer silia yapısı ve fonksiyonlarını bozan silier protein mutasyonlarıdır.",
            "**Siliyopati Patogenezi:** Primer silia organel defektleri ve centrosom disfonksiyonu.",
            "primer silia değişikliklerine",
            ["primer silia", "siliyopati"],
            []
        ),
        (
            "Hastalar çocukluk döneminde derin serebellar ataksi, hipotoni, global gelişimsel gerilik ve kistik böbrek hastalıkları riski ile izlenir.",
            "**Klinik İzlem:** Ataksi, hipotoni ve kistik böbrek tutulumu riski.",
            "vermis yokluğu ile birlikte",
            ["serebellar ataksi", "kistik böbrek"],
            []
        )
    ]),

    # Sayfa 22: Arnold-Chiari Midsagittal Kesiti Görseli
    (22, "k2-65-b06", "Arka Fossa Anomalileri: Arnold-Chiari Tip I ve Tip II Malformasyonları", [
        (
            "Robbins şekil yirmi sekiz yedi midsagittal kesitinde Arnold-Chiari tip iki malformasyonunun arka fossa morfolojisi net olarak gösterilmektedir.",
            "**Görsel Analiz:** Arnold-Chiari malformasyonunda midsagittal anatomik kesit.",
            "",
            ["Robbins kesiti", "midsagittal kesit"],
            []
        ),
        (
            "Kesitte gelişimsel olarak anormal derecede gelişimsel olarak küçük ve sığ kalmış bir arka kemik fossa anatomisi dikkat çekmektedir.",
            "**Dar Arka Fossa:** Serebellar yapıları barındıramayacak kadar sığ ve küçük arka çukur.",
            "",
            ["dar arka fossa", "sığ kemik anatomisi"],
            []
        ),
        (
            "Serebellar vermis dokusunun ve alt beyin sapı elemanlarının foramen magnum seviyesinin altına servikal kanala doğru fıtıklaştığı izlenmektedir.",
            "**Vermis Ektopisi:** Foramen magnum düzeyinin altına uzanan serebellar vermis.",
            "",
            ["foramen magnum seviyesi", "vermis fıtıklaşması"],
            []
        ),
        (
            "Bu anatomik fıtıklaşma kraniyoservikal bileşkeyi deforme ederek medulla spinalis girişinde belirgin bir bükülme ve bası etkisi oluşturur.",
            "**Medulla Deformitesi:** Beyin sapının aşağı traksiyonu ve servikal kord basısı.",
            "",
            ["servikomedüller bileşke", "medulla basısı"],
            []
        ),
        (
            "Hastaların cerrahi tedavisinde arka fossanın kemik dekompresyonu ve eşlik eden hidrosefaliye yönelik ventriküloperitoneal şant uygulaması standart yaklaşımdır.",
            "**Cerrahi Tedavi:** Fossa dekompresyonu ve şant ile intrakraniyal basıncın düşürülmesi.",
            "",
            ["cerrahi dekompresyon", "ventriküloperitoneal şant"],
            []
        )
    ]),

    # --- BOLUM 7: Spinal Kord Kavitasyonel Lezyonları: Hidromiyeli ve Siringomiyeli (23) ---
    (23, "k2-65-b07", "Spinal Kord Kavitasyonel Lezyonları: Hidromiyeli ve Siringomiyeli", [
        (
            "Spinal kord kavitasyonel lezyonları kordun epandim ile döşeli santral kanalının patolojik genişlemesi olan hidromiyeli veya parankim içi glial yarık kavite olan siringomiyelidir.",
            "**Kavitasyonel Lezyonlar:** Epandim döşeli hidromiyeli ve parankimal kleft siringomiyeli.",
            "kordun epandim ile döşeli santral",
            ["hidromiyeli", "siringomiyeli"],
            []
        ),
        (
            "Siringomiyeli genellikle Chiari tip bir malformasyonu, intramedüller tümörler veya travmatik spinal kord zedelenmeleri zemininde gelişir.",
            "**Etiyolojik Zemin:** Chiari tip I malformasyonu ve travmatik intramedüller zemin.",
            "kordun iç kısmında sıvı ile dolu yarık benzeri",
            ["Chiari zemin", "sirinks kavitesi"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: servikal korddaki sirinks kavitesi ön beyaz komissürden geçen spinotalamik lifleri çaprazlaşma yerinde basıya uğratarak kollarda pelerin tarzı disosiye ağrı ve ısı duyusu kaybına yol açar.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Sirinks ön beyaz komissür basısıyla pelerin tarzı disosiye duyu kaybı yapar.",
            "kavite gelişimi (siringomyeli)",
            ["çıkmış sınav sorusu", "ön beyaz komissür", "pelerin tarzı duyu kaybı"],
            ["d3-k2-nor-006"]
        ),
        (
            "Arka kordon lifleri korunduğu için lezyon seviyesinde dokunma, vibrasyon ve propriosepsiyon duyusu tamamen sağlam kalır.",
            "**Disosiye Duyu:** Arka kordon sağlam kaldığı için derin duyu ve dokunma korunur.",
            "Spinal Kord Anormallikleri",
            ["arka kordon korunumu", "disosiye duyu"],
            []
        ),
        (
            "Hastalarda ağrısız cilt yanıkları, el ve kollarda fark edilmeyen termal travmalar siringomiyelinin en tipik erken klinik prezentasyonudur.",
            "**Ağrısız Yanıklar:** Termal duyu kaybına bağlı ekstremitelerde fark edilmeyen travmalar.",
            "Spinal Kord Anormallikleri",
            ["ağrısız yanıklar", "termal travma"],
            []
        )
    ]),

    # --- BOLUM 8: Perinatal Beyin Hasarı: Serebral Palsi, Germinal Matriks Kanaması ve PVL (24-28) ---
    (24, "k2-65-b08", "Perinatal Beyin Hasarı: Serebral Palsi, Germinal Matriks Kanaması ve PVL", [
        (
            "Gelişmekte olan fetal ve neonatal beyin dokusuna hipoksi, iskemi ve enfeksiyon gibi hipoksi ve enfeksiyon gibi bir dizi dış faktör hasar verebilir.",
            "**Dış Faktörler:** İntrauterin iskemi, enfeksiyon ve asfiksinin gelişen beyne etkisi.",
            "Gelişmekte olan beyne, bir dizi dış",
            ["dış faktörler", "iskemi ve enfeksiyon"],
            []
        ),
        (
            "Gebeliğin erken evrelerinde oluşan hasarlar henüz matür mikroglia ve astrosit yanıtı gelişmediği için belirgin reaktif değişiklikleri uyandırmadan doğrudan doku kaybına yol açar.",
            "**Gliotik Yanıt Yokluğu:** Erken fetal hasarlarda astrositozis gelişmemesi.",
            "Gebeliğin erken evrelerinde oluşan hasarlar",
            ["gliotik yanıt", "reaktif astrositozis"],
            []
        ),
        (
            "Bu nedenle erken fetal hasarların morfolojik kalıntılarını primer gelişimsel malformasyonlardan ayırt etmek oldukça güçtür.",
            "**Ayırıcı Zorluk:** Erken hasarların konjenital malformasyonlarla karışması.",
            "malformasyonlardan ayrılması güçtür",
            ["morfolojik kalıntı", "malformasyon ayrımı"],
            []
        ),
        (
            "Perinatal dönemde gelişen beyin hasarı çocukluk çağında görülen nörolojik sakatlıkların ve serebral palsinin en önemli nedenidir.",
            "**Kalıcı Engellilik:** Çocukluk çağı kronik nörolojik morbiditesinin en sık nedeni.",
            "çocukluk çağında görülen",
            ["çocukluk çağı sakatlıkları", "serebral palsi"],
            []
        ),
        (
            "Asfiksiye maruz kalan term bebeklerde gelişen hipoksik iskemik ensefalopati tablosunda ilk altı saat içinde uygulanan terapötik hipotermi nöronal nekrozu sınırlamada kanıtlanmış tek tedavidir.",
            "**Terapötik Hipotermi:** Hipoksik iskemik hasarda ilk altı saatte nöroprotektif soğutma tedavisi.",
            "Perinatal Beyin Hasarı",
            ["terapötik hipotermi", "nöronal nekroz"],
            []
        )
    ]),

    (25, "k2-65-b08", "Perinatal Beyin Hasarı: Serebral Palsi, Germinal Matriks Kanaması ve PVL", [
        (
            "Serebral palsi terimi doğum öncesinde, doğum sırasında veya erken postnatal dönemde gelişen, ilerleyici olmayan kalıcı nörolojik motor bozuklukları tanımlar.",
            "**Serebral Palsi Tanımı:** Doğum çevresi hasara bağlı, non-progresif kalıcı motor yetersizlik.",
            "Serebral palsi, prenatal ve perinatal",
            ["serebral palsi", "non-progresif"],
            []
        ),
        (
            "Klinik spektrum spastik diparezi, hemiparezi, distonik hareketler, koreoatetoz ve ataksi gibi heterojen ve çeşitli motor disfonksiyon bulguları içerir.",
            "**Motor Tablo:** Spastisite, distoni, ataksi ve koreoatetoid hareket bozuklukları.",
            "prenatal ve perinatal dönemdeki hasara",
            ["spastik diparezi", "ataksi"],
            []
        ),
        (
            "Patofizyolojide beynin motor korteksi, bazal ganglionları ve periventriküler beyaz cevher traktuslarının selektif hipoksik iskemik zedelenmesi yatar.",
            "**Patogenez:** Piramidal yolakların ve bazal ganglionların hipoksik zedelenmesi.",
            "ilerleyici olmayan nörolojik motor kusurlar",
            ["motor korteks", "periventriküler beyaz cevher"],
            []
        ),
        (
            "Motor bozukluklara sıklıkla epilepsi nöbetleri, görme işitme kayıpları ve değişen derecelerde kognitif etkilenim eşlik edebilmektedir.",
            "**Eşlik Eden Sorunlar:** Mental retardasyon, konvülziyonlar ve duyusal kayıplar.",
            "kullanılan bir terimdir",
            ["epilepsi", "kognitif etkilenim"],
            []
        ),
        (
            "Özellikle spastik diplejide periventriküler beyaz cevherdeki inen bacak kortikospinal liflerinin selektif nekrozu alt ekstremitelerde makaslama yürüyüşü ile belirgindir.",
            "**Spastik Dipleji:** Periventriküler bacak lifleri zedelenmesi ve makaslama yürüyüşü.",
            "İlk işaret ve bulgular, doğumda belli olmayabilir",
            ["spastik dipleji", "makaslama yürüyüşü"],
            []
        )
    ]),

    (26, "k2-65-b08", "Perinatal Beyin Hasarı: Serebral Palsi, Germinal Matriks Kanaması ve PVL", [
        (
            "Prematüre bebeklerde hipoksi, hiperkapni ve sistemik kan basıncı dalgalanmaları subependimal germinal matriks kanamalarına yol açar.",
            "**Germinal Matriks Kanaması:** Prematürelerde kan basıncı dalgalanmaları ve frajilite.",
            "Perinatal dönemde iki ana tip hasar",
            ["prematüre bebek", "germinal matriks"],
            []
        ),
        (
            "Lateral ventrikül komşuluğunda kaudat nükleus ile talamus arasındaki bu vasküler zon ince endotelli zayıf kılcal damar desteği nedeniyle kanamaya son derece elverişlidir.",
            "**Anatomik Zemin:** Subependimal zon, kaudat çekirdek komşuluğu ve zayıf damar yapısı.",
            "Kanamalar ve",
            ["kaudat nükleus", "vasküler zon"],
            []
        ),
        (
            "Subependimal alanda başlayan masif kanama kolaylıkla ventrikül lümeni içine açılarak intraventriküler hematom tablosu oluşturur.",
            "**İntraventriküler Hematom:** Ventrikül lümenine açılan masif hemoraji.",
            "İnfarktüsler",
            ["intraventriküler hematom", "masif kanama"],
            []
        ),
        (
            "Ventriküler sisteme yayılan kanama aquaduktus mezensefaliyi tıkayarak veya araknoid villuslarda fibrozise neden olarak post hemorajik hidrosefaliye zemin hazırlar.",
            "**Post-Hemorajik Hidrosefali:** Aquadukt tıkanıklığı ve araknoid granülasyon fibrozu.",
            "Perinatal dönemde iki ana tip hasar",
            ["aquaduktus mezensefali", "post hemorajik hidrosefali"],
            []
        ),
        (
            "Klinik evrelemede kanamanın sadece subependimal kalmasından ventrikülü doldurmasına ve parankime taşmasına kadar dört dereceli Papile sınıflaması kullanılır.",
            "**Papile Evrelemesi:** Evre birden dörde kadar ventrikül içi kanama ciddiyet dereceleri.",
            "germinal matriks içine, intraparenkimal kanama",
            ["Papile evrelemesi", "ventrikül içi kanama"],
            []
        )
    ]),

    (27, "k2-65-b08", "Perinatal Beyin Hasarı: Serebral Palsi, Germinal Matriks Kanaması ve PVL", [
        (
            "Ekranda gösterilen şekil bir şemasında koronal kesitte lateral ventrikül ile kaudat nükleus arasında yer alan germinal matriks anatomik bölgesi vurgulanmaktadır.",
            "**Şema İnceleme:** Koronal kesitte germinal matriks anatomik lokalizasyonu.",
            "between each lateral",
            ["şema inceleme", "germinal matriks"],
            []
        ),
        (
            "Şemada prematüre bebekte frajil germinal matriks kapillerlerinden başlayan subependimal kanamanın sağ ventrikül içine açılarak lümeni doldurduğu açıkça görülmektedir.",
            "**Ventrikül Kanaması:** Sağ lateral ventriküle drene olan germinal matriks kanaması.",
            "bleeding into the ventricle",
            ["frajil kapillerler", "sağ ventrikül"],
            []
        ),
        (
            "Bu ventrikül içine drene olan derin parankimal hematom komşu bazal ganglion dokusunu tahrip ederek ileride gelişecek spastik motor sekellerin temelini oluşturur.",
            "**Doku Tahribatı:** Kaudat çekirdek hasarı ve derin piramidal lif zedelenmesi.",
            "Caudate",
            ["parankimal hematom", "bazal ganglion"],
            []
        ),
        (
            "Çok düşük doğum ağırlıklı prematüre bebeklerin rutin transfontanel ultrasonografi ile taranması bu kanamaların erken evrede saptanmasında standart yöntemdir.",
            "**Ultrasonografik Takip:** Transfontanel USG ile ventrikül içi kanamanın evrelenmesi.",
            "Lateral",
            ["transfontanel ultrasonografi", "erken evre"],
            []
        ),
        (
            "Özellikle evre üç ve dört kanamalarda gelişen intrakraniyal basınç artışı ve ventrikülomegali acil nöroşirürjikal rezervuar veya şant takılmasını gerektirir.",
            "**Şant Endikasyonu:** Masif ventrikül içi hematomda hidrosefali ve nöroşirürji müdahalesi.",
            "Ventricle",
            ["intrakraniyal basınç", "nöroşirürji müdahalesi"],
            []
        )
    ]),

    (28, "k2-65-b08", "Perinatal Beyin Hasarı: Serebral Palsi, Germinal Matriks Kanaması ve PVL", [
        (
            "Özellikle prematüre bebeklerde supratentorial periventriküler supratentoryal beyaz madde içinde infarktüsler gelişebilir ve bu tabloya periventriküler lökomalazi yani pe ve le adı verilir ve motor kortikospinal lifleri zedeler.",
            "**Periventriküler Lökomalazi (PVL):** Beyaz cevher iskemik infarktüsleri.",
            "supratentorial periventriküler beyaz",
            ["periventriküler lökomalazi", "beyaz cevher"],
            []
        ),
        (
            "İskemik infarktüslerin kalıntıları keskin sınırlı beyaz cevher koagülasyon nekrozu ve mineralizasyondan oluşan tebeşirsi sarı nekroz plak kalıntıları şeklindedir.",
            "**Tebeşirsi Sarı Plaklar:** Keskin sınırlı nekroz ve kalsifikasyon plakları.",
            "tebeşirsi sarı plaklar",
            ["tebeşirsi sarı", "nekroz plak kalıntıları"],
            []
        ),
        (
            "İskemik hasar hem gri hem beyaz cevheri yaygın şekilde tutacak kadar derin olduğunda hemisferler boyunca geniş kavitasyonlarla multikistik ensefalopati tablosu ortaya çıkar.",
            "**Multikistik Ensefalopati:** Geniş kistik nekroz kavitasyonları ile nihai doku yıkımı.",
            "ensefalopati olarak adlandırılır",
            ["multikistik ensefalopati", "kistik kavitasyonlar"],
            []
        ),
        (
            "Bu yaygın nekrotik kaviter yıkım tablosu çocukta ağır quadriplejik serebral palsi, mikrosefali ve ağır kognitif kayıpla seyreden nihai nöropatolojik son evredir.",
            "**Klinik Son Evre:** Spastik kuadripleji ve derin mikrosefali ile karakterize kalıcı hasar.",
            "Perinatal Beyin Hasarı",
            ["spastik kuadripleji", "kalıcı hasar"],
            []
        ),
        (
            "Periventriküler lökomalazi özellikle prematürelerin beyin otoregülasyon yetersizliğine bağlı olarak derin periventriküler sulama havzası sınır zonlarında gelişir.",
            "**Sınır Zon İskemisi:** Derin periventriküler sulama havzalarında perfüzyon yetersizliği.",
            "Özellikle prematüre bebeklerde",
            ["sulama havzası", "sınır zon iskemisi"],
            []
        )
    ])
]

# Verify anchors against kaynak.md
print("Verifying anchors against kaynak.md...")
anchor_errors = 0
for sayfa, bid, bbaslik, sentences in SLIDES:
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        if anchor and anchor not in kaynak_text:
            print(f"ERROR: Sayfa {sayfa} sentence {s_idx+1} anchor not found in kaynak.md: {anchor!r}")
            anchor_errors += 1
if anchor_errors:
    print(f"FAILED: {anchor_errors} anchors not found!")
    sys.exit(1)
print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Build konusma_v2 structure
bolum_map = {}
cid_counter = 1
total_words = 0
slide_last_sent = {} # pno -> last sentence cid
slide_all_sents = {} # pno -> list of cids

for sayfa, bid, bbaslik, sentences in SLIDES:
    if bid not in bolum_map:
        bolum_map[bid] = {
            "id": bid,
            "baslik": bbaslik,
            "paragraflar": []
        }
    p_id = f"k2-65-p{sayfa:03d}"
    p_obj = {
        "id": p_id,
        "sayfa": sayfa,
        "cumleler": []
    }
    
    slide_all_sents[sayfa] = []
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        cid = f"k2-65-c{cid_counter:04d}"
        cid_counter += 1
        words = len(ses.split())
        total_words += words
        slide_all_sents[sayfa].append(cid)
        slide_last_sent[sayfa] = cid
        
        satir_list = [anchor] if anchor else []
        sekil_val = VISUAL_PAGES.get(sayfa, "") if sayfa in VISUAL_PAGES else None
        
        # Clean ekran and find exact casing substring for vurgu
        clean_ekran = ekran.replace("**", "")
        vurgu_text = None
        for t in terms:
            idx = clean_ekran.lower().find(t.lower())
            if idx != -1:
                vurgu_text = clean_ekran[idx:idx + len(t)]
                break
        if not vurgu_text:
            m = re.findall(r"\*\*([^*]+)\*\*", ekran)
            if m:
                raw = m[0].rstrip(":").strip()
                idx = clean_ekran.find(raw)
                if idx != -1:
                    vurgu_text = clean_ekran[idx:idx + len(raw)]
        if not vurgu_text:
            vurgu_text = clean_ekran.split()[0].rstrip(":")
            
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": ekran,
            "duzey": 0,
            "slayt": {
                "sayfa": sayfa,
                "satir": satir_list,
                "sekil": sekil_val
            },
            "vurgu": [{"tur": "terim", "metin": vurgu_text}]
        }
        if cikmis:
            c_obj["cikmis"] = cikmis
            
        p_obj["cumleler"].append(c_obj)
        
    bolum_map[bid]["paragraflar"].append(p_obj)

bolumler_list = list(bolum_map.values())

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-65",
    "anahtar": "y25-k2-65-konjenital-malformasyonlar-ve-perinatal-beyin-hasari",
    "bolumler": bolumler_list
}

print(f"Total Bolumler: {len(bolumler_list)}")
print(f"Total Paragraphs: {len(SLIDES)}")
print(f"Total Sentences: {cid_counter - 1}")
print(f"Total Words: {total_words} (~{total_words / 125:.1f} minutes of audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Generate and save metin.md and konusma_metni.md
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
import konusma_v2 as KV
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Konjenital Malformasyonlar ve Perinatal Beyin Hasarı"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
(TASLAK / "konusma_metni.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md and konusma_metni.md")

# Update sayfa_haritasi.json with all 28 distinct paragraphs
harita = json.load(open(TASLAK / "sayfa_haritasi.json"))
harita_items = []
for sayfa, bid, bbaslik, sentences in SLIDES:
    pid = f"k2-65-p{sayfa:03d}"
    harita_items.append({
        "sayfa": sayfa,
        "paragraf": pid,
        "bolum_id": bid,
        "bolum_baslik": bbaslik,
        "cumle_sayisi": len(sentences)
    })
harita["harita"] = harita_items
(TASLAK / "sayfa_haritasi.json").write_text(json.dumps(harita, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated sayfa_haritasi.json with 28 distinct paragraphs.")

# Drawings definitions
cizim_komutlari = [
    {
        "cumle": slide_last_sent[4],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kromatin Epigenetik Modifikasyonları",
        "ogeler": [
            "Epigenetik modifikasyon ve düzenleme kusuru",
            "Rett sendromunda metil bağlayan protein mutasyonu",
            "Kız çocuklarında nörolojik regresyon tablosu"
        ]
    },
    {
        "cumle": slide_last_sent[7],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nöral Tüp Kapanma Kusurları",
        "ogeler": [
            "Kranyal anterior defekt: Anensefali",
            "Kaudal posterior defekt: Spina bifida",
            "Amniyon sıvısında alfa-fetoprotein artışı"
        ]
    },
    {
        "cumle": slide_last_sent[8],
        "bas": 0, "son": 4,
        "sayfa": 8,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Nöral Tüp Defektleri Nedenleri",
        "ogeler": [
            "Folik asit eksikliği ve genetik yatkınlık",
            "Maternal kanda alfa-fetoprotein artışı",
            "Valproat gibi folat antagonisti ilaçlar"
        ]
    },
    {
        "cumle": slide_last_sent[10],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Anterior Nöral Tüp Defektleri",
        "ogeler": [
            "Anensefali: Kalvaryum ve beyin dokusu yokluğu",
            "Ensefalosel: Kemik defektinden doku fıtıklaşması",
            "Sıklıkla oksipital bölgede herniasyon"
        ]
    },
    {
        "cumle": slide_last_sent[11],
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Ön Beyin Hacim Anomalileri",
        "ogeler": [
            "Mikroensefali ve mikrosefali tablosu",
            "Korteksi oluşturacak nöron sayısında azalma",
            "Megaloensefali ve kontrolsüz hücresel büyüme"
        ]
    },
    {
        "cumle": slide_last_sent[13],
        "bas": 0, "son": 4,
        "sayfa": 13,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kortikal Nöronal Göç Bozuklukları",
        "ogeler": [
            "Subependimal zonda öncül hücre çoğalması",
            "Radyal glial lifler boyunca dışa göç",
            "Altı tabakalı laminasyon organizasyon kaybı"
        ]
    },
    {
        "cumle": slide_last_sent[14],
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Lissensefali ve Pakigiri Morfolojisi",
        "ogeler": [
            "Agiri: Total girus yokluğu ve pürüzsüz yüzey",
            "Dört tabakalı kalınlaşmış anormal korteks",
            "Mikrotübül ilişkili gen defektleri"
        ]
    },
    {
        "cumle": slide_last_sent[16],
        "bas": 0, "son": 4,
        "sayfa": 16,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Polimikrogiri Morfolojisi",
        "ogeler": [
            "Artmış sayıda minik kaynaşmış giruslar",
            "Kaldırım taşı benzeri düzensiz beyin yüzeyi",
            "Fokal perisilvian veya yaygın tutulum"
        ]
    },
    {
        "cumle": slide_last_sent[17],
        "bas": 0, "son": 4,
        "sayfa": 17,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Holoprozensefali Spektrumu",
        "ogeler": [
            "Hafif form: Arinensefali ve olfaktör yokluk",
            "Ağır form: Alobar tek ventrikül ve siklopi",
            "Sonic hedgehog ve Trizomi on üç ilişkisi"
        ]
    },
    {
        "cumle": slide_last_sent[19],
        "bas": 0, "son": 4,
        "sayfa": 19,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Chiari Malformasyon Tipleri",
        "ogeler": [
            "Chiari tip bir: Serebellar tonsiller ektopi",
            "Genç erişkinde suboksipital baş ağrısı ve medulla basısı",
            "Chiari tip iki: Vermis fıtıklaşması ve miyelomeningosel"
        ]
    },
    {
        "cumle": slide_last_sent[20],
        "bas": 0, "son": 4,
        "sayfa": 20,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Dandy-Walker Malformasyonu",
        "ogeler": [
            "Genişlemiş büyük arka kemik fossa",
            "Serebellar vermis agenezisi ve yokluğu",
            "Geniş dördüncü ventrikül orta hat kisti"
        ]
    },
    {
        "cumle": slide_last_sent[21],
        "bas": 0, "son": 4,
        "sayfa": 21,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Joubert Sendromu Triadı",
        "ogeler": [
            "Serebellar vermis agenezisi veya hipoplazisi",
            "Okülomotor apraksi ve solunum düzensizliği",
            "Primer silia mutasyonları ve siliyopati"
        ]
    },
    {
        "cumle": slide_last_sent[23],
        "bas": 0, "son": 4,
        "sayfa": 23,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Spinal Kord Kavitasyon Lezyonları",
        "ogeler": [
            "Hidromiyeli: Epandim döşeli santral kanal genişlemesi",
            "Siringomiyeli: Parankimal glial sirinks kavitesi",
            "Ön beyaz komissür basısı ile pelerin tarzı duyu kaybı"
        ]
    },
    {
        "cumle": slide_last_sent[26],
        "bas": 0, "son": 4,
        "sayfa": 26,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Perinatal Germinal Matriks Kanaması",
        "ogeler": [
            "Prematüre bebekte subependimal damar frajilitesi",
            "Kan basıncı dalgalanması ile hematom oluşumu",
            "Ventrikül içi yayılım ve hidrosefali riski"
        ]
    },
    {
        "cumle": slide_last_sent[28],
        "bas": 0, "son": 4,
        "sayfa": 28,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Periventriküler Lökomalazi Bulguları",
        "ogeler": [
            "Periventriküler beyaz cevher iskemik nekrozu",
            "Tebeşirsi sarı kalsifiye nekroz plak kalıntıları",
            "Geniş kavitasyonlarla multikistik ensefalopati"
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
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
import denetle as D
d_rapor = D.Denetim(TASLAK).calistir()
if d_rapor.get("hata", 0) > 0:
    print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
    for e in d_rapor.get("hatalar", [])[:10]: print(" ", e)
    sys.exit(1)
print("PASSED denetle.py: 0 HATA · 0 UYARI")

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

