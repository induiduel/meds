# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 6: Homolog Rekombinasyon Kusurları ve BRCA Biyolojisi (Slayt 51 - 60)
Checkpoint: Slayt 59
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_6_slides():
    return [
        # Slayt 51
        {
            "slideNumber": 51,
            "title": "DNA Çift İplik Kırıkları (DSB): En Tehlikeli Lezyon",
            "content": (
                "DNA molekülünde meydana gelen hasarlar arasında hücre sağkalımı ve genomik kararlılık açısından "
                "en ölümcül olanı **DNA çift iplik kırıklarıdır (Double-Strand Breaks - DSB)**. Tek iplik lezyonlarında "
                "karşı iplik sağlam bir kalıp (şablon) vazifesi görerek hatasız onarımı mümkün kılarken; her iki "
                "fosfodiester zincirinin aynı noktadan koptuğu DSB lezyonlarında referans kalıp kalmaz. Çift iplik "
                "kırıkları en sık iyonlaştırıcı radyasyon (X ve gama ışınları), reaktif oksijen radikalleri (ROS), "
                "kemoterapötik topoizomeraz inhibitörleri ve replikasyon çatallarının çökmesi sonucu meydana gelir. "
                "Hücre bu kritik lezyonları restore etmek için iki ana onarım mekanizması geliştirmiştir: **Homolog "
                "Rekombinasyon (HR)** ve **Homolog Olmayan Uç Birleştirme (NHEJ)**."
            ),
            "elements": [
                make_cloze(
                    "İyonize radyasyon ve serbest radikallerin yol açtığı en tehlikeli ölümcül nükleik asit hasarı çift iplik kırıklarıdır.",
                    "çift",
                    "İkili zincir kopması niteliği"
                ),
                make_active_recall(
                    "Tek iplik hasarlarının aksine çift iplik kırıklarının hücresel tamirini son derece zorlaştıran temel biyolojik neden nedir?",
                    "Kopma noktasında sağlam bir karşı kalıp (şablon) ipliğin bulunmamasıdır.",
                    "Replikatif referans kılavuzunun yokluğu"
                )
            ]
        },

        # Slayt 52
        {
            "slideNumber": 52,
            "title": "Homolog Rekombinasyon vs NHEJ Yolağı",
            "content": (
                "Hücre çift iplik kırığını tamir ederken hücre siklusunun evresine göre iki alternatif yoldan birini "
                "seçer. **Homolog Olmayan Uç Birleştirme (NHEJ)**, G1 evresinde ve bölünmeyen hücrelerde kullanılır; "
                "kopan iki DNA ucu Ku70/Ku80 ve DNA-PK kompleksi ile doğrudan birbirine yapıştırılır. NHEJ kalıp "
                "kullanmadığı için son derece **hataya yatkındır (error-prone)**; nükleotid kayıplarına ve translokasyonlara "
                "neden olabilir. Buna karşılık **Homolog Rekombinasyon (HR)**, S ve G2 evrelerinde kromatidler replike "
                "olduktan sonra devreye girer. Kardeş kromatidi sağlam bir şablon olarak kullanarak kırığı **hatasız "
                "(error-free)** ve mükemmel bir sadakatle onarır. Homolog rekombinasyonun merkezinde **BRCA1, "
                "BRCA2, RAD51 ve PALB2** proteinleri görev yapar."
            ),
            "elements": [
                make_table(
                    "Homolog Rekombinasyon (HR) ile NHEJ Karşılaştırması",
                    ["Parametre", "Homolog Rekombinasyon (HR)", "Homolog Olmayan Uç Birleştirme (NHEJ)"],
                    [
                        {
                            "cells": ["Aktif Olduğu Siklus Fazı", "S ve G2 evresi (Kardeş kromatid varlığında)", "G1 ve tüm evreler (Kalıp aranmaz)"],
                            "hiddenIndex": 1,
                            "hint": "Replikasyon sonrası çift iplik fazları"
                        },
                        {
                            "cells": ["Onarım Sadakati", "Hatasız (Error-free, tam korunum)", "Hataya son derece yatkın (Error-prone)"],
                            "hiddenIndex": 1,
                            "hint": "Kusursuz şablonlu tamir kalitesi"
                        },
                        {
                            "cells": ["Kilit Protein Ekibi", "BRCA1, BRCA2, RAD51, PALB2", "Ku70, Ku80, DNA-PKcs, DNA Ligaz IV"],
                            "hiddenIndex": 1,
                            "hint": "Meme ve over tümör baskılayıcıları"
                        }
                    ]
                ),
                make_cloze(
                    "Kardeş kromatidi şablon olarak kullanarak çift iplik kırıklarını hatasız onaran mekanizma homolog rekombinasyon mekanizmasıdır.",
                    "homolog",
                    "Eşlenik dizi benzerliği temelli tamir"
                )
            ]
        },

        # Slayt 53
        {
            "slideNumber": 53,
            "title": "BRCA1 ve BRCA2 Genlerinin Moleküler Biyolojisi",
            "content": (
                "**BRCA1 (17q21)** ve **BRCA2 (13q12)**, homolog rekombinasyon yolağının koordinatör tümör "
                "baskılayıcı genleridir. BRCA1 çok fonksiyonlu bir nükleer bekçidir; ATM/ATR kinazları tarafından "
                "fosforillenerek DNA hasar yanıtını başlatır, hücre siklusunu G2-M kontrol noktasında durdurur ve "
                "onarım kompleksini kırık bölgesine çağırır. BRCA2 ise daha spesifik bir role sahiptir; homolog "
                "rekombinasyonun icracı nükleoproteini olan **RAD51'e** doğrudan bağlanır ve RAD51 moleküllerini tek "
                "iplikli DNA kuyruklarına yükleyerek nükleoprotein flamentlerinin oluşmasını sağlar; bu flamentler "
                "sağlam kardeş kromatidi tarayarak iplik invazyonunu (strand invasion) gerçekleştirir. Bu genlerdeki "
                "işlev kaybı, hücreyi çift iplik kırıklarında hataya açık NHEJ yoluna mahkum eder."
            ),
            "elements": [
                make_causal_chain(
                    "BRCA Aracılı Homolog Rekombinasyonel Tamir Zinciri",
                    [
                        "1. DSB Sensör Aktivasyonu: Çift iplik kırığı MRN kompleksi ve ATM kinazı tarafından tespit edilir.",
                        "2. BRCA1 Nükleer Odaklanması: Fosforillenen BRCA1 BARD1 ile birleşerek kırık odağına hızla göç eder.",
                        "3. Uç Rezeksiyonu: DNA uçları 5'→3' yönünde tıraşlanarak tek iplikli 3' çıkıntılı kuyruklar hazırlanır.",
                        "4. RAD51 Yüklenmesi: BRCA2 ve PALB2 eskortluğunda RAD51 rekombinazı tek iplikli kuyruğa dizilir.",
                        "5. İplik İnvazyonu ve Sentez: RAD51 kardeş kromatide dalarak sağlam diziyi kopyalar ve hatasız ligasyon yapılır."
                    ]
                ),
                make_active_recall(
                    "Homolog rekombinasyonda BRCA2 tarafından tek iplikli DNA'ya yüklenerek iplik invazyonunu yürüten temel rekombinaz enzimi hangisidir?",
                    "RAD51 rekombinaz proteinidir.",
                    "Rekombinasyon icracı nükleoproteini"
                )
            ]
        },

        # Slayt 54
        {
            "slideNumber": 54,
            "title": "Kalıtsal Meme ve Over Kanseri Sendromu",
            "content": (
                "BRCA1 ve BRCA2 genlerindeki germline mutasyonlar otozomal dominant kalıtılır ve **Kalıtsal Meme "
                "ve Over Kanseri Sendromunun (HBOC)** etiyolojik temelini oluşturur. Tüm kalıtsal meme kanserlerinin "
                "yaklaşık %50-70'i bu iki genin inaktivasyonuna bağlıdır. **BRCA1 mutasyonu** taşıyan kadınlarda yaşam "
                "boyu meme kanseri riski %65-85, epitelyal over karsinomu (özellikle yüksek dereceli seröz karsinom) "
                "riski ise %40-50 düzeyindedir. **BRCA2 mutasyonu** taşıyıcılarında ise meme kanseri riski %45-70, "
                "over kanseri riski %15-25 civarındadır. Ayrıca BRCA2 mutasyonları erkeklerde dramatik şekilde "
                "**erkek meme kanseri** (riskte ~100 kat artış), agresif **prostat kanseri**, pankreas adenokarsinomu "
                "ve malign melanom riskini yükseltir."
            ),
            "elements": [
                make_table(
                    "BRCA1 ile BRCA2 Kalıtsal Kanser Risk Profili Karşılaştırması",
                    ["Genetik Parametre", "BRCA1 Germline Mutasyonu", "BRCA2 Germline Mutasyonu"],
                    [
                        {
                            "cells": ["Kromozomal Konum", "17q21 lokusu", "13q12 lokusu"],
                            "hiddenIndex": 2,
                            "hint": "On üç numaralı kromozom"
                        },
                        {
                            "cells": ["Yaşam Boyu Over Ca Riski", "Yüksek (%40-50)", "Orta-Yüksek (%15-25)"],
                            "hiddenIndex": 1,
                            "hint": "Yarıya yakın over karsinomu riski"
                        },
                        {
                            "cells": ["Erkek Maligniteleri", "Düşük erkek meme kanseri riski", "Yüksek erkek meme ve prostat kanseri riski"],
                            "hiddenIndex": 2,
                            "hint": "Pektoral gland ve pelvik organ neoplazisi yatkınlığı"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Erkeklerde meme kanseri ve agresif prostat karsinomu riskini en çarpıcı şekilde artıran kalıtsal DNA onarım geni mutasyonu hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "BRCA2 germline mutasyonu",
                            "isCorrect": True,
                            "explanation": "BRCA2 erkek meme kanserlerinin en sık kalıtsal nedenidir ve agresif prostat kanseri riskini katlar."
                        },
                        {
                            "key": "B",
                            "text": "APC germline mutasyonu",
                            "isCorrect": False,
                            "explanation": "APC familyal adenomatöz polipozis (FAP) nedenidir."
                        },
                        {
                            "key": "C",
                            "text": "MSH2 germline mutasyonu",
                            "isCorrect": False,
                            "explanation": "MSH2 Lynch sendromu nedenidir."
                        },
                        {
                            "key": "D",
                            "text": "RET onkogen mutasyonu",
                            "isCorrect": False,
                            "explanation": "RET mutasyonu MEN-2 sendromu ve medüller tiroid kanserine yol açar."
                        }
                    ],
                    "Erkek meme kanserinin en önemli kalıtsal belirteci BRCA2 mutasyonudur."
                )
            ]
        },

        # Slayt 55
        {
            "slideNumber": 55,
            "title": "BRCA Tümörlerinin Histopatolojik Fenotipi",
            "content": (
                "BRCA1 ilişkili meme kanserleri, sporadik meme kanserlerinden morfolojik ve immünofenotipik olarak "
                "belirgin farklılıklar gösterir. Bu karsinomlar tipik olarak **üçlü negatif (triple-negative)** "
                "fenotiptedir; yani östrojen reseptörü [ER(-)], progesteron reseptörü [PR(-)] ve HER2/neu [HER2(-)] "
                "ekspresyonundan tamamen yoksundurlar. Histopatolojik incelemede yüksek nükleer grade, solid büyüme "
                "paterni, itici (pushing) sınırlar, santral geniş nekroz alanları ve yoğun **tümör infiltre eden "
                "lenfositik stroma (medüller benzeri histoloji)** izlenir. Bu tümörler hormonal tedavilere (tamoksifen, "
                "aromataz inhibitörleri) ve Trastuzumab'a yanıt vermezler; ancak DNA çapraz bağlayıcı kemoterapötiklere "
                "(sisplatin, karboplatin) ve PARP inhibitörlerine son derece duyarlıdırlar."
            ),
            "elements": [
                make_before_after(
                    "Klasik Luminal Meme Kanseri vs BRCA1 Üçlü Negatif Karsinom",
                    "Luminal Meme Karsinomu (Sporadik)",
                    "ER(+), PR(+), iyi-orta diferansiye tübüler glandüler yapılar, desmoplastik stroma, düşük lenfosit infiltrasyonu.",
                    "BRCA1 İlişkili Üçlü Negatif Karsinom",
                    "ER(-), PR(-), HER2(-), anaplastik solid tabakalar, medüller benzeri pushing sınır, santral nekroz ve yoğun TIL infiltrasyonu.",
                    "Hormonal reseptör yokluğu endokrin tedaviyi engellerken, homolog rekombinasyon kusuru DNA hasarlayıcı ilaçlara duyarlılık yaratır."
                ),
                make_cloze(
                    "BRCA1 mutasyonlu meme karsinomları östrojen, progesteron ve HER2 ekspresyonu içermediği için üçlü negatif olarak tanımlanır.",
                    "negatif",
                    "Üç reseptörün de bulunmama durumu"
                )
            ]
        },

        # Slayt 56
        {
            "slideNumber": 56,
            "title": "Homolog Rekombinasyon Kusurlu Diğer Sendromlar",
            "content": (
                "Homolog rekombinasyon ve DNA çift iplik kırığı onarım yolağındaki kusurlar, BRCA dışında iyi "
                "tanımlanmış nadir kalıtsal sendromlara da yol açar. **Fanconi Anemisi (FA)**, en az 22 farklı FANC "
                "genindeki (FANCD2, FANCA vb. ve BRCA2/FANCD1) mutasyonlarla gelişir; DNA çapraz bağlayıcı ajanlara "
                "(mitomisin C, diepoksibütan) aşırı duyarlılık, kemik iliği yetmezliği (aplastik anemi), radius "
                "hipoplazisi ve akut miyeloid lösemi (AML) riski ile seyreder. **Ataksi-Telanjiektazi (AT)**, "
                "çift iplik kırıklarının birincil sensör kinazı olan **ATM geninin** inaktivasyonuna bağlıdır; "
                "progresif serebellar ataksi, okülokutanöz telanjiektaziler, iyonize radyasyona aşırı duyarlılık "
                "ve lenfoma/lösemi gelişimi ile karakterizedir. **Bloom Sendromunda** ise DNA helikazı kodlayan "
                "**BLM gen kusuru** aşırı kardeş kromatid değişimi (SCE) ve yaygın malignitelere yol açar."
            ),
            "elements": [
                make_table(
                    "Homolog Rekombinasyon İlişkili Genetik Kararsızlık Sendromları",
                    ["Sendrom Adı", "Kusurlu Gen / Protein", "Karakteristik Klinik Triad", "Gelişen Maligniteler"],
                    [
                        {
                            "cells": ["Fanconi Anemisi", "FANC gen kompleksi (BRCA2)", "Kemik iliği aplazisi, başparmak/radius anomalisi, hiperpigmentasyon", "AML ve skuamöz karsinomlar"],
                            "hiddenIndex": 1,
                            "hint": "Kemik iliği yetmezliği yapan onarım genleri"
                        },
                        {
                            "cells": ["Ataksi-Telanjiektazi", "ATM kinaz geni (11q22)", "Serebellar ataksi, gözde telanjiektaziler, radyasyon duyarlılığı", "Lösemi ve lenfomalar"],
                            "hiddenIndex": 1,
                            "hint": "DSB lezyonlarını algılayan ana sensör enzim"
                        },
                        {
                            "cells": ["Bloom Sendromu", "BLM (RecQ DNA helikaz)", "Güneş hassasiyeti, kelebek döküntü, cücelik", "Tüm organ kanserleri ve lösemi"],
                            "hiddenIndex": 1,
                            "hint": "DNA sarmal açıcı enzim kusuru"
                        }
                    ]
                ),
                make_active_recall(
                    "İyonlaştırıcı radyasyona aşırı hücresel duyarlılık, serebellar ataksi ve telanjiektazilerle seyreden sendromda kusurlu olan sensör kinaz geni hangisidir?",
                    "ATM kinaz genidir (Ataxia Telangiectasia Mutated).",
                    "Çift iplik kırığı algılayıcı nükleer protein"
                )
            ]
        },

        # Slayt 57
        {
            "slideNumber": 57,
            "title": "Sentetik Letalite ve PARP İnhibisyonu",
            "content": (
                "**Sentetik letalite**, iki ayrı genetik bozukluğun tek başlarına hücre için öldürücü olmamasına "
                "karşın, aynı hücrede eş zamanlı bir araya geldiklerinde kaçınılmaz hücresel ölüme yol açması "
                "prensibidir. Kanser tedavisinde bunun en mükemmel uygulaması **PARP (Poli-ADP Riboz Polimeraz) "
                "inhibitörleridir (Olaparib, Rucaparib, Talazoparib)**. Normal hücrelerde her gün oluşan on binlerce "
                "DNA tek iplik kırığı PARP enzimi tarafından onarılır. PARP ilacıyla bloke edildiğinde tek iplik "
                "kırıkları tamir edilemez ve replikasyon çatalının çökmesiyle çift iplik kırıklarına dönüşür. Normal "
                "hücrelerde sağlam BRCA/HR sistemi bu kırıkları tamir eder ve hücre yaşar. Ancak **BRCA mutant "
                "tümör hücresinde** hem tek iplik onarımı (ilaçla) hem de çift iplik onarımı (genetik kusurla) felç "
                "olduğu için kanser hücresi seçici olarak apoptoza sürüklenir; normal dokular ise zarar görmez."
            ),
            "elements": [
                make_causal_chain(
                    "BRCA Mutant Kanser Hücrelerinde PARP Sentetik Letalite Kaskadı",
                    [
                        "1. PARP Blokajı: Olaparib PARP-1 enzimini DNA tek iplik kırık lezyonları üzerine kilitler.",
                        "2. Replikasyon Çöküşü: İlerleyen DNA replikasyon çatalı bloke PARP'a çarparak çift iplik kırığına döner.",
                        "3. HR Tamir Yetersizliği: Kanser hücresinde BRCA1/2 genleri inaktif olduğundan kırıklar tamir edilemez.",
                        "4. Kaotik Uç Birleştirme: Hücre çaresizce hataya yatkın NHEJ'e başvurur; devasa kromozomal kırıklar oluşur.",
                        "5. Seçici Apoptoz (Sentetik Letalite): Normal hücreler sağlam BRCA ile yaşarken kanser hücresi seçici olarak ölür."
                    ]
                ),
                make_cloze(
                    "İki ayrı genetik veya farmakolojik yetersizliğin birleşerek kanser hücresini seçici olarak öldürmesi prensibine sentetik letalite adı verilir.",
                    "letalite",
                    "Birlikte ölüm getiren biyolojik mekanizma"
                )
            ]
        },

        # Slayt 58
        {
            "slideNumber": 58,
            "title": "Platin Duyarlılığı ve Edinsel Direnç Mutasyonları",
            "content": (
                "Homolog rekombinasyon kusuru taşıyan (BRCA eksikliği veya HRD pozitif) tümörler, DNA iplikleri "
                "arasında kovalent çapraz bağlar kuran **platin temelli kemoterapötiklere (sisplatin, karboplatin)** "
                "olağanüstü derecede duyarlıdır. Çapraz bağları çözmek için çift iplik kırıkları açılması gerekir "
                "ve BRCA'sız hücre bu kırıkları tamir edemeyerek hızla ölür. Ancak hastalar başlangıçta platin "
                "ve PARP inhibitörlerine tam yanıt verseler dahi, zamanla tümör klonunda **edinsel tedavi direnci** "
                "gelişir. Bu direncin en hayret verici moleküler mekanizması **ikincil geri dönüş (reversion) "
                "mutasyonlarıdır**. Kanser hücresi, ilk mutasyonun okuma çerçevesini bozan frameshift lezyonunun "
                "hemen yanına ikinci bir mikrodelesyon veya mutasyon ekleyerek proteinin okuma çerçevesini yeniden "
                "düzeltir (fonksiyonel BRCA proteinini restore eder); böylece ilaçlara dirençli hale gelir."
            ),
            "elements": [
                make_before_after(
                    "PARP İnhibitörüne Duyarlılık vs Geri Dönüş (Reversion) Direnci",
                    "Tedaviye Duyarlı Evre (Mutant BRCA)",
                    "Frameshift mutasyonu nedeniyle fonksiyonel BRCA üretilemez; PARP inhibitörü veya sisplatin hücreyi hızla apoptoza sokar.",
                    "Dirençli Nüks Evresi (Reversion Mutasyonu)",
                    "Tümör hücresi ek bir somatik delesyonla okuma çerçevesini restore eder; fonksiyonel BRCA proteini yeniden üretilerek direnç kazanılır.",
                    "Reversion mutasyonları kanser genomunun tedavi baskısı altında geliştirdiği olağanüstü klonal plastisiteyi kanıtlar."
                ),
                make_active_recall(
                    "BRCA mutant over veya meme karsinomlarında PARP inhibitörleri ve platine karşı gelişen en önemli direnç mekanizması nedir?",
                    "Kanser hücresinde BRCA geninin açık okuma çerçevesini düzelten ikincil geri dönüş (reversion) mutasyonlarıdır.",
                    "Genetik çerçevenin restorasyonu ile direnç"
                )
            ]
        },

        # Slayt 59: CHECKPOINT 6
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Homolog Rekombinasyon ve BRCA Biyolojisi",
            "content": (
                "Altıncı bölümün bu tekrar sayfasında, DNA çift iplik kırıklarının hatasız tamirini yöneten "
                "homolog rekombinasyon yolağı ve BRCA biyolojisi özetlenmektedir. Çift iplik kırıkları en öldürücü "
                "lezyondur; G1'de hataya açık NHEJ, S/G2'de kardeş kromatidi şablon alan hatasız HR kullanılır. "
                "BRCA1 hasar yanıtını koordine ederken, BRCA2 RAD51'i tek iplikli DNA'ya yükleyerek iplik "
                "invazyonunu yönetir. BRCA1/2 germline mutasyonları Kalıtsal Meme ve Over Kanseri Sendromuna "
                "yol açar; BRCA1 üçlü negatif meme kanserleri ile, BRCA2 ise erkek meme ve prostat kanseri ile "
                "ilişkilidir. PARP inhibitörleri (Olaparib) tek iplik tamirini bloke ederek BRCA mutant hücrelerde "
                "çift taraflı çöküş ve sentetik letalite yaratır; tümör ise reversion mutasyonları ile direnç üretir."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp06-fc01",
                    "front": "Homolog rekombinasyon yolağında tek iplikli DNA kuyruklarına yüklenerek kardeş kromatide iplik invazyonunu gerçekleştiren enzim nedir?",
                    "back": "RAD51 rekombinaz enzimidir.",
                    "hint": "BRCA2 eskortluğundaki nükleoprotein"
                },
                {
                    "id": "k1-29-cp06-fc02",
                    "front": "BRCA mutant homolog rekombinasyon kusuru taşıyan kanser hücrelerinde tek iplik tamirini tıkayarak sentetik letalite oluşturan ilaç grubu nedir?",
                    "back": "PARP inhibitörleridir (Olaparib vb.).",
                    "hint": "Nükleer polimeraz engelleyicileri"
                },
                {
                    "id": "k1-29-cp06-fc03",
                    "front": "BRCA1 mutasyonu taşıyıcılarında gelişen meme karsinomlarının karakteristik immünofenotipik özelliği nedir?",
                    "back": "Üçlü negatif fenotiptir [ER(-), PR(-), HER2(-)].",
                    "hint": "Hormon reseptörleri ve büyüme faktörü yokluğu"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 6 Özet Tablosu: Homolog Rekombinasyon ve BRCA",
                    ["Parametre / Antite", "Moleküler Mekanizma", "Klinik Tedavi / Sonuç"],
                    [
                        {
                            "cells": ["Homolog Rekombinasyon", "Kardeş kromatid şablonlu hatasız DSB tamiri", "BRCA1, BRCA2 ve RAD51 bağımlı süreç"],
                            "hiddenIndex": 0,
                            "hint": "Kusursuz çift zincir onarım mekanizması"
                        },
                        {
                            "cells": ["Sentetik Letalite", "PARP blokajı + BRCA genetik kusuru", "Olaparib ile kanser hücresinin seçici ölümü"],
                            "hiddenIndex": 0,
                            "hint": "İkili yetmezlikle hedeflenen hücre ölümü"
                        }
                    ]
                )
            ]
        },

        # Slayt 60
        {
            "slideNumber": 60,
            "title": "Klinik Karar: BRCA Taşıyıcılarında Risk Yönetimi ve PARP Seçimi",
            "content": (
                "Genetik test sonucunda patojenik germline BRCA1 veya BRCA2 mutasyonu saptanan kadınlarda "
                "risk azaltıcı cerrahi ve profilaksi hayati önem taşır. Meme kanseri riskini %90-95 azaltmak için "
                "hastaya **bilateral profilaktik mastektomi** seçeneği sunulur. Over kanseri için ise erken tarama "
                "yöntemleri (CA-125 ve transvajinal USG) mortaliteyi azaltmadığından, doğurganlığını tamamlamış "
                "kadınlarda 35-40 yaş civarında **bilateral profilaktik salpingo-ooferektomi (RRSO)** standart "
                "öneridir. İnvaziv over veya meme kanseri gelişmiş BRCA mutant hastalarda ise platin bazlı kemoterapiye "
                "yanıt sonrası idame tedavisinde PARP inhibitörlerinin (Olaparib) kullanımı progresyonsuz sağkalımı "
                "iki katından fazla uzatmaktadır."
            ),
            "elements": [
                make_branching_logic(
                    "38 yaşında iki çocuk sahibi kadın hastada genetik analizde patojenik germline BRCA1 mutasyonu saptanıyor. Hastanın over kanseri taraması amacıyla yılda iki kez CA-125 ve pelvik ultrason ile izlenmek istediği öğreniliyor.",
                    "Jinekolojik onkoloji konseyinde bu hastaya sunulması gereken en doğru kılavuz önerisi ve tıbbi gerekçesi ne olmalıdır?",
                    [
                        {
                            "text": "Over kanserinde tarama yöntemleri mortaliteyi düşürmediğinden, doğurganlık tamamlandıysa en geç 40 yaşına kadar bilateral profilaktik salpingo-ooferektomi (RRSO) uygulanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Over kanseri taraması yetersizdir ve erken evrede yakalayamaz. RRSO over kanseri riskini %90'ın üzerinde azaltır."
                        },
                        {
                            "text": "Yalnızca CA-125 takibi yeterlidir; değer yükselmedikçe cerrahiye kesinlikle gerek yoktur.",
                            "isCorrect": False,
                            "explanation": "CA-125 yüksek dereceli seröz karsinomları erken evrede yakalayamaz; mortaliteyi azaltmaz."
                        },
                        {
                            "text": "Profilaktik cerrahi yerine ömür boyu kesintisiz oral antibiyotik kullanılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Antibiyotiğin BRCA ilişkili over karsinogenezinde hiçbir koruyucu rolü yoktur."
                        }
                    ]
                ),
                make_micro_quiz(
                    "BRCA mutant epitelyal over karsinomu tanısı alan bir hastada platin kemoterapisi sonrası idame tedavisinde progresyonsuz sağkalımı uzatan sentetik letalite temelli ajan hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Olaparib (PARP inhibitörü)",
                            "isCorrect": True,
                            "explanation": "Olaparib, homolog rekombinasyon kusurlu BRCA mutant over kanserlerinde onaylı hedefe yönelik PARP inhibitörüdür."
                        },
                        {
                            "key": "B",
                            "text": "İmatinib",
                            "isCorrect": False,
                            "explanation": "İmatinib BCR-ABL ve KIT inhibitörüdür."
                        },
                        {
                            "key": "C",
                            "text": "Trastuzumab",
                            "isCorrect": False,
                            "explanation": "Trastuzumab HER2 amplifiye karsinomlarda kullanılır."
                        },
                        {
                            "key": "D",
                            "text": "Rituksimab",
                            "isCorrect": False,
                            "explanation": "Rituksimab CD20 pozitif B hücreli lenfomalarda kullanılır."
                        }
                    ],
                    "BRCA mutant over kanserinde standart idame ilacı PARP inhibitörü Olaparib'dir."
                )
            ]
        }
    ]
