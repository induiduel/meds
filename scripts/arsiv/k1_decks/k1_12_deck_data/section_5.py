# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-12-s41",
        "title": "Kronik Enflamasyon Sitokinleri: Makrofaj-T Lenfosit Diyaloğu",
        "content": "Akut enflamasyon patojeni temizleyemediğinde süreç haftalar ve aylar süren **kronik enflamasyona** evrilir. Kronik enflamasyonun merkezinde granülositler (nötrofiller) değil; mononükleer hücreler olan **Makrofajlar ve T Lenfositler** yer alır. Bu iki hücre grubu birbirlerini karşılıklı olarak sürekli uyaran iki yönlü bir 'sitokin döngüsü (amplifikasyon aksı)' kurarlar:\n\n1. Doku makrofajı antijeni T hücrelerine sunar ve **IL-12** salgılar.\n2. IL-12'yi alan naif CD4+ T hücresi **Th1 fenotipine** farklılaşarak yoğun miktarda **İnterferon-gama (IFN-γ)** üretir.\n3. IFN-γ geri dönerek makrofajı 'klasik aktive (M1)' hale getirir. M1 makrofaj daha fazla TNF, IL-1 ve reaktif oksijen türeterek doku hasarını sürdürür.\n\nBu kısır döngü tüberküloz, sarkoidoz, romatoid artrit ve Crohn hastalığı gibi kronik granülomatöz ve otoimmün tabloların temel moleküler motorudur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Akut ve Kronik Sitokin Eksenleri Karşılaştırması",
                "Akut Enflamasyon Ekseni",
                "TNF ve IL-1 baskındır; nötrofil rekrutmanı, endotel aktivasyonu ve hızlı eksüda üretilir.",
                "Kronik Enflamasyon Ekseni",
                "IFN-γ, IL-12 ve IL-17 baskındır; makrofaj-lenfosit işbirliği, doku yıkımı ve fibrozis gelişir."
            ),
            make_cloze(
                "Kronik enflamasyonda makrofaj ve T lenfositler karsılıklı olarak IL-12 ve IFN-gama sitokinleriyle birbirini sürekli aktive eder.",
                "IL-12 ve IFN-gama",
                "Makrofaj-Th1 aksının iki kilit iletişim sitokini"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-12-s42",
        "title": "İnterferon-Gama (IFN-γ): Klasik Makrofaj Aktivasyonu (M1)",
        "content": "İnterferon-gama (IFN-γ / Tip II İnterferon), hücresel bağışıklığın ve kronik enflamasyonun tartışmasız en güçlü aktivatörüdür. Temel hücresel kaynakları antijenle uyarılmış **Th1 T lenfositleri ve Doğal Katil (NK) hücreleridir**. IFN-γ'nın hedefi doku monosit ve makrofajlarıdır:\n\n- **M1 (Klasik) Makrofaj Fenotipi:** Makrofaj yüzeyindeki IFNGR reseptörüne bağlanan IFN-γ, JAK-STAT1 yolağını aktive eder. Makrofaj sitoplazmik hacmini artırır, lizozomal enzim içeriğini katlar ve membran yüzeyinde MHC Sınıf II moleküllerini artırır.\n- **İndüklenebilir NO Sentaz (iNOS) ve Oksidatif Patlama:** Makrofajda iNOS enzimini indükleyerek yüksek miktarda Nitrik Oksit (NO) ve serbest oksijen radikalleri (ROS) ürettirir; hücre içi bakterileri (örneğin *Mycobacterium tuberculosis*) öldürme yeteneği maksimuma çıkar.\n- **Epiteloid Hücre ve Dev Hücre Dönüşümü:** Granülomatöz enflamasyonda makrofajların geniş eozinofilik sitoplazmalı epiteloid histiyositlere ve kaynaşarak Langhans tipi dev hücrelere dönüşmesini bizzat IFN-γ yönetir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "IFN-Gama Aracılı M1 Aktivasyon Zinciri",
                [
                    "1. Th1 Aktivasyonu: T lenfositinin antijen uyarısıyla IFN-γ sekrete etmesi",
                    "2. Makrofaj Reseptör Bağlanması: IFNGR ile JAK-STAT1 transkripsiyonunun uyarılması",
                    "3. iNOS ve Lizozomal Patlama: Mikrobisidal NO ve ROS üretiminin tavan yapması",
                    "4. Granülomatöz Dönüşüm: Makrofajların epiteloid ve çok çekirdekli dev hücrelere evrilmesi"
                ]
            ),
            make_recall(
                "Kronik enflamasyonda makrofajları klasik M1 yolunda aktive ederek mikrobisidal gücü artıran temel sitokin hangisidir?",
                "İnterferon-gamadır (IFN-γ).",
                "Th1 hücrelerinin majör efektör sitokini"
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-12-s43",
        "title": "İnterlökin-12 (IL-12): Th1 Yanıtının Başlatıcısı ve IFN-γ İndükleyicisi",
        "content": "İnterlökin-12 (IL-12), p35 ve p40 alt birimlerinden oluşan heterodimerik bir sitokindir. Temel hücresel kaynakları intraselüler patojenlerle (bakteriler, parazitler, virüsler) karşılaşan **antijen sunan hücrelerdir (doku makrofajları ve dendritik hücreler)**. IL-12'nin organizmadaki vazgeçilmez görevi, naif CD4+ T yardımcı lenfositlerin (Th0) kaderini belirlemektir:\n\n1. Naif T hücrelerindeki IL-12 reseptörüne bağlanarak STAT4 transkripsiyon faktörünü ve T-bet ana düzenleyicisini aktive eder; hücreyi **Th1 alt kümesine farklılaştırır**.\n2. Hem Th1 hücrelerinden hem de NK hücrelerinden **İnterferon-gama (IFN-γ)** salgılanmasını kat kat artırır.\n3. Sitotoksik CD8+ T lenfositlerin ve NK hücrelerinin hücre öldürme (sitotoksisite) kapasitesini uyarır.\n\nIL-12 veya reseptör eksikliği olan bireylerde atipik mikobakteri enfeksiyonlarına ve salmonelloza karşı ağır genetik yatkınlık (MSMD sendromu) gelişir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Makrofajlar ve dendritik hücreler tarafından salgılanarak naif T lenfositleri Th1 fenotipine yönlendiren ve IFN-γ üretimini indükleyen temel sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterlökin-12 (IL-12)", "explanation": "A seçeneği DOĞRUDUR: IL-12 Th1 farklılaşmasını ve IFN-γ sentezini başlatan anahtar sitokindir."},
                    {"key": "B", "text": "İnterlökin-4 (IL-4)", "explanation": "B seçeneği yanlıştır: IL-4 Th2 fenotipine yönlendirir."},
                    {"key": "C", "text": "İnterlökin-10 (IL-10)", "explanation": "C seçeneği yanlıştır: İmmünsüpresif anti-inflamatuar sitokindir."},
                    {"key": "D", "text": "Histamin", "explanation": "D seçeneği yanlıştır: Vazoaktif amindir."},
                    {"key": "E", "text": "Bradikinin", "explanation": "E seçeneği yanlıştır: Kinin peptitidir."}
                ],
                "A"
            ),
            make_cloze(
                "Makrofaj ve dendritik hücre kaynaklı IL-12 naif T hücrelerini Th1 soyuna farklılaştırarak hücresel bağışıklığı başlatır.",
                "Th1 soyuna",
                "Hücresel bağışıklığı yöneten T yardımcı hücre alt grubu"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-12-s44",
        "title": "İnterlökin-17 (IL-17): Th17 Hücreleri ve Nötrofilik Enflamasyon",
        "content": "Son yıllarda kronik enflamasyon ve otoimmünite patogenezinde en büyük çığırı açan sitokin **İnterlökin-17'dir (IL-17)**. Başlıca **Th17 lenfositleri** (farklılaşmaları IL-6 ve IL-23 ile uyarılır) tarafından salgılanır. IL-17 epitel hücreleri, endotel ve fibroblastlar üzerindeki reseptörlerine bağlanarak olağanüstü bir lökosit rekrutmanı başlatır:\n\n- **Kemokin ve G-CSF İndüksiyonu:** Dokudan yoğun CXCL8 (IL-8) kemokini ve G-CSF salgılanmasını tetikler; bu sayede kronikleşen bir dokuya adeta akut enflamasyon gibi **masif nötrofil ve monosit akını** gerçekleşir.\n- **Antimikrobiyal Peptitler:** Cilt ve mukozalarda defensin üretimini artırarak ekstraselüler bakteriyel ve fungal (özellikle *Candida albicans*) enfeksiyonlara karşı birinci basamak savunma kurar.\n- **Otoimmün Hastalıklardaki Rolü:** Aşırı veya kontrolsüz IL-17 üretimi **Psöriyazis (sedef hastalığı), Romatoid Artrit, Ankilozan Spondilit ve Multipl Skleroz** gibi kronik destruktif hastalıkların temel patofizyolojik zeminini oluşturur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hücre / Sitokin", "Primer Görevi", "İlişkili Klinik Patoloji"],
                [
                    [
                        {"text": "Th17 / IL-17", "isMasked": False, "hint": ""},
                        {"text": "Nötrofil ve monosit rekrutmanı, defensin artışı", "isMasked": True, "hint": "Kronik dokuya nötrofil çağırma gücü"},
                        {"text": "Psöriyazis, Romatoid Artrit, Ankilozan Spondilit", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Th1 / IFN-γ", "isMasked": False, "hint": ""},
                        {"text": "Klasik makrofaj aktivasyonu (M1) ve granülom", "isMasked": True, "hint": "Hücresel intraselüler temizlik"},
                        {"text": "Tüberküloz, Sarkoidoz, Crohn hastalığı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Th2 / IL-4, IL-13", "isMasked": False, "hint": ""},
                        {"text": "Eozinofil alımı, IgE sentezi ve M2 onarım", "isMasked": True, "hint": "Alerjik ve paraziter savunma"},
                        {"text": "Alerjik astım, egzama ve doku fibrozisi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Th17 lenfositleri tarafından üretilerek dokuya nötrofil toplayan ve psöriyazis tedavisinde monoklonal antikorlarla hedeflenen sitokin nedir?",
                "İnterlökin-17'dir (IL-17).",
                "Sedef ve ankilozan spondilitin kilit sitokini"
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-12-s45",
        "title": "Alternatif Makrofaj Aktivasyonu (M2): IL-4, IL-13 ve Doku Onarımı",
        "content": "Makrofajlar tek tip hücreler olmayıp çevre sitokin sinyallerine göre birbirine tamamen zıt iki kutba farklılaşabilirler. IFN-γ makrofajı mikrop öldüren yıkıcı 'M1' kutbuna çekerken; **İnterlökin-4 (IL-4) ve İnterlökin-13 (IL-13)** sitokinleri makrofajı **'M2 (Alternatif Aktive Makrofaj)'** kutbuna dönüştürür:\n\n- **M2 Fenotipinin Görevleri:** M2 makrofajlar mikrop öldürücü reaktif oksijen ve nitrik oksit üretmezler (iNOS kapalıdır; arginaz-1 enzimi ile ornitin ve prolin üretirler). Temel görevleri doku onarımı ve enflamasyonun yatıştırılmasıdır.\n- **Büyüme Faktörleri Salınımı:** Yüksek miktarda **TGF-β (Transforming Growth Factor-beta)**, PDGF ve FGF salgılarlar; fibroblast proliferasyonunu, kollajen sentezini ve yeni damar oluşumunu (anjiyogenez) uyarırlar.\n- **Klinik Risk (Patolojik Fibrozis):** Eğer M2 aktivasyonu aşırı veya kontrolsüz sürerse, doku sklerozuna, karaciğer sirozuna, idiyopatik pulmoner fibrozise ve organ yetmezliğine yol açar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "M1 ve M2 Makrofaj Kutuplaşması",
                "M1 Makrofaj (Klasik / IFN-γ)",
                "Mikrobisidal NO ve ROS üretir, pro-inflamatuar sitokinler salar, doku yıkımı ve savunma yapar.",
                "M2 Makrofaj (Alternatif / IL-4, IL-13)",
                "Anti-inflamatuardır; arginaz-1, TGF-β ve büyüme faktörleri ile yara iyileşmesi ve fibrozis yapar."
            ),
            make_cloze(
                "Makrofajların alternatif M2 aktivasyonunu indükleyerek yara onarımı ve kolajen sentezini baslatan sitokinler IL-4 ve IL-13 tür.",
                "IL-4 ve IL-13 tür",
                "Th2 kökenli iki alternatif makrofaj indükleyici sitokin"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-12-s46",
        "title": "Tip I İnterferonlar (IFN-α, IFN-β): Antiviral Savunma",
        "content": "Tip I İnterferon ailesi; plazmasitoid dendritik hücreler ve lökositler tarafından üretilen **İnterferon-alfa (IFN-α)** ile fibroblastlar ve enfekte epitel hücreleri tarafından üretilen **İnterferon-beta'yı (IFN-β)** kapsar. Hücre içi viral nükleik asitlerin (çift sarmallı RNA) sitoplazmik RIG-I ve MDA5 sensörleri veya endozomal TLR3/7/9 tarafından algılanmasıyla transkripsiyonları başlar. Başlıca fonksiyonları:\n\n1. **Antiviral Durum İndüksiyonu:** Parakrin etkiyle komşu sağlıklı hücrelerin IFNAR reseptörlerine bağlanırlar; protein kinaz R (PKR) ve 2'-5' oligoadenilat sentaz enzimlerini aktive ederek viral mRNA translasyonunu durdururlar ve viral genomu parçalarlar.\n2. **Sitotoksisite Uyarımı:** Tüm çekirdekli hücrelerde **MHC Sınıf I** moleküllerinin ekspresyonunu artırarak enfekte hücrelerin Sitotoksik CD8+ T lenfositler tarafından tanınmasını sağlarlar; NK hücrelerinin litik aktivitesini güçlendirirler.\n3. **Sistemik Semptomlar:** Viral enfeksiyonlarda (örneğin grip) hissedilen yaygın kas ağrıları (miyalji), halsizlik ve kırgınlıktan bizzat Tip I interferonlar sorumludur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Tip I İnterferon Antiviral Savunma Kaskadı",
                [
                    "1. Viral İstilası: Hücre içine giren viral RNA'nın endozomal TLR tarafından tanınması",
                    "2. IFN-Alfa/Beta Sentezi: Plazmasitoid dendritik hücrelerden kana interferon salınması",
                    "3. Antiviral Enzim Aktivasyonu: Komşu hücrelerde protein kinaz R ile viral translasyonun durdurulması",
                    "4. MHC-I Artışı: Enfekte hücrelerin sitotoksik T ve NK hücrelerine hedef gösterilmesi"
                ]
            ),
            make_recall(
                "Viral enfeksiyonlarda komşu hücrelerde antiviral durum oluşturan ve gripteki yaygın kas ağrılarına yol açan Tip I interferonlar hangileridir?",
                "İnterferon-alfa (IFN-α) ve İnterferon-beta'dır (IFN-β).",
                "İki klasik antiviral Tip I interferon üyesi"
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-12-s47",
        "title": "Anti-İnflamatuar Sitokinler: İnterlökin-10 ve TGF-Beta",
        "content": "Kontrolsüz enflamasyonun organizmayı yok etmesini önleyen ve doku yıkımını frenleyen en kritik regülatuvar mediyatörler **Anti-İnflamatuar Sitokinlerdir**. Bu grubun iki kardinal lideri vardır:\n\n- **İnterlökin-10 (IL-10):** Başlıca düzenleyici T hücreleri (Treg), M2 makrofajlar ve B hücreleri tarafından salgılanır. Makrofaj ve dendritik hücrelerin aktivasyonunu doğrudan kapatır; makrofajlardan TNF, IL-1, IL-12 ve kemokin salınımını bloke eder. Antijen sunumunu durdurmak için MHC Sınıf II ve ko-stimülatör B7 (CD80/86) moleküllerinin ekspresyonunu baskılar ('enflamasyonun ana şalterini indirir').\n- **Transforming Growth Factor-beta (TGF-β):** Makrofaj ve lenfosit proliferasyonunu baskılar, endotel aktivasyonunu soğutur. Ancak diğer taraftan fibroblastları şiddetle uyararak ekstraselüler matriks, kollajen sentezi ve skar oluşumunu (fibrozis) yönetir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Pro-İnflamatuar vs Anti-İnflamatuar Sitokinler",
                "Pro-İnflamatuar Sitokinler (TNF, IL-1, IL-6, IFN-γ)",
                "Endoteli aktive eder, lökositleri toplar, doku yıkımı, ateş ve akut faz yanıtı üretir.",
                "Anti-İnflamatuar Sitokinler (IL-10, TGF-β)",
                "Makrofaj aktivasyonunu durdurur, sitokin üretimini keser, immün yanıtı söndürür ve onarım başlatır."
            ),
            make_quiz(
                "Makrofajların TNF ve IL-12 üretimini baskılayan, MHC Sınıf II ekspresyonunu azaltarak enflamasyonu sonlandıran en güçlü endojen anti-inflamatuar sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterlökin-10 (IL-10)", "explanation": "A seçeneği DOĞRUDUR: IL-10 makrofaj fonksiyonlarını ve sitokin sentezini kapatan majör anti-inflamatuar sitokindir."},
                    {"key": "B", "text": "İnterlökin-1 (IL-1)", "explanation": "B seçeneği yanlıştır: Majör pro-inflamatuar sitokindir."},
                    {"key": "C", "text": "Tümör Nekroz Faktörü (TNF)", "explanation": "C seçeneği yanlıştır: Pro-inflamatuardır."},
                    {"key": "D", "text": "İnterferon-gama (IFN-γ)", "explanation": "D seçeneği yanlıştır: M1 makrofaj aktivatörüdür."},
                    {"key": "E", "text": "İnterlökin-17 (IL-17)", "explanation": "E seçeneği yanlıştır: Nötrofilik enflamasyon yapar."}
                ],
                "A"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-12-s48",
        "title": "Kemokinlerin Moleküler Yapısı, 4 Alt Grubu ve Reseptörleri",
        "content": "Kemokinler (kemotaktik sitokinler), 8-10 kDa ağırlığında, lökositlerin hedefe yönelik yönelimini (kemotaksi) yöneten küçük proteinlerdir. Yapılarındaki korunmuş **sistein (C) amino asitlerinin** dizilimine göre 4 ana yapısal alt gruba ayrılırlar:\n\n1. **C-X-C Kemokinler (Alfa Kemokinler):** İlk iki sistein arasında değişken bir amino asit (X) bulunur. Prototipi **IL-8'dir (CXCL8)**. Temel hedefleri **nötrofillerdir**; akut enflamasyonda nötrofilleri çekerler.\n2. **C-C Kemokinler (Beta Kemokinler):** İlk iki sistein yan yanadır. MCP-1 (CCL2), MIP-1α (CCL3), RANTES (CCL5) ve Eotaksin (CCL11) bu gruptadır. Hedefleri **monositler, lenfositler, eozinofiller ve bazofillerdir** (nötrofillere etki etmezler).\n3. **C Kemokinler (Gama Kemokinler):** Yalnızca tek bir sistein kalıntısı taşırlar (Lenfotaktin / XCL1); T ve NK hücrelerini çekerler.\n4. **CX3C Kemokinler (Delta Kemokinler):** İki sistein arasında 3 amino asit bulunur (Fraktalkin / CX3CL1); endotel yüzeyinde tutunarak lökosit adezyonunu doğrudan sağlar.\n\nKemokinler hedef hücrelerdeki 7 transmembranlı G-protein kenetli reseptörlere (CXCR1-6, CCR1-10) bağlanarak etki ederler.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kemokin Grubu", "Yapısal Karakter", "Prototip Molekül", "Majör Hedef Lökosit"],
                [
                    [
                        {"text": "C-X-C (Alfa)", "isMasked": False, "hint": ""},
                        {"text": "Sisteinler arası tek amino asit", "isMasked": True, "hint": "Aralıklı iki sistein"},
                        {"text": "IL-8 (CXCL8)", "isMasked": False, "hint": ""},
                        {"text": "Nötrofiller", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "C-C (Beta)", "isMasked": False, "hint": ""},
                        {"text": "Bitişik iki sistein kalıntısı", "isMasked": True, "hint": "Yan yana iki sistein"},
                        {"text": "MCP-1 (CCL2), Eotaksin", "isMasked": False, "hint": ""},
                        {"text": "Monositler, Eozinofiller, Lenfositler", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "CX3C (Delta)", "isMasked": False, "hint": ""},
                        {"text": "Üç amino asit aralıklı sisteinler", "isMasked": True, "hint": "Üçlü aralık"},
                        {"text": "Fraktalkin (CX3CL1)", "isMasked": False, "hint": ""},
                        {"text": "Monosit ve T hücre adezyonu", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Nötrofilleri spesifik olarak enflamasyon bölgesine çeken C-X-C grubunun prototip kemokini interlökin sekizdir.",
                "interlökin sekizdir",
                "CXCL8 kodlu klasik nötrofil kemoatraktanı"
            )
        ]
    })

    # Slide 49 (CHECKPOINT 5)
    slides.append({
        "id": "k1-12-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Kronik Enflamasyon Sitokinleri ve Kemokin Biyolojisi",
        "content": "Kronik enflamasyon sitokinleri ve kemokinlerin temel prensipleri:\n\n1. **Aks:** Makrofajlar IL-12 salgılar, Th1 hücreleri IFN-γ üretir; IFN-γ makrofajı M1 yaparak döngüyü büyütür.\n2. **M1 vs M2:** M1 (IFN-γ) mikrobisidal NO/ROS üretip doku yıkar; M2 (IL-4, IL-13) TGF-β ve arginaz ile onarım ve fibrozis yapar.\n3. **Th17 ve IL-17:** Kronik dokuya nötrofil ve monosit toplar; psöriyazis ve romatoid artrit patogenezindedir.\n4. **Tip I İnterferonlar:** IFN-α ve IFN-β antiviral savunma kurar, MHC-I artırır, miyalji yapar.\n5. **Anti-enflamatuar Fren:** IL-10 makrofajları kapatır, MHC-II ve TNF'yi baskılar; TGF-β doku onarımı yapar.\n6. **Kemokinler:** C-X-C grubu (IL-8) nötrofilleri çeker; C-C grubu (MCP-1, Eotaksin) monosit ve eozinofilleri toplar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Kemokin alt grupları ve hedef hücreleriyle ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "C-X-C kemokinler (ör. IL-8): Başlıca nötrofilleri çeker.", "explanation": "A seçeneği DOĞRUDUR: C-X-C kemokinler primer olarak nötrofil kemoatraktanlarıdır."},
                    {"key": "B", "text": "C-C kemokinler (ör. MCP-1): Yalnızca eritrositleri çeker.", "explanation": "B seçeneği yanlıştır: Eritrositler kemotaksi yapmaz; monosit ve lenfositleri çeker."},
                    {"key": "C", "text": "İnterlökin-10: Nötrofil üretimini 100 katına çıkarır.", "explanation": "C seçeneği yanlıştır: IL-10 immünsüpresiftir."},
                    {"key": "D", "text": "İnterferon-gama: Makrofaj aktivasyonunu tamamen durdurur.", "explanation": "D seçeneği yanlıştır: M1 makrofaj aktivatörüdür."},
                    {"key": "E", "text": "İnterlökin-17: Virüslerin çoğalmasını doğrudan hızlandırır.", "explanation": "E seçeneği yanlıştır."}
                ],
                "A"
            ),
            make_cloze(
                "Kronik hücresel granülomatöz yanıtta makrofajları epiteloid hücreye dönüstüren ana sitokin interferon-gamadır.",
                "interferon-gamadır",
                "Th1 kaynaklı Tip II interferon"
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-12-s50",
        "title": "İnflamatuar vs Homeostatik Kemokinler: İmmün Trafik ve Lenfoid Mimari",
        "content": "Kemokinler görev aldıkları fizyolojik bağlama göre iki ana fonksiyonel kategoriye ayrılırlar:\n\n1. **İnflamatuar Kemokinler:** Sağlıklı dokularda bazal olarak bulunmazlar. Mikrobiyal ürünler (LPS) veya sitokinler (TNF, IL-1) tarafından hasar anında endotel ve makrofajlarda hızla indüklenirler (örneğin CXCL8 / IL-8, CCL2 / MCP-1). Vasküler endotel yüzeyindeki heparan sülfat proteoglikanlarına bağlanarak yüksek bir 'kemokin gradyenti' oluştururlar. Dolaşımdaki lökositleri damar duvarına bağlar ve doku derinliklerine doğru yönlendirirler.\n2. **Homeostatik (Konstitütif) Kemokinler:** Enflamasyon olmaksızın, sağlıklı dokularda sürekli üretilirler (örneğin CXCL12 / SDF-1, CXCL13, CCL19, CCL21). Görevleri bağışıklık hücrelerinin normal anatomik trafiğini yönetmektir: Kemik iliğinden kök hücre çıkışını, T ve B lenfositlerin dalak ve lenf düğümü kompartımanlarına (T zonu / B folikülü) yerleşmesini ve lenfoid doku mimarisinin korunmasını sağlarlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İnflamatuar ve Homeostatik Kemokinler",
                "İnflamatuar Kemokinler (İndüklenebilir)",
                "Enfeksiyon ve hasarla indüklenir; lökositleri damardan hasarlı doku odağına toplar.",
                "Homeostatik Kemokinler (Konstitütif)",
                "Normal sağlıklı dokularda süreklidir; lenfositlerin lenf nodu ve dalağa yerleşimini organize eder."
            ),
            make_recall(
                "Sağlıklı lenf düğümlerinde T ve B hücrelerinin spesifik anatomik zonlara yerleşmesini sağlayan konstitütif kemokin grubuna ne ad verilir?",
                "Homeostatik kemokinlerdir.",
                "Lenfoid doku trafiğini düzenleyen fizyolojik kemokinler"
            )
        ]
    })

    return slides
