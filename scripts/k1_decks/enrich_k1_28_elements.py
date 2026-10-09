# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.

Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar:
- branching_logic: +19 adet (toplam 28, ~%11.3)
- causal_chain: +17 adet (toplam 28, ~%11.3)
- micro_quiz: +10 adet (toplam 27, ~%11.0)
- before_after_slider: +3 adet (toplam 28, ~%11.3)
"""

from scripts.k1_28_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar senaryoları) ek ögeleri (19 adet)."""
    return {
        3: make_branching_logic(
            "Meme biyopsisinde lobüler glandüler yapılar ile bol mikzoid stromadan oluşan, kapsüllü ve 2 cm çapında kitle saptanan 24 yaşındaki kadın hasta değerlendiriliyor.",
            "Tümörün parankim ve stroma analizi yapıldığında patoloğun bu kitlenin biyolojik davranışını ve tanısını belirlemede izleyeceği en uygun patolojik yaklaşım nedir?",
            [
                {
                    "text": "Parankimal epitel hücrelerinde hücresel atipi ve stromal infiltrasyon aranmalı; benign bifazik bir neoplazm olan fibroadenom tanısı verilmelidir.",
                    "isCorrect": True,
                    "explanation": "Fibroadenom hem epitelyal glandüler hem de fibröz stromal proliferasyondan oluşan benign mikst bir neoplazmdır."
                },
                {
                    "text": "Stroma yoğunluğu yüksek olduğu için kitlenin doğrudan mezenkimal kaynaklı malign osteosarkom olduğu kabul edilmelidir.",
                    "isCorrect": False,
                    "explanation": "Mikzoid veya fibröz stroma sarkom kanıtı değildir; hücre atipisi ve osteoid üretim aranmalıdır."
                },
                {
                    "text": "Lobüler yapılar varlığı doğrudan lobüler karsinom kanıtı olup acil radikal mastektomi önerilmelidir.",
                    "isCorrect": False,
                    "explanation": "Kapsüllü ve düzenli glandüler yapılar benign fibroadenom ile uyumludur."
                }
            ]
        ),
        7: make_branching_logic(
            "Kolorektal adenokarsinom tanısı alan 58 yaşındaki hastada anti-EGFR monoklonal antikor tedavisi (setuksimab) planlanmaktadır.",
            "Bu hedefe yönelik biyolojik tedavinin uygulanabilirliğini belirlemek için onkoloji konseyinde öncelikle hangi moleküler patoloji testi istenmelidir?",
            [
                {
                    "text": "KRAS ve NRAS gen dizilemesi; şayet RAS yolağında sürücü mutasyon varsa EGFR blokajı etkisiz olacağından tedavi verilmemelidir.",
                    "isCorrect": True,
                    "explanation": "KRAS geni mutant ise reseptörün aşağısındaki yolak otonom aktif kalır; EGFR blokerleri hiçbir klinik fayda sağlamaz."
                },
                {
                    "text": "Tümör dokusunda p24 antijen düzeyi ve viral yük bakılmalıdır.",
                    "isCorrect": False,
                    "explanation": "p24 HIV belirtecidir, kolon kanseri EGFR hedefe yönelik tedavisiyle ilişkisi yoktur."
                },
                {
                    "text": "Anti-EGFR tedavisinin tek belirleyicisi serum laktat dehidrogenaz (LDH) düzeyidir.",
                    "isCorrect": False,
                    "explanation": "Moleküler yanıt için KRAS/NRAS mutasyon analizi şarttır."
                }
            ]
        ),
        13: make_branching_logic(
            "Subkutan yerleşimli, hareketli ve yavaş büyüyen 3 cm kitle eksizyonu yapılan hastada histopatolojide fibröz kapsülle çevrili, olgun üniviloküler yağ hücreleri izleniyor; atipi veya mitoz saptanmıyor.",
            "Bu patolojik bulgular ışığında kitlenin biyolojik doğası ve klinik prognozu nasıl sınıflandırılmalıdır?",
            [
                {
                    "text": "İyi diferansiye benign lipom; cerrahi eksizyon ile tam kür sağlanır ve nüks beklenmez.",
                    "isCorrect": True,
                    "explanation": "Normal yağ dokusuna birebir benzeyen, kapsüllü ve atipisiz lezyon benign lipomdur; lokal eksizyon küratiftir."
                },
                {
                    "text": "Tümör yağ dokusundan köken aldığı için daima malign liposarkom kabul edilip geniş rezeksiyon yapılmalıdır.",
                    "isCorrect": False,
                    "explanation": "Liposarkomda lipoblastlar, nükleer atipi ve infiltratif sınır görülür; bu olguda atipi yoktur."
                },
                {
                    "text": "Lezyon çevre bağ dokusuna invaze kabul edilip adjuvan radyoterapiye başlanmalıdır.",
                    "isCorrect": False,
                    "explanation": "Kapsüllü benign lipomda radyoterapi endikasyonu yoktur."
                }
            ]
        ),
        16: make_branching_logic(
            "Uterusta multipl düzgün sınırlı nodülleri olan 42 yaşındaki kadın hastanın myomektomi materyalinde düz kas hücrelerinin oluşturduğu hiposelüler girdap paternleri saptanıyor.",
            "Patoloğun leiomyom ile leiomyosarkom ayırıcı tanısında kitleyi malignite lehine yorumlamasını gerektiren en kritik tanısal triad nedir?",
            [
                {
                    "text": "Belirgin sitolojik atipi, yüksek mitotik indeks (>10 mitoz/10 BBA) ve koagülatif tümör hücre nekrozu.",
                    "isCorrect": True,
                    "explanation": "Uterus düz kas neoplazmlarında malignite kriterleri atipi, mitotik hız ve tümör hücre nekrozunun birlikteliğidir."
                },
                {
                    "text": "Tümörün birden fazla odakta görülmesi ve hastanın premenopozal yaşta olması.",
                    "isCorrect": False,
                    "explanation": "Uterin leiomyomlar sıklıkla multifokaldir ve premenopozda çok yaygındır."
                },
                {
                    "text": "Kitle içerisinde distrofik kalsifikasyon ve hyalin dejenerasyon alanlarının varlığı.",
                    "isCorrect": False,
                    "explanation": "Distrofik kalsifikasyon ve hyalinizasyon benign leiomyomların klasik dejeneratif değişiklikleridir."
                }
            ]
        ),
        23: make_branching_logic(
            "Kolonoskopi taramasında rektosigmoid bölgede 1.5 cm saplı polip saptanan 55 yaşındaki hastanın polipektomi spesimeninde tübüler yapılar oluşturan displastik epitel izleniyor ancak muskularis mukoza sağlam.",
            "Bu lezyonun patolojik terminolojik sınıflandırması ve hastaya yaklaşım ne olmalıdır?",
            [
                {
                    "text": "Tübüler adenom (benign prekanseröz epitel lezyonu); sap cerrahi sınırı negatifse tam eksizyon ile takip yeterlidir.",
                    "isCorrect": True,
                    "explanation": "Muskularis mukozayı aşmayan lezyon adenomdur; sap sınırı temizse küratiftir."
                },
                {
                    "text": "İnvaziv adenokarsinom gelişmiştir; derhal segmental rezeksiyon ve lenfadenektomi uygulanmalıdır.",
                    "isCorrect": False,
                    "explanation": "Muskularis mukoza sağlam olduğundan invazyon yoktur, karsinom tanısı verilemez."
                },
                {
                    "text": "Lezyon inflamatuar psödopolip olup kanser riski taşımaz, takibe gerek yoktur.",
                    "isCorrect": False,
                    "explanation": "Displastik epitelyal adenomlar kolorektal karsinomun majör premalign öncülleridir."
                }
            ]
        ),
        26: make_branching_logic(
            "Mide endoskopisinde antrumda lümeni daraltan ülsere bir kitle saptanan 64 yaşındaki hastanın biyopsisinde hücrelerarası köprüler ve keratin incileri içermeyen, glandüler tübüller oluşturan atipik hücreler izleniyor.",
            "Bu malign epitelyal neoplazmın terminolojik isimlendirilmesi hangi seçenekte eksiksiz verilmiştir?",
            [
                {
                    "text": "Mide Adenokarsinomu (Glandüler diferansiyasyon gösteren malign epitel tümörü)",
                    "isCorrect": True,
                    "explanation": "Glandüler diferansiyasyon sergileyen karsinomlar 'adenokarsinom' olarak adlandırılır."
                },
                {
                    "text": "Mide Skuamöz Hücreli Karsinomu",
                    "isCorrect": False,
                    "explanation": "Skuamöz karsinom keratin incileri ve intersellüler köprülerle karakterizedir; burada glandüler tübüller vardır."
                },
                {
                    "text": "Gastrik Leiomyom",
                    "isCorrect": False,
                    "explanation": "Leiomyom düz kas kökenli benign bir neoplazmdır."
                }
            ]
        ),
        33: make_branching_logic(
            "Uyluk derin adale lojunda 12 cm çapında, çevre dokuya infiltre, kıkırdak matrisi üreten pleomorfik kondrositlerden zengin kitle rezeke ediliyor.",
            "Bu mezenkimal kaynaklı malign neoplazmın histopatolojik adlandırılması ve metastaz paterni nasıldır?",
            [
                {
                    "text": "Kondrosarkom; mezenkimal malignite olduğu için primer olarak hematojen yolla akciğere yayılır.",
                    "isCorrect": True,
                    "explanation": "Kıkırdak üreten malign mezenkimal neoplazm kondrosarkomdur ve sarkomlar kural olarak hematojen yolla akciğere metastaz yapar."
                },
                {
                    "text": "Kondrom; benign bir tümör olup lenfatik yolla bölgesel lenf nodlarına yayılır.",
                    "isCorrect": False,
                    "explanation": "Kondrom benign olup metastaz yapmaz; bu lezyon infiltratif ve pleomorfiktir."
                },
                {
                    "text": "Skuamöz karsinom; epitelyal kökenli olup perinevral yayılım gösterir.",
                    "isCorrect": False,
                    "explanation": "Kıkırdak mezenkimal bir dokudur; karsinom terimi epitelyal maligniteler için kullanılır."
                }
            ]
        ),
        36: make_branching_logic(
            "Kulak önünde parotis bezinde yavaş büyüyen, ağrısız kitle nedeniyle opere edilen hastada epitelyal adacıklar ile kondromikzoid mezenkimal matriksin iç içe geçtiği saptanıyor.",
            "Bu hastada patoloğun raporlaması gereken benign mikst tümör ve klinik önemi nedir?",
            [
                {
                    "text": "Pleomorfik Adenom (Benign mikst tümör); kapsülü ince ve psödopodlu olabileceğinden nüksü önlemek için yüzeyel parotidektomi ile çıkarılmalıdır.",
                    "isCorrect": True,
                    "explanation": "Tükürük bezinin en sık tümörü pleomorfik adenomdur; mikst komponentler içerir ve tam çıkarılmazsa nüks edebilir."
                },
                {
                    "text": "Mukoepidermoid karsinom; doğrudan malign kabul edilip boyun diseksiyonu yapılmalıdır.",
                    "isCorrect": False,
                    "explanation": "Kondromikzoid matriks ve epitelyal elemanlar pleomorfik adenom için klasiktir."
                },
                {
                    "text": "Warthin tümörü; bilateral kistik kitle olup yalnızca sigara içenlerde görülür.",
                    "isCorrect": False,
                    "explanation": "Warthin tümöründe çift sıralı onkositik epitel ve yoğun lenfoid stroma bulunur."
                }
            ]
        ),
        43: make_branching_logic(
            "Yenidoğan bir bebeğin sakrokoksigeal bölgesinde tespit edilen 10 cm boyutundaki kitlede histopatolojik olarak solunum epiteli, bağırsak mukozası, nöroepitelyal odaklar, immatür kıkırdak ve yağ dokusu saptanıyor.",
            "Üç germ yaprağına ait türevler içeren bu neoplazmın sınıflaması ve malignite riski açısından en kritik inceleme nedir?",
            [
                {
                    "text": "Teratom; kitle içindeki nöroepitelyal dokuların immatürlük derecesinin belirlenmesi malign potansiyeli gösterir.",
                    "isCorrect": True,
                    "explanation": "Teratomlar üç germ yaprağından köken alır; immatür nöroepitel oranı tümörün grade'ini ve malign potansiyelini belirler."
                },
                {
                    "text": "Hamartom; tamamen olgun dokuların disorganize yığını olup malignite riski sıfırdır.",
                    "isCorrect": False,
                    "explanation": "Farklı germ yapraklarının varlığı hamartom değil, teratom tanısı koydurur."
                },
                {
                    "text": "Koristom; heterotopik normal doku ektopisidir ve cerrahiye gerek yoktur.",
                    "isCorrect": False,
                    "explanation": "Koristom tek bir normal dokunun yabancı anatomik yerde bulunmasıdır."
                }
            ]
        ),
        53: make_branching_logic(
            "Tiroid ince iğne aspirasyon biyopsisinde nükleer yarıklar (groove), buzlu cam nükleus (Orphan Annie gözleri) ve intranükleer psödoinklüzyonlar saptanan 35 yaşındaki kadın hasta.",
            "Bu sitopatolojik bulgular karşısında kesin tanı ve cerrahi yaklaşım ne olmalıdır?",
            [
                {
                    "text": "Papiller Tiroid Karsinomu; total tiroidektomi ve santral boyun lenf nodu değerlendirmesi planlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "Buzlu cam nükleuslar, intranükleer inklüzyonlar ve nükleer yarıklar papiller tiroid karsinomu için patognomoniktir."
                },
                {
                    "text": "Medüller Tiroid Karsinomu; kalsitonin salgılayan parafolliküler C hücresi tümörüdür.",
                    "isCorrect": False,
                    "explanation": "Medüller karsinom amiloid stroma ve kalsitonin ile karakterizedir, Orphan Annie nükleusu içermez."
                },
                {
                    "text": "Tiroid Folliküler Adenomu; benign lezyon olup takip yeterlidir.",
                    "isCorrect": False,
                    "explanation": "Söz konusu nükleer atipiler folliküler adenomda görülmez, papiller karsinom göstergesidir."
                }
            ]
        ),
        56: make_branching_logic(
            "Postmenopozal kanama ile başvuran 60 yaşındaki kadında endometrial biyopside bez yapıları tamamen kaybolmuş, belirgin hücresel pleomorfizm ve atipik tripolar mitozlar içeren solid tümör tabakaları izleniyor.",
            "Bu tümörün diferansiyasyon derecesi ve klinik agresifliği nasıl derecelendirilmelidir?",
            [
                {
                    "text": "Grade 3 (Az diferansiye / Yüksek dereceli); agressif biyolojik gidişat ve yüksek metastaz potansiyeli taşır.",
                    "isCorrect": True,
                    "explanation": "Gland formasyonunun kaybolup solid tabakalara dönüşmesi Grade 3 az diferansiye/anaplastik karsinom kriteridir."
                },
                {
                    "text": "Grade 1 (İyi diferansiye); gland formasyonu korunduğu için son derece selim seyreder.",
                    "isCorrect": False,
                    "explanation": "Gland formasyonu korunmamış, tamamen solid tabakalar mevcuttur."
                },
                {
                    "text": "Lezyon displazi evresinde olup karsinom tanısı verilemez.",
                    "isCorrect": False,
                    "explanation": "Solid anaplastik büyüme ve atipik mitozlar invaziv yüksek dereceli malignite kanıtıdır."
                }
            ]
        ),
        63: make_branching_logic(
            "Kolonoskopi taramasında çekumda lümeni dolduran fungöz bir polipoid lezyon saptanıyor; rezeksiyon patolojisinde malign glandların submukozayı aşıp muskularis propriaya infiltre olduğu görülüyor.",
            "TNM evrelemesinde bu derinlikteki invaziv büyüme hangi patolojik T (primer tümör) kategorisine karşılık gelir?",
            [
                {
                    "text": "pT2 evresi (Tümör muskularis propriayı infiltre etmiştir ancak subserozaya geçmemiştir).",
                    "isCorrect": True,
                    "explanation": "TNM sınıflamasında pT1 submukoza invazyonu, pT2 muskularis propria invazyonudur."
                },
                {
                    "text": "Tis (Karsinoma in situ); muskularis mukozayı aşmamıştır.",
                    "isCorrect": False,
                    "explanation": "Muskularis propriaya invazyon geliştiği için karsinoma in situ kabul edilemez."
                },
                {
                    "text": "pT4 evresi; tümör visseral peritonu delmiş veya komşu organa yapışmıştır.",
                    "isCorrect": False,
                    "explanation": "pT4 seroza perforasyonu veya organ invazyonudur; muskularis propria pT2'dir."
                }
            ]
        ),
        66: make_branching_logic(
            "Aksiller lenf nodu diseksiyonu yapılan meme kanseri hastasında 15 lenf nodundan 4 adedinde metastatik karsinom odakları tespit ediliyor.",
            "Bu histopatolojik bulgu hastanın prognozu ve sistemik tedavi kararı üzerinde nasıl bir etki yaratır?",
            [
                {
                    "text": "Bölgesel lenf nodu metastazı prognozu dramatik kötüleştirir ve adjuvan sistemik kemoterapi endikasyonu doğurur.",
                    "isCorrect": True,
                    "explanation": "Lenf nodu pozitifliği mikrometastaz ve nüks riskini fırlatır; evreyi yükselterek kemoterapi gerektirir."
                },
                {
                    "text": "Lenf nodu tutulumu sadece lokal bir olay olup sistemik tedaviyi etkilemez.",
                    "isCorrect": False,
                    "explanation": "Lenf nodu metastazı hematolojik sistemik yayılım riskinin güçlü bir öngörücüsüdür."
                },
                {
                    "text": "Hastanın primer tümörü küçükse lenf nodu tutulumunun evrelemeye hiçbir katkısı yoktur.",
                    "isCorrect": False,
                    "explanation": "TNM evrelemesinde N (nod) parametresi bağımsız bir majör prognostik faktördür."
                }
            ]
        ),
        73: make_branching_logic(
            "Meme kanseri operasyonu sırasında cerrah nöbetçi (sentinel) lenf nodunu mavi boya ve radyoizotop kılavuzluğunda çıkararak patolojiye intraoperatif konsültasyona (frozen section) gönderiyor.",
            "Patoloğun dondurulmuş kesitte sentinel lenf nodunda metastaz saptaması durumunda cerrahi ekibin o anki tavrı ne olmalıdır?",
            [
                {
                    "text": "Sentinel lenf nodu pozitif olduğu için operasyona tam aksiller lenf nodu diseksiyonu ile devam edilmelidir.",
                    "isCorrect": True,
                    "explanation": "İlk filtre düğümünde tümör varsa gerideki nodlarda da metastaz riski yüksek olduğundan aksiller diseksiyona geçilir."
                },
                {
                    "text": "Frozen section güvenilir olmadığından operasyon derhal sonlandırılmalıdır.",
                    "isCorrect": False,
                    "explanation": "Frozen section intraoperatif karar için rutin ve güvenilir bir yöntemdir."
                },
                {
                    "text": "Sentinel nod tutulumunda mastektomiden vazgeçilip yalnızca radyoterapi verilmelidir.",
                    "isCorrect": False,
                    "explanation": "Pozitif sentinel nod aksiller diseksiyon endikasyonudur, primer cerrahiyi engellemez."
                }
            ]
        ),
        76: make_branching_logic(
            "Pankreas başı adenokarsinomu ameliyat edilen hastanın rezeksiyon materyalinde tümörün retroperitoneal cerrahi sınırda mürekkep işaretine sıfır mesafede olduğu saptanıyor.",
            "Patoloji raporunda cerrahi sınır tutulumu nasıl kodlanmalı ve onkolojik anlamı ne olmalıdır?",
            [
                {
                    "text": "R1 rezeksiyon (Mikroskobik rezidüel tümör pozitif); lokal nüks riski çok yüksektir ve kemoradyoterapi gerektirir.",
                    "isCorrect": True,
                    "explanation": "Mikroskobik sınır pozitifliği R1 olarak adlandırılır ve rezidüel tümör varlığını simgeler."
                },
                {
                    "text": "R0 rezeksiyon; tümör sınırda olsa dahi cerrahi başarılı kabul edilir.",
                    "isCorrect": False,
                    "explanation": "R0 sınırların tamamen negatif (temiz) olmasıdır; sınırda tümör varsa R1'dir."
                },
                {
                    "text": "R2 rezeksiyon; cerrahın gözle gördüğü masif tümör parçasını geride bırakması durumudur.",
                    "isCorrect": False,
                    "explanation": "R2 makroskobik rezidüel tümördür; histopatolojik mikroskobik tutulum R1'dir."
                }
            ]
        ),
        83: make_branching_logic(
            "55 yaşında günde 2 paket sigara ve düzenli yüksek miktarda alkol kullanan erkek hasta, 3 aydır devam eden ses kısıklığı ve yutma güçlüğü ile başvuruyor; laringoskopide vokal kordda ülsere kitle görülüyor.",
            "Bu etiyolojik arka planda gelişen laringeal neoplazmın en olası histopatolojik tipi ve biyolojik davranışı nedir?",
            [
                {
                    "text": "Skuamöz Hücreli Karsinom; tütün ve alkolün sinerjik etkisiyle solunum epitelindeki displazi üzerinden gelişir.",
                    "isCorrect": True,
                    "explanation": "Larinksin en sık malignitesi tütün ve alkolle doğrudan indüklenen skuamöz hücreli karsinomdur."
                },
                {
                    "text": "Vokal kord hemanjiyomu; vasküler selim bir lezyon olup alkolle ilişkisizdir.",
                    "isCorrect": False,
                    "explanation": "Ses kısıklığı ve ülsere infiltratif kitle tütün zemininde malign karsinom lehinedir."
                },
                {
                    "text": "Larinks rabdomyosarkomu; çocukluk çağı çizgili kas tümörüdür.",
                    "isCorrect": False,
                    "explanation": "Rabdomyosarkom erişkinde nadir olup sigara/alkol ile doğrudan ilişkili değildir."
                }
            ]
        ),
        91: make_branching_logic(
            "Yeni tanı konmuş bir glioblastoma hastasının tümör dokusu moleküler panelinde IDH1 gen mutasyonu ve MGMT promotor hipermetilasyonu araştırılıyor.",
            "Patoloğun bu moleküler belirteçleri raporlamasının nöroonkolojik hasta yönetimindeki temel amacı nedir?",
            [
                {
                    "text": "Tümörün moleküler alt tipini sınıflandırmak, prognozu öngörmek ve temozolomid alkilleyici kemoterapisine duyarlılığı belirlemek.",
                    "isCorrect": True,
                    "explanation": "MGMT metilasyonu DNA tamir enzimini susturarak temozolomid ilacına duyarlılığı ve sağkalımı belirgin artırır."
                },
                {
                    "text": "Hastada viral ensefalit etkeni olan Herpes simpleks virüsünü ekarte etmek.",
                    "isCorrect": False,
                    "explanation": "IDH1 ve MGMT glioma biyolojisi ve tedavisiyle ilgili onkolojik belirteçlerdir."
                },
                {
                    "text": "Glioblastomun benign bir astrositoma dönüşüp dönüşmeyeceğini izlemek.",
                    "isCorrect": False,
                    "explanation": "Glioblastoma en yüksek dereceli (Grade 4) primer beyin tümörüdür, selimleşmez."
                }
            ]
        ),
        95: make_branching_logic(
            "7 yaşındaki bir çocukta güneşe maruz kalan yüz ve kollarda yaygın lentigo, cilt atrofisi ve burnunda 0.8 cm boyutunda ülsere nodül saptanıyor; biyopside skuamöz hücreli karsinom tanısı konuyor.",
            "Bu yaşta beklenmeyen cilt karsinomunun etiyolojisinde araştırılması gereken temel genetik bozukluk nedir?",
            [
                {
                    "text": "Nükleotid eksizyon onarımı (NER) gen kusuruna bağlı Kseroderma Pigmentozum; UV timin dimerleri tamir edilemez.",
                    "isCorrect": True,
                    "explanation": "Çocuklukta güneş gören alanlarda karsinom gelişimi tipik olarak XP ve nükleotid eksizyon onarım yetmezliği kanıtıdır."
                },
                {
                    "text": "Ailesel polipozis koli (FAP) sendromu; APC gen mutasyonu araştırılmalıdır.",
                    "isCorrect": False,
                    "explanation": "FAP kolonda polipozis yapar, erken cilt karsinomu sendromu kseroderma pigmentozumdur."
                },
                {
                    "text": "Wilms tümörü sendromu; WT1 gen delesyonu araştırılmalıdır.",
                    "isCorrect": False,
                    "explanation": "WT1 böbrek tümörü (nefroblastom) yapar."
                }
            ]
        ),
        98: make_branching_logic(
            "Akciğer adenokarsinomu nedeniyle erlotinib (EGFR inhibitörü) tedavisi alan ve başlangıçta tam yanıt veren bir hastada 14 ay sonra primer kitlede büyüme ve yeni akciğer lezyonları gelişiyor.",
            "Tümörün klonal evrimi ve tedavi direnci mekanizması açısından patoloğun re-biyopside öncelikle araması gereken edinsel mutasyon nedir?",
            [
                {
                    "text": "EGFR ekzon 20'de T790M ikincil direnç mutasyonu; ilacın ATP bağlama cebine bağlanmasını sterik olarak engeller.",
                    "isCorrect": True,
                    "explanation": "EGFR TKI direncinin %50'den fazlasından T790M mutasyonu sorumludur; bu durumda üçüncü kuşak inhibitörlere (osimertinib) geçilir."
                },
                {
                    "text": "Hastada karsinomun selim bir hamartoma transdiferansiye olması.",
                    "isCorrect": False,
                    "explanation": "Kanserler selim dokuya transdiferansiye olmaz; dirençli agresif subklonlar ürer."
                },
                {
                    "text": "Erlotinibin karsinojene dönüşerek kitleyi büyütmesi.",
                    "isCorrect": False,
                    "explanation": "İlaç karsinojen değildir; klonal seleksiyonla dirençli mutant klon genişler."
                }
            ]
        )
    }

