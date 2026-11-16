# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_21_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik karar verme, acil vaka yönetimi ve tanı algoritmaları) ögeleri."""
    return {
        4: make_branching_logic(
            "Geniş spektrumlu sefalosporin tedavisi almakta olan 68 yaşındaki yatan hastada tedavinin 6. gününde bol sulu, kötü kokulu ishal ve lökositoz gelişiyor. Endoskopide kolonda psödomembranlar izleniyor.",
            "Normal bağırsak mikrobiyotasının antibiyotikle baskılanması sonucu fırsatçı üreyen bu tablonun en olası etkeni ve ilk yapılması gereken müdahale hangisidir?",
            [
                {
                    "text": "Etken Clostridioides difficile'dir; mevcut antibiyotik derhal kesilmeli ve oral vankomisin başlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "Doğru. Geniş spektrumlu antibiyotikler kolon mikrobiyotasını baskılayarak C. difficile sporlarının çimlenmesine ve toksin A/B salgılayarak psödomembranöz enterokolite yol açmasına zemin hazırlar. İlk adım tetikleyici antibiyotiğin kesilmesidir."
                },
                {
                    "text": "Etken Shigella dysenteriae'dir; hastaya acilen intravenöz siprofloksasin yüklenmelidir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Shigella toplum kaynaklı invazif basilli dizanteri etkenidir; antibiyotik ilişkili psödomembranöz kolit yapmaz."
                },
                {
                    "text": "Tablo fizyolojik bir flora yanıtıdır, hiçbir tedavi gerekmez ve mevcut antibiyotiğe devam edilmelidir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Psödomembranöz kolit toksik megakolon ve perforasyona yol açabilen ölümcül bir komplikasyondur, acil tedavi şarttır."
                }
            ]
        ),
        8: make_branching_logic(
            "Kemik iliği nakli sonrası nötropenik (mutlak nötrofil sayısı < 500/mm3) olan bir hastada santral venöz kateter giriş yerinde kızarıklık ve 39 derece ateş saptanıyor. Normalde ciltte zararsız bir kommensal olan bakteri izole ediliyor.",
            "Bu klinik senaryoda kommensal bir bakterinin hastalık tablosuna yol açmasını en iyi tanımlayan mikrobiyolojik kavram hangisidir?",
            [
                {
                    "text": "Fırsatçı (Oportünist) Enfeksiyon",
                    "isCorrect": True,
                    "explanation": "Doğru. Normal florada bulunan veya çevrede zararsız olan mikroorganizmaların konak bağışıklığı çöktüğünde (nötropeni, kateter vb.) invazyon yaparak ağır hastalık oluşturmasına fırsatçı enfeksiyon denir."
                },
                {
                    "text": "Primer Yüksek Virülan Enfeksiyon",
                    "isCorrect": False,
                    "explanation": "Yanlış. Primer patojenler sağlam immünitesi olan sağlıklı bireylerde de tek başına hastalık yapabilen etkenlerdir."
                },
                {
                    "text": "Subklinik Taşıyıcılık",
                    "isCorrect": False,
                    "explanation": "Yanlış. Hastada aktif ateş, lokal kateter enfeksiyonu ve bakteriyemi mevcuttur; semptomsuz bir taşıyıcılık söz konusu değildir."
                }
            ]
        ),
        12: make_branching_logic(
            "İki farklı bakteriyel patojen laboratuvar ortamında karşılaştırılmaktadır. Bakteri X'in denek farelerin %50'sinde hastalık oluşturması için 10 adet mikroorganizma gerekirken, Bakteri Y için 100.000 adet gerekmektedir.",
            "Bu deneysel farmakolojik/mikrobiyolojik veriye göre aşağıdaki çıkarımlardan hangisi kesinlikle doğrudur?",
            [
                {
                    "text": "Bakteri X'in İnfeksiyöz Doz 50 (ID50) değeri daha düşüktür ve bulaşıcılık/virülansı Bakteri Y'ye göre çok daha yüksektir.",
                    "isCorrect": True,
                    "explanation": "Doğru. ID50 değeri ne kadar düşükse mikroorganizmanın konağı enfekte etme potansiyeli ve virülansı o kadar yüksektir. Shigella (ID50 ~10-100) ve Kolera (ID50 ~10^6) klasik örnektir."
                },
                {
                    "text": "Bakteri Y'nin virülansı Bakteri X'ten daha yüksektir çünkü çoğalmak için daha fazla sayıda bakteriye ihtiyaç duyar.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Yüksek ID50 değeri düşük virülansı simgeler; hastalığı başlatmak için çok büyük inokulum gerekir."
                },
                {
                    "text": "Her iki bakterinin virülansı eşittir çünkü ikisi de farelerde ölüm oluşturmaktadır.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Gerekli bakteri sayıları arasında 10.000 kat fark vardır; virülans düzeyleri son derece farklıdır."
                }
            ]
        ),
        16: make_branching_logic(
            "Genç bir kadında tekrarlayan idrar yolu enfeksiyonu şikayeti mevcuttur. İzole edilen üropatojen E. coli (UPEC) suşunun idrar akımına rağmen mesane epiteline sımsıkı tutunduğu belirleniyor.",
            "Bu bakterinin mesane uroepitelindeki mannoz reseptörlerine kilitlenerek dışarı atılmasını engelleyen en kritik virülans yapısı hangisidir?",
            [
                {
                    "text": "Fimbriya (Pili) ve Tip 1 adezin molekülleri",
                    "isCorrect": True,
                    "explanation": "Doğru. Üropatojen E. coli, Tip 1 pili ve P-fimbriyaları sayesinde mesane ve böbrek epitelindeki glikolipid/glikoprotein reseptörlere tutunarak mekanik idrar akışının yıkama etkisine direnç gösterir."
                },
                {
                    "text": "Endotoksin Lipid A komponenti",
                    "isCorrect": False,
                    "explanation": "Yanlış. Lipid A septik şok ve ateşi tetikler; adezyon görevi görmez."
                },
                {
                    "text": "Bakteriyel plazmit DNA molekülleri",
                    "isCorrect": False,
                    "explanation": "Yanlış. Plazmitler sitoplazmada genetik aktarım sağlar, yüzeyel reseptör tutunması yapmaz."
                }
            ]
        ),
        22: make_branching_logic(
            "Diyaliz kateteri takılı bir hastada kateter çekilmeden verilen intravenöz vankomisin tedavisine rağmen bakteriyeminin tekrarladığı gözleniyor. Kateter yüzeyinde hücre dışı polisakkarit matriks içinde kümelenmiş mikroorganizmalar saptanıyor.",
            "Antibiyotiklerin ve nötrofillerin penetre olamadığı bu korunaklı bakteriyel organizasyon modeli hangisidir?",
            [
                {
                    "text": "Biyofilm (Biofilm) tabakası",
                    "isCorrect": True,
                    "explanation": "Doğru. Biyofilm, bakterilerin abiyotik yüzeylere (kateter, protez, kalp kapağı) yapışarak salgıladığı ekzopolisakkarit (EPS) matriksidir; antibiyotik konsantrasyonuna 1000 kata kadar direnç sağlar ve mekanik olarak temizlenmedikçe (kateter çekilmedikçe) enfeksiyon kür edilemez."
                },
                {
                    "text": "Endospor formasyonu",
                    "isCorrect": False,
                    "explanation": "Yanlış. Sporlar tek hücreli dehidrate formlardır; kateter üzerinde çok hücreli biyofilm matriksi kurmazlar."
                },
                {
                    "text": "Bakteriyofaj lizogenik döngüsü",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bakteriyofaj virüstür; kateter enfeksiyonunun matriksini oluşturmaz."
                }
            ]
        ),
        26: make_branching_logic(
            "Cerrahi operasyon geçiren bir hastanın yarasında hızla yayılan eritem, bül oluşumu ve cilt altı dokuda gaz çıtırtısı (krepitasyon) tespit ediliyor. Biyopside kollajenin ve bağ dokusunun süratle parçalandığı görülüyor.",
            "Clostridium perfringens suşunun doku planlarında hızla yayılmasını ve gazlı gangren oluşturmasını sağlayan invaziv enzimler hangileridir?",
            [
                {
                    "text": "Kollajenaz ve Lesitinaz (Alfa Toksin)",
                    "isCorrect": True,
                    "explanation": "Doğru. Clostridium perfringens kollajenazı ile kas ve bağ dokusu liflerini sindirirken, lesitinaz (fosfolipaz C) ile hücre membranlarındaki fosfolipidleri parçalayarak yaygın doku nekrozu ve gazlı gangrene neden olur."
                },
                {
                    "text": "Katalaz ve Oksidaz enzimleri",
                    "isCorrect": False,
                    "explanation": "Yanlış. Katalaz ve oksidaz oksidatif metabolizma enzimleridir, invazif nekrotizan doku harabiyeti yapmazlar."
                },
                {
                    "text": "Streptokinaz ve Hyaluronidaz",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bunlar daha çok Streptococcus pyogenes enzimleridir; gazlı gangrenin karakteristik lesitinazı C. perfringens'e aittir."
                }
            ]
        ),
        32: make_branching_logic(
            "Aşılanmamış 7 yaşındaki çocukta boğaz ağrısı, boyunda boğa boynu görünümü (masif lenfadenopati) ve farenkste kaldırılınca kanayan gri-beyaz psödomembran izleniyor. Patojenin A-B yapısında bir toksin salgıladığı biliniyor.",
            "Corynebacterium diphtheriae toksininin hücre ölümüne yol açtığı moleküler mekanizma hangisidir?",
            [
                {
                    "text": "Elongasyon Faktör 2'yi (EF-2) ADP-ribozilasyon ile inaktive ederek ribozomal protein sentezini tamamen durdurur.",
                    "isCorrect": True,
                    "explanation": "Doğru. Difteri toksininin B alt birimi reseptöre tutunmayı sağlarken, hücre içine giren A alt birimi EF-2'yi ADP-ribozilleyerek protein translokasyonunu bloke eder ve hücre ölümüne yol açar."
                },
                {
                    "text": "Hücre zarındaki asetilkolin reseptörlerini bloke ederek felç oluşturur.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bu mekanizma botulinum toksinine aittir; protein senteziyle ilişkisi yoktur."
                },
                {
                    "text": "cAMP düzeyini artırarak enterositlerden masif su ve klor sekresyonuna yol açar.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bu mekanizma Vibrio cholerae kolera toksinine aittir."
                }
            ]
        ),
        36: make_branching_logic(
            "Açık konserve yedikten 18 saat sonra çift görme (diplopi), göz kapağı düşüklüğü (ptozis), yutma güçlüğü ve yukarıdan aşağıya inen gevşek (flask) felç tablosuyla acile getirilen hastada botulizm düşünülüyor.",
            "Botulinum nörotoksininin periferik nöromüsküler kavşakta flask paraliziye yol açtığı biyokimyasal mekanizma hangisidir?",
            [
                {
                    "text": "SNARE proteinlerini parçalayarak sinaps boşluğuna Asetilkolin salınımını engeller.",
                    "isCorrect": True,
                    "explanation": "Doğru. Botulinum toksini motor nöron uçlarında vezikül füzyonunu sağlayan SNARE (sinaptobrevin, SNAP-25) proteinlerini yıkar; asetilkolin boşluğa dökülemez ve kas uyarılamayarak gevşek felç gelişir."
                },
                {
                    "text": "Renshaw hücrelerinde GABA ve glisin salınımını engelleyerek spastik kasılma yapar.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Tetanospazmin (tetanoz toksini) internöronlarda inhibitör transmitterleri bloke ederek rijit spastik felç yapar."
                },
                {
                    "text": "Kas hücresindeki sodyum kanallarını bloke ederek aksiyon potansiyelini durdurur.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bu tetrodotoksin mekanizmasıdır; botulinum presinaptik nörotransmitter salınımını vurur."
                }
            ]
        ),
        42: make_branching_logic(
            "Gram-negatif sepsisli hastada tansiyon 70/40 mmHg'ye düşüyor, laktik asidoz ve yaygın peteşi/purpuralar gelişiyor. Bakterinin dış membranındaki lipopolisakkaritin (LPS) bağışıklık hücrelerini aşırı uyardığı belirleniyor.",
            "Endotoksinin (LPS) septik şok, ateş ve yaygın damar içi pıhtılaşmayı (DIC) tetikleyen en toksik biyokimyasal komponenti ve bağlandığı konak reseptörü hangisidir?",
            [
                {
                    "text": "Lipid A komponentidir; makrofaj yüzeyindeki TLR-4 reseptörüne bağlanarak fırtına şeklinde TNF-alfa ve IL-1 salınımını tetikler.",
                    "isCorrect": True,
                    "explanation": "Doğru. LPS'nin O-antijeni değişken serolojik kısmı iken, asıl endotoksik etkiden sorumlu yapı Lipid A'dır. Lipid A, makrofajlardaki CD14/TLR-4 kompleksini aktive ederek masif pirojen ve vazodilatatör sitokin salgılatır."
                },
                {
                    "text": "O-polisakkarit zinciridir; CD4 T hücrelerindeki TCR reseptörünü yıkar.",
                    "isCorrect": False,
                    "explanation": "Yanlış. O-antijeni hidrofilik polisakkarit kuyruktur, toksik etkiden Lipid A sorumludur."
                },
                {
                    "text": "Kore polisakkaritidir; kompleman C3 molekülünü doğrudan eritir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Kore bölgesi yapısal bir bağlayıcıdır; asıl toksisite Lipid A'dadır."
                }
            ]
        ),
        46: make_branching_logic(
            "Staphylococcus aureus kaynaklı bir apseden alınan bakterilerin fagositoza son derece dirençli olduğu ve opsonizasyonu engellediği saptanıyor. Bakterinin Fc reseptörlerine ters bağlanarak immün kaçış sağlayan bir yüzey proteini taşıdığı anlaşılıyor.",
            "Bakteriyel hücre duvarında bulunan ve IgG moleküllerinin Fc bölgesini bağlayarak fagositozu nötralize eden bu molekül hangisidir?",
            [
                {
                    "text": "Protein A",
                    "isCorrect": True,
                    "explanation": "Doğru. S. aureus hücre duvarındaki Protein A, IgG antikorlarının Fc ucunu bağlar; antikorun Fab ucu dışarıda kalır. Nötrofillerin Fc reseptörleri antikoru tanıyamaz ve opsonofagositoz engellenir."
                },
                {
                    "text": "M Proteini",
                    "isCorrect": False,
                    "explanation": "Yanlış. M proteini Streptococcus pyogenes'in antifagositik yüzey proteinidir."
                },
                {
                    "text": "Koagülaz",
                    "isCorrect": False,
                    "explanation": "Yanlış. Koagülaz fibrinojeni fibrine çevirerek pıhtı bariyeri oluşturur, IgG Fc bölgesine bağlanmaz."
                }
            ]
        ),
        52: make_branching_logic(
            "Dalgalı ateş, gece terlemesi ve bel ağrısı şikayetiyle başvuran köylü bir hastada pastörize edilmemiş koyun peyniri tüketimi öyküsü alınıyor. Hastanın kanında Brucella bakterilerinin monosit ve makrofajların içinde canlı kaldığı tespit ediliyor.",
            "Fakültatif hücre içi patojen olan Brucella'nın makrofaj fagozomu içinde canlı kalarak kronik enfeksiyona yol açmasını sağlayan temel hücresel mekanizma nedir?",
            [
                {
                    "text": "Fagozom-lizozom füzyonunu engellemek ve fagozomal asidifikasyona direnç göstererek hücre içinde çoğalmak.",
                    "isCorrect": True,
                    "explanation": "Doğru. Brucella, Mycobacterium tuberculosis ve Legionella gibi fakültatif intrasellüler patojenler, fagozomun lizozomla birleşmesini bloke ederek lizozomal enzimlerden kaçar ve makrofaj içinde güvenle çoğalırlar."
                },
                {
                    "text": "Eritrositlerin içine girerek hemoglobin moleküllerini parçalamak.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bu Plasmodium sıtma parazitlerinin özelliğidir; Brucella mononükleer fagositik sistemde yaşar."
                },
                {
                    "text": "Derhal hücre dışına çıkarak nötrofilleri lize eden ekzotoksin salgılamak.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Brucella hücre dışında değil, makrofaj içinde saklanarak persistan seyreder."
                }
            ]
        ),
        56: make_branching_logic(
            "Afrika seyahatinden dönen bir hastada her 48 saatte bir tekrarlayan şiddetli titreme ve yüksek ateş nöbetleri görülüyor. Periferik kanda Plasmodium falciparum halka formları izleniyor.",
            "Parazitin dalgalı ateş nöbetlerine ve immün sistemden yıllarca kaçabilmesine zemin hazırlayan genetik mekanizma hangisidir?",
            [
                {
                    "text": "Antijenik Varyasyon (PfEMP-1 proteinlerinin yüzeyde sürekli genetik rekombinasyonla değiştirilmesi)",
                    "isCorrect": True,
                    "explanation": "Doğru. P. falciparum eritrosit membranında eksprese ettiği PfEMP-1 yüzey proteinlerini kodlayan 'var' gen ailesini sürekli değiştirerek (antijenik varyasyon) gelişen antikor yanıtından kurtulur."
                },
                {
                    "text": "Spor oluşturarak kanda inaktif halde beklemesi",
                    "isCorrect": False,
                    "explanation": "Yanlış. Parazitler spor oluşturmaz; antijenik modifikasyon yaparlar."
                },
                {
                    "text": "Bakteriyel plazmit transferi ile antibiyotik direnci kazanması",
                    "isCorrect": False,
                    "explanation": "Yanlış. Plasmodium ökaryotik bir protozoondur; bakteriyel plazmit taşımaz."
                }
            ]
        ),
        62: make_branching_logic(
            "Bir köyde su şebekesine kanalizasyon karışması sonucu 48 saat içinde 300 kişide şiddetli pirinç suyu kıvamında ishal ve dehidratasyon patlak veriyor. Etkenin Vibrio cholerae olduğu saptanıyor.",
            "Bu salgının epidemiyolojik paterni ve rezervuar kaynağı ile ilgili en doğru değerlendirme hangisidir?",
            [
                {
                    "text": "Tek kaynaktan (ortak kaynaklı su) yayılan ani patlamalı salgındır; acil klorlama ve temiz içme suyu sağlanmasıyla enfeksiyon zinciri hızla kırılır.",
                    "isCorrect": True,
                    "explanation": "Doğru. Kontamine su şebekesi tipik bir ortak kaynak salgınıdır (point source outbreak). Kaynağın dezenfeksiyonu veya kapatılması yeni vakaların ortaya çıkışını derhal durdurur."
                },
                {
                    "text": "Kişiden kişiye havayolu ile yayılan bir pandemidir; herkese cerrahi maske dağıtılmalıdır.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Kolera havayoluyla değil, fekal-oral yolla (kontamine su/gıda) bulaşır."
                },
                {
                    "text": "Vektör kaynaklı bir kene salgınıdır; köydeki hayvanlar ilaçlanmalıdır.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Kolera vektörlerle taşınmaz; su kaynaklı bir enterik patojendir."
                }
            ]
        ),
        66: make_branching_logic(
            "Yenidoğan yoğun bakım ünitesinde üç prematüre bebekte aynı gün Klebsiella pneumoniae sepsisi gelişiyor. Yapılan moleküler incelemede suşların klonal olarak tıpatıp aynı olduğu saptanıyor.",
            "Enfeksiyon kontrol komitesinin bulaşma zincirinde odaklanması gereken en olası transfer aracı (ara konak) nedir?",
            [
                {
                    "text": "Sağlık personelinin elleri veya ortak kullanılan kontamine tıbbi aletler (fomitler)",
                    "isCorrect": True,
                    "explanation": "Doğru. Hastane ortamında bebekten bebeğe klonal bakteri geçişinin bir numaralı aracısı personelin yıkanmamış elleri ve ortak kullanılan steteskop, derece veya aspiratörlerdir (kontakt bulaş)."
                },
                {
                    "text": "Hastane bahçesindeki sokak kedileri ve sinekler",
                    "isCorrect": False,
                    "explanation": "Yanlış. Yenidoğan yoğun bakımında klonal Klebsiella salgını hastane içi temasla yayılır; sokak hayvanlarıyla ilişkili değildir."
                },
                {
                    "text": "Merkezi havalandırma sisteminden üflenen steril hava",
                    "isCorrect": False,
                    "explanation": "Yanlış. Klebsiella havayolu aerosolüyle değil, temas yoluyla bulaşır."
                }
            ]
        ),
        72: make_branching_logic(
            "Bir tüberküloz hastasının yattığı odaya girecek olan stajyer doktorun enfeksiyon zincirini kırmak ve akciğerlerini korumak için alması gereken en uygun kişisel koruyucu donanım (KKD) hangisidir?",
            "Tüberküloz basillerinin havada saatlerce asılı kalan ince çekirdekli damlacıklar (aerosol) halinde taşındığı bilinmektedir.",
            [
                {
                    "text": "N95 / FFP2 veya FFP3 partikül filtreli solunum maskesi takmak ve hastayı negatif basınçlı odaya almak.",
                    "isCorrect": True,
                    "explanation": "Doğru. Mycobacterium tuberculosis partikül boyutu <5 mikron olan havayolu (airborne) çekirdekleriyle yayılır; standart cerrahi maskeler kenarlardan sızdırır, mutlaka yüze tam oturan N95 maske ve negatif basınçlı izolasyon gerekir."
                },
                {
                    "text": "Basit cerrahi maske takmak ve kapıyı sonuna kadar açık bırakmak.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Cerrahi maske aerosolleri filtrelemez ve kapının açık kalması basillerin koridora yayılmasına neden olur."
                },
                {
                    "text": "Yalnızca steril eldiven takmak, maske takmaya gerek görmemek.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Tüberküloz temasla değil inhalasyonla bulaşır; maskesiz solunum ölümcül bulaşa yol açar."
                }
            ]
        ),
        76: make_branching_logic(
            "Kurban Bayramı'nda büyükbaş hayvan kesimi yapan bir kasabın el sırtında 5 gün sonra ağrısız, etrafı veziküllerle çevrili, ortası siyah nekrotik bir yara (eskar) beliriyor. Çevresinde belirgin ödem izleniyor.",
            "Bacillus anthracis kaynaklı bu klinik tablonun adı ve etkenin mikrobiyolojik morfolojisi hangisidir?",
            [
                {
                    "text": "Kutanöz Şarbon (Malign Püstül); Gram-pozitif sporlu basil",
                    "isCorrect": True,
                    "explanation": "Doğru. Şarbonun kutanöz formunda ağrısız siyah nekrotik eskar ve jelatinöz ödem karakteristiktir. Bacillus anthracis büyük, bambu kamışı görünümlü, Gram-pozitif, sporlu ve kapsüllü bir basildir."
                },
                {
                    "text": "Kedi tırmığı hastalığı; Gram-negatif pleomorfik basil",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bartonella henselae kedi tırmığı yapar, büyükbaş hayvan kesimiyle ve siyah eskarla ilişkili değildir."
                },
                {
                    "text": "Gazlı Gangren; Gram-pozitif anaerop sporlu basil",
                    "isCorrect": False,
                    "explanation": "Yanlış. Gazlı gangrende aşırı şiddetli ağrı, gaz çıtırtısı ve nekroz vardır; şarbonun eskarı ise ağrısızdır."
                }
            ]
        ),
        80: make_branching_logic(
            "Kırsal alanda tarlada çalışırken bacağından kene tutunan ve keneyi çıplak elle ezerek koparan 45 yaşındaki çiftçide 4 gün sonra ani başlayan 40 derece ateş, kas ağrısı, burun kanaması ve trombositopeni gelişiyor.",
            "Kırım-Kongo Kanamalı Ateşi (KKKA) şüphesinde bulaşmadan sorumlu rezervuar/vektör kene cinsi ve etken mikroorganizma hangisidir?",
            [
                {
                    "text": "Hyalomma cinsi sert keneler ve Nairoviridae ailesinden KKKA virüsü",
                    "isCorrect": True,
                    "explanation": "Doğru. KKKA, Hyalomma marginatum kenelerinin ısırması veya ezilmesiyle bulaşan, yaygın endotel hasarı ve DIC tablosuyla seyreden yüksek mortaliteli bir viral zoonozdur."
                },
                {
                    "text": "Ixodes keneleri ve Borrelia burgdorferi bakterisi",
                    "isCorrect": False,
                    "explanation": "Yanlış. Ixodes keneleri Lyme hastalığı etkeni olan Borrelia'yı bulaştırır; kanamalı ateş yapmaz."
                },
                {
                    "text": "Rhipicephalus keneleri ve Rickettsia conorii",
                    "isCorrect": False,
                    "explanation": "Yanlış. Bu kene Akdeniz benekli humması etkenidir, masif kanamalı viral tablo oluşturmaz."
                }
            ]
        ),
        84: make_branching_logic(
            "Grip benzeri halsizlik ve hafif ateş yakınmasıyla başvuran bir hastada hekim viral üst solunum yolu enfeksiyonu prodromunda olduğunu düşünüyor. Hastanın 2 gün sonra vücudunda çiçek döküntüleri beliriyor.",
            "Prodromal dönemdeki bu hastanın bulaştırıcılığı ve toplum sağlığı riski ile ilgili en kritik ilke hangisidir?",
            [
                {
                    "text": "Prodromal dönemde özgül tanı konamasa bile patojen saçılımı başlamış olabilir; hasta bu evrede oldukça bulaştırıcıdır.",
                    "isCorrect": True,
                    "explanation": "Doğru. Kızamık, suçiçeği ve SARS-CoV-2 gibi pek çok enfeksiyonda prodrom evresinde yüksek titrede mikrop saçılımı vardır. Hastanın 'basit üşütme' sanılarak izole edilmemesi salgınları tetikler."
                },
                {
                    "text": "Prodrom evresinde mikroorganizma henüz çoğalmadığı için hiçbir bulaş riski yoktur.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Prodrom evresi patojenin kritik eşiğe ulaştığı evredir ve bulaştırıcılık son derece yüksektir."
                },
                {
                    "text": "Prodrom evresindeki bir hastaya derhal geniş spektrumlu 3 antibiyotik başlanmalıdır.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Viral prodromda antibiyotiklerin yeri yoktur; gereksiz antibiyotik direnç oluşturur."
                }
            ]
        ),
        88: make_branching_logic(
            "Bir okulda sarılık salgını araştırılırken, kreş çağındaki 4 yaşındaki çocukların hiçbirinde sarılık görülmediği ancak tamamında serum Anti-HAV IgM antikorlarının pozitifleştiği saptanıyor.",
            "Küçük çocuklarda Hepatit A virüsünün bu sessiz seyrini ve epidemiyolojik tehlikesini en iyi anlatan kavram hangisidir?",
            [
                {
                    "text": "Subklinik (Asemptomatik) Enfeksiyon; çocuklar sarılık olmasalar da dışkılarıyla virüsü saçarak ebeveynlerine bulaştırırlar.",
                    "isCorrect": True,
                    "explanation": "Doğru. Hepatit A çocuklarda %80 oranında sarılıksız (anovikterik) ve subklinik seyreder; ancak bu çocuklar çevreye virüs saçarak evdeki yetişkinlerin ağır akut hepatit geçirmesine kaynaklık ederler."
                },
                {
                    "text": "Toksikasyon; çocukların karaciğer enzimleri virüsten hiç etkilenmemiştir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Anti-HAV IgM pozitifliği aktif viral replikasyonun ve immün yanıtın kesin kanıtıdır."
                },
                {
                    "text": "Yalancı Pozitiflik; çocuklarda hiçbir viral enfeksiyon antikor oluşturamaz.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Çocukların bağışıklık sistemi son derece aktiftir ve antikor üretir."
                }
            ]
        ),
        92: make_branching_logic(
            "Şüpheli cinsel temastan 3 gün sonra paniğe kapılarak kliniğe başvuran bir kişide Anti-HIV antikor testi (ELISA) negatif sonuçlanıyor.",
            "Hekimin bu test sonucunu yorumlarken pencere dönemi (window period) açısından hastaya vermesi gereken en doğru tıbbi bilgi hangisidir?",
            [
                {
                    "text": "Testin negatif olması kesinlikle virüs alınmadığını kanıtlamaz; antikor oluşumu için 2-6 hafta (pencere dönemi) gerekir, erken evrede şüphe varsa HIV-RNA (PCR) bakılmalı veya test tekrarlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "Doğru. Pencere döneminde kanda virüs çoğalmakta ve hasta bulaştırıcı olmakta iken serolojik antikorlar henüz ölçülebilir titreye ulaşmamıştır. Bu evrede antikor testleri yalancı negatif verir."
                },
                {
                    "text": "ELISA testi negatif çıktığı için hasta tamamen sağlıklıdır ve bir daha asla kontrol testine gerek yoktur.",
                    "isCorrect": False,
                    "explanation": "Yanlış. 3. günde antikor oluşması imkansızdır; bu sonuç erken dönemin kısıtlılığını yansıtır."
                },
                {
                    "text": "Pencere dönemi kavramı sadece bakteriler için geçerlidir, virüslerde ilk dakikadan itibaren antikor saptanır.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Antikor üretimi için B hücre klonlarının uyarılması en az 1-2 hafta sürer."
                }
            ]
        ),
        94: make_branching_logic(
            "Yüksek ateş ve lökositozla yatan hastanın sağ kolundan alınan kan kültürü şişesinde 24 saat sonra koagülaz-negatif stafilokok (KNS) ürerken, sol koldan alınan çift sette hiçbir üreme olmuyor.",
            "Enfeksiyon hastalıkları uzmanının bu tek şişedeki üremeyi değerlendirirken izlemesi gereken en doğru strateji hangisidir?",
            [
                {
                    "text": "Bu durum büyük olasılıkla cilt antisepsisinin yetersizliğine bağlı bir kontaminasyondur; hastaya derhal gereksiz vankomisin başlanmamalı, klinik tablo stabilse kan kültürleri tekrarlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "Doğru. Kan kültürlerinde tek bir şişede KNS veya difteroid gibi cilt florası üremesi sıklıkla kontaminasyonu işaret eder. Gerçek bakteriyemiden söz edebilmek için birden fazla farklı koldan alınan şişede aynı bakterinin üremesi gerekir."
                },
                {
                    "text": "Tek şişede bir tek bakteri hücresi bile ürese bu kesin endokardittir ve 6 hafta damardan üçlü antibiyotik verilmelidir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Kan kültürü kontaminasyonları gereksiz antibiyotik kullanımının en sık nedenidir."
                },
                {
                    "text": "Sol koldaki kan kültürü cihazının bozuk olduğu kabul edilmeli ve laboratuvar kapatılmalıdır.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Cihaz hatası değil, ven ponksiyonu sırasında cilt florasının şişeye taşınması söz konusudur."
                }
            ]
        ),
        97: make_branching_logic(
            "Hastaneye apandisit ameliyatı için yatan ve ameliyatı sorunsuz geçen hastada yatışının 4. gününde yoğun balgamlı öksürük, akciğer grafisinde yeni infiltrasyon ve 38.8 derece ateş gelişiyor.",
            "Bu klinik tablonun Sağlık Hizmeti İlişkili Enfeksiyon (SHİE) olarak kabul edilmesinin temel gerekçesi hangisidir?",
            [
                {
                    "text": "Hastanın hastaneye yatışında inkübasyon evresinde olmaması ve belirtilerin hastaneye yatıştan en az 48 saat sonra ortaya çıkmış olmasıdır.",
                    "isCorrect": True,
                    "explanation": "Doğru. SHİE tanımının temel kriteri, enfeksiyonun yatış anında kuluçkada bulunmaması ve yatıştan itibaren en az 48 saat geçtikten sonra hastanede edinilmiş olarak patlak vermesidir."
                },
                {
                    "text": "Hastanın ameliyat edilmiş olması tek başına SHİE tanısı koydurur, 48 saat kuralı önemsizdir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Yatıştan sonraki ilk 24 saatte gelişen enfeksiyonlar toplum kökenli kabul edilir; 48 saat kuralı esastır."
                },
                {
                    "text": "Pnömoniler asla hastane enfeksiyonu sayılamaz, sadece cerrahi yara yerleri SHİE olabilir.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Hastane kökenli pnömoni ve ventilatör ilişkili pnömoni en ölümcül SHİE türlerindendir."
                }
            ]
        ),
        99: make_branching_logic(
            "Uzak Doğu'da bir canlı hayvan pazarında çalışan işçilerde ağır akut solunum sıkıntısı ve atipik pnömoni ile seyreden yeni bir koronavirüs suşu tespit ediliyor.",
            "Bu yeni ortaya çıkan (emerging) pandemik tehdidi kontrol altına almak için 'Tek Sağlık' konsepti çerçevesinde atılması gereken en kritik adım hangisidir?",
            [
                {
                    "text": "Tıp hekimleri, veterinerler ve vahşi yaşam biyologlarının ortak çalışarak hayvan rezervuarını saptaması, pazardaki hayvan ticaretini denetlemesi ve insan-hayvan temas zincirini kırması.",
                    "isCorrect": True,
                    "explanation": "Doğru. Emerging enfeksiyonların %75'i zoonotik kökenlidir. Tek Sağlık yaklaşımı insan, evcil/yabani hayvan ve çevre sağlığını tek bir şemsiye altında multidisipliner olarak yönetmeyi şart koşar."
                },
                {
                    "text": "Sadece insan hastaları tedavi etmek, hayvan pazarları ve vahşi hayvan rezervuarlarıyla hiç ilgilenmemek.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Rezervuar kontrol edilmedikçe hayvanlardan insanlara virüs sıçraması devam eder ve salgın önlenemez."
                },
                {
                    "text": "Bölgedeki tüm antibiyotik fabrikalarını kapatıp yalnızca vitamin dağıtmak.",
                    "isCorrect": False,
                    "explanation": "Yanlış. Viral pandemilerde virüsün biyolojisini ve bulaşma zincirini hedefleyen entegre epidemiyolojik adımlar esastır."
                }
            ]
        )
    }

