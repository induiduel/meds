#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 3: Patolojinin Klinik Önemi, Patoloğun Konsültan Rolü ve Raporlama (Adımlar 20 - 29)
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
        # Adım 20
        {
            "slideNumber": 20,
            "title": "Neoplazilerde Altın Standart: Neden Patolojik Tanı Şarttır?",
            "subtitle": "Klinik muayene ve radyoloji şüphe uyandırır; ancak kanser tanısını ve tedavi yetkisini kesinleştiren tek otorite patolojidir.",
            "badge": "Altın Standart",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Klinik muayene ve radyolojik görüntüleme şüphe uyandırsa da, ==özellikle neoplazilerde patoloji tartışmasız altın standart tanı yöntemidir==.

Gelişmiş görüntüleme yöntemleri lezyonun yerini ve metabolizmasını gösterir; ancak lezyonun benign, in situ ya da invaziv olduğunu kanıtlayamaz. Kesin kanser teşhisi koymak, radikal cerrahi planlamak ve kemoterapi başlamak, ancak doku biyopsisinde ==karsinomatöz hücrelerin bazal membranı aştığının histopatolojik olarak kanıtlanmasıyla== mümkündür. Mikroskobik inceleme; tümörün histolojik alt tipini, diferansiyasyon derecesini ve çevre doku invazyonunu netleştirerek onkolojik tedaviyi doğrudan yönlendirir.

> [TEMEL İLKE] Patolojik doku kanıtı olmadan hiçbir hastaya radikal onkolojik tedavi veya organ rezeksiyonu uygulanamaz.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Altın Standart", "desc": "Kanser tanısında patoloji nihai tanısal karar vericidir.", "isKey": True},
                    {"title": "Radyolojinin Sınırı", "desc": "Radyoloji kitlenin yerini ve metabolizmasını gösterir; mikroskobik invazyonu kanıtlayamaz.", "isKey": True},
                    {"title": "Tedavi Yetkisi", "desc": "Kemoterapi, immünoterapi ve radikal cerrahi patoloji raporuna göre planlanır.", "isKey": False}
                ],
                "table": {
                    "title": "Tanısal Modalitelerin Onkolojideki Rol ve Sınırları",
                    "headers": ["Yöntem", "Klinik Katkısı", "Temel Kısıtlılığı ve Sınırı"],
                    "rows": [
                        ["Fizik Muayene", "Ele gelen kitleyi, lenfadenopatiyi ve organomegaliyi saptar", "Benign-malign ayrımı yapamaz, doku tipi veremez"],
                        ["Görüntüleme (BT/MR/PET)", "Tümörün anatomik sınırlarını, vasküler komşuluğunu ve metastazını gösterir", "Hücresel düzeyde mikroskobik invazyonu ve reseptör profilini gösteremez"],
                        ["Tümör Belirteçleri (CEA, CA-125)", "Tedavi yanıtını ve nüksleri izlemede faydalıdır", "Spesifitesi düşüktür, tek başına kanser tanısı koyduramaz"],
                        ["Patolojik İnceleme (Altın Standart)", "Tümör tipi, derecesi, cerrahi sınır, İHK ve mutasyon profilini netleştirir", "Yeterli ve doğru doku örneklemesi gerektirir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Neoplazilerde ve inflamatuvar doku hastalıklarında kesin tanı için altın standart yöntem patolojik incelemedir.",
                "📌 [SINAV SPOTU] PET-BT'de tutulum gösteren her lezyon kanser değildir; granülomatöz inflamasyonlar (tüberküloz) da yüksek SUV tutulumu yapar.",
                "🚨 [KRİTİK UYARI] Patoloji raporu olmadan kemoterapi başlanması ağır bir tıbbi malpraktistir."
            ],
            "medicalTerms": [
                {"term": "Altın Standart (Gold Standard)", "explanation": "Bir hastalığın varlığını en yüksek doğrulukla kanıtlayan referans tanı yöntemidir."},
                {"term": "İn Situ Karsinom", "explanation": "Bazal membranı henüz aşmamış ve metastaz yeteneği kazanmamış erken evre kanserdir."},
                {"term": "İnvaziv Karsinom", "explanation": "Bazal membranı aşarak stromaya ve damarlara yayılan metastaz potansiyelli kanserdir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Akciğerinde 3 cm'lik spiküle kitle ve PET-BT'de yüksek metabolik aktivite saptanan bir hastada, kesin kanser tanısı koyup cerrahi veya kemoterapi planlamak için hangisi zorunludur?",
                    {
                        "A": "Sadece serum CEA ve karsinoembriyonik antijen düzeyini ölçmek",
                        "B": "Hastaya hemen 3 kür ampirik kemoterapi başlayıp kitle küçülmesini izlemek",
                        "C": "Kitleden biyopsi alarak histopatolojik inceleme ile maligniteyi kanıtlamak",
                        "D": "Üç ay sonra tekrar kontrol akciğer tomografisi çekmek",
                        "E": "Hastaya hemen solunum egzersizleri başlayıp taburcu etmek"
                    },
                    "C",
                    {
                        "A": "Serum tümör belirteçleri düşük özgüllükleri nedeniyle tek başına kanser tanısı koyduramaz.",
                        "B": "Doku tanısı olmadan ampirik kemoterapi başlanması ağır bir tıbbi hatadır.",
                        "C": "Neoplastik süreçlerde kesin tanı ve tedavi yetkisi biyopsinin histopatolojik doğrulamasına dayanır.",
                        "D": "Malignite şüphesinde biyopsisiz beklemek tümörün ilerlemesine ve metastaza yol açar.",
                        "E": "Malignite şüphesi taşıyan spiküle bir kitlede ileri tetkik yapılmadan hasta taburcu edilemez."
                    }
                ),
                make_cloze(
                    "Neoplastik hastalıklarda tanı, evreleme, cerrahi sınır değerlendirmesi ve hedefe yönelik tedavi planlamasında [altın standart] kabul edilen disiplin patolojidir.",
                    "altın standart",
                    "Tıpta en güvenilir referans tanı yöntemi terimi"
                )
            ]
        },

        # Adım 21
        {
            "slideNumber": 21,
            "title": "Cerrahi Patoloji Raporunun Mimarisi: Tanı, Evre, Derece ve Sınırlar",
            "subtitle": "Patoloji raporu rastgele bir metin değildir; onkoloğun ve cerrahın yol haritası olan standardize bir belgedir.",
            "badge": "Rapor Standartları",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Cerrahi patoloji raporu, tümörün biyolojik davranışını ve yayılımını standardize formatta aktaran yasal ve tıbbi bir belgedir.

Standart bir onkolojik raporda ==dört temel parametre== yer alır: Tümörün hücresel kökenini belirten **histolojik tanı**, diferansiyasyon ve çoğalma hızını yansıtan **histolojik derece (grade)**, anatomik yayılımı ölçen **patolojik evreleme (pTNM)** ve geride rezidüel doku kalıp kalmadığını gösteren **cerrahi sınırlar**. Ayrıca lenfovasküler invazyon, perinöral yayılım ve immünohistokimyasal belirteçler tedavi yanıtını ve prognozu belirlemede klinisyene rehberlik eder.

> [YÜKSEK VERİM] Cerrahi sınır pozitifliği geride tümör kaldığını gösterir; grade hücresel agresifliği, evre ise anatomik yayılımı ifade eder.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Histolojik Tip ve Derece", "desc": "Tümörün kökeni ve hücresel agresifliği (Grade 1-3) belirlenir.", "isKey": True},
                    {"title": "pTNM Evrelemesi", "desc": "Tümör boyutu (pT) ve lenf nodu tutulum sayısı (pN) eksiksiz yazılır.", "isKey": True},
                    {"title": "Cerrahi Sınırlar", "desc": "Tümörün boyanmış cerrahi kenara olan uzaklığı mm cinsinden verilir.", "isKey": True}
                ],
                "table": {
                    "title": "Onkolojik Cerrahi Patoloji Raporunun Temel Bileşenleri",
                    "headers": ["Rapor Bileşeni", "Patolojik İnceleme", "Klinisyene Verdiği Mesaj"],
                    "rows": [
                        ["Histolojik Tanı", "Doku tipi ve hücre diferansiyasyonu", "Hastalığın kesin adı ve hücresel kökeni"],
                        ["Histolojik Grade", "Tubul formasyonu, nükleer atipi, mitoz sayısı", "Tümörün biyolojik çoğalma hızı ve agresifliği"],
                        ["pTNM Evresi", "Tümör çapı, derinliği ve lenf nodu metastazı", "Hastalığın anatomik yayılımı ve adjuvan tedavi endikasyonu"],
                        ["Cerrahi Sınır", "Mürekkep ile boyanmış cerrahi hatta tümör varlığı", "Ameliyatın küratif olup olmadığı ve tekrar cerrahi gereksinimi"],
                        ["LVI ve PNI", "Damar, lenfatik ve sinir kılıfı invazyonu", "Uzak metastaz ve lokal nüks riskinin yüksekliği"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Grade hücresel diferansiyasyonu (mikroskobik agresifliği), Evre (Stage) ise tümörün anatomik yayılım genişliğini (pTNM) ifade eder.",
                "📌 [SINAV SPOTU] Cerrahi sınır pozitifliği, tümörün cerrah tarafından geride bırakıldığı anlamına gelir ve lokal nüks riskini katlar.",
                "🚨 [KRİTİK UYARI] Lenfovasküler invazyon (LVI), tümör hücrelerinin lenf nodlarına ve uzak organlara göç yoluna girdiğini gösteren bağımsız bir kötü prognostik faktördür."
            ],
            "medicalTerms": [
                {"term": "Histolojik Derece (Grade)", "explanation": "Tümör hücrelerinin diferansiyasyon ve mitotik agresifliğini yansıtan mikroskobik derecedir."},
                {"term": "pTNM Evrelemesi", "explanation": "Rezeksiyon materyalinde tümör boyutu, lenf nodu ve metastazı belirten evreleme sistemidir."},
                {"term": "Perinöral İnvazyon (PNI)", "explanation": "Tümör hücrelerinin sinir kılıfı boyunca ilerleyerek lokal nükse yol açan yayılımıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Tümörde Derece (Grade) ile Evre (Stage) Arasındaki Ayrım",
                    "Histolojik Derece (Grade)",
                    "Patolojik Evre (pTNM Stage)",
                    [
                        "Tümörün mikroskobik hücresel farklılaşmasını gösterir",
                        "Nükleer atipi, mitoz sayısı ve mimari tübül formasyonuna dayanır",
                        "Grade 1 (İyi), Grade 2 (Orta), Grade 3 (Kötü diferansiye)"
                    ],
                    [
                        "Tümörün vücuttaki anatomik yayılım genişliğini gösterir",
                        "Tümör boyutu (T), lenf nodu sayısı (N) ve metastaza (M) dayanır",
                        "Evre I (Lokal erken), Evre IV (Uzak metastaz yapmış ileri evre)"
                    ]
                ),
                make_cloze(
                    "Tümörün mikroskobik hücresel diferansiyasyon ve agresifliğine derece (grade) denirken, vücuttaki anatomik yayılım ve lenf nodu tutulum genişliğine [evre] adı verilir.",
                    "evre",
                    "Hastalığın anatomik yayılımını (TNM) belirten basamak"
                )
            ]
        },

        # Adım 22
        {
            "slideNumber": 22,
            "title": "Patoloğun Konsültan Hekim Kimliği: Klinisyenin Teşhis ve Tedavi Ortağı",
            "subtitle": "Patolog numuneyi işleyen bir laborant değildir; klinisyene ayırıcı tanı ve tedavi stratejisi sunan konsültandır.",
            "badge": "Konsültan Hekim",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patoloji uzmanı; yalnızca numune işleyen bir görevli değil, klinik tanı ve tedavi stratejisini belirleyen ==konsültan bir tıp doktorudur==.

Patolog dokuyu incelerken etiyolojik ve ayırıcı tanıları değerlendirir, inflamatuvar veya neoplastik süreçleri ayırt eder ve klinisyene rehberlik eder. Ameliyat esnasında uygulanan **frozen kesit** ile cerrahi sınırın temizliğini dakikalar içinde bildirerek rezeksiyon genişliğini tayin eder. Onkolojiye hormon reseptörleri ve genetik belirteçlerle tedavi haritası sunarken, benign lezyonları saptayarak hastayı gereksiz radikal cerrahilerden korur.

> [TEMEL İLKE] Patolog, klinikopatolojik korelasyon kurarak hastanın tanı, ameliyat ve ilaç tedavi sürecini yönlendiren konsültandır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Konsültan Hekimlik", "desc": "Klinisyen hekime diferansiyel tanı ve tedavi kılavuzluğu sağlar.", "isKey": True},
                    {"title": "İntraoperatif Karar", "desc": "Ameliyat esnasında dakikalar içinde cerrahi yönü belirler (Frozen).", "isKey": True},
                    {"title": "Hasta Odaklılık", "desc": "Rapor klinisyenin tedavi stratejisini netleştirecek pratik soruları yanıtlar.", "isKey": False}
                ],
                "table": {
                    "title": "Patoloğun Klinik Branşlarla Konsültasyon Alanları",
                    "headers": ["Klinik Branş", "Klinisyenin Sorusu", "Patoloğun Konsültan Yanıtı"],
                    "rows": [
                        ["Genel Cerrahi", "Meme kitlesinin cerrahi sınırları temiz mi?", "İntraoperatif frozen ile cerrahi sınır negatif, rezeksiyon yeterli"],
                        ["Medikal Onkoloji", "Bu kolon kanserine anti-EGFR ilaç verebilir miyim?", "KRAS ve NRAS genleri wild-type (mutasyonsuz), hasta anti-EGFR tedaviden fayda görür"],
                        ["Gastroenteroloji", "Ülseratif kolitli bu hastada displazi başladı mı?", "Düşük dereceli epitelyal displazi mevcut, kolektomi endikasyonu tartışılmalı"],
                        ["Romatoloji", "Böbrek tutulumlu lupus hastasında glomerül hasarı ne evrede?", "Lupus Nefriti Sınıf IV (Diffüz proliferatif), agresif immünosüpresyon şart"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patoloji uzmanı, klinikopatolojik korelasyon kurarak klinisyene rehberlik eden konsültan hekimdir.",
                "📌 [SINAV SPOTU] Frozen kesit (intraoperatif konsültasyon) ameliyat esnasında yaklaşık 5-10 dakikada sonuç veren hayati bir konsültasyon aracıdır.",
                "🚨 [KRİTİK UYARI] Patoloji raporu pasif bir teşhis metni değil; hastanın sonraki tüm tedavisini belirleyen aktif bir klinik karardır."
            ],
            "medicalTerms": [
                {"term": "Konsültasyon", "explanation": "Hekimin tanı veya tedavi sürecinde başka bir uzmanın resmi tıbbi görüşüne başvurmasıdır."},
                {"term": "Frozen Kesit (İntraoperatif İnceleme)", "explanation": "Ameliyat sırasında dokunun dondurularak dakikalar içinde incelendiği hızlı tanı yöntemidir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Meme koruyucu cerrahi yapılan bir hastanın ameliyatı sırasında cerrah, kitlenin derin sınırından şüphelenerek taze dokuyu patolojiye 'Frozen Kesit' için gönderiyor. Patoloğun dondurma kesitinde cerrahi sınırda tümör saptaması durumunda ameliyat masasındaki en doğru karar ne olmalıdır?",
                    [
                        {"text": "Cerrahın derin sınırdan ek bir doku tabakası çıkararak cerrahi sınırı temizlemesi", "isCorrect": True, "feedback": "Doğru yaklaşım. Frozen inceleme ameliyat bitmeden cerrahi sınırı netleştirerek hastayı ek ameliyattan korur."},
                        {"text": "Ameliyatı hemen bitirip hastayı hiçbir şey yapmadan uyandırmak", "isCorrect": False, "feedback": "Hatalı yaklaşım. Cerrahi sınırda kalan tümör nedeniyle hasta ikinci bir ameliyat geçirmek zorunda kalır."},
                        {"text": "Bütün memeyi, göğüs kaslarını ve tüm kolu anında ampute etmek", "isCorrect": False, "feedback": "Hatalı yaklaşım. Yalnızca pozitif olan sınırın temizlenmesi yeterlidir, gereksiz mutilasyondan kaçınılır."}
                    ]
                ),
                make_cloze(
                    "Ameliyat esnasında dokunun dondurularak yaklaşık 5-10 dakika içinde incelenmesini ve cerrahi sınırın temiz olup olmadığının belirlenmesini sağlayan yönteme [frozen] kesit adı verilir.",
                    "frozen",
                    "İntraoperatif dondurarak hızlı tanı yöntemi"
                )
            ]
        },

        # Adım 23
        {
            "slideNumber": 23,
            "title": "İyi Bir Patoloji Raporunun Standartları ve Kalite Kriterleri",
            "subtitle": "Klinik soruları doğrudan yanıtlayan, açık, net, kılavuzlara uyumlu ve hekimler arası anlaşılır rapor esastır.",
            "badge": "Kalite Standartları",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Bir patoloji raporunun temel amacı, mikroskobik bulguları klinisyenin hızla uygulayabileceği açık ve net bir tedavi kılavuzuna dönüştürmektir.

İdeal bir raporda kesin tanı ikirciksiz biçimde yer almalı ve belirsiz ifadelerden kaçınılmalıdır. Uluslararası standartlara dayanan **sinoptik raporlama** formatı sayesinde tümör boyutu, lenf nodu sayısı ve cerrahi sınır mesafesi gibi kritik parametrelerin atlanması engellenir. Rapor, klinisyenin ön tanısını doğrudan yanıtlamalı ve dar cerrahi sınırlarda re-eksizyon gibi ==klinik yönlendirici notlar== içermelidir. Ayrıca doku takibi sürecinin kalitesini bozmadan kabul edilebilir geri dönüş sürelerine uyulmalıdır.

> [TEMEL İLKE] İyi bir patoloji raporu, klinisyenin hastaya yönelik tedavi kararını tereddütsüz almasını sağlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Sinoptik Raporlama", "desc": "Kontrol listesi formatıyla eksiksiz standart parametre sunumu.", "isKey": True},
                    {"title": "Net Klinik Cevap", "desc": "Klinisyenin ameliyat öncesi sorduğu şüpheyi doğrudan aydınlatır.", "isKey": True},
                    {"title": "Zamanında Teslim", "desc": "Tanısal gecikmelerin hastanın tedavi şansını azaltması önlenir.", "isKey": False}
                ],
                "table": {
                    "title": "Geleneksel Serbest Metin Raporu vs Modern Sinoptik Rapor",
                    "headers": ["Özellik", "Geleneksel Serbest Rapor", "Modern Sinoptik Patoloji Raporu"],
                    "rows": [
                        ["Format", "Paragraf şeklinde uzun anlatım", "Madde madde kontrol listesi ve yapılandırılmış alanlar"],
                        ["Veri Eksikliği Riski", "Yüksek (patolog cerrahi sınırı yazmayı unutabilir)", "Sıfır (sistem eksik parametre olduğunda onay vermez)"],
                        ["Veri Madenciliği ve Yapay Zeka", "Metin analizi zordur, standart veri üretmez", "Elektronik sağlık kaydına (LBS) ve araştırmaya tam uyumludur"],
                        ["Klinisyenin Okuma Hızı", "Tüm metni taramak zorundadır", "Tanı, evre ve sınırları saniyeler içinde görür"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sinoptik raporlama; onkolojik rezeksiyonlarda hiçbir prognostik parametrenin atlanmamasını sağlayan standart formattır.",
                "📌 [SINAV SPOTU] İyi bir patoloji raporu klinisyenin 'Bu kitle nedir, tamamen çıktı mı, ek tedavi gerekir mi?' sorularını doğrudan yanıtlar.",
                "🚨 [KRİTİK UYARI] Patoloji raporunda cerrahi sınır mesafesi mutlaka milimetre cinsinden belirtilmelidir."
            ],
            "medicalTerms": [
                {"term": "Sinoptik Raporlama", "explanation": "Kritik tümör parametrelerini eksiksiz sunan standart kontrol listeli rapor formatıdır."},
                {"term": "Rapor Dönüş Süresi (Turnaround Time - TAT)", "explanation": "Biyopsinin laboratuvara kabulünden onaylı raporun çıkışına kadar geçen toplam süredir."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "Onkolojik patolojide 'Sinoptik Raporlama' sisteminin geleneksel serbest metin raporlarına göre en büyük hasta güvenliği avantajı nedir?",
                    "Zorunlu kontrol listesi kullandığı için tümör boyutu, lenf nodu sayısı ve cerrahi sınır gibi hayati prognostik verilerin atlanmasını engeller. Bu standardizasyon tedavi planlamasında veri eksikliğini sıfıra indirir."
                ),
                make_cloze(
                    "Kanser patolojisi raporlarında uluslararası kılavuzlarca önerilen ve tüm parametrelerin kontrol listesi halinde eksiksiz sunulduğu yapılandırılmış formata [sinoptik] raporlama denir.",
                    "sinoptik",
                    "Madde madde kontrol listeli raporlama biçimi"
                )
            ]
        },

        # Adım 24
        {
            "slideNumber": 24,
            "title": "İstek Formunun Önemi: Yaş, Cinsiyet, Girişim Türü ve Klinik Ön Tanı",
            "subtitle": "Klinik bilgi patolojinin pusulasıdır; eksik istek formu tanısal hataların en sık başlangıç noktasıdır.",
            "badge": "İstek Formu",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patoloji istek formu, hasta öyküsünü ve klinik şüpheyi laboratuvara taşıyan ==en kritik tanısal köprüdür==.

Formda hastanın yaş ve cinsiyeti mutlaka belirtilmelidir; çünkü benzer morfolojiler farklı yaş gruplarında bambaşka neoplazilere karşılık gelir. Doku örneğinin alındığı **kesin anatomik lokalizasyon**, taraf bilgisi ve yapılan cerrahi girişimin türü eksiksiz yazılmalıdır. Geçirilmiş radyoterapi, kemoterapi veya immünsüpresyon öyküsü gibi **klinik bilgiler**, patoloğun reaktif hücresel değişiklikleri maligniteden ayırt etmesini sağlar ve tanısal hataları önler.

> [TEMEL İLKE] Eksiksiz klinik bilgi içermeyen bir patoloji isteği, tanısal yanılgıların en sık başlangıç noktasıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Demografi", "desc": "Yaş ve cinsiyet ayırıcı tanının algoritmasını baştan sona değiştirir.", "isKey": True},
                    {"title": "Kesin Lokalizasyon", "desc": "Anatomik komşuluklar lezyonun benign-malign sınırını belirler.", "isKey": True},
                    {"title": "Özel Sorular", "desc": "Klinisyenin şüphesi patoloğun özel boyaları seçmesine rehberlik eder.", "isKey": False}
                ],
                "table": {
                    "title": "İstek Formunda Bulunması Zorunlu Bilgiler ve Tanısal Riskler",
                    "headers": ["İstek Formu Alanı", "Zorunlu İçerik", "Yazılmadığında Oluşabilecek Hata"],
                    "rows": [
                        ["Hastanın Yaşı", "Doğum tarihi ve tam yaş", "Çocukluk çağı küçük yuvarlak hücreli tümörlerinin yetişkin karsinomu sanılması"],
                        ["Anatomik Lokalizasyon", "Taraf (sağ/sol), organ, tam kadran", "Yanlış tarafa cerrahi yapılması veya yanlış organ atfı"],
                        ["Girişim Türü", "Eksizyonel vs İnsizyonel biyopsi", "Cerrahi sınırın pozitif sanılarak hastanın tekrar ameliyata alınması"],
                        ["Geçirilmiş Tedavi", "Radyoterapi / İmmünosüpresyon", "Radyasyon atipisinin sarkom, fırsatçı enfeksiyonun tümör sanılması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patoloji istek formunda yaş, cinsiyet, kesin anatomik lokalizasyon ve klinik ön tanı yazılması zorunludur.",
                "📌 [SINAV SPOTU] Aynı mikroskobik morfoloji hastanın yaşına göre tamamen zıt iki farklı hastalığa karşılık gelebilir.",
                "🚨 [KRİTİK UYARI] Taraf (sağ/sol) belirtilmeyen biyopsi kapları derhal ameliyathaneye iade edilmeli ve teslim alınmamalıdır."
            ],
            "medicalTerms": [
                {"term": "İnsizyonel Biyopsi", "explanation": "Büyük bir lezyondan tanı amacıyla sadece temsili bir parçanın çıkarılması işlemidir."},
                {"term": "Eksizyonel Biyopsi", "explanation": "Lezyonun tamamının sağlam çevre doku sınırıyla birlikte cerrahi olarak çıkarılmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Patoloji laboratuvarına gönderilen bir biyopsi istek formunda 'hastanın yaşı' bilgisinin bulunması ayırıcı tanıda neden en kritik faktörlerden biridir?",
                    {
                        "A": "Laboratuvar faturalandırma sisteminin yaşa göre otomatik fiyat belirlemesi için",
                        "B": "Mikroskop altında küçük yuvarlak mavi hücreli görünen bir tümörün çocukta nöroblastom/Wilms, yaşlıda ise küçük hücreli karsinom/lenfoma olabilmesi nedeniyle",
                        "C": "Yaşlı hastalarda parafin blokların daha düşük sıcaklıkta eritilmesinin gerekmesi için",
                        "D": "Genç hastaların biyopsilerine Hematoksilen boyasının tutunmaması nedeniyle",
                        "E": "Sadece adli vakalarda yaş tespiti yapılmasının kanunen zorunlu olması nedeniyle"
                    },
                    "B",
                    {
                        "A": "Yaş bilgisi idari faturalandırma için değil, doğru histopatolojik tanı için gereklidir.",
                        "B": "Benzer morfolojik lezyonlar çocuklarda ve yaşlılarda bütünüyle farklı tümörleri temsil eder.",
                        "C": "Parafin bloklama sıcaklığı standart laboratuvar protokolüdür, hastanın yaşıyla değişmez.",
                        "D": "Rutin histokimyasal boyaların kimyasal tutulumu hasta yaşıyla ilişkili değildir.",
                        "E": "Hastanın yaş bilgisi adli vakalarla sınırlı olmayıp tüm biyopsilerde zorunludur."
                    }
                ),
                make_cloze(
                    "Bir lezyonun tamamının sağlam doku sınırı ile birlikte çıkarılmasına eksizyonel biyopsi, kitleden yalnızca tanı amaçlı küçük bir parça alınmasına ise [insizyonel] biyopsi adı verilir.",
                    "insizyonel",
                    "Lezyonun bir kısmının tanı amaçlı çıkarılması"
                )
            ]
        },

        # Adım 25
        {
            "slideNumber": 25,
            "title": "Eksik veya Hatalı Klinik Bilginin Doğurabileceği Tanısal Tehlikeler",
            "subtitle": "Klinik bilgi yetersiz olduğunda patolog raporu geciktirir ve klinisyenden ek bilgi talep eder.",
            "badge": "Tanısal Tehlikeler",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Klinik bilginin eksik veya hatalı iletilmesi, patolojide ağır ==tanısal yanılgılara ve malpraktise== yol açabilir.

Örneğin pelvik radyoterapi öyküsü bilinmediğinde, radyasyonun stromal hücrelerde yol açtığı dev nükleer atipi invaziv bir sarkom veya karsinom sanılabilir. Benzer biçimde kortikosteroid kullanımı tüberküloz granülomlarını maskeleyebilir ya da ağır B12 eksikliği kemik iliğinde lösemiyi taklit edebilir. Bu nedenle sorumlu bir patolog, klinik verisi yetersiz veya şüpheli olgularda **raporu bekletir** ve klinisyenle doğrudan iletişime geçerek anamnezi netleştirir.

> [KRİTİK UYARI] Klinik bilgi doğrulanmadan şüpheli olgularda kesin malignite raporu verilmemelidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Raporun Bekletilmesi", "desc": "Klinik bilgi yetersizse patolog raporu onaylamaz ve bilgi ister.", "isKey": True},
                    {"title": "Radyasyon ve İlaç", "desc": "Tedavi sekelleri maligniteyi taklit eden en büyük yalancı pozitiflik nedenidir.", "isKey": True},
                    {"title": "Hasta Güvenliği", "desc": "Eksik bilgiyle acele rapor çıkarmak malpraktise zemin hazırlar.", "isKey": False}
                ],
                "table": {
                    "title": "Klinik Bilgi Eksikliğinde Sık Görülen Yalancı Pozitif ve Negatifler",
                    "headers": ["Klinik Durum", "Bilinmediğinde Yanıltıcı Görünüm", "Hatalı Teşhis Tehlikesi"],
                    "rows": [
                        ["Pelvik Radyoterapi", "Dev, hiperkromatik pleomorfik fibroblastlar", "İnvaziv sarkom veya karsinom sanılması"],
                        ["Megaloblastik Anemi", "Kemik iliğinde aşırı selülarite ve blast benzeri megaloblastlar", "Akut miyeloid lösemi sanılması"],
                        ["Kriyoterapi / Koterizasyon", "Nekroz, nükleer uzama ve hiperkromazi", "Termal hasarın malign nekroz sanılması"],
                        ["İmmünsüpresif Tedavi", "Zayıf granülom ve lenfoid doku silinmesi", "Tüberküloz ve lenfoma tanısının atlanması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Klinik bilgi yetersiz olduğunda patolog raporu geciktirebilir ve klinisyenden ek anamnez talep eder.",
                "🚨 [KRİTİK UYARI] Megaloblastik anemi kemik iliğinde lösemiyi; radyasyon fibrozu ise malign sarkomu taklit edebilir.",
                "📌 [SINAV SPOTU] Patolojide 'tahmin' kabul edilemez; klinik bilgi doğrulanmadan şüpheli olguda kesin malignite raporlanmaz."
            ],
            "medicalTerms": [
                {"term": "Yalancı Pozitiflik (False Positive)", "explanation": "Benign veya reaktif bir lezyonun hatalı şekilde malign olarak raporlanmasıdır."},
                {"term": "Yalancı Negatiflik (False Negative)", "explanation": "Mevcut bir malign lezyonun doku örneğinde atlanarak benign raporlanmasıdır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Patoloji uzmanı olarak incelediğiniz bir mesane biyopsisinde yaygın nükleer atipi ve dev pleomorfik hücreler görüyorsunuz. İstek formunda hiçbir klinik öykü yazılmamış. Bu aşamada en doğru patolojik tutumunuz ne olmalıdır?",
                    [
                        {"text": "Raporu onaylamayıp bekletmek; üroloğu arayarak hastanın daha önce pelvik radyoterapi veya intravezikal BCG alıp almadığını sorgulamak", "isCorrect": True, "feedback": "Doğru yaklaşım. Radyoterapi atipisinin bilinmesi hastayı gereksiz radikal sistektomiden korur."},
                        {"text": "Hemen 'Yüksek Dereceli İnvaziv Karsinom' raporu çıkarıp sisteme onay vermek", "isCorrect": False, "feedback": "Hatalı yaklaşım. Reaktif hücresel atipiyi kanser sanmak ağır bir malpraktis doğurur."},
                        {"text": "Doku parçalarını çöpe atıp biyopsiyi kayboldu olarak bildirmek", "isCorrect": False, "feedback": "Hatalı yaklaşım. Numuneyi imha etmek etik dışı ve yasal olarak suçtur."}
                    ]
                ),
                make_active_recall(
                    "Patolojide 'Yalancı Pozitiflik' ile 'Yalancı Negatiflik' hatalarından hangisi hastaya gereksiz organ kaybı ve toksik kemoterapi riski doğurur?",
                    "Yalancı pozitiflik hatasıdır. Selim bir sürecin kanser sanılması hastaya gereksiz radikal cerrahi uygulanmasına ve toksik onkolojik tedaviler verilmesine neden olur."
                )
            ]
        },

        # Adım 26
        {
            "slideNumber": 26,
            "title": "Klinikopatolojik Uyumsuzluklar: Karşılaşıldığında Ne Yapılmalıdır?",
            "subtitle": "Klinik şüphe ile patoloji sonucu çeliştiğinde; doğrudan hekim teması, blok tekrarı veya yeniden biyopsi şarttır.",
            "badge": "Uyumsuzluk Yönetimi",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Klinik ve radyolojik bulgular ile patoloji sonucunun çelişmesi durumu ==klinikopatolojik uyumsuzluk== olarak tanımlanır.

Kuvvetli bir kanser şüphesine rağmen patoloji raporu 'normal doku' geldiğinde bu sonuç kesin kabul edilip hasta takipsiz bırakılamaz. Biyopsi iğnesinin tümörü ıskalayarak komşu reaktif dokuyu örneklemesi (**sampling hatası**) sık görülen bir nedendir. Bu tabloda patolog ile klinisyen doğrudan iletişime geçer; laboratuvarda parafin bloktan **derin seri kesitler** alınır ve kalan dokudan ek örnekleme yapılır. Şüphe devam ederse görüntüleme eşliğinde biyopsi mutlaka tekrarlanır.

> [TEMEL İLKE] Klinik şüphe ile patoloji uyumsuz olduğunda doğrudan hekim teması ve gerekirse biyopsi tekrarı esastır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Uyumsuzluk Farkındalığı", "desc": "Klinik şüphe yüksekse 'benign' patoloji raporu körü körüne kabul edilmez.", "isKey": True},
                    {"title": "Laboratuvar Adımları", "desc": "Derin seri kesitler alınır, kalan makroskopi dokusu yeniden örneklenir.", "isKey": True},
                    {"title": "Yeniden Biyopsi", "desc": "Örnekleme hatası (tümörün ıskalanması) şüphesinde biyopsi tekrarlanır.", "isKey": False}
                ],
                "table": {
                    "title": "Klinikopatolojik Uyumsuzluk Algoritması",
                    "headers": ["Basamak", "Eylem", "Amaç"],
                    "rows": [
                        ["1. İletişim", "Klinisyen ve patoloğun doğrudan görüşmesi", "Klinik şüphenin ve patolojik bulgunun netleştirilmesi"],
                        ["2. Derin Kesit", "Parafin bloktan 5-10 seviye daha derine inilmesi", "Bloğun yüzeyinde görünmeyen tümör odağının yakalanması"],
                        ["3. Ek Örnekleme", "Kavanozda saklanan makroskobik dokunun incelenmesi", "Farklı alanlardan yeni doku kasetleri hazırlanması"],
                        ["4. Yeniden Biyopsi", "Görüntüleme rehberliğinde lezyondan tekrar örnek alınması", "İlk biyopsideki örnekleme hatasının (ıskalama) giderilmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Klinik şüphe ile patoloji sonucu uyumsuz olduğunda klinisyen-patolog teması ve derin kesit incelemesi zorunludur.",
                "🚨 [KRİTİK UYARI] Biyopsi iğnesi tümörü ıskalayıp çevre normal dokudan örnek almış olabilir (sampling hatası); şüphe sürüyorsa biyopsi tekrarlanmalıdır.",
                "📌 [SINAV SPOTU] Bir klinik şüphe güçlü ise tek bir 'benign' biyopsi raporu maligniteyi tamamen dışlamaya yetmez."
            ],
            "medicalTerms": [
                {"term": "Sampling Hatası (Örnekleme Hatası)", "explanation": "Biyopsi sırasında lezyonun ıskalanarak komşu normal dokudan parça alınması hatasıdır."},
                {"term": "Derin Seri Kesit", "explanation": "Parafin bloğun daha derin tabakalarından mikrotomla ek kesitler alınarak incelenmesidir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Meme muayenesinde sert, fikse, meme başını çeken kitle saptanan ve mamografide spiküle malign kalsifikasyonları olan 55 yaşındaki bir kadının kor (tru-cut) biyopsi patoloji raporu 'Normal meme parankimi ve fibroadipöz doku' olarak geliyor. Cerrah olarak yaklaşımınız ne olmalıdır?",
                    [
                        {"text": "Patoloji raporunun klinikopatolojik uyumsuzluk (örnekleme hatası) taşıdığını fark ederek patologla görüşmek ve USG eşliğinde biyopsiyi tekrarlamak", "isCorrect": True, "feedback": "Doğru klinik yaklaşım. Aşikar malignite şüphesinde normal rapor sampling hatasını düşündürür ve biyopsi tekrarlanmalıdır."},
                        {"text": "'Patoloji temiz gelmiş, hastada kanser yok' diyerek hastayı 1 yıl sonra kontrole çağırmak", "isCorrect": False, "feedback": "Hatalı yaklaşım. Tümörün ıskalanması göz ardı edilirse hastalık hızla metastaz yapar."},
                        {"text": "Biyopsi sonucuna bakarak hastaya derhal radyoterapi başlamak", "isCorrect": False, "feedback": "Hatalı yaklaşım. Histopatolojik doku doğrulaması olmadan radyoterapi uygulanamaz."}
                    ]
                ),
                make_cloze(
                    "Biyopsi iğnesinin tümör odağını ıskalayarak komşu normal dokudan parça alması sonucu gelişen duruma [örnekleme] hatası adı verilir.",
                    "örnekleme",
                    "Lezyonun hedeflenememesi ve ıskalanması (sampling hatası)"
                )
            ]
        },

        # Adım 27
        {
            "slideNumber": 27,
            "title": "Çok Disiplinli Tümör Konseyleri ve Morbidite-Mortalite Toplantıları",
            "subtitle": "Kanser hastasının kaderi tek bir hekimin odasında değil; tümör konseyindeki multidisipliner konsensüsle çizilir.",
            "badge": "Tümör Konseyi",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Modern onkolojik tedavinin temel karar organı, farklı uzmanlıkların ortak konsensüs oluşturduğu ==Çok Disiplinli Tümör Konseyleridir==.

Bu konseylerde cerrah, medikal onkolog, radyasyon onkoloğu, radyolog ve **patoloji uzmanı** bir araya gelir. Patolog mikroskobik görüntüleri canlı paylaşarak tümörün histolojik tipini, derecesini, cerrahi sınır mesafesini ve immünohistokimyasal reseptör profilini kurula aktarır. Elde edilen ortak verilerle cerrahi öncesi **neoadjuvan** tedavi veya operasyon sonrası adjuvan protokoller kararlaştırılır. Komplikasyonlu vakaların incelendiği morbidite-mortalite toplantıları ise sistemik hataların giderilmesini sağlar.

> [YÜKSEK VERİM] Tümör konseylerinde multidisipliner yaklaşımla tedavi edilen hastalarda sağkalım oranları belirgin olarak daha yüksektir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Çok Disiplinli Masa", "desc": "Patolog, onkolog, cerrah ve radyolog her vakayı ortak konsensüsle yönetir.", "isKey": True},
                    {"title": "Canlı Mikroskopi", "desc": "Patolog tümör histolojisini ve cerrahi sınırları ekranda hekimlere gösterir.", "isKey": True},
                    {"title": "Kanıta Dayalı Tedavi", "desc": "Neoadjuvan, cerrahi ve adjuvan tedavi sıralaması konseyde kararlaştırılır.", "isKey": False}
                ],
                "table": {
                    "title": "Tümör Konseyinde Branşların Sorumluluk Matrisi",
                    "headers": ["Branş", "Konseye Sunduğu Temel Veri", "Tedavi Kararına Katkısı"],
                    "rows": [
                        ["Patoloji", "Histolojik tip, grade, cerrahi sınır, pTNM, İHK/moleküler profil", "Hastalığın biyolojik kimliği ve hedefe yönelik ilaç uygunluğu"],
                        ["Radyoloji", "Tümörün anatomik komşulukları, damar invazyonu, uzak organ taraması", "Tümörün cerrahi olarak rezeke edilebilirliği (rezektabilite)"],
                        ["Cerrahi Branş", "Hastanın ameliyat tolere edebilirlik durumu ve cerrahi plan", "Primer cerrahi veya neoadjuvan tedavi sonrası rezeksiyon kararı"],
                        ["Medikal Onkoloji", "Sistemik kemoterapi, immünoterapi ve akıllı ilaç seçenekleri", "Adjuvan veya palyatif sistemik tedavi protokolünün yönetimi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Tümör konseyleri, patolog ve klinisyenlerin kanser tedavisini multidisipliner olarak ortak kararlaştırdığı kuruldur.",
                "📌 [SINAV SPOTU] Patoloğun tümör konseyindeki rolü; doku tanısını, cerrahi sınırları ve moleküler belirteçleri doğrudan klinik heyete sunmaktır.",
                "🚨 [KRİTİK UYARI] M&M (Morbidite-Mortalite) toplantıları kişileri suçlama platformu değil; sistemik hataları analiz ederek kalite artıran eğitim ortamıdır."
            ],
            "medicalTerms": [
                {"term": "Neoadjuvan Tedavi", "explanation": "Tümörü cerrahi öncesinde küçülterek rezeksiyonu kolaylaştıran ameliyat öncesi tedavidir."},
                {"term": "Adjuvan Tedavi", "explanation": "Cerrahi sonrası mikroskobik odakları yok etmek ve nüksü önlemek için verilen ek tedavidir."},
                {"term": "Rezektabilite", "explanation": "Tümörün cerrahi olarak temiz sınırlarla güvenle çıkarılabilme durumudur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Çok disiplinli tümör konseylerinde (Tumor Board) patoloğun üstlendiği temel klinik sorumluluk aşağıdakilerden hangisidir?",
                    {
                        "A": "Hastanın ameliyat masraflarını hesaplayıp tahsilat planını onaylamak",
                        "B": "Tümörün histolojik tipini, derecesini, cerrahi sınırlarını ve moleküler belirteçlerini heyete sunarak tedavi algoritmasına yön vermek",
                        "C": "Hastanın ameliyatını bizzat cerrahın yerine gerçekleştirmek",
                        "D": "Radyoloji görüntülerini cerrahtan gizleyerek sadece kendi mikroskop camını esas almak",
                        "E": "Tümörün genetik testlerini yapmayı reddederek sadece 1800'lü yılların mikroskop yöntemlerini savunmak"
                    },
                    "B",
                    {
                        "A": "İdari ve mali süreçler konseyin tartışma alanı değildir.",
                        "B": "Patolog tümör biyolojisini, evresini ve moleküler hedeflerini kurula sunarak tedavi stratejisini belirler.",
                        "C": "Cerrahi rezeksiyonu konseydeki ilgili cerrahi uzmanı gerçekleştirir.",
                        "D": "Konseyler branşlar arası şeffaf veri paylaşımı ve işbirliği esasına dayanır.",
                        "E": "Modern patoloji moleküler ve genetik incelemeleri tedaviye entegre eder."
                    }
                ),
                make_cloze(
                    "Büyük bir tümörü cerrahi olarak çıkarılabilir hale getirmek amacıyla ameliyattan ÖNCE uygulanan kemoterapi veya radyoterapiye [neoadjuvan] tedavi adı verilir.",
                    "neoadjuvan",
                    "Ameliyat öncesi küçültücü onkolojik tedavi"
                )
            ]
        },

        # Adım 28
        {
            "slideNumber": 28,
            "title": "Patolojide Tıbbi Hata Önleme ve Hasta Güvenliği Standartları",
            "subtitle": "Materyal kabulünden rapor imzasına kadar barkodlama, çift kontrol ve sıfır hata toleransı geçerlidir.",
            "badge": "Hasta Güvenliği",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patoloji laboratuvarında doku veya kimlik karışıklığı, geri dönüşsüz organ kayıplarına yol açabileceğinden ==sıfır hata toleransı== esastır.

Hasta güvenliğini sağlamak amacıyla materyal kabulünde ad-soyad ve kimlik numarası olmak üzere **iki bağımsız doğrulayıcı** kullanılır. Numuneler kabul edildiği andan itibaren kaset ve lamlara lazerle işlenen **barkodlama sistemleriyle** takip edilir; manuel etiketleme yapılmaz. Mikrotom su banyosunda önceki doku kırıntılarının bulaşması (**floater**) titizlikle engellenir. İlk defa kanser tanısı alan veya şüpheli tüm olgular, departman içinde ikinci bir patolog tarafından incelenerek çift kontrol sağlanır.

> [TEMEL İLKE] Patolojide hız değerlidir; ancak doğruluk ve hasta güvenliği her zaman önceliklidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Sıfır Tolerans", "desc": "Numune karışması geri döndürülemez cerrahi ve hukuki felaketler yaratır.", "isKey": True},
                    {"title": "Lazer Barkodlama", "desc": "Kaset ve lamlar üzerine barkod kazınarak manuel etiket hataları engellenir.", "isKey": True},
                    {"title": "İkinci Görüş", "desc": "Tüm yeni kanser tanıları departman içinde ikinci patologla teyit edilir.", "isKey": False}
                ],
                "table": {
                    "title": "Patoloji Laboratuvarında Kritik Güvenlik Kontrol Noktaları",
                    "headers": ["Aşama", "Olası Hata Riski", "Uygulanan Güvenlik Standardı"],
                    "rows": [
                        ["Numune Kabulü", "Farklı hastanın biyopsi kaplarının karışması", "İki kimlik doğrulayıcı ve anında LBS protokol numarası üretimi"],
                        ["Makroskopi ve Kasetleme", "Parçanın yanlış kasede konması", "Kaset üzerine silinmez 2D karekod lazer baskısı"],
                        ["Mikrotomi (Kesit Alma)", "Yüzdürme banyosunda önceki hastadan doku taşınması (floaters)", "Her blok kesiminden sonra su banyosunun temizlenmesi"],
                        ["Rapor Onayı", "Raporun yanlış hastanın dosyasına girilmesi", "Patoloğun imzalamadan önce kimlik ve lezyon tarafını son kontrolü"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojide doku kasetleri ve lamlar üzerinde silinmez barkod/karekod kullanılması kimlik karışmasını önleyen altın standarttır.",
                "🚨 [KRİTİK UYARI] Mikrotom su banyosunda önceki hastadan kalan doku kırıntıları (floater) sonraki hastanın lamına yapışarak yanlış kanser tanısı koydurabilir.",
                "📌 [SINAV SPOTU] İlk defa kanser tanısı alan biyopsilerde departman içi ikinci uzman kontrolü kalite standardıdır."
            ],
            "medicalTerms": [
                {"term": "Floater (Doku Sıçraması / Kırıntı)", "explanation": "Hazırlık aşamasında başka bir hastaya ait doku kırıntısının preparata bulaşmasıdır."},
                {"term": "İki Bağımsız Doğrulayıcı", "explanation": "Kimlik karışmasını önlemek için en az iki bağımsız verinin birlikte doğrulanmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Patoloji laboratuvarında mikrotomi (kesit alma) aşamasında su banyosunun her bloktan sonra temizlenmemesi durumunda ortaya çıkabilecek en tehlikeli teknik hata hangisidir?",
                    {
                        "A": "Banyodaki suyun sıcaklığının oda sıcaklığına düşmesi",
                        "B": "Önceki hastanın tümör kırıntısının (floater) sonraki hastanın temiz lamına yapışarak sağlıklı bireye yanlış kanser tanısı konulması",
                        "C": "Hematoksilen boyasının mikrotom bıçağını paslandırması",
                        "D": "Formalin kokusunun odaya yayılması",
                        "E": "Parafin blokların ağırlığının mikrogram düzeyinde azalması"
                    },
                    "B",
                    {
                        "A": "Su banyoları termostatik sistemle ısıtılır, temizlikle sıcaklığı düşmez.",
                        "B": "Önceki hastadan sıçrayan kanser hücresi masum bir hastaya yanlış kanser tanısı koydurabilir.",
                        "C": "Boyama aşaması mikrotomda değil ayrı boyama cihazlarında gerçekleştirilir.",
                        "D": "Su banyosunda formalin değil distile su kullanılır.",
                        "E": "Parafin blok kütlesi tanısal süreçle ilişkili bir hata kaynağı değildir."
                    }
                ),
                make_cloze(
                    "Laboratuvar hazırlık basamaklarında başka bir hastadan kopup gelen yabancı doku parçacığının lama yapışarak yanlış tanı oluşturması artefaktına [floater] adı verilir.",
                    "floater",
                    "Başka hastadan sıçrayan doku kırıntısı artefaktı"
                )
            ]
        },

        # Adım 29 (CHECKPOINT 3)
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Patolojinin Klinik Önemi ve Patoloğun Rolü",
            "subtitle": "Altın standart tanı, sinoptik raporlama, frozen konsültasyonu ve klinikopatolojik uyumsuzluk yönetimini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 3,
            "synthesisNarrative": """Patoloji, klinik onkolojide kesin tanıyı ve tedavi yetkisini belirleyen ==tartışmasız altın standarttır==.

Nitelikli bir cerrahi patoloji raporu; histolojik tanı, diferansiyasyonu gösteren grade, anatomik yayılımı belirten pTNM evresi ve cerrahi sınır durumunu eksiksiz sunmalıdır. Patolog, ameliyat sırasında **frozen kesit** ile rezeksiyon sınırlarını tayin eden ve tümör konseylerinde tedavi rotası çizen konsültan bir hekimdir. Klinikopatolojik uyumsuzluklarda şüphe sürdükçe biyopsi tekrarlanmalı; istek formunun eksiksiz doldurulması ve barkodlama ile hasta güvenliği güvenceye alınmalıdır.

> [BÖLÜM ÖZETİ] Klinisyen ile patoloğun şeffaf iletişimi ve klinikopatolojik korelasyon, hatasız onkolojik tedavinin temelidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Altın Standart", "desc": "Neoplastik hastalıklarda tedavi patolojik tanı olmadan başlayamaz.", "isKey": True},
                    {"title": "Sinoptik Standart", "desc": "Kontrol listesiyle tüm evreleme ve sınır parametreleri sunulur.", "isKey": True},
                    {"title": "Uyumsuzlukta Şüphe", "desc": "Klinik kanser şüphesi güçlüyse benign rapor kabul edilmez, biyopsi tekrarlanır.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 3 Klinik Patoloji İlkeleri Sentezi",
                    "headers": ["Klinik Alan", "Temel Kural", "Hayati Sonuç"],
                    "rows": [
                        ["Neoplazi Tanısı", "Patolojik doku doğrulaması şarttır", "Yanlış veya gereksiz kemoterapi ve organ kaybı önlenir"],
                        ["Cerrahi Sınır", "Pozitif sınır geride tümör kaldığını gösterir", "Hastaya acil re-eksizyon veya ek radyoterapi planlanır"],
                        ["İstek Formu", "Yaş, lokalizasyon ve tedavi öyküsü zorunludur", "Radyasyon atipisinin kanser sanılması engellenir"],
                        ["Uyumsuzluk", "Klinik şüphe sürüyorsa biyopsi tekrarlanır", "Örnekleme hatasına (ıskalama) bağlı gecikmeler önlenir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Histolojik Grade hücresel diferansiyasyonu (mikroskobik agresifliği), Evre (Stage) ise tümörün anatomik yayılım genişliğini gösterir.",
                "📌 [SINAV SPOTU] Frozen kesit (intraoperatif konsültasyon) ameliyat esnasında cerrahi sınırı netleştirmek için yaklaşık 5-10 dakikada yapılan dondurma incelemesidir.",
                "🚨 [KRİTİK UYARI] Mikrotom su banyosundan bulaşan doku kırıntısı (floater), sağlıklı bir preparatta yalancı kanser tanısına yol açabilir."
            ],
            "medicalTerms": [
                {"term": "Sinoptik Raporlama", "explanation": "Tümör tipi, evresi ve cerrahi sınırları kontrol listesiyle sunan standart rapordur."},
                {"term": "Floater", "explanation": "İşlemler sırasında başka bir hastadan preparata bulaşan yabancı doku kırıntısıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p3-1",
                    "Tümör patolojisinde Derece (Grade) ile Evre (Stage) arasındaki en temel kavramsal fark nedir?",
                    "Derece (Grade) tümör hücrelerinin mikroskop altındaki diferansiyasyon ve mitotik agresiflik derecesini gösterir. Evre (Stage/pTNM) ise tümörün vücuttaki anatomik yayılım genişliğini (çap, lenf nodu ve metastaz) ifade eder.",
                    "Hücresel vs Anatomik",
                    "Klinik Onkoloji"
                ),
                make_flashcard(
                    "fc-p3-2",
                    "Klinisyenin fizik muayene ve görüntülemede kesin kanser düşündüğü bir kitlede patoloji raporu 'normal doku' gelirse (klinikopatolojik uyumsuzluk) hekimin yaklaşımı ne olmalıdır?",
                    "Rapor körü körüne kabul edilip hasta taburcu edilemez. Patologla doğrudan görüşülmeli, bloktan derin seri kesitler alınmalı ve tümörün ıskalanmış olabileceği (sampling hatası) düşünülerek biyopsi mutlaka tekrarlanmalıdır.",
                    "Uyumsuzluk algoritması",
                    "Tanısal Güvenlik"
                ),
                make_flashcard(
                    "fc-p3-3",
                    "Ameliyat esnasında yapılan 'Frozen Kesit' (intraoperatif konsültasyon) incelemesinin en kritik cerrahi endikasyonu nedir?",
                    "Ameliyat bitmeden önce cerrahi sınırların tümörden temiz olup olmadığını doğrulamak ve lezyonun malign/benign ayrımını yaparak cerrahın rezeksiyon sınırını anında genişletmesini sağlamaktır.",
                    "Ameliyat içi hızlı tanı",
                    "Cerrahi Patoloji"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 3'te incelenen cerrahi patoloji ve raporlama ilkeleri dikkate alındığında, aşağıdakilerden hangisi yanlıştır?",
                    {
                        "A": "Cerrahi sınırın pozitif olması, tümörün kesi hattında devam ettiğini ve geride tümör kaldığını gösterir.",
                        "B": "Radyoterapi almış dokulardaki atipik fibroblastlar morfolojik olarak malign sarkomu taklit edebilir.",
                        "C": "Patoloji laboratuvarında su banyosunun temizlenmesi floater artefaktını engellemek için zorunludur.",
                        "D": "Sinoptik raporlama sistemi gereksiz bir bürokrasidir ve serbest metin raporları daima daha güvenilirdir.",
                        "E": "Tümör konseyleri kanser hastalarında multidisipliner konsensüs ile sağkalımı artıran konseylerdir."
                    },
                    "D",
                    {
                        "A": "Pozitif cerrahi sınır rezeksiyon hattında rezidüel tümör kaldığını kanıtlar.",
                        "B": "Radyoterapiye bağlı hücresel atipi morfolojik olarak karsinom veya sarkomu taklit edebilir.",
                        "C": "Su banyosunun temizlenmesi floater kaynaklı yanlış pozitif tanıyı engeller.",
                        "D": "Sinoptik raporlama kritik prognostik verilerin atlanmasını önleyen uluslararası standarttır.",
                        "E": "Tümör konseyleri multidisipliner konsensüs ile kanser sağkalımını belirgin biçimde artırır."
                    }
                ),
                make_active_recall(
                    "Patoloji raporunda 'Lenfovasküler İnvazyon (LVI) Pozitif' ifadesi klinisyen ve hasta için ne anlama gelir?",
                    "Tümör hücrelerinin kan veya lenf damarlarının lümenine girdiğini gösterir. Bu bulgu metastaz riskini artıran bağımsız bir kötü prognostik faktördür ve adjuvan kemoterapi gereksinimini destekler."
                )
            ]
        }
    ]
