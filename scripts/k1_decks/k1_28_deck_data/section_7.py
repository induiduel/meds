# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 7: Displazi, Karsinoma In Situ ve İnvazyon (Slayt 61 - 70)
Checkpoint: Slayt 69
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_7_slides():
    return [
        # Slayt 61
        {
            "slideNumber": 61,
            "title": "Displazi Kavramı: Düzensiz Epitelyal Proliferasyon",
            "content": (
                "Displazi, kelime anlamı olarak 'bozuk veya düzensiz büyüme' demektir ve hemen hemen daima epitelyal "
                "doku tabakalarında görülen premalign bir lezyondur. Displazik epitelde hücrelerin normal olgunlaşma "
                "ve sıralanma hiyerarşisi bozulur; mimari polarite kaybolur. Normalde yalnızca bazal tabakada görülmesi "
                "gereken mitotik figürler epitelin orta ve yüzeyel katlarında da izlenmeye başlar. Hücrelerde pleomorfizm, "
                "hiperkromazi ve nükleus-sitoplazma oranında artış gibi sitolojik atipi bulguları ortaya çıkar. Ancak "
                "buradaki en temel kural şudur: 'Displazi kanser ile eş anlamlı değildir'. Displazi epitel içinde sınırlıdır "
                "ve bazal membranı kesinlikle delip geçmez."
            ),
            "elements": [
                make_cloze(
                    "Epitel tabakasında hücresel atipi ve polarite kaybıyla giden düzensiz proliferasyona displazi adı verilir.",
                    "displazi",
                    "Bozuk epitel büyümesi terimi"
                ),
                make_active_recall(
                    "Displazik bir epitelin henüz kanser olmadığını kanıtlayan en temel histopatolojik sınır nedir?",
                    "Bazal membranın tamamen sağlam olması ve alttaki stromaya hiçbir invazyonun bulunmamasıdır.",
                    "İntakt epitel altı tabaka"
                )
            ]
        },
        # Slayt 62
        {
            "slideNumber": 62,
            "title": "Displazinin Derecelendirilmesi: Hafif, Orta ve Şiddetli",
            "content": (
                "Displazik değişiklikler, epitelyal tabakanın dikey kalınlığının ne kadarını tuttuğuna göre üç histopatolojik "
                "dereceye ayrılır. En klasik model servikal intraepitelyal neoplazidir (CIN): 'Hafif displazi' (CIN 1), "
                "atipik ve hiperkromatik hücrelerin epitel kalınlığının yalnızca alt üçte birinde (1/3) sınırlı kaldığı "
                "ve yüzeyel katlarda olgunlaşmanın korunduğu durumdur. 'Orta displazi'de (CIN 2) atipi epitelin alt üçte ikisine "
                "(2/3) kadar yükselir. 'Şiddetli displazi'de (CIN 3) ise atipik hücreler epitel kalınlığının üçte ikisinden "
                "fazlasını istila eder; yüzeye doğru hücre olgunlaşması neredeyse tamamen çöker."
            ),
            "elements": [
                make_table(
                    "Displazi Derecelendirme Kriterleri (CIN Modeli)",
                    ["Displazi Derecesi", "Epitel Kalınlığı Tutulumu", "Kanserleşme Riski", "Klinik Seyir"],
                    [
                        {
                            "cells": ["Hafif Displazi (CIN 1)", "Epitelin alt 1/3 tabakası", "Çok düşük (<%1)", "Büyük oranda kendiliğinden geriler (%60)"],
                            "hiddenIndex": 3,
                            "hint": "Spontan iyileşme oranı yüksek"
                        },
                        {
                            "cells": ["Orta Displazi (CIN 2)", "Epitelin alt 2/3 tabakası", "Orta (~%5)", "Tedavi veya yakın takip gerektirir"],
                            "hiddenIndex": 1,
                            "hint": "İki bölü üç tutulum sınırı"
                        },
                        {
                            "cells": ["Şiddetli Displazi (CIN 3)", "Epitelin 2/3'sinden fazlası", "Yüksek (>%12)", "Cerrahi ablasyon/eksizyon şarttır"],
                            "hiddenIndex": 1,
                            "hint": "Tüm katlara yakın tutulum"
                        }
                    ]
                ),
                make_active_recall(
                    "Hafif displazide (CIN 1) atipik hücrelerin epitel içinde tuttuğu dikey kalınlık sınırı nedir?",
                    "Epitel kalınlığının alt üçte bir (1/3) bölümüdür.",
                    "Alt tabaka kalınlık oranı"
                )
            ]
        },
        # Slayt 63
        {
            "slideNumber": 63,
            "title": "Displazi vs Kanser: Geri Dönüşümlülük (Reversibilite)",
            "content": (
                "Kanser hücreleri otonomdur ve mutasyonel geri dönüş yeteneği yoktur; tedavi edilmezse sürekli ilerler. "
                "Buna karşılık displazi, özellikle hafif ve orta dereceli formlarında, 'potansiyel olarak geri dönüşümlü' "
                "(reversibl) bir süreçtir. Eğer displaziyi başlatan kronik etken (örneğin sigara dumanı, kronik enfeksiyon "
                "veya mekanik irritasyon) ortadan kaldırılırsa, epiteldeki displazik değişiklikler haftalar veya aylar "
                "içinde tamamen gerileyerek doku eski normal histolojik yapısına dönebilir. Ancak etken devam ederse veya "
                "displazi şiddetli dereceye (CIN 3) ulaşırsa, geri dönüş olasılığı dramatik biçimde düşer ve lezyon hızla "
                "invaziv karsinoma ilerleme rotasına girer."
            ),
            "elements": [
                make_before_after(
                    "Displazi vs İnvaziv Kanser Davranışı",
                    "Displazi (Premalign)",
                    "Uyaran kalktığında gerileyebilir (reversibl), bazal membran sağlamdır, lenfovasküler metastaz riski sıfırdır.",
                    "İnvaziv Kanser (Malign)",
                    "Uyaran kalksa dahi otonom çoğalır (irreversibl), bazal membranı deler, stromayı istila eder ve metastaz yapar.",
                    "Hafif displazide cerrahi yerine altta yatan nedenin tedavisi ve takip önceliklidir."
                ),
                make_cloze(
                    "Tetikleyici karsinojen etken uzaklaştırıldığında displazinin tamamen gerileyebilme özelliğine reversibilite adı verilir.",
                    "reversibilite",
                    "Geri dönebilirlik niteliği"
                )
            ]
        },
        # Slayt 64
        {
            "slideNumber": 64,
            "title": "Karsinoma In Situ (CIS): Preinvaziv Zirve Noktası",
            "content": (
                "Karsinoma in situ (CIS), malign sitolojik atipinin epitelin 'tüm kalınlığını' (tabandan en yüzeyel tabakaya kadar) "
                "tamamen kapladığı, ancak 'bazal membranın henüz delinmediği' preinvaziv kanser evresidir. Mikroskop altında "
                "bakıldığında hücreler sitolojik olarak tam bir invaziv karsinom görünümündedir; aşırı pleomorfik, hiperkromatik "
                "ve bol atipik mitozludurlar. Ancak neoplastik hücreler bazal membranın üzerinde hapis durumdadır; alttaki stromaya "
                "hiçbir tümör hücresi geçmemiştir. Stroma intakt olduğu için neoplastik hücreler ne kan ne de lenf damarlarına "
                "ulaşamaz; bu nedenle karsinoma in situ evresinde metastaz riski teorik ve pratik olarak kesinlikle 'sıfır'dır."
            ),
            "elements": [
                make_table(
                    "Karsinoma In Situ (CIS) Temel Kriterleri",
                    ["Kriter", "Histopatolojik Durum", "Klinik ve Biyolojik Anlamı"],
                    [
                        {
                            "cells": ["Epitel Tutulumu", "Tüm kalınlık (%100)", "Tam kat sitolojik malignite"],
                            "hiddenIndex": 1,
                            "hint": "Epitelin tüm katmanları"
                        },
                        {
                            "cells": ["Bazal Membran", "Kesinlikle Sağlam ve İntakt", "Stromaya geçiş yoktur"],
                            "hiddenIndex": 1,
                            "hint": "Delinmemiş koruyucu bazal zar"
                        },
                        {
                            "cells": ["Metastaz Olasılığı", "Tamamen Sıfır (%0)", "Damarlarla temas olmadığı için metastaz imkansızdır"],
                            "hiddenIndex": 1,
                            "hint": "Uzak yayılım olasılığı yokluğu"
                        }
                    ]
                ),
                make_active_recall(
                    "Karsinoma in situ lezyonlarında metastaz olasılığının kesin olarak sıfır olmasının anatomik nedeni nedir?",
                    "Tümörün bazal membranı aşamayarak stromadaki kan ve lenf damarlarıyla hiçbir temas kuramamasıdır.",
                    "Damarsal ağ ile bağlantısızlık"
                )
            ]
        },
        # Slayt 65
        {
            "slideNumber": 65,
            "title": "İnvaziv Karsinoma Geçiş: Bazal Membranın Yıkımı",
            "content": (
                "Karsinoma in situ'nun gerçek bir 'invaziv karsinoma' dönüşmesi, epitelin altında uzanan tip IV kolajenden "
                "ve lamininden zengin 'bazal membranın' proteolitik olarak delinmesiyle başlar. Kanser hücreleri bu aşamada "
                "yoğun miktarda matriks metalloproteinazlar (MMP), özellikle 'Tip IV kollejenazlar' (MMP-2 ve MMP-9) salgılarlar. "
                "MMP'ler bazal membranın kolajen ağını eriterek delikler açar. Bazal membranı aşan tümör hücreleri konakçı "
                "bağ dokusu stromasıyla doğrudan temas haline geçer; burada anjiyogenezi tetikler, lenfatik yarıklara sızar "
                "ve artık gerçek bir metastatik potansiyel kazanmış olur."
            ),
            "elements": [
                make_causal_chain(
                    "In Situ'dan İnvaziv Karsinoma Geçişin Proteolitik Yolu",
                    [
                        "1. Preinvaziv Durum: Tümör hücrelerinin bazal membran üzerinde tam kat birikmesi (CIS)",
                        "2. Enzim Salgılanması: Kanser hücrelerinden Tip IV kollejenaz (MMP-2/MMP-9) salgılanması",
                        "3. Membran Yıkımı: Bazal zardaki tip IV kolajen ve laminin ağının enzimatik parçalanması",
                        "4. Stromal Giriş: Tümör hücrelerinin subepitelyal gevşek bağ dokusuna sızması (mikroinvazyon)",
                        "5. İnvaziv Kanser: Stromadaki kapiller ve lenfatik kanallarla temas kurularak sistemik yayılım yolunun açılması"
                    ]
                ),
                make_cloze(
                    "Kanser hücrelerinin bazal membranı eriterek stromaya geçmesini sağlayan ana enzimler Tip IV kollejenaz metalloproteinazlarıdır.",
                    "Tip IV kollejenaz",
                    "MMP-2 ve MMP-9 enzimleri"
                )
            ]
        },
        # Slayt 66
        {
            "slideNumber": 66,
            "title": "İnvazyon Basamakları: E-Kaderin Kaybı ve Ayrılma",
            "content": (
                "Tümör hücrelerinin komşu hücrelerden ayrılarak çevre dokulara ilerlemesi dört sıralı biyolojik basamakta "
                "gerçekleşir: Birinci basamak 'tümör hücrelerinin birbirine tutunmasını sağlayan hücreler arası bağlantıların "
                "çözülmesidir'. Normal epitel hücreleri birbirlerine 'E-kaderin' glikoproteinleri ve katenin kompleksleri "
                "ile kuvvetle kenetlenmiştir. Karsinom hücrelerinde E-kaderin geninin mutasyonla inaktive olması veya "
                "epigenetik susturulması sonucu bu bağlantılar kopar; neoplastik hücreler epitelyal kümeden tek tek koparak "
                "bağımsız amoboid hareket yeteneği kazanırlar. E-kaderin kaybı, invazyonun ilk ve zorunlu moleküler anahtarıdır."
            ),
            "elements": [
                make_before_after(
                    "E-Kaderin Varlığı vs Kaybının Biyolojik Etkisi",
                    "İntakt E-Kaderin Ekspresyonu",
                    "Hücreler sıkıca birbirine yapışıktır, epitel bütünlüğü korunur, tek tek ayrılıp stromaya sızamazlar.",
                    "E-Kaderin Kaybı / İnaktivasyonu",
                    "Hücreler arası yapışma sıfırlanır; hücreler birbirini bırakarak bağımsız hareketli invaziv hücrelere dönüşür.",
                    "E-kaderin kaybı meme lobüler karsinomu ve diffüz mide karsinomunun (taşlı yüzük) patognomonik defektidir."
                ),
                make_active_recall(
                    "Karsinom hücrelerinin birbirine tutunmasını sağlayan ve invazyonun ilk basamağında inaktive olan hücreler arası adezyon molekülü nedir?",
                    "E-kaderin (E-cadherin) molekülüdür.",
                    "Kalsiyum bağımlı epitelyal bağlantı proteini"
                )
            ]
        },
        # Slayt 67
        {
            "slideNumber": 67,
            "title": "Amoboid Hareket ve Ekstraselüler Matriks Bozulması",
            "content": (
                "E-kaderin bağlarını koparan ve bazal membranı delen tümör hücreleri, ekstraselüler matriks (ECM) içinde "
                "ilerlemek için 'lokomosyon' (amoboid hareket) yeteneği geliştirir. Tümör hücrelerinin yüzeyindeki 'integrin' "
                "reseptörleri stromadaki fibronektin, laminin ve kolajen liflerine dinamik olarak tutunur. Hücre ön ucundan "
                "aktin polimerizasyonu ile 'psödopodlar' (yalancı ayaklar) uzatarak matriks liflerine yapışır; ardından "
                "arkadaki temas noktalarını proteazlarla eriterek tüm hücre gövdesini aktin-miyozin kasılmasıyla ileriye doğru "
                "çeker. Tümör hücrelerinden ve konak stromal hücrelerinden salgılanan kemotaktik faktörler (otokrin motilite faktörü), "
                "tümörün en düşük dirençli bağ dokusu düzlemleri boyunca hızla göç etmesini sağlar."
            ),
            "elements": [
                make_cloze(
                    "Kanser hücrelerinin stroma fibronektin ve kolajen liflerine tutunarak ilerlemesini sağlayan membran reseptör ailesine integrinler denir.",
                    "integrinler",
                    "Hücre-matriks bağlantı reseptörleri"
                ),
                make_micro_quiz(
                    "Tümör hücrelerinin stroma içinde psödopodlar uzatarak amoboid hareket etmesinde görevli hücre iskeleti motoru hangisidir?",
                    [
                        {
                            "text": "Aktin polimerizasyonu ve miyozin kasılması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; psödopod oluşumu ve hücresel çekilme aktin-miyozin mikrofilamanlarıyla yürütülür."
                        },
                        {
                            "text": "Hücre çekirdeğinin nükleazlarla erimesi",
                            "isCorrect": False,
                            "explanation": "Nükleus erimesi karyolizistir, hücre hareketini sağlamaz."
                        },
                        {
                            "text": "Mitokondri kristalarının dışarı fırlaması",
                            "isCorrect": False,
                            "explanation": "Mitokondriyal patlama hücreyi öldürür, hareket ettirmez."
                        },
                        {
                            "text": "Endoplazmik retikulumun yağ salgılaması",
                            "isCorrect": False,
                            "explanation": "Lipid sentezi motilite motoru değildir."
                        }
                    ],
                    "Aktin-miyozin hücre iskeleti kanser lokomosyonunun itici gücüdür."
                )
            ]
        },
        # Slayt 68
        {
            "slideNumber": 68,
            "title": "Epitelyal-Mezenkimal Geçiş (EMT): Moleküler Dönüşüm",
            "content": (
                "Epitelyal-Mezenkimal Geçiş (EMT), hareketsiz, polarize ve birbirine yapışık epitelyal kanser hücrelerinin; "
                "hareketli, iğsi şekilli, fagozitoz yapabilen ve invaziv mezenkimal benzeri hücrelere dönüştüğü moleküler bir "
                "metamorfozdur. Bu dönüşüm tümör mikroçevresindeki stromal faktörler (TGF-beta, hipoksi, Wnt) tarafından "
                "tetiklenir ve 'SNAIL', 'TWIST' ve 'SLUG' transkripsiyon faktörleri tarafından aktive edilir. EMT sırasında "
                "hücre epitelyal belirteçler olan E-kaderin ve sitokeratin ekspresyonunu tamamen kapatırken; mezenkimal belirteçler "
                "olan 'vimentin', N-kaderin ve matriks proteazlarını aşırı düzeyde sentezlemeye başlar. EMT kazanan hücreler "
                "kanser kök hücresi özellikleri kazanarak apoptoza ve kemoterapiye aşırı dirençli hale gelir."
            ),
            "elements": [
                make_table(
                    "Epitelyal-Mezenkimal Geçiş (EMT) Sırasında Fenotipik Dönüşüm",
                    ["Hücresel Parametre", "Epitel Fenotipi (Pre-EMT)", "Mezenkimal Fenotip (Post-EMT)"],
                    [
                        {
                            "cells": ["Hücre Morfolojisi", "Kübik/silindirik, polarize, hareketsiz", "İğsi (mekik), hareketli amoboid"],
                            "hiddenIndex": 2,
                            "hint": "Fusiform şekilli motil yapı"
                        },
                        {
                            "cells": ["Hücreler Arası Adezyon", "Yüksek (E-kaderin intakt)", "Yok (E-kaderin baskılı, N-kaderin var)"],
                            "hiddenIndex": 2,
                            "hint": "Hücrelerarası adezyon molekülü dönüşümü"
                        },
                        {
                            "cells": ["Ara Filaman Tipi", "Sitokeratin pozitif", "Vimentin pozitif"],
                            "hiddenIndex": 2,
                            "hint": "Mezenkimal ara filaman belirteci"
                        }
                    ]
                ),
                make_active_recall(
                    "Kanser hücrelerinin epitelyal fenotipten mezenkimal fenotipe (EMT) dönüşümünü yöneten anahtar transkripsiyon faktörleri nelerdir?",
                    "SNAIL, TWIST ve SLUG faktörleridir.",
                    "EMT'yi başlatan gen düzenleyicileri"
                )
            ]
        },
        # Slayt 69 [CHECKPOINT 7]
        {
            "slideNumber": 69,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Displazi, CIS ve İnvazyon",
            "content": (
                "Bu bölümde displazi spektrumunu, karsinoma in situ kavramını ve invazyonun moleküler mekanizmalarını özetledik. "
                "Displazi, epitel içinde sınırlı kalan hücresel atipi ve mimari bozukluktur; kanser demek değildir ve potansiyel olarak geri dönüşümlüdür. "
                "CIN sınıflamasında hafif (1/3), orta (2/3) ve şiddetli (>2/3) tutulum kullanılır. "
                "Karsinoma in situ (CIS), atipinin epitelin tüm katını tuttuğu ancak bazal membranın delinmediği preinvaziv kanserdir; metastaz riski sıfırdır. "
                "İnvaziv karsinom, tümörün Tip IV kollejenaz (MMP-2/9) salgılayarak bazal membranı yıkmasıyla başlar. "
                "İnvazyon basamakları: E-kaderin kaybıyla ayrılma, matriksin enzimatik yıkımı, integrinlerle matrikse tutunma ve amoboid harekettir. "
                "Epitelyal-Mezenkimal Geçiş (EMT), Snail ve Twist ile tetiklenen, sitokeratinden vimentine geçişle seyreden invaziv dönüşümdür."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp07-fc01",
                    "front": "Atipik hücrelerin epitelin tüm kalınlığını kaplamasına rağmen bazal membranın sağlam kaldığı preinvaziv lezyona ne ad verilir?",
                    "back": "Karsinoma in situ adı verilir.",
                    "hint": "Sıfır metastazlı tam kat epitel kanseri"
                },
                {
                    "id": "k1-28-cp07-fc02",
                    "front": "Kanser hücrelerinin bazal membranın tip IV kolajen iskeletini eriterek stromaya sızmasını sağlayan ana metalloproteinazlar nelerdir?",
                    "back": "Tip IV kollejenaz proteinleri olan MMP-2 ve MMP-9 molekülleridir.",
                    "hint": "Bazal zarı eriten matriks biyokatalizörleri"
                },
                {
                    "id": "k1-28-cp07-fc03",
                    "front": "Kanser hücrelerinin birbirine tutunmasını engelleyerek invazyonun ilk basamağını başlatan adezyon molekülü kaybı hangisidir?",
                    "back": "E-kaderin kaybıdır.",
                    "hint": "Hücreler arası fermuar görevi gören epitel proteini"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 7 Özet Tablosu: Preinvazivden İnvaziv Karsinoma Aşamalar",
                    ["Evre", "Bazal Membran Durumu", "Metastaz Riski", "Tedavi Yaklaşımı"],
                    [
                        {
                            "cells": ["Karsinoma In Situ (CIS)", "Tamamen Sağlam", "Kesinlikle %0", "Lokal cerrahi eksizyon yeterli"],
                            "hiddenIndex": 2,
                            "hint": "Sıfır sistemik yayılım riski"
                        },
                        {
                            "cells": ["İnvaziv Karsinom", "Delinmiş / Parçalanmış", "Var (Lenfovasküler temas)", "Geniş rezeksiyon + lenf nodu diseksiyonu"],
                            "hiddenIndex": 1,
                            "hint": "Yıkılmış bazal zar"
                        }
                    ]
                )
            ]
        },
        # Slayt 70
        {
            "slideNumber": 70,
            "title": "Klinik Karar: Servikal Tarama ve Premalign Lezyon Yönetimi",
            "content": (
                "Rutin Pap-smear taramasında servikal intraepitelyal neoplazi (CIN 3 / Şiddetli Displazi / Karsinoma In Situ) "
                "saptanan 32 yaşında kadın hastanın kolposkopik servikal biyopsisinde de lezyon doğrulanıyor; bazal membranın "
                "tamamen sağlam olduğu teyit ediliyor. Bu aşamada hastaya radikal histerektomi veya lenf nodu diseksiyonu "
                "kesinlikle gerekmez; çünkü bazal membran sağlam olduğu için metastaz riski sıfırdır. En akılcı ve doğurganlığı "
                "koruyucu yaklaşım, 'servikal LEEP' (Loop Elektrosurgical Excision Procedure) veya 'soğuk konizasyon' ile "
                "displazik transformasyon zonunun negatif cerrahi sınırlarla lokal olarak tam çıkarılmasıdır."
            ),
            "elements": [
                make_branching_logic(
                    "Servikal biyopsi raporunda bazal membranı sağlam tam kat displazi (Karsinoma In Situ / CIN 3) saptanan 29 yaşında çocuk sahibi olmak isteyen bir kadında en doğru klinik ve cerrahi yaklaşım ne olmalıdır?",
                    "Metastaz riski taşımayan bu preinvaziv lezyonda doğurganlığı korurken kür sağlayan tedavi nedir?",
                    [
                        {
                            "text": "Lokal servikal konizasyon veya LEEP eksizyonu uygulanarak lezyon negatif cerrahi sınırla çıkarılmalı ve uterus korunmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; CIS bazal membranı aşmadığı için lokal eksizyon küratiftir, radikal cerrahiye gerek yoktur."
                        },
                        {
                            "text": "Kanser olduğu için acilen radikal histerektomi ve pelvik lenfadenektomi yapılmalıdır.",
                            "isCorrect": False,
                            "explanation": "CIS metastaz yapmaz; radikal histerektomi overtreatment (aşırı tedavi) olur."
                        },
                        {
                            "text": "Hiçbir müdahale yapılmadan 5 yıl sonra kontrole çağrılmalıdır.",
                            "isCorrect": False,
                            "explanation": "CIN 3 tedavi edilmezse invaziv karsinoma ilerler; takipsiz bırakılamaz."
                        }
                    ]
                )
            ]
        }
    ]
