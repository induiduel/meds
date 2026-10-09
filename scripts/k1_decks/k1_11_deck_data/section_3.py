# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-11-s21",
        "title": "Kronik İnfravezikal Obstrüksiyon: Kompansasyon Evresi",
        "content": "Kronik alt üriner sistem obstrüksiyonunun başlangıç aşaması kompanzasyon evresidir. Bu evrede prostat veya üretra seviyesindeki artmış çıkım direncini yenebilmek amacıyla mesane detrüsör kası hipertrofiye uğrar. Frank-Starling mekanizmasına benzer şekilde detrüsör hücreleri daha kuvvetli kasılmalar üreterek mesanedeki idrarı tamamen boşaltmayı başarır. Bu evrenin en kritik patognomonik özelliği, işeme sonrasında mesanede rezidüel idrar kalmamasıdır (PVR = 0 ml). Ancak detrüsör kası yüksek dirence karşı kasılırken erkenden yorulur; işeme süresi uzar, idrar akım hızı (Qmax) azalır, atım mesafesi kısalır ve idrar kalibrasyonu incelir. Hasta idrarını kesik kesik yapmaya başlar fakat henüz mesane tam boşalabilmektedir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Kronik infravezikal obstrüksiyonun kompanzasyon evresinde detrüsör hipertrofisi sayesinde mesanede postmiksiyonel rezidüel idrar kalmaz.",
                "rezidüel idrar kalmaz",
                "Erken evredeki tam boşalma başarısını düşününüz"
            ),
            make_chain(
                "Detrüsör Kompansasyon Mekanizması",
                [
                    "1. Çıkım Direnci: Prostatik veya üretral lümende mekanik tıkanıklık oluşması",
                    "2. Duvar Gerilimi: Mesane içi miksiyon basıncının telafi edici yükselişi",
                    "3. Miyosit Hipertrofisi: Detrüsör kas liflerinin kalınlaşarak güç üretmesi",
                    "4. Tam Boşalma: Rezidüel idrar kalmaksızın idrarın dışarı atılması"
                ]
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-11-s22",
        "title": "Kronik İnfravezikal Obstrüksiyon: İrritasyon ve Konjesyon Evresi",
        "content": "Obstrüksiyon sürdükçe sürekli yüksek basınca maruz kalan mesane mukozasında venöz konjesyon ve submukozal ödem gelişir. Bu ödemli ve konjesyone mukoza aşırı hassaslaşarak mesane dolum hissiyatını bozar. Hasta henüz mesane tam dolmadan çok şiddetli işeme hissi duymaya başlar. Klinik tabloda irritatif alt üriner sistem semptomları (LUTS) ön plana geçer: Gündüz sık idrara çıkma (pollaküri), gece idrara kalkma (noktüri), ani sıkışma hissi (urgency) ve ağrılı işeme (dizüri). Bu evrede detrüsör hipertrofisi maksimuma ulaşmıştır ancak kas liflerinde yorgunluk belirginleşir. Detrüsör kasılması erken sonlandığı için mesane tabanında az miktarda (genellikle 50 ml'den az) rezidüel idrar birikmeye başlar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Kronik infravezikal obstrüksiyonun irritasyon evresinde ortaya çıkan pollaküri, noktüri ve urgency semptomlarının temel patofizyolojik nedeni hangisidir?",
                [
                    {"key": "A", "text": "Mesane mukozasındaki venöz göllenme, ödem ve aşırı duyarlılık", "explanation": "A seçeneği doğrudur: Yüksek intravezikal basınç submukozal konjesyon ve ödem yaparak gerilme reseptörlerini erkenden uyarır."},
                    {"key": "B", "text": "Mesane kapasitesinin 1000 ml'nin üzerine çıkması", "explanation": "B seçeneği yanlıştır: Bu durum ileri dekompansasyon evresine aittir."},
                    {"key": "C", "text": "Detrüsör kasında tam atrofi ve felç gelişmesi", "explanation": "C seçeneği yanlıştır: İrritasyon evresinde kas henüz hipertrofiktir."},
                    {"key": "D", "text": "Üreteral peristaltizmin retrograd yöne dönmesi", "explanation": "D seçeneği yanlıştır: Üreter dinamikleri mesane irritasyon semptomunu doğrudan açıklamaz."},
                    {"key": "E", "text": "Böbrek tübüllerinde ADH duyarlılığının aşırı artması", "explanation": "E seçeneği yanlıştır: Obstrüksiyonda ADH direnci gelişir, artış olmaz."}
                ],
                "A"
            ),
            make_recall(
                "İrritasyon ve konjesyon evresinde saptanan postmiksiyonel rezidüel idrar hacmi genelde hangi sınırın altındadır?",
                "Genellikle 50 ml'nin altındadır.",
                "Erken dönemdeki mililitre sınırını anımsayınız"
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-11-s23",
        "title": "Kronik İnfravezikal Obstrüksiyon: Dekompansasyon Evresi",
        "content": "Obstrüksiyon giderilmezse detrüsör kasının kompanse etme gücü tükenir ve dekompansasyon evresi başlar. Sürekli yüksek basınca karşı çalışan düz kas lifleri dejenere olur, aralarına bağ dokusu infiltre eder ve kasılma yeteneği çöker. Miksiyon esnasında detrüsör yeterli basınç oluşturamaz ve miksiyon yarıda kalır. Her işeme sonrası mesanede yüksek miktarda (sıklıkla 500 ml'nin üzerinde) rezidüel idrar kalır. Mesane kapasitesi 1-2 litreye kadar ulaşabilir (kronik retansiyon). Mesane içi basınç üretral sfinkter kapanma direncini aştığında idrar damla damla sızar; buna taşma inkontinansı (işeme taşması / overflow incontinence) denir. Aşırı gerilen mesane duvarı üreterotrigonal bileşkeyi deforme ederek vezikoüreteral reflüye ve bilateral böbrek yetmezliğine zemin hazırlar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "İnfravezikal Obstrüksiyon Evreleri Karşılaştırması",
                "Kompansasyon Evresi",
                "Detrüsör güçlü hipertrofi gösterir, miksiyon tamdır, rezidüel idrar hacmi 0 ml düzeyindedir.",
                "Dekompansasyon Evresi",
                "Detrüsör tükenmiş ve atoniktir, taşma inkontinansı izlenir, rezidüel idrar hacmi 500 ml üzerindedir."
            ),
            make_cloze(
                "Dekompansasyon evresinde mesane içi aşırı basıncın sfinkter direncini yenmesiyle damla damla kontrolsüz idrar kaçırma tablosuna tasma inkontinansi adı verilir.",
                "tasma inkontinansi",
                "Mesanenin dolup taşmasıyla karakterize istemsiz kaçırma tipi"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-11-s24",
        "title": "Mesane Duvarındaki Histopatolojik ve Biyomekanik Dönüşüm",
        "content": "İnfravezikal obstrüksiyonda intravezikal basınç artışı ve gerilme mesane duvarında kronolojik bir histopatolojik yeniden şekillenme (remodeling) başlatır. Erken saatlerde mukozada inflamatuar infiltrasyon ve epitel proliferasyonu izlenir. Birinci haftanın sonunda submukozada fibroblast aktivasyonu baskın hale gelir. İkinci haftanın sonunda ise düz kas hücrelerinde yoğun hipertrofi meydana gelir. Ancak bu süreçte en kritik biyomekanik dönüşüm, ekstraselüler matrikste Tip III kollajen liflerinin orantısız artışıdır. Elastik liflerin yerini rijit Tip III kollajenin alması mesane kompliyansını (esneyebilirlik) dramatik şekilde düşürür. Mesane düşük basınçta idrar depolayabilen elastik bir rezervuar olmaktan çıkıp kalın, sert ve yüksek basınçlı rijit bir küreye dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Dönem", "Baskın Hücresel Yanıt", "Biyomekanik Sonuç"],
                [
                    [
                        {"text": "İlk Günler", "isMasked": False, "hint": ""},
                        {"text": "İnflamasyon ve mukozal epitel proliferasyonu", "isMasked": True, "hint": "Yüksek basınca karşı ilk hücresel savunma tepkisi"},
                        {"text": "Mukozal kalınlaşma", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "1. Hafta Sonu", "isMasked": False, "hint": ""},
                        {"text": "Submukozal fibroblast proliferasyonu", "isMasked": True, "hint": "Bağ dokusu sentezleyen temel hücrelerin uyarımı"},
                        {"text": "Matriks sentezinde artış", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "2. Hafta Sonu", "isMasked": False, "hint": ""},
                        {"text": "Düz kas hipertrofisi ve Tip III kollajen artışı", "isMasked": True, "hint": "Kas kalınlaşması ve rijit fibriler protein birikimi"},
                        {"text": "Kompliyansta belirgin azalma", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Kronik mesane çıkım obstrüksiyonunda duvar esnekliğini yok ederek kompliyansı düşüren temel kollajen alt tipi hangisidir?",
                "Tip III kollajendir.",
                "Skarlarda ve rijit fibroziste artan kollajen tipi"
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-11-s25",
        "title": "Trabekülasyon, Selül, Sakkül ve Mesane Divertikülü Gelişimi",
        "content": "İntravezikal basıncın normalin 2 ila 4 katına çıkması mesane lümeninde tipik morfolojik değişikliklere neden olur. Detrüsör kas demetleri basınca direnmek için kalınlaşarak kabarık çizgiler halinde lümene doğru fırlar; bu kaba kafes görünümüne trabekülasyon denir. Hipertrofiye uğramış komşu kas demetleri arasında kalan zayıf bölgelerde, artan hidrostatik basıncın etkisiyle mesane mukozası dışarıya doğru fıtıklaşmaya başlar. Bu mukozal ceplerin küçük olanlarına selül denir. Selüller perivezikal yağ dokusu ve peritona doğru büyüyüp genişledikçe sakkül ve nihayetinde gerçek mesane divertiküllerini oluşturur. Mesane divertikülleri kendi kas tabakasından yoksun (yalnızca mukoza ve seroza içeren) sahte divertiküllerdir; bu nedenle kasılamazlar, içlerindeki idrarı boşaltamazlar, kronik staz, taş ve enfeksiyon yuvası haline gelirler.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Mesane Duvarı Fıtıklaşma Aşamaları",
                [
                    "1. Trabekülasyon: Hipertrofik detrüsör kas demetlerinin lümende kabarması",
                    "2. Selül: Kas demetleri arasındaki zayıf noktalardan mukozanın dışa cepleşmesi",
                    "3. Sakkül: Selüllerin perivezikal yağ dokusuna doğru derinleşmesi",
                    "4. Divertikül: Kas tabakası içermeyen geniş mukozal fıtık kesesi oluşumu"
                ]
            ),
            make_branching(
                "Sistoskopi yapılan 72 yaşında BPH tanılı erkek hastada mesane duvarında yoğun kafes benzeri kalınlaşmış kas demetleri ve aralarında dışarıya fıtıklaşmış 3 cm boyutunda geniş mukozal keseler saptanıyor.",
                "Bu keselerin (mesane divertikülü) patolojik özelliği ve klinik riski nedir?",
                [
                    {
                        "text": "Duvarda aktif kas tabakası bulunmaz; idrar stazı, enfeksiyon ve sekonder taş oluşumuna yol açar.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Mesane edinsel divertikülleri detrüsör katından yoksundur; aktif kasılamadıkları için staz ve taş yuvasıdır."
                    },
                    {
                        "text": "Kalınlaşmış düz kas tabakası sayesinde mesaneden daha kuvvetli kasılarak idrarı boşaltır.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Divertiküller kas tabakası içermez, yalancı divertiküldür ve kasılamazlar."
                    },
                    {
                        "text": "Renal pelvise doğru idrarı aktif pompalayarak hidronefrozu engeller.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Divertikülün böbreğe idrar pompalama veya hidronefrozu önleme görevi yoktur."
                    }
                ]
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-11-s26",
        "title": "İkincil Vezikoüreteral Reflü (VUR) Patofizyolojisi",
        "content": "Normal bir üriner sistemde intramural üreter mesane duvarı içinden oblik bir tünel şeklinde geçer. Mesane idrarla dolup intravezikal basınç arttıkça, bu basınç tünelin tavanını tabanına doğru bastırarak üreter ağzını kapatır ve pasif bir flap-valv mekanizmasıyla reflüyü önler. Ancak kronik infravezikal obstrüksiyonda gelişen dekompansasyon evresinde mesane duvarı aşırı gerilir ve incelir. Üreterotrigonal mimari bozulur, intramural tünelin boyu kısalır ve oblik açısı kaybolur. Ayrıca trabekülasyon ve divertiküller üreter orifisinin hemen yanında geliştiklerinde valv desteğini tamamen yok eder. Sonuç olarak, mesanedeki yüksek basınçlı ve sıklıkla enfekte idrar miksiyon sırasında geriye doğru üretere ve böbreğe kaçar (sekonder VUR). Bu durum bilateral hidroüreteronefrozu hızlandırır ve renal parankimde yıkıcı basınç hasarı üretir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "İnfravezikal obstrüksiyonda mesane duvar gerilimi intramural üreter tünelini kısaltarak sekonder vezikoüreteral reflü gelişimine yol açar.",
                "vezikoüreteral reflü",
                "İdrarın mesaneden geriye üretere ve böbreğe kaçış patolojisi"
            ),
            make_quiz(
                "Kronik mesane çıkım obstrüksiyonunda sekonder vezikoüreteral reflü (VUR) oluşumunun temel anatomik mekanizması hangisidir?",
                [
                    {"key": "A", "text": "Mesane duvar gerilmesiyle intramural oblik üreter tünelinin kısalması ve valv mekanizmasının bozulması", "explanation": "A seçeneği doğrudur: Normalde oblik seyreden intramural tünel gerilmeyle dikleşir, kısalır ve flap-valv kapanamaz hale gelir."},
                    {"key": "B", "text": "Üreter orifislerinin aşırı büzülerek komplet tıkanması", "explanation": "B seçeneği yanlıştır: Bu tıkanıklık yapar, reflü yapmaz."},
                    {"key": "C", "text": "Detrüsör kasında parasempatik inervasyonun aşırı artması", "explanation": "C seçeneği yanlıştır: Sinir uyarımı tünel geometrisindeki mekanik bozulmayı açıklamaz."},
                    {"key": "D", "text": "Renal pelvisteki fornikslerin yırtılarak idrarı retroperitona sızdırması", "explanation": "D seçeneği yanlıştır: Bu pyelointerstisyel reflüdür, VUR değildir."},
                    {"key": "E", "text": "Prostat bezinin üreteral orifisleri fiziksel olarak yukarı itmesi", "explanation": "E seçeneği yanlıştır: Prostat üretra çıkımındadır, üreter orifislerini yukarı itmez."}
                ],
                "A"
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-11-s27",
        "title": "Nörojenik Mesane ve Detrüsör-Sfinkter Dissinerjisi (DSD)",
        "content": "Fonksiyonel infravezikal obstrüksiyonların en tehlikeli örneği suprasakral spinal kord lezyonlarında görülen detrüsör-sfinkter dissinerjisidir (DSD). Normal fizyolojide miksiyon esnasında ponsun miksiyon merkezinin kontrolünde detrüsör kasılırken, eksternal çizgili üretral sfinkter eş zamanlı olarak gevşer ve dirençsiz bir idrar akımı sağlanır. Servikal veya torakal kord yaralanmalarında, multipl sklerozda veya spina bifidalı hastalarda bu koordinasyon kopar. Detrüsör kasılarak yüksek basınç üretirken, eksternal sfinkter de eş zamanlı olarak şiddetle kasılır (dissinerji). Bu tablo 'kapalı bir kapıya karşı kasılma' anlamına gelir. İntravezikal basınç 100 cmH2O seviyelerini aşarak üst üriner sisteme iletilir; süratle VUR, bilateral hidroüreteronefroz ve nefron kaybına yol açar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Miksiyon Koordinasyonu Karşılaştırması",
                "Normal Sinerjik Miksiyon",
                "Detrüsör kasılırken eksternal sfinkter tam gevşer; idrar düşük intravezikal basınçla tamamen atılır.",
                "Detrüsör-Sfinkter Dissinerjisi (DSD)",
                "Detrüsör kasılırken eksternal sfinkter de kasılır; 100 cmH2O üstü aşırı basınç böbreği tehdit eder."
            ),
            make_recall(
                "Detrüsör kasılması esnasında eksternal üretral sfinkterin gevşeyemeyip kasılmasıyla oluşan yüksek riskli nörojenik duruma ne ad verilir?",
                "Detrüsör-sfinkter dissinerjisi (DSD).",
                "Kas ve kapakçık arasındaki uyumsuzluğu tanımlayan terim"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-11-s28",
        "title": "İnfravezikal Obstrüksiyonun Üretra ve Prostat Dokusuna Etkileri",
        "content": "Tıkanıklık eksternal üretral meatus veya üretra düzeyinde olduğunda, yüksek hidrostatik basınç üretra lümenini ve komşu prostatik dokuyu da harap eder:\n\n- **Üretral Değişiklikler:** Obstrüksiyonun proksimalinde üretral lümende aşırı distansiyon ve duvar incelmesi gelişir. Sürekli gerilme ve eşlik eden enfeksiyon üretra duvarında rüptüre, periüretral idrar ekstravazasyonuna, periüretral apselere ve kronik üretro-kutanöz fistüllere ('süzgeç üretra') yol açabilir.\n- **Prostatik Değişiklikler:** Yüksek intraüretral basınç idrarın prostatik duktuslara ve asinüslere geri kaçmasına (intraprostatik reflü) neden olur. Enfekte veya kristal içeren idrarın duktuslara girmesi prostatik kanallarda dilatasyon, kronik prostatit, prostat apsesi ve duktal taş oluşumu ile sonuçlanır. Benzer reflü mekanizması ejakülatuar kanallar yoluyla epididime ulaşarak tekrarlayan akut epididimo-orşit ataklarını tetikler.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Etkilenen Organ", "Temel Patolojik Süreç", "Nihai Komplikasyon"],
                [
                    [
                        {"text": "Üretra Duvarı", "isMasked": False, "hint": ""},
                        {"text": "Aşırı distansiyon ve duvar incelmesi", "isMasked": True, "hint": "Lümen gerilmesi ve doku zayıflaması"},
                        {"text": "Periüretral apse ve fistül oluşumu", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Prostatik Duktuslar", "isMasked": False, "hint": ""},
                        {"text": "İntraprostatik idrar reflüsü ve kanal dilatasyonu", "isMasked": True, "hint": "İdrarın bez kanallarına geri kaçışı"},
                        {"text": "Prostatit, prostat apsesi ve duktus taşları", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Vaz Deferens / Epididim", "isMasked": False, "hint": ""},
                        {"text": "İntralüminal yüksek basınçla retrograd bakteri iletimi", "isMasked": True, "hint": "Kanal boyunca geriye doğru enfeksiyon yayılımı"},
                        {"text": "Tekrarlayan epididimo-orşit", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Yüksek intraüretral basınç sonucu idrarın prostatik kanallara geri kaçışına intraprostatik reflü denir ve bu durum prostatit gelişiminde kilit rol oynar.",
                "intraprostatik reflü",
                "İdrarın prostat bez kanallarına retrograd dolması"
            )
        ]
    })

    # Slide 29 (CHECKPOINT 3)
    slides.append({
        "id": "k1-11-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Alt Üriner Sistem Obstrüksiyonunun Evreleri ve Mesane Mimarisi",
        "content": "Alt üriner sistem obstrüksiyonunun patolojik seyrini ve mesane yanıtını özetleyen kritik dönüm noktası:\n\n1. **Evreler:** Kompansasyon evresinde detrüsör hipertrofisiyle rezidüel idrar kalmaz (PVR=0). İrritasyon evresinde konjesyon ve ödem nedeniyle pollaküri/noktüri gelişir, PVR < 50 ml'dir. Dekompansasyon evresinde kas gücü tükenir, PVR > 500 ml olur, taşma inkontinansı ve sekonder VUR başlar.\n2. **Histopatoloji:** Basınç artışıyla 2. hafta sonunda düz kas hipertrofisi ve Tip III kollajen artışı izlenir; bu durum mesane kompliyansını yok eder.\n3. **Morfoloji:** Yüksek basınç trabekülasyona, kas aralarından fıtıklaşan mukozal selüllere, sakküllere ve kas tabakası olmayan yalancı divertiküllere yol açar.\n4. **Fonksiyonel Tehdit:** Nörojenik mesanede detrüsör-sfinkter dissinerjisi aşırı yüksek basınç (>100 cmH2O) üreterek üst sistemi hızla harap eder.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "İnfravezikal Obstrüksiyonun Klinik Aşamaları",
                [
                    "1. Kompansasyon: Detrüsör hipertrofisi ve sıfır rezidüel idrar",
                    "2. İrritasyon: Mukozal konjesyon, LUTS semptomları ve hafif rezidü",
                    "3. Dekompansasyon: Detrüsör yetmezliği, 500 ml üstü retansiyon ve taşma inkontinansı",
                    "4. Sekonder Hasar: VUR gelişimi, bilateral hidronefroz ve üremi"
                ]
            ),
            make_quiz(
                "Kronik alt üriner sistem obstrüksiyonunda 'dekompansasyon evresini' kompanzasyon evresinden ayıran en temel klinik bulgu hangisidir?",
                [
                    {"key": "A", "text": "Postmiksiyonel rezidüel idrarın 500 ml'nin üzerine çıkması ve taşma inkontinansı", "explanation": "A seçeneği doğrudur: Kompansasyonda rezidüel idrar sıfır iken dekompansasyonda belirgin retansiyon (>500 ml) ve taşma görülür."},
                    {"key": "B", "text": "Mesane duvar kalınlığının tamamen normale dönmesi", "explanation": "B seçeneği yanlıştır: Duvar kalınlaşması ve fibrozis devam eder."},
                    {"key": "C", "text": "Rezidüel idrarın tamamen ortadan kalkması", "explanation": "C seçeneği yanlıştır: Bu kompanzasyon evresinin özelliğidir."},
                    {"key": "D", "text": "Glomerüler filtrasyon hızının iki katına çıkması", "explanation": "D seçeneği yanlıştır: Dekompansasyonda GFR azalır ve azotemi gelişir."},
                    {"key": "E", "text": "Tip III kollajen liflerinin tamamen parçalanması", "explanation": "E seçeneği yanlıştır: Tip III kollajen artışı kalıcı fibrozise yol açar."}
                ],
                "A"
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-11-s30",
        "title": "Dekompanse Mesanede İrreversibilite Kavramı ve Tedaviye Direnç",
        "content": "Üriner obstrüksiyonun klinik yönetiminde en kritik uyarılardan biri dekompansasyon evresindeki gecikmedir. Dekompanse aşamaya gelmiş bir mesanede obstrüksiyon (örneğin prostat ameliyatı ile) cerrahi olarak tamamen ortadan kaldırılsa bile, mesane fonksiyonlarında her zaman beklenen klinik düzelme gerçekleşmez. Bunun başlıca nedeni, detrüsör miyositlerinin geri dönüşümsüz olarak atrofiye uğraması, sinir uçlarının (intramural pleksus) bası iskemisiyle dejenere olması ve kas demetlerinin yerini masif Tip III kollajen fibrozisinin almasıdır. Bu hastalar obstrüksiyon açıldıktan sonra da idrarlarını tam boşaltamazlar (miyojenik atoni) ve kalıcı temiz aralıklı kateterizasyon (TAK) ihtiyacı duyabilirler. Bu nedenle cerrahi tedavi, mesane dekompanse olmadan ve kompliyans yok olmadan önce planlanmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "75 yaşında hasta, 10 yıldır ihmal edilmiş BPH öyküsüyle başvuruyor. Mesanede 1200 ml idrar ve bilateral hidronefroz saptanıyor. Başarılı bir prostat rezeksiyonu (TUR-P) yapılmasına rağmen postoperatif 1. ayda hasta hala idrar yapamıyor ve mesanede 600 ml rezidü kalıyor.",
                "Bu tablonun altta yatan geri dönüşümsüz fizyopatolojik mekanizması nedir?",
                [
                    {
                        "text": "Detrüsör miyosit atrofisi ve masif Tip III kollajen fibrozisi sonucu kalıcı miyojenik detrüsör atonisi gelişmiştir.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Dekompanse evrede kas dokusunun fibrozise yenik düşmesi kalıcı atoniye yol açar; cerrahi tıkanıklığı açsa da mesane kasılamaz."
                    },
                    {
                        "text": "Üretral sfinkterin aşırı kasılarak idrar akımını tamamen durdurması.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. TUR-P sonrası anatomik tıkanıklık kalkmıştır, sorun sfinkter spazmı değil mesane kasının atonisidir."
                    },
                    {
                        "text": "Böbreklerin idrar üretimini tamamen durdurması.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Mesanede 600 ml rezidü birikmesi böbreğin idrar ürettiğini ancak mesanenin boşaltamadığını gösterir."
                    }
                ]
            ),
            make_recall(
                "Dekompanse evrede tıkanıklık cerrahiyle açılsa dahi mesane kasılmasının geri dönmemesine yol açan geri dönüşümsüz patolojik süreç nedir?",
                "Detrüsör atrofisi ve yoğun Tip III kollajen fibrozisidir.",
                "Kas kaybı ve sert bağ dokusu birikimi"
            )
        ]
    })

    return slides
