# -*- coding: utf-8 -*-
"""Part 2: Slides 13 to 24 for Kronik ve Granülomatöz Enflamasyon Deck."""

slides_part2 = [
    # SLIDE 13
    {
        "slideNumber": 13,
        "title": "Mast Hücreleri ve Kronikleşmede Rol Oynayan Nötrofiller",
        "subtitle": "Mediyatör Köprüleri, Kronik Osteomiyelit ve Süregelen Nötrofilik Yangı",
        "content": (
            "Derslerimizde sıklıkla nötrofillerin akut, mononükleer hücrelerin ise kronik enflamasyona ait olduğunu vurgularız. "
            "Fakat doğa her zaman ders kitaplarındaki şematik kutulara sığmaz. Klinik patolojide bazı kronik enflamasyon tablolarında "
            "aylar geçmesine rağmen nötrofillerin alandan hiç çekilmediğini, hatta baskın hücre olarak hasara devam ettiğini görürüz. "
            "Bunun en klasik ve dramatik örneği 'Kronik Osteomiyelit'tir. Kemik dokusunda kan dolaşımının bozulmasıyla oluşan nekrotik "
            "kemik parçaları (sekestr), bakterilerin tutunması için korunaklı bir biyofilm yuvası oluşturur; bağışıklık sistemi bu ölü "
            "kemiği eritemediği için aylar boyu bölgeye kesintisiz nötrofil pompalar. Benzer şekilde sigara dumanına bağlı kronik obstrüktif "
            "akciğer hastalığında (KOAH) ve psöriasis plaklarında da uzamış nötrofil infiltrasyonu kronik hasarın motorudur.\n\n"
            "Diğer yandan mast hücreleri, hem akut alerjik yanıtların hem de kronik immün reaksiyonların kavşak noktasında bekleyen "
            "nöbetçilerdir. Kemik iliği kökenli olan mast hücreleri, yüzeylerindeki KIT (CD117) reseptörü aracılığıyla olgunlaşır ve "
            "özellikle bağ dokusunda damar komşuluklarında konuşlanır. Yüzeylerindeki yüksek afiniteli Fc-epsilon-RI reseptörlerine "
            "bağlı IgE molekülleri antijenle çapraz bağlandığında degranüle olurlar.\n\n"
            "Mast hücrelerinin kronik enflamasyondaki kritik rolü, yalnızca saniyeler içinde boşalttıkları vazoaktif aminlerden (histamin) "
            "ibaret değildir. Asıl hünerleri, uyarımı takip eden saatler içinde gen ekspresyonu yoluyla sentezledikleri geniş sitokin "
            "yelpazesidir. Masif miktarda TNF-alfa, IL-1, kemokinler ve lökotrienler salgılayarak endotel hücrelerini sürekli uyarırlar "
            "ve dokuya monosit, eozinofil ve T lenfositlerinin akışını canlı tutarlar. Bu özellikleriyle mast hücreleri akut bir atağı "
            "kolayca kronik bir yangı yangınına çevirebilen moleküler bir köprü vazifesi görürler."
        ),
        "synthesisNarrative": (
            "Kronik osteomiyelitte sekestr varlığı nedeniyle nötrofiller aylarca yangı alanında kalabilir; mast hücreleri ise "
            "degranülasyonun ötesinde sentezledikleri TNF-alfa ve kemokinlerle kronik mononükleer infiltrasyonu besler."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Kronik enflamasyon kural olarak mononükleer hücrelerle karakterize olsa da; kronik osteomiyelitte nekrotik sekestr kemik nedeniyle nötrofiller aylarca alanda kalmaya devam eder.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Mast hücreleri yüzeyinde c-kit (CD117) reseptörü taşır; akut fazda histamin salarken kronik fazda de novo TNF-alfa ve lipid mediyatörleri üreterek yangıyı sürekli kılar.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Sekestr kemik içeren kronik osteomiyelitte nötrofiller persistan olarak bulunur.",
            "Mast hücreleri c-kit (CD117) ile karakterize bağ dokusu nöbetçi hücreleridir.",
            "De novo üretilen TNF ve lökotrienler mast hücrelerinin kronik yangıdaki etkisini açıklar."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-013",
            "question": "Aşağıdaki klinik-patolojik durumlardan hangisinde, tablonun kronik seyirli olmasına rağmen histopatolojik incelemede bol miktarda aktif nötrofil lökosit infiltrasyonu görülmesi en tipiktir?",
            "options": [
                "A) Sarkoidoz hiler lenfadenopatisi",
                "B) Hashimoto tiroiditi",
                "C) Sekestr kemik odağı içeren kronik osteomiyelit",
                "D) Tersiyer sifilis gom lezyonu",
                "E) Silikozise bağlı pulmoner nodül"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Kronik osteomiyelitte ölü kemik dokusu (sekestr) fagositozla yok edilemediği ve bakteriyel biyofilmleri barındırdığı için, aylar süren kronik bir süreç olmasına rağmen nötrofilik infiltrasyon kesintisiz olarak devam eder. Sarkoidoz, Hashimoto, sifilis ve silikoziste mononükleer hücreler ve granülomlar hakimdir."
        }
    },

    # SLIDE 14
    {
        "slideNumber": 14,
        "title": "Granülomatöz Enflamasyonun Tanımı ve Patogenezi",
        "subtitle": "Sindirilemeyen Ajanlara Karşı İzolasyon Yanıtı ve Gecikmiş Tip Aşırı Duyarlılık",
        "content": (
            "Şimdi konumuzun en sofistike, patolojinin en karakteristik morfolojik tablolarından birine geçiyoruz: "
            "Granülomatöz Enflamasyon. Granülomatöz enflamasyon, kronik enflamasyonun çok özel ve özelleşmiş bir alt tipidir. "
            "Organizmanın rutin fagositoz ve enzimatik sindirim mekanizmalarıyla ortadan kaldıramadığı, parçalanmaya dirençli "
            "mikroorganizmalara veya yabancı partiküllere karşı geliştirdiği bir 'hücresel karantina ve tecrit' stratejisidir.\n\n"
            "Vücut bu inatçı ajanı yok edemeyeceğini anladığında, onu sağlıklı çevre dokudan tamamen izole etmek amacıyla etrafına "
            "adeta hücresel bir hapishane duvarı örer. Bu yapının merkezinde modifiye olmuş makrofajlar yer alır. Patogenetik açıdan "
            "granülom oluşumu iki temel mekanizmayla gerçekleşir: İmmün granülomlar ve Yabancı cisim granülomları. İmmün granülomlar, "
            "persistan antijenik uyarılara karşı gelişen klasik bir Tip IV (hücresel / gecikmiş tip) aşırı duyarlılık reaksiyonudur.\n\n"
            "Moleküler mekanizma kusursuz bir orkestrasyonla işler: Patojeni fagosite eden ancak sindiremeyen makrofaj, antijeni "
            "MHC-II üzerinde naif CD4+ T hücrelerine sunar ve IL-12 salgılar. Antijene spesifik T hücreleri Th1 fenotipine polarize "
            "olarak bol miktarda İnterferon-gama (IFN-γ) üretir. Ortama yayılan IFN-γ, yangı sahasındaki makrofajları yoğun bir şekilde "
            "bombardımana tutar. Bu sürekli IFN-γ uyarısı altında kalan makrofajlar olağanüstü bir morfolojik ve fonksiyonel dönüşüm "
            "geçirirler: Fagositik hücre kimliğinden sıyrılarak, birbirine sıkıca kenetlenen ve epitel hücrelerini taklit eden "
            "'Epiteloid Histiyositlere' dönüşürler. Bu hücrelerin nodüler bir küme oluşturmasıyla granülomun çekirdeği atılmış olur."
        ),
        "synthesisNarrative": (
            "Granülomatöz enflamasyon, sindirilemeyen ajanları tecrit etmek için oluşan özel bir kronik yangı paternidir; "
            "Tip IV aşırı duyarlılık zemininde T hücre kaynaklı IFN-γ'nın makrofajları epiteloid histiyositlere dönüştürmesiyle kurulur."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Granülom oluşumunun patogenetik omurgası Tip IV (gecikmiş tip) aşırı duyarlılık reaksiyonudur; T hücresinden salınan IFN-γ makrofajları epiteloid histiyositlere dönüştüren kilit sitokindir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Granülomun olmazsa olmaz temel yapıtaşı 'Epiteloid Histiyosit' (modifiye makrofaj) kümesidir. Çok çekirdekli dev hücreler veya kazeifikasyon nekrozu her granülomda bulunmak zorunda değildir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Granülom sindirilemeyen patojen veya partikülleri izole eden hücresel bir duvardır.",
            "İmmün granülom patogenezinde IL-12 / Th1 / IFN-γ moleküler aksı esastır.",
            "Epiteloid histiyosit kümesi olmadan granülom tanısı konulamaz."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-014",
            "question": "İmmün granülom gelişiminde makrofajların epiteloid histiyositlere dönüşümünü indükleyen ve granülom mimarisini başlatan en kritik T lenfosit kaynaklı sitokin aşağıdakilerden hangisidir?",
            "options": [
                "A) İnterlökin-4 (IL-4)",
                "B) İnterferon-gama (IFN-γ)",
                "C) İnterlökin-10 (IL-10)",
                "D) Transforming Growth Factor-beta (TGF-β)",
                "E) İnterlökin-5 (IL-5)"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Granülomatöz enflamasyonda aktive Th1 lenfositlerinden salgılanan İnterferon-gama (IFN-γ), dokudaki makrofajları uyararak onları epiteloid histiyositlere dönüştüren ve granülomun hücresel çatısını kuran en temel sitokindir."
        }
    },

    # SLIDE 15
    {
        "slideNumber": 15,
        "title": "Epiteloid Histiyositlerin Biyolojisi",
        "subtitle": "Nükleer ve Sitoplazmik Değişimler, Terlik Nükleus ve Salgısal Uzmanlaşma",
        "content": (
            "Granülomun tartışmasız en temel hücresel yapıtaşı, histopatologların mikroskopta ilk aradığı hücre olan "
            "'Epiteloid Histiyosit'tir (modifiye makrofaj). Bu hücreler adını, birbirlerine sıkıca yaslanarak tabakalar oluşturan "
            "epitel hücrelerine olan morfolojik benzerliklerinden alırlar. Ancak epiteloid histiyositler epitelyal dokudan değil, "
            "tamamen mononükleer fagositik sistemden köken alırlar.\n\n"
            "Işık mikroskobunda epiteloid histiyositlerin morfolojisi son derece ayırt edicidir: Hücre sınırları belirsizleşmiştir; "
            "yan yana gelen hücrelerin sitoplazmaları adeta birbiri içine akmış gibi (sinsityal) bir görünüm sergiler. Sitoplazmaları "
            "son derece geniş, bol miktarda ve eozin boyasıyla soluk pembe (eozinofilik) ve ince granüllü boyanır. En karakteristik "
            "özellikleri ise nükleus morfolojisidir: Normal monositin böbrek biçimli nükleusu gitmiş; yerine uzun, oval, uçları yuvarlaklaşmış, "
            "veziküler (kromatin ağı ince ve açık renk) ve patoloji literatüründe 'terlik tabanı' ya da 'ayakkabı tabanı' (slipper-shaped) "
            "olarak tarif edilen nükleus gelmiştir. Nükleolleri belirgindir.\n\n"
            "Biyolojik fonksiyon açısından ise epiteloid histiyosit çok şaşırtıcı bir metamorfoz geçirmiştir: Klasik makrofajın sahip olduğu "
            "fagositoz kapasitesi bu hücrelerde belirgin derecede azalmıştır! Artık ortalıkta dolaşıp parçacık yutan ameboid bir hücre "
            "değildir. Buna karşılık hücrenin endoplazmik retikulum ve Golgi organelleri muazzam derecede hipertrofiye uğramıştır; "
            "epiteloid histiyosit yüksek sekresyon (salgı) kapasitesine sahip bir hücreye dönüşmüştür. Sürekli olarak ortama TNF-alfa, "
            "fibrojenik büyüme faktörleri, anjiyotensin dönüştürücü enzim (ACE) ve lizozomal enzimler salgılayarak granülomun sınırlarını "
            "tahkim eder ve çevreye lenfositleri çeker."
        ),
        "synthesisNarrative": (
            "Epiteloid histiyositler; bol eozinofilik sitoplazmalı, belirsiz sınırlı, terlik/ayakkabı tabanı şeklinde veziküler "
            "nükleuslu modifiye makrofajlardır; fagositoz yetenekleri azalmış ancak salgısal kapasiteleri belirgin artmıştır."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Epiteloid histiyositlerin fagositoz kapasitesi normal makrofaja göre azalmıştır; buna karşın protein sentez ve sekresyon (salgı) kapasiteleri dramatik şekilde artmıştır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Mikroskobik incelemede geniş eozinofilik sitoplazmalı, belirsiz hücre sınırlı ve 'terlik/ayakkabı tabanı' şeklinde veziküler nükleus içeren hücre Epiteloid Histiyosit'tir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Hücre sınırları sinsityal şekilde birbiriyle kaynaşmış gibi görünür.",
            "Veziküler, açık kromatinli nükleus terlik tabanına benzetilir.",
            "Granülom oluşumunda epiteloid histiyosit varlığı tanı için zorunludur."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-015",
            "question": "Granülomatöz lezyonların merkezini oluşturan epiteloid histiyositlerin sitomorfolojik ve fonksiyonel özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Fagositoz kapasiteleri klasik makrofajlara göre katbekat artmıştır",
                "B) Hücre sınırları çok keskin olup bol miktarda musin salgılarlar",
                "C) Nükleusları hiperkromatik, piknotik ve at nalı şeklinde periferik dizilimlidir",
                "D) Bol eozinofilik sitoplazmalı, veziküler 'terlik tabanı' nükleuslu ve salgı kapasitesi yüksek hücrelerdir",
                "E) Kemik iliğindeki B lenfositlerinin terminal farklılaşmasıyla meydana gelirler"
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği doğrudur. Epiteloid histiyositler; geniş soluk eozinofilik sitoplazmalı, belirsiz sınırlı, veziküler 'terlik/ayakkabı tabanı' biçiminde nükleuslu hücrelerdir. Fagositoz yetenekleri azalmış, protein ve sitokin salgı kapasiteleri ise belirgin olarak artmıştır."
        }
    },

    # SLIDE 16
    {
        "slideNumber": 16,
        "title": "Çok Çekirdekli Dev Hücrelerin Oluşumu",
        "subtitle": "Epiteloid Hücre Füzyonu, Moleküler Mekanizmalar ve Biyolojik İşlev",
        "content": (
            "Granülom sahasına baktığımızda hemen gözümüze çarpan, onlarca nükleusu aynı sitoplazma havuzunda barındıran "
            "devasa yapılar vardır: Çok Çekirdekli Dev Hücreler (Multinükleer Dev Hücreler). Bu hücreler 40 ila 100 mikrometre "
            "çapına ulaşabilen, adeta hücresel birer titandır. Geçmişte bu dev hücrelerin nükleusun sitoplazma bölünmeksizin "
            "art arda mitoz geçirmesiyle (endomitoz) oluştuğu sanılırdı. Ancak modern hücre biyolojisi kanıtlamıştır ki, dev hücreler "
            "kesinlikle mitozla değil, tek çekirdekli epiteloid histiyositlerin hücre zarlarının birbirleriyle birleşmesi (füzyonu) "
            "sonucu meydana gelir.\n\n"
            "Epiteloid histiyositlerin birbirine kaynaşması rastgele bir süreç değildir; karmaşık bir moleküler füzyon programı "
            "tarafından kontrol edilir. T hücrelerinden salgılanan IFN-γ ve ortamdaki IL-4/IL-13 sitokinleri, histiyosit yüzeyindeki "
            "özgül füzyon moleküllerinin ekspresyonunu tetikler. Bunların en önemlileri CD44, Dendritik Hücreye Özgü Transmembran Protein "
            "(DC-STAMP) ve Makrofaj Füzyon Reseptörü (MFR / SIRP-alfa) ile CD47 etkileşimidir. Bu moleküler kancalar iki komşu "
            "hücre zarını birbirine çeker; hücre iskeletinde aktin yeniden düzenlenmesi gerçekleşir ve lipid çift tabakaları kaynaşarak "
            "tek bir devasa sitoplazmik gövde oluşturur.\n\n"
            "Tek bir dev hücre içerisinde 20, 50 ve bazen 100'den fazla nükleus yer alabilir. Peki bu birleşmenin biyolojik mantığı nedir? "
            "Küçük bir makrofajın tek başına yutamayacağı büyüklükteki bir cisim (örneğin cerrahi bir iplik, bir asbest lifi ya da "
            "kolonize olmuş geniş bir mantar hif kümesi), dev hücrenin devasa sitoplazması tarafından sarılır. Böylece hücre dışı "
            "sindirim enzimlerinin yoğunlaşacağı kapalı bir mikro-çevre oluşturulur. Ancak unutulmamalıdır ki, çok çekirdekli dev hücreler "
            "granülomatöz reaksiyonu zenginleştiren çarpıcı unsurlar olsa da, bir lezyona granülom demek için dev hücre varlığı şart "
            "değildir; epiteloid histiyosit kümesi tek başına yeterlidir."
        ),
        "synthesisNarrative": (
            "Çok çekirdekli dev hücreler, mitozla değil, epiteloid histiyositlerin DC-STAMP ve CD44 gibi fusogenik moleküllerle "
            "birbirine kaynaşması (füzyon) sonucu oluşur; sindirilemeyen büyük partikülleri kuşatmayı amaçlar."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Dev hücreler nükleusun bölünmesiyle (mitoz) değil, epiteloid histiyositlerin sitoplazmik füzyonu (kaynaşması) ile meydana gelir. Granülom tanısı için dev hücre bulunması şart değildir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Granülomatöz enflamasyonda izlenen çok çekirdekli dev hücrelerin kökeni Monosit / Makrofaj (Epiteloid histiyosit) serisidir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Dev hücre çapı 100 mikrometreye, çekirdek sayısı onlarcaya ulaşabilir.",
            "DC-STAMP ve integrinler makrofaj membran füzyonunda kilit rol oynar.",
            "Büyük yabancı cisimleri ve paraziter partikülleri kuşatmaya yarar."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-016",
            "question": "Granülomatöz enflamasyon odağında saptanan çok çekirdekli dev hücrelerin biyogenezi ve özellikleri ile ilgili aşağıdaki ifadelerden hangisi BİYOLOJİK OLARAK DOĞRUDUR?",
            "options": [
                "A) Tek bir makrofajın sitokinezi olmaksızın art arda çok sayıda mitoz bölünme geçirmesiyle oluşurlar",
                "B) Epiteloid histiyositlerin hücre zarlarının füzyonu (birbirine kaynaşması) sonucu meydana gelirler",
                "C) Granülomatöz enflamasyon tanısı koyabilmek için biyopside mutlaka dev hücre görülmesi zorunludur",
                "D) Bu dev hücreler kemik iliğindeki megakaryositlerin dokuya göç etmiş formlarıdır",
                "E) Sitoplazmalarında fagozom oluşturma yetenekleri tamamen kaybolmuştur ve metabolik olarak inaktiftirler"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Çok çekirdekli dev hücreler endomitozla değil; IFN-γ ve sitokinlerin etkisiyle epiteloid histiyositlerin hücre zarlarının birbirine kaynaşması (füzyon) sonucu oluşurlar. Granülom tanısı için esas olan epiteloid histiyosit kümesidir; dev hücre şart değildir."
        }
    },

    # SLIDE 17
    {
        "slideNumber": 17,
        "title": "Dev Hücre Tipleri ve Morfolojik Ayrımı",
        "subtitle": "Langhans, Yabancı Cisim ve Touton Dev Hücrelerinin Diagnostik İmzaları",
        "content": (
            "Patoloji laboratuvarında mikroskop başına geçtiğinizde dev hücrelerin nükleus yerleşim paternine bakarak "
            "etiyoloji hakkında son derece kritik öngörülerde bulunabilirsiniz. Tıbbi patolojide granülomatöz reaksiyonlarda "
            "karşılaştığımız üç ana klasik dev hücre tipi mevcuttur: Langhans dev hücresi, Yabancı cisim dev hücresi ve "
            "Touton dev hücresi. Bu hücrelerin ayrımı kurul ve uzmanlık sınavlarının vazgeçilmez sorularındandır.\n\n"
            "İlki ve en meşhuru 'Langhans Tipi Dev Hücre'dir (Langerhans hücresiyle karıştırılmamalıdır!). Langhans dev hücresinde "
            "onlarca nükleus sitoplazmanın periferine (kenarlarına) göç etmiştir. Nükleuslar kenarda dizilerek tipik bir 'at nalı' "
            "(horseshoe), yarım ay (hilal) veya tam bir dairesel taç konfigürasyonu oluştururlar. Hücrenin sitoplazmik merkezi ise "
            "boş, nükleussuz ve granüler pembe renkte kalır. Bu dizilim tüberküloz ve sarkoidoz gibi immün granülomlar için son derece "
            "karakteristiktir.\n\n"
            "İkincisi 'Yabancı Cisim Tipi Dev Hücre'dir. Burada nükleuslar periferik bir düzen sergilemez; sitoplazmanın her tarafına "
            "rastgele, düzensiz ve dağınık şekilde serpiştirilmiştir. Sitoplazmanın ortasında kümelenebilir veya karmakarışık yayılabilirler. "
            "Sütür iplikleri, talk pudrası, cerrahi gazlı bez artıkları ve silika gibi yabancı materyallerin çevresinde tipiktir.\n\n"
            "Üçüncüsü ise lipid yüklü dokularda gördüğümüz 'Touton Dev Hücresi'dir. Touton dev hücresinde nükleuslar hücre merkezinde "
            "birbirine yakın dairesel bir halka oluşturur. Bu halkanın dışında kalan periferik sitoplazma ise yoğun lipid birikiminden "
            "ötürü köpüksü, vakuollü ve tamamen berrak (şeffaf) bir hale gelmiştir. Ksantomlarda, jüvenil ksantogranülomda ve yağ "
            "nekrozu zemininde gelişen granülomlarda Touton hücreleri patognomonik bir güzellik sergiler."
        ),
        "synthesisNarrative": (
            "Dev hücre tipleri nükleus dağılımıyla ayrılır: Langhans periferik at nalı/hilal dizilimli (tüberküloz); "
            "Yabancı cisim dağınık/düzensiz yerleşimli; Touton ise santral nükleus halkası etrafında berrak lipid sitoplazmalıdır."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Langhans dev hücresi (periferik at nalı nükleus) ile derideki antijen sunucu dendritik hücre olan Langerhans hücresi asla karıştırılmamalıdır; isim benzerliği tamamen tesadüfidir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Santral nükleus halkası etrafında lipid yüklü vakuollü berrak sitoplazma halkası içeren dev hücre 'Touton dev hücresi'dir (ksantogranülom/ksantomlarda izlenir).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Langhans dev hücresi at nalı / hilal nükleer dizilimiyle immün granülomları simgeler.",
            "Yabancı cisim dev hücresinde nükleuslar sitoplazmaya rastgele dağılmıştır.",
            "Touton hücresi lipid metabolizması bozukluklarında ve ksantomlarda görülür."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-017",
            "question": "Deri lezyonu biyopsisinde; merkezde nükleusların oluşturduğu bir çember ve bu çemberin periferinde lipid vakuolleri nedeniyle soluk-berrak görünen sitoplazma halkası içeren çok çekirdekli dev hücre aşağıdakilerden hangisidir?",
            "options": [
                "A) Langhans dev hücresi",
                "B) Yabancı cisim dev hücresi",
                "C) Touton dev hücresi",
                "D) Aschoff dev hücresi",
                "E) Reed-Sternberg hücresi"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Touton dev hücresi, santralde yerleşmiş nükleus halkası ve bunun çevresini saran köpüksü, berrak, lipid yüklü sitoplazma kuşağı ile karakterizedir. Ksantomlar ve jüvenil ksantogranülom için tipiktir. Langhans hücresinde nükleuslar periferik at nalı şeklinde dizilir."
        }
    },

    # SLIDE 18
    {
        "slideNumber": 18,
        "title": "Kazeifiye vs Non-Kazeifiye Granülom Ayrımı",
        "subtitle": "Santral Nekrozun Varlığı, Moleküler Nedenleri ve Diagnostik Algoritma",
        "content": (
            "Patoloji pratiğinde bir granülomla karşılaştığımızda sorduğumuz ilk ve en hayati soru şudur: "
            "'Bu granülomun merkezinde nekroz var mı, yok mu?' Bu iki kelimelik soru, hastanın tanı haritasını iki tamamen "
            "farklı patikaya ayırır: Kazeifiye (nekrotizan) granülomlar ve Non-kazeifiye (non-nekrotizan) granülomlar.\n\n"
            "Kazeifiye granülomun merkezinde mikroskobik olarak hücresel sınırların tamamen silindiği, nükleusların parçalandığı "
            "(karyoreksis), amorf, asellüler, granüler ve eozinofilik (pembe) bir nekroz alanı yer alır. Makroskopik olarak taze "
            "kesitte bu alan sarımsı-beyaz, yumuşak, ufalanabilen kuru çökelek ya da beyaz peynir kıvamındadır; bu nedenle 'kazeöz' "
            "(peynirimsi) nekroz adını almıştır. Kazeifikasyon nekrozu tesadüfen oluşmaz; T hücrelerinin (Th1) salgıladığı aşırı miktardaki "
            "TNF-alfa, makrofajların ürettiği reaktif oksijen ve nitrojen ürünleri, lizozomal hidrolazlar ve lokal iskemi nedeniyle "
            "hücrelerin kütlesel olarak sindirilip mumyalaşmasıyla meydana gelir. Kazeifiye granülom aksi kanıtlanana kadar enfeksiyöz "
            "bir etkeni (başta tüberküloz olmak üzere, mantarlar veya sifilis) düşündürür.\n\n"
            "Non-kazeifiye granülomlarda ise granülomun merkezinde hiçbir nekrotik erime odağı bulunmaz. Lezyon baştan sona canlı, "
            "sağlıklı epiteloid histiyositlerin oluşturduğu homojen solid bir nodüldür. Hücrelerin çekirdekleri canlılığını korur, "
            "amorf pembe bir debris tabakası izlenmez. Non-kazeifiye granülomlar klinik olarak sıklıkla sarkoidoz, Crohn hastalığı, "
            "berilyozis ve yabancı cisim reaksiyonlarında karşımıza çıkar. Ancak altın bir patoloji kuralını unutmamak gerekir: Erken "
            "evredeki bir tüberküloz granülomu henüz nekroz geliştirmemiş olabilir veya bağışıklığı baskılanmış bir hastada nekroz "
            "atipik seyredebilir; bu yüzden her non-kazeifiye granülomda da özel mikrobiyolojik boyalar mutlaka çalışılmalıdır."
        ),
        "synthesisNarrative": (
            "Granülomlar santral nekroza göre ikiye ayrılır: Kazeifiye granülomlar (tüberküloz, mantar) amorf eozinofilik debris içerir; "
            "non-kazeifiye granülomlar (sarkoidoz, Crohn) ise nekrozsuz, tamamen solid epiteloid hücre kümeleridir."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Kazeifikasyon nekrozu amorf, yapısız, asellüler eozinofilik granüler birikimle karakterizedir. Varlığı kural olarak enfeksiyöz etiyolojiyi (özellikle mikobakteri veya mantar) işaret eder.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Histopatolojik olarak santralinde peynirimsi amorf debris (kazeöz nekroz) İÇERMEYEN, solid epiteloid histiyosit kümeleriyle karakterize non-kazeifiye granülomların prototipi Sarkoidoz'dur.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Kazeifikasyon nekrozunun makroskopik karşılığı kuru beyaz peynir kıvamıdır.",
            "Non-kazeifiye granülomlarda tüm hücreler canlı olup nekrotik tabaka yoktur.",
            "Her granülomda etkeni ekarte etmek için özel boyalar (EZN, GMS) yapılmalıdır."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-018",
            "question": "Aşağıdaki hastalıklardan hangisinin karakteristik histopatolojik lezyonu 'santral kazeifikasyon nekrozu içeren kazeifiye granülom' tablosudur?",
            "options": [
                "A) Sarkoidoz",
                "B) Crohn hastalığı",
                "C) Mycobacterium tuberculosis enfeksiyonu",
                "D) Berilyum maruziyeti (Berilyozis)",
                "E) Silikon implant rüptürüne bağlı yabancı cisim reaksiyonu"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Mycobacterium tuberculosis enfeksiyonu kazeifiye granülomların (tüberküllerin) klasik prototipidir; merkezinde amorf granüler peynir benzeri kazeöz nekroz bulunur. Sarkoidoz, Crohn hastalığı, berilyozis ve yabancı cisim reaksiyonları ise tipik olarak non-kazeifiye (nekrozsuz) granülomlar oluşturur."
        }
    },

    # SLIDE 19
    {
        "slideNumber": 19,
        "title": "Tüberküloz Granülomu (Tüberkül)",
        "subtitle": "Mycobacterium tuberculosis, Kazeöz Nekroz, Langhans Hücreleri ve Ghon Odağı",
        "content": (
            "Granülomatöz enflamasyonun dünyadaki en yaygın, en ölümcül ve patolojide en detaylı tanımlanmış prototipi "
            "Tüberküloz'dur. Mycobacterium tuberculosis, kalın ve mumsu mikolik asit zengini hücre duvarı sayesinde makrofajın "
            "fagolizozom birleşmesini engeller. Makrofaj içinde çoğalan basiller, güçlü bir gecikmiş tip aşırı duyarlılık (Tip IV) "
            "reaksiyonunu tetikler. Yaklaşık 2-3 hafta sonra gelişen bu hücresel immün yanıt sonucunda klasik 'Tüberkül' (tüberküloz "
            "granülomu) teşekkül eder.\n\n"
            "Mikroskop altında tüberküloz granülomunun anatomisi bir hedef tahtasını andırır: En merkezde yapısal detayı tamamen "
            "kaybolmuş, nükleer tozlar içeren amorf, asellüler, granüler eozinofilik kazeöz nekroz alanı yer alır. Bu nekrotik çekirdeğin "
            "hemen etrafında, ışınsal olarak dizilmiş epiteloid histiyositler ve aralarına serpiştirilmiş at nalı nükleuslu 'Langhans tipi "
            "dev hücreler' bulunur. Bu kuşağın da dışını, yangı alanını çevreleyen yoğun bir CD4+ T lenfosit halkası (lenfositik manson) "
            "kuşatır. En dışta ise granülomu sınırlamaya çalışan fibroblastlar ve yeni sentezlenmiş kollajen lifler yer alır.\n\n"
            "Primer tüberkülozda basillerin akciğerde ilk yerleştiği subplevral odakta (genellikle alt lob üstü veya üst lob altı) oluşan "
            "granülom odakcığına 'Ghon Odağı' denir. Ghon odağındaki basiller lenfatiklerle drene olan hiler lenf noduna taşınır ve orada da "
            "kazeifiye granülomlar oluşturur. Akciğer parankimindeki Ghon odağı ile drene eden kazeifiye hiler lenf nodunun oluşturduğu bu "
            "çifte lezyona 'Ghon Kompleksi' adı verilir. Ghon kompleksi zamanla kalsifiye ve fibrotik hale geldiğinde radyolojide 'Ranke "
            "Kompleksi' olarak adlandırılır. Kesin tanı için mikroskopta Ziehl-Neelsen (EZN) boyası ile kırmızı, parlak, ince 'Aside Dirençli "
            "Basiller' (ARB) aranmalıdır."
        ),
        "synthesisNarrative": (
            "Tüberküloz granülomu; merkezde kazeöz nekroz, etrafında epiteloid histiyositler, Langhans dev hücreleri ve periferik "
            "lenfosit kuşağından oluşur; akciğer Ghon odağı ve kazeifiye hiler lenf nodu birleşerek Ghon kompleksini oluşturur."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Ghon kompleksi = Akciğer parankimindeki subplevral Ghon odağı + Drene eden kazeifiye hiler lenf nodu. Bu lezyonun fibrokalsifiye olması Ranke kompleksi adını alır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Tüberküloz granülomunda Mycobacterium tuberculosis basillerini göstermek için kullanılan özel histokimyasal boya Ziehl-Neelsen (Ehrlich-Ziehl-Neelsen / EZN) aside dirençli basil boyasıdır.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Tüberkül merkezinde kazeöz nekroz, çevresinde Langhans dev hücreleri bulunur.",
            "Mikolik asit tabakası basillerin fagositer sindirime direnmesini sağlar.",
            "EZN boyasında basiller mavi zemin üzerinde parlak kırmızı çomaklar şeklinde parlar."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-019",
            "question": "Primer pulmoner tüberküloz patolojisinde; akciğer parankiminde subplevral yerleşimli kazeifiye granülom odağı ile buna eşlik eden kazeifiye hiler lenfadenopatinin oluşturduğu anatomik lezyon kompleksi aşağıdakilerden hangisidir?",
            "options": [
                "A) Aschoff nodülü",
                "B) Ghon kompleksi",
                "C) Charcot-Leyden kristali",
                "D) Gamna-Gandy cisimciği",
                "E) Councilman cisimciği"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Primer tüberkülozda akciğer parankimindeki kazeifiye lezyon (Ghon odağı) ile drene eden hiler lenf nodundaki kazeifiye granülomun birlikteliğine 'Ghon kompleksi' adı verilir. İlerleyen dönemde kalsifiye olduğunda Ranke kompleksi adını alır."
        }
    },

    # SLIDE 20
    {
        "slideNumber": 20,
        "title": "Treponema pallidum ve Sifilitik Gom (Gumma)",
        "subtitle": "Tersiyer Sifilis, Koagülatif Gom Nekrozu, Endarteritis Obliterans ve Plazma Hücreleri",
        "content": (
            "Granülomatöz enflamasyonun tıp tarihindeki en dramatik enfeksiyöz nedenlerinden biri Treponema pallidum "
            "tarafından oluşturulan Sifilis (Frengi) hastalığıdır. Primer sifilisteki sert şankr ve sekonder sifilisteki yaygın "
            "makülopapüler döküntülerin ardından, yıllar sonra hastalığın üçüncü evresinde (Tersiyer Sifilis) ortaya çıkan "
            "karakteristik granülomatöz lezyona 'Gom' (Gumma) adı verilir.\n\n"
            "Gom lezyonu karaciğer, kemik, deri, testis ve damar duvarı dahil hemen her organda gelişebilen, tümör benzeri destrüktif "
            "bir kitle tablosudur. Mikroskop altında gomun merkezinde bir nekroz alanı yer alır; ancak bu nekroz tüberkülozun "
            "kazeöz nekrozundan belirgin bir nüansla ayrılır. Gom nekrozunda doku nekroze olmuştur fakat hücrelerin hayalet konturları "
            "ve dokunun kaba silüeti tam olarak erimemiştir; yani koagülasyon nekrozuna çok daha yakın, kauçuksu (elastik ve sakızımsı) "
            "bir kıvam sergiler.\n\n"
            "Gom lezyonunun ve sifilis patolojisinin iki tartışmasız alametifarikası vardır. Birincisi: Nekroz alanının etrafında yer alan "
            "hücresel infiltratta inanılmaz derecede yoğun ve baskın Plazma Hücreleri mevcuttur. Doku adeta plazma hücresi deniziyle "
            "kaplıdır. İkincisi ve en diagnostik vasküler lezyon ise 'Endarteritis Obliterans'tır. Treponema pallidum küçük arter ve "
            "arteriyollerin duvarına özel bir tropizm gösterir. Damar endotel hücreleri prolifere olur, adventisyada yoğun plazma hücreleri "
            "ve lenfositler birikir (periarterit), intima tabakası konsantrik olarak kalınlaşır ve damar lümeni tıkanır (soğan zarı manzarası). "
            "Lümenin tıkanmasıyla dokuda derin bir iskemi oluşur; gom lezyonunun merkezindeki nekrozun oluşumunda da bu iskemik "
            "obliterasyon başrolü oynar."
        ),
        "synthesisNarrative": (
            "Tersiyer sifilisin granülomatöz lezyonu olan Gom (Gumma); kauçuksu gom nekrozu, masif plazma hücresi infiltrasyonu "
            "ve damar lümenini tıkayan karakteristik endarteritis obliterans ile tanımlanır."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Sifilis patolojisinde nereye bakarsanız bakın iki değişmez histopatolojik imza bulursunuz: Yoğun plazma hücresi infiltrasyonu ve perivasküler 'Endarteritis Obliterans'.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Tersiyer sifiliste görülen kauçuksu gom nekrozu, yoğun plazma hücre infiltrasyonu ve konsantrik intimal kalınlaşmayla seyreden endarteritis obliterans lezyonudur.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Gom lezyonunun nekrozu kazeöz nekroza göre hücre konturlarını daha çok korur.",
            "T. pallidum vazo vazorumları tutarak assendan aort anevrizmasına (sifilitik aortit) yol açar.",
            "Gümüşleme boyalarında (Warthin-Starry) spiroketler tirbüşon şeklinde izlenebilir."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-020",
            "question": "Karaciğerde kitle lezyonu nedeniyle opere edilen hastanın biyopsisinde; santralde lastik kıvamlı nekroz, çevresinde bol miktarda plazma hücresi infiltrasyonu ve küçük arterlerde endarteritis obliterans saptanmıştır. Bu tablo için en olası tanı aşağıdakilerden hangisidir?",
            "options": [
                "A) Tüberküloz tüberkülü",
                "B) Tersiyer sifilis gom lezyonu",
                "C) Sarkoidoz nodülü",
                "D) Kedi tırmığı hastalığı",
                "E) Eozinofilik granülom"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Lastik/kauçuksu kıvamda nekroz (gom nekrozu), lezyon çevresinde belirgin plazma hücresi hakimiyeti ve damar lümenlerini tıkayan endarteritis obliterans, Treponema pallidum'un neden olduğu tersiyer sifilis gom (gumma) lezyonunun klasik triadıdır."
        }
    },

    # SLIDE 21
    {
        "slideNumber": 21,
        "title": "Kedi Tırmığı Hastalığı ve Nekrotizan Granülomlar",
        "subtitle": "Bartonella henselae, Stellat Mikroapseler ve Mantar Granülomları",
        "content": (
            "Granülomatöz enflamasyonun çok ilginç ve akut enflamasyonla köprü kuran bir diğer enfeksiyöz yüzü "
            "'Süpüratif (Nekrotizan) Granülomlar'dır. Normalde granülom mononükleer hücrelerden oluşur; fakat bazı özel patojenler "
            "öyle bir hücresel yanıt kışkırtır ki, granülomun merkezinde masif nötrofil birikimiyle karakterize mikroapseler meydana gelir. "
            "Bu tablonun en prototipik örneği 'Kedi Tırmığı Hastalığı'dır (Cat-scratch disease).\n\n"
            "Etken gram-negatif, pleomorfik bir basil olan Bartonella henselae'dir. Genellikle bir kedi tırmalaması veya ısırması sonrasında "
            "bölgesel lenf nodlarında (aksiller veya servikal) ağrılı lenfadenopati gelişir. Lenf nodunun histopatolojisinde zaman içinde "
            "büyüleyici bir morfolojik evrim izlenir: Erken evrede non-spesifik mononükleer foliküler hiperplazi varken, günler içinde "
            "merkezinde yoğun nekrotik nötrofillerin toplandığı yıldızsı, düzensiz şekilli mikroapseler belirir. Bu apselerin çevresinde "
            "palizatlanma gösteren epiteloid histiyositler dizilir ve 'Yıldızsı / Stellat Nekrotizan Granülom' manzarası oluşur. "
            "Bu lezyonlarda çok çekirdekli dev hücreler genellikle nadirdir. Bakteriler Warthin-Starry gümüşleme boyası ile gösterilebilir.\n\n"
            "Benzer süpüratif ve nekrotizan granülomlar derin mikozlarda da (mantar enfeksiyonları) karşımıza çıkar. Örneğin "
            "Histoplasma capsulatum, Coccidioides immitis ve Blastomyces dermatitidis enfeksiyonlarında kazeifiye veya süpüratif "
            "granülomlar oluşur. Histoplazmoziste makrofaj sitoplazmalarında küçük mayalar görülürken; koksidioidomikoziste içinde "
            "endosporlar bulunan iri sferüller granülomların merkezinde yer alır. Tularemi (Francisella tularensis) ve Lenfogranüloma "
            "venereum (Chlamydia trachomatis) da lenf nodlarında benzer stellat nekrotizan süpüratif granülomlara yol açar."
        ),
        "synthesisNarrative": (
            "Kedi tırmığı hastalığı (Bartonella henselae); merkezinde nötrofillerden zengin mikroapse, çevresinde epiteloid histiyositler "
            "bulunan yıldızsı (stellat) nekrotizan granülomlarla seyreder; benzer lezyonlar mantarlarda ve tularemide de görülür."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Kedi tırmığı hastalığında (Bartonella henselae) lenf nodunda merkezinde nötrofil infiltrasyonu (mikroapse) içeren 'yıldızsı / stellat nekrotizan granülomlar' patognomoniktir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Kedi tırmalaması sonrası aksiller lenf nodu biyopsisinde merkezinde nötrofillerin oluşturduğu mikroapse ve periferinde epiteloid histiyosit palizadı içeren yıldızsı granülom Bartonella henselae enfeksiyonudur.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Stellat nekroz nötrofilik süpürasyon ile granülomun birleşimidir.",
            "Warthin-Starry gümüş boyası Bartonella basillerini görünür kılar.",
            "Tularemi ve LGV de benzer süpüratif granülomatöz lenfadenit yapar."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-021",
            "question": "Genç bir hastanın kolunda kedi tırmalaması sonrası gelişen aksiller lenfadenopati biyopsisinde; merkezinde nötrofil lökosit birikimi içeren mikroapseler ve çevresinde epiteloid histiyositlerden oluşan yıldızsı (stellat) nekrotizan granülomlar izlenmiştir. En olası etken mikroorganizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Mycobacterium leprae",
                "B) Treponema pallidum",
                "C) Bartonella henselae",
                "D) Leishmania donovani",
                "E) Toxoplasma gondii"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Kedi tırmığı hastalığı (Bartonella henselae), lenf nodlarında merkezinde nötrofil lökositlerin oluşturduğu apseler ve periferinde epiteloid histiyosit kuşakları bulunan 'yıldızsı / stellat süpüratif nekrotizan granülomlar' ile karakterizedir."
        }
    },

    # SLIDE 22
    {
        "slideNumber": 22,
        "title": "Non-Kazeifiye Granülomların Baş Tacı: Sarkoidoz",
        "subtitle": "Çıplak Granülomlar, Schaumann Cisimcikleri ve Asteroid İnklüzyonları",
        "content": (
            "Non-kazeifiye (nekrozsuz) granülomatöz hastalıkların tartışmasız en önemli klinik temsilcisi ve tıbbi sınavların "
            "en sevilen patolojisi 'Sarkoidoz'dur. Sarkoidoz etiyolojisi tam olarak aydınlatılamamış, genetik yatkınlığı olan bireylerde "
            "çevresel antijenlere karşı gelişen kontrolsüz CD4+ Th1 hücre yanıtıyla karakterize, sistemik bir hastalıktır. Olguların "
            "%90'ından fazlasında akciğer parankimi ve hiler/mediastinal lenf nodları iki taraflı olarak (bilateral hiler lenfadenopati) tutulur.\n\n"
            "Sarkoidozun histopatolojisi mikroskopta adeta bir sanat eseri gibidir ve tüberkülozdan çok keskin sınırlarla ayrılır. "
            "En temel özelliği: Granülomların merkezinde KESİNLİKLE kazeifikasyon nekrozu bulunmaz; granülomlar sıkı, derli toplu, solid "
            "epiteloid histiyosit adacıkları şeklindedir. İkinci ve çok diagnostik bir özellik 'Çıplak Granülom' (naked granuloma) "
            "kavramıdır. Tüberkülozda granülomun çevresinde çok kalın ve yoğun bir T lenfosit kuşağı (manson) bulunurken; sarkoidoz "
            "granülomlarının etrafında lenfositik kuşak ya hiç yoktur ya da son derece incedir. Granülomlar bağ dokusu içinde adeta çıplak "
            "şekilde tek tek veya kümelenerek dururlar.\n\n"
            "Sarkoidoz granülomlarındaki Langhans dev hücrelerinin sitoplazmasında iki karakteristik inklüzyon cisimciği izlenir: "
            "1. 'Schaumann Cisimcikleri': Konsantrik lamelli, kalsiyum ve proteinden zengin, bazofilik kabuksu birikintilerdir. "
            "2. 'Asteroid Cisimcikleri': Sitoplazma içinde yıldız şeklinde, ışınsal kollar uzatan eozinofilik inklüzyonlardır (sitoiskelet "
            "proteinlerinden oluşur). Bu cisimcikler sarkoidoza spesifik olmasa da tanıyı kuvvetle destekler. Epiteloid histiyositlerin "
            "1-alfa hidroksilaz enzimi salgılaması nedeniyle D vitamini aktivasyonu artar ve hastalarda hiperkalsemi/hiperkalsiüri "
            "gelişebilir; ayrıca granülomların sekresyonuna bağlı serum ACE (Anjiyotensin Dönüştürücü Enzim) düzeyleri fırlar."
        ),
        "synthesisNarrative": (
            "Sarkoidoz, bilateral hiler LAP yapan sistemik bir tablodur; histolojisinde nekrozsuz, çevre lenfosit kuşağı zayıf "
            "'çıplak granülomlar', dev hücrelerde Schaumann ve Asteroid cisimcikleri izlenir; ACE ve kalsiyum yüksekliği eşlik eder."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Sarkoidoz granülomları non-kazeifiyedir ve etraflarında yoğun lenfosit kuşağı bulunmadığı için 'Çıplak Granülom' (Naked Granuloma) olarak tanımlanır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Sarkoidoz dev hücreleri içinde izlenen konsantrik kalsiyum-protein lamellerine 'Schaumann cisimciği', yıldızsı sitoplazmik inklüzyonlara ise 'Asteroid cisimciği' denir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Bilateral hiler lenfadenopati ve intertisyel akciğer tutulumu çok tipiktir.",
            "Epiteloid histiyositlerdeki 1-alfa hidroksilaz hiperkalsemiye yol açabilir.",
            "Kazeifikasyon nekrozu olmaması tüberkülozdan ayrımda ilk basamaktır."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-022",
            "question": "Genç kadın hastada akciğer grafisinde bilateral hiler lenfadenopati saptanıyor. Transbronşiyal akciğer biyopsisinde santral nekroz içermeyen, çevresinde belirgin lenfosit halkası bulunmayan (çıplak granülom), dev hücrelerinde Schaumann ve asteroid cisimcikleri içeren granülomlar görülüyor. Bu hasta için en olası tanı aşağıdakilerden hangisidir?",
            "options": [
                "A) Primer Tüberküloz",
                "B) Sarkoidoz",
                "C) Silikozis",
                "D) Kedi Tırmığı Hastalığı",
                "E) Romatoid Nodül"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Bilateral hiler lenfadenopati, nekroz içermeyen 'çıplak' non-kazeifiye granülomlar ve dev hücrelerde konsantrik Schaumann cisimcikleri ile yıldızsı Asteroid cisimciklerinin varlığı Sarkoidoz için klasik histopatolojik bulgulardır."
        }
    },

    # SLIDE 23
    {
        "slideNumber": 23,
        "title": "Gastrointestinal Granülomlar ve Crohn Hastalığı",
        "subtitle": "Transmural Enflamasyon, Atlamalı Tutulum ve Non-Kazeifiye Granülomlar",
        "content": (
            "Gastrointestinal sistem granülomatöz reaksiyonların en sık görüldüğü organ sistemlerinden biridir ve burada "
            "patoloğun karşısına çıkan en büyük klinik düğüm, iki İnflamatuar Barsak Hastalığı (İBH) olan Crohn Hastalığı "
            "ile Ülseratif Kolit'in (ÜK) ayrımıdır. Bu ayrımda granülom varlığı altın değerinde bir diagnostik anahtardır.\n\n"
            "Crohn hastalığı ağızdan anüse kadar sindirim kanalının herhangi bir segmentini tutabilen, ancak en sık terminal ileum "
            "ve çekumu hedef alan kronik granülomatöz bir hastalıktır. Ülseratif kolitin aksine Crohn'da lezyonlar kesintisiz değildir; "
            "sağlıklı mukoza adacıklarıyla ayrılmış lezyonlu alanlar şeklinde 'atlamalı tutulum' (skip lesions) gösterir. En kritik "
            "patolojik fark ise tutulumun derinliğindedir: Ülseratif kolit sadece mukoza ve submukozayla sınırlı yüzeyel bir yangı "
            "yaparken, Crohn hastalığı bağırsak duvarının tüm katmanlarını (mukoza, submukoza, muskularis propria ve subserroza) "
            "tutan 'Transmural' bir enflamasyondur.\n\n"
            "Crohn hastalarının yaklaşık %50-60'ında bağırsak duvarının herhangi bir katmanında veya drene eden mezenterik lenf "
            "nodlarında 'Non-Kazeifiye Granülomlar' saptanır. Bu granülomlar gevşek, küçük epiteloid histiyosit kümeleri şeklindedir ve "
            "kazeifikasyon nekrozu kesinlikle içermezler. Transmural tutulum ve granülomatöz reaksiyon, bağırsak duvarında derin çatlak "
            "şeklinde ülserlere (fissürler), bağırsak kıvrımlarının birbirine veya deriye yapışarak fistül oluşturmasına ve lümenin "
            "fibrozisle daralarak tıkanmasına (darlık / striktür) zemin hazırlar. Biyopside non-kazeifiye granülom görülmesi, Ülseratif "
            "Koliti kesin olarak ekarte ettirir ve ibreyi doğrudan Crohn lehine çevirir."
        ),
        "synthesisNarrative": (
            "Crohn hastalığı sindirim kanalında atlamalı ve transmural (tüm katları tutan) tutulumla seyreder; bağırsak duvarında "
            "ve mezenterik lenf nodlarında saptanan non-kazeifiye granülomlar, onu Ülseratif Kolit'ten ayıran temel patolojik bulgudur."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: İnflamatuar barsak hastalıklarında granülom saptanması Ülseratif Kolit'i kesin olarak ekarte ettirir; non-kazeifiye granülomlar Crohn hastalığının karakteristik ayırt edici bulgusudur.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Gastrointestinal kanalda transmural enflamasyon, atlamalı (skip) lezyonlar, fissürler ve non-kazeifiye granülomlarla karakterize hastalık Crohn Hastalığı'dır.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Crohn hastalığında tutulum transmural olup tüm bağırsak duvarını kat eder.",
            "Non-kazeifiye granülomlar mukoza, submukoza ve subserozada bulunabilir.",
            "Ülseratif kolitte granülom izlenmez; yangı mukoza-submukozayla sınırlıdır."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-023",
            "question": "Kronik ishal ve karın ağrısı olan hastanın terminal ileum rezeksiyon materyalinde; atlamalı (skip) lezyonlar, bağırsak duvarının tüm katlarını tutan transmural mononükleer infiltrasyon, fissür tarzı derin ülserler ve submukozada non-kazeifiye granülomlar izleniyor. Bu hasta için en olası patolojik tanı nedir?",
            "options": [
                "A) Ülseratif Kolit",
                "B) Crohn Hastalığı",
                "C) İskemik Kolit",
                "D) Psödomembranöz Enterokolit",
                "E) Çölyak Hastalığı"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Transmural tutulum (bağırsak duvarının tüm katları), atlamalı lezyonlar, fissürler ve histopatolojik olarak non-kazeifiye granülomların saptanması Crohn Hastalığı için patognomoniktir. Ülseratif Kolit sadece mukoza ve submukozayla sınırlıdır ve granülom içermez."
        }
    },

    # SLIDE 24
    {
        "slideNumber": 24,
        "title": "Yabancı Cisim Granülomları ve Kronik Enflamasyonun Sistemik Sonuçları",
        "subtitle": "Polarize Işıkta Birefringens, Fibröz Skarlar, AA Amiloidozu ve Kaşeksi",
        "content": (
            "Dersimizin finalini yaparken granülomatöz reaksiyonların non-immün kolu olan 'Yabancı Cisim Granülomları'na "
            "ve kronik enflamasyonun tüm organizmayı ilgilendiren sistemik faturasına değineceğiz. Yabancı cisim granülomları, "
            "T hücresi aracılı bir immün yanıt olmaksızın, organizmanın antijenik olmayan ancak fagositozla eritilemeyecek kadar iri "
            "materyallere karşı geliştirdiği fiziksel bir kuşatma tepkisidir. Cerrahi sütür iplikleri, talk pudrası partikülleri, "
            "silikon, protez döküntüleri, odun kıymıkları veya intravenöz ilaç bağımlılarında damara enjekte edilen mikrokristaller "
            "bu reaksiyonun başlıca nedenleridir.\n\n"
            "Histopatolojide yabancı cisim granülomunun merkezinde yabancı materyalin kendisi yer alır. Bu materyal genellikle "
            "çok çekirdekli yabancı cisim dev hücrelerinin sitoplazması içinde hapsolmuş veya bu hücrelerle çevrelenmiştir. Patoloğun "
            "en büyük teşhis yardımcısı 'Polarize Işık Mikroskobu'dur. Polarize ışık altında talk, silika ve sütür iplikleri ışığı "
            "iki farklı kırma indisine ayırarak karanlık zemin üzerinde elmas gibi parlar (birefringens / çift kırıcılık gösterirler).\n\n"
            "Haftalarca veya aylarca süren kronik enflamasyon sadece lokal dokuyu tahrip etmekle kalmaz; tüm vücudu saran üç ölümcül "
            "sistemik komplikasyon doğurur: 1. 'Organ Fibrozisi': M2 makrofajlarından salınan kontrolsüz TGF-β parankimi yok ederek "
            "karaciğer sirozu, son dönem böbrek yetmezliği veya fibrotik balpeteği akciğere yol açar. 2. 'Sistemik Sekonder (AA) Amiloidoz': "
            "Kronik enflamasyonda IL-1 ve IL-6 etkisiyle karaciğerden sentezlenen Serum Amiloid A (SAA) proteini kanda tavan yapar; "
            "bu protein kırılarak böbrek ve dalakta amiloid fibrilleri halinde çöker ve nefrotik sendrom yaratır. 3. 'Kaşeksi': Makrofajlarca "
            "sürekli üretilen TNF-alfa (eski adıyla kaşektin), beyinde iştah merkezini baskılar, lipoprotein lipazı inhibe ederek periferik "
            "yağ ve kas kütlesini eritir; hastada derin bir tükenmişlik ve aşırı kilo kaybı (kaşeksi) tablosu oluşturur."
        ),
        "synthesisNarrative": (
            "Yabancı cisim granülomlarında polarize ışıkta parlayan partiküller yabancı cisim dev hücrelerince sarılır; "
            "kronik enflamasyonun sistemik sonuçları ise organ fibrozisi, sekonder (AA) amiloidoz ve TNF kaynaklı kaşeksidir."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Polarize ışık mikroskobunda yabancı cisim granülomlarındaki talk, silika veya dikiş iplikleri çift kırıcılık (birefringens) göstererek parlak ışık yansıtmasıyla kesin olarak ayırt edilir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Uzamış kronik enflamasyon zemininde karaciğerden IL-6/IL-1 uyarısıyla aşırı sentezlenen Serum Amiloid A (SAA) proteininin dokularda çökmesi Sekonder (AA) Amiloidoz'a yol açar.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Polarize mikroskopta parlayan materyal yabancı cisim granülomunu doğrular.",
            "TNF-alfa (kaşektin) iştahı kesip yağları yıkarak kronik kaşeksiye sebep olur.",
            "Kronik enflamasyonun nihai yapısal sonucu TGF-β güdümlü doku fibrozisidir."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-024",
            "question": "Yıllardır kronik granülomatöz tüberküloz veya romatoid artrit tanısıyla takip edilen bir hastada masif proteinüri ve böbrek yetmezliği gelişiyor. Böbrek biyopsisinde glomerüllerde amorf birikim saptanıyor. Bu sistemik tablonun patogenezinde rol oynayan temel protein prekürsörü aşağıdakilerden hangisidir?",
            "options": [
                "A) İmmünglobulin hafif zinciri (AL)",
                "B) Transtiretin (ATTR)",
                "C) Serum Amiloid A (SAA)",
                "D) Beta-2 mikroglobulin",
                "E) Kalsitonin öncül proteini"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Kronik enflamatuvar ve granülomatöz hastalıklarda (tüberküloz, romatoid artrit, bronşektazi vb.) makrofaj ve lökosit kaynaklı sitokinlerin (IL-6, IL-1, TNF) karaciğeri uyarması sonucu üretilen Serum Amiloid A (SAA) proteini artar ve dokularda Sekonder Sistemik (AA) Amiloidozis şeklinde çökerek organ yetmezliğine yol açar."
        }
    }
]
