# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.

Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar:
- branching_logic: +18 adet (toplam 27, ~%11.3)
- causal_chain: +12 adet (toplam 27, ~%11.3)
- micro_quiz: +13 adet (toplam 27, ~%11.3)
- before_after_slider: +5 adet (toplam 27, ~%11.3)
"""

from scripts.k1_29_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar senaryoları) ek ögeleri (18 adet)."""
    return {
        3: make_branching_logic(
            "Akciğer adenokarsinomu saptanan 56 yaşındaki hiç sigara içmemiş kadın hastanın moleküler patoloji biyopsisinde EGFR ekzon 19 delesyonu tespit edilmiştir.",
            "Bu hastada onkoloji konseyinde birinci basamakta tercih edilecek en akılcı hedefe yönelik tedavi yaklaşımı ne olmalıdır?",
            [
                {
                    "text": "EGFR tirozin kinaz inhibitörü (erlotinib, osimertinib gibi TKI) başlanmalıdır; çünkü mutant kinaz alanı bu inhibitörlere dramatik duyarlılık gösterir.",
                    "isCorrect": True,
                    "explanation": "EGFR aktive edici mutasyonları taşıyan akciğer adenokarsinomları tirozin kinaz inhibitörlerine yüksek yanıt oranı verir."
                },
                {
                    "text": "EGFR mutasyonu direnç belirteci olduğundan hedefe yönelik ilaçlar kesinlikle kontrendikedir ve sadece palyatif radyoterapi verilmelidir.",
                    "isCorrect": False,
                    "explanation": "Aksine ekzon 19 delesyonu TKI duyarlılığının en güçlü prediktif belirtecidir."
                },
                {
                    "text": "Doğrudan anti-CD20 antikoru olan rituksimab başlanmalıdır.",
                    "isCorrect": False,
                    "explanation": "Rituksimab B hücreli lenfomalarda kullanılır, EGFR mutant akciğer kanserinde yeri yoktur."
                }
            ]
        ),
        5: make_branching_logic(
            "Meme karsinomu rezeksiyon materyalinde immünhistokimya ile HER2/neu proteini 3+ kuvvetli membranöz boyanma gösteren 48 yaşındaki kadın hasta değerlendirilmektedir.",
            "Bu tümörün biyolojik davranışı ve uygulanacak hedefe yönelik tedavi stratejisi açısından en doğru patolojik ve klinik karar nedir?",
            [
                {
                    "text": "HER2 gen amplifikasyonuna bağlı reseptör aşırı ekspresyonu mevcuttur; trastuzumab (anti-HER2 monoklonal antikor) tedavisi planlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "HER2 aşırı ekspresyonu agresif seyirle ilişkilidir ancak trastuzumab tedavisiyle belirgin sağkalım artışı elde edilir."
                },
                {
                    "text": "HER2 3+ boyanma tümörün benign bir lezyon olduğunu gösterir ve ek onkolojik tedaviye ihtiyaç duyulmaz.",
                    "isCorrect": False,
                    "explanation": "HER2 bir onkoprotein olup aşırı ekspresyonu malign karsinomlarda kötü prognostik faktördür."
                },
                {
                    "text": "İmmünhistokimya 3+ boyanma negatif kabul edilir ve floresan in situ hibridizasyon (FISH) ile mutasyon taranmasına gerek yoktur.",
                    "isCorrect": False,
                    "explanation": "3+ boyanma doğrudan pozitif kabul edilir, şüpheli (2+) olgularda FISH doğrulaması istenir."
                }
            ]
        ),
        12: make_branching_logic(
            "Metastatik malign melanom tanısıyla takip edilen 52 yaşındaki erkek hastanın tümör dokusunda BRAF V600E mutasyonu saptanmıştır.",
            "Bu hastada MAP kinaz yolağını hedeflemek amacıyla hangi hedefe yönelik ilaç kombinasyonu en uygundur?",
            [
                {
                    "text": "BRAF inhibitörü (vemurafenib/dabrafenib) ile MEK inhibitörü (trametinib) kombinasyonu verilmelidir.",
                    "isCorrect": True,
                    "explanation": "BRAF V600E mutasyonunda BRAF ve MEK kombine blokajı, tekli ajan direncini geciktirerek en yüksek klinik yanıtı sağlar."
                },
                {
                    "text": "Yalnızca yüksek doz metotreksat ve alkilleyici ajan verilmeli, kinaz inhibitörlerinden kaçınılmalıdır.",
                    "isCorrect": False,
                    "explanation": "Metotreksat antimetabolittir; BRAF mutant melanomda öncelikli tercih hedefe yönelik BRAF/MEK inhibitörleridir."
                },
                {
                    "text": "BRAF mutasyonu varlığında tüm kinaz inhibitörleri toksik şok oluşturacağından tedavi tamamen kesilmelidir.",
                    "isCorrect": False,
                    "explanation": "Bu mutasyon doğrudan hedeflenebilir moleküler bir anomalidir ve hedefe yönelik tedavi endikasyonudur."
                }
            ]
        ),
        16: make_branching_logic(
            "Kronik miyeloid lösemi (KML) şüphesiyle kemik iliği biyopsisi yapılan hastada sitogenetik analizde t(9;22)(q34;q11) translokasyonu (Philadelphia kromozomu) saptanmıştır.",
            "Oluşan BCR-ABL füzyon proteininin patolojik aktivitesini durdurmak için klinik pratikte devrim yaratan hangi ajan tercih edilmelidir?",
            [
                {
                    "text": "BCR-ABL kinazının ATP bağlanma cebini kompetitif olarak bloke eden imatinib (tirozin kinaz inhibitörü) başlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "İmatinib constitutively aktif BCR-ABL kinazını spesifik olarak inhibe ederek KML remisyonunu sağlar."
                },
                {
                    "text": "Hücre zarındaki lipid sentezini durduran statin grubu kolesterol düşürücü ilaçlar verilmelidir.",
                    "isCorrect": False,
                    "explanation": "Statinler HMG-CoA redüktaz inhibitörüdür, tirozin kinaz onkoproteinini bloke etmez."
                },
                {
                    "text": "BCR-ABL füzyonu DNA replikasyonunu doğrudan hızlandırmadığı için sadece flebotomi ile lökositler uzaklaştırılmalıdır.",
                    "isCorrect": False,
                    "explanation": "BCR-ABL kesintisiz mitojenik sinyal üreten güçlü bir sitoplazmik kinazdır, sistemik TKI tedavisi şarttır."
                }
            ]
        ),
        23: make_branching_logic(
            "Retinoblastom tanısı alan 18 aylık bir bebeğin bilateral tümör geliştirdiği ve ailesinde retinoblastom öyküsü bulunduğu öğrenilmiştir.",
            "Knudson'ın çift darbe (two-hit) hipotezi ışığında bu hastadaki genetik sapmanın doğası nasıl açıklanır?",
            [
                {
                    "text": "İlk darbe ebeveynden germline olarak kalıtılmıştır, ikinci darbe ise retina hücresinde somatik olarak kazanılmış ve homozigot inaktivasyon oluşmuştur.",
                    "isCorrect": True,
                    "explanation": "Ailesel retinoblastomda germline tek mutant alel tüm vücutta bulunur; retina hücresinde ikinci somatik mutasyonla bilateral tümör gelişir."
                },
                {
                    "text": "Her iki darbe de aynı anda fertilizasyon sırasında mitokondriyal DNA'da meydana gelmiştir.",
                    "isCorrect": False,
                    "explanation": "RB geni çekirdekte kromozom 13q14'te kodlanır, mitokondriyal kalıtımla ilişkisizdir."
                },
                {
                    "text": "Retinoblastom yalnızca onkogen amplifikasyonuyla gelişir ve tümör baskılayıcı gen inaktivasyonu söz konusu değildir.",
                    "isCorrect": False,
                    "explanation": "RB klasik bir tümör baskılayıcı gendir ve çift darbe ile inaktive olur."
                }
            ]
        ),
        27: make_branching_logic(
            "Genç yaşta osteosarkom, meme karsinomu, yumuşak doku sarkomu ve lösemi öyküsü bulunan çok sayıda bireyin olduğu bir ailede Li-Fraumeni sendromu düşünülmektedir.",
            "Bu sendromun moleküler patogenezini doğrulamak için taranması gereken birincil gen hangisidir?",
            [
                {
                    "text": "TP53 geni sekanslanarak germline heterozigot inaktive edici mutasyon varlığı araştırılmalıdır.",
                    "isCorrect": True,
                    "explanation": "Li-Fraumeni sendromu TP53 genindeki germline inaktivasyon sonucu çoklu organ maligniteleriyle karakterizedir."
                },
                {
                    "text": "Yalnızca HLA-B27 doku grubu alleli taranmalıdır.",
                    "isCorrect": False,
                    "explanation": "HLA-B27 ankilozan spondilit ile ilişkilidir, kanser predispozisyon sendromu belirteci değildir."
                },
                {
                    "text": "Mitokondriyal sitokrom c oksidaz gen dizilimi taranmalıdır.",
                    "isCorrect": False,
                    "explanation": "Li-Fraumeni sendromunun etiyolojik nedeni nükleer TP53 tümör baskılayıcı gen mutasyonudur."
                }
            ]
        ),
        34: make_branching_logic(
            "Ailesel Adenomatöz Polipozis (FAP) tanısı alan 22 yaşındaki bir hastada kolonoskopide kolonda yüzlerce adenomatöz polip saptanmıştır.",
            "Wnt/β-katenin yolağının kontrolsüz aktivasyonuna neden olan APC proteininin moleküler işlevi nedir?",
            [
                {
                    "text": "APC, normalde sitoplazmik β-katenin yıkım kompleksinde yer alarak onu fosforilasyona ve proteazomal yıkıma yönlendirir; kaybında serbest kalan β-katenin nükleusa geçerek proliferasyonu tetikler.",
                    "isCorrect": True,
                    "explanation": "APC yıkım kompleksinin temel bileşenidir; mutasyonunda β-katenin parçalanamaz ve nükleusta sürekli transkripsiyonu uyarır."
                },
                {
                    "text": "APC hücre zarında kalsiyum kanalı olarak görev yaparak hücreye kalsiyum girişini engeller.",
                    "isCorrect": False,
                    "explanation": "APC iyon kanalı değil, sitoplazmik iskele ve yıkım kompleksi proteinidir."
                },
                {
                    "text": "APC proteini直接 ribozomlara bağlanarak protein sentezini global düzeyde durdurur.",
                    "isCorrect": False,
                    "explanation": "APC spesifik olarak Wnt sinyal iletiminde β-katenin homeostazını denetler."
                }
            ]
        ),
        38: make_branching_logic(
            "Von Hippel-Lindau (VHL) sendromlu bir hastada bilateral berrak hücreli renal hücreli karsinom ve serebellar hemanjioblastom saptanmıştır.",
            "VHL gen mutasyonunun tümörde masif vaskülarizasyon ve neovaskülarizasyona yol açmasının altında yatan patolojik mekanizma nedir?",
            [
                {
                    "text": "VHL proteini hipoksi ile indüklenen faktör-1α (HIF-1α) yıkımını sağlar; kaybında normokside bile HIF-1α birikerek kontrolsüz VEGF transkripsiyonunu başlatır.",
                    "isCorrect": True,
                    "explanation": "VHL bir ubiquitin ligaz kompleksidir; yokluğunda HIF-1a parçalanamaz ve güçlü anjiyogenik faktör VEGF'yi salgılatır."
                },
                {
                    "text": "VHL doğrudan trombositleri parçalayarak serbest heparini ortama salar.",
                    "isCorrect": False,
                    "explanation": "VHL pıhtılaşma faktörü değil, transkripsiyon faktörü regülatörüdür."
                },
                {
                    "text": "VHL mutasyonu endotel hücrelerinde apoptozu hızlandırarak damarların tıkanmasına yol açar.",
                    "isCorrect": False,
                    "explanation": "Aksine VHL kaybı kontrolsüz yeni damar oluşumu (hemanjioblastom ve hipervasküler karsinom) ile sonuçlanır."
                }
            ]
        ),
        43: make_branching_logic(
            "Foliküler lenfoma tanısı konan 60 yaşındaki bir hastada t(14;18)(q32;q21) translokasyonu saptanmıştır.",
            "Bu translokasyon sonucunda BCL-2 geninin immünoglobulin ağır zincir (IgH) lokusuna taşınmasının neoplastik hücreye sağladığı temel avantaj nedir?",
            [
                {
                    "text": "BCL-2 anti-apoptotik proteininin aşırı üretimi sayesinde mitokondriyal membran bütünlüğü korunur ve hücre fizyolojik programlı ölümden kaçar.",
                    "isCorrect": True,
                    "explanation": "BCL-2 sitokrom c salınımını engelleyerek intrensek apoptozu bloke eder ve neoplastik B hücrelerinin sağkalımını uzatır."
                },
                {
                    "text": "Hücrelerin fagositoz yeteneğini artırarak çevre nötrofilleri yutmasını sağlar.",
                    "isCorrect": False,
                    "explanation": "BCL-2 fagositoz proteini değil, mitokondri dış zarında apoptozu engelleyen onkoproteindir."
                },
                {
                    "text": "Pro-apoptotik kaspaz enzimlerinin doğrudan sentezini uyararak hücreyi parçalar.",
                    "isCorrect": False,
                    "explanation": "BCL-2 kaspazları aktive etmez, tam tersine kaspaz kaskadının başlamasını önler."
                }
            ]
        ),
        47: make_branching_logic(
            "Tümör hücrelerinin sınırsız çoğalma (replikatif ölümsüzlük) kazanmasında telomeraz enziminin rolü incelenmektedir.",
            "Normal insan somatik hücreleri ile ileri evre karsinom hücreleri telomer dinamiği açısından karşılaştırıldığında hangisi doğrudur?",
            [
                {
                    "text": "Normal somatik hücrelerde telomeraz inaktiftir ve her bölünmede telomer kısalır; karsinom hücrelerinin %85-90'ında ise telomeraz reaktive edilerek telomer uzunluğu korunur.",
                    "isCorrect": True,
                    "explanation": "Telomeraz reaktivasyonu krizden ve replikatif yaşlanmadan (senescence) kaçışı sağlayarak tümöre ölümsüzlük kazandırır."
                },
                {
                    "text": "Normal somatik hücreler karsinom hücrelerine kıyasla 100 kat daha yüksek telomeraz aktivitesine sahiptir.",
                    "isCorrect": False,
                    "explanation": "Somatik hücrelerde telomeraz baskılanmıştır; sadece kök hücrelerde ve germ hücrelerinde aktiftir."
                },
                {
                    "text": "Karsinom hücrelerinde telomerlerin tamamen yok edilmesi mitoz bölünmeyi durduran temel mekanizmadır.",
                    "isCorrect": False,
                    "explanation": "Telomerlerin tükenmesi krize yol açar; tümör hücreleri telomerazı aktifleyerek bu krizi aşar."
                }
            ]
        ),
        53: make_branching_logic(
            "Kolorektal karsinomun karaciğer metastazı oluşturma sürecinde tümör hücrelerinin adezyon molekülleri incelenmektedir.",
            "Tümör hücrelerinin epitel tabakasından ayrılıp stromayı invaze etmesinde rol oynayan en kritik moleküler değişiklik nedir?",
            [
                {
                    "text": "E-kaderin ekspresyonunun kaybı ve epitelyal-mezenkimal geçiş (EMT) transkripsiyon faktörlerinin (SNAIL, TWIST) aktivasyonu gerçekleşir.",
                    "isCorrect": True,
                    "explanation": "E-kaderin homofilik hücre-hücre bağlantılarını sağlar; kaybı hücrelerin birbirinden koparak hareket etmesine yol açar."
                },
                {
                    "text": "Kollajen tip IV sentezinin aşırı artarak bazal membranı kalınlaştırması gerçekleşir.",
                    "isCorrect": False,
                    "explanation": "Bazal membranın kalınlaşması invazyonu engeller; tümör hücreleri kollajenaz (MMP) salgılayarak membranı eritir."
                },
                {
                    "text": "Hücrelerarası desmozom ve sıkı bağlantıların kovalent bağlarla pekiştirilmesi gerçekleşir.",
                    "isCorrect": False,
                    "explanation": "Bağlantıların pekişmesi hücreleri bir arada tutar; invazyonda bu bağlantılar dağıtılır."
                }
            ]
        ),
        58: make_branching_logic(
            "Metastatik karsinom hücrelerinin dolaşımdan hedef organ parankimine geçişi (ekstravazasyon) değerlendirilmektedir.",
            "Tümör embolisinin hedef organ kapiller yatağına tutunmasında ve organ tropizminde rol oynayan temel moleküler mekanizma hangisidir?",
            [
                {
                    "text": "Tümör hücresi adezyon moleküllerinin (integrinler) hedef organ endotel reseptörleriyle ve kemokin-kemokin reseptör (CXCR4/CXCL12) gradyanlarıyla etkileşimi.",
                    "isCorrect": True,
                    "explanation": "Organ tropizmi endotelyal adezyon molekülleri ve kemokin reseptör eksenleri (ör. meme kanserinde CXCR4) tarafından belirlenir."
                },
                {
                    "text": "Tümör hücrelerinin sadece eritrositlerle kovalent bağ kurarak pasif agregasyon oluşturması.",
                    "isCorrect": False,
                    "explanation": "Tümör embolileri trombositlerle kümelenebilir ancak ekstravazasyon spesifik integrin ve kemokin etkileşimleriyle yönetilir."
                },
                {
                    "text": "Metastaz yalnızca rastgele mekanik tıkanmayla gerçekleşir, moleküler reseptörlerin hiçbir rolü yoktur.",
                    "isCorrect": False,
                    "explanation": "Kemokin gradyanları ve adezyon molekülleri 'seed and soil' teorisinin moleküler temelini oluşturur."
                }
            ]
        ),
        63: make_branching_logic(
            "Klinik evreleme amacıyla 18F-FDG PET/BT çekilen akciğer karsinomlu bir hastada tümör dokusunda yoğun florodeoksiglukoz tutulumu (yüksek SUV değeri) izlenmiştir.",
            "Tümör dokusunun oksijen varlığında bile glukozu laktata fermente etmesine dayanan bu metabolik yeniden programlanma (Warburg etkisi) moleküler düzeyde tümöre hangi avantajı sağlar?",
            [
                {
                    "text": "Hızlı bölünen hücrenin ihtiyaç duyduğu nükleik asit, lipid ve aminoasit gibi biyosentetik yapıtaşlarının (karbon iskeletlerinin) bol miktarda sentezlenmesini sağlar.",
                    "isCorrect": True,
                    "explanation": "Warburg etkisi glikolitik ara ürünleri pentoz fosfat yolağına ve biyosentetik süreçlere yönlendirerek hızlı proliferasyona zemin hazırlar."
                },
                {
                    "text": "Hücre içi oksijen seviyesini sıfırlayarak mitokondrileri tamamen eritip yok eder.",
                    "isCorrect": False,
                    "explanation": "Mitokondriler erimez; metabolik ara ürün üretimi ve apoptoz regülasyonu için işlevsel kalırlar."
                },
                {
                    "text": "Tümörün glukoz yerine yalnızca serbest yağ asitlerini enerji kaynağı olarak kullanmasını zorunlu kılar.",
                    "isCorrect": False,
                    "explanation": "Warburg etkisinde temel yakıt ve anabolik hammadde kaynağı glukozdur."
                }
            ]
        ),
        67: make_branching_logic(
            "Glioblastoma multiforme rezeksiyon materyalinde IDH1 (izositrat dehidrogenaz 1) R132H mutasyonu saptanan 38 yaşındaki hastanın moleküler analizi yapılmaktadır.",
            "Mutant IDH enziminin ürettiği onkometabolit olan 2-hidroksiglutaratın (2-HG) neoplastik dönüşümü tetiklemedeki temel epigenetik mekanizması nedir?",
            [
                {
                    "text": "TET2 ve histon demetilaz enzimlerini kompetitif olarak inhibe ederek genomda yaygın DNA hipermetilasyonuna ve tümör baskılayıcı genlerin susturulmasına yol açar.",
                    "isCorrect": True,
                    "explanation": "2-HG bir onkometabolittir; alfa-ketoglutarat bağımlı dioksijenazları (TET2) inhibe ederek hipermetilasyon fenotipine (CIMP) neden olur."
                },
                {
                    "text": "Sitoplazmada doğrudan ATP sentezini 500 kat artırarak toksik enerji şokuna neden olur.",
                    "isCorrect": False,
                    "explanation": "2-HG enerji artışı yapmaz, epigenetik düzenleyici enzimleri bloke eder."
                },
                {
                    "text": "Hücre zarındaki sodyum-potasyum pompasını geri dönüşsüz parçalar.",
                    "isCorrect": False,
                    "explanation": "Onkometabolit mekanizması nükleer epigenetik susturma üzerinden işler."
                }
            ]
        ),
        73: make_branching_logic(
            "Kolon kanseri rezeksiyonu yapılan 45 yaşındaki hastanın biyopsisinde mikrosatellit instabilitesi yüksek (MSI-H) ve DNA uyumsuzluk onarım (MMR) proteini MSH2 kaybı saptanmıştır.",
            "Bu hastada immün kontrol noktası inhibitörlerine (anti-PD-1 / pembrolizumab) karşı beklenilen tedavi yanıtı ve gerekçesi nedir?",
            [
                {
                    "text": "Yüksek mutasyon yükü ve bol miktarda neomutasyon kaynaklı 'neoantijen' oluşumu nedeniyle immünoterapiye son derece dramatik ve kalıcı yanıt verir.",
                    "isCorrect": True,
                    "explanation": "MMR defektli MSI-H tümörler binlerce somatik mutasyon taşır; oluşan neoantijenler CD8+ T lenfositleri uyarır ve anti-PD-1 blokajına mükemmel yanıt sağlar."
                },
                {
                    "text": "MSI-H tümörler kesinlikle immün yanıttan yoksundur ve kontrol noktası inhibitörlerine primer dirençlidir.",
                    "isCorrect": False,
                    "explanation": "Tam tersine MSI-H tümörler immünoterapinin en başarılı olduğu solid karsinom grubudur."
                },
                {
                    "text": "MSI-H sadece B hücrelerini uyardığı için T hücre kontrol noktası tedavisinden etkilenmez.",
                    "isCorrect": False,
                    "explanation": "Tümör içi yoğun sitotoksik T lenfosit (TIL) infiltrasyonu mevcuttur ve T hücre aracılı yanıt baskındır."
                }
            ]
        ),
        77: make_branching_logic(
            "Kseroderma pigmentozum (XP) hastası olan 12 yaşındaki çocukta güneşe maruz kalan yüz derisinde çok sayıda skuamöz karsinom ve malign melanom gelişmiştir.",
            "Bu hastalarda UV ışığının oluşturduğu DNA hasarını onaramayan hangi moleküler mekanizma defektiftir?",
            [
                {
                    "text": "Pirimidin dimerlerini tanıyan ve uzaklaştıran nükleotid kesip çıkarma onarımı (Nucleotide Excision Repair - NER) mekanizması kalıtsal olarak bozuktur.",
                    "isCorrect": True,
                    "explanation": "UVB pirimidin (timin-timin) çapraz bağları yapar; bu hasar NER enzimleri (XPA-XPG) tarafından onarılır. XP'de NER mutasyonu vardır."
                },
                {
                    "text": "Mitokondriyal DNA polimeraz gama enziminin aşırı aktif çalışması.",
                    "isCorrect": False,
                    "explanation": "Sorun mitokondri değil, nükleer DNA'daki UV hasarının kesip çıkarılamamasıdır."
                },
                {
                    "text": "Baz kesip çıkarma onarımında (BER) görevli DNA ligaz IV mutasyonu.",
                    "isCorrect": False,
                    "explanation": "UV hasarı tipik olarak BER ile değil, NER ile onarılır."
                }
            ]
        ),
        83: make_branching_logic(
            "Karasal iklimde yaşayan ve uzun yıllar kömür/zift dumanına maruz kalan bir işçide meslek hastalığı olarak bronş karsinomu gelişmiştir.",
            "Polisiklik aromatik hidrokarbonların (ör. benzo[a]piren) karsinojenik etki göstermesi için vücutta hangi biyokimyasal dönüşüme uğraması gerekir?",
            [
                {
                    "text": "Karaciğer sitokrom P450 (CYP1A1) monooksijenaz enzimleriyle elektrofilik epoksit türevlerine metabolize edilerek DNA ile kovalent adükt oluşturması gerekir.",
                    "isCorrect": True,
                    "explanation": "Benzo[a]piren bir prokarsinojendir; CYP enzimleri tarafından nihai karsinojene dönüştürülerek DNA adüktleri yapar."
                },
                {
                    "text": "Mide asidinde hidroliz olarak doğrudan inaktif serbest azot gazına dönüşmesi gerekir.",
                    "isCorrect": False,
                    "explanation": "İnaktif gaza dönüşürse karsinojenik etki ortaya çıkmazdı."
                },
                {
                    "text": "Böbrek tübüllerinden hiçbir metabolik değişikliğe uğramadan süzülmesi yeterlidir.",
                    "isCorrect": False,
                    "explanation": "Endojen metabolik aktivasyon olmaksızın dolaylı karsinojenler DNA'ya bağlanamaz."
                }
            ]
        ),
        87: make_branching_logic(
            "Kronik Hepatit B virüsü (HBV) enfeksiyonu zemininde karaciğerinde multifokal hepatosellüler karsinom (HCC) saptanan 50 yaşındaki hasta incelenmektedir.",
            "HBV'nin karsinogenezdeki moleküler onkogenik mekanizması nasıl açıklanır?",
            [
                {
                    "text": "HBx proteini transkripsiyonu uyarır ve p53'ü inaktive eder; ayrıca virüs genomunun konak DNA'sına rastgele integrasyonu insersiyonel mutageneze yol açar.",
                    "isCorrect": True,
                    "explanation": "HBV'nin kodladığı HBx proteini kritik tümör baskılayıcıları inhibe ederken genomik integrasyon onkogenleri aktive edebilir."
                },
                {
                    "text": "HBV virüsü doğrudan vasküler endotel büyüme faktörü geni kodlar ve tümörü besler.",
                    "isCorrect": False,
                    "explanation": "Virüs VEGF kodlamaz; onkogenez HBx proteini, kronik rejenerasyon ve insersiyonel mutagenezle yürür."
                },
                {
                    "text": "Virüs yalnızca safra asitlerinin emilimini bozarak mekanik sarılık yapar, onkogenez yapmaz.",
                    "isCorrect": False,
                    "explanation": "HBV Dünya Sağlık Örgütü tarafından Grup 1 insan karsinojeni olarak tanımlanmış majör bir onkojenik virüstür."
                }
            ]
        )
    }

