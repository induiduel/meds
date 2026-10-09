# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_25_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar senaryoları) ögeleri (26 adet)."""
    return {
        2: make_branching_logic(
            "Penisilin enjeksiyonundan 5 dakika sonra dudaklarında şişme, yaygın ürtiker ve nefes darlığı gelişen 30 yaşında bir hastanın tansiyonu 70/40 mmHg ölçülüyor.",
            "Acil serviste bu akut anafilaktik şok tablosunda derhal yapılması gereken ilk hayat kurtarıcı müdahale ne olmalıdır?",
            [
                {
                    "text": "Vakit kaybetmeden uyluk anterolateral bölgesinden intramusküler (İM) adrenalin uygulanması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; adrenalin alfa-1 vazokonstriksiyonu ile tansiyonu yükseltir, beta-2 bronkodilatasyonu ile bronkospazmı çözer ve mast hücre degranülasyonunu durdurur."
                },
                {
                    "text": "Yalnızca oral antihistaminik şurup verilerek hastanın gözleme alınması",
                    "isCorrect": False,
                    "explanation": "Hatalı ve ölümcül; antihistaminikler laringeal ödem ve vazodilatasyonu hızla durduramaz, anafilakside ilk tercih mutlaka adrenalindir."
                },
                {
                    "text": "Geniş spektrumlu sefalosporin antibiyotiğe geçilmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; penisilin alerjisi olanlarda sefalosporinlerle çapraz reaksiyon riski vardır ve tabloyu ağırlaştırır."
                }
            ]
        ),
        4: make_branching_logic(
            "Kronik saman nezlesi (alerjik rinit) olan bir hastada bahar aylarında polen teması sonrası nazal konjesyon, burun akıntısı ve hapşırma nöbetleri gelişiyor.",
            "Bu tablonun erken fazında salgılanan primer mediyatörler ile geç fazında dokuya infiltre olan lökosit alt tipi hangi seçenekte doğru eşleştirilmiştir?",
            [
                {
                    "text": "Erken fazda mast hücre granüllerinden salınan histamin; geç fazda (2-8 saat sonra) dokuya toplanan eozinofiller",
                    "isCorrect": True,
                    "explanation": "Doğrudur; erken vazodilatasyon ve mukus sekresyonundan histamin sorumludur; geç faz inflamasyonunu IL-5 uyarısıyla gelen eozinofiller yönetir."
                },
                {
                    "text": "Erken fazda monosit kökenli lizozim; geç fazda dokuyu saran nötrofilik granülomlar",
                    "isCorrect": False,
                    "explanation": "Hatalı; Tip I hipersensitivite granülomatöz değildir ve erken fazda histamin salınır."
                },
                {
                    "text": "Erken fazda sitotoksik T lenfosit perforini; geç fazda B lenfosit proliferasyonu",
                    "isCorrect": False,
                    "explanation": "Hatalı; perforin Tip IV hücresel sitotoksisitede rol oynar."
                }
            ]
        ),
        6: make_branching_logic(
            "ABO uygunsuz kan transfüzyonu yapılan bir hastada transfüzyondan dakikalar sonra ani bel ağrısı, titreme, yüksek ateş, hemoglobinüri ve hipotansiyon gelişiyor.",
            "Bu akut hemolitik transfüzyon reaksiyonunun immünolojik ve histopatolojik mekanizması nedir?",
            [
                {
                    "text": "Alıcının doğal IgM antikorlarının donör eritrosit yüzeyindeki A/B antijenlerine bağlanarak klasik kompleman yolağını (MAC / C5b-9) aktive etmesi ve intravasküler hemoliz yapması (Tip II Hipersensitivite)",
                    "isCorrect": True,
                    "explanation": "Kusursuz Patoloji Bilgisi: ABO uyuşmazlığında preform IgM antikorları komplemanı bağlayarak membran atak kompleksiyle eritrositleri intravasküler ortamda parçalar."
                },
                {
                    "text": "Dolaşan çözünür immün komplekslerin böbrek glomerüllerine çökerek Tip III nefrit yapması",
                    "isCorrect": False,
                    "explanation": "Hatalı; eritrosit yüzey antijeni çözünür değil sabittir, bu nedenle Tip II sitotoksik hasardır."
                },
                {
                    "text": "Duyarlı T hücrelerinin donör eritrositlerine karşı granülomatöz reaksiyon başlatması",
                    "isCorrect": False,
                    "explanation": "Hatalı; akut hemoliz dakikalar içinde humoral antikorlarla gerçekleşir, T hücresi aracılı değildir."
                }
            ]
        ),
        8: make_branching_logic(
            "Akut romatizmal ateş geçiren bir çocukta solunum sıkıntısı ve kardiyomegali gelişiyor. Ekokardiyografide mitral yetmezlik ve miyokardit saptanıyor.",
            "Streptokok farenjiti sonrası kalpte gelişen bu hasarın immünolojik temeli nedir?",
            [
                {
                    "text": "Grup A streptokok M proteinine karşı gelişen antikorların insan kardiyak miyozin ve sarkolemma proteinleriyle çapraz reaksiyon vermesi (Moleküler Benzerlik - Tip II Hipersensitivite)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; bakteriyel M proteini ile miyokard antijenleri arasındaki moleküler taklit miyokardit ve Aschoff nodüllerine neden olur."
                },
                {
                    "text": "Bakteriyel toksinlerin doğrudan koroner damarları tıkamasıyla gelişen akut miyokard enfarktüsü",
                    "isCorrect": False,
                    "explanation": "Hatalı; akut romatizmal ateş iskemik enfarktüs değil, immün kaynaklı pankardit tablosudur."
                },
                {
                    "text": "Mast hücrelerinin miyokardda degranüle olarak Tip I anafilaktik spazm yapması",
                    "isCorrect": False,
                    "explanation": "Hatalı; ARA tipik bir antikor bağımlı çapraz reaksiyonel Tip II tablosudur."
                }
            ]
        ),
        12: make_branching_logic(
            "Goodpasture sendromu kuşkusuyla böbrek biyopsisi yapılan bir hastanın direkt immünfloresans incelemesinde glomerül bazal membranları boyunca düzgün, kesintisiz, şerit tarzında (lineer) IgG depolanması izleniyor.",
            "Bu lezyonun patofizyolojik mekanizması ve hedef antijeni nedir?",
            [
                {
                    "text": "Tip IV kollajenin alfa-3 zincirine (Goodpasture antijeni) karşı gelişen otoantikorların kompleman ve nötrofilleri aktive etmesi (Tip II Sitotoksik Hipersensitivite)",
                    "isCorrect": True,
                    "explanation": "Mükemmel Patoloji Bilgisi: Lineer paternde immünfloresans Goodpasture için karakteristiktir ve Tip IV kollajen alfa-3 zincirini hedefler."
                },
                {
                    "text": "Dolaşan çözünür DNA-anti-DNA komplekslerinin granüler tarzda mezangiyuma çökmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; çözünür kompleksler granüler çökelti yapar (Tip III lupus), lineer boyanma yapmaz."
                },
                {
                    "text": "CD8+ T lenfositlerin Bowman kapsülünü granülomlarla eritmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; Goodpasture otoantikor kaynaklı lineer bazal membran hasarıdır."
                }
            ]
        ),
        14: make_branching_logic(
            "Ciltte gevşek büller, ağız içinde erozyonlar ve Nikolsky belirtisi pozitifliği ile başvuran 45 yaşındaki hastanın biyopsisinde intraepidermal akantoliz ve bül tabanında 'mezar taşı' görünümü saptanıyor.",
            "Bu hastadaki kesin patolojik tanı ve otoantikorların hedef molekülü hangisidir?",
            [
                {
                    "text": "Pemfigus Vulgaris; keratinositler arası desmozom proteini olan desmoglein-3'e karşı otoantikorlar",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Pemfigus vulgaris desmoglein-3'ü hedefler, intraepidermal suprabazal ayrışma ve mezar taşı manzarası oluşturur."
                },
                {
                    "text": "Büllöz Pemfigoid; dermoepidermal bileşkedeki hemidesmozom BP180/BP230 antijenlerine karşı otoantikorlar",
                    "isCorrect": False,
                    "explanation": "Hatalı; büllöz pemfigoid subepidermal gergin büller yapar, akantoliz ve mezar taşı görüntüsü Pemfigus'a özgüdür."
                },
                {
                    "text": "Dermatitis Herpetiformis; epidermal transglutaminaza karşı IgA depolanması",
                    "isCorrect": False,
                    "explanation": "Hatalı; dermatitis herpetiformiste dermal papillalarda mikroabseler ve granüler IgA görülür."
                }
            ]
        ),
        16: make_branching_logic(
            "Akut kas güçsüzlüğü, pitozis ve çift görme şikayeti olan ve günün ilerleyen saatlerinde yoruldukça semptomları artan bir hastada edrofonyum (Tensilon) testi ile güçsüzlük dramatik olarak düzeliyor.",
            "Bu tablonun nöromusküler kavşaktaki immünopatolojik temeli nedir?",
            [
                {
                    "text": "Postsinaptik nikotinik asetilkolin reseptörlerine (AChR) bağlanan otoantikorların reseptör fonksiyonunu ve iletimi bloke etmesi (Tip II Hipersensitivite)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Myastenia Gravis antikor aracılı reseptör blokajı prototipidir."
                },
                {
                    "text": "Presinaptik voltaj kapılı kalsiyum kanallarına bağlanan antikorların asetilkolin salınımını engellemesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu durum Lambert-Eaton miyastenik sendromudur ve güç egzersizle artar."
                },
                {
                    "text": "Periferik miyelin kılıfına karşı CD8+ T lenfositlerin demiyelinizan plaklar oluşturması",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu durum Guillain-Barré sendromudur."
                }
            ]
        ),
        18: make_branching_logic(
            "Tip I Diabetes Mellitus tanılı bir çocuğun pankreas biyopsisinde Langerhans adacıklarında lenfosit infiltrasyonu (insülit) ve beta hücrelerinin selektif apoptozu saptanıyor.",
            "Bu doku hasarı hangi aşırı duyarlılık mekanizmasının sonucudur?",
            [
                {
                    "text": "Otoantijenleri tanıyan CD4+ Th1/Th17 sitokinleri ve CD8+ sitotoksik T lenfositlerin aracılık ettiği Tip IV Hücresel Aşırı Duyarlılık",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Tip 1 diyabet beta hücre otoantijenlerine karşı gelişen T lenfosit aracılı hücresel immün yanıttır."
                },
                {
                    "text": "Mast hücrelerinin pankreas adacıklarında IgE ile degranüle olması (Tip I)",
                    "isCorrect": False,
                    "explanation": "Hatalı; diyabette mast hücre aracılı acil yanıt söz konusu değildir."
                },
                {
                    "text": "Dolaşan çözünür immün komplekslerin Langerhans kılcallarını tıkaması (Tip III)",
                    "isCorrect": False,
                    "explanation": "Hatalı; Tip 1 diyabette primer lezyon vaskülit değil, T hücre insülitidir."
                }
            ]
        ),
        22: make_branching_logic(
            "Lupus nefriti şüphesiyle incelenen bir böbrek biyopsisinde ışık mikroskobunda glomerül kılcal duvarlarında diffüz tel halka (wire loop) lezyonları, immünfloresanda ise 'full-house' depolanma izleniyor.",
            "Bu morfoloji DSÖ/RPS sınıflamasına göre hangi lupus nefriti evresine aittir ve klinik önemi nedir?",
            [
                {
                    "text": "Sınıf IV Diffüz Lupus Nefriti; en sık görülen, en ağır seyreden ve son dönem böbrek yetmezliğine en hızlı ilerleyen formdur",
                    "isCorrect": True,
                    "explanation": "Mükemmel Patoloji Bilgisi: Tel halka manzarası masif subendotelyal immün kompleks birikimini gösterir ve Sınıf IV lupus nefritinin en tipik morfolojik bulgusudur."
                },
                {
                    "text": "Sınıf I Minimal Mezangiyal Lupus Nefriti; ışık mikroskopisinde tamamen normal olan iyi huylu tablodur",
                    "isCorrect": False,
                    "explanation": "Hatalı; Sınıf I'de tel halka görülmez ve glomerüller ışık mikroskobunda normaldir."
                },
                {
                    "text": "Sınıf VI İlerlemiş Sklerozan Lupus Nefriti; böbreğin tamamen taşlaştığı ve immün komplekslerin kaybolduğu evredir",
                    "isCorrect": False,
                    "explanation": "Hatalı; Sınıf VI diffüz sklerozdur; tel halka ve aktif subendotelyal birikim Sınıf IV'e özgüdür."
                }
            ]
        ),
        24: make_branching_logic(
            "SLE tanısı olan gebe bir kadında tekrarlayan düşük öyküsü, bacakta derin ven trombozu ve trombositopeni tespit ediliyor. Laboratuvarda lupus antikoagülanı pozitif bulunuyor.",
            "Bu hastadaki ek klinik tablonun adı ve pıhtılaşma testlerindeki karakteristik paradoks nedir?",
            [
                {
                    "text": "Antifosfolipid Antikor Sendromu; in vitro ortamda aPTT süresi uzar ancak in vivo vücutta arteriyel/venöz trombozlar gelişir",
                    "isCorrect": True,
                    "explanation": "Doğrudur; fosfolipid-protein komplekslerine bağlanan antikorlar laboratuvarda aPTT'yi uzatırken canlıda hiperkoagülabilite ve tromboz yapar."
                },
                {
                    "text": "Hemofili A sendromu; Faktör VIII eksikliğine bağlı spontan kas içi kanamalar görülür",
                    "isCorrect": False,
                    "explanation": "Hatalı; hemofilide tromboz değil kanama olur ve lupusla doğrudan ilişkili otoantikor tablosu değildir."
                },
                {
                    "text": "Von Willebrand Hastalığı; primer hemostaz bozukluğu ile trombosit tıkacı oluşamaz",
                    "isCorrect": False,
                    "explanation": "Hatalı; vWF eksikliği kanamaya eğilim yapar, tromboz yapmaz."
                }
            ]
        ),
        26: make_branching_logic(
            "Romatoid artritli bir hastada el parmaklarında ulnar deviasyon, kuğu boynu ve düğme iliği deformiteleri saptanıyor. Sinovyal biyopside hiperplastik villöz sinovya, lenfosit folikülleri ve nötrofilik eksüda görülüyor.",
            "Bu eklem hasarını yönlendiren temel granülasyon ve inflamasyon dokusunun patolojik adı nedir?",
            [
                {
                    "text": "Pannus dokusu; eklem kıkırdağını ve altındaki kemiği eriten proliferatif fibroblast, kan damarı ve inflamatuar hücre kütlesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; RA'nın eklem harabiyetinden sorumlu patognomonik lezyonu kıkırdak üzerine yürüyen agresif pannustur."
                },
                {
                    "text": "Tofüs plağı; monosodyum ürat kristallerinin çevrelediği yabancı cisim granülomu",
                    "isCorrect": False,
                    "explanation": "Hatalı; tofüs gut artritinde görülür, romatoid artrit lezyonu değildir."
                },
                {
                    "text": "Aschoff cisimciği; miyokardda fibrinoid nekroz etrafındaki Anitschkow miyositleri",
                    "isCorrect": False,
                    "explanation": "Hatalı; Aschoff nodülleri romatizmal karditte görülür."
                }
            ]
        ),
        28: make_branching_logic(
            "Romatoid faktör (RF) laboratuvar testi pozitif çıkan bir hastanın raporu değerlendiriliyor.",
            "Romatoid faktörün immünolojik moleküler yapısı ve hedefi nedir?",
            [
                {
                    "text": "Hastanın kendi endojen IgG moleküllerinin Fc bölgesine karşı gelişmiş IgM sınıfı otoantikorlardır",
                    "isCorrect": True,
                    "explanation": "Kusursuz Patoloji Bilgisi: RF klasik olarak IgG Fc bölgesine yönelmiş IgM otoantikorudur."
                },
                {
                    "text": "Streptokok DNA'sına karşı üretilmiş IgE sınıfı degranülasyon antikorudur",
                    "isCorrect": False,
                    "explanation": "Hatalı; RF antijenik hedefi endojen IgG Fc fragmentidir."
                },
                {
                    "text": "Eritrosit yüzeyindeki Rh(D) antijenine bağlanan IgG antikordur",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu Rh uyuşmazlığındaki anti-D antikorudur."
                }
            ]
        ),
        32: make_branching_logic(
            "Primer Sjögren sendromu olan 50 yaşındaki kadın hastanın takiplerinde sağ parotis bezinde asimetrik, ağrısız ve hızlı büyüyen sert bir kitle gelişiyor.",
            "Bu hastada ilk olarak şüphelenilmesi gereken ve Sjögren hastalarında 40 kat artmış olan malignite hangisidir?",
            [
                {
                    "text": "B hücreli Non-Hodgkin Marjinal Zon (MALT) Lenfoması",
                    "isCorrect": True,
                    "explanation": "Mükemmel Klinik ve Patolojik Bilgi: Sjögren hastalarında persistan poliklonal B hücre uyarısı klonal malign lenfomaya (MALT lenfoma) dönüşebilir."
                },
                {
                    "text": "Adenoid kistik karsinom",
                    "isCorrect": False,
                    "explanation": "Hatalı; Sjögren zemininde risk artıran majör neoplazi lenfoid kökenli B hücreli lenfomadır."
                },
                {
                    "text": "Warthin tümörü (kistadenolenfoma)",
                    "isCorrect": False,
                    "explanation": "Hatalı; Warthin sigara içen yaşlı erkeklerde benign bir tükürük bezi tümörüdür."
                }
            ]
        ),
        34: make_branching_logic(
            "Ellerinde soğukta beyazlaşma, morarma ve ardından kızarma (Raynaud fenomeni), yutma güçlüğü (disfaji) ve parmak cildinde parlak sertleşme (sklerodaktili) olan bir hastada CREST sendromu düşünülüyor.",
            "Bu sınırlı sistemik skleroz tablosunda kanda pozitifleşmesi beklenen son derece özgül otoantikor hangisidir?",
            [
                {
                    "text": "Anti-Sentromer antikoru (ACA)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; anti-sentromer antikorları CREST (sınırlı kutanöz sistemik skleroz) hastalarının %70-80'inde pozitiftir ve visseral fibroz riskinin düşük olduğunu gösterir."
                },
                {
                    "text": "Anti-Scl-70 (DNA Topoizomeraz I) antikoru",
                    "isCorrect": False,
                    "explanation": "Hatalı; Anti-Scl-70 diffüz kutanöz sistemik sklerozda pozitiftir ve ağır akciğer fibrozu ile seyreder."
                },
                {
                    "text": "Anti-dsDNA antikoru",
                    "isCorrect": False,
                    "explanation": "Hatalı; anti-dsDNA SLE için spesifiktir."
                }
            ]
        ),
        36: make_branching_logic(
            "Diffüz sistemik skleroz tanısıyla izlenen 42 yaşındaki hastada nefes darlığı ve kuru öksürük başlıyor. Yüksek çözünürlüklü toraks BT'sinde bilateral bazallerde bal peteği akciğer ve interlobüler septal kalınlaşmalar izleniyor.",
            "Bu komplikasyonun patolojisi ve hastadaki en sık ölüm nedeni nedir?",
            [
                {
                    "text": "İnterstisyel pulmoner fibrozis; günümüzde sistemik sklerozlu hastalarda bir numaralı mortalite nedenidir",
                    "isCorrect": True,
                    "explanation": "Doğrudur; ACE inhibitörlerinin renal krizi kontrol altına almasından sonra sklerodermada başlıca ölüm nedeni akciğer fibrozu ve pulmoner hipertansiyondur."
                },
                {
                    "text": "Masif lober pnömoni ve alveoler apse gelişimi",
                    "isCorrect": False,
                    "explanation": "Hatalı; sklerodermadaki lezyon enfeksiyon değil, TGF-beta aracılı diffüz interstisyel fibrozistir."
                },
                {
                    "text": "Bronşiyal karsinoid tümör tıkanması",
                    "isCorrect": False,
                    "explanation": "Hatalı; karsinoid tümör nöroendokrin neoplazidir."
                }
            ]
        ),
        38: make_branching_logic(
            "Ciltte heliotrop döküntü (göz kapaklarında leylak rengi ödem), Gottron papülleri ve proksimal kas güçsüzlüğü ile başvuran hastanın kas biyopsisinde perimisyal inflamasyon ve perifasiküler atrofi saptanıyor.",
            "Bu hastadaki kesin tanı ve kanda interstisyel akciğer hastalığı birlikteliğini gösteren antikor hangisidir?",
            [
                {
                    "text": "Dermatomiyozit; Anti-Jo-1 (histidil-tRNA sentetaz) antikoru pozitifliği",
                    "isCorrect": True,
                    "explanation": "Doğrudur; heliotrop raş, Gottron papülleri ve perifasiküler atrofi dermatomiyozitin patognomonik triadıdır; Anti-Jo-1 akciğer tutulumu riskini belirler."
                },
                {
                    "text": "Polimiyozit; Anti-Sentromer antikoru pozitifliği",
                    "isCorrect": False,
                    "explanation": "Hatalı; polimiyozitte cilt döküntüleri olmaz ve endomisyal CD8+ infiltrasyonu görülür."
                },
                {
                    "text": "Miyastenia Gravis; Anti-AChR antikoru pozitifliği",
                    "isCorrect": False,
                    "explanation": "Hatalı; miyastenide kas enzim yüksekliği, cilt döküntüsü ve inflamatuar miyopati olmaz."
                }
            ]
        ),
        42: make_branching_logic(
            "Döküntü, ateş, artralji ve lenfadenopati şikayetleriyle başvuran bir hastada ANA pozitif, Anti-U1 RNP antikoru çok yüksek titrede saptanıyor; ancak anti-dsDNA ve anti-Scl-70 negatif bulunuyor.",
            "SLE, sistemik skleroz ve polimiyozit bulgularının bir arada görüldüğü bu overlap sendromunun adı nedir?",
            [
                {
                    "text": "Mikst Bağ Dokusu Hastalığı (MCTD - Sharp Sendromu)",
                    "isCorrect": True,
                    "explanation": "Mükemmel Patoloji Bilgisi: MCTD'nin ayırt edici serolojik belirteci yüksek titrede Anti-U1 RNP antikorudur ve böbrek tutulumu SLE'ye göre çok daha seyrektir."
                },
                {
                    "text": "Sınıf IV Diffüz Proliferatif Lupus",
                    "isCorrect": False,
                    "explanation": "Hatalı; Sınıf IV lupusta anti-dsDNA pozitiftir ve ağır nefrit vardır."
                },
                {
                    "text": "Romatoid Artrit",
                    "isCorrect": False,
                    "explanation": "Hatalı; RA'da anti-CCP ve RF pozitiftir, Anti-U1 RNP özgül değildir."
                }
            ]
        ),
        44: make_branching_logic(
            "Böbrek transplantasyonu yapılan bir hastada cerrah vasküler anastomozları tamamlayıp klempleri açtıktan birkaç dakika sonra greft böbrek aniden siyanotik, soluk, benekli ve gevşek hale geliyor; idrar çıkışı aniden duruyor.",
            "Bu hiperakut rejeksiyon tablosunun patogenezi ve mikroskopik bulgusu nedir?",
            [
                {
                    "text": "Alıcıda donör HLA veya ABO antijenlerine karşı önceden var olan antikorların (preform antikorlar) endoteli tahrip etmesi ve yaygın trombotik tıkanma yapması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; hiperakut rejeksiyon dakikalar içinde gelişen preform antikor bağımlı vasküler tromboz ve iskemik nekroz tablosudur."
                },
                {
                    "text": "Duyarlı donör T lenfositlerinin alıcı organını aylar sonra yavaşça eritmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu kronik hücresel rejeksiyondur, dakikalar içinde gelişmez."
                },
                {
                    "text": "Cerrahi sütür materyaline karşı gelişen granülomatöz yabancı cisim reaksiyonu",
                    "isCorrect": False,
                    "explanation": "Hatalı; cerrahi sütür reaksiyonu lokal ve gecikmiştir, hiperakut greft kaybı yapmaz."
                }
            ]
        ),
        46: make_branching_logic(
            "Kemik iliği nakli yapılan lösemili bir hastada naklin 25. gününde yaygın döküntü, sarılık (kolestaz) ve kanlı ishal gelişiyor.",
            "Bu tablonun patolojik adı ve immünolojik yönü nedir?",
            [
                {
                    "text": "Graft-versus-Host Hastalığı (GvHD); donör T lenfositlerinin alıcının epitel hücrelerine (cilt, safra kanalları, bağırsak) saldırması",
                    "isCorrect": True,
                    "explanation": "Mükemmel Patoloji Bilgisi: Kemik iliği naklinde donör immün hücreleri immün yetmezlikli alıcının dokularını 'yabancı' olarak tanıyıp yok eder."
                },
                {
                    "text": "Alıcının plazma hücrelerinin donör iliğine karşı hiperakut kompleman hasarı yapması",
                    "isCorrect": False,
                    "explanation": "Hatalı; alıcı nakil öncesi miyeloablasyonla immün baskılanmıştır; hasarı yapan donör lenfositleridir."
                },
                {
                    "text": "Lösemi hücrelerinin kemik iliğini tekrar istila etmesi (nüks lösemi)",
                    "isCorrect": False,
                    "explanation": "Hatalı; döküntü, sarılık ve ishal GvHD'nin klasik hedef organ triadıdır."
                }
            ]
        ),
        48: make_branching_logic(
            "6 aylık erkek bebekte anne sütünden kesildikten sonra tekrarlayan bakteriyel pnömoni ve otit atakları başlıyor. Fizik muayenede tonsiller ve periferik lenf nodları palpe edilemiyor. Kanda B lenfositleri (CD19/CD20) tamamen yok.",
            "Bu konjenital immün yetmezliğin adı ve altta yatan moleküler defekt nedir?",
            [
                {
                    "text": "X'e Bağlı Agamaglobulinemi (Bruton Hastalığı); Bruton Tirozin Kinaz (BTK) gen mutasyonu",
                    "isCorrect": True,
                    "explanation": "Doğrudur; BTK pre-B hücrelerinin matür B lenfositlerine olgunlaşmasını sağlar; mutasyonunda B hücresi ve antikor üretimi sıfırlanır."
                },
                {
                    "text": "DiGeorge Sendromu; 22q11 delesyonuna bağlı timus aplazisi",
                    "isCorrect": False,
                    "explanation": "Hatalı; DiGeorge T hücre eksikliğidir ve paratiroid yokluğuna bağlı tetani görülür."
                },
                {
                    "text": "Ağır Kombine İmmün Yetmezlik (SCID); T ve B hücrelerinin birlikte yokluğu",
                    "isCorrect": False,
                    "explanation": "Hatalı; Bruton'da T hücre sayısı ve hücresel bağışıklık tamamen normaldir."
                }
            ]
        ),
        52: make_branching_logic(
            "Konjenital kalp anomalisi (fallot tetralojisi) ve hipokalsemik konvülsiyonlar ile doğan bir bebekte lateral akciğer grafisinde timus gölgesi izlenmiyor.",
            "Bu hastadaki kesin tanı ve embriyolojik gelişimsel defekt hangisidir?",
            [
                {
                    "text": "DiGeorge Sendromu; 3. ve 4. faringeal ceplerin gelişimsel hipoplazisi/aplazisi",
                    "isCorrect": True,
                    "explanation": "Kusursuz Embriyoloji ve Patoloji: 3. ve 4. faringeal ceplerden timus ve paratiroid bezleri gelişir; 22q11 delesyonunda ikisi de gelişemez."
                },
                {
                    "text": "Wiskott-Aldrich Sendromu; trombositopeni, egzama ve WASP gen mutasyonu",
                    "isCorrect": False,
                    "explanation": "Hatalı; WASP gen defekti faringeal cep aplazisi ve hipokalsemi yapmaz."
                },
                {
                    "text": "Ataksi Telenjiektazi; ATM geni mutasyonuna bağlı serebellar ataksi",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu tablo DNA tamir defektidir."
                }
            ]
        ),
        54: make_branching_logic(
            "Bir bebekte T hücrelerinin tamamen yok olduğu, ADA (adenozin deaminaz) enzim eksikliği saptandığı ve hem hücresel hem humoral bağışıklığın çöktüğü belirleniyor.",
            "Bu tablonun tıbbi adı nedir?",
            [
                {
                    "text": "Ağır Kombine İmmün Yetmezlik (SCID - Severe Combined Immunodeficiency)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; ADA eksikliği toksik deoksiadenozin metabolitlerini biriktirerek lenfositleri öldürür ve otozomal resesif SCID yapar."
                },
                {
                    "text": "İzole IgA Eksikliği",
                    "isCorrect": False,
                    "explanation": "Hatalı; izole IgA eksikliğinde T hücreleri normaldir ve hastalar çoğunlukla asemptomatiktir."
                },
                {
                    "text": "Yaygın Değişken İmmün Yetmezlik (CVID)",
                    "isCorrect": False,
                    "explanation": "Hatalı; CVID genç erişkinlikte antikor yetmezliği ile ortaya çıkar, bebekte ADA eksikliği SCID'dir."
                }
            ]
        ),
        56: make_branching_logic(
            "Trombositopeni, kanamaya eğilim, şiddetli egzama ve tekrarlayan kapsüllü bakteri enfeksiyonları olan bir erkek çocukta X'e bağlı kalıtılan immün yetmezlik düşünülüyor.",
            "Hücre iskelet aktin polimerizasyonunu bozan bu tablonun adı nedir?",
            [
                {
                    "text": "Wiskott-Aldrich Sendromu (WASP gen mutasyonu)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; trombositopeni (mikrotrombositler), egzama ve enfeksiyon Wiskott-Aldrich sendromunun klasik triadıdır."
                },
                {
                    "text": "Hiper-IgM Sendromu",
                    "isCorrect": False,
                    "explanation": "Hatalı; hiper-IgM'de CD40L mutasyonu vardır, egzama ve mikrotrombositopeni görülmez."
                },
                {
                    "text": "Chediak-Higashi Sendromu",
                    "isCorrect": False,
                    "explanation": "Hatalı; Chediak-Higashi'de dev lizozomlar ve parsiyel albinizm vardır."
                }
            ]
        ),
        58: make_branching_logic(
            "HIV virüsünün CD4+ T yardımcı lenfositlere tutunması ve membran füzyonu yaparak hücre içine girmesi basamağında rol alan viral yüzey glikoproteinleri hangileridir?",
            "gp120 ve gp41 glikoproteinlerinin hücre girişindeki spesifik fonksiyonel iş bölümü nedir?",
            [
                {
                    "text": "gp120 konak CD4 reseptörüne ve kemokin koreseptörüne (CCR5/CXCR4) bağlanır; gp41 ise viral zarfın hücre zarıyla füzyonunu sağlar",
                    "isCorrect": True,
                    "explanation": "Mükemmel Moleküler Viroloji Bilgisi: gp120 bağlanma proteinidir, gp41 transmembran füzyon peptitidir."
                },
                {
                    "text": "gp41 konak hücresine tutunurken gp120 virüsün ters transkripsiyonunu katalizler",
                    "isCorrect": False,
                    "explanation": "Hatalı; ters transkripsiyonu glikoproteinler değil viral reverse transcriptase enzimi yapar."
                },
                {
                    "text": "Her iki glikoprotein de konak çekirdeğine girerek insan genomunu parçalar",
                    "isCorrect": False,
                    "explanation": "Hatalı; glikoproteinler viral zarf bileşenleridir, çekirdek entegrasyonunu integraz enzimi yürütür."
                }
            ]
        ),
        62: make_branching_logic(
            "HIV bulaşının erken evrelerinde virüsün makrofajlara ve dendritik hücrelere girmesini sağlayan kemokin koreseptörü CCR5'tir.",
            "Toplumda bazı bireylerin HIV bulaşına karşı doğal dirençli olmasını sağlayan genetik mutasyon nedir?",
            [
                {
                    "text": "CCR5 geninde 32 baz çiftlik homozigot delesyon (CCR5-delta32 mutasyonu)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; homozigot delta-32 mutasyonu taşıyan bireylerde fonksiyonel CCR5 reseptörü sentezlenemez ve R5 suşu HIV virüsü hücreye giremez."
                },
                {
                    "text": "CD4 geninin tamamen susturulması",
                    "isCorrect": False,
                    "explanation": "Hatalı; CD4 hayat için esansiyeldir ve silinmesi immün sistem çöküşü yapar."
                },
                {
                    "text": "HLA-B27 alelinin aşırı ekspresyonu",
                    "isCorrect": False,
                    "explanation": "Hatalı; HLA-B27 ankilozan spondilit ile ilişkilidir, HIV direnci sağlamaz."
                }
            ]
        ),
        64: make_branching_logic(
            "HIV pozitif bir hastada CD4+ T lenfosit sayısı 140/mikrolitreye düştüğünde kuru öksürük ve nefes darlığı gelişiyor. Akciğer biyopsisinde alveollerde pembe köpüksü eksüda ve gümüş boyasında fincan tabağı şeklinde mikroorganizmalar izleniyor.",
            "Bu hastadaki kesin fırsatçı enfeksiyon tanısı nedir?",
            [
                {
                    "text": "Pneumocystis jirovecii (PCP) pnömonisi; AIDS tanımlayıcı en klasik fungal enfeksiyon",
                    "isCorrect": True,
                    "explanation": "Doğrudur; CD4 < 200 eşiğinde PCP pnömonisi AIDS tanımlayıcı en tipik fırsatçı patolojidir."
                },
                {
                    "text": "Streptococcus pneumoniae lober pnömonisi",
                    "isCorrect": False,
                    "explanation": "Hatalı; pnömokok bakteriyeldir ve alveollerde nötrofilik eksüda yapar, gümüş boyalı fincan kistleri P. jirovecii'ye özgüdür."
                },
                {
                    "text": "Mycobacterium leprae enfeksiyonu",
                    "isCorrect": False,
                    "explanation": "Hatalı; lepra periferik sinirleri ve cildi tutar."
                }
            ]
        )
    }

