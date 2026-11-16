# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 7: Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar (Slayt 61 - 70)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # Slayt 61: Şokun Patofizyolojik Tanımı ve Hücresel Hipoksi Temeli
    slides.append({
        "id": "k1-24-s61",
        "title": "Şokun Patofizyolojik Tanımı ve Hücresel Hipoksi Temeli",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 61,
        "narrative": (
            "Şok, kardiyovasküler sistemin dokulara yeterli oksijen ve besin maddesi iletememesi sonucunda gelişen, "
            "yaygın doku hipoperfüzyonu ve generalize hücresel hipoksi ile karakterize hayatı tehdit eden nihai klinik tablodur: "
            "1. **Patofizyolojik Temel:** Azalmış kardiyak debi veya efektif dolaşan intravasküler kan hacminin kritik düzeyde azalmasıdır. "
            "2. **Hücresel Çöküş Kaskadı:** Akut perfüzyon yetmezliği, mitokondriyal oksidatif fosforilasyonun çökmesine, "
            "adenozin trifosfat (ATP) üretiminin durmasına ve membran Na+/K+ ATPaz pompalarının bozulmasına yol açar. "
            "3. **Geri Dönüşümsüz Faz:** Hücre içinde kalsiyum ve su birikimi hidropik şişmeye, lizozomal membran yırtılmasına "
            "ve ilerleyen safhada geri dönüşümsüz parankimal hücre ölümüne neden olur. Başlangıçta hücresel hasar geri dönüşümlü "
            "iken, perfüzyon bozukluğunun uzaması kalıcı parankimal nekroza ve ölümcül çoklu organ yetmezliğine (MODS) yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Şok tablosunda doku hasarının evrensel patofizyolojik temeli dokuların yaygın hipoperfüzyon yaşaması ve hücresel hipoksidir.",
                "hipoperfüzyon",
                "Kılcal damar yatağında hücrelerin yeterli kan alamaması durumu"
            ),
            make_micro_quiz(
                "Şok sendromunun tüm etyolojik formlarında ortak olan ve hücresel disfonksiyonu başlatan temel hemodinamik bozukluk hangisidir?",
                {
                    "A": "Yaygın doku hipoperfüzyonu ve hücresel hipoksi",
                    "B": "Primer sistemik arteriyel hipertansiyon",
                    "C": "İzole eritrosit glukoz-6-fosfat dehidrogenaz eksikliği",
                    "D": "Lokalize lenfatik obstrüksiyon ve amiloidoz",
                    "E": "Pulmoner surfaktan aşırı sentezi"
                },
                "A",
                {
                    "A": "Doğrudur; şokun evrensel tanımı ve mekanizması yaygın doku hipoperfüzyonu ve hücresel hipoksidir.",
                    "B": "Yanlış; şokta arteriyel hipotansiyon ve perfüzyon çöküşü esastır.",
                    "C": "Yanlış; bu hemolitik anemi nedenidir, primer şok fizyopatolojisi değildir.",
                    "D": "Yanlış; lokalize lenfödem şok oluşturmaz.",
                    "E": "Yanlış; şokta ARDS gelişir ve surfaktan sentezi azalır."
                }
            )
        ]
    })

    # Slayt 62: Şokun Beş Temel Etyolojik ve Patofizyolojik Sınıfı
    slides.append({
        "id": "k1-24-s62",
        "title": "Şokun Beş Temel Etyolojik ve Patofizyolojik Sınıfı",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 62,
        "narrative": (
            "Klinik ve patolojik pratikte şok sendromu altta yatan primer tetikleyiciye göre başlıca beş ana grupta incelenir: "
            "1. **Kardiyojenik Şok:** Miyokardiyal pompa yetmezliğine bağlı kardiyak output çöküşüdür (geniş MI, aritmiler, tamponad). "
            "2. **Hipovolemik Şok:** İntravasküler kan veya plazma hacminin doğrudan kaybıdır (masif hemoraji, ağır yanıklar, dehidratasyon). "
            "3. **Septik Şok:** Patojen mikroorganizmalar ve sitokin fırtınasının yol açtığı endotel hasarı ve vazodilatasyondur. "
            "4. **Nörojenik Şok:** Vazomotor sempatik damar tonusunun yaygın kaybı sonucu venöz göllenmedir (spinal kord travması, anestezi). "
            "5. **Anafilaktik Şok:** IgE aracılı Tip I hipersensitiviteyle histamin salınımı ve generalize mikrovasküler kaçaktır. "
            "Bu beş form farklı hemodinamik yanıtlarla başlasa da nihayetinde doku perfüzyon yetmezliğinde birleşir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Şok Sınıflandırması ve Temel Fizyopatolojik Nedenler",
                ["Şok Kategorisi", "Primer Etyolojik Neden", "Temel Patofizyolojik Mekanizma"],
                [
                    ["Kardiyojenik", "Miyokard enfarktüsü veya aritmi", "Sol ventrikül pompa yetersizliği"],
                    ["Hipovolemik", "Masif hemoraji veya ağır yanık", "Dolaşan plazma ve eritrosit hacim kaybı"],
                    [
                        "Septik",
                        "Bakteriyemi ve endotoksin salınımı",
                        {"text": "Sistemik vazodilatasyon ve endotel hasarı", "isMasked": True, "hint": "Sitokin fırtınasıyla damar tonusunun çökmesi"}
                    ],
                    ["Nörojenik", "Spinal kord travması veya anestezi", "Sempatik vazomotor tonus felci"],
                    ["Anafilaktik", "Alerjenle tetiklenen mast hücre degranülasyonu", "Yaygın histaminerjik venöz göllenme"]
                ]
            ),
            make_active_recall(
                "Şok sınıflandırmasında primer miyokardiyal pompa fonksiyonunun akut çöküşüne bağlı gelişen form hangisidir?",
                "Kardiyojenik şok tablosudur.",
                "Kalp kasının ejeksiyon gücünü kaybetmesi"
            )
        ]
    })

    # Slayt 63: Kardiyojenik Şok: Miyokard Pompa Yetmezliği ve Hemodinami
    slides.append({
        "id": "k1-24-s63",
        "title": "Kardiyojenik Şok: Miyokard Pompa Yetmezliği ve Hemodinami",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 63,
        "narrative": (
            "Kardiyojenik şok, sol ventrikül miyokardının akut veya geniş hasarı sonucu kardiyak outputun kritik seviyeye "
            "düşmesiyle karakterize tablodur: "
            "1. **En Sık Etyoloji:** Sol ventrikül kas kitlesinin %40'ından fazlasını etkileyen transmural akut miyokard enfarktüsüdür. "
            "2. **Diğer Mekanik Nedenler:** Ölümcül ventriküler aritmiler, ventrikül serbest duvar veya papiller kas rüptürü, "
            "kardiyak tamponad ve pulmoner ana dalları tıkayan masif eyer embolilerdir (obstrüktif form). "
            "3. **Hemodinamik Profil:** Primer bozukluk kardiyak output (CO) düşüşüdür. Sol ventrikül kanı ileri pompalayamadığı için "
            "sol ventrikül diyastol sonu basıncı ve pulmoner kapiller uç basıncı (PCWP) belirgin şekilde artar. Periferik organları "
            "korumak adına sempatik sistem tetiklenir; sistemik vasküler rezistans (SVR) kompansatuar vazokonstriksiyonla yükselir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Kardiyojenik Şok Gelişim Kaskadı",
                [
                    "1. Miyokard Hasarı: Geniş alanda transmural ventriküler parankim nekrozu oluşması",
                    "2. Pompa Yetmezliği: Sol ventrikül debisinin çökmesi ve kardiyak outputun kritik gerilemesi",
                    "3. Geriye Yansıma: Pulmoner kapiller uç basıncının (PCWP) ve sol atriyal basıncın yükselmesi",
                    "4. Kompansatuar Yanıt: Hayati organları korumak adına sistemik vazokonstriksiyon ve SVR artışı"
                ]
            ),
            make_before_after(
                "Kardiyojenik Şokta Dinamikler",
                "Kompansatuar Faz",
                "Taşikardi, periferik vazokonstriksiyon, hafif pulmoner staz ve korunmuş beyin perfüzyonu",
                "Dekompanse Faz",
                "Masif PCWP artışı, alveolar pulmoner ödem, hipotansiyon ve periferik doku nekrozu"
            )
        ]
    })

    # Slayt 64: Hipovolemik Şok: Akut Hacim Kaybı ve Hemodinamik Yanıt
    slides.append({
        "id": "k1-24-s64",
        "title": "Hipovolemik Şok: Akut Hacim Kaybı ve Hemodinamik Yanıt",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 64,
        "narrative": (
            "Hipovolemik şok, vasküler yatak içindeki dolaşan kan veya plazma hacminin akut kaybı sonucu gelişir: "
            "1. **Etyolojik Spektrum:** Majör arteriyel travmalar, rüptüre aort anevrizması, gastrointestinal sistem masif "
            "kanamaları gibi tam kan kayıpları başı çeker. Geniş yüzeyli yanıklarda plazma kaybı, kontrolsüz diyare ve inatçı "
            "kusmalarda ise ağır sıvı-elektrolit kaybı aynı klinik tabloyu doğurur. "
            "2. **Ön Yük (Preload) Çöküşü:** Efektif dolaşan kan hacmi azaldığı için kalbe dönen venöz kan miktarı dramatik düşer. "
            "Santral venöz basınç (CVP) ve pulmoner kapiller uç basıncı (PCWP) belirgin şekilde azalır. "
            "3. **Sempatik Kompansasyon:** Baroreseptör refleksiyle şiddetli taşikardi ve alfa-adrenerjik periferik "
            "vazokonstriksiyon gelişir; sistemik vasküler rezistans (SVR) ileri derecede yükselir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Ağır politravmalı bir hastada masif retroperitoneal kanama sonucu taşikardi, derin hipotansiyon ve soluk soğuk ekstremiteler saptanıyor.",
                [
                    {
                        "text": "Hipovolemik şok tanısıyla acil izotonik kristalloid/eritrosit süspansiyonu replasmanı ve cerrahi hemostaz planlanması",
                        "isCorrect": True,
                        "explanation": "Mükemmel. Akut kan kaybında primer hedef intravasküler volümü süratle yerine koymak ve kanama odağını hemostazla kontrol etmektir."
                    },
                    {
                        "text": "Sistemik vazodilatatör infüzyonu başlanarak periferik damar direncinin düşürülmesi",
                        "isCorrect": False,
                        "explanation": "Hatalı ve ölümcül. Hipovolemik hastada periferik direnci kırmak hipotansiyonu derinleştirir ve kardiyak arreste sürükler."
                    }
                ]
            ),
            make_cloze(
                "Hipovolemik şokta sol ventriküle dönen venöz kan hacmi azaldığı için ölçülen pulmoner kapiller uç basıncı PCWP düzeyi düşüktür.",
                "PCWP",
                "Sol ventrikül dolum basıncını yansıtan pulmoner kama basıncı kısaltması"
            )
        ]
    })

    # Slayt 65: Nörojenik Şok: Sempatik Tonus Kaybı ve Periferik Vazodilatasyon
    slides.append({
        "id": "k1-24-s65",
        "title": "Nörojenik Şok: Sempatik Tonus Kaybı ve Periferik Vazodilatasyon",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 65,
        "narrative": (
            "Nörojenik şok, merkezi sinir sistemindeki vazomotor merkezlerin hasarlanması veya sempatik otonom sinir liflerinin "
            "akut kesintiye uğraması sonucu damar düz kas tonusunun aniden kaybolmasıdır: "
            "1. **Başlıca Etyolojik Nedenler:** Yüksek seviyeli spinal kord travmaları (servikal ve üst torakal transeksiyon), "
            "derin genel anestezi kazaları ve yüksek spinal anestezi komplikasyonlarıdır. "
            "2. **Damar Yatağında Göllenme:** Sempatik tonus ortadan kalkınca arteriyoller ve geniş kapasitans venleri yaygın biçimde genişler. "
            "Kan periferik venöz göllerde hapsolur; kalbe dönen efektif venöz hacim yetersiz kalır. "
            "3. **Ayırt Edici Hemodinamik Özellik:** Sistemik vasküler rezistansın (SVR) kompanse olmak yerine dramatik şekilde "
            "düşmesidir. Ayrıca sempatik kardiyak deşarj kesintiye uğradığından taşikardi yerine paradoksal bradikardi izlenebilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_micro_quiz(
                "Yüksek servikal kord yaralanması geçiren bir hastada gelişen nörojenik şokun diğer hipovolemik şok tiplerinden en temel hemodinamik farkı hangisidir?",
                {
                    "A": "Sempatik tonus kaybına bağlı periferik vasküler rezistansın (SVR) düşmesi",
                    "B": "Kardiyak debinin belirgin şekilde kompanse olarak artması",
                    "C": "Pulmoner kapiller uç basıncının aşırı yükselmesi",
                    "D": "Yaygın mikrovasküler eritrosit agregasyonu ve masif hemoliz",
                    "E": "Trombosit tüketimine bağlı izole primer kanama"
                },
                "A",
                {
                    "A": "Doğrudur; nörojenik şokta sempatik vazomotor felç nedeniyle SVR kompanse olarak artamaz, aksine dramatik düşer.",
                    "B": "Yanlış; venöz göllenme nedeniyle preload azalır ve debi düşer.",
                    "C": "Yanlış; PCWP artmaz, venöz dönüş azaldığı için düşer.",
                    "D": "Yanlış; nörojenik şok primer hemolitik tablo değildir.",
                    "E": "Yanlış; DİK septik şokta belirgindir, nörojenik şokun primer bulgusu değildir."
                }
            ),
            make_active_recall(
                "Nörojenik şokta sempatik felç nedeniyle arteriyol ve venlerin gevşemesi hangi hemodinamik parametrede dramatik düşüşe yol açar?",
                "Sistemik vasküler rezistans (SVR) düzeyidir.",
                "Periferik arteriyollerin damar içi akıma gösterdiği toplam direnç"
            )
        ]
    })

    # Slayt 66: Anafilaktik Şok: Tip I Hipersensitivite ve Sistemik Kapiller Kaçak
    slides.append({
        "id": "k1-24-s66",
        "title": "Anafilaktik Şok: Tip I Hipersensitivite ve Sistemik Kapiller Kaçak",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 66,
        "narrative": (
            "Anafilaktik şok, önceden duyarlılaşmış bir bireyde spesifik bir antijenle sistemik temas sonucu tetiklenen, "
            "Tip I immünoglobulin E (IgE) aracılı aşırı duyarlılık tablosudur: "
            "1. **Tetikleyici Antijenler:** Arı ve böcek venomları, parenteral penisilin ve beta-laktam antibiyotikler, "
            "radyoopak kontrast maddeler ve besin proteinleridir (yer fıstığı, deniz ürünleri). "
            "2. **Mast Hücre Degranülasyonu:** Sistemik dolaşıma giren antijen, bazofil ve doku mast hücreleri yüzeyindeki IgE "
            "moleküllerini çapraz bağlayarak saniyeler içinde masif degranülasyona yol açar. "
            "3. **Mediyatör Etkileri:** Salınan histamin, PAF ve lökotrienler yaygın arteriyoler dilatasyon, şiddetli bronkokonstriksiyon "
            "ve aşırı kapiller permeabilite artışına yol açar. Plazma hızla doku aralığına sızarak laringeal ödem ve dolaşım çöküşü yaratır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Anafilaktik Şok Moleküler Patogenezi",
                [
                    "1. Antijen Teması: Sistemik antijenin duyarlı mast hücre yüzeyindeki IgE'yi çapraz bağlaması",
                    "2. Mediyatör Fırtınası: Masif histamin, lökotrien C4-D4-E4 ve trombosit aktive edici faktör salınımı",
                    "3. Yaygın Vazodilatasyon: Sistemik vasküler rezistansın çökmesi ve mikrovasküler relaksasyon",
                    "4. Kapiller Kaçak ve Asfiksi: Plazmanın interstisyuma kaçışı, laringeal ödem ve sirkülatuar arrest"
                ]
            ),
            make_cloze(
                "Anafilaktik şokta mast hücresi degranülasyonunu başlatan immünoglobulin sınıfı IgE izotipidir.",
                "IgE",
                "Alerjik erken tip aşırı duyarlılık reaksiyonlarından sorumlu antikor"
            )
        ]
    })

    # Slayt 67: Şok Tiplerinde Karşılaştırmalı Hemodinamik Profil Tablosu
    slides.append({
        "id": "k1-24-s67",
        "title": "Şok Tiplerinde Karşılaştırmalı Hemodinamik Profil Tablosu",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 67,
        "narrative": (
            "Klinik pratikte ve patolojik değerlendirmede şok tiplerinin ayrımı hemodinamik profiller üzerinden yapılır: "
            "1. **Kardiyojenik Şok:** Primer bozukluk sol ventrikül pompa yetersizliğidir; kardiyak debi (CO) düşüktür. "
            "Sol atriyum arkasında kan biriktiğinden PCWP belirgin artmıştır; sempatik refleksle SVR yükselir. "
            "2. **Hipovolemik Şok:** İntravasküler hacim azaldığı için CO ve PCWP düşüktür; kompanse vazokonstriksiyonla SVR yükselir. "
            "3. **Erken Septik Şok:** Patojen ve sitokinlerin yarattığı vazodilatasyon nedeniyle SVR belirgin düşüktür; "
            "kalp debisi (CO) başlangıçta normal veya kompanse olarak artmıştır (hiperdinamik evre). "
            "4. **Nörojenik Şok:** Sempatik tonus kaybına bağlı SVR düşüktür; venöz göllenme nedeniyle PCWP ve CO azalır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Şok Tiplerinde Hemodinamik Parametre Değişimleri",
                ["Şok Tipi", "Kardiyak Debi (CO)", "Kama Basıncı (PCWP)", "Sistemik Direnç (SVR)"],
                [
                    ["Kardiyojenik", "Belirgin Azalmış", "Artmış", "Artmış (Vazokonstriksiyon)"],
                    [
                        "Hipovolemik",
                        "Belirgin Azalmış",
                        {"text": "Belirgin Azalmış", "isMasked": True, "hint": "İntravasküler hacim azaldığında sol kalp dolumunun yönü"},
                        "Artmış (Vazokonstriksiyon)"
                    ],
                    ["Septik (Erken)", "Normal veya Artmış", "Normal veya Azalmış", "Belirgin Azalmış (Vazodilatasyon)"],
                    ["Nörojenik", "Azalmış veya Normal", "Azalmış", "Belirgin Azalmış (Sempatik Felç)"],
                    ["Anafilaktik", "Azalmış veya Değişken", "Azalmış", "Belirgin Azalmış (Histamin Kaçağı)"]
                ]
            ),
            make_active_recall(
                "Hipovolemik şok ile kardiyojenik şok arasındaki en temel hemodinamik ayrım hangi sol kalp dolum parametresinin yönüyle belirlenir?",
                "Pulmoner kapiller uç basıncı (PCWP) düzeyidir; kardiyojenik şokta artarken hipovolemik şokta azalır.",
                "Sol atriyum basıncını yansıtan pulmoner kama parametresi"
            )
        ]
    })

    # Slayt 68: Sıcak Şok ve Soğuk Şok Klinik Ayrımının Patofizyolojisi
    slides.append({
        "id": "k1-24-s68",
        "title": "Sıcak Şok ve Soğuk Şok Klinik Ayrımının Patofizyolojisi",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 68,
        "narrative": (
            "Hastanın fizik muayenesinde cilt ısısı ve periferik vasküler dolum altta yatan şok mekanizması hakkında anahtar verir: "
            "1. **Soğuk Şok Fenomeni:** Hipovolemik ve kardiyojenik şokta, beyin ve koroner perfüzyonunu korumak amacıyla "
            "cilt, böbrek ve splanknik yatakta masif alfa-adrenerjik vazokonstriksiyon gerçekleşir. "
            "Ekstremiteler soğuk, soluk, nemli ve siyanotik hale gelir; periferik nabızlar ipliksi ve zayıftır. "
            "2. **Sıcak Şok Fenomeni:** Erken septik şokta bakteriyel ürünler ve sitokinler (indüklenebilir NO sentaz / iNOS uyarımı) "
            "yaygın periferik vazodilatasyona yol açar. Kutanöz mikrodolaşım genişlediği için hastanın ekstremiteleri sıcak, kuru ve "
            "pembe-kırmızıdır; nabızlar dolgun ve sıçrayıcı hissedilir. Geç dönemde miyokard baskılanınca septik şok da soğuk şoka döner."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Periferik Perfüzyon ve Cilt Bulguları",
                "Soğuk Şok (Hipovolemik / Kardiyojenik)",
                "Alfa-adrenerjik vazokonstriksiyon, soğuk, nemli, siyanotik cilt ve zayıf ipliksi nabız",
                "Sıcak Şok (Erken Septik)",
                "Nitrik oksit aracılı vazodilatasyon, sıcak, kuru, pembe ekstremiteler ve sıçrayıcı nabız"
            ),
            make_micro_quiz(
                "Fizik muayenede cildi belirgin olarak sıcak, kuru ve pembe renkte bulunan, sıçrayıcı nabızları olan bir şok hastasında öncelikle hangi tip şok düşünülmelidir?",
                {
                    "A": "Erken dönem hiperdinamik septik şok",
                    "B": "Akut masif kanamaya bağlı hipovolemik şok",
                    "C": "Transmural anterolateral miyokard enfarktüsü şoku",
                    "D": "Masif eyer pulmoner emboli şoku",
                    "E": "Ağır dehidratasyon şoku"
                },
                "A",
                {
                    "A": "Doğrudur; periferik vazodilatasyon sonucu sıcak cilt bulgusu erken hiperdinamik septik şokun en karakteristik kliniğidir.",
                    "B": "Yanlış; hipovolemide vazokonstriksiyon nedeniyle cilt soğuk ve nemlidir.",
                    "C": "Yanlış; kardiyojenik şokta cilt soğuk ve soluktur.",
                    "D": "Yanlış; pulmoner embolide kardiyak debi düşer ve soğuk şok gelişir.",
                    "E": "Yanlış; dehidratasyonda cilt turgoru azalır ve soğuktur."
                }
            )
        ]
    })

    # Slayt 69: Checkpoint 7
    slides.append({
        "id": "k1-24-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Şokun Sınıflandırılması, Hemodinamisi ve Klinik Tipleri",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 69,
        "narrative": (
            "Bu yedinci kontrol noktasında, şok patolojisinin sınıflandırma ve hemodinamik prensiplerini pekiştiriyoruz: "
            "1. **Evrensel Tanım:** Dokularda yaygın hipoperfüzyon ve generalize hücresel hipoksi tablosudur. "
            "2. **Kardiyojenik Şok:** Primer pompa çöküşüdür; debi düşer, PCWP ve SVR belirgin şekilde yükselir. "
            "3. **Hipovolemik Şok:** Kan/plazma kaybıdır; debi ve PCWP düşer, kompanse SVR yükselir. "
            "4. **Nörojenik Şok:** Sempatik tonus felcidir; SVR dramatik düşer, venöz göllenme gelişir. "
            "5. **Anafilaktik Şok:** IgE aracılı histamin salınımı ve sistemik kapiller kaçak tablosudur. "
            "6. **Sıcak vs Soğuk Şok:** Erken septik şokta vazodilatasyonla cilt sıcak ve pembedir (sıcak şok); "
            "hipovolemik ve kardiyojenik şokta vazokonstriksiyonla cilt soğuk ve nemlidir (soğuk şok)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s69-1",
                "Sol ventrikül infarktüsüne bağlı kardiyojenik şokta pulmoner kapiller uç basıncı (PCWP) düzeyinde ne yönde bir değişim izlenir?",
                "Belirgin bir artış izlenir.",
                "Miyokard pompa fonksiyonu yetersizliğinde sol atriyuma geriye doğru yansıyan hidrostatik yükseklik",
                "Kardiyojenik PCWP Değişimi"
            ),
            make_flashcard(
                "k1-24-fc-s69-2",
                "Erken hiperdinamik septik şok tablosunda cildin sıcak, kuru ve pembe renkte olmasının altında yatan primer vasküler mekanizma nedir?",
                "Yaygın periferik arteriyoler vazodilatasyondur.",
                "Doku düzeyinde endotelyal mediyatörler ve NO salınımıyla damar tonusunun gevşemesi hali",
                "Sıcak Şok Mekanizması"
            ),
            make_flashcard(
                "k1-24-fc-s69-3",
                "Sempatik vazomotor tonusun ortadan kalkmasıyla sistemik vasküler rezistansın (SVR) dramatik düşüş gösterdiği şok tipi hangisidir?",
                "Nörojenik şok tablosudur.",
                "Üst spinal kord zedelenmesi veya genel anestezik blokaj sonrası otonom kontrol kaybı",
                "Nörojenik Şok Direnci"
            )
        ],
        "interactiveElements": [
            make_table(
                "Şok Checkpoint Karşılaştırma Matrisi",
                ["Şok Tipi", "Primer Patofizyoloji", "Cilt Bulgusu", "SVR Değişimi"],
                [
                    ["Kardiyojenik", "Miyokard infarktüsü / Pompa yetmezliği", "Soğuk, nemli, soluk", "Artmış"],
                    ["Hipovolemik", "Masif kanama / Plazma kaybı", "Soğuk, soluk, yapışkan", "Artmış"],
                    [
                        "Septik (Erken)",
                        "Sitokin fırtınası / Bakteriyemi",
                        {"text": "Sıcak, kuru, pembe (Sıcak şok)", "isMasked": True, "hint": "Vazodilatasyon sonucu ekstremitelerin aldığı klinik durum"},
                        "Düşmüş"
                    ],
                    ["Nörojenik", "Sempatik tonus felci", "Ilık veya kuru", "Belirgin Düşmüş"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki hemodinamik profil eşleştirmelerinden hangisi hipovolemik şok için karakteristik bulgudur?",
                {
                    "A": "Kardiyak debi azalmış, PCWP azalmış, SVR artmış",
                    "B": "Kardiyak debi artmış, PCWP artmış, SVR azalmış",
                    "C": "Kardiyak debi azalmış, PCWP artmış, SVR artmış",
                    "D": "Kardiyak debi normal, PCWP belirgin artmış, SVR azalmış",
                    "E": "Kardiyak debi azalmış, PCWP artmış, SVR belirgin azalmış"
                },
                "A",
                {
                    "A": "Doğrudur; hipovolemide volüm kaybıyla debi ve PCWP düşerken, sempatik kompansasyonla SVR artar.",
                    "B": "Yanlış; bu profil erken septik şoka uyar.",
                    "C": "Yanlış; debi düşük, PCWP yüksek ve SVR yüksek tablosu kardiyojenik şoktur.",
                    "D": "Yanlış; hipovolemide PCWP artmaz.",
                    "E": "Yanlış; SVR düşüşü vazodilatatör şoklarda görülür."
                }
            )
        ]
    })

    # Slayt 70: Bölüm Özeti: Şok Tiplerinden Septik Şok İmmünopatolojisine Geçiş
    slides.append({
        "id": "k1-24-s70",
        "title": "Bölüm Özeti: Şok Tiplerinden Septik Şok İmmünopatolojisine Geçiş",
        "section": "Şok Patolojisi: Tanım, Sınıflandırma ve Temel Mekanizmalar",
        "slideNumber": 70,
        "narrative": (
            "Şok etyolojisi ve hemodinamisi incelendiğinde, kardiyojenik ve hipovolemik şokun temel olarak fiziksel "
            "veya mekanik bir dolaşım arızasına dayandığı görülür: "
            "1. **Mekanik vs İmmünolojik Çatışma:** Hipovolemi ve kardiyojenik şokta sorun hacim ve pompadır; septik şokta ise "
            "sorun patojen mikroorganizmalar ile konağın bağışıklık sistemi arasındaki ölümcül çatışmanın sistemik sonucudur. "
            "2. **Mikrobiyal Tetikleyiciler:** Bakteriyel ürünler endotel hücrelerini ve makrofajları doğrudan uyararak sistemik "
            "bir inflamasyon, mikrovasküler tromboz ve metabolik çöküş kaskadı başlatır. "
            "3. **Sonraki Bölüm Köprüsü:** Yoğun bakım ünitelerinde en sık ölüm nedeni olan septik şokun patogenezini kavramak; "
            "lipopolisakkarit (LPS) tanınmasını, TLR reseptörlerini, TNF-alfa ve IL-1 sitokin fırtınasını ve dissemine intravasküler "
            "koagülasyonu (DİK) moleküler düzeyde anlamayı zorunlu kılar. Bölüm 8'de bu patogenezi inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Şok Mekanizmalarının Evrimi",
                "Mekanik ve Hacimsel Şok",
                "Kardiyojenik ve hipovolemik formlarda primer debi ve dolaşan hacim yetersizliği",
                "İmmün ve Sitokin Aracılı Şok",
                "Septik şokta endotel hasarı, mikrovasküler tromboz, DİK ve metabolik çöküş"
            ),
            make_active_recall(
                "Yoğun bakım ünitelerinde en sık görülen ve endotel hasarı ile sitokin fırtınasının başrolde olduğu şok tipi hangisidir?",
                "Septik şok tablosudur.",
                "Patojenik mikroorganizmaların tetiklediği sistemik inflamatuar sendrom"
            )
        ]
    })

    return slides
