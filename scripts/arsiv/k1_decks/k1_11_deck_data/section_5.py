# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-11-s41",
        "title": "Glomerüler Hemodinami: Starling Kuvvetleri ve Normal Basınçlar",
        "content": "Glomerüler ultrafiltrasyon, glomerül kapiller duvarı boyunca etki eden fiziksel hidrostatik ve onkotik kuvvetlerin (Starling kuvvetleri) hassas dengesiyle yürütülür:\n\n- **Glomerül İçi Hidrostatik Basınç (Pgc):** Sistemik ortalama arteriyel kan basıncının yaklaşık %60'ına denk gelir ve normal bir bireyde yaklaşık **70 mmHg** düzeyindedir. Filtrasyonu Bowman boşluğuna doğru iten temel kuvvettir.\n- **Plazma Kapiller Onkotik Basıncı (πgc):** Glomerül lümenindeki plazma proteinlerinin oluşturduğu çekme kuvvetidir ve normalde **25-30 mmHg** aralığındadır. Sıvıyı kapiller içinde tutmaya çalışır.\n- **Bowman Kapsülü İçi Hidrostatik Basınç (Pbs):** Bowman aralığındaki sıvının oluşturduğu karşı dirençtir ve normal koşullarda **10-15 mmHg** civarındadır.\n\nNet Efektif Filtrasyon Basıncı (EFP) = Pgc - (πgc + Pbs) formülüyle hesaplanır ve normalde 15-20 mmHg net ileri yönde filtrasyon kuvveti üretir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Starling Kuvveti", "Normal Basınç Değeri", "Filtrasyona Yönelik Etkisi"],
                [
                    [
                        {"text": "Glomerül İçi Hidrostatik Basınç", "isMasked": False, "hint": ""},
                        {"text": "Yaklaşık 70 mmHg (Sistemik basıncın %60'ı)", "isMasked": True, "hint": "Filtrasyonu iten ana hidrostatik güç"},
                        {"text": "Filtrasyonu Bowman boşluğuna doğru iter", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kapiller Onkotik Basınç", "isMasked": False, "hint": ""},
                        {"text": "25-30 mmHg", "isMasked": True, "hint": "Plazma proteinlerinin oluşturduğu ozmotik güç"},
                        {"text": "Filtrasyona karşı koyar, sıvıyı damarda tutar", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Bowman Kapsülü İçi Basınç", "isMasked": False, "hint": ""},
                        {"text": "10-15 mmHg", "isMasked": True, "hint": "Tübül lümeninin glomerüle uyguladığı geri basınç"},
                        {"text": "Filtrasyona karşı koyar", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Normal bir böbrekte glomerül içi hidrostatik basınç sistemik arteriyel basıncın yaklasık yüzde altmısına denk gelir.",
                "yüzde altmısına",
                "Yüzde altmış oranındaki fraksiyonu anımsayınız"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-11-s42",
        "title": "Efektif Filtrasyon Basıncı ve Stop Flow Pressure Kavramı",
        "content": "Glomerüler filtrasyon hızını (GFR) sıfıra indiren iki temel patolojik durum mevcuttur:\n\n1. **Sistemik Hipotansiyon:** Sistemik ortalama arteriyel basınç 70 mmHg'nın altına düştüğünde, glomerül içi hidrostatik basınç (Pgc) onkotik basınç ve bazal tübüler direncin toplamını yenemez hale gelir ve filtrasyon durur (GFR = 0).\n2. **Tübüler Geri Basınç Artışı (Stop Flow Pressure):** Üriner traktusta bir obstrüksiyon geliştiğinde, proksimalde göllenen idrar hidrostatik basıncı retrograd olarak toplayıcı tübüllere, Henle kulpuna, proksimal tübüle ve en nihayetinde Bowman kapsülüne iletir. Bowman kapsülü içi hidrostatik basınç (Pbs) yükselerek Pgc - πgc farkına eşitlendiğinde net filtrasyon basıncı sıfırlanır. Ultrafiltrasyonun tamamen durduğu bu kritik intralüminal basınca 'Stop Flow Pressure (Durdurma Basıncı)' adı verilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Filtrasyonun Durma Mekanizmaları Karşılaştırması",
                "Sistemik Hipotansiyon (Arter Basıncı < 70 mmHg)",
                "Glomerül kapiller hidrostatik basıncı düşer; ileri itici kuvvet yetersiz kalarak GFR sıfırlanır.",
                "Stop Flow Pressure (Obstrüktif Basınç)",
                "Bowman kapsülü içi hidrostatik basınç aşırı yükselir; karşı direnç itici güce eşitlenerek GFR sıfırlanır."
            ),
            make_recall(
                "Obstrüksiyon sonucu Bowman kapsülü içi hidrostatik basıncın yükselerek net filtrasyonu tamamen durdurduğu basınca ne ad verilir?",
                "Stop flow pressure (durdurma basıncı).",
                "Filtrasyon akımını sıfırlayan kritik intralüminal basınç"
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-11-s43",
        "title": "Akut Üreter Obstrüksiyonunda Bifazik Hemodinamik Yanıt",
        "content": "Akut tek taraflı tam üreter obstrüksiyonu geliştiğinde böbrek hemodinamiği zaman içinde birbirine zıt iki ayrı fazdan geçer (bifazik yanıt):\n\n- **Erken Faz (İlk 1-2 Saat):** Üreter lümenindeki ani tıkanıklık intrapelvik basıncı artırır. Böbrek filtrasyonu sürdürebilmek için otoregülatuvar bir savunma başlatır: Aferent arteriyollerde belirgin vazodilatasyon gelişir. Bu sayede renal kan akımı (RBF) ve glomerül içi hidrostatik basınç geçici olarak artar.\n- **Geç Faz (2-5 Saat Sonrası ve Kronikleşme):** Sürekli yüksek tübüler basınca maruz kalan dokularda potent vazokonstriktör ajanlar salgılanmaya başlar. Aferent arteriyolde başlayan ve giderek eferent damarlara da yayılan şiddetli vazokonstriksiyon gelişir. Renal kan akımı (RBF) ve glomerül içi basınç hızla düşüşe geçer; böbrek parankimi progresif iskemiye sürüklenir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Obstrüksiyonda Bifazik Hemodinamik Seyir",
                [
                    "1. Akut Tıkanma: İntralüminal hidrostatik basıncın aniden tepe yapması",
                    "2. Erken Vazodilatasyon (0-2 saat): Aferent arteriyol dilatasyonu ile RBF ve Pgc artışı",
                    "3. Vazokonstriktör Hakimiyet: TXA2 ve Anjiyotensin II salınımının başlaması",
                    "4. Geç İskemik Faz (2 saat sonrası): Şiddetli vazokonstriksiyon ile RBF ve GFR'de çöküş"
                ]
            ),
            make_quiz(
                "Akut üreter obstrüksiyonunun ilk 1-2 saatlik erken fazında renal kan akımının (RBF) ve glomerül basıncının geçici olarak artmasını sağlayan temel hemodinamik değişiklik hangisidir?",
                [
                    {"key": "A", "text": "Aferent arteriyolde belirgin vazodilatasyon gelişmesi", "explanation": "A seçeneği doğrudur: İlk 1-2 saatte lokal mediyatörlerle aferent damar genişler ve kan akımı artar."},
                    {"key": "B", "text": "Eferent arteriyolün tamamen gevşeyip basıncı sıfırlaması", "explanation": "B seçeneği yanlıştır: Eferent dilatasyon glomerül basıncını düşürürdü."},
                    {"key": "C", "text": "Sistemik kan basıncının şok düzeyine inmesi", "explanation": "C seçeneği yanlıştır: Bu filtrasyonu durdurur."},
                    {"key": "D", "text": "Toplayıcı tübüllerdeki tüm kolajen liflerinin erimesi", "explanation": "D seçeneği yanlıştır: Kolajen erken saatlerde erimez."},
                    {"key": "E", "text": "Renal venin lümeninin tamamen tıkanması", "explanation": "E seçeneği yanlıştır: Renal ven trombozu patolojisidir, normal bifazik yanıt değildir."}
                ],
                "A"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-11-s44",
        "title": "Erken Evre Vazoaktif Mediyatörler: Prostaglandin E2 ve Nitrik Oksit",
        "content": "Akut obstrüksiyonun erken fazındaki aferent arteriyol vazodilatasyonunu yöneten temel moleküler oyuncular vazodilatatör prostaglandinler ve nitrik oksittir (NO). Tübüler basınç artışına bağlı gerilme, renal medüller ve kortikal hücrelerde siklooksijenaz-2 (COX-2) enzimini uyarır; lokal olarak yüksek miktarda **Prostaglandin E2 (PGE2)** ve Prostasiklin (PGI2) sentezlenir. Eş zamanlı olarak vasküler endotelden **Nitrik Oksit (NO)** salınır. PGE2 ve NO doğrudan aferent arteriyol düz kaslarını gevşeterek renal kan akımını artırır ve glomerüler filtrasyon basıncını korumaya çalışır. Bu nedenle, akut renal kolik atağı geçiren bir hastaya Non-Steroid Antiinflamatuar İlaç (NSAİİ) verildiğinde, COX inhibisyonu ile PGE2 sentezi baskılanır; aferent damar genişleyemez, renal kan akımı ve pelvik basınç düşer ve böylece hastanın ağrısı hızla rahatlar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Akut obstrüksiyonun erken evresinde aferent arteriyol vazodilatasyonunu saglayan temel vazodilatatör moleküller PGE2 ve nitrik oksittir.",
                "PGE2 ve nitrik oksittir",
                "Prostasiklin ailesi üyesi ve endotelyal gaz mediyatör"
            ),
            make_branching(
                "Acil servise şiddetli akut renal kolik tablosuyla başvuran bir hastaya kas içine diklofenak sodyum (NSAİİ) enjeksiyonu yapılıyor ve 20 dakika içinde hastanın böğür ağrısı belirgin şekilde geriliyor.",
                "Bu analjezik etkinin altındaki primer vazoaktif ve hemodinamik mekanizma hangisidir?",
                [
                    {
                        "text": "COX inhibisyonu ile PGE2 sentezi baskılanır; aferent arteriyol vazodilatasyonu kırılarak intrapelvik hidrostatik basınç düşürülür.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. NSAİİ'ler PGE2 sentezini keserek böbrek içi vazodilatasyonu ve toplayıcı sistem gerilimini azaltır."
                    },
                    {
                        "text": "Üreter taşını kimyasal olarak eriterek idrar akımını anında açar.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. NSAİİ taşı eritmez; pelvik basıncı ve gerilmeyi azaltarak ağrıyı keser."
                    },
                    {
                        "text": "Mesane kapasitesini beş katına çıkararak geri akımı emer.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. İlacın mesane kapasitesini katlama etkisi yoktur."
                    }
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-11-s45",
        "title": "Geç Evre Vazoaktif Değişiklikler: Tromboksan A2 ve Anjiyotensin II",
        "content": "Obstrüksiyonun 4-5. saatlerinden itibaren vazoaktif denge vazokonstriktör mediyatörlerin lehine bozulur. İnfiltrasyon yapan mononükleer inflamatuar hücreler ve aktive olan renal tübül hücreleri yüksek miktarda **Tromboksan A2 (TXA2)** sentezler. Eş zamanlı olarak lokal Renin-Anjiyotensin-Aldosteron Sistemi (RAAS) aşırı aktive edilerek **Anjiyotensin II (Ang II)** ve endotelin seviyeleri tavan yapar. TXA2 ve Anjiyotensin II, renal damar yatağında çok şiddetli bir vazokonstriksiyona neden olur. Bu konstriksiyon hem preglomerüler aferent hem de postglomerüler eferent arteriyolleri sıkarak renal vasküler direnci dramatik şekilde yükseltir. Sonuç olarak glomerül kapiller basıncı çöker, renal perfüzyon dibe vurur ve böbrek dokusu hipoksiye mahkum olur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Obstrüksiyon Mediyatörleri Dengesi",
                "Erken Faz Mediyatörleri (PGE2 / NO)",
                "Aferent vazodilatasyon yapar, renal kan akımını ve intrapelvik basıncı yükseltir.",
                "Geç Faz Mediyatörleri (TXA2 / Ang II)",
                "Şiddetli renal vazokonstriksiyon yapar, renal kan akımını düşürür ve iskemi başlatır."
            ),
            make_recall(
                "Obstrüksiyonun geç evresinde renal vasküler direnci artırıp kan akımını azaltarak iskemiyi tetikleyen temel vazokonstriktör mediyatörler hangileridir?",
                "Tromboksan A2 (TXA2) ve Anjiyotensin II'dir.",
                "Trombosit kaynaklı siklooksijenaz ürünü ve temel oligopeptit hormon"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-11-s46",
        "title": "Renal Kan Akımında Progresif Azalma ve Dokusal İskemi",
        "content": "Üriner obstrüksiyonda nihai parankim yıkımının en kritik tetikleyicisi renal kan akımındaki (RBF) progresif ve sürekli azalmadır. İlk birkaç saatlik kompanzatuar dilatasyon hızla tükenir; vazokonstriktör mediyatörler ve artan interstisyel basıncın kompresyon etkisiyle renal kortikal ve medüller kan akımı normalin %20-30'una kadar gerileyebilir. Dokusal perfüzyonun çökmesi böbrek parankiminde derin bir hücresel hipoksi ve iskemi tablosu yaratır. Özellikle metabolik olarak son derece aktif olan ve yüksek oksijen tüketen proksimal tübül epiteli ile Henle kulpunun kalın çıkan kolu iskemik hasara karşı en duyarlı segmentlerdir. İskemi ATP tükenmesine, membran sodyum-potasyum pompalarının iflasına ve mitokondriyal hasara yol açarak tübüler epitel dökülmesini başlatır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Üriner obstrüksiyonun ileri döneminde parankim yıkımına baslangıctaki basınç artısından ziyade iskemi ve hemodinamik bozukluklar yol açar.",
                "iskemi ve hemodinamik bozukluklar",
                "Doku kanlanmasının çökmesi ve vasküler bozulma süreci"
            ),
            make_quiz(
                "Kronikleşen hidronefroz tablosunda parankim hasarının ve hücresel atrofisinin ilerlemesinde geç evrede en belirleyici rolü oynayan mekanizma hangisidir?",
                [
                    {"key": "A", "text": "Renal kan akımının progresif azalması sonucu gelişen derin doku iskemisi", "explanation": "A seçeneği doğrudur: Ders notunda açıkça belirtildiği üzere ileri dönemde hasardan iskemi ve hemodinamik bozukluklar sorumludur."},
                    {"key": "B", "text": "Kalsiyum kristallerinin tüm böbrek arterlerini mekanik tıkaması", "explanation": "B seçeneği yanlıştır: Arterler kristalle tıkanmaz, vazokonstriksiyon gelişir."},
                    {"key": "C", "text": "Böbrek lenf damarlarının yırtılarak kanı sulandırması", "explanation": "C seçeneği yanlıştır: Lenfatik sistem parankim iskemisinin nedeni değildir."},
                    {"key": "D", "text": "Bowman kapsülünün aşırı kalınlaşarak glomerülü ezmesi", "explanation": "D seçeneği yanlıştır: Hasar Bowman kapsülü kalınlaşmasından kaynaklanmaz."},
                    {"key": "E", "text": "Karşı böbreğin aşırı kan çekerek tek böbreği kansız bırakması", "explanation": "E seçeneği yanlıştır: Böbrekler arası kan çalma fenomeni söz konusu değildir."}
                ],
                "A"
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-11-s47",
        "title": "İnflamatuar Sitokinler ve TNF-Alfa: Apoptozdan İnterstisyel Fibrozise",
        "content": "İskemik ve mekanik gerilim altındaki böbrek hücreleri monosit kemoatraktan protein-1 (MCP-1) salgılayarak interstisyuma yoğun makrofaj ve T lenfosit göçünü uyarır. İnfiltre olan bu mononükleer hücrelerden ve hasarlı tübül epitelinden salınan en kritik proinflamatuar sitokin **Tümör Nekroz Faktörü-alfa (TNF-α)** dır. TNF-α, ölüm reseptörlerini (Fas/TNFR1) aktive ederek kaspaz kaskadını tetikler ve tübüler epitel hücrelerinde kitlesel **apoptoz** başlatır. Eş zamanlı olarak uyarılan Transforming Growth Factor-beta (TGF-β), interstisyel fibroblastları miyofibroblastlara dönüştürerek masif kollajen ve fibronektin sentezini başlatır. Apoptoza uğrayan tübüllerin yerini yoğun bağ dokusu alır; bu durum geri dönüşümsüz tubulointerstisyel fibrozis ile nefron kaybını mühürler.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "İnterstisyel Fibrozis ve Nefron Kaybı Kaskadı",
                [
                    "1. Mekanik/İskemik Stres: Tübül epitelinin hasarlanması ve kemokin salması",
                    "2. Makrofaj İnfiltrasyonu: İnterstisyuma mononükleer inflamatuar hücre göçü",
                    "3. TNF-Alfa ve TGF-Beta Salınımı: Proinflamatuar ve profibrotik sitokin fırtınası",
                    "4. Tübüler Apoptoz ve Fibrozis: Hücre ölümü ve yerini sklerotik bağ dokusunun alması"
                ]
            ),
            make_recall(
                "İskemik renal hasarda inflamatuar hücre infiltrasyonunu ve tübüler hücre apoptozunu uyararak fibrozisi tetikleyen potent sitokin hangisidir?",
                "Tümör Nekroz Faktörü-alfa (TNF-α)'dır.",
                "Klasik kaşeksi ve doku yıkımı sitokini"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-11-s48",
        "title": "Hidronefrotik Parankim Atrofisi ve Korteks İncelmesi",
        "content": "Basınç ve iskeminin aylar boyunca sürmesi böbreğin anatomik yapısında dramatik bir yıkıma yol açar. Toplayıcı sistem aşırı genişlerken böbrek parankimi medulladan başlayarak kortekse doğru kademeli olarak erir. Normalde 15-20 mm kalınlığında olan fonksiyonel renal parankim, ileri hidronefrozda **4-6 mm'ye kadar** incelir. Medüller piramitler tamamen silinir, kaliksler devasa kistik odacıklara dönüşür ve böbrek dışarıdan bakıldığında lobüle, ince cidarlı, içi idrarla dolu dev bir keseyi (hidronefrotik kese) andırır. Ağır olgularda parankimal atrofi o kadar ilerler ki mikroskobik incelemede geride neredeyse hiç sağlam glomerül ve tübül kalmaz; böbrek tamamen afonksiyonel hale gelir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Parametre", "Normal Böbrek", "İleri Hidronefroz (Atrofi)"],
                [
                    [
                        {"text": "Parankim Kalınlığı", "isMasked": False, "hint": ""},
                        {"text": "15-20 mm", "isMasked": True, "hint": "Normal korteks ve medulla toplamı"},
                        {"text": "4-6 mm'ye kadar incelmiş (kağıt gibi)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Medüller Piramitler", "isMasked": False, "hint": ""},
                        {"text": "Belirgin, üçgen biçimli piramitler", "isMasked": True, "hint": "Tübüllerin toplandığı anatomik bölge"},
                        {"text": "Tamamen düzleşmiş, silinmiş ve kaybolmuş", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Toplayıcı Sistem Mimarisi", "isMasked": False, "hint": ""},
                        {"text": "Küçük hacimli dar pelvis ve kaliksler", "isMasked": True, "hint": "Normal toplayıcı boşluk"},
                        {"text": "Dev kistik keseler haline gelmiş kaliksektazi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "İleri evre hidronefrotik renal atrofide fonksiyonel parankim kalınlığı dört ila altı milimetreye kadar incelme gösterebilir.",
                "dört ila altı milimetreye",
                "Parankim kalınlığının dramatik düştüğü milimetre aralığı"
            )
        ]
    })

    # Slide 49 (CHECKPOINT 5)
    slides.append({
        "id": "k1-11-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Glomerüler Hemodinami, Basınç Dinamikleri ve Parankim İskemisi",
        "content": "Glomerüler hemodinami ve parankimal yıkım süreçlerinin kilit ilkeleri:\n\n1. **Basınçlar:** Glomerül içi hidrostatik basınç sistemik basıncın %60'ıdır (~70 mmHg). Bowman kapsülü basıncı 10-15 mmHg'dır. Arteriyel basınç 70 mmHg altına düştüğünde veya Bowman basıncı durdurma basıncına (stop flow pressure) ulaştığında GFR=0 olur.\n2. **Bifazik Yanıt:** İlk 1-2 saatte PGE2 ve NO aracılı aferent vazodilatasyonla RBF artar. Geç evrede ise TXA2 ve Anjiyotensin II aracılı vazokonstriksiyonla RBF çöker.\n3. **İskemi ve Sitokinler:** İleri dönemde hasardan basınçtan ziyade iskemi sorumludur. TNF-α tübüler apoptozu, TGF-β ise interstisyel fibrozisi yönetir.\n4. **Parankim Atrofisi:** İleri hidronefrozda parankim 4-6 mm'ye kadar incelir; medüller piramitler silinir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Glomerüler filtrasyon hızını (GFR) sıfıra indiren basınç durumlarıyla ilgili hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "Sistemik arteriyel basıncın 70 mmHg'nın altına düşmesi GFR'yi sıfırlar.", "explanation": "A seçeneği doğrudur: Sistemik basınç 70 mmHg altına indiğinde filtrasyon durur."},
                    {"key": "B", "text": "Bowman kapsülü içi basıncın stop flow pressure değerine çıkması GFR'yi sıfırlar.", "explanation": "B seçeneği doğrudur: Karşı hidrostatik direnç itici kuvvete eşitlendiğinde filtrasyon biter."},
                    {"key": "C", "text": "Kapiller onkotik basıncın sıfıra düşmesi GFR'yi tamamen durdurur.", "explanation": "C seçeneği YANLIŞTIR: Onkotik basıncın düşmesi filtrasyonu durdurmaz, tam aksine net filtrasyon basıncını artırır."},
                    {"key": "D", "text": "Normalde glomerül içi hidrostatik basınç yaklaşık 70 mmHg'dır.", "explanation": "D seçeneği doğrudur: Sistemik basıncın yaklaşık %60'ına karşılık gelir."},
                    {"key": "E", "text": "Bowman kapsülü içi normal hidrostatik basınç 10-15 mmHg civarındadır.", "explanation": "E seçeneği doğrudur: Bazal tübüler direnç bu aralıktadır."}
                ],
                "C"
            ),
            make_recall(
                "Akut üreter obstrüksiyonunda erken fazda aferent vazodilatasyon yapan iki temel mediyatör nedir?",
                "PGE2 (Prostaglandin E2) ve Nitrik Oksittir (NO).",
                "İki majör erken vazodilatatör ajan"
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-11-s50",
        "title": "Obstrüksiyon Seviyesinin Parankimal Hasara Etkisi",
        "content": "Obstrüksiyonun üriner traktus boyunca yerleştiği anatomik seviye böbrek parankiminin maruz kalacağı hasarın hızını ve şiddetini belirler. Eğer tıkanıklık üreteropelvik bileşke (UPJ) gibi en üst seviyede ise, arada tampon görevi görecek hiçbir kompliyan üreter segmenti bulunmadığından basınç artışı saniyeler içinde doğrudan kalikslere ve renal parankime yansır; bu nedenle UPJ darlıklarında parankim atrofisi en hızlı gelişir. Buna karşılık, üreterovezikal bileşke (UVJ) düzeyindeki distal obstrüksiyonlarda 25-30 cm uzunluğundaki üreter lümeni bir rezervuar gibi esneyip genişleyerek (hidroüreter) basıncı bir süre sönümler ve böbreğe basınç iletimini geciktirir. Pelvis tipi de önemlidir: İntrarenal pelviste basınç doğrudan parankimi ezerken, ekstrarenal pelvis dışa doğru balonlaşarak parankimi koruyucu bir emniyet sübabı oluşturur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Pelvis Tiplerinin Basınç İletimine Etkisi",
                "İntrarenal Pelvis",
                "Tamamen parankim içinde gömülüdür; balonlaşamaz, yüksek basıncı doğrudan böbreğe iletir.",
                "Ekstrarenal Pelvis",
                "Böbrek dışına doğru serbestçe genişleyebilir; hacmi emerek parankimi bir süre korur."
            ),
            make_cloze(
                "Böbrek parankimi içinde gömülü olan intrarenal pelvis tipi yüksek basıncı doğrudan dokuya ileterek hasarı hızlandırır.",
                "intrarenal pelvis",
                "Böbrek sinüsü içine hapsolmuş pelvis anatomik varyantı"
            )
        ]
    })

    return slides
