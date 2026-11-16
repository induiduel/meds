# -*- coding: utf-8 -*-
"""
Deck 61 Section 8: İlk Trimester Kanamalı ve Ağrılı Hastaya Yaklaşım & Ultrasonografi
Slides 71-80 (Checkpoint 8 at slide 80)
Focus:
- İlk trimester kanama ve ağrı sıklığı: Tüm gebelerin %20-40'ında görülmesi
- İlk başvuru laboratuvar testleri: CBC (tam kan sayımı), KG (kan grubu), Rh tayini ve serum hCG
- Ayırıcı tanı basamakları: Ektopik gebelik, abortus ve normal gebelik ayrımı; uterin, servikal ve vajinal patolojiler
- Özel durumlar: Heterotopik gebelik ve çoğul gebeliğin birinin kaybı (vanishing twin) olasılığı
- Ektopik gebelik dışlama kuralı: Seri hCG düzeyleri ve transvajinal ultrasonografi kombinasyonu ile dışlanması
- TV-USG Mihenk Taşları: Gestasyonel kese (TV-USG 4-5. hafta, TA-USG 6. hafta), GS günde 1 mm büyüme kuralı
- Kritik hCG diskriminatif zon kuralı: hCG >2000 mIU/ml ise mutlaka gebelik kesesi görülmelidir
- Yolk sac ve Fetal Pole: Yolk sac 5. haftadan itibaren; Fetal pole 6. haftada TV-USG ile yolk sac kenarında kalınlaşma olarak izlenir
- Biyometri ve CRL formülü: 7-14. hafta gebelik yaşı ölçümü, pratik yaklaşım: 6 hafta + CRL(mm) = 6 hafta + gün
- Tahmini doğum tarihi uyumu: İlk trimesterde SAT ile USG arasında 7 günlük fark önemsizdir; 2. trimesterde 10 günlük fark önemsizdir
- Checkpoint 8 (Tekrar ve pekiştirme sayfası)
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

def get_sec8_slides():
    slides = []

    # Slide 71
    slides.append(make_slide(
        slide_num=71,
        title="İlk Trimester Kanamalı ve Ağrılı Hasta: İnsidans ve İlk Testler",
        subtitle="Tüm gebelerin %20-40'ında başvuru; CBC, KG, Rh ve hCG dörtlüsü",
        clinical_focus="Erken gebelik acillerinde ilk basamak değerlendirme ve laboratuvar protokolü",
        narrative=(
            "İlk trimesterde vajinal kanama, kasık ağrısı ve adet gecikmesi semptom kompleksi obstetrik acil başvurularının en yaygın nedenidir.\n\n"
            "- **Görülme Sıklığı:** Amfi ders notunda açıkça belirtildiği üzere, ilk trimesterde kanama ve ağrı tablosu **tüm gebelerin %20 ila 40'ında** izlenir.\n"
            "- **İlk Başvuru Testleri (Dörtlü Paket):** Bu şikayetlerle başvuran her hastada derhal istenmesi gereken 4 temel laboratuvar testi şunlardır:\n"
            "  1. **CBC (Tam Kan Sayımı):** Hemoglobin/hematokrit ile kan kaybının derinliğini, lökosit ile enfeksiyonu değerlendirmek için.\n"
            "  2. **KG (Kan Grubu):** Transfüzyon ihtiyacı için hazırlık.\n"
            "  3. **Rh Tayini:** Rh-negatif annelerde fetomaternal kanamaya karşı Anti-D immünglobulin profilaksisi endikasyonunu belirlemek için.\n"
            "  4. **Kantitatif serum hCG:** Trofoblastik aktiviteyi ve gebeliğin viabilitesini izlemek için.\n\n"
            "> [!IMPORTANT]\n"
            "> Kanama ve ağrısı olan gebede ilk başvuru testleri: CBC, KG (kan grubu), Rh ve hCG testleridir; tüm gebelerin %20-40'ında görülür."
        ),
        bullets=[
            "İlk trimesterde kanama ve ağrı tüm gebelerin %20-40'ında izlenir",
            "İlk başvuruda mutlaka istenecek 4 test: CBC, KG, Rh ve hCG'dir",
            "Rh uygunsuzluğu saptanan hastalara Anti-D profilaksisi planlanır",
            "Hemodinamik stabilite ve hemoglobin düzeyi derhal kontrol edilir"
        ],
        elements=[
            make_quiz(
                question="İlk trimesterde vajinal kanama, kasık ağrısı ve adet gecikmesi ile acil servise başvuran bir hastada ders notuna göre İLK BAŞVURU SIRASINDA istenmesi gereken temel laboratuvar testleri hangisinde eksiksiz verilmiştir?",
                options=[
                    {"key": "A", "text": "CBC, KG (kan grubu), Rh ve hCG", "isCorrect": True, "explanation": "Doğru. Notta ilk başvuruda istenecek testler açıkça CBC, KG, Rh ve hCG olarak listelenmiştir."},
                    {"key": "B", "text": "Yalnızca karaciğer fonksiyon testleri ve lipid paneli", "isCorrect": False, "explanation": "İlk basamak obstetrik kanama testleri değildir."},
                    {"key": "C", "text": "Toraks BT ve D-Dimer", "isCorrect": False, "explanation": "Gereksiz radyasyon ve yanlış endikasyondur."},
                    {"key": "D", "text": "Kromozom analizi ve tümör belirteçleri", "isCorrect": False, "explanation": "Acil başvuruda ilk istenecek testler değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="İlk trimesterde kanama ve ağrısı olan hastadan ilk başvuru sırasında CBC, kan grubu, Rh faktörü ve hCG testleri istenir.",
                masked_term="Rh faktörü",
                hint="Alloimmünizasyon profilaksisi için kanda bakılan temel eritrosit antijen belirteci"
            ),
            make_table(
                title="İlk Başvuru Laboratuvar Paneli ve Gerekçeleri",
                headers=["Laboratuvar Testi", "Ders Notu Belirtimi", "Klinik Hedef"],
                rows=[
                    [
                        {"text": "Tam Kan Sayımı (CBC)", "isMasked": False},
                        {"text": "İlk başvuru testi", "isMasked": True, "hint": "Kanamalı gebede rutin basamak kan analizi"},
                        {"text": "Maternal anemi ve enfeksiyon düzeyini belirleme", "isMasked": False}
                    ],
                    [
                        {"text": "Kan Grubu ve Rh (KG/Rh)", "isMasked": False},
                        {"text": "İlk başvuru testi", "isMasked": False},
                        {"text": "Anti-D immünglobulin profilaksi ihtiyacını saptama", "isMasked": True, "hint": "Rh uyuşmazlığı koruma tedavisi"}
                    ],
                    [
                        {"text": "Serum hCG Düzeyi", "isMasked": False},
                        {"text": "İlk başvuru testi", "isMasked": False},
                        {"text": "Diskriminatif zon ve canlılık takibi", "isMasked": True, "hint": "Kese görünme eşiği ve trofoblast aktivitesi"}
                    ]
                ]
            ),
            make_recall(
                question="İlk trimester kanamalarında Rh tayininin ilk başvuruda acilen istenmesinin en kritik klinik gerekçesi nedir?",
                answer="Eğer anne Rh-negatif ve baba Rh-pozitif ise, ilk trimesterdeki kanama fetomaternal kanamaya yol açarak anneyi duyarlaştırabilir; bunu önlemek için ilk 72 saat içinde Anti-D immünglobulin uygulanması şarttır."
            )
        ]
    ))

    # Slide 72
    slides.append(make_slide(
        slide_num=72,
        title="İlk Trimester Ayırıcı Tanısı ve Ektopik Gebeliği Dışlama Kuralı",
        subtitle="Ektopik gebelik, abortus ve normal gebelik ayrımı; seri hCG ve USG kombinasyonu",
        clinical_focus="Maternal mortalitenin 1 numaralı nedeni olan ektopik gebeliğin ekarte edilmesi",
        narrative=(
            "Kanamalı erken gebede en acil görev, hayatı tehdit eden ektopik gebeliği ekarte etmektir.\n\n"
            "- **Temel Ayırıcı Tanı Üçgeni:** Amfi ders notunda vurgulandığı üzere klinisyen öncelikle **ektopik gebelik, abortus ve normal gebelik** tablolarını birbirinden ayırt etmelidir. Ayrıca ayırıcı tanıda uterin (miyom), servikal (polip, servisit) veya vajinal patolojiler de yer alır.\n"
            "- **Özel Riskler:** Yardımcı üreme teknikleri (YÜT) ile gebe kalanlarda intrauterin ve ektopik gebeliğin bir arada bulunduğu **heterotopik gebelik** ve ikiz gebeliklerde bir kesenin kaybolduğu **çoğul gebeliğin birinin kaybı (vanishing twin)** akılda tutulmalıdır.\n"
            "- **Dışlama Kuralı:** Ders notunun altın kuralı: **'Ektopik gebelik, seri hCG düzeyleri ve ultrasonografi kombinasyonu ile dışlanabilir.'** Tek bir ölçüm tanı koyduramaz; 48 saatlik aralıklı hCG takibi ve transvajinal USG bulgusu birleştirilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Ektopik gebelik, seri hCG düzeyleri ve transvajinal ultrasonografi kombinasyonu ile güvenle dışlanabilir."
        ),
        bullets=[
            "Ayırıcı tanı: Ektopik gebelik, abortus ve normal canlı gebelik ayrımıdır",
            "Uterin, servikal ve vajinal patolojiler spekulumla kontrol edilmelidir",
            "Heterotopik gebelik ve çoğul gebelik tekil kaybı akılda tutulmalıdır",
            "Ektopik gebelik seri hCG takibi ve ultrasonografi kombinasyonu ile dışlanır"
        ],
        elements=[
            make_quiz(
                question="Ders notunda ilk trimester kanamalarında hayatı tehdit eden 'ektopik gebelik' tablosunun kesin olarak dışlanabilmesi için önerilen tanısal yöntem kombinasyonu hangisidir?",
                options=[
                    {"key": "A", "text": "Yalnızca tek bir idrar çubuk testi", "isCorrect": False, "explanation": "İdrar testi ektopik gebeliği dışlayamaz."},
                    {"key": "B", "text": "Seri hCG düzeyleri ve ultrasonografi kombinasyonu", "isCorrect": True, "explanation": "Doğru. Ders notu açıkça: 'ektopik gebelik, seri hCG düzeyleri ve ultrasonografi kombinasyonu ile dışlanabilir' demektedir."},
                    {"key": "C", "text": "Rutin servikal smear ve HPV DNA testi", "isCorrect": False, "explanation": "Kanser taramasıdır, ektopik gebelik dışlamaz."},
                    {"key": "D", "text": "Karın muayenesinde steteskopla dinleme", "isCorrect": False, "explanation": "İlk trimesterde steteskopla fetal ses duyulmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre ektopik gebelik şüphesi seri hCG düzeyleri ve ultrasonografi kombinasyonu ile dışlanabilir.",
                masked_term="seri hCG düzeyleri",
                hint="Ders notunda ektopik gebeliği dışlamak için ultrasonla birlikte bakılması şart koşulan tekrarlayan hormon ölçümü"
            ),
            make_slider(
                left_title="Normal İntrauterin Canlı Gebelik",
                right_title="Ektopik Gebelik (Dış Gebelik)",
                left_points=[
                    "Serum hCG 48 saatte en az %50-66 katlanarak artar",
                    "Transvajinal USG'de kavite içinde düzgün gestasyonel kese izlenir",
                    "Adnekslerde kitle veya serbest peritoneal sıvı yoktur"
                ],
                right_points=[
                    "Serum hCG anormal plato çizer veya subnormal artar (<%35)",
                    "Uterus kavitesi boştur (psödogestasyonel kese olabilir)",
                    "Adneksiyel tubal kitle, halka belirtisi ve batında serbest sıvı saptanır"
                ]
            ),
            make_recall(
                question="Yardımcı üreme tekniği (IVF) ile gebe kalmış kanamalı bir kadında ultrasonda intrauterin canlı bir kese görülmesi ektopik gebeliği tamamen ekarte ettirir mi?",
                answer="Hayır, ettirmez. Tüp bebek gebeliklerinde 1/100 ila 1/500 gibi yüksek oranlarda intrauterin ve ekstrauterin gebeliğin aynı anda bulunduğu heterotopik gebelik görülebilir; adneksler mutlaka taranmalıdır."
            )
        ]
    ))

    # Slide 73
    slides.append(make_slide(
        slide_num=73,
        title="TV-USG Mihenk Taşı 1: Gestasyonel Kese (GS) ve Büyüme Hızı",
        subtitle="TV-USG'de 4-5. hf, TA-USG'de 6. hf; erken gebelikte GS günde 1 mm büyür",
        clinical_focus="Kesenin ilk tespiti ve normal büyüme hızının milimetrik kontrolü",
        narrative=(
            "Canlı gebeliğin teyidinde transvajinal ultrasonografi transabdominal ultrasonografiye göre yaklaşık 1-2 hafta erken tanı sağlar.\n\n"
            "- **Görülme Zamanı:** Gestasyonel kese (GS); **transvajinal USG'de 4-5. gebelik haftalarında**, **transabdominal USG'de ise 6. haftada** ilk kez görülür.\n"
            "- **Ultrasonik Görünüm:** Uterus kavitesi içinde ekojen kalın bir desidual halka (çift desidual halka belirtisi) içinde anekoik yuvarlak/oval sıvı alanıdır.\n"
            "- **Günlük Büyüme Hızı:** Ders notunun en kritik biyometrik kuralı: **Erken gebelikte GS günde 1 mm büyür**. Ortalama kese çapı (MSD), kesenin üç dikey boyutu toplanıp üçe bölünerek hesaplanır. Günlük 1 mm'lik büyümenin durması erken gelişimsel arrestin habercisidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Gestasyonel kese (GS) transvajinal USG'de 4-5. haftada, transabdominalde 6. haftada görülür; erken gebelikte GS günde 1 mm büyür."
        ),
        bullets=[
            "Gestasyonel kese TV-USG'de 4-5. haftada, karından USG'de 6. haftada izlenir",
            "Ekojen bir desidual halka içinde anekoik yuvarlak alan olarak tanımlanır",
            "Erken gebelikte gestasyonel kese günde ortalama 1 mm büyür",
            "Büyüme hızının günde 1 mm'nin altına düşmesi abortus şüphesi doğurur"
        ],
        elements=[
            make_quiz(
                question="Ders notunda belirtilen ultrasonografik mihenk taşlarına göre, gestasyonel kesenin (GS) transvajinal USG'de görülme haftası ve erken gebelikteki günlük büyüme hızı hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "TV-USG'de 8-10. hafta; günde 10 mm", "isCorrect": False, "explanation": "Aşırı geç ve hızlıdır."},
                    {"key": "B", "text": "TV-USG'de 4-5. hafta; günde 1 mm", "isCorrect": True, "explanation": "Doğru. Ders notu: 'GS transvajinal USG'de 4-5. haftalarda, TA-USG'de 6. haftada görülür; GS günde 1 mm büyür' kuralını verir."},
                    {"key": "C", "text": "TV-USG'de 12. hafta; haftada 1 mm", "isCorrect": False, "explanation": "Yanlış zamanlamadır."},
                    {"key": "D", "text": "Sadece doğum anında ölçülür", "isCorrect": False, "explanation": "Erken ilk trimester ölçümüdür."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre erken gebelik döneminde gestasyonel kese günde bir milimetre büyüme gösterir.",
                masked_term="bir milimetre",
                hint="Ders notunda gestasyonel kesenin günlük büyüme hızı (rakamla 1 mm)"
            ),
            make_slider(
                left_title="Transvajinal Ultrasonografi (TV-USG)",
                right_title="Transabdominal Ultrasonografi (TA-USG)",
                left_points=[
                    "Gestasyonel kese 4-5. haftada saptanır",
                    "Yüksek prob frekansı ile milimetrik erken çözünürlük",
                    "Mesanenin dolu olmasına ihtiyaç duymaz"
                ],
                right_points=[
                    "Gestasyonel kese ancak 6. haftada saptanabilir",
                    "Yaklaşık 1-2 hafta daha geç görüntüleme eşiği",
                    "İyi pencere için akustik dolu mesane gerektirir"
                ]
            ),
            make_recall(
                question="Transvajinal ultrasonda gestasyonel kesenin 5 gün arayla yapılan iki ölçümünde sadece 1 mm büyüdüğü saptanırsa bu durum neye işaret eder?",
                answer="Kesenin günde 1 mm büyüme kuralına uymadığını (5 günde en az 4-5 mm büyümesi gerekirdi), embriyonik gelişimin durakladığını ve yaklaşan bir abortus veya gelişimsel arrest olduğunu düşündürür."
            )
        ]
    ))

    # Slide 74
    slides.append(make_slide(
        slide_num=74,
        title="Kritik Eşik: hCG >2000 mIU/ml ve Kese Görülme Kuralı",
        subtitle="Diskriminatif zon eşiği; kese görülmezse ektopik gebelik alarmı",
        clinical_focus="Biyokimyasal değer ile ultrasonografik anatomik korelasyon",
        narrative=(
            "Klinik obstetride acil kararları belirleyen en ünlü sayısal kural hCG diskriminatif zon kuralıdır.\n\n"
            "- **Resmi Ders Notu Kuralı (BÜYÜK HARFLERLE ÖNEMLİ):** Amfi ders notunda ünlemle vurgulanmıştır: **'ÖNEMLİ: hCG >2000 mIU/ml ise mutlaka gebelik kesesi görülmelidir.'**\n"
            "- **Diskriminatif Zonun Anlamı:** Serum beta-hCG düzeyi 2000 mIU/ml ve üzerine çıktığında, normal bir intrauterin gebelikte transvajinal ultrasonografi ile kavite içinde gestasyonel kesenin saptanamaması tıbben imkansızdır.\n"
            "- **Klinik Alarm:** Eğer hastanın serum beta-hCG düzeyi **>2000 mIU/ml** olmasına rağmen transvajinal ultrasonda uterus kavitesi **boş** ise, aksi kanıtlanana kadar tanı **EKTOPİK GEBELİKTİR** (veya yeni tamamlanmış komplet abortustur). Hasta tubal rüptür riski nedeniyle derhal yakın takibe veya laparoskopi/medikal metotreksat protokolüne alınmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> ÖNEMLİ KURAL: Serum hCG >2000 mIU/ml ise transvajinal ultrasonda mutlaka gebelik kesesi görülmelidir."
        ),
        bullets=[
            "Ders notu kuralı: hCG >2000 mIU/ml ise mutlaka gebelik kesesi görülmelidir",
            "Bu değer transvajinal USG için kabul edilen diskriminatif zon eşiğidir",
            "hCG >2000 iken kavite boşsa ektopik gebelik şüphesi en üst düzeye çıkar",
            "Acil obstetride hayat kurtaran en kritik hormon-ultrason eşiğidir"
        ],
        elements=[
            make_quiz(
                question="Ders notunda 'ÖNEMLİ' vurgu kutusu ile belirtilen kurala göre, transvajinal ultrasonografide uterus içinde gebelik kesesinin MUTLAKA görülmesi gereken kritik serum hCG eşik düzeyi hangisidir?",
                options=[
                    {"key": "A", "text": "hCG >5 mIU/ml", "isCorrect": False, "explanation": "Bu gebelik pozitiflik alt sınırıdır, kese görülmez."},
                    {"key": "B", "text": "hCG >50 mIU/ml", "isCorrect": False, "explanation": "Çok erken biyokimyasal evredir."},
                    {"key": "C", "text": "hCG >2000 mIU/ml", "isCorrect": True, "explanation": "Doğru. Ders notundaki resmi ifade: 'ÖNEMLİ: hCG >2000 mIU/ml ise mutlaka gebelik kesesi görülmelidir' kuralıdır."},
                    {"key": "D", "text": "hCG >500.000 mIU/ml", "isCorrect": False, "explanation": "Koryokarsinom seviyesidir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notuna göre kandaki hormon değeri iki bin mIU/ml üzerinde ise transvajinal ultrasonda mutlaka gebelik kesesi görülmelidir.",
                masked_term="iki bin mIU/ml üzerinde",
                hint="Ders notunda gebelik kesesinin mutlaka görülmesi şart koşulan kritik hCG seviyesi (>2000)"
            ),
            make_chain(
                title="hCG >2000 mIU/ml ve Boş Uterus Klinik Karar Kaskadı",
                steps=[
                    "Laboratuvar Tespiti: Kanamalı hastada serum kantitatif beta-hCG'nin 2400 mIU/ml (>2000) saptanması",
                    "Ultrasonografik İnceleme: Transvajinal ultrasonda uterus kavitesinin tamamen boş olduğunun görülmesi",
                    "Diskriminatif İhlal: Kese görülmesi gereken eşik aşılmasına rağmen intrauterin kesenin bulunamaması",
                    "Ektopik Gebelik Yönetimi: Rüptüre olmamış ektopik gebelik ön tanısıyla acil adneks taraması ve tedavi protokolü"
                ]
            ),
            make_recall(
                question="Serum beta-hCG düzeyi 3500 mIU/ml olan asemptomatik bir gebenin transvajinal ultrasonunda kavitede gebelik kesesi izlenmezse ilk şüphelenilmesi gereken patoloji nedir?",
                answer="Ektopik gebeliktir (dış gebelik); çünkü hCG >2000 mIU/ml eşiğini geçtiği halde kavitede kese izlenmemesi normal intrauterin gebelik kuralına uymaz."
            )
        ]
    ))

    # Slide 75
    slides.append(make_slide(
        slide_num=75,
        title="TV-USG Mihenk Taşı 2: Yolk Sac ve Fetal Pole",
        subtitle="Yolk sac 5. hf; Fetal pole 6. hf TV-USG ile yolk sac kenarında kalınlaşma",
        clinical_focus="İntrauterin gerçek gebelik kesesinin doğrulanması ve embriyonik beliriş",
        narrative=(
            "Gestasyonel kese görüldükten sonra gelişimin devam ettiğini kanıtlayan iki ardışık yapı yolk sac ve fetal poledur.\n\n"
            "- **Yolk Sac (Vitellin Kese):** Gestasyonel kese içerisinde ortası anekoik, kenarları ince ekojen bir yüzük şeklinde izlenir. Ders notuna göre **5. gebelik haftasından itibaren** görülür. Yolk kesesinin görülmesi, görüntünün psödogestasyonel kese (yalancı kese) olmadığını ve kesin intrauterin bir gebelik olduğunu kanıtlar.\n"
            "- **Fetal Pole (Embriyo):** Amfi ders notundaki resmi tanımla: **'6. haftada transvajinal USG ile yolk sak kenarında kalınlaşma olarak görülmeye başlar.'**\n"
            "- **Fetal Kalp Atımı (FKA):** Ders notu kuralı: **'Fetal kalp atımı: Fetal pole görüntülendikten sonra tespit edilmeye başlar.'** Embriyo boyutu 2-4 mm'ye ulaştığında dakikada 100-110 atım ile başlayan ritmik flicker hareketi M-mod veya Doppler ile kaydedilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Yolk sac 5. haftadan itibaren; Fetal pole ise 6. haftada TV-USG ile yolk sac kenarında kalınlaşma olarak izlenir."
        ),
        bullets=[
            "Yolk sac (yüzük görüntüsü) 5. gebelik haftasından itibaren saptanır",
            "Yolk sac varlığı intrauterin gebeliğin kesin anatomik kanıtıdır",
            "Fetal pole 6. haftada yolk sac kenarında kalınlaşma olarak belirir",
            "Fetal kalp atımı fetal pole görüntülendikten hemen sonra saptanır"
        ],
        elements=[
            make_quiz(
                question="Ders notunda yer alan transvajinal ultrasonografi mihenk taşlarına göre, yolk sac ve fetal pole'ün ilk görülme zamanları ve fetal pole'ün ilk ultrasonik görünümü hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "Yolk sac 3. hf; Fetal pole 10. hf plasenta içinde kitle", "isCorrect": False, "explanation": "Haftalar ve lokalizasyon yanlıştır."},
                    {"key": "B", "text": "Yolk sac 5. hf; Fetal pole 6. haftada yolk sak kenarında kalınlaşma olarak", "isCorrect": True, "explanation": "Doğru. Ders notundaki net ifadeler: 'Yolk sac 5. haftadan itibaren; Fetal pole 6. haftada yolk sak kenarında kalınlaşma olarak görülür' şeklindedir."},
                    {"key": "C", "text": "Yolk sac hiç görülmez; fetal pole sadece 20. haftada kemikleşir", "isCorrect": False, "explanation": "Embriyolojik gerçek dışıdır."},
                    {"key": "D", "text": "Her iki yapı da aynı anda 12. haftada belirir", "isCorrect": False, "explanation": "Çok geçtir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre fetal pole altıncı haftada transvajinal ultrasonografi ile yolk sak kenarında kalınlaşma şeklinde izlenmeye başlar.",
                masked_term="yolk sak kenarında kalınlaşma",
                hint="Ders notunda fetal pole'ün 6. haftadaki transvajinal ilk görünüm tarifi"
            ),
            make_table(
                title="İlk Trimester Ultrasonik Gelişim Kronolojisi",
                headers=["Gebelik Haftası", "Beliren Ultrasonik Yapı", "Morfolojik Görünüm"],
                rows=[
                    [
                        {"text": "4-5. Hafta (TV-USG)", "isMasked": False},
                        {"text": "Gestasyonel Kese (GS)", "isMasked": True, "hint": "Uterustaki lümen içi anekoik kaviter oluşum"},
                        {"text": "Ekojen halkalı anekoik alan; günde 1 mm büyür", "isMasked": False}
                    ],
                    [
                        {"text": "5. Hafta", "isMasked": False},
                        {"text": "Yolk Sac (Vitellin Kese)", "isMasked": True, "hint": "Lümen içi ilk yuvarlak yüzük yapısı"},
                        {"text": "Kese içinde anekoik yuvarlak yüzük", "isMasked": False}
                    ],
                    [
                        {"text": "6. Hafta", "isMasked": False},
                        {"text": "Fetal Pole ve Kalp Atımı", "isMasked": True, "hint": "İlk embriyonik doku ve FKA"},
                        {"text": "Yolk sac kenarında kalınlaşma; FKA başlar", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Transvajinal ultrasonda gestasyonel kese içinde yolk sac görüldükten sonra fetal kalp aktivitesinin ne zaman tespit edilmesi beklenir?",
                answer="6. haftada fetal pole yolk sac kenarında bir kalınlaşma olarak belirdikten hemen sonra fetal kalp atımının tespit edilmesi beklenir."
            )
        ]
    ))

    # Slide 76
    slides.append(make_slide(
        slide_num=76,
        title="TV-USG Mihenk Taşı 3: CRL Ölçümü ve Pratik Formül",
        subtitle="Crown-rump length 7-14. hafta; 6 hafta + CRL(mm) = 6 hafta + gün formülü",
        clinical_focus="Gebelik yaşının en hassas tayini ve amfi dersinin pratik hesabı",
        narrative=(
            "Gebelik haftasını ve tahmini doğum tarihini belirlemede tüm obstetrik sürecin en güvenilir biyometrik parametresi CRL'dir.\n\n"
            "- **Geçerlilik Aralığı:** Ders notuna göre **Crown-rump length (CRL) 7-14. haftalar arasında** gebelik yaşı ölçümünde kullanılır.\n"
            "- **Ölçüm Tekniği:** Embriyonun uzun ekseninde başın en üst noktası (crown) ile kalçanın en alt noktası (rump) arasındaki mesafe düz bir çizgiyle ölçülür. Ders notunda açıkça belirtildiği üzere: **embriyonun uzun ekseni yolk sak veya ekstremiteleri içine alınmadan ölçülür**.\n"
            "- **Resmi Pratik Formül:** Amfi ders notunda öğretim üyesinin vurguladığı pratik klinik yaklaşım:\n"
            "  **6 hafta + CRL (mm) = 6 hafta + gün** formülüdür.\n"
            "- **Örnek Hesaplama:** CRL boyutu 9 mm ölçülen bir embriyoda: 6 hafta + 9 gün = 7 hafta 2 günlük gebelik yaşı bulunur.\n\n"
            "> [!IMPORTANT]\n"
            "> CRL 7-14. haftalarda kullanılır; yolk sac/ekstremite dahil edilmez. Pratik formül: 6 hafta + CRL(mm) = 6 hafta + gün."
        ),
        bullets=[
            "CRL ölçümü 7-14. gebelik haftaları arasında en güvenilir yaş belirtecidir",
            "Ölçüme yolk sac veya ekstremiteler kesinlikle dahil edilmez",
            "Ders notu pratik formülü: 6 hafta + CRL(mm) = 6 hafta + gün eşitliğidir",
            "Tüm gebelik boyunca biyometrik yaş tayininde hata payı en düşük parametredir (±3-5 gün)"
        ],
        elements=[
            make_quiz(
                question="Ders notunda yer alan pratik yaklaşıma göre, transvajinal ultrasonografide CRL ölçümü 12 mm olarak saptanan bir embriyonun gebelik haftası ve günü hangisinde doğru hesaplanmıştır? (Formül: 6 hafta + CRL mm = 6 hafta + gün)",
                options=[
                    {"key": "A", "text": "6 hafta 2 gün", "isCorrect": False, "explanation": "12 mm 12 gündür, 6 hafta + 12 gün = 7 hafta 5 gün eder."},
                    {"key": "B", "text": "12 hafta 0 gün", "isCorrect": False, "explanation": "CRL mm doğrudan hafta değildir."},
                    {"key": "C", "text": "7 hafta 5 gün", "isCorrect": True, "explanation": "Doğru. 6 hafta + 12 gün = 6 hafta + 1 hafta 5 gün = 7 hafta 5 gün olarak hesaplanır."},
                    {"key": "D", "text": "20 hafta 0 gün", "isCorrect": False, "explanation": "Hatalı hesaptır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notuna göre Crown-rump length ölçümünde embriyonun uzun ekseni ölçülürken yolk sak veya ekstremiteleri içine alınmadan ölçülür.",
                masked_term="yolk sak veya ekstremiteleri",
                hint="Ders notunda CRL ölçüm cetveline dahil edilmemesi emredilen anatomik yapılar"
            ),
            make_chain(
                title="Doğru CRL Ölçüm ve Yaş Hesaplama Protokolü",
                steps=[
                    "Doğru Büyütme ve Kesit: Embriyonun sagital düzlemde tüm uzun ekseni boyunca ekrana net büyütülmesi",
                    "Ayrıştırma Kuralı: Kalipırların yolk kesesine veya beliren fetal kol/bacak uzantılarına değdirilmemesi",
                    "Kalipır Yerleşimi: Başın en tepe dış sınırı (crown) ile kuyruk sokumu dış sınırı (rump) arasına yerleştirilmesi",
                    "Pratik Dönüşüm: Ölçülen milimetre değerinin '6 hafta + CRL mm = 6 hafta + gün' formülüyle gebelik yaşına çevrilmesi"
                ]
            ),
            make_recall(
                question="Neden CRL ölçümüne yolk kesesi veya uzuvların (ekstremiteler) dahil edilmesi kesinlikle yasaktır?",
                answer="Çünkü yolk kesesi veya ekstremitelerin ölçüme katılması baş-popo uzunluğunu yapay olarak büyüterek gebelik haftasının olduğundan ileri hesaplanmasına ve yanlış doğum tarihi belirlenmesine yol açar."
            )
        ]
    ))

    # Slide 77
    slides.append(make_slide(
        slide_num=77,
        title="Tahmini Doğum Tarihi ve SAT-USG Diskordans Kuralları",
        subtitle="1. trimesterde 7 günlük fark önemsiz; 2. trimesterde 10 günlük fark önemsizdir",
        clinical_focus="Son adet tarihine göre düzeltilmiş gebelik yaşı ve ultrasonik sınır toleransları",
        narrative=(
            "Klinik obstetride gebenin bildirdiği son adet tarihi (SAT) ile ultrasonda ölçülen gebelik yaşı arasında sıklıkla birkaç günlük uyumsuzluklar saptanır.\n\n"
            "- **Resmi Ders Notu Tolerans Kuralı:** Amfi ders notunda net olarak bildirildiği üzere:\n"
            "  * **İlk trimesterde SAT ile USG arasında 7 günlük fark önemsizdir.** (Fark ≤7 gün ise gebelik SAT'a göre takip edilir; fark >7 gün ise gebelik yaşı ultrasona göre yeniden tarihlendirilir / redating).\n"
            "  * **İkinci trimesterde ise 10 günlük fark önemsizdir.** (Fark >10 gün ise ultrason tarihi esas alınır).\n"
            "- **Biyolojik Mantık:** İlk trimesterde embriyoların büyüme hızları birbirine çok yakındır ve biyolojik varyasyon düşüktür (±7 gün tolerans). İkinci trimesterde genetik ve ailesel büyüme farklılıkları devreye girdiğinden tolerans sınırı 10 güne genişletilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Tahmini doğum tarihi kuralı: İlk trimesterde SAT ile USG arasında 7 günlük fark önemsizdir; 2. trimesterde 10 günlük fark önemsizdir."
        ),
        bullets=[
            "İlk trimesterde SAT ile USG arasında 7 güne kadar olan fark önemsiz kabul edilir",
            "Fark >7 gün ise tahmini doğum tarihi ilk trimester ultrasonuna göre düzeltilir",
            "İkinci trimesterde kabul edilebilir önemsiz fark sınırı 10 gündür",
            "Erken trimester ultrasonu doğum tarihini belirlemede son adet tarihinden daha üstündür"
        ],
        elements=[
            make_quiz(
                question="Ders notunda belirtilen tahmini doğum tarihi ve gebelik yaşı düzeltme kurallarına göre, trimesterlerde SAT ile ultrasonografi arasında 'önemsiz' kabul edilen gün farkı sınırları hangisinde eksiksiz verilmiştir?",
                options=[
                    {"key": "A", "text": "İlk trimesterde 1 gün; 2. trimesterde 3 gün", "isCorrect": False, "explanation": "Toleranslar çok dardır."},
                    {"key": "B", "text": "İlk trimesterde 7 günlük fark önemsizdir; 2. trimesterde 10 günlük fark önemsizdir", "isCorrect": True, "explanation": "Doğru. Ders notu aynen: 'İlk trimesterde SAT ile USG arasında 7 günlük fark önemsizdir; 2. trimesterde 10 günlük fark önemsizdir' kuralını verir."},
                    {"key": "C", "text": "İlk trimesterde 30 gün; 2. trimesterde 60 gün", "isCorrect": False, "explanation": "Aşırı geniştir."},
                    {"key": "D", "text": "Hiçbir fark önemsiz değildir, her farkta küretaj yapılır", "isCorrect": False, "explanation": "Tıbbi saçmalıktır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre ilk trimesterde son adet tarihi ile ultrason ölçümü arasında yedi günlük fark önemsizdir.",
                masked_term="yedi günlük fark",
                hint="Ders notunda ilk trimesterde SAT ile USG arasında önemsiz kabul edilen gün sınırı (rakamla 7 gün)"
            ),
            make_table(
                title="Trimesterlere Göre SAT-USG Diskordans Toleransları",
                headers=["Trimester Dönemi", "Önemsiz Kabul Edilen Fark", "Klinik Yönetim Kararı"],
                rows=[
                    [
                        {"text": "1. Trimester (İlk Trimester)", "isMasked": False},
                        {"text": "7 günlük fark önemsizdir", "isMasked": True, "hint": "İlk trimester tolerans gün sayısı"},
                        {"text": "Fark ≤7 gün ise SAT korunur; >7 gün ise USG'ye göre düzeltilir", "isMasked": False}
                    ],
                    [
                        {"text": "2. Trimester (İkinci Trimester)", "isMasked": False},
                        {"text": "10 günlük fark önemsizdir", "isMasked": True, "hint": "İkinci trimester tolerans gün sayısı"},
                        {"text": "Fark ≤10 gün ise SAT korunur; >10 gün ise USG'ye göre düzeltilir", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="İlk trimesterde son adet tarihine göre 8 hafta 0 günlük olan bir gebenin ultrason ölçümü 8 hafta 4 gün (4 gün fark) gelirse tahmini doğum tarihi değiştirilir mi?",
                answer="Hayır, değiştirilmez. Çünkü ilk trimesterde 7 güne kadar olan farklar önemsiz kabul edilir; 4 günlük fark bu sınırın içinde kaldığından hastanın son adet tarihi (SAT) esas alınarak takibe devam edilir."
            )
        ]
    ))

    # Slide 78
    slides.append(make_slide(
        slide_num=78,
        title="İlk Trimester Ayırıcı Tanısı 1: Subkoryonik Hematom",
        subtitle="Koryon frondosum ile desidua arasında kanama; düşük tehdidinden kayba ilerleyiş",
        clinical_focus="Ultrasonografik kresentik ekojenite ve hematom boyutunun risk korelasyonu",
        narrative=(
            "İlk trimester kanaması ile başvuran canlı gebeliklerde ultrasonda en sık saptanan patolojik antite subkoryonik hematomdur.\n\n"
            "- **Resmi Ders Notu Tanımı:** Amfi ders notunda ayırıcı tanı başlığı altında yer alır: **'Subkoryonik hematom: genellikle vajinal kanama ile seyreder → düşük tehdidi → gebelik kaybı.'**\n"
            "- **Patolojik Mekanizma:** Gelişmekte olan koryonik villusların maternal desidua bazalisten kısmi olarak ayrılması sonucu aradaki marjinal venöz sinüsler yırtılır. Koryon zarı ile desidua arasında retrokoryonik kan göllenmesi (hematom) oluşur.\n"
            "- **Ultrasonik Görünüm:** Gestasyonel kesenin kenarına komşu, kresentik (hilal şeklinde) anekoik veya mikst ekojenik sıvı koleksiyonudur.\n"
            "- **Klinik Risk:** Çoğu küçük hematom spontan rezorbe olurken; hematom hacminin kese çevresinin >%50'sini aşması durumunda plasental beslenme bozulur, düşük tehdidi (imminens) kaçınılmaz gebelik kaybına ilerleyebilir.\n\n"
            "> [!NOTE]\n"
            "> Subkoryonik hematom genellikle vajinal kanama ile seyreder; düşük tehdidine (abortus imminens) ve gebelik kaybına yol açabilir."
        ),
        bullets=[
            "Koryonik membranlar ile desidua arasında kan birikmesidir",
            "Ders notuna göre: Genellikle kanama ile seyreder → düşük tehdidi → kayıp",
            "Ultrasonda kese kenarında hilal şeklinde anekoik koleksiyon izlenir",
            "Hematom boyutu kese çevresinin yarısını aştığında düşük riski yükselir"
        ],
        elements=[
            make_quiz(
                question="Ders notunda erken gebelik kanamalarının ayırıcı tanısında yer alan ve 'genellikle vajinal kanama ile seyreder → düşük tehdidi → gebelik kaybı' patolojik zinciri ile tanımlanan durum hangisidir?",
                options=[
                    {"key": "A", "text": "Subkoryonik hematom", "isCorrect": True, "explanation": "Doğru. Ders notu bu sıralamayı doğrudan subkoryonik hematom başlığı altında vermiştir."},
                    {"key": "B", "text": "Asherman sendromu", "isCorrect": False, "explanation": "Uterin yapışıklıktır, akut hematom zinciri değildir."},
                    {"key": "C", "text": "Turner sendromu (45,X0)", "isCorrect": False, "explanation": "Kromozomal anomalidir."},
                    {"key": "D", "text": "Akut apandisit", "isCorrect": False, "explanation": "Gastrointestinal enfeksiyondur."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Ders notuna göre subkoryonik hematom genellikle vajinal kanama ile seyrederek düşük tehdidine ve gebelik kaybına yol açabilir.",
                masked_term="subkoryonik hematom",
                hint="Ders notundaki ayırıcı tanı başlığı: koryon zarı altında kan toplanması tablosu"
            ),
            make_chain(
                title="Ders Notu Subkoryonik Hematom Klinik Seyir Zinciri",
                steps=[
                    "Desidual Venöz Yırtılma: Koryonik villusların marjinal venöz sinüslerinden ayrılması ve retrokoryonik kan birikimi",
                    "Klinik Başvuru (Genellikle Vajinal Kanama): Kanamanın servikal ostan dışarı sızarak hastada ilk trimester kanaması yapması",
                    "Düşük Tehdidi (Abortus İmminens): Ultrasonda canlı embriyoya eşlik eden kresentik hematomun saptanması",
                    "Gebelik Kaybı Riski: Hematomun genişleyerek desidual ayrılmayı artırması ve gebeliğin sonlanması"
                ]
            ),
            make_recall(
                question="Subkoryonik hematom saptanan kanamalı bir gebede gebelik kaybı riskini belirleyen en önemli ultrasonografik faktör nedir?",
                answer="Hematomun gestasyonel keseye göre rölatif boyutudur; kese çevresinin %50'sinden büyük olan hematomlarda gebelik kaybı riski belirgin şekilde yüksektir."
            )
        ]
    ))

    # Slide 79
    slides.append(make_slide(
        slide_num=79,
        title="İlk Trimester Ayırıcı Tanısı 2: Trofoblastik Hastalık ve Servikovajinal Nedenler",
        subtitle="Gestasyonel trofoblastik hastalık, aşırı yüksek hCG, teka lutein kistleri; servisit ve polipler",
        clinical_focus="Karışık ekojenik intrauterin patern ve temas kanamalarının ayırıcı tanısı",
        narrative=(
            "Kanamalı erken gebede ultrason ve fizik muayene diğer non-abortif patolojileri aydınlatır.\n\n"
            "- **Gestasyonel Trofoblastik Hastalık (Mol Hidatiform):** Ders notundaki tam tarifle: **'Gebelikte kanama, gebelik yaşına göre beklenenden daha büyük uterus boyutu, anormal derecede yüksek β-hCG düzeyleri (>100.000 mIU/ml), hiperemesis gravidarum ve ultrasonda uterus içinde yaygın karışık ekojenik patern (kar fırtınası / veziküler görünüm) ile maternal overlerde kistik büyüme (teka lutein kistleri).'**\n"
            "- **Servikal ve Vajinal Patolojiler:** Kanama her zaman uterus içinden kaynaklanmaz. Ders notuna göre: **'Postkoital veya temas kanaması durumunda enfeksiyöz servisit, servikal polipler, ektropion, displazi veya travma düşünülmelidir.'**\n"
            "- **Sentez:** Spekulum takılmadan yapılan bir muayene servikal polip kanamasını abortus zannedilmesine yol açabilir; bu nedenle spekulum muayenesi asla atlanamaz.\n\n"
            "> [!IMPORTANT]\n"
            "> Beklenenden büyük uterus, aşırı yüksek hCG ve kistik overler mol hidatiformu; postkoital temas kanaması ise servisit/polip/ektropionu düşündürür."
        ),
        bullets=[
            "Mol: Büyük uterus, aşırı yüksek hCG, hiperemezis, karışık ekojenite ve teka lutein",
            "Teka lutein kistleri aşırı hCG uyarısıyla overlerin bilateral kistik büyümesidir",
            "Servikal/vajinal nedenler: Enfeksiyöz servisit, servikal polip, ektropion ve travma",
            "Postkoital (ilişki sonrası) veya spekulum temas kanaması servikal patolojileri işaret eder"
        ],
        elements=[
            make_quiz(
                question="İlk trimesterde vajinal kanama ile başvuran bir kadında; gebelik haftasına göre beklenenden daha büyük uterus boyutu, anormal derecede yüksek β-hCG düzeyleri, hiperemesis gravidarum, ultrasonda yaygın karışık ekojenik patern ve overlerde kistik büyüme saptanıyor. Ders notuna göre en olası tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Abortus imminens", "isCorrect": False, "explanation": "Uterus haftasıyla uyumludur, hCG normaldir."},
                    {"key": "B", "text": "Gestasyonel trofoblastik hastalık (Mol hidatiform)", "isCorrect": True, "explanation": "Doğru. Ders notundaki mol hidatiform klinik ve ultrasonik tanımının birebir karşılığıdır."},
                    {"key": "C", "text": "Ektopik gebelik", "isCorrect": False, "explanation": "Ektopik gebelikte uterus küçüktür ve hCG düşüktür."},
                    {"key": "D", "text": "Missed abortus", "isCorrect": False, "explanation": "Uterus küçüktür ve hCG düşüştedir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre postkoital veya temas kanaması varlığında enfeksiyöz servisit, servikal polipler, ektropion veya travma düşünülmelidir.",
                masked_term="servikal polipler",
                hint="Ders notunda temas kanaması yapabileceği belirtilen iyi huylu mukozal kitle lezyonları"
            ),
            make_slider(
                left_title="Gestasyonel Trofoblastik Hastalık",
                right_title="Servikal ve Vajinal Patolojiler",
                left_points=[
                    "Uterus haftasına göre belirgin büyüktür",
                    "Beta-hCG anormal derecede yüksektir (>100.000)",
                    "Ultrasonda kavitary veziküler ekojenite ve teka lutein kistleri izlenir"
                ],
                right_points=[
                    "Uterus boyutu ve gebelik haftası tamamen normaldir",
                    "Beta-hCG seviyesi normal gestasyonel aralıktadır",
                    "Spekulumda eksternal osta polip, erozyon veya servisit akıntısı izlenir"
                ]
            ),
            make_recall(
                question="Mol hidatiform vakalarında overlerde bilateral multikistik büyüme (teka lutein kistleri) izlenmesinin endokrinolojik mekanizması nedir?",
                answer="Prolifere trofoblastik dokunun dolaşıma anormal derecede yüksek miktarda beta-hCG salgılaması ve hCG'nin LH reseptörlerini aşırı uyararak teka hücrelerini luteinize edip kistleştirmesidir."
            )
        ]
    ))

    # Slide 80 (Checkpoint 8)
    slides.append(make_slide(
        slide_num=80,
        title="[TEKRAR SAYFASI - CHECKPOINT 8] Kanamalı Hastaya Yaklaşım ve TV-USG",
        subtitle="İlk testler, ayırıcı tanı, hCG >2000 eşiği, ultrason haftaları ve CRL formülü",
        clinical_focus="Erken gebelik kanamalarının acil değerlendirmesi ve ultrasonik ölçümlerin tam entegrasyonu",
        narrative=(
            "Bu tekrar sayfası, 71-79. adımlarda işlenen İlk Trimester Kanamalı Hastaya Yaklaşım ve Ultrasonografi mihenk taşlarını sentezler.\n\n"
            "- **İnsidans ve Testler:** Kanama tüm gebelerin **%20-40'ında** görülür. İlk testler: **CBC, KG (kan grubu), Rh ve hCG**.\n"
            "- **Ayırıcı Tanı:** Ektopik gebelik, abortus ve normal gebelik ayrılır; ektopik gebelik **seri hCG ve ultrason kombinasyonu** ile dışlanır. Subkoryonik hematom, trofoblastik hastalık ve servikal lezyonlar akılda tutulur.\n"
            "- **USG Mihenk Taşları:** Gestasyonel kese TV-USG'de **4-5. hf**, TA-USG'de **6. hf**; GS erken gebelikte **günde 1 mm büyür**. **hCG >2000 mIU/ml ise mutlaka kese görülmelidir**.\n"
            "- **Embriyo ve Yaş:** Yolk sac **5. hf'tan** itibaren; Fetal pole **6. hf'ta** yolk sac kenarında kalınlaşma olarak izlenir. CRL **7-14. haftada** kullanılır; **6 hafta + CRL(mm) = 6 hafta + gün**. SAT-USG farkı: **1. trimesterde 7 gün**, **2. trimesterde 10 gün** önemsizdir.\n\n"
            "> [!IMPORTANT]\n"
            "> Testler: CBC, KG, Rh, hCG | Eşik: hCG >2000 kese görülmeli | Formül: 6 hafta + CRL mm = 6 hf + gün | Tolerans: 1. trim 7 gün, 2. trim 10 gün."
        ),
        bullets=[
            "İlk testler: CBC, kan grubu, Rh faktörü ve serum hCG ölçümüdür",
            "hCG >2000 mIU/ml iken transvajinal ultrasonda mutlaka kese görülmelidir",
            "Kese TV-USG'de 4-5. hf görülür ve günde 1 mm büyüme gösterir",
            "Yolk sac 5. hf; Fetal pole 6. hf'ta yolk sac kenarında kalınlaşmadır",
            "CRL formülü: 6 hafta + CRL(mm) = 6 hafta + gün; 1. trim toleransı 7 gündür"
        ],
        elements=[
            make_quiz(
                question="İlk trimester ultrasonografisi ve kanamalı hastaya yaklaşımla ilgili aşağıdaki eşleştirmelerden hangisi amfi ders notuna göre KESİNLİKLE DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Gestasyonel kese TV-USG'de 10. haftada görülür ve günde 10 cm büyür", "isCorrect": False, "explanation": "Hafta ve büyüme hızı tamamen yanlıştır."},
                    {"key": "B", "text": "hCG >2000 mIU/ml ise mutlaka gebelik kesesi görülmelidir; 1. trimesterde SAT ile USG arasında 7 günlük fark önemsizdir", "isCorrect": True, "explanation": "Doğru. Ders notundaki iki en kritik obstetrik kuralı eksiksiz içeren doğrudur."},
                    {"key": "C", "text": "CRL ölçümüne yolk kesesi ve kollar mutlaka dahil edilmelidir", "isCorrect": False, "explanation": "Yolk sac ve uzuvlar kesinlikle dahil edilmez."},
                    {"key": "D", "text": "İlk trimester kanamalarında Rh faktörüne bakmaya gerek yoktur", "isCorrect": False, "explanation": "Rh tayini ilk başvuru testidir, Anti-D için şarttır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre transvajinal ultrasonda fetal pole altıncı haftada yolk sak kenarında kalınlaşma olarak izlenmeye başlar.",
                masked_term="altıncı haftada",
                hint="Ders notunda fetal pole morfolojisinin transvajinal USG ile belirdiği resmi zaman dilimi"
            ),
            make_table(
                title="Bölüm 8 Altın Mihenk Taşları Sentez Tablosu (Checkpoint 8)",
                headers=["Ultrasonik / Klinik Parametre", "Ders Notu Resmi Değeri / Kuralı", "Klinik Anlamı"],
                rows=[
                    [
                        {"text": "Diskriminatif Zon Kuralı", "isMasked": False},
                        {"text": "hCG >2000 mIU/ml ise kese görülmeli", "isMasked": True, "hint": "Kaviter yapının mutlaka izlenmesi gereken eşik değer"},
                        {"text": "Aşılırsa boş uterusta ektopik gebelik alarmı", "isMasked": False}
                    ],
                    [
                        {"text": "Gestasyonel Kese Büyüme Hızı", "isMasked": False},
                        {"text": "Erken gebelikte günde 1 mm büyür", "isMasked": True, "hint": "Kavitenin 24 saatlik milimetrik ilerleme temposu"},
                        {"text": "Biyometrik canlılık ve gelişim takibi", "isMasked": False}
                    ],
                    [
                        {"text": "CRL Yaş Hesaplama Formülü", "isMasked": False},
                        {"text": "6 hafta + CRL(mm) = 6 hafta + gün", "isMasked": True, "hint": "Pratik biyometri eşitliği"},
                        {"text": "7-14. haftalarda en hassas yaş tayini", "isMasked": False}
                    ],
                    [
                        {"text": "SAT-USG Fark Toleransı", "isMasked": False},
                        {"text": "1. trim 7 gün; 2. trim 10 gün önemsiz", "isMasked": True, "hint": "Dönemlere göre göz ardı edilen sapma süreleri"},
                        {"text": "Tahmini doğum tarihini düzeltme kriteri", "isMasked": False}
                    ]
                ]
            ),
            make_branching(
                scenario="Acil servise 6 haftalık kanamalı bir gebe başvuruyor. Yapılan tetkik sonuçlarına göre klinik karar verilecektir.",
                options=[
                    {
                        "text": "Serum hCG 2800 mIU/ml saptanıp transvajinal ultrasonda uterus boş ve sağ adnekste 2 cm halka belirtisi görülürse ektopik gebelik tanısıyla acil yönetime geçilir.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. hCG >2000 iken kavitenin boş olması ektopik gebelik için patognomoniktir."
                    },
                    {
                        "text": "Hastada hCG 2500 mIU/ml ve kavite boş olmasına rağmen hiçbir şey yapılmadan 1 ay sonraya randevu verilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Tubal rüptür ve ölümcül intraabdominal kanama riski doğurur."
                    },
                    {
                        "text": "İlk başvuruda kan grubu ve Rh bakılmasına gerek yoktur denilerek test iptal edilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Rh tayini ilk başvuruda istenmesi zorunlu temel testtir."
                    }
                ]
            ),
            make_recall(
                question="Bölüm 8'in en kritik klinik spotu olan 'hCG diskriminatif zonu' ve 'CRL pratik formülü' kurallarını özetleyiniz.",
                answer="Kural 1: hCG >2000 mIU/ml ise transvajinal ultrasonda mutlaka gebelik kesesi görülmelidir. Kural 2: 7-14. haftalarda pratik gebelik yaşı '6 hafta + CRL(mm) = 6 hafta + gün' formülü ile hesaplanır."
            )
        ]
    ))

    return slides
