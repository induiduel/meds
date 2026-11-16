# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 10: Enfeksiyon Taşları, İlaçlar ve Korunma İlkeleri (Slayt 91 - 100)
Checkpoint: Slayt 100
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_10_slides():
    return [
        # Slayt 91
        {
            "slideNumber": 91,
            "title": "Enfeksiyon Taşlarının Mikrobiyolojisi: Üreaz Pozitif Bakteriler",
            "content": (
                "Enfeksiyon taşları, üriner sistemde 'üreaz enzimi' üreten bakteriyel patojenlerin yol açtığı persistan "
                "kolonizasyon ve enfeksiyon zemininde meydana gelir. En sık ve en klasik etken, güçlü üreaz aktivitesine sahip "
                "olan 'Proteus mirabilis'tir (%70-80). Diğer önemli üreaz üreten mikroorganizmalar arasında Klebsiella pneumoniae, "
                "Pseudomonas aeruginosa, Staphylococcus aureus, Staphylococcus epidermidis, Providencia, Serratia ve Ureaplasma "
                "urealyticum yer alır. Buna karşılık toplum kökenli komplike olmayan üriner enfeksiyonların en sık etkeni olan "
                "'Escherichia coli' kural olarak üreaz enzimine sahip değildir (üreaz negatiftir) ve tek başına asla strüvit "
                "taşı oluşturmaz; ancak hasarlı dokuya sekonder olarak eklenebilir."
            ),
            "elements": [
                make_table(
                    "Üriner Patojenlerin Üreaz Enzim Aktivitesine Göre Dağılımı",
                    ["Mikroorganizma", "Üreaz Aktivitesi", "Strüvit Taşı Oluşturma Yeteneği"],
                    [
                        {
                            "cells": ["Proteus mirabilis", "Çok Güçlü Pozitif", "Klasik ve en sık etken"],
                            "hiddenIndex": 1,
                            "hint": "Primer üreaz aktivitesi"
                        },
                        {
                            "cells": ["Klebsiella pneumoniae", "Pozitif", "Sık etken"],
                            "hiddenIndex": 0,
                            "hint": "Kapsüllü üreaz bakterisi"
                        },
                        {
                            "cells": ["Escherichia coli", "Negatif", "Tek başına strüvit oluşturamaz"],
                            "hiddenIndex": 1,
                            "hint": "Enzim yokluğu durumu"
                        }
                    ]
                ),
                make_cloze(
                    "Üreaz enzimi üreterek enfeksiyon taşlarının oluşumuna en sık yol açan klasik bakteri Proteus mirabilis bakterisidir.",
                    "Proteus mirabilis",
                    "En yaygın üreaz patojeni"
                )
            ]
        },
        # Slayt 92
        {
            "slideNumber": 92,
            "title": "Üre Hidrolizi ve Aşırı Alkali İdrar (pH > 7.2)",
            "content": (
                "Bakteriyel üreaz enziminin katalizlediği temel kimyasal reaksiyon, idrarda bol bulunan ürenin hidrolizidir: "
                "Üre [CO(NH2)2] + H2O → 2 NH3 + CO2. Açığa çıkan serbest amonyak (NH3), ortamdaki hidrojen iyonlarını (H+) "
                "kendine bağlayarak amonyum (NH4+) formuna dönüşür. Bu proton tüketimi, idrar pH'ının dramatik bir biçimde "
                "yükselmesine ve fizyolojik sınırların çok ötesine (pH 7.5 - 8.5) fırlamasına neden olur. Alkali ortamda "
                "fosfat iyonları üç değerlikli anyon formuna (PO4^3-) iyonlaşır. Masif amonyum, serbest magnezyum ve fosfat "
                "iyonlarının birleşmesiyle 'strüvit' (magnezyum amonyum fosfat), kalsiyum ile fosfatın birleşmesiyle de "
                "'karbonat apatit' kristalleri eş zamanlı çökerek taşı meydana getirir."
            ),
            "elements": [
                make_causal_chain(
                    "Bakteriyel Üreazdan Strüvit ve Karbonat Apatit Çökelmesine Uzanan Yol",
                    [
                        "1. Üreaz Enzimi: Bakterinin üreyi amonyak ve karbondioksite parçalaması",
                        "2. Proton Tüketimi: Amonyağın serbest hidrojenleri bağlayarak amonyum oluşturması",
                        "3. Aşırı Alkalinizasyon: İdrar pH'ının 7.5'in üzerine fırlaması",
                        "4. Fosfat İyonlaşması: Üç değerlikli fosfat anyonlarının açığa çıkması",
                        "5. Kristalizasyon: Amonyum, magnezyum ve fosfatın strüvit; kalsiyum ve fosfatın karbonat apatit yapması"
                    ]
                ),
                make_active_recall(
                    "Bakteriyel üreaz reaksiyonunda amonyağın hidrojen iyonlarını tüketmesi sonucu idrar pH'ında meydana gelen karakteristik değişim nedir?",
                    "İdrar pH'ının yedi buçuğun üzerine çıkarak aşırı alkali hale gelmesidir.",
                    "Belirgin bazikleşme süreci"
                )
            ]
        },
        # Slayt 93
        {
            "slideNumber": 93,
            "title": "Koraliform (Staghorn) Taşlar ve Cerrahi Zorunluluk",
            "content": (
                "Enfeksiyon taşları, toplayıcı sistemin anatomik sınırlarına hızla uyum sağlayarak böbrek pelvisini ve "
                "kalikslerin tamamını dolduran devasa boyutlara ulaşır; bu görünümlerinden ötürü 'geyik boynuzu' veya "
                "'koraliform (staghorn)' taş olarak adlandırılırlar. Bu taşlar kadınlarda erkeklere oranla 2 kat daha sıktır. "
                "Koraliform taşlar yalnızca mekanik bir kitle olmayıp, bakteriler taşın derin mikrogözeneklerinde ve organik "
                "matriks içinde canlı kalır. Antibiyotikler taşın içine penetre olamadığından enfeksiyon asla tam kür edilemez. "
                "Tedavi edilmeyen staghorn taşlar kronik obstrüksiyon, ksantogranülomatöz piyelonefrit, renal atrofi ve "
                "ürosepsise bağlı ölüm yaratır; cerrahi olarak tek bir fragman dahi kalmayacak şekilde tamamen temizlenmelidir."
            ),
            "elements": [
                make_before_after(
                    "Staghorn Taşında Tedavi Yaklaşımları",
                    "Yalnızca Medikal Antibiyotik Tedavisi",
                    "Antibiyotikler taşın çekirdeğindeki bakterilere ulaşamaz; taş hızla büyümeye devam eder, sepsis ve nefron kaybı kaçınılmazdır.",
                    "Eksiksiz Cerrahi Temizleme (PCNL) + Antibiyoterapi",
                    "Tüm taş fragmanları çıkarılır, enfeksiyon yuvası yok edilir, postoperatif steril idrarla nüksler engellenir.",
                    "Enfeksiyon taşlarında 'rezidü taş parçası kalmaması' nüksü önlemenin mutlak koşuludur."
                ),
                make_cloze(
                    "Böbrek pelvisini ve kaliksleri tamamen dolduran dallanmış enfeksiyon taşlarına geyik boynuzu veya koraliform taş denir.",
                    "koraliform taş",
                    "Toplayıcı sistemi kaplayan staghorn kitle"
                )
            ]
        },
        # Slayt 94
        {
            "slideNumber": 94,
            "title": "Doğrudan Çöken İlaç Taşları",
            "content": (
                "İlaç taşları tüm taşların yaklaşık %1-2'sini teşkil eder ve direkt olarak ilacın kendisinin idrarda "
                "çözünürlük sınırını aşarak kristalleşmesiyle meydana gelir. En bilinen prototip, HIV enfeksiyonu tedavisinde "
                "kullanılan bir proteaz inhibitörü olan 'indinavir'dir. İndinavir, özellikle asidik idrarda ve dehidratasyonda "
                "hızla çöker; yumuşak, jelatinöz kitleler oluşturur. Bu kitleler tamamen radyolüsen olup kontrassız bilgisayarlı "
                "tomografide bile zayıf dansite verir. Diğer doğrudan çöken ilaçlar arasında potasyum tutucu bir diüretik olan "
                "'triamteren', antibiyotik olarak kullanılan 'sülfadiazin/sülfametoksazol', öksürük şuruplarındaki 'guaifenesin' "
                "ve astım tedavisindeki 'efedrin' yer alır."
            ),
            "elements": [
                make_table(
                    "Doğrudan İdrarda Kristalleşen İlaçlar ve Özellikleri",
                    ["İlaç Adı", "Kullanım Endikasyonu", "Kristal Karakteri", "Radyolojik Görünüm"],
                    [
                        {
                            "cells": ["İndinavir", "HIV enfeksiyonu (Proteaz inhibitörü)", "Jelatinöz agregat, iğsi kristal", "BT ve DÜSG'de tamamen lüsen"],
                            "hiddenIndex": 0,
                            "hint": "Antiretroviral proteaz ilacı"
                        },
                        {
                            "cells": ["Triamteren", "Hipertansiyon (K-tutucu diüretik)", "Yuvarlak kahverengi kristaller", "Zayıf radyoopak / lüsen"],
                            "hiddenIndex": 0,
                            "hint": "Potasyum tutucu idrar söktürücü"
                        },
                        {
                            "cells": ["Sülfadiazin", "Enfeksiyonlar (Toksoplazmoz vb.)", "Şok demeti şeklinde kristaller", "Radyolüsen"],
                            "hiddenIndex": 0,
                            "hint": "Klasik sülfonamid antibiyotiği"
                        }
                    ]
                ),
                make_active_recall(
                    "HIV tedavisinde kullanılan ve idrarda doğrudan kristalleşerek radyolüsen taş oluşturan proteaz inhibitörü hangisidir?",
                    "İndinavir etken maddesidir.",
                    "Antiviral proteaz blokörü"
                )
            ]
        },
        # Slayt 95
        {
            "slideNumber": 95,
            "title": "Metabolik Dengeyi Bozan Sekonder İlaç Taşları",
            "content": (
                "Bazı ilaçlar kendileri kristalleşmez; ancak renal tübüler fizyolojiyi veya sistemik asit-baz dengesini "
                "bozarak ikincil olarak kalsiyum veya ürik asit taşlarının oluşumuna zemin hazırlar. En klasik örnekler "
                "karbonik anhidraz enzim inhibitörleri olan 'asetazolamid' ve antiepileptik/migren ilacı olan 'topiramat'tır. "
                "Bu ilaçlar proksimal tübülde bikarbonat geri emilimini engelleyerek sistemik metabolik asidoza yol açar; "
                "asidoz tübüler sitrat geri emilimini uyararak idrarda aşırı hipositratüri (<50 mg/gün) yaratırken, idrar "
                "pH'ını da 7.0'nin üzerine çıkarır. Alkali idrarda sitratsız ortam kalsiyum fosfat (apatit) taşlarını hızla tetikler. "
                "Kronik laksatif suistimali ise amonyum ürat taşlarına neden olur."
            ),
            "elements": [
                make_before_after(
                    "Topiramat / Asetazolamid Kullanımının Litogenik Etkisi",
                    "İlaç Kullanımı Öncesi",
                    "Normal bikarbonat geri emilimi, dengeli asit-baz durumu, yeterli idrar sitrat atılımı, taş yok.",
                    "İlaç Kullanımı Sonrası (Karbonik Anhidraz Blokajı)",
                    "Sistemik asidoz, yüksek idrar pH'ı, idrarda sitratın tamamen tükenmesi; kalsiyum fosfat taşında patlama.",
                    "Topiramat kullanan migren ve epilepsi hastalarında periyodik idrar sitratı ve ultrason kontrolü şarttır."
                ),
                make_cloze(
                    "Karbonik anhidraz inhibisyonu yaparak alkali idrar ve şiddetli hipositratüri üzerinden taş oluşturan antiepileptik ilaç topiramat molekülüdür.",
                    "topiramat",
                    "Migren ve epilepside kullanılan CA inhibitörü"
                )
            ]
        },
        # Slayt 96
        {
            "slideNumber": 96,
            "title": "Ürolitiyaziste Genel Diyet İlkeleri",
            "content": (
                "Ürolitiyazis hastalarında medikal korunmanın en temel basamağını kanıta dayalı diyet düzenlemeleri oluşturur. "
                "En kritik kural, 24 saatlik idrar hacmini en az 2.5 litrenin üzerine çıkaracak şekilde günlük 2.5 - 3 litre "
                "sıvı (özellikle su) tüketilmesidir. Yaygın bir klinik hata, kalsiyum taşı olan hastalarda diyet kalsiyumunun "
                "kısıtlanmasıdır. Kalsiyum kısıtlandığında bağırsakta oksalatı bağlayacak serbest kalsiyum kalmaz; serbest "
                "oksalat emilerek hiperoksalüriye ve taş nüksüne yol açar. Bu nedenle diyet kalsiyumu normal sınırlarda "
                "(1000-1200 mg/gün) tutulmalıdır. Bunun yerine sofra tuzu (<2 gr/gün sodyum) ve hayvansal protein kısıtlanmalı, "
                "oksalattan zengin besinler dengelenmelidir."
            ),
            "elements": [
                make_micro_quiz(
                    "Kalsiyum oksalat taşı düşüren bir hastaya diyet önerilerinde bulunurken yapılan en tehlikeli ve hatalı yaklaşım hangisidir?",
                    [
                        {
                            "text": "Diyetteki kalsiyum alımının aşırı kısıtlanması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; kalsiyumu kısıtlamak bağırsakta oksalat emilimini artırarak taş nüksünü fırlatır."
                        },
                        {
                            "text": "Günlük sıvı tüketiminin artırılması",
                            "isCorrect": False,
                            "explanation": "Sıvı artışı taş önlemede en etkili koruyucu kuraldır."
                        },
                        {
                            "text": "Diyetle alınan sofra tuzunun azaltılması",
                            "isCorrect": False,
                            "explanation": "Tuz kısıtlaması idrar kalsiyumunu düşürerek taşı önler."
                        },
                        {
                            "text": "Aşırı hayvansal protein tüketiminden kaçınılması",
                            "isCorrect": False,
                            "explanation": "Protein kısıtlaması asit ve pürin yükünü düşürür, doğrudur."
                        }
                    ],
                    "Kalsiyum kısıtlaması oksalat emilimini artırdığı için güncel kılavuzlarda kesinlikle önerilmez."
                ),
                make_active_recall(
                    "Taş hastalarında taş nüksünü önlemek için 24 saatlik idrar hacminin en az kaç litrenin üzerinde tutulması hedeflenir?",
                    "İki buçuk litrenin üzerinde tutulması hedeflenir.",
                    "İki buçuk litrelik idrar debisi hedefi"
                )
            ]
        },
        # Slayt 97
        {
            "slideNumber": 97,
            "title": "Farmakolojik Tedavi: Tiyazidler, Allopurinol ve Sitrat",
            "content": (
                "Diyet önlemlerine rağmen metabolik risk faktörleri devam eden veya agresif nüks gösteren hastalarda "
                "hedefe yönelik farmakolojik tedavi başlanır. İdiyopatik hiperkalsiüride birinci seçenek 'tiyazid grubu "
                "diüretikler'dir (hidroklorotiyazid, klortalidon, indapamid); distal kıvrıntılı tübülde sodyum-klorür kotransportunu "
                "bloke ederek kalsiyum reabsorpsiyonunu artırır ve idrar kalsiyumunu %50 azaltırlar. Hiperürikozürik kalsiyum "
                "taşı veya ürik asit taşlarında ksantin oksidaz inhibitörü 'allopurinol' (veya febuksostat) pürin üretimini "
                "baskılar. Hipositratürik veya asidik idrarlı olgularda ise 'potasyum sitrat' idrar inhibitör kapasitesini güçlendirir."
            ),
            "elements": [
                make_table(
                    "Metabolik Risk Bozukluğuna Göre Farmakolojik Tedavi Eşleşmesi",
                    ["Metabolik Bozukluk", "Birinci Seçenek İlaç", "Etki Mekanizması"],
                    [
                        {
                            "cells": ["Hiperkalsiüri", "Tiyazid diüretikler (Klortalidon / İndapamid)", "Distal tübülde kalsiyum geri emilimini artırma"],
                            "hiddenIndex": 1,
                            "hint": "Kalsiyum düşürücü idrar söktürücü"
                        },
                        {
                            "cells": ["Hiperürikozüri", "Allopurinol / Febuksostat", "Ksantin oksidazı inhibe ederek ürik asit sentezini azaltma"],
                            "hiddenIndex": 1,
                            "hint": "Pürin sentez inhibitörü"
                        },
                        {
                            "cells": ["Hipositratüri", "Potasyum sitrat", "İdrar sitratını artırma ve idrarı alkalileştirme"],
                            "hiddenIndex": 1,
                            "hint": "En güçlü alkali sitrat tuzu"
                        }
                    ]
                ),
                make_cloze(
                    "İdiyopatik hiperkalsiüri tedavisinde distal tübüler kalsiyum geri emilimini artıran ilaç grubu tiyazid diüretiklerdir.",
                    "tiyazid diüretiklerdir",
                    "Kalsiyum atılımını düşüren diüretik sınıfı"
                )
            ]
        },
        # Slayt 98
        {
            "slideNumber": 98,
            "title": "Taş Hastasında İzlem ve 24 Saatlik İdrar Analiz Protokolü",
            "content": (
                "İlk kez taş düşüren ve düşük riskli olan hastalarda rutin tam idrar tahlili, serum kreatinin, kalsiyum "
                "ve ürik asit bakılması yeterlidir. Ancak tekrarlayan taşları olan, bilateral veya koraliform taş taşıyan, "
                "tek böbrekli olan, çocukluk çağında taş başlatan veya sistemik hastalığı (bağırsak rezeksiyonu, sarkoidoz vb.) "
                "bulunan 'yüksek riskli' hastalarda '24 saatlik idrar analizi' zorunludur. İdrar analizi taş çıkarıldıktan "
                "ve hasta olağan beslenme ve aktivite düzenine döndükten en az 4-6 hafta sonra yapılmalıdır. Analizde hacim, "
                "pH, kalsiyum, oksalat, sitrat, ürik asit, sodyum, potasyum, magnezyum ve kreatinin düzeyleri ölçülür."
            ),
            "elements": [
                make_before_after(
                    "24 Saatlik İdrar Analizinin Zamanlaması",
                    "Akut Kolik ve Girişim Sırasında İdrar Toplama",
                    "Ağrı stresi, kontrast madde ve diyet kısıtlaması nedeniyle yanıltıcı sonuçlar verir; metabolik profili yansıtmaz.",
                    "Taşsız Dönemde (Taştan 4-6 Hafta Sonra) İdrar Toplama",
                    "Hasta normal beslenme ve iş hayatındadır; bazal litogenik biyokimyasal risk faktörlerini kusursuz yansıtır.",
                    "24 saatlik metabolik idrar değerlendirmesi mutlaka hastanın olağan yaşam döngüsünde yapılmalıdır."
                ),
                make_active_recall(
                    "Yüksek riskli bir taş hastasında 24 saatlik idrar analizi taşın düşürülmesinden veya tedavisinden en az kaç hafta sonra yapılmalıdır?",
                    "En az dört ila altı hafta sonra yapılmalıdır.",
                    "Dört haftalık dinlenme aralığı"
                )
            ]
        },
        # Slayt 99
        {
            "slideNumber": 99,
            "title": "Acil Durumlar: Obstrüktif Piyelonefrit ve Ürosepsis",
            "content": (
                "Ürolitiyaziste acil cerrahi drenaj gerektiren en kritik ve ölümcül klinik tablo 'enfekte hidronefroz' "
                "(obstrüktif taş ile birlikte idrar yolu enfeksiyonu) durumudur. Obstrüksiyonun arkasında hapsolan idrar "
                "yüksek basınçlı bir apse poşu gibi davranır; bakteriler ve endotoksinler pelvivenöz ve pelvilenfatik reflü "
                "ile dakikalar içinde kana karışarak septik şoka yol açar. Yan ağrısı olan bir taş hastasında ateş (>38°C), "
                "titreme, taşikardi veya hipotansiyon saptandığında bu durum acil bir ürolojik tablodur. Kesinlikle taşa "
                "yönelik litotripsi veya cerrahi manipülasyon yapılmamalı; derhal retrograd üreteral stent (Double-J) veya "
                "perkütan nefrostomi ile böbrek acilen dekomprese edilmelidir."
            ),
            "elements": [
                make_causal_chain(
                    "Obstrüktif Taştan Ürosepsise Uzanan Ölümcül Yol",
                    [
                        "1. Mekanik Obstrüksiyon: Üreter taşının toplayıcı sistemde idrar çıkışını tıkaması",
                        "2. İntrapelvik Basınç Artışı: Hidronefroz ile birlikte renal pelvis içi hidrostatik basıncın yükselmesi",
                        "3. Bakteriyel Proliferasyon: Stazdaki idrarda bakterilerin kontrolsüz çoğalması",
                        "4. Pelvivenöz Reflü: Basınç etkisiyle bakterilerin ve endotoksinlerin doğrudan kan dolaşımına sızması",
                        "5. Septik Şok: Sistemik hipotansiyon, çoklu organ yetmezliği ve acil drenaj ihtiyacı"
                    ]
                ),
                make_cloze(
                    "Taşa bağlı üriner obstrüksiyon ile yüksek ateşin birlikte görüldüğü enfekte hidronefrozda ilk hayat kurtarıcı adım acil drenaj işlemidir.",
                    "acil drenaj",
                    "Dekompresyon tüpü veya stent takılması"
                )
            ]
        },
        # Slayt 100 [CHECKPOINT 10]
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Enfeksiyon Taşları, İlaçlar ve Korunma İlkeleri",
            "content": (
                "Bu son bölümde enfeksiyon taşlarını, ilaca bağlı kalkülleri, diyet/farmakolojik korunma ilkelerini ve acil durumları özetledik. "
                "Strüvit taşları Proteus mirabilis gibi üreaz pozitif bakterilerin üreyi hidrolize etmesiyle oluşur; E. coli üreaz negatiftir. "
                "Amonyak oluşumu idrarı aşırı alkalileştirir (pH >7.2); amonyum, magnezyum ve fosfat birleşerek koraliform (staghorn) taşlar yapar. "
                "İndinavir doğrudan çöken radyolüsen ilaç taşıdır; topiramat ve asetazolamid ise hipositratüri yaparak kalsiyum fosfat taşını tetikler. "
                "Diyet korumasında 2.5 L üzeri idrar hacmi esastır; diyet kalsiyumu kısıtlanmamalı (oksalat emilimi artar), tuz ve hayvansal protein azaltılmalıdır. "
                "Tiyazid diüretikler hiperkalsiüriyi düzeltir, allopurinol ürik asidi baskılar, potasyum sitrat hipositratüriyi çözer. "
                "Ateş ve obstrüksiyon varlığı (obstrüktif piyelonefrit) acil dekompresyon (Double-J stent veya nefrostomi) gerektiren hayatı tehdit eden bir tablodur."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp10-fc01",
                    "front": "Üreaz üreterek magnezyum amonyum fosfat (strüvit) taşlarının gelişimine yol açan en yaygın bakteriyel patojen hangisidir?",
                    "back": "Proteus mirabilis patojenidir.",
                    "hint": "Enfeksiyon kalkülünün primer mikrobiyal kaynağı"
                },
                {
                    "id": "k1-27-cp10-fc02",
                    "front": "HIV tedavisinde kullanılan ve idrarda doğrudan kristalleşerek radyolüsen taş oluşturan proteaz inhibitörü ilaç nedir?",
                    "back": "İndinavir etken maddesidir.",
                    "hint": "Antiviral proteaz blokörü ilaç"
                },
                {
                    "id": "k1-27-cp10-fc03",
                    "front": "Üreteral taş obstrüksiyonuna ateş ve titremenin eşlik ettiği obstrüktif piyelonefrit tablosunda yapılması gereken ilk hayat kurtarıcı müdahale nedir?",
                    "back": "Acil drenaj müdahalesidir.",
                    "hint": "Dekompresyon stent veya tüp uygulaması"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 10 Özet Tablosu: Korunma ve Acil Tedavi Protokolü",
                    ["Klinik Durum", "Primer Terapötik Yaklaşım", "Kritik Hedef / Kural"],
                    [
                        {
                            "cells": ["İdiyopatik Hiperkalsiüri", "Tiyazid diüretik + Tuz kısıtlaması", "İdrar kalsiyumunu düşürme"],
                            "hiddenIndex": 1,
                            "hint": "Hiperkalsiüri medikal ilacı"
                        },
                        {
                            "cells": ["Enfekte Obstrüksiyon", "Acil DJ stent veya perkütan nefrostomi", "Sepsis gelişimini önleme"],
                            "hiddenIndex": 1,
                            "hint": "Üriner yolun acil dekompresyonu"
                        }
                    ]
                )
            ]
        }
    ]
