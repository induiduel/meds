"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 8 (Slayt 71 - 80)
Konu: Turner Sendromu (45,X), Sitogenetik Varyantlar, Kardiyovasküler/Renal Bulgular, Çizgi Gonad ve Gonadoblastom
Checkpoint: Slayt 79 ([TEKRAR SAYFASI - CHECKPOINT 8])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_8_slides():
    return [
        # Slayt 71
        {
            "title": "Turner Sendromu (45,X): Yaşamla Bağdaşan Tek Monozomi",
            "subtitle": "Epidemiyoloji, Fetal Doğal Seleksiyon ve Maternal X Baskınlığı",
            "badge": "Turner Sendromu",
            "coreContent": {
                "text": "Turner sendromu, dişi fenotipinde bir cinsiyet kromozomunun tamamen veya kısmen yokluğu ile karakterize, insan türünde YAŞAMLA BAĞDAŞAN TEK TAM MONOZOMİDİR. Canlı doğan kız bebeklerdeki görülme sıklığı yaklaşık 1/2500 ila 1/4000 arasındadır. Ancak insan üreme biyolojisindeki en çarpıcı doğal seleksiyon filtrelerinden biri burada çalışır: 45,X konsepsiyonlarının yaklaşık %95 ila %99'u intrauterin dönemde (özellikle 1. ve 2. trimesterde masif kistik higroma ve hidrops fetalis tablosuyla) spontan düşükle sonuçlanır. Tüm kromozomal düşüklerin yaklaşık %10'unu tek başına 45,X konsepsiyonları oluşturur. Canlı doğabilen şanslı %1-5'lik fraksiyonun moleküler analizi yapıldığında, mevcut tek sağlam X kromozomunun yaklaşık %70-80 oranında anne (maternal), yalnız %20-30 oranında baba kaynaklı olduğu görülür (yani mayotik kayıp çoğunlukla paternal spermatogenezdedir). Çok kritik bir sınav kuralı olarak: Turner sendromu oluşumu ANNE YAŞINA BAĞLI DEĞİLDİR.",
                "keyBullets": [
                    {"title": "Yaşayan Tek Monozomi", "desc": "İnsan türünde canlı doğumla bağdaşan tek tam monozomi karyotipidir.", "isKey": True},
                    {"title": "Devasa Düşük Oranı (%95+)", "desc": "45,X konsepsiyonlarının %95'ten fazlası intrauterin dönemde düşükle kaybedilir.", "isKey": True},
                    {"title": "Anne Yaşından Bağımsız", "desc": "Down sendromunun aksine anne yaşıyla hiçbir korelasyon göstermez.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "İnsan türünde canlı doğumla bağdaşabilen tek tam monozomi Turner sendromudur.",
                    "Turner",
                    "Canlı doğabilen monozomi sendrom adını yazınız"
                ),
                make_table(
                    ["Klinik Parametre", "Turner Sendromu (45,X)", "Biyolojik Yorum"],
                    [
                        [("Canlı Kız Doğum Sıklığı", False, ""), ("~1/2500 - 1/4000 canlı kız doğum", True, "Nispeten seyrek canlı doğum"), ("Canlı doğanların fenotipi ılımlıdır", False, "")],
                        [("Spontan Abortus Oranı", False, ""), ("Konsepsiyonların %95 - 99'u", True, "Aşırı yüksek intrauterin letalite"), ("Düşüklerdeki en sık tekil anomalidir", False, "")],
                        [("Mevcut X Kromozomu Kaynağı", False, ""), ("~%70 - 80 Maternal (anneden)", True, "Maternal X baskınlığı"), ("Kayıp genellikle paternal spermatogenezdedir", False, "")],
                        [("Anne Yaşı İlişkisi", False, ""), ("Anne yaşından tamamen BAĞIMSIZDIR", True, "Yaş korelasyonu yok"), ("Genç annelerde de aynı sıklıkta görülür", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Turner sendromunun (45,X) epidemiyolojisi ve etiyolojik özellikleri ile ilgili aşağıdaki ifadelerden hangisi bilimsel olarak DOĞRUDUR?",
                    {
                        "A": "İleri anne yaşı en önemli kanıtlanmış risk faktörüdür",
                        "B": "45,X konsepsiyonlarının %95'inden fazlası intrauterin dönemde spontan abortusla kaybedilir",
                        "C": "Canlı doğan bebeklerin tamamında ağır mental retardasyon bulunur",
                        "D": "Tüm otozomal monozomiler gibi yaşamla bağdaşmaz",
                        "E": "Ekstra bir X kromozomu içerir"
                    },
                    "B",
                    {
                        "A": "Turner sendromu anne yaşından tamamen bağımsızdır.",
                        "B": "Doğru cevap B'dir: 45,X konsepsiyonlarının %95-99'u düşükle kaybedilir; canlı doğanlar çok küçük bir fraksiyondur.",
                        "C": "Turner sendromunda zekâ genellikle tamamen normaldir.",
                        "D": "Turner otozomal değil gonozomaldir ve yaşayan tek monozomidir.",
                        "E": "Kromozom fazlalığı değil eksikliğidir."
                    }
                )
            ],
            "spotPearls": [
                "Turner sendromu (45,X) yaşamla bağdaşan TEK monozomidir.",
                "45,X konsepsiyonlarının %95'ten fazlası intrauterin dönemde düşükle sonuçlanır.",
                "Turner sendromu ANNE YAŞINA BAĞLI DEĞİLDİR; mevcut X %70-80 anneden gelir."
            ]
        },

        # Slayt 72
        {
            "title": "Turner Sendromunda Karyotip Çeşitliliği ve Genotip-Fenotip Korelasyonu",
            "subtitle": "45,X Monozomisi, i(Xq) İzokromozomu ve del(Xp) vs del(Xq) Ayrımı",
            "badge": "Turner Karyotipleri",
            "coreContent": {
                "text": "Turner sendromu sitogenetik açıdan tek bir karyotip değildir; geniş bir yapısal ve sayısal spektrum sergiler. Olguların yaklaşık %50'si klasik saf monozomi X (45,X) karyotipine sahiptir. İkinci en sık grup %15-20 sıklıkla X kromozomunun uzun kol izokromozomudur [46,X,i(Xq)]; bu varyantta Xp tamamen silindiği ve Xq trizomik olduğu için fenotip klasik 45,X'e çok benzer. Olguların %10-15'i mozaiktir (en sık 45,X / 46,XX). Çok kritik bir genotip-fenotip kuralı olarak: X kromozomunun kısa kol delesyonlarında [del(Xp)] hem belirgin kısa boy hem de çoklu konjenital malformasyonlar görülür (çünkü SHOX geni Xp'dedir). Buna karşılık X kromozomunun uzun kol delesyonlarında [del(Xq)] boy genellikle tamamen normal kalır, klinik tablo yalnız gonadal disfonksiyon ve primer amenore ile sınırlı kalır.",
                "keyBullets": [
                    {"title": "Klasik 45,X Oranı", "desc": "Turner olgularının yaklaşık %50'si klasik tam monozomi X'tir.", "isKey": True},
                    {"title": "İzokromozom i(Xq)", "desc": "Olguların %15'ini oluşturur; Xp kaybı nedeniyle klasik 45,X gibi seyreder.", "isKey": True},
                    {"title": "Xp vs Xq Kuralı", "desc": "del(Xp) kısa boy ve somatik malformasyon yapar; del(Xq) yalnız gonadal yetmezlik yapar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "del(Xp) vs del(Xq) Klinik Farklılığı",
                    "X Kısa Kol Delesyonu [del(Xp)]",
                    "SHOX geni kaybolur; belirgin kısa boy, yele boyun, iskelet deformiteleri ve somatik malformasyonlar ön plandadır.",
                    "X Uzun Kol Delesyonu [del(Xq)]",
                    "SHOX geni korunur; boy normaldir; kritik ovaryan belirteçler silindiği için yalnız gonadal disfonksiyon ve amenore görülür."
                ),
                make_table(
                    ["Karyotipik Yapı", "Görülme Oranı", "Klinik Özellik / Fenotipik Şiddet"],
                    [
                        [("Saf Monozomi 45,X", False, ""), ("~%50 (En sık tip)", True, "Klasik monozomi"), ("Tam klasik fenotip: kısa boy, çizgi gonad, yele boyun", False, "")],
                        [("İzokromozom 46,X,i(Xq)", False, ""), ("~%15 (İkinci en sık)", True, "Uzun kol izokromozomu"), ("Klasik 45,X fenotipine çok benzer tablo", False, "")],
                        [("Mozaik Karyotip (45,X/46,XX)", False, ""), ("~%15", True, "Mozaik varyant"), ("Daha ılımlı fenotip; bazen spontan menstrüasyon", False, "")],
                        [("Ring X [46,X,r(X)]", False, ""), ("~%5", False, ""), ("Halka X'in büyüklüğüne göre değişen fenotip", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "X kromozomunun yapısal anomalilerine bağlı Turner varyantlarında, boy uzunluğunun tamamen normal kaldığı ancak hastanın yalnız gonadal disfonksiyon ve primer amenore ile başvurduğu spesifik delesyon hangisidir?",
                    {
                        "A": "X kromozomu kısa kol delesyonu [del(Xp)]",
                        "B": "X kromozomu uzun kol delesyonu [del(Xq)]",
                        "C": "X kromozomu uzun kol izokromozomu [i(Xq)]",
                        "D": "Tam 45,X monozomisi",
                        "E": "Trizomi X"
                    },
                    "B",
                    {
                        "A": "del(Xp)'de SHOX silindiği için belirgin kısa boy olur.",
                        "B": "Doğru cevap B'dir: del(Xq)'da SHOX geni korunduğu için boy normaldir, yalnız gonadal disfonksiyon izlenir.",
                        "C": "i(Xq)'da Xp silinmiştir, kısa boy olur.",
                        "D": "45,X'te kısa boy sabittir.",
                        "E": "Trizomi X'te boy uzundur."
                    }
                )
            ],
            "spotPearls": [
                "Turner'ın %50'si klasik 45,X; %15'i izokromozom i(Xq); %15'i mozaiktir.",
                "del(Xp)'de KISA BOY ve malformasyonlar sıktır (SHOX geni Xp'dedir).",
                "del(Xq)'da boy normaldir; YALNIZ gonadal disfonksiyon görülür."
            ]
        },

        # Slayt 73
        {
            "title": "Turner Sendromunda Fetal Lenfödem Kalıntıları: Yele Boyun ve Kistik Higroma",
            "subtitle": "Juguler Lenfatik Kese Tıkanıklığı ve Postnatal Morfolojik İzler",
            "badge": "Lenfatik Dismorfoloji",
            "coreContent": {
                "text": "Turner sendromlu bir kız bebeğin dış muayenesinde göze çarpan karakteristik yumuşak doku ve deri stigmalarının neredeyse tamamı, intrauterin dönemde yaşanan masif lenfatik drenaj yetersizliğinin postnatal kalıntılarıdır. Embriyogenez sırasında juguler lenfatik damarların internal juguler vene drene olamaması (lenfatik obstrüksiyon), boynun arka-yan kısımlarında devasa sıvı keseleri olan fetal kistik higromaların ve yaygın fetal hidrops tablosunun gelişmesine yol açar (fetal ölümlerin ana nedenidir). İntrauterin dönemde bu lenfatik ödemi atlatan bebeklerde, rezolüsyona uğrayan higroma alanlarında aşırı gevşek ve genişlemiş cilt kıvrımları kalır. Bu durum doğumda enseden omuzlara doğru uzanan kanat benzeri deri katlantısı olan 'yele boyun' (pterygium colli) ve ense saç çizgisinin aşırı aşağıda olması tablosunu oluşturur. Benzer lenfödem mekanizmasıyla yenidoğanda el ve ayak sırtında gode bırakan şişlikler (konjenital lenfödem) saptanır.",
                "keyBullets": [
                    {"title": "Yele Boyun (Pterygium Colli)", "desc": "Rezorbe olan kistik higromanın bıraktığı kanat benzeri bilateral boyun cildidir.", "isKey": True},
                    {"title": "Düşük Saç Çizgisi", "desc": "Ensede saç çizgisinin belirgin biçimde aşağıya doğru uzanmasıdır.", "isKey": True},
                    {"title": "Periferik Lenfödem", "desc": "Doğumda el ve ayak sırtlarında gode bırakan ödem tanı koydurucu ilk ipucudur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Fetal Lenfödemden Yele Boyuna Uzanan Zincir",
                    [
                        "1. 45,X embriyosunda juguler lenfatik keselerin venöz sisteme bağlanması gecikir",
                        "2. Lenf sıvısı boyun arkasında birikerek büyük nuchal kistik higromalar oluşturur",
                        "3. İntrauterin geç dönemde lenfatik bağlantılar açılarak sıvı dokulardan drene olur",
                        "4. Aşırı gerilmiş gevşek cilt büzüşerek boyundan omuza uzanan 'yele boyun' (pterygium colli) olarak kalır"
                    ]
                ),
                make_cloze(
                    "Turner sendromlu kız bebeklerde rezorbe olan fetal kistik higromanın bıraktığı enseden omuzlara uzanan karakteristik cilt katlantısına yele boyun veya pterygium colli denir.",
                    "yele boyun",
                    "Kanat boyun teriminin Türkçe karşılığını anımsayınız"
                ),
                make_active_recall(
                    "Turner sendromlu bir kız bebeğin doğum odasında pediatrist tarafından ilk dakikalarda fark edilen ve intrauterin lenfatik drenaj bozukluğuna bağlı olan el-ayak bulgusu nedir?",
                    "El ve ayak sırtlarında saptanan belirgin, gode bırakan konjenital lenfödemdir.",
                    "Ekstremite dorsal ödem bulgusu"
                )
            ],
            "spotPearls": [
                "Yele boyun (pterygium colli) rezorbe olan fetal kistik higromanın kalıntısıdır.",
                "Ensede düşük saç çizgisi ve el/ayak sırtında lenfödem kardinal bulgulardır.",
                "Fetal kistik higroma intrauterin 45,X ölümlerinin ana morfolojik zeminidir."
            ]
        },

        # Slayt 74
        {
            "title": "Turner Sendromunda Kısa Boyun Moleküler Temeli: SHOX Geni Dozajı",
            "subtitle": "Kondrosit Proliferasyonu, İskelet Displazisi ve Büyüme Eğrileri",
            "badge": "SHOX ve Kısa Boy",
            "coreContent": {
                "text": "Kısa boy (orijinal boy ortalaması tedavi edilmeyen erişkinde ~140-143 cm), Turner sendromunun en sabit (%95-100 oranında görülen) ve neredeyse istisnasız kardinal klinik bulgusudur. Turner sendromunda boy kısalığının moleküler temeli, X ve Y kromozomlarının kısa kolundaki psödootozomal bölgede (PAR1; Xp22.33) lokalize olan SHOX (Short Stature Homeobox) geninin tek kopyaya düşmesidir (haploinsüfisyens). SHOX geni, büyüme plaklarındaki (epifiz kıkırdağı) kondrositlerin proliferasyonunu ve hipertrofik farklılaşmasını yöneten ana transkripsiyon faktörüdür. Normal kadın ve erkekte SHOX iki aktif kopyadan ifade edilirken, 45,X bireylerde yalnız tek bir kopya bulunur. Bu %50 dozaj kaybı; erken epifizyal füzyona, kemik uzamasının duraklamasına, kubitus valgus deformitesine (dirsek taşıma açısının artması) ve 4. metakarp kısalığına yol açar. Bu nedenle Turner tanısı alan her kıza erken yaşta rekombinant insan Büyüme Hormonu (rhGH) başlanmalıdır.",
                "keyBullets": [
                    {"title": "En Sabit Bulgu", "desc": "Kısa boy (%95+) Turner sendromunun en değişmez fiziksel özelliğidir.", "isKey": True},
                    {"title": "SHOX Haploinsüfisyensi", "desc": "PAR1'deki SHOX geninin tek kopyaya düşmesi epifiz büyümesini duraklatır.", "isKey": True},
                    {"title": "rhGH Tedavisi", "desc": "Erken yaşta başlanan rekombinant büyüme hormonu erişkin boyunu 7-10 cm uzatır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "SHOX Gen Dozajı ve Boy Fenotipi",
                    "Normal Dişi (46,XX - İki Aktif SHOX)",
                    "İki adet PAR1 bölgesi; büyüme plaklarında yeterli kondrosit proliferasyonu; normal erişkin boy persentili.",
                    "Turner Sendromu (45,X - Tek Aktif SHOX)",
                    "Tek bir PAR1 bölgesi; SHOX haploinsüfisyensi nedeniyle epifizde erken duraklama; tedavi edilmezse ortalama 140 cm boy."
                ),
                make_cloze(
                    "Turner sendromundaki kardinal boy kısalığı ve iskelet anomalilerinin temel moleküler nedeni PAR1 bölgesindeki SHOX geninin haploinsüfisyensidir.",
                    "SHOX",
                    "Kısa boy homeobox geni kısaltmasını yazınız"
                ),
                make_active_recall(
                    "Turner sendromlu bir kız çocuğunda nihai erişkin boy potansiyelini artırmak amacıyla pediatrik endokrinoloji tarafından erken çocuklukta başlanan primer medikal tedavi nedir?",
                    "Rekombinant insan Büyüme Hormonu (rhGH) tedavisidir.",
                    "Büyüme plaklarını uyaran hormon tedavisi"
                )
            ],
            "spotPearls": [
                "Kısa boy Turner sendromunun en sabit bulgusudur (%95-100).",
                "Temel moleküler mekanizma PAR1'deki SHOX geninin haploinsüfisyensidir.",
                "Erken dönemde başlanan Büyüme Hormonu (rhGH) tedavisi erişkin boyunu belirgin artırır."
            ]
        },

        # Slayt 75
        {
            "title": "Gonadal Disgenezi: Çizgi Gonad (Streak Gonads) ve Primer Amenore",
            "subtitle": "Oosit Apoptozu, Fibröz Bant Dönüşümü ve Hipergonadotropik Hipogonadizm",
            "badge": "Gonadal Disgenezi",
            "coreContent": {
                "text": "Turner sendromlu bireylerde primer üreme organı olan overlerin embriyolojik gelişiminde dramatik bir hızlanmış dejenerasyon süreci yaşanır. Fetal yaşamın 12-14. haftasına kadar 45,X embriyosunda primordial germ hücreleri normal şekilde genital sırta göç eder ve primitif over taslağını kurar. Ancak normal bir oositin mayoz profazında hayatta kalabilmesi için hücrede İKİ AKTİF X KROMOZOMUNA ihtiyaç vardır. İkinci X kromozomunun yokluğu nedeniyle, intrauterin 16. haftadan itibaren oositlerde kitlesel apoptoz ve foliküler atrezi başlar. Doğum anında veya erken çocuklukta oosit rezervi tamamen tükenir. Over parankimi yerini fonksiyonel folikül içermeyen, avasküler beyazımsı fibröz bağ dokusu bantlarına bırakır; bu patognomonik yapıya 'çizgi gonad' (streak gonad / fibröz bant gonad) adı verilir. Sonuç olarak olguların %90-95'inde spontan puberte gerçekleşmez; sekonder seks karakterleri gelişemez ve primer amenore tablosuyla hipergonadotropik hipogonadizm (yüksek FSH/LH, saptanamayan östrojen) gelişir.",
                "keyBullets": [
                    {"title": "Çizgi Gonad (Streak Gonad)", "desc": "Folikül içermeyen, beyazımsı fibröz bağ dokusu kalıntısına dönüşmüş overlerdir.", "isKey": True},
                    {"title": "Primer Amenore", "desc": "Over yetmezliği nedeniyle hastaların %90'ından fazlası hiç adet kanaması göremez.", "isKey": True},
                    {"title": "Hormon Profili", "desc": "Hipergonadotropik hipogonadizm: FSH ve LH aşırı yüksek, östradiol tabandadır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Turner Over Disgenezisi ve Amenore Zinciri",
                    [
                        "1. 45,X fetüsünde germ hücreleri genital sırta göç eder ancak ikinci X kromozomu yoktur",
                        "2. İki X kromozomu desteği olmayan oositlerde intrauterin 16. haftadan itibaren kitlesel atrezi başlar",
                        "3. Doğumdan önce tüm foliküller ölür ve over dokusu fibröz 'çizgi gonad' bandına dönüşür",
                        "4. Pubertede östrojen üretilemez; primer amenore ve yüksek FSH/LH ile hipergonadotropik hipogonadizm gelişir"
                    ]
                ),
                make_table(
                    ["Hormon", "Turner Sendromundaki Değişim", "Klinik Anlamı"],
                    [
                        [("Serum FSH", False, ""), ("Aşırı derecede YÜKSEK (Menopozal düzey)", True, "FSH tavan yapar"), ("Overde geri bildirim yapacak folikül yokluğu", False, "")],
                        [("Serum LH", False, ""), ("Belirgin derecede YÜKSEK", True, "LH tavan yapar"), ("Hipofizin yanıtsız overi aşırı uyarma çabası", False, "")],
                        [("Östradiol (E2)", False, ""), ("Çok DÜŞÜK veya ölçülemez düzeyde", True, "Östrojen sıfıra yakın"), ("Primer amenore ve meme gelişiminin duraklaması", False, "")]
                    ]
                ),
                make_cloze(
                    "Turner sendromunda over foliküllerinin intrauterin tükenmesi sonucu overlerin dönüştüğü fibröz bağ dokusu kalıntısına çizgi gonad adı verilir.",
                    "çizgi gonad",
                    "Fibröz over şeridi tıbbi terimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Turner sendromunda overler folikülsüz fibröz bantlara döner: ÇİZGİ GONAD (streak gonad).",
                "En sık prezentasyon pubertede adet görememe: PRİMER AMENOREDİR.",
                "Hormon profili hipergonadotropik hipogonadizmdir (FSH ve LH çok yüksek, östrojen çok düşük)."
            ]
        },

        # Slayt 76
        {
            "title": "Kardiyovasküler Anomaliler: Aort Koarktasyonu ve Biküspit Aort",
            "subtitle": "Turner Sendromunda Sol Kalp Obstrüktif Lezyonları ve Aort Diseksiyonu Riski",
            "badge": "Kardiyak Malformasyonlar",
            "coreContent": {
                "text": "Turner sendromlu kız çocuklarının yaklaşık %30-50'sinde kardiyovasküler sistem malformasyonları mevcuttur ve bu anomaliler sendromdaki erken mortalitenin en önemli belirleyicisidir. Trizomi 21'deki AVSD'nin aksine, Turner sendromunda tipik olarak 'sol kalp obstrüktif lezyonları' hakimdir. Tek başına en sık rastlanan konjenital kardiyak anomali olguların yaklaşık %30-40'ında görülen Biküspit Aort Kapağıdır (normal 3 yaprakçık yerine 2 yaprakçık). İkinci en karakteristik ve klasik lezyon ise aort arkının inen aorta geçiş bölgesinde lümenin daralması olan Aort Koarktasyonudur (olguların %10-15'i; kadınlardaki koarktasyon olgularının önemli bir kısmı Turner sendromludur). Bu lezyonlar hipertansiyonla birleştiğinde adölesan ve genç erişkin yaşta yaşamı tehdit eden Aort Diseksiyonu ve Rüptürü riskini genel popülasyona kıyasla 100 katın üzerinde artırır. Tanı anında kardiyak MRG şarttır.",
                "keyBullets": [
                    {"title": "Biküspit Aort Kapağı", "desc": "Turner sendromunda en sık görülen kardiyak anomalidir (olguların %30-40'ı).", "isKey": True},
                    {"title": "Aort Koarktasyonu", "desc": "Turner'ın en klasik lezyonudur (olguların %10-15'i); üst ekstremite hipertansiyonu yapar.", "isKey": True},
                    {"title": "Aort Diseksiyonu Riski", "desc": "Aort dilatasyonu ve koarktasyon zemininde genç yaşta ölümcül diseksiyon riski yüksektir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Down vs Turner Kardiyak Lezyon Karşılaştırması",
                    "Down Sendromu Kalp Lezyonu",
                    "Endokardiyal yastık defektleri (AVSD, VSD); sağ-sol veya sol-sağ şant lezyonları; pulmoner hipertansiyon riski.",
                    "Turner Sendromu Kalp Lezyonu",
                    "Sol kalp obstrüktif lezyonları (Biküspit aort kapağı, Aort koarktasyonu); aort anevrizması ve diseksiyon riski."
                ),
                make_micro_quiz(
                    "15 yaşında boy kısalığı ve primer amenore nedeniyle incelenen bir kız hastada üst ekstremite tansiyonu 150/90 mmHg, alt ekstremite tansiyonu 90/60 mmHg ölçülüyor ve femoral nabızlar zayıf alınıyor. Bu hastada Turner sendromuna eşlik eden en olası kardiyovasküler malformasyon hangisidir?",
                    {
                        "A": "Endokardiyal yastık defekti (AVSD)",
                        "B": "Aort koarktasyonu",
                        "C": "Trunkus arteriyozus",
                        "D": "Büyük arterlerin transpozisyonu",
                        "E": "Triküspit atrezisi"
                    },
                    "B",
                    {
                        "A": "AVSD Down sendromuna özgüdür.",
                        "B": "Doğru cevap B'dir: Üst ekstremite hipertansiyonu, alt ekstremitede düşük tansiyon ve femoral nabız gecikmesi Aort Koarktasyonunun klasik tablosudur ve Turner'da sıktır.",
                        "C": "Trunkus DiGeorge'dadır.",
                        "D": "Transpozisyon siyanotiktir.",
                        "E": "Triküspit atrezisi siyanotik defekttir."
                    }
                ),
                make_cloze(
                    "Turner sendromunda en sık görülen konjenital kardiyak anomali biküspit aort kapağı iken, en karakteristik obstrüktif anomali aort koarktasyonudur.",
                    "aort koarktasyonu",
                    "Karakteristik aort daralma lezyonunu anımsayınız"
                )
            ],
            "spotPearls": [
                "Turner'da en sık kalp anomalisi BİKÜSPİT AORT KAPAĞIDIR (~%30).",
                "En karakteristik lezyon AORT KOARKTASYONUDUR (~%15).",
                "Bu hastalar adölesan ve erişkin dönemde AORT DİSEKSİYONU riski altındadır."
            ]
        },

        # Slayt 77
        {
            "title": "Renal Anomaliler (At Nalı Böbrek) ve İskelet Bulguları: Kubitus Valgus",
            "subtitle": "Kalkan Göğüs, Ayrık Meme Başları ve 4. Metakarp Kısalığı",
            "badge": "Renal ve İskelet Stigmaları",
            "coreContent": {
                "text": "Turner sendromunda kardiyovasküler sisteme ek olarak üriner sistem ve iskelet sisteminde de son derece karakteristik malformasyonlar izlenir. Olguların yaklaşık üçte birinde (%33) yapısal böbrek anomalileri saptanır; bu anomaliler arasında en klasik olanı böbreklerin alt kutuplarının omurga önünde fibröz veya parankimal bir köprüyle birleşmesiyle oluşan 'At Nalı Böbrek' (horseshoe kidney) anomalisidir. Çift toplayıcı sistem ve renal agenezis de görülebilir. İskelet sisteminde kollar vücut yanına sarkıtıldığında dirsek taşıma açısının dışa doğru anormal genişlemesi anlamına gelen 'kubitus valgus' karakteristiktir. Göğüs kafesi geniş ve basıktır; meme başları birbirinden belirgin derecede uzak yerleşimlidir ('kalkan göğüs' / shield chest). Elde 4. metakarp kemiğinin kısa olması (kısalmış 4. parmak) ve yüksek damak diğer tipik dismorfik bulgulardır.",
                "keyBullets": [
                    {"title": "At Nalı Böbrek", "desc": "Böbreklerin alt kutuplarının birleştiği malformasyondur; olguların üçte birinde görülür.", "isKey": True},
                    {"title": "Kubitus Valgus", "desc": "Dirsek taşıma açısının dışa doğru artmasıdır; karakteristik iskelet bulgusudur.", "isKey": True},
                    {"title": "Kalkan Göğüs (Shield Chest)", "desc": "Geniş göğüs kafesi ve birbirinden uzaklaşmış ayrık meme başları tablosudur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sistem", "Karakteristik Turner Bulgusu", "Morfolojik / Klinik Tanım"],
                    [
                        [("Üriner Sistem", False, ""), ("At Nalı Böbrek (Horseshoe Kidney)", True, "Alt kutupları birleşik böbrek"), ("Pelviüreterik darlık ve enfeksiyon riski"), ],
                        [("Dirsek Eklemi", False, ""), ("Kubitus Valgus", True, "Dirsek taşıma açısı artışı"), ("Kolların dışa doğru açılanması"), ],
                        [("Göğüs Kafesi", False, ""), ("Kalkan göğüs (Shield chest)", True, "Geniş basık toraks"), ("Geniş aralıklı, ayrık meme başları"), ],
                        [("El İskeleti", False, ""), ("Kısa 4. metakarp kemiği", False, ""), ("Yumruk sıkıldığında 4. eklem çukuru"), ]
                    ]
                ),
                make_micro_quiz(
                    "Turner sendromlu bir kız çocuğunun batın ultrasonografisinde böbreklerin alt kutuplarının orta hatta birleştiği saptanıyor. Bu karakteristik konjenital anomaliye ne ad verilir?",
                    {
                        "A": "Polikistik böbrek",
                        "B": "At nalı böbrek (horseshoe kidney)",
                        "C": "Multikistik displazik böbrek",
                        "D": "Medüller sünger böbrek",
                        "E": "Pelvik ektopik böbrek"
                    },
                    "B",
                    {
                        "A": "Polikistik kistik lezyondur.",
                        "B": "Doğru cevap B'dir: Böbreklerin alt kutuplarının füzyonuna at nalı böbrek denir ve Turner sendromunda olguların üçte birinde görülür.",
                        "C": "Multikistik unilateral displazidir.",
                        "D": "Medüller sünger tübül dilatasyonudur.",
                        "E": "Pelvik böbrek göç duraklamasıdır."
                    }
                ),
                make_cloze(
                    "Turner sendromunda dirsek ekleminde kolların dışa doğru aşırı açılanması deformitesine kubitus valgus denir.",
                    "kubitus valgus",
                    "Dirsek taşıma açısı deformitesi tıbbi adını yazınız"
                )
            ],
            "spotPearls": [
                "Turner sendromunda en karakteristik renal anomali AT NALI BÖBREKTİR (%33).",
                "Kubitus valgus ve kısa 4. metakarp kemiği tipik iskelet stigmalarıdır.",
                "Kalkan göğüs (shield chest) ve ayrık meme başları göğüs kafesi muayenesinde belirgindir."
            ]
        },

        # Slayt 78
        {
            "title": "Turner Sendromunda Endokrin ve Bilişsel Yönetim Stratejileri",
            "subtitle": "Büyüme Hormonu, Östrojen/Progesteron Replasmanı ve Bilişsel Profil",
            "badge": "Klinik Yönetim",
            "coreContent": {
                "text": "Turner sendromlu bir kız çocuğunun multidisipliner takibinde iki ana endokrinolojik hedef bulunur: (1) Erişkin boyunun maksimize edilmesi: Tanı konur konmaz (genellikle 4-6 yaş civarında) epifizler kapanmadan önce yüksek doz rekombinant insan Büyüme Hormonu (rhGH) başlanır; bu tedavi nihai erişkin boya ortalama 7-10 cm kazandırır. (2) Puberte indüksiyonu ve sekonder seks karakterlerinin kazanılması: 11-12 yaş civarında fizyolojik puberteyi taklit etmek amacıyla düşük doz östrojen replasmanına başlanır; doz kademeli olarak artırılarak meme gelişimi (telarş) ve uterus büyümesi sağlanır. Yaklaşık 2 yıl sonra veya vajinal kanama başladığında endometrial hiperplaziyi önlemek için rejime progesteron eklenir (siklik HRT). Bilişsel açıdan zekâ normaldir; sözel IQ genellikle çok yüksektir, ancak uzamsal algı, görsel-motor koordinasyon ve ileri matematiksel problem çözmede seçici zorluklar yaşanabilir.",
                "keyBullets": [
                    {"title": "Büyüme Hormonu (rhGH)", "desc": "Erken yaşta başlanır; epifizler açıkken boy kazanımını sağlar.", "isKey": True},
                    {"title": "Sıralı Hormon Replasmanı", "desc": "11-12 yaşta östrojenle puberte başlatılır; 2 yıl sonra progesteron eklenir.", "isKey": True},
                    {"title": "Bilişsel Profil", "desc": "Zekâ normaldir; sözel beceriler mükemmeldir, uzamsal/matematiksel destek gerekebilir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Turner Sendromunda Hormon Replasman Aşamaları",
                    [
                        "1. Erken çocuklukta (4-6 yaş) SHOX eksikliğini kompanse etmek için rekombinant büyüme hormonu (rhGH) başlanır",
                        "2. 11-12 yaşında fizyolojik puberteyi başlatmak için kademeli düşük doz östrojen tedavisi verilir",
                        "3. Meme gelişimi (Tanner evre 3) ve uterus matürasyonu sağlandıktan sonra siklik progesteron eklenir",
                        "4. Düzenli siklik çekilme kanamaları (yapay menstrüasyon) sağlanarak osteoporoz ve kardiyovasküler risk önlenir"
                    ]
                ),
                make_cloze(
                    "Turner sendromlu kızlarda puberteyi başlatmak ve sekonder seks karakterlerini geliştirmek için ilk olarak östrojen replasmanına başlanır.",
                    "östrojen",
                    "Puberte indükleyici dişi steroid hormonunu yazınız"
                ),
                make_active_recall(
                    "Turner sendromlu kız çocuklarında zekâ düzeyi genellikle normal iken hangi spesifik akademik ve bilişsel alanda seçici güçlük görülebilir?",
                    "Görsel-uzamsal algı, motor planlama ve ileri matematiksel/geometrik problem çözme alanlarında seçici güçlük görülebilir.",
                    "Seçici bilişsel kısıtlılık alanı"
                )
            ],
            "spotPearls": [
                "Turner'da erken çocuklukta Büyüme Hormonu (rhGH) başlanmalıdır.",
                "11-12 yaşta östrojen ile meme gelişimi sağlanır, sonra endometrial koruma için progesteron eklenir.",
                "Zekâ normaldir; sözel IQ yüksektir, matematik ve uzamsal algıda destek gerekebilir."
            ]
        },

        # Slayt 79 (CHECKPOINT 8)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Turner Sendromu (45,X): Sitogenetik, Klinik ve Yönetim",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 8",
            "coreContent": {
                "text": "Bu bölümde yaşamla bağdaşan tek tam monozomi olan Turner sendromunu (45,X) inceledik. Konsepsiyonların %95'ten fazlası düşükle kaybedilir; canlı doğum 1/2500'dür; ANNE YAŞINA BAĞLI DEĞİLDİR; mevcut X %70 maternaldir. Karyotip: %50 klasik 45,X, %15 izokromozom i(Xq), %15 mozaik. del(Xp) kısa boy ve somatik malformasyon yaparken, del(Xq) yalnız gonadal yetmezlik yapar. Kardinal bulgular: Lenfödem kalıntısı yele boyun (pterygium colli; fetal kistik higromadan kalır), düşük saç çizgisi, periferik ödem; PAR1'deki SHOX haploinsüfisyensine bağlı KISA BOY (%95+); oosit apoptozuna bağlı folikülsüz ÇİZGİ GONAD (streak gonad), primer amenore ve hipergonadotropik hipogonadizm (yüksek FSH/LH, düşük E2); kardiyak olarak biküspit aort kapağı (%30) ve aort koarktasyonu (%15; aort diseksiyonu riski); renal olarak at nalı böbrek (%33); iskelette kubitus valgus ve kalkan göğüstür.",
                "keyBullets": [
                    {"title": "Karyotip ve Yaş", "desc": "Yaşayan tek monozomi; anne yaşından bağımsız; %50 45,X, %15 i(Xq).", "isKey": True},
                    {"title": "Klinik Dörtlü", "desc": "Kısa boy (SHOX), Çizgi gonad (primer amenore), Yele boyun, Aort koarktasyonu/Biküspit aort.", "isKey": True},
                    {"title": "Tedavi Esasları", "desc": "Erken dönemde Büyüme Hormonu (rhGH), adölesanda sıralı östrojen + progesteron.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Boyut", "Turner Sendromundaki İmzası", "Moleküler / Patolojik Karşılığı"],
                    [
                        [("Sitogenetik Durum", False, ""), ("Yaşayan TEK tam monozomi (45,X)", True, "Otozomlar letaldir"), ("Anne yaşından bağımsız oluşur", False, "")],
                        [("En Sabit Bulgu", False, ""), ("Kısa Boy (%95+)", True, "Değişmez fiziksel özellik"), ("SHOX geni haploinsüfisyensi", False, "")],
                        [("Over Patolojisi", False, ""), ("Çizgi Gonad (Streak Gonad)", True, "Fibröz bant over"), ("Hızlanmış intrauterin oosit atrezisi", False, "")],
                        [("Karakteristik Kalp", False, ""), ("Aort Koarktasyonu ve Biküspit Aort", True, "Sol kalp obstrüksiyonu"), ("Aort diseksiyonu riski taşır", False, "")],
                        [("Karakteristik Böbrek", False, ""), ("At Nalı Böbrek (%33)", True, "Alt kutup füzyonu"), ("Üriner staz ve enfeksiyon riski", False, "")]
                    ]
                ),
                make_cloze(
                    "Turner sendromlu kızlarda over parankiminin tamamen bağ dokusuna dönüştüğü patolojik yapıya çizgi gonad adı verilir.",
                    "çizgi gonad",
                    "Fibröz bant gonad terimini anımsayınız"
                ),
                make_active_recall(
                    "Turner sendromunda aort kökü genişlemesi ve koarktasyon zemininde adölesan ve erişkin dönemde riski 100 kat artan yaşamı tehdit edici vasküler acil nedir?",
                    "Aort Diseksiyonu ve Rüptürü (yırtılması) tablosudur.",
                    "Ölümcül aortik acil durum"
                )
            ],
            "spotPearls": [
                "Turner sendromu yaşamla bağdaşan TEK monozomidir ve anne yaşından bağımsızdır.",
                "Kısa boy (SHOX) ve çizgi gonad (primer amenore, yüksek FSH/LH) kardinaldir.",
                "Aort koarktasyonu, biküspit aort ve at nalı böbrek karakteristik malformasyonlardır."
            ]
        },

        # Slayt 80
        {
            "title": "Y Kromozomu İçeren Turner Varyantları (45,X/46,XY) ve Gonadoblastom",
            "subtitle": "Kromozomal Mozaiklik, Maskülinizasyon ve Profilaktik Gonadektomi",
            "badge": "Y Varyantı ve Kanser",
            "coreContent": {
                "text": "Turner sendromu kliniğiyle izlenen hastaların yaklaşık %5-10'unda, sitogenetik analizde karyotipte tam veya parçalı bir Y kromozomu materyali saptanır (en tipik karyotip 45,X / 46,XY mozaikliğidir). Bu hastalar fenotipik dişi olabileceği gibi, klitoromegali veya ambigus genitalya sergileyebilirler. Çok kritik bir onkogenetik kural olarak: Fonksiyon görmeyen disgenezik bir çizgi gonadda Y kromozomuna ait genetik materyal (özellikle Y kromozomunun GBY - Gonadoblastoma lokusu) bulunması, bu gonadda erken çocukluk ve genç kızlık döneminde %20 ila %30 oranında malign potansiyele sahip bir germ hücreli tümör olan Gonadoblastom (ve zemininde Disgerminom) gelişme riskini doğurur. Bu nedenle karyotipinde veya moleküler analizinde (PCR/FISH) Y kromozomu parçası saptanan tüm Turner olgularında, kanser gelişimini önlemek amacıyla tanı anında her iki çizgi gonadın cerrahi olarak çıkarılması (profilaktik bilateral gonadektomi) zorunlu bir hayat kurtarıcı yaklaşımdır.",
                "keyBullets": [
                    {"title": "Y Kromozomu Varlığı", "desc": "Turner olgularının %5-10'unda 45,X/46,XY mozaisizmi veya marker Y bulunur.", "isKey": True},
                    {"title": "Gonadoblastom Riski (%20-30)", "desc": "Disgenezik overde Y varlığı gonadoblastom ve disgerminom riskini tetikler.", "isKey": True},
                    {"title": "Profilaktik Gonadektomi", "desc": "Y materyali saptanan her Turner hastasına acil cerrahi gonadektomi şarttır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Y Kromozomlu Turner ve Gonadoblastom Zinciri",
                    [
                        "1. 45,X/46,XY mozaik karyotipli bireyde çizgi over dokusu içinde Y kromozom dizileri bulunur",
                        "2. Disgenezik gonad dokusunda Y kromozomundaki TSPY ve GBY lokusu anormal aktive olur",
                        "3. Disgenezik germ hücreleri maturasyona uğrayamayarak prekanseröz gonadoblastom odakları kurar",
                        "4. Erken yaşta invaziv disgerminoma dönüşümünü önlemek için profilaktik cerrahi gonadektomi yapılır"
                    ]
                ),
                make_micro_quiz(
                    "Sitogenetik analizinde 45,X / 46,XY mozaik karyotipi saptanan 14 yaşında bir kız çocuğunda, çizgi gonad dokusunda gelişebilecek hangi malign tümör riskini önlemek amacıyla profilaktik bilateral gonadektomi (gonadların cerrahi olarak çıkarılması) önerilir?",
                    {
                        "A": "Granüloza hücreli tümör",
                        "B": "Gonadoblastom (ve Disgerminom)",
                        "C": "Seröz kistadenokarsinom",
                        "D": "Koryokarsinom",
                        "E": "Brenner tümörü"
                    },
                    "B",
                    {
                        "A": "Granüloza seks kord tümörüdür.",
                        "B": "Doğru cevap B'dir: Disgenezik overde Y kromozomu varlığı %20-30 oranında Gonadoblastom ve Disgerminom riskini doğurur; cerrahi şarttır.",
                        "C": "Seröz kistadenokarsinom epiteliyaldir.",
                        "D": "Koryokarsinom trofoblastiktir.",
                        "E": "Brenner transizyonel epiteliyaldir."
                    }
                ),
                make_cloze(
                    "Karyotipinde Y kromozomu materyali saptanan Turner olgularında çizgi gonadlarda gelişme riski yüksek olan spesifik germ hücreli tümör gonadoblastom olarak adlandırılır.",
                    "gonadoblastom",
                    "Disgenezik gonad tümör adını yazınız"
                )
            ],
            "spotPearls": [
                "45,X/46,XY mozaik Turner olgularında Y kromozomu mevcuttur.",
                "Bu olgularda çizgi gonadda %20-30 oranında GONADOBLASTOM gelişme riski vardır.",
                "Tedavide tanı anında PROFİLAKTİK BİLATERAL GONADEKTOMİ zorunludur."
            ]
        }
    ]
