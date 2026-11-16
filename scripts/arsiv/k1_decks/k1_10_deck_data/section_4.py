"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 4 (Slayt 31 - 40)
Konu: Down Sendromu (Trizomi 21) Sitogenetiği, Fenotipik Spektrum, Konjenital Anomaliler ve Klinik Seyir
Checkpoint: Slayt 39 ([TEKRAR SAYFASI - CHECKPOINT 4])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_4_slides():
    return [
        # Slayt 31
        {
            "title": "Canlı Doğumla Bağdaşan Otozomal Trizomiler: Genel Bakış ve Epidemiyoloji",
            "subtitle": "Trizomi 21, Trizomi 18 ve Trizomi 13 Spektrumu",
            "badge": "Otozomal Trizomiler",
            "coreContent": {
                "text": "İnsan türünde otozomal monozomilerin tamamı mutlak embriyonik letal iken, otozomal trizomilerin de çok büyük bir kısmı fetal dönemde ölümle sonuçlanır. 22 çift otozom arasında canlı doğumla bağdaşabilen yalnızca üç tam otozomal trizomi mevcuttur: Trizomi 21 (Down sendromu), Trizomi 18 (Edwards sendromu) ve Trizomi 13 (Patau sendromu). Bu üç kromozomun canlı doğumda görülebilmesinin temel biyolojik nedeni, insan genomundaki gen yoğunluğu en düşük olan otozomlar arasında yer almalarıdır (21. kromozom en küçük otozomdur; 13 ve 18 ise gen fakiri akrosentrik ve submetasentrik kromozomlardır). Bu üç sendromun her biri ileri maternal yaş ile güçlü bir pozitif korelasyon gösterir. Canlı doğum sıklığı Down sendromunda yaklaşık 1/660-1/800, Edwards sendromunda yaklaşık 1/750-1/6000 ve Patau sendromunda yaklaşık 1/5000-1/10000'dir. Trizomi 21 dışındaki diğer iki sendromda prognoz son derece ağırdır.",
                "keyBullets": [
                    {"title": "Yaşayan Üç Trizomi", "desc": "Yalnızca Trizomi 21 (Down), Trizomi 18 (Edwards) ve Trizomi 13 (Patau) canlı doğabilir.", "isKey": True},
                    {"title": "Gen Yoğunluğu Faktörü", "desc": "13, 18 ve 21 numaralı kromozomlar genetik içerik açısından en seyrek otozomlardır.", "isKey": True},
                    {"title": "Maternal Yaş İlişkisi", "desc": "Üç sendromda da anne yaşının 35'in üzerine çıkması riski katlanarak artırır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sendrom Adı", "Kromozomal Anöploidi", "Canlı Doğum İnsidansı", "1 Yaşında Sağkalım Oranı"],
                    [
                        [("Down Sendromu", False, ""), ("Trizomi 21 (47,+21)", False, ""), ("~1/660 - 1/800 canlı doğum", True, "En sık görülen trizomi"), ("%85 - 90 (Erişkin yaşa ulaşır)", False, "")],
                        [("Edwards Sendromu", False, ""), ("Trizomi 18 (47,+18)", False, ""), ("~1/750 canlı doğum (ders slaytı)", True, "İkinci en sık trizomi"), ("%5 - 10 (%50'si ilk hafta ölür)", False, "")],
                        [("Patau Sendromu", False, ""), ("Trizomi 13 (47,+13)", False, ""), ("~1/5000 canlı doğum (ders slaytı)", True, "En nadir canlı trizomi"), ("%10'dan az (%90'ı ilk yıl ölür)", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "İnsan türünde canlı doğumla bağdaşabilen otozomal trizomiler aşağıdakilerden hangisinde eksiksiz ve doğru olarak verilmiştir?",
                    {
                        "A": "Trizomi 8, Trizomi 16, Trizomi 21",
                        "B": "Trizomi 13, Trizomi 18, Trizomi 21",
                        "C": "Trizomi 9, Trizomi 13, Trizomi 18",
                        "D": "Trizomi 14, Trizomi 21, Trizomi 22",
                        "E": "Trizomi 16, Trizomi 18, Trizomi 21"
                    },
                    "B",
                    {
                        "A": "Trizomi 16 asla canlı doğamaz.",
                        "B": "Doğru cevap B'dir: Canlı doğabilen üç tam otozomal trizomi 13 (Patau), 18 (Edwards) ve 21 (Down) sendromlarıdır.",
                        "C": "Trizomi 9 tam formda canlı doğamaz.",
                        "D": "Trizomi 14 ve 22 tam formda letaldir.",
                        "E": "Trizomi 16 canlı doğamaz."
                    }
                ),
                make_active_recall(
                    "Neden otozomal kromozomlar arasında yalnız 13, 18 ve 21 numaralı kromozomların tam trizomileri canlı doğuma ulaşabilir?",
                    "Bu kromozomlar diğer otozomlara kıyasla gen yoğunluğu (gen sayısı) en düşük olan kromozomlar olduğu için.",
                    "Gen yoğunluğu azlığı ve nispi tolerans"
                )
            ],
            "spotPearls": [
                "Canlı doğabilen otozomal trizomiler YALNIZCA 13, 18 ve 21'dir.",
                "En sık görülen ve yaşam beklentisi en uzun olan Down sendromudur (1/660).",
                "Edwards (trizomi 18) ve Patau (trizomi 13) olgularının %90'ı ilk bir yıl içinde kaybedilir."
            ]
        },

        # Slayt 32
        {
            "title": "Down Sendromu (Trizomi 21): Genel Biyoloji ve Epidemiyoloji",
            "subtitle": "Orta Derece Zihinsel Yetersizliğin En Yaygın Genetik Nedeni",
            "badge": "Down Sendromu",
            "coreContent": {
                "text": "Down sendromu (Trizomi 21), insan türünde en sık tanımlanan kromozomal hastalık ve orta dereceli zihinsel yetersizliğin tek başına en yaygın genetik nedenidir. Canlı doğumlardaki genel sıklığı yaklaşık 1/660 ila 1/800 arasındadır. Ancak trizomi 21 konsepsiyonlarının yaklaşık %75-80'i intrauterin dönemde spontan düşükle sonuçlanır; yani konsepsiyonların yalnız %20-25'i canlı doğuma ulaşabilir. Canlı doğan bebeklerin de yaklaşık dörtte biri ilk yaşını doldurmadan (özellikle konjenital kalp defektleri ve solunum yolu enfeksiyonları nedeniyle) kaybedilir. Bireylerin IQ düzeyleri genellikle 30-60 aralığında (hafif-orta mental retardasyon) seyreder. Uygun özel eğitim ve sevgi dolu bir sosyal çevreyle desteklendiklerinde iletişim becerileri yüksek, mutlu, sosyal ve yarı bağımsız bireyler olarak toplumsal yaşama başarıyla entegre olabilirler.",
                "keyBullets": [
                    {"title": "Zekâ Geriliğinde Sıklık", "desc": "Orta dereceli zihinsel engelliliğin en yaygın genetik sebebidir.", "isKey": True},
                    {"title": "Fetal Kayıp Oranı", "desc": "Trizomi 21 gebeliklerinin yaklaşık %75-80'i düşükle sonuçlanır, yalnız %20-25'i doğar.", "isKey": True},
                    {"title": "Zekâ Düzeyi", "desc": "IQ ortalaması 30-60 arasındadır; sosyal uyum ve taklit yetenekleri belirgindir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "Down sendromu genel popülasyonda orta derece zekâ geriliğinin en sık saptanan genetik nedenidir.",
                    "orta",
                    "Zihinsel yetersizlik şiddet derecesini anımsayınız"
                ),
                make_micro_quiz(
                    "Down sendromlu (Trizomi 21) fetüslerin intrauterin sağkalımı ve doğal seyri ile ilgili hangisi doğrudur?",
                    {
                        "A": "Konsepsiyonların %100'ü sorunsuz canlı doğar",
                        "B": "Trizomi 21 konsepsiyonlarının yalnız %20-25'i canlı doğuma ulaşabilir; çoğu düşükle sonlanır",
                        "C": "Asla kalp anomalisi görülmez",
                        "D": "Zekâ geriliği hiçbir zaman gelişmez",
                        "E": "Tüm bebekler ilk 24 saatte ölür"
                    },
                    "B",
                    {
                        "A": "Çoğu intrauterin dönemde elenir.",
                        "B": "Doğru cevap B'dir: Trizomi 21 gebeliklerinin yaklaşık %75-80'i spontan abortusla sonuçlanır, sadece %20-25'i doğar.",
                        "C": "Kalp anomalisi olguların en az üçte birinde görülür.",
                        "D": "Zekâ geriliği kardinal bulgudur.",
                        "E": "Down sendromlu bireyler erişkin yaşa rahatlıkla ulaşır."
                    }
                ),
                make_active_recall(
                    "Down sendromlu bireylerin bilişsel profilinde ortalama IQ seviyesi hangi aralıkta seyreder?",
                    "Genellikle 30 ile 60 arasında (hafif ila orta derece zihinsel engellilik) seyreder.",
                    "Tipik zekâ puanı ranjı"
                )
            ],
            "spotPearls": [
                "Down sendromu orta derece zihinsel yetersizliğin en sık genetik nedenidir.",
                "Trizomi 21 konsepsiyonlarının yalnız %20-25'i canlı doğuma ulaşabilir.",
                "Canlı doğum insidansı yaklaşık 1/660'tır."
            ]
        },

        # Slayt 33
        {
            "title": "Down Sendromunun Sitogenetik Tipleri: Klasik Trizomi (%95)",
            "subtitle": "Mayotik Ayrılamama ve Anne Yaşı Riski",
            "badge": "Klasik Trizomi 21",
            "coreContent": {
                "text": "Down sendromu olgularının genetik temeli incelendiğinde üç farklı sitogenetik alt tip karşımıza çıkar: Klasik serbest trizomi (%95), Robertsonian translokasyon (%4) ve Mozaisizm (%1). Olguların ezici çoğunluğunu oluşturan Klasik Trizomi 21 karyotipinde [47,XX,+21 veya 47,XY,+21], hücrelerde serbest halde ekstra bir 21. kromozom bulunur. Bu durum gametogenez sırasındaki mayotik ayrılamamadan (nondisjunction) kaynaklanır. Moleküler sitogenetik çalışmalar, fazladan 21. kromozomun yaklaşık %90-95 oranında maternal, yalnız %5-10 oranında paternal kökenli olduğunu ortaya koymuştur. Maternal hataların da yaklaşık dörtte üçü maternal Mayoz I aşamasında gerçekleşir. Klasik trizomi riski doğrudan anne yaşıyla koreledir: 20 yaşındaki bir kadında risk 1/1500 iken, 35 yaşında 1/350'ye, 40 yaşında 1/100'e ve 45 yaşında 1/30'a yükselir. Klasik trizomili çocuğu olan bir kadının sonraki gebeliğinde rekürrens riski yaklaşık %1'dir.",
                "keyBullets": [
                    {"title": "Klasik Trizomi Oranı", "desc": "Down sendromunun %95'i serbest tam trizomi 21 [47,+21] şeklindedir.", "isKey": True},
                    {"title": "Maternal Mayoz I", "desc": "Ekstra kromozomun %90'ı anneden ve çoğunlukla Mayoz I ayrılamamasından gelir.", "isKey": True},
                    {"title": "Rekürrens Riski", "desc": "Klasik trizomi sonrası sonraki gebelikte tekrarlama riski yaklaşık %1'dir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sitogenetik Tip", "Görülme Oranı", "Mekanizma", "Anne Yaşıyla İlişki"],
                    [
                        [("Klasik (Serbest) Trizomi 21", False, ""), ("%95", True, "Ezici çoğunluk payı"), ("Mayotik ayrılamama (%90 maternal)", False, ""), ("Anne yaşıyla dramatik artar", False, "")],
                        [("Robertsonian Translokasyon", False, ""), ("%4", True, "Kalıtsal potansiyelli pay"), ("Sentrik füzyon (rob(14;21) vb.)", False, ""), ("Anne yaşından tamamen BAĞIMSIZDIR", False, "")],
                        [("Mozaisizm (46/47,+21)", False, ""), ("%1", True, "En nadir varyant"), ("Post-zigotik mitotik ayrılma hatası", False, ""), ("Anne yaşıyla ilişkisizdir", False, "")]
                    ]
                ),
                make_cloze(
                    "Klasik Trizomi 21 olgularında ekstra 21. kromozom yaklaşık %90 oranında anne kaynaklıdır.",
                    "anne",
                    "Ekstra kromozomun primer ebeveyn kökenini anımsayınız"
                ),
                make_active_recall(
                    "30 yaşın altındaki bir annenin ilk çocuğu klasik trizomi 21 (serbest trizomi) doğarsa, ikinci gebelikte Down sendromu tekrarlama ampirik riski yaklaşık ne kadardır?",
                    "Yaklaşık %1 (veya %1.4) kadardır.",
                    "Klasik trizomi rekürrens riski"
                )
            ],
            "spotPearls": [
                "Down sendromunun %95'i serbest Klasik Trizomidir (47,+21).",
                "Ekstra kromozomun %90'ı anneden (özellikle Mayoz I) kaynaklanır.",
                "Klasik trizomi doğrudan anne yaşıyla artar; sonraki gebelikte risk ~%1'dir."
            ]
        },

        # Slayt 34
        {
            "title": "Down Sendromunda Translokasyon (%4) ve Mozaisizm (%1)",
            "subtitle": "Kalıtsal Risk Taşıyan Varyantlar ve Parental Karyotip Zorunluluğu",
            "badge": "Translokasyon ve Mozaik Down",
            "coreContent": {
                "text": "Down sendromu olgularının yaklaşık %4'ü Robertsonian translokasyona bağlıdır. Bu olgularda toplam kromozom sayısı normal gibi görünerek 46'dır; ancak 21. kromozomun uzun kolu başka bir akrosentrik kromozomun (en sık 14. kromozom, nadiren 22 veya 13) üzerine yapışmıştır [örneğin 46,XX,rob(14;21)(q10;q10),+21]. Çok kritik bir sınav kuralı olarak: Translokasyon tipi Down sendromu ANNE YAŞINA BAĞLI DEĞİLDİR; genç annelerde de eşit sıklıkla görülür. Translokasyonlu bebeklerin yaklaşık yarısında anomali de novo oluşurken, diğer yarısında ebeveynlerden biri dengeli taşıyıcıdır. Bu nedenle translokasyon Down saptanan her olguda ebeveynlere karyotip analizi yapılması zorunludur. Olguların %1'ini oluşturan Mozaisizmde (46/47,+21) ise döllenme sonrası erken mitozda trizomik kurtarma veya mitotik ayrılamama olmuştur; klinik bulgular ve zekâ düzeyi klasik trizomiye göre çok daha ılımlıdır.",
                "keyBullets": [
                    {"title": "Translokasyon Down (%4)", "desc": "Genellikle rob(14;21) kaynaklıdır; toplam kromozom sayısı 46'dır.", "isKey": True},
                    {"title": "Anne Yaşı Kuralı", "desc": "Translokasyon tipi Down sendromu anne yaşından tamamen BAĞIMSIZDIR.", "isKey": True},
                    {"title": "Parental Karyotip", "desc": "Translokasyon saptandığında taşıyıcılığı ekarte etmek için ebeveyn karyotipi şarttır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Klasik Trizomi vs Translokasyon Down Sendromu",
                    "Klasik Trizomi 21 (%95)",
                    "47 kromozom; ileri anne yaşı riski taşır; ebeveyn karyotipleri normaldir; tekrarlama riski düşüktür (~%1).",
                    "Translokasyon Down (%4)",
                    "46 kromozom; anne yaşından tamamen bağımsızdır; ebeveynlerden biri %50 olasılıkla dengeli taşıyıcıdır; tekrarlama riski yüksektir."
                ),
                make_micro_quiz(
                    "Translokasyon tipi Down sendromu tanısı alan bir yenidoğanın genetik yönetimi ve epidemiyolojisi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                    {
                        "A": "Yalnızca 40 yaş üstü annelerin bebeklerinde görülür",
                        "B": "Anne yaşından tamamen bağımsızdır ve ebeveynlere mutlaka karyotip analizi yapılmalıdır",
                        "C": "Karyotipinde 47 kromozom bulunur",
                        "D": "Asla bir sonraki gebeliğe aktarılamaz",
                        "E": "Down sendromu olgularının %95'ini oluşturur"
                    },
                    "B",
                    {
                        "A": "Translokasyon Down anne yaşına bağlı değildir.",
                        "B": "Doğru cevap B'dir: Translokasyon tipi anne yaşından bağımsızdır ve ebeveyn taşıyıcılığını araştırmak için ebeveyn karyotipi zorunludur.",
                        "C": "Translokasyon Downda 46 kromozom bulunur.",
                        "D": "Ebeveyn taşıyıcı ise yüksek oranda aktarılır.",
                        "E": "Olguların sadece %4'ünü oluşturur."
                    }
                ),
                make_active_recall(
                    "Down sendromlu bir bebekte sitogenetik incelemede rob(14;21) saptandığında genetik danışmanın ebeveynler için atacağı ilk adım ne olmalıdır?",
                    "Ebeveynlerin dengeli translokasyon taşıyıcısı olup olmadığını belirlemek için her iki ebeveyne periferik karyotip analizi yapmaktır.",
                    "Parental taşıyıcılık taraması"
                )
            ],
            "spotPearls": [
                "Translokasyon Down sendromu (%4) ANNE YAŞINA BAĞLI DEĞİLDİR.",
                "Translokasyon Down karyotipinde 46 kromozom bulunur.",
                "Translokasyon saptandığında ebeveynlere KARYOTİP analizi yapılması zorunludur."
            ]
        },

        # Slayt 35
        {
            "title": "Down Sendromunun Karakteristik Dismorfolojisi ve Muayene Bulguları",
            "subtitle": "Yenidoğan Döneminde Tanı Koyduran Fiziksel Stigmalar",
            "badge": "Klinik Dismorfoloji",
            "coreContent": {
                "text": "Down sendromlu bir yenidoğanda klinik tanı genellikle ilk dakikalarda tipik dismorfik stigmaların bir arada görülmesiyle konur. Doğumda en erken ve en belirgin nöromusküler bulgu genel hipotonidir ('bez bebek' manzarası); Moro refleksi zayıftır. Baş ve yüz muayenesinde: düzleşmiş oksiput, brakisefali, hafif mikrosefali ve basık burun kökü dikkati çeker. Gözlerde yukarı ve dışa doğru çekik palpebral fissürler (mongoloid çekiklik) ve iç kantal bölgede epikantal kıvrımlar (epikantus) karakteristiktir. İris stromasında küçük, beyazımsı benekler olan Brushfield lekeleri görülür. Kulaklar küçük, düşük yerleşimli ve heliksi kıvrıktır. Ağız boşluğu rölatif olarak dar olup dil belirgin derecede dışarı sarkar (dil protrüzyonu). Boyun kısa ve geniştir; ensede gevşek, kalın bir cilt kıvrımı (artmış ense pilisi) mevcuttur. Bu bulguların birçoğu prenatal ultrasonda da ipucu verir.",
                "keyBullets": [
                    {"title": "Yenidoğan Hipotonisi", "desc": "Doğumda hekimin dikkatini çeken ilk ve en kardinal nörolojik stigmattır.", "isKey": True},
                    {"title": "Kraniyofasiyal Bulgular", "desc": "Brakisefali, basık burun kökü, epikantus ve yukarı çekik gözler karakteristiktir.", "isKey": True},
                    {"title": "Ağız ve Boyun", "desc": "Dar damak, dil protrüzyonu ve ensede kalın gevşek cilt katlantısı bulunur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Anatomik Bölge", "Karakteristik Dismorfik Bulgu", "Klinik Anlamı"],
                    [
                        [("Kas Tonusu", False, ""), ("Genel infantil hipotoni", True, "Gevşek kas yapısı"), ("Yenidoğanda ilk dikkat çeken bulgu"), ],
                        [("Kranium / Oksiput", False, ""), ("Brakisefali ve düz oksiput", True, "Düz kafa arkası"), ("Tipik kafa şekli"), ],
                        [("Gözler", False, ""), ("Yukarı çekik fissürler ve epikantus", True, "Çekik göz kapağı katlantısı"), ("Mongoloid görünüm"), ],
                        [("İris", False, ""), ("Brushfield lekeleri", True, "İriste beyaz benekler"), ("İris stromasında tuz benzeri halka"), ],
                        [("Boyun", False, ""), ("Kısa boyun, kalın ense pilisi", True, "Artmış nuchal fold"), ("Prenatal USG belirteci"), ]
                    ]
                ),
                make_cloze(
                    "Down sendromlu yenidoğanda doğum odasında ilk dikkat çeken kardinal nöromusküler bulgu belirgin kas hipotonisidir.",
                    "hipotoni",
                    "Kas gevşekliğini belirten tıbbi terimi anımsayınız"
                ),
                make_active_recall(
                    "Down sendromlu bireylerin göz muayenesinde iris stromasında halka şeklinde dizilmiş küçük beyazımsı beneklere ne ad verilir?",
                    "Brushfield lekeleri (Brushfield spots) adı verilir.",
                    "İris benekleri eponimi"
                )
            ],
            "spotPearls": [
                "Yenidoğanda Down sendromunu ilk düşündüren bulgu genel HİPOTONİDİR.",
                "Brakisefali, düz oksiput, yukarı çekik gözler ve epikantus tipik yüz stigmalarıdır.",
                "İristeki beyaz lekeler Brushfield lekeleri olarak adlandırılır."
            ]
        },

        # Slayt 36
        {
            "title": "Ekstremite Bulguları: Simian Çizgisi, Klinodaktili ve Sandal Gap",
            "subtitle": "Down Sendromunun Karakteristik Periferik Fiziksel İpuçları",
            "badge": "Ekstremite Stigmaları",
            "coreContent": {
                "text": "Down sendromunda ekstremitelerin fiziksel muayenesi son derece karakteristik tanısal ipuçları barındırır. Eller geniş, parmaklar kısa ve küttür (brakidaktili). Avuç içinde normalde bulunan iki ayrı transvers fleksiyon çizgisi yerine, avucu baştan başa tek bir hat şeklinde kat eden tek transvers palmar çizgi (Simian çizgisi) olguların yaklaşık %50'sinde mevcuttur. Beşinci parmakta (küçük parmak) orta falanks hipoplazisine bağlı olarak parmağın dördüncü parmağa doğru içe kıvrılması anlamına gelen klinodaktili görülür. Ayak muayenesinde ise birinci ve ikinci ayak parmakları arasında belirgin bir açıklık ve bu aralıktan tabana doğru uzanan derin bir dikey oluk bulunur; bu görünüme 'sandal gap' (parmak arası açık sandal oluğu) adı verilir. Ayrıca eklemlerde aşırı gevşeklik (hipermobilite) ve atlantoaksiyel eklem laksisitesi diğer kritik iskelet bulgularıdır.",
                "keyBullets": [
                    {"title": "Simian Çizgisi", "desc": "Avuç içini tek bir hat olarak geçen transvers fleksör çizgidir (olguların %50'si).", "isKey": True},
                    {"title": "Klinodaktili", "desc": "5. parmak orta falanks hipoplazisine bağlı küçük parmağın içe kıvrılmasıdır.", "isKey": True},
                    {"title": "Sandal Gap", "desc": "Ayak 1. ve 2. parmakları arasındaki geniş boşluk ve tabandaki derin oluktur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Normal El/Ayak vs Down Sendromu Stigmaları",
                    "Normal Ekstremite Bulguları",
                    "Avuç içinde iki ayrı transvers çizgi; 5. parmak düz; ayak 1-2. parmakları bitişik.",
                    "Down Sendromu Ekstremite Bulguları",
                    "Tek transvers palmar çizgi (Simian çizgisi); 5. parmakta klinodaktili; ayak 1-2. parmak arası geniş (Sandal gap)."
                ),
                make_micro_quiz(
                    "Down sendromlu bir bebeğin el muayenesinde 5. parmağın orta falanks hipoplazisi nedeniyle 4. parmağa doğru eğri durması bulgusuna ne ad verilir?",
                    {
                        "A": "Sindaktili",
                        "B": "Polidaktili",
                        "C": "Klinodaktili",
                        "D": "Araknodaktili",
                        "E": "Ektrodaktili"
                    },
                    "C",
                    {
                        "A": "Sindaktili parmakların yapışık olmasıdır.",
                        "B": "Polidaktili fazla parmaktır.",
                        "C": "Doğru cevap C'dir: Beşinci parmağın içe kıvrıklığına klinodaktili denir.",
                        "D": "Araknodaktili örümcek parmaktır (Marfan).",
                        "E": "Ektrodaktili kıskaç eldir."
                    }
                ),
                make_cloze(
                    "Down sendromunda ayak 1. ve 2. parmakları arasındaki belirgin geniş boşluğa sandal gap görünümü denir.",
                    "sandal gap",
                    "Ayak başparmak aralığı terimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Simian çizgisi avuç içindeki tek transvers çizgidir (Down'da sıktır).",
                "Klinodaktili 5. parmağın içe kıvrılmasıdır.",
                "Sandal gap 1. ve 2. ayak parmakları arasındaki geniş açıklıktır."
            ]
        },

        # Slayt 37
        {
            "title": "Kardiyovasküler Anomaliler: Endokardiyal Yastık Defektleri (AVSD)",
            "subtitle": "Down Sendromunda Erken Mortalitenin Bir Numaralı Nedeni",
            "badge": "Kardiyak Malformasyonlar",
            "coreContent": {
                "text": "Down sendromlu canlı doğan bebeklerin yaklaşık %40-50'sinde (en az üçte birinde) majör bir konjenital kalp hastalığı mevcuttur. Bu kardiyovasküler malformasyonlar, Down sendromlu çocuklarda ilk yaş içindeki morbidite ve erken mortalitenin tek başına en önemli nedenidir. En karakteristik ve patognomonik kalp anomalisi, embriyonik endokardiyal yastıkların birleşme kusurundan kaynaklanan Atriyoventriküler Septal Defekttir (AVSD / Endokardiyal Yastık Defekti). AVSD olguların yaklaşık %40'ını oluşturur ve trizomi 21 ile son derece spesifik bir birliktelik gösterir. İkinci en sık kardiyak anomali Ventriküler Septal Defekttir (VSD, ~%30); bunu Atriyal Septal Defekt (ASD - ostium primum tipi, ~%15) ve Patent Duktus Arteriyozus (PDA) izler. Bu ağır sol-sağ şantlar hızla pulmoner hipertansiyona ve Eisenmenger sendromuna ilerleyebileceği için tüm Down sendromlu yenidoğanlara ilk ayda ekokardiyografi yapılmalıdır.",
                "keyBullets": [
                    {"title": "Kalp Anomalisi Sıklığı", "desc": "Canlı doğan Down sendromlu bebeklerin yaklaşık %40-50'sinde kalp defekti vardır.", "isKey": True},
                    {"title": "En Karakteristik Defekt", "desc": "Endokardiyal yastık defekti (Atriyoventriküler Septal Defekt - AVSD).", "isKey": True},
                    {"title": "Mortalite Rolü", "desc": "Erken bebeklik ölümlerinin en sık nedenidir; ilk haftalarda ekokardiyografi şarttır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Konjenital Kalp Defekti", "Down Sendromundaki Payı", "Embriyolojik / Klinik Özellik"],
                    [
                        [("AVSD (Endokardiyal Yastık Defekti)", False, ""), ("~%40 (En karakteristik)", True, "Down sendromuna en spesifik defekt"), ("Atriyum ve ventriküller arası ortak kapak", False, "")],
                        [("Ventriküler Septal Defekt (VSD)", False, ""), ("~%30 (İkinci en sık)", True, "Sık görülen şant lezyonu"), ("Membranöz veya perimembranöz defekt", False, "")],
                        [("Atriyal Septal Defekt (ASD)", False, ""), ("~%15 (Ostium primum tipi)", False, ""), ("Endokardiyal yastık parsiyel defekti", False, "")],
                        [("Fallot Tetralojisi (TOF)", False, ""), ("~%5 (Siyanotik anomali)", False, ""), ("Sağ ventrikül çıkım yolu obstrüksiyonu", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Down sendromlu yenidoğanlarda en karakteristik olarak görülen ve erken çocukluk dönemi ölümlerinin başlıca nedenini oluşturan konjenital kardiyovasküler anomali hangisidir?",
                    {
                        "A": "Biküspit aort kapağı",
                        "B": "Aort koarktasyonu",
                        "C": "Endokardiyal yastık defekti (Atriyoventriküler Septal Defekt - AVSD)",
                        "D": "Büyük arterlerin transpozisyonu",
                        "E": "Triküspit atrezisi"
                    },
                    "C",
                    {
                        "A": "Biküspit aort Turner'da sıktır.",
                        "B": "Aort koarktasyonu Turner sendromuna özgüdür.",
                        "C": "Doğru cevap C'dir: Down sendromunun en karakteristik kardiyak anomalisi AVSD'dir (endokardiyal yastık defekti).",
                        "D": "Transpozisyon diyabetik anne bebeklerinde sıktır.",
                        "E": "Triküspit atrezisi primer siyanotik nadir defekttir."
                    }
                ),
                make_cloze(
                    "Down sendromunda görülen en karakteristik kardiyak malformasyon endokardiyal yastık defekti veya atriyoventriküler septal defekttir.",
                    "endokardiyal yastık",
                    "Karakteristik embriyonik doku defektini anımsayınız"
                )
            ],
            "spotPearls": [
                "Down sendromunun en karakteristik kalp defekti ENDOKARDİYAL YASTIK DEFEKTİDİR (AVSD).",
                "Canlı doğanların %40-50'sinde kalp anomalisi vardır.",
                "Bebeklik dönemindeki erken ölümlerin en sık nedeni konjenital kalp hastalıklarıdır."
            ]
        },

        # Slayt 38
        {
            "title": "Gastrointestinal Malformasyonlar: Duodenal Atrezi ve Çift Kabarcık",
            "subtitle": "Gelişimsel Sindirim Sistemi Stenozları ve Hirschsprung Hastalığı",
            "badge": "Gastrointestinal Tutulum",
            "coreContent": {
                "text": "Down sendromlu bebeklerin yaklaşık %5-10'unda cerrahi müdahale gerektiren ciddi gastrointestinal sistem malformasyonları saptanır. Bu anomaliler arasında en klasik ve spesifik olanı duodenal atrezi veya duodenal stenozdur. Embriyonik lümen rekanalizasyon kusuru sonucu duodenumun ikinci kısmında tam tıkanıklık gelişir. Prenatal ultrasonda polihidramnios ve tipik 'çift kabarcık' (double bubble) manzarası (mide ve proksimal duodenum dilatasyonu) ile tanı alır; doğumdan hemen sonra safralı kusma ile acil cerrahi endikasyonu doğurur. Down sendromunda artış gösteren diğer önemli gastrointestinal malformasyonlar: trakeoözofageal fistül ve özofagus atrezisi, anüler pankreas, anal atrezi (imperfore anüs) ve ganglion hücrelerinin yokluğuyla giden Hirschsprung hastalığıdır (aganglionik megakolon riski Down sendromunda genel popülasyona göre 40 kat artmıştır).",
                "keyBullets": [
                    {"title": "Duodenal Atrezi", "desc": "Down sendromuna en spesifik gastrointestinal anomalidir; çift kabarcık verir.", "isKey": True},
                    {"title": "Hirschsprung Riski", "desc": "Aganglionik megakolon riski Down sendromlu bebeklerde 40 kat daha fazladır.", "isKey": True},
                    {"title": "Diğer Anomaliler", "desc": "Özofagus atrezisi, trakeoözofageal fistül ve imperfore anüs sıktır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Duodenal Atrezi ve Çift Kabarcık Gelişim Zinciri",
                    [
                        "1. Embriyogenezin 6-7. haftasında duodenumun katı kordon epitelinde vakuolizasyon ve rekanalizasyon başarısız olur",
                        "2. Duodenumun inen (ikinci) parçasında lümen tamamen kapalı (atrezik) kalır",
                        "3. Fetus amniyon sıvısını yutamaz; amniyotik kese içinde aşırı sıvı birikerek polihidramnios gelişir",
                        "4. Ayakta batın grafisinde mide ve proksimal duodenumda gaz-sıvı birikimiyle 'çift kabarcık' (double-bubble) manzarası görülür"
                    ]
                ),
                make_cloze(
                    "Down sendromlu bebeklerde radyolojik olarak mide ve duodenum dilatasyonuyla çift kabarcık manzarası veren sindirim anomalisi duodenal atrezi olarak bilinir.",
                    "duodenal atrezi",
                    "Klasik bağırsak tıkanıklığı anomalisini düşününüz"
                ),
                make_active_recall(
                    "Down sendromunda genel topluma oranla riski yaklaşık 40 kat artan ve bağırsak miyenterik pleksusunda nöronal ganglion hücrelerinin yokluğuyla karakterize hastalık nedir?",
                    "Hirschsprung hastalığı (konjenital aganglionik megakolon).",
                    "Aganglionik megakolon eponimi"
                )
            ],
            "spotPearls": [
                "Down sendromuna en spesifik gastrointestinal malformasyon DUODENAL ATREZİDİR.",
                "Duodenal atrezi radyolojide çift kabarcık (double-bubble) manzarası verir.",
                "Hirschsprung hastalığı riski Down sendromunda 40 kat artmıştır."
            ]
        },

        # Slayt 39 (CHECKPOINT 4)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Down Sendromu (Trizomi 21) Sitogenetiği ve Klinik Fenotipi",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 4",
            "coreContent": {
                "text": "Bu bölümde canlı doğan trizomilerin ve Down sendromunun temel sitogenetik ve dismorfolojik dinamiklerini özetledik. Canlı doğan 3 otozomal trizomi 13, 18 ve 21'dir. Down sendromu (1/660) orta derece zekâ geriliğinin en sık genetik nedenidir. Sitogenetik tipler: Klasik Trizomi (%95; %90 maternal kaynaklı, anne yaşıyla artar), Robertsonian Translokasyon (%4; en sık rob(14;21), anne yaşından BAĞIMSIZDIR, ebeveyn karyotipi şarttır) ve Mozaisizm (%1). Yenidoğanda ilk kardinal bulgu kas hipotonisidir. Karakteristik yüz bulguları: brakisefali, düz oksiput, epikantus, yukarı çekik gözler, Brushfield lekeleri, dil protrüzyonu ve gevşek ense pilisidir. Ekstremitelerde tek transvers palmar çizgi (Simian çizgisi), 5. parmakta klinodaktili ve ayak 1-2. parmak arasında sandal gap mevcuttur. En karakteristik kalp defekti AVSD (endokardiyal yastık defekti; bebek ölümlerinin en sık nedeni); en karakteristik GİS anomalisi ise duodenal atrezidir (çift kabarcık manzarası).",
                "keyBullets": [
                    {"title": "Sitogenetik Dağılım", "desc": "%95 Klasik Trizomi (yaşa bağlı), %4 Translokasyon (yaştan bağımsız), %1 Mozaik.", "isKey": True},
                    {"title": "Stigmalar", "desc": "Hipotoni, Simian çizgisi, klinodaktili, sandal gap, Brushfield lekeleri, epikantus.", "isKey": True},
                    {"title": "Organ Tutulumu", "desc": "Kalpte AVSD (endokardiyal yastık), sindirimde duodenal atrezi ve Hirschsprung.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Boyut", "Karakteristik Bulgu", "Patofizyolojik / Epidemiyolojik Önemi"],
                    [
                        [("Sitogenetik Dağılım", False, ""), ("%95 serbest trizomi, %4 translokasyon", True, "Yüzde oranları"), ("Translokasyon anne yaşından bağımsızdır", False, "")],
                        [("Kardinal Nöromusküler", False, ""), ("İnfantil genel hipotoni", True, "Kas gevşekliği"), ("Doğum odasında ilk fark edilen bulgu", False, "")],
                        [("Karakteristik Kalp Defekti", False, ""), ("AVSD (Endokardiyal yastık defekti)", True, "En sık malformasyon"), ("İlk yaştaki ölümlerin bir numaralı nedeni", False, "")],
                        [("Karakteristik GİS Defekti", False, ""), ("Duodenal atrezi (Çift kabarcık)", True, "Safralı kusma nedeni"), ("Rekanalizasyon duraklaması", False, "")]
                    ]
                ),
                make_cloze(
                    "Down sendromunda görülen Robertsonian translokasyon varyantı anne yaşından tamamen bağımsız olarak ortaya çıkar.",
                    "bağımsız",
                    "Anne yaşıyla ilişkisizlik durumunu anımsayınız"
                ),
                make_active_recall(
                    "Down sendromlu bir bebekte erken bebeklik döneminde mortalitenin en sık nedenini oluşturan konjenital malformasyon grubu hangisidir?",
                    "Konjenital kalp hastalıklarıdır (özellikle Atriyoventriküler Septal Defekt - AVSD).",
                    "Erken ölümün kardiyak nedeni"
                )
            ],
            "spotPearls": [
                "Down sendromu olgularının %95'i klasik serbest trizomi, %4'ü translokasyondur.",
                "Translokasyon Down sendromu anne yaşından tamamen BAĞIMSIZDIR.",
                "En karakteristik kalp anomalisi AVSD, en karakteristik GİS anomalisi duodenal atrezidir."
            ]
        },

        # Slayt 40
        {
            "title": "Uzun Dönem Riskler: Hematolojik Malignite ve Erken Evre Alzheimer",
            "subtitle": "21. Kromozom Dozajının İmmünolojik ve Nörodejeneratif Yansımaları",
            "badge": "Uzun Dönem Riskler",
            "coreContent": {
                "text": "Down sendromlu bireylerde 21. kromozom üzerindeki genlerin trizomik aşırı ekspresyonu, çocukluk ve erişkinlik döneminde çok spesifik kronik hastalıklara yatkınlık yaratır. Çocukluk çağında lösemi gelişme riski genel popülasyona kıyasla yaklaşık 10-20 kat (ders notunda 15 kat) artmıştır. Yenidoğan döneminde geçici miyeloproliferatif hastalık (TMD / geçici lösemi; GATA1 mutasyonu ile ilişkili) sık görülür; ilk 3 yaşta Akut Megakaryoblastik Lösemi (AML-M7), 3 yaşından sonra ise Akut Lenfoblastik Lösemi (ALL) riski belirgin derecede yüksektir. Diğer taraftan, 35-40 yaşından itibaren neredeyse tüm Down sendromlu bireylerin beyninde Alzheimer tipi nöropatolojik değişiklikler (senil plaklar ve nörofibriler yumaklar) birikir ve 50'li yaşlarda erken başlangıçlı demans tablosu gelişir. Bunun moleküler nedeni, Amiloid Öncül Proteini (APP) geninin 21. kromozomda (21q21.3) yer alması ve 3 kopya nedeniyle aşırı amiloid-beta birikmesidir.",
                "keyBullets": [
                    {"title": "Lösemi Riski (15 Kat)", "desc": "İlk 3 yaşta AML-M7 (megakaryoblastik), sonrasında ALL riski 15 kat artmıştır.", "isKey": True},
                    {"title": "Erken Alzheimer", "desc": "APP geni 21. kromozomdadır; gen dozajı nedeniyle 40 yaş civarında demans gelişir.", "isKey": True},
                    {"title": "Diğer Sorunlar", "desc": "Hipotiroidi, çölyak hastalığı, periodontal hastalıklar ve atlantoaksiyel instabilite sıktır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Down Sendromunda Erken Alzheimer Gelişim Zinciri",
                    [
                        "1. 21. kromozomun uzun kolunda yer alan Amiloid Öncül Proteini (APP) geni 3 kopya olarak bulunur",
                        "2. Hücrelerde APP proteini sürekli olarak %150 oranında aşırı sentezlenir",
                        "3. Gama ve beta sekretazlarca kesilen APP, nörotoksik Amiloid-beta (A-beta 42) oligomerlerini artırır",
                        "4. 40'lı yaşlarda serebral kortekste yaygın senil plaklar birikerek erken evre Alzheimer demansı gelişir"
                    ]
                ),
                make_micro_quiz(
                    "Down sendromlu bireylerde genel popülasyona göre çocukluk çağında lösemi gelişme riski yaklaşık kaç kat artmıştır?",
                    {
                        "A": "2 kat",
                        "B": "5 kat",
                        "C": "15 kat",
                        "D": "50 kat",
                        "E": "100 kat"
                    },
                    "C",
                    {
                        "A": "Çok düşüktür.",
                        "B": "Yetersiz orandır.",
                        "C": "Doğru cevap C'dir: Down sendromlu çocuklarda lösemi riski yaklaşık 15 kat (10-20 kat) artmıştır.",
                        "D": "Gerçek değerden yüksektir.",
                        "E": "Aşırı yüksektir."
                    }
                ),
                make_cloze(
                    "Down sendromunda erken yaşta Alzheimer hastalığı gelişmesinin temel moleküler nedeni Amiloid Öncül Proteini (APP) geninin 21. kromozomda yer almasıdır.",
                    "APP",
                    "Amiloid öncül proteini gen kısaltmasını yazınız"
                )
            ],
            "spotPearls": [
                "Down sendromunda çocukluk çağı lösemi riski 15 kat artmıştır.",
                "İlk 3 yaşta AML-M7 (akut megakaryoblastik lösemi), sonra ALL sıktır.",
                "APP geninin 21. kromozomda bulunması nedeniyle 40 yaş üstünde erken Alzheimer gelişir."
            ]
        }
    ]
