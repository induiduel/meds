"""
Deck 54 - Section 3: Mol Hidatiform Genetiği ve Komplet vs Parsiyel Mol (Slayt 21-30)
Slayt 30: Checkpoint 3
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec3_slides():
    slides = []
    
    # Slide 21
    slides.append(make_slide(
        slide_num=21,
        title="Mol Hidatiform: Anormal Fertilizasyon ve Genetik Temel",
        subtitle="Paternal kromozom fazlalığı ve dengesiz genom mekanizması",
        clinical_focus="Molar gebeliğin sitogenetik kökeni ve paternal etki",
        narrative=(
            "Mol hidatiform, normal bir zigot gelişiminin aksine, anormal fertilizasyon (döllenme) süreçleri sonucu ortaya çıkan patolojik bir gebelik ürünüdür. "
            "Gelişimsel biyolojide trofoblastik dokunun proliferasyonu esas olarak babadan gelen (**paternal**) genetik materyalin denetimi altındadır.\n\n"
            "- **Paternal Aşırılık Etkisi:** Molar hastalıklarda maternal genomun inaktivasyonu veya kaybına karşılık, paternal genomun çift dozda bulunması aşırı trofoblastik büyümeye ve embriyonik dokunun baskılanmasına yol açar.\n"
            "- **İki Temel Alt Tip:** Bu döllenme anomalisi fertilize olan ovumun genetik içeriğine ve dölleyen sperm sayısına bağlı olarak iki morfolojik forma ayrılır: **komplet mol** ve **parsiyel mol**.\n"
            "- **Klinik Yansıma:** Anormal paternal gen ekspresyonu koryonik villusların aşırı sıvı biriktirmesine ve trofoblastların kontrolsüzce çoğalmasına neden olur.\n\n"
            "> [!NOTE]\n"
            "> Normal bir embriyoda maternal genom fetal organogenezi yönetirken, paternal genom plasenta ve trofoblast gelişiminden sorumludur; molar gebelikler paternal aşırılıktır."
        ),
        bullets=[
            "Anormal fertilizasyon sonucu meydana gelen genetik kusurdur",
            "Trofoblast gelişimi paternal (baba) genomunun kontrolü altındadır",
            "Paternal kromozom fazlalığı aşırı trofoblastik proliferasyon yapar",
            "Komplet mol ve parsiyel mol olmak üzere iki alt tipi vardır"
        ],
        elements=[
            make_quiz(
                question="Mol hidatiform gelişiminde koryonik villusların kistik büyümesini ve aşırı trofoblastik proliferasyonu yönlendiren temel genetik mekanizma nedir?",
                options=[
                    {"key": "A", "text": "Maternal mitokondriyal DNA'da nokta mutasyonları birikmesi", "isCorrect": False, "explanation": "Mitokondriyal myopatilerle ilgilidir; trofoblastik proliferasyonu kontrol etmez."},
                    {"key": "B", "text": "Y kromozomundaki SRY geninin delesyonu", "isCorrect": False, "explanation": "SRY gonadal cinsiyet diferansiasyonunu belirler; molar patogenezde rol almaz."},
                    {"key": "C", "text": "X inaktivasyonunun tamamen durması ve maternal trizomi", "isCorrect": False, "explanation": "Molar gebelik maternal fazlalık değil paternal aşırılık tablosudur."},
                    {"key": "D", "text": "Döllenmede paternal (babadan gelen) genetik materyalin anormal baskınlığı", "isCorrect": True, "explanation": "Doğru. Trofoblast gelişimi paternal genom kontrolündedir; paternal kromozomların anormal dağılımı molar hastalığa yol açar."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Molar hastalık, gebelikte paternal kromozomların anormal bir şekilde dağılmasına bağlıdır.",
                masked_term="paternal kromozomların",
                hint="Trofoblastik büyümeyi yöneten babaya ait genetik yapılar"
            ),
            make_recall(
                question="Gebelikte plasenta ve trofoblast proliferasyonunu esas olarak hangi ebeveyne ait genom kontrol eder?",
                answer="Babadan gelen (paternal) genom kontrol eder; bu nedenle paternal aşırılık trofoblastik hiperplaziye yol açar."
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Molar Gebelik Genetik Kökeni",
                items=[
                    {"text": "Molar patoloji anormal fertilizasyon mekanizmalarından kaynaklanır.", "isLie": False, "explanation": "Doğru. Anormal döllenme paternleri esastır."},
                    {"text": "Komplet ve parsiyel olmak üzere iki morfolojik alt tipi tanımlanmıştır.", "isLie": False, "explanation": "Doğru. İki alt tip klinikte ve patolojide ayrılır."},
                    {"text": "Trofoblastik hiperplazi tamamen maternal genomun aşırı aktivitesi sonucu oluşur.", "isLie": True, "explanation": "Tuzak! Trofoblast gelişimi maternal değil paternal genom kontrolündedir; molar hastalık paternal aşırılıktır."},
                    {"text": "Paternal genomun baskınlığı koryon villuslarında sıvı birikimine ve proliferasyona yol açar.", "isLie": False, "explanation": "Doğru. Kistik veziküller bu aşırı trofoblastik aktiviteden doğar."}
                ]
            )
        ]
    ))

    # Slide 22
    slides.append(make_slide(
        slide_num=22,
        title="Komplet Mol Hidatiform: Androgenetik Mekanizma ve Karyotip",
        subtitle="Boş ovum, diploid paternal genom (46,XX ve 46,XY)",
        clinical_focus="Komplet molün döllenme dinamiği ve monozigotik/dizigotik patern",
        narrative=(
            "Komplet mol hidatiform, maternal çekirdek DNA'sı bulunmayan ('boş' veya inaktif) bir ovumun döllenmesi sonucu meydana gelir. "
            "Bu süreçte maternal nükleer genom tamamen kayıptır ve zigottaki tüm nükleer genetik materyal babadan kaynaklanır (**androgenez**).\n\n"
            "- **Monospermi (%90):** Vakaların yaklaşık %90'ında boş bir ovum tek bir haploid (23,X) sperm tarafından döllenir; sperm nükleusu ovum içinde kendi kendini kopyalayarak (duplikasyon) homozigot **diploid 46,XX** karyotipini meydana getirir.\n"
            "- **Dispermi (%10):** Vakaların yaklaşık %10'unda ise boş bir ovum iki ayrı bağımsız sperm (23,X ve 23,Y) tarafından eşzamanlı döllenir; bu durumda heterozigot **diploid 46,XY** (veya 46,XX) karyotip oluşur.\n"
            "- **Embriyogenezisin İflası:** Maternal nükleer DNA bulunmadığı için embriyonik organ gelişimi imkansızdır; **hiçbir zaman fetüse ait doku izlenmez**.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet mol hidatiformda döllenen ovum 'boştur'; karyotip diploittir (en sık 46,XX) ve nükleer genlerin %100'ü paternal kaynaklıdır."
        ),
        bullets=[
            "Maternal nükleusu olmayan 'boş ovum' döllenir",
            "Karyotip diploittir: En sık 46,XX (%90), nadiren 46,XY (%10)",
            "Tüm nükleer kromozomlar babadan gelir (androgenez)",
            "Embriyogenezise izin vermez; kesinlikle fetal doku bulunmaz"
        ],
        elements=[
            make_quiz(
                question="Komplet mol hidatiformun genetik yapısı ve döllenme mekanizması ile ilgili aşağıdaki ifadelerden hangisi patofizyolojik olarak DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Normal bir ovum iki spermle döllenir ve triploid (69,XXY) karyotip oluşur.", "isCorrect": False, "explanation": "Bu mekanizma parsiyel mol hidatiforma aittir; komplet mole değil."},
                    {"key": "B", "text": "Boş bir ovum döllenir, karyotip diploittir (çoğunlukla 46,XX) ve fetal doku izlenmez.", "isCorrect": True, "explanation": "Doğru. Komplet molde boş ovum döllenir, paternal diploid (46,XX) karyotip vardır ve hiçbir fetal doku bulunmaz."},
                    {"key": "C", "text": "Maternal DNA iki katına çıkar, sperm DNA'sı kaybolur ve monozomi oluşur.", "isCorrect": False, "explanation": "Maternal genom kayıptır, paternal genom aktiftir (partenogenez değil androgenezdir)."},
                    {"key": "D", "text": "Karyotip her zaman 47,XXY Klinefelter sendromudur.", "isCorrect": False, "explanation": "Klinefelter sendromu primer hipogonadizm tablosudur; komplet molde 46,XX diploidi esastır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Komplet mol hidatiform embriyogenezise izin vermediği için hiçbir zaman fetusa ait dokular izlenmez ve koryonik epitel hücreleri çoğunlukla diploittir.",
                masked_term="hiçbir zaman fetusa ait dokular izlenmez",
                hint="Maternal genom yokluğuna bağlı fetal organogenezisin imkansızlığı"
            ),
            make_table(
                title="Komplet Mol Fertilizasyon Mekanizmaları",
                headers=["Fertilizasyon Tipi", "Sıklık Oranı", "Oluşan Karyotip ve Patern"],
                rows=[
                    [
                        {"text": "Monospermik Duplikasyon", "isMasked": False},
                        {"text": "Olguların %90'ı", "isMasked": True, "hint": "Ezici çoğunluktaki yüzde"},
                        {"text": "46,XX (Tek spermin kopyalanması, homozigot)", "isMasked": False}
                    ],
                    [
                        {"text": "Dispermik Fertilizasyon", "isMasked": False},
                        {"text": "Olguların %10'u", "isMasked": True, "hint": "Kalan azınlık dilimi"},
                        {"text": "46,XY veya 46,XX (İki ayrı sperm girişi, heterozigot)", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Komplet mol hidatiformda 46,YY karyotipi neden hiçbir zaman canlı dokuda izlenmez?",
                answer="X kromozomu hayati genleri taşır; X kromozomu içermeyen bir zigot (46,YY) hücre bölünmesini bile başlatamadan ölür."
            )
        ]
    ))

    # Slide 23
    slides.append(make_slide(
        slide_num=23,
        title="Parsiyel Mol Hidatiform: Triploidi Mekanizması ve Fetal Varlık",
        subtitle="Normal ovum, dispermi ve triploid genom (69,XXY)",
        clinical_focus="Parsiyel molün sitogenetik yapısı ve embriyonik kanıtlar",
        narrative=(
            "Parsiyel mol hidatiformun genetik mekanizması komplet molden tamamen farklıdır. Burada döllenen ovum normaldir ve fonksiyonel maternal nükleer genetik materyal taşır (23,X).\n\n"
            "- **Dispermik Döllenme:** Normal bir haploid ovum, iki ayrı bağımsız sperm (veya nadiren bölünememiş tek bir diploid sperm) tarafından döllenir.\n"
            "- **Triploid Karyotip:** Maternal bir takıma karşılık iki takım paternal kromozom zigota katılır. Sonuçta toplam 69 kromozomlu **triploidi (en sık 69,XXY**, daha seyrek 69,XXX veya 69,XYY) ortaya çıkar.\n"
            "- **Fetal Dokuların Varlığı:** Maternal genom korunduğu için parsiyel molde kısıtlı bir embriyogenezis gerçekleşebilir. Küretaj materyalinde **fetal parçalar, kıkırdak odakları, amniyon zarı ve koryonik villus damarları içinde fetal çekirdekli eritrositler** izlenir. Ancak bu triploid fetüs malformasyonlar nedeniyle viable değildir.\n\n"
            "> [!IMPORTANT]\n"
            "> Parsiyel mol hidatiform daima triploidtir (69,XXY); komplet molden en kritik ayrımı fetal dokuların ve villus içi fetal eritrositlerin varlığıdır."
        ),
        bullets=[
            "Normal bir ovum iki sperm tarafından döllenir (dispermi)",
            "Karyotip daima triploidtir: En sık 69,XXY",
            "Maternal genom mevcut olduğu için embriyogenezis başlar",
            "Fetal parçalar ve villus içi fetal eritrositler izlenir"
        ],
        elements=[
            make_quiz(
                question="Normal bir ovumun iki ayrı sperm tarafından döllenmesi sonucu ortaya çıkan, triploid (69,XXY) karyotipe sahip olan ve histolojisinde fetal doku parçaları izlenen molar lezyon hangisidir?",
                options=[
                    {"key": "A", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Komplet molde boş ovum döllenir, diploidtir (46,XX) ve fetal doku kesinlikle bulunmaz."},
                    {"key": "B", "text": "İnvaziv komplet mol", "isCorrect": False, "explanation": "İnvaziv mol komplet molün derin myometrial invazyonudur; diploidtir ve fetüs içermez."},
                    {"key": "C", "text": "Parsiyel mol hidatiform", "isCorrect": True, "explanation": "Doğru. Parsiyel mol dispermi ile normal ovumun döllenmesinden doğar; triploidtir (69,XXY) ve fetal parçalar içerir."},
                    {"key": "D", "text": "Plasental bölge trofoblastik tümörü", "isCorrect": False, "explanation": "İntermediate trofoblastlardan köken alan nadir bir tümördür; triploid dispermi lezyonu değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Parsiyel mol hidatiform fetusa ait parçalar ve bir miktar normal koryonik villuslar içerir ve her zaman triploittir.",
                masked_term="her zaman triploittir",
                hint="Üç takım kromozom (69 kromozom) içerme durumu"
            ),
            make_slider(
                left_title="Komplet Mol Genetik Özeti",
                right_title="Parsiyel Mol Genetik Özeti",
                left_points=[
                    "Döllenen ovum: Boş (maternal DNA yok)",
                    "Karyotip: Diploid (46,XX veya 46,XY)",
                    "Genom kaynağı: %100 Paternal (androgenetik)",
                    "Fetal doku: Kesinlikle izlenmez (yoktur)"
                ],
                right_points=[
                    "Döllenen ovum: Normal haploid (23,X)",
                    "Karyotip: Daima triploid (69,XXY)",
                    "Genom kaynağı: 1 takım Anne + 2 takım Baba",
                    "Fetal doku: Fetal parçalar ve eritrositler bulunur"
                ]
            ),
            make_recall(
                question="Parsiyel mol hidatiformda saptanan en karakteristik kromozom sayısı ve karyotip formülü nedir?",
                answer="69 kromozomlu triploidi olup en sık 69,XXY formülünde izlenir."
            )
        ]
    ))

    # Slide 24
    slides.append(make_slide(
        slide_num=24,
        title="Komplet Mol Hidatiform: Histopatolojik Bulgular",
        subtitle="Diffüz villöz ödem, santral sisterna ve avasküler stroma",
        clinical_focus="Komplet molün mikroskobik tanı kriterleri",
        narrative=(
            "Komplet mol hidatiformun histopatolojik incelemesinde villusların neredeyse tamamını (%100) tutan belirgin bir kistik transformasyon izlenir.\n\n"
            "- **Diffüz Hidrofik Genişleme:** Tüm koryon villusları ileri derecede hidropik şişme gösterir. Villusların santralindeki stroma sıvı birikimiyle çözünür ve geniş sıvı dolu boşluklar (**sisterna**) meydana gelir.\n"
            "- **Fetal Damar Yokluğu:** Komplet molde embriyonik dolaşım hiçbir zaman kurulamaz; bu nedenle villus stromasında **fetal kapillerler ve fetal eritrositler tamamen yoktur (avasküler villus)**.\n"
            "- **Diffüz Çevresel Proliferasyon:** Koryonik villusların çevresini 360 derece çepeçevre saran belirgin sito- ve sinsityotrofoblastik hiperplazi izlenir. Bu proliferasyona belirgin nükleer atipi ve sık mitotik figürler eşlik eder.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet molün mikroskobik patognomonik ikilisi: Villusların tamamında hidrofik sisterna oluşumu ve villus içi fetal damarların kesin yokluğudur."
        ),
        bullets=[
            "Villusların tümünde (%100) diffüz hidrofik genişleme",
            "Santral miksomatöz erime ve sıvı dolu sisterna oluşumu",
            "Villus içi fetal damarlar ve fetal eritrositler tamamen yoktur",
            "Villusları çepeçevre saran diffüz trofoblastik proliferasyon ve atipi"
        ],
        elements=[
            make_quiz(
                question="Komplet mol hidatiformun mikroskobik incelemesinde koryonik villus stroması ile ilgili saptanan en karakteristik patolojik özellik nedir?",
                options=[
                    {"key": "A", "text": "Villus içinde bol miktarda çekirdekli fetal eritrosit içeren geniş kapiller ağ", "isCorrect": False, "explanation": "Fetal kapiller ve eritrositler parsiyel molde izlenir; komplet molde villus damarı yoktur."},
                    {"key": "B", "text": "Villus içi damarların tamamen yokluğu ve santral sisterna oluşumu", "isCorrect": True, "explanation": "Doğru. Komplet molde embriyogenezis olmadığı için villus içi damarlar bulunmaz ve santralde sıvı dolu sisterna oluşur."},
                    {"key": "C", "text": "Villus stromasının yoğun nötrofil infiltrasyonu ve granülomlarla dolması", "isCorrect": False, "explanation": "Bu durum enfeksiyöz villitis (listeria veya sifiliz) bulgusudur; mol tablosu değildir."},
                    {"key": "D", "text": "Villusların tamamen atrofiye uğrayarak fibröz kordonlara dönüşmesi", "isCorrect": False, "explanation": "Komplet molde villuslar atrofik değil, aşırı hidropik ve geniştir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Komplet molde villuslarda hidrofik şişme vardır ve villus içindeki damarlar yoktur.",
                masked_term="villus içindeki damarlar yoktur",
                hint="Fetal vaskülarizasyonun ve kapiller ağın bulunmama durumu"
            ),
            make_table(
                title="Komplet Mol Villus Histolojisi Parametreleri",
                headers=["Morfolojik Alan", "Histopatolojik Görünüm", "Klinik Yorum"],
                rows=[
                    [
                        {"text": "Villöz Tutulum", "isMasked": False},
                        {"text": "Diffüz, tüm villuslar hidrofik", "isMasked": True, "hint": "Dokunun yüzde yüzünde yaygınlaşma"},
                        {"text": "Üzüm salkımı görüntüsünü oluşturur", "isMasked": False}
                    ],
                    [
                        {"text": "Vaskülarizasyon", "isMasked": False},
                        {"text": "Fetal damar tamamen yoktur", "isMasked": True, "hint": "Avasküler villus stroması"},
                        {"text": "Fetal dolaşımın kurulamadığını kanıtlar", "isMasked": False}
                    ],
                    [
                        {"text": "Trofoblast Proliferasyonu", "isMasked": False},
                        {"text": "Diffüz ve çevresel (çevresel hiperplazi)", "isMasked": False},
                        {"text": "Yüksek hCG salınımının hücresel kaynağıdır", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Bir koryon villusunun komplet mole ait olduğunu gösteren mikroskobik damar bulgusu nedir?",
                answer="Villus stromasında fetal kan damarlarının ve fetal eritrositlerin kesinlikle bulunmamasıdır (avasküler stroma)."
            )
        ]
    ))

    # Slide 25
    slides.append(make_slide(
        slide_num=25,
        title="Parsiyel Mol Hidatiform: Histopatolojik Bulgular",
        subtitle="Villöz heterojenite, girintili kenarlar ve psödoinklüzyonlar",
        clinical_focus="Parsiyel molün mikroskobik ayırt edici morfolojisi",
        narrative=(
            "Parsiyel mol hidatiform mikroskop altında komplet molün homojen kistik tablosundan oldukça farklı, heterojen bir patern sergiler.\n\n"
            "- **Villöz Heterojenite:** Villusların yalnızca bir kısmı hidrofik genişleme gösterirken, diğer kısmı normal boyutlarda hatta küçük ve fibrotiktir. İki farklı villus populasyonunun yan yana bulunması tipiktir.\n"
            "- **Girintili Çıkıntılı Kontur ve Psödoinklüzyon:** Hidrofik villusların kenarları düzgün yuvarlak değil; derin çentikler ve girintiler taşır (scalloped borders). Kesit düzlemine bağlı olarak trofoblast hücreleri villus stromasının içine gömülmüş gibi görünür (**trofoblastik psödoinklüzyonlar**).\n"
            "- **Odaksal Proliferasyon:** Trofoblastik proliferasyon komplet molden farklı olarak diffüz değil; fokal, odaksal ve hafiftir; belirgin sitolojik atipi izlenmez.\n"
            "- **Fetal Eritrositler:** Villus içi damarlar mevcuttur ve bu damarlarda sıklıkla çekirdekli fetal eritrositler saptanır.\n\n"
            "> [!NOTE]\n"
            "> Girintili çıkıntılı villus kenarları, trofoblastik psödoinklüzyonlar ve villus içi fetal eritrositler parsiyel molün en güvenilir tanısal ipuçlarıdır."
        ),
        bullets=[
            "Villöz heterojenite: Hidrofik ve küçük fibrotik villuslar bir arada",
            "Villus kenarlarında belirgin girinti-çıkıntılar (scalloping)",
            "Trofoblastik psödoinklüzyonlar karakteristiktir",
            "Fokal ve hafif trofoblast proliferasyonu; fetal eritrositler izlenir"
        ],
        elements=[
            make_quiz(
                question="Koryonik villusların mikroskopisinde villöz heterojenite (büyük hidrofik ve küçük fibrotik villuslar), çentikli girintili kenarlar ve trofoblastik psödoinklüzyonlar izlenmesi öncelikle hangi tanıyı destekler?",
                options=[
                    {"key": "A", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Komplet molde tüm villuslar homojen diffüz hidropiktir; çentiklenme veya çift populasyon görülmez."},
                    {"key": "B", "text": "Parsiyel mol hidatiform", "isCorrect": True, "explanation": "Doğru. Villöz heterojenite, çentikli scalloped kenarlar ve psödoinklüzyonlar parsiyel molün patognomonik mikroskopisidir."},
                    {"key": "C", "text": "Koryokarsinom", "isCorrect": False, "explanation": "Koryokarsinomda hiçbir şekilde koryon villusu bulunmaz; saf hücre kitlesidir."},
                    {"key": "D", "text": "Tüberkülöz villitis", "isCorrect": False, "explanation": "Tüberküloz granülomatöz kazeifiye iltihap yapar; molar trofoblastik psödoinklüzyon yapmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Parsiyel molde genişlemiş villuslar girintili çıkıntılı halde izlenir ve sekonder trofoblastik psödoinklüzyonlar içerir.",
                masked_term="trofoblastik psödoinklüzyonlar",
                hint="Villus girintilerinin kesitte stroma içi ada gibi görünmesi"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Parsiyel Mol Mikroskopisi",
                items=[
                    {"text": "Villus populasyonunda hidrofik genişlemiş ve küçük fibrotik villuslar bir arada yer alır.", "isLie": False, "explanation": "Doğru. Villöz heterojenite parsiyel molün esasıdır."},
                    {"text": "Villus sınırları girintili çıkıntılı (scalloped) kontura sahiptir.", "isLie": False, "explanation": "Doğru. Çentikli düzensiz sınırlar tipiktir."},
                    {"text": "Villus içi fetal damarlar bulunur ve sıklıkla fetal eritrositler saptanır.", "isLie": False, "explanation": "Doğru. Fetal hematopoez kanıtları mevcuttur."},
                    {"text": "Villusların çevresinde koryokarsinoma benzer yaygın, diffüz, 360 derece anaplastik trofoblast proliferasyonu vardır.", "isLie": True, "explanation": "Tuzak! Parsiyel molde trofoblastik proliferasyon diffüz değil; odaksal, hafif ve atipisizdir; diffüz ve atipik proliferasyon komplet molde görülür."}
                ]
            ),
            make_recall(
                question="Parsiyel molde trofoblastik psödoinklüzyon oluşumunun mekanizması nedir?",
                answer="Villus kenarlarındaki derin girinti ve çentiklerin (scalloping) doku kesitinde stroma içinde hapsolmuş epitel adacıkları gibi görünmesidir."
            )
        ]
    ))

    # Slide 26
    slides.append(make_slide(
        slide_num=26,
        title="Komplet ve Parsiyel Mol: Karşılaştırmalı Ayırıcı Tanı",
        subtitle="Genetik, morfolojik ve onkolojik risk tablosu",
        clinical_focus="İki molar lezyonun patolojik ve klinik parametrelerinin sentezi",
        narrative=(
            "Molar gebeliğin bu iki alt tipinin doğru ayırt edilmesi, hastanın takip protokolünü ve malignite risk değerlendirmesini doğrudan belirler.\n\n"
            "- **Karyotip Farkı:** Komplet mol diploidtir (46,XX); parsiyel mol triploidtir (69,XXY).\n"
            "- **Villöz Ödem ve Atipi:** Komplet molde tüm villuslarda diffüz ödem ve belirgin trofoblastik atipi izlenirken; parsiyel molde bazı villuslarda odaksal ödem izlenir ve atipi saptanmaz.\n"
            "- **Serum hCG Düzeyleri:** Komplet molde aşırı trofoblastik proliferasyon nedeniyle serum hCG düzeyleri yüzbinlerce üniteye ulaşırken; parsiyel molde hCG artışı daha ılımlıdır.\n"
            "- **Malignite Riski:** Komplet mollerin %10'u invaziv mole, %2-3'ü koryokarsinoma ilerlerken; parsiyel molde koryokarsinom gelişimi son derece nadirdir (<%0.1).\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet mol yüksek hCG, diffüz atipi ve %2 koryokarsinom riski taşır; parsiyel molde ise fetüs parçaları bulunur ve koryokarsinom riski ihmal edilebilir düzeydedir."
        ),
        bullets=[
            "Komplet: Diploid (46,XX), diffüz ödem, fetüs yok, belirgin atipi",
            "Parsiyel: Triploid (69,XXY), fokal ödem, fetüs parçaları var, atipi yok",
            "Serum hCG: Komplet molde çok yüksek, parsiyel molde ılımlı artış",
            "Malignite: Komplet molde %2 koryokarsinom riski, parsiyelde nadir"
        ],
        elements=[
            make_table(
                title="Komplet ve Parsiyel Mol Karşılaştırma Matrisi",
                headers=["Özellik", "Komplet Mol", "Parsiyel Mol"],
                rows=[
                    [
                        {"text": "Karyotip", "isMasked": False},
                        {"text": "Diploid (46,XX veya 46,XY)", "isMasked": True, "hint": "İki takım kromozom"},
                        {"text": "Triploid (69,XXY)", "isMasked": True, "hint": "Üç takım kromozom"}
                    ],
                    [
                        {"text": "Fetal Doku", "isMasked": False},
                        {"text": "Kesinlikle yoktur", "isMasked": False},
                        {"text": "Mevcuttur (parçalar/eritrosit)", "isMasked": True, "hint": "Embriyonik kalıntı varlığı"}
                    ],
                    [
                        {"text": "Trofoblast Atipisi", "isMasked": False},
                        {"text": "Sıklıkla mevcuttur", "isMasked": False},
                        {"text": "Kural olarak yoktur", "isMasked": False}
                    ],
                    [
                        {"text": "Koryokarsinom Riski", "isMasked": False},
                        {"text": "Yüzde 2-3 civarında", "isMasked": True, "hint": "Düşük tek haneli malignite oranı"},
                        {"text": "Son derece nadirdir", "isMasked": False}
                    ]
                ]
            ),
            make_quiz(
                question="Komplet mol hidatiform ile parsiyel mol hidatiform karşılaştırıldığında hangisi KOMPLET MOL lehine bir özelliktir?",
                options=[
                    {"key": "A", "text": "Triploid (69,XXY) karyotip bulunması", "isCorrect": False, "explanation": "Triploidi parsiyel molün özelliğidir."},
                    {"key": "B", "text": "Villus içinde fetal doku ve fetal eritrositlerin saptanması", "isCorrect": False, "explanation": "Fetal dokular parsiyel molde bulunur."},
                    {"key": "C", "text": "Trofoblastik proliferasyonun sadece fokal ve hafif sınırlı kalması", "isCorrect": False, "explanation": "Fokal proliferasyon parsiyel moldür; komplet molde diffüz hiperplazi vardır."},
                    {"key": "D", "text": "Trofoblastlarda sitolojik atipi ve yaklaşık %2 oranında koryokarsinom riski", "isCorrect": True, "explanation": "Doğru. Komplet molde sitolojik atipi sıktır ve olguların %2-3'ünde koryokarsinom gelişme potansiyeli mevcuttur."}
                ],
                correct_key="D"
            ),
            make_venn(
                title="Komplet Mol vs Parsiyel Mol Karşılaştırması",
                label_a="Komplet Mol",
                label_b="Parsiyel Mol",
                items=[
                    {"criterion": "Karyotipin diploid (46,XX) olması ve fetal doku içermemesi", "correct": "A", "explanation": "Komplet molde fetüs dokusu kesinlikle yoktur."},
                    {"criterion": "Karyotipin triploid (69,XXY) olması ve fetal eritrosit içermesi", "correct": "B", "explanation": "Parsiyel molde fetal parçalar ve triploidi saptanır."},
                    {"criterion": "Anormal fertilizasyona bağlı trofoblastik hastalık spektrumunda yer alma", "correct": "both", "explanation": "Her iki form da paternal genom anomalisiyle gelişen molar gebeliktir."},
                    {"criterion": "Akciğerlere erken hematojen metastaz yaparak %100 fatal seyretme", "correct": "neither", "explanation": "Moller selimdir, metastaz yapmaz; fatal metastaz koryokarsinoma özgüdür."}
                ]
            ),
            make_recall(
                question="Komplet mol hastasında küretaj sonrası koryokarsinoma progresyon riski yüzde kaçtır?",
                answer="Yaklaşık %2-3 oranındadır (ayrıca %10 invaziv mole ilerler)."
            )
        ]
    ))

    # Slide 27
    slides.append(make_slide(
        slide_num=27,
        title="Mol Hidatiform: Klinik Tablo ve Risk Faktörleri",
        subtitle="Uç yaşlar (<20 ve >40 yaş), Asya coğrafyası ve klinik triad",
        clinical_focus="Molar gebeliğin epidemiyolojik demografisi ve semptomları",
        narrative=(
            "Mol hidatiform gelişiminde anne yaşı en kuvvetli epidemiyolojik risk faktörüdür. Yaş dağılımı klasik bir 'U eğrisi' çizer.\n\n"
            "- **Uç Yaşlar:** Molar gebelik riski **20 yaş altındaki çok genç gebelerde** ve özellikle **40 yaş üzerindeki ileri anne yaşında** belirgin şekilde artar (40 yaş üzerinde risk 5-10 katına çıkar).\n"
            "- **Coğrafi Dağılım:** Molar hastalık insidansı Batı ülkelerine kıyasla **Asya ülkelerinde** (örneğin Güneydoğu Asya ve Filipinler) belirgin olarak daha sıktır.\n"
            "- **Klinik Triad:** Gebeliğin 12-14. haftalarında **ağrısız vajinal kanama**, kistik veziküller nedeniyle **gününe göre çok büyük uterus** ve fetal kalp seslerinin duyulmaması en tipik klinik tablodur. Aşırı hCG artışı şiddetli bulantı-kusmaya (hiperemezis gravidarum) ve erken preeklampsi bulgularına yol açabilir.\n\n"
            "> [!NOTE]\n"
            "> 20 yaş öncesi ve 40 yaş sonrası gebelikler ile Asya kökeni mol hidatiform gelişiminde en belirgin epidemiyolojik risk faktörleridir."
        ),
        bullets=[
            "En yüksek risk uç yaşlardadır: <20 yaş ve >40 yaş gebelikler",
            "Asya ülkelerinde görülme insidansı belirgin yüksektir",
            "Klasik prezentasyon: Vajinal kanama ve gününe göre büyük uterus",
            "Fetal kalp sesleri duyulmaz; aşırı hCG nedeniyle hiperemezis eşlik eder"
        ],
        elements=[
            make_quiz(
                question="Mol hidatiform epidemiyolojisinde görülme sıklığının en yüksek olduğu yaş grupları ve coğrafi bölge aşağıdakilerden hangisidir?",
                options=[
                    {"key": "A", "text": "25-30 yaş arası — Kuzey Avrupa ülkeleri", "isCorrect": False, "explanation": "25-30 yaş en düşük risk grubudur."},
                    {"key": "B", "text": "20 yaş öncesi ve 40 yaş sonrası — Asya ülkeleri", "isCorrect": True, "explanation": "Doğru. Mol hidatiform 20 yaş altı ve 40 yaş üstü uç yaşlarda ve Asya coğrafyasında belirgin yüksek sıklıkta izlenir."},
                    {"key": "C", "text": "Yalnızca 30-35 yaş arası multiparlar — Sahra altı Afrika", "isCorrect": False, "explanation": "Uç yaşlar molar gebelikte temel risk faktörüdür."},
                    {"key": "D", "text": "Postmenopozal dönem — Akdeniz kuşağı", "isCorrect": False, "explanation": "Mol hidatiform fertilizasyon komplikasyonudur; postmenopozda döllenme olmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Komplet mol hidatiform insidansı yaş grupları açısından 20 yaş öncesi ve 40 yaş sonrası daha sıktır.",
                masked_term="20 yaş öncesi ve 40 yaş sonrası",
                hint="Doğurganlık döneminin iki uç sınırındaki zaman dilimleri"
            ),
            make_recall(
                question="İlk trimesterde gebelik haftasına göre belirgin büyük uterus ve vajinal kanaması olan bir gebede fetal kalp seslerinin alınamaması neyi düşündürür?",
                answer="Komplet mol hidatiformu düşündürür; acil ultrasonografi ve beta-hCG ölçümü gerektirir."
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Molar Gebelik Kliniği",
                items=[
                    {"text": "Molar gebelik riski 40 yaş üzeri gebeliklerde belirgin artış gösterir.", "isLie": False, "explanation": "Doğru. İleri anne yaşı majör risk faktörüdür."},
                    {"text": "Asya toplumlarında molar hastalık insidansı Batı'ya kıyasla daha yüksektir.", "isLie": False, "explanation": "Doğru. Coğrafi ve ırksal yatkınlık mevcuttur."},
                    {"text": "Komplet molar gebelikte uterus muayenede her zaman haftasına göre aşırı derecede küçük kalır.", "isLie": True, "explanation": "Tuzak! Komplet molde kistik veziküller ve kan birikimi nedeniyle uterus gününe göre belirgin olarak çok büyüktür."},
                    {"text": "Aşırı yükselen hCG düzeyleri gebelikte erken preeklampsi tablosunu tetikleyebilir.", "isLie": False, "explanation": "Doğru. İlk trimesterde preeklampsi bulguları mol lehinedir."}
                ]
            )
        ]
    ))

    # Slide 28
    slides.append(make_slide(
        slide_num=28,
        title="Mol Hidatiform: Küretaj Sonrası Seyir ve Takip",
        subtitle="%80-90 şifa, %10 invaziv mol ve %2-3 koryokarsinom riski",
        clinical_focus="Molar tahliye sonrası beta-hCG izlemi ve persistan hastalık yönetimi",
        narrative=(
            "Mol hidatiform saptanan bir hastada primer tedavi uterin kavitenin emme küretajı (vakum aspirasyon) ile tamamen boşaltılmasıdır. Ancak işlem cerrahi olarak tamamlansa bile hastanın onkolojik takibi hayati önem taşır.\n\n"
            "- **Benign Seyir Oranı:** Vakum küretaj uygulanan mol hidatiform olgularının **%80-90'ı sorunsuz iyileşir** ve hastalık tekrarlamaz.\n"
            "- **Lokal İnvazyon ve Malignite Riski:** Komplet mol olgularının yaklaşık **%10'unda trofoblastlar myometriuma penetre olarak invaziv mole** dönüşür; olguların **%2-3'ünde ise agresif koryokarsinom** gelişir.\n"
            "- **Beta-hCG İzlemi:** Küretajdan sonra haftalık serum beta-hCG seviyeleri takip edilir. Hormon düzeyinin düşmemesi, plato çizmesi veya yeniden yükselmesi tam olmayan küretajı, invaziv molü veya koryokarsinoma gidişi gösterir.\n\n"
            "> [!IMPORTANT]\n"
            "> Mollerin %80-90'ı küretaj sonrası tekrarlamaz; komplet mollerin %10'u invaziv olup %2-3'ünde koryokarsinom gelişir."
        ),
        bullets=[
            "Primer tedavi vakum küretaj ile kavitenin boşaltılmasıdır",
            "Olguların %80-90'ında tam şifa sağlanır, nüks olmaz",
            "Komplet mollerin yaklaşık %10'u invaziv mole ilerler",
            "Komplet mollerin %2-3'ünde koryokarsinom gelişir; beta-hCG takibi zorunludur"
        ],
        elements=[
            make_quiz(
                question="Vakum küretaj ile tahliye edilen komplet mol hidatiform olgularında postoperatif dönemde koryokarsinom gelişme riski yaklaşık yüzde kaçtır?",
                options=[
                    {"key": "A", "text": "%50-60", "isCorrect": False, "explanation": "Bu oran koryokarsinomun komplet molden köken alma payıdır; molün kanserleşme riski değildir."},
                    {"key": "B", "text": "%20-30", "isCorrect": False, "explanation": "Bu oran atipili endometrial hiperplazinin kanserleşme riskidir."},
                    {"key": "C", "text": "%2-3", "isCorrect": True, "explanation": "Doğru. Komplet mollerin %80-90'ı kür olurken %10'u invaziv mole, %2-3'ü ise koryokarsinoma ilerler."},
                    {"key": "D", "text": "%0 (asla gelişmez)", "isCorrect": False, "explanation": "Miyom sarkoma dönüşmez ancak komplet molün %2-3 koryokarsinom riski vardır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Mollerin yüzde 80-90 kadarı küretaj sonrası tekrarlamaz; komplet mollerin yüzde 10 kadarı invaziv olup yüzde 2-3 kadarında koryokarsinom gelişir.",
                masked_term="yüzde 2-3",
                hint="Komplet molün koryokarsinoma dönüşme olasılık dilimi"
            ),
            make_chain(
                "Mol Hidatiform Postoperatif Takip Zinciri",
                [
                    "1. Cerrahi Tahliye: Uterus kavitesindeki kistik molar doku vakum küretaj ile temizlenir.",
                    "2. Seri Beta-hCG Monitörizasyonu: Serum beta-hCG düzeyleri haftalık ölçümlerle sıfırlanana kadar takip edilir.",
                    "3. Persistan Hastalık Tespiti: Hormon değerlerinin plato yapması veya yükselmesi durumunda invaziv mol / koryokarsinom lehine ileri görüntüleme ve kemoterapi başlatılır."
                ]
            ),
            make_recall(
                question="Molar gebelik küretajı sonrasında hastanın remisyonda olduğunu teyit etmek için hangi laboratuvar parametresi izlenir?",
                answer="Serum beta-hCG alt biriminin seri haftalık takibidir; değerlerin sıfırlanması tam remisyonu gösterir."
            )
        ]
    ))

    # Slide 29
    slides.append(make_slide(
        slide_num=29,
        title="Erken Molar Gebelik ve Güncel Ultrasonografi Tanısı",
        subtitle="Erken gebelik haftalarında histopatolojik tanı güçlükleri",
        clinical_focus="12-14. haftalardan 6-8. haftalara kayan molar tanı süreci",
        narrative=(
            "Geçmişte komplet mol hidatiform olguları gebeliğin 12-14. haftalarında aşırı vajinal kanama, üzüm taneleri dökülmesi ve aşırı büyük uterus kliniğiyle geç dönemde tanınıyordu. "
            "Günümüzde yüksek çözünürlüklü transvajinal ultrasonografi ve erken gebelikte rutin beta-hCG taramaları sayesinde molar gebelikler çok daha erken haftalarda (6-8. haftalar) saptanmaktadır.\n\n"
            "- **Erken Komplet Mol Morfolojisi:** Erken haftalarda koryon villuslarında tam gelişmiş klasik sisterna formasyonu ve aşırı belirgin trofoblastik hiperplazi henüz oturmamış olabilir.\n"
            "- **Histolojik Tuzak:** Erken mol villusları hidropik abortus villuslarına benzeyebilir. Tanıda villus çevresindeki hafif polarize trofoblast tomurcuklanması ve immünohistokimyasal belirteçler (p57KIP2 kaybı) yol göstericidir.\n"
            "- **Erken Tanının Faydası:** Hastalar hayatı tehdit eden ağır kanama veya preeklampsi krizlerine girmeden erken dönemde tedavi edilmektedir.\n\n"
            "> [!NOTE]\n"
            "> Günümüz obstetrik pratiğinde erken ultrasonografi sayesinde klasik üzüm salkımı manzarası oturmadan 'erken komplet mol' tanısı konabilmektedir."
        ),
        bullets=[
            "Eski klasik tanı: 12-14. haftada ağır kanama ve üzüm dökülmesi",
            "Güncel yaklaşım: Transvajinal USG ile 6-8. haftada erken tanı",
            "Erken komplet molde klasik sisterna ve aşırı atipi henüz belirginleşmeyebilir",
            "Erken teşhis hayatı tehdit eden komplikasyonları önler"
        ],
        elements=[
            make_quiz(
                question="Modern obstetrikte transvajinal ultrasonografinin yaygınlaşması ile komplet mol hidatiformun klinik ve histopatolojik prezentasyonunda meydana gelen temel değişim nedir?",
                options=[
                    {"key": "A", "text": "Hastalığın tamamen ortadan kalkması ve insidansın sıfırlanması", "isCorrect": False, "explanation": "İnsidans sıfırlanmamıştır; tanı zamanı öne çekilmiştir."},
                    {"key": "B", "text": "Karyotipin diploidden triploide dönüşmesi", "isCorrect": False, "explanation": "Genetik yapı değişmez; komplet mol daima diploid kalır."},
                    {"key": "C", "text": "Hastalığın 12-14. haftalar yerine 6-8. haftalarda 'erken komplet mol' olarak saptanması", "isCorrect": True, "explanation": "Doğru. Yüksek çözünürlüklü USG sayesinde lezyon tam gelişmiş üzüm salkımı tablosuna ulaşmadan 6-8. haftalarda erken teşhis edilmektedir."},
                    {"key": "D", "text": "Koryokarsinoma dönüşüm riskinin %100'e fırlaması", "isCorrect": False, "explanation": "Erken tanı komplikasyonları azaltır; riski artırmaz."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Gelişen ultrason sayesinde gebelik haftasına göre çok büyük uterus olguları erken komplet mol olarak çok daha erken saptanmaktadır.",
                masked_term="erken komplet mol",
                hint="Görüntülemenin ilk trimesterde yakaladığı lezyon evresi"
            ),
            make_recall(
                question="Erken komplet mol hidatiform olgularında mikroskobik incelemede patoloğu yanıltabilecek temel morfolojik durum nedir?",
                answer="Klasik kistik sisternaların ve belirgin trofoblastik hiperplazinin henüz tam gelişmemiş olması nedeniyle basit hidropik abortusla karışabilmesidir."
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erken Molar Tanı",
                items=[
                    {"text": "Transvajinal ultrason erken haftalarda intrauterin anormallikleri tespit edebilir.", "isLie": False, "explanation": "Doğru. Erken molar eko paternini yakalar."},
                    {"text": "Erken tanı sayesinde hastalar ağır anemi ve şok tablosu gelişmeden tedavi edilir.", "isLie": False, "explanation": "Doğru. Erken küretaj komplikasyonları önler."},
                    {"text": "Erken komplet molde villusların içinde daima canlı embriyo iskeleti izlenir.", "isLie": True, "explanation": "Tuzak! Komplet mol ister erken ister geç olsun hiçbir zaman fetal doku içermez."},
                    {"text": "Erken dönemde koryon villus ödemi hidropik düşük ile ayırıcı tanı gerektirebilir.", "isLie": False, "explanation": "Doğru. Histopatolojide erken evrede ayrım zordur."}
                ]
            )
        ]
    ))

    # Slide 30 - Checkpoint 3
    slides.append(make_slide(
        slide_num=30,
        title="[TEKRAR SAYFASI - CHECKPOINT 3] Mol Hidatiform Genetiği ve Morfolojisi",
        subtitle="Bölüm 3 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Komplet vs parsiyel mol genetiği, histopatolojisi ve klinik seyir özeti",
        narrative=(
            "Bu tekrar sayfası, 21-29. adımlarda işlenen Mol Hidatiform Genetiği ve Komplet vs Parsiyel Mol kazanımlarını pekiştirmek için düzenlenmiştir. "
            "Molar gebelikler paternal kromozom dengesizliklerinden kaynaklanan anormal fertilizasyon ürünleridir.\n\n"
            "- **Komplet Mol:** Boş ovum döllenir; karyotip diploidtir (en sık 46,XX). Fetüs dokusu kesinlikle yoktur; villusların tamamı diffüz hidropiktir ve fetal damar bulunmaz. %10 invaziv mole, %2-3 koryokarsinoma ilerler.\n"
            "- **Parsiyel Mol:** Normal ovum iki spermle döllenir (dispermi); karyotip triploidtir (69,XXY). Fetal dokular ve fetal eritrositler bulunur. Villöz heterojenite, çentikli kenarlar ve trofoblastik psödoinklüzyonlar izlenir; koryokarsinom riski ihmal edilebilir.\n"
            "- **Klinik ve Takip:** 20 yaş altı ve 40 yaş üstü uç yaşlarda ve Asya'da sıktır. Küretaj sonrası olguların %80-90'ı kür olur; takipler seri haftalık beta-hCG ölçümleriyle yapılır.\n\n"
            "> [!NOTE]\n"
            "> Komplet mol: Diploid + Fetüs yok + Damarsız villus + %2 kanser riski; Parsiyel mol: Triploid + Fetüs var + Girintili villus + Kanser riski yok denecek kadar az."
        ),
        bullets=[
            "Komplet mol: Boş ovum, diploid (46,XX), fetal doku yok, diffüz ödem",
            "Parsiyel mol: Normal ovum + 2 sperm, triploid (69,XXY), fetal doku var",
            "Komplet molde villus damarı yoktur; parsiyelde fetal eritrositler izlenir",
            "Uç yaşlar (<20, >40) ve Asya kökeni majör risk faktörüdür",
            "Mollerin %80-90'ı kür olur; komplet molde %2-3 koryokarsinom riski vardır"
        ],
        elements=[
            make_quiz(
                question="Komplet mol hidatiform ile parsiyel mol hidatiformun ayırıcı tanısında aşağıdakilerden hangisi kesin bir ayırıcı kriterdir?",
                options=[
                    {"key": "A", "text": "Komplet molde uterusun normalden küçük olması, parsiyelde ise dev boyutlara ulaşması", "isCorrect": False, "explanation": "Yanlış. Komplet molde uterus gününe göre çok büyüktür."},
                    {"key": "B", "text": "Komplet molde karyotipin diploid (46,XX) olup fetal doku içermemesi; parsiyelde triploid (69,XXY) olup fetal parçalar içermesi", "isCorrect": True, "explanation": "Doğru. Karyotip (diploid vs triploid) ve fetal doku varlığı en temel ve kesin ayırıcı kriterlerdir."},
                    {"key": "C", "text": "Parsiyel molün %50 koryokarsinoma dönüşmesi, komplet molün ise tamamen selim kalması", "isCorrect": False, "explanation": "Yanlış. Koryokarsinom riski komplet molde (%2-3) vardır; parsiyelde neredeyse hiç yoktur."},
                    {"key": "D", "text": "Komplet molün sadece postmenopozal dönemde görülmesi", "isCorrect": False, "explanation": "Yanlış. Mol gebelik ürünüdür; reprodüktif dönemde ortaya çıkar."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Komplet mol hidatiform vakalarında koryonik villus epitel hücreleri çoğunlukla diploit olarak saptanır.",
                masked_term="diploit",
                hint="İki takım kromozom (2n) taşıma durumu"
            ),
            make_table(
                title="Bölüm 3 Temel Molar Kazanımlar Özeti",
                headers=["Özellik", "Komplet Mol", "Parsiyel Mol"],
                rows=[
                    [
                        {"text": "Genetik Döllenme", "isMasked": False},
                        {"text": "Boş ovum + sperm", "isMasked": True, "hint": "Çekirdeksiz yumurtanın döllenmesi"},
                        {"text": "Normal ovum + 2 sperm (dispermi)", "isMasked": False}
                    ],
                    [
                        {"text": "Karyotip", "isMasked": False},
                        {"text": "46,XX (Diploid)", "isMasked": False},
                        {"text": "69,XXY (Triploid)", "isMasked": True, "hint": "Üç takım kromozom formülü"}
                    ],
                    [
                        {"text": "Fetal Doku & Eritrosit", "isMasked": False},
                        {"text": "Hiçbir zaman izlenmez", "isMasked": True, "hint": "Embriyo kanıtının kesin yokluğu"},
                        {"text": "Mevcuttur ve izlenebilir", "isMasked": False}
                    ],
                    [
                        {"text": "Villus İçi Damarlanma", "isMasked": False},
                        {"text": "Damarlar yoktur", "isMasked": True, "hint": "Fetal vasküler yapının bulunmaması"},
                        {"text": "Damarlar ve fetal eritrositler vardır", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 3 Kontrol Önermeleri",
                items=[
                    {"text": "Komplet mol hidatiform olgularının %80-90'ı küretaj sonrasında sorunsuz iyileşir.", "isLie": False, "explanation": "Doğru. Büyük çoğunluğu küretajla tam şifaya kavuşur."},
                    {"text": "Komplet mollerin yaklaşık %10'u invaziv mole, %2-3'ü koryokarsinoma ilerler.", "isLie": False, "explanation": "Doğru. Klinik onkolojik takip gerektiren oranlardır."},
                    {"text": "Parsiyel molde fetal parçaların varlığı komplet moldekinden çok daha yüksek oranda koryokarsinoma yol açar.", "isLie": True, "explanation": "Tuzak! Koryokarsinom riski komplet molde (%2-3) yüksektir; parsiyel molde koryokarsinom gelişimi istisnadır."},
                    {"text": "Trofoblastik hastalıklarda hCG düzeylerinin takibi nüks veya invazyonu saptamada temel rehberdir.", "isLie": False, "explanation": "Doğru. Beta-hCG takibi altın standarttır."}
                ]
            ),
            make_recall(
                question="Checkpoint 3: Komplet mol hidatiform ile parsiyel mol hidatiformun karyotiplerini ve fetal doku durumlarını tek bir cümleyle özetleyiniz.",
                answer="Komplet mol diploidtir (46,XX) ve fetal doku içermez; parsiyel mol ise triploidtir (69,XXY) ve fetal parçalar içerir."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=3
    ))
    
    return slides
