"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 10 (Slayt 91 - 100)
Konu: Genetik Danışma İlkeleri, Yönlendirici Olmayan Yaklaşım, Pedigri, Prenatal Tanı ve Büyük Entegrasyon
Checkpoint: Slayt 100 ([TEKRAR SAYFASI - CHECKPOINT 10])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_10_slides():
    return [
        # Slayt 91
        {
            "title": "Genetik Danışmanın Tanımı, Kapsamı ve Temel Hedefleri",
            "subtitle": "Kalıtsal Hastalık Riski Taşıyan Ailelere Bilimsel ve Psikolojik Rehberlik",
            "badge": "Genetik Danışma Esasları",
            "coreContent": {
                "text": "Genetik danışma; kalıtsal veya kromozomal bir hastalık tanısı almış, bu hastalık açısından risk taşıyan bireylere ve ailelerine hastalığın doğasını, genetik mekanizmasını, kalıtım kalıbını, tekrarlama (rekürrens) risklerini, prognozunu, varsa tedavi ve izlem seçeneklerini anlaşılır bir dille aktaran, üreme kararlarında aileye rehberlik eden profesyonel bir iletişim ve destek sürecidir. Genetik danışma yalnızca hasta bireyi değil, tüm geniş aileyi ve gelecek kuşakları kapsar. Danışmanın temel hedefleri: (1) Aileye tıbbi bilgileri eksiksiz ve abartısız aktarmak, (2) Hastalığın sonraki gebeliklerde tekrarlama riskini doğru hesaplamak, (3) Ailenin kendi değer yargılarına, inançlarına ve kültürel yapısına uygun kararları özgürce alabilmesi için psikolojik destek sağlamak ve (4) Varsa doğum öncesi (prenatal) ve preimplantasyon genetik tanı seçeneklerini sunmaktır.",
                "keyBullets": [
                    {"title": "İletişim Süreci", "desc": "Hastalığın risklerini ve seçeneklerini aileye anlaşılır dille aktaran profesyonel rehberliktir.", "isKey": True},
                    {"title": "Geniş Aile Odaklı", "desc": "Yalnızca hastayı değil, risk taşıyan ebeveynleri, kardeşleri ve akrabaları da kapsar.", "isKey": True},
                    {"title": "Özerk Karar Desteği", "desc": "Ailenin kendi değerlerine göre en uygun üreme kararını vermesine destek olur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Danışma Boyutu", "Temel İşlev / İçerik", "Klinik Amaç"],
                    [
                        [("Tanısal Doğrulama", False, ""), ("Klinik ve sitogenetik tanının kesinleştirilmesi", True, "Doğru teşhis"), ("Yanlış risk hesabını önlemek"), ],
                        [("Risk Hesabı", False, ""), ("Mendeliyen ve ampirik rekürrens riskleri", True, "Tekrarlama olasılığı"), ("Gelecek gebelik riskini netleştirmek"), ],
                        [("Seçeneklerin Sunumu", False, ""), ("Prenatal tanı, PGT, evlat edinme seçenekleri", True, "Alternatif üreme yolları"), ("Aileye çözüm alternatifleri sunmak"), ],
                        [("Psikososyal Destek", False, ""), ("Suçluluk duygusunu hafifletme, yas yönetimi", False, ""), ("Ailenin duygusal yükünü hafifletmek"), ]
                    ]
                ),
                make_cloze(
                    "Kalıtsal hastalık riski taşıyan bireylere hastalığın tekrarlama risklerini ve üreme seçeneklerini aktaran profesyonel sürece genetik danışma adı verilir.",
                    "genetik danışma",
                    "Tıbbi iletişim sürecinin adını yazınız"
                ),
                make_active_recall(
                    "Genetik danışmanlık hizmeti kimlere verilmelidir?",
                    "Kalıtsal veya kromozomal bir hastalık tanısı almış bireylere, taşıyıcı ebeveynlere ve bu hastalığı taşıma riski bulunan tüm akrabalarına verilir.",
                    "Danışmanlık hedef kitlesi"
                )
            ],
            "spotPearls": [
                "Genetik danışma profesyonel bir iletişim, risk hesaplama ve destek sürecidir.",
                "Hedef kitlesi hasta birey, ebeveynler ve risk altındaki tüm akrabalarıdır.",
                "Hastalığın doğası, kalıtımı, tekrarlama riski ve prenatal tanı seçenekleri aktarılır."
            ]
        },

        # Slayt 92
        {
            "title": "Yönlendirici Olmayan (Non-Directive) Danışmanlık İlkesi ve Etik",
            "subtitle": "Hasta Özerkliğine Saygı, Tarafsızlık ve Bilgilendirilmiş Onam",
            "badge": "Etik İlkeler",
            "coreContent": {
                "text": "Tıbbi genetik danışmanlığın en temel, en kutsal ve vazgeçilmez etik ilkesi 'Yönlendirici Olmayan Danışmanlık' (non-directive counseling) prensibidir. Genetik danışman hiçbir koşulda aile adına karar vermez; 'gebelik sonlandırılmalıdır' veya 'kesinlikle çocuk sahibi olmalısınız' gibi yönlendirici, emredici veya yargılayıcı cümleler kuramaz. Hekimin görevi; bilimsel gerçekleri, istatistiki riskleri, hastalığın prognozunu, yaşanabilecek zorlukları ve mevcut tüm seçenekleri (gebelik takibi, gebelik terminasyonu, prenatal tanı, PGT, donör gamet, evlat edinme) tamamen tarafsız, objektif ve empatik bir dille masaya yatırmaktır. Nihai karar hakkı istisnasız ve tamamen aileye (ebeveynlere) aittir (özerkliğe saygı ilkesi). Ailenin verdiği karar ne olursa olsun genetik ekibi aileyi desteklemeye ve tıbbi bakımını eksiksiz sürdürmeye devam eder.",
                "keyBullets": [
                    {"title": "Yönlendirici Olmama Kuralı", "desc": "Genetik danışman HİÇBİR ZAMAN aile adına karar vermez ve aileyi yönlendirmez.", "isKey": True},
                    {"title": "Özerkliğe Saygı (Autonomy)", "desc": "Üreme ve gebelik sonlandırma kararı tamamen ve yalnızca ebeveynlere aittir.", "isKey": True},
                    {"title": "Tarafsız Bilgilendirme", "desc": "Tüm riskler ve seçenekler objektif, bilimsel ve empatik bir dille sunulur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_branching_logic(
                    "Prenatal amniyosentez sonucunda bebeğinde Trizomi 21 (Down sendromu) saptanan 34 yaşında bir çift, genetik polikliniğinde gözyaşları içinde 'Doktor bey, siz bizim yerimizde olsaydınız bu gebeliği sonlandırır mıydınız? Bize ne yapmamız gerektiğini söyleyin' diye soruyor. Tıbbi genetik etiğine göre verilecek en doğru yanıt hangisidir?",
                    [
                        {"text": "Bu kararın ailenin inançları, değerleri ve yaşam koşulları doğrultusunda yalnızca kendileri tarafından verilebileceğini empatik bir dille belirtmek; her iki seçeneğin de (gebeliğin devamı ve sonlandırılması) tıbbi, sosyal ve yasal boyutlarını tarafsızca anlatarak kararlarında yanlarında olunacağını ifade etmek", "isCorrect": True, "feedback": "Kusursuz tıp etiği ve empati! Genetik danışman yönlendirici olamaz (non-directive); karar aileye aittir ve hekim tarafsız rehberlik sağlar."},
                        {"text": "Down sendromlu bireylerin topluma yük olacağını söyleyerek aileyi acilen kürtaja yönlendirmek", "isCorrect": False, "feedback": "Yönlendirici olmak etik dışıdır ve hekimlik andına aykırıdır."},
                        {"text": "Her koşulda doğumun kutsal olduğunu savunarak terminasyon seçeneğinden hiç bahsetmemek", "isCorrect": False, "feedback": "Tüm yasal ve tıbbi seçeneklerin objektif sunulması zorunludur."}
                    ]
                ),
                make_cloze(
                    "Tıbbi genetikte danışmanın aile adına karar vermediği ve tamamen tarafsız kaldığı temel etik ilkeye yönlendirici olmayan veya non-directive danışmanlık denir.",
                    "yönlendirici olmayan",
                    "Tarafsız danışmanlık ilkesini anımsayınız"
                ),
                make_active_recall(
                    "Genetik danışmanlık sürecinde yönlendirici olmama ilkesinin dayandığı en temel tıp etiği prensibi nedir?",
                    "Hasta özerkliğine saygı (otonomi) ilkesidir.",
                    "Dört temel biyoetik ilkeden biri"
                )
            ],
            "spotPearls": [
                "Genetik danışma HİÇBİR ZAMAN yönlendirici olmamalıdır (non-directive).",
                "Karar verme yetkisi tamamen ebeveynlere aittir; hekim sadece objektif bilgi verir.",
                "Seçenekler tarafsızca anlatılır ve ailenin vereceği her karar saygıyla desteklenir."
            ]
        },

        # Slayt 93
        {
            "title": "Pedigri (Soyağacı) Çizimi, Aile Öyküsü ve Risk Analizi",
            "subtitle": "Klinik Genetiğin Temel Tanısal Haritası ve Standart Semboller",
            "badge": "Pedigri Analizi",
            "coreContent": {
                "text": "Genetik danışmanlık sürecinin vazgeçilmez ilk klinik adımı, standart uluslararası sembollerle en az üç kuşağı kapsayan ayrıntılı bir soyağacının (pedigri) çizilmesidir. Pedigri çiziminde: kareler erkekleri, daireler dişileri, aralarındaki yatay çizgi evliliği, çift yatay çizgi ise akraba evliliğini (konsanguinite) temsil eder. Etkilenmiş (hasta) bireylerin içi taranır; taşıyıcılar yarım taranır veya ortasına nokta konur; ölen bireylerin üzerine çapraz çizgi çekilir. Aileyi genetik polikliniğe getiren ilk hasta bireye 'proband' (veya indeks vaka / propositus) denir ve pedigride bir ok işaretiyle gösterilir. Pedigride tekrarlayan düşükler, ölü doğumlar, erken bebek ölümleri, infertilite, zihinsel yetersizlik ve dismorfik öyküler titizlikle sorgulanır. Bu harita kalıtım modelinin (otozomal dominant, resesif, X'e bağlı veya kromozomal) deşifre edilmesini ve risk altındaki akrabaların belirlenmesini sağlar.",
                "keyBullets": [
                    {"title": "En Az Üç Kuşak", "desc": "Standart bir genetik incelemede soyağacı mutlaka en az 3 kuşağı içermelidir.", "isKey": True},
                    {"title": "Proband (İndeks Vaka)", "desc": "Ailede ilk saptanan veya kliniğe başvuran hasta bireydir; okla gösterilir.", "isKey": True},
                    {"title": "Akraba Evliliği", "desc": "Eşler arasındaki çift yatay çizgi akraba evliliğini gösterir; resesif riski artırır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Pedigri Sembolü", "Temsil Ettiği Durum", "Klinik Anlamı"],
                    [
                        [("Kare Sembolü", False, ""), ("Erkek cinsiyet", True, "Erkek birey"), ("Normal erkek")],
                        [("Daire Sembolü", False, ""), ("Dişi cinsiyet", True, "Dişi birey"), ("Normal dişi")],
                        [("Çift Yatay Çizgi", False, ""), ("Akraba evliliği (Konsanguinite)", True, "Kan bağı olan evlilik"), ("Otozomal resesif hastalık risk artışı")],
                        [("Ok ile İşaretli Birey", False, ""), ("Proband (İndeks vaka)", True, "İlk başvuran hasta"), ("Ailede ilk dikkat çeken hasta birey")],
                        [("İçi Tamamen Taranmış Sembol", False, ""), ("Etkilenmiş (hasta) birey", False, ""), ("Klinik fenotipi sergileyen kişi")]
                    ]
                ),
                make_cloze(
                    "Genetik soyağacında ailede ilk saptanan veya genetik kliniğine ilk başvuran hasta bireye proband veya indeks vaka denir.",
                    "proband",
                    "İndeks hasta terimini yazınız"
                ),
                make_active_recall(
                    "Genetik soyağacı çiziminde eşler arasındaki evlilik bağının akraba evliliği (konsanguinite) olduğunu belirtmek için hangi sembol kullanılır?",
                    "İki birey arasına çekilen ÇİFT YATAY ÇİZGİ kullanılır.",
                    "Akrabalık çizgisel sembolü"
                )
            ],
            "spotPearls": [
                "Pedigri mutlaka en az 3 kuşağı kapsamalıdır.",
                "Proband (indeks vaka) ailede ilk incelenen bireydir ve okla gösterilir.",
                "Çift çizgi akraba evliliğini, taranmış sembol etkilenmiş bireyi gösterir."
            ]
        },

        # Slayt 94
        {
            "title": "Sitogenetik ve Moleküler Tanı Araçları: Karyotip, FISH ve Mikroarray",
            "subtitle": "Kromozomal Analiz Yöntemlerinin Çözünürlük ve Endikasyon Hiyerarşisi",
            "badge": "Tanısal Genetik Araçlar",
            "coreContent": {
                "text": "Kromozomal hastalıkların laboratuvar tanısında kullanılan üç ana sitogenetik yöntem mevcuttur: (1) Klasik Karyotip Analizi (G-bantlama): Hücrelerin (periferik lenfosit, amniyosit vb.) bölünmeye teşvik edilip metafazda durdurulmasıyla yapılır. Sayısal anomalileri (trizomi, monozomi) ve büyük dengeli/dengesiz yapısal anomalileri (translokasyon, inversiyon) saptar. Çözünürlüğü düşüktür (~4-5 Mb); submikroskobik delesyonları göremez. Dengeli translokasyonları gösteren yegane testtir. (2) Floresan İn Situ Hibridizasyon (FISH): Spesifik bir DNA bölgesine bağlanan floresan problar kullanılır. Hızlıdır (24-48 saat), metafaz veya interfazda çalışabilir; mikrodelesyonları ve marker kromozom kökenini net gösterir. (3) Kromozomal Mikroarray (CMA / aCGH): Tüm genomu milyonlarca oligonükleotid probla tarar; çözünürlüğü çok yüksektir (~50-100 kb). Nedeni bilinmeyen zihinsel yetersizlik, otizm ve çoklu malformasyonlarda İLK TERCİH EDİLECEK TESTTİR; ancak dengeli translokasyonları SAPTAYAMAZ.",
                "keyBullets": [
                    {"title": "Karyotip (G-Bantlama)", "desc": "Dengeli translokasyonları yakalar; çözünürlüğü düşüktür (~5 Mb).", "isKey": True},
                    {"title": "Kromozomal Mikroarray (CMA)", "desc": "Zekâ geriliği ve çoklu anomalide İLK TESTTİR; dengeli anomalileri GÖREMEZ.", "isKey": True},
                    {"title": "FISH Tekniği", "desc": "Hızlı ön tanı ve hedefe yönelik mikrodelesyon (22q11 vb.) saptamasında kullanılır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Genetik Test Yöntemi", "Çözünürlük Sınırı", "Dengeli Translokasyonu Görür mü?", "Primer Kullanım Endikasyonu"],
                    [
                        [("G-Bantlama Karyotip", False, ""), ("~4 - 5 Mb (Düşük)", False, ""), ("EVET, görür (En iyi test)", True, "Dengeli anomaliyi yakalar"), ("Tekrarlayan düşük, translokasyon şüphesi", False, "")],
                        [("Kromozomal Mikroarray (CMA)", False, ""), ("~50 - 100 kb (Çok yüksek)", False, ""), ("HAYIR, göremez (Dengeyi anlamaz)", True, "Materyal kaybı yoksa göremez"), ("Zihinsel gerilik, otizm, dismorfoloji ilk test", False, "")],
                        [("FISH (İn Situ Hibridizasyon)", False, ""), ("Hedefe spesifik prob boyutu", False, ""), ("Kırık noktası biliniyorsa görebilir", False, ""), ("Hızlı anöploidi taraması, mikrodelesyon", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Çoklu konjenital malformasyonları ve gelişimsel gecikmesi olan bir çocukta etiyolojiyi aydınlatmak amacıyla güncel uluslararası kılavuzlara göre ilk basamakta istenmesi gereken en yüksek çözünürlüklü genomik tanı testi hangisidir?",
                    {
                        "A": "Klasik G-bantlama karyotip analizi",
                        "B": "Kromozomal Mikroarray Analizi (CMA / aCGH)",
                        "C": "Tek gen dizi analizi",
                        "D": "Düşük çözünürlüklü C-bantlama",
                        "E": "Southern Blotting"
                    },
                    "B",
                    {
                        "A": "Karyotip çözünürlüğü düşüktür, mikrodelesyonları atlar.",
                        "B": "Doğru cevap B'dir: Güncel kılavuzlarda zekâ geriliği ve çoklu anomalide ilk basamak test Kromozomal Mikroarray'dir (CMA).",
                        "C": "Tek gen çoklu anomalide ilk test olamaz.",
                        "D": "C-bantlama heterokromatin içindir.",
                        "E": "Southern blot artık rutin ilk basamak değildir."
                    }
                ),
                make_cloze(
                    "Kromozomal Mikroarray (CMA) analizi net genetik materyal kaybı veya kazanımı olmayan dengeli translokasyonları saptayamaz.",
                    "dengeli",
                    "CMA'nın göremediği anomali tipini anımsayınız"
                )
            ],
            "spotPearls": [
                "Zekâ geriliği ve çoklu konjenital anomalide İLK TERCİH Kromozomal Mikroarray'dir (CMA).",
                "Kromozomal Mikroarray DENGELİ translokasyonları ve inversiyonları SAPTAYAMAZ.",
                "Dengeli yapısal translokasyonların tespitinde altın standart klasik KARYOTİPTİR."
            ]
        },

        # Slayt 95
        {
            "title": "Down Sendromlu Bebeğe Sahip Aileye Genetik Danışma Yaklaşımı",
            "subtitle": "Karyotipik Doğrulama, Ebeveyn Eğitimi ve İzlem Protokolü",
            "badge": "Down Danışmanlığı",
            "coreContent": {
                "text": "Down sendromlu bir bebek doğduğunda veya prenatal tanı aldığında genetik danışmanlık süreci katı ve kanıta dayalı bir protokolle yürütülür: (1) Sitogenetik Doğrulama: Klinik tanı ne kadar bariz olursa olsun, mutlaka periferik kandan KARYOTİP ANALİZİ yapılmalıdır; çünkü olgunun serbest trizomi mi (%95), translokasyon mu (%4) yoksa mozaik mi (%1) olduğu yalnız karyotiple anlaşılır ve bu ayrım ailenin gelecekteki üreme riskini belirler. (2) Komplikasyon Taraması: Doğumda acilen ekokardiyografi (endokardiyal yastık defekti açısından), işitme testi, tiroid fonksiyon testleri (konjenital hipotiroidi taraması) ve gastrointestinal pasaj takibi yapılmalıdır. (3) Aile Desteği ve Özel Eğitim: Erken müdahale programları, fizyoterapi ve dil terapisi ilk aylardan itibaren planlanmalıdır. (4) Gelecek Gebelikler: Klasik trizomili bir bebeğe sahip olan aileye, sonraki gebeliklerinde ampirik Down sendromu tekrarlama riskinin yaklaşık %1 olduğu ve prenatal tanı endikasyonu bulunduğu anlatılmalıdır.",
                "keyBullets": [
                    {"title": "Karyotip Şarttır", "desc": "Klinik tanı ne kadar açık olursa olsun sitogenetik tip için karyotip zorunludur.", "isKey": True},
                    {"title": "Acil Taramalar", "desc": "İlk ay içinde ekokardiyografi, işitme testi ve tiroid testleri yapılmalıdır.", "isKey": True},
                    {"title": "Gelecek Gebelik Riski", "desc": "Klasik trizomi sonrası rekürrens riski ~%1'dir; prenatal tanı endikasyonudur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Down Sendromlu Yenidoğanda Klinik Yönetim Zinciri",
                    [
                        "1. Doğum odasında hipotoni ve tipik dismorfik stigmalar saptanır",
                        "2. Kesin sitogenetik varyantı (klasik vs translokasyon) belirlemek için periferik karyotip gönderilir",
                        "3. İlk 48 saat içinde kardiyak AVSD taraması için ekokardiyografi ve hipotiroidi taraması yapılır",
                        "4. Aileye yönlendirici olmayan danışmanlık verilerek erken fizyoterapi ve gelişim planı başlatılır"
                    ]
                ),
                make_cloze(
                    "Down sendromu klinik bulguları belirgin olan bir yenidoğanda sitogenetik tipi doğrulamak ve rekürrens riskini belirlemek için karyotip analizi yapılması zorunludur.",
                    "karyotip",
                    "Doğrulayıcı genetik test adını yazınız"
                ),
                make_active_recall(
                    "Down sendromlu bir bebeğe sahip olan ve karyotipi klasik serbest trizomi (47,+21) çıkan genç bir annenin sonraki gebeliğinde Down sendromlu bebek sahibi olma ampirik riski yaklaşık yüzde kaçtır?",
                    "Yaklaşık %1 (veya %1.4) kadardır.",
                    "Klasik trizomi rekürrens yüzdesi"
                )
            ],
            "spotPearls": [
                "Down sendromunda klinik tanı ne kadar belirgin olursa olsun KARYOTİP ANALİZİ ZORUNLUDUR.",
                "İlk haftalarda ekokardiyografi, tiroid paneli ve işitme testi şarttır.",
                "Klasik trizomi 21 sonrası sonraki gebelikte tekrarlama riski yaklaşık %1'dir."
            ]
        },

        # Slayt 96
        {
            "title": "Translokasyon Down Sendromunda Ebeveyn Analizi ve Rekürrens Riski",
            "subtitle": "Kalıtsal Risk Yönetimi, rob(14;21) ve Ebeveyn Taşıyıcılığı",
            "badge": "Translokasyon Danışmanlığı",
            "coreContent": {
                "text": "Eğer yenidoğan bir bebekte Down sendromu tanısı konmuş ve yapılan sitogenetik analizde karyotip Robertsonian translokasyon [örneğin 46,XX,rob(14;21),+21] olarak raporlanmışsa, genetik danışmanlık yaklaşımı klasik trizomiden tamamen farklı bir yola girer. Bu olguların yaklaşık yarısında translokasyon de novo oluşmuştur; ancak diğer yarısında anne veya babadan biri dengeli rob(14;21) taşıyıcısıdır (45 kromozomlu). Bu nedenle bebeğinde translokasyon saptanan HER İKİ EBEVEYNE acilen periferik karyotip analizi yapılmalıdır. Ebeveyn testleri sonucunda: (1) Ebeveynlerin karyotipi normal çıkarsa (de novo translokasyon), sonraki gebeliklerde tekrarlama riski ihmal edilebilir düzeydedir (<%1). (2) ANNE dengeli taşıyıcı çıkarsa, sonraki gebeliklerde Down sendromlu çocuk doğurma riski yaklaşık %15'tir. (3) BABA dengeli taşıyıcı çıkarsa bu risk sperm seleksiyonu nedeniyle yaklaşık %4-5'tir. Taşıyıcı ebeveynlerin kardeşleri ve yakın akrabaları da taranmalıdır.",
                "keyBullets": [
                    {"title": "Ebeveyn Karyotipi Zorunlu", "desc": "Translokasyon Down'da anne ve babanın karyotipi mutlaka incelenmelidir.", "isKey": True},
                    {"title": "Anne Taşıyıcı Riski (%15)", "desc": "Maternal rob(14;21) taşıyıcılığında rekürrens riski yaklaşık %15'tir.", "isKey": True},
                    {"title": "Baba Taşıyıcı Riski (%4-5)", "desc": "Paternal rob(14;21) taşıyıcılığında sperm seleksiyonu nedeniyle risk %4-5'tir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Translokasyon Down: De Novo vs Ebeveyn Taşıyıcılığı",
                    "De Novo Translokasyon (Ebeveynler Normal)",
                    "Translokasyon gametogenezde tesadüfen oluşmuştur; ebeveyn karyotipleri 46 normaldir; tekrarlama riski <%1'dir.",
                    "Ebeveynlerden Biri Dengeli Taşıyıcı (45 Kromozom)",
                    "Translokasyon kalıtsaldır; anne taşıyıcı ise risk %15, baba taşıyıcı ise risk %4-5'tir; PGT veya prenatal tanı önerilir."
                ),
                make_micro_quiz(
                    "İlk çocuğu translokasyon tipi Down sendromu [46,XY,rob(14;21),+21] tanısı alan bir ailede yapılan ebeveyn analizinde annenin 45,XX,rob(14;21) dengeli taşıyıcısı olduğu saptanıyor. Bu annenin bir sonraki gebeliğinde Down sendromlu çocuk doğurma riski yaklaşık yüzde kaçtır?",
                    {
                        "A": "Yaklaşık %1",
                        "B": "Yaklaşık %4-5",
                        "C": "Yaklaşık %15",
                        "D": "Yaklaşık %50",
                        "E": "Yüzde 100"
                    },
                    "C",
                    {
                        "A": "Klasik trizomi veya de novo riskidir.",
                        "B": "Baba taşıyıcı olduğundaki ampirik risktir.",
                        "C": "Doğru cevap C'dir: Anne rob(14;21) taşıyıcısı olduğunda Down sendromlu çocuk riski ampirik olarak yaklaşık %15'tir.",
                        "D": "Çok yüksektir.",
                        "E": "Yalnızca rob(21;21)'de görülür."
                    }
                ),
                make_cloze(
                    "rob(14;21) dengeli taşıyıcısı bir annenin çocuğunda Down sendromu gelişme ampirik riski yaklaşık %15 düzeyindedir.",
                    "%15",
                    "Maternal translokasyon risk oranını yazınız"
                )
            ],
            "spotPearls": [
                "Translokasyon Down sendromlu bebeğin anne ve babasına KARYOTİP analizi şarttır.",
                "Anne rob(14;21) taşıyıcısı ise tekrarlama riski %15'tir.",
                "Baba rob(14;21) taşıyıcısı ise sperm seleksiyonu nedeniyle tekrarlama riski %4-5'tir."
            ]
        },

        # Slayt 97
        {
            "title": "Dengeli Taşıyıcı Çiftlerde İnfertilite, Düşükler ve PGT Seçenekleri",
            "subtitle": "Preimplantasyon Genetik Tanı (PGT-SR) ile Sağlıklı Embriyo Seçimi",
            "badge": "Üreme Genetiği ve PGT",
            "coreContent": {
                "text": "Ebeveynlerden birinde dengeli resiprokal veya Robertsonian translokasyon bulunması, mayoz bölünmede kromatitlerin dengesiz ayrılması (segregasyon) nedeniyle ardışık tekrarlayan düşüklere, ölü doğumlara veya çoklu anomalili çocuk doğumuna yol açar. Bu çiftler için günümüz üreme tıbbında en güçlü ve modern çözüm Preimplantasyon Genetik Tanı - Yapısal Düzenlenmeler (PGT-SR) yöntemidir. Çifte tüp bebek (IVF) uygulanır; elde edilen embriyolardan 5. günde (blastokist evresinde) trofektoderm biyopsisi yapılarak hücreler yeni nesil dizileme (NGS) veya mikroarray ile taranır. Yalnızca kromozomal dengesi tam olan (öploid normal veya dengeli taşıyıcı) embriyolar seçilerek anne rahmine transfer edilir. Dengesiz delesyon/duplikasyon taşıyan embriyolar elenir. Bu yöntem habitüel abortus öyküsü olan translokasyon taşıyıcısı çiftlerde canlı doğum oranını %60-70'in üzerine çıkarır.",
                "keyBullets": [
                    {"title": "Dengesiz Embriyo Riski", "desc": "Dengeli taşıyıcı çiftlerde her konsepsiyonda yüksek delesyon/duplikasyon riski vardır.", "isKey": True},
                    {"title": "PGT-SR Yöntemi", "desc": "Tüp bebek embriyolarından biyopsi alınarak dengeli olanların seçilmesidir.", "isKey": True},
                    {"title": "Klinik Başarı", "desc": "Düşükleri engeller ve sağlıklı canlı doğum şansını dramatik olarak artırır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Dengeli Taşıyıcıda PGT-SR Uygulama Zinciri",
                    [
                        "1. Ebeveynde dengeli resiprokal translokasyon saptanır ve tüp bebek (IVF) siklusu başlatılır",
                        "2. Gelişen embriyolar 5. güne (blastokist evresine) ulaştırılır ve trofektoderm biyopsisi yapılır",
                        "3. Biyopside yeni nesil dizileme (NGS) ile segmental delesyon ve duplikasyonlar taranır",
                        "4. Yalnızca dengeli/normal öploid embriyo anne rahmine transfer edilerek sağlıklı gebelik sağlanır"
                    ]
                ),
                make_cloze(
                    "Yapısal kromozom anomalisi taşıyan çiftlerde embriyoların genetik dengesini incelemek için uygulanan preimplantasyon testine PGT-SR adı verilir.",
                    "PGT-SR",
                    "Yapısal düzenlenme PGT kısaltmasını yazınız"
                ),
                make_active_recall(
                    "Preimplantasyon Genetik Tanıda (PGT-SR) embriyonun iç hücre kütlesine (fetüse) zarar vermemek amacıyla biyopsi blastokistin hangi hücre tabakasından alınır?",
                    "Plasentayı oluşturacak olan dış trofektoderm (trophectoderm) hücre tabakasından alınır.",
                    "Blastokist dış hücre tabakası"
                )
            ],
            "spotPearls": [
                "Dengeli translokasyon taşıyıcılarında tekrarlayan düşükleri önlemek için PGT-SR uygulanır.",
                "PGT-SR blastokist trofektoderm biyopsisi ve NGS analiziyle yapılır.",
                "Yalnızca öploid (normal veya dengeli) embriyolar transfer edilir."
            ]
        },

        # Slayt 98
        {
            "title": "Prenatal Tarama ve İnvaziv Tanı Yöntemleri: İkili Test, NIPT ve Amniyosentez",
            "subtitle": "Tarama Testi ile Kesin Tanı Testi Arasındaki Biyolojik ve Klinik Fark",
            "badge": "Prenatal Tanı Yöntemleri",
            "coreContent": {
                "text": "Prenatal genetik yaklaşım iki temel basamakta yürütülür: Tarama Testleri ve İnvaziv Tanı Testleri. Tarama testleri risk belirler, kesin tanı koydurmaz: (1) Birinci Trimester İkili Test (11-14. hafta): Fetal ense saydamlığı (NT) ölçümü ile maternal serumda serbest beta-hCG ve PAPP-A düzeylerinin kombine edilmesidir (Down sendromunda NT artmış, hCG artmış, PAPP-A düşüktür). (2) Hücresiz Fetal DNA Taraması (NIPT / cfDNA): Maternal kanda dolaşan plasental kaynaklı serbest DNA parçalarının yeni nesil dizilenmesidir; Down sendromu için duyarlılığı >%99'dur ancak bir TARAMA TESTİDİR; pozitif sonuç mutlaka invaziv testle doğrulanmalıdır. Kesin Tanı Testleri ise fetüse ait hücreleri doğrudan inceleyen invaziv yöntemlerdir: Koryon Villus Örneklemesi (CVS; 11-14. haftalarda trofoblast biyopsisi) ve Amniyosentez (15-20. haftalarda amniyon sıvısı aspirasyonu). İnvaziv testlerde hücre kültürüyle Karyotip ve Mikroarray çalışılarak %100 kesin tanı konur.",
                "keyBullets": [
                    {"title": "Tarama vs Tanı", "desc": "İkili test ve NIPT tarama testidir (kesin tanı koymaz); CVS ve Amniyosentez tanı testidir.", "isKey": True},
                    {"title": "İkili Test Belirteçleri", "desc": "Down sendromunda fetal NT artar, hCG artar, PAPP-A belirgin derecede düşer.", "isKey": True},
                    {"title": "NIPT Doğrulaması", "desc": "NIPT pozitif çıksa bile gebelik sonlandırma kararı için invaziv test doğrulaması ŞARTTIR.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Yöntem", "Uygulama Haftası", "Test Niteliği (Tarama vs Tanı)", "Fetal Kayıp Riski"],
                    [
                        [("Kombine İkili Test", False, ""), ("11 - 14. gebelik haftası", False, ""), ("Biyokimyasal Tarama Testi", True, "Yalnızca risk belirler"), ("Risk yok (Non-invaziv)")],
                        [("Hücresiz Fetal DNA (NIPT)", False, ""), ("10. haftadan itibaren her an", False, ""), ("Moleküler Tarama Testi (>%99 duyarlı)", True, "Pozitiflik doğrulama gerektirir"), ("Risk yok (Anne kanı)")],
                        [("Koryon Villus Örneklemesi (CVS)", False, ""), ("11 - 14. gebelik haftası", False, ""), ("Kesin İnvaziv Tanı Testi", True, "Karyotip/CMA ile %100 tanı"), ("Düşük riski: ~1/200 - 1/500")],
                        [("Amniyosentez", False, ""), ("15 - 20. gebelik haftası", False, ""), ("Kesin İnvaziv Tanı Testi", True, "Amniyosit kültürü"), ("Düşük riski: ~1/300 - 1/1000")]
                    ]
                ),
                make_micro_quiz(
                    "36 yaşında bir gebede hücresiz fetal DNA (NIPT) tarama testi sonucu Trizomi 21 (Down sendromu) açısından yüksek riskli olarak raporlanıyor. Genetik danışmanlıkta hastaya önerilmesi gereken bir sonraki en doğru yaklaşım hangisidir?",
                    {
                        "A": "NIPT kesin tanıdır, derhal gebelik sonlandırılmalıdır",
                        "B": "NIPT bir tarama testidir; gebelik kararı verilmeden önce sonuç mutlaka invaziv bir testle (Amniyosentez veya CVS) doğrulanmalıdır",
                        "C": "Test hatalıdır, gebelik rutin takibe bırakılmalıdır",
                        "D": "Yalnızca üçlü tarama testi tekrarlanmalıdır",
                        "E": "Gebeye yüksek doz folik asit başlanmalıdır"
                    },
                    "B",
                    {
                        "A": "NIPT kesin tanı değildir, doğrudan terminasyon yapılamaz.",
                        "B": "Doğru cevap B'dir: NIPT tarama testidir; yalancı pozitiflikler olabileceğinden sonuç mutlaka amniyosentez veya CVS karyotipi ile doğrulanmalıdır.",
                        "C": "Yüksek risk göz ardı edilemez.",
                        "D": "Üçlü test NIPT'ten daha zayıftır.",
                        "E": "Trizomiyi tedavi etmez."
                    }
                ),
                make_cloze(
                    "Birinci trimester kombine ikili tarama testinde Down sendromlu fetüslerde maternal serum PAPP-A düzeyi belirgin derecede düşük bulunur.",
                    "düşük",
                    "PAPP-A değişim yönünü anımsayınız"
                )
            ],
            "spotPearls": [
                "NIPT ve İkili Test TARAMA testidir; kesin tanı koymaz.",
                "CVS ve Amniyosentez İNVAZİV KESİN TANI testleridir.",
                "NIPT pozitifliği gebelik sonlandırılmadan önce MUTLAKA amniyosentez veya CVS ile doğrulanmalıdır."
            ]
        },

        # Slayt 99
        {
            "title": "Kromozomal Hastalıklarda Multidisipliner Takip ve Yaşam Kalitesi",
            "subtitle": "Kardiyoloji, Endokrinoloji, Özel Eğitim ve Sosyal Entegrasyon",
            "badge": "Multidisipliner İzlem",
            "coreContent": {
                "text": "Kromozomal hastalıkların ve sendromların günümüzde tam bir genetik küratif tedavisi bulunmamaktadır; ancak erken tanı, proaktif tıbbi takip ve organize multidisipliner yaklaşımlar bu bireylerin yaşam süresini ve kalitesini dramatik biçimde artırmıştır (Down sendromunda ortalama yaşam süresi 1960'larda 12 yıl iken günümüzde 60 yaşın üzerine çıkmıştır). Başarılı bir izlem protokolü şu uzmanlık alanlarının senkronize çalışmasını gerektirir: (1) Pediatrik Kardiyoloji: Yaşamın ilk haftasında ekokardiyografi ile konjenital anomalilerin (AVSD, Fallot, koarktasyon) tespiti ve erken cerrahi düzeltimi. (2) Pediatrik Endokrinoloji: Turner'da büyüme hormonu ve östrojen replasmanı, Down'da hipotiroidi taraması, Klinefelter'da testosteron replasmanı. (3) Özel Eğitim, Fizyoterapi ve Dil Terapisi: Nörogelişimsel potansiyelin en üst düzeye çıkarılması. (4) Tıbbi Genetik: Düzenli izlem, aile eğitimi ve yeni gebelik planlaması.",
                "keyBullets": [
                    {"title": "Yaşam Beklentisi Artışı", "desc": "Down sendromunda yaşam süresi modern kardiyak cerrahi ile 60 yaşın üzerine çıkmıştır.", "isKey": True},
                    {"title": "Kardiyak Erken Cerrahi", "desc": "Kardiyak defektlerin erken tamiri bebeklik mortalitesini ortadan kaldıran en büyük adımdır.", "isKey": True},
                    {"title": "Bütüncül Rehabilitasyon", "desc": "Fizyoterapi, dil terapisi ve endokrin replasmanlar bağımsız yaşamı destekler.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sendrom", "Birincil Multidisipliner İzlem Odağı", "Temel Tıbbi Müdahale"],
                    [
                        [("Down Sendromu (Trizomi 21)", False, ""), ("Kardiyoloji, Tiroid, İşitme, Erken Eğitim", True, "Kalp ve tiroid izlemi"), ("AVSD erken cerrahisi, L-tiroksin, fizyoterapi")],
                        [("Turner Sendromu (45,X)", False, ""), ("Endokrinoloji, Kardiyoloji, Nefroloji", True, "Boy ve kalp izlemi"), ("Büyüme hormonu, östrojen/progesteron, koarktasyon takibi")],
                        [("Klinefelter Sendromu (47,XXY)", False, ""), ("Endokrinoloji, Psikiyatri, Üroloji", True, "Hormon ve infertilite"), ("11-12 yaşta testosteron replasmanı, mikro-TESE danışmanlığı")],
                        [("Prader-Willi Sendromu", False, ""), ("Endokrinoloji, Diyetisyen, Uyku Kliniği", False, ""), ("Büyüme hormonu, sıkı kalori kısıtlaması, PSG izlemi")]
                    ]
                ),
                make_cloze(
                    "Down sendromlu bireylerde 1960'larda 12 yıl olan ortalama yaşam beklentisi, konjenital kalp cerrahisindeki ilerlemelerle günümüzde 60 yaşın üzerine çıkmıştır.",
                    "60",
                    "Güncel yaşam beklentisi yaşını düşününüz"
                ),
                make_active_recall(
                    "Klinefelter sendromlu adölesanlarda önökoid vücut yapısını düzeltmek, kemik mineral yoğunluğunu korumak ve sekonder seks karakterlerini geliştirmek için hangi medikal tedavi başlanır?",
                    "Kademeli testosteron (androjen) replasman tedavisi başlanır.",
                    "Erkek steroid replasmanı"
                )
            ],
            "spotPearls": [
                "Down sendromunda yaşam beklentisi kalp cerrahisi sayesinde 60 yaşın üzerine çıkmıştır.",
                "Turner'da büyüme hormonu ve östrojen; Klinefelter'da testosteron replasmanı esastır.",
                "Tüm sendromlarda erken eğitim ve multidisipliner takip esastır."
            ]
        },

        # Slayt 100 (CHECKPOINT 10)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Tıbbi Genetik Büyük Entegrasyon ve Sınav Spotları",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 10",
            "coreContent": {
                "text": "Bu final checkpoint sayfasında 'Kromozomal Hastalıklar ve Genetik Danışma' dersinin tüm kardinal sınav spotlarını ve kavramsal mimarisini büyük bir entegrasyonla özetliyoruz. Canlı doğumların %1'inde kromozom anomalisi vardır; en sık anöploidilerdir. Turner (45,X) yaşayan tek monozomidir ve anne yaşından bağımsızdır. Canlı doğan 3 otozomal trizomi: Down (21; en sık, hipotoni, AVSD, lösemi), Edwards (18; hipertoni, clenched hand, rocker-bottom ayak, %80 kız) ve Patau'dur (13; holoprozensefali, mikroftalmi + yarık damak + polidaktili triadı, kutis aplazi). En sık yapısal anomali Robertsonian translokasyondur (rob(13;14) ve rob(14;21)); anne taşıyıcı ise Down riski %15, baba taşıyıcı ise %4-5'tir; rob(21;21) riski %100'dür. Klasik delesyonlar Cri du chat (5p15; kedi ağlaması) ve Wolf-Hirschhorn'dur (4p16.3; Yunan miğferi yüzü, nöbet). Mikrodelesyonlar DiGeorge (22q11; CATCH-22, TBX1) ve Williams'tır (7q11; SVAS, kokteyl kişiliği). PMP22 duplikasyonu CMT-1A, delesyonu HNPP yapar. Klinefelter (47,XXY) azospermi, infertilite, yüksek FSH/LH, jinekomasti yapar; 47,XYY fertildir. 15q11 paternal delesyonu Prader-Willi (hiperfaji, obezite), maternal delesyonu Angelman (mutlu kukla, kahkaha, ataksi, UBE3A) yapar. Genetik danışma asla yönlendirici olmamalıdır (non-directive).",
                "keyBullets": [
                    {"title": "Kardinal Trizomiler", "desc": "Down (Hipotoni, AVSD), Edwards (Hipertoni, Clenched hand), Patau (Holoprozensefali, Triad).", "isKey": True},
                    {"title": "Gonozomal ve Yapısal", "desc": "Turner (45,X; kısa boy, çizgi gonad); Klinefelter (47,XXY; infertil); rob(14;21) Anne %15, Baba %4-5.", "isKey": True},
                    {"title": "İmprinting ve Danışma", "desc": "PWS (Paternal 15q kayıp); AS (Maternal 15q kayıp); Genetik Danışma YÖNLENDİRİCİ OLMAZ.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sendrom / Kavram", "Kromozomal / Moleküler Temel", "En Karakteristik Sınav Spotu"],
                    [
                        [("Turner Sendromu", False, ""), ("45,X (Yaşayan tek monozomi)", True, "Otozomal monozomiler yaşamaz"), ("Kısa boy (SHOX), çizgi gonad, aort koarktasyonu, anne yaşından bağımsız")],
                        [("Down Sendromu", False, ""), ("Trizomi 21 (Klasik %95, Translokasyon %4)", True, "Translokasyon anne yaşından bağımsız"), ("İnfantil hipotoni, AVSD, duodenal atrezi, lösemi riski 15 kat")],
                        [("Edwards Sendromu", False, ""), ("Trizomi 18", False, ""), ("İnfantil hipertonisite, clenched hand, rocker-bottom ayak, %80 kız")],
                        [("Patau Sendromu", False, ""), ("Trizomi 13", False, ""), ("Holoprozensefali, mikroftalmi + yarık damak + polidaktili triadı, kutis aplazi")],
                        [("Cri du Chat", False, ""), ("del(5p15)", False, ""), ("Tiz kedi ağlaması sesi (erişkinlikte kaybolur), ay yüz, mikrosefali")],
                        [("Wolf-Hirschhorn", False, ""), ("del(4p16.3)", False, ""), ("Yunan savaşçı miğferi yüzü, balık ağzı, dirençli epilepsi (GABRG1)")],
                        [("DiGeorge Sendromu", False, ""), ("del(22q11.2) [CATCH-22]", False, ""), ("Fallot tetralojisi, timus aplazisi (T hücre yetmezliği), neonatal hipokalsemi")],
                        [("Williams Sendromu", False, ""), ("del(7q11.23)", False, ""), ("Elastin kaybı (Supravalvüler aort stenozu), elfin yüzü, kokteyl partisi kişiliği")],
                        [("Klinefelter Sendromu", False, ""), ("47,XXY (1 Barr cismi)", False, ""), ("Seminifer tübül hiyalinizasyonu, azospermi, infertilite, yüksek FSH/LH, jinekomasti")],
                        [("Prader-Willi (PWS)", False, ""), ("Paternal 15q11 kaybı (%70 delesyon, %30 mUPD)", False, ""), ("İnfantil hipotoni -> Hiperfaji, morbid obezite, hipogonadizm")],
                        [("Angelman (AS)", False, ""), ("Maternal 15q11 kaybı (%70 delesyon, %3-5 pUPD)", False, ""), ("Mutlu kukla, uygunsuz kahkaha, el çırpma ataksisi, konuşamama, UBE3A")],
                        [("Genetik Danışma", False, ""), ("Hasta özerkliği etik ilkesi", True, "En temel biyoetik kural"), ("HİÇBİR ZAMAN YÖNLENDİRİCİ OLMAMALIDIR (Non-directive)")]
                    ]
                ),
                make_cloze(
                    "Tıbbi genetik danışmanlığın en temel biyoetik kuralı sürecin hiçbir zaman yönlendirici olmamasıdır.",
                    "yönlendirici",
                    "Danışmanın kaçınması gereken tavır kelimesini yazınız"
                ),
                make_active_recall(
                    "Tüm kromozomal hastalıklar içinde yaşamla bağdaşan tek tam monozomi hangisidir ve oluşumu anne yaşına bağlı mıdır?",
                    "Turner Sendromudur (45,X) ve oluşumu ANNE YAŞINA BAĞLI DEĞİLDİR.",
                    "Yaşayan tek monozomi ve maternal yaş kuralı"
                )
            ],
            "spotPearls": [
                "Turner (45,X) yaşayan TEK monozomidir ve anne yaşından bağımsızdır.",
                "Down = Hipotoni + AVSD; Edwards = Hipertoni + Clenched hand; Patau = Holoprozensefali + Triad.",
                "rob(14;21) Down riski: Anne taşıyıcı ise %15, baba taşıyıcı ise %4-5; rob(21;21) riski %100.",
                "PWS = Paternal 15q kaybı (hiperfaji); AS = Maternal 15q kaybı (mutlu kukla, UBE3A).",
                "Genetik danışma HİÇBİR ZAMAN YÖNLENDİRİCİ OLMAMALIDIR (non-directive)."
            ]
        }
    ]