def get_extra_causal_chains():
    """Causal chain (mekanizma zinciri) ögeleri (14 adet)."""
    return {
        3: make_causal_chain(
            "Tip I Aşırı Duyarlılıkta Sistemik Anafilaksi Zinciri",
            [
                "1. Duyarlanma: Antijenin B hücrelerince IgE üretimine yol açması ve mast hücre Fc-epsilon-RI reseptörlerine bağlanması",
                "2. Çapraz Bağlanma: Tekrar giren antijenin mast hücresindeki komşu IgE moleküllerini çapraz bağlaması",
                "3. Granül Boşalması: Saniyeler içinde histamin, nötrofil kemotaktik faktör ve proteazların ekzositozu",
                "4. Lipid Mediyatörler: Fosfolipaz aktivasyonu ile lökotrienler (LTC4, LTD4, LTE4) ve PGD2 sentezi",
                "5. Sistemik Şok: Masif periferik vazodilatasyon, laringeal ödem ve bronkospazm ile kardiyovasküler kollaps"
            ]
        ),
        7: make_causal_chain(
            "Tip II Antikor Bağımlı Hücre Aracılı Sitotoksisite (ADCC) Zinciri",
            [
                "1. Opsonizasyon: Hedef hücre yüzey antijenlerine IgG antikorlarının bağlanması",
                "2. Efektör Tanıma: NK hücrelerinin Fc-gama-RIII (CD16) reseptörüyle bağlı IgG'nin Fc ucunu yakalaması",
                "3. Polarizasyon: NK hücresinin litik granüllerini temas yüzeyine doğru yönlendirmesi",
                "4. Hedef Lizisi: Perforin porları açılması ve granzim enzimleriyle hedef hücrenin apoptoza sokulması"
            ]
        ),
        13: make_causal_chain(
            "Tip III Hipersensitivitede Akut İmmün Kompleks Vasküliti",
            [
                "1. Kompleks Oluşumu: Dolaşımda çözünür antijen ve antikorların birleşerek orta büyüklükte immün kompleksler yapması",
                "2. Duvara Çökme: Artmış vasküler permeabilite zemininde komplekslerin arteriyol duvarlarına çökmesi",
                "3. Kompleman Aktivasyonu: Çöken komplekslerin C5a ve C3a üreterek nötrofilleri odak noktasına çekmesi",
                "4. Fibrinoid Nekroz: Nötrofil enzimlerinin damar duvarını eritmesi ve plazma proteinlerinin pıhtılaşmasıyla fibrinoid nekroz"
            ]
        ),
        17: make_causal_chain(
            "Tip IV Gecikmiş Tip Granülomatöz İnflamasyon Zinciri",
            [
                "1. Antijen Sunumu: Dendritik hücrelerin antijeni naif CD4+ T hücrelerine MHC Sınıf II ile sunması",
                "2. Th1 Farklılaşması: IL-12 uyarısıyla naif lenfositlerin efektör Th1 fenotipine dönüşmesi",
                "3. İnterferon-Gama Salınımı: Th1 hücrelerinin dokuda yoğun IFN-gama salgılaması",
                "4. Epiteloid Dönüşüm: Makrofajların aktive olarak epiteloid histiyositlere ve çok çekirdekli dev hücrelere dönüşmesi",
                "5. Granülom Sınırlandırması: Merkezinde nekroz çevresinde lenfosit yakası olan organize granülom oluşumu"
            ]
        ),
        23: make_causal_chain(
            "SLE Patogenezinde Apoptoz Artıkları ve Tip I İnterferon Döngüsü",
            [
                "1. Klirens Yetersizliği: Apoptoza giden hücre artıklarının ve nükleer nükleozomların temizlenememesi",
                "2. TLR Aktivasyonu: Serbest nükleer DNA/RNA'ların dendritik hücrelerdeki TLR7 ve TLR9'u uyarması",
                "3. İnterferon İmzası: Plazmasitoid dendritik hücrelerden masif Tip I İnterferon (IFN-alfa) fırtınası kopması",
                "4. B Hücre Çoğalması: Nükleer antijenlere özgül B hücrelerinin uyarılıp anti-dsDNA ve anti-Sm üretmesi",
                "5. Organ Vasküliti: İmmün komplekslerin glomerül ve deride birikerek yaygın nekrotizan vaskülit yapması"
            ]
        ),
        27: make_causal_chain(
            "Romatoid Artritte Pannus Oluşumu ve Kıkırdak Harabiyeti Zinciri",
            [
                "1. T Hücre İmmünitesi: Sinovyada Th1 ve Th17 lenfositlerinin sitokinler (TNF-alfa, IL-1, IL-6) salgılaması",
                "2. Sinovyal Hiperplazi: Sinovyal fibroblastların kontrolsüz çoğalarak kalın, villöz bir örtüye dönüşmesi",
                "3. Pannus İnvazyonu: Anjiyogenez eşliğinde granülasyon dokusunun eklem kıkırdağı üzerine doğru yürümesi",
                "4. Enzimatik Sindirim: Kondrosit ve fibroblastlardan salınan matriks metalloproteinazların (MMP) kıkırdağı eritmesi",
                "5. Fibröz ve Kemik Ankiloz: Kıkırdak kaybı sonrası eklem yüzlerinin kaynaşması ve kalıcı deformite"
            ]
        ),
        33: make_causal_chain(
            "Sjögren Sendromunda Ekzokrin Bez Atrofisi Mekanizması",
            [
                "1. Duktal Tetiklenme: Tükürük ve gözyaşı bezi duktus epitelinde viral veya çevresel hasar oluşması",
                "2. Lenfosit İnfiltrasyonu: Asinüsler çevresine CD4+ T hücreleri ve plazma hücrelerinin organize odaklanması",
                "3. Otoantikor Üretimi: Lokal B lenfositlerince Anti-SSA (Ro) ve Anti-SSB (La) üretilmesi",
                "4. Asiner Apoptoz: Perforin ve FasL yolağıyla salgı yapan asinüs epitel hücrelerinin yok edilmesi",
                "5. Kserostomi ve Sikka: Salgı kaybıyla ağız kuruluğu, keratokonjonktivit sikka ve parotis şişmesi"
            ]
        ),
        37: make_causal_chain(
            "Sistemik Sklerozda Mikrovasküler Hasardan Yaygın Fibroza Giden Yol",
            [
                "1. Endotel Hasarı: Bilinmeyen tetikleyiciyle mikrovasküler endotel hücrelerinin hasarlanması ve apoptozu",
                "2. İntimal Proliferasyon: Hasarlı damarlarda PDGF ve endotelin-1 salınımıyla konsantrik intimal kalınlaşma",
                "3. Dokuda Hipoksi: Kapiller lümenlerin tıkanması ve doku iskemisi gelişmesi",
                "4. Fibroblast Aktivasyonu: İskemik ortamda makrofajlardan TGF-beta ve PDGF patlaması",
                "5. Masif Kollajen Birikimi: Fibroblastların durmaksızın Tip I ve Tip III kollajen üreterek organları sklerozlaması"
            ]
        ),
        43: make_causal_chain(
            "Akut Allogreft Hücresel Rejeksiyon Mekanizması",
            [
                "1. Donör Antijeni Sunumu: Greftteki lökositlerin donör HLA moleküllerini alıcı T hücrelerine sunması",
                "2. Alloreaktif T Aktivasyonu: Alıcı CD4+ Th1 ve CD8+ CTL klonlarının hızla çoğalması",
                "3. Vasküler İnfiltrasyon: CTL'lerin greft böbrek endoteline ve tübül epitel hücrelerine tutunması",
                "4. Endotelit ve Tübülit: Perforin ve granzimlerle tübül ve damar hücrelerinin öldürülmesi",
                "5. Greft İskemisi: Damar içi tromboz ve tübüler nekroz ile böbrek fonksiyonunun akut bozulması"
            ]
        ),
        47: make_causal_chain(
            "Bruton Hastalığında Antikor Üretiminin Çöküş Zinciri",
            [
                "1. Genetik Mutasyon: X kromozomundaki Bruton Tirozin Kinaz (BTK) geninde mutasyon olması",
                "2. Sinyal Yolağı Blokajı: Pre-B reseptöründen çekirdeğe büyüme ve hayatta kalma sinyalinin iletilememesi",
                "3. Apoptoz ve Arrest: Kemik iliğinde pre-B hücrelerinin matür B lenfositlerine dönüşemeden ölmesi",
                "4. Periferik Dolaşımda B Yokluğu: Kanda ve lenfoid organlarda CD19+/CD20+ B lenfositlerin sıfırlanması",
                "5. Agamaglobulinemi: Plazma hücresi oluşamadığı için tüm immünoglobulin sınıflarının (IgG, IgA, IgM) çökmesi"
            ]
        ),
        53: make_causal_chain(
            "HIV Replikasyonu ve Proviral Entegrasyon Basamakları",
            [
                "1. Reseptör Bağlanması: Viral gp120'nin konak CD4 molekülüne ve kemokin koreseptörüne (CCR5/CXCR4) kilitlenmesi",
                "2. Membran Füzyonu: gp41 konformasyon değişimiyle viral zarı konak plazma zarıyla kaynaştırması",
                "3. Ters Transkripsiyon: Viral RNA genomunun viral Reverse Transcriptase ile çift iplikli cDNA'ya çevrilmesi",
                "4. Nükleer Entegrasyon: Viral İntegraz enziminin viral DNA'yı konak kromozomuna kovalent olarak eklemesi",
                "5. Matürasyon ve Tomurcuklanma: Viral proteazın öncül proteinleri keserek enfektif viryonları dışarı salması"
            ]
        ),
        57: make_causal_chain(
            "AIDS Döneminde CD4+ T Hücre Tükenmesi ve İmmün Çöküş",
            [
                "1. Direkt Sitopatik Etki: Virüs replikasyonu sırasında plazma membran geçirgenliğinin bozulması ve hücre lizisi",
                "2. Pyroptoz İndüksiyonu: Enfekte olmayan 'seyirci' CD4 T hücrelerinde kaspaz-1 aktivasyonuyla inflamatuar hücre ölümü",
                "3. Sinsisya Teşekkülü: gp120 taşıyan enfekte hücrelerin sağlam CD4 hücreleriyle birleşip dev çok çekirdekli ölü kitleler yapması",
                "4. İmmün Sistem Felci: CD4 sayısı <200/mikrolitreye inerek antikor üretimi ve hücresel bağışıklığın tamamen felç olması"
            ]
        ),
        63: make_causal_chain(
            "AA Amiloidozunda Serum Amiloid A'dan Glomerüler Harabiyete",
            [
                "1. Kronik Yangı: Osteomiyelit, RA veya FMF zemininde persistan makrofaj uyarımı",
                "2. Karaciğer Uyarısı: Makrofaj kaynaklı IL-6 ve IL-1 sitokinlerinin hepatositleri uyarması",
                "3. SAA Patlaması: Karaciğerden dolaşıma Serum Amiloid A akut faz proteininin bin kat artarak pompalanması",
                "4. Kısmi Proteoliz: Doku makrofajlarının SAA'yı çözünmeyen 8.5 kDa'lık AA fibril parçalarına budaması",
                "5. Mezangiyal Çöküş: Fibrillerin glomerül mezangiyumuna çökerek masif nefrotik sendrom yapması"
            ]
        ),
        67: make_causal_chain(
            "AL Amiloidozunda Hafif Zincir Klonalitesinden Kalp Yetmezliğine",
            [
                "1. Plazma Hücre Klonu: Kemik iliğinde neoplastik veya klonal plazma hücrelerinin kontrolsüz çoğalması",
                "2. Monoklonal Hafif Zincir: Fazla miktarda lambda veya kappa serbest immünoglobulin hafif zinciri üretimi",
                "3. Yanlış Katlanma: Hafif zincirlerin proteolitik dirençli çapraz beta-kırmalı fibriller halinde katlanması",
                "4. Miyokardiyal İnfiltrasyon: Fibrillerin kalp kası lifleri arasına birikerek ventrikül duvarlarını sertleştirmesi",
                "5. Restriktif Kardiyomiyopati: Diyastolik doluş çöküşü, düşük voltajlı EKG ve ölümcül aritmiler"
            ]
        )
    }

