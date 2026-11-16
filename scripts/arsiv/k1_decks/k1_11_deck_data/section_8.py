# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-11-s71",
        "title": "Tanısal Algoritma ve İlk Basamak Görüntüleme: Ultrasonografi",
        "content": "Üriner sistem obstrüksiyonu veya renal kolik şüphesiyle başvuran bir hastada ilk basamakta tercih edilmesi gereken temel görüntüleme yöntemi **Ultrasonografidir (USG)**. USG'nin ilk basamak olmasını sağlayan temel üstünlükleri; iyonizan radyasyon içermemesi, non-invaziv olması, kontrast madde gerektirmemesi (böbrek yetmezliği olan veya gebe hastalarda güvenle kullanılabilmesi), yatak başında dakikalar içinde uygulanabilmesi ve düşük maliyetli olmasıdır. USG ile toplayıcı sistemdeki hidronefrozun varlığı, kaliksiyel dilatasyon, parankim kalınlığı ve mesane doluluğu hızla saptanabilir. Ancak sonuçların hekimin deneyimine (kullanıcı bağımlı) ve hastanın vücut yapısına (obezite, yoğun barsak gazı) göre değişkenlik göstermesi ve üreterin orta segmentinin net görülememesi yöntemin en önemli sınırlılıklarıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Üriner obstrüksiyon şüphesinde radyasyonsuz, hızlı ve non-invaziv olması nedeniyle ilk değerlendirme yöntemi ultrasonografidir.",
                "ultrasonografidir",
                "Ses dalgalarıyla çalışan ilk basamak görüntüleme tekniği"
            ),
            make_quiz(
                "Obstrüktif üropati düşünülen bir hastanın radyolojik değerlendirmesinde 'ilk basamak yöntem' olarak ultrasonografinin (USG) seçilmesinin temel gerekçesi hangisidir?",
                [
                    {"key": "A", "text": "Non-invaziv, radyasyonsuz, hızlı ve böbrek yetmezliğinde dahi güvenli olması", "explanation": "A seçeneği DOĞRUDUR: USG kontrast gerektirmez, radyasyon vermez, her hastada ilk basamak triyaj aracıdır."},
                    {"key": "B", "text": "Üreter taşının kimyasal moleküler formülünü kesin olarak vermesi", "explanation": "B seçeneği yanlıştır: USG taş kimyasını analiz edemez."},
                    {"key": "C", "text": "Glomerüler filtrasyon hızını mililitre cinsinden kesin ölçmesi", "explanation": "C seçeneği yanlıştır: GFR ölçümü nükleer tıp ve biyokimyayla yapılır."},
                    {"key": "D", "text": "Tüm üreter lümenini baştan sona %100 doğrulukla göstermesi", "explanation": "D seçeneği yanlıştır: Barsak gazları nedeniyle orta üreter USG ile zayıf izlenir."},
                    {"key": "E", "text": "İntravenöz radyoaktif madde verilmesini zorunlu kılması", "explanation": "E seçeneği yanlıştır: USG radyoaktif madde kullanmaz."}
                ],
                "A"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-11-s72",
        "title": "USG'de Hidronefroz Derecelendirmesi ve Hata Tuzakları",
        "content": "Ultrasonografide hidronefroz kaliks ve pelvis genişliğine göre hafif, orta ve ileri derece olarak sınıflandırılır. Ancak klinisyen iki kritik hata tuzağını daima akılda tutmalıdır:\n\n1. **Yalancı Negatiflik (Obstrüksiyon Var, USG'de Hidronefroz Yok):** Akut obstrüksiyonun ilk birkaç saatinde toplayıcı sistem henüz genişleyecek zaman bulamamış olabilir. Ayrıca hastanın aşırı dehidrate olması veya forniks rüptürü ile retroperitona idrar sızması durumunda hidronefroz görülmeyebilir ('non-dilate obstrüktif üropati'). Şiddetli kolik ağrısı olan hastada USG normal olsa bile tıkanıklık ekarte edilmiş sayılmaz.\n2. **Yalancı Pozitiflik (Hidronefroz Görünüyor, Gerçek Obstrüksiyon Yok):** Doğuştan ekstrarenal pelvis anomalisi olanlarda, aşırı sıvı yüklenmesi (aşırı hidrasyon) yapılmış olgularda veya aşırı dolu mesane varlığında toplayıcı sistem genişlemiş görünür; ancak lümende mekanik bir tıkanıklık yoktur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "USG Değerlendirmesinde Hata Tuzakları",
                "Yalancı Negatiflik (Gizli Tıkanma)",
                "Akut ilk saatler, derin dehidratasyon veya forniks rüptüründe hidronefroz izlenmeyebilir.",
                "Yalancı Pozitiflik (Mekanik Olmayan Dilatasyon)",
                "Ekstrarenal pelvis, aşırı hidrasyon veya çok dolu mesane obstrüksiyon olmaksızın geniş görünür."
            ),
            make_recall(
                "Akut şiddetli üreter taşı atağında obstrüksiyona rağmen USG'de kaliks dilatasyonunun henüz görülememesine ne ad verilir?",
                "Yalancı negatiflik (veya non-dilate obstrüksiyon).",
                "Erken dönemde genişlemenin gecikmesi durumu"
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-11-s73",
        "title": "Kontrassız Helikal Taş BT: Akut Taş Tanısında Altın Standart",
        "content": "Akut böğür ağrısı ve ürolitiyazis şüphesinde günümüz modern tıbbının tartışmasız **altın standart tanı yöntemi Kontrassız Helikal Bilgisayarlı Tomografidir (Taş BT)**. Bu yöntemin üstünlükleri:\n\n- **Maksimum Duyarlılık ve Özgüllük:** %98-99 duyarlılık ve özgüllükle birkaç milimetrelik mikrolitleri dahi gösterir.\n- **Tüm Taş Tiplerini Görme Kapasitesi:** Klasik röntgende ve IVP'de görünmeyen radyo-lusent ürik asit, ksantin ve sistin taşları da dahil olmak üzere neredeyse tüm taşlar tomografide opaktır (tek istisna retroviral proteaz inhibitörü olan indinavir taşlarıdır).\n- **Sekonder Obstrüksiyon Bulguları:** Yalnızca taşı değil; taşın proksimalinde üreter dilatasyonu, böbrekte büyüme, kaliksektazi ve renal pelvis/perirenal yağ dokusunda ödemi ('perirenal stranding / periüreteral sıvı') net olarak sergiler.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Akut böğür ağrısında taş tanısı için en yüksek duyarlılık ve özgüllüğe sahip altın standart yöntem kontrassız helikal bilgisayarlı tomografidir.",
                "bilgisayarlı tomografidir",
                "Kesitsel X-ışını teknolojisine dayanan altın standart yöntem"
            ),
            make_quiz(
                "Kontrassız taş bilgisayarlı tomografisinde radyo-opasite göstermeyen ve görünmeyebilen tek istisnai taş türü hangisidir?",
                [
                    {"key": "A", "text": "İndinavir taşları (HIV proteaz inhibitörü ilacı)", "explanation": "A seçeneği DOĞRUDUR: İndinavir metabolit taşları kontrassız BT'de dansite farkı oluşturmayarak görünmeyebilir."},
                    {"key": "B", "text": "Kalsiyum oksalat monohidrat taşları", "explanation": "B seçeneği yanlıştır: En yüksek dansiteli taşlardır (1000-1500 HU)."},
                    {"key": "C", "text": "Ürik asit taşları", "explanation": "C seçeneği yanlıştır: Düz grafide lüsenttir ancak kontrassız BT'de net opaktır."},
                    {"key": "D", "text": "Magnezyum amonyum fosfat (strüvit) taşları", "explanation": "D seçeneği yanlıştır: BT'de belirgin opaktır."},
                    {"key": "E", "text": "Kalsiyum fosfat taşları", "explanation": "E seçeneği yanlıştır: Çok yüksek dansitede görünür."}
                ],
                "A"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-11-s74",
        "title": "Kontrastlı BT ve Ürografi (BTÜ): Ekstrensek Patolojiler ve Kitleler",
        "content": "Üriner obstrüksiyonun nedeni taş dışı bir patoloji olduğunda (örneğin retroperitoneal kitleler, lenfomalar, üreter ürotelyal tümörleri veya retroperitoneal fibrozis), intravenöz iyotlu kontrast madde verilerek çekilen Kontrastlı Bilgisayarlı Tomografi ve BT Ürografi (BTÜ) devreye girer. Bu yöntem üç ayrı fazda incelenir:\n\n1. **Kortikomedüller Faz:** Vasküler yapılar ve parankim perfüzyonunu gösterir.\n2. **Nefrografik Faz:** Renal parankimal kitleleri (RCC) ve tübüler tutulumu gösterir.\n3. **Boşaltım (Ekskretuar) Fazı:** İyotlu kontrast toplayıcı sisteme döküldüğünde kaliks, pelvis ve üreter anatomisini milimetrik çözer; lümen içi dolma defektlerini (ürotelyal karsinom veya striktür) ve üreteri dışarıdan saran kitle veya fibrozis sınırlarını net olarak ortaya koyar. Ancak kontrast maddenin nefrotoksik riski nedeniyle yüksek kreatininli olgularda dikkatli olunmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["BTÜ Fazı", "Zamanlama", "Temel Tanısal Değer"],
                [
                    [
                        {"text": "Kortikomedüller Faz", "isMasked": False, "hint": ""},
                        {"text": "Kontrattan 30-40 sn sonra", "isMasked": True, "hint": "Arteryel dolaşım zamanı"},
                        {"text": "Vasküler yapılar ve renal perfüzyon", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Nefrografik Faz", "isMasked": False, "hint": ""},
                        {"text": "Kontrattan 80-100 sn sonra", "isMasked": True, "hint": "Tüm parankimin boyandığı zaman"},
                        {"text": "Renal parankim kitleleri ve kortikal skar", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Ekskretuar Faz", "isMasked": False, "hint": ""},
                        {"text": "Kontrattan 5-15 dk sonra", "isMasked": True, "hint": "İdrarın toplayıcı sisteme döküldüğü an"},
                        {"text": "Toplayıcı sistem, lümen dolma defektleri ve üreter darlıkları", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "BT ürografide toplayıcı sistem lümenini ve üreter darlıklarını ayrıntılı gösteren en son görüntüleme fazı hangisidir?",
                "Boşaltım (ekskretuar) fazıdır.",
                "Kontrastın idrarla toplayıcı sisteme döküldüğü faz"
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-11-s75",
        "title": "İntravenöz Piyelografi (IVP / İVU): Klasik Anatomik Değerlendirme",
        "content": "İntravenöz Piyelografi (IVP veya İVU), damar yolundan iyotlu kontrast madde verilerek belirli zaman aralıklarıyla direkt grafilerin çekildiği klasik radyolojik incelemedir. Toplayıcı sistem anatomisini ve obstrüksiyonun tam seviyesini ortaya koymada tarihsel olarak çok büyük öneme sahiptir. Obstrükte böbrekte IVP'de tipik olarak **gecikmiş nefrogram** izlenir; kontrast madde filtre edilmekte gecikir ancak glomerüllerde ve proksimal tübüllerde birikerek böbrek silüetini saatler boyunca yoğun ve beyaz gösterir. İlerleyen saatlerde (bazen 12-24. saat gecikmiş filmlerde) kontrast toplayıcı sisteme sızarak hidronefrotik kaliksleri ve tıkanıklık seviyesini sergiler. Ancak radyasyon maruziyeti, kontrast nefrotoksisitesi ve BT'nin yaygınlaşması nedeniyle günümüzde kullanımı sınırlanmıştır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Akut üreter obstrüksiyonlu böbreğin IVP incelemesinde kontrast maddenın tübüllerde birikmesiyle gecikmis nefrogram bulgusu ortaya çıkar.",
                "gecikmis nefrogram",
                "Böbrek gölgesinin uzun süre beyaz ve yoğun boyanması fenomeni"
            ),
            make_quiz(
                "İntravenöz piyelografide (IVP) obstrükte bir böbreğin klasik karakteristik radyolojik bulgusu hangisidir?",
                [
                    {"key": "A", "text": "Gecikmiş nefrogram ve obstrüksiyon düzeyine kadar toplayıcı sistem dilatasyonu", "explanation": "A seçeneği DOĞRUDUR: Akut tıkanıklıkta kontrast atımı gecikir, nefrogram uzar ve geç filmlerde dilatasyon görünür."},
                    {"key": "B", "text": "Kontrast maddenin böbreğe hiç ulaşmadan tamamen karaciğerde tutulması", "explanation": "B seçeneği yanlıştır."},
                    {"key": "C", "text": "Toplayıcı sistemin 1. dakikada tamamen boşalması", "explanation": "C seçeneği yanlıştır: Bu normal veya hiperfonksiyone böbrektir, obstrüksiyon gecikme yapar."},
                    {"key": "D", "text": "Mesanenin tamamen ortadan kaybolması", "explanation": "D seçeneği anlamsızdır."},
                    {"key": "E", "text": "Üreterin lümeninin tamamen kalsifiye beyaz tüp olarak doğması", "explanation": "E seçeneği yanlıştır: Bu parazitoz veya tüberküloz sekeli olabilir, akut bulgu değildir."}
                ],
                "A"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-11-s76",
        "title": "Dinamik Renal Sintigrafi: Tc-99m MAG3 ve DTPA ile Fonksiyon Tayini",
        "content": "Radyolojik yöntemler toplayıcı sistemin anatomik dilatasyonunu gösterirken; Nükleer Tıp yöntemleri böbreğin ayrılmış (diferansiyel) fonksiyonunu ve obstrüksiyonun dinamik ciddiyetini kantitatif olarak ölçer:\n\n- **Tc-99m DTPA (Dietilentriaminpentaasetik Asit):** Yalnızca glomerüler filtrasyonla (GFR) temizlenir. Böbrek yetmezliği olan veya GFR'si düşük olgularda görüntü kalitesi düşer.\n- **Tc-99m MAG3 (Merkaptoasetiltriglisin):** %95 oranında proksimal tübüler sekresyonla atılır. Ekstraksiyon fraksiyonu çok yüksek olduğundan, renal perfüzyonu ve GFR'si belirgin düşmüş, üremik veya pediatrik böbreklerde dahi mükemmel görüntü kalitesi ve diferansiyel fonksiyon hesabı sağlar.\n\nSintigrafi ile sağ ve sol böbreğin total fonksiyona katkısı (normalde %50-%50) net olarak hesaplanır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Nükleer Renal Radyofarmasötikler Karşılaştırması",
                "Tc-99m DTPA",
                "Glomerüler filtrasyonla atılır; GFR hesabı sağlar ancak üremik böbreklerde görüntü kalitesi zayıftır.",
                "Tc-99m MAG3",
                "Tübüler sekresyonla atılır; yüksek ekstraksiyon oranıyla bozulmuş böbreklerde dahi üstün görüntü verir."
            ),
            make_recall(
                "Böbrek yetmezliği ve hidronefrozu olan hastalarda dinamik sintigrafide tübüler sekresyonla atıldığı için tercih edilen radyofarmasötik hangisidir?",
                "Tc-99m MAG3'tür (Merkaptoasetiltriglisin).",
                "Tübüler atılımlı modern teknetyum bileşiği"
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-11-s77",
        "title": "Diüretikli Renal Sintigrafi (Lasix Testi): Gerçek Obstrüksiyonun Ayırımı",
        "content": "Genişlemiş bir toplayıcı sistem her zaman mekanik bir darlık anlamına gelmez; hipotonik ve atonik bir sistem de geniş görünebilir. Bu ayrımı yapmak için Diüretikli Renal Sintigrafi (Furosemid / Lasix testi) uygulanır. Radyofarmasötik verildikten sonra pelviste radyoaktivite birikip plato çizdiğinde (genellikle 20. dakikada) hastaya intravenöz **furosemid (Lasix)** enjekte edilir:\n\n1. **Obstrüksiyon Yok (Hipotonik Dilatasyon):** Furosemidin ürettiği masif idrar akımı toplayıcı sistemdeki radyoaktiviteyi hızla yıkar. Yarılanma boşalma süresi (T1/2) **10 dakikanın altındadır**.\n2. **Mekanik Obstrüksiyon:** Masif idrar akımına rağmen çıkıştaki darlık nedeniyle radyoaktivite pelvisten tahliye edilemez ve eğri yükselmeye devam eder. T1/2 süresi **20 dakikanın üzerindedir**.\n3. **Şüpheli Bölge:** T1/2 süresinin 10-20 dakika arasında olması gri zontur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Lasix Yanıtı", "Yarılanma Süresi (T1/2)", "Klinik Tanı"],
                [
                    [
                        {"text": "Hızlı Boşalma", "isMasked": False, "hint": ""},
                        {"text": "T1/2 < 10 dakika", "isMasked": True, "hint": "Diüretikle derhal yıkanan sistem"},
                        {"text": "Obstrüksiyon yok (Non-obstrüktif dilatasyon)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Boşalamama (Plato/Yükselme)", "isMasked": False, "hint": ""},
                        {"text": "T1/2 > 20 dakika", "isMasked": True, "hint": "Mekanik tıkanıklık kriteri"},
                        {"text": "Gerçek mekanik obstrüksiyon (Cerrahi endikasyon)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kısmi / Yavaş Boşalma", "isMasked": False, "hint": ""},
                        {"text": "T1/2 10-20 dakika", "isMasked": True, "hint": "Belirsiz gri alan"},
                        {"text": "Şüpheli / indetermine sonuç", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Diüretikli renal sintigrafide furosemid sonrası toplayıcı sistem yarılanma boşalma süresinin yirmi dakikadan uzun olması mekanik obstrüksiyon lehinedir.",
                "yirmi dakikadan uzun",
                "T1/2 süresinin obstrüksiyon eşiği olan dakika sınırı"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-11-s78",
        "title": "Manyetik Rezonans Ürografi (MRÜ): Gebe ve Pediatrik Olgular",
        "content": "Manyetik Rezonans Ürografi (MRÜ), iyonizan radyasyon riski taşımaması ve üstün yumuşak doku kontrast rezolüsyonu sayesinde özellikle gebe kadınlarda, çocuklarda ve iyotlu kontrast alerjisi olan hastalarda vazgeçilmez bir tanı aracıdır. İki temel teknikte uygulanır:\n\n1. **Statik Sıvı Ağırlıklı MRÜ (T2-Ağırlıklı):** Hiçbir intravenöz kontrast madde verilmeden uygulanır. Ağır T2 ağırlıklı sekanslarda durağan veya yavaş akan idrar yüksek sinyal vererek parlak beyaz görünür. Toplayıcı sistemin üç boyutlu anatomik kalıbı mükemmel çıkarılır.\n2. **Dinamik Kontrastlı MRÜ (T1 Gadolinyumlu):** Gadolinyum bazlı kontrast madde verilerek böbreğin parankimal perfüzyonu, GFR'si ve toplayıcı sisteme atılım dinamikleri eş zamanlı incelenir. Ancak eGFR < 30 ml/dk olan derin böbrek yetmezlikli olgularda Nefrojenik Sistemik Fibrozis (NSF) riski nedeniyle gadolinyum kullanımından kaçınılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "MR Ürografi Klinik Kullanım Endikasyonları",
                [
                    "1. Gebe Hastalar: Fetal radyasyon maruziyetini tamamen sıfırlamak",
                    "2. İyot Kontrast Alerjisi: Anaflaksi riski olan olgularda güvenli inceleme",
                    "3. Pediatrik Anomaliler: Kompleks çift sistem ve ektopik üreterlerin haritalanması",
                    "4. Statik T2 İnceleme: Kontratsız toplayıcı sistem morfolojisinin çıkarılması"
                ]
            ),
            make_recall(
                "Hiçbir kontrast madde vermeden yalnızca idrarın doğal sinyalini kullanarak toplayıcı sistem haritası çıkaran MR tekniği hangisidir?",
                "Statik sıvı ağırlıklı T2 MR ürografidir.",
                "Ağır T2 sekanslı hidrografi tekniği"
            )
        ]
    })

    # Slide 79 (CHECKPOINT 8)
    slides.append({
        "id": "k1-11-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Radyolojik ve Nükleer Tıp Tanı Yöntemleri",
        "content": "Obstrüksiyonun tanısal algoritmasının temel sacayakları:\n\n1. **İlk Basamak:** USG; radyasyonsuz ve hızlıdır. Akut dönemde veya dehidratasyonda yalancı negatif, aşırı hidrasyonda yalancı pozitif olabilir.\n2. **Altın Standart:** Akut taş koliğinde kontrassız helikal taş BT; %99 doğrulukla indinavir hariç tüm taşları saptar.\n3. **Klasik Yöntem:** IVP'de obstrükte böbrek gecikmiş nefrogram verir.\n4. **Nükleer Tıp:** MAG3 tübüler sekresyonla atılır ve bozuk böbrekte DTPA'dan üstündür. Lasix testinde T1/2 > 20 dk ise gerçek mekanik obstrüksiyondur.\n5. **Özel Popülasyon:** Gebe ve çocuklarda radyasyonsuz alternatif T2-MR ürografidir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Üriner obstrüksiyonun radyolojik değerlendirmesinde kullanılan yöntemler ve özellikleri ile ilgili hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "Ultrasonografi ilk değerlendirme yöntemidir.", "explanation": "A seçeneği doğrudur: İlk basamak triyaj modalitesidir."},
                    {"key": "B", "text": "Kontrassız helikal BT akut taş şüphesinde altın standarttır.", "explanation": "B seçeneği doğrudur: En duyarlı ve özgül yöntemdir."},
                    {"key": "C", "text": "Lasix sintigrafisinde T1/2 süresinin 5 dakikanın altında olması mekanik tıkanıklığı kanıtlar.", "explanation": "C seçeneği YANLIŞTIR: T1/2 < 10 dakika obstrüksiyon OLMADIĞINI gösterir; obstrüksiyon için T1/2 > 20 dakika olmalıdır."},
                    {"key": "D", "text": "Tc-99m MAG3 tübüler sekresyonla atıldığı için üremik hastalarda da iyi sonuç verir.", "explanation": "D seçeneği doğrudur: Ekstraksiyonu çok yüksektir."},
                    {"key": "E", "text": "MR ürografi gebe kadınlarda radyasyonsuz inceleme avantajı sunar.", "explanation": "E seçeneği doğrudur: Fetal radyasyon riski yoktur."}
                ],
                "C"
            ),
            make_cloze(
                "Diüretikli sintigrafide T1/2 boşalma süresi on dakikanın altında ise sistemde mekanik obstrüksiyon bulunmadığı kabul edilir.",
                "on dakikanın altında",
                "Non-obstrüktif drenajı simgeleyen zaman eşiği"
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-11-s80",
        "title": "Ürodinamik İncelemeler ve Basınç-Akım Çalışmaları",
        "content": "Alt üriner sistem (mesane çıkımı) obstrüksiyonlarının objektif, kesin ve altın standart tanısı Ürodinamik Basınç-Akım Çalışmaları (Pressure-Flow Study) ile konur. Yalnızca hastanın şikayetlerine veya serbest üroflowmetri eğrisine bakılarak mekanik darlık ile zayıf detrüsör kasılması birbirinden ayırt edilemez. İnceleme esnasında mesaneye ve rektuma yerleştirilen çift lümenli basınç kateterleri ile detrüsör basıncı (Pdet) ve eş zamanlı idrar akım hızı (Q) kaydedilir. Miksiyon esnasında yüksek detrüsör basıncına rağmen (örneğin Pdet.Qmax > 40-50 cmH2O) düşük idrar akım hızı (Qmax < 10 ml/sn) saptanması kesin mekanik **mesane çıkım obstrüksiyonunu (BOO)** kanıtlar. Bu veriler Abrams-Griffiths nomogramında 'obstrükte alan' içine düşer.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "70 yaşında erkek hastada serbest üroflowmetride maksimum akım hızı 7 ml/sn (düşük) bulunuyor. Hastanın BPH nedeniyle mi yoksa detrüsör kas zaafiyeti (hipoaktif detrüsör) nedeniyle mi bu zayıf akıma sahip olduğu anlaşılamıyor.",
                "Bu ayrımı kesin ve objektif olarak yapacak en güvenilir tanısal test nedir?",
                [
                    {
                        "text": "Basınç-akım ürodinami çalışması; eş zamanlı detrüsör basıncı ve idrar debisini ölçerek yüksek basınç-düşük akım kombinasyonuyla mekanik obstrüksiyonu kanıtlar.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Basınç-akım çalışması kas gücü ile çıkım direncini ayıran tek objektif altın standarttır."
                    },
                    {
                        "text": "Akciğer grafisi çekerek diyafram yüksekliğini ölçmek.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Akciğer grafisinin mesane çıkım obstrüksiyonunu gösterme yeteneği yoktur."
                    },
                    {
                        "text": "Hastaya su içirip idrar rengini gözlemlemek.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. İdrar rengi mekanik darlık ile kas güçsüzlüğü ayrımını veremez."
                    }
                ]
            ),
            make_recall(
                "İnfravezikal çıkım obstrüksiyonu ile detrüsör kas tembelliğini kesin olarak ayırt eden ürodinamik inceleme hangisidir?",
                "Basınç-akım çalışmasıdır (pressure-flow study).",
                "Detrüsör basıncı ile akım hızını eş zamanlı ölçen yöntem"
            )
        ]
    })

    return slides
