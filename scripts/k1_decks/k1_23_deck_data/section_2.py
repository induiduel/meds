# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 2: Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey (Slayt 11 - 20)
Checkpoint 2: Slayt 19
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # Slayt 11: Anne Ölümü (Maternal Mortality) DSÖ Tanımı ve 42 Gün Kuralı
    slides.append({
        "id": "k1-23-s11",
        "title": "Anne Ölümü (Maternal Mortality) DSÖ Tanımı ve 42 Gün Kuralı",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 11,
        "narrative": (
            "Dünya Sağlık Örgütü (DSÖ) ve Uluslararası Hastalık Sınıflandırması (ICD) kriterlerine göre **Anne Ölümü**: "
            "'Kadının gebelik süresince veya gebeliğin sonlanmasından sonraki **ilk 42 gün (6 hafta) içinde**, "
            "gebeliğin süresine ve yerine (intrauterin veya ektopik) bakılmaksızın, "
            "gebelik durumunun kendisinden veya gebelik yönetiminden kaynaklanan ya da bu süreçlerin ağırlaştırdığı "
            "herhangi bir nedenden ölmesidir'. "
            "Burada iki hayati epidemiyolojik kural vardır: "
            "1. **Zaman Sınırı (42 Gün):** Doğumdan sonraki ilk 42 gün puerperium (lohusalık) evresi olup gebeliğin hemodinamik etkilerinin sürdüğü dönemdir. "
            "2. **Hariç Tutulanlar:** Kaza (trafik kazası, düşme vb.) veya tesadüfi nedenler (ör. deprem, ateşli silah yaralanması) "
            "gebe kadında meydana gelse bile ASLA anne ölümü sınıflandırmasına dahil edilmez."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Anne ölümü gebelik süresince veya gebelik bittikten sonraki ilk kırk iki gün içinde obstetrik nedenlerle meydana gelen ölümdür.",
                "ilk kırk iki gün içinde",
                "Doğum sonrası lohusalık süresine denk gelen altı haftalık epidemiyolojik sınır"
            ),
            make_micro_quiz(
                "Dünya Sağlık Örgütü'nün standart 'Anne Ölümü' tanımına göre aşağıdakilerden hangisi bir anne ölümü vakası olarak KABUL EDİLEMEZ?",
                {
                    "A": "Doğumdan 10 gün sonra ağır lohusalık kanaması (atoni) nedeniyle vefat eden kadın",
                    "B": "Gebelikte preeklampsiye bağlı konvülsiyon geçirip 32. haftada ölen kadın",
                    "C": "Doğumdan 20 gün sonra puerperal sepsis ve septik şok nedeniyle ölen kadın",
                    "D": "Doğum yaptıktan 15 gün sonra bindiği yolcu otobüsünün kaza yapması sonucu ölen kadın",
                    "E": "Ektopik (dış) gebelik rüptürüne bağlı hemorajik şoktan kaybedilen kadın"
                },
                "D",
                {
                    "A": "Anne ölümüdür; Doğum sonrası 42 gün içinde doğrudan obstetrik kanamadır.",
                    "B": "Anne ölümüdür; Gebelikte toksemiye bağlı doğrudan obstetrik nedendir.",
                    "C": "Anne ölümüdür; Lohusalık döneminde doğrudan enfeksiyon komplikasyonudur.",
                    "D": "Anne Ölümü Değildir; Kaza veya tesadüfi nedenler gebe/lohusa kadında görülse dahi anne ölümü sayılmaz.",
                    "E": "Anne ölümüdür; Ektopik gebelik gebelik yeri neresi olursa olsun obstetrik nedendir."
                }
            ),
            make_active_recall(
                "Bir kadının ölümünün anne ölümü (maternal mortality) sayılabilmesi için doğumdan sonra en fazla kaç gün içinde gerçekleşmiş olması şarttır?",
                "Doğumu izleyen ilk 42 gün (6 hafta) içinde gerçekleşmiş olması şarttır.",
                "Lohusalık süresini kapsayan gün sayısı"
            )
        ]
    })

    # Slayt 12: Anne Ölüm Oranı (AÖO) Formülü ve 100.000 Çarpanı
    slides.append({
        "id": "k1-23-s12",
        "title": "Anne Ölüm Oranı (AÖO) Formülü ve 100.000 Çarpanı",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 12,
        "narrative": (
            "Epidemiyolojide anne ölümlerinin büyüklüğü **Anne Ölüm Oranı (Maternal Mortality Ratio - MMR)** ile ölçülür. "
            "Formül şöyledir: "
            "$$\\text{Anne Ölüm Oranı} = \\frac{\\text{Bir yılda obstetrik nedenlerle ölen kadın sayısı}}{\\text{Aynı yıldaki toplam canlı doğum sayısı}} \\times 100.000$$ "
            "Bu formülde iki kritik metodolojik özellik bulunur: "
            "1. **Paydada 'Canlı Doğum' Kullanılması:** İdeal payda 'gebe kadın sayısı' olmalıdır; ancak düşükler ve erken kayıplar tam kayıt altına "
            "alınamadığından, gebelik riskine maruz kalan kadın popülasyonunu en güvenilir temsil eden payda canlı doğum sayısıdır. "
            "2. **Çarpanın 100.000 Olması:** Anne ölümleri genel nüfusa oranla nadir görülen trajik olaylar olduğundan, "
            "çıkan ondalık sayıyı anlaşılır tam sayılara dönüştürmek için çarpan olarak **yüz bin (100.000)** kullanılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Anne ölüm oranı hesaplanırken formülde payda olarak canlı doğum sayısı kullanılır ve sonuç yüz bin katsayısıyla çarpılır.",
                "yüz bin",
                "Nadir görülen maternal ölümleri tamsayıya çeviren yüz binlik çarpan"
            ),
            make_table(
                "Anne Ölümü Göstergeleri ve Epidemiyolojik Formülleri",
                ["Gösterge Adı", "Pay (Ölçülen Olay)", "Payda (Risk Altındaki Popülasyon)", "Çarpan"],
                [
                    [
                        "Anne Ölüm Oranı (MMR)",
                        "Obstetrik nedenli anne ölüm sayısı",
                        {"text": "Aynı yıldaki canlı doğum sayısı", "isMasked": True, "hint": "Gebelik maruziyetini temsil eden kayıtlı doğum parametresi"},
                        "100.000 Canlı Doğumda"
                    ],
                    ["Anne Ölüm Hızı (MMRate)", "Obstetrik nedenli anne ölüm sayısı", "15-49 yaş doğurganlık çağı kadın sayısı", "100.000 Kadında"],
                    ["Bebek Ölüm Hızı (BÖH)", "1 yaş altı ölen bebek sayısı", "Aynı yıldaki canlı doğum sayısı", "1.000 Canlı Doğumda"]
                ]
            ),
            make_active_recall(
                "Anne ölüm oranı (AÖO) formülünde paydada 'toplam gebe kadın sayısı' yerine neden 'canlı doğum sayısı' kullanılır?",
                "Tüm gebeliklerin (özellikle erken spontan ve indüklenmiş düşüklerin) tam ve güvenilir olarak kaydedilmesinin imkansız olmasıdır.",
                "Erken gebelik kayıt güçlüğü ve güvenilir doğum verisi"
            )
        ]
    })

    # Slayt 13: Doğrudan ve Dolaylı Obstetrik Nedenler Ayrımı
    slides.append({
        "id": "k1-23-s13",
        "title": "Doğrudan ve Dolaylı Obstetrik Nedenler Ayrımı",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 13,
        "narrative": (
            "Anne ölümleri klinik patofizyolojilerine göre iki ana sınıfa ayrılır: "
            "1. **Doğrudan (Direkt) Obstetrik Nedenler:** Yalnızca gebelik, doğum ve lohusalık durumuna özgü olan; "
            "gebelik durumunun fizyolojisinden, komplikasyonlarından veya hatalı/yetersiz obstetrik yönetimden kaynaklanan ölümlerdir. "
            "Örnekler: Postpartum atoni kanaması, preeklampsi-eklampsi, puerperal sepsis, amniyon sıvı embolisi, ektopik gebelik rüptürü ve anestezi komplikasyonları. "
            "Gelişmekte olan ülkelerdeki anne ölümlerinin %70-80'i doğrudan nedenlidir ve **tamamen önlenebilir niteliktedir**. "
            "2. **Dolaylı (İndirekt) Obstetrik Nedenler:** Gebelikten önce var olan veya gebelikte ortaya çıkan, doğrudan obstetrik kökenli olmayan "
            "ancak gebeliğin artmış kardiyovasküler ve metabolik yüküyle ağırlaşarak ölüme yol açan sistemik hastalıklardır. "
            "Örnekler: Romatizmal kalp kapak hastalığı, peripartum kardiyomiyopati, kronik böbrek yetmezliği, tüberküloz, diyabet ve ağır anemi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Yalnızca gebelik, doğum ve lohusalık komplikasyonlarına bağlı olarak gelişen ve önlenebilir olan ölümlere doğrudan obstetrik ölüm denir.",
                "doğrudan obstetrik ölüm",
                "Obstetrik sürece özgü kanama ve toksemi gibi primer nedenler"
            ),
            make_table(
                "Doğrudan ve Dolaylı Anne Ölümü Nedenlerinin Karşılaştırması",
                ["Kriter / Özellik", "Doğrudan (Direkt) Nedenler", "Dolaylı (İndirekt) Nedenler"],
                [
                    ["Etiyolojik Köken", "Gebelik ve doğuma özgü komplikasyonlar", "Önceden var olan veya ağırlaşan sistemik hastalıklar"],
                    [
                        "Klasik Klinik Örnekler",
                        {"text": "Postpartum kanama, preeklampsi, lohusalık sepsisi", "isMasked": True, "hint": "Obstetrik triad ve enfeksiyon komplikasyonları"},
                        "Kalp kapak hastalığı, kronik hipertansiyon, anemi"
                    ],
                    ["Önlenebilirlik Oranı", "Son derece yüksek (>%80-90)", "Kısmen önlenebilir (Multidisipliner izlemle)"],
                    ["Gelişmekte Olan Ülkelerdeki Payı", "Ezici çoğunluk (%70-80)", "Azınlık payı (%20-30)"]
                ]
            ),
            make_micro_quiz(
                "Anne ölümlerinin sınıflandırılmasında aşağıdakilerden hangisi 'Doğrudan (Direkt) Obstetrik Ölüm' grubuna girer?",
                {
                    "A": "Gebelikte ağırlaşan romatizmal mitral kapak darlığına bağlı kalp yetmezliği",
                    "B": "Doğum sonrasında uterus atonisi nedeniyle durdurulamayan masif kanama",
                    "C": "Gebelik sırasında ilerleyen kronik böbrek yetmezliği",
                    "D": "Gebelikte immün baskılanmaya bağlı alevlenen akciğer tüberkülozu",
                    "E": "Gebelikte derinleşen kronik aplastik anemi"
                },
                "B",
                {
                    "A": "Dolaylı Nedendir; Kalp kapak hastalığı sistemik kardiyak patolojidir.",
                    "B": "Doğrudan Nedendir; Postpartum kanama ve atoni yalnızca doğuma özgü doğrudan obstetrik komplikasyondur.",
                    "C": "Dolaylı Nedendir; Renal patoloji sistemiktir.",
                    "D": "Dolaylı Nedendir; Tüberküloz enfeksiyöz sistemik hastalıktır.",
                    "E": "Dolaylı Nedendir; Hematolojik hastalık gebelikle ağırlaşmıştır."
                }
            )
        ]
    })

    # Slayt 14: Doğrudan Obstetrik Nedenler: Kanama, Toksemi ve Sepsis
    slides.append({
        "id": "k1-23-s14",
        "title": "Doğrudan Obstetrik Nedenler: Kanama, Toksemi ve Sepsis",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 14,
        "narrative": (
            "Doğrudan anne ölümlerinin %75'inden sorumlu olan **'Ölümcül Üçlü' (Lethal Triad)** şunlardır: "
            "1. **Postpartum Hemoraji (Aşırı Kanama):** Dünya genelinde anne ölümlerinin bir numaralı nedenidir. "
            "En sık etken **Uterus Atonisidir** (myometriumun doğum sonrası kasılamaması). "
            "Ayrıca plasenta dekolmanı, plasenta previa ve doğum yolu yırtıkları da masif hemorajik şoka yol açar. "
            "Doğumun aktif yönetimi ve rutin profilaktik oksitosin ile %90'ı önlenebilir. "
            "2. **Gebelik Toksemisi (Preeklampsi / Eklampsi):** Plasental iskemi sonucu gelişen endotel disfonksiyonudur. "
            "Hipertansiyon, ödem ve proteinüri triadı konvülsiyonlara (eklampsi), intrakraniyal kanamaya veya HELLP sendromuna dönebilir. "
            "3. **Puerperal Sepsis (Lohusalık Enfeksiyonu):** Doğum sırasında hijyen eksikliği veya uzamış membran rüptürü sonucu "
            "uterus içine patojenlerin invazyonuyla septik şok tablosu gelişir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Dünya genelinde ve gelişmekte olan ülkelerde doğrudan anne ölümlerinin en sık görülen ve en hızlı öldüren nedeni postpartum kanamadır.",
                "postpartum kanamadır",
                "Uterus atonisinin tetiklediği aşırı lohusalık kanaması"
            ),
            make_causal_chain(
                "Uterus Atonisine Bağlı Maternal Ölüm Zinciri",
                [
                    "1. Myometrium Yorgunluğu: Uzamış doğum eylemi veya aşırı gerilmiş uterus doğum sonrası kasılamaz.",
                    "2. Spiral Arterlerin Açık Kalması: Myometrium lifleri 'canlı ligatür' görevini yapamaz; spiral damarlar boşluğa kanar.",
                    "3. Masif Hipovolemik Şok: Dakikalar içinde 1000-1500 ml kan kaybedilir; doku perfüzyonu çöker.",
                    "4. Koagülopati ve Ölüm: Tüketim koagülopatisi (DİK) ve kardiyak arrest gelişir; acil müdahale hayat kurtarır."
                ]
            ),
            make_active_recall(
                "Postpartum kanamayı önlemek amacıyla doğum eyleminin üçüncü evresinde (bebeğin çıkışından hemen sonra) rutin uygulanan farmakolojik altın standart ilaç nedir?",
                "Profilaktik intramüsküler veya intravenöz Oksitosin uygulamasıdır.",
                "Uterusu sıkarak hemostaz sağlayan uterotonik hormon"
            )
        ]
    })

    # Slayt 15: Dolaylı Obstetrik Nedenler: Kardiyak Hastalıklar ve Anemi
    slides.append({
        "id": "k1-23-s15",
        "title": "Dolaylı Obstetrik Nedenler: Kardiyak Hastalıklar ve Anemi",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 15,
        "narrative": (
            "Gelişmiş ülkelerde ve anne ölüm oranı düşen toplumlarda doğrudan nedenler kontrol altına alındıkça "
            "**Dolaylı (İndirekt) Nedenlerin payı göreceli olarak artar**: "
            "1. **Maternal Kalp Hastalıkları:** Gebelikte plazma hacmi %40-50 artar, kardiyak debi %30-50 yükselir. "
            "Bu devasa fizyolojik yük; altta yatan subklinik mitral darlığı, aort koarktasyonu veya konjenital kalp defekti olan "
            "kadında 28-32. haftalarda veya doğum anında akut akciğer ödemi ve kardiyojenik şoka yol açar. "
            "Ayrıca gebeliğe özgü **Peripartum Kardiyomiyopati** ani ventriküler iflas yapabilir. "
            "2. **Ağır Anemi (Hb < 7 g/dl):** Gebelik öncesi yetersiz beslenme veya sık doğumlarla tükenen demir depoları derinleşir. "
            "Şiddetli anemi doku hipoksisi, kalp yetmezliği ve doğumda normal miktardaki bir kan kaybını bile tolere edemeyerek ölümcül şok yaratır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gebelikte plazma hacminin yüzde elli artması kompanse kalp kapak hastalıklarını dekompanse ederek dolaylı anne ölümüne yol açabilir.",
                "yüzde elli",
                "Gebeliğin hemodinamik plazma ekspansiyon oranı"
            ),
            make_table(
                "Dolaylı Anne Ölümü Nedenleri ve Gebelikteki Ağırlaşma Mekanizmaları",
                ["Sistemik Hastalık", "Gebelik Öncesi Durum", "Gebelikte Ağırlaşma Mekanizması", "Ölümcül Sonuç"],
                [
                    [
                        "Mitral Kapak Darlığı",
                        "Hafif semptomatik veya sessiz",
                        {"text": "Plazma hacmi ve taşikardi artışı", "isMasked": True, "hint": "Gebelikte kardiyak debi ve kalp hızının yükselmesi"},
                        "Akut pulmoner ödem ve kardiyojenik şok"
                    ],
                    ["Şiddetli Anemi (Hb < 7)", "Kronik demir açlığı", "Fetal demir çekimi ve hemodilüsyon", "Hipoksik kalp yetmezliği ve şok"],
                    ["Kronik Hipertansiyon", "Esansiyel hipertansiyon", "Süperempoze preeklampsi gelişimi", "Serebrovasküler kanama"],
                    ["Gestasyonel Diyabet", "Gizli insülin direnci", "Plasental hormonlarla ketoasidoz", "Diyabetik koma ve intrauterin ölüm"]
                ]
            ),
            make_active_recall(
                "Birinci basamak gebe izleminde hemoglobin değeri kaç g/dl'nin altına düştüğünde maternal kalp yetmezliği ve ölüm riski nedeniyle acil sevk zorunludur?",
                "Hemoglobin değeri 7 g/dl'nin altına (Hb < 7 g/dl) düştüğünde acil üst merkeze sevk edilmelidir.",
                "Ağır anemi ve acil sevk hemoglobin eşiği"
            )
        ]
    })

    # Slayt 16: Türkiye'de Anne Ölüm Oranı Trendi ve 2024 Düzeyi (11.5)
    slides.append({
        "id": "k1-23-s16",
        "title": "Türkiye'de Anne Ölüm Oranı Trendi ve 2024 Düzeyi (11.5)",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 16,
        "narrative": (
            "Türkiye, son çeyrek asırda anne ölümlerini düşürmede tüm dünyaya örnek gösterilen muazzam bir halk sağlığı başarısına imza atmıştır: "
            "1. **Tarihsel Düşüş:** 1970'lerde 100.000 canlı doğumda 200'lerin üzerinde, 1990'larda yaklaşık 130 olan Anne Ölüm Oranı; "
            "1998'de 68'e, 2005'te 28.5'e ve **2024 yılı itibarıyla 11.5 / 100.000 canlı doğuma gerilemiştir**. "
            "2. **Bu Başarının Temel Dinamikleri:** "
            "- Hastanede ve eğitimli sağlık personeli eşliğinde doğum oranının **%99'un üzerine çıkarılması**, "
            "- Birinci basamakta aile hekimliği gebe izlemlerinin düzenli yapılması (%90'ın üzerinde 4+ DÖB), "
            "- Ücretsiz doğum, acil obstetrik bakım ve ambulans sevk zincirinin (hava ambulansları dahil) kurulması, "
            "- Misafir Anne Projesi ile kışın yolu kapanan köylerdeki gebelerin doğum öncesinde ilçe merkezlerindeki otel/hastanelerde misafir edilmesi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de Sağlık Bakanlığı 2024 verilerine göre Anne Ölüm Oranı yüz bin canlı doğumda 11.5 seviyesine gerilemiştir.",
                "11.5",
                "Türkiye'nin 2024 yılı anne ölüm oranı resmi değeri"
            ),
            make_before_after(
                "Türkiye'de Anne Ölüm Oranı Evrimi: 1990'lar vs 2024",
                "1990'lar Başlangıç Dönemi",
                "AÖO yüz binde yüz otuzun üzerindedir; kırsalda ev doğumları yaygındır, geleneksel ebe müdahaleleriyle kanama ve sepsis ölümleri sıradandır.",
                "2024 Güncel Dönemi",
                "AÖO yüz binde 11.5'e inmiştir; doğumların yüzde doksan dokuzu hastanede gerçekleşir, acil obstetrik bakım ve misafir anne modeli aktiftir.",
                "Anne ölüm oranındaki tarihi başarı süreci"
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı resmi verilerine göre Türkiye'de 2024 yılı Anne Ölüm Oranı (100.000 canlı doğumda) yaklaşık kaçtır?",
                {
                    "A": "1.2",
                    "B": "11.5",
                    "C": "45.0",
                    "D": "82.3",
                    "E": "130.0"
                },
                "B",
                {
                    "A": "Yanlıştır; 1.2 henüz ulaşılamamış aşırı düşük bir değerdir.",
                    "B": "Doğrudur; Türkiye 2024 yılı anne ölüm oranı 11.5/100.000 canlı doğumdur.",
                    "C": "Yanlıştır; 45.0 eski yılların verisidir.",
                    "D": "Yanlıştır; Çok yüksektir.",
                    "E": "Yanlıştır; 1990'ların başındaki düzeydir."
                }
            )
        ]
    })

    # Slayt 17: Türkiye'de Bölgesel Eşitsizlikler ve Sosyoekonomik Farklar
    slides.append({
        "id": "k1-23-s17",
        "title": "Türkiye'de Bölgesel Eşitsizlikler ve Sosyoekonomik Farklar",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 17,
        "narrative": (
            "Türkiye genel ortalaması 11.5 olsa da, halk sağlığı analizlerinde **bölgesel eşitsizlikler** dikkatle incelenmelidir: "
            "1. **Bölgesel Uç Noktalar (2024 Verileri):** "
            "- **En Yüksek Bölge:** **Kuzeydoğu Anadolu (Erzurum, Erzincan, Bayburt vb.)** bölgesinde AÖO **14.2 / 100.000** ile ulusal ortalamanın üzerindedir. "
            "Nedenleri: Zorlu coğrafi arazi koşulları, kış aylarında ulaşım güçlükleri, kırsal nüfus yoğunluğu ve geciken hastane başvuruları. "
            "- **En Düşük Bölge:** **Doğu Karadeniz (Trabzon, Rize, Artvin vb.)** bölgesinde o yıl kayıtlı **0.0 / 100.000** ile anne ölümü görülmemiştir. "
            "2. **Kırsal-Kentsel Uçurum:** Kırsal kesimde 4 ve daha fazla DÖB alma oranı (%84) kentsel alanlara (%92) göre daha geridedir. "
            "Halk sağlığının nihai hedefi bölgesel makasları kapatarak tüm Türkiye'de anne ölümünü sıfıra yaklaştırmaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de 2024 verilerine göre anne ölüm oranının en yüksek olduğu bölge yüz binde 14.2 ile Kuzeydoğu Anadolu bölgesidir.",
                "Kuzeydoğu Anadolu",
                "Zorlu kış şartları ve coğrafi engellerin ölümleri artırdığı bölge"
            ),
            make_table(
                "Türkiye'de Bölgelere Göre Anne Ölüm Oranı Dağılımı (2024)",
                ["Bölge Adı", "Anne Ölüm Oranı (100.000 Canlı Doğumda)", "Bölgesel Dinamik / Risk Faktörü"],
                [
                    ["Türkiye Geneli", "11.5", "Ulusal ortalama ve genel başarı düzeyi"],
                    [
                        "Kuzeydoğu Anadolu",
                        {"text": "14.2", "isMasked": True, "hint": "En yüksek mortaliteye sahip bölgesel oran"},
                        "En yüksek bölge; dağınık yerleşim ve kış ulaşım zorlukları"
                    ],
                    ["Doğu Karadeniz", "0.0", "En düşük bölge; o yıl sıfır anne ölümü kaydedilmiştir"]
                ]
            ),
            make_active_recall(
                "Sağlık Bakanlığı verilerine göre Türkiye'de 2024 yılında Anne Ölüm Oranının en yüksek saptandığı coğrafi bölge hangisidir?",
                "Kuzeydoğu Anadolu bölgesidir (14.2 / 100.000).",
                "En yüksek maternal mortaliteye sahip bölge"
            )
        ]
    })

    # Slayt 18: Anne Ölümlerini Önleme Komisyonları ve Sürveyans Sistemi
    slides.append({
        "id": "k1-23-s18",
        "title": "Anne Ölümlerini Önleme Komisyonları ve Sürveyans Sistemi",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 18,
        "narrative": (
            "Türkiye'de anne ölümlerinin bu denli keskin düşürülmesinin arkasındaki en güçlü yönetsel mekanizma "
            "**Anne Ölümleri Sürveyans Sistemi (RAM)** ve denetim komisyonlarıdır: "
            "1. **Zorunlu Bildirim:** 15-49 yaş grubundaki herhangi bir kadının ölümü gerçekleştiğinde sistem otomatik alarm verir. "
            "Ölen kadının son 1 yıl içinde gebe veya lohusa olup olmadığı MERNİS ve Sağlık Bilgi Sistemleri üzerinden derhal sorgulanır. "
            "2. **İl İnceleme Komisyonları:** Meydana gelen her bir anne ölümü için il düzeyinde bağımsız bir uzman komisyonu (kadın doğumcu, "
            "halk sağlığı uzmanı, anestezi uzmanı) toplanır. "
            "3. **Önlenebilirlik Analizi:** 'Bu ölüm önlenebilir miydi?', 'Hangi basamakta hata yapıldı?' soruları araştırılır. "
            "Gecikme nerede yaşandı: 1. Karar vermede gecikme, 2. Ulaşımda gecikme, 3. Sağlık kuruluşunda müdahalede gecikme. "
            "Hata saptanan süreçler hızla revize edilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Her anne ölümü vakasının önlenebilirlik ve sistemik aksaklıklar açısından araştırılması amacıyla il inceleme komisyonları kurulur.",
                "il inceleme komisyonları",
                "Maternal ölümleri bağımsız inceleyen uzman heyetleri"
            ),
            make_causal_chain(
                "Anne Ölümü Sürveyansı ve Geri Bildirim Süreci",
                [
                    "1. Otomatik Tespit: 15-49 yaş kadın ölümü sistemde maternal sorgulamayı tetikler.",
                    "2. Dosya İncelemesi: Gebelik takipleri, sevk süresi ve hastane epikrizleri toplanır.",
                    "3. Komisyon Değerlendirmesi: Uzman heyet doğrudan/dolaylı nedeni ve önlenebilirliği raporlar.",
                    "4. Sistematik Düzeltme: Protokol ihlali varsa sevk zinciri veya hastane altyapısı derhal güçlendirilir."
                ]
            ),
            make_micro_quiz(
                "Maternal mortalite analizlerinde kullanılan 'Üç Gecikme Modeli'ne (Three Delays Model) göre ikinci gecikme basamağı hangisidir?",
                {
                    "A": "Ailenin sağlık kuruluşuna gitme kararı almasındaki gecikme",
                    "B": "Sağlık kuruluşuna ulaşım ve nakil sırasındaki gecikme",
                    "C": "Hastaneye vardıktan sonra uygun tıbbi müdahalenin yapılmasındaki gecikme",
                    "D": "Doğum sonrasında emzirmenin başlatılmasındaki gecikme",
                    "E": "Bebeğin nüfus müdürlüğüne tescil edilmesindeki gecikme"
                },
                "B",
                {
                    "A": "1. Gecikmedir; Karar verme aşamasıdır.",
                    "B": "2. Gecikmedir; Coğrafi engel, ambulans ve yol nedeniyle merkeze ulaşım gecikmesidir.",
                    "C": "3. Gecikmedir; Sağlık personelinin ve ekipmanın müdahale gecikmesidir.",
                    "D": "Obstetrik gecikme modeli dışındadır.",
                    "E": "Bürokratik süreçtir, tıbbi gecikmeyle ilgisi yoktur."
                }
            )
        ]
    })

    # Slayt 19: [TEKRAR SAYFASI - CHECKPOINT 2] Anne Ölüm Göstergeleri ve Değerlendirme
    slides.append({
        "id": "k1-23-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Anne Ölüm Göstergeleri ve Değerlendirme",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 19,
        "narrative": (
            "Bu ikinci checkpoint sayfasında, anne ölümü epidemiyolojisini, nedenlerini ve Türkiye verilerini pekiştiriyoruz: "
            "1. **Anne Ölümü Tanımı:** Gebelikte veya doğumdan sonraki ilk 42 gün içinde obstetrik nedenlerle ölüm; kaza/tesadüfi nedenler hariçtir. "
            "2. **Formül:** 1 yıldaki obstetrik ölümler / Canlı doğum sayısı $\\times$ 100.000. "
            "3. **Doğrudan Nedenler:** Yalnızca gebelik ve doğuma özgü komplikasyonlar (postpartum kanama, preeklampsi/eklampsi, lohusalık sepsisi); %80 önlenebilir. "
            "4. **Dolaylı Nedenler:** Gebelikle ağırlaşan sistemik hastalıklar (kalp kapak hastalığı, kardiyomiyopati, ağır anemi Hb < 7). "
            "5. **Türkiye 2024:** Anne Ölüm Oranı 11.5 / 100.000; en yüksek Kuzeydoğu Anadolu (14.2), en düşük Doğu Karadeniz (0.0). "
            "6. **Önleme Stratejileri:** %99 hastanede doğum, acil obstetrik bakım ve Misafir Anne Projesi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s19-1",
                "DSÖ tanımına göre bir ölümün anne ölümü (maternal mortality) sayılması için doğumdan sonra en fazla kaç gün içinde gerçekleşmesi gerekir?",
                "Doğumdan sonraki ilk kırk iki gün içinde gerçekleşmesi gerekir.",
                "Lohusalık sürecine denk gelen altı haftalık süre sınırı",
                "Epidemiyolojik Tanımlar"
            ),
            make_flashcard(
                "k1-23-fc-s19-2",
                "Türkiye'de Sağlık Bakanlığı'nın açıkladığı 2024 yılı resmi Anne Ölüm Oranı (AÖO) yüz bin canlı doğumda kaçtır?",
                "Yüz bin canlı doğumda on bir buçuktur (11.5).",
                "On bir ile on iki arasındaki resmi ulusal değer",
                "Ulusal Sağlık Göstergeleri"
            ),
            make_flashcard(
                "k1-23-fc-s19-3",
                "Doğrudan anne ölümlerinin dünyada en sık görülen ve acil uterotonik ilaçlarla önlenebilen kardinal nedeni nedir?",
                "Uterus atonisine bağlı postpartum kanamadır.",
                "Miyometriyum kas liflerinin gevşekliğinden kaynaklanan masif hemoraji",
                "Obstetrik Komplikasyonlar"
            )
        ],
        "interactiveElements": [
            make_table(
                "Özet Tablo: Anne Ölümü Epidemiyolojisi",
                ["Parametre / Soru", "Doğru Bilimsel Yanıt", "Klinik / Halk Sağlığı Anlamı"],
                [
                    ["Süre Sınırı", "Gebelikte veya doğumdan sonra ilk 42 gün", "Lohusalık hemodinamiğini kapsar"],
                    [
                        "Hariç Tutulan Durumlar",
                        {"text": "Kaza ve tesadüfi nedenler", "isMasked": True, "hint": "Obstetrik süreç dışı travma ve olaylar"},
                        "Trafik kazası, cinayet veya afetler"
                    ],
                    ["Hesaplama Çarpanı", "100.000 canlı doğum", "Nadir olay standardizasyonu"],
                    ["Türkiye 2024 Değeri", "11.5 / 100.000", "Sağlıkta dönüşümün büyük başarısı"],
                    ["En Sık Neden", "Postpartum kanama (Atoni)", "Doğumun 3. evresinin aktif yönetimiyle önlenir"]
                ]
            )
        ]
    })

    # Slayt 20: Bölüm Özeti: Anne Ölümlerinden Doğum Öncesi Bakımın Tarihçesine Geçiş
    slides.append({
        "id": "k1-23-s20",
        "title": "Bölüm Özeti: Anne Ölümlerinden Doğum Öncesi Bakımın Tarihçesine Geçiş",
        "section": "Anne Ölümü: Tanım, Ölçütler, Nedenler ve Küresel-Ulusal Düzey",
        "slideNumber": 20,
        "narrative": (
            "Anne ölümleri analizi, doğrudan obstetrik nedenlerin (kanama, eklampsi, sepsis) %80-90 oranında önlenebilir olduğunu, "
            "dolaylı nedenlerin ise gebeliğin erken haftalarında saptanarak kontrol altına alınabileceğini göstermiştir. "
            "Bu önlenebilirliğin dünyadaki bir numaralı anahtarı **Doğum Öncesi Bakım (DÖB)** hizmetleridir. "
            "Bir kadının gebeliği boyunca düzenli sağlık personeli kontrolünden geçmesi; hem anne ölümlerini hem de "
            "ölü doğum ve prematürite riskini dramatik şekilde azaltır. "
            "Peki DÖB dünyada ve Türkiye'de nasıl doğdu? Geçmişte önerilen 13 izlemden günümüzdeki 4 izleme nasıl gelindi? "
            "Bakımın kalitesini ölçen Kessner İndeksi nedir? "
            "Üçüncü bölümümüzde, **'Doğum Öncesi Bakımın Tarihçesi, 224 Sayılı Kanun, Kessner İndeksi ve TNSA-2018 Verileri'** "
            "tüm detaylarıyla incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Anne ölümlerini ve düşük doğum ağırlıklı bebek oranını düşürmede en maliyet-etkili birinci basamak müdahale nedir?",
                "Eğitimli sağlık personeli tarafından verilen düzenli Doğum Öncesi Bakımdır (DÖB).",
                "Gebelikte periyodik koruyucu izlem hizmeti"
            ),
            make_branching_logic(
                "Birinci basamakta çalışan bir hekim, gebe bir kadının 34. haftada şiddetli baş ağrısı, görmede bulanıklık ve epigastrik ağrıyla başvurduğunu görüyor. Tansiyonu 165/110 mmHg, idrarda +++ protein saptanıyor.",
                "Bu hastada acil yapılması gereken hayat kurtarıcı yönetim hangisidir?",
                [
                    {
                        "text": "Şiddetli Preeklampsi tanısıyla derhal damar yolu açmak, Magnezyum Sülfat yüklemesi ve antihipertansif tedavi başlayarak acil donanımlı 3. basamak obstetrik merkeze sevk etmek",
                        "isCorrect": True,
                        "feedback": "Mükemmel Acil Obstetrik Karar: Hasta eklampsi ve konvülsiyon eşiğindedir; MgSO4 konvülsiyon profilaksisidir ve acil sevk anne-bebek hayatını kurtarır."
                    },
                    {
                        "text": "Hastaya migren teşhisi koyup parasetamol yazarak evine istirahate göndermek",
                        "isCorrect": False,
                        "feedback": "Ölümcül Hata: Hipertansiyon ve proteinüri toksemidir, migren değildir; hasta evde konvülsiyon geçirip ölebilir."
                    },
                    {
                        "text": "Tansiyonun gebelikte normal olduğunu söyleyip 38. haftada kontrole çağırmak",
                        "isCorrect": False,
                        "feedback": "Tıbbi Malpraktis: 165/110 mmHg acil hipertansif krizdir, ertelenemez."
                    }
                ]
            )
        ]
    })

    return slides
