# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-12-s71",
        "title": "Trombosit Aktive Edici Faktör (PAF): Yapı ve Kaynakları",
        "content": "Trombosit Aktive Edici Faktör (PAF), membran fosfolipidlerinden türetilen bioaktif bir fosfolipiddir (kimyasal yapısı asetil-gliseril-eter-fosforilkolindir). Fosfolipaz A2'nin membran alkil-açil fosfatidilkolini parçalamasıyla açığa çıkan lizo-PAF'ın asetiltransferaz enzimiyle asetillenmesi sonucu sentezlenir. Geniş bir hücre yelpazesi tarafından üretilir:\n\n- Trombositler, bazofiller, mast hücreleri, nötrofiller, monosit/makrofajlar ve vasküler endotel hücreleri.\n\nPAF, hedef hücrelerin plazma zarında bulunan tek bir G-protein kenetli reseptör (PAFR) üzerinden olağanüstü geniş bir biyolojik yanıt yelpazesini tetikler. Enflamasyondaki önemi hem vasküler tonusu düzenlemesinden hem de lökositleri en yüksek düzeyde aktive eden pleiotropik bir sinyal molekülü olmasından kaynaklanır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Trombosit aktive edici faktör membran fosfolipidlerinden fosfolipaz A2 ve asetiltransferaz enzimleriyle sentezlenen biyoaktif bir lipid mediyatördür.",
                "Trombosit aktive edici faktör",
                "PAF kısaltmasının açık Türkçe adı"
            ),
            make_recall(
                "PAF'ın prekürsörü olan lizo-PAF'ı hücre membranından koparan eikozanoid yolağının da ortak enzimi hangisidir?",
                "Fosfolipaz A2'dir (PLA2).",
                "Fosfolipid parçalayan temel lipaz"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-12-s72",
        "title": "PAF'ın Çift Fazlı Vasküler ve Bronşiyal Etkileri",
        "content": "PAF'ın biyolojik etkileri lokal doku konsantrasyonuna ve hedef organa göre dramatik farklılıklar sergiler:\n\n1. **Vasküler Permeabilite Artışı:** Aşırı düşük (pikomolar) konsantrasyonlarda dahi postkapiller venüllerde endotel kasılması yapar; venüler geçirgenliği artırma gücü **histaminden 10.000 kat daha fazladır**.\n2. **Vazodilatasyon ve Hipotansiyon:** Düşük dozlarda endotelden nitrik oksit salarak güçlü arterioler vazodilatasyona yol açar; anaflaktik şoktaki ani tansiyon düşüşünün majör tetikleyicilerindendir.\n3. **Trombosit Agregasyonu ve Vazokonstriksiyon:** Yüksek konsantrasyonlarda trombositleri hızla degranüle edip kümeleştirir ve hasarlı damarı büzer.\n4. **Bronkokonstriksiyon:** Bronş düz kaslarını kuvvetle kasarak inatçı hava yolu obstrüksiyonu yapar.\n5. **Lökosit Aktivasyonu:** Nötrofillerin integrin adezyonunu, kemotaksisini, degranülasyonunu ve oksidatif patlamasını uyarır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "PAF Konsantrasyona Bağımlı Etkiler",
                "Düşük (Pikomolar) Konsantrasyon",
                "Histaminden 10.000 kat güçlü venüler permeabilite artışı ve sistemik vazodilatasyon yapar.",
                "Yüksek Konsantrasyon",
                "Güçlü trombosit agregasyonu, vazokonstriksiyon ve şiddetli bronkospazm oluşturur."
            ),
            make_quiz(
                "Postkapiller venüllerde mikrovasküler geçirgenliği artırma potansiyeli histaminden yaklaşık 10.000 kat daha güçlü olan fosfolipid türevi mediyatör hangisidir?",
                [
                    {"key": "A", "text": "Trombosit Aktive Edici Faktör (PAF)", "explanation": "A seçeneği DOĞRUDUR: PAF düşük dozlarda histaminden 10.000 kat daha güçlü venüler sızıntı üretir."},
                    {"key": "B", "text": "Serotonin", "explanation": "B seçeneği yanlıştır: Serotonin primer vazokonstriktördür."},
                    {"key": "C", "text": "Prostaglandin D2", "explanation": "C seçeneği yanlıştır: Permeabiliteyi artırır ancak PAF kadar aşırı potent değildir."},
                    {"key": "D", "text": "İnterlökin-12", "explanation": "D seçeneği yanlıştır: Th1 farklılaşma sitokinidir."},
                    {"key": "E", "text": "Faktör XII", "explanation": "E seçeneği yanlıştır: Pıhtılaşma faktörüdür."}
                ],
                "A"
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-12-s73",
        "title": "Nitrik Oksit (NO) Biyolojisi ve Üç Nitrik Oksit Sentaz İzoformu",
        "content": "Nitrik Oksit (NO), hücre membranlarını serbestçe geçebilen, çok kısa yarılanma ömrüne (saniyeler) sahip çözünür bir gaz mediyatördür. L-Arjinin amino asidinden moleküler oksijen ve NADPH kullanılarak **Nitrik Oksit Sentaz (NOS)** enzimi tarafından sentezlenir. Vücutta üç farklı NOS izoformu mevcuttur:\n\n1. **Endotelyal NOS (eNOS / NOS3):** Vasküler endotelde konstitütif (sürekli) olarak bulunur. Bazal vasküler tonusu korur, arteriolleri gevşetir ve trombosit agregasyonunu engeller.\n2. **Nöronal NOS (nNOS / NOS1):** Santral ve periferik sinir sisteminde konstitütiftir; nörotransmitter olarak görev yapar ve ağrı iletiminde rol oynar.\n3. **İndüklenebilir NOS (iNOS / NOS2):** Normal sağlıklı hücrelerde bulunmaz. Makrofajlar, endotel ve düz kas hücrelerinde pro-inflamatuar sitokinler (**IFN-γ, TNF**) veya bakteriyel **LPS** ile gen transkripsiyonu düzeyinde **indüklenir**; mikromolar düzeyde masif ve sürekli NO üretir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["NOS İzoformu", "Ekspresyon Türü", "Hücresel Kaynak", "Temel Fizyolojik / Enflamatuar Görev"],
                [
                    [
                        {"text": "eNOS (NOS3)", "isMasked": False, "hint": ""},
                        {"text": "Konstitütif (Sürekli)", "isMasked": True, "hint": "Bazal damar tonusu enzimi"},
                        {"text": "Vasküler Endotel", "isMasked": False, "hint": ""},
                        {"text": "Vazodilatasyon ve kan akımının idamesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "nNOS (NOS1)", "isMasked": False, "hint": ""},
                        {"text": "Konstitütif (Sürekli)", "isMasked": True, "hint": "Sinir dokusu enzimi"},
                        {"text": "Nöronlar", "isMasked": False, "hint": ""},
                        {"text": "Nörotransmisyon ve sinaps iletişimi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "iNOS (NOS2)", "isMasked": False, "hint": ""},
                        {"text": "İndüklenebilir (İnflamasyonla)", "isMasked": True, "hint": "Sitokinlerle uyarım"},
                        {"text": "Makrofajlar ve Endotel", "isMasked": False, "hint": ""},
                        {"text": "Mikrop öldürme ve septik vazodilatasyon", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Makrofajlarda IFN-gama ve bakteriyel LPS uyarısıyla indüklenerek mikrop öldürücü yüksek konsantrasyonda NO üreten enzim indüklenebilir nitrik oksit sentazdır.",
                "indüklenebilir nitrik oksit sentazdır",
                "iNOS enziminin tam Türkçe adı"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-12-s74",
        "title": "iNOS ve Peroksinitrit (ONOO-): Mikrobisidal Mekanizma",
        "content": "Aktive makrofajlarda indüklenen iNOS enzimi, akut ve kronik enflamasyonda patojenlerin hücre içinde imha edilmesinde kilit bir ölüm silahı üretir. Makrofaj fagositoz esnasında eş zamanlı olarak iki radikal sistemi devreye sokar:\n\n1. **Süperoksit Radikali (O2•-):** Membrana bağlı NADPH oksidaz enzimi moleküler oksijeni tek elektronla indirgeyerek süperoksit anyonu üretir.\n2. **Nitrik Oksit (NO•):** Sitoplazmik iNOS enzimi yüksek konsantrasyonda serbest radikal nitrik oksit üretir.\n3. **Peroksinitrit (ONOO-) Sentezi:** Fagozom lümeninde süperoksit radikali ile nitrik oksit difüzyon hızında birleşerek son derece reaktif ve toksik bir oksidan olan **Peroksinitrit (ONOO-)** molekülünü oluşturur.\n\nPeroksinitrit bakteriyel membran lipidlerini perokside eder, bakteri proteinlerindeki tirozin kalıntılarını nitrolar (nitrozilasyon) ve DNA zincirini kırarak bakterileri ve parazitleri (örneğin *Leishmania*, *Tuberculosis*) süratle parçalar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Makrofaj İçi Mikrobisidal Peroksinitrit Kaskadı",
                [
                    "1. Fagositoz ve PAMP Uyarısı: Bakterinin yutulması ve iNOS/NADPH oksidaz aktivasyonu",
                    "2. Eş Zamanlı Radikal Üretimi: Süperoksit (O2•-) ve Nitrik Oksitin (NO•) sentezlenmesi",
                    "3. Radikal Birleşimi: Fagozomda O2•- ve NO•'in reaksiyonuyla Peroksinitrit (ONOO-) oluşumu",
                    "4. Bakteriyel İmha: Lipid peroksidasyonu ve tirozin nitrasyonu ile mikrobun parçalanması"
                ]
            ),
            make_recall(
                "Aktive makrofaj fagozomunda süperoksit radikali ile nitrik oksitin birleşmesi sonucu oluşan son derece güçlü mikrobisidal oksidan molekül nedir?",
                "Peroksinitrittir (ONOO-).",
                "NO ve O2 birleşimiyle oluşan reaktif nitrojen türü"
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-12-s75",
        "title": "Reaktif Oksijen Türleri (ROS) ve Miyeloperoksidaz (MPO) Yolağı",
        "content": "Nötrofillerin mikrop öldürme mekanizmasının çekirdeğini **Reaktif Oksijen Türleri (ROS)** oluşturur. Fagositoz anında nötrofil hücre zarındaki NADPH oksidaz enzimi aktive olur; hücre içi oksijen tüketimi aniden katlanarak artar (bu fenomene **solunumsal patlama / respiratuar patlama** denir):\n\n1. **Süperoksit (O2•-):** Oksijenin tek elektronla indirgenmesiyle ilk basamakta oluşur.\n2. **Hidrojen Peroksit (H2O2):** Süperoksit dismutaz (SOD) enzimi süperoksiti hidrojen peroksite dönüştürür.\n3. **Hipokloröz Asit (HOCl - Çamaşır Suyu):** Nötrofil azurofilik primer granüllerinde bolca bulunan **Miyeloperoksidaz (MPO)** enzimi, klor iyonları (Cl-) varlığında H2O2'yi son derece öldürücü bir halojenik oksidana dönüştürür: **Hipokloröz Asit (HOCl)**.\n\nHOCl saniyeler içinde bakteriyel proteinleri klorlayarak mikropları öldürür. Ancak nötrofiller ortama aşırı ROS saçtığında komşu konak dokusunda endotel hasarı, lipid peroksidasyonu ve doku nekrozu meydana gelir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Enzimatik Basamak", "Enzim", "Üretilen Reaktif Ürün", "Biyolojik Etki"],
                [
                    [
                        {"text": "1. Oksidatif Patlama", "isMasked": False, "hint": ""},
                        {"text": "NADPH Oksidaz", "isMasked": True, "hint": "Membrana bağlı elektron pompası"},
                        {"text": "Süperoksit (O2•-)", "isMasked": False, "hint": ""},
                        {"text": "İlk serbest oksijen radikali", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "2. Dismutasyon", "isMasked": False, "hint": ""},
                        {"text": "Süperoksit Dismutaz (SOD)", "isMasked": True, "hint": "Süperoksiti peroksite çeviren enzim"},
                        {"text": "Hidrojen Peroksit (H2O2)", "isMasked": False, "hint": ""},
                        {"text": "Orta güçte oksidan prekürsör", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "3. Halojenasyon", "isMasked": False, "hint": ""},
                        {"text": "Miyeloperoksidaz (MPO)", "isMasked": True, "hint": "Nötrofil azurofilik granül enzimi"},
                        {"text": "Hipokloröz Asit (HOCl)", "isMasked": False, "hint": ""},
                        {"text": "En güçlü bakterisidal oksidan", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Nötrofil granüllerindeki miyeloperoksidaz enzimi klor varlığında hidrojen peroksiti son derece öldürücü hipokloröz aside dönüştürür.",
                "hipokloröz aside",
                "HOCl formüllü güçlü bakterisidal oksidan"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-12-s76",
        "title": "Lizozomal Enzimler ve Nötrofil Ekstraselüler Tuzakları (NET'ler)",
        "content": "Nötrofiller mikrop öldürürken iki ek mekanizmayla doku ortamına müdahale ederler:\n\n1. **Lizozomal Enzimler:** Nötrofil azurofilik granülleri miyeloperoksidaz, lizozim, defensinler ve asit hidrolazların yanı sıra ekstraselüler matriksi parçalayan nötral proteazlar (**Elastaz, Katepsin G ve Proteinaz-3**) içerir. Bu enzimler dışarıya sızdığında bağ dokusunu eriterek apse formasyonuna ve doku likefaksiyonuna yol açar (alfa-1 antitripsin bu elastazı nötralize eden koruyucu serum proteinidir).\n2. **Nötrofil Ekstraselüler Tuzakları (NET'ler / Netozis):** Ağır enfeksiyonlarda nötrofiller intihar benzeri özelleşmiş bir hücre ölümü programına (netozis) girerler. Nötrofil nükleer zarı parçalanır; de-kondanse olmuş nükleer **kromatin (DNA ve histon proteinleri)** sitoplazmik granül antimikrobiyal enzimleri (MPO, elastaz) ile harmanlanarak doku dışına devasa bir 'örümcek ağı' gibi fırlatılır. Bakteriler bu yapışkan DNA ağına takılarak mekanik olarak hapsedilir ve yüksek konsantrasyondaki enzimlerle öldürülür.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Nötrofil Savunma Yöntemleri Karşılaştırması",
                "Klasik Fagositoz",
                "Mikrop hücre içine yutulur, fagozomda ROS ve lizozomal enzimlerle sessizce sindirilir.",
                "NET Oluşumu (Netozis)",
                "Nötrofil DNA ve granül enzimlerini dışarıya yapışkan bir ağ gibi fırlatarak mikropları dışarıda hapseder."
            ),
            make_recall(
                "Nötrofillerin nükleer kromatin ipliklerini granül proteinleriyle birleştirip ekstraselüler alana saçarak mikropları hapsettiği ağ yapısına ne ad verilir?",
                "Nötrofil Ekstraselüler Tuzaklarıdır (NET / Netozis).",
                "DNA ve enzimlerden oluşan antimikrobiyal ağ"
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-12-s77",
        "title": "Nöropeptitler ve Nörojenik Enflamasyon: Madde P ve CGRP",
        "content": "Enflamasyonun kontrolünde sinir sistemi ile bağışıklık sistemi arasında iki yönlü doğrudan bir köprü bulunur. Periferik dokularda yer alan miyelinsiz duyusal C lifleri hasar gördüğünde veya kimyasal uyaranlarla (kapsaisin, histamin, bradikinin) uyarıldığında ortama **Nöropeptitler** salgılarlar. Bu fenomene **Nörojenik Enflamasyon** denir:\n\n- **Madde P (Substance P):** Duyusal sinir uçlarından salınır. Mast hücrelerinde NK-1 reseptörlerine bağlanarak güçlü histamin degranülasyonunu tetikler; arterioler vazodilatasyon yapar, postkapiller venüllerde geçirgenliği dramatik artırır ve ağrı sinyalini spinal korda iletir.\n- **Kalsitonin Gen İlişkili Peptit (CGRP):** İnsan vücudundaki en güçlü mikrovasküler vazodilatatörlerden biridir. Lokal kan akımını katlar; özellikle **Migren baş ağrısının** patogenezinde meningeal vasküler dilatasyon ve nörojenik enflamasyonun temel sorumlusudur (güncel migren ilaçları CGRP reseptör blokerleridir).",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Nöropeptit", "Hücresel Kaynak", "Temel Enflamatuar Etki", "İlişkili Klinik Durum"],
                [
                    [
                        {"text": "Madde P (Substance P)", "isMasked": False, "hint": ""},
                        {"text": "Duyusal C tipi sinir lifleri", "isMasked": True, "hint": "Ağrı ileten miyelinsiz lifler"},
                        {"text": "Mast degranülasyonu, ödem ve ağrı iletimi", "isMasked": False, "hint": ""},
                        {"text": "Nörojenik doku ödemi ve kronik ağrı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "CGRP", "isMasked": False, "hint": ""},
                        {"text": "Trigeminal ve periferik duyusal nöronlar", "isMasked": True, "hint": "Kafa ve yüz sinir ganglionları"},
                        {"text": "Aşırı güçlü serebral/periferik vazodilatasyon", "isMasked": False, "hint": ""},
                        {"text": "Migren atağı patogenezi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Duyusal sinir uçlarından salınarak mast hücrelerinden histamin salınımını tetikleyen ve nörojenik ödem yapan temel nöropeptit madde P dir.",
                "madde P dir",
                "Ağrı ve nörojenik enflamasyonun klasik P harfli peptiti"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-12-s78",
        "title": "Koagülasyon ve Fibrinoliz Sistemleri ile Enflamasyon Kesişimi",
        "content": "Pıhtılaşma (koagülasyon) ve fibrinoliz kaskadları, enflamasyondan izole sistemler olmayıp sayısız çapraz aktivasyon düğüm noktasıyla birbirine kenetlenmiştir:\n\n1. **Trombin ve PAR Reseptörleri:** Pıhtılaşma kaskadının nihai enzimi olan **Trombin**, yalnızca fibrinojeni fibrine çevirmekle kalmaz; endotel hücreleri, lökositler ve trombositler üzerindeki **Proteazla Aktive Olan Reseptörleri (PAR-1)** proteolitik olarak keserek aktive eder. Trombin-PAR bağlanması endotelde P-selektin ekspresyonunu, kemokin (IL-8) salınımını, COX-2 indüksiyonunu ve prostaglandin üretimini patlatır.\n2. **Faktör Xa:** Benzer şekilde PAR reseptörleri üzerinden vasküler permeabiliteyi artırır.\n3. **Fibrinopeptitler:** Fibrinojen fibrine dönüşürken açığa çıkan küçük fibrinopeptitler lökositler için kemotaktiktir ve damar geçirgenliğini artırır.\n4. **Plazmin ve Kompleman Kesişimi:** Fibrini eriten plazmin enzimi doğrudan **kompleman C3 ve C5'i parçalayarak C3a ve C5a** anafilatoksinlerini serbest bırakabilir; böylece pıhtı erirken bile enflamasyon uyarılmaya devam eder.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Koagülasyon-Enflamasyon Çapraz Etkileşim Zinciri",
                [
                    "1. Doku Faktörü / Hasar: Ekstrinsek ve intrinsik koagülasyon kaskadının ateşlenmesi",
                    "2. Trombin Üretimi: Protrombinden aktif serin proteaz trombin sentezi",
                    "3. PAR-1 Kesimi: Trombinin endotel yüzeyindeki proteaz-aktive reseptörü aktive etmesi",
                    "4. Enflamatuar Yanıt: Endotelden P-selektin, kemokinler ve PGE2 salınımının tetiklenmesi"
                ]
            ),
            make_recall(
                "Pıhtılaşma kaskadı enzimi olan trombinin endotel ve lökositlerde enflamatuar yanıtı uyarmak için aktive ettiği reseptör ailesi nedir?",
                "PAR reseptörleridir (Protease-activated receptors / PAR-1).",
                "Proteazla aktive olan transmembran reseptör ailesi"
            )
        ]
    })

    # Slide 79 (CHECKPOINT 8)
    slides.append({
        "id": "k1-12-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] PAF, Nitrik Oksit, Nöropeptitler ve Koagülasyon Kesişimi",
        "content": "Çeşitli hücre kaynaklı ve plazma mediyatörlerinin kesişim ilkeleri:\n\n1. **PAF:** Membran fosfolipid türevidir (PLA2 ile); pikomolar düzeyde histaminden 10.000 kat güçlü permeabilite artışı ve vazodilatasyon, yüksek dozda trombosit agregasyonu ve bronkospazm yapar.\n2. **Nitrik Oksit (NO):** eNOS bazal damar tonusunu sürdürür; makrofajlardaki **iNOS** sitokinlerle (IFN-γ) indüklenir ve süperoksitle birleşerek öldürücü **Peroksinitrit (ONOO-)** üretir.\n3. **ROS ve MPO:** Solunumsal patlamada NADPH oksidaz süperoksit üretir; nötrofil granülündeki Miyeloperoksidaz (MPO) bunu klorla birleştirip **Hipokloröz Asit (HOCl)** yapar.\n4. **NET'ler:** Nötrofiller kromatin ve antimikrobiyal enzimleri dışarı saçarak mikropları ağa hapseder.\n5. **Nöropeptitler:** Madde P mast hücresini degranüle edip ödem ve ağrı yapar; CGRP güçlü vazodilatatördür ve migrende rol oynar.\n6. **Trombin ve PAR:** Trombin PAR-1 reseptörüyle endoteli uyararak pıhtılaşma ile enflamasyonu birbirine bağlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Nötrofil azurofilik granüllerinde bulunan ve hidrojen peroksiti klorür iyonlarıyla birleştirerek son derece güçlü bakterisidal hipokloröz aside (HOCl) dönüştüren enzim hangisidir?",
                [
                    {"key": "A", "text": "Miyeloperoksidaz (MPO)", "explanation": "A seçeneği DOĞRUDUR: MPO klor varlığında H2O2'yi HOCl'ye (çamaşır suyu) dönüştüren primer enzimdir."},
                    {"key": "B", "text": "Süperoksit dismutaz", "explanation": "B seçeneği yanlıştır: Süperoksiti H2O2'ye çevirir."},
                    {"key": "C", "text": "Fosfolipaz C", "explanation": "C seçeneği yanlıştır: İnozitol fosfat yolak enzimidir."},
                    {"key": "D", "text": "Kallikrein", "explanation": "D seçeneği yanlıştır: Kinin yolak enzimidir."},
                    {"key": "E", "text": "Siklooksijenaz-1", "explanation": "E seçeneği yanlıştır: Prostaglandin enzimdir."}
                ],
                "A"
            ),
            make_cloze(
                "Pıhtılaşma enzimi trombin vasküler endotel yüzeyindeki PAR-1 reseptörlerini aktive ederek koagülasyon ile enflamasyonu birleştirir.",
                "PAR-1 reseptörlerini",
                "Trombinin bağlandığı proteazla aktive olan reseptör"
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-12-s80",
        "title": "Mediyatörlerin Fazlalığı (Redundancy) ve Sinerjik Ağ Yapısı",
        "content": "Evrimsel süreçte konak savunması hayati bir öneme sahip olduğundan, enflamasyon sistemi tek bir mediyatörün tekeline bırakılmamıştır. Sistemde muazzam bir **fazlalık (redundancy / yedeklilik)** ve **sinerji** mevcuttur:\n\n- **Aynı Görevi Paylaşan Çok Sayıda Mediyatör:** Örneğin vazodilatasyonu yalnızca histamin yapmaz; PGE2, PGD2, PGI2, bradikinin, NO ve PAF da yapar. Kemotaksiyi yalnızca IL-8 yönetmez; LTB4, C5a ve bakteriyel formil peptitler de yürütür.\n- **Klinik ve Terapötik Önemi:** Tek bir mediyatörü ilaçla bloke etmek (örneğin sadece antihistaminik vermek veya sadece tek bir sitokini kesmek) çoğu zaman enflamatuar reaksiyonu tamamen durduramaz; diğer yedek mediyatörler bayrağı devralarak enflamasyonu sürdürür.\n- **Stratejik Düğüm Noktaları:** Bu nedenle modern farmakoloji tek tek son ürünleri değil, kaskadların tepe anahtarlarını hedefler: PLA2 (kortikosteroidler), COX (NSAİİ'ler) veya merkezi ana sitokinler (TNF ve IL-1 reseptör blokerleri).",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Tek Mediyatör Blokajı vs Stratejik Düğüm Blokajı",
                "Tek Mediyatör Blokajı (Ör. Antihistaminik)",
                "Yalnızca histamini keser; eikozanoidler, sitokinler ve kompleman enflamasyonu sürdürür.",
                "Stratejik Düğüm Blokajı (Ör. Kortikosteroid / Anti-TNF)",
                "Kaskadın tepesini susturur; onlarca farklı mediyatörün üretimini aynı anda durdurur."
            ),
            make_recall(
                "Enflamasyonda birden fazla farklı kimyasal mediyatörün aynı vasküler veya hücresel biyolojik yanıtı üretebilme özelliğine ne ad verilir?",
                "Yedeklilik / fazlalıktır (redundancy).",
                "Sistemin tek bir moleküle bağımlı olmama güvencesi"
            )
        ]
    })

    return slides
