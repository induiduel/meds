"""
Bölüm 8: Hemosiderin ve Demir Depolanması: Hemosideroz, Hemokromatoz ve Prusya Mavisi
Adımlar: 71 - 80
Checkpoint: Adım 79 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # ADIM 71
    slides.append({
        "slideNumber": 71,
        "title": "Demir Metabolizması, Ferritin ve Hemosiderin Biyokimyası",
        "subtitle": "Apoferritin kabuğu, misel agregasyonu ve lizozomal sindirim artıkları",
        "badge": "Demir Biyolojisi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Demir, oksijen taşınması (hemoglobin, miyoglobin) ve sitokrom oksidaz enzimleri için vazgeçilmez bir "
            "elementtir; ancak serbest Fe2+ iyonları Fenton reaksiyonuyla son derece yıkıcı hidroksil radikalleri "
            "üreterek hücre membranlarını parçalar. Bu nedenle vücutta demir daima proteinlere bağlı tutulur. "
            "Hücre içinde demir, apoferritin protein kılıfı içinde 'ferritin' kompleksleri halinde güvenle saklanır.\n\n"
            "> [TEMEL İLKE] Hücre içi demir yükü ferritinin depolama kapasitesini aştığında, ferritin molekülleri "
            "birbirine yapışıp kümelenerek lizozomlarda parçalanır ve çözünmeyen 'hemosiderin' granüllerine dönüşür.\n\n"
            "Hemosiderin, demir yüklü lizozomların (siderozom) ışık mikroskobunda görünür hale gelmiş nihai agregatıdır."
        ),
        "medicalTerms": [
            {"term": "Ferritin", "explanation": "Demiri apoferritin küresi içinde toksisitesiz depolayan temel hücresel proteindir."},
            {"term": "Hemosiderin", "explanation": "Aşırı demir yükünde ferritin moleküllerinin agregasyonuyla oluşan çözünmez granüler pigmenttir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ferritin fizyolojik depodur; hemosiderin aşırı demir yükünün agregatıdır.",
            "📌 [SINAV SPOTU] Serbest demir Fenton reaksiyonu ile ölümcül serbest radikaller üretir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Toksik Serbest Demir", "desc": "Fe2+ hidroksil radikali üretir; daima şaperonla saklanmalıdır.", "isKey": True},
                {"title": "Hemosiderin Dönüşümü", "desc": "Aşırı ferritinin lizozomal sindirim ve agregasyon ürünüdür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hücrede aşırı demir varlığında ferritin moleküllerinin agregasyonu ile hemosiderin granülleri meydana gelir.",
                "hemosiderin",
                "Demir fazlalığında oluşan kaba granüler pigment"
            ),
            make_active_recall(
                "Vücutta fizyolojik demir deposu olan ferritin ile patolojik birikim pigmenti olan hemosiderin arasındaki biyokimyasal ilişki nedir?",
                "Hücre içi demir düzeyi ferritinin bağlama kapasitesini aştığında ferritin molekülleri kümeleşip lizozomlarda kısmen yıkılarak çözünmeyen hemosiderin agregatlarına dönüşür."
            )
        ]
    })

    # ADIM 72
    slides.append({
        "slideNumber": 72,
        "title": "Hemosiderin Morfolojisi: Işık Mikroskopisi ve Prusya Mavisi Boyası",
        "subtitle": "Kaba altın sarısı-kahverengi granüller ve Perls reaksiyonunun parlak mavisi",
        "badge": "Prusya Mavisi",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Işık mikroskobunda hematoksilen-eozin (H&E) ile boyanmış kesitlerde hemosiderin, sitoplazmada iri taneli, "
            "refraktil (ışığı kıran), altın sarısı ile pas kahverengisi arasında değişen parlak granüller olarak izlenir. "
            "Lipofusin daha ince taneli ve soluk iken, hemosiderin kaba, düzensiz ve parçacıklı bir yapıya sahiptir.\n\n"
            "> [SINAV SPOTU] Hemosiderin varlığını ve kimliğini kesinleştiren altın standart boya 'Prusya mavisi' "
            "(Prussian blue / Perls reaksiyonu) boyasıdır. Bu boyada hidroklorik asit ve potasyum ferrosiyanür "
            "demirle birleşerek parlak mavi (ferrosiyanür) çökelti oluşturur.\n\n"
            "Prusya mavisi boyaması hem hemosiderozun şiddetini derecelendirmede hem de lipofusin/melanin ayrımında vazgeçilmezdir."
        ),
        "medicalTerms": [
            {"term": "Prusya Mavisi (Perls)", "explanation": "Dokudaki ferrik demiri (Fe3+) potasyum ferrosiyanürle parlak mavi ferrosiyanür kompleksine çeviren histokimyasal boyadır."},
            {"term": "Refraktil Granül", "explanation": "Işık mikroskobunda optik yoğunluğu nedeniyle parıldayan partiküldür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hemosiderin Prusya mavisi ile masmavi boyanır.",
            "📌 [SINAV SPOTU] H&E'de kaba, refraktil altın sarısı-pas rengi granüllerdir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "H&E Görünümü", "desc": "Kaba, parlak altın-kahverengi refraktil partiküller.", "isKey": True},
                {"title": "Özel Boya", "desc": "Prusya mavisi (Perls) ile spesifik parlak mavi boyanma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Pigment", "H&E Işık Mikroskopisi", "Prusya Mavisi (Perls)", "Fontana-Masson"],
                [
                    [("Hemosiderin", False, ""), ("Kaba altın-pas kahverengi", False, ""), ("Pozitif (Masmavi)", True, "Demir içeren pigmentin spesifik reaksiyonu"), ("Negatif (Boyanmaz)", False, "")],
                    [("Lipofusin", False, ""), ("İnce altın sarısı-kahve", False, ""), ("Negatif (Boyanmaz)", True, "Demir içermeyen yaşlılık lipid pigmenti"), ("Negatif / Zayıf", False, "")],
                    [("Melanin", False, ""), ("Kahverengi-siyah ince", False, ""), ("Negatif (Boyanmaz)", False, ""), ("Pozitif (Simsiyah)", True, "Gümüşü indirgeyen UV pigmenti")]
                ]
            ),
            make_cloze(
                "Hemosiderin granülleri histokimyasal incelemede Prusya mavisi boyası ile parlak mavi renge boyanır.",
                "Prusya mavisi",
                "Demiri maviye boyayan klasik histokimyasal yöntem"
            )
        ]
    })

    # ADIM 73
    slides.append({
        "slideNumber": 73,
        "title": "Lokal Hemosideroz: Ekimoz (Çürük) Evrimi ve Hematom Rezorpsiyonu",
        "subtitle": "Kırmızıdan maviye, yeşile ve altın sarısına dönen kutanöz renk tayfı",
        "badge": "Lokal Hemosideroz",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Lokal hemosideroz, doku içine meydana gelen lokal kanamalarda (hematom, ekimoz/çürük) eritrositlerin "
            "parçalanması sonucu gelişen sınırlı demir depolanmasıdır. Travma sonrası damar dışına kaçan eritrositler "
            "doku makrofajları (histiositler) tarafından fagosite edilir. Makrofaj lizozomlarında hemoglobinin globini "
            "ayrılır, hem halkası 'hem oksijenaz' enzimi tarafından parçalanır.\n\n"
            "> [SINAV SPOTU] Hem halkasının açılmasıyla önce yeşil renkli 'biliverdin', ardından sarı-kırmızı renkli "
            "'bilirubin' oluşur; açığa çıkan demir ise ferritin ve hemosiderine dönüştürülerek altın sarısı-kahve rengi verir.\n\n"
            "Bir çürüğün günbegün mor-maviden yeşile, sarıya ve pas rengine dönüşmesi bu enzim basamaklarının görsel yansımasıdır."
        ),
        "medicalTerms": [
            {"term": "Ekimoz (Çürük)", "explanation": "Deri altına kan sızması sonucu gelişen ve hemoglobin yıkımıyla renk değiştiren lezyondur."},
            {"term": "Hem Oksijenaz", "explanation": "Hemoglobin hem halkasını parçalayarak biliverdin ve serbest demir açığa çıkaran enzimdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Çürükteki yeşil rengi biliverdin, altın sarısı-kahverengiyi hemosiderin verir.",
            "📌 [SINAV SPOTU] Lokal hemosideroz eski kanama odaklarının değişmez patolojik bulgusudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemoglobin Yıkımı", "desc": "Eritrosit fagositozu sonrası hem oksijenaz aktivasyonu.", "isKey": True},
                {"title": "Renk Skalası", "desc": "Kırmızı-mavi (Hb) -> Yeşil (Biliverdin) -> Sarı (Bilirubin) -> Pas (Hemosiderin).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Çürükte Hemoglobin Parçalanması ve Renk Döngüsü",
                [
                    "1. Damar Dışı Kanama: Eritrositler dokuya sızarak kırmızı-mor ekimoz alanını başlatır.",
                    "2. Makrofaj Fagositozu: Histiositler yaşlanan eritrositleri yutar ve lizozomda yıkar.",
                    "3. Biliverdin Oluşumu: Hem oksijenaz hem halkasını açarak yeşil renkli biliverdini üretir.",
                    "4. Bilirubin Redüksiyonu: Biliverdin redüktaz lezyona sarı rengi veren bilirubini oluşturur.",
                    "5. Hemosiderin Çöküşü: Ayrılan demir makrofajda toplanarak altın-pas renkli hemosiderini kurar."
                ]
            ),
            make_cloze(
                "Travma sonrası oluşan bir hematomda yeşil rengi veren hemoglobin yıkım ürünü biliverdin pigmentidir.",
                "biliverdin",
                "Hem halkasının açılmasıyla oluşan yeşil ara metabolit"
            )
        ]
    })

    # ADIM 74
    slides.append({
        "slideNumber": 74,
        "title": "Konjestif Kalp Yetersizliği ve Kalp Hata Hücreleri (Siderofajlar)",
        "subtitle": "Pulmoner venöz konjesyon, eritrosit diyapezi ve hemosiderin yüklü alveoler makrofajlar",
        "badge": "Kalp Hata Hücreleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Sol kalp yetersizliğinde sol ventrikül kanı aortaya pompalayamaz; sol atriyum ve pulmoner venlerde hidrostatik "
            "basınç aşırı yükselir. Bu durum akciğer kapillerlerinde kronik pasif konjesyona yol açar. Artan hidrostatik "
            "basınç nedeniyle eritrositler kapiller endotel aralıklarından alveol lümenine sızar (diapedez).\n\n"
            "> [SINAV SPOTU] Alveollere dökülen bu eritrositleri yutan alveoler makrofajlar sitoplazmalarını kaba "
            "hemosiderin granülleriyle doldurur; bu hücrelere 'kalp hata hücreleri' (heart failure cells / siderofajlar) denir.\n\n"
            "Akciğer parankimi zamanla kahverengi, sert ve fibrotik bir hal alır; bu patolojiye 'kahverengi endürasyon' adı verilir."
        ),
        "medicalTerms": [
            {"term": "Kalp Hata Hücresi (Siderofaj)", "explanation": "Kronik akciğer konjesyonunda alveole kaçan eritrositleri yutmuş hemosiderin dolu makrofajdır."},
            {"term": "Kahverengi Endürasyon", "explanation": "Kronik pasif konjesyonda hemosiderin birikimi ve fibrozisle sertleşmiş kahverengi akciğerdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kalp hata hücreleri kronik sol kalp yetmezliğinde alveollerdeki hemosiderinli makrofajlardır.",
            "📌 [SINAV SPOTU] Akciğerde hemosiderin ve fibrozis 'kahverengi endürasyon' oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemodinamik Neden", "desc": "Kronik pulmoner venöz konjesyon ve kapiller kaçak.", "isKey": True},
                {"title": "Tanısal Hücre", "desc": "Balgamda veya dokuda Prusya mavisi(+) kalp yetmezliği hücreleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Kronik sol kalp yetersizliği olan bir hastanın balgam yaymasında ve akciğer biyopsisinde alveol lümenlerinde altın sarısı-kahverengi kaba granüller içeren makrofajlar izleniyor. Prusya mavisi ile bu hücreler masmavi boyanıyor. Bu hücrelere patolojide verilen ad hangisidir?",
                {
                    "A": "Toz hücreleri (Dust cells)",
                    "B": "Kalp hata hücreleri (Siderofajlar)",
                    "C": "Köpük hücreler (Foam cells)",
                    "D": "Mott hücreleri",
                    "E": "Gaucher hücreleri"
                },
                "B",
                {
                    "A": "Toz hücreleri karbon yutan antrakotik makrofajlardır.",
                    "B": "Doğru! Hemosiderin yutan alveoler makrofajlara kalp hata hücreleri (siderofaj) denir.",
                    "C": "Köpük hücreler lipid yüklü makrofajlardır.",
                    "D": "Mott hücreleri Russell cisimcikli plazma hücreleridir.",
                    "E": "Gaucher hücreleri glukoserebrozid yüklü makrofajlardır."
                }
            ),
            make_cloze(
                "Kronik akciğer konjesyonunda alveollerde hemosiderin yutmuş makrofajlara kalp hata hücreleri adı verilir.",
                "kalp hata hücreleri",
                "Sol kalp yetmezliğinde akciğerdeki siderofajların adı"
            )
        ]
    })

    # ADIM 75
    slides.append({
        "slideNumber": 75,
        "title": "Sistemik Hemosideroz Etiyolojisi: Transfüzyon, Hemoliz ve Dağılım",
        "subtitle": "Kanda aşırı demir yükü ve retiküloendotelyal sistem makrofajlarının doyurulması",
        "badge": "Sistemik Hemosideroz",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Vücudun toplam demir yükünün fizyolojik sınırları aştığı durumlarda sistemik hemosideroz gelişir. "
            "En önemli nedenler: 1) Talasemi majör ve aplastik anemide tekrarlayan kan transfüzyonları (her ünite kan ~250 mg "
            "demir ekler ve vücudun fizyolojik demir atılım yolu yoktur), 2) Kronik intravasküler/ekstravasküler hemolitik "
            "anemiler, 3) Aşırı oral demir alımı.\n\n"
            "> [TEMEL İLKE] Erken sistemik hemosiderozda demir öncelikle retiküloendotelyal sistem (RES) makrofajlarında "
            "(dalak, kemik iliği ve karaciğer Kupffer hücrelerinde) birikir; bu evrede doku hasarı yoktur.\n\n"
            "Ancak RES kapasitesi taştığında demir hepatositler, pankreas ve kalp parankim hücrelerine sızmaya başlar."
        ),
        "medicalTerms": [
            {"term": "Sistemik Hemosideroz", "explanation": "Genel demir aşırı yükü sonucu organlarda yaygın hemosiderin depolanmasıdır."},
            {"term": "Retiküloendotelyal Sistem (RES)", "explanation": "Karaciğer (Kupffer), dalak, lenf nodu ve kemik iliği fagositer makrofaj ağıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Vücutta demiri aktif olarak dışarı atacak fizyolojik bir boşaltım mekanizması yoktur.",
            "📌 [SINAV SPOTU] Hemosideroz başlangıçta RES makrofajlarındadır; organ disfonksiyonu yapmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Demir Yükü Nedenleri", "desc": "Kronik kan transfüzyonları, orak hücre/talasemi hemolizi.", "isKey": True},
                {"title": "İlk Durak (RES)", "desc": "Dalak, kemik iliği ve Kupffer hücreleri demiri hapseder.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Lokal Hemosideroz vs Erken Sistemik Hemosideroz",
                "Lokal Hemosideroz",
                "Tek bir hematom veya konjesyon odağında lokal eritrosit yıkımıyla sınırlı makrofajik demir birikimidir.",
                "Sistemik Hemosideroz (Erken)",
                "Tüm vücutta aşırı demir yükü sonucu dalak, karaciğer Kupffer hücreleri ve kemik iliği makrofajlarında yaygın demir toplanmasıdır."
            ),
            make_active_recall(
                "Tekrarlayan kan transfüzyonu yapılan talasemi hastalarında erken dönemde hemosiderin öncelikle hangi hücrelerde birikir?",
                "Retiküloendotelyal sistemin fagositer makrofajlarında (Kupffer hücreleri, dalak ve kemik iliği makrofajlarında) birikir."
            )
        ]
    })

    # ADIM 76
    slides.append({
        "slideNumber": 76,
        "title": "Primer Hemokromatoz (HFE Mutasyonu) ve Hepasidin Eksikliği",
        "subtitle": "C282Y mutasyonu, ferroportin kapısının açık kalması ve kontrolsüz bağırsak emilimi",
        "badge": "Primer Hemokromatoz",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Herediter (primer) hemokromatoz, 6. kromozomdaki HFE geninde meydana gelen mutasyonlar (en sık C282Y ve "
            "H63D) sonucu gelişen otozomal resesif bir hastalıktır. HFE proteini hepatositlerde demir sensörü gibi "
            "çalışarak sistemik demir freni olan 'hepasidin' hormonunun üretimini düzenler.\n\n"
            "> [SINAV SPOTU] HFE mutasyonunda karaciğer hepasidin üretemez; hepasidin yokluğunda enterosit ve makrofaj "
            "zarındaki demir çıkış kapısı olan 'ferroportin' açık kalır ve kontrolsüz duodenal demir emilimi gerçekleşir.\n\n"
            "Vücut her gün 2-3 mg ekstra demir emer; 40-50 gramlık devasa toksik demir birikintileri parankim organlarına çöker."
        ),
        "medicalTerms": [
            {"term": "Herediter Hemokromatoz", "explanation": "HFE mutasyonuna bağlı hepasidin eksikliği ve aşırı bağırsak demir emilimi hastalığıdır."},
            {"term": "Hepasidin", "explanation": "Karaciğerde üretilen, ferroportini yıkarak demir emilimini ve salınımını durduran ana hormondur."},
            {"term": "Ferroportin", "explanation": "Hücre içindeki demiri kana veren tek hücresel demir ihraç kanalıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hemokromatozun temel moleküler defekti HFE gen mutasyonu (C282Y) ve hepasidin eksikliğidir.",
            "📌 [SINAV SPOTU] Hepasidin eksikliği duodenal demir emilimini kontrolsüz şekilde artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Genetik Kusur", "desc": "HFE C282Y homozigotluğu, hepasidin üretiminin baskılanması.", "isKey": True},
                {"title": "Ferroportin Açıklığı", "desc": "Bağırsaktan kana sınırsız demir geçişi ve organ parankim toksisitesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Primer Hemokromatozda Moleküler Patogenez",
                [
                    "1. HFE C282Y Mutasyonu: Hepatosit yüzeyinde mutant HFE demir sinyalini algılayamaz.",
                    "2. Hepasidin Çöküşü: Karaciğer dolaşıma yeterli hepasidin hormonu salgılayamaz.",
                    "3. Ferroportin Aktivasyonu: Bağırsak enterositlerindeki ferroportin kanalları parçalanmaz, açık kalır.",
                    "4. Kontrolsüz Emilim: Diyetle alınan demir sürekli kana boşaltılır.",
                    "5. Parankimal Hasar: Serbest demir hepatosit, pankreas ve kalpte Fenton reaksiyonuyla siroz ve yetmezlik yapar."
                ]
            ),
            make_cloze(
                "Herediter hemokromatozda karaciğerden salınımı bozularak bağırsak demir emiliminin kontrolsüz artmasına yol açan hormon hepasidin hormonudur.",
                "hepasidin",
                "Demir homeostazının karaciğer kökenli ana fren hormonu"
            )
        ]
    })

    # ADIM 77
    slides.append({
        "slideNumber": 77,
        "title": "Sekonder Hemokromatoz vs Hemosideroz: Doku Hasarı ve Fibrozis",
        "subtitle": "Kupffer hücre hapsinden parankimal hücre nekrozuna ve serbest radikal yangınına geçiş",
        "badge": "Hasar ve Toksisite",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Patolojide 'hemosideroz' ile 'hemokromatoz' kavramları arasındaki temel fark doku hasarı ve fibrozistir. "
            "Hemosiderozda demir retiküloendotelyal makrofajların içinde güvenle hapsolmuştur; hücre hasarı veya organ "
            "disfonksiyonu eşlik etmez. Ancak demir yükü parankimal hücrelere (hepatosit, adacık hücresi, miyosit) taştığında "
            "tablo hemokromatoza dönüşür.\n\n"
            "> [SINAV SPOTU] Parankim hücrelerindeki serbest demir Fenton reaksiyonu ile lipid peroksidasyonunu, DNA "
            "kırıklarını ve Ito hücre aktivasyonunu tetikleyerek parankim nekrozu ve ilerleyici fibrozis (siroz) yapar.\n\n"
            "Bu durum geri dönüşümlü bir birikintinin geri dönüşsüz organ yetmezliğine dönüştüğü kritik eşiktir."
        ),
        "medicalTerms": [
            {"term": "Fenton Reaksiyonu", "explanation": "Fe2+ iyonunun hidrojen peroksitle reaksiyona girerek aşırı toksik hidroksil radikali (OH•) üretmesidir."},
            {"term": "Pigmenter Siroz", "explanation": "Yoğun hemosiderin birikimi ve yaygın fibrozisle nodüllere ayrılmış karaciğer sirozudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hemosiderozda organ hasarı yoktur; hemokromatozda parankim ölümü ve fibrozis vardır.",
            "📌 [SINAV SPOTU] Demir toksisitesinin temel mekanizması Fenton reaksiyonu kaynaklı lipid peroksidasyonudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemosideroz", "desc": "RES makrofajlarında birikir, hasar ve fibrozis yapmaz.", "isKey": True},
                {"title": "Hemokromatoz", "desc": "Parankimde birikir, serbest radikallerle siroz ve yetmezlik yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Hemosideroz vs Hemokromatoz",
                "Hemosideroz",
                "Demir öncelikle Kupffer hücrelerinde ve dalak makrofajlarında birikir; parankim hasarı ve fibrozis izlenmez.",
                "Hemokromatoz",
                "Demir hepatositler, kalp kası ve pankreas parankiminde birikir; Fenton reaksiyonuyla siroz, diyabet ve kalp yetmezliği yapar."
            ),
            make_active_recall(
                "Patolojide hemosideroz terimi ile hemokromatoz terimi arasındaki en temel fonksiyonel ve yapısal fark nedir?",
                "Hemosiderozda demir makrofajlarda toplanır ve organ hasarı/fibrozis yapmaz; hemokromatozda ise demir parankim hücrelerini zedeleyerek fibrozis ve organ yetmezliğine yol açar."
            )
        ]
    })

    # ADIM 78
    slides.append({
        "slideNumber": 78,
        "title": "Bronz Diyabet Triadı: Pigmenter Siroz, Deri ve Endokrin Yıkım",
        "subtitle": "Klinik triat: Karaciğer sirozu, diabetes mellitus ve bronz ten hiperpigmentasyonu",
        "badge": "Bronz Diyabet",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "İlerlemiş hemokromatozun klasik klinik tablosu 'bronz diyabet' (bronze diabetes) olarak bilinir ve meşhur "
            "bir klinik triad ile tanımlanır: 1) Mikronodüler pigmenter karaciğer sirozu (hepatomegali ve karaciğer yetmezliği), "
            "2) Pankreas adacık hücrelerinin demirle tahrip olması sonucu gelişen diabetes mellitus, 3) Deride dermal hemosiderin "
            "birikimi ve uyarılmış melanin sentezi sonucu cildin bronz/gri-kahverengi renk alması.\n\n"
            "> [SINAV SPOTU] Ayrıca kardiyak tutulum (aritmi ve dilate kardiyomiyopati), eklemlerde kalsiyum pirofosfat "
            "çökmesi (psödogut) ve gonadal atrofi (testis atrofisi/libido kaybı) eşlik eder.\n\n"
            "Hemokromatozlu hastalarda hepatosellüler karsinom (HCC) riski normal popülasyona göre 200 kat artmıştır."
        ),
        "medicalTerms": [
            {"term": "Bronz Diyabet", "explanation": "Hemokromatozda pigmenter siroz, endokrin pankreas harabiyeti ve deri hiperpigmentasyonu triadıdır."},
            {"term": "HCC Riski", "explanation": "Hemokromatoz sirozunda karaciğer kanseri gelişme riskinin 200 kat artmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Bronz diyabet triadı = Pigmenter siroz + Diabetes mellitus + Deride bronz pigmentasyon.",
            "📌 [SINAV SPOTU] Hemokromatoz hastalarında hepatosellüler karsinom riski 200 kat yüksektir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Klasik Triad", "desc": "Siroz, diyabet ve deride bronzlaşma.", "isKey": True},
                {"title": "Malignite Tehdidi", "desc": "Primer karaciğer kanseri (HCC) için devasa risk artışı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "52 yaşında bir erkek hasta halsizlik, karında şişlik, yeni başlayan şeker hastalığı ve cildinde koyulaşma (bronzlaşma) şikayetleriyle başvuruyor. Muayenede hepatomegali ve testis atrofisi saptanıyor. Karaciğer biyopsisinde hepatositlerde yoğun Prusya mavisi(+) granüller ve mikronodüler siroz görülüyor. Bu hastanın klinik tablosu aşağıdakilerden hangisidir?",
                {
                    "A": "Wilson hastalığı",
                    "B": "Herediter hemokromatoz (Bronz diyabet)",
                    "C": "α1-Antitripsin eksikliği",
                    "D": "Gaucher hastalığı",
                    "E": "Primer biliyer kolanjit"
                },
                "B",
                {
                    "A": "Wilson hastalığında bakır birikir ve Kayser-Fleischer halkası görülür.",
                    "B": "Doğru! Pigmenter siroz, diyabet ve bronz ten klasik hemokromatoz (bronz diyabet) triadıdır.",
                    "C": "AAT eksikliğinde akciğer amfizemi ve PAS(+) granüller izlenir.",
                    "D": "Gaucher hastalığında glukoserebrozid birikir.",
                    "E": "Primer biliyer kolanjitte safra kanalları granülomlarla yıkılır."
                }
            ),
            make_cloze(
                "Hemokromatozda siroz, diyabet ve ciltte bronzlaşma birlikteliğine bronz diyabet adı verilir.",
                "bronz diyabet",
                "İlerlemiş hemokromatozun klasik klinik triadının adı"
            )
        ]
    })

    # ADIM 79 - CHECKPOINT 8
    slides.append({
        "slideNumber": 79,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Hemosiderin ve Hemokromatoz",
        "subtitle": "Demir birikimi, Perls boyası, kalp hata hücreleri ve HFE mutasyonunun sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 8,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında demir metabolizması ve patolojik birikintilerini sentezliyoruz. 1) Hemosiderin: "
            "Aşırı ferritinin lizozomlarda agregat oluşturmasıdır; kaba refraktil pas rengidir, Prusya mavisi (Perls) ile "
            "masmavi boyanır. 2) Lokal hemosideroz: Çürüklerde biliverdin (yeşil), bilirubin (sarı) ve hemosiderin oluşumu; "
            "kronik sol kalp yetmezliğinde alveollerde kalp hata hücreleri (siderofajlar). 3) Sistemik hemosideroz: "
            "Transfüzyon veya hemolizle RES makrofajlarında birikir (hasarsız). 4) Hemokromatoz: HFE (C282Y) mutasyonu, "
            "hepasidin düşüklüğü, parankimde birikim, Fenton hasarı ve bronz diyabet.\n\n"
            "> [KLİNİK İPUCU] Sınavda Prusya mavisi pozitifliği daima demir/hemosiderini kanıtlar.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle inceleyiniz."
        ),
        "medicalTerms": [
            {"term": "Perls Reaksiyonu", "explanation": "Hemosiderin tanısında kullanılan histokimyasal Prusya mavisi yöntemidir."},
            {"term": "Siderofaj", "explanation": "Akciğer veya dokuda hemosiderin fagosite etmiş makrofajdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hemosiderin = Prusya mavisi pozitif altın-pas rengi granül.",
            "📌 [SINAV SPOTU] Kalp hata hücresi = Sol kalp yetmezliğinde alveoler siderofaj.",
            "📌 [SINAV SPOTU] HFE mutasyonu = Hepasidin yokluğu, kontrolsüz demir emilimi, bronz diyabet."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Histokimya", "desc": "Prusya mavisi ile parlak mavi renk reaksiyonu.", "isKey": True},
                {"title": "Lokal Model", "desc": "Hematom rezorpsiyonu ve kalp hata hücreleri.", "isKey": True},
                {"title": "Sistemik Model", "desc": "Transfüzyonel hemosideroz vs genetik hemokromatoz.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-22",
                "Hemosiderin pigmentini lipofusin ve melaninden ayıran en temel histokimyasal reaksiyon nedir?",
                "Prusya mavisi (Perls) boyası ile parlak mavi renge boyanmasıdır; lipofusin ve melanin bu boyayla boyanmaz.",
                "Prusya mavisi boyaması ve demir ayrımı"
            ),
            make_flashcard(
                "k1-07-fc-23",
                "Kronik sol kalp yetmezliğinde akciğer alveollerinde izlenen 'kalp hata hücreleri' (siderofajlar) ne içerir?",
                "Alveol lümenine sızan eritrositlerin fagositozu sonucu sitoplazmada biriken kaba hemosiderin granülleri içerir.",
                "Pulmoner konjesyon ve hemosiderinli makrofajlar"
            ),
            make_flashcard(
                "k1-07-fc-24",
                "Primer herediter hemokromatozda kontrolsüz demir emiliminden sorumlu temel hormonal defekt nedir?",
                "HFE mutasyonuna bağlı olarak karaciğerden hepasidin hormonunun yeterli üretilememesi ve enterosit ferroportin kanallarının sürekli açık kalmasıdır.",
                "Hepasidin eksikliği ve ferroportin kapısı"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Herediter hemokromatoz hastalarında karaciğer parankiminde gelişen malign tümör riski hepatosellüler karsinom riskidir.",
                "hepatosellüler karsinom",
                "Siroz zemininde 200 kat artan primer karaciğer kanseri"
            )
        ]
    })

    # ADIM 80
    slides.append({
        "slideNumber": 80,
        "title": "Demir Aşırı Yükünün Klinik Yönetimi ve Tedavi Prensipleri",
        "subtitle": "Terapötik flebotomi, şelasyon ajanları (deferoksamin) ve organ koruma",
        "badge": "Tedavi Yönetimi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Demir aşırı yükü erken saptandığında organ hasarı gelişmeden tedavi edilebilen bir hastalıktır. Herediter "
            "hemokromatozda en basit ve en etkili hayat kurtarıcı tedavi haftalık veya iki haftada bir yapılan düzenli "
            "'terapötik flebotomidir' (kan alma; her 500 mL kanda ~250 mg demir uzaklaştırılır). Flebotomi ile vücut "
            "demir depoları güvenli sınırlara (ferritin < 50 ng/mL) çekilir.\n\n"
            "> [KLİNİK İPUCU] Tekrarlayan transfüzyonlara bağlı anemik hastalarda (talasemi) kan almak anemi nedeniyle "
            "mümkün olmadığından, demiri bağlayıp idrar/safra ile atan demir şelatörleri (deferoksamin, deferasiroks) kullanılır.\n\n"
            "Siroz gelişmeden önce tedaviye başlanan hastaların yaşam beklentisi normal popülasyonla farksızdır."
        ),
        "medicalTerms": [
            {"term": "Terapötik Flebotomi", "explanation": "Vücuttan fazla demiri uzaklaştırmak amacıyla düzenli kan alma işlemidir."},
            {"term": "Demir Şelasyonu", "explanation": "Serbest ve depo demiri bağlayarak böbrek/safra yoluyla atılmasını sağlayan ilaç tedavisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hemokromatozda altın standart tedavi terapötik flebotomidir.",
            "📌 [SINAV SPOTU] Anemik transfüzyonel hemosiderozda flebotomi yapılamaz; şelasyon tedavisi verilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemokromatoz Tedavisi", "desc": "Düzenli flebotomi ile ferritin ve demir düzeyini sıfırlama.", "isKey": True},
                {"title": "Şelasyon Tedavisi", "desc": "Talasemik transfüzyon hastalarında deferoksamin kullanımı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Talasemi majör tanısıyla çocukluğundan beri ayda 2 ünite eritrosit süspansiyonu alan 18 yaşında bir hastada serum ferritini 3500 ng/mL bulunuyor. Hastada kardiyak ve hepatik demir toksisitesini önlemek için en uygun yaklaşım hangisidir?",
                [
                    {
                        "text": "Haftalık terapötik flebotomi ile 500 mL kan alınmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış! Ağır anemisi olan talasemi hastasından kan alınamaz, anemi krizi ve ölüm tetiklenir."
                    },
                    {
                        "text": "Düzenli demir şelasyon tedavisi (deferasiroks / deferoksamin) başlanmalıdır.",
                        "isCorrect": True,
                        "feedback": "Mükemmel! Transfüzyonel demir yükü olan anemik hastalarda kan alınamaz; demir şelatörleri verilmelidir."
                    }
                ]
            ),
            make_active_recall(
                "Primer hemokromatoz ile transfüzyonel hemosiderozun tedavi stratejileri arasındaki en temel fark nedir?",
                "Primer hemokromatozda anemi olmadığı için düzenli kan alma (flebotomi) yapılırken; transfüzyonel hemosiderozda altta yatan anemi nedeniyle kan alınamaz, demir şelatörleri kullanılır."
            )
        ]
    })

    return slides