def get_extra_causal_chains():
    """Causal chain (patofizyolojik ve moleküler mekanizma zincirleri) ek ögeleri (17 adet)."""
    return {
        2: make_causal_chain(
            "Tümör Parankim ve Stroma Etkileşimi ile Anjiyogenez İndüksiyon Zinciri",
            [
                "1. Parankimal Hipoksi: Hızla prolifere olan tümör hücreleri oksijen difüzyon sınırını (100-200 mikron) aşar.",
                "2. HIF-1alfa Stabilizasyonu: Hipoksi ortamında prolil hidroksilazlar inaktive olur ve HIF-1alfa proteolizden kurtulur.",
                "3. VEGF ve bFGF Salınımı: Transkripsiyonel aktivasyonla parankim hücreleri çevre stromaya anjiyogenik faktörler salgılar.",
                "4. Endotel Aktivasyonu ve Filizlenme: Stromal kapiller endoteli bazal membranı eriterek tümöre doğru yeni damar tomurcukları uzatır.",
                "5. Düzensiz Vasküler Ağ Oluşumu: Perisit desteğinden yoksun, hiperpermeabl ve kıvrıntılı neoplastik kapiller yatak tamamlanır."
            ]
        ),
        5: make_causal_chain(
            "Rezidüel GTPaz Eksikliğinde RAS Onkogenik Sinyal Aktivasyon Zinciri",
            [
                "1. Nokta Mutasyonu: KRAS geninin 12, 13 veya 61. kodonlarında meydana gelen mutasyon GTP bağlanma cebini değiştirir.",
                "2. GAP İnaktivasyonu: GTPaz aktive edici proteinler (GAP) mutant RAS proteinine bağlanıp GTP'yi GDP'ye hidroliz edemez.",
                "3. Sürekli GTP Bağlı Kalma: RAS proteini hücre zarında kesintisiz aktif konformasyonda kilitli kalır.",
                "4. Kaskad Uyarımı: Sitoplazmik RAF/MEK/ERK mitojenik kinaz yolağı otonom olarak fosforillenir.",
                "5. Nükleer Transkripsiyon: MYC ve Siklin D genleri tetiklenerek kontrolsüz hücre bölünmesi başlatılır."
            ]
        ),
        6: make_causal_chain(
            "Retinoblastom (RB) Proteini Aracılı G1-S Hücre Döngüsü Kontrol Zinciri",
            [
                "1. Hipofosforile Dinlenme Evresi: Erken G1 fazında RB proteini hipofosforiledir ve E2F transkripsiyon faktörünü sıkıca hapseder.",
                "2. Mitojenik Sinyal ve CDK Aktivasyonu: Büyüme faktörleri Siklin D/CDK4-6 kompleksini aktifleştirir.",
                "3. İlerleyici RB Hiperfosforilasyonu: CDK enzimleri RB üzerindeki serin rezidülerini yoğun biçimde fosforiller.",
                "4. E2F Transkripsiyon Faktörünün Serbest Kalması: Konformasyonu değişen RB, E2F proteinini serbest bırakır.",
                "5. S Fazına Giriş: Serbest E2F, DNA polimeraz ve Siklin E genlerini uyararak hücreyi geri dönüşsüz replikasyon fazına geçirir."
            ]
        ),
        12: make_causal_chain(
            "Benign Tümörlerde Fibröz Kapsül Oluşumu ve İtici Büyüme Mekanizması",
            [
                "1. Yavaş ve Simetrik Proliferasyon: Benign parankimal hücreler homojen ve düşük hızda klonal olarak çoğalır.",
                "2. Çevre Dokuya Bası: Genişleyen kitle komşu normal stroma ve parankimi dışa doğru mekanik olarak iter.",
                "3. Doku Atrofisi ve Kolajen Kondansasyonu: Bası altındaki komşu konak bağ dokusu sıkışır ve fibroblastlar uyarılır.",
                "4. Fibröz Kapsül Gelişimi: Kitle etrafında çevre dokudan ayıran muntazam kollajenöz bir kılıf organize olur.",
                "5. Cerrahi Enükleasyon Kolaylığı: Kapsül kitlenin çevreye sızmasını engelleyerek cerrahın kitleyi kabuğuyla soymasını sağlar."
            ]
        ),
        15: make_causal_chain(
            "Malign Epitelyal Hücrelerde Anaplazi ve Dediferansiyasyon Gelişim Zinciri",
            [
                "1. Genomik Kaos: DNA onarım bozuklukları ve mutasyonel birikimler epigenetik kontrol ağlarını bozar.",
                "2. Morfolojik Polarite Kaybı: Epitel hücrelerinin bazal ve apikal yüzey ayrımı ve kadrilateral dizilimi silinir.",
                "3. Nükleer Hiperkromazi ve Büyüme: DNA içeriği katlandıkça nükleuslar irileşir, boyanma koyulaşır ve N/C oranı 1:1'e yaklaşır.",
                "4. Dev Hücre ve Tripolar Mitoz: İğ ipliği anomalileri sonucu atipik çok kutuplu mitotik figürler ve tümör dev hücreleri belirir.",
                "5. Tam Fonksiyonel Anaplazi: Transforme hücreler köken aldıkları dokunun keratin veya müsin gibi tüm özgül salgılarını terk eder."
            ]
        ),
        22: make_causal_chain(
            "Epitelyal Displaziden İnvaziv Karsinoma İlerleme (CIN/SIL Modeli) Kaskadı",
            [
                "1. Bazal Polarite Bozukluğu (Hafif Displazi): Atipik hücreler epitel tabakasının alt 1/3'lük kısmına sınırlı kalır.",
                "2. Katman Tutulumunun İlerlemesi (Orta Displazi): Nükleer atipi ve mitotik figürler epitelin 2/3 kalınlığına yayılır.",
                "3. Karsinoma İn Situ (Şiddetli Displazi): Epitelin tam katında atipi mevcuttur ancak bazal membran tamamen intakttır.",
                "4. Kolajenaz ve MMP Aktivasyonu: Atipik hücreler Matriks Metalloproteinaz (MMP-2, MMP-9) salgılamaya başlar.",
                "5. İnvaziv Karsinom Başlangıcı: Bazal membranın Tip IV kolajeni parçalanır ve tümör hücreleri stroma içine penetre olur."
            ]
        ),
        32: make_causal_chain(
            "Karsinom vs Sarkom Yayılım Yolu Ayrımının Patogenetik Mekanizması",
            [
                "1. Histogenetik Çıkış Farkı: Karsinomlar lenfatik damarlardan zengin epitelyal yüzeylerden, sarkomlar vasküler mezenşimden çıkar.",
                "2. Lenfatik Kılcal Girişi: Karsinom hücreleri gevşek bağlantılı lenfatik endotel aralıklarından lümene kolayca sızar.",
                "3. Sentinel Lenf Nodu Filtresi: Lenfatik akım tümör hücrelerini bölgesel lenf ganglionunun subkapsüler sinüsüne taşır.",
                "4. Sarkomlarda Venöz İnvazyon: Mezenkimal maligniteler zengin venöz damar duvarlarını delerek sistemik kana karışır.",
                "5. Hedef Organ Filtresi: Hematojen metastaz kaval drenajla akciğer kapiller yatağında takılarak kolonize olur."
            ]
        ),
        35: make_causal_chain(
            "Epitelyal-Mezenkimal Transdiferansiyasyon (EMT) Moleküler Kaskadı",
            [
                "1. Snail ve Twist Transkripsiyonu: Tümör mikroçevresindeki TGF-beta ve hipoksi sinyalleri EMT transkripsiyon faktörlerini aktive eder.",
                "2. E-Kaderin Baskılanması: Hücrelerarası yapıştırıcı kalsiyum bağımlı E-kaderin gen ekspresyonu tamamen durdurulur.",
                "3. N-Kaderin ve Vimentin Açılımı: Kanser hücresi mezenkimal adezyon molekülleri ve ara filamanlar sentezlemeye başlar.",
                "4. İğsi Motil Fenotip Kazanımı: Epitelyal kohezyonunu kaybeden hücre fuziform mekik şekline bürünerek motilite kazanır.",
                "5. Bazal Membran Delinmesi: Hücre tek tek amoboid hareketlerle ekstraselüler matriksi parçalayıp stromaya dalar."
            ]
        ),
        42: make_causal_chain(
            "Teratom Histogenezinde Totipotent Germ Hücre Farklılaşma Zinciri",
            [
                "1. Primordiyal Germ Hücresi Ayrışımı: Gonadlara veya orta hat kordona göç eden totipotent kök hücrede neoplastik dönüşüm başlar.",
                "2. Çok Yönlü Diferansiyasyon: Hücre tüm embriyonik germ tabakalarına (ektoderm, mezoderm, endoderm) farklılaşma yeteneğini korur.",
                "3. Doku Adacıkları Organizasyonu: Tümör içinde kıl folikülleri, diş, solunum epiteli, kıkırdak ve tiroid dokuları bir arada gelişir.",
                "4. Matür Teratom Formasyonu: Bütün dokular tamamen olgunlaşırsa kistik benign yapı (dermoid kist) ortaya çıkar.",
                "5. İmmatür Blastik Gelişim: Nöroepitelyal veya mezenkimal dokuların blastik kalması durumunda yüksek malignite potansiyeli doğar."
            ]
        ),
        52: make_causal_chain(
            "TP53 Aracılı Hücre Döngüsü Durdurma ve Apoptoz Karar Zinciri",
            [
                "1. DNA Çift İplik Hasarı: Radyasyon veya kemoterapötikler genomda çift iplik kırıkları meydana getirir.",
                "2. ATM/ATR Kinaz Aktivasyonu: Hasar sensör kinazları p53 proteinini fosforilleyerek MDM2 yıkımından korur.",
                "3. p21 (CDKN1A) İndüksiyonu: Kararlı p53, CDK inhibitörü p21'i transkribe ederek hücreyi G1-S fazında kilitler.",
                "4. Tamir Denemesi: Hasar düzeltilebilirse p53 düzeyi düşer ve hücre döngüsüne kaldığı yerden devam eder.",
                "5. Geri Dönüşsüz Apoptoz: Hasar tamir sınırını aşarsa p53 BAX ve PUMA genlerini tetikleyerek mitokondriyal apoptozu başlatır."
            ]
        ),
        62: make_causal_chain(
            "Ekstraselüler Matriks İnvazyonu ve Metalloproteinaz Yıkım Kaskadı",
            [
                "1. Adezyon Gevşemesi: Kanser hücreleri E-kaderin kaybıyla birbirinden koparak bağımsız amoboid hücrelere dönüşür.",
                "2. Matriks Reseptör Ligasyonu: Tümör yüzey integrinleri bazal membranın laminin ve fibronektin proteinlerine kenetlenir.",
                "3. Proteolitik Enzim Salınımı: Tümör ve reaktif stroma MMP-2, MMP-9 ve katepsin enzimlerini çevreye boşaltır.",
                "4. Bazal Membran Çözünmesi: Tip IV kolajen ve laminin ağı enzimatik sindirimle delinerek bir geçit açılır.",
                "5. Stromal Göç: Tümör kökenli otokrin motilite faktörleri kılavuzluğunda hücreler stromal bağ dokusuna doğru yürür."
            ]
        ),
        65: make_causal_chain(
            "Tümörün İntravazasyon ve Dolaşımda Sağkalım Kaskadı",
            [
                "1. Damar Duvarı Delinmesi: Stromaya sızan motil neoplastik hücreler kapiller endotel bazal membranını parçalar.",
                "2. İntravazasyon: Hücreler endotel aralıklarından vasküler veya lenfatik lümen içine sıkışarak giriş yapar.",
                "3. Trombosit Zırhlanması: Dolaşımdaki kanser hücresi trombositleri aktive ederek etrafında mikrotrombüs zırhı örer.",
                "4. İmmün Kaçış ve Makaslama Koruması: Trombosit kalkanı tümörü NK hücrelerinin sitotoksik lizisinden ve damar türbülansından korur.",
                "5. Kapiller Yatakta Tutunma: Korunan tümör embolisi hedef organın ilk mikrosirkülasyon endoteline integrinlerle yapışır."
            ]
        ),
        72: make_causal_chain(
            "Sentinel Lenf Nodu Tutulumu ve Aksiller Yayılım Kaskadı",
            [
                "1. Primer Odakta Lenfatik Emboli: Meme dokusundaki invaziv karsinom stromadaki lenf kapillerlerine dalar.",
                "2. Afferent Drenaj Akımı: Lenf sıvısı tümör hücrelerini anatomik ilk durak olan bekçi (sentinel) lenf noduna taşır.",
                "3. Subkapsüler Sinüs Kolonizasyonu: Hücreler sentinel nodun marjinal sinüsüne takılır, ekstravaze olur ve çoğalmaya başlar.",
                "4. Gangliyonik Mimari Silinmesi: Büyüyen metastatik kitle sentinel nodun lenfoid foliküllerini yıkar ve kapsülü deler.",
                "5. İkinci ve Üçüncü Düzey Yayılım: Taşma sonucu tümör efferent lenfatiklerle aksillanın üst grup derin nodlarına ilerler."
            ]
        ),
        75: make_causal_chain(
            "Gastrointestinal Sistem Kanserlerinde Portal Venöz Karaciğer Metastaz Zinciri",
            [
                "1. Kolon Submukozal Ven İnvazyonu: Karsinom glandları mezenterik venöz dalların lümenine penetre olur.",
                "2. Portal Ven Akımı: Neoplastik emboliler superior veya inferior mezenterik ven üzerinden ana portal vene akar.",
                "3. Karaciğer Sinüzoidlerine Takılma: Portal kan karaciğer mikrosirkülasyonuna girince dar sinüzoidlerde tümör hücreleri sıkışır.",
                "4. Karaciğer Mikroçevresine Adaptasyon: Tümör hücreleri hepatik stellat hücreleri ve sinüzoid endotelini aktive ederek ekstravaze olur.",
                "5. Metastatik Odak Genişlemesi: Portal triad çevresinde multipl metastatik kitleler büyüyerek karaciğer parankimini harap eder."
            ]
        ),
        82: make_causal_chain(
            "Kimyasal Karsinogenezde İnisiyasyon ve Promosyon İşbirliği Zinciri",
            [
                "1. Prokarsinojen Alımı: Vücuda alınan inert kimyasal ajan (ör. polisiklik aromatik hidrokarbon) kana karışır.",
                "2. Hepatik P450 Metabolizması: Karaciğer monooksijenazları prokarsinojeni yüksek derecede elektrofilik nihai karsinojene çevirir.",
                "3. DNA Aduk Oluşumu (İnisiyasyon): Reaktif molekül guanin bazlarına kovalent bağlanarak genomda kalıcı hasar yaratır.",
                "4. Promotör Maruziyeti (Promosyon): Mutajen olmayan mitojenik ajanlar (hormon, forbol esteri) inisiye hücreyi bölünmeye zorlar.",
                "5. Malign Progresyon: Çoğalan hücreler ek somatik mutasyonlar biriktirerek otonom karsinoma evrilir."
            ]
        ),
        92: make_causal_chain(
            "Mikrosatellit İnstabilitesi (MSI) ve Lynch Karsinogenez Kaskadı",
            [
                "1. Kalıtsal Germline Mutasyon: Birey MSH2 veya MLH1 geninde tek mutant alelle dünyaya gelir.",
                "2. İkinci Alelin Yitimi: Kolon epitelyal kök hücresinde somatik mutasyonla sağlam ikinci alel inaktive olur (Knudson 2. vuruş).",
                "3. Eşleşme Kaçaklarının Birikmesi: MMR kompleksi felç olunca replikasyon sırasındaki baz kaymaları tamir edilemez.",
                "4. Mikrosatellitlerde Boy Değişimi: Genomdaki tekrarlayan oligonükleotid dizilerinde yaygın delesyon ve insersiyonlar oluşur (MSI-H).",
                "5. Kodlayıcı Bölge Sürücü Mutasyonları: TGF-beta Reseptör II ve BAX gibi genlerin mikrosatellitleri bozularak invaziv kanser patlak verir."
            ]
        ),
        97: make_causal_chain(
            "BRCA1 Kusuru ve PARP İnhibitörü Sentetik Letalite Mekanizması",
            [
                "1. Kalıtsal Homolog Rekombinasyon Kusuru: Kanser hücresi mutant BRCA1 nedeniyle çift iplik DNA kırıklarını tamir edemez.",
                "2. PARP İle Tek İplik Tamiri: Hücre tek iplik lezyonlarını onararak hayatta kalmak için PARP enzimine bağımlı hale gelir.",
                "3. Terapötik PARP Blokajı: PARP inhibitörü ilaç (olaparib) enzimi kovalent olarak DNA üzerine kilitler.",
                "4. Çift İplik Kırıklarına Çöküş: İlerleyen replikasyon çatalı bloke PARP lezyonlarına çarparak çift iplik kırıklarına dönüşür.",
                "5. Sentetik Letalite ve Apoptoz: Çift iplik kırıklarını tamir edecek BRCA sistemi de bulunmadığından kanser hücresi seçici olarak ölür."
            ]
        )
    }

