# -*- coding: utf-8 -*-
"""
Build High-Quality Academic Deck:
'learn-uriner-sistem-enfeksiyonlari-epidemiyoloji' (24 Slayt)
Kaynak: Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi
Uzman Tıbbi Mikrobiyoloji ve Enfeksiyon Hastalıkları Akademisyen Düzeyi
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_PATH = r"C:\Users\indui\.gemini\antigravity\brain\386176b3-c821-4f99-a837-6f25ae2aca35\scratch\deck_uriner_epidemiyoloji.json"

def make_slide(slide_num, title, subtitle, narrative, spot_onemli, spot_cikmis, practice_q):
    spots = [
        {"type": "warning", "badge": "🔴 ÖNEMLİ", "text": spot_onemli, "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU", "text": spot_cikmis, "color": "sky"}
    ]
    spot_pearls = [
        f"🔴 ÖNEMLİ: {spot_onemli}",
        f"🔵 ÇIKMIŞ SORU: {spot_cikmis}"
    ]
    
    # Format options for universal compatibility
    opts = []
    correct_key = practice_q.get("correctAnswer", "A")
    for opt in practice_q.get("options", []):
        if isinstance(opt, dict):
            opts.append(opt)
        elif isinstance(opt, str):
            # Parse 'A) Text' format if string
            k = opt[:1] if len(opt) > 1 and opt[1] in [')', '.', ':'] else "A"
            t = opt[3:].strip() if len(opt) > 2 and opt[1] in [')', '.', ':'] else opt
            opts.append({
                "key": k,
                "text": t,
                "isCorrect": (k == correct_key)
            })
            
    pq = {
        "id": practice_q["id"],
        "stem": practice_q.get("stem", practice_q.get("question", "")),
        "question": practice_q.get("question", practice_q.get("stem", "")),
        "options": opts,
        "correctAnswer": correct_key,
        "explanation": practice_q["explanation"],
        "topic": title,
        "discipline": "Tıbbi Mikrobiyoloji / Enfeksiyon Hastalıkları",
        "examYear": "Özgün Akademik Pekiştirme Sorusu",
        "isPracticeQuestion": True
    }

    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "content": narrative,
        "synthesisNarrative": narrative,
        "spots": spots,
        "spotPearls": spot_pearls,
        "relatedQuestions": [pq],
        "practiceQuestion": pq
    }

slides = []

# ==============================================================================
# SLAYT 1
# ==============================================================================
slides.append(make_slide(
    1,
    "Üriner Sistem Enfeksiyonlarının Tanımı, Sınıflandırılması ve Klinik Spektrumu",
    "Ürotelyal İnflamatuar Yanıt, Anatomik Lokalizasyon ve Semptomatik Yelpaze",
    """Üriner sistem enfeksiyonları (ÜSE), mikrobiyal patojenlerin idrar yollarını kolonize ve invaze etmesi sonucunda ürotelyal epitelde tetiklenen inflamatuar yanıtla karakterize, klinik tıpta en sık karşılaşılan enfeksiyon tablolarından biridir. İdrar yolu, normal koşullarda üretra meası hariç tutulduğunda steril bir ortamdır. Patojenlerin bu steril bariyeri aşarak mukozaya tutunması; bakteriüri (idrarda bakteri varlığı) ve piyüri (idrarda lökosit varlığı) ile belirginleşen dinamik bir konak savunma kaskadını başlatır.

Enfeksiyonun üriner traktus boyunca yerleştiği anatomik odağa göre temel klinik sınıflandırma yapılır. Alt üriner sistem enfeksiyonları üretrit ve mesane mukozasının inflamasyonu olan sistiti kapsarken; üst üriner sistem enfeksiyonları böbrek toplayıcı sistemini ve parankimini tutan akut veya kronik piyelonefriti ifade eder. Ayrıca enfeksiyon doğrudan parankimal organlara sınırlı kalmayıp prostatit veya epididimo-orşit gibi adneksiyel yapıları da içine alabilir. Klinik seyir bakımından enfeksiyonlar semptomatik veya tamamen asemptomatik olarak prezente olabilirler.

Hastalığın klinik semptom yelpazesi olağanüstü geniştir. Bir uçta hastanın günlük yaşamını hafif düzeyde etkileyen miksiyon sırasında geçici yanma hissi (dizüri) ve sık idrara çıkma yer alırken; diğer uçta böbrek parankiminde yaygın apse oluşumu, ürosepsis, sistemik bakteriyemi, septik şok ve ölüme kadar varabilen ağır tablolar izlenir. Bu nedenle her üriner sistem enfeksiyonu olgusu, hastanın yaşı, cinsiyeti, immün durumu ve anatomik yapısı göz önüne alınarak bir bütün olarak değerlendirilmelidir.""",
    "Üriner sistem enfeksiyonu sadece bakterinin idrarda varlığı değil, ürotelyal epitelin bu invazyona karşı geliştirdiği piyüri ile karakterize aktif inflamatuar yanıttır.",
    "Üst üriner sistem enfeksiyonu (piyelonefrit) ile alt üriner sistem enfeksiyonu (sistit) arasındaki en temel klinik ayrım; piyelonefritte tabloya yüksek ateş, titreme ve yan (flank) ağrısının eşlik etmesidir.",
    {
        "id": "prac-use-001",
        "stem": "Üriner sistem enfeksiyonlarının tanımı ve klinik sınıflandırması dikkate alındığında, aşağıdaki ifadelerden hangisi doğru bir klinik yaklaşımı yansıtır?",
        "options": [
            {"key": "A", "text": "Üriner sistem enfeksiyonu tanısı için yalnızca idrarda bakteri görülmesi yeterlidir, konak inflamatuar yanıtı aranmaz.", "isCorrect": False},
            {"key": "B", "text": "Mesane mukozasını tutan sistit tablosunda daima yüksek ateş, titreme ve flank ağrısı gibi sistemik toksisite bulguları beklenir.", "isCorrect": False},
            {"key": "C", "text": "Üst üriner sistem enfeksiyonları (akut piyelonefrit), böbrek parankiminin tutulumu nedeniyle sistemik inflamatuar bulgular ve yan ağrısı ile seyreder.", "isCorrect": True},
            {"key": "D", "text": "Asemptomatik seyreden tüm bakteriüri olgularında böbrek hasarını önlemek amacıyla derhal geniş spektrumlu antibiyotik başlanmalıdır.", "isCorrect": False},
            {"key": "E", "text": "Üriner sistemde üretrovezikal bileşkenin proksimalinde normal fizyolojik şartlarda yoğun bir kommensal bakteri florası bulunur.", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Piyelonefrit böbrek parankim ve toplayıcı sistemini tuttuğu için ateş, titreme ve yan ağrısı gibi sistemik bulgular oluşturur; sistitte ise inflamasyon mesane mukozasıyla sınırlı olduğundan sistemik ateş genellikle izlenmez. Sağlıklı bireylerde üretrovezikal bileşke proksimali sterildir."
    }
))

# ==============================================================================
# SLAYT 2
# ==============================================================================
slides.append(make_slide(
    2,
    "Bakteriüri, Piyüri ve İdrar Örnekleme Tekniklerinin Güvenilirliği",
    "Kontaminasyon Dinamikleri, Numune Toplama Yolları ve Yalancı Pozitiflikler",
    """Bakteriüri, idrarda mikroorganizmaların saptanması durumudur ve semptomatik bir enfeksiyonun bileşeni olabileceği gibi tamamen asemptomatik olarak da seyredebilir. Ancak idrarın mikrobiyolojik analizinde karşılaşılan en büyük tanısal handikap kontaminasyondur. Kontaminasyon; steril olan mesane idrarının dış ortamdan, üretra distalinden, perine, prepisyum veya vajinal sekresyonlardan kaynaklanan mikroorganizmalarla kirlenmesi halidir. Bu durum klinik olarak enfeksiyonu olmayan bir hastaya gereksiz antibiyotik verilmesine yol açabilir.

İdrar alma tekniğinin güvenilirliği, kontaminasyon olasılığını doğrudan belirleyen en kritik parametredir. Güvenilirlik hiyerarşisinde altın standart, cildin lokal dezenfeksiyonu sonrası doğrudan pubisin üzerinden mesaneye iğne ile girilerek yapılan 'suprapubik aspirasyon'dur; bu yöntemde kontaminasyon riski teorik ve pratik olarak sıfıra yakındır. İkinci sırada steril şartlarda uygulanan 'üretral kateterizasyon' yer alır. Poliklinik pratiğinde en yaygın kullanılan yöntem ise hastanın perine temizliğini takiben ilk gelen idrarı tuvalete yapıp idrar akımının ortasını topladığı 'orta akım idrarı' (clean-catch midstream) yöntemidir.

Piyüri, normal koşullarda idrarda bulunmayan veya mikroskopide büyük büyütme alanında (HPF) 5'ten az olan lökositlerin idrarda belirgin artışıdır ve ürotelyal epitelin inflamatuar yanıtının doğrudan göstergesidir. İdrar kültüründe yoğun bakteri üremesine rağmen mikroskopide hiç lökosit (piyüri) saptanmaması, tablonun gerçek bir ürotelyal enfeksiyondan ziyade numune alma aşamasındaki bir kontaminasyon olduğunu düşündüren en önemli mikrobiyolojik ipucudur.""",
    "Kontaminasyon riskinin en düşük olduğu idrar toplama yöntemi suprapubik aspirasyondur; idrar sedimentinde piyüri olmaksızın sadece bakteriüri görülmesi kuvvetle numune kontaminasyonunu gösterir.",
    "İdrar alma yöntemlerinin kontaminasyon açısından güvenilirlik sırası: Suprapubik aspirasyon > Üretral kateterizasyon > Orta akım idrarı şeklindedir.",
    {
        "id": "prac-use-002",
        "stem": "Poliklinik şartlarında üriner sistem enfeksiyonu şüphesiyle değerlendirilen bir hastanın idrar tetkikinde bol bakteri görülmesine karşın mikroskobik incelemede lökosit (piyüri) saptanmamıştır. Bu klinik tablo en yüksek olasılıkla aşağıdakilerden hangisini düşündürmelidir?",
        "options": [
            {"key": "A", "text": "Akut piyelonefrit erken evresi", "isCorrect": False},
            {"key": "B", "text": "İdrar numunesinin kontaminasyonu", "isCorrect": True},
            {"key": "C", "text": "Böbrek tüberkülozu", "isCorrect": False},
            {"key": "D", "text": "Karsinoma in situ", "isCorrect": False},
            {"key": "E", "text": "Üriner sistem obstrüktif taş hastalığı", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "Piyüri olmaksızın bakteriüri görülmesi enfeksiyondan ziyade idrar alma sırasındaki dış genital veya perineal kaynaklı kontaminasyonun en tipik göstergesidir. Gerçek ürotelyal invazyonda konağın inflamatuar yanıtı olarak daima piyüri eşlik eder."
    }
))

# ==============================================================================
# SLAYT 3
# ==============================================================================
slides.append(make_slide(
    3,
    "Anlamlı Bakteriüri Kavramı ve Sayısal Koloni Eşikleri",
    "Kass Kriterleri, Cinsiyete ve Klinik Tabloya Göre CFU/ml Standartları",
    """Anlamlı bakteriüri, idrar kültüründe saptanan bakterilerin perineal kontaminasyon sonucu mu yoksa gerçek bir ürotelyal enfeksiyon nedeniyle mi bulunduğunu ayırt etmek amacıyla geliştirilmiş nicel bir mikrobiyolojik kriterdir. Klasik olarak Edward Kass tarafından tanımlanan kriterlere göre, semptomsuz bir bireyde orta akım idrarında mililitrede 10^5 (100.000) koloni oluşturan birim (CFU/ml) veya daha fazla sayıda tek bir patojenin üremesi 'anlamlı bakteriüri' olarak kabul edilir.

Güncel enfeksiyon hastalıkları kılavuzları, hastanın cinsiyetine, semptom varlığına ve enfeksiyonun anatomik lokalizasyonuna göre bu eşik değerleri özelleştirmiştir. Tipik alt üriner sistem semptomları (dizüri, sık idrara çıkma) bulunan semptomatik kadınlarda, komplike olmayan akut sistit tablosunda orta akım idrarında 10^3 CFU/ml gibi daha düşük koloni sayıları dahi tanı koydurucu ve anlamlı kabul edilir. Buna karşılık kadınlarda akut komplike olmayan piyelonefritlerde 10^4 CFU/ml, altta yatan yapısal anomalisi olan komplike piyelonefritlerde ise 10^5 CFU/ml eşik değeri aranır.

Erkeklerde üretra anatomik olarak uzun olduğu için kontaminasyon olasılığı kadınlara göre çok daha düşüktür; bu nedenle semptomatik erkek hastaların orta akım idrarında 10^4 CFU/ml bakteri saptanması tanı için anlamlı kabul edilir. Ancak suprapubik aspirasyon ile doğrudan mesaneden alınan idrar numunelerinde durum radikal olarak değişir: Normalde tamamen steril olan mesaneden bu invaziv yöntemle elde edilen idrarda üreyen her sayıda bakteri (1 CFU/ml dahi olsa) kontaminasyon olarak nitelendirilemez ve mutlak enfeksiyon kanıtı olarak kabul edilir.""",
    "Suprapubik aspirasyon ile alınan idrarda herhangi bir sayıda (tek bir koloni dahi) bakteri üremesi istisnasız anlamlı bakteriüri kabul edilir.",
    "Semptomatik akut komplike olmayan sistitli kadınlarda orta akım idrarında anlamlı bakteriüri eşik değeri 10^3 CFU/ml iken, semptomatik erkekte bu sınır 10^4 CFU/ml'dir.",
    {
        "id": "prac-use-003",
        "stem": "İdrar yolu enfeksiyonu tanısında kullanılan anlamlı bakteriüri eşik değerleri ile ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?",
        "options": [
            {"key": "A", "text": "Kadınlarda akut komplike olmayan sistit: Orta akım idrarında >= 10^3 CFU/ml", "isCorrect": False},
            {"key": "B", "text": "Erkeklerde orta akım idrarı: >= 10^4 CFU/ml", "isCorrect": False},
            {"key": "C", "text": "Kadınlarda akut komplike olmayan piyelonefrit: Orta akım idrarında >= 10^4 CFU/ml", "isCorrect": False},
            {"key": "D", "text": "Suprapubik aspirasyon ile alınan idrar: Yalnızca >= 10^5 CFU/ml üreme olması halinde anlamlıdır", "isCorrect": True},
            {"key": "E", "text": "Asemptomatik kadınlarda iki ardışık orta akım idrarında: >= 10^5 CFU/ml", "isCorrect": False}
        ],
        "correctAnswer": "D",
        "explanation": "Suprapubik aspirasyon doğrudan steril mesaneden alındığı için kontaminasyon riski yoktur ve idrarda saptanan herhangi bir sayıda bakteri (1 CFU/ml dahi) anlamlı kabul edilir; 10^5 CFU/ml sınırı aranmaz."
    }
))

