# -*- coding: utf-8 -*-
from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_steps():
    return [
        {
            "slideNumber": 20,
            "title": "Hücresel Şişmenin Işık Mikroskobik Görünümü",
            "subtitle": "Bulanık şişme, berrak vakuolizasyon ve sitoplazmik değişiklikler",
            "badge": "Histopatoloji",
            "badgeColor": "blue",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücresel şişme rutin hematoksilen-eozin (H&E) boyalı kesitlerde ışık mikroskobunda "
                "karakteristik bir morfoloji sergiler. İlk evrede hücreler normal boyutlarına göre belirgin "
                "şekilde irileşir, sınırları belirsizleşir ve sitoplazma granüllü, soluk bir görünüm alır; "
                "bu tabloya klasik patolojide 'bulanık şişme' (cloudy swelling) denir.\n\n"
                "> [TEMEL İLKE] Su girişi arttıkça genişleyen endoplazmik retikulum sisternaları sitoplazmada "
                "küçük, berrak vakuoller oluşturur; buna 'hidropik dejenerasyon' veya vakuoler dejenerasyon denir.\n\n"
                "Çekirdek bu evrede henüz sağlamdır, normal pozisyonunda ve kromatin yapısındadır. "
                "Bu tablo lipid veya glikojen birikimiyle karışabilir; özel histokimyasal boyalarla ayrılır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Bulanık Şişme", "desc": "Hücre sınırlarının silikleştiği ve sitoplazmanın granüllü soluklaştığı erken evredir.", "isKey": True},
                    {"title": "Vakuolizasyon", "desc": "ER sisternalarının su toplayarak mikro-kaviteler oluşturmasıdır.", "isKey": True},
                    {"title": "Çekirdek Durumu", "desc": "Geri dönüşümlü evrede çekirdeğin büzülmesi veya erimesi (nekroz) görülmez.", "isKey": False}
                ],
                "table": {
                    "title": "Hücresel Şişmenin Işık Mikroskopisi",
                    "headers": ["Evre", "Sitoplazma Görünümü", "Hücresel Organel Karşılığı"],
                    "rows": [
                        ["Bulanık Şişme", "Soluk, pembe, granüllü ve genişlemiş", "Genel hücresel ödem, hafif organel şişmesi"],
                        ["Hidropik Dejenerasyon", "Çok sayıda berrak, optik boş vakuol", "Parçalanmış ve genişlemiş ER sisternaları"],
                        ["Balonlaşma Dejenerasyonu", "İleri derecede şişmiş, devasa hücre", "Ağır intraselüler sıvı göllenmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Işık mikroskobunda hidropik dejenerasyonda görülen berrak vakuoller, genişlemiş endoplazmik retikulum sisternalarına karşılık gelir.",
                "📌 [YÜKSEK VERİM] Geri dönüşümlü hücresel şişmede çekirdek yerinde ve sağlamdır; nükleer piknoz veya karyolizis görülmez."
            ],
            "medicalTerms": [
                {"term": "Bulanık Şişme", "explanation": "Hücresel şişmenin başlangıcında sitoplazmanın soluk ve granüllü görünümüdür."},
                {"term": "Balonlaşma", "explanation": "Viral hepatit gibi tablolarda hepatositlerin masif su toplayarak yuvarlak dev hücrelere dönmesidir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Hidropik dejenerasyonda ışık mikroskobunda izlenen berrak sitoplazmik vakuoller genişlemiş endoplazmik retikulum sisternalarıdır.",
                    "endoplazmik retikulum sisternalarıdır",
                    "Hücresel Organel"
                ),
                make_active_recall(
                    "Bir doku kesitinde hücresel şişme ile yağlanma (steatoz) ışık mikroskobunda nasıl ayırt edilir?",
                    "Her ikisinde de berrak vakuoller görülür; ancak donmuş kesitte Oil Red O boyası yapıldığında yağ vakuolleri parlak kırmızı boyanırken, hidropik şişmedeki su vakuolleri boya tutmaz."
                )
            ]
        },
        {
            "slideNumber": 21,
            "title": "Hücresel Şişmenin Makroskobik ve Organ Düzeyinde Bulguları",
            "subtitle": "Parankimatöz organlarda solukluk, turgor artışı ve ağırlık artışı",
            "badge": "Makroskopi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Milyonlarca hücre aynı anda şiştiğinde bu mikroskobik olay tüm organ düzeyinde belirgin "
                "makroskobik değişiklikler doğurur. Şişme en belirgin olarak böbrek, karaciğer ve miyokard "
                "gibi metabolik hızı yüksek parankimatöz organlarda izlenir. Şişen hücreler doku içindeki "
                "kapiller damarları dıştan basıya uğratır.\n\n"
                "> [TEMEL İLKE] Kapiller damarların sıkışması organa gelen kan akımını azaltır; bu nedenle "
                "şişmiş bir organ makroskobik olarak belirgin şekilde SOLUK görünür.\n\n"
                "Ayrıca hücre içi su birikimi nedeniyle organın turgoru (gerginliği) artar, kapsülü gerilir "
                "ve organın total ağırlığında artış saptanır. Kesit yüzeyinden dışarı doğru parankim kabarır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Solukluk", "desc": "Şişen parankim hücrelerinin mikrosirkülasyonu sıkıştırmasıyla organın kansızlaşmasıdır.", "isKey": True},
                    {"title": "Turgor Artışı", "desc": "Su yüklenmesi sonucu organın sert ve gergin bir kıvam almasıdır.", "isKey": True},
                    {"title": "Ağırlık Artışı", "desc": "Tüm hücrelere dolan suyun organ gramajını belirgin yükseltmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Hücresel Şişmenin Makroskobik Özellikleri",
                    "headers": ["Makroskobik Parametre", "Gözlenen Değişiklik", "Fizyopatolojik Neden"],
                    "rows": [
                        ["Organ Rengi", "Soluk, cansız ve opak görünüm", "Şişen hücrelerin kapillerleri ezip kanı boşaltması"],
                        ["Organ Ağırlığı", "Belirgin artmış", "Milyonlarca hücreye su toplanması"],
                        ["Organ Kapsülü", "Gergin, parlaklığını yitirmiş", "Parankim hacim artışının kapsülü germesi"],
                        ["Kesit Yüzü", "Dışa doğru bombeleşir ve taşar", "Kapsül kesilince gergin parankimin rahatlaması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücresel şişme gösteren bir parankimatöz organ makroskobik olarak soluk, gergin (turgoru artmış) ve ağırlaşmıştır.",
                "📌 [YÜKSEK VERİM] Organın soluk görünmesinin nedeni anemi değil, şişen hücrelerin kapiller damarları mekanik olarak sıkıştırmasıdır."
            ],
            "medicalTerms": [
                {"term": "Turgor Artışı", "explanation": "İntraselüler sıvı fazlalığı nedeniyle dokunun elastik gerginliğinin artması durumudur."},
                {"term": "Parankim Kabarması", "explanation": "Şişmiş bir organ kesildiğinde gerilim altındaki dokunun kesi hattından dışarı bombeleşmesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Organ Makroskopisi Karşılaştırması",
                    "Normal Sağlıklı Organ",
                    "Şişmiş (Hidropik) Organ",
                    [
                        "Normal pembe-kırmızı canlı renk",
                        "Normal kıvam ve esneklik",
                        "Kapsül gevşek ve pürüzsüz",
                        "Kesit yüzeyi düz kalır"
                    ],
                    [
                        "Belirgin soluk ve donuk renk",
                        "Turgor artmış, sertleşmiş kıvam",
                        "Kapsül ileri derecede gerilmiş",
                        "Kesit yüzeyi dışa doğru kabarır"
                    ]
                ),
                make_cloze(
                    "Hidropik şişme gösteren bir böbreğin makroskobik olarak soluk görünmesinin nedeni şişen epitel hücrelerinin kapiller damarları sıkıştırmasıdır.",
                    "kapiller damarları sıkıştırmasıdır",
                    "Mikrovasküler Mekanizma"
                )
            ]
        },
        {
            "slideNumber": 22,
            "title": "Geri Dönüşümlü Hasarın Ultrastrüktürel Değişiklikleri",
            "subtitle": "Bleb oluşumu, mikrovillus kaybı ve ribozomların ayrılması",
            "badge": "Ultrastrüktür",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Transmisyon elektron mikroskobisi (TEM), geri dönüşümlü hasarın hücre altı organel düzeyindeki "
                "ilk izlerini ışık mikroskobundan saatler önce yakalar. Plazma membranında hücre iskeletinin "
                "gevşemesiyle dışarı doğru balonlaşmalar ('bleb' veya kabarcıklar) oluşur ve absorptif "
                "yüzeylerdeki mikrovilluslar silinerek kaybolur.\n\n"
                "> [TEMEL İLKE] Granüllü endoplazmik retikulum sisternaları su alarak genişler; bu genişleme "
                "zara tutunmuş olan ribozomların sitoplazmaya dökülmesine (ayrılmasına) yol açar.\n\n"
                "Ribozomların ayrılması protein sentezini dramatik olarak düşürür. Mitokondriler hafifçe "
                "şişer ve fosfolipid membran artıklarından oluşan 'miyelin figürleri' belirmeye başlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Plazma Zarı Blebleri", "desc": "Hücre iskeletinin membranla bağının kopması sonucu oluşan yüzey kabarcıklarıdır.", "isKey": True},
                    {"title": "Ribozom Detachment", "desc": "GER dilatasyonuyla ribozomların dökülmesi ve protein sentezinin durmasıdır.", "isKey": True},
                    {"title": "Miyelin Figürleri", "desc": "Hasarlı organel zarlarından dökülen fosfolipid lamellerinin sarmal oluşturmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Geri Dönüşümlü Hasarın EM Bulguları",
                    "headers": ["Hücresel Yapı", "Elektron Mikroskobu Değişikliği", "Fonksiyonel Etkisi"],
                    "rows": [
                        ["Plazma Zarı", "Bleb oluşumu, mikrovillus kaybı", "Emilim yüzeyinin çökmesi, membran gerginliği"],
                        ["Granüllü ER", "Sisternal dilatasyon, ribozom ayrılması", "Protein sentezinin durması"],
                        ["Mitokondri", "Hafif şişme, krista aralanması", "ATP üretim hızının düşmesi"],
                        ["Sitoplazma", "Miyelin figürleri birikimi", "Membran fosfolipidlerinin kümeleşmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Geri dönüşümlü hasarın elektron mikroskobu bulguları: Membran blebleri, mikrovillus kaybı, ER dilatasyonu ve ribozomların ayrılmasıdır.",
                "📌 [YÜKSEK VERİM] Ribozomların endoplazmik retikulumdan ayrılması (detachment) protein sentez mekanizmasının durduğunu gösterir."
            ],
            "medicalTerms": [
                {"term": "Bleb (Kabarcık)", "explanation": "Hücre zarının sitoiskeletten ayrılarak sitoplazmik sıvıyla dışarı doğru balonlaşmasıdır."},
                {"term": "Ribozom Ayrılması", "explanation": "ER şişmesi sonucu poliribozomların granüllü ER zarından çözülüp sitozole dağılmasıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Geri dönüşümlü hasarda protein sentezinin çökmesine yol açan ultrastrüktürel olay ribozomların granüllü ER'den ayrılmasıdır.",
                    "ribozomların granüllü ER'den ayrılmasıdır",
                    "Translasyonel Hasar"
                ),
                make_active_recall(
                    "Elektron mikroskobunda izlenen 'Miyelin Figürleri' nedir ve nasıl oluşur?",
                    "Hasar gören hücre ve organel membranlarından ayrılan fosfolipidlerin, su içinde lameller konsantrik tabakalar (soğan zarı gibi) halinde kümelenmesiyle oluşur."
                )
            ]
        },
        {
            "slideNumber": 23,
            "title": "Böbrek Proksimal Tübülünde Erken İskemik Hasar",
            "subtitle": "Klinikte akut tübüler hasarın geri dönüşümlü evresi",
            "badge": "Organ Patolojisi",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Böbrek proksimal tübül epitel hücreleri, glomerüllerden filtre edilen devasa sodyum miktarını "
                "aktif olarak geri emdikleri için vücudun bazal metabolik hızı en yüksek hücrelerindendir. "
                "Ağır kan kaybı, septik şok veya hipotansiyonda renal kan akımı azaldığında ilk etkilenen "
                "bölge proksimal tübüllerin kıvrıntılı kısımlarıdır.\n\n"
                "> [KLİNİK İPUCU] Erken iskemide proksimal tübül fırçamsı kenarı (mikrovilluslar) hızla dökülür; "
                "apikal zarda blebler oluşarak tübül lümenine dökülür ve silendirler oluşturur.\n\n"
                "Sitoplazmada artmış eozinofili ve hidropik şişme gelişir. Eğer kan basıncı vaktinde düzeltilirse "
                "tübül epiteli tamamen yenilenir ve böbrek fonksiyonları normale döner."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Yüksek Enerji Talebi", "desc": "Proksimal tübülün Na+/K+ ATPaz yoğunluğu iskemiye aşırı duyarlılık yaratır.", "isKey": True},
                    {"title": "Fırçamsı Kenar Kaybı", "desc": "Mikrovillusların dökülerek lümende tıkayıcı silendirler oluşturmasıdır.", "isKey": True},
                    {"title": "Reversibilite", "desc": "Tübül bazal membranı sağlam kaldığı sürece epitel tamamen rejenere olabilir.", "isKey": False}
                ],
                "table": {
                    "title": "Proksimal Tübülde İskemik Hasar Evreleri",
                    "headers": ["Evre", "Morfolojik Lezyon", "Klinik Yansıma"],
                    "rows": [
                        ["Erken (Geri Dönüşümlü)", "Fırçamsı kenar kaybı, blebler, hidropik şişme", "İdrar konsantrasyon yeteneğinde azalma"],
                        ["İlerlemiş (Nekroz)", "Tübül epitelinin dökülmesi, lümende hücresel silendirler", "Oligüri, akut böbrek hasarı (ABH)"],
                        ["İyileşme (Rejenerasyon)", "Kök hücrelerin mitozu, yassılaşmış genç epitel", "Poliüri dönemi ve fonksiyonel düzelme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İskemik böbrek hasarında proksimal tübüllerdeki ilk mikroskobik değişiklik fırçamsı kenar (mikrovillus) kaybı ve apikal bleb oluşumudur.",
                "📌 [KLİNİK İPUCU] Şok tablosunda erken sıvı resüsitasyonu, geri dönüşümlü tübüler şişmenin akut tübüler nekroza (ATN) ilerlemesini engeller."
            ],
            "medicalTerms": [
                {"term": "Fırçamsı Kenar", "explanation": "Böbrek proksimal tübül epitelinin emilim yüzeyini artıran yoğun mikrovillus örtüsüdür."},
                {"term": "Tübüler Silendir", "explanation": "Lümene dökülen nekrotik epitel hücreleri ve proteinlerin idrar yolunda preslenerek oluşturduğu kalıplardır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Trafik kazası sonrası ağır kanaması olan ve tansiyonu 70/40 mmHg'ye düşen hastanın böbrek patolojisi senaryosu.",
                    [
                        {
                            "text": "Böbrekler iskemiye tamamen dirençlidir; idrar çıkışı hiçbir zaman etkilenmez.",
                            "isCorrect": False,
                            "feedback": "Hatalı! Böbrek tübülleri iskemiye en duyarlı dokulardandır."
                        },
                        {
                            "text": "Proksimal tübüllerde erken hidropik şişme ve fırçamsı kenar kaybı gelişir; acil sıvı replasmanı yapılırsa doku kalıcı hasarsız kurtulabilir.",
                            "isCorrect": True,
                            "feedback": "Mükemmel klinik patoloji kararı! Geri dönüşümlü evrede volüm replasmanı iskemi süresini sınırlandırarak nekrozu önler."
                        },
                        {
                            "text": "Hastanın iki böbreği de anında taşlaşır ve kalsifiye olur.",
                            "isCorrect": False,
                            "feedback": "Biyolojik olarak imkansızdır."
                        }
                    ]
                ),
                make_cloze(
                    "İskemik böbrek hasarında proksimal tübül lümenine bakan mikrovillusların dökülmesine fırçamsı kenar kaybı adı verilir.",
                    "fırçamsı kenar kaybı",
                    "Böbrek Patolojisi"
                )
            ]
        },
        {
            "slideNumber": 24,
            "title": "Yağlanma (Steatoz): İkinci Geri Dönüşümlü Hasar Kalıbı",
            "subtitle": "Trigliserit metabolizmasının bozulması ve sitoplazmik birikim",
            "badge": "Steatoz",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Yağlanma (steatoz), parankim hücrelerinin sitoplazmasında anormal trigliserit birikimini "
                "ifade eden ikinci ana geri dönüşümlü hasar biçimidir. Yağ metabolizmasında merkezi rol "
                "oynayan organlarda, özellikle karaciğerde, kalpte, iskelet kasında ve böbrekte görülür. "
                "Karaciğer steatozunun en sık nedenleri alkol kötüye kullanımı, obezite ve tip 2 diyabettir.\n\n"
                "> [TEMEL İLKE] Yağlanma geri dönüşümlü bir hasar formudur; etken (örneğin alkol veya toksin) "
                "ortadan kalktığında biriken lipit damlacıkları metabolize edilerek hepatositler tamamen temizlenir.\n\n"
                "Ancak stres devam ederse yağlanma zemininde steatohepatit, kronik hücre ölümü, fibrozis "
                "ve nihayetinde geri dönüşümsüz siroz tablosu gelişebilir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Trigliserit Birikimi", "desc": "Serbest yağ asitlerinin esterleşip hepatositten salgılanamamasıdır.", "isKey": True},
                    {"title": "Reversibilite", "desc": "Neden ortadan kaldırıldığında karaciğer tamamen eski sağlıklı yapısına döner.", "isKey": True},
                    {"title": "Sık Etyolojiler", "desc": "Alkolizm, metabolik sendrom, malnütrisyon, hipoksi ve CCl4 toksisitesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Steatoz Gelişim Mekanizmaları",
                    "headers": ["Etiyolojik Neden", "Biyokimyasal Bozukluk", "Lipit Birikim Nedeni"],
                    "rows": [
                        ["Alkol Tüketimi", "NADH/NAD+ oranı artışı", "Yağ asidi oksidasyonu durur, trigliserit sentezi artar"],
                        ["Açlık / Diyabet", "Periferik yağ dokudan masif lipoliz", "Karaciğere serbest yağ asidi hücumu"],
                        ["Protein Malnütrisyonu", "Apoprotein sentez yetersizliği", "VLDL paketlenemez ve salgılanamaz"],
                        ["Karbon Tetraklorür", "ER zarlarında lipid peroksidasyonu", "Apoprotein üretimi çöker"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Steatoz parankimatöz hücrelerde nötral trigliseritlerin anormal birikimidir; en sık karaciğerde görülür.",
                "📌 [YÜKSEK VERİM] Steatoz geri dönüşümlü bir hasardır; etken ortadan kalktığında organ normale dönebilir."
            ],
            "medicalTerms": [
                {"term": "Trigliserit", "explanation": "Gliserol omurgasına bağlı üç yağ asidinden oluşan temel depo nötral lipittir."},
                {"term": "Apoprotein", "explanation": "Lipitleri bağlayarak suda çözünen lipoprotein (VLDL) kompleksini oluşturan protein zinciridir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Parankimatöz hücrelerde anormal nötral trigliserit birikimiyle karakterize geri dönüşümlü lezyona steatoz denir.",
                    "steatoz",
                    "Metabolik Hasar"
                ),
                make_active_recall(
                    "Alkol tüketimi karaciğerde hangi biyokimyasal mekanizmayla yağlanmaya (steatoza) yol açar?",
                    "Alkolün alkol dehidrogenazla yıkımı intraselüler NADH düzeyini aşırı yükseltir; yüksek NADH yağ asitlerinin mitokondride yakılmasını (beta-oksidasyon) durdurarak trigliserit sentezine yönlendirir."
                )
            ]
        },
        {
            "slideNumber": 25,
            "title": "Karaciğer Yağlanmasının Morfolojisi: Makro ve Mikro",
            "subtitle": "Büyük sarı karaciğer, mikroveziküler ve makroveziküler steatoz",
            "badge": "Histopatoloji",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Karaciğer yağlanması makroskobik olarak organı büyütür (hepatomegali); karaciğer 4-6 kg "
                "ağırlığa ulaşabilir. Organ yumuşak kıvamlı, sarı renkli, parlak ve kesildiğinde bıçağa "
                "yağ bulaştıran bir hal alır. Işık mikroskobunda iki ana histopatolojik patern izlenir: "
                "Mikroveziküler steatoz ve Makroveziküler steatoz.\n\n"
                "> [TEMEL İLKE] Makroveziküler yağlanmada (alkol, obezite), tek bir dev yağ vakuolü çekirdeği "
                "hücre zarına doğru iter; mikroveziküler yağlanmada (Reye sendromu, gebelik akut yağlı karaciğeri) "
                "ise çekirdek merkezdedir ve etrafında minik damlacıklar vardır.\n\n"
                "Parafin kesitlerde ksilen lipitleri erittiği için yağ damlacıkları yuvarlak boşluklar "
                "halinde görünür. Kesin kanıt için dondurulmuş kesitte Oil Red O boyası yapılır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Makroveziküler", "desc": "Tek büyük yağ damlası çekirdeği kenara iter (ör. Alkolizm, Obezite).", "isKey": True},
                    {"title": "Mikroveziküler", "desc": "Çok sayıda küçük damlacık çekirdeği merkezde tutar (ör. Reye sendromu).", "isKey": True},
                    {"title": "Makroskopi", "desc": "Sarı, yumuşak, yağlı ve ileri derecede ağırlaşmış karaciğerdir.", "isKey": False}
                ],
                "table": {
                    "title": "Mikroveziküler vs Makroveziküler Steatoz",
                    "headers": ["Özellik", "Makroveziküler Steatoz", "Mikroveziküler Steatoz"],
                    "rows": [
                        ["Vakuol Boyutu", "Büyük, tek, sitoplazmayı dolduran", "Küçük, çok sayıda, köpüksü"],
                        ["Çekirdek Pozisyonu", "Kenara itilmiş, hilal şeklinde", "Merkezi, yerini korur"],
                        ["Tipik Etyoloji", "Kronik alkolizm, obezite, DM", "Reye sendromu, gebelik akut yağlı karaciğeri"],
                        ["Klinik Seyir", "Sessiz, kronik, geri dönüşümlü", "Akut mitokondriopati, fulminan seyir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Makroveziküler steatozda çekirdek periferik kenara itilir; mikroveziküler steatozda çekirdek merkezde kalır.",
                "📌 [SINAV SPOTU] Reye sendromu ve gebeliğin akut yağlı karaciğerinde tipik olarak mikroveziküler steatoz görülür.",
                "🚨 [KRİTİK UYARI] Rutin parafin bloklarda yağlar erir; bu nedenle steatozu doğrulamak için dondurulmuş (frozen) kesitte Oil Red O boyanır."
            ],
            "medicalTerms": [
                {"term": "Makroveziküler Steatoz", "explanation": "Hepatosit sitoplazmasını tek bir büyük lipit vakuolünün doldurup çekirdeği kenara itmesidir."},
                {"term": "Reye Sendromu", "explanation": "Viral enfeksiyon sırasında aspirin alan çocuklarda mikroveziküler karaciğer yağlanması ve ensefalopati tablosudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Steatoz Tipleri Ayırıcı Tanısı",
                    "Makroveziküler Steatoz",
                    "Mikroveziküler Steatoz",
                    [
                        "Büyük tek bir yağ vakuolü vardır",
                        "Çekirdek kenara doğru itilmiştir",
                        "Tipik örnek: Kronik alkolizm ve obezite",
                        "Klinik tablo genellikle sessizdir"
                    ],
                    [
                        "Çok sayıda minik köpüksü damlacık vardır",
                        "Çekirdek merkezdeki yerini korur",
                        "Tipik örnek: Reye sendromu ve gebelik",
                        "Akut karaciğer yetmezliği yapabilir"
                    ]
                ),
                make_cloze(
                    "Çocuklarda viral enfeksiyonda aspirin kullanımı sonrası gelişen mikroveziküler karaciğer yağlanması tablosuna Reye sendromu denir.",
                    "Reye sendromu",
                    "Pediatrik Patoloji"
                )
            ]
        },
        {
            "slideNumber": 26,
            "title": "Miyokardda Yağlanma: Kaplan Derisi (Cor Tigrinum) Görünümü",
            "subtitle": "Kronik anemi ve hipoksinin kalp kasındaki morfolojik yansıması",
            "badge": "Kardiyopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Lipit birikimi yalnızca karaciğerde değil, enerji için yağ asitlerini yoğun kullanan kalp "
                "kasında da gelişebilir. Miyokardiyal yağlanmanın en klasik nedeni uzamış orta dereceli "
                "hipoksi veya derin kronik anemidir. Oksijen azlığı miyositlerde yağ asidi oksidasyonunu "
                "yavaşlatır ve mikroskobik intraselüler lipit damlacıkları birikir.\n\n"
                "> [SINAV SPOTU] Hipoksiye bağlı miyokard yağlanmasında, soluk sarı yağlı miyokard şeritleri "
                "ile normal kırmızı-kahverengi kas şeritleri ardışık çizgilenmeler oluşturur; buna 'Kaplan Derisi Kalp' (Cor Tigrinum) denir.\n\n"
                "Bu çizgilenme epikard altındaki damarların oksijenlenme gradyentinden kaynaklanır. "
                "Buna karşın difteri toksini gibi ağır toksik miyokarditlerde yağlanma çizgisel değil diffüzdür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Cor Tigrinum", "desc": "Kronik hipokside sarı yağlı ve kırmızı sağlam miyokardın zebra/kaplan deseni oluşturmasıdır.", "isKey": True},
                    {"title": "Hipoksi Mekanizması", "desc": "Yağ asitlerinin beta-oksidasyonunun oksijensizlik nedeniyle durmasıdır.", "isKey": True},
                    {"title": "Diffüz Yağlanma", "desc": "Difteri ekzotoksini gibi ağır zehirlenmelerde tüm kalbin homojen sararmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Miyokard Yağlanma Kalıpları",
                    "headers": ["Kalıp", "Etiyolojik Neden", "Makroskobik Görünüm"],
                    "rows": [
                        ["Çizgili (Cor Tigrinum)", "Kronik anemi, orta dereceli hipoksi", "Ardışık sarı-kırmızı şeritler (kaplan postu)"],
                        ["Diffüz Yağlanma", "Difteri toksini, ağır sistemik hipoksi", "Tüm miyokardda homojen soluk sararma ve gevşeme"],
                        ["Adipoz İnfiltrasyon", "Obezite, yaşlılık (Steatoz değil!)", "Epikardiyal yağın miyokard lifleri arasına girmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kronik derin anemide kalp kasında görülen ardışık sarı-kırmızı çizgilenme tablosuna 'Kaplan derisi kalp' (Cor tigrinum) denir.",
                "🚨 [KRİTİK UYARI] Cor tigrinum intraselüler yağ birikimidir (steatoz); miyositler arasına matür yağ dokusu girmesi (lipomatozis/adipoz infiltrasyon) ile karıştırılmamalıdır."
            ],
            "medicalTerms": [
                {"term": "Cor Tigrinum", "explanation": "Kronik anemiye bağlı miyokardiyal yağlanmada izlenen kaplan postu benzeri çizgilenmedir."},
                {"term": "Beta-Oksidasyon", "explanation": "Yağ asitlerinin mitokondri matriksinde parçalanarak asetil-KoA ve ATP ürettiği metabolik yoldur."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Kronik derin anemisi olan bir hastada kalp kasında sarı ve kırmızı şeritlerin oluşturduğu makroskobik tabloya kaplan derisi kalp adı verilir.",
                    "kaplan derisi kalp",
                    "Kardiyak Patoloji"
                ),
                make_active_recall(
                    "Cor Tigrinum tablosundaki sarı çizgilenme ile kırmızı çizgilenmenin hücresel temeli nedir?",
                    "Sarı çizgiler damardan uzak kalarak derin hipoksi yaşayan ve yağ biriktiren miyosit alanlarıdır; kırmızı çizgiler ise damara yakın olup yeterli oksijen alarak normal rengini koruyan miyositlerdir."
                )
            ]
        },
        {
            "slideNumber": 27,
            "title": "Hücre Hasarında İntraselüler Kalsiyum Dengesi",
            "subtitle": "Kalsiyum pompaları, mitokondriyal sekestrasyon ve sitotoksisite",
            "badge": "Biyokimya",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Normal sağlıklı bir hücrede sitozolik serbest kalsiyum (Ca2+) konsantrasyonu, ekstraselüler "
                "sıvıya kıyasla 10.000 kat daha düşüktür (~0.1 mikromolar vs 1.3 milimolar). Bu devasa gradient, "
                "hücre zarı ve endoplazmik retikulumdaki ATP bağımlı Ca2+ pompaları ile mitokondrinin kalsiyum "
                "sekestrasyon yeteneği sayesinde titizlikle korunur.\n\n"
                "> [TEMEL İLKE] İskemi ve toksinler ATP'yi tükettiğinde kalsiyum pompaları çöker; hücre dışından "
                "sitozole kontrolsüz Ca2+ akar ve ER depolarındaki kalsiyum sitoplazmaya boşalır.\n\n"
                "Sitozolik kalsiyumun kontrolsüz yükselmesi, hücre hasarının geri dönüşümsüz faza geçmesinde "
                "en ölümcül tetikleyicidir; çünkü hücreyi içeriden parçalayacak yıkıcı enzimleri aktive eder."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "10.000 Kat Gradient", "desc": "Sitozol kalsiyumu son derece düşük tutularak hücre uyarılabilirliği kontrol edilir.", "isKey": True},
                    {"title": "Depo Boşalması", "desc": "ATP tükenmesiyle ER ve mitokondrideki kalsiyum sitoplazmaya sızar.", "isKey": True},
                    {"title": "Enzim Aktivasyonu", "desc": "Artan serbest kalsiyum fosfolipaz, proteaz ve endonükleazları çalıştırır.", "isKey": True}
                ],
                "table": {
                    "title": "Hücre İçi ve Dışı Kalsiyum Dinamikleri",
                    "headers": ["Kompartıman", "Serbest Ca2+ Düzeyi", "Dengeyi Koruyan Mekanizma"],
                    "rows": [
                        ["Ekstraselüler Sıvı", "~ 1.3 mM (Yüksek)", "Sistemik kalsiyum homeostazı"],
                        ["Normal Sitozol", "~ 0.1 µM (Çok düşük)", "ATP bağımlı Ca2+ ATPaz pompaları"],
                        ["İskemik Sitozol", "Masif artmış (> 1-10 µM)", "Pompaların iflası ve hücre içine kontrolsüz akış"],
                        ["İntraselüler Depolar", "ER ve Mitokondri", "Membran potansiyeli ve kalsiyum bağlayıcı proteinler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Normalde sitozolik serbest kalsiyum düzeyi ekstraselüler kalsiyumdan yaklaşık 10.000 kat daha düşüktür.",
                "📌 [YÜKSEK VERİM] Hücre hasarında sitozole kalsiyum girişi fosfolipazları, proteazları, ATPazları ve endonükleazları aktive ederek hücreyi intihara sürükler."
            ],
            "medicalTerms": [
                {"term": "Sitozolik Ca2+", "explanation": "Hücre sitoplazmasında serbest iyon halinde bulunan ve sinyal iletiminde kullanılan kalsiyumdur."},
                {"term": "Sekestrasyon", "explanation": "İyonların sitoplazmadan çekilerek endoplazmik retikulum veya mitokondri içine hapsedilmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kalsiyum Aracılı Hücre Yıkım Zinciri",
                    [
                        "1. Enerji Krizi: İskemi sonucu ATP tükenir ve membran Ca2+ pompaları durur.",
                        "2. Kalsiyum Hücumu: Ekstraselüler Ca2+ ve ER kalsiyumu sitoplazmaya boşalır.",
                        "3. Enzim İndüksiyonu: Sitozolik kalsiyum membran yıkan fosfolipazları aktive eder.",
                        "4. İskelet Yıkımı: Ca2+ bağımlı proteazlar sitoiskelet proteinlerini parçalar.",
                        "5. DNA Parçalanması: Endonükleazlar aktive olarak nükleer kromatini kırar."
                    ]
                ),
                make_cloze(
                    "Hücre hasarında sitozolik kalsiyum artışının membranları parçalamasını sağlayan enzim fosfolipazdır.",
                    "fosfolipazdır",
                    "Yıkıcı Enzim"
                )
            ]
        },
        {
            "slideNumber": 28,
            "title": "Kalsiyumun Aktive Ettiği 4 Yıkıcı Enzim Ailesi",
            "subtitle": "Fosfolipazlar, proteazlar, endonükleazlar ve ATPazlar",
            "badge": "Enzimler",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Sitozolik kalsiyum konsantrasyonundaki anormal artış, hücre için 'kıyamet sinyali' anlamına gelir. "
                "Yüksek kalsiyum hücre içinde sessizce bekleyen 4 ölümcül enzim ailesini aktif hale getirir: "
                "1) Fosfolipazlar (hücre ve organel zarlarındaki fosfolipidleri yıkar), 2) Proteazlar (hücre "
                "iskeletini ve membran proteinlerini parçalar), 3) Endonükleazlar (nükleer DNA ve kromatini "
                "parçalar), 4) ATPazlar (kalan kısıtlı ATP rezervlerini hızla tüketir).\n\n"
                "> [KRİTİK UYARI] Fosfolipazların aktivasyonu sonucu açığa çıkan serbest yağ asitleri ve "
                "lizofosfolipidler, deterjan etkisi göstererek zarları doğrudan deler.\n\n"
                "Bu enzimlerin kontrolsüz çalışması, geri dönüşümlü şişme evresini saniyeler içinde geri dönüşümsüz "
                "membran rüptürüne ve otolitik nekroza taşır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Fosfolipaz", "desc": "Zar fosfolipidlerini yıkarak membran geçirgenliğini kalıcı bozar.", "isKey": True},
                    {"title": "Proteaz", "desc": "Hücre iskeletini parçalayarak membranın balonlaşıp patlamasına yol açar.", "isKey": True},
                    {"title": "Endonükleaz", "desc": "Nükleer DNA'yı parçalayarak kromatin erimesini (karyolizis) başlatır.", "isKey": True}
                ],
                "table": {
                    "title": "Kalsiyum Bağımlı 4 Yıkıcı Enzim",
                    "headers": ["Enzim Grubu", "Hedef Substrat", "Hücresel Yıkıcı Sonuç"],
                    "rows": [
                        ["Fosfolipazlar", "Membran fosfolipidleri", "Plazma ve mitokondri zarında delikler, lizofosfolipid birikimi"],
                        ["Proteazlar", "Sitoiskelet ve membran proteinleri", "Hücre iskeletinin çözülmesi, membran rüptürü"],
                        ["Endonükleazlar", "Kromozomal DNA ve RNA", "Kromatin fragmantasyonu, nükleer parçalanma"],
                        ["ATPazlar", "Adenozin trifosfat (ATP)", "Kalan enerjinin hızla sıfırlanması, metabolik çöküş"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalsiyumun aktive ettiği enzimler: Fosfolipaz (membran hasarı), Proteaz (sitoiskelet yıkımı), Endonükleaz (DNA kırıkları) ve ATPaz'dır (enerji tükenmesi).",
                "📌 [YÜKSEK VERİM] Kalsiyum girişi hücre ölümünün infazcısıdır; enzimatik otolizi tetikler."
            ],
            "medicalTerms": [
                {"term": "Lizofosfolipid", "explanation": "Fosfolipaz etkisiyle bir yağ asidi koparılan, deterjan etkili zar delici moleküldür."},
                {"term": "Endonükleaz", "explanation": "DNA zincirindeki fosfodiester bağlarını içten kırarak genomu parçalayan enzimdir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Kalsiyum Enzimleri",
                    ["Enzim Türü", "Primer Substrat", "Patolojik Etki"],
                    [
                        [("Fosfolipaz", False), ("Membran lipidleri", True, "Zar Bileşeni"), ("Zar delinmesi ve lizis", False)],
                        [("Proteaz", False), ("Hücre iskeleti", True, "Yapısal Protein"), ("Sitoiskelet kopması", False)],
                        [("Endonükleaz", False), ("Genomik DNA", True, "Nükleik Asit"), ("Nükleer erime (karyolizis)", False)],
                        [("ATPaz", False), ("ATP molekülü", True, "Enerji Birimi"), ("Kalan enerjinin tükenmesi", False)]
                    ]
                ),
                make_micro_quiz(
                    "Hücre içi kalsiyum konsantrasyonunun aşırı artması sonucu aktive olan enzimlerden hangisi hücre zarlarındaki fosfolipidleri parçalayarak kalıcı membran defektine yol açar?",
                    {
                        "A": "Endonükleaz",
                        "B": "Fosfolipaz",
                        "C": "Kaspaz-3",
                        "D": "Telomeraz",
                        "E": "Glutatyon peroksidaz"
                    },
                    "B",
                    {
                        "A": "Endonükleaz DNA'yı parçalar.",
                        "B": "Doğru cevap B'dir: Fosfolipazlar membran fosfolipidlerini yıkarak membran bütünlüğünü bozar.",
                        "C": "Kaspaz-3 apoptoz yolağında çalışır.",
                        "D": "Telomeraz telomerleri uzatan koruyucu enzimdir.",
                        "E": "Glutatyon peroksidaz antioksidan savunma enzimidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Geri Dönüşümlü Hasar ve Hidropik Şişme",
            "subtitle": "Bulanık şişme, steatoz kalıpları, cor tigrinum ve kalsiyum toksisitesi",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 3,
            "synthesisNarrative": (
                "Üçüncü kontrol noktasında, geri dönüşümlü hücre hasarının iki temel formu olan hidropik "
                "şişmeyi ve steatozu (yağlanmayı) tüm mikroskobik ve klinik yönleriyle özetliyoruz. "
                "Hücresel şişmede membran bütünlüğü korunmuştur; organ makroskobik olarak soluk ve ağırdır.\n\n"
                "> [ÖZET VURGU] Steatozda makroveziküler yağlanma çekirdeği kenara iterken mikroveziküler "
                "yağlanmada çekirdek merkezdedir; kalsiyum akışı ise yıkıcı enzimleri aktive ederek geri dönüşsüzlüğe kapı açar.\n\n"
                "Aşağıdaki 3 akıl kartını dikkatle gözden geçirerek bu temel bilgileri hafızanıza sabitleyin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Geri Dönüşümlü Karakter", "desc": "Membran sağlamdır, etken kalkarsa hücre tamamen iyileşebilir.", "isKey": True},
                    {"title": "Steatoz Tipleri", "desc": "Makroveziküler (Alkol/Obezite) vs Mikroveziküler (Reye/Gebelik).", "isKey": True},
                    {"title": "Kalsiyum Enzimleri", "desc": "Fosfolipaz, proteaz, endonükleaz ve ATPaz'ın aktivasyonu.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 3 Sentez Tablosu",
                    "headers": ["Lezyon / Mekanizma", "Tipik Morfoloji", "Kritik Klinik Örnek"],
                    "rows": [
                        ["Hidropik Dejenerasyon", "Genişlemiş ER vakuolleri, soluk şişme", "Şokta böbrek tübüler hasarı"],
                        ["Makroveziküler Steatoz", "Tek dev vakuol, çekirdek kenarda", "Kronik alkol karaciğeri"],
                        ["Cor Tigrinum", "Sarı-kırmızı çizgili miyokard deseni", "Kronik derin anemi"],
                        ["Kalsiyum Toksisitesi", "Fosfolipaz ve proteaz aktivasyonu", "İskemik dokuda membran parçalanması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Makroveziküler steatozda çekirdek perifere itilir; mikroveziküler steatozda çekirdek merkezde kalır.",
                "📌 [SINAV SPOTU] Kalsiyum artışının aktive ettiği enzimler: Fosfolipaz, Proteaz, Endonükleaz ve ATPaz'dır."
            ],
            "medicalTerms": [
                {"term": "Lipogenez", "explanation": "Glukoz ve ara ürünlerden yağ asidi ve trigliserit sentezlenmesi sürecidir."},
                {"term": "Otoliz", "explanation": "Ölü hücrenin kendi lizozomal enzimleri tarafından kendi kendini eritmesi olayıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-007",
                    "Makroveziküler steatoz ile mikroveziküler steatoz arasındaki en kritik histopatolojik ayrım kriteri nedir?",
                    "Makroveziküler steatozda tek büyük lipit vakuolü çekirdeği hücre zarına (perifere) iter; mikroveziküler steatozda ise çok sayıda minik damlacık vardır ve çekirdek merkezdeki yerini korur."
                ),
                make_flashcard(
                    "fc-k1-04-008",
                    "Kronik anemide kalpte gelişen 'Cor Tigrinum' (Kaplan derisi) görünümünün patogenetik nedeni nedir?",
                    "Orta dereceli kronik hipoksi nedeniyle miyositlerde yağ asidi oksidasyonunun durması ve biriken intraselüler yağ damlacıklarının kırmızı normal miyokard şeritleriyle ardışık çizgilenmeler oluşturmasıdır."
                ),
                make_flashcard(
                    "fc-k1-04-009",
                    "Hücre içi kalsiyum artışı hangi 4 kritik enzimi aktive ederek hücreyi nekroza sürükler?",
                    "1) Fosfolipaz (membranları deler), 2) Proteaz (hücre iskeletini parçalar), 3) Endonükleaz (DNA'yı kırar), 4) ATPaz (kalan ATP'yi tüketir)."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 3 Sentezi: Geri dönüşümlü hasarda plazma membranında oluşan 'bleb'lerin histolojik kökeni nedir?",
                    "Hücre içi ATP azalması ve kalsiyum yükselmesi sonucu hücre iskeletinin (aktin flamanları) hücre zarına tutunduğu noktalardan gevşemesi ve membranın dışarı doğru balonlaşmasıdır."
                ),
                make_cloze(
                    "Miyokardda hipoksiye bağlı yağlanmada sarı yağlı çizgilerle kırmızı sağlam kas liflerinin oluşturduğu görünüme cor tigrinum denir.",
                    "cor tigrinum",
                    "Kardiyak Terim"
                )
            ]
        }
    ]