def get_extra_micro_quizzes():
    """Micro quiz (ayrıntılı şık açıklamalı sorular) ek ögeleri (10 adet)."""
    return {
        4: make_micro_quiz(
            "Kanser hücrelerinin normal oksijen varlığında dahi glukozu oksidatif fosforilasyon yerine laktata yıkması ve biyosentetik ara ürünler üretmesi olayına ne ad verilir?",
            [
                {
                    "key": "A",
                    "text": "Warburg etkisi (aerobik glikoliz)",
                    "isCorrect": True,
                    "explanation": "Warburg etkisi, tümör hücrelerinin bol oksijende dahi glukozu laktata çevirerek hızlı hücre bölünmesi için nükleik asit, lipid ve protein yapıtaşları üretmesidir."
                },
                {
                    "key": "B",
                    "text": "Pasteur etkisi",
                    "isCorrect": False,
                    "explanation": "Pasteur etkisi oksijen varlığında glikolizin baskılanmasıdır; Warburg etkisi ise oksijen varken bile glikolizin sürmesidir."
                },
                {
                    "key": "C",
                    "text": "Cori döngüsü",
                    "isCorrect": False,
                    "explanation": "Cori döngüsü kas ile karaciğer arasındaki laktat ve glukoz dönüşüm metabolizmasıdır."
                },
                {
                    "key": "D",
                    "text": "Krebs döngüsü arresti",
                    "isCorrect": False,
                    "explanation": "Kanser hücresinde Krebs döngüsü tamamen durmaz, anaplerotik ara maddeler sağlar."
                }
            ],
            "Warburg etkisi PET taramasında 18-FDG tutulumunun temel biyokimyasal mekanizmasıdır."
        ),
        14: make_micro_quiz(
            "Benign ve malign neoplazmların ayırıcı tanısında patolojik incelemede malignitenin tartışmasız en kesin kanıtı olan kriter aşağıdakilerden hangisidir?",
            [
                {
                    "key": "A",
                    "text": "Tümör kitlesinin 5 santimetreden daha büyük çapa ulaşması",
                    "isCorrect": False,
                    "explanation": "Kitle boyutu tek başına malignite kanıtı olamaz; benign leiyomiyomlar 20 cm boyuta ulaşabilir."
                },
                {
                    "key": "B",
                    "text": "Uzak doku veya organlara metastaz yapmış olması",
                    "isCorrect": True,
                    "explanation": "Metastaz varlığı lezyonun tartışmasız ve kesin olarak malign olduğunu ispatlar; benign tümörler asla metastaz yapmaz."
                },
                {
                    "key": "C",
                    "text": "Histopatolojik kesitlerde distrofik kalsifikasyon bulunması",
                    "isCorrect": False,
                    "explanation": "Kalsifikasyon hem benign (menenjiom, leiyomiyom) hem de malign lezyonlarda görülebilir."
                },
                {
                    "key": "D",
                    "text": "Tümör parankimi içerisinde vasküler damarlanmanın zengin olması",
                    "isCorrect": False,
                    "explanation": "Zengin damarlanma benign anjiyomlarda da mevcuttur."
                }
            ],
            "Metastaz malignitenin tartışılamaz yegane biyolojik kanıtıdır."
        ),
        24: make_micro_quiz(
            "Aşağıdaki epitelyal neoplazmlardan hangisi mikroskopik veya makroskopik olarak parmak benzeri parankimal çıkıntılar ve fibrovasküler kor ile karakterizedir?",
            [
                {
                    "key": "A",
                    "text": "Papillom",
                    "isCorrect": True,
                    "explanation": "Papillomlar, epitelyal yüzeylerden parmak benzeri (papiller) projeksiyonlar oluşturan ve ortasında fibrovasküler stroma içeren benign neoplazmlardır."
                },
                {
                    "key": "B",
                    "text": "Kistadenom",
                    "isCorrect": False,
                    "explanation": "Kistadenom geniş kistik boşluklar oluşturan glandüler tümördür."
                },
                {
                    "key": "C",
                    "text": "Adenom",
                    "isCorrect": False,
                    "explanation": "Adenom bez epiteli oluşturan veya bezlerden köken alan selim tümördür; papiller mimari şart değildir."
                },
                {
                    "key": "D",
                    "text": "Karsinom",
                    "isCorrect": False,
                    "explanation": "Karsinom malign epitel tümörlerinin genel adıdır."
                }
            ],
            "Papiller yapılar santral fibrovasküler bir eksen etrafında organize olur."
        ),
        34: make_micro_quiz(
            "Mezenkimal kaynaklı malign neoplazmlar adlandırılırken köken aldıkları doku isminin sonuna hangi takı getirilir?",
            [
                {
                    "key": "A",
                    "text": "-om (-oma)",
                    "isCorrect": False,
                    "explanation": "-om takısı kural olarak benign neoplazmlar için kullanılır (lipom, kondrom)."
                },
                {
                    "key": "B",
                    "text": "-karsinom (-carcinoma)",
                    "isCorrect": False,
                    "explanation": "-karsinom takısı epitelyal kaynaklı malign neoplazmlar için kullanılır."
                },
                {
                    "key": "C",
                    "text": "-sarkom (-sarcoma)",
                    "isCorrect": True,
                    "explanation": "Mezenkimal bağ dokusu kökenli malign neoplazmlar köken aldıkları dokunun sonuna -sarkom takısı alırlar (osteosarkom, liposarkom)."
                },
                {
                    "key": "D",
                    "text": "-blastom (-blastoma)",
                    "isCorrect": False,
                    "explanation": "-blastom primitif embriyonik doku tümörleri için kullanılır."
                }
            ],
            "Mezenkimal maligniteler sarkom, epitelyal maligniteler karsinom adını alır."
        ),
        45: make_micro_quiz(
            "Geliştiği organa ait yerli doku elemanlarının matür ancak tamamen düzensiz ve kaotik bir mimaride kitle oluşturmasına ne ad verilir?",
            [
                {
                    "key": "A",
                    "text": "Hamartom",
                    "isCorrect": True,
                    "explanation": "Hamartom, o organın doğal yapıtaşlarının matür fakat mimari olarak kaotik bir kitle oluşturmasıdır (ör. akciğer kondroid hamartomu)."
                },
                {
                    "key": "B",
                    "text": "Koristom",
                    "isCorrect": False,
                    "explanation": "Koristom yabancı bir dokunun başka organda bulunmasıdır (ektopi/heterotopi)."
                },
                {
                    "key": "C",
                    "text": "Teratom",
                    "isCorrect": False,
                    "explanation": "Teratom üç germ yaprağı türevi içeren gerçek bir neoplazmdır."
                },
                {
                    "key": "D",
                    "text": "Metaplazi",
                    "isCorrect": False,
                    "explanation": "Metaplazi bir olgun hücre tipinin başka bir olgun hücre tipine dönüşmesidir."
                }
            ],
            "Hamartom yerli doku kaosu, koristom yabancı doku ektopisidir."
        ),
        55: make_micro_quiz(
            "Mikroskopik incelemede atipik mitotik figürler (tripolar, tetrapolar iğ iplikleri) görülmesi aşağıdakilerden hangisinin en güçlü göstergesidir?",
            [
                {
                    "key": "A",
                    "text": "Malign neoplastik dönüşüm ve anaplazi",
                    "isCorrect": True,
                    "explanation": "Bipolar simetrik mitozlar normal dokularda da görülebilirken; tripolar, tetrapolar veya asimetrik atipik mitozlar malignitenin ve anaplazinin patognomonik bulgularıdır."
                },
                {
                    "key": "B",
                    "text": "Fizyolojik doku rejenerasyonu",
                    "isCorrect": False,
                    "explanation": "Fizyolojik rejenerasyonda sadece normal bipolar mitotik figürler izlenir."
                },
                {
                    "key": "C",
                    "text": "Benign hiperplazi",
                    "isCorrect": False,
                    "explanation": "Hiperplazide mitotik iğ ipliği düzeni kesinlikle bipolar ve simetriktir."
                },
                {
                    "key": "D",
                    "text": "Hücresel senesens ve yaşlanma",
                    "isCorrect": False,
                    "explanation": "Senesenste hücre bölünmesi tamamen durur, mitotik figür görülmez."
                }
            ],
            "Atipik çok kutuplu mitozlar malignite için son derece spesifiktir."
        ),
        67: make_micro_quiz(
            "Tümörlerin histopatolojik derecelendirmesi (grade) ile klinik evrelemesi (stage) arasındaki temel fark nedir?",
            [
                {
                    "key": "A",
                    "text": "Grade diferansiyasyon ve sitolojik atipiyi ölçerken; Stage tümörün anatomik yayılım derecesini ve büyüklüğünü ölçer.",
                    "isCorrect": True,
                    "explanation": "Derecelendirme (Grade) mikroskopik diferansiyasyon ve anaplazi derecesidir; Evreleme (Stage/TNM) tümörün vücuttaki anatomik yayılım boyutudur ve klinik prognoza daha güçlü yön verir."
                },
                {
                    "key": "B",
                    "text": "Grade cerrah tarafından ameliyatta belirlenir, Stage ise sadece patolog tarafından mikroskopta saptanır.",
                    "isCorrect": False,
                    "explanation": "Tam tersine, Grade mikroskobik inceleme ile patolog tarafından, Stage ise radyolojik ve klinik yayılım ile belirlenir."
                },
                {
                    "key": "C",
                    "text": "Grade sadece benign tümörler için, Stage ise sadece malign tümörler için kullanılır.",
                    "isCorrect": False,
                    "explanation": "Grade ve stage malign neoplazmların klinik-patolojik değerlendirme araçlarıdır."
                },
                {
                    "key": "D",
                    "text": "Stage ile grade eş anlamlı kavramlar olup aynı parametreyi ifade ederler.",
                    "isCorrect": False,
                    "explanation": "Biri hücresel diferansiyasyon (grade), diğeri anatomik yayılım (stage) göstergesidir."
                }
            ],
            "Evre (stage) prognoz tayininde ve tedavi planlamasında daima dereceden (grade) daha belirleyicidir."
        ),
        77: make_micro_quiz(
            "Over karsinomunun periton boşluğu boyunca yayılarak omentum ve serozal yüzeylerde multipl tümör nodülleri oluşturması hangi metastaz şeklidir?",
            [
                {
                    "key": "A",
                    "text": "Transsölomik (Vücut boşluklarına tohumlanma)",
                    "isCorrect": True,
                    "explanation": "Tümörün doğal bir vücut boşluğuna (periton, plevra, perikard) dökülerek yüzeyler boyu ekilmesine transsölomik tohumlanma denir."
                },
                {
                    "key": "B",
                    "text": "Hematojen metastaz",
                    "isCorrect": False,
                    "explanation": "Hematojen metastaz venöz veya arteriyel damarlar yoluyla uzak organ parankimine yayılımdır."
                },
                {
                    "key": "C",
                    "text": "Lenfatik permeasyon",
                    "isCorrect": False,
                    "explanation": "Lenfatik yayılım lenf nodları ve damarları aracılığıyla gerçekleşir."
                },
                {
                    "key": "D",
                    "text": "İyatrojenik implantasyon",
                    "isCorrect": False,
                    "explanation": "Cerrahi aletlerle bulaşma iyatrojeniktir; periton yayılımı doğal transsölomik yoldur."
                }
            ],
            "Over kanseri periton karsinomatozisinin prototipik örneğidir."
        ),
        84: make_micro_quiz(
            "Boya, kauçuk ve petrol endüstrisinde benzen maruziyeti olan işçilerde kemik iliği toksisitesi sonucu en sık gelişen hematolojik malignite nedir?",
            [
                {
                    "key": "A",
                    "text": "Akut miyeloid lösemi (AML)",
                    "isCorrect": True,
                    "explanation": "Benzen kemik iliği kök hücrelerini hasarlayarak pansitopeni, aplastik anemi ve özellikle akut miyeloid lösemiye (AML) yol açar."
                },
                {
                    "key": "B",
                    "text": "Kronik lenfositik lösemi (KLL)",
                    "isCorrect": False,
                    "explanation": "KLL yaşlılık dönemi B hücreli malignitesi olup benzen ile spesifik ilişkisi yoktur."
                },
                {
                    "key": "C",
                    "text": "Hodgkin lenfoma",
                    "isCorrect": False,
                    "explanation": "Hodgkin lenfoma EBV ve immün faktörlerle ilişkilidir."
                },
                {
                    "key": "D",
                    "text": "Multipl miyelom",
                    "isCorrect": False,
                    "explanation": "Plazma hücre malignitesidir, benzenin klasik mesleki hedefi AML'dir."
                }
            ],
            "Benzen maruziyeti AML gelişiminde patognomonik mesleki karsinojendir."
        ),
        96: make_micro_quiz(
            "Knudson'ın iki vuruş (two-hit) hipotezine göre kalıtsal retinoblastom hastalarında tümör gelişimi için gereken genetik mekanizma nedir?",
            [
                {
                    "key": "A",
                    "text": "Birinci mutant alel germline kalıtılır; ikinci alel somatik olarak inaktive olduğunda tümör ortaya çıkar.",
                    "isCorrect": True,
                    "explanation": "Kalıtsal vakalarda birinci darbe anne/babadan tüm hücrelere aktarılır; hedef retinal hücrede ikinci darbe (LOH) vurunca kontrol kalkar."
                },
                {
                    "key": "B",
                    "text": "Her iki mutant alelin de anne ve babadan aynı anda sağlam aktarılması gerekir.",
                    "isCorrect": False,
                    "explanation": "Kalıtım otozomal dominanttır; birey heterozigot doğar, ikinci mutasyon somatiktir."
                },
                {
                    "key": "C",
                    "text": "RB1 geninin aşırı amplifiye olarak onkogene dönüşmesi gerekir.",
                    "isCorrect": False,
                    "explanation": "RB1 bir onkogen değil, tümör baskılayıcı gendir; işlev kaybı ile inaktive olur."
                },
                {
                    "key": "D",
                    "text": "Tümör gelişimi için sadece viral bir enfeksiyonun eklenmesi yeterlidir.",
                    "isCorrect": False,
                    "explanation": "İki vuruş hipotezi genetik alel kayıplarını açıklar."
                }
            ],
            "Tümör baskılayıcı genler Knudson iki vuruş modeline göre resesif davranır."
        )
    }