def get_extra_chains():
    """Causal chain (patofizyolojik etki mekanizması) ögeleri."""
    return {
        7: make_causal_chain(
            "Fırsatçı Patojenlerin İnvazyon Kaskadı",
            [
                "1. İmmün Çöküş: Nötropeni veya geniş spektrumlu antibiyotikle doğal bariyerler zayıflar.",
                "2. Aşırı Çoğalma: Düşük virülanslı kommensal bakteri yüzeyde kontrolsüzce çoğalır.",
                "3. Epitelyal Geçiş: Hasarlı mukoza veya kateter lümeninden submukozaya sızar.",
                "4. Dolaşıma Karışma: Fagosite edilemeyen patojen damar yatağına ulaşarak bakteriyemi yapar."
            ]
        ),
        15: make_causal_chain(
            "Bakteriyel Adezyon ve Kolonizasyon Süreci",
            [
                "1. Yaklaşma: Mikroorganizma konak epitel yüzeyine elektrostatik çekimle yaklaşır.",
                "2. Spesifik Kilitlenme: Fimbriya adezinleri epitel reseptörlerine anahtar-kilit gibi bağlanır.",
                "3. Yıkama Direnci: Mukosiliyer akım ve sıvı geçişine rağmen yüzeyden koparılamaz.",
                "4. Mikrokoloni: Quorum sensing ile çoğalarak stabil kolonizasyon odağı oluşturur."
            ]
        ),
        25: make_causal_chain(
            "Biyofilm Tabakası Oluşum Evreleri",
            [
                "1. Geri Dönüşümlü Tutunma: Bakteriler kateter veya protez yüzeyine zayıfça temas eder.",
                "2. Stabil Bağlanma: Adezinler ve pili ile yüzeye geri dönüşümsüz olarak kilitlenir.",
                "3. Matriks Sentezi: Hücre dışı ekzopolisakkarit (EPS) salgılanarak koruyucu zırh örülür.",
                "4. Olgunlaşma: Matriks içinde besin kanalları ve antibiyotiklere dirençli mikrokoloniler gelişir.",
                "5. Dağılma (Dispersal): Biyofilmden kopan bakteriler dolaşıma katılarak metastatik apseler kurar."
            ]
        ),
        35: make_causal_chain(
            "Tetanospazmin Aracılı Rijit Kas Spazmı Mekanizması",
            [
                "1. Yara İnokülasyonu: Clostridium tetani sporları derin anaerop yarada çimlenir.",
                "2. Retrograd Aksonal Göç: Tetanospazmin motor aksonlar boyunca medulla spinalise taşınır.",
                "3. Renshaw İnhibisyonu: İnhibitör internöronlarda sinaptobrevin parçalanır.",
                "4. GABA Blokajı: Glisin ve GABA salınımı durunca alfa motor nöronlar kontrolsüz uyarılır.",
                "5. Spastik Felç: Çenede trismus, yüzde alaycı gülüş (risus sardonicus) ve opistotonus gelişir."
            ]
        ),
        45: make_causal_chain(
            "Süperantijen Aracılı Toksik Şok Sendromu Kaskadı",
            [
                "1. Salınım: S. aureus TSST-1 veya S. pyogenes SpeA ekzotoksinini kana verir.",
                "2. Non-Spesifik Köprü: Toksin MHC-II ile TCR'ın V-beta bölgesine dışarıdan köprü kurar.",
                "3. Masif T Hücre Aktivasyonu: Dolaşımdaki T hücrelerinin %20'si kontrolsüzce uyarılır.",
                "4. Sitokin Fırtınası: Devasa miktarda IL-1, IL-2, TNF-alfa ve IFN-gama salınır.",
                "5. Şok ve Döküntü: Yaygın kapiller sızıntı, inatçı hipotansiyon ve deskuamasyon gelişir."
            ]
        ),
        55: make_causal_chain(
            "Kapsüllü Bakterilerin İmmün Kaçış Zinciri",
            [
                "1. Kapsül Zırhı: Patojen yüzeyini nötr polisakkarit kılıfla kaplar.",
                "2. Kompleman Maskelemesi: C3b'nin hücre duvarına kovalent bağlanması engellenir.",
                "3. Opsonizasyon Yetmezliği: Nötrofil ve makrofajlar bakteriyi tanıyamaz.",
                "4. İnvazyon ve Bakteriyemi: Fagosite edilemeyen kapsüllü bakteri meninks veya kana yayılır."
            ]
        ),
        65: make_causal_chain(
            "Fekal-Oral Bulaşma Zincirinin İlerlemesi",
            [
                "1. Kaynak Saçılımı: Enfekte hasta veya taşıyıcı patojeni dışkı ile çevreye atar.",
                "2. Su/Gıda Kontaminasyonu: Arıtılmamış atık sular kuyuya veya sulama suyuna karışır.",
                "3. Tüketim: Yeni duyarlı konak klorlanmamış suyu içer veya çiğ sebzeyi yer.",
                "4. Mide Asidini Aşma: Kritik doza ulaşan patojen sindirim epiteline kolonize olur."
            ]
        ),
        75: make_causal_chain(
            "Zoonotik Bulaşmada Tür Atlama Aşamaları",
            [
                "1. Doğal Rezervuar: Patojen yarasa, kemirici veya yabani kuşta asemptomatik yaşar.",
                "2. Ara Konak Teması: Vahşi hayvan evcil çiftlik hayvanlarıyla temas eder.",
                "3. İnsan Teması: Enfekte hayvanın kesimi, sütü veya etiyle insan enfekte olur.",
                "4. İnsandan İnsana Adaptasyon: Mutasyon kazanan patojen insandan insana yayılmaya başlar."
            ]
        ),
        85: make_causal_chain(
            "Akut Enfeksiyonun Patolojik Zirveye İlerlemesi",
            [
                "1. Patojen İnvazyonu: Doku bariyerini aşan mikroorganizma geometrik hızla çoğalır.",
                "2. Doku Nekrozu: Patojen toksinleri ve lökosit degranülasyonu hücreleri eritir.",
                "3. Patognomonik Belirtiler: Hedef organ disfonksiyonuna bağlı özgül bulgular belirir.",
                "4. İmmün Çatışma: Sitotoksik T hücreleri ve nötrofiller maksimum inflamatuar yanıt verir."
            ]
        ),
        95: make_causal_chain(
            "Antibiyotik Seçiminde De-Eskalasyon Mantığı",
            [
                "1. Kültür Alımı: Tedavi öncesi kan ve doku örnekleri aseptik kurallarla alınır.",
                "2. Ampirik Kapsama: Hayatı tehdit eden durumda geniş spektrumlu antibiyotik başlanır.",
                "3. Antibiyogram Raporu: 48 saat sonra etkenin duyarlı olduğu ilaçlar listelenir.",
                "4. Hedefe Yönelik Daraltma: En dar spektrumlu ilaca geçilerek flora korunur ve direnç önlenir."
            ]
        )
    }

