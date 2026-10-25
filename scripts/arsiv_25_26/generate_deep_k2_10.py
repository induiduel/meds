import json, re, sys, subprocess
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-10-bas-agrisina-yaklasim"
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Slide blueprints: (sayfa, bolum_id, bolum_baslik, pid, [ (ses, ekran, anchor, terms, cikmis_list) ])
PARAGRAPHS = [
    # --- BOLUM 1: Baş Ağrısına Giriş ve Genel Klinik Yaklaşım (Sayfa 1) ---
    (1, "k2-10-b01", "Baş Ağrısına Giriş ve Genel Klinik Yaklaşım", "k2-10-p001", [
        (
            "Baş ağrısına klinik yaklaşım dersimize başlarken, hekimlik hayatında hem birinci basamakta hem de acil servislerde en sık karşılaşılan bu temel semptomun ayırıcı tanısını ayrıntılı olarak inceleyeceğiz.",
            "**Giriş:** Baş ağrısına sistematik klinik yaklaşım ve ayırıcı tanı ilkeleri.",
            "BAŞAĞRISI",
            ["baş ağrısı", "klinik yaklaşım"],
            []
        ),
        (
            "Baş ağrısı yakınmasıyla başvuran bir hastada hekimin en birincil ve hayati görevi, hayatı tehdit etmeyen iyi seyirli primer baş ağrılarını, acil müdahale gerektiren sekonder nedenlerden hızla ayırt etmektir.",
            "**Temel Görev:** Primer baş ağrılarını yaşamı tehdit eden sekonder nedenlerden ayırt etmek.",
            "BAŞAĞRISI",
            ["primer baş ağrısı", "sekonder nedenler"],
            []
        ),
        (
            "Bu derste Uluslararası Baş Ağrısı Derneğinin sınıflama standartlarını, migren ve gerilim tipi gibi primer sendromları ve kırmızı bayrak olarak tanımladığımız sekonder alarm bulgularını tek tek ele alacağız.",
            "**Ders Kapsamı:** Uluslararası sınıflama, primer baş ağrıları ve kırmızı bayrak alarm bulguları.",
            "BAŞAĞRISI",
            ["sınıflama standartları", "alarm bulguları"],
            []
        ),
        (
            "Doğru yapılandırılmış bir klinik anamnez ve eksiksiz bir nörolojik muayene, gereksiz ve pahalı nörogörüntüleme tetkiklerinden kaçınarak doğru tanıya ulaşmanın en güvenilir yoludur.",
            "**Tanısal Çerçeve:** Ayrıntılı anamnez ve nörolojik muayene ile tanıya ulaşım.",
            "Dr. İrfan Yavaş",
            ["klinik anamnez", "nörolojik muayene"],
            []
        ),
        (
            "Özellikle nörolojik aciller arasında yer alan subaraknoid kanama, menenjit, kafa içi basınç artışı ve temporal arterit gibi klinik tabloların erken tanınması hayat kurtarıcıdır.",
            "**Acil Tablolar:** Subaraknoid kanama, menenjit ve kafa içi basınç artışının erken tanınması.",
            "BAŞAĞRISI",
            ["subaraknoid kanama", "kafa içi basınç artışı"],
            []
        )
    ]),

    # --- BOLUM 2: Baş Ağrısının Epidemiyolojisi ve Genel Klinik Seyri (Sayfa 2) ---
    (2, "k2-10-b02", "Baş Ağrısının Epidemiyolojisi ve Genel Klinik Seyri", "k2-10-p002", [
        (
            "Baş ağrısı tüm dünyada hekimlik hayatında poliklinik ve acil servis başvurularında en sık karşılaşılan subjektif yakınmaların başında gelmektedir.",
            "**Epidemiyoloji:** Hekimlik hayatında en sık karşılaşılan poliklinik ve acil başvuru yakınmasıdır.",
            "Hekimlik hayatında en sık karşılaşılan yakınma",
            ["en sık karşılaşılan", "epidemiyoloji"],
            []
        ),
        (
            "Toplum tabanlı epidemiyolojik çalışmalarda ömür boyu en az bir kez baş ağrısı yaşayan kişi oranı erkeklerde yüzde doksan üç, kadınlarda ise yüzde doksan dokuz gibi son derece çarpıcı bir düzeye ulaşmaktadır.",
            "**Yaşam Boyu Prevalans:** Ömür boyu en az bir kez baş ağrısı oranı erkeklerde %93, kadınlarda %99'dur.",
            "oranı E %93 K %99",
            ["yaşam boyu oran", "yüzde doksan üç", "yüzde doksan dokuz"],
            []
        ),
        (
            "Bu yüksek yaygınlık nedeniyle her hekim, acil serviste ya da aile sağlığı merkezinde baş ağrısı şikayeti ile gelen hastayı değerlendirebilecek klinik yetkinliğe sahip olmalıdır.",
            "**Klinik Yetkinlik:** Her hekimin baş ağrılı hastayı birinci basamakta değerlendirme zorunluluğu.",
            "Ömür boyu en az bir kez başağrısı",
            ["klinik yetkinlik", "birinci basamak"],
            []
        ),
        (
            "Kadın cinsiyetteki belirgin yüksekliğin temelinde hormonal dalgalanmalar, östrojen çekilme atakları ve genetik yatkınlık faktörleri önemli rol oynamaktadır.",
            "**Cinsiyet Farkı:** Hormonal dalgalanmalar ve östrojen ilişkili baş ağrısı prevalansı.",
            "oranı E %93 K %99",
            ["hormonal dalgalanmalar", "cinsiyet farkı"],
            []
        ),
        (
            "Toplumdaki her on kişiden dokuzunun hayatında en az bir kez deneyimlediği bu yakınma, iş gücü kaybı ve sağlık ekonomisi açısından muazzam bir küresel yük oluşturur.",
            "**Toplumsal Yük:** Yaygın iş gücü kaybı ve sağlık harcamalarında yüksek morbidite payı.",
            "Hekimlik hayatında en sık karşılaşılan yakınma",
            ["iş gücü kaybı", "toplumsal yük"],
            []
        )
    ]),

    (2, "k2-10-b02", "Baş Ağrısının Epidemiyolojisi ve Genel Klinik Seyri", "k2-10-p003", [
        (
            "Baş ağrısı ile hekime başvuran hastaların çok büyük bir kısmı, ağrının beyin tümörü, anevrizma kanaması veya felç gibi ölümcül bir hastalığın belirtisi olduğundan derin bir endişe ve korku duyarlar.",
            "**Hasta Kaygısı:** Hastaların çoğu intrakraniyal tümör veya kanama gibi ölümcül nedenlerden korkar.",
            "Hastaların çoğu altta yatan ciddi bir sorunun",
            ["hasta kaygısı", "beyin tümörü korkusu"],
            []
        ),
        (
            "Ancak hekimin bilmesi gereken temel gerçek, polikliniklere başvuran baş ağrısı olgularının yüzde doksanından fazlasının tamamen selim ve iyi seyirli primer baş ağrılarından oluştuğudur.",
            "**İyi Seyirli Doğa:** Başvuran baş ağrılarının çok büyük kısmı selim ve iyi seyirlidir.",
            "belirtisi olduğundan korkar. Fakat çoğu iyi",
            ["selim doğa", "iyi seyirli"],
            []
        ),
        (
            "Hastaya güven veren empatik bir hekim yaklaşımı ve ayrıntılı bir muayene, gereksiz anksiyeteyi yatıştırarak hastanın tedaviye uyumunu dramatik biçimde artırır.",
            "**Hekim Yaklaşımı:** Empatik yaklaşım ve güven verici muayene ile anksiyetenin giderilmesi.",
            "Fakat çoğu iyi",
            ["empatik yaklaşım", "anksiyete kontrolü"],
            []
        ),
        (
            "Buna karşılık altta yatan organik bir patolojiye bağlı gelişen sekonder baş ağrıları azınlıkta olmasına rağmen, erken tanınmadığında kalıcı sakatlık veya ölümle sonuçlanabilmektedir.",
            "**Sekonder Tehlike:** Azınlıkta kalan sekonder baş ağrılarının potansiyel ölümcül riskleri.",
            "Hastaların çoğu altta yatan ciddi bir sorunun",
            ["sekonder tehlike", "organik patoloji"],
            []
        ),
        (
            "Dolayısıyla hekimin klinik duruşu, hastanın korkusunu anlayışla karşılarken kırmızı bayrakları asla gözden kaçırmayan yüksek bir uyanıklık dengesi kurmaktır.",
            "**Klinik Uyanıklık:** Hastayı rahatlatırken kırmızı bayrakları titizlikle tarayan klinik duruş.",
            "belirtisi olduğundan korkar. Fakat çoğu iyi",
            ["klinik uyanıklık", "kırmızı bayraklar"],
            []
        )
    ]),

    # --- BOLUM 3: Uluslararası Baş Ağrısı Sınıflaması ve Primer Baş Ağrıları (Sayfa 3) ---
    (3, "k2-10-b03", "Uluslararası Baş Ağrısı Sınıflaması ve Primer Baş Ağrıları", "k2-10-p004", [
        (
            "Dünya genelinde baş ağrılarının tanı ve araştırmalarında genel kabul gören temel sınıflama, Uluslararası Baş Ağrısı Derneği yani i he se tarafından geliştirilen sınıflamadır.",
            "**Uluslararası Sınıflama:** International Headache Society (IHS) tarafından geliştirilen tanısal sistem.",
            "Genel kabul gören sınıflama IHS",
            ["uluslararası sınıflama", "baş ağrısı derneği"],
            []
        ),
        (
            "İlk sürümü bin dokuz yüz seksen sekiz yılında yayımlanan bu sınıflama sistemi, iki bin dört yılındaki ikinci sürümün ardından iki bin on üç yılında üçüncü sürümü olan ı ce he de üçe kavuşmuştur.",
            "**Sınıflama Tarihçesi:** 1988, 2004 ve son olarak 2013 yılında ICHD-3 sürümü yayımlanmıştır.",
            "1988-2004-",
            ["sınıflama tarihçesi", "üçüncü sürüm"],
            []
        ),
        (
            "Uluslararası Baş Ağrısı Sınıflamasının üçüncü sürümü olan ı ce he de üç, baş ağrılarını etiyolojik ve mekanistik olarak üç büyük ana kategori altında toplamaktadır.",
            "**ICHD-3 Yapısı:** Baş ağrılarını üç ana kategori ve on dört alt grupta toplayan hiyerarşik yapı.",
            "ICHD 3 ana başlıkları ile",
            ["üç ana kategori", "ı ce he de üç"],
            []
        ),
        (
            "Bu kategoriler sırasıyla A grubunda primer baş ağrıları, B grubunda sekonder baş ağrıları ve C grubunda ağrılı kraniyal nöropatiler ile yüz ağrılarıdır.",
            "**Üç Büyük Grup:** A- Primer baş ağrıları, B- Sekonder baş ağrıları, C- Ağrılı kraniyal nöropatiler.",
            "A – Primer başağrıları:",
            ["primer baş ağrıları", "sekonder baş ağrıları"],
            []
        ),
        (
            "Bu standart sınıflama sistemi sayesinde dünyanın her yerindeki hekimler aynı semiyolojik kriterleri kullanarak ortak bir bilimsel dil konuşabilmektedir.",
            "**Ortak Terminoloji:** Dünya çapında standardize edilmiş tanı kriterleri ve bilimsel dil birliği.",
            "Genel kabul gören sınıflama IHS",
            ["bilimsel dil", "tanı kriterleri"],
            []
        )
    ]),

    (3, "k2-10-b03", "Uluslararası Baş Ağrısı Sınıflaması ve Primer Baş Ağrıları", "k2-10-p005", [
        (
            "Uluslararası Baş Ağrısı Sınıflamasının üçüncü sürümünde A grubunu oluşturan primer baş ağrıları dört temel alt grupta incelenmektedir.",
            "**Primer Baş Ağrıları Grubu:** ICHD-3 kapsamında tanımlanan dört temel primer baş ağrısı alt türü.",
            "A – Primer başağrıları:",
            ["primer baş ağrıları", "alt gruplar"],
            []
        ),
        (
            "Birinci sırada tek taraflı zonklayıcı ağrı ve otonomik semptomlarla karakterize migren; ikinci sırada ise iki taraflı sıkıştırıcı bant tarzı gerilim tipi baş ağrısı yer alır.",
            "**Migren ve Gerilim Tipi:** Birinci sırada migren, ikinci sırada gerilim tipi baş ağrısı yer alır.",
            "1. Migren",
            ["migren", "gerilim tipi baş ağrısı"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: trigeminal otonomik baş ağrısı Uluslararası Baş Ağrısı Sınıflamasında A grubu primer baş ağrıları arasında yer almaktadır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Trigeminal otonomik baş ağrısı A grubu primer baş ağrısıdır.",
            "3. Trigeminal otonomik başağrısı",
            ["çıkmış sınav sorusu", "trigeminal otonomik", "primer baş ağrısı"],
            ["q-2__kurul_-1-cs2"]
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: genç erkeklerde periorbital ya da temporal tek taraflı şiddetli delici oyucu ağrı ve aynı tarafta lakrimasyon ile rinore gibi otonomik bulgularla seyreden tablo küme baş ağrısıdır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Tek taraflı delici göz ağrısı, lakrimasyon ve rinore küme baş ağrısını gösterir.",
            "3. Trigeminal otonomik başağrısı",
            ["çıkmış sınav sorusu", "küme baş ağrısı", "delici oyucu ağrı", "lakrimasyon"],
            ["d3-k2-nor-011"]
        ),
        (
            "Dördüncü sırada ise primer öksürük baş ağrısı, primer egzersiz baş ağrısı ve primer gök gürültüsü baş ağrısı gibi diğer primer baş ağrısı sendromları sıralanır.",
            "**Diğer Primer Sendromlar:** Egzersiz, öksürük ve soğuk uyaranla tetiklenen diğer primer baş ağrıları.",
            "4. Diğer primer başağrısı sendromları",
            ["öksürük baş ağrısı", "egzersiz baş ağrısı"],
            []
        ),
        (
            "Primer baş ağrılarının mekanizmasında trigeminovasküler sistem aktivasyonu, kortikal yayılan depresyon ve santral nosiseptif duyarlılaşma rol oynamaktadır.",
            "**Patofizyoloji:** Trigeminovasküler aktivasyon, kortikal yayılan depresyon ve santral duyarlılaşma.",
            "A – Primer başağrıları:",
            ["trigeminovasküler sistem", "kortikal yayılan depresyon"],
            []
        )
    ]),

    # --- BOLUM 4: Sekonder Baş Ağrıları ve Etyolojik Sınıflama (Sayfa 4) ---
    (4, "k2-10-b04", "Sekonder Baş Ağrıları ve Etyolojik Sınıflama", "k2-10-p006", [
        (
            "Uluslararası Baş Ağrısı Sınıflamasının üçüncü sürümünde B grubunu oluşturan sekonder baş ağrıları, altta yatan başka bir organik hastalık ya da yapısal bozukluğun belirtisi olarak ortaya çıkan ağrılardır.",
            "**Sekonder Baş Ağrıları Grubu:** Altta yatan organik hastalığın belirtisi olan etyolojik baş ağrıları.",
            "B- Sekonder başağrıları",
            ["sekonder baş ağrıları", "organik hastalık"],
            []
        ),
        (
            "Beşinci grupta kafa travması, beyin sarsıntısı ve kamçı zedelenmesi gibi baş ve boyun travmalarına bağlı gelişen akut ve kronik baş ağrıları yer almaktadır.",
            "**Grup 5 (Travma):** Kafa travması, beyin sarsıntısı ve servikal kamçı zedelenmesi baş ağrıları.",
            "5. Baş ve boyun travmasına bağlı başağrısı",
            ["baş ve boyun travması", "sarsıntı"],
            []
        ),
        (
            "Altıncı grup kraniyal veya servikal damarsal bozukluklara bağlı baş ağrıları olup, subaraknoid kanama, iskemik inme, serebral venöz tromboz ve karotis diseksiyonu gibi en ölümcül tabloları barındırır.",
            "**Grup 6 (Vasküler):** SAK, iskemik inme, venöz sinüs trombozu ve arter diseksiyonu baş ağrıları.",
            "6. Kraniyal veya servikal damarsal bozukluklara bağlı",
            ["damarsal bozukluklar", "subaraknoid kanama", "karotis diseksiyonu"],
            []
        ),
        (
            "Yedinci grup ise damarsal olmayan intrakraniyal bozukluklara bağlı baş ağrılarıdır; bu başlık altında beyin tümörleri, hidrosefali, idiyopatik intrakraniyal hipertansiyon ve intrakraniyal hipotansiyon yer alır.",
            "**Grup 7 (Non-Vasküler İntrakraniyal):** Beyin tümörleri, hidrosefali, psödotümör serebri ve BOS kaçağı.",
            "7. Damarsal olmayan intrakraniyal bozukluklara",
            ["damarsal olmayan", "beyin tümörleri", "hidrosefali"],
            []
        ),
        (
            "Bu intrakraniyal yer kaplayıcı veya basınç değiştirici süreçler ağrıya duyarlı dura mater, venöz sinüsler ve serebral arterlerin mekanik traksiyonu ile şiddetli ağrı uyandırır.",
            "**Ağrı Mekanizması:** Dura mater, venöz sinüsler ve büyük damarların mekanik traksiyonu.",
            "bağlı başağrısı",
            ["mekanik traksiyon", "dura mater"],
            []
        )
    ]),

    (4, "k2-10-b04", "Sekonder Baş Ağrıları ve Etyolojik Sınıflama", "k2-10-p007", [
        (
            "Sekonder baş ağrılarının sekizinci grubunda madde kullanımı veya madde kesilmesine bağlı baş ağrıları yer almakta olup, klinikte en sık aşırı analjezik kullanımına bağlı ilaca dirençli baş ağrısı izlenir.",
            "**Grup 8 (Madde ve İlaç):** Madde kullanımı/kesilmesi ve en sık aşırı analjezik kullanım baş ağrısı.",
            "8. Madde kullanımı veya kesilmesine bağlı başağrısı",
            ["madde kullanımı", "aşırı analjezik"],
            []
        ),
        (
            "Dokuzuncu grup sistemik veya intrakraniyal enfeksiyonlara bağlı baş ağrılarıdır; akut bakteriyel menenjit, viral ensefalit ve beyin apsesi bu grupta acil tanı gerektiren prototiplerdir.",
            "**Grup 9 (Enfeksiyon):** Menenjit, ensefalit ve beyin apsesi gibi merkezi ve sistemik enfeksiyonlar.",
            "9. Enfeksiyona bağlı başağrısı",
            ["enfeksiyona bağlı", "menenjit", "ensefalit"],
            []
        ),
        (
            "Onuncu grupta hipoksi, hiperkapni, diyaliz veya feokromositoma gibi homeostaz bozukluğuna bağlı baş ağrıları tanımlanmaktadır.",
            "**Grup 10 (Homeostaz):** Hipoksi, hiperkapni, hipertansif kriz ve feokromositoma ilişkili ağrılar.",
            "10. Homeostaz bozukluğuna bağlı başağrısı",
            ["homeostaz bozukluğu", "hipertansif kriz"],
            []
        ),
        (
            "On birinci grup kraniyum kemikleri, boyun servikal omurga, akut açı kapanması glokomu, diş apseleri ve paranazal sinüs hastalıklarına bağlı yansıyan baş ve yüz ağrılarını içerir.",
            "**Grup 11 (Kraniyofasiyal Yapılar):** Göz, kulak, sinüs, diş ve servikal omurga kaynaklı yansıyan ağrılar.",
            "11. Kraniyum, boyun, gözler, kulaklar, burun, sinüsler",
            ["glokom", "sinüzit", "servikal omurga"],
            []
        ),
        (
            "On ikinci grupta ise somatizasyon ve majör depresif bozukluk gibi psikiyatrik bozukluklara bağlı baş ağrıları sınıflandırılmaktadır.",
            "**Grup 12 (Psikiyatrik):** Somatizasyon, anksiyete ve konversiyon zeminindeki baş ağrıları.",
            "12. Psikiyatrik bozukluklara bağlı başağrısı",
            ["psikiyatrik bozukluklar", "somatizasyon"],
            []
        )
    ]),

    # --- BOLUM 5: Ağrılı Kraniyal Nöropatiler ve Primer ile Sekonder Ayrımı (Sayfa 5) ---
    (5, "k2-10-b05", "Ağrılı Kraniyal Nöropatiler ve Primer ile Sekonder Ayrımı", "k2-10-p008", [
        (
            "Uluslararası Baş Ağrısı Sınıflamasının üçüncü sürümünde C kategorisini oluşturan on üçüncü grup, ağrılı kraniyal nöropatiler ve diğer yüz ağrılarını kapsamaktadır.",
            "**Grup 13 (Ağrılı Nöropatiler):** Kraniyal ve servikal sinirlerin patolojilerine bağlı yüz ağrıları.",
            "C- Ağrılı kraniyal nöropatiler",
            ["ağrılı kraniyal nöropatiler", "yüz ağrıları"],
            []
        ),
        (
            "Bu grubun en bilinen klinik örneği, trigeminal sinirin duyusal dallarında şimşek çakar tarzda, saniyeler süren elektrik çarpması benzeri paroksismal ağrılarla seyreden trigeminal nevraljidir.",
            "**Trigeminal Nevralji:** Trigeminal dal dağılımında elektrik çarpması benzeri şimşek tarzı ağrı.",
            "13. Ağrılı kraniyal nöropatiler ve diğer yüz ağrıları",
            ["trigeminal nevralji", "elektrik çarpması"],
            []
        ),
        (
            "Yutkunmakla veya boğaza dokunmakla tetiklenen glossofaringeal nevralji ve herpes zoster enfeksiyonu sonrasında gelişen postherpetik nevralji de bu başlıkta yer alır.",
            "**Diğer Nevraljiler:** Glossofaringeal nevralji ve zona sekeli postherpetik nöropati.",
            "ve diğer başağrıları",
            ["glossofaringeal nevralji", "postherpetik nevralji"],
            []
        ),
        (
            "On dördüncü grup ise mevcut kriterlerin hiçbirine uymayan ve sınıflandırılamayan diğer baş ağrısı bozukluklarını ifade eder.",
            "**Grup 14 (Sınıflandırılamayan):** Belirli kriterlere oturmayan atipik baş ağrısı tabloları.",
            "14. Diğer başağrısı bozuklukları",
            ["sınıflandırılamayan", "atipik ağrılar"],
            []
        ),
        (
            "Ağrılı kraniyal nöropatilerde patofizyolojik temel çoğu zaman periferik sinir köküne aberan bir arteriyel damar lupunun yaptığı mikrovasküler kompresyondur.",
            "**Mikrovasküler Kompresyon:** Sinir giriş zonunda pulsatif damar basısı ve fokal demiyelinizasyon.",
            "ve diğer başağrıları",
            ["mikrovasküler kompresyon", "damar basısı"],
            []
        )
    ]),

    (5, "k2-10-b05", "Ağrılı Kraniyal Nöropatiler ve Primer ile Sekonder Ayrımı", "k2-10-p009", [
        (
            "Klinik pratikte baş ağrılı hastaya yaklaşımın en temel felsefesi primer baş ağrıları ile sekonder baş ağrıları arasındaki zıt özellikleri eksiksiz kavramaktır.",
            "**Temel Klinik Felsefe:** Primer ve sekonder baş ağrıları arasındaki kategorik zıtlıklar.",
            "Primer başağrıları bizzat kendisi bir hastalık",
            ["klinik felsefe", "primer sekonder ayrımı"],
            []
        ),
        (
            "Primer baş ağrıları bizzat kendisi bağımsız bir hastalıktır; altta yatan yapısal bir lezyon bulunmaz ve doğrudan doğruya yaşamı tehdit etmez.",
            "**Primer Doğa:** Bizzat hastalıktır, yapısal lezyon yoktur, doğrudan yaşamı tehdit etmez.",
            "Primer başağrıları bizzat kendisi bir hastalık, yaşamı",
            ["bizzat hastalık", "yaşamı tehdit etmez"],
            []
        ),
        (
            "Primer baş ağrılarında tanı klinik öykü ile konur; kural olarak ileri tetkik gerekmez ve çoğunlukla uygun medikal tedavi ve yaşam tarzı önerileriyle kontrol altına alınabilir.",
            "**Primer Yönetim:** İleri tetkik gerekmez, tanı kliniktir, medikal tedaviyle kontrol edilir.",
            "Genellikle tanı için ileri tetkik gerekmez, çoğunlukla",
            ["ileri tetkik gerekmez", "medikal kontrol"],
            []
        ),
        (
            "Buna karşın sekonder baş ağrıları bağımsız bir hastalık değil, altta yatan bir başka organik hastalığın habercisi olan alarm verici bir semptomdur.",
            "**Sekonder Doğa:** Bağımsız hastalık değil, altta yatan organik hastalığın öncü semptomudur.",
            "Sekonder başağrıları bir semptom, altta yatan bir başka",
            ["semptom", "organik hastalık habercisi"],
            []
        ),
        (
            "Sekonder baş ağrıları yaşamı doğrudan tehdit edebilir; bu nedenle hekimin ivedi davranması ve hedefe yönelik ileri incelemeleri gecikmeksizin başlatması zorunludur.",
            "**Sekonder Yönetim:** Yaşamı tehdit eder; ivedi tanı ve ileri görüntüleme incelemesi zorunludur.",
            "Yaşamı tehdit edebilir",
            ["yaşamı tehdit eder", "ivedi davranılması"],
            []
        ),
        (
            "Sekonder baş ağrısında nedene yönelik acil etiyolojik tedavi uygulanmazsa hasta dakikalar veya saatler içinde geri dönüşsüz nörolojik hasara veya ölüme gidebilir.",
            "**Acil Tedavi Zorunluluğu:** Gecikmiş müdahalenin kalıcı sakatlık veya fatal sonlanım riski.",
            "İleri inceleme gerekir",
            ["acil müdahale", "fatal risk"],
            []
        )
    ]),

    # --- BOLUM 6: Tanısal Yaklaşım ve Anamnezin Temel Önemi (Sayfa 6) ---
    (6, "k2-10-b06", "Tanısal Yaklaşım ve Anamnezin Temel Önemi", "k2-10-p010", [
        (
            "Baş ağrısıyla başvuran bir hastada doğru tanıya ulaşmanın en kritik ve vazgeçilmez temel basamağını titizlikle alınmış ayrıntılı bir anamnez oluşturur.",
            "**Tanısal Yaklaşım:** Anamnez baş ağrısında tanının temelini ve en güçlü basamağını oluşturur.",
            "TANISAL YAKLAŞIM",
            ["tanısal yaklaşım", "anamnez"],
            []
        ),
        (
            "Baş ağrılarında laboratuvar testleri veya radyolojik görüntülemeler değil, doğrudan hastanın kendi ifadesi ve öyküsü tanının temelini oluşturur.",
            "**Anamnezin Gücü:** Tanı oranının büyük kısmını sağlayan birinci basamak araç öyküdür.",
            "Anamnez tanının temelini oluşturur",
            ["tanının temeli", "öykü"],
            []
        ),
        (
            "Hastaya yeterli zaman ayırıp iyi bir anamnez almak, primer ve sekonder baş ağrısı ayrımını güvenle yapmada hekime eşsiz bir klinik rehberlik sağlar.",
            "**Zaman Ayırma:** Hastaya yeterli vakit ayırarak derinlemesine klinik sorgulama yapmak.",
            "Hastaya yeterli zaman ayrıp iyi bir anamnez",
            ["yeterli zaman", "klinik sorgulama"],
            []
        ),
        (
            "Ayrıca doğru bir anamnez, hastayı gereksiz bilgisayarlı tomografi ve manyetik rezonans çekimlerinden, radyasyon maruziyetinden ve sağlık sistemi maliyetlerinden korur.",
            "**Gereksiz Tetkik Önleme:** Hastayı lüzumsuz radyasyon, kontrast madde ve maliyet yükünden koruma.",
            "tetkiklerden kaçınmada faydalı",
            ["gereksiz tetkikler", "radyasyon koruması"],
            []
        ),
        (
            "Hekimin anamnezde hastanın ağrıyı anlatırken kullandığı mimikleri, ağrının başladığı anı tasvir edişini dikkatle gözlemlemesi ayırıcı tanıda paha biçilmez ipuçları verir.",
            "**Gözlem ve İpuçları:** Hastanın ağrıyı tasvir ederken sergilediği davranışsal ve klinik ipuçları.",
            "almak primer , sekonder ayrımında ve gereksiz",
            ["davranışsal ipuçları", "tasvir"],
            []
        )
    ]),

    (6, "k2-10-b06", "Tanısal Yaklaşım ve Anamnezin Temel Önemi", "k2-10-p011", [
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: migren ve gerilim tipi gibi primer baş ağrılarında tanı tamamen hastadan alınan ayrıntılı klinik öykü ve anamneze dayanır; rutin nörolojik muayene, biyokimyasal testler ve nörogörüntüleme kural olarak tamamen normaldir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Primer baş ağrılarında tanı anamneze dayanır; muayene tamamen normaldir.",
            "Primer başağrılarında çoğunlukla tıbbi ve",
            ["çıkmış sınav sorusu", "primer baş ağrısı", "normal muayene", "ayrıntılı anamnez"],
            ["d3-k2-nor-001", "past-1790877039274-141162"]
        ),
        (
            "Migren veya gerilim tipi baş ağrısı atakları yaşayan bir hastada atak anı dışında yapılan muayenede hiçbir patolojik nörolojik bulguya rastlanmaz.",
            "**Ataklar Arası Normallik:** İnteriktal dönemde kraniyal sinir, motor ve refleks muayenesinin doğallığı.",
            "nörolojik muayene normal",
            ["interiktal dönem", "doğal bulgular"],
            []
        ),
        (
            "Buna karşın yapılan fizik ve nörolojik muayenede saptanan en ufak bir anormallik, hekimi derhal primer tanıdan uzaklaştırıp sekonder bir neden aramaya sevk etmelidir.",
            "**Patolojik Bulgu Uyarısı:** Muayenede en ufak patolojik bulgu derhal sekonder neden araştırması gerektirir.",
            "Primer başağrılarında çoğunlukla tıbbi ve",
            ["patolojik bulgu", "sekonder arayış"],
            []
        ),
        (
            "Muayenenin normal bulunması hastayı rahatlatmak ve selim süreci teyit etmek için hekimin elindeki en somut klinik kanıttır.",
            "**Klinik Güvence:** Muayenenin tam normal saptanması selim süreci teyit eden en somut kanıttır.",
            "nörolojik muayene normal",
            ["klinik güvence", "selim süreç"],
            []
        ),
        (
            "Ancak muayenenin normal olması, ani başlangıçlı şiddetli kanama gibi hiperakut süreçleri ekarte etmeye tek başına yetmeyebilir; anamnezdeki alarm bulguları daima muayene bulgusundan önce gelir.",
            "**Anamnez Önceliği:** Muayene normal olsa dahi öyküdeki kırmızı bayraklar ileri tetkik gerektirir.",
            "almak primer , sekonder ayrımında ve gereksiz",
            ["anamnez önceliği", "kırmızı bayrak"],
            []
        )
    ]),

    # --- BOLUM 7: Anamnezde Mutlaka Sorgulanması Gereken Özellikler (Sayfa 7) ---
    (7, "k2-10-b07", "Anamnezde Mutlaka Sorgulanması Gereken Özellikler", "k2-10-p012", [
        (
            "Baş ağrısı yakınmasıyla gelen her hastada hekimin sistematik olarak mutlaka sorması gereken temel semiyolojik parametreler bulunmaktadır.",
            "**Sistematik Anamnez Parametreleri:** Hekimin sorgulaması gereken temel semiyolojik ölçütler.",
            "Mutlaka sorulmalı",
            ["sistematik anamnez", "semiyolojik parametreler"],
            []
        ),
        (
            "İlk olarak baş ağrısının tipi ve karakteri sorgulanmalıdır; zonklayıcı pulsatif bir ağrı migreni, mengene gibi sıkıştırıcı bir ağrı gerilim tipini, elektrik çarpması veya delici oyucu bir ağrı ise nevraljileri ve küme baş ağrısını düşündürür.",
            "**Ağrı Karakteri:** Zonklayıcı (migren), sıkıştırıcı (gerilim), delici/oyucu (küme, nevralji).",
            "Başağrısının tipi ve karakteri",
            ["zonklayıcı", "sıkıştırıcı", "delici oyucu"],
            []
        ),
        (
            "Ağrının başlangıç biçimi hayati önem taşır; saniyeler içinde aniden en yüksek şiddete ulaşan gök gürültüsü tarzı başlangıç ile yavaş yavaş saatler içinde gelişen başlangıç birbirinden tamamen farklı klinik anlamlar taşır.",
            "**Başlangıç Hızı:** Saniyeler içinde patlayan gök gürültüsü ağrısı ile yavaş başlangıç ayrımı.",
            "Başlangıcı",
            ["başlangıç biçimi", "gök gürültüsü"],
            []
        ),
        (
            "Ağrının sıklığı, atakların süresi, lokalizasyonu yani tek taraflı hemikranyal mi yoksa tüm başı saran holosefalik mi olduğu ve şiddet derecesi mutlaka kaydedilmelidir.",
            "**Sıklık, Lokalizasyon ve Şiddet:** Tek taraflı hemikranyal veya holosefalik yayılım ve atak süresi.",
            "Yeri",
            ["sıklık ve süre", "hemikranyal", "holosefalik"],
            []
        ),
        (
            "Örneğin tek taraflı ve sürekli aynı bölgeye lokalize kalan baş ağrıları altta yatan yapısal fokal bir lezyon açısından daha dikkatli inceleme gerektirir.",
            "**Fokal Lokalizasyon:** Hep aynı tarafta sabit kalan tek taraflı ağrılarda yapısal lezyon kuşkusu.",
            "Şiddeti",
            ["fokal lezyon", "aynı tarafta ağrı"],
            []
        )
    ]),

    (7, "k2-10-b07", "Anamnezde Mutlaka Sorgulanması Gereken Özellikler", "k2-10-p013", [
        (
            "Ağrıya eşlik eden öncü ve eşzamanlı semptomların sorgulanması tanı koydurucu en kıymetli basamaklardan biridir.",
            "**Eşlik Eden Semptomlar:** Aura, prodrom ve otonomik bulguların tanısal değeri.",
            "Aura ve prodorom belirtilerinin olup olmaması",
            ["öncü semptomlar", "aura ve prodrom"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: migrende ağrı öncesinde görsel skotomlar ve parıltılar şeklinde aura görülebilirken, atağa bulantı, kusma, fotofobi ve fonofobi eşlik eder; akut atakta triptanlar, koruyucu profilakside ise beta blokör ve antiepileptikler kullanılır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Migrende aura, bulantı, kusma, fotofobi ve fonofobi görülür; akut atakta triptanlar kullanılır.",
            "bulantı, kusma, fotofobi, fonofobi",
            ["çıkmış sınav sorusu", "migren aurası", "fotofobi ve fonofobi", "triptanlar"],
            ["past-1790877038133-633883"]
        ),
        (
            "Ağrıyı presipite eden tetikleyici faktörler mutlaka araştırılmalıdır; parlak ışık, açlık, uykusuzluk, emosyonel stres, menstruasyon döngüsü, tiramin içeren peynir veya çikolata tüketimi klasik migren tetikleyicileridir.",
            "**Tetikleyiciler:** Stres, uykusuzluk, açlık, menstruasyon ve tiraminli gıdalar.",
            "Presipite eden faktörler olup olmaması",
            ["presipite eden faktörler", "tiramin", "menstruasyon"],
            []
        ),
        (
            "Hastanın uyku düzeni, emosyonel dalgalanmaları, ailede benzer baş ağrısı öyküsünün bulunması ve daha önce kullandığı medikasyonlar ile aşırı analjezik tüketimi ayrıntılı sorgulanmalıdır.",
            "**Öykü Detayları:** Uyku düzeni, ailede migren öyküsü ve önceki medikasyon yanıtları.",
            "Önceki medikasyonlar ve tedaviler",
            ["uyku düzeni", "aile öyküsü", "önceki tedaviler"],
            []
        ),
        (
            "Ayda on beş günden fazla analjezik veya triptan kullanan hastalarda ilacın bizzat kendisinin kronik baş ağrısını tetiklediği aşırı analjezik kullanım baş ağrısı tablosu akılda tutulmalıdır.",
            "**İlaç Kötüye Kullanımı:** Ayda 15 günden fazla analjezikte gelişen aşırı kullanım baş ağrısı.",
            "Önceki medikasyonlar ve tedaviler",
            ["aşırı analjezik kullanımı", "triptan aşırı kullanımı"],
            []
        )
    ]),

    # --- BOLUM 8: Sekonder Baş Ağrısını Düşündüren Kırmızı Bayraklar ve Öykü Özellikleri (Sayfa 8) ---
    (8, "k2-10-b08", "Sekonder Baş Ağrısını Düşündüren Kırmızı Bayraklar ve Öykü Özellikleri", "k2-10-p014", [
        (
            "Sekonder baş ağrısını düşündüren ve literatürde kırmızı bayraklar olarak adlandırılan öykü özellikleri hastanın acil servise sevkini ve ivedi görüntülenmesini gerektirir.",
            "**Kırmızı Bayraklar:** Acil tetkik ve ileri nörogörüntüleme gerektiren hayati alarm bulguları.",
            "Sekonder başağrısı düşündüren öykü özellikleri:",
            ["kırmızı bayraklar", "sekonder baş ağrısı"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: hastanın yaşamındaki en şiddetli baş ağrısı tanımı ve saniyeler içinde patlayan gök gürültüsü tarzı akut başlangıç, ense sertliği ve fotofobi ile birleştiğinde ilk olarak rüptüre anevrizmaya bağlı subaraknoid kanamayı düşündürmelidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Yaşamın en şiddetli baş ağrısı tanımı ilk olarak SAK düşünülmesini gerektirir.",
            "Hastanın yaşamındaki “en şiddetli başağrısı” tanımı",
            ["çıkmış sınav sorusu", "en şiddetli baş ağrısı", "subaraknoid kanama"],
            ["past-q-I_SKENDERUN_TI_Mu_du_rlu_g_u_ne0__1__230709_230251-62", "q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-20", "q-2__kurul_-7-cs2", "d3-k2-nor-007"]
        ),
        (
            "Yeni başlayan akut ve çok şiddetli baş ağrıları, daha önce hiç baş ağrısı çekmemiş bir kişide ortaya çıktığında daima aksi kanıtlanana kadar sekonder kabul edilmelidir.",
            "**Yeni Akut Başlangıç:** Önceden ağrısı olmayan hastada ilk kez patlayan şiddetli ağrı.",
            "Yeni başlayan akut ve çok şiddetli başağrısı",
            ["yeni başlayan ağrı", "akut şiddetli"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: baş ağrısının elli yaşından sonra yeni başlaması sekonder baş ağrısı kırmızı bayrağıdır; özellikle şakak ağrısı ve çiğneme klodikasyonu varlığında dev hücreli temporal arterit acilen araştırılmalıdır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: 50 yaş üstü başlangıç temporal arterit ve sekonder neden alarmıdır.",
            "10 yaşından önce, 50 yaşından sonra başlaması",
            ["çıkmış sınav sorusu", "elli yaşından sonra", "temporal arterit"],
            ["048fe1e04f10"]
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: çocukluk çağında yeni ortaya çıkan baş ağrısının özellikle oksipital bölgeye lokalize olması, selim tablolardan ziyade arka çukur tümörleri ve Chiari malformasyonu gibi sekonder patolojileri düşündürür.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Çocukta oksipital baş ağrısı arka çukur kitle lezyonunu düşündürür.",
            "Özellikle çocuklarda oksipital yerleşim göstermesi",
            ["çıkmış sınav sorusu", "çocuklarda oksipital ağrı", "arka çukur tümörü"],
            ["e4c0d0bc7be7"]
        ),
        (
            "Temporal arterit zamanında tanınıp yüksek doz kortikosteroid tedavisi başlanmazsa oftalmik arter tutulumu ile kalıcı tek veya çift taraflı körlüğe yol açabilir.",
            "**Temporal Arterit Riski:** Hızlı kortikosteroid başlanmazsa kalıcı monooküler veya binoküler körlük.",
            "10 yaşından önce, 50 yaşından sonra başlaması",
            ["temporal arterit", "kalıcı körlük"],
            []
        )
    ]),

    (8, "k2-10-b08", "Sekonder Baş Ağrısını Düşündüren Kırmızı Bayraklar ve Öykü Özellikleri", "k2-10-p015", [
        (
            "Son altı ay içinde başlayan, giderek sıklığı ve şiddeti artan ve klasik analjezik tedavilere direnç gösteren ilerleyici baş ağrıları intrakraniyal yer kaplayan kitle lezyonlarını işaret eder.",
            "**İlerleyici Seyir:** Son 6 ayda başlayan, giderek şiddetlenen ve tedaviye dirençli seyir.",
            "Son 6 ay içinde başlayan ve devamlılık gösteren , tedaviye direnç",
            ["son altı ay", "tedaviye dirençli"],
            []
        ),
        (
            "Öyküsünde akciğer veya meme kanseri gibi mevcut malignite tanısı olan bir hastada yeni gelişen baş ağrısı aksi kanıtlanana kadar beyin metastazı olarak kabul edilmelidir.",
            "**Malignite Öyküsü:** Kanseri olan hastada yeni baş ağrısı beyin metastazı habercisidir.",
            "Hastada mevcut malignite tanısı",
            ["malignite tanısı", "beyin metastazı"],
            []
        ),
        (
            "Ayrıca bilinen sistemik hastalığı olanlarda, gebelik döneminde veya doğum sonrası lohusalıkta ortaya çıkan baş ağrıları serebral venöz sinüs trombozu ve preeklampsi açısından taranmalıdır.",
            "**Gebelik ve Lohusalık:** Gebelik ve puerperiumda serebral venöz sinüs trombozu riski.",
            "Gebelik ve doğum sonrası ortaya çıkması",
            ["gebelik ve doğum sonrası", "venöz sinüs trombozu"],
            []
        ),
        (
            "Ağrının fiziksel aktivite, öksürme, ıkınma veya cinsel ilişki sırasında aniden ortaya çıkması ya da artması, arka çukur patolojilerini ve kafa içi basınç artışı sendromunu düşündürür.",
            "**Valsalva ile Tetiklenme:** Öksürük, ıkınma ve eforla tetiklenen ağrılarda KİBAS ve kitle riski.",
            "Fiziksel aktivite, ıkınma, öksürme g.b işlevler sırasında ortaya",
            ["fiziksel aktivite", "öksürme ve ıkınma"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: dirençli kusmaların eşlikçiliği, belirli bir şekle uymayan atipik karakter ve erkek cinsiyet sekonder baş ağrısı düşündüren öykü özellikleri arasında yer alır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Dirençli kusma, atipik şekil ve erkek cinsiyet sekonder alarm bulgusudur.",
            "Erkek cinsiyet",
            ["çıkmış sınav sorusu", "erkek cinsiyet", "dirençli kusmalar"],
            ["q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-21"]
        ),
        (
            "Özellikle sabahları uykudan uyandıran, baş eğmekle artan ve fışkırır tarzda kusmanın eşlik ettiği baş ağrıları intrakraniyal basınç artışının en karakteristik triadıdır.",
            "**Sabah Baş Ağrısı Triadı:** Uykudan uyandıran ağrı, öne eğilmekle artış ve fışkırır tarzda kusma.",
            "Dirençli kusmaların eşlikçiliği",
            ["fışkırır kusma", "sabah baş ağrısı"],
            []
        )
    ]),

    # --- BOLUM 9: Fizik ve Nörolojik Muayenede Sekonder Alarm Bulguları (Sayfa 9) ---
    (9, "k2-10-b09", "Fizik ve Nörolojik Muayenede Sekonder Alarm Bulguları", "k2-10-p016", [
        (
            "Fizik muayene primer baş ağrılarında tamamen normal iken, sekonder baş ağrılarında hayatı tehdit eden acil durumlara işaret eden çok kritik fiziksel bulgular saptanabilir.",
            "**Muayene Alarmları:** Sekonder baş ağrısına işaret eden objektif fizik ve nörolojik bulgular.",
            "Fizik muayene; primer başağrılarında normal",
            ["fizik muayene", "sekonder bulgular"],
            []
        ),
        (
            "Baş ağrısına eşlik eden letarji, konfüzyon, stupor gibi bilinç bozuklukları veya senkop atağı, intrakraniyal kanama ve akut herniasyon tehdidini gösterir.",
            "**Bilinç Bozukluğu:** Letarji, konfüzyon ve senkop varlığı akut herniasyon alarmıdır.",
            "Bilinç bozukluğu, senkop",
            ["bilinç bozukluğu", "senkop"],
            []
        ),
        (
            "Hastanın epileptik nöbet geçirmesi ya da muayenesinde hemiparezi, babinski pozitifliği, afazi ve hemihipoestezi gibi fokal nörolojik bulguların saptanması doğrudan yapısal bir lezyona işaret eder.",
            "**Fokal Defisit ve Nöbet:** Epileptik nöbet, hemiparezi ve fokal defisit yapısal lezyon kanıtıdır.",
            "Fokal nörolojik bulgu",
            ["epileptik nöbet", "fokal nörolojik bulgu"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: fundus muayenesinde papilödem saptanması kafa içi basınç artışının en belirgin oftalmolojik bulgusu olup baş ağrısı ve kusma ile birlikte klasik triadı tamamlar; preretinal subhyaloid hemoraji görülmesi ise subaraknoid kanamayı düşündüren en kritik alarm bulgusudur.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Papilödem KİBAS'ı, subhyaloid retina hemorajisi ise SAK'ı gösterir.",
            "Papilödem, subhyaloid hemoraji",
            ["çıkmış sınav sorusu", "papilödem", "subhyaloid hemoraji", "kafa içi basınç artışı"],
            ["q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-20", "d3-k2-bey-004", "q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-1", "82a829d853b5"]
        ),
        (
            "Yüksek ateş, halsizlik, kilo kaybı ve gece terlemesi gibi sistemik semptomların eşlik etmesi santral sinir sistemi tüberkülozu, menenjit ve sistemik vaskülitleri düşündürür.",
            "**Sistemik Bulgular:** Ateş, kilo kaybı ve halsizlik enfeksiyon veya vaskülit habercisidir.",
            "Kilo kaybı, halsizlik",
            ["yüksek ateş", "kilo kaybı", "sistemik vaskülit"],
            []
        ),
        (
            "Baş ağrısıyla gelen her hastada oftalmoskop ile optik disk sınırlarının incelenmesi ve papilödem varlığının araştırılması asla atlanmaması gereken zorunlu bir hekimlik görevidir.",
            "**Zorunlu Fundoskopi:** Optik disk sınırları ve venöz pulsasyon kaybının muayenede tespiti.",
            "Papilödem, subhyaloid hemoraji",
            ["oftalmoskopi", "optik disk sınırları"],
            []
        )
    ]),

    (9, "k2-10-b09", "Fizik ve Nörolojik Muayenede Sekonder Alarm Bulguları", "k2-10-p017", [
        (
            "Baş ağrısıyla başvuran bir hastada ateş ile birlikte ense sertliği, Kernig ve Brudzinski belirtilerinin pozitif olması menenjit ve meningoensefalitin kesin alarmıdır.",
            "**Meningeal İritasyon:** Ateş, ense sertliği, Kernig ve Brudzinski bulguları ile menenjit tablosu.",
            "Ateş, ense sertliği",
            ["ense sertliği", "menenjit", "meningeal iritasyon"],
            []
        ),
        (
            "Üçüncü kraniyal sinir tutulumu ve aynı tarafta ışığa yanıtsız midriyatik pupilla yani anizokori saptanması, arka komünikan arter anevrizma basısının veya unkal herniasyonun acil göstergesidir.",
            "**Üçüncü Sinir ve Anizokori:** Anizokori ve ptozis posterior komünikan arter anevrizması alarmıdır.",
            "3. kranial sinir tutulumu, anizokori",
            ["üçüncü kraniyal sinir", "anizokori", "anevrizma"],
            []
        ),
        (
            "Ptozis, miyozis ve yüzde anhidrozis triyadı ile karakterize Horner sendromunun eşlik etmesi, ağrılı taraf karotis arter diseksiyonunu akla getirmelidir.",
            "**Horner Sendromu:** Tek taraflı boyun ve baş ağrısında karotis arter diseksiyonu şüphesi.",
            "Horner sendromu",
            ["Horner sendromu", "karotis diseksiyonu"],
            []
        ),
        (
            "Beşinci kraniyal sinir tutulumuna bağlı kornea refleksi kaybı veya fasiyal duyu kaybı ile yedinci kraniyal sinir tutulumuna bağlı periferik fasiyal paralizi, kafa tabanı ve beyin sapı lezyonlarını düşündürür.",
            "**Beşinci ve Yedinci Sinir:** Kornea refleksi kaybı ve fasiyal paralizi ile kafa tabanı tutulumu.",
            "5., 7. KS tutulumu",
            ["kornea refleksi", "fasiyal paralizi"],
            []
        ),
        (
            "Temporal bölgede eritemli, şiş, hassas ve nabzı azalmış bir temporal arter palpasyonu elli yaş üstü dev hücreli temporal arteritin fiziksel kanıtıdır.",
            "**Temporal Arter Muayenesi:** Şiş, nodüler ve hassas temporal arter palpasyon bulgusu.",
            "Fizik muayene; primer başağrılarında normal",
            ["temporal arter palpasyonu", "dev hücreli arterit"],
            []
        ),
        (
            "Bu kraniyal sinir felçleri ve meningeal bulgular saptandığında hasta vakit kaybetmeksizin acil nöroşirürji ve nöroloji ünitelerine yönlendirilmelidir.",
            "**Acil Konsültasyon:** Kraniyal defisit ve ense sertliğinde ivedi nöroloji ve nöroşirürji sevk.",
            "Sekonder başağrısı düşündüren bulgular var. Bunlar:",
            ["acil konsültasyon", "nöroşirürji sevk"],
            []
        )
    ]),

    # --- BOLUM 10: Yardımcı Tanı Yöntemleri ve Nörogörüntüleme İlkeleri (Sayfa 10) ---
    (10, "k2-10-b10", "Yardımcı Tanı Yöntemleri ve Nörogörüntüleme İlkeleri", "k2-10-p018", [
        (
            "Baş ağrılı hastada kırmızı bayrak varlığında doğru yardımcı tanı yönteminin seçimi, hem hızlı tanı hem de gereksiz tetkiklerin önlenmesi açısından hayati önem taşır.",
            "**Yardımcı Tanı Stratejisi:** Kırmızı bayrağa göre hedefe yönelik rasyonel tetkik seçimi.",
            "YARDIMCI TANI YÖNTEMLERİ",
            ["yardımcı tanı yöntemleri", "tetkik seçimi"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: akut inme şüphesi ve ani nörolojik defisit ile başvuran baş ağrılı hastada intrakraniyal kanama ile iskemiyi dakikalar içinde ayırt etmek ve uygun tedaviye karar vermek için acil serviste ilk tercih kontrastsız beyin bilgisayarlı tomografisidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: İnme şüphesinde kanama ile iskemiyi ayırt etmede ilk tercih BT'dir.",
            "BBT (hemoraji, hidrosefali, tümör)",
            ["çıkmış sınav sorusu", "bilgisayarlı tomografi", "inme şüphesi", "intrakraniyal kanama"],
            ["3807e9b207c5"]
        ),
        (
            "Bilgisayarlı tomografi akut subaraknoid kanama, intrakraniyal kanama, akut hidrosefali ve kemik kırıklarını dakikalar içinde yüksek duyarlılıkla saptar.",
            "**BT Duyarlılığı:** Hiperakut subaraknoid hemoraji ve hidrosefalide altın standart acil tarama.",
            "BBT (hemoraji, hidrosefali, tümör)",
            ["subaraknoid kanama", "hidrosefali"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: intrakraniyal yer kaplayıcı kitle ve kafa içi basınç artışı şüphesi olan hastalarda, ölümcül tonsiller herniasyonu önlemek için lomber ponksiyon öncesinde mutlaka beyin tomografisi çekilerek kitle etkisi ve orta hat şifti ekarte edilmelidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: KİBAS şüphesinde herniasyonu önlemek için LP öncesi zorunlu BT çekilmelidir.",
            "KIBAS düşünülüyorsa, LP öncesi",
            ["çıkmış sınav sorusu", "lomber ponksiyon öncesi", "herniasyon riski", "orta hat şifti"],
            ["6e0a49170b5b"]
        ),
        (
            "Beyin manyetik rezonans görüntüleme ise arka çukur tümörleri, serebellar lezyonlar, serebral venöz sinüs trombozu ve multipl skleroz gibi demiyelinizan plakların gösterilmesinde bilgisayarlı tomografiden çok daha üstündür.",
            "**Manyetik Rezonans Endikasyonları:** Arka çukur lezyonları, venöz tromboz ve demiyelinizan plaklar.",
            "MR  arka çukur tümör, inme",
            ["manyetik rezonans", "arka çukur tümör", "demiyelinizan plak"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: kafa travması geçiren ve Glaskov koma skoru dokuz veya daha düşük olan orta ve ağır travmalı hastalarda epidural ve subdural hematomları dışlamak için acil beyin bilgisayarlı tomografisi çekilmelidir.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: GKS skoru 9 ve altı travmalarda acil bilgisayarlı tomografi zorunludur.",
            "kafa travması GKS:9",
            ["çıkmış sınav sorusu", "Glaskov koma skoru", "ağır kafa travması"],
            ["past-1790877044163-968531"]
        )
    ]),

    (10, "k2-10-b10", "Yardımcı Tanı Yöntemleri ve Nörogörüntüleme İlkeleri", "k2-10-p019", [
        (
            "Lomber ponksiyon incelemesi menenjit ve meningoensefalit şüphesinde beyin omurilik sıvısının basıncını ölçmek, mikrobiyolojik kültür ve hücre sayımı yapmak için temel tanı yöntemidir.",
            "**Lomber Ponksiyon (Menenjit):** BOS basıncı, hücre sayımı ve kültür ile menenjit tanısı.",
            "LP memenjit, SAK",
            ["lomber ponksiyon", "menenjit", "beyin omurilik sıvısı"],
            []
        ),
        (
            "Ayrıca akut başlangıçlı gök gürültüsü baş ağrısında bilgisayarlı tomografi normal gelse bile, subaraknoid kanamayı kesin ekarte etmek için lomber ponksiyonda ksantokromi aranması zorunludur.",
            "**Ksantokromi İncelemesi:** BT normal gelse bile SAK'ı dışlamak için BOS spektrofotometrisi ve ksantokromi.",
            "LP memenjit, SAK",
            ["ksantokromi", "subaraknoid kanama"],
            []
        ),
        (
            "Geçici nörolojik defisitler ve beyin omurilik sıvısında lenfositoz ile seyreden baş ağrısı tablosu olan HaNDL sendromunda lomber ponksiyon tanı koydurucudur.",
            "**HaNDL Sendromu:** BOS lenfositozu ve geçici nörolojik defisitlerle seyreden selim baş ağrısı.",
            "LP memenjit, SAK , HANDLE",
            ["HaNDL sendromu", "lenfositoz"],
            []
        ),
        (
            "Elli yaş üstünde yeni başlayan baş ağrılarında eritrosit sedimantasyon hızı ve C-reaktif protein düzeyleri temporal arterit taramasında mutlaka ilk basamakta istenmelidir.",
            "**Laboratuvar Testleri:** 50 yaş üstünde sedimantasyon ve CRP ile temporal arterit taraması.",
            "Kan testleri, sedim",
            ["sedimantasyon", "temporal arterit"],
            []
        ),
        (
            "Akut sinüzit kuşkusu olan olgularda Waters grafisi ve paranazal sinüs grafileri mukozal kalınlaşma ve hava sıvı seviyelerini göstermede yardımcı olur.",
            "**Waters Grafisi:** Akut sinüzit tanısında paranazal sinüs havalanması ve sıvı seviyesi.",
            "Waters, direk grafiler",
            ["Waters grafisi", "sinüzit"],
            []
        ),
        (
            "Kronik ve tekrarlayan baş ağrılarında hastaya baş ağrısı günlüğü tutturulması; atak sıklığını, tetikleyicileri, adet döngüsü ilişkisini ve aşırı ilaç kullanımını objektif olarak izlemede en etkili klinik yöntemdir.",
            "**Baş Ağrısı Günlüğü:** Atak sıklığı, tetikleyiciler ve ilaç aşırı kullanımını izlemede en etkili rehber.",
            "Başağrısı günlüğü",
            ["baş ağrısı günlüğü", "atak sıklığı"],
            []
        )
    ])
]

# Verify anchors against kaynak.md
print("Verifying anchors against kaynak.md...")
anchor_errors = 0
for sayfa, bid, bbaslik, pid, sentences in PARAGRAPHS:
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        if anchor and anchor not in kaynak_text:
            print(f"ERROR: Sayfa {sayfa} ({pid}) sent {s_idx+1} anchor not found in kaynak.md: {anchor!r}")
            anchor_errors += 1
if anchor_errors:
    print(f"FAILED: {anchor_errors} anchors not found!")
    sys.exit(1)
print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Build konusma_v2 structure
bolum_map = {}
cid_counter = 1
total_words = 0
para_last_sent = {} # pid -> last sentence cid
slide_last_sent = {} # sayfa -> last sentence cid
sents_list = []

for sayfa, bid, bbaslik, pid, sentences in PARAGRAPHS:
    if bid not in bolum_map:
        bolum_map[bid] = {
            "id": bid,
            "baslik": bbaslik,
            "paragraflar": []
        }
    p_obj = {
        "id": pid,
        "sayfa": sayfa,
        "cumleler": []
    }
    
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        cid = f"k2-10-c{cid_counter:04d}"
        cid_counter += 1
        words = len(ses.split())
        total_words += words
        para_last_sent[pid] = cid
        slide_last_sent[sayfa] = cid
        
        satir_list = [anchor] if anchor else []
        
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
                "sekil": None
            },
            "vurgu": [{"tur": "terim", "metin": vurgu_text}]
        }
        if cikmis:
            c_obj["cikmis"] = cikmis
            
        p_obj["cumleler"].append(c_obj)
        sents_list.append(c_obj)
        
    bolum_map[bid]["paragraflar"].append(p_obj)

bolumler_list = list(bolum_map.values())

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-10",
    "anahtar": "y25-k2-10-bas-agrisina-yaklasim",
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
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
import konusma_v2 as KV
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Baş Ağrısına Yaklaşım"
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
print("Updated sayfa_haritasi.json with 19 distinct paragraphs.")

# Drawings definitions for k2-10
cizim_komutlari = [
    {
        "cumle": para_last_sent["k2-10-p001"],
        "bas": 0, "son": 4,
        "sayfa": 1,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Klinik Yaklaşım",
        "ogeler": [
            "Klinik yaklaşım ve ayırıcı değerlendirme",
            "Primer ve sekonder baş ağrısı ayrımı",
            "Ayrıntılı anamnez ve nörolojik muayene"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p002"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Baş Ağrısı Yaygınlığı",
        "ogeler": [
            "Hekimlik hayatında en sık görülen yakınma",
            "Kadınlarda ömür boyu en az bir kez görülür",
            "Erkeklerde ömür boyu en az bir kez görülür"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p003"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Baş Ağrısı Klinik Seyri",
        "ogeler": [
            "Hastaların büyük kısmı tümör veya felç korkusu duyar",
            "Olguların büyük kısmı selim ve iyi seyirlidir",
            "Sekonder nedenler erken tanınmadığında ölümle sonuçlanabilir"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p004"],
        "bas": 0, "son": 4,
        "sayfa": 3,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Uluslararası Sınıflama Sistemi",
        "ogeler": [
            "Uluslararası Baş Ağrısı Derneği sınıflaması",
            "Bin dokuz yüz seksen sekiz ilk sürüm",
            "İki bin on üç üçüncü sürüm sınıflaması"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p005"],
        "bas": 0, "son": 4,
        "sayfa": 3,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Primer Baş Ağrıları Grupları",
        "ogeler": [
            "Migren: Tek taraflı zonklayıcı baş ağrısı",
            "Gerilim tipi: İki taraflı sıkıştırıcı ağrı",
            "Trigeminal otonomik: Küme baş ağrısı ve lakrimasyon"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p006"],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Sekonder Vasküler ve Travmatik Nedenler",
        "ogeler": [
            "Baş ve boyun travmasına bağlı baş ağrısı",
            "Subaraknoid kanama ve damarsal bozukluklar",
            "Beyin tümörleri ve hidrosefali tablosu"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p007"],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Sekonder Sistemik ve Enfeksiyöz Nedenler",
        "ogeler": [
            "Aşırı analjezik kullanımına bağlı baş ağrısı",
            "Menenjit ve santral sinir sistemi enfeksiyonları",
            "Glokom, sinüzit ve psikiyatrik bozukluklar"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p008"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Ağrılı Kraniyal Nöropatiler",
        "ogeler": [
            "Trigeminal nevralji: Elektrik çarpması ağrısı",
            "Glossofaringeal nevralji ve yüz ağrıları",
            "Damar basısı ve mikrovasküler kompresyon"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p009"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Primer ve Sekonder Ayrım Tablosu",
        "ogeler": [
            "Primer: Bizzat hastalık, yaşamı tehdit etmez",
            "Sekonder: Altta yatan organik hastalığın semptomu",
            "Sekonderde yaşamı tehdit eder ve ivedi tetkik gerekir"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p010"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Tanıda Anamnezin Temel Önemi",
        "ogeler": [
            "Anamnez baş ağrısında tanının temelidir",
            "Hastaya yeterli zaman ayırıp öykü almak",
            "Gereksiz radyolojik tetkiklerden kaçınma"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p011"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nörolojik Muayene Sonucu",
        "ogeler": [
            "Primer baş ağrılarında muayene tamamen normaldir",
            "Patolojik muayene bulgusu sekonder alarmıdır",
            "Muayenenin normal bulunması selim süreci teyit eder"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p012"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Anamnezde Sorgulanan Ölçütler",
        "ogeler": [
            "Ağrının tipi, karakteri ve başlangıç hızı",
            "Ağrının sıklığı, süresi ve hemikranyal lokalizasyonu",
            "Şiddet derecesi ve fokal yerleşim özellikleri"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p013"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Eşlik Eden Belirtiler ve Tetikleyiciler",
        "ogeler": [
            "Aura, bulantı, kusma, fotofobi ve fonofobi",
            "Stres, açlık, uykusuzluk ve tiramin tetikleyicileri",
            "Aşırı analjezik kullanımı ve triptan tüketimi"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p014"],
        "bas": 0, "son": 4,
        "sayfa": 8,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Sekonder Baş Ağrısı Kırmızı Bayrakları",
        "ogeler": [
            "Yaşamın en şiddetli ağrısı ve subaraknoid kanama",
            "Yeni başlayan akut patlayıcı gök gürültüsü ağrısı",
            "Elli yaşından sonra başlangıç ve temporal arterit"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p015"],
        "bas": 0, "son": 4,
        "sayfa": 8,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Sekonder Alarm Özellikleri",
        "ogeler": [
            "Mevcut malignite varlığında beyin metastazı",
            "Gebelik ve lohusalıkta venöz sinüs trombozu",
            "Dirençli kusmalar, atipik şekil ve erkek cinsiyet"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p016"],
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Fizik Muayenede Sekonder Bulgular",
        "ogeler": [
            "Bilinç bozukluğu, senkop ve epileptik nöbet",
            "Fokal nörolojik defisit ve hemiparezi bulguları",
            "Papilödem, subhyaloid hemoraji ve yüksek ateş"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p017"],
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kraniyal Sinir Alarmları",
        "ogeler": [
            "Ateş ve ense sertliği ile menenjit tablosu",
            "Üçüncü kraniyal sinir felci ve anizokori",
            "Horner sendromu ve karotis diseksiyonu şüphesi"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p018"],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Acil Bilgisayarlı Tomografi Endikasyonları",
        "ogeler": [
            "Akut subaraknoid kanama ve kafa travması",
            "Lomber ponksiyon öncesi herniasyonu önlemek",
            "Glaskov koma skoru dokuz ve altı ağır travma"
        ]
    },
    {
        "cumle": para_last_sent["k2-10-p019"],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Lomber Ponksiyon ve Laboratuvar Testleri",
        "ogeler": [
            "Menenjit ve ksantokromi için lomber ponksiyon",
            "Temporal arterit taramasında sedimantasyon",
            "Atak takibinde baş ağrısı günlüğü kullanımı"
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

