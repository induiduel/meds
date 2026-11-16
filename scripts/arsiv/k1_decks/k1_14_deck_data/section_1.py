# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-14-s01",
        "title": "Bulaşıcı Hastalıkların Tarihsel Seyri: 1970'lerin İyimserliğinden Günümüze",
        "content": "20. yüzyılın ortalarında penisilinin keşfi, geniş spektrumlu antibiyotiklerin geliştirilmesi ve çiçek aşısı gibi küresel aşılama başarıları tıp dünyasında aşırı bir iyimserlik dalgası yarattı:\n\n- **1970'lerin Yanılgısı:** Birçok bilim insanı ve halk sağlığı otoritesi bulaşıcı hastalıklar kitabının artık kapandığını, insanlığın bundan böyle yalnızca kanser ve kardiyovasküler kronik hastalıklarla mücadele edeceğini ilan etti.\n- **Gerçeklikle Yüzleşme:** Bu iyimserlik kısa sürede çöktü. Mikroorganizmaların antibiyotik direnci geliştirmesi, yeni zoonotik virüslerin ortaya çıkması ve küreselleşme, bulaşıcı hastalıkların 21. yüzyılın en büyük küresel varoluşsal tehdidi olarak kalmaya devam ettiğini gösterdi.\n- **Günümüz Tablosu:** Bulaşıcı hastalıklar tehdidi azalmamış, aksine insanlığın ekolojik dengeleri bozmasıyla çok daha karmaşık ve tehlikeli bir evreye evrilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "1970'lerin İyimserliği vs 21. Yüzyıl Salgın Gerçekliği",
                "1970'lerin Yanılgısı",
                "Antibiyotik ve aşılarla enfeksiyon hastalıklarının tarihe karıştığı kabul ediliyordu.",
                "21. Yüzyıl Gerçekliği",
                "1500'den fazla yeni patojen keşfedildi; pandemiler insanlığın en büyük tehdidi haline geldi."
            ),
            make_cloze(
                "Yirminci yüzyılın ikinci yarısındaki iyimserliğin aksine enfeksiyon etkenleri direnç geliştirerek ve yeni patojenler türeterek küresel tehdit olmayı sürdürmüştür.",
                "yeni patojenler",
                "Son yarım asırda ortaya çıkan bilinmeyen mikroorganizmalar"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-14-s02",
        "title": "Yeni ve Yeniden Ortaya Çıkan Patojenler: 1500'den Fazla Tehdit",
        "content": "1970'lerden günümüze geçen yaklaşık 50 yıllık süreçte tıp bilimi daha önce insanlarda tanımlanmamış **1500'den fazla yeni patojen** keşfetmiştir:\n\n- **HIV/AIDS Örneği:** 1980'lerin başında tanımlanan İnsan İmmün Yetmezlik Virüsü (HIV), bugüne kadar dünya çapında **70 milyondan fazla insanı enfekte etmiş** ve **35 milyondan fazla insanın ölümüne** yol açarak modern çağın en yıkıcı pandemilerinden birine imza atmıştır.\n- **Yeniden Ortaya Çıkanlar (Re-emerging):** Geçmişte kontrol altına alınmış sanılan tüberküloz, sıtma, kızamık ve kolera gibi hastalıklar; aşı tereddütü, ilaç direnci, savaşlar ve yetersiz altyapı nedeniyle yeniden patlama yapmaktadır.\n- **Bilinmeyen 'X Hastalığı':** DSÖ, henüz bilinmeyen ancak küresel bir felakete yol açma potansiyeli olan varsayımsal patojeni 'Disease X' olarak tanımlamaktadır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Patojen Kategorisi", "Tanım ve Karakteristik", "Klasik Örnekler"],
                [
                    [
                        {"text": "Yeni Ortaya Çıkanlar (Emerging)", "isMasked": False, "hint": ""},
                        {"text": "Daha önce insan popülasyonunda bilinmeyen yeni ajanlar", "isMasked": False, "hint": ""},
                        {"text": "HIV, SARS-CoV-1, MERS-CoV, SARS-CoV-2", "isMasked": True, "hint": "Son 40 yılda çıkan yeni koronavirüsler ve retrovirüs"}
                    ],
                    [
                        {"text": "Yeniden Ortaya Çıkanlar (Re-emerging)", "isMasked": True, "hint": "Eski kontrol edilmiş hastalıkların canlanması"},
                        {"text": "Kontrol altındayken direnç veya ihmalle hortlayanlar", "isMasked": False, "hint": ""},
                        {"text": "Çok ilaca dirençli Tüberküloz, Kolera, Kızamık", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Hastalık X (Disease X)", "isMasked": False, "hint": ""},
                        {"text": "Henüz bilinmeyen varsayımsal küresel pandemi patojeni", "isMasked": False, "hint": ""},
                        {"text": "DSÖ öncelikli araştırma listesindeki potansiyel ajan", "isMasked": True, "hint": "Bilinmeyen gelecekteki küresel tehdit kodu"}
                    ]
                ]
            ),
            make_recall(
                "1970'lerden bu yana tıp dünyası tarafından tanımlanan yeni patojen sayısı yaklaşık ne kadardır?",
                "1500'den fazladır (HIV, Ebola, SARS, MERS vb. dahil).",
                "Son yarım asırda keşfedilen mikrop adedi"
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-14-s03",
        "title": "Küreselleşme, Hızlı Ulaşım ve Salgınların Kıtalararası Hızı",
        "content": "Orta Çağ'da Kara Veba'nın İpek Yolu ve ticaret gemileriyle Asya'dan Avrupa'ya yayılması yıllar sürmüştür. 21. yüzyılda ise salgınların dinamiği kökten değişmiştir:\n\n- **Uçak Hızında Salgınlar:** Günümüzde lokal bir köyde veya pazarda ortaya çıkan bir patojen, **kıtalararası bir yolcu uçağının uçabildiği hızla (24 saatten kısa sürede)** dünyanın en uzak metropolüne taşınabilmektedir.\n- **Yolcu Sayısı Hacmi:** Her gün milyonlarca insan kıtalararası uçuş yapmaktadır. Asemptomatik kuluçka dönemindeki bir yolcu, havaalanı taramalarını hiçbir belirti vermeden geçerek virüsü başka bir kıtaya ekebilir.\n- **Şehirleşme ve Yoğunluk:** Plansız mega-kentler, toplu taşıma ve hava sirkülasyonu yetersiz binalar patojenin bir kıtaya ayak bastığı anda katlanarak çoğalmasına (amplifikasyon) kusursuz zemin hazırlar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Tarihsel Salgın Yayılımı vs 21. Yüzyıl Uçak Hızında Salgın",
                "Geçmiş Dönemler (Kervan ve Yelkenli)",
                "Patojenin bir kıtadan diğerine geçmesi aylar veya yıllar sürerdi; gemide hastalananlar yolda ölürdü.",
                "21. Yüzyıl (Jet Havacılığı)",
                "Lokal bir vaka 24 saat içinde dünyanın tüm kıtalarına yayılabilir; inkübasyon süresi uçuş süresinden uzundur."
            ),
            make_cloze(
                "Yirmi birinci yüzyılda lokal salgınların küreselleşme hızı kıtalararası bir yolcu uçağının uçabildiği hız ile aynı seviyeye ulaşmıştır.",
                "yolcu uçağının",
                "Hızlı küresel yayılımı sağlayan modern ulaşım aracı"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-14-s04",
        "title": "2009 H1N1 Pandemisi: 9 Ayda Tüm Dünyayı Sarma Hızı",
        "content": "2009 yılında Meksika ve Amerika Birleşik Devletleri'nde domuz kökenli yeni bir H1N1 influenza A virüsü patlak verdi:\n\n- **Yayılma Hızı Rekoru:** Virüs tespit edildikten sonra **9 aydan daha kısa bir süre içinde dünyanın tüm kıtalarına ve neredeyse tüm ülkelerine** ulaştı.\n- **Pandemi İlanı:** Dünya Sağlık Örgütü (DSÖ), virüsün küresel hızına dayanarak 41 yıl aradan sonra ilk kez en üst seviye olan Faz 6 Pandemi ilan etti.\n- **Çıkarılan Dersler:** Modern ulaşım ağlarının ne kadar entegre olduğu ve solunum yoluyla yayılan bir damlacık patojeninin konvansiyonel sınır kontrolleriyle durdurulmasının imkansıza yakın olduğu tüm dünyaya kanıtlandı.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "2009 H1N1 Pandemisinin Küresel Yayılma Çarkı",
                [
                    "1. Zoonotik Sıçrama: Domuz, kuş ve insan influenza genlerinin reasortmanı ile yeni H1N1 suşu doğdu.",
                    "2. İnsandan İnsana Solunumsal Bulaş: Meksika'da genç yetişkinlerde hızla yayılan pnömoniler başladı.",
                    "3. Havayolu İhracatı: İnkübasyon dönemindeki yolcular virüsü Kuzey Amerika ve Avrupa'ya taşıdı.",
                    "4. 9 Ayda Küresel Kuşatma: 9 ay dolmadan tüm kıtalarda milyonlarca vaka ve DSÖ Pandemi ilanı gerçekleşti."
                ]
            ),
            make_quiz(
                "2009 yılında ortaya çıkan ve modern küresel ulaşım hızı sayesinde 9 aydan kısa sürede dünyanın tüm kıtalarına yayılan pandemi etkeni patojen hangisidir?",
                [
                    {"key": "A", "text": "Pandemik İnfluenza A (H1N1)", "explanation": "A seçeneği DOĞRUDUR: 2009 H1N1 domuz gribi 9 aydan kısa sürede tüm dünyaya yayılan ilk 21. yüzyıl pandemisidir."},
                    {"key": "B", "text": "SARS-CoV-1", "explanation": "B seçeneği yanlıştır: 2003 yılında Asya merkezli sınırlı salgın yaptı."},
                    {"key": "C", "text": "Zika Virüsü", "explanation": "C seçeneği yanlıştır: 2015 yılında Güney Amerika'da yayıldı."},
                    {"key": "D", "text": "Ebola Virüsü", "explanation": "D seçeneği yanlıştır: 2014 Batı Afrika odaklıdır."},
                    {"key": "E", "text": "Vibrio cholerae O139", "explanation": "E seçeneği yanlıştır: Su kaynaklı kolera salgınıdır."}
                ],
                "A"
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-14-s05",
        "title": "Koronavirüs Salgınları: SARS (2003) ve MERS-CoV (2012 / 2015)",
        "content": "21. yüzyılın ilk çeyreği, koronavirüslerin hayvanlardan insanlara sıçrayarak ne denli öldürücü olabileceğinin iki büyük uyarısına sahne oldu:\n\n1. **SARS (Ağır Akut Solunum Sendromu - 2003):**\n   - Çin'in Guangdong bölgesinde misk kedileri ve yarasalardan insana geçti.\n   - Hong Kong'daki bir otelden dünyaya yayıldı; 8000'den fazla insan hastalandı ve 800'e yakın ölüm (%10 mortalite) görüldü.\n2. **MERS-CoV (Ortadoğu Solunum Sendromu - 2012):**\n   - Suudi Arabistan'da tek hörgüçlü develerden insana bulaştı; %35 gibi korkunç bir vaka-ölüm hızına sahiptir.\n   - **2015 Güney Kore Dersi (Sınav Spotu):** Ortadoğu'dan dönen tek bir enfekte iş insanı Seul'e indi; hastane içi süper-bulaştırma zinciriyle **186 vakaya ve 36 ölüme** yol açtı, binlerce kişi karantinaya alındı ve ekonomi sarsıldı!",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "SARS-CoV (2003) vs MERS-CoV (2012) Karşılaştırması",
                "SARS (2003 Salgını)",
                "Misk kedisi/yarasa kaynaklı; %10 mortalite; Hong Kong otelinden hızla dünyaya yayıldı.",
                "MERS (2012 Salgını)",
                "Tek hörgüçlü deve kaynaklı; %35 yüksek mortalite; 2015'te tek yolcuyla Güney Kore'de kriz yarattı."
            ),
            make_cloze(
                "2015 yılında Ortadoğu'dan Güney Kore'ye dönen tek bir enfekte yolcunun hastanelerde süper bulaşmaya yol açması sonucu patlak veren koronavirüs salgını MERS salgınıdır.",
                "MERS",
                "Ortadoğu solunum sendromu virüsü kısaltması"
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-14-s06",
        "title": "Kanamalı Ateşler: 2014 Batı Afrika Ebola Salgını",
        "content": "Filovirüs ailesinden Ebola virüsü, tarihin en korkutucu kanamalı ateş etkenlerinden biridir. 2014 Batı Afrika (Gine, Liberya, Sierra Leone) salgını tarihin en büyük Ebola felaketi oldu:\n\n- **Gecikmiş Farkındalık:** Salgın ormanlık bir köyde başladı ancak zayıf sağlık altyapısı ve sürveyans eksikliği nedeniyle **ilk iki ay boyunca hiçbir hekim ve otorite tarafından teşhis edilemedi!**\n- **Yıkıcı Bilanço:** 28.000'den fazla vaka ve 11.000'den fazla ölüm kaydedildi. Yüzlerce doktor ve hemşire hayatını kaybetti.\n- **Kritik Bulaş Yolu:** Havadan solunumla değil; hastaların kanı, kusmuğu, ishali ve ter gibi enfekte vücut sıvılarıyla doğrudan temasla bulaşır.\n- **Güvenli Defin Krizi:** Geleneksel cenaze yıkama ritüelleri virüsün yayılmasında süper-bulaşma odağı oldu; kültürel inançlara saygılı güvenli defin protokolleri geliştirildi.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Batı Afrika'da ateş, ishal, kusma ve cilt altı kanamaları olan bir hastaya müdahale eden sağlık ekibinde görev alıyorsunuz. Hastanın Ebola virüs enfeksiyonu olduğu doğrulanıyor.",
                "Bu hastanın takibinde ve izolasyonunda personelin ve toplumun korunması için bulaşma dinamiklerine göre en kritik kural nedir?",
                [
                    {
                        "text": "Virüs hava yoluyla değil enfekte vücut sıvılarıyla (kan, dışkı, kusmuk) bulaşır; tam koruyucu KKE ve sıvı izolasyonu şarttır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Ebola aerosol değil temas ve vücut sıvısı kaynaklıdır; en ufak deri/mukoza teması ölümcül enfeksiyon yapar."
                    },
                    {
                        "text": "Yalnızca basit cerrahi maske takılıp normal serviste takip edilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Cerrahi maske vücut sıvısı sıçramasına ve temas bulaşına karşı yetersizdir; tam su geçirmez KKE zorunludur."
                    },
                    {
                        "text": "Hastanın cenazesi geleneksel yöntemlerle yakınlarına teslim edilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Cenaze en bulaşıcı kaynaktır; güvenli ve onurlu defin ekibi tarafından gömülmelidir."
                    }
                ]
            ),
            make_recall(
                "2014 Batı Afrika Ebola salgınında salgının başlangıcında iki ay boyunca tanı konulamamasının altında yatan temel halk sağlığı açığı nedir?",
                "Erken uyarı ve birinci basamak sürveyans sisteminin yetersizliğidir.",
                "Klinisyen düzeyinde vaka tanıma ve bildirim eksikliği"
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-14-s07",
        "title": "Vektör Kaynaklı Yeni Tehditler: 2015 Zika Virüsü ve Mikrosefali",
        "content": "2015 yılında Brezilya'da patlak veren Zika virüsü salgını, vektör kaynaklı arbovirüslerin beklenmedik teratojenik tehlikelerini gözler önüne serdi:\n\n- **Bulaşma Vektörü:** Gündüzleri ısıran **Aedes aegypti** ve **Aedes albopictus** sivrisinekleridir. Ayrıca cinsel yolla ve kan transfüzyonuyla da bulaşabilir.\n- **Klinik ve Teratojenite (Sınav Spotu):** Yetişkinlerde hafif döküntü ve eklem ağrısıyla atlatan hastalık, hamile kadınlara bulaştığında plasentayı aşarak fetal nöral kök hücreleri enfekte etti.\n- **Konjenital Zika Sendromu:** Binlerce bebekte ağır **mikrosefali (küçük baş anomalisi)**, serebral korteks kalsifikasyonu ve körlük gelişti.\n- **Küresel Acil Durum:** DSÖ, mikrosefali patlaması nedeniyle 2016 yılında Uluslararası Öneme Sahip Halk Sağlığı Acil Durumu (PHEIC) ilan etti.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Klasik Arbovirüsler vs Zika Virüsü Klinik Farkı",
                "Klasik Arbovirüsler (Dang, Chikungunya)",
                "Yüksek ateş, şiddetli kas/eklem kırıklığı ve kanama yapar; belirgin teratojenik mikrosefali yapmaz.",
                "Zika Virüsü (2015 Salgını)",
                "Annede çok hafif geçer ancak fetüste kalıcı mikrosefali ve konjenital beyin yıkımı yaratır."
            ),
            make_quiz(
                "2015 yılında Brezilya'da Aedes sivrisinekleriyle yayılarak hamile kadınlarda fetal mikrosefali ve nörogelişimsel defektlere yol açan arbovirüs hangisidir?",
                [
                    {"key": "A", "text": "Zika Virüsü", "explanation": "A seçeneği DOĞRUDUR: Zika virüsü plasentayı aşarak nöral kök hücreleri yıkar ve mikrosefaliye yol açar."},
                    {"key": "B", "text": "Kuduz Virüsü", "explanation": "B seçeneği yanlıştır: Rhabdovirüstür, sivrisinekle bulaşmaz."},
                    {"key": "C", "text": "Hepatit B Virüsü", "explanation": "C seçeneği yanlıştır: Kan ve cinsel yolla bulaşan hepadnavirüstür."},
                    {"key": "D", "text": "Kırım-Kongo Kanamalı Ateşi Virüsü", "explanation": "D seçeneği yanlıştır: Kene kaynaklı nairovirüstür."},
                    {"key": "E", "text": "Poliovirüs", "explanation": "E seçeneği yanlıştır: Fekal-oral bulaşan enterovirüstür."}
                ],
                "A"
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-14-s08",
        "title": "Tarihin Yeniden Uyanan Salgınları: Madagaskar Vebası ve Kolera",
        "content": "Salgın tehditleri yalnızca yepyeni virüslerden ibaret değildir; bin yıllık kadim hastalıklar da fırsat bulduğunda kitlesel ölümlere yol açar:\n\n1. **Madagaskar Veba Salgını (2017):**\n   - Yersinia pestis bakterisi kemirgen pireleriyle bulaşan hıyarcıklı veba yaparken, 2017'de insandan insana damlacıkla bulaşan **pnömonik vebaya** dönüştü.\n   - Kısa sürede 2400'den fazla vaka ve **209 ölüm** kaydedildi.\n2. **Kolera Salgınları (Vibrio cholerae):**\n   - Temiz su ve sanitasyonun çöktüğü savaş ve afet bölgelerinde (Yemen, Haiti, Sahra altı Afrika) her yıl **40'tan fazla büyük kolera salgını** patlak vermektedir.\n   - Pirinç suyu benzeri masif sulu ishal saatler içinde hipovolemik şok ve ölüm yaratır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Kadim Salgın Hastalık", "Etken Ajan", "Temel Bulaş Yolu", "Kritik Klinik Özellik"],
                [
                    [
                        {"text": "Veba (Pnömonik)", "isMasked": False, "hint": ""},
                        {"text": "Yersinia pestis", "isMasked": True, "hint": "Kara ölüm etkeni gram-negatif bakteri"},
                        {"text": "Damlacık / solunum yolu", "isMasked": False, "hint": ""},
                        {"text": "İnsandan insana hızlı ölümcül akciğer enfeksiyonu", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kolera", "isMasked": True, "hint": "Pirinç suyu ishali yapan bakteri hastalığı"},
                        {"text": "Vibrio cholerae", "isMasked": False, "hint": ""},
                        {"text": "Fekal-oral / kontamine su", "isMasked": True, "hint": "Kanalizasyon karışmış içme suları"},
                        {"text": "Masif dehidratasyon ve saatler içinde şok", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "2017 yılında Madagaskar'da 200'den fazla insanın ölümüne yol açan, kemirgen piresi gerektirmeden insandan insana solunum damlacıklarıyla bulaşan veba formu hangisidir?",
                "Pnömonik vebadır (akciğer vebası).",
                "İnsandan insana solunumla geçen en ölümcül veba formu"
            )
        ]
    })

    # Slide 9
    slides.append({
        "id": "k1-14-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] 21. Yüzyıl Salgın Tehditleri ve Küresel Dinamikler",
        "content": "Bu ilk kontrol noktasında modern çağın salgın tehditlerini ve küresel yayılma hızını özetliyoruz:\n\n- **1970 Yanılgısı:** 'Bulaşıcı hastalıklar bitti' iddiası çöktü; 1500'den fazla yeni patojen tanımlandı (HIV tek başına 35 milyon can aldı).\n- **Uçak Hızında Salgın:** Kıtalararası jet uçuşları sayesinde lokal bir odak 24 saatte tüm dünyaya ulaşabilmektedir.\n- **2009 H1N1:** 9 aydan kısa sürede tüm kıtaları sardı ve pandemi ilan edildi.\n- **Koronavirüsler:** SARS-CoV (2003, %10 ölüm) ve MERS-CoV (2012, %35 ölüm; 2015'te tek yolcuyla Güney Kore'de hastane salgını).\n- **Ebola (2014):** 2 ay tanı alamadı; vücut sıvılarıyla bulaşır; 11.000 ölüm.\n- **Zika (2015):** Aedes sivrisineğiyle bulaşan konjenital mikrosefali etkeni.\n- **Tarihin Yeniden Uyanışı:** Madagaskar'da pnömonik veba (2017) ve su kaynaklı kolera salgınları.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "1970'lerden günümüze keşfedilen yeni patojenler ve 21. yüzyıl salgın dinamikleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "21. yüzyılda gelişen modern tıp sayesinde patojenlerin kıtalararası yayılma hızı Orta Çağ'a göre çok daha yavaşlamıştır", "explanation": "A seçeneği DOĞRUDUR (aranan yanlıştır): Modern jet uçakları salgınların yayılma hızını katbekat artırmış, 24 saate indirmiştir."},
                    {"key": "B", "text": "1970'lerden bu yana 1500'den fazla yeni patojen tanımlanmıştır", "explanation": "B seçeneği doğru bir ifadedir."},
                    {"key": "C", "text": "2009 H1N1 pandemisi 9 aydan kısa sürede tüm kıtalara yayılmıştır", "explanation": "C seçeneği doğru bir ifadedir."},
                    {"key": "D", "text": "2014 Batı Afrika Ebola salgınında erken sürveyans yetersizliği nedeniyle ilk iki ay tanı konulamamıştır", "explanation": "D seçeneği doğru bir ifadedir."},
                    {"key": "E", "text": "Zika virüsü gebelikte geçirildiğinde fetal mikrosefaliye yol açabilir", "explanation": "E seçeneği doğru bir ifadedir."}
                ],
                "A"
            ),
            make_cloze(
                "İki bin dokuz yılındaki H1N1 influenza pandemisi küresel hava ulaşımı sayesinde dokuz aydan kısa sürede tüm dünya kıtalarına yayılmıştır.",
                "dokuz aydan",
                "Pandeminin tüm kıtalara ulaşma zamanı"
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-14-s10",
        "title": "Salgın Tehditlerinin Çok Sektörlü ve Ekonomik Maliyeti",
        "content": "Salgınlar asla yalnızca tıbbi bir mesele değildir; toplumun tüm organlarını felç eden sistemik bir depremdir:\n\n- **Sağlık Sisteminin Kilitlenmesi:** Ani hasta akışı hastane yataklarını, yoğun bakımları ve ventilatörleri tüketir. Rutin sağlık hizmetleri (kanser ameliyatları, aşılar, doğumlar) aksar; salgından ölenler kadar aksayan rutin bakımdan ölenler olur (**dolaylı mortalite**).\n- **Ekonomik Yıkım:** Karantinalar, sınırların kapatılması, turizm ve ticaretin durması trilyonlarca dolarlık küresel kayıp yaratır.\n- **Sosyal ve Politik İstikrarsızlık:** Güven kaybı, sokağa çıkma yasakları, panik ve gıda tedarik zincirlerinin kopması hükümetleri ve toplumsal barışı tehdit eder.\n- **Sonuç:** Salgınlara hazırlık yapmak bir masraf kalemi değil, medeniyetin devamı için zorunlu bir güvenlik yatırımıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Doğrudan Salgın Kayıpları vs Dolaylı Sağlık Sistemi Kayıpları",
                "Doğrudan Kayıplar",
                "Patojenin kendisinin yol açtığı enfeksiyon, ağır pnömoni ve doğrudan ölümlerdir.",
                "Dolaylı Kayıplar",
                "Hastanelerin kilitlenmesi sonucu ameliyat olamayan kalp ve kanser hastalarının ölümleridir."
            ),
            make_recall(
                "Salgın sırasında sağlık sisteminin kilitlenmesi nedeniyle rutin aşıların, kanser tedavilerinin ve acil cerrahilerin aksaması sonucu ortaya çıkan ölümlere ne ad verilir?",
                "Dolaylı mortalitedir (indirect mortality / aşırı ölümler).",
                "Sağlık hizmeti aksamasına bağlı ikincil ölümler"
            )
        ]
    })

    return slides