def get_extra_sliders():
    """Before/after slider (karşılaştırmalı durum ve fizyopatolojik geçiş) ögeleri."""
    return {
        18: make_before_after(
            "Kommensal Flora ile İnvaziv Patojen Ayrımı",
            "Dost Kommensal Flora",
            "Epitel yüzeyini kaplayarak patojenlerin tutunmasını engeller, vitamin üretir ve immüniteyi eğitir.",
            "İnvaziv Patojen",
            "Adezinleri ve toksinleriyle konak hücrelerini parçalar, derin dokulara sızarak inflamasyon başlatır.",
            "Floranın koruyucu kolonizasyon direnci ile patojenin doku yıkıcı invazyonunun kıyaslanması"
        ),
        38: make_before_after(
            "Ekzotoksin ile Endotoksin Arasındaki Temel Zıtlık",
            "Bakteriyel Ekzotoksin",
            "Canlı bakteri tarafından salgılanır, protein yapıdadır, ısıya duyarlıdır ve aşılanabilir toksoid oluşturur.",
            "Bakteriyel Endotoksin",
            "Gram-negatif hücre duvarı parçalanınca açığa çıkar, LPS/Lipid A yapıdadır, ısıya dirençlidir ve toksoidi yoktur.",
            "Protein yapılı spesifik toksin ile lipit yapılı sistemik şok toksininin moleküler ayrımı"
        ),
        58: make_before_after(
            "Antijenik Sapma (Drift) ile Antijenik Kayma (Shift) Kıyaslaması",
            "Antijenik Sapma (Drift)",
            "Nokta mutasyonlarıyla yavaşça gelişir; küçük antijenik değişiklikler yapar ve yıllık mevsimsel epidemilere yol açar.",
            "Antijenik Kayma (Shift)",
            "Farklı türlerin virüs genomlarının rekombinasyonu ile aniden yeni yüzey proteini doğar; küresel ölümcül pandemilere yol açar.",
            "İnfluenza virüsünün kademeli mevsimsel değişimi ile aniden patlayan küresel pandemi mekanizması"
        ),
        78: make_before_after(
            "Doğrudan Temas ile Vektör Aracılı Bulaşma Farkı",
            "Doğrudan Temas Yolu",
            "Patojen enfekte kişinin derisinden, cinsel salgısından veya yarasından doğrudan yeni konağa transfer edilir.",
            "Biyolojik Vektör Yolu",
            "Patojen sivrisinek veya kene gibi canlı bir eklembacaklının vücudunda çoğalarak ısırıkla yeni konağa aşılanır.",
            "Fiziksel temas transferi ile canlı eklembacaklı ara konak aracılı aşılanmanın ayrımı"
        )
    }

