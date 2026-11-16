#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 10: Sitopatoloji, Moleküler Devrim ve Patolojinin Geleceği (Adımlar 90 - 100)
Ders: Tıbbi Patoloji - Patolojiye Giriş
Öğretim Üyesi: Prof. Dr. Hikmet Keleş
"""

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
        # Adım 90
        {
            "slideNumber": 90,
            "title": "Sitopatolojinin Temel Prensipleri ve Klinik Avantajları",
            "subtitle": "Sitopatoloji; doku bütünlüğü olmadan, tek tek hücrelerin ve hücre kümelerinin nükleer ve sitoplazmik morfolojisinden kesin tanı koyma sanatıdır.",
            "badge": "Sitopatoloji",
            "badgeColor": "cyan",
            "discipline": "Sitopatoloji",
            "synthesisNarrative": """==Sitopatoloji==; doku bütünlüğü ve stroma olmadan, tek tek hücrelerin ve hücre kümelerinin morfolojik ayrıntılarından tanı koyan patoloji dalıdır.

Klinik pratikteki temel amacı; minimal invazivite ile hızlı, güvenilir ve düşük maliyetli tanı sağlamaktır. Cerrahi kesi veya genel anestezi gerekmeden sürüntü veya ince enjektör iğnesiyle uygulanabilir. Doku takibi beklenmeden dakikalar veya saatler içinde sonuç verir ve asemptomatik lezyonları tarar. Sitopatolojinin temel sınırlılığı ise stroma ve doku mimarisinin izlenememesidir; hücrenin bazal membranı aşıp aşmadığı görülemediğinden karsinoma in situ ile invaziv karsinom ayrımında histopatolojik biyopsi doğrulaması gerekir.

