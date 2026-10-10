# sec7.py
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec7():
    slides = []
    
    # Slide 61
    slides.append(
        make_slide(
            title="Kardiyovasküler Sifiliz Patogenezi: Vaza Vazorumların Endarteritis Obliteransı",
            narrative="""Kardiyovasküler sifiliz, sifilizin tersiyer döneminde görülen ve genellikle enfeksiyondan 10-30 yıl sonra ortaya çıkan yıkıcı bir komplikasyondur. Temel patolojik lezyon, büyük kan damarlarını, özellikle de aortu besleyen küçük damarlar olan *vaza vazorum*ların tutulumudur. 

Treponema pallidum'un neden olduğu kronik inflamasyon, vaza vazorumlarda **endarteritis obliterans** (lümeni daraltan veya tıkayan damar inflamasyonu) tablosuna yol açar. Vaza vazorumların lümeni daraldığında ve tıkandığında, aortun tunika media tabakası iskemik kalır. Bu durum, media tabakasındaki düz kas ve elastik liflerin harabiyetiyle sonuçlanır. 

> *Endarteritis obliterans*, sadece santral sinir sisteminde (meningovasküler nörosifiliz) değil, kardiyovasküler sistemde de ana patojenik mekanizmadır. Aort duvarının zayıflaması, kardiyovasküler sifilizin tüm klinik sonuçlarının (anevrizma, yetersizlik) başlangıç noktasıdır.""",
            interactions=[
                make_cloze("Kardiyovasküler sifilizin temel patolojisi, aortu besleyen küçük damarlar olan vaza vazorumlarda gelişen {{endarteritis obliterans}} tablosudur."),
                make_recall("Vaza vazorumların tıkanması aortun hangi tabakasında iskemi ve harabiyete yol açar?", "Tunika media tabakasında (düz kas ve elastik lif harabiyeti)."),
                make_quiz(
                    "Aşağıdakilerden hangisi kardiyovasküler sifilizin primer patojenik mekanizmasıdır?",
                    ["Aterosklerotik plak rüptürü", "Vaza vazorumların endarteritis obliteransı", "Miyokard hücrelerinin doğrudan invazyonu", "Endokardiyal fibrozis", "Konjenital kalp kapağı defekti"],
                    1,
                    "Doğru. Treponemalar vaza vazorumlarda endarteritis obliteransa neden olarak aort mediasında iskemiye yol açarlar."
                ),
                make_cloze("Vaza vazorum tıkanıklığı sonucu aortun {{tunika media}} tabakasındaki elastik lifler ve düz kas hücreleri yıkıma uğrar.")
            ]
        )
    )

    # Slide 62
    slides.append(
        make_slide(
            title="Asendan Aort (Çıkan Aort) Predileksiyonu ve Elastik Doku Yıkımı",
            narrative="""Kardiyovasküler sifiliz tipik olarak asendan aortayı (çıkan aortu) ve aort arkını tutar; desendan aort veya abdominal aort tutulumu çok nadirdir. Bunun nedeni, çıkan aortun vaza vazorumlardan çok daha zengin bir ağa sahip olmasıdır.

Asendan aortun tunika media tabakasındaki yoğun elastik lifler, endarteritis obliteransa bağlı iskemiden derin şekilde etkilenir. Normalde aorta esneklik sağlayan bu elastik doku harap olduğunda, yerini skar dokusu (fibrozis) alır. Bu fibrotik süreç, aort intimasında makroskopik olarak "ağaç kabuğu" (tree-bark) görünümü adı verilen kırışık ve düzensiz bir yüzey oluşturur.

> Çıkan aortun selektif tutulumu, kardiyovasküler sifilizi aterosklerozdan ayıran en önemli klinik ve patolojik özelliklerden biridir. Ateroskleroz daha çok abdominal aortu tutarken, sifiliz asendan aortu hedefler.""",
            interactions=[
                make_cloze("Kardiyovasküler sifiliz karakteristik olarak {{asendan}} (çıkan) aortayı tutar, çünkü bu bölge vaza vazorumlardan daha zengindir."),
                make_recall("Kardiyovasküler sifilizde elastik doku yıkımı ve fibrozis sonucu aort intimasında izlenen makroskopik görünüme ne ad verilir?", "Ağaç kabuğu (tree-bark) görünümü."),
                make_quiz(
                    "Sifilitik aortit ile aterosklerozun klasik lokalizasyon farkı hangi seçenekte doğru verilmiştir?",
                    ["Sifiliz abdominal aortu, ateroskleroz çıkan aortu tutar", "Sifiliz çıkan aortu, ateroskleroz abdominal aortu tutar", "Her ikisi de ağırlıklı olarak desendan aortu tutar", "Sifiliz sadece venleri, ateroskleroz arterleri tutar", "Sifiliz kapillerleri, ateroskleroz venülleri tutar"],
                    1,
                    "Doğru. Sifilitik aortit asendan aortayı hedeflerken, aterosklerotik anevrizmalar en sık abdominal aortta yerleşir."
                ),
                make_spot_lie(
                    "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilitik aort tutulumu",
                    [
                        {"text": "Sifiliz tipik olarak çıkan aortu (asendan aorta) ve aort arkını etkiler.", "isLie": False, "explanation": "Çıkan aorta, zengin vaza vazorum ağı nedeniyle sifilizin ana hedefidir."},
                        {"text": "Elastik doku kaybı sonucu aort intimasında ağaç kabuğu görünümü ortaya çıkar.", "isLie": False, "explanation": "Skarlanma ve büzüşme intima yüzeyinde bu tipik görünüme neden olur."},
                        {"text": "Kardiyovasküler sifilizde primer olarak desendan abdominal aort etkilenir.", "isLie": True, "explanation": "TUZAK! Abdominal aort aterosklerozun hedefidir, sifiliz ise asendan aortu (çıkan aort) tutar."}
                    ]
                )
            ]
        )
    )

    # Slide 63
    slides.append(
        make_slide(
            title="Sifilitik Aort Anevrizması Gelişimi ve Rüptür Tehlikesi",
            narrative="""Elastik doku yıkımı nedeniyle zayıflayan asendan aort duvarı, kan basıncının etkisiyle giderek genişler ve **sifilitik aort anevrizması** gelişir. Bu, tersiyer sifilizin en ölümcül komplikasyonlarından biridir.

Sifilitik anevrizmalar sıklıkla sakküler (kese şeklinde) veya füziform yapıda olabilir. Büyüyen anevrizma komşu yapılara bası yaparak semptom verebilir: trakea veya bronş basısına bağlı öksürük ve dispne, n. laryngeus recurrens basısına bağlı ses kısıklığı (Ortner sendromu) ve sternum ile kaburgaların erozyonuna bağlı inatçı göğüs ağrısı görülebilir. 

> En büyük risk, incelmiş anevrizma duvarının aniden yırtılmasıdır (rüptür). Sifilitik aort anevrizması rüptürü, masif iç kanama ve kardiyak tamponad veya hemotoraks nedeniyle genellikle hızla fatal sonuçlanır.""",
            interactions=[
                make_cloze("Elastik doku yıkımı sonucu duvarı zayıflayan çıkan aortta, tersiyer sifilizde {{sifilitik aort anevrizması}} gelişir."),
                make_recall("Sifilitik aort anevrizmasının n. laryngeus recurrens'e bası yapması sonucu hangi semptom ortaya çıkar?", "Ses kısıklığı (Ortner sendromu)."),
                make_chain([
                    {"q": "Endarteritis obliterans sonucu asendan aortun hangi tabakası harap olur?", "a": "Tunika media (elastik doku)"},
                    {"q": "Zayıflayan duvar kan basıncıyla genişleyince ne oluşur?", "a": "Sifilitik aort anevrizması"},
                    {"q": "Anevrizmanın en korkulan ve ölümcül komplikasyonu nedir?", "a": "Rüptür (yırtılma)"}
                ]),
                make_quiz(
                    "Asendan aort anevrizmasının sternum ve kosta erozyonu yapması sonucu klinikte hangi bulgu en belirgin şekilde ortaya çıkar?",
                    ["Bradikardi", "Kemik erozyonuna bağlı şiddetli ve inatçı göğüs ağrısı", "Siyanoz", "Peteşiyal döküntü", "İleus"],
                    1,
                    "Doğru. Anevrizmanın çevre kemik dokuları aşındırması tipik olarak inatçı, kemik kaynaklı göğüs ağrısına yol açar."
                )
            ]
        )
    )

    # Slide 64
    slides.append(
        make_slide(
            title="Aort Halkası Dilatasyonu ve İleri Derece Aort Yetersizliği",
            narrative="""Sifilitik aortit asendan aort köküne (aort kapağının bağlandığı halkaya) yayıldığında, aort anulusu (halkası) genişler. Bu dilatasyon, aort kapakçıklarının (küspislerin) diyastol sırasında tam kapanamamasına neden olur. 

Sonuç olarak, **ileri derece aort yetersizliği (regürjitasyonu)** gelişir. Sol ventrikül, diyastolde aorttan geri kaçan devasa kan volümüyle başa çıkmak için eksantrik olarak hipertrofiye uğrar ve genişler (Cor bovinum - sığır kalbi görünümü). Bu volüm yükü hızla sol kalp yetersizliğine doğru ilerler.

> Kardiyovasküler sifilizde kapakçıkların kendisi doğrudan mikroorganizma tarafından yıkıma uğramaz; sorun, kapağın tutunduğu halkanın (aort kökünün) genişleyip kapakların birbirinden uzaklaşmasıdır (komissürlerin ayrılması).""",
            interactions=[
                make_cloze("Aort kökünün genişlemesi sonucu kapakların kapanamamasıyla sifilizde {{aort yetersizliği}} (regürjitasyonu) gelişir."),
                make_recall("Aort yetersizliğine bağlı oluşan sol ventrikülün devasa genişlemesine ne ad verilir?", "Cor bovinum (sığır kalbi)."),
                make_quiz(
                    "Sifilitik kalp hastalığında aort yetersizliği gelişmesinin temel mekanizması nedir?",
                    ["Kapak yaprakçıklarında vejetasyon oluşumu", "Aort anulusunun (kökünün) dilatasyonu", "Kapakçıkların kalsifiye olup stenoz yapması", "Papiller kas rüptürü", "Korda tendineaların kopması"],
                    1,
                    "Doğru. Sifilizde kapakçıklar doğrudan hasar görmez, kapağın oturduğu aort kökü genişlediği için kapaklar kapanamaz."
                ),
                make_cloze("Aort yetersizliği nedeniyle sol ventrikülde aşırı volüm yüklenmesi zamanla sol {{kalp yetersizliğine}} yol açar.")
            ]
        )
    )

    # Slide 65
    slides.append(
        make_slide(
            title="Koroner Arter Ostium Stenozu ve Sifilitik Anjina",
            narrative="""Sifilitik aortitin bir diğer önemli ve yaşamı tehdit eden sonucu, inflamasyonun aort kökündeki koroner arter çıkış deliklerini (ostiumları) daraltmasıdır. 

Koroner ostiumların skar dokusu ve kalınlaşmış intima (ağaç kabuğu görünümü) tarafından daraltılmasına **koroner ostiyal stenoz** denir. Bu durum, koroner arterlerin dallarından ziyade tam çıkış noktalarını tıkar. Hastalarda, miyokardiyal iskemiye bağlı olarak tipik veya atipik anjina pektoris gelişir; miyokard enfarktüsü riski artar. 

> Sifilitik koroner tutulum, aterosklerotik koroner arter hastalığından farklıdır. Ateroskleroz sıklıkla koroner damarların trasesi boyunca tıkanıklık yaparken, sifiliz sadece koroner arterlerin aorttan ayrıldığı noktayı (ostiumu) daraltır.""",
            interactions=[
                make_cloze("Sifilitik aortitin koroner arter çıkış noktalarını daraltması tablosuna {{koroner ostiyal stenoz}} adı verilir."),
                make_recall("Sifilize bağlı koroner ostium darlığı miyokardiyal iskemi yaparak hangi klasik semptoma yol açar?", "Anjina pektoris."),
                make_table(
                    "Sifilitik ve Aterosklerotik Koroner Tutulum Farkı",
                    ["Özellik", "Sifilitik Tutulum", "Aterosklerotik Tutulum"],
                    [
                        ["Tıkanıklık Yeri", "Sadece koroner ostium (çıkış deliği)", "Koroner arter dalları boyunca"],
                        ["Mekanizma", "İntimal fibrozis ve skarlanma", "Aterom plağı oluşumu"],
                        ["İlişkili Aort Patolojisi", "Çıkan aort anevrizması", "Abdominal aort anevrizması"]
                    ]
                ),
                make_quiz(
                    "Tersiyer sifilizi olan bir hastada şiddetli anjina pektoris atakları başlamıştır. Bu durumun en olası sifilitik nedeni nedir?",
                    ["Koroner arterlerin distal dallarında vaskülit", "Koroner ostiumların daralması (ostiyal stenoz)", "Miyokard içinde doğrudan granülom oluşumu", "Endokardit pıhtılarının koronerleri tıkaması", "Aortik diseksiyon"],
                    1,
                    "Doğru. Sifilitik aortit aort kökünde fibrozis yaparak koroner ostiumları daraltır ve iskemik kalp hastalığına (anjina) neden olur."
                )
            ]
        )
    )

    # Slide 66
    slides.append(
        make_slide(
            title="Çıkan Aort Duvarında Doğrusal Kalsifikasyonun Radyolojik Değeri",
            narrative="""Kardiyovasküler sifiliz yıllar içinde ilerledikçe, hasarlı aort duvarında distrofik kalsifikasyon birikimi başlar. Çıkan aortun (asendan aort) duvarında ince, doğrusal bir kireçlenme (lineer kalsifikasyon) radyolojik olarak saptanabilir. 

Basit bir akciğer grafisinde (tele radyografi) çıkan aort trasesinde görülen bu kalsifikasyon, aksi ispat edilene kadar sifilitik aortiti düşündürmelidir. Ateroskleroz da aortta kalsifikasyon yapabilir, ancak bu genellikle aort topuzu (arkus aort) veya inen (desendan) aortta daha belirgindir. 

> Çıkan aortun izole kalsifikasyonu, özellikle aort anevrizması eşlik ediyorsa, kardiyovasküler sifiliz tanısı için güçlü bir klinik ipucudur.""",
            interactions=[
                make_cloze("Akciğer grafisinde {{çıkan}} (asendan) aort duvarında izlenen doğrusal kalsifikasyon sifilitik aortiti düşündürür."),
                make_recall("Hasarlı dokuda kalsiyum çökmesi sonucu oluşan ve sifilitik aortitte görülen radyolojik bulgu nedir?", "Doğrusal (lineer) kalsifikasyon."),
                make_spot_lie(
                    "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifiliz radyolojisi",
                    [
                        {"text": "Sifilitik aortitte asendan aort duvarında distrofik kalsifikasyon gelişebilir.", "isLie": False, "explanation": "Evet, hasarlı elastik doku üzerinde lineer kalsifikasyon birikir."},
                        {"text": "Akciğer grafisinde çıkan aort trasesindeki kireçlenme sifiliz açısından ipucudur.", "isLie": False, "explanation": "Bu bulgu özellikle sifilitik aortit için oldukça spesifik kabul edilir."},
                        {"text": "Aterosklerotik kalsifikasyonlar genellikle asendan aortu tutarken sifiliz desendan aortu tutar.", "isLie": True, "explanation": "TUZAK! Tam tersidir. Sifiliz asendan aortu, ateroskleroz ise desendan/abdominal aortu ve aort topuzunu kalsifiye eder."}
                    ]
                ),
                make_cloze("Hasarlı dokuda kan kalsiyum düzeyi normalken gelişen bu kireçlenmeye genel patolojide {{distrofik}} kalsifikasyon denir.")
            ]
        )
    )

    # Slide 67
    slides.append(
        make_slide(
            title="Kardiyovasküler Sifilizde Klinik Seyir ve Kalp Yetersizliği",
            narrative="""Kardiyovasküler sifilizin klinik tablosu genellikle uzun bir asemptomatik dönemin (10-30 yıl) ardından sessizce, fakat dramatik biçimde ortaya çıkar. Hastalar genellikle nefes darlığı (dispne), göğüs ağrısı (anjina) ve çarpıntı şikayetleriyle hekime başvururlar. 

Kapak halkası genişlemesine bağlı aort yetersizliği ilerledikçe sol ventrikül iflas eder ve dekompanse sol kalp yetersizliği bulguları (ortopne, paroksismal noktürnal dispne, akciğer ödemi) gelişir. Anevrizmanın trakea veya bronşlara basısı ise stridor ve inatçı öksürük yapabilir. 

> Erken dönemde sifiliz tedavisi (penisilin) kardiyovasküler sifiliz gelişimini tamamen önleyebilir; ancak anevrizma veya aort yetersizliği oluştuktan sonra antibiyotik tedavisi oluşan yapısal hasarı geri döndüremez. Bu aşamada cerrahi onarım şarttır.""",
            interactions=[
                make_cloze("Kardiyovasküler sifilizde ileri derece aort yetersizliği sonucu en sık gelişen nihai tablo sol {{kalp yetersizliği}}dir."),
                make_recall("Kardiyovasküler tutulum oluştuktan sonra yapısal hasar antibiyotikle (penisilin) geri döndürülebilir mi?", "Hayır, oluşan yapısal hasar geri döndürülemez (cerrahi gerekir)."),
                make_chain([
                    {"q": "Aort kökü genişleyip kapaklar kapanamayınca ne oluşur?", "a": "Aort yetersizliği"},
                    {"q": "Aort yetersizliği nedeniyle aşırı hacim yüklenen kalp odacığı neresidir?", "a": "Sol ventrikül"},
                    {"q": "Sol ventrikül kompanzasyon yeteneğini kaybedince ne gelişir?", "a": "Sol kalp yetersizliği"}
                ]),
                make_quiz(
                    "Tersiyer dönem kardiyovasküler sifilizi olan ve dev anevrizması bulunan bir hastaya verilen penisilin tedavisinin temel amacı nedir?",
                    ["Anevrizmayı küçültmek", "Kopmuş elastik lifleri yenilemek", "Aktif treponemal enfeksiyonu durdurup hasarın ilerlemesini engellemek", "Aort kapaklarını cerrahi olmadan tamir etmek", "Koroner ostium darlığını mekanik olarak açmak"],
                    1,
                    "Doğru. Penisilin sadece mikroorganizmaları öldürüp süreci durdurur, ancak daha önce oluşmuş anatomik yıkımı tamir edemez."
                )
            ]
        )
    )

    # Slide 68
    slides.append(
        make_slide(
            title="Kardiyovasküler Sifilizde Spiroketemi ve Bulaştırıcılık Durumu (Bulaş Yoktur)",
            narrative="""Tersiyer sifiliz (kardiyovasküler sifiliz, nörosifiliz ve gomlar dahil) aşamasında vücuttaki Treponema pallidum sayısı son derece düşüktür. Sifilizin bu geç döneminde artık aktif bir spiroketemi (kanda bakteri dolaşımı) yoktur. 

Bu durumun klinik açıdan en önemli sonucu şudur: Kardiyovasküler sifilizli bir hastanın açık lezyonu (şankr veya kondilom) yoktur ve kanı veya dokuları yoluyla cinsel temasla hastalığı başkasına **bulaştırmaz**. Hastalığın bu evresi, immün sistemin kalıcı bir aşırı duyarlılık (hipersensitivite) reaksiyonu ve kronik doku yıkımı dönemidir. 

> Primer ve sekonder sifiliz çok bulaşıcıyken, tersiyer sifiliz (kardiyovasküler form dahil) non-enfeksiyöz (bulaştırıcı olmayan) kabul edilir.""",
            interactions=[
                make_cloze("Tersiyer sifiliz formlarında (kardiyovasküler sifiliz dahil) hastaların cinsel yolla {{bulaştırıcılığı}} yoktur."),
                make_recall("Tersiyer evrede kanda aktif olarak T. pallidum bulunmamasına (bakteriyemi olmamasına) ne ad verilir?", "Spiroketemi yoktur."),
                make_quiz(
                    "Kardiyovasküler sifilizi olan 65 yaşındaki bir hastanın eşine cinsel yolla bulaştırma riski için aşağıdakilerden hangisi doğrudur?",
                    ["Risk primer evreden bile daha yüksektir", "Hastada kondiloma lata gelişirse bulaşabilir", "Spiroketemi olduğu için bulaştırıcılık devam eder", "Tersiyer evre bulaştırıcı olmadığı için risk yoktur", "Sadece aort rüptürü anında bulaş olur"],
                    1,
                    "Doğru. Tersiyer evrede organizma sayısı çok azdır ve hastalık başkalarına bulaşmaz."
                ),
                make_cloze("Tersiyer evredeki yıkım esas olarak mikroorganizmanın doğrudan toksisitesinden çok, konağın {{immün}} yanıtı (hipersensitivite) nedeniyledir.")
            ]
        )
    )

    # Slide 69
    slides.append(
        make_slide(
            title="Tersiyer Dönemde Nörosifiliz ve Kardiyovasküler Tutulumun Birlikteliği",
            narrative="""Tersiyer sifilizin alt tipleri olan kardiyovasküler sifiliz ve nörosifiliz, her zaman birbirini dışlayan durumlar değildir. Klinik pratikte, kardiyovasküler sifilizi olan hastaların önemli bir bölümünde eşzamanlı asemptomatik veya semptomatik **nörosifiliz** de saptanabilir. 

Bu nedenle, kardiyovasküler sifiliz teşhisi konan her hastanın beyin omurilik sıvısı (BOS) incelemesi dahil olmak üzere nörosifiliz açısından da dikkatle değerlendirilmesi önerilir. Her iki tutulum da temelde vaza vazorumları ve meningeal damarları hedef alan *endarteritis obliterans* mekanizmasını paylaşır.

> Sifilizin geç dönemi sistemik bir vasküler enflamasyon halidir; aort tutulumu (kardiyovasküler) ve SSS damar tutulumu (meningovasküler) bir arada görülebilir.""",
            interactions=[
                make_cloze("Kardiyovasküler sifilizi olan hastalarda aynı zamanda {{nörosifiliz}} (SSS tutulumu) de bulunabileceğinden dikkatli olunmalıdır."),
                make_recall("Kardiyovasküler ve nörolojik tutulumun ortak vasküler patolojik mekanizması nedir?", "Endarteritis obliterans."),
                make_quiz(
                    "Kardiyovasküler sifiliz tanısı alan bir hastada, eşlik edebilecek geç dönem tutulumunu dışlamak için hangi sıvının incelenmesi önem taşır?",
                    ["Plevral sıvı", "BOS (Beyin Omurilik Sıvısı)", "Perikardiyal sıvı", "Eklem sıvısı", "Asit sıvısı"],
                    1,
                    "Doğru. Nörosifiliz birlikteliğini dışlamak için BOS incelemesi yapmak gerekebilir."
                ),
                make_cloze("Tersiyer dönem, hem aort hem de beyin zarı damarlarını etkileyebilen sistemik bir {{vasküler}} enflamasyon sürecidir.")
            ]
        )
    )

    # Slide 70
    slides.append(
        make_slide(
            title="[TEKRAR SAYFASI - CHECKPOINT 7] Kardiyovasküler Sifiliz ve Endarteritis Obliterans",
            narrative="""Bu bölümde kardiyovasküler sifilizin ölümcül ve dramatik patolojisini inceledik.

- **Mekanizma**: Vaza vazorumlarda endarteritis obliterans ve mediasal iskemi (elastik doku yıkımı).
- **Yerleşim**: Karakteristik olarak *çıkan (asendan) aorta* tutulur.
- **Klinik Sonuçlar**:
  - *Aort Anevrizması*: Rüptür riski yüksektir.
  - *Aort Yetersizliği*: Aort kökü genişler (kapaklar sağlamdır ama ayrılır), sol kalp yetmezliği ve cor bovinum gelişir.
  - *Koroner Ostiyal Stenoz*: Aort kökündeki fibrozis koroner çıkışlarını daraltır, sifilitik anjina gelişir.
- **Bulgular**: Asendan aortta doğrusal kalsifikasyon (ağaç kabuğu görünümü).
- **Özellikler**: Tersiyer evrede olduğu için bulaştırıcı DEĞİLDİR. Sıklıkla nörosifiliz eşlik edebilir.

İlerleyen bölümde sifilizin laboratuvar tanısına (Karanlık Saha ve Nontreponemal testler) giriş yapacağız.""",
            interactions=[
                make_table(
                    "Kardiyovasküler Sifiliz Özet Tablosu",
                    ["Patoloji", "Etkilenen Yapı", "Klinik Sonuç"],
                    [
                        ["Elastik doku yıkımı", "Asendan aort", "Anevrizma ve rüptür"],
                        ["Aort kökü dilatasyonu", "Aort kapak halkası", "Aort yetersizliği ve kalp yetmezliği"],
                        ["Fibrozis / Ağaç kabuğu", "Koroner ostium", "Anjina pektoris"]
                    ]
                ),
                make_cloze("Sifilitik aortit, vaza vazorumların tıkanmasına yani {{endarteritis obliterans}} patolojisine dayanır."),
                make_recall("Kardiyovasküler sifiliz en sık aortun hangi bölgesini tutar?", "Asendan (çıkan) aort."),
                make_spot_lie(
                    "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kardiyovasküler sifiliz sonuçları",
                    [
                        {"text": "Aort anevrizması komşu yapılara bası (ör. n. laryngeus recurrens) yapabilir.", "isLie": False, "explanation": "Evet, bu bası ses kısıklığına (Ortner sendromu) yol açabilir."},
                        {"text": "Aort kapakçıkları bizzat T. pallidum tarafından yıkıldığı için aort stenozu (darlığı) gelişir.", "isLie": True, "explanation": "TUZAK! Kapaklar yıkılmaz, aort kökü genişlediği için kapaklar birbirinden uzaklaşır ve aort YETERSİZLİĞİ gelişir."},
                        {"text": "Hastalığın bu aşamasında hasta cinsel temasla enfeksiyonu eşine bulaştırmaz.", "isLie": False, "explanation": "Tersiyer sifiliz bulaştırıcı değildir."}
                    ]
                )
            ]
        )
    )

    return slides
