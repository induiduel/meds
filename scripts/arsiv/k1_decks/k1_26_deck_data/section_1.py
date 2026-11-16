# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 1: İnsan Genomu Mimarisi, Kodlamayan DNA ve Epigenetik Düzenleme (Slayt 1-10)
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

def get_section_1_slides():
    slides = []

    # Slayt 1: Giriş ve Hastalıkta Üçlü Çerçeve
    slides.append({
        "id": "k1-26-s01",
        "title": "Giriş ve Hastalıkta Üçlü Çerçeve",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 1,
        "narrative": (
            "Modern tıbbi patolojide hastalıkların gelişimi ve klinik seyri, tek bir nedensel faktörle açıklanamaz; "
            "hastalıklar üç temel bileşenin dinamik etkileşimiyle şekillenir: "
            "1. **Genetik Zemin:** Bireyin kalıtsal DNA dizilimi, tek gen mutasyonları, kromozomal yapısı ve yatkınlık polimorfizmleri. "
            "2. **Çevresel Maruziyet:** Hava kirliliği, toksik ağır metaller, kimyasal ajanlar, radyasyon, tütün dumanı ve iklimsel faktörler. "
            "3. **Yaşam Tarzı ve Beslenme:** Makro ve mikro besin ögelerinin alımı, kalori fazlalığı veya protein eksikliği, "
            "fiziksel aktivite ve metabolik homeostaz. "
            "Bu **Üçlü Çerçeve (Genetik + Çevre + Beslenme)** bir araya geldiğinde fenotipik hastalık ortaya çıkar. "
            "Örneğin; aynı genetik yatkınlığı taşıyan iki bireyden çevresel toksinlere maruz kalan ve kötü beslenende ağır "
            "organ patolojisi gelişirken, koruyucu çevrede yaşayan birey asemptomatik kalabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Hastalık Patogenezinde Üçlü Çerçeve Modeli",
                ["Bileşen", "Temel Biyolojik İçerik", "Patolojik Etki Örneği"],
                [
                    ["Genetik Zemin", "DNA dizilimi, kromozomlar, polimorfizmler", "Kistik fibrozis (CFTR), Marfan (FBN1), HLA yatkınlıkları"],
                    ["Çevresel Faktörler", "Hava kirliliği, toksinler, iklim, kurşun, sigara", "Kurşun anemisi/nöropatisi, silikozis, ozon hasarı"],
                    [
                        "Beslenme ve Yaşam Tarzı",
                        "Kalori dengesi, protein alımı, vitaminler, obezite",
                        {"text": "Kwashiorkor, marasmus, metabolik sendrom, steatoz", "isMasked": True, "hint": "Protein ve kalori açığı veya yağ birikimi ile karakterize beslenme bozuklukları"}
                    ]
                ]
            ),
            make_active_recall(
                "Modern patolojide insan hastalıklarının gelişimini belirleyen ve klinik yaklaşımda mutlaka birlikte değerlendirilmesi gereken üçlü nedensel çerçeve hangi bileşenlerden oluşur?",
                "Genetik zemin, çevresel maruziyet ile yaşam tarzı ve beslenme dengesidir.",
                "Kalıtsal miras, dış fizikokimyasal ortam ve metabolik gıda alımının kesişimi"
            )
        ]
    })

    # Slayt 2: İnsan Genomunun Büyüklüğü ve Yapısı
    slides.append({
        "id": "k1-26-s02",
        "title": "İnsan Genomunun Büyüklüğü ve Yapısı",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 2,
        "narrative": (
            "İnsan genomu yaklaşık **3.3 milyar baz çiftinden (bç)** meydana gelen devasa bir moleküler kütüphanedir: "
            "1. **Protein Kodlayan Genler:** Genomumuzda yaklaşık **19.000 ile 20.000 adet** protein kodlayan gen bulunur. "
            "Tarihsel olarak tahmin edilen 100.000 gen beklentisinin aksine, insan proteomunun karmaşıklığı gen sayısından "
            "ziyade alternatif uçbirleştirme (alternative splicing) ve translasyon sonrası modifikasyonlarla sağlanır. "
            "2. **Kodlayan Fraksiyonun Oranı:** Tüm bu 19.000 genin ekzonik dizileri (yani doğrudan proteine tercüme edilen kısımlar), "
            "tüm insan genomunun **yalnızca %1.5'ini** oluşturur. "
            "3. **Kodlamayan Genom:** Geriye kalan **%98.5'lik devasa nükleotid dizisi** geçmişte yanıltıcı şekilde 'çöp DNA' "
            "(junk DNA) olarak adlandırılmışsa da, günümüzde bu bölgelerin gen ekspresyonunu, hücresel kimliği ve gelişimi "
            "yöneten kritik düzenleyici orkestra şefi olduğu kanıtlanmıştır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İnsan Genomunun Yapısal Metrikleri",
                ["Genomik Parametre", "Sayısal Değer / Ölçü", "Biyolojik Karşılığı"],
                [
                    ["Toplam Nükleotid Boyutu", "~3.3 Milyar Baz Çifti", "Haploid insan genomunun toplam DNA içeriği"],
                    [
                        "Protein Kodlayan Gen Adedi",
                        {"text": "~19.000 - 20.000 gen", "isMasked": True, "hint": "İnsan proteomunu oluşturan protein kodlayıcı genlerin yaklaşık sayısı"},
                        "Tüm hücresel enzimatik ve yapısal proteinlerin kalıbı"
                    ],
                    ["Protein Kodlayan Ekzon Oranı", "Tüm genomun yalnız %1.5'i", "Doğrudan polipeptide çevrilen aminoasit kodlama alanı"],
                    ["Kodlamayan Bölge Oranı", "Genomun %98.5'i", "Promotörler, güçlendiriciler, intronlar ve düzenleyici ncRNA'lar"]
                ]
            ),
            make_micro_quiz(
                "İnsan genomunun nükleotid yapısı ve protein kodlama kapasitesi ile ilgili olarak aşağıda verilen ifadelerden hangisi BİLİMSEL OLARAK DOĞRUDUR?",
                {
                    "A": "Protein kodlayan ekzonik diziler genomun yalnızca yaklaşık %1.5'lik kısmını oluşturur",
                    "B": "İnsan genomunda 150.000'den fazla bağımsız protein kodlayan gen mevcuttur",
                    "C": "Kodlamayan %98.5'lik DNA bölgesi hücresel işlevi olmayan tamamen inaktif atık dizilerdir",
                    "D": "Genomun toplam büyüklüğü yaklaşık 300 milyon baz çiftidir",
                    "E": "Tüm hücresel RNA molekülleri mutlaka bir proteine tercüme edilir"
                },
                "A",
                {
                    "A": "Doğrudur; protein kodlayan ekzonlar genomun yalnız %1.5'idir, geri kalan %98.5 düzenleyici mimaridir.",
                    "B": "Yanlış; insan genomunda yalnızca yaklaşık 19.000-20.000 protein kodlayan gen bulunur.",
                    "C": "Yanlış; kodlamayan bölgeler kritik promotör, güçlendirici ve ncRNA'ları barındırır.",
                    "D": "Yanlış; genom boyutu 300 milyon değil, 3.3 milyar baz çiftidir.",
                    "E": "Yanlış; miRNA ve lncRNA gibi fonksiyonel kodlamayan RNA'lar proteine çevrilmez."
                }
            )
        ]
    })

    # Slayt 3: Kodlamayan DNA'nın Biyolojik Rolü
    slides.append({
        "id": "k1-26-s03",
        "title": "Kodlamayan DNA'nın Biyolojik Rolü",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 3,
        "narrative": (
            "Genomun %98.5'ini oluşturan kodlamayan DNA dizileri, hücresel işlevin ve dokuya özgü gen ifadesinin anahtarıdır: "
            "1. **Promotör Bölgeleri (Promoters):** Genlerin hemen transkripsiyon başlangıç bölgesinin yukarısında (upstream) yer alır; "
            "RNA polimeraz ve genel transkripsiyon faktörlerinin DNA'ya bağlandığı, transkripsiyonu başlatan kontrol merkezleridir. "
            "2. **Güçlendiriciler (Enhancers):** Hedef genden bazen **100 kilobaz (kb) veya daha uzakta** yer alabilen, "
            "DNA sarmalının ilmek (looping) yapmasıyla promotörle temas kurarak transkripsiyon hızını yüzlerce kat artıran "
            "dokuya özgü düzenleyici dizilerdir. "
            "3. **İntronlar:** Ekzonların arasına serpiştirilmiş, primer transkriptten alternatif uçbirleştirme ile kesilip "
            "çıkarılan dizilerdir; içlerinde düzenleyici elemanlar ve kodlamayan RNA'lar barındırırlar. "
            "4. **Kromatin Mimarisi Düzenleyicileri:** DNA'nın çekirdek içindeki üç boyutlu katlanmasını ve kromatin "
            "ilmeklerinin sınırlarını belirleyen insülatör (yalıtıcı) diziler ve CTCF bağlanma odaklarıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Promotör ve Güçlendirici (Enhancer) Karşılaştırması",
                "Promotör (Transkripsiyon Başlatıcı)",
                "Genin hemen başında lokalizedir; RNA polimeraz II kompleksini bağlayarak bazal transkripsiyonu ateşler",
                "Güçlendirici / Enhancer (Uzak Düzenleyici)",
                "Genden yüzbinlerce baz uzakta bulunabilir; DNA ilmeklenmesiyle promotöre yaklaşarak doku spesifik ekspresyonu artırır"
            ),
            make_cloze(
                "Hedef genden yüz kilobaz uzakta yer alabilen ve DNA ilmeklenmesiyle promotörle temas kurup transkripsiyonu katlayan dizilere güçlendirici adı verilir.",
                "güçlendirici",
                "Uzak mesafeden gen anlatımını aktive eden dokuya özgü regülatör DNA elemanı"
            )
        ]
    })

    # Slayt 4: Kodlamayan Fonksiyonel RNA'lar: miRNA ve lncRNA
    slides.append({
        "id": "k1-26-s04",
        "title": "Kodlamayan Fonksiyonel RNA'lar: miRNA ve lncRNA",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 4,
        "narrative": (
            "Hücrede transkribe edilen RNA'ların büyük çoğunluğu proteine çevrilmez; bu moleküller 'kodlamayan RNA' (ncRNA) olarak işlev görür: "
            "1. **MikroRNA (miRNA):** Yaklaşık **21-23 nükleotid** uzunluğunda küçük, tek iplikli RNA molekülleridir. "
            "- Sitoplazmada **RISC (RNA-induced silencing complex)** ile birleşir. "
            "- Hedef mRNA'nın 3'-UTR bölgesine kısmi komplementerlikle bağlanır. "
            "- Sonuç: Hedef mRNA'nın **translasyonunu baskılar** veya mRNA'yı parçalayarak **geni translasyonel düzeyde susturur**. "
            "Tek bir miRNA yüzlerce farklı mRNA'yı koordine şekilde regüle edebilir. "
            "2. **Uzun Kodlamayan RNA (lncRNA):** Uzunluğu **>200 nükleotid** olan kodlamayan transkriptlerdir. "
            "- Kromatin yeniden modelleme enzimlerini spesifik gen bölgelerine yönlendirir (scaffold / iskele görevi). "
            "- En klasik örneği: Dişi embriyoda iki X kromozomundan birini kalıcı olarak heterokromatinleştirip inaktive eden "
            "**XIST lncRNA'sıdır**. Kanser patogenezinde de onkojenik veya tümör baskılayıcı lncRNA'lar kritik rol oynar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "MikroRNA (miRNA) Aracılı Gen Susturulması Yolağı",
                [
                    "1. Nükleer Transkripsiyon: Çekirdekte pri-miRNA sentezi ve Drosha enzimiyle pre-miRNA'ya kesilmesi",
                    "2. Sitoplazmaya İhraç: Pre-miRNA'nın Dicer enzimi tarafından 21-23 bç'lik çift iplikli olgun miRNA'ya budanması",
                    "3. RISC Birleşmesi: Tek ipliğin RISC protein kompleksi içine yüklenerek aktif susturucu kompleksi oluşturması",
                    "4. Hedef mRNA Tanıma: Hedef transkriptin 3'-UTR bölgesine baz eşleşmesiyle kilitlenmesi",
                    "5. Translasyonel Blokaj: mRNA'nın ribozomda okunmasının engellenmesi veya degredasyona uğratılması"
                ]
            ),
            make_active_recall(
                "Dişi memeli embriyosunda dozaj kompansasyonu sağlamak amacıyla iki X kromozomundan birini baştan sona kaplayarak inaktive eden prototip uzun kodlamayan RNA hangisidir?",
                "XIST lncRNA'sıdır (X-inactive specific transcript).",
                "Kromatin susturulmasını ve heterokromatinleşmeyi tetikleyen dişi cinsiyet kromozomu inaktivasyon faktörü"
            )
        ]
    })

    # Slayt 5: Kromatin Mimarisi ve Dinamiği: Ökromatin vs Heterokromatin
    slides.append({
        "id": "k1-26-s05",
        "title": "Kromatin Mimarisi ve Dinamiği: Ökromatin vs Heterokromatin",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 5,
        "narrative": (
            "Genomik DNA çekirdekte çıplak halde bulunmaz; nükleozom adı verilen histon oktamerleri (H2A, H2B, H3, H4) "
            "etrafına 1.65 tur sarılarak kromatin yapısını oluşturur. Kromatin iki temel konformasyonel durumda bulunur: "
            "1. **Ökromatin (Aktif Kromatin):** "
            "- Nükleozomlar birbirinden gevşek ve açıktır. "
            "- Işık mikroskopisinde soluk boyanır. "
            "- Transkripsiyon faktörleri ve RNA polimeraz DNA dizilerine kolayca erişebilir. "
            "- Aktif olarak proteine çevrilen genleri barındırır. "
            "2. **Heterokromatin (İnaktif / Sessiz Kromatin):** "
            "- Nükleozomlar son derece sıkı paketlenmiş, yoğun ve kondensedir. "
            "- Işık mikroskopisinde koyu bazofilik boyanır (çekirdek zarına yakın yerleşimlidir). "
            "- Transkripsiyon aygıtının erişimine kapalıdır; transkripsiyonel olarak **inaktiftir / sessizdir**. "
            "Sentromerler, telomerler ve inaktif X kromozomu (Barr cisimciği) klasik heterokromatindir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Ökromatin ve Heterokromatin Zıtlığı",
                ["Karakteristik Özellik", "Ökromatin", "Heterokromatin"],
                [
                    ["Paketlenme Yoğunluğu", "Gevşek, açık ve dağınık nükleozomlar", "Sıkı, kondense ve yoğun paketli"],
                    ["Transkripsiyonel Aktivite", "Aktif gen ekspresyonu", "Transkripsiyonel olarak inaktif ve sessiz"],
                    ["Mikroskobik Görünüm", "Açık renkli, soluk nükleoplazma", "Koyu bazofilik, nükleer membran kenarı"],
                    [
                        "Klasik Örnek",
                        "Hücrenin ihtiyaç duyduğu fonksiyonel genler",
                        {"text": "Barr cisimciği (inaktif X kromozomu) ve sentromerler", "isMasked": True, "hint": "Dişilerde heterokromatine dönüşerek susturulan cinsiyet kromozomu yapısı"}
                    ]
                ]
            ),
            make_before_after(
                "Kromatin Konformasyonunun Gen İfadesine Etkisi",
                "Ökromatik Durum (Erişilebilir DNA)",
                "Histon asetilasyonu ile pozitif yükün nötralize edilmesi ve transkripsiyon faktörlerinin gen promotörlerine serbestçe bağlanması",
                "Heterokromatik Durum (Kondanse DNA)",
                "Histon deasetilasyonu ve DNA metilasyonu ile nükleozomların kilitlenmesi ve genlerin transkripsiyondan tamamen men edilmesi"
            )
        ]
    })

    # Slayt 6: Genetik Varyasyon Tipleri 1: SNP ve Farmakogenomik
    slides.append({
        "id": "k1-26-s06",
        "title": "Genetik Varyasyon Tipleri 1: SNP ve Farmakogenomik",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 6,
        "narrative": (
            "İnsanlar arasında DNA dizilim benzerliği %99.5'in üzerindedir; bireyler arasındaki morfolojik, biyokimyasal "
            "ve hastalıklara yatkınlık farklarını genetik varyasyonlar yönetir: "
            "1. **Tek Nükleotid Polimorfizmi (SNP - Single Nucleotide Polymorphism):** "
            "- Genomda tek bir baz çifti pozisyonunda görülen kalıcı varyasyonlardır (Örn: Bir bireyde A-T varken diğerinde G-C olması). "
            "- Bir varyasyonun polimorfizm sayılması için toplumda **en az %1 sıklıkta** bulunması gerekir. "
            "- İnsan genomunda milyonlarca SNP haritalanmıştır. Çoğu kodlamayan bölgelerde yer alır ve nötrdür. "
            "2. **Kodlayan Bölge SNP'leri:** Aminoasit değişimine yol açarak protein fonksiyonunu veya katlanmasını modifiye edebilir. "
            "3. **Farmakogenomik ve Klinik Önem:** "
            "- Karaciğer sitokrom P450 enzim genlerindeki (CYP2D6, CYP2C19 vb.) SNP'ler, ilaçların metabolizma hızını belirler. "
            "- 'Hızlı metabolize ediciler' ilacı hızla inaktive ederken, 'yavaş metabolize ediciler' standart dozda ölümcül toksisiteye uğrayabilir. "
            "- Kompleks multifaktöriyel hastalıkların (hipertansiyon, ateroskleroz, diyabet) genetik yatkınlığı SNP panelleriyle ölçülür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "SNP Varyasyonlarının Klinik ve Biyolojik Dağılımı",
                ["Yerleşim Bölgesi", "Biyolojik Mekanizma", "Klinik / Fenotipik Sonuç"],
                [
                    ["Kodlayan Ekzonik Alan", "Mis-sense aminoasit değişimi", "Protein aktivitesinde hafif artış veya azalma"],
                    ["Promotör / Güçlendirici", "Transkripsiyon faktörü afinitesini değiştirme", "Gen ekspresyon düzeyinde kantitatif değişim"],
                    [
                        "İlaç Metabolizma Enzimleri",
                        {"text": "Sitokrom P450 izoenzim polimorfizmi (CYP varyantları)", "isMasked": True, "hint": "Kişiselleştirilmiş ilaç yanıtını ve toksisite riskini belirleyen hepatik enzim ailesi"},
                        "Bireyler arası farklı ilaç etkinlik ve yan etki profili (Farmakogenomik)"
                    ]
                ]
            ),
            make_active_recall(
                "İlaçların karaciğerde metabolize edilme hızını, terapötik etkinliğini ve toksisite riskini bireyler arasında farklı kılan en yaygın tek bazlık genetik varyasyonlara ne ad verilir?",
                "Tek nükleotid polimorfizmleri (SNP) ve farmakogenomik varyasyonlardır.",
                "Toplumda yüzde birin üzerinde sıklıkla görülen tek baz çifti alternatifleri"
            )
        ]
    })

    # Slayt 7: Genetik Varyasyon Tipleri 2: Kopya Sayısı Varyasyonları (CNV)
    slides.append({
        "id": "k1-26-s07",
        "title": "Genetik Varyasyon Tipleri 2: Kopya Sayısı Varyasyonları (CNV)",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 7,
        "narrative": (
            "Genetik varyasyonların ikinci büyük sınıfı, tek bazdan çok daha büyük segmentleri kapsayan yapısal değişimlerdir: "
            "1. **Kopya Sayısı Varyasyonu (CNV - Copy Number Variation):** "
            "- Boyutu **1 kilobazdan (1.000 bç) birkaç megabaza (milyonlarca bç)** kadar uzanan DNA parçalarının delesyonu (kaybı) "
            "veya duplikasyonu (çoğalması) ile karakterizedir. "
            "2. **Genomik Kapsam:** İki sağlıklı insan karşılaştırıldığında, baz sayısı açısından genomik farklılıkların "
            "yaklaşık yarısı CNV'lerden kaynaklanır; çünkü tek bir CNV yüzlerce geni birden kapsayabilir. "
            "3. **Klinik Fenotipler:** "
            "- CNV'ler gen dozajını doğrudan değiştirir. "
            "- Nörogelişimsel bozukluklar, **otizm spektrum bozukluğu**, şizofreni ve nedeni açıklanamayan mental/motor gelişimsel geriliklerde "
            "yüksek oranda de novo patojenik CNV'ler saptanır. "
            "- Ayrıca belirli kanser türlerine genetik yatkınlıkta da önemli rol oynarlar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "SNP ve CNV Arasındaki Boyutsal ve Mekanik Zıtlık",
                "Tek Nükleotid Polimorfizmi (SNP)",
                "Tek bir baz çifti değişimidir; genellikle minör yatkınlıklar ve ilaç metabolizma hızlarını modüle eder",
                "Kopya Sayısı Varyasyonu (CNV)",
                "Binlerce ila milyonlarca bazı kapsayan delesyon veya duplikasyondur; gen dozajını değiştirerek otizm ve gelişim geriliği yapar"
            ),
            make_cloze(
                "Boyutu bin bazdan milyonlarca baza kadar uzanan DNA parçalarının delesyonu veya duplikasyonuyla oluşan varyasyonlara kopya sayısı varyasyonu adı verilir.",
                "kopya sayısı varyasyonu",
                "Gen dozajını değiştirerek otizm ve gelişimsel anomalilere yol açabilen büyük segmenter genomik değişim"
            )
        ]
    })

    # Slayt 8: Epigenetik Mekanizmalar: DNA Metilasyonu ve Histon Kodları
    slides.append({
        "id": "k1-26-s08",
        "title": "Epigenetik Mekanizmalar: DNA Metilasyonu ve Histon Kodları",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 8,
        "narrative": (
            "Epigenetik, **DNA nükleotid diziliminde hiçbir mutasyon veya değişiklik olmaksızın**, gen ekspresyonunun mitoz "
            "boyunca stabil ve kalıtsal şekilde düzenlenmesidir: "
            "1. **DNA Metilasyonu:** "
            "- Sitozin bazlarına DNA metiltransferazlar (DNMT) tarafından metil grubu eklenmesiyle **5-metilsitozin** oluşur. "
            "- Metilasyon tipik olarak gen promotörlerindeki CG zengini adalarda (**CpG adaları**) gerçekleşir. "
            "- **Altın Kural:** Bir gen promotörünün yoğun metillenmesi (hipermetilasyon), o genin transkripsiyonel olarak "
            "**tamamen susturulmasına (gen sessizleşmesi)** yol açar. "
            "2. **Histon Modifikasyonları:** "
            "- **Histon Asetilasyonu (HAT):** Lizin kalıntılarına asetil eklenmesi pozitif yükü nötralize eder; histon-DNA bağını "
            "gevşetir ve transkripsiyonu **aktive eder** (açık kromatin). "
            "- **Histon Deasetilasyonu (HDAC):** Asetili uzaklaştırarak kromatini kapatır ve geni **susturur**. "
            "- Histon metilasyonu ise modifiye olan aminoaside göre aktivasyon veya baskılama yapabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Promotör Hipermetilasyonu ile Gen Susturulması Zinciri",
                [
                    "1. Enzimatik Uyarım: DNA metiltransferazların (DNMT) promotör CpG adalarını tanıması",
                    "2. Sitozin Modifikasyonu: Sitozin halkalarına kovalent metil grubu eklenerek 5-metilsitozin yapılması",
                    "3. Baskılayıcı Protein Bağlanması: Metil-CpG bağlayıcı proteinlerin (MeCP2) modifiye adalara kilitlenmesi",
                    "4. Histon Deasetilaz Toplanması: HDAC enzimlerinin bölgeye çekilerek kromatini aşırı yoğunlaştırması",
                    "5. Transkripsiyonel Felç: RNA polimeraz II erişiminin engellenmesi ve genin tamamen sessizleştirilmesi"
                ]
            ),
            make_active_recall(
                "Gen promotörlerindeki CpG adalarında yer alan sitozin bazlarının DNA metiltransferazlarca yoğun şekilde metillenmesinin (hipermetilasyon) gen ifadesi üzerindeki temel net etkisi nedir?",
                "Genin transkripsiyonunun kalıcı olarak susturulmasıdır (gen sessizleşmesi).",
                "Kromatinin kilitlenerek RNA polimeraz II erişiminin durdurulması sonucu"
            )
        ]
    })

    # Slayt 9: Checkpoint 1
    slides.append({
        "id": "k1-26-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] İnsan Genomu, Varyasyonlar ve Epigenetik Temeller",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 9,
        "narrative": (
            "İlk bölüm kontrol noktamızda genomun temel mimarisini ve epigenetik düzenlemeyi pekiştiriyoruz: "
            "1. **Genom Metrikleri:** 3.3 milyar baz çifti, ~19.000 protein kodlayan gen; ekzonlar genomun yalnız %1.5'idir. "
            "2. **Kodlamayan Mimarisi:** Promotörler transkripsiyonu başlatır; güçlendiriciler (enhancers) 100 kb uzaktan bile "
            "ilmek yaparak gen ekspresyonunu hızlandırır. "
            "3. **Düzenleyici ncRNA:** miRNA (21-23 nt) RISC ile mRNA 3'-UTR'sine bağlanıp translasyonu baskılar; lncRNA (>200 nt) "
            "iskelet oluşturur (XIST X inaktivasyonu yapar). "
            "4. **Kromatin Durumu:** Ökromatin gevşek ve aktif; heterokromatin kondanse ve sessizdir. "
            "5. **Varyasyonlar:** SNP tek bazlık en yaygın varyasyondur (farmakogenomik); CNV ise kilobaz-megabazlık delesyon/duplikasyondur (otizm, gelişim geriliği). "
            "6. **Epigenetik Kod:** DNA dizisi değişmez; CpG metilasyonu geni susturur; histon asetilasyonu kromatini açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s09-1",
                "İnsan genomunda protein kodlayan genlerin tüm nükleotid dizisine oranı yaklaşık yüzde kaçtır?",
                "Yalnızca yüzde bir buçukluk kısımdır.",
                "Ekzonik dizilerin toplam nükleotid kütlesi içindeki minimal payı",
                "Genom Mimarisi"
            ),
            make_flashcard(
                "k1-26-fc-s09-2",
                "Tek bir nükleotid pozisyonunda toplumda en az yüzde bir sıklıkla görülen ve farmakogenomik yanıtı belirleyen genetik varyasyon tipi nedir?",
                "Tek nükleotid polimorfizmidir (SNP).",
                "Bireyler arasındaki baz çifti dizilim çeşitliliğinin en yaygın moleküler formu",
                "Genetik Varyasyon"
            ),
            make_flashcard(
                "k1-26-fc-s09-3",
                "DNA nükleotid dizisinde hiçbir değişiklik olmadan gen ekspresyonunun kalıcı olarak düzenlenmesi ve promotör hipermetilasyonu ile gen susturulması mekanizmasına ne ad verilir?",
                "Epigenetik modifikasyondur.",
                "Sitozin bazlarına metil grupları eklenmesi ve kromatin yapısının kimyasal olarak yeniden şekillenmesi",
                "Epigenetik"
            )
        ],
        "interactiveElements": [
            make_table(
                "Genetik ve Epigenetik Temeller Karşılaştırma Matrisi",
                ["Kavram", "Temel Biyolojik Mekanizma", "Tipik Boyut / Kapsam", "Klinik Örnek"],
                [
                    ["Protein Kodlayan Genler", "Ekzonik aminoasit kalıbı", "~19.000 gen (%1.5)", "Enzimler, yapısal proteinler"],
                    ["Güçlendirici (Enhancer)", "Uzak düzenleyici DNA dizisi", "Genden >100 kb uzakta", "Doku spesifik transkripsiyon artışı"],
                    [
                        "Tek Nükleotid Polimorfizmi",
                        "Tek baz çifti alternatifi",
                        {"text": "1 baz çifti (SNP)", "isMasked": True, "hint": "Toplumda yüzde birden sık görülen tek nükleotidlik varyasyon boyutu"},
                        "İlaç metabolizması (CYP enzimleri)"
                    ],
                    ["Kopya Sayısı Varyasyonu", "Delesyon veya duplikasyon", "1 kb - birkaç megabaz", "Otizm, mental retardasyon"],
                    ["DNA Hipermetilasyonu", "CpG adalarına metil eklenmesi", "Promotör dizileri", "Tümör baskılayıcı gen susturulması"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi ökromatinin heterokromatinden ayırt edilmesini sağlayan temel moleküler ve morfolojik özelliktir?",
                {
                    "A": "Nükleozomların gevşek paketlenmiş olması ve aktif gen transkripsiyonuna izin vermesi",
                    "B": "Yalnızca sentromer ve telomerik bölgelerde lokalize olması",
                    "C": "Transkripsiyonel olarak tamamen sessiz ve inaktif kalması",
                    "D": "DNA metilasyon oranının heterokromatine göre katbekat yüksek olması",
                    "E": "Işık mikroskobunda nükleer membran çevresinde koyu bazofilik kütleler oluşturması"
                },
                "A",
                {
                    "A": "Doğrudur; ökromatin dağınık, açık nükleozom yapısına ve yüksek transkripsiyonel aktiviteye sahiptir.",
                    "B": "Yanlış; sentromer ve telomerler heterokromatindir.",
                    "C": "Yanlış; inaktif ve sessiz olan heterokromatindir.",
                    "D": "Yanlış; hipermetilasyon heterokromatinde yoğundur.",
                    "E": "Yanlış; koyu bazofilik kütle heterokromatindir."
                }
            )
        ]
    })

    # Slayt 10: Kanser ve Hastalıklarda Epigenetik Sapmalar
    slides.append({
        "id": "k1-26-s10",
        "title": "Kanser ve Hastalıklarda Epigenetik Sapmalar",
        "section": "Genom Mimarisi ve Epigenetik",
        "slideNumber": 10,
        "narrative": (
            "Epigenetik mekanizmalar malign neoplazilerde ve kronik edinsel hastalıklarda genetik mutasyonlar kadar ölümcül rol oynar: "
            "1. **Tümör Baskılayıcı Genlerin Susturulması:** "
            "- Karsinojenezde en sık görülen epigenetik sapma, **tümör baskılayıcı genlerin promotör CpG adalarının hipermetillenmesidir**. "
            "- Örnek: Kolon kanserinde DNA uyumsuzluk tamir geni **MLH1** promotörünün hipermetilasyonu, gen dizisi sağlam "
            "olduğu halde enzimi sıfırlar; bu durum mikrosatellit instabilitesine (MSI) ve maligniteye yol açar. "
            "- Meme kanserinde BRCA1, retinoblastomda RB genleri de mutasyon olmaksızın epigenetik metilasyonla susturulabilir. "
            "2. **Global Hipometilasyon:** Kanser hücrelerinde tüm genom genelinde yaygın hipometilasyon görülür; bu durum "
            "kromozomal instabiliteye ve transpozonların aktifleşmesine zemin hazırlar. "
            "3. **Epigenetik Tedavi Fırsatı:** Genetik mutasyonlar geri döndürülemezken, epigenetik değişiklikler DNA dizisini "
            "değiştirmediği için **geri dönüşümlüdür (reversibl)**. DNMT inhibitörleri (Azasitidin, Desitabin) ve HDAC inhibitörleri "
            "(Vorinostat) miyelodisplastik sendrom ve lenfomalarda susturulmuş koruyucu genleri yeniden uyandırır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Genetik Mutasyon vs Epigenetik Susturulma Ayrımı",
                "Genetik Mutasyon (Kalıcı Sekans Değişimi)",
                "DNA baz dizisinde delesyon, insersiyon veya nokta mutasyonu vardır; primer dizi bozulmuştur ve geri dönüşümsüzdür",
                "Epigenetik Susturulma (Kimyasal İşaretleme)",
                "DNA baz dizisi tamamen kusursuzdur; promotör CpG hipermetilasyonu geni sessizleştirir ve ilaçlarla geri döndürülebilir"
            ),
            make_active_recall(
                "Kolorektal karsinomlarda DNA tamir geni MLH1'in nükleotid dizisinde hiçbir mutasyon olmadığı halde enzimin üretilememesine ve mikrosatellit instabilitesine yol açan temel epigenetik anomali nedir?",
                "Promotör CpG adalarının hipermetilasyonudur.",
                "DNA metiltransferazlarca genin başlangıç bölgesine yoğun metil grubu eklenmesi"
            )
        ]
    })

    return slides
