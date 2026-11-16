# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 3: Özel Emboli Tipleri I: Yağ Embolisi ve Amniyon Sıvısı Embolisi (Slayt 21 - 30)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # Slayt 21: Non-Trombotik Embolilere Genel Bakış
    slides.append({
        "id": "k1-24-s21",
        "title": "Non-Trombotik Embolilere Genel Bakış: Biyolojik Çeşitlilik",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 21,
        "narrative": (
            "Klinik embolilerin %99'u kan pıhtısı parçalarından oluşsa da, pıhtı harici maddelerin damar lümenini tıkamasıyla gelişen non-trombotik emboliler son derece ölümcüldür: "
            "1. **Biyolojik Kaynaklar:** "
            "- **Yağ Embolisi:** Kemik iliği veya yumuşak doku lipidleri. "
            "- **Amniyon Sıvısı Embolisi:** Fetal döküntüler ve plasental sıvılar. "
            "- **Hava ve Gaz Embolisi:** Atmosferik hava veya kanda çözünmüş azot gazı kabarcıkları. "
            "- **Tümör Embolisi:** Malign neoplazmların damar invazyonu yaparak metastaz oluşturması. "
            "- **Aterom / Kolesterol Embolisi:** Yırtılan aterosklerotik plak kristalleri. "
            "- **Kemik İliği Embolisi:** Kardiyopulmoner resüsitasyon (CPR) sırasında kırılan kaburgalardan kemik iliği elemanlarının venlere geçmesi. "
            "2. **Önemi:** Bu emboliler yalnızca mekanik tıkanma yapmakla kalmaz; toksik, immünolojik veya koagülasyonu tetikleyen sistemik sendromlar başlatır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Kardiyopulmoner resüsitasyon sırasında sternum ve kosta kırıklarına bağlı olarak akciğer damarlarında hematopoetik hücreler ve yağ dokusu içeren kemik iliği embolisi görülebilir.",
                "kemik iliği embolisi",
                "CPR travması sonrası kemik iliği elemanlarının pulmoner dolaşıma geçmesi"
            ),
            make_table(
                "Non-Trombotik Emboli Türleri ve Morfolojik Özellikleri",
                ["Emboli Türü", "Tipik Etyolojik Neden", "Tanısal Histopatolojik Belirteç"],
                [
                    ["Yağ Embolisi", "Uzun kemik (femur) kırıkları", "Lipid damlacıkları (Oil Red O pozitif)"],
                    [
                        "Amniyon Sıvısı Embolisi",
                        "Zor doğum, plasenta dekolmanı",
                        {"text": "Fetal skuamöz hücreler ve lanugo tüyleri", "isMasked": True, "hint": "Anne pulmoner damarlarında bebeğe ait epitel ve kıllar"}
                    ],
                    ["Gaz / Hava Embolisi", "Boyun cerrahisi, derin dalış", "Damarlarda hava kabarcıkları, köpüklü kan"],
                    ["Kemik İliği Embolisi", "CPR kosta kırıkları", "Hematopoetik adacıklar ve yağ hücreleri"]
                ]
            ),
            make_micro_quiz(
                "Kalp masajı (CPR) uygulanarak resüsite edilen ancak kurtarılamayan yaşlı bir hastanın otopsisinde, pulmoner arter dalları içinde yağ vakuolleri ile birlikte eritroid ve miyeloid hematopoetik hücre kordonları izlenmiştir. Bu lezyonun tanısı hangisidir?",
                {
                    "A": "Kemik İliği Embolisi",
                    "B": "Amniyon Sıvısı Embolisi",
                    "C": "Saf Kolesterol Kristal Embolisi",
                    "D": "Mural Ventrikül Trombüsü",
                    "E": "Tümör Hücre Agregatı"
                },
                "A",
                {
                    "A": "Kaburga kırıkları sonrası pulmoner damarlarda hematopoetik hücre ve yağ adacıklarının görülmesi kemik iliği embolisidir.",
                    "B": "Amniyon sıvısı fetal hücre içerir.",
                    "C": "Kolesterol kleftleri ateromda olur.",
                    "D": "Mural trombüs fibrin ve eritrosit pıhtısıdır, kemik iliği içermez.",
                    "E": "Tümör embolisinde malign atipik hücreler vardır."
                }
            )
        ]
    })

    # Slayt 22: Yağ Embolisi Etyolojisi: Uzun Kemik Kırıkları
    slides.append({
        "id": "k1-24-s22",
        "title": "Yağ Embolisi Etyolojisi: Uzun Kemik Kırıkları ve Travma",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 22,
        "narrative": (
            "Yağ embolisi, iskelet sistemi travmalarının ve ortopedik cerrahilerin sık rastlanan bir komplikasyonudur: "
            "1. **Etyolojik Nedenler:** "
            "- **Uzun Kemik Kırıkları (En Sık):** Femur, tibia ve pelvis gibi sarı kemik iliğinden zengin kemiklerin kırıkları. "
            "- **Ortopedik Cerrahi Müdahaleler:** Kalça ve diz artroplastisi (protez takılması), intramedüller çivileme işlemleri. "
            "- **Ağır Yumuşak Doku Ezilmeleri ve Yanıklar:** Deri altı yağ dokusunun masif travması. "
            "2. **Venöz Lümen Giriş Mekanizması:** Kemik kırıldığında medüller boşluktaki ince duvarlı kemik iliği venöz sinüzoidleri yırtılır. "
            "Rigid kemik yapısı nedeniyle sinüzoidler açık kalır; kırık hattındaki hematomun yüksek basıncı yağ globüllerini bu açık venöz lümene pompalar. "
            "3. **Mikroskobik vs Klinik Ayrımı:** Ciddi kemik travması geçiren hastaların **>%90'ında mikroskobik yağ embolisi** mevcuttur; "
            "ancak bunların yalnızca küçük bir azınlığında (%1-10) klinik olarak belirgin 'Yağ Embolisi Sendromu' gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Yağ embolisinin klinik pratikte en sık görüldüğü klinik durum, medüller sinüzoidlerin yırtıldığı femur ve pelvis gibi uzun kemik kırıklarıdır.",
                "uzun kemik kırıklarıdır",
                "Kemik iliği yağının venöz lümene geçtiği primer travma türü"
            ),
            make_table(
                "Yağ Embolisi Risk Grupları ve Görülme Oranları",
                ["Klinik Durum", "Histolojik Yağ Embolisi Oranı", "Klinik Sendrom Riski"],
                [
                    ["Tekli Uzun Kemik Kırığı (Tibia)", "~%90 (Mikroskobik)", "< %1 - 2"],
                    [
                        "Çoklu Kırıklar (Femur + Pelvis)",
                        "~%100",
                        {"text": "%5 - 10 (Yağ Embolisi Sendromu)", "isMasked": True, "hint": "Çoklu kırıklarda semptomatik klinik sendrom sıklığı"}
                    ],
                    ["Total Kalça Protezi Ameliyatı", "~%80 - 90 (Geçici)", "< %1"],
                    ["Ağır Yanık ve Geniş Doku Ezilmesi", "~%50", "Nadir"]
                ]
            ),
            make_micro_quiz(
                "Trafik kazası sonrası bilateral femur şaft kırığı ve pelvis fraktürü saptanan 24 yaşındaki bir hastada, kemik iliğindeki yağın dolaşıma geçmesini kolaylaştıran temel anatomik özellik hangisidir?",
                {
                    "A": "Kemik içi venöz sinüzoidlerin ince duvarlı olması ve rijit kemik içinde açık kalarak kollobe olamaması",
                    "B": "Femur iliğinde hiç damar bulunmaması",
                    "C": "Kemik iliği yağının suda tamamen çözünür olması",
                    "D": "Kırık hattında kan basıncının sıfıra inmesi",
                    "E": "Trombositlerin yağı doğrudan fagosite etmesi"
                },
                "A",
                {
                    "A": "Rijit kemik dokusu içindeki venöz sinüzoidler yırtılınca açık kalır; artan basınç yağı doğrudan dolaşıma iter.",
                    "B": "Kemik iliği son derece damarsal bir yapıdır.",
                    "C": "Lipidler suda çözünmez.",
                    "D": "Kırık hematomunda basınç yüksektir.",
                    "E": "Trombositler yağı fagosite etmez, endotel zedelenir."
                }
            )
        ]
    })

    # Slayt 23: Yağ Embolisi Sendromu (FES) Patogenezi
    slides.append({
        "id": "k1-24-s23",
        "title": "Yağ Embolisi Sendromu Patogenezi: Mekanik Tıkanma ve Yağ Asidi Toksisitesi",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 23,
        "narrative": (
            "Yağ Embolisi Sendromu (FES), basit bir mekanik damar tıkanmasının çok ötesinde sistemik bir toksik-inflamatuar reaksiyondur: "
            "1. **Mekanik Obstrüksiyon:** Dolaşıma giren mikro yağ damlacıkları pulmoner ve serebral kılcal damarlara oturarak kan akımını keser. "
            "2. **Biyokimyasal Toksisite (Serbest Yağ Asidi Hasarı):** "
            "Damarlar içinde sıkışan nötral trigliseridler, endotelyal ve doku lipoprotein lipazları tarafından **Serbest Yağ Asitlerine (FFA)** hidrolize edilir. "
            "Serbest yağ asitleri endotel hücreleri için doğrudan sitotoksiktir: "
            "- **Yaygın Endotel Hasarı:** Kapiller geçirgenliği patlatır, alveol içine protein ve sıvı sızarak akciğer ödemi ve ARDS tablosu oluşturur. "
            "- **Trombosit Aktivasyonu ve Tüketimi:** Yağ asitleri trombosit agregasyonunu uyarır; trombositler mikrodamarlarda tükenerek **trombositopeni** yapar. "
            "- **Nötrofil Kemotaksisi:** Lokal inflamasyonu körükleyerek doku yıkımını artırır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Yağ embolisi sendromunda nötral yağların lipaz enzimiyle parçalanması sonucu açığa çıkan serbest yağ asitleri doğrudan endotel hasarı ve kapiller kaçak yapar.",
                "serbest yağ asitleri",
                "Lipidlerin hidroliziyle açığa çıkan sitotoksik kimyasal mediyatörler"
            ),
            make_causal_chain(
                "Yağ Embolisi Sendromu Biyokimyasal Toksisite Zinciri",
                [
                    "1. Medüller Yırtık: Femur kırığı sonrası nötral trigliseridlerin venöz sinüzoidlere geçmesi",
                    "2. Kılcal Tıkanma: Yağ mikro-globüllerinin akciğer ve beyin kapillerlerinde mekanik tıkanma yapması",
                    "3. Enzimatik Hidroliz: Lipaz enzimlerinin trigliseridleri toksik serbest yağ asitlerine dönüştürmesi",
                    "4. Endotelyal Yıkım: Serbest yağ asitlerinin kapiller endoteli parçalaması ve trombositleri tüketmesi",
                    "5. Sistemik Sendrom: Alveoler ödem (ARDS), trombositopenik peteşiler ve nörolojik deliryum tablosu"
                ]
            ),
            make_micro_quiz(
                "Yağ embolisi sendromunda kemik iliğinden kopan nötral yağların mekanik tıkanmanın ötesinde endotel hasarı ve diffüz alveolar hasara (ARDS) yol açmasından sorumlu olan primer toksik kimyasal ajan hangisidir?",
                {
                    "A": "Lipoprotein lipazla açığa çıkan Serbest Yağ Asitleri",
                    "B": "Plazminojen aktivatör inhibitörü (PAI-1)",
                    "C": "Eritrosit içindeki hemoglobin molekülleri",
                    "D": "Kemik minerali olan hidroksiapatit kristalleri",
                    "E": "Trombosit granüllerindeki serotonin"
                },
                "A",
                {
                    "A": "Serbest yağ asitleri doğrudan endotelyal sitotoksisite ve kapiller kaçak yaparak ARDS'yi tetikler.",
                    "B": "PAI-1 fibrinolizi inhibe eder, primer toksin değildir.",
                    "C": "Hemoglobin toksik etken değildir.",
                    "D": "Hidroksiapatit kemik tuzudur, endotel toksini değildir.",
                    "E": "Serotonin vazokonstriktördür, primer toksik ajan değildir."
                }
            )
        ]
    })

    # Slayt 24: Yağ Embolisi Sendromunun Klasik Klinik Triadı
    slides.append({
        "id": "k1-24-s24",
        "title": "Yağ Embolisi Sendromunun Klasik Klinik Triadı ve Zaman Penceresi",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 24,
        "narrative": (
            "Yağ Embolisi Sendromu (FES), travmanın hemen anında değil, tipik bir sessiz kuluçka evresinden sonra patlak verir: "
            "1. **Zaman Penceresi:** Semptomlar kemik kırığı veya travmadan **1 - 3 gün (24 - 72 saat) sonra** aniden başlar (bu gecikme lipaz aktivitesi ve yağ asidi birikimi için gereklidir). "
            "2. **Klasik Klinik Triad:** "
            "- **Solunum Yetmezliği (İlk ve En Sabit Bulgu):** Ani taşipne, dispne, hipoksemi; akciğer grafisinde bilateral kar fırtınası infiltratları (ARDS tablosu). "
            "- **Nörolojik Bozukluklar:** Serebral mikrosirkülasyon tutulumuna bağlı konfüzyon, ajitasyon, deliryum, stupor, fokal nörolojik defisit ve koma. "
            "- **Peteşiyal Döküntü (Patognomonik!):** Trombositopeni ve kapiller destrüksiyon sonucu **gövdenin üst yarısında, boyunda, aksillada ve konjonktivada** belirgin peteşiler görülür (olguların %20-50'sinde bulunur, tanı koydurucudur!). "
            "3. **Eşlik Eden Bulgular:** Taşikardi, açıklanamayan ateş (>38°C), anemi ve trombositopeni."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Yağ embolisi sendromunun patognomonik fizik muayene bulgusu gövdenin üst kısmı, boyun, aksilla ve konjonktivada ortaya çıkan peteşiyal döküntüdür.",
                "peteşiyal döküntüdür",
                "Trombositopeni ve endotel hasarına bağlı noktasal deri kanamaları"
            ),
            make_table(
                "Yağ Embolisi Sendromu Klasik Triadı Özeti",
                ["Triad Bileşeni", "Ortaya Çıkış Zamanı", "Karakteristik Klinik Bulgular", "Patolojik Mekanizma"],
                [
                    ["1. Solunum Yetmezliği", "Travmadan 24-72 saat sonra", "Taşipne, dispne, ağır hipoksi, ARDS", "Pulmoner kapiller kaçak ve endotel nekrozu"],
                    [
                        "2. Nörolojik Defisit",
                        "Solunum bulgularıyla eşzamanlı",
                        "Konfüzyon, huzursuzluk, deliryum, koma",
                        {"text": "Serebral mikrodamarlarda yağ embolizasyonu", "isMasked": True, "hint": "Beyin kılcal damarlarının yağ damlacıklarıyla tıkanması"}
                    ],
                    ["3. Peteşiyal Döküntü", "2-3. günlerde belirginleşir", "Aksilla, boyun, konjonktiva peteşileri", "Trombosit tüketimi ve dermal kapiller hasar"]
                ]
            ),
            make_micro_quiz(
                "Motosiklet kazasında sağ femur ve tibia kırığı nedeniyle ameliyat edilen 22 yaşındaki bir hastada, operasyondan 48 saat sonra aniden dispne, hipoksemi, konfüzyon ve boyun-aksilla bölgesinde noktasal peteşiyal döküntüler gelişmiştir. En olası klinik tanı hangisidir?",
                {
                    "A": "Yağ Embolisi Sendromu",
                    "B": "Amniyon Sıvısı Embolisi",
                    "C": "Akut Bakteriyel Menenjit",
                    "D": "Dekompresyon Hastalığı",
                    "E": "Masif Akut Miyokard Enfarktüsü"
                },
                "A",
                {
                    "A": "Femur kırığından 2 gün sonra solunum sıkıntısı, nörolojik konfüzyon ve aksiller peteşi triadı klasik Yağ Embolisi Sendromudur.",
                    "B": "Amniyon sıvısı embolisi doğuran kadınlarda olur.",
                    "C": "Menenjitte ense sertliği ve yüksek lökositoz ön plandadır.",
                    "D": "Dekompresyon derin dalış sonrası azot kabarcıklarıyla gelişir.",
                    "E": "MI sol göğüs ağrısı ve EKG değişikliği yapar, aksiller peteşi yapmaz."
                }
            )
        ]
    })

    # Slayt 25: Yağ Embolisinde Laboratuvar ve Otopsi Bulguları
    slides.append({
        "id": "k1-24-s25",
        "title": "Yağ Embolisinde Laboratuvar, Özel Boyalar ve Otopsi Bulguları",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 25,
        "narrative": (
            "Yağ embolisinin patolojik doğrulaması rutin doku takibinde özel teknikler gerektirir: "
            "1. **Rutin Histopatoloji Tuzağı:** Standart formalin fiksasyonu ve parafin bloklama sürecinde alkol ve ksilol kullanıldığından, "
            "tüm nötral yağlar çözünerek erir; geride damar içinde yalnızca boş yuvarlak vakuoller kalır! "
            "2. **Özel Yağ Boyaları ve Dondurma Kesiti (Frozen):** Doku taze dondurularak (frozen section) kesilmeli ve "
            "**Oil Red O** veya **Sudan Black / Sudan IV** boyaları ile boyanmalıdır; nötral lipidler parlak kırmızı/turuncu renkte parlar. "
            "3. **Laboratuvar Bulguları:** "
            "- **Trombositopeni:** Trombositler lipid globüllerine yapışıp mikrodolaşımda hızla tükenir. "
            "- **Anemi:** İskemik kapillerlerden geçerken eritrositlerin mekanik parçalanması. "
            "- **Lipidüri ve Balgamda Yağ:** İdrarda ve bronkoalveoler lavaj (BAL) sıvısında serbest yağ damlacıkları veya makrofaj içi yağ vakuolleri gösterilebilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Patoloji laboratuvarında yağ embolisinin kesin gösterilmesi için standart parafin blok yerine taze dondurma kesiti alınarak Oil Red O veya Sudan boyaları kullanılmalıdır.",
                "Oil Red O",
                "Lipidleri erimeden parlak kırmızı boyayan özel histokimyasal boya"
            ),
            make_table(
                "Yağ Embolisi Tanısal Yöntemleri ve Patolojik Karşılıkları",
                ["Tanı Yöntemi", "Uygulama Şekli", "Pozitif Bulgusu", "Tanısal Değeri"],
                [
                    ["Frozen Dondurma Kesiti", "Fiksasyonsuz taze akciğer dokusu", "Erimemiş lipid kürecikleri", "Kesin patolojik kanıt"],
                    [
                        "Oil Red O Boyaması",
                        "Lipid spesifik boyama",
                        {"text": "Kapiller lümeninde parlak kırmızı-turuncu damlacıklar", "isMasked": True, "hint": "Nötral yağların kırmızı boyanması"},
                        "Altın standart histokimya"
                    ],
                    ["Tam Kan Sayımı", "Periferik venöz kan", "Trombositopeni ve açıklanamayan anemi", "Klinik destekleyici bulgu"],
                    ["İdrar Mikroskopisi", "Santrifüj edilmiş idrar sedimenti", "Sudan pozitif serbest yağ globülleri", "Lipidüri tespiti"]
                ]
            ),
            make_micro_quiz(
                "Kırık sonrası ölen bir hastanın otopsisinde akciğer kapillerlerinde yağ embolisi varlığını mikroskop altında histokimyasal olarak kanıtlamak isteyen bir patoloğun uygulaması gereken en uygun doku hazırlama ve boyama yöntemi hangisidir?",
                {
                    "A": "Dondurma kesiti (frozen section) üzerine Oil Red O boyası",
                    "B": "Standart parafin bloklama ve Hematoksilen-Eozin",
                    "C": "Kongo kırmızısı boyası",
                    "D": "Prusya mavisi demir boyası",
                    "E": "Masson Trikrom bağ dokusu boyası"
                },
                "A",
                {
                    "A": "Yağlar parafin takipte eridiğinden frozen kesitte Oil Red O veya Sudan boyaları ile yağ gösterilir.",
                    "B": "Parafinde yağ erir, sadece boşluk kalır, tanı konamaz.",
                    "C": "Kongo kırmızısı amiloid boyasıdır.",
                    "D": "Prusya mavisi hemosiderin demirini gösterir.",
                    "E": "Masson trikrom kollajen liflerini boyar."
                }
            )
        ]
    })

    # Slayt 26: Amniyon Sıvısı Embolisi: Tanım ve Epidemiyoloji
    slides.append({
        "id": "k1-24-s26",
        "title": "Amniyon Sıvısı Embolisi (AFE): Tanım, İnsidans ve Yüksek Mortalite",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 26,
        "narrative": (
            "Amniyon Sıvısı Embolisi (AFE), obstetriğin en ani, tahmin edilemez ve ölümcül acil tablosudur: "
            "1. **Tanım:** Doğum eylemi sırasında veya doğumun hemen ardından amniyon sıvısının, "
            "fetal hücrelerin ve döküntülerin maternal venöz dolaşıma karışarak akciğer mikrosirkülasyonunu tıkamasıdır. "
            "2. **İnsidans:** Yaklaşık **40.000 doğumda 1** görülür; nadir bir olaydır. "
            "3. **Korkutucu Mortalite Oranı:** Anne ölüm oranı **yaklaşık %80'dir!** "
            "Gelişmiş ülkelerde anne ölümlerinin en sık doğrudan nedenleri arasında ikinci veya üçüncü sıradadır. "
            "4. **Ölüm Zamanlaması:** Olguların çoğunda ölüm ilk 1 saat içinde gelişir. "
            "Sağ kalan annelerin ise **%85'inden fazlasında ağır kalıcı nörolojik sekeller (hipoksik ensefalopati)** kalır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Amniyon sıvısı embolisi yaklaşık kırk bin doğumda bir görülmesine rağmen anne mortalitesi yaklaşık yüzde seksen olan en ölümcül obstetrik acildir.",
                "yüzde seksen",
                "Amniyon sıvısı embolisinde annenin tahmini ölüm yüzdesi"
            ),
            make_table(
                "Amniyon Sıvısı Embolisinin Epidemiyolojik ve Prognostik Profili",
                ["Epidemiyolojik Parametre", "Sayısal Değer / Oran", "Klinik Yansıması"],
                [
                    ["Görülme Sıklığı (İnsidans)", "~1 / 40.000 doğum", "Nadir fakat tamamen öngörülemez"],
                    [
                        "Maternal Mortalite Oranı",
                        {"text": "~%80 mortalite", "isMasked": True, "hint": "Olguların beşte dördünün kaybedilmesi"},
                        "Gelişmiş ülkelerde en ölümcül obstetrik felaket"
                    ],
                    ["Ölüm Zaman Penceresi", "İlk 1 saat içinde", "Kardiyak arrest ve refrakter şok"],
                    ["Nörolojik Sekel (Kalanlarda)", "> %85", "Hipoksik iskemik beyin hasarı ve koma"]
                ]
            ),
            make_micro_quiz(
                "Amniyon sıvısı embolisi (AFE) ile ilgili epidemiyolojik ve klinik verilerden hangisi doğrudur?",
                {
                    "A": "Mortalite oranı yaklaşık %80 olup anne ölümlerinin en ölümcül nedenlerindendir",
                    "B": "Yalnızca sezaryen doğumlarda görülür, normal vajinal doğumda asla görülmez",
                    "C": "Her 100 doğumda bir görülen çok yaygın bir durumdur",
                    "D": "Hastalarda hiçbir zaman pıhtılaşma bozukluğu (DİK) gelişmez",
                    "E": "Tüm hastalar tamamen sekelsiz iyileşir"
                },
                "A",
                {
                    "A": "Mortalite ~%80'dir; nadir (~1/40.000) fakat son derece ölümcüldür.",
                    "B": "Hem vajinal hem sezaryen doğumda gelişebilir.",
                    "C": "40.000 doğumda bir görülür, yaygın değildir.",
                    "D": "Hemen hemen tüm olgularda masif DİK gelişir.",
                    "E": "Sağ kalanların %85'inde ağır kalıcı nörolojik sekel kalır."
                }
            )
        ]
    })

    # Slayt 27: AFE Patogenezi: Şok, Anafilaktoid Reaksiyon ve DİK
    slides.append({
        "id": "k1-24-s27",
        "title": "AFE Patogenezi: İntrauterin Yırtık, Anafilaktoid Yanıt ve Masif DİK",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 27,
        "narrative": (
            "Amniyon sıvısı embolisinin patogenezi üçlü ölümcül bir mekanizma üzerinde ilerler: "
            "1. **Bariyer Yıkımı:** Doğum eylemi sırasında amniyon zarlarının yırtılması ve "
            "uterus veya serviksteki genişlemiş venöz sinüzoidlerin açılmasıyla amniyon sıvısı anne dolaşımına girer. "
            "2. **Anafilaktoid Şok (Gebelikteki Anafilaktoid Sendrom):** "
            "Amniyon sıvısı anne immün sistemi için yabancı antijenler ve vazoaktif maddeler (lökotrienler, prostaglandinler) içerir. "
            "Anne pulmoner damarlarında ani şiddetli vazospazm tetiklenir; "
            "akut sağ kalp yetmezliği, derin hipotansiyon ve kardiyojenik şok gelişir. "
            "3. **Masif Tüketim Koagülopatisi (DİK):** "
            "Amniyon sıvısı yüksek miktarda **Doku Faktörü (Tromboplastin)** ve prokoagülan madde içerir. "
            "Anne dolaşımına karıştığı anda sistemik pıhtılaşma kaskadını patlatır; "
            "tüm mikrodolaşımda fibrin trombüsleri oluşur, pıhtılaşma faktörleri tükenir ve **Dissemine İntravasküler Koagülasyon (DİK)** nedeniyle kontrolsüz masif kanamalar başlar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Amniyon sıvısının yüksek oranda doku faktörü içermesi nedeniyle anne dolaşımına girdiğinde tüm damar ağında pıhtılaşmayı tetikleyerek dissemine intravasküler koagülasyona yol açar.",
                "dissemine intravasküler koagülasyona",
                "Tüketim koagülopatisi ve yaygın mikrotromboz sendromu"
            ),
            make_table(
                "Amniyon Sıvısı Embolisinde Klinik Kaskad",
                ["Klinik Faz", "Patofizyolojik Mekanizma", "Klinik Tablo"],
                [
                    ["1. Pulmoner Vazospazm", "Vazoaktif mediyatörlerin pulmoner arterleri daraltması", "Ani siyanoz, şiddetli dispne, hipoksemi"],
                    [
                        "2. Kardiyojenik Şok",
                        "Sağ ventrikül yetmezliği ve sol ventrikül doluş kaybı",
                        {"text": "Ağır hipotansiyon ve kardiyovasküler kollaps", "isMasked": True, "hint": "Tansiyonun ölçülememesi ve kardiyak arrest"}
                    ],
                    ["3. Masif DİK Evresi", "Doku faktörüyle pıhtılaşma faktörlerinin tükenmesi", "Uterus atonisinden ve damar yollarından durdurulamayan kanama"]
                ]
            ),
            make_micro_quiz(
                "Doğum eylemi sırasında aniden derin siyanoz ve şoka giren, ardından doğum kanalından ve damar yolu girişlerinden pıhtılaşmayan yoğun kanama başlayan bir lohusada bu kanama tablosunun altta yatan primer patolojik mekanizması hangisidir?",
                {
                    "A": "Amniyon sıvısındaki doku faktörünün tetiklediği Dissemine İntravasküler Koagülasyon (DİK)",
                    "B": "Akut apandisit perforasyonu",
                    "C": "Fizyolojik lochia rubra artışı",
                    "D": "Konjenital hemofili A taşıyıcılığı",
                    "E": "Trombositoz ve hiperkoagülabilite fazı"
                },
                "A",
                {
                    "A": "Amniyon sıvısındaki prokoagülan doku faktörü tüketim koagülopatisi (DİK) yaparak masif kanamalara neden olur.",
                    "B": "Apandisit doğumda ani şok ve DİK yapmaz.",
                    "C": "Lochia normal doğum akıntısıdır.",
                    "D": "Hemofili A erkeklerde görülür, ani doğum şoku yapmaz.",
                    "E": "Burada trombosit artışı değil, tüketim trombositopenisi vardır."
                }
            )
        ]
    })

    # Slayt 28: AFE Morfolojik Kanıtları ve Otopsi Bulguları
    slides.append({
        "id": "k1-24-s28",
        "title": "AFE Morfolojik Kanıtları: Akciğer Damarlarında Fetal Döküntüler",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 28,
        "narrative": (
            "Amniyon Sıvısı Embolisinin kesin patolojik tanısı otopside annenin akciğer histopatolojisiyle konur: "
            "1. **Karakteristik Mikroskobik Bulgular:** Annenin küçük pulmoner arterlerinde, arteriyollerinde ve alveoler kapillerlerinde "
            "bebeğe ait döküntülerin lümeni tıkadığı görülür: "
            "- **Fetal Skuamöz Epitel Hücreleri (Verniks Hücreleri):** Fetal deriden dökülen yassı keratinize hücreler (müsin ve keratin boyalarıyla parlar). "
            "- **Lanugo Tüyleri:** Fetusun vücudunu kaplayan ince kılların enine/boyuna kesitleri. "
            "- **Verniks Kazeoza Yağı:** Fetal cildini kaplayan peynir kıvamındaki sebum lipidleri. "
            "- **Fetal Solunum ve Sindirim Mukusu:** Asellüler müsin birikintileri. "
            "- **Mekonyum:** Fetal dışkı pigmentleri (aspirasyon varsa belirgindir). "
            "2. **Eşlik Eden Patolojiler:** Alveollerde yaygın fibrin trombüsleri (DİK kanıtı), diffüz alveolar hasar (DAD / şok akciğeri) ve masif pulmoner ödem."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Amniyon sıvısı embolisinde otopside annenin pulmoner mikrodolaşım damarları içinde fetal skuamöz epitel hücreleri ve lanugo tüyleri saptanması patognomoniktir.",
                "fetal skuamöz epitel",
                "Fetusun cildinden dökülüp anne damarlarını tıkayan yassı hücreler"
            ),
            make_table(
                "Amniyon Sıvısı Embolisi Histopatolojik Bileşenleri",
                ["Fetal Döküntü Bileşeni", "Köken Aldığı Fetal Yapı", "Histopatolojik Görünüm"],
                [
                    ["Fetal Skuamöz Hücreler", "Fetal epidermis ve verniks kazeoza", "Nükleussuz, yassı keratin plakları"],
                    [
                        "Lanugo Tüyleri",
                        "Fetal cilt tüyleri",
                        {"text": "İnce silindirik kıl gövdesi kesitleri", "isMasked": True, "hint": "Fetal kılların mikroskobik kesitleri"}
                    ],
                    ["Müsin / Mukus", "Fetal solunum ve bağırsak salgıları", "Alcian blue pozitif asellüler kitleler"],
                    ["Fibrin Trombüsleri", "Maternal DİK reaksiyonu", "Mikrodamarları tıkayan pembe fibrin ağları"]
                ]
            ),
            make_micro_quiz(
                "Doğum sırasında aniden dispne, şok ve yaygın kanamayla kaybedilen bir kadının akciğer biyopsi/otopsi kesitlerinde pulmoner arteriyol lümenlerinde fetal skuamöz hücreler ve lanugo tüyleri saptanmıştır. Bu bulgu aşağıdaki patolojilerden hangisi için kesin tanı koydurucudur?",
                {
                    "A": "Amniyon Sıvısı Embolisi (AFE)",
                    "B": "Yağ Embolisi Sendromu",
                    "C": "Eyer (Saddle) Tromboembolisi",
                    "D": "Dekompresyon Hastalığı",
                    "E": "Tümör Hücre Embolisi"
                },
                "A",
                {
                    "A": "Anne pulmoner damarlarında fetal skuamöz hücre ve lanugo tüyü görülmesi AFE'nin patognomonik otopsi bulgusudur.",
                    "B": "Yağ embolisinde lipid damlacıkları vardır, fetal hücre olmaz.",
                    "C": "Eyer embolisinde fibrin-trombosit trombüsü vardır.",
                    "D": "Dekompresyonda gaz kabarcığı vardır.",
                    "E": "Tümör embolisinde atipik malign hücreler izlenir."
                }
            )
        ]
    })

    # Slayt 29: [TEKRAR SAYFASI - CHECKPOINT 3] Yağ Embolisi Sendromu ve Amniyon Sıvısı Embolisi
    slides.append({
        "id": "k1-24-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Yağ Embolisi Sendromu ve Amniyon Sıvısı Embolisi",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 29,
        "narrative": (
            "Bu üçüncü checkpoint sayfasında, yağ embolisi ve amniyon sıvısı embolisinin temel mekanizmalarını özetliyoruz: "
            "1. **Yağ Embolisi Etyolojisi:** Uzun kemik (femur, tibia, pelvis) kırıkları ve ortopedik protez cerrahisidir. "
            "2. **FES Patogenezi:** Mekanik tıkanma + Lipazların trigliseridi parçalamasıyla oluşan SERBEST YAĞ ASİTLERİNİN endotelyal toksisitesidir. "
            "3. **FES Triadı:** Travmadan 1-3 GÜN (24-72 saat) sonra başlayan SOLUNUM YETMEZLİĞİ (ARDS), NÖROLOJİK BOZUKLUK (deliryum/koma) "
            "ve boyun/aksilla/konjonktivada PETEŞİYAL DÖKÜNTÜDÜR (trombositopeni eşlik eder). "
            "4. **Özel Boyama:** Parafinde yağ erir; tanıda dondurma kesiti (frozen) ve OİL RED O / SUDAN boyaları şarttır. "
            "5. **Amniyon Sıvısı Embolisi:** Doğumda zarların yırtılmasıyla anne dolaşımına geçiştir; mortalitesi ~%80'dir. "
            "6. **AFE Kliniği:** Ani dispne, siyanoz, şok ve amniyon sıvısındaki doku faktörüne bağlı MASİF DİK (tüketim kanamaları). "
            "7. **AFE Otopside Kanıtı:** Anne akciğer damarlarında FETAL SKUAMÖZ HÜCRELER, LANUGO TÜYLERİ ve verniks kazeoza saptanmasıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s29-1",
                "Uzun kemik kırıklarından bir ile üç gün sonra ortaya çıkan solunum yetmezliği, konfüzyon ve gövdede peteşiyal döküntü triadı hangi klinik sendromu tanımlar?",
                "Yağ embolisi sendromudur.",
                "Kırık kemik iliğindeki medüller lipidlerin serbest yağ asidi toksisitesi yapması",
                "Yağ Embolisi Triadı"
            ),
            make_flashcard(
                "k1-24-fc-s29-2",
                "Doğum sırasında aniden gelişen kardiyak arrest ve şok tablosuyla ölen bir annenin akciğer damarlarında mikroskopta saptanan fetal skuamöz hücreler ve lanugo tüyleri hangi tanıyı kesinleştirir?",
                "Amniyon sıvısı embolisi tablosudur.",
                "Gebelikte yırtılan uterin venlerden anne kan dolaşımına geçen fetal ürünler",
                "Amniyon Sıvısı Embolisi"
            ),
            make_flashcard(
                "k1-24-fc-s29-3",
                "Amniyon sıvısı embolisinde hastada dakikalar içinde masif tüketim koagülopatisine ve kontrolsüz kanamalara yol açan hematolojik tablo nedir?",
                "Dissemine intravasküler koagülasyondur (DİK).",
                "Fibrin trombüsleri ve pıhtılaşma faktörlerinin aşırı tüketilmesi sendromu",
                "AFE ve DİK"
            )
        ],
        "interactiveElements": [
            make_table(
                "Yağ Embolisi ile Amniyon Sıvısı Embolisi Karşılaştırması",
                ["Klinik Özellik", "Yağ Embolisi Sendromu (FES)", "Amniyon Sıvısı Embolisi (AFE)"],
                [
                    ["Tipik Hasta Grubu", "Femur/pelvis kırığı olan genç travma hastası", "Doğum eyleminde veya lohusalıkta kadın"],
                    ["Başlangıç Zamanı", "Travmadan 24 - 72 saat sonra (gecikmeli)", "Doğum sırasında veya hemen ardından (ani)"],
                    [
                        "Klasik Patoloji",
                        "Solunum sıkıntısı + Deliryum + Peteşiyal döküntü",
                        {"text": "Kardiyak arrest + Şok + Masif DİK kanamaları", "isMasked": True, "hint": "Kardiyovasküler çöküş ve tüketim koagülopatisi"}
                    ],
                    ["Histopatolojik Kanıt", "Kapillerlerde Oil Red O pozitif lipidler", "Akciğer damarlarında fetal skuamöz epitel ve lanugo"],
                    ["Mortalite Düzeyi", "~%5 - 10", "~%80 (Son derece yüksek)"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi Yağ Embolisi Sendromu ile Amniyon Sıvısı Embolisinin ORTAK özelliklerinden biridir?",
                {
                    "A": "Her ikisinin de akciğer mikrosirkülasyonunu etkileyerek ağır solunum yetmezliğine (ARDS) yol açabilmesi",
                    "B": "Her ikisinin de yalnızca erkeklerde görülmesi",
                    "C": "Her ikisinde de Oil Red O boyasının negatif sonuç vermesi",
                    "D": "Her ikisinin de derin dalış sonrasında azot gazıyla oluşması",
                    "E": "Her ikisinin de mortalitesinin %1'in altında olması"
                },
                "A",
                {
                    "A": "Her iki emboli türü de akciğer kapiller endotelini yıkarak ağır solunum yetmezliği ve ARDS tablosu oluşturur.",
                    "B": "AFE yalnızca doğuran kadınlarda görülür.",
                    "C": "Yağ embolisinde Oil Red O pozitiftir.",
                    "D": "Azot gazı dekompresyon hastalığıdır.",
                    "E": "AFE'de mortalite %80'dir."
                }
            )
        ]
    })

    # Slayt 30: Bölüm Özeti: Gaz/Hava Embolisi ve Dekompresyon Hastalığına Geçiş
    slides.append({
        "id": "k1-24-s30",
        "title": "Bölüm Özeti: Gaz/Hava Embolisi ve Dekompresyon Hastalığına Geçiş",
        "section": "Özel Emboli Tipleri: Yağ ve Amniyon Sıvısı Embolisi",
        "slideNumber": 30,
        "narrative": (
            "Yağ ve amniyon sıvısı embolilerini tamamlarken hekimlik derslerini özetliyoruz: "
            "1. **Gecikmiş Dispne Yağ Embolisidir:** Kırık sonrası 2. günde nefes darlığı ve konfüzyon gelişen genç hastada FES düşünülmeli ve aksilla peteşileri aranmalıdır. "
            "2. **AFE Bir Anafilaktoid ve Koagülasyon Krizidir:** Doğum salonunda ani siyanoz ve şok geliştiğinde masif DİK için kan ürünleri hazır tutulmalıdır. "
            "3. **Otopsi İpuçları:** Frozen kesit yağ için, keratin/müsin boyaları fetal döküntü için altın standarttır. "
            "4. **Sonraki Bölüme Köprü:** Bir sonraki bölümümüzde gaz halindeki embolileri; cerrahi hava embolisini, "
            "dalgıçlarda görülen dekompresyon hastalığını (bends ve chokes), kronik Caisson hastalığını ve nadir tümör embolilerini inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Doğum sırasında gelişen amniyon sıvısı embolisinde anne hayatını tehdit eden en ölümcül kardiyovasküler komplikasyon anafilaktoid şok ve masif tüketim koagülopatisidir.",
                "tüketim koagülopatisidir",
                "Pıhtılaşma faktörlerinin tükenmesiyle durdurulamayan kanama tablosu"
            ),
            make_active_recall(
                "Femur kırığı ameliyatı sonrası 2. günde konfüzyon ve dispne geliştiren bir hastada göğüs cildinde aranması gereken ve yağ embolisi sendromu tanısını destekleyen en spesifik fizik muayene bulgusu nedir?",
                "Gövde üst kısmı, boyun ve aksilladaki peteşiyal döküntülerdir.",
                "Trombositopeniye bağlı küçük noktasal deri kanamaları"
            ),
            make_micro_quiz(
                "Aşağıdaki durumlardan hangisinde yağ embolisi sendromu gelişme riski diğerlerine göre belirgin olarak DAHA YÜKSEKTİR?",
                {
                    "A": "Bilateral femur şaft kırığı ve ezilme yaralanması olan politravmalı hasta",
                    "B": "Yalnızca el bileğinde fissür çatlağı olan çocuk",
                    "C": "Diş çekimi yapılan sağlıklı birey",
                    "D": "Düşme sonrası burun kemiği kırılan hasta",
                    "E": "Grip enfeksiyonu geçiren genç erişkin"
                },
                "A",
                {
                    "A": "Bilateral femur kırığı çok miktarda kemik iliği yağı açığa çıkarır ve FES için en yüksek riskli tablodur.",
                    "B": "El bileği fissürü medüller yağ salmaz.",
                    "C": "Diş çekimi yağ embolisi yapmaz.",
                    "D": "Burun kemiği kıkırdaktır, iliği yoktur.",
                    "E": "Viral enfeksiyon kemik iliğini etkilemez."
                }
            )
        ]
    })

    return slides
