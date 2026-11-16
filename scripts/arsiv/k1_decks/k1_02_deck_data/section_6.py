#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 6: Tanısal Araçlar: Makroskopi, Rutin HE, Özel Histokimya ve İmmünohistokimya (Adımlar 50 - 59)
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
        # Adım 50
        {
            "slideNumber": 50,
            "title": "Makroskobik İnceleme ve Örnekleme (Sampling) Sanatı",
            "subtitle": "Histopatolojik tanının kaderi; dokunun diseksiyon masasında doğru incelenmesi, cerrahi sınırların işaretlenmesi ve temsili örnekleme yapılmasıyla çizilir.",
            "badge": "Makroskopi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Histopatolojik tanının en kritik ve geri dönüşü olmayan ilk basamağı makroskobik inceleme ve örneklemedir.

Ameliyathaneden gelen rezeksiyon materyalinin anatomik oryantasyonu yapıldıktan sonra boyut ve ağırlık ölçümleri kaydedilir. Cerrahi sınırların mikroskopta kesin ayırt edilebilmesi için doku dış yüzeyi farklı renklerde ==çini mürekkebi (surgical ink)== ile boyanır. Ardından organ 3-5 milimetrelik paralel dilimlerle açılır; tümörün en derin invazyon odağı, çevre sağlam doku sınırı, nekroz alanları ve çevre lenf nodları seçilerek kasetlenir. Doku parçalarının fiksatif penetrasyonu için 3-4 mm kalınlığı aşmaması şarttır.

> [TEMEL İLKE] Alınmayan doku mikroskopta incelenemez; örnekleme hatası (sampling error) patolojideki en yaygın yalancı negatiflik kaynağıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Cerrahi Sınır Boyama", "desc": "Mürekkeple işaretlenen sınırlar mikroskopta tümörün rezeksiyon hattına mesafesini gösterir.", "isKey": True},
                    {"title": "Temsili Kasetleme", "desc": "Tümör çapına göre (genellikle her 1 cm kitle için en az 1 kaset) doku alınır.", "isKey": True},
                    {"title": "Lenf Nodu Diseksiyonu", "desc": "Tümör evresini (pN) belirleyecek lenf nodları makroskopide aranıp çıkarılır.", "isKey": False}
                ],
                "table": {
                    "title": "Makroskobik İnceleme ve Örnekleme Kriterleri",
                    "headers": ["Aşama", "Yapılan İşlem", "Patolojik Hatanın Önlenmesi"],
                    "rows": [
                        ["Oryantasyon & Ölçüm", "Boyut, ağırlık, üç boyutlu milimetrik kayıt", "Tümörün makroskobik T evresinin doğru belirlenmesi"],
                        ["Mürekkep Boyama", "Cerrahi sınırların çini mürekkebiyle boyanması", "Mikroskopta cerrahi sınır pozitifliğinin yanlış değerlendirilmesinin önlenmesi"],
                        ["Dilimleme (Slicing)", "3-5 mm paralel kesitlerle organın açılması", "İç organ derinliğinde saklı kalan küçük tümör odaklarının kaçırılmaması"],
                        ["Kasetleme", "Doku takip kasetine uygun boyutta (en fazla 3-4 mm kalınlık) parça koyma", "Aşırı kalın parçanın fikse olamayıp merkezinin çürümesinin (otoliz) önlenmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Örnekleme (sampling), mikroskobik incelemenin kalitesini ve doğruluğunu belirleyen en kritik makroskobik basamaktır.",
                "📌 [SINAV SPOTU] Doku kasetlerine konulan parçalar fiksatifin eşit nüfuz edebilmesi için 3-4 milimetreden daha kalın olmamalıdır.",
                "🚨 [KRİTİK UYARI] Makroskobik incelemede yeterli lenf nodu bulunup örneklenmezse hastanın patolojik evresi (pN) hatalı olarak düşük çıkar."
            ],
            "medicalTerms": [
                {"term": "Örnekleme (Sampling)", "explanation": "Büyük cerrahi materyalden tanı ve evreleme için kritik doku odaklarının kasetlenmesidir."},
                {"term": "Çini Mürekkebi Boyaması", "explanation": "Cerrahi sınırların mikroskopta net seçilmesi için doku dışına sürülen özel boyadır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Makroskobik Diseksiyondan Kasetlemeye Örnekleme Zinciri",
                    [
                        "1. Oryantasyon: Rezeksiyon materyalinin anatomik yönleri belirlenip ölçümleri yapılır.",
                        "2. Sınır Boyama: Mikroskopta cerrahi sınırı görmek için yüzeye çini mürekkebi uygulanır.",
                        "3. Dilimleme: Organ 3-5 mm aralıkla paralel kesilerek tümör derinliği incelenir.",
                        "4. Kasetleme: Tümörün en derin odağı, cerrahi sınırlar ve lenf nodları kasetlere alınır.",
                        "5. Doku Takibi: Kasetlenen dokular formalin fiksasyonunun ardından takibe aktarılır."
                    ]
                ),
                make_micro_quiz(
                    "Meme karsinomu nedeniyle mastektomi yapılan bir materyalde patoloji uzmanının doku kasetlerine koyacağı parçaları 3-4 milimetreden daha kalın kesmemesinin temel nedeni nedir?",
                    {
                        "A": "Bıçakların daha az körelmesini sağlamak",
                        "B": "Formalin fiksatifinin dokunun merkezine saatte ~1 mm hızla nüfuz edebilmesi ve doku ortasında otolizi önlemek",
                        "C": "Lam üzerine kesit alırken hematoksilen boyasının tükenmesini engellemek",
                        "D": "Mikroskop objektifinin büyütme gücünü artırmak",
                        "E": "Doku kasetlerinin ağırlığını azaltmak"
                    },
                    "B",
                    {
                        "A": "Yanlış. Mikrotom bıçaklarının aşınmasıyla ilgisi yoktur.",
                        "B": "Doğru. Formalin saatte ~1 mm nüfuz eder; 4 mm'yi aşan parçaların merkezinde otoliz gelişir.",
                        "C": "Yanlış. Boyama basamağı doku takibi ve kesit sonrasındaki aşamadır.",
                        "D": "Yanlış. Mikroskobik büyütme optik sistemle ilgilidir.",
                        "E": "Yanlış. Kaset ağırlığının fiksasyon kalitesiyle ilgisi yoktur."
                    }
                ),
                make_cloze(
                    "Makroskobik incelemede dokunun cerrahi sınırlarının mikroskop altında kesin olarak ayırt edilebilmesi için çini mürekkebi ile boyama yapılır.",
                    "çini mürekkebi",
                    "Cerrahi sınırları işaretlemek için kullanılan özel boya"
                )
            ]
        },

        # Adım 51
        {
            "slideNumber": 51,
            "title": "Işık Mikroskopisi ve Optik Büyütme Prensipleri",
            "subtitle": "Işık mikroskobu; oküler, objektif ve kondansatör optik sistemleriyle doku kesitlerini yaklaşık 1000 kata kadar büyüterek hücre morfolojisini görünür kılar.",
            "badge": "Işık Mikroskobu",
            "badgeColor": "indigo",
            "discipline": "Optik ve Patoloji",
            "synthesisNarrative": """Rutin patoloji pratiğinin temel optik inceleme aracı aydınlık alan ışık mikroskobudur.

Işık mikroskobu; ışık kaynağı, kondansatör, objektifler ve oküler mercek sisteminden oluşur. Toplam büyütme gücü, 10x oküler ile kullanılan objektif büyütmesinin çarpımıyla belirlenir (örneğin 40x objektif ile 400x büyütme). Işık mikroskobunun teorik ==çözünürlük sınırı yaklaşık 0.2 mikrometredir (200 nm)==. Patolog kesiti incelerken önce ==4x-10x küçük büyütmeyle== genel doku mimarisini ve lezyon sınırlarını haritalandırır; ardından ==40x büyük büyütmeye== geçerek nükleer atipi, kromatin yapısı ve atipik mitozları değerlendirir.

> [OPTİK KURAL] Büyütme görüntüyü yaklaştırırken, çözünürlük birbirine yakın iki noktanın ayrı seçilebilmesini belirler.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Toplam Büyütme", "desc": "Oküler (10x) ile objektif büyütmesinin çarpımıdır (en fazla 1000-1500x).", "isKey": True},
                    {"title": "Çözünürlük Sınırı", "desc": "Görünür ışık dalga boyu nedeniyle teorik çözünürlük sınırı yaklaşık 0.2 µm'dir.", "isKey": True},
                    {"title": "Kondansatör Fonksiyonu", "desc": "Işık huzmesini kesit üzerine odaklayarak kontrast ve netliği ayarlar.", "isKey": False}
                ],
                "table": {
                    "title": "Işık Mikroskobunda Objektifler ve Patolojik Kullanım Amaçları",
                    "headers": ["Objektif Büyütmesi", "Toplam Büyütme (10x Oküler)", "İncelenen Patolojik Yapı"],
                    "rows": [
                        ["4x (Tarama)", "40x", "Doku mimarisi genel haritası, lezyon sınırları, kıkırdak/kemik dağılımı"],
                        ["10x (Küçük Büyütme)", "100x", "Granülom odakları, tübüler yapılar, inflamatuvar infiltrasyon yoğunluğu"],
                        ["40x (Büyük Büyütme)", "400x", "Hücre çekirdeği özellikleri, kromatin yapısı, atipik mitoz figürleri"],
                        ["100x (İmmersiyon)", "1000x", "Bakteriler (tüberküloz basili), kemik iliği hücreleri, ince sitolojik ayrıntılar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Standart ışık mikroskobunun teorik çözünürlük sınırı yaklaşık 0.2 mikrometre (200 nm)'dir.",
                "📌 [OPTİK SPOT] Toplam mikroskobik büyütme, oküler merceği ile objektif merceğinin büyütme değerlerinin çarpımıdır.",
                "💡 [ÖĞRENME İPUCU] Patolog bir preparatı incelerken daima önce 4x veya 10x küçük büyütmeyle genel mimariyi tarar, ardından 40x ile nükleer detaylara iner."
            ],
            "medicalTerms": [
                {"term": "Çözünürlük (Resolution)", "explanation": "Birbirine yakın iki ayrı noktayı bağımsız nesneler olarak ayırt edebilme yeteneğidir."},
                {"term": "Kondansatör", "explanation": "Işık kaynağından gelen ışınları toplayıp preparat üzerine odaklayan optik parçadır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Küçük Büyütme (4x-10x) vs Büyük Büyütme (40x) İnceleme Amacı",
                    "Küçük Büyütme (Mimari Bakış)",
                    "Büyük Büyütme (Sitolojik Detay)",
                    [
                        "Doku mimarisini ve organ katmanlarını bir bütün olarak gösterir",
                        "Tümörün çevre sağlam dokuyla olan sınırını ve derinliğini tarar",
                        "Nekroz ve inflamasyon odaklarının dağılım haritasını çıkarır",
                        "Cerrahi sınırların temiz olup olmadığını geniş açıdan kontrol eder"
                    ],
                    [
                        "Tek tek hücrelerin nükleus/sitoplazma (N/S) oranını gösterir",
                        "Kromatin kabalaşmasını ve belirgin nükleolleri analiz eder",
                        "Mitoz figürlerini ve anormal atipik mitozları sayar",
                        "Apoptoz cisimcikleri ve nötrofilik infiltrasyon ayrıntılarını inceler"
                    ]
                ),
                make_micro_quiz(
                    "Standart bir ışık mikroskobunda 10x oküler ve 40x objektif kullanılırken incelenen bir doku kesiti kaç kat büyütülmüş olur ve bu mikroskobun teorik çözünürlük sınırı yaklaşık ne kadardır?",
                    {
                        "A": "50 kat büyütme — 2 mikrometre",
                        "B": "400 kat büyütme — 0.2 mikrometre (200 nm)",
                        "C": "40 kat büyütme — 0.02 nanometre",
                        "D": "4000 kat büyütme — 2 nanometre",
                        "E": "100 kat büyütme — 5 mikrometre"
                    },
                    "B",
                    {
                        "A": "Yanlış. Büyütmeler toplanmaz, birbiriyle çarpılır.",
                        "B": "Doğru. Toplam büyütme 10x40=400x olup ışık mikroskobunun çözünürlük sınırı ~0.2 µm'dir.",
                        "C": "Yanlış. Büyütme hesabı ve çözünürlük değeri hatalıdır.",
                        "D": "Yanlış. Standart ışık mikroskobunda 4000x büyütme sağlanamaz.",
                        "E": "Yanlış. Büyütme ve çözünürlük sayısal olarak yanlıştır."
                    }
                ),
                make_cloze(
                    "Işık mikroskobunda iki ayrı noktayı birbirinden bağımsız iki nesne olarak ayırt edebilme kabiliyetine çözünürlük adı verilir.",
                    "çözünürlük",
                    "Mikroskobun ayırt etme gücünü tanımlayan optik kavram"
                )
            ]
        },

        # Adım 52
        {
            "slideNumber": 52,
            "title": "Rutin Hematoksilen-Eozin (HE) Boyası: Bazofili ve Eozinofili Mekanizması",
            "subtitle": "Histopatolojinin altın standart boyası olan HE; bazik hematoksilen ile nükleusu maviye, asidik eozin ile sitoplazmayı pembeye boyar.",
            "badge": "Rutin Boya HE",
            "badgeColor": "red",
            "discipline": "Histopatoloji",
            "synthesisNarrative": """Histopatoloji laboratuvarlarında doku kesitlerinin büyük çoğunluğu Hematoksilen-Eozin (HE) boyasıyla değerlendirilir.

==Hematoksilen== bazik bir boyadır; pozitif yüküyle hücre çekirdeğindeki negatif yüklü asidik DNA ve RNA'ya bağlanır. Bu duruma ==Bazofili== denir ve nükleuslar mikroskopta koyu ==mavi-mor== boyanır. ==Eozin== ise asidik bir boyadır; negatif yüküyle sitoplazmadaki pozitif yüklü bazik proteinlere ve kollajene bağlanır. Bu duruma ==Eozinofili (Asidofili)== denir ve sitoplazma ile bağ dokusu ==pembe-kırmızı== renk alır. Malign hücrelerde DNA ve ribozom artışı dokunun daha koyu mor-mavi (hiperkromatik) görünmesine neden olur.

> [KİMYASAL İLKE] Nükleus asidiktir ve bazik boyayı tutar (bazofilik/mor); sitoplazma baziktir ve asidik boyayı tutar (eozinofilik/pembe).""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hematoksilen", "desc": "Bazik boyadır; DNA ve RNA'yı koyu mavi-mor renge boyar (Bazofilik).", "isKey": True},
                    {"title": "Eozin", "desc": "Asidik boyadır; sitoplazma ve kollajen lifleri pembeye boyar (Eozinofilik).", "isKey": True},
                    {"title": "Hiperkromazi", "desc": "Malign hücrelerde artan DNA içeriği çekirdeğin aşırı koyu mavi boyanmasına yol açar.", "isKey": False}
                ],
                "table": {
                    "title": "Hematoksilen ve Eozin Boyasının Kimyasal Karşılaştırması",
                    "headers": ["Parametre", "Hematoksilen", "Eozin"],
                    "rows": [
                        ["Boya Niteliği", "Bazik (katyonik) boya", "Asidik (anyonik) boya"],
                        ["Bağlandığı Doku Yapısı", "Asidik bileşenler (DNA, RNA, kıkırdak matriksi)", "Bazik bileşenler (proteinler, sitoplazma, kollajen)"],
                        ["Oluşturduğu Renk", "Koyu mavi, mor", "Açık pembe, kırmızı"],
                        ["Afinite Adı", "Bazofili (bazik boyayı sevme)", "Eozinofili / Asidofili (asidik boyayı sevme)"],
                        ["Tipik Hücresel Hedef", "Hücre nükleusu, nükleol, ribozomlar", "Sitoplazma, mitokondriler, kas lifleri, kollajen"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hematoksilen bazik bir boyadır; asidik nükleik asitleri (DNA/RNA) mavi-mor renge boyar (bazofili).",
                "📌 [SINAV SPOTU] Eozin asidik bir boyadır; bazik proteinleri, sitoplazmayı ve kollajeni pembe renge boyar (eozinofili).",
                "💡 [ÖĞRENME İPUCU] Kanserli hücreler ribozom ve DNA fazlalığından dolayı standart dokuya göre çok daha belirgin mor-mavi (bazofilik) izlenir."
            ],
            "medicalTerms": [
                {"term": "Bazofili", "explanation": "Doku yapılarının bazik boyaya (hematoksilen) bağlanarak mavi-mor renge boyanmasıdır."},
                {"term": "Eozinofili (Asidofili)", "explanation": "Sitoplazma ve proteinlerin asidik boyaya (eozin) tutunarak pembe boyanması özelliğidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Bazofilik vs Eozinofilik Hücresel Yapılar (HE Boyasında)",
                    "Bazofilik Yapılar (Hematoksilen / Mavi-Mor)",
                    "Eozinofilik Yapılar (Eozin / Pembe)",
                    [
                        "Hücre çekirdeğindeki kromatin ve DNA iplikçikleri",
                        "Çekirdekçikteki yoğun ribozomal RNA konsantrasyonu",
                        "Granüllü endoplazmik retikulum üzerindeki ribozomlar",
                        "Hiyalin kıkırdaktaki asidik kondroitin sülfat zemin"
                    ],
                    [
                        "Hücre sitoplazması ve sitozoldeki enzim proteinleri",
                        "Sitoplazmadaki yoğun mitokondriler (ör. onkositik hücre)",
                        "Hücre dışı matriksteki kollajen ve elastik bağ dokusu",
                        "Eritrositlerin içindeki yoğun hemoglobin proteini"
                    ]
                ),
                make_micro_quiz(
                    "Rutin histopatolojik Hematoksilen-Eozin (HE) boyaması ile ilgili aşağıdaki ifadelerden hangisi BİYOKİMYASAL OLARAK DOĞRUDUR?",
                    {
                        "A": "Hematoksilen asidik bir boyadır ve sitoplazmayı pembeye boyar.",
                        "B": "Eozin bazik bir boyadır ve çekirdekteki DNA moleküllerine bağlanır.",
                        "C": "Hematoksilen bazik boyadır ve asidik nükleik asitleri (DNA/RNA) mavi-mor renge boyar.",
                        "D": "Kollajen lifleri hematoksilen ile koyu mor renkte izlenir.",
                        "E": "HE boyasında hücre çekirdeği pembe, sitoplazma ise daima mavidir."
                    },
                    "C",
                    {
                        "A": "Yanlış. Hematoksilen bazik bir boyadır ve sitoplazmayı değil nükleusu boyar.",
                        "B": "Yanlış. Eozin asidik boyadır ve sitoplazmik proteinlere bağlanır.",
                        "C": "Doğru. Hematoksilen baziktir; asidik nükleik asitlere bağlanarak nükleusu mavi-mor boyar.",
                        "D": "Yanlış. Kollajen lifleri eozin ile pembe renkte boyanır.",
                        "E": "Yanlış. HE boyasında çekirdek mavi-mor, sitoplazma ise pembedir."
                    }
                ),
                make_cloze(
                    "Hematoksilen-eozin boyasında sitoplazmanın ve ekstraselüler kollajen liflerinin eozin ile pembe renge boyanması özelliğine eozinofili adı verilir.",
                    "eozinofili",
                    "Asidik boya eozine afinite sonucu pembe boyanma özelliği"
                )
            ]
        },

        # Adım 53
        {
            "slideNumber": 53,
            "title": "Özel Histokimyasal Boyalar I: Prusya Mavisi (Perls) ile Demir ve Hemosiderin Tayini",
            "subtitle": "Prusya mavisi histokimyasal reaksiyonu; dokularda biriken demir (Fe3+) ve hemosiderin pigmentini parlak mavi renge boyayarak hemokromatozis tanısını koyar.",
            "badge": "Demir Boyası",
            "badgeColor": "blue",
            "discipline": "Histokimya",
            "synthesisNarrative": """Rutin HE boyasında sarı-kahverengi izlenen doku pigmentlerinin ayırıcı tanısında özel histokimyasal yöntemler kullanılır.

Demir birikimini kanıtlayan temel yöntem ==Prusya Mavisi (Perls Reaksiyonu)== boyasıdır. Asidik ortamda dokudaki serbest ferrik demir ($Fe^{3+}$) iyonları potasyum ferrosiyanür ile birleşerek suda erimeyen ferrik ferrosiyanür tuzunu oluşturur. Bu reaksiyon sonucunda demir odakları mikroskopta parlak ==mavi (turkuaz)== renk alır. Prusya mavisi; ==hemokromatozis== tanısında karaciğer demir yükünü, sol kalp yetmezliğinde akciğerdeki ==kalp yetersizliği hücrelerini== ve kemik iliğinde sideroblastik anemiyi doğrulamada kullanılır.

> [TANI KURALI] Karaciğer biyopsisinde görülen pigment Prusya mavisiyle parlak maviye dönüyorsa kesinlikle hemosiderindir (demir).""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hedef Molekül", "desc": "Hemosiderin ve ferritin yapısındaki ferrik demir ($Fe^{3+}$) iyonlarıdır.", "isKey": True},
                    {"title": "Oluşan Renk", "desc": "Demir odakları mikroskop altında çarpıcı parlak mavi renge döner.", "isKey": True},
                    {"title": "Kalp Yetersizliği Hücresi", "desc": "Akciğer alveollerinde hemosiderin yüklü makrofajları doğrular.", "isKey": False}
                ],
                "table": {
                    "title": "Prusya Mavisi (Perls) Boyasının Klinikopatolojik Endikasyonları",
                    "headers": ["Klinik Tablo", "İncelenen Organ", "Histokimyasal Prusya Mavisi Görünümü"],
                    "rows": [
                        ["Primer Hemokromatozis", "Karaciğer biyopsisi", "Hepatosit sitoplazmasında ve safra kanaliküllerinde yoğun mavi granüller"],
                        ["Kronik Sol Kalp Yetersizliği", "Akciğer dokusu / Balgam", "Alveol lümenlerindeki makrofaj sitoplazmalarında parlak mavi granüller"],
                        ["Sideroblastik Anemi", "Kemik iliği biyopsisi", "Eritroid öncüllerinde çekirdek etrafında halkalanmış mavi demir birikimi (ring sideroblast)"],
                        ["Eski Hemoraji / Hematom", "Deri altı / Beyin dokusu", "Makrofajlar içinde fagosite edilmiş hemosiderin granülleri maviye boyanır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Dokularda demir ve hemosiderin varlığını gösteren özel histokimyasal boya Prusya Mavisi (Perls) boyasıdır.",
                "📌 [SINAV SPOTU] Kronik akciğer konjesyonunda 'kalp yetersizliği hücreleri' hemosiderin içerir ve Prusya mavisi ile pozitif boyanır.",
                "💡 [ÖĞRENME İPUCU] Melanin ve lipofuskin pigmentleri sarı-kahverengidir fakat Prusya mavisiyle boyanmaz; bu sayede demirden ayırt edilir."
            ],
            "medicalTerms": [
                {"term": "Prusya Mavisi (Perls)", "explanation": "Ferrik demir iyonlarını potasyum ferrosiyanür ile parlak maviye boyayan demir boyasıdır."},
                {"term": "Kalp Yetersizliği Hücresi", "explanation": "Sol kalp yetmezliğinde akciğer alveollerinde hemosiderin depolayan makrofajlardır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kalp Yetersizliğinde Prusya Mavisi Pozitiflik Zinciri",
                    [
                        "1. Konjesyon: Sol ventrikül yetmezliğinde pulmoner venöz basınç ve kapiller dolgunluk artar.",
                        "2. Eritrosit Kaçağı: Basınç artışıyla alveol boşluğuna eritrosit ekstravazasyonu gerçekleşir.",
                        "3. Fagositoz: Alveoler makrofajlar eritrositleri yutarak hemoglobini parçalar.",
                        "4. Hemosiderin Oluşumu: Parçalanan demir makrofaj sitoplazmasında hemosiderin kristallerine döner.",
                        "5. Mavi Boyanma: Prusya mavisi uygulandığında hemosiderin yüklü makrofajlar parlak maviye boyanır."
                    ]
                ),
                make_micro_quiz(
                    "Kronik karaciğer hastalığı şüphesiyle yapılan karaciğer biyopsisinde hepatosit sitoplazmasında biriken kahverengi granüllerin 'hemosiderin (demir)' olduğunu kanıtlamak için aşağıdaki histokimyasal boyalardan hangisi seçilmelidir?",
                    {
                        "A": "Masson Trikrom Boyası",
                        "B": "Prusya Mavisi (Perls) Boyası",
                        "C": "Periyodik Asit-Schiff (PAS) Boyası",
                        "D": "Kongo Kırmızısı Boyası",
                        "E": "Touluidin Mavisi Boyası"
                    },
                    "B",
                    {
                        "A": "Yanlış. Masson trikrom bağ dokusu kollajenini gösteren boyadır.",
                        "B": "Doğru. Prusya mavisi hemosiderin ve serbest demiri parlak mavi renge boyar.",
                        "C": "Yanlış. PAS glikojen, bazal membran ve mantarları boyar.",
                        "D": "Yanlış. Kongo kırmızısı amiloid birikimini gösterir.",
                        "E": "Yanlış. Toluidin mavisi mast hücrelerindeki metakromaziyi boyar."
                    }
                ),
                make_cloze(
                    "Dokularda biriken demir ve hemosiderin granüllerini mikroskopta parlak mavi renge boyayan özel histokimyasal yönteme Prusya mavisi adı verilir.",
                    "Prusya mavisi",
                    "Demir birikimini gösteren ünlü mavi histokimyasal boya"
                )
            ]
        },

        # Adım 54
        {
            "slideNumber": 54,
            "title": "Özel Histokimyasal Boyalar II: Periyodik Asit-Schiff (PAS) ile Glikojen, Mukus ve Mantarlar",
            "subtitle": "PAS boyası; glikojen, bazal membran mukopolisakkaritleri ve mantar hücre duvarlarını parlak macenta (pembe-eflatun) renge boyar.",
            "badge": "PAS Boyası",
            "badgeColor": "pink",
            "discipline": "Histokimya",
            "synthesisNarrative": """Karbonhidrat yapılarının ve mantarların gösterilmesinde altın standart boya Periyodik Asit-Schiff (PAS) yöntemidir.

==PAS boyamasında== periyodik asit glikol gruplarını oksitleyerek serbest aldehitlere dönüştürür; renksiz Schiff reaktifi bu aldehitlere bağlanarak dokuyu parlak ==macenta (eflatun-pembe)== renge boyar. PAS boyası; böbrek glomerül ve epitel ==bazal membranlarını==, goblet hücrelerinin müsin salgısını ve ==mantar hücre duvarındaki== kitin-glukan polisakkaritlerini net şekilde ortaya koyar. Dokudaki pozitifliğin glikojen olduğunu kanıtlamak için ==diastaz enzimi== kullanılır; diastaz ile sindirilen glikojen PAS boyanmasını kaybeder (d-PAS testi).

> [TANI KURALI] Glomerüler bazal membran kalınlaşmalarını ve Candida/Aspergillus hiflerini dokuda en iyi gösteren boya PAS'tır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hedef Yapılar", "desc": "Glikojen, bazal membran, nötral müsin ve mantar hücre duvarı polisakkaritleridir.", "isKey": True},
                    {"title": "Macenta Rengi", "desc": "Schiff reaktifiyle reaksiyon sonucu çarpıcı eflatun-kırmızı renk oluşur.", "isKey": True},
                    {"title": "Diastaz Duyarlılığı", "desc": "Glikojen diastaz enzimiyle sindirilir; d-PAS ile glikojen diğer maddelerden ayrılır.", "isKey": False}
                ],
                "table": {
                    "title": "PAS Boyamasının Başlıca Pozitiflik Alanları",
                    "headers": ["Yapı / Patojen", "PAS Reaktivitesi", "Klinikopatolojik Anlamı"],
                    "rows": [
                        ["Glikojen", "PAS Pozitif (Diastaz ile sindirilir)", "Glikojen depo hastalıkları, Ewing sarkomu, berrak hücreli karsinom"],
                        ["Glomerül Bazal Membranı", "PAS Pozitif (Diastaza dirençli)", "Diyabetik nefropati (Kimmelstiel-Wilson nodülleri), membranöz GN"],
                        ["Mantar Duvarı (Candida)", "PAS Pozitif (Koyu macenta)", "Doku invazyonu yapan mantar hif ve sporlarının tanısı"],
                        ["Goblet Hücre Müsini", "PAS Pozitif", "İntestinal metaplazi ve adenokarsinomlarda müsin salgısının gösterilmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Glikojen, nötral mukopolisakkaritler, bazal membran ve mantar hücre duvarlarını boyayan özel boya PAS (Periyodik Asit-Schiff) boyasıdır.",
                "📌 [SINAV SPOTU] PAS ile boyanan yapının 'glikojen' olduğunu kanıtlamak için Diastaz enzimi kullanılır (d-PAS ile glikojen kaybolur).",
                "💡 [ÖĞRENME İPUCU] Böbrek biyopsisinde glomerüler bazal membran kalınlaşmasını HE'den çok daha net olarak PAS boyası gösterir."
            ],
            "medicalTerms": [
                {"term": "Periyodik Asit-Schiff (PAS)", "explanation": "Polisakkaritleri, bazal membranları ve mantar duvarlarını macenta renge boyayan yöntemdir."},
                {"term": "Diastaz (Amilaz)", "explanation": "Glikojeni sindirerek dokudaki PAS boyanmasını kaldıran ve glikojeni doğrulayan enzimdir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "PAS Boyasının Tanısal Hedefleri",
                    ["Doku / Lezyon", "Hedef Biyomolekül", "Klinik Tanı"],
                    [
                        [
                            ("Candida Özofajiti", False),
                            ("Mantar hücre duvarı polisakkaritleri", True, "Kitin ve glukan polimerleri"),
                            ("Mantar hiflerinin eflatun boyanması", False)
                        ],
                        [
                            ("Diyabetik Glomerüloskleroz", False),
                            ("Glomerül bazal membran glikoproteinleri", True, "Bazal membran kalınlaşması"),
                            ("Kimmelstiel-Wilson nodülleri", False)
                        ],
                        [
                            ("Glikojenozis (Gierke)", False),
                            ("Hepatosit içi glikojen birikimi", True, "Hücre içi depo polisakkariti"),
                            ("d-PAS ile sindirilen birikim", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Böbrek biyopsisinde glomerüler bazal membranın kalınlaşmasını ve Candida mantar enfeksiyonundaki hiflerin hücre duvarını parlak macenta (pembe-mor) renkte gösteren histokimyasal boya hangisidir?",
                    {
                        "A": "Prusya Mavisi",
                        "B": "Periyodik Asit - Schiff (PAS)",
                        "C": "Oil Red O",
                        "D": "Masson Trikrom",
                        "E": "Kongo Kırmızısı"
                    },
                    "B",
                    {
                        "A": "Yanlış. Prusya mavisi hemosiderin demirini boyar.",
                        "B": "Doğru. PAS bazal membranları, glikojeni ve mantar hücre duvarlarını macenta boyar.",
                        "C": "Yanlış. Oil Red O lipidleri kırmızıya boyar.",
                        "D": "Yanlış. Masson trikrom bağ dokusu kollajenini boyar.",
                        "E": "Yanlış. Kongo kırmızısı amiloid birikimini gösterir."
                    }
                ),
                make_cloze(
                    "Glikojen, mukopolisakkaritler ve mantar hücre duvarını macenta renge boyayan yönteme Periyodik Asit-Schiff boyası adı verilir.",
                    "Periyodik Asit-Schiff",
                    "Polisakkaritleri ve bazal membranı boyayan ünlü yöntem"
                )
            ]
        },

        # Adım 55
        {
            "slideNumber": 55,
            "title": "Özel Histokimyasal Boyalar III: Masson Trikrom ile Bağ Dokusu ve Fibrozis Tayini",
            "subtitle": "Masson trikrom; kolajen liflerini mavi/yeşil, kas liflerini kırmızı boyayarak karaciğer sirozunda ve kalp infarktında fibrozisi haritalandırır.",
            "badge": "Fibrozis Boyası",
            "badgeColor": "emerald",
            "discipline": "Histokimya",
            "synthesisNarrative": """Kronik organ hasarlarında gelişen fibrozisi ve skar dokusunu haritalandırmak için Masson Trikrom boyası kullanılır.

Rutin HE boyasında kollajen ile kas dokusu benzer pembe tonlarda boyandığından fibrozisin derecesini saptamak zordur. ==Masson Trikrom== boyası doku bileşenlerini üç renkle ayırır: ==Kollajen bağ dokusu mavi== (veya yeşil), ==kas lifleri ve sitoplazma kırmızı==, ==hücre çekirdekleri ise koyu siyah-kahverengi== boyanır. Bu boya; kronik hepatitte portal alanlar arası fibröz köprüleşmeyi ve ==karaciğer sirozu evrelemesini== (METAVIR/Ishak) netleştirmede ve geçirilmiş miyokard enfarktüsü skarlarını göstermede vazgeçilmezdir.

> [KLİNİK İLKE] Siroz tanısında fibröz bantların köprüleşmesi rutin HE ile değil, Masson trikrom boyasıyla kanıtlanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Üçlü Renk Ayrımı", "desc": "Kollajen mavi, kas lifleri kırmızı, çekirdekler siyah boyanır.", "isKey": True},
                    {"title": "Siroz Evreleme Standardı", "desc": "Portal-santral köprüleşme fibrozisini net gösteren zorunlu boyadır.", "isKey": True},
                    {"title": "Miyokard Skarı", "desc": "Eski kalp krizinde canlı kas ile ölü fibröz doku sınırını keskinleştirir.", "isKey": False}
                ],
                "table": {
                    "title": "Masson Trikrom Boyasında Doku Bileşenlerinin Renk Dağılımı",
                    "headers": ["Doku Bileşeni", "Oluşan Renk", "Patolojik İnceleme Amacı"],
                    "rows": [
                        ["Kollajen Lifler (Tip I ve III)", "Parlak Mavi (veya Yeşil)", "Fibrozis, skleroz, sirotik fibröz bantlar"],
                        ["Kas Dokusu (Miyokard / Düz Kas)", "Kırmızı", "Kas atrofisi ve sağlam parankim adaları"],
                        ["Hücre Çekirdekleri", "Siyah / Koyu Kahverengi", "Hücre sayısı ve nükleer lokalizasyon"],
                        ["Eritrositler", "Sarı / Kırmızı", "Vasküler lümen ve konjesyon kontrolü"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kollajen bağ dokusunu mavi, kas dokusunu kırmızı boyayarak fibrozisi ve sirozu gösteren özel boya Masson Trikrom boyasıdır.",
                "📌 [SINAV SPOTU] Van Gieson boyası da kollajeni kırmızı, kası sarı boyayan bir diğer bağ dokusu boyasıdır.",
                "💡 [ÖĞRENME İPUCU] Siroz biyopsisinde patolog mavi boyanan fibröz bantların portal alanları birleştirip birleştirmediğine (köprüleşme) bakar."
            ],
            "medicalTerms": [
                {"term": "Masson Trikrom", "explanation": "Kollajeni maviye, kas dokusunu kırmızıya boyayarak organ fibrozisini gösteren boyadır."},
                {"term": "Fibrozis", "explanation": "Kronik zedelenme sonrası dokuda kollajen birikimiyle oluşan nedbeleşme sürecidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Kronik Karaciğer Biyopsisinde HE vs Masson Trikrom Boyası",
                    "Rutin HE Görünümü",
                    "Masson Trikrom Görünümü",
                    [
                        "Fibröz bantlar ve parankim pembe tonda birbirine benzer",
                        "Erken dönem portal fibrozis gözden kaçabilir",
                        "Kollajen ile komşu parankim sınırı belirsizdir",
                        "Siroz evrelemesinde kantitatif skorlama güçtür"
                    ],
                    [
                        "Kollajen lifleri parlak mavi, hepatosit kordonları kırmızıdır",
                        "En ince portal ve perisinüzoidal fibrozis dahi parlar",
                        "Portal-portal ve portal-santral mavi köprüler keskinleşir",
                        "METAVIR/Ishak fibrozis evresi hatasız skorlanır"
                    ]
                ),
                make_micro_quiz(
                    "Kronik hepatit B hastasında karaciğer biyopsisinde fibrozisin derecesini ve portal alanlar arasında köprüleşme oluşup oluşmadığını değerlendirmek için patoloji uzmanının mutlaka istemesi gereken histokimyasal boya hangisidir?",
                    {
                        "A": "Prusya Mavisi",
                        "B": "Masson Trikrom Boyası",
                        "C": "Oil Red O Boyası",
                        "D": "Kongo Kırmızısı",
                        "E": "Touluidin Mavisi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Prusya mavisi hemosiderin demirini boyar.",
                        "B": "Doğru. Masson trikrom kollajeni mavi boyayarak siroz ve fibrozisi kesin olarak gösterir.",
                        "C": "Yanlış. Oil Red O lipidleri gösteren boyadır.",
                        "D": "Yanlış. Kongo kırmızısı amiloid depolarını boyar.",
                        "E": "Yanlış. Toluidin mavisi mast hücresi granüllerini gösterir."
                    }
                ),
                make_cloze(
                    "Karaciğer ve kalp dokusunda kollajen liflerini maviye, kas dokusunu kırmızıya boyayarak fibrozisi gösteren yönteme Masson trikrom boyası denir.",
                    "Masson trikrom",
                    "Bağ dokusunu mavi boyayan üçlü boyama tekniği"
                )
            ]
        },

        # Adım 56
        {
            "slideNumber": 56,
            "title": "Özel Histokimyasal Boyalar IV: Dondurulmuş Kesitte Lipid Boyaları (Oil Red O ve Sudan Siyahı)",
            "subtitle": "Rutin takipteki organik çözücüler yağları erittiği için; hücresel lipidler ancak dondurulmuş (frozen) taze kesitlerde Oil Red O ile gösterilebilir.",
            "badge": "Lipid Boyaları",
            "badgeColor": "orange",
            "discipline": "Histokimya",
            "synthesisNarrative": """Hücresel lipidlerin mikroskobik tayininde en önemli kural, parafin takibi yerine taze dondurulmuş doku kullanılmasıdır.

Rutin parafin doku takibinde kullanılan alkol ve ==ksilen gibi organik çözücüler dokudaki tüm nötral yağları çözer==; bu nedenle standart HE kesitlerinde yağ damlaları boş vakuol şeklinde kalır. Hücre içindeki maddenin lipid olduğunu kanıtlamak veya ==yağ embolisi== tanısı koymak için taze doku kriostat cihazında dondurularak kesilir. Alınan kesitler lipofilik ==Oil Red O== ile boyandığında trigliseridler parlak ==kırmızı-turuncu==, Sudan Siyahı ile boyandığında ise siyah renk alır.

> [METODOLOJİK KURAL] Dokuda lipid göstermek için parafin takip yapılamaz; taze doku dondurularak Oil Red O ile boyanmalıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Ksilenin Yağı Eritmesi", "desc": "Rutin parafin takibinde solventler yağı tamamen erittiğinden vakuol boş kalır.", "isKey": True},
                    {"title": "Dondurulmuş Kesit Şartı", "desc": "Lipid boyaması yalnızca taze dondurulmuş (kriostat) dokularda uygulanabilir.", "isKey": True},
                    {"title": "Oil Red O Rengi", "desc": "Nötral trigliserit damlacıklarını parlak kırmızı renge boyar.", "isKey": False}
                ],
                "table": {
                    "title": "Lipid Boyama Metodolojisi ve Tuzaklar",
                    "headers": ["Yöntem / Parametre", "Rutin Parafin Takip", "Kriostat + Oil Red O"],
                    "rows": [
                        ["Organik Çözücü (Ksilen)", "Kullanılır (Lipidleri tamamen eritir ve uzaklaştırır)", "Kullanılmaz (Doku dondurularak fiziksel kesilir)"],
                        ["Mikroskopik Görünüm", "Hücre sitoplazmasında 'optik olarak boş' yuvarlak delikler", "Sitoplazma içinde parlak kırmızı-turuncu boyanmış lipid damlaları"],
                        ["Tanısal Değer", "Yağ şüphesi uyandırır ama glikojen/müsinle karışabilir", "Nötral lipit varlığını kesin olarak kanıtlar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Dokularda nötral lipidleri (yağ) göstermek için rutin parafin kesit kullanılamaz; dondurulmuş (frozen) kesitte Oil Red O boyası yapılır.",
                "📌 [SINAV SPOTU] Rutin parafin blok takibinde yağların erimesine ve boş vakuol kalmasına neden olan kimyasal basamak ksilen (şeffaflaştırma) ve alkoldür.",
                "💡 [ÖĞRENME İPUCU] Kemik kırığı sonrası ani solunum yetmezliğinden ölen bir hastanın otopsisinde akciğerde yağ embolisi Oil Red O ile dondurulmuş kesitte kanıtlanır."
            ],
            "medicalTerms": [
                {"term": "Oil Red O", "explanation": "Nötral lipidleri dondurulmuş kesitlerde parlak kırmızı renge boyayan lipofilik boyadır."},
                {"term": "Kriostat", "explanation": "Dondurulmuş taze dokulardan fiksasyonsuz mikron düzeyinde kesit alan soğutmalı cihazdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Lipid Boyamasında Metodoloji Zinciri",
                    [
                        "1. Taze Doku Alımı: Karaciğer veya şüpheli emboli dokusu tespit sıvısına konmadan taze alınır.",
                        "2. Kriyofiksasyon: Doku kriostat cihazında dondurularak kesit almaya uygun sertliğe getirilir.",
                        "3. Dondurma Kesiti: Dondurulan bloktan mikrotom bıçağıyla lam üzerine ince kesit alınır.",
                        "4. Boyama: Çözücü kullanılmadan lipofilik Oil Red O boyası doğrudan kesite uygulanır.",
                        "5. Mikroskobik Tanı: Hepatosit veya damar içindeki nötral yağlar parlak kırmızı renkte görülür."
                    ]
                ),
                make_micro_quiz(
                    "Bir patoloji asistanı şüpheli karaciğer steatozu (yağlanması) olan bir dokuyu rutin dehidrasyon ve ksilen şeffaflaştırmasından geçirip parafine gömmüş ve HE ile incelemiştir. Asistanın lipid damlacıklarını kırmızı renkte boyamak için bu parafin bloğa Oil Red O uygulayamamasının nedeni nedir?",
                    {
                        "A": "Oil Red O boyasının parafin bloklarda nükleusu tahrip etmesi",
                        "B": "Rutin takepteki alkol ve ksilenin dokudaki tüm nötral lipidleri çözüp yok etmiş olması",
                        "C": "Parafinin sadece elektron mikroskobu için uygun olması",
                        "D": "Oil Red O'nun sadece formalin içinde aktifleşen bir boya olması",
                        "E": "Karaciğer dokusunun hiçbir boyayı tutmaması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Nükleusun tahrip olmasıyla ilgisi yoktur.",
                        "B": "Doğru. Rutin takipteki etanol ve ksilen organik solventlerdir; nötral yağları eritip uzaklaştırır.",
                        "C": "Yanlış. Parafin ışık mikroskopisinin standart gömme ortamıdır.",
                        "D": "Yanlış. Oil Red O dondurulmuş kesitlerde doğrudan uygulanan boyadır.",
                        "E": "Yanlış. Karaciğer parankimi boyaları çok iyi tutar."
                    }
                ),
                make_cloze(
                    "Dokulardaki nötral lipidlerin erimeden gösterilebilmesi için dondurulmuş kesitlerde Oil Red O boyası kullanılır.",
                    "Oil Red O",
                    "Lipidleri kırmızı boyayan dondurulmuş kesit boyası"
                )
            ]
        },

        # Adım 57
        {
            "slideNumber": 57,
            "title": "İmmünohistokimya (İHK) Prensipleri: Antijen-Antikor Özgüllüğü",
            "subtitle": "İmmünohistokimya; doku kesitindeki hedef protein antijenlerini işaretli monoklonal antikorlar ve kromojen reaksiyonuyla mikroskopta görünür kılar.",
            "badge": "İmmünohistokimya",
            "badgeColor": "purple",
            "discipline": "İmmünohistokimya",
            "synthesisNarrative": """İmmünohistokimya (İHK), antijen-antikor özgüllüğü ile mikroskobik görselleştirmeyi birleştiren moleküler düzeyde bir tanı yöntemidir.

İHK protokolünde ilk adım, formalinin kapattığı epitopları ısı ve tampon solüsyonlarla açığa çıkaran ==Antijen Geri Kazanımı (Antigen Retrieval)== işlemidir. Ardından hedef doku proteinine özgül monoklonal primer antikor kesite uygulanır. Primer antikora peroksidaz (HRP) enzimi taşıyan sekonder antikorlar bağlanır. Enzim substratı olarak ==DAB (Diaminobenzidin)== eklendiğinde, antijenin bulunduğu hücresel odakta suda erimeyen kalıcı ==kahverengi çökelti== oluşur. Hedefe göre boyanma nükleer (ER), membranöz (HER2) veya sitoplazmik (sitokeratin) gerçekleşir.

> [MOLEKÜLER KURAL] İHK'da kahverengi çökelti antijen pozitifliğini, boyanmama ise hedef proteinin yokluğunu gösterir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Antijen-Antikor Özgüllüğü", "desc": "Yalnızca hedeflenen spesifik proteine bağlanan monoklonal antikorlar kullanılır.", "isKey": True},
                    {"title": "DAB Kromojeni", "desc": "Peroksidaz enzimiyle reaksiyona girerek antijen bölgesinde kahverengi çökelti yapar.", "isKey": True},
                    {"title": "Lokalizasyon Tipleri", "desc": "Boyanma hedefin türüne göre nükleer (ER/PR), membranöz (HER2) veya sitoplazmik (Sitokeratin) olabilir.", "isKey": False}
                ],
                "table": {
                    "title": "İmmünohistokimyasal Boyanma Paternleri ve Örnekleri",
                    "headers": ["Boyanma Paterni", "Hücresel Lokalizasyon", "Klasik Belirteç Örneği", "Klinik Anlamı"],
                    "rows": [
                        ["Nükleer", "Yalnızca hücre çekirdeğinde kahverengi halka/dolgu", "Östrojen Reseptörü (ER), Ki-67, TTF-1", "Hormon duyarlılığı ve proliferasyon hızı"],
                        ["Membranöz", "Hücre zarı boyunca kesintisiz kahverengi çerçeve", "HER2 (c-erbB2), CD20, E-kaderin", "Hedefe yönelik antikor tedavisi (Trastuzumab)"],
                        ["Sitoplazmik", "Tüm sitoplazma alanında diffüz kahverengi granüller", "Sitokeratin (CK), Desmin, Vimentin", "Tümörün köken aldığı doku tipi (epitelyal/mezenkimal)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İmmünohistokimyada peroksidaz enzimi substratı olarak en sık kullanılan ve kahverengi çökelti veren kromojen DAB (Diaminobenzidin)'dir.",
                "📌 [SINAV SPOTU] Formalin fiksasyonunun kapattığı epitopları antikorun bağlanabilmesi için açığa çıkarma işlemine 'Antijen Geri Kazanımı' (Antigen Retrieval) denir.",
                "💡 [ÖĞRENME İPUCU] İHK boyamasında pozitif kontrol lamı (antijeni kesin içeren doku) kullanılmadan negatif rapor verilemez."
            ],
            "medicalTerms": [
                {"term": "İmmünohistokimya (İHK)", "explanation": "Hedef proteinlerin işaretli antikor ve kromojen reaksiyonuyla mikroskopta gösterilmesidir."},
                {"term": "DAB (Diaminobenzidin)", "explanation": "Peroksidaz enzimiyle reaksiyona girerek kalıcı kahverengi çökelti oluşturan kromojendir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İmmünohistokimyasal Boyama Basamakları Zinciri",
                    [
                        "1. Deparafinizasyon: Kesit ksilenden geçirilerek parafinden arındırılır ve suya indirilir.",
                        "2. Antijen Geri Kazanımı: Isı ve tamponla formalinin kapattığı protein epitopları açığa çıkarılır.",
                        "3. Primer Antikor: Hedef doku proteinine özgül monoklonal antikor kesite inkübe edilir.",
                        "4. Sekonder Antikor: Primer antikora bağlanan peroksidaz işaretli sekonder antikor eklenir.",
                        "5. Kromojen Reaksiyonu: DAB eklenerek antijen bölgesinde kalıcı kahverengi çökelti oluşturulur."
                    ]
                ),
                make_micro_quiz(
                    "İmmünohistokimyasal boyamada formalinin doku proteinlerinde oluşturduğu çapraz bağları çözerek antikorların bağlanacağı epitopları açığa çıkarma işlemine ne ad verilir?",
                    {
                        "A": "Doku takibi",
                        "B": "Şeffaflaştırma",
                        "C": "Antijen Geri Kazanımı (Antigen Retrieval)",
                        "D": "Mikrotomi",
                        "E": "Otoliz"
                    },
                    "C",
                    {
                        "A": "Yanlış. Doku takibi fiksasyondan bloklamaya uzanan süreçtir.",
                        "B": "Yanlış. Şeffaflaştırma ksilende gerçekleştirilen basamaktır.",
                        "C": "Doğru. Antijen geri kazanımı ısı veya enzimle epitopları antikora hazır hale getirir.",
                        "D": "Yanlış. Mikrotomi mikron düzeyinde kesit alma işlemidir.",
                        "E": "Yanlış. Otoliz hücrelerin kendi enzimiyle çürümesidir."
                    }
                ),
                make_cloze(
                    "İmmünohistokimyada peroksidaz enzimiyle reaksiyona girerek antijenin bulunduğu odakta kahverengi çökelti oluşturan kromojen maddeye DAB adı verilir.",
                    "DAB",
                    "Kahverengi çökelti veren kromojenin kısaltması"
                )
            ]
        },

        # Adım 58
        {
            "slideNumber": 58,
            "title": "İHK'nın Onkolojideki Rolü: Tümör Kökeni, Reseptörler ve Ki-67",
            "subtitle": "İHK panelleri; metastatik kitlelerin kökenini belirler, hormon reseptörlerini (ER/PR/HER2) gösterir ve Ki-67 ile tümörün bölünme hızını ölçer.",
            "badge": "Onkolojik İHK",
            "badgeColor": "red",
            "discipline": "Onkolojik Patoloji",
            "synthesisNarrative": """Modern onkolojide tümör tanısı, köken tayini ve tedavi planlaması immünohistokimyasal belirteç panellerine dayanır.

İHK panelleri üç temel alanda yön belirler: ==Histogenetik köken== tayininde epitel için ==Sitokeratin== (karsinom), mezenkim için ==Vimentin== (sarkom), lenfoid seri için ==CD45== ve melanositler için ==S100== kullanılır. ==Prediktif belirteçler== olarak meme karsinomunda ==ER/PR== hormon duyarlılığını, ==HER2== ise hedefe yönelik trastuzumab yanıtını öngörür. Nükleer bir protein olan ==Ki-67 proliferasyon indeksi== ise hücre siklusundaki çoğalan hücre oranını belirleyerek tümörün büyüme hızını ve klinik agresifliğini gösterir.

> [ONKOLOJİK KURAL] Karsinom sitokeratin, sarkom vimentin, lenfoma CD45, melanom S100 pozitiftir; Ki-67 ise çoğalma hızını verir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Köken Ayrımı", "desc": "Sitokeratin (karsinom), Vimentin (sarkom), CD45 (lenfoma), S100 (melanom).", "isKey": True},
                    {"title": "Meme Paneli (ER/PR/HER2)", "desc": "Hormonoterapi ve biyolojik hedefe yönelik tedavi seçimini belirler.", "isKey": True},
                    {"title": "Ki-67 Proliferasyon İndeksi", "desc": "Tümörün aktif mitoz ve çoğalma fraksiyonunu nükleer boyamayla ölçer.", "isKey": False}
                ],
                "table": {
                    "title": "Onkolojik İmmünohistokimya Tanı Paneli",
                    "headers": ["İHK Belirteci", "Boyanma Niteliği", "Pozitif Olduğu Tümör Grubu", "Klinik Karar"],
                    "rows": [
                        ["Pan-Sitokeratin (CK)", "Sitoplazmik", "Karsinomlar (Epitelyal tümörler)", "Karsinom protokolü tedavisi uygulanır"],
                        ["Vimentin", "Sitoplazmik", "Sarkomlar (Mezenkimal tümörler)", "Yumuşak doku sarkom protokolü uygulanır"],
                        ["LCA (CD45)", "Membranöz", "Lenfomalar ve Lösemiler", "Hematoloji/Onkoloji kemoterapisi planlanır"],
                        ["S100 / Melan-A", "Nükleer & Sitoplazmik", "Malign Melanom", "İmmünoterapi ve cerrahi sınır genişletmesi"],
                        ["Ki-67", "Nükleer", "Tüm proliferatif malign tümörler", "Tümörün agresiflik derecesi ve kemoterapi duyarlılığı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İHK'da Sitokeratin epitel kökenli karsinomları; Vimentin mezenkimal kökenli sarkomları; LCA (CD45) lenfoid tümörleri gösterir.",
                "📌 [SINAV SPOTU] Ki-67 nükleer antijeni, hücre siklusunun G0 fazı dışındaki tüm aktif bölünen hücreleri boyayarak proliferasyon fraksiyonunu verir.",
                "💡 [ÖĞRENME İPUCU] Karaciğerde kitle saptandığında sitokeratin 7 ve 20 profili tümörün akciğerden mi yoksa kolondan mı metastaz yaptığını belirler."
            ],
            "medicalTerms": [
                {"term": "Sitokeratin", "explanation": "Epitelyal hücrelerin iskeletinde bulunan ve karsinom tanısında kullanılan ara filamandır."},
                {"term": "Ki-67 İndeksi", "explanation": "Hücre döngüsündeki bölünen hücreleri nükleer boyamayla ölçen proliferasyon belirtecidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Tümör Kökeni İHK Belirteç Eşleştirmesi",
                    ["Tümör Grubu", "Pozitif İHK Belirteci", "Tipik Hücresel Boyanma"],
                    [
                        [
                            ("Karsinom (Epitelyal)", False),
                            ("Sitokeratin (CK)", True, "Epitel ara filaman proteini"),
                            ("Diffüz sitoplazmik kahverengi boyanma", False)
                        ],
                        [
                            ("Sarkom (Mezenkimal)", False),
                            ("Vimentin", True, "Mezenkim ara filaman proteini"),
                            ("Sitoplazmik kahverengi boyanma", False)
                        ],
                        [
                            ("Malign Melanom", False),
                            ("S100 / HMB-45", True, "Nöroektodermal melanosit proteini"),
                            ("Nükleer ve sitoplazmik boyanma", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Karın içi kitle biyopsisinde ışık mikroskobunda malign hücreler izlenmiş ancak tümörün tipi ayırt edilememiştir. Yapılan İHK incelemesinde tümör hücrelerinin Sitokeratin pozitif, Vimentin negatif ve CD45 negatif olduğu saptanmıştır. Bu tümörün histogenetik kökeni hangisidir?",
                    {
                        "A": "Mezenkimal kökenli Sarkom",
                        "B": "Hematopoietik kökenli Malign Lenfoma",
                        "C": "Epitelyal kökenli Karsinom",
                        "D": "Sinir kılıfı kökenli Schwannom",
                        "E": "Melanositik kökenli Malign Melanom"
                    },
                    "C",
                    {
                        "A": "Yanlış. Sarkomlar vimentin pozitif, sitokeratin negatif boyanır.",
                        "B": "Yanlış. Malign lenfomalar CD45 (LCA) pozitifliği gösterir.",
                        "C": "Doğru. Sitokeratin epitel ara filamanıdır; sitokeratin pozitifliği karsinomu kanıtlar.",
                        "D": "Yanlış. Schwannomlar nöral kökenli olup S100 pozitiftir.",
                        "E": "Yanlış. Melanomlar S100 ve HMB45 pozitif boyanır."
                    }
                ),
                make_cloze(
                    "Malign tümörlerde hücre döngüsünün G0 fazı dışındaki tüm çoğalan hücreleri çekirdekte boyayarak proliferasyon hızını ölçen belirteç Ki-67 olarak bilinir.",
                    "Ki-67",
                    "Nükleer proliferasyon belirtecinin adı"
                )
            ]
        },

        # Adım 59: [TEKRAR SAYFASI - CHECKPOINT 6]
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Tanısal Araçlar, Boyama Teknikleri ve İHK Panelleri",
            "subtitle": "Bölüm 6'nın makroskopi, ışık mikroskopisi, rutin HE, özel histokimya (Prusya, PAS, Trikrom, Oil Red O) ve İHK konularını sentezleyen kritik istasyon.",
            "badge": "Checkpoint 6",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 6,
            "synthesisNarrative": """Tanısal patoloji süreci; makroskobik örneklemeden histokimyasal boyalara ve moleküler İHK panellerine uzanan entegre bir bütündür.

Makroskopi ve doğru örnekleme mikroskobik tanının temelini oluşturur. Rutin ==Hematoksilen-Eozin (HE)== nükleusu mor-maviye (bazofili), sitoplazmayı pembeye (eozinofili) boyayarak doku mimarisini kurar. Özel histokimyada ==Prusya mavisi== demiri (mavi), ==PAS== glikojen ve mantarları (macenta), ==Masson trikrom== kollajeni (mavi), dondurulmuş kesitte ==Oil Red O== ise lipidleri (kırmızı) gösterir. İmmünohistokimyada ise ==Sitokeratin== karsinomu, ==Vimentin== sarkomu, ==CD45== lenfomayı saptarken ==Ki-67== çoğalma hızını belirler.

> [BÖLÜM ÖZETİ] Tanı basamakları: Makroskopi ve HE ile doku yapısı → Özel histokimya ile birikimler → İHK ile hücresel köken ve tedavi hedefleri.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "HE Bazofili/Eozinofili", "desc": "Hematoksilen asit nükleusu mavi-mora, eozin bazik sitoplazmayı pembeye boyar.", "isKey": True},
                    {"title": "Özel Boya Dörtlüsü", "desc": "Prusya (demir/mavi), PAS (glikojen/macenta), Trikrom (kollajen/mavi), Oil Red O (lipid/kırmızı).", "isKey": True},
                    {"title": "İHK Paneli", "desc": "Sitokeratin (karsinom), Vimentin (sarkom), ER/PR/HER2 (meme), Ki-67 (çoğalma hızı).", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 6 Özel Boyalar ve İHK Belirteçleri Sentez Tablosu",
                    "headers": ["Boya / Belirteç", "Hedeflenen Madde / Yapı", "Verdiği Renk", "Klinikopatolojik Endikasyon"],
                    "rows": [
                        ["Hematoksilen (HE)", "Nükleik asitler (DNA/RNA)", "Mavi - Mor", "Rutin mikroskopi, nükleus atipisi ve nükleol değerlendirmesi"],
                        ["Eozin (HE)", "Sitoplazmik proteinler, kollajen", "Pembe - Kırmızı", "Sitoplazma sınırı, kas lifleri, nekroz eozinofilisinin tespiti"],
                        ["Prusya Mavisi (Perls)", "Hemosiderin, ferrik demir ($Fe^{3+}$)", "Parlak Mavi", "Hemokromatozis, kalp yetmezliği hücreleri, sideroblastik anemi"],
                        ["PAS (Periyodik Asit-Schiff)", "Glikojen, bazal membran, mantar", "Macenta (Eflatun)", "Diyabetik nefropati, Candida hifleri, glikojenozis"],
                        ["Masson Trikrom", "Tip I/III Kollajen lifleri", "Parlak Mavi (veya Yeşil)", "Karaciğer sirozu evrelemesi, miyokard enfarktüs skarı"],
                        ["Oil Red O", "Nötral lipidler (Dondurulmuş kesit)", "Parlak Kırmızı", "Hepatosteatoz, yağ embolisi sendromu, liposarkom"],
                        ["Sitokeratin (CK)", "Epitelyal ara filamanlar", "Kahverengi (İHK)", "Karsinomların tanısı ve metastaz odağının bulunması"],
                        ["Ki-67", "Nükleer proliferasyon antijeni", "Kahverengi Nükleer (İHK)", "Tümörlerin büyüme hızı ve histolojik agresiflik indeksi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Dokuda lipidler parafin takibinde ksilende eridiği için Oil Red O boyası sadece taze dondurulmuş (frozen) kesitte yapılabilir.",
                "📌 [SINAV SPOTU] Karaciğer biyopsisinde sirotik köprüleşme fibrozisini gösteren boya Masson Trikrom; demir birikimini gösteren boya Prusya Mavisidir.",
                "📌 [SINAV SPOTU] Sitokeratin karsinomları, Vimentin sarkomları, CD45 lenfomaları boyar; Ki-67 proliferasyon fraksiyonunu verir."
            ],
            "medicalTerms": [
                {"term": "DAB Kromojeni", "explanation": "İHK'da peroksidaz enzimiyle suda çözünmeyen kahverengi çökelti oluşturan kromojendir."},
                {"term": "Antijen Geri Kazanımı", "explanation": "Formalinin kapattığı epitopları ısıyla açarak antikor bağlanmasını sağlayan işlemdir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p6-1",
                    "Rutin Hematoksilen-Eozin (HE) boyasında hücre çekirdeğinin mavi-mor, sitoplazmanın pembe boyanmasının biyokimyasal mekanizması nedir?",
                    "Hematoksilen bazik bir boyadır; hücre çekirdeğindeki negatif yüklü asidik nükleik asitlere (DNA/RNA) bağlanarak onları mavi-mor boyar (bazofili). Eozin ise asidik bir boyadır; sitoplazmadaki pozitif yüklü bazik proteinlere bağlanarak sitoplazmayı pembeye boyar (eozinofili).",
                    "Bazofili (nükleus) vs Eozinofili (sitoplazma)",
                    "Histokimya"
                ),
                make_flashcard(
                    "fc-p6-2",
                    "Dokulardaki nötral lipidleri (yağları) göstermek için neden rutin parafin blok kullanılamaz ve hangi yöntem zorunludur?",
                    "Çünkü rutin parafin takip basamaklarında kullanılan alkol ve ksilen gibi organik solventler hücre içindeki tüm lipidleri eritip yıkar ve geride boşluk bırakır. Bu nedenle doku dondurulmalı (kriostat frozen kesit) ve çözücüye sokulmadan Oil Red O veya Sudan Siyahı ile boyanmalıdır.",
                    "Ksilen erimesi ve dondurulmuş kesit şartı",
                    "Özel Histokimya"
                ),
                make_flashcard(
                    "fc-p6-3",
                    "İmmünohistokimyada (İHK) Sitokeratin, Vimentin ve Ki-67 belirteçlerinin onkolojideki temel tanısal rolleri nelerdir?",
                    "Sitokeratin epitel kökenli karsinomları boyar. Vimentin mezenkimal kökenli sarkomları boyar. Ki-67 ise hücre döngüsünün G0 dışındaki evrelerinde bulunan bölünen hücrelerin çekirdeğini boyayarak tümörün proliferasyon (büyüme) hızını ve agresifliğini belirler.",
                    "Karsinom, sarkom ve nükleer proliferasyon",
                    "Onkolojik İHK"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 6'da incelenen özel boyalar ve tanısal yöntemler dikkate alındığında, aşağıdaki klinik durum - histokimyasal boya eşleştirmelerinden hangisi YANLIŞTIR?",
                    {
                        "A": "Kronik hepatitte karaciğer sirozunun ve köprüleşme fibrozisinin gösterilmesi → Masson Trikrom",
                        "B": "Kronik akciğer konjesyonunda hemosiderin yüklü makrofajların saptanması → Prusya Mavisi",
                        "C": "Karaciğer biyopsisinde nötral lipidlerin gösterilmesi → Dondurulmuş kesitte Oil Red O",
                        "D": "Özofagus biyopsisinde Candida mantar hiflerinin gösterilmesi → Periyodik Asit - Schiff (PAS)",
                        "E": "Malign tümörde proliferasyon hızının ve çoğalan hücre yüzdesinin ölçülmesi → Vimentin İmmünohistokimyası"
                    },
                    "E",
                    {
                        "A": "Doğru. Masson trikrom kollajen liflerini maviye boyar.",
                        "B": "Doğru. Prusya mavisi hemosiderin demirini maviye boyar.",
                        "C": "Doğru. Nötral lipidler dondurulmuş kesitte Oil Red O ile boyanır.",
                        "D": "Doğru. PAS mantar hücre duvarını macenta renge boyar.",
                        "E": "Yanlış (aranan cevap): Proliferasyon hızını ölçen nükleer belirteç Ki-67'dir; Vimentin sarkom belirtecidir."
                    }
                ),
                make_interactive_table(
                    "Tanısal Boyalar ve Biyomoleküler Hedefleri",
                    ["Özel Yöntem", "Kimyasal Hedef", "Tanısal Renk"],
                    [
                        [
                            ("Prusya Mavisi (Perls)", False),
                            ("Ferrik Demir iyonları ($Fe^{3+}$)", True, "Hemosiderin ve ferritin tespiti"),
                            ("Parlak Mavi renk oluşumu", False)
                        ],
                        [
                            ("PAS Boyası", False),
                            ("1,2-glikol karbonhidrat grupları", True, "Bazal membran ve mantar duvarı"),
                            ("Parlak Macenta / Eflatun renk", False)
                        ],
                        [
                            ("Masson Trikrom", False),
                            ("Ekstraselüler kollajen lifleri", True, "Fibrozis ve sirotik bantlar"),
                            ("Parlak Mavi / Yeşil renk", False)
                        ]
                    ]
                )
            ]
        }
    ]
