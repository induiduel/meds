# sec8.py
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec8():
    slides = []
    
    # Slide 71
    slides.append(
        make_slide(
            title="Sifiliz Tanısında Karanlık Saha Mikroskobisi ve Endikasyonları (Şankr, Kondiloma Lata)",
            narrative="""Treponema pallidum, çok ince bir spiral bakteri olduğu için standart Gram boyası veya ışık mikroskobuyla doğrudan görülemez. Sifilizin erken evrelerinde kesin ve en hızlı tanı yöntemi, spiroketlerin hareketini canlı olarak gösteren **karanlık saha mikroskobisi**dir (dark-field microscopy).

Karanlık saha incelemesi, aktif ve eksüda salgılayan lezyonların olduğu **primer (şankr)** ve **sekonder (kondiloma lata)** dönemlerde en değerlidir. Bu dönemlerde lezyonlar çok sayıda spiroket içerir. Zemin karanlık görünürken, ışığı yansıtan tirbuşon şeklindeki canlı treponemaların ileri-geri ve kendi etrafında dönme hareketleri net bir şekilde izlenebilir.

> Karanlık saha, antikorların henüz pozitifleşmediği erken primer evrede (seronegatif pencere dönemi) hayat kurtarıcı bir kesin tanı aracıdır.""",
            interactions=[
                make_cloze("T. pallidum çok ince olduğundan ışık mikroskobu yerine {{karanlık saha}} mikroskobisi ile incelenir."),
                make_recall("Karanlık saha incelemesi en çok hangi lezyonlardan (primer ve sekonder) alınan örneklerde başarılıdır?", "Şankr ve kondiloma lata."),
                make_quiz(
                    "Bir hastada şüpheli genital ülser çıkalı 3 gün olmuştur ve serolojik testler henüz negatiftir. Kesin tanı için en uygun yöntem hangisidir?",
                    ["Kültürde üreme beklemek", "Karanlık saha mikroskobisi", "Gram boyama", "Tzanck preparatı", "BOS analizi"],
                    1,
                    "Doğru. Antikorlar oluşmadan önceki erken şankr döneminde en iyi yöntem lezyondan alınan örneğin karanlık sahada incelenmesidir."
                ),
                make_cloze("Karanlık saha mikroskobisinde bakteriler canlıdır ve {{tirbuşon}} benzeri (spiral) hareketleri gözlemlenir.")
            ]
        )
    )

    # Slide 72
    slides.append(
        make_slide(
            title="Karanlık Saha Mikroskobisinde Örnek Alma Tekniği ve Seröz Eksuda",
            narrative="""Karanlık saha için örnek alınırken dikkatli olunmalıdır. Lezyon (örneğin şankr) yüzeyi hafifçe serum fizyolojik ile temizlenir, kabuk varsa kaldırılır. Ardından lezyon kenarları hafifçe sıkılarak berrak bir **seröz eksuda** çıkması sağlanır. Çıkan bu eksuda lama alınarak hemen, kurumadan incelenmelidir.

Kanlı bir örnek almaktan kaçınılmalıdır, çünkü yoğun kırmızı kan hücreleri karanlık sahada spiroketlerin görülmesini engeller ve yalancı negatifliğe yol açar. Ayrıca, ağız içi lezyonlardan alınan örneklerde karanlık saha önerilmez; çünkü ağız florasında zararsız (non-patojen) treponema türleri (örn. *T. denticola*) bulunur ve *T. pallidum* ile morfolojik olarak karışabilir.

> Oral lezyonlarda karanlık saha yanıltıcı olabilir. Bu lezyonlar için diğer tanı testleri (DFA-TP, PCR veya seroloji) tercih edilmelidir.""",
            interactions=[
                make_cloze("Karanlık saha için örnek alınırken eritrositlerin görüntüyü bozmaması için kanlı değil, berrak {{seröz}} eksuda elde edilmelidir."),
                make_recall("Ağız florasındaki normal treponemalarla karışabileceği için, karanlık saha incelemesi hangi bölge lezyonlarında önerilmez?", "Ağız içi (oral) lezyonlarda."),
                make_chain([
                    {"q": "Lezyon yüzeyi temizlenip hafifçe sıkıldığında ne çıkması beklenir?", "a": "Seröz eksuda (sıvı)"},
                    {"q": "Aşırı sıkıp kanatırsak mikroskopta ne görülmesini zorlaştırırız?", "a": "Spiroketlerin görünümünü"},
                    {"q": "Neden ağız lezyonundan (ör. müköz yamalar) karanlık saha yapılmaz?", "a": "Normal ağız florasındaki non-patojen treponemalarla karışır"}
                ]),
                make_quiz(
                    "Karanlık saha incelemesi için hazırlanan bir preparatın yetersiz olmasının veya yanlış sonuç vermesinin en olası sebebi aşağıdakilerden hangisidir?",
                    ["Örneğin fazla soğutulması", "Preparatın kuruması veya çok kanlı olması", "Lezyonun ağrısız olması", "Bakterilerin Gram negatif olması", "Örneğin BOS'tan alınması"],
                    1,
                    "Doğru. Preparatın kuruması hareketin durmasına, kanlı olması ise spiroketlerin gizlenmesine neden olur."
                )
            ]
        )
    )

    # Slide 73
    slides.append(
        make_slide(
            title="Serolojik Tanıya Giriş: Nontreponemal vs Treponemal Test Ayrımı",
            narrative="""Karanlık saha mikroskobisi her zaman pratik olmadığından (uzmanlık ve aktif lezyon gerektirir), sifiliz tanısında altın standart yaklaşım **serolojik (antikor) testlerdir**. Sifiliz serolojisi iki büyük kategoriye ayrılır: Nontreponemal (spesifik olmayan) ve Treponemal (spesifik) testler.

**1. Nontreponemal Testler:** Bakterinin kendisine değil, enfeksiyon sonucu hasar gören hücrelerden açığa çıkan lipidlere (kardiyolipin) karşı oluşan antikorları ölçer. (Örnek: VDRL, RPR). Tarama ve tedavi takibi için kullanılır.
**2. Treponemal Testler:** Doğrudan T. pallidum yüzey antijenlerine karşı oluşan spesifik antikorları ölçer. (Örnek: FTA-ABS, TPHA). Nontreponemal testi pozitif çıkanları doğrulamak için kullanılır ve ömür boyu pozitif kalır.

> Sifiliz tanısında klasik algoritma: Önce nontreponemal bir test (VDRL/RPR) ile tara, pozitifse treponemal bir testle (FTA-ABS/TPHA) doğrula!""",
            interactions=[
                make_cloze("Sifiliz serolojisi temel olarak {{nontreponemal}} (tarama) ve treponemal (doğrulama) testler olmak üzere ikiye ayrılır."),
                make_recall("Kardiyolipine karşı gelişen antikorları ölçen ve taramada kullanılan test grubunun adı nedir?", "Nontreponemal (spesifik olmayan) testler."),
                make_table(
                    "Sifiliz Serolojik Testlerinin Karşılaştırması",
                    ["Özellik", "Nontreponemal Testler (VDRL, RPR)", "Treponemal Testler (FTA-ABS, TPHA)"],
                    [
                        ["Ölçülen Antikor", "Kardiyolipin antikorları (Reagin)", "T. pallidum spesifik antikorları"],
                        ["Temel Kullanım", "Tarama ve tedavi takibi", "Doğrulama (Konfirmasyon)"],
                        ["Tedavi Sonrası", "Negatifleşir (Titre düşer)", "Ömür boyu pozitif kalır"]
                    ]
                ),
                make_quiz(
                    "Klasik sifiliz tanı algoritmasında doğru sıralama hangisidir?",
                    ["Önce treponemal ile tara, nontreponemal ile doğrula", "Önce nontreponemal ile tara, treponemal ile doğrula", "Sadece nontreponemal test yap, yeterlidir", "Aynı anda iki farklı nontreponemal test yap", "Önce kültür, sonra seroloji yap"],
                    1,
                    "Doğru. Geleneksel algoritmada tarama için ucuz ve hızlı olan nontreponemal (VDRL/RPR), doğrulama için treponemal test kullanılır."
                )
            ]
        )
    )

    # Slide 74
    slides.append(
        make_slide(
            title="Nontreponemal (Spesifik Olmayan) Testlerin Temeli: Kardiyolipin-Lesitin-Kolesterol Antijeni",
            narrative="""Nontreponemal testlerin mantığı oldukça ilginçtir. T. pallidum vücuda girdiğinde hücre membranlarında hasar oluşturur. Hasarlanan konak hücrelerinden (ve bir miktar da bakterinin kendisinden) bir lipid olan **kardiyolipin** açığa çıkar. 

Vücut bağışıklık sistemi bu kardiyolipine karşı IgM ve IgG yapısında otoantikorlar üretir. Bu antikorlara tarihsel olarak **"Reagin"** adı verilmiştir. Laboratuvarda, hastanın serumundaki bu reaginleri saptamak için sığır kalbinden elde edilen "Kardiyolipin-Lesitin-Kolesterol" karışımı yapay bir antijen olarak kullanılır.

> Bu reaksiyon T. pallidum'a özgü olmadığından (sadece doku hasarına bağlı lipidi hedeflediğinden), nontreponemal testler başka hastalıklarda (lupus, lepra, gebelik) yalancı pozitiflik verebilir.""",
            interactions=[
                make_cloze("Nontreponemal testler, hasarlı dokulardan açığa çıkan lipid yapısındaki {{kardiyolipin}} molekülüne karşı gelişen antikorları saptar."),
                make_recall("Kardiyolipine karşı gelişen bu antikorlara tarihsel olarak ne ad verilir?", "Reagin."),
                make_quiz(
                    "Nontreponemal testlerde laboratuvarda hastanın antikorlarını bağlamak için kullanılan antijen karışımının ana bileşeni nedir?",
                    ["Treponema dış membran proteinleri", "Sığır kalbinden elde edilen kardiyolipin-lesitin-kolesterol", "Koyun eritrositleri", "İnsan immünglobulini", "T. pallidum flagellasından saflaştırılmış protein"],
                    1,
                    "Doğru. Nontreponemal testler sığır kalbinden (cardio) izole edilen bir lipid (kardiyolipin) antijenini kullanır."
                ),
                make_cloze("Nontreponemal testlerdeki antikorlar bakteriye spesifik olmadığı için, diğer durumlarda da (örneğin otoimmün hastalıklar) {{yalancı pozitiflik}} görülebilir.")
            ]
        )
    )

    # Slide 75
    slides.append(
        make_slide(
            title="VDRL (Venereal Disease Research Laboratory) Testi ve Klinik Kullanımı",
            narrative="""Nontreponemal testlerin en eski ve en klasik olanı **VDRL (Venereal Disease Research Laboratory)** testidir. VDRL, mikroskobik bir flokülasyon (kümeleşme) testidir. Hastanın ısıtılarak inaktive edilmiş serumu, kardiyolipin antijeni ile lam üzerinde karıştırılır; reagin antikorları varsa mikroskop altında kümeler oluşturur.

VDRL günümüzde serum için daha çok RPR'ye yerini bırakmış olsa da, çok kritik bir kullanım alanı devam etmektedir: **Nörosifiliz tanısı**. VDRL, beyin omurilik sıvısında (BOS) güvenle çalışılabilen ve BOS için standardize edilmiş tek nontreponemal testtir.

> BOS-VDRL pozitifliği, (kanla kontaminasyon yoksa) nörosifiliz tanısı için son derece spesifiktir ve altın standart kabul edilir.""",
            interactions=[
                make_cloze("VDRL testi, antijen ve antikor reaksiyonunu mikroskopta gösteren bir {{flokülasyon}} (kümeleşme) testidir."),
                make_recall("Nörosifiliz tanısında beyin omurilik sıvısında (BOS) rutin olarak hangi nontreponemal test kullanılır?", "VDRL (BOS-VDRL)."),
                make_spot_lie(
                    "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: VDRL testi",
                    [
                        {"text": "VDRL kardiyolipine karşı gelişen antikorları saptar.", "isLie": False, "explanation": "Evet, klasik bir nontreponemal testtir."},
                        {"text": "Nörosifiliz şüphesinde BOS örneğinden VDRL testi çalışılabilir.", "isLie": False, "explanation": "BOS için en geçerli ve standart test BOS-VDRL'dir."},
                        {"text": "VDRL testi T. pallidum'un kendisine ait spesifik protein antijenlerini kullanır.", "isLie": True, "explanation": "TUZAK! VDRL spesifik DEĞİLDİR, sığır kalbinden alınan lipid (kardiyolipin) kullanır."}
                    ]
                ),
                make_chain([
                    {"q": "VDRL testinin uzun açılımı nedir?", "a": "Venereal Disease Research Laboratory"},
                    {"q": "VDRL testinde gözlenen reaksiyon tipine ne denir?", "a": "Flokülasyon"},
                    {"q": "Günümüzde VDRL'nin en kritik klinik kullanım yeri neresidir?", "a": "BOS'ta nörosifiliz tanısı"}
                ])
            ]
        )
    )

    # Slide 76
    slides.append(
        make_slide(
            title="RPR (Rapid Plasma Reagin) Testi ve Tarama Dinamiği",
            narrative="""**RPR (Rapid Plasma Reagin)**, VDRL testinin daha modern, pratik ve hızlı bir modifikasyonudur. VDRL'den farklı olarak mikroskop gerektirmez (makroskobik flokülasyon) ve serumun önceden ısıtılmasını (inaktivasyon) istemez. 

RPR testinde kardiyolipin antijenine **karbon partikülleri** eklenmiştir. Antikor-antijen reaksiyonu gerçekleştiğinde (pozitif sonuç), karbon tanecikleri bir araya toplanarak beyaz kart üzerinde siyah kümeler halinde çıplak gözle görülür hale gelir. 

> Pratikliği, hızı ve mikroskop gerektirmemesi nedeniyle RPR, günümüzde kan (serum) ile yapılan sifiliz taramalarında VDRL'nin yerini almış ve standart nontreponemal test haline gelmiştir. Ancak RPR, BOS örneklerinde *kullanılmaz*.""",
            interactions=[
                make_cloze("RPR testinde kümeleşmenin mikroskop olmadan çıplak gözle görülebilmesi için antijene {{karbon}} partikülleri eklenmiştir."),
                make_recall("Serum taramasında VDRL'den daha pratik olan makroskobik testin adı nedir?", "RPR (Rapid Plasma Reagin)."),
                make_table(
                    "VDRL ve RPR Karşılaştırması",
                    ["Özellik", "VDRL", "RPR"],
                    [
                        ["Okunma Şekli", "Mikroskobik flokülasyon", "Makroskobik flokülasyon (Karbon)"],
                        ["Serum Hazırlığı", "Isı ile inaktivasyon gerekir", "İnaktivasyon gerektirmez"],
                        ["BOS'ta Kullanım", "Kullanılır (Altın standart)", "Önerilmez"]
                    ]
                ),
                make_quiz(
                    "Birinci basamak sağlık kuruluşunda çıplak gözle sonuç alınabilen, mikroskop gerektirmeyen en yaygın sifiliz tarama testi hangisidir?",
                    ["BOS-VDRL", "RPR (Rapid Plasma Reagin)", "Karanlık saha", "FTA-ABS", "Kültür"],
                    1,
                    "Doğru. RPR karbon partikülleri sayesinde makroskobik olarak kolayca yorumlanır ve tarama için idealdir."
                )
            ]
        )
    )

    # Slide 77
    slides.append(
        make_slide(
            title="Nontreponemal Testlerin Primer ve Sekonder Dönemde Pozitifliği",
            narrative="""Nontreponemal testler (VDRL/RPR) şankr (primer sifiliz) ilk çıktığı günlerde **negatiftir**. Doku hasarı birikip antikor (reagin) üretimi zamana yayılır. Genellikle şankr ortaya çıktıktan 1-3 hafta sonra VDRL/RPR pozitifleşmeye başlar. Bu nedenle, erken primer dönemde test yalancı negatif olabilir.

Ancak hastalık yayılıp **sekonder sifiliz** evresine (döküntüler, sistemik bulgular) ulaşıldığında, nontreponemal testler %100'e yakın oranda pozitiftir ve antikor titreleri en yüksek seviyelerine (ör. 1:64, 1:128) ulaşır. 

> Eğer hastada sekonder sifilizin klasik yaygın döküntüleri varken RPR/VDRL negatif geliyorsa, bunun en olası sebebi 'Prozon fenomeni'dir (Antikor miktarının çok aşırı olup antijenle optimalleşememesi ve çökelme yapamaması). Serum sulandırılarak test tekrarlandığında pozitifleşir.""",
            interactions=[
                make_cloze("Nontreponemal testler şankrın ilk günlerinde negatiftir, lezyon çıktıktan yaklaşık 1-3 hafta sonra {{pozitifleşir}}."),
                make_recall("Nontreponemal antikor titrelerinin (RPR/VDRL) vücutta en yüksek seviyeye ulaştığı hastalık evresi hangisidir?", "Sekonder sifiliz."),
                make_quiz(
                    "Yaygın makülopapüler döküntüleri olan (sekonder sifiliz kliniği) bir hastada ilk bakılan VDRL negatif gelmiştir. Serum dilüe edilip (sulandırılıp) tekrarlandığında ise yüksek titrede pozitif gelmiştir. Bu durum ne ile açıklanır?",
                    ["Otoimmünite", "Yalancı negatiflik yapan Prozon fenomeni", "Karanlık saha etkisi", "Çapraz reaksiyon", "Tersiyer faza geçiş"],
                    1,
                    "Doğru. Antikorun çok yüksek olması reaksiyonu engeller (Prozon fenomeni). Dilüsyon yapıldığında antikor-antijen oranı dengelenir ve test pozitif çıkar."
                ),
                make_cloze("Sekonder sifiliz evresinde nontreponemal testlerin duyarlılığı (sensitivitesi) neredeyse %{{100}}'dür.")
            ]
        )
    )

    # Slide 78
    slides.append(
        make_slide(
            title="Nontreponemal Test Titrelerinin Tedavi Takibindeki Rolü",
            narrative="""Nontreponemal testlerin en benzersiz ve paha biçilmez özelliği, **kantitatif (sayısal) titre** verebilmeleri ve hastalığın aktivitesiyle korele olmalarıdır. RPR veya VDRL raporlanırken "1:16", "1:32" gibi bir titre ile verilir. 

Bu testler **tedaviye yanıtın takibinde** kullanılır. Hasta başarılı bir şekilde tedavi edildiğinde (örneğin penisilin ile), doku hasarı duracağı için kardiyolipin salınımı kesilir ve reagin antikor titreleri zamanla düşmeye başlar. Başarılı bir tedavi için kural, tedaviden sonraki 6-12 ay içinde titrenin en az 4 kat (2 dilüsyon, örneğin 1:32'den 1:8'e) düşmesidir.

> Titrenin düşmemesi veya 4 kat artması (ör. 1:4'ten 1:16'ya) tedavinin başarısız olduğunu veya hastanın yeniden enfekte olduğunu (re-enfeksiyon) gösterir.""",
            interactions=[
                make_cloze("Nontreponemal testler hastalığın aktivitesiyle orantılıdır ve kantitatif sonuç verdikleri için {{tedavi takibinde}} kullanılırlar."),
                make_recall("Başarılı bir sifiliz tedavisinden sonra nontreponemal test titresinin (RPR) 6 ay içinde en az kaç kat düşmesi beklenir?", "4 kat (2 dilüsyon)."),
                make_chain([
                    {"q": "Hastanın tedavi öncesi RPR titresi 1:64'tür. Başarılı tedavi için 6 ay sonra en fazla kaç olmalıdır?", "a": "1:16 (4 kat düşüş)"},
                    {"q": "Titre düşmeyip artarsa veya aynı kalırsa ne düşünülür?", "a": "Tedavi başarısızlığı veya re-enfeksiyon"},
                    {"q": "Treponemal testler tedavi takibi için kullanılabilir mi?", "a": "Hayır, ömür boyu pozitif kalırlar"}
                ]),
                make_quiz(
                    "Sifiliz tedavisi alan bir hastanın takibinde VDRL titresinin 1:32'den 1:128'e yükseldiği görülmüştür. Bu durum en çok hangisiyle uyumludur?",
                    ["Tedavi başarılı olmuştur", "Titreler sadece yaşla artar", "Re-enfeksiyon (yeni enfeksiyon) veya relaps gelişmiştir", "Bu normal bir iyileşme yanıtıdır", "Testin kanda karbonla reaksiyonudur"],
                    1,
                    "Doğru. Titrenin 4 kat artması aktif hastalık veya yeni bir enfeksiyon (re-enfeksiyon) göstergesidir."
                )
            ]
        )
    )

    # Slide 79
    slides.append(
        make_slide(
            title="Tedavi Sonrası Titre Düşüşü ve 1-2 Yılda Negatifleşme Süreci",
            narrative="""Tedavi başarılı olduğunda, VDRL veya RPR titrelerinin seyri öngörülebilirdir. Primer sifilizde tedavi sonrası testler genellikle 1 yıl içinde tamamen negatife (non-reaktif) döner. Sekonder sifilizde tedavi başlandıysa, negatifleşme 2 yılı bulabilir.

Ancak bazı hastalarda, titre uygun şekilde 4 kat düşse bile test yıllarca düşük bir titrede (örneğin 1:2 veya 1:4) pozitif kalmaya devam edebilir. Başarılı tedaviye rağmen ömür boyu kalabilen bu düşük düzey reaktiviteye **serofast durum** adı verilir. 

> Serofast bir hastada titre stabil kalır, klinik semptom yoktur. Bu durum aktif hastalık anlamına gelmez ve tekrarlayan tedavilere gerek yoktur. Sadece titrenin aniden yükselip yükselmediği (re-enfeksiyon) takip edilir.""",
            interactions=[
                make_cloze("Erken evre sifiliz başarıyla tedavi edildiğinde VDRL/RPR testleri genellikle 1-2 yıl içinde tamamen {{negatifleşir}}."),
                make_recall("Tedavi başarılı olmasına rağmen VDRL/RPR'nin ömür boyu düşük titrede (1:2 gibi) pozitif kalmasına ne ad verilir?", "Serofast durum."),
                make_spot_lie(
                    "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tedavi sonrası seroloji",
                    [
                        {"text": "Primer sifiliz tedavi edildikten sonra 1 yıl içinde RPR sıklıkla negatifleşir.", "isLie": False, "explanation": "Erken tedavide antikorlar hızla kaybolur."},
                        {"text": "Düşük titrede pozitifliğin (serofast) yıllarca devam etmesi aktif hastalığı gösterir ve tekrar penisilin verilir.", "isLie": True, "explanation": "TUZAK! Serofast durum aktif hastalık DEĞİLDİR ve stabil kaldığı sürece tekrar tedavi gerektirmez."},
                        {"text": "Tedavinin başarısı ilk 6-12 ayda titrenin en az 4 kat düşmesiyle doğrulanır.", "isLie": False, "explanation": "Evet, VDRL/RPR'nin temel kullanım amacı budur."}
                    ]
                ),
                make_cloze("Serofast durumlarda hasta klinik olarak iyidir; sadece titrenin gelecekte aniden artıp artmayacağı (örneğin yeni bir bulaş olan {{re-enfeksiyon}}) takip edilmelidir.")
            ]
        )
    )

    # Slide 80
    slides.append(
        make_slide(
            title="[TEKRAR SAYFASI - CHECKPOINT 8] Karanlık Saha ve Nontreponemal Testler (VDRL, RPR)",
            narrative="""Bu bölümde sifilizin temel tanı testlerini özetledik:

- **Karanlık Saha Mikroskobisi**: Primer (şankr) ve sekonder lezyonlarda canlı treponemaların tirbuşon hareketini gösterir. Erken tanıda altındır. (Ağız içi lezyonlarda kullanılmaz!).
- **Nontreponemal Testler**: VDRL ve RPR.
  - *Antijen*: Kardiyolipin (Sığır kalbinden).
  - *Ölçtüğü*: Doku hasarı sonucu oluşan reagin antikorları (Spesifik değil).
  - *Kullanım Amacı*: Tarama ve **Tedavi Takibi** (Titresi hastalığın aktivitesini yansıtır).
  - *RPR*: Serum taramasında makroskobik ve hızlıdır.
  - *VDRL*: **Nörosifiliz tanısında** (BOS'ta) altın standarttır.
  - *Takip*: Başarılı tedavide titre 6 ayda 4 kat düşmelidir.

Bir sonraki bölümde, nontreponemal testlerin yalancı pozitiflik nedenlerini ve Treponemal testleri (FTA-ABS vb.) işleyeceğiz.""",
            interactions=[
                make_table(
                    "Nontreponemal Test Özet Tablosu",
                    ["Test", "Örnek Tipi", "Temel Özellik"],
                    [
                        ["Karanlık Saha", "Lezyon Eksudası", "Erken dönem kesin tanısı (Canlı hareket)"],
                        ["RPR", "Serum (Kan)", "Tarama için en pratik makroskobik test"],
                        ["VDRL", "BOS ve Serum", "Nörosifiliz tanısında BOS'ta tek geçerli test"]
                    ]
                ),
                make_cloze("Karanlık saha mikroskobisi {{şankr}} evresinde henüz antikorlar pozitifleşmeden kesin tanı koydurur."),
                make_recall("Başarılı sifiliz tedavisinde nontreponemal (VDRL/RPR) titrenin seyri nasıl olmalıdır?", "En az 4 kat düşmeli ve zamanla negatifleşmelidir."),
                make_quiz(
                    "Sifiliz şüphesiyle laboratuvara gönderilen bir test isteminde, 'Tedaviye yanıtın takibi' amacı güdülüyorsa aşağıdakilerden hangisi istenmelidir?",
                    ["FTA-ABS", "Karanlık saha mikroskobisi", "RPR veya VDRL (Kantitatif titre)", "T. pallidum PCR", "TPHA"],
                    1,
                    "Doğru. Tedavi takibi sadece kantitatif sonuç verebilen nontreponemal testler (VDRL/RPR) ile yapılır."
                )
            ]
        )
    )

    return slides
