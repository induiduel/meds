# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
(Dr. Öğr. Üyesi Fahrettin Şamil Uysal - Üroloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_27_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar senaryoları) ek ögeleri (21 adet)."""
    return {
        4: make_branching_logic(
            "48 yaşında dökümhane işçisi, çalışma saatlerinde aşırı terleme sonrası akşam saatlerinde sol yan ağrısı ve mikroskobik hematüri ile başvuruyor. Günlük idrar çıkışı 700 mL olarak hesaplanıyor.",
            "Dehidratasyona bağlı bu akut tabloda litogenezi durdurmak ve kristalizasyonu engellemek için derhal yapılması gereken ilk müdahale ne olmalıdır?",
            [
                {
                    "text": "İntravenöz/oral sıvı takviyesi ile idrar çıkışını hızla artırıp idrar dansitesini ve süpersatürasyonu düşürmek",
                    "isCorrect": True,
                    "explanation": "Doğrudur; akut dehidratasyonda acil hidrasyon çözünen tuzların konsantrasyonunu Ksp altına çeker."
                },
                {
                    "text": "Hastaya derhal yüksek doz kalsiyum glukonat infüzyonu başlamak",
                    "isCorrect": False,
                    "explanation": "Kalsiyum yükü idrar kalsiyumunu fırlatarak kalsiyum taşı riskini daha da artırır."
                },
                {
                    "text": "Böbrek tübüllerini asitleştirmek için amonyum klorür vermek",
                    "isCorrect": False,
                    "explanation": "Asitleştirme ürik asit çökmesini tetikler."
                }
            ]
        ),
        8: make_branching_logic(
            "6 yaşında erkek çocukta ultrasonografide bilateral böbrek toplayıcı sistemlerinde multipl kalsifiye taşlar ve nefrokalsinozis saptanıyor. 24 saatlik idrar analizinde oksalat atılımı 120 mg/gün (aşırı yüksek) ölçülüyor.",
            "Pediatrik nefrokalsinozis ile seyreden bu olguda genetik tarama ve kesin tanı için ilk olarak hangi patoloji düşünülmelidir?",
            [
                {
                    "text": "Karaciğer peroksizomal AGXT gen mutasyonuna bağlı Primer Hiperoksalüri Tip 1",
                    "isCorrect": True,
                    "explanation": "Doğrudur; çocuklukta masif hiperoksalüri ve nefrokalsinozis Tip 1 PH için klasiktir."
                },
                {
                    "text": "Yaşlılık dönemi benign prostat hiperplazisi",
                    "isCorrect": False,
                    "explanation": "6 yaşındaki çocukta BPH söz konusu olamaz."
                },
                {
                    "text": "İndinavir kullanımına bağlı ilaç nefropatisi",
                    "isCorrect": False,
                    "explanation": "İndinavir oksalat atılımını 120 mg/gün'e çıkarmaz."
                }
            ]
        ),
        12: make_branching_logic(
            "Spontan düşürülen siyah renkli, son derece sert taşın FTIR analizinde %95 kalsiyum oksalat monohidrat (whewellit) saptanıyor.",
            "Bu mineralojik bileşime sahip hastanın metabolik etiyolojisinde primer olarak hangi bozukluk araştırılmalıdır?",
            [
                {
                    "text": "Diyet veya enterik emilim kaynaklı hiperoksalüri tablosu",
                    "isCorrect": True,
                    "explanation": "Doğrudur; whewellit monohidrat formu primer olarak oksalat fazlalığı ile tetiklenir."
                },
                {
                    "text": "İdrarda aşırı alkali pH ve Proteus mirabilis enfeksiyonu",
                    "isCorrect": False,
                    "explanation": "Alkali idrar ve Proteus strüvit taşı yapar, whewellit yapmaz."
                },
                {
                    "text": "SLC3A1 gen mutasyonuna bağlı sistinüri",
                    "isCorrect": False,
                    "explanation": "Sistinüri sistin taşı oluşturur, whewellit bir kalsiyum oksalat formudur."
                }
            ]
        ),
        14: make_branching_logic(
            "Böbrek pelvisinde 1.5 cm taş saptanan 32 yaşında hastaya ESWL uygulanıyor; ancak 3 seans şok dalgaya rağmen taşta hiçbir kırılma veya parçalanma gözlenmiyor. Taş analizinde bruşit minerali saptanıyor.",
            "Bruşit taşlarının şok dalga litotripsiye (ESWL) bu yüksek direnci karşısında bir sonraki en uygun girişim ne olmalıdır?",
            [
                {
                    "text": "ESWL sonlandırılmalı; perkütan nefrolitotomi (PCNL) veya fleksibl üreterorenoskopi (RIRS) ile intrakorporeal lazer litotripsi planlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; bruşit ESWL'ye en dirençli mineraldir, endoürolojik cerrahi gerekir."
                },
                {
                    "text": "ESWL seans sayısı 10'a tamamlanarak aynı enerjiyle devam edilmelidir.",
                    "isCorrect": False,
                    "explanation": "Dirençli taşa kontrolsüz ESWL böbrek parankim hematomuna yol açar."
                },
                {
                    "text": "Oral potasyum sitrat verilerek taşın birkaç saatte erimesi beklenmelidir.",
                    "isCorrect": False,
                    "explanation": "Bruşit kalsiyum fosfattır, alkalinizasyon ile erimez."
                }
            ]
        ),
        16: make_branching_logic(
            "Gut hastalığı ve metabolik sendromu olan 55 yaşında obez erkek hastanın idrar pH'ı daima 5.0 ölçülüyor. DÜSG'de görünmeyen ancak BT'de 12 mm taş saptanan hastada tanı ürik asit taşı olarak kesinleşiyor.",
            "Bu hastada taşın oluşumunu tetikleyen en kritik biyokimyasal mekanizma nedir?",
            [
                {
                    "text": "İdrar pH'ının ürik asit pKa değeri olan 5.35'in altında kalarak çözünmeyen serbest ürik aside dönüşmesidir.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; pH 5.35'in altına indiğinde ürik asit çözünmez ve hızla kristalleşir."
                },
                {
                    "text": "İdrarın aşırı alkali olması nedeniyle amonyum üratın çökmesidir.",
                    "isCorrect": False,
                    "explanation": "İdrar pH'ı 5.0'dır, alkali değil aşırı asidiktir."
                },
                {
                    "text": "Hastada aşırı kemik resorpsiyonuna bağlı hiperkalsiüri gelişmesidir.",
                    "isCorrect": False,
                    "explanation": "Ürik asit taşı kalsiyum metabolizmasıyla doğrudan ilişkili değildir."
                }
            ]
        ),
        22: make_branching_logic(
            "Sol böbrek alt kaliksinde 8 mm asemptomatik taşı olan 40 yaşında hastanın infundibulopelvik açısı 35 derece (dar) ve infundibulum uzunluğu 3 cm (uzun) ölçülüyor.",
            "Bu anatomik özellikler ışığında hastada taşın spontan pasajı ve temizlenmesi hakkında ne söylenebilir?",
            [
                {
                    "text": "Dar açı ve uzun boyun nedeniyle taşın yerçekimi aleyhine dökülmesi zordur; ESWL başarısı düşük olup endoürolojik yaklaşım gerekebilir.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; akut infundibulopelvik açı fragman dökülmesini fiziksel olarak engeller."
                },
                {
                    "text": "Yerçekimi alt pol taşlarını yukarı üretere fırlattığından spontan düşme oranı %100'dür.",
                    "isCorrect": False,
                    "explanation": "Yerçekimi taşın alt kaliks dibinde kalmasına yol açar."
                },
                {
                    "text": "Taş derhal mesaneye kendiliğinden geçer.",
                    "isCorrect": False,
                    "explanation": "Alt pol anatomisi dökülmeye elverişli değildir."
                }
            ]
        ),
        24: make_branching_logic(
            "72 yaşında benign prostat hiperplazisine (BPH) bağlı mesane çıkım obstrüksiyonu olan erkek hastada mesane içinde 3 cm çapında tek bir sert kalsifiye kitle saptanıyor.",
            "Bu sekonder mesane taşının tedavisinde ve nüksünün önlenmesinde temel cerrahi strateji ne olmalıdır?",
            [
                {
                    "text": "Mesane taşı sistolitotripsi ile kırılıp temizlenmeli ve eş zamanlı olarak BPH'ya yönelik prostat rezeksiyonu (TURP) yapılarak staz ortadan kaldırılmalıdır.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; primer obstrüksiyon düzeltilmezse taş hızla tekrarlar."
                },
                {
                    "text": "Yalnızca taş kırılmalı, prostata kesinlikle dokunulmamalıdır.",
                    "isCorrect": False,
                    "explanation": "Staz devam ettiği sürece nüks kaçınılmazdır."
                },
                {
                    "text": "Hastaya ömür boyu üreaz inhibitörü antibiyotik verilmelidir.",
                    "isCorrect": False,
                    "explanation": "Obstrüksiyon cerrahi bir sorundur, antibiyotikle BPH düzelmez."
                }
            ]
        ),
        26: make_branching_logic(
            "Direkt grafide sağ renal lojda silik buzlu cam dansitesinde zayıf radyoopak kitle izlenen genç hastanın idrar mikroskopisinde hekzagonal kristaller saptanıyor.",
            "Bu radyolojik ve mikroskobik bulgular hangi kalıtsal hastalığın taşını işaret eder?",
            [
                {
                    "text": "Sistin amino asidindeki kükürt atomlarına bağlı zayıf opaklık veren sistinüri taşını işaret eder.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; sistin kükürt nedeniyle zayıf opaktır ve altıgen kristaller oluşturur."
                },
                {
                    "text": "Saf kalsiyum fosfat yapısındaki bruşit taşını işaret eder.",
                    "isCorrect": False,
                    "explanation": "Bruşit belirgin radyoopaktır ve çubuksu kristaller yapar."
                },
                {
                    "text": "Saf ürik asit taşını işaret eder.",
                    "isCorrect": False,
                    "explanation": "Saf ürik asit tamamen radyolüsendir, zayıf opak değildir."
                }
            ]
        ),
        32: make_branching_logic(
            "Bir taş hastasının 24 saatlik idrar analizinde kalsiyum oksalat bağıl süpersatürasyonu (CaOx SS) 0.7 (birden küçük) olarak rapor ediliyor.",
            "Bu termodinamik veriye göre idrarın kalsiyum oksalat açısından durumu ve taş riski nasıl yorumlanmalıdır?",
            [
                {
                    "text": "İdrar doymamış bölgededir; yeni kristal oluşamaz ve mevcut küçük kristaller çözünme eğilimindedir.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; SS < 1 doymamış fazı temsil eder ve koruyucudur."
                },
                {
                    "text": "İdrar kararsız fazdadır ve acil de novo nükleasyon beklenir.",
                    "isCorrect": False,
                    "explanation": "Kararsız faz için SS > ULM olmalıdır."
                },
                {
                    "text": "İdrarda protein eksikliği nedeniyle böbrek iflas etmiştir.",
                    "isCorrect": False,
                    "explanation": "SS < 1 normal ve arzu edilen bir çözünürlük fazıdır."
                }
            ]
        ),
        34: make_branching_logic(
            "Bir solüsyonda kalsiyum ve oksalat konsantrasyonu metastabil bölge sınırları içinde (1.0 < SS < ULM) ölçülüyor. Ortamda hiçbir yabancı çekirdek, epitel veya nidus bulunmuyor.",
            "Bu koşullar altında solüsyonda spontan olarak yeni bir kristal nükleusu oluşabilir mi?",
            [
                {
                    "text": "Hayır; metastabil bölgede aktivasyon enerjisi yüksek olduğundan nidus olmaksızın spontan nükleasyon gerçekleşemez.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; metastabil bölge heterojen nükleasyon için yabancı tohum gerektirir."
                },
                {
                    "text": "Evet; metastabil bölgede tüm iyonlar saniyeler içinde patlayarak homojen çöker.",
                    "isCorrect": False,
                    "explanation": "Homojen nükleasyon metastabil değil kararsız bölgede görülür."
                },
                {
                    "text": "Evet; ancak sadece güneş ışığı altında kristalleşebilir.",
                    "isCorrect": False,
                    "explanation": "Işık in vivo biyolojik nükleasyonun belirleyicisi değildir."
                }
            ]
        ),
        36: make_branching_logic(
            "Aşırı sıvı kaybeden maraton koşucusunda idrar konsantrasyonu aniden metastabilitenin üst sınırını (ULM) aşıyor.",
            "Kararsız bölgeye geçen bu idrarda meydana gelen kristalizasyon tipi hangisidir?",
            [
                {
                    "text": "Yabancı yüzeye ihtiyaç duymayan kendiliğinden homojen çekirdeklenme",
                    "isCorrect": True,
                    "explanation": "Doğrudur; ULM aşıldığında aşırı termodinamik enerji homojen nükleasyon başlatır."
                },
                {
                    "text": "Yalnızca bakteriyel biyofilme yapışan sekonder litogenez",
                    "isCorrect": False,
                    "explanation": "Homojen nükleasyon steril ve yabancı yüzeyden bağımsızdır."
                },
                {
                    "text": "Tübüllerin genişleyerek kristali emmesi",
                    "isCorrect": False,
                    "explanation": "Tübüller aşırı kristali ememez, lümen tıkanır."
                }
            ]
        ),
        42: make_branching_logic(
            "Tübüler akım hızı yüksek olan bir nefronda tek bir kalsiyum oksalat kristalinin difüzyonla büyümesi saatler sürerken, hastada dakikalar içinde akut tübüler obstrüksiyon gelişiyor.",
            "Bu hızlı obstrüksiyon tablosunu açıklayan temel fiziksel basamak nedir?",
            [
                {
                    "text": "Çok sayıda kristalin elektrostatik ve makromoleküler kuvvetlerle hızla kümelendiği kristal agregasyonu",
                    "isCorrect": True,
                    "explanation": "Doğrudur; agregasyon saniyeler içinde kitleyi büyüterek lümeni tıkar."
                },
                {
                    "text": "Böbrek hücrelerinin tüm su içeriğini bir anda kaybetmesi",
                    "isCorrect": False,
                    "explanation": "Hücre su kaybı mekanik kristal kitlesini tek başına açıklamaz."
                },
                {
                    "text": "Kalsiyumun nükleer füzyonla demire dönüşmesi",
                    "isCorrect": False,
                    "explanation": "Biyolojik sistemlerde transmutasyon olmaz."
                }
            ]
        ),
        44: make_branching_logic(
            "Hiperoksalüriye bağlı tübüler epitel hasarı gelişen bir deneysel modelde, soyulmuş hücre yüzeylerinde kristal adezyonunun patolojik olarak arttığı saptanıyor.",
            "Bu tablo litogenezin partikül tutulma modellerinden hangisinin temel mekanizmasını oluşturur?",
            [
                {
                    "text": "Epitelyal adezyonun birincil rol oynadığı Sabit Partikül Hipotezi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; hasarlı epitele kristal yapışması sabit partikül modelidir."
                },
                {
                    "text": "Yalnızca partikül büyüklüğüne odaklanan Serbest Partikül Hipotezi",
                    "isCorrect": False,
                    "explanation": "Serbest partikül modeli epitele yapışmaya ihtiyaç duymaz, lüminal sıkışmayı savunur."
                },
                {
                    "text": "Bakteriyel plazmid aktarımı hipotezi",
                    "isCorrect": False,
                    "explanation": "Plazmid antibiyotik direnciyle ilgilidir."
                }
            ]
        ),
        52: make_branching_logic(
            "Tekrarlayan kalsiyum taşı olan hastada potasyum sitrat tedavisi planlanıyor. Hasta sitratın taşları nasıl engellediğini soruyor.",
            "Sitratın en önemli kalsiyum bağlayıcı fizyopatolojik etkisi hastaya nasıl açıklanmalıdır?",
            [
                {
                    "text": "Sitrat serbest kalsiyum ile son derece çözünür bir kompleks oluşturarak kalsiyum oksalat süpersatürasyonunu doğrudan düşürür.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; kalsiyum sitrat kompleksi kalsiyum oksalat çökelmesini önler."
                },
                {
                    "text": "Sitrat böbrekleri tamamen dondurarak idrar üretimini durdurur.",
                    "isCorrect": False,
                    "explanation": "Sitrat fizyolojik bir anyondur, idrar üretimini durdurmaz."
                },
                {
                    "text": "Sitrat kandaki tüm kalsiyumu yok eder.",
                    "isCorrect": False,
                    "explanation": "Sitrat sistemik hipokalsemi yapmaz, idrarda şelasyon yapar."
                }
            ]
        ),
        54: make_branching_logic(
            "Nefrokalsin proteini izole edilen idiyopatik taş hastasında, proteinin kalsiyum oksalat agregasyonunu engelleyemediği görülüyor.",
            "Bu patolojik fonksiyonsuzluğun altında yatan moleküler defekt nedir?",
            [
                {
                    "text": "Proteinin yapısındaki gama-karboksiglutamik asit (Gla) kalıntılarının eksikliği",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Gla kalıntıları eksik C ve D izoformları agregasyon inhibitör gücünü kaybeder."
                },
                {
                    "text": "Proteinin saf kolesterole dönüşmesi",
                    "isCorrect": False,
                    "explanation": "Nefrokalsin bir glikoproteindir, lipid değildir."
                },
                {
                    "text": "Tüm amino asitlerin glikoza dönüşmesi",
                    "isCorrect": False,
                    "explanation": "Yapısal Gla posttranslasyonel modifikasyon defektidir."
                }
            ]
        ),
        62: make_branching_logic(
            "Endoürolojik biyopside renal papillada Henle kulpu bazal membranı çevresinde subepitelyal kalsiyum apatit kristalleri izleniyor.",
            "Bu patolojik oluşum literatürde hangi isimle anılır ve hangi taş tipinin beşiğidir?",
            [
                {
                    "text": "Randall plağıdır ve idiyopatik kalsiyum oksalat taşlarının başlangıç yuvasıdır.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Randall plağı apatitten doğar ve CaOx taşlarına zemin hazırlar."
                },
                {
                    "text": "Aschoff nodülüdür ve romatizmal karditin böbrek bulgusudur.",
                    "isCorrect": False,
                    "explanation": "Aschoff nodülü miyokardiyal romatizmal granülomdur."
                },
                {
                    "text": "Mallory cisimciğidir ve alkolik hepatitin böbrek yansımasıdır.",
                    "isCorrect": False,
                    "explanation": "Mallory-Denk cisimcikleri hepatosit içi sitokeratin yığınlarıdır."
                }
            ]
        ),
        72: make_branching_logic(
            "24 saatlik idrar kalsiyumu 420 mg/gün saptanan hastada, kalsiyum kısıtlı diyet verildiğinde idrar kalsiyumu 180 mg/gün seviyesine geriliyor. Serum PTH ve kalsiyum normaldir.",
            "Bu hiperkalsiüri tablosu nasıl sınıflandırılmalıdır?",
            [
                {
                    "text": "Diyete bağımlı Tip II Absorptif Hiperkalsiüri",
                    "isCorrect": True,
                    "explanation": "Doğrudur; diyet kısıtlamasıyla normale dönen emilim kusuru Tip II absorptiftir."
                },
                {
                    "text": "Primer otonom hiperparatiroidizm",
                    "isCorrect": False,
                    "explanation": "Primer hiperparatiroidide PTH ve serum kalsiyumu yüksek olur."
                },
                {
                    "text": "Renal tübüler kaçak hiperkalsiürisi",
                    "isCorrect": False,
                    "explanation": "Renal kaçakta açlıkta da idrar kalsiyumu yüksek kalır ve sekonder PTH artar."
                }
            ]
        ),
        74: make_branching_logic(
            "Bilateral böbrek taşları olan 58 yaşında postmenopozal kadın hastanın laboratuvarında serum kalsiyumu 11.4 mg/dL (yüksek), 24 saatlik idrar kalsiyumu 380 mg/gün (yüksek) ve intakt PTH 145 pg/mL (belirgin yüksek) ölçülüyor.",
            "Bu klinik tablonun altta yatan primer nedeni ve kesin küratif tedavisi nedir?",
            [
                {
                    "text": "Soliter paratiroid adenomuna bağlı primer hiperparatiroidi; paratiroidektomi kesin tedavidir.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; yüksek kalsiyum + yüksek PTH primer hiperparatiroidiyi kanıtlar."
                },
                {
                    "text": "Aşırı süt içilmesine bağlı süt-alkali sendromu; süt kısıtlaması yeterlidir.",
                    "isCorrect": False,
                    "explanation": "Süt-alkali sendromunda PTH baskılı olur, burada PTH yüksektir."
                },
                {
                    "text": "Sarkoidoza bağlı kontrolsüz D vitamini aktivasyonu",
                    "isCorrect": False,
                    "explanation": "Sarkoidozda PTH baskılanır (düşük olur)."
                }
            ]
        ),
        78: make_branching_logic(
            "Crohn hastalığı nedeniyle ileal rezeksiyon geçiren hastada 24 saatlik idrar oksalat atılımı 85 mg/gün (yüksek) ölçülüyor. Kalsiyum oksalat taşları tekrarlıyor.",
            "Bu hastada enterik hiperoksalüriyi azaltmak için yemeklerle birlikte verilebilecek en rasyonel destek nedir?",
            [
                {
                    "text": "Yemeklerle birlikte kalsiyum sitrat veya kalsiyum karbonat verilerek bağırsaktaki serbest oksalatın bağlanıp dışkıyla atılması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; yemekle alınan kalsiyum bağırsakta oksalatı bağlayarak kolonik emilimini önler."
                },
                {
                    "text": "Yemeklerle yüksek doz saf oksalat tozu verilmesi",
                    "isCorrect": False,
                    "explanation": "Oksalat vermek taş krizini ölümcül hale getirir."
                },
                {
                    "text": "Tüm yağların kısıtlanmadan günde 200 grama çıkarılması",
                    "isCorrect": False,
                    "explanation": "Yağ artışı sabunlaşmayı ve serbest oksalatı daha da artırır."
                }
            ]
        ),
        86: make_branching_logic(
            "Sistinüri tanısı konan 19 yaşında hastada günlük sistin atılımı 800 mg olarak ölçülüyor. İdrar hacmi 2 litre ve idrar pH'ı 6.0'dır.",
            "Bu hastada sistin taşlaşmasını durdurmak için atılması gereken ilk basamak tedavi adımları ne olmalıdır?",
            [
                {
                    "text": "Günlük idrar hacmini 3.5 litrenin üzerine çıkaracak hidrasyon sağlanmalı, potasyum sitrat ile idrar pH'ı 7.5 üzerine çekilmeli ve tuz kısıtlanmalıdır.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; sistin çözünürlüğü pH >7.5 ve yüksek hacimde belirgin artar."
                },
                {
                    "text": "İdrarı asitleştirmek için yüksek doz C vitamini başlanmalıdır.",
                    "isCorrect": False,
                    "explanation": "Asidik idrarda sistin anında taşlaşır."
                },
                {
                    "text": "Sistin amino asidini yok etmek için kemoterapi verilmelidir.",
                    "isCorrect": False,
                    "explanation": "Sistinüri malignite değildir, kemoterapi endikasyonu yoktur."
                }
            ]
        ),
        92: make_branching_logic(
            "İdrar tahlilinde pH 8.2 saptanan ve idrar kültüründe 100.000 CFU/mL Proteus mirabilis üreyen hastanın böbrek grafisinde staghorn kalkül izleniyor.",
            "Bu patolojide idrarın bu derece aşırı alkali olmasının temel biyokimyasal nedeni nedir?",
            [
                {
                    "text": "Bakteriyel üreazın üreyi amonyağa hidrolize etmesi ve amonyağın proton bağlayarak pH'ı yükseltmesidir.",
                    "isCorrect": True,
                    "explanation": "Doğrudur; üreaz aktivitesi ortamdaki protonları tüketerek idrarı bazikleştirir."
                },
                {
                    "text": "Hastanın böbrek tübüllerinden masif bikarbonat salgılaması",
                    "isCorrect": False,
                    "explanation": "Böbrek bazikleştirmez; bakteriyel amonyak reaksiyonu alkalileştirir."
                },
                {
                    "text": "Proteus bakterisinin idrara saf sodyum hidroksit pompalaması",
                    "isCorrect": False,
                    "explanation": "Bakteriler serbest NaOH pompalamaz, üreaz ile amonyak üretir."
                }
            ]
        )
    }

def get_extra_micro_quizzes():
    """Micro quiz ek ögeleri (14 adet)."""
    return {
        5: make_micro_quiz(
            "Metabolik sendromlu hastalarda renal tübüler amonyogenez kusuruna yol açan primer hücresel anormallik nedir?",
            [
                {
                    "text": "Proksimal tübül hücrelerinde insülin direnci ve lipotoksisite",
                    "isCorrect": True,
                    "explanation": "Doğrudur; insülin direnci tübüler amonyak sentezini bozar."
                },
                {
                    "text": "Glomerül bazal membranının aşırı kalınlaşması",
                    "isCorrect": False,
                    "explanation": "Membran kalınlaşması nefropati bulgusudur, amonyogenez proksimal tübüldedir."
                },
                {
                    "text": "Medullada aşırı kalsiyum birikimi",
                    "isCorrect": False,
                    "explanation": "Kalsiyum birikimi amonyogenezi doğrudan primer olarak bozmaz."
                },
                {
                    "text": "Mesane kapasitesinin küçülmesi",
                    "isCorrect": False,
                    "explanation": "Mesane depolama organıdır, renal tübüler sentezle ilişkisi yoktur."
                }
            ],
            "Tübüler insülin direnci amonyum sentezini baskılar."
        ),
        15: make_micro_quiz(
            "Strüvit taşlarının oluşumunda yer alan magnezyum amonyum fosfat bileşiğinin çökebilmesi için idrar ortamının nasıl olması zorunludur?",
            [
                {
                    "text": "Alkali idrar (pH > 7.2) ve yüksek amonyum konsantrasyonu",
                    "isCorrect": True,
                    "explanation": "Doğrudur; strüvit yalnızca alkali ve amonyum zengini ortamda çöker."
                },
                {
                    "text": "Aşırı asidik idrar (pH < 5.0) ve sıfır amonyum",
                    "isCorrect": False,
                    "explanation": "Asidik ortamda strüvit erir, çökelemez."
                },
                {
                    "text": "Mutlak olarak doymamış steril idrar",
                    "isCorrect": False,
                    "explanation": "Strüvit enfeksiyon taşıdır ve süpersatürasyon gerektirir."
                },
                {
                    "text": "Kalsiyumun sıfır olduğu saf tuzlu ortam",
                    "isCorrect": False,
                    "explanation": "Kalsiyum varlığında karbonat apatit de eşlik eder."
                }
            ],
            "Strüvit alkali ve amonyum zengini enfeksiyon ortamının ürünüdür."
        ),
        25: make_micro_quiz(
            "Direkt üriner sistem grafisinde (DÜSG) kalsiyum oksalat taşlarının belirgin beyaz (opak) görünmesini sağlayan fiziksel özellik nedir?",
            [
                {
                    "text": "Kalsiyum atomunun yüksek atom numarası (20) nedeniyle X-ışınlarını kuvvetle absorbe etmesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; kalsiyum yüksek elektron yoğunluğuyla ışını soğurur."
                },
                {
                    "text": "Taşın içinde radyoaktif uranyum atomlarının bulunması",
                    "isCorrect": False,
                    "explanation": "Böbrek taşları uranyum içermez."
                },
                {
                    "text": "Taşın etrafındaki idrarın tamamen siyah ışık yayması",
                    "isCorrect": False,
                    "explanation": "Radyoopasite absorbsiyon farkından kaynaklanır."
                },
                {
                    "text": "Yalnızca taşın dış kabuğundaki bakterilerin parlaması",
                    "isCorrect": False,
                    "explanation": "Bakteriler radyoopasite vermez."
                }
            ],
            "Kalsiyumun atom numarası radyoopasitenin fiziksel temelidir."
        ),
        35: make_micro_quiz(
            "Metastabilitenin üst sınırı (ULM) aşıldığında gerçekleşen homojen çekirdeklenmenin temel özelliği nedir?",
            [
                {
                    "text": "Önceden var olan hiçbir yabancı yüzeye veya çekirdeğe ihtiyaç duymaksızın de novo gerçekleşmesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; homojen çekirdeklenme saf çözeltide spontan başlar."
                },
                {
                    "text": "Daima bakteriyel enfeksiyon zemininde oluşması",
                    "isCorrect": False,
                    "explanation": "Bakteri heterojen bir yüzeydir, homojen nükleasyon değildir."
                },
                {
                    "text": "Yalnızca eksi 10 derece sıcaklıkta görülmesi",
                    "isCorrect": False,
                    "explanation": "Vücut ısısında termodinamik olarak gerçekleşir."
                },
                {
                    "text": "Tüm böbrek fonksiyonlarını saniyeler içinde kalıcı olarak durdurması",
                    "isCorrect": False,
                    "explanation": "Kristalizasyon faz değişimidir, doğrudan anüri nedeni değildir."
                }
            ],
            "Homojen nükleasyon yabancı çekirdeksiz de novo çökelmedir."
        ),
        45: make_micro_quiz(
            "Serbest partikül hipotezine göre kristal agregatlarının toplayıcı kanallarda takılmasına yol açan en dar anatomik filtre noktası neresidir?",
            [
                {
                    "text": "Bellini toplayıcı kanallarının papilla ucundaki ağızları",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Bellini kanalı toplayıcı sistemin en dar çıkış kapısıdır (~100-200 mikron)."
                },
                {
                    "text": "Glomerül Bowman kapsülü boşluğu",
                    "isCorrect": False,
                    "explanation": "Kristal agregasyonu Bowman boşluğunda değil toplayıcı kanallarda oluşur."
                },
                {
                    "text": "Mesane boynu detrusor kası",
                    "isCorrect": False,
                    "explanation": "Mesane boynu çok daha geniştir, serbest partikül hipotezi tübüler seviyededir."
                },
                {
                    "text": "Prostatik üretra lümeni",
                    "isCorrect": False,
                    "explanation": "Böbrek içi mikroobstrüksiyon Bellini kanalı düzeyindedir."
                }
            ],
            "Bellini kanalı lümen çapı serbest partikül hipotezinin kritik tıkaç bölgesidir."
        ),
        55: make_micro_quiz(
            "Osteopontin proteininin kalsiyum taşı oluşumunu engellemedeki en özgül savunma mekanizması hangisidir?",
            [
                {
                    "text": "Hasarlı tübül epitelini örterek kristallerin apikal membrana yapışmasını (adezyonunu) bloke etmesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; osteopontin anti-adherent bir kalkan oluşturur."
                },
                {
                    "text": "Kalsiyum atomlarını parçalayarak potasyuma dönüştürmesi",
                    "isCorrect": False,
                    "explanation": "Biyokimyasal element dönüşümü imkansızdır."
                },
                {
                    "text": "İdrarı aşırı derecede asitleştirerek pH'ı 2.0 yapması",
                    "isCorrect": False,
                    "explanation": "Osteopontin pH'ı bu derece düşürmez."
                },
                {
                    "text": "Böbrek taşlarını lazer gibi eritmesi",
                    "isCorrect": False,
                    "explanation": "Osteopontin bir proteindir, lazer etkisi yoktur."
                }
            ],
            "Osteopontin epitelyal kristal adezyonunu engelleyen kilit moleküldür."
        ),
        65: make_micro_quiz(
            "Distal RTA ve bruşit taşlarında toplayıcı kanal lümenini dolduran Randall Tip 2 lezyonunun adı nedir?",
            [
                {
                    "text": "Bellini kanal tıkacı",
                    "isCorrect": True,
                    "explanation": "Doğrudur; intralüminal toplayıcı kanal kristalleri Bellini tıkacı olarak bilinir."
                },
                {
                    "text": "Bowman kapsül hilusu",
                    "isCorrect": False,
                    "explanation": "Bowman glomerüldedir, tübül tıkacı değildir."
                },
                {
                    "text": "İnterkalar hücre vakuolü",
                    "isCorrect": False,
                    "explanation": "Hücre içi organeldir, intralüminal taş kitlesi değildir."
                },
                {
                    "text": "Podosit ayaksı çıkıntısı",
                    "isCorrect": False,
                    "explanation": "Podosit glomerüler filtrasyon bariyerindedir."
                }
            ],
            "Randall Tip 2 lezyonu Bellini kanal tıkacıdır."
        ),
        75: make_micro_quiz(
            "Primer hiperoksalüri Tip 1 hastalığında karaciğer peroksizomlarında eksik olan enzim hangisidir?",
            [
                {
                    "text": "Alanin:glioksilat aminotransferaz (AGT)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; AGXT geni tarafından kodlanan AGT eksikliği Tip 1 PH nedenidir."
                },
                {
                    "text": "Ksantin oksidaz",
                    "isCorrect": False,
                    "explanation": "Ksantin oksidaz pürin metabolizmasındadır."
                },
                {
                    "text": "Karbonik anhidraz tip 2",
                    "isCorrect": False,
                    "explanation": "Karbonik anhidraz bikarbonat dengesindedir."
                },
                {
                    "text": "Alkalen fosfataz",
                    "isCorrect": False,
                    "explanation": "Alkalen fosfataz kemik ve karaciğer enzim testidir."
                }
            ],
            "Tip 1 Primer Hiperoksalüride AGT enzim kusuru vardır."
        ),
        85: make_micro_quiz(
            "Sistinüri hastalığında renal proksimal tübülde emilimi bozulan amino asit grubu hangisidir?",
            [
                {
                    "text": "Sistin, Ornitin, Lizin, Arjinin (COLA)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; dibazik amino asit transportu bozulur."
                },
                {
                    "text": "Metiyonin, Lösin, İzolösin, Valin",
                    "isCorrect": False,
                    "explanation": "Dallı zincirli ve kükürtlü nötral amino asitlerdir."
                },
                {
                    "text": "Glisin, Alanin, Prolin",
                    "isCorrect": False,
                    "explanation": "İminoglisinüri grubudur, sistinüri değildir."
                },
                {
                    "text": "Fenilalanin, Tirozin",
                    "isCorrect": False,
                    "explanation": "Aromatik amino asitlerdir."
                }
            ],
            "COLA amino asitleri sistinüride taşınamayan gruptur."
        ),
        95: make_micro_quiz(
            "Karbonik anhidraz inhibitörü olan topiramat veya asetazolamid kullanımının yol açtığı en belirgin idrar litogenik bozukluğu nedir?",
            [
                {
                    "text": "Metabolik asidoz zemininde yüksek idrar pH'ı ve şiddetli hipositratüri",
                    "isCorrect": True,
                    "explanation": "Doğrudur; alkali idrarda sitrat tükenir ve kalsiyum fosfat taşları hızla çöker."
                },
                {
                    "text": "İdrarın aşırı asitleşmesi ve ürik asit çökmesi",
                    "isCorrect": False,
                    "explanation": "Bu ilaçlar idrarı asitleştirmez, alkalileştirir."
                },
                {
                    "text": "Saf sistinüri gelişmesi",
                    "isCorrect": False,
                    "explanation": "Sistin genetik hastalıktır, ilaçla oluşmaz."
                },
                {
                    "text": "İdrar hacminin günde 10 litreye çıkması",
                    "isCorrect": False,
                    "explanation": "Bu derece masif poliüri diabetes insipidus bulgusudur."
                }
            ],
            "Karbonik anhidraz inhibisyonu kalsiyum fosfat taşlarını tetikler."
        ),
        97: make_micro_quiz(
            "İdiyopatik hiperkalsiürili kalsiyum taşı hastalarında idrar kalsiyum atılımını yüzde elli azaltan ilk tercih ilaç grubu nedir?",
            [
                {
                    "text": "Tiyazid grubu diüretikler (klortalidon, hidroklorotiyazid)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; distal tübülde kalsiyum reabsorpsiyonunu artırarak kalsiüriyi yarıya indirir."
                },
                {
                    "text": "Furosemid ve loop diüretikleri",
                    "isCorrect": False,
                    "explanation": "Furosemid kalsiyum atılımını artırır (kalsiüretiktir), taşı daha da tetikler."
                },
                {
                    "text": "Yüksek doz kalsiyum tabletleri",
                    "isCorrect": False,
                    "explanation": "Aşırı kalsiyum hiperkalsiüriyi provake eder."
                },
                {
                    "text": "Potasyum klorür infüzyonu",
                    "isCorrect": False,
                    "explanation": "Potasyum klorür asidoz yapabilir ve sitratı düşürebilir."
                }
            ],
            "Tiyazidler hiperkalsiürinin temel farmakolojik tedavisidir."
        ),
        99: make_micro_quiz(
            "Taşa bağlı üriner obstrüksiyona yüksek ateş (>38°C) ve titremenin eşlik ettiği acil tabloda ilk yapılması gereken müdahale nedir?",
            [
                {
                    "text": "Acilen Double-J stent veya perkütan nefrostomi ile böbrek dekompresyonu ve intravenöz antibiyoterapi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; enfekte hidronefrozda acil drenaj hayat kurtarıcıdır."
                },
                {
                    "text": "Hemen açık cerrahi ile böbreğin tamamen çıkarılması",
                    "isCorrect": False,
                    "explanation": "Akut enfeksiyonda dekompresyon yeterlidir, nefrektomi endikasyonu yoktur."
                },
                {
                    "text": "Hastaya bol su içirilip eve gönderilmesi",
                    "isCorrect": False,
                    "explanation": "Enfekte tıkanıklık saatler içinde septik şok ve ölüme yol açar."
                },
                {
                    "text": "Hemen ESWL şok dalga litotripsi uygulanması",
                    "isCorrect": False,
                    "explanation": "Enfekte obstrüksiyonda ESWL bakteriyi kana saçar ve kesinlikle kontrendikedir."
                }
            ],
            "Enfekte obstrüksiyonda acil drenaj mutlak kuraldır."
        ),
        28: make_micro_quiz(
            "Renkli Doppler ultrasonografide taşın arkasında saçılan yüksek frekanslı ses dalgalarının oluşturduğu renkli parlama artefaktının adı nedir?",
            [
                {
                    "text": "Twinkling (parlama) artefaktı",
                    "isCorrect": True,
                    "explanation": "Doğrudur; taş yüzeyindeki akustik yansımalar renkli Doppler'de twinkling oluşturur."
                },
                {
                    "text": "Ayna görüntüsü artefaktı",
                    "isCorrect": False,
                    "explanation": "Ayna artefaktı diyafram arkasında görülür."
                },
                {
                    "text": "Gölge yokluğu etkisi",
                    "isCorrect": False,
                    "explanation": "Taşın arkasında daima akustik gölge vardır."
                },
                {
                    "text": "Sıfır akım fenomeni",
                    "isCorrect": False,
                    "explanation": "Damarsal patolojilerle ilgilidir."
                }
            ],
            "Twinkling artefaktı taş tespitinde son derece yararlıdır."
        ),
        68: make_micro_quiz(
            "At nalı böbrek anomalisinde taş oluşumuna zemin hazırlayan primer anatomik faktör nedir?",
            [
                {
                    "text": "Böbrek alt pollerinin füzyonu sonucu üreterlerin yüksekten çıkması ve idrar stazı gelişmesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; isthmus basısı ve yüksek üreter çıkımı akımı yavaşlatır."
                },
                {
                    "text": "Böbreğin vücuttan dışarı fırlaması",
                    "isCorrect": False,
                    "explanation": "Anatomik bir füzyon anomalisidir."
                },
                {
                    "text": "Kalsiyum kanallarının tamamen kaybolması",
                    "isCorrect": False,
                    "explanation": "Taşın nedeni anatomik stazdır, iyon kanalı yokluğu değildir."
                },
                {
                    "text": "Mesanenin hiç gelişmemiş olması",
                    "isCorrect": False,
                    "explanation": "At nalı böbrek üst üriner sistem anomalisidir."
                }
            ],
            "At nalı böbrekte idrar stazı taş gelişiminin ana motorudur."
        )
    }

def get_extra_causal_chains():
    """Causal chain (nedensellik zinciri) ek ögeleri (14 adet)."""
    return {
        13: make_causal_chain(
            "Hiperkalsiüriden Weddellit Kristalizasyonuna Uzanan Mekanizma",
            [
                "1. Kalsiyum Yükü: Absorptif veya renal kaçak sonucu tübüler kalsiyum konsantrasyonunun tırmanması",
                "2. İyon Aktivite Çarpımı: İdrarda Ca2+ iyonlarının çözünürlük eşiğini aşarak weddellit lehine kayması",
                "3. Zarf Geometrisi: Çift piramidal kalsiyum oksalat dihidrat kristallerinin nükleasyonu",
                "4. Agregasyon: Yüksek kalsiyum ortamında kristallerin birikerek taş nüvesine dönüşmesi"
            ]
        ),
        17: make_causal_chain(
            "APRT Eksikliğinden 2,8-Dihidroksiadenin Taşına Uzanan Biyokimyasal Yol",
            [
                "1. Enzim Yokluğu: Adenin fosforiboziltransferaz (APRT) aktivitesinin otozomal resesif olarak sıfırlanması",
                "2. Adenin Birikimi: Serbest kalan adeninin alternatif yol olan ksantin dehidrogenaza yönelmesi",
                "3. Oksidasyon: Adeninin önce 8-hidroksiadenine, ardından 2,8-DHA'ya oksitlenmesi",
                "4. Kristal Çökmesi: Çözünürlüğü neredeyse sıfır olan 2,8-DHA'nın tübüllerde taşlaşarak böbreği tıkaması"
            ]
        ),
        23: make_causal_chain(
            "Üreter Taşı İmpaksiyonundan Hidronefroza İlerleyen Obstrüksiyon Kaskadı",
            [
                "1. Mekanik Blokaj: Taşın üreterovezikal bileşkeye (UVJ) oturarak lümeni tıkaması",
                "2. Proksimal Basınç: İdrarın birikmesiyle üreter içi hidrostatik basıncın 50-70 mmHg'ye fırlaması",
                "3. Peristaltik Felç: Aşırı gerilen üreter düz kasının hiperperistaltizm sonrası dekompanse olması",
                "4. Pelvikaliseal Ektazi: Renal pelvis ve kalikslerin genişleyerek hidronefroz oluşturması"
            ]
        ),
        33: make_causal_chain(
            "Yetersiz Sıvı Alımından Doymamış Alanın Kaybına Uzanan Fizikokimya",
            [
                "1. Hipovolemi: Günlük su alımının azalması ve medüller hiperozmolalite",
                "2. Konsantre İdrar: 24 saatlik idrar hacminin 1 litrenin altına çakılması",
                "3. İyon Yoğunlaşması: Çözünen kalsiyum ve oksalat iyon konsantrasyonunun Ksp sınırını aşması",
                "4. Süpersatürasyon: Doymamış fazdan metastabil ve kararsız kristal fazına geçiş"
            ]
        ),
        37: make_causal_chain(
            "Hücresel Debris Üzerinde Heterojen Çekirdeklenme Kaskadı",
            [
                "1. Epitel Dökülmesi: İskemi veya toksinle soyulan tübül epitel parçalarının idrara karışması",
                "2. Enerji Düşüşü: Organik membran parçacıklarının serbest yüzey enerjisini sıfıra yaklaştırması",
                "3. Nükleus Yapışması: Kalsiyum ve oksalat iyonlarının bu yabancı yüzeye kenetlenmesi",
                "4. Hızlı Taşlaşma: Ilımlı süpersatürasyonda bile dev taş kristalizasyonunun başlaması"
            ]
        ),
        43: make_causal_chain(
            "Kristal Retansiyonundan Klinik Taşa Uzanan Basamaklar",
            [
                "1. Serbest Mikrokristaller: İdrar lümeninde yüzen küçük kalsiyum oksalat tanecikleri",
                "2. Agregasyon Hızlanması: İnhibitör eksikliğinde kristallerin birbirine yapışarak büyümesi",
                "3. Epitelyal Tutunma: Büyüyen kitlenin apikal membrana yapışarak idrar akımına direnmesi",
                "4. Sürekli Büyüme: İdrardaki yeni iyonların sabitlenen kitleye eklenerek klinik kalküle dönüşmesi"
            ]
        ),
        53: make_causal_chain(
            "Magnezyum Eksikliğinden Kalsiyum Oksalat Süpersatürasyonuna Uzanan Yol",
            [
                "1. Hipomagnezüri: Diyet yetersizliği veya emilim kusuruyla idrar magnezyumunun düşmesi",
                "2. Oksalatın Serbest Kalması: Magnezyum oksalat kompleksinin kurulamaması",
                "3. Kalsiyum Bağlanması: Serbest kalan oksalatın idrardaki kalsiyum ile hızla birleşmesi",
                "4. CaOx Çökelmesi: Metastabil sınırın aşılarak kristal kümelenmesinin hızlanması"
            ]
        ),
        63: make_causal_chain(
            "Henle Kulpu Apatit Mineralizasyonunun Basamakları",
            [
                "1. Medüller Yoğunluk: İnce Henle kulpu çevresinde kalsiyum ve fosfat konsantrasyonunun zirve yapması",
                "2. Matriks Bağlanması: Bazal membrandaki anyonik proteoglikanların kalsiyumu hapsetmesi",
                "3. Apatit Sferülleri: İlk mikroskobik karbonat apatit kristal çekirdeklerinin çökelmesi",
                "4. İnterstisyel Yayılım: Apatitin papilla ürotelyumu altına doğru yayılarak dev plak yapması"
            ]
        ),
        67: make_causal_chain(
            "Vasa Rekta Mikrodolaşım Hasarından Kalsifikasyona İlerleme",
            [
                "1. Vasküler Stres: Hipertansiyon ve lipid peroksidasyonu ile vasa rekta endotelinin zedelenmesi",
                "2. Doku İskemisi: Papilla ucundaki türbülanslı kapiller yatakta mikroenfarktüs gelişmesi",
                "3. Distrofik Kalsifikasyon: İskemik perivasküler dokuda kalsiyum fosfat çökeleğinin birikmesi",
                "4. Randall Plağına Dönüşüm: Kalsifikasyonun interstisyuma yayılarak ürotelyumu aşındırması"
            ]
        ),
        73: make_causal_chain(
            "Renal Kalsiyum Kaçağından Sekonder Hiperparatiroidiye Uzanan Döngü",
            [
                "1. Tübüler Kaçak: Proksimal ve kalın çıkan kolda kalsiyum taşıyıcılarının yetersizliği",
                "2. İdrarla Kayıp: Kalsiyumun kontrolsüz biçimde idrara akması ve hafif serum düşüşü",
                "3. Paratiroid Uyarısı: CaSR reseptörlerinin uyarılmasıyla reaktif PTH salgılanması",
                "4. Kalsitriol Artışı: Böbrekte aktif D vitamini yapılarak bağırsaktan kalsiyum çekilmesi"
            ]
        ),
        77: make_causal_chain(
            "AGXT Gen Defektinden Sistemik Oksalozise Uzanan Ölümcül Yol",
            [
                "1. Genetik Mutasyon: Karaciğer AGXT geninde otozomal resesif inaktive edici kusur",
                "2. Glioksilat Birikimi: Karaciğerde glioksilatın glisine çevrilemeyip oksalata oksitlenmesi",
                "3. Masif Hiperoksalüri: İdrara günde 100 mg üzerinde serbest oksalat dökülmesi",
                "4. Renal Yıkım: Nefrokalsinozis ve tübüler fibrozis ile GFR'nin çökmesi",
                "5. Sistemik Oksalozis: Oksalatın kanda birikerek kalp, kemik ve damarlarda taşlaşması"
            ]
        ),
        83: make_causal_chain(
            "Metabolik Sendromda Amonyogenez Çöküşü ve Asit İdrar Kaskadı",
            [
                "1. İnsülin Direnci: Renal proksimal tübül hücrelerinde insülin sinyalinin iletilememesi",
                "2. Glutamin Yıkım Kusuru: Amonyum sentezinden sorumlu mitokondriyal enzimlerin duraklaması",
                "3. Tamponlama Kaybı: İdrar lümenine amonyum verilememesi sonucu serbest protonların birikmesi",
                "4. Düşük pH: İdrar pH'ının kalıcı olarak 5.2 altına inmesi ve ürik asidin taşlaşması"
            ]
        ),
        87: make_causal_chain(
            "Yüksek Sodyum Alımından Sistinüri Şiddetlenmesine Uzanan Mekanizma",
            [
                "1. Tuz Tüketimi: Diyetle aşırı sodyum klorür alınması ve tübüler filtrasyon artışı",
                "2. Elektrokimyasal Gradyent: Proksimal lümende sodyum yoğunluğunun amino asit kaçağını uyarması",
                "3. Sistin Sekresyonu: İdrarla atılan sistin miktarının 1000 mg/gün seviyesini aşması",
                "4. Taş Agregasyonu: 250 mg/L çözünürlük limitinin kat kat aşılarak kristalleşmenin patlaması"
            ]
        ),
        93: make_causal_chain(
            "Proteus Kolonizasyonundan Geyik Boynuzu Taş Kitlesine Uzanan Süreç",
            [
                "1. Bakteriyel Giriş: Proteus mirabilis suşlarının toplayıcı sisteme yerleşmesi",
                "2. Üreaz Patlaması: Milyonlarca bakterinin üreyi amonyak ve CO2'ye parçalaması",
                "3. Alkali Ortam: İdrar pH'ının 8.0 üzerine fırlayarak strüvit ve karbonat apatit oluşturması",
                "4. Biyofilm Harcı: Bakteriyel eksopolisakkaritlerin kristalleri yapıştırarak kaliksleri doldurması"
            ]
        )
    }

def get_extra_before_afters():
    """Before after slider ek ögeleri (7 adet)."""
    return {
        6: make_before_after(
            "Normal İdrar vs Asidik Diyabetik İdrar Litogenezi",
            "Fizyolojik İdrar (pH 6.0 - 6.5)",
            "Amonyum tamponlaması intakt, ürik asit tamamen çözünür ürat fazında, taş riski minimum.",
            "Diyabetik İdrar (pH < 5.3)",
            "Amonyum yokluğu nedeniyle tamponlanamayan serbest protonlar, ürik asit pKa'sının altında hızla çöken ürisit kristalleri.",
            "İdrar pH'ındaki 1 birimlik düşüş ürik asit çözünürlüğünü 6 kat azaltır."
        ),
        18: make_before_after(
            "Mineral Taşı vs Jelatinöz Matris Taşı",
            "Klasik Kalsiyum Taşı (Mineral Ağırlıklı)",
            "Kuru ağırlığın %97'si inorganik kalsiyum tuzu, aşırı sert, grafide ve tomografide belirgin beyaz gölge.",
            "Matris Taşı (Organik Ağırlıklı)",
            "Kuru ağırlığın %65'i bakteriyel biyofilm ve inflamatuar protein, yumuşak macunsu kıvam, grafide tamamen şeffaf.",
            "Matris taşları enfeksiyonlu kadınlarda sessizce toplayıcı sistemi doldurarak böbreği tüketebilir."
        ),
        38: make_before_after(
            "Rastgele Büyüme vs Epitaktik Kafes Büyümesi",
            "Rastgele Heterojen Çökelme",
            "Kristaller biçimsiz yüzeylere zayıf yapışır, enerji bariyeri tam düşmez, büyüme yavaş ilerler.",
            "Epitaktik Çekirdeklenme (Ürik Asit Üzerinde CaOx)",
            "Ürik asit kristal kafesi ile kalsiyum oksalat kafesi moleküler düzeyde birebir örtüşür; CaOx hızla taşlaşır.",
            "Epitaksi, hiperürikozürili hastalarda neden kalsiyum taşı geliştiğinin kristalografik kanıtıdır."
        ),
        56: make_before_after(
            "Tamm-Horsfall Proteininin Alkali vs Asit Davranışı",
            "Alkali İdrarda THP (İnhibitör)",
            "Monomerik serbest yapı, kristal yüzeylerini kaplayarak birbirine yapışmasını engeller.",
            "Asidik İdrarda THP (Promotör)",
            "Polimerize jel fibrilleri, kristalleri bir ağ gibi yakalayarak dev agregatlara dönüştürür.",
            "İdrar alkalinizasyonu Tamm-Horsfall proteinini promotörden koruyucu inhibitöre çevirir."
        ),
        76: make_before_after(
            "Düşük Kalsiyumlu vs Dengeli Kalsiyumlu Diyet",
            "Hatalı Kalsiyum Kısıtlaması (<400 mg/gün)",
            "Bağırsakta kalsiyum kalmaz, serbest oksalat hızla emilir, idrar oksalatı fırlar, kalsiyum taşı nüks eder.",
            "Dengeli Kalsiyum Alımı (1000-1200 mg/gün)",
            "Kalsiyum bağırsakta oksalatı bağlayarak dışkıyla atar, idrara oksalat geçişi engellenir ve taş önlenir.",
            "Kalsiyum kısıtlaması paradoksal olarak hiperoksalüriyi tetikleyen en büyük klinik yanılgıdır."
        ),
        84: make_before_after(
            "Asidik İdrarda Ürik Asit vs Alkalinize Kemoliz",
            "pH 5.0 (Tedavisiz Durum)",
            "Ürik asit suda çözünmez sert taş kütlesi olarak büyür, renal kolik ve obstrüksiyon atakları yaratır.",
            "pH 6.8 (Potasyum Sitrat ile Kemoliz)",
            "Çözünürlük 15 kat artar, taş yüzeyindeki iyonlar çözünerek sıvı faza geçer, taş cerrahisiz erir.",
            "Ürik asit taşları medikal olarak tamamen eritilebilen tek üriner taş grubudur."
        ),
        94: make_before_after(
            "Radyoopak Kalsiyum Taşı vs İndinavir İlaç Taşı",
            "Kalsiyum Oksalat Taşı",
            "Yüksek atom numarası nedeniyle hem DÜSG'de hem de bilgisayarlı tomografide kemik gibi bembeyaz seçilir.",
            "İndinavir İlaç Taşı",
            "Saf organik molekül olması nedeniyle direkt grafide ve tomografide görünmez, kontrast dolum defektiyle yakalanır.",
            "İndinavir kullanan HIV hastalarında tomografi negatif olsa bile klinik taş obstrüksiyonu dışlanamaz."
        )
    }

def enrich_slides(slides):
    """Slaytlara ek interaktif elemanları ekler ve çeşitliliği dengeler."""
    extra_branching = get_extra_branching()
    extra_quizzes = get_extra_micro_quizzes()
    extra_chains = get_extra_causal_chains()
    extra_bas = get_extra_before_afters()

    for s in slides:
        num = s["slideNumber"]
        els = s.setdefault("interactiveElements", [])

        if num in extra_branching:
            els.append(extra_branching[num])
        if num in extra_quizzes:
            els.append(extra_quizzes[num])
        if num in extra_chains:
            els.append(extra_chains[num])
        if num in extra_bas:
            els.append(extra_bas[num])

    return slides