# ==============================================================================
# SLAYT 4
# ==============================================================================
slides.append(make_slide(
    4,
    "Asemptomatik Bakteriüri (ASB): Tanı Kriterleri ve Tedavi Endikasyonları",
    "Gereksiz Antibiyotik Direncinden Kaçınma ve Kesin Tedavi Gerektiren Klinik Durumlar",
    """Asemptomatik bakteriüri (ASB), hastada dizüri, pollaküri, ateş veya yan ağrısı gibi hiçbir üriner sistem semptomu bulunmamasına rağmen, uygun koşullarda alınmış orta akım idrar kültüründe mililitrede 10^5 CFU veya üzerinde aynı bakterinin üremesi durumudur. Kadınlarda tanı için genellikle en az 24 saat arayla alınmış iki ardışık idrar kültüründe aynı mikroorganizmanın üremesi istenirken, erkeklerde tek bir numunede 10^5 CFU/ml üreme yeterli kabul edilir.

Modern enfeksiyon hastalıkları ve antimikrobiyal yönetim ilkelerine göre, asemptomatik bakteriürisi olan genel popülasyonda antibiyotik tedavisi kesinlikle önerilmez. ASB varlığında asemptomatik hastaları tedavi etmek enfeksiyon sıklığını azaltmadığı gibi dirençli suşların (özellikle genişlemiş spektrumlu beta-laktamaz - GSBL üreten enterik bakterilerin) kolonizasyonuna, Clostridioides difficile enterokolitine ve yüksek maliyete yol açar.

Ders notunda vurgulandığı üzere, asemptomatik bakteriürinin tedavisiz bırakılamayacağı ve antimikrobiyal eradikasyonun zorunlu olduğu belirli istisnai hasta grupları mevcuttur: Gebe kadınlar (piyelonefrit ve preterm eylem riski nedeniyle), mukozal kanama riski taşıyan invaziv ürolojik girişim planlanan hastalar (ürosepsisi önlemek için), vezikoüreteral reflü veya skar riski olan çocuklar ve seçilmiş kırılgan yaşlı hastalar. Bu endikasyonlar haricinde (örneğin kalıcı idrar sondası olan asemptomatik yaşlılarda) antibiyotik verilmesi kontrendikedir.""",
    "Asemptomatik bakteriüride antibiyotik tedavisinin zorunlu olduğu iki majör kanıta dayalı durum: Gebeler ve mukozal kanama riski olan invaziv ürolojik girişim yapılacak hastalardır.",
    "Kalıcı üretral kateteri olan asemptomatik bir yaşlıda idrar kültüründe >10^5 CFU/ml bakteri üremesi durumunda antibiyotik tedavisi verilmez; gereksiz tedavi sadece dirençli patojen kolonizasyonuna yol açar.",
    {
        "id": "prac-use-004",
        "stem": "Aşağıdaki hasta gruplarından hangisinde asemptomatik bakteriüri (>10^5 CFU/ml) saptanması durumunda rutin antimikrobiyal tedavi verilmesi kesinlikle önerilmez?",
        "options": [
            {"key": "A", "text": "14 haftalık gebe kadın", "isCorrect": False},
            {"key": "B", "text": "Transüretral prostat rezeksiyonu (TUR-P) planlanan asemptomatik hasta", "isCorrect": False},
            {"key": "C", "text": "Kronik bakım evinde yaşayan, kalıcı üretral kateteri bulunan ve şikayeti olmayan 78 yaşındaki hasta", "isCorrect": True},
            {"key": "D", "text": "Vezikoüreteral reflü şüphesiyle takip edilen 2 yaşındaki çocuk", "isCorrect": False},
            {"key": "E", "text": "Rijit sistoskopi ve üreteral biyopsi uygulanacak olan hasta", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Kalıcı üretral kateteri olan veya kurumsal bakım alan asemptomatik yaşlı bireylerde bakteriüri kalıcı kolonizasyondur; antibiyotik vermek kolonizasyonu temizlemez aksine çoklu dirençli mikroorganizmaların gelişimine neden olur. Buna karşılık gebelerde ve mukozal kanamalı invaziv cerrahi öncesinde tedavi zorunludur."
    }
))

# ==============================================================================
# SLAYT 5
# ==============================================================================
slides.append(make_slide(
    5,
    "Piyüri ve Bakteriüri Etkileşimi: Steril Piyüri ve Kontaminasyon Ayrımı",
    "Lökositüri Mekanizması, Tüberküloz, Taş ve Kanser Tehdidi",
    """Piyüri, santrifüj edilmiş idrar sedimentinin mikroskobik incelenmesinde her büyük büyütme alanında (HPF) 5 veya daha fazla polimorfonükleer lökosit görülmesidir. İdrar çubuğu (strip) testlerinde lökosit esteraz pozitifliği de piyüriyi yansıtır. Piyüri, ürotelyumun bakteriyel invazyona, toksinlere veya yabancı cisimlere karşı geliştirdiği aktif hücresel yanıtın en dolaysız göstergesidir.

Piyüri olmaksızın sadece bakteriüri saptanması, hastanın immün yetmezlik veya aşırı nötropeni tablosunda olmadığı durumlarda, hemen daima numune alma esnasında dış genital organlardan karışan bir kontaminasyonun sonucudur. Tersine, idrarda belirgin piyüri olmasına rağmen standart besiyerlerinde (kanlı agar, EMB) hiçbir bakteriyel üremenin olmaması tablosuna 'Steril Piyüri' adı verilir.

Steril piyüri tespit edilen bir hastada klinisyen standart antibiyotik verip hastayı göndermemeli, derhal altta yatan spesifik patolojileri araştırmalıdır. Steril piyürinin en önemli üç nedeni: 1) Ürogenital Tüberküloz (Mycobacterium tuberculosis standart kültürde üremez; Lowenstein-Jensen besiyeri veya mikobakteriyel PCR gerekir), 2) Üriner sistem taşları (taşın mukozayı mekanik olarak tahriş etmesi sonucu lökosit dökülmesi), ve 3) Mesane tümörleri veya Karsinoma in situ (CIS) lezyonlarıdır. Ayrıca cinsel temasla bulaşan Chlamydia trachomatis, Ureaplasma ve Mycoplasma üretritleri de rutin idrar kültüründe üremeksizin piyüri oluşturur.""",
    "İdrar analizinde belirgin piyüri saptanmasına karşın rutin kültürde üreme olmaması (steril piyüri) durumunda akla ilk olarak Ürogenital Tüberküloz, Üriner Taş ve Malignite gelmelidir.",
    "Standart idrar kültüründe üreme olmaksızın piyüri (steril piyüri) saptanan bir hastada asidorezistan basil (ARB) ve idrar sitolojisi incelemesi yapılmalıdır.",
    {
        "id": "prac-use-005",
        "stem": "Polikliniğe idrarda yanma şikayetiyle başvuran hastanın tam idrar tahlilinde bol lökosit (piyüri) saptanmış, ancak tekrarlanan rutin idrar kültürlerinde hiçbir bakteri ürememiştir. Bu hastada öncelikle dışlanması gereken patolojiler hangi seçenekte eksiksiz verilmiştir?",
        "options": [
            {"key": "A", "text": "Ürogenital tüberküloz - Üriner sistem taşı - Mesane karsinoması", "isCorrect": True},
            {"key": "B", "text": "Diabetes insipidus - Polikistik böbrek hastalığı - Renal ven trombozu", "isCorrect": False},
            {"key": "C", "text": "Akut tübüler nekroz - Minimal değişiklik hastalığı - Amiloidoz", "isCorrect": False},
            {"key": "D", "text": "Glomerülonefrit - Renal hücreli karsinom - Basit böbrek kisti", "isCorrect": False},
            {"key": "E", "text": "Akut böbrek yetmezliği - İnkontinans - Üretral darlık", "isCorrect": False}
        ],
        "correctAnswer": "A",
        "explanation": "Bakteriürisiz piyüri (steril piyüri) tablosunda mutlaka ürogenital tüberküloz (M. tuberculosis standart kültürde üremez), üriner sistem taşı (mekanik mukozal erozyon) ve mesane tümörleri/karsinoma in situ araştırılmalıdır."
    }
))

# ==============================================================================
# SLAYT 6
# ==============================================================================
slides.append(make_slide(
    6,
    "Komplike ve Komplike Olmayan Üriner Sistem Enfeksiyonları",
    "Yapısal, Fonksiyonel ve Tedavi Bariyerlerinin Ayrımı",
    """Üriner sistem enfeksiyonları, hastanın anatomik yapısına ve tedaviye yanıtını etkileyen faktörlere göre 'komplike olmayan' (uncomplicated) ve 'komplike' (complicated) olarak iki temel kategoriye ayrılır. Bu ayrım, ampirik antibiyotik seçiminden tedavi süresine, görüntüleme gereksiniminden hastaneye yatış endikasyonuna kadar tüm klinik yönetim algoritmasını belirler.

Komplike olmayan ÜSE, üriner sisteminde hiçbir yapısal veya işlevsel anomali bulunmayan, böbrek fonksiyonları normal olan, gebe olmayan ve bilinen immün yetmezliği bulunmayan sağlıklı premenopozal kadınlarda görülen akut sistit veya hafif piyelonefrit ataklarını tanımlar. Bu olgularda etken ezici oranda (%75-95) floraya duyarlı Escherichia coli'dir ve kısa süreli (3-5 gün) oral antibiyotik rejimleri ile kalıcı hasar bırakmaksızın tam iyileşme sağlanır.

Komplike ÜSE ise bakteri bulaşma ve kolonizasyon ihtimalini artıran, enfeksiyonun üst sisteme yayılımını kolaylaştıran veya antibiyotik tedavisinin etkinliğini azaltan herhangi bir faktörün varlığında gelişen enfeksiyonlardır. Erkeklerde görülen tüm ÜSE'ler (anatomik uzunluk ve prostat varlığı nedeniyle), gebeler, çocuklar, yaşlılar, üriner kateteri olanlar, taş veya tümöre bağlı obstrüksiyonu bulunanlar, vezikoüreteral reflüsü (VUR) olanlar, böbrek nakli alıcıları, nörojenik mesane ve kontrolsüz diyabet hastalarındaki tüm enfeksiyonlar komplike kabul edilir. Bu grupta tedavi süresi daha uzundur ve etkenler çok daha dirençlidir.""",
    "Komplike olmayan ÜSE yalnızca anatomik/fonksiyonel anomalisi olmayan gebe dışı premenopozal sağlıklı kadınlarda tanımlanır; erkeklerdeki tüm ÜSE'ler aksine kanıtlanmadıkça komplike kabul edilir.",
    "Üriner sistemde yabancı cisim (kateter, nefrostomi), taş, nörojenik disfonksiyon, gebelik, immünsüpresyon veya anatomik darlık bulunması enfeksiyonu doğrudan 'komplike ÜSE' sınıfına sokar.",
    {
        "id": "prac-use-006",
        "stem": "Aşağıdaki hasta profillerinden hangisinde gelişen üriner sistem enfeksiyonu 'komplike olmayan ÜSE' kapsamında değerlendirilebilir?",
        "options": [
            {"key": "A", "text": "Nefrolitiyazis öyküsü olan ve yan ağrısı bulunan 45 yaşında erkek hasta", "isCorrect": False},
            {"key": "B", "text": "Bilinen herhangi bir kronik hastalığı ve anatomik anomalisi bulunmayan 24 yaşında gebe olmayan kadın", "isCorrect": True},
            {"key": "C", "text": "Tip 2 diyabeti ve nörojenik mesanesi olan 55 yaşında kadın hasta", "isCorrect": False},
            {"key": "D", "text": "Kalıcı foley sonda takılı olan 70 yaşında yatağa bağımlı erkek hasta", "isCorrect": False},
            {"key": "E", "text": "18 haftalık gebe olup dizüri tarifleyen 28 yaşında kadın hasta", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "Komplike olmayan ÜSE sadece üriner sistemde anatomik/fonksiyonel anomali veya taş bulunmayan, gebe olmayan, premenopozal sağlıklı erişkin kadınlarda tanımlanır. Erkek hastalar, gebeler, diyabetikler ve kateteri olanlar doğrudan komplike kategoridedir."
    }
))

# ==============================================================================
# SLAYT 7
# ==============================================================================
slides.append(make_slide(
    7,
    "ÜSE Terminolojisinde İnce Ayrımlar: Rekürrens, Re-enfeksiyon, Persistans ve Süpresyon",
    "Tedavi Sonrası Nüks Dinamikleri, Odak Varlığı ve Farmakolojik Stratejiler",
    """Üriner sistem enfeksiyonu geçiren hastalarda tedavinin tamamlanmasının ardından yeni semptomların ortaya çıkması farklı patofizyolojik süreçlerle açıklanır. Bu kavramlar doğru anlaşılmadığında tedavi başarısızlığı ile yeni temaslar birbirine karıştırılır. Başarılı bir antimikrobiyal tedavi kürünün ardından, genellikle iki haftadan daha kısa bir süre içerisinde aynı bakteriyel patojenle enfeksiyonun tekrarlamasına 'Rekürren Enfeksiyon (Nüks / Relaps)' adı verilir.

Buna karşılık 'Re-enfeksiyon', daha önce geçirilmiş enfeksiyonun tamamen eradike edilmesinden sonra, üriner sisteme dışarıdan (genellikle rektal floradan perineye ve üretraya) gelen tamamen yeni bir patojen suş ile ya da aynı suşun haftalar-aylar sonra yeniden bulaşmasıyla meydana gelen enfeksiyondur. 'Bakteriyel Persistans' ise üriner sistem içinde anatomik veya yabancı bir odakta (örneğin infekte bir böbrek taşı, struvit taşı, kronik bakteriyel prostatit odağı, üretral divertikül) bakterinin antibiyotiklerden korunarak canlı kalması ve tedavi biter bitmez aynı mikroorganizmanın yeniden üreyerek rekürrenslere yol açmasıdır.

Bu tablolara yönelik farmakolojik stratejiler de farklılaşır: 'Antimikrobiyal profilaksi', sık re-enfeksiyon geçiren bireylerde dışarıdan yeni bulaşları engellemek için düşük doz antibiyotik verilmesidir. 'Cerrahi antimikrobiyal profilaksi', mukozal bariyerin bozulacağı ameliyatlar öncesinde tek doz verilir. 'Antimikrobiyal süpresyon' ise cerrahi olarak çıkarılamayan veya eradike edilemeyen bir bakteriyel persistans odağının (örneğin opere edilemeyen taşın veya prostattaki kalsifikasyonun) büyümesini ve klinik enfeksiyon oluşturmasını baskılamak amacıyla sürekli düşük doz antibiyotik kullanılmasıdır.""",
    "Tedaviden sonraki 2 hafta içinde aynı patojenle tekrarlayan enfeksiyon rekürrens (bakteriyel persistans) lehine iken; farklı bir patojenle veya uzun süre sonra gelişen enfeksiyon re-enfeksiyondur.",
    "Eradike edilemeyen infekte böbrek taşı veya kronik prostatit gibi anatomik odaklarda bakterinin canlı kalıp klinik alevlenmeler yapmasını engellemek için uygulanan tedavi 'Antimikrobiyal Süpresyon'dur.",
    {
        "id": "prac-use-007",
        "stem": "Akut sistit atağı nedeniyle 7 günlük uygun antibiyotik tedavisi tamamlanan ve semptomları tamamen gerileyen bir kadın hastada, tedavinin bitiminden 8 gün sonra aynı antibiyotiğe duyarlılık profili gösteren birebir aynı E. coli suşu ile klinik enfeksiyon tekrarlamıştır. Bu tabloyu en iyi tanımlayan kavram ve altta yatan olası mekanizma aşağıdakilerden hangisidir?",
        "options": [
            {"key": "A", "text": "Re-enfeksiyon - Yeni bir fekal bulaş odağı", "isCorrect": False},
            {"key": "B", "text": "Rekürren enfeksiyon (Relaps) - Üriner sistemde bakteriyel persistans odağı", "isCorrect": True},
            {"key": "C", "text": "Nozokomiyal süperenfeksiyon - Pseudomonas kolonizasyonu", "isCorrect": False},
            {"key": "D", "text": "Asemptomatik bakteriüri - İmmün tolerans gelişimi", "isCorrect": False},
            {"key": "E", "text": "Steril piyüri - Karsinoma in situ gelişimi", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "Başarılı tedavi sonrası iki haftadan kısa sürede aynı mikroorganizma ile tablonun alevlenmesi 'rekürren enfeksiyon'dur ve üriner sistemde antibiyotiklerin ulaşamadığı bir bakteriyel persistans odağını (taş, anatomik anomali, prostat odağı) düşündürür."
    }
))

# ==============================================================================
# SLAYT 8
# ==============================================================================
slides.append(make_slide(
    8,
    "Üriner Sistem Enfeksiyonlarının Epidemiyolojisi ve Toplum Sağlığı Yükü",
    "Global Morbidite, Poliklinik/Acil Başvuruları ve Sağlık Bakanlığı Verileri",
    """Üriner sistem enfeksiyonları, dünya genelinde solunum yolu enfeksiyonlarından sonra ayaktan poliklinik ve acil servis başvurularına en sık neden olan ikinci enfeksiyon kümesidir. Hastalığın epidemiyolojik sıklığı, veri kaynaklarının özelliklerine, seçilen tanı kriterlerine ve incelenen yaş/cinsiyet gruplarına göre farklılıklar göstermekle birlikte küresel sağlık ekonomisi üzerinde devasa bir yük oluşturmaktadır.

Amerika Birleşik Devletleri'nde yapılan geniş ölçekli epidemiyolojik analizlere göre, ÜSE nedeniyle yılda yaklaşık 7 milyon poliklinik başvurusu ve 1 milyon acil servis başvurusu gerçekleşmektedir. Bu başvuruların yaklaşık 100.000'i ağır klinik tablo veya komplikasyonlar nedeniyle hastaneye yatışla sonuçlanmaktadır. Poliklinik ve acil başvurularında kadınların başvuru sıklığı (%1.2), erkeklerin başvuru sıklığına (%0.6) kıyasla tam iki kat daha fazladır.

Türkiye verilerine bakıldığında Sağlık Bakanlığı'nın ICD-10 tanı kodları istatistiklerine göre genitoüriner sistem hastalıklarının tüm hastalıklar içindeki görülme sıklığı %8.6 düzeyindedir (kadınlarda %8.3, erkeklerde %9.1). Tüm ölüm nedenleri incelendiğinde ise genitoüriner sistem hastalıklarına bağlı ölümlerin oranı %4.5'tir (kadınlarda %4.7, erkeklerde %4.3). Ayrıca ÜSE'ler tüm hastane kaynaklı (nozokomiyal) enfeksiyonların yaklaşık %40'ından tek başına sorumlu olup, bunların ezici çoğunluğu üriner kateterizasyon uygulamalarıyla doğrudan ilişkilidir.""",
    "Üriner sistem enfeksiyonları hastane kaynaklı (nozokomiyal) enfeksiyonların %40'ını oluşturarak hastanelerde en sık görülen enfeksiyon kaynağıdır.",
    "ÜSE poliklinik ve acil servis başvuru sıklığı kadınlarda (%1.2), erkeklere (%0.6) kıyasla tam iki kat daha yüksektir.",
    {
        "id": "prac-use-008",
        "stem": "Üriner sistem enfeksiyonlarının epidemiyolojik özellikleri ve hastane morbiditesi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            {"key": "A", "text": "ÜSE'ler nozokomiyal enfeksiyonların yaklaşık %40'ından sorumludur.", "isCorrect": False},
            {"key": "B", "text": "Nozokomiyal ÜSE olgularının büyük çoğunluğu üriner kateter uygulamaları ile ilişkilidir.", "isCorrect": False},
            {"key": "C", "text": "Poliklinik başvurularında kadınların başvuru sıklığı erkeklerin yaklaşık iki katıdır.", "isCorrect": False},
            {"key": "D", "text": "Genç erişkin erkeklerde ÜSE insidansı kadınlara kıyasla belirgin şekilde daha yüksektir.", "isCorrect": True},
            {"key": "E", "text": "ÜSE'ye bağlı komplikasyonlar ve ürosepsis önemli mortalite nedenleri arasındadır.", "isCorrect": False}
        ],
        "correctAnswer": "D",
        "explanation": "Genç erişkin dönemde (15-50 yaş) ÜSE kadınlarda erkeklere göre katbekat fazladır; erkeklerde bu yaş grubunda bakteriüri prevalansı %0.1'in altındadır ve oldukça nadirdir."
    }
))

# ==============================================================================
# SLAYT 9
# ==============================================================================
slides.append(make_slide(
    9,
    "Semptomatik ÜSE'de Yaşa ve Cinsiyete Göre Epidemiyolojik Risk Faktörleri",
    "24 Yaş Eşiği, Yaşam Boyu %50 Risk ve Genç Erkekteki Nadirlik",
    """Semptomatik üriner sistem enfeksiyonlarının insidansı yaş ve cinsiyete göre dramatik bir dağılım sergiler. Özellikle cinsel olarak aktif genç kadınlar, anatomik ve fizyolojik yatkınlıkları nedeniyle en yüksek risk grubunu teşkil eder. Epidemiyolojik veriler, 24 yaşına gelen her üç kadından birinin en az bir kez hekim tarafından antibiyotik reçete edilen semptomatik bir ÜSE atağı geçirdiğini göstermektedir.

Bir kadının yaşamı boyunca en az bir kez semptomatik ÜSE geçirme kümülatif olasılığı %40 ila %50 arasındadır. Üstelik enfeksiyon geçiren kadınların yaklaşık %20'sinde ilk 6 ay içerisinde yeni bir ÜSE atağı (rekürrens) gelişmektedir. Kadınlarda bu yüksek sıklığın ardında davranışsal ve biyolojik faktörler yatar: Sık cinsel temas ('balayı sistiti'), diyafram ve spermisit kullanımı (vajinal koruyucu laktobasil florasını bozarak E. coli kolonizasyonunu artırır), geçirilmiş ÜSE öyküsü, postmenopozal dönemde östrojen eksikliği ve diyabet risk faktörleridir.

Buna karşılık 15-50 yaş arasındaki genç ve orta yaşlı erkeklerde semptomatik ÜSE son derece nadir bir klinik olaydır; bu grupta asemptomatik bakteriüri prevalansı %0.1'in dahi altındadır. Erkeklerde üretranın uzun olması, kuru periüretral çevre ve prostat sıvısının antibakteriyel özellikleri (çinko içeriği) koruyucu kalkan oluşturur. Bu nedenle 15-50 yaş arası bir erkekte ÜSE saptandığında sünnetsizlik, anal ilişki veya en önemlisi üriner sistemde anatomik/işlevsel bir anomali (üretral darlık, taş, posterior üretral valf kalıntısı) mutlaka araştırılmalıdır.""",
    "Kadınların %40-50'si yaşam boyu en az bir kez ÜSE geçirir ve geçirenlerin %20'sinde ilk 6 ayda nüks gelişir; 15-50 yaş erkeklerde ise ÜSE prevalansı <%0.1 olup daima altta yatan anomali araştırılmalıdır.",
    "Kadınlarda vajinal koruyucu laktobasil florasını yok ederek üropatojen E. coli kolonizasyonunu en fazla artıran kontraseptif yöntem spermisit ve diyafram kullanımıdır.",
    {
        "id": "prac-use-009",
        "stem": "28 yaşında sağlıklı bir erkek hasta idrarda yanma ve sık idrara çıkma şikayetleriyle başvuruyor. Yapılan idrar kültüründe 10^4 CFU/ml E. coli üremesi saptanıyor. Bu hastanın epidemiyolojik değerlendirmesinde hekimin öncelikle göz önünde bulundurması gereken temel prensip aşağıdakilerden hangisidir?",
        "options": [
            {"key": "A", "text": "Bu yaş grubundaki erkeklerde ÜSE çok sık görüldüğü için rutin 3 günlük tedavi verilip ileri tetkik yapılmamalıdır.", "isCorrect": False},
            {"key": "B", "text": "Genç erkeklerde ÜSE son derece nadir (<%0.1) olduğundan, altta yatan ürolojik anatomik/fonksiyonel bir anomali mutlaka araştırılmalıdır.", "isCorrect": True},
            {"key": "C", "text": "Erkek hastalarda saptanan E. coli üremesi daima asemptomatik kabul edilmeli ve tedavi edilmemelidir.", "isCorrect": False},
            {"key": "D", "text": "Bu yaş grubunda en sık etken Staphylococcus saprophyticus olduğu için kültür sonucu kontaminasyon kabul edilmelidir.", "isCorrect": False},
            {"key": "E", "text": "Erkeklerde idrar yolu enfeksiyonu gelişimi prostat kanserinin kesin öncül lezyonudur.", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "15-50 yaş arası erkeklerde ÜSE prevalansı <%0.1 olup son derece nadirdir. Bu grupta gelişen bir enfeksiyon aksi ispatlanana kadar komplike kabul edilir ve altta yatan anatomik veya fonksiyonel üriner patoloji araştırılmalıdır."
    }
))

# ==============================================================================
# SLAYT 10
# ==============================================================================
slides.append(make_slide(
    10,
    "ÜSE Etyolojisinde Mikrobiyal Spektrum ve Patojen Hiyerarşisi",
    "Akut Komplike Olmayan Sistitin Liderleri ve Dirençli Nozokomiyal İzolatlar",
    """Üriner sistem enfeksiyonlarına neden olan mikrobiyal ajanların dağılımı, enfeksiyonun toplum kaynaklı mı yoksa hastane kaynaklı mı olduğuna, hastanın altta yatan hastalıklarına ve üriner enstrümantasyon varlığına göre belirgin farklılık gösterir. Ancak toplum kökenli akut komplike olmayan enfeksiyonlarda etyolojik spektrum şaşırtıcı derecede homojendir ve bağırsak kaynaklı enterik bakterilerin hakimiyeti altındadır.

Akut komplike olmayan sistit ve piyelonefrit olgularında en sık izole edilen patojen açık ara **Escherichia coli**'dir (%75-95). E. coli'yi genç ve cinsel olarak aktif kadınlarda ikinci sırada izole edilen koagülaz-negatif bir stafilokok olan **Staphylococcus saprophyticus** takip eder (%5-10). Bu iki patojen tek başına ayaktan başvuran komplike olmayan genç kadın hastaların neredeyse %90'ından fazlasından sorumludur. Diğer enterik gram-negatif basillerden Proteus mirabilis ve Klebsiella pneumoniae daha nadir izole edilir; gram-pozitiflerden Enterococcus faecalis ise toplum kaynaklı olgularda nadirdir.

Buna karşılık hastane ortamında (nozokomiyal), üriner kateteri olan, ürolojik cerrahi geçiren veya geniş spektrumlu antibiyotik kullanmış hastalarda mikrobiyal dağılım dramatik biçimde çeşitlenir ve dirençli suşlara kayar. Bu olgularda E. coli oranı %40-50'lere gerilerken; Pseudomonas aeruginosa, Klebsiella pneumoniae, Proteus mirabilis, Enterobacter türleri, Enterococcus faecalis (ve VRE) ile Candida albicans gibi fungal patojenler ön plana çıkar.""",
    "Akut komplike olmayan toplum kaynaklı sistitin açık ara en sık etkeni E. coli (%75-95), genç cinsel aktif kadınlarda ikinci en sık etken ise Staphylococcus saprophyticus'tur (%5-10).",
    "Genç cinsel aktif bir kadında dizüri ve piyüri tablosunda idrarda Gram-pozitif, katalaz-pozitif, koagülaz-negatif ve novobiyosine dirençli kok üremesi saptanırsa etken Staphylococcus saprophyticus'tur.",
    {
        "id": "prac-use-010",
        "stem": "21 yaşında üniversite öğrencisi kadın hasta, son 2 gündür devam eden ani başlangıçlı dizüri, sık idrara çıkma ve suprapubik rahatsızlık şikayetleriyle başvuruyor. Özgeçmişinde ek hastalık bulunmayan hastanın idrar kültüründe Gram-pozitif, koagülaz-negatif bir kok üremesi saptanıyor. Bu klinik tabloda E. coli'den sonra ikinci en olası etken olan bu mikroorganizma hangisidir?",
        "options": [
            {"key": "A", "text": "Staphylococcus aureus", "isCorrect": False},
            {"key": "B", "text": "Streptococcus agalactiae", "isCorrect": False},
            {"key": "C", "text": "Staphylococcus saprophyticus", "isCorrect": True},
            {"key": "D", "text": "Enterococcus faecalis", "isCorrect": False},
            {"key": "E", "text": "Staphylococcus epidermidis", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Genç ve cinsel aktif kadınlarda komplike olmayan akut sistitin E. coli'den sonra ikinci en sık etkeni (%5-10) novobiyosine dirençli, koagülaz-negatif Staphylococcus saprophyticus'tur."
    }
))

# ==============================================================================
# SLAYT 11
# ==============================================================================
slides.append(make_slide(
    11,
    "Özel Popülasyonlarda ÜSE: Pediyatrik ve Geriyatrik Dinamikler",
    "Çocuklarda Bimodal İnsidans ve Yaşlılarda Atipik Asemptomatik Bakteriüri",
    """Çocukluk çağında üriner sistem enfeksiyonları, solunum yolu enfeksiyonlarından sonra en sık görülen bakteriyel enfeksiyonlardan biridir. Pediyatrik yaş grubunda ÜSE insidansı yaşamın ilk bir yılında ve ergenlik döneminde iki belirgin zirve yaparak 'bimodal' bir eğri çizer. Yaşamın ilk 3 ayında erkek bebeklerde ÜSE insidansı kız bebeklere göre belirgin şekilde daha yüksektir. Bunun temel nedeni erkek bebeklerde prepisyum altında yüksek bakteri kolonizasyonu ve konjenital ürolojik anomalilerin varlığıdır. Ancak ilk aylardan sonra ve prepubertal dönem boyunca kız çocuklarında (%3), erkek çocuklara (%1) kıyasla 3 kat daha fazla ÜSE görülür.

Geriyatrik popülasyonda ise ÜSE, solunum yolu enfeksiyonlarının ardından ikinci en sık görülen enfeksiyon olup tüm geriyatrik enfeksiyonların yaklaşık %25'ini oluşturur. Yaşlanmayla birlikte pelvik taban zayıflığı, mesane prolapsusu (sistosel), postmenopozal atrofi, erkekte prostat hiperplazisine bağlı mesane çıkım obstrüksiyonu ve nörolojik hastalıklar zemin hazırlar. Yaşlılarda asemptomatik bakteriüri (ASB) sıklığı muazzam düzeylere ulaşır; 65 yaş üzeri toplumda yaşayan kadınların %20'sinde, erkeklerin %10'unda ASB vardır. Huzurevlerinde kurumsal bakım alan yaşlılarda bu oran kadınlarda %17-55'e, erkeklerde %15-31'e fırlar.

Geriyatrik hastalarda enfeksiyonun klinik tablosu gençlerdeki gibi klasik dizüri ve pollaküri şeklinde ortaya çıkmayabilir. Yaşlı hastalar kliniğe sıklıkla atipik semptomlarla; ani bilinç bulanıklığı, deliryum, düşmeler, iştahsızlık veya idrar inkontinansının aniden kötüleşmesiyle başvururlar. Ayrıca yaşlı erkeklerde izole edilen Proteus türleri çoğunlukla enfeksiyon taşları (strüvit) ve kalıcı renal parankim hasarı ile yakından ilişkilidir.""",
    "Pediyatrik grupta ÜSE yaşamın ilk 3 ayında erkek çocuklarda daha sık iken, sonraki çocukluk yaşlarında kız çocuklarında sıklık 3 kat fazladır.",
    "Huzurevinde kalan yaşlılarda asemptomatik bakteriüri prevalansı kadınlarda %50'lere varabilir; bu hastalarda klasik semptomlar yerine ani deliryum ve konfüzyon görülebilir.",
    {
        "id": "prac-use-011",
        "stem": "Çocukluk ve yaşlılık dönemindeki üriner sistem enfeksiyonu epidemiyolojisi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            {"key": "A", "text": "Yaşamın ilk 3 ayında erkek çocuklarda ÜSE görülme sıklığı kız çocuklarından fazladır.", "isCorrect": False},
            {"key": "B", "text": "Prepubertal dönemde kız çocuklarında ÜSE insidansı erkek çocukların yaklaşık üç katıdır.", "isCorrect": False},
            {"key": "C", "text": "Huzurevlerinde kalan yaşlı bireylerde asemptomatik bakteriüri oranı %30-50 düzeylerine ulaşabilir.", "isCorrect": False},
            {"key": "D", "text": "Yaşlılarda asemptomatik bakteriüri saptanan her hastaya böbrek fonksiyonlarını korumak için profilaktik antibiyotik başlanmalıdır.", "isCorrect": True},
            {"key": "E", "text": "Yaşlı erkeklerde Proteus türlerinin etken olduğu enfeksiyonlar sıklıkla böbrek taşları ile ilişkilidir.", "isCorrect": False}
        ],
        "correctAnswer": "D",
        "explanation": "Yaşlılarda ve kurumsal bakım alanlarda ASB prevalansı çok yüksek olmasına karşın semptom veya mukozal kanamalı cerrahi endikasyonu yoksa antibiyotik verilmesi önerilmez; gereksiz tedavi dirençli patojenleri selekte eder."
    }
))

# ==============================================================================
# SLAYT 12
# ==============================================================================
slides.append(make_slide(
    12,
    "Hamile Kadınlarda Üriner Sistem Enfeksiyonları",
    "Maternal/Fetal Tehlikeler, 2. Trimester Piyelonefriti ve Rutin Tarama",
    """Gebelik, kadının üriner sistem anatomisinde ve fizyolojisinde enfeksiyona yatkınlık yaratan derin değişikliklere yol açar. Progesteron hormonunun etkisiyle üreter düz kaslarında gevşeme, tonus kaybı ve peristaltizm azalması meydana gelir; buna büyüyen uterusun üreterlere (özellikle sağ üretere) mekanik basısı eklenince 'fizyolojik hidroüreteronefroz' ve idrar stazı gelişir. Ayrıca idrarda glukoz ve aminoasit atılımının artması ile idrar pH'sının yükselmesi bakteriyel çoğalma için mükemmel bir ortam hazırlar.

Hamile kadınların yaklaşık %4 ila %10'unda asemptomatik bakteriüri (ASB), %1 ila %4'ünde akut sistit gelişir. Eğer gebelikteki ASB erken dönemde tespit edilip tedavi edilmezse, bu kadınların %20 ila %40'ında özellikle ikinci ve üçüncü trimesterde ağır 'Akut Piyelonefrit' gelişir. Akut piyelonefrit tüm gebelerin %1-2'sinde görülür ve maternal sepsis, solunum sıkıntısı sendromu (ARDS), erken membran rüptürü, preterm doğum ve düşük doğum ağırlığı gibi ölümcül obstetrik komplikasyonlara neden olur.

Ders notunda vurgulandığı üzere, çocukluğunda ÜSE öyküsü olan hamile kadınlarda ASB riski %27 oranında artarken, renal skarı bulunan hamilelerde bu risk %47'ye fırlar. Gebelikte ÜSE riskini artıran diğer faktörler düşük sosyoekonomik düzey, orak hücre anemisi veya taşıyıcılığı, multiparite ve yetersiz prenatal bakımdır. Bu nedenle obstetrik kılavuzlar, ilk prenatal vizitte (tercihen 12-16. gebelik haftasında) her hamile kadından rutin idrar kültürü taranmasını ve ASB saptandığında uygun antibiyotiklerle eradike edilmesini şart koşar.""",
    "Hamilelikte tedavi edilmeyen asemptomatik bakteriürinin %20-40 oranında akut piyelonefrite ve preterm doğuma yol açması nedeniyle ilk trimesterde rutin kültür taraması zorunludur.",
    "Gebelikte akut piyelonefrit en sık ikinci trimesterde görülür; hidronörotik dilatasyon progesteronun düz kas gevşetici etkisi ve uterusun sağ üretere mekanik basısı nedeniyle en sık sağ böbrekte belirgindir.",
    {
        "id": "prac-use-012",
        "stem": "14 haftalık gebe bir kadının rutin ilk trimester kontrolünde alınan idrar kültüründe 10^5 CFU/ml E. coli üremesi saptanıyor. Hastanın hiçbir klinik şikayeti bulunmamaktadır. Bu klinik durum ve yönetimi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
        "options": [
            {"key": "A", "text": "Hastada dizüri ve ateş olmadığı için antibiyotik tedavisi verilmemeli, doğum sonrasına ertelenmelidir.", "isCorrect": False},
            {"key": "B", "text": "Gebelikte ASB tedavi edilmezse olguların %20-40'ında 2. ve 3. trimesterde akut piyelonefrit ve preterm doğum riski oluşur; derhal tedavi edilmelidir.", "isCorrect": True},
            {"key": "C", "text": "Gebelikte hidronefroz oluşumu patolojik kabul edilmeli ve derhal cerrahi nefrostomi açılmalıdır.", "isCorrect": False},
            {"key": "D", "text": "Bu hastada en olası etken Chlamydia trachomatis olup standart antibiyotiklere yanıtsızdır.", "isCorrect": False},
            {"key": "E", "text": "Asemptomatik gebelerde bakteriüri saptanması bebeğin tahliyesi (terapötik abortus) için mutlak endikasyondur.", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "Gebelerde ASB asemptomatik kalsa dahi hormonal staz nedeniyle %20-40 oranında akut piyelonefrit, erken doğum ve düşük doğum ağırlığına yol açar. Bu nedenle gebelerde ASB mutlak tedavi endikasyonudur."
    }
))

# ==============================================================================
# SLAYT 13
# ==============================================================================
slides.append(make_slide(
    13,
    "Diyabet ve HIV/İmmünsüpresyon Zemininde Gelişen Ağır Üriner Enfeksiyonlar",
    "Glukozüri, Nörojenik Atoni, Amfizematöz Komplikasyonlar ve Klebsiella Artışı",
    """Diabetes mellitus (DM), üriner sistem enfeksiyonlarının insidansını, şiddetini ve komplikasyon oranını artıran en kritik sistemik metabolik hastalıktır. Diyabetli hastalar, diyabeti olmayanlara kıyasla 2 ila 4 kat daha yüksek bakteriüri riskine sahiptir. Özellikle diyabetik kadınlarda asemptomatik bakteriüri prevalansı %26 düzeyinde iken, sağlıklı kadınlarda bu oran %6 civarındadır. Bu artışın temel patofizyolojik nedenleri glukozürinin bakteriyel proliferasyonu kolaylaştırması, otonom nöropatiye bağlı mesane boşalma disfonksiyonu (nörojenik mesane ve yüksek rezidüel idrar) ve lökosit fagositoz fonksiyonlarındaki defektlerdir.

Diyabetik bireylerde uzun hastalık süresi, mikroalbüminüri/proteinüri ve periferik nöropati varlığı ÜSE riskini katlar. Diyabet, Enterobacteriaceae kaynaklı akut piyelonefrit riskini belirgin şekilde artırır. Çok dikkat çekici bir etyolojik fark olarak; diyabeti olan hastalarda Klebsiella pneumoniae enfeksiyonları diyabeti olmayanlara kıyasla iki kat daha sık izlenir (%25'e karşılık %12). En tehlikelisi, diyabet zemininde doku iskemisi ve glukoz fermantasyonu nedeniyle gaz üreten bakterilerin yol açtığı yaşamı tehdit eden 'Amfizematöz Sistit' ve 'Amfizematöz Piyelonefrit' gibi nekrotizan komplikasyonlar gelişebilir.

HIV/AIDS hastalarında da immünsüpresyon derecesine (özellikle CD4 T-lenfosit sayısının düşmesine) paralel olarak ÜSE insidansı genel popülasyondan belirgindir. HIV ile ilişkili trombotik mikroanjiyopati ve immün kompleks aracılı nefropatiler böbrek parankim direncini kırar. HIV/AIDS hastalarında üropatojen profili de değişir; bu hastalarda enterik basillerin yanı sıra Enterococcus türleri alışılmadık biçimde baskın üropatojenler olarak izole edilir ve parankimal apselere neden olabilir.""",
    "Diyabetik hastalarda Klebsiella enfeksiyonu sıklığı normal popülasyonun iki katına (%25'e %12) çıkar; glukoz fermantasyonuna bağlı gaz oluşumuyla amfizematöz sistit ve piyelonefrit riski yüksektir.",
    "HIV/AIDS hastalarında üriner sistem enfeksiyonlarında klasik etkenlerin yanı sıra en sık baskın üropatojen olarak izole edilen bakteri cinsi Enterococcus türleridir.",
    {
        "id": "prac-use-013",
        "stem": "58 yaşında kontrolsüz Tip 2 diyabet ve diyabetik nöropati öyküsü olan kadın hasta, yan ağrısı ve yüksek ateşle acile başvuruyor. Çekilen direkt üriner sistem grafisinde ve BT'de renal parankimde gaz kabarcıkları saptanıyor. Bu hastanın etyolojik ve klinik özellikleri ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            {"key": "A", "text": "Diyabetik hastalarda Klebsiella kaynaklı piyelonefrit sıklığı diyabetik olmayanlara göre yaklaşık iki kat daha fazladır.", "isCorrect": False},
            {"key": "B", "text": "Görüntülemede gaz saptanması gaz oluşturan basillere bağlı gelişen amfizematöz piyelonefrit tablosudur.", "isCorrect": False},
            {"key": "C", "text": "Diyabetik kadınlarda ASB sıklığı genel popülasyona göre belirgin olarak artmıştır (%26'ya %6).", "isCorrect": False},
            {"key": "D", "text": "Diyabetik hastalarda otonom nöropatiye bağlı rezidü idrar kalması enfeksiyon patogenezinde rol oynamaz.", "isCorrect": True},
            {"key": "E", "text": "Glukozüri ve bozulmuş lökosit kemotaksisi bakteriyel üremeyi hızlandıran temel faktörlerdendir.", "isCorrect": False}
        ],
        "correctAnswer": "D",
        "explanation": "Otonom nöropati mesanede tam boşalamamaya ve yüksek post-voiding rezidüel idrara yol açarak enfeksiyon patogenezinde kritik bir rol oynar. Bu nedenle D seçeneğindeki ifade kesinlikle yanlıştır."
    }
))

# ==============================================================================
# SLAYT 14
# ==============================================================================
slides.append(make_slide(
    14,
    "Katater İlişkili Üriner Sistem Enfeksiyonları (Kİ-ÜSE / CAUTI)",
    "Biyofilm Dinamikleri, Günlük %5 Risk Artışı ve Polimikrobiyal Kolonizasyon",
    """Katater ilişkili üriner sistem enfeksiyonları (Kİ-ÜSE), tüm dünyada sağlık bakımı ilişkili (nozokomiyal) enfeksiyonların yaklaşık %40'ını tek başına oluşturan en yaygın hastane enfeksiyonudur. Hastanede gelişen nozokomiyal ÜSE olgularının %80'inden fazlasında altta yatan neden bir üriner katater varlığıdır. Genel hastane servislerinde yatan hastaların %15-25'ine, yoğun bakım ünitelerinde yatan hastaların ise neredeyse tamamına üriner katater uygulanır. YBÜ'lerde ÜSE, ventilatör ilişkili pnömoni ve santral katater ilişkili kan dolaşımı enfeksiyonlarının ardından 3. en sık enfeksiyondur.

Katater ilişkili enfeksiyon patogenezindeki en kritik risk faktörü 'kataterin kalış süresidir'. Kataterin takılı kaldığı her geçen gün bakteriüri gelişme riski kümülatif olarak %3 ila %10 arasında artar (30 günde neredeyse %100 bakteriüri). Katater lümeninin içinden (intraluminal - drenaj torbasındaki bakterilerin retrograd göçü) veya katater ile üretra mukozası arasındaki sıvı filminden (ekstraluminal - periüretral deriden tırmanış) mikroorganizmalar mesaneye ulaşır. Katater yüzeyinde bakteriler ekstraselüler polisakkarit matriks sentezleyerek 'biyofilm' tabakası oluşturur. Biyofilm içindeki bakteriler konak bağışıklığından ve antibiyotiklerin penetrasyonundan korunurlar.

Kısa süreli kataterizasyonda (1-30 gün) enfeksiyonlar çoğunlukla tek bir patojenle (monomikrobiyal, polimikrobiyal olasılığı sadece %15) oluşurken; 30 günden uzun süren kalıcı kataterizasyonlarda olguların %95'i polimikrobiyaldir. Kİ-ÜSE mikrobiyal spektrumunda klasik E. coli'nin yanı sıra Pseudomonas aeruginosa, Klebsiella pneumoniae, üreaz üreten ve katateri tıkayan Proteus mirabilis, Staphylococcus epidermidis, glikopeptid dirençli Enterococcus spp. ve Candida spp. (fungüri) sıklıkla izole edilir.""",
    "Katater takılı kalan her gün için bakteriüri riski %3-10 artar; 30 günü aşan kataterizasyonlarda enfeksiyonların %95'i polimikrobiyaldir ve biyofilm ile korunur.",
    "Nozokomiyal enfeksiyonların %40'ı üriner sistem kaynaklıdır ve bu enfeksiyonların %80'inde indwelling (kalıcı) üriner katater öyküsü mevcuttur.",
    {
        "id": "prac-use-014",
        "stem": "Yoğun bakım ünitesinde 35 gündür kalıcı foley kateter ile izlenen bir hastada gelişen katater ilişkili üriner sistem enfeksiyonu (Kİ-ÜSE) patogenezi ve mikrobiyolojisi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
        "options": [
            {"key": "A", "text": "30 günü aşan kataterizasyonlarda enfeksiyonlar %95 oranında tek bir bakteri suşuna (monomikrobiyal) bağlıdır.", "isCorrect": False},
            {"key": "B", "text": "Katater varlığında bakteriüri riski kataterin takılı kaldığı her gün sabit kalır ve süreyle artış göstermez.", "isCorrect": False},
            {"key": "C", "text": "Uzun süreli kataterizasyonda olguların %95'i polimikrobiyaldir; bakteriler katater yüzeyinde antibiyotiklere dirençli biyofilm oluşturur.", "isCorrect": True},
            {"key": "D", "text": "Katater ilişkili enfeksiyonlarda en sık izole edilen mikroorganizma tartışmasız Streptococcus pneumoniae'dir.", "isCorrect": False},
            {"key": "E", "text": "Katater ilişkili asemptomatik bakteriürisi olan her hastaya derhal geniş spektrumlu karbapenem tedavisi başlanmalıdır.", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "30 günden uzun kataterizasyonlarda enfeksiyonların %95'i polimikrobiyaldir. Bakterilerin katater yüzeyinde oluşturduğu biyofilm matriksi, antibiyotiklerin penetrasyonunu ve hücresel bağışıklığı engeller."
    }
))

# ==============================================================================
# SLAYT 15
# ==============================================================================
slides.append(make_slide(
    15,
    "Ürosepsis: Patofizyoloji, Risk Grupları ve Klinik Yönetim",
    "Tıkanma Kaynaklı Bakteriyemi, Endotoksin Fırtınası ve %40'a Varan Mortalite",
    """Ürosepsis, üriner sistemdeki bir enfeksiyon odağından (en sık piyelonefrit veya obstrükte enfekte böbrek) kaynaklanan mikroorganizmaların ve toksinlerinin sistemik dolaşıma karışması sonucu kontrolsüz bir konak inflamatuar yanıtının (SIRS / Sepsis) tetiklenmesidir. Genel yoğun bakım popülasyonunda ciddi sepsise yol açan nedenler arasında pulmoner enfeksiyonlar (%50) ve intraabdominal enfeksiyonların (%24) ardından üriner sistem enfeksiyonları yaklaşık %5'lik bir paya sahiptir. Ancak sepsisin erkeklerde kadınlardan daha fazla görüldüğü ve mortalite oranının %20 ila %42 arasında değiştiği bilinmektedir.

Ürosepsisin patofizyolojisinde en tehlikeli tetikleyici mekanizma, obstrüksiyon (örneğin üreteri tıkayan bir taş veya tümör) varlığında toplayıcı sistem içindeki intraluminal basıncın aşırı yükselmesidir. Yüksek hidrostatik basınç, enfekte idrarın ve Gram-negatif bakterilerin yüzeyindeki lipopolisakkaritlerin (LPS / endotoksin) fornikslerden renal venöz ve lenfatik dolaşıma hızla geçmesine (piyelovenöz geri akım) yol açar. Dolaşıma salınan sitokinler (TNF-alfa, IL-1, IL-6) yaygın vazodilatasyona, kapiller kaçışa, dissemine intravasküler koagülasyona (DİK), çoklu organ yetmezliğine ve septik şoka neden olur.

Ürosepsis gelişiminde en yüksek risk altındaki hasta grupları: İleri yaştaki hastalar, kontrolsüz diyabetikler, solid organ nakli yapılmış veya kemoterapi alan immünsüpresifler ve AIDS hastalarıdır. Ürosepsis şüphesi olan bir hastada yönetim hayati bir acildir: Kan ve idrar kültürleri derhal alınmalı, ilk bir saat içinde geniş spektrumlu intravenöz bakterisidal antibiyotik tedavisi başlanmalı ve en önemlisi eğer üriner obstrüksiyon varsa (piyonefroz/taş) acil olarak perkütan nefrostomi veya üreteral DJ stent ile basınç boşaltılmalıdır (dekompresyon yapılmazsa antibiyotikler tıkanmış böbreğe ulaşamaz ve hasta kaybedilir).""",
    "Tıkayıcı bir taş zemininde gelişen ürosepsis tablosunda tek başına antibiyotik tedavisi yetersizdir; acil ürolojik dekompresyon (nefrostomi veya stent) hayat kurtarıcıdır.",
    "Ürosepsiste mortalite %20-42 arasında seyreder; sepsise yol açan Gram-negatif bakterilerin dış membranında bulunan ve septik şoku tetikleyen temel bileşen Lipopolisakkarittir (Endotoksin / Lipid A).",
    {
        "id": "prac-use-015",
        "stem": "67 yaşında diyabetik bir hasta, sağ yan ağrısı, 39.5 °C ateş, titreme, hipotansiyon (80/50 mmHg), taşikardi ve konfüzyon tablosunda acile getiriliyor. Çekilen USG'de sağ üreteri tıkayan 12 mm'lik taş ve toplayıcı sistemde pürülan dilatasyon (piyonefroz) saptanıyor. Bu hastanın acil yönetiminde antibiyotik tedavisinin yanı sıra en kritik ve geciktirilmemesi gereken girişim hangisidir?",
        "options": [
            {"key": "A", "text": "Taşın derhal açık cerrahi ile çıkarılması", "isCorrect": False},
            {"key": "B", "text": "Hastanın sedatize edilerek spontan taş düşürmesinin beklenmesi", "isCorrect": False},
            {"key": "C", "text": "Perkütan nefrostomi veya JJ stent ile toplayıcı sistemin acil dekompresyonu", "isCorrect": True},
            {"key": "D", "text": "Yüksek doz loop diüretiği uygulanarak idrar debisinin artırılması", "isCorrect": False},
            {"key": "E", "text": "Ağrı kontrolü amacıyla intramüsküler analjezik verilip taburcu edilmesi", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Obstrüktif üropati zemininde gelişen piyonefroz ve ürosepsiste hidrostatik basınç düşürülmezse piyelovenöz reflü ile bakteriyemi durdurulamaz. Bu nedenle acil nefrostomi veya stent ile idrar drenajı (dekompresyon) mutlak hayat kurtarıcı adımdır."
    }
))

# ==============================================================================
# SLAYT 16
# ==============================================================================
slides.append(make_slide(
    16,
    "ÜSE Patogenezinde Konak-Patojen Etkileşimi: Fimbriyalar ve Adhezinler",
    "Tip 1 (Mannoz Duyarlı) vs P-Fimbriya (Gal-Gal Reseptörleri) ve Virülans Silahları",
    """Üriner sistem enfeksiyonları, üropatojen bakterilerin virülans donanımı ile konağın anatomik ve immünolojik savunma düzenekleri arasındaki dinamik mücadelenin bir sonucudur. Bakterinin idrar akımının mekanik yıkama (flushing) etkisine direnerek mukozada kalabilmesinin ilk ve en kritik adımı 'bakteriyel adherens' yani ürotelyuma tutunmadır. Bakteriler bu tutunmayı hücre yüzeylerinden dışarı uzanan özelleşmiş protein yapıları olan fimbriyalar (pili) ve afimbriyal adhezinler aracılığıyla gerçekleştirir.

Üropatojenik Escherichia coli (UPEC) suşlarında iki temel fimbriya tipi enfeksiyonun anatomik kaderini belirler:
1. **Tip 1 Fimbriya (Mannoz-duyarlı adhezinler):** Ürotelyum yüzeyindeki üroplakin proteinlerinde bulunan D-mannoz kalıntılarına bağlanır. Tip 1 fimbriyalar özellikle alt üriner sistemde, mesane epitel hücrelerine tutunmada ve sistit patogenezinde kritik rol oynar; serbest D-mannoz varlığında bağlanmaları inhibe olur.
2. **P-Fimbriya (P-pili / Pap / Mannoz-dirençli adhezinler):** Renal tübül epiteli ve eritrosit yüzeyinde bulunan alfa-D-galaktopiranozil-(1->4)-beta-D-galaktopiranozid (Gal-Gal) oligosakkarit reseptörlerine spesifik olarak bağlanır. P-fimbriyalar serbest mannoz ile bloke edilemez ve bakterinin mesaneden üretere, üreterden renal parankime tırmanmasında rol oynayan, **akut piyelonefrit patogenezindeki 1 numaralı virülans faktörüdür**.

Bakteriyel adherensin ötesinde konak epitel hücrelerinin reseptivite kapasitesi de önemlidir; vajinal ve mesane epitelinde reseptör yoğunluğu fazla olan bireyler rekürrenslere yatkındır. Ayrıca UPEC suşları hemolizin (eritrosit ve lökositleri lizise uğratarak doku hasarı yapar), sitotoksik nekrotizan faktör tip 1 (CNF-1), aerobaktin ve enterobaktin (ortamdaki demiri bağlayarak bakteriye sağlayan sideroforlar) gibi sekonder virülans faktörleri ile donatılmıştır. Konağın savunmasında obstrüksiyon, vezikoüreteral reflü (VUR), metabolik bozukluklar (DM, gut, nefrokalsinozis, analjezik nefropatisi) ve yaşlanma bu mekanizmaları çökertir.""",
    "E. coli'nin mesane mukozasına tutunmasında Tip 1 fimbriya (mannoz duyarlı) rol oynarken; böbrek parankimine tutunarak akut piyelonefrit yapmasında P-fimbriya (Gal-Gal reseptörleri, mannoz dirençli) rol oynar.",
    "Akut piyelonefrit etkeni UPEC suşlarının böbrek tübül epiteline tutunmasını sağlayan Gal-Gal reseptör spesifik virülans faktörü P-fimbriyadır (Pap adezini).",
    {
        "id": "prac-use-016",
        "stem": "Üropatojenik Escherichia coli'nin (UPEC) patogenezinde rol oynayan virülans faktörleri ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            {"key": "A", "text": "Tip 1 fimbriyalar D-mannoz kalıntılarına bağlanır ve özellikle mesane epitel hücrelerine tutunmada rol oynar.", "isCorrect": False},
            {"key": "B", "text": "P-fimbriyalar eritrosit ve tübül epitelindeki Gal-Gal reseptörlerine bağlanarak akut piyelonefrit patogenezinde kritik görev üstlenir.", "isCorrect": False},
            {"key": "C", "text": "P-fimbriyaların epitele tutunması ortamda serbest D-mannoz bulunması durumunda tamamen inhibe olur.", "isCorrect": True},
            {"key": "D", "text": "Bakteriyel adhezyon, idrar akımının mekanik yıkama gücünü aşmak için gereken ilk ve en zorunlu basamaktır.", "isCorrect": False},
            {"key": "E", "text": "UPEC suşları demir kazanımı için aerobaktin gibi özelleşmiş sideroforlar salgılar.", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "P-fimbriyalar 'mannoz-dirençli' adhezinlerdir; Gal-Gal reseptörlerine bağlanırlar ve ortamdaki D-mannoz tarafından inhibe edilemezler. Mannoz ile inhibe olan Tip 1 fimbriyalardır."
    }
))

# ==============================================================================
# SLAYT 17
# ==============================================================================
slides.append(make_slide(
    17,
    "Enfeksiyonun Giriş Yolları: Asendan, Hematojen ve Lenfojen Mekanizmalar",
    "Asendan Tırmanışın %95 Üstünlüğü, Hematojen Stafilokoklar ve VUR",
    """Mikroorganizmaların üriner sisteme ve böbrek parankimine ulaşabilmesi üç ana patofizyolojik yolla gerçekleşir: 1) Asendan (retrograd) yol, 2) Hematojen (kan yoluyla) yol, ve 3) Lenfojen yol. Normal fizyolojide üriner sistemde bakterilerin kolonize olabildiği tek anatomik bölge eksternal üretranın distal kısmıdır; üretrovezikal bileşkenin proksimalinde yer alan mesane, üreterler ve böbrekler tamamen sterildir.

**Asendan Yol:** Üriner sistem enfeksiyonlarının %95'inden fazlasının geliştiği açık ara en yaygın mekanizmadır. Bağırsak florasından kaynaklanan enterik bakteriler perine ve periüretral bölgeyi kolonize eder. Kadınlarda üretranın kısa olması (yaklaşık 4 cm) ve anüse yakınlığı bakterilerin mesaneye mekanik olarak (örneğin cinsel ilişki veya kateterizasyon ile) itilmesini kolaylaştırır. Bakteriler mesanede çoğalarak sistit tablosu oluşturur; normalde üreterovezikal bileşkedeki flep-valv mekanizması idrarın geri kaçışını engeller. Ancak Vezikoüreteral Reflü (VUR) veya obstrüksiyon varlığında bakteriler idrar stazı ve antiperistaltik dalgalarla üreter boyunca böbrek pelvisine ve toplayıcı kanallara tırmanarak piyelonefrite neden olur. Postmenopozal dönemdeki östrojen eksikliği de laktobasilleri azaltıp asendan kolonizasyonu hızlandırır.

**Hematojen Yol:** Çok daha nadir görülen (<%5) bir yoldur. Primer bir bakteriyemi odağından kan yoluyla böbrek parankimine ulaşan bakterilerin tutulumudur. Hematojen yolla piyelonefrit veya renal kortikal apse gelişiminde Gram-negatif enterik basillerin rolü son derece düşüktür. Bu yol tipik olarak Staphylococcus aureus bakteriyemisi, infektif endokardit olguları veya dissemine mantar (Candida) enfeksiyonlarında görülür; kortekste multipl mikroabseler oluşturur. **Lenfojen Yol** ise bağırsak veya servikal lenfatiklerden retroperitoneal lenf damarları yoluyla böbreğe yayılımı tarif etse de patogenezdeki klinik rolü kanıtlanmamış ve son derece tartışmalıdır.""",
    "Üriner sistem enfeksiyonları %95'in üzerinde asendan (tırmanıcı) yolla gelişir; hematojen yol ise nadirdir ve tipik olarak Staphylococcus aureus endokarditi/bakteriyemisinde görülür.",
    "Hematojen yolla böbrek parankimine ulaşarak renal kortikal apse oluşturan en tipik mikroorganizma Gram-negatif basiller değil, Staphylococcus aureus'tur.",
    {
        "id": "prac-use-017",
        "stem": "Üriner sistem enfeksiyonlarının patogenezinde mikroorganizmaların yayılım yolları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            {"key": "A", "text": "ÜSE'lerin ezici çoğunluğu (%95+) periüretral alandan mesaneye ve böbreğe uzanan asendan yolla gelişir.", "isCorrect": False},
            {"key": "B", "text": "Vezikoüreteral reflü (VUR), asendan yolla bakterilerin mesaneden renal toplayıcı sisteme ulaşmasındaki en önemli defekttir.", "isCorrect": False},
            {"key": "C", "text": "Hematojen yolla piyelonefrit ve parankim apsesi oluşumunda E. coli ve diğer Gram-negatif basiller primer rol oynar.", "isCorrect": True},
            {"key": "D", "text": "Staphylococcus aureus bakteriyemisi veya infektif endokardit varlığında böbrek parankimi hematojen yolla enfekte olabilir.", "isCorrect": False},
            {"key": "E", "text": "Kadınlarda üretranın anatomik olarak kısa olması asendan enfeksiyonlara yatkınlığın temel nedenlerindendir.", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Hematojen yolla piyelonefrit oluşumunda Gram-negatif basillerin rolü çok düşüktür; hematojen yayılım tipik olarak S. aureus bakteriyemisi veya sistemik mantar enfeksiyonlarında izlenir. Enterik Gram negatif basiller asendan yolla bulaşır."
    }
))

# ==============================================================================
# SLAYT 18
# ==============================================================================
slides.append(make_slide(
    18,
    "Ürolojik Semptomatoloji: Hematüriye Klinik ve Laboratuvar Yaklaşımı",
    "Makroskopik vs Mikroskopik, Malignite Arayışı ve İzomorfik/Dismorfik Eritrositler",
    """Hematüri, idrarda anormal miktarda eritrosit bulunması durumudur ve ürolojik semptomatolojinin en alarm verici bulgularından biridir. İdrarın çıplak gözle kırmızı, çay rengi veya kola renginde görülmesine 'makroskopik hematüri' adı verilir. Çıplak gözle normal renkte olan idrarın santrifüj edilmiş sedimentinin mikroskobik incelenmesinde, büyük büyütme alanında (HPF) 3 veya daha fazla eritrosit saptanması ise 'mikroskopik hematüri' olarak tanımlanır.

Hematüri ile başvuran yetişkin bir hastada aksi kanıtlanana kadar ürolojik bir malignite (mesane tümörü, böbrek tümörü) varlığı kabul edilmeli ve ileri ürolojik tetkik yapılmalıdır. Üriner sistem enfeksiyonları da (özellikle hemorajik sistit) sık hematüri nedenidir. Ancak hayati bir klinik kural olarak: Hematürinin makroskopik ya da mikroskopik oluşu altta yatan patolojinin ciddiyetini doğrudan yansıtmaz. Basit, selim bir akut sistit atağı hastada korkutucu bir makroskopik hematüriye yol açabilirken; yaşamı tehdit eden invaziv bir mesane karsinoması aylarca yalnızca tesadüfen saptanan asemptomatik mikroskopik hematüri ile seyredebilir. Bununla birlikte makroskopik hematürili hastalarda araştırma sonucunda ürolojik patoloji bulunma oranı mikroskopik olgulara göre çok daha yüksektir.

Hematürinin ayırıcı tanısında iki kritik parametre yol gösterir: 1) Hematürinin miksiyon içindeki zamanlaması: İşemenin başında görülmesi üretra lezyonunu; miksiyonun tamamı boyunca görülmesi mesane veya üst üriner sistem patolojisini; işemenin sonunda (terminal hematüri) görülmesi ise mesane boynu, prostatik üretra veya trigon patolojilerini gösterir. 2) Eritrosit morfolojisi: Faz kontrast mikroskopisinde idrarda izlenen 'izomorfik (normal şekilli) eritrositler' taş, enfeksiyon veya tümör gibi ürolojik patolojileri işaret ederken; glomerüler filtrasyon bariyerindeki mekanik hasardan geçerek şekil bozukluğuna uğramış 'dismorfik eritrositler' (akantositler) ve eritrosit silindirleri primer glomerüler nefritik hastalıkları gösterir.""",
    "Erişkin bir hastada hematüri aksi ispat edilene kadar ürolojik malignite bulgusu kabul edilir; basit sistit makroskopik hematüri yapabilirken ölümcül mesane kanseri mikroskopik hematüriyle seyredebilir.",
    "İdrar mikroskopisinde izomorfik eritrositler ürolojik cerrahi patolojileri (taş, tümör, sistit); dismorfik eritrositler ve eritrosit silindirleri ise nefrolojik glomerüler hastalıkları gösterir.",
    {
        "id": "prac-use-018",
        "stem": "54 yaşında erkek hasta idrarda kan görme şikayetiyle başvuruyor. Yapılan tetkiklerde hematürinin miksiyonun tamamı boyunca devam ettiği ve idrar sedimentinde ağırlıklı olarak izomorfik eritrositlerin bulunduğu saptanıyor. Bu hastanın klinik yaklaşımı ile ilgili aşağıdaki ilkelerden hangisi doğrudur?",
        "options": [
            {"key": "A", "text": "İzomorfik eritrositler primer glomerülonefrit lehine olup hastaya derhal renal kortikal biyopsi yapılmalıdır.", "isCorrect": False},
            {"key": "B", "text": "Hematürinin miktarı patolojinin ciddiyetiyle doğru orantılıdır; ağrısız olduğu için ileri araştırma gerekmez.", "isCorrect": False},
            {"key": "C", "text": "Yetişkin bir hastada aksi kanıtlanana kadar ürolojik malignite dışlanmalı, sistoskopi ve üst üriner sistem görüntülemesi planlanmalıdır.", "isCorrect": True},
            {"key": "D", "text": "Miksiyonun tamamında görülen hematüri yalnızca distal üretral inflamasyona özgüdür.", "isCorrect": False},
            {"key": "E", "text": "İdrarda eritrosit görülmesi durumunda antibiyotik verilerek 6 ay sonra kontrole çağrılması yeterlidir.", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Erişkinde hematüri aksi ispatlanana kadar ürolojik malignite (mesane/böbrek tümörü) kabul edilir. Total hematüri ve izomorfik eritrositler glomerül dışı ürolojik traktusu gösterdiğinden sistoskopi ve görüntüleme şarttır."
    }
))

# ==============================================================================
# SLAYT 19
# ==============================================================================
slides.append(make_slide(
    19,
    "Üriner Ağrı Tipleri: Renal Kolik, İnflamatuar Ağrı ve İntraperitoneal Ayrım",
    "Kapsüler Gerilme, Toplayıcı Sistem Spazmı ve Fizik Muayenede Hasta Hareketi",
    """Üriner sistemi ilgilendiren ağrılar temel olarak iki fizyopatolojik mekanizmaya sekonder gelişir: 'Obstrüksiyon' veya 'İnflamasyon'. Böbrek parankiminde, epididimde veya testiste gelişen inflamatuar süreçler doku ödemine, organ distansiyonuna ve organı çevreleyen fibröz kapsülde (böbrekte Gerota fasyası ve fibröz kapsül) gerginliğe yol açarak künt, devamlı ve sabit bir ağrı oluşturur. Buna karşılık mesane ve üreter gibi içi boş visseral organlarda inflamasyon genellikle mukozada sınırlı kaldığından şiddetli ağrıdan ziyade rahatsızlık ve yanma hissi olarak algılanır.

Renal toplayıcı sistemde akut bir taş veya pıhtı obstrüksiyonu geliştiğinde ortaya çıkan tablo 'Akut Renal Kolik'tir. Renal kolik, flank (böbrek yatağı) bölgesinde aniden başlayan, üreter trasesi boyunca alt abdomene, kasığa, testise veya labiuma yayılan, dalgalar halinde artıp azalan (kolik tarzda) ve hastaların yaklaşık yarısında bulantı ve kusmanın eşlik ettiği son derece şiddetli bir ağrıdır. Ağrının nedeni renal kapsülün ve üreter düz kaslarının intraluminal basınç artışına bağlı gerilmesidir. Orta üreter taşlarının ağrısı sağ alt kadranda McBurney noktasında hissedilerek akut apandisit ve divertiküliti taklit edebilir; alt uç taşları ise mesane irritasyonu yaparak acil işeme hissi (urgency) ve pollaküri doğurur.

Acil serviste böbrek kaynaklı ağrılar ile akut batına yol açan intraperitoneal organ patolojilerinin ayrımı hayati önem taşır. Bu iki tabloyu ayırt eden kardinal özellikler şunlardır:
1. **Fiziksel Davranış:** İntraperitoneal patolojilerde (örneğin perfore apandisit, peritonit) hasta peritonu irrite etmemek için sırtüstü pozisyonda tamamen hareketsiz yatar. Oysa renal kolikli hasta hiçbir pozisyonda rahatlayamaz, kıvranır ve oda içinde sürekli hareket halindedir.
2. **Ağrı Yayılımı:** İntraperitoneal patolojiler diyafram üzerinden frenik sinir irritasyonu ile omuza veya sırta yayılabilir ve en sık epigastriumda hissedilir. Böbrek patolojileri ise frenik sinir irritasyonu yapmaz, en yaygın kostovertebral açıda hissedilir ve kasığa/genitale yayılır.""",
    "Renal kolikli hasta ağrısını dindirecek pozisyon bulamadığı için sürekli hareket eder ve kıvranır; peritonitli hasta ise periton irritasyonunu önlemek için yatakta tamamen hareketsiz kalır.",
    "Orta üreter kaynaklı ağrılar sağ alt kadranda McBurney noktasında hissedilerek akut apandisit ile karışabilir; distal üreter ağrıları ise kasık, testis/labium ve mesaneye yansır.",
    {
        "id": "prac-use-019",
        "stem": "Acil servise sağ yan ağrısı şikayetiyle başvuran bir hastanın ayırıcı tanısında akut böbrek/üreter patolojisi ile intraperitoneal bir organ perforasyonu (peritonit) arasında kalınmıştır. Aşağıdaki klinik bulgulardan hangisi intraperitoneal bir patolojiden ziyade böbrek/üreter kaynaklı akut renal koliği en güçlü şekilde destekler?",
        "options": [
            {"key": "A", "text": "Hastanın karın ağrısını azaltmak için yatakta tamamen sırtüstü ve hareketsiz yatması", "isCorrect": False},
            {"key": "B", "text": "Ağrının frenik sinir irritasyonu aracılığıyla sağ omuza yayılması", "isCorrect": False},
            {"key": "C", "text": "Ağrının epigastrik bölgede sabit bir şekilde lokalize olması", "isCorrect": False},
            {"key": "D", "text": "Hastanın hiçbir pozisyonda rahat edemeyip kıvranarak oda içinde sürekli hareket halinde olması", "isCorrect": True},
            {"key": "E", "text": "Fizik muayenede yaygın defans ve rebound hassasiyeti saptanması", "isCorrect": False}
        ],
        "correctAnswer": "D",
        "explanation": "Akut renal kolikte viseral gerilme nedeniyle hasta rahat bir pozisyon bulamaz ve sürekli kıvranıp hareket eder. İntraperitoneal inflamasyonda (peritonit) ise hasta periton temasını engellemek için yatakta kıpırdamadan yatar."
    }
))

# ==============================================================================
# SLAYT 20
# ==============================================================================
slides.append(make_slide(
    20,
    "Alt Üriner Sistem Semptomları (AÜSS / LUTS): Sınıflandırma ve Dinamikler",
    "Depolama (İrritatif), İşeme (Tıkayıcı) ve İşeme Sonrası Semptom Yelpazesi",
    """Alt üriner sistem semptomları (AÜSS / LUTS), mesane ve üretranın fonksiyonel veya yapısal bozukluklarına bağlı olarak ortaya çıkan geniş bir semptomlar kümesidir. Uluslararası Kontinans Derneği (ICS) sınıflamasına göre LUTS üç ana kategoride incelenir: 1) Depolama (dolum / irritatif) semptomları, 2) İşeme (boşaltım / obstrüktif) semptomları, ve 3) İşeme sonrası (postmiksiyonel) semptomlar. Bu ayrım hastanın şikayetlerinin mesane inflamasyonundan mı yoksa çıkış obstrüksiyonundan mı kaynaklandığını aydınlatır.

**Depolama (İrritatif) Semptomları:** Mesanenin idrarı depolama fazındaki irritasyon veya fonksiyon kaybından doğar.
- *Pollaküri (Frequency - Sıklık):* Gün içinde anormal sıklıkta idrara çıkma hissidir.
- *Noktüri:* Kişinin gece uyku bölünerek bir veya daha fazla kez idrar yapmak için uyanmasıdır (60 yaş üzeri bireylerde gecede 2'den fazla olması patolojiktir).
- *Urgency (Ani Sıkışma):* Ertelenmesi son derece güç, aniden gelen şiddetli işeme hissidir.
- *Dizüri:* İdrar yaparken hissedilen ağrı ve yanmadır.
- *Stres ve Urge İnkontinans:* Depolama fazındaki istemsiz idrar kaçırmalardır.

**İşeme (Obstrüktif / Tıkayıcı) Semptomları:** Mesane çıkım obstrüksiyonu (özellikle BPH, üretra darlığı) veya detrüsör kasılma zayıflığında görülür. İdrar akış hızında azalma (zayıf akım), işemeyi başlatmada gecikme ve tutukluk (*Hesitancy*), idrar akımının istemsiz durup başlaması (*Kesintili Akım / Intermittency*), işemeyi sürdürmek için karın kaslarını kasma (*Ikınma / Straining*) ve işemenin son fazının damlamalarla uzaması (*Terminal Dribbling*). **İşeme Sonrası Semptomlar** ise işeme bittikten ve tuvaletten ayrıldıktan sonra istemsiz damlama olması (*Postvoid Dribbling*) ve mesanenin tam boşalmadığı hissidir; bunlar sıklıkla erken evre BPH bulgusudur.""",
    "Sıklık (frequency), noktüri, urgency ve dizüri depolama (irritatif) semptomlarıdır; akış hızında azalma, hesitancy, kesintili işeme ve ıkınma ise işeme (tıkayıcı) semptomlarıdır.",
    "İşemeye hazır olunduğu halde idrar akışının başlamasında gecikme olması 'Tutukluk' (Hesitancy); işeme bittikten sonra istemsiz damlama olması ise 'Postvoid Dribbling' olarak adlandırılır.",
    {
        "id": "prac-use-020",
        "stem": "Aşağıdaki alt üriner sistem semptomlarından hangisi mesanenin idrar depolama (irritatif) fazına ait semptomlar arasında yer almaz?",
        "options": [
            {"key": "A", "text": "Sık idrara çıkma (Frequency / Pollaküri)", "isCorrect": False},
            {"key": "B", "text": "Gece idrara kalkma (Noktüri)", "isCorrect": False},
            {"key": "C", "text": "Ani sıkışma hissi (Urgency)", "isCorrect": False},
            {"key": "D", "text": "İdrar yaparken ağrı ve yanma (Dizüri)", "isCorrect": False},
            {"key": "E", "text": "İdrara başlamada duraksama ve gecikme (Hesitancy)", "isCorrect": True}
        ],
        "correctAnswer": "E",
        "explanation": "İdrara başlamada gecikme ve duraksama (Hesitancy), mesane çıkım obstrüksiyonuna bağlı gelişen bir 'işeme (obstrüktif)' semptomudur. Pollaküri, noktüri, urgency ve dizüri ise depolama (irritatif) semptomlarıdır."
    }
))

# ==============================================================================
# SLAYT 21
# ==============================================================================
slides.append(make_slide(
    21,
    "İrritatif ve Fonksiyonel Bozukluklar: Dizüri, İnkontinans, Pnömatüri ve Hematospermi",
    "Ağrının Zamanlaması, İnkontinans Tipleri, Gaz Çıkışı ve Ejakülatta Kan",
    """**Dizüri**, idrar yaparken üretra ve mesane boynundaki nosiseptif reseptörlerin inflamatuar irritasyonu sonucu ortaya çıkan ağrılı ve yanmalı işemedir. Dizürinin miksiyon içindeki zamanlaması lezyonun yerini gösterir: Eğer ağrı idrarın ilk akmaya başladığı anda (başlangıçta) belirginse problem üretradadır (üretrit); eğer ağrı işemenin tam sonunda ve mesane boşalırken suprapubik krampla hissediliyorsa patoloji mesane tabanında veya trigondadır (sistit). **İnkontinans** tiplerinden *Stres İnkontinans*, öksürme, hapşırma, gülme ve ağır kaldırma gibi karın içi basıncını artıran anlarda sfinkter yetersizliğine bağlı damla damla kaçırmadır (gebelik, doğum, menopoz temel nedendir); *Urge İnkontinans* ise aniden gelen şiddetli işeme hissiyle tuvalete yetişemeden mesanenin istemsiz kasılması sonucu idrar kaçırmadır (enfeksiyon, taş, nörolojik hastalıklar).

**Pnömatüri**, idrar yaparken idrarla birlikte havanın veya gaz kabarcıklarının çıkması durumudur. Hastalar idrar yaparken köpürme veya gaz çıkışı tarif ederler. Pnömatürinin üç temel klinik nedeni vardır: 1) İdrar yollarına yakın zamanda kateterizasyon, sistoskopi veya cerrahi enstrümantasyon uygulanmış olması (iyatrojenik hava girişi), 2) Gastrointestinal sistem ile mesane arasında fistül gelişmesi (en sık divertikülit veya kolorektal kansere bağlı kolovezikal fistül; fekalüri de eşlik edebilir), ve 3) Kontrolsüz diyabetik hastalarda idrardaki yüksek glukozu fermente ederek karbondioksit oluşturan bakterilerle (E. coli, Klebsiella, Proteus) gelişen nekrotizan amfizematöz sistit veya amfizematöz piyelonefrit tablosudur.

**Hematospermi**, seminal sıvıda (ejakülatta) kan bulunmasıdır. Genç erkeklerde son derece korkutucu bir tablo olmasına rağmen, olguların neredeyse tamamında prostat veya seminal veziküllerin nonspesifik, benign ve geçici inflamasyonuna bağlı olarak gelişir ve birkaç hafta içinde kendiliğinden geriler. Nadiren etyolojik bir patojen saptanır. Ancak hematospermi tablosu düzelmeyen, persistan olan veya 40 yaş üstü erkeklerde: Prostat kanserini dışlamak için serum PSA düzeyi ve parmakla rektal muayene (PRM), ürogenital tüberkülozu dışlamak için genital/rektal muayene ve üretral transizyonel hücreli karsinomu (TCC) dışlamak için idrar sitolojisi yapılmalıdır.""",
    "İdrarla gaz çıkması (pnömatüri); kolovezikal fistül, yakın zamanda enstrümantasyon veya diyabette gaz üreten bakterilerin yol açtığı amfizematöz sistiti gösterir.",
    "Düzelmeyen ve persistan hematospermi olgularında ürogenital tüberküloz, prostat adenokarsinoması (PSA/PRM) ve transizyonel hücreli karsinom (idrar sitolojisi) araştırılmalıdır.",
    {
        "id": "prac-use-021",
        "stem": "62 yaşında diyabetik bir hasta, idrar yaparken hava kabarcıkları çıktığını (pnömatüri) ve idrarının kötü koktuğunu ifade ediyor. Hastanın yakın zamanda herhangi bir ürolojik girişim öyküsü bulunmamaktadır. Bu klinik bulgunun etyolojisinde öncelikle düşünülmesi gereken patolojiler hangi seçenekte doğru verilmiştir?",
        "options": [
            {"key": "A", "text": "Enterovezikal (kolovezikal) fistül veya gaz üreten mikroorganizmalarla gelişen amfizematöz enfeksiyon", "isCorrect": True},
            {"key": "B", "text": "Benign prostat hiperplazisi veya primer üretra darlığı", "isCorrect": False},
            {"key": "C", "text": "Basit böbrek kisti rüptürü veya glomerülonefrit", "isCorrect": False},
            {"key": "D", "text": "Minimal değişiklik hastalığı veya nefrotik sendrom", "isCorrect": False},
            {"key": "E", "text": "Saf stres tipi üriner inkontinans veya pelvik taban relaksasyonu", "isCorrect": False}
        ],
        "correctAnswer": "A",
        "explanation": "Enstrümantasyon öyküsü olmayan bir hastada pnömatüri görülmesi ya bağırsak ile mesane arasında fistül varlığını (kolovezikal fistül) ya da diyabette gaz oluşturan bakterilerle (E. coli, Klebsiella) meydana gelen amfizematöz sistiti/piyelonefriti gösterir."
    }
))

# ==============================================================================
# SLAYT 22
# ==============================================================================
slides.append(make_slide(
    22,
    "Sistit, Akut Piyelonefrit ve Kronik Piyelonefrit Klinik Tabloları",
    "Mukozal İnflamasyon Triadı, Parankimal Süpürasyon ve Skarlı Küçülmüş Böbrek",
    """**Sistit**, mesane mukozasının bakteriyel enfeksiyonu ve inflamasyonudur. Klinik olarak dizüri (ağrılı işeme), pollaküri (sık idrara çıkma) ve urgency (ani sıkışma hissi) şeklindeki klasik depolama semptom triadı ile karakterizedir; bu tabloya sıklıkla suprapubik rahatsızlık/ağrı ve olguların bir kısmında makroskopik hematüri eşlik eder. İnflamasyon mesane mukozası ile sınırlı olduğu için akut sistitte yüksek ateş, titreme veya yan ağrısı gibi sistemik toksisite bulguları BEKLENMEZ. Sistit benzeri semptomlar üretrit, vajinit gibi enfeksiyöz patolojilerde görülebileceği gibi interstisyel sistit, mesane taşları ve mesane karsinoması gibi non-enfektif hastalıklarda da ortaya çıkabilir.

**Akut Piyelonefrit**, böbrek toplayıcı sisteminin ve renal parankimin akut süpüratif bakteriyel enfeksiyonudur. Klinik tablosunu sistitten ayıran kardinal bulgular: Ani başlayan yüksek ateş (genellikle >38.5 °C), titreme/titremeyle yükselen ateş, belirgin halsizlik, bulantı-kusma ve en önemlisi tek veya çift taraflı **flank (yan) ağrısıdır**. Fizik muayenede kostovertebral açı hassasiyeti (KVAH / Murphy böbrek darbe testi) pozitiftir. Ders notunun en kritik vurgusu: **'Yan ağrısının eşlik etmediği durumlarda akut piyelonefritten söz edilemez.'** Ancak spinal kord hasarlı paraplejik hastalarda ve kognitif fonksiyonları bozulmuş yaşlılarda ağrı lokalize edilemediği için tanı koymak güçleşebilir; bu grupta izole ateş veya deliryum araştırılmalıdır.

**Kronik Piyelonefrit**, akut piyelonefritten tamamen farklı olarak klinik değil, **morfolojik, radyolojik ve fonksiyonel** bir tanıdır. Genellikle çocukluk çağında tekrarlayan akut enfeksiyonlar, vezikoüreteral reflü (reflü nefropatisi) veya kronik obstrüktif üropatiler zemininde gelişir. Böbrek parankiminde ilerleyici tübülointerstisyel hasar, fibrozis ve kaliksler üzerinde çekintilere yol açan düzensiz U-şekilli polar skarlar oluşur. Zamanla böbrek asimetrik olarak küçülür, kaliksler deforme olur (küntleşir) ve kalıcı renal fonksiyon kaybı ile son dönem böbrek yetmezliğine ilerler.""",
    "Akut piyelonefrit tanısı için yan (flank) ağrısı, ateş ve kostovertebral açı hassasiyeti zorunludur; yan ağrısının olmadığı tabloda akut piyelonefritten söz edilemez.",
    "Kronik piyelonefrit klinik bir enfeksiyon atağı değil; tekrarlayan enfeksiyon ve reflü zemininde gelişen, küçülmüş ve polar skarlı böbrekle karakterize morfolojik/radyolojik bir tanıdır.",
    {
        "id": "prac-use-022",
        "stem": "29 yaşında kadın hasta 2 gündür devam eden 39 °C ateş, titreme, sağ böbrek lojunda şiddetli yan ağrısı ve bulantı şikayetiyle başvuruyor. Fizik muayenede sağ kostovertebral açı hassasiyeti belirgin pozitif saptanıyor. Bu klinik tablonun tanısı ve patolojisi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
        "options": [
            {"key": "A", "text": "Tablo basit akut sistit olup hastaya yalnızca 3 günlük oral tedavi verilip taburcu edilmelidir.", "isCorrect": False},
            {"key": "B", "text": "Yan ağrısı, ateş ve KVAH birlikteliği böbrek parankiminin akut bakteriyel enfeksiyonu olan Akut Piyelonefriti gösterir.", "isCorrect": True},
            {"key": "C", "text": "Hastada yan ağrısı olmasına rağmen ateş olmaması nedeniyle piyelonefrit tanısı kesinlikle dışlanır.", "isCorrect": False},
            {"key": "D", "text": "Bu tablonun tanısı yalnızca renal biyopside glomerül nekrozu gösterilerek konulabilir.", "isCorrect": False},
            {"key": "E", "text": "Olguların tamamında etken cinsel yolla bulaşan Chlamydia trachomatis'tir.", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "Yüksek ateş, titreme, tek taraflı yan ağrısı ve kostovertebral açı hassasiyeti böbrek parankiminin akut süpüratif enfeksiyonu olan Akut Piyelonefritin kardinal klinik göstergeleridir."
    }
))

# ==============================================================================
# SLAYT 23
# ==============================================================================
slides.append(make_slide(
    23,
    "Prostatit Sendromları ve NIH Sınıflaması: Akut, Kronik ve KP/KPAS",
    "Kategori I-IV Yelpazesi, Rektal Tuşe Kontrendikasyonu ve Pelvik Ağrı",
    """Prostatit, prostat bezinin enfeksiyonu ve inflamatuar hastalıklarını kapsayan heterojen bir klinik sendromdur. Polikliniklere başvuran hastaların çok büyük bir kısmında prostatit semptomları bulunmasına rağmen, olguların yalnızca %5 ila %10'unda kanıtlanabilir bir mikrobiyal etken saptanabilir; geri kalan %90'lık kısım abakteriyel ve nöromusküler süreçlerden kaynaklanır. Amerikan Ulusal Sağlık Enstitüsü (NIH) prostatitleri 4 ana kategoride sınıflandırmıştır:
- *Kategori I:* Akut Bakteriyel Prostatit
- *Kategori II:* Kronik Bakteriyel Prostatit
- *Kategori III:* Kronik Prostatit / Kronik Pelvik Ağrı Sendromu (KP/KPAS - IIIA İnflamatuar, IIIB Non-inflamatuar)
- *Kategori IV:* Asemptomatik İnflamatuar Prostatit

**Akut Bakteriyel Prostatit (Kategori I):** Ani başlayan titremeyle yükselen yüksek ateş, şiddetli perineal ve suprapubik ağrı, dizüri, acil idrar yapma hissi ve halsizlik ile seyreder. Şişen prostat bezi üretrayı tıkayarak akut üriner retansiyona yol açabilir. Bu tabloda en kritik kural: **Parmakla rektal muayene (PRM) ve agresif prostat masajı KESİNLİKLE KONTRENDİKEDİR!** İltihaplı ve ödemli prostata baskı yapmak bakterilerin doğrudan dolaşıma karışmasına, bakteriyemiye ve septik şoka neden olabilir. Komplikasyon olarak prostat apsesi ve bakteriyemi gelişebilir.

**Kronik Bakteriyel Prostatit (Kategori II)** tekrarlayan relaps ÜSE atakları, hematospermi, skrotal ve lumbosakral ağrı ile seyreder ve prostat tüberkülozunu maskeleyebileceği unutulmamalıdır. **KP/KPAS (Kategori III)** ise klinik olarak en sık görülen formdur; son 6 ay içinde en az 3 aydır devam eden perine, testis, penis kökü veya suprapubik ağrı mevcuttur. Ağrılı ejakülasyon önemli bir semptomdur. Prostat masajı sonrası sıvıda veya idrarda lökosit >10 ise Kategori IIIA (inflamatuar), lökosit <10 ise Kategori IIIB (non-inflamatuar) olarak adlandırılır. Kategori IV ise tamamen şikayetsiz olup infertilite veya PSA yüksekliği araştırmasında tesadüfen saptanan tablodur.""",
    "Akut bakteriyel prostatitte bakteriyemi ve sepsis riskinden dolayı sert parmakla rektal muayene ve prostat masajı kesinlikle yapılmamalıdır.",
    "NIH sınıflamasına göre prostat masajı sonrası idrar sedimentinde veya sekresyonda >10 lökosit olması Kategori IIIA (inflamatuar KP/KPAS), <10 lökosit olması Kategori IIIB'dir.",
    {
        "id": "prac-use-023",
        "stem": "42 yaşında erkek hasta yüksek ateş (39.2 °C), titreme, perineal bölgede şiddetli dolgunluk ve ağrı, idrar yaparken yoğun yanma ve idrar yapamama (akut retansiyon) şikayetiyle acile başvuruyor. Bu hastanın klinik yaklaşımında kesinlikle kaçınılması gereken uygulama aşağıdakilerden hangisidir?",
        "options": [
            {"key": "A", "text": "İntravenöz geniş spektrumlu antibiyotik başlanması", "isCorrect": False},
            {"key": "B", "text": "Kan ve idrar kültürlerinin alınması", "isCorrect": False},
            {"key": "C", "text": "Sert parmakla rektal muayene ve tanısal prostat masajı yapılması", "isCorrect": True},
            {"key": "D", "text": "Retansiyonu gidermek amacıyla suprapubik sistostomi planlanması", "isCorrect": False},
            {"key": "E", "text": "Vital bulguların ve kan basıncının yakın takibi", "isCorrect": False}
        ],
        "correctAnswer": "C",
        "explanation": "Akut bakteriyel prostatitte aşırı inflamasyon ve apse riski nedeniyle sert parmakla rektal muayene ve prostat masajı kontrendikedir; bakterilerin kana karışarak bakteriyemi ve septik şok oluşturma riski bulunur."
    }
))

# ==============================================================================
# SLAYT 24
# ==============================================================================
slides.append(make_slide(
    24,
    "Skrotal İnflamasyonlar ve Üretritler: Orşit, Epididimit ve Üretrit Ayrımı",
    "Kabakulak Orşiti, Testis Torsiyonu Acil Ayrımı ve Gonokoksik vs Non-Gonokoksik Tablo",
    """**Orşit**, testisin inflamasyonudur. En sık formu postpubertal dönemde kabakulak geçiren erkeklerin %20-30'unda görülen 'Kabakulak Orşiti'dir; olguların %20'sinde bilateral seyreder ve kalıcı testiküler atrofi ile azoospermiye/infertiliteye yol açabilir. Akut orşitte skrotum eritemli, ödemli ve ileri derecede hassastır. Genç erkek ve çocuklarda akut skrotal ağrıda yapılması gereken **en kritik ayırıcı tanı Testis Torsiyonudur**. Doppler US yardımcı olsa da parsiyel torsiyonda yanıltıcı olabilir; torsiyon şüphesi varsa testis nekrozunu önlemek için acil cerrahi eksplorasyon şarttır. **Epididimit** ise epididimin inflamasyonu olup retrograde asendan yayılımla genellikle kuyruk (kauda) kısmından başlar ve korda yayılır; testisin de etkilenmesiyle tablo epididimo-orşite dönüşür.

**Üretrit**, dizüri, üretral kaşıntı ve üretral akıntı ile seyreden, cinsel yolla bulaşan en sık klinik sendromdur. Etyolojik olarak ikiye ayrılır:
1. **Gonokokkal Üretrit (GU):** Etken Neisseria gonorrhoeae'dir (Gram-negatif hücre içi kahve çekirdeği diplokok). Kuluçka süresi **kısa (2-7 gün)**, başlangıcı **ani**, akıntısı **sarı-yeşil, bol ve pürülan**, dizüri ise belirgindir.
2. **Non-Gonokokkal Üretrit (NGU):** En sık etken Chlamydia trachomatis'tir (%30-50). Diğer etkenler Ureaplasma urealyticum, Mycoplasma genitalium, Trichomonas vaginalis ve Herpes simplex virüstür. Kuluçka süresi **uzun (10-21 gün)**, başlangıcı **sinsi/dereceli**, akıntısı **az miktarda, açık renkli, müköz veya sulu**, dizüri ise hafiftir.

Üretral akıntının mikroskopisinde polimorfonükleer lökositlerin içinde Gram-negatif diplokokların görülmesi gonokoksik üretrit için kesin tanı koydurucudur. 40 yaş üstü erkeklerde geçirilmiş CYBH, katater veya üretral travma öyküsü yoksa üretral akıntının en sık nedeni mesane çıkımını daraltan benign prostat hiperplazisidir. Tedavide gonore ve klamidyanın sıklıkla (%20-30) ko-enfeksiyon oluşturduğu unutulmamalı ve her iki etkene yönelik kombine tedavi verilmelidir.""",
    "Akut skrotal ağrısı olan bir gençte veya çocukta acil cerrahi eksplorasyon gerektiren Testis Torsiyonu ekarte edilmeden hasta epididimit/orşit kabul edilerek evine gönderilemez.",
    "Gonokokkal üretrit kısa kuluçka süresi (2-7 gün), ani başlangıç ve bol pürülan sarı akıntı ile; Chlamydia kaynaklı non-gonokokkal üretrit ise uzun kuluçka süresi (10-21 gün) ve az, sulu akıntı ile karakterizedir.",
    {
        "id": "prac-use-024",
        "stem": "Şüpheli cinsel ilişkiden 14 gün sonra başlayan hafif dizüri ve sabahları üretradan az miktarda gelen açık renkli, müköz/sulu akıntı şikayetiyle başvuran erkek hastanın akıntı yaymasında Gram-negatif diplokok görülmemiştir. Bu hastada en olası klinik tablo ve en sık sorumlu mikroorganizma aşağıdakilerden hangisidir?",
        "options": [
            {"key": "A", "text": "Gonokokkal üretrit - Neisseria gonorrhoeae", "isCorrect": False},
            {"key": "B", "text": "Non-gonokokkal üretrit - Chlamydia trachomatis", "isCorrect": True},
            {"key": "C", "text": "Akut piyelonefrit - Escherichia coli", "isCorrect": False},
            {"key": "D", "text": "Kabakulak orşiti - Paramyxovirüs", "isCorrect": False},
            {"key": "E", "text": "Kronik sistit - Proteus mirabilis", "isCorrect": False}
        ],
        "correctAnswer": "B",
        "explanation": "10-21 günlük uzun kuluçka süresi, sinsi başlangıç, az miktarda sulu/müköz akıntı ve mikroskopide diplokok görülmemesi Chlamydia trachomatis kaynaklı Non-gonokokkal üretritin (NGU) tipik özellikleridir. Gonorede ise kuluçka 2-7 gün olup bol pürülan sarı akıntı görülür."
    }
))

print(f"Toplam {len(slides)} slayt basariyla hazirlandi.")

deck_output = {
    "deckId": "learn-uriner-sistem-enfeksiyonlari-epidemiyoloji",
    "title": "Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi",
    "slides": slides
}

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(deck_output, f, ensure_ascii=False, indent=2)

print(f"JSON basariyla kaydedildi: {OUTPUT_PATH}")

# Verify validity
with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
    loaded = json.load(f)
assert loaded["deckId"] == "learn-uriner-sistem-enfeksiyonlari-epidemiyoloji"
assert len(loaded["slides"]) == 24
print("Dogrulama basarili! 24 slayt eksiksiz.")
