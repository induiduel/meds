# -*- coding: utf-8 -*-
"""
Deck 61 Section 4: Abortus Tipleri Ayrımı 1 — Abortus İmminens ve Abortus İnsipiens
Slides 31-40 (Checkpoint 4 at slide 40)
Focus:
- Abortus sınıflamasına genel bakış (İmminens, İnsipiens, İnkomplet, Komplet, Missed, Rekürren)
- Abortus imminens (düşük tehdidi) tanımı ve klinik özellikleri: 20. haftadan önce vajinal kanama, hafif kramp/ağrı
- Abortus imminens pelvik muayene bulgusu: Servikal os KAPALI, vajinada taze/kahverengi kanama
- Abortus imminens ultrasonografisi: İntrauterin canlı embriyo/fetüs, pozitif fetal kalp atımı (FKA +)
- Abortus imminens medikal tedavisi ve yaklaşım: Yatak istirahati kanıtı, progesteron desteği, indometazin
- Abortus imminens prognozu ve sonraki gebelik riskleri (subkoryonik hematom, düşük veya miada ulaşma)
- Abortus insipiens (kaçınılmaz düşük) tanımı ve klinik tablosu: Gebelik kaybının kaçınılmaz olduğu evre
- Abortus insipiens pelvik muayene ve klinik ayrımı: Servikal os AÇIK, şiddetli kasık ağrısı, yoğun kanama
- Abortus insipiens ultrasonografi bulguları: Kavitede henüz atılmamış ancak desiduadan ayrılmakta olan gebelik
- Abortus insipiens yönetimi: Ekspektan takip vs acil medikal/cerrahi terminasyon
- Checkpoint 4 (Tekrar ve pekiştirme sayfası)
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

def get_sec4_slides():
    slides = []

    # Slide 31
    slides.append(make_slide(
        slide_num=31,
        title="Abortus Tipleri ve Klinik Sınıflama Mantığı",
        subtitle="İmminens, İnsipiens, İnkomplet, Komplet, Missed ve Rekürren sınıflaması",
        clinical_focus="Kanamalı gebede servikal açıklık ve gebelik materyalinin akıbetine dayalı sınıflama",
        narrative=(
            "Klinik obstetride abortus tek bir homojen tablo değil, patolojik sürecin ilerleme evresine göre adlandırılan altı ana klinik tipten oluşur.\n\n"
            "- **Altı Klinik Tip:** **1) Abortus imminens (düşük tehdidi)**, **2) Abortus insipiens (kaçınılmaz düşük)**, **3) İnkomplet abortus (tam olmayan düşük)**, **4) Komplet abortus (tam düşük)**, **5) Missed abortus (gecikmiş düşük)** ve **6) Rekürren abortus (tekrarlayan düşük)**.\n"
            "- **Ayırıcı Tanının Temel Direkleri:** Bir hastanın hangi abortus tipinde olduğunu belirlerken klinisyen üç temel veriyi birleştirir: Vajinal kanama ve ağrının şiddeti, spekulum/pelvik muayenede **servikal kanalın durumu (açık veya kapalı)** ve **ultrasonografide gebelik ürününün lokalizasyonu ile viabilitesi**.\n"
            "- **Klinik Karar Eşiği:** Serviksin kapalı ve embriyonun canlı olması gebeliğin korunabileceğini gösterirken (imminens), serviksin açılması sürecin artık durdurulamaz bir terminasyona girdiğini (insipiens/inkomplet) gösterir.\n\n"
            "> [!IMPORTANT]\n"
            "> Abortus tiplerinin ayırıcı tanısında serviksin açık/kapalı olması ve ultrasondaki viabilite durumu en kritik iki kriterdir."
        ),
        bullets=[
            "Başlıca 6 abortus tipi: İmminens, İnsipiens, İnkomplet, Komplet, Missed, Rekürren",
            "Servikal açıklık (açık vs kapalı) prognozu ve klinik tipi belirleyen ana muayenedir",
            "Ultrasonografi ile fetal viabilite (FKA varlığı) ve kavite içeriği teyit edilir",
            "Abortus imminens gebeliğin devam şansı olan tek kanamalı erken tiptir"
        ],
        elements=[
            make_quiz(
                question="İlk trimesterde vajinal kanama ile acil servise başvuran bir gebede abortus tipini doğru belirlemek için fizik muayenede öncelikle değerlendirilmesi gereken en kritik anatomik bulgu hangisidir?",
                options=[
                    {"key": "A", "text": "Hastanın bazal vücut sıcaklığı", "isCorrect": False, "explanation": "Ateş septik abortusta önemlidir ancak ilk basamak sınıflama kriteri değildir."},
                    {"key": "B", "text": "Maternal tiroid bezinin boyutu", "isCorrect": False, "explanation": "Tiroid muayenesi akut tip tayini yapmaz."},
                    {"key": "C", "text": "Servikal kanalın (servikal internal os) açık veya kapalı olması", "isCorrect": True, "explanation": "Doğru. Serviksin açık veya kapalı olması imminens ile diğer tipleri ayıran en temel fizik muayene bulgusudur."},
                    {"key": "D", "text": "Deri turgor ve elastikiyeti", "isCorrect": False, "explanation": "Dehidratasyon bulgusudur, obstetrik sınıflama belirteci değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Abortus sınıflamasında servikal os kapalı ve canlı embriyo izlenen durum abortus imminens olarak adlandırılır.",
                masked_term="abortus imminens",
                hint="Türkçe karşılığı düşük tehdidi olan klinik tablo"
            ),
            make_slider(
                left_title="Gebeliğin Korunabildiği Durum (İmminens)",
                right_title="Geri Dönüşsüz Durumlar (İnsipiens / İnkomplet)",
                left_points=[
                    "Servikal kanal kesinlikle KAPALI",
                    "İntrauterin kalp atımı pozitif (FKA +)",
                    "Gebeliğin miada ulaşma şansı devam eder"
                ],
                right_points=[
                    "Servikal kanal AÇIK",
                    "Kaviteden ayrılma veya kısmi atılım süreci",
                    "Gebeliğin devamı tıbben imkansızdır"
                ]
            ),
            make_recall(
                question="Ders notunda tanımlanan başlıca 6 klinik abortus tipi hangileridir?",
                answer="Abortus imminens, abortus insipiens, inkomplet abortus, komplet abortus, missed abortus ve rekürren abortustur."
            )
        ]
    ))

    # Slide 32
    slides.append(make_slide(
        slide_num=32,
        title="Abortus İmminens (Düşük Tehdidi): Tanım ve Klinik Belirtiler",
        subtitle="20. haftadan önce vajinal kanama, hafif kramp veya ağrısız seyir",
        clinical_focus="İlk trimester kanamalarının en sık karşılaşılan klinik prezantasyonu",
        narrative=(
            "Klinik pratikte gebeliğin erken aylarında vajinal kanama ile başvuran olguların büyük kısmı bu kategoriye girer.\n\n"
            "- **Resmi Tanım:** **20. gebelik haftasından önce** vajinal kanama görülmesi durumudur. Hastada hafif kramp tarzı alt karın ağrısı eşlik edebilir veya kanama tamamen ağrısız olabilir.\n"
            "- **Epidemiyolojik Görülme Sıklığı:** Tüm gebeliklerin yaklaşık **%20 ila 40'ında** ilk trimesterde vajinal lekelenme veya kanama gelişir. Bu kanamalı hastaların yaklaşık yarısı gebeliğini sorunsuz sürdürürken, diğer yarısı ilerleyen süreçte gebelik kaybına uğrar.\n"
            "- **Klinik Yaklaşım:** Spekulum muayenesi yapılarak kanamanın uterus içinden geldiği, vajinal veya servikal bir yırtık/polip kaynaklı olmadığı teyit edilmeli ve hemen ardından acil ultrasonografi planlanmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Abortus imminens: 20. gebelik haftasından önce vajinal kanama ile karakterizedir; ağrı/kramp olabilir veya olmayabilir."
        ),
        bullets=[
            "20. gebelik haftasından önce vajinal kanama varlığı ile tanımlanır",
            "Kasıklarda hafif kramp/ağrı bulunabilir veya kanama tamamen ağrısızdır",
            "Tüm gebeliklerin %20-40'ında ilk trimester kanaması izlenir",
            "İlk basamakta spekulum muayenesi ile kanama kaynağı doğrulanmalıdır"
        ],
        elements=[
            make_quiz(
                question="Ders notuna göre, 8 haftalık gebe bir kadında 'abortus imminens' (düşük tehdidi) tanısı koyabilmek için temel klinik tablo hangisinde doğru tarif edilmiştir?",
                options=[
                    {"key": "A", "text": "20. gebelik haftasından önce vajinal kanama olması; ağrı veya krampın eşlik edebilmesi ya da olmaması", "isCorrect": True, "explanation": "Doğru. Notta imminens tanımı 20. haftadan önce vajinal kanama; ağrı/kramp olabilir veya olmayabilir şeklinde verilmiştir."},
                    {"key": "B", "text": "Gebelik materyalinin yarısının vajinadan dışarı atılmış olması", "isCorrect": False, "explanation": "Bu durum inkomplet abortustur."},
                    {"key": "C", "text": "Fetal kalp atımının en az iki haftadır durmuş olması", "isCorrect": False, "explanation": "Bu durum missed abortustur."},
                    {"key": "D", "text": "Serviksin 4 cm açılmış ve amniyon kesesinin patlamış olması", "isCorrect": False, "explanation": "Bu durum abortus insipienstir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Düşük tehdidinde yirminci gebelik haftasından önce vajinal kanama görülür ve tabloya kramp eşlik edebilir veya etmeyebilir.",
                masked_term="yirminci gebelik haftasından",
                hint="Abortus tanımında kabul edilen obstetrik üst sınır zamanı"
            ),
            make_chain(
                title="Abortus İmminens Klinik Değerlendirme Algoritması",
                steps=[
                    "Başvuru Semptomu: 20. haftadan önce vajinal kanama veya kahverengi lekelenme",
                    "Spekulum İncelemesi: Kanamanın eksternal servikal ostan geldiğinin ve vajinal lezyon olmadığının teyidi",
                    "Bimanuel Muayene: Servikal kanalın iç ve dış deliğinin kapalı olduğunun saptanması",
                    "Transvajinal Ultrasonografi: İntrauterin yerleşimli embriyonun ve pozitif kalp atımının (FKA +) gösterilmesi"
                ]
            ),
            make_recall(
                question="Abortus imminens tablosunda vajinal kanamaya kasık ağrısı eşlik etmesi zorunlu mudur?",
                answer="Hayır, zorunlu değildir. Kramp veya hafif kasık ağrısı bulunabilir veya hasta tamamen ağrısız sadece vajinal kanama ile başvurabilir."
            )
        ]
    ))

    # Slide 33
    slides.append(make_slide(
        slide_num=33,
        title="Abortus İmminens Muayene ve Ultrason Bulguları",
        subtitle="Serviks KAPALI, kanama +, intrauterin kalp atımı pozitif (FKA +)",
        clinical_focus="Canlı gebeliğin ultrasonografik olarak belgelenmesi",
        narrative=(
            "Abortus imminens tablosunu diğer tüm abortus tiplerinden ayıran en temel özellik pelvik muayene ve ultrasonografik viabilitedir.\n\n"
            "- **Pelvik Muayene Bulgusu:** Vajinal spekulum incelemesinde servikal kanaldan gelen aktif taze kanama veya eski kahverengi kan görülür; ancak **servikal internal os KESİNLİKLE KAPALIDIR**. Uterus gebelik haftasıyla uyumlu büyüklüktedir.\n"
            "- **Ultrasonografi Bulgusu:** Transvajinal USG'de uterus kavitesi içinde yerleşimli gestasyonel kese, yolk kesesi, embriyo ve en önemlisi **POZİTİF FETAL KALP ATIMI (FKA +)** izlenir.\n"
            "- **Subkoryonik Hematom Eşliği:** Koryon frondosum ile desidua bazalis arasında kan toplanması (subkoryonik hematom) sıklıkla saptanır. Hematomun boyutu arttıkça gebelik kaybı riski yükselmekle birlikte, FKA pozitif kaldığı sürece tanı imminenstir.\n\n"
            "> [!IMPORTANT]\n"
            "> Abortus imminens tanısının iki kardinal direği: Serviksin KAPALI olması ve ultrasonda intrauterin KALP ATINININ (FKA +) pozitif olmasıdır."
        ),
        bullets=[
            "Spekulum ve bimanuel muayenede serviks kesinlikle KAPALIDIR",
            "Vajinada kanama mevcuttur (aktif veya eski lekelenme)",
            "Ultrasonografide intrauterin embriyo/fetüste kalp atımı (FKA +) pozitiftir",
            "Uterus boyutu beklenen gebelik haftası ile tam uyumludur"
        ],
        elements=[
            make_quiz(
                question="İlk trimesterde vajinal kanama şikayetiyle başvuran bir kadında abortus imminens (düşük tehdidi) tanısını kesinleştiren muayene ve ultrasonografi bulguları ikilisi hangisidir?",
                options=[
                    {"key": "A", "text": "Serviks açık — Kavitede düzensiz parçalı doku", "isCorrect": False, "explanation": "İnkomplet abortus bulgusudur."},
                    {"key": "B", "text": "Serviks kapalı — Boş kavite ve negatif gebelik testi", "isCorrect": False, "explanation": "Komplet abortus veya gebelik yokluğu bulgusudur."},
                    {"key": "C", "text": "Serviks kapalı — İntrauterin canlı embriyo ve pozitif kalp atımı (FKA +)", "isCorrect": True, "explanation": "Doğru. Kapalı serviks ve pozitif FKA abortus imminensin temel tanımıdır."},
                    {"key": "D", "text": "Serviks açık — Amniyon kesesinin vajinaya bombeleşmesi", "isCorrect": False, "explanation": "Abortus insipiens bulgusudur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Abortus imminens tablosunda vajinal muayenede servikal os kapalı olarak izlenir ve ultrasonda kalp atımı pozitiftir.",
                masked_term="kapalı",
                hint="Düşük tehdidinde servikal kanalın açıklık durumu"
            ),
            make_table(
                title="Abortus İmminens Kardinal Özellikleri",
                headers=["Klinik Parametre", "Bulgu Değeri", "Tanısal Önemi"],
                rows=[
                    [
                        {"text": "Servikal Kanal Durumu", "isMasked": False},
                        {"text": "Kesinlikle kapalıdır", "isMasked": True, "hint": "Açılmamış servikal os durumu"},
                        {"text": "Gebelik materyalinin atılmadığını gösterir", "isMasked": False}
                    ],
                    [
                        {"text": "Vajinal Kanama", "isMasked": False},
                        {"text": "Kanama mevcuttur (+)", "isMasked": False},
                        {"text": "Klinik başvuruyu başlatan temel semptomdur", "isMasked": False}
                    ],
                    [
                        {"text": "Ultrasonografi Bulgusu", "isMasked": False},
                        {"text": "İntrauterin kalp atımı pozitif", "isMasked": True, "hint": "Embriyonun canlı olduğunu gösteren FKA durumu"},
                        {"text": "Fetal viabilitenin sürdüğünü belgeler", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Bir gebede kanama olmasına rağmen serviksin kapalı ve ultrasonda FKA'nın pozitif olması klinik olarak neyi ifade eder?",
                answer="Abortus imminens tablosunu ifade eder; fetüsün canlı olduğunu, sürecin henüz kaçınılmaz bir düşüğe dönüşmediğini ve gebeliğin devam etme şansının bulunduğunu gösterir."
            )
        ]
    ))

    # Slide 34
    slides.append(make_slide(
        slide_num=34,
        title="Abortus İmminens Tedavisi: Progesteron, İndometazin ve Yönetim",
        subtitle="Medikal yaklaşımlar, istirahat kanıtları ve tokolitik ajanlar",
        clinical_focus="Miyometrial kontraktiliteyi baskılama ve luteal faz desteği",
        narrative=(
            "Abortus imminens saptanan gebede tedavi stratejisi semptomların hafifletilmesine ve miyometrial aktivitenin yatıştırılmasına odaklanır.\n\n"
            "- **Medikal Tedavi (Progesteron):** Ders notunda özellikle vurgulandığı üzere medikal tedavide **progesteron** temel ajanlardan biridir. Progesteron, miyometriumda gevşeme sağlar, lokal immün toleransı (PIBF - progesteronla indüklenen bloke edici faktör) artırır ve luteal faz yetmezliği olan kadınlarda desiduayı destekler.\n"
            "- **İndometazin:** Şiddetli kramp ve kontraksiyonları olan seçilmiş vakalarda prostaglandin sentezini inhibe etmek amacıyla **indometazin (NSAİİ)** kullanılabilir.\n"
            "- **İstirahat ve Yaşam Tarzı:** Klasik pratikte fiziksel aktivite kısıtlaması ve cinsel ilişki yasağı sık önerilse de yatak istirahatinin gebelik kaybını kesin olarak önlediğine dair kanıt düzeyi sınırlıdır. Ağır kaldırmaktan ve yorucu aktivitelerden kaçınma tavsiye edilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Amfi ders notuna göre abortus imminens tedavisinde medikal olarak progesteron ve indometazin gibi farmakolojik ajanlar kullanılır."
        ),
        bullets=[
            "Abortus imminens tedavisinde temel medikal ajan progesterondur",
            "Miyometrial krampların baskılanmasında indometazin (prostaglandin inhibitörü) kullanılır",
            "Progesteron desidual desteği artırarak uterus kontraksiyonlarını gevşetir",
            "Yatak istirahati ve koitus kısıtlaması sıklıkla önerilen konservatif önlemlerdir"
        ],
        elements=[
            make_quiz(
                question="Ders notunda abortus imminens (düşük tehdidi) tablosunun medikal tedavisinde kullanıldığı özellikle belirtilen farmakolojik ajanlar hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "Metotreksat ve aktinomisin D", "isCorrect": False, "explanation": "Bunlar kemoterapötiklerdir, gebeliği sonlandırır."},
                    {"key": "B", "text": "Oksitosin ve ergometrin", "isCorrect": False, "explanation": "Bunlar uterus kasıcı uterotoniklerdir, düşüğü hızlandırır."},
                    {"key": "C", "text": "Yüksek doz östrojen ve misoprostol", "isCorrect": False, "explanation": "Misoprostol düşük ilacıdır."},
                    {"key": "D", "text": "Progesteron ve indometazin", "isCorrect": True, "explanation": "Doğru. Ders notu imminens tedavisinde medikal olarak progesteron ve indometazin belirtmiştir."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Abortus imminens tedavisinde desidual desteği artırmak ve miyometriyumu gevşetmek amacıyla progesteron hormonu reçete edilir.",
                masked_term="progesteron",
                hint="Gebeliği koruyucu korpus luteum kökenli temel steroid hormon"
            ),
            make_spot_the_lie(
                topic="Abortus imminens tedavisi",
                items=[
                    {"text": "Abortus imminens medikal tedavisinde progesteron desteği kullanılabilir.", "isLie": False, "explanation": "Doğrudur; notta medikal tedavide progesteron yer alır."},
                    {"text": "Abortus imminens tanısı konulduğu anda derhal acil cerrahi küretaj ile uterus boşaltılmalıdır.", "isLie": True, "explanation": "Tuzak önerme. İmminenste fetüs canlıdır ve serviks kapalıdır; cerrahi boşaltma kontrendikedir, gebelik korunmaya çalışılır."},
                    {"text": "Kramp ve ağrısı belirgin olan vakalarda prostaglandin sentezini baskılamak için indometazin verilebilir.", "isLie": False, "explanation": "Doğrudur; notta indometazin medikal seçenek olarak geçer."}
                ]
            ),
            make_recall(
                question="Abortus imminens tanısı alan bir hastada miyometrial kontraksiyonları ve desidual inflamasyonu azaltmak için ders notunda adı geçen nonsteroid antiinflamatuvar ajan hangisidir?",
                answer="İndometazindir (prostaglandin sentez inhibitörü)."
            )
        ]
    ))

    # Slide 35
    slides.append(make_slide(
        slide_num=35,
        title="Abortus İmminens Prognozu ve Komplikasyonlar",
        subtitle="Kanamalı gebelerin %50'sinde devam, subkoryonik hematom ve sonraki riskler",
        clinical_focus="Erken kanama geçiren kadınlarda gebeliğin ileri dönem obstetrik riskleri",
        narrative=(
            "Abortus imminens atağı geçiren bir gebede sürecin nasıl sonlanacağı hastanın en büyük endişe kaynağıdır.\n\n"
            "- **Genel Prognoz:** İlk trimesterde düşük tehdidi (kanama) yaşayan kadınların yaklaşık **%50'si gebeliğini başarıyla miada ulaştırır** ve sağlıklı canlı doğum yapar. Diğer %50'sinde ise süreç kaçınılmaz düşüğe ilerler.\n"
            "- **Fetal Kalp Atımının Gücü:** Eğer ultrasonda pozitif fetal kalp atımı (FKA +) belgelenmişse, gebeliğin devam etme olasılığı belirgin şekilde yükselir (%85-90 üzerine çıkar). Ancak kanamanın haftalarca sürmesi veya subkoryonik hematom alanının kese çevresinin >%50'sini kaplaması riski artırır.\n"
            "- **İleri Gebelik Riskleri:** İlk trimesterde imminens geçiren ve doğuma ulaşan kadınlarda; ilerleyen haftalarda **preterm eylem**, **ablasyo plasenta**, **düşük doğum ağırlığı (SGA)** ve erken membran rüptürü (EMR) insidansı genel topluma göre daha yüksek bildirilmektedir.\n\n"
            "> [!NOTE]\n"
            "> FKA pozitif imminens olgularının çoğu canlı doğuma ulaşır; ancak bu gebeliklerde ileri haftalarda ablasyo ve preterm doğum riski artmıştır."
        ),
        bullets=[
            "Kanamalı gebelerin yaklaşık yarısı miada ulaşır, diğer yarısı kaybedilir",
            "FKA pozitifliği belgelendiğinde gebeliğin devam şansı %85-90'lara çıkar",
            "Büyük subkoryonik hematom varlığı fetal kayıp riskini artıran faktördür",
            "Gebelikte ilerleyen dönemde ablasyo plasenta ve preterm doğum riski artar"
        ],
        elements=[
            make_quiz(
                question="8 haftalık gebe bir kadında vajinal kanama sonrası yapılan ultrasonda intrauterin canlı embriyo ve pozitif kalp atımı (FKA +) saptanıyor. Bu hastaya prognoz hakkında verilecek en doğru bilimsel bilgi hangisidir?",
                options=[
                    {"key": "A", "text": "FKA pozitifliği tespit edilen imminens olgularında gebeliğin devam etme ve miada ulaşma olasılığı oldukça yüksektir.", "isCorrect": True, "explanation": "Doğru. FKA pozitif olduktan sonra gebeliklerin büyük kısmı canlı doğuma ulaşır."},
                    {"key": "B", "text": "Kanama olduğu için fetüs kesinlikle ölecektir, hemen küretaj yapılmalıdır.", "isCorrect": False, "explanation": "Yanlış. Hastaların en az yarısı miada ulaşır."},
                    {"key": "C", "text": "Kanama olması fetüsün kesinlikle Down sendromlu olduğunu gösterir.", "isCorrect": False, "explanation": "Kanama Down sendromu için patognomonik değildir."},
                    {"key": "D", "text": "Kanama geçiren hiçbir kadın normal vajinal doğum yapamaz.", "isCorrect": False, "explanation": "Doğum şekliyle doğrudan ilişkisi yoktur."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Abortus imminens atağı geçiren gebelerde ilerleyen haftalarda plasentanın erken ayrılması yani ablasyo plasenta riski hafif artış gösterir.",
                masked_term="ablasyo plasenta",
                hint="Uterin yatakta besleyici organın doğum öncesi vaktinden önce dekolmanı"
            ),
            make_slider(
                left_title="Erken Dönem Seyri (İlk Trimester)",
                right_title="Geç Dönem Riskleri (İkinci/Üçüncü Trimester)",
                left_points=[
                    "Hastaların yaklaşık %50'sinde kanama kendiliğinden durur",
                    "FKA pozitifliği varlığında sağkalım %85-90 düzeyindedir",
                    "Küçük subkoryonik hematomlar zamanla organize olup rezorbe olur"
                ],
                right_points=[
                    "Preterm doğum ve düşük doğum ağırlığı riski artar",
                    "Ablasyo plasenta (erken ayrılma) gelişme sıklığı yükselir",
                    "Doğuma kadar daha yakın obstetrik takip gerektirir"
                ]
            ),
            make_recall(
                question="İlk trimesterde ultrasonografide fetal kalp atımı (FKA) pozitif olarak teyit edilmiş bir gebede abortus imminens atağı sonrası canlı doğum şansı yaklaşık ne kadardır?",
                answer="Yaklaşık %85 ila %90'ın üzerindedir; FKA'nın pozitif görülmesi en güçlü olumlu prognostik göstergedir."
            )
        ]
    ))

    # Slide 36
    slides.append(make_slide(
        slide_num=36,
        title="Abortus İnsipiens (Kaçınılmaz Düşük): Tanım ve Klinik Tablo",
        subtitle="Gebelik kaybının gerçekleşmek üzere olduğu, geri dönüşümsüz evre",
        clinical_focus="Düşük tehdidinden kaçınılmaz terminasyona geçiş patofizyolojisi",
        narrative=(
            "Spontan abortus sürecinin geri döndürülemez noktaya ulaştığı tablo abortus insipienstir.\n\n"
            "- **Resmi Tanım:** Gebelik kaybının gerçekleşmek üzere olduğu, sürecin artık hiçbir medikal veya istirahat girişimiyle durdurulamayacağı kaçınılmaz düşük tablosudur.\n"
            "- **Klinik Belirtiler:** Hastada **şiddetli ve ritmik kasık ağrısı (uterin kontraksiyonlar)** mevcuttur. Vajinal kanama miktarı imminense kıyasla belirgin şekilde fazladır; pıhtılı ve yoğun kanama izlenir.\n"
            "- **Gebelik Materyalinin Durumu:** Bu evrede gebelik materyali (fetüs ve plasenta) henüz uterus dışına **atılmamıştır**; ancak serviks açıldığı ve desidual ayrılma başladığı için atılım an meselesidir.\n"
            "- **Klinik Yaklaşım:** Hastaya gebeliğin kurtarılma şansının kalmadığı uygun dille açıklanmalı, hemodinamik stabilite sağlanarak maternal kan kaybı ve enfeksiyon riskini önleyici terminasyon protokolü planlanmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Abortus insipiens: Gebelik kaybının gerçekleşmek üzere olduğu, kanamanın fazla, kasık ağrısının şiddetli olduğu ancak materyalin henüz atılmadığı durumdur."
        ),
        bullets=[
            "Gebelik kaybının gerçekleşmek üzere olduğu kaçınılmaz durumdur",
            "Kanama miktarı belirgin derecede fazladır ve pıhtılıdır",
            "Miyometrial kasılmalara bağlı şiddetli kasık ağrısı mevcuttur",
            "Gebelik materyali henüz uterus kavitesi dışına atılmamıştır"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki tanımlara göre, gebelik kaybının gerçekleşmek üzere olduğu, kanamanın fazla ve kasık ağrısının şiddetli olduğu ancak gebelik materyalinin henüz dışarı atılmadığı klinik tablo hangisidir?",
                options=[
                    {"key": "A", "text": "Abortus imminens", "isCorrect": False, "explanation": "İmminenste serviks kapalıdır, ağrı hafif veya yoktur ve kayıp kaçınılmaz değildir."},
                    {"key": "B", "text": "Abortus insipiens (kaçınılmaz düşük)", "isCorrect": True, "explanation": "Doğru. Fazla kanama, şiddetli ağrı ve atılmamış materyalle giden tablo abortus insipienstir."},
                    {"key": "C", "text": "Komplet abortus", "isCorrect": False, "explanation": "Komplet abortusta tüm materyal atılmıştır."},
                    {"key": "D", "text": "Missed abortus", "isCorrect": False, "explanation": "Missed abortusta kanama ve akut şiddetli ağrı genellikle yoktur, fetüs ölü kalmıştır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Gebelik kaybının gerçekleşmek üzere olduğu, şiddetli kasık ağrısı ve yoğun kanamayla giden kaçınılmaz tablo abortus insipiens olarak tanımlanır.",
                masked_term="abortus insipiens",
                hint="Kaçınılmaz düşük anlamına gelen Latince obstetrik tanı"
            ),
            make_chain(
                title="Abortus İnsipiense İlerleme Kaskadı",
                steps=[
                    "Miyometrial Kontraksiyon Başlangıcı: Prostaglandin salınımı ile güçlü ve ritmik uterin kasılmalar",
                    "Geniş Desidual Dekolman: Koryonik villusların desiduadan yaygın ayrılması ve yoğun kanama",
                    "Servikal Dilatasyon: Uterin basıncın internal os'u zorlaması ve serviksin açılması",
                    "Kaçınılmaz Sonlanma: Embriyonun kaviteden vajinaya doğru itilme sürecine girmesi"
                ]
            ),
            make_recall(
                question="Abortus imminens ile abortus insipiens arasındaki temel klinik ve semptomatik farklar nelerdir?",
                answer="İmminenste ağrı hafif/yoktur, kanama azdır, serviks kapalıdır ve gebelik sürebilir; insipienste ise kasık ağrısı şiddetlidir, kanama fazladır, serviks açılmıştır ve kayıp kaçınılmazdır."
            )
        ]
    ))

    # Slide 37
    slides.append(make_slide(
        slide_num=37,
        title="Abortus İnsipienste Muayene Bulgusu: Servikal Os AÇIK",
        subtitle="Dilate servikal kanal, ele gelen membranlar ve kanama şiddeti",
        clinical_focus="Muayenede açık internal os saptanmasının geri döndürülemez prognostik anlamı",
        narrative=(
            "Abortus insipiens tanısını fizik muayenede kesinleştiren temel patoloji serviksin açılmış olmasıdır.\n\n"
            "- **Servikal Muayene Bulgusu:** Spekulum ve vajinal tuşede **servikal kanal (internal ve eksternal os) AÇIKTIR**. Muayene eden parmak servikal kanaldan içeriye kolaylıkla girer.\n"
            "- **Muayenede Ele Gelen Bulgular:** Açılmış servikal kanaldan dışarı doğru bombeleşen intakt veya açılmış **amniyon kesesi membranları**, pıhtılar ve aktif yoğun kanama saptanır. Ancak henüz embriyonik doku parçaları vajinaya dökülmemiştir (materyal dışarı atılmamıştır).\n"
            "- **Klinik Ayrım:** Serviksin açık olması, hastayı düşük tehdidi (imminens) grubundan kesin olarak çıkarır. Artık gebeliği tokolizle veya istirahatle kurtarmak tıbben imkansızdır; konservatif beklenti maternal enfeksiyon veya kontrolsüz kanama riski yaratır.\n\n"
            "> [!IMPORTANT]\n"
            "> Abortus insipienste serviks AÇIKTIR; kanama fazladır ve gebelik materyali henüz atılmamıştır."
        ),
        bullets=[
            "Fizik muayenede servikal internal os kesin olarak AÇIKTIR",
            "Servikal kanaldan amniyon kesesi membranları palpe edilebilir",
            "Yoğun vajinal kanama ve pıhtılar spekulumda izlenir",
            "Açık serviks tablonun geri döndürülemez olduğunu kanıtlar"
        ],
        elements=[
            make_quiz(
                question="Kanamalı bir gebede yapılan spekulum ve tuşe muayenesinde servikal kanalın açık olduğu saptanmıştır. Bu hastada aşağıdaki tanılardan hangisi KESİNLİKLE EKARTE EDİLİR?",
                options=[
                    {"key": "A", "text": "Abortus insipiens", "isCorrect": False, "explanation": "İnsipienste serviks açıktır."},
                    {"key": "B", "text": "İnkomplet abortus", "isCorrect": False, "explanation": "İnkomplet abortusta serviks açıktır."},
                    {"key": "C", "text": "Abortus imminens (düşük tehdidi)", "isCorrect": True, "explanation": "Doğru. Abortus imminens tanısı için serviksin kesinlikle KAPALI olması şarttır; açık serviks imminensi ekarte eder."},
                    {"key": "D", "text": "Erken membran rüptürü", "isCorrect": False, "explanation": "EMR'de serviks açık olabilir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Abortus insipiens tablosunda pelvik muayenede serviks açık olarak saptanır ve gebelik materyali henüz atılmamıştır.",
                masked_term="açık",
                hint="Kaçınılmaz düşükte servikal internal os'un genişlemiş ve parmak geçişine izin veren dilatasyon statüsü"
            ),
            make_table(
                title="Servikal Açıklığa Göre Abortus Tipleri Ayrımı",
                headers=["Abortus Tipi", "Servikal Açıklık Durumu", "Gebelik Materyali Durumu"],
                rows=[
                    [
                        {"text": "Abortus İmminens", "isMasked": False},
                        {"text": "Kesinlikle kapalı", "isMasked": True, "hint": "Açılmamış serviks durumu"},
                        {"text": "Kavitede intakt ve canlıdır", "isMasked": False}
                    ],
                    [
                        {"text": "Abortus İnsipiens", "isMasked": False},
                        {"text": "Açık", "isMasked": True, "hint": "Açılmış internal os durumu"},
                        {"text": "Kavitededir, henüz atılmamıştır", "isMasked": False}
                    ],
                    [
                        {"text": "İnkomplet Abortus", "isMasked": False},
                        {"text": "Açık", "isMasked": False},
                        {"text": "Bir kısmı atılmış, bir kısmı içeridedir", "isMasked": True, "hint": "Parçalı boşalma tablosu"}
                    ]
                ]
            ),
            make_recall(
                question="Pelvik muayenede servikal internal os'un açık olduğunun saptanması klinisyene neyi ifade eder?",
                answer="Sürecin düşük tehdidi (imminens) aşamasını geçtiğini, gebeliğin korunmasının artık mümkün olmadığını ve kaçınılmaz sonlanma sürecinin başladığını gösterir."
            )
        ]
    ))

    # Slide 38
    slides.append(make_slide(
        slide_num=38,
        title="Abortus İnsipiens Ultrasonografi Bulguları",
        subtitle="Kavite içi gebelik kesesi, servikal kanala doğru yer değiştirme ve FKA durumu",
        clinical_focus="Gebeliğin henüz kavitede gözlenmesi ancak anatomik oryantasyonun bozulması",
        narrative=(
            "Abortus insipienste ultrasonografi, gebelik materyalinin henüz atılmadığını teyit etmek için kritik öneme sahiptir.\n\n"
            "- **Resmi Ders Notu Bulgusu:** Amfi ders notu tablosunda abortus insipiens için ultrasonografi bulgusu net olarak **'Gebelik gözlenir'** şeklinde tanımlanmıştır.\n"
            "- **Spesifik Ultrasonik Görünüm:** Uterus içinde gestasyonel kese halen mevcuttur; ancak kese sıklıkla alt uterin segmente veya internal servikal os hizasına doğru **aşağı yer değiştirmiş (distale kaymış)** olarak izlenir. Kese kenarları düzensizleşmiş, çevresinde geniş dekolman hematomları oluşmuştur.\n"
            "- **FKA Durumu:** Fetal kalp atımı başlangıçta pozitif olabilir veya dekolmana bağlı yeni durmuş olabilir; ancak serviks açık olduğu için FKA pozitif olsa dahi tablonun geri dönüşü yoktur.\n"
            "- **İnkompletten Ayrımı:** İnkomplet abortusta kavitede düzensiz parçalı kalıntılar izlenirken, insipienste gebelik kesesi bir bütün olarak kavitede gözlenmektedir.\n\n"
            "> [!NOTE]\n"
            "> Abortus insipienste ultrasonda gebelik gözlenir; kese henüz atılmamıştır ancak servikal kanala doğru yer değiştirmektedir."
        ),
        bullets=[
            "Ders notuna göre abortus insipienste ultrasonda gebelik gözlenir",
            "Kese henüz atılmamıştır ancak alt uterin segmente doğru kaymıştır",
            "Gestasyonel kese çevresinde geniş dekolman hematomları izlenir",
            "FKA pozitif olsa dahi açık serviks nedeniyle prognoz kaçınılmaz kayıptır"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki sınıflama tablosuna göre abortus insipiens (kaçınılmaz düşük) tablosunda ultrasonografi bulgusu hangisinde doğru ifade edilmiştir?",
                options=[
                    {"key": "A", "text": "Gebelik materyali kesinlikle gözlenmez, kavite boştur", "isCorrect": False, "explanation": "Bu komplet abortus ultrasonudur."},
                    {"key": "B", "text": "Yalnızca overde korpus luteum kisti görülür", "isCorrect": False, "explanation": "Kavitary gebelik görülmelidir."},
                    {"key": "C", "text": "Gebelik gözlenir (gebelik materyali henüz atılmamıştır)", "isCorrect": True, "explanation": "Doğru. Ders notu insipiens ultrason bulgusunu doğrudan 'Gebelik gözlenir' olarak kaydetmiştir."},
                    {"key": "D", "text": "Kavite içinde yaygın veziküler kar fırtınası paterni", "isCorrect": False, "explanation": "Mol hidatiform ultrason bulgusudur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notu tablosuna göre abortus insipiens vakalarında ultrasonografide kavite içinde gebelik gözlenir.",
                masked_term="gebelik gözlenir",
                hint="Ders notundaki tablodan birebir alıntı: ultrasonografik inceleme sonucu"
            ),
            make_slider(
                left_title="Abortus İnsipiens Ultrasonu",
                right_title="Komplet Abortus Ultrasonu",
                left_points=[
                    "Kavite içinde gebelik kesesi gözlenir",
                    "Kese henüz dışarı atılmamıştır",
                    "Alt segmente doğru desidual ayrılma eşlik eder"
                ],
                right_points=[
                    "Uterus kavitesinde gebelik materyali gözlenmez",
                    "Tüm fetal ve plasental dokular atılmıştır",
                    "Endometrial kavite ince ve boştur"
                ]
            ),
            make_recall(
                question="Abortus insipienste ultrasonda fetal kalp atımının (FKA) halen pozitif saptanması gebeliğin kurtarılabileceğini gösterir mi?",
                answer="Hayır, göstermez. Servikal internal os açıldığı ve yaygın desidual ayrılma başladığı için FKA pozitif olsa dahi tablo kaçınılmazdır (abortus insipiens); gebeliğin miada ulaşması imkansızdır."
            )
        ]
    ))

    # Slide 39
    slides.append(make_slide(
        slide_num=39,
        title="Abortus İnsipiens Yönetimi: Terminasyon Prensipleri",
        subtitle="Medikal ve cerrahi terminasyon, kanama kontrolü ve enfeksiyon önleme",
        clinical_focus="Geri dönüşsüz süreçte maternal morbiditeyi minimize eden aktif yönetim",
        narrative=(
            "Abortus insipiens tanısı kesinleştiğinde tedavi yaklaşımı gebeliği korumak değil, anneyi korumaktır.\n\n"
            "- **Resmi Tedavi Yaklaşımı:** Amfi ders notunda abortus insipiens için tedavi seçeneği **'Medikal / cerrahi terminasyon'** olarak belirtilmiştir.\n"
            "- **Cerrahi Tahliye (Vakum Aspirasyon / Küretaj):** Şiddetli vajinal kanaması, hipotansiyonu veya taşikardisi olan hemodinamik olarak anstabil hastalarda en hızlı ve güvenli yöntem vakum aspirasyon ile cerrahi terminasyondur.\n"
            "- **Medikal Terminasyon:** Hemodinamisi stabil, kanaması kontrol altında olan hastalarda prostaglandin E1 analoğu (misoprostol) ile uterin kasılmalar desteklenerek materyalin tam atılımı sağlanabilir.\n"
            "- **Destek Tedavi:** Hastanın kan grubu Rh uygunsuzluğu açısından kontrol edilmeli, gerekirse Anti-D immünglobulin uygulanmalı ve enfeksiyon şüphesinde antibiyoterapi planlanmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Abortus insipienste tedavi medikal veya cerrahi terminasyondur; amaç maternal kanamayı durdurmak ve sepsisi önlemektir."
        ),
        bullets=[
            "Ders notuna göre tedavi medikal veya cerrahi terminasyondur",
            "Şiddetli kanama varlığında acil vakum aspirasyon cerrahisi tercih edilir",
            "Hemodinamik olarak stabil olgularda medikal prostaglandin terminasyonu uygulanabilir",
            "Rh-negatif gebelerde Anti-D profilaksisi asla ihmal edilmemelidir"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki bilgilere göre, serviksi açık, yoğun vajinal kanaması ve şiddetli kasık ağrısı olan abortus insipiens tanılı bir hastanın uygun tedavisi hangisidir?",
                options=[
                    {"key": "A", "text": "Hemen servikal serklaj dikişi atılarak serviksin kapatılması", "isCorrect": False, "explanation": "İnsipienste serklaj kontrendikedir, enfeksiyon ve rüptür yapar."},
                    {"key": "B", "text": "Medikal veya cerrahi terminasyon", "isCorrect": True, "explanation": "Doğru. Ders notu tablosunda insipiens tedavisi medikal / cerrahi terminasyon olarak belirtilmiştir."},
                    {"key": "C", "text": "Yalnızca progesteron verilip eve gönderilmesi", "isCorrect": False, "explanation": "İnsipiens progesteronla tedavi edilemez, süreç kaçınılmazdır."},
                    {"key": "D", "text": "Hiçbir müdahale yapılmadan 3 ay beklenmesi", "isCorrect": False, "explanation": "Kanama ve sepsisten anne hayatını riske atar."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notunda abortus insipiens vakalarının tedavisinde medikal veya cerrahi terminasyon yapılması gerektiği bildirilmektedir.",
                masked_term="cerrahi terminasyon",
                hint="Kavitenin operatif mekanik tahliye (küretaj / vakum) ile sonlandırılması işlemi"
            ),
            make_spot_the_lie(
                topic="Abortus insipiens tedavisi",
                items=[
                    {"text": "Abortus insipiens olgularında medikal veya cerrahi terminasyon uygulanır.", "isLie": False, "explanation": "Doğrudur; nottaki tedavi sütununda bu yöntemler geçer."},
                    {"text": "Abortus insipienste serviks açık olmasına rağmen gebeliği korumak için yüksek doz tokolitik verilip miada kadar beklenmelidir.", "isLie": True, "explanation": "Tuzak önerme. İnsipiens kaçınılmaz gebelik kaybıdır; tokolizle miada beklenmez, terminasyon yapılır."},
                    {"text": "Şiddetli kanaması olan hastalarda vakum aspirasyon ile cerrahi tahliye maternal hayatı korur.", "isLie": False, "explanation": "Doğrudur; acil hemostaz sağlar."}
                ]
            ),
            make_recall(
                question="Neden abortus insipienste progesteron verilerek gebelik kurtarılmaya çalışılmaz, terminasyon uygulanır?",
                answer="Çünkü servikal os açılmış, membranlar bombeleşmiş ve yaygın plasental ayrılma gerçekleşmiştir; sürecin geri dönüşü biyolojik olarak imkansızdır ve bekleme maternal enfeksiyon/kanama tehlikesi yaratır."
            )
        ]
    ))

    # Slide 40 (Checkpoint 4)
    slides.append(make_slide(
        slide_num=40,
        title="[TEKRAR SAYFASI - CHECKPOINT 4] Abortus Tipleri 1: İmminens vs İnsipiens",
        subtitle="Servikal açıklık, klinik ayrım, ultrason bulguları ve tedavi farkları",
        clinical_focus="Erken kanamalarda gebeliğin korunabilirliği ile kaçınılmaz terminasyonun karşılaştırılması",
        narrative=(
            "Bu tekrar sayfası, 31-39. adımlarda incelenen Abortus İmminens ve Abortus İnsipiens ayrımını kristalleştirir.\n\n"
            "- **Abortus İmminens (Düşük Tehdidi):** 20. haftadan önce vajinal kanama vardır; ağrı olabilir/olmayabilir. **Serviks KAPALIDIR**. Ultrasonda **intrauterin canlı embriyo ve FKA (+)** izlenir. Tedavisi medikaldir (**progesteron, indometazin** vb.). Gebeliğin miada ulaşma şansı devam eder.\n"
            "- **Abortus İnsipiens (Kaçınılmaz Düşük):** Gebelik kaybının gerçekleşmek üzere olduğu tablodur; kanama fazladır, şiddetli kasık ağrısı vardır; gebelik materyali henüz atılmamıştır. **Serviks AÇIKTIR**. Ultrasonda **gebelik gözlenir**. Tedavisi **medikal / cerrahi terminasyondur**.\n"
            "- **Altın Kural:** Kanamalı gebede spekulumla serviksin kapalı mı açık mı olduğunu belirlemek, iki tablo arasındaki en kesin klinik ayrımdır.\n\n"
            "> [!IMPORTANT]\n"
            "> İmminens: Serviks KAPALI, FKA (+), medikal (progesteron/indometazin) | İnsipiens: Serviks AÇIK, şiddetli ağrı, gebelik materyali henüz atılmamış, terminasyon."
        ),
        bullets=[
            "İmminens: Serviks KAPALI, FKA (+), tedavi progesteron/indometazindir",
            "İnsipiens: Serviks AÇIK, şiddetli kramp, tedavi medikal/cerrahi terminasyondur",
            "Her iki tabloda da gebelik materyali henüz dışarı atılmamıştır",
            "Servikal açıklık ve FKA varlığı iki klinik antiteyi ayıran ana eksendir"
        ],
        elements=[
            make_quiz(
                question="Abortus imminens ile abortus insipiens arasındaki farkları karşılaştıran aşağıdaki ifadelerden hangisi amfi ders notuna göre KESİNLİKLE DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "İmminenste serviks açıkken, insipienste serviks kesinlikle kapalıdır.", "isCorrect": False, "explanation": "Tam tersidir; imminenste kapalı, insipienste açıktır."},
                    {"key": "B", "text": "İmminenste tedavi progesteron/indometazin iken, insipienste tedavi medikal/cerrahi terminasyondur.", "isCorrect": True, "explanation": "Doğru. Ders notu tablosundaki tedavi protokolü tam olarak bu şekildedir."},
                    {"key": "C", "text": "İnsipienste gebelik materyalinin tamamı dışarı atılmıştır, imminenste ise henüz atılmamıştır.", "isCorrect": False, "explanation": "İnsipienste materyal henüz atılmamıştır; tamamı atılan komplet abortustur."},
                    {"key": "D", "text": "İmminens 20. haftadan sonra, insipiens ilk 12 haftada görülür.", "isCorrect": False, "explanation": "Her ikisi de 20. haftadan önceki abortus spektrumundadır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Abortus imminenste serviks kapalı ve FKA pozitif iken abortus insipienste serviks açıktır ve tedavi terminasyondur.",
                masked_term="FKA pozitif",
                hint="Düşük tehdidinde ultrasonda canlılığı gösteren kalp aktivitesi bulgusu"
            ),
            make_table(
                title="Bölüm 4 Karşılaştırmalı Sentez Tablosu (Checkpoint 4)",
                headers=["Klinik Özellik", "Abortus İmminens (Düşük Tehdidi)", "Abortus İnsipiens (Kaçınılmaz Düşük)"],
                rows=[
                    [
                        {"text": "Servikal Kanal Durumu", "isMasked": False},
                        {"text": "Kapalı", "isMasked": True, "hint": "Açılmamış serviks durumu"},
                        {"text": "Açık", "isMasked": True, "hint": "Dilate olmuş serviks durumu"}
                    ],
                    [
                        {"text": "Kasık Ağrısı Şiddeti", "isMasked": False},
                        {"text": "Hafif olabilir veya hiç yoktur", "isMasked": False},
                        {"text": "Şiddetli kasık ağrısı mevcuttur", "isMasked": True, "hint": "Güçlü miyometrial kasılmaların yarattığı ağrı"}
                    ],
                    [
                        {"text": "Ultrasonografi Bulgusu", "isMasked": False},
                        {"text": "İntrauterin kalp atımı pozitif", "isMasked": True, "hint": "Canlı embriyo varlığı"},
                        {"text": "Gebelik gözlenir", "isMasked": False}
                    ],
                    [
                        {"text": "Tedavi Yaklaşımı", "isMasked": False},
                        {"text": "Medikal (progesteron, indometazin)", "isMasked": False},
                        {"text": "Medikal / cerrahi terminasyon", "isMasked": True, "hint": "Kavitenin boşaltılması işlemi"}
                    ]
                ]
            ),
            make_branching(
                scenario="Acil servise 7 haftalık gebe bir kadın vajinal kanama ile getiriliyor. Spekulum ve ultrason muayenesi sonuçlarına göre yönetim seçilecektir.",
                options=[
                    {
                        "text": "Serviks kapalı ve ultrasonda intrauterin FKA (+) saptanırsa abortus imminens tanısıyla progesteron/medikal destek planlanır.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. İmminens kriterleri tamdır, gebelik korunabilir."
                    },
                    {
                        "text": "Serviks açık, şiddetli ağrısı var ve kese distale kaymışsa hemen eve gönderilip istirahat önerilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Açık serviks insipienstir, terminasyon gerekir; eve gönderilmez."
                    },
                    {
                        "text": "Serviks kapalı olan hastaya canlı embriyo görülmesine rağmen hemen cerrahi küretaj uygulanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. İmminenste cerrahi terminasyon kontrendikedir."
                    }
                ]
            ),
            make_recall(
                question="Birinci basamak hekimi kanamalı bir erken gebede abortus imminens ile abortus insipiens ayrımını en basit ve kesin olarak nasıl yapar?",
                answer="Spekulum ve pelvik muayene ile servikal kanalın kapalı mı yoksa açık mı olduğunu kontrol ederek; kapalı ise imminens, açık ise insipiens (veya inkomplet) tanısına yönelir."
            )
        ]
    ))

    return slides
