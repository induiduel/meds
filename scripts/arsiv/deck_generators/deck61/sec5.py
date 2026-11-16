# -*- coding: utf-8 -*-
"""
Deck 61 Section 5: Abortus Tipleri Ayrımı 2 — İnkomplet Abortus ve Komplet Abortus
Slides 41-50 (Checkpoint 5 at slide 50)
Focus:
- İnkomplet abortus (tam olmayan düşük) tanımı: Gebelik ürünlerinin bir kısmının dışarı atılmış olması
- İnkomplet abortus klinik ve pelvik muayene: Servikal kanal AÇIK, yoğun kanama, vajinada plasental doku parçaları
- İnkomplet abortus ultrasonografisi: Kavitede bozulmuş gebelik, heterojen fetoplasental elemanlar, ekojenik kitle
- İnkomplet abortus uterus boyutu: Uterus beklenen gebelik haftasında veya daha küçük
- İnkomplet abortus tedavisi: Hemodinamik stabilizasyon, medikal (misoprostol) veya cerrahi tahliye (küretaj / vakum)
- Komplet abortus (tam düşük) tanımı: Tüm gebelik materyalinin tamamen uterus dışına atılmış olması
- Komplet abortus klinik ve pelvik muayene: Kanama ve ağrının dramatik azalması, serviks KAPALI OLABİLİR
- Komplet abortus ultrasonografisi: Gebelik materyali gözlenmez, endometrial kavite boş ve ince düzenli çizgi
- Komplet abortus laboratuvar ve tedavi: B-hCG pozitif çıkabilir (yavaşça düşer), TEDAVİ GEREKMEZ kuralı
- Checkpoint 5 (Tekrar ve pekiştirme sayfası)
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

def get_sec5_slides():
    slides = []

    # Slide 41
    slides.append(make_slide(
        slide_num=41,
        title="İnkomplet Abortus: Tanım ve Kısmi Atılım Mekanizması",
        subtitle="Gebelik ürünlerinin bir kısmının dışarı atılması, fetoplasental retansiyon",
        clinical_focus="Uterus kavitesinde kalan artık dokunun yarattığı kanama riski",
        narrative=(
            "Klinik pratikte acil cerrahi veya medikal müdahale gerektiren en sık abortus tablosu inkomplet abortustur.\n\n"
            "- **Resmi Tanım:** Gebelik mahsulünün (embriyo, membranlar ve plasenta) **bir kısmının uterus dışına atıldığı**, ancak geriye kalan parçaların uterus kavitesi içinde tutulduğu durumdur.\n"
            "- **Fizyopatolojik Süreç:** Miyometrium güçlü kasılmalarla gebelik kesesini parçalar ve servikal kanaldan vajinaya doğru iter. Ancak plasental villusların bir kısmı desidua bazalise yapışık kaldığı için tam atılım gerçekleşemez.\n"
            "- **Kanama Mekanizması:** Kavitede kalan plasental doku parçaları miyometriumun düzenli kasılarak spiral arterleri mekanik olarak sıkıştırmasını (fizyolojik ligatür - hemostatik 'canlı ligatür' mekanizması) engeller. Bu nedenle inkomplet abortus durdurulamayan masif vajinal kanamalara yol açabilir.\n\n"
            "> [!IMPORTANT]\n"
            "> İnkomplet abortus: Gebelik ürünlerinin bir kısmının dışarı atıldığı, bir kısmının kavitede kaldığı tablodur; açık serviks ve devam eden kanama ile karakterizedir."
        ),
        bullets=[
            "Gebelik materyalinin bir kısmı dışarı atılmış, bir kısmı içeride kalmıştır",
            "Kavitede kalan fetoplasental artıklar miyometrial kasılmayı ve hemostazı engeller",
            "Miyometriumun tam kasılamaması nedeniyle devam eden yoğun kanama izlenir",
            "Acil servise başvuran kanamalı düşüklerin en sık rastlanan formudur"
        ],
        elements=[
            make_quiz(
                question="Ders notuna göre, gebelik ürünlerinin yalnızca bir kısmının dışarı atıldığı ve kavite içinde doku kalıntılarının bulunduğu klinik abortus tipi hangisidir?",
                options=[
                    {"key": "A", "text": "Komplet abortus", "isCorrect": False, "explanation": "Komplet abortusta tüm materyal atılmıştır."},
                    {"key": "B", "text": "İnkomplet abortus", "isCorrect": True, "explanation": "Doğru. Notta inkomplet abortus: 'Gebelik ürünlerinin bir kısmı dışarı atılmış' olarak tanımlanmıştır."},
                    {"key": "C", "text": "Abortus imminens", "isCorrect": False, "explanation": "İmminenste hiçbir materyal atılmamıştır, serviks kapalıdır."},
                    {"key": "D", "text": "Missed abortus", "isCorrect": False, "explanation": "Missed abortusta canlılığını yitirmiş gebelik tamamen içeride kalmıştır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Gebelik ürünlerinin bir kısmının dışarı atıldığı ve kavitede artıkların kaldığı tablo inkomplet abortus olarak tanımlanır.",
                masked_term="inkomplet abortus",
                hint="Tam olmayan, yarım kalmış düşük anlamına gelen obstetrik terim"
            ),
            make_chain(
                title="İnkomplet Abortusta Devam Eden Kanama Patofizyolojisi",
                steps=[
                    "Kısmi Atılım: Gebelik kesesinin bir bölümünün açılan servikal kanaldan vajinaya dökülmesi",
                    "Doku Retansiyonu: Plasental kotiledonların ve membranların desiduaya yapışık kalarak kavitede tutulması",
                    "Hemostatik Engelleme: Retifiye dokunun miyometrial liflerin tam kasılmasını (ligatür etkisini) bloke etmesi",
                    "Kalıcı Kanama: Açık kalan spiral arterlerden aralıksız aktif vajinal kanama sürmesi"
                ]
            ),
            make_recall(
                question="İnkomplet abortusta vajinal kanamanın komplet abortusa göre çok daha şiddetli ve uzun süreli olmasının temel fizyopatolojik nedeni nedir?",
                answer="Kavitede kalan plasental doku parçalarının miyometriumun tam ve homojen kasılmasını engelleyerek açık spiral arterlerin mekanik olarak kapanmasını (hemostatik ligatürü) bozmasıdır."
            )
        ]
    ))

    # Slide 42
    slides.append(make_slide(
        slide_num=42,
        title="İnkomplet Abortus Klinik ve Muayene: Serviks AÇIK",
        subtitle="Spekulumda plasenta parçaları, açık internal os ve aktif kanama",
        clinical_focus="Pelvik muayenede eksternal ve internal os'ta doku varlığının tespiti",
        narrative=(
            "İnkomplet abortus hastası genellikle evde parça düşürme öyküsü ve devam eden vajinal kanama ile acil servise başvurur.\n\n"
            "- **Servikal Muayene Bulgusu:** Spekulum ve bimanuel tuşede **servikal internal os AÇIKTIR**. Servikal açıklık doku pasajı nedeniyle birkaç santimetreye ulaşmış olabilir.\n"
            "- **Spekulum Bulguları:** Spekulum muayenesinde eksternal servikal os ağzında veya vajen arka forniksinde pıhtılarla karışık **gri-beyaz etsi parçalar (fetoplasental ve plasenta parçaları)** doğrudan gözlenir.\n"
            "- **Klinik Belirtiler:** Kanama miktarı genellikle fazladır; hasta parçalar düşürdüğünü ifade etmesine rağmen kramp tarzı alt karın ağrısı ve kanama kesilmemiştir. Uterin enfeksiyon gelişmemişse palpasyonda uterus hassas olabilir.\n\n"
            "> [!IMPORTANT]\n"
            "> İnkomplet abortusta serviks AÇIKTIR; vajinal kanama devam eder ve muayenede servikal osta plasenta parçaları görülebilir."
        ),
        bullets=[
            "Servikal internal os kesinlikle AÇIKTIR",
            "Vajinal kanama fazladır ve aktif olarak devam eder",
            "Spekulum muayenesinde osta plasenta parçaları doğrudan izlenebilir",
            "Hasta sıklıkla evde pıhtı ve etsi doku parçaları düşürdüğünü ifade eder"
        ],
        elements=[
            make_quiz(
                question="Vajinal kanama ile başvuran bir gebenin spekulum muayenesinde servikal kanalın açık olduğu ve servikal os ağzından dışarı sarkan plasenta parçaları saptanıyor. Bu hastada en olası klinik tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Abortus imminens", "isCorrect": False, "explanation": "İmminenste serviks kapalıdır, doku parçası sarkmaz."},
                    {"key": "B", "text": "Komplet abortus", "isCorrect": False, "explanation": "Komplet abortusta serviks kapalı olabilir ve kavite/os boştur."},
                    {"key": "C", "text": "İnkomplet abortus", "isCorrect": True, "explanation": "Doğru. Açık serviks, devam eden kanama ve osta plasenta parçaları inkomplet abortusun patognomonik muayenesidir."},
                    {"key": "D", "text": "Missed abortus", "isCorrect": False, "explanation": "Missed abortusta serviks kapalıdır ve doku atılımı olmamıştır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="İnkomplet abortus olgularında spekulum muayenesinde servikal kanal açık izlenir ve osta plasenta parçaları saptanabilir.",
                masked_term="plasenta parçaları",
                hint="Kısmi düşükte rahim ağzından sarkan trofoblastik etsi doku kalıntıları"
            ),
            make_table(
                title="İnkomplet Abortus Kardinal Muayene Bulguları",
                headers=["Fizik Muayene Alanı", "Klinik Bulgu", "Patolojik Anlamı"],
                rows=[
                    [
                        {"text": "Servikal Os Durumu", "isMasked": False},
                        {"text": "Kesin olarak açıktır", "isMasked": True, "hint": "Genişlemiş serviks kanalı"},
                        {"text": "Doku pasajının devam ettiğini gösterir", "isMasked": False}
                    ],
                    [
                        {"text": "Vajinal Spekulum İncelemesi", "isMasked": False},
                        {"text": "Kanama ve plasenta parçaları (+)", "isMasked": True, "hint": "Kaviteden sarkan trofoblastik etsi doku kalıntıları"},
                        {"text": "Atılımın tam gerçekleşmediğini belgeler", "isMasked": False}
                    ],
                    [
                        {"text": "Uterus Boyutu", "isMasked": False},
                        {"text": "Gebelik haftasında veya daha küçük", "isMasked": False},
                        {"text": "Kısmi boşalma sonucu hacmin küçülmesidir", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Spekulum muayenesinde servikal kanal ağzına sıkışmış plasental doku parçası görülen bir inkomplet abortus hastasında ilk yapılması gereken mekanik işlem nedir?",
                answer="Servikal osta sıkışan doku parçası bir ring forseps yardımıyla nazikçe çekilerek çıkarılmalı; bu sayede servikal kramp hafifletilmeli ve kanama kontrol altına alınmalıdır."
            )
        ]
    ))

    # Slide 43
    slides.append(make_slide(
        slide_num=43,
        title="İnkomplet Abortus Ultrasonografisi ve Uterus Boyutu",
        subtitle="Kavitede bozulmuş gebelik, heterojen fetoplasental elemanlar",
        clinical_focus="Endometrial kalınlaşma, ekojenik kitle ve gebelik haftasından küçük uterus",
        narrative=(
            "İnkomplet abortusta ultrasonografi tanıyı kesinleştiren ve kavitede kalan artık miktarını gösteren en güvenilir araçtır.\n\n"
            "- **Resmi Ders Notu Ultrason Bulgusu:** Amfi ders notunda inkomplet abortus ultrasonografisi **'Kavitede bozulmuş gebelik, fetoplasental elemanlar'** olarak tanımlanmıştır.\n"
            "- **Ultrasonik Görünüm:** Uterus kavitesi içinde intakt bir gebelik kesesi artık izlenmez; bunun yerine düzensiz sınırlı, heterojen ekojenitede, akustik gölgelenmeler veren kavitary doku birikimi (**retansiyone konseptüs materyali - RPOC**) ve kalınlaşmış endometrial hat (>15 mm) izlenir. Renkli Doppler'de bu dokularda desidual düşük dirençli kan akımları saptanabilir.\n"
            "- **Uterus Boyutu:** Amfi notunda açıkça belirtildiği üzere pelvik muayenede uterus **'gebelik haftasında veya daha küçük'** olarak palpe edilir; çünkü materyalin bir kısmı atılmış ve amniyon sıvısı boşalmıştır.\n\n"
            "> [!NOTE]\n"
            "> İnkomplet abortusta ultrasonda kavitede bozulmuş gebelik ve fetoplasental elemanlar görülür; uterus boyutu gebelik haftasında veya daha küçüktür."
        ),
        bullets=[
            "Ders notuna göre ultrasonda kavitede bozulmuş gebelik ve fetoplasental elemanlar izlenir",
            "Uterus boyutu beklenen gebelik haftasında veya haftasından daha küçüktür",
            "İntakt gebelik kesesi kaybolmuş, yerini heterojen ekojenik doku almıştır",
            "Kavite içi kalınlaşmış endometrial eko ve Doppler akımları retansiyonu belgeler"
        ],
        elements=[
            make_quiz(
                question="Amfi ders notu tablosuna göre inkomplet abortus vakalarında ultrasonografi bulgusu ve uterus boyutu hakkında hangisi KESİNLİKLE DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Ultrasonda gebelik materyali hiç gözlenmez; uterus gebelik haftasından çok büyüktür", "isCorrect": False, "explanation": "Gebelik materyali görülmeyen komplet abortustur."},
                    {"key": "B", "text": "Ultrasonda kavitede bozulmuş gebelik ve fetoplasental elemanlar izlenir; uterus gebelik haftasında veya daha küçüktür", "isCorrect": True, "explanation": "Doğru. Ders notundaki inkomplet abortus satırında ultrason ve uterus boyutu tam olarak böyle tanımlanmıştır."},
                    {"key": "C", "text": "Ultrasonda canlı fetal kalp atımı görülür; uterus gebelik haftasından 4 hafta büyüktür", "isCorrect": False, "explanation": "FKA canlılığı imminenstedir; aşırı büyük uterus mol hidatiformda olur."},
                    {"key": "D", "text": "Ultrasonda boş kavite vardır; uterus tamamen atrofiktir", "isCorrect": False, "explanation": "Kavitede fetoplasental artıklar mevcuttur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnkomplet abortus tablosunda ultrasonografide kavitede bozulmuş gebelik ve fetoplasental elemanlar izlenir.",
                masked_term="fetoplasental elemanlar",
                hint="Ders notunda kavite içinde kaldığı belirtilen doku kalıntıları"
            ),
            make_slider(
                left_title="İnkomplet Abortus Bulgusu",
                right_title="Missed Abortus Bulgusu",
                left_points=[
                    "Kavitede bozulmuş, parçalı fetoplasental doku",
                    "Servikal kanal açık ve vajinal kanama yoğun",
                    "Materyalin bir kısmı dışarı atılmıştır"
                ],
                right_points=[
                    "Kavitede intakt ancak cansız embriyo/kese",
                    "Servikal kanal kapalıdır",
                    "Materyalin hiçbiri henüz atılmamıştır"
                ]
            ),
            make_recall(
                question="İnkomplet abortusta uterus boyutunun beklenen son adet tarihine göre daha küçük olmasının nedeni nedir?",
                answer="Gebelik materyalinin bir kısmının dışarı atılmış olması, amniyon sıvısının tamamen boşalması ve miyometriumun kısmen kasılarak hacmini küçültmesidir."
            )
        ]
    ))

    # Slide 44
    slides.append(make_slide(
        slide_num=44,
        title="İnkomplet Abortus Tedavisi: Tahliye Prensipleri",
        subtitle="Cerrahi tahliye (vakum küretaj) ve medikal yaklaşım seçenekleri",
        clinical_focus="Maternal kanama kontrolü ve enfeksiyonu önlemek için kavitenin arındırılması",
        narrative=(
            "İnkomplet abortus hastasında tedavi geciktirilemez; temel amaç kavitede kalan enfeksiyöz ve kanamalı artıkları hızla temizlemektir.\n\n"
            "- **Cerrahi Tahliye (Vakum Aspirasyon):** Yoğun vajinal kanaması olan, hemoglobin düzeyi düşen veya enfeksiyon şüphesi bulunan hastalarda ilk tercih **vakum aspirasyon (manuel veya elektrikli vakum küretaj)** ile kavitenin boşaltılmasıdır. İşlem keskin küretaja kıyasla uterin perforasyon ve Asherman sendromu riskini çok daha aza indirir.\n"
            "- **Medikal Tedavi (Misoprostol):** Hemodinamik olarak tamamen stabil, kanaması hafif olan seçilmiş olgularda prostaglandin E1 analoğu olan **misoprostol** (oral, sublingual veya vajinal yoldan) uygulanarak uterus kasılmaları tetiklenebilir ve kalan parçaların cerrahisiz atılması denenebilir.\n"
            "- **Profilaksi:** Tüm cerrahi tahliyeler öncesinde profilaktik antibiyoterapi verilmeli ve Rh-negatif annelere Anti-D uygulanmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> İnkomplet abortusta kavitede kalan fetoplasental artıklar cerrahi tahliye (vakum aspirasyon) veya medikal yöntemlerle (misoprostol) tamamen temizlenmelidir."
        ),
        bullets=[
            "Yoğun kanamalı veya anstabil hastalarda ilk seçenek vakum aspirasyondur",
            "Vakum küretaj perforasyon ve Asherman sendromu riskini belirgin azaltır",
            "Hemodinamisi stabil olgularda misoprostol ile medikal tahliye uygulanabilir",
            "Müdahale öncesi profilaktik antibiyotik ve Anti-D immünglobulin şarttır"
        ],
        elements=[
            make_quiz(
                question="Vajinal kanaması devam eden ve ultrasonografisinde kavite içinde geniş fetoplasental doku artıkları (inkomplet abortus) saptanan hemodinamik olarak kanamalı bir hastada en uygun ve güvenli tedavi yöntemi hangisidir?",
                options=[
                    {"key": "A", "text": "Hemen yüksek doz progesteron verilerek kanamanın durması için 1 ay beklenmesi", "isCorrect": False, "explanation": "Progesteron doku artıklarını temizlemez, kanamayı durdurmaz."},
                    {"key": "B", "text": "Acil vakum aspirasyon ile kavitenin cerrahi olarak tahliye edilmesi", "isCorrect": True, "explanation": "Doğru. Kanamalı inkomplet abortusta kavitenin vakum aspirasyon ile hızla boşaltılması hemostazı sağlar."},
                    {"key": "C", "text": "Hastaya tanısal laparoskopi yapılması", "isCorrect": False, "explanation": "Laparoskopi kavite içini temizlemez."},
                    {"key": "D", "text": "Yalnızca yatak istirahati ve demir ilacı verilmesi", "isCorrect": False, "explanation": "İstirahat retansiyone dokuyu boşaltamaz, sepsis riski doğurur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnkomplet abortus olgularında kavite içinde kalan fetoplasental artıkların güvenle boşaltılmasında vakum aspirasyon cerrahisi ilk seçenektir.",
                masked_term="vakum aspirasyon",
                hint="Negatif basınçla dokuları emerek temizleyen modern küretaj tekniği"
            ),
            make_spot_the_lie(
                topic="İnkomplet abortus yönetimi",
                items=[
                    {"text": "İnkomplet abortusta kavitede kalan plasental doku miyometrial kasılmayı engelleyerek masif kanama yapabilir.", "isLie": False, "explanation": "Doğrudur; hemostaz için dokuların tamamen temizlenmesi gerekir."},
                    {"text": "İnkomplet abortus saptandığında hiçbir müdahale yapılmaz, kavitedeki canlı fetüsün büyümesi beklenir.", "isLie": True, "explanation": "Tuzak önerme. İnkomplet abortusta canlı fetüs yoktur; materyal parçalanmış ve kısmen atılmıştır, tahliye şarttır."},
                    {"text": "Cerrahi tahliye öncesinde enfeksiyon profilaksisi ve Rh uygunsuzluğu kontrolü yapılmalıdır.", "isLie": False, "explanation": "Doğrudur; standart obstetrik güvenlik protokolüdür."}
                ]
            ),
            make_recall(
                question="Neden inkomplet abortus cerrahi tahliyesinde klasik keskin metal küret yerine vakum aspiratör kanülleri tercih edilir?",
                answer="Vakum aspirasyon işlemi daha hızlıdır, daha az ağrılıdır, kan kaybı daha düşüktür; en önemlisi myometrium perforasyonu ve ileride Asherman sendromuna (sineşi) yol açma riski belirgin derecede daha düşüktür."
            )
        ]
    ))

    # Slide 45
    slides.append(make_slide(
        slide_num=45,
        title="Komplet Abortus (Tam Düşük): Tanım ve Klinik Tablo",
        subtitle="Tüm gebelik materyalinin dışarı atılması, semptomların dramatik hafiflemesi",
        clinical_focus="Spontan tam tahliyenin klinik semptomları ve tanınması",
        narrative=(
            "Spontan düşük sürecinin fizyolojik olarak başarıyla tamamlandığı evre komplet abortustur.\n\n"
            "- **Resmi Tanım:** Gebelik mahsulünün (embriyo, amniyon zarları ve plasenta) **tamamının uterus kavitesi dışına atıldığı** durumdur.\n"
            "- **Klinik Öykü ve Anamnez:** Hasta hekime tipik olarak 'Yoğun bir kasık ağrısı ve kanama sonrası vajinamdan etsi, yuvarlak bir kese şeklinde et parçası düştü' şeklinde net bir öykü ile gelir.\n"
            "- **Semptomların Gerilemesi:** Düşük materyalinin tamamı atıldığı anda kavite boşalır. Miyometrium hızla tam ve güçlü şekilde kasılır, spiral arterleri sıkar ve hastanın şiddetli kasık ağrısı ile yoğun vajinal kanaması **dramatik şekilde bıçak gibi kesilir** veya hafif bir lekelenmeye dönüşür.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet abortus: Tüm gebelik materyalinin atıldığı durumdur; hasta parça veya tüm materyali düşürdüğünü söyler, kanama ve ağrı hızla azalır."
        ),
        bullets=[
            "Tüm gebelik materyali (fetüs ve plasenta) tamamen dışarı atılmıştır",
            "Hasta etsi bir parça veya tam bir kese düşürdüğünü net olarak tarifler",
            "Materyalin atılmasıyla şiddetli kasık ağrısı ve kanama hızla geriler",
            "Uterusun tam kasılması hemostazı kendiliğinden sağlar"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki tanımlara göre, tüm gebelik materyalinin dışarı atıldığı ve hastanın parça veya tüm materyali düşürdüğünü ifade ettiği klinik abortus tipi hangisidir?",
                options=[
                    {"key": "A", "text": "Abortus insipiens", "isCorrect": False, "explanation": "İnsipienste materyal henüz atılmamıştır."},
                    {"key": "B", "text": "İnkomplet abortus", "isCorrect": False, "explanation": "İnkomplet abortusta materyalin yalnızca bir kısmı atılmıştır."},
                    {"key": "C", "text": "Komplet abortus (tam düşük)", "isCorrect": True, "explanation": "Doğru. Ders notunda komplet abortus: 'Tüm gebelik materyali atılmış; hasta parça veya tüm materyali düşürdüğünü söyler' şeklinde tanımlanmıştır."},
                    {"key": "D", "text": "Abortus imminens", "isCorrect": False, "explanation": "İmminenste hiçbir doku atılmamıştır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Tüm gebelik materyalinin uterus dışına atıldığı ve kanamanın hızla dindiği durum komplet abortus olarak adlandırılır.",
                masked_term="komplet abortus",
                hint="Tam düşük anlamına gelen Latince obstetrik terim"
            ),
            make_slider(
                left_title="İnkomplet Abortus Kliniği",
                right_title="Komplet Abortus Kliniği",
                left_points=[
                    "Materyalin bir kısmı içeride kalmıştır",
                    "Kramp ve şiddetli kanama aktif devam eder",
                    "Miyometrium tam kasılamaz ve açık arterler kanar"
                ],
                right_points=[
                    "Tüm fetal ve plasental materyal atılmıştır",
                    "Ağrı ve kanama dramatik şekilde azalır/kesilir",
                    "Miyometrium sıkıca kasılarak hemostazı sağlar"
                ]
            ),
            make_recall(
                question="Komplet abortusta hastanın materyali düşürdükten hemen sonra kasık ağrısının ve kanamasının aniden kesilmesinin mekanizması nedir?",
                answer="Kavitenin tamamen boşalmasıyla miyometrial düz kas liflerinin homojen ve güçlü şekilde kasılarak spiral damarları bir ligatür gibi sıkıştırması ve hemostazı sağlamasıdır."
            )
        ]
    ))

    # Slide 46
    slides.append(make_slide(
        slide_num=46,
        title="Komplet Abortus Muayene Bulgusu: Serviks Kapalı Olabilir",
        subtitle="Spekulum ve tuşede regrese servikal kanal ve kanama azlığı",
        clinical_focus="Materyal atılımı sonrası servikal internal os'un hızla kapanması",
        narrative=(
            "Komplet abortusta pelvik muayene bulguları materyalin atıldığı andan itibaren geçen süreye göre şekillenir.\n\n"
            "- **Resmi Ders Notu Muayene Bulgusu:** Amfi ders notunda komplet abortus için servikal durum **'Kapalı olabilir'** şeklinde net olarak belirtilmiştir.\n"
            "- **Servikal Dinamik:** Gebelik ürününün tamamı servikal kanaldan geçip dışarı atıldıktan sonra, uterin kasılmaların da etkisiyle servikal internal ve eksternal os hızla toparlanır ve kapanır. Hasta acile ulaştığında serviks genellikle kapanmıştır veya kapanma sürecindedir.\n"
            "- **Spekulum İncelemesi:** Vajinada aktif fışkırır tarzda kanama yoktur; servikal ostan sadece minimal seröz veya kahverengi bir sızıntı izlenir. Vajinal fornikste daha önce düşürülmüş doku kalıntıları bazen saptanabilir.\n"
            "- **Uterus Boyutu:** Bimanuel muayenede uterus tamamen küçülmüş, boşalmış ve neredeyse gebe olmayan boyutlara yakın sert bir kitle olarak palpe edilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet abortusta serviks KAPALI OLABİLİR; kavite boşalmış ve kanama belirgin şekilde azalmıştır."
        ),
        bullets=[
            "Ders notuna göre komplet abortusta serviks KAPALI OLABİLİR",
            "Materyalin geçişinden sonra servikal internal os hızla kontrakte olup kapanır",
            "Spekulumda aktif yoğun kanama izlenmez, minimal sızıntı olabilir",
            "Bimanuel muayenede uterus küçülmüş, sert ve non-gebe boyutuna yakındır"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki sınıflama tablosuna göre, komplet abortus (tam düşük) vakalarında servikal kanalın muayene bulgusu hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "Daima 5 cm açık ve gergindir", "isCorrect": False, "explanation": "Materyal atıldıktan sonra serviks açık kalmaz."},
                    {"key": "B", "text": "Yalnızca cerrahi dikişle kapatılabilir", "isCorrect": False, "explanation": "Fizyolojik olarak miyometrial kontraksiyonla kendisi kapanır."},
                    {"key": "C", "text": "Karsinom nedeniyle tamamen fiksedir", "isCorrect": False, "explanation": "Malignite ilişkisi yoktur."},
                    {"key": "D", "text": "Kapalı olabilir", "isCorrect": True, "explanation": "Doğru. Ders notu tablosunda komplet abortus serviks sütunu 'Kapalı olabilir' olarak belirtilmiştir."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Ders notuna göre komplet abortus tablosunda tüm materyalin atılmasını takiben serviks muayenede kapalı olabilir.",
                masked_term="kapalı olabilir",
                hint="Ders notundaki tablodan birebir alıntı: serviksin komplet düşükteki durumu"
            ),
            make_table(
                title="Abortus Tiplerinde Servikal Durum Özeti",
                headers=["Abortus Tipi", "Serviks Muayenesi", "Kavite İçeriği"],
                rows=[
                    [
                        {"text": "Abortus İmminens", "isMasked": False},
                        {"text": "Kesinlikle kapalı", "isMasked": False},
                        {"text": "Canlı embriyo mevcuttur", "isMasked": True, "hint": "FKA pozitifliği"}
                    ],
                    [
                        {"text": "Abortus İnsipiens", "isMasked": False},
                        {"text": "Kesinlikle açık", "isMasked": True, "hint": "Açılmış servikal kanal"},
                        {"text": "Gebelik kavitede henüz atılmamış", "isMasked": False}
                    ],
                    [
                        {"text": "İnkomplet Abortus", "isMasked": False},
                        {"text": "Kesinlikle açık", "isMasked": False},
                        {"text": "Fetoplasental artıklar mevcuttur", "isMasked": True, "hint": "Kısmi retansiyon durumu"}
                    ],
                    [
                        {"text": "Komplet Abortus", "isMasked": False},
                        {"text": "Kapalı olabilir", "isMasked": True, "hint": "Atılım sonrası toparlanan kanal durumu"},
                        {"text": "Gebelik materyali gözlenmez (boş)", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Neden komplet abortusta serviks muayenesinde 'açıktır' yerine 'kapalı olabilir' ifadesi kullanılır?",
                answer="Çünkü materyal yeni atılmışsa serviks henüz tam kapanmamış olabilir; ancak atılım tamamlandıktan kısa süre sonra miyometrium kasılarak servikal kanalı hızla kapattığı için hasta muayene edildiğinde serviks çoğunlukla kapalı bulunur."
            )
        ]
    ))

    # Slide 47
    slides.append(make_slide(
        slide_num=47,
        title="Komplet Abortus Ultrasonografisi: Boş Uterus Kavitesi",
        subtitle="Gebelik materyali gözlenmez, ince endometrial hat",
        clinical_focus="Ektopik gebelik şüphesi ile boş kavite arasındaki ayırıcı tanı",
        narrative=(
            "Komplet abortus tanısının kesinleşmesi ve hastanın cerrahi küretajdan kurtulması ultrasonografi bulgusuna bağlıdır.\n\n"
            "- **Resmi Ders Notu Ultrason Bulgusu:** Amfi ders notunda komplet abortus için ultrasonografi bulgusu **'Gebelik materyali gözlenmez'** şeklinde kaydedilmiştir.\n"
            "- **Ultrasonik Görüntüleme:** Transvajinal ultrasonografide uterus kavitesi içinde hiçbir gestasyonel kese, yolk kesesi veya kavitary heterojen fetoplasental doku izlenmez. Endometrial kavite düzgün sınırlı, ince bir çizgi halinde (<8-10 mm) ve boştur.\n"
            "- **Ektopik Gebelik Uyarısı (KRİTİK AYIRICI TANI):** Eğer hastada daha önce ultrasonla intrauterin bir gebelik kesesi belgelenmemişse; ultrasonda uterusun 'boş' görülmesi komplet abortus olabileceği gibi **ektopik gebelik (dış gebelik)** de olabilir! Bu nedenle adneksler dikkatle taranmalı ve seri serum hCG takibi yapılmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet abortusta ultrasonda gebelik materyali gözlenmez; ancak ektopik gebeliğin ekarte edilmesi için seri hCG ve adneks muayenesi şarttır."
        ),
        bullets=[
            "Ders notuna göre ultrasonda gebelik materyali gözlenmez",
            "Endometrial kavite ince, düzenli ve tamamen boş olarak izlenir",
            "Önceden intrauterin kese görülmemişse ektopik gebelik mutlaka dışlanmalıdır",
            "Kavitede doku kalıntısı olmaması hastayı gereksiz cerrahiden korur"
        ],
        elements=[
            make_quiz(
                question="Ders notu tablosuna göre komplet abortus (tam düşük) vakalarında yapılan ultrasonografide beklenen temel bulgu hangisidir?",
                options=[
                    {"key": "A", "text": "Gebelik materyali gözlenmez (kavite boştur)", "isCorrect": True, "explanation": "Doğru. Ders notu tablosunda komplet abortus USG bulgusu doğrudan 'Gebelik materyali gözlenmez' olarak tanımlanmıştır."},
                    {"key": "B", "text": "Kavitede bozulmuş gebelik ve fetoplasental elemanlar", "isCorrect": False, "explanation": "Bu inkomplet abortus bulgusudur."},
                    {"key": "C", "text": "Kavitede canlı embriyo ve pozitif kalp atımı", "isCorrect": False, "explanation": "Bu abortus imminens bulgusudur."},
                    {"key": "D", "text": "Uterus içinde yaygın veziküler ekojenite", "isCorrect": False, "explanation": "Bu mol hidatiform bulgusudur."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Komplet abortus tablosunda transvajinal ultrasonografi yapıldığında kavite içinde gebelik materyali gözlenmez.",
                masked_term="gebelik materyali gözlenmez",
                hint="Ders notunda komplet abortusun ultrason sütununda yazan resmi ifade"
            ),
            make_slider(
                left_title="Komplet Abortus Ultrasonu",
                right_title="İnkomplet Abortus Ultrasonu",
                left_points=[
                    "Gebelik materyali gözlenmez",
                    "Endometrial hat ince ve düzenlidir (<8-10 mm)",
                    "Kavite içinde retansiyone parça veya ekojenite yoktur"
                ],
                right_points=[
                    "Kavitede bozulmuş gebelik ve fetoplasental elemanlar",
                    "Endometrial hat kalın, düzensiz ve heterojendir (>15 mm)",
                    "Kavite içinde akustik gölgelenmeli ekojen dokular izlenir"
                ]
            ),
            make_recall(
                question="Daha önce hiç ultrason yapılmamış kanamalı bir kadında ultrasonda uterusun tamamen 'boş' izlenmesi komplet abortus dışında hangi hayati patolojiyi düşündürmelidir?",
                answer="Ektopik gebeliği (dış gebelik) düşündürmelidir; tubal yerleşimli bir gebelik nedeniyle uterus kavitesi boş olabilir, bu nedenle adneksler taranmalı ve serum hCG düzeyleri izlenmelidir."
            )
        ]
    ))

    # Slide 48
    slides.append(make_slide(
        slide_num=48,
        title="Komplet Abortusta Laboratuvar: B-hCG Dinamikleri",
        subtitle="B-hCG pozitif çıkabilir ancak hızla düşme eğilimindedir",
        clinical_focus="Kanda trofoblastik hormon klirensi ve canlı gebelikten ayrım",
        narrative=(
            "Komplet abortus geçiren bir kadında gebelik testinin durumu hastalar ve genç hekimler tarafından sıklıkla yanlış yorumlanabilir.\n\n"
            "- **Resmi Ders Notu Bulgusu:** Amfi ders notunda komplet abortus tablosunda **'B-HCG + çıkabilir'** uyarısı açıkça yapılmıştır.\n"
            "- **Biyolojik Mekanizma:** Gebelik materyali tamamen atılmış olsa dahi, daha önce maternal dolaşıma salınmış olan beta-hCG hormonunun yarı ömrü yaklaşık **24-36 saattir**. Bu nedenle tam düşükten sonraki birkaç gün boyunca kanda ve idrarda beta-hCG pozitifliği devam eder.\n"
            "- **Klinik İzlem:** Kritik nokta hormonun mutlak değeri değil, trendidir. Canlı intrauterin gebelikte hCG her 48 saatte en az %50-66 artarken, komplet abortusta 48 saat arayla bakılan serum beta-hCG seviyesi **%50'den fazla dramatik bir düşüş** gösterir. Seviye sıfırlanana kadar haftalık takip önerilebilir.\n\n"
            "> [!NOTE]\n"
            "> Komplet abortusta tüm doku atılmış olsa bile B-hCG kanda bir süre daha pozitif kalabilir; tanı için düzeyin hızla düşmesi beklenir."
        ),
        bullets=[
            "Ders notuna göre komplet abortusta B-HCG pozitif (+) çıkabilir",
            "Dolaşımdaki hCG'nin yarı ömrü nedeniyle kanda klirensi birkaç gün/hafta sürer",
            "Seri ölçümlerde beta-hCG'nin 48 saatte hızla düşmesi komplet atılımı doğrular",
            "Hormon düzeyinin plato çizmesi veya artması rezidü doku veya ektopik gebelik alarmıdır"
        ],
        elements=[
            make_quiz(
                question="Tüm gebelik materyalini düşüren ve ultrasonunda kavitesi tamamen boş izlenen (komplet abortus) bir hastada yapılan kanda gebelik testinin (B-hCG) durumu hakkında hangisi amfi ders notuna göre doğrudur?",
                options=[
                    {"key": "A", "text": "Materyal atıldığı saniyede B-hCG kesinlikle sıfıra iner ve negatifleşir", "isCorrect": False, "explanation": "Hormonun yarı ömrü nedeniyle hemen sıfırlanmaz."},
                    {"key": "B", "text": "B-HCG pozitif çıkabilir", "isCorrect": True, "explanation": "Doğru. Ders notu açıkça 'B-HCG + çıkabilir' notunu düşmüştür; dolaşımdaki hormon zamanla temizlenir."},
                    {"key": "C", "text": "B-hCG her 48 saatte iki katına katlanarak artar", "isCorrect": False, "explanation": "Bu canlı intrauterin gebelik paterndir, düşükte düşer."},
                    {"key": "D", "text": "B-hCG yalnızca beyin omurilik sıvısında saptanır", "isCorrect": False, "explanation": "Kanda ve idrarda saptanır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Ders notunda komplet abortus vakalarında tüm materyal atılmış olsa dahi dolaşımdaki klirens nedeniyle B-HCG pozitif çıkabilir.",
                masked_term="B-HCG pozitif",
                hint="Ders notunda komplet abortus satırında belirtilen kanda hormon testi sonucu"
            ),
            make_chain(
                title="Komplet Abortus Sonrası hCG Düşüş Dinamiği",
                steps=[
                    "Tam Atılım: Fetoplasental dokunun uterus dışına atılması ve trofoblastik hormon üretiminin durması",
                    "Dolaşımdaki Yarı Ömür: Kanda mevcut hCG moleküllerinin karaciğer ve böbrek yoluyla kademeli klirensi (yarı ömür ~24-36 saat)",
                    "Test Pozitifliği: İlk günlerde yapılan kalitatif veya kantitatif testlerde B-hCG'nin pozitif saptanması",
                    "Hormonal Sıfırlanma: 48 saatlik aralıklı kontrollerde hCG'nin hızla düşerek 1-2 hafta içinde sıfıra ulaşması"
                ]
            ),
            make_recall(
                question="Komplet abortus şüphesi olan bir kadında 48 saat arayla bakılan serum beta-hCG düzeyleri düşmek yerine yükseliyorsa ne düşünülmelidir?",
                answer="Tanı komplet abortus olamaz; kavitede canlı kalan rezidü doku (inkomplet abortus), ektopik gebelik veya trofoblastik bir hastalık düşünülerek acil ileri tetkik yapılmalıdır."
            )
        ]
    ))

    # Slide 49
    slides.append(make_slide(
        slide_num=49,
        title="Komplet Abortus Tedavisi: 'TEDAVİ GEREKMEZ' İlkesi",
        subtitle="Fizyolojik hemostaz, gereksiz küretajdan kaçınma ve Anti-D profilaksisi",
        clinical_focus="Tüm dokuları atılmış hastaya cerrahi müdahale yapmama kuralı",
        narrative=(
            "Obstetrik amfi sınavlarında ve klinik pratikte en çok sorulan ve altı çizilen altın kurallardan biri komplet abortusun tedavisidir.\n\n"
            "- **Resmi Ders Notu Kuralı:** Amfi ders notundaki abortus tipleri tablosunda komplet abortus için tedavi sütununda büyük harflerle **'TEDAVİ GEREKMEZ'** yazmaktadır.\n"
            "- **Gerekçesi:** Uterus boşalmış, miyometrium tamamen kasılmış ve hemostaz sağlanmıştır. Bu aşamada hastaya küretaj yapmak uterus perforasyonu, enfeksiyon ve Asherman sendromu (yapışıklık) riskinden başka hiçbir fayda sağlamaz.\n"
            "- **İstisna / Profilaksi:** Her ne kadar medikal veya cerrahi bir boşaltma tedavisi gerekmese de; eğer anne kan grubu **Rh-negatif** ise fetomaternal kanamaya bağlı alloimmünizasyonu önlemek amacıyla **Anti-D immünglobulin** uygulaması mutlak şarttır.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet abortusta tedavi gerekmez; kavite boştur ve kanama durmuştur. Gereksiz küretaj kontrendikedir."
        ),
        bullets=[
            "Ders notuna göre komplet abortusta TEDAVİ GEREKMEZ",
            "Miyometrium doğal olarak kasılmış ve hemostazı sağlamıştır",
            "Gereksiz küretaj yapmak Asherman sendromu ve perforasyon riski doğurur",
            "Rh-negatif annelere Anti-D immünglobulin yapılması unutulmamalıdır"
        ],
        elements=[
            make_quiz(
                question="Ders notundaki resmi tabloya göre komplet abortus (tam düşük) tanısı kesinleşen bir hastanın tedavi yaklaşımı hangisinde doğru olarak belirtilmiştir?",
                options=[
                    {"key": "A", "text": "Acil keskin küretaj ile kavitenin kazınması", "isCorrect": False, "explanation": "Kavite zaten boştur, kazıma Asherman sendromu yapar."},
                    {"key": "B", "text": "Yüksek doz intravenöz oksitosin infüzyonu", "isCorrect": False, "explanation": "Uterus zaten boşalmış ve kasılmıştır."},
                    {"key": "C", "text": "Tedavi gerekmez", "isCorrect": True, "explanation": "Doğru. Ders notu tablosunda komplet abortusun tedavi sütununda doğrudan 'Tedavi gerekmez' yazmaktadır."},
                    {"key": "D", "text": "Radyoterapi uygulanması", "isCorrect": False, "explanation": "Kanser tedavisi değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notu tablosunda komplet abortus vakalarında kavitenin boş olması nedeniyle tedavi gerekmez şeklinde belirtilmiştir.",
                masked_term="tedavi gerekmez",
                hint="Ders notundaki tablodan alıntı: komplet düşükte hiçbir medikal veya cerrahi müdahale ihtiyacının olmaması kuralı"
            ),
            make_spot_the_lie(
                topic="Komplet abortus tedavisi",
                items=[
                    {"text": "Komplet abortus tanısı kesinleştiğinde rutin cerrahi veya medikal tedavi gerekmez.", "isLie": False, "explanation": "Doğrudur; nottaki tedavi kuralı 'Tedavi gerekmez'dir."},
                    {"text": "Komplet abortus yapan her hastaya kavite tamamen boş olsa dahi rutin olarak genel anestezi altında küretaj yapılmalıdır.", "isLie": True, "explanation": "Tuzak önerme. Boş kaviteye küretaj yapmak perforasyon ve Asherman sendromu riski yaratır; kontrendikedir."},
                    {"text": "Komplet abortus geçiren Rh-negatif kadınlara Anti-D immünglobulin profilaksisi uygulanmalıdır.", "isLie": False, "explanation": "Doğrudur; alloimmünizasyon önlenmelidir."}
                ]
            ),
            make_recall(
                question="Komplet abortusta neden 'tedavi gerekmez' kuralı geçerlidir ve küretaj yapmaktan kaçınılır?",
                answer="Çünkü tüm fetoplasental dokular dışarı atılmış, kavite boşalmış ve miyometrium doğal olarak kasılarak kanamayı durdurmuştur; gereksiz bir küretaj hastaya fayda sağlamayacağı gibi uterus perforasyonu ve Asherman sendromu riski yaratır."
            )
        ]
    ))

    # Slide 50 (Checkpoint 5)
    slides.append(make_slide(
        slide_num=50,
        title="[TEKRAR SAYFASI - CHECKPOINT 5] Abortus Tipleri 2: İnkomplet vs Komplet",
        subtitle="Kısmi vs tam atılım, servikal durum, ultrason ve tedavi farkları",
        clinical_focus="İnkomplet ve komplet abortus ayrımının eksiksiz karşılaştırmalı entegrasyonu",
        narrative=(
            "Bu tekrar sayfası, 41-49. adımlarda incelenen İnkomplet Abortus ile Komplet Abortus arasındaki kritik klinik zıtlıkları özetler.\n\n"
            "- **İnkomplet Abortus:** Gebelik ürünlerinin **bir kısmı dışarı atılmış**, bir kısmı içeride kalmıştır. **Serviks AÇIKTIR**. Kanama fazladır; bazen osta plasenta parçaları izlenir. Ultrasonda **kavitede bozulmuş gebelik ve fetoplasental elemanlar** görülür. Uterus gebelik haftasında veya daha küçüktür. Tedavisi cerrahi (vakum aspirasyon) veya medikal tahliyedir.\n"
            "- **Komplet Abortus:** **Tüm gebelik materyali atılmıştır**; hasta parça/tüm materyali düşürdüğünü söyler. **Serviks KAPALI OLABİLİR**. Ultrasonda **gebelik materyali gözlenmez (kavite boştur)**. B-hCG pozitif çıkabilir. **TEDAVİ GEREKMEZ**.\n"
            "- **Klinik Ayrım:** İnkomplet abortusta açık serviks ve kavitede artık varken; komplet abortusta kavite boştur, serviks toparlanmıştır ve müdahale yapılmaz.\n\n"
            "> [!IMPORTANT]\n"
            "> İnkomplet: Bir kısmı atılmış, serviks AÇIK, kavitede artık var, tahliye gerekir | Komplet: Tüm materyal atılmış, serviks KAPALI OLABİLİR, kavite boş, TEDAVİ GEREKMEZ."
        ),
        bullets=[
            "İnkomplet: Kısmi atılım, serviks AÇIK, kavitede fetoplasental artıklar, tahliye şart",
            "Komplet: Tam atılım, serviks KAPALI OLABİLİR, kavite tamamen boş, TEDAVİ GEREKMEZ",
            "Komplet abortusta kanda B-hCG bir süre daha pozitif kalabilir",
            "Her iki tabloda da Rh-negatif hastalara Anti-D profilaksisi uygulanmalıdır"
        ],
        elements=[
            make_quiz(
                question="İnkomplet abortus ile komplet abortus arasındaki temel farkları özetleyen aşağıdaki ifadelerden hangisi amfi ders notuna göre KESİNLİKLE DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "İnkomplet abortusta tüm materyal atılmıştır ve tedavi gerekmez; komplet abortusta ise cerrahi tahliye şarttır.", "isCorrect": False, "explanation": "Tam tersidir; komplet abortusta tedavi gerekmez, inkomplet abortusta tahliye gerekir."},
                    {"key": "B", "text": "İnkomplet abortusta serviks açıktır ve kavitede fetoplasental artıklar vardır; komplet abortusta tüm materyal atılmıştır ve tedavi gerekmez.", "isCorrect": True, "explanation": "Doğru. Notun en önemli 'ÖNEMLİ' vurgu kutusunu eksiksiz özetleyen doğrudur."},
                    {"key": "C", "text": "Her iki tabloda da ultrasonda canlı embriyo ve pozitif kalp atımı izlenir.", "isCorrect": False, "explanation": "Canlı embriyo abortus imminenstedir."},
                    {"key": "D", "text": "Komplet abortusta serviks daima 10 cm açık kalır.", "isCorrect": False, "explanation": "Komplet abortusta serviks kapalı olabilir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnkomplet abortusta serviks açık ve kavitede artık varken komplet abortusta tüm materyal atılmıştır ve tedavi gerekmez.",
                masked_term="tedavi gerekmez",
                hint="Ders notunda komplet abortus için vurgulanan resmi yaklaşım"
            ),
            make_table(
                title="İnkomplet vs Komplet Abortus Karşılaştırma Matrisi (Checkpoint 5)",
                headers=["Klinik Kriter", "İnkomplet Abortus", "Komplet Abortus"],
                rows=[
                    [
                        {"text": "Materyalin Atılma Derecesi", "isMasked": False},
                        {"text": "Bir kısmı dışarı atılmış", "isMasked": True, "hint": "Parçalı doku tahliyesi hali"},
                        {"text": "Tüm gebelik materyali atılmış", "isMasked": True, "hint": "Eksiksiz doku kaybı hali"}
                    ],
                    [
                        {"text": "Servikal Kanal Durumu", "isMasked": False},
                        {"text": "Kesinlikle açık", "isMasked": False},
                        {"text": "Kapalı olabilir", "isMasked": True, "hint": "Atılım sonrası toparlanan kanal durumu"}
                    ],
                    [
                        {"text": "Ultrasonografi Bulgusu", "isMasked": False},
                        {"text": "Kavitede bozulmuş gebelik, fetoplasental elemanlar", "isMasked": False},
                        {"text": "Gebelik materyali gözlenmez", "isMasked": True, "hint": "Boş kavite görüntüsü"}
                    ],
                    [
                        {"text": "Tedavi Yaklaşımı", "isMasked": False},
                        {"text": "Cerrahi / medikal tahliye", "isMasked": False},
                        {"text": "Tedavi gerekmez", "isMasked": True, "hint": "Resmi kural: müdahale ihtiyacı olmaması"}
                    ]
                ]
            ),
            make_branching(
                scenario="Acil servise 9 haftalık gebe bir kadın şiddetli kanama ve parça düşürme şikayeti ile getiriliyor. Yapılan muayene ve USG sonucuna göre tedavi seçilecektir.",
                options=[
                    {
                        "text": "Serviks açık, kanama aktif devam ediyor ve ultrasonda kavitede heterojen fetoplasental artıklar varsa inkomplet abortus tanısıyla vakum aspirasyon planlanır.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. İnkomplet abortusta kavitedeki artıkların acil tahliyesi hemostazı sağlar."
                    },
                    {
                        "text": "Serviks kapalı, kanama durmuş ve ultrasonda kavite tamamen boşsa hemen acil küretaj ile kavite kazınmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Komplet abortusta kavite boşsa tedavi gerekmez; küretaj yapmak perforasyon ve yapışıklık riski yaratır."
                    },
                    {
                        "text": "İnkomplet abortus saptanan hastaya canlı embriyo bekleniyor denilerek eve gönderilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış. İnkomplet abortus geri döndürülemez bir kayıptır, evde kanama şoku riski doğurur."
                    }
                ]
            ),
            make_recall(
                question="Bölüm 5'in en kritik klinik spotu olan 'İnkomplet abortus ile Komplet abortus arasındaki temel farklar' nelerdir?",
                answer="İnkomplet abortusta gebelik materyalinin bir kısmı atılmıştır, serviks açıktır, kavitede artıklar vardır ve cerrahi/medikal tahliye gerekir; komplet abortusta ise tüm materyal atılmıştır, serviks kapalı olabilir, kavitede materyal gözlenmez ve tedavi gerekmez."
            )
        ]
    ))

    return slides
