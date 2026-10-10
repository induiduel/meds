# -*- coding: utf-8 -*-
"""
Deck 61 Section 6: Missed Abortus ve TV-USG Tanı Kriterleri
Slides 51-60 (Checkpoint 6 at slide 60)
Focus:
- Missed abortus (gecikmiş düşük) tanımı: Viabilitesini (canlılığını) yitirmiş gebeliğin uterusta birden fazla hafta (>1 hafta) kalması
- Missed abortus klinik prezantasyonu: Uterusun beklenen gebelik haftasından küçük olması, gebelik semptomlarının gerilemesi, hafif lekelenme
- Missed abortus laboratuvar bulguları: Gebelik testi pozitif (+) kalabilir ancak B-hCG değerleri düşüş trendindedir
- TV-USG Gebelik kaybını düşündüren (tanısal olmayan) bulgular 1: CRL <7 mm ve kalp atımı yokluğu; ortalama kese çapı (MSD) 16-24 mm ve embriyo yokluğu
- TV-USG Gebelik kaybını düşündüren (tanısal olmayan) bulgular 2: Yolk kesesiz keseden 7-13 gün sonra veya yolk keseli keseden 7-10 gün sonra embriyo/FKA yokluğu
- TV-USG Gebelik kaybını düşündüren (tanısal olmayan) bulgular 3: SAT'tan ≥6 hafta sonra embriyo yokluğu, boş amnion, büyümüş yolk kesesi (>7 mm), MSD ile CRL farkı <5 mm
- TV-USG Gebelik kaybı KESİN TANI koyduran bulgular 1: CRL ≥7 mm ve kalp atımı yokluğu; ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğu
- TV-USG Gebelik kaybı KESİN TANI koyduran bulgular 2: Yolk kesesiz keseden ≥2 hafta veya yolk keseli keseden ≥11 gün sonra embriyo ve FKA yokluğu
- Missed abortus komplikasyonları ve yönetimi: Dissemine intravasküler koagülasyon (DIC) riski, bekleme vs medikal (misoprostol) vs cerrahi tahliye
- Checkpoint 6 (Tekrar ve pekiştirme sayfası)
"""

from meds.scripts.deck_generators.deck61.deck61_helper import (
    make_slide,
    make_quiz,
    make_cloze,
    make_table,
    make_chain,
    make_recall,
    make_spot_the_lie,
    make_slider,
    make_swipe,
    make_branching,
    make_venn
)

