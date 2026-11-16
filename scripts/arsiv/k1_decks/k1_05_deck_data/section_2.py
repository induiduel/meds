"""
Bölüm 2: Enzimatik Yağ Nekrozu, Akut Pankreatit ve Sabunlaşma Mekanizması
Adımlar: 11 - 20
Checkpoint: Adım 19 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # ADIM 11
    slides.append({
        "slideNumber": 11,
        "title": "Yağ Nekrozu: Yağ Dokusunun Enzimatik ve Travmatik Yıkımı",
        "subtitle": "Lipid dokusunda fokal yıkım alanları ve kalsiyum tuzlarının çökelmesi",
        "badge": "Yağ Nekrozu",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Yağ nekrozu, aslında spesifik bir hücre ölümü tipinden ziyade, yağ dokusunda meydana gelen "
            "fokal hücresel yıkım alanlarını ve ardından gelişen kalsiyum sabunlaşmasını tanımlayan morfolojik bir terimdir. "
            "Klinik patolojide başlıca iki ayrı patolojik senaryoda gözlenir: Akut pankreatite bağlı enzimatik yıkım "
            "veya memede/subkutan dokuda fiziksel travmaya bağlı mekanik hasar.\n\n"
            "> [SINAV SPOTU] Yağ nekrozunun en sık ve en dramatik görüldüğü klinik tablo 'Akut Pankreatit'tir; "
            "burada aktive olan pankreatik enzimler peripankreatik ve omental yağ dokusunu eritir.\n\n"
            "Normal yağ hücreleri (adipositler) sitoplazmalarında büyük bir trigliserit damlası barındırır. "
            "Hücre zarı hasar gördüğünde veya lipazlarla karşılaşıldığında, bu hidrofobik trigliseritler parçalanarak "
            "serbest yağ asitlerine ayrışır ve ortamdaki katyonları bağlayıcı hale gelir."
        ),
        "medicalTerms": [
            {"term": "Yağ Nekrozu", "explanation": "Yağ dokusunda lipaz enzimleri veya travma sonucu trigliseritlerin hidrolizi ve kalsiyumla sabunlaşmasıyla oluşan lezyon."},
            {"term": "Akut Pankreatit", "explanation": "Pankreas asiner hücrelerinin hasarı ve proenzimlerin erken aktivasyonuyla gelişen akut parankim ve peripankreatik yağ oto-sindirimi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yağ nekrozu başlıca akut pankreatitte ve travmaya uğramış yağ dokusunda (meme) görülür.",
            "📌 [SINAV SPOTU] Ayırt edici temel patolojik olay yağ asitlerinin kalsiyum ile birleşmesidir (sabunlaşma)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Klinik Eşleşme", "desc": "Akut pankreatit ve travmatik meme hasarı ana örneklerdir.", "isKey": True},
                {"title": "Biyokimyasal Özellik", "desc": "Trigliseritlerin parçalanıp kalsiyum bağlayıcı serbest asitlere dönüşmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Yağ nekrozunun patolojideki en dramatik ve ölümcül klinik örneği akut pankreatit tablosudur.",
                "akut pankreatit",
                "Pankreas enzimlerinin aktive olarak çevre dokuyu sindirdiği akut kriz"
            ),
            make_active_recall(
                "Yağ nekrozu hangi iki temel klinik durumda ortaya çıkar?",
                "1) Akut pankreatitte (enzimatik yağ nekrozu) ve 2) Travmaya uğramış meme/subkutan yağ dokusunda (travmatik yağ nekrozu)."
            )
        ]
    })

    # ADIM 12
    slides.append({
        "slideNumber": 12,
        "title": "Akut Pankreatitte Yağ Nekrozu Patogenezi: Asiner Enzim Sızıntısı",
        "subtitle": "Aktive olan tripsinojen, lipaz ve fosfolipazların peri-pankreatik dokuya hücumu",
        "badge": "Patogenez",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Akut pankreatitin merkezinde, pankreas asiner hücrelerinde proenzimlerin henüz pankreas kanallarına "
            "ulaşmadan hücre içinde erken aktive olması yatar. Safra taşlarının ampulla Vateri tıkaması veya "
            "alkol toksisitesi sonucu duktusta basınç artar ve intraselüler kalsiyum kaskadı tripsinojeni tripsine çevirir.\n\n"
            "Aktif tripsin diğer proenzimleri (elastaz, fosfolipaz A2) tetikleyerek asiner hücre zarlarını deler. "
            "Böylece pankreatik lipazlar peripankreatik yağ dokusuna, omentum majusa ve mezenter yataklarına sızar.\n\n"
            "> [KRİTİK UYARI] Pankreatik lipazlar adiposit membranını geçerek hücre içi trigliseritleri hidrolize eder; "
            "açığa çıkan serbest yağ asitleri hidroksil ve karboksil uçlarıyla kalsiyumu mıknatıs gibi çeker.\n\n"
            "Bu süreç lokal doku hasarıyla sınırlı kalmayıp retroperitoneal kanamalara ve sistemik şoka kadar ilerleyebilir."
        ),
        "medicalTerms": [
            {"term": "Tripsinojen", "explanation": "Pankreas tarafından üretilen ve tripsine dönüşerek diğer tüm sindirim enzimlerini aktive eden ana zimojen."},
            {"term": "Pankreatik Lipaz", "explanation": "Trigliserit ester bağlarını yıkarak gliserol ve serbest yağ asitlerine ayıran enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut pankreatitte asiner hücrelerden sızan aktif lipazlar trigliseritleri hidrolize eder.",
            "📌 [SINAV SPOTU] Açığa çıkan serbest yağ asitleri kalsiyum ile reaksiyona girer."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Zimojen Aktivasyonu", "desc": "Asiner hücrede tripsinojenin erken tripsine dönüşmesi.", "isKey": True},
                {"title": "Enzimatik Sızıntı", "desc": "Lipazların peripankreatik ve omental yağ dokusuna taşması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Akut Pankreatitte Enzimatik Yağ Nekrozu Basamakları",
                [
                    "1. Asiner Hasar: Safra taşı veya alkol hasarı sonucu asiner proenzimler intraselüler aktive olur.",
                    "2. Enzim Sızıntısı: Aktive tripsin ve lipaz enzimleri zedelenen hücrelerden peripankreatik dokuya sızar.",
                    "3. Trigliserit Hidrolizi: Lipazlar yağ hücrelerindeki trigliseritleri serbest yağ asitlerine parçalar.",
                    "4. Kalsiyum Bağlanması: Açığa çıkan anyonik yağ asitleri interstisyel kalsiyum (Ca2+) iyonlarıyla birleşir.",
                    "5. Saponifikasyon: Çözünmeyen tebeşir beyazı kalsiyum sabunları (yağ nekrozu) çöker."
                ]
            ),
            make_cloze(
                "Pankreas asiner hücrelerinden sızan lipazlar peripankreatik yağ hücrelerindeki trigliseritleri yıkarak serbest yağ asitleri oluşturur.",
                "serbest yağ asitleri",
                "Trigliseritlerin hidrolizi sonucu açığa çıkan kalsiyum bağlayıcı moleküller"
            )
        ]
    })

    # ADIM 13
    slides.append({
        "slideNumber": 13,
        "title": "Sabunlaşma (Saponifikasyon): Tebeşir Beyazı Birikintilerin Kimyası",
        "subtitle": "Serbest yağ asitlerinin kalsiyum iyonlarıyla oluşturduğu çözünmez tuzlar",
        "badge": "Biyokimya",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Yağ nekrozunun en karakteristik biyokimyasal olayı 'sabunlaşma' (saponifikasyon) reaksiyonudur. "
            "Lipazlar tarafından açığa çıkarılan yağ asitlerinin negatif yüklü karboksilat (-COO⁻) uçları, "
            "ekstraselüler sıvıda ve plazmada bulunan çift değerlikli kalsiyum iyonları (Ca²⁺) ile iyonik bağlar kurar.\n\n"
            "Bu kimyasal birleşme sonucunda suda çözünmeyen 'kalsiyum sabunları' meydana gelir.\n\n"
            "> [SINAV SPOTU] Akut pankreatit cerrahisinde periton açıldığında omentum ve mezenter üzerinde görülen "
            "tebeşir beyazı, opak, mum benzeri sert lekeler saponifikasyonun makroskobik ifadesidir.\n\n"
            "Bu süreçte o kadar yüksek miktarda kalsiyum dokuda sabunlaşarak hapsolur ki, hastanın dolaşımdaki "
            "serum kalsiyumu hızla düşebilir ve ağır 'hipokalsemi' gelişebilir. Bu durum kötü prognoz göstergesidir."
        ),
        "medicalTerms": [
            {"term": "Saponifikasyon (Sabunlaşma)", "explanation": "Serbest yağ asitlerinin kalsiyum gibi katyonlarla birleşerek çözünmez sabun kompleksleri oluşturması."},
            {"term": "Hipokalsemi", "explanation": "Kalsiyumun periton içi yağ nekrozu odaklarında tüketilmesine bağlı serum kalsiyumunun kritik derecede düşmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Makroskopik görünüm: Tebeşir-beyazı (chalky white), sert, peynir kırıntısı benzeri odaklar.",
            "📌 [SINAV SPOTU] Kalsiyumun sabunlaşmada aşırı tüketilmesi akut pankreatitte hipokalsemiye yol açabilir (Ranson kriteri)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kimyasal Reaksiyon", "desc": "Serbest Yağ Asidi + Ca2+ -> Kalsiyum Sabunu (Saponifikasyon).", "isKey": True},
                {"title": "Klinik Yansıma", "desc": "Serum kalsiyumunun hızla dokuya çekilmesi ve tetani riski.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut nekrotizan pankreatit nedeniyle yoğun bakımda izlenen hastanın serum kalsiyum düzeyi 6.2 mg/dL (belirgin düşük) ölçülüyor. Bu durumun patogenetik açıklaması nedir?",
                [
                    {
                        "text": "Pankreas hasarı nedeniyle paratiroid bezi iflas etmiş ve PTH salgısı tamamen durmuştur.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Primer sorun paratiroid bezinde değildir."
                    },
                    {
                        "text": "Peripankreatik yağ nekrozu alanlarında açığa çıkan serbest yağ asitleri serumdaki kalsiyumu sabunlaşma ile bağlayıp dokuda tüketmiştir.",
                        "isCorrect": True,
                        "feedback": "Kusursuz klinik patoloji yorumu! Kalsiyum sabunlarının oluşumu serum kalsiyumunu tüketerek hipokalsemiye yol açar."
                    },
                    {
                        "text": "Böbrekler kalsiyumu idrarla kaybetmiştir.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Buradaki primer mekanizma intraabdominal saponifikasyondur."
                    }
                ]
            ),
            make_cloze(
                "Akut pankreatitte yağ asitlerinin kalsiyum ile birleşerek oluşturduğu tebeşir beyazı odaklara saponifikasyon veya sabunlaşma denir.",
                "saponifikasyon",
                "Yağ asidi ve metal katyon birleşimi reaksiyonunun tıp adı"
            )
        ]
    })

    # ADIM 14
    slides.append({
        "slideNumber": 14,
        "title": "Yağ Nekrozunun Işık Mikroskopisi: Gölge Yağ Hücreleri",
        "subtitle": "Çekirdeksiz adiposit konturları ve çevreleyen bazofilik kalsiyum tuzları",
        "badge": "Mikroskopi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Işık mikroskobu altında yağ nekrozu sahası incelendiğinde son derece tanısal bir mimari izlenir. "
            "Nekroza uğrayan adipositler sitoplazmik lipidlerini ve çekirdeklerini bütünüyle kaybetmiştir.\n\n"
            "Geriye yalnızca soluk, belirsiz hücre zarı konturlarından ibaret 'gölge yağ hücreleri' (shadow cells) kalır. "
            "Bu hücrelerin sitoplazması normaldeki şeffaf lipid vakuolü yerine pembe-morumsu ince granüler bir çökelti barındırır.\n\n"
            "> [SINAV SPOTU] Gölge yağ hücrelerinin sınırlarında, dokuya çöken kalsiyum sabunları hematoksilen boyasını "
            "yoğun şekilde tutarak koyu mor-mavi (bazofilik) kalsiyum birikintileri şeklinde parlar.\n\n"
            "Bu nekrotik alanın periferinde ise yağ kalıntılarını temizlemeye çalışan nötrofiller, köpüksü makrofajlar "
            "ve lenfositlerden oluşan belirgin bir inflamatuar infiltrasyon eşlik eder."
        ),
        "medicalTerms": [
            {"term": "Gölge Yağ Hücreleri (Shadow Cells)", "explanation": "Çekirdeğini ve lipid damlasını kaybetmiş, yalnızca dış membran hatları seçilebilen ölü adipositler."},
            {"term": "Bazofilik Kalsiyum Tuzları", "explanation": "Hematoksilenle koyu mor-mavi boyanan, kalsiyum sabunlaşmasının mikroskobik görüntüsü."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mikroskopide çekirdeğini kaybetmiş 'gölge yağ hücreleri' izlenir.",
            "📌 [SINAV SPOTU] Hücre sınırlarında koyu mor-mavi (bazofilik) kalsiyum birikintileri ve çevreleyen inflamasyon mevcuttur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Gölge Adipositler", "desc": "Nükleussuz, soluk, konturları korunmuş hücre hayaletleri.", "isKey": True},
                {"title": "Bazofilik Çerçeve", "desc": "Membran kenarlarında çöken mor-mavi kalsiyum sabunları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Histolojik Bileşen", "Mikroskobik Görünüm", "Biyokimyasal Karşılığı"],
                [
                    [("Gölge Adipositler", False, ""), ("Çekirdeksiz, soluk hücre anahatları", True, "Nükleus kaybı göstergesi"), ("Ölü yağ hücresi iskeleti", False, "")],
                    [("Kalsiyum Sabunları", False, ""), ("Koyu mor-mavi (bazofilik) granüler birikim", True, "Hematoksilen boyanma rengi"), ("Yağ asidi + Ca2+ tuzu", False, "")],
                    [("Çevre İnfiltrat", False, ""), ("Köpüksü makrofajlar ve nötrofiller", True, "Fagositik hücre tipi"), ("Akut ve kronik yangısal yanıt", False, "")]
                ]
            ),
            make_cloze(
                "Yağ nekrozu mikroskopisinde çekirdeğini kaybetmiş ölü adipositlere gölge yağ hücreleri adı verilir.",
                "gölge yağ hücreleri",
                "İçeriği boşalmış ölü adiposit kalıntıları"
            )
        ]
    })

    # ADIM 15
    slides.append({
        "slideNumber": 15,
        "title": "Travmatik Yağ Nekrozu: Meme Dokusunda Tümör Benzeri Kitle",
        "subtitle": "Kaza veya cerrahi sonrası memede gelişen ve mamografide karsinomu taklit eden lezyon",
        "badge": "Meme Patolojisi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Yağ nekrozunun pankreas dışındaki en önemli klinik örneği memede görülen 'travmatik yağ nekrozu'dur. "
            "Emniyet kemeri travması, künt darbe, meme biyopsisi veya cerrahi müdahale sonrasında adipositler parçalanır.\n\n"
            "Açığa çıkan serbest lipitler dokuda güçlü bir yabancı cisim tipi inflamatuar reaksiyon tetikler. "
            "Makrofajlar lipitleri fagosite ederek bol vakuollü 'köpüksü histiyositlere' dönüşürler.\n\n"
            "> [KLİNİK İPUCU] Lezyon iyileşirken yoğun fibroblastik proliferasyon ve distrofik kalsifikasyon gelişir; "
            "bu durum memede sert, düzensiz sınırlı ve deriye yapışık bir kitle oluşturarak mamografide meme kanserini (karsinom) taklit eder!\n\n"
            "Histopatolojik biyopside lipid yüklü makrofajlar, dev hücreler ve kalsiyum sabunları görülerek malignite ekarte edilir."
        ),
        "medicalTerms": [
            {"term": "Travmatik Yağ Nekrozu", "explanation": "Meme veya subkutan yağ dokusunda travma sonrası gelişen, köpüksü makrofaj ve fibrozisle seyreden psödotümoral lezyon."},
            {"term": "Köpüksü Histiyosit (Foamy Macrophage)", "explanation": "Nekrotik yağ damlacıklarını içine alarak sitoplazması vakuollerle dolan fagositer hücre."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Memede travmatik yağ nekrozu klinik ve radyolojik olarak meme kanserini (karsinom) taklit edebilir.",
            "📌 [SINAV SPOTU] Histolojide köpüksü makrofajlar, yabancı cisim dev hücreleri, kalsifikasyon ve fibrozis izlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Meme Kanserini Taklit", "desc": "Palpasyonda sert, deriye fikse kitle ve mamografide mikrokalsifikasyon.", "isKey": True},
                {"title": "Histopatolojik Ayırım", "desc": "Lipofaglar, kalsiyum sabunları ve fibrotik skar dokusu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Meme Yağ Nekrozu vs İnvaziv Meme Karsinomu",
                "Travmatik Yağ Nekrozu",
                "Benign lezyon; biyopside köpüksü histiyositler, lipit vakuolleri ve kalsifiye gölge adipositler izlenir.",
                "İnvaziv Meme Karsinomu",
                "Malign neoplazm; atipik duktal/lobüler epitel hücre adaları, nükleer pleomorfizm ve desmoplazi izlenir."
            ),
            make_active_recall(
                "Memede travmatik yağ nekrozunun klinik ve mamografik açıdan en önemli pratik önemi nedir?",
                "Sert ve düzensiz sınırlı kitle oluşturması ve kalsifikasyon içermesi nedeniyle meme kanserini (karsinom) taklit edebilmesidir."
            )
        ]
    })

    # ADIM 16
    slides.append({
        "slideNumber": 16,
        "title": "Subkutan Yağ Nekrozu: Yenidoğanda Travmatik ve Soğuk Hasarı",
        "subtitle": "Zor doğum veya hipotermi sonrası subkutan yağ lobüllerinde dev hücreli yangı",
        "badge": "Pediatrik Patoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Yağ nekrozunun bir diğer özgün varyantı 'Yenidoğanın Subkutan Yağ Nekrozu'dur. Genellikle zor doğum, "
            "asfiksi, doğum forsepsi travması veya hipotermiye maruz kalan miadında doğmuş bebeklerde ilk haftalarda ortaya çıkar.\n\n"
            "Yenidoğan adipositleri yüksek oranda doymuş yağ asidi (palmitik ve stearik asit) içerdiğinden, erime noktaları "
            "yüksektir ve hafif soğuk maruziyetinde kolayca kristalize olarak nekroza uğrarlar.\n\n"
            "> [SINAV SPOTU] Histolojide yağ hücreleri içinde radyal (ışınsal) dizilimli iğsi lipid kristalleri "
            "ve etrafında granülomatöz inflamasyon izlenir.\n\n"
            "Klinik olarak omuz, sırt ve kalçada eritemli, sert plaklar şeklinde palpe edilir; aylar içinde kendiliğinden "
            "geriler ancak nadiren hiperkalsemiye yol açabilir."
        ),
        "medicalTerms": [
            {"term": "Yenidoğan Subkutan Yağ Nekrozu", "explanation": "Miadında yenidoğanlarda travma veya hipotermi sonucu gelişen, iğsi kristallerle karakterize benign subkutan yangı."},
            {"term": "İğsi Lipid Kristalleri", "explanation": "Doymuş yağ asitlerinin soğukta kristalize olmasıyla adiposit içinde oluşan çatallı radyal kristaller."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yenidoğanda subkutan yağ nekrozu hipotermi ve doğum travmasıyla tetiklenir.",
            "📌 [SINAV SPOTU] Adipositlerde iğsi lipid yarıkları ve çevreleyen granülomatöz yanıt karakteristiktir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Doymuş Yağ Duyarlılığı", "desc": "Yenidoğan yağının düşük ısılarda donarak kristalleşmesi.", "isKey": True},
                {"title": "Kristal Morfolojisi", "desc": "Hücre içinde radyal iğne benzeri kristal boşlukları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Zor bir doğum sonrası sırtında sert, ağrısız cilt altı nodülleri gelişen 10 günlük bebeğin biyopsisinde adipositlerde radyal iğsi kristaller ve kalsifikasyon saptanıyor. En olası tanı nedir?",
                {
                    "A": "Kazeöz nekrozlu tüberküloz",
                    "B": "Yenidoğanın subkutan yağ nekrozu",
                    "C": "Poliarteritis nodosa",
                    "D": "Enzimatik koagülatif nekroz",
                    "E": "Malign liposarkom"
                },
                "B",
                {
                    "A": "Tüberküloz yenidoğan cildinde nodül yapmaz.",
                    "B": "Doğru cevap B'dir: Doğum travması/soğuk sonrası radyal kristalli lezyon yenidoğan subkutan yağ nekrozudur.",
                    "C": "Vaskülit lezyonudur.",
                    "D": "Enzimatik yağ nekrozu pankreatittedir.",
                    "E": "Çocuklukta son derece nadir malign tümördür."
                }
            ),
            make_cloze(
                "Yenidoğan subkutan yağ nekrozunda adipositlerin içinde radyal dizilimli iğsi kristaller ve kalsifikasyon izlenir.",
                "iğsi kristaller",
                "Doymuş yağların oluşturduğu mikroskobik iğne biçimli yapılar"
            )
        ]
    })

    # ADIM 17
    slides.append({
        "slideNumber": 17,
        "title": "Yağ Nekrozunda Boyama Özellikleri: Özel Yağ Boyaları",
        "subtitle": "Rutin preparatlarda eriyen lipidlerin dondurma kesitte Oil Red O ve Sudan ile gösterilmesi",
        "badge": "Laboratuvar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Rutin patoloji laboratuvarında dokular parafine gömülürken ksilen ve alkol gibi organik solventlerden geçer. "
            "Bu kimyasallar hücrelerdeki tüm lipid damlacıklarını eritir; bu nedenle standart H&E kesitlerinde yağ hücreleri "
            "ve vakuolleri tamamen boş ve beyaz delikler şeklinde görünür.\n\n"
            "Yağ nekrozunda serbest lipidleri ve makrofajların fagositozunu kesin olarak kanıtlamak için doku taze "
            "olarak dondurulmalı (frozen section) ve özel lipid boyaları uygulanmalıdır.\n\n"
            "> [SINAV SPOTU] Dondurma kesitlerde serbest yağ damlacıklarını ve trigliseritleri göstermek için "
            "Oil Red O veya Sudan III / Sudan Black boyaları kullanılır; lipidler parlak kırmızı-turuncu boyanır.\n\n"
            "Kalsiyum sabunlarını göstermek için ise Von Kossa (gümüşleme) veya Alizarin Red S boyası uygulanır."
        ),
        "medicalTerms": [
            {"term": "Oil Red O", "explanation": "Dondurma kesitlerde nötral lipitleri ve trigliseritleri parlak kırmızıya boyayan özel histokimyasal boya."},
            {"term": "Von Kossa Boyası", "explanation": "Doku kesitlerinde çöken kalsiyum tuzlarını siyaha boyayan gümüşleme reaksiyonu."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Rutin parafin takibinde lipidler eridiği için adipositler boş delikler olarak görünür.",
            "📌 [SINAV SPOTU] Lipidleri göstermek için taze donuk kesitte Oil Red O veya Sudan boyaları kullanılır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Ksilen Çözünmesi", "desc": "Parafin bloklamada alkol ve ksilenin yağı eritip boşluk bırakması.", "isKey": True},
                {"title": "Lipid Boyama Prensibi", "desc": "Taze dokuda Oil Red O ile parlak kırmızı lipid damlaları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hedef Madde", "Tercih Edilen Boya", "Görülen Pozitif Renk"],
                [
                    [("Trigliserit / Nötral Yağ", False, ""), ("Oil Red O / Sudan III", True, "Lipid tespit boyası"), ("Parlak Kırmızı / Turuncu", False, "")],
                    [("Kalsiyum Sabunları", False, ""), ("Von Kossa / Alizarin Red", True, "Kalsiyum tespit boyası"), ("Siyah / Koyu Kırmızı", False, "")],
                    [("Hücre Çekirdeği", False, ""), ("Hematoksilen", True, "Nükleus rutin boyası"), ("Koyu Mor-Mavi", False, "")]
                ]
            ),
            make_cloze(
                "Dondurma kesitlerde yağ nekrozu alanlarındaki serbest lipitleri göstermek için Oil Red O boyası kullanılır.",
                "Oil Red O",
                "Lipitleri kırmızıya boyayan özel histokimyasal boya adı"
            )
        ]
    })

    # ADIM 18
    slides.append({
        "slideNumber": 18,
        "title": "Yağ Nekrozunun İyileşme Süreci: Fibröz Skar ve Yağ Kistleri",
        "subtitle": "Köpüksü histiyosit fagositozundan distrofik kalsifikasyon ve skar oluşumuna evrilme",
        "badge": "İyileşme",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Yağ nekrozu sahası akut enflamatuar fırtına dindikten sonra kademeli bir doku onarım sürecine girer. "
            "Ölü adipositlerin ve kalsiyum sabunlarının temizlenmesi haftalar veya aylar sürebilir.\n\n"
            "İlk evrede ortama doluşan köpüksü makrofajlar (lipofaglar) serbest lipitleri içine alır. "
            "Eğer nekroz sahası genişse, makrofajlar nekrotik lipitleri tamamen temizleyemez ve etrafı fibröz kapsülle "
            "çevrili sıvı lipid dolu 'yağ kistleri' (lipid kistleri) oluşur.\n\n"
            "> [SINAV SPOTU] Küçük yağ nekrozu odakları ise zamanla fibroblast göçü ve kollajen senteziyle tamamen "
            "fibröz skara dönüşür ve distrofik kalsifikasyon ile sert bir taş kıvamı kazanır.\n\n"
            "Bu durum karın ameliyatı geçiren veya pankreatit atlatan hastaların batın tomografilerinde kalsifiye nodüller "
            "olarak ömür boyu izlenebilir."
        ),
        "medicalTerms": [
            {"term": "Lipofag", "explanation": "Nekrotik yağ damlacıklarını fagosite eden ve sitoplazması köpüksü görünen makrofaj."},
            {"term": "Yağ Kisti (Lipid Kisti)", "explanation": "Eriyen yağın temizlenemeyip fibröz kapsülle çevrilmesi sonucu oluşan kistik lezyon."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yağ nekrozu iyileşirken köpüksü makrofaj infiltrasyonu, fibrozis ve kalsifikasyon gelişir.",
            "📌 [SINAV SPOTU] Büyük nekroz alanları fibröz duvarlı 'yağ kistlerine' dönüşebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Makrofaj Süreci", "desc": "Lipofagların nekrotik damlacıkları temizleme çabası.", "isKey": True},
                {"title": "Fibröz Kapsülleme", "desc": "Skar dokusu, distrofik kalsiyum çökmesi ve lipid kisti oluşumu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Yağ Nekrozu İyileşme Basamakları",
                [
                    "1. Akut Hücresel Yıkım: Serbest yağ asitleri ve kalsiyum sabunları nötrofilleri çeker.",
                    "2. Köpüksü Makrofaj Hücumu: Lipofaglar ortama girerek parçalanmış lipidleri fagosite eder.",
                    "3. Fibroblast Aktivasyonu: Salınan büyüme faktörleri kollajen sentezini ve granülasyon dokusunu başlatır.",
                    "4. Fibröz Skarlaşma: Nekrotik alan yoğun fibrotik bir kapsül veya skara dönüşür.",
                    "5. Distrofik Kalsifikasyon: Kalsiyum sabunları hidroksiapatit kristallerine dönüşerek lezyonu taşlaştırır."
                ]
            ),
            make_cloze(
                "Yağ nekrozunda serbest lipitleri yutarak sitoplazması vakuollerle dolan makrofajlara köpüksü makrofaj veya lipofag denir.",
                "köpüksü makrofaj",
                "Lipid yüklü yangısal fagositer hücre"
            )
        ]
    })

    # ADIM 19 (CHECKPOINT 2)
    slides.append({
        "slideNumber": 19,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Enzimatik ve Travmatik Yağ Nekrozu",
        "subtitle": "Pankreatit, meme travması, sabunlaşma kimyası ve histolojinin kilit konsolidasyonu",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 2,
        "synthesisNarrative": (
            "Bu kontrol noktasında, yağ dokusunun özgün reaksiyonu olan yağ nekrozunu ve klinik yansımalarını özetliyoruz.\n\n"
            "Yağ nekrozu temel olarak akut pankreatitte salınan lipazların trigliseritleri parçalaması veya "
            "meme/subkutan dokuda travma sonucu oluşur. En ayırt edici biyokimyasal basamak, açığa çıkan serbest "
            "yağ asitlerinin kalsiyum (Ca²⁺) ile birleşerek sabunlaşma (saponifikasyon) yapmasıdır.\n\n"
            "> [ÖZET REÇETE] Makroskopi = Tebeşir beyazı odaklar; Mikroskopi = Çekirdeksiz gölge adipositler + "
            "bazofilik mor kalsiyum tuzları; Klinik Risk = Pankreatitte hipokalsemi, memede kanser mimikrisi!\n\n"
            "Bu üçleme (pankreatit - sabunlaşma - gölge hücreler) tüm patoloji ve klinik sınavlarının değişmez soru kaynağıdır."
        ),
        "medicalTerms": [
            {"term": "Saponifikasyon", "explanation": "Serbest yağ asitlerinin kalsiyum ile tebeşir beyazı sabun çökeltileri oluşturması."},
            {"term": "Gölge Adiposit", "explanation": "Çekirdeğini kaybetmiş ancak hücre dış zarı seçilebilen nekrotik yağ hücresi."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Yağ nekrozu = Akut pankreatit (lipaz) veya meme travması.",
            "📌 [CHECKPOINT ÖZETİ] Biyokimya = Trigliserit -> Yağ asidi + Ca2+ -> Sabunlaşma (Saponifikasyon).",
            "📌 [CHECKPOINT ÖZETİ] Mikroskopi = Çekirdeksiz gölge yağ hücreleri + bazofilik kalsiyum tuzları."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-04",
                "Akut pankreatitte gelişen yağ nekrozunda tebeşir beyazı odakların biyokimyasal temeli nedir?",
                "Pankreatik lipazların trigliseritleri serbest yağ asitlerine hidrolize etmesi ve bu asitlerin kalsiyum ile birleşerek kalsiyum sabunları (saponifikasyon) oluşturmasıdır."
            ),
            make_flashcard(
                "fc-k1-05-05",
                "Yağ nekrozunun ışık mikroskopisindeki iki temel karakteristik bulgusu nedir?",
                "1) Çekirdeğini kaybetmiş soluk 'gölge yağ hücreleri' ve 2) Hücre sınırlarında hematoksilenle mor-mavi boyanan bazofilik kalsiyum sabunu birikintileridir."
            ),
            make_flashcard(
                "fc-k1-05-06",
                "Memede görülen travmatik yağ nekrozunun klinik ve cerrahi açıdan en büyük tehlikesi nedir?",
                "Sert, düzensiz sınırlı kitle yapması ve kalsifikasyon içermesi nedeniyle meme karsinomunu (kanserini) taklit etmesidir."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Yağ Nekrozu ve Diğer Nekroz Tiplerinin Karşılaştırma Matrisi",
                "headers": ["Parametre", "Yağ Nekrozu", "Kazeöz Nekroz", "Koagülatif Nekroz"],
                "rows": [
                    ["Tetikleyici Neden", "Lipaz aktivasyonu / Travma", "Tüberküloz enfeksiyonu", "İskemi / Hipoksi (infarkt)"],
                    ["Etkilenen Doku", "Adipoz doku (omentum, meme)", "Akciğer, lenf nodu", "Böbrek, kalp, dalak"],
                    ["Makroskobik Renk", "Tebeşir beyazı opak lekeler", "Sarı-beyaz peynirimsi yumuşak", "Soluk sarı-gri sert kama"],
                    ["Mikroskobik Hücreler", "Gölge adipositler + Ca tuzları", "Amorf granüler + Langhans", "Hücre anahatları korunmuş hayalet"],
                    ["Özel Reaksiyon", "Saponifikasyon (sabunlaşma)", "Granülomatöz sınırlandırma", "Protein denatürasyonu"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Patolojik Durum", "Primer Enzim / Faktör", "Kritik Klinik Komplikasyon"],
                [
                    [("Akut Pankreatit Yağ Nekrozu", False, ""), ("Pankreatik Lipaz", True, "Yağ yıkan temel enzim"), ("Şiddetli Hipokalsemi", False, "")],
                    [("Meme Travmatik Yağ Nekrozu", False, ""), ("Mekanik Künt Travma", True, "Hücre zarlarını delen olay"), ("Meme Kanserini Taklit Etme", False, "")],
                    [("Yenidoğan Subkutan Yağ Nekrozu", False, ""), ("Hipotermi / Asfiksi", True, "Kristalleşmeyi başlatan faktör"), ("Derialtı Sert Plaklar", False, "")]
                ]
            ),
            make_active_recall(
                "Akut pankreatitte serum kalsiyumunun hızla düşerek hipokalsemiye yol açmasının doğrudan sebebi nedir?",
                "Açığa çıkan serbest yağ asitlerinin serum kalsiyumunu sabunlaşma (saponifikasyon) reaksiyonuyla dokuda tüketmesidir."
            )
        ]
    })

    # ADIM 20
    slides.append({
        "slideNumber": 20,
        "title": "Pankreatitte Sistemik Enzim Dağılımı: Uzak Yağ Dokusu Nekrozları",
        "subtitle": "Dolaşıma katılan lipazların kemik iliği ve eklem çevresi yağ dokusunu eritmesi",
        "badge": "Sistemik Patoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Ağır nekrotizan pankreatitte pankreas kaynaklı enzimler yalnızca batın içi omentum ve mezenterle "
            "sınırlı kalmaz. Yıkılan kılcal damarlar yoluyla kana karışan pankreatik lipaz ve fosfolipazlar tüm dolaşıma yayılır.\n\n"
            "Bu enzimler vücudun en ücra köşelerindeki yağ depolarına ulaşarak 'metastatik yağ nekrozu' odakları oluşturur. "
            "Özellikle cilt altı yağ dokusunda, periartiküler bölgelerde ve kemik iliğinde yağ nekrozu meydana gelebilir.\n\n"
            "> [KLİNİK İPUCU] Akut pankreatitli bir hastada bacaklarda ağrılı eritemli nodüller ve eklem ağrısı geliştiğinde "
            "cilt altı ve sinovyal yağ nekrozu (pankreatik pannikülit) akla gelmelidir.\n\n"
            "Kemik iliğindeki trabeküler yağın nekrozu ise kemik infarktlarına ve şiddetli kemik ağrılarına yol açabilir."
        ),
        "medicalTerms": [
            {"term": "Pankreatik Pannikülit", "explanation": "Dolaşımdaki pankreatik lipazların deri altı yağ dokusunu eritmesiyle oluşan ağrılı nodüler yağ nekrozu tablosu."},
            {"term": "Metastatik Yağ Nekrozu", "explanation": "Enzimlerin kan yoluyla pankreastan uzak yağ dokularına (kemik iliği, eklem) ulaşıp nekroz yapması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut pankreatitte lipaz dolaşıma geçerek cilt altında ve kemik iliğinde metastatik yağ nekrozu yapabilir.",
            "📌 [SINAV SPOTU] Bu klinik tabloya 'pankreatik pannikülit' adı verilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enzim Hematojen Yayılımı", "desc": "Lipazın sistemik dolaşımla uzak yağ depolarına taşınması.", "isKey": True},
                {"title": "Pannikülit Görünümü", "desc": "Alt ekstremitede hassas, eritemli subkutan nodüller.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut pankreatit tanısıyla yatan 52 yaşındaki hastanın bacak ön yüzlerinde ağrılı, kızarık cilt altı nodülleri ve ayak bileğinde artralji gelişiyor. Biyopside cilt altı yağında gölge adipositler ve kalsiyum sabunları izleniyor.",
                [
                    {
                        "text": "Hastada metastatik meme kanseri gelişmiştir; derhal kemoterapi planlanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Lezyon neoplazi değil, pankreatik enzimlere bağlı yağ nekrozudur."
                    },
                    {
                        "text": "Dolaşıma karışan pankreatik lipazların deri altı yağını eritmesiyle gelişen 'pankreatik pannikülit' tablosudur.",
                        "isCorrect": True,
                        "feedback": "Doğru patogenetik tanı! Pankreatik enzimlerin sistemik yayılımı subkutan yağ nekrozuna (pannikülit) yol açar."
                    },
                    {
                        "text": "Hastaya tüberküloz basili bulaşmış ve eritema nodozum gelişmiştir.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Histolojide kalsiyum sabunlaşması pankreatik kökeni kanıtlar."
                    }
                ]
            ),
            make_cloze(
                "Pankreatik lipazların kan dolaşımıyla cilt altı yağ dokusuna ulaşarak oluşturduğu nodüler lezyonlara pankreatik pannikülit denir.",
                "pankreatik pannikülit",
                "Enzimatik cilt altı yağ yangısı tablosu"
            )
        ]
    })

    return slides