def get_extra_causal_chains():
    """Causal chain (fizyopatolojik mekanizma basamakları) ek ögeleri (12 adet)."""
    return {
        2: make_causal_chain(
            "Protoonkogenlerin Onkogene Dönüşüm Mekanizması",
            [
                "1. Genomik Hasar: Nokta mutasyonu, kromozom translokasyonu veya gen amplifikasyonu meydana gelir.",
                "2. Yapısal Modifikasyon: Kodlanan onkoprotein regülatör inhibisyon alanlarından kurtulur.",
                "3. Otonom Sinyal: Ligand veya büyüme faktörü uyarısı olmaksızın kesintisiz aktivasyon başlar.",
                "4. Neoplastik Proliferasyon: Çekirdeğe sürekli mitojenik sinyal iletilerek kontrolsüz hücre bölünmesi indüklenir."
            ]
        ),
        7: make_causal_chain(
            "RAS-RAF-MAPK Sinyal Kaskadı ve Onkogenik Kilitlenme",
            [
                "1. Reseptör Aktivasyonu: Büyüme faktörü RTK'ye bağlanır ve dimerizasyonla otofosforilasyon tetiklenir.",
                "2. Guanin Değişimi: SOS adaptör proteini RAS üzerindeki GDP'yi GTP ile değiştirerek RAS'ı aktive eder.",
                "3. Kaskad İletimi: Aktif RAS proteini sitoplazmada RAF (MAPKKK) ve MEK kinazlarını sırayla fosforiller.",
                "4. İntrensek GTPaz Kusuru: Onkojenik mutant RAS (G12D), GTP'yi hidrolize edemez ve sürekli aktif konumda kilitlenir.",
                "5. Transkripsiyon İndüksiyonu: Nükleusa göç eden ERK, MYC ve FOS gibi proliferatif genleri kesintisiz transkribe eder."
            ]
        ),
        13: make_causal_chain(
            "PI3K-AKT-mTOR Yolağı ve Sağkalım Sinyali",
            [
                "1. Lipid Fosforilasyonu: Aktif tirozin kinaz reseptörü PI3K enzimini zar yüzeyine çağırır ve PIP2'yi PIP3'e çevirir.",
                "2. AKT Kenetlenmesi: PIP3 lipidine bağlanan AKT serin/treonin kinazı PDK1 tarafından tam olarak aktive edilir.",
                "3. Apoptoz Blokajı: Aktif AKT, pro-apoptotik BAD proteinini fosforilleyerek 14-3-3 proteinine bağlar ve inaktive eder.",
                "4. Hücresel Büyüme: mTOR kompleksinin aktivasyonu ribozomal protein sentezini ve hücre hacim artışını tetikler."
            ]
        ),
        17: make_causal_chain(
            "MYC Transkripsiyon Faktörünün Onkojenik Proliferasyon Kaskadı",
            [
                "1. Gen Deregülasyonu: Kromozomal translokasyon t(8;14) veya gen amplifikasyonuyla MYC aşırı üretilir.",
                "2. Dimerizasyon: MYC proteini MAX ortağıyla heterodimer oluşturarak DNA üzerindeki E-box dizilerine bağlanır.",
                "3. Hücre Döngüsü İtici Gücü: Siklin D ve CDK4 gen ekspresyonu indüklenirken p21 gibi inhibitörler baskılanır.",
                "4. Metabolik Dönüşüm: Aerobik glikoliz enzimleri ve ribozomal biyogenez genleri eş zamanlı aktive edilir."
            ]
        ),
        25: make_causal_chain(
            "TP53 Aracılı Hücre Döngüsü Duraklaması ve DNA Onarım Kaskadı",
            [
                "1. DNA Hasar Algısı: Çift zincir kırıkları ATM ve ATR kinazları tarafından tanınır.",
                "2. p53 Fosforilasyonu: Fosforillenen p53, inhibitörü olan MDM2 ubiquitin ligazından ayrılarak kararlı hale gelir.",
                "3. Transkripsiyonel İndüksiyon: Kararlı p53 nükleusta birikir ve p21 (CDKN1A) geninin transkripsiyonunu başlatır.",
                "4. G1/S Blokajı: Sentezlenen p21 proteini Siklin E/CDK2 kompleksini inhibe ederek hücreyi G1 evresinde kilitler.",
                "5. Onarım veya Apoptoz: Hasar onarılırsa döngü devam eder; hasar tamir edilemezse BAX ve PUMA ile apoptoz tetiklenir."
            ]
        ),
        33: make_causal_chain(
            "Wnt/β-katenin Sinyal Yolağı ve APC Mutasyon Patogenezi",
            [
                "1. Fizyolojik Yıkım: Normal hücrede APC, aksin ve GSK-3b proteini β-katenini fosforilleyip proteazomda yıkar.",
                "2. APC İnaktivasyonu: Kolorektal karsinogenezde APC geninin her iki aleli mutasyonla işlevsizleşir.",
                "3. β-katenin Birikimi: Parçalanamayan serbest β-katenin sitoplazmada aşırı birikir ve nükleusa transloke olur.",
                "4. Hedef Gen Aktivasyonu: TCF/LEF transkripsiyon faktörleriyle birleşerek MYC ve Siklin D1 transkripsiyonunu ateşler."
            ]
        ),
        44: make_causal_chain(
            "İntrensek Mitokondriyal Apoptoz ve BCL-2 Blokajı",
            [
                "1. Hücresel Stres: DNA hasarı veya büyüme faktörü yoksunluğu BH3-only proteinlerini (BIM, PUMA) uyarır.",
                "2. Kanal Açılımı: Aktifleşen BAX ve BAK mitokondri dış zarında oligomerleşerek MOMP gözenekleri oluşturur.",
                "3. Onkoprotein Engeli: Foliküler lenfomada aşırı üretilen BCL-2, BAX ve BAK oligomerizasyonunu fiziksel olarak kilitler.",
                "4. Kaçış ve Sağkalım: Sitokrom c sitoplazmaya sızamaz, apoptazom kurulamaz ve neoplastik hücre ölümsüzleşir."
            ]
        ),
        52: make_causal_chain(
            "Tümör Anjiyojenez Kaskadı ve Damar Gelişimi",
            [
                "1. Hipoksik İndüksiyon: Tümör çapı 1-2 mm'yi aştığında merkezde hipoksi gelişir ve HIF-1alfa birikir.",
                "2. VEGF Sekresyonu: Neoplastik hücreler çevre ortama bol miktarda VEGF ve temel fibroblast büyüme faktörü salgılar.",
                "3. Matriks Sindirimi: Endotel hücreleri proteazlar salgılayarak bazal membranı eritir ve tümöre doğru göç eder.",
                "4. Düzensiz Lümen: Gelişen neovasküler damarlar kıvrımlı, aşırı geçirgen ve perisit desteğinden yoksundur."
            ]
        ),
        64: make_causal_chain(
            "Aerobik Glikoliz (Warburg Etkisi) ve Biyosentetik Kaskad",
            [
                "1. Onkogenik Komut: Aktifleşen RAS ve MYC onkogenleri membran glukoz taşıyıcılarını (GLUT1) upregüle eder.",
                "2. Hızlı Akış: Glukoz sitoplazmaya masif hızla girer ve piruvata kadar seri enzimlerle parçalanır.",
                "3. Laktat Üretimi: Piruvat mitokondriyal oksidasyon yerine LDHA enzimiyle hızla laktata dönüştürülür.",
                "4. Anabolik Havuz: Glikolitik ara ürünler nükleotid, aminoasit ve lipid sentezi için dallanmış yollara akar."
            ]
        ),
        74: make_causal_chain(
            "DNA Uyumsuzluk Onarım (MMR) Defekti ve Mikrosatellit İnstabilitesi",
            [
                "1. Replikasyon Kayması: DNA polimeraz tekrarlayan mikrosatellit baz dizilerinde kayma ve hata yapar.",
                "2. Tanıma Kusuru: MSH2, MLH1, MSH6 veya PMS2 kaybı nedeniyle baz uyumsuzluğu algılanıp düzeltilemez.",
                "3. Mikrosatellit Değişimi: Genom genelindeki mononükleotid ve dinükleotid tekrar dizilerinin uzunlukları bozulur.",
                "4. Kanser Gen Mutasyonları: Mikrosatellit içeren TGF-beta reseptör II ve BAX genlerinde çerçeve kayması mutasyonları birikir."
            ]
        ),
        84: make_causal_chain(
            "Kimyasal Karsinojenezin Çok Aşamalı Kaskadı",
            [
                "1. Başlatma (Initiation): Prokarsinojen elektrofilik türeve metabolize olur ve DNA'da kalıcı mutasyon oluşturur.",
                "2. Bellek: Tek başına başlatılmış hücre morfolojik olarak normaldir ancak potansiyel olarak transformasyona hazırdır.",
                "3. Teşvik (Promotion): Forbol esterleri veya kronik irritanlar hücre bölünmesini uyararak klonal genişleme sağlar.",
                "4. İlerleme (Progression): Artan genetik instabiliteyle invazyon, anjiyojenez ve malign fenotip tam oturur."
            ]
        ),
        94: make_causal_chain(
            "HPV Kaynaklı Servikal Karsinojenez Kaskadı",
            [
                "1. Viral Enfeksiyon: Yüksek riskli HPV (tip 16/18) servikal skuamöz epitelin bazal kök hücrelerini enfekte eder.",
                "2. Genomik İntegrasyon: Virüs dairesel formdan lineer forma geçerek konak DNA'sına integre olur; E2 represörü kırılır.",
                "3. Onkoprotein Saldırısı: Kontrolsüz sentezlenen E6 proteini p53'ü parçalar; E7 proteini RB'yi bağlayarak E2F'yi salar.",
                "4. Malign Transformasyon: Hücre döngüsü kontrol noktaları tamamen çöker, genomik hasarlar birikir ve karsinom gelişir."
            ]
        )
    }

