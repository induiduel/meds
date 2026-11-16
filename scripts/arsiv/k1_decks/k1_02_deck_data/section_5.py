#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 5: Dünya ve Türkiye'de Patolojinin Tarihsel Gelişimi (Adımlar 40 - 49)
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
        # Adım 40
        {
            "slideNumber": 40,
            "title": "Antik Çağ ve Yangının Beş Kardinal Belirtisi: Celsus ve Galen",
            "subtitle": "İnflamasyonun evrensel klinik belirtileri antik Roma hekimleri Celsus ve Galen tarafından tanımlanarak tıp tarihine altın harflerle kazınmıştır.",
            "badge": "Antik Tarihçe",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Yangının temel klinik tablosunu oluşturan kardinal belirtiler, antik Roma hekimleri Celsus ve Galen tarafından tanımlanmıştır.

==Aulus Cornelius Celsus==, yangının dört kardinal belirtisini ortaya koymuştur: ==Rubor== (vazodilatasyona bağlı kızarıklık), ==Calor== (kan akımı artışıyla sıcaklık), ==Dolor== (medyatör uyarısıyla ağrı) ve ==Tumor== (ödem ve eksüdaya bağlı şişlik). Yaklaşık bir asır sonra ==Claudius Galen== bu tabloya beşinci belirti olarak doku hasarından kaynaklanan ==Functio Laesa== (fonksiyon kaybı) durumunu eklemiştir. Bu beş belirti, mikrovasküler geçirgenlik artışı ile hücresel infiltrasyonun dokudaki klinik yansımasıdır.

> [KLASİK SINAV KURALI] Nekroz, apoptoz veya irin kardinal belirti değildir; temel bulgular Rubor, Calor, Dolor, Tumor ve Functio Laesa'dır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Celsus'un 4 Belirtisi", "desc": "Rubor (kızarıklık), Calor (sıcaklık), Dolor (ağrı) ve Tumor (şişlik).", "isKey": True},
                    {"title": "Galen'in 5. Belirtisi", "desc": "Functio Laesa (fonksiyon kaybı) listeye eklenen 5. kardinal bulgudur.", "isKey": True},
                    {"title": "Nekroz Yanılgısı", "desc": "Nekroz hücresel bir ölüm şeklidir; kardinal inflamasyon belirtisi değildir.", "isKey": False}
                ],
                "table": {
                    "title": "İnflamasyonun Beş Kardinal Belirtisi ve Patofizyolojik Karşılıkları",
                    "headers": ["Latince Terim", "Türkçe Karşılığı", "Tanımlayan Hekim", "Altta Yatan Patofizyolojik Mekanizma"],
                    "rows": [
                        ["Rubor", "Kızarıklık", "Aulus Cornelius Celsus", "Histamin etkisiyle arteriyoler vazodilatasyon ve kapiller konjesyon"],
                        ["Calor", "Sıcaklık", "Aulus Cornelius Celsus", "Bölgeye akan arteriyel kan hacminin ve metabolik ısının artışı"],
                        ["Dolor", "Ağrı", "Aulus Cornelius Celsus", "Bradikinin ve PGE2 salınımı, nosiseptörlerin uyarılması ve gerilme"],
                        ["Tumor", "Şişlik (Ödem)", "Aulus Cornelius Celsus", "Endotel aralıklarının açılmasıyla dokuya protein zengini eksüda sızması"],
                        ["Functio Laesa", "Fonksiyon Kaybı", "Claudius Galen", "Hücre zedelenmesi, doku gerginliği ve ağrı refleksiyle işlev yitimi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [ÇIKMIŞ SINAV SORUSU] Aşağıdakilerden hangisi inflamasyonun kardinal belirtilerinden değildir? → CEVAP: Nekroz.",
                "📌 [SINAV SPOTU] Celsus: Rubor, Calor, Dolor, Tumor; Galen: Functio Laesa (Fonksiyon Kaybı).",
                "💡 [ÖĞRENME İPUCU] Yangıda 'Tumor' sözcüğü kanserli kitle demek değildir; doku ödemine bağlı şişlik anlamına gelir."
            ],
            "medicalTerms": [
                {"term": "Kardinal Belirti", "explanation": "İnflamasyonun varlığını gösteren evrensel ve temel klinik bulgulardır."},
                {"term": "Functio Laesa", "explanation": "Doku hasarı ve ağrı nedeniyle organın normal işlevini kaybetmesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "İnflamasyon Belirtileri ve Fizyopatoloji Eşleştirmesi",
                    ["Belirti", "Mekanizma", "İlk Tanımlayan"],
                    [
                        [
                            ("Rubor (Kızarıklık)", False),
                            ("Prekapiller vazodilatasyon ve kan akımı artışı", True, "Damar lümeninin genişlemesi"),
                            ("Celsus", False)
                        ],
                        [
                            ("Tumor (Şişlik)", False),
                            ("Artmış vasküler permeabilite ve eksüda birikimi", True, "Endotel aralıklarının açılması"),
                            ("Celsus", False)
                        ],
                        [
                            ("Functio Laesa (Fonksiyon Kaybı)", False),
                            ("Ağrı ve doku yıkımına bağlı işlev durması", True, "Fizyolojik aktivitenin sekteye uğraması"),
                            ("Galen", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Tıp tarihi ve genel patoloji sınavlarında klasik olarak sorulan: 'Aşağıdakilerden hangisi inflamasyonun klasik kardinal belirtilerinden biri DEĞİLDİR?' sorusunun doğru yanıtı hangisidir?",
                    {
                        "A": "Rubor (Kızarıklık)",
                        "B": "Dolor (Ağrı)",
                        "C": "Nekroz (Hücre Ölümü)",
                        "D": "Calor (Sıcaklık)",
                        "E": "Functio Laesa (Fonksiyon Kaybı)"
                    },
                    "C",
                    {
                        "A": "Yanlış. Rubor Celsus'un tanımladığı kızarıklık belirtisidir.",
                        "B": "Yanlış. Dolor Celsus tarafından tanımlanan ağrı bulgusudur.",
                        "C": "Doğru. Nekroz hücresel bir ölüm şeklidir, yangının kardinal belirtisi değildir.",
                        "D": "Yanlış. Calor Celsus'un tanımladığı sıcaklık artışıdır.",
                        "E": "Yanlış. Functio Laesa Galen'in eklediği fonksiyon kaybı belirtisidir."
                    }
                ),
                make_cloze(
                    "Bergamalı hekim Galen, Celsus'un dört yangı belirtisine beşinci olarak functio laesa yani fonksiyon kaybını eklemiştir.",
                    "functio laesa",
                    "Galen'in eklediği 5. kardinal belirtinin Latince adı"
                )
            ]
        },

        # Adım 41
        {
            "slideNumber": 41,
            "title": "İslam ve Doğu Tıbbı: İbni Sina ve Amasyalı Şerefeddin Sabuncuoğlu",
            "subtitle": "Orta Çağ tıbbında Doğu hekimleri gözlem, cerrahi diseksiyon ve resimli tıp kitaplarıyla modern patolojinin temellerine öncülük etmiştir.",
            "badge": "Doğu ve İslam Tıbbı",
            "badgeColor": "teal",
            "discipline": "Tıp Tarihi",
            "synthesisNarrative": """Orta Çağ döneminde Doğu hekimleri gözlem, diseksiyon ve cerrahi kayıtlarla modern patolojinin temellerine öncülük etmiştir.

==İbni Sina (Avicenna)==, 'El-Kanun fi't-Tıbb' adlı anıtsal eserinde tümörlerin çevre dokulara yayılımını, apse gelişimini ve bulaşıcı hastalıkların mikroskobik etkenlerle taşınabileceğini öngörmüştür. 15. yüzyılda ise ==Amasyalı Şerefeddin Sabuncuoğlu==, 'Cerrahiyetü'l-Haniyye' eseriyle ==Türk-İslam tıbbındaki ilk resimli cerrahi ve patoloji atlasını== oluşturmuştur. Sabuncuoğlu lezyonları kendi çizdiği minyatürlerle görselleştirmiş ve doku yanıtlarını 'Mücerrebname' eserinde deneysel yöntemlerle belgelemiştir.

> [TARİHİ MİRAS] Sabuncuoğlu, lezyon morfolojisini ve cerrahi sınırları minyatürlerle kaydeden dünyadaki öncü cerrah-patologlardandır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "İbni Sina (Avicenna)", "desc": "El-Kanun fi't-Tıbb eseri yüzlerce yıl Doğu ve Batı tıbbının temel başvuru kaynağı olmuştur.", "isKey": True},
                    {"title": "Şerefeddin Sabuncuoğlu", "desc": "Cerrahiyetü'l-Haniyye ile ilk resimli Türkçe cerrahi ve lezyon atlasını üretmiştir.", "isKey": True},
                    {"title": "Mücerrebname", "desc": "İlaç ve doku tedavilerini bizzat deneyerek kaydeden ilk Türkçe farmako-patoloji kitabıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Doğu Tıbbının Öncü Hekimleri ve Eserleri",
                    "headers": ["Hekim", "Yaşadığı Dönem", "Başlıca Eseri", "Tıbbi ve Patolojik Katkısı"],
                    "rows": [
                        ["İbni Sina (Avicenna)", "980 - 1037", "El-Kanun fi't-Tıbb (Canon Medicinae)", "Tümörlerin yayılımı, inflamasyon evreleri ve bulaşıcı etken kuramı"],
                        ["Şerefeddin Sabuncuoğlu", "1385 - 1468", "Cerrahiyetü'l-Haniyye", "İlk resimli Türkçe cerrahi eseri; lezyon morfolojisi ve cerrahi eksizyon minyatürleri"],
                        ["Şerefeddin Sabuncuoğlu", "15. Yüzyıl", "Mücerrebname", "Kendi üzerinde ve hayvanlarda denediği deneysel tıp gözlemleri"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Şerefeddin Sabuncuoğlu'nun 'Cerrahiyetü'l-Haniyye' eseri, Türk tıp tarihindeki ilk resimli cerrahi tıp kitabıdır.",
                "📌 [SINAV SPOTU] İbni Sina'nın 'El-Kanun fi't-Tıbb' eseri Doğu ve Batı tıp fakültelerinde yüzyıllarca temel kaynak olmuştur.",
                "💡 [ÖĞRENME İPUCU] Sabuncuoğlu Amasya Darüşşifası'nda hekimlik yapmış ve cerrahi girişimlerin doku morfolojisini kaydetmiştir."
            ],
            "medicalTerms": [
                {"term": "Cerrahiyetü'l-Haniyye", "explanation": "Sabuncuoğlu'nun lezyon ve cerrahiyi minyatürlerle anlatan ilk Türkçe tıp atlasıdır."},
                {"term": "Canon Medicinae (El-Kanun)", "explanation": "İbni Sina'nın yüzyıllarca Doğu ve Batı'da temel kaynak kabul edilen tıp külliyatıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Doğu Tıbbından Modern Anatomiye Bilgi Akış Zinciri",
                    [
                        "1. Metinlerin Korunması: İslam hekimleri antik tıp metinlerini çevirip geliştirdi.",
                        "2. Sistematik Sınıflama: İbni Sina hastalıkları organ ve belirtilere göre sınıflandırdı.",
                        "3. Görsel Kayıt: Sabuncuoğlu lezyonları minyatürlerle ilk kez resmetti.",
                        "4. Batıya Aktarım: El-Kanun Latinceye çevrilerek Avrupa üniversitelerinde okutuldu.",
                        "5. Anatomik Gelişim: Bu birikim modern patolojik anatominin doğuşuna zemin hazırladı."
                    ]
                ),
                make_cloze(
                    "Amasyalı Şerefeddin Sabuncuoğlu tarafından yazılan ve ilk resimli Türkçe tıp kitabı olma özelliği taşıyan eser Cerrahiyetü'l-Haniyye adını taşır.",
                    "Cerrahiyetü'l-Haniyye",
                    "İlk resimli Türkçe cerrahi eserin adı"
                ),
                make_active_recall(
                    "Şerefeddin Sabuncuoğlu'nun tıp ve patoloji tarihindeki en özgün ve devrimci yönü nedir?",
                    "Cerrahi müdahaleleri ve lezyon morfolojisini bizzat çizdiği minyatürlerle belgeleyerek ilk resimli Türkçe cerrahi atlasını hazırlamasıdır."
                )
            ]
        },

        # Adım 42
        {
            "slideNumber": 42,
            "title": "Organ Patolojisinin Doğuşu: Giovanni Battista Morgagni (1682-1771)",
            "subtitle": "Morgagni; hastalıkların soyut vücut sıvılarından değil, spesifik organlardaki yapısal lezyonlardan kaynaklandığını kanıtlayarak patolojik anatominin babası olmuştur.",
            "badge": "Patolojik Anatomi Kurucusu",
            "badgeColor": "blue",
            "discipline": "Tıp Tarihi",
            "synthesisNarrative": """18. yüzyılda İtalyan anatomist Giovanni Battista Morgagni, Galen'in hümoral sıvı teorisini yıkarak patolojik anatominin temelini atmıştır.

==Giovanni Battista Morgagni==, 1761 yılında yayımladığı =="De Sedibus et Causis Morborum per Anatomen Indagatis"== adlı anıtsal eserinde 700'den fazla otopsiyi incelemiştir. Hastaların ölüm öncesi klinik semptomlarını otopsi masasındaki organ harabiyetiyle doğrudan eşleştirmiştir. Morgagni bu çalışmalarıyla hastalığın vücut sıvılarında değil, ==belirli bir organdaki yapısal lezyonda== yerleştiğini kanıtlamış ve ==Patolojik Anatominin Kurucusu== kabul edilmiştir.

> [DÖNÜM NOKTASI] Morgagni, 'Hastalık nerede oturuyor?' (De Sedibus) sorusunu tıbba kazandırarak klinikopatolojik korelasyonu başlatmıştır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Patolojik Anatominin Babası", "desc": "Morgagni organ temelli patolojik anatomiyi kurarak hümoral teoriyi yıkmıştır.", "isKey": True},
                    {"title": "De Sedibus Eseri (1761)", "desc": "700'den fazla otopside klinik belirtileri organ lezyonlarıyla eşleştirmiştir.", "isKey": True},
                    {"title": "Kliniko-Patolojik Korelasyon", "desc": "Yatak başındaki şikayetlerin otopsi masasındaki organ hasarıyla bağı kanıtlanmıştır.", "isKey": False}
                ],
                "table": {
                    "title": "Morgagni Devrimi: Hümoral Tıptan Organ Patolojisine Geçiş",
                    "headers": ["Parametre", "Morgagni Öncesi (Hümoral Patoloji)", "Morgagni Sonrası (Organ Patolojisi)"],
                    "rows": [
                        ["Hastalığın Kaynağı", "Soyut vücut sıvıları (kan, balgam, kara safra)", "Belirli bir organın anatomik dokusundaki lezyon"],
                        ["Tanı Metodu", "Hastanın mizacına ve nabzına göre spekülasyon", "Klinik semptomlar ile otopsi bulgularının eşleştirilmesi"],
                        ["Morgagni'nin Temel Eseri", "Eski Grek metinlerine körü körüne inanç", "De Sedibus et Causis Morborum per Anatomen Indagatis (1761)"],
                        ["Tarihsel Unvan", "Orta Çağ dogmatizmi", "Patolojik Anatominin Kurucusu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Giovanni Battista Morgagni, 'Patolojik Anatominin Kurucusu' olarak kabul edilir.",
                "📌 [SINAV SPOTU] Morgagni'nin 1761 tarihli anıtsal eseri: 'De Sedibus et Causis Morborum per Anatomen Indagatis'.",
                "💡 [ÖĞRENME İPUCU] Morgagni tıp bilimine 'Hastalığın organ düzeyinde bir adresi vardır' kuralını getirmiştir."
            ],
            "medicalTerms": [
                {"term": "Giovanni Battista Morgagni", "explanation": "Hastalıkların organ lezyonuna dayandığını kanıtlayan patolojik anatominin kurucusudur."},
                {"term": "De Sedibus et Causis Morborum", "explanation": "Morgagni'nin klinikopatolojik korelasyonu başlatan 1761 tarihli beş ciltlik başyapıtıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Morgagni Öncesi vs Morgagni Sonrası Tıp Anlayışı",
                    "Morgagni Öncesi (Galenik Sıvı Teorisi)",
                    "Morgagni Sonrası (Patolojik Anatomi)",
                    [
                        "Hastalık 4 vücut sıvısının (hümor) dengesizliğidir",
                        "Organların iç yapısına ve lezyonlarına bakılmaz",
                        "Tedavi hacamatla kan akıtarak sıvı dengesi kurmaktır",
                        "Klinik semptomların fiziksel bir doku adresi yoktur"
                    ],
                    [
                        "Hastalık spesifik bir organdaki fiziksel hasardır",
                        "Otopsi ile lezyonun anatomik yeri (sedibus) gösterilir",
                        "Tedavi hasarlı organı hedefleyen tıbbi müdahaledir",
                        "Her klinik semptom organdaki morfolojik lezyonun sonucudur"
                    ]
                ),
                make_micro_quiz(
                    "Tıp tarihinde hastalıkların vücut sıvılarının dengesizliğinden değil, doğrudan belirli organlardaki yapısal lezyonlardan kaynaklandığını otopsilerle kanıtlayarak 'Patolojik Anatominin Kurucusu' unvanını alan bilim insanı kimdir?",
                    {
                        "A": "Rudolf Virchow",
                        "B": "Aulus Cornelius Celsus",
                        "C": "Giovanni Battista Morgagni",
                        "D": "Claudius Galen",
                        "E": "Hamdi Suat Aknar"
                    },
                    "C",
                    {
                        "A": "Yanlış. Virchow 1858'de hücresel patolojiyi kurmuştur.",
                        "B": "Yanlış. Celsus yangının dört kardinal belirtisini tanımlamıştır.",
                        "C": "Doğru. Morgagni organ patolojisini kurarak patolojik anatominin babası olmuştur.",
                        "D": "Yanlış. Galen antik çağ hümoral sıvı teorisinin savunucusudur.",
                        "E": "Yanlış. Hamdi Suat Aknar Türkiye'de modern patolojinin kurucusudur."
                    }
                ),
                make_cloze(
                    "Patolojik anatominin kurucusu sayılan Morgagni'nin 1761 yılında yayımladığı anıtsal eseri De Sedibus et Causis Morborum adını taşır.",
                    "De Sedibus et Causis Morborum",
                    "Morgagni'nin anıtsal Latince eserinin adı"
                )
            ]
        },

        # Adım 43
        {
            "slideNumber": 43,
            "title": "Hücresel Patoloji Devrimi: Rudolf Virchow (1821-1902)",
            "subtitle": "Virchow; 'Omnis cellula e cellula' ilkesiyle hastalığın odağını organdan hücreye indirmiş ve modern patolojinin babası olmuştur.",
            "badge": "Modern Patoloji Kurucusu",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """19. yüzyılda ışık mikroskobunun gelişimiyle hastalık kavramı organdan hücre düzeyine inmiş ve modern patoloji başlamıştır.

Alman hekim ==Rudolf Virchow==, 1858'de yayımladığı 'Die Cellularpathologie' eseriyle tıp tarihine damga vurmuştur. Virchow'un temelini attığı =="Omnis cellula e cellula"== (her hücre önceden var olan bir hücreden türer) doktrini, tüm hastalıkların özünde hücresel zedelenmeye dayandığını kanıtlamıştır. Kanser dahil tüm patolojik süreçlerin hücresel temelde gerçekleştiğini gösteren Virchow, ==Modern Patolojinin Kurucusu== unvanını almıştır. Ayrıca tromboz oluşumunu açıklayan ünlü 'Virchow Triadı'nı tanımlamıştır.

> [TARİHİN ZİRVESİ] Morgagni hastalığı organ düzeyine, Virchow ise hücresel düzeye indirerek modern tıbbı başlatmıştır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Modern Patolojinin Babası", "desc": "Rudolf Virchow 1858 hücresel patoloji yayınıyla modern patolojiyi kurmuştur.", "isKey": True},
                    {"title": "Omnis Cellula e Cellula", "desc": "Her hücre bir hücreden türer; tüm hastalıklar hücresel düzeydeki zedelenmelerdir.", "isKey": True},
                    {"title": "Virchow Triadı", "desc": "Trombozun üç temel mekanizmasını (endotel hasarı, staz, hiperkoagülabilite) tanımlamıştır.", "isKey": False}
                ],
                "table": {
                    "title": "Morgagni ile Virchow'un Patoloji Tarihindeki Karşılaştırması",
                    "headers": ["Karşılaştırma Noktası", "Giovanni Battista Morgagni (1761)", "Rudolf Virchow (1858)"],
                    "rows": [
                        ["İnceleme Düzeyi", "Makroskopik organ düzeyi (Organ Patolojisi)", "Mikroskobik hücresel düzey (Hücresel Patoloji)"],
                        ["Temel Eseri", "De Sedibus et Causis Morborum", "Die Cellularpathologie"],
                        ["Temel Doktrini", "Hastalık belirli organlarda yerleşir", "Omnis cellula e cellula (Tüm hastalık hücre hasarıdır)"],
                        ["Evrensel Unvanı", "Patolojik Anatominin Kurucusu", "Modern Patolojinin Kurucusu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Rudolf Virchow 1858 yılında 'Cellularpathologie' eserini yayımlayarak 'Modern Patolojinin Kurucusu' unvanını almıştır.",
                "📌 [SINAV SPOTU] 'Omnis cellula e cellula' aforizması Rudolf Virchow'a aittir.",
                "💡 [ÖĞRENME İPUCU] Morgagni makroskopinin ve organın, Virchow ise mikroskobun ve hücrenin kurucu babasıdır."
            ],
            "medicalTerms": [
                {"term": "Rudolf Virchow", "explanation": "Hücresel patolojiyi kurarak modern patolojinin babası kabul edilen Alman bilim insanıdır."},
                {"term": "Omnis cellula e cellula", "explanation": "Her hücrenin var olan başka bir hücreden bölündüğünü belirten temel biyoloji ilkesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Virchow'un Hücresel Patoloji Mantık Zinciri",
                    [
                        "1. Hücre Bölünmesi: Her canlı hücre var olan bir hücrenin bölünmesiyle çoğalır.",
                        "2. Hücresel Zedelenme: Etiyolojik etkenler doğrudan hücre yapısına ve biyokimyasına zarar verir.",
                        "3. Fonksiyonel Bozulma: Hücre hasarı doku ve organların fizyolojik işlevini aksatır.",
                        "4. Morfolojik Bulgular: Hücre zedelenmesi ve nekroz mikroskop altında görünür hale gelir.",
                        "5. Modern Patoloji: Hastalıkların tedavisinde temel hedef hücresel mekanizmalar olur."
                    ]
                ),
                make_micro_quiz(
                    "1858 yılında yayımladığı 'Cellularpathologie' eseriyle hastalıkların temelinde hücresel hasarın yattığını kanıtlayan ve 'Omnis cellula e cellula' ilkesiyle Modern Patolojinin Kurucusu kabul edilen bilim insanı kimdir?",
                    {
                        "A": "Giovanni Battista Morgagni",
                        "B": "Rudolf Virchow",
                        "C": "Claudius Galen",
                        "D": "Aulus Cornelius Celsus",
                        "E": "Philipp Schwartz"
                    },
                    "B",
                    {
                        "A": "Yanlış. Morgagni organ patolojisinin kurucusudur.",
                        "B": "Doğru. Virchow hücresel patolojiyi kurarak modern patolojinin babası olmuştur.",
                        "C": "Yanlış. Galen antik Roma hekimidir.",
                        "D": "Yanlış. Celsus inflamasyon belirtilerini tanımlamıştır.",
                        "E": "Yanlış. Schwartz 1933 reformuyla İstanbul'a gelen patologdur."
                    }
                ),
                make_cloze(
                    "Rudolf Virchow'un modern hücre teorisinin temeli olan ve her hücrenin bir hücreden doğduğunu belirten ilkesi Omnis cellula e cellula olarak ifade edilir.",
                    "Omnis cellula e cellula",
                    "Virchow'un ünlü Latince hücresel aforizması"
                )
            ]
        },

        # Adım 44
        {
            "slideNumber": 44,
            "title": "Osmanlı'da Modernleşme ve Patoloji Eğitiminin Başlangıcı",
            "subtitle": "II. Mahmut döneminde kadavrada anatomi öğretimiyle başlayan süreç; Mekteb-i Tıbbiye-i Şahane'de ilk patoloji derslerinin verilmesiyle kurumsallaşmıştır.",
            "badge": "Osmanlı Patolojisi",
            "badgeColor": "purple",
            "discipline": "Tıp Tarihi",
            "synthesisNarrative": """Osmanlı İmparatorluğu'nda modern tıp ve patoloji eğitimi, 14 Mart 1827'de Mekteb-i Tıbbiye-i Şahane'nin kuruluşuyla başlamıştır.

Sultan II. Mahmut döneminde verilen izinle Osmanlı tarihinde ilk kez ==kadavra üzerinde diseksiyon ve anatomi öğretimi== hayata geçirilmiştir. 19. yüzyılın son çeyreğinde patoloji bağımsız bir disiplin olarak müfredata girmiştir. ==Ahmet Hilmi Paşa== ilk bağımsız patoloji derslerini verirken, ==Ohannes Tabibyan Bey== patolojik anatomi kürsüsünü yönetmiştir. ==Ahmet Ferit Bey== ve ==Rıfat Hüsamettin Paşa== ise mikroskopi ve otopsi uygulamalarını yerleştirerek Cumhuriyet patolojisinin zeminini hazırlamıştır.

> [KURUMSAL TEMEL] Mekteb-i Tıbbiye'deki kadavra diseksiyonu adımı, Türkiye'de modern patoloji ve cerrahinin doğuşunu sağlamıştır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mekteb-i Tıbbiye-i Şahane", "desc": "1827'de açılarak modern Osmanlı tıp eğitiminin ve Tıp Bayramı'nın kökeni olmuştur.", "isKey": True},
                    {"title": "Kadavra Diseksiyonu İzni", "desc": "II. Mahmut döneminde kadavra üzerinde eğitim izniyle patolojinin önü açılmıştır.", "isKey": True},
                    {"title": "İlk Patoloji Hocaları", "desc": "Ahmet Hilmi Paşa, Ohannes Tabibyan, Ahmet Ferit Bey ve Rıfat Hüsamettin Paşa.", "isKey": False}
                ],
                "table": {
                    "title": "Osmanlı'da Patoloji Eğitiminin Öncü İsimleri",
                    "headers": ["Hekim / Şahsiyet", "Dönemi ve Kurumu", "Tıbbi Patolojiye Katkısı"],
                    "rows": [
                        ["Sultan II. Mahmut", "1827 - Mekteb-i Tıbbiye", "Modern tıp okulunu kurdu; kadavra diseksiyonuna izin vererek anatomik incelemeyi başlattı"],
                        ["Ahmet Hilmi Paşa", "19. Yüzyıl sonu Mekteb-i Tıbbiye", "Müfredatta ilk bağımsız patoloji derslerini veren Osmanlı askeri hekimi"],
                        ["Ohannes Tabibyan Bey", "19. Yüzyıl sonu Mekteb-i Tıbbiye", "Patolojik anatomi ve doku inceleme derslerini yürüttü"],
                        ["Rıfat Hüsamettin Paşa", "19. Yüzyıl sonu - 20. Yüzyıl başı", "Klinik otopsi ve mikroskopi derslerinin yerleşmesine öncülük etti"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Osmanlı'da Mekteb-i Tıbbiye-i Şahane'nin açılış tarihi olan 14 Mart 1827, günümüzde Tıp Bayramı olarak kutlanmaktadır.",
                "📌 [SINAV SPOTU] Mekteb-i Tıbbiye-i Şahane'nin ilk patoloji hocaları arasında Ahmet Hilmi Paşa, Ohannes Tabibyan, Ahmet Ferit Bey ve Rıfat Hüsamettin Paşa yer alır.",
                "💡 [ÖĞRENME İPUCU] II. Mahmut döneminde kadavra ile diseksiyon izni verilmesi, Türkiye'de patoloji eğitiminin en temel yasal başlangıcıdır."
            ],
            "medicalTerms": [
                {"term": "Mekteb-i Tıbbiye-i Şahane", "explanation": "Sultan II. Mahmut'un 1827'de açtığı, modern tıp eğitiminin başladığı askeri okuldur."},
                {"term": "Diseksiyon", "explanation": "Kadavra dokularının anatomik ve patolojik amaçla katmanlarına ayrılarak incelenmesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Osmanlı Dönemi Patoloji Öncüleri ve Katkıları",
                    ["İsim", "Kurum", "Tarihsel Rol"],
                    [
                        [
                            ("Sultan II. Mahmut", False),
                            ("Mekteb-i Tıbbiye-i Şahane", True, "Modern tıp mektebi"),
                            ("Kadavra diseksiyon izni ve modern okul kuruluşu", False)
                        ],
                        [
                            ("Ahmet Hilmi Paşa", False),
                            ("Osmanlı Askeri Tıbbiyesi", True, "Askeri hekimlik"),
                            ("İlk bağımsız patoloji derslerinin verilmesi", False)
                        ],
                        [
                            ("Ohannes Tabibyan Bey", False),
                            ("Tıbbiye Patolojik Anatomi", True, "Patoloji kürsüsü"),
                            ("Patolojik anatomi ve histoloji eğitiminin yürütülmesi", False)
                        ]
                    ]
                ),
                make_cloze(
                    "Osmanlı'da kadavra diseksiyonu ve modern tıp eğitiminin başlangıcı kabul edilen Mekteb-i Tıbbiye-i Şahane 1827 yılında açılmıştır.",
                    "1827",
                    "Mekteb-i Tıbbiye'nin açılış yılı"
                ),
                make_micro_quiz(
                    "Osmanlı İmparatorluğu'nda patoloji eğitiminin gelişim süreci ile ilgili aşağıdakilerden hangisi yanlıştır?",
                    {
                        "A": "II. Mahmut döneminde kadavra ile anatomi öğretimine izin verilmiştir.",
                        "B": "1827'de Mekteb-i Tıbbiye-i Şahane kurularak modern tıp eğitimi başlatılmıştır.",
                        "C": "İlk patoloji dersi veren hocalar arasında Ahmet Hilmi Paşa ve Ohannes Tabibyan Bey bulunmaktadır.",
                        "D": "Osmanlı döneminde otopsi ve mikroskopik inceleme tamamen yasaklanmış ve Cumhuriyet'e kadar hiç uygulanmamıştır.",
                        "E": "19. yüzyılın sonunda patoloji bağımsız bir ders olarak tıp müfredatına girmiştir."
                    },
                    "D",
                    {
                        "A": "Doğru. Kadavra diseksiyonu II. Mahmut döneminde başlamıştır.",
                        "B": "Doğru. 14 Mart 1827 tarihi günümüzde Tıp Bayramı olarak kutlanır.",
                        "C": "Doğru. Bu hekimler Osmanlı'daki ilk patoloji hocalarıdır.",
                        "D": "Yanlış (aranan cevap): 19. yüzyıl sonunda otopsi ve mikroskopi dersleri bizzat yürütülmüştür.",
                        "E": "Doğru. Patoloji bu dönemde bağımsız ders olarak müfredata girmiştir."
                    }
                )
            ]
        },

        # Adım 45
        {
            "slideNumber": 45,
            "title": "Türkiye'de Modern Patolojinin Kurucusu: Prof. Dr. Hamdi Suat Aknar (1869-1936)",
            "subtitle": "Almanya Leipzig'de doktora yapan Hamdi Suat Aknar; ilk patoloji laboratuvarını, 1800 kavanozluk müzeyi kurmuş ve kanser cemiyetine öncülük etmiştir.",
            "badge": "Türk Patolojisinin Babası",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Türkiye'de çağdaş ve kurumsal patolojinin temelleri Ord. Prof. Dr. Hamdi Suat Aknar tarafından atılmıştır.

1904'te Almanya ==Leipzig Üniversitesi'nde Patolojik Anatomi Doktorasını== tamamlayan ==Hamdi Suat Aknar==, 1909'da Darülfünun Patolojik Anatomi Kürsüsü Başkanlığı'na getirilmiştir. Türkiye'deki ilk modern patoloji laboratuvarını kurmuş ve tıp eğitimi için ==yaklaşık 1800 kavanozluk zengin bir Patoloji Müzesi== oluşturmuştur. Veba lenf nodlarında bakterileri fagosite eden mononükleer hücreleri tanımlayarak literatüre giren Aknar, 1933 yılında ==Kanserle Mücadele Cemiyeti'nin== kuruluşuna da öncülük etmiştir.

> [MİLLİ GURUR] Hamdi Suat Aknar, modern Türk patolojisinin kurucu babası olarak kabul edilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Türk Patolojisinin Babası", "desc": "1904 Leipzig doktorasıyla modern patolojiyi Türkiye'ye taşıyan kurucu isimdir.", "isKey": True},
                    {"title": "Patoloji Müzesi", "desc": "Darülfünun bünyesinde yaklaşık 1800 kavanozluk dev eğitim müzesini kurmuştur.", "isKey": True},
                    {"title": "Kanserle Mücadele (1933)", "desc": "Kanserle Mücadele ve Taharri Cemiyeti'nin kuruluşuna liderlik etmiştir.", "isKey": False}
                ],
                "table": {
                    "title": "Prof. Dr. Hamdi Suat Aknar'ın Tarihsel Başarıları",
                    "headers": ["Yıl / Dönem", "Görev ve Faaliyet", "Patoloji Bilimine Katkısı"],
                    "rows": [
                        ["1904", "Almanya Leipzig Üniversitesi", "Patolojik Anatomi doktorasını üstün başarıyla tamamladı"],
                        ["1909", "Darülfünun Tıp Fakültesi", "Patolojik Anatomi Kürsü Başkanı oldu; ilk modern laboratuvarı kurdu"],
                        ["1910'lar", "Patoloji Eğitim Müzesi", "Öğrenciler için yaklaşık 1800 kavanozluk zengin bir organ müzesi oluşturdu"],
                        ["1920'ler", "Veba Araştırmaları", "Veba lenfadenitinde fagositoz yapan retiküloendotelyal hücreleri tanımladı"],
                        ["1933", "Kanser Cemiyeti", "'Kanserle Mücadele ve Taharri Cemiyeti'nin kurucu liderliğini üstlendi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Türkiye'de modern patolojinin kurucusu kabul edilen bilim insanı Prof. Dr. Hamdi Suat Aknar'dır.",
                "📌 [SINAV SPOTU] Hamdi Suat Aknar, Darülfünun'da yaklaşık 1800 kavanozluk ilk zengin Patoloji Müzesi'ni kurmuştur.",
                "📌 [SINAV SPOTU] 1933'te 'Kanserle Mücadele ve Taharri Cemiyeti'nin kuruluşuna öncülük etmiştir."
            ],
            "medicalTerms": [
                {"term": "Hamdi Suat Aknar", "explanation": "1904 Leipzig doktorasıyla Türkiye'de modern patolojiyi kuran bilim insanıdır."},
                {"term": "Patoloji Müzesi", "explanation": "Makroskobik organ lezyonlarının kavanozlarda saklandığı patoloji eğitim arşividir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hamdi Suat Aknar'ın Türk Patolojisini İnşa Süreci",
                    [
                        "1. Leipzig Eğitimi: 1904'te Almanya'da patolojik anatomi doktorasını tamamladı.",
                        "2. Kürsü Kuruluşu: Darülfünun Patolojik Anatomi Kürsüsü'nde modern laboratuvarı kurdu.",
                        "3. Müze Arşivi: Tıp eğitimi için yaklaşık 1800 kavanozluk patoloji müzesini oluşturdu.",
                        "4. Bilimsel Tanımlama: Veba lenf nodlarındaki retiküloendotelyal hücre yanıtını tarif etti.",
                        "5. Kanserle Mücadele: 1933 yılında Türkiye'nin ilk Kanser Cemiyeti'nin kuruluşuna öncülük etti."
                    ]
                ),
                make_micro_quiz(
                    "1904 yılında Leipzig Üniversitesi'nde patoloji doktorasını tamamlayarak yurda dönen, Darülfünun'da ilk modern patoloji laboratuvarını ve yaklaşık 1800 kavanozluk patoloji müzesini kuran 'Türkiye'de Modern Patolojinin Kurucusu' hekim kimdir?",
                    {
                        "A": "Prof. Dr. Philipp Schwartz",
                        "B": "Ord. Prof. Dr. Hamdi Suat Aknar",
                        "C": "Dr. Osman Nuri Aker",
                        "D": "Prof. Dr. Kamile Şevki Mutlu",
                        "E": "Şerefeddin Sabuncuoğlu"
                    },
                    "B",
                    {
                        "A": "Yanlış. Schwartz 1933 reformuyla gelen Alman profesördür.",
                        "B": "Doğru. Hamdi Suat Aknar modern Türk patolojisinin kurucu babasıdır.",
                        "C": "Yanlış. Aker servikal sitolojiyi Türkiye'ye getiren hekimdir.",
                        "D": "Yanlış. Kamile Şevki Mutlu Ankara histoloji kürsüsünün kurucusudur.",
                        "E": "Yanlış. Sabuncuoğlu 15. yüzyılda yaşamış Osmanlı cerrahıdır."
                    }
                ),
                make_cloze(
                    "Hamdi Suat Aknar, tıp öğrencilerinin eğitimi için Darülfünun Tıp Fakültesi bünyesinde yaklaşık 1800 kavanozluk patoloji müzesi kurmuştur.",
                    "1800",
                    "Hamdi Suat Aknar'ın kurduğu müzedeki kavanoz sayısı"
                )
            ]
        },

        # Adım 46
        {
            "slideNumber": 46,
            "title": "1933 Üniversite Reformu ve Yabancı Bilim İnsanları: Schwartz ve Oberndorfer",
            "subtitle": "Cumhuriyet'in 1933 Üniversite Reformuyla İstanbul Üniversitesi'ne davet edilen Philipp Schwartz ve Siegfried Oberndorfer Türk patolojisine çağ atlatmıştır.",
            "badge": "1933 Reformu",
            "badgeColor": "blue",
            "discipline": "Tıp Tarihi",
            "synthesisNarrative": """1933 Üniversite Reformu ile kurulan İstanbul Üniversitesi, Türk patolojisinin uluslararası düzeye ulaşmasında dönüm noktası olmuştur.

Reform kapsamında göreve getirilen Ord. Prof. Dr. ==Philipp Schwartz==, makroskopi, mikroskopi ve otopsiyi patolojinin merkezine yerleştirmiştir. Schwartz, 1942 yılında Türkiye'de klinisyenlerle patologların ortak vaka tartıştığı ==Kliniko-Patolojik Dersleri== başlatmış ve arşiv sistemini modernize etmiştir. Kanser Enstitüsü'nü yöneten Prof. Dr. ==Siegfried Oberndorfer== ise ince bağırsak nöroendokrin tümörlerini tıp literatüründe ilk kez =="Karsinoid Tümör"== olarak tanımlayan dünya çapında bir bilim insanıdır.

> [CUMHURİYET VİZYONU] Schwartz ve Oberndorfer'in getirdiği Alman patoloji ekolü, modern tanı ve arşiv standartlarımızın temelini oluşturmuştur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "1933 Üniversite Reformu", "desc": "Darülfünun yerine İstanbul Üniversitesi kuruldu, yabancı bilim insanları davet edildi.", "isKey": True},
                    {"title": "Philipp Schwartz", "desc": "Otopsi-mikroskopi entegrasyonu, 1942 kliniko-patolojik dersleri ve arşiv sistemini kurdu.", "isKey": True},
                    {"title": "Siegfried Oberndorfer", "desc": "'Karsinoid Tümör' kavramını dünyaya kazandıran, İstanbul'da görev yapmış büyük patologdur.", "isKey": False}
                ],
                "table": {
                    "title": "1933 Reformu Patoloji Profesörleri ve Temel Mirasları",
                    "headers": ["Profesör", "Tarihsel Önemi", "Türk Tıbbına Kazandırdığı Yenilik"],
                    "rows": [
                        ["Ord. Prof. Dr. Philipp Schwartz", "İstanbul Tıp Patoloji Direktörü (1933-1953)", "1942 Kliniko-Patolojik Dersleri, otopsi disiplini ve arşiv kodlama sistemi"],
                        ["Prof. Dr. Siegfried Oberndorfer", "Karsinoid tümörleri dünyaya tanımlayan hekim", "İstanbul Üniversitesi Kanser Enstitüsü yöneticiliği ve onkolojik patoloji araştırmaları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Ord. Prof. Dr. Philipp Schwartz, 1942 yılında Türkiye'de ilk 'Kliniko-Patolojik Dersleri' başlatmıştır.",
                "📌 [SINAV SPOTU] Tıp literatüründe nöroendokrin tümörlere 'Karsinoid' adını veren Prof. Dr. Siegfried Oberndorfer, 1933 reformuyla İstanbul'a gelmiştir.",
                "💡 [ÖĞRENME İPUCU] Schwartz ve Oberndorfer'in getirdiği Alman patoloji disiplini, bugünkü modern Türk patoloji laboratuvarlarının temelini oluşturur."
            ],
            "medicalTerms": [
                {"term": "Philipp Schwartz", "explanation": "1933 reformuyla İstanbul'a gelip kliniko-patolojik dersleri başlatan patoloji hocasıdır."},
                {"term": "Siegfried Oberndorfer", "explanation": "Karsinoid tümörü tıp literatürüne kazandıran ve İstanbul'da çalışan Alman patologdur."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "1933 Reformu Patoloji Liderleri ve Başarıları",
                    ["Bilim İnsanı", "Yıl", "Tıbbi Devrim"],
                    [
                        [
                            ("Philipp Schwartz", False),
                            ("1942", True, "Kliniko-patolojik vaka tartışmalarının başladığı yıl"),
                            ("Kliniko-patolojik dersler ve modern laboratuvar arşivi", False)
                        ],
                        [
                            ("Siegfried Oberndorfer", False),
                            ("1907 - 1933", True, "Karsinoid kavramı ve İstanbul'a gelişi"),
                            ("Karsinoid tümör tanımı ve Kanser Enstitüsü liderliği", False)
                        ]
                    ]
                ),
                make_cloze(
                    "Ord. Prof. Dr. Philipp Schwartz tarafından 1942 yılında başlatılan ve klinisyenler ile patologları vaka başında buluşturan eğitime kliniko-patolojik dersler adı verilir.",
                    "kliniko-patolojik dersler",
                    "Schwartz'ın 1942'de başlattığı multidisipliner ders formatı"
                ),
                make_micro_quiz(
                    "1933 Üniversite Reformu sonrası Türkiye'ye gelerek İstanbul Üniversitesi'nde patoloji kürsüsünü yöneten, 1942'de klinisyenlerle ortak 'Kliniko-Patolojik Dersleri' başlatan ve modern patoloji arşiv sistemini kuran ordinaryüs profesör kimdir?",
                    {
                        "A": "Rudolf Virchow",
                        "B": "Philipp Schwartz",
                        "C": "Hamdi Suat Aknar",
                        "D": "Osman Nuri Aker",
                        "E": "Kamile Şevki Mutlu"
                    },
                    "B",
                    {
                        "A": "Yanlış. Virchow 19. yüzyılda Almanya'da hücresel patolojiyi kurmuştur.",
                        "B": "Doğru. Philipp Schwartz 1942'de kliniko-patolojik dersleri ve modern arşivi başlatmıştır.",
                        "C": "Yanlış. Hamdi Suat Aknar reform öncesi Darülfünun dönemi kurucusudur.",
                        "D": "Yanlış. Osman Nuri Aker servikal sitolojiyi Türkiye'ye kazandırmıştır.",
                        "E": "Yanlış. Kamile Şevki Mutlu Ankara Tıp Histoloji Kürsüsü'nü kurmuştur."
                    }
                )
            ]
        },

        # Adım 47
        {
            "slideNumber": 47,
            "title": "Cumhuriyet'in Öncü Kadın Hekimi: Prof. Dr. Kamile Şevki Mutlu (1906-1987)",
            "subtitle": "Türkiye'nin ilk kadın patoloji uzmanlarından Kamile Şevki Mutlu; Ankara Numune Hastanesi Patoloji Laboratuvarı'nı ve Ankara Tıp Histoloji Kürsüsü'nü kurmuştur.",
            "badge": "Cumhuriyet Öncüsü",
            "badgeColor": "cyan",
            "discipline": "Tıp Tarihi",
            "synthesisNarrative": """Türkiye Cumhuriyeti'nin ilk kadın patoloji uzmanlarından Prof. Dr. Kamile Şevki Mutlu, başkent Ankara'da patoloji ve histolojinin kurumsallaşmasını sağlamıştır.

Hamdi Suat Aknar'ın yanında uzmanlaşan ==Kamile Şevki Mutlu==, ==Ankara Numune Hastanesi Patoloji Laboratuvarı'nı== kurarak başkentin ilk modern tanı merkezini oluşturmuştur. 1945'te kurulan ==Ankara Üniversitesi Tıp Fakültesi Histoloji ve Embriyoloji Kürsüsü'nün== kurucu başkanlığını üstlenmiştir. Adrenal bez kromafin hücrelerini gösteren özel boyama tekniğiyle ('Şevki Metodu') literatüre geçmiş; 1953'te Atatürk'ün naaşının Anıtkabir'e naklinde tahnid denetim heyetinde yer almıştır.

> [İLHAM VEREN YAŞAM] Kamile Şevki Mutlu, başkent Ankara'nın ilk patoloji laboratuvarını ve tıp fakültesi histoloji kürsüsünü kuran öncü bilim insanıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Ankara Numune Laboratuvarı", "desc": "Başkent Ankara'nın ilk modern patoloji laboratuvarını kurmuştur.", "isKey": True},
                    {"title": "Ankara Tıp Histoloji Kürsüsü", "desc": "1945'te kurulan kürsünün ilk başkanı ve efsane hocası olmuştur.", "isKey": True},
                    {"title": "Şevki Boyama Metodu", "desc": "Adrenal bez kromafin hücrelerinin gösterilmesinde kendi geliştirdiği boyama tekniği vardır.", "isKey": False}
                ],
                "table": {
                    "title": "Prof. Dr. Kamile Şevki Mutlu'nun Hayatı ve Kurucu Başarıları",
                    "headers": ["Yıl / Aşama", "Kurum / Görev", "Öncü Hizmeti"],
                    "rows": [
                        ["1928", "Darülfünun Tıp Fakültesi", "İlk kadın tıp mezunlarından biri olarak Hamdi Suat Bey ile patoloji ihtisası"],
                        ["1930'lar", "Ankara Numune Hastanesi", "Başkentin ilk modern patoloji laboratuvarını kurdu ve yönetti"],
                        ["1945", "Ankara Üniversitesi Tıp Fakültesi", "Histoloji ve Embriyoloji Kürsüsü Kurucu Başkanlığına atandı"],
                        ["1953", "Anıtkabir Tıp Komisyonu", "Atatürk'ün naaşının naklinde tahnid kontrol heyetinde görev aldı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Ankara Numune Hastanesi Patoloji Laboratuvarı'nı ve Ankara Üniversitesi Tıp Fakültesi Histoloji-Embriyoloji Kürsüsü'nü Prof. Dr. Kamile Şevki Mutlu kurmuştur.",
                "📌 [TARİHİ SPOT] Kamile Şevki Mutlu, 1953'te Atatürk'ün naaşının Anıtkabir'e nakli heyetinde yer alan seçkin hekimdir.",
                "💡 [ÖĞRENME İPUCU] Hamdi Suat Aknar'ın öğrencisidir ve Alman ekolünü Ankara'ya taşıyan kurucu isimdir."
            ],
            "medicalTerms": [
                {"term": "Kamile Şevki Mutlu", "explanation": "Ankara Numune Patoloji ve Ankara Tıp Histoloji kürsüsünü kuran ilk kadın patologdur."},
                {"term": "Kromafin Hücre", "explanation": "Adrenal medullada katekolamin salgılayan ve krom tuzlarıyla boyanan nöroendokrin hücredir."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "Prof. Dr. Kamile Şevki Mutlu'nun Türkiye'deki patoloji ve tıp eğitimine en büyük iki kurumsal katkısı nedir?",
                    "Ankara Numune Hastanesi Patoloji Laboratuvarı'nı kurmuş ve Ankara Üniversitesi Tıp Fakültesi Histoloji-Embriyoloji Kürsüsü'nün kurucu başkanı olmuştur."
                ),
                make_cloze(
                    "Ankara Numune Hastanesi Patoloji Laboratuvarı'nı ve Ankara Tıp Histoloji Kürsüsü'nü kuran Cumhuriyetin öncü kadın hekimi Kamile Şevki Mutlu'dur.",
                    "Kamile Şevki Mutlu",
                    "Ankara patoloji laboratuvarını kuran kadın tıp profesörümüzün adı"
                ),
                make_micro_quiz(
                    "Cumhuriyet döneminde Ankara Numune Hastanesi Patoloji Laboratuvarı'nı kuran ve daha sonra 1945'te kurulan Ankara Üniversitesi Tıp Fakültesi Histoloji ve Embriyoloji Kürsüsü'nün ilk başkanı olan öncü bilim insanımız kimdir?",
                    {
                        "A": "Prof. Dr. Philipp Schwartz",
                        "B": "Prof. Dr. Kamile Şevki Mutlu",
                        "C": "Dr. Osman Nuri Aker",
                        "D": "Ahmet Hilmi Paşa",
                        "E": "Ord. Prof. Dr. Hamdi Suat Aknar"
                    },
                    "B",
                    {
                        "A": "Yanlış. Schwartz İstanbul Üniversitesi Patoloji Enstitüsü Direktörüdür.",
                        "B": "Doğru. Kamile Şevki Mutlu Ankara'daki laboratuvar ve kürsülerin kurucusudur.",
                        "C": "Yanlış. Aker servikal sitolojiyi Türkiye'ye getiren uzmandır.",
                        "D": "Yanlış. Ahmet Hilmi Paşa 19. yüzyıl Mekteb-i Tıbbiye hocasıdır.",
                        "E": "Yanlış. Hamdi Suat Aknar Darülfünun dönemi kürsü başkanıdır."
                    }
                )
            ]
        },

        # Adım 48
        {
            "slideNumber": 48,
            "title": "Türkiye'de Sitolojinin Doğuşu: Dr. Osman Nuri Aker ve PAP Testi",
            "subtitle": "Dr. Osman Nuri Aker; New York'ta bizzat Dr. George Papanicolaou ile çalışarak servikal smear (PAP testi) yöntemini Türkiye'ye kazandırmıştır.",
            "badge": "Sitoloji Öncüsü",
            "badgeColor": "indigo",
            "discipline": "Sitopatoloji Tarihi",
            "synthesisNarrative": """Serviks kanserinin erken evrede yakalanmasını sağlayan sitopatoloji devrimi, Dr. Osman Nuri Aker sayesinde Türkiye'ye taşınmıştır.

==Dr. Osman Nuri Aker==, 1947 yılında New York'ta bizzat yöntemin mucidi ==Dr. George Papanicolaou'nun yanında== çalışarak ilk sitoloji kursunu tamamlamıştır. Yurda döndüğünde ==Papanicolaou Servikal Sitoloji (PAP Smear)== yöntemini Türkiye'ye kazandırmıştır. Rutin jinekolojik smear taramalarını başlatmış, servikal prekanseröz lezyonların invaziv kansere dönüşmeden saptanmasını sağlamış ve ülkemizde sitopatolojinin bağımsız bir disiplin olarak kurulmasına öncülük etmiştir.

> [TANI DEVRİMİ] Osman Nuri Aker'in kurduğu PAP testi taramaları, Türkiye'de serviks karsinomu kaynaklı mortaliteyi belirgin şekilde düşürmüştür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Papanicolaou ile Çalışma", "desc": "1947'de ABD'de bizzat yöntemin mucidi Dr. Papanicolaou'dan eğitim almıştır.", "isKey": True},
                    {"title": "PAP Smear Türkiye'de", "desc": "Servikal sitoloji yöntemini Türkiye'ye getirerek rutin kanser taramasını başlatmıştır.", "isKey": True},
                    {"title": "Sitopatoloji Disiplini", "desc": "Türkiye'de sitopatolojinin cerrahi patolojiden bağımsız bir uzmanlık alanı olmasını sağlamıştır.", "isKey": False}
                ],
                "table": {
                    "title": "Dr. Osman Nuri Aker ve Sitoloji Devriminin Kilometre Taşları",
                    "headers": ["Yıl", "Gelişme", "Klinikopatolojik Etki"],
                    "rows": [
                        ["1943", "Papanicolaou ve Traut'un PAP testi yayını", "Dünyada eksfolyatif sitolojiyle serviks kanseri teşhisi başladı"],
                        ["1947", "Osman Nuri Aker'in New York eğitimi", "Dr. Papanicolaou'nun ilk geniş kapsamlı sitoloji kursuna katılan ilk Türk hekim oldu"],
                        ["1950'ler", "Türkiye'de PAP testinin uygulanması", "Servikal preinvaziv lezyonların taranması ve erken tedavisi başladı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Türkiye'ye Papanicolaou servikal sitoloji (PAP smear) yöntemini getiren ve bu alanda öncülük eden hekim Dr. Osman Nuri Aker'dir.",
                "📌 [SINAV SPOTU] Dr. Osman Nuri Aker 1947'de ABD'de Dr. George Papanicolaou ile bizzat birlikte çalışmıştır.",
                "💡 [ÖĞRENME İPUCU] PAP testi bugün Sağlık Bakanlığı KETEM merkezlerinde serviks kanseri taramasının temel yöntemidir."
            ],
            "medicalTerms": [
                {"term": "Osman Nuri Aker", "explanation": "1947'de Dr. Papanicolaou ile çalışarak PAP smear yöntemini Türkiye'ye kazandıran hekimdir."},
                {"term": "Papanicolaou (PAP) Testi", "explanation": "Servikal epitel hücreleriyle prekanseröz lezyonları erken tarayan sitolojik testtir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "PAP Testinin Türkiye'ye Geliş Zinciri",
                    [
                        "1. New York Eğitimi: Dr. Osman Nuri Aker bizzat Dr. Papanicolaou'nun sitoloji kursuna katıldı.",
                        "2. Metodun Aktarımı: Papanicolaou boyama ve fiksasyon protokollerini Türkiye'ye taşıdı.",
                        "3. Rutin Tarama: Jinekolojik muayenelerde servikal yayma ve tarama pratiği başlatıldı.",
                        "4. Erken Tanı: Karsinoma in situ evresindeki servikal lezyonlar mikroskopiyle yakalandı.",
                        "5. Sitopatolojinin Kuruluşu: Türkiye'de sitopatoloji güvenilir ve bağımsız bir disiplin oldu."
                    ]
                ),
                make_micro_quiz(
                    "1947 yılında New York'ta bizzat Dr. George Papanicolaou ile çalışarak servikal sitoloji (PAP smear) tarama yöntemini Türkiye'ye getiren ve sitopatolojinin ülkemizde kurumsallaşmasını sağlayan hekim kimdir?",
                    {
                        "A": "Hamdi Suat Aknar",
                        "B": "Osman Nuri Aker",
                        "C": "Philipp Schwartz",
                        "D": "Kamile Şevki Mutlu",
                        "E": "Şerefeddin Sabuncuoğlu"
                    },
                    "B",
                    {
                        "A": "Yanlış. Hamdi Suat Aknar modern patolojiyi kurmuştur.",
                        "B": "Doğru. Osman Nuri Aker PAP testini Türkiye'ye getiren ve sitolojiyi kuran hekimdir.",
                        "C": "Yanlış. Schwartz 1933 reformu patoloji ordinaryüsüdür.",
                        "D": "Yanlış. Kamile Şevki Mutlu Ankara Histoloji Kürsüsü kurucusudur.",
                        "E": "Yanlış. Sabuncuoğlu 15. yüzyıl Amasya cerrahıdır."
                    }
                ),
                make_cloze(
                    "Papanicolaou servikal sitoloji yöntemini Türkiye'ye getiren hekim Dr. Osman Nuri Aker olarak tıp tarihimize geçmiştir.",
                    "Osman Nuri Aker",
                    "PAP smear yöntemini Türkiye'ye kazandıran hekimin adı"
                )
            ]
        },

        # Adım 49: [TEKRAR SAYFASI - CHECKPOINT 5]
        {
            "slideNumber": 49,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Patoloji Tarihi: Antik Çağdan Modern Türkiye'ye Tarihsel Çizgi",
            "subtitle": "Bölüm 5'in Celsus, Galen, Morgagni, Virchow, Sabuncuoğlu, Hamdi Suat Aknar, Schwartz ve Aker konularını toparlayan kritik sentez istasyonu.",
            "badge": "Checkpoint 5",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 5,
            "synthesisNarrative": """Patoloji tarihi, antik çağın hümoral sıvılarından organ lezyonlarına ve hücresel zedelenmeye uzanan bilimsel bir dönüşümdür.

Antik Roma'da Celsus ve Galen yangının kardinal belirtilerini saptamıştır. 1761'de ==Giovanni Battista Morgagni== organ patolojisini, 1858'de ise ==Rudolf Virchow== hücresel patolojiyi ('Omnis cellula e cellula') kurarak modern patolojinin temellerini atmıştır. Türkiye'de ise Sabuncuoğlu'nun cerrahi atlası, II. Mahmut'un kadavra izni, ==Hamdi Suat Aknar'ın== laboratuvar ve müzesi, 1933 reformunda ==Philipp Schwartz'ın== kliniko-patolojik dersleri, ==Kamile Şevki Mutlu'nun== Ankara kürsüleri ve ==Osman Nuri Aker'in== PAP testi bu gelişimin köşe taşlarıdır.

> [BÖLÜM ÖZETİ] Morgagni hastalığı organa, Virchow hücreye indirmiştir; modern Türk patolojisinin temeli ise Hamdi Suat Aknar ile atılmıştır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Morgagni vs Virchow", "desc": "Morgagni organ patolojisinin (1761), Virchow ise hücresel/modern patolojinin (1858) babasıdır.", "isKey": True},
                    {"title": "Yangının 5 Belirtisi", "desc": "Rubor, Calor, Dolor, Tumor (Celsus) + Functio Laesa (Galen). Nekroz kardinal belirti değildir.", "isKey": True},
                    {"title": "Türk Patolojisinin Omurgası", "desc": "Hamdi Suat Aknar (kurucu baba), Philipp Schwartz (1933 reformu), Osman Nuri Aker (sitoloji).", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 5 Patoloji Tarihi Kronolojik Sentez Tablosu",
                    "headers": ["Bilim İnsanı / Dönem", "Yıl / Çağ", "Kritik Eser / Unvan", "Tarihe Kazandırdığı Temel İlke"],
                    "rows": [
                        ["Aulus Cornelius Celsus", "MÖ 30 - MS 38", "De Medicina", "İnflamasyonun 4 belirtisi: Rubor, Calor, Dolor, Tumor"],
                        ["Claudius Galen", "MS 130 - 200", "Galenik Tıp", "İnflamasyona 5. belirti: Functio Laesa (Fonksiyon Kaybı)"],
                        ["Amasyalı Şerefeddin Sabuncuoğlu", "1465", "Cerrahiyetü'l-Haniyye", "İlk resimli Türkçe cerrahi tıp atlası ve minyatürleri"],
                        ["Giovanni Battista Morgagni", "1761", "De Sedibus et Causis Morborum", "Patolojik Anatominin Kurucusu (Hastalık organ lezyonudur)"],
                        ["Rudolf Virchow", "1858", "Cellularpathologie", "Modern Patolojinin Kurucusu ('Omnis cellula e cellula')"],
                        ["Hamdi Suat Aknar", "1904 - 1909", "1800 kavanozluk Müze", "Türkiye'de Modern Patolojinin Kurucusu"],
                        ["Ord. Prof. Philipp Schwartz", "1933 - 1942", "Kliniko-Patolojik Dersler", "1933 Reformu, arşivleme ve kliniko-patolojik konferanslar"],
                        ["Prof. Dr. Kamile Şevki Mutlu", "1930'lar - 1945", "Ankara Tıp Histoloji Kürsüsü", "Ankara Numune ve Ankara Tıp'ın öncü kadın kurucusu"],
                        ["Dr. Osman Nuri Aker", "1947", "PAP Smear Yöntemi", "Papanicolaou servikal sitolojisini Türkiye'ye getiren hekim"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekroz inflamasyonun kardinal belirtisi DEĞİLDİR; kardinal belirtiler Rubor, Calor, Dolor, Tumor ve Functio Laesa'dır.",
                "📌 [SINAV SPOTU] Morgagni: Patolojik Anatomi kurucusu (1761); Virchow: Modern Patoloji kurucusu (1858).",
                "📌 [SINAV SPOTU] Hamdi Suat Aknar: Türkiye'de modern patoloji kurucusu; Osman Nuri Aker: PAP testini getiren hekim."
            ],
            "medicalTerms": [
                {"term": "Hümoral Teori", "explanation": "Hastalıkların dört vücut sıvısının dengesizliğinden doğduğunu savunan antik tıp teorisidir."},
                {"term": "Kliniko-Patolojik Korelasyon", "explanation": "Klinik semptomlar ile doku ve organlardaki lezyonların eşleştirilerek tanı konmasıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p5-1",
                    "İnflamasyonun kardinal belirtilerini tanımlayan antik Roma hekimleri kimlerdir ve hangi belirtileri eklemişlerdir?",
                    "Aulus Cornelius Celsus 4 kardinal belirtiyi tanımlamıştır: Rubor (kızarıklık), Calor (sıcaklık), Dolor (ağrı) ve Tumor (şişlik). Galen ise buna 5. belirti olarak Functio Laesa'yı (fonksiyon kaybı) eklemiştir. Nekroz kardinal belirti değildir.",
                    "Celsus (4) + Galen (1)",
                    "Patoloji Tarihi"
                ),
                make_flashcard(
                    "fc-p5-2",
                    "Patoloji tarihinde Giovanni Battista Morgagni ile Rudolf Virchow arasındaki temel inceleme düzeyi ve devrim farkı nedir?",
                    "Morgagni 1761'de organ patolojisini (Patolojik Anatomi) kurmuş ve hastalığın belirli organlarda oturduğunu kanıtlamıştır. Virchow ise 1858'de mikroskobik hücresel patolojiyi (Modern Patoloji) kurmuş ve 'Omnis cellula e cellula' ilkesiyle her hastalığın hücresel düzeyde zedelenme olduğunu kanıtlamıştır.",
                    "Organ (Morgagni) vs Hücre (Virchow)",
                    "Patoloji Tarihi"
                ),
                make_flashcard(
                    "fc-p5-3",
                    "Türk tıp tarihinde Hamdi Suat Aknar, Philipp Schwartz ve Osman Nuri Aker'in sırasıyla en kritik kurucu hizmetleri nelerdir?",
                    "Hamdi Suat Aknar Türkiye'de ilk modern patoloji laboratuvarını ve 1800 kavanozluk müzeyi kuran Türk patolojisinin babasıdır. Philipp Schwartz 1933 reformuyla gelerek 1942'de kliniko-patolojik dersleri ve arşiv sistemini başlatmıştır. Osman Nuri Aker ise 1947'de bizzat Papanicolaou ile çalışarak PAP smear servikal sitolojisini Türkiye'ye getirmiştir.",
                    "Kurucu baba, 1933 reformu hocası, sitoloji öncüsü",
                    "Türk Patoloji Tarihi"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 5'te incelenen tıp tarihi ve patoloji öncüleri dikkate alındığında, aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                    {
                        "A": "Rubor, Calor, Dolor, Tumor → Aulus Cornelius Celsus",
                        "B": "Omnis cellula e cellula ve Modern Patoloji → Rudolf Virchow",
                        "C": "Patolojik Anatominin Kurucusu ve De Sedibus → Giovanni Battista Morgagni",
                        "D": "Papanicolaou servikal sitolojisini Türkiye'ye getiren hekim → Dr. Osman Nuri Aker",
                        "E": "Türkiye'de ilk modern patoloji müzesini kuran hekim → Ord. Prof. Dr. Philipp Schwartz"
                    },
                    "E",
                    {
                        "A": "Doğru. Celsus inflamasyonun ilk 4 kardinal belirtisini tanımlamıştır.",
                        "B": "Doğru. Virchow 1858'de hücresel modern patolojiyi kurmuştur.",
                        "C": "Doğru. Morgagni 1761'de patolojik anatominin temellerini atmıştır.",
                        "D": "Doğru. Osman Nuri Aker 1947'de PAP testini Türkiye'ye getirmiştir.",
                        "E": "Yanlış (aranan cevap): 1800 kavanozluk Patoloji Müzesi'ni kuran hekim Prof. Dr. Hamdi Suat Aknar'dır."
                    }
                ),
                make_interactive_table(
                    "Patoloji Tarihinin Kurucu İsimleri ve Katkıları",
                    ["Tarihsel İsim", "Dönemi", "Tıbbi Devrimi"],
                    [
                        [
                            ("Giovanni Battista Morgagni", False),
                            ("1761 - Padova", True, "Organ patolojisinin anıtsal eseri"),
                            ("Patolojik Anatominin Kurucusu; hastalık organda yerleşir", False)
                        ],
                        [
                            ("Rudolf Virchow", False),
                            ("1858 - Berlin", True, "Hücresel patolojinin kuruluşu"),
                            ("Modern Patolojinin Kurucusu; Omnis cellula e cellula", False)
                        ],
                        [
                            ("Hamdi Suat Aknar", False),
                            ("1904 - 1909 İstanbul", True, "Leipzig doktorası ve kürsü"),
                            ("Türk Patolojisinin Babası; ilk modern laboratuvar ve müze", False)
                        ]
                    ]
                )
            ]
        }
    ]