def get_extra_before_afters():
    """Before after slider ek ögeleri (3 adet)."""
    return {
        18: make_before_after(
            "Benign Leiomyom vs Malign Leiomyosarkom Morfolojik Dönüşümü",
            "Benign Uterin Leiomyom",
            "Muntazam sınırlı, homojen girdap paterni, atipisiz üniform iğsi düz kas hücreleri, sıfır veya çok ender mitoz.",
            "Malign Uterin Leiomyosarkom",
            "İnfiltratif kanamalı nekrotik kitle, nükleer pleomorfizm, atipik dev hücreler ve yüksek mitotik indeks (>10/10 BBA).",
            "Leiomyom ve leiomyosarkom ayrımı ameliyatın kapsamını ve hastanın sağkalımını doğrudan belirler."
        ),
        58: make_before_after(
            "İyi Diferansiye Skuamöz Karsinom vs Anaplastik Karsinom",
            "İyi Diferansiye Skuamöz Hücreli Karsinom",
            "Konsantrik keratin incileri (horn pearls), belirgin hücrelerarası dikenli köprüler ve nükleer polarite kalıntıları.",
            "Az Diferansiye / Anaplastik Karsinom",
            "Keratinden tamamen yoksun, polaritesiz tabakalar, dev pleomorfik nükleuslar ve atipik tripolar mitozlar.",
            "Diferansiyasyon derecesi tümörün grade'ini ve radyoterapiye yanıt duyarlılığını doğrudan etkiler."
        ),
        78: make_before_after(
            "Lokal Karsinom İnvazyonu vs Uzak Hematojen Metastaz",
            "Lokal İnvazyon Evresi (T3)",
            "Tümör primer organ sınırlarını ve bazal membranı aşarak komşu yağ ve kas dokularına infiltratif uzanır.",
            "Uzak Metastaz Evresi (M1)",
            "Tümör hücreleri damar yoluyla akciğer, karaciğer veya kemiğe ulaşıp primer kitleyle bağımsız koloniler kurar.",
            "Lokal invazyon cerrahiyle temizlenebilirken, uzak metastaz sistemik tedavi gerektiren evre 4 durumudur."
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