def get_sec6_slides():
    slides = []

    # Slide 51
    slides.append(make_slide(
        slide_num=51,
        title="Missed Abortus (Gecikmiş Düşük): Tanım ve Zaman Kriteri",
        subtitle="Canlılığını yitirmiş gebelik mahsulünün uterusta birden fazla hafta kalması",
        clinical_focus="Fetal ölümün sessiz seyretmesi ve uterusun büyümesinin durması",
        narrative=(
            "Klinik pratikte kanamasız veya minimal lekelenmeli asemptomatik gebelerde rutin ultrasonografide en sık yakalanan kayıp türü missed abortustur.\n\n"
            "- **Resmi Tanım Kriteri:** Amfi ders notundaki resmi tanıma göre **missed abortus (gecikmiş düşük)**; viabilitesini (canlılığını) yitirmiş gebelik mahsulünün uterus içinde **birden fazla hafta (>1 hafta / haftalarca)** kalmış olması durumudur.\n"
            "- **Uterus Boyutu:** Hasta haftalar önce embriyonik ölüm yaşamış olmasına rağmen miyometrium kontraksiyon başlatmadığı için dokular atılamaz. Sonuç olarak pelvik muayenede **uterus beklenen gebelik haftasından belirgin şekilde küçük** bulunur.\n"
            "- **Klinik Belirtiler:** Anne adayı genellikle gebeliğin sonlandığının farkında değildir; ancak bulantı, kusma ve göğüslerdeki dolgunluk/hassasiyet gibi gebelik semptomlarının aniden gerilediğini veya kahverengi hafif bir akıntı başladığını ifade edebilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Missed abortus: Viabilitesini yitirmiş gebelik mahsulünün uterus kavitesinde birden fazla hafta kalmasıdır; uterus haftasına göre küçüktür."
        ),
        bullets=[
            "Viabilitesini yitirmiş gebelik mahsulü uterusta birden fazla hafta kalır",
            "Miyometrial kasılmalar başlamadığı için doku atılımı gerçekleşmez",
            "Pelvik muayenede uterus beklenen gebelik haftasından belirgin küçüktür",
            "Maternal gebelik semptomları (bulantı, göğüs dolgunluğu) gerilemiştir"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki resmi tanıma göre, viabilitesini (canlılığını) yitirmiş gebelik mahsulünün uterus kavitesinde birden fazla hafta kalmış olması durumu hangi klinik abortus tipidir?",
                options=[
                    {"key": "A", "text": "Missed abortus (gecikmiş düşük)", "isCorrect": True, "explanation": "Doğru. Canlılığını yitirmiş materyalin birden fazla hafta kalması missed abortustur."},
                    {"key": "B", "text": "Abortus insipiens", "isCorrect": False, "explanation": "İnsipienste canlı doku açık serviksten atılmak üzeredir."},
                    {"key": "C", "text": "İnkomplet abortus", "isCorrect": False, "explanation": "İnkomplet abortusta materyalin bir kısmı atılmıştır."},
                    {"key": "D", "text": "Abortus imminens", "isCorrect": False, "explanation": "İmminenste embriyo canlıdır (FKA +)."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Viabilitesini yitirmiş gebelik mahsulünün uterus içinde birden fazla hafta kalmış olması missed abortus olarak adlandırılır.",
                masked_term="birden fazla hafta",
                hint="Ders notunda missed abortus tanımında geçen resmi bekleme süresi ifadesi"
            ),
            make_slider(
                left_title="Canlı Gebelik (İmminens / Normal)",
                right_title="Missed Abortus",
                left_points=[
                    "Uterus son adet tarihine göre beklenen haftayla tam uyumlu büyür",
                    "Bulantı, kusma ve meme hassasiyeti aktif sürer",
                    "Ultrasonda pozitif kalp aktivitesi izlenir"
                ],
                right_points=[
                    "Uterus beklenen gebelik haftasından belirgin şekilde küçüktür",
                    "Maternal subjektif gebelik belirtileri aniden kaybolur",
                    "Kalp aktivitesi durmuş embriyo kavitede sessizce bekler"
                ]
            ),
            make_recall(
                question="Missed abortus tanısında ders notunda belirtilen temel zaman kriteri ve uterus muayene bulgusu nedir?",
                answer="Zaman kriteri canlılığını yitirmiş gebelik mahsulünün uterusta birden fazla hafta kalmasıdır; muayene bulgusu ise uterusun beklenen gebelik haftasından daha küçük olmasıdır."
            )
        ]
    ))

    # Slide 52
    slides.append(make_slide(
        slide_num=52,
        title="Missed Abortus Laboratuvarı ve USG Zamanlama Kriteri",
        subtitle="Gebelik testi pozitif (+) ama B-hCG düşüyor; 2 hafta ara ile USG ölçümleri aynı",
        clinical_focus="Hormonal düşüş trendi ve büyümenin ultrasonografik duraklaması",
        narrative=(
            "Missed abortus tanısında laboratuvar parametreleri ve seri ultrason takipleri tanısal şüpheyi kesinleştirir.\n\n"
            "- **Resmi Ders Notu Laboratuvar Kriteri:** Amfi ders notu tablosunda açıkça belirtildiği üzere: **'Gebelik testi + ama B-HCG düşüyor'** tablosu izlenir. Dolaşımdaki trofoblastik hormon miktarı azaldığı için kantitatif değer hızla düşerken, kalitatif testler bir süre daha pozitif kalır.\n"
            "- **Resmi Ultrasonik Zamanlama Kriteri:** Ders notundaki kritik tanı kriteri: **'FKA yok veya daha önce FKA ve embriyo görülmemiş ise 2 hafta ara ile yapılan USG ölçümleri aynı'** olmasıdır.\n"
            "- **Biyolojik Anlamı:** Sağlıklı bir erken gebelikte gestasyonel kese günde yaklaşık 1 mm büyür ve embriyo hızla gelişir. İki hafta (14 gün) arayla yapılan ultrason kontrollerinde kese ve embriyo ölçümlerinde hiçbir büyüme saptanmaması, gebeliğin haftalar önce arrest olduğunu kesin olarak belgeler.\n\n"
            "> [!IMPORTANT]\n"
            "> Missed abortus: Gebelik testi pozitif olsa da B-hCG düzeyi düşmektedir; 2 hafta ara ile yapılan ultrason ölçümleri aynıdır."
        ),
        bullets=[
            "Ders notuna göre gebelik testi (+) çıkabilir ancak B-hCG seviyesi düşmektedir",
            "Ultrasonda fetal kalp atımı yoktur",
            "Daha önce FKA/embriyo görülmemişse 2 hafta ara ile yapılan USG ölçümleri aynıdır",
            "Kese ve embriyonun 14 gün boyunca hiç büyümemesi gelişimsel arresti kanıtlar"
        ],
        elements=[
            make_quiz(
                question="Ders notu tablosuna göre, daha önce embriyo ve fetal kalp atımı görülmemiş bir erken gebelikte missed abortus tanısını kesinleştiren ultrasonografi kriteri hangisinde doğru ifade edilmiştir?",
                options=[
                    {"key": "A", "text": "24 saat ara ile yapılan USG'de fetal hareketlerin azalması", "isCorrect": False, "explanation": "24 saat çok erkendir, fetal hareket ilk trimesterde tanı kriteri değildir."},
                    {"key": "B", "text": "2 hafta ara ile yapılan USG ölçümlerinin aynı kalması", "isCorrect": True, "explanation": "Doğru. Ders notu: 'Daha önce FKA ve embriyo görülmemiş ise 2 hafta ara ile yapılan USG ölçümleri aynı' kriterini belirtmiştir."},
                    {"key": "C", "text": "Kese çapının günde 5 mm büyümesi", "isCorrect": False, "explanation": "Bu hızlı büyümedir, normal gebeliktir."},
                    {"key": "D", "text": "Overde korpus luteumun kaybolması", "isCorrect": False, "explanation": "Over bulgusu kavitary tanı kriteri değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre missed abortus olgularında gebelik testi pozitif olmasına rağmen kandaki B-HCG düzeyi düşüş gösterir.",
                masked_term="B-HCG düzeyi düşüş",
                hint="Trofoblastik canlılık kaybı nedeniyle kanda izlenen hormonal gerileme"
            ),
            make_chain(
                title="Missed Abortus Hormonal ve Biyometrik Gerileme Kaskadı",
                steps=[
                    "Embriyonik Arrest: Genetik veya vasküler yetersizlikle embriyonik dolaşımın ve kardiyak aktivitenin durması",
                    "Trofoblastik İnvolüsyon: Plasental villusların fonksiyonunu kaybetmesi ve maternal kanda B-hCG sentezinin azalması",
                    "Hormonal Ayrışma: İdrar testinin pozitif kalmasına rağmen kantitatif serum hCG düzeyinin düşüş trendine girmesi",
                    "Biyometrik Duraklama: 2 hafta ara ile yapılan transvajinal ultrasonda kese boyutlarının milimetrik olarak tamamen aynı kalması"
                ]
            ),
            make_recall(
                question="Missed abortus şüphesi olan bir hastada idrar testinin pozitif çıkması canlı bir gebelik olduğunu kanıtlar mı?",
                answer="Hayır, kanıtlamaz. Çünkü trofoblastik dokunun dolaşıma salmış olduğu beta-hCG'nin klirensi haftalar alabilir; bu nedenle gebelik testi pozitif kalsa dahi kandaki hCG düzeyleri düşmektedir."
            )
        ]
    ))

    # Slide 53
    slides.append(make_slide(
        slide_num=53,
        title="TV-USG Tanısal Olmayan Bulgular 1: CRL <7 mm ve MSD 16-24 mm",
        subtitle="Gebelik kaybını düşündüren ancak kesin tanı koydurmayan erken ölçümler",
        clinical_focus="Erken biyometrik sınırlarda gereksiz küretajı önleyen bekleme kuralları",
        narrative=(
            "Transvajinal ultrasonografide (TV-USG) erken gebelik kaybı tanısı koyarken yanlış bir kararla canlı bir embriyoyu tahliye etmemek için kriterler 'tanısal olan' ve 'tanısal olmayan' olarak ikiye ayrılır.\n\n"
            "- **Resmi Ders Notu Kuralı:** Gebelik kaybını **düşündüren (tanısal olmayan / şüpheli)** bulgular hemen tahliye endikasyonu doğurmaz; mutlaka belirli bir süre sonra kontrol USG gerektirir.\n"
            "- **Kritik CRL Eşiği:** **Crown-rump length (CRL) <7 mm ve kalp atımı yokluğu**: Embriyo boyutu 7 mm'nin altındayken kalp atımının görülememesi cihaz çözünürlüğü veya erken dönem nedeniyle olabilir; tek başına gebelik kaybı tanısı koydurmaz.\n"
            "- **Kritik Kese Eşiği:** **Ortalama kese çapı (MSD) 16-24 mm ve embriyo yokluğu**: Kese çapı 25 mm'ye ulaşana kadar embriyonun izlenememesi mümkündür; bu nedenle 16-24 mm arası boş kese gebelik kaybını düşündürür ancak tanısal değildir.\n\n"
            "> [!IMPORTANT]\n"
            "> Tanısal OLMAYAN (yalnızca şüphe uyandıran) kriterler: CRL <7 mm ve FKA yokluğu; Ortalama kese çapı (MSD) 16-24 mm ve embriyo yokluğudur."
        ),
        bullets=[
            "CRL <7 mm iken kalp atımının izlenmemesi tanısal değildir, şüphe uyandırır",
            "Ortalama kese çapı (MSD) 16-24 mm iken embriyo görülmemesi tanısal değildir",
            "Bu bulgular varlığında derhal tahliye yapılmaz, 7-14 gün sonra kontrol USG istenir",
            "Amaç canlı olabilecek erken bir gebeliğin yanlışlıkla sonlandırılmasını önlemektir"
        ],
        elements=[
            make_quiz(
                question="Transvajinal ultrasonografide aşağıdaki bulgulardan hangisi erken gebelik kaybını 'düşündüren' (tanısal olmayan / şüpheli) bulgular arasında yer alır?",
                options=[
                    {"key": "A", "text": "CRL ≥7 mm ve kalp atımı yokluğu", "isCorrect": False, "explanation": "Bu kesin tanı koyduran bulgudur."},
                    {"key": "B", "text": "Ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğu", "isCorrect": False, "explanation": "Bu kesin tanı koyduran bulgudur."},
                    {"key": "C", "text": "CRL <7 mm ve kalp atımı yokluğu; ortalama kese çapı 16-24 mm ve embriyo yokluğu", "isCorrect": True, "explanation": "Doğru. Ders notuna göre CRL <7 mm FKA yokluğu ve MSD 16-24 mm embriyo yokluğu gebelik kaybını düşündüren (tanısal olmayan) bulgulardır."},
                    {"key": "D", "text": "Yolk keseli gebelik kesesinden 14 gün sonra embriyo yokluğu", "isCorrect": False, "explanation": "Bu kesin tanı bulgusudur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notuna göre transvajinal ultrasonda embriyo boyutu yedi milimetreden küçük iken kalp atımı yokluğu kesin tanı koydurmaz, yalnızca kaybı düşündürür.",
                masked_term="yedi milimetreden küçük",
                hint="Ders notunda CRL için belirtilen tanısal olmayan sınır (rakamla <7 mm)"
            ),
            make_slider(
                left_title="Tanısal Olmayan (Şüpheli) Eşikler",
                right_title="Kesin Tanı Koyduran Eşikler",
                left_points=[
                    "CRL <7 mm ve kalp atımı yokluğu",
                    "Ortalama kese çapı (MSD) 16-24 mm ve embriyo yokluğu",
                    "Kontrol ultrasonografisi ile takip gerektirir"
                ],
                right_points=[
                    "CRL ≥7 mm ve kalp atımı yokluğu",
                    "Ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğu",
                    "Gebelik kaybı kesin tanısı konur ve tahliye planlanır"
                ]
            ),
            make_recall(
                question="Transvajinal ultrasonda embriyo boyutu 5 mm ölçülen ve kalp atımı izlenmeyen asemptomatik bir gebede klinik yaklaşım ne olmalıdır?",
                answer="CRL <7 mm olduğu için bu bulgu kesin tanısal değildir; hastaya hemen küretaj yapılmaz, 7 ila 10 gün sonra kontrol ultrasonografisi yapılarak viabilite yeniden değerlendirilir."
            )
        ]
    ))

    # Slide 54
    slides.append(make_slide(
        slide_num=54,
        title="TV-USG Tanısal Olmayan Bulgular 2: Zaman Aralıklı Kese Kriterleri",
        subtitle="Yolk kesesiz keseden 7-13 gün; yolk keseli keseden 7-10 gün sonra FKA yokluğu",
        clinical_focus="Erken ultrasonik mihenk taşlarının zamansal gelişim sınırları",
        narrative=(
            "Kese içinde yapıların belirmesi belirli bir kronolojik sıra izler ve bu sıralamadaki gecikmeler şüphe uyandırır.\n\n"
            "- **Yolk Kesesiz Kese Takibi:** İlk ultrasonda içinde henüz yolk kesesi bulunmayan bir gebelik kesesi saptanmışsa; bu incelemeden **7 ila 13 gün sonra** yapılan kontrolde halen embriyo ve kalp atımı izlenememesi gebelik kaybını düşündüren (tanısal olmayan) bir bulgudur.\n"
            "- **Yolk Keseli Kese Takibi:** İlk ultrasonda yolk kesesi görülmüş bir gebelik kesesi mevcutsa; bu incelemeden **7 ila 10 gün sonra** yapılan kontrolde halen embriyo ve kalp atımı saptanamaması yine kaybı düşündüren (tanısal olmayan) bulgudur.\n"
            "- **Klinik Yorum:** Bu süreler kesin tanı için gereken gün sınırlarının (sırasıyla 14 gün ve 11 gün) hemen altında kaldığı için hekim kesin karar vermeden önce birkaç gün daha bekleyerek viabiliteyi doğrulamalıdır.\n\n"
            "> [!NOTE]\n"
            "> Tanısal olmayan zaman kriterleri: Yolk kesesiz keseden 7-13 gün sonra; yolk keseli keseden 7-10 gün sonra embriyo/FKA yokluğudur."
        ),
        bullets=[
            "Yolk kesesiz keseden 7-13 gün sonra embriyo/FKA yokluğu tanısal değildir",
            "Yolk keseli keseden 7-10 gün sonra embriyo/FKA yokluğu tanısal değildir",
            "Bu süreler gebelik kaybı şüphesi doğurur ancak kesin tanı koydurmaz",
            "Kesin tanı için yolk kesesiz kesede ≥14 gün, yolk keseli kesede ≥11 gün beklenmelidir"
        ],
        elements=[
            make_quiz(
                question="Transvajinal ultrasonda yolk kesesi izlenen bir gebelik kesesinde, bu muayeneden kaç gün sonra yapılan kontrolde embriyo ve kalp atımı izlenememesi ders notuna göre 'gebelik kaybını düşündüren (tanısal olmayan)' bulgudur?",
                options=[
                    {"key": "A", "text": "1 ila 2 gün sonra", "isCorrect": False, "explanation": "Bu süre herhangi bir gelişim değerlendirmesi için çok kısadır."},
                    {"key": "B", "text": "11 gün veya daha fazla süre sonra", "isCorrect": False, "explanation": "≥11 gün kesin tanı koyduran bulgudur."},
                    {"key": "C", "text": "40 gün sonra", "isCorrect": False, "explanation": "Aşırı uzun bir süredir."},
                    {"key": "D", "text": "7 ila 10 gün sonra", "isCorrect": True, "explanation": "Doğru. Ders notu: 'Yolk keseli gebelik kesesinden 7-10 gün sonra embriyo ve kalp atımı yokluğu' tanısal olmayan bulgudur."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Ders notuna göre yolk keseli gebelik kesesi görüldükten yedi ila on gün sonra embriyo ve kalp atımı izlenememesi gebelik kaybını düşündüren bulgudur.",
                masked_term="yedi ila on gün",
                hint="Ders notunda yolk keseli kesenin tanısal olmayan takip süresi aralığı"
            ),
            make_table(
                title="Kese İçeriğine Göre Şüpheli Takip Aralıkları",
                headers=["İlk Ultrason Bulgusu", "Şüpheli (Tanısal Olmayan) Süre", "Klinik Yaklaşım"],
                rows=[
                    [
                        {"text": "Yolk kesesi OLMAYAN gebelik kesesi", "isMasked": False},
                        {"text": "7-13 gün sonra embriyo/FKA yokluğu", "isMasked": True, "hint": "Yolk kesesiz şüpheli aralık"},
                        {"text": "Kesin tanı için 14. güne kadar beklenir", "isMasked": False}
                    ],
                    [
                        {"text": "Yolk kesesi OLAN gebelik kesesi", "isMasked": False},
                        {"text": "7-10 gün sonra embriyo/FKA yokluğu", "isMasked": True, "hint": "Yolk keseli şüpheli aralık"},
                        {"text": "Kesin tanı için 11. güne kadar beklenir", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="İlk ultrasonda yolk kesesi görülen bir gebede 8 gün sonra yapılan kontrolde embriyo izlenmezse neden hemen küretaj kararı verilmez?",
                answer="Çünkü 7-10 günlük süre kaybı düşündürse de kesin tanısal değildir; kesin tanı koyabilmek için en az 11 gün geçmiş olması şarttır."
            )
        ]
    ))

    # Slide 55
    slides.append(make_slide(
        slide_num=55,
        title="TV-USG Tanısal Olmayan Bulgular 3: Amniyon, Yolk Sac ve Uyumsuzluk",
        subtitle="SAT'tan ≥6 hafta sonra embriyo yokluğu, boş amnion, büyümüş yolk sac (>7 mm)",
        clinical_focus="İkincil ultrasonik belirteçler ve embriyo-kese boyut diskordansı",
        narrative=(
            "Ders notunda erken gebelik kaybını düşündüren (tanısal olmayan) bulgular listesinde embriyo dışı yapılarla ilgili dört spesifik anatomik kriter daha yer alır.\n\n"
            "- **SAT Kriteri:** Son menstrual periyottan (SAT) **6 hafta veya daha uzun süre sonra** transvajinal ultrasonda embriyo yokluğu.\n"
            "- **Boş Amniyon Belirtisi:** Kese içinde amniyon zarı ve sıvısının belirmesine rağmen içinde embriyonik dokunun bulunmaması (**boş amnion**).\n"
            "- **Büyümüş Yolk Kesesi (>7 mm):** Yolk kesesinin çapının **7 mm'nin üzerinde (>7 mm)** ölçülmesi, koryonik villus beslenmesinde ve vitellin dolaşımda ağır bir yetersizlik olduğunu düşündürür.\n"
            "- **Kese-Embriyo Diskordansı:** Embriyoya göre küçük gebelik kesesi, yani **ortalama kese çapı (MSD) ile CRL arasında <5 mm fark** olması (oligohidroamniyos benzeri sıkışma görüntüsü).\n\n"
            "> [!NOTE]\n"
            "> Tanısal olmayan diğer bulgular: SAT'tan ≥6 hf sonra embriyo yokluğu, boş amnion, büyümüş yolk sac (>7 mm) ve MSD ile CRL farkının <5 mm olmasıdır."
        ),
        bullets=[
            "Son adet tarihinden ≥6 hafta sonra ultrasonda embriyo izlenmemesi",
            "Amniyon kesesinin varlığına rağmen içinde embriyo olmaması (boş amnion)",
            "Yolk kesesi çapının anormal genişleyerek >7 mm olarak ölçülmesi",
            "Ortalama kese çapı ile CRL arasındaki farkın <5 mm olması (küçük kese)"
        ],
        elements=[
            make_quiz(
                question="Transvajinal ultrasonda yolk kesesi çapının kaç milimetrenin üzerinde (>mm) ölçülmesi ders notuna göre gebelik kaybını düşündüren (tanısal olmayan) kriterlerden biridir?",
                options=[
                    {"key": "A", "text": ">2 mm", "isCorrect": False, "explanation": "2 mm normal erken yolk sac boyutudur."},
                    {"key": "B", "text": ">7 mm", "isCorrect": True, "explanation": "Doğru. Amfi ders notunda: 'büyümüş yolk kesesi (>7 mm)' gebelik kaybını düşündüren bulgudur."},
                    {"key": "C", "text": ">25 mm", "isCorrect": False, "explanation": "25 mm embriyosuz gebelik kesesi (MSD) sınırıdır, yolk sac değil."},
                    {"key": "D", "text": ">50 mm", "isCorrect": False, "explanation": "Gerçekçi olmayan bir boyuttur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre transvajinal ultrasonda yolk kesesi çapının yedi milimetrenin üzerinde olması gebelik kaybını düşündüren bulgudur.",
                masked_term="yedi milimetrenin üzerinde",
                hint="Ders notunda büyümüş yolk kesesi için verilen boyut eşiği (rakamla >7 mm)"
            ),
            make_table(
                title="Şüpheli İkincil Ultrasonik Kriterler",
                headers=["Ultrasonik Parametre", "Patolojik Eşik Değer", "Klinik Anlamı"],
                rows=[
                    [
                        {"text": "Yolk Kesesi Çapı", "isMasked": False},
                        {"text": "Büyümüş yolk kesesi (>7 mm)", "isMasked": True, "hint": "Genişlemiş vitellin yapı eşiği"},
                        {"text": "Erken koryonik dolaşım bozukluğu", "isMasked": False}
                    ],
                    [
                        {"text": "Kese ve Embriyo Farkı", "isMasked": False},
                        {"text": "MSD ile CRL arasında <5 mm fark", "isMasked": True, "hint": "Kavitary boşluk ve konseptüs boyu diskordans sınırı"},
                        {"text": "Embriyoya göre küçük gebelik kesesi", "isMasked": False}
                    ],
                    [
                        {"text": "SAT Süresi", "isMasked": False},
                        {"text": "SAT'tan ≥6 hafta sonra embriyo yokluğu", "isMasked": False},
                        {"text": "Gelişimsel gecikme şüphesi", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Transvajinal ultrasonda 'boş amnion' görülmesi ne anlama gelir ve kesin tanı koydurur mu?",
                answer="Amniyon zarının oluştuğunu ancak içinde embriyonun bulunmadığını gösterir; ders notuna göre bu bulgu gebelik kaybını düşündürür ancak tek başına kesin tanısal değildir, kontrol gerektirir."
            )
        ]
    ))

    # Slide 56
    slides.append(make_slide(
        slide_num=56,
        title="TV-USG KESİN TANI Kriterleri 1: CRL ≥7 mm ve MSD ≥25 mm",
        subtitle="Erken gebelik kaybı tanısını kesinleştiren ve tahliye kararı verdiren mihenk taşları",
        clinical_focus="Geri dönüşümsüz embriyonik ölümün ultrasonografik kesin belgelenmesi",
        narrative=(
            "Klinik pratikte gebeliğin sonlandığına ve tahliye gerektiğine şüphe bırakmaksızın karar verdiren altın standart bulgular kesin tanı kriterleridir.\n\n"
            "- **Resmi Ders Notu Kesin Tanı Kriteri 1 (CRL Eşiği):** **CRL ≥7 mm ve kalp atımı (FKA) yokluğu**. Embriyo boyutu 7 mm veya daha büyükse (≥7 mm), modern transvajinal problarla kalp atımının görülmemesi imkansızdır. Bu boyuttaki bir embriyoda FKA yokluğu kesin fetal ölüm tanısıdır.\n"
            "- **Resmi Ders Notu Kesin Tanı Kriteri 2 (MSD Eşiği):** **Ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğu**. Gestasyonel kesenin ortalama çapı 25 mm ve üzerinde olmasına rağmen içinde embriyonik doku saptanamıyorsa (anembriyonik gebelik / boş kese), gebelik kaybı tanısı kesindir.\n"
            "- **Klinik Yaklaşım:** Bu iki bulgudan herhangi biri saptandığında başka bir bekleme veya kontrol ultrasonuna gerek kalmaksızın gebelik kaybı tanısı konur ve medikal/cerrahi yönetim başlatılır.\n\n"
            "> [!IMPORTANT]\n"
            "> Kesin gebelik kaybı tanısı koyduran iki temel bulgu: CRL ≥7 mm ve FKA yokluğu ile Ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğudur."
        ),
        bullets=[
            "CRL ≥7 mm iken kalp atımının olmaması KESİN gebelik kaybı tanısıdır",
            "Ortalama kese çapı (MSD) ≥25 mm iken embriyo olmaması KESİN tanıdır",
            "Bu iki kriter varlığında ek bekleme süresine gerek kalmadan tanı kesinleşir",
            "Sınavlarda en sık sorgulanan iki resmi obstetrik kesinlik eşiğidir"
        ],
        elements=[
            make_quiz(
                question="Transvajinal ultrasonografide aşağıdaki bulgulardan hangisi gebelik kaybı (missed abortus / anembriyonik gebelik) tanısını KESİN OLARAK KOYDURAN bulgulardan biridir?",
                options=[
                    {"key": "A", "text": "CRL 4 mm ve kalp atımı yokluğu", "isCorrect": False, "explanation": "<7 mm tanısal değildir, kontrol gerekir."},
                    {"key": "B", "text": "Ortalama kese çapı 18 mm ve embriyo yokluğu", "isCorrect": False, "explanation": "16-24 mm arası şüphelidir, kesin tanı değildir."},
                    {"key": "C", "text": "Ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğu", "isCorrect": True, "explanation": "Doğru. MSD ≥25 mm ve embriyo yokluğu (veya CRL ≥7 mm FKA yokluğu) kesin tanı koydurur."},
                    {"key": "D", "text": "Yolk kesesi çapının 4 mm olması", "isCorrect": False, "explanation": "4 mm tamamen normal bir yolk sac çapıdır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Transvajinal ultrasonda embriyo boyutu yedi milimetre veya üzerinde iken kalp atımı saptanamaması kesin gebelik kaybı tanısı koydurur.",
                masked_term="yedi milimetre veya üzerinde",
                hint="Ders notunda FKA yokluğunda kesin tanı koyduran CRL sınır boyutu (rakamla ≥7 mm)"
            ),
            make_table(
                title="Şüpheli vs Kesin TV-USG Tanı Kriterleri Karşılaştırması",
                headers=["Biyometrik Ölçüm", "Şüpheli (Tanısal Olmayan) Sınır", "Kesin Tanı Koyduran Sınır"],
                rows=[
                    [
                        {"text": "CRL (FKA Yokluğunda)", "isMasked": False},
                        {"text": "CRL <7 mm", "isMasked": True, "hint": "Tanısal olmayan embriyo boyutu"},
                        {"text": "CRL ≥7 mm", "isMasked": True, "hint": "Kesin tanı embriyo boyutu"}
                    ],
                    [
                        {"text": "MSD (Embriyo Yokluğunda)", "isMasked": False},
                        {"text": "MSD 16-24 mm", "isMasked": True, "hint": "Tanısal olmayan kese boyutu aralığı"},
                        {"text": "MSD ≥25 mm", "isMasked": True, "hint": "Kesin tanı kese boyutu eşiği"}
                    ]
                ]
            ),
            make_recall(
                question="Transvajinal ultrasonda ortalama kese çapı (MSD) 26 mm ölçülen ancak içinde embriyo izlenmeyen bir hastada kontrol ultrasonu için beklenmeli midir?",
                answer="Hayır, beklenmemelidir. MSD ≥25 mm ve embriyo yokluğu gebelik kaybı için kesin tanı koyduran bir kriterdir; tanı kesinleşmiştir ve tahliye seçenekleri konuşulmalıdır."
            )
        ]
    ))

    # Slide 57
    slides.append(make_slide(
        slide_num=57,
        title="TV-USG KESİN TANI Kriterleri 2: Kesinleşmiş Takip Aralıkları",
        subtitle="Yolk kesesiz keseden ≥2 hafta; yolk keseli keseden ≥11 gün sonra FKA yokluğu",
        clinical_focus="Zaman aralıklı takiplerde geri dönüşsüzlüğün kesin belgelenmesi",
        narrative=(
            "Kese boyutları henüz 25 mm'ye veya embriyo 7 mm'ye ulaşmamış küçük gebeliklerde kesin tanı zamansal takiplerle konur.\n\n"
            "- **Resmi Ders Notu Kuralı 1 (Yolk Kesesiz Kese):** İlk ultrasonda yolk kesesi bulunmayan bir gebelik kesesi görüldükten **2 hafta veya daha fazla süre sonra (≥14 gün)** yapılan kontrolde halen embriyo ve kalp atımı yoksa gebelik kaybı tanısı **KESİNDİR**.\n"
            "- **Resmi Ders Notu Kuralı 2 (Yolk Keseli Kese):** İlk ultrasonda yolk kesesi bulunan bir gebelik kesesi görüldükten **11 gün veya daha fazla süre sonra (≥11 gün)** yapılan kontrolde halen embriyo ve kalp atımı yoksa gebelik kaybı tanısı **KESİNDİR**.\n"
            "- **Zamanlama Mantığı:** Yolk kesesi zaten oluşmuş bir konseptüste embriyonun belirmesi için gereken süre daha kısadır (11 gün yeterlidir); yolk kesesi henüz olmayan çok erken bir kesede ise biyolojik tolerans 14 güne (2 haftaya) kadar uzatılır.\n\n"
            "> [!IMPORTANT]\n"
            "> Kesin tanı koyduran zaman kriterleri: Yolk kesesiz keseden ≥2 hafta sonra; yolk keseli keseden ≥11 gün sonra embriyo ve FKA yokluğudur."
        ),
        bullets=[
            "Yolk kesesiz keseden ≥2 hafta (14 gün) sonra embriyo/FKA yokluğu KESİN TANIDIR",
            "Yolk keseli keseden ≥11 gün sonra embriyo/FKA yokluğu KESİN TANIDIR",
            "Yolk kesesi varlığında kesinleşme süresi 11 güne kısalır",
            "Bu süreler aşıldığında gebeliğin canlı olma olasılığı sıfırdır"
        ],
        elements=[
            make_quiz(
                question="Ders notuna göre, ilk transvajinal ultrasonografisinde yolk kesesi saptanmış olan bir gebelik kesesinde, en az kaç gün sonra yapılan kontrolde embriyo ve kalp atımı izlenememesi gebelik kaybı KESİN TANISI koydurur?",
                options=[
                    {"key": "A", "text": "3 gün sonra", "isCorrect": False, "explanation": "3 gün kesin tanı için çok erkendir."},
                    {"key": "B", "text": "7 gün sonra", "isCorrect": False, "explanation": "7-10 gün şüphelidir (tanısal değildir)."},
                    {"key": "C", "text": "11 gün veya daha fazla süre sonra", "isCorrect": True, "explanation": "Doğru. Ders notu: 'Yolk keseli gebelik kesesinden 11 gün veya daha fazla süre sonra embriyo ve kalp atımı yokluğu' kesin tanı koydurur."},
                    {"key": "D", "text": "30 gün sonra", "isCorrect": False, "explanation": "Gereksiz uzun bir beklemedir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notuna göre yolk kesesi olmayan bir gebelik kesesi görüldükten iki hafta veya daha fazla süre sonra embriyo izlenememesi kesin tanı koydurur.",
                masked_term="iki hafta veya daha fazla",
                hint="Ders notunda yolk kesesiz kese için kesin tanı koyduran resmi bekleme süresi"
            ),
            make_table(
                title="Zaman Aralıklı Kesin Tanı Kriterleri",
                headers=["Başlangıç Ultrason Bulgusu", "Kesin Tanı Koyduran Süre", "Gerekli Sonuç"],
                rows=[
                    [
                        {"text": "Yolk kesesi OLMAYAN gebelik kesesi", "isMasked": False},
                        {"text": "≥2 hafta (≥14 gün)", "isMasked": True, "hint": "Yolk kesesiz kesin tanı süresi"},
                        {"text": "Embriyo ve kalp atımı yokluğu", "isMasked": False}
                    ],
                    [
                        {"text": "Yolk kesesi OLAN gebelik kesesi", "isMasked": False},
                        {"text": "≥11 gün", "isMasked": True, "hint": "Yolk keseli kesin tanı süresi"},
                        {"text": "Embriyo ve kalp atımı yokluğu", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Neden yolk kesesi olan bir gebelik kesesinde kesin tanı için 11 gün yetiyorken, yolk kesesi olmayan kesede 14 gün (2 hafta) beklenir?",
                answer="Çünkü yolk kesesi varlığı gebeliğin daha ileri bir aşamada olduğunu gösterir ve embriyonun kalp atımıyla belirmesi daha hızlı gerçekleşmelidir; yolk kesesiz kese ise çok daha erken olduğu için gelişim toleransı 14 güne uzatılır."
            )
        ]
    ))

    # Slide 58
    slides.append(make_slide(
        slide_num=58,
        title="Missed Abortus Komplikasyonları: DIC ve Koagülopati",
        subtitle="Ölü konseptüsün uzun süre kalması ve tromboplastin salınımı",
        clinical_focus="Hematolojik kaskad bozukluğu ve sistemik tüketim koagülopatisi",
        narrative=(
            "Missed abortusta gebelik ürününün haftalarca uterus içinde kalması sadece obstetrik değil, ağır bir hematolojik risk doğurur.\n\n"
            "- **Dissemine İntravasküler Koagülasyon (DIC) Riski:** Canlılığını yitirmiş fetal ve desidual dokular nekroze oldukça maternal dolaşıma **doku faktörü (tromboplastin)** salgılar. Eğer ölü fetüs uterusta **4 haftadan (bir aydan) uzun süre kalırsa**, maternal dolaşımda yaygın mikrovasküler trombozlar başlar.\n"
            "- **Tüketim Koagülopatisi:** Pıhtılaşma faktörlerinin (fibrinojen, faktör V ve VIII) ve trombositlerin tükenmesi sonucu hastada **hipofibrinojenemi ve tüketim koagülopatisi (DIC)** gelişir. Hasta cerrahi tahliyeye alındığında kontrol edilemeyen masif kanamalar ortaya çıkabilir.\n"
            "- **Klinik Tedbir:** Uzamış missed abortus vakalarında cerrahi veya medikal müdahale öncesinde tam kan sayımı, PT, aPTT ve **plazma fibrinojen düzeyi** mutlaka kontrol edilmelidir.\n\n"
            "> [!NOTE]\n"
            "> Uterusta >4 hafta kalan ölü gebelik materyali, doku tromboplastini salınımı ile tüketim koagülopatisine (DIC) ve hipofibrinojenemiye yol açabilir."
        ),
        bullets=[
            "Ölü dokulardan maternal dolaşıma doku faktörü (tromboplastin) salınır",
            "Ölü materyalin >4 hafta uterusta kalması DIC riskini belirgin artırır",
            "Fibrinojen ve trombositlerin tükenmesi masif kanamaya zemin hazırlar",
            "Tahliye öncesi koagülasyon parametreleri ve fibrinojen düzeyi bakılmalıdır"
        ],
        elements=[
            make_quiz(
                question="Missed abortus tanısı alan bir gebede ölü gebelik materyalinin uterus içinde 4 haftadan uzun süre kalması durumunda gelişebilecek en ciddi hematolojik komplikasyon hangisidir?",
                options=[
                    {"key": "A", "text": "Megaloblastik kemik iliği hiperplazisi", "isCorrect": False, "explanation": "B12/folat eksikliği komplikasyonudur."},
                    {"key": "B", "text": "Dissemine intravasküler koagülasyon (DIC) ve tüketim koagülopatisi", "isCorrect": True, "explanation": "Doğru. Nekrotik dokulardan salınan tromboplastin DIC ve hipofibrinojenemiye yol açar."},
                    {"key": "C", "text": "Akut otoimmün hemolitik anemi", "isCorrect": False, "explanation": "İmmün aracılı eritrosit yıkımı değildir."},
                    {"key": "D", "text": "Esansiyel trombositemi", "isCorrect": False, "explanation": "Miyeloproliferatif neoplazidir, düşük komplikasyonu değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Missed abortusta nekrotik dokulardan salınan tromboplastin anne dolaşımında dissemine intravasküler koagülasyon tablosuna neden olabilir.",
                masked_term="dissemine intravasküler koagülasyon",
                hint="Faktör ve trombositlerin tükenmesiyle giden sistemik yaygın pıhtılaşma sendromu (DIC)"
            ),
            make_chain(
                title="Uzamış Missed Abortusta DIC Patogenezi",
                steps=[
                    "Doku Nekrozu: Uterusta haftalarca kalan ölü fetoplasental elemanların otolize uğraması",
                    "Tromboplastin Sızıntısı: Nekrotik dokudan maternal venöz sinüslere doku faktörü salınımı",
                    "Mikrovasküler Tromboz: Sistemik kapiller yatakta yaygın fibrin pıhtılarının oluşması",
                    "Tüketim ve Kanama: Fibrinojen ve trombositlerin tükenmesi sonucu hemostazın çökmesi (DIC)"
                ]
            ),
            make_recall(
                question="Missed abortus tanısıyla küretaja alınacak bir hastada operasyon öncesi pıhtılaşma açısından özellikle hangi laboratuvar parametresi kontrol edilmelidir?",
                answer="Plazma fibrinojen düzeyi, trombosit sayısı ve pıhtılaşma zamanları (PT, aPTT) kontrol edilmelidir."
            )
        ]
    ))

    # Slide 59
    slides.append(make_slide(
        slide_num=59,
        title="Missed Abortus Yönetimi: Bekleme, Medikal ve Cerrahi",
        subtitle="Ekspektan yaklaşım sınırları, misoprostol protokolü ve vakum küretaj",
        clinical_focus="Tanı kesinleştikten sonra hasta tercihi ve klinik stabiliteye dayalı yönetim",
        narrative=(
            "Missed abortus tanısı kesinleştiğinde tedavi seçenekleri hastanın klinik durumuna ve tercihine göre planlanır.\n\n"
            "- **Bekleme-Takip (Ekspektan Yönetim):** Kanama ve enfeksiyon bulgusu olmayan stabil hastalarda vücudun gebeliği kendiliğinden atması için 1-2 hafta beklenebilir. Ancak hastaların yaklaşık üçte birinde süreç uzar ve sonunda cerrahi veya medikal müdahale gerekir. Enfeksiyon veya aşırı kanama durumunda derhal sonlandırılır.\n"
            "- **Medikal Tedavi (Misoprostol):** En sık uygulanan cerrahisiz seçenektir. Prostaglandin E1 analoğu olan misoprostol (genellikle 800 mcg vajinal veya sublingual) servikal olgunlaşma ve miyometrial kontraksiyon başlatarak dokuların atılmasını sağlar (%80-90 başarı).\n"
            "- **Cerrahi Tahliye (Vakum Aspirasyon):** Hastanın hemen sonuç istemesi, aşırı kanama olması, enfeksiyon şüphesi veya medikal tedavinin başarısız olması durumunda günübirlik anestezi altında vakum aspirasyon uygulanır.\n\n"
            "> [!IMPORTANT]\n"
            "> Missed abortus yönetiminde bekleme-takip, medikal tedavi (misoprostol) ve cerrahi tahliye (vakum aspirasyon) seçenekleri mevcuttur."
        ),
        bullets=[
            "Bekleme-takip: Semptomsuz stabil olgularda 1-2 hafta kendiliğinden düşme beklenebilir",
            "Medikal tedavi: Prostaglandin E1 analoğu misoprostol ile farmakolojik atılım sağlanır",
            "Cerrahi tahliye: Vakum aspirasyon en hızlı ve güvenli cerrahi boşaltma yöntemidir",
            "Yönetim seçiminde hasta tercihi, enfeksiyon riski ve kanama durumu belirleyicidir"
        ],
        elements=[
            make_quiz(
                question="Missed abortus tanısı kesinleşen, hemodinamik olarak stabil ve kanaması olmayan bir kadında invaziv cerrahi işlemden kaçınmak amacıyla uygulanabilecek en etkili farmakolojik medikal ajan hangisidir?",
                options=[
                    {"key": "A", "text": "Progesteron", "isCorrect": False, "explanation": "Progesteron miyometriyumu gevşetir, ölü dokuyu atamaz."},
                    {"key": "B", "text": "Misoprostol (Prostaglandin E1 analoğu)", "isCorrect": True, "explanation": "Doğru. Misoprostol serviksi açıp uterus kasılmalarını tetikleyerek medikal tahliye sağlar."},
                    {"key": "C", "text": "Metargin (Ergometrin)", "isCorrect": False, "explanation": "Metargin servikal dilatasyon yapmaz, tonik spazm yapar."},
                    {"key": "D", "text": "Levotiroksin", "isCorrect": False, "explanation": "Tiroid hormonudur, düşük ilacı değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Missed abortus olgularında medikal tahliye amacıyla miyometriyumu kasan prostaglandin E1 analoğu olan misoprostol kullanılır.",
                masked_term="misoprostol",
                hint="Ders notunda erken gebelik kaybı medikal tedavisinde adı geçen PGE1 analoğu"
            ),
            make_slider(
                left_title="Medikal Tedavi (Misoprostol)",
                right_title="Cerrahi Tahliye (Vakum Aspirasyon)",
                left_points=[
                    "İnvaziv anestezi ve cerrahi gerektirmez",
                    "Ev ortamında kramplı kanama ile atılım süreci",
                    "Başarı oranı yaklaşık %80-90 düzeyindedir"
                ],
                right_points=[
                    "Klinikte dakikalar içinde kesin boşalma sağlar",
                    "Doku retansiyonu ve uzamış kanama riski düşüktür",
                    "Düşük oranda da olsa perforasyon ve enfeksiyon riski taşır"
                ]
            ),
            make_recall(
                question="Missed abortus tedavisinde ekspektan (bekleme) yaklaşımının en önemli dezavantajları nelerdir?",
                answer="Düşüğün ne zaman gerçekleşeceğinin öngörülememesi, yoğun kanamanın evde aniden başlayabilmesi, sürecin uzamasıyla hastada anksiyete ve nadiren enfeksiyon/DIC riskinin artmasıdır."
            )
        ]
    ))

    # Slide 60 (Checkpoint 6)
    slides.append(make_slide(
        slide_num=60,
        title="[TEKRAR SAYFASI - CHECKPOINT 6] Missed Abortus ve TV-USG Kriterleri",
        subtitle="Tanım, şüpheli vs kesin TV-USG ölçümleri, takip süreleri ve yönetim",
        clinical_focus="Missed abortus ve erken gebelik ultrasonik tanı kriterlerinin eksiksiz sentezi",
        narrative=(
            "Bu tekrar sayfası, 51-59. adımlarda işlenen Missed Abortus ve TV-USG Tanı Kriterlerini eksiksiz özetler.\n\n"
            "- **Missed Abortus Tanımı:** Viabilitesini yitirmiş gebeliğin uterusta **birden fazla hafta** kalmasıdır. Uterus haftasından küçüktür. Gebelik testi (+) ama **B-hCG düşmektedir**. FKA yoktur veya 2 hafta ara ile USG ölçümleri aynıdır.\n"
            "- **Tanısal Olmayan (Şüpheli) Bulgular:** **CRL <7 mm** ve FKA yok; **MSD 16-24 mm** ve embriyo yok; yolk kesesizden **7-13 gün**, yolk keseliden **7-10 gün** sonra embriyo/FKA yok; SAT'tan **≥6 hf** sonra embriyo yok; boş amnion, **yolk sac >7 mm**, MSD-CRL farkı <5 mm.\n"
            "- **KESİN TANI Koyduran Bulgular:** **CRL ≥7 mm** ve FKA yok; **MSD ≥25 mm** ve embriyo yok; yolk kesesizden **≥2 hafta**, yolk keseliden **≥11 gün** sonra embriyo ve FKA yokluğu.\n"
            "- **Yönetim:** Bekleme-takip, medikal (**misoprostol**) veya cerrahi (**vakum aspirasyon**); uzamış vakalarda DIC riski akılda tutulmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Kesin tanı eşikleri: CRL ≥7 mm FKA yok | MSD ≥25 mm embriyo yok | Yolk kesesiz ≥2 hafta | Yolk keseli ≥11 gün sonra FKA yok."
        ),
        bullets=[
            "Missed abortus: Canlılığını yitirmiş gebeliğin uterusta >1 hafta kalmasıdır",
            "Kesin TV-USG: CRL ≥7 mm FKA yok; MSD ≥25 mm embriyo yok",
            "Kesin takip: Yolk kesesizden ≥2 hafta; yolk keseliden ≥11 gün sonra FKA yokluğu",
            "Şüpheli (tanısal olmayan): CRL <7 mm FKA yok; MSD 16-24 mm embriyo yok",
            "Yönetim: Bekleme, medikal (misoprostol) ve cerrahi (vakum aspirasyon)"
        ],
        elements=[
            make_quiz(
                question="Aşağıdaki transvajinal ultrasonografi bulgularından hangisi erken gebelik kaybı için 'şüpheli (tanısal olmayan)' bir bulgu iken, diğeri 'KESİN TANI' koyduran bir bulgudur? (Şüpheli — Kesin)",
                options=[
                    {"key": "A", "text": "CRL ≥7 mm FKA yok — CRL <7 mm FKA yok", "isCorrect": False, "explanation": "Sıralama tam terstir."},
                    {"key": "B", "text": "Ortalama kese çapı (MSD) 16-24 mm embriyo yok — Ortalama kese çapı (MSD) ≥25 mm embriyo yok", "isCorrect": True, "explanation": "Doğru. 16-24 mm şüphelidir, ≥25 mm ise kesin tanı koydurur."},
                    {"key": "C", "text": "Yolk keseli keseden 11 gün sonra — Yolk keseli keseden 7 gün sonra", "isCorrect": False, "explanation": "11 gün kesin, 7 gün şüphelidir (sıra ters)."},
                    {"key": "D", "text": "Her iki bulgu da kesin tanıdır", "isCorrect": False, "explanation": "16-24 mm kesin tanı değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Transvajinal ultrasonda kesin gebelik kaybı tanısı koyabilmek için embriyo boyutu en az yedi milimetre iken kalp atımı saptanmamalıdır.",
                masked_term="yedi milimetre",
                hint="Ders notunda FKA yokluğunda kesin tanı için gereken asgari CRL boyutu (rakamla 7 mm)"
            ),
            make_table(
                title="Bölüm 6 Büyük TV-USG Tanı Matrisi (Checkpoint 6)",
                headers=["Ultrasonik Parametre", "Gebelik Kaybını Düşündüren (Tanısal Olmayan)", "Gebelik Kaybı KESİN TANI"],
                rows=[
                    [
                        {"text": "Embriyo Boyutu (CRL)", "isMasked": False},
                        {"text": "CRL <7 mm ve FKA yok", "isMasked": True, "hint": "Şüpheli embriyonik baş-popo uzunluğu alt sınırı"},
                        {"text": "CRL ≥7 mm ve FKA yok", "isMasked": True, "hint": "Kesin kardiyak sessizlik baş-popo eşiği"}
                    ],
                    [
                        {"text": "Kese Çapı (MSD)", "isMasked": False},
                        {"text": "MSD 16-24 mm embriyo yok", "isMasked": True, "hint": "Şüpheli ortalama gestasyonel kavitary aralık"},
                        {"text": "MSD ≥25 mm embriyo yok", "isMasked": True, "hint": "Kesin boş gebelik kesesi çap eşiği"}
                    ],
                    [
                        {"text": "Yolk Kesesiz Kese Takibi", "isMasked": False},
                        {"text": "7-13 gün sonra embriyo/FKA yok", "isMasked": False},
                        {"text": "≥2 hafta sonra embriyo/FKA yok", "isMasked": True, "hint": "Vitellin yapısı bulunmayan kese için kesin süre"}
                    ],
                    [
                        {"text": "Yolk Keseli Kese Takibi", "isMasked": False},
                        {"text": "7-10 gün sonra embriyo/FKA yok", "isMasked": False},
                        {"text": "≥11 gün sonra embriyo/FKA yok", "isMasked": True, "hint": "Vitellin yapısı bulunan kese için kesin süre"}
                    ]
                ]
            ),
            make_branching(
                scenario="Rutin kontrole gelen 8 haftalık gebe bir kadında vajinal kanama veya ağrı yoktur. Yapılan transvajinal USG bulgusuna göre klinik karar verilecektir.",
                options=[
                    {
                        "text": "CRL 8 mm ölçülür ve kalp atımı izlenmezse CRL ≥7 mm kriteri karşılandığından missed abortus kesin tanısı konur ve tahliye seçenekleri konuşulur.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. CRL ≥7 mm iken FKA yokluğu kesin fetal ölüm kanıtıdır, bekleme gerekmez."
                    },
                    {
                        "text": "MSD 18 mm ve embriyo görülmediğinde hemen acil küretaj ile kavite boşaltılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. MSD 16-24 mm tanısal değildir; 7-10 gün sonra kontrol USG yapılmalıdır."
                    },
                    {
                        "text": "Yolk kesesiz bir keseden 8 gün sonra embriyo görülmediğinde kesin ölümdür denilerek laparotomi yapılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Yolk kesesiz kesede kesin tanı için en az 14 gün (2 hafta) beklenmelidir."
                    }
                ]
            ),
            make_recall(
                question="Bölüm 6'nın en hayati iki sınav spotu olan transvajinal ultrasonografi kesin tanı eşikleri nelerdir?",
                answer="1) CRL ≥7 mm ve kalp atımı yokluğu, 2) Ortalama kese çapı (MSD) ≥25 mm ve embriyo yokluğudur."
            )
        ]
    ))

    return slides
