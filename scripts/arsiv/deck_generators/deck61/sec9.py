"""
Deck 61: Abortus - Section 9 (Slides 81-90)
Konu: Erken Gebelik Kaybında Yönetim Seçenekleri ve Alloimmünizasyon Profilaksisi
Müfredat: TIP 310 · Abortus · Dr. Öğr. Üyesi Hilal Ezgi Türkmen · Dönem 3 Kurul 1
"""

from typing import List, Dict, Any
from .deck61_helper import (
    make_slide,
    make_quiz,
    make_cloze,
    make_table,
    make_slider,
    make_chain,
    make_recall,
    make_spot_the_lie,
    make_swipe,
    make_venn,
    make_branching
)

def get_sec9_slides() -> List[Dict[str, Any]]:
    slides = [
        # Slide 81
        make_slide(
            slide_num=81,
            title="Yönetim Seçeneklerine Genel Bakış: Üç Temel Klinik Yol",
            subtitle="Ekspektan, Medikal ve Cerrahi Tedavi Yaklaşımlarının Karşılaştırılması",
            clinical_focus="Erken gebelik kaybında hasta kliniği, hemodinami ve tercihe göre üç yönetim seçeneği sunulur.",
            narrative="""Erken gebelik kaybı kesinleştiğinde tedavi kararı hastanın klinik durumuna ve tercihlerine göre şekillenir. Ders notunda erken gebelik kaybında üç temel yönetim seçeneği tanımlanmıştır: bekleme-takip, medikal yönetim ve cerrahi yönetim.

- **Ekspektan (Bekleme-Takip) Yaklaşım:** Hemodinamisi stabil, enfeksiyon ve yoğun kanama bulgusu olmayan hastalarda gebelik ürünlerinin kendiliğinden düşmesini bekleme prensibine dayanır.
- **Medikal Tedavi:** Uterin kontraksiyonları ve servikal olgunlaşmayı tetikleyen farmakolojik ajanların (misoprostol, mifepriston) kullanımıyla kavitenin boşaltılmasıdır.
- **Cerrahi Tahliye:** Dilatasyon ve küretaj (D&C) veya vakum aspirasyon ile materyalin mekanik olarak temizlenmesidir; aşırı kanama veya enfeksiyonda ilk tercihtir.

> [!NOTE]
> Yönetim stratejisi belirlenirken maternal hemodinamik stabilite, enfeksiyon bulguları ve hastanın psikolojik tercihi mutlaka birlikte değerlendirilir.""",
            bullets=[
                "Üç temel yaklaşım: Bekleme-takip, medikal tedavi ve cerrahi tahliye",
                "Ekspektan yönetim stabil, asemptomatik veya hafif semptomatik hastalara sunulur",
                "Ağır kanama veya enfeksiyon varlığında cerrahi tahliye zorunlu hale gelir"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre erken gebelik kaybı tanısı kesinleşen hemodinamik olarak stabil bir hastada sunulabilecek temel yönetim seçenekleri hangi seçenekte eksiksiz verilmiştir?",
                    options=[
                        {"key": "A", "text": "Bekleme-takip, medikal yönetim ve cerrahi yönetim", "isCorrect": True, "explanation": "Doğru. Ders notu Bölüm 9'da üç temel seçenek: Bekleme-takip, medikal ve cerrahi olarak tanımlanmıştır."},
                        {"key": "B", "text": "Yalnızca acil laparotomi ve histerektomi", "isCorrect": False, "explanation": "Gereksiz radikal cerrahidir, erken gebelik kaybında endike değildir."},
                        {"key": "C", "text": "Sadece yüksek doz sistemik metotreksat infüzyonu", "isCorrect": False, "explanation": "Metotreksat abortus yönetiminde standart tedavi değildir, ektopikte kullanılır."},
                        {"key": "D", "text": "Yalnızca radyoterapi ve hormonal baskılama", "isCorrect": False, "explanation": "Tıbbi gerçek dışıdır."}
                    ],
                    correct_key="A"
                ),
                make_cloze(
                    sentence="Ders notuna göre erken gebelik kaybında yönetim seçenekleri bekleme-takip, medikal tedavi ve cerrahi yönetim olmak üzere üç ana başlıkta toplanır.",
                    masked_term="bekleme-takip",
                    hint="Herhangi bir müdahale yapmadan kendiliğinden atılımı gözleme yöntemi"
                ),
                make_table(
                    title="Erken Gebelik Kaybında Üç Temel Yönetim Modelinin Özellikleri",
                    headers=["Yönetim Modeli", "Temel Mekanizma / Yöntem", "Uygun Hasta Profili"],
                    rows=[
                        [
                            {"text": "Bekleme-Takip (Ekspektan)", "isMasked": False},
                            {"text": "Kendiliğinden atılımı izleme", "isMasked": True, "hint": "Doğal fizyolojik düşük sürecini gözlemleme"},
                            {"text": "Hemodinamik açıdan stabil, enfeksiyonu olmayan", "isMasked": False}
                        ],
                        [
                            {"text": "Medikal Yönetim", "isMasked": False},
                            {"text": "Misoprostol ve mifepriston kullanımı", "isMasked": True, "hint": "Uterotonik farmakolojik protokol"},
                            {"text": "Cerrahiden kaçınmak isteyen stabil hasta", "isMasked": False}
                        ],
                        [
                            {"text": "Cerrahi Yönetim", "isMasked": False},
                            {"text": "Dilatasyon ve küretaj veya vakum aspirasyon", "isMasked": True, "hint": "Kaviter içeriği aletle mekanik tahliye"},
                            {"text": "Aşırı kanamalı, enfekte veya kesin çözüm isteyen", "isMasked": False}
                        ]
                    ]
                ),
                make_recall(
                    question="Ders notunda erken gebelik kaybında belirtilen üç temel yönetim seçeneği nelerdir?",
                    answer="Bekleme-takip (ekspektan yaklaşım), medikal yönetim (misoprostol, mifepriston) ve cerrahi yönetim (D&C, vakum aspirasyon)."
                )
            ]
        ),

        # Slide 82
        make_slide(
            slide_num=82,
            title="Bekleme-Takip (Ekspektan Yönetim): Doğal Düşük Süreci",
            subtitle="Hasta Seçimi, Başarı Oranları ve Takip Prensipleri",
            clinical_focus="Ekspektan yönetimde hasta kanama ve enfeksiyon belirtileri açısından çok yakın bilgilendirilmelidir.",
            narrative="""Bekleme-takip yöntemi, hastaya herhangi bir ilaç veya cerrahi müdahale yapmaksızın gebelik dokularının fizyolojik kontraksiyonlarla atılmasını izlemektir. Özellikle inkomplet abortus veya erken missed abortus vakalarında stabil hastalara sunulabilir.

- **Hasta Uygunluğu:** Hastada aşırı vajinal kanama, hemodinamik dengesizlik veya pelvik enfeksiyon (septik abortus şüphesi) bulunmamalıdır.
- **Klinik Süreç:** Süreç birkaç günden birkaç haftaya kadar uzayabilir. Hastaya kanama artışı, parça düşürme ve kramp ağrıları olacağı önceden anlatılmalıdır.
- **Acil Uyarı Kriterleri:** Ateş yüksekliği, kötü kokulu akıntı, saatte 2'den fazla ped kirletecek şiddette aşırı kanama veya presenkop durumunda acil cerrahiye geçilir.

> [!IMPORTANT]
> Ekspektan yönetim seçilen hastalarda enfeksiyon ve kontrolsüz kanama riski nedeniyle hastanın acil servise hızlı ulaşım imkanı bulunmalıdır.""",
            bullets=[
                "İlaçsız ve cerrahisiz kendiliğinden atılım prensibine dayanır",
                "Yalnızca hemodinamik olarak stabil ve enfeksiyon bulgusu olmayan gebelere önerilir",
                "Aşırı kanama veya sepsis belirtisinde derhal cerrahi tahliyeye dönülür"
            ],
            elements=[
                make_quiz(
                    question="Bekleme-takip (ekspektan) yönetimi tercih edilen erken gebelik kayıplı bir hastada aşağıdaki durumlardan hangisi gelişirse acilen cerrahi tahliyeye geçilmelidir?",
                    options=[
                        {"key": "A", "text": "Hafif lekelenme tarzında pembe akıntı olması", "isCorrect": False, "explanation": "Beklenen hafif semptomdur, acil cerrahi gerektirmez."},
                        {"key": "B", "text": "Yüksek ateş, taşikardi, pürülan kokulu akıntı ve aşırı kontrolsüz kanama gelişmesi", "isCorrect": True, "explanation": "Doğru. Sepsis ve şiddetli hemoraji gelişimi acil cerrahi boşaltma endikasyonudur."},
                        {"key": "C", "text": "Serum hCG değerinin düşüş eğiliminde olması", "isCorrect": False, "explanation": "Düşüş normal rezolüsyon bulgusudur."},
                        {"key": "D", "text": "Hafif pelvik kramp hissedilmesi", "isCorrect": False, "explanation": "Uterin kontraksiyonların doğal sonucudur."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notunda erken gebelik kaybı seçenekleri arasında yer alan bekleme-takip süreci enfeksiyon veya aşırı kanama varlığında kesinlikle sonlandırılır.",
                    masked_term="aşırı kanama",
                    hint="Hemodinamik şok riski doğuran majör obstetrik komplikasyon"
                ),
                make_spot_the_lie(
                    topic="Erken gebelik kaybında bekleme-takip (ekspektan) yönetimi prensipleri",
                    items=[
                        {"text": "Ekspektan yönetim stabil, enfeksiyonu olmayan ve yakın takip edilebilen hastalara sunulur.", "isLie": False, "explanation": "Temel kuraldır."},
                        {"text": "Septik abortus tablosundaki hastalarda bekleme-takip yöntemi güvenle uygulanabilir.", "isLie": True, "explanation": "Tuzak! Septik abortusta bekleme yapılamaz, acil IV antibiyotik ve cerrahi tahliye şarttır."},
                        {"text": "Hastada süreç boyunca şiddetli kanama ve enfeksiyon semptomları gelişirse cerrahiye geçilir.", "isLie": False, "explanation": "Güvenlik protokolüdür."},
                        {"text": "Bekleme sürecinde gebelik dokularının tam olarak atılıp atılmadığı ultrasonla doğrulanır.", "isLie": False, "explanation": "Klinik standarttır."}
                    ]
                ),
                make_recall(
                    question="Erken gebelik kaybında ekspektan yönetimin en önemli kontrendikasyonları nelerdir?",
                    answer="Hemodinamik instabilite, şiddetli kontrolsüz kanama, pelvik enfeksiyon veya septik abortus bulgularının varlığıdır."
                )
            ]
        ),

        # Slide 83
        make_slide(
            slide_num=83,
            title="Medikal Yönetim: Misoprostol (Prostaglandin E1 Analoğu)",
            subtitle="Farmakolojik Etki, Dozaj Yolları ve Uterotonik Etki Mekanizması",
            clinical_focus="Misoprostol serviksi olgunlaştırır ve güçlü myometrial kontraksiyonlar oluşturur.",
            narrative="""Medikal abortus yönetiminde en yaygın ve temel farmakolojik ajan prostaglandin E1 analoğu olan misoprostoldur. Ders notunda medikal yönetim seçenekleri arasında açıkça vurgulanmıştır.

- **Etki Mekanizması:** Servikal konnektif dokuyu yumuşatarak servikal dilatasyon sağlar ve myometriumdaki düz kas liflerini uyararak güçlü ritmik uterin kasılmalar başlatır.
- **Uygulama Yolları:** Vajinal, bukkal, sublingual veya oral yollarla uygulanabilir; vajinal ve sublingual uygulamalar genellikle daha yüksek biyoyararlanım ve başarı gösterir.
- **Yan Etkiler:** Prostaglandin reseptörlerinin uyarılmasına bağlı olarak karın krampları, hafif ateş, titreme, bulantı, kusma ve diyare görülebilir.
- **Klinik Sonuç:** Olguların çoğunda saatler veya günler içinde gebelik dokularının atılmasını sağlayarak cerrahi anestezi ve mekanik travma risklerini ortadan kaldırır.

> [!NOTE]
> Misoprostol bir prostaglandin E1 analoğudur; myometriumu kasar ve servikal efasman sağlayarak kavitenin tahliyesine yol açar.""",
            bullets=[
                "Misoprostol sentetik bir Prostaglandin E1 (PGE1) analoğudur",
                "Servikal yumuşama ve güçlü myometrial kontraksiyonlar oluşturur",
                "Cerrahi müdahale ve anestezi risklerinden kaçınmayı sağlar"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre erken gebelik kaybının medikal yönetiminde kullanılan prostaglandin E1 analoğu farmakolojik ajan aşağıdakilerden hangisidir?",
                    options=[
                        {"key": "A", "text": "Metotreksat", "isCorrect": False, "explanation": "Folat antagonistidir, PGE1 analoğu değildir."},
                        {"key": "B", "text": "Oksitosin", "isCorrect": False, "explanation": "Nonapeptit nörohipofiz hormonudur, PGE1 değildir."},
                        {"key": "C", "text": "Misoprostol", "isCorrect": True, "explanation": "Doğru. Ders notu Bölüm 9'da medikal ajan olarak 'Misoprostol (prostaglandin E1)' açıkça belirtilmiştir."},
                        {"key": "D", "text": "Metherjin (Metilergonovin)", "isCorrect": False, "explanation": "Ergot alkaloididir, PGE1 analoğu değildir."}
                    ],
                    correct_key="C"
                ),
                make_cloze(
                    sentence="Ders notunda erken gebelik kaybının medikal yönetiminde kullanılan temel ajan Misoprostol olup farmakolojik olarak prostaglandin E1 analoğudur.",
                    masked_term="Misoprostol",
                    hint="Medikal abortusta sık kullanılan sentetik prostaglandin E1 türevi"
                ),
                make_chain(
                    title="Misoprostol Aracılı Medikal Abortus Mekanizma Zinciri",
                    steps=[
                        "1. İlaç Alımı: Misoprostolün mukozal yüzeylerden emilerek dolaşıma katılması",
                        "2. Servikal Yumuşama: Kolajenaz aktivasyonu ile servikal kanalın açılması",
                        "3. Myometrial Kasılma: Prostaglandin reseptörleriyle güçlü uterin krampların başlaması",
                        "4. Doku Ayrışması: Desidua ve fetoplasental elemanların uterus duvarından kopması",
                        "5. Doku Tahliyesi: Gebelik materyalinin servikal os üzerinden dışarı atılması"
                    ]
                ),
                make_recall(
                    question="Misoprostolün erken gebelik kaybındaki farmakolojik sınıfı ve iki temel fizyolojik etkisi nedir?",
                    answer="Sınıfı: Prostaglandin E1 (PGE1) analoğudur. İki temel etkisi: Servikal yumuşama/dilatasyon sağlama ve güçlü myometrial kontraksiyonlar oluşturmaktır."
                )
            ]
        ),

        # Slide 84
        make_slide(
            slide_num=84,
            title="Medikal Yönetim: Mifepriston (Antiprogesteron)",
            subtitle="Kombine Protokolün Biyokimyasal Mantığı ve Etki Mekanizması",
            clinical_focus="Mifepriston desiduayı nekroze eder ve uterusu prostaglandinlere duyarlı hale getirir.",
            narrative="""Medikal abortusta başarı oranını belirgin şekilde artıran diğer temel molekül mifepristondur. Ders notunda medikal yönetim kapsamında 'Mifepriston (antiprogesteron)' olarak tanımlanmıştır.

- **Moleküler Mekanizma:** Mifepriston bir nükleer progesteron reseptör antagonistidir. Progesteronun desidua üzerindeki destekleyici etkisini bloke eder.
- **Desidual Ayrılma:** Progesteron blokajı desiduada nekroza ve trofoblastik implantasyon bölgesinin ayrılmasına yol açar.
- **Uterin Duyarlılık:** Endojen ve ekzojen prostaglandinlere karşı myometrium duyarlılığını katbekat artırır.
- **Kombine Protokol:** Önce mifepriston verilip ardından misoprostol uygulandığında, tek başına misoprostole kıyasla komplet tahliye oranı çok daha yüksek seviyelere ulaşır.

> [!NOTE]
> Mifepriston bir antiprogesterondur; gebeliğin hormonal desteğini keserek desiduayı çözer ve myometriumu prostaglandin uyarısına hazır hale getirir.""",
            bullets=[
                "Mifepriston güçlü bir nükleer progesteron reseptör antagonistidir (antiprogesteron)",
                "Desidual nekroz oluşturur ve gebelik ürününün duvardan ayrılmasını başlatır",
                "Myometriumun prostaglandinlere (misoprostol) olan yanıtını ve kasılma şiddetini artırır"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre erken gebelik kaybının medikal tedavisinde misoprostol ile kombine edilebilen antiprogesteron etkili ajan hangisidir?",
                    options=[
                        {"key": "A", "text": "Danazol", "isCorrect": False, "explanation": "Zayıf androjen türevidir, antiprogesteron değildir."},
                        {"key": "B", "text": "Mifepriston", "isCorrect": True, "explanation": "Doğru. Ders notu Bölüm 9'da 'Mifepriston (antiprogesteron)' açıkça yazılıdır."},
                        {"key": "C", "text": "Letrozol", "isCorrect": False, "explanation": "Aromataz inhibitörüdür."},
                        {"key": "D", "text": "Klomifen sitrat", "isCorrect": False, "explanation": "Selektif östrojen reseptör modülatörüdür (SERM)."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notunda erken gebelik kaybında medikal yönetim için belirtilen Mifepriston farmakolojik olarak bir antiprogesteron moleküldür.",
                    masked_term="antiprogesteron",
                    hint="Progesteron hormon reseptörlerini bloke eden ilaç grubu"
                ),
                make_slider(
                    left_title="Mifepriston (Antiprogesteron)",
                    right_title="Misoprostol (Prostaglandin E1)",
                    left_points=[
                        "Progesteron reseptörlerini rekabetçi bloke eder",
                        "Desidual nekroz ve trofoblastik ayrılma sağlar",
                        "Myometriumun prostaglandin duyarlılığını artırır"
                    ],
                    right_points=[
                        "Prostaglandin EP reseptörlerini uyarır",
                        "Servikal kolajeni parçalayarak kanalı genişletir",
                        "Doğrudan güçlü myometrial kasılmalar oluşturur"
                    ]
                ),
                make_recall(
                    question="Mifepristonun medikal abortustaki farmakolojik etki sınıfı ve biyolojik rolü nedir?",
                    answer="Mifepriston bir antiprogesterondur. Progesteron reseptörlerini bloke ederek desidual nekroza neden olur ve myometriumu misoprostolün kasıcı etkisine karşı aşırı duyarlı hale getirir."
                )
            ]
        ),

        # Slide 85
        make_slide(
            slide_num=85,
            title="Cerrahi Yönetim: Dilatasyon ve Küretaj (D&C) ve Vakum Aspirasyon",
            subtitle="Mekanik Tahliye Yöntemleri, Endikasyonlar ve Komplikasyonlar",
            clinical_focus="Cerrahi tahliye acil kanamalarda ve enfekte uterus varlığında hayat kurtarıcı kesin yöntemdir.",
            narrative="""Erken gebelik kaybında cerrahi yöntemler kavite içeriğinin aletlerle doğrudan boşaltılmasını sağlar. Ders notunda cerrahi yöntemler olarak 'dilatasyon ve küretaj' ve 'vakum aspirasyon' tanımlanmıştır.

- **Vakum Aspirasyon (Manuel veya Elektrikli):** Plastik bir kanül (Karman kanülü) ve negatif basınç kaynağı kullanılarak kavite içeriği aspire edilir. Keskin küretaja göre uterus perforasyonu ve Asherman sendromu (sineşi) riski çok daha düşüktür.
- **Dilatasyon ve Keskin Küretaj (D&C):** Servikal kanal bujilerle dilate edildikten sonra keskin metal küretle endometrium kazınır. Aşırı kazıma bazal tabaka hasarına ve sineşilere yol açabilir.
- **Temel Cerrahi Endikasyonlar:** Ağır kontrolsüz hemoraji, hemodinamik şok, septik abortus, medikal tedavinin başarısız olması veya hastanın cerrahi istemesi.

> [!IMPORTANT]
> Cerrahi tahliyede vakum aspirasyon, doku travmasını ve gelecekteki intrauterin sineşi (Asherman sendromu) riskini keskin küretaja göre belirgin düzeyde azaltır.""",
            bullets=[
                "Ders notunda belirtilen cerrahi seçenekler: Dilatasyon & küretaj ve vakum aspirasyondur",
                "Vakum aspirasyon daha az travmatik olup perforasyon ve sineşi riskini azaltır",
                "Şiddetli kanama, hemodinamik instabilite veya septik abortusta cerrahi ilk tercihtir"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre erken gebelik kaybının cerrahi yönetiminde kullanılan mekanik tahliye yöntemleri hangi seçenekte doğru verilmiştir?",
                    options=[
                        {"key": "A", "text": "Yalnızca histerotomi ve myomektomi", "isCorrect": False, "explanation": "İnvaziv laparotomi işlemleridir, ilk trimester abortus cerrahisi değildir."},
                        {"key": "B", "text": "Radikal trakelektomi ve pelvik lenfadenektomi", "isCorrect": False, "explanation": "Jinekolojik onkoloji ameliyatıdır."},
                        {"key": "C", "text": "Yalnızca acil uterin arter embolizasyonu", "isCorrect": False, "explanation": "Mekanik kaviter tahliye yöntemi değildir."},
                        {"key": "D", "text": "Dilatasyon ve küretaj ile vakum aspirasyon", "isCorrect": True, "explanation": "Doğru. Ders notu Bölüm 9'da 'Cerrahi: dilatasyon ve küretaj, vakum aspirasyon' olarak tanımlanmıştır."}
                    ],
                    correct_key="D"
                ),
                make_cloze(
                    sentence="Ders notunda erken gebelik kaybının cerrahi yönetim seçenekleri arasında dilatasyon ve küretaj ile vakum aspirasyon yer almaktadır.",
                    masked_term="vakum aspirasyon",
                    hint="Negatif basınçlı kanül ile kavite içeriğini çekme tekniği"
                ),
                make_table(
                    title="Cerrahi Tahliye Yöntemlerinin Karşılaştırmalı Analizi",
                    headers=["Yöntem Adı", "Kullanılan Temel Ekipman", "Klinik Özellik ve Risk Profili"],
                    rows=[
                        [
                            {"text": "Vakum Aspirasyon", "isMasked": False},
                            {"text": "Kanül ve negatif basınç kaynağı", "isMasked": True, "hint": "Plastik boru ve emme vakum düzeneği"},
                            {"text": "Daha az travmatik, sineşi riski daha düşüktür", "isMasked": False}
                        ],
                        [
                            {"text": "Dilatasyon ve Küretaj (D&C)", "isMasked": False},
                            {"text": "Metal dilatatör ve keskin küret", "isMasked": True, "hint": "Kanal genişletici çubuk ve kazıyıcı kaşık"},
                            {"text": "Bazal tabaka hasarı ve Asherman riski taşır", "isMasked": False}
                        ]
                    ]
                ),
                make_recall(
                    question="Erken gebelik kaybında vakum aspirasyon yönteminin klasik keskin küretaja (D&C) kıyasla en önemli klinik avantajı nedir?",
                    answer="Vakum aspirasyon myometriuma ve bazalis tabakasına daha az mekanik hasar verir; bu sayede uterus perforasyonu ve işlem sonrası intrauterin sineşi (Asherman sendromu) riskini anlamlı ölçüde düşürür."
                )
            ]
        ),

        # Slide 86
        make_slide(
            slide_num=86,
            title="Yönetim Seçeneklerinin Karşılaştırmalı Değerlendirmesi",
            subtitle="Ekspektan, Medikal ve Cerrahinin Artı, Eksi ve Başarı Kriterleri",
            clinical_focus="Her yöntemin başarı oranı, komplikasyon profili ve hasta memnuniyeti farklıdır.",
            narrative="""Erken gebelik kaybında uygulanan üç yöntemin avantaj ve dezavantajları dengeli bir şekilde tartılmalıdır. Klinik kanıtlar her yöntemin kendine has güçlü yönleri olduğunu göstermektedir.

- **Cerrahi Tahliye:** En yüksek ve en hızlı komplet tahliye başarısına sahiptir (%95-99). İşlem dakikalar içinde tamamlanır; ancak anestezi riski, enfeksiyon, servikal hasar veya sineşi komplikasyonu barındırır.
- **Medikal Tedavi:** Cerrahiden kaçınmak isteyen hastalarda %80-90 başarı sağlar. Non-invazivdir; fakat kramp, kanama süresinin uzaması ve %10-15 olguda cerrahiye ihtiyaç duyulması dezavantajdır.
- **Ekspektan Yönetim:** Tamamen doğaldır ve hiçbir medikal ya da cerrahi yan etki taşımaz. Ancak sürecin ne zaman tamamlanacağı öngörülemez, başarı oranı daha düşüktür (%50-70) ve kanama uzayabilir.

> [!NOTE]
> Hasta hemodinamik olarak stabil olduğu sürece hangi yöntemin seçileceği, hekim ve hastanın ortak kararı ile belirlenir.""",
            bullets=[
                "Cerrahi yönetim en hızlı ve en yüksek kesin çözümü sunar",
                "Medikal yönetim cerrahi ve anestezi risklerini bertaraf eden non-invaziv bir seçenektir",
                "Ekspektan yaklaşım doğal atılım sağlar ancak süreç uzayabilir ve acil cerrahiye dönebilir"
            ],
            elements=[
                make_quiz(
                    question="Erken gebelik kaybı olan stabil bir hastada üç yönetim seçeneğinin karşılaştırılması ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                    options=[
                        {"key": "A", "text": "Bekleme-takip seçeneğinin başarı oranı %100 olup cerrahiden her zaman daha hızlı sonuç verir", "isCorrect": False, "explanation": "Yanlış. Bekleme-takip süreci haftalarca uzayabilir ve başarısı düşüktür."},
                        {"key": "B", "text": "Cerrahi tahliye en yüksek ve en hızlı komplet boşalma başarısına sahip olup acil hemorajide hayat kurtarıcıdır", "isCorrect": True, "explanation": "Doğru. Cerrahi tahliye %95+ kesin başarı sağlar ve acil durumlarda ilk tercihtir."},
                        {"key": "C", "text": "Medikal tedavide hiçbir zaman kramp veya kanama görülmez", "isCorrect": False, "explanation": "Yanlış. Prostaglandinler belirgin kramp ve kanama yapar."},
                        {"key": "D", "text": "Septik abortusta kesinlikle ekspektan yönetim uygulanmalıdır", "isCorrect": False, "explanation": "Yanlış. Septik abortusta ekspektan kontrendikedir, acil cerrahi şarttır."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notuna göre erken gebelik kaybında medikal yönetimde prostaglandin E1 analoğu olarak Misoprostol tercih edilmektedir.",
                    masked_term="prostaglandin E1",
                    hint="Kasıcı etkili farmakolojik molekül ailesi"
                ),
                make_venn(
                    title="Medikal Tedavi ve Cerrahi Tahliye Karşılaştırma Matrisi",
                    label_a="Medikal Yönetim (Misoprostol)",
                    label_b="Cerrahi Yönetim (Vakum / D&C)",
                    items=[
                        {"criterion": "Non-invaziv farmakolojik etki mekanizması", "correct": "A", "explanation": "İlaçla servikal efasman ve kontraksiyon uyarılır."},
                        {"criterion": "Uterus perforasyonu ve genel anestezi riski taşımaz", "correct": "A", "explanation": "Mekanik cerrahi invazyon içermez."},
                        {"criterion": "Dakikalar içinde en kesin ve en hızlı tahliyeyi sağlar", "correct": "B", "explanation": "Aletle kaviter materyal doğrudan boşaltılır."},
                        {"criterion": "Mekanik alet travması veya Asherman sineşisi riski taşır", "correct": "B", "explanation": "Özellikle keskin küretaj bazalis hasarı yapabilir."},
                        {"criterion": "Rh-negatif gebelerde Anti-D immünglobulin profilaksisi gerektirir", "correct": "both", "explanation": "Her iki yöntemde de fetomaternal transfüzyon riski vardır."},
                        {"criterion": "Sadece 20. haftadan sonraki canlı doğumlarda uygulanır", "correct": "neither", "explanation": "Her iki yöntem de erken gebelik kayıplarında uygulanır."}
                    ]
                ),
                make_recall(
                    question="Erken gebelik kaybında medikal yönetimin cerrahiye göre en temel avantajı nedir?",
                    answer="Cerrahi operasyon gereksinimini, genel anestezi risklerini, mekanik uterus perforasyonunu ve intrauterin sineşi oluşum riskini önlemesidir."
                )
            ]
        ),

        # Slide 87
        make_slide(
            slide_num=87,
            title="Alloimmünizasyon Riski ve Rh Uygunsuzluğu Patolojisi",
            subtitle="Fetomaternal Hemoraji, D Antijeni Duyarlaşması ve İmmün Yanıt",
            clinical_focus="Erken gebelik kaybındaki vajinal kanamalar Rh-negatif kadında fetomaternal immünizasyonu tetikleyebilir.",
            narrative="""Erken gebelik kayıplarında kanama ve doku ayrışması fetal eritrositlerin maternal dolaşıma sızmasına yol açabilir. Anne Rh-negatif (D-negatif) ve fetus Rh-pozitif (D-pozitif) olduğunda bu durum alloimmünizasyona zemin hazırlar.

- **D Antijeni İmmünojenitesi:** Rh sistemindeki D antijeni eritrosit yüzeyindeki en güçlü immünojenik proteindir. Maternal bağışıklık sistemi yabancı D antijenini tanıyarak anti-D antikorları üretir.
- **Primer İmmünizasyon:** İlk temasla önce IgM tipi antikorlar oluşur; ardından hafıza B hücreleri gelişerek plasentayı geçebilen yüksek afiniteli IgG antikorları sentezlenir.
- **Gelecek Gebelikler İçin Tehlike:** Bu gebelikte fetüs kaybedilse bile gelişen anne antikorları, bir sonraki Rh-pozitif gebelikte plasentayı geçerek fetusta hemolitik hastalık (Eritroblastozis fetalis) ve intrauterin ölüme neden olur.

> [!IMPORTANT]
> Erken gebelik kaybı geçiren her hastanın kan grubu ve Rh durumu ilk başvuruda mutlaka öğrenilmelidir.""",
            bullets=[
                "Rh-negatif anne ile Rh-pozitif fetal eritrositler arasındaki uyuşmazlıktır",
                "Fetomaternal sızıntı maternal dolaşımda anti-D antikor üretimini başlatır",
                "Duyarlaşma bir sonraki Rh-pozitif gebelikte fetal hemolitik hastalığa yol açar"
            ],
            elements=[
                make_quiz(
                    question="Rh-negatif bir gebenin abortus geçirmesi sırasında gelişebilecek Rh alloimmünizasyonu ile ilgili aşağıdaki patofizyolojik mekanizmalardan hangisi doğrudur?",
                    options=[
                        {"key": "A", "text": "Maternal dolaşıma sızan fetal D antijenleri annede kalıcı anti-D antikor sentezini tetikler", "isCorrect": True, "explanation": "Doğru. Fetomaternal kanama sonucu anne D antijenine karşı duyarlı hale gelir ve anti-D antikorları üretir."},
                        {"key": "B", "text": "Rh uyuşmazlığı sadece anne Rh-pozitif fetus Rh-negatif olduğunda görülür", "isCorrect": False, "explanation": "Tam tersidir; anne negatif, bebek pozitif olmalıdır."},
                        {"key": "C", "text": "İlk trimester kanamalarında hiçbir zaman fetomaternal kanama meydana gelmez", "isCorrect": False, "explanation": "Hafif kanamalar bile fetomaternal sızıntı yapabilir."},
                        {"key": "D", "text": "Alloimmünizasyon sadece trombosit yıkımına neden olan otoimmün bir hastalıktır", "isCorrect": False, "explanation": "Alloimmündir ve hedef fetal eritrositlerdir."}
                    ],
                    correct_key="A"
                ),
                make_cloze(
                    sentence="Ders notuna göre erken gebelik kaybında alloimmünizasyonu önlemek amacıyla Rh D immün globulin uygulaması yapılmalıdır.",
                    masked_term="Rh D immün globulin",
                    hint="Rh negatif duyarsızlaşmamış gebelere uygulanan koruyucu antikor preparatı"
                ),
                make_chain(
                    title="Fetomaternal Transfüzyon ve Alloimmünizasyon Basamakları",
                    steps=[
                        "1. Doku Hasarı: Abortus sürecinde koryonik villusların desiduadan ayrılması",
                        "2. Fetomaternal Kanama: Fetal Rh(+) eritrositlerin maternal venöz sinüslere sızması",
                        "3. Antijen Sunumu: Maternal dalak ve lenf nodlarında D antijeninin tanınması",
                        "4. Antikor Sentezi: B lenfositlerince anti-D antikorlarının (önce IgM, sonra IgG) üretilmesi",
                        "5. Gelecek Gebelik Riski: Maternal IgG'nin sonraki fetüse geçip eritroblastozis yapma potansiyeli"
                    ]
                ),
                make_recall(
                    question="Abortus sırasında Rh-negatif bir annede fetomaternal kanama gelişmesinin gelecekteki gebelikler açısından doğuracağı en büyük risk nedir?",
                    answer="Gelecekteki Rh-pozitif fetuslarda plasentayı geçen maternal anti-D (IgG) antikorlarının fetal eritrositleri parçalayarak fetal hemolitik hastalığa (eritroblastozis fetalis) yol açmasıdır."
                )
            ]
        ),

        # Slide 88
        make_slide(
            slide_num=88,
            title="Anti-D İmmün Globulin Profilaksisi: Zamanlama ve Doz Prensipleri",
            subtitle="İlk 72 Saat Kuralı, Birinci Trimester Dozu ve Koruma Mekanizması",
            clinical_focus="Rh-negatif duyarsızlaşmamış her abortus hastasına Anti-D immün globulin uygulanmalıdır.",
            narrative="""Ders notunun 10. bölümünde açıkça belirtildiği üzere erken gebelik kaybı ve kanamalarda 'Alloimmünizasyon: Rh D immün globulin uygulaması' esastır.

- **Koruma Mekanizması:** Dolaşıma giren az miktardaki fetal D-pozitif eritrositler, ekzojen verilen Anti-D immün globulin ile hızla kaplanır ve retiküloendotelyal sistemde anne bağışıklık sistemi uyarılmadan yok edilir.
- **Zamanlama Kuralı:** İdeal olarak fetomaternal kanamayı takip eden **ilk 72 saat içinde** uygulanmalıdır; ancak 72 saat aşılsa bile 28 güne kadar profilaksi yapılması önerilir.
- **Trimester Dozajı:** İlk trimester kayıplarında fetomaternal kanama hacmi küçük olduğundan 50 mcg (250 IU) mini doz Anti-D yeterlidir; 12. haftadan sonraki veya dozu belirsiz durumlarda standart 300 mcg (1500 IU) doz tercih edilir.
- **İndirekt Coombs:** Anneye Anti-D yapılmadan önce indirekt Coombs testi negatif olmalıdır (önceden duyarlaşmamış olmalıdır).

> [!IMPORTANT]
> Tüm erken gebelik kayıplarında (imminens, inkomplet, komplet, missed, cerrahi veya medikal tahliye) anne Rh-negatif ise Anti-D profilaksisi zorunludur.""",
            bullets=[
                "Ders notu gereği: 'Alloimmünizasyon: Rh D immün globulin uygulaması' şarttır",
                "Fetomaternal kanamadan sonraki ilk 72 saat içinde uygulanması esastır",
                "İlk 12 haftada 50 mcg mini doz yeterli kabul edilir, sonrasında standart 300 mcg kullanılır"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre erken gebelik kaybı yaşayan ve Rh-negatif olduğu bilinen duyarsızlaşmamış bir kadında alloimmünizasyonu önlemek için ne uygulanmalıdır?",
                    options=[
                        {"key": "A", "text": "Yüksek doz oral folik asit tedavisi", "isCorrect": False, "explanation": "Nöral tüp defekti profilaksisidir, alloimmünizasyonla ilgisi yoktur."},
                        {"key": "B", "text": "Rh D immün globulin uygulaması", "isCorrect": True, "explanation": "Doğru. Ders notunda 'Alloimmünizasyon: Rh D immün globulin uygulaması' açıkça belirtilmiştir."},
                        {"key": "C", "text": "Geniş spektrumlu oral tetrasiklin", "isCorrect": False, "explanation": "Enfeksiyon profilaksisidir, immünizasyonu önlemez."},
                        {"key": "D", "text": "Fetal eritrosit aferezi", "isCorrect": False, "explanation": "Uygulanamaz ve endike değildir."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notuna göre Rh-negatif gebelerde erken gebelik kaybı ve kanamalarda alloimmünizasyon riskine karşı Rh D immün globulin uygulaması yapılır.",
                    masked_term="Rh D immün globulin",
                    hint="Kırmızı kan hücresi sızıntısını etkisiz kılan koruyucu antikor"
                ),
                make_swipe(
                    title="Rh Profilaksisi Klinik Endikasyon Doğrulama Kartları",
                    left_category="Anti-D Gerekli",
                    right_category="Anti-D Gerekmez",
                    cards=[
                        {"text": "Anne Rh-negatif, baba Rh-pozitif, inkomplet abortus kanaması olan hasta", "category": "left", "explanation": "Fetomaternal transfüzyon ve duyarlaşma riski nedeniyle ilk 72 saatte uygulanmalıdır."},
                        {"text": "Anne Rh-negatif, missed abortus nedeniyle vakum aspirasyon yapılan hasta", "category": "left", "explanation": "Cerrahi tahliyede fetomaternal sızıntı riski yüksektir, profilaksi şarttır."},
                        {"text": "Anne Rh-negatif, abortus imminens tablosunda aktif vajinal kanaması olan gebe", "category": "left", "explanation": "Düşük tehdidinde kanama fetomaternal geçiş yapabileceğinden profilaksi gerekir."},
                        {"text": "Anne Rh-pozitif, eşi Rh-negatif olan erken gebelik kayıplı hasta", "category": "right", "explanation": "Anne zaten Rh-pozitif olduğundan D antijenine karşı duyarlaşamaz."},
                        {"text": "Anne Rh-negatif, eşi kesin olarak genetik kanıtlı Rh-negatif olan çift", "category": "right", "explanation": "Baba negatif olduğunda fetüs de kesinlikle Rh-negatiftir, antijen uyuşmazlığı yoktur."},
                        {"text": "Anne Rh-pozitif, missed abortus nedeniyle medikal tahliye alan hasta", "category": "right", "explanation": "Anne Rh-pozitiftir, Anti-D profilaksisi gerekmez."}
                    ]
                ),
                make_recall(
                    question="Rh-negatif gebelerde abortus sonrası Anti-D immün globulin uygulamasının ideal zamanlaması nedir?",
                    answer="Kanama veya müdahaleden sonraki ilk 72 saat içinde uygulanması esastır; fakat 72 saat geçse dahi 28 güne kadar uygulanması önerilmektedir."
                )
            ]
        ),

        # Slide 89
        make_slide(
            slide_num=89,
            title="Taburculuk, Takip ve Post-Abortus Danışmanlığı",
            subtitle="Enfeksiyon Takibi, Ovulasyonun Dönüşü ve Kontrasepsiyon",
            clinical_focus="Abortus sonrası fertilite hemen geri dönebilir; kontrasepsiyon ve psikolojik destek ihmal edilmemelidir.",
            narrative="""Erken gebelik kaybı tamamlandıktan sonra hastanın fiziksel ve psikolojik iyileşme süreci yakından yönetilmelidir. Müdahale veya atılım sonrası taburculuk kriterleri ve takip adımları belirlenmelidir.

- **Fiziksel İyileşme:** Kanamaların birkaç gün içinde lekelenmeye dönmesi ve 1-2 hafta içinde tamamen kesilmesi beklenir. Karın ağrısı gerilemelidir.
- **Ovulasyonun Geri Dönüşü:** Erken gebelik kaybından sonra ovulasyon ortalama **2 ila 4 hafta içinde** yeniden gerçekleşebilir. Bu nedenle hasta yeni bir gebelik planlamıyorsa hemen güvenilir bir kontraseptif yönteme başlanmalıdır.
- **Gelecek Gebelik Planı:** Enfeksiyon riski geçene kadar (yaklaşık 1-2 hafta) vajinal tampon ve cinsel ilişkiden kaçınılması önerilir. Yeni bir gebelik için genellikle hastanın normal bir menstrüel siklus görmesi tavsiye edilir.
- **Psikolojik Destek:** Erken kayıplar aile üzerinde yas, suçluluk ve anksiyete yaratır; empatik yaklaşım esastır.

> [!NOTE]
> Abortus sonrası ilk menstrüasyon genellikle 4-6 hafta içinde görülür; ancak ovulasyon çok daha erken (2. haftadan itibaren) başlayabilir.""",
            bullets=[
                "Ovulasyon abortusu takiben 2-4 hafta kadar erken bir sürede dönebilir",
                "İstenmeyen ardışık gebelikleri önlemek için etkili kontrasepsiyon hemen planlanmalıdır",
                "Ateş, şiddetli ağrı ve kötü kokulu akıntı varlığında enfeksiyon şüphesiyle acil kontrol gerekir"
            ],
            elements=[
                make_quiz(
                    question="Erken gebelik kaybı yaşayan bir kadında ovulasyonun geri dönüşü ve taburculuk sonrası danışmanlık ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                    options=[
                        {"key": "A", "text": "Abortus sonrası overler en az 1 yıl boyunca anovulatuar kalır", "isCorrect": False, "explanation": "Tamamen yanlıştır; ovulasyon 2-4 haftada dönebilir."},
                        {"key": "B", "text": "Ovulasyon işlemden sonraki 2-4 hafta gibi kısa bir sürede geri dönebileceğinden hemen kontrasepsiyon planlanmalıdır", "isCorrect": True, "explanation": "Doğru. Hızlı folikülogenez nedeniyle doğurganlık hızla geri döner."},
                        {"key": "C", "text": "Hastaya hemen ertesi gün intrauterin araç takılması ölümcül komplikasyondur", "isCorrect": False, "explanation": "Septik durum yoksa post-abortif RİA takılabilir."},
                        {"key": "D", "text": "Abortus sonrası hiçbir zaman psikolojik desteğe gerek duyulmaz", "isCorrect": False, "explanation": "Maternal kayıp ve yas reaksiyonu sıktır."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Erken gebelik kaybından sonra ovulasyon ortalama iki ila dört hafta içinde yeniden gerçekleşebilir.",
                    masked_term="iki ila dört hafta",
                    hint="Fertilitenin ve yumurtlamanın süratle geri döndüğü tahmini zaman aralığı"
                ),
                make_spot_the_lie(
                    topic="Erken gebelik kaybı sonrası hasta takibi ve klinik danışmanlık kuralları",
                    items=[
                        {"text": "Abortus sonrasında ovulasyon 2 ila 4 hafta kadar kısa bir sürede yeniden başlayabilir.", "isLie": False, "explanation": "Doğru fizyolojik gerçektir."},
                        {"text": "Rh-negatif ve eşi Rh-pozitif olan gebelerde Anti-D immün globulin yapılması gereksizdir.", "isLie": True, "explanation": "Tuzak! Anti-D uygulanması kritik bir zorunluluktur; yapılmazsa sonraki bebekte hemolitik hastalık riski doğar."},
                        {"text": "Hastada kötü kokulu pürülan akıntı veya yüksek ateş gelişmesi enfeksiyonu (septik tabloyu) düşündürür.", "isLie": False, "explanation": "Doğru uyarı işaretidir."},
                        {"text": "Vakum aspirasyon keskin küretaja göre uterus bazal tabakasını daha iyi korur.", "isLie": False, "explanation": "Doğru cerrahi üstünlüktür."}
                    ]
                ),
                make_recall(
                    question="Erken gebelik kaybı sonrası kontraseptif danışmanlığın derhal verilmesinin fizyolojik gerekçesi nedir?",
                    answer="Çünkü ovulasyon abortusu takiben 2 ila 4 hafta gibi çok erken bir sürede yeniden başlayabilir ve hasta farkında olmadan hızla tekrar gebe kalabilir."
                )
            ]
        ),

        # Slide 90 (Checkpoint 9)
        make_slide(
            slide_num=90,
            title="[TEKRAR SAYFASI - CHECKPOINT 9] Erken Gebelik Kaybında Yönetim ve Profilaksi Sentezi",
            subtitle="Bölüm 9 Kapsamlı Tekrarı: Tedavi Seçenekleri, İlaçlar, Cerrahi ve Rh Profilaksisi",
            clinical_focus="Erken gebelik kaybında üç tedavi seçeneği, misoprostol, mifepriston, cerrahi yöntemler ve Anti-D immün globulin sentezi.",
            narrative="""Bölüm 9 boyunca erken gebelik kayıplarında ders notunda tanımlanan tüm yönetim basamaklarını ve profilaktik yaklaşımları ayrıntısıyla inceledik. Bu checkpoint sayfası kazanımları pekiştirmeyi amaçlar.

- **Üç Temel Yönetim Seçeneği:** Bekleme-takip (ekspektan), medikal yönetim ve cerrahi yönetim (D&C, vakum aspirasyon).
- **Medikal Tedavi Ajanları:** Uterotonik ve servikal olgunlaştırıcı prostaglandin E1 analoğu olan **Misoprostol** ve nükleer progesteron reseptör antagonisti olan **Mifepriston**.
- **Cerrahi Seçenekler:** Mekanik kaviter boşaltma sağlayan dilatasyon ve küretaj (D&C) ile sineşi ve perforasyon riski daha düşük olan **vakum aspirasyon**.
- **Alloimmünizasyon Korunması:** Rh-negatif duyarsızlaşmamış annelerde fetomaternal transfüzyona bağlı anti-D antikor gelişimini engellemek için **Rh D immün globulin** uygulanması şarttır.

> [!IMPORTANT]
> Yönetim kararı hastanın hemodinamik stabilitesi, kanama şiddeti, enfeksiyon varlığı ve kişisel tercihi gözetilerek kişiselleştirilmelidir.""",
            bullets=[
                "Yönetim üç yoldan yürütülür: Bekleme-takip, medikal yönetim ve cerrahi yönetim",
                "Medikal ajanlar: Misoprostol (prostaglandin E1) ve Mifepriston (antiprogesteron)",
                "Cerrahi ajanlar: Dilatasyon ve küretaj ile vakum aspirasyon",
                "Rh-negatif gebelerde zorunlu profilaksi: Rh D immün globulin uygulaması"
            ],
            elements=[
                make_quiz(
                    question="Ders notu verilerine göre erken gebelik kaybı yönetimi ve profilaksisi ile ilgili aşağıdaki klinik ifadelerden hangisi YANLIŞTIR?",
                    options=[
                        {"key": "A", "text": "Medikal tedavide Misoprostol (PGE1) ve Mifepriston (antiprogesteron) kullanılır", "isCorrect": False, "explanation": "Doğrudur. Ders notundaki resmi medikal ajanlardır."},
                        {"key": "B", "text": "Cerrahi yönetimde dilatasyon ve küretaj ile vakum aspirasyon yer alır", "isCorrect": False, "explanation": "Doğrudur. Ders notundaki cerrahi yöntemlerdir."},
                        {"key": "C", "text": "Rh-negatif bir gebe erken gebelik kaybı geçirdiğinde Rh D immün globulin uygulamasına gerek yoktur", "isCorrect": True, "explanation": "Yanlış (Tuzak!). Ders notunda 'Alloimmünizasyon: Rh D immün globulin uygulaması' açıkça şart koşulmuştur."},
                        {"key": "D", "text": "Hemodinamik instabilite veya şiddetli kanamada bekleme-takip kontrendikedir", "isCorrect": False, "explanation": "Doğrudur. Acil cerrahi tahliye gerekir."}
                    ],
                    correct_key="C"
                ),
                make_cloze(
                    sentence="Ders notuna göre erken gebelik kaybının cerrahi yönetiminde dilatasyon ve küretaj ile birlikte vakum aspirasyon yöntemi kullanılır.",
                    masked_term="vakum aspirasyon",
                    hint="Plastik kanülle emme sağlayarak materyali tahliye eden cerrahi seçenek"
                ),
                make_table(
                    title="Bölüm 9 Yönetim ve Profilaksi Altın Standartlar Tablosu (Checkpoint 9)",
                    headers=["Klinik Kategori", "Ders Notu Resmi Tanımı / Ajanı", "Klinik Amaç ve Gerekçe"],
                    rows=[
                        [
                            {"text": "Medikal Tedavi (PGE1)", "isMasked": False},
                            {"text": "Misoprostol kullanımı", "isMasked": True, "hint": "Kasıcı uterotonik sentetik ajan"},
                            {"text": "Serviksi olgunlaştırıp kontraksiyon başlatma", "isMasked": False}
                        ],
                        [
                            {"text": "Medikal Tedavi (Hormonal)", "isMasked": False},
                            {"text": "Mifepriston kullanımı", "isMasked": True, "hint": "Antiprogesteron sınıfı molekül"},
                            {"text": "Desidual nekroz ve trofoblast ayrışması", "isMasked": False}
                        ],
                        [
                            {"text": "Cerrahi Tahliye", "isMasked": False},
                            {"text": "Dilatasyon küretaj ve vakum aspirasyon", "isMasked": True, "hint": "Mekanik kaviter cerrahi teknikler"},
                            {"text": "Kavitenin doğrudan aletlerle boşaltılması", "isMasked": False}
                        ],
                        [
                            {"text": "Alloimmünizasyon Önleme", "isMasked": False},
                            {"text": "Rh D immün globulin uygulaması", "isMasked": True, "hint": "Pasif antikor koruma enjeksiyonu"},
                            {"text": "Gelecek gebelikte fetal eritroblastozisi önleme", "isMasked": False}
                        ]
                    ]
                ),
                make_branching(
                    scenario="Acil servise 8 haftalık missed abortus tanısı alan, vajinal lekelenmesi olan, kan grubu A Rh-negatif, eşi A Rh-pozitif hemodinamik açıdan stabil bir gebe başvuruyor. İzlenecek klinik rota hangisidir?",
                    options=[
                        {
                            "text": "Hastaya yönetim seçenekleri (bekleme, medikal, cerrahi) anlatılarak ortak karar verilir ve alloimmünizasyonu önlemek amacıyla ilk 72 saatte Anti-D immün globulin uygulanır.",
                            "isCorrect": True,
                            "feedback": "Doğru yaklaşım. Stabil hastada seçenekler sunulur ve Rh profilaksisi asla ihmal edilmez."
                        },
                        {
                            "text": "Hasta Rh-negatif olduğu için derhal acil histerektomiye alınmalı ve Anti-D yapılmamalıdır.",
                            "isCorrect": False,
                            "feedback": "Yanlış. Histerektomi endikasyonu yoktur ve Anti-D yapılmaması ağır tıbbi hatadır."
                        },
                        {
                            "text": "Hasta evine gönderilmeli, kan grubu testi iptal edilmeli ve hiçbir tedavi veya takip planlanmamalıdır.",
                            "isCorrect": False,
                            "feedback": "Yanlış. Komplikasyon ve duyarlaşma riskini görmezden gelen hatalı yaklaşımdır."
                        }
                    ]
                ),
                make_recall(
                    question="Bölüm 9'un en kritik klinik spotu olan erken gebelik kaybı yönetim basamaklarını ve Rh kuralını özetleyiniz.",
                    answer="Yönetim seçenekleri bekleme-takip, medikal tedavi (Misoprostol - PGE1, Mifepriston - antiprogesteron) ve cerrahi tahliyedir (D&C, vakum aspirasyon). Anne Rh-negatif ise mutlaka Rh D immün globulin profilaksisi uygulanmalıdır."
                )
            ],
            is_checkpoint=True,
            checkpoint_number=9
        )
    ]
    return slides
