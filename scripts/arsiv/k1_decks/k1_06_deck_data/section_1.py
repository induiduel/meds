"""
Bölüm 1: Anne Sağlığı Kavramı, Küresel Göstergeler ve DSÖ Anne Ölüm Verileri
Adımlar: 1 - 10
Checkpoint: Adım 9 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # ADIM 1
    slides.append({
        "slideNumber": 1,
        "title": "Anne Sağlığı Kavramı ve Yaşam Boyu Perspektif",
        "subtitle": "Hamilelik, doğum ve puerperium döneminde optimal iyilik hali",
        "badge": "Anne Sağlığı",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Anne sağlığı, kadının hamilelik, doğum eylemi ve doğum sonrası lohusalık (puerperium) dönemlerindeki "
            "fiziksel, ruhsal ve sosyal iyilik halinin bütünüdür. Dünya Sağlık Örgütü (DSÖ), anne sağlığını yalnızca "
            "hastalık veya sakatlığın bulunmayışı olarak değil, gebelik ve doğum sürecinin her aşamasında kadının ve "
            "bebeğinin tam biyolojik ve psikososyal potansiyeline ulaşmasını sağlayan olumlu ve güçlendirici bir deneyim "
            "olarak tanımlar.\n\n"
            "> [SINAV SPOTU] Anne sağlığı yalnızca anne mortalitesini sıfırlamayı değil; gebelik, doğum ve puerperium "
            "sürecinde kadının ve fetüsün optimal sağlık düzeyini korumayı amaçlar.\n\n"
            "Maternal mortalite ve morbidite oranları, bir ülkenin sosyoekonomik kalkınmışlık seviyesinin, kadın haklarının "
            "ve sağlık sistemi kalitesinin en hassas barometresidir. Destekleyici bir ortamda çalışan vasıflı bir sağlık "
            "profesyonelinin zamanında müdahalesi ile anne ölümlerinin çok büyük bir kısmı önlenebilir niteliktedir."
        ),
        "medicalTerms": [
            {"term": "Anne Sağlığı (Maternal Health)", "explanation": "Gebelik, doğum ve lohusalık dönemlerinde kadının fiziksel, zihinsel ve sosyal tam iyilik halidir."},
            {"term": "Puerperium (Lohusalık)", "explanation": "Doğumu takip eden ve maternal üreme organlarının gebelik öncesi durumuna döndüğü yaklaşık 6 haftalık dönemdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne sağlığı; hamilelik, doğum ve puerperium evrelerinin tamamını kapsayan bütüncül bir halk sağlığı disiplinidir.",
            "📌 [SINAV SPOTU] Anne ölümlerinin çok büyük bölümü vasıflı sağlık personeli gözetiminde tamamen önlenebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bütüncül Kapsam", "desc": "Gebelik, doğum ve puerperium olmak üzere üç temel evreyi içerir.", "isKey": True},
                {"title": "Gelişmişlik Barometresi", "desc": "Maternal göstergeler bir toplumun sağlık ve refah düzeyinin en net aynasıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Anne sağlığı hamilelik, doğum ve puerperium evrelerinde kadının tam iyilik halini temsil eder.",
                "puerperium",
                "Doğum sonrası lohusalık süreci"
            ),
            make_active_recall(
                "Anne sağlığı hangi üç temel dönemi kapsar ve neden toplumların sağlık barometresi sayılır?",
                "Gebelik, doğum ve doğum sonrası lohusalık (puerperium) dönemlerini kapsar; sağlık hizmetlerine erişim, sosyoekonomik eşitlik ve koruyucu sağlık kalitesini doğrudan yansıtır."
            )
        ]
    })

    # ADIM 2
    slides.append({
        "slideNumber": 2,
        "title": "Anne Ölüm Oranı (MMR) Tanımı ve Epidemiyolojik Önemi",
        "subtitle": "100.000 canlı doğum başına düşen anne ölümü sayısı ve hesaplama tekniği",
        "badge": "Epidemiyoloji",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Anne Ölüm Oranı (Maternal Mortality Ratio - MMR), bir toplumda anne sağlığı düzeyini değerlendirmede kullanılan "
            "uluslararası altın standart epidemiyolojik göstergedir. MMR formülü; belirli bir coğrafyada ve yılda gebelik, "
            "doğum veya doğum sonu 42 gün içerisinde gelişen maternal nedenli ölüm sayısının, aynı dönemdeki canlı doğum sayısına "
            "bölünüp 100.000 katsayısı ile çarpılmasıyla hesaplanır.\n\n"
            "> [SINAV SPOTU] Anne Ölüm Oranı (MMR) paydada canlı doğum sayısını alır ve 100.000 canlı doğum başına hesaplanır; "
            "Anne Ölüm Hızı (Maternal Mortality Rate) ise paydada doğurgan çağdaki kadın nüfusunu kullanır.\n\n"
            "MMR'nin paydasında toplam kadın nüfusu değil, doğrudan gebelik riskiyle karşılaşmış olan canlı doğum sayısı "
            "kullanıldığı için, doğurganlık düzeyindeki dalgalanmalardan etkilenmeksizin sağlık sisteminin obstetrik bakım "
            "yetkinliğini net olarak ortaya koyar."
        ),
        "medicalTerms": [
            {"term": "Anne Ölüm Oranı (MMR)", "explanation": "Belirli bir yılda 100.000 canlı doğuma düşen maternal ölüm sayısıdır."},
            {"term": "Maternal Ölüm", "explanation": "Gebelik sırasında veya gebeliğin sonlanmasından sonraki 42 gün içinde, kaza harici gebelik veya yönetiminden kaynaklanan ölümdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne Ölüm Oranı (MMR) paydasında 100.000 canlı doğum kullanılır.",
            "📌 [SINAV SPOTU] Maternal ölüm süresi gebelik boyu ve gebeliğin sonlanmasını izleyen 42 günlük süredir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "MMR Katsayısı", "desc": "Uluslararası kabul gören çarpan 100.000 canlı doğumdur.", "isKey": True},
                {"title": "42 Gün Sınırı", "desc": "Doğumdan sonraki ilk 42 günde gerçekleşen obstetrik ölümler dahil edilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Anne Ölüm Oranı hesaplanırken paydada canlı doğum sayısı kullanılır ve sonuç 100.000 ile çarpılır.",
                "canlı doğum",
                "Formülün paydasındaki demografik veri"
            ),
            make_active_recall(
                "Anne Ölüm Oranı (MMR) ile Anne Ölüm Hızı arasındaki en temel metodolojik fark nedir?",
                "MMR paydasında canlı doğum sayısını (100.000 katsayısıyla) kullanırken, Anne Ölüm Hızı 15-49 yaş doğurgan çağ kadın nüfusunu (genellikle 1.000 katsayısıyla) kullanır."
            )
        ]
    })

    # ADIM 3
    slides.append({
        "slideNumber": 3,
        "title": "DSÖ 2020 Küresel Anne Ölüm Verileri ve Bilanço",
        "subtitle": "287.000 yıllık kayıp ve her iki dakikada bir yaşanan önlenebilir trajedi",
        "badge": "DSÖ Verileri",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü'nün (DSÖ) 2020 yılı küresel raporuna göre, dünya genelinde gebelik ve doğuma bağlı komplikasyonlar "
            "nedeniyle yaklaşık 287.000 kadın yaşamını yitirmiştir. Bu istatistik, her gün yaklaşık 800 kadının veya neredeyse her "
            "iki dakikada bir annenin önlenebilir nedenlerle hayatını kaybettiği anlamına gelmektedir.\n\n"
            "> [SINAV SPOTU] 2020 DSÖ verilerine göre yıllık maternal kayıp yaklaşık 287.000 olup, günlük önlenebilir ölüm "
            "sayısı yaklaşık 800'dür (her 2 dakikada bir kadın).\n\n"
            "Bu ölümlerin çok büyük bir kısmının modern obstetrik bakım, acil kan transfüzyonu ve antibiyotik tedavisi gibi temel "
            "müdahalelerle tamamen engellenebilir olması, küresel ölçekte acil bir halk sağlığı müdahalesi gerektirmektedir."
        ),
        "medicalTerms": [
            {"term": "Önlenebilir Anne Ölümü", "explanation": "Vasıflı personel, zamanında sevk ve acil obstetrik bakım ile engellenmesi mümkün olan ölümlerdir."},
            {"term": "Sürdürülebilir Kalkınma Amaçları (SKA)", "explanation": "DSÖ ve BM'nin 2030 yılına kadar küresel MMR'yi 70'in altına indirmeyi hedefleyen küresel planıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 2020 yılında gebelik ve doğuma bağlı ölen kadın sayısı yaklaşık 287.000'dir.",
            "📌 [SINAV SPOTU] Günlük önlenebilir anne ölümü yaklaşık 800 olup neredeyse her 2 dakikada bir ölüme karşılık gelir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "287.000 Anne Kaybı", "desc": "2020 yılı küresel yıllık toplam anne ölümü bilançosudur.", "isKey": True},
                {"title": "Günde 800 Ölüm", "desc": "Neredeyse her iki dakikada bir anne önlenebilir sebeplerle ölmektedir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "DSÖ 2020 verilerine göre dünyada yılda yaklaşık 287.000 kadın gebelik ve doğum komplikasyonları nedeniyle ölmektedir.",
                "287.000",
                "Küresel yıllık anne kaybı sayısı"
            ),
            make_active_recall(
                "DSÖ verilerine göre 2020 yılında her gün ortalama kaç anne hayatını kaybetmiştir?",
                "Her gün yaklaşık 800 kadın önlenebilir gebelik ve doğum komplikasyonları nedeniyle hayatını kaybetmiştir (neredeyse her 2 dakikada bir ölüm)."
            )
        ]
    })

    # ADIM 4
    slides.append({
        "slideNumber": 4,
        "title": "Küresel Eğilim: 2000-2020 Arası MMR Değişimi",
        "subtitle": "20 yıllık süreçte sağlanan %34'lük düşüş ve kazanımların korunması",
        "badge": "Zaman Serisi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "2000 ile 2020 yılları arasındaki yirmi yıllık dönemde dünya genelinde anne sağlığı alanında önemli adımlar atılmıştır. "
            "Milenyum Kalkınma Hedefleri ve ardından gelen Sürdürülebilir Kalkınma Amaçları doğrultusunda yürütülen küresel kampanyalar "
            "sayesinde küresel Anne Ölüm Oranında (MMR) yaklaşık %34'lük bir düşüş kaydedilmiştir.\n\n"
            "> [SINAV SPOTU] 2000-2020 yılları arasında küresel MMR yaklaşık %34 oranında gerilemiştir; ancak son yıllarda bu düşüş "
            "hızı yavaşlamış ve bazı bölgelerde duraklama noktasına gelmiştir.\n\n"
            "Bu gerileme sevindirici olmakla birlikte, hedeflenen yıllık %6,4'lük azalma hızının oldukça gerisinde kalınmıştır. "
            "Doğum öncesi bakımın yaygınlaşması, kurumsal doğumların artması ve acil obstetrik hizmetlerin kırsal bölgelere ulaştırılması "
            "bu kazanımın temel lokomotifleri olmuştur."
        ),
        "medicalTerms": [
            {"term": "Kurumsal Doğum", "explanation": "Doğumun donanımlı bir sağlık kuruluşunda ve ehil sağlık personeli eşliğinde gerçekleştirilmesidir."},
            {"term": "Temel Acil Obstetrik Bakım (BEmONC)", "explanation": "Parenteral antibiyotik, oksitosik ve manuel plasenta çıkarılması gibi hayat kurtarıcı paket hizmettir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 2000-2020 yılları arasında küresel MMR düşüşü yaklaşık %34'tür.",
            "📌 [SINAV SPOTU] İlerlemenin sürmesi için kurumsal doğum ve vasıflı ebe desteği vazgeçilmezdir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "%34 Küresel Düşüş", "desc": "2000-2020 arasında kaydedilen toplam düşüş oranıdır.", "isKey": True},
                {"title": "Yetersiz Hız", "desc": "Mevcut düşüş ivmesi 2030 SKA hedeflerine ulaşmak için hızlandırılmalıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dünya genelinde 2000-2020 yılları arasında anne ölüm oranında yaklaşık yüzde 34 oranında düşüş kaydedilmiştir.",
                "yüzde 34",
                "Yirmi yıllık süreçteki küresel düşüş yüzdesi"
            ),
            make_active_recall(
                "2000-2020 yılları arasında küresel MMR oranında ne kadarlık bir düşüş sağlanmıştır?",
                "Yaklaşık %34 oranında bir düşüş sağlanmıştır; bu gelişme kurumsal doğumların ve vasıflı ebelik hizmetlerinin artışına bağlıdır."
            )
        ]
    })

    # ADIM 5
    slides.append({
        "slideNumber": 5,
        "title": "Bölgesel Eşitsizlikler ve Düşük-Orta Gelirli Ülkeler",
        "subtitle": "Ölümlerin %95'inin yoğunlaştığı dezavantajlı coğrafyalar",
        "badge": "Sağlıkta Adalet",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Anne ölümleri dünya üzerinde son derece adaletsiz bir coğrafi dağılım sergilemektedir. 2020 yılında kaydedilen tüm anne "
            "ölümlerinin neredeyse %95'i düşük ve alt-orta gelirli ülkelerde meydana gelmiştir. Bu ölümlerin yarısından fazlası ise "
            "yalnızca Sahra Altı Afrika ve Güney Asya bölgelerinde yoğunlaşmaktadır.\n\n"
            "> [SINAV SPOTU] Küresel anne ölümlerinin yaklaşık %95'i düşük ve alt-orta gelirli ülkelerde gerçekleşmektedir.\n\n"
            "Gelişmiş ülkelerde bir kadının yaşam boyu anne ölüm riski 5.400'de 1 iken, düşük gelirli bazı ülkelerde bu risk 45'te 1 gibi "
            "korkutucu düzeylere tırmanmaktadır. Bu derin uçurum, anne sağlığının doğrudan bir küresel sosyal adalet ve kaynak dağılımı "
            "sorunu olduğunu kanıtlamaktadır."
        ),
        "medicalTerms": [
            {"term": "Sağlıkta Eşitsizlik (Health Disparity)", "explanation": "Sosyoekonomik, coğrafi veya ırksal faktörlere bağlı olarak önlenebilir sağlık çıktılarındaki haksız uçurumlardır."},
            {"term": "Yaşam Boyu Anne Ölüm Riski", "explanation": "15 yaşındaki bir kadının doğurganlık yaşamı boyunca maternal nedenle hayatını kaybetme olasılığıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 2020 yılı anne ölümlerinin yaklaşık %95'i düşük ve orta gelirli ülkelerde toplanmıştır.",
            "📌 [SINAV SPOTU] Sahra Altı Afrika tek başına küresel anne ölümlerinin yaklaşık üçte ikisini barındırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "%95 Yığılma", "desc": "Ölümlerin neredeyse tamamı düşük ve orta gelirli ülkelerdedir.", "isKey": True},
                {"title": "Kaynak Yetersizliği", "desc": "Ulaşım güçlüğü, donanımsız hastaneler ve sağlık personeli azlığı temel etkendir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dünyadaki toplam anne ölümlerinin neredeyse yüzde 95 kadarı düşük ve alt-orta gelirli ülkelerde yoğunlaşmaktadır.",
                "yüzde 95",
                "Ölümlerin yığıldığı gelir grubunun yüzdesi"
            ),
            make_active_recall(
                "Anne ölümlerinin düşük ve orta gelirli ülkelerde %95 oranında yığılmasının altında yatan temel sistemik aksaklıklar nelerdir?",
                "Vasıflı doğum personeli eksikliği, acil obstetrik bakım ve kan bankası yetersizliği, ulaşım engelleri ve kırsal sağlık altyapısının zayıflığıdır."
            )
        ]
    })

    # ADIM 6
    slides.append({
        "slideNumber": 6,
        "title": "Adolesan Gebelikler: 15-19 Yaş Grubunun Risk Profili",
        "subtitle": "Yılda 21 milyon gebelik ve biyopsikososyal kırılganlık",
        "badge": "Adolesan Sağlığı",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Düşük ve orta gelirli ülkelerde 15-19 yaş arasındaki adölesan kızlarda yılda tahminen 21 milyon gebelik gerçekleşmektedir. "
            "Bu gebeliklerin yaklaşık %50'si plansız veya istenmeyen gebelik niteliğinde olup, yaklaşık 12 milyonu doğumla sonuçlanmaktadır.\n\n"
            "> [SINAV SPOTU] Adolesan anneler (10-19 yaş), 20-24 yaş grubundaki erişkin kadınlara kıyasla eklampsi, puerperal "
            "endometrit ve sistemik enfeksiyon açısından belirgin derecede yüksek risk taşır.\n\n"
            "Adolesan dönemde biyolojik pelvik kemik çatısı henüz gelişimini tamamlamadığı için sefalopelvik disproporsiyon (çatı darlığı) "
            "ve buna bağlı uzamış doğum eylemi ile obstetrik fistül riski dramatik şekilde artar. Aynı zamanda yenidoğanlarda düşük doğum "
            "ağırlığı ve prematürite sıktır."
        ),
        "medicalTerms": [
            {"term": "Adolesan Gebelik", "explanation": "Dünya Sağlık Örgütü tanımına göre 10-19 yaş aralığında gerçekleşen gebeliklerdir."},
            {"term": "Sefalopelvik Disproporsiyon (CPD)", "explanation": "Fetal baş çapı ile maternal doğum kanalı kemik çatısı arasındaki uyumsuzluktur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Adolesan gebeliklerde eklampsi, sistemik enfeksiyon ve puerperal endometrit riski katbekat yüksektir.",
            "📌 [SINAV SPOTU] Adolesan annelerin bebeklerinde düşük doğum ağırlığı (<2500 g) ve preterm doğum riski belirgin artar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "21 Milyon Gebelik", "desc": "Düşük-orta gelirli ülkelerde her yıl kaydedilen adölesan gebelik sayısıdır.", "isKey": True},
                {"title": "Yüksek Komplikasyon", "desc": "Eklampsi, uzamış travay ve lohusalık enfeksiyonları belirgin sıktır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Adolesan gebeliklerde maternal kemik çatısı olgunlaşmadığı için sefalopelvik disproporsiyon ve obstrüktif doğum riski yüksektir.",
                "sefalopelvik disproporsiyon",
                "Baş-leğen kemiği kemik darlığı uyumsuzluğu"
            ),
            make_active_recall(
                "Adolesan gebelerde (10-19 yaş) 20-24 yaş erişkin gebelere kıyasla en sık artış gösteren üç maternal komplikasyon nedir?",
                "Eklampsi (konvülsiyonlu gebelik zehirlenmesi), puerperal endometrit ve ağır sistemik enfeksiyonlardır."
            )
        ]
    })

    # ADIM 7
    slides.append({
        "slideNumber": 7,
        "title": "Erken Adolesan Dönem (10-14 Yaş) ve Uç Riskler",
        "subtitle": "Biyolojik olgunlaşmamışlık ve en yüksek mortalite grubu",
        "badge": "Kritik Risk",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Adolesan yaş dilimi içerisinde 10-14 yaş grubu (genç adolesanlar), obstetrik komplikasyonlar ve anne ölümü açısından "
            "tüm yaş grupları içerisindeki en kırılgan ve en yüksek riskli popülasyonu oluşturur. Bu grupta jinekolojik yaş "
            "(menarştan itibaren geçen süre) çok kısa olduğundan, üreme sistemi ve endokrin eksen tam olgunlaşmamıştır.\n\n"
            "> [KRİTİK UYARI] 10-14 yaş grubundaki genç adölesanlarda maternal mortalite ve kalıcı morbidite riski, 15-19 yaş grubundan "
            "bile çok daha dramatik düzeydedir.\n\n"
            "Bu kız çocuklarında pelvis henüz dar olduğu için obstrüktif (tıkalı) doğum eylemi kaçınılmaz hale gelir. Zamanında cerrahi "
            "ulaşımı olmayan kırsal bölgelerde bu durum doku nekrozuna, vezikovajinal veya rektovajinal obstetrik fistüllere ve "
            "ağır sepsis tablolarına yol açmaktadır."
        ),
        "medicalTerms": [
            {"term": "Jinekolojik Yaş", "explanation": "Kronolojik yaştan bağımsız olarak menarş (ilk adet) ile gebelik arasındaki süredir; <2 yıl yüksek risktir."},
            {"term": "Obstetrik Fistül", "explanation": "Tıkalı doğum eyleminde baş basısına bağlı iskemi sonucu mesane/rektum ile vajina arasında anormal kanal açılmasıdır."}
        ],
        "spotPearls": [
            "📌 [KRİTİK UYARI] 10-14 yaş grubu kızlarda anne ölüm riski diğer tüm adolesan dilimlerinden belirgin şekilde yüksektir.",
            "📌 [SINAV SPOTU] Tıkalı doğum ve buna bağlı obstetrik fistül gelişimi erken adölesanlarda en yıkıcı komplikasyondur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "En Kırılgan Grup", "desc": "10-14 yaş grubu biyolojik ve anatomik olarak gebeliğe hazır değildir.", "isKey": True},
                {"title": "Obstetrik Fistül", "desc": "Uzayan baş basısı kalıcı idrar ve gaita inkontinansına yol açar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Genç adölesanlarda tıkalı doğum eylemi sonucu gelişen doku nekrozu obstetrik fistül oluşumuna zemin hazırlar.",
                "obstetrik fistül",
                "Mesane ile vajina arasındaki patolojik kanal"
            ),
            make_active_recall(
                "10-14 yaş grubunda gebeliğin maternal açıdan en ölümcül olmasının anatomik ve fizyolojik gerekçeleri nelerdir?",
                "Pelvis kemik yapısının henüz dar olması, jinekolojik yaşın 2 yıldan kısa olması, hormonal dengesizlik ve doku direncinin yetersizliğidir."
            )
        ]
    })

    # ADIM 8
    slides.append({
        "slideNumber": 8,
        "title": "Türkiye Epidemiyolojisi: Adolesan Doğurganlık Hızında Büyük Başarı",
        "subtitle": "2001'de binde 49'dan 2023'te binde 11'e uzanan düşüş çizgisi",
        "badge": "TÜİK Verisi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Türkiye İstatistik Kurumu (TÜİK) ve Sağlık Bakanlığı resmi verileri, ülkemizin anne ve çocuk sağlığı alanındaki kararlı "
            "politikalarının son yirmi yılda çok somut bir halk sağlığı başarısına dönüştüğünü göstermektedir. 15-19 yaş grubunda "
            "bin kadın başına düşen canlı doğum sayısı olarak tanımlanan 'Adolesan Doğurganlık Hızı', Türkiye'de 2001 yılında binde 49 iken, "
            "2023 yılı itibarıyla binde 11 düzeyine gerilemiştir.\n\n"
            "> [SINAV SPOTU] Türkiye'de TÜİK verilerine göre adölesan doğurganlık hızı 2001'de binde 49 iken, 2023 yılında "
            "binde 11'e düşürülmüştür.\n\n"
            "Bu belirgin başarı; kız çocuklarının eğitime katılımının artması, temel sağlık hizmetlerinin ve aile planlaması "
            "danışmanlığının yaygınlaştırılması ve erken yaşta evliliklerle mücadele eden yasal düzenlemelerin hayata geçirilmesiyle sağlanmıştır."
        ),
        "medicalTerms": [
            {"term": "Adolesan Doğurganlık Hızı", "explanation": "15-19 yaş grubundaki 1.000 kadın başına düşen yıllık canlı doğum sayısıdır."},
            {"term": "Birinci Basamak Sağlık Hizmetleri", "explanation": "Aile hekimliği birimlerince sunulan koruyucu, izlem ve danışmanlık hizmetlerinin bütünüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Türkiye'de 15-19 yaş adolesan doğurganlık hızı 2001'de binde 49 iken 2023'te binde 11'e gerilemiştir.",
            "📌 [SINAV SPOTU] Bu gösterge Türkiye'nin anne-çocuk sağlığında katettiği mesafenin en güçlü delilidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "2001: Binde 49", "desc": "Yüzyılın başında Türkiye'deki adölesan doğurganlık hızı seviyesidir.", "isKey": True},
                {"title": "2023: Binde 11", "desc": "Son TÜİK verilerine göre ulaşılan başarılı halk sağlığı seviyesidir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Türkiye'de TÜİK verilerine göre 15-19 yaş adolesan doğurganlık hızı 2023 yılında binde 11 seviyesine düşmüştür.",
                "binde 11",
                "2023 yılı TÜİK adolesan doğurganlık değeri"
            ),
            make_active_recall(
                "Türkiye'de adolesan doğurganlık hızının 2001-2023 yılları arasındaki değişimi nasıldır ve hangi politikalar etkilidir?",
                "Binde 49'dan binde 11'e gerilemiştir; kız çocuklarının eğitime erişimi, birinci basamak aile sağlığı merkezlerinin izlem gücü ve erken evliliklerin önlenmesi etkilidir."
            )
        ]
    })

    # ADIM 9 [CHECKPOINT 1]
    slides.append({
        "slideNumber": 9,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Anne Sağlığı ve Küresel Göstergeler İstasyonu",
        "subtitle": "İlk 8 adımın kritik halk sağlığı verilerini ve epidemiyolojik göstergelerini pekiştirme",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 1,
        "synthesisNarrative": (
            "Bu istasyon, ilk 8 adımda incelenen Anne Sağlığı kavramını, Anne Ölüm Oranı (MMR) hesaplama mantığını, DSÖ'nün 2020 küresel "
            "bilançosunu (yıllık 287.000 ölüm, günde 800 kayıp), düşük-orta gelirli ülkelerdeki %95'lik trajik yığılmayı, adölesan "
            "gebeliklerin (15-19 yaş ve uç riskli 10-14 yaş) komplikasyon yükünü ve Türkiye'nin 2001'den 2023'e adölesan doğurganlık hızını "
            "binde 49'dan binde 11'e indirme başarısını sentezlemektedir.\n\n"
            "> [YÜKSEK VERİM] MMR paydada daima 100.000 canlı doğumu kullanır. Ölümlerin %95'i kaynak kısıtlı ülkelerdedir. 10-14 yaş "
            "adölesanlar biyolojik immatürite nedeniyle en yüksek ölüm riski altındadır. Türkiye'de adölesan doğurganlık hızı binde 11'dir."
        ),
        "medicalTerms": [
            {"term": "MMR Paydası", "explanation": "100.000 canlı doğum esasına dayanır, nüfusu değil riske giren olayı baz alır."},
            {"term": "Adolesan Komplikasyon Triadı", "explanation": "Eklampsi, sistemik enfeksiyon/endometrit ve tıkalı travaya bağlı fistüldür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne Ölüm Oranı (MMR): 100.000 canlı doğumda anne ölümü sayısıdır.",
            "📌 [SINAV SPOTU] 2020 DSÖ: Yılda 287.000 anne ölümü, günde ~800 ölüm, %95'i düşük-orta gelirli ülkelerde.",
            "📌 [SINAV SPOTU] Türkiye TÜİK 2023: 15-19 yaş adölesan doğurganlık hızı binde 11."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "MMR Standardı", "desc": "100.000 canlı doğum başına hesaplanan altın standart göstergedir.", "isKey": True},
                {"title": "Adolesan Risk", "desc": "Eklampsi ve obstrüktif travay riski adölesanlarda pik yapar.", "isKey": True},
                {"title": "Türkiye Düzeyi", "desc": "Adolesan doğurganlık hızı binde 11 seviyesine indirilmiştir.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-01",
                "Anne Ölüm Oranı (MMR) formülünde pay ve paydada hangi veriler yer alır ve katsayı kaçtır?",
                "Pay: Belirli yıldaki maternal ölüm sayısı (gebelik + lohusalık 42 gün).\nPayda: Aynı yıldaki canlı doğum sayısı.\nKatsayı: 100.000.",
                "100.000 canlı doğum esası"
            ),
            make_flashcard(
                "fc-k1-06-02",
                "DSÖ 2020 verilerine göre dünyada yılda ve günde kaç kadın anne ölümü nedeniyle kaybedilmektedir?",
                "Yılda yaklaşık 287.000 kadın; günde yaklaşık 800 kadın (neredeyse her 2 dakikada bir önlenebilir ölüm).",
                "Yıllık 287.000 bilançosu"
            ),
            make_flashcard(
                "fc-k1-06-03",
                "Türkiye'de 15-19 yaş adölesan doğurganlık hızının 2001 ve 2023 yılı TÜİK değerleri nelerdir?",
                "2001 yılında binde 49 iken, 2023 yılı itibarıyla binde 11 düzeyine gerilemiştir.",
                "49'dan 11'e düşüş"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Gösterge / Parametre", "Küresel Değer (DSÖ)", "Türkiye Düzeyi (TÜİK)"],
                [
                    [("Yıllık Anne Ölümü", False, ""), ("Yaklaşık 287.000 kadın", True, "Küresel yıllık maternal ölüm sayısı"), ("Gelişmiş ülke seviyesine yakın düşüş", False, "")],
                    [("Ölümlerin Gelir Grubu Dağılımı", False, ""), ("Yüzde 95 düşük ve orta gelirli ülkelerde", True, "Yoksul ülkelerdeki yığılma yüzdesi"), ("Hastanede doğum oranı yüzde 99 üstü", False, "")],
                    [("Adolesan Doğurganlık Hızı", False, ""), ("Dünya genelinde binde 40 civarı", False, ""), ("2023 itibarıyla binde 11", True, "Türkiye'nin güncel adölesan doğum hızı")]
                ]
            )
        ]
    })

    # ADIM 10
    slides.append({
        "slideNumber": 10,
        "title": "Vasıflı Doğum Personelinin Hayat Kurtarıcı Rolü",
        "subtitle": "Ebe, hekim ve obstetrik ekiplerin zamanında müdahale gücü",
        "badge": "Sağlık İş Gücü",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Dünya Sağlık Örgütü verileri ve uluslararası halk sağlığı kanıtları, anne ölümlerinin ezici çoğunluğunun destekleyici "
            "bir sağlık sisteminde görev yapan 'vasıflı bir sağlık profesyoneli' (eğitimli ebe, hekim veya kadın doğum uzmanı) "
            "tarafından zamanında yapılacak temel müdahalelerle tamamen önlenebileceğini tartışmasız şekilde ortaya koymaktadır.\n\n"
            "> [SINAV SPOTU] Anne ölümlerini azaltmada en maliyet-etkili ve kanıtlanmış tekil müdahale, her doğuma eğitimli "
            "ve vasıflı bir sağlık personelinin (özellikle ebe veya hekim) eşlik etmesidir.\n\n"
            "Vasıflı personelin varlığı; doğum sonu kanamanın ilk 10 dakikada oksitosinle durdurulmasını, preeklamptik konvülsiyonun "
            "magnezyum sülfat ile önlenmesini, steril koşullarla puerperal enfeksiyonların engellenmesini ve tıkalı travayın acil sezaryenle "
            "çözümlenmesini sağlayarak anneyi yaşama bağlar."
        ),
        "medicalTerms": [
            {"term": "Vasıflı Doğum Personeli (Skilled Birth Attendant)", "explanation": "Normal gebelik, doğum ve lohusalık sürecini yönetebilen, komplikasyonları tanıyıp sevk eden lisanslı sağlık çalışanıdır."},
            {"term": "Aktif Üçüncü Evre Yönetimi (AMTSL)", "explanation": "Doğum sonu kanamayı %60 azaltan rutin profilaktik uterotonik ve kontrollü kord traksiyonu uygulamasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne ölümlerinin önlenmesinde en kritik basamak vasıflı doğum personeli eşliğinde kurumsal doğumdur.",
            "📌 [SINAV SPOTU] Doğumun üçüncü evresinde profilaktik uterotonik kullanımı postpartum kanamayı dramatik şekilde önler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Vasıflı Ebe Gücü", "desc": "Doğum komplikasyonlarının %80'den fazlası ehil ebelerce önlenebilir.", "isKey": True},
                {"title": "Zamanında Sevk", "desc": "Gerekli cerrahi veya yoğun bakım ihtiyacını ilk anda saptamak hayat kurtarır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Doğumun üçüncü evresinde rutin uygulanan aktif üçüncü evre yönetimi maternal postpartum kanama oranını belirgin azaltır.",
                "aktif üçüncü evre yönetimi",
                "Oksitosin ile plasenta yönetim protokolü"
            ),
            make_active_recall(
                "Vasıflı bir doğum personelinin (ebe/hekim) varlığı doğumun ilk anlarında hangi ölümcül komplikasyonları doğrudan engeller?",
                "Postpartum atonik kanama (oksitosin ile), preeklampsi nöbeti (magnezyum sülfat ile) ve doğum kanalı enfeksiyonları (asepsi ilkeleriyle)."
            )
        ]
    })

    return slides
