#!/usr/bin/env python3
"""Comprehensive Enrichment Elements Generator for k1-08 Deck (Hücresel Yaşlanma)"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_08_deck_data.helpers import (
    make_micro_quiz, make_branching_logic, make_causal_chain,
    make_before_after, make_table
)

def get_extra_quizzes():
    """Ekstra mikro soru envanteri (k1-08)"""
    return {
        6: make_micro_quiz(
            "Replikatif senesense giren somatik insan hücrelerinde hücre döngüsünün G1/S fazında kalıcı olarak durmasını sağlayan temel siklin bağımlı kinaz inhibitörleri hangileridir?",
            {"A": "p16INK4a ve p21CIP1/WAF1", "B": "p53 ve Rb defosforilasyonu", "C": "Siklin D ve CDK4 kompleksi", "D": "MDM2 ve E2F serbestleşmesi", "E": "ATM ve ATR kinaz inaktivasyonu"},
            "A",
            {
                "A": "Doğru cevap A'dır: DNA hasarı p53 aracılığıyla p21'i uyarırken, telomer erozyonu ve hücresel stres p16INK4a ekspresyonunu artırarak CDK4/6'yı inhibe eder ve hücre döngüsünü G1'de kalıcı durdurur.",
                "B": "p53 transkripsiyon faktörüdür ve Rb fosforilasyon durumunu doğrudan inhibe etmez, kinaz inhibitörleri aracılığıyla düzenler.",
                "C": "Siklin D/CDK4 kompleksi döngüyü ilerleten komplekstir, durduran inhibitör değildir.",
                "D": "MDM2 p53'ü yıkar, serbest E2F ise S fazına geçişi tetikler.",
                "E": "ATM ve ATR DNA hasarında inaktive olmaz, aksine fosforilasyon kaskadını başlatarak aktive olur."
            }
        ),
        16: make_micro_quiz(
            "Hutchinson-Gilford Progeria Sendromunda lamin A genindeki (LMNA) sessiz nokta mutasyonu sonucu ortaya çıkan anormal protein hangisidir?",
            {"A": "WRN Helikaz", "B": "Progerin", "C": "Shelterin", "D": "Sirtuin 1", "E": "Ubikitin Ligaz"},
            "B",
            {
                "A": "WRN proteini erişkin tipi erken yaşlanma olan Werner sendromunda defektiftir.",
                "B": "Doğru cevap B'dir: LMNA genindeki c.1824C>T mutasyonu hatalı bir kırpılma alanı yaratarak farnesil grubunu kaybedemeyen toksik 'progerin' proteininin üretilmesine ve nükleer zar anomalilerine yol açar.",
                "C": "Shelterin telomer uçlarını koruyan altı proteinli komplekstir.",
                "D": "Sirtuin 1 NAD+ bağımlı deasetilaz olup ömrü uzatıcı etki gösterir.",
                "E": "Ubikitin ligaz protein yıkım sisteminde yer alır."
            }
        ),
        26: make_micro_quiz(
            "Telomerik DNA'nın 3' tek zincirli çıkıntısını bir düğüm gibi nükleazlardan ve DNA onarım enzimlerinden saklayan özel ilmek yapısı hangisidir?",
            {"A": "Holliday kavşağı", "B": "D-loop / T-loop yapısı", "C": "Okazaki halkası", "D": "Kinetokor kıvrımı", "E": "Nükleozom çekirdeği"},
            "B",
            {
                "A": "Holliday kavşağı homolog rekombinasyon ara ürünüdür.",
                "B": "Doğru cevap B'dir: Telomerik 3' sarkan uç çift zincirli DNA içerisine sokularak D-loop ve T-loop (telomeric loop) yapısını oluşturur; bu sayede çift zincir kırığı olarak algılanmaktan korunur.",
                "C": "Okazaki parçacıkları kesintili DNA replikasyonunda oluşur.",
                "D": "Kinetokor iğ ipliklerinin bağlandığı sentromerik komplekstir.",
                "E": "Nükleozom histon oktameri etrafına sarılı DNA birimidir."
            }
        ),
        36: make_micro_quiz(
            "Kritik telomer erozyonuna uğrayan ancak p53 ve pRb kontrol noktaları inaktive olmuş pre-kanseröz hücrelerde gözlenen 'Bridge-Fusion-Breakage' (BFB) döngüsünün temel patogenetik sonucu nedir?",
            {"A": "Mitotik kriz, yaygın kromozomal translokasyonlar ve anöploidi", "B": "Anında kaspaz bağımlı kontrollü apoptoz", "C": "G0 fazında kalıcı hücre döngüsü arresti", "D": "Eksojen telomeraz aşırı salgılanması", "E": "Hücre çekirdeğinin lizozomal fagositozu"},
            "A",
            {
                "A": "Doğru cevap A'dır: p53 kontrolü yokluğunda çıplak telomer uçları uç-uca birleşir (disentrik kromozomlar), anafazda köprü oluşturur ve parçalanarak masif genomik kararsızlığa, kriz evresine ve kanserojenik translokasyonlara yol açar.",
                "B": "p53 inaktif olduğu için fizyolojik apoptoz kaskadı tetiklenemez.",
                "C": "Kalıcı arrest olsaydı senesense girerdi, oysa p53/pRb kaybı bölünmeyi sürdürür.",
                "D": "Telomeraz salgılanması hücre içi enzimatik reaktivasyondur, eksojen salgı değildir.",
                "E": "Nükleofaji krizin temel nedeni değil geç evre sekonder fenomendir."
            }
        ),
        46: make_micro_quiz(
            "Mitokondriyal iç zarda elektron transport zincirinden kaçan tek elektronların moleküler oksijeni kısmen indirgemesiyle oluşan primer Reaktif Oksijen Türü (ROS) hangisidir?",
            {"A": "Hidroksil radikali (OH·)", "B": "Süperoksit anyonu (O2·-)", "C": "Hidrojen peroksit (H2O2)", "D": "Peroksinitrit (ONOO-)", "E": "Hipokloröz asit (HOCl)"},
            "B",
            {
                "A": "Hidroksil radikali Fenton reaksiyonuyla hidrojen peroksitten üretilen en reaktif sekonder türevdir.",
                "B": "Doğru cevap B'dir: Kompleks I ve Kompleks III'ten sızan elektronların O2 ile doğrudan reaksiyona girmesiyle öncelikle süperoksit anyonu (O2·-) meydana gelir.",
                "C": "Hidrojen peroksit, süperoksit dismutaz (SOD) aracılığıyla süperoksitten oluşturulur.",
                "D": "Peroksinitrit süperoksidin nitrik oksit ile birleşmesiyle oluşur.",
                "E": "Hipokloröz asit nötrofil miyeloperoksidazı tarafından üretilir."
            }
        ),
        56: make_micro_quiz(
            "Yaşlanan hücrelerde hasarlı ve depolarize mitokondrilerin dış zarında birikerek Parkin ubikitin ligazını stroma çekip mitofajiyi başlatan kinaz hangisidir?",
            {"A": "PINK1 kinaz", "B": "AMPK kinaz", "C": "ATM kinaz", "D": "Akt/PKB", "E": "mTORC1"},
            "A",
            {
                "A": "Doğru cevap A'dır: Normalde iç zara transfer edilip PARL ile yıkılan PINK1, membran potansiyeli çöken yaşlı mitokondrinin dış zarında birikir, fosforilasyonla Parkin'i aktive ederek mitofajiyi başlatır.",
                "B": "AMPK genel hücresel enerji sensörüdür.",
                "C": "ATM nükleer çift zincir DNA kırıklarını tanır.",
                "D": "Akt/PKB insülin sinyalinde hücre sağkalımını destekler.",
                "E": "mTORC1 otofajiyi ve mitofajiyi baskılayan anabolik kinaz kompleksidir."
            }
        )
    }

def get_extra_causal_chains():
    """Ekstra nedensel mekanizma zincirleri (k1-08)"""
    return {
        13: make_causal_chain(
            "Oksidatif DNA Hasarı ve Replikasyon Bloğu Zinciri",
            [
                "1. Eksojen toksinler veya mitokondriyal kaçaklar sonucu hidroksil radikali nükleer DNA'ya ulaşır",
                "2. Guanin bazları oksitlenerek 8-okso-7,8-dihidro-2'-deoksiguanozin (8-oxo-dG) lezyonuna dönüşür",
                "3. DNA replikasyon çatalı ilerlerken 8-oxo-dG bazını adenin ile hatalı eşleştirir",
                "4. Baz kesip onarım mekanizması (BER/OGG1) yetersiz kaldığında replikasyon çatalı çöker ve çift zincir kırığı oluşur",
                "5. ATM/ATR kinazlar aktive olarak p53'ü fosforiller ve hücre döngüsü kalıcı olarak durur"
            ]
        ),
        23: make_causal_chain(
            "Shelterin Disfonksiyonu ve DNA Hasar Yanıtı Kaskadı",
            [
                "1. TRF1, TRF2 ve POT1 proteinlerinin telomer ucundaki koruyucu bağlanması gevşer veya azalır",
                "2. 3' sarkan tek zincirli telomerik uç D-loop yapısından çözülerek serbest nükleer ortama açılır",
                "3. Hücresel DNA gözetim sistemi serbest telomerik ucu çıplak çift zincir kırığı (DSB) olarak algılar",
                "4. 53BP1 ve gama-H2AX odakları telomer ucu üzerinde birikerek TIF (Telomere Dysfunction-Induced Foci) oluşturur",
                "5. ATM kinaz p53'ü uyararak hücreyi senesens veya programlı apoptoz yoluna sokar"
            ]
        ),
        33: make_causal_chain(
            "Kritik Telomer Kısalması ve Hayflick Arrest Zinciri",
            [
                "1. Somatik hücre her bölünme döngüsünde 50-100 baz çifti telomerik TTAGGG dizisi kaybeder",
                "2. Yaklaşık 50-60 bölünme sonunda telomer uzunluğu 3-5 kilobaza gerileyerek kritik eşiğe ulaşır",
                "3. Shelterin kompleksi artık telomerik ucu çift zincirli DNA içine gömemez",
                "4. Nükleer sensörler aktive olur ve CDKN2A lokusundan p16INK4a ekspresyonu fırlar",
                "5. CDK4/CDK6 inaktive olur, Rb defosforile kalır ve E2F bloke edilerek hücre kalıcı G1 senesensine girer"
            ]
        ),
        43: make_causal_chain(
            "Mitokondriyal Elektron Sızıntısı ve Kısır Döngü Kaskadı",
            [
                "1. Yaşlanan mitokondrinin elektron transport zincirinde Kompleks I ve III proteinleri hasarlanır",
                "2. Elektronlar ubikinondan kaçarak moleküler oksijene aktarılır ve süperoksit (O2·-) üretimi artar",
                "3. Artan süperoksit mitokondriyal DNA'yı (mtDNA) histon koruması olmadığı için hızla mutasyona uğratır",
                "4. Mutasyona uğrayan mtDNA solunum zinciri alt birimlerini kusurlu sentezleyerek elektron kaçaklarını katlar",
                "5. Bu kısır döngü sitoplazmik proteazları ve lipidleri peroksidasyona uğratarak hücresel tükenişe yol açar"
            ]
        ),
        53: make_causal_chain(
            "MOMP Açılması ve İntrinsik Apoptoz Tetiği Mekanizması",
            [
                "1. Aşırı hücresel stres ve ROS mitokondri membranında Bax ve Bak pro-apoptotik proteinlerini oligomerize eder",
                "2. Mitokondri dış zarında geçirgenlik gözenekleri (MOMP) açılır ve zar potansiyeli çöker",
                "3. Zarlar arası mesafede depolanan sitokrom c sitoplazmaya kontrolsüz şekilde salınır",
                "4. Sitokrom c sitozolik Apaf-1 ve dATP ile birleşerek apoptomazom tekerleğini oluşturur",
                "5. Apoptomazom prokaspaz-9'u keserek aktif kaspaz-9 ve kaspaz-3 kaskadını tetikler"
            ]
        ),
        63: make_causal_chain(
            "Proteazomal Aşırı Yüklenme ve Agregom Oluşum Kaskadı",
            [
                "1. Oksidatif stres ve mutasyonlar nedeniyle yanlış katlanmış polipeptitlerin miktarı katlanarak artar",
                "2. Hsp70 ve Hsp90 gibi moleküler şaperonlar hatalı proteinlerin katlanmasını düzeltmede yetersiz kalır",
                "3. Yanlış katlanmış proteinler poliubikitinlenerek 26S proteazoma sevk edilir ancak proteazom kanalları tıkanır",
                "4. Sitoplazmada çözünmeyen protein kümeleri mikrotübül bağımlı dynein motorlarıyla sentrozom çevresinde toplanır",
                "5. Agregom adı verilen sitoplazmik inklüzyonlar oluşur ve lizozomal otofajiyi de tüketerek nörodejenerasyona zemin hazırlar"
            ]
        ),
        73: make_causal_chain(
            "mTOR Aktivasyonu ve Erken Senesens Kaskadı",
            [
                "1. Yüksek kalorili beslenme ve hiperinsülinemi IGF-1 reseptörü ve PI3K/Akt yolağını sürekli uyarır",
                "2. Akt kinaz TSC1/TSC2 kompleksini fosforilleyerek Rheb-GTP üzerinden mTORC1 kompleksini aşırı aktive eder",
                "3. Aktif mTORC1 p70S6K ve 4E-BP1 üzerinden ribozomal protein translasyonunu kontrolsüz hızlandırır",
                "4. Eşzamanlı olarak ULK1 kompleksini fosforilleyip baskılayarak lizozomal otofajiyi durdurur",
                "5. Hücre içi organel ve protein temizliği felç olur, oksidatif yük birikir ve hücre erken replikatif tükenişe girer"
            ]
        ),
        83: make_causal_chain(
            "SASP ve Parakrin Senesens Bulaşması Kaskadı",
            [
                "1. Replikatif veya stres kaynaklı senesense giren hücrede nükleer NF-kappaB ve p38 MAPK devamlı aktive kalır",
                "2. Hücre IL-1alfa, IL-6, IL-8, TNF-alfa ve MMP matris metalloproteinazlarını bol miktarda salgılar (SASP)",
                "3. Salgılanan pro-enflamatuar sitokinler çevre dokudaki sağlıklı komşu hücrelerin reseptörlerine bağlanır",
                "4. Komşu hücrelerde otokrin/parakrin sinyalleme ile intrasellüler ROS artışı ve DNA hasar yanıtı uyarılır",
                "5. Sağlıklı komşu hücreler de ikincil olarak senesense sürüklenir ve kronik doku steril inflamasyonu gelişir"
            ]
        ),
        93: make_causal_chain(
            "Senolitik Tedavi ve Doku Gençleşmesi Mekanizması",
            [
                "1. Senolitik ajanlar (örneğin dasatinib ve kuersetin kombinasyonu) sistemik dolaşıma verilir",
                "2. İlaçlar senesens hücrelerinin hayatta kalmasını sağlayan anti-apoptotik Bcl-2, Bcl-xL ve p21 kalkanlarını spesifik inhibe eder",
                "3. Senesens hücreleri yüksek iç stresleri nedeniyle hızla intrensek apoptoza uğrayarak seçici şekilde elenir",
                "4. Dokudaki SASP sitokin yükü ve kronik inflamatuar baskı dramatik düzeyde geriler",
                "5. Doku kök hücre kompartımanı baskılanmaktan kurtulur ve parankimal rejenerasyon yeniden başlar"
            ]
        ),
        98: make_causal_chain(
            "Kalori Kısıtlaması ve Sirtuin Aracılı Yaşam Uzatma Zinciri",
            [
                "1. Günlük kalori alımı malnütrisyon yaratmaksızın yüzde otuz oranında kısıtlanır",
                "2. İntrasellüler ATP/AMP oranı düşer ve NAD+/NADH oranı belirgin şekilde yükselir",
                "3. Artan NAD+ havuzu sitozolik ve nükleer SIRT1 ve SIRT3 deasetilaz enzimlerini güçlü biçimde uyarır",
                "4. SIRT1 PGC-1alfayı deasetile ederek aktive eder; mitokondriyal biyogenez ve antioksidan enzim sentezi artar",
                "5. Eşzamanlı FOXO transkripsiyon faktörleri uyarılır, DNA onarımı güçlenir ve organizma düzeyinde yaşam süresi uzar"
            ]
        )
    }

def get_extra_sliders():
    """Ekstra Before-After Karşılaştırma Kaydırıcıları (k1-08)"""
    return {
        7: make_before_after(
            "Hücresel Yaşlanma Durumu",
            "Genç Proliferatif Hücre",
            [
                "Uzun ve korunaklı telomer dizileri (10-15 kilobaz)",
                "Düşük p16INK4a ve p21CIP1 inhibitör ekspresyonu",
                "Yüksek replikatif kapasite ve hızlı hücre döngüsü",
                "Sağlam nükleer lamin ağı ve heterokromatin dengesi"
            ],
            "Yaşlı Senesent Hücre",
            [
                "Kritik düzeyde kısalmış telomer uçları (3-5 kilobaz)",
                "Kalıcı olarak artmış p16INK4a ve p21CIP1 ekspresyonu",
                "G1/S fazında geri dönüşümsüz kalıcı hücre döngüsü durması",
                "Lamin B1 kaybı ve SA-beta-galaktosidaz enzim pozitifliği"
            ]
        ),
        17: make_before_after(
            "Nükleer Zar Organizasyonu",
            "Fizyolojik Nükleer Zar (Lamin A)",
            [
                "ZMPSTE24 endoproteazı tarafından farnesil ucu temizlenmiş lamin A",
                "Pürüzsüz, yuvarlak ve esnek nükleer membran bütünlüğü",
                "Normal kromatin organizasyonu ve regüle gen transkripsiyonu",
                "Standart somatik ömür ve kontrollü mitoz süreci"
            ],
            "Hutchinson-Gilford Progerin Nükleusu",
            [
                "Kırpılma defekti nedeniyle farnesil kuyruğu kesilemeyen toksik progerin",
                "Zarda biriken progerin sonucu kırışık, lobüle ve dismorfik çekirdek",
                "Heterokromatin kaybı, kontrolsüz DNA çift zincir kırıkları",
                "Çocukluk çağında şiddetli ateroskleroz ve erken biyolojik yaşlanma"
            ]
        ),
        27: make_before_after(
            "Telomer Konformasyon Karşılaştırması",
            "Telomer Koruma Modu (İntakt T-Loop)",
            [
                "3' sarkan uç çift zincirli DNA içine kıvrılıp ilmeklenmiştir",
                "POT1 ve TRF2 telomerik DNA'yı tam kaplamıştır",
                "DNA onarım sensörleri telomeri çift zincir kırığı olarak görmez",
                "Hücre serbestçe replikasyon döngüsünü tamamlar"
            ],
            "Telomer Açılma Modu (D-Loop Bozulması)",
            [
                "Telomer kısalması nedeniyle T-loop yapısı gevşeyip çözülür",
                "Shelterin alt birimleri DNA ucundan ayrışır",
                "Nükleer ATM ve 53BP1 açık ucu çift zincir kırığı sanıp alarma geçer",
                "DNA hasar yanıtı tetiklenir ve kalıcı p53 aktivasyonu başlar"
            ]
        ),
        37: make_before_after(
            "Telomer Krizi ve Kontrol Noktaları",
            "p53 İntakt Telomer Krizi",
            [
                "Kritik telomer erozyonunda p53 p21'i uyarır",
                "Hücre ya güvenli senesense yönlendirilir ya da apoptoza sokulur",
                "Genomik bütünlük korunur ve malign transformasyon engellenir",
                "Doku dengesi stabil kalır, hücre klonal genişleme yapamaz"
            ],
            "p53 Defektif BFB Döngüsü",
            [
                "p53 mutasyonu varlığında erozyona uğrayan kromozomlar bölünmeyi sürdürür",
                "Çıplak uçlar non-homolog birleşmeyle disentrik kromozomlar oluşturur",
                "Anafazda köprüler kırılır ve yeniden birleşir (BFB döngüsü)",
                "Masif genomik instabilite, anöploidi ve telomeraz reaktivasyonu ile kanserleşme"
            ]
        ),
        47: make_before_after(
            "Mitokondriyal Sağlık Ayrımı",
            "Sağlıklı Mitokondri",
            [
                "Sıkı krista yapısı ve yüksek iç membran potansiyeli",
                "Minimum elektron kaçağı ve etkin ATP sentaz çalışması",
                "Aktif ve hasarsız mitokondriyal DNA transkripsiyonu",
                "Kusursuz ROS detoksifikasyonu (MnSOD ve Glutatyon peroksidaz)"
            ],
            "Yaşlanmış Disfonksiyonel Mitokondri",
            [
                "Şişmiş, parçalanmış kristalar ve çökmüş zar potansiyeli",
                "Elektron sızıntısı sonucu patlayıcı süperoksit üretimi",
                "Histonsuz mtDNA'da birikmiş geniş delesyonlar ve mutasyonlar",
                "Düşük ATP üretimi, sitoplazmik Ca2+ ve kaspaz salınım riski"
            ]
        ),
        57: make_before_after(
            "Mitofajik Temizlik Kapasitesi",
            "Fizyolojik Mitofaji Klirensi",
            [
                "Depolarize mitokondri dış zarında PINK1 birikir ve Parkin'i çeker",
                "Parkin dış zar proteinlerini ubikitinler",
                "LC3 reseptörleri hasarlı organeli fagozoma alıp lizozoma götürür",
                "Sitoplazma temiz kalır ve oksidatif stres kontrol altında tutulur"
            ],
            "Bozulmuş Mitofaji ve Organel Birikimi",
            [
                "Yaşlanma ile azalan lizozomal asidifikasyon ve defektif otofaji",
                "PINK1-Parkin yolağı aşırı yüke yanıt veremez",
                "Kusurlu mitokondriler sitozolde birikerek ROS saçmaya devam eder",
                "NLRP3 inflamazomu tetiklenir ve kronik hücresel harabiyet başlar"
            ]
        ),
        67: make_before_after(
            "Hücresel Proteom Bütünlüğü",
            "Genç Proteostaz Ağı",
            [
                "Hsp70/90 şaperonları proteinleri düzgün katlar veya onarır",
                "26S proteazom ubikitinli hatalı proteinleri anında hidroliz eder",
                "Şaperon aracılı otofaji lizozomal klirensi eksiksiz sağlar",
                "Berrak sitoplazma ve homojen nöronal iletim korunur"
            ],
            "Yaşlı Çökmüş Proteom",
            [
                "Şaperon sentez kapasitesinde düşüş ve yanlış katlanma artışı",
                "Okside proteinlerin 26S proteazom kanallarını tıkaması",
                "Agregomlar, amiloid fibrilleri ve çözünmeyen inklüzyon birikimi",
                "Alzheimer, Parkinson ve ALS gibi nörodejeneratif agregasyon hastalıkları"
            ]
        ),
        77: make_before_after(
            "Besin Algılama ve Yaşlanma Hızı",
            "Aşırı Kalorili / Yüksek IGF-1 Beslenme",
            [
                "Sürekli insülin salınımı ve mTORC1 hiperaktivasyonu",
                "Ribozomal translasyon aşırı yükü ve otofajinin baskılanması",
                "Mitokondriyal biyogenez düşüşü ve hızlanmış yaşlanma hızı",
                "Obezite, insülin direnci ve vasküler endotelyal disfonksiyon"
            ],
            "Kalori Kısıtlaması / AMPK ve Sirtuin Aktivasyonu",
            [
                "Düşük glukoz ile yükselen AMP/ATP oranı ve aktive AMPK",
                "Artan NAD+ düzeyiyle indüklenen SIRT1/SIRT3 deasetilazlar",
                "mTORC1 inhibisyonu, yoğun otofajik temizlik ve PGC-1alfa uyarımı",
                "Uzamış sağlıklı yaşam süresi ve kardiyovasküler koruma"
            ]
        ),
        87: make_before_after(
            "Dokusal İnflamasyon Profili",
            "Normal Yaşlanma Dokusu",
            [
                "Minimal senesent hücre popülasyonu ve kontrollü fagositoz",
                "Düşük bazal interlökin ve sitokin seviyeleri",
                "Korunmuş hücre dışı matriks elastisitesi ve bazal membran",
                "Doku kök hücrelerinin fizyolojik yenilenme dinamikleri"
            ],
            "SASP Yüklü İnflammaging Dokusu",
            [
                "Dokuda biriken ve immün sistemden kaçan senesent fibroblastlar",
                "Sürekli IL-6, IL-8, TNF-alfa ve MMP salgılanması",
                "Doku matriksinde kollajen yıkımı, fibrozis ve parakrin hasar",
                "Kök hücre rezervuarının tükenmesi ve tümör mikroçevresi oluşumu"
            ]
        ),
        97: make_before_after(
            "Geriatrik Tedavi Modelleri",
            "Konvansiyonel Geriatrik Yaklaşım",
            [
                "Yalnızca sekonder kronik hastalıkların semptomatik tedavisi",
                "Biriken senesent hücre yüküne ve SASP salgısına müdahale edilememesi",
                "Doku harabiyetinin ilerleyici ve geri dönüşsüz kabul edilmesi",
                "Çoklu ilaç kullanımı ve kümülatif organ toksisitesi"
            ],
            "Senolitik ve Senomorfik Hedefe Yönelik Tedavi",
            [
                "Dasatinib, kuersetin veya fisetin ile senesent hücrelerin seçici apoptozu",
                "Senomorfikler (metformin, rapamisin) ile SASP salgısının susturulması",
                "Doku inflamasyonunda gerileme ve kök hücre rejenerasyonunda canlanma",
                "Biyolojik yaşlanmanın temel sürücülerini hedefleyen nedensel tıp modeli"
            ]
        ),
        99: make_before_after(
            "Hücresel Çoğalma ve Savunma",
            "Kontrolsüz Hücresel Replikasyon",
            [
                "Telomer kısalması dikkate alınmadan devam eden mitoz",
                "Kromozomal kırıklar ve translokasyonların birikme tehlikesi",
                "Tümörijenez yönünde artan mutasyonel instabilite riski",
                "Hücrenin neoplastik klona dönüşme potansiyeli"
            ],
            "Replikatif Senesens Kontrol Ağı",
            [
                "Hayflick sınırında p16 ve p21 ile kalıcı G1 fazı duraklaması",
                "Bozuk genomlu hücrelerin bölünmesinin kesin olarak engellenmesi",
                "Kansere karşı primer ve güçlü bir antineoplastik savunma barikatı",
                "Organizma düzeyinde tümör gelişiminin önlenmesi pahasına lokal yaşlanma"
            ]
        ),
        100: make_before_after(
            "Yaşlanma Ölçütleri",
            "Kronolojik Yaşlanma",
            [
                "Doğumdan itibaren geçen takvimsel gün ve yıl sayısı",
                "Hücrelerin moleküler stresinden bağımsız doğrusal zaman akışı",
                "Organ fonksiyon rezervi hakkında kesin bilgi vermeyen standart ölçüt",
                "Değiştirilemeyen ve modifiye edilemeyen evrensel parametre"
            ],
            "Biyolojik ve Epigenetik Yaşlanma",
            [
                "DNA metilasyon saatleri (Horvath saati) ile ölçülen hücresel yaş",
                "Telomer uzunluğu, mitokondriyal sağlık ve proteostaz durumu",
                "Kalori kısıtlaması, egzersiz ve farmakoterapiyle yavaşlatılabilen süreç",
                "Gerçek fonksiyonel morbidite ve mortaliteyi belirleyen fizyolojik durum"
            ]
        )
    }

def get_extra_branching():
    """Ekstra Dallanma Mantığı (Branching Logic) Karar Senaryoları (k1-08)"""
    return {
        8: make_branching_logic(
            "Bir araştırmacı primer insan fibroblast kültüründe 55 pasaj sonrasında hücre bölünmesinin durduğunu ve hücrelerin morfolojik olarak yassılaştığını gözlemliyor. Hangi moleküler inceleme ilk adımı olmalıdır?",
            [
                {
                    "text": "SA-beta-galaktosidaz boyaması ve p16INK4a/p21 ekspresyon düzeyini analiz et",
                    "feedback": "Klinik Olarak En Doğru Seçim: Replikatif senesensin altın standardı pH 6.0'da SA-beta-galaktosidaz enzim aktivitesi ve CDK inhibitörlerinin gösterilmesidir.",
                    "isOptimal": True
                },
                {
                    "text": "Doğrudan sitotoksik kemoterapi uygulayarak hücreleri zorla S fazına sok",
                    "feedback": "Hatalı Yaklaşım: Senesent hücreler geri dönüşümsüz olarak G1 fazında durmuştur; sitotoksik ajanlar apoptoza veya nekroza yol açar.",
                    "isOptimal": False
                },
                {
                    "text": "Besi yerine glukoz ekleyip hücrelerin mitoza başlamasını bekle",
                    "feedback": "Yetersiz Yaklaşım: Replikatif senesens besin eksikliğinden değil, Hayflick sınırı ve telomer kısalmasından kaynaklanır.",
                    "isOptimal": False
                },
                {
                    "text": "Kültürü dondurup çözerek nükleer laminleri parçala",
                    "feedback": "Hatalı Yaklaşım: Fiziksel hücre hasarı yaratır, senesens fizyolojisini aydınlatmaz.",
                    "isOptimal": False
                }
            ]
        ),
        18: make_branching_logic(
            "Genç yaşta katarakt, bilateral subkutan yağ dokusu atrofisi, saç dökülmesi ve osteoporoz gelişen 35 yaşındaki bir hastada Werner Sendromu şüphesiyle hangi gen paneli taranmalıdır?",
            [
                {
                    "text": "WRN geni dizi analizi (RecQ helikaz mutasyonları)",
                    "feedback": "Mükemmel Karar: Werner sendromu WRN genindeki delesyon/nokta mutasyonları sonucu gelişen otozomal resesif helikaz yetersizliğidir.",
                    "isOptimal": True
                },
                {
                    "text": "Yalnızca hemoglobin elektroforezi ve oraklaşma testi",
                    "feedback": "Alakasız Seçenek: Hemoglobinopatiler erken yaşlanma kliniği oluşturmaz.",
                    "isOptimal": False
                },
                {
                    "text": "Sitolojik idrar mikroskopisi",
                    "feedback": "Yetersiz: Werner sendromunun primer genetik etiyolojisini saptamaz.",
                    "isOptimal": False
                },
                {
                    "text": "Yalnızca tiroid hormonları taraması",
                    "feedback": "Eksik: Tiroid hormonları genel metabolizmayı gösterir ancak erken yaşlanma helikaz defektini aydınlatmaz.",
                    "isOptimal": False
                }
            ]
        ),
        28: make_branching_logic(
            "Telomer boyunu uzatmak amacıyla bir dokuda TERT genini adenovirüs aracılığıyla aşırı eksprese etmeyi planlayan onkoloji ekibinin alması gereken en kritik güvenlik önlemi nedir?",
            [
                {
                    "text": "Hücrelerde p53 ve Rb mutasyonu olup olmadığını kontrol etmek ve malign transformasyon riskini izlemek",
                    "feedback": "Hayati Onkolojik Karar: Telomeraz aktivasyonu yaşlanmayı geciktirirken, hasarlı genoma sahip hücrelerde kontrolsüz kanserojenik immortalizasyona yol açabilir.",
                    "isOptimal": True
                },
                {
                    "text": "Virüsün hücre içine sadece kalsiyum tuzları ile sokulması",
                    "feedback": "Önemsiz/Hatalı: Kanserleşme riskini bertaraf etmeyen teknik bir detaydır.",
                    "isOptimal": False
                },
                {
                    "text": "Hücreleri 42 derecede ısıtarak telomerazı denatüre etmek",
                    "feedback": "Mantıksız: Amacımız enzimi çalıştırmaktır; enzimi denatüre etmek müdahaleyi anlamsızlaştırır.",
                    "isOptimal": False
                },
                {
                    "text": "Yalnızca sitoplazmik pH ölçümü yapmak",
                    "feedback": "Yetersiz: Neoplastik transformasyon riskini denetlemez.",
                    "isOptimal": False
                }
            ]
        ),
        38: make_branching_logic(
            "Kolorektal adenomda p53 geni mutasyona uğramış ve telomerleri kritik kısalığa ulaşmış bir polipoid lezyonda Bridge-Fusion-Breakage krizini durdurmak için hangi biyolojik hedef seçilmelidir?",
            [
                {
                    "text": "Hücrelerin hTERT telomeraz reaktivasyonunu engelleyerek mitotik kriz evresinde tükenip ölmelerini sağlamak",
                    "feedback": "Hedefe Yönelik Karar: Telomerazı aktive edemeyen kanser öncülü hücreler BFB krizinden sağ çıkamaz ve mitotik felaketle ölür.",
                    "isOptimal": True
                },
                {
                    "text": "Telomeraz genini aktive edip hücrelerin ömrünü uzatmak",
                    "feedback": "Kritik Hata: Telomerazı aktive etmek lezyonu tam teşekküllü malign karsinoma dönüştürür.",
                    "isOptimal": False
                },
                {
                    "text": "Kolon lümenine hipertonik salin lavajı uygulamak",
                    "feedback": "Etkisiz: Hücre içi genomik instabiliteyi etkilemez.",
                    "isOptimal": False
                },
                {
                    "text": "p53 yerine nükleozomları parçalayan nükleaz vermek",
                    "feedback": "Toksik ve Hatalı: Bütün sağlıklı dokuyu yok eder.",
                    "isOptimal": False
                }
            ]
        ),
        48: make_branching_logic(
            "Kardiyomiyositlerde mitokondri kaynaklı süperoksit üretimini baskılamak ve membran lipid peroksidasyonunu azaltmak isteyen araştırmacı hangi enzim sistemini hedeflemelidir?",
            [
                {
                    "text": "Mitokondriyal manganez süperoksit dismutaz (MnSOD/SOD2) ve glutatyon peroksidaz (GPx) aktivitesini artırmak",
                    "feedback": "En İdeal Biyokimyasal Karar: Süperoksit radikallerini hızla H2O2 ve suya çeviren SOD2 ve GPx antioksidan savunmanın omurgasıdır.",
                    "isOptimal": True
                },
                {
                    "text": "Elektron transport zincirinde Sitokrom c oksidazı tamamen bloke etmek",
                    "feedback": "Ölümcül Hata: Kompleks IV'ün inhibisyonu hücresel solunumu durdurur ve hücreyi akut hipoksik nekroza sokar.",
                    "isOptimal": False
                },
                {
                    "text": "Mitokondri iç zarına kalsiyum pompalamak",
                    "feedback": "Zararlı Seçim: Kalsiyum yükü mitokondriyal geçirgenlik gözeneğini (MPTP) açarak apoptozu tetikler.",
                    "isOptimal": False
                },
                {
                    "text": "Mitokondri DNA'sını kesip atmak",
                    "feedback": "Yıkıcı Seçim: Hücresel enerji üretimini tamamen felç eder.",
                    "isOptimal": False
                }
            ]
        ),
        58: make_branching_logic(
            "Dopaminerjik nöronlarda depolarize olmuş hasarlı mitokondrilerin birikmesini engellemek için geliştirilen yeni bir nöroprotektif molekülün etki mekanizması ne olmalıdır?",
            [
                {
                    "text": "PINK1 stabilizasyonunu ve Parkin translokasyonunu destekleyerek mitofajiyi artırmak",
                    "feedback": "Patofizyolojik Olarak Mükemmel: Hasarlı organellerin hızla otofagozoma alınması dopaminerjik nöronları Parkinson patolojisinden korur.",
                    "isOptimal": True
                },
                {
                    "text": "Lizozomal v-ATPase proton pompasını bloke etmek",
                    "feedback": "Hatalı Karar: Asidifikasyonu bozmak mitofajik sindirimi durdurur ve toksik birikimi artırır.",
                    "isOptimal": False
                },
                {
                    "text": "Mitokondri dış zarına kaspaz-3 eklemek",
                    "feedback": "Yanlış Hedef: Kaspaz-3 mitofajiyi başlatmaz, doğrudan hücresel apoptoz ve nöron ölümüne yol açar.",
                    "isOptimal": False
                },
                {
                    "text": "Sitozolik ubikitini yok etmek",
                    "feedback": "Felaket Senaryosu: Ubikitinsiz hücre protein ve organel temizliğini hiçbir şekilde yapamaz.",
                    "isOptimal": False
                }
            ]
        ),
        68: make_branching_logic(
            "Yaşlı farelerin hipokampusunda amiloid-beta ve fosforile tau agregatlarının proteazomal yolla temizlenemediği saptanıyor. Terapötik müdahale hangi basamağa odaklanmalıdır?",
            [
                {
                    "text": "Hsp70 şaperon ekspresyonunu artırmak ve 20S/26S proteazom peptidaz aktivitesini stimüle etmek",
                    "feedback": "Optimal Moleküler Müdahale: Şaperonlar oligomerlerin agrege olmasını engellerken, aktif proteazom bu polipeptitleri zararsız amino asitlere yıkar.",
                    "isOptimal": True
                },
                {
                    "text": "Hücre içi ribozomal translasyonu on katına çıkarmak",
                    "feedback": "Durumu Ağırlaştırır: Proteazom kapasitesi yetersizken daha fazla protein sentezlemek agregasyonu katlar.",
                    "isOptimal": False
                },
                {
                    "text": "Proteazom kapakçıklarını kimyasal inhibitörlerle kapatmak",
                    "feedback": "Kritik Yanlış: Proteazomu bloke etmek (bortezomib gibi) nöronlarda masif toksik protein birikimi yapar.",
                    "isOptimal": False
                },
                {
                    "text": "Endoplazmik retikulum Ca2+ kanallarını delmek",
                    "feedback": "Ölümcül Yanıt: ER stresi ve apoptozu indükler.",
                    "isOptimal": False
                }
            ]
        ),
        78: make_branching_logic(
            "Tip 2 diyabet ve metabolik sendrom zemininde hızlanmış vasküler yaşlanma gösteren 55 yaşındaki bir hastada besin algılama yolaklarını gençleştirmek için en rasyonel farmakolojik tercih hangisidir?",
            [
                {
                    "text": "Metformin kullanarak AMPK'yi aktive etmek ve dolaylı olarak mTORC1'i baskılamak",
                    "feedback": "Mükemmel Klinik Karar: Metformin AMP/ATP oranını taklit ederek AMPK'yi uyarır, mTORC1'i dizginler ve otofajiyi uyararak vasküler yaşlanmayı geciktirir.",
                    "isOptimal": True
                },
                {
                    "text": "Yüksek doz ekzojen insülin ve IGF-1 enjeksiyonları ile mTORC1'i sürekli uyarmak",
                    "feedback": "Ters Teper: mTORC1'in hiperaktivasyonu otofajiyi boğar ve hücresel yaşlanmayı hızlandırır.",
                    "isOptimal": False
                },
                {
                    "text": "Sirtuin enzimlerini yıkan kimyasal antagonistler vermek",
                    "feedback": "Hatalı Seçenek: Sirtuinleri inhibe etmek epigenetik instabiliteyi ve metabolik hasarı artırır.",
                    "isOptimal": False
                },
                {
                    "text": "Karbonhidrattan zengin hiperkalorik diyet reçete etmek",
                    "feedback": "Hastalığı Şiddetlendirir: Hiperglisemi AGE ürünlerini ve hücresel tükenişi tetikler.",
                    "isOptimal": False
                }
            ]
        ),
        88: make_branching_logic(
            "Osteoartritik eklem sıvısında yüksek oranda senesent sinovyal fibroblastlar ve SASP kaynaklı IL-6, MMP-13 saptanıyor. Eklem kıkırdağını korumak için hangi strateji tercih edilmelidir?",
            [
                {
                    "text": "Lokal senolitik enjeksiyonu veya NF-kappaB/SASP inhibitörü (senomorfik) uygulamak",
                    "feedback": "Hedefe Tam İsabet: Senesent hücrelerin eklemden temizlenmesi veya SASP sekresyonunun susturulması kıkırdak matriks yıkımını dramatik olarak durdurur.",
                    "isOptimal": True
                },
                {
                    "text": "Ekleme rekombinant IL-1 ve TNF-alfa enjekte etmek",
                    "feedback": "Tahrip Edici Yanlış: İnflamasyonu ve kıkırdak nekrozunu daha da hızlandırır.",
                    "isOptimal": False
                },
                {
                    "text": "Kıkırdak dokusuna radyasyon uygulayarak DNA hasarını artırmak",
                    "feedback": "Felaket Kararı: Sağlıklı kondrositleri de senesense ve apoptoza sokar.",
                    "isOptimal": False
                },
                {
                    "text": "Sinovyal membranı tamamen koterize edip eklemi hareketsiz bırakmak",
                    "feedback": "Hatalı ve İnvaziv: Eklem ankilozuna ve kalıcı fonksiyon kaybına yol açar.",
                    "isOptimal": False
                }
            ]
        ),
        95: make_branching_logic(
            "Klinik araştırmalarda senolitik kokteyl (Dasatinib + Kuersetin) verilen bir pre-klinik modelde tedavi başarısını doğrulamak için hangi doku biyobelirteci takip edilmelidir?",
            [
                {
                    "text": "Dokudaki SA-beta-galaktosidaz pozitif hücre sayısının ve serum IL-6 düzeyinin gerilemesi",
                    "feedback": "Altın Standart İzlem: Senolitik etkinliğin kanıtı hedef senesent hücrelerin dokudan temizlenmesi ve SASP yükünün düşmesidir.",
                    "isOptimal": True
                },
                {
                    "text": "Yalnızca idrar dansitesinin ölçülmesi",
                    "feedback": "Yetersiz ve İlgisiz: Senesens klirensini spesifik yansıtmaz.",
                    "isOptimal": False
                },
                {
                    "text": "Hücrelerin telomer boyunun anında iki katına çıkmasını beklemek",
                    "feedback": "Biyolojik İmkansızlık: Senolitikler senesent hücreleri öldürür, kalan hücrelerin telomerini uzatmaz.",
                    "isOptimal": False
                },
                {
                    "text": "Serum kalsiyumunun taş oluşturacak kadar yükselmesi",
                    "feedback": "Toksisite Bulgusu: Başarı kriteri değil patolojidir.",
                    "isOptimal": False
                }
            ]
        ),
        96: make_branching_logic(
            "Uzun yaşam (longevity) araştırmasında kalorik kısıtlama protokolü uygulanan primatlarda SIRT1'in transkripsiyonel aktivitesini kanıtlamak için hangi moleküler değişim aranmalıdır?",
            [
                {
                    "text": "PGC-1alfa ve FOXO3 transkripsiyon faktörlerinin deasetilasyonu ve mitokondriyal biyogenez genlerinin artışı",
                    "feedback": "Eksiksiz Moleküler Kanıt: SIRT1 bir deasetilazdır; PGC-1alfa ve FOXO'yu deasetile ederek antioksidan ve mitokondriyal genleri aktive eder.",
                    "isOptimal": True
                },
                {
                    "text": "DNA metilasyonunun tamamen sıfırlanması",
                    "feedback": "Biyolojik İmkansızlık: DNA metilasyonu sıfırlanırsa hücre kimliğini kaybeder ve ölür.",
                    "isOptimal": False
                },
                {
                    "text": "Histonların aşırı asetillenerek kromatinin çözülmesi",
                    "feedback": "Ters Mekanizma: Sirtuinler deasetilazdır, asetilasyonu artırmaz; deasetile eder.",
                    "isOptimal": False
                },
                {
                    "text": "Bütün proteazom enzimlerinin lize edilmesi",
                    "feedback": "Zararlı Sonuç: Proteostazın çökmesi anlamına gelir.",
                    "isOptimal": False
                }
            ]
        ),
        92: make_branching_logic(
            "Kardiyovasküler senesens ve aterosklerozda SASP faktörlerinden hangisinin monositleri vasküler duvara çeken temel kemokin olduğu bilinmektedir?",
            [
                {
                    "text": "MCP-1 (CCL2) ve İnterlökin-8 (CXCL8)",
                    "feedback": "Doğru Patolojik Seçim: Yaşlanan endotel ve köpük hücreler MCP-1 ve IL-8 salgılayarak lökosit ekstravazasyonunu tetikler.",
                    "isOptimal": True
                },
                {
                    "text": "Eritropoietin ve Trombopoietin",
                    "feedback": "Alakasız: Hematopoietik büyüme faktörleridir, senesent vasküler kemokin değildir.",
                    "isOptimal": False
                },
                {
                    "text": "Safra asitleri ve kolik asit",
                    "feedback": "İlgisiz: Karaciğerde sentezlenen sindirim molekülleridir.",
                    "isOptimal": False
                },
                {
                    "text": "İnsülin benzeri büyüme faktörü-2",
                    "feedback": "Hatalı: Monosit kemotaksisinde primer rol oynamaz.",
                    "isOptimal": False
                }
            ]
        ),
        82: make_branching_logic(
            "Yaşlanan dokularda cGAS-STING yolağının kronik olarak tetiklenmesinin altında yatan temel hücresel patoloji nedir?",
            [
                {
                    "text": "Lamin B1 kaybı ve nükleer zardan sitoplazmaya sızan endojen kromatin fragmanları (mikronükleuslar)",
                    "feedback": "Son Derece Derin Bilimsel Seçim: Nükleer kılıf geçirgenliği bozulunca sitoplazmaya sızan DNA parçaları cGAS enzimi tarafından yabancı patojen gibi algılanarak STING ve interferon yanıtını ateşler.",
                    "isOptimal": True
                },
                {
                    "text": "Lizozomların içine kalsiyum girmesi",
                    "feedback": "Alakasız Mekanizma: cGAS-STING sitozolik DNA sensörüdür.",
                    "isOptimal": False
                },
                {
                    "text": "Mitokondrinin fazla glukoz üretmesi",
                    "feedback": "Biyokimyasal Yanlış: Mitokondri glukoz üretmez, glukoz türevlerini yıkar.",
                    "isOptimal": False
                },
                {
                    "text": "Ribozomların çekirdeğe göç etmesi",
                    "feedback": "Anatomik Olarak İmkansız: Ribozomlar sitoplazmada translasyon yapar.",
                    "isOptimal": False
                }
            ]
        ),
        72: make_branching_logic(
            "Yaşlanma karşıtı çalışmalarda rapamisinin yaşam süresini uzatıcı etkisinin temel moleküler temeli hangisidir?",
            [
                {
                    "text": "mTORC1 kompleksini allosterik inhibe ederek protein translasyon stresini düşürmesi ve otofajiyi serbest bırakması",
                    "feedback": "Kusursuz Moleküler Açıklama: Rapamisin FKBP12 ile birleşerek mTORC1'i bloke eder; böylece ULK1 üzerindeki baskı kalkar ve otofajik organel temizliği başlar.",
                    "isOptimal": True
                },
                {
                    "text": "DNA helikaz enzimlerini tamamen parçalaması",
                    "feedback": "Ölümcül Hata: Helikazların yok edilmesi replikasyonu durdurur ve hücreyi öldürür.",
                    "isOptimal": False
                },
                {
                    "text": "ATP sentezini sıfırlayarak hücreyi nekroza yönlendirmesi",
                    "feedback": "Yıkıcı Etki: Sağlıklı ömür uzatmaz, doku ölümüne yol açar.",
                    "isOptimal": False
                },
                {
                    "text": "Hücre çekirdeğini eritmesi",
                    "feedback": "Saçma ve Toksik Seçenek.",
                    "isOptimal": False
                }
            ]
        )
    }

def get_extra_tables():
    """Ekstra İnteraktif Karşılaştırma Tabloları (k1-08)"""
    return {
        14: make_table(
            ["Klinik Sendrom", "Mutasyona Uğrayan Gen", "Hücresel İşlev Kusuru"],
            [
                [("Werner Sendromu", False, ""), ("WRN Helikaz", True, "DNA replikasyon ve onarım enzimini düşününüz"), ("Genomik instabilite", False, "")],
                [("Hutchinson-Gilford", False, ""), ("LMNA Geni", True, "Nükleer zar ara filaman proteinini anımsayınız"), ("Progerin birikimi", False, "")],
                [("Ataksi Telenjiektazi", False, ""), ("ATM Kinaz", True, "Çift zincir kırık sensörünü hatırlayınız"), ("DSB sinyal kusuru", False, "")]
            ]
        ),
        24: make_table(
            ["Protein Birimi", "DNA Bölgesi", "Moleküler Görevi"],
            [
                [("TRF1", False, ""), ("Çift zincirli telomerik dizi", True, "Telomerin çift iplikli bölgesine bağlanan faktörü anımsayınız"), ("Replikasyon kontrolü", False, "")],
                [("TRF2", False, ""), ("T-loop kavşağı", True, "Kromozom uçlarını non-homolog birleşmeden koruyan faktörü düşününüz"), ("Uç birleşmesini önleme", False, "")],
                [("POT1", False, ""), ("3' tek zincirli çıkıntı", True, "Tek iplikli telomerik DNA'yı örten faktörü hatırlayınız"), ("ATR yanıtını baskılama", False, "")]
            ]
        ),
        34: make_table(
            ["Hücresel Evre", "Telomer Durumu", "Hücrenin Akıbeti"],
            [
                [("Hayflick Senesensi", False, ""), ("Kritik kısalmış (3-5 kb)", True, "Hücre bölünmesini durduran baz çifti eşiğini düşününüz"), ("Kalıcı G1 fazı arresti", False, "")],
                [("Kriz Evresi", False, ""), ("Çıplak uçlar ve BFB döngüsü", True, "Kromozom füzyonlarına zemin hazırlayan aşınmayı anımsayınız"), ("Mitotik felaket ve ölüm", False, "")],
                [("Ölümsüz Kanser", False, ""), ("Telomeraz ile stabilize", True, "Malign hücrelerde yeniden aktive olan enzimi hatırlayınız"), ("Sınırsız replikasyon", False, "")]
            ]
        ),
        44: make_table(
            ["Radikal Türü", "Primer Kaynağı", "Detoksifiye Eden Enzim"],
            [
                [("Süperoksit (O2·-)", False, ""), ("Mitokondri ETC Kompleks I/III", True, "Solunum zincirindeki elektron kaçak noktalarını düşününüz"), ("Süperoksit Dismutaz", False, "")],
                [("Hidrojen Peroksit", False, ""), ("SOD enzimatik reaksiyonu", True, "Süperoksidin dismutasyon reaksiyonunu hatırlayınız"), ("Katalaz ve GPx", False, "")],
                [("Hidroksil Radikali", False, ""), ("Fenton reaksiyonu", True, "Demir katalizli tehlikeli serbest radikal üretimini düşününüz"), ("Endojen antioksidanlar", False, "")]
            ]
        ),
        54: make_table(
            ["Protein Grubu", "Ana Temsilcileri", "Mitokondriyal Etkisi"],
            [
                [("Anti-apoptotik", False, ""), ("Bcl-2 ve Bcl-xL", True, "Hücre sağkalımını koruyan onkogenik proteinleri düşününüz"), ("MOMP oluşumunu engelleme", False, "")],
                [("Pro-apoptotik Efektör", False, ""), ("Bax ve Bak", True, "Zarda delik açan temel oligomerik proteinleri hatırlayınız"), ("Geçirgenlik gözeneği açma", False, "")],
                [("BH3-only Sensör", False, ""), ("Puma ve Noxa", True, "DNA hasarında p53 tarafından aktive edilen sensörleri anımsayınız"), ("Anti-apoptotikleri bağlama", False, "")]
            ]
        ),
        64: make_table(
            ["Kontrol Düzeneği", "Hücresel Yerleşim", "Primer Görevi"],
            [
                [("Moleküler Şaperonlar", False, ""), ("Sitozol ve ER lümeni", True, "Isı şoku yanıtı ile uyarılan katlanma yardımcılarını anımsayınız"), ("Katlanmayı sağlama", False, "")],
                [("Ubikitin-Proteazom", False, ""), ("Sitozol ve Nükleus", True, "26S silindirik yıkım kompleksinin bulunduğu alanları düşününüz"), ("Kısa ömürlü proteinleri yıkma", False, "")],
                [("Makrootofaji", False, ""), ("Lizozomal sistem", True, "Çift zarlı vezikülün lizozomla kaynaştığı organel ağını hatırlayınız"), ("Agregat ve organel temizliği", False, "")]
            ]
        ),
        74: make_table(
            ["Sinyal Yolağı", "Metabolik Uyaran", "Ömür Üzerine Etkisi"],
            [
                [("IGF-1 / Akt / mTOR", False, ""), ("Yüksek kalori ve glukoz", True, "Büyüme faktörlerinin yüksek olduğu anabolik durumu düşününüz"), ("Yaşlanmayı hızlandırır", False, "")],
                [("AMPK Kinaz", False, ""), ("Düşük ATP / Yüksek AMP", True, "Hücrenin enerji krizinde olduğu metabolik sinyali hatırlayınız"), ("Ömrü uzatır", False, "")],
                [("SIRT1 Sirtuin", False, ""), ("Yüksek NAD+ seviyesi", True, "Kalori kısıtlamasında artan deasetilaz kofaktörünü anımsayınız"), ("Genomik stabilite ve uzun ömür", False, "")]
            ]
        ),
        84: make_table(
            ["SASP Grubu", "Örnek Moleküller", "Dokusal Patolojik Etki"],
            [
                [("İnflamatuar Sitokinler", False, ""), ("IL-1alfa, IL-6, TNF-alfa", True, "Akut faz yangısını tetikleyen temel interlökinleri anımsayınız"), ("Steril kronik inflamasyon", False, "")],
                [("Kemokinler", False, ""), ("MCP-1 ve IL-8", True, "Lökositleri dokuya çeken atraktan kemokinleri düşününüz"), ("İmmün hücre infiltrasyonu", False, "")],
                [("Metaloproteinazlar", False, ""), ("MMP-1 ve MMP-13", True, "Kollajen ve elastini yıkan çinko bağımlı enzimleri hatırlayınız"), ("Matriks ve elastisite kaybı", False, "")]
            ]
        ),
        94: make_table(
            ["Anti-Aging Sınıfı", "Öncü Ajanlar", "Temel Moleküler Hedef"],
            [
                [("Senolitikler", False, ""), ("Dasatinib ve Kuersetin", True, "Bcl-2 ailesini ve SCAP kalkanlarını hedefleyen molekülleri düşününüz"), ("Senesent hücre apoptozu", False, "")],
                [("Senomorfikler", False, ""), ("Metformin ve Rapamisin", True, "Hücreyi öldürmeden zararlı salgısını susturan ajanları hatırlayınız"), ("SASP salgısını baskılama", False, "")],
                [("NAD+ Öncülleri", False, ""), ("NMN ve Nikotinamid", True, "Sirtuin kofaktörü olan moleküler öncülleri anımsayınız"), ("Sirtuin aktivasyonu", False, "")]
            ]
        )
    }
