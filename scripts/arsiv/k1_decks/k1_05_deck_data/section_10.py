"""
Bölüm 10: Hücre Hasarının Biyokimyasal Mekanizmaları - II: ROS, Membran Hasarı ve Büyük Sentez
Adımlar: 91 - 100
Checkpoint: Adım 100 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # ADIM 91
    slides.append({
        "slideNumber": 91,
        "title": "Reaktif Oksijen Türleri (ROS) ve Serbest Radikaller: Kimyasal Kararsızlık",
        "subtitle": "Dış yörüngesinde eşleşmemiş elektron taşıyan son derece agresif moleküller",
        "badge": "ROS Giriş",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücresel hasarın kimyasal düzeydeki en yıkıcı ajanları 'Serbest Radikaller' ve bunların türevleri olan "
            "'Reaktif Oksijen Türleri'dir (ROS - Reactive Oxygen Species). Kimyasal olarak serbest radikal, "
            "dış moleküler yörüngesinde tek başına (eşleşmemiş) bir elektron barındıran kararsız atom veya gruptur.\n\n"
            "Bu eşleşmemiş elektron molekülü aşırı enerjik ve agresif kılar. Kararlı hale geçebilmek için "
            "komşu lipid, protein veya DNA molekülünden zorla bir elektron çalar.\n\n"
            "> [SINAV SPOTU] Serbest radikaller fizyolojik olarak mitokondriyal elektron taşıma zincirinde (oksidatif "
            "fosforilasyon) O2'nin 4 elektronla suya indirgenmesi sırasında eser miktarda kaçan elektronlardan oluşur.\n\n"
            "Ayrıca nötrofil ve makrofajların fagositoz sırasında mikropları öldürmek için başlattığı solunum patlamasında "
            "(respiratory burst) bolca ROS üretilir."
        ),
        "medicalTerms": [
            {"term": "Serbest Radikal", "explanation": "Dış yörüngesinde eşleşmemiş elektron taşıyan, son derece reaktif ve kararsız kimyasal molekül."},
            {"term": "Reaktif Oksijen Türleri (ROS)", "explanation": "Oksijen metabolizması sırasında üretilen süperoksit, hidrojen peroksit ve hidroksil gibi radikal ve oksidanlar."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Serbest radikaller dış yörüngede eşleşmemiş elektron taşıyan kararsız moleküllerdir.",
            "📌 [SINAV SPOTU] Fizyolojik olarak mitokondriyal solunum zincirinde ve fagositlerin solunum patlamasında üretilirler.",
            "📌 [SINAV SPOTU] Radyasyon, toksinler, ilaçlar ve reperfüzyon ROS üretimini patlatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Elektron Açlığı", "desc": "Kararsız tek elektronun komşu biyomoleküllere saldırması.", "isKey": True},
                {"title": "Hücresel Kaynaklar", "desc": "Mitokondri kaçakları ve lökosit NADPH oksidaz enzimi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dış yörüngesinde eşleşmemiş elektron taşıyan ve komşu moleküllere saldırarak zincirleme hasar başlatan kimyasallara serbest radikaller denir.",
                "serbest radikaller",
                "Kararsız elektron taşıyan oksitleyici moleküllerin genel adı"
            ),
            make_active_recall(
                "Sağlıklı bir hücrede serbest radikaller fizyolojik olarak başlıca hangi iki hücresel süreçte üretilir?",
                "1) Mitokondriyal elektron taşıma zincirinde (oksidatif fosforilasyon) ve 2) Lökositlerin mikropları öldürürken yaptığı solunum patlamasında (respiratory burst)."
            )
        ]
    })

    # ADIM 92
    slides.append({
        "slideNumber": 92,
        "title": "Başlıca Reaktif Oksijen Türleri: Süperoksit, Hidrojen Peroksit ve Peroksinitrit",
        "subtitle": "Oksijenin kademeli indirgenme basamakları ve hücresel dağılımı",
        "badge": "Radikal Türleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Ders notumuzdaki Tablo 1.3'e göre hücre hasarında rol oynayan başlıca 4 reaktif tür vardır:\n\n"
            "1. Süperoksit Anyonu (O₂•⁻): O2'nin mitokondride tam indirgenememesiyle veya lökositlerde 'fagosit oksidaz' "
            "(NADPH oksidaz) ile üretilir. Doğrudan lipid, protein ve DNA hasarı yapar.\n\n"
            "2. Hidrojen Peroksit (H₂O₂): Bir serbest radikal değildir (eşleşmemiş elektronu yoktur) ancak güçlü bir "
            "oksidandır. Süperoksitten SOD enzimiyle üretilir. Membranları kolayca geçerek uzak organellere yayılabilir. "
            "Nötrofillerde miyeloperoksidaz (MPO) ile hipoklorite (ClO⁻ - çamaşır suyu) dönüştürülür.\n\n"
            "> [SINAV SPOTU] 3. Peroksinitrit (ONOO⁻): Süperoksit ile nitrik oksitin (NO) birleşmesiyle oluşur; "
            "hem oksidatif hem nitrozatif hasar yapar!\n\n"
            "Bu ara ürünler en ölümcül radikal olan hidroksil radikalinin öncülleridir."
        ),
        "medicalTerms": [
            {"term": "Süperoksit (O2.-)", "explanation": "Oksijene bir elektron eklenmesiyle oluşan ilk reaktif oksijen ara ürünü."},
            {"term": "Peroksinitrit (ONOO-)", "explanation": "Süperoksitin nitrik oksit (NO) ile birleşmesiyle oluşan güçlü oksidan ve nitrolayıcı radikal."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Süperoksit (O₂•⁻) mitokondri kaçağı veya NADPH oksidaz ile üretilir.",
            "📌 [SINAV SPOTU] Hidrojen peroksit (H₂O₂) süperoksitten SOD ile üretilir; miyeloperoksidaz ile hipoklorite (ClO⁻) dönüşür.",
            "📌 [SINAV SPOTU] Peroksinitrit (ONOO⁻) süperoksit ile NO etkileşiminden doğar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kademeli İndirgenme", "desc": "O2 -> O2.- -> H2O2 -> .OH dönüşüm zinciri.", "isKey": True},
                {"title": "MPO ve Hipoklorit", "desc": "Nötrofil lökositlerin H2O2'den mikrop öldürücü klor gazı türetmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Reaktif Tür", "Üretim Mekanizması", "Patolojik Etki Alanı"],
                [
                    [("Süperoksit (O2•⁻)", False, ""), ("Eksik O2 indirgenmesi / NADPH Oksidaz", True, "Mitokondri ve lökosit kaynağı"), ("Lipid, protein ve DNA'da doğrudan hasar", False, "")],
                    [("Hidrojen Peroksit (H2O2)", False, ""), ("Süperoksitten SOD enzimi aracılığıyla", True, "Dismutaz ürünü"), ("Zarları geçer; MPO ile hipoklorite (ClO⁻) dönüşür", False, "")],
                    [("Peroksinitrit (ONOO⁻)", False, ""), ("Süperoksit (O2•⁻) + Nitrik Oksit (NO)", True, "NO ile radikal birleşimi"), ("Oksidatif ve nitrozatif doku hasarı", False, "")]
                ]
            ),
            make_cloze(
                "Süperoksit anyonunun nitrik oksit ile reaksiyona girmesi sonucu oluşan hem oksidatif hem nitrozatif hasar yapan moleküle peroksinitrit denir.",
                "peroksinitrit",
                "O2.- ve NO birleşimiyle doğan reaktif tür adı"
            )
        ]
    })

    # ADIM 93
    slides.append({
        "slideNumber": 93,
        "title": "Hidroksil Radikali (•OH) ve Fenton Reaksiyonu: En Yıkıcı Serbest Radikal",
        "subtitle": "Demir kataliziyle hidrojen peroksitten üretilen ve hiçbir enzimi durduramayan ölümcül ajan",
        "badge": "Fenton Reaksiyonu",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Tüm reaktif oksijen türleri arasında biyolojik dokulara en doğrudan, en hızlı ve en vahşi hasarı veren "
            "molekül 'Hidroksil Radikali'dir (•OH). Hidroksil radikalinin yarı ömrü saniyenin milyarda biri kadardır; "
            "üretildiği mikronluk alandaki ilk moleküle (DNA, membran lipidi, enzim) anında saldırır.\n\n"
            "Hidroksil radikali vücutta başlıca iki yolla üretilir: Suyun iyonizan radyasyonla radyolizi veya "
            "serbest demir (Fe²⁺) katalizörlüğünde gerçekleşen 'Fenton Reaksiyonu'.\n\n"
            "> [SINAV SPOTU] Fenton Reaksiyonu: Fe²⁺ + H₂O₂ -> Fe³⁺ + •OH + OH⁻ formülüyle yürür. "
            "Hidroksil radikali dokularda bilinen EN GÜÇLÜ serbest radikaldir!\n\n"
            "Vücutta bu radikali doğrudan parçalayan hiçbir enzim yoktur; hücre tek korunma yolu olarak H2O2'yi "
            "henüz hidroksile dönüşmeden katalaz ve glutatyon peroksidaz ile suya çevirmeye çalışır."
        ),
        "medicalTerms": [
            {"term": "Hidroksil Radikali (•OH)", "explanation": "Biyolojik sistemlerde üretilen en reaktif, en kısa ömürlü ve en tahripkar serbest radikal."},
            {"term": "Fenton Reaksiyonu", "explanation": "İki değerlikli demirin (Fe2+) hidrojen peroksiti hidroksil radikaline çevirdiği redoks reaksiyonu."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücre hasarında EN GÜÇLÜ ve en doğrudan hasar verici serbest radikal HİDROKSİL RADİKALİDİR (•OH).",
            "📌 [SINAV SPOTU] Hidroksil radikali başlıca 'Fenton Reaksiyonu' (Fe²⁺ + H₂O₂) ile üretilir.",
            "📌 [SINAV SPOTU] Hidroksil radikalini doğrudan temizleyen enzim yoktur; öncüsü olan H₂O₂ temizlenmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Zirve Tahribat", "desc": "Biyolojideki en güçlü serbest radikal: Hidroksil radikali.", "isKey": True},
                {"title": "Fenton Kimyası", "desc": "Demir (Fe2+) varlığında H2O2'nin hidroksil patlamasına dönüşmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "İki değerlikli demir (Fe²⁺) varlığında hidrojen peroksitin parçalanmasıyla (Fenton reaksiyonu) oluşan ve hücre hasarındaki EN GÜÇLÜ ve en tahripkar serbest radikal hangisidir?",
                {
                    "A": "Süperoksit anyonu (O₂•⁻)",
                    "B": "Hidrojen peroksit (H₂O₂)",
                    "C": "Hidroksil radikali (•OH)",
                    "D": "Nitrik oksit (NO)",
                    "E": "Hipokloröz asit (HOCl)"
                },
                "C",
                {
                    "A": "Süperoksit ilk radikaldir ancak en güçlüsü değildir.",
                    "B": "H2O2 radikal bile değildir.",
                    "C": "Doğru cevap C'dir: Hidroksil radikali (•OH) Fenton reaksiyonuyla üretilen en güçlü serbest radikaldir.",
                    "D": "NO bir gaz haberci ve vazodilatatördür.",
                    "E": "HOCl nötrofillerin fagositoz mikrop öldürücüsüdür."
                }
            ),
            make_cloze(
                "Demir aracılı Fenton reaksiyonu sonucu üretilen ve dokularda bilinen en güçlü serbest radikal hidroksil radikali molekülüdür.",
                "hidroksil radikali",
                "En güçlü ve en tahripkar serbest radikalin tam adı"
            )
        ]
    })

    # ADIM 94
    slides.append({
        "slideNumber": 94,
        "title": "Antioksidan Savunma Sistemleri: Enzimatik ve Non-Enzimatik Kalkanlar",
        "subtitle": "Süperoksit dismutaz, katalaz, glutatyon peroksidaz ve vitaminlerin dengesi",
        "badge": "Antioksidanlar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre serbest radikal tehdidine karşı muazzam bir antioksidan savunma ordusuyla donatılmıştır. "
            "Bu sistem iki büyük kolda organize olmuştur:\n\n"
            "1. Enzimatik Savunma:\n"
            "- Süperoksit Dismutaz (SOD): Süperoksiti (O₂•⁻) daha az zararlı olan Hidrojen Peroksite (H₂O₂) dönüştürür.\n"
            "- Glutatyon Peroksidaz (GSH-Px): Sitozol ve mitokondride H₂O₂'yi redükte glutatyon (GSH) kullanarak suya (H₂O) çevirir.\n"
            "- Katalaz: Peroksizomlarda yoğun bulunur; H₂O₂'yi doğrudan H₂O ve O₂'ye parçalar.\n\n"
            "> [SINAV SPOTU] 2. Non-Enzimatik Savunma: Vitamin E (alfa-tokoferol - en güçlü yağda çözünen antioksidan, "
            "membranları korur), Vitamin C (askorbat - suda çözünür), Glutatyon ve Beta-karotendir!\n\n"
            "Serbest radikal üretimi temizleme kapasitesini aştığında ortaya çıkan patolojiye 'Oksidatif Stres' denir."
        ),
        "medicalTerms": [
            {"term": "Süperoksit Dismutaz (SOD)", "explanation": "Süperoksit radikallerini hidrojen peroksit ve moleküler oksijene dönüştüren enzim."},
            {"term": "Oksidatif Stres", "explanation": "Pro-oksidan serbest radikal üretimi ile antioksidan savunma arasındaki dengenin hasar yönünde bozulması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enzimatik antioksidanlar: Süperoksit dismutaz (SOD), Katalaz ve Glutatyon peroksidazdır.",
            "📌 [SINAV SPOTU] Non-enzimatik antioksidanlar: Vitamin E, Vitamin C, Glutatyon ve β-karotendir.",
            "📌 [SINAV SPOTU] Üretim > Temizleme = Oksidatif Stres."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Üçlü Enzim Kalkanı", "desc": "SOD (O2.-'yi dönüştürür), Katalaz ve Glutatyon Peroksidaz (H2O2'yi suya çevirir).", "isKey": True},
                {"title": "Oksidatif Terazi", "desc": "Radikal fazlalığının oksidatif stres hasarına yol açması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Antioksidan Mekanizma", "Enzim / Molekül", "Temizlediği Serbest Radikal / Reaksiyon"],
                [
                    [("Enzimatik Dismutasyon", False, ""), ("Süperoksit Dismutaz (SOD)", True, "İlk basamak enzimi"), ("Süperoksiti (O2•⁻) H2O2'ye dönüştürür", False, "")],
                    [("Enzimatik Peroksit Yıkımı", False, ""), ("Katalaz ve Glutatyon Peroksidaz", True, "H2O2 temizleyiciler"), ("H2O2'yi zararsız H2O ve O2'ye dönüştürür", False, "")],
                    [("Non-Enzimatik Membran Koruma", False, ""), ("Vitamin E (Alfa-tokoferol)", True, "Yağda çözünen vitamin"), ("Lipid peroksidasyon zincirini kırar", False, "")]
                ]
            ),
            make_cloze(
                "Süperoksit radikallerini hidrojen peroksite dönüştürerek temizleyen enzime süperoksit dismutaz veya SOD denir.",
                "süperoksit dismutaz",
                "SOD kısaltmasının Türkçe açık enzim adı"
            )
        ]
    })

    # ADIM 95
    slides.append({
        "slideNumber": 95,
        "title": "ROS'un Üç Yıkıcı Hedefi: Lipid, Protein ve DNA Hasarı",
        "subtitle": "Zincirleme peroksidasyon, sülfhidril çapraz bağlanması ve çift zincir mutasyonları",
        "badge": "Yıkıcı Etkiler",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Ders notumuzda vurgulandığı üzere, serbest radikaller hücreye ulaştığında 3 ana makromolekül sınıfını vurur:\n\n"
            "1. Lipid Peroksidasyonu: Radikaller membran fosfolipidlerinin doymamış çift bağlarındaki hidrojeni çalar. "
            "Oluşan lipid peroksi radikali komşu fosfolipide saldırır; otokatalitik bir zincirleme reaksiyonla tüm membran delinir.\n\n"
            "2. Protein Oksidasyonu: Aminoasitlerin yan zincirlerini oksitler. Özellikle sülfhidril (-SH) bağları disülfid "
            "(-S-S-) köprülerine dönüşerek çapraz bağlanır. Enzimler aktivitesini kaybeder, yapısal proteinler çöker.\n\n"
            "> [SINAV SPOTU] 3. DNA Hasarı: Tek ve çift sarmal kırıkları, timin glikol gibi baz modifikasyonları ve "
            "p53 aktivasyonu yapar!\n\n"
            "Bu üçlü tahribat nekroz, apoptoz, hücresel yaşlanma ve kanserojenez ile sonuçlanır."
        ),
        "medicalTerms": [
            {"term": "Lipid Peroksidasyonu", "explanation": "Serbest radikallerin membran lipid çift bağlarını kopararak zincirleme otokatalitik membran yıkımı yapması."},
            {"term": "Protein Çapraz Bağlanması", "explanation": "Oksidasyon sonucu sülfhidril gruplarının kovalent bağlanarak proteinleri inaktive etmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] ROS'un 3 temel hasarı: 1) Lipid peroksidasyonu, 2) Protein oksidasyonu/çapraz bağlanma, 3) DNA tek/çift zincir kırıkları.",
            "📌 [SINAV SPOTU] Hücresel sonuçlar: Nekroz, apoptoz, yaşlanma ve kanserdir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Otokatalitik Membran Yıkımı", "desc": "Bir radikalin binlerce lipid molekülünü yakması.", "isKey": True},
                {"title": "Kanser ve Yaşlanma", "desc": "DNA mutasyonları ve protein agregasyonunun kronik sonuçları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Makromoleküler Hedef", "Biyokimyasal Hasar Mekanizması", "Patolojik Nihai Sonuç"],
                [
                    [("Membran Fosfolipidleri", False, ""), ("Lipid peroksidasyonu zincir reaksiyonu", True, "Zar hasarı türü"), ("Zar geçirgenlik kaybı ve rüptür", False, "")],
                    [("Hücresel Proteinler", False, ""), ("Sülfhidril (-SH) çapraz bağlanması", True, "Protein hasarı türü"), ("Enzim inaktivasyonu ve yanlış katlanma", False, "")],
                    [("Nükleer ve Mitokondriyal DNA", False, ""), ("Tek ve çift zincir kırıkları, baz modifikasyonu", True, "Genotoksik hasar türü"), ("Mutasyonlar, apoptoz ve neoplazi", False, "")]
                ]
            ),
            make_cloze(
                "Serbest radikallerin hücre zarı doymamış yağ asitlerine saldırarak başlattığı zincirleme reaksiyona lipid peroksidasyonu denir.",
                "lipid peroksidasyonu",
                "Membran yağlarının radikallerce otokatalitik yıkımı terimi"
            )
        ]
    })

    # ADIM 96
    slides.append({
        "slideNumber": 96,
        "title": "Membran Hasarının Üçlü Mekanizması: ROS, ATP Azalması ve Fosfolipazlar",
        "subtitle": "Hücre zarı delinmesinin arkasındaki biyokimyasal sacayağı ve deterjan etkisi",
        "badge": "Membran Hasarı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre ölümünde geri dönüşüm sınırını (point of no return) çizen plazma zarı parçalanması rastgele "
            "meydana gelmez; arkasında birbiriyle kenetlenmiş 3 patofizyolojik mekanizma yatar (Ders Şekil 1.17):\n\n"
            "1. Reaktif Oksijen Türleri (ROS): Lipid peroksidasyonu yaparak membran fosfolipidlerini doğrudan yakar.\n"
            "2. ATP Azalması: Fosfolipid sentezi enerji bağımlıdır; ATP tükenince yeni membran lipidi üretilemez.\n"
            "3. Sitozolik Ca²⁺ Artışı: Kalsiyum hem fosfolipazları hem proteazları aktive eder. Fosfolipazlar "
            "membran lipitlerini parçalar; açığa çıkan serbest yağ asitleri ve lizofosfolipidler deterjan etkisi "
            "yaparak zarı daha da eritir. Proteazlar ise zarın altındaki iskelet proteinlerini keser.\n\n"
            "> [SINAV SPOTU] Sonuçta hücre zarı parçalanır, lizozom membranları yırtılarak asit hidrolazlar sitoplazmaya "
            "sızar ve hücre oto-sindirim ile nekroza uğrar!"
        ),
        "medicalTerms": [
            {"term": "Deterjan Etkisi", "explanation": "Fosfolipid yıkım ürünlerinin (lizofosfolipidler) membran çift tabakasını çözerek eritmesi."},
            {"term": "Lizozomal Rüptür", "explanation": "Lizozom zarının yırtılarak asit hidrolazların sitoplazmaya dökülmesi ve oto-sindirim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Membran hasarının 3 mekanizması: ROS (lipid peroksidasyonu), ATP azalması (sentez azalması) ve Sitozolik Ca²⁺ artışı (fosfolipaz aktivasyonu).",
            "📌 [SINAV SPOTU] Fosfolipid yıkım ürünleri deterjan etkisi yaparak zar hasarını derinleştirir.",
            "📌 [SINAV SPOTU] Plazma ve lizozom zarlarının parçalanması geri dönüşümsüz hasarın kesin imzasıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sacayağı Mekanizma", "desc": "ROS saldırısı + ATP yokluğu + Ca2+ fosfolipaz yıkımı.", "isKey": True},
                {"title": "Deterjan Kısır Döngüsü", "desc": "Açığa çıkan lizofosfolipidlerin zarı daha hızlı çözmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Membran Hasarı ve Hücre Ölümü Basamakları",
                [
                    "1. Başlatıcı Darbe: İskemi veya toksin ATP'yi tüketir ve serbest kalsiyumu fırlatır.",
                    "2. Enzim Aktivasyonu: Yüksek Ca2+ membran fosfolipazlarını ve sitoskeleton proteazlarını açar.",
                    "3. Fosfolipid Yıkımı: Fosfolipazlar zarı parçalarken açığa çıkan deterjan ürünler zarı çözer.",
                    "4. Plazma Zarı Rüptürü: Hücre dışarıya enzim sızdırırken içeri kontrolsüz sıvı akar.",
                    "5. Lizozomal Kaçış: Lizozom zarı delinir ve asit hidrolazlar tüm organelleri eriterek nekrozu tamamlar."
                ]
            ),
            make_cloze(
                "Hücre hasarında kalsiyum bağımlı fosfolipaz aktivasyonu sonucu açığa çıkan lipid yıkım ürünleri deterjan etkisi ile membran hasarını artırır.",
                "deterjan etkisi",
                "Membran lipitlerini çözen fizikokimyasal etki"
            )
        ]
    })

    # ADIM 97
    slides.append({
        "slideNumber": 97,
        "title": "İskeminin Patofizyolojik Akışı: Arter Tıkanmasından Hücre Ölümüne",
        "subtitle": "Robbins ve Keleş ders sunumundaki Şekil 1.19'un eksiksiz patolojik dekonstrüksiyonu",
        "badge": "İskemi Akışı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dersimizin en temel sentetik şekli olan Şekil 1.19, bir arter tıkandığında hücrede saniyeler ve "
            "dakikalar içinde gelişen patofizyolojik zinciri gösterir:\n\n"
            "1. Arter Tıkanması -> İskemi -> Oksidatif Fosforilasyon Durur -> ATP Azalır.\n"
            "2. Kol 1 (Pompalar): Na+/K+ ATPaz çöker -> Hücreye sodyum ve su girer -> Hücresel şişme ve zar kabarcıkları oluşur.\n"
            "3. Kol 2 (Glikoliz): Anaerobik glikoliz artar -> Glikojen tükenir -> Laktik asit birikir -> İntraselüler pH düşer -> Kromatin kümelenir ve enzimler durur.\n"
            "4. Kol 3 (Translasyon): Ribozomlar granüllü ER'den ayrılır -> Protein sentezi çöker.\n\n"
            "> [SINAV SPOTU] Bu evreler geri dönüşümlüdür. Ancak hipoksi uzarsa mitokondri ve lizozom zarları yırtılır; "
            "enzimler kana kaçar ve inflamasyon eşliğinde GERİ DÖNÜŞÜMSÜZ NEKROZ gelişir!"
        ),
        "medicalTerms": [
            {"term": "Ribozom Dekolmanı", "explanation": "ATP tükenmesi sonucu ribozomların granüllü ER zarlarından kopup protein sentezini durdurması."},
            {"term": "Laktik Asidoz", "explanation": "Anaerobik glikolizin hızlanmasıyla hücre içinde laktik asit birikip pH'ı düşürmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İskemide ilk olay ATP azalmasıdır.",
            "📌 [SINAV SPOTU] Na⁺/K⁺ pompa iflası -> Su girişi, hücre şişmesi, membran kabarcıkları.",
            "📌 [SINAV SPOTU] Anaerobik glikoliz -> Laktik asit -> pH düşmesi -> Enzim aktivite kaybı.",
            "📌 [SINAV SPOTU] Ribozomların ER'den ayrılması -> Protein sentezi azalması.",
            "📌 [SINAV SPOTU] Geri dönüşümsüz membran hasarı -> Enzim salınımı, inflamasyon ve nekroz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Üçlü Kol", "desc": "1) Na/K pompası (şişme), 2) Glikoliz (asidoz), 3) Ribozom ayrılması (protein sentezi durması).", "isKey": True},
                {"title": "Geri Dönüş Eşiği", "desc": "Zar ve mitokondri parçalanana kadar süreç geri döndürülebilirdir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["İskemik Basamak", "Tetiklenen Hücresel Olay", "Morfolojik / Fonksiyonel Sonuç"],
                [
                    [("ATP Azalması", False, ""), ("Na+/K+ ATPaz pompa yetmezliği", True, "Pompa durması"), ("Su girişi, hücresel şişme ve kabarcıklar", False, "")],
                    [("Anaerobik Glikoliz Artışı", False, ""), ("Laktik asit birikimi ve glikojen tükenmesi", True, "Metabolik asit üretimi"), ("Hücre içi pH düşmesi ve enzim inaktivasyonu", False, "")],
                    [("Ribozomların Ayrılması", False, ""), ("Granüllü ER'den poliribozom kopması", True, "Translasyon kompleksi ayrışması"), ("Protein sentezinin durması ve lipid birikimi", False, "")],
                    [("Geri Dönüşsüz Zar Hasarı", False, ""), ("Membran yırtılması ve enzim sızıntısı", True, "Point of no return"), ("Lizozomal oto-sindirim, inflamasyon ve nekroz", False, "")]
                ]
            ),
            make_cloze(
                "İskemi sırasında anaerobik glikolizin hızlanması sonucu hücre içinde laktik asit birikir ve pH düşerek enzimleri inaktive eder.",
                "laktik asit",
                "Anaerobik glikoliz son ürünü olan asit"
            )
        ]
    })

    # ADIM 98
    slides.append({
        "slideNumber": 98,
        "title": "İskemi-Reperfüzyon Hasarı: Kan Akımının Getirdiği İkinci Yıkım",
        "subtitle": "Yeniden gelen oksijenin serbest radikallere dönüşmesi ve lökosit istilası",
        "badge": "Reperfüzyon",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İskemik bir dokuya kan akımını yeniden sağlamak (reperfüzyon), hücreleri kurtarmak için şarttır; "
            "ancak paradoksal olarak bazen doku hasarını daha da şiddetlendirebilir. Bu fenomene 'İskemi-Reperfüzyon Hasarı' denir.\n\n"
            "Tıkanıklık açılıp dokuya ani ve bol oksijenli kan dolduğunda, mitokondrinin hasarlı solunum zinciri "
            "oksijeni tam indirgeyemez ve devasa bir serbest radikal (ROS) patlaması meydana gelir.\n\n"
            "> [SINAV SPOTU] Ayrıca reperfüzyonla gelen kanda bulunan kompleman proteinleri ve nötrofiller nekrotik "
            "dokuyu görünce alevlenerek bölgeye hücum eder ve çevreleyen yarı canlı dokuları da yakıp yıkar!\n\n"
            "Kalsiyum aşırı yüklenmesi de eklenince miyokard infarktüsü reperfüzyonunda 'kontraksiyon bandı nekrozu' "
            "ve öldürücü aritmiler gelişebilir."
        ),
        "medicalTerms": [
            {"term": "İskemi-Reperfüzyon Hasarı", "explanation": "İskemik dokuya kan akımının yeniden sağlanmasıyla ROS ve lökositler aracılığıyla hasarın artması."},
            {"term": "Kontraksiyon Bandı Nekrozu", "explanation": "Reperfüzyonla kardiyomiyositlere aşırı kalsiyum girmesi sonucu miyofibrillerin aşırı kasılıp bantlar yapması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Reperfüzyon hasarında ROS patlaması, nötrofil infiltrasyonu ve kompleman aktivasyonu rol oynar.",
            "📌 [SINAV SPOTU] Reperfüze miyokard dokusunda aşırı kalsiyum girişiyle 'kontraksiyon bandı nekrozu' görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Oksijen Paradoksu", "desc": "Kurtarıcı oksijenin hasarlı mitokondride radikale dönüşmesi.", "isKey": True},
                {"title": "İmmün Saldırı", "desc": "Kan akımıyla gelen nötrofil ve komplemanın dokuyu ezmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut miyokard infarktüsü geçiren hastada koroner damar 3 saat sonra anjiyografiyle açılıyor. Ancak reperfüzyondan sonra hastanın kalp dokusunda hasarın paradoksal olarak arttığı ve aritmiler geliştiği saptanıyor. Patogenetik neden nedir?",
                [
                    {
                        "text": "Stent takıldığı için kalpte kazeöz nekroz gelişmiştir.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Tüberküloz nekrozu koroner girişimde görülmez."
                    },
                    {
                        "text": "Yeniden gelen oksijenin hasarlı mitokondrilerce reaktif oksijen türlerine (ROS) çevrilmesi, nötrofil hücumu ve kalsiyum kaosu (reperfüzyon hasarı).",
                        "isCorrect": True,
                        "feedback": "Kusursuz klinik patoloji yorumu! İskemi-reperfüzyon hasarının temeli ROS, inflamasyon ve kalsiyum patlamasıdır."
                    },
                    {
                        "text": "Kalp kası kemik dokusuna dönüşmüştür.",
                        "isCorrect": False,
                        "feedback": "Biyolojik olarak anlamsızdır."
                    }
                ]
            ),
            make_cloze(
                "İskemik dokuya kan akımının yeniden sağlanması sonrası serbest radikal patlaması ve nötrofil hücumuyla doku hasarının artmasına reperfüzyon hasarı denir.",
                "reperfüzyon hasarı",
                "Kan akımı restorasyonuyla gelişen paradoksal hasar terimi"
            )
        ]
    })

    # ADIM 99
    slides.append({
        "slideNumber": 99,
        "title": "Nekroz Tiplerinin Büyük Ayırıcı Tanı Atlası: 6 Nekrozun Özeti",
        "subtitle": "Koagülatif, sıvılaşma, gangrenöz, kazeöz, yağ ve fibrinoid nekrozun nihai sentezi",
        "badge": "Nekroz Atlası",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Ders 4 ve Ders 5 boyunca incelediğimiz 6 temel nekroz kalıbını tek bir zihinsel şablonda birleştiriyoruz:\n\n"
            "1. Koagülatif Nekroz: Tüm solid organ infarktları (beyin hariç); protein denatürasyonu, hayalet hücreler.\n"
            "2. Sıvılaşma (Likefaksiyon) Nekrozu: Beyin infarktı ve bakteriyel apseler; enzimatik lizis, kistik kavite.\n"
            "3. Gangrenöz Nekroz: Ekstremitelerde koagülatif (kuru) veya süperenfeksiyonlu sıvılaşma (ıslak).\n"
            "4. Kazeöz Nekroz: Tüberküloz enfeksiyonu; sarı-beyaz peynirimsi, amorf granüler, Langhans granülomu.\n"
            "5. Yağ Nekrozu: Akut pankreatit ve meme travması; lipaz hidrolizi, kalsiyum sabunlaşması (saponifikasyon).\n"
            "> [SINAV SPOTU] 6. Fibrinoid Nekroz: Yalnızca mikroskopta tanınır; vaskülitler (PAN) ve malign hipertansiyon; "
            "damar duvarında parlak pembe camsı immün kompleks ve fibrin birikimi!\n\n"
            "Bu 6 nekroz patolojinin temel alfabesidir."
        ),
        "medicalTerms": [
            {"term": "Nekroz Spektrumu", "explanation": "Farklı dokularda etiyoloji ve enzim dengesine göre ortaya çıkan 6 temel morfolojik ölüm kalıbı."},
            {"term": "Ayırıcı Tanı Kriterleri", "explanation": "Makroskopi, ışık mikroskopisi, histokimyasal boyanma ve klinik bağlam eşleşmeleri."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Katı organ enfarktları = Koagülatif (Beyin = Sıvılaşma).",
            "📌 [SINAV SPOTU] Tüberküloz = Kazeöz (peynirimsi amorf).",
            "📌 [SINAV SPOTU] Akut pankreatit = Yağ nekrozu (sabunlaşma).",
            "📌 [SINAV SPOTU] Vaskülit (PAN) ve Malign HT = Fibrinoid nekroz (damar duvarı camsı pembe)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Altılı Nekroz Mimarisi", "desc": "Koagülatif, likefaksiyon, gangrenöz, kazeöz, yağ ve fibrinoid.", "isKey": True},
                {"title": "Klinik Eşleşme Kesinliği", "desc": "Her nekroz tipinin kendine özgü patognomonik organı ve nedeni.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Nekroz Tipi", "Karakteristik Makroskopi", "Karakteristik Mikroskopi", "Tipik Klinik Örnek"],
                [
                    [("Koagülatif Nekroz", False, ""), ("Soluk sert kama biçimli alan", False, ""), ("Hücre anahatları korunmuş hayalet hücreler", True, "Hücre sınırları korunur"), ("Böbrek, kalp, dalak infarktı", False, "")],
                    [("Sıvılaşma Nekrozu", False, ""), ("Kistik yumuşak kavite, püy", False, ""), ("Hücre kalıntısız erimiş sıvı alan", True, "Komple enzimatik lizis"), ("Beyin infarktı, bakteriyel apse", False, "")],
                    [("Kazeöz Nekroz", False, ""), ("Sarı-beyaz ufalanan peynir kitlesi", False, ""), ("Amorf pembe granüler + Langhans granülomu", True, "Peynirimsi amorf alan"), ("Akciğer tüberkülozu", False, "")],
                    [("Yağ Nekrozu", False, ""), ("Tebeşir beyazı sabunlaşma odakları", False, ""), ("Gölge adipositler + bazofilik kalsiyum", True, "Mor kalsiyum tuzları"), ("Akut pankreatit, meme travması", False, "")],
                    [("Fibrinoid Nekroz", False, ""), ("Makroskopide GÖRÜLEMEZ", False, ""), ("Damar duvarında parlak pembe camsı bant", True, "Mikroskobik camsı bant"), ("Poliarteritis nodosa, Malign HT", False, "")]
                ]
            ),
            make_cloze(
                "Diğer tüm nekroz tipleri makroskobik olarak görülebilirken fibrinoid nekroz yalnızca ışık mikroskobunda damar duvarında tanınır.",
                "fibrinoid nekroz",
                "Makroskopik görüntüsü olmayan tek nekroz tipi"
            )
        ]
    })

    # ADIM 100 (CHECKPOINT 10 - BÜYÜK FİNAL)
    slides.append({
        "slideNumber": 100,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Ders 5 Büyük Sentez ve Mezuniyet İstasyonu",
        "subtitle": "Kazeöz, yağ ve fibrinoid nekrozdan apoptoz kaskadına, yeni ölüm biçimlerinden ROS ve iskemiye tam özet",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 10,
        "synthesisNarrative": (
            "Tebrikler! Kurul 1 Patoloji müfredatının en kapsamlı derslerinden biri olan 'Hücre Hasarı ve Nekroz - II' "
            "mikro-öğrenme destesini 100 adımda başarıyla tamamladınız.\n\n"
            "Bu destede:\n"
            "1. Kazeöz Nekroz (tüberküloz, amorf granüler, Langhans granülomu)\n"
            "2. Yağ Nekrozu (pankreatit, lipaz, sabunlaşma, gölge hücreler, meme travması)\n"
            "3. Fibrinoid Nekroz (damar duvarı, PAN, malign HT) ve Serum Biyobelirteçleri (CK-MB, ALT, AST, ALP)\n"
            "4. Apoptoz (ATP bağımlı, büzüşme, sıfır inflamasyon, embriyogenez, hormon çekilmesi, otoreaktif hücre elenmesi)\n"
            "5. Mitokondriyal Yol (BCL-2, BAX/BAK, MOMP, Sitokrom c, Apaptozom, Kaspaz-9)\n"
            "6. Dışsal Yol (Fas/CD95, DISC, Kaspaz-8, Bid köprüsü, FLIP)\n"
            "7. Efektör İnfaz (KASPAZ-3, CAD, 180-200 bç DNA Merdiveni)\n"
            "8. Yeni Ölüm Biçimleri (Nekroptoz / RIPK1-RIPK3-MLKL; Piroptoz / Kaspaz-1-IL-1-Ateş; Ferroptoz / Demir-GPX4)\n"
            "9. Otofaji (Atg genleri, Otofagozom, hayatta kalma)\n"
            "10. Biyokimyasal Hasar (p53 / Genom Bekçisi; ER Stresi / UPR / CHOP; Ca²⁺ Tufanı / 4 Yıkıcı Enzim; "
            "ROS / Fenton / Hidroksil Radikali; İskemik şema) konularının tamamını derinlemesine fethettiniz!\n\n"
            "> [MEZUNİYET SPOTU] Hücre hasarını moleküler mekanizmasıyla bilen hekim, tüm klinik hastalıkların "
            "ve farmakolojik tedavilerin kök nedenini kavramış demektir!"
        ),
        "medicalTerms": [
            {"term": "Hücre Hasarı Uzmanlığı", "explanation": "Nekroz, apoptoz ve moleküler mekanizmaları klinik olgularla tam bağdaştırabilme yetisi."},
            {"term": "Konsolide Bilgi Ağı", "explanation": "Patoloji, biyokimya, immünoloji ve kliniği birleştiren entegre tıp bilgisi."}
        ],
        "spotPearls": [
            "📌 [BÜYÜK FİNAL] Kazeöz = Tüberküloz. Yağ = Pankreatit / Sabunlaşma. Fibrinoid = Vaskülit / Malign HT.",
            "📌 [BÜYÜK FİNAL] Apoptoz = ATP bağımlı, membran sağlam, inflamasyon yok. İçsel = Kaspaz-9; Dışsal = Kaspaz-8; İnfazcı = Kaspaz-3.",
            "📌 [BÜYÜK FİNAL] DNA kırılması = 180-200 bç DNA merdiveni (CAD).",
            "📌 [BÜYÜK FİNAL] Nekroptoz = RIPK1/3/MLKL. Piroptoz = Kaspaz-1/IL-1/Ateş. Ferroptoz = Demir/GPX4.",
            "📌 [BÜYÜK FİNAL] En güçlü serbest radikal = Hidroksil radikali (Fenton reaksiyonu)."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-28",
                "Apoptozun içsel (mitokondriyal) ve dışsal (ölüm reseptörü) yolaklarının başlatıcı kaspazları ile ortak infazcı kaspazı sırasıyla nelerdir?",
                "İçsel yol başlatıcısı: KASPAZ-9; Dışsal yol başlatıcısı: KASPAZ-8; Ortak ana infazcı kaspaz: KASPAZ-3'tür."
            ),
            make_flashcard(
                "fc-k1-05-29",
                "Piroptoz ile Ferroptoz arasındaki temel tetikleyici mekanizma ve klinik/biyokimyasal fark nedir?",
                "Piroptoz inflamozom ve Kaspaz-1 ile IL-1 salıp yüksek ateşe yol açar; Ferroptoz ise demir (Fe²⁺) bağımlı lipid peroksidasyonu ve GPX4 inaktivasyonu ile seyreder."
            ),
            make_flashcard(
                "fc-k1-05-30",
                "Hücre hasarında Fenton reaksiyonu ile üretilen en güçlü serbest radikal hangisidir ve hücre içi kalsiyum artışının tetiklediği membran parçalayıcı enzim nedir?",
                "En güçlü serbest radikal Hidroksil radikalidir (•OH); kalsiyumla tetiklenen membran parçalayıcı enzim ise Fosfolipazdır."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Hücre Hasarı ve Nekroz - II Mega Sentez Matrisi",
                "headers": ["Patolojik Süreç", "Anahtar Moleküller / Enzimler", "Morfolojik Görünüm", "Klinik Yansıması"],
                "rows": [
                    ["Kazeöz Nekroz", " Aside Dirençli Basil, Mikolik Asit", "Amorf granüler pembe döküntü", "Tüberküloz, Ghon kompleksi, kavern"],
                    ["Yağ Nekrozu", "Pankreatik Lipaz, Ca2+ Tuzları", "Gölge adipositler, bazofilik kireç", "Akut pankreatit, tebeşir beyazı sabunlaşma"],
                    ["Fibrinoid Nekroz", "İmmün kompleksler, Fibrin", "Damar duvarında parlak pembe camsı bant", "Poliarteritis nodosa, Malign hipertansiyon"],
                    ["İçsel Apoptoz", "BCL-2, BAX/BAK, Sitokrom c, Kaspaz-9", "Hücre büzüşmesi, kromatin hilalleri", "DNA hasarı, kemoterapi, Foliküler lenfoma"],
                    ["Dışsal Apoptoz", "Fas (CD95), FasL, FADD, Kaspaz-8", "Apoptotik cisimcikler, Anneksin V (+)", "CTL infazı, otoreaktif hücre tasfiyesi"],
                    ["Nekroptoz", "RIPK1, RIPK3, MLKL oligomeri", "Nekroz gibi şişme ve membran yırtılması", "Kaspaz-8 yokluğunda TNF yanıtı, pankreatit"],
                    ["Piroptoz", "İnflamozom, Kaspaz-1, Gazdermin D", "Por açılması, IL-1 salınımı", "Hücre içi bakteri enfeksiyonları, yüksek ateş"],
                    ["Ferroptoz", "Fe2+, GPX4 iflası, peroksitler", "Mitokondri büzüşmesi, krista kaybı", "Nörodejenerasyon, kanser kemoterapisi"],
                    ["Otofaji", "Atg genleri, LC3-II, Lizozom", "Çift zarlı otofagozomlar", "Besin yoksunluğu, tümör kemodirenci"],
                    ["Serbest Radikal", "Süperoksit, Fenton / Hidroksil (•OH)", "Lipid peroksidasyonu, DNA kırıkları", "İskemi-reperfüzyon, radyasyon, toksinler"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Hücre Ölümü ve Hasar Bileşeni", "En Ayırt Edici Biyokimyasal İmzası", "Klinik Önemi"],
                [
                    [("Kazeöz Granülom", False, ""), ("Ziehl-Neelsen boyasında kırmızı ARB basilleri", True, "Aside dirençli basil tespiti"), ("Tüberküloz teşhisinin temeli", False, "")],
                    [("Yağ Saponifikasyonu", False, ""), ("Açığa çıkan yağ asitlerinin Ca2+ bağlaması", True, "Kalsiyum sabunu oluşumu"), ("Pankreatitte hipokalsemi riski", False, "")],
                    [("Fibrinoid Damar Nekrozu", False, ""), ("Antijen-antikor + Fibrin camsı bandı", True, "Mikroskobik vasküler lezyon"), ("PAN ve Malign Hipertansiyon teşhisi", False, "")],
                    [("Apoptoz DNA Merdiveni", False, ""), ("180-200 baz çifti katlarında internükleozomal kırılma", True, "CAD enzimi basamakları"), ("Apoptozun kesin biyokimyasal kanıtı", False, "")],
                    [("En Güçlü Serbest Radikal", False, ""), ("Fenton reaksiyonlu Hidroksil Radikali (•OH)", True, "Demir katalizli radikal"), ("Radyasyon ve reperfüzyon hasarı", False, "")]
                ]
            ),
            make_active_recall(
                "Kurul 1 Patoloji müfredatında öğrendiğiniz üzere, iskemik dokuda hücre zarının parçalanarak nekrozu kesinleştiren en kritik 3 patobiyokimyasal mekanizma nedir?",
                "1) ROS kaynaklı lipid peroksidasyonu, 2) ATP yetersizliğine bağlı fosfolipid sentezi durması ve 3) Sitozolik kalsiyum artışına bağlı fosfolipaz ve proteaz aktivasyonudur."
            )
        ]
    })

    return slides
