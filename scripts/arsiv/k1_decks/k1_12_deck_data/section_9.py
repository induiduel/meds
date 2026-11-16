# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-12-s81",
        "title": "Enflamasyonun Sonlanması ve Aktif Rezolüsyon Programı",
        "content": "Geleneksel görüş enflamasyonun mediyatörlerin yarı ömürlerinin tükenmesiyle kendiliğinden sönümlenen pasif bir süreç olduğunu savunmaktaydı. Güncel moleküler patoloji ise rezolüsyonun (enflamasyonun doku hasarı bırakmadan çözünmesinin) son derece koordineli, gen ekspresyonuyla yönlendirilen **aktif bir biyolojik program** olduğunu kanıtlamıştır:\n\n1. **Kısa Yarı Ömür:** Histamin, lökotrienler ve PAF gibi pro-enflamatuar mediyatörlerin yarı ömürleri dakikalarla sınırlıdır ve enzimlerce hızla yıkılırlar.\n2. **Nötrofillerin Apoptozu:** Dokudaki nötrofiller 24-48 saat içinde programlı hücre ölümüne (apoptoz) girerek toksik enzimlerini çevreye saçmadan sessizce paketlenirler.\n3. **Aktif İnhibitör Sinyaller:** Enflamasyonun doruk noktasında pro-rezolüsyon mediyatörleri üretilerek lökosit göçü aktif olarak durdurulur ve doku onarım fazı başlatılır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Enflamasyonun Sonlanma Modelleri",
                "Eski Pasif Model",
                "Mediyatörlerin tükenmesiyle enflamasyonun kendiliğinden sönümlendiği kabul edilirdi.",
                "Güncel Aktif Rezolüsyon Modeli",
                "Özel çözücü lipidler ve anti-enflamatuar sitokinlerle yönetilen aktif bir moleküler programdır."
            ),
            make_cloze(
                "Enflamasyonun dokuya zarar vermeden çözünmesi pasif bir tükeniş değil aktif gen ekspresyonuyla yönetilen aktif rezolüsyon programıdır.",
                "aktif rezolüsyon",
                "Doku iyileşmesini yöneten biyolojik çözünme mekanizması"
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-12-s82",
        "title": "Eikozanoid Sınıf Değişimi: Pro-İnflamatuardan Pro-Rezolüsyona",
        "content": "Akut enflamasyon sırasında endotel ve lökositlerin eikozanoid sentezinde dramatik bir biyokimyasal makas değişimi (lipid mediator class switching) gerçekleşir:\n\n- **Erken Faz (Pro-enflamatuar):** Enflamasyonun ilk saatlerinde araşidonik asit öncelikle PGE2 ve LTB4 sentezine yönlendirilir; böylece damar genişler, geçirgenlik artar ve nötrofiller odağa çağrılır.\n- **Sınıf Değişimi:** Dokuda biriken PGE2 belirli bir eşik konsantrasyonu aştığında lökositlerdeki 15-lipoksijenaz (15-LOX) gen ekspresyonunu uyarır.\n- **Geç Faz (Pro-rezolüsyon):** 15-LOX aktivasyonuyla birlikte araşidonik asit artık LTB4 yerine **lipoksinlere (LXA4 ve LXB4)** dönüştürülür. Lipoksinler nötrofil kemotaksisini anında frenler, monositleri temizlik amacıyla dokuya çağırır ve rezolüsyonu başlatır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Eikozanoid Sınıf Değişimi Kaskadı",
                [
                    "1. Pro-enflamatuar Sentez: Erken fazda araşidonik asitten yoğun PGE2 ve LTB4 üretimi gerçekleşir.",
                    "2. Eşik Konsantrasyon: Dokuda biriken PGE2 lökositlerdeki 15-lipoksijenaz enzimini genetik olarak uyarır.",
                    "3. Sentez Dönüşümü: Araşidonik asit akışı LTB4 sentezinden lipoksin (LXA4) üretimine yönlendirilir.",
                    "4. Frenleme ve Rezolüsyon: Lipoksinler nötrofil alımını durdurup monosit temizliğini başlatır."
                ]
            ),
            make_quiz(
                "Enflamasyonun ilerleyen saatlerinde lökositlerde 15-lipoksijenaz enzimini indükleyerek pro-enflamatuar lökotrien sentezinden anti-enflamatuar lipoksin sentezine geçişi (lipid sınıf değişimi) tetikleyen lipid mediyatör hangisidir?",
                [
                    {"key": "A", "text": "Prostaglandin E2 (PGE2)", "explanation": "A seçeneği DOĞRUDUR: PGE2 birikimi 15-LOX'u indükleyerek lipoksin sentezine sınıf değişimini tetikler."},
                    {"key": "B", "text": "Tromboksan A2", "explanation": "B seçeneği yanlıştır: Agregasyon ve vazokonstriksiyon yapar."},
                    {"key": "C", "text": "Lökotrien C4", "explanation": "C seçeneği yanlıştır: Bronkokonstriktördür."},
                    {"key": "D", "text": "Histamin", "explanation": "D seçeneği yanlıştır: Vazoaktif amindir, enzim indüklemez."},
                    {"key": "E", "text": "Serotonin", "explanation": "E seçeneği yanlıştır: Trombosit kaynaklı vazoaktif amindir."}
                ],
                "A"
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-12-s83",
        "title": "Özel Pro-Rezolüsyon Mediyatörleri (SPM): Rezolvin, Protektin ve Maresin",
        "content": "Rezolüsyon sürecini yöneten en güçlü moleküller, esansiyel **omega-3 çoklu doymamış yağ asitlerinden (PUFA)** sentezlenen Özel Pro-Rezolüsyon Mediyatörleridir (Specialized Pro-resolving Mediators - SPM):\n\n1. **Rezolvinler (E ve D Serisi):** E serisi EPA'dan (eikosapentaenoik asit), D serisi DHA'dan (dokosaheksaenoik asit) sentezlenir. Nötrofillerin transendotelyal göçünü bloke eder, sitokin fırtınasını dindirirler.\n2. **Protektinler (PD1 / Nöroprotektin D1):** DHA kökenlidir; T-hücre apoptozunu uyarır ve sinir dokusunda sitotoksik hasarı engeller.\n3. **Maresinler (MaR1):** Makrofajlar tarafından DHA'dan sentezlenir; ölü hücrelerin fagositozunu uyarır ve doku rejenerasyonunu hızlandırır.\n\nSPM'ler immün sistemi baskılamadan (immün yetmezlik yaratmadan) enflamasyonu fizyolojik olarak sonlandıran süper-çözücülerdir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özel Çözücü Mediyatör (SPM)", "Öncül Omega-3 Yağ Asidi", "Temel Biyolojik Görevi"],
                [
                    [
                        {"text": "Rezolvin E Serisi (RvE)", "isMasked": False, "hint": ""},
                        {"text": "Eikosapentaenoik Asit (EPA)", "isMasked": True, "hint": "Balık yağındaki 20 karbonlu omega-3"},
                        {"text": "Nötrofil adezyonunu ve göçünü engelleme", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Rezolvin D Serisi (RvD)", "isMasked": False, "hint": ""},
                        {"text": "Dokosaheksaenoik Asit (DHA)", "isMasked": False, "hint": ""},
                        {"text": "İnflamazom inhibisyonu ve lökosit durdurma", "isMasked": True, "hint": "Sitokin üretimini durduran hücresel etki"}
                    ],
                    [
                        {"text": "Maresinler (MaR1)", "isMasked": True, "hint": "Makrofaj kökenli çözücü lipid adı"},
                        {"text": "Dokosaheksaenoik Asit (DHA)", "isMasked": False, "hint": ""},
                        {"text": "Makrofaj eferositozu ve doku rejenerasyonu", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "DHA'dan sentezlenen ve özellikle sinir sisteminde doku hasarını engelleyip T-hücre apoptozunu teşvik eden pro-rezolüsyon mediyatörü hangisidir?",
                "Protektin D1'dir (PD1 / Nöroprotektin D1).",
                "Koruyucu kökenli DHA türevi mediyatör"
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-12-s84",
        "title": "Nötrofillerin Apoptozu ve Makrofaj Eferositozu",
        "content": "Akut enflamasyonun çözülmesinde en kritik basamak dokuyu istila etmiş milyonlarca nötrofilin ortadan kaldırılmasıdır:\n\n- **Apoptoz:** Ömrünü tamamlayan nötrofiller yüzeylerinde fosfatidilserin (PS) molekülünü dış yaprağa çevirerek 'beni ye' (eat-me) sinyali sergiler.\n- **Eferositoz (Efferocytosis):** Doku makrofajları, apoptoza uğramış bu nötrofilleri hücre zarları patlamadan yutarak fagositozla temizlerler.\n- **Anti-enflamatuar Anahtarın Çevrilmesi:** Makrofajın apoptotik nötrofili yutması, makrofaj içi sinyalleri dramatik şekilde değiştirir: Pro-enflamatuar TNF-α ve IL-1 üretimi tamamen kapatılır; yerine güçlü anti-enflamatuar ve doku onarıcı sitokinler olan **TGF-β** ve **IL-10** salgılanmaya başlar. Böylece doku harabiyeti son bulur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Doku makrofajlarının apoptoza giden nötrofilleri temizlediği (eferositoz) bir odakta sitokin profili inceleniyor.",
                "Makrofajların apoptotik hücreleri fagositozu sonrasında dokuya salgılanan ve enflamasyonu aktif olarak baskılayan temel sitokin çifti hangisidir?",
                [
                    {
                        "text": "TGF-β ve IL-10 salgılanarak doku onarımı ve immünsüpresyon başlatılır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Eferositoz makrofajın fenotipini anti-enflamatuar M2 yönüne çevirerek TGF-β ve IL-10 salgısını uyarır."
                    },
                    {
                        "text": "TNF-alfa ve IL-1 salgılanarak yeni nötrofiller çağrılır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Bu pro-enflamatuar yanıttır; eferositoz bu sitokinleri aktif olarak baskılar."
                    },
                    {
                        "text": "IL-12 ve IFN-gama salgılanarak granülom oluşumu tetiklenir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Bu kronik Th1 yanıtıdır, rezolüsyon fazında görülmez."
                    }
                ]
            ),
            make_cloze(
                "Apoptoza uğrayan nötrofillerin makrofajlarca sessizce fagositozla yutulup temizlenmesi sürecine eferositoz adı verilir.",
                "eferositoz",
                "Ölü hücrelerin çevreye zarar vermeden temizlenmesi terimi"
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-12-s85",
        "title": "İmmünosupresif Sitokinler ve Doku Onarım Faktörleri",
        "content": "Rezolüsyon fazının oturmasıyla birlikte doku tamiri ve skar oluşumu için büyüme faktörleri devreye girer:\n\n- **İnterlökin-10 (IL-10):** En güçlü anti-enflamatuar sitokindir. Makrofaj ve dendritik hücrelerin MHC sınıf II ve ko-stimülatör molekül ekspresyonunu baskılar; IL-1, TNF ve IL-12 üretimini engeller.\n- **Dönüştürücü Büyüme Faktörü-Beta (TGF-β):** Güçlü bir immünosupresandır; lökosit proliferasyonunu durdurur. Aynı zamanda fibroblast kemotaksisini uyarır, kollajen sentezini artırır ve doku matriksinin yeniden inşasını sağlar.\n- **VEGF ve FGF:** Hasarlı vasküler yatağın yeniden canlanması için anjiyogenezi (yeni damar oluşumunu) tetiklerler. Bu dengeli geçiş bozulursa ya kronik granülomatöz enflamasyon ya da kontrolsüz fibrozis gelişir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Pro-Enflamatuar vs Anti-Enflamatuar / Onarıcı Sitokin Profili",
                "Enflamasyonun Yıkım Fazı",
                "TNF, IL-1, IL-6 ve kemokinler hakimdir; nötrofil infiltrasyonu ve doku nekrozu görülür.",
                "Rezolüsyon ve Onarım Fazı",
                "IL-10 ve TGF-beta hakimdir; fibroblast proliferasyonu, anjiyogenez ve kollajen sentezi uyarılır."
            ),
            make_quiz(
                "Makrofajların pro-enflamatuar sitokin üretimini en güçlü şekilde inhibe eden, antijen sunumunu baskılayan temel anti-enflamatuar sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterlökin-10 (IL-10)", "explanation": "A seçeneği DOĞRUDUR: IL-10 makrofaj aktivasyonunu ve pro-enflamatuar sitokinleri durduran baş regülatördür."},
                    {"key": "B", "text": "İnterlökin-8", "explanation": "B seçeneği yanlıştır: Nötrofil kemotaktik kemokinidir."},
                    {"key": "C", "text": "İnterlökin-1", "explanation": "C seçeneği yanlıştır: Pirojenik pro-enflamatuar sitokindir."},
                    {"key": "D", "text": "TNF-alfa", "explanation": "D seçeneği yanlıştır: Majör pro-enflamatuar sitokindir."},
                    {"key": "E", "text": "İnterferon-gama", "explanation": "E seçeneği yanlıştır: Klasik makrofaj aktivatörüdür."}
                ],
                "A"
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-12-s86",
        "title": "Sistemik İnflamatuar Yanıt Sendromu (SIRS) ve Sepsis Kliniği",
        "content": "Lokal dokuda yararlı olan kimyasal mediyatörlerin sistemik dolaşıma kontrolsüz ve yüksek miktarlarda taşması felaketle sonuçlanan bir klinik tablo yaratır:\n\n- **SIRS Kriterleri:** Ateş (>38°C) veya hipotermi (<36°C), taşikardi (>90/dk), taşipne (>20/dk veya PaCO2 <32 mmHg) ve lökositoz (>12.000/µL) veya lökopeni (<4.000/µL).\n- **Sepsis Tanımı:** Kanıtlanmış veya şüphelenilen bir enfeksiyona karşı konağın düzensiz (disregüle) bağışıklık yanıtı sonucu gelişen, hayatı tehdit edici organ fonksiyon bozukluğudur (SOFA skoru artışı).\n- **Mediyatör Kaynaklı Patoloji:** TNF, IL-1 ve endotel kaynaklı aşırı NO salınımı sistemik arterioler dilatasyona ve yaygın venüler sızıntıya yol açar. Sonuç: Ağır refrakter hipotansiyon ve doku hipoksisidir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Klinik Durum", "Tetikleyici Mekanizma", "Mediyatör Profili"],
                [
                    [
                        {"text": "Lokal Enflamasyon", "isMasked": False, "hint": ""},
                        {"text": "Lokal doku hasarı veya sınırlı mikrobiyal invazyon", "isMasked": False, "hint": ""},
                        {"text": "Lokal histamin, LTB4 ve parakrin sitokinler", "isMasked": True, "hint": "Yalnızca hasarlı bölgede etkili moleküller"}
                    ],
                    [
                        {"text": "SIRS / Sepsis", "isMasked": True, "hint": "Sistemik yangısal yanıt kısaltması"},
                        {"text": "Mediyatörlerin sistemik dolaşıma taşması ve yaygın endotel hasarı", "isMasked": False, "hint": ""},
                        {"text": "Sistemik TNF, IL-1, IL-6 ve aşırı iNOS üretimi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Septik Şok", "isMasked": False, "hint": ""},
                        {"text": "Yaygın vazodilatasyon, kapiller kaçış ve kardiyak depresyon", "isMasked": False, "hint": ""},
                        {"text": "Sıvı resüsitasyonuna yanıtsız ağır hipotansiyon", "isMasked": True, "hint": "Vazopressör gerektiren klinik durum"}
                    ]
                ]
            ),
            make_recall(
                "Konağın enfeksiyona karşı verdiği düzensiz sistemik enflamatuar yanıtın yol açtığı yaşamı tehdit eden organ yetmezliği tablosuna ne ad verilir?",
                "Sepsistir.",
                "Enfeksiyöz kaynaklı sistemik yanıt tablosu"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-12-s87",
        "title": "Sitokin Salınım Sendromu ve Sitokin Fırtınası",
        "content": "Sitokin Salınım Sendromu (CRS - Cytokine Release Syndrome) ya da halk arasında bilinen adıyla **Sitokin Fırtınası**, T-hücreleri, makrofajlar ve endotelin birbirini pozitif geri bildirimle aşırı kamçılaması sonucu ortaya çıkar:\n\n- **Etiyoloji:** Şiddetli viral enfeksiyonlar (COVID-19, SARS, influenza), CAR-T hücre immünoterapileri veya bispesifik antikor infüzyonları.\n- **Kilit Mediyatör İnterlökin-6 (IL-6):** T-hücreleri ve monositlerden salınan aşırı IL-6 endotel geçirgenliğini bozar, kompleman ve koagülasyon kaskadını patlatır.\n- **Yaygın Damar İçi Pıhtılaşma (DIC):** Mediyatörlerin endoteldeki doku faktörünü (faktör III) açığa çıkarması ve trombomodulini baskılaması mikrovasküler trombozlara yol açar; tüketim koagülopatisi gelişir.\n- **ARDS ve MODS:** Akciğer alveollerinde hiyalen membranlar ve çoklu organ yetmezliği gelişir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Sitokin Fırtınası ve Çoklu Organ Hasarı Gelişim Basamakları",
                [
                    "1. Hücresel Aşırı Aktivasyon: T-hücreleri ve monositlerden masif TNF, IL-1 ve özellikle IL-6 deşarjı olur.",
                    "2. Sistemik Endotel Hasarı: Aşırı sitokinler yaygın endotel bariyerini yıkar ve aşırı geçirgenlik yaratır.",
                    "3. Koagülasyon Patlaması: Trombomodulin azalır, doku faktörü açığa çıkarak mikrovasküler DIC gelişir.",
                    "4. Uç Organ İskemisi ve ARDS: Alveolo-kapiller membran yıkılır, dokular oksijensiz kalarak iflas eder."
                ]
            ),
            make_quiz(
                "CAR-T hücre tedavileri ve ağır viral pnömoniler sırasında gelişen Sitokin Salınım Sendromunda (CRS) patogenezin merkezinde yer alan ve reseptör blokajı (tosilizumab) ile hedeflenen majör sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterlökin-6 (IL-6)", "explanation": "A seçeneği DOĞRUDUR: Sitokin fırtınasının merkezindeki sitokindir ve tosilizumab ile bloke edilir."},
                    {"key": "B", "text": "İnterlökin-4", "explanation": "B seçeneği yanlıştır: Th2 ve IgE sitokinidir."},
                    {"key": "C", "text": "İnterlökin-10", "explanation": "C seçeneği yanlıştır: Anti-enflamatuar sitokindir."},
                    {"key": "D", "text": "TGF-beta", "explanation": "D seçeneği yanlıştır: Fibrozis ve baskılama sitokinidir."},
                    {"key": "E", "text": "Bradikinin", "explanation": "E seçeneği yanlıştır: Kinin sistemi peptididir."}
                ],
                "A"
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-12-s88",
        "title": "Akut Faz Reaktanları: Sedimentasyon (ESR) ve C-Reaktif Protein (CRP)",
        "content": "Klinik pratikte vücuttaki enflamasyonun varlığı, şiddeti ve tedaviye yanıtı karaciğer kökenli Akut Faz Proteinleri ile izlenir:\n\n1. **C-Reaktif Protein (CRP):** İnterlökin-6 uyarısıyla hepatositlerce üretilir. Bakteriyel fosfokoline bağlanarak kompleman aktivasyonu ve opsonizasyon yapar. Yarı ömrü çok kısadır (yaklaşık 19 saat); enflamasyon başladığında 6 saatte hızla yükselir, tedaviyle hızla düşer. Bu nedenle **akut olayların en duyarlı göstergesidir**.\n2. **Eritrosit Sedimentasyon Hızı (ESR):** IL-6 etkisiyle karaciğerde sentezlenen **fibrinojen**, eritrositlerin negatif yüzey yükünü (zeta potansiyeli) nötralize eder. Eritrositler madeni para gibi üst üste dizilir (**Rouleaux formasyonu**) ve tüpte hızla dibe çöker. Fibrinojenin yarı ömrü uzun olduğundan ESR geç yükselir ve haftalarca yüksek kalır; kronik enflamasyon takibinde değerlidir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "CRP ve Sedimentasyon (ESR) Dinamikleri",
                "C-Reaktif Protein (CRP)",
                "Saatler içinde hızla fırlar, yarı ömrü kısadır; akut alevlenme ve erken tedavi takibinde idealdir.",
                "Eritrosit Sedimentasyon Hızı (ESR)",
                "Fibrinojenin yavaş kinetiği nedeniyle geç yükselir ve geç düşer; kronik süreç takibinde kullanılır."
            ),
            make_cloze(
                "Eritrosit sedimentasyon hızının artışındaki temel biyokimyasal mekanizma fibrinojenin eritrositlerin yüzeyindeki negatif zeta potansiyelini nötralize etmesidir.",
                "zeta potansiyelini",
                "Eritrositlerin birbirini itmesini sağlayan elektriksel yük"
            )
        ]
    })

    # Slide 89
    slides.append({
        "id": "k1-12-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Enflamasyonun Rezolüsyonu, Sepsis ve Laboratuvar İzlemi",
        "content": "Bu kontrol noktasında enflamasyonun aktif çözünme mekanizmalarını, pro-rezolüsyon lipidlerini, kontrolsüz sistemik yanıtları ve klinik izlem parametrelerini pekiştiriyoruz:\n\n- **Aktif Rezolüsyon:** Enflamasyonun bitişi pasif değildir; PGE2'nin 15-LOX'u uyarmasıyla lipoksinlere geçilir (sınıf değişimi).\n- **Omega-3 Kökenli SPM'ler:** EPA'dan rezolvin E, DHA'dan rezolvin D, protektin ve maresinler sentezlenerek enflamasyon doku hasarı bırakmadan söndürülür.\n- **Eferositoz ve Sitokinler:** Makrofajlar apoptotik nötrofilleri yutarak IL-10 ve TGF-β salgılar; doku tamir ve anjiyogenez fazına geçilir.\n- **Sepsis ve Sitokin Fırtınası:** Mediyatörlerin sistemik dolaşıma taşması, IL-6 patlaması, aşırı NO salınımı ve DIC tablosuyla hayatı tehdit eder.\n- **Laboratuvar:** Akut fazda IL-6 karaciğerden CRP ve fibrinojen sentezletir; CRP erken ve dinamik, ESR ise geç ve kalıcı kinetik gösterir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Enflamasyonun çözülme fazında apoptotik nötrofilleri yutan makrofajların dokuya salgıladığı, fibroblast kemotaksisi ve kollajen sentezini uyararak doku onarımını başlatan temel sitokin hangisidir?",
                [
                    {"key": "A", "text": "Dönüştürücü Büyüme Faktörü-Beta (TGF-β)", "explanation": "A seçeneği DOĞRUDUR: TGF-beta doku onarımı, fibroblast göçü ve matriks sentezinin baş mimarıdır."},
                    {"key": "B", "text": "Tümör Nekroz Faktörü-alfa", "explanation": "B seçeneği yanlıştır: Güçlü doku hasarı ve nekroz sitokinidir."},
                    {"key": "C", "text": "İnterlökin-8", "explanation": "C seçeneği yanlıştır: Nötrofil çağıran kemokindir."},
                    {"key": "D", "text": "Bradikinin", "explanation": "D seçeneği yanlıştır: Ağrı ve permeabilite mediyatörüdür."},
                    {"key": "E", "text": "Histamin", "explanation": "E seçeneği yanlıştır: Erken faz vazoaktif aminidir."}
                ],
                "A"
            ),
            make_cloze(
                "Omega-3 yağ asitlerinden sentezlenen ve doku onarımını başlatan özel pro-rezolüsyon mediyatörleri arasında rezolvinler, protektinler ve maresinler yer alır.",
                "maresinler",
                "Makrofaj kökenli özel çözücü lipid molekül grubu"
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-12-s90",
        "title": "Kronik Enflamasyonda Hedefe Yönelik Biyolojik Tedaviler",
        "content": "Kimyasal mediyatörlerin hücresel ve moleküler mekanizmalarının aydınlatılması, modern tıpta kronik enflamatuar ve otoimmün hastalıkların tedavisinde bir devrim yaratmıştır:\n\n- **Biyolojik Ajan Mantığı:** Eskiden kullanılan genel immünsüpresiflerin (steroidler, metotreksat) aksine, yalnızca kilit sitokinleri veya reseptörlerini nötralize eden monoklonal antikorlar ya da füzyon proteinleridir.\n- **Hedeflenen Majör Mediyatörler:**\n  1. **TNF-α:** Romatoid artrit, inflamatuar bağırsak hastalıkları, psöriyazis tedavisinde.\n  2. **IL-1:** Ailesel Akdeniz Ateşi (FMF), CAPS ve Still hastalığında.\n  3. **IL-6 Reseptörü:** Dev hücreli arterit ve sitokin fırtınasında.\n  4. **IL-17 ve IL-23:** Ankilozan spondilit ve psöriyaziste.\n  5. **Kompleman C5:** Paroksismal Noktürnal Hemoglobinüri (PNH) ve aHUS'ta.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hedef Mediyatör", "Örnek Biyolojik İlaç", "Temel Endikasyon Alanı"],
                [
                    [
                        {"text": "Tümör Nekroz Faktörü-alfa (TNF-α)", "isMasked": False, "hint": ""},
                        {"text": "İnfliksimab, Adalimumab, Etanersept", "isMasked": True, "hint": "En yaygın anti-TNF monoklonal antikorlar"},
                        {"text": "Romatoid Artrit, Crohn Hastalığı, Psöriyazis", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "İnterlökin-1 Reseptörü (IL-1R)", "isMasked": True, "hint": "Ateş ve inflamazom sitokin reseptörü"},
                        {"text": "Anakinra", "isMasked": False, "hint": ""},
                        {"text": "Ailesel Akdeniz Ateşi, CAPS, Gut", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "İnterlökin-6 Reseptörü (IL-6R)", "isMasked": False, "hint": ""},
                        {"text": "Tosilizumab", "isMasked": True, "hint": "Sitokin fırtınasında kullanılan monoklonal antikor"},
                        {"text": "Dev Hücreli Arterit, CRS, Romatoid Artrit", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Kimyasal mediyatörlerin tek tek biyolojik ajanlarla hedeflenmesinin genel immünosupresiflere göre en temel farmakolojik avantajı nedir?",
                "Hedefe yönelik seçici blokaj yaparak tüm immün sistemi baskılamadan lokal enflamasyonu durdurmasıdır.",
                "Hedefe özgüllük ve seçici etki"
            )
        ]
    })

    return slides