def get_extra_cloze():
    """Cloze masking (boşluk doldurma) ögeleri (10 adet)."""
    return {
        5: make_cloze(
            "Tip I aşırı duyarlılık reaksiyonlarında mast hücre yüzeyindeki yüksek afiniteli IgE reseptörüne Fc-epsilon-RI adı verilir.",
            "Fc-epsilon-RI",
            "Mast hücresi ve bazofillerde antikorun sabit kuyruk parçasını bağlayan yüksek afiniteli almaç kompleksi"
        ),
        15: make_cloze(
            "Büllöz pemfigoid hastalığında dermoepidermal bileşkede hemidesmozom antijenlerine karşı subepidermal bül oluşur.",
            "subepidermal",
            "Epidermis tabakasının bazal membran üzerinden dermisten tam kat ayrıldığı histolojik derinlik seviyesi"
        ),
        25: make_cloze(
            "Sistemik lupus eritematozus hastalarında böbrek hasarı aktivitesini ve nefrit alevlenmesini en iyi takip eden otoantikor anti-dsDNA antikorudur.",
            "anti-dsDNA",
            "Çift sarmallı deoksiribonükleik asit molekülüne özgül yüksek afiniteli antinükleer belirteç"
        ),
        35: make_cloze(
            "Sjögren sendromunda tükürük bezi parankimine yoğun lenfosit infiltrasyonu fokus skoru ile histopatolojik olarak derecelendirilir.",
            "fokus skoru",
            "Dudak biyopsisinde minör tükürük bezi kesitlerinde elli veya daha fazla mononükleer hücre içeren odakların sayımı"
        ),
        45: make_cloze(
            "Diffüz sistemik skleroz hastalarında ağır visseral fibroz ve akciğer tutulumu ile ilişkili otoantikor Anti-Scl-70 antikorudur.",
            "Anti-Scl-70",
            "DNA topoizomeraz-1 enzimini hedefleyen ve diffüz sklerodermada pozitifleşen serolojik antikor"
        ),
        55: make_cloze(
            "X'e bağlı agamaglobulinemi hastalarında pre-B hücrelerinin olgunlaşmasını durduran mutasyon Bruton tirozin kinaz genindedir.",
            "Bruton tirozin kinaz",
            "B hücre reseptör sinyal yolağında sitoplazmik fosforilasyon yapan kritik tirosin kinaz enzimi"
        ),
        65: make_cloze(
            "HIV virüsünün konağa ilk bulaşında ve erken enfeksiyon fazında kullandığı temel kemokin koreseptörü CCR5 reseptörüdür.",
            "CCR5",
            "Makrofaj ve dendritik hücrelerin yüzeyindeki beta-kemokin almaç proteini"
        ),
        75: make_cloze(
            "Kongo kırmızısı boyası ile boyanan amiloid birikintileri polarize ışık mikroskobunda patognomonik elma yeşili çift kırıcılık verir.",
            "elma yeşili",
            "Polarize filtreler altında amiloid beta tabakalarının saçtığı karakteristik zümrüt pırıltısı rengi"
        ),
        85: make_cloze(
            "Kronik inflamasyon, romatoid artrit ve FMF zemininde karaciğerden sentezlenen proteinden köken alan amiloid türü AA amiloidozudur.",
            "AA amiloidozudur",
            "Akut faz reaktanı SAA molekülünden türeyen sistemik sekonder amiloidoz tablosu"
        ),
        95: make_cloze(
            "Sistemik amiloidoz kuşkusu olan bir hastada majör organ kanamasından kaçınmak için ilk tercih edilen güvenli doku biyopsisi abdominal yağ aspirasyonudur.",
            "abdominal yağ",
            "Göbek çevresindeki cilt altı stromal dokudan ince enjektörle yapılan minimal invaziv örnekleme alanı"
        )
    }

