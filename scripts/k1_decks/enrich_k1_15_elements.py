# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını garanti eder.
"""

from scripts.k1_15_deck_data.helpers import (
    make_branching_logic, make_active_recall
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar verme) oranını artırmak için eklenecek ögeler."""
    return {
        2: make_branching_logic(
            "Ciddi bir araba kazası geçiren 24 yaşındaki hastada karaciğerde geniş yırtık ve sol kolda derin bir cilt laserasyonu saptanıyor.",
            "Bu iki organdaki onarım mekanizması karşılaştırıldığında cerrahi ekibin beklentisi ne olmalıdır?",
            [
                {
                    "text": "Karaciğer de kol derisi de kesinlikle yalnızca kalın fibröz skarla iyileşir, hücre bölünmesi olmaz.",
                    "outcome": "Hatalı yaklaşım: Karaciğer stabil dokudur; ECM çatısı sağlamsa kompanse rejenerasyonla kütlesini tamamlar.",
                    "isCorrect": False
                },
                {
                    "text": "Karaciğer parankiminde geride kalan sağlam hepatositler hızla bölünerek kütleyi kompanse ederken; koldaki derin dermis kesisinde granülasyon dokusu ve fibröz skar gelişir.",
                    "outcome": "Kusursuz patolojik muhakeme: Karaciğerin stabil doku rejenerasyonu ile derin cilt yarasının skarla onarımı doğru ayrıştırılır.",
                    "isCorrect": True
                },
                {
                    "text": "Koldaki derin cilt kesisinde hiçbir iz kalmazken, karaciğer tamamen yok olur.",
                    "outcome": "Tam tersi ve bilim dışı bir iddia.",
                    "isCorrect": False
                }
            ]
        ),
        12: make_branching_logic(
            "Laboratuvarda Parkinson ve Tip 1 Diyabet tedavisi için kök hücre araştırması yapan bir biyolog iki kaynak arasında seçim yapıyor: Biri blastokistten elde edilen embriyonik kök hücreler, diğeri kemik iliğinden alınan mezankimal kök hücreler.",
            "Tüm germ yapraklarına ait her türlü hücre tipine (dopaminerjik nöron, beta hücresi) dönüşme potansiyeli arayan araştırmacı hangisini seçmelidir?",
            [
                {
                    "text": "Kemik iliği kök hücreleri (çünkü sadece yetişkinlerde bulunur).",
                    "outcome": "Yetersiz potansiyel: Yetişkin kök hücreler multipotenttir; nöronlara dönüşme kapasiteleri çok sınırlıdır.",
                    "isCorrect": False
                },
                {
                    "text": "Embriyonik kök hücreler (çünkü pluripotenttir ve ektoderm, mezoderm, endoderm kökenli tüm hücrelere dönüşebilir).",
                    "outcome": "Doğru kök hücre biyolojisi seçimi: Pluripotensi her dokuya farklılaşma gücünü sağlar.",
                    "isCorrect": True
                },
                {
                    "text": "Kardiyak miyositler.",
                    "outcome": "Kardiyak miyositler post-mitotik hücrelerdir, kök hücre değildir.",
                    "isCorrect": False
                }
            ]
        ),
        22: make_branching_logic(
            "Hemofili A (Faktör VIII eksikliği) hastasında diş çekimi sonrası kanama pıhtılaşmıyor ve yara iyileşmesi başlayamıyor.",
            "Onarımın ilk basamağını başlatabilmek için hematoloji ve cerrahi ekibinin acil müdahalesi ne olmalıdır?",
            [
                {
                    "text": "Hastaya yüksek doz heparin vererek pıhtıyı eritmek",
                    "outcome": "Ölümcül hata: Kanamayı artırarak hipovolemik şoka sokar.",
                    "isCorrect": False
                },
                {
                    "text": "Faktör VIII konsantresi veya taze donmuş plazma replasmanı yaparak hemostazı sağlamak ve fibrin pıhtısının (geçici matriks) oluşmasını temin etmek",
                    "outcome": "Kusursuz klinik yaklaşım: Fibrin çatısı kurulur, kanama durur ve yara enflamatuar onarım evresine geçer.",
                    "isCorrect": True
                },
                {
                    "text": "Yarayı hiçbir şey yapmadan açık bırakmak",
                    "outcome": "Devam eden kanama ve enfeksiyon riski.",
                    "isCorrect": False
                }
            ]
        ),
        24: make_branching_logic(
            "Cerrahi kesisinin 24. saatinde hastanın yara kenarlarından alınan biyopside yoğun nötrofil infiltrasyonu görülüyor. Asistan hekim 'Bu hastada kesinlikle flegmonöz enfeksiyon var' diyor.",
            "Patoloji hocasının asistana vereceği en doğru eğitim cevabı ne olmalıdır?",
            [
                {
                    "text": "'Haklısın, 24. saatte nötrofil varsa yara mutlaka iltihap kapmıştır, antibiyotik başlayalım.'",
                    "outcome": "Fizyolojik yanılgı: İlk 24 saatte nötrofil akını normal yara iyileşmesinin standart evresidir.",
                    "isCorrect": False
                },
                {
                    "text": "'Yanılıyorsun; akut doku hasarından sonraki ilk 24 saatte nötrofillerin yara yatağına akması fizyolojik akut enflamasyonun doğal ve beklenen ilk basamağıdır; klinik enfeksiyon bulgusu yoksa normal kabul edilir.'",
                    "outcome": "Mükemmel patoloji eğitimi: İlk 24 saatteki fizyolojik nötrofil dalgası doğru kavranır.",
                    "isCorrect": True
                },
                {
                    "text": "'Nötrofiller yara iyileşmesinde asla görülmez, lamlar karışmış.'",
                    "outcome": "Bilim dışı iddia.",
                    "isCorrect": False
                }
            ]
        ),
        32: make_branching_logic(
            "Bir patoloji asistanı mikroskop altında genç granülasyon dokusunu incelerken gördüğü yoğun endotel tomurcuklarını ve damarları malign hemanjiyosarkom tümörü ile karıştırıyor.",
            "Kıdemli patoloğun mikroskop başında granülasyon dokusu lehine göstereceği en temel özellik ne olmalıdır?",
            [
                {
                    "text": "Endotel hücrelerinde atipik mitozlar ve nekroz olması",
                    "outcome": "Bu özellikler malign sarkom lehinedir.",
                    "isCorrect": False
                },
                {
                    "text": "Damarların yüzeye dik, düzenli kapiller ilmekler yapması, endotel atipisinin olmaması ve aralarında aktif fibroblastlar ile ödemli gevşek ECM bulunması",
                    "outcome": "Kusursuz histopatolojik ayrım: Granülasyon dokusunun düzenli reaktif anjiyogenezi doğru teşhis edilir.",
                    "isCorrect": True
                },
                {
                    "text": "Dokuda hiç damar bulunmaması",
                    "outcome": "Granülasyon dokusu aşırı damarlıdır.",
                    "isCorrect": False
                }
            ]
        ),
        34: make_branching_logic(
            "Kronik bir yarada fibroblast proliferasyonunun ve granülasyon dokusunun son derece yetersiz olduğu görülüyor.",
            "Bu yara yatağında eksik olduğu düşünülen ve fibroblast kemotaksisi ile mitozunu en güçlü uyaran faktör hangisidir?",
            [
                {
                    "text": "Histamin ve heparin",
                    "outcome": "Bunlar vazoaktif mediyatörlerdir, fibroblast mitojeni değildir.",
                    "isCorrect": False
                },
                {
                    "text": "PDGF (Trombosit Kaynaklı Büyüme Faktörü) ve FGF-2",
                    "outcome": "Doğru moleküler hedef: PDGF ve FGF fibroblastların yara alanına göçünü ve çoğalmasını sağlayan ana itici güçlerdir.",
                    "isCorrect": True
                },
                {
                    "text": "İnsülin benzeri büyüme faktörü-4",
                    "outcome": "Primer yara fibroblast mitojeni değildir.",
                    "isCorrect": False
                }
            ]
        ),
        44: make_branching_logic(
            "Anjiyogenez araştırmalarında deney hayvanlarına Notch sinyal yolağını bloke eden anti-Dll4 antikoru veriliyor.",
            "Bu biyolojik deneyde yeni oluşan kapiller damarlarda ne tür bir anjiyogenik morfoloji gözlenir?",
            [
                {
                    "text": "Damar oluşumu tamamen durur ve doku avasküler kalır.",
                    "outcome": "Yanlış: Notch baskılanınca tomurcuklanma durmaz, aksine çığırından çıkar.",
                    "isCorrect": False
                },
                {
                    "text": "Tüm endotel hücreleri kontrolsüzce tip hücresi olmaya çalışır; aşırı dallanan ancak içi boş lümeni olmayan kaotik ve işlevsiz damar yumakları oluşur.",
                    "outcome": "Kusursuz moleküler anjiyogenez kavrayışı: Notch/Dll4 lateral inhibisyonunun yokluğunda oluşan anjiyogenik kaos doğru açıklanır.",
                    "isCorrect": True
                },
                {
                    "text": "Tüm damarlar saniyeler içinde arteriyole dönüşür.",
                    "outcome": "Mantık dışı.",
                    "isCorrect": False
                }
            ]
        ),
        54: make_branching_logic(
            "Uzun yol gemi yolculuğunda 4 ay taze gıdaya erişemeyen bir denizcide bacaklarda kanamalar ve 2 yıl önceki apandisit ameliyatı yara izinin tekrar açıldığı (dehisens) görülüyor.",
            "Gemi hekimi olarak bu denizcide acil etiyolojik teşhis ve tedaviniz ne olmalıdır?",
            [
                {
                    "text": "Akut apandisit nüksü düşünülerek gemide acil tekrar ameliyat yapılmalıdır.",
                    "outcome": "Ölümcül cerrahi hata: Hasta apandisit değil, skorbüttür; ameliyat edilirse kanamadan ölür.",
                    "isCorrect": False
                },
                {
                    "text": "Skorbüt (C vitamini eksikliği) tanısıyla hastaya derhal turunçgiller veya C vitamini ampulü verilmeli, kollajen hidroksilasyonu yeniden sağlanmalıdır.",
                    "outcome": "Mükemmel klinik tanı: C vitamini eksikliğinin eski skarları dahi çözdüğü gerçeği hayat kurtarır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaya sadece tuzlu su içirilmelidir.",
                    "outcome": "Tabloyu ağırlaştırır.",
                    "isCorrect": False
                }
            ]
        ),
        62: make_branching_logic(
            "Acrodermatitis enteropathica (genetik çinko emilim bozukluğu) olan bir çocukta cerrahi yara iyileşmesi ve remodeling evresi duruyor.",
            "Bu metabolik tabloda yara iyileşmesinin durmasının hücresel enzim kofaktörü gerekçesi nedir?",
            [
                {
                    "text": "Çinko eksikliğinde Matriks Metalloproteinazların (MMP) çalışamaması ve ECM remodelinginin kilitlenmesi",
                    "outcome": "Kusursuz biyokimyasal patoloji: Çinkonun MMP katalitik merkezindeki vazgeçilmez kofaktör rolü doğru açıklanır.",
                    "isCorrect": True
                },
                {
                    "text": "Çinkonun kanda kalsiyumu bağlayarak kemikleri eritmesi",
                    "outcome": "Yanlış mekanizma.",
                    "isCorrect": False
                },
                {
                    "text": "Mide asidinin tamamen yok olması",
                    "outcome": "Konuyla ilgisi yoktur.",
                    "isCorrect": False
                }
            ]
        ),
        74: make_branching_logic(
            "Geniş bası yarası (dekübitus ülseri) olan yatağa bağımlı bir hastada yara tabanı 10 cm çapında açık bir krater halindedir. Cerrah yarayı zorlayarak dikişle kapatmayı deniyor.",
            "Böyle geniş doku kayıplı bir yarada zorlayarak primer kapatma yapmanın en büyük riski nedir?",
            [
                {
                    "text": "Yaranın anında kansere dönüşmesi",
                    "outcome": "Primer kapatma kanser yapmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Aşırı gerilim nedeniyle yara kenarlarının iskemik nekroza uğraması, dikişlerin patlaması ve derin doku enfeksiyonu gelişmesi; bu nedenle yara sekonder iyileşmeye bırakılmalıdır.",
                    "outcome": "Doğru cerrahi prensip: Geniş defektlerde gerilimsiz onarım esastır; sekonder iyileşme veya greftleme tercih edilmelidir.",
                    "isCorrect": True
                },
                {
                    "text": "Yaranın tamamen skarsız rejenere olması",
                    "outcome": "Böyle derin bir yara skarsız rejenere olamaz.",
                    "isCorrect": False
                }
            ]
        ),
        82: make_branching_logic(
            "HbA1c düzeyi %11 olan kontrolsüz diyabetik bir hastada sol ayak tabanında ağrısız, derin, etrafı hiperkeratozlu bir ülser saptanıyor.",
            "Yara bakımında antibiyotik ve pansumana ek olarak iyileşmeyi sağlayacak en kritik sistemik hamle ne olmalıdır?",
            [
                {
                    "text": "Hastanın kan şekerini regüle etmek için agresif insülin tedavisi başlamak ve ayağı basıdan korumak (off-loading)",
                    "outcome": "Mükemmel diyabetik yara yönetimi: Nötrofil fonksiyonları düzelir, doku glikozilasyonu kırılır ve off-loading ile bası kalkar.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaya günde 5 km tempolu yürüyüş yaptırmak",
                    "outcome": "Ayak tabanına bası bindirerek ülseri kemiğe (osteomiyelite) kadar derinleştirir.",
                    "isCorrect": False
                },
                {
                    "text": "Yaraya hiç dokunmayıp sadece insülin vermeyi reddetmek",
                    "outcome": "Ayak ampütasyonuyla sonuçlanır.",
                    "isCorrect": False
                }
            ]
        ),
        86: make_branching_logic(
            "Göğüs ön duvarında kaynar çorba dökülmesi sonrası derin yanık geçiren 16 yaşındaki hastada 3 ay sonra yanık çizgisi üzerinde deriden kabarık, sert, kırmızı lezyonlar beliriyor. Lezyonların yanık alanının sınırları içinde kaldığı görülüyor.",
            "Bu hastada tanı ve klinik prognoz hakkında aileye ne söylenmelidir?",
            [
                {
                    "text": "'Bu bir keloiddir, asla geçmez ve tüm vücudunuza yayılacaktır.'",
                    "outcome": "Yanlış ve gereksiz panik: Sınırları aşmadığı için keloid değil, hipertrofik skardır.",
                    "isCorrect": False
                },
                {
                    "text": "'Bu bir hipertrofik skardır; lezyon yara sınırları içinde kalmıştır ve zamanla (aylar-yıllar içinde) kendiliğinden gerileyip solma eğilimindedir.'",
                    "outcome": "Kusursuz klinik tanı: Hipertrofik skarın sınırda kalma ve regresyon kuralı aileye doğru aktarılır.",
                    "isCorrect": True
                },
                {
                    "text": "'Derhal tüm göğüs derisini ameliyatla kesip çıkarmalıyız.'",
                    "outcome": "Gereksiz cerrahi travma.",
                    "isCorrect": False
                }
            ]
        ),
        92: make_branching_logic(
            "Kronik Hepatit B hastasının karaciğer biyopsisinde Disse aralıklarında yoğun kollajen birikimi ve sinüzoid kapillerizasyonu saptanıyor.",
            "Bu hastada portal hipertansiyon gelişimini başlatan temel hücresel dönüşüm hangisidir?",
            [
                {
                    "text": "Kupffer hücrelerinin alyuvara dönüşmesi",
                    "outcome": "Biyolojik olarak imkansız.",
                    "isCorrect": False
                },
                {
                    "text": "Hepatik stellat (İto) hücrelerinin A vitaminini kaybederek miyofibroblasta dönüşmesi ve sinüzoid pencerelerini kapatan Tip I kollajen üretmesi",
                    "outcome": "Doğru patogenetik mekanizma: Karaciğer sirozunun kilit hücresi İto hücresinin miyofibroblastik dönüşümüdür.",
                    "isCorrect": True
                },
                {
                    "text": "Safra kesesinin aşırı kasılarak karaciğeri ezmesi",
                    "outcome": "Konu dışı.",
                    "isCorrect": False
                }
            ]
        ),
        96: make_branching_logic(
            "Akut lösemi nedeniyle allojenik kemik iliği nakli yapılan 40 yaşındaki hastada nakilden 25 gün sonra yaygın cilt döküntüsü, sarılık ve günde 2 litreye varan yeşil sulu diyare başlıyor.",
            "Bu dramatik klinik tablonun immünopatolojik tanısı ve nedeni nedir?",
            [
                {
                    "text": "Basit bir besin zehirlenmesidir, yoğurt verilmelidir.",
                    "outcome": "Ölümcül tıbbi körlük: Tablo hayatı tehdit eden akut GVHD'dir.",
                    "isCorrect": False
                },
                {
                    "text": "Akut Graft-Versus-Host Hastalığıdır (GVHD); donör kemik iliğindeki T lenfositleri alıcının deri, karaciğer ve bağırsak epitelini yabancı görerek saldırmaktadır.",
                    "outcome": "Kusursuz klinik tanı: GVHD'nin klasik üçlü hedef organı (deri, karaciğer, GIS) ve mekanizması doğru teşhis edilir.",
                    "isCorrect": True
                },
                {
                    "text": "Alıcının böbrek naklini reddetmesidir.",
                    "outcome": "Hasta kemik iliği nakli olmuştur, böbrek nakli değil.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_recall():
    """Active recall (aktif hatırlama) oranını artırmak için eklenecek ögeler."""
    return {
        4: make_active_recall(
            "Gastrointestinal sistem mukozasındaki labil epitel hücrelerinin sürekli yenilenmesini sağlayan kök hücreler tam olarak nerede yerleşiktir?",
            "İnce ve kalın bağırsak Liberkühn kriptlerinin en tabanında (Lgr5+ kript kök hücreleri) yerleşiktir.",
            "Bağırsak bezlerinin dip kısmı"
        ),
        14: make_active_recall(
            "Parsiyel hepatektomide karaciğerin üçte ikisi cerrahi olarak çıkarıldığında geride kalan dokunun eski ağırlığına ulaşma süresi yaklaşık ne kadardır?",
            "Yaklaşık 1 ila 2 hafta gibi son derece kısa bir sürede orijinal ağırlığına ulaşır.",
            "Haftalık büyüme takvimi"
        ),
        26: make_active_recall(
            "Akut enflamasyonun onarıma evrilmesinde M1 makrofajların mikropları öldüren ana enzimi ile M2 makrofajların kollajen öncülü üreten ana enzimi hangileridir?",
            "M1'de indüklenebilir nitrik oksit sentaz (iNOS); M2'de ise prolin sentezini başlatan arginaz-1 enzimidir.",
            "Biri NO diğeri ornitin yapan enzimler"
        ),
        36: make_active_recall(
            "Granülasyon dokusunda endotel hücreleri arasında henüz sıkı bağlantıların kurulamamış olmasının yara yatağında yarattığı karakteristik klinik bulgu nedir?",
            "Yüksek oranda plazma sızıntısına bağlı doku ödemi ve yaranın sürekli nemli/eksudalı olmasıdır.",
            "Sıvı birikimi klinik durumu"
        ),
        42: make_active_recall(
            "Anjiyogenez sırasında perisitlerin endotelden ayrılarak damarı tomurcuklanmaya açmasını sağlayan Tie-2 reseptör antagonisti molekül nedir?",
            "Angiopoietin-2 (Ang-2) molekülüdür.",
            "Perisitleri çözen ikinci faktör"
        ),
        46: make_active_recall(
            "Hücre içi oksijen seviyesi düştüğünde parçalanmaktan kurtularak çekirdeğe giren ve VEGF-A üretimini başlatan transkripsiyon faktörü hangisidir?",
            "HIF-1alfa (Hipoksi İle İndüklenen Faktör-1alfa) transkripsiyon faktörüdür.",
            "Oksijensizlikte aktive olan faktör"
        ),
        52: make_active_recall(
            "Deri, kemik ve tendon gibi mekanik gerilime en dayanıklı dokularda ve olgun skar dokusunda bulunan hakim kollajen türü hangisidir?",
            "Tip I fibriler kollajendir.",
            "En yaygın ve sert kollajen numarası"
        ),
        56: make_active_recall(
            "Miyofibroblastların yara kontraksiyonunu gerçekleştirirken sitoplazmalarında bol miktarda eksprese ettikleri kasılma proteini nedir?",
            "Alfa-düz kas aktinidir (α-SMA).",
            "Düz kaslara özgü aktin izoformu"
        ),
        64: make_active_recall(
            "Ekstrasellüler matrikste MMP enzimlerinin kollajeni kontrolsüzce sindirmesini önleyen doku inhibitörlerine ne ad verilir?",
            "TIMP (Tissue Inhibitors of Metalloproteinases / Doku Metalloproteinaz İnhibitörleri) adı verilir.",
            "MMP'yi bloke eden kısaltma"
        ),
        72: make_active_recall(
            "Temiz cerrahi bir insizyonda dikişler alındığında (1. hafta) yaranın gerilme direnci sağlam derinin yaklaşık ne kadarı kadardır?",
            "Sağlam derinin yalnızca yüzde 10'u (%10) kadardır.",
            "Dikiş alımındaki zayıf direnç yüzdesi"
        ),
        84: make_active_recall(
            "Yara iyileşmesini geciktiren lokal faktörler içerisinde klinikte en sık rastlanan birincil neden nedir?",
            "Yara yeri enfeksiyonudur (bakteriyel kontaminasyon).",
            "Mikropların yerleşmesi durumu"
        ),
        94: make_active_recall(
            "Kronik böbrek yetmezliğinde glomerüllerin fonksiyonel kapiller yumaklarını kaybedip asellüler pembe bağ dokusuna dönüşmesine ne ad verilir?",
            "Glomerüloskleroz (küresel böbrek sklerozu) adı verilir.",
            "Glomerülün taşlaşması terimi"
        )
    }

def enrich_slides(slides):
    """Slayt listesini alır ve eklenen elemanlarla zenginleştirip dengeli olarak geri döndürür."""
    branching_map = get_extra_branching()
    recall_map = get_extra_recall()

    for idx, slide in enumerate(slides, start=1):
        if idx in branching_map:
            slide["elements"].append(branching_map[idx])
        if idx in recall_map:
            slide["elements"].append(recall_map[idx])

    return slides
