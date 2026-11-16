"""
Bölüm 9: Patolojik Kalsifikasyon: Distrofik vs Metastatik Kalsifikasyon Mekanizmaları
Adımlar: 81 - 90
Checkpoint: Adım 89 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # ADIM 81
    slides.append({
        "slideNumber": 81,
        "title": "Patolojik Kalsifikasyon Kavramı ve İki Temel Formun Tanımı",
        "subtitle": "Kemik ve diş dışındaki yumuşak dokularda anormal kalsiyum tuzu çökelmesi",
        "badge": "Kalsifikasyon Giriş",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Patolojik kalsifikasyon, kemik ve diş gibi fizyolojik olarak mineralize dokular haricinde, vücudun yumuşak "
            "dokularında anormal miktarda kalsiyum tuzlarının (beraberinde az miktarda demir, magnezyum ve diğer minerallerle "
            "birlikte) çökelmesi durumudur. Bu mineral birikintileri genellikle kalsiyum fosfat kristalleri (hidroksiapatit) "
            "formundadır.\n\n"
            "> [TEMEL İLKE] Patolojik kalsifikasyon serum kalsiyum düzeyi ve tutulan dokunun canlılık durumuna göre iki "
            "temel forma ayrılır: Distrofik kalsifikasyon ve Metastatik kalsifikasyon.\n\n"
            "Bazı durumlarda kalsifikasyon yalnızca eski bir hasarın zararsız bir 'radyolojik izi' iken, bazen organ "
            "lümenini tıkayarak veya kapak hareketini durdurarak ölümcül yetmezliklere yol açar."
        ),
        "medicalTerms": [
            {"term": "Patolojik Kalsifikasyon", "explanation": "Yumuşak dokularda anormal kalsiyum tuzu çökelmesiyle giden mineralizasyon patolojisidir."},
            {"term": "Hidroksiapatit", "explanation": "Kalsiyum ve fosfatın oluşturduğu kemik benzeri kristal mineral yapısıdır [Ca10(PO4)6(OH)2]."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Patolojik kalsifikasyon hidroksiapatit kalsiyum tuzlarının birikimidir.",
            "📌 [SINAV SPOTU] İki tipi vardır: Distrofik (hasarlı doku) ve Metastatik (hiperkalsemi)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mineral Çökmesi", "desc": "Yumuşak dokularda kalsiyum fosfat tuzlarının kristalizasyonu.", "isKey": True},
                {"title": "İki Ayrı Yol", "desc": "Lokal nekroz odakları (distrofik) vs Sistemik hiperkalsemi (metastatik).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Yumuşak dokularda anormal kalsiyum tuzu birikmesi durumuna patolojik kalsifikasyon adı verilir.",
                "patolojik kalsifikasyon",
                "Kemik dışı yumuşak dokularda kalsiyum çökmesini niteleyen kavram"
            ),
            make_active_recall(
                "Patolojik kalsifikasyonun iki temel klinik formu hangileridir?",
                "Distrofik kalsifikasyon ve metastatik kalsifikasyondur."
            )
        ]
    })

    # ADIM 82
    slides.append({
        "slideNumber": 82,
        "title": "Distrofik Kalsifikasyon: Serum Kalsiyumu Normal, Doku Hasarlı",
        "subtitle": "Sistemik kalsiyum homeostazının korunduğu nekroz zemininde mineralizasyon",
        "badge": "Distrofik Tanım",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Distrofik kalsifikasyon, serum kalsiyum düzeylerinin ve genel kalsiyum metabolizmasının tamamen normal "
            "olduğu bireylerde, yalnızca ölü, dejenere veya nekrotik dokularda meydana gelen lokal kalsiyum çökelmesidir. "
            "Burada itici güç kandaki kalsiyum yüksekliği değil, hasarlı dokunun bizzat kendisinde oluşan mikro-çevresel "
            "değişikliklerdir.\n\n"
            "> [SINAV SPOTU] Distrofik kalsifikasyonda serum kalsiyumu kesinlikle normaldir; birikim nekroz (koagülatif, "
            "kazeöz, likefaksiyon, yağ nekrozu) veya ileri derecede aterosklerotik dokularda gelişir.\n\n"
            "Dokunun pH'sındaki lokal kaymalar ve açığa çıkan fosfat iyonları kalsiyumun çökelmesini başlatır."
        ),
        "medicalTerms": [
            {"term": "Distrofik Kalsifikasyon", "explanation": "Serum kalsiyumu normalken hasarlı/nekrotik dokuda gelişen lokal mineralizasyondur."},
            {"term": "Normokalsemi", "explanation": "Kanda serum total ve iyonize kalsiyum düzeylerinin fizyolojik sınırlarda olmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Distrofik kalsifikasyonda serum kalsiyum düzeyi tamamen normaldir.",
            "📌 [SINAV SPOTU] Birikim daima hasarlı, nekrotik veya yaşlanmış dokularda meydana gelir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Serum Ca", "desc": "Kesinlikle normal sınırlardadır (normokalsemi).", "isKey": True},
                {"title": "Hedef Dokular", "desc": "Enfarkt alanları, tüberküloz kazeöz odakları, aterom plakları, yaşlı kapaklar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Distrofik kalsifikasyonda serum kalsiyum düzeyi tamamen normal sınırlardadır.",
                "normal",
                "Distrofik kalsifikasyondaki serum kalsiyum düzeyinin durumu"
            ),
            make_active_recall(
                "Distrofik kalsifikasyonu metastatik kalsifikasyondan ayıran en temel biyokimyasal ve dokusal kriter nedir?",
                "Distrofik kalsifikasyonda serum kalsiyumu normaldir ve birikim sadece hasarlı/nekrotik dokularda olur; metastatik kalsifikasyonda ise serum kalsiyumu yüksektir (hiperkalsemi) ve normal dokularda birikir."
            )
        ]
    })

    # ADIM 83
    slides.append({
        "slideNumber": 83,
        "title": "Distrofik Kalsifikasyonun İntraselüler Başlangıcı: Mitokondriler",
        "subtitle": "Membran geçirgenlik geçişi, kalsiyum göllenmesi ve kristal çekirdeklenmesi",
        "badge": "Mitokondriyal Başlangıç",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Distrofik kalsifikasyonun moleküler mekanizması iki fazda incelenir: çekirdeklenme (başlatma) ve kristal "
            "yayılması. İntraselüler çekirdeklenmenin en kritik başlangıç noktası nekrotik hücrelerin mitokondrileridir. "
            "Hücre ölüm sürecinde plazma membranı delindiğinde hücre dışındaki yüksek kalsiyum sitozole boşalır.\n\n"
            "> [SINAV SPOTU] Sitoplazmik kalsiyum yükü karşısında mitokondri kalsiyum uniporterı çalışarak Ca2+'yi "
            "mitokondri matriksine pompalar; matriksteki inorganik fosfatla birleşen kalsiyum ilk kristal çekirdeklerini "
            "(nükleus) oluşturur.\n\n"
            "Bu mitokondriyal kristal odakları hücre parçalandığında çevre dokuya saçılarak kalsifikasyon odağını büyütür."
        ),
        "medicalTerms": [
            {"term": "Kristal Çekirdeklenmesi (İnitiation)", "explanation": "Kalsiyum ve fosfat iyonlarının bir araya gelerek ilk mikroskobik kristal odağını kurmasıdır."},
            {"term": "Mitokondriyal Kalsifikasyon", "explanation": "Nekrotik hücre matriksinde Ca2+ ve PO4'ün ilk kristalize olduğu organel içi başlangıçtır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Distrofik kalsifikasyonun intraselüler başlangıç yeri nekrotik hücre mitokondrileridir.",
            "📌 [SINAV SPOTU] Mitokondride kalsiyum fosfat çökmesi kristal çekirdeğini (nidus) oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücre İçi Nidus", "desc": "Nekrotik hücrelerin mitokondri matriksi.", "isKey": True},
                {"title": "İyon Çöküşü", "desc": "Matriksteki aşırı Ca2+ ve PO4 hidroksiapatit tohumlarını atar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Distrofik kalsifikasyon sürecinde kristal çekirdeklenmesinin (initiation) intraselüler olarak başladığı temel organel aşağıdakilerden hangisidir?",
                {
                    "A": "Granüllü endoplazmik retikulum",
                    "B": "Nekrotik hücrelerin mitokondrileri",
                    "C": "Golgi aygıtı sisternaları",
                    "D": "Peroksizomlar",
                    "E": "Sentrozom mikrotübülleri"
                },
                "B",
                {
                    "A": "Granüllü ER protein sentezler, kristal çekirdeklenmesinin primer organeli değildir.",
                    "B": "Doğru! Distrofik kalsifikasyon hücre içinde nekrotik hücre mitokondrilerinde başlar.",
                    "C": "Golgi glikozilasyon yapar.",
                    "D": "Peroksizom hidrojen peroksit metabolizması yürütür.",
                    "E": "Sentrozom hücre bölünmesini yönetir."
                }
            ),
            make_cloze(
                "Distrofik kalsifikasyonun intraselüler başlangıç odağı nekrotik hücrelerin mitokondrileri olarak tanımlanır.",
                "mitokondrileri",
                "Kalsiyum ve fosfatın ilk çöktüğü hücre içi organel"
            )
        ]
    })

    # ADIM 84
    slides.append({
        "slideNumber": 84,
        "title": "Ekstraselüler Başlangıç: Membran Vezikülleri ve Hidroksiapatit",
        "subtitle": "Membran fosfatidilserini, alkalen fosfataz aktivitesi ve kristal yayılımı",
        "badge": "Ekstraselüler Nidus",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Distrofik kalsifikasyonun ekstraselüler çekirdeklenmesi ise parçalanan ölü hücrelerin membranlarından "
            "kopan mikroskobik veziküllerde (matriks vezikülleri) başlar. Dejenerasyonla birlikte hücre membranındaki "
            "asidik fosfolipidler (özellikle fosfatidilserin) kalsiyum iyonlarını mıknatıs gibi yüzeyine bağlar.\n\n"
            "> [YÜKSEK VERİM] Vezikül zarında yerleşik membran fosfatazları (alkalen fosfataz) fosfat esterlerini "
            "parçalayarak lokal inorganik fosfat konsantrasyonunu aşırı artırır; kalsiyum ve fosfat birleşerek "
            "hidroksiapatit kristallerini oluşturur.\n\n"
            "Oluşan kristaller vezikül zarını delerek dışarı taşar, komşu kollajen lifleri üzerine yayılır ve birleşerek "
            "makroskopik sert taş kitlelerine dönüşür."
        ),
        "medicalTerms": [
            {"term": "Matriks Vezikülü", "explanation": "Nekrotik hücre zarından kopan ve yüzeyinde kalsiyum-fosfat kristalleri başlatan membran parçacığıdır."},
            {"term": "Fosfatidilserin", "explanation": "Kalsiyum iyonlarını elektrostatik olarak bağlayan negatif yüklü membran fosfolipididir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ekstraselüler başlangıç yeri hasarlı membranlardan kopan veziküllerdir.",
            "📌 [SINAV SPOTU] Membran fosfatazları lokal fosfatı artırarak hidroksiapatit kristalizasyonunu besler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücre Dışı Nidus", "desc": "Parçalanan hücre zar vezikülleri (matriks vezikülleri).", "isKey": True},
                {"title": "Kristal Büyümesi", "desc": "Hidroksiapatit kristalleri birleşerek makroskopik kalsiyum birikintisi yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Distrofik Kalsifikasyonun İki Fazlı Oluşum Mekanizması",
                [
                    "1. Membran Hasarı: Nekrotik hücrelerden fosfatidilserin zengini membran vezikülleri kopar.",
                    "2. İyon Bağlanması: Asidik fosfolipidler Ca2+ iyonlarını bağlar; alkalen fosfataz PO4 açığa çıkarır.",
                    "3. Çekirdeklenme (Nidus): Mitokondri içinde ve vezikül yüzeyinde ilk kalsiyum fosfat kristalleri çöker.",
                    "4. Kristal Yayılması: Kristaller vezikül zarını aşarak kollajen fibrilleri üzerine ekstraselüler yayılır.",
                    "5. Makroskopik Taşlaşma: Kristaller birleşerek sert, ufalanan beyaz tebeşirsi kalsifikasyon odaklarını oluşturur."
                ]
            ),
            make_cloze(
                "Distrofik kalsifikasyonun hücre dışı başlangıç odakları parçalanan hücre membranlarından kopan veziküllerdir.",
                "veziküllerdir",
                "Hücre dışı çekirdeklenmeyi başlatan membran parçacıkları"
            )
        ]
    })

    # ADIM 85
    slides.append({
        "slideNumber": 85,
        "title": "Kalsifiye Kalp Kapakları: Senil Aort Stenozu ve Romatizmal Mitral",
        "subtitle": "Mekanik hemodinamik stres, kronik inflamasyon ve kapak hareketinin kilitlenmesi",
        "badge": "Kapak Kalsifikasyonu",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Distrofik kalsifikasyonun en sık ve klinik olarak en tehlikeli örneklerinden biri yaşlılarda görülen "
            "'kalsifik aort stenozu'dur. Aort kapağı her kalp atımında muazzam bir mekanik sürtünme ve bükülme stresine "
            "maruz kalır. Yıllar içinde kapak fibroblastları ve interstisyel hücreleri hasarlanır, apoptoza uğrar ve "
            "lipid birikimiyle birlikte distrofik kalsifikasyon başlar.\n\n"
            "> [SINAV SPOTU] Aort kapak kuspislerinin Valsalva sinüslerine bakan yüzeylerinde sert, taş benzeri kalsifiye "
            "nodüller gelişir; kapak yaprakçıkları rijit hale gelerek açılamaz ve ileri derecede sol ventrikül hipertrofisi/yetmezliği gelişir.\n\n"
            "Geçirilmiş akut romatizmal ateş sonrası mitral kapakta gelişen kalsifikasyon da benzer mekanizmayla kapak darlığı yapar."
        ),
        "medicalTerms": [
            {"term": "Kalsifik Aort Stenozu", "explanation": "Yaşlanma ve mekanik stresle aort kapağında distrofik kalsiyum nodülleri gelişip kapağı daraltmasıdır."},
            {"term": "Kuspis Rijiditesi", "explanation": "Kapak yaprakçıklarının kalsiyumla taşlaşarak esnekliğini ve açılma yetisini kaybetmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Senil aort stenozu distrofik kalsifikasyonun klasik bir örneğidir.",
            "📌 [SINAV SPOTU] Kalsifikasyon kapağın serbest kenarında değil, tabanında ve Valsalva sinüsü komşuluğunda başlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mekanik Travma", "desc": "Ömür boyu süren hemodinamik çarpma kapak hücrelerini öldürür.", "isKey": True},
                {"title": "Klinik Çıktı", "desc": "Sertleşen kapak açılmaz, aort stenozu ve senkop/kalp yetersizliği yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Normal Aort Kapağı vs Kalsifik Aort Stenozu",
                "Normal Aort Kapağı",
                "İnce, yarı saydam, esnek ve sistolde sonuna kadar açılarak kanın rahatça geçmesine izin veren üç kuspisli kapak.",
                "Kalsifik Aort Stenozu (Distrofik)",
                "Taş gibi sert kalsiyum nodülleriyle kalınlaşmış, hareketsizleşmiş ve lümeni daraltan rijit kuspis yapısı."
            ),
            make_active_recall(
                "Yaşlı bireylerde senil kalsifik aort stenozu gelişiminde rol oynayan temel kalsifikasyon tipi ve serum kalsiyum durumu nedir?",
                "Distrofik kalsifikasyondur ve hastaların serum kalsiyum düzeyleri tamamen normaldir."
            )
        ]
    })

    # ADIM 86
    slides.append({
        "slideNumber": 86,
        "title": "Aterosklerotik Plaklarda Kalsifikasyon ve Damar Sertliği (Rijidite)",
        "subtitle": "Nekrotik köpük hücre artıklarında mineralizasyon ve damar frajilitesi",
        "badge": "Plak Kalsifikasyonu",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "İlerlemiş aterosklerotik plakların nekrotik çekirdeğinde ölen köpük makrofajlar ve düz kas hücreleri "
            "büyük miktarda membranöz döküntü bırakır. Bu nekrotik debris tam anlamıyla bir distrofik kalsifikasyon "
            "odağıdır. Zamanla kalsiyum tuzları birikerek plağın içindeki yumuşak lipid göletini taşlaşmış bir tabakaya dönüştürür.\n\n"
            "> [YÜKSEK VERİM] Aort ve koroner arterlerde plak kalsifikasyonu damar duvarının esnekliğini tamamen yok eder, "
            "damarı kırılganlaştırır ve anevrizma veya rüptür riskini artırır.\n\n"
            "Kardiyolojide kullanılan koroner arter kalsiyum (CAC) skoru, koronerlerdeki bu distrofik kalsifikasyonu "
            "ölçerek aterosklerotik plak yükünü doğrudan yansıtır."
        ),
        "medicalTerms": [
            {"term": "Plak Kalsifikasyonu", "explanation": "Aterom plağının nekrotik merkezinde gelişen distrofik hidroksiapatit mineralizasyonudur."},
            {"term": "Koroner Kalsiyum Skoru (CAC)", "explanation": "BT ile koroner arterlerdeki distrofik kalsiyum miktarını ölçen kardiyak risk belirtecidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Aterosklerotik plak kalsifikasyonu distrofik kalsifikasyonun klasik prototipidir.",
            "📌 [SINAV SPOTU] Damar duvarındaki kalsifikasyon damarın esnekliğini azaltıp frajilitesini artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Nekrotik Nidus", "desc": "Ölen köpük hücrelerin parçalanmış membran vezikülleri.", "isKey": True},
                {"title": "Damar Sertliği", "desc": "Elastikiyet kaybı, lümen daralması ve trombüs riski.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "İlerlemiş aterosklerotik plaklarda nekrotik hücre artıklarının üzerinde distrofik kalsifikasyon gelişir.",
                "distrofik kalsifikasyon",
                "Plakta serum kalsiyumu normalken gelişen taşlaşma süreci"
            ),
            make_active_recall(
                "Koroner arter kalsiyum (CAC) skorlamasında bilgisayarlı tomografi ile görüntülenen kalsiyum birikiminin patolojik tipi nedir?",
                "Distrofik kalsifikasyondur (ateromatöz plakların nekrotik çekirdeğindeki mineralizasyon)."
            )
        ]
    })

    # ADIM 87
    slides.append({
        "slideNumber": 87,
        "title": "Tüberküloz Lenf Düğümlerinde ve Kazeöz Odaklarda Taşlaşma",
        "subtitle": "Kazeöz nekrozun distrofik kalsifikasyonu ve Ghon kompleksinin kireçlenmesi",
        "badge": "Ghon Kompleksi",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Mycobacterium tuberculosis enfeksiyonunda granülom merkezinde meydana gelen kazeöz nekroz, hücresel "
            "çatının silindiği amorf lipopolisakkarit ve protein kalıntılarından oluşur. Tüberküloz lezyonları iyileşirken "
            "veya sınırlandırılırken bu kazeöz kütle yoğun şekilde distrofik kalsifikasyona uğrar.\n\n"
            "> [SINAV SPOTU] Akciğer parankimindeki kalsifiye tüberküloz odağı ile drene eden kalsifiye hiler lenf "
            "düğümünün birlikteliğine 'Ranke kompleksi' (kalsifiye Ghon kompleksi) adı verilir.\n\n"
            "Radyolojide akciğer grafilerinde tesadüfen saptanan tebeşir beyazı yuvarlak kalsifiye nodüller, hastanın "
            "yıllar önce geçirdiği ve kalsifikasyonla hapsedilmiş tüberküloz odaklarıdır."
        ),
        "medicalTerms": [
            {"term": "Ghon Odağı", "explanation": "Akciğer subplevral parankiminde gelişen primer tüberküloz granülom odağıdır."},
            {"term": "Ranke Kompleksi", "explanation": "Kalsifiye olmuş Ghon odağı ve kalsifiye hiler lenf nodunun oluşturduğu radyolojik komplekstir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tüberküloz lenf düğümlerinde kazeöz nekroz distrofik kalsifikasyonla taşlaşır.",
            "📌 [SINAV SPOTU] Ranke kompleksi kalsifiye tüberküloz lezyonunun radyolojik adıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kazeöz Zemin", "desc": "Amorf peynirimsi nekroz kalıntıları kalsiyum kristalleriyle dolar.", "isKey": True},
                {"title": "Kalıcı İz", "desc": "Radyolojide radyoopak beyaz lezyon olarak ömür boyu kalır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Akciğer tüberkülozu geçirmiş bir hastanın rutin göğüs radyografisinde akciğer orta zonunda ve hiler lenf düğümünde radyoopak (kemik yoğunluğunda) sert nodüller izleniyor (Ranke kompleksi). Biyopside kazeöz nekroz kalıntılarında kalsiyum tuzları saptanıyor. Hastanın serum kalsiyum düzeyi normal bulunuyor. Bu kalsifikasyon tipi hangisidir?",
                {
                    "A": "Metastatik kalsifikasyon",
                    "B": "Distrofik kalsifikasyon",
                    "C": "Psödogut kalsifikasyonu",
                    "D": "Kalsifilaksi",
                    "E": "Tümöral kalsinozis"
                },
                "B",
                {
                    "A": "Metastatik kalsifikasyonda hiperkalsemi şarttır ve normal dokularda olur.",
                    "B": "Doğru! Kazeöz nekroz odağında serum Ca normalken gelişen kalsifikasyon distrofik kalsifikasyondur.",
                    "C": "Psödogut eklem kıkırdağında pirofosfat birikimidir.",
                    "D": "Kalsifilaksi üremide damar kalsifikasyonudur.",
                    "E": "Tümöral kalsinozis periartiküler genetik fosfat metabolizma hastalığıdır."
                }
            ),
            make_cloze(
                "Akciğer tüberkülozunda kazeöz nekroz odaklarının distrofik kalsifikasyonu ile kireçlenmiş Ranke kompleksi meydana gelir.",
                "Ranke kompleksi",
                "Kalsifiye Ghon odağı ve hiler lenf bezinin oluşturduğu radyolojik yapı"
            )
        ]
    })

    # ADIM 88
    slides.append({
        "slideNumber": 88,
        "title": "Psammom Cisimcikleri (Psammoma Bodies): Tümöral Distrofik Çökelme",
        "subtitle": "Konsantrik lameller kalsiyum küreleri ve görüldüğü karakteristik tümörler",
        "badge": "Psammom Cisimcikleri",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Psammom cisimcikleri (psammoma bodies / kum cisimcikleri), histopatolojik kesitlerde konsantrik lameller "
            "(ağaç kütüğü halkaları veya soğan zarı gibi iç içe geçmiş katmanlar) halinde dizilmiş, yuvarlak, bazofilik "
            "(mor-mavi) distrofik kalsifikasyon odaklarıdır. Tek bir nekrotik tümör hücresinin membranı üzerinde "
            "başlayan kalsiyum fosfat çökmesi, katman katman dışa doğru büyüyerek bu lameller küreleri kurar.\n\n"
            "> [SINAV SPOTU] Psammom cisimcikleri en sık şu 4 neoplazide görülür: 1) Tiroid papiller karsinomu, "
            "2) Over seröz karsinomu, 3) Menenjiyom, 4) Malign mezotelyoma.\n\n"
            "Patolog ince iğne aspirasyonunda veya biyopside psammom cisimciği gördüğünde bu neoplazileri derhal ekarte etmelidir."
        ),
        "medicalTerms": [
            {"term": "Psammom Cisimciği", "explanation": "Konsantrik lameller katmanlar içeren yuvarlak mikroskobik distrofik kalsiyum küresidir (Grekçe psammos = kum)."},
            {"term": "Papiller Karsinom", "explanation": "Parmaksı çıkıntılar oluşturan ve sıklıkla psammom cisimciği içeren epitel tümörüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Psammom cisimciği lameller konsantrik distrofik kalsifikasyon örneğidir.",
            "📌 [SINAV SPOTU] Tiroid papiller karsinomu, over seröz karsinomu ve menenjiyomda patognomoniktir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lameller Yapı", "desc": "İç içe geçmiş soğan zarı biçimli kalsiyum tabakaları.", "isKey": True},
                {"title": "Tümör Dörtlüsü", "desc": "Tiroid papiller, Over seröz, Menenjiyom, Mezotelyoma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Neoplazi", "Lokalizasyon", "Histolojik Özellik", "Psammom Cisimciği Rolü"],
                [
                    [("Tiroid Papiller Karsinom", False, ""), ("Tiroid bezi", False, ""), ("Buzlu cam nükleuslar, yarıklar", False, ""), ("Papiller eksende konsantrik kalsiyum", True, "Tanı koydurucu lamel küre")],
                    [("Over Seröz Karsinomu", False, ""), ("Over / Periton", False, ""), ("Papiller yapılar, atipi", False, ""), ("Stroma ve papilla tepelerinde yaygın", True, "Konsantrik mikrokalsifikasyon")],
                    [("Menenjiyom", False, ""), ("Dura mater / Meninks", False, ""), ("İğsi hücreler, girdap paterni", False, ""), ("Girdap merkezinde taşlaşma", True, "Menenjiyomun klasik kalsiyum küresi")]
                ]
            ),
            make_cloze(
                "Tiroid papiller karsinomu ve menenjiyomda izlenen konsantrik lameller kalsiyum kürelerine psammom cisimcikleri adı verilir.",
                "psammom cisimcikleri",
                "İç içe lamelli kum benzeri kalsifikasyon küreleri"
            )
        ]
    })

    # ADIM 89 - CHECKPOINT 9
    slides.append({
        "slideNumber": 89,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Distrofik Kalsifikasyon ve Morfolojik Özellikler",
        "subtitle": "Normokalsemi, mitokondriyal nükleasyon, kapak stenozu ve psammom cisimciklerinin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 9,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında distrofik kalsifikasyon mekanizmasını ve klinik örneklerini sentezliyoruz. "
            "1) Temel kural: Serum kalsiyumu kesinlikle normaldir; çökme ölü, hasarlı veya nekrotik dokularda olur. "
            "2) Nükleasyon (çekirdeklenme): Hücre içi başlangıç yeri nekrotik hücre mitokondrileri, hücre dışı başlangıç "
            "ise hasarlı membran vezikülleridir. 3) Klinik formlar: Yaşlılarda senil kalsifik aort stenozu, ileri "
            "aterosklerotik plaklar (CAC skoru), kalsifiye tüberküloz granülomları (Ranke kompleksi). 4) Mikroskopi: "
            "H&E kesitlerinde bazofilik kaba amorf çökeltiler ve tümörlerde konsantrik lameller psammom cisimcikleri.\n\n"
            "> [KLİNİK İPUCU] Sınavda serum Ca normal + nekrotik doku eşleşmesi daima distrofik kalsifikasyonu işaret eder.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle zihninize sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Distrofik Kalsifikasyon", "explanation": "Normokalsemi zemininde nekrotik dokularda hidroksiapatit çökmesidir."},
            {"term": "Psammom Cisimciği", "explanation": "Tümör nekrozu zemininde konsantrik lameller kalsiyum küreleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Distrofik kalsifikasyonda serum kalsiyumu daima normaldir.",
            "📌 [SINAV SPOTU] Hücre içi nükleasyon mitokondride, hücre dışı membran veziküllerinde başlar.",
            "📌 [SINAV SPOTU] Psammom cisimcikleri tiroid papiller Ca, over seröz Ca ve menenjiyomda görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Normokalsemi", "desc": "Kalsiyum metabolizması tamamen normaldir.", "isKey": True},
                {"title": "Nükleasyon Odakları", "desc": "Mitokondri ve matriks membran vezikülleri.", "isKey": True},
                {"title": "Klasik Lezyonlar", "desc": "Aort stenozu, aterom plağı, Ghon odağı, psammom cisimcikleri.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-25",
                "Distrofik kalsifikasyonda serum kalsiyum düzeyi ile tutulan dokunun canlılık durumu nasıldır?",
                "Serum kalsiyum düzeyi tamamen normaldir (normokalsemi); birikim ise daima ölü, hasarlı veya nekrotik dokularda gerçekleşir.",
                "Distrofik kalsifikasyon temel biyokimyasal ve dokusal tanımı"
            ),
            make_flashcard(
                "k1-07-fc-26",
                "Distrofik kalsifikasyonun kristal çekirdeklenmesinin başladığı intraselüler ve ekstraselüler yapılar nelerdir?",
                "Hücre içinde nekrotik hücrelerin mitokondrileri; hücre dışında ise parçalanan hücre membranlarından kopan membran vezikülleridir.",
                "İntraselüler ve ekstraselüler çekirdeklenme odakları"
            ),
            make_flashcard(
                "k1-07-fc-27",
                "Psammom cisimcikleri (psammoma bodies) mikroskobik olarak nasıl görünür ve en sık hangi 3 tümörde izlenir?",
                "Konsantrik lameller (iç içe geçmiş halkalar halinde) bazofilik kalsiyum küreleridir; en sık tiroid papiller karsinomu, over seröz karsinomu ve menenjiyomda izlenir.",
                "Psammom cisimciği morfolojisi ve neoplazi örnekleri"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Distrofik kalsifikasyonda hücre içi ilk kristal çekirdeklenmesi nekrotik hücrelerin mitokondrileri organelinde başlar.",
                "mitokondrileri",
                "Kalsiyum fosfatın ilk çöktüğü hücre içi organel"
            )
        ]
    })

    # ADIM 90
    slides.append({
        "slideNumber": 90,
        "title": "Distrofik ve Metastatik Kalsifikasyonun Karşılaştırmalı Ayrımı",
        "subtitle": "Klinik senaryolarda kalsifikasyon tipini belirleyen temel algoritma",
        "badge": "Karşılaştırma",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Patolojide ve klinikte kalsifikasyonla karşılaşıldığında hekimin atacağı ilk adım serum kalsiyum düzeyini "
            "ölçmektir. Eğer serum kalsiyumu normalse süreç lokal doku hasarına bağlı 'distrofik kalsifikasyondur' "
            "(enfarkt skarı, aterom, kalsifiye kapak, kazeöz nekroz). Eğer serum kalsiyumu yüksekse (hiperkalsemi) "
            "süreç sistemik nedenli 'metastatik kalsifikasyondur'.\n\n"
            "> [KLİNİK İPUCU] Distrofik kalsifikasyon lokal hasarlı tek bir odakta kalırken; metastatik kalsifikasyon "
            "vücudun çok sayıda normal organında (mide, böbrek, akciğer) yaygın ve multifokal çökelir.\n\n"
            "Bu ayrım, altta yatan malignite, hiperparatiroidizm veya kapak stenozunun doğru yönetilmesini sağlar."
        ),
        "medicalTerms": [
            {"term": "Metastatik Kalsifikasyon", "explanation": "Hiperkalsemi zemininde normal dokularda yaygın kalsiyum tuzu çökelmesidir."},
            {"term": "Hiperkalsemi", "explanation": "Serum kalsiyum düzeyinin normal üst sınırı (>10.5 mg/dL) aşması durumudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Distrofik = Serum Ca normal, hasarlı doku, lokal lezyon.",
            "📌 [SINAV SPOTU] Metastatik = Hiperkalsemi, normal dokular, yaygın çoklu organ tutulumu."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Biyokimya Ayrımı", "desc": "Normokalsemi (distrofik) vs Hiperkalsemi (metastatik).", "isKey": True},
                {"title": "Doku Ayrımı", "desc": "Nekrotik skar dokusu (distrofik) vs Normal sağlıklı dokular (metastatik).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Distrofik Kalsifikasyon vs Metastatik Kalsifikasyon",
                "Distrofik Kalsifikasyon",
                "Serum kalsiyumu tamamen normaldir; birikim yalnızca hasarlı, nekrotik veya yaşlanmış dokularda (enfarkt, kapak, aterom) lokalize olarak gelişir.",
                "Metastatik Kalsifikasyon",
                "Serum kalsiyumu belirgin şekilde yüksektir (hiperkalsemi); birikim normal sağlıklı dokularda (mide, böbrek, akciğer) yaygın ve sistemik olarak gelişir."
            ),
            make_active_recall(
                "Distrofik kalsifikasyon ile metastatik kalsifikasyonu ayırt etmek için istenecek ilk ve en kritik laboratuvar testi nedir?",
                "Serum total ve iyonize kalsiyum düzeyi ölçümüdür (normokalsemi distrofiği, hiperkalsemi metastatiği gösterir)."
            )
        ]
    })

    return slides