def get_extra_sliders():
    """Before/After slider (karşılaştırmalı durum) ögeleri (4 adet)."""
    return {
        72: make_before_after(
            "HIV Enfeksiyonunda Faz Değişimi ve Hücresel Profil",
            "Erken Asemptomatik Klinik Latent Dönem",
            "CD4 sayısı >500/mikrolitre; lenfoid organlarda aktif viral replikasyon devam ederken kanda asemptomatik tablo",
            "Geç Kriz Dönemi (AIDS)",
            "CD4 sayısı <200/mikrolitreye düşer; immün sistem çöker, fırsatçı enfeksiyonlar ve sekonder neoplaziler patlar"
        ),
        74: make_before_after(
            "Santral ve Periferik İmmün Tolerans Ayrımı",
            "Santral Tolerans (Timus ve Kemik İliği)",
            "Kendi antijenlerini yüksek afiniteyle tanıyan klonların negatif seleksiyonla (klonal delesyon) doğrudan apoptoza gönderilmesi",
            "Periferik Tolerans (Lenf Nodları ve Dokular)",
            "Kaçan otoreaktif hücrelerin anerjiye sokulması, Treg hücrelerince baskılanması veya FasL yolağıyla intihar ettirilmesi"
        ),
        82: make_before_after(
            "İmmün Kompleks Boyutu ve Klirens Dinamiği",
            "Büyük İmmün Kompleksler (Antikor Fazlalığı)",
            "Makrofajların Fc ve kompleman reseptörlerince hızla fagositozla kandan temizlenir; dokuya çöküp vaskülit yapamaz",
            "Orta Büyüklükte Çözünür Kompleksler (Hafif Antijen Fazlalığı)",
            "Fagositozdan kaçar, dolaşımda uzun süre gezinir ve vasküler bazal membranlara çökerek ağır nekrotizan vaskülit yapar"
        ),
        84: make_before_after(
            "Amiloidoz Fibril Çapı ve Işık Mikroskopisi Zıtlığı",
            "Işık Mikroskopisinde Rutin H&E",
            "Tamamen asellüler, amorf, yapısız ve camsı hiyalin pembe birikinti (Nonspesifik ve kollajenle karışabilir)",
            "Elektron Mikroskopisinde Ultrastrüktür",
            "7.5 ile 10 nm çapında son derece düzenli, dallanmayan, düz ve rijit sert protein nanofibrilleri"
        )
    }

def enrich_slides(slides):
    """Slaytlara ek interaktif elemanları yerleştirir ve dengeler."""
    extra_branching = get_extra_branching()
    extra_chains = get_extra_causal_chains()
    extra_cloze = get_extra_cloze()
    extra_sliders = get_extra_sliders()

    for slide in slides:
        s_num = slide.get("slideNumber", 0)
        elems = slide.get("interactiveElements", [])

        if s_num in extra_branching:
            elems.append(extra_branching[s_num])
        if s_num in extra_chains:
            elems.append(extra_chains[s_num])
        if s_num in extra_cloze:
            elems.append(extra_cloze[s_num])
        if s_num in extra_sliders:
            elems.append(extra_sliders[s_num])

        slide["interactiveElements"] = elems

    return slides
