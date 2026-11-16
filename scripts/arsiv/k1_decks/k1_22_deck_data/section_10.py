# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 10: Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti (Slayt 91 - 100)
Checkpoint 10: Slayt 100
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: Protein-Enerji Malnütrisyonu (PEM): Epidemiyoloji ve Tipleri
    slides.append({
        "id": "k1-22-s91",
        "title": "Protein-Enerji Malnütrisyonu (PEM): Epidemiyoloji ve Tipleri",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 91,
        "narrative": (
            "Protein-Enerji Malnütrisyonu (PEM), özellikle gelişmekte olan ülkelerde 5 yaş altı çocuk ölümlerinin en az üçte birinde "
            "doğrudan veya dolaylı altta yatan küresel bir halk sağlığı trajedisidir. "
            "PEM temel olarak iki formda sınıflandırılır: "
            "1. **Birincil (Primer) PEM:** Yoksulluk, kıtlık, anne sütünün erken kesilmesi veya cehalet nedeniyle besinlere hiç ulaşılamamasıdır. "
            "2. **İkincil (Sekonder) PEM:** Altta yatan kistik fibrozis, çölyak, konjenital kalp hastalığı veya kronik enfeksiyon gibi patolojiler "
            "sonucu besinlerin emilememesi veya metabolik tüketimin aşırı artmasıdır. "
            "Dünya Sağlık Örgütü sınıflandırmasında PEM klinik ve antropometrik olarak başlıca iki zıt kutupta incelenir: "
            "Tüm besin ögelerinin ve kalorinin eksik olduğu **Marasmus** ve enerjiden ziyade saf proteinin eksik olduğu **Kvaşiorkor**."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Protein-Enerji Malnütrisyonu kalori ve proteinin birlikte tükendiği marasmus ile saf protein eksikliğiyle seyreden kvaşiorkor olmak üzere iki ana klinik kutba ayrılır.",
                "marasmus ile saf protein eksikliğiyle seyreden kvaşiorkor",
                "Çocukluk çağı beslenme yetersizliğinin iki temel klinik tablosu"
            ),
            make_table(
                "Protein-Enerji Malnütrisyonu (PEM) Etyolojik Sınıflandırması",
                ["PEM Tipi", "Temel Etyolojik Neden", "Klinik Örnek Durum", "Öncelikli Tedavi Yaklaşımı"],
                [
                    ["Primer (Birincil) PEM", "Gıdaya ulaşılamaması / Açlık", "Erken sütten kesilme ve yetersiz ek gıda", "Beslenme rehabilitasyonu"],
                    [
                        "Sekonder (İkincil) PEM",
                        {"text": "Malabsorpsiyon veya hipermetabolizma", "isMasked": True, "hint": "Emilim bozukluğu veya aşırı kalori sarfiyatı"},
                        "Kistik fibrozis, Çölyak veya Kanser",
                        "Altta yatan hastalığın tedavisi"
                    ]
                ]
            ),
            make_micro_quiz(
                "Pediatrik Protein-Enerji Malnütrisyonu (PEM) etyolojisi ve epidemiyolojisi ile ilgili aşağıdakilerden hangisi yanlıştır?",
                {
                    "A": "Primer PEM'in en yaygın nedeni yoksulluk ve anne sütünün vaktinden önce kesilmesidir",
                    "B": "Sekonder PEM'de altta yatan kronik bir organ hastalığı veya malabsorpsiyon mevcuttur",
                    "C": "Kvaşiorkor tablosunda sadece kalori eksiktir, plazma proteinleri tamamen normaldir",
                    "D": "Marasmus tablosu hem enerji hem proteinin uzun süreli genel yokluğuyla gelişir",
                    "E": "PEM gelişmekte olan ülkelerde 5 yaş altı çocuk ölümlerinin en önemli hazırlayıcısıdır"
                },
                "C",
                {
                    "A": "Doğrudur; Yoksulluk ve yanlış besleme primer PEM'i doğurur.",
                    "B": "Doğrudur; Çölyak ve Kistik Fibrozis klasik sekonder nedenlerdir.",
                    "C": "Yanlıştır; Kvaşiorkor'da temel defisit proteindir ve ağır hipoalbüminemi görülür.",
                    "D": "Doğrudur; Marasmus ağır kalori ve enerji yokluğudur.",
                    "E": "Doğrudur; Enfeksiyonlara yatkınlık yaratarak ölümleri katlar."
                }
            )
        ]
    })

    # Slayt 92: Marasmus: Ağır Kalori Açlığı ve 'İhtiyar Adam Yüzü'
    slides.append({
        "id": "k1-22-s92",
        "title": "Marasmus: Ağır Kalori Açlığı ve 'İhtiyar Adam Yüzü'",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 92,
        "narrative": (
            "Marasmus (Yunanca 'tükenme' / 'erime'), genellikle **yaşamın ilk 1 yılında**, anne sütünün erken kesilip "
            "son derece sulandırılmış hijyensiz mamalarla beslenen bebeklerde gelişen **ağır kalori ve enerji açlığıdır**. "
            "Patofizyolojik ve klinik özellikleri şunlardır: "
            "1. **Doku Yıkımı:** Vücut hayatta kalabilmek için kendi kas dokusunu (proteinlerini) ve cilt altı yağ dokusunu yakar. "
            "Yağ dokusu tamamen eridiğinde deri sarkar ve bollaşır ('torba pantolon' görünümü). "
            "2. **İhtiyar Adam (Faun) Yüzü:** Yanaklardaki emme yağ yastıkçıkları (Bichat yağ dokusu) en son eriyen yağdır; "
            "o da tükendiğinde temporal ve zigomatik kemikler fırlar, çocuk **buruşuk derili bir yaşlı insan yüzü** alır. "
            "3. **Ödem YOKTUR:** Marasmusun en ayırt edici kardinal özelliği **ödemin kesinlikle bulunmamasıdır** (godet bırakmaz). "
            "4. **Davranış:** Karaciğer fonksiyonları ve plazma albümini göreceli korunmuştur; bebek sürekli aç, huzursuz ve iştahlıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Marasmus tablosunun kvaşiorkordan en kritik ayırt edici klinik farkı ödemin kesinlikle bulunmamasıdır.",
                "ödemin kesinlikle bulunmamasıdır",
                "Godet bırakmayan ağır doku erimesi tablosu"
            ),
            make_before_after(
                "Marasmus vs Kvaşiorkor Klinik Görünüm",
                "Marasmus (Tükenmişlik Tablosu)",
                "Cilt altı yağ dokusu ve kaslar tamamen erimiştir; ödem kesinlikle yoktur; ihtiyar adam yüzü vardır; çocuk huzursuz ve açtır.",
                "Kvaşiorkor (Ödemli Malnütrisyon)",
                "Yaygın godet bırakan ödem vardır; karaciğer yağlanıp büyümüştür; saçta renk açılması (bayrak belirtisi) görülür; çocuk apatik ve iştahsızdır."
            ),
            make_active_recall(
                "Marasmus tablosunda çocuğun yüzünün 'ihtiyar adam' görünümü almasına yol açan en son eriyen anatomik yağ yastıkçığı nedir?",
                "Yanaklarda bulunan Bichat yağ yastıkçığıdır.",
                "Emme eylemini destekleyen bukkal yağ dokusu"
            )
        ]
    })

    # Slayt 93: Kvaşiorkor: Saf Protein Yetersizliği, Ödem ve Yağlı Karaciğer
    slides.append({
        "id": "k1-22-s93",
        "title": "Kvaşiorkor: Saf Protein Yetersizliği, Ödem ve Yağlı Karaciğer",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 93,
        "narrative": (
            "Kvaşiorkor (Gana dilinde 'yeni bir bebek doğduğunda tahttan indirilen ilk çocuğun hastalığı'), "
            "genellikle **1-4 yaş arasında**, yeni kardeş doğunca aniden sütten kesilip sadece karbonhidrattan (patates, manyok, pirinç lapası) "
            "zengin fakat **proteinden neredeyse tamamen yoksun** beslenen çocuklarda görülür. "
            "Patofizyolojik basamakları şunlardır: "
            "1. **Genelleşmiş Ödem:** Diyette amino asit olmayınca karaciğer albümin sentezleyemez; derin hipoalbüminemi sonucu plazma onkotik basıncı çöker "
            "ve sıvı interstisyuma kaçar. Ayak sırtından başlayıp yüze yayılan **godet bırakan gode ödem** (aydede yüzü) oluşur. "
            "2. **Hepatomegali (Yağlı Karaciğer):** Karaciğerde trigliseritler sentezlenir ancak onları kana taşıyacak apolipoproteinler "
            "üretilemediği için yağ hepatositlerde hapsolur; devasa hepatomegali gelişir. "
            "3. **Cilt ve Saç:** Ciltte soyulmalar (pul pul döküntü), saçlarda hipopigmentasyon ve renk açılması bantları (**Bayrak Belirtisi / Flag Sign**) görülür. "
            "4. **Apatik ve İştahsız:** Çocuk çevreye tamamen ilgisiz, hüzünlü ve aşırı iştahsızdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Kvaşiorkor tablosunda karaciğerde sentezlenen trigliseritleri kana taşıyacak apolipoprotein üretilemediği için yağlı karaciğer gelişir.",
                "yağlı karaciğer",
                "Hepatik trigliserit hapsine bağlı organ büyümesi"
            ),
            make_table(
                "Marasmus ile Kvaşiorkor'un Karşılaştırmalı Tanı Tablosu",
                ["Klinik Bulgu / Parametre", "Marasmus", "Kvaşiorkor", "Temel Biyolojik Neden"],
                [
                    ["Temel Eksiklik", "Kalori ve Protein (Genel Açlık)", "Saf Protein Eksikliği", "Karbonhidrat bol, amino asit yok"],
                    [
                        "Periferik Ödem",
                        "Kesinlikle Yoktur",
                        {"text": "Daima Vardır (Kardinal Bulgudur)", "isMasked": True, "hint": "Hipoalbüminemiye bağlı onkotik basınç çökmesi"},
                        "Düşük albümin ve hidrostatik kaçış"
                    ],
                    ["Karaciğer Büyüklüğü", "Normal", "Hepatomegali (Yağlı Karaciğer)", "Apolipoprotein sentezlenememesi"],
                    ["Yüz Görünümü", "İhtiyar Adam (Kuru/Kırışık)", "Aydede Yüzü (Ödemli)", "Ödem sıvısının dağılımı"],
                    ["Davranış / İştah", "Huzursuz, Sürekli Aç", "Apatik, Hüzünlü, İştahsız", "Nörotransmitter disfonksiyonu"],
                    ["Saç Değişikliği", "Genellikle normal", "Bayrak Belirtisi (Bant bant açılma)", "Dönemsel protein açlığı"]
                ]
            ),
            make_micro_quiz(
                "Kvaşiorkor hastası bir çocukta belirgin hepatomegali ve karaciğer yağlanması (steatoz) görülmesinin temel patofizyolojik mekanizması nedir?",
                {
                    "A": "Çocuğun aşırı miktarda doymuş hayvansal yağ tüketmesi",
                    "B": "Karaciğerde biriken trigliseritleri dolaşıma taşıyacak apolipoproteinlerin protein eksikliği nedeniyle sentezlenememesi",
                    "C": "Safra kesesinin konjenital yokluğu nedeniyle safranın karaciğerde göllenmesi",
                    "D": "A vitamini fazlalığına bağlı hepatotoksisite",
                    "E": "Karaciğer parankiminde glikojen sentaz enziminin aşırı çalışması"
                },
                "B",
                {
                    "A": "Yanlıştır; Kvaşiorkor hastaları yağ değil sadece karbonhidrat tüketir.",
                    "B": "Doğrudur; Apolipoprotein sentezi çöktüğü için VLDL yapılamaz ve yağ hepatositte birikir.",
                    "C": "Yanlıştır; Safra anomalisiyle ilgisi yoktur.",
                    "D": "Yanlıştır; Bilakis A vitamini eksiktir.",
                    "E": "Yanlıştır; Yağ birikiminin nedeni apolipoprotein yokluğudur."
                }
            )
        ]
    })

    # Slayt 94: Ağır Akut Malnütrisyon (SAM) Yönetimi ve Yeniden Besleme Sendromu
    slides.append({
        "id": "k1-22-s94",
        "title": "Ağır Akut Malnütrisyon (SAM) Yönetimi ve Yeniden Besleme Sendromu",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 94,
        "narrative": (
            "Ağır Akut Malnütrisyon (SAM) tablosundaki bir çocuğu tedavi ederken yapılan en ölümcül hata "
            "**'çocuğa hemen yüksek kalorili ve bol proteinli besin yüklemektir'**. "
            "SAM yönetiminde DSÖ'nün 10 altın kuralı uygulanır: "
            "1. **İlk 24-48 Saat (Stabilizasyon):** Ölümcül üçlü olan **Hipoglisemi, Hipotermi ve Dehidratasyon** derhal önlenmelidir. "
            "Çocuk asla üşütülmemeli, sık aralıklarla %10 glukoz ve F-75 (düşük protein ve sodyumlu özel formül) ile beslenmelidir. "
            "2. **Yeniden Besleme Sendromu (Refeeding Syndrome) Tehdidi:** Uzun süre aç kalan vücuda aniden yüksek glukoz verilirse "
            "muazzam bir insülin deşarjı olur. İnsülin kandaki fosfat, potasyum ve magnezyumu hücre içine sokar; "
            "sonuçta derin **hipofosfatemi**, kardiyak arrest, solunum yetmezliği ve ani ölüm gelişir! "
            "3. **Demir Tedavisi Yasağı:** Akut fazda ve enfeksiyon varken **asla demir başlanmaz!** "
            "Serbest demir bakteriyel çoğalmayı ve sepsisi patlatır; demir ancak çocuk toparlanıp kilo almaya başladığında (Rehabilitasyon fazı) eklenir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Ağır akut malnütrisyonlu bir çocuğa aniden yüksek karbonhidrat verildiğinde insülin etkisiyle gelişen ve ölüme yol açan tabloya yeniden besleme sendromu denir.",
                "yeniden besleme sendromu",
                "Hücre içine fosfat kaçışıyla seyreden metabolik çöküş tablosu"
            ),
            make_causal_chain(
                "Yeniden Besleme (Refeeding) Sendromunun Ölümcül Mekanizması",
                [
                    "1. Kronik Açlık Hali: Vücut katabolik evrededir; hücre içi fosfat ve potasyum depoları boştur.",
                    "2. Ani Karbonhidrat Yüklemesi: Çocuğa hızlıca yüksek kalorili şekerli besin veya mama verilir.",
                    "3. Masif İnsülin Patlaması: Pankreas yüksek miktarda insülin salgılar; glukozla beraber fosfat hücreye çekilir.",
                    "4. Ağır Hipofosfatemi ve Arrest: Kanda serbest fosfat tükenir, ATP yapılamaz; diyafram felci ve kalp durması gelişir."
                ]
            ),
            make_micro_quiz(
                "Ağır akut malnütrisyon (SAM) nedeniyle acil servise getirilen 2 yaşındaki bir çocuğun ilk stabilizasyon aşamasında aşağıdakilerden hangisinin yapılması KESİNLİKLE KONTRENDİKEDİR?",
                {
                    "A": "Vücut ısısını korumak için çocuğu sıcak tutmak ve hipotermiyi önlemek",
                    "B": "Hipoglisemiyi engellemek için ağızdan veya damardan seyreltik glukoz çözeltisi vermek",
                    "C": "Hemen yüksek doz intravenöz demir infüzyonu başlamak",
                    "D": "Düşük proteinli başlangıç formülü (F-75) ile beslemeyi başlatmak",
                    "E": "Olası enfeksiyonlar için geniş spektrumlu antibiyotik başlamak"
                },
                "C",
                {
                    "A": "Uygulanmalıdır; Hipotermi ölümcül üçlünün parçasıdır.",
                    "B": "Uygulanmalıdır; Hipoglisemi komayı tetikler.",
                    "C": "Kesinlikle Kontrendikedir; Akut fazda demir verilmesi serbest radikal hasarını ve ölümcül sepsis riskini artırır; demir rehabilitasyon fazına bırakılır.",
                    "D": "Uygulanmalıdır; Düşük proteinli F-75 refeeding sendromunu önler.",
                    "E": "Uygulanmalıdır; İmmünite çöktüğü için gizli sepsise karşı ampirik antibiyotik verilir."
                }
            )
        ]
    })

    # Slayt 95: Kritik Mikro Besin Eksiklikleri: A Vitamini, D Vitamini ve İyot
    slides.append({
        "id": "k1-22-s95",
        "title": "Kritik Mikro Besin Eksiklikleri: A Vitamini, D Vitamini ve İyot",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 95,
        "narrative": (
            "Gelişmekte olan ülkelerde kalori açığı olmasa bile tek yönlü beslenme sonucu **'Gizli Açlık' (Mikronütrient Eksiklikleri)** tablosu yaygındır: "
            "1. **A Vitamini Eksikliği:** Çocukluk çağı önlenebilir körlüğünün bir numaralı nedenidir. "
            "Korneada kuruluk (kseroftalmi), konjonktivada köpüksü keratin plakları (**Bitot Lekeleri**), gece körlüğü ve kızamık enfeksiyonlarında ölüm riskini artırır. "
            "Sağlık Bakanlığı riskli bölgelerde yüksek doz A vitamini kapsülü dağıtır. "
            "2. **D Vitamini Eksikliği:** Kemik mineralizasyon bozukluğu (**Raşitizm**). "
            "Kafatasında yumuşama (**Kraniyotabes**), kostakondral bileşkelerde şişlikler (**Raşitik Tespih**), el bileklerinde genişleme ve O-bacak deformitesi yapar. "
            "Türkiye'de her bebeğe doğumdan itibaren **400 IU/gün D vitamini profilaksisi** ücretsiz verilir. "
            "3. **İyot Eksikliği:** Konjenital hipotiroidi ve geri dönülmez zeka geriliği (**Endemik Kretinizm**). "
            "Tuzların zorunlu iyotlanmasıyla kontrol altına alınmıştır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "D vitamini eksikliğine bağlı raşitizm tablosunda kafatası kemiklerinin pinpon topu gibi içe çöküp esnemesine kraniyotabes denir.",
                "kraniyotabes",
                "Yenidoğan ve erken süt çocuğunda oksipital yumuşama bulgusu"
            ),
            make_table(
                "Temel Mikro Besin Eksiklikleri ve Ulusal Sağlık Profilaksileri",
                ["Mikro Besin", "Eksikliğinde Gelişen Ağır Patoloji", "Karakteristik Klinik İşaret", "Ulusal Sağlık Politikası"],
                [
                    [
                        "A Vitamini",
                        "Kseroftalmi ve önlenebilir körlük",
                        {"text": "Bitot lekeleri ve gece körlüğü", "isMasked": True, "hint": "Konjonktivadaki gümüşi köpüksü keratin birikintileri"},
                        "Riskli bölgelerde periyodik mega doz"
                    ],
                    ["D Vitamini", "Raşitizm (Kemik yumuşaması)", "Kraniyotabes ve raşitik tespih", "Tüm bebeklere 400 IU/gün (1 yaşına kadar)"],
                    ["İyot", "Kretinizm ve derin zeka geriliği", "Büyüme duraklaması ve guatr", "Sofra tuzlarının zorunlu iyotlanması"],
                    ["Demir", "Demir eksikliği anemisi", "Solukluk, pika ve bilişsel duraklama", "4. aydan itibaren profilaktik damla"]
                ]
            ),
            make_active_recall(
                "Türkiye'de Sağlık Bakanlığı'nın yürüttüğü ulusal profilaksi programına göre sağlıklı term doğan her bebeğe doğumdan itibaren kaç ünite D vitamini başlanır?",
                "Günde 400 IU (3 damla) D vitamini başlanır ve en az 1 yaşına kadar aralıksız sürdürülür.",
                "D vitamini damlasının günlük profilaktik dozu"
            )
        ]
    })

    # Slayt 96: Bebek Öncülüğünde Beslenme (BLW - Baby-Led Weaning)
    slides.append({
        "id": "k1-22-s96",
        "title": "Bebek Öncülüğünde Beslenme (BLW - Baby-Led Weaning)",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 96,
        "narrative": (
            "Son yıllarda pediatride yaygınlaşan **Bebek Öncülüğünde Beslenme (Baby-Led Weaning - BLW)**, "
            "tamamlayıcı beslenmeye kaşıkla püre yedirmek yerine, bebeğin kendi kendine parmaklarıyla tutabileceği "
            "yumuşak gıdaları (finger foods) kendi hızında yemesine izin veren bir besleme felsefesidir. "
            "1. **BLW'nin Ön Koşulları:** Bebek mama sandalyesinde desteksiz dik oturabilmeli, başını tam kontrol edebilmeli, "
            "nesneleri eliyle kavrayıp ağzına götürebilmeli ve ekstrüzyon refleksi kaybolmuş olmalıdır (asla 6 aydan önce uygulanamaz). "
            "2. **Faydaları:** İnce motor becerileri ve el-göz koordinasyonunu geliştirir; bebeğin tokluk sinyallerini tanımasını sağlayarak "
            "ileride **obeziteye karşı koruyucu öz-düzenleme (self-regulation)** kazandırır. "
            "3. **Güvenlik İlkesi:** Besinler bebeğin avucundan taşacak uzunlukta (çubuk şeklinde) ve dudak/damak arasında ezilebilecek "
            "yumuşaklıkta (buharda pişmiş havuç, brokoli, muz) olmalıdır. Tane kuruyemiş, çiğ elma, üzüm gibi yuvarlak sert besinler yasaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bebeğin püre yerine kendi kendine kavrayabileceği yumuşak gıdalarla beslenmesini hedefleyen yönteme bebek öncülüğünde beslenme denir.",
                "bebek öncülüğünde beslenme",
                "Kaşıksız ve bebeğin inisiyatifinde yürütülen alternatif beslenme tarzı"
            ),
            make_table(
                "Gagging (Öğürme) ile Choking (Boğulma) Arasındaki Hayati Fark",
                ["Kriter", "Öğürme Refleksi (Gagging)", "Hava Yolu Boğulması (Choking)"],
                [
                    ["Patoloji Tipi", "Fizyolojik koruyucu refleks", "Ölümcül hava yolu tıkanıklığı"],
                    [
                        "Ses ve Solunum",
                        {"text": "Gürültülü, öksürüklü, sesli", "isMasked": True, "hint": "Hava yolunun açık olduğunu gösteren sesli öksürük"},
                        "Sessiz, nefes alamama, afoni"
                    ],
                    ["Cilt Rengi", "Kızarma (Yüzde kırmızılık)", "Siyanoz (Morarma)"],
                    ["Ebeveyn Tutumu", "Sakin kalıp müdahale etmemek", "Acil Heimlich / Sırt vuruşu müdahalesi"]
                ]
            ),
            make_micro_quiz(
                "Bebek Öncülüğünde Beslenme (BLW) uygulanan bir bebekte gıdanın dilin arkasına değmesiyle sesli öksürme ve öğürme (gagging) başladığında ebeveynin yapması gereken en doğru yaklaşım nedir?",
                {
                    "A": "Derhal bebeğin ağzına parmağını sokup körlemesine besini aramalıdır",
                    "B": "Bebeği baş aşağı çevirip sırtına vurmalıdır",
                    "C": "Sakin kalıp bebeğin dik oturur pozisyonda kendi öksürüğüyle besini öne atmasına izin vermelidir",
                    "D": "Bebeğe hızlıca bir bardak su içirmelidir",
                    "E": "BLW yöntemini derhal terk edip ömür boyu sıvı mamaya dönmelidir"
                },
                "C",
                {
                    "A": "Tehlikelidir; Körlemesine parmak sokmak besini trakeaya itebilir.",
                    "B": "Gereksizdir; Boğulma değil öğürme refleksidir.",
                    "C": "Doğrudur; Öğürme fizyolojik korumadır, sesli öksürük hava yolunun açık olduğunu gösterir; bebek dik tutularak izlenir.",
                    "D": "Tehlikelidir; Sıvı aspirasyona neden olabilir.",
                    "E": "Gereksizdir; Çiğneme eğitiminin normal parçasıdır."
                }
            )
        ]
    })

    # Slayt 97: 1-2 Yaş Arası Beslenme: Aile Sofrasına Entegrasyon
    slides.append({
        "id": "k1-22-s97",
        "title": "1-2 Yaş Arası Beslenme: Aile Sofrasına Entegrasyon",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 97,
        "narrative": (
            "1 yaşını dolduran çocuk artık bebeklikten oyun çağı çocukluğuna adım atmıştır: "
            "1. **Aile Sofrası Birlikteliği:** Çocuk artık ailenin tükettiği tencere yemeklerini yiyebilir. "
            "Yemeklerin az tuzlu, baharatsız ve sağlıklı pişirme yöntemleriyle (haşlama, fırınlama) hazırlanması tüm ailenin sağlığını korur. "
            "2. **Porsiyon Kontrolü:** 1-2 yaşındaki bir çocuğun mide kapasitesi erişkinin dörtte biri kadardır (~250-300 ml). "
            "Çocuğa erişkin tabağı konulmamalı, her ana yemekten kendi yaşının kaşığı kadar (ör. 1-2 yemek kaşığı) porsiyonlanmalıdır. "
            "3. **Süt Tüketim Sınırı (Süt Anemisi Tehlikesi):** 1 yaşından sonra pastörize inek sütü verilebilir; ancak günlük miktar "
            "**kesinlikle 400-500 ml'yi (2 su bardağını) geçmemelidir!** "
            "Aşırı süt içen çocuk tokluk hissettiği için katı gıdaları ve eti reddeder; sonuçta derin bir **'Süt Anemisi' (Demir Eksikliği)** gelişir. "
            "4. **Sofra Disiplini:** Ekran (tablet, televizyon) karşısında yedirme alışkanlığı kesinlikle yasaklanmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bir yaşından sonra çocuklarda günlük inek sütü tüketiminin 500 ml'yi aşması katı gıda reddine ve süt anemisine yol açar.",
                "süt anemisine",
                "Aşırı inek sütü tüketimiyle tetiklenen demir eksikliği tablosu"
            ),
            make_micro_quiz(
                "15 aylık bir çocuğun günlük beslenmesinde inek sütü tüketimi ile ilgili en doğru pediatrik yaklaşım hangisidir?",
                {
                    "A": "Günde en az 1.5 litre inek sütü içirilerek kalsiyum ihtiyacı karşılanmalıdır",
                    "B": "İnek sütü günde en fazla 400-500 ml ile sınırlandırılmalı, aşırı tüketimin demir emilimini ve iştahı bozduğu bilinmelidir",
                    "C": "İnek sütü 5 yaşına kadar kesinlikle verilmemelidir",
                    "D": "İnek sütünün içine bal ve bisküvi katılarak biberonla gece boyu verilmelidir",
                    "E": "Çocuk yemek yemediğinde tüm öğünler inek sütüyle ikame edilmelidir"
                },
                "B",
                {
                    "A": "Tehlikelidir; 1.5 litre süt ağır demir eksikliği anemisi yapar.",
                    "B": "Doğrudur; Maksimum 400-500 ml önerilir; fazlası tokluk yaparak et ve sebze alımını engeller.",
                    "C": "Yanlıştır; 1 yaşından sonra ölçülü verilebilir.",
                    "D": "Yanlıştır; Çürük, obezite ve refrakter iştahsızlık yapar.",
                    "E": "Yanlıştır; Katı gıdaya geçişi baltalar."
                }
            ),
            make_active_recall(
                "Küçük çocuklarda aşırı inek sütü tüketimine bağlı gelişen 'süt anemisi' tablosunun iki temel patolojik nedeni nedir?",
                "Sütün iştahı kapatıp demir zengini et ve sebzelerin yenmesini engellemesi ve yüksek kalsiyumun bağırsakta demir emilimini yarışmalı bloke etmesidir.",
                "İştah baskılanması ve kalsiyum-demir yarışması"
            )
        ]
    })

    # Slayt 98: Emzirmenin 2 Yaşına Kadar Sürdürülmesi ve İmmünolojik Devamlılık
    slides.append({
        "id": "k1-22-s98",
        "title": "Emzirmenin 2 Yaşına Kadar Sürdürülmesi ve İmmünolojik Devamlılık",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 98,
        "narrative": (
            "Dünya Sağlık Örgütü ve UNICEF'in bebek beslenmesindeki altın standardı: "
            "**'İlk 6 ay yalnızca anne sütü, ardından uygun tamamlayıcı besinlerle birlikte emzirmenin 2 yaşına kadar veya ötesine sürdürülmesidir'**. "
            "İkinci yılda emzirmenin devam etmesinin biyolojik gerekçeleri şunlardır: "
            "1. **Besinsel Katkı:** 12-24 ay arasında anne sütü çocuğun günlük enerji ihtiyacının yaklaşık **%30-35'ini**, "
            "protein ihtiyacının **%40'ını**, A vitamini ihtiyacının **%45'ini** ve C vitamini ihtiyacının **%95'ini** tek başına karşılayabilir. "
            "2. **Hastalık Döneminde Hayat Kurtarıcı Rol:** Çocuk ishal, pnömoni veya ateşli hastalık geçirirken tüm katı gıdaları reddetse bile "
            "anne memesini emmeye devam eder; böylece ölümcül dehidratasyon ve akut kilo kaybı önlenir. "
            "3. **Süregelen İmmün Koruma:** İkinci yılda anne sütündeki sekretuvar IgA ve laktoferrin konsantrasyonu azalmaz, "
            "aksine süt hacmi azaldığı için konsantrasyon olarak daha da yoğunlaşır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Dünya Sağlık Örgütü ilk 6 ay tek başına anne sütünü ve ardından tamamlayıcı besinlerle birlikte emzirmenin iki yaşına kadar sürdürülmesini önerir.",
                "iki yaşına kadar",
                "Optimum nörogelişimsel ve immünolojik laktasyon süresi hedefi"
            ),
            make_table(
                "Yaşamın 2. Yılında Anne Sütünün Günlük Gereksinimleri Karşılama Oranları",
                ["Besin Ögesi / Vitamin", "Anne Sütünün Karşılama Yüzdesi", "Klinik Önemi"],
                [
                    ["C Vitamini", "%95", "Enfeksiyon direnci ve demir emilimi"],
                    [
                        "A Vitamini",
                        {"text": "%45", "isMasked": True, "hint": "Yarıya yakın oranda göz ve mukoza sağlığı desteği"},
                        "Kseroftalmi ve mukozal bariyer koruması"
                    ],
                    ["Protein", "%40", "Yüksek biyoyararlanımlı büyüme amino asitleri"],
                    ["Toplam Enerji", "%30 - 35", "Aktif oyun çağında güvenilir kalori desteği"]
                ]
            ),
            make_active_recall(
                "İkinci yaşta akut gastroenterit veya pnömoni geçiren bir süt çocuğunda anne sütünün en kritik hayat kurtarıcı fonksiyonu nedir?",
                "Katı gıdaların reddedildiği enfeksiyon döneminde hidrasyonu sağlaması, dehidratasyonu ve ani kilo kaybını önlemesidir.",
                "Hastalıkta sıvı dengesi ve dehidratasyon kalkanı"
            )
        ]
    })

    # Slayt 99: Çocuk Beslenmesinde DSÖ Global Hedefleri ve Ulusal Sağlık Politikaları
    slides.append({
        "id": "k1-22-s99",
        "title": "Çocuk Beslenmesinde DSÖ Global Hedefleri ve Ulusal Sağlık Politikaları",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 99,
        "narrative": (
            "Bebek ve çocuk beslenmesi yalnızca ailevi bir tercih değil, toplumların geleceğini belirleyen stratejik bir kalkınma göstergesidir. "
            "DSÖ ve Dünya Sağlık Asamblesi (WHA) 2025/2030 hedefleri doğrultusunda ülkemizde yürütülen temel halk sağlığı programları şunlardır: "
            "1. **Bebek Dostu Sağlık Kuruluşları Programı:** Doğum yapılan hastanelerin %95'inden fazlası Bebek Dostu unvanına sahiptir; "
            "amaç ilk 6 ay sadece anne sütü oranını küresel hedef olan **en az %50'nin üzerine çıkarmaktır**. "
            "2. **D Vitamini ile Büyüyorum Projesi:** Tüm yenidoğanlara 1 yıl boyunca ücretsiz profilaktik 400 IU D vitamini sağlanarak raşitizm sıfırlanmıştır. "
            "3. **Demir Gibi Türkiye Projesi:** 4-12 ay arası tüm bebeklere ücretsiz profilaktik demir damlası dağıtılarak demir eksikliği anemisiyle savaşılır. "
            "4. **Tuzun İyotlanması:** Konjenital guatr ve zeka geriliğini önlemek amacıyla sofra tuzlarına zorunlu potasyum iyodat eklenir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de yürütülen 'Demir Gibi Türkiye' projesi kapsamında dördüncü aydan itibaren tüm bebeklere profilaktik demir damlası ücretsiz sağlanır.",
                "dördüncü aydan itibaren",
                "Fetal demir depoları tükenirken başlatılan ulusal anemi profilaksisi zamanı"
            ),
            make_table(
                "Türkiye'de Yürütülen Temel Çocuk Sağlığı Profilaksi Programları",
                ["Ulusal Program Adı", "Hedef Yaş Grubu", "Verilen Destek / İlaç", "Önlenen Hastalık"],
                [
                    ["D Vitamini Desteği", "0 - 12 Ay Arası", "400 IU/gün D3 Vitamini", "Nutrisyonel Raşitizm"],
                    [
                        "Demir Profilaksisi",
                        "4 - 12 Ay Arası",
                        {"text": "Profilaktik elementer demir damlası", "isMasked": True, "hint": "Kansızlığı önleyen damla takviyesi"},
                        "Demir Eksikliği Anemisi"
                    ],
                    ["Tuzun İyotlanması", "Tüm Toplum", "Potasyum İyodatlı Tuz", "Kretinizm ve İyot Eksikliği Guatrı"],
                    ["Yenidoğan Taramaları", "İlk 72 Saat (Topuk Kanı)", "Guthrie Kartı Taraması", "Fenilketonüri, Hipotiroidi, Kistik Fibrozis, SMA"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı'nın ulusal çocuk sağlığı programlarına göre term doğan sağlıklı bebeklerde profilaktik demir desteğine başlama zamanı hangisidir?",
                {
                    "A": "Doğar doğmaz ilk gün",
                    "B": "1. ayın sonunda",
                    "C": "4. ayın tamamlanmasıyla birlikte",
                    "D": "1 yaşından sonra",
                    "E": "Yalnızca kan tahlilinde hemoglobin 10'un altına düşerse"
                },
                "C",
                {
                    "A": "Yanlıştır; İlk günlerde fetal demir boldur, gerek yoktur.",
                    "B": "Yanlıştır; Prematüreler hariç term bebekte erkendir.",
                    "C": "Doğrudur; Term bebekte depolar 4-6 ayda tükendiği için 4. ayda profilaktik başlanır.",
                    "D": "Yanlıştır; 1 yaş çok geçtir, anemi yerleşir.",
                    "E": "Yanlıştır; Bu tedavi değil profilaksi programıdır, tahlil beklenmeden başlanır."
                }
            )
        ]
    })

    # Slayt 100: [TEKRAR SAYFASI - CHECKPOINT 10] Bebek Beslenmesi Büyük Özeti
    slides.append({
        "id": "k1-22-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Bebek Beslenmesi Büyük Özeti",
        "section": "Çocukluk Çağı Malnütrisyonu ve Bebek Beslenmesi Büyük Özeti",
        "slideNumber": 100,
        "narrative": (
            "Tebrikler! Kurul 1 Bebek Beslenmesi dersinin 100 slaytlık eksiksiz tıp eğitim yolculuğunu başarıyla tamamladınız. "
            "Bu son checkpoint sayfasında, tüm dersin en kritik sınav ve klinik spotlarını özetliyoruz: "
            "1. **Altın İlk 6 Ay:** Yalnızca anne sütü; su dahi verilmez. Kolostrum ilk aşıdır (sIgA, laksatif). "
            "2. **Hormonal Motor:** Prolaktin süt yapar (gece pik yapar), oksitosin süt fışkırtır ve uterusu kasar. "
            "3. **Anne Sütü vs İnek Sütü:** %60 whey / %40 kazein (yumuşak pıhtı). Beta-laktoglobulin insan sütünde ASLA yoktur! "
            "Demir emilimi anne sütünde %50, inek sütünde %10'dur. İnek sütünün renal solüt yükü (308 mOsm/L) dehidratasyon yapar. 1 yaşından önce inek sütü yasaktır! "
            "4. **Emzirme & Saklama:** Ten tene temas ilk 30-60 dakikada başlar. 3-3-3 kuralı: oda ısısında 3 saat, dolapta 3 gün, dondurucuda 3 ay. "
            "Mastitte emzirmeye KESİNLİKLE devam edilir! Galaktozemide mutlak kesilir. "
            "5. **Tamamlayıcı Beslenme:** 6. ayda başlar; 3 gün kuralı uygulanır; bal (botulizm), tuz, bakla 1 yaşa kadar yasaktır. "
            "6. **Malnütrisyon:** Marasmus = kalori açlığı, doku erimesi, ödem YOK. Kvaşiorkor = saf protein eksikliği, godet bırakan ÖDEM, yağlı karaciğer."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "flashcards": [
            make_flashcard(
                "k1-22-fc-s100-1",
                "Marasmus ile Kvaşiorkor arasındaki en temel patofizyolojik ayrım ve kardinal fizik muayene bulgusu nedir?",
                "Marasmus kalori açlığı olup ödem kesinlikle yoktur; Kvaşiorkor saf protein eksikliği olup gode bırakan yaygın ödem mevcuttur.",
                "Tükenmişlik tablosu ile albümin kaybı ayrımı",
                "Malnütrisyon Ayırıcı Tanısı"
            ),
            make_flashcard(
                "k1-22-fc-s100-2",
                "Ağır Akut Malnütrisyonlu (SAM) bir çocuğa başlangıçta aniden yüksek karbonhidrat verildiğinde ölümcül kardiyak arreste yol açan tablo nedir?",
                "Yeniden Besleme (Refeeding) Sendromudur.",
                "Hücre içine masif fosfat kaymasıyla seyreden iyonik kriz",
                "Metabolik Komplikasyonlar"
            ),
            make_flashcard(
                "k1-22-fc-s100-3",
                "Dünya Sağlık Örgütü ve Sağlık Bakanlığı'nın bebek beslenmesinde önerdiği laktasyon süresi protokolü nedir?",
                "İlk 6 ay sadece anne sütü ve ardından tamamlayıcı besinlerle beraber 2 yaşına kadar emzirmenin sürdürülmesidir.",
                "Altı ay tek başına ve yirmi dört aya kadar destekli devam süresi",
                "Küresel Beslenme Standardı"
            )
        ],
        "interactiveElements": [
            make_table(
                "Bebek Beslenmesi Dersinin 10 Altın Kuralı",
                ["Kural No", "Temel İlke / Rehber", "Tıbbi Gerekçe"],
                [
                    ["Kural 1", "İlk 6 ay yalnızca anne sütü", "Tüm besin ve sıvı ihtiyacını eksiksiz karşılar"],
                    ["Kural 2", "İlk 30-60 dk içinde ten tene temas", "Oksitosin salgısı ve başarılı laktasyon başlangıcı"],
                    [
                        "Kural 3",
                        {"text": "İnek sütünde Beta-laktoglobulin var, anne sütünde YOK", "isMasked": True, "hint": "İnek sütü proteini alerjisinin temel sorumlusu"},
                        "Alerjenite ve mukozal tolerans"
                    ],
                    ["Kural 4", "Sağılmış sütte 3-3-3 kuralı", "3 saat oda, 3 gün buzdolabı, 3 ay dondurucu"],
                    ["Kural 5", "Mastitte emzirmeye devam edilir", "Kanal stazını çözmek ve apseyi önlemek"],
                    ["Kural 6", "Tam 6. ayda tamamlayıcı beslenme", "Enerji açığı ve tükenen fetal demir depoları"],
                    ["Kural 7", "1 yaşına kadar bal ve inek sütü YASAK", "İnfantil botulizm ve mikroskobik bağırsak kanaması"],
                    ["Kural 8", "Yeni gıdalarda 3 gün kuralı", "Alerji ve intoleransın kesin tespiti"],
                    ["Kural 9", "Marasmusta ödem YOK, Kvaşiorkorda ödem VAR", "Hipoalbüminemi ve onkotik basınç farkı"],
                    ["Kural 10", "Emzirme 2 yaşına kadar sürdürülür", "Süregiden immünite ve hastalıkta hidrasyon kalkanı"]
                ]
            )
        ]
    })

    return slides
