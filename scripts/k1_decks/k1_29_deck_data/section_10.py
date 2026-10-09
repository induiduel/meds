# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 10: Çok Aşamalı Karsinogenez, Klonal Heterojenite ve Hedefe Yönelik Tedaviler (Slayt 91 - 100)
Checkpoint: Slayt 100
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_10_slides():
    return [
        # Slayt 91
        {
            "slideNumber": 91,
            "title": "Çok Aşamalı Karsinogenez ve Vogelstein Kolon Modeli",
            "content": (
                "Karsinogenez tek bir genetik darbenin sonucu değil, on yıllar boyu süren aşamalı bir genetik "
                "ve epigenetik lezyonlar zinciridir. Bu sürecin klasik paradigması Fearon ve Vogelstein tarafından "
                "kolorektal kanser için tanımlanan **adenom-karsinom sekansıdır**. Normal kolon epitelinde ilk "
                "olarak 5q21 lokusundaki **APC tümör baskılayıcı geninin** çift alelik inaktivasyonu gerçekleşir; "
                "bu durum Wnt/beta-katenin yolağını açarak erken adenom (polip) gelişimini başlatır. Ardından "
                "**KRAS onkogen mutasyonu** eklenerek adenom büyür ve displazi derinleşir. Son aşamada 18q "
                "(SMAD4/DCC) kaybı ve nihayet **TP53 inaktivasyonu** ile birlikte invaziv adenokarsinom patlak "
                "verir. Bu model, malignitenin kümülatif mutasyonel eşiğin aşılmasıyla kazanıldığını gösterir."
            ),
            "elements": [
                make_causal_chain(
                    "Vogelstein Kolorektal Adenom-Karsinom Sekansı Basamakları",
                    [
                        "1. APC Gen Kaybı (5q21): Beta-katenin yıkılamaz; epitelde erken adenom (küçük tübüler polip) belirir.",
                        "2. KRAS Aktivasyonu (12p12): Otonom mitojenik sinyalle polip büyür ve villöz ara adenoma ilerler.",
                        "3. 18q Kaybı (SMAD4): TGF-beta büyüme baskılama yolağı felç olur; şiddetli epitelyal displazi gelişir.",
                        "4. TP53 İnaktivasyonu (17p13): Apoptoz tetiği düşer; hücreler genomik kaosla bazal membranı deler.",
                        "5. İnvaziv Karsinom ve Metastaz: Ek telomeraz ve MMP aktivasyonuyla uzak organ metastazları başlar."
                    ]
                ),
                make_cloze(
                    "Kolorektal adenom-karsinom sekansında normal epiteli erken adenoma dönüştüren ilk mutasyonel darbe APC genindedir.",
                    "APC",
                    "Adenomatöz polipozis koli geni"
                )
            ]
        },

        # Slayt 92
        {
            "slideNumber": 92,
            "title": "Sürücü (Driver) Mutasyonlar ve Onkojenik Bağımlılık",
            "content": (
                "Bir tümör genomunda yüzlerce hatta binlerce nükleotid değişikliği bulunsa da, bu mutasyonların "
                "yalnızca çok küçük bir azınlığı karsinogenezi doğrudan yönetir. **Sürücü (driver) mutasyonlar**, "
                "kanser hücresine doğrudan büyüme, proliferasyon ve sağkalım avantajı kazandıran, pozitif klonal "
                "seleksiyona uğrayan mutasyonlardır (örneğin EGFR, KRAS, BRAF V600E). Sürücü mutasyonlar kanser "
                "hücresinde **onkojenik bağımlılık (oncogene addiction)** adı verilen olağanüstü bir biyolojik zafiyet "
                "yaratır. Kanser hücresi genomik karmaşasına rağmen hayatta kalabilmek için o tek sürücü onkoproteinin "
                "sağladığı sinyale bağımlı hale gelir; bu tek molekül spesifik bir inhibitörle bloke edildiğinde tüm "
                "tümör hücresi domino taşı gibi hızla apoptoza çöker."
            ),
            "elements": [
                make_table(
                    "Sürücü (Driver) vs Yolcu (Passenger) Mutasyon Özellikleri",
                    ["Parametre", "Sürücü (Driver) Mutasyon", "Yolcu (Passenger) Mutasyon"],
                    [
                        {
                            "cells": ["Karsinogeneze Katkı", "Doğrudan malign fenotip kazandırır", "Fenotipik avantaj sağlamaz (Nötr birikim)"],
                            "hiddenIndex": 1,
                            "hint": "Habis dönüşümü primer tetikleyen güç"
                        },
                        {
                            "cells": ["Terapötik Değer", "Hedefe yönelik akıllı ilaçların birincil hedefidir", "Doğrudan ilaç hedefi oluşturmaz"],
                            "hiddenIndex": 1,
                            "hint": "Hedefli moleküler tedavilerin bağlanma odağı"
                        },
                        {
                            "cells": ["Klondaki Temsil", "Klonun neredeyse tüm hücrelerinde sabittir", "Subklonlar arasında değişken dağılım gösterir"],
                            "hiddenIndex": 1,
                            "hint": "Tümör kitlesinin geneline yayılmış kalıcılık"
                        }
                    ]
                ),
                make_active_recall(
                    "Kanser hücrelerinin karmaşık genomik yapısına rağmen hayatta kalmak için tek bir sürücü onkogenin sinyaline muhtaç olması olgusuna ne ad verilir?",
                    "Onkojenik bağımlılık (Oncogene addiction) adı verilir.",
                    "Tek bir büyüme sinyaline esir olma hali"
                )
            ]
        },

        # Slayt 93
        {
            "slideNumber": 93,
            "title": "Yolcu (Passenger) Mutasyonlar ve Mutasyonel İmzalar",
            "content": (
                "**Yolcu (passenger) mutasyonlar**, neoplastik transformasyona ve büyüme kinetiğine doğrudan katkı "
                "sağlamayan, genomik kararsızlık ve hücre bölünmeleri sırasında rastlantısal olarak genoma yazılan "
                "nötr genetik değişikliklerdir. Sayıca sürücü mutasyonlardan katbekat fazladırlar (genomdaki "
                "mutasyonların %99'u passenger niteliktedir). Ancak yolcu mutasyonlar onkolojide devasa bir bilgi "
                "hazinesidir: Bir tümörün genomundaki yolcu mutasyonların nükleotid değişim tipleri (transisyon/transversiyon) "
                "ve komşu baz dizilimleri matematiksel olarak dekonvolüe edildiğinde **spesifik mutasyonel imzalar "
                "(COSMIC mutational signatures)** elde edilir. Bu imzalar, hastanın hangi karsinojene maruz kalarak "
                "kanser geliştirdiğini (ör. İmza 4 = tütün dumanı; İmza 7 = ultraviyole ışık; İmza 2/13 = APOBEC sitidin "
                "deaminaz aktivitesi) ele veren moleküler bir arkeolojik parmak izidir."
            ),
            "elements": [
                make_before_after(
                    "Sürücü Mutasyonun Rolü vs Mutasyonel İmzanın Görevi",
                    "Sürücü (Driver) Mutasyonlar",
                    "Tedavi hedefini belirler (Ör. BRAF V600E saptandı, dabrafenib başla). Etiyolojik geçmiş hakkında bilgi vermez.",
                    "Yolcu Mutasyonel İmzaları (Signatures)",
                    "Kanserin geçmiş etiyolojisini ele verir (Ör. Tütün transversiyonu, UV pirimidin imzası, defektif MMR imzası).",
                    "Mutasyonel imzalar adli tıp ve koruyucu halk sağlığında karsinojenik etkenleri kesin olarak aydınlatır."
                ),
                make_cloze(
                    "Tümör genomundaki yolcu mutasyonların örüntüsünden yola çıkarak etiyolojik karsinojeni belirleyen moleküler parmak izine mutasyonel imza denir.",
                    "imza",
                    "Etiyolojik nedenin moleküler parmak izi"
                )
            ]
        },

        # Slayt 94
        {
            "slideNumber": 94,
            "title": "Klonal Heterojenite ve Dallanan Evrim",
            "content": (
                "Tümörler başlangıçta tek bir transforme atasal kök hücreden monoklonal olarak çıksa da, büyüme "
                "sürecinde çizgisel (lineer) değil, **dallanan (branching) bir Darwinyen evrim** sergilerler. Hücreler "
                "çoğaldıkça genomik istikrarsızlık nedeniyle her alt grupta farklı yeni mutasyonlar türer; sonuçta "
                "aynı tümör kitlesi içerisinde genetik ve epigenetik olarak birbirinden farklı onlarca **subklon** "
                "ortaya çıkar (**intratümöral heterojenite**). Primer tümörün merkezindeki bir hücre ile invaziv "
                "kenarındaki bir hücre veya karaciğer metastazındaki bir hücre tamamen farklı mutasyon profilleri "
                "taşıyabilir. Bu durum, tek bir iğne biyopsisinin tüm tümör kitlesini temsil edememesine ve heterojen "
                "tedavi yanıtlarına yol açan en büyük onkolojik engeldir."
            ),
            "elements": [
                make_table(
                    "Tümör İçi (İntratümöral) Heterojenite Düzeyleri",
                    ["Heterojenite Düzeyi", "Biyolojik Tanım", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Uzamsal (Spatial) Heterojenite", "Aynı tümör kitlesinin farklı bölgeleri arası genetik fark", "Tek bir biyopsinin tümörü temsil edememesi"],
                            "hiddenIndex": 2,
                            "hint": "Örnekleme hatası ve biyopsi yetersizliği"
                        },
                        {
                            "cells": ["Zamansal (Temporal) Heterojenite", "Primer tümör ile yıllar sonraki nüks/metastaz arası fark", "Tedavi sonrası genetik profilin baştan değişmesi"],
                            "hiddenIndex": 2,
                            "hint": "Zaman içinde dirençli subklonların belirmesi"
                        }
                    ]
                ),
                make_active_recall(
                    "Tek bir tümör kitlesi içinde genetik ve biyolojik özellikleri farklı alt hücre gruplarının bir arada bulunmasına ne ad verilir?",
                    "İntratümöral klonal heterojenite adı verilir.",
                    "Tümör içi alt grup çeşitliliği"
                )
            ]
        },

        # Slayt 95
        {
            "slideNumber": 95,
            "title": "Terapötik Seleksiyon Baskısı ve Edinsel Direnç",
            "content": (
                "Tümör klonal heterojenitesi, kanser tedavisinde kaçınılmaz olarak **tedavi direncinin (edinsel "
                "rezistans)** gelişmesine neden olur. Bir tümör hastasına kemoterapi veya hedefe yönelik akıllı "
                "ilaç verildiğinde, bu tedavi tümör mikroçevresinde güçlü bir **Darwinyen seleksiyon baskısı** "
                "yaratır. Tedaviye duyarlı olan baskın klonlar hızla ölür ve tümör kitlesi küçülerek remisyona "
                "girer. Ancak heterojenite nedeniyle önceden kitle içinde %0.1 oranında mevcut olan dirençli bir "
                "minör subklon (örneğin EGFR inhibitörüne dirençli T790M mutant hücreler) ilaçtan etkilenmez. "
                "Duyarlı hücreler temizlenip rekabet ortamı ortadan kalkınca, bu dirençli subklon hızla çoğalarak "
                "boşalan alanı doldurur; sonuçta tedaviye tamamen dirençli agresif bir nüks patlak verir."
            ),
            "elements": [
                make_causal_chain(
                    "Terapötik Seleksiyon ve Edinsel Tedavi Direnci Kaskadı",
                    [
                        "1. Pre-Mevcut Heterojenite: Tümör kitlesinde ilaca dirençli minör bir subklon gizlice mevcuttur.",
                        "2. Terapötik Baskı: Hedefe yönelik ilaç duyarlı baskın hücreleri apoptoza sürükleyerek kitleyi küçültür.",
                        "3. Alan Açılması: Duyarlı hücrelerin ölümü dirençli subklon üzerindeki kaynak rekabetini kaldırır.",
                        "4. Dirençli Klon Klonal Genişlemesi: Dirençli mutant hücreler monoklonal olarak kontrolsüz çoğalmaya başlar.",
                        "5. Refrakter Nüks: Hasta ilaca tamamen yanıtsız agresif sekonder metastazlarla yeniden kliniğe gelir."
                    ]
                ),
                make_cloze(
                    "Hedefe yönelik tedaviler altında duyarlı hücrelerin ölüp dirençli minör hücrelerin çoğalması Darwinyen seleksiyon baskısı ile gerçekleşir.",
                    "seleksiyon",
                    "Doğal ayıklanma ve seçilim terimi"
                )
            ]
        },

        # Slayt 96
        {
            "slideNumber": 96,
            "title": "Moleküler Hedefe Yönelik Tedaviler: TKI Başarıları",
            "content": (
                "Karsinogenezin moleküler temelinin çözülmesi, kanser kemoterapisini kör sitotoksik zehirlerden "
                "seçici akıllı ilaç çağına taşımıştır. Bu devrimin öncüleri küçük moleküllü **Tirozin Kinaz "
                "İnhibitörleridir (TKI)**. Akciğer adenokarsinomunda **EGFR kinaz mutasyonu** (ekzon 19 delesyonu, "
                "L858R) taşıyan hastalarda **Osimertinib, Erlotinib**; **ALK veya ROS1 translokasyonu** taşıyanlarda "
                "**Krizotinib, Alektinib**; metastatik malign melanomda **BRAF V600E mutasyonu** saptandığında "
                "**Vemurafenib, Dabrafenib (MEK inhibitörü Trametinib ile kombine)**; GİST tümörlerinde **c-KIT "
                "mutasyonunda İmatinib** hastalara kür veya uzun süreli sağkalım sunar. Patolog, rezeksiyon materyalinde "
                "bu moleküler hedefleri saptamadan hastaya sistemik tedavi başlanamaz."
            ),
            "elements": [
                make_table(
                    "Klinik Pratikte Majör Hedefe Yönelik Tedavi Çiftleri",
                    ["Malignite Tipi", "Sürücü Moleküler Hedef", "Hedefe Yönelik Akıllı İlaç Sınıfı"],
                    [
                        {
                            "cells": ["Akciğer Adenokarsinomu", "EGFR ekzon 19 delesyonu / L858R", "Osimertinib, Erlotinib (EGFR-TKI)"],
                            "hiddenIndex": 2,
                            "hint": "Epidermal reseptör kinaz blokerleri"
                        },
                        {
                            "cells": ["Malign Melanom", "BRAF V600E nokta mutasyonu", "Dabrafenib + Trametinib (BRAF/MEK inhibitörü)"],
                            "hiddenIndex": 2,
                            "hint": "Raf kinaz ve downstream kaskad inhibitörleri"
                        },
                        {
                            "cells": ["Gastrointestinal Stromal Tümör (GİST)", "c-KIT (CD117) veya PDGFRA mutasyonu", "İmatinib (Tirozin kinaz inhibitörü)"],
                            "hiddenIndex": 2,
                            "hint": "Kit reseptörü bloke edici öncü ilaç"
                        }
                    ]
                ),
                make_active_recall(
                    "Metastatik malign melanom olgularının yaklaşık yarısında saptanan ve Vemurafenib/Dabrafenib ile hedeflenen sürücü kinaz mutasyonu hangisidir?",
                    "BRAF V600E mutasyonudur.",
                    "Altı yüzüncü valin glutamat mutasyonu"
                )
            ]
        },

        # Slayt 97
        {
            "slideNumber": 97,
            "title": "İmmün Kontrol Noktaları: PD-1 / PD-L1 ve CTLA-4",
            "content": (
                "Normal fizyolojide bağışıklık sistemi, otoimmün doku hasarını engellemek için T hücre aktivasyonunu "
                "sınırlayan negatif fren sistemlerine sahiptir; bunlara **immün kontrol noktaları (immune checkpoints)** "
                "denir. Karsinogenezde tümör hücreleri bu fizyolojik kontrol mekanizmalarını istismar ederek konak "
                "immün gözetiminden kaçarlar. **CTLA-4**, lenf nodunda T hücresinin ilk antijen tanıma evresinde "
                "CD28 ile yarışarak kostimülasyonu keser ve T hücresini uykuda tutar. **PD-1 (Programmed Death 1)** "
                "ise periferik dokularda ve tümör yatağında efektör T hücrelerinde eksprese edilen bir ölüm reseptörüdür. "
                "Tümör hücreleri yüzeylerinde **PD-L1** eksprese ederek PD-1'e bağlanır; T lenfosit içine tirozin "
                "fosfataz (SHP-2) sinyali göndererek TCR aktivasyonunu sıfırlar ve lenfositi anarjik hale sokar."
            ),
            "elements": [
                make_before_after(
                    "CTLA-4 vs PD-1 İmmün Kontrol Noktalarının Farkı",
                    "CTLA-4 Yolağı (Erken / Santral Fren)",
                    "Lenf nodunda T hücresinin ilk uyarılma anında etki eder. Dendritik hücrenin B7 ligandına bağlanarak CD28 kostimülasyonunu engeller.",
                    "PD-1 / PD-L1 Yolağı (Geç / Periferik Fren)",
                    "Tümör dokusunda efektör sitotoksik T hücresi üzerinde etki eder. Tümör hücresinin PD-L1 ligasyonuyla lenfositi anarjik kılar.",
                    "Anti-CTLA-4 genel T hücresi cevabını ateşlerken, Anti-PD-1 tümör yatağındaki lenfositleri seçici uyandırır."
                ),
                make_cloze(
                    "Tümör yatağındaki sitotoksik T lenfositlerin PD-1 reseptörüne bağlanarak lenfositi anerjiye sokan yüzey molekülü PD-L1'dir.",
                    "PD-L1'dir",
                    "Programlı ölüm yüzey ligandı"
                )
            ]
        },

        # Slayt 98
        {
            "slideNumber": 98,
            "title": "İmmünoterapi ve Öngörücü Biyobelirteçler",
            "content": (
                "İmmün kontrol noktası inhibitörleri (ICI: **Pembrolizumab, Nivolumab, Atezolizumab, İpilimumab**), "
                "PD-1, PD-L1 veya CTLA-4'ü monoklonal antikorlarla kapatarak hastanın kendi T hücrelerini tümöre "
                "karşı serbest bırakır. Ancak bu devrimsel tedavi her hastada eşit çalışmaz ve bağışıklık ilişkili "
                "ağır otoimmün toksisiteler (kolit, hipofizit, pnömonit) yapabilir. Bu nedenle patologlar tedavi "
                "öncesinde üç majör **öngörücü (prediktif) biyobelirteci** değerlendirirler: 1) **PD-L1 İmmünohistokimyası**: "
                "Tümör Hücre Skoru (TPS) veya Birleşik Pozitiflik Skoru (CPS) ile membranöz PD-L1 oranı hesaplanır. "
                "2) **Mikrosatellit İnstabilitesi (MSI-H / dMMR)**: Tümörden bağımsız evrensel immünoterapi göstergesidir. "
                "3) **Tümör Mutasyon Yükü (TMB-High, >10 mutasyon/Mb)**: Yüksek TMB bol neoantijen ve güçlü T hücre yanıtı demektir."
            ),
            "elements": [
                make_table(
                    "İmmünoterapi Başarısını Öngören Üç Majör Biyobelirteç",
                    ["Biyobelirteç", "Laboratuvar Tayin Yöntemi", "Pozitiflik Kriteri", "Klinik Tedavi Anlamı"],
                    [
                        {
                            "cells": ["PD-L1 Ekspresyonu", "İmmünohistokimya (İHK)", "TPS >= %50 veya CPS >= 10", "Anti-PD-1 monoterapi endikasyonu"],
                            "hiddenIndex": 2,
                            "hint": "Yüksek yüzdelik membranöz boyanma skoru"
                        },
                        {
                            "cells": ["MSI-High / dMMR", "İHK veya PCR / NGS", "En az 2 mikrosatellit instabilitesi", "Tümör agnostik Pembrolizumab onayı"],
                            "hiddenIndex": 2,
                            "hint": "Tümör tipinden bağımsız kullanım onay kriteri"
                        },
                        {
                            "cells": ["Tümör Mutasyon Yükü (TMB)", "Yeni Nesil Dizileme (NGS)", ">= 10 mutasyon / Megabaz", "Yüksek neoantijen yükü ile güçlü yanıt"],
                            "hiddenIndex": 2,
                            "hint": "Milyon baz başına çift haneli nükleotid hasarı eşiği"
                        }
                    ]
                ),
                make_active_recall(
                    "İmmün kontrol noktası inhibitörlerine yanıtı öngörmede doku patolojisinde tümör ve inflamatuar hücrelerde hesaplanan kombine skorlama sistemine ne ad verilir?",
                    "Birleşik Pozitiflik Skoru (Combined Positive Score - CPS) adı verilir.",
                    "Tümör ve lökosit boyanma oranı bileşkesi"
                )
            ]
        },

        # Slayt 99
        {
            "slideNumber": 99,
            "title": "Sıvı Biyopsi ve Dolaşan Tümör DNA'sı (ctDNA)",
            "content": (
                "Kanser takibinde ve moleküler profillemede en ileri teknolojik aşama **sıvı biyopsidir (liquid "
                "biopsy)**. Katı tümör dokusundan apoptoz ve nekroz sonucu dolaşım kanına dökülen serbest DNA "
                "parçacıklarına **dolaşan tümör DNA'sı (circulating tumor DNA - ctDNA)** denir. Basit bir venöz "
                "kan örneğinden yüksek duyarlıklı dijital PCR veya ultra-derin NGS yöntemleriyle ctDNA analizi "
                "yapılarak invaziv doku biyopsisine gerek kalmadan sürücü mutasyonlar saptanabilir. Sıvı biyopsi "
                "üç kritik avantaj sağlar: 1) İntratümöral heterojeniteyi tek bir biyopsiden çok daha kapsamlı "
                "temsil eder; 2) Tedavi sırasında kanda direnç mutasyonlarının (ör. EGFR T790M) belirişini aylar "
                "önceden yakalar; 3) Ameliyat sonrası kanda gözle veya radyolojiyle görülemeyen **Minimal Rezidüel "
                "Hastalığı (MRD)** saptayarak relapsı önceden haber verir."
            ),
            "elements": [
                make_before_after(
                    "Konvansiyonel Doku Biyopsisi vs Sıvı Biyopsi (ctDNA)",
                    "Konvansiyonel İğne Biyopsisi",
                    "İnvazivdir, risk taşır; yalnızca girdiği tek bir odaktan örnek alır, intratümöral heterojeniteyi ve metastazları kaçırabilir.",
                    "Sıvı Biyopsi (Periferik Kan ctDNA)",
                    "Non-invazivdir; vücuttaki tüm tümör odaklarından kana dökülen mutasyonları yansıtır, seri olarak tekrarlanabilir.",
                    "Sıvı biyopsi gelecekte erken kanser taraması ve nüksün aylar önce öngörülmesinde standart olacaktır."
                ),
                make_cloze(
                    "Tümör hücrelerinin ölümüyle periferik kan plazmasına dökülen serbest neoplastik nükleik asit parçacıklarına ctDNA adı verilir.",
                    "ctDNA",
                    "Dolaşan serbest tümör DNA kısaltması"
                )
            ]
        },

        # Slayt 100: CHECKPOINT 10
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Çok Aşamalı Karsinogenez ve Hedefe Yönelik Tedaviler",
            "content": (
                "Karsinojenezin Moleküler Temeli dersinin bu son bölümünde, kanser evrimi ve modern onkolojik "
                "tedavi stratejileri sentezlenmektedir. Karsinogenez Fearon-Vogelstein modelinde olduğu gibi "
                "aşama aşama (APC → KRAS → TP53) gelişir. Sürücü (driver) mutasyonlar kanser hücresine onkojenik "
                "bağımlılık kazandırırken; yolcu (passenger) mutasyonlar etiyolojik mutasyonel imzaları ele verir. "
                "Dallanan Darwinyen evrim intratümöral heterojenite yaratır; bu heterojenite ilaç baskısı altında "
                "dirençli subklonların seçilmesine yol açar. TKI'lar (Osimertinib, Vemurafenib) sürücü kinazları "
                "bloke ederken; immün kontrol noktası inhibitörleri (Anti-PD-1, CTLA-4) lenfosit frenlerini kaldırır "
                "ve yüksek TMB/MSI olgularında küratif yanıtlar sağlar. Sıvı biyopsi (ctDNA) ise minimal rezidüel "
                "hastalığı aydınlatır."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp10-fc01",
                    "front": "Vogelstein kolorektal karsinogenez sekansında normal kolon epitelini erken adenom zeminine sokan ilk mutasyonel darbe hangi gendedir?",
                    "back": "APC tümör baskılayıcı genindedir.",
                    "hint": "Adenomatöz polipozis koli geni"
                },
                {
                    "id": "k1-29-cp10-fc02",
                    "front": "Tümör hücrelerinin sitotoksik CD8+ T lenfositleri periferik dokuda ve tümör yatağında susturmak için kullandığı immün kontrol noktası ekseni nedir?",
                    "back": "PD-1 / PD-L1 kontrol noktası eksenidir.",
                    "hint": "Programlanmış ölüm reseptör ve ligand sistemi"
                },
                {
                    "id": "k1-29-cp10-fc03",
                    "front": "Tümör dokusundan kana dökülen, kanda minimal rezidüel hastalığı ve ilaç direnç mutasyonlarını saptayan serbest nükleik asitlere ne ad verilir?",
                    "back": "Dolaşan tümör DNA'sı (ctDNA) adı verilir.",
                    "hint": "Sıvı biyopsi analizinin serbest plazma hedefi"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 10 Özet Tablosu: Moleküler Onkoloji Sentezi",
                    ["Kavram / Teknoloji", "Biyolojik Mekanizma", "Klinik Uygulama"],
                    [
                        {
                            "cells": ["Onkojenik Bağımlılık", "Tek sürücü mutasyona hayati muhtaçlık", "Hedefe yönelik kinaz inhibitörleri (TKI)"],
                            "hiddenIndex": 0,
                            "hint": "Tek büyüme molekülüne muhtaçlık zafiyeti"
                        },
                        {
                            "cells": ["İmmün Kontrol Noktası", "PD-1 / PD-L1 ile T hücresi anerjisi", "Pembrolizumab ve Nivolumab ile immünoterapi"],
                            "hiddenIndex": 0,
                            "hint": "Bağışıklık freni blokajı ile tedavi"
                        }
                    ]
                )
            ]
        }
    ]
