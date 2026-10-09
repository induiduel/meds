# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 19: Doğumsal Kadın/Erkek Genital Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 (hedef %10-20) oranına ulaşmasını sağlar.
"""

from scripts.k1_19_deck_data.helpers import (
    make_branching_logic, make_active_recall
)

def get_extra_branching():
    """Branching logic (klinik karar verme, genetik danışma ve acil algoritma) ögeleri."""
    return {
        2: make_branching_logic(
            "Gebeliğin 6. gününde blastosistin endometriyuma tutunması sırasında maternal kanda hCG tespit ediliyor. Kadın doğum kliniğine başvuran aile gebeliğin seyrini ve embriyonun cinsiyet tayinini öğrenmek istiyor.",
            "Genetik danışman olarak ailenin cinsiyet farklılaşması sorusuna verilecek en doğru bilimsel yanıt hangisidir?",
            [
                {
                    "text": "Genetik cinsiyet döllenme anında belirlenmiştir; ancak fetal gonadların ve dış genital organların ultrasonla ayırt edilebilmesi için en az 12-14. haftaya kadar beklenmelidir.",
                    "outcome": "Mükemmel tıbbi ve genetik bilgilendirme: Döllenmedeki genetik tayin ile embriyolojik morfolojik farklılaşma takvimi net olarak açıklanır.",
                    "isCorrect": True
                },
                {
                    "text": "Cinsiyet henüz belirlenmemiştir, 6. haftada anneye verilecek hormonlarla cinsiyet yönlendirilebilir.",
                    "outcome": "Tamamen hatalı ve zararlı yaklaşım: Genetik cinsiyet fertilizasyon anında belirlenir, sonradan değiştirilemez.",
                    "isCorrect": False
                },
                {
                    "text": "6. günde bakılacak rutin pelvik ultrason ile fetüsün kız mı erkek mi olduğu hemen görülebilir.",
                    "outcome": "İmkansız iddia: 6. günde blastosist mikroskobik düzeydedir ve gonad taslağı henüz oluşmamıştır.",
                    "isCorrect": False
                }
            ]
        ),
        5: make_branching_logic(
            "Laboratuvarda 5 haftalık bir insan embriyosunun histolojik kesiti inceleniyor. Asistan hem Wolff hem Müller kanallarının yan yana bulunduğunu görerek embriyonun çift cinsiyetli olduğunu iddia ediyor.",
            "Kıdemli embriyoloğun bu gözleme yönelik açıklaması ne olmalıdır?",
            [
                {
                    "text": "Bu gözlem patolojik değildir; insan embriyoları ilk 6 hafta boyunca indiferan bipotansiyel evrededir ve her iki kanal sistemi fizyolojik olarak bir arada bulunur.",
                    "outcome": "Doğru embriyolojik değerlendirme: 6. haftanın sonuna kadar indiferan dönem ve bipotansiyel gonad/kanal varlığı normal kabul edilir.",
                    "isCorrect": True
                },
                {
                    "text": "Embriyoda kesin bir ovotestiküler CGB vardır, derhal imha edilmelidir.",
                    "outcome": "Hatalı çıkarım: Bu evrede tüm normal embriyolarda her iki kanal mevcuttur.",
                    "isCorrect": False
                },
                {
                    "text": "Müller kanalı varsa embriyo kesinlikle genetik olarak 46,XX'tir.",
                    "outcome": "Yanlış: 46,XY erkek embriyolarda da 6. haftada Müller kanalları mevcuttur, 8. haftada AMH ile geriler.",
                    "isCorrect": False
                }
            ]
        ),
        8: make_branching_logic(
            "Klasik bir genetik araştırmasında Alfred Jost'un 1947 yılındaki tavşan embriyosu gonad çıkarma deneyi tartışılıyor.",
            "Henüz gonadal farklılaşma başlamadan önce gonad taslakları cerrahi olarak çıkarılan bir tavşan embriyosunun gelecekteki genital gelişimi için ne söylenebilir?",
            [
                {
                    "text": "Kromozomal cinsiyeti XY veya XX olsun, testis hormonları (AMH ve Testosteron) bulunmayacağı için embriyo dişi yönünde gelişir.",
                    "outcome": "Jost deneyinin temel kanıtı: Testis hormonları yokluğunda dişi kanal ve dış genitalya varsayılan yol olarak gelişir.",
                    "isCorrect": True
                },
                {
                    "text": "Gonadlar çıkarıldığı için embriyo her iki genital sistemi de tamamen kaybeder ve hiçbir kanal gelişmez.",
                    "outcome": "Hatalı: Müller kanalları hormonsuz ortamda kendiliğinden uterus ve tüplere farklılaşır.",
                    "isCorrect": False
                },
                {
                    "text": "Erkek hormonları hipofizden salgılanarak erkek iç kanallarını oluşturur.",
                    "outcome": "Hatalı: Wolff kanalları hipofize değil, doğrudan lokal testis testosteronuna bağımlıdır.",
                    "isCorrect": False
                }
            ]
        ),
        12: make_branching_logic(
            "Yenidoğan polikliniğine getirilen 46,XY karyotipli bir bebeğin dış genitalyasının kız olduğu, kanda AMH ve testosteronun saptanmadığı ve pelvik USG'de uterus bulunduğu görülüyor. SRY geninde nokta mutasyonu saptanıyor.",
            "Bu hastanın ailesine Swyer sendromu tablosu açıklanırken verilmesi gereken en kritik onkolojik uyarı nedir?",
            [
                {
                    "text": "İçeride kalan streak gonadlarda Y kromozomu varlığı nedeniyle yüksek oranda gonadoblastom ve disgerminom riski vardır; erken dönemde cerrahi gonadektomi planlanmalıdır.",
                    "outcome": "Hayati doğru klinik karar: Y materyali taşıyan disgenetik streak gonadlar malignite riski nedeniyle çıkarılmalıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Testosteron verilerek streak gonadlar hızla normal çalışan testise dönüştürülebilir.",
                    "outcome": "Biyolojik olarak imkansız: Fibröz streak gonad hormonla testise dönüştürülemez.",
                    "isCorrect": False
                },
                {
                    "text": "Hiçbir takip veya ameliyata gerek yoktur, ergenlikte kendiliğinden adet görecektir.",
                    "outcome": "Ölümcül ihmal: Streak gonad hormon üretmez ve kanserleşme riski taşır.",
                    "isCorrect": False
                }
            ]
        ),
        14: make_branching_logic(
            "Doğum salonunda tibia ve femurlarında yay şeklinde eğrilik, hipoplastik toraks ve yarık damak saptanan bir bebeğin karyotipinin 46,XY olmasına rağmen dış genitalyasının kız olduğu bildiriliyor.",
            "Tıbbi genetik konsültanının şüphelenmesi gereken hastalık ve planlayacağı genetik analiz ne olmalıdır?",
            [
                {
                    "text": "Kampomelik Displazi düşünülmeli ve 17q24 lokusundaki SOX9 geni dizi analizi istenmelidir.",
                    "outcome": "Mükemmel klinik tanı: SOX9 mutasyonu hem kıkırdak displazisi hem de 46,XY cinsiyet tersinmesi yapar.",
                    "isCorrect": True
                },
                {
                    "text": "Akondroplazi düşünülmeli ve FGFR3 geni taranmalıdır.",
                    "outcome": "Yetersiz/hatalı: FGFR3 cinsiyet tersinmesi yapmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Osteogenezis imperfekta düşünülmeli ve tip 1 kollajen genleri incelenmelidir.",
                    "outcome": "Hatalı: OI cinsiyet tersinmesi tablosu oluşturmaz.",
                    "isCorrect": False
                }
            ]
        ),
        16: make_branching_logic(
            "Proteinüri ve nefrotik sendrom tablosuyla başvuran 14 yaşındaki bir kız çocuğunda renal biyopside diffüz mezanjiyal skleroz saptanıyor. USG'de böbrekte Wilms tümörü kitlesi ve pelviste disgenetik gonadlar görülüyor. Karyotipi 46,XY çıkıyor.",
            "Bu hastada altta yatan sendromik patoloji ve mutasyonlu gen hangisidir?",
            [
                {
                    "text": "Denys-Drash Sendromu - WT1 geni ekzon 8-9 missense mutasyonu.",
                    "outcome": "Kusursuz klinik patoloji eşleşmesi: Diffüz mezanjiyal skleroz, Wilms tümörü ve 46,XY CGB üçlüsü Denys-Drash sendromudur.",
                    "isCorrect": True
                },
                {
                    "text": "Frasier Sendromu - WT1 geni intron 9 splice mutasyonu.",
                    "outcome": "Yanlış ayrım: Frasier sendromunda FSGS görülür, Wilms tümörü çok nadirdir ve böbrek tutulumu daha geçtir.",
                    "isCorrect": False
                },
                {
                    "text": "Alport Sendromu - COL4A5 gen mutasyonu.",
                    "outcome": "Hatalı: Alport sendromu nefrit ve sağırlık yapar, CGB ve Wilms tümörü yapmaz.",
                    "isCorrect": False
                }
            ]
        ),
        22: make_branching_logic(
            "17 yaşında primer amenore şikayetiyle başvuran genç bir kadında yapılan tetkiklerde uterus ve vajinanın üst kısmının bulunmadığı (Müller aplazisi), hafif klitoromegali ve yüksek serum androjen düzeyleri saptanıyor. Karyotipi 46,XX geliyor.",
            "Genetik köken araştırılırken öncelikle taranması gereken over farklılaşma geni hangisidir?",
            [
                {
                    "text": "WNT4 geni heterozigot inaktive edici mutasyonu.",
                    "outcome": "Kusursuz tanı: WNT4 defekti 46,XX kadınlarda Müller aplazisi, over disfonksiyonu ve androjen fazlalığı ile seyreder.",
                    "isCorrect": True
                },
                {
                    "text": "SRY geni duplikasyonu.",
                    "outcome": "Hatalı: SRY Y kromozomundadır ve bu hastada Müller aplazisi ile birlikte over stroma hiperandrojenizmi WNT4'e özgüdür.",
                    "isCorrect": False
                },
                {
                    "text": "AR (Androjen Reseptör) mutasyonu.",
                    "outcome": "Hatalı: AR mutasyonu 46,XY bireylerde görülür ve androjen fazlalığına değil direncine yol açar.",
                    "isCorrect": False
                }
            ]
        ),
        24: make_branching_logic(
            "Karyotipi 46,XX olan bir çocuğun muayenesinde ovotestis dokusu, el ve ayak tabanlarında ileri derecede deri kalınlaşması (palmoplantar hiperkeratoz) ve skuamöz hücreli karsinom gelişimi saptanıyor.",
            "Wnt/β-katenin yolağını destekleyen ve bu klinik tabloya yol açan kusurlu gen hangisidir?",
            [
                {
                    "text": "RSPO1 geni homozigot inaktivasyon mutasyonu.",
                    "outcome": "Kusursuz genetik eşleşme: RSPO1 mutasyonu 46,XX cinsiyet tersinmesi ve palmoplantar hiperkeratoz ile karakterizedir.",
                    "isCorrect": True
                },
                {
                    "text": "FOXL2 gen delesyonu.",
                    "outcome": "Hatalı: FOXL2 göz kapağı anomalisi (BPES) yapar, hiperkeratoz yapmaz.",
                    "isCorrect": False
                },
                {
                    "text": "DAX1 gen duplikasyonu.",
                    "outcome": "Hatalı: DAX1 duplikasyonu 46,XY bireylerde cinsiyet tersinmesi yapar.",
                    "isCorrect": False
                }
            ]
        ),
        26: make_branching_logic(
            "Genetik polikliniğinde bir ailenin 46,XY karyotipli çocuğunda dişi dış genitalya saptanıyor. Yapılan mikrodizi (Array-CGH) analizinde Xp21 bölgesinde bir duplikasyon tespit ediliyor.",
            "Bu tablonun patofizyolojisi hakkında hekimin yapacağı en doğru açıklama nedir?",
            [
                {
                    "text": "Xp21'deki DAX1 geninin çift kopya olması (duplikasyon), SF1 ve SOX9'u aşırı baskılayarak dozaj duyarlı cinsiyet tersinmesine yol açmıştır.",
                    "outcome": "Tam doğru moleküler mekanizma: DAX1 duplikasyonu doza bağlı olarak SRY/SOX9 kaskadını bloke eder.",
                    "isCorrect": True
                },
                {
                    "text": "Xp21'de SRY geninin yer alması nedeniyle testis gelişimini hızlandırmıştır.",
                    "outcome": "Hatalı: SRY Yp11.3'tedir, Xp21'de DAX1 yer alır.",
                    "isCorrect": False
                },
                {
                    "text": "Bu duplikasyon klinik olarak önemsiz bir selim polimorfizmdir.",
                    "outcome": "Hatalı: DAX1 duplikasyonu klasik bir cinsiyet tersinmesi nedenidir.",
                    "isCorrect": False
                }
            ]
        ),
        32: make_branching_logic(
            "Fıtık operasyonuna alınan 6 aylık normal erkek dış genitalyasına sahip bir bebeğin fıtık kesesi açıldığında içinde uterus ve fallop tüpü benzeri yapılar görülüyor. Testisler tüplere yapışık olarak izleniyor. Karyotip 46,XY olarak raporlanıyor.",
            "Bu durum karşısında cerrahi ve genetik ekibin ortak yaklaşımı ne olmalıdır?",
            [
                {
                    "text": "Persistan Müller Kanalı Sendromu (PMDS) düşünülmeli; AMH veya AMHR2 gen mutasyonu araştırılmalı, testis sperm yollarına zarar vermeden dikkatle skrotuma indirilmelidir.",
                    "outcome": "Mükemmel klinik yaklaşım: PMDS'de testis kanallarını zedelemeden orşiopeksi ve genetik analiz esastır.",
                    "isCorrect": True
                },
                {
                    "text": "Uterus görüldüğü için bebek hemen kız cinsiyetine çevrilmeli ve bilateral testisler çıkarılmalıdır.",
                    "outcome": "Korkunç bir tıbbi hata: PMDS'de birey tamamen erkektir ve erkek olarak yaşamını sürdürmelidir.",
                    "isCorrect": False
                },
                {
                    "text": "Uterus hızla koterize edilip tüm pelvik organlar körlemesine temizlenmelidir.",
                    "outcome": "Tehlikeli ve kanamalı cerrahi zarar: Vas deferens uterus duvarına yapışık olabilir, organ yaralanması riski yüksektir.",
                    "isCorrect": False
                }
            ]
        ),
        34: make_branching_logic(
            "Tek taraflı inmemiş testis nedeniyle ameliyat edilen bir çocukta sağ testisin normal olduğu ve sağda vas deferensin geliştiği, ancak sol tarafta testis agenezisi olduğu ve sol vas deferensin hiç oluşmadığı görülüyor.",
            "Alfred Jost'un embriyolojik prensiplerine göre sol vas deferensin gelişmemesinin nedeni nedir?",
            [
                {
                    "text": "Wolff kanalının gelişimi yalnızca o taraftaki (ipsilateral) testisten salgılanan yüksek lokal testosteron konsantrasyonuna bağımlıdır; sol testis olmadığı için sol Wolff erimiştir.",
                    "outcome": "Tam embriyolojik mekanizma: Testosteronun Wolff üzerindeki etkisi lokal/parakrindir, dolaşımdaki testosteron karşı tarafı kurtarmaya yetmez.",
                    "isCorrect": True
                },
                {
                    "text": "Sağ testis sol testisin hormonlarını tüketmiştir.",
                    "outcome": "Biyolojik olarak anlamsız yorum.",
                    "isCorrect": False
                },
                {
                    "text": "Sol tarafta aşırı östrojen üretilmiştir.",
                    "outcome": "Hatalı: Sebep östrojen değil, ipsilateral lokal testosteron yokluğudur.",
                    "isCorrect": False
                }
            ]
        ),
        38: make_branching_logic(
            "Bilateral inmemiş testis (intraabdominal kriptorşidizm) saptanan bir erkek bebekte yapılan genetik analizde RXFP2 (LGR8) reseptör geninde homozigot mutasyon saptanıyor.",
            "Bu bebeğin testis iniş kusurunun embriyolojik kökeni nedir?",
            [
                {
                    "text": "Leydig kaynaklı INSL3 hormonunun gubernakulumdaki RXFP2 reseptörüne bağlanamaması sonucu transabdominal iniş fazı gerçekleşememiştir.",
                    "outcome": "Mükemmel patofizyolojik açıklama: INSL3-RXFP2 aksı transabdominal fazın temel mekanizmasıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Testosteron reseptörünün yokluğu nedeniyle inguinoskrotal faz tıkalıdır.",
                    "outcome": "Yanlış: RXFP2 androjen reseptörü değil, INSL3 reseptörüdür.",
                    "isCorrect": False
                },
                {
                    "text": "Sertoli hücrelerinin aşırı AMH salgılaması testisi yukarı çekmiştir.",
                    "outcome": "Hatalı: AMH testisin inişini engellemez.",
                    "isCorrect": False
                }
            ]
        ),
        42: make_branching_logic(
            "Doğum salonunda ebe ve aile hekimi kuşkulu genitalyalı bir bebek gördüklerinde 'Bu çocuk hermafrodit mi?' diye soruyorlar.",
            "Yenidoğan sorumlusu hekimin 2006 Chicago Konsensüsü ilkelerine göre vermesi gereken en profesyonel yanıt nedir?",
            [
                {
                    "text": "Eski damgalayıcı hermafroditizm terimlerinin terk edildiğini, bebeğin durumunun 'Cinsiyet Gelişim Bozukluğu' olarak adlandırıldığını ve karyotip ile etiyolojinin belirleneceğini söylemek.",
                    "outcome": "Etik, bilimsel ve güncel Chicago konsensüsüne tam uyumlu iletişim.",
                    "isCorrect": True
                },
                {
                    "text": "Bebeğin gerçek bir hermafrodit olduğunu ve derhal ameliyata alınacağını ilan etmek.",
                    "outcome": "Eski ve damgalayıcı dil, yanlış aceleci tutum.",
                    "isCorrect": False
                },
                {
                    "text": "Cinsiyetin bir önemi olmadığını söyleyip aileyi hiçbir test yapmadan taburcu etmek.",
                    "outcome": "Hayati ihmal: Altta yatan KAH tuz krizi ölümcül olabilir.",
                    "isCorrect": False
                }
            ]
        ),
        45: make_branching_logic(
            "Tıp fakültesi intörnü vaka sunumunda: 'Hastamızın over dokusu ve uterusu mevcuttur ancak dış genitalyası aşırı virilizedir; bu tablo klasik erkek psödohermafroditizmdir' diyor.",
            "Öğretim üyesinin intörnü düzeltmesi gereken nokta hangisidir?",
            [
                {
                    "text": "Over ve uterus taşıyan virilize birey 'erkek' değil, eski adıyla 'dişi psödohermafroditizm' (modern adıyla 46,XX CGB) tablosudur; gonad over olduğu için dişi kökenlidir.",
                    "outcome": "Doğru terminolojik düzeltme: Psödohermafroditizmde ön ek (erkek/dişi) daima gonadın gerçek türünü ifade eder.",
                    "isCorrect": True
                },
                {
                    "text": "İntörn haklıdır, dış genitalya erkeksi olduğu için erkek psödohermafrodit denir.",
                    "outcome": "Hatalı: Eski sınıflamada ön ek dış genitalyaya değil, gonadın kendisine göre verilirdi.",
                    "isCorrect": False
                },
                {
                    "text": "Uterus varsa karyotip kesinlikle 47,XXY'dir.",
                    "outcome": "Hatalı: Uterus 46,XX dişi bireylerde bulunur, 47,XXY Klinefelter'de uterus olmaz.",
                    "isCorrect": False
                }
            ]
        ),
        48: make_branching_logic(
            "Yenidoğan yoğun bakımda takip edilen bir term erkek bebekte gerilmiş penis boyu 1.8 cm (-2.5 SD altı) ölçülüyor. Bebeğin kan şekerinin 25 mg/dL (derin hipoglisemi) olduğu ve sarılığının uzadığı saptanıyor.",
            "Nöbet geçirme riski olan bu bebekte acilen hangi endokrin acil durum düşünülmeli ve araştırılmalıdır?",
            [
                {
                    "text": "Konjenital Panhipopituitarizm (ACTH ve Büyüme Hormonu eksikliği).",
                    "outcome": "Hayat kurtarıcı klinik refleks: Mikrofallus + hipoglisemi hipofiz yetmezliğinin ölümcül uyarı sinyalidir.",
                    "isCorrect": True
                },
                {
                    "text": "Basit idiyopatik sünnet derisi darlığı.",
                    "outcome": "Ölümcül teşhis hatası: Hipoglisemi sünnet derisiyle açıklanamaz.",
                    "isCorrect": False
                },
                {
                    "text": "Turner sendromu.",
                    "outcome": "Hatalı: Turner kızlarda görülür ve mikrofallus yapmaz.",
                    "isCorrect": False
                }
            ]
        ),
        52: make_branching_logic(
            "20 yaşında uzun boylu bir erkek hasta, ergenlikte memelerinin büyümesi (jinekomasti) ve testislerinin hiç büyümemesi nedeniyle başvuruyor. Yapılan sperm analizinde tam azospermi saptanıyor.",
            "Genetik uzmanın isteyeceği karyotip analizinde beklenen en olası kromozom formülü nedir?",
            [
                {
                    "text": "47,XXY (Klinefelter Sendromu).",
                    "outcome": "Kusursuz klinik eşleşme: Uzun boy, jinekomasti, atrofik testis ve azospermi klasik Klinefelter tablosudur.",
                    "isCorrect": True
                },
                {
                    "text": "45,X (Turner Sendromu).",
                    "outcome": "Hatalı: Turner kızlarda görülür ve boy kısadır.",
                    "isCorrect": False
                },
                {
                    "text": "47,XYY (Jakob Sendromu).",
                    "outcome": "Hatalı: 47,XYY fertildir ve jinekomasti tipik değildir.",
                    "isCorrect": False
                }
            ]
        ),
        55: make_branching_logic(
            "Yenidoğan muayenesinde ellerinde ve ayak sırtlarında gode bırakmayan lenfödem, ense bölgesinde kalın deri kıvrımları (yele boyun) saptanan bir kız bebekte üfürüm duyuluyor. Ekokardiyografide aort koarktasyonu saptanıyor.",
            "Bu yenidoğanın genetik tanısı için en kuvvetli ön tanı nedir?",
            [
                {
                    "text": "Turner Sendromu (45,X).",
                    "outcome": "Kusursuz neonatal tanı: Yenidoğanda el-ayak ödemi, yele boyun ve aort koarktasyonu Turner sendromunu gösterir.",
                    "isCorrect": True
                },
                {
                    "text": "Down Sendromu (Trizomi 21).",
                    "outcome": "Hatalı: Down sendromunda atriyoventriküler septal defekt sıktır, yele boyun ve lenfödem Turner'a özgüdür.",
                    "isCorrect": False
                },
                {
                    "text": "Marfan Sendromu.",
                    "outcome": "Hatalı: Marfan'da lens luksasyonu ve aort anevrizması olur, yenidoğan lenfödemi görülmez.",
                    "isCorrect": False
                }
            ]
        ),
        58: make_branching_logic(
            "Kuşkulu genitalyalı bir hastanın laparoskopisinde sağ tarafta disgenetik bir testis ve vas deferens, sol tarafta ise fibröz streak gonad, sol fallop tüpü ve yarım uterus boynuzu görülüyor. Karyotipi 45,X/46,XY mozaik çıkıyor.",
            "Bu hastada miks gonadal disgenezi tanısı konulduktan sonra cerrahi planlama ne olmalıdır?",
            [
                {
                    "text": "Y kromozomu taşıyan disgenetik dokularda ve streak gonadda yüksek gonadoblastom riski nedeniyle profilaktik gonadektomi yapılmalıdır.",
                    "outcome": "Hayati doğru karar: MGD olgularında malignite riski yüksektir, streak gonad derhal çıkarılmalıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Streak gonad korunmalı, normal çalışan testis çıkarılmalıdır.",
                    "outcome": "Ters ve zararlı uygulama: Kanser riski streak ve inmemiş disgenetik dokudadır.",
                    "isCorrect": False
                },
                {
                    "text": "Hiçbir cerrahi yapılmadan 50 yaşına kadar beklenmelidir.",
                    "outcome": "Ölümcül ihmal: Kanser çocukluk ve genç erişkinlikte gelişir.",
                    "isCorrect": False
                }
            ]
        ),
        62: make_branching_logic(
            "Kız olarak büyütülen 2 yaşındaki bir çocuğun kasık fıtığı kesesinde testis palpe ediliyor. Karyotip 46,XY bulunuyor. hCG stimülasyon testi yapıldığında testosteronun çok yükseldiği ancak DHT'nin düşük kaldığı ve T/DHT oranının 45 olduğu saptanıyor.",
            "Bu bulgular ışığında hastanın moleküler tanısı nedir?",
            [
                {
                    "text": "SRD5A2 gen mutasyonuna bağlı 5α-Redüktaz 2 Eksikliği.",
                    "outcome": "Kusursuz biyokimyasal tanı: T/DHT oranının >30-35 olması 5α-redüktaz eksikliğinin altın standart kanıtıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Komplet Androjen Duyarsızlık Sendromu.",
                    "outcome": "Hatalı: CAIS'te T/DHT oranı normaldir (DHT rahatça üretilir).",
                    "isCorrect": False
                },
                {
                    "text": "21-Hidroksilaz Eksikliği.",
                    "outcome": "Hatalı: 21-OH eksikliği 46,XX kızda virilizasyon yapar.",
                    "isCorrect": False
                }
            ]
        ),
        65: make_branching_logic(
            "Dominik Cumhuriyeti'nde veya Doğu Karadeniz'de bir köyde kız olarak yetiştirilen 13 yaşındaki bir çocukta ergenlikle birlikte ses kalınlaşıyor, klitoris zannedilen fallus uzayarak penise dönüşüyor ve kas kütlesi artıyor.",
            "Aileye bu biyolojik dönüşümün nedeni nasıl açıklanmalıdır?",
            [
                {
                    "text": "Pubertede aşırı artan testosteron ve devreye giren tip 1 enzim sayesinde dokuların erkekleştiği, bireyin biyolojik ve psikolojik olarak erkek olduğu açıklanmalıdır.",
                    "outcome": "Tam doğru bilimsel ve insani bilgilendirme: 5α-redüktaz eksikliğinde pubertal virilizasyon doğal seyrin parçasıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Çocuğun aniden cinsiyet değiştiren doğaüstü bir varlık olduğu söylenmelidir.",
                    "outcome": "Hurafe ve bilim dışı yaklaşım.",
                    "isCorrect": False
                },
                {
                    "text": "Derhal penis kesilerek kadın yapılmalıdır.",
                    "outcome": "Geri dönülmez cerrahi ve psikolojik yıkım: Bu bireylerin çoğu erkek kimliğindedir.",
                    "isCorrect": False
                }
            ]
        ),
        68: make_branching_logic(
            "5α-redüktaz eksikliği tanısı kesinleşen ve ailesi ile hekim konseyi tarafından erkek cinsiyetinde büyütülmesine karar verilen 4 yaşındaki bir çocukta penis boyunun çok küçük (mikrofallus) olduğu görülüyor.",
            "Hipospadias ameliyatı öncesinde fallik dokuyu ameliyata uygun boyuta getirmek için hangi medikal tedavi başlanmalıdır?",
            [
                {
                    "text": "Topikal Dihidrotestosteron (DHT) jel tedavisi.",
                    "outcome": "Kusursuz farmakoterapötik seçim: Eksik olan DHT doğrudan cilde sürülerek lokal reseptörler uyarılır ve fallus büyütülür.",
                    "isCorrect": True
                },
                {
                    "text": "Oral östrojen hapları.",
                    "outcome": "Tamamen zıt etki: Östrojen fallusu küçültür ve meme büyütür.",
                    "isCorrect": False
                },
                {
                    "text": "Büyüme hormonu blokörü.",
                    "outcome": "Hatalı: Büyümeyi durdurmak hedef değildir.",
                    "isCorrect": False
                }
            ]
        ),
        72: make_branching_logic(
            "17 yaşında boylu poslu, meme gelişimi kusursuz olan genç bir kadın hiç menstrüasyon görmeme (primer amenore) nedeniyle başvuruyor. Pelvik USG'de uterus ve overlerin bulunmadığı, vajinanın kör bir cep şeklinde bittiği saptanıyor. Karyotipi 46,XY çıkıyor.",
            "Bu hastada tanıyı kesinleştirmek için öncelikle hangi gen sekanslanmalıdır?",
            [
                {
                    "text": "Xq11-12 lokusundaki Androjen Reseptörü (AR) geni.",
                    "outcome": "Kusursuz genetik hedef: CAIS tablosunun nedeni AR genindeki fonksiyon kaybı mutasyonlarıdır.",
                    "isCorrect": True
                },
                {
                    "text": "CYP21A2 geni.",
                    "outcome": "Hatalı: CYP21A2 KAH nedenidir, karyotip 46,XX olur.",
                    "isCorrect": False
                },
                {
                    "text": "SRD5A2 geni.",
                    "outcome": "Hatalı: 5α-redüktaz eksikliğinde meme gelişmez, virilizasyon olur.",
                    "isCorrect": False
                }
            ]
        ),
        75: make_branching_logic(
            "CAIS şüphesiyle incelenen bir hastanın fizik muayenesinde memeler Tanner Evre 5 olarak değerlendiriliyor ancak aksiller ve pubik bölgede tek bir kıl dahi bulunmadığı görülüyor.",
            "Genetik stajyerinin 'Meme varsa kıllanma neden hiç yok?' sorusuna verilecek en doğru fizyolojik yanıt nedir?",
            [
                {
                    "text": "Meme gelişimi testosteronun aromatazla östrojene dönüşmesiyle sağlanır; ancak pubik kıllanma doğrudan androjen reseptörlerine bağımlıdır ve reseptör direnci nedeniyle kıl folikülleri uyarılamaz.",
                    "outcome": "Kusursuz endokrinolojik açıklama: Östrojen reseptörleri sağlamdır (meme büyür), androjen reseptörleri tıkalıdır (kıl çıkmaz).",
                    "isCorrect": True
                },
                {
                    "text": "Hastanın epilasyon yaptırmış olması en olası sebeptir.",
                    "outcome": "Tıbbi derinlikten uzak ciddiyetsiz yanıt.",
                    "isCorrect": False
                },
                {
                    "text": "Kıllanmanın cinsiyet hormonlarıyla hiçbir ilişkisi yoktur.",
                    "outcome": "Yanlış: Adrenarş ve pubarş tamamen androjenlere bağımlıdır.",
                    "isCorrect": False
                }
            ]
        ),
        82: make_branching_logic(
            "Yenidoğan servisinde 10 günlük bir bebekte kusma, kilo kaybı ve letarji gelişiyor. Biyokimyada sodyum 118 mEq/L (ağır hiponatremi), potasyum 7.2 mEq/L (tehlikeli hiperkalemi) saptanıyor. Bebeğin dış genitalyasında klitoromegali ve labial füzyon görülüyor.",
            "Nöbet ve kardiyak arrest riski altındaki bu bebeğin acil medikal yönetimi nasıl olmalıdır?",
            [
                {
                    "text": "Tuz kaybettirici KAH adrenal krizi olarak kabul edilip derhal serum fizyolojik, glukoz, parenteral hidrokortizon ve hiperkalemi tedavisi başlanmalıdır.",
                    "outcome": "Hayat kurtaran acil tıp müdahalesi: Tuz kaybettirici KAH krizinde intravenöz sıvı ve hidrokortizon geciktirilemez.",
                    "isCorrect": True
                },
                {
                    "text": "Sadece anne sütü artırılmalı ve taburcu edilmelidir.",
                    "outcome": "Ölümcül ihmal: Bebek birkaç saat içinde kardiyak arrestle kaybedilir.",
                    "isCorrect": False
                },
                {
                    "text": "Derhal klitoris küçültme ameliyatına alınmalıdır.",
                    "outcome": "Ölümcül cerrahi hata: Hasta elektrolit dengesizliği ve şoktayken ameliyat edilemez.",
                    "isCorrect": False
                }
            ]
        ),
        85: make_branching_logic(
            "KAH tanısı almış 46,XX bir kız çocuğunda büyüme takibi yapılırken yıllık boy uzamasının yaşıtlarından çok daha hızlı olduğu ancak kemik yaşının takvim yaşından 4 yıl ileri olduğu saptanıyor.",
            "Endokrinolog bu tabloyu nasıl yorumlamalı ve tedaviyi nasıl ayarlamalıdır?",
            [
                {
                    "text": "Glukokortikoid dozu yetersizdir; aşırı adrenal androjenler büyüme plaklarını hızla olgunlaştırmaktadır; doz artırılmazsa epifizler erken kapanacak ve nihai boy çok kısa kalacaktır.",
                    "outcome": "Kusursuz pediatrik endokrinoloji yönetimi: KAH'ta androjen baskılanmazsa erken epifiz kapanması ve kısa boy kaçınılmazdır.",
                    "isCorrect": True
                },
                {
                    "text": "Çocuğun gelecekte basketbolcu olacağı söylenerek hiçbir ilaç verilmemelidir.",
                    "outcome": "Feci bir yanılgı: Hızlı uzama erken duracak ve çocuk çok kısa boylu kalacaktır.",
                    "isCorrect": False
                },
                {
                    "text": "Büyümeyi yavaşlatmak için çocuğun beslenmesi tamamen kesilmelidir.",
                    "outcome": "Zararlı ve tıbbi olmayan yaklaşım.",
                    "isCorrect": False
                }
            ]
        ),
        92: make_branching_logic(
            "Daha önce 21-hidroksilaz eksikliği olan tuz kaybettirici formda bir çocuk dünyaya getiren anne tekrar gebe kalıyor ve 6. haftada başvuruyor. Anneye derhal deksametazon başlanıyor. 11. haftada yapılan CVS testinde fetüsün 46,XX ve CYP21A2 bileşik heterozigot mutasyonlu (hasta) olduğu saptanıyor.",
            "Perinatoloji ve genetik kurulunun bu gebelikteki deksametazon tedavi kararı ne olmalıdır?",
            [
                {
                    "text": "Fetus etkilenmiş bir 46,XX kız olduğu için virilizasyonu önlemek amacıyla deksametazon tedavisi doğuma kadar aynı şekilde sürdürülmelidir.",
                    "outcome": "Tam doğru kılavuz kararı: Deksametazonun doğuma kadar devam ettiği tek senaryo etkilenmiş kız fetustur.",
                    "isCorrect": True
                },
                {
                    "text": "Fetus hasta olduğu için deksametazon hemen kesilmelidir.",
                    "outcome": "Hatalı: Tedavi kesilirse kız fetus intrauterin dönemde ileri derecede virilize olur.",
                    "isCorrect": False
                },
                {
                    "text": "Deksametazon yerine yüksek doz testosteron verilmelidir.",
                    "outcome": "Felaket bir hata: Testosteron verilirse bebek daha da virilize olur.",
                    "isCorrect": False
                }
            ]
        ),
        95: make_branching_logic(
            "Doğum salonunda kuşkulu genitalyalı bir bebek dünyaya geliyor. Aile panik içinde 'Bebeğimiz kız mı erkek mi, nüfusa ne yazdıralım?' diye soruyor.",
            "Yenidoğan hekiminin ilk 24 saatteki en doğru yaklaşımı ne olmalıdır?",
            [
                {
                    "text": "Aileyi teskin ederek genital organ gelişiminin henüz tamamlanmadığını, hızlı testler (karyotip, hormonlar, USG) yapılana kadar nüfus tescilinin bekletilmesi gerektiğini ve multidisipliner bir konseyin durumu değerlendireceğini söylemek.",
                    "outcome": "Kusursuz tıp etiği ve hasta iletişimi: Aceleci yanlış cinsiyet atamasını ve ailenin travmatize olmasını önler.",
                    "isCorrect": True
                },
                {
                    "text": "Bebeğin fallusuna bakıp 'Bence bu erkektir' diyerek hemen erkek kimliği çıkarmalarını söylemek.",
                    "outcome": "Ağır tıbbi ve hukuki hata: Altta yatan 46,XX KAH tuz kriziyle ölebilir.",
                    "isCorrect": False
                },
                {
                    "text": "Bebeği hemen ameliyathaneye alıp rastgele bir dış genitalya dikmek.",
                    "outcome": "Etik dışı ve kabul edilemez cerrahi istismar.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_recalls():
    """Active recall (hızlı hatırlama ve kilit bilgi pekiştirme) ögeleri."""
    return {
        4: make_active_recall(
            "Erkek cinsiyetinin belirlenmesinde en az bir kopyasının bulunması zorunlu olan ve üzerinde SRY genini taşıyan seks kromozomu hangisidir?",
            "Y kromozomu",
            "Erkek cinsiyeti belirleyen ve p kolunda TDF taşıyan insan kromozomu"
        ),
        7: make_active_recall(
            "İnterfaz çekirdeğinde dişi memelilerde inaktif kalan X kromozomunun mikroskop altında koyu bir kitle olarak görülmesine ne ad verilir?",
            "Barr cisimciği (Seks kromatini)",
            "Lionizasyon hipotezine dayanan çekirdek kütlesi"
        ),
        11: make_active_recall(
            "Testis gelişimini tetikleyen SRY geni embriyonik dönemin hangi post-konsepsiyonel gününde presertoli hücrelerinde en yüksek ekspresyon düzeyine (pik) ulaşır?",
            "41. gün (Kırk birinci gün)",
            "SRY ekspresyonunun tepe noktasına çıktığı embriyonik gün"
        ),
        15: make_active_recall(
            "Bipotansiyel gonad taslağının ve adrenal korteksin oluşması için zorunlu olan, SOX9 ile birlikte AMH salgısını açan nükleer reseptör faktörü hangisidir?",
            "SF1 (Steroidogenic Factor 1 / NR5A1)",
            "Adrenal steroidogenez ve erken katlantıyı yöneten faktör"
        ),
        23: make_active_recall(
            "Over belirleyici WNT4 geninin homozigot inaktive edici mutasyonu sonucu 46,XX cinsiyet tersinmesi, böbrek agenezisi ve adrenal disgenezisi ile giden letal sendrom hangisidir?",
            "SERKAL sendromu",
            "WNT4 tam kaybında görülen sendrom"
        ),
        27: make_active_recall(
            "Xp21 bölgesinde yer alan DAX1 (NR0B1) geninin inaktive edici mutasyonu erkeklerde hangi iki temel klinik probleme yol açar?",
            "X'e bağlı konjenital adrenal hipoplazi ve hipogonadotropik hipogonadizm",
            "Böbrek üstü bezi yetersizliği ve puberteye girememe birlikteliği"
        ),
        33: make_active_recall(
            "Persistan Müller Kanalı Sendromunda (PMDS) 46,XY normal bir erkekte uterus ve fallop tüplerinin kalmasına yol açan iki gen mutasyonu hangileridir?",
            "AMH ve AMHR2 genleri",
            "Müller'i gerileten hormon ve onun tip 2 reseptörü"
        ),
        37: make_active_recall(
            "Kolesterol sentezinin son basamağında 7-dehidrokolesterol redüktaz enzim eksikliği sonucu 46,XY ambigus genitalya ve 2-3 ayak sindaktilisi yapan sendrom hangisidir?",
            "Smith-Lemli-Opitz Sendromu (SLOS / DHCR7)",
            "Kolesterol sentez defektiyle seyreden doğumsal anomali sendromu"
        ),
        43: make_active_recall(
            "2006 Chicago Konsensüsü öncesinde kullanılan 'erkek psödohermafroditizm' teriminin günümüzdeki karyotip tabanlı bilimsel karşılığı nedir?",
            "46,XY CGB (Cinsiyet Gelişim Bozukluğu)",
            "Testis taşıyan ancak yetersiz virilize olan bireylerin yeni sınıf adı"
        ),
        47: make_active_recall(
            "Erkek çocuklarda eksternal üretral ağzın penisin ventral alt yüzüne açılmasıyla karakterize en sık ürogenital katlantı kapanma defekti anomalisi nedir?",
            "Hipospadias",
            "Ventral üretra açıklığı anomalisi"
        ),
        53: make_active_recall(
            "47,XXY Klinefelter sendromlu bir erkeğin bukkal yayma hücrelerinde mikroskop altında kaç adet Barr cisimciği izlenir?",
            "1 adet (Bir adet)",
            "X kromozomu sayısının 1 eksiği kadar olan sayı"
        ),
        57: make_active_recall(
            "47,XXX (Trizomi X) karyotipine sahip bir kadının interfaz çekirdeğinde kaç adet Barr cisimciği saptanır?",
            "2 adet (İki adet)",
            "3 adet X kromozomundan inaktive olanların sayısı"
        ),
        63: make_active_recall(
            "5α-redüktaz tip 2 eksikliğinde hedef dış genital dokularda üretilemeyen ve penis/skrotum maskülinizasyonundan sorumlu olan anahtar androjen hormonu hangisidir?",
            "Dihidrotestosteron (DHT)",
            "Testosteronun 5-alfa indirgenmesiyle oluşan yüksek afiniteli hormon"
        ),
        67: make_active_recall(
            "5α-redüktaz 2 eksikliği tanısında hCG stimülasyonu sonrasında serum Testosteron / Dihidrotestosteron (T/DHT) oranının kaçın üzerinde olması patognomoniktir?",
            "30'un üzerinde (>30)",
            "Enzim bloğunu kanıtlayan eşik T/DHT sayısal oranı"
        ),
        73: make_active_recall(
            "Komplet Androjen Duyarsızlık Sendromunda (CAIS) hastanın dış görünüşü tamamen kadın olmasına rağmen pelviste neden uterus ve fallop tüpleri bulunmaz?",
            "Testis Sertoli hücrelerinin normal AMH salgılaması nedeniyle",
            "Müller kanallarını eriten hormonun varlığı"
        ),
        77: make_active_recall(
            "Androjen reseptör fonksiyonunun kısmen korunduğu ve mikrofallus, perineal hipospadias ile jinekomastiye yol açan parsiyel androjen duyarsızlığının klasik eponimi nedir?",
            "Reifenstein Sendromu (PAIS)",
            "Parsiyel androjen duyarsızlığının tarihi sendrom adı"
        ),
        83: make_active_recall(
            "Konjenital adrenal hiperplazide 21-hidroksilaz enzim eksikliğinde birikerek yenidoğan topuk kanı taramasında bakılan temel steroid belirteci nedir?",
            "17-Hidroksiprogesteron (17-OHP)",
            "KAH yenidoğan tarama belirteci"
        ),
        87: make_active_recall(
            "Doğumda genital anomalisi olmayan ancak ergenlikte şiddetli akne, hirsutizm ve oligomenore ile kliniğe başvuran hafif 21-hidroksilaz eksikliği formuna ne ad verilir?",
            "Non-klasik (Geç başlangıçlı) KAH",
            "PCOS taklitçisi hafif form"
        ),
        93: make_active_recall(
            "Kuşkulu genitalya ile doğan bir bebekte bilateral gonadların palpe edilememesi durumunda ilk dışlanması gereken hayatı tehdit edici durum nedir?",
            "46,XX Konjenital Adrenal Hiperplazi (Tuz kaybettirici kriz riski)",
            "Adrenal kriz ve ölüm riski taşıyan durum"
        ),
        97: make_active_recall(
            "Tüm ileri moleküler genetik yöntemlere (WES, NGS panelleri) rağmen 46,XY CGB olgularının yaklaşık yüzde kaçında genetik neden aydınlatılamamaktadır?",
            "Yüzde 20 ila 25'inde (%20-25)",
            "Açıklanamayan 46,XY CGB oranı"
        )
    }

def apply_enrichment(slides):
    """Slayt listesine branching logic ve active recall ögelerini entegre eder."""
    extra_branching = get_extra_branching()
    extra_recalls = get_extra_recalls()
    
    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        if slide_num in extra_branching:
            slide.setdefault("elements", []).append(extra_branching[slide_num])
        if slide_num in extra_recalls:
            slide.setdefault("elements", []).append(extra_recalls[slide_num])
            
    return slides
