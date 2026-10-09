# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 7: Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması (Slayt 61 - 70)
Checkpoint 7: Slayt 69
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # Slayt 61: Protein Profili: Whey / Kazein Dengesi ve Sindirilebilirlik
    slides.append({
        "id": "k1-22-s61",
        "title": "Protein Profili: Whey / Kazein Dengesi ve Sindirilebilirlik",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 61,
        "narrative": (
            "Anne sütü ile inek sütü arasındaki en köklü fizyolojik fark protein fraksiyonlarının oranında yatar. "
            "Anne sütünde toplam protein miktarı yaklaşık **0.9-1.2 g/100 ml** olup yeni doğmuş bebeğin böbrek kapasitesine tam uyumludur. "
            "Buna karşın inek sütü **3.3-3.5 g/100 ml** protein içererek bebeğin immatür nefronlarına aşırı solüt yükü bindirir. "
            "Daha da önemlisi protein kalitesidir: Anne sütü proteinlerinin **%60-70'i whey (serum proteini)**, **%30-40'ı kazeindir**. "
            "Whey proteinleri midede asitle temas edince son derece yumuşak, gevşek ve ince floküllü pıhtı oluşturarak 1.5 saatte hızla boşalır. "
            "İnek sütünde ise proteinin **%80'i kazein**, sadece **%20'si wheydir**. "
            "Kazein yoğunluğu midede sert, sindirimi saatler süren devasa küme pıhtıları yapar; bebeğin sindirim kanalını zorlar ve kusmaya zemin hazırlar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki whey-kazein oranı yaklaşık 60-70'e 30-40 iken, inek sütünde kazein baskın olup oran 20'ye 80 şeklindedir.",
                "60-70'e 30-40",
                "Mideyi kolay boşaltan serum ve çökelti fraksiyonu dengesi"
            ),
            make_before_after(
                "Mide İçi Pıhtılaşma ve Boşalma: Anne Sütü vs İnek Sütü",
                "İnek Sütü Alımı",
                "İnek sütü alımı sonrasında midede yüzde seksen kazein içeriği sebebiyle sert, kauçuk kıvamlı dev pıhtılar oluşur; mide boşalması dört saati aşar ve kolik kramplarına yol açar.",
                "Anne Sütü Alımı",
                "Anne sütü alımıyla yüzde altmış-yetmiş whey baskınlığı sayesinde yumuşak, gevşek mikropıhtılar oluşur; mide doksan dakikada fizyolojik olarak boşalır."
            ),
            make_table(
                "Anne Sütü ile İnek Sütü Protein Dağılımı ve Özellikleri",
                ["Biyokimyasal Parametre", "Anne Sütü", "İnek Sütü", "Klinik Yansıması"],
                [
                    ["Toplam Protein", "0.9 - 1.2 g/100 ml", "3.3 - 3.5 g/100 ml", "Böbrek süzme yükü farkı"],
                    [
                        "Whey / Kazein Oranı",
                        {"text": "%60-70 Whey / %30-40 Kazein", "isMasked": True, "hint": "Sindirimi kolay serum fraksiyonunun belirgin üstünlüğü"},
                        "%20 Whey / %80 Kazein",
                        "Mide boşalma süresi ve pıhtı sertliği"
                    ],
                    ["Sindirilebilirlik", "Çok kolay, yumuşak pıhtı", "Zor, kaba pıhtı", "Gastrointestinal tolerans"],
                    ["Gastrik Boşalma Süresi", "~90 dakika", "~240 dakika", "Açlık ve tokluk ritmi"]
                ]
            )
        ]
    })

    # Slayt 62: Alerjenik Fark: Beta-Laktoglobulin Varlığı ve Mutlak Yokluğu
    slides.append({
        "id": "k1-22-s62",
        "title": "Alerjenik Fark: Beta-Laktoglobulin Varlığı ve Mutlak Yokluğu",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 62,
        "narrative": (
            "İnek sütü whey fraksiyonunun en baskın proteini **Beta-laktoglobulindir** (tüm whey proteinlerinin yaklaşık %50'sini oluşturur). "
            "En kritik tıp bilgisi şudur: **İnsan anne sütünde Beta-laktoglobulin ASLA bulunmaz (mutlak yokluk)**. "
            "Beta-laktoglobulin, insan immün sistemi için yabancı bir sığır antijenidir ve bebeklerde gelişen **'İnek Sütü Proteini Alerjisi'nin (İSPA)** "
            "başlıca tetikleyicisidir. İSPA tablosunda bebekte atopik dermatit, hırıltılı solunum, rektal kanama (alerjik proktokolit), "
            "şiddetli kusma ve anafilaksiye kadar varan klinik bulgular gelişebilir. "
            "Buna karşılık anne sütünün ana whey proteini **Alfa-laktalbumindir**. "
            "Alfa-laktalbumin hem laktoz sentaz enziminin düzenleyici alt birimidir hem de zengin esansiyel amino asit kaynağıdır; sıfır alerjeniteye sahiptir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İnek sütünde bol miktarda bulunan fakat insan anne sütünde mutlak olarak bulunmayan en alerjenik whey proteini beta-laktoglobulindir.",
                "beta-laktoglobulin",
                "İnek sütü alerjisinin baş sorumlusu sığır kökenli serum fraksiyonu"
            ),
            make_micro_quiz(
                "İnek sütü ile insan anne sütü protein bileşimi karşılaştırıldığında aşağıdakilerden hangisi biyokimyasal bir gerçektir?",
                {
                    "A": "Beta-laktoglobulin anne sütünde yüksek oranda bulunurken inek sütünde bulunmaz",
                    "B": "Alfa-laktalbumin yalnızca inek sütünde bulunur ve yüksek alerjenite taşır",
                    "C": "Beta-laktoglobulin inek sütünde bol bulunur, insan anne sütünde ise kesinlikle bulunmaz",
                    "D": "Anne sütündeki toplam kazein konsantrasyonu inek sütündekinin üç katıdır",
                    "E": "İnek sütündeki whey fraksiyonu anne sütünden çok daha yüksektir"
                },
                "C",
                {
                    "A": "Yanlıştır; Beta-laktoglobulin insan sütünde ASLA bulunmaz, inek sütüne özgüdür.",
                    "B": "Yanlıştır; Alfa-laktalbumin anne sütünün temel whey proteinidir ve alerjen değildir.",
                    "C": "Doğrudur; Beta-laktoglobulin inek sütünde baskındır, anne sütünde mutlak olarak yoktur ve en önemli alerjendir.",
                    "D": "Yanlıştır; İnek sütündeki kazein (%80) anne sütündekinden (%30-40) çok daha fazladır.",
                    "E": "Yanlıştır; Anne sütünde whey oranı %60-70 iken inek sütünde sadece %20'dir."
                }
            ),
            make_branching_logic(
                "2 aylık bir bebeğe ailesi formül mama yerine ekonomik nedenlerle kaynatılmış tam inek sütü vermeye başlamıştır. "
                "1 hafta sonra bebekte yaygın egzama lezyonları, mukuslu ve çizgisel kanlı dışkılama ile huzursuzluk saptanmıştır.",
                "Bu tablonun patogenezinde rol oynayan ve anne sütünde ASLA bulunmayan protein fraksiyonu hangisidir?",
                [
                    {
                        "text": "Beta-laktoglobulin (İnek sütü whey alerjeni)",
                        "isCorrect": True,
                        "feedback": "Klinik Tanı Doğru: İnek sütü proteini alerjisi gelişmiştir; insan sütünde olmayan Beta-laktoglobulin başlıca tetikleyicidir."
                    },
                    {
                        "text": "Alfa-laktalbumin (Anne sütü whey proteini)",
                        "isCorrect": False,
                        "feedback": "Hatalı: Alfa-laktalbumin anne sütünde boldur ve alerji yapmaz; inek sütüne özgü majör alerjen Beta-laktoglobulindir."
                    },
                    {
                        "text": "Laktoferrin (Demir bağlayıcı antimikrobiyal protein)",
                        "isCorrect": False,
                        "feedback": "Hatalı: Laktoferrin koruyucu immün faktördür, yabancı antijenik alerjen Beta-laktoglobulindir."
                    },
                    {
                        "text": "Sekretuvar IgA (Mukozal koruyucu antikor)",
                        "isCorrect": False,
                        "feedback": "Hatalı: sIgA mukozayı zırh gibi örten koruyucu immünoglobulindir, alerjen değildir."
                    }
                ]
            )
        ]
    })

    # Slayt 63: Nörolojik Gelişim Proteini Taurin ve Serbest Amino Asitler
    slides.append({
        "id": "k1-22-s63",
        "title": "Nörolojik Gelişim Proteini Taurin ve Serbest Amino Asitler",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 63,
        "narrative": (
            "Anne sütü sadece yapısal proteinlerle değil, serbest amino asit profiliyle de mucizevi bir tasarım sunar. "
            "Yenidoğanın karaciğerinde **sistationaz enzimi** immatürdür; bu yüzden metiyoninden sistein ve taurin sentezi son derece kısıtlıdır. "
            "Bu biyokimyasal immatürite nedeniyle **Taurin ve Sistein, yenidoğan ve süt çocuğu için şartlı esansiyeldir**. "
            "Anne sütünde serbest **Taurin konsantrasyonu inek sütüne göre yaklaşık 30-40 kat daha yüksektir**. "
            "Taurin; 1. Beyin korteksi ve nöronal membran stabilizasyonunda, "
            "2. Retina fotoreseptör tabakasının gelişiminde ve görme keskinliğinde, "
            "3. Safra asitlerinin konjugasyonunda (taurokolik asit) ve yağ sindiriminde mutlak gereklidir. "
            "Ayrıca anne sütü tirozinaz yetersizliği nedeniyle düşük fenilalanin ve tirozin içerir; böylece santral sinir sistemi toksisitesi önlenir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Beyin ve retina gelişimi için elzem olan serbest taurin miktarı anne sütünde inek sütüne oranla 30-40 kat daha yüksektir.",
                "taurin",
                "Fotoreseptör ve nöron zarı için kükürtlü serbest amino asit türevi"
            ),
            make_causal_chain(
                "Taurinin Nörolojik ve Bilişsel Gelişim Mekanizması",
                [
                    "1. Hepatik İmmatürite: Yenidoğanda sistationaz enzimi yetersiz olduğundan endojen taurin sentezlenemez.",
                    "2. Anne Sütü Zenginliği: Anne sütündeki yüksek serbest taurin bağırsaktan hızla emilerek dolaşıma geçer.",
                    "3. Kan-Beyin Bariyeri Geçişi: Taurin santral sinir sistemine geçerek nöron membranlarını stabilize eder.",
                    "4. Fotoreseptör Diferansiyasyonu: Retinada fotoreseptör tabakasının sağlıklı olgunlaşmasını ve görme keskinliğini garantiye alır."
                ]
            ),
            make_active_recall(
                "Yenidoğan döneminde taurin ve sistein amino asitlerinin endojen sentezlenemeyip diyetle mutlak alınmasını zorunlu kılan hepatik enzim yetersizliği nedir?",
                "Sistationaz enziminin immatür olmasıdır.",
                "Metiyonin yolundaki kükürtlü basamak enzimi"
            )
        ]
    })

    # Slayt 64: Demir Biyoyararlanımı: %50 Emilim Mucizesi vs %10 Engel
    slides.append({
        "id": "k1-22-s64",
        "title": "Demir Biyoyararlanımı: %50 Emilim Mucizesi vs %10 Engel",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 64,
        "narrative": (
            "Laboratuvar analizinde anne sütü ve inek sütünün demir miktarları birbirine oldukça yakın ve düşüktür (litrede yaklaşık 0.5-0.7 mg). "
            "Ancak tıbbi mucize **biyoyararlanım (emilim yüzdesi)** farkında gizlidir: "
            "Anne sütündeki demirin **%50'si (yarısı)** bebeğin bağırsaklarından doğrudan emilirken, "
            "inek sütündeki demirin sadece **%10'u** emilebilmektedir. "
            "Bu beş katlık olağanüstü emilim farkının mekanizmaları şunlardır: "
            "1. **Laktoferrin:** Demir iyonlarını mükemmel şekilde bağlayarak enterosit yüzeyindeki spesifik reseptörlerine taşır. "
            "2. **Asidik Bağırsak pH'sı:** Bifidus florası ve laktoz sayesinde oluşan asit ortam, demirin çözünür ferroz (Fe2+) formda kalmasını sağlar. "
            "3. **Düşük Fosfor ve Kalsiyum:** İnek sütündeki yüksek kalsiyum ve fosfat demirle çözünmez tuzlar çöktürerek emilimi felç eder; anne sütünde bu engel yoktur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki demirin biyoyararlanımı yaklaşık yüzde elli iken, inek sütündeki demirin yalnızca yüzde onu emilir.",
                "yüzde elli",
                "Anne sütü demirinin yarısının kana geçiş oranı"
            ),
            make_table(
                "Anne Sütü ile İnek Sütü Demir Kinetiği Karşılaştırması",
                ["Demir Parametresi", "Anne Sütü", "İnek Sütü", "Fizyolojik Mekanizma"],
                [
                    ["Toplam Demir Miktarı", "~0.5 mg/L", "~0.5 mg/L", "Kantitatif olarak benzer düzey"],
                    [
                        "Biyoyararlanım (Emilim)",
                        {"text": "%50 emilim", "isMasked": True, "hint": "Yarı yarıya kana geçiş verimi"},
                        "%10 emilim",
                        "Laktoferrin ve pH etkisiyle 5 kat fark"
                    ],
                    ["Taşıyıcı Molekül", "Laktoferrin (Aktif transfer)", "Pasif inorganik difüzyon", "Reseptör aracılı enterosit alımı"],
                    ["GİS Mukozal Kanama", "Yok (Mukozayı korur)", "Mikrokanama yapar", "Alerjik enteropati ve kan kaybı"]
                ]
            ),
            make_micro_quiz(
                "Anne sütü ile inek sütündeki demir metabolizması karşılaştırıldığında aşağıdakilerden hangisi doğrudur?",
                {
                    "A": "İnek sütündeki demir konsantrasyonu anne sütünden 20 kat fazladır",
                    "B": "Anne sütündeki demirin yaklaşık %50'si emilirken, inek sütünde bu oran %10 civarındadır",
                    "C": "İnek sütü laktoferrin açısından anne sütünden çok daha zengindir",
                    "D": "Anne sütü alan bebeklerde ilk 6 ayda rutin demir takviyesi şarttır",
                    "E": "İnek sütündeki yüksek fosfor konsantrasyonu demir emilimini artırır"
                },
                "B",
                {
                    "A": "Yanlıştır; İki sütün de demir miktarı litrede ~0.5 mg olup birbirine yakındır.",
                    "B": "Doğrudur; Anne sütü demirinin biyoyararlanımı %50 olup inek sütünün (%10) tam beş katıdır.",
                    "C": "Yanlıştır; Laktoferrin anne sütünde çok yüksektir, inek sütünde eser düzeydedir.",
                    "D": "Yanlıştır; Term doğan sağlıklı anne sütü alan bebek ilk 4-6 ay kendi depoları ve anne sütüyle idare eder.",
                    "E": "Yanlıştır; Yüksek fosfor demirle çözünmeyen bileşikler oluşturarak emilimi bozar."
                }
            )
        ]
    })

    # Slayt 65: Mineral ve Elektrolit Yükü: Kalsiyum / Fosfor Oranı ve Tetani
    slides.append({
        "id": "k1-22-s65",
        "title": "Mineral ve Elektrolit Yükü: Kalsiyum / Fosfor Oranı ve Tetani",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 65,
        "narrative": (
            "İnek sütü buzağının hızlı iskelet gelişimini sağlamak üzere muazzam miktarda mineral içerir: "
            "Kalsiyum miktarı anne sütünden yaklaşık **3-4 kat**, fosfor miktarı ise tam **6 kat** fazladır. "
            "Ayrıca sodyum, potasyum ve klor iyonları anne sütünün 3 katıdır. "
            "Ancak bebek için kritik olan mineralin toplam miktarı değil, **Kalsiyum / Fosfor (Ca/P) oranıdır**. "
            "Anne sütünde Ca/P oranı ideal kemikleşme ve bağırsak emilimi için mükemmel olan **2 : 1** düzeyindedir. "
            "İnek sütünde ise fosfor aşırı yüksek olduğundan bu oran **1.2 : 1** seviyesine düşer. "
            "Yenidoğana inek sütü verilmesi durumunda aşırı fosfor kana geçer; immatür böbrek fosforu atamaz. "
            "Kanda biriken fosfor kalsiyumu bağlayarak çöktürür ve ağır hipokalsemiye yol açar; bu tablo **'Yenidoğan Hipokalsemik Tetanisi'** olarak adlandırılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütünde kalsiyum fosfor oranı fizyolojik olarak ikiye bir iken, inek sütünde bu oran bire ikiye geriler ve tetani riski yaratır.",
                "ikiye bir",
                "Kemik mineralizasyonu için optimum ikili oran"
            ),
            make_causal_chain(
                "İnek Sütüne Bağlı Yenidoğan Hipokalsemik Tetani Mekanizması",
                [
                    "1. Aşırı Fosfor Alımı: İnek sütü anne sütüne göre 6 kat fazla inorganik fosfor yükler.",
                    "2. İmmatür Renal Klerens: Yenidoğanın glomerüler filtrasyonu ve tübüler fosfat atılımı kısıtlıdır.",
                    "3. Hiperfosfatemi: Kanda fosfat konsantrasyonu hızla yükselerek iyonize kalsiyumu bağlar.",
                    "4. Hipokalsemik Tetani: Serbest kalsiyum düşer; nöromüsküler uyarılabilirlik artar, kasılma ve konvülsiyon gelişir."
                ]
            ),
            make_active_recall(
                "Erken dönemde inek sütüyle beslenen yenidoğanlarda gelişen hipokalsemik tetaninin temel biyokimyasal tetikleyicisi nedir?",
                "İnek sütündeki aşırı fosfor yükünün (anne sütünün 6 katı) immatür böbreklerce atılamayıp kanda kalsiyumu bağlamasıdır.",
                "Aşırı fosfat birikimi ve kalsiyum çökmesi"
            )
        ]
    })

    # Slayt 66: Renal Solüt Yükü ve Ozmolarite: Dehidratasyon Tehdidi
    slides.append({
        "id": "k1-22-s66",
        "title": "Renal Solüt Yükü ve Ozmolarite: Dehidratasyon Tehdidi",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 66,
        "narrative": (
            "Renal Solüt Yükü (RSY); böbrekler yoluyla atılması gereken üre (protein metabolizması ürünü) ile sodyum, potasyum ve klor iyonlarının toplamıdır. "
            "Anne sütünün potansiyel renal solüt yükü yaklaşık **93 mOsm/L** iken, inek sütünün yükü tam üç katına çıkarak **308 mOsm/L** seviyesine ulaşır. "
            "Anne sütünün ozmolaritesi **286-290 mOsm/kg** ile insan plazmasıyla mükemmel bir izoozmolarite gösterir; inek sütü ise **350-400 mOsm/kg** hiperozmolardır. "
            "Yenidoğan böbreğinin idrarı konsantre etme yeteneği erişkinin üçte biri kadardır (maksimum 600-700 mOsm/L). "
            "İnek sütü alan bir bebek bu devasa solüt yükünü atabilmek için idrarla aşırı su kaybetmek (zorunlu ozmotik diürez) zorunda kalır. "
            "Ateş, sıcak hava veya ishal gibi su kaybı durumlarında inek sütüyle beslenen bebek hızla **hipernatremi ve ölümcül dehidratasyona** girer."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütünün renal solüt yükü yaklaşık 93 mOsm/L iken inek sütünde bu yük 308 mOsm/L olup üç katından fazladır.",
                "308 mOsm/L",
                "İnek sütündeki üre ve elektrolitlerin böbreğe bindirdiği devasa ozmotik yük"
            ),
            make_before_after(
                "Böbrek Yükü ve Su Dengesi: Anne Sütü vs İnek Sütü",
                "İnek Sütü Beslenmesi",
                "İnek sütü alımında 308 mOsm/L solüt yükü sebebiyle böbrek idrarı seyreltmek için vücudun tüm serbest suyunu harcar; hafif ateş veya sıcak havada hipernatremik dehidratasyon patlak verir.",
                "Anne Sütü Beslenmesi",
                "Anne sütü alımında 93 mOsm/L düşük solüt yükü sayesinde böbrekler zorlanmaz; bebeğin vücudunda serbest su rezervi kalır ve en sıcak iklimde bile ek suya gerek kalmaz."
            ),
            make_micro_quiz(
                "İnek sütü ile beslenen süt çocuklarının anne sütü alanlara kıyasla hipernatremik dehidratasyona çok daha yatkın olmasının nedeni nedir?",
                {
                    "A": "İnek sütünün su içeriğinin anne sütünden belirgin az olması",
                    "B": "İnek sütündeki yüksek protein ve elektrolitlerin oluşturduğu devasa renal solüt yükü",
                    "C": "İnek sütündeki laktoz konsantrasyonunun aşırı yüksek olması",
                    "D": "İnek sütünün bağırsaktan su emilimini tamamen engellemesi",
                    "E": "Anne sütündeki sodyum miktarının inek sütünden üç kat fazla olması"
                },
                "B",
                {
                    "A": "Yanlıştır; İki sütün de su içeriği yaklaşık %87-88 olup birbirine yakındır.",
                    "B": "Doğrudur; Yüksek protein (üre) ve mineral yükü (308 mOsm/L) böbrekten zorunlu ozmotik su atılımına yol açar.",
                    "C": "Yanlıştır; İnek sütünde laktoz anne sütünden daha düşüktür (%4.8 vs %7).",
                    "D": "Yanlıştır; İnek sütü su emilimini engellemez, böbrekten su kaybını tetikler.",
                    "E": "Yanlıştır; Tam tersine inek sütündeki sodyum anne sütündekinin üç katıdır."
                }
            )
        ]
    })

    # Slayt 67: Yağ Asidi Profili, BSSL Enzimi ve Emilim Verimi
    slides.append({
        "id": "k1-22-s67",
        "title": "Yağ Asidi Profili, BSSL Enzimi ve Emilim Verimi",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 67,
        "narrative": (
            "Anne sütü ile inek sütünün yağ miktarları benzerdir (~3.5-4 g/100 ml), ancak yağın kalitesi ve sindirimi gece ile gündüz kadar farklıdır. "
            "Anne sütü yağlarının **%90-95'i** bağırsaktan eksiksiz emilirken, inek sütü yağının **%20-48'i emilemeyip dışkıyla atılır** (steatoreye eğilim). "
            "Bu farkın nedenleri şunlardır: "
            "1. **Bile Salt-Stimulated Lipase (BSSL):** Anne sütünde duodenuma ulaşınca safra tuzlarıyla aktive olan BSSL enzimi bulunur; "
            "bu enzim immatür pankreas lipazının eksikliğini mükemmel kompanse eder. İnek sütünde BSSL kesinlikle yoktur. "
            "2. **Trigliserit Pozisyonu:** Anne sütünde palmitik asit trigliseridin **sn-2 (orta) pozisyonundadır**; sabunlaşmadan hızla 2-monogliserid olarak emilir. "
            "İnek sütünde ise palmitik asit sn-1 ve sn-3 ucundadır; serbestleşince kalsiyumla birleşerek çözünmez sabunlar oluşturur ve atılır. "
            "3. **PUFA Zenginliği:** Anne sütü linoleik, alfa-linolenik asit ve uzun zincirli çoklu doymamış yağ asitlerinden (DHA, ARA) zengindir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütünde bulunan ve duodenal safra tuzlarıyla aktive olarak yağların yüzde doksan beşinin emilmesini sağlayan enzim BSSL enzimidir.",
                "BSSL",
                "Safra tuzlarınca uyarılan laktasyonel lipaz enzimi"
            ),
            make_table(
                "Anne Sütü ile İnek Sütü Lipid Özelliklerinin Karşılaştırması",
                ["Lipid Özelliği", "Anne Sütü", "İnek Sütü", "Fizyolojik Sonuç"],
                [
                    ["Sindirim Lipazı (BSSL)", "Var (Sütte aktif)", "Yok", "Pankreas immatüritesini kompanse etme"],
                    [
                        "Palmitik Asit Pozisyonu",
                        {"text": "sn-2 pozisyonu (orta)", "isMasked": True, "hint": "Kalsiyumla sabunlaşmayı önleyen merkezi ester bağı"},
                        "sn-1 ve sn-3 pozisyonu",
                        "Kalsiyum sabunu oluşturmadan emilim"
                    ],
                    ["Yağ Emilim Yüzdesi", "%90 - 95", "%60 - 80", "Enerji kaybı ve steatore önleme"],
                    ["DHA ve ARA İçeriği", "Zengin", "Eser / Yok", "Beyin korteksi ve miyelinizasyon"]
                ]
            ),
            make_active_recall(
                "İnek sütündeki palmitik asidin sn-1 ve sn-3 pozisyonunda olmasının bebekte yarattığı iki olumsuz klinik sonuç nedir?",
                "Serbest palmitik asidin kalsiyumla birleşerek kalsiyum sabunları oluşturması, hem yağ emilimini bozması hem de kalsiyum kaybına yol açmasıdır.",
                "Kalsiyum sabunlaşması ve fekal kayıp"
            )
        ]
    })

    # Slayt 68: Neden 1 Yaşından Önce İnek Sütü Verilmez? (Dörtlü Engel)
    slides.append({
        "id": "k1-22-s68",
        "title": "Neden 1 Yaşından Önce İnek Sütü Verilmez? (Dörtlü Engel)",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 68,
        "narrative": (
            "Dünya Sağlık Örgütü (DSÖ) ve Sağlık Bakanlığı yönergelerine göre **yaşamın ilk 1 yılında doğrudan inek sütü verilmesi kesinlikle yasaktır**. "
            "Bu kesin kontrendikasyonun arkasında 4 temel tıbbi ve fizyopatolojik gerekçe yatar: "
            "1. **Gastrointestinal Mikrokanama:** İnek sütü proteinleri immatür bağırsak mukozasında inflamasyon ve mikroskobik kanamalara yol açar; "
            "bebek fark edilmeden dışkıyla sürekli kan kaybeder. "
            "2. **Ağır Demir Eksikliği Anemisi:** Düşük demir biyoyararlanımı (%10) ve mukozal mikrokanamaların birleşimi derin demir eksikliği yaratır. "
            "3. **Yüksek Renal Solüt Yükü (RSY):** Üç kat yüksek protein ve mineral yükü immatür böbreği tüketerek hipernatremik dehidratasyona davetiye çıkarır. "
            "4. **Alerji ve İmmün Reaksiyon:** Beta-laktoglobulin ve sığır kazeini atopik egzama, alerjik kolit ve solunum yolu reaktivitesini tetikler."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İlk bir yaşta inek sütü verilmesinin kesinlikle yasaklanmasının başlıca nedeni bağırsakta mikroskobik kanama ve demir eksikliği anemisi yapmasıdır.",
                "mikroskobik kanama",
                "Dışkıyla gizli kan kaybına yol açan mukozal hasar"
            ),
            make_causal_chain(
                "1 Yaş Altında İnek Sütü Verilmesinin Anemi Patogenezi",
                [
                    "1. Yabancı Antijen Teması: İnek sütü kazeini ve beta-laktoglobulini bağırsak mukozasına temas eder.",
                    "2. Mukozal Enteropati: İmmün inflamasyon sonucu villuslarda mikroerozyonlar ve gizli kanama başlar.",
                    "3. Fekal Demir Kaybı: Bebek her gün dışkıyla mikroskobik düzeyde eritrosit ve demir kaybeder.",
                    "4. Ağır Refrakter Anemi: İnek sütünün emilmeyen demiri bu kaybı karşılayamaz ve derin demir eksikliği anemisi oturur."
                ]
            ),
            make_micro_quiz(
                "Süt çocukluğu döneminde ilk 1 yaş içerisinde tam inek sütü başlanmasının kesin kontrendike olmasının gerekçeleri arasında hangisi yer almaz?",
                {
                    "A": "Gastrointestinal kanalda mikroskobik kanamalara yol açması",
                    "B": "Yüksek renal solüt yükü ile böbrekleri zorlaması ve dehidratasyon riski",
                    "C": "Beta-laktoglobulin içeriği nedeniyle yüksek alerjenite taşıması",
                    "D": "İçerdiği laktoz miktarının anne sütünden çok daha yüksek olup ozmotik ishal yapması",
                    "E": "Demir emilim oranının son derece düşük (%10) olması"
                },
                "D",
                {
                    "A": "Yer alır; İnek sütü bağırsakta mikrokanama yaparak demir kaybına yol açar.",
                    "B": "Yer alır; 308 mOsm/L RSY böbreğe aşırı yük bindirir.",
                    "C": "Yer alır; Beta-laktoglobulin en güçlü sığır alerjenidir.",
                    "D": "Yer almaz; Tam tersine inek sütünün laktozu (%4.8) anne sütünden (%7) daha düşüktür; bu ifade yanlıştır.",
                    "E": "Yer alır; İnek sütündeki demirin sadece %10'u emilebilir."
                }
            )
        ]
    })

    # Slayt 69: [TEKRAR SAYFASI - CHECKPOINT 7] Anne Sütü ile İnek Sütü Biyokimyasal Farkları
    slides.append({
        "id": "k1-22-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Anne Sütü ile İnek Sütü Biyokimyasal Farkları",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 69,
        "narrative": (
            "Bu checkpoint sayfasında, anne sütü ile inek sütünün protein fraksiyonları, alerjenite farkları, "
            "demir biyoyararlanımı ve renal solüt yükü karşılaştırmalarını pekiştiriyoruz: "
            "1. **Protein Profili:** Anne sütü %60-70 whey / %30-40 kazein içerir ve yumuşak mikropıhtı yapar. "
            "İnek sütü %80 kazein içerir ve sindirimi çok zor kaba pıhtı oluşturur. "
            "2. **Alerjenite:** İnek sütü majör alerjeni Beta-laktoglobulin insan sütünde ASLA bulunmaz. "
            "3. **Taurin:** Retina ve beyin gelişimi için şart olan taurin anne sütünde 30-40 kat fazladır. "
            "4. **Demir:** Miktarları benzer olsa da biyoyararlanım anne sütünde %50, inek sütünde sadece %10'dur. "
            "5. **Mineral Dengesi:** Anne sütünde Ca/P oranı 2:1 iken inek sütünde 1.2:1'dir; inek sütü hipokalsemik tetani tetikleyebilir. "
            "6. **Böbrek Yükü:** İnek sütünün renal solüt yükü (308 mOsm/L) anne sütünün (93 mOsm/L) 3 katıdır ve hipernatremik dehidratasyona zemin hazırlar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "flashcards": [
            make_flashcard(
                "k1-22-fc-s69-1",
                "İnek sütünde bol miktarda bulunan fakat insan anne sütünde mutlak olarak bulunmayan majör alerjenik protein hangisidir?",
                "Beta-laktoglobulin proteinidir.",
                "Sığır serum fraksiyonuna özgü alerjen molekül",
                "Alerjenik Biyokimya"
            ),
            make_flashcard(
                "k1-22-fc-s69-2",
                "Anne sütü ile inek sütünün demir biyoyararlanım (bağırsaktan emilim) oranları sırasıyla yüzde kaçtır?",
                "Anne sütünde yüzde elli, inek sütünde yüzde on oranındadır.",
                "Biri yarısı düzeyinde diğeri onda bir seviyesinde emilir",
                "Mikro Besin Biyoyararlanımı"
            ),
            make_flashcard(
                "k1-22-fc-s69-3",
                "İnek sütünün renal solüt yükü yaklaşık kaç mOsm/L olup anne sütünün kaç katıdır?",
                "Yaklaşık 308 mOsm/L olup anne sütünün üç katından fazladır.",
                "Üç yüzün üzerindeki böbrek süzme ozmolaritesi",
                "Renal Fizyoloji"
            )
        ],
        "interactiveElements": [
            make_table(
                "Özet Karşılaştırma Matrisi: Anne Sütü vs İnek Sütü",
                ["Kriter / Bileşen", "Anne Sütü", "İnek Sütü", "Fizyolojik Avantaj"],
                [
                    ["Whey / Kazein", "60:40 (Whey baskın)", "20:80 (Kazein baskın)", "Hızlı ve yumuşak gastrik boşalma"],
                    [
                        "Beta-Laktoglobulin",
                        {"text": "Yok (Sıfır)", "isMasked": True, "hint": "İnsan sütünde mutlak bulunmayan alerjenik molekül"},
                        "Var (Baskın whey)",
                        "Alerji ve egzama riskini sıfırlama"
                    ],
                    ["Demir Emilimi", "%50 emilim", "%10 emilim", "Laktoferrinle maksimum kana geçiş"],
                    ["Renal Solüt Yükü", "93 mOsm/L", "308 mOsm/L", "Dehidratasyondan koruyan düşük yük"]
                ]
            )
        ]
    })

    # Slayt 70: Bölüm Özeti: Biyokimyasal Karşılaştırmadan Başarılı Emzirme Yönetimine Geçiş
    slides.append({
        "id": "k1-22-s70",
        "title": "Bölüm Özeti: Biyokimyasal Karşılaştırmadan Başarılı Emzirme Yönetimine Geçiş",
        "section": "Anne Sütü ile İnek Sütünün Biyokimyasal Karşılaştırması",
        "slideNumber": 70,
        "narrative": (
            "Anne sütü ile inek sütünün detaylı biyokimyasal analizi, insan sütünün türümüze özgü mükemmel bir biyomühendislik eseri olduğunu kanıtlamıştır. "
            "Düşük ama yüksek kaliteli protein, whey baskınlığı (%60), Beta-laktoglobulinin mutlak yokluğu, "
            "30-40 kat yüksek serbest taurin, %50 demir biyoyararlanımı, 2:1 Ca/P dengesi ve düşük renal solüt yükü (93 mOsm/L) "
            "bebeğin hassas organlarını aşırı yükten korurken büyümesini optimize eder. "
            "İlk bir yılda inek sütünden kesin kaçınma kuralı, mikrokanama ve anemi profilaksisinin temel taşıdır. "
            "Bir sonraki bölümde, bu paha biçilmez besinin bebeğe ulaştırılmasını garanti eden **'Başarılı Emzirme Yönetimi, "
            "Doğru Pozisyon, Bebek Dostu Hastane İlkeleri ve Süt Saklama Koşulları'** konusuna adım atıyoruz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_active_recall(
                "Anne sütünün inek sütüne kıyasla bebeğe sunduğu en kritik üç biyokimyasal üstünlük nedir?",
                "Whey baskın protein yapısı (%60), Beta-laktoglobulin içermemesi ve demir emiliminin 5 kat yüksek (%50) olmasıdır.",
                "Protein kalitesi, alerjen yokluğu ve demir emilim oranı"
            ),
            make_branching_logic(
                "Polikliniğe başvuran bir anne, 3 aylık bebeğine formül mamanın pahalı gelmesi nedeniyle piyasadan aldığı pastörize inek sütünü sulandırarak vermeyi düşündüğünü belirtiyor.",
                "Hekim olarak bu anneye verilecek en doğru ve kanıta dayalı bilimsel yaklaşım hangisidir?",
                [
                    {
                        "text": "İnek sütünün 1 yaşından önce mikroskobik bağırsak kanaması, anemi ve böbrek yetmezliği riski nedeniyle kesinlikle yasak olduğunu anlatmak ve anne sütünü artırma yöntemlerini planlamak",
                        "isCorrect": True,
                        "feedback": "Mükemmel Klinik Yaklaşım: İlk 1 yaşta inek sütü mutlak kontrendikedir; öncelik emzirmenin desteklenmesi veya uygun formül mamanın sağlanmasıdır."
                    },
                    {
                        "text": "İnek sütünü yarı yarıya sulandırıp içine şeker ekleyerek verebileceğini söylemek",
                        "isCorrect": False,
                        "feedback": "Hatalı ve Tehlikeli: Sulandırmak solüt yükünü düşürse de enerji yoğunluğunu çökertir, protein kalitesini düzeltmez ve bağırsak mikrokanamasını engellemez."
                    },
                    {
                        "text": "İnek sütünü iyice kaynattıktan sonra demir damlası ekleyerek başlamasını önermek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Kaynatma Beta-laktoglobulini ve renal solüt yükünü ortadan kaldırmaz; 1 yaşından önce inek sütü kesinlikle verilmez."
                    }
                ]
            )
        ]
    })

    return slides
