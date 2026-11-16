# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 3: Kistik Fibrozis ve Sitogenetik Hastalıklar (Slayt 21-30)
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

def get_section_3_slides():
    slides = []

    # Slayt 21: Kistik Fibrozis Etyolojisi: CFTR Geni ve İyon Kanalı
    slides.append({
        "id": "k1-26-s21",
        "title": "Kistik Fibrozis Etyolojisi: CFTR Geni ve İyon Kanalı",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 21,
        "narrative": (
            "Kistik Fibrozis (KF / Mukovissidoz), beyaz ırkta en sık görülen, yaşamı tehdit eden ölümcül **otozomal resesif** hastalıktır: "
            "1. **Genetik Temel:** Kromozom **7q31.2** lokusunda yer alan **CFTR (Cystic Fibrosis Transmembrane Conductance Regulator)** "
            "genindeki mutasyonlardan kaynaklanır. Taşıyıcılık sıklığı beyaz popülasyonda yaklaşık 1/25'tir. "
            "2. **CFTR Proteini:** ATP-bağlayıcı kaset (ABC) taşıyıcı protein ailesine mensup bir transmembran iyon kanalıdır. "
            "- Hücre zarında **klorür ($Cl^-$) ve bikarbonat ($HCO_3^-$)** anyonlarının geçişini düzenler. "
            "- cAMP bağımlı protein kinaz A (PKA) fosforilasyonu ile aktive olur. "
            "3. **Fizyolojik Görevi:** Ekzokrin bezlerin ve solunum epitelinin lümenine klorür ve su salgılanmasını sağlayarak "
            "mukusun akışkanlığını (hidrasyonunu) korur. CFTR defektinde tüm ekzokrin salgılar dehidrate, yapışkan ve koyu kıvamlı hale gelir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "CFTR Proteini ve Kistik Fibrozis Temelleri",
                ["Genomik / Biyokimyasal Parametre", "Biyolojik Karşılığı", "Patofizyolojik Fonksiyonu"],
                [
                    ["Kromozom Haritası", "7q31.2", "CFTR gen lokusu"],
                    ["Kalıtım Şekli", "Otozomal Resesif (OR)", "Homozigot mutantlarda klinik hastalık tablosu"],
                    [
                        "Taşıyıcı Protein Sınıfı",
                        {"text": "ATP-bağlayıcı kaset (ABC) ailesi klorür/bikarbonat kanalı", "isMasked": True, "hint": "cAMP bağımlı anyon iletimini sağlayan transmembran pompa yapısı"},
                        "Epitel lümenine klor ve bikarbonat sekresyonu"
                    ],
                    ["Temel Patolojik Problem", "Salgıların dehidratasyonu ve viskozite artışı", "Mukus tıkaçları, organ kanal tıkanıklıkları"]
                ]
            ),
            make_active_recall(
                "Kistik fibrozis hastalığında epitel hücre zarlarında klorür ve bikarbonat anyonlarının geçişini yöneten ve cAMP ile aktive olan iyon kanalı proteininin adı nedir?",
                "CFTR proteinidir (Kistik Fibrozis Transmembran İletkenlik Düzenleyicisi).",
                "Yedinci kromozomda kodlanan anyon geçirgenliği regülatörü"
            )
        ]
    })

    # Slayt 22: CFTR Mutasyon Sınıfları ve Delta-F508 Defekti
    slides.append({
        "id": "k1-26-s22",
        "title": "CFTR Mutasyon Sınıfları ve Delta-F508 Defekti",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 22,
        "narrative": (
            "CFTR geninde 2000'den fazla farklı mutasyon tanımlanmıştır ve bunlar altı ana sınıfa ayrılır: "
            "1. **Sınıf I (Sentez Yokluğu):** Erken stop kodonu; fonksiyonel protein hiç üretilmez (Örn: G542X). "
            "2. **Sınıf II (Katlanma ve İşlenme Kusuru - EN SIK):** "
            "- Dünya genelinde kistik fibrozis hastalarının yaklaşık **%70'inde saptanan delta-F508 (Phe508del)** mutasyonudur. "
            "- 508. pozisyondaki **fenilalanin aminoasidinin 3 bazlık delesyonudur**. "
            "- Protein sentezlenir ancak endoplazmik retikulumda (ER) hatalı katlanır; ER kalite kontrol sistemi proteini tanır, "
            "hücre zarına ulaşmasına izin vermeden **proteazomlarda tamamen parçalar**. "
            "3. **Sınıf III (Düzenleme / Açılma Bozukluğu):** Protein zardadır ancak kanal kapısı açılmaz (Örn: G551D). "
            "4. **Sınıf IV (İletkenlik Azalması):** Klor akışı yavaştır. "
            "5. **Sınıf V-VI:** Azalmış sentez veya zarda instabilite."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "CFTR Mutasyon Sınıflaması ve Moleküler Mekanizmalar",
                ["Sınıf", "Moleküler Bozukluk", "Prototip Mutasyon", "Zardaki Durum"],
                [
                    ["Sınıf I", "Transkripsiyon/translasyon durması", "Nonsense mutasyonlar (G542X)", "Zarda protein hiç yok"],
                    [
                        "Sınıf II (En Sık)",
                        "Endoplazmik retikulumda hatalı katlanma ve yıkım",
                        {"text": "Delta-F508 (Fenilalanin-508 delesyonu)", "isMasked": True, "hint": "Kistik fibrozis vakalarının yüzde yetmişinden sorumlu olan aminoasit kaybı"},
                        "Zara ulaşamaz, proteazomda yok edilir"
                    ],
                    ["Sınıf III", "Kanal kapısının açılamaması (gating defekti)", "G551D", "Zarda var ama inaktif"],
                    ["Sınıf IV", "Kanal por iletkenliğinin azalması", "R117H", "Zarda var, düşük anyon akışı"]
                ]
            ),
            make_active_recall(
                "Dünya genelinde kistik fibrozis vakalarının yaklaşık %70'inden sorumlu olan ve proteinin endoplazmik retikulumda hatalı katlanarak hücre zarına ulaşamadan proteazomlarda yıkılmasına neden olan en sık mutasyon nedir?",
                "Delta-F508 (Phe508del) mutasyonudur.",
                "Beş yüz sekizinci pozisyondaki fenilalanin aminoasit kodonunun 3 bazlık delesyonu"
            )
        ]
    })

    # Slayt 23: Solunum Epitelinde CFTR Arızası ve ENaC
    slides.append({
        "id": "k1-26-s23",
        "title": "Solunum Epitelinde CFTR Arızası ve ENaC",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 23,
        "narrative": (
            "Solunum yolu mukozasında CFTR kanalı ile epitel sodyum kanalı (**ENaC**) arasında hayati bir fonksiyonel denge vardır: "
            "1. **Normal Solunum Epiteli:** Sağlam CFTR kanalı klorürü lümene pompalar ve **ENaC kanalını fizyolojik olarak inhibe eder "
            "(frenler)**. Böylece sodyum ve suyun hücre içine aşırı emilmesi engellenir; mukus hidrate ve akışkan kalır. "
            "2. **Kistik Fibroziste Solunum Epiteli:** "
            "- CFTR çalışmadığında klorür lümene sekrete edilemez. "
            "- En kritiği: **CFTR'nin ENaC üzerindeki inhibitör freni ortadan kalkar!** "
            "- ENaC aşırı aktifleşir (hiperaktif); lümendeki sodyumu ($Na^+$) ve peşinden ozmotik olarak suyu hücre içine çeker. "
            "3. **Sonuç: Dehidrate Yapışkan Mukus:** "
            "- Epitel yüzey sıvısı tamamen kurur; mukus son derece yapışkan, koyu ve vizkoz bir hal alır. "
            "- Mukosiliyer temizleme asansörü (silyalar) bu ağır jel tabakasını hareket ettiremez ve felç olur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Solunum Yolunda Dehidrate Mukus ve Silier Felç Zinciri",
                [
                    "1. CFTR İnhibisyonu: Solunum epitel apikal membranında CFTR klorür kanalının yokluğu",
                    "2. ENaC Disinhibisyonu: Klor kanalının freni kalkınca ENaC sodyum kanallarının hiperaktifleşmesi",
                    "3. Masif Su Emilimi: Sodyumun hücre içine çekilmesiyle lümendeki suyun ozmotik olarak epitele geri emilmesi",
                    "4. Dehidrate Jel Tabakası: Epitel yüzey sıvısının tükenmesi ve mukusun viskoz yapışkan çamura dönmesi",
                    "5. Mukosiliyer Felç: Silyaların mukus altında ezilmesi, mukus tıkaçları ve bakteriyel kolonizasyon"
                ]
            ),
            make_before_after(
                "Normal vs Kistik Fibrozis Solunum Epiteli Ayrımı",
                "Normal Solunum Epiteli",
                "CFTR klor salgılar, ENaC'ı frenler; yeterli su tabakası üzerinde silyalar mukusu serbestçe yukarı süpürür",
                "Kistik Fibrozis Epiteli",
                "Klor salgısı durur, ENaC freni kalkar; su hücre içine çekilir, dehidrate vizkoz mukus silyaları kilitler"
            )
        ]
    })

    # Slayt 24: Ter Bezinde CFTR Paradoksu: "Tuzlu Ter"
    slides.append({
        "id": "k1-26-s24",
        "title": "Ter Bezinde CFTR Paradoksu: Tuzlu Ter",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 24,
        "narrative": (
            "CFTR kanalının ter bezindeki fonksiyonu solunum epitelinin **tam tersi (zıt) bir fizyolojiye** sahiptir: "
            "1. **Normal Ter Bezi Fizyolojisi:** "
            "- Ter bezi duktusunda primer salgı lümenden geçerken, CFTR klorürü lümenden hücre içine geri emer ($Cl^-$ absorbsiyonu). "
            "- Elektriksel gradyantı dengelemek için sodyum da hücre içine geri emilir. "
            "- Böylece cilt yüzeyine ulaşan nihai ter sıvısı hipotoniktir (tuzu alınmış sudur). "
            "2. **Kistik Fibroziste Ter Bezi Arızası:** "
            "- Duktusta CFTR çalışmadığı için **klorür geri emilemez**; klor içeride kalamayınca sodyum da lümende kalır. "
            "- Duktus epitelinin suya geçirgenliği düşük olduğundan su çekilemez ve **tuz (NaCl) cilt yüzeyine atılır**. "
            "3. **Klinik Tanısal Altın Standart: Ter Testi:** "
            "- Kistik fibrozisli bebekleri anneleri öptüklerinde 'tuzlu tat' aldıklarını söylerler. "
            "- İyontoforez yöntemiyle toplanan terde **klorür konsantrasyonunun >60 mEq/L bulunması** kistik fibrozis için kesin tanısaldır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "CFTR Kanalının Dokuya Özgü Zıt Çalışma Prensibi",
                "Solunum Yolu ve Bağırsak Epiteli",
                "CFTR lümene klorür SALGILAR; mutasyonunda lümen susuz kalır ve salgılar kurur",
                "Ter Bezi Duktus Epiteli",
                "CFTR lümenden klorürü GERİ EMER; mutasyonunda geri emilim çöker ve terde masif tuz birikir (>60 mEq/L)"
            ),
            make_cloze(
                "Kistik fibrozis tanısında altın standart olan ter testinde ter klorür düzeyinin litrede 60 mEq üzerinde bulunması kesin tanı koydurucudur.",
                "ter testinde",
                "Pilokarpin iyontoforezi ile deri yüzeyinden toplanan sıvıda klor konsantrasyonu ölçüm yöntemi"
            )
        ]
    })

    # Slayt 25: Kistik Fibroziste Akciğer Patolojisi ve Enfeksiyonlar
    slides.append({
        "id": "k1-26-s25",
        "title": "Kistik Fibroziste Akciğer Patolojisi ve Enfeksiyonlar",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 25,
        "narrative": (
            "Kistik fibrozisli hastaların %80-90'ında morbidite ve mortalite akciğer komplikasyonlarından kaynaklanır: "
            "1. **Mukus Tıkaçları ve Bronşiektazi:** "
            "- Dehidrate viskoz mukus bronş ve bronşiyol lümenlerini tıkar; atelektazi ve hava hapsi oluşturur. "
            "- Tekrarlayan enfeksiyonlar bronş duvarındaki kıkırdak ve elastik dokuyu yıkarak **yaygın silindirik ve kistik bronşiektaziye** yol açar. "
            "2. **Mikrobiyolojik Kolonizasyon Dinamiği (Yaşa Göre Değişim):** "
            "- **Bebeklik ve Erken Çocukluk:** En sık izole edilen patojenler **Staphylococcus aureus** ve kapsüllü *Haemophilus influenzae*'dır. "
            "- **Ergenlik ve Erişkinlik:** Hastaların neredeyse tamamı **Pseudomonas aeruginosa** ile kronik olarak kolonize olur. "
            "- P. aeruginosa lümende 'aljinat' kapsülü üreterek **mukoid fenotipe** dönüşür ve biyofilm oluşturur; antibiyotiklere ve immün sisteme direnç kazanır. "
            "- **Burkholderia cepacia:** Ağır fulminan pnömoni ve hızlanmış solunum çöküşüne ('cepacia sendromu') neden olan korkulan patojendir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kistik Fibroziste Solunum Yolu Patojenleri Spektrumu",
                ["Mikroorganizma", "Baskın Olduğu Yaş Dönemi", "Klinik / Patolojik Karakteri"],
                [
                    ["Staphylococcus aureus", "Bebeklik ve erken çocukluk", "Erken bronkopnömoni ve apse odakları"],
                    ["Haemophilus influenzae", "İlk çocukluk yılları", "Rekürren bronşit atakları"],
                    [
                        "Pseudomonas aeruginosa",
                        "Ergenlik ve erişkinlik (>%80)",
                        {"text": "Mukoid biyofilm tabakası ile kronik dirençli bronşiektazi", "isMasked": True, "hint": "Aljinat polimeri salgılayarak akciğerde ömür boyu yerleşen gram negatif basil"}
                    ],
                    ["Burkholderia cepacia", "İleri evre adolesan / erişkin", "Ağır nekrotizan pnömoni ve cepacia sendromu"]
                ]
            ),
            make_micro_quiz(
                "Kistik fibrozis tanılı 16 yaşındaki bir adolesanın balgam kültüründe aljinat kapsülü üreterek mukoid koloniler oluşturan, antibiyotiklere yüksek direnç sergileyen ve kronik bronşiektazinin ana etkeni olan bakteri hangisidir?",
                {
                    "A": "Pseudomonas aeruginosa",
                    "B": "Streptococcus pneumoniae",
                    "C": "Mycoplasma pneumoniae",
                    "D": "Legionella pneumophila",
                    "E": "Mycobacterium leprae"
                },
                "A",
                {
                    "A": "Doğrudur; erişkin KF hastalarının akciğerinde mukoid suşlarıyla yerleşen ve prognozu belirleyen temel ajan P. aeruginosa'dır.",
                    "B": "Yanlış; pnömokok lober pnömoni yapar, KF mukoid kronik ajanı değildir.",
                    "C": "Yanlış; mikoplazma atipik pnömoni etkenidir.",
                    "D": "Yanlış; lejyonella klima sistemlerinden bulaşır.",
                    "E": "Yanlış; cüzzam etkenidir."
                }
            )
        ]
    })

    # Slayt 26: Kistik Fibroziste Gastrointestinal ve Pankreatik Tutulum
    slides.append({
        "id": "k1-26-s26",
        "title": "Kistik Fibroziste Gastrointestinal ve Pankreatik Tutulum",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 26,
        "narrative": (
            "Gastrointestinal sistem ve pankreas, kistik fibrozisin ilk klinik belirtilerinin ortaya çıktığı organlardır: "
            "1. **Mekonyum İleusu (Yenidoğan Belirtisi):** "
            "- KF'li yenidoğanların yaklaşık %10-20'sinde doğumdan sonraki ilk 24-48 saatte mekonyum çıkışı olmaz. "
            "- Aşırı yapışkan ve koyu mekonyum terminal ileum lümenini tıkar; intestinal obstrüksiyon, kusma ve perforasyon riski yaratır. "
            "2. **Pankreatik Ekzokrin Yetmezlik:** "
            "- Hastaların %85-90'ında pankreas kanalları dehidrate mukus tıkaçlarıyla tıkanır. "
            "- Salgılanamayan sindirim enzimleri kanallarda kistik dilatasyonlara ve asinüs otolizine yol açar. "
            "- Zamanla pankreas ekzokrin parankimi tamamen atrofiye uğrar ve yerini yağ ve fibröz bağ dokusuna bırakır (**Kistik Fibrozis adı buradan gelir!**). "
            "3. **Malabsorpsiyon ve Steatore:** "
            "- Lipaz ve proteaz eksikliği nedeniyle yağ ve proteinler sindirilemez; bol miktarda, kötü kokulu, yağlı dışkı (**steatore**) ve "
            "yağda eriyen vitaminlerin (A, D, E, K) ağır eksikliği gelişir. Büyüme-gelişme geriliği belirgindir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Pankreatik Asiner Atrofi ve Steatore Gelişim Basamakları",
                [
                    "1. Duktal Mukus Tıkacı: CFTR yokluğunda duktus epitelinin klor ve bikarbonat salgılayamaması",
                    "2. Kanal Genişlemesi ve İntralüminal Basınç: Sindirim enzimlerinin kanallarda göllenip kistler oluşturması",
                    "3. Enzimatik Otoliz ve Skleroz: Asinüslerin kendi enzimleri tarafından sindirilip fibröz dokuya dönüşmesi",
                    "4. Enzim Yokluğu: Onikiparmak bağırsağına lipaz, amilaz ve tripsin ulaştırılamaması",
                    "5. Ağır Steatore: Yağların emilemeyip dışkıyla atılması ve yağda eriyen vitamin eksiklikleri"
                ]
            ),
            make_active_recall(
                "Kistik fibrozisli bir yenidoğanda doğumdan sonraki ilk 48 saat içinde aşırı yapışkan mukus nedeniyle distal ileumun tıkanmasıyla karakterize ilk klinik tablo nedir?",
                "Mekonyum ileusudur.",
                "Yenidoğanda bağırsak obstrüksiyonuna yol açan ilk barsak içeriği tıkacı"
            )
        ]
    })

    # Slayt 27: Kistik Fibroziste Ürogenital Patoloji: CBAVD
    slides.append({
        "id": "k1-26-s27",
        "title": "Kistik Fibroziste Ürogenital Patoloji: CBAVD",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 27,
        "narrative": (
            "Kistik fibrozis hastalarında ürogenital sistem tutulumu yaşam kalitesini ve üremeyi doğrudan etkiler: "
            "1. **Erkek İnfertilitesi ve CBAVD:** "
            "- Kistik fibrozis tanılı erişkin erkeklerin **>%95'i infertildir (kısırdır)**. "
            "- İnfertilitenin temel nedeni, embriyolojik gelişim sırasında mezonefrik (Wolff) kanal türevlerinin "
            "viskoz salgılarla tıkanıp dejenere olması sonucu gelişen **Konjenital Bilateral Vas Deferens Agenezisidir (CBAVD)**. "
            "- Vas deferens, epididim gövde/kuyruğu ve seminal veziküller iki taraflı olarak yoktur veya kör sonlanır. "
            "2. **Sperm Üretimi:** Testis parankiminde spermatogenez genellikle tamamen normaldir; ancak iletim yolu kapalı olduğu "
            "için ejakülatta sperm bulunmaz (**obstrüktif azospermi**). Bu hastalar testiküler sperm ekstraksiyonu (TESE) ve IVF ile çocuk sahibi olabilirler. "
            "3. **Kadınlarda:** Servikal mukusun aşırı koyu ve viskoz olması spermin geçişini zorlaştırır; subfertilite görülür ancak "
            "gebelik mümkündür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Kistik Fibroziste Erkek vs Kadın Üreme Patolojisi",
                "Erkek Üreme Sistemi (CBAVD)",
                "Bilateral vas deferens agenezisi; normal spermatogeneze rağmen obstrüktif azospermi ve >%95 infertilite",
                "Kadın Üreme Sistemi (Servikal Mukus)",
                "Anatomik kanal anomalisi yoktur; kalın servikal mukus tıkacı mekanik engel oluşturur ve subfertilite yapar"
            ),
            make_cloze(
                "Kistik fibrozisli erişkin erkeklerin yüzde doksan beşinde obstrüktif azospermiye yol açan konjenital anomali bilateral vas deferens agenezisidir.",
                "vas deferens",
                "Testis epididiminden spermi taşıyan sperm kanalının iki taraflı embriyolojik yokluğu"
            )
        ]
    })

    # Slayt 28: Sitogenetik Bozukluklar ve Down Sendromu
    slides.append({
        "id": "k1-26-s28",
        "title": "Sitogenetik Bozukluklar ve Down Sendromu",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 28,
        "narrative": (
            "Sitogenetik hastalıklar, kromozom sayısında veya yapısında ışık mikroskobunda görülebilen majör sapmalardır: "
            "1. **Trizomi 21 (Down Sendromu):** Canlı doğan bebeklerde en sık görülen kromozom anomalisi (1/700) ve "
            "genetik zihinsel geriliğin en yaygın nedenidir. "
            "2. **Sitogenetik Mekanizmalar:** "
            "- **Maternal Mayoz Ayrılamaması (%95):** Oogenez sırasında 21. kromozom çiftinin ayrılamaması (non-disjunction); "
            "anne yaşıyla risk katlanarak artar (20 yaşında 1/1500 iken, 45 yaşında 1/25'e çıkar). "
            "- **Robertsonian Translokasyonu (%4):** 21. kromozomun uzun kolunun genellikle 14 veya 22. kromozoma yapışması; "
            "anne yaşından bağımsızdır ve ailesel kalıtılabilir. "
            "- **Mozaiklik (%1):** Postzigotik mitoz hatası. "
            "3. **Klinik Fenotip:** Düz yüz profili, epikantik kıvrımlar, yukarı çekik gözler, simian çizgisi (avuçta tek enine çizgi), "
            "hipotoni, zeka geriliği (IQ 25-50). "
            "4. **Kritik Tıbbi Riskler:** "
            "- Konjenital kalp defektleri (%40 - en sık **atriyoventriküler septal defekt - endokardiyal yastık defekti**). "
            "- Akut lösemi (ALL ve **Akut Megakaryoblastik Lösemi - AML M7**) riskinde 10-20 kat artış. "
            "- 40 yaş üstünde kaçınılmaz **Alzheimer benzeri nöropatoloji** (APP geni 21. kromozomdadır!)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Trizomi 21 (Down Sendromu) Sitogenetiği ve Riskleri",
                ["Parametre", "Biyolojik Karşılığı", "Patolojik Önemi"],
                [
                    ["En Sık Sitogenetik Neden", "Maternal Mayoz I ayrılamaması (%95)", "İleri anne yaşıyla doğrudan ilişkili sayısal anomali"],
                    [
                        "Kardiyak Malformasyon",
                        {"text": "Endokardiyal yastık defekti (AV septal defekt)", "isMasked": True, "hint": "Down sendromlu bebeklerin yüzde kırkında görülen majör doğumsal kalp anomalisi"},
                        "Erken kalp yetmezliği ve Eisenmenger riski"
                    ],
                    ["Hematolojik Malignite", "Akut Megakaryoblastik Lösemi (AML M7) ve ALL", "GATA1 mutasyonları eşliğinde lösemogenez"],
                    ["Nöropatolojik Risk", "Erken başlangıçlı Alzheimer hastalığı", "Amiloid prekürsör protein (APP) geninin 21. kromozomda 3 kopya olması"]
                ]
            ),
            make_active_recall(
                "Down sendromlu bireylerde kırk yaşından sonra neredeyse kaçınılmaz olarak nörofibriler yumaklar ve senil amiloid plaklarıyla seyreden nörodejeneratif hastalığın adı nedir?",
                "Alzheimer hastalığıdır.",
                "Yirmi birinci kromozomda yer alan amiloid prekürsör protein gen dozaj artışına bağlı demans"
            )
        ]
    })

    # Slayt 29: Checkpoint 3
    slides.append({
        "id": "k1-26-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Kistik Fibrozis Patofizyolojisi ve Sitogenetik",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 29,
        "narrative": (
            "Üçüncü bölüm kontrol noktamızda kistik fibrozis ve sitogenetik temelleri özetliyoruz: "
            "1. **CFTR Geni:** 7q31.2 lokusunda klorür/bikarbonat kanalı; en sık mutasyon ER katlanma kusuru yapan Delta-F508'dir (%70). "
            "2. **Doku Zıtlığı:** Solunumda klor sekresyonu durur, ENaC hiperaktifleşir, su emilir ve yapışkan mukus silyaları kilitler. "
            "Ter bezinde ise klor geri emilemez ve terde tuz fırlar (>60 mEq/L kesin tanı). "
            "3. **Akciğer:** Çocukta S. aureus; adolesan ve erişkinde mukoid Pseudomonas aeruginosa ve bronşiektazi. "
            "4. **Gastrointestinal:** Yenidoğanda mekonyum ileusu; pankreasta duktus tıkanması, kistik dilatasyon, atrofi ve steatore. "
            "5. **Üreme:** Erkeklerde bilateral vas deferens agenezisi (CBAVD) ile obstrüktif azospermi (%95). "
            "6. **Down Sendromu:** Trizomi 21 (maternal ayrılamama %95); AV septal defekt, megakaryoblastik lösemi (AML M7) ve erken Alzheimer."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s29-1",
                "Kistik fibrozis hastalarında ter bezlerinde lümenden klor ve sodyum geri emiliminin bozulmasıyla ortaya çıkan klasik tanısal laboratuvar bulgusu nedir?",
                "Yüksek klorürlü hipertonik terdir.",
                "Deri yüzeyinde salgılanan sıvıda iyon yoğunluğunun anormal artması",
                "Ter Testi"
            ),
            make_flashcard(
                "k1-26-fc-s29-2",
                "Kistik fibrozisli erişkin erkeklerin yüzde doksan beşinden fazlasında obstrüktif azospermi ve infertiliteye yol açan konjenital ürogenital anomali nedir?",
                "Bilateral vas deferens agenezisidir.",
                "Testislerden spermi üretraya taşıyan kanalların çift taraflı embriyolojik yokluğu",
                "CBAVD"
            ),
            make_flashcard(
                "k1-26-fc-s29-3",
                "İnsanlarda canlı doğumlarda en sık görülen kromozomal sayısal anomali ve zihinsel gerilik nedeni olan genetik sendrom nedir?",
                "Trizomi 21'dir (Down sendromu).",
                "Yirmi birinci otozomun maternal mayoz bölünmede ayrılamamasıyla oluşan fazlalık",
                "Sitogenetik"
            )
        ],
        "interactiveElements": [
            make_table(
                "Kistik Fibrozis ve Down Sendromu Karşılaştırma Matrisi",
                ["Hastalık", "Genetik Hata Tipi", "Altın Standart Tanı Yöntemi", "En Önemli Yaşam Tehdidi"],
                [
                    ["Kistik Fibrozis", "CFTR gen mutasyonu (7q31.2, OR)", "Ter testi (>60 mEq/L klorür)", "Pseudomonas bronşiektazisi ve solunum yetmezliği"],
                    [
                        "Down Sendromu",
                        "Trizomi 21 (sayısal anomali)",
                        {"text": "Karyotip analizi (47,XX,+21 veya 47,XY,+21)", "isMasked": True, "hint": "Kromozomların bantlama yöntemiyle sayı ve yapısının mikroskobik incelenmesi"},
                        "Konjenital AV septal defekt ve lösemi"
                    ]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi kistik fibrozis patofizyolojisinde solunum epitelinde gözlenen moleküler olaylar zincirini DOĞRU olarak açıklar?",
                {
                    "A": "CFTR'nin çalışmaması sonucu ENaC üzerindeki frenin kalkması, sodyum ve suyun hücre içine emilerek mukusun kuruması",
                    "B": "Hücre dışına kontrolsüz klor ve su pompalanması sonucu mukusun aşırı sulanması",
                    "C": "ENaC kanallarının mutasyonla tamamen yok olması ve sodyum emiliminin sıfırlanması",
                    "D": "Ter bezlerinde klorür geri emiliminin yüz kat artarak terin tamamen tuzsuz kalması",
                    "E": "Pankreas duktuslarında aşırı sıvı akışı ile enzimlerin seyreltilmesi"
                },
                "A",
                {
                    "A": "Doğrudur; CFTR kaybı ENaC frenini kaldırır, sodyum ve su lümenden emilir, mukus kurur ve silyalar kilitlenir.",
                    "B": "Yanlış; CFTR klor pompalamaz, su kurur.",
                    "C": "Yanlış; ENaC yok olmaz, aşırı aktifleşir.",
                    "D": "Yanlış; ter bezinde klor emilemez ve ter tuzlu olur.",
                    "E": "Yanlış; pankreasta salgı kurur ve tıkaç yapar."
                }
            )
        ]
    })

    # Slayt 30: Diğer Sitogenetik Sendromlar: Edwards, Patau, Turner ve Klinefelter
    slides.append({
        "id": "k1-26-s30",
        "title": "Diğer Sitogenetik Sendromlar: Edwards, Patau, Turner ve Klinefelter",
        "section": "Kistik Fibrozis ve Sitogenetik",
        "slideNumber": 30,
        "narrative": (
            "Down sendromunun ötesinde, klinikte sık karşılaşılan diğer majör sayısal kromozom anomalileri şunlardır: "
            "1. **Trizomi 18 (Edwards Sendromu - 47,+18):** "
            "- İkinci en sık otozomal trizomidir. Şiddetli zeka geriliği, mikrosefali, mikrognati, düşük kulaklar. "
            "- **Karakteristik Eller:** Parmakların birbiri üzerine binmesi (2. parmak 3'ün üzerine, 5. parmak 4'ün üzerine kilitlenir). "
            "- **Beşik Tabandaki Ayak (Rocker-bottom feet):** Tabanın dışbükey kavis alması. Çoğu ilk 1 yıl içinde kaybedilir. "
            "2. **Trizomi 13 (Patau Sendromu - 47,+13):** "
            "- Şiddetli orta hat gelişim defektleri: **Holoprozensefali**, mikzoftalmi/anoftalmi, yarık dudak/damak, **polidaktili** "
            "(fazla parmak) ve aplazia kutis (saçlı deride doku yokluğu). Çok ağır prognozludur. "
            "3. **Turner Sendromu (45,X):** "
            "- Kadınlarda tek X kromozomu; **çizgi gonadlar (streak gonads)**, primer amenore, boy kısalığı, **boyunda yelelenme (webbed neck)**, "
            "geniş kalkan göğüs ve **aort koarktasyonu** / biküspit aort kapağı. Zeka genellikle normaldir. "
            "4. **Klinefelter Sendromu (47,XXY):** "
            "- Erkeklerde fazladan X kromozomu; testiküler atrofi, seminifer tübül sklerozu, azospermi, uzun boy, jinekomasti ve "
            "artmış meme kanseri riski. Erkek hipogonadizminin en sık genetik nedenidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sayısal Kromozom Anomalileri Karşılaştırma Tablosu",
                ["Sendrom", "Karyotip Formülü", "Patognomonik / Karakteristik Bulgular", "Temel Prognoz"],
                [
                    ["Edwards Sendromu", "47,XX,+18 veya 47,XY,+18", "Üst üste binen parmaklar, beşik ayak, mikrognati", "Çoğu ilk 1 yaşta ölümcül"],
                    ["Patau Sendromu", "47,XX,+13 veya 47,XY,+13", "Holoprozensefali, polidaktili, yarık dudak/damak", "Ağır letal orta hat defektleri"],
                    [
                        "Turner Sendromu",
                        "45,X (veya mozaik)",
                        {"text": "Çizgi gonadlar, yele boyun, boy kısalığı, aort koarktasyonu", "isMasked": True, "hint": "Kadında tek X kromozomu ile giden amenore ve kardiyak vasküler darlık tablosu"},
                        "Primer amenore, normal zeka"
                    ],
                    ["Klinefelter Sendromu", "47,XXY", "Testis atrofisi, seminifer skleroz, jinekomasti, uzun boy", "Erkek hipogonadizmi ve azospermi"]
                ]
            ),
            make_active_recall(
                "Fizik muayenesinde boy kısalığı, boyunda yelelenme (webbed neck), geniş kalkan göğüs ve kardiyak incelemede aort koarktasyonu saptanan primer amenoreli bir kadında en olası sitogenetik tanı nedir?",
                "Turner sendromudur (45,X karyotipi).",
                "Dişi cinsiyet kromozomlarından birinin monozomisi ile karakterize sendrom"
            )
        ]
    })

    return slides
