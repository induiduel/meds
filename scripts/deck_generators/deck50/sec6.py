from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec6():
    slides = []

    # Slide 51: Nörosifiliz Spektrumu ve En Sık Görülen Form: Asemptomatik Nörosifiliz
    slide51_text = """
    ## Nörosifiliz Spektrumu ve En Sık Görülen Form: Asemptomatik Nörosifiliz

    Nörosifiliz, *T. pallidum*'un merkezi sinir sistemini (MSS) istila etmesiyle gelişen tüm tabloları kapsar. Klasik olarak tersiyer dönemle ilişkilendirilse de, spiroketlerin MSS invazyonu hastalığın çok erken evrelerinde (primer/sekonder) başlar.

    Nörosifilizin en sık görülen klinik formu **Asemptomatik Nörosifiliz**'dir. Hastada hiçbir nörolojik şikayet yoktur, ancak beyin omurilik sıvısı (BOS) incelemesinde anormallikler (lenfositik pleositoz, yüksek protein ve pozitif VDRL) saptanır.

    > Nörosifiliz erken dönemde de başlayabilir ve çoğu olguda nörolojik semptom vermeyen, sadece BOS anormallikleriyle saptanan asemptomatik form en yaygın klinik tablodur.
    """
    slides.append(make_slide(
        title="Nörosifiliz Spektrumu ve En Sık Görülen Form: Asemptomatik Nörosifiliz",
        text=slide51_text,
        elements=[
            make_cloze("Nörosifilizin en sık görülen formu, hastanın klinik bulgu vermediği {{asemptomatik}} formdur."),
            make_cloze("Asemptomatik nörosifiliz tanısı, nörolojik muayene normalken {{BOS}} (beyin omurilik sıvısı) incelemesindeki anormalliklerle konur."),
            make_quiz(
                question="Nörosifiliz patogenezi hakkında hangisi doğrudur?",
                options=[
                    "Spiroketlerin MSS invazyonu sadece tersiyer evrede başlar.",
                    "En sık görülen form ağır demansla seyreden formdur.",
                    "Spiroketler MSS'ye daha primer veya sekonder evrede girebilir.",
                    "Asemptomatik formda BOS bulguları tamamen normaldir."
                ],
                answer="Spiroketler MSS'ye daha primer veya sekonder evrede girebilir.",
                explanation="MSS istilası hastalığın çok erken evrelerinde gerçekleşir ve en sık saptanan tablo asemptomatik BOS anormallikleridir."
            ),
            make_chain([
                "Erken evrede T. pallidum MSS'ye ulaşır...",
                "Klinik semptom yaratmadan inflamasyon başlar...",
                "Sadece BOS analizi (pleositoz, pozitif VDRL) ile asemptomatik nörosifiliz tanısı konur."
            ])
        ]
    ))

    # Slide 52: Meningovasküler Sifiliz: Endarteritis, İskemi ve Fokal Nörolojik Defisitler
    slide52_text = """
    ## Meningovasküler Sifiliz: Endarteritis, İskemi ve Fokal Nörolojik Defisitler

    Asemptomatik dönemi takip edebilen ilk semptomatik formlardan biri meningovasküler sifilizdir. Genellikle enfeksiyondan 5-10 yıl sonra görülür. Patolojik temelinde meningeal inflamasyon ve serebral damarlarda endarteritis obliterans (damar lümeninin daralması) yatar.

    Damar lümenindeki bu daralma beyin dokusunda iskemiye (enfarktlara) yol açar. Klinik olarak bu durum, genç veya orta yaşlı bir hastada inme (stroke), hemiparezi, afazi gibi akut fokal nörolojik defisitlerle kendini gösterir.

    > Meningovasküler sifiliz, MSS damarlarını etkileyen inflamatuvar vaskülite bağlı iskemik beyin enfarktları ve buna ikincil fokal nörolojik kayıplarla karakterizedir.
    """
    slides.append(make_slide(
        title="Meningovasküler Sifiliz: Endarteritis, İskemi ve Fokal Nörolojik Defisitler",
        text=slide52_text,
        elements=[
            make_cloze("Meningovasküler sifilizde serebral damarlarda gelişen inflamasyona {{endarteritis}} obliterans denir."),
            make_cloze("Damar lümeninin daralması beyinde {{iskemiye}} (enfarkta) yol açar, bu da inme benzeri tablolar oluşturur."),
            make_spot_lie(
                question="Meningovasküler sifiliz patolojisi hakkında hangisi yanlıştır (tuzaktır)? Odak: Klinik mekanizma",
                lies=[
                    "Temel sorun MSS'deki büyük gomların kitle etkisi yaratmasıdır."
                ],
                truths=[
                    "Serebral kan damarlarının inflamasyonu (endarteritis) esastır.",
                    "Damar tıkanıklığı beyinde iskemik enfarktlara neden olur.",
                    "Fokal nörolojik defisitler (ör: hemiparezi) iskeminin sonucudur."
                ],
                explanation="Meningovasküler sifilizin klinik bulguları gom kitlesinden değil, damar inflamasyonuna bağlı serebral iskemiden (inme) kaynaklanır.",
                isLie=True
            ),
            make_recall("Meningovasküler sifilizde genç hastada gelişebilen akut klinik tablo nedir?", "İskemiye bağlı inme (fokal nörolojik defisit, stroke).")
        ]
    ))

    # Slide 53: Parankimatöz Nörosifiliz: Kortikal Nöron Hasarı ve Demiyelinizasyon
    slide53_text = """
    ## Parankimatöz Nörosifiliz: Kortikal Nöron Hasarı ve Demiyelinizasyon

    Enfeksiyondan 10-20 yıl sonra, spiroketlerin beyin ve omurilik parankimine (kendi dokusuna) doğrudan hasar vermesiyle parankimatöz nörosifiliz gelişir. Bu evre asıl nörodejeneratif dönemdir.

    İki klasik tablosu vardır: Serebral korteksi tutan **Genel Parezi** ve medulla spinalis arka kordonunu tutan **Tabes Dorsalis**. Parankimatöz formlarda yaygın nöron ölümü, akson kaybı, mikroglial aktivasyon ve miyelin kılıf hasarı (demiyelinizasyon) gözlenir.

    > Parankimatöz nörosifiliz, *T. pallidum*'un uzun süreli varlığına bağlı olarak beyin korteksinde ve omurilikte kalıcı nöronal harabiyet ve demiyelinizasyon yarattığı ilerleyici tablodur.
    """
    slides.append(make_slide(
        title="Parankimatöz Nörosifiliz: Kortikal Nöron Hasarı ve Demiyelinizasyon",
        text=slide53_text,
        elements=[
            make_cloze("Parankimatöz nörosifilizde kortikal doku tutulumu {{Genel Parezi}}, omurilik arka kordon tutulumu ise {{Tabes Dorsalis}} olarak adlandırılır."),
            make_cloze("Parankimatöz evrede nöronal kayıp ve miyelin kılıf hasarına bağlı {{demiyelinizasyon}} ön plandadır."),
            make_table(
                headers=["Nörosifiliz Formu", "Tutulan Anatomik Bölge"],
                rows=[
                    ["Meningovasküler", "MSS Damarları (İskemi)"],
                    ["Genel Parezi", "Serebral Korteks (Beyin parankimi)"],
                    ["Tabes Dorsalis", "Medulla Spinalis Arka Kordonu"]
                ]
            ),
            make_recall("Beyin parankimi tutulumu sonucu gelişen kalıcı nöronal hasar tablosunun adı nedir?", "Genel Parezi (Paresis Generalis).")
        ]
    ))

    # Slide 54: Genel Parezi (Paresis Generalis): Kişilik Değişikliği, Paranoya ve Demans
    slide54_text = """
    ## Genel Parezi (Paresis Generalis): Kişilik Değişikliği, Paranoya ve Demans

    Genel parezi, frontal ve temporal loblardaki yaygın nöronal kayıp (atrofi) nedeniyle ortaya çıkan, ilerleyici bir zihinsel yıkım tablosudur. Hastalığın erken belirtileri hafıza kayıpları ve ince kişilik değişiklikleridir.

    Hastalık ilerledikçe megalomani (büyüklük hezeyanları), paranoya, emosyonel labilite, bozulmuş yargılama yeteneği ve nihayetinde derin bir demans tablosu gelişir. Psikiyatrik kliniği nedeniyle bu hastalar sıklıkla yanlışlıkla şizofreni veya bipolar bozukluk tanısı alabilir.

    > Genel parezi, sifilizin kortikal atrofisi sonucu oluşan; psikiyatrik hezeyanlar, kişilik değişimleri ve demans ile karakterize ciddi bir organik beyin sendromudur.
    """
    slides.append(make_slide(
        title="Genel Parezi (Paresis Generalis): Kişilik Değişikliği, Paranoya ve Demans",
        text=slide54_text,
        elements=[
            make_cloze("Genel parezi, özellikle frontal lob tutulumuna bağlı gelişen kişilik değişiklikleri ve kalıcı {{demans}} ile karakterizedir."),
            make_cloze("Genel parezili hastalarda büyüklük hezeyanları ({{megalomani}}) ve paranoya sık görülür."),
            make_quiz(
                question="Genel parezinin erken dönemlerinde en dikkat çekici bulgu hangisidir?",
                options=[
                    "Akut hemiparezi",
                    "Kişilik değişiklikleri ve bozulmuş yargılama",
                    "Derin koma hali",
                    "Spastik parapleji"
                ],
                answer="Kişilik değişiklikleri ve bozulmuş yargılama",
                explanation="Frontal lob korteksinin etkilenmesi öncelikle ince kişilik değişiklikleri, demans başlangıcı ve psikiyatrik bulgularla kendini gösterir."
            ),
            make_chain([
                "Frontal ve temporal kortekste nöron kaybı (atrofi)...",
                "Hafıza kusurları ve ince kişilik değişiklikleri başlar...",
                "Zamanla megalomani, paranoya ve ağır demansa ilerler."
            ])
        ]
    ))

    # Slide 55: Genel Parezide Refleks Hiperaktivitesi ve Motor Bozulmalar
    slide55_text = """
    ## Genel Parezide Refleks Hiperaktivitesi ve Motor Bozulmalar

    Genel parezi sadece zihinsel fonksiyonları bozmakla kalmaz, aynı zamanda kortikospinal yolların da etkilenmesiyle motor disfonksiyonlara neden olur. İstemsiz kas krampları, disartri (konuşma bozukluğu) ve elde, dilde, dudaklarda ince tremorlar gözlenir.

    Derin tendon reflekslerinde artış (hiperrefleksi) ve patolojik refleksler (Babinski pozitifliği) üst motor nöron hasarının klasik belirtileridir. Hastalar zamanla yatağa bağımlı (paretik) hale gelir.

    > Genel parezi tablosunda psikiyatrik semptomlara üst motor nöron lezyonu bulguları olan hiperrefleksi, tremor ve konuşma bozuklukları (disartri) eşlik eder.
    """
    slides.append(make_slide(
        title="Genel Parezide Refleks Hiperaktivitesi ve Motor Bozulmalar",
        text=slide55_text,
        elements=[
            make_cloze("Genel parezide üst motor nöron hasarına bağlı olarak derin tendon reflekslerinde {{artış}} (hiperrefleksi) görülür."),
            make_cloze("Hastalarda dilde ve dudaklarda tremor ile konuşma bozukluğu ({{disartri}}) tabloya eşlik eder."),
            make_spot_lie(
                question="Genel parezinin motor bulguları hakkında hangisi yanlıştır (tuzaktır)? Odak: Nöronal hasar tipi",
                lies=[
                    "Hastalarda derin tendon refleksleri tamamen kaybolur (arefleksi)."
                ],
                truths=[
                    "Üst motor nöron hasarı nedeniyle hiperrefleksi (artmış refleks) görülür.",
                    "Ellerde, dudaklarda ince tremorlar saptanır.",
                    "Kortikal yıkıma bağlı ilerleyici paretik (felç) tablo gelişir."
                ],
                explanation="Genel parezi kortikal (üst motor nöron) bir hasardır, bu nedenle refleksler kaybolmaz aksine artar (hiperrefleksi).",
                isLie=True
            ),
            make_recall("Genel parezide görülen konuşma bozukluğuna ne ad verilir?", "Disartri.")
        ]
    ))

    # Slide 56: Tabes Dorsalis Patofizyolojisi: Dorsal Kök Gangliyonları ve Arka Kordon Tutulumu
    slide56_text = """
    ## Tabes Dorsalis Patofizyolojisi: Dorsal Kök Gangliyonları ve Arka Kordon Tutulumu

    Tabes dorsalis, parankimatöz nörosifilizin medulla spinalis'i (omuriliği) tutan formudur. Patoloji, spiroketlerin dorsal kök gangliyonlarını (duyu sinirlerinin merkezleri) harap etmesiyle başlar.

    Bu harabiyet, omuriliğin arka (dorsal) kordonlarında ikincil demiyelinizasyon ve aksonal dejenerasyona (Wallerian dejenerasyon) yol açar. Arka kordonlar propriyosepsiyon (pozisyon duyusu) ve vibrasyon (titreşim) duyusunu taşıdığından, bu yolların kesilmesi duyu iletimini ciddi şekilde bozar.

    > Tabes dorsalis, omurilik arka kordonunun (dorsal kolon) dejenerasyonu ile karakterize olup, temel olarak kalın çaplı duyu liflerinin pozisyon ve vibrasyon duyusunu beyne taşıyamaması durumudur.
    """
    slides.append(make_slide(
        title="Tabes Dorsalis Patofizyolojisi: Dorsal Kök Gangliyonları ve Arka Kordon Tutulumu",
        text=slide56_text,
        elements=[
            make_cloze("Tabes dorsalis'te omuriliğin {{arka}} (dorsal) kordonlarında demiyelinizasyon gelişir."),
            make_cloze("Arka kordon hasarı, hastada pozisyon duyusu ({{propriyosepsiyon}}) ve vibrasyon duyusunun kaybına yol açar."),
            make_quiz(
                question="Tabes dorsalis'te hangi anatomik yapı primer olarak dejenere olur?",
                options=[
                    "Anterior (ön) boynuz motor nöronları",
                    "Dorsal (arka) kök gangliyonları ve kordonları",
                    "Kortikospinal traktus",
                    "Serebellar hemisferler"
                ],
                answer="Dorsal (arka) kök gangliyonları ve kordonları",
                explanation="Tabes dorsalis, dorsal kök gangliyonlarının harabiyeti ve arka kordon dejenerasyonu ile seyreder."
            ),
            make_chain([
                "Dorsal kök gangliyonları hasar görür...",
                "Omurilik arka kordonlarında demiyelinizasyon gelişir...",
                "Propriyosepsiyon (pozisyon) ve vibrasyon duyuları kaybolur."
            ])
        ]
    ))

    # Slide 57: Tabes Dorsalis Klinik Triadı: Şimşek Ağrıları, Parestezi ve Düşük Ayak
    slide57_text = """
    ## Tabes Dorsalis Klinik Triadı: Şimşek Ağrıları, Parestezi ve Düşük Ayak

    Arka köklerin uyarılması ve hasarı tabes dorsalis'in çok karakteristik klinik bulgularını yaratır. En erken ve en sık görülen semptom "şimşek ağrıları" (lightning pains) olarak bilinen, bacaklara ve karna saniyeler içinde aniden saplanan şiddetli, elektrik çarpması benzeri ağrılardır.

    Ayrıca hastalarda parestezi (karıncalanma, uyuşma) ve alt ekstremite derin tendon reflekslerinin kaybı (arefleksi) görülür. Eklem pozisyonunun hissedilememesi, yürüme paternini bozarak ayaklarını sertçe yere vurma (stepaj yürüyüşü) ihtiyacına neden olur.

    > Tabes dorsalis'in klasik bulguları; bacaklarda ani şimşek ağrıları, derin tendon arefleksisi ve zeminle teması hissedememeye bağlı gelişen atipik yürüyüş bozukluklarıdır.
    """
    slides.append(make_slide(
        title="Tabes Dorsalis Klinik Triadı: Şimşek Ağrıları, Parestezi ve Düşük Ayak",
        text=slide57_text,
        elements=[
            make_cloze("Tabes dorsalis'te bacaklara aniden saplanan şiddetli, kısa süreli ağrılara {{şimşek}} (lightning) ağrıları denir."),
            make_cloze("Arka kök hasarı nedeniyle bacaklarda derin tendon refleksleri kaybolur ({{arefleksi}} gelişir)."),
            make_table(
                headers=["Bulgu", "Patofizyolojik Neden"],
                rows=[
                    ["Şimşek Ağrıları", "Dorsal köklerin irritasyonu"],
                    ["Arefleksi", "Duyu refleks arkının kesilmesi"],
                    ["Stepaj Yürüyüşü", "Zeminle temasın (pozisyon) hissedilememesi"]
                ]
            ),
            make_recall("Tabes dorsalis'te refleksler artar mı azalır mı?", "Arka kök (duyu) hasarı nedeniyle azalır veya kaybolur (arefleksi).")
        ]
    ))

    # Slide 58: Duyusal Ataksi ve Pozitif Romberg Belirtisi
    slide58_text = """
    ## Duyusal Ataksi ve Pozitif Romberg Belirtisi

    Propriyosepsiyon (eklem pozisyon hissi) kaybı, hastaların uzaydaki konumlarını beyne iletememesine yol açar. Gözleri açıkken görme duyusu bu eksikliği telafi edebilir, ancak karanlıkta veya gözleri kapalıyken denge sağlanamaz. Buna duyusal ataksi denir.

    Klinikte bu durum **Romberg testi** ile gösterilir: Hasta ayaklarını bitişik tutarak ayakta dururken gözlerini kapattığında, dengesini kaybedip sendelemeye veya düşmeye başlar (Pozitif Romberg belirtisi).

    > Pozitif Romberg belirtisi, tabes dorsalis'te arka kordon harabiyetine bağlı gelişen duyusal ataksinin en klasik nörolojik muayene bulgusudur.
    """
    slides.append(make_slide(
        title="Duyusal Ataksi ve Pozitif Romberg Belirtisi",
        text=slide58_text,
        elements=[
            make_cloze("Tabes dorsalis hastasında, propriyosepsiyon eksikliğine bağlı gelişen denge kaybına {{duyusal ataksi}} denir."),
            make_cloze("Hasta gözlerini kapattığında dengesini kaybedip sendeliyorsa bu duruma pozitif {{Romberg}} belirtisi adı verilir."),
            make_spot_lie(
                question="Tabes dorsalis ve Romberg testi hakkında hangisi yanlıştır (tuzaktır)? Odak: Denge mekanizması",
                lies=[
                    "Romberg testi, vestibüler (iç kulak) hasarı saptamak için spesifiktir."
                ],
                truths=[
                    "Pozitif Romberg belirtisi propriyosepsiyon (arka kordon) kaybını gösterir.",
                    "Hasta gözleri açıkken vizüel destekle dengesini koruyabilir.",
                    "Ataksi motor değil, tamamen duyusal (pozisyon hissi kaybı) kaynaklıdır."
                ],
                explanation="Romberg testi propriyoseptif yolakları test eder; pozitifliği serebellar veya vestibüler değil, arka kordon (duyusal) hasarı gösterir.",
                isLie=True
            ),
            make_chain([
                "Arka kordon hasarı ile eklem pozisyon hissi kaybolur...",
                "Gözler kapatıldığında görsel telafi mekanizması ortadan kalkar...",
                "Hasta dengesini kaybeder (Pozitif Romberg Testi)."
            ])
        ]
    ))

    # Slide 59: Argyll Robertson Pupili: Işığa Yanıtsız, Uyum (Akomodasyon) Yapan Pupil
    slide59_text = """
    ## Argyll Robertson Pupili: Işığa Yanıtsız, Uyum (Akomodasyon) Yapan Pupil

    Nörosifiliz (özellikle tabes dorsalis ve genel parezi) için son derece patognomonik bir bulgu **Argyll Robertson pupili**'dir (Fahişenin Gözü olarak da bilinir). Bu durumda pupil, göze ışık tutulduğunda küçülmez (ışık refleksi kayıptır).

    Ancak hasta yakındaki bir nesneye odaklandığında pupil başarıyla küçülür (akomodasyon/uyum refleksi korunmuştur). Bu klinik fenomenin nedeni, midensefalonda (pretektal alan) ışık refleks yollarının hasar görmesi, ancak akomodasyon yollarının sağlam kalmasıdır.

    > Argyll Robertson pupili, ışığa yanıt vermeyen (miyozis olmayan) ancak uyum (akomodasyon) yapabilen tipik nörosifiliz göz bulgusudur; "uyum var, ışık yok" şeklinde akılda tutulur.
    """
    slides.append(make_slide(
        title="Argyll Robertson Pupili: Işığa Yanıtsız, Uyum (Akomodasyon) Yapan Pupil",
        text=slide59_text,
        elements=[
            make_cloze("Işık refleksinin kaybolduğu ancak uyum (akomodasyon) refleksinin korunduğu patolojik duruma {{Argyll Robertson}} pupili denir."),
            make_cloze("Bu pupil anormalliği, midensefalondaki {{pretektal}} alanın hasar görmesiyle ortaya çıkar."),
            make_quiz(
                question="Argyll Robertson pupilinin klasik tanımı aşağıdakilerden hangisidir?",
                options=[
                    "Hem ışığa hem de uyuma yanıt vermeyen dilated pupil",
                    "Işığa daralan ancak uyum yapamayan pupil",
                    "Işık refleksinin olmadığı ancak akomodasyonun (uyumun) olduğu pupil",
                    "Işıkta genişleyen, karanlıkta daralan pupil"
                ],
                answer="Işık refleksinin olmadığı ancak akomodasyonun (uyumun) olduğu pupil",
                explanation="Argyll Robertson pupilinde akomodasyon yolları sağlamdır ancak pretektal lezyon nedeniyle ışık refleksi alınamaz."
            ),
            make_recall("Argyll Robertson pupiline halk arasında verilen eski mecazi isim nedir?", "Fahişenin Gözü (uyum var, ışığa/tepkiye kapalı manasında).")
        ]
    ))

    # Slide 60: [TEKRAR SAYFASI - CHECKPOINT 6]
    slide60_text = """
    ## [TEKRAR SAYFASI - CHECKPOINT 6] Nörosifiliz, Genel Parezi ve Tabes Dorsalis

    Nörosifiliz, erken evreden geç evreye yayılan MSS tutulumlarıdır.
    Önemli kavramlar:
    - **Asemptomatik Form:** En sık görülen; sadece BOS bulguları (VDRL+, pleositoz).
    - **Meningovasküler Sifiliz:** Endarteritis, iskemi ve genç hastada inme.
    - **Genel Parezi:** Frontal kortikal atrofi; demans, hezeyan, hiperrefleksi.
    - **Tabes Dorsalis:** Arka kordon hasarı; şimşek ağrıları, arefleksi, pozitif Romberg (duyusal ataksi).
    - **Argyll Robertson Pupili:** Işık refleksi yok, akomodasyon var ("uyum var, ışık yok").
    """
    slides.append(make_slide(
        title="[TEKRAR SAYFASI - CHECKPOINT 6] Nörosifiliz, Genel Parezi ve Tabes Dorsalis",
        text=slide60_text,
        elements=[
            make_cloze("Meningovasküler sifilizde MSS damarlarındaki hasar beyinde {{iskemi}} ve inmeye yol açar."),
            make_cloze("Tabes dorsalis hastasında propriyosepsiyon kaybını gösteren ve gözler kapalıyken denge kaybıyla karakterize bulgu pozitif {{Romberg}} belirtisidir."),
            make_table(
                headers=["Form", "Klinik Özellik"],
                rows=[
                    ["Genel Parezi", "Kortikal nöron kaybı, demans, megalomani"],
                    ["Tabes Dorsalis", "Arka kök hasarı, şimşek ağrısı, arefleksi"],
                    ["Argyll Robertson Pupili", "Işığa yanıtsız, uyum yapabilen pupil"]
                ]
            ),
            make_recall("Argyll Robertson pupilinin en belirgin özelliği nedir?", "Işık refleksinin yokluğu, akomodasyon (uyum) refleksinin varlığı.")
        ]
    ))

    return slides