> [SİTOLOJİ İLKESİ] Sitopatolojide stroma yoktur; tanı nükleus boyutu, kromatin yapısı ve N/S oranı üzerinden konur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hücre Düzeyinde Tanı", "desc": "Nükleer atipi, pleomorfizm ve N/S oranı üzerinden malignite değerlendirilir.", "isKey": True},
                    {"title": "Hızlı ve Düşük Maliyetli", "desc": "Poliklinik şartlarında dakikalar içinde uygulanabilen ekonomik bir yöntemdir.", "isKey": True},
                    {"title": "Stroma Yokluğu Sınırı", "desc": "Bazal membran invazyonu kanıtlanamadığı için bazen cerrahi biyopsi gerekir.", "isKey": False}
                ],
                "table": {
                    "title": "Sitopatoloji ile Histopatoloji Arasındaki Temel Farklar",
                    "headers": ["Parametre", "Sitopatoloji", "Histopatoloji"],
                    "rows": [
                        ["İncelenen Birim", "İzole tek hücreler veya küçük hücre grupları", "Hücreler + Hücreler arası stroma + Damarsal mimari"],
                        ["Örnekleme Yöntemi", "Sürüntü (smear), vücut sıvısı, İİAS (22G)", "Punch, forseps biyopsi, tru-cut, organ rezeksiyonu"],
                        ["Sonuç Süresi", "Dakikalar - birkaç saat", "24 - 48 saat (doku takibi şart)"],
                        ["İnvazyon Kanıtı", "Gösterilemez (yalnız hücresel malignite)", "Kesin olarak kanıtlanır (bazal membran aşımı)"],
                        ["Maliyet ve Travma", "Son derece düşük maliyet, minimal travma", "Daha yüksek maliyet, cerrahi invazyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sitopatoloji hücre düzeyinde inceleme yapar; stroma mimarisi ve bazal membran ilişkisi görülemez.",
                "📌 [KLİNİK SPOT] Sitopatolojinin en büyük başarısı minimal morbidite ile hızlı ve güvenilir tanı koymasıdır.",
                "💡 [ÖĞRENME İPUCU] Bir sitopatolog hücreye bakarken 'Çekirdek ne kadar büyümüş ve kromatini ne kadar kabalaşmış?' sorusunu sorar."
            ],
            "medicalTerms": [
                {"term": "Sitopatoloji", "explanation": "Hücrelerin nükleer ve sitoplazmik morfolojisini inceleyerek tanı koyan patoloji dalıdır."},
                {"term": "N/S Oranı", "explanation": "Çekirdek alanının sitoplazmaya oranıdır; malign hücrelerde nükleus büyüdükçe bu oran artar."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Sitopatoloji vs Histopatoloji Tanısal Karşılaştırması",
                    "Sitopatoloji (Hücresel İnceleme)",
                    "Histopatoloji (Doku Mimarisi)",
                    [
                        "Tek tek hücreler veya hücre tabakaları incelenir",
                        "Stroma, kolajen lifler ve damarsal yatak izlenemez",
                        "Bazal membran bütünlüğü görülemediğinden mikroinvazyon bilinemez",
                        "Anestezi gerekmez, poliklinikte dakikalar içinde uygulanır"
                    ],
                    [
                        "Hücreler, stroma ve doku katmanları bir bütün halinde görülür",
                        "Tümörün çevre bağ dokusuna ve damarlara invazyonu kanıtlanır",
                        "İn situ karsinom ile invaziv karsinom ayrımı kesinleşir",
                        "Doku takibi gerektirir, sonuç genellikle 24-48 saatte çıkar"
                    ]
                ),
                make_micro_quiz(
                    "Sitopatolojinin cerrahi histopatolojiye kıyasla en belirgin kısıtlılığı ve tanısal zayıflığı aşağıdakilerden hangisidir?",
                    {
                        "A": "Hücre çekirdeğinin büyüklüğünün ölçülememesi",
                        "B": "Doku mimarisi ve stroma bulunmadığından bazal membran invazyonunun gösterilememesi",
                        "C": "Hücrelerin hiçbir boyayı tutmaması",
                        "D": "Sonuç çıkış süresinin haftalarca sürmesi",
                        "E": "Hastaya genel anestezi verilmesinin şart olması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Sitopatoloji nükleer büyüme ve atipiyi değerlendirmede son derece başarılıdır.",
                        "B": "Doğru. Doku mimarisi ve stroma izlenemediğinden bazal membran invazyonu gösterilemez.",
                        "C": "Yanlış. Sitolojik örnekler PAP ve Giemsa boyalarıyla mükemmel boyanır.",
                        "D": "Yanlış. Sitopatoloji günler değil dakikalar veya saatler içinde hızlı sonuç verir.",
                        "E": "Yanlış. Sitolojik işlemler lokal anesteziyle veya anestezisiz kolayca uygulanır."
                    }
                ),
                make_cloze(
                    "Sitopatolojide malignite değerlendirmesinde en kritik kriter hücre çekirdeğinin sitoplazmaya oranını ifade eden N/S oranı olarak adlandırılır.",
                    "N/S oranı",
                    "Çekirdek/sitoplazma büyüklük oranının kısaltması"
                )
            ]
        },

        # Adım 91
        {
            "slideNumber": 91,
            "title": "Sitolojik Materyal Tipleri: Eksfolyatif vs Mekanik Örnekleme",
            "subtitle": "Sitolojik materyaller; vücut yüzeylerinden kendiliğinden dökülen (eksfolyatif) ve hekim tarafından fırça/iğneyle kazınan (mekanik) olmak üzere ikiye ayrılır.",
            "badge": "Materyal Tipleri",
            "badgeColor": "teal",
            "discipline": "Sitopatoloji",
            "synthesisNarrative": """Sitolojik numuneler elde ediliş yöntemlerine göre ==eksfolyatif sitoloji== ve ==mekanik (girişimsel) sitoloji== olmak üzere iki ana gruba ayrılır.

==Eksfolyatif Sitoloji==; epitel yüzeylerinden veya seröz zarlardan doğal olarak dökülen hücrelerin incelenmesidir. Rahim ağzı PAP smear sürüntüleri, plevra ve periton asit sıvıları, idrar hücreleri ve balgam bu gruptadır. ==Mekanik Örnekleme== ise kendiliğinden dökülmeyen hücrelerin hekim tarafından aletlerle toplanmasıdır. Şüpheli tümör yüzeyinin fırçalanması (brushing), hava yollarının yıkanması (lavaj/BAL) ve kitlelerden vakumla hücre çekilen ince iğne aspirasyon sitolojisi (İİAS) bu kategoriye girer.

> [METODOLOJİ] Eksfolyatif sitoloji dökülen hücreyi toplar; mekanik yöntemler ise hücreyi yüzeyden veya kitleden alır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Eksfolyatif (Dökülen)", "desc": "Serviks smear, idrar, balgam ve plevra/periton asit sıvıları.", "isKey": True},
                    {"title": "Mekanik (Girişimsel)", "desc": "Endoskopik fırçalama, lavaj (BAL) ve ince iğne aspirasyonu (İİAS).", "isKey": True},
                    {"title": "Tazelik Zorunluluğu", "desc": "İdrar ve plevra sıvıları beklerse hücreler hızla lizise uğrar; hızla santrifüj edilmelidir.", "isKey": False}
                ],
                "table": {
                    "title": "Eksfolyatif ve Mekanik Sitoloji Örneklerinin Dağılımı",
                    "headers": ["Kategori", "Örnek Türü", "Alınan Anatomik Bölge", "Klinikopatolojik Hedef"],
                    "rows": [
                        ["Eksfolyatif", "Servikal Smear (PAP)", "Uterus serviksi transformasyon zonu", "Serviks kanseri ve HPV ilişkili prekanseröz lezyon taraması"],
                        ["Eksfolyatif", "Plevral / Peritoneal Sıvı", "Toraks ve batın seröz boşlukları", "Metastatik adenokarsinom ve malign mezotelyoma tespiti"],
                        ["Eksfolyatif", "İdrar Sitolojisi", "Mesane ve üriner sistem lümeni", "Yüksek dereceli ürotelyal karsinom nüks taraması"],
                        ["Mekanik", "Bronşiyal Fırçalama", "Bronkoskopide santral bronş mukozası", "Akciğer skuamöz hücreli karsinom tanısı"],
                        ["Mekanik", "Bronkoalveoler Lavaj (BAL)", "Distal alveoler hava boşlukları", "İnterstisyel akciğer hastalıkları, Pneumocystis jirovecii"],
                        ["Mekanik", "İİAS (İnce İğne Aspiratı)", "Tiroid nodülü, meme, lenfadenopati", "Solid kitlelerden hücre çekilerek anestezi olmadan teşhis"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Servikal smear, idrar ve plevral sıvılar 'eksfolyatif' sitoloji; bronşiyal fırçalama ve İİAS ise 'mekanik' örneklemedir.",
                "📌 [TANI SPOTU] İdrar sitolojisi düşük dereceli karsinomlarda duyarsızdır ancak yüksek dereceli ürotelyal karsinom ve karsinoma in situ tanısında çok duyarlıdır.",
                "💡 [ÖĞRENME İPUCU] Vücut sıvıları laboratuvara ulaştığında santrifüj edilerek dipte çöken hücresel tortudan (sediment) yayma yapılır."
            ],
            "medicalTerms": [
                {"term": "Eksfolyatif Sitoloji", "explanation": "Vücut yüzeylerinden veya boşluklara kendiliğinden dökülen hücrelerin incelenmesidir."},
                {"term": "Bronkoalveoler Lavaj (BAL)", "explanation": "Distal hava yollarına salin verilip geri aspire edilmesiyle hücre ve etken toplanmasıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Sitolojik Yöntem ve Örnek Eşleştirmesi",
                    ["Numune Türü", "Sitoloji Sınıfı", "Klinik Örnekleme Şekli"],
                    [
                        [
                            ("Servikal PAP Smear", False),
                            ("Eksfolyatif Sitoloji", True, "Dökülen servikal epitel"),
                            ("Transformasyon zonundan spatul/fırça sürüntüsü", False)
                        ],
                        [
                            ("Bronş Fırçalama", False),
                            ("Mekanik Örnekleme", True, "Yüzeyden kazınan hücreler"),
                            ("Endoskopik fırçanın lezyona sürtülmesi", False)
                        ],
                        [
                            ("Tiroid Nodülü İİAS", False),
                            ("Girişimsel Sitoloji", True, "Vakumla çekilen hücreler"),
                            ("22G iğneyle negatif basınçlı aspirasyon", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdaki sitolojik materyallerden hangisi vücut yüzeyinden KENDİLİĞİNDEN DÖKÜLEN hücrelerin incelendiği 'Eksfolyatif Sitoloji' grubuna girer?",
                    {
                        "A": "Bronkoskopi sırasında kitleye fırça sürtülerek alınan bronş fırçalama örneği",
                        "B": "Tiroid soliter nodülüne 22G enjektör batırılarak yapılan ince iğne aspirasyonu",
                        "C": "Akciğer zarları arasında biriken plevral efüzyon sıvısı sitolojisi",
                        "D": "Ameliyat esnasında kitle yüzeyinden lam üzerine yapılan imprint (dokundurma)",
                        "E": "Deri lezyonuna yapılan punch biyopsi kesiti"
                    },
                    "C",
                    {
                        "A": "Yanlış. Bronş fırçalama fırça yardımıyla dokudan hücre kazınan mekanik bir yöntemdir.",
                        "B": "Yanlış. İİAS negatif basınçla dokudan hücre aspire edilen girişimsel mekanik tekniktir.",
                        "C": "Doğru. Plevral efüzyon seröz zara dökülen hücrelerin incelendiği doğal eksfolyatif sitolojidir.",
                        "D": "Yanlış. Doku imprinti lezyon yüzeyinin lama bastırılmasıyla yapılan mekanik dokundurmadır.",
                        "E": "Yanlış. Punch biyopsi hücre değil bütün doku parçasını alan histopatolojik yöntemdir."
                    }
                ),
                make_cloze(
                    "Vücut boşluklarına veya lümenlere kendiliğinden dökülen hücrelerin incelendiği sitoloji dalına eksfolyatif sitoloji adı verilir.",
                    "eksfolyatif sitoloji",
                    "Doğal dökülen hücreleri inceleyen sitoloji dalı"
                )
            ]
        },

        # Adım 92
        {
            "slideNumber": 92,
            "title": "Servikal Sitoloji ve PAP Smear Devrimi",
            "subtitle": "Dr. George Papanicolaou'nun 1943'te tanımladığı PAP testi; serviks kanserini erken yakalayarak tıp tarihindeki en başarılı tarama programı olmuştur.",
            "badge": "PAP Testi",
            "badgeColor": "pink",
            "discipline": "Sitopatoloji Tarihi",
            "synthesisNarrative": """Dr. George Papanicolaou ve Herbert Traut'un 1943'te tanımladığı ==PAP Smear Testi==; serviks kanserini öncü evrede yakalayan en başarılı halk sağlığı taramasıdır.

Serviks kanseri aniden gelişmez; invaziv forma dönüşmeden önce yıllar süren displazi ve preinvaziv lezyon (CIN) evrelerinden geçer. Bu neoplastik dönüşüm serviksteki çok katlı yassı epitel ile tek katlı prizmatik epitelin birleştiği ==Transformasyon Zonunda (Skuamokolumnar Bileşke)== başlar. Özel fırçalarla bu bölgeden dökülen hücreler toplanarak alkolde fikse edilir ve polikromatik PAP boyasıyla boyanır. Düzenli PAP smear tarama programları sayesinde gelişmiş ülkelerde serviks kanserine bağlı mortalite ==%70'ten fazla azalmıştır==.

> [HALK SAĞLIĞI ZAFERİ] PAP testi; kanseri henüz oluşmadan öncü displazi evresinde yakalayıp önleyen altın standarttır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Papanicolaou & Traut (1943)", "desc": "Servikal smear yöntemini tanımlayarak jinekolojik onkolojiyi dönüştürdüler.", "isKey": True},
                    {"title": "Transformasyon Zonu", "desc": "Skuamokolumnar bileşke HPV ve karsinogenezin başladığı kritik odaktır.", "isKey": True},
                    {"title": "%70 Mortalite Azalması", "desc": "Serviks kanseri ölümlerini dramatik olarak düşüren altın standart taramadır.", "isKey": False}
                ],
                "table": {
                    "title": "Servikal PAP Testinin Tarihsel ve Klinik Başarısı",
                    "headers": ["Parametre", "PAP Smear Öncesi Dönem", "PAP Smear Sonrası Dönem"],
                    "rows": [
                        ["Kanser Teşhis Evresi", "İleri evre, kanamalı, inoperabl invaziv karsinom", "Asemptomatik preinvaziv lezyon (CIN 1-3, karsinoma in situ)"],
                        ["Kadın Kanser Mortalitesi", "Kadınlarda en ölümcül ilk 3 kanserden biri", "Düzenli taranan toplumlarda alt sıralara gerilemiştir"],
                        ["Tedavi Yaklaşımı", "Radikal histerektomi ve palyatif radyoterapi", "Lokal leep/konizasyon ile organ koruyucu erken tedavi"],
                        ["Türkiye'deki Öncüsü", "Uygulanmıyordu", "1947'de Dr. Osman Nuri Aker tarafından Türkiye'ye getirildi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Servikal sitolojiyi (PAP smear) 1943 yılında Dr. George Papanicolaou ve Herbert Traut tanımlamıştır.",
                "📌 [KLİNİK SPOT] Servikal smear örneği mutlaka transformasyon zonunu (skuamokolumnar bileşkeyi) içermelidir; aksi halde yetersiz kabul edilir.",
                "💡 [ÖĞRENME İPUCU] PAP smear bir tarama testidir; biyopsi değildir. Şüpheli sonuçlarda kolposkopi eşliğinde servikal biyopsi yapılır."
            ],
            "medicalTerms": [
                {"term": "Transformasyon Zonu", "explanation": "Servikste yassı ve prizmatik epitelin birleştiği, neoplazinin başladığı kritik alandır."},
                {"term": "PAP Smear", "explanation": "Serviks transformasyon zonundan alınan hücrelerle prekanseröz lezyonların taranmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "PAP Testinin Kanser Önleme Zinciri",
                    [
                        "1. Örnekleme: Rahim ağzı transformasyon zonundan fırça ile hücresel sürüntü alınır",
                        "2. Alkol Fiksasyonu: Lam derhal %95 etil alkole daldırılarak nükleer şeffaflık sabitlenir",
                        "3. PAP Boyama: Polikromatik Papanicolaou boyasıyla çekirdek ve sitoplazma boyanır",
                        "4. Prekanseröz Tespit: İnvaziv karsinom öncesi displazi ve koilositoz atipisi yakalanır",
                        "5. Erken Müdahale: Lezyon basit bir lokal girişimle (LEEP) çıkarılarak kanser önlenir"
                    ]
                ),
                make_micro_quiz(
                    "1943 yılında Dr. George Papanicolaou ve Herbert Traut tarafından tıp dünyasına tanıtılan ve kadınlarda serviks karsinomu mortalitesini %70'ten fazla düşüren eksfolyatif sitoloji tarama yöntemi hangisidir?",
                    {
                        "A": "İdrar sitolojisi",
                        "B": "Servikal PAP Smear Testi",
                        "C": "Bronkoalveoler lavaj",
                        "D": "Balgam sitolojisi",
                        "E": "Kemik iliği aspirasyonu"
                    },
                    "B",
                    {
                        "A": "Yanlış. İdrar sitolojisi üriner sistem ürotelyal tümörlerinin taranmasında kullanılır.",
                        "B": "Doğru. Papanicolaou ve Traut'un geliştirdiği servikal PAP smear serviks kanseri taramasının temelidir.",
                        "C": "Yanlış. Bronkoalveoler lavaj alt solunum yolu enfeksiyonları ve interstisyel hastalıklarda uygulanır.",
                        "D": "Yanlış. Balgam sitolojisi santral yerleşimli akciğer tümörlerinin teşhisinde kullanılır.",
                        "E": "Yanlış. Kemik iliği aspirasyonu hematolojik malignitelerin teşhisinde kullanılır."
                    }
                ),
                make_cloze(
                    "Serviks kanserinin öncü lezyonlarının doğduğu ve PAP testinde mutlaka örneklenmesi gereken anatomik bölgeye transformasyon zonu adı verilir.",
                    "transformasyon zonu",
                    "Skuamokolumnar bileşkenin klinik anatomik adı"
                )
            ]
        },

        # Adım 93
        {
            "slideNumber": 93,
            "title": "Bethesda Sistemi: Servikal Sitolojik Raporlama Standartları",
            "subtitle": "Bethesda sistemi; servikal smear sonuçlarını uluslararası standart terminolojiyle sınıflayarak klinisyenin biyopsi veya takip kararını yönetir.",
            "badge": "Bethesda Sistemi",
            "badgeColor": "purple",
            "discipline": "Sitopatoloji",
            "synthesisNarrative": """==Bethesda Sistemi==; servikal sitoloji raporlarını uluslararası standart terminolojiyle sınıflayarak klinisyenin biyopsi ve takip kararlarını yönetir.

Rapor öncelikle örnek yeterliliğini değerlendirir; güvenilir inceleme için yeterli skuamöz hücre ve transformasyon zonunu temsil eden endoservikal hücreler aranır. Tanısal kategorilerde ==NILM== lezyon veya malignite negatifliğini simgeler. ==ASC-US== önemi belirsiz hafif atipiyi, ==ASC-H== yüksek dereceli lezyon dışlanamayan kuşkulu hücreleri ifade eder. ==LSIL==, HPV sitopatik etkisi (koilositoz) ve hafif displaziyi (CIN 1) kapsar. ==HSIL== ise karsinoma in situ (CIN 2-3) lezyonlarını içerir ve gecikmeden kolposkopik biyopsi gerektirir.

> [KLİNİK ALGORİTMA] Bethesda raporunda HSIL saptandığında hızla kolposkopi ve servikal biyopsi yapılmalıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Örnek Yeterliliği", "desc": "Yeterli skuamöz hücre ve transformasyon zonu hücresi şarttır.", "isKey": True},
                    {"title": "LSIL (CIN 1)", "desc": "HPV koilositik etkisi ve hafif displazidir; çoğu immün sistemle geriler.", "isKey": True},
                    {"title": "HSIL (CIN 2-3)", "desc": "Kanser öncüsü yüksek riskli lezyondur; acil kolposkopik biyopsi gerektirir.", "isKey": False}
                ],
                "table": {
                    "title": "Bethesda Sistemi Sitolojik Kategorileri ve Klinik Yönetim",
                    "headers": ["Bethesda Sitoloji Tanısı", "Histopatolojik Karşılığı", "HPV İlişkisi", "Klinik Yönetim Kararı"],
                    "rows": [
                        ["NILM", "Normal epitel veya reaktif tamir", "Genellikle HPV negatif", "Rutin 3-5 yıllık taramaya devam"],
                        ["ASC-US", "Hafif atipik hücreler (kuşkulu)", "Olası HPV enfeksiyonu", "Refleks Yüksek Riskli HPV DNA testi veya 1 yıl sonra tekrar"],
                        ["ASC-H", "HSIL olasılığı elenemeyen atipi", "Yüksek riskli HPV sıktır", "Doğrudan Kolposkopi ve biyopsi"],
                        ["LSIL", "Hafif Displazi / CIN 1 / Koilositoz", "HPV 6, 11, 16, 18 pozitif", "Yaşa göre kolposkopi veya HPV takibi"],
                        ["HSIL", "Orta-Ağır Displazi / CIN 2, CIN 3, CIS", "Yüksek riskli HPV (Tip 16, 18)", "Kesin Kolposkopi + Çoklu Biyopsi / LEEP"],
                        ["SCC", "İnvaziv Skuamöz Karsinom", "Onkojenik HPV", "Onkolojik cerrahi ve kemoradyoterapi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Servikal sitolojide HPV'nin karakteristik sitopatik etkisi olan 'perinükleer halo' ve nükleer hiperkromazi gösteren hücreye Koilosit (LSIL) denir.",
                "📌 [SINAV SPOTU] Bethesda sisteminde HSIL (High-grade Squamous Intraepithelial Lesion), histopatolojik olarak CIN 2 ve CIN 3 (karsinoma in situ)'a karşılık gelir.",
                "🚨 [KRİTİK UYARI] Bethesda raporunda endoservikal hücre bildirilmemişse transformasyon zonu örneklenememiş olabilir; klinik şüphede test tekrarlanır."
            ],
            "medicalTerms": [
                {"term": "Bethesda Sistemi", "explanation": "Servikal sitoloji sonuçlarını uluslararası standart kategorilerle bildiren rapor sistemidir."},
                {"term": "Koilosit", "explanation": "HPV enfeksiyonu sonucu geniş perinükleer halo ve nükleer hiperkromazi kazanan hücredir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Bethesda Kategorileri ve Klinik Karşılıkları",
                    ["Bethesda Kodu", "Biyolojik Anlamı", "Klinik Karar"],
                    [
                        [
                            ("ASC-US", False),
                            ("Önemi belirsiz atipik skuamöz hücreler", True, "Hafif kuşkulu hücresel değişim"),
                            ("Yüksek riskli HPV DNA testi istenir", False)
                        ],
                        [
                            ("LSIL (CIN 1)", False),
                            ("Düşük dereceli lezyon ve koilositoz", True, "HPV sitopatik etkisi"),
                            ("Yaşa göre kolposkopi veya 1 yıl sonra kontrol", False)
                        ],
                        [
                            ("HSIL (CIN 2/3)", False),
                            ("Yüksek dereceli intraepitelyal neoplazi", True, "Kanser öncüsü yüksek riskli lezyon"),
                            ("Acil kolposkopi ve servikal biyopsi", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "28 yaşındaki asemptomatik bir kadının rutin servikal PAP smear taramasında Bethesda sistemine göre 'HSIL (Yüksek Dereceli Skuamöz İntraepitelyal Lezyon)' rapor edilmiştir. Bu hastanın klinik yönetiminde yapılması gereken en doğru basamak hangisidir?",
                    {
                        "A": "Rapor önemsenmeyip 5 yıl sonra rutin kontrole çağrılmalıdır.",
                        "B": "Kolposkopi eşliğinde servikal biyopsi ve endoservikal küretaj yapılmalıdır.",
                        "C": "Doğrudan kemoterapi başlanmalıdır.",
                        "D": "Klinik otopsi istenmelidir.",
                        "E": "Yalnızca antibiyotik tedavisi verilmelidir."
                    },
                    "B",
                    {
                        "A": "Yanlış. HSIL invaziv kansere dönüşme riski yüksek bir lezyondur, takibe bırakılamaz.",
                        "B": "Doğru. HSIL varlığında kolposkopi eşliğinde biyopsi yapılarak CIN 2/3 varlığı doğrulanmalıdır.",
                        "C": "Yanlış. Histopatolojik doku biyopsisi yapılmadan malignite kemoterapisi verilemez.",
                        "D": "Yanlış. Otopsi yalnızca vefat etmiş kişilere uygulanan postmortem incelemedir.",
                        "E": "Yanlış. HSIL neoplastik bir öncü lezyondur, bakteriyel antibiyotik tedavisiyle gerilemez."
                    }
                ),
                make_cloze(
                    "HPV enfeksiyonunun servikal epitelde oluşturduğu geniş perinükleer halo ve nükleer hiperkromazi ile karakterize hücrelere koilosit adı verilir.",
                    "koilosit",
                    "HPV sitopatik etkisini gösteren tipik atipik hücre adı"
                )
            ]
        },

        # Adım 94
        {
            "slideNumber": 94,
            "title": "İnce İğne Aspirasyon Sitolojisi (İİAS) Detayları: Tiroid ve Derin Kitleler",
            "subtitle": "22 Gauge ince iğne ve ultrason eşliğinde; tiroid, meme, karaciğer ve pankreas kitlelerinden %90-95 doğrulukla hücresel tanı alınır.",
            "badge": "İİAS Detayları",
            "badgeColor": "cyan",
            "discipline": "Girişimsel Sitoloji",
            "synthesisNarrative": """==İnce İğne Aspirasyon Sitolojisi (İİAS)==; 22-25 Gauge enjektör iğnesiyle solid kitlelerden hücre çekilerek poliklinik şartlarında uygulanan minimal invaziv bir yöntemdir.

İnce lümenli iğne kullanımı damar travmasını ve aspiratın kanla dolmasını önler; kalın iğneler hücrelerin kan gölünde kaybolmasına yol açar. Yüzeyel kitlelerde palpasyonla, derin organ kitlelerinde ise mutlaka ==Ultrason (US) veya Bilgisayarlı Tomografi (BT)== eşliğinde hedefe girilerek uygulanır. Yeterli hücresel materyal alındığında tanısal doğruluğu ==%90 ila %95== arasındadır. Tiroid kitlelerinde Bethesda sınıflaması kullanılarak benign nodüller korunurken, malign şüpheli lezyonlar cerrahiye yönlendirilir.

> [KLİNİK DEĞERİ] İİAS 5 dakikada %90-95 doğrulukla ameliyat ihtiyacını belirleyen minimal invaziv tanı aracıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "22-25G İğne Standardı", "desc": "Aspiratın kanla kirlenmesini önlemek için ince lümenli iğne esastır.", "isKey": True},
                    {"title": "US/BT Kılavuzluğu", "desc": "Derin retroperitoneal ve intraabdominal organ kitlelerinde görüntüleme eşliğinde yapılır.", "isKey": True},
                    {"title": "%90-95 Doğruluk Oranı", "desc": "Cerrahi histopatolojiye yakın güvenilirlikle ameliyat kararını yönetir.", "isKey": False}
                ],
                "table": {
                    "title": "İİAS'ın Başlıca Organ Endikasyonları ve Doğruluk Oranları",
                    "headers": ["Hedef Organ / Lezyon", "Kılavuz Yöntemi", "Ortalama Tanısal Doğruluk", "Klinik Karar"],
                    "rows": [
                        ["Tiroid Nodülleri", "Ultrasonografi (US)", "%92 - 95", "Benign ise medikal takip; Malign ise total tiroidektomi cerrahisi"],
                        ["Boyun Lenfadenopatisi", "Palpasyon veya US", "%90 - 95", "Reaktif lenfadenit vs Malign lenfoma / Karsinom metastazı ayrımı"],
                        ["Pankreas Baş Kitleleri", "Endoskopik Ultrason (EUS)", "%88 - 92", "Duktal adenokarsinom vs Otoimmün kronik pankreatit ayrımı"],
                        ["Akciğer Pulmoner Nodül", "Toraks Tomografisi (BT)", "%85 - 90", "Primer akciğer karsinomu tanısı ve moleküler mutasyon analizi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İİAS'ta 22-25 Gauge iğneler kullanılır; uygun koşullarda tanısal doğruluğu %90-95'tir.",
                "📌 [KLİNİK SPOT] İİAS derin yerleşimli organlarda (akciğer, karaciğer, pankreas) mutlaka US veya BT kılavuzluğunda yapılır.",
                "💡 [ÖĞRENME İPUCU] İİAS materyalinde tanı koyacak kadar tiroid follikül hücresi yoksa sonuç 'Kategori I: Yetersiz' olarak raporlanır ve işlem tekrarlanır."
            ],
            "medicalTerms": [
                {"term": "EUS-FNA", "explanation": "Endoskopik ultrason iğnesiyle derin mediastinal ve pankreas kitlelerinden hücre çekilmesidir."},
                {"term": "Folliküler Neoplazi (Bethesda IV)", "explanation": "Tiroid İİAS'ında kapsül invazyonu görülemediğinden cerrahi rezeksiyon gerektiren kategoridir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Ultrason Eşliğinde Tiroid İİAS Zinciri",
                    [
                        "1. Sonografik Odaklama: Tiroiddeki şüpheli nodül ultrason probuyla netleştirilir",
                        "2. İğne Girişi: 22 Gauge ince iğne ultrason kılavuzluğunda nodül içine sokulur",
                        "3. Negatif Basınç: Enjektör pistonu çekilerek lezyondan hücresel materyal aspire edilir",
                        "4. Hızlı Fiksasyon: Lamlara yayılan hücreler bekletilmeden %95 alkol banyosuna aktarılır",
                        "5. Bethesda Raporu: Sitopatolog nükleer kriterleri inceleyerek malignite riskini bildirir"
                    ]
                ),
                make_micro_quiz(
                    "İnce İğne Aspirasyon Sitolojisi (İİAS) tekniğinde 16-18 Gauge gibi kalın iğneler yerine 22-25 Gauge ince iğnelerin tercih edilmesinin en temel patolojik nedeni nedir?",
                    {
                        "A": "İnce iğnelerin hastanede daha ucuz olması",
                        "B": "Kalın iğnelerin damarları parçalayarak aspiratı aşırı kanla doldurması ve tümör hücrelerinin kan gölü içinde kaybolmasını engellemek",
                        "C": "Kalın iğnelerin mikrotomda kesilememesi",
                        "D": "İnce iğnelerin sadece sıvı maddeleri çekebilmesi",
                        "E": "Formalin fiksatifinin ince iğneye daha kolay girmesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. İğne seçiminde belirleyici kriter maliyet değil tanısal hücre kalitesidir.",
                        "B": "Doğru. Kalın iğneler damarları yırtıp aspiratı kanla doldurarak tanısal hücreleri gizler.",
                        "C": "Yanlış. Aspirasyon iğneleri mikrotomda kesilen araçlar değildir.",
                        "D": "Yanlış. İnce iğneler katı tümör odaklarından da zengin hücresel kümeler toplayabilir.",
                        "E": "Yanlış. Formalin lam üzerine yayma yapıldıktan sonra kullanılan bir solüsyondur."
                    }
                ),
                make_cloze(
                    "İnce iğne aspirasyon sitolojisinde uygun teknik ve uzman sitopatolog eşliğinde tanısal doğruluk oranı yüzde 90-95 seviyesine ulaşır.",
                    "90-95",
                    "İİAS'ın tanısal doğruluk yüzdesi aralığı"
                )
            ]
        },

        # Adım 95
        {
            "slideNumber": 95,
            "title": "Sitolojik Fiksasyon ve Boyama: Alkol vs Havada Kurutma",
            "subtitle": "Sitolojik yaymalar; nükleer detaylar için alkolle fikse edilip PAP ile boyanırken, sitoplazma ve zemin için havada kurutulup Giemsa ile boyanır.",
            "badge": "Sitolojik Fiksasyon",
            "badgeColor": "indigo",
            "discipline": "Sitoteknoloji",
            "synthesisNarrative": """Sitolojik yaymalarda fiksasyon tercihi; nükleer atipinin mi yoksa sitoplazma ve zemin özelliklerinin mi inceleneceğini belirler.

==Islak Alkol Fiksasyonu==; yayma yapılır yapılmaz kurumadan derhal ==%95 Etil Alkol== içine daldırılmasıdır. Bu lamlar ==Papanicolaou (PAP)== ile boyanır; nükleer şeffaflık, kromatin ve nükleol detayları korunarak kanser atipisi saptanır. ==Havada Kurutma Fiksasyonu== ise lamın oda havasında kurutulup metanolle sabitlenmesidir. ==May-Grünwald-Giemsa (MGG)== ile boyanan bu preparatlarda sitoplazmik granüller, tiroid kolloidi ve müsin gibi zemin maddeleri çok net izlenir. İdeal bir İİAS'ta lamların yarısı alkole atılır, yarısı havada kurutulur.

> [TEKNİK KURAL] PAP boyası kurumamış yaş alkol fiksasyonu, Giemsa boyası ise havada kurutulmuş lam gerektirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Yaş Alkol Fiksasyonu", "desc": "%95 alkolde bekletilmeden fikse edilir; PAP boyasıyla nükleus şeffaflığı sağlar.", "isKey": True},
                    {"title": "Havada Kurutma", "desc": "Metanolle sabitlenip MGG ile boyanır; sitoplazma, granüller ve kolloid parlar.", "isKey": True},
                    {"title": "Kuruma Artefaktı", "desc": "Islak alkole geç atılan lamda kuruma artefaktı oluşur ve nükleuslar şişer.", "isKey": False}
                ],
                "table": {
                    "title": "Alkol Fiksasyonu ile Havada Kurutmanın Karşılaştırması",
                    "headers": ["Parametre", "Islak Alkol Fiksasyonu", "Havada Kurutma Fiksasyonu"],
                    "rows": [
                        ["Fiksatif Maddesi", "%95 Etanol (veya sprey fiksatif)", "Oda havasında hızlı kurutma + Saf Metanol"],
                        ["Uygulanan Boya", "Papanicolaou (PAP) boyası, HE", "May-Grünwald-Giemsa (MGG), Diff-Quik, Wright"],
                        ["En İyi Gösterdiği Yapı", "Hücre çekirdeği, kromatin ince yapısı, nükleol", "Sitoplazma miktarı, müsin, kolloid zemini, lipid damlaları"],
                        ["Kullanım Alanı", "Servikal PAP smear, solunum yolu, idrar", "Kemik iliği yaymaları, tiroid İİAS, lenf nodu sitolojisi"],
                        ["En Büyük Hata", "Havada kuruduktan sonra alkole atmak", "Yavaş kuruma nedeniyle hücrelerin otolize uğraması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Papanicolaou (PAP) boyası için lamlar ıslakken derhal %95 alkolde fikse edilmelidir.",
                "📌 [SINAV SPOTU] May-Grünwald-Giemsa (MGG) ve Diff-Quik boyaları için lamlar havada kurutularak hazırlanır.",
                "🚨 [KRİTİK UYARI] Alkol fiksasyonu yapılacak lam havada kurursa hücreler yapay olarak şişer ve 'yalancı kanser' atipisi oluşturur."
            ],
            "medicalTerms": [
                {"term": "Islak Fiksasyon", "explanation": "Sitoloji yaymasının kurumasına fırsat verilmeden derhal %95 alkole daldırılmasıdır."},
                {"term": "Romanowsky Boyaları", "explanation": "Havada kurutulmuş lamlarda sitoplazma ve zemin maddelerini boyayan Giemsa grubu boyalardır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Alkol Fiksasyonu (PAP) vs Havada Kurutma (MGG)",
                    "Alkol Fiksasyonu + PAP Boyası",
                    "Havada Kurutma + MGG Boyası",
                    [
                        "Yayma kurumadan anında %95 alkole daldırılır",
                        "Nükleer membran, kromatin dağılımı ve nükleol çok keskindir",
                        "Kanser taramalarında çekirdek atipisini kanıtlar",
                        "Sitoplazma şeffaf ve açık tonlarda boyanır"
                    ],
                    [
                        "Yayma odada sallanarak hızla havada kurutulur",
                        "Sitoplazmik granüller, müsin ve zemin maddesi çok nettir",
                        "Tiroid kolloidi ve hematolojik hücre ayrımında üstündür",
                        "Hücreler yayıldığı için nükleus boyutları daha geniş görünür"
                    ]
                ),
                make_micro_quiz(
                    "Servikal sürüntü veya tiroid aspirasyonunda Papanicolaou (PAP) boyası uygulanacak bir sitoloji lamında teknisyenin yaymayı yaptıktan sonra HİÇ BEKLEMEDEN hangi fiksatif içine daldırması zorunludur?",
                    {
                        "A": "Saf distile su",
                        "B": "%95 Etil Alkol (Etanol)",
                        "C": "Sıcak parafin (60°C)",
                        "D": "Ksilen",
                        "E": "Glutaraldehit"
                    },
                    "B",
                    {
                        "A": "Yanlış. Saf su hipotonik etkisiyle hücre zarlarını patlatarak lizise neden olur.",
                        "B": "Doğru. PAP boyası uygulanacak lamlar hücreler kurumadan derhal %95 etil alkole daldırılmalıdır.",
                        "C": "Yanlış. Sıcak parafin hücreleri pişirerek termal doku yanığı artefaktı yapar.",
                        "D": "Yanlış. Ksilen lam boyama ve kapatma basamaklarında kullanılan bir şeffaflaştırıcıdır.",
                        "E": "Yanlış. Glutaraldehit ışık sitolojisinde değil, elektron mikroskobunda kullanılan fiksatiftir."
                    }
                ),
                make_cloze(
                    "May-Grünwald-Giemsa ve Diff-Quik gibi sitolojik boyaların uygulanabilmesi için lamların alkole atılmadan havada kurutulması gerekir.",
                    "havada kurutulması",
                    "Giemsa boyası öncesi lamın hazırlanma biçimi"
                )
            ]
        },

        # Adım 96
        {
            "slideNumber": 96,
            "title": "Sıvı Bazlı Sitoloji (LBC) ve Hücre Bloğu (Cell Block) Yöntemi",
            "subtitle": "Sıvı bazlı sitoloji arka plan kan ve mukusunu temizlerken; hücre bloğu sitolojik sıvıları parafin bloğa dönüştürerek İHK yapma imkanı sağlar.",
            "badge": "Sitolojik Yenilikler",
            "badgeColor": "teal",
            "discipline": "Sitoteknoloji",
            "synthesisNarrative": """Sıvı bazlı sitoloji ve hücre bloğu; konvansiyonel sitolojinin kan, mukus ve stroma yokluğu kısıtlılıklarını aşan modern yeniliklerdir.

==Sıvı Bazlı Sitoloji (LBC)==; hücrelerin koruyucu sıvıya alınıp filtre edilmesiyle uygulanır. Eritrosit ve mukus temizlenir; hücreler lam üzerinde ==tek tabaka (monolayer)== halinde dizilir ve kalan sıvıdan HPV DNA'sı bakılabilir. ==Hücre Bloğu (Cell Block)== ise plevra veya periton sıvılarının santrifüj tortusunun pıhtılaştırılmasıdır. Doku takibinden geçirilip parafin bloğa gömülen bu hücresel pelletten seri kesitler alınarak cerrahi biyopsilerdeki gibi ==İHK antikor panelleri== ve moleküler testler çalışılabilir.

> [MODERN ENTEGRASYON] Hücre bloğu sitolojiyi histopatolojiye dönüştürür; efüzyonlarda sınırsız İHK paneline imkan tanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Temiz Monolayer Alan", "desc": "Sıvı bazlı sitoloji eritrosit ve mukusu temizleyerek hücreleri tek tabaka dizer.", "isKey": True},
                    {"title": "Hücre Bloğunda İHK", "desc": "Sitolojik sıvıdan elde edilen parafin blokla onlarca İHK antikor testi yapılabilir.", "isKey": True},
                    {"title": "Artık Sıvıdan DNA", "desc": "LBC flakonunda kalan sıvıdan tekrar hastayı çağırmadan HPV veya moleküler test çalışılır.", "isKey": False}
                ],
                "table": {
                    "title": "Konvansiyonel Yayma, Sıvı Bazlı Sitoloji ve Hücre Bloğu Karşılaştırması",
                    "headers": ["Yöntem", "Örnek Formatı", "Arka Plan Kirliliği (Kan/Mukus)", "İHK ve Moleküler Uygulama"],
                    "rows": [
                        ["Konvansiyonel Yayma", "Lama doğrudan yayma", "Yoğun kan ve mukus hücreleri örtebilir", "Çok kısıtlıdır; lam sayısı sınırlıdır"],
                        ["Sıvı Bazlı Sitoloji (LBC)", "Sıvı flakonunda filtre edilmiş tek tabaka", "Mükemmel temiz; kan ve mukus elenir", "Kalan sıvıdan HPV ve nükleik asit testleri yapılabilir"],
                        ["Hücre Bloğu (Cell Block)", "Santrifüj pelletinden parafin blok", "Tamamen doku kaseti formatındadır", "Rutin cerrahi biyopsi gibi sınırsız İHK ve FISH yapılabilir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sıvı bazlı sitoloji (LBC), kan ve mukus örtücülüğünü engelleyerek hücreleri lam üzerine tek tabaka (monolayer) halinde dizer.",
                "📌 [TANI SPOTU] Plevral ve peritoneal efüzyonlarda metastatik tümörün primer odağını İHK ile bulmak için mutlaka 'Hücre Bloğu' (Cell Block) hazırlanmalıdır.",
                "💡 [ÖĞRENME İPUCU] Akciğer adenokarsinomu plevra sıvısına metastaz yaptığında, hücre bloğu sayesinde hastadan yeniden invaziv biyopsi almadan EGFR mutasyonu bakılabilir."
            ],
            "medicalTerms": [
                {"term": "Sıvı Bazlı Sitoloji (LBC)", "explanation": "Hücreleri kan ve mukustan arındırarak lama tek tabaka dizen modern sitoloji yöntemidir."},
                {"term": "Hücre Bloğu (Cell Block)", "explanation": "Sitolojik sıvı pelletinin parafine gömülerek İHK yapılmasına olanak tanıyan blok formatıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Plevra Sıvısından Hücre Bloğu ve İHK Tanı Zinciri",
                    [
                        "1. Sıvı Santrifüjü: Plevral sıvı santrifüj edilerek hücresel pellet tüpün dibine çöktürülür",
                        "2. Pellet Pıhtılaştırma: Dibe çöken hücreler plazma-trombin ile karıştırılıp pıhtılaştırılır",
                        "3. Doku Takibi: Hücre pıhtısı kasede konup dehidrasyon, ksilen ve parafine sokulur",
                        "4. Mikrotom Kesimi: Elde edilen parafin hücre bloğundan mikrotomla seri kesitler alınır",
                        "5. İHK Tanısı: Kesitlere TTF-1 ve Kalretinin boyanarak karsinom-mezotelyoma ayrımı netleştirilir"
                    ]
                ),
                make_micro_quiz(
                    "Plevral efüzyon sıvısı sitolojisinde malign hücreler saptanan bir hastada, bu tümör hücrelerinin akciğer adenokarsinomu mu yoksa plevranın primer malign mezotelyoması mı olduğunu ayırt etmek için çok sayıda İmmünohistokimyasal (İHK) antikor paneli uygulanmak istenmektedir. Bu amaçla laboratuvarda hazırlanması gereken en uygun sitolojik preparat formatı hangisidir?",
                    {
                        "A": "Sadece tek bir lam üzerine havada kurutulmuş yayma",
                        "B": "Sıvı santrifüj tortusundan hazırlanan parafin Hücre Bloğu (Cell Block)",
                        "C": "Klinik otopsi",
                        "D": "Deri punch biyopsisi",
                        "E": "Taze dondurulmuş frozen kesit"
                    },
                    "B",
                    {
                        "A": "Yanlış. Tek bir yayma lamı üzerinde onlarca farklı İHK antikoru uygulamak teknik olarak imkansızdır.",
                        "B": "Doğru. Hücre bloğu sıvıyı parafin bloğa çevirerek sınırsız sayıda İHK kesiti alınmasını sağlar.",
                        "C": "Yanlış. Klinik otopsi yaşayan hastalarda değil, vefat sonrası uygulanan postmortem yöntemdir.",
                        "D": "Yanlış. Punch biyopsi deri lezyonlarına uygulanan cerrahi bir histopatoloji yöntemidir.",
                        "E": "Yanlış. Sıvı numuneler mikrotomda dondurularak kesilemez, önce hücre bloğu yapılmalıdır."
                    }
                ),
                make_cloze(
                    "Sitolojik sıvıların santrifüj tortusunun pıhtılaştırılarak parafine gömülmesi ve İHK testlerine olanak sağlaması yöntemine hücre bloğu adı verilir.",
                    "hücre bloğu",
                    "Sıvılardan parafin blok elde etme tekniği"
                )
            ]
        },

        # Adım 97
        {
            "slideNumber": 97,
            "title": "Solunum ve Vücut Boşlukları Sitolojisi",
            "subtitle": "Balgam ve bronkoalveoler lavaj derin akciğer parankimini tararken; plevra ve asit sıvıları seröz boşluklardaki gizli karsinom metastazlarını yakalar.",
            "badge": "Efüzyon Sitolojisi",
            "badgeColor": "blue",
            "discipline": "Sitopatoloji",
            "synthesisNarrative": """Solunum yolları ve seröz boşluk sitolojisi; derin akciğer parankimi ve seröz zarlardaki gizli karsinom metastazlarını yakalar.

==Balgam (Sputum) Sitolojisi==; santral akciğer tümörlerinde öksürükle atılan hücreleri inceler. Örneği tükürükten ayıran geçerlilik kriteri ==alveoler makrofajların== varlığıdır. Fırsatçı enfeksiyonlarda (Pneumocystis jirovecii) bronkoalveoler lavaj (BAL) kullanılır. ==Seröz Boşluk Sıvılarında (Plevra, Periton)== ise en kritik basamak; iltihapta irileşen ==reaktif mezotel hücreleri== ile ==metastatik adenokarsinom== ayrımıdır. Bu ayrımda mezotelyal Kalretinin/WT1 ile karsinoma özgü CEA/EpCAM panelleri kullanılır.

> [TANI İNCİSİ] Balgamda alveoler makrofaj görülmezse örnek tükürük kabul edilir ve tanı verilmeden tekrarlanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Balgamda Makrofaj Şartı", "desc": "Alveoler makrofaj içermeyen balgam örneği tükürük sayılır ve reddedilir.", "isKey": True},
                    {"title": "Malign Efüzyon Tanısı", "desc": "Plevra ve periton sıvısında metastatik adenokarsinom kümesi aranır.", "isKey": True},
                    {"title": "Mezotel vs Karsinom", "desc": "Reaktif mezotel kanseri taklit edebilir; ayırıcı tanıda Kalretinin ve CEA kullanılır.", "isKey": False}
                ],
                "table": {
                    "title": "Solunum ve Efüzyon Sitolojisi Tanı Kriterleri",
                    "headers": ["Materyal", "Geçerlilik Kriteri", "En Sık Tanı Konulan Patoloji"],
                    "rows": [
                        ["Balgam (Sputum)", "Karbon yüklü alveoler makrofaj varlığı", "Santral yerleşimli skuamöz hücreli akciğer karsinomu"],
                        ["Bronkoalveoler Lavaj", "Distal hava yollarından bol makrofaj", "Pneumocystis jirovecii kistleri (Grocott boyası ile), sarkoidoz"],
                        ["Plevral Sıvı", "Santrifüj sedimentinde hücresellik", "Meme ve akciğer adenokarsinom metastazı, malign mezotelyoma"],
                        ["Peritoneal Sıvı (Asit)", "Girdap şeklinde hücre kümeleri", "Over karsinomu ve gastrointestinal adenokarsinom yayılımı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Balgam (sputum) sitolojisinin tanısal açıdan yeterli ve alt solunum yollarını temsil ettiğini gösteren hücre Alveoler Makrofajdır.",
                "📌 [SINAV SPOTU] Plevral sıvıda reaktif mezotel hücrelerini metastatik adenokarsinomdan ayırmak için mezotelyal belirteç Kalretinin kullanılır.",
                "💡 [ÖĞRENME İPUCU] Over kanseri şüpheli kadınlarda ameliyat esnasında batın açılır açılmaz periton yıkama sıvısı (peritoneal lavaj) alınarak evreleme yapılır."
            ],
            "medicalTerms": [
                {"term": "Alveoler Makrofaj", "explanation": "Balgamın tükürük değil derin solunum yolu örneği olduğunu kanıtlayan fagositik hücredir."},
                {"term": "Kalretinin", "explanation": "Reaktif ve neoplastik mezotel hücrelerini karsinomdan ayıran pozitif belirteç proteindir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Plevra Sıvısında Reaktif Mezotel vs Metastatik Adenokarsinom",
                    "Reaktif Mezotel Hücreleri",
                    "Metastatik Adenokarsinom Hücreleri",
                    [
                        "Hücreler arasında 'pencerelenme' (windowing) boşlukları vardır",
                        "Nükleuslar yuvarlak, santral ve nükleol düzenlidir",
                        "Mezotelyal belirteç olan Kalretinin ve WT1 ile pozitif boyanır",
                        "Benign inflamasyona sekonder gelişen reaktif çoğalmadır"
                    ],
                    [
                        "Hücreler üç boyutlu sıkı küreler ve morulalar şeklinde kümelenir",
                        "Nükleuslar eksantrik, aşırı pleomorfik ve atipiktir",
                        "Karsinom belirteçleri (MOC-31, CEA, EpCAM) ile pozitif boyanır",
                        "Uzak organdan seröz zara atlamış gerçek kanser metastazıdır"
                    ]
                ),
                make_micro_quiz(
                    "Akciğer kanseri şüphesiyle poliklinikten patolojiye gönderilen bir balgam (sputum) sitolojisi preparatını inceleyen patolog, örnekte sadece yassı epitel hücreleri ve bakteriler görmüş, hiç 'alveoler makrofaj' saptamamıştır. Patoloğun bu numuneyle ilgili kararı ne olmalıdır?",
                    {
                        "A": "Hastada kesinlikle akciğer kanseri olmadığı rapor edilmelidir.",
                        "B": "Örnek alt solunum yollarını temsil etmemektedir (tükürüktür); 'yetersiz materyal' olarak raporlanıp derin balgam örneği tekrar istenmelidir.",
                        "C": "Hastaya acil kemoterapi başlanmalıdır.",
                        "D": "Numuneye derhal Masson trikrom boyası yapılmalıdır.",
                        "E": "Tümör evresi pT1 olarak kabul edilmelidir."
                    },
                    "B",
                    {
                        "A": "Yanlış. Alveoler materyale ulaşılamadığından kanser olasılığı güvenle dışlanamaz.",
                        "B": "Doğru. Makrofaj içermeyen balgam tükürük sayılır; yetersiz olarak raporlanıp yeni örnek istenir.",
                        "C": "Yanlış. Geçerli bir sitolojik tanı olmadan hastaya onkolojik tedavi başlanamaz.",
                        "D": "Yanlış. Masson trikrom bağ dokusu kollajenini gösteren histopatolojik bir boyadır.",
                        "E": "Yanlış. Yetersiz sitolojik örnek üzerinden tümör TNM evrelemesi yapılamaz."
                    }
                ),
                make_cloze(
                    "Balgam sitolojisinin alt solunum yollarını temsil eden kaliteli bir materyal olduğunu kanıtlayan hücresel kriter alveoler makrofaj varlığıdır.",
                    "alveoler makrofaj",
                    "Balgamın geçerlilik kanıtı olan fagositik hücre"
                )
            ]
        },

        # Adım 98
        {
            "slideNumber": 98,
            "title": "Patolojinin Geleceği I: Moleküler Biyobelirteçler, NGS ve Likit Biyopsi",
            "subtitle": "Kişiselleştirilmiş onkoloji çağında patoloji; Yeni Nesil Dizileme (NGS) ve kanda serbest tümör DNA'sını yakalayan likit biyopsiyle geleceği şekillendiriyor.",
            "badge": "Geleceğin Patolojisi",
            "badgeColor": "emerald",
            "discipline": "Moleküler Patoloji",
            "synthesisNarrative": """21. yüzyıl patolojisi; Yeni Nesil Dizileme (NGS) ve periferik kandan ctDNA izole eden likit biyopsiyle moleküler tıp çağına geçmiştir.

==Yeni Nesil Dizileme (NGS)==; tek bir biyopsi dokusundan elde edilen nükleik asitler üzerinde eşzamanlı olarak yüzlerce onkogeni (EGFR, ALK, KRAS, BRAF) 48 saat içinde diziler. Patolog hastaya hangi akıllı ilacın verileceğini belirleyen prediktif biyobelirteçleri raporlar. ==Likit Biyopsi== ise cerrahi invazivliği ortadan kaldırarak koldan alınan kanda dolaşan ==serbest tümör DNA'sını (ctDNA)== analiz eder. Tedavi altındaki hastada yeniden doku biyopsisi yapmadan, kanda ortaya çıkan direnç mutasyonları (ör. EGFR T790M) basit bir kan tahliliyle anlık olarak izlenir.

> [MOLEKÜLER ÇAĞ] Patoloji artık yalnızca doku morfolojisi değil; kandan genetik mutasyon izleyen moleküler kılavuzdur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "NGS Panelleri", "desc": "Tek seferde yüzlerce kanser genini eşzamanlı haritalayan yüksek teknolojili dizilemedir.", "isKey": True},
                    {"title": "Likit Biyopsi (ctDNA)", "desc": "Koldan alınan kanda dolaşan tümör DNA'sından cerrahisiz mutasyon analizi yapılır.", "isKey": True},
                    {"title": "Direnç Takibi", "desc": "Tedavi esnasında gelişen ikincil direnç mutasyonları kandan anlık izlenir.", "isKey": False}
                ],
                "table": {
                    "title": "Klasik Doku Biyopsisi ile Likit Biyopsi Karşılaştırması",
                    "headers": ["Parametre", "Klasik Doku Biyopsisi", "Likit Biyopsi (ctDNA)"],
                    "rows": [
                        ["Örnek Kaynağı", "Tümör dokusu (tru-cut, forseps, rezeksiyon)", "Periferik koldan alınan venöz kan (plazma)"],
                        ["İnvazivite ve Risk", "İnvaziv girişim; kanama ve pnömotoraks riski taşır", "Minimal invaziv; basit kan alma işlemi"],
                        ["Tekrarlanabilirlik", "Zor, ağrılı ve maliyetli", "Tedavi boyunca haftalık veya aylık sınırsız tekrarlanabilir"],
                        ["Tümör Heterojenitesi", "Yalnızca iğnenin girdiği küçük odağı yansıtır", "Vücuttaki tüm primer ve metastaz odaklarının DNA'sını kapsar"],
                        ["Doku Mimarisi", "Mükemmel mimari ve İHK sağlar", "Doku mimarisi yoktur; yalnız nükleik asit analiz edilir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Periferik kanda dolaşan serbest tümör DNA'sının (ctDNA) analiz edilerek cerrahi olmadan mutasyonların saptanmasına Likit Biyopsi denir.",
                "📌 [TEKNOLOJİ SPOTU] NGS (Yeni Nesil Dizileme), tek bir formalin-parafin dokusundan onlarca onkogeni eşzamanlı haritalar.",
                "💡 [ÖĞRENME İPUCU] Akciğer kanserli hasta akıllı ilaç alırken tümör nüksettiğinde, yeniden akciğer biyopsisi yapmak yerine likit biyopsiyle kandan direnç mutasyonu (T790M) taranır."
            ],
            "medicalTerms": [
                {"term": "Likit Biyopsi", "explanation": "Kanda dolaşan serbest tümör DNA'sından cerrahisiz mutasyon analizi yapan testtir."},
                {"term": "NGS (Next-Generation Sequencing)", "explanation": "Yüzlerce kanser genini eşzamanlı dizileyerek kapsamlı mutasyon profili çıkaran teknolojidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Likit Biyopsi ile Direnç Mutasyonu Yakalama Zinciri",
                    [
                        "1. ctDNA Salınımı: Apoptoza uğrayan kanser hücreleri kanda serbest tümör DNA'sı bırakır",
                        "2. Venöz Kan Alımı: Akıllı ilaç kullanan hastadan basit bir tüp periferik kan alınır",
                        "3. Plazma İzolasyonu: Santrifüjle hücresel elemanlar çökertilerek plazma ctDNA'sı izole edilir",
                        "4. NGS Analizi: Kanda düşük oranda bulunan mutant DNA dizileri çoğaltılıp dizilenir",
                        "5. Hedefe Yönelik Tedavi: Direnç mutasyonu saptandığında cerrahisiz olarak yeni kuşak ilaca geçilir"
                    ]
                ),
                make_micro_quiz(
                    "İleri evre akciğer adenokarsinomu nedeniyle hedefe yönelik akıllı ilaç kullanan bir hastada tedaviye direnç geliştiğinde, hastaya yeniden invaziv akciğer biyopsisi yapmadan koldan alınan venöz kanda dolaşan serbest tümör DNA'sı (ctDNA) üzerinden mutasyon analizi yapan modern yönteme ne ad verilir?",
                    {
                        "A": "Punch biyopsi",
                        "B": "Likit Biyopsi (Liquid Biopsy)",
                        "C": "Klinik otopsi",
                        "D": "Masson trikrom boyaması",
                        "E": "Frozen kesit"
                    },
                    "B",
                    {
                        "A": "Yanlış. Punch biyopsi deriden parça alan cerrahi bir histopatolojik yöntemdir.",
                        "B": "Doğru. Likit biyopsi kanda dolaşan ctDNA parçacıklarından cerrahisiz mutasyon analizi yapan yöntemdir.",
                        "C": "Yanlış. Klinik otopsi vefat eden kişilerin ölüm nedenini belirleyen postmortem incelemedir.",
                        "D": "Yanlış. Masson trikrom boyası dokudaki kolajen liflerini maviye boyayan histokimyasal yöntemdir.",
                        "E": "Yanlış. Frozen kesit ameliyat esnasında dokuyu dondurarak dakikalar içinde incelenen tekniktir."
                    }
                ),
                make_cloze(
                    "Periferik kanda dolaşan serbest tümör DNA parçacıklarının analiz edilmesiyle cerrahisiz genetik takip sağlayan yönteme likit biyopsi adı verilir.",
                    "likit biyopsi",
                    "Kandan tümör genetik analizi yapan modern testin adı"
                )
            ]
        },

        # Adım 99
        {
            "slideNumber": 99,
            "title": "Patolojinin Geleceği II: Dijital Patoloji, WSI ve Yapay Zekâ (AI)",
            "subtitle": "Tüm Slayt Görüntüleme (WSI) ile cam lamlar gigapiksel dijital dosyalara dönüşmekte; yapay zekâ algoritmaları mitoz ve Ki-67'yi hatasız saymaktadır.",
            "badge": "Dijital Patoloji",
            "badgeColor": "blue",
            "discipline": "Dijital Patoloji ve AI",
            "synthesisNarrative": """==Dijital Patoloji ve Yapay Zekâ (AI)==; Tüm Slayt Görüntüleme (WSI) teknolojisiyle cam lamları gigapiksel verilere dönüştürerek tanı sürecini modernize eder.

Lam tarayıcıları preparatları saniyeler içinde tarayarak monitörde incelenebilir WSI dosyalarına çevirir. Bu sayede ==telepatoloji== ile görüntüler uzaktaki uzmanlara iletilerek anında konsültasyon yapılır. ==Yapay Zekâ ve Derin Öğrenme== ise gözle sayması güç olan Ki-67 proliferasyon indeksini ve mitotik figürleri on binlerce hücreyi tek tek sayarak nesnel yüzdeyle hesaplar. Ayrıca lenf nodlarındaki mikrometastaz odaklarını kırmızı çerçeveyle işaretler ve rutin kesitten mutasyon tahmini yapar.

> [YENİ ÇAĞ] Yapay zekâ patoloğun yerini almayacak; ancak yapay zekâyı kullanan hekimler tanı kalitesini artıracaktır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "WSI (Tüm Slayt Görüntüleme)", "desc": "Cam lamlar gigapiksel dijital verilere taranarak monitörden incelenir.", "isKey": True},
                    {"title": "Telepatoloji", "desc": "Sınırlar kalkar; dijital preparat dünya çapında anında konsülte edilir.", "isKey": True},
                    {"title": "AI ile Hatasız Skorlama", "desc": "Ki-67 indeksi, mitoz sayısı ve HER2 skorlaması yapay zekâ ile standartlaşır.", "isKey": False}
                ],
                "table": {
                    "title": "Geleneksel Işık Mikroskopisi ile Dijital ve AI Destekli Patoloji",
                    "headers": ["Özellik", "Geleneksel Işık Mikroskopisi", "Dijital Patoloji ve Yapay Zekâ (AI)"],
                    "rows": [
                        ["Görüntüleme Ortamı", "Cam lam ve optik mikroskop oküleri", "Dijital taranmış WSI dosyası ve tıbbi monitör"],
                        ["Konsültasyon Hızı", "Lamların kargoyla veya postayla günlerce taşınması", "İnternet üzerinden saniyeler içinde telepatoloji konsültasyonu"],
                        ["Kantitatif Sayım (Ki-67 / Mitoz)", "Gözle manuel tahmin (öznellik ve hata payı yüksek)", "Yapay zekâ algoritmasıyla on binlerce hücrenin nesnel tam sayımı"],
                        ["Arşivleme Güvenliği", "Cam lamların kırılma, solma ve depoda kaybolma riski", "Bulut sunucularda bozulmadan sonsuza dek dijital saklama"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [TEKNOLOJİ SPOTU] Cam lamların yüksek çözünürlükte taranarak dijital ortama aktarılmasına WSI (Whole Slide Imaging - Tüm Slayt Görüntüleme) denir.",
                "📌 [SINAV SPOTU] Dijital patolojide yapay zekâ en çok Ki-67 indeksi hesaplama, mitoz sayımı ve HER2 skorlamasında standartlaştırıcı rol oynar.",
                "💡 [ÖĞRENME İPUCU] Telepatoloji sayesinde ameliyathanedeki frozen kesit, hastanede patolog olmasa bile başka şehirdeki patoloji merkezinden anında raporlanabilir."
            ],
            "medicalTerms": [
                {"term": "WSI (Whole Slide Imaging)", "explanation": "Cam lamın taranarak monitörde incelenebilir gigapiksel dijital görüntüye dönüştürülmesidir."},
                {"term": "Telepatoloji", "explanation": "Dijital lamların internet üzerinden iletilerek uzaktan konsültasyon yapılması yöntemidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Geleneksel Mikroskopi vs Dijital ve Yapay Zekâlı Patoloji",
                    "Geleneksel Optik Mikroskopi",
                    "Dijital Patoloji ve Yapay Zekâ (AI)",
                    [
                        "Hekim fiziksel olarak mikroskop başına oturmak zorundadır",
                        "Ki-67 pozitif hücre yüzdesi hekimin göz kararı tahminiyle belirlenir",
                        "Konsültasyon için cam preparatların kargoyla gitmesi beklenir",
                        "Cam lamlar zamanla solabilir, kırılabilir veya arşivde kaybolabilir"
                    ],
                    [
                        "WSI dosyaları bulut üzerinden her yerden monitörde incelenebilir",
                        "Yapay zekâ 50.000 hücreyi sayarak Ki-67 indeksini %34.2 olarak tam verir",
                        "Telepatoloji ile dünyanın en yetkin merkezinden anında 2. görüş alınır",
                        "Dijital görüntüler veri tabanında kalite kaybı olmadan sonsuza dek saklanır"
                    ]
                ),
                make_micro_quiz(
                    "Modern patolojide cam mikroskop lamlarının yüksek çözünürlüklü dijital tarayıcılarla taranarak monitör üzerinde gigapiksel düzeyinde incelenmesini ve yapay zekâ algoritmalarıyla otomatik hücre sayımı yapılmasını sağlayan teknolojiye ne ad verilir?",
                    {
                        "A": "Rotary mikrotomi",
                        "B": "Tüm Slayt Görüntüleme (WSI - Whole Slide Imaging)",
                        "C": "Kriostat kesit tekniği",
                        "D": "Parafin infiltrasyonu",
                        "E": "Dehidrasyon serisi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Rotary mikrotomi parafin bloklardan fiziksel ince kesit alan mekanik aygıttır.",
                        "B": "Doğru. WSI lamları tarayarak bilgisayara aktarır ve yapay zekâ analizlerine olanak sağlar.",
                        "C": "Yanlış. Kriostat intraoperatif dondurma kesiti yapan dondurucu mikrotom cihazıdır.",
                        "D": "Yanlış. Parafin infiltrasyonu doku takibinde mum emdirme aşamasıdır.",
                        "E": "Yanlış. Dehidrasyon dokudan suyun alkolle çekildiği kimyasal takip basamağıdır."
                    }
                ),
                make_cloze(
                    "Cam lamların dijital ortama taranarak monitörden incelenmesini ve telepatoloji yapılmasını sağlayan teknolojiye Tüm Slayt Görüntüleme veya İngilizce kısaltmasıyla WSI adı verilir.",
                    "WSI",
                    "Whole Slide Imaging teknolojisinin evrensel kısaltması"
                )
            ]
        },

        # Adım 100: [TEKRAR SAYFASI - CHECKPOINT 10]
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Sitopatoloji, Moleküler Devrim ve Patolojinin Geleceği",
            "subtitle": "Dersin büyük final sentezi: Eksfolyatif sitoloji, Bethesda sistemi, İİAS, sıvı bazlı sitoloji, hücre bloğu, NGS, likit biyopsi ve dijital patoloji.",
            "badge": "Final Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 10,
            "synthesisNarrative": """Bu final kontrol noktası; sitopatoloji, moleküler onkoloji ve dijital patolojinin modern tanısal gücünü birleştiren büyük sentez istasyonudur.

Sitopatoloji; stroma olmadan tek tek hücrelerin morfolojisinden hızla tanı koyar. Servikal PAP smear Bethesda sistemiyle prekanseröz lezyonları tararken, İİAS %90-95 doğrulukla ameliyat ihtiyacını belirler. Sıvı bazlı sitoloji hücresel zemini temizler; Hücre Bloğu ise sıvıları parafine gömerek İHK panelleri sunar. Patolojinin geleceğinde iki güç yükselmektedir: Kanser genlerini haritalayan NGS ve kandan tümör DNA'sı izleyen Likit Biyopsi (ctDNA); diğer yanda ise camı ekrana taşıyan WSI, telepatoloji ve Ki-67'yi nesnel sayan yapay zekâ.

> [BÜYÜK SÖZ] Patoloji; hücre morfolojisinden kanda ctDNA dizileyen yapay zekâlı dijital platformlara uzanan temel tıp pusulasıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Sitopatoloji İlkeleri", "desc": "Eksfolyatif/mekanik sitoloji, 22G İİAS, Bethesda raporlaması, LBC ve Hücre Bloğu.", "isKey": True},
                    {"title": "Moleküler Devrim", "desc": "NGS panelleri, hedefe yönelik akıllı tedaviler ve kandan Likit Biyopsi (ctDNA).", "isKey": True},
                    {"title": "Dijital Gelecek", "desc": "WSI, telepatoloji ve yapay zekâ destekli otomatik nükleer skorlama.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 10 ve Tüm Dersin Büyük Metodolojik Sentez Tablosu",
                    "headers": ["Yöntem / Alan", "Temel Materyal / Araç", "Sağladığı Kritik Bilgi", "Klinik Rolü"],
                    "rows": [
                        ["PAP Smear Sitolojisi", "Servikal transformasyon zonu", "Bethesda sistemi: LSIL (CIN1), HSIL (CIN2/3)", "Serviks kanserini oluşmadan önleyen tarama zaferi"],
                        ["İİAS Sitolojisi", "22-25G ince iğne aspiratı", "Tiroid ve lenf nodlarında nükleer atipi", "Poliklinikte 5 dakikada %90-95 doğrulukla cerrahi kararı"],
                        ["Hücre Bloğu (Cell Block)", "Santrifüj pelletinden parafin blok", "Sitolojik sıvıda doku formatında İHK yapma", "Plevra/asit sıvısında metastatik tümörün primer odağını bulma"],
                        ["Moleküler NGS", "Parafin blok DNA/RNA'sı", "Yüzlerce kanser onkogeninin haritası", "EGFR, ALK, KRAS, BRAF mutasyonlarına akıllı ilaç seçimi"],
                        ["Likit Biyopsi", "Koldan alınan venöz kan (ctDNA)", "Kanda serbest tümör DNA'sı ve direnç mutasyonları", "Cerrahisiz, ağrısız ve sınırsız tekrarlanabilir kanser takibi"],
                        ["Dijital WSI ve Yapay Zekâ", "Taranmış gigapiksel dijital lam", "Hatasız Ki-67 indeksi ve mikrometastaz tespiti", "Telepatoloji ile global konsültasyon ve standartlaşma"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Servikal sitolojide HPV ilişkili lezyonlar Bethesda sistemiyle sınıflandırılır; HSIL kesin kolposkopi ve biyopsi endikasyonudur.",
                "📌 [SINAV SPOTU] İİAS 22G iğneyle yapılır; doğruluk %90-95'tir. Hücre bloğu sitolojik sıvıları parafin bloğa çevirerek İHK yapılmasını sağlar.",
                "📌 [SINAV SPOTU] Kanda serbest tümör DNA'sının (ctDNA) analiz edilerek cerrahisiz tümör mutasyonu takibi yapılmasına Likit Biyopsi denir."
            ],
            "medicalTerms": [
                {"term": "ctDNA (Dolaşan Tümör DNA'sı)", "explanation": "Kanser hücrelerinden kana salınan ve likit biyopside analiz edilen serbest tümör DNA'sıdır."},
                {"term": "Hücre Bloğu (Cell Block)", "explanation": "Sitolojik sıvı pelletinin parafine gömülerek doku formatında İHK yapılmasını sağlayan bloktur."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p10-1",
                    "Bethesda servikal sitoloji raporunda 'HSIL' gelen bir kadında klinikopatolojik karşılık ve hekimin yapması gereken zorunlu işlem nedir?",
                    "HSIL, histopatolojik olarak CIN 2 ve CIN 3 (karsinoma in situ) yüksek riskli kanser öncüsü tablolara karşılık gelir. Bu sonuç varlığında hekim zaman kaybetmeden kolposkopi eşliğinde servikal biyopsi yapmalıdır.",
                    "CIN 2/3 ve zorunlu kolposkopik biyopsi",
                    "Servikal Sitopatoloji"
                ),
                make_flashcard(
                    "fc-p10-2",
                    "Sitolojik sıvılarda hazırlanan 'Hücre Bloğu' (Cell Block) yönteminin standart cam yaymalara göre en büyük tanısal avantajı nedir?",
                    "Sitolojik sıvının santrifüj tortusunu pıhtılaştırarak rutin bir parafin doku bloğuna dönüştürür. Bu sayede bloktan seri kesitler alınarak cerrahi biyopsilerdeki gibi kapsamlı İHK panelleri ve moleküler testler çalışılabilir.",
                    "Sitolojiyi parafin bloğa çevirerek sınırsız İHK yapma",
                    "Modern Sitoteknoloji"
                ),
                make_flashcard(
                    "fc-p10-3",
                    "Onkolojide 'Likit Biyopsi' (Liquid Biopsy) kavramı neyi ifade eder ve klasik doku biyopsisini tekrar tekrar yapmanın zor olduğu durumlarda hastaya ne kazandırır?",
                    "Periferik kanda dolaşan serbest tümör DNA'sının (ctDNA) analiz edilmesidir. Hastaya cerrahi müdahale yapmadan basit bir kan örneğiyle tümör mutasyonlarını ve gelişen ilaç dirençlerini gerçek zamanlı takip etme imkanı sağlar.",
                    "Kanda ctDNA analizi ve cerrahisiz genetik takip",
                    "Patolojinin Geleceği"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Ders boyunca incelenen patoloji ve sitoloji ilkeleri dikkate alındığında, aşağıdaki ifadelerden hangisi BİLİMSEL OLARAK YANLIŞTIR?",
                    {
                        "A": "İnce iğne aspirasyon sitolojisi (İİAS) 22G iğneyle uygulanır ve deneyimli ellerde tanısal doğruluğu %90-95'tir.",
                        "B": "Servikal smear taramasında Bethesda sistemine göre HSIL rapor edilen hastada kolposkopik biyopsi zorunludur.",
                        "C": "Hücre bloğu (cell block) yöntemi, plevral efüzyon gibi sıvılardan parafin blok hazırlayarak İHK antikor paneli çalışılmasına imkan tanır.",
                        "D": "Periferik kanda serbest dolaşan tümör DNA'sının (ctDNA) analiz edilmesine Likit Biyopsi denir.",
                        "E": "Sitopatolojik inceleme hücre mimarisi ve bazal membranı çok net gösterdiğinden karsinoma in situ ile invaziv karsinom ayrımında histopatolojiden daha üstündür."
                    },
                    "E",
                    {
                        "A": "Doğru ifade. İİAS 22-25G iğneyle yapılır ve tanısal doğruluğu %90-95 düzeyindedir.",
                        "B": "Doğru ifade. HSIL kanser öncüsü yüksek riskli lezyon olduğundan kolposkopik biyopsi şarttır.",
                        "C": "Doğru ifade. Hücre bloğu sıvıdan parafin blok hazırlayarak zengin İHK paneline imkan tanır.",
                        "D": "Doğru ifade. Likit biyopsi kanda dolaşan serbest ctDNA üzerinden yapılan mutasyon analizidir.",
                        "E": "Yanlış ifade (aranan cevap). Sitopatolojide stroma ve bazal membran görülemediğinden invazyon histopatolojiyle kanıtlanır."
                    }
                ),
                make_interactive_table(
                    "Modern Patolojinin Tanısal Yöntemleri",
                    ["Teknoloji / Yöntem", "Kullanılan Temel Materyal", "Tanısal Çıktı"],
                    [
                        [
                            ("Likit Biyopsi", False),
                            ("Periferik kanda serbest ctDNA", True, "Plazma DNA analizi"),
                            ("Cerrahisiz tümör mutasyonu ve direnç takibi", False)
                        ],
                        [
                            ("Tüm Slayt Görüntüleme (WSI)", False),
                            ("Taranmış gigapiksel dijital lam", True, "Dijital lam formatı"),
                            ("Telepatoloji ve AI ile Ki-67/mitoz sayımı", False)
                        ],
                        [
                            ("Hücre Bloğu (Cell Block)", False),
                            ("Sıvı santrifüj pıhtı parafin bloğu", True, "Doku formatında pıhtı"),
                            ("Efüzyonda metastaz için çoklu İHK paneli", False)
                        ]
                    ]
                )
            ]
        }
    ]
