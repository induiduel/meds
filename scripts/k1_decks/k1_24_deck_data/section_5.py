# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 5: Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma (Slayt 41 - 50)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # Slayt 41: Enfarktüs Tanımı ve Klinik Önemi
    slides.append({
        "id": "k1-24-s41",
        "title": "Enfarktüs Tanımı ve Klinik Önemi: İskemik Hücre Ölümü",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 41,
        "narrative": (
            "Enfarktüs, klinik tıpta mortalitenin ve kalıcı organ yetmezliklerinin en yaygın patolojik zeminidir: "
            "1. **Enfarktüs Tanımı:** Bir doku veya organın arteriyel kan akımının veya venöz drenajının "
            "ani olarak kesilmesine bağlı gelişen lokal **iskemik nekroz alanıdır**. "
            "2. **Global Mortalitedeki Yeri:** Gelişmiş ve gelişmekte olan ülkelerde tüm ölümlerin yaklaşık yarısı enfarktüs kaynaklıdır: "
            "- **Miyokard Enfarktüsü (MI):** Koroner arter tıkanmasına bağlı kalp kası nekrozu (en sık ölüm nedeni). "
            "- **Serebral Enfarktüs (İskemik İnme):** Beyin damarlarının tıkanmasıyla oluşan nörolojik kayıp ve felç. "
            "3. **Diğer Kritik Enfarktlar:** Pulmoner enfarktüs, akut mezenterik iskemiye bağlı bağırsak gangreni, "
            "periferik vasküler hastalıkta alt ekstremite gangreni ve septik böbrek/dalak enfarktüsleri."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Bir dokunun arteriyel kanlanmasının veya venöz drenajının kesilmesine bağlı olarak gelişen lokal iskemik nekroz alanına enfarktüs denir.",
                "iskemik nekroz",
                "Kan akımı kesintisi sonucu oluşan doku ölümü biçimi"
            ),
            make_table(
                "Klinik Pratikte En Sık Görülen Enfarktüs Tipleri ve Sonuçları",
                ["Etkilenen Organ", "Tıkanan Primer Damar", "Tipik Nekroz Türü", "Temel Klinik Sonuç"],
                [
                    ["Kalp (Miyokard)", "Koroner arterler (LAD, RCA, Cx)", "Koagülatif nekroz", "Kardiyojenik şok, aritmi, kalp yetmezliği"],
                    [
                        "Beyin (Serebrum)",
                        "A. Cerebri Media (MCA), Karotis",
                        {"text": "Sıvılaşma (Likuefaksiyon) nekrozu", "isMasked": True, "hint": "Beyin dokusuna özgü erime nekrozu"},
                        "Hemipleji, afazi, kalıcı nörolojik defisit"
                    ],
                    ["Akciğer", "Pulmoner arter dalları", "Hemorajik koagülatif nekroz", "Plevritik ağrı, hemoptizi"],
                    ["İnce Bağırsak", "A. Mesenterica Superior", "Hemorajik transmural nekroz", "Perforasyon, peritonit, septik şok"]
                ]
            ),
            make_micro_quiz(
                "Dünya genelinde insan ölümlerinin ve kalıcı morbiditelerin yaklaşık yarısından sorumlu olan ve patolojik olarak lokal iskemik nekrozla karakterize klinik tablo hangisidir?",
                {
                    "A": "Enfarktüs (İskemik Doku Nekrozu)",
                    "B": "Primer Amiloidoz",
                    "C": "Akut Fibrinoid Vaskülit",
                    "D": "Dekompresyon Artriti",
                    "E": "Hemangiom Proliferasyonu"
                },
                "A",
                {
                    "A": "MI ve iskemik inme (enfarktüsler) dünyadaki en sık ölüm nedenleridir.",
                    "B": "Amiloidoz nadir protein katlanma hastalığıdır.",
                    "C": "Vaskülit enfarktüs yapabilir ancak ölümlerin yarısını oluşturmaz.",
                    "D": "Dekompresyon mesleki hastalıktır.",
                    "E": "Hemangiom benign damar tümörüdür."
                }
            )
        ]
    })

    # Slayt 42: Enfarktüs Nedenleri: Arteriyel Tromboz ve Vazospazm
    slides.append({
        "id": "k1-24-s42",
        "title": "Enfarktüs Nedenleri: Arteriyel Tromboz, Emboli ve Vazospazm",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 42,
        "narrative": (
            "Enfarktüsün patolojik nedenleri vasküler tıkanmanın mekanizmasına göre sınıflandırılır: "
            "1. **Ezici Çoğunluk (%99):** Enfarktüslerin neredeyse tamamı **arteriyel tromboz veya arteriyel tromboemboliye** bağlıdır. "
            "Aterosklerotik plağın yırtılması (rüptür) üzerinde dakikalar içinde gelişen lüminal trombüs, koroner ve serebral enfarktüslerin ana tetikleyicisidir. "
            "2. **Lokal Vazospazm:** Aterom plağı olan veya olmayan damarlarda düz kasların aşırı kasılması (vazospazm); "
            "Prinzmetal vazospastik angina, kokain kullanımı veya Raynaud fenomeninde olduğu gibi geçici veya kalıcı iskemi yaratabilir. "
            "3. **Plak İçi Kanama (İntraplak Hematom):** Aterosklerotik plağın içine neovasküler damarlardan kanama olması, "
            "plağın hacmini aniden katlayarak damar lümenini tamamen tıkayabilir. "
            "4. **Dıştan Bası:** Büyüyen bir tümörün, genişleyen bir hematomun veya aort diseksiyonunda yalancı lümenin damarı dıştan sıkıştırması."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Klinik pratikte enfarktüslerin yüzde doksan dokuzundan sorumlu olan en yaygın primer damarsal patoloji arteriyel tromboz ve arteriyel tromboembolidir.",
                "arteriyel tromboz",
                "Damar lümeninde aterom rüptürüyle oluşan lokal pıhtı tıkanması"
            ),
            make_table(
                "Enfarktüs Etyolojik Mekanizmaları ve Klinik Örnekleri",
                ["Mekanizma Sınıfı", "Patolojik Olay", "Klinik Prototip Örnek"],
                [
                    ["Arteriyel Tromboz (%90+)", "Aterosklerotik plak rüptürü ve trombüs", "Akut transmural miyokard enfarktüsü (AMI)"],
                    ["Arteriyel Emboli", "Sol ventrikül mural pıhtısının distal artere oturması", "Akut bacak iskemisi, renal kama enfarktüsü"],
                    [
                        "Vasküler Vazospazm",
                        {"text": "Aşırı arteriyel düz kas kontraksiyonu", "isMasked": True, "hint": "Damar lümeninin fonksiyonel şiddetli büzüşmesi"},
                        "Kokain intoksikasyonu MI, Prinzmetal angina"
                    ],
                    ["İntraplak Kanama", "Aterom plağı içine neovasküler hematom", "Karotis arterin ani tam tıkanması"]
                ]
            ),
            make_micro_quiz(
                "Yirmi sekiz yaşında bilinen hiçbir ateroskleroz öyküsü olmayan bir gençte aşırı doz kokain kullanımı sonrasında elektrokardiyografide ST elevasyonlu anterior miyokard enfarktüsü gelişmiştir. Bu olgudaki enfarktüsün primer patofizyolojik mekanizması hangisidir?",
                {
                    "A": "Şiddetli koroner arter vazospazmı",
                    "B": "Diz üstü venlerden gelen paradoksal emboli",
                    "C": "Kapak vejetasyonunun kalsifikasyonu",
                    "D": "Konjenital koroner arter agenezisi",
                    "E": "Kemik iliği yağ embolisi"
                },
                "A",
                {
                    "A": "Kokain aşırı adrenerjik uyarıyla şiddetli koroner vazospazma yol açarak gençlerde akut MI tetikler.",
                    "B": "Paradoksal emboli beyne daha sık gider.",
                    "C": "Kalsifikasyon yaşlı hastalardadır.",
                    "D": "Agenezi doğumsaldır, kokainle tetiklenmez.",
                    "E": "Yağ embolisi kemik kırığında olur."
                }
            )
        ]
    })

    # Slayt 43: Venöz Tıkanmaya Bağlı Enfarktüs Mekanizması
    slides.append({
        "id": "k1-24-s43",
        "title": "Venöz Tıkanmaya Bağlı Enfarktüs Mekanizması: Torsiyon ve Boğulma",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 43,
        "narrative": (
            "Enfarktüsler yalnızca arterlerin tıkanmasıyla değil, venöz kan çıkışının tamamen engellenmesiyle de gelişebilir: "
            "1. **Venöz Tıkanma Dinamiği:** İnce duvarlı venler dıştan gelen basılara ve burkulmalara karşı kalın duvarlı arterlerden çok daha duyarlıdır. "
            "Venöz akım kesildiğinde, kalın arterler dokuya kan pompalamaya devam eder. "
            "2. **Geriye Doğru Basınç Yükselmesi:** Dokudan kan çıkamadığı için kapiller ve venöz yatakta hidrostatik basınç fırlar. "
            "Basınç arteriyel perfüzyon basıncına ulaştığında, dokuya taze oksijenli arter kanı giremez hale gelir. "
            "Doku masif konjesyona uğrar ve hipoksi nedeniyle **iskemik nekroza** sürüklenir. "
            "3. **Klinik Prototipler:** "
            "- **Testis Torsiyonu:** Funiculus spermaticus'un kendi etrafında dönmesiyle venöz pleksus tıkanır; acil cerrahi detorsiyon yapılmazsa testis hemorajik nekroza gider. "
            "- **Over Kist Torsiyonu:** Over pedikülünün burkulması. "
            "- **İnkarsere / Strangüle Herni (Fıtık Boğulması):** Fıtık halkasında sıkışan bağırsak segmentinin venöz dönüşünün boğulması. "
            "- **Serebral Venöz Sinüs Trombozu.**"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Testis torsiyonu veya boğulmuş fıtıklarda ince duvarlı venlerin tıkanması sonucu geriye doğru basınç yükselerek arteriyel girişi durdurur ve venöz enfarktüse yol açar.",
                "venöz enfarktüse",
                "Venöz kan çıkışının engellenmesiyle oluşan kanamalı iskemik nekroz"
            ),
            make_table(
                "Venöz Enfarktüs Prototip Klinik Tabloları",
                ["Klinik Tablo", "Anatomik Mekanizma", "Patolojik Sonuç"],
                [
                    ["Testis Torsiyonu", "Funiculus spermaticus venlerinin burkulması", "Testisin koyu mor-siyah hemorajik nekrozu"],
                    [
                        "Strangüle İnguinal Herni",
                        "Fıtık halkasında mezenter venlerinin sıkışması",
                        {"text": "İnce bağırsak kangreni ve perforasyon", "isMasked": True, "hint": "Boğulmuş bağırsak segmentinin iskemik ölümü"}
                    ],
                    ["Over Torsiyonu", "Over ligamanının dönmesi ve ven stazı", "Hemorajik over nekrozu ve akut batın"]
                ]
            ),
            make_micro_quiz(
                "On altı yaşında bir erkek çocuk aniden başlayan şiddetli skrotal ağrı ve şişlik ile acile başvurmuştur. Skrotal doppler ultrasonografide testise kan girişinin durduğu ve spermatik kordun burkulduğu saptanmıştır. Bu hastada doku nekrozunu başlatan primer vasküler olay hangisidir?",
                {
                    "A": "İnce duvarlı venöz damarların burkularak tıkanması ve geriye doğru venöz hipertansiyonla arteriyel akımı durdurması",
                    "B": "Aortadan kaynaklanan bir kolesterol embolusunun testisi tıkaması",
                    "C": "Testis arterinde aterosklerotik plak yırtılması",
                    "D": "Bakteriyel infektif endokardit vejetasyonu",
                    "E": "Kemik iliği yağ embolisi"
                },
                "A",
                {
                    "A": "Torsiyonda önce ince duvarlı venler tıkanır; venöz konjesyon arteriyel akımı durdurarak hemorajik enfarktüs yapar.",
                    "B": "16 yaşında kolesterol embolisi beklenmez.",
                    "C": "Testis arterinde aterom rüptürü olmaz.",
                    "D": "Endokardit vejetasyonu arteriyel emboli yapar, burulma yapmaz.",
                    "E": "Yağ embolisi kemik kırığında görülür."
                }
            )
        ]
    })

    # Slayt 44: Enfarktüsün Sınıflandırılması: Kırmızı vs Beyaz Enfarktüs
    slides.append({
        "id": "k1-24-s44",
        "title": "Enfarktüsün Sınıflandırılması: Kırmızı (Hemorajik) vs Beyaz (Anemik)",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 44,
        "narrative": (
            "Patolojide enfarktüsler makroskobik renklerine ve nekroz alanındaki kan miktarına göre iki ana gruba ayrılır: "
            "1. **Kırmızı (Hemorajik) Enfarktüsler:** "
            "Nekroz alanının içine komşu damarlardan veya kollaterallerden yoğun eritrosit ve kan sızması sonucu oluşur. "
            "Doku koyu kırmızı, bordo veya mor-siyah renkte görünür. "
            "Tipik olarak: Venöz tıkanmalarda, çift dolaşımlı organlarda (akciğer, ince bağırsak), gevşek süngerimsi dokularda ve "
            "arter tıkanıklığı açılan reperfüzyon alanlarında görülür. "
            "2. **Beyaz (Anemik / Soluk) Enfarktüsler:** "
            "Nekroz alanına kan sızmasının minimal olduğu veya hiç olmadığı durumlardır. "
            "Tipik olarak: **Uç arter dolaşımına sahip katı (solid) organlarda (kalp, dalak, böbrek)** görülür. "
            "Organ parankimi son derece sıkı ve sert olduğundan çevre dokudan nekrotik alana kanama sızamaz. "
            "Zamanla eritrositler lizise uğrar ve alan fildişi beyazı veya soluk sarı bir renk alır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Uç arter dolaşımına sahip katı organlar olan kalp, dalak ve böbrekte gelişen iskemik nekroz alanları beyaz yani anemik enfarktüs olarak sınıflandırılır.",
                "anemik enfarktüs",
                "Katı organlarda görülen soluk renkli enfarktüs tipi"
            ),
            make_table(
                "Kırmızı ve Beyaz Enfarktüs Temel Ayrım Tablosu",
                ["Ölçüt / Özellik", "Kırmızı (Hemorajik) Enfarktüs", "Beyaz (Anemik) Enfarktüs"],
                [
                    ["Makroskobik Renk", "Koyu kırmızı, mor, kanamalı", "Soluk, fildişi beyazı - sarımsı"],
                    [
                        "Doku Anatomisi",
                        "Gevşek, süngerimsi doku veya çift dolaşım",
                        {"text": "Katı (solid) parankim ve uç arter dolaşımı", "isMasked": True, "hint": "Kan sızmasını engelleyen sert organ yapısı"}
                    ],
                    ["Tipik Organlar", "Akciğer, İnce Bağırsak, Testis/Over torsiyonu", "Kalp (Miyokard), Dalak, Böbrek"],
                    ["Vasküler Neden", "Venöz tıkanma veya reperfüzyon", "Primer arteriyel tam tıkanma"]
                ]
            ),
            make_micro_quiz(
                "Patoloji laboratuvarında incelenen bir doku kesitinde enfarktüs alanının 'Beyaz (Anemik)' tipte olmasını belirleyen en temel anatomik ve histolojik faktör hangisidir?",
                {
                    "A": "Organın katı (solid) yapıda olması ve uç arter dolaşımına sahip olması",
                    "B": "Organın çift kan dolaşımına sahip olması",
                    "C": "Dokunun gevşek ve süngerimsi alveoller içermesi",
                    "D": "Damar tıkanıklığının bir venöz torsiyondan kaynaklanması",
                    "E": "Tıkalı alana yoğun reperfüzyon kanaması olması"
                },
                "A",
                {
                    "A": "Katı organlar (kalp, böbrek, dalak) uç artere sahiptir ve sert parankimleri kan sızmasını engellediğinden beyaz enfarktüs oluşur.",
                    "B": "Çift dolaşım kırmızı enfarktüs yapar.",
                    "C": "Gevşek doku kırmızı enfarktüs yapar.",
                    "D": "Venöz torsiyon kırmızı enfarktüs yapar.",
                    "E": "Reperfüzyon kırmızı enfarktüs yapar."
                }
            )
        ]
    })

    # Slayt 45: Kırmızı (Hemorajik) Enfarktüsün Görüldüğü Durumlar
    slides.append({
        "id": "k1-24-s45",
        "title": "Kırmızı (Hemorajik) Enfarktüsün Görüldüğü Durumlar ve Kurallar",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 45,
        "narrative": (
            "Robbins patoloji ilkelerine göre kırmızı (hemorajik) enfarktüsün ortaya çıktığı 5 temel durum vardır: "
            "1. **Venöz Tıkanmalar:** Kanın dokudan çıkamadığı durumlar (Testis ve over torsiyonu, strangüle fıtık, mezenter ven trombozu). "
            "2. **Çift Kan Dolaşımı Olan Dokular:** "
            "- **Akciğer:** Pulmoner arter tıkandığında bronşiyal arterlerden nekrotik alana kan akmaya devam eder. "
            "- **İnce Bağırsak:** Mezenterik vasküler arklar zengin kollateraller içerdiğinden tıkalı alana çevre damarlardan kan sızar. "
            "3. **Gevşek ve Süngerimsi Dokular:** Akciğer alveolleri gibi dirençsiz boşluklar kanın kolayca toplanmasına izin verir. "
            "4. **Önceden Konjesyone Olan Dokular:** Kronik pasif konjesyon zeminindeki organlar. "
            "5. **Reperfüzyon Hasarı:** Tıkalı bir arter trombolitik ilaçla (tPA), anjiyoplastiyle (stent) veya spazmın çözülmesiyle yeniden açıldığında; "
            "iskemi nedeniyle bütünlüğünü kaybetmiş nekrotik kapillerlerden doku içine masif kan fışkırır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Akut miyokard enfarktüsü geçiren bir hastada koroner arter stentle açıldığında hasarlı nekrotik damarlardan dokuya kan sızmasıyla beyaz enfarktüs kırmızı hemorajik enfarktüse dönüşebilir.",
                "kırmızı hemorajik enfarktüse",
                "Reperfüzyon sonrası nekrotik dokuda kanama birikmesiyle oluşan morfoloji"
            ),
            make_table(
                "Kırmızı Enfarktüsün Beş Temel Nedeni ve Mekanizmaları",
                ["Neden / Durum", "Mekanizma", "Klinik Örnek"],
                [
                    ["1. Venöz Tıkanma", "Çıkamayan kanın dokuda göllenmesi", "Testis torsiyonu, boğulmuş fıtık"],
                    [
                        "2. Çift Dolaşım",
                        {"text": "İkinci paralel sistemden nekrotik alana kan girişi", "isMasked": True, "hint": "Kollateral veya alternatif arterden devam eden kan akımı"},
                        "Akciğer ve İnce bağırsak enfarktüsü"
                    ],
                    ["3. Gevşek Doku", "Eritrositlerin serbestçe yayılması", "Akciğer parankimi"],
                    ["4. Önceden Konjesyon", "Yavaş venöz akım zemininde iskemi", "Kronik kalp yetmezliğinde karaciğer"],
                    ["5. Reperfüzyon", "Nekrotik damarlara ani kan hücumu", "Stent/tPA sonrası miyokard veya inme alanı"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki organ ve klinik durum eşleştirmelerinden hangisinde gelişen enfarktüsün morfolojik olarak 'Kırmızı (Hemorajik)' özellikte olması BEKLENMEZ?",
                {
                    "A": "Uç arter dolaşımlı böbrek korteksinde arter embolisine bağlı gelişen enfarktüs",
                    "B": "Çift dolaşımlı akciğerde gelişen pulmoner enfarktüs",
                    "C": "Funiculus spermaticus burkulmasına bağlı testis torsiyonu",
                    "D": "Strangüle fıtık kesesinde sıkışan ince bağırsak ansı",
                    "E": "Trombolitik tedavi sonrası reperfüzyona uğrayan beyin enfarktüsü alanı"
                },
                "A",
                {
                    "A": "Böbrek uç arterli katı bir organdır; enfarktüsü daima BEYAZ (anemik) tiptedir, kırmızı olması beklenmez.",
                    "B": "Akciğer çift dolaşımla kırmızı enfarktüs yapar.",
                    "C": "Testis torsiyonu venöz tıkanmayla kırmızı enfarktüs yapar.",
                    "D": "İnce bağırsak çift arklarla kırmızı enfarktüs yapar.",
                    "E": "Reperfüzyon kanaması enfarktüsü kırmızıya çevirir."
                }
            )
        ]
    })

    # Slayt 46: Beyaz (Anemik) Enfarktüsün Görüldüğü Durumlar
    slides.append({
        "id": "k1-24-s46",
        "title": "Beyaz (Anemik) Enfarktüsün Görüldüğü Organlar ve Özellikleri",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 46,
        "narrative": (
            "Beyaz (anemik veya soluk) enfarktüsler, katı organların uç arter tıkanıklıklarında gelişen klasik iskemik nekrozlardır: "
            "1. **Temsilci Üç Organ (Patoloji Altın Kuralı):** "
            "- **Kalp (Miyokard):** Koroner arter dalları fonksiyonel uç arterlerdir; reperfüzyon uygulanmadıkça miyokard enfarktüsü soluk beyazdır. "
            "- **Dalak:** Splenik arter dalları uç arterdir; sistemik embolilerle sıkça soluk beyaz enfarktüsler oluşur. "
            "- **Böbrek:** İnterlober ve arkuat arterler anastomoz içermez; tıkanma kortekste fildişi beyazı enfarktüs yapar. "
            "2. **Neden Soluktur?** "
            "- **Sert Doku Yapısı:** Organ parankimi son derece sıkı ve fibröz stromal iskeletle çevrilidir; komşu alanlardan kapiller sızıntıyı sınırlar. "
            "- **Koagülatif Nekroz:** İskemi sonrası hücre proteinleri denatüre olur, hücreler şişer ve mikrosirkülasyondaki kanı dışarı doğru sıkar. "
            "- **Eritrosit Lizisi:** Başlangıçta kenarlarda hafif kızarıklık olsa da, 24-48 saat içinde eritrositler parçalanır ve alan tamamen beyazlaşır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Uç arter beslenmesine sahip olan kalp, dalak ve böbrek gibi katı organlarda gelişen iskemik nekroz alanları beyaz anemik enfarktüs olarak adlandırılır.",
                "beyaz anemik enfarktüs",
                "Katı organ parankiminde görülen soluk renkli iskemik nekroz"
            ),
            make_table(
                "Beyaz Enfarktüs Gelişen Katı Organlar ve Klinik Tablolar",
                ["Katı Organ", "Tıkanan Uç Damar", "Makroskobik Lezyon Şekli", "Histopatolojik Nekroz"],
                [
                    ["Böbrek", "İnterlobar / Arkuat arter", "Kortekste tabanı kapsülde beyaz kama", "Koagülatif nekroz (hayalet glomerüller)"],
                    [
                        "Dalak",
                        "Splenik arter dalları",
                        {"text": "Subkapsüler kama biçimli soluk sert alan", "isMasked": True, "hint": "Kapsül altında sarımsı beyaz piramidal nekroz"},
                        "Koagülatif nekroz ve fibrinöz kapsülit"
                    ],
                    ["Kalp", "Koroner arter dalları (LAD/RCA)", "Transmural veya subendokardiyal soluk alan", "Koagülatif nekroz ve kontraksiyon bantları"]
                ]
            ),
            make_micro_quiz(
                "Atriyal fibrilasyonu olan bir hastada mural trombüsten kopan bir embolusun sol renal arteri tıkaması sonucu böbrekte gelişmesi beklenen enfarktüsün makroskobik renk ve tip sınıflaması hangisidir?",
                {
                    "A": "Beyaz (Anemik) Enfarktüs",
                    "B": "Kırmızı (Hemorajik) Enfarktüs",
                    "C": "Primer Sıvılaşma Nekrozu",
                    "D": "Kazeifiye Granülomatöz Enfarktüs",
                    "E": "Enzimik Yağ Nekrozu"
                },
                "A",
                {
                    "A": "Böbrek katı bir organdır ve uç arter beslenmesine sahiptir; emboli sonrası klasik Beyaz (Anemik) enfarktüs gelişir.",
                    "B": "Kırmızı enfarktüs akciğer ve bağırsakta olur.",
                    "C": "Sıvılaşma beyinde görülür.",
                    "D": "Kazeifikasyon tüberküloz enfeksiyonudur.",
                    "E": "Enzimik yağ nekrozu akut pankreatitte görülür."
                }
            )
        ]
    })

    # Slayt 47: Enfarktüsün Makroskobik Morfolojisi: Kama Biçimi
    slides.append({
        "id": "k1-24-s47",
        "title": "Enfarktüsün Makroskobik Morfolojisi: Kama (Wedge-Shaped) Mimarisi",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 47,
        "narrative": (
            "Katı organlarda ve akciğerde gelişen enfarktüslerin makroskobik geometrisi damarsal dallanma ağacının doğrudan bir sonucudur: "
            "1. **Kama (Wedge / Piramit) Şekli:** Bir arter tek bir noktadan dallanarak yelpaze şeklinde dokuya yayılır. "
            "Damar tıkandığında, o damarın sulama alanındaki tüm parankim üçgen/kama şeklinde ölür: "
            "- **Kamanın Tabanı:** Organın dış yüzeyine (**serozaya, kapsüle veya plevraya**) oturur. "
            "- **Kamanın Tepesi (Apeksi):** Dokunun derinliğindeki tıkalı besleyici arter dalına doğru bakar. "
            "2. **Zaman İçinde Makroskobik Evrim:** "
            "- **İlk 24 Saat:** Enfarkt sınırları belirsizdir, doku hafif ödemli ve kızarıktır. "
            "- **24 - 48 Saat:** Sınırlar son derece keskinleşir. Çevre sağlam doku hiperemik dar bir kırmızı inflamasyon halkasıyla enfarktüsü kuşatır. "
            "- **Günler - Haftalar:** Nekrotik alan solar, sarı-beyaz renk alır ve sertleşir. "
            "- **Aylar:** Skar dokusu büzüşerek organ yüzeyinde içeri doğru çökük derin bir fibröz çentik (skar) bırakır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Böbrek ve dalak enfarktüslerinde kamanın tabanı organ kapsülüne otururken, kamanın tepe noktası doku derinliğindeki tıkalı besleyici artere bakar.",
                "organ kapsülüne",
                "Kama biçimli enfarktüsün geniş tabanının temas ettiği anatomik dış yüzey"
            ),
            make_table(
                "Enfarktüsün Zamana Göre Makroskobik Evrimi",
                ["Zaman Penceresi", "Enfarktüs Alanı Görünümü", "Kenar / Çevre Doku Özelliği"],
                [
                    ["İlk 24 Saat", "Hafif ödemli, sınırları belirsiz, siyanotik", "Henüz belirgin reaksiyon çizgisi yok"],
                    [
                        "24 - 48 Saat",
                        {"text": "Sınırlar son derece net, soluk ve kama biçimli", "isMasked": True, "hint": "Koagülatif nekrozun oturduğu ve sınırların çizildiği evre"},
                        "Dar, kırmızı hiperemik inflamasyon halkası"
                    ],
                    ["1 - 2 Hafta", "Sarımsı-beyaz, yumuşamış kenarlar", "Granülasyon dokusu içe doğru ilerler"],
                    ["Aylar Sonra", "Sert, beyaz, içeriye çökük fibröz skar", "Normal komşu parankim"]
                ]
            ),
            make_micro_quiz(
                "Otopsi sırasında bir hastanın böbrek kesitinde korteksten medullaya doğru uzanan, tabanı böbrek fibröz kapsülüne oturan ve etrafı ince kırmızı hiperemik bir halkayla çevrili sarımsı-beyaz üçgen bir lezyon görülmüştür. Bu lezyonun geometrik ve patolojik tanımı hangisidir?",
                {
                    "A": "Kama biçimli (wedge-shaped) beyaz renal enfarktüs",
                    "B": "Diffüz akut glomerülonefrit",
                    "C": "Polikistik böbrek kisti",
                    "D": "Renal hücreli karsinom tümör nodülü",
                    "E": "Akut piyelonefrit apsesi"
                },
                "A",
                {
                    "A": "Tabanı kapsüle oturan üçgen/kama biçimli soluk lezyon klasik kama biçimli renal enfarktüstür.",
                    "B": "Glomerülonefrit diffüzdür, kama şeklinde lokal olmaz.",
                    "C": "Kist sıvı doludur.",
                    "D": "RCC heterojen vasküler kanamalı kitle yapar.",
                    "E": "Piyelonefrit apsesi sarı irin odaklarıdır."
                }
            )
        ]
    })

    # Slayt 48: Enfarktüsün Mikroskobik Morfolojisi: Koagülatif ve İstisna Sıvılaşma
    slides.append({
        "id": "k1-24-s48",
        "title": "Mikroskobik Morfoloji: Koagülatif Nekroz ve Beyindeki Sıvılaşma İstisnası",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 48,
        "narrative": (
            "Enfarktüsün histopatolojik tanısı temel nekroz tiplerine dayanır: "
            "1. **Koagülatif Nekroz (Genel Kural):** "
            "Santral sinir sistemi hariç, vücuttaki **tüm organ enfarktüslerinin temel mikroskobik karşılığı koagülatif nekrozdur**: "
            "- Asidoz nedeniyle litik enzimler de denatüre olur, bu nedenle doku kendi kendini hemen eritemez. "
            "- **Hücre sınırları ve temel doku mimarisi günlerce korunur** ('hayalet hücreler' / ghost cells). "
            "- Sitoplazma yoğun eozinofilik (kıpkırmızı pembe) boyanır. "
            "- Nükleus sırasıyla büzüşür (piknoz), parçalanır (karyoreksis) ve tamamen erir (karyolizis). "
            "2. **BEYİNDEKİ KRİTİK İSTİSNA (Sıvılaşma / Likuefaksiyon Nekrozu):** "
            "Santral sinir sisteminde (beyin ve omurilik) arter tıkanması koagülatif değil, **daima SIVI LAŞMA (LİKUEFAKSİYON) NEKROZUNA** yol açar! "
            "Beyin dokusu yüksek lipid ve miyelin içerir, litik enzimler çok aktiftir. "
            "Nekrotik nöronlar ve glia hızla eriyerek sıvılaşır; makrofajlar (köpüksü lipid yüklü mikroglia) alanı temizler ve geride kistik bir boşluk kalır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Santral sinir sistemi hariç tüm organ enfarktüslerinde koagülatif nekroz görülürken, beyin dokusunda gelişen iskemik enfarktüs daima sıvılaşma yani likuefaksiyon nekrozu ile sonuçlanır.",
                "sıvılaşma",
                "Beyin dokusunda dokunun eriyerek kavitasyon oluşturduğu nekroz tipi"
            ),
            make_table(
                "Koagülatif ve Sıvılaşma Nekrozu Karşılaştırması",
                ["Özellik", "Koagülatif Nekroz (Genel Organlar)", "Sıvılaşma Nekrozu (Beyin Dokusu)"],
                [
                    ["Görüldüğü Dokular", "Kalp, böbrek, dalak, karaciğer enfarktları", "Beyin ve medulla spinalis enfarktları"],
                    ["Doku Mimarisi", "Hücre sınırları günlerce korunur (hayalet hücreler)", "Doku mimarisi hızla tamamen erir ve sıvılaşır"],
                    [
                        "Nihai Patolojik Sonuç",
                        "Granülasyon dokusu ve fibröz skar",
                        {"text": "İçinde berrak sıvı olan kistik boşluk (kavitasyon)", "isMasked": True, "hint": "Gliozis duvarıyla çevrili kistik beyin lezyonu"}
                    ],
                    ["Hücresel Temel", "Protein denatürasyonu baskındır", "Enzimatik otoliz ve sindirim baskındır"]
                ]
            ),
            make_micro_quiz(
                "Tıp patolojisinde arteriyel iskemiye bağlı enfarktüs gelişen organlar arasında 'Koagülatif Nekroz' kuralına uymayan ve daima 'Sıvılaşma (Likuefaksiyon) Nekrozu' geliştiren tek organ hangisidir?",
                {
                    "A": "Beyin (Santral Sinir Sistemi)",
                    "B": "Miyokard (Kalp)",
                    "C": "Böbrek",
                    "D": "Dalak",
                    "E": "Karaciğer"
                },
                "A",
                {
                    "A": "Beyin dokusu zengin lipid ve litik enzim içeriği nedeniyle iskemide daima sıvılaşma nekrozu yapar.",
                    "B": "Miyokard koagülatif nekroz yapar.",
                    "C": "Böbrek koagülatif nekroz yapar.",
                    "D": "Dalak koagülatif nekroz yapar.",
                    "E": "Karaciğer koagülatif nekroz yapar."
                }
            )
        ]
    })

    # Slayt 49: [TEKRAR SAYFASI - CHECKPOINT 5] Enfarktüs Etyolojisi, Morfolojisi ve Sınıflaması
    slides.append({
        "id": "k1-24-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Enfarktüs Etyolojisi, Morfolojisi ve Sınıflaması",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 49,
        "narrative": (
            "Bu beşinci checkpoint sayfasında, enfarktüs etyolojisini, sınıflamasını ve morfolojisini özetliyoruz: "
            "1. **Enfarktüs Tanımı:** Arteriyel akım kesintisine (veya venöz tıkanmaya) bağlı gelişen lokal iskemik nekrozdur. "
            "2. **Etyoloji:** %99 arteriyel tromboz ve embolidir. Torsiyon (testis/over) ve boğulmuş fıtık venöz enfarktüs yapar. "
            "3. **Beyaz (Anemik) Enfarktüs:** Uç arter dolaşımlı KATI ORGANLARDA (KALP, DALAK, BÖBREK) görülür; parankim serttir, kan sızamaz. "
            "4. **Kırmızı (Hemorajik) Enfarktüs:** Venöz tıkanmalarda, ÇİFT DOLAŞIMLI organlarda (AKCİĞER, İNCE BAĞIRSAK), "
            "gevşek dokularda ve REPERFÜZYON alanlarında görülür. "
            "5. **Kama Geometrisi:** Tabanı organ yüzeyine/kapsüle, tepesi tıkalı damara bakan piramit mimarisidir. "
            "6. **Mikroskopi Kuralı:** Tüm organlarda KOAGÜLATİF NEKROZ (hayalet hücreler) görülürken, "
            "BEYİNDE İSTİSNA OLARAK DAİMA SIVILAŞMA (LİKUEFAKSİYON) NEKROZU gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s49-1",
                "Patolojide uç arter dolaşımına sahip katı (solid) organlar olan kalp, dalak ve böbrekte gelişen enfarktüslerin rengi ve morfolojik tipi nedir?",
                "Beyaz (anemik) enfarktüs tipidir.",
                "Kan sızmasına izin vermeyen sert parankimde görülen soluk iskemik nekroz",
                "Beyaz Enfarktüs"
            ),
            make_flashcard(
                "k1-24-fc-s49-2",
                "İnsan vücudundaki hemen hemen tüm organlarda enfarktüs koagülatif nekroz ile sonlanırken, hangi organda her zaman sıvılaşma (likuefaksiyon) nekrozu gelişir?",
                "Beyin (santral sinir sistemi) dokusudur.",
                "Yüksek lipid ve hidrolitik enzim zengini serebral parankim",
                "Beyin Enfarktüsü İstisnası"
            ),
            make_flashcard(
                "k1-24-fc-s49-3",
                "Testis torsiyonu veya strangüle fıtık gibi venöz dönüşün engellendiği durumlarda gelişen enfarktüslerin rengi daima ne renktir?",
                "Kırmızı (hemorajik) renktedir.",
                "Tıkanan damardan kanın çıkamayarak dokuda göllenmesi sonucu oluşan kanamalı görünüm",
                "Kırmızı Enfarktüs"
            )
        ],
        "interactiveElements": [
            make_table(
                "Enfarktüs Tipleri ve Organ Eşleştirme Matrisi",
                ["Enfarktüs Tipi", "Vasküler Anatomik Zemin", "Klasik Organ Örnekleri", "Histopatolojik Karşılık"],
                [
                    ["Beyaz (Anemik)", "Uç arterli katı organlar", "Kalp, Dalak, Böbrek", "Koagülatif nekroz"],
                    ["Kırmızı (Hemorajik)", "Çift dolaşım veya venöz tıkanma", "Akciğer, İnce bağırsak, Testis", "Hemorajik koagülatif nekroz"],
                    [
                        "Sıvılaşma (Likuefaktif)",
                        "Serebral arteriyel tıkanma",
                        {"text": "Beyin (Serebrum ve Serebellum)", "isMasked": True, "hint": "Sıvılaşma kavitasyonu gösteren tek primer organ"},
                        "Likuefaksiyon nekrozu (erime)"
                    ]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki eşleştirmelerden hangisi enfarktüs morfolojisi ve patolojisi açısından YANLIŞTIR?",
                {
                    "A": "Böbrek enfarktüsü - Beyaz (anemik) koagülatif nekroz",
                    "B": "Akciğer enfarktüsü - Kırmızı (hemorajik) kama nekroz",
                    "C": "Testis torsiyonu - Kırmızı venöz enfarktüs",
                    "D": "Beyin enfarktüsü - Koagülatif kazeifiye nekroz",
                    "E": "Dalak enfarktüsü - Beyaz kama biçimli enfarktüs"
                },
                "D",
                {
                    "A": "Doğrudur; böbrek uç arterli katı organdır, beyaz koagülatif nekroz olur.",
                    "B": "Doğrudur; akciğer çift dolaşımla kırmızı enfarktüs yapar.",
                    "C": "Doğrudur; venöz staz kırmızı enfarktüs yapar.",
                    "D": "YANLIŞTIR; Beyin enfarktüsünde koagülatif veya kazeifiye nekroz DEĞİL, daima SIVILAŞMA (LİKUEFAKSİYON) NEKROZU görülür.",
                    "E": "Doğrudur; dalak beyaz enfarktüs yapar."
                }
            )
        ]
    })

    # Slayt 50: Bölüm Özeti: Enfarktüs İyileşme Süreci ve Doku Duyarlılığına Geçiş
    slides.append({
        "id": "k1-24-s50",
        "title": "Bölüm Özeti: Enfarktüs İyileşme Süreci ve Doku Duyarlılığına Geçiş",
        "section": "Enfarktüs: Etyoloji, Patogenez ve Sınıflandırma",
        "slideNumber": 50,
        "narrative": (
            "Enfarktüs sınıflamasını ve temel morfolojisini tamamlarken şu kuralları zihnimize kazıyoruz: "
            "1. **Katı Eşittir Beyaz, Çift/Venöz Eşittir Kırmızı:** Bu kural patolojinin en değişmez kanunudur. "
            "2. **Beyin Daima Sıvılaşır:** Diğer organlar koagülatif nekrozla taşlaşırken, beyin eritilip kist olur. "
            "3. **Kama Şekli Damar Ağacıdır:** Üçgen tabanı dışarıda, tepesi içerideki damardadır. "
            "4. **Sonraki Bölüme Köprü:** Bir doku nekroza uğradıktan sonra vücut bu alanı nasıl temizler ve iyileştirir? "
            "Tüm dokuların iskemiye dayanma süresi aynı mıdır? "
            "Bir sonraki bölümümüzde enfarktüs iyileşme dinamiklerini (granülasyon dokusu ve skar), "
            "farklı hücrelerin hipoksi duyarlılıklarını (nöron vs miyosit vs fibroblast) ve septik enfarktüsleri inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İskemik doku nekrozunun ardından ölü hücrelerin makrofajlarca temizlenmesi ve neovaskülarizasyonla fibröz dokuya dönüşmesi granülasyon dokusu aracılığıyla gerçekleşir.",
                "granülasyon dokusu",
                "İyileşme sürecinde yeni damarlar ve fibroblastlardan oluşan geçici doku"
            ),
            make_active_recall(
                "Enfarktüs gelişiminde santral sinir sistemi nöronlarının geri dönüşümsüz hipoksik iskemik nekroza uğramadan önce tolere edebildiği maksimum süre yaklaşık kaç dakikadır?",
                "Yaklaşık 3 - 4 dakikadır.",
                "Nöronların oksijensizliğe dayanabildiği kritik dakika penceresi"
            ),
            make_micro_quiz(
                "Enfarktüs geçiren bir organ parankiminde iyileşme sürecinin sonunda granülasyon dokusunun yerini alan kalıcı tamir dokusu aşağıdakilerden hangisidir?",
                {
                    "A": "Kollajenden zengin Fibröz Skar Dokusu",
                    "B": "Hipertrofik kas tabakası",
                    "C": "Hiyalin kıkırdak plakları",
                    "D": "Kalsifiye kemik iliği trabekülleri",
                    "E": "Mukoid miksoma kütlesi"
                },
                "A",
                {
                    "A": "Bölünme yeteneği olmayan miyosit veya nöron gibi dokularda enfarktüs fibröz skar dokusu ile iyileşir.",
                    "B": "Nekroze kas kendini hipertrofiyle yenileyemez.",
                    "C": "Kıkırdak oluşmaz.",
                    "D": "Kemikleşme gelişmez.",
                    "E": "Miksoma neoplazmdır."
                }
            )
        ]
    })

    return slides