def get_extra_micro_quizzes():
    """Micro quiz (çoktan seçmeli mini pekiştirme soruları) ek ögeleri (13 adet)."""
    return {
        4: make_micro_quiz(
            "Aşağıdaki protoonkogen ve ilişkili olduğu malignite eşleştirmelerinden hangisi yanlıştır?",
            [
                {
                    "text": "ERBB2 (HER2/neu) - Meme karsinomu amplifikasyonu",
                    "isCorrect": False,
                    "explanation": "ERBB2 meme karsinomunda amplifiye olan klasik bir reseptör tirozin kinazdır."
                },
                {
                    "text": "RET - Medüller tiroid karsinomu nokta mutasyonu",
                    "isCorrect": False,
                    "explanation": "RET mutasyonları ailesel MEN 2 sendromu ve medüller tiroid karsinomunda tipiktir."
                },
                {
                    "text": "ALK füzyonu - Akciğer adenokarsinomu translokasyonu",
                    "isCorrect": False,
                    "explanation": "EML4-ALK translokasyonu akciğer adenokarsinomunda hedeflenebilir hedeftir."
                },
                {
                    "text": "RB1 - Onkogenik nokta mutasyonuyla sürekli aktive olan büyüme faktörü",
                    "isCorrect": True,
                    "explanation": "RB1 bir onkogen değil, çift darbe kuralıyla inaktive olan klasik bir tümör baskılayıcı gendir."
                }
            ],
            "RB1 bir tümör baskılayıcı gendir; onkogenler grubunda yer almaz."
        ),
        8: make_micro_quiz(
            "RAS onkogeni ile ilgili aşağıdaki ifadelerden hangisi biyolojik ve moleküler mekanizma açısından doğrudur?",
            [
                {
                    "text": "En sık mutasyon kodon 12, 13 veya 61'de GTPaz aktive edici protein (GAP) yanıtını bozan nokta mutasyonudur.",
                    "isCorrect": True,
                    "explanation": "RAS'ın GTP hidroliz yeteneği bozulur ve GTP bağlı aktif konumda sürekli kalarak kontrolsüz sinyal iletir."
                },
                {
                    "text": "RAS nükleer bir transkripsiyon faktörü olup doğrudan DNA promotor bölgelerine bağlanır.",
                    "isCorrect": False,
                    "explanation": "RAS plazma membranının iç yüzeyine bağlı küçük bir G proteinidir, transkripsiyon faktörü değildir."
                },
                {
                    "text": "Mutant RAS proteini hücre içinde GTP yerine sadece serbest kalsiyum bağlayarak aktive olur.",
                    "isCorrect": False,
                    "explanation": "RAS bir guanozin trifosfat (GTP) bağlayıcı proteindir."
                },
                {
                    "text": "RAS inaktivasyonu hücre proliferasyonunu tetiklerken, aşırı aktivasyonu hücreyi senesense sokarak tümörü engeller.",
                    "isCorrect": False,
                    "explanation": "Tam tersine RAS'ın konstitütif aktivasyonu mitojenik sinyali patlatarak tümörogenezi başlatır."
                }
            ],
            "RAS mutasyonları intrensek GTPaz aktivitesini ve GAP duyarlılığını ortadan kaldırır."
        ),
        14: make_micro_quiz(
            "Tümör baskılayıcı PTEN fosfataz enziminin hücre içindeki fizyolojik moleküler görevi aşağıdakilerden hangisidir?",
            [
                {
                    "text": "PIP3'ü defosforilleterek PIP2'ye çevirip PI3K/AKT yolağını frenlemek",
                    "isCorrect": True,
                    "explanation": "PTEN, PI3K'nin ürettiği PIP3 lipidini PIP2'ye yıkarak AKT sağkalım yolağını durduran temel tümör baskılayıcıdır."
                },
                {
                    "text": "Hücre zarındaki serbest kolesterol moleküllerini esterleştirmek",
                    "isCorrect": False,
                    "explanation": "PTEN bir lipid fosfatazdır ancak inozitol fosfatları hedefler, kolesterol metabolizmasını değil."
                },
                {
                    "text": "Mitokondride sitokrom c proteinini parçalamak",
                    "isCorrect": False,
                    "explanation": "PTEN plazma zarı yakınında PIP3 defosforilasyonu yapar."
                },
                {
                    "text": "DNA çift zincir kırıklarını homolojiye gerek kalmadan uç uca bağlamak",
                    "isCorrect": False,
                    "explanation": "Bu görev NHEJ onarım enzimlerine (Ku70/80, DNA ligaz IV) aittir."
                }
            ],
            "PTEN kaybı PIP3 birikimine ve AKT kinazının kontrolsüz aktivasyonuna neden olur."
        ),
        18: make_micro_quiz(
            "Burkitt lenfomasında karakteristik olarak izlenen sitogenetik sapma ve aktive olan gen hangisidir?",
            [
                {
                    "text": "t(8;14) translokasyonu ve c-MYC onkogeninin aşırı ekspresyonu",
                    "isCorrect": True,
                    "explanation": "Kromozom 8'deki c-MYC, kromozom 14'teki immünoglobulin ağır zincir lokusunun kuvvetli promotoru altına taşınır."
                },
                {
                    "text": "t(9;22) translokasyonu ve BCR-ABL füzyonu",
                    "isCorrect": False,
                    "explanation": "t(9;22) KML ve B-ALL için karakteristiktir."
                },
                {
                    "text": "t(14;18) translokasyonu ve BCL-2 aktivasyonu",
                    "isCorrect": False,
                    "explanation": "t(14;18) foliküler lenfoma için karakteristiktir."
                },
                {
                    "text": "t(15;17) translokasyonu ve PML-RARA füzyonu",
                    "isCorrect": False,
                    "explanation": "t(15;17) akut promiyelositer lösemi (APL) için karakteristiktir."
                }
            ],
            "Burkitt lenfoması t(8;14) translokasyonu ve c-MYC deregülasyonu ile tanımlanır."
        ),
        24: make_micro_quiz(
            "Retinoblastoma proteini (pRB), hücre döngüsünün hangi kontrol noktasında nöbetçi görevi yaparak G1'den S fazına geçişi denetler?",
            [
                {
                    "text": "Hipofosforile formda E2F transkripsiyon faktörünü bağlayıp hapsederek G1/S kontrol noktasını tutar.",
                    "isCorrect": True,
                    "explanation": "Aktif (hipofosforile) pRB, E2F'yi bağlayarak S fazı genlerinin transkripsiyonunu engeller."
                },
                {
                    "text": "Aşırı hiperfosforile haldeyken mikrotübüllere tutunarak metafaz/anafaz kontrolünü sağlar.",
                    "isCorrect": False,
                    "explanation": "Hiperfosforilasyon pRB'yi inaktive eder ve E2F'nin serbest kalmasına neden olur."
                },
                {
                    "text": "Doğrudan ribozomal RNA sentezini durdurarak G2/M geçişini kilitler.",
                    "isCorrect": False,
                    "explanation": "RB'nin ana hedefi G1/S geçişi ve E2F bağımlı DNA replikasyon genleridir."
                },
                {
                    "text": "Telomeraz enzimini parçalayarak mitotik fazın sonlanmasını denetler.",
                    "isCorrect": False,
                    "explanation": "RB telomerazı parçalamaz; hücre döngüsü kinazları tarafından fosforillenerek regüle edilir."
                }
            ],
            "Hipofosforile pRB aktif frendir; Siklin D/CDK4 tarafından hiperfosforillendiğinde fren kalkar."
        ),
        28: make_micro_quiz(
            "p53 proteininin hücredeki fizyolojik düzeyini ve yarı ömrünü negatif geri bildirimle kontrol eden birincil ubiquitin ligaz hangisidir?",
            [
                {
                    "text": "MDM2",
                    "isCorrect": True,
                    "explanation": "MDM2 p53'e bağlanarak onu ubikitinler ve proteazomal yıkıma yönlendirir; DNA hasarında p53 fosforillenerek MDM2'den kurtulur."
                },
                {
                    "text": "VHL",
                    "isCorrect": False,
                    "explanation": "VHL HIF-1alfa'yı ubikitinler, p53'ü değil."
                },
                {
                    "text": "APC",
                    "isCorrect": False,
                    "explanation": "APC beta-katenin yıkım kompleksinde yer alır."
                },
                {
                    "text": "BRCA1",
                    "isCorrect": False,
                    "explanation": "BRCA1 homolog rekombinasyon DNA onarım kompleksinde görevlidir."
                }
            ],
            "MDM2 amplifikasyonu bazı sarkomlarda p53 mutasyonu olmaksızın p53 işlevini felç eder."
        ),
        35: make_micro_quiz(
            "CDH1 gen mutasyonu veya promoter hipermetilasyonu sonucu E-kaderin ekspresyonunu kaybeden bir tümörde hangi histopatolojik karsinom tipi tipik olarak gelişir?",
            [
                {
                    "text": "Diffüz tip mide karsinomu (taşlı yüzük hücreli karsinom)",
                    "isCorrect": True,
                    "explanation": "CDH1 inaktivasyonu hücrelerarası adezyonu yok eder; kohezyonsuz infiltratif taşlı yüzük hücreli diffüz mide karsinomu ve lobüler meme karsinomu gelişir."
                },
                {
                    "text": "İyi diferansiye keratinize skuamöz hücreli karsinom",
                    "isCorrect": False,
                    "explanation": "Skuamöz karsinomda desmozomlar ve dikenli köprüler korunur."
                },
                {
                    "text": "Berrak hücreli renal karsinom",
                    "isCorrect": False,
                    "explanation": "Renal berrak hücreli karsinom VHL mutasyonuyla ilişkilidir."
                },
                {
                    "text": "Foliküler tiroid karsinomu",
                    "isCorrect": False,
                    "explanation": "Foliküler tiroid karsinomu PAX8-PPARG füzyonu veya RAS mutasyonlarıyla karakterizedir."
                }
            ],
            "E-kaderin kaybı epitelyal hücrelerin birbirinden bağımsız tek tek infiltre olmasına (diffüz paterne) yol açar."
        ),
        45: make_micro_quiz(
            "Kaspaz-8 aktivasyonunu engelleyerek ekstrinsek (ölüm reseptörü) apoptoz yolağını bloke eden ve bazı tümörlerde aşırı eksprese edilen protein hangisidir?",
            [
                {
                    "text": "c-FLIP",
                    "isCorrect": True,
                    "explanation": "c-FLIP prokaspaz-8 ile yapısal homoloji gösterir ancak katalitik aktivitesi yoktur; DISC kompleksine bağlanarak kaspaz-8 kesimini önler."
                },
                {
                    "text": "BAX",
                    "isCorrect": False,
                    "explanation": "BAX intrensek yolda pro-apoptotik gözenek oluşturur."
                },
                {
                    "text": "Sitokrom c",
                    "isCorrect": False,
                    "explanation": "Sitokrom c intrensek yolda APAF-1 ile apoptazomu kurar."
                },
                {
                    "text": "Apaf-1",
                    "isCorrect": False,
                    "explanation": "Apaf-1 intrensek apoptozun prokaspaz-9 aktive edici iskeletidir."
                }
            ],
            "c-FLIP ekstrinsek ölüm reseptörü kaskadının temel fizyolojik ve neoplastik inhibitörüdür."
        ),
        55: make_micro_quiz(
            "Tümör hücrelerinin ekstrasellüler matriksi ve bazal membranı eriterek doku invazyonu yapmasında görev alan çinko bağımlı temel proteaz enzim ailesi hangisidir?",
            [
                {
                    "text": "Matriks metalloproteinazlar (MMP-2 ve MMP-9 gibi)",
                    "isCorrect": True,
                    "explanation": "MMP'ler tip IV kollajen dahil bazal membran bileşenlerini proteolitik olarak yıkarak invazyon yolunu açar."
                },
                {
                    "text": "Pankreatik tripsinojen enzimleri",
                    "isCorrect": False,
                    "explanation": "Tripsinojen sindirim enzimidir, tümör stroma invazyonunun primer metalloproteinazı değildir."
                },
                {
                    "text": "Alkalen fosfataz izoenzimleri",
                    "isCorrect": False,
                    "explanation": "Alkalen fosfataz fosfat esterlerini yıkar, ekstrasellüler matriks kollajenini eritmez."
                },
                {
                    "text": "Laktat dehidrogenaz izoformları",
                    "isCorrect": False,
                    "explanation": "LDH sitoplazmik anaerobik metabolizma enzimidir, matriks proteazı değildir."
                }
            ],
            "MMP-2 ve MMP-9 (jelatinazlar) bazal membran kollajenini eriterek vasküler ve dokusal invazyonu sağlar."
        ),
        65: make_micro_quiz(
            "Sitotoksik T lenfositlerin yüzeyindeki PD-1 reseptörüne bağlanarak T hücresini anerjiye sokan ve tümör mikroçevresinde immün kaçışı sağlayan ligand hangisidir?",
            [
                {
                    "text": "PD-L1 (Programmed Death-Ligand 1)",
                    "isCorrect": True,
                    "explanation": "Tümör hücreleri yüzeyinde PD-L1 ekspresyonunu artırarak CD8+ sitotoksik T hücrelerindeki PD-1'i uyarır ve immün saldırıyı felç eder."
                },
                {
                    "text": "CD28 ko-stimülatörü",
                    "isCorrect": False,
                    "explanation": "CD28 T hücresi aktivasyon reseptörüdür, inhibitör ligand değildir."
                },
                {
                    "text": "İnterlökin-2 reseptör alfa zinciri",
                    "isCorrect": False,
                    "explanation": "IL-2R T hücre proliferasyonunu uyarır."
                },
                {
                    "text": "Tümör nekroz faktörü alfa",
                    "isCorrect": False,
                    "explanation": "TNF-alfa bir proinflamatuar sitokindir, PD-1 spesifik ligandı değildir."
                }
            ],
            "Anti-PD-1 ve anti-PD-L1 antikorları (kontrol noktası blokajı) bu fren mekanizmasını kaldırarak T hücresini yeniden aktifler."
        ),
        75: make_micro_quiz(
            "BRCA1 veya BRCA2 mutasyonu taşıyan over ve meme karsinomlu hastalarda 'sentetik ölüm' (synthetic lethality) prensibiyle kullanılan hedefe yönelik ilaç sınıfı hangisidir?",
            [
                {
                    "text": "PARP inhibitörleri (olaparib vb.)",
                    "isCorrect": True,
                    "explanation": "PARP tek zincir onarımını yapar; inhibe edildiğinde çift zincir kırıkları birikir. Homolog rekombinasyonu (BRCA) bozuk tümör hücresi ölürken normal hücreler yaşar."
                },
                {
                    "text": "Alkilleyici platin türevleri dışındaki tüm antibiyotikler",
                    "isCorrect": False,
                    "explanation": "Sentetik ölüm mekanizması spesifik olarak PARP enzimi blokajıyla çift zincir kırıklarının birikmesine dayanır."
                },
                {
                    "text": "Anti-CD20 monoklonal antikorları",
                    "isCorrect": False,
                    "explanation": "Anti-CD20 B hücre yüzey antijenini hedefler, DNA onarımıyla ilişkisizdir."
                },
                {
                    "text": "Yalnızca hormon replasman östrojen preparatları",
                    "isCorrect": False,
                    "explanation": "Östrojen replasmanı meme kanserinde tedavi değil kontrendikasyon oluşturabilir."
                }
            ],
            "PARP inhibisyonu ve BRCA defekti birleştiğinde DNA tamiri imkansızlaşır ve seçici tümör ölümü gerçekleşir."
        ),
        85: make_micro_quiz(
            "Güneş ışığındaki ultraviyole B (UVB) radyasyonunun DNA üzerinde oluşturduğu en karakteristik moleküler lezyon türü hangisidir?",
            [
                {
                    "text": "Pirimidin dimerleri (özellikle timin-timin çapraz bağları)",
                    "isCorrect": True,
                    "explanation": "UVB doğrudan DNA bazları tarafından emilir ve komşu iki pirimidin bazının kovalent bağlanarak dimerleşmesine yol açar."
                },
                {
                    "text": "Yalnızca pürin bazlarının metilasyonu",
                    "isCorrect": False,
                    "explanation": "Baz metilasyonu alkilleyici ajanlarla oluşur, UV radyasyonunun temel etkisi pirimidin dimerleridir."
                },
                {
                    "text": "DNA çift sarmalının tamamen glikozillenmesi",
                    "isCorrect": False,
                    "explanation": "Glikozilasyon enzim aracılı bir modifikasyondur, radyasyon hasarı değildir."
                },
                {
                    "text": "Kromozomların sentromer bölgesinden kovalent olarak telomerlere yapışması",
                    "isCorrect": False,
                    "explanation": "UVB mikroskobik kromozom füzyonundan ziyade lokalize pirimidin dimerleşmesi yapar."
                }
            ],
            "UVB pirimidin dimerleri yapar; nükleotid kesip çıkarma onarımı bozuksa kseroderma pigmentozumda olduğu gibi karsinomlar patlar."
        ),
        95: make_micro_quiz(
            "Yüksek riskli İnsan Papilloma Virüsü (HPV) tip 16 ve 18'in onkojenik potansiyeli hangi iki viral proteinin konak tümör baskılayıcılarını inaktive etmesine dayanır?",
            [
                {
                    "text": "E6 (p53'ü ubikitinleyip yıkan) ve E7 (RB'yi bağlayıp E2F'yi serbest bırakan)",
                    "isCorrect": True,
                    "explanation": "E6 p53 yıkımını sağlayarak apoptozu önler; E7 ise RB'yi inaktive ederek kontrolsüz S fazı geçişini tetikler."
                },
                {
                    "text": "E1 ve E2 yapısal kapsid proteinleri",
                    "isCorrect": False,
                    "explanation": "E1 ve E2 replikasyon ve regülasyondan sorumludur; onkojenik sürücüler E6 ve E7'dir."
                },
                {
                    "text": "L1 ve L2 geç faz viral zarf antijenleri",
                    "isCorrect": False,
                    "explanation": "L1 ve L2 yapısal proteinlerdir ve aşı üretiminde kullanılırlar, tümör baskılayıcıları doğrudan inaktive etmezler."
                },
                {
                    "text": "Yalnızca revers transkriptaz ve integraz enzimleri",
                    "isCorrect": False,
                    "explanation": "HPV bir DNA virüsüdür, retrovirüsler gibi revers transkriptaz kodlamaz."
                }
            ],
            "HPV onkogenezinin iki temel sütunu: E6 -> p53 yıkımı, E7 -> RB inaktivasyonudur."
        )
    }