def get_extra_recalls():
    """Active recall (derin kavrama ve sınav spotu sorgulama) ögeleri."""
    return {
        48: make_active_recall(
            "Gram-pozitif bakterilerin ürettiği Süperantijenlerin konak immün sistemini klasik antijenlerden farklı olarak devasa boyutta uyarmasının nedeni nedir?",
            "Süperantijenler antijen sunumuna ihtiyaç duymadan MHC Sınıf II molekülü ile T hücre reseptörünün (TCR) V-beta bölgesine dışarıdan doğrudan bağlanarak dolaşımdaki T hücrelerinin %20'sini birden aktive eder ve ölümcül sitokin fırtınasına yol açar.",
            "MHC-TCR dış yüzey köprüleme mekanizması"
        ),
        68: make_active_recall(
            "Enfeksiyon kontrolünde kaynak (rezervuar) ile bulaşma yolu arasındaki ayrımın en pratik önemi nedir?",
            "Kaynağa yönelik müdahaleler (vaka izolasyonu, hasta tedavisi, taşıyıcı tespiti) mikrobun çıkışını durdururken; bulaşma yoluna yönelik müdahaleler (el hijyeni, maske, su klorlama) mikrobun yeni kişiye transferini fiziksel olarak engeller.",
            "Rezervuar kontrolü ile geçiş engelleme stratejisinin ayrımı"
        )
    }

def apply_enrichment(slides):
    """Slayt listesine tüm ek interaktif ögeleri entegre eder."""
    extra_branching = get_extra_branching()
    extra_chains = get_extra_chains()
    extra_sliders = get_extra_sliders()
    extra_recalls = get_extra_recalls()

    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        if "elements" in slide:
            elements = slide["elements"]
        else:
            elements = slide.setdefault("interactiveElements", [])

        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_chains:
            elements.append(extra_chains[slide_num])
        if slide_num in extra_sliders:
            elements.append(extra_sliders[slide_num])
        if slide_num in extra_recalls:
            elements.append(extra_recalls[slide_num])

    return slides
