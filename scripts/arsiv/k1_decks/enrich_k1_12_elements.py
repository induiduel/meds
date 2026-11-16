# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını garanti eder.
"""

from scripts.k1_12_deck_data.helpers import (
    make_branching_logic, make_causal_chain, make_before_after, make_table
)

def get_extra_branching():
    """Branching logic (klinik karar verme) oranını artırmak için hedeflenen slaytlara eklenecek ögeler."""
    return {
        2: make_branching_logic(
            "22 yaşında hasta arı sokması sonrası dakikalar içinde dudaklarda şişme, yaygın ürtiker, ses kısıklığı ve hırıltılı solunum ile acil servise getiriliyor. Tansiyon 75/40 mmHg, nabız 125/dk ölçülüyor.",
            "Bu hastada mast hücre degranülasyonu ile salınan masif histamin ve lökotrien fırtınasını geri çevirmek için ilk yapılması gereken hayat kurtarıcı müdahale nedir?",
            [
                {
                    "text": "Derhal intramusküler (IM) epinefrin (adrenalin) uygulanmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Anaflakside histamin kaynaklı yaygın vazodilatasyon ve laringeal ödemi geri çeviren ilk ve en kritik ilaç intramusküler epinefrindir."
                },
                {
                    "text": "Yalnızca oral H1 antihistaminik verilip 30 dakika beklenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Şok ve hava yolu tıkanıklığında antihistaminik tek başına yetersizdir ve emilimi gecikir; epinefrin zorunludur."
                },
                {
                    "text": "Hastaya hemen sedatif verilerek sakinleşmesi sağlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Solunum sıkıntısı ve hipotansiyonda sedasyon kardiyorespiratuar arrest riskini artırır."
                }
            ]
        ),
        6: make_branching_logic(
            "Soğuk algınlığı sonrası burun tıkanıklığı ve akıntısı nedeniyle H1 antihistaminik kullanan bir tıp öğrencisi, ilacın burun akıntısını kestiğini ancak burun mukozasındaki lokal doku dolgunluğu ve tıkanıklığının devam ettiğini fark ediyor.",
            "Bu klinik tablonun kimyasal mediyatör fizyopatolojisi açısından en mantıklı gerekçesi nedir?",
            [
                {
                    "text": "Histamin venüler geçirgenliği artırır ancak tıkanıklıktaki uzun süreli vazodilatasyon ve lökosit toplanmasından eikozanoidler ve kininler de sorumludur.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Mediyatör fazlalığı (redundancy) nedeniyle tek başına histamin blokajı eikozanoid ve bradikinin kaynaklı mukozal konjesyonu tamamen gideremez."
                },
                {
                    "text": "Histamin vazodilatasyon değil yalnızca vazokonstriksiyon yapar.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Histamin H1 reseptörleriyle güçlü arterioler vazodilatasyon ve venüler sızıntı yapar."
                },
                {
                    "text": "Antihistaminikler kompleman sistemini doğrudan uyararak ödemi artırır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Antihistaminiklerin kompleman aktivasyonu ile ilişkisi yoktur."
                }
            ]
        ),
        12: make_branching_logic(
            "65 yaşında osteoartrit tanılı, geçmişinde mide ülseri perforasyonu öyküsü bulunan hastaya diz ağrısı için analjezik tedavi planlanmaktadır.",
            "Gastrointestinal kanama riskini en aza indirmek için eikozanoid farmakolojisine göre hangi yaklaşım en uygundur?",
            [
                {
                    "text": "Selektif COX-2 inhibitörü (selekoksib) bir proton pompa inhibitörü ile kombine edilerek verilmelidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Mide mukozasını koruyan PGE2 sentezi COX-1 kaynaklıdır; selektif COX-2 inhibitörleri mideyi korur ancak kardiyovasküler risk açısından takip gerekir."
                },
                {
                    "text": "Yüksek doz non-selektif indometazin başlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. İndometazin en güçlü COX-1 inhibitörlerinden biridir ve ciddi ülser/kanama riski taşır."
                },
                {
                    "text": "Sadece aspirin verilip başka önlem alınmamalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Aspirin kovalent COX-1 inhibisyonu ile gastrik mukozal bariyeri yıkar."
                }
            ]
        ),
        15: make_branching_logic(
            "Kardiyovasküler aterosklerotik hastalığı olan bir bireyde endotel kaynaklı Prostasiklin (PGI2) ile trombosit kaynaklı Tromboksan A2 (TXA2) arasındaki biyolojik denge araştırılmaktadır.",
            "Trombosit agregasyonunu ve vazokonstriksiyonu engelleyerek damar içi pıhtılaşmayı önleyen fizyolojik eikozanoid dengesi nasıldır?",
            [
                {
                    "text": "Endotel kaynaklı PGI2 trombosit kümeleşmesini ve vazokonstriksiyonu inhibe ederken, TXA2 kümeleşmeyi uyarır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. PGI2 vazodilatatör ve anti-agregan iken, TXA2 güçlü vazokonstriktör ve agregandır; denge hemostazı belirler."
                },
                {
                    "text": "TXA2 trombosit agregasyonunu durdurur, PGI2 ise pıhtıyı tetikler.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bu rollerin tam tersidir."
                },
                {
                    "text": "Hem TXA2 hem de PGI2 trombositleri tamamen inaktive eder.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Birbirine zıt (antagonist) çalışan iki temel moleküldür."
                }
            ]
        ),
        22: make_branching_logic(
            "Şiddetli bronşiyal astım atağı geçiren 12 yaşındaki çocukta hava yollarında aşırı mukus salgısı, epitel dökülmesi ve yoğun bronkokonstriksiyon saptanıyor.",
            "Histaminden 1000 kat daha güçlü ve uzun süreli bronkospazm oluşturan sisteinil lökotrienlerin sentezini durdurmak için hangi enzimin hedeflenmesi gerekir?",
            [
                {
                    "text": "5-Lipoksijenaz (5-LOX) enzimi zileuton gibi ajanlarla hedeflenmelidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Araşidonik asitten lökotrien (LTC4, LTD4, LTE4) sentezindeki kilit enzim 5-lipoksijenazdır."
                },
                {
                    "text": "Siklooksijenaz-1 enzimi hedeflenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. COX inhibisyonu araşidonik asidi lipoksijenaz yolağına kaydırarak astımı daha da kötüleştirebilir."
                },
                {
                    "text": "Tromboksan sentaz enzimi hedeflenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Tromboksan sentaz bronkospazmdan sorumlu majör enzim değildir."
                }
            ]
        ),
        26: make_branching_logic(
            "Nazal polip ve astımı olan 35 yaşındaki hasta baş ağrısı nedeniyle 500 mg aspirin aldıktan 20 dakika sonra şiddetli nefes darlığı, siyanoz ve hırıltı krizi ile acile başvuruyor (Samter Triadı / AERD).",
            "Bu reaksiyonun gelişmesindeki temel patofizyolojik mekanizma nedir?",
            [
                {
                    "text": "COX inhibisyonu sonucu araşidonik asit 5-LOX yolağına kayarak aşırı bronkokonstriktör lökotrien (LTC4, LTD4, LTE4) üretimine yol açmıştır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Aspirin COX'u bloke edince araşidonik asit şant yaparak sisteinil lökotrien patlamasına neden olur."
                },
                {
                    "text": "Aspirine karşı gelişen Tip I IgE aracılı anafilaksi tablosudur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bu bir immünolojik alerji değil, farmakolojik enzim kayması (şant) tablosudur."
                },
                {
                    "text": "Aspirin histamin reseptörlerini doğrudan uyararak bronkospazm yapmıştır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Mekanizma histamin reseptör agonizması değil, lökotrien artışıdır."
                }
            ]
        ),
        32: make_branching_logic(
            "Gram-negatif bakteriyemiye bağlı septik şok tablosundaki hastada lökositlerden ve makrofajlardan masif oranda TNF-α salgılanmaktadır.",
            "Sistemik dolaşımda aşırı yüksek konsantrasyona ulaşan TNF-alfa'nın miyokard ve vasküler yatak üzerindeki en ölümcül etkisi nedir?",
            [
                {
                    "text": "Miyokard kontraktilitesini deprese eder, sistemik vasküler rezistansı düşürür ve yaygın kapiller kaçışa yol açar.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Yüksek doz TNF kardiyak debiyi düşürür ve ağır vazodilatasyonla refrakter septik şoka neden olur."
                },
                {
                    "text": "Koroner vazokonstriksiyon yaparak hipertansif krize yol açar.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. TNF hipertansiyon değil derin hipotansiyon ve şok yapar."
                },
                {
                    "text": "Karaciğerde glikojen depolanmasını aşırı artırarak hiperglisemi yapar.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Septik şokta glikoz kullanımı bozulur ve kaşeksiye yol açar."
                }
            ]
        ),
        36: make_branching_logic(
            "Akut pnömonili bir hastada titremeyle birlikte vücut sıcaklığı 39.5°C'ye yükseliyor. Beyin omurilik sıvısında ve hipotalamusta mediyatör değişiklikleri inceleniyor.",
            "Hipotalamik preoptik alanda termostat ayar noktasını yukarı çekerek ateşi başlatan sitokin ve lipid mediyatör çifti hangisidir?",
            [
                {
                    "text": "İnterlökin-1 (veya TNF) uyarısıyla hipotalamik endotelden salınan Prostaglandin E2'dir (PGE2).",
                    "isCorrect": True,
                    "feedback": "Doğrudur. IL-1 ve TNF endojen pirojenlerdir; hipotalamusta COX-2 üzerinden PGE2 sentezleterek termostatı yükseltirler."
                },
                {
                    "text": "İnterlökin-10 ve TGF-beta salınımıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bunlar anti-enflamatuar ve ateşi düşürücü sitokinlerdir."
                },
                {
                    "text": "Histamin ve Bradikinin hipotalamik reseptör uyarımıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Hipotalamustaki primer endojen pirojenik aracı PGE2'dir."
                }
            ]
        ),
        42: make_branching_logic(
            "Tüberküloz şüphesi olan hastanın akciğer biyopsisinde granülomatöz odak, Langhans tipi dev hücreler ve kazeifikasyon nekrozu saptanıyor.",
            "Monositlerin epiteloid histiositlere dönüşmesini ve birleşerek çok çekirdekli dev hücreler oluşturmasını sağlayan en kritik Th1 sitokini hangisidir?",
            [
                {
                    "text": "İnterferon-gama'dır (IFN-γ).",
                    "isCorrect": True,
                    "feedback": "Doğrudur. CD4+ Th1 hücreleri ve NK hücrelerinden salınan IFN-gama klasik makrofaj aktivasyonunun (M1) ve granülom mimarisinin ana motorudur."
                },
                {
                    "text": "İnterlökin-4'tür (IL-4).",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. IL-4 alternatif makrofaj aktivasyonu (M2) ve alerjik yanıttan sorumludur."
                },
                {
                    "text": "İnterlökin-8'dir (CXCL8).",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. IL-8 akut nötrofilik kemotaksiden sorumludur."
                }
            ]
        ),
        46: make_branching_logic(
            "HIV-1 virüsünün hedef CD4+ T hücrelerine ve makrofajlara girişte kemokin reseptörlerini koreseptör olarak kullandığı bilinmektedir.",
            "T-trofik HIV suşlarının T-hücrelerine, M-trofik HIV suşlarının makrofajlara girişte kullandığı kemokin reseptörleri hangileridir?",
            [
                {
                    "text": "T-hücreleri için CXCR4, makrofajlar için CCR5 reseptörleridir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. R5 suşları CCR5'i, X4 suşları CXCR4'ü koreseptör olarak kullanır; CCR5 mutasyonu (CCR5-delta32) HIV direncine yol açar."
                },
                {
                    "text": "Her iki suş için de yalnızca histamin H2 reseptörüdür.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. HIV girişi kemokin reseptörlerine bağımlıdır, histamine değil."
                },
                {
                    "text": "Kompleman CR1 ve CR3 reseptörleridir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. CR1 opsonizasyon reseptörüdür, viral füzyon koreseptörü değildir."
                }
            ]
        ),
        52: make_branching_logic(
            "Tekrarlayan piyojenik akciğer ve sinüzit enfeksiyonları geçiren 6 yaşındaki çocukta serum kompleman düzeyleri inceleniyor ve homozigot C3 eksikliği saptanıyor.",
            "Bu çocukta tekrarlayan bakteriyel enfeksiyonların altında yatan temel immünolojik kusur nedir?",
            [
                {
                    "text": "C3b oluşamadığı için bakterilerin opsonizasyonu ve fagositozu ağır derecede kusurludur.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. C3 tüm yolların kesişim noktasıdır; C3b yokluğunda opsonizasyon ve C5 konvertaz oluşumu durur."
                },
                {
                    "text": "Nötrofillerin integrin molekülleri sentezlenemez.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bu LAD-1 sendromudur, komplemanla doğrudan ilişkili değildir."
                },
                {
                    "text": "Plazma hücreleri antikor sentezleyemez.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Antikor sentezi kompleman eksikliğinde normal kalabilir."
                }
            ]
        ),
        56: make_branching_logic(
            "19 yaşında üniversite öğrencisi, hayatında üçüncü kez Neisseria meningitidis menenjiti atağı geçirerek yoğun bakıma yatırılıyor.",
            "Neisseria türlerine karşı aşırı duyarlılıkla karakterize olan ve terminal litik kompleman fonksiyonunu bozan genetik defekt hangisidir?",
            [
                {
                    "text": "Membran Atak Kompleksi (C5b-9) bileşenlerinden birinin konjenital eksikliğidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Kapsüllü ince zarlı Neisseria bakterilerinin lizisi için sağlam C5, C6, C7, C8 veya C9 (MAC) varlığı şarttır."
                },
                {
                    "text": "Mannoz bağlayan lektin (MBL) fazlalığıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. MBL fazlalığı menenjit yatkınlığı yapmaz."
                },
                {
                    "text": "Faktör I aşırı ekspresyonudur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Faktör I inhibitör bir proteindir, terminal yol eksikliği primer Neisseria risk faktörüdür."
                }
            ]
        ),
        62: make_branching_logic(
            "28 yaşında kadın hasta, diş çekimi sonrasında dudaklarda, dilde ve farenkste kaşıntısız, ürtikersiz, basmakla gode bırakmayan masif anjiyoödem ile başvuruyor. Geçmişte de benzer tekrarlayan karın ağrısı atakları olduğu öğreniliyor.",
            "C1 esteraz inhibitör (C1-INH) eksikliğine bağlı Herediter Anjiyoödem tanısı konan bu hastada ödemin baş sorumlusu mediyatör ve acil hedef ilaç hangisidir?",
            [
                {
                    "text": "Baş sorumlu Bradikinindir; tedavisinde bradikinin B2 reseptör blokeri İkatibant veya C1-INH konsantresi verilir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. C1-INH kallikrein ve Faktör XIIa'yı baskılayamazsa aşırı bradikinin birikir; antihistaminik ve kortizona yanıt vermez."
                },
                {
                    "text": "Baş sorumlu Histamindir; yüksek doz H1 bloker ile tamamen geriler.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Herediter anjiyoödem histaminik değil bradikininerjiktir, antihistaminiklere yanıtsızdır."
                },
                {
                    "text": "Baş sorumlu TNF-alfadır; acilen anti-TNF antikor verilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. HAE patogenezi kallikrein-kinin yolağı bozukluğudur."
                }
            ]
        ),
        66: make_branching_logic(
            "Sabahları koyu renkli idrar yapma (gece hemolizi) ve tromboz atakları olan hastanın eritrosit akım sitometrisinde CD55 (DAF) ve CD59 (MIRL) proteinlerinin eksik olduğu tespit ediliyor.",
            "Paroksismal Noktürnal Hemoglobinüri (PNH) tablosundaki bu hastada eritrositlerin kompleman litik lizisinden korunması için hangi biyolojik tedavi endikedir?",
            [
                {
                    "text": "Anti-C5 monoklonal antikoru Ekulizumab verilerek C5b-9 oluşumu durdurulmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Ekulizumab C5 bölünmesini engelleyerek CD59 yokluğunda savunmasız kalan eritrositlerin intravasküler parçalanmasını önler."
                },
                {
                    "text": "Hastaya acil splenektomi yapılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. PNH'de hemoliz dalakta değil komplemanla damar içinde (intravasküler) gerçekleşir."
                },
                {
                    "text": "H1 antihistaminik başlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kompleman hemolizinde antihistaminiklerin hiçbir rolü yoktur."
                }
            ]
        ),
        74: make_branching_logic(
            "Septik şoktaki bir hastada endotel hücreleri ve makrofajlarda iNOS enziminin aşırı indüklenmesiyle litrelerce mikromolar düzeyde nitrik oksit (NO) sentezlenmektedir.",
            "Aşırı NO üretiminin damar düz kas hücresinde uyardığı ikinci haberci sistem ve sonuçtaki hemodinamik değişiklik hangisidir?",
            [
                {
                    "text": "Guanilat siklazı uyararak cGMP düzeyini artırır; aşırı vazodilatasyon ve vazopressörlere dirençli şok tablosu yaratır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. NO çözünür guanilat siklazı aktive ederek GTP'yi cGMP'ye çevirir; düz kas gevşer ve derin refrakter hipotansiyon gelişir."
                },
                {
                    "text": "Adenilat siklazı inhibe ederek cAMP'yi düşürür ve hipertansiyon yapar.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. NO vazokonstriktör değil güçlü vazodilatatördür ve cGMP yoluyla etkir."
                },
                {
                    "text": "Kalsiyum girişini artırarak damar spazmına yol açar.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. NO düz kasta kalsiyum duyarlılığını azaltarak gevşeme sağlar."
                }
            ]
        )
    }

def get_extra_chains():
    """Causal chain oranını artırmak için hedeflenen slaytlara eklenecek zincirler."""
    return {
        13: make_causal_chain(
            "Aspirinin Trombositte TXA2 Sentezini İnhibe Etme Mekanizması",
            [
                "1. Kovalent Asetilasyon: Aspirin trombosit COX-1 enziminin Serin 529 kalıntısını kovalent olarak asetiller.",
                "2. Geri Dönüşümsüz Blokaj: Trombosit enzimatik aktif bölgesi kalıcı olarak tıkanır ve PGH2 sentezi durur.",
                "3. Çekirdeksizlik Faktörü: Çekirdeği olmayan trombosit yeni COX enzimi sentezleyemez.",
                "4. Yaşam Boyu Baskı: Trombositin 7-10 günlük dolaşım ömrü boyunca TXA2 üretimi tamamen felç olur."
            ]
        ),
        55: make_causal_chain(
            "Kompleman Membran Atak Kompleksi (MAC) Montaj Zinciri",
            [
                "1. C5b Oluşumu: C5 konvertaz C5 proteinini parçalayarak labil C5b parçasını açığa çıkarır.",
                "2. C6 ve C7 Katılımı: C5b sırasıyla C6 ve C7'yi bağlar; hidrofobik bölgeleriyle hedef zara tutunur.",
                "3. C8 Entegrasyonu: C8 komplekse eklenerek hedef lipid çift tabakasının içine saplanır.",
                "4. Çoklu C9 Polimerizasyonu: 10-16 adet C9 molekülü halka şeklinde polimerleşerek zarda 10 nm por açar.",
                "5. Osmotik Lizis: Pordan su ve iyonlar içeri hücum ederek bakteriyi ya da hedef hücreyi patlatır."
            ]
        )
    }

def get_extra_sliders():
    """Before-after slider oranını artırmak için hedeflenen slaytlara eklenecek sliderlar."""
    return {
        3: make_before_after(
            "Histamin H1 vs H2 Reseptörlerinin Fonksiyonel Karşılaştırması",
            "H1 Reseptörü (Enflamasyon ve Alerji)",
            "Bronşlarda kasılma, venüllerde endotel kontraksiyonu ile permeabilite artışı ve kaşıntı/ağrı iletimi yapar.",
            "H2 Reseptörü (Gastrik ve Kardiyak)",
            "Mide pariyetal hücrelerinden hidroklorik asit (HCl) salgılanmasını uyarır ve kalp atım hızını artırır."
        ),
        53: make_before_after(
            "Kompleman Klasik Yol vs Alternatif Yol Karşılaştırması",
            "Klasik Kompleman Yolu",
            "Antijen-antikor (IgM veya IgG) komplekslerine C1q'nun bağlanmasıyla başlar; edinsel bağışıklığa bağımlıdır.",
            "Alternatif Kompleman Yolu",
            "Antikor gerektirmeden doğrudan mikrobiyal polisakkaritler ve C3 spontan hidrolizi (tick-over) ile başlar."
        )
    }

def get_extra_tables():
    """Interactive table oranını artırmak için hedeflenen slaytlara eklenecek tablolar."""
    return {
        24: make_table(
            ["Lökotrien Tipi", "Temel Hücresel Kaynak", "Başlıca Biyolojik Görevi"],
            [
                [
                    {"text": "Lökotrien B4 (LTB4)", "isMasked": False, "hint": ""},
                    {"text": "Nötrofiller ve Makrofajlar", "isMasked": False, "hint": ""},
                    {"text": "Güçlü nötrofil kemotaksisi ve lizozomal enzim salınımı", "isMasked": True, "hint": "Nötrofilleri enflamasyon odağına çeken aktivite"}
                ],
                [
                    {"text": "Sisteinil Lökotrienler (LTC4, LTD4, LTE4)", "isMasked": False, "hint": ""},
                    {"text": "Mast hücreleri ve Eozinofiller", "isMasked": True, "hint": "Alerjik granülositler ve doku mastositleri"},
                    {"text": "Şiddetli bronkokonstriksiyon ve artmış damar geçirgenliği", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Lipoksin A4 (LXA4)", "isMasked": True, "hint": "Trombosit-lökosit etkileşimiyle sentezlenen antienflamatuar lipid"},
                    {"text": "Lökosit-Trombosit transselüler sentezi", "isMasked": False, "hint": ""},
                    {"text": "Nötrofil adezyonunu engelleme ve rezolüsyon", "isMasked": False, "hint": ""}
                ]
            ]
        ),
        44: make_table(
            ["Sitokin Grubu", "Anahtar Sitokinler", "Temel Enflamatuar Fonksiyon"],
            [
                [
                    {"text": "Akut Doğal Sitokinler", "isMasked": False, "hint": ""},
                    {"text": "TNF-α, IL-1, IL-6", "isMasked": True, "hint": "Endotel aktivasyonu ve ateş yapan klasik üçlü"},
                    {"text": "Endotel yapışması, ateş ve karaciğer akut faz yanıtı", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Th1 Adaptif Sitokinleri", "isMasked": False, "hint": ""},
                    {"text": "İnterferon-gama (IFN-γ), IL-12", "isMasked": False, "hint": ""},
                    {"text": "Klasik makrofaj (M1) aktivasyonu ve granülom bütünlüğü", "isMasked": True, "hint": "Epiteloid histiosit oluşumu"}
                ],
                [
                    {"text": "Anti-enflamatuar Sitokinler", "isMasked": True, "hint": "Enflamasyonu söndüren düzenleyici grup"},
                    {"text": "İnterlökin-10 (IL-10), TGF-β", "isMasked": False, "hint": ""},
                    {"text": "Makrofaj baskılanması, fibroblast uyarımı ve doku tamiri", "isMasked": False, "hint": ""}
                ]
            ]
        ),
        64: make_table(
            ["Kinin Sistemi Elemanı", "Biyokimyasal Rolü", "Enflamasyondaki Etkisi"],
            [
                [
                    {"text": "Hageman Faktörü (FXIIa)", "isMasked": False, "hint": ""},
                    {"text": "Prekallikreini aktif kallikreine çevirir", "isMasked": True, "hint": "Kallikrein aktivasyon enzimi"},
                    {"text": "Pıhtılaşma ve kinin sisteminin ortak başlangıç tetiği", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Plazma Kallikreini", "isMasked": True, "hint": "HMWK'dan bradikinin koparan serin proteaz"},
                    {"text": "Yüksek molekül ağırlıklı kininojenden bradikinin koparır", "isMasked": False, "hint": ""},
                    {"text": "Faktör XII'yi pozitif geri bildirimle daha da uyarır", "isMasked": False, "hint": ""}
                ],
                [
                    {"text": "Bradikinin", "isMasked": False, "hint": ""},
                    {"text": "B2 reseptörlerine bağlanır", "isMasked": False, "hint": ""},
                    {"text": "Arterioler dilatasyon, venüler sızıntı ve nosiseptif ağrı", "isMasked": True, "hint": "Ödem ve sinir ucu uyarımı"}
                ]
            ]
        )
    }

def enrich_slides(slides):
    """Slayt listesini alır ve eklenen elemanlarla zenginleştirip dengeli olarak geri döndürür."""
    branching_map = get_extra_branching()
    chain_map = get_extra_chains()
    slider_map = get_extra_sliders()
    table_map = get_extra_tables()

    for idx, slide in enumerate(slides, start=1):
        if idx in branching_map:
            slide["elements"].append(branching_map[idx])
        if idx in chain_map:
            slide["elements"].append(chain_map[idx])
        if idx in slider_map:
            slide["elements"].append(slider_map[idx])
        if idx in table_map:
            slide["elements"].append(table_map[idx])

    return slides
