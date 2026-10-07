# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

GLOSSARY_PATH = 'src/data/medical_glossary.json'
ENCYCLOPEDIA_PATH = 'src/data/medical_encyclopedia.json'

with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
    glossary = json.load(f)

with open(ENCYCLOPEDIA_PATH, 'r', encoding='utf-8') as f:
    encyclopedia = json.load(f)

print(f"Başlangıç: {len(glossary)} sözlük terimi, {len(encyclopedia)} ansiklopedi maddesi")

NEW_ITEMS = [
    {
        "id": "upec",
        "term": "Üropatojenik Escherichia coli (UPEC)",
        "latinName": "Uropathogenic Escherichia coli",
        "aliases": ["UPEC", "Üropatojen E. coli"],
        "category": "mikrobiyoloji",
        "kurul": "Kurul 1",
        "discipline": "Üroloji / Enfeksiyon Hastalıkları",
        "instructorAndSource": "ÜSE Epidemiyoloji, Etyoloji ve Semptomatolojisi • Dr. F. Şamil Uysal",
        "definition": "Toplum kökenli komplike olmayan üriner sistem enfeksiyonlarının %75-90'ından sorumlu, özgül virülans faktörleri (Tip 1 pili, P fimbriyası, alfa-hemolizin) taşıyan E. coli alt grubudur.",
        "lectureContextNotes": "Dr. F. Şamil Uysal dersinde vurguladı: Dışkı florasından periüretral bölgeye tırmanan UPEC, mesane epitelindeki mannoza Tip 1 fimbriyalarıyla yapışarak sistit; renal tübüllerdeki Gal-Gal reseptörlerine P fimbriyasıyla yapışarak akut piyelonefrit yapar.",
        "morphologyOrMechanism": "Tip 1 pili (mannoz duyarlı, sistit) ve P fimbriyası (mannoz dirençli, piyelonefrit) en kritik adezinleridir. Aerobaktin ile demir çalar, alfa-hemolizin ile doku lizisi yapar.",
        "differentialDiagnosis": "Genç kadınlarda sistitte 2. en sık etken Staphylococcus saprophyticus iken; hastane kökenli ve kateter ilişkili ÜSE'lerde Proteus, Klebsiella ve Pseudomonas sıklığı artar.",
        "examSpotPearls": "TUS & Komite Sorusu: Akut piyelonefrite neden olan UPEC suşlarının böbrek toplayıcı tübül epitelindeki digalaktozid (Gal-Gal) reseptörlerine bağlanmasını sağlayan adezin 'P fimbriyası (Pap pili)'dır.",
        "pitfallsAndWarnings": "🔴 Sınav Tuzağı: Tip 1 fimbriya mesane sistitinden; P fimbriyası böbrek piyelonefritinden sorumludur.",
        "relatedItems": ["p-fimbriyasi", "akut-piyelonefrit", "akut-sistit"]
    },
    {
        "id": "p-fimbriyasi",
        "term": "P Fimbriyası (Pap Pili / Pyelonephritis-associated Pili)",
        "latinName": "Pyelonephritis-associated pili",
        "aliases": ["Pap pili", "P fimbriyası", "Mannoz-rezistan pilus"],
        "category": "mikrobiyoloji",
        "kurul": "Kurul 1",
        "discipline": "Üroloji / Tıbbi Patoloji",
        "instructorAndSource": "Üriner Sistem Enfeksiyonları • Dr. F. Şamil Uysal",
        "definition": "Üropatojen E. coli suşlarında bulunan, renal tübül hücre yüzeyindeki alfa-D-galaktopiranozil-(1-4)-beta-D-galaktopiranozid (Gal-Gal) reseptörlerine özgül olarak bağlanan mannoz-dirençli adezindir.",
        "lectureContextNotes": "Amfi Vurgusu: Normal kommensal fekal E. coli'lerde P fimbriyası bulunmaz. Bu fimbriyayı taşıyan suşlar asendan yolla böbreğe tırmanarak Akut Piyelonefrit geliştirme potansiyeline sahiptir.",
        "morphologyOrMechanism": "PapG adezin alt birimi böbrek epitelindeki P kan grubu antijenik yapısına (Gal-Gal) yüksek affiniteyle bağlanarak fagositoza karşı bakteriyi dokuya sabitler.",
        "differentialDiagnosis": "Tip 1 fimbriya mannozla inhibe edilebilirken (mannoz-sensitif), P fimbriyası mannoz eklenmesiyle inhibe olmaz (mannoz-rezistan).",
        "examSpotPearls": "Komite Sorusu: E. coli'nin böbrek parankimini tutarak piyelonefrit yapmasından sorumlu virülans faktörü P fimbriyasıdır.",
        "pitfallsAndWarnings": "🔴 Kızılcık (Cranberry) ekstresindeki proantosiyanidinler P fimbriyasının ürotelyuma yapışmasını kompetitif olarak bloke eder.",
        "relatedItems": ["upec", "akut-piyelonefrit"]
    },
    {
        "id": "fournier-gangreni",
        "term": "Fournier Gangreni (Perine Nekrotizan Fasiiti)",
        "latinName": "Gangraena Fournier",
        "aliases": ["Fournier gangreni", "Erkek genital nekrotizan fasiiti"],
        "category": "uroloji",
        "kurul": "Kurul 1",
        "discipline": "Üroloji",
        "instructorAndSource": "Üriner Sistemin Spesifik Enfeksiyonları • Doç. Dr. Salih Birlikkara",
        "definition": "Erkek perine, skrotum ve perianal dokularını tutan, fasyal planlar boyunca yıldırım hızıyla yayılan, mikst aerob-anaerob etkenlerle oluşan cerrahi acil bir nekrotizan fasiit tablosudur.",
        "lectureContextNotes": "Doç. Dr. Salih Birlikkara derste vurguladı: En sık kontrolsüz diyabetik erkeklerde, kronik alkoliklerde ve immünsüpresiflerde görülür. Cilt altında gaz varlığına bağlı 'krepitasyon' patognomoniktir.",
        "morphologyOrMechanism": "Bakteriyel sinerji: Aeroblar oksijeni tüketir -> anaeroblar (Bacteroides, Clostridium) çoğalarak fasyal iskemi ve endarterit yapar -> doku nekrozu ve gaz oluşumu -> septik şok.",
        "differentialDiagnosis": "Basit selülit veya erizipelde fasyal nekroz ve subkutan krepitasyon yoktur. Fournier gangreninde ağrı başlangıçta fiziksel bulguların çok ötesindedir.",
        "examSpotPearls": "TUS & Komite Sorusu: Fournier gangreninin tedavisinde tek başına antibiyotik ASLA yeterli değildir; ilk ve en kritik adım 'ACİL RADİKAL CERRAHİ DEBRİDMAN'dır.",
        "pitfallsAndWarnings": "🔴 Cerrahi gecikirse mortalite %40-50'ye tırmanır; hastanın yoğun bakıma alınması ve geniş spektrumlu üçlü IV antibiyotik verilmesi şarttır.",
        "relatedItems": ["ksantogranulamatoz-piyelonefrit", "amfizematöz-piyelonefrit"]
    },
    {
        "id": "ksantogranulamatoz-piyelonefrit",
        "term": "Ksantogranülamatöz Piyelonefrit (XPN)",
        "latinName": "Pyelonephritis xanthogranulomatosa",
        "aliases": ["XPN", "Ksantogranülomatöz piyelonefrit"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Üroloji",
        "instructorAndSource": "Üriner Sistemin Spesifik Enfeksiyonları • Doç. Dr. Salih Birlikkara",
        "definition": "Böbreğin kronik obstrüksiyonu ve Proteus mirabilis enfeksiyonu zemininde gelişen, böbrek parankimini harap ederek lipid yüklü köpüksü histiyositlerle (ksantom hücreleri) dolduran destrüktif kronik granülomatöz lezyondur.",
        "lectureContextNotes": "Amfi Vurgusu: Radyolojik ve klinik olarak Renal Hücreli Karsinomu (RCC) birebir taklit eden psödotümoral bir lezyondur. Kontrastlı BT'de pelvisteki koraliform taşa komşu genişlemiş hipodens kaliksler 'Ayı Pençesi (Bear Paw)' işareti verir.",
        "morphologyOrMechanism": "Pelviste staghorn taş -> kaliks obstrüksiyonu -> Proteus enfeksiyonu -> doku destrüksiyonu -> lipid fagosite eden histiyositler ve dev hücreler ile psödotümör kitlesi.",
        "differentialDiagnosis": "RCC berrak hücrelerinde glikojen ve lipid boldur ancak XPN'deki gibi yoğun granülasyon dokusu ve köpüksü histiyosit infiltrasyonu değil, malign epitelyal neoplazi vardır.",
        "examSpotPearls": "Komite & TUS Sorusu: BT'de 'Ayı Pençesi' görünümü veren, Proteus enfeksiyonu ve staghorn taş zemininde gelişen ve RCC ile karışan kitle: Ksantogranülamatöz Piyelonefrit.",
        "pitfallsAndWarnings": "🔴 Çoğu olguda nefrektomi öncesi RCC şüphesiyle ameliyata girilir; kesin ayrım histopatolojik incelemeyle yapılır.",
        "relatedItems": ["fournier-gangreni", "proteus-mirabilis", "bobrek-tumorleri"]
    },
    {
        "id": "malakoplaki",
        "term": "Malakoplaki ve Michaelis-Gutmann Cisimcikleri",
        "latinName": "Malakoplakia",
        "aliases": ["Malakoplaki", "Michaelis-Gutmann cisimcikleri"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Üroloji",
        "instructorAndSource": "Üriner Sistemin Spesifik Enfeksiyonları • Doç. Dr. Salih Birlikkara",
        "definition": "Kronik bakteriyel enfeksiyonlara (özellikle E. coli) karşı histiyositlerin fagozom-lizozom füzyon defekti sonucu bakterileri sindirememesiyle karakterize, mesanede sarı-yumuşak plaklar oluşturan granülomatöz hastalıktır.",
        "lectureContextNotes": "Amfi Vurgusu: Histopatolojide histiyositler içinde demir ve kalsiyum mineralizasyonu gösteren konsantrik lameller hedef tahtası benzeri inklüzyonlara 'Michaelis-Gutmann Cisimcikleri' denir.",
        "morphologyOrMechanism": "Makrofaj içi bakterisidal defekt -> sindirilemeyen bakteri kalıntıları üzerine kalsiyum ve demir tuzlarının konsantrik çökmesi -> Michaelis-Gutmann cisimcikleri. Von Hansemann histiyositleri.",
        "differentialDiagnosis": "Sistoskopide mesane tümörünü taklit eden sarımsı plaklar izlenir; biyopside Michaelis-Gutmann cisimciklerinin görülmesiyle karsinomdan ayırt edilir.",
        "examSpotPearls": "TUS & Komite Sorusu: Malakoplakinin patognomonik histopatolojik bulgusu olan konsantrik lamine kalsifiye yapılar: 'Michaelis-Gutmann cisimcikleri'dir (Von Kossa ve Prusya mavisi pozitif).",
        "pitfallsAndWarnings": "🔴 Kolinerjik agonistler (Bethanechol) makrofaj içi siklik GMP düzeyini artırarak fagozom füzyonunu uyarır.",
        "relatedItems": ["ksantogranulamatoz-piyelonefrit", "upec"]
    },
    {
        "id": "schistosoma-haematobium",
        "term": "Schistosoma haematobium (Üriner Bilharyazis)",
        "latinName": "Schistosoma haematobium",
        "aliases": ["Bilharyazis", "Üriner şistozomiyaz"],
        "category": "parazitoloji",
        "kurul": "Kurul 1",
        "discipline": "Üroloji / Tıbbi Patoloji",
        "instructorAndSource": "Üriner Sistemin Spesifik Enfeksiyonları • Doç. Dr. Salih Birlikkara",
        "definition": "Tatlı su salyangozlarından dökülen serkaryaların deriyi delmesiyle bulaşan, vezikal venöz pleksusa yerleşerek mesane duvarında granülomatöz lezyonlar ve kalsifikasyon oluşturan trematod parazittir.",
        "lectureContextNotes": "Doç. Dr. Salih Birlikkara derste altını çizdi: İdrar sedimentinde 'terminal dikenli' yumurtaların görülmesi tanısaldır. En hayati onkolojik sonucu: Mesanenin Skuamöz Hücreli (Yassı Epitel) Karsinomuna yol açmasıdır!",
        "morphologyOrMechanism": "Yumurtalar mesane mukozasında granülom, kumlu yamalar (sandy patches) ve kronik irritasyon yapar -> skuamöz metaplazi -> Yassı hücreli karsinom transformasyonu.",
        "differentialDiagnosis": "Schistosoma mansoni ve japonicum intestinal tutulum yaparken ve lateral dikenli yumurtalara sahipken; S. haematobium üriner tutulum yapar ve terminal dikenlidir.",
        "examSpotPearls": "Komite & TUS Sorusu: Mesanede transizyonel (ürotelyal) karsinom DEĞİL, 'Skuamöz Hücreli Karsinom' riskini belirgin artıran parazit Schistosoma haematobium'dur.",
        "pitfallsAndWarnings": "🔴 Tedavide altın standart tek gün oral Prazikuantel uygulamasıdır.",
        "relatedItems": ["mesane-tumorleri", "skuamoz-hucreli-karsinom"]
    },
    {
        "id": "steril-piyuri",
        "term": "Steril Piyüri",
        "latinName": "Pyuria sterilis",
        "aliases": ["Kültür negatif piyüri", "Steril lökositüri"],
        "category": "uroloji",
        "kurul": "Kurul 1",
        "discipline": "Üroloji / Enfeksiyon Hastalıkları",
        "instructorAndSource": "Üriner Sistemin Spesifik Enfeksiyonları • Doç. Dr. Salih Birlikkara",
        "definition": "İdrar mikroskopisinde santrifüjsüz idrarda $\\ge 10$ lökosit/mm3 bulunmasına rağmen, standart bakteriyolojik besiyerlerinde (kanlı ve EMB agar) üreme olmaması durumudur.",
        "lectureContextNotes": "Amfi Vurgusu: Antibiyotik tedavisine yanıt vermeyen, dizüri ve hematürisi olan genç bir hastada steril piyüri saptandığında ilk akla 'Ürogenital Tüberküloz' gelmelidir!",
        "morphologyOrMechanism": "Etkenler: 1. Mycobacterium tuberculosis, 2. Chlamydia trachomatis, 3. Mycoplasma / Ureaplasma, 4. Viral sistitler (Adenovirüs), 5. Fungal etkenler, 6. Ürolitiyazis, interstisyel sistit, analjezik nefropatisi.",
        "differentialDiagnosis": "Yakın zamanda antibiyotik kullanmış hastalarda bakteriyel üreme baskılandığı için geçici steril piyüri görülebilir.",
        "examSpotPearls": "Komite Sorusu: Steril piyürinin en klasik ve ekarte edilmesi gereken enfeksiyöz nedeni Ürogenital Tüberkülozdur (3 ardışık sabah idrarında ARB ve kültür istenir).",
        "pitfallsAndWarnings": "🔴 Steril piyüri tespit edildiğinde hastaya körlemesine florokinolon verilmemeli; mikobakteriyel ve klamidya testleri yapılmalıdır.",
        "relatedItems": ["urogenital-tuberkuloz", "akut-sistit"]
    },
    {
        "id": "temel-ureme-katsayisi-r0",
        "term": "Temel Üreme Katsayısı (R0 / Basic Reproduction Number)",
        "latinName": "R-naught",
        "aliases": ["R0", "R sıfır", "Temel çoğalma hızı"],
        "category": "epidemiyoloji",
        "kurul": "Kurul 1",
        "discipline": "Halk Sağlığı / Enfeksiyon Hastalıkları",
        "instructorAndSource": "Enfeksiyon Hastalıklarının Genel Epidemiyolojik Özellikleri • Uzm. Dr. Merve Kaçar",
        "definition": "Tümüyle duyarlı (hiç bağışıklığı olmayan) bir popülasyonda enfekte bir indeks vakanın bulaştırıcılık süresi boyunca doğrudan enfekte ettiği ortalama ikincil vaka sayısıdır.",
        "lectureContextNotes": "Uzm. Dr. Merve Kaçar derste vurguladı: R0 > 1 ise vaka sayısı geometrik artar ve salgın büyür; R0 = 1 ise hastalık endemik kalır; R0 < 1 ise enfeksiyon zamanla kendiliğinden sönümlenir.",
        "morphologyOrMechanism": "R0 = Bulaş olasılığı (c) x Temas hızı (d) x Bulaştırıcılık süresi (v). Filyasyon ve izolasyon temas hızını ve bulaştırıcılığı azaltarak R0'ı 1'in altına düşürür.",
        "differentialDiagnosis": "R0 teorik başlangıç katsayısıdır; toplumda aşı veya bağışıklık geliştikten sonraki anlık üreme katsayısına ise Efektif Üreme Katsayısı (Re veya Rt) denir.",
        "examSpotPearls": "Komite & TUS Sorusu: Bir salgının durdurulabilmesi için efektif üreme sayısının (Rt) mutlaka 1'in altına (Rt < 1) indirilmesi zorunludur.",
        "pitfallsAndWarnings": "🔴 Kızamık R0 = 12-18 ile bilinen en yüksek bulaşıcılığa sahip enfeksiyon etkenidir.",
        "relatedItems": ["suru-bagisikligi-esigi", "salgin-incelemesi"]
    },
    {
        "id": "suru-bagisikligi-esigi",
        "term": "Sürü Bağışıklığı Eşiği (Herd Immunity Threshold - HIT)",
        "latinName": "Herd immunity threshold",
        "aliases": ["Toplum bağışıklığı eşiği", "Kolektif bağışıklık"],
        "category": "epidemiyoloji",
        "kurul": "Kurul 1",
        "discipline": "Halk Sağlığı",
        "instructorAndSource": "Enfeksiyon Hastalıklarının Genel Epidemiyolojik Özellikleri • Uzm. Dr. Merve Kaçar",
        "definition": "Bir toplumda hastalığın yayılmasını durdurmak ve bağışık olmayan bireyleri de dolaylı olarak korumak için aşılanması veya bağışık olması gereken minimum nüfus yüzdesidir.",
        "lectureContextNotes": "Amfi Formülü: HIT = 1 - (1 / R0). R0 değeri ne kadar yüksekse, sürü bağışıklığı sağlamak için gereken aşılama oranı da o kadar yüksek olmak zorundadır.",
        "morphologyOrMechanism": "Toplumda bağışık bireyler artınca patojen duyarlı konak bulamaz ve bulaşma zinciri kırılır; böylece aşı olamayan kanserli hastalar ve bebekler de korunur.",
        "differentialDiagnosis": "Bireysel bağışıklık sadece aşılanan kişiyi korurken; sürü bağışıklığı tüm toplumu şemsiye gibi korur.",
        "examSpotPearls": "TUS & Komite Sorusu: R0 değeri 4 olan bir hastalıkta salgını durdurmak için toplumun en az %75'i bağışık olmalıdır (1 - 1/4 = 0.75).",
        "pitfallsAndWarnings": "🔴 Aşı reddi sürü bağışıklığı eşiğinin altına düşülmesine ve elimine edilmiş kızamık gibi hastalıkların yeniden patlamasına (re-emerging) neden olur.",
        "relatedItems": ["temel-ureme-katsayisi-r0", "genisletilmis-bagisiklama-programi"]
    },
    {
        "id": "john-snow-broad-street",
        "term": "John Snow ve Broad Street Kolera Salgını (1854)",
        "latinName": "John Snow cholera investigation",
        "aliases": ["John Snow", "Modern epidemiyolojinin babası"],
        "category": "halk-sagligi",
        "kurul": "Kurul 1",
        "discipline": "Halk Sağlığı",
        "instructorAndSource": "Halk Sağlığı Tarihçesi ve Koruyucu Hekimlik • Doç. Dr. Nergiz Sevinç",
        "definition": "1854 Londra Soho kolera salgınında vakaları harita üzerinde noktalayarak (spot map) hastalığın miasma (kötü hava) ile değil, Broad Street tulumbasından içilen kontamine su ile bulaştığını kanıtlayan ve tulumba kolunu söktürerek salgını durduran hekimdir.",
        "lectureContextNotes": "Doç. Dr. Nergiz Sevinç derste vurguladı: Robert Koch kolera basilini (Vibrio cholerae) mikroskopta izole etmeden 30 yıl önce, John Snow tamamen epidemiyolojik gözlem ve haritalama ile su kaynaklı bulaşı kanıtlamış ve tarihin ilk analitik saha epidemiyoloğu olmuştur.",
        "morphologyOrMechanism": "Su şirketlerinin (Southwark & Vauxhall vs Lambeth) kaynaklarını karşılaştırmış; lağım karışan Thames suyunu kullanan abonelerde kolera ölümünün 14 kat fazla olduğunu göstermiştir.",
        "differentialDiagnosis": "O dönem hakim olan 'Miasma teorisi' (hastalıkların bataklık gazı ve kokulardan çıktığı inancı) Snow'un çalışmasıyla çökertilmiştir.",
        "examSpotPearls": "Komite & TUS Sorusu: Modern epidemiyolojinin kurucusu kimdir? Cevap: Dr. John Snow (1854 Londra Kolera Salgını).",
        "pitfallsAndWarnings": "🔴 Snow tulumba kolunu söktürerek halk sağlığında 'bulaşma yolunun kesilmesi' ilkesinin ilk evrensel örneğini vermiştir.",
        "relatedItems": ["alma-ata-bildirgesi", "salgin-incelemesi"]
    },
    {
        "id": "alma-ata-bildirgesi",
        "term": "Alma-Ata Bildirgesi (1978) ve Temel Sağlık Hizmetleri",
        "latinName": "Alma-Ata Declaration",
        "aliases": ["Alma-Ata", "Temel Sağlık Hizmetleri", "Herkes için Sağlık 2000"],
        "category": "halk-sagligi",
        "kurul": "Kurul 1",
        "discipline": "Halk Sağlığı",
        "instructorAndSource": "Halk Sağlığı Tarihçesi ve Koruyucu Hekimlik • Doç. Dr. Nergiz Sevinç",
        "definition": "1978 yılında DSÖ ve UNICEF öncülüğünde Kazakistan'ın Alma-Ata şehrinde kabul edilen, '2000 Yılında Herkes İçin Sağlık' hedefini ilan eden ve koruyucu hekimliği esas alan Temel Sağlık Hizmetleri (TSH) modelini başlatan tarihi bildirgedir.",
        "lectureContextNotes": "Amfi Vurgusu: Bildirgenin 4 temel taşı: 1. Eşitlik, 2. Toplum katılımı, 3. Sektörler arası işbirliği, 4. Uygun teknoloji kullanımıdır. Pahalı hastane tıbbı yerine birinci basamak koruyucu hekimlik savunulmuştur.",
        "morphologyOrMechanism": "Temel bileşenler: Temiz su ve sanitasyon, ana-çocuk sağlığı ve aile planlaması, temel ilaçların sağlanması, bulaşıcı hastalıklara karşı aşılama ve sağlık eğitimi.",
        "differentialDiagnosis": "Ottawa Şartı (1986) sağlığı geliştirmeye (health promotion) odaklanırken; Alma-Ata (1978) birinci basamak temel sağlık hizmetlerinin evrensel örgütlenmesine odaklanır.",
        "examSpotPearls": "Komite Sorusu: 'Herkes İçin Sağlık 2000' sloganıyla Temel Sağlık Hizmetlerini küresel standart haline getiren uluslararası belge Alma-Ata Bildirgesi'dir.",
        "pitfallsAndWarnings": "🔴 Sağlıkta eşitsizliklerin kabul edilemez olduğu ve sağlığın temel bir insan hakkı olduğu ilk kez bu kadar güçlü vurgulanmıştır.",
        "relatedItems": ["john-snow-broad-street", "kuaterner-koruma"]
    },
    {
        "id": "kuaterner-koruma",
        "term": "Kuaterner Koruma (Dördüncül Koruma / Aşırı Tıbbileştirmeyi Önleme)",
        "latinName": "Quaternary prevention",
        "aliases": ["Kuaterner koruma", "Aşırı tanı ve tedaviyi önleme"],
        "category": "halk-sagligi",
        "kurul": "Kurul 1",
        "discipline": "Halk Sağlığı",
        "instructorAndSource": "Halk Sağlığı Tarihçesi ve Koruyucu Hekimlik • Doç. Dr. Nergiz Sevinç",
        "definition": "Aşırı tıbbileştirme (over-medicalization) ve iyatrojenik zarar riski taşıyan hastaları belirleyerek, onları gereksiz tetkik, polifarmasi, aşırı tanı ve invaziv tıbbi müdahalelerden koruma faaliyetidir.",
        "lectureContextNotes": "Doç. Dr. Nergiz Sevinç derste açıkladı: Hipokrat'ın 'Primum non nocere' (Önce zarar verme) ilkesinin 21. yüzyıldaki izdüşümüdür. Örneğin basit viral ÜSYE'de antibiyotik yazmamak kuaterner korumadır.",
        "morphologyOrMechanism": "Koruma Piramidi: Primordial (risk yokken politik önlem), Primer (risk varken aşı/eğitim), Sekonder (erken tanı/tarama), Tersiyer (komplikasyon/rehabilitasyon), Kuaterner (tıbbın hastaya zarar vermesini önleme).",
        "differentialDiagnosis": "Tersiyer koruma hastalığın komplikasyonunu önlerken; kuaterner koruma 'doktorun ve tıbbi sistemin' hastaya gereksiz girişimlerle zarar vermesini önler.",
        "examSpotPearls": "Komite & TUS Sorusu: Bir hekimin gereksiz tetkik ve polifarmasiyi engelleyerek hastayı tıbbi zarardan (iyatrojenezis) koruması 'Kuaterner Koruma'dır.",
        "pitfallsAndWarnings": "🔴 Asemptomatik bakteriüride antibiyotik başlamamak kuaterner korumanın en tipik örneğidir.",
        "relatedItems": ["alma-ata-bildirgesi", "asemptomatik-bakteriuri"]
    }
]

# Append new encyclopedia items
seen_enc_ids = {e['id'] for e in encyclopedia}
added_enc = 0
for ni in NEW_ITEMS:
    if ni['id'] not in seen_enc_ids:
        encyclopedia.append(ni)
        seen_enc_ids.add(ni['id'])
        added_enc += 1

# Append new glossary items (glossary is a dict: key -> object)
added_glo = 0
for ni in NEW_ITEMS:
    t_name = ni['term'].split(' (')[0].strip()
    key_low = t_name.lower()
    if key_low not in glossary:
        glossary[key_low] = {
            "term": t_name,
            "category": ni.get('category', 'hastalik'),
            "description": ni['definition'],
            "clinicalPearl": ni['examSpotPearls'],
            "discipline": ni.get('discipline', 'Tıp'),
            "committee": ni.get('kurul', 'Kurul 1'),
            "definition": ni['definition']
        }
        added_glo += 1

with open(ENCYCLOPEDIA_PATH, 'w', encoding='utf-8') as f:
    json.dump(encyclopedia, f, ensure_ascii=False, indent=2)

with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
    json.dump(glossary, f, ensure_ascii=False, indent=2)

print(f"Başarıyla eklendi: +{added_enc} ansiklopedi maddesi, +{added_glo} sözlük terimi.")
print(f"Yeni Toplam: {len(encyclopedia)} ansiklopedi maddesi, {len(glossary)} sözlük terimi.")
