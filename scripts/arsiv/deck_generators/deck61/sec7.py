# -*- coding: utf-8 -*-
"""
Deck 61 Section 7: Septik Düşük ve İleri Komplikasyonlar
Slides 61-70 (Checkpoint 7 at slide 70)
Focus:
- Septik düşük tanımı ve insidansı: Abortus sonrası %1-2 oranında enfeksiyon/sepsis gelişimi
- Maternal mortalite verisi: 100.000 medikal düşükte 0.58 maternal ölüm oranı
- Septik abortus etiyolojisi ve mikrobiyolojisi: Polimikrobiyal asendan enfeksiyon (Grup B streptokok, E. coli, anaeroplar, Clostridium perfringens)
- Klinik tablo ve tanı kriterleri: Yüksek ateş (>38°C), kötü kokulu pürülan vajinal akıntı, pelvik ve rebound hassasiyet, lökositoz
- Acil medikal yönetim: Erken geniş spektrumlu intravenöz (IV) antimikrobiyal tedavi kombinasyonları
- Cerrahi yönetim: Rest (retansiyone doku) varlığında IV antibiyoterapi sonrası uterusun cerrahi boşaltılması
- Önleyici profilaksi ilkesi: Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanması
- Ağır komplikasyonlar: Pelvik apse, septik tromboflebit, septik şok, nekrotizan miyometrit ve acil histerektomi endikasyonu
- Kriminal/güvensiz düşükler ve global obstetrik halk sağlığı önemi
- Checkpoint 7 (Tekrar ve pekiştirme sayfası)
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

def get_sec7_slides():
    slides = []

    # Slide 61
    slides.append(make_slide(
        slide_num=61,
        title="Septik Düşük: Tanım ve Epidemiyolojik İnsidans",
        subtitle="Abortus sonrası %1-2 oranında enfeksiyon/sepsis gelişimi",
        clinical_focus="Erken gebelik kaybının en ölümcül komplikasyonu olan pelvik enfeksiyon",
        narrative=(
            "Spontan veya indüklenmiş abortus süreçlerinin en korkulan ve hayatı tehdit eden komplikasyonu septik düşüktür.\n\n"
            "- **Resmi Tanım ve Kapsam:** Düşük öncesinde, düşüğün gerçekleştiği sırada veya abortus sonrasında endometrium, miyometrium ve pelvik dokuların enfeksiyon kaparak sistemik inflamatuvar yanıta ve sepsise ilerlemesi tablosudur.\n"
            "- **İnsidans Oranı:** Amfi ders notunda açıkça vurgulandığı üzere; **abortus sonrası %1-2 oranında enfeksiyon/sepsis** gelişimi izlenir.\n"
            "- **Risk Zeminleri:** Özellikle kavitede fetoplasental doku artıklarının uzun süre kalması (inkomplet veya uzamış missed abortus), steril olmayan cerrahi aletlerle yapılan merdiven altı müdahaleler ve gecikmiş başvurular septik tabloya zemin hazırlar. Erken tanı ve parenteral tedavi maternal hayatı kurtarır.\n\n"
            "> [!IMPORTANT]\n"
            "> Ders notuna göre abortus sonrası %1-2 oranında enfeksiyon ve sepsis gelişimi izlenir."
        ),
        bullets=[
            "Abortusların yaklaşık %1-2'sinde pelvik enfeksiyon ve sepsis gelişir",
            "Endometrit, miyometrit ve parametrit basamaklarıyla pelvise yayılır",
            "Kavitede kalan nekrotik dokular bakteriyel üreme için ideal besiyeridir",
            "Maternal mortaliteyi önlemede en kritik acil obstetrik tablodur"
        ],
        elements=[
            make_quiz(
                question="Amfi ders notunda yer alan resmi epidemiyolojik verilere göre, abortus sonrasında enfeksiyon veya sepsis gelişme oranı yaklaşık yüzde kaçtır?",
                options=[
                    {"key": "A", "text": "%1-2", "isCorrect": True, "explanation": "Doğru. Ders notu: 'Abortus sonrası %1-2 oranında enfeksiyon/sepsis gelişir' bilgisini verir."},
                    {"key": "B", "text": "%15-20", "isCorrect": False, "explanation": "Bu oran tüm gebeliklerdeki genel spontan abortus sıklığıdır."},
                    {"key": "C", "text": "%50", "isCorrect": False, "explanation": "İlk trimester kayıplarındaki kromozom anomalisi oranıdır."},
                    {"key": "D", "text": "%80", "isCorrect": False, "explanation": "Düşüklerin ilk trimesterde görülme oranıdır."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Amfi ders notunda bildirildiğine göre abortus sonrasında yüzde bir ila iki oranında enfeksiyon ve sepsis tablosu gelişir.",
                masked_term="yüzde bir ila iki",
                hint="Ders notunda abortus sonrası sepsis gelişimi için verilen resmi sayısal frekans aralığı (%1-2)"
            ),
            make_slider(
                left_title="Komplike Olmayan Abortus (%98-99)",
                right_title="Septik Abortus (%1-2)",
                left_points=[
                    "Ateş veya sistemik toksisite bulgusu yoktur",
                    "Vajinal akıntı kokusuz ve minimaldir",
                    "Standart medikal veya cerrahi yönetim yeterlidir"
                ],
                right_points=[
                    "Yüksek ateş, taşikardi ve kötü kokulu pürülan akıntı",
                    "Pelvik peritonit ve septik şok riski mevcuttur",
                    "Acil intravenöz antibiyoterapi ve cerrahi tahliye şarttır"
                ]
            ),
            make_recall(
                question="Abortus sonrasında enfeksiyon/sepsis gelişme sıklığı ders notunda ne olarak ifade edilmiştir?",
                answer="Abortus sonrası %1-2 oranında enfeksiyon/sepsis geliştiği belirtilmiştir."
            )
        ]
    ))

    # Slide 62
    slides.append(make_slide(
        slide_num=62,
        title="Septik Düşükte Maternal Mortalite Oranı",
        subtitle="100.000 medikal düşükte 0.58 maternal ölüm oranı",
        clinical_focus="Erken gebelik kayıplarında nadir fakat ölümcül maternal komplikasyon",
        narrative=(
            "Medikal düşük protokolleri günümüzde son derece güvenli kabul edilmekle birlikte, ölümcül enfeksiyon riski tamamen sıfır değildir.\n\n"
            "- **Resmi Ders Notu Mortalite Verisi:** Amfi ders notunda altı çizilen epidemiyolojik istatistik: **'100.000 medikal düşükte 0,58 maternal ölüm'** görüldüğüdür.\n"
            "- **Mortalite Nedenleri:** Bu ölümlerin en büyük bölümü, atipik anaerop bakterilerin (örneğin *Clostridium sordellii* veya *Clostridium perfringens*) yol açtığı toksik şok sendromu, endotoksemik septik şok, akut böbrek hasarı ve yaygın tüketim koagülopatisine bağlıdır.\n"
            "- **Klinik Güvenlik:** Bu oran medikal düşüğün (ör. misoprostol/mifepriston) cerrahi küretaj ve hatta canlı doğumdaki maternal mortaliteden çok daha güvenli olduğunu kanıtlar. Ancak ateş ve pelvik ağrı gelişen her olguda hızlı hekim başvurusu hayatidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Amfi ders notuna göre 100.000 medikal düşükte 0,58 maternal ölüm görülür."
        ),
        bullets=[
            "100.000 medikal düşük uygulamasında 0,58 maternal ölüm bildirilmiştir",
            "Ölümlerin başlıca sebebi hızlı ilerleyen anaerop endotoksemik sepsistir",
            "Medikal düşük cerrahi ve terme göre çok güvenli bir prosedürdür",
            "Ateşsiz toksik şok olgularında taşikardi ve lökositoz erken uyarıcıdır"
        ],
        elements=[
            make_quiz(
                question="Ders notunda belirtilen resmi epidemiyolojik istatistiğe göre, medikal düşük uygulamalarında saptanan maternal ölüm oranı hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "100 gebelikte 5 maternal ölüm", "isCorrect": False, "explanation": "Aşırı abartılı ve gerçek dışı bir orandır."},
                    {"key": "B", "text": "1.000 düşükte 10 ölüm", "isCorrect": False, "explanation": "Çok yüksek bir orandır."},
                    {"key": "C", "text": "100.000 medikal düşükte 0,58 maternal ölüm", "isCorrect": True, "explanation": "Doğru. Notta: '100.000 medikal düşükte 0,58 maternal ölüm görülür' şeklinde tam istatistik verilmiştir."},
                    {"key": "D", "text": "Herhangi bir maternal ölüm bildirilmemiştir (sıfır)", "isCorrect": False, "explanation": "Nadir de olsa 0.58 oranı mevcuttur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notundaki verilere göre yüz bin medikal düşükte sıfır virgül elli sekiz oranında maternal ölüm görülür.",
                masked_term="sıfır virgül elli sekiz",
                hint="Ders notunda 100.000 medikal düşük başına düşen resmi maternal ölüm sayısı"
            ),
            make_table(
                title="Ders Notu Septik Düşük Epidemiyoloji Özeti",
                headers=["Klinik Gösterge", "Resmi İstatistiksel Oran", "Klinik Yansıması"],
                rows=[
                    [
                        {"text": "Abortus Sonrası Sepsis Oranı", "isMasked": False},
                        {"text": "%1-2 enfeksiyon/sepsis", "isMasked": True, "hint": "Düşük sonrası mikrobiyal pelvik komplikasyon sıklığı"},
                        {"text": "Post-abortif enfeksiyon gelişim riski", "isMasked": False}
                    ],
                    [
                        {"text": "Medikal Düşük Maternal Mortalitesi", "isMasked": False},
                        {"text": "100.000'de 0,58 ölüm", "isMasked": True, "hint": "Yüz binde sıfır virgül elli sekiz maternal kayıp"},
                        {"text": "Nadir fakat ölümcül toksik komplikasyon", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Medikal düşüklerde 100.000'de 0.58 gibi son derece düşük bir mortaliteye rağmen ölümlerin en sık görülen enfeksiyöz patofizyolojisi nedir?",
                answer="Uterustan kana karışan bakteriyel endotoksin ve ekzotoksinlerin (özellikle anaerop Clostridium türleri veya Gram-negatif basiller) tetiklediği septik/toksik şok ve yaygın damar içi pıhtılaşmasıdır (DIC)."
            )
        ]
    ))

    # Slide 63
    slides.append(make_slide(
        slide_num=63,
        title="Septik Abortus Mikrobiyolojisi ve Patogenezi",
        subtitle="Polimikrobiyal asendan enfeksiyon: Aerop, anaerop ve Clostridium türleri",
        clinical_focus="Vajinal floranın nekrotik desiduaya invazyonu ve bakteriyemi",
        narrative=(
            "Septik abortus tablosu nadiren tek bir mikroorganizmaya bağlıdır; olguların ezici çoğunluğu **polimikrobiyal asendan enfeksiyon** karakterindedir.\n\n"
            "- **Etken Patojenler:** Normal vajinal ve servikal florada bulunan patojenlerin yukarı servikal kanaldan nekrotik plasental artıklarla dolu uterusa tırmanmasıyla başlar. En sık izole edilenler:\n"
            "  * **Gram-Negatif Enterik Basiller:** *Escherichia coli*, *Klebsiella pneumoniae*, *Proteus mirabilis*.\n"
            "  * **Gram-Pozitif Koklar:** Grup B Streptokoklar (*S. agalactiae*), *Enterococcus faecalis*.\n"
            "  * **Anaeroplar:** *Bacteroides fragilis*, *Peptostreptococcus* ve sporlu anaerop *Clostridium perfringens*.\n"
            "- **Toksik Tablo (Gazlı Gangren):** Özellikle *Clostridium perfringens* enfeksiyonunda salınan alfa-toksin (lesitinaz) masif intravasküler hemolize, sarılığa, akut tübüler nekroza ve miyometriumda gaz kabarcıklarına yol açarak saatler içinde ölümcül seyreder.\n\n"
            "> [!NOTE]\n"
            "> Septik abortus polimikrobiyal bir enfeksiyondur; enterik Gram-negatif basiller, streptokoklar ve anaerop bakteriler birlikte rol oynar."
        ),
        bullets=[
            "Enfeksiyon tipi polimikrobiyaldir (aerop ve anaerop karışımı)",
            "Enterik basiller (E. coli) ve Grup B streptokoklar sıklıkla izole edilir",
            "Bacteroides ve Peptostreptococcus gibi anaeroplar kokuşmuş püy yapar",
            "Clostridium enfeksiyonu intravasküler hemoliz ve gazlı miyometrit yapabilir"
        ],
        elements=[
            make_quiz(
                question="Septik abortus patogenezinde rol oynayan mikroorganizmaların genel mikrobiyolojik karakteri hakkında hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Yalnızca tek bir virüse (HSV) bağlı saf viral enfeksiyondur", "isCorrect": False, "explanation": "Septik abortus bakteriyel bir enfeksiyondur."},
                    {"key": "B", "text": "Çoğunlukla aerop Gram-negatif basiller, streptokoklar ve anaeropların bir arada bulunduğu polimikrobiyal enfeksiyondur", "isCorrect": True, "explanation": "Doğru. Septik düşük klasik olarak polimikrobiyal asendan bir tablodur."},
                    {"key": "C", "text": "Sadece steril havadan bulaşan mantar sporları rol oynar", "isCorrect": False, "explanation": "Asendan vajinal/enterik bakteriler rol oynar."},
                    {"key": "D", "text": "Mycobacterium tuberculosis tek kanıtlanmış etkendir", "isCorrect": False, "explanation": "Tüberküloz akut septik abortus etkeni değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Septik abortus vakalarında enfeksiyon odağında aerop ve anaerop bakterilerin birlikte ürediği polimikrobiyal tablo hakimdir.",
                masked_term="polimikrobiyal",
                hint="Birden çok bakteri türünün bir arada enfeksiyon oluşturması durumu"
            ),
            make_swipe(
                title="Septik Abortus Mikrobiyolojik Spektrumu",
                left_category="Gram-Negatif / Anaerop Floralar",
                right_category="Gram-Pozitif Koklar ve Sporlular",
                cards=[
                    {"text": "Escherichia coli ve Klebsiella", "category": "left", "explanation": "Enterik endotoksin kaynağı basillerdir."},
                    {"text": "Grup B Streptokok (S. agalactiae)", "category": "right", "explanation": "Genital traktusta yaygın kolonize koktur."},
                    {"text": "Bacteroides fragilis", "category": "left", "explanation": "Kötü kokulu pürülan püy oluşturan anaeroptur."},
                    {"text": "Clostridium perfringens", "category": "right", "explanation": "İntravasküler hemoliz ve gaz üreten sporlu anaeroptur."}
                ]
            ),
            make_recall(
                question="Septik abortus hastasında ultrasonda miyometrium içinde gaz ekojeniteleri ve idrarda koyu bordo/kahverengi renk (hemoglobinüri) saptanması hangi spesifik mikroorganizmayı düşündürür?",
                answer="Clostridium perfringens enfeksiyonunu düşündürür; bakterinin ürettiği alfa-toksin masif intravasküler hemoliz ve gazlı miyometrit (nekrotizan enfeksiyon) yapar."
            )
        ]
    ))

    # Slide 64
    slides.append(make_slide(
        slide_num=64,
        title="Septik Düşük Klinik Belirtileri ve Tanı Kriterleri",
        subtitle="Yüksek ateş, kokuşmuş vajinal püy, pelvik hassasiyet ve peritoneal irritasyon",
        clinical_focus="Erken sepsisin tanınması ve pelvik peritonit ayrımı",
        narrative=(
            "Septik abortus kliniği lokal bir endometritten fulminan septik şoka kadar geniş bir yelpazede seyreder.\n\n"
            "- **Klasik Semptomlar:** Yakın zamanda spontan düşük veya küretaj öyküsü olan kadında **yüksek ateş (>38°C / titreme)**, taşikardi, şiddetli alt karın/kasık ağrısı ve vajinadan gelen **kötü kokulu, pürülan (cerahatli) akıntı** mevcuttur.\n"
            "- **Fizik Muayene Bulguları:** Abdominal palpasyonda suprapubik hassasiyet, defans ve enfeksiyon pelvise yayılmışsa **rebound hassasiyeti (peritonit bulgusu)** saptanır. Pelvik bimanuel muayenede uterus aşırı derecede hassastır (dokunmakla şiddetli ağrı) ve servikal os genellikle açıktır.\n"
            "- **Laboratuvar Bulguları:** Kanda belirgin **lökositoz (>15.000/mm³)**, sola kayma (bant formları), CRP ve prokalsitonin yüksekliği izlenir. Şok gelişen olgularda hipotansiyon, oligüri ve laktat yüksekliği tabloya eklenir.\n\n"
            "> [!IMPORTANT]\n"
            "> Düşük sonrası yüksek ateş, kötü kokulu pürülan akıntı, uterin hassasiyet ve lökositoz septik abortusun kardinal belirtileridir."
        ),
        bullets=[
            "Yüksek ateş (>38°C), titreme ve taşikardi sistemik enfeksiyon göstergesidir",
            "Vajinadan gelen akıntı tipik olarak pürülan ve kötü kokuludur",
            "Bimanuel muayenede uterus ileri derecede ağrılı ve hassastır",
            "Rebound ve defans enfeksiyonun pelvik peritona taştığını belgeler"
        ],
        elements=[
            make_quiz(
                question="Düşük yaptıktan 3 gün sonra acil servise başvuran bir kadında yüksek ateş (38.9°C), taşikardi, kötü kokulu pürülan vajinal akıntı ve palpasyonda aşırı uterin hassasiyet saptanıyor. Bu hastada öncelikle düşünülmesi gereken tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Komplet abortus", "isCorrect": False, "explanation": "Komplet abortusta ateş, püy ve enfeksiyon yoktur; kavite boştur."},
                    {"key": "B", "text": "Basit fizyolojik loşi akıntısı", "isCorrect": False, "explanation": "Fizyolojik loşi yüksek ateş ve pürülan koku yapmaz."},
                    {"key": "C", "text": "Septik abortus (septik düşük)", "isCorrect": True, "explanation": "Doğru. Düşük sonrası ateş, pürülans, kötü koku ve uterin hassasiyet septik abortusun klasik tablosudur."},
                    {"key": "D", "text": "Gestasyonel trofoblastik neoplazi", "isCorrect": False, "explanation": "Akut bakteriyel sepsis tablosu ile başlamaz."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Septik abortus olgularında spekulum muayenesinde eksternal servikal ostan gelen kötü kokulu pürülan akıntı en belirgin lokal enfeksiyon bulgusudur.",
                masked_term="pürülan akıntı",
                hint="Bakteriyel enfeksiyona bağlı cerahatli ve iltihaplı vajinal drenaj"
            ),
            make_table(
                title="Komplike Olmayan Düşük vs Septik Düşük Bulguları",
                headers=["Klinik Parametre", "Komplike Olmayan Düşük", "Septik Düşük"],
                rows=[
                    [
                        {"text": "Vücut Sıcaklığı", "isMasked": False},
                        {"text": "Normal (<37.5°C)", "isMasked": False},
                        {"text": "Yüksek ateş (>38°C, titreme)", "isMasked": True, "hint": "Sistemik hipertermi yanıtı"}
                    ],
                    [
                        {"text": "Vajinal Akıntı Niteliği", "isMasked": False},
                        {"text": "Kokusuz kan / seröz sıvı", "isMasked": False},
                        {"text": "Kötü kokulu pürülan püy", "isMasked": True, "hint": "Cerahatli iltihaplı akıntı"}
                    ],
                    [
                        {"text": "Uterus Muayenesi", "isMasked": False},
                        {"text": "Hafif kramp, kütle hassas değil", "isMasked": False},
                        {"text": "Aşırı duyarlı ve ağrılı uterus", "isMasked": True, "hint": "Şiddetli pelvik hassasiyet"}
                    ]
                ]
            ),
            make_recall(
                question="Septik düşük şüphesi olan bir hastada pelvik muayenede serviksin hareket ettirilmesiyle (servikal hareket hassasiyeti) aşırı ağrı uyanması neyi düşündürür?",
                answer="Enfeksiyonun endometrium sınırını aşarak miyometriuma, parametriyuma ve pelvik peritona (pelvik peritonit) yayıldığını düşündürür."
            )
        ]
    ))

    # Slide 65
    slides.append(make_slide(
        slide_num=65,
        title="Septik Abortus Acil Medikal Yönetimi: İntravenöz Antibiyoterapi",
        subtitle="Geniş spektrumlu IV antimikrobiyal kombinasyonları",
        clinical_focus="Kültür sonuçları beklenmeden başlanan agresif parenteral bakterisidal rejim",
        narrative=(
            "Septik abortus acil serviste bir tıp öğrencisinin ve hekimin saniyeler içinde tanı koyup tedavi başlatması gereken bir durumdur.\n\n"
            "- **Resmi Ders Notu Kuralı:** Amfi ders notunda septik düşük için ilk basamak tedavi: **'Acil intravenöz antimikrobiyal tedavi'** şeklinde net olarak emredilmiştir.\n"
            "- **Tedavi Protokolü:** Kan, idrar ve servikal püy kültürleri alındıktan hemen sonra kültür sonuçları beklenmeden **geniş spektrumlu üçlü intravenöz antibiyoterapi** başlanır. Standart rejimler:\n"
            "  * Ampisilin (veya seftriakson) + Gentamisin (Gram-negatif enterikler için) + Metronidazol (veya klindamisin - anaeroplar için).\n"
            "  * Alternatif olarak geniş spektrumlu beta-laktam/beta-laktamaz inhibitörleri (ampisilin-sulbaktam, piperasilin-tazobaktam) veya karbapenemler.\n"
            "- **Sıvı Resüsitasyonu:** Vasküler dilatasyon ve kapiller kaçış nedeniyle hastalara kristaloid sıvı replasmanı yapılarak organ perfüzyonu korunur.\n\n"
            "> [!IMPORTANT]\n"
            "> Septik abortus yönetiminde ilk ve en acil basamak kültürler alınır alınmaz derhal geniş spektrumlu intravenöz antimikrobiyal tedaviye başlanmasıdır."
        ),
        bullets=[
            "Ders notuna göre ilk adım acil intravenöz antimikrobiyal tedavidir",
            "Kültür sonuçları beklenmeden üçlü kombine parenteral rejim başlanır",
            "Rejim Gram-pozitif, Gram-negatif ve anaerop bakterileri kapsamalıdır",
            "Yeterli kristaloid sıvı resüsitasyonu ile septik şok önlenmelidir"
        ],
        elements=[
            make_quiz(
                question="Ders notunda septik abortus tablosu ile başvuran bir hastada ilk olarak uygulanması gereken tedavi hangisinde doğru belirtilmiştir?",
                options=[
                    {"key": "A", "text": "Oral demir ve folik asit takviyesi", "isCorrect": False, "explanation": "Sepsis acil parenteral tedavi gerektirir."},
                    {"key": "B", "text": "Hemen eve gönderilip poliklinik randevusu verilmesi", "isCorrect": False, "explanation": "Hayatı tehdit eden tablodur, yatış şarttır."},
                    {"key": "C", "text": "Acil intravenöz antimikrobiyal tedavi", "isCorrect": True, "explanation": "Doğru. Ders notu: 'Acil intravenöz antimikrobiyal tedavi, sonrasında rest varsa uterusun cerrahi boşaltılması' kuralını koyar."},
                    {"key": "D", "text": "Yalnızca subkutan düşük doz heparin yapılması", "isCorrect": False, "explanation": "Primer enfeksiyonu tedavi etmez."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notuna göre septik düşük olgularında ilk ve en acil yaklaşım acil intravenöz antimikrobiyal tedavi uygulanmasıdır.",
                masked_term="antimikrobiyal tedavi",
                hint="Ders notunda acil intravenöz olarak verilmesi gerektiği belirtilen antibiyotik rejimi"
            ),
            make_chain(
                title="Septik Abortus Acil Resüsitasyon Protokolü",
                steps=[
                    "Acil İntravenöz Erişim: İki adet geniş lümenli damar yolu açılarak izotonik kristaloid sıvı infüzyonunun başlatılması",
                    "Kültür Örneklemesi: Kan kültürleri, idrar ve servikal akıntıdan aerob/anaerob mikrobiyolojik sürüntü alınması",
                    "Geniş Spektrumlu IV Antibiyoterapi: Kültür sonucu beklenmeden aerop ve anaeropları kapsayan bakterisidal IV antibiyotik başlanması",
                    "Hemodinamik Stabilizasyon: İdrar çıkışı ve arteryel tansiyonun monitörize edilerek organ perfüzyonunun sağlanması"
                ]
            ),
            make_recall(
                question="Neden septik abortusta antibiyoterapi oral değil de mutlaka 'acil intravenöz' olarak uygulanmalıdır?",
                answer="Çünkü enfeksiyon hızla bakteriyemiye ve septik şoka ilerleme riski taşır; terapötik kanda bakterisidal ilaç konsantrasyonuna en hızlı ve güvenilir şekilde ancak parenteral intravenöz yolla ulaşılabilir."
            )
        ]
    ))

    # Slide 66
    slides.append(make_slide(
        slide_num=66,
        title="Septik Düşükte Cerrahi Yönetim: Uterusun Boşaltılması",
        subtitle="Rest (artık doku) varlığında IV antibiyotik sonrası cerrahi tahliye",
        clinical_focus="Enfeksiyon odağının mekanik eradikasyonu ve bakteriyemi baskılanması",
        narrative=(
            "Septik abortusta yalnızca antibiyotik vermek yeterli değildir; çünkü enfeksiyonun kaynağı uterus içindeki nekrotik artık dokulardır.\n\n"
            "- **Resmi Ders Notu Kuralı:** Amfi ders notunda cerrahi zamanlama prensibi açıkça belirtilmiştir: **'Acil intravenöz antimikrobiyal tedavi, sonrasında rest varsa uterusun cerrahi boşaltılması gerekir.'**\n"
            "- **Zamanlama İlkesi:** Önce IV antibiyotik başlanır ve kanda terapötik düzeye ulaşması için ideal olarak birkaç saat (genellikle 2-4 saat) beklenir. Uterus içinde **rest (retansiyone nekrotik konseptüs artıkları)** olduğu ultrasonda gösterildiğinde kavite cerrahi olarak tahliye edilir.\n"
            "- **Cerrahi Teknik:** Vakum aspirasyon en uygun yöntemdir. Ancak enfekte miyometrium son derece yumuşak ve frajildir; bu nedenle **uterin perforasyon riski çok yüksektir**. İşlem son derece nazik yapılmalı, keskin küretlerden olabildiğince kaçınılmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Septik abortusta kural: Önce acil IV antibiyotik başlanır, ardından kavitede rest varsa uterus cerrahi olarak boşaltılır."
        ),
        bullets=[
            "Ders notu kuralı: Acil IV antibiyotik, sonrasında rest varsa cerrahi boşaltmadır",
            "Nekrotik doku odağı temizlenmedikçe sepsis tablosu gerilemez",
            "Enfekte miyometrium son derece yumuşak olduğundan perforasyon riski çok yüksektir",
            "Cerrahi tahliye için nazik vakum aspirasyon tekniği tercih edilir"
        ],
        elements=[
            make_quiz(
                question="Septik abortus hastasında cerrahi tahliye (küretaj / boşaltma) kararı ve zamanlaması ile ilgili ders notunda belirtilen en doğru prensip hangisidir?",
                options=[
                    {"key": "A", "text": "Antibiyotik vermeden hemen ameliyathaneye alınıp keskin küretaj yapılmalıdır", "isCorrect": False, "explanation": "Antibiyotik verilmeden dokunulursa masif bakteriyemi ve septik şok tetiklenir."},
                    {"key": "B", "text": "Acil IV antimikrobiyal tedavi verilip sonrasında kavitede rest varsa uterus cerrahi olarak boşaltılmalıdır", "isCorrect": True, "explanation": "Doğru. Ders notundaki net kural: Acil IV antimikrobiyal tedavi, sonrasında rest varsa uterusun cerrahi boşaltılmasıdır."},
                    {"key": "C", "text": "Kavitede doku olsa bile cerrahi işlem 6 ay ertelenmelidir", "isCorrect": False, "explanation": "Enfeksiyon odağı bekletilmez."},
                    {"key": "D", "text": "Septik abortusta cerrahi tahliye tıbben yasaktır", "isCorrect": False, "explanation": "Rest varsa tahliye hayatidir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre septik abortusta acil intravenöz antimikrobiyal tedavi verildikten sonra kavitede rest varsa uterusun cerrahi boşaltılması uygulanır.",
                masked_term="cerrahi boşaltılması",
                hint="Ders notundaki tablodan alıntı: nekrotik odağın tahliyesi işlemi"
            ),
            make_slider(
                left_title="Yanlış Yaklaşım: Antibiyotiksiz Erken Küretaj",
                right_title="Doğru Yaklaşım: IV Antibiyotik Sonrası Tahliye",
                left_points=[
                    "Kanda antibiyotik seviyesi olmadan kavitenin manipülasyonu",
                    "Açık venöz sinüslerden kana masif bakteri ve endotoksin dökülmesi",
                    "Ani fulminan septik şok ve kardiyovasküler kollaps riski"
                ],
                right_points=[
                    "Önce acil geniş spektrumlu IV antibiyotik başlanması",
                    "Kanda terapötik bakterisidal seviye oluştuktan sonra tahliye",
                    "Bakteriyemi baskılanarak enfeksiyon odağının güvenle temizlenmesi"
                ]
            ),
            make_recall(
                question="Neden septik abortus olgularında cerrahi boşaltma öncesinde birkaç saat intravenöz antibiyotik verilmesi beklenir?",
                answer="Kavite içindeki enfekte dokuların mekanik olarak manipülasyonu ve damarların açılması sırasında kana masif bakteri ve endotoksin dökülerek septik şok tablosunun tetiklenmesini önlemek için dolaşımda bakterisidal antibiyotik düzeyi sağlanmalıdır."
            )
        ]
    ))

    # Slide 67
    slides.append(make_slide(
        slide_num=67,
        title="Profilaktik Antibiyoterapi İlkesi: Tahliye Öncesi Koruma",
        subtitle="Cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanması",
        clinical_focus="Komplike olmayan düşüklerin cerrahisinde septik tabloyu önleme stratejisi",
        narrative=(
            "Septik düşük tablosunu tedavi etmek son derece güç ve yıpratıcı olduğundan, modern obstetrinin temel felsefesi septik süreci henüz başlamadan önlemektir.\n\n"
            "- **Resmi Ders Notu Profilaksi Kuralı:** Amfi ders notunda net ve bağımsız bir ilke olarak vurgulanmıştır: **'Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanır.'**\n"
            "- **Klinik Gerekçesi:** Düşük nedeniyle (missed abortus, inkomplet abortus veya terminasyon) uterin kavitesi vakumla tahliye edilecek olan her hastada; cerrahi kanüller vajinal florayı geçerek uterusa girer. İşlem öncesinde uygulanan profilaktik antibiyotik, asendan bakteri translokasyonunu ve işlem sonrası gelişebilecek endometrit/sepsis riskini **%70-80 oranında azaltır**.\n"
            "- **Kullanılan Ajanlar:** En sık tercih edilen profilaksi rejimi cerrahi işlemden 1 saat önce oral veya IV **doksisiklin** veya **azitromisin** / metronidazol uygulamasıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Ders notu kuralı: Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanır."
        ),
        bullets=[
            "Ders notuna göre cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanır",
            "Amaç işlem sırasında vajinal floranın kaviteye taşınmasını ve sepsisi önlemektir",
            "Profilaksi post-abortif endometrit riskini dramatik olarak düşürür",
            "Tek doz doksisiklin veya uygun geniş spektrumlu ajan tercih edilir"
        ],
        elements=[
            make_quiz(
                question="Amfi ders notunda cerrahi tahliye yapılacak erken gebelik kaybı vakalarında enfeksiyon ve sepsisi önlemek amacıyla belirtilen temel koruyucu klinik ilke hangisidir?",
                options=[
                    {"key": "A", "text": "Tahliye öncesinde hastaya 1 ay yatak istirahati verilmesi", "isCorrect": False, "explanation": "İstirahat enfeksiyonu önlemez."},
                    {"key": "B", "text": "Tüm cerrahi kanüllerin steril edilmeden kullanılması", "isCorrect": False, "explanation": "Tıbbi hata ve enfeksiyon kaynağıdır."},
                    {"key": "C", "text": "İşlemden sonra hastanın yıkanmasının yasaklanması", "isCorrect": False, "explanation": "Bilimsel profilaksi ilkesi değildir."},
                    {"key": "D", "text": "Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanması", "isCorrect": True, "explanation": "Doğru. Ders notundaki resmi cümle: 'Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanır' kuralıdır."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Ders notunda belirtildiği üzere önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanması temel obstetrik kuraldır.",
                masked_term="profilaktik antibiyoterapi",
                hint="Ders notunda cerrahi tahliye öncesi enfeksiyonu önlemek için verilmesi şart koşulan koruyucu tedavi"
            ),
            make_spot_the_lie(
                topic="Septik abortus ve profilaksi ilkeleri",
                items=[
                    {"text": "Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanmalıdır.", "isLie": False, "explanation": "Doğrudur; ders notundaki açık ve net kuraldır."},
                    {"text": "Septik abortusta kavitede nekrotik artık doku bulunsa bile kesinlikle hiçbir zaman cerrahi tahliye yapılamaz.", "isLie": True, "explanation": "Tuzak önerme. IV antibiyotik verildikten sonra rest varsa kavite cerrahi olarak tahliye edilmek zorundadır."},
                    {"text": "Abortus sonrası enfeksiyon ve sepsis gelişme oranı yaklaşık %1-2'dir.", "isLie": False, "explanation": "Doğrudur; nottaki resmi insidans oranıdır."}
                ]
            ),
            make_recall(
                question="Neden rutin cerrahi küretaj veya vakum aspirasyon öncesinde profilaktik antibiyoterapi uygulanması obstetrik bir standarttır?",
                answer="Vajinal kanaldan kaviteye cerrahi alet geçişi sırasında floradaki patojenlerin steril desiduaya inokülasyonunu engellemek ve işlem sonrası %1-2 oranında görülebilen hayatı tehdit edici septik abortus riskini önlemek içindir."
            )
        ]
    ))

    # Slide 68
    slides.append(make_slide(
        slide_num=68,
        title="Ağır Septik Komplikasyonlar: Pelvik Apse ve Histerektomi",
        subtitle="Miyometrial mikroabseler, septik pelvik tromboflebit ve acil cerrahi",
        clinical_focus="Maksimal antibiyoterapye yanıtsız refrakter sepsiste hayat kurtarıcı organ rezeksiyonu",
        narrative=(
            "Septik abortus olgularında intravenöz üçlü antibiyoterapiye ve kavitary cerrahi boşaltmaya rağmen klinik tablonun gerilemediği refrakter durumlar gelişebilir.\n\n"
            "- **Miyometrial Apseler ve Nekrotizan Miyometrit:** Bakteriyel toksinler miyometrium derin kas liflerine penetre olarak yaygın nekroz ve mikroabseler oluşturur. Uterus dokusu gangrene döner (**nekrotizan panmetrit**).\n"
            "- **Septik Pelvik Tromboflebit:** Enfeksiyon pelvik venöz pleksusa ve ovaryan venlere yayılarak enfekte trombüsler oluşturur. Antibiyotiğe rağmen düşmeyen dirençli 'çivi gibi batan' ateş pikleri ile karakterizedir.\n"
            "- **Acil Histerektomi Endikasyonları:** IV antibiyoterapi ve tahliyeye rağmen 48-72 saatte klinik düzelme olmaması, uterin perforasyon şüphesi, pelvik apse varlığı, miyometriumda gaz oluşumu (*Clostridium*) veya kontrol edilemeyen septik şok/DIC varlığında **tek hayat kurtarıcı seçenek acil histerektomidir (uterusun cerrahi olarak çıkarılması)**.\n\n"
            "> [!NOTE]\n"
            "> Antibiyotik ve küretaja yanıt vermeyen miyometrial apse, perforasyon ve Clostridium nekrozunda hayat kurtarıcı müdahale acil histerektomidir."
        ),
        bullets=[
            "Refrakter vakalarda miyometrial nekroz ve pelvik apse gelişebilir",
            "Septik pelvik tromboflebit inatçı yüksek ateş pikleri ile seyreder",
            "48-72 saatte düzelmeyen ağır sepsis histerektomi endikasyonudur",
            "Uterin perforasyon veya gazlı gangren varlığında gecikmeksizin uterus alınır"
        ],
        elements=[
            make_quiz(
                question="Septik abortus nedeniyle geniş spektrumlu IV antibiyotik başlanan ve kavitary vakum tahliyesi yapılan bir hastada 48 saat sonra yüksek ateş devam ediyor, ultrasonda miyometriumda gaz kabarcıkları ve yaygın apse saptanıyor. Bu hastada maternal hayatı kurtarmak için en uygun yaklaşım hangisidir?",
                options=[
                    {"key": "A", "text": "Tüm antibiyotikleri kesip hastayı taburcu etmek", "isCorrect": False, "explanation": "Ölüme yol açar."},
                    {"key": "B", "text": "Yalnızca oral vitamin desteği vermek", "isCorrect": False, "explanation": "Etkisizdir."},
                    {"key": "C", "text": "Acil cerrahi eksplorasyon ve histerektomi (uterusun çıkarılması)", "isCorrect": True, "explanation": "Doğru. Nekrotizan miyometrit ve gazlı enfeksiyonda enfeksiyon odağını yok etmek için histerektomi hayat kurtarıcıdır."},
                    {"key": "D", "text": "Bir sonraki menstrüasyona kadar hiçbir şey yapmadan beklemek", "isCorrect": False, "explanation": "Septik şoktan maternal ölüme neden olur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Septik abortusta nekrotizan enfeksiyon ve miyometrial gaz varlığında maternal hayatı kurtarmak için acil cerrahi yöntem olan histerektomi uygulanır.",
                masked_term="histerektomi",
                hint="Uterusun ameliyatla tamamen çıkarılması operasyonu"
            ),
            make_slider(
                left_title="Erken Evre Septik Abortus",
                right_title="İleri Nekrotizan Evre",
                left_points=[
                    "Enfeksiyon endometrium ve kavite artıklarıyla sınırlıdır",
                    "Geniş spektrumlu IV antibiyotik ve vakum aspirasyona hızla yanıt verir",
                    "Uterus korunabilir, fertilite etkilenmez"
                ],
                right_points=[
                    "Enfeksiyon miyometriuma, parametriyuma ve venöz pleksusa yayılmıştır",
                    "Miyometrial abseler, Clostridium gangreni ve refrakter şok izlenir",
                    "Hayat kurtarmak amacıyla acil histerektomi gerekir"
                ]
            ),
            make_recall(
                question="Septik abortus tablosunda acil histerektomi kararını gerektiren en kritik obstetrik ve cerrahi durumlar nelerdir?",
                answer="Geniş spektrumlu IV antibiyotik ve tahliyeye rağmen devam eden refrakter sepsis/septik şok, uterin perforasyon şüphesi, miyometrial derin abseler ve Clostridium'a bağlı gazlı nekrotizan gangren varlığıdır."
            )
        ]
    ))

    # Slide 69
    slides.append(make_slide(
        slide_num=69,
        title="Güvensiz Düşükler ve Global Obstetrik Perspektif",
        subtitle="Merdiven altı invaziv müdahaleler, kimyasal travma ve halk sağlığı",
        clinical_focus="Steril olmayan koşullarda uygulanan indüklenmiş abortusların trajik sonuçları",
        narrative=(
            "Gelişmiş ülkelerde medikal ve cerrahi abortus komplikasyonları son derece nadirken, küresel ölçekte güvensiz düşükler majör bir maternal ölüm nedenidir.\n\n"
            "- **Güvensiz (Kriminal) Düşük Tanımı:** Yeterli tıbbi beceriye sahip olmayan kişilerce veya asgari tıbbi standartlardan yoksun hijyenik olmayan ortamlarda gebeliğin sonlandırılmasıdır.\n"
            "- **Kullanılan İlkel Yöntemler:** Uterus içine yabancı cisim sokulması (örgü şişleri, kateterler, tahta çubuklar), toksik kimyasalların (sabunlu su, kostik solüsyonlar) vajinal duşla verilmesi veya künt abdominal travma uygulanmasıdır.\n"
            "- **Patolojik Sonuçlar:** Uterin perforasyon, bağırsak ve mesane yaralanmaları, kimyasal peritonit ve son derece ağır polimikrobiyal septik şok tablosu ile sonuçlanır. Dünya Sağlık Örgütü verilerine göre dünya genelinde maternal ölümlerin yaklaşık %8-13'ü güvensiz düşük komplikasyonlarından kaynaklanır.\n\n"
            "> [!NOTE]\n"
            "> Steril olmayan güvensiz abortus girişimleri uterin perforasyon, bağırsak yaralanması ve ölümcül septik şokun en yaygın küresel nedenidir."
        ),
        bullets=[
            "Güvensiz düşükler ehil olmayan kişilerce steril olmayan koşullarda yapılır",
            "Mekanik yabancı cisimler uterin perforasyon ve bağırsak rüptürü yapar",
            "Kimyasal kostik ajanlar kimyasal nekroz ve peritonit oluşturur",
            "Dünyadaki maternal mortalitenin önemli bir fraksiyonundan sorumludur"
        ],
        elements=[
            make_quiz(
                question="İstenmeyen gebeliği sonlandırmak amacıyla vajinasına yabancı cisim uygulandığı öğrenilen bir kadında akut karın, vajinal kanama, serbest peritoneal hava ve septik şok tablosu gelişiyor. Bu hastada meydana gelen en olası cerrahi komplikasyon hangisidir?",
                options=[
                    {"key": "A", "text": "İzole kutanöz kontakt dermatit", "isCorrect": False, "explanation": "İç organ hasarı ve serbest hava açıklar."},
                    {"key": "B", "text": "Uterus perforasyonu ve bağırsak yaralanmasına bağlı septik peritonit", "isCorrect": True, "explanation": "Doğru. Güvensiz mekanik girişimler uterus perforasyonu, bağırsak yaralanması ve sepsisle sonuçlanır."},
                    {"key": "C", "text": "Fizyolojik korpus luteum rüptürü", "isCorrect": False, "explanation": "İatrojenik septik tabloyu açıklamaz."},
                    {"key": "D", "text": "Benign servikal polip kanaması", "isCorrect": False, "explanation": "Polip akut karın ve serbest hava yapmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Güvensiz ortamlarda uygulanan mekanik düşük girişimleri sıklıkla uterus perforasyonu ve pelvik peritonit ile sonuçlanır.",
                masked_term="uterus perforasyonu",
                hint="Rahim duvarının mekanik aletlerle delinmesi ve delik açılması"
            ),
            make_slider(
                left_title="Steril Tıbbi Tahliye",
                right_title="Güvensiz (Kriminal) Girişim",
                left_points=[
                    "Vakum aspirasyon ile steril cerrahi ortamda yapılır",
                    "Profilaktik antibiyoterapi uygulanır",
                    "Mortalite 100.000'de 0.58 gibi son derece düşüktür"
                ],
                right_points=[
                    "Yabancı cisim ve toksik maddeler kullanılır",
                    "Organ perforasyonu ve fekal kontaminasyon sıktır",
                    "Yüksek maternal mortalite ve histerektomi riski taşır"
                ]
            ),
            make_recall(
                question="Güvensiz düşük şüphesiyle başvuran ve ayakta direkt batın grafisinde (ADBG) diyafragma altında serbest hava saptanan bir hastada acil tanı nedir?",
                answer="Uterus perforasyonuna eşlik eden gastrointestinal traktus (bağırsak) perforasyonu ve akut septik peritonittir; derhal acil cerrahi laparotomi gerektirir."
            )
        ]
    ))

    # Slide 70 (Checkpoint 7)
    slides.append(make_slide(
        slide_num=70,
        title="[TEKRAR SAYFASI - CHECKPOINT 7] Septik Düşük ve İleri Komplikasyonlar",
        subtitle="İnsidans (%1-2), mortalite (0.58/100.000), acil IV antibiyotik ve cerrahi kuralı",
        clinical_focus="Septik abortusun epidemiyolojik ve klinik yönetim prensiplerinin eksiksiz sentezi",
        narrative=(
            "Bu tekrar sayfası, 61-69. adımlarda işlenen Septik Düşük ve Komplikasyonları bölümünü eksiksiz özetler.\n\n"
            "- **Resmi İnsidans:** Abortus sonrası **%1-2 oranında enfeksiyon/sepsis** gelişir.\n"
            "- **Resmi Mortalite:** **100.000 medikal düşükte 0,58 maternal ölüm** görülür.\n"
            "- **Klinik Tablo:** Yüksek ateş (>38°C), kötü kokulu pürülan akıntı, pelvik/uterin hassasiyet ve lökositoz mevcuttur. Polimikrobiyaldir (E. coli, Grup B streptokok, anaeroplar).\n"
            "- **Resmi Tedavi Kuralı:** **Acil intravenöz antimikrobiyal tedavi, sonrasında rest varsa uterusun cerrahi boşaltılması** gerekir.\n"
            "- **Resmi Profilaksi Kuralı:** **Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanır**.\n\n"
            "> [!IMPORTANT]\n"
            "> İnsidans: %1-2 | Mortalite: 0.58/100.000 | Tedavi: Acil IV antibiyotik + rest varsa cerrahi tahliye | Profilaksi: Tahliye öncesi şart."
        ),
        bullets=[
            "Abortus sonrası %1-2 oranında enfeksiyon/sepsis gelişimi görülür",
            "100.000 medikal düşükte 0,58 maternal ölüm bildirilmiştir",
            "Acil intravenöz antimikrobiyal tedavi verilir; rest varsa cerrahi tahliye yapılır",
            "Cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanması standarttır"
        ],
        elements=[
            make_quiz(
                question="Ders notunda yer alan septik düşük bilgileriyle ilgili aşağıdaki ifadelerden hangisi KESİNLİKLE DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Abortus sonrası enfeksiyon gelişme oranı %80'dir ve hiçbir medikal ölüm görülmez.", "isCorrect": False, "explanation": "İnsidans %1-2'dir."},
                    {"key": "B", "text": "Septik abortusta acil IV antibiyotik başlanır, ardından rest varsa cerrahi boşaltma yapılır; 100.000 medikal düşükte 0.58 ölüm görülür.", "isCorrect": True, "explanation": "Doğru. Ders notunun tüm resmi istatistik ve tedavi kurallarını eksiksiz içeren doğru ifadedir."},
                    {"key": "C", "text": "Cerrahi tahliye öncesinde profilaktik antibiyotik verilmesi kesinlikle yasaktır.", "isCorrect": False, "explanation": "Tam tersine önlem amaçlı profilaksi şarttır."},
                    {"key": "D", "text": "Septik abortus yalnızca virüslerle oluşur, bakteriler rol oynamaz.", "isCorrect": False, "explanation": "Polimikrobiyal bakteriyel enfeksiyondur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notuna göre abortus sonrası yüzde bir ila iki enfeksiyon ve yüz bin medikal düşükte sıfır virgül elli sekiz ölüm görülür.",
                masked_term="sıfır virgül elli sekiz",
                hint="Ders notundaki resmi maternal mortalite sayısı (rakamla 0,58)"
            ),
            make_table(
                title="Bölüm 7 Altın Sentez Tablosu (Checkpoint 7)",
                headers=["Konu Başlığı", "Ders Notu Resmi İlkesi / Değeri", "Klinik Yönetim Anlamı"],
                rows=[
                    [
                        {"text": "Enfeksiyon / Sepsis Sıklığı", "isMasked": False},
                        {"text": "%1-2 enfeksiyon/sepsis", "isMasked": True, "hint": "Düşük sonrası mikrobiyal komplikasyon oranı"},
                        {"text": "Yakın post-abortif takip gereksinimi", "isMasked": False}
                    ],
                    [
                        {"text": "Maternal Mortalite İstatistiği", "isMasked": False},
                        {"text": "100.000'de 0,58 ölüm", "isMasked": True, "hint": "Yüz binde sıfır virgül elli sekiz kayıp"},
                        {"text": "Nadir fakat ölümcül risk farkındalığı", "isMasked": False}
                    ],
                    [
                        {"text": "Temel Tedavi Sıralaması", "isMasked": False},
                        {"text": "Acil IV antibiyotik + rest varsa tahliye", "isMasked": True, "hint": "Parenteral antimikrobiyal ve odak temizliği basamakları"},
                        {"text": "Bakteriyemi kontrolü ve odak eradikasyonu", "isMasked": False}
                    ],
                    [
                        {"text": "Koruyucu Profilaksi İlkesi", "isMasked": False},
                        {"text": "Cerrahi tahliye öncesi profilaktik antibiyotik", "isMasked": True, "hint": "Mekanik işlem evvelinde koruyucu ilaç şartı"},
                        {"text": "Asendan iyatrojenik sepsisi önleme", "isMasked": False}
                    ]
                ]
            ),
            make_branching(
                scenario="Düşük sonrası 4. günde acile getirilen bir hastada yüksek ateş, kötü kokulu akıntı ve ultrasonda kavite içinde 25 mm fetoplasental rest dokusu saptanıyor. Doğru yönetim seçilecektir.",
                options=[
                    {
                        "text": "Kan kültürleri alınarak derhal acil IV geniş spektrumlu antimikrobiyal tedavi başlanır; ardından kanda antibiyotik seviyesi sağlanınca vakumla cerrahi boşaltma yapılır.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. Ders notunun tedavi protokolüne tam uygundur: önce IV antibiyotik, sonra rest tahliyesi."
                    },
                    {
                        "text": "Hiç antibiyotik verilmeden hasta acil cerrahi küretaja alınmalı, antibiyotik taburculukta oral verilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Antibiyotiksiz cerrahi manipülasyon masif septik şok tetikler."
                    },
                    {
                        "text": "Rest dokusu bulunmasına rağmen cerrahi tahliye yapılmamalı, hasta sadece evde dinlenmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Rest varlığında cerrahi boşaltma yapılmazsa enfeksiyon odağı temizlenemez ve ölüm riski doğar."
                    }
                ]
            ),
            make_recall(
                question="Bölüm 7'nin en temel iki obstetrik kuralı olan 'septik abortus tedavisi' ve 'tahliye öncesi profilaksi' ilkelerini özetleyiniz.",
                answer="Tedavide kural: Acil intravenöz antimikrobiyal tedavi, sonrasında kavitede rest varsa uterusun cerrahi boşaltılmasıdır. Profilakside kural: Önlem amaçlı cerrahi tahliye öncesinde profilaktik antibiyoterapi uygulanmasıdır."
            )
        ]
    ))

    return slides
