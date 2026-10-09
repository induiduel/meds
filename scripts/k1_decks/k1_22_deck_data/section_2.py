# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 2: Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim (Slayt 11 - 20)
Checkpoint 2: Slayt 19
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # Slayt 11: Bebeklikte Ağırlık Artış Paterni: Fizyolojik Tartı Kaybı
    slides.append({
        "id": "k1-22-s11",
        "title": "Bebeklikte Ağırlık Artış Paterni: Fizyolojik Tartı Kaybı",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 11,
        "narrative": (
            "Yenidoğan bebek dünyaya geldiğinde tartı eğrisi düz bir yükseliş göstermez. "
            "Doğumu takip eden ilk 3-5 gün içinde bebeklerde **%5 ila %10 arasında fizyolojik bir ağırlık kaybı (tartı kaybı)** yaşanır. "
            "Bu geçici kilo kaybının temel fizyopatolojik nedenleri: "
            "1. Ekstrasellüler sıvı fazlalığının idrar ve terle atılması (fizyolojik diürez), "
            "2. Mekonyumun (ilk yapışkan koyu dışkı) vücuttan boşalması, "
            "3. İlk günlerde anne sütü (kolostrum) miktarının az hacimli (ancak yoğun konsantre) olmasıdır. "
            "Sağlıklı ve yeterli emzirilen bir bebeğin **10 ila 14. günlerde doğum ağırlığına geri dönmesi** beklenir. "
            "Eğer bir bebek ilk haftada doğum ağırlığının %10'undan fazlasını kaybetmişse veya 14. günde doğum tartısına "
            "ulaşamamışsa, mutlaka emzirme tekniği hatası, yetersiz süt alımı veya altta yatan organik bir patoloji araştırılmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan bebeklerde ilk günlerde görülen fizyolojik kilo kaybının ardından 10-14. günde doğum ağırlığına geri dönülmesi beklenir.",
                "10-14. günde",
                "İkinci haftanın nihayetinde doğum kilosuna yeniden ulaşma süresi"
            ),
            make_causal_chain(
                "Yenidoğanda Fizyolojik Tartı Kaybı ve Toparlanma Aşamaları",
                [
                    "1. Doğum: Fetal ekstrasellüler sıvı birikimi ve mekonyum ile tartım yapılır.",
                    "2. 1-4. Günler: Sıvı diürezi ve dışkılama ile vücut ağırlığının %5-10'u kaybedilir.",
                    "3. 5-7. Günler: Geçiş sütünün inmesi ve kalori alımının artmasıyla kilo kaybı durur.",
                    "4. 10-14. Günler: Günlük 20-30 gram tartı artışıyla bebek doğum kilosuna yeniden ulaşır."
                ]
            ),
            make_active_recall(
                "Yenidoğanda doğumdan sonraki ilk günlerde gerçekleşen tartı kaybının fizyolojik kabul edilen üst sınırı nedir?",
                "Doğum ağırlığının en fazla %10'u kadardır (%10'u aşan kayıplar patolojik kabul edilir ve dehidratasyon alarmıdır).",
                "Yüzdelik maksimal normal kayıp eşiği"
            )
        ]
    })

    # Slayt 12: Ağırlık Katlanma Dönüm Noktaları: 4-6. Ayda 2 Kat, 1 Yaşında 3 Kat
    slides.append({
        "id": "k1-22-s12",
        "title": "Ağırlık Katlanma Dönüm Noktaları: 4-6. Ayda 2 Kat, 1 Yaşında 3 Kat",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 12,
        "narrative": (
            "Bebeklik döneminde büyüme hızı yaşamın diğer tüm evrelerinden kat kat yüksektir. "
            "Klinik pratikte hekimlerin ve hemşirelerin bebeğin büyümesini değerlendirirken kullandığı altın kurallar şunlardır: "
            "- **4. - 6. Aylarda:** Bebek doğum ağırlığının **yaklaşık 2 katına** ulaşır (ortalama 3.3 kg doğan bebek 6. ayda ~6.6-7 kg olur). "
            "- **1 Yaşında:** Bebek doğum ağırlığının **tam 3 katına** ulaşır (~10 kg). "
            "- **İkinci Yaşam Yılında:** Büyüme hızı fizyolojik olarak yavaşlar; bebeğin 2. yıl boyunca kazandığı toplam ağırlık "
            "yaklaşık doğum ağırlığı kadardır (~2.5-3 kg). "
            "Bu olağanüstü kütle artışı, bebeğin kilogram başına enerji, protein ve su ihtiyacının neden bir yetişkinden "
            "2-3 kat daha fazla olduğunu biyolojik olarak açıklar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Sağlıklı bir bebek 4-6. ayda doğum ağırlığının iki katına, 1 yaşında ise üç katına ulaşır.",
                "1 yaşında ise üç katına",
                "İlk yaş dönümünde doğum kilosunun ulaştığı katlama düzeyi"
            ),
            make_table(
                "Bebeklikte Yaşa Göre Tartı Katlanma Kuralları",
                ["Gelişimsel Dönüm Noktası", "Beklenen Tartı Düzeyi", "Tipik Ağırlık Örneği (3.3 kg Doğum İçin)"],
                [
                    ["Doğum Anı", "Doğum Ağırlığı (1x)", "3.3 kg (Standart persentil)"],
                    [
                        "4 - 6. Aylar",
                        {"text": "Doğum ağırlığının 2 katı", "isMasked": True, "hint": "Yarım yaş civarında gerçekleşen ikiye katlanma"},
                        "~6.6 - 7.0 kg"
                    ],
                    ["1 Yaş Sonu", "Doğum ağırlığının 3 katı", "~10.0 kg"],
                    ["2 Yaş Sonu", "Doğum ağırlığının 4 katı", "~12.5 - 13.0 kg"]
                ]
            ),
            make_micro_quiz(
                "Doğum ağırlığı 3200 gram olan miadında sağlıklı bir bebeğin 1 yaş kontrolünde beklenen yaklaşık ağırlığı nedir?",
                {
                    "A": "6400 gram",
                    "B": "7500 gram",
                    "C": "9600 gram",
                    "D": "12800 gram",
                    "E": "15000 gram"
                },
                "C",
                "Doğru cevap C'dir: 1 yaşında doğum ağırlığının 3 katına ulaşılması kuralı uyarınca: 3200 g × 3 = 9600 g (9.6 kg) olması beklenir. A seçeneği (6400 g) 5-6. ay beklentisidir (2 katı)."
            )
        ]
    })

    # Slayt 13: Boy ve Baş Çevresi Gelişimi: İlk Yılda %50 Artış
    slides.append({
        "id": "k1-22-s13",
        "title": "Boy ve Baş Çevresi Gelişimi: İlk Yılda %50 Artış",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 13,
        "narrative": (
            "Bebeklikte yalnızca tartı değil, lineer boy uzaması ve nöral dokunun aynası olan baş çevresi de "
            "baş döndürücü bir hızla ilerler: "
            "- **Boy Uzaması:** Term yenidoğanın ortalama boyu 50 cm'dir. "
            "İlk bir yılda bebeğin boyu **yaklaşık %50 oranında artarak 1 yaşında 75 cm'ye** ulaşır! "
            "Daha sonra uzama yavaşlar ve çocuk **4 yaşına geldiğinde doğum boyunun 2 katına (100 cm)** ulaşır. "
            "- **Baş Çevresi:** Doğumda ortalama 35 cm'dir ve göğüs çevresinden 1-2 cm daha geniştir. "
            "İlk yılda yaklaşık 12 cm artarak 1 yaşında 47 cm'ye ulaşır; bu artış beynin hızla büyüdüğünün kanıtıdır. "
            "Yetersiz beslenme ilk aşamada tartıyı, kronikleştiğinde ise boy uzamasını ve baş çevresini vurur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğanda ortalama 50 cm olan boy ilk yılda yüzde elli artarak 1 yaşında 75 cm'ye, 4 yaşında ise doğum boyunun iki katına ulaşır.",
                "yüzde elli",
                "İlk 12 ayda boyun yarısı kadar uzamasını ifade eden oran"
            ),
            make_before_after(
                "İlk Yıl Boy Artışı ile 4 Yaş Boy Düzeyi Kıyası",
                "1 Yaş Sonu Boy Gelişimi",
                "Doğum boyuna göre %50 artış göstererek 50 cm'den yaklaşık 75 cm düzeyine ulaşır.",
                "4 Yaş Sonu Boy Gelişimi",
                "Büyümenin kümülatif devamıyla doğum boyunun tam 2 katına (ortalama 100 cm) erişir.",
                "Süt çocukluğu hızlı uzama evresi ile okul öncesi dönem boy katlanması karşılaştırması"
            ),
            make_active_recall(
                "Kronik malnütrisyon ile akut açlık tablosunun boy ve tartı parametreleri üzerindeki temel ayrımı nedir?",
                "Akut açlık öncelikle tartıyı düşürür (wasting/çelimsizlik); aylar süren kronik yetersiz beslenme ise boy uzamasını durdurarak bodurluğa (stunting) yol açar.",
                "Akut tartı kaybı ile kronik boy duraklaması farkı"
            )
        ]
    })

    # Slayt 14: Vücut Bileşiminin Değişimi: Su Oranının Gerilemesi ve Yağlanma
    slides.append({
        "id": "k1-22-s14",
        "title": "Vücut Bileşiminin Değişimi: Su Oranının Gerilemesi ve Yağlanma",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 14,
        "narrative": (
            "Yenidoğanın vücut kompozisyonu erişkinden radikal biçimde farklıdır ve ilk yılda hızla değişir: "
            "- **Vücut Su Oranı:** Yenidoğanda toplam vücut suyu **vücut ağırlığının %70'ini (prematürelerde %80'ini)** oluşturur. "
            "Bu suyun büyük kısmı hücre dışı (ekstrasellüler) alandadır. "
            "Bir yaşın sonunda hücre içi kütlenin ve yağ dokusunun artmasıyla toplam vücut suyu **%60'a geriler** (erişkin düzeyi). "
            "Ekstrasellüler sıvının bu denli yüksek olması, bebeği ishal ve kusma durumunda dakikalar içinde ölümcül hipovolemiye sokabilir. "
            "- **Yağ Dokusu:** Yağ oranı doğumda %12-14 iken, ilk 9 ayda hızla artarak %25'e çıkar. "
            "Bu fizyolojik yağlanma, miyelinizasyon, termoregülasyon ve hızlı büyüme için kalori deposu işlevi görür."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan vücudunun yüzde yetmişi sudan oluşurken, bir yaşın sonunda bu oran yüzde altmışa geriler.",
                "yüzde yetmişi",
                "Doğum anındaki yüksek vücut su fraksiyonu"
            ),
            make_table(
                "Bebeklikte Vücut Sıvı ve Yağ Kompozisyonu Değişimi",
                ["Yaşam Evresi", "Toplam Vücut Suyu (%)", "Ekstrasellüler Sıvı Payı", "Klinik Yansıması"],
                [
                    ["Prematüre Bebek", "%80 - 85", "Çok yüksek", "Olağanüstü yüksek dehidratasyon hassasiyeti"],
                    [
                        "Term Yenidoğan",
                        {"text": "%70", "isMasked": True, "hint": "Zamanında doğan bebeğin sıvı ağırlık oranı"},
                        "Yüksek (Hücre dışı baskın)",
                        "Fizyolojik tartı kaybı ve su ihtiyacı"
                    ],
                    ["1 Yaşında Çocuk", "%60", "Dengeli", "Erişkin benzeri kompartıman dağılımı"],
                    ["Erişkin Birey", "%55 - 60", "İntrasellüler baskın", "Standart fizyolojik tamponlama"]
                ]
            ),
            make_micro_quiz(
                "Yenidoğan ve erken süt çocukluğu döneminde vücut su oranının yüksek olması ile ilgili hangisi doğrudur?",
                {
                    "A": "Bebekler sıvı kaybına yetişkinlerden çok daha dayanıklıdır ve susuz kalmazlar",
                    "B": "Vücut suyu doğumda %70 olup, ishal ve kusmada hızla hipovolemik şok gelişebilir",
                    "C": "Hücre içi sıvı hacmi hücre dışı sıvı hacminden 3 kat daha fazladır",
                    "D": "Bebeklerin böbrekleri suyu mükemmel konsantre ederek sıvı kaybını sıfırlar",
                    "E": "Bir yaşına gelindiğinde vücut su oranı %30'a kadar geriler"
                },
                "B",
                "Doğru cevap B'dir: Yenidoğanda su oranı %70'tir ve büyük bölümü ekstrasellülerdir; bu dinamik sıvı devir hızını yükseltir ve ishale bağlı dehidratasyon riskini katbekat artırır. A, C, D ve E tamamen hatalıdır."
            )
        ]
    })

    # Slayt 15: Sindirim Sistemi İmmadüritesi I: Mide Kapasitesi
    slides.append({
        "id": "k1-22-s15",
        "title": "Sindirim Sistemi İmmadüritesi I: Mide Kapasitesi",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 15,
        "narrative": (
            "Bebek beslenmesinde porsiyon ve sıklık kurallarını belirleyen en somut anatomik sınır **mide kapasitesidir**. "
            "Yenidoğan bir bebeğin anatomik mide hacmi: "
            "- Doğumun ilk günü: **Yalnızca 10 - 20 ml** (küçük bir kiraz veya ceviz büyüklüğünde), "
            "- Birinci haftanın sonu: **Yaklaşık 60 - 90 ml**, "
            "- Birinci ayın sonu: **90 - 150 ml**, "
            "- Bir yaşın sonunda: **Yaklaşık 250 ml** (standart bir su bardağı) hacme ulaşır. "
            "**Klinik Çıkarım:** "
            "Doğumdan hemen sonra bebeğe 50-60 ml mama veya su vermeye kalkışmak mideyi aşırı gererek regürjitasyona, "
            "kusmaya, aspirasyona ve mide rüptürüne zemin hazırlar. "
            "İlk günlerde salgılanan kolostrumun damla damla ve küçük hacimlerde (öğün başına 5-15 ml) gelmesi, "
            "bebeğin minik mide kapasitesiyle kusursuz bir biyolojik senkronizasyon içindedir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan bir bebeğin mide kapasitesi doğumda 10-20 ml iken bir yaşın sonunda yaklaşık 250 ml düzeyine ulaşır.",
                "10-20 ml",
                "İlk günlerdeki kiraz-ceviz büyüklüğündeki mililitre hacmi"
            ),
            make_causal_chain(
                "Mide Hacmi ile Emzirme Sıklığı İlişkisi",
                [
                    "1. Minik Kapasite: Doğumda mide ancak 10-20 ml hacim barındırabilir.",
                    "2. Hızlı Boşalma: Anne sütü hafif pıhtılaşır ve 1.5-2 saatte duodenuma geçer.",
                    "3. Sık Acıkma: Bebek günde 8-12 kez (2-3 saatte bir) açlık belirtisi gösterir.",
                    "4. İsteğe Bağlı Emzirme: Saat kısıtlaması olmadan bebek her istedikçe emzirilmelidir."
                ]
            ),
            make_active_recall(
                "İlk günlerde annelerin 'sütüm çok az geliyor, sadece birkaç damla' kaygısına hekim anatomik olarak nasıl yanıt vermelidir?",
                "Yenidoğanın mide kapasitesinin doğumda sadece 10-20 ml olduğu, birkaç damla kolostrumun bu minik mideyi tam doyurduğu ve fazlasının kusmaya yol açacağı anlatılarak anne rahatlatılmalıdır.",
                "Mide hacmi ve kolostrum uyumu açıklaması"
            )
        ]
    })

    # Slayt 16: Sindirim Sistemi İmmadüritesi II: Gastrik Asidite ve Pepsin
    slides.append({
        "id": "k1-22-s16",
        "title": "Sindirim Sistemi İmmadüritesi II: Gastrik Asidite ve Pepsin",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 16,
        "narrative": (
            "Yenidoğan bebeğin midesi sadece hacim olarak küçük değil, biyokimyasal olarak da immatürdür: "
            "- **Düşük Gastrik Asidite (Yüksek pH):** Yetişkinlerde mide pH'sı 1.5-2.0 iken, yenidoğanda mide pH'sı 4.0-6.0 civarındadır. "
            "Bu yüksek pH'nın iki zıt sonucu vardır: "
            "1. Olumlu: Anne sütündeki koruyucu immünglobulinler (sIgA) ve laktoferrin asitte denatüre olmadan bozulmaksızın bağırsağa geçer. "
            "2. Olumsuz: Midenin asit bariyeri zayıftır; kontamine gıdalardaki bakteriler kolayca bağırsağa sızabilir. "
            "- **Pepsin Aktivitesi:** Pepsinogen salgısı ve asidik aktivasyonu düşüktür. "
            "Ancak anne sütündeki whey proteinleri (albümin, laktalbümin) düşük pepsinde bile kolayca sindirilirken, "
            "inek sütündeki kazein kalın pıhtılar oluşturarak sindirilemez ve bebeğe ağır gelir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan midesinde gastrik asiditenin düşük olması anne sütündeki sekretuvar IgA ve koruyucu proteinlerin parçalanmadan bağırsağa geçmesini sağlar.",
                "koruyucu proteinlerin",
                "Bağışıklık antikorları ve antimikrobiyal enzimlerin sağlam kalması"
            ),
            make_before_after(
                "Yenidoğan Mide Asiditesi ile Yetişkin Midesi Ayrımı",
                "Yenidoğan Mide Ortamı",
                "pH 4.0 - 6.0 civarındadır; antikorlar ve enzimler tahrip olmadan sağlam bağırsağa ulaşır.",
                "Yetişkin Mide Ortamı",
                "pH 1.5 - 2.0 kuvvetli asidiktir; tüm proteinleri ve bakterileri hızla denatüre eder.",
                "Antikor koruyucu yüksek pH ortamı ile bakterisidal kuvvetli asit ortamı farkı"
            ),
            make_active_recall(
                "Yenidoğan midesinde pepsin ve asit salgısının düşük olması anne sütü sindirimini engeller mi?",
                "Hayır engellemez; anne sütündeki proteinler (whey ağırlıklı) yumuşak pıhtı oluşturarak düşük enzim düzeylerinde bile kolayca sindirilir.",
                "Whey proteini ve düşük pepsin sindirilebilirliği"
            )
        ]
    })

    # Slayt 17: Ekzokrin Pankreas ve Safra Fonksiyonları: Yağ ve Karbonhidrat Emilimi
    slides.append({
        "id": "k1-22-s17",
        "title": "Ekzokrin Pankreas ve Safra Fonksiyonları: Yağ ve Karbonhidrat Emilimi",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 17,
        "narrative": (
            "Bebeklikte duodenal sindirim enzimleri kademeli olarak olgunlaşır: "
            "- **Pankreatik Amilaz Yetersizliği:** Pankreatik alfa-amilaz aktivitesi ilk 4-6 ayda son derece düşüktür; "
            "bu nedenle nişastalı katı gıdalar (pirinç unu, patates, tahıllar) 6 aydan önce verilirse sindirilemez, "
            "kolonda fermantasyona uğrayarak gaz sancısı, meteorizm ve ozmotik diyareye yol açar. "
            "- **Pankreatik Lipaz ve Safra Tuzu Düşüklüğü:** Yenidoğanda safra asidi havuzu ve pankreatik lipaz yetersizdir. "
            "Buna rağmen anne sütü alan bebek yağları mükemmel sindirir! Bunun nedeni: "
            "1. Anne sütünde bulunan **Safra Tuzu Bağımlı Lipaz (BSSL)** enziminin sütün kendi yağlarını bağırsakta sindirmesi, "
            "2. Dil kökünden salgılanan lingual lipazın midede yağ sindirimini başlatmasıdır. "
            "İnek sütü veya hayvansal yağlar ise lipaz içermediğinden yağların %20-48'i sindirilmeden feçesle (steatore) atılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İlk aylarda pankreatik amilaz aktivitesinin yetersiz olması nedeniyle nişastalı ek gıdalar 6 aydan önce sindirilemez.",
                "pankreatik amilaz",
                "Nişasta ve kompleks karbonhidratları yıkan sindirim salgısı"
            ),
            make_table(
                "Bebeklikte Sindirim Enzimlerinin Olgunlaşma Zamanlaması",
                ["Sindirim Enzimi", "Bebeklikteki Düzeyi", "Klinik Beslenme Yansıması"],
                [
                    [
                        "Pankreatik Amilaz",
                        {"text": "İlk 4-6 ayda çok düşüktür", "isMasked": True, "hint": "Kompleks nişasta sindiriminin gecikme nedeni"},
                        "Nişastalı katı besinler 6. aydan önce kesinlikle verilmemelidir"
                    ],
                    ["Pankreatik Lipaz", "İlk aylarda yetersizdir", "Anne sütündeki BSSL enzimi ve lingual lipaz bu açığı kapatır"],
                    ["Laktaz Enzimi", "Doğumda tam aktiftir", "Anne sütündeki yüksek laktozu mükemmel sindirir"],
                    ["Safra Tuzları", "Havuz küçüktür", "Ağır hayvansal yağlar feçesle atılır; anne sütü yağı iyi emilir"]
                ]
            ),
            make_micro_quiz(
                "Bebeklerde pankreatik lipaz yetersiz olmasına rağmen anne sütündeki yağların %95 oranında emilebilmesinin sırrı nedir?",
                {
                    "A": "Bebeklerin midesinde aşırı miktarda pepsin üretilmesi",
                    "B": "Anne sütünün kendi içinde Safra Tuzu Bağımlı Lipaz (BSSL) enzimi taşıması",
                    "C": "Anne sütündeki yağların tamamının suda çözünen karbonhidratlara dönüşmesi",
                    "D": "Bebek kalın bağırsağının yağları doğrudan emebilmesi",
                    "E": "Pankreatik amilazın lipaz görevini üstlenmesi"
                },
                "B",
                "Doğru cevap B'dir: Anne sütü biyolojik bir mucize olarak Safra Tuzu Bağımlı Lipaz (BSSL) enzimi içerir; süt bağırsağa ulaştığında bu enzim aktifleşerek sütün kendi yağlarını sindirir ve bebek pankreasının yetersizliğini telafi eder."
            )
        ]
    })

    # Slayt 18: Renal Fonksiyon İmmadüritesi ve Yüksek Renal Solüt Yükü
    slides.append({
        "id": "k1-22-s18",
        "title": "Renal Fonksiyon İmmadüritesi ve Yüksek Renal Solüt Yükü",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 18,
        "narrative": (
            "Bebek böbreği anatomik olarak mevcut olmakla birlikte fizyolojik açıdan son derece **immatürdür**: "
            "- **Düşük Glomerüler Filtrasyon Hızı (GFH):** Yenidoğanda GFH erişkinin yaklaşık üçte biri kadardır. "
            "- **Düşük Konsantrasyon Kapasitesi:** Yetişkin böbreği idrarı 1200-1400 mOsm/kg konsantre edebilirken, "
            "yenidoğan böbreği en fazla **600-700 mOsm/kg** konsantre edebilir; Henle kulpu kısadır ve medüller osmotik gradyan düşüktür. "
            "**Renal Solüt Yükü (RSY) Tehlikesi:** "
            "Besinlerle alınan protein yıkım ürünleri (üre) ve elektrolitler (Na, K, Cl, P) böbrekten atılmak zorundadır. "
            "Anne sütü düşük protein ve ideal elektrolit içeriğiyle çok düşük bir renal solüt yükü oluşturur (286 mOsm/kg). "
            "Buna karşın inek sütü veya aşırı konsantre mamalar 3 kat fazla protein ve mineral içerir (400 mOsm/kg); "
            "bu durum immatür böbreği aşırı zorlar, idrarla zorunlu su kaybına yol açar ve bebeği süratle hipernatremiye sokar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan böbreğinin konsantrasyon kapasitesinin düşük olması nedeniyle yüksek solüt yükü içeren besinler dehidratasyona yol açar.",
                "konsantrasyon kapasitesinin",
                "İdrarı yoğunlaştırıp suyu geri emme yeteneği kısıtı"
            ),
            make_before_after(
                "Anne Sütü ile İnek Sütünün Böbrek Solüt Yükü Kıyası",
                "Anne Sütü Renal Yükü (İdeal)",
                "Düşük protein ve dengeli elektrolit ile ~286 mOsm/kg yük oluşturur; böbreği hiç yormaz, su kaybı yapmaz.",
                "İnek Sütü Renal Yükü (Ağır)",
                "Yüksek protein (üre) ve minerallerle ~400 mOsm/kg yük bindirir; zorunlu idrar çıkışı ve hipernatremi yapar.",
                "Düşük ozmolariteli güvenli beslenme ile yüksek solüt yüklü dehidratasyon riski ayrımı"
            ),
            make_active_recall(
                "Bebeklere ilk 1 yaşta inek sütü verilmemesinin en kritik nefrolojik gerekçesi nedir?",
                "İnek sütünün yüksek protein ve elektrolit içeriğinin immatür böbreğe aşırı renal solüt yükü bindirmesi ve düşük konsantrasyon kapasitesi nedeniyle dehidratasyon/hipernatremi riski yaratmasıdır.",
                "Renal solüt yükü ve hipernatremik dehidratasyon riski"
            )
        ]
    })

    # Slayt 19: [TEKRAR SAYFASI - CHECKPOINT 2] Bebeklikte Büyüme ve Organ İmmadüritesi
    slides.append({
        "id": "k1-22-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Bebeklikte Büyüme ve Organ İmmadüritesi",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 19,
        "narrative": (
            "Bu ikinci checkpoint sayfasında, bebeklik dönemindeki büyüme dönüm noktalarını ve "
            "organ immadüritesi mekanizmalarını kilitliyoruz: "
            "1. **Tartı Dinamikleri:** İlk günlerde %5-10 fizyolojik kayıp; 10-14. günde doğum ağırlığına dönüş; 4-6. ayda 2 kat, 1 yaşında 3 kat. "
            "2. **Boy Artışı:** İlk 1 yılda %50 artış (50 cm'den 75 cm'ye); 4 yaşında doğum boyunun 2 katına ulaşma (100 cm). "
            "3. **Vücut Suyu:** Doğumda %70 iken 1 yaşında %60'a geriler; ekstrasellüler sıvı fazlalığı dehidratasyon riskini artırır. "
            "4. **Mide Hacmi:** Doğumda 10-20 ml'den 1 yaş sonunda 250 ml'ye ulaşır; küçük hacimli sık beslenme şarttır. "
            "5. **Organ İmmadüritesi:** Pankreatik amilaz ilk 6 ay düşüktür (nişasta verilmez); böbrek konsantrasyon kapasitesi düşüktür (yüksek solüt yükünden kaçınılır)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "k1-22-fc-04",
                "Yenidoğan bir bebeğin doğum sonrası ilk günlerdeki fizyolojik tartı kaybını telafi ederek doğum ağırlığına geri dönmesi en geç kaçıncı günlerde beklenir?",
                "10 - 14. günlerde",
                "İkinci haftanın bitimine denk gelen kilo toparlanma süresi",
                "Fizyolojik Büyüme"
            ),
            make_flashcard(
                "k1-22-fc-05",
                "Sağlıklı bir süt çocuğunun doğum ağırlığının yaklaşık 2 katına ve 3 katına ulaştığı tipik aylar/yaşlar hangileridir?",
                "4-6. ayda 2 katına, 1 yaşında 3 katına çıkar",
                "Süt çocukluğu kilo çarpanı dönüm noktaları",
                "Fizyolojik Büyüme"
            ),
            make_flashcard(
                "k1-22-fc-06",
                "Yenidoğan bebeğin mide hacmi doğumda kaç mililitredir ve 1 yaşın sonunda yaklaşık kaç mililitreye ulaşır?",
                "Doğumda 10-20 ml, 1 yaşında yaklaşık 250 ml",
                "İlk günlerde fındık büyüklüğünden su bardağı doluluğuna ulaşan anatomik skala",
                "Gastrointestinal Anatomi"
            )
        ]
    })

    # Slayt 20: Bölüm Özeti: Fizyolojik Olgunlaşmadan Besin Gereksinimlerine Geçiş
    slides.append({
        "id": "k1-22-s20",
        "title": "Bölüm Özeti: Fizyolojik Olgunlaşmadan Besin Gereksinimlerine Geçiş",
        "section": "Bebeklik Döneminde Büyüme Dinamikleri ve Fizyolojik Gelişim",
        "slideNumber": 20,
        "narrative": (
            "Bebeklik döneminde organ sistemlerinin immadüritesi ve hızlı büyüme dinamikleri, besin gereksinimlerinin "
            "erişkinden neden bu kadar farklı olduğunu ortaya koymaktadır. "
            "Bebek ne bir minyatür yetişkindir ne de rasgele mamalarla beslenebilecek olgun bir sindirim kanalına sahiptir. "
            "Her kilogram başına ihtiyaç duyulan kalori, esansiyel aminoasitler, linoleik asit, su ve mineraller "
            "miligram düzeyinde hassas bir denge gerektirir. "
            "Üçüncü bölümümüzde, bebeğin enerji ihtiyacının persentil eğrileriyle takibi, protein fazlalığının zararları, "
            "beyin gelişimi için linoleik asit zorunluluğu, kalsiyum-fosfor dengesi ve 4. aydan sonra tükenen demir depoları "
            "tüm biyokimyasal ayrıntılarıyla incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bebeklerin enerji ve besin ögesi gereksinimlerinin yeterliliğini gösteren en güvenilir klinik parametre büyüme eğrilerinde persentil izlemidir.",
                "büyüme eğrilerinde",
                "Standart persentil grafiklerinde tartı ve boy takibi yöntemi"
            ),
            make_causal_chain(
                "Büyüme Hızından Besin Gereksinimine Mantıksal Geçiş",
                [
                    "1. Kütle Katlanması: 1 yılda kilonun 3 katına çıkması yüksek anabolik sentez gerektirir.",
                    "2. Yüksek İhtiyaç: Kg başına kalori ve protein ihtiyacı yetişkinin iki katıdır.",
                    "3. Denge Zorunluluğu: Fazla protein asidoz ve üremi yapar; eksik protein kvaşiorkor doğurur.",
                    "4. Hassas Ayar: Enerji, esansiyel yağlar ve demir gereksinimi gelişim basamaklarına göre karşılanır."
                ]
            ),
            make_active_recall(
                "Bebeklikte bir bebeğin günlük kalori ve besin alımının yeterli olup olmadığını anlamanın sahada en pratik ve güvenilir yolu nedir?",
                "Düzenli aralıklarla tartı ve boy ölçümü yapılarak büyüme eğrilerinde (persentil çizelgelerinde) kendi eğrisini izleyip izlemediğinin takip edilmesidir.",
                "Persentil büyüme eğrisi takibi kuralı"
            )
        ]
    })

    return slides
