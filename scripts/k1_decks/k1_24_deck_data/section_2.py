# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 2: Sistemik Tromboembolizm ve Paradoksal Emboli (Slayt 11 - 20)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # Slayt 11: Sistemik Tromboembolizm Tanımı ve Akış Yolu
    slides.append({
        "id": "k1-24-s11",
        "title": "Sistemik Tromboembolizm Tanımı, Akış Yolu ve Arteriyel Hedefler",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 11,
        "narrative": (
            "Sistemik tromboembolizm, arteriyel dolaşım ağında seyreden ve uç organlarda doku ölümüne yol açan tablodur: "
            "1. **Tanım ve Ayrım:** Pulmoner emboli venöz kaynaklı olup akciğer kapiller yatağında takılıp kalırken, "
            "sistemik emboli **arteriyel dolaşım içinde seyreder** ve vücudun tüm organlarına yayılabilir. "
            "2. **Köken Noktası:** Sistemik embolilerin ezici çoğunluğu **kalbin sol boşluklarından** kaynaklanır. "
            "Aort ve büyük arterler boyunca yüksek basınçlı akımla hızla distal dallara fırlar. "
            "3. **Klinik Sonuç:** Embolus çapına uygun bir arter lümenine ulaştığında tam tıkanma yapar. "
            "Gittiği dokuda kollateral dolaşım yetersizse sonuç **iskemik koagülatif nekroz (enfarktüs)** veya ekstremite gangrenidir. "
            "Enfarktüsün boyutu tıkalı damarın kalibresine ve dokunun hipoksi duyarlılığına göre değişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Sistemik tromboemboliler arteriyel dolaşım içinde seyrederek periferik organlarda uç arterleri tıkayıp iskemik nekroza yani enfarktüse yol açar.",
                "enfarktüse",
                "Arteriyel tıkanma sonucu gelişen iskemik doku ölümü alanı"
            ),
            make_table(
                "Pulmoner ve Sistemik Tromboembolizm Karşılaştırma Matrisi",
                ["Özellik", "Pulmoner Tromboembolizm (PTE)", "Sistemik Tromboembolizm"],
                [
                    ["Dolaşım Yolu", "Venöz dolaşım $\\rightarrow$ Sağ kalp $\\rightarrow$ Akciğer", "Arteriyel dolaşım $\\rightarrow$ Sol kalp $\\rightarrow$ Perifer"],
                    ["En Sık Kaynak", "Bacak derin venleri (DVT, >%95)", "Sol ventrikül ve sol atriyum trombüsleri (~%80)"],
                    [
                        "Temel Klinik Sonuç",
                        "Hipoksi, akut kor pulmonale, ani ölüm",
                        {"text": "Uç organ enfarktüsü (İnme, ekstremite iskemisi)", "isMasked": True, "hint": "Arteriyel beslenmenin kesilmesine bağlı doku nekrozu"}
                    ],
                    ["Enfarktüs Tipi", "Kırmızı (Hemorajik) kama enfarktüsü", "Beyaz (Anemik) enfarktüs (beyin ve bağırsak hariç)"]
                ]
            ),
            make_micro_quiz(
                "Dolaşım sistemi patolojisinde 'Sistemik Tromboembolizm' ile 'Pulmoner Tromboembolizm' arasındaki en temel fizyopatolojik ayrım hangisidir?",
                {
                    "A": "Sistemik embolinin arteriyel dolaşımda seyrederek periferik organ enfarktüslerine yol açması",
                    "B": "Sistemik embolinin yalnızca çocuklarda görülmesi",
                    "C": "Pulmoner embolinin daima sol ventrikülden kaynaklanması",
                    "D": "Sistemik embolilerin hiçbir zaman pıhtı içermemesi",
                    "E": "Pulmoner embolinin ekstremite gangreni yapması"
                },
                "A",
                {
                    "A": "Sistemik emboli arteriyel dolaşımda taşınır ve periferik organlarda enfarktüs oluşturur.",
                    "B": "Sistemik emboli her yaşta, özellikle ileri yaşta sıktır.",
                    "C": "Pulmoner emboli sol değil sağ kalpten geçer, venöz kökenlidir.",
                    "D": "Sistemik embolilerin %80'den fazlası pıhtıdır (mural trombüs).",
                    "E": "Ekstremite gangrenini sistemik arteriyel emboli yapar."
                }
            )
        ]
    })

    # Slayt 12: İntrakardiyak Mural Trombüsler: Sol Ventrikül Enfarktüsü
    slides.append({
        "id": "k1-24-s12",
        "title": "İntrakardiyak Mural Trombüsler: Sol Ventrikül Enfarktüsü ve Anevrizmalar",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 12,
        "narrative": (
            "Sistemik arteriyel embolilerin yaklaşık **%80'i kalbin iç yüzeyine yapışık intrakardiyak mural trombüslerden** kopar: "
            "1. **Sol Ventrikül Hâkimiyeti:** İntrakardiyak mural trombüslerin yaklaşık **üçte ikisi (%60 - 70)** sol ventrikülden kaynaklanır. "
            "2. **Miyokard Enfarktüsü (MI) Sonrası Zemin:** Geniş bir transmural anterior veya apikal MI geçiren hastalarda: "
            "- Nekrotik endokard subendotelyal kollajeni açığa çıkarır (**endotel hasarı**). "
            "- İskemik miyokard kasılamaz (akinezi/diskinezi), apeks bölgesinde kan göllenir (**staz**). "
            "- Bölgesel inflamasyon prokoagülan ortam yaratır (**hiperkoagülabilite**). "
            "Virchow triadının üç bileşeni de tamamlanır ve lümen içine doğru uzanan büyük mural trombüsler oluşur. "
            "3. **Ventrikül Anevrizması:** İyileşen miyokardın incelip keseleşmesi (kronik ventrikül anevrizması) pıhtı stazını kalıcı hale getirir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İntrakardiyak mural trombüslerin yaklaşık üçte ikisi sol ventrikül transmural miyokard enfarktüsü ve apeks anevrizması zemininde gelişir.",
                "sol ventrikül",
                "Miyokard enfarktüsü sonrası en sık mural trombüs barındıran kalp boşluğu"
            ),
            make_table(
                "Miyokard Enfarktüsü Sonrası Mural Trombüs Oluşum Basamakları",
                ["Virchow Faktörü", "Kardiyak Patoloji", "Tromboza Katkısı"],
                [
                    ["Endotel Hasarı", "Transmural nekrozun endokarda ulaşması", "Trombosit adezyonu ve intrensek yolak aktivasyonu"],
                    [
                        "Kan Akımı Stazı",
                        {"text": "Akinetik / Diskinetik enfarkt alanı ve anevrizma", "isMasked": True, "hint": "Kasılmayan miyokard duvarında kan göllenmesi"},
                        "Girdaplı akım ve eritrosit-fibrin agregasyonu"
                    ],
                    ["İnflamatuar Yanıt", "Nötrofil ve makrofaj sitokin salınımı", "Lokal doku faktörü artışı ve fibrinoliz inhibisyonu"]
                ]
            ),
            make_micro_quiz(
                "Ön duvar (anterior) miyokard enfarktüsü geçiren 58 yaşındaki bir hastada 2 hafta sonra sol bacakta ani gelişen soğukluk ve nabız kaybı saptanmıştır. Bu arteryel embolinin en olası intrakardiyak kaynağı hangisidir?",
                {
                    "A": "Sol ventrikül apeksindeki mural trombüs",
                    "B": "Sağ atriyum içi trabeküler pıhtı",
                    "C": "Triküspid kapak vejetasyonu",
                    "D": "Pulmoner kapak fibroelastomatozu",
                    "E": "Koroner sinüs endoteliti"
                },
                "A",
                {
                    "A": "Anterior MI sonrası sol ventrikül apeksinde akinetik alanda mural trombüs oluşur ve sistemik dolaşıma pıhtı atar.",
                    "B": "Sağ atriyum pıhtısı pulmoner emboli yapar.",
                    "C": "Triküspid kapağı akciğere emboli yollar.",
                    "D": "Pulmoner kapak sağ kalptedir.",
                    "E": "Koroner sinüs sağ atriyuma drene olur."
                }
            )
        ]
    })

    # Slayt 13: Sol Atriyal Trombüsler: Mitral Darlık ve Atriyal Fibrilasyon
    slides.append({
        "id": "k1-24-s13",
        "title": "Sol Atriyal Trombüsler: Mitral Darlık ve Atriyal Fibrilasyon",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 13,
        "narrative": (
            "İntrakardiyak sistemik embolilerin yaklaşık **dörtte biri (%20 - 25)** sol atriyum kaynaklıdır: "
            "1. **Mitral Kapak Darlığı (Stenozu):** Akut romatizmal ateş sekeli olarak kalınlaşıp daralan mitral kapak, "
            "sol atriyumun boşalmasını engeller. Sol atriyum aşırı derecede genişler (sol atriyal dilatasyon). "
            "2. **Atriyal Fibrilasyon (AF):** Sol atriyumun miyokard lifleri koordine kasılamaz, dakikada 300-400 mikroskobik fibrilasyon dalgasıyla titreşir. "
            "Kan atriyum içinde, özellikle de girintili çıkıntılı olan **Sol Atriyal Aurikula (Apendiks)** içinde tamamen durağanlaşır (staz). "
            "3. **Serbest / Küre Trombus (Ball Thrombus):** Bazen atriyum içinde serbest dolaşan dev bir küre pıhtı oluşur; "
            "bu kitle bir subap gibi mitral kapağın ağzını aniden kapatarak ani senkop ve ölüme yol açabilir veya parçalanıp beyne gider."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Mitral kapak darlığı ve atriyal fibrilasyonu olan hastalarda sistemik emboli kaynağı olan pıhtılar en sık sol atriyal aurikula içinde gelişir.",
                "sol atriyal aurikula",
                "Sol atriyumun staza en yatkın girintili kör cep anatomik bölgesi"
            ),
            make_table(
                "Sol Atriyal Trombüs Dinamikleri ve Emboli Riski",
                ["Patoloji Bileşeni", "Mekanik / Elektriksel Bozukluk", "Trombojenik Mekanizma"],
                [
                    ["Mitral Stenoz", "Kapak lümeninde daralma ve akım engeli", "Sol atriyum basınç artışı ve dev dilatasyon"],
                    [
                        "Atriyal Fibrilasyon",
                        "Atriyum kasılmasının kaybı (etkisiz titreme)",
                        {"text": "Apendiks içinde aşırı kan stazı", "isMasked": True, "hint": "Kör cepte akımsız göllenme ve pıhtı agregasyonu"}
                    ],
                    ["Ball Trombüs", "Atriyum kavitasyonunda serbest yüzen pıhtı", "Mitral orifis obstrüksiyonu veya sistemik embolizasyon"]
                ]
            ),
            make_micro_quiz(
                "Romatizmal mitral kapak stenozu ve kronik atriyal fibrilasyonu olan bir hastada gelişen iskemik inmenin (serebral enfarktüs) patolojik kökeni araştırıldığında, trombüsün en olası birincil yerleşim yeri hangisidir?",
                {
                    "A": "Sol atriyal apendiks (aurikula)",
                    "B": "Sağ ventrikül trabekülası",
                    "C": "Pulmoner ven kökü",
                    "D": "Sinüs venozus kapağı",
                    "E": "Ductus arteriosus artığı"
                },
                "A",
                {
                    "A": "Atriyal fibrilasyonda kan stazı en belirgin sol atriyal apendikste olur ve sistemik emboli buradan fırlar.",
                    "B": "Sağ ventrikül pulmoner dolaşıma emboli atar.",
                    "C": "Pulmoner ven pıhtı odağı değildir.",
                    "D": "Sinüs venozus sağ atriyum yapısıdır.",
                    "E": "Duktus arteriosus aort-pulmoner arter bağıdır."
                }
            )
        ]
    })

    # Slayt 14: Aterosklerotik Plak Ülserasyonu ve Aort Anevrizmaları
    slides.append({
        "id": "k1-24-s14",
        "title": "Aort Kaynaklı Emboliler: Ülserleşmiş Plaklar ve Anevrizmalar",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 14,
        "narrative": (
            "Kalp dışındaki büyük arteriyel damarlar da sistemik embolilerin önemli bir bölümünü oluşturur: "
            "1. **Komplike Aterosklerotik Plak Ülserasyonu:** "
            "Aort ve ana dallarındaki ileri evre aterom plaklarının fibröz başlığı yırtıldığında (ülserasyon), "
            "plağın altındaki yumuşak lipid zengin nekrotik çekirdek kan akımına maruz kalır. "
            "Plak yüzeyinde hem taze trombüsler oluşarak embolize olur hem de serbest kolesterol kristalleri çevreye saçılır. "
            "2. **Aterom / Kolesterol Embolisi:** Çapı küçük kolesterol yarıkları böbrek, pankreas ve parmak uçlarındaki mikrodamarları tıkar "
            "(mor parmak / blue toe sendromu). Biyopside damar lümeninde iğsi kolesterol yarıkları karakteristiktir. "
            "3. **Abdominal Aort Anevrizması (AAA):** Aort lümeninin balonlaşması sonucu kan akımı türbülansa uğrar; "
            "anevrizma kesesi içinde soğan zarı gibi tabakalanmış lamine trombüsler (Zahn çizgileri) oluşur. "
            "Bu pıhtıların kopmasıyla her iki bacağa masif emboliler atılır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Aort aterom plağının yırtılmasıyla mikrodamarları tıkayan kolesterol embolisinde doku biyopsisinde damar lümeni içinde iğsi kolesterol kristalleri yarıkları izlenir.",
                "iğsi kolesterol kristalleri",
                "Kolesterol kleftlerinin histopatolojik morfolojik şekli"
            ),
            make_table(
                "Aort Kaynaklı Embolizasyon Mekanizmaları",
                ["Aortik Patoloji", "Embolize Olan Materyal", "Hedef Damar Çapı", "Klinik Tablo"],
                [
                    [
                        "Abdominal Aort Anevrizması",
                        "Lamine mural trombüs kitleleri",
                        "Geniş çaplı arterler (İliak, Femoral)",
                        {"text": "Akut bacak iskemisi ve 6P tablosu", "isMasked": True, "hint": "Geniş pıhtı tıkanmasına bağlı ekstremite iskemisi"}
                    ],
                    ["Ülseröz Aterom Plağı", "Kolesterol kristalleri ve mikro-debris", "Arteriyol ve kapillerler", "Böbrek yetmezliği, mavi parmak (blue toe)"]
                ]
            ),
            make_micro_quiz(
                "Koroner anjiyografi yapılan 72 yaşındaki aterosklerotik bir hastada işlemden 2 gün sonra ayak parmaklarında morarma (blue toe sendromu) ve akut böbrek yetmezliği gelişmiştir. Böbrek biyopsisinde arkuat arter lümeninde saptanması beklenen patognomonik lezyon hangisidir?",
                {
                    "A": "Bikonveks iğsi kolesterol kristalleri yarıkları",
                    "B": "Kazeifiye granülom odakları",
                    "C": "Fetal skuamöz epitel adacıkları",
                    "D": "Kemik iliği yağ vakuolleri",
                    "E": "Aspergillus mantar hifleri"
                },
                "A",
                {
                    "A": "Aterom plağının kateterle zedelenmesi kolesterol kristal embolizasyonuna yol açar; lümende iğsi kolesterol yarıkları görülür.",
                    "B": "Granülom tüberküloz lezyonudur.",
                    "C": "Fetal skuamöz hücre amniyon sıvısı embolisidir.",
                    "D": "Kemik kırığında yağ embolisidir.",
                    "E": "Aspergillus mantar enfeksiyonudur."
                }
            )
        ]
    })

    # Slayt 15: Kalp Kapak Lezyonları ve Vejetasyonlar
    slides.append({
        "id": "k1-24-s15",
        "title": "Kalp Kapak Vejetasyonları: İnfektif ve Non-Bakteriyel Endokardit",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 15,
        "narrative": (
            "Kalp kapaklarında oluşan kitleler (vejetasyonlar), sistemik arteriyel embolizasyonun en tehlikeli kaynaklarıdır: "
            "1. **İnfektif Endokardit (İE):** "
            "Bakteriyel (Staphylococcus aureus, Streptococcus viridans) veya fungal mikroorganizmalar kapak endoteline tutunur. "
            "Oluşan vejetasyonlar **büyük, düzensiz, son derece kırılgan ve mikrop doludur**. "
            "Bu kitlelerden kopan parçalar sistemik dolaşıma yayılarak hem iskemik enfarktüs yapar hem de dokularda metastatik apselere yol açar (**Septik Emboli**). "
            "2. **Non-Bakteriyel Trombotik Endokardit (NBTE / Marantik Endokardit):** "
            "İleri evre kanser (müsinöz adenokarsinomlar) veya ağır sepsis zemininde kapak kapanma çizgilerinde **steril, küçük ve tahribatsız fibrin pıhtıları** birikir. "
            "Sterildir fakat kolayca kopup beyin veya böbreğe embolize olur. "
            "3. **Libman-Sacks Endokarditi:** Sistemik Lupus Eritematozus (SLE) hastalarında kapakların her iki yüzünde küçük steril vejetasyonlar gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İnfektif endokardit vejetasyonlarından kopan parçalar canlı mikroorganizmalar taşıdığından gittikleri organlarda septik enfarktüs ve metastatik apse odakları oluşturur.",
                "septik enfarktüs",
                "Canlı bakteriler içeren enfekte emboli doku nekrozu"
            ),
            make_table(
                "Kalp Kapak Vejetasyon Tipleri ve Embolik Karakteristikleri",
                ["Vejetasyon Türü", "Mikrobiyolojik İçerik", "Makroskobik Özellik", "Embolizasyon Niteliği"],
                [
                    ["İnfektif Endokardit", "Bakteri / Mantar kolonileri", "Büyük, kırılgan, kapak destruksiyonu var", "Septik emboli ve metastatik apseler"],
                    [
                        "Marantik Endokardit (NBTE)",
                        "Tamamen sterildir (mikrop içermez)",
                        {"text": "Kapanma çizgisinde küçük, tahribatsız pıhtılar", "isMasked": True, "hint": "Kanser zemininde steril fibrin birikintileri"},
                        "Aseptik iskemik organ enfarktüsleri"
                    ],
                    ["Libman-Sacks Endokarditi", "Steril, immün kompleks ilişkili", "Kapağın hem ön hem arka yüzünde küçük nodüller", "Orta dereceli emboli riski"]
                ]
            ),
            make_micro_quiz(
                "İntravenöz madde bağımlılığı olan bir hastada aort kapağında Staphylococcus aureus üreyen kırılgan vejetasyonlar saptanmıştır. Bu hastanın dalağında gelişen kama şekilli enfarktüs alanında patolojik olarak hangisinin gelişmesi beklenir?",
                {
                    "A": "Bakteriyel kolonizasyon ve septik apse formasyonu",
                    "B": "Aseptik kireçlenme ve taşlaşma",
                    "C": "Primer kazeifikasyon nekrozu",
                    "D": "Fibrinoid damar duvarı nekrozu",
                    "E": "Yağ nekrozu ve sabunlaşma"
                },
                "A",
                {
                    "A": "İnfektif endokardit embolileri bakteri taşır (septik emboli); enfarkt alanında süpürasyon ve apse gelişir.",
                    "B": "Kireçlenme kronik süreçtir.",
                    "C": "Kazeifikasyon tüberkülozda görülür.",
                    "D": "Fibrinoid nekroz immün vaskülit ve malign hipertansiyondadır.",
                    "E": "Yağ nekrozu pankreatit ve travmada görülür."
                }
            )
        ]
    })

    # Slayt 16: Paradoksal Emboli Patofizyolojisi: Sağdan Sola Şantlar
    slides.append({
        "id": "k1-24-s16",
        "title": "Paradoksal Emboli Patofizyolojisi: Sağdan Sola Şant Mekanizması",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 16,
        "narrative": (
            "Dolaşım fizyolojisinin normal kurallarını bozan en çarpıcı emboli türü Paradoksal Embolidir: "
            "1. **Paradoksal Emboli Tanımı:** Sistemik venöz dolaşımdan (DVT) kopan bir pıhtının, "
            "akciğer kapiller filtresine gitmek yerine, **intrakardiyak veya intrapulmoner bir defektten geçerek sol kalbe ulaşması** "
            "ve sistemik arteriyel yatağa fırlatılmasıdır. "
            "2. **Anatomik Zemin (Şantlar):** "
            "- **Patent Foramen Ovale (PFO):** En sık nedendir! Erişkin popülasyonun yaklaşık **%25'inde foramen ovale fonksiyonel olarak kapalı fakat anatomik olarak açıktır (prob patent)**. "
            "- **Atriyal Septal Defekt (ASD)** veya Ventriküler Septal Defekt (VSD). "
            "- Pulmoner arteriyovenöz malformasyonlar (AVM). "
            "3. **Basınç Tersine Dönüşü (Sağdan Sola Geçiş):** Normalde sol atriyum basıncı sağdan yüksektir. "
            "Ancak masif pulmoner emboli, şiddetli öksürük veya Valsalva manevrası (ıkınma) sağ atriyum basıncını sol atriyumun üzerine çıkardığında, "
            "PFO kapağı açılır; venöz pıhtı doğrudan sol atriyuma geçer ve beyne giderek **genç bir hastada kriptojenik inmeye** yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Venöz dolaşımda oluşan bir trombüsün Patent Foramen Ovale veya ASD üzerinden sol kalbe geçerek sistemik arterleri tıkaması olayına paradoksal emboli denir.",
                "paradoksal emboli",
                "Sağdan sola kardiyak defekt yoluyla arteriyel sisteme geçen çapraz emboli"
            ),
            make_causal_chain(
                "Paradoksal Emboli ile İskemik İnme Gelişim Zinciri",
                [
                    "1. Venöz Pıhtı: Bacak derin veninde immobilizasyona bağlı DVT oluşumu",
                    "2. Akciğer Mikroembolisi: Pıhtı parçalarının sağ kalbe gelip pulmoner vasküler direnci artırması",
                    "3. Sağ Atriyal Basınç Artışı: Direnç nedeniyle sağ atriyum basıncının sol atriyum basıncını aşması",
                    "4. Şant Açılması: Basınç farkıyla Patent Foramen Ovale kapağının açılarak sağdan sola geçit vermesi",
                    "5. Serebral Tıkanma: Pıhtının sol ventrikülden aorta ve karotis yoluyla beyne gidip inme yapması"
                ]
            ),
            make_micro_quiz(
                "Yirmi sekiz yaşında bilinen hiçbir kardiyovasküler hastalığı olmayan bir kadında uzun bir otobüs yolculuğu sonrasında bacakta ağrı ve ardından aniden sağ tarafında felç (inme) gelişmiştir. Ekokardiyografide bu patolojiyi açıklayan en olası konjenital defekt hangisidir?",
                {
                    "A": "Patent Foramen Ovale (Sağdan sola geçişli paradoksal emboli)",
                    "B": "Aort koarktasyonu",
                    "C": "Bikuspit aort kapağı",
                    "D": "Mitral kapak prolapsusu",
                    "E": "Sol ventrikül hipertrofisi"
                },
                "A",
                {
                    "A": "DVT sonrası genç hastada inme gelişmesi PFO üzerinden gerçekleşen paradoksal embolinin tipik klinik tablosudur.",
                    "B": "Koarktasyon üst ekstremitede hipertansiyon yapar.",
                    "C": "Bikuspit aort kapak stenozuna eğilim yaratır.",
                    "D": "Mitral prolapsus geç sistolik üfürüm yapar, şant oluşturmaz.",
                    "E": "Hipertrofi bir şant defekti değildir."
                }
            )
        ]
    })

    # Slayt 17: Sistemik Embolinin Hedef Organ Dağılımı
    slides.append({
        "id": "k1-24-s17",
        "title": "Sistemik Embolinin Hedef Organ Dağılımı: Bacaklar, Beyin ve Visseral Organlar",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 17,
        "narrative": (
            "Sol kalpten veya aorttan fırlayan sistemik embolusların yerleştiği anatomik hedefler kan akımının debisine göre dağılır: "
            "1. **Alt Ekstremiteler (%75):** Sistemik embolilerin ezici çoğunluğu **bacak arterlerine** gider: "
            "- Arteria femoralis ve bifurkasyonu "
            "- Arteria poplitea "
            "- Tibial arterler "
            "Hastada ani başlayan şiddetli bacak ağrısı, soğukluk, solukluk ve nabız kaybı (akut bacak iskemisi) gelişir. "
            "2. **Beyin (%10):** Aort arkından karotis arterlere yönelen pıhtılar özellikle **Orta Serebral Arter (MCA)** dallarını tıkar; "
            "akut iskemik inme, afazi ve hemiplejiye yol açar. "
            "3. **Mezenterik Dolaşım:** Arteria mesenterica superior tıkanması akut mezenterik iskemi ve bağırsak gangreni yapar; mortalitesi çok yüksektir. "
            "4. **Böbrekler ve Dalak:** Uç arter yapısındaki renal ve splenik arterlerin tıkanmasıyla sınırları keskin **soluk kama enfarktüsleri** oluşur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Sistemik arteriyel embolizasyonların yaklaşık yüzde yetmiş beşi alt ekstremite arterlerini tutarak akut bacak iskemisine yol açar.",
                "yüzde yetmiş beşi",
                "Sistemik embolinin alt ekstremite arterlerini tutma oranı"
            ),
            make_table(
                "Sistemik Emboli Hedef Organ Dağılımı ve Klinik Bulgular",
                ["Hedef Anatomik Bölge", "Görülme Oranı", "Tıkanan Damarlar", "Klasik Klinik Belirti"],
                [
                    [
                        "Alt Ekstremiteler",
                        "%70 - 75 (En sık)",
                        "A. Femoralis, A. Poplitea",
                        {"text": "Akut bacak iskemisi ve 6P tablosu", "isMasked": True, "hint": "Ağrı, solukluk ve nabız kaybıyla seyreden akut ekstremite tablosu"}
                    ],
                    ["Santral Sinir Sistemi", "~%10", "A. Cerebri Media (MCA)", "Akut iskemik inme, afazi, hemipleji"],
                    ["Gastrointestinal Sistem", "~%3 - 5", "A. Mesenterica Superior", "Şiddetli orantısız karın ağrısı, bağırsak nekrozu"],
                    ["Böbrekler", "~%5", "Arkuat ve interlobar arterler", "Yan ağrısı, hematüri, beyaz kortikal enfarkt"],
                    ["Dalak", "~%3", "Splenik arter dalları", "Sol üst kadran ağrısı, plevritik sürtünme"]
                ]
            ),
            make_micro_quiz(
                "Sistemik tromboemboli olgularında embolusların arteriyel dolaşımda en yüksek sıklıkla (%70-75) yerleştiği anatomik hedef bölge hangisidir?",
                {
                    "A": "Alt ekstremite arterleri (Femoral / Popliteal)",
                    "B": "Koroner arterler",
                    "C": "Çölyak trunkus",
                    "D": "Retinal santral arter",
                    "E": "Üst ekstremite aksiller arter"
                },
                "A",
                {
                    "A": "Sistemik embolilerin yaklaşık %75'i alt ekstremite arterlerine oturur.",
                    "B": "Koroner emboliler nadirdir (<%2).",
                    "C": "Çölyak arter geniş açılıdır, mezenterik arter kadar sık tutulmaz.",
                    "D": "Retinal arter mikroemboli alanıdır, oran olarak düşüktür.",
                    "E": "Üst ekstremite tutulumu <%10'dur."
                }
            )
        ]
    })

    # Slayt 18: Akut Ekstremite İskemisi: 6P Kuralı
    slides.append({
        "id": "k1-24-s18",
        "title": "Akut Ekstremite İskemisi: Tanısal '6P Kuralı' ve Doku Canlılığı",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 18,
        "narrative": (
            "Alt ekstremite ana arterinin embolusla aniden tıkanması, dakikalar içinde müdahale gerektiren cerrahi bir acildir: "
            "1. **Klasik '6P Belirtileri' (İngilizce Akronim):** "
            "- **Pain (Ağrı):** Ani başlayan, dayanılmaz şiddette iskemik ağrı (ilk ve en sabit bulgudur). "
            "- **Pallor (Solukluk):** Kan akımının kesilmesiyle bacak mermer gibi beyazlaşır, kılcal dolum kaybolur. "
            "- **Pulselessness (Nabızsızlık):** Tıkanıklık seviyesinin distalindeki arteriyel nabızlar (femoral, popliteal, dorsalis pedis) tamamen kaybolur. "
            "- **Paresthesia (Uyuşma / Hipoestezi):** İskemiye en duyarlı dokulardan olan periferik sinirlerin beslenememesiyle duyu kaybı başlar. "
            "- **Paralysis (Kuvvet Kaybı / Felç):** İskelet kaslarının iskemik nekroza girmesiyle parmak ve ayak hareketleri durur (kötü prognoz!). "
            "- **Poikilothermia (Soğukluk):** Bacak ortam sıcaklığına kadar soğur (buz gibi olur). "
            "2. **Zaman Penceresi:** İlk 6 saat içinde cerrahi embolektomi (Fogarty kateteri) yapılmazsa ekstremite kuru gangrene gider ve ampute edilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Akut arteriyel ekstremite iskemisinde iskelet kası nekrozuna bağlı paralizi yani hareket kaybı gelişmesi irreversibl doku hasarının ve kötü prognozun en kritik işaretidir.",
                "paralizi",
                "Akut iskemide kas ölümü ve kalıcı felç tablosunu belirten 6P bulgusu"
            ),
            make_table(
                "Akut Ekstremite İskemisinde 6P Bulguları ve Anlamları",
                ["Bulgu Adı", "Klinik Özellik", "Patofizyolojik Düzey"],
                [
                    ["Pain (Ağrı)", "Ani başlayan şiddetli iskemik kas ağrısı", "Anaerobik metabolizma ve laktik asit uyarısı"],
                    ["Pallor (Solukluk)", "Mermer beyazı soluk cilt", "Mikrovasküler kapiller perfüzyonun durması"],
                    [
                        "Pulselessness (Nabızsızlık)",
                        {"text": "Tıkanıklık distalinde nabız alınamaması", "isMasked": True, "hint": "Arteriyel pulsasyon dalgasının tamamen kaybolması"},
                        "Lümenin embolusla tam obstrüksiyonu"
                    ],
                    ["Paresthesia (Uyuşma)", "Karıncalanma, duyu kaybı", "Periferik duyu siniri hipoksisi"],
                    ["Paralysis (Felç)", "Parmak ve ayak hareket kaybı", "İskelet kası ve motor nöron ölümü (alarm bulgusu)"],
                    ["Poikilothermia (Soğukluk)", "Buz gibi soğuk ekstremite", "Arteriyel ısı transferinin kesilmesi"]
                ]
            ),
            make_micro_quiz(
                "Atriyal fibrilasyonu olan 70 yaşındaki bir hastada sağ bacakta aniden başlayan şiddetli ağrı, solukluk, soğukluk, distal nabızların alınamaması ve ayak parmaklarında kuvvet kaybı (hareket edememe) saptanmıştır. Bu klinik durumdaki 6P bulgularından hangisi kas liflerinin geri dönüşsüz nekroza girmeye başladığını gösteren en ağır prognostik göstergedir?",
                {
                    "A": "Paralizi (Paralysis / Kuvvet Kaybı)",
                    "B": "Ağrı (Pain)",
                    "C": "Solukluk (Pallor)",
                    "D": "Soğukluk (Poikilothermia)",
                    "E": "Parestazi (Paresthesia)"
                },
                "A",
                {
                    "A": "Paralizi (hareket kaybı) iskelet kasının iskemik nekrozunu gösterir; acil reaskülarizasyon yapılmazsa amputasyon kaçınılmazdır.",
                    "B": "Ağrı ilk ve erken bulgudur, doku henüz canlıdır.",
                    "C": "Solukluk akım kesintisini gösterir, nekroz kanıtı değildir.",
                    "D": "Soğukluk erken fiziksel değişimdir.",
                    "E": "Parestazi sinir iskemisini gösterir ancak paraliziden önce görülür."
                }
            )
        ]
    })

    # Slayt 19: [TEKRAR SAYFASI - CHECKPOINT 2] Sistemik Tromboembolizm ve Paradoksal Emboli Dinamikleri
    slides.append({
        "id": "k1-24-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Sistemik Tromboembolizm ve Paradoksal Emboli Dinamikleri",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 19,
        "narrative": (
            "Bu ikinci checkpoint sayfasında, sistemik tromboembolizm ve paradoksal emboli dinamiklerini pekiştiriyoruz: "
            "1. **Sistemik Emboli Kökeni:** %80'i intrakardiyak mural trombüslerden (2/3 sol ventrikül MI sonrası, 1/4 sol atriyal fibrilasyon) kaynaklanır. "
            "2. **Aort Kaynakları:** Ülserleşmiş aterom plakları (kolesterol embolisi) ve abdominal aort anevrizması (lamine trombüsler). "
            "3. **Kapak Vejetasyonları:** İnfektif endokardit (mikroplu septik emboli/apse) ve marantik endokardit (kanser ilişkili steril fibrin pıhtıları). "
            "4. **Paradoksal Emboli:** Venöz DVT pıhtısının PFO veya ASD gibi sağdan sola şantlarla sol kalbe geçip arteriyel inme yapmasıdır. "
            "5. **Hedef Dağılımı:** En sık ALT EKSTREMİTELER (%75), ardından BEYİN (%10), mezenterik damarlar, böbrek ve dalaktır. "
            "6. **Akut Ekstremite İskemisi:** 6P Kuralı: Pain, Pallor, Pulselessness, Paresthesia, Paralysis, Poikilothermia. "
            "İlk 6 saatte embolektomi yapılmazsa kuru gangren ve amputasyon gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s19-1",
                "Sistemik arteriyel tromboembolilerin yaklaşık yüzde sekseninin kaynaklandığı primer anatomik yapı nedir?",
                "Sol ventrikül ve atriyum içi mural trombüslerdir.",
                "Miyokard enfarktüsü veya mitral darlık zemininde kardiyak kavitelerde oluşan pıhtılar",
                "Sistemik Emboli Kaynakları"
            ),
            make_flashcard(
                "k1-24-fc-s19-2",
                "Bacak derin venlerinde oluşan bir pıhtının Patent Foramen Ovale üzerinden sol kalbe geçerek beyin arterlerini tıkaması olayına ne ad verilir?",
                "Paradoksal emboli tablosudur.",
                "Venöz sistemden arteriyel sisteme anormal şant geçişi terimi",
                "Paradoksal Emboli"
            ),
            make_flashcard(
                "k1-24-fc-s19-3",
                "Sistemik arteriyel tromboembolilerin klinik pratikte yaklaşık yüzde yetmiş beş oranında en sık tıkadığı anatomik hedef bölge neresidir?",
                "Alt ekstremite arter yatağıdır.",
                "Femoral ve popliteal bacak atardamarları lokasyonu",
                "Hedef Organlar"
            )
        ],
        "interactiveElements": [
            make_table(
                "Sistemik Emboli Kaynakları ve Temsilci Klinik Tablolar",
                ["Kardiyovasküler Kaynak", "Temel Etyolojik Hastalık", "Emboli Materyali"],
                [
                    ["Sol Ventrikül (%60-70)", "Akut transmural MI, ventrikül apeks anevrizması", "Geniş mural pıhtı kitlesi"],
                    ["Sol Atriyum (%20-25)", "Mitral darlığı, kronik atriyal fibrilasyon", "Apendiks içinde organize trombüs"],
                    [
                        "Aortik Kaynaklar",
                        "İleri ateroskleroz, abdominal aort anevrizması",
                        {"text": "Aterom plağı debrisleri ve lamine trombüsler", "isMasked": True, "hint": "Kolesterol kleftleri ve damar içi pıhtı tabakaları"}
                    ],
                    ["Kapak Vejetasyonları", "Bakteriyel endokardit, marantik endokardit", "Septik veya aseptik fibrin yığınları"]
                ]
            ),
            make_micro_quiz(
                "Sistemik tromboembolizm patolojisinde aşağıdakilerden hangisi bir 'Paradoksal Emboli' mekanizmasını açıklar?",
                {
                    "A": "Vena saphena magnadaki pıhtının atriyal septal defekt yoluyla sol atriyuma geçip serebral arteri tıkaması",
                    "B": "Sol ventrikül apeksindeki mural trombüsün renal arteri tıkaması",
                    "C": "Aort anevrizmasındaki trombüsün femoral arteri tıkaması",
                    "D": "Mitral vejetasyonun dalak arterini tıkaması",
                    "E": "Femoral ven trombüsünün pulmoner arter bifurkasyonuna oturması"
                },
                "A",
                {
                    "A": "Venöz sistemden gelen pıhtının ASD/PFO ile arteriyel sisteme atlaması paradoksal embolidir.",
                    "B": "Sol ventrikülden böbreğe gidiş klasik sistemik embolidir.",
                    "C": "Aorttan femorale gidiş direkt arteriyel embolidir.",
                    "D": "Mitralden dalağa gidiş klasik sistemik embolidir.",
                    "E": "Femoral venden pulmoner artere gidiş klasik pulmoner tromboembolizmdir."
                }
            )
        ]
    })

    # Slayt 20: Bölüm Özeti: Tromboembolilerden Non-Trombotik Özel Emboli Tiplerine Geçiş
    slides.append({
        "id": "k1-24-s20",
        "title": "Bölüm Özeti: Tromboembolilerden Non-Trombotik Özel Emboli Tiplerine Geçiş",
        "section": "Sistemik Tromboembolizm ve Paradoksal Emboli",
        "slideNumber": 20,
        "narrative": (
            "Sistemik ve paradoksal emboli mekanizmalarını tamamlarken şu klinik gerçekleri netleştiriyoruz: "
            "1. **Mural Trombüs Yönetimi:** Kalp boşluklarında oluşan pıhtıların erken tespiti ve antikoagülasyonu, "
            "hastayı kalıcı felçten (inme) ve bacak amputasyonundan korur. "
            "2. **PFO Her 4 Kişiden Birinde Vardır:** Genç bir hastada açıklanamayan inme görüldüğünde DVT ve PFO mutlaka araştırılmalıdır. "
            "3. **6P Kuralı Zamana Karşı Yarıştır:** İskelet kası 6 saatten fazla iskemiye dayanamaz. "
            "4. **Sonraki Bölüme Köprü:** Buraya kadar pıhtı kökenli (tromboemboli) kitleleri inceledik. "
            "Bir sonraki bölümümüzde pıhtı harici oluşan, dramatik klinik tablolara yol açan "
            "'Özel Emboli Tipleri I: Yağ Embolisi ve Amniyon Sıvısı Embolisi' patolojilerini ele alacağız."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Toplumda her dört kişiden birinde anatomik olarak açık bulunan patent foramen ovale defekti genç yaştaki kriptojenik inmelerin en önemli paradoksal emboli zeminidir.",
                "patent foramen ovale",
                "Erişkinlerde sık görülen sağdan sola şant oluşturan atriyal açıklık"
            ),
            make_active_recall(
                "Akut alt ekstremite arter embolisinde cerrahi olarak pıhtının çıkarılması ve damarın açılması amacıyla kullanılan balonlu özel kateterin tıbbi adı nedir?",
                "Fogarty embolektomi kateteridir.",
                "Vasküler cerrahide pıhtıyı çekip çıkaran balonlu cihaz"
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi bir hastada gelişen sistemik arteriyel embolinin kaynağının intrakardiyak bir patoloji olduğunu düşündüren en güçlü klinik kanıttır?",
                {
                    "A": "Ekokardiyografide sol ventrikül apeksinde transmural MI zemininde hareketli kitle saptanması",
                    "B": "Hastanın bacak yüzeyel venlerinde variköz genişlemeler olması",
                    "C": "Hastanın sigara içiyor olması",
                    "D": "Hastada hafif anemi bulunması",
                    "E": "Karaciğer enzimlerinin hafif yüksek seyretmesi"
                },
                "A",
                {
                    "A": "Sol ventrikül apeksindeki hareketli kitle intrakardiyak mural trombüstür ve sistemik embolinin primer kaynağıdır.",
                    "B": "Varisler yüzeyel venöz hastalıktır, sistemik emboli yapmaz.",
                    "C": "Sigara risk faktörüdür ancak spesifik pıhtı kaynağı kanıtı değildir.",
                    "D": "Anemi kardiyak kitle kanıtı değildir.",
                    "E": "Karaciğer enzimleri emboli odağını göstermez."
                }
            )
        ]
    })

    return slides
