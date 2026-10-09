# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 6: Tütün ve Alkol Toksikolojisi (Slayt 51-60)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_6_slides():
    slides = []

    # Slayt 51: Tütün Kullanımının Küresel Epidemiyolojisi
    slides.append({
        "id": "k1-26-s51",
        "title": "Tütün Kullanımının Küresel Epidemiyolojisi",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 51,
        "narrative": (
            "Tütün kullanımı, insanlık tarihinde önlenebilir morbidite, maluliyet ve erken ölümün **tartışmasız bir numaralı nedenidir**: "
            "1. **Küresel Rakamlar:** Dünyada yaklaşık **1.3 milyar aktif tütün kullanıcısı** bulunmaktadır. "
            "Her yıl 8 milyondan fazla insan tütüne bağlı nedenlerle hayatını kaybetmektedir (bunun 1.2 milyondan fazlası pasif içicidir!). "
            "2. **Önlenebilir Kanser Nedeni:** Tüm insan kanserlerine bağlı ölümlerin yaklaşık **üçte birinden (%30-35)** "
            "ve akciğer kanseri ölümlerinin **%80-90'ından doğrudan tütün sorumludur**. "
            "3. **Kazanılan Ömür:** Sigarayı bırakan bireylerde kardiyovasküler risk ilk 1-2 yılda dramatik düşerken, "
            "akciğer kanseri riski 15-20 yıl içinde hiç içmeyenlerin düzeyine yaklaşır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tütün Kullanımının Küresel Patolojik Bilançosu",
                ["Epidemiyolojik Parametre", "Küresel İstatistik", "Tıbbi Önemi"],
                [
                    ["Aktif Tütün Kullanıcısı Sayısı", "~1.3 Milyar İnsan", "Küresel bağımlılık epidemisi"],
                    ["Yıllık Doğrudan / Dolaylı Ölüm", ">8 Milyon İnsan / Yıl", "Önlenebilir ölümlerin bir numaralı etkeni"],
                    [
                        "Akciğer Kanseri Nedensel Payı",
                        {"text": "Tüm akciğer kanserlerinin %80 - 90'ı", "isMasked": True, "hint": "Bronkojenik akciğer tümörlerinde tütüne atfedilen ezici nedensellik yüzdesi"},
                        "En sık görülen ölümcül malignitenin ana kaynağı"
                    ],
                    ["Kardiyovasküler Katkı", "Miyokard enfarktüsü riskinde 2-4 kat artış", "Aterosklerozun majör bağımsız risk faktörü"]
                ]
            ),
            make_active_recall(
                "Tüm dünyada önlenebilir erken ölümlerin ve tüm kanser ölümlerinin yaklaşık üçte birinin doğrudan sorumlusu olan en yaygın kişisel çevresel maruziyet ajanı nedir?",
                "Tütün ve sigara kullanımıdır.",
                "Yaklaşık dört bin kimyasal barındıran duman soluma alışkanlığı"
            )
        ]
    })

    # Slayt 52: Tütün Dumanının Toksik Kimyası
    slides.append({
        "id": "k1-26-s52",
        "title": "Tütün Dumanının Toksik Kimyası",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 52,
        "narrative": (
            "Sigara dumanı, tütün yaprağının 600-900°C'de eksik yanmasıyla oluşan 4000'den fazla kimyasal bileşiğin ölümcül kokteylidir: "
            "1. **Nikotin (Bağımlılık Ajanı):** "
            "- Dumanla saniyeler içinde kan-beyin bariyerini geçer. "
            "- Santral sinir sistemindeki **nikotinik asetilkolin reseptörlerine** bağlanarak dopamin salınımını patlatır; "
            "eroin ve kokain kadar güçlü fiziksel ve psikolojik bağımlılık yapar. "
            "- Adrenal medulladan katekolamin salgılatarak taşikardi ve hipertansiyon oluşturur. Doğrudan karsinojen değildir. "
            "2. **Majör Karsinojenler (Kanser Yapıcılar - >60 adet kanıtlanmış karsinojen):** "
            "- **Polisiklik Aromatik Hidrokarbonlar (PAH):** Kömür ve katran artığıdır (Örn: Benzo[a]piren). Sitokrom P450 ile epoksitlere "
            "dönüşür; **TP53 geninde mutasyonel sıcak noktalara (hotspot)** kovalent bağlanarak DNA kırıkları yapar. "
            "- **Tütüne Özgü Nitrozaminler (NNK):** K-RAS onkogeninde mutasyon yapar. "
            "- **Aromatik Aminler (2-Naftilamin):** Karaciğerde glukuronide bağlanıp mesaneye atılır; idrarda hidrolize olarak **mesane kanseri** yapar. "
            "3. **Karbonmonoksit ($CO$):** Hemoglobine bağlanarak doku oksijen sunumunu kronik olarak bozar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tütün Dumanındaki Başlıca Toksinler ve Hedefleri",
                ["Kimyasal Madde", "Toksik / Biyolojik Etki Mekanizması", "Spesifik Patolojik Sonuç"],
                [
                    ["Nikotin", "SSS nikotinik reseptörler, dopamin deşarjı", "Ağır nörokimyasal bağımlılık, taşikardi"],
                    [
                        "Polisiklik Aromatik Hidrokarbonlar (PAH)",
                        "DNA aduktları oluşturma (TP53 mutasyonu)",
                        {"text": "Akciğer skuamöz ve küçük hücreli karsinomu", "isMasked": True, "hint": "Benzo-a-piren türevi hidrokarbonların bronş epitelinde yaptığı primer maligniteler"}
                    ],
                    ["Nitrozaminler (NNK)", "K-RAS onkogen aktivasyonu", "Akciğer adenokarsinomu patogenezi"],
                    ["Aromatik Aminler (2-Naftilamin)", "İdrarla atılım sırasında ürotelyuma temas", "Mesane ürotelyal karsinomu"],
                    ["Karbonmonoksit (CO)", "Oksihemoglobin eğrisini sola kaydırma", "Kronik doku hipoksisi ve endotel hasarı"]
                ]
            ),
            make_active_recall(
                "Sigara içen bireylerde mesaneden atılırken ürotelyal epitele temas ederek mesane kanseri (ürotelyal karsinom) riskini katbekat artıran tütün dumanı karsinojeni kimyasal sınıfı nedir?",
                "Aromatik aminlerdir (özellikle 2-naftilamin).",
                "Karaciğerde işlenip böbrek yoluyla mesane lümenine atılan boyar madde benzeri kanserojenler"
            )
        ]
    })

    # Slayt 53: Sigaranın Solunum Sistemine Etkileri ve KOAH
    slides.append({
        "id": "k1-26-s53",
        "title": "Sigaranın Solunum Sistemine Etkileri ve KOAH",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 53,
        "narrative": (
            "Tütün dumanı solunum yolunda trakeadan alveollere kadar tüm epitel mimarisini tahrip eder: "
            "1. **Silier Felç ve Mukus Aşırı Salgısı:** "
            "- Duman silyaların hareketini dondurur (silier disfonksiyon). "
            "- Submukozal bezleri hipertrofiye uğratır ve goblet hücre metaplazisi yapar; aşırı mukus birikir (**Kronik Bronşit**). "
            "2. **Elastaz-Antielastaz Dengesizliği (Amfizem Patogenezi):** "
            "- Tütün partikülleri alveol makrofajlarını ve nötrofilleri uyarır; bu hücrelerden nötrofil elastazı salgılanır. "
            "- Eşzamanlı olarak dumandaki serbest radikaller, akciğerin koruyucu kalkanı olan **alfa-1 antitripsini (AAT) oksitleyerek inaktive eder**. "
            "- Frenlenemeyen elastaz enzimi, alveol duvarlarındaki elastik lifleri parçalar (**elastolizis**). "
            "3. **Sentriasiner Amfizem:** Alveol duvarları yırtılır; terminal bronşiyoller çevresinde kistik genişlemeler oluşur; "
            "gaz değişim yüzeyi çöker, ekspiratuar hava hapsi ve ağır dispne gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Sigaraya Bağlı Sentriasiner Amfizem Gelişim Basamakları",
                [
                    "1. Lökosit Göçü: Tütün dumanının alveollere nötrofil ve makrofajları çekmesi",
                    "2. Elastaz Salınımı: Nötrofillerden masif nötrofil elastazı enziminin boşaltılması",
                    "3. Koruyucu Frenin Kırılması: Oksidan dumanın alfa-1 antitripsin (AAT) inhibitörünü yakıp inaktive etmesi",
                    "4. Alveoler Elastoliz: Kontrolsüz elastazın alveol septalarındaki elastik lifleri eritmesi",
                    "5. Alveol Yıkımı: Alveollerin birleşip dev amfizematöz boşluklara dönüşmesi ve hava hapsi"
                ]
            ),
            make_before_after(
                "Sigara Amfizemi vs Alfa-1 Antitripsin Genetik Eksikliği",
                "Sigara Kaynaklı Amfizem (Sentriasiner)",
                "Dumana ilk maruz kalan üst lobların apikal segmentlerinde ve asinusun merkezinde (sentriasiner) lokalize yıkım",
                "AAT Genetik Eksikliği (Panasiner)",
                "Kan dolaşımı zengin olan alt lobların bazal segmentlerinde tüm asinusu homojen tutan (panasiner) yıkım"
            )
        ]
    })

    # Slayt 54: Tütün Kaynaklı Maligniteler
    slides.append({
        "id": "k1-26-s54",
        "title": "Tütün Kaynaklı Maligniteler",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 54,
        "narrative": (
            "Sigara yalnızca akciğeri değil, dumanın temas ettiği ve karsinojenlerin kanla ulaştığı tüm organları kansere boğar: "
            "1. **Akciğer Kanserleri:** "
            "- **Skuamöz Hücreli Karsinom ve Küçük Hücreli Akciğer Karsinomu (SCLC):** Sigara ile ilişkisi en güçlü olan iki tiptir "
            "(neredeyse tamamı ağır sigara içicilerinde görülür). Sentral yerleşimlidir. "
            "- **Adenokarsinom:** Günümüzde en sık görülen tip haline gelmiştir; sigara içenlerde de içmeyenlerde de görülebilir (periferik yerleşimli). "
            "2. **Üst Solunum ve Sindirim Yolu Kanserleri:** "
            "- Ağız boşluğu, dil, farenks ve **larenks kanserleri** (sigara + alkol kombinasyonunda risk 100 katına fırlar!). "
            "- Özofagus skuamöz hücreli karsinomu. "
            "3. **Uzak Organ Maligniteleri:** "
            "- **Mesane Kanseri:** 2-naftilamin birikimiyle sigara içenlerde mesane kanseri riski 3-5 kat fazladır. "
            "- **Pankreas Adenokarsinomu:** Sigara pankreas kanseri için en önemli önlenebilir risk faktörüdür. "
            "- Mide, böbrek (renal hücreli karsinom), serviks ve Akut Miyeloblastik Lösemi (AML - dumandaki benzen nedeniyle)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tütünün Tetiklediği Kanser Türleri ve Göreceli Risk",
                ["Malignite Türü", "Sigara İle İlişki Derecesi", "Primer Karsinojenik Mekanizma"],
                [
                    ["Küçük Hücreli ve Skuamöz Akciğer Kanseri", "Aşırı Yüksek (>%95 sigara ilişkili)", "PAH ile TP53 ve RB mutasyonları"],
                    ["Larenks Karsinomu", "Çok Yüksek (%85-90)", "Larenks mukozasında skuamöz metaplazi ve displazi"],
                    [
                        "Mesane Ürotelyal Karsinomu",
                        "Yüksek (Vakaların %50'si)",
                        {"text": "Aromatik aminlerin idrarla temas ederek ürotelyumu mutasyona uğratması", "isMasked": True, "hint": "Tütün metabolitlerinin mesane depolama fazında duvara yaptığı kimyasal hasar"}
                    ],
                    ["Pankreas Adenokarsinomu", "Orta-Yüksek (2-3 kat risk artışı)", "Dolaşımdaki nitrozaminlerin asiner hücre hasarı"],
                    ["Akut Miyeloid Lösemi (AML)", "Orta (Benzen maruziyeti)", "Kemik iliği kök hücre DNA hasarı"]
                ]
            ),
            make_micro_quiz(
                "Histopatolojik olarak sigara kullanımı ile nedensel ilişkisi EN GÜÇLÜ olan ve neredeyse tamamı (>%95) ağır sigara içiciliği öyküsü bulunan hastalarda santral bronşlardan köken alan akciğer karsinomu alt tipi hangisidir?",
                {
                    "A": "Küçük hücreli akciğer karsinomu (SCLC)",
                    "B": "Akciğer karsinoid tümörü",
                    "C": "Bronkoalveoler karsinom (lepidik adenokarsinom)",
                    "D": "Mezotelyoma",
                    "E": "Hamartom"
                },
                "A",
                {
                    "A": "Doğrudur; küçük hücreli karsinom ve skuamöz karsinom sigara ile en ayrılmaz bağa sahip nöroendokrin agresif tümörlerdir.",
                    "B": "Yanlış; karsinoid tümörler sigarayla ilişkisiz nöroendokrin neoplazilerdir.",
                    "C": "Yanlış; sigara içmeyenlerde sık görülen adenokarsinom formudur.",
                    "D": "Yanlış; mezotelyoma asbest maruziyetiyle gelişir.",
                    "E": "Yanlış; hamartom benign lezyondur."
                }
            )
        ]
    })

    # Slayt 55: Sigaranın Kardiyovasküler Felaketleri
    slides.append({
        "id": "k1-26-s55",
        "title": "Sigaranın Kardiyovasküler Felaketleri",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 55,
        "narrative": (
            "Sigara içen bir bireyin kalp krizinden ölme olasılığı, akciğer kanserinden ölme olasılığından çok daha yüksektir: "
            "1. **Endotel Yıkımı ve Aterogenez:** "
            "- Tütün dumanındaki serbest radikaller koroner ve sistemik arter endotelini doğrudan tahrip eder. "
            "- Damar koruyucu nitrik oksit ($NO$) ve prostasiklin ($PGI_2$) sentezini baskılar; vazokonstriksiyonu tetikler. "
            "- LDL kolesterolün okside olmasını hızlandırır; makrofajlar okside LDL'yi yutarak **köpük hücrelerine** ve aterosklerotik plaklara dönüşür. "
            "2. **Trombosit Agregasyonu ve Tromboz:** "
            "- Dumandaki kimyasallar trombosit agregasyonunu uyarır; tromboksan A2 ($TXA_2$) salınımını artırır. "
            "- Pıhtılaşma faktörlerini (fibrinojen vb.) yükselterek pro-trombotik bir hiperkoagülabilite tablosu yaratır. "
            "3. **Miyokard Oksijen Açlığı:** "
            "- Karbonmonoksit hemoglobini bağlayarak karboksihemoglobin yapar; kalbe taşınan $O_2$ miktarını azaltır. "
            "- Nikotin ise kalp hızını ve kan basıncını artırarak miyokardın $O_2$ talebini yükseltir. "
            "- Azalan sunum + Artan talep = Şiddetli iskemi, kararsız angina, akut koroner oklüzyon ve **ani kardiyak ölüm**."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sigaranın Kalp ve Damar Sistemindeki Triadı",
                ["Hedef Patoloji", "Biyokimyasal / Hücresel Tetikleyici", "Klinik Yansıması"],
                [
                    ["Hızlanmış Ateroskleroz", "Endotel disfonksiyonu ve LDL oksidasyonu", "Koroner arter hastalığı, periferik damar tıkanıklığı"],
                    ["Akut Trombofili", "Trombosit hiperaktivitesi ve fibrinojen artışı", "Plak rüptürü üzerine oturan letal koroner trombüs"],
                    [
                        "Doku Oksijen Kriz",
                        {"text": "Karboksihemoglobinemi (CO) ve nikotin taşikardisi", "isMasked": True, "hint": "Oksijen taşıma kapasitesinin düşmesi ile kalp iş yükünün eşzamanlı fırlaması"},
                        "Akut miyokard iskemisi ve letal ventriküler aritmi"
                    ]
                ]
            ),
            make_active_recall(
                "Sigara içiminde tütün dumanındaki karbonmonoksitin oksijen sunumunu azaltırken nikotinin kalp hızını artırarak miyokardın oksijen talebini yükseltmesi durumunun kardiyolojideki adı nedir?",
                "Miyokardiyal oksijen arz-talep uyumsuzluğudur (iskemi tetiklenmesi).",
                "Oksijen taşıyan molekülün bloke olmasıyla kalbin iş yükünün eşzamanlı artması"
            )
        ]
    })

    # Slayt 56: Pasif İçicilik ve Fetal Maruziyet
    slides.append({
        "id": "k1-26-s56",
        "title": "Pasif İçicilik ve Fetal Maruziyet",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 56,
        "narrative": (
            "Sigara içmeyen bireylerin tütün dumanına maruz kalması da ağır morbidite ve mortalite ile sonuçlanır: "
            "1. **Pasif İçicilik (İkinci El Duman):** "
            "- Sigaranın ucundan çıkan yan akım dumanı (sidestream smoke), içicinin çektiği ana duman kadar toksiktir. "
            "- Evde veya işyerinde pasif dumana maruz kalan sağlıklı bireylerde **akciğer kanseri ve koroner kalp hastalığı riski %20-30 oranında artar**. "
            "2. **Çocuklarda Pasif Maruziyet:** "
            "- Evde sigara içilen ailelerin çocuklarında rekürren otitis media (orta kulak iltihabı), astım alevlenmeleri ve "
            "ciddi alt solunum yolu enfeksiyonları (bronşiolit, pnömoni) belirgin olarak fazladır. "
            "3. **Fetal Tütün Maruziyeti (Gebelikte Sigara):** "
            "- Nikotin ve karbonmonoksit plasentayı kolayca geçer. "
            "- Nikotin plasental damarlarda vazokonstriksiyon yapar; CO ise fetal kanda karboksihemoglobin yaparak fetal hipoksi oluşturur. "
            "- **Sonuçlar:** **İntrauterin Gelişme Geriliği (İUGR)**, düşük doğum ağırlığı, erken doğum, plasenta dekolmanı ve "
            "**Ani Bebek Ölümü Sendromu (SIDS)** riskinde iki kat artış!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Aktif vs Pasif ve Fetal Tütün Maruziyeti",
                "Erişkinde Pasif İçicilik",
                "Dumana maruz kalan sigara içmeyen bireyde koroner kalp hastalığı ve akciğer kanseri riskinde %20-30 net artış",
                "Fetal Dönemde Anne Sigarası",
                "Uteroplasental vazokonstriksiyon ve hipoksi sonucu düşük doğum ağırlığı, İUGR ve Ani Bebek Ölümü (SIDS)"
            ),
            make_cloze(
                "Gebelikte anne adayının sigara içmesi plasental vazokonstriksiyon ve fetal hipoksiye yol açarak intrauterin gelişme geriliği ve düşük doğum ağırlığına neden olur.",
                "intrauterin gelişme geriliği",
                "Bebeğin anne karnında haftasına göre yetersiz kilo ve boy gelişimi göstermesi durumu"
            )
        ]
    })

    # Slayt 57: Alkolün Emilimi ve Hepatik Metabolizması
    slides.append({
        "id": "k1-26-s57",
        "title": "Alkolün Emilimi ve Hepatik Metabolizması",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 57,
        "narrative": (
            "Etanol (alkol), mideden (%20) ve ince bağırsaktan (%80) hızla emilerek kan yoluyla doğrudan karaciğere ulaşır. "
            "Alınan alkolün %90-95'i karaciğerde metabolize edilir: "
            "1. **Birinci Basamak (Etanol -> Asetaldehit): Üç Temel Enzim Yolağı:** "
            "- **Alkol Dehidrojenaz (ADH - Sitoplazmik Ana Yol):** Düşük ve orta dozlarda alkolün %80'ini yıkan ana yoldur. "
            "Etanolü **toksik bir metabolit olan asetaldehite** çevirirken, koenzim **NAD+'yi tüketerek NADH'ye indirger**. "
            "- **Mikrozomal Etanol Oksidasyon Sistemi (MEOS / CYP2E1):** Endoplazmik retikulumda yer alır. Yüksek doz alkolde "
            "devreye girer. Alkoliklerde CYP2E1 enzimi indüklenir; diğer ilaçlarla (parasetamol) ölümcül etkileşimlere ve serbest radikallere yol açar. "
            "- **Katalaz (Peroksizomal):** %5'ten az minör paya sahiptir. "
            "2. **İkinci Basamak (Asetaldehit -> Asetat):** "
            "- Mitokondriyal **Asetaldehit Dehidrojenaz (ALDH)** asetaldehiti zararsız asetata çevirir (yine NAD+ -> NADH). "
            "- Asyalı toplumların %50'sinde ALDH2 geninde inaktive edici nokta mutasyonu vardır; asetaldehit birikir ve "
            "azıcık alkolle bile yüzde kızarma (flushing), taşikardi, bulantı ve baş dönmesi gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Hepatik Alkol Metabolizması ve Toksik Ara Ürün Zinciri",
                [
                    "1. Gastrik/İntestinal Emilim: Etanolün lümenden portal vene difüzyonu ve hepatositlere girişi",
                    "2. ADH Sitoplazmik Oksidasyonu: Alkol dehidrojenazın etanolü toksik asetaldehite dönüştürmesi",
                    "3. Koenzim Kayması: Enzimin ortamdaki serbest NAD+'yi hızla tüketip bol miktarda NADH üretmesi",
                    "4. Mitokondriyal ALDH: Asetaldehitin ALDH2 enzimi ile asetat molekülüne çevrilmesi",
                    "5. Sistemik Kullanım: Asetatın asetil-CoA'ya dönüştürülerek periferik dokularda yakılması"
                ]
            ),
            make_active_recall(
                "Karaciğerde alkolün alkol dehidrojenaz enzimiyle ilk oksidasyonu sonucu ortaya çıkan, hücre hasarından, akşamdan kalmalık semptomlarından ve karsinojenezden sorumlu toksik ara metabolit nedir?",
                "Asetaldehittir.",
                "Etanolün ilk oksidasyon ürünü olan reaktif aldehit bileşiği"
            )
        ]
    })

    # Slayt 58: Alkol Toksisitesinde Biyokimyasal Hasar ve Steatoz
    slides.append({
        "id": "k1-26-s58",
        "title": "Alkol Toksisitesinde Biyokimyasal Hasar ve Steatoz",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 58,
        "narrative": (
            "Alkol metabolizmasının merkezindeki en ölümcül biyokimyasal bozukluk, **hücre içi $NADH / NAD^+$ oranının aşırı yükselmesidir**: "
            "1. **NAD+ Tükenmesi:** "
            "- Hem sitoplazmik ADH hem de mitokondriyal ALDH, $NAD^+$ kofaktörünü kullanarak $NADH$'ye çevirir. "
            "- Karaciğerde serbest $NAD^+$ tükenir; bu durum $NAD^+$ bağımlı tüm metabolik yolları kilitler. "
            "2. **Karaciğer Yağlanması (Hepatik Steatoz) Mekanizması:** "
            "- Mitokondriyal **yağ asidi beta-oksidasyonu** çalışmak için $NAD^+$'ye muhtaçtır; $NAD^+$ olmayınca yağ asitleri yakılamaz! "
            "- Aşırı $NADH$ varlığı gliserol-3-fosfat sentezini ve **trigliserid üretimini (lipogenez)** patlatır. "
            "- Karaciğerden VLDL salınımı da bozulunca, trigliseridler hepatosit sitoplazmasında birikerek **makroveziküler yağlanma (steatoz)** yapar. "
            "Tek bir ağır alkol tüketim seansından sonra bile karaciğer yağlanması başlar (tamamen reversibldir). "
            "3. **Laktik Asidoz ve Hipoglisemi:** Piruvat laktata dönüşür (laktik asidoz); glukoneogenez durur ve açlıkta **ölümcül hipoglisemi** tetiklenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "NADH/NAD+ Oranı Artışının Metabolik Sonuçları",
                ["Etkilenen Biyokimyasal Yolak", "Moleküler Bozukluk", "Klinik / Patolojik Karşılığı"],
                [
                    ["Yağ Asidi Beta-Oksidasyonu", "NAD+ yokluğu nedeniyle mitokondriyal yağ yakımının durması", "Hepatik Steatoz (Karaciğer yağlanması)"],
                    [
                        "Hepatik Glukoneogenez",
                        {"text": "Piruvatın glukoza gidemeyip aşırı laktata çevrilmesi", "isMasked": True, "hint": "Aç alkoliklerde glukoz üretiminin durmasıyla komaya sokan metabolik tablo"},
                        "Ağır açlık hipoglisemisi ve laktik asidoz"
                    ],
                    ["Ürat Klirensi", "Laktatın böbrekte ürik asitle yarışarak atılımı tıkaması", "Hiperürisemi ve gut artriti alevlenmesi"]
                ]
            ),
            make_active_recall(
                "Kronik alkol tüketiminde hepatositlerde alkol dehidrojenaz aktivitesi sonucu hangi koenzimin tükenmesi yağ asitlerinin mitokondriyal beta-oksidasyonunu bloke ederek karaciğer yağlanmasına yol açar?",
                "NAD+ koenzimidir (nikotinamid adenin dinükleotid).",
                "Okside piridin nükleotid elektron alıcısı"
            )
        ]
    })

    # Slayt 59: Checkpoint 6
    slides.append({
        "id": "k1-26-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Tütün ve Alkol Patolojisi",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 59,
        "narrative": (
            "Altıncı kontrol noktamızda iki büyük kişisel çevre toksininin patolojisini özetliyoruz: "
            "1. **Tütün Toksinleri:** Nikotin bağımlılık yapar; polisiklik aromatik hidrokarbonlar (PAH) TP53 mutasyonuyla akciğer kanseri; "
            "aromatik aminler mesane kanseri yapar; CO doku hipoksisi oluşturur. "
            "2. **KOAH Patogenezi:** Dumandaki oksidanlar alfa-1 antitripsini inaktive eder; nötrofil elastazı alveol elastik liflerini "
            "sindirerek sentriasiner amfizem yapar. "
            "3. **Kardiyovasküler Felaket:** Endotel disfonksiyonu, LDL oksidasyonu, trombosit hiperaktivitesi ve karboksihemoglobin ile fatal MI. "
            "4. **Fetal Tütün:** Plasental vazokonstriksiyonla İUGR, düşük doğum ağırlığı ve SIDS. "
            "5. **Alkol Metabolizması:** ADH etanolü asetaldehite çevirir; NAD+ tükenir, NADH fırlar. "
            "6. **Hepatik Hasar:** Yağ asidi beta-oksidasyonu durur; karaciğer yağlanması (steatoz) başlar; laktik asidoz ve hipoglisemi gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s59-1",
                "Tütün dumanında bağımlılık yapıcı ana kimyasal ajan ile akciğer kanserine yol açan güçlü polisiklik aromatik kanserojenler hangileridir?",
                "Nikotin ve polisiklik aromatik hidrokarbonlardır (PAH).",
                "Biri dopaminerjik ödül yolağını tutan alkaloid, diğeri katrandaki mutajenik yanma ürünü",
                "Tütün Toksisitesi"
            ),
            make_flashcard(
                "k1-26-fc-s59-2",
                "Karaciğerde alkol metabolizması sırasında alkol dehidrojenaz enziminin hızla tükettiği ve eksikliğinde hepatik steatoza yol açan koenzim nedir?",
                "NAD+ koenzimidir (nikotinamid adenin dinükleotid).",
                "Hücresel elektron alıcısı piridin nükleotid kofaktörü",
                "Alkol Metabolizması"
            ),
            make_flashcard(
                "k1-26-fc-s59-3",
                "Kronik alkolizmde tiamin (B1 vitamini) eksikliği zemininde gelişen, oftalmopleji, ataksi ve konfüzyon ile seyreden nörolojik sendrom nedir?",
                "Wernicke-Korsakoff sendromudur.",
                "Korpus mammillare kanamaları ve hafıza kaybıyla karakterize nörodejeneratif tablo",
                "Wernicke-Korsakoff"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tütün ve Alkol Toksisitesi Karşılaştırma Matrisi",
                ["Ajan", "Ana Toksik / Karsinojenik Bileşen", "Biyokimyasal Hasar Mekanizması", "En Ağır Organ Hasarı"],
                [
                    ["Tütün Dumanı", "PAH, nitrozaminler, nikotin, CO", "DNA aduktları, AAT oksidasyonu, endotel lizisi", "Küçük hücreli akciğer kanseri, sentriasiner amfizem, MI"],
                    [
                        "Alkol (Etanol)",
                        "Asetaldehit ve aşırı NADH birikimi",
                        {"text": "Yağ asidi beta-oksidasyon blokajı ve protein aduktları", "isMasked": True, "hint": "Koenzim dengesinin bozulması ile hepatositlerde trigliserid birikimi"},
                        "Mikronodüler karaciğer sirozu, pankreatit, Wernicke"
                    ]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi kronik alkol tüketiminde karaciğer parankiminde erken evrede ortaya çıkan makroveziküler yağlanmanın (steatoz) doğrudan biyokimyasal tetikleyicisidir?",
                {
                    "A": "Alkol dehidrojenaz aktivitesiyle hücresel NAD+'nin tükenmesi ve yağ asidi beta-oksidasyonunun durması",
                    "B": "Midede pepsin salgısının tamamen durması",
                    "C": "Safra kesesinde aşırı safra asidi birikimi",
                    "D": "Pankreasın insülin üretimini durdurması",
                    "E": "Dolaşımdaki eritrositlerin aşırı parçalanması"
                },
                "A",
                {
                    "A": "Doğrudur; NAD+ yetersizliği mitokondriyal yağ asidi yıkımını kilitler ve trigliserid birikimine yol açar.",
                    "B": "Yanlış; pepsin mide enzimidir, steatoz yapmaz.",
                    "C": "Yanlış; safra birikimi kolestazdır.",
                    "D": "Yanlış; diyabette ketoasidoz olur.",
                    "E": "Yanlış; hemoliz sarılık yapar."
                }
            )
        ]
    })

    # Slayt 60: Kronik Alkolizmin Sistemik Organ Hasarları
    slides.append({
        "id": "k1-26-s60",
        "title": "Kronik Alkolizmin Sistemik Organ Hasarları",
        "section": "Tütün ve Alkol Toksikolojisi",
        "slideNumber": 60,
        "narrative": (
            "Kronik alkol bağımlılığı karaciğerin ötesinde vücuttaki hemen her dokuda geri dönüşümsüz yıkıma yol açar: "
            "1. **Karaciğer Hastalığı Spektrumu:** "
            "- **Steatoz (Yağlanma - %90-100):** Reversibl ilk basamak. "
            "- **Alkolik Steatohepatit (%10-35):** Hepatosit balonlaşması, nekroz, Mallory-Denk cisimcikleri (sitokeratin yumakları) ve nötrofilik infiltrasyon. "
            "- **Alkolik Siroz (%8-20):** İto (stellat) hücre aktivasyonuyla kollajen depolanması; mikronodüler siroz, portal hipertansiyon ve hepatoselüler karsinom (HCC) riski. "
            "2. **Pankreas:** Protein tıkaçları ve duktal hasarla **kronik kalsifiye pankreatit** ve akut nekrotizan ataklar. "
            "3. **Kardiyovasküler:** Alkolün miyositlere doğrudan toksik etkisiyle ventriküllerde dört boşluk dilatasyonu: **Dilate Kardiyomiyopati** ve aritmiler. "
            "4. **Sinir Sistemi:** Tiamin (B1) emilim bozukluğuna bağlı **Wernicke-Korsakoff sendromu** (korpus mammillare atrofisi, oftalmopleji, konfabülasyon) ve serebellar vermis atrofisi. "
            "5. **Fetal Alkol Sendromu (FAS):** Gebelikte alkol tüketimi; mikrosefali, düz filtrum, ince üst dudak, büyüme geriliği ve mental retardasyon."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kronik Alkolizmin Sistemik Hedef Organları",
                ["Organ Sistemi", "Patolojik Tablo", "Histopatolojik / Klinik Belirteç"],
                [
                    ["Karaciğer", "Steatohepatit ve Mikronodüler Siroz", "Mallory-Denk cisimcikleri, nötrofiller, stellat hücre fibrozu"],
                    ["Pankreas", "Kronik kalsifiye pankreatit", "Duktal protein tıkaçları, parankim kalsifikasyonu ve atrofi"],
                    [
                        "Kardiyovasküler",
                        "Alkolik Dilate Kardiyomiyopati",
                        {"text": "Tüm kalp odacıklarında dilatasyon ve pompa yetmezliği", "isMasked": True, "hint": "Miyositlerin doğrudan toksik hasarıyla kalbin genişleyip kasılamaması tablosu"}
                    ],
                    ["Santral Sinir Sistemi", "Wernicke-Korsakoff ve vermis atrofisi", "Tiamin (B1) eksikliği, korpus mammillare hemorajisi, ataksi"],
                    ["Gelişimsel (Fetal)", "Fetal Alkol Sendromu (FAS)", "Mikrosefali, düz filtrum, ince üst dudak, mental retardasyon"]
                ]
            ),
            make_active_recall(
                "Alkolik hepatit tanılı bir hastanın karaciğer biyopsisinde dejenere hepatosit sitoplazmasında izlenen pembe-kırmızı renkli eozinofilik sitokeratin ara filaman yumaklarına ne ad verilir?",
                "Mallory-Denk cisimcikleridir (Mallory hiyaleni).",
                "Hasarlı sitokeratin filamanlarının ubikitinle kümelenmesi sonucu oluşan inklüzyon"
            )
        ]
    })

    return slides
