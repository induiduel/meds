# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 5: Kristal Büyümesi, Agregasyon, Retansiyon ve Matriks (Slayt 41 - 50)
Checkpoint: Slayt 49
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_5_slides():
    return [
        # Slayt 41
        {
            "slideNumber": 41,
            "title": "Kristal Büyümesi Kinetiği ve Yüzey Reaksiyonları",
            "content": (
                "Çekirdeklenme aşamasını başarıyla tamamlayan kararlı bir kristal tohumu, çözeltideki iyonların kendi yüzeyine "
                "sürekli olarak eklenmesi yoluyla büyüme evresine girer. Kristal büyümesi iki temel basamaktan oluşur: "
                "çözeltideki iyonların kristal yüzeyine doğru difüzyonu ve bu iyonların kristal kafes basamaklarına kimyasal "
                "olarak entegre olduğu yüzey reaksiyonu. Büyüme hızı, çözeltinin aşırı doygunluk derecesi ve sıcaklık ile "
                "doğru orantılıdır. Ancak normal insan nefronunda idrar akım hızı oldukça yüksektir; bir nefron boyunca "
                "sıvı geçiş süresi yalnızca birkaç dakikadır (ortalama 5-10 dakika). Yalnızca kristal büyümesi yoluyla "
                "nefron lümenini tıkayacak boyutta bir partikül oluşması bu kısa sürede fiziksel olarak imkansızdır."
            ),
            "elements": [
                make_active_recall(
                    "Tek bir nefron boyunca sıvı ve kristal transit süresi ortalama kaç dakikadır?",
                    "Beş ila on dakika arasındadır.",
                    "On dakikadan kısa tübüler geçiş"
                ),
                make_cloze(
                    "Nefron boyunca sıvı geçiş süresi yalnızca beş ila on dakika olduğundan tek başına kristal büyümesi obstrüksiyona yetmez.",
                    "beş ila on dakika",
                    "Kısa tübüler akım süresi"
                )
            ]
        },
        # Slayt 42
        {
            "slideNumber": 42,
            "title": "Kristal Agregasyonu (Aglomerasyon): Boyut Artışı",
            "content": (
                "Kristal agregasyonu (aglomerasyon), idrar akımı içinde bağımsız olarak yüzen birden fazla mikrokristalin "
                "çekim kuvvetleri, elektrostatik etkileşimler ve organik makromoleküler köprüler aracılığıyla bir araya "
                "gelerek tek bir büyük konglomerat kitle oluşturmasıdır. Taş oluşumunun en kritik ve en hızlı boyut "
                "artıran basamağı agregasyondur. Tek bir kristalin büyümesi saatler sürerken, agregasyon saniyeler içinde "
                "gerçekleşebilir. Eğer idrarda kristal agregasyonunu engelleyen doğal inhibitörler yetersizse, hızla büyüyen "
                "kristal kümeleri toplayıcı kanalların ve Bellini kanallarının lümen çapını aşarak mekanik olarak takılma "
                "ve obstrüksiyon potansiyeli kazanır."
            ),
            "elements": [
                make_before_after(
                    "Kristal Büyümesi vs Kristal Agregasyonu",
                    "Kristal Büyümesi",
                    "İyonların tek tek kafese eklenmesiyle ilerler, son derece yavaş bir kinetiğe sahiptir, transit süresinde yetersiz kalır.",
                    "Kristal Agregasyonu",
                    "Yüzlerce kristalin aniden birbirine yapışarak dev kitleler oluşturmasıdır; nefron lümenini saniyeler içinde tıkayabilir.",
                    "Taş oluşumunu önlemede agregasyonun inhibe edilmesi büyümenin durdurulmasından kat kat daha etkilidir."
                ),
                make_micro_quiz(
                    "İdrar akım hızı karşısında kristallerin nefron lümenini tıkayabilecek boyuta ulaşmasını sağlayan en hızlı mekanizma hangisidir?",
                    [
                        {
                            "text": "Kristal agregasyonu (aglomerasyon)",
                            "isCorrect": True,
                            "explanation": "Doğrudur; kristallerin kümelenmesi saniyeler içinde hacim artışı sağlayarak takılmaya yol açar."
                        },
                        {
                            "text": "Yalnızca pasif yüzey difüzyonel büyümesi",
                            "isCorrect": False,
                            "explanation": "Difüzyonel büyüme çok yavaştır ve nefron transit süresinde taş yapamaz."
                        },
                        {
                            "text": "İdrarın aniden donarak katılaşması",
                            "isCorrect": False,
                            "explanation": "Vücut içinde donma söz konusu değildir."
                        },
                        {
                            "text": "Paratiroid hormonunun tübülü tıkaması",
                            "isCorrect": False,
                            "explanation": "PTH bir hormondur, mekanik bir tıkaç oluşturmaz."
                        }
                    ],
                    "Agregasyon, taş kitlesinin hızla büyümesini sağlayan en belirleyici fiziksel adımdır."
                )
            ]
        },
        # Slayt 43
        {
            "slideNumber": 43,
            "title": "Kristal Tutulması (Retansiyon): Nihai Eşik",
            "content": (
                "İdrarda kristal nükleasyonu ve agregasyonu ne kadar yoğun olursa olsun, eğer bu partiküller idrar akımıyla "
                "birlikte yıkanıp mesaneye atılırsa (asemptomatik kristalüri) klinik olarak bir taş hastalığı tablosu gelişmez. "
                "Klinik ürolitiyazis gelişiminin mutlak ve son basamağı 'kristal tutulması'dır (retansiyon). Tutulma, partiküllerin "
                "böbrek dokusunda kalıcı hale gelmesini ifade eder. Bu tutulma iki temel mekanizmayla gerçekleşebilir: ya "
                "kristal kümesinin lümen çapını aşarak mekanik olarak bir kanalda sıkışması ya da kristalin tübüler epitel "
                "hücrelerinin yüzeyine biyokimyasal olarak yapışması (adezyon)."
            ),
            "elements": [
                make_cloze(
                    "Klinik taş hastalığının ortaya çıkabilmesi için idrardaki kristallerin böbrekte kalıcı hale geldiği kristal tutulması basamağı şarttır.",
                    "kristal tutulması",
                    "Retansiyon aşaması"
                ),
                make_active_recall(
                    "Kristalüriye sahip sağlıklı bir bireyi taş hastasından ayıran temel fizyopatolojik olay nedir?",
                    "Kristallerin böbrek içinde tutulamayıp idrar akımıyla tamamen dışarı atılmasıdır.",
                    "Serbest partikül temizliği"
                )
            ]
        },
        # Slayt 44
        {
            "slideNumber": 44,
            "title": "Sabit Partikül Hipotezi (Fixed Particle Hypothesis)",
            "content": (
                "Sabit partikül hipotezi, litogenezde kristallerin böbrek içinde kalabilmesi için 'epitelyal adezyon'un "
                "birincil rol oynadığını savunan teoridir. Bu görüşe göre, sağlıklı intakt tübül epitelinde bulunan "
                "koruyucu glikokaliks tabakası kristalleri iter ve yapışmayı önler. Ancak hiperoksalüri, iskemi, serbest "
                "oksijen radikalleri veya toksinler nedeniyle tübül epitelinde hasar meydana geldiğinde, hücre yüzeyinde "
                "kristal bağlayıcı moleküller eksprese olur. Mikrokristaller hasarlı apikal membranlara kuvvetle tutunur "
                "(sabitlenir) ve sürekli geçen idrar akımından iyon toplayarak sabit bir odakta büyümeye devam eder."
            ),
            "elements": [
                make_table(
                    "Litogenezde Partikül Tutulma Hipotezleri",
                    ["Hipotez", "Kritik Belirleyici", "Primer Mekanizma", "Tipik Lokalizasyon"],
                    [
                        {
                            "cells": ["Sabit Partikül Hipotezi", "Epitelyal Adezyon", "Hasarlı hücre zarına kristal yapışması", "Tübül epiteli ve renal papilla"],
                            "hiddenIndex": 1,
                            "hint": "Hücre yüzeyine tutunma süreci"
                        },
                        {
                            "cells": ["Serbest Partikül Hipotezi", "Partikül Büyüklüğü", "Agregatın lümen çapını aşması", "Bellini toplayıcı kanalları ve UPJ"],
                            "hiddenIndex": 1,
                            "hint": "Mekanik lümen tıkanıklığı boyutu"
                        }
                    ]
                ),
                make_active_recall(
                    "Sabit partikül hipotezine göre kristallerin epitele yapışmasını tetikleyen en temel öncül patoloji nedir?",
                    "Tübüler epitel hücre hasarı ve koruyucu yüzey glikokaliksinin bozulmasıdır.",
                    "Hücresel membran zedelenmesi"
                )
            ]
        },
        # Slayt 45
        {
            "slideNumber": 45,
            "title": "Serbest Partikül Hipotezi (Free Particle Hypothesis)",
            "content": (
                "Serbest partikül hipotezi, kristallerin epitele yapışmaya ihtiyaç duymaksızın, yalnızca idrar lümeni içinde "
                "serbestçe yüzerken devasa agregatlar oluşturarak mekanik olarak sıkıştığını ileri sürer. Nefron boyunca "
                "tübül çapları proksimalden distale doğru daralır ve en dar nokta toplayıcı sistemin sonlandığı Bellini kanalı "
                "ağızlarıdır (çapı yaklaşık 100-200 mikrometre). Serbest partikül hipotezine göre, aşırı süpersatüre idrarda "
                "hızlı agregasyon meydana gelirse, kristal kümesinin çapı 200 mikrometreyi aşarak Bellini kanalının lümenini "
                "mekanik olarak tıkar. Tıkaç arkasında idrar göllenir ve kristal kitlesi hızla taşa dönüşür."
            ),
            "elements": [
                make_before_after(
                    "Sabit vs Serbest Partikül Hipotezi Mekanizması",
                    "Sabit Partikül (Adezyon Bağımlı)",
                    "Kristal boyutu küçük olsa bile hasarlı epitele yapışır; akım hızı kristali sürükleyemez ve taş epitel üzerinde büyür.",
                    "Serbest Partikül (Boyut Bağımlı)",
                    "Epitel yapışması gerekmez; serbest yüzen kristal kümesi kanal çapından büyük hale gelerek lümeni mekanik tıkar.",
                    "Klinikte her iki mekanizma farklı taş türlerinde ve anatomik bölgelerde birlikte rol oynayabilir."
                ),
                make_cloze(
                    "Serbest partikül hipotezinde kritik tıkanma noktası toplayıcı sistemin açıldığı Bellini kanalı düzeyidir.",
                    "Bellini kanalı",
                    "Papiller uçtaki toplayıcı kanal ağzı"
                )
            ]
        },
        # Slayt 46
        {
            "slideNumber": 46,
            "title": "Tübüler Epitel Membranında Moleküler Değişimler",
            "content": (
                "Normal sağlıklı renal tübül epitel hücrelerinde membran lipidleri asimetrik olarak dağılmıştır; negatif "
                "yüklü fosfolipidler (özellikle fosfatidilserin) hücrenin iç sitoplazmik yaprağında yer alır. Oksidatif stres, "
                "iskemi veya sitotoksik oksalat maruziyeti geliştiğinde apoptoz ve membran hasarı tetiklenir; flipaz/skramblaz "
                "enzim aktivasyonuyla fosfatidilserin dış membran yüzeyine taşınır (eksternalizasyon). Dışarı açığa çıkan "
                "negatif yüklü fosfatidilserin ve sialik asit grupları, idrardaki pozitif yüklü kalsiyum iyonları ve kalsiyum "
                "oksalat monohidrat kristalleri için son derece yüksek afiniteli bir elektrostatik yapışma odağı yaratır."
            ),
            "elements": [
                make_causal_chain(
                    "Oksidatif Hasardan Epitelyal Kristal Adezyonuna Moleküler Yol",
                    [
                        "1. Hücresel Stres: Hiperoksalüri veya iskemiye bağlı reaktif oksijen türlerinin (ROS) artması",
                        "2. Membran Flip-Flop: Sitoplazmik fosfatidilserinin hücre dış yaprağına eksternalize olması",
                        "3. Negatif Yüzey Yükü: Hasarlı hücre membranında anyonik bağlanma bölgelerinin açığa çıkması",
                        "4. Kristal Adezyonu: Pozitif kalsiyum yüzeyli whewellit kristallerinin bu bölgelere kuvvetle kenetlenmesi",
                        "5. Epitel İçi Alım: Kristalin endositozla hücre içine alınarak inflamasyon ve nekrozu derinleştirmesi"
                    ]
                ),
                make_active_recall(
                    "Tübül hasarı sırasında apikal hücre zarına çıkarak kalsiyum kristallerine elektrostatik yapışma odağı sunan negatif yüklü fosfolipid nedir?",
                    "Fosfatidilserin molekülüdür.",
                    "Apoptozda dışa dönen membran lipidi"
                )
            ]
        },
        # Slayt 47
        {
            "slideNumber": 47,
            "title": "Taş Matrisi: Organik İskeletin Kimyasal Doğası",
            "content": (
                "İdrar taşları saf inorganik mineral kitleleri değildir; tüm taşların bünyesinde inorganik kristalleri "
                "birbirine bağlayan organik bir 'taş matrisi' mevcuttur. Tipik enfeksiyon dışı kalsiyum oksalat taşlarında "
                "organik matris taş kuru ağırlığının yaklaşık %2-3'ünü oluşturur. Matrisin ana bileşenleri proteinler (%65), "
                "mukopolisakkaritler/glikozaminoglikanlar (%10-15), serbest heksozlar ve lipidlerdir. Buna karşılık "
                "kronik üreaz pozitif bakteriyel enfeksiyon zemininde gelişen enfeksiyon ve matris taşlarında bu oran "
                "dramatik biçimde yükselerek taş kitlesinin %65'ine kadar ulaşabilir ve taşı jelatinöz, yumuşak bir kıvama büründürür."
            ),
            "elements": [
                make_table(
                    "Taş Matrisi Oranları ve Klinik Tipleri",
                    ["Taş Kategorisi", "Ortalama Matris Oranı", "Fiziksel Özellik", "Temel Neden"],
                    [
                        {
                            "cells": ["Kalsiyum Oksalat Taşları", "~%2 - 3", "Çok sert, mineral ağırlıklı", "Metabolik süpersatürasyon"],
                            "hiddenIndex": 1,
                            "hint": "Düşük organik içerik yüzdesi"
                        },
                        {
                            "cells": ["Enfeksiyon ve Matris Taşları", "%65'e kadar", "Yumuşak, jelatinöz kitle", "Bakteriyel biyofilm ve proteolitik döküntü"],
                            "hiddenIndex": 1,
                            "hint": "Yüksek organik içerik yüzdesi"
                        }
                    ]
                ),
                make_cloze(
                    "Tipik enfeksiyon dışı kalsiyum taşlarında organik matris içeriği taşın yaklaşık yüzde iki ila üçünü teşkil eder.",
                    "yüzde iki ila üçünü",
                    "Düşük oransal matris payı"
                )
            ]
        },
        # Slayt 48
        {
            "slideNumber": 48,
            "title": "Taş Matrisinin İkili Rolü: Çekirdek mi, İnhibitör mü?",
            "content": (
                "Taş matrisinde yer alan idrar proteinlerinin litogenezdeki rolü biyokimyasal olarak 'ikili' (paradoksal) "
                "bir nitelik taşır. Bir yandan matristeki bazı makromoleküller (albümin, immünoglobulin fragmanları, alfa-1 "
                "mikroglobulin), kristallerin arasına girerek bir 'harç veya yapıştırıcı' gibi davranır, agregasyonu "
                "kolaylaştırır ve heterojen çekirdeklenme için organik bir nidus şablonu sunar. Diğer yandan matris içinde "
                "tespit edilen osteopontin, nefrokalsin ve Tamm-Horsfall proteini gibi moleküller, solübl fazdayken kristal "
                "büyümesini engelleyen güçlü doğal inhibitörlerdir; ancak polimerize olduklarında veya hasarlı epitele "
                "çöktüklerinde promotör (litogenezi destekleyici) bir karaktere bürünürler."
            ),
            "elements": [
                make_before_after(
                    "Matris Proteinlerinin İkili Rolü",
                    "Çözünür Monomerik Fazda İnhibitör",
                    "Kristal yüzeylerine bağlanarak yeni iyonların eklenmesini engeller, kristal agregasyonunu önler ve korur.",
                    "Polimerize veya Çökmüş Fazda Promotör",
                    "İdrardaki kalsiyum ve oksalat için şablon oluşturur; kristalleri birbirine yapıştırarak agregatları büyütür.",
                    "İdrar ortamındaki pH ve konsantrasyon değişiklikleri proteinlerin inhibitörden promotöre dönüşümünü tetikleyebilir."
                ),
                make_active_recall(
                    "İdrar yolu enfeksiyonu taşlarında matris oranının yüzde altmış beşe kadar çıkmasının temel sebebi nedir?",
                    "Bakteriyel biyofilm üretimi, lökosit lizisi ve yoğun inflamatuar protein döküntüsüdür.",
                    "Mikroorganizma ve hücresel eksuda birikimi"
                )
            ]
        },
        # Slayt 49 [CHECKPOINT 5]
        {
            "slideNumber": 49,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Agregasyon, Retansiyon ve Taş Matrisi",
            "content": (
                "Bu bölümde kristal büyümesi, agregasyon mekanizmaları, epitelyal retansiyon hipotezleri ve taş matrisini inceledik. "
                "Nefron transit süresi 5-10 dakika kadar kısa olduğundan, tek başına kristal büyümesi obstrüksiyona yetmez; agregasyon şarttır. "
                "Kristal agregasyonu (aglomerasyon), saniyeler içinde dev partiküller yaratarak taş boyutunu artıran en hızlı süreçtir. "
                "Klinik taşın oluşması için partiküllerin böbrekte takılı kalması (retansiyon) zorunludur. "
                "Sabit partikül hipotezi epitelyal hasar ve adezyonu, serbest partikül hipotezi ise Bellini kanalı mekanik tıkanmasını savunur. "
                "Hasarlı tübül epitelinde fosfatidilserin dışa dönerek kalsiyum kristalleri için güçlü bir yapışma odağı sunar. "
                "Kalsiyum taşlarında matris %2-3 iken enfeksiyon kaynaklı taşlarda %65'e kadar çıkabilir ve taş kıvamını yumuşatır."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp05-fc01",
                    "front": "Nefron boyunca idrar akım süresi çok kısa olduğundan kristallerin lümeni tıkayacak boyuta ulaşmasını sağlayan en süratli adım nedir?",
                    "back": "Kristal agregasyonu adımıdır.",
                    "hint": "Taneciklerin birbirine kümelenmesi"
                },
                {
                    "id": "k1-27-cp05-fc02",
                    "front": "Hücresel zedelenme sırasında epitel zarının dış yüzüne açığa çıkarak kalsiyum çökeleğini bağlayan negatif yüklü fosfolipid nedir?",
                    "back": "Fosfatidilserin adlı fosfolipiddir.",
                    "hint": "Apoptozda dışa kayan membran yağı"
                },
                {
                    "id": "k1-27-cp05-fc03",
                    "front": "Kronik üreaz pozitif bakteriyel enfeksiyon zemininde gelişen taşlarda organik matris oranı en fazla yüzde kaça tırmanabilir?",
                    "back": "Yüzde altmış beş oranına tırmanabilir.",
                    "hint": "En yüksek organik içerik seviyesi"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 5 Özet Tablosu: Büyüme, Retansiyon ve Matriks Kriterleri",
                    ["Evre / Yapı", "Temel Karakter", "Süre / Oran", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Transit Süresi", "Nefron geçişi", "5 - 10 dakika", "Büyümenin tek başına yetersiz kalması"],
                            "hiddenIndex": 2,
                            "hint": "Dakikalarla ifade edilen akım süresi"
                        },
                        {
                            "cells": ["Enfeksiyon Matrisi", "Biyofilm ve hücresel debris", "%65'e kadar", "Yumuşak kıvamlı matris taşları"],
                            "hiddenIndex": 2,
                            "hint": "Zirve yapan protein fraksiyonu"
                        }
                    ]
                )
            ]
        },
        # Slayt 50
        {
            "slideNumber": 50,
            "title": "Klinik Karar: Epitelyal Hasar ve Kristal Tutulmasını Önleme",
            "content": (
                "Böbrek taşı nüksünü engellemede sadece süpersatürasyonu düşürmek yeterli olmayıp, tübüler epitel hasarını "
                "ve kristal retansiyonunu önlemek de kritik önem taşır. Hiperoksalürisi olan hastalarda hücresel oksidatif "
                "hasarı azaltmak amacıyla serbest radikal üretimini baskılayan yaşam tarzı düzenlemeleri, yeterli magnezyum "
                "ve sitrat desteği sağlanmalıdır. Magnezyum, oksalat ile bağırsakta ve idrarda birleşerek serbest oksalatı "
                "tüketir ve tübüler epitelin fosfatidilserin eksternalizasyonunu önleyerek kristal adezyonunu kökten engeller."
            ),
            "elements": [
                make_branching_logic(
                    "İdrar analizinde kalsiyum oksalat kristalleri saptanan ancak henüz obstrüktif taş geliştirmemiş bir hastada, tübüler epitele kristal yapışmasını engellemek hedefleniyor.",
                    "Fizyopatolojik olarak kristalin epitele adezyonunu ve agregasyonunu engellemede en etkili koruyucu yaklaşım hangisidir?",
                    [
                        {
                            "text": "İdrar hacmini artırarak transit süresini hızlandırmak, sitrat ve magnezyum takviyesiyle kristal yüzey yükünü nötralize edip adezyonu baskılamak",
                            "isCorrect": True,
                            "explanation": "Doğrudur; hızlı akım retansiyonu önler, sitrat ve magnezyum ise kristal agregasyonunu ve adezyonunu doğrudan inhibe eder."
                        },
                        {
                            "text": "Hastaya yüksek doz kalsiyum tabletleri vererek idrar kalsiyumunu aşırı doygun hale getirmek",
                            "isCorrect": False,
                            "explanation": "Aşırı kalsiyum verilmesi hiperkalsiüriyi ve kristal çökelmesini provoke eder."
                        },
                        {
                            "text": "Tübül epitelini asitleştirici amonyum klorür infüzyonu uygulamak",
                            "isCorrect": False,
                            "explanation": "Amonyum klorür asidoz yapar ve sitrat atılımını düşürerek taşı tetikler."
                        }
                    ]
                )
            ]
        }
    ]
