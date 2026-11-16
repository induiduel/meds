#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 7: Patoloji Laboratuvarı: Materyal Tipleri, Biyopsi Çeşitleri ve Güvenlik (Adımlar 60 - 69)
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
        # Adım 60
        {
            "slideNumber": 60,
            "title": "Patoloji Laboratuvarına Gelen Materyal Tipleri ve Sınıflandırma",
            "subtitle": "Patoloji laboratuvarı; biyopsilerden organ rezeksiyonlarına, vücut sıvılarından taze dokulara kadar geniş bir spektrumda materyal kabul eder.",
            "badge": "Laboratuvar Materyalleri",
            "badgeColor": "blue",
            "discipline": "Laboratuvar Yönetimi",
            "synthesisNarrative": """Patoloji laboratuvarına gelen materyaller morfolojik büyüklüklerine ve klinik amaçlarına göre dört ana grupta sınıflandırılır.

1. ==Biyopsi Örnekleri:== Tanı amacıyla yaşayan hastadan endoskopi, iğne veya punch yöntemleriyle alınan küçük doku parçalarıdır.
2. ==Cerrahi Rezeksiyon Materyalleri:== Tanısı konulmuş lezyonların cerrahi tedavisinde organın bir kısmının veya tamamının çıkarıldığı büyük örneklerdir (kolektomi, mastektomi).
3. ==Sitolojik Materyaller:== Vücut boşluk sıvıları (plevra, periton), sürüntüler (smear) ve ince iğne aspiratlarıdır.
4. ==Özel ve Taze Dokular:== İntraoperatif frozen inceleme, elektron mikroskopisi ve moleküler testler için formalinsiz gönderilen taze dokulardır.

> [LABORATUVAR KURALI] Her materyal grubunun preanalitik kabul protokolü, fiksasyon süresi ve işleme basamakları birbirinden farklıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Dört Temel Grup", "desc": "Biyopsi, rezeksiyon, sitoloji ve taze/özel materyaller.", "isKey": True},
                    {"title": "Farklı Protokoller", "desc": "Küçük biyopsi 6-12 saatte fikse olurken, büyük rezeksiyonlar 24-48 saat fiksasyon gerektirir.", "isKey": True},
                    {"title": "Taze Materyal Duyarlılığı", "desc": "Frozen ve mikrobiyoloji dokuları kesinlikle formalin fiksatifi konmadan getirilmelidir.", "isKey": False}
                ],
                "table": {
                    "title": "Patolojiye Gelen Materyal Tiplerinin Karşılaştırması",
                    "headers": ["Materyal Grubu", "Klinik Örnek", "Temel Tanısal Amaç", "Fiksasyon Yaklaşımı"],
                    "rows": [
                        ["Küçük Biyopsi", "Endoskopik mide biyopsisi, punch", "Hızlı tanı, lezyonun benign/malign ayrımı", "Doğrudan %10 nötral tamponlu formalin"],
                        ["Büyük Rezeksiyon", "Sağ hemikolektomi, radikal nefrektomi", "Tümör evresi, cerrahi sınırlar, lenf nodu sayısı", "Açılarak/dilimlenerek 24-48 saat formalin fiksasyonu"],
                        ["Sitolojik Sıvı", "Asit sıvısı, plevral efüzyon", "Malign hücre taraması ve hücre bloğu hazırlama", "Taze veya %50-70 alkol fiksasyonu"],
                        ["İntraoperatif Materyal", "Ameliyat esnasında gönderilen sınır dokusu", "Dakikalar içinde cerrahi sınır kontrolü (frozen)", "Asla fiksatif konmaz; kuru gazlı bezde taze gönderilir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İntraoperatif dondurma (frozen) kesit için gönderilen dokular kesinlikle formalin içine KONULMAZ; taze olarak kuru gazlı bezde ulaştırılır.",
                "📌 [LABORATUVAR SPOTU] Büyük rezeksiyon materyalleri açılmadan fiksatife atılırsa merkez doku fiksatifle temas edemez ve otolize uğrar.",
                "🚨 [KRİTİK UYARI] Taze doku ile formalinli doku kaplarının karıştırılması frozen incelemesini teknik olarak imkansız kılar."
            ],
            "medicalTerms": [
                {"term": "Rezeksiyon", "explanation": "Bir organ veya dokunun tedavi amacıyla cerrahi olarak tamamen veya kısmen çıkarılmasıdır."},
                {"term": "Preanalitik Süreç", "explanation": "Numunenin hastadan alınmasından doku takibine kadar geçen kayıt ve hazırlık sürecidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Materyal Tipleri ve Taşıma Koşulları Eşleştirmesi",
                    ["Materyal Niteliği", "Klinik Amaç", "Doğru Taşıma Koşulu"],
                    [
                        [
                            ("Frozen Kesit Dokusu", False),
                            ("Ameliyat esnasında hızlı sınır kontrolü", True, "Dakikalar içinde cerrahi karar"),
                            ("Taze, fiksatifsiz, nemli gazlı bezde", False)
                        ],
                        [
                            ("Punch Deri Biyopsisi", False),
                            ("Displastik lezyonun histolojik tanısı", True, "Deri katmanlarının incelenmesi"),
                            ("%10 nötral tamponlu formalin içinde", False)
                        ],
                        [
                            ("Plevral Efüzyon Sıvısı", False),
                            ("Malign mezotelyoma / metastaz taraması", True, "Dökülen malign hücre tespiti"),
                            ("Taze veya sitolojik alkol fiksatifinde", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Ameliyathanede meme kanseri operasyonu sürerken cerrahın cerrahi sınırın temiz olup olmadığını 10 dakika içinde öğrenmek için patolojiye gönderdiği doku kabına servis hemşiresi yanlışlıkla %10 formalin doldurmuştur. Bu durumun yol açacağı en büyük teknik hata nedir?",
                    {
                        "A": "Meme dokusunun aşırı yumuşaması",
                        "B": "Formalinin doku suyunu çekip dondurucu kriostat cihazında buz kristali artefaktı yapması ve acil frozen kesit alma kalitesini bozması",
                        "C": "Doku kasetinin erimesi",
                        "D": "Mikroskop okülerinin kirlenmesi",
                        "E": "Tümör hücrelerinin tamamen yok olması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Formalin dokuyu yumuşatmaz, sertleştirir.",
                        "B": "Doğru. Formalin doku suyunu çekerek dondurma esnasında buz kristali artefaktı yaratır ve acil kesit kalitesini bozar.",
                        "C": "Yanlış. Plastik doku kasetleri formalinde erimez.",
                        "D": "Yanlış. Mikroskop oküleri kimyasal temasla kirlenmez.",
                        "E": "Yanlış. Formalin hücreleri öldürür ancak yok etmez."
                    }
                ),
                make_cloze(
                    "İntraoperatif konsültasyon amacıyla gönderilen dokular dondurularak kesileceği için kesinlikle formalin fiksatifine konulmadan taze ulaştırılmalıdır.",
                    "formalin",
                    "Frozen dokusuna asla konulmaması gereken rutin fiksatif"
                )
            ]
        },

        # Adım 61
        {
            "slideNumber": 61,
            "title": "Biyopsi Kavramı ve Klinik Amaçları",
            "subtitle": "Biyopsi; canlı bir organizmadan kesin histopatolojik tanı koymak amacıyla en az invaziv yolla en yüksek tanısal bilginin elde edilmesidir.",
            "badge": "Biyopsi Kavramı",
            "badgeColor": "teal",
            "discipline": "Cerrahi Patoloji",
            "synthesisNarrative": """==Biyopsi==; yaşayan bir hastadan mikroskobik inceleme yapmak üzere doku veya hücre örneği alınması işlemidir.

Tıbbi uygulamadaki temel ilke **en az invaziv yöntemle en yüksek tanısal veriyi** elde etmektir. Biyopsinin klinik tıp pratiğindeki başlıca hedefleri şunlardır:
1. ==Kesin Tanı:== Şüpheli lezyonun neoplazi, inflamasyon veya metabolik bir hasar olup olmadığını ayırt etmek.
2. ==Tedavi Planlaması:== Cerrahi sınır genişliğini veya ameliyat öncesi neoadjuvan kemoterapi gerekliliğini belirlemek.
3. ==Hastalık ve Rejeksiyon İzlemi:== Hepatit aktivitesini ya da organ nakli sonrası doku reddini takip etmek.
4. ==Prognoz Tayini:== Tümörün histolojik diferansiyasyon derecesini ve moleküler profilini saptamak.

> [KLİNİK İLKE] Biyopsi sadece lezyonu adlandırmaz; cerrahın neşter yönünü ve onkoloğun tedavi planını doğrudan yönetir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Yaşayan Hastadan Alınır", "desc": "Otopsiden en temel farkı canlı hastaya tedavi rehberliği yapmasıdır.", "isKey": True},
                    {"title": "Minimal İnvaziv Hedef", "desc": "Hastaya en az zarar vererek en doğru doku mimarisini elde etmek esastır.", "isKey": True},
                    {"title": "Tedavi ve İzlem", "desc": "Tanının yanı sıra organ rejeksiyonu ve tedaviye yanıtı izlemede kullanılır.", "isKey": False}
                ],
                "table": {
                    "title": "Klinik Pratikte Biyopsi Alma Endikasyonları",
                    "headers": ["Endikasyon Grubu", "Klinik Senaryo", "Patolojik İncelemenin Katkısı"],
                    "rows": [
                        ["Neoplazi Şüphesi", "Mamografide şüpheli kitle, akciğerde nodül", "Benign-malign ayrımı, histolojik alt tip ve İHK profili"],
                        ["İnflamatuvar Hastalıklar", "Kronik ishal, kanlı dışkılama", "Ülseratif kolit vs Crohn hastalığı ayrımı"],
                        ["Organ Nakli İzlemi", "Böbrek/karaciğer nakli sonrası kreatinin/AST artışı", "Hücresel veya hümoral rejeksiyon varlığının kanıtlanması"],
                        ["Metabolik / Genetik", "Açıklanamayan hepatomegali", "Demir, bakır (Wilson) veya lipid depo hastalığı tespiti"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Biyopsi yaşayan hastadan tanısal amaçla doku/hücre alınmasıdır; otopside ise ölü beden incelenir.",
                "📌 [KLİNİK SPOT] Böbrek ve karaciğer nakillerinde 'rejeksiyon' tanısını koyduran altın standart tanı yöntemi organ biyopsisidir.",
                "💡 [ÖĞRENME İPUCU] Bir lezyondan biyopsi alınırken nekrotik merkez yerine canlı tümörün bulunduğu periferik kenarlar tercih edilmelidir."
            ],
            "medicalTerms": [
                {"term": "Biyopsi", "explanation": "Yaşayan hastadan mikroskobik tanı koymak amacıyla doku veya hücre örneği alınmasıdır."},
                {"term": "Rejeksiyon", "explanation": "Alıcının bağışıklık sisteminin nakledilen organ dokusunu yabancı tanıyıp hasarlamasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Biyopsi vs Otopsi Temel Karşılaştırması",
                    "Biyopsi (Biopsia)",
                    "Otopsi (Autopsia)",
                    [
                        "Yaşayan hastadan teşhis ve tedavi amacıyla alınır",
                        "Milimetrik dokulardan organ parçalarına kadar değişir",
                        "Hastanın tedavi protokolünü ve sağkalımını yönetir",
                        "Cerrahi patoloji laboratuvarında hızla incelenir"
                    ],
                    [
                        "Ölüm sonrasında vefat eden bedenden alınır",
                        "Tüm organ sistemleri bütünüyle diseke edilir",
                        "Ölüm nedenini, klinik tanı doğruluğunu ve adli gerçeği aydınlatır",
                        "Morg ve otopsi salonunda patolog veya adli tıp uzmanınca yapılır"
                    ]
                ),
                make_micro_quiz(
                    "Klinik pratikte biyopsi uygulamalarının temel felsefesi ve hekimi yönlendiren ana kural aşağıdakilerden hangisidir?",
                    {
                        "A": "Lezyonun boyutuna bakılmaksızın daima tüm organın cerrahi olarak çıkarılması",
                        "B": "Hastaya en az invaziv (en düşük morbidite) yöntemle en yüksek tanısal bilginin elde edilmesi",
                        "C": "Tüm biyopsilerin yalnızca genel anestezi altında ameliyathanede yapılması",
                        "D": "Patolojik tanı alınmadan önce doğrudan yüksek doz kemoterapiye başlanması",
                        "E": "Biyopsi parçalarının daima fiksatif konulmadan bekletilmesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Gereksiz organ kaybına yol açacak radikal cerrahi kabul edilemez.",
                        "B": "Doğru. Temel biyopsi ilkesi en az invaziv girişimle en doğru tanısal bilgiyi elde etmektir.",
                        "C": "Yanlış. Çoğu biyopsi poliklinik şartlarında lokal anesteziyle uygulanır.",
                        "D": "Yanlış. Histopatolojik doku tanısı konulmadan kemoterapiye başlanamaz.",
                        "E": "Yanlış. Fiksatifsiz bekleyen dokularda otoliz gelişir."
                    }
                ),
                make_cloze(
                    "Biyopsi kelimesi Yunanca bios (yaşam) ve opsis (görmek) sözcüklerinin birleşiminden türetilmiştir.",
                    "yaşam",
                    "Biyopsi kelimesindeki 'bios' kökünün Türkçe anlamı"
                )
            ]
        },

        # Adım 62
        {
            "slideNumber": 62,
            "title": "İnsizyonel ve Eksizyonel Biyopsi Karşılaştırması",
            "subtitle": "İnsizyonel biyopsi büyük lezyondan tanı amaçlı bir parça alırken; eksizyonel biyopsi lezyonun tamamını sağlam sınırla çıkararak hem tanı hem tedavi sağlar.",
            "badge": "Cerrahi Biyopsiler",
            "badgeColor": "red",
            "discipline": "Cerrahi Patoloji",
            "synthesisNarrative": """Cerrahi pratikte lezyonun boyutu ve yerine göre ==İnsizyonel Biyopsi== ve ==Eksizyonel Biyopsi== olmak üzere iki temel yaklaşım kullanılır.

==1. İnsizyonel Biyopsi (Parça Alma):== Çok büyük veya çevreye yapışık kitlelerde lezyonun yalnızca temsili bir parçasının kesilip alınmasıdır. Temel amaç lezyonu tüketmek değil; histolojik alt tipi öğrenerek neoadjuvan tedavi ve cerrahi planı yapmaktır.
==2. Eksizyonel Biyopsi (Tamamını Çıkarma):== Küçük ve sınırlı lezyonlarda dokunun sağlam çevre sınırı ile birlikte bir bütün halinde çıkarılmasıdır. Hem kesin teşhis koyar hem de lezyonu vücuttan temizleyerek tedavi sağlar.

> [CERRAHİ AYRIM] İnsizyonel biyopside kitle hastada kalır (yalnız tanı); eksizyonel biyopside lezyon bütünüyle çıkarılır (tanı + tedavi).""",
            "coreContent": {
                "keyBullets": [
                    {"title": "İnsizyonel (Parça)", "desc": "Büyük kitlelerden tanı için örnek parça alınır; kitle hastada kalır.", "isKey": True},
                    {"title": "Eksizyonel (Bütün)", "desc": "Küçük lezyon sağlam sınırla tamamen çıkarılır; hem tanı hem tedavi sağlar.", "isKey": True},
                    {"title": "Cerrahi Sınır İncelemesi", "desc": "Eksizyonel biyopside cerrahi sınırların temizliği mutlaka raporlanır.", "isKey": False}
                ],
                "table": {
                    "title": "İnsizyonel ile Eksizyonel Biyopsi Karşılaştırması",
                    "headers": ["Özellik", "İnsizyonel Biyopsi", "Eksizyonel Biyopsi"],
                    "rows": [
                        ["Alınan Doku Miktarı", "Lezyonun temsili bir kısmı veya dilimi", "Lezyonun tamamı + sağlam çevre doku sınırı"],
                        ["Tipik Endikasyon", "Geniş yumuşak doku sarkomları, dev retroperitoneal kitleler", "Küçük deri lezyonları, şüpheli benler, küçük meme nodülleri"],
                        ["Tedavi Edici Rolü", "Tedavi edici değildir; yalnız tanı amaçlıdır", "Hem tanısal hem de tedavi edicidir (küratiftir)"],
                        ["Cerrahi Sınır Raporu", "Raporlanmaz (kitle yerinde bırakılmıştır)", "Mutlaka milimetrik olarak raporlanır (temiz / pozitif)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Eksizyonel biyopsi, lezyonun tamamının sağlam çevre dokuyla birlikte çıkarılmasıdır; hem tanı hem tedavi sağlar.",
                "📌 [SINAV SPOTU] Büyük yumuşak doku kitlelerinde tanı koyup kemoterapi planlamak için insizyonel biyopsi tercih edilir.",
                "🚨 [KRİTİK UYARI] Malign melanom şüphesi olan bir deri lezyonuna asla punch veya traşlama ile eksik insizyonel biyopsi yapılmamalı; sağlam sınırla eksizyonel biyopsi uygulanmalıdır."
            ],
            "medicalTerms": [
                {"term": "İnsizyonel Biyopsi", "explanation": "Büyük kitlelerden tanı amacıyla cerrahi olarak yalnızca temsili bir parça alınmasıdır."},
                {"term": "Eksizyonel Biyopsi", "explanation": "Lezyonun sağlam çevre doku payıyla birlikte tek parça halinde bütünüyle çıkarılmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "İnsizyonel vs Eksizyonel Biyopsi Karşılaştırması",
                    "İnsizyonel Biyopsi",
                    "Eksizyonel Biyopsi",
                    [
                        "Lezyonun sadece bir kısmı teşhis için cerrahi olarak kesilir",
                        "Dev tümörlerde ve sarkomlarda tedavi öncesi tanı için yapılır",
                        "Kitle vücutta bırakıldığı için cerrahi sınır değerlendirilemez",
                        "Yalnızca tanısal amaçlıdır, tedavi edici (küratif) değildir"
                    ],
                    [
                        "Lezyonun tamamı sağlam çevre doku güvenliğiyle çıkarılır",
                        "Küçük deri lezyonları, benler ve meme nodüllerinde uygulanır",
                        "Tümörün cerrahi sınırlara mesafesi mikroskopta ölçülür",
                        "Hem kesin tanı koyar hem de lezyonu temizleyerek tedavi eder"
                    ]
                ),
                make_micro_quiz(
                    "Dermatoloji poliklinik muayenesinde sırtında 8 mm çapında, asimetrik, sınırları düzensiz ve alacalı renk dağılımı gösteren şüpheli bir 'Malign Melanom' lezyonu saptanan hastada uygulanması gereken en doğru biyopsi türü hangisidir?",
                    {
                        "A": "Lezyonun ortasından küçük bir parça koparan insizyonel forseps biyopsi",
                        "B": "Lezyonun tamamını sağlam cerrahi sınırla çıkaran eksizyonel biyopsi",
                        "C": "Yalnızca yüzeyel hücreleri döken eksfolyatif sürüntü",
                        "D": "Lezyonun merkezine yapılan ve mimariyi bozan ince iğne aspirasyonu",
                        "E": "Hiç doku almadan yalnızca 1 yıl sonra takip"
                    },
                    "B",
                    {
                        "A": "Yanlış. İnsizyonel kesi melanomda tümör derinliği (Breslow) ölçümünü bozar.",
                        "B": "Doğru. Melanom şüphesinde lezyon sağlam sınırla eksizyonel çıkarılarak tam evreleme ve tedavi sağlanır.",
                        "C": "Yanlış. Sürüntü sitolojisi invazyon derinliğini ve mimariyi gösteremez.",
                        "D": "Yanlış. İİAS melanomda mikromimariyi ve Breslow kalınlığını veremez.",
                        "E": "Yanlış. Şüpheli melanomda bekleme yaklaşımı mortaliteyi artırır."
                    }
                ),
                make_cloze(
                    "Lezyonun tamamının çevre sağlam doku sınırıyla birlikte çıkarılarak hem tanı hem tedavi sağlayan yönteme eksizyonel biyopsi adı verilir.",
                    "eksizyonel biyopsi",
                    "Lezyonun tümünün çıkarıldığı biyopsi türü"
                )
            ]
        },

        # Adım 63
        {
            "slideNumber": 63,
            "title": "Punch ve Forseps (Endoskopik) Biyopsiler",
            "subtitle": "Punch biyopsi derinin tüm katmanlarını silindirik olarak örneklerken; endoskopik forseps biyopsileri mukoza yüzeyinden milimetrik parçalar koparır.",
            "badge": "Yüzeyel Biyopsiler",
            "badgeColor": "amber",
            "discipline": "Klinik Patoloji",
            "synthesisNarrative": """Poliklinikte en sık uygulanan yüzeyel doku örnekleme yöntemleri ==Punch Biyopsi== ve ==Endoskopik Forseps Biyopsisi==dir.

==1. Punch Biyopsi (Deri Biyopsisi):== Dairesel ve keskin metal bir bıçakla (3-6 mm) uygulanır. En büyük üstünlüğü epidermis, dermis ve subkutan yağ dokusunu tam kat içeren silindirik bir örnek sunmasıdır. Vaskülit, pemfigus ve lupus gibi inflamatuvar dermatozlarda altın standarttır.
==2. Endoskopik Forseps Biyopsisi:== Endoskop çalışma kanalından uzatılan forseps ile lümen mukozasından 1-3 mm'lik parçaların koparılmasıdır. Gastrit, peptik ülser ve kolon poliplerinde kullanılır; yalnızca mukoza ve submukozayı örnekler.

> [PATOLOJİ TUZAĞI] Forseps çenelerinin aşırı basısı hücrelerde ezilme (crush) artefaktına yol açabileceğinden doku nazikçe kasetlenmelidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Punch Biyopsi", "desc": "Epidermis, dermis ve subkutisi içeren tam kat silindirik deri örneği alır.", "isKey": True},
                    {"title": "Forseps Biyopsi", "desc": "Endoskop içinden mukoza yüzeyinden 1-3 mm parçacıklar koparır.", "isKey": True},
                    {"title": "Crush Riski", "desc": "Küçük forseps örneklerinde ezilme artefaktı nükleus morfolojisini bozabilir.", "isKey": False}
                ],
                "table": {
                    "title": "Punch Biyopsi ile Endoskopik Forseps Biyopsisi Karşılaştırması",
                    "headers": ["Parametre", "Punch Biyopsi", "Endoskopik Forseps Biyopsisi"],
                    "rows": [
                        ["Kullanılan Alan", "Dermatoloji (Deri ve mukozalar)", "Gastroenteroloji, Göğüs Hastalıkları, Üroloji"],
                        ["Alet Yapısı", "Dairesel keskin metal silindir (3-6 mm)", "Endoskop kanalından geçen ince çeneli forseps pensi"],
                        ["Örneklenen Katmanlar", "Epidermis + Dermis + Subkutan yağ (Tam kat)", "Yalnızca epitel ve lamina propria (yüzeyel mukoza)"],
                        ["Tipik Hastalıklar", "Lupus, pemfigus, psoriazis, deri lenfoması", "H. pylori gastriti, mide ülseri, kolit, bronş karsinomu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Deri inflamatuvar hastalıklarında (vaskülit, lupus vb.) dermis ve subkutisi içeren tam kat örnek almak için Punch biyopsi kullanılır.",
                "📌 [KLİNİK SPOT] Mide ve kolon endoskopilerinde şüpheli alanlardan forseps biyopsi alınırken ülser tabanındaki nekroz yerine ülser kenarındaki canlı mukoza örneklenmelidir.",
                "💡 [ÖĞRENME İPUCU] Punch biyopside doku silindiri forsepsle sıkılmadan cımbızın ucuyla hafifçe kaldırılarak tabanından neşterle kesilmelidir."
            ],
            "medicalTerms": [
                {"term": "Punch Biyopsi", "explanation": "Derinin tüm katmanlarını içeren silindirik dokunun dairesel bıçakla alınmasıdır."},
                {"term": "Forseps Biyopsisi", "explanation": "Endoskopi forsepsi ile organ mukozasından küçük doku parçalarının koparılmasıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Biyopsi Aleti ve Doku Katmanı İlişkisi",
                    ["Biyopsi Türü", "Uygulama Alanı", "Ulaştığı Doku Derinliği"],
                    [
                        [
                            ("Punch Biyopsi (4 mm)", False),
                            ("Dermatoloji kliniği", True, "Deri lezyonu analizi"),
                            ("Epidermis, dermis ve subkutan yağ dokusu", False)
                        ],
                        [
                            ("Endoskopik Forseps", False),
                            ("Gastroskopi / Kolonoskopi", True, "Lümen içi mukoza örneklemesi"),
                            ("Mukoza epiteli ve yüzeyel lamina propria", False)
                        ],
                        [
                            ("Tru-cut İğne", False),
                            ("Ultrason eşliğinde meme/karaciğer", True, "Derin parankim kor örneği"),
                            ("Derin parankimal doku silindiri", False)
                        ]
                    ]
                ),
                make_cloze(
                    "Epidermis, dermis ve subkutan yağ dokusunu tam kat olarak silindirik biçimde çıkaran deri biyopsi türüne punch biyopsi adı verilir.",
                    "punch biyopsi",
                    "Dermatolojide kullanılan dairesel bıçaklı biyopsi tekniği"
                ),
                make_micro_quiz(
                    "Gastroenteroloji uzmanı kronik karın ağrısı ve kilo kaybı olan bir hastada endoskopi esnasında antrumda derin tabanlı bir ülser görmüştür. Kanser şüphesiyle forseps biyopsisi alırken patolojiye en kaliteli materyali ulaştırmak için nereden örnek almalıdır?",
                    {
                        "A": "Ülserin tabanındaki sarı-beyaz avasküler nekrotik eksüda alanından",
                        "B": "Ülserin kabarmış, sertleşmiş canlı kenar mukozasından",
                        "C": "Yalnızca mide kardiyasındaki sağlam dokudan",
                        "D": "Özofagus skuamöz epitelinden",
                        "E": "Duodenum ampullasından"
                    },
                    "B",
                    {
                        "A": "Yanlış. Nekrotik tabanda yalnızca hücresel döküntüler bulunur ve tanı konulamaz.",
                        "B": "Doğru. Ülserin canlı kenar mukozası tümör invazyonunu ve hücresel atipiyi en iyi gösteren alandır.",
                        "C": "Yanlış. Kardiya sağlam bölgedir, lezyon antrumdadır.",
                        "D": "Yanlış. Özofagus anatomik olarak farklı bir lezyon dışı alandır.",
                        "E": "Yanlış. Lezyon duodenumda değil mide antrumundadır."
                    }
                )
            ]
        },

        # Adım 64
        {
            "slideNumber": 64,
            "title": "Kor (Tru-cut) İğne Biyopsisi: Meme, Karaciğer, Prostat ve Böbrek Dokusu",
            "subtitle": "Tru-cut kalın iğne biyopsisi; özel yaylı mekanizmasıyla organ parankiminden doku mimarisi bozulmamış silindirik kor parçalar çıkarır.",
            "badge": "Tru-cut Biyopsi",
            "badgeColor": "purple",
            "discipline": "Cerrahi Patoloji",
            "synthesisNarrative": """==Kor İğne Biyopsisi (Core Needle / Tru-cut Biyopsi)==; organ parankiminden doku mimarisi, stroması ve hücresel komşulukları korunmuş silindirik şeritler çıkaran kalın iğne yöntemidir.

Genellikle 14-18 Gauge kesici iğnelerle ultrason veya tomografi kılavuzluğunda uygulanır. Başlıca klinik kullanım alanları:
1. ==Meme Kitleleri:== İnvazyonu kanıtlamak ve immünohistokimya ile ER, PR, HER2 reseptörlerini çalışmak için zorunludur.
2. ==Prostat Kanseri:== TRUS eşliğinde korlar alınarak Gleason derecelendirmesi yapılır.
3. ==Böbrek ve Karaciğer:== Glomerülonefrit tanısı ve hepatit fibrozis evrelemesinde altın standarttır.

> [TANI ÜSTÜNLÜĞÜ] Tru-cut biyopsi bazal membran bütünlüğünü ve doku mimarisini koruduğu için in situ ve invaziv karsinom ayrımını kesinleştirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Doku Mimarisi Korunur", "desc": "Hücrelerin yanı sıra stroma ve bazal membran ilişkisi incelenebilir.", "isKey": True},
                    {"title": "Meme Kanserinde Şart", "desc": "İnvazyon kanıtı ve ER/PR/HER2 reseptör analizi için Tru-cut biyopsi altın standarttır.", "isKey": True},
                    {"title": "14-18G Kalın İğne", "desc": "Özel yaylı mekanizmayla 1-2 cm uzunluğunda doku silindiri çıkarır.", "isKey": False}
                ],
                "table": {
                    "title": "Kor (Tru-cut) İğne Biyopsisinin Organlara Göre Rolü",
                    "headers": ["Organ", "Kılavuz Yöntemi", "Patoloğun Aradığı Kritik Bilgi"],
                    "rows": [
                        ["Meme", "Ultrason veya Mamografi (Stereotaktik)", "İn situ vs İnvaziv karsinom ayrımı, histolojik grade, ER/PR/HER2 durumu"],
                        ["Prostat", "Transrektal Ultrason (TRUS)", "Gleason skoru, perinöral invazyon varlığı, tutulan kor yüzdesi"],
                        ["Böbrek", "Ultrason kılavuzluğunda renal korteks", "Glomerül sayısı, kresent varlığı, skleroz oranı, immün kompleksler"],
                        ["Karaciğer", "Ultrason eşliğinde sağ lob", "Portal inflamasyon, arayüz hepatiti ve Masson trikrom ile fibrozis evresi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Meme lezyonlarında invazyonu kanıtlamak ve hormon reseptörlerini (ER, PR, HER2) belirlemek için Tru-cut (kor) biyopsi altın standarttır.",
                "📌 [SINAV SPOTU] Prostat karsinomunun Gleason skorlaması TRUS eşliğinde alınan Tru-cut kor biyopsiler üzerinde yapılır.",
                "💡 [ÖĞRENME İPUCU] İnce iğne (İİAS) hücreleri çekerken, Tru-cut iğnesi doku mimarisini koruyan bir kumaş şeridi gibi kor parça keser."
            ],
            "medicalTerms": [
                {"term": "Tru-cut (Kor) Biyopsi", "explanation": "Geniş lümenli kesici iğneyle doku mimarisini koruyan silindirik kor alma yöntemidir."},
                {"term": "Gleason Skoru", "explanation": "Prostat kanserinde tümör bezlerinin diferansiyasyonunu derecelendiren skor sistemidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "İnce İğne Aspirasyonu (İİAS) vs Kor (Tru-cut) Biyopsi",
                    "İnce İğne Aspirasyonu (İİAS)",
                    "Kor (Tru-cut) Biyopsi",
                    [
                        "22-25 Gauge ince enjektör iğnesi kullanılır",
                        "Yalnızca izole hücreler ve sıvı aspire edilir",
                        "Doku mimarisi ve bazal membran görülmez",
                        "İnvaziv kanser ile in situ kanser ayrımı yapılamaz"
                    ],
                    [
                        "14-18 Gauge kalın kesici yaylı iğne kullanılır",
                        "Doku şeridi (kor) ve stroma bütünüyle çıkarılır",
                        "Doku mimarisi, damarlar ve çevre stroma korunur",
                        "Kanser invazyonu ve İHK reseptör paneli kesinleşir"
                    ]
                ),
                make_micro_quiz(
                    "Memede 2 cm'lik şüpheli spiküle kitle saptanan bir kadında cerrahi öncesi kemoterapi (neoadjuvan) planlanmaktadır. Tümörün invaziv olup olmadığını kanıtlamak ve ER/PR/HER2 reseptörlerini belirlemek için hangisi en uygun biyopsi yöntemidir?",
                    {
                        "A": "Eksfolyatif meme başı akıntısı yayması",
                        "B": "Ultrason eşliğinde Tru-cut (kor) iğne biyopsisi",
                        "C": "Klinik otopsi",
                        "D": "Deri punch biyopsisi",
                        "E": "Yalnızca meme cildine yüzeyel kazıma"
                    },
                    "B",
                    {
                        "A": "Yanlış. Meme başı akıntısı yayması invazyon derinliğini ve reseptör profilini gösteremez.",
                        "B": "Doğru. Tru-cut biyopsi doku mimarisini koruyarak invazyonu kanıtlar ve ER/PR/HER2 testlerine olanak tanır.",
                        "C": "Yanlış. Hasta hayattadır, otopsi uygulanamaz.",
                        "D": "Yanlış. Punch biyopsi deri lezyonları içindir, meme parankimine inemez.",
                        "E": "Yanlış. Yüzeyel kazıma derin parankimal kitleyi örnekleyemez."
                    }
                ),
                make_cloze(
                    "Meme kitlelerinde invaziv karsinom tanısı koymak ve İHK reseptörlerini çalışmak için tercih edilen kalın iğne yöntemine Tru-cut biyopsi adı verilir.",
                    "Tru-cut",
                    "Doku mimarisini koruyan kor biyopsi iğnesinin ticari/klinik adı"
                )
            ]
        },

        # Adım 65
        {
            "slideNumber": 65,
            "title": "İnce İğne Aspirasyon Biyopsisi (İİAS): Hücresel Aspirasyon Prensipleri",
            "subtitle": "İİAS; 22-25G ince iğnelerle kitleye girilerek negatif basınçla tek tek hücrelerin emildiği hızlı, anestezi gerektirmeyen tanı yöntemidir.",
            "badge": "İİAS Tekniği",
            "badgeColor": "cyan",
            "discipline": "Sitopatoloji",
            "synthesisNarrative": """==İnce İğne Aspirasyon Sitolojisi (İİAS / FNAB)==; lezyona enjektör iğnesi ile girilerek negatif basınçla tanısal hücre aspire etme yöntemidir.

İşlemde standart 22 ila 25 Gauge enjektör iğneleri kullanılır. İğne kitleye yönlendirilip piston geri çekilerek negatif basınç oluşturulur ve aspire edilen hücre damlası lam üzerine homojen yayılır.
- ==Tiroid Nodülleri:== Cerrahi gereksinimini belirlemede Bethesda sınıflandırmasıyla dünyadaki ilk basamak yöntemdir.
- ==Lenfadenopatiler ve Tükürük Bezi:== Reaktif süreçler ile lenfoma, metastaz veya adenom ayrımını hızla sağlar.
Deneyimli ellerde tanısal doğruluğu **%90-95** düzeyindedir; anestezi gerektirmemesi ve düşük komplikasyon oranı başlıca avantajlarıdır.

> [KLİNİK İLKE] Tiroid nodülü saptanan bir hastada cerrahi ameliyat kararı verilmeden önce mutlaka minimal invaziv İİAS uygulanmalıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "22-25G İnce İğne", "desc": "Son derece ince iğnelerle doku hasarı ve kanama yaratmadan hücre çekilir.", "isKey": True},
                    {"title": "Tiroidde İlk Seçenek", "desc": "Nodülün benign veya malign olduğunu saptayan ilk basamak tetkiktir.", "isKey": True},
                    {"title": "%90-95 Doğruluk", "desc": "Doğru teknik ve deneyimli sitopatologla cerrahiye yakın güvenilirlik sağlar.", "isKey": False}
                ],
                "table": {
                    "title": "İnce İğne Aspirasyon Sitolojisinin Avantaj ve Sınırları",
                    "headers": ["Parametre", "İİAS Üstünlükleri", "İİAS Kısıtlılıkları"],
                    "rows": [
                        ["İşlem Süresi ve Konfor", "Poliklinikte 5 dakikada yapılır, lokal anestezi bile çoğu zaman gerekmez", "Yetersiz hücresel materyal gelme riski (%5-10) vardır"],
                        ["Maliyet ve Hız", "Çok ucuzdur; aynı gün içinde rapor verilebilir", "Doku mimarisi ve stromayı göstermez"],
                        ["Komplikasyon Oranı", "Hematom ve enfeksiyon riski son derece düşüktür", "Folliküler tiroid karsinomunda kapsül invazyonunu kanıtlayamaz"],
                        ["Kullanım Alanı", "Tiroid nodülü, lenfadenopati, tükürük bezi, kist sıvıları", "Kemik ve sert kalsifiye lezyonlarda hücre çekilemez"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İİAS işleminde rutin olarak 22-25 Gauge ince iğneler kullanılır; tanısal doğruluğu uygun koşullarda %90-95'tir.",
                "📌 [SINAV SPOTU] Tiroid nodüllerinin ayırıcı tanısında ilk tercih edilen altın standart tanı yöntemi İİAS'tır.",
                "🚨 [KRİTİK UYARI] Tiroid folliküler adenom ile folliküler karsinom ayrımı İİAS ile yapılamaz; çünkü kapsül ve damar invazyonu için cerrahi doku kesiti şarttır."
            ],
            "medicalTerms": [
                {"term": "İİAS (İnce İğne Aspirasyon Sitolojisi)", "explanation": "İnce enjektör iğnesi ve negatif basınçla kitlelerden hücresel örnekleme yöntemidir."},
                {"term": "Bethesda Sistemi", "explanation": "Tiroid İİAS sonuçlarını kanser riskine göre 6 grupta standardize eden tanı sistemidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İİAS Uygulama ve Değerlendirme Zinciri",
                    [
                        "1. Hedef Belirleme: Boyundaki nodül palpasyon veya ultrason kılavuzluğunda sabitlenir.",
                        "2. Vakumla Aspirasyon: 22 Gauge iğne nodüle sokulup negatif basınçla hücreler çekilir.",
                        "3. Lam Yayması: İğne lümenindeki hücresel damla lam üzerine aktarılarak yayılır.",
                        "4. Fiksasyon: Lamların bir kısmı havada kurutulur, diğer kısmı %95 alkole atılır.",
                        "5. Sitolojik Raporlama: Nükleer atipi ve hücresel mimari incelenerek tanı verilir."
                    ]
                ),
                make_micro_quiz(
                    "Boynunda 2 cm soliter tiroid nodülü palpe edilen 35 yaşındaki bir hastada nodülün iyi huylu mu yoksa ameliyat gerektiren bir malignite mi olduğunu netleştirmek için poliklinikte yapılacak ilk basamak tanı yöntemi hangisidir?",
                    {
                        "A": "Doğrudan total tiroidektomi ameliyatı",
                        "B": "İnce İğne Aspirasyon Sitolojisi (İİAS)",
                        "C": "Boyun cildinden punch biyopsi",
                        "D": "Klinik otopsi",
                        "E": "Kemik iliği aspirasyonu"
                    },
                    "B",
                    {
                        "A": "Yanlış. Tanısal biyopsi yapılmadan doğrudan radikal tiroidektomi yapılamaz.",
                        "B": "Doğru. Tiroid nodüllerinin ayırıcı tanısında ilk tercih edilen yüksek doğruluklu minimal invaziv tetkik İİAS'tır.",
                        "C": "Yanlış. Punch biyopsi deri lezyonları içindir, tiroid parankiminde kullanılmaz.",
                        "D": "Yanlış. Hasta hayattadır, otopsi endikasyonu yoktur.",
                        "E": "Yanlış. Kemik iliği aspirasyonu tiroid patolojilerinde tanısal değildir."
                    }
                ),
                make_cloze(
                    "Tiroid nodüllerinde minimal travmayla hücre toplayan ince iğne aspirasyon sitolojisinde standart olarak 22 gauge kalınlığında iğneler kullanılır.",
                    "22",
                    "İİAS'ta en sık kullanılan standart iğne gauge numarası"
                )
            ]
        },

        # Adım 66
        {
            "slideNumber": 66,
            "title": "Materyal Kabulü, Kimlik Doğrulama ve Barkodlama Güvenliği",
            "subtitle": "Preanalitik laboratuvar güvenliği; en az iki bağımsız hasta kimlik bilgisi, benzersiz barkod protokol numarası ve zincirleme takip ile sağlanır.",
            "badge": "Hasta Güvenliği",
            "badgeColor": "red",
            "discipline": "Laboratuvar Güvenliği",
            "synthesisNarrative": """Patoloji laboratuvarında en kritik risk preanalitik evredeki ==materyal veya hasta kimliği karışıklıklarıdır==.

Hasta güvenliğini sağlamak amacıyla numune kabulünde tavizsiz şu standartlar uygulanır:
1. ==Çift Bağımsız Kimlik:== İstek formu ve numune kabında ad-soyad ile birlikte mutlaka TC Kimlik No veya benzersiz Dosya No bulunmalıdır; oda numarası yetersizdir.
2. ==Gövdeye Etiketleme:== Kapaklar açıldığında yer değiştirebileceğinden etiket asla kapağa değil, mutlaka kabın plastik gövdesine yapıştırılır.
3. ==Tekil Barkod Protokolü:== Kabulde verilen benzersiz numara, kimyasala dirençli barkod yazıcılarla kaset ve lamlara işlenir.

> [GÜVENLİK KURALI] Kimlik bilgisi eksik, çelişkili veya etiketsiz gelen hiçbir numune işleme alınmaz; tutanak tutularak kliniğe iade edilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Çift Kimlik Doğrulama", "desc": "Ad-soyad ve T.C. Kimlik / Dosya Numarası zorunludur.", "isKey": True},
                    {"title": "Gövdeye Etiketleme", "desc": "Etiket kapağa değil, mutlaka kabın gövdesine yapıştırılır.", "isKey": True},
                    {"title": "Lazer Barkod Baskısı", "desc": "Kaset ve lamlar ksilende silinmeyen kalıcı barkodlarla takip edilir.", "isKey": False}
                ],
                "table": {
                    "title": "Preanalitik Kabulde Kritik Güvenlik Denetimleri",
                    "headers": ["Güvenlik Basamağı", "Hatalı Uygulama", "Doğru Protokol", "Önlenen Kritik Risk"],
                    "rows": [
                        ["Numune Kabı Etiketi", "Etiketin kabın çıkarılabilir kapağına yapıştırılması", "Etiketin doğrudan numune kabının plastik gövdesine yapıştırılması", "Kapaklar açılınca numunelerin karışması önlenir"],
                        ["Kimlik Bilgisi", "Yalnızca 'Yatak 4 - Ahmet Bey' yazılması", "Ad, Soyad, TC Kimlik No ve Doğum Tarihinin tam yazılması", "Aynı isimli hastaların raporlarının karışması önlenir"],
                        ["Doku Kaseti İşareti", "Kaset üzerine kurşun veya tükenmez kalemle numara yazma", "Kimyasala dirençli lazer barkod yazıcıyla baskı", "Ksilen banyosunda numaranın silinip dokunun kaybolması önlenir"],
                        ["Çoklu Biyopsi", "Aynı hastanın 3 farklı odağını aynı kaba koyma", "Her odağı 'Kadran A, B, C' diye ayrı kaplara koyup etiketleme", "Hangi odakta tümör olduğunun anlaşılamaması önlenir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [GÜVENLİK SPOTU] Numune etiketi asla kabın kapağına yapıştırılamaz; daima kabın gövdesine yapıştırılmalıdır.",
                "📌 [SINAV SPOTU] Patolojide preanalitik kimlik doğrulamada en az iki bağımsız parametre (Ad-Soyad ve TC Kimlik No) bulunması şarttır.",
                "🚨 [KRİTİK UYARI] Kaset üzerine tükenmez kalemle yazılan numaralar doku takibindeki alkol ve ksilende tamamen silinir."
            ],
            "medicalTerms": [
                {"term": "Barkod Protokol Numarası", "explanation": "Materyalin kaset ve lam üzerinde kimyasala dirençle takibini sağlayan tekil koddur."},
                {"term": "Kimlik Doğrulayıcı (Identifier)", "explanation": "Hastayı kesin ayırt etmekte kullanılan ad-soyad veya TC kimlik no gibi bağımsız veridir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Patoloji laboratuvarı kabul sekreteryasına kapağına sadece 'Mide Biyopsisi - Mehmet' yazılmış etiketsiz bir kap gelmesi senaryosu.",
                    [
                        {
                            "text": "Materyal hemen doku takibine alınır, rapor çıkınca servise sorulup hasta adı öğrenilir.",
                            "isCorrect": False,
                            "feedback": "Ağır hata! Bu uygulama hastaların karışmasına ve malpraktise yol açar; etiketsiz numune asla işleme alınamaz."
                        },
                        {
                            "text": "Numune kabulü durdurulur; gönderen klinik ve hekim derhal aranarak resmi tutanak tutulur, iki bağımsız kimlikle etiketlenmesi sağlanır.",
                            "isCorrect": True,
                            "feedback": "Mükemmel hasta güvenliği kararı! İki bağımsız kimlik doğrulanmadan ve tutanak düzenlenmeden hiçbir doku kabul edilemez."
                        },
                        {
                            "text": "Materyal çöpe atılır ve kliniğe haber verilmez.",
                            "isCorrect": False,
                            "feedback": "Hukuken kabul edilemez! Hastadan alınan biyopsi geri dönüşü olmayan bir dokudur, derhal klinikle iletişime geçilmelidir."
                        }
                    ]
                ),
                make_cloze(
                    "Numunelerin laboratuvarda kapak açılması sırasında karışmasını önlemek için etiket kapağa değil daima kabın gövdesine yapıştırılmalıdır.",
                    "gövdesine",
                    "Etiketin yapıştırılması gereken doğru yer"
                ),
                make_micro_quiz(
                    "Patoloji laboratuvarında preanalitik kabul aşamasında numune kaplarının etiketlenmesi ile ilgili aşağıdaki kurallardan hangisi HASTA GÜVENLİĞİ AÇISINDAN ZORUNLUDUR?",
                    {
                        "A": "Etiket daima kabın kapağına yapıştırılmalıdır.",
                        "B": "Etikette sadece hastanın yattığı oda numarası bulunması yeterlidir.",
                        "C": "Etiket kabın gövdesine yapıştırılmalı ve en az iki bağımsız hasta kimlik bilgisi (Ad-Soyad ve TC No) içermelidir.",
                        "D": "Kaset numaraları standart tükenmez kalemle yazılmalıdır.",
                        "E": "Farklı organlardan alınan parçalar aynı kaba konulmalıdır."
                    },
                    "C",
                    {
                        "A": "Yanlış. Kapak açıldığında kapaklar yer değiştirebilir ve hastalar karışır.",
                        "B": "Yanlış. Oda ve yatak numarası dinamiktir, bağımsız kimlik parametresi sayılmaz.",
                        "C": "Doğru. Gövdeye etiketleme kapak karışmasını önler; en az iki bağımsız kimlik hasta güvenliğini garanti eder.",
                        "D": "Yanlış. Tükenmez kalem doku takibindeki organik çözücülerde silinir.",
                        "E": "Yanlış. Farklı organ odakları mutlaka ayrı kaplarda etiketlenmelidir."
                    }
                )
            ]
        },

        # Adım 67
        {
            "slideNumber": 67,
            "title": "Patoloji İstek Formunun Önemi ve Eksik Bilginin Riskleri",
            "subtitle": "İstek formu; patoloğa hastanın yaşını, lezyonun yerini, operasyon bulgularını ve geçmiş tedavi öyküsünü aktaran vazgeçilmez pusuladır.",
            "badge": "İstek Formu",
            "badgeColor": "indigo",
            "discipline": "Klinik Patoloji",
            "synthesisNarrative": """Cerrahi patolojide hekim ile patolog arasındaki temel iletişim köprüsü ==Patoloji İstek Formu==dur.

Eksiksiz bir istek formunda mutlaka bulunması gereken klinik veriler:
1. ==Hasta Demografisi ve Lokalizasyon:== Hastanın yaşı, cinsiyeti ve lezyonun tam anatomik odağı (örneğin 'sol meme üst dış kadran').
2. ==Operasyon ve Radyoloji Bulguları:== Kitlenin boyutu, invazyon şüphesi ve görüntüleme özellikleri.
3. ==Geçmiş Tedavi Öyküsü:== Geçirilmiş radyoterapi ve kemoterapi dokuda **radyasyon atipisi** oluşturur; bu bilgi verilmezse reaktif hücreler malign karsinom sanılabilir.
4. ==Hormonal Durum ve SAT:== Endometrium biyopsisinde son adet tarihi histolojik fazın yorumlanmasını sağlar.

> [TIBBİ VE HUKUKİ İLKE] Eksik klinik bilgi tanı sürecini geciktirir ve patoloğu yanıltıcı veya hatalı kanser tanısı tuzağına düşürebilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Yaş ve Lokalizasyon", "desc": "Yaş ve kesin organ odağı ayırıcı tanı listesini tamamen değiştirir.", "isKey": True},
                    {"title": "Tedavi Öyküsü Hayatidir", "desc": "Geçirilmiş radyoterapi atipik hücreler yapar; belirtilmezse kanserle karışır.", "isKey": True},
                    {"title": "Özel Soru İletimi", "desc": "Tüberküloz, mantar veya vaskülit şüphesi özel boyaları tetikler.", "isKey": False}
                ],
                "table": {
                    "title": "İstek Formundaki Bilgilerin Patolojik Tanıya Doğrudan Etkisi",
                    "headers": ["İstek Formu Parametresi", "Eksik Olmasının Doğuracağı Ağır Risk", "Klinik Neden"],
                    "rows": [
                        ["Hasta Yaşı", "Pediatrik küçük yuvarlak hücreli tümör ile yetişkin karsinomu ayrımının gecikmesi", "Nöroblastom ve Wilms çocukta, karsinomlar yaşlıda sıktır"],
                        ["Geçirilmiş Radyoterapi", "Radyasyona bağlı atipik fibroblastların 'nüks sarkom' sanılması", "İyonize radyasyon hücre çekirdeklerinde pleomorfik devleşme yapar"],
                        ["Son Adet Tarihi (SAT)", "Endometrium biyopsisinde normal fazın 'endometrial hiperplazi' sanılması", "Proliferatif ve sekretuar fazlar adet gününe göre yorumlanır"],
                        ["Kortikosteroid Kullanımı", "Temporal arterit veya böbrek glomerülonefritinde yangının baskılanıp negatif çıkması", "İlaç inflamasyonu sildiği için patolog yanıltıcı temiz rapor verebilir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Radyoterapi almış dokulardaki 'radyasyon atipisi' malign karsinomu taklit edebilir; klinisyenin bu öyküyü formda belirtmesi zorunludur.",
                "📌 [KLİNİK SPOT] Endometrium biyopsilerinde son adet tarihi (SAT) ve hormon ilacı kullanımı istek formunda mutlaka yazılmalıdır.",
                "🚨 [KRİTİK UYARI] İstek formunda klinik ön tanısı ve lokalizasyonu yazılmayan dokular patoloji uzmanı tarafından bekletilerek kliniğe ek bilgi sorulur."
            ],
            "medicalTerms": [
                {"term": "Radyasyon Atipisi", "explanation": "İyonize radyoterapi sonrası hücrelerde kanseri taklit eden reaktif nükleer devleşmedir."},
                {"term": "Klinik Ön Tanı", "explanation": "Klinisyenin muayene ve görüntüleme verileriyle oluşturup patoloğa ilettiği olası tanıdır."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "İstek formunda hastanın daha önce radyoterapi aldığının belirtilmemesi patoloji uzmanını mikroskop başında hangi ölümcül tanısal tuzağa düşürebilir?",
                    "Radyoterapi sonrası hücrelerde oluşan reaktif nükleer büyüme ve hiperkromazi (radyasyon atipisi), malign karsinom veya sarkomu taklit edebilir. Öykü bilinmediğinde bu iyi huylu atipik hücreler yanlışlıkla nüks kanser olarak raporlanabilir."
                ),
                make_micro_quiz(
                    "Patoloji istek formuna 'Son Adet Tarihi (SAT)' bilgisinin yazılması aşağıdaki biyopsi türlerinden hangisinin doğru histopatolojik evrelenmesi için en kritiktir?",
                    {
                        "A": "Tiroid ince iğne aspirasyonu",
                        "B": "Endometrium küretaj biyopsisi",
                        "C": "Karaciğer kor biyopsisi",
                        "D": "Deri punch biyopsisi",
                        "E": "Beyin tümörü rezeksiyonu"
                    },
                    "B",
                    {
                        "A": "Yanlış. Tiroid foliküler hücreleri menstrüel siklus gününe göre histolojik değişiklik göstermez.",
                        "B": "Doğru. Endometrium siklusun gününe göre proliferatif veya sekretuar faza girer; SAT bilinmezse normal sekretuar faz hiperplaziyle karışabilir.",
                        "C": "Yanlış. Karaciğer parankim mimarisi adet döngüsünden doğrudan etkilenmez.",
                        "D": "Yanlış. Deri histopatolojisinde SAT belirleyici bir parametre değildir.",
                        "E": "Yanlış. Beyin tümörlerinde hormonal siklus günü aranmaz."
                    }
                ),
                make_cloze(
                    "İyonize radyasyon tedavisi görmüş dokularda kanser hücrelerini taklit eden yalancı malign çekirdek değişimlerine radyasyon atipisi adı verilir.",
                    "radyasyon atipisi",
                    "Radyoterapi sonrası oluşan kanser benzeri hücresel değişiklik terimi"
                )
            ]
        },

        # Adım 68
        {
            "slideNumber": 68,
            "title": "Laboratuvar Biyogüvenliği ve Formaldehit Maruziyeti",
            "subtitle": "Patoloji çalışanları; formaldehitin kanserojen buharlarına ve taze dokulardaki enfeksiyöz patojenlere karşı biyogüvenlik kabinleri ve koruyucularla korunur.",
            "badge": "Biyogüvenlik",
            "badgeColor": "amber",
            "discipline": "İş Sağlığı ve Güvenliği",
            "synthesisNarrative": """Patoloji laboratuvarı hem kimyasal toksisite hem de biyolojik enfeksiyon risklerinin yoğunlaştığı bir çalışma ortamıdır.

Güvenlik yönetimi iki ana eksende yürütülür:
==1. Formaldehit ve Ksilen Toksisitesi:== Fiksasyonda kullanılan formaldehit gazı ($CH_2O$), IARC tarafından **Grup 1 Kesin İnsan Kanserojeni** (nazofarenks kanseri ve myeloid lösemi) kabul edilmiştir. Diseksiyon masaları mutlaka hava emişli **çeker ocak (fume hood)** sistemine sahip olmalı, nitril eldiven ve uygun maskeler kullanılmalıdır.
==2. Biyolojik Enfeksiyon:== Fikse edilmemiş taze dokular (frozen kesit, lenf nodu) HBV, HCV, HIV ve tüberküloz gibi canlı patojenleri barındırır; kriostatta aerosol bariyerleri şarttır.

> [HAYATİ İLKE] Formaldehit buharları açık ortamda solunamaz; çeker ocak çalıştırılmadan hiçbir numune kabı açılamaz.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Grup 1 Kanserojen", "desc": "Formaldehit nazofarenks kanseri ve lösemi riski taşıyan kesin kanserojendir.", "isKey": True},
                    {"title": "Çeker Ocak Şartı", "desc": "Tüm makroskobik diseksiyonlar hava tahliyeli çeker ocaklarda yapılır.", "isKey": True},
                    {"title": "Taze Doku Enfeksiyonu", "desc": "Frozen kesitte tüberküloz ve viral hepatit bulaşma riski çok yüksektir.", "isKey": False}
                ],
                "table": {
                    "title": "Patoloji Laboratuvarı Riskleri ve Korunma Standartları",
                    "headers": ["Tehlike Kaynağı", "Toksik / Biyolojik Etki", "Uluslararası Güvenlik Önlemi"],
                    "rows": [
                        ["Formaldehit Gazı", "Göz/solunum iritasyonu, IARC Grup 1 Kanserojen (Nazofarenks Ca, Lösemi)", "Laminer akımlı çeker ocak, kimyasal buhar maskesi, ortam ppm dedektörü"],
                        ["Ksilen Solventi", "Santral sinir sistemi depresyonu, baş dönmesi, kemik iliği toksisitesi", "Kapalı sistem doku takip cihazları, kimyasal dayanıklı nitril eldiven"],
                        ["Taze Dokular (Frozen)", "Hepatit B/C, HIV, Tüberküloz basili bulaşı", "Kesilmeye dirençli çelik örgü eldiven, N95 maske, kriostat UV dezenfeksiyonu"],
                        ["Mikrotom Jiletleri", "Derin kesici delici yaralanmalar ve kan yoluyla bulaş", "Bıçak koruma kilitleri, manyetik jilet tutucular, tıbbi atık kutuları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Formaldehit, IARC tarafından Grup 1 kesin insan kanserojeni olarak kabul edilmiştir (nazofarenks kanseri ve lösemi ilişkisi).",
                "📌 [GÜVENLİK SPOTU] Patolojide makroskobik inceleme ve doku açma işlemleri mutlaka hava emişli 'çeker ocak' (fume hood) altında yapılmalıdır.",
                "🚨 [KRİTİK UYARI] Tüberküloz şüpheli akciğer dokuları frozen kesit için dondurulurken aerosol yayılımı nedeniyle havaya basiller saçılabilir; azami biyogüvenlik gerekir."
            ],
            "medicalTerms": [
                {"term": "Çeker Ocak (Fume Hood)", "explanation": "Zararlı kimyasal buharları çalışma ortamından emerek tahliye eden hava emişli kabindir."},
                {"term": "IARC Grup 1", "explanation": "İnsanlarda kanser yapıcı etkisi kesin olarak kanıtlanmış kimyasal etkenler grubudur."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Formaldehit Maruziyeti ve Güvenlik Protokolü Zinciri",
                    [
                        "1. Numune Açılışı: Numune kabı hava tahliyesi devrede olan çeker ocak içinde açılır.",
                        "2. Buhar Tahliyesi: Uçucu formaldehit gazı emiş kanallarıyla personelden uzaklaştırılır.",
                        "3. Kişisel Koruma: Diseksiyon esnasında kimyasal koruyucu gözlük ve nitril eldiven kullanılır.",
                        "4. Atık Yönetimi: Kullanılmış formalin solüsyonları kimyasal atık bidonlarında toplanır.",
                        "5. Periyodik Takip: Personel sağlık taramaları ve ortam gaz ölçümleri düzenli yapılır."
                    ]
                ),
                make_micro_quiz(
                    "Patoloji laboratuvarında fiksasyon amacıyla rutin olarak kullanılan formaldehit (formalin) kimyasalı ile ilgili aşağıdaki ifadelerden hangisi BİYOGÜVENLİK AÇISINDAN DOĞRUDUR?",
                    {
                        "A": "Tamamen zararsız doğal bir gazdır, oda içinde serbestçe buharlaşabilir.",
                        "B": "IARC tarafından Grup 1 kesin insan kanserojeni kabul edilmiştir; makroskopi daima çeker ocak altında yapılmalıdır.",
                        "C": "Kullanılmış atık formalin doğrudan şehir kanalizasyonuna dökülmelidir.",
                        "D": "Formaldehit taze dokulardaki tüm virüsleri saniyeler içinde yok ettiğinden eldivensiz tutulabilir.",
                        "E": "Formaldehit buharları akciğer sağlığını güçlendirici etkiye sahiptir."
                    },
                    "B",
                    {
                        "A": "Yanlış. Formaldehit son derece toksik, irritan ve kanserojen bir gazdır.",
                        "B": "Doğru. Formaldehit IARC Grup 1 insan kanserojenidir ve mutlaka hava tahliyeli çeker ocak altında işlenmelidir.",
                        "C": "Yanlış. Formalin kanalizasyona dökülemez, özel kimyasal atık protokolüyle toplanmalıdır.",
                        "D": "Yanlış. Fiksasyon yavaş bir kimyasal süreçtir, taze dokular bulaşıcı patojen barındırabilir.",
                        "E": "Yanlış. Formaldehit buharları solunum yollarında kronik hasar ve irritasyon yapar."
                    }
                ),
                make_cloze(
                    "Formaldehit buharlarını laboratuvar ortamından uzaklaştırmak için makroskobik diseksiyon masalarında çeker ocak adı verilen havalandırma kabinleri kullanılır.",
                    "çeker ocak",
                    "Zararlı kimyasal buharları tahliye eden emişli laboratuvar kabini"
                )
            ]
        },

        # Adım 69: [TEKRAR SAYFASI - CHECKPOINT 7]
        {
            "slideNumber": 69,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Materyal Tipleri, Biyopsiler ve Preanalitik Güvenlik",
            "subtitle": "Bölüm 7'nin biyopsi tipleri (insizyonel, eksizyonel, punch, tru-cut, İİAS), hasta güvenliği, istek formu ve formaldehit biyogüvenliğini sentezleyen istasyon.",
            "badge": "Checkpoint 7",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 7,
            "synthesisNarrative": """Bu kontrol noktası; lezyona uygun biyopsi seçimini, hasta kimlik güvenliğini ve laboratuvar biyogüvenlik prensiplerini sentezler.

Biyopsi stratejisi klinik hedefe göre belirlenir:
- Meme ve prostatta invazyon ve reseptör analizi için ==Tru-cut (kor) biyopsi==,
- Tiroid nodüllerinde poliklinik ilk basamak taraması için ==İİAS (22-25G)==,
- Deri inflamatuvar lezyonlarında tüm katmanları incelemek için ==Punch biyopsi==,
- Küçük lezyonlarda tanı ve tedavi amacıyla sağlam sınırlı ==Eksizyonel biyopsi==,
- Dev kitlelerde tedavi öncesi tanı koymak için ==İnsizyonel biyopsi==.
Preanalitik güvenliğin temeli ise kabın gövdesine yapıştırılan çift kimlikli etiket ve çeker ocak disiplinidir.

> [BÖLÜM ÖZETİ] Doğru biyopsi tekniği + Gövdeye çift kimlikli etiket + Ayrıntılı klinik bilgi + Çeker ocak disiplini = Hatasız patoloji süreci.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Biyopsi Endikasyon Haritası", "desc": "Meme/prostat: Tru-cut; Tiroid: İİAS; Deri: Punch; Küçük kitle: Eksizyonel; Dev kitle: İnsizyonel.", "isKey": True},
                    {"title": "Preanalitik Kural", "desc": "Etiket kapağa değil gövdeye yapıştırılır; istek formunda radyoterapi öyküsü zorunludur.", "isKey": True},
                    {"title": "Biyogüvenlik Standardı", "desc": "Formaldehit IARC Grup 1 kanserojendir; çeker ocak kullanımı hayati zorunluluktur.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 7 Biyopsi Yöntemleri ve Laboratuvar Standartları Sentez Tablosu",
                    "headers": ["Yöntem / Standart", "Kullanılan Alet / Özellik", "Temel Endikasyon", "Patolojik Kritik Kural"],
                    "rows": [
                        ["İnsizyonel Biyopsi", "Cerrahi neşter / kama kesi", "Dev sarkomlar ve kitleler", "Yalnızca tanı amaçlıdır, kitle hastada kalır"],
                        ["Eksizyonel Biyopsi", "Cerrahi rezeksiyon", "Küçük pigmente benler, nodüller", "Hem tanı hem tedavidir, cerrahi sınırlar raporlanır"],
                        ["Punch Biyopsi", "Dairesel metal bıçak (3-6 mm)", "Lupus, vaskülit, pemfigus", "Epidermis, dermis ve subkutan yağ tam kat alınır"],
                        ["Tru-cut Biyopsi", "14-18G kesici yaylı iğne", "Meme kanseri, prostat, karaciğer", "Doku mimarisini korur; invazyon ve İHK reseptörleri belirlenir"],
                        ["İİAS Sitolojisi", "22-25G enjektör iğnesi", "Tiroid nodülü, lenfadenopati", "Doku mimarisi görülmez; hücre nükleus atipisi taranır"],
                        ["Gövdeye Etiketleme", "İki bağımsız kimlik (Ad-Soyad, TC)", "Tüm numune kapları", "Kapak karışıklığına bağlı malpraktisi önler"],
                        ["Çeker Ocak", "Laminer hava tahliyeli kabin", "Formaldehit makroskopi masası", "Grup 1 kanserojen formaldehit gazından personeli korur"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Meme kanserinde invazyonu ve ER/PR/HER2 reseptör durumunu kanıtlayan altın standart biyopsi Tru-cut (kor) biyopsisidir.",
                "📌 [SINAV SPOTU] Tiroid nodülünde ilk seçenek 22G iğneyle yapılan İİAS'tır; folliküler adenom-karsinom ayrımını yapamaz.",
                "📌 [GÜVENLİK SPOTU] Numune kabı etiketi asla kapağa yapıştırılamaz, kabın gövdesine yapıştırılmalıdır."
            ],
            "medicalTerms": [
                {"term": "Crush Artefaktı", "explanation": "Küçük biyopsilerde forseps basısıyla hücre çekirdeklerinin ezilerek bozulmasıdır."},
                {"term": "Sampling Hatası", "explanation": "Heterojen tümörün nekrotik veya yanlış bölgesinden parça alınarak ıskalanmasıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p7-1",
                    "Meme kitlelerinde İnce İğne Aspirasyon Sitolojisine (İİAS) kıyasla Tru-cut (kor) biyopsinin en büyük onkolojik üstünlükleri nelerdir?",
                    "İİAS yalnızca serbest hücreleri çeker ve bazal membran mimarisini gösteremez (in situ ile invaziv kanseri ayıramaz). Tru-cut biyopsi ise doku mimarisini ve stromayı koruyarak kanser invazyonunu kesin olarak kanıtlar; ayrıca parafin blokta ER, PR ve HER2 reseptör panellerinin çalışılmasını sağlar.",
                    "İnvazyon kanıtı ve İHK reseptörleri",
                    "Cerrahi Biyopsiler"
                ),
                make_flashcard(
                    "fc-p7-2",
                    "Patoloji laboratuvarına gönderilen numune kaplarında etiketin kapağa değil, mutlaka kabın gövdesine yapıştırılmasının hasta güvenliği açısından gerekçesi nedir?",
                    "Laboratuvarda aynı anda birden fazla hastanın numune kapları açıldığında kapaklar yer değiştirebilir. Etiket kapakta olursa kapak başka hastanın kabına kapatıldığında kimlikler karışır; bu durum sağlıklı bir hastaya yanlışlıkla kanser tanısı verilmesine yol açabilecek ölümcül bir preanalitik hatadır.",
                    "Kapak değişimi ve kimlik karışması riski",
                    "Hasta Güvenliği"
                ),
                make_flashcard(
                    "fc-p7-3",
                    "Formaldehit gazının insan sağlığı üzerindeki en ağır uzun vadeli riski nedir ve bu risk laboratuvarda hangi mühendislik önlemiyle bertaraf edilir?",
                    "Formaldehit IARC tarafından Grup 1 kesin insan kanserojeni olarak kabul edilmiştir; uzun süreli solunması nazofarenks karsinomu ve miyeloid lösemiye yol açar. Bu risk, makroskopi masalarında formaldehit buharlarını hekimden uzağa tahliye eden hava emişli 'çeker ocak' (fume hood) sistemleri kullanılarak önlenir.",
                    "Grup 1 kanserojen ve çeker ocak tahliyesi",
                    "Laboratuvar Biyogüvenliği"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 7'de incelenen biyopsi çeşitleri ve laboratuvar güvenliği prensipleri dikkate alındığında, aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                    {
                        "A": "Tiroid soliter nodülünde poliklinik ilk basamak tanı yöntemi → İnce İğne Aspirasyon Sitolojisi (İİAS)",
                        "B": "Şüpheli displastik pigmente deri beninin sağlam sınırla çıkarılması → Eksizyonel Biyopsi",
                        "C": "Vaskülit şüpheli deri lezyonunda epidermis ve subkutan yağın tam kat alınması → Punch Biyopsi",
                        "D": "Meme kitlesinde invazyon tespiti ve ER/PR/HER2 analizi → Tru-cut (kor) Biyopsi",
                        "E": "Dondurularak acil intraoperatif incelenecek frozen dokusunun taşınması → %10 Formalin içinde 24 saat bekletilerek"
                    },
                    "E",
                    {
                        "A": "Doğru. İİAS tiroid nodüllerinde ilk basamak minimal invaziv tanı aracıdır.",
                        "B": "Doğru. Eksizyonel biyopsi lezyonun tamamını sağlam sınırla çıkararak hem tanı hem tedavi sağlar.",
                        "C": "Doğru. Punch biyopsi epidermis, dermis ve subkutan dokuyu tam kat silindirik örnekler.",
                        "D": "Doğru. Tru-cut biyopsi doku mimarisini koruyarak invazyonu kanıtlar ve reseptör analizine izin verir.",
                        "E": "Yanlış (aranan cevap): Frozen kesit dokuları kesinlikle formaline konulmaz; taze olarak dondurulmak üzere ulaştırılır."
                    }
                ),
                make_interactive_table(
                    "Biyopsi Endikasyonu ve Yöntem Karşılaştırması",
                    ["Klinik Senaryo", "Seçilen Biyopsi", "Kritik Patolojik Hedef"],
                    [
                        [
                            ("Meme karsinomu şüphesi", False),
                            ("Tru-cut İğne Biyopsisi", True, "Doku mimarisi koruma"),
                            ("İnvazyon kanıtı ve ER/PR/HER2 tayini", False)
                        ],
                        [
                            ("Tiroid soğuk nodülü", False),
                            ("İnce İğne Aspirasyonu (İİAS)", True, "22G ince iğne aspiratı"),
                            ("Hızlı sitolojik benign/malign ayrımı", False)
                        ],
                        [
                            ("Deri vasküliti", False),
                            ("Punch Biyopsi (4 mm)", True, "Tam kat dairesel deri örneği"),
                            ("Dermis ve subkutis damarlarının analizi", False)
                        ]
                    ]
                )
            ]
        }
    ]