def get_extra_before_afters():
    """Before after slider (moleküler ve patolojik dönüşüm) ek ögeleri (5 adet)."""
    return {
        6: make_before_after(
            "Fizyolojik RTK Sinyali vs Onkojenik Reseptör Sürekli Aktivasyonu",
            "Fizyolojik Reseptör Tirozin Kinaz (RTK)",
            "Ligand bağlandığında geçici dimerizasyon ve otofosforilasyon gerçekleşir; ardından reseptör endositozla içeri alınarak sinyal hızla sonlandırılır.",
            "Onkojenik Mutant / Amplifiye RTK (EGFR, HER2)",
            "Ligand yokluğunda bile yapısal olarak aktif homodimerler kurulur; içe alım defektiftir ve kesintisiz mitojenik sinyal çekirdeğe pompalanır.",
            "Ligand bağımsız sürekli sinyal iletimi, tirozin kinaz inhibitörleri ve monoklonal antikor tedavilerinin temel biyolojik hedefini oluşturur."
        ),
        22: make_before_after(
            "Knudson Çift Darbe Hipotezi: Sporadik vs Ailesel Kanserler",
            "Sporadik Kanser Patogenezi (İki Somatik Darbe)",
            "Birey iki sağlam allel ile doğar; aynı hücrede bağımsız iki somatik mutasyonun peş peşe birikmesi yıllar alır, tümör ileri yaşta ve unifokaldir.",
            "Ailesel Sendrom Patogenezi (Bir Germline + Bir Somatik Darbe)",
            "Birey tüm hücrelerinde tek mutant allelle doğar; tek bir ek somatik mutasyon tümör oluşumu için yeterlidir; erken yaşta, bilateral veya multifokaldir.",
            "Knudson modeli retinoblastom, Li-Fraumeni ve ailesel kolon kanserlerinin kalıtım ve başlangıç yaşını kusursuz açıklar."
        ),
        36: make_before_after(
            "Normoksi Durumunda VHL vs Hipoksi / VHL Mutasyonunda HIF-1a",
            "Fizyolojik Normoksi (VHL İşlevsel)",
            "Prolil hidroksilazlar HIF-1a'yı hidroksiller; VHL ubiquitin ligazı bunu tanıyıp bağlar ve HIF-1a proteazomda sessizce yıkılır.",
            "Hipoksi veya VHL Gen Mutasyonu / Kaybı",
            "HIF-1a hidroksillenemez veya yıkılamaz; nükleusa geçerek VEGF, GLUT1 ve PDGF transkripsiyonunu kontrolsüz başlatır ve hipervaskülarizasyon yaratır.",
            "Berrak hücreli böbrek karsinomlarının hipervasküler yapısının ve anti-VEGF tedavilere duyarlılığının moleküler temelini oluşturur."
        ),
        66: make_before_after(
            "Normal Oksidatif Fosforilasyon vs Tümöral Warburg Etkisi",
            "Diferansiye Normal Hücre (Oksidatif Fosforilasyon)",
            "Glukoz piruvata yıkılır ve mitokondriye girerek Krebs döngüsü ve ETS ile mol başına ~36 ATP üretir; laktat üretimi düşüktür.",
            "Prolifere Kanser Hücresi (Warburg Aerobik Glikolizi)",
            "Oksijen bol olsa bile glukoz hızla laktata çevrilir; mol başına sadece 2 ATP kazanılır ancak nükleotid ve lipid biyosentezi için hammadde taşar.",
            "Warburg etkisi 18F-FDG PET görüntülemenin temelidir ve tümöre hızlı büyüme için devasa bir biyosentez fabrikası sağlar."
        ),
        86: make_before_after(
            "Doğrudan Etkili Karsinojenler vs Dolaylı Etkili Prokarsinojenler",
            "Doğrudan Etkili (Direct-Acting) Karsinojenler",
            "Metabolik aktivasyona ihtiyaç duymazlar; kendileri kuvvetli elektrofiliktir ve dokuyla temas anında doğrudan DNA adüktleri oluştururlar (ör. alkilleyiciler).",
            "Dolaylı Etkili (Prokarsinojen) Ajanlar",
            "Başlangıçta biyolojik olarak inerttirler; karaciğer mikrozomal CYP enzimleri tarafından metabolize edilerek nihai elektrofilik karsinojene dönüşürler (ör. benzo[a]piren).",
            "Bireyler arasındaki CYP1A1 genetik polimorfizmleri aynı karsinojene maruz kalan kişilerdeki kanser risk farklılığını açıklar."
        )
    }

def enrich_slides(slides):
    """Slaytlara ek interaktif elemanları ekler ve çeşitliliği dengeler."""
    extra_branching = get_extra_branching()
    extra_chains = get_extra_causal_chains()
    extra_quizzes = get_extra_micro_quizzes()
    extra_bas = get_extra_before_afters()

    for s in slides:
        num = s["slideNumber"]
        els = s.setdefault("interactiveElements", [])

        if num in extra_branching:
            els.append(extra_branching[num])
        if num in extra_chains:
            els.append(extra_chains[num])
        if num in extra_quizzes:
            els.append(extra_quizzes[num])
        if num in extra_bas:
            els.append(extra_bas[num])

    return slides
