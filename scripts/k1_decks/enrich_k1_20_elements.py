# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 (hedef %12-16) oranına ulaşmasını sağlar.
"""

from scripts.k1_20_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik karar verme, acil vaka yönetimi ve tanı algoritmaları) ögeleri."""
    return {
        3: make_branching_logic(
            "Acil servise ani başlayan tek taraflı göğüs ağrısı ve nefes darlığı ile başvuran genç bir kadında yapılan tetkiklerde pıhtılaşma kaskadının aşırı aktive olduğu ve endotel yüzeyinde fizyolojik antitrombotik dengenin bozulduğu görülüyor.",
            "Normal endotelin trombosit adezyonunu engelleyen ve vazodilatasyon yapan en temel iki salgısı hangisidir?",
            [
                {
                    "text": "Prostasiklin (PGI2) ve Nitrik Oksit (NO)",
                    "outcome": "Doğru karar: Sağlıklı endotel PGI2 ve NO salgılayarak trombosit agregasyonunu güçlü şekilde inhibe eder ve lümeni açık tutar.",
                    "isCorrect": True
                },
                {
                    "text": "Tromboksan A2 ve Endotelin",
                    "outcome": "Hatalı: Bunlar endotel veya trombosit hasarında salınan protrombotik ve vazokonstriktör ajanlardır.",
                    "isCorrect": False
                },
                {
                    "text": "Von Willebrand Faktör ve Doku Faktörü",
                    "outcome": "Hatalı: vWF ve doku faktörü hemostazı ve trombozu başlatan prokoagülan moleküllerdir.",
                    "isCorrect": False
                }
            ]
        ),
        6: make_branching_logic(
            "Yoğun bakımda sepsis nedeniyle takip edilen hastada yaygın intravasküler koagülasyon (DIC) gelişiyor. Mikrodolaşımda yaygın mikrotrombüsler oluşurken endotel yüzeyindeki trombomodulin aktivitesinin çöktüğü belirleniyor.",
            "Trombomodulinin endotel yüzeyinde trombin ile birleşerek aktive ettiği doğal antikoagülan sistem hangisidir?",
            [
                {
                    "text": "Protein C ve Protein S yolak sistemi",
                    "outcome": "Doğru karar: Trombomodulin trombini bağlayarak antikoagülan bir enzime dönüştürür ve Protein C'yi aktive eder; aktif Protein C ise FVa ve FVIIIa'yı parçalar.",
                    "isCorrect": True
                },
                {
                    "text": "Faktör XII kontakt aktivasyon sistemi",
                    "outcome": "Hatalı: FXII intrinsik koagülasyon yolağını başlatır, antikoagülan değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Siklooksijenaz-1 enzimatik yolağı",
                    "outcome": "Hatalı: COX-1 trombosit aktivasyonuyla ilgilidir.",
                    "isCorrect": False
                }
            ]
        ),
        13: make_branching_logic(
            "Kronik sigara içicisi 55 yaşındaki hipertansif hastada koroner arter aterosklerotik plağının yüzeyinde endotel denudasyonu meydana geliyor. Endotel altındaki ekstrasellüler matriks açığa çıkıyor.",
            "Subendotelyal kollajen ile trombosit GpIb reseptörü arasında köprü kurarak adezyonu başlatan temel molekül hangisidir?",
            [
                {
                    "text": "Von Willebrand Faktör (vWF)",
                    "outcome": "Doğru karar: vWF endotel Weibel-Palade cisimciklerinden salınarak subendotelyal kollajen ile trombosit GpIb arasına bağlanır.",
                    "isCorrect": True
                },
                {
                    "text": "Plazminojen Aktivatör İnhibitörü-1 (PAI-1)",
                    "outcome": "Hatalı: PAI-1 fibrinolizi baskılar, adezyon köprüsü kurmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Fibrinojen",
                    "outcome": "Hatalı: Fibrinojen iki trombosit arasındaki agregasyonda GpIIb/IIIa reseptörlerine bağlanır, adezyonda primer rol oynamaz.",
                    "isCorrect": False
                }
            ]
        ),
        17: make_branching_logic(
            "Homosistinüri tanılı 18 yaşındaki bir gençte tekrarlayan venöz ve arteriyel tromboz atakları gözleniyor. Biyokimyasal incelemede kanda serbest homosistein düzeyi aşırı yüksek saptanıyor.",
            "Homosistein yüksekliğinin vasküler sistemde tromboza yol açan primer patolojik etkisi nedir?",
            [
                {
                    "text": "Direkt endotel hücresi hasarı oluşturarak oksidatif stresi artırması ve endotelyal disfonksiyon yaratması",
                    "outcome": "Doğru karar: Homosistein serbest oksijen radikalleri üreterek endotelde doğrudan nekroz ve prokoagülan fenotip indükler.",
                    "isCorrect": True
                },
                {
                    "text": "K vitamini sentezini artırarak pıhtılaşma faktörlerini çoğaltması",
                    "outcome": "Hatalı: Homosistein K vitamini sentezini etkilemez.",
                    "isCorrect": False
                },
                {
                    "text": "Trombosit sayısını bir milyonun üzerine çıkarması",
                    "outcome": "Hatalı: Homosistein trombositoz yapmaz, endotel hasarı yapar.",
                    "isCorrect": False
                }
            ]
        ),
        23: make_branching_logic(
            "Atriyal fibrilasyonu olan 70 yaşındaki hastanın sol atriyumunda kan akımının yavaşladığı ve türbülanslı girdaplar oluştuğu ekokardiyografide izleniyor.",
            "Kardiyak odacıklarda veya genişlemiş venlerde kan akım hızının yavaşlaması (staz) trombozu hangi mekanizmayla tetikler?",
            [
                {
                    "text": "Trombositlerin damar duvarına temasını (marjinasyon) kolaylaştırır ve aktif pıhtılaşma faktörlerinin temizlenmesini engeller.",
                    "outcome": "Doğru karar: Staz durumunda eritrositler merkezde toplanırken trombositler endotel yüzeyine itilir ve faktörler lümende birikir.",
                    "isCorrect": True
                },
                {
                    "text": "Endotelden t-PA salgısını aşırı artırarak pıhtıyı eritir.",
                    "outcome": "Hatalı: t-PA artışı tromboz yapmaz, tam tersine pıhtıyı çözer.",
                    "isCorrect": False
                },
                {
                    "text": "Kanın hematokrit değerini sıfıra indirir.",
                    "outcome": "Hatalı: Staz hematokriti düşürmez.",
                    "isCorrect": False
                }
            ]
        ),
        27: make_branching_logic(
            "Uzun süreli kıtalararası uçak yolculuğu (12 saat) yapan 42 yaşındaki obez bir yolcuda yolculuk sonrası sol bacakta şişlik ve baldır ağrısı gelişiyor.",
            "Bu yolcuda venöz tromboza zemin hazırlayan temel hemodinamik bozukluk hangisidir?",
            [
                {
                    "text": "Oturur pozisyonda hareketsiz kalmaya bağlı alt ekstremite venöz stazı ve baldır kas pompasının çalışmaması",
                    "outcome": "Doğru karar: Uzun süreli hareketsizlik kas pompasını durdurur, kapak ceplerinde kan stazına ve DVT'ye yol açar.",
                    "isCorrect": True
                },
                {
                    "text": "Uçak kabinindeki yüksek oksijen konsantrasyonuna bağlı vazokonstriksiyon",
                    "outcome": "Hatalı: Kabin içi hipoksi ve düşük kabin basıncı vardır, staz asıl faktördür.",
                    "isCorrect": False
                },
                {
                    "text": "Hızlı yürümeye bağlı arteriyel kayma gerilimi artışı",
                    "outcome": "Hatalı: Hareketsizlik söz konusudur.",
                    "isCorrect": False
                }
            ]
        ),
        33: make_branching_logic(
            "Genç yaşta açıklanamayan DVT atağı geçiren 24 yaşındaki erkek hastada aktive Protein C rezistansı (APCR) pozitif saptanıyor. Genetik testte Faktör V geninde G1691A mutasyonu doğrulanıyor.",
            "Faktör V Leiden mutasyonunda pıhtılaşma sisteminin kontrolsüz kalmasının moleküler gerekçesi nedir?",
            [
                {
                    "text": "Aktif Protein C'nin Faktör Va molekülünü kesip inaktive ettiği 506. pozisyondaki arjinin kalıntısının glutamine dönüşmesi ve APC'ye direnç kazanması",
                    "outcome": "Doğru karar: Arg506Gln mutasyonu APC'nin Faktör Va'yı parçalamasını engeller ve pıhtılaşma frenlenemez.",
                    "isCorrect": True
                },
                {
                    "text": "Faktör V'in doğrudan antitrombin III'e bağlanarak onu yok etmesi",
                    "outcome": "Hatalı: Faktör V antitrombini yok etmez.",
                    "isCorrect": False
                },
                {
                    "text": "Karaciğerde fibrinojen üretiminin on katına çıkması",
                    "outcome": "Hatalı: FV Leiden mutasyonu fibrinojen genini etkilemez.",
                    "isCorrect": False
                }
            ]
        ),
        37: make_branching_logic(
            "Tekrarlayan derin ven trombozları olan bir hastada plazma Antitrombin III (ATIII) düzeyi %30 olarak ölçülüyor. Hastaya standart dozda intravenöz heparin başlanmasına rağmen aPTT süresi hiç uzamıyor (heparin direnci).",
            "Bu hastada heparinin etkisiz kalmasının nedeni nedir ve yönetimde ne yapılmalıdır?",
            [
                {
                    "text": "Heparin antikoagülan etkisini ATIII üzerinden gösterdiğinden ATIII eksikliğinde etkisizdir; taze donmuş plazma veya ATIII konsantresi verilmelidir.",
                    "outcome": "Doğru karar: Heparin bir kofaktördür; ortamda ATIII olmadan trombin ve FXa'yı inhibe edemez.",
                    "isCorrect": True
                },
                {
                    "text": "Heparin dozu 50 katına çıkarılmalıdır çünkü heparin tek başına tüm pıhtıyı çözer.",
                    "outcome": "Hatalı ve tehlikeli: ATIII yokken heparin dozunu kontrolsüz artırmak çözüm değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Hastaya acil yüksek doz K vitamini enjeksiyonu yapılmalıdır.",
                    "outcome": "Hatalı: K vitamini prokoagülandır, trombozu daha da şiddetlendirir.",
                    "isCorrect": False
                }
            ]
        ),
        43: make_branching_logic(
            "Sistemik Lupus Eritematozus tanılı 29 yaşındaki kadın hastada 2 kez ikinci trimester gebelik kaybı ve sol bacakta DVT öyküsü bulunuyor. Laboratuvarda aPTT süresi uzamış saptanıyor.",
            "Antifosfolipid antikor sendromunda (APS) in vitro aPTT uzamasına rağmen in vivo ortamda tromboz gelişmesinin paradoksal mekanizması nedir?",
            [
                {
                    "text": "Antikorlar test tüpündeki fosfolipidleri bağlayarak testi yalancı uzatır; ancak in vivo endotel ve trombositleri aktive ederek güçlü hiperkoagülabilite oluşturur.",
                    "outcome": "Doğru karar: APS'nin en meşhur laboratuvar paradoksudur; in vitro antikoagülan, in vivo güçlü protrombotiktir.",
                    "isCorrect": True
                },
                {
                    "text": "Hastada hemofili A hastalığı da aynı anda bulunmaktadır.",
                    "outcome": "Hatalı: Hemofili kanama yapar, tromboz yapmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Antikorlar tüm pıhtılaşma faktörlerini parçalayarak yok etmiştir.",
                    "outcome": "Hatalı: Yaygın faktör yokluğu tromboz değil kanama tablosu oluşturur.",
                    "isCorrect": False
                }
            ]
        ),
        47: make_branching_logic(
            "Pulmoner emboli nedeniyle standart fraksiyone olmayan heparin infüzyonu alan hastada tedavinin 6. gününde trombosit sayısı 280.000'den 85.000'e düşüyor ve diğer bacakta yeni bir akut DVT gelişiyor.",
            "Heparin Kaynaklı Trombositopeni Tip 2 (HIT-2) şüphesinde derhal yapılması gereken ilk hayat kurtarıcı adım nedir?",
            [
                {
                    "text": "Heparinin tüm formları derhal kesilmeli ve direkt trombin inhibitörü (argatroban) başlanmalıdır.",
                    "outcome": "Doğru karar: HIT-2'de heparin derhal kesilmeli, asla DMAH veya varfarin verilmemeli, non-heparin antikoagülan (argatroban) başlanmalıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Trombosit süspansiyonu transfüzyonu yapılmalı ve heparin dozu iki katına çıkarılmalıdır.",
                    "outcome": "Ölümcül hata: HIT-2'de trombosit vermek trombozu alevlendirir, heparin devamı felakete yol açar.",
                    "isCorrect": False
                },
                {
                    "text": "Hiçbir şey yapılmadan 1 hafta beklenmelidir.",
                    "outcome": "Hatalı: HIT-2 mortalitesi %20-30 olan acil bir tromboz tablosudur.",
                    "isCorrect": False
                }
            ]
        ),
        53: make_branching_logic(
            "Pankreas gövde karsinomu tanısı alan 63 yaşındaki hastada kolda ve bacaklarda yer değiştiren, ağrılı venöz kordonlar (tromboflebitis migrans / Trousseau sendromu) gelişiyor.",
            "Müsin salgılayan adenokarsinomlarda görülen bu gezici venöz trombozların altta yatan temel paraneoplastik mekanizması nedir?",
            [
                {
                    "text": "Tümör hücrelerinden kana salınan prokoagülan müsin molekülleri ve doku faktörünün pıhtılaşma kaskadını sistemik olarak aktive etmesi",
                    "outcome": "Doğru karar: Müsin ve tümör doku faktörü Faktör X'i doğrudan aktive ederek Trousseau fenomenine yol açar.",
                    "isCorrect": True
                },
                {
                    "text": "Kanser hücrelerinin kemik iliğinde aşırı lenfosit üretmesi",
                    "outcome": "Hatalı: Trousseau sendromu lenfosit artışıyla ilgili değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Pankreas enzimlerinin portal vende pıhtıyı tamamen eritmesi",
                    "outcome": "Hatalı: Pıhtı erimesi değil kontrolsüz tromboz söz konusudur.",
                    "isCorrect": False
                }
            ]
        ),
        57: make_branching_logic(
            "Menenjit ön tanısıyla acile getirilen 8 yaşındaki çocukta yaygın purpurik deri döküntüleri, hipotansiyon ve bilateral adrenal bezlerde masif hemorajik nekroz (Waterhouse-Friderichsen sendromu) saptanıyor.",
            "Bu hastada pıhtılaşma faktörlerinin ve trombositlerin tükenmesi sonucu hem mikrotromboz hem şiddetli kanamanın bir arada görüldüğü tablo nedir?",
            [
                {
                    "text": "Yaygın İntravasküler Koagülasyon (DIC)",
                    "outcome": "Doğru karar: Meningokoksemide endotoksin etkisiyle gelişen akut dekompanse DIC tablosu tüketim koagülopatisi ve adrenal kanamaya yol açar.",
                    "isCorrect": True
                },
                {
                    "text": "İdiopatik Trombositopenik Purpura (ITP)",
                    "outcome": "Hatalı: ITP mikrotrombüs ve adrenal nekroz yapmaz, sadece izole trombosit otoantikorudur.",
                    "isCorrect": False
                },
                {
                    "text": "Hemofili B",
                    "outcome": "Hatalı: Hemofili B Faktör IX eksikliğidir, DIC gibi mikrotrombüs ve şok oluşturmaz.",
                    "isCorrect": False
                }
            ]
        ),
        63: make_branching_logic(
            "Koroner anjiyografi yapılan akut anterior STEMI hastasında sol ön inen arterde (LAD) tam tıkayıcı bir trombüs saptanıyor. Trombüsün mikroskobik incelemesinde trombosit ve fibrin ağlarının hakim olduğu görülüyor.",
            "Arteriyel lümende yüksek akım hızına rağmen gelişen bu pıhtı tipine ne ad verilir ve tedavide neden antiplateletler esastır?",
            [
                {
                    "text": "Beyaz trombüs; endotel hasarı zemininde primer olarak trombosit agregatları ile oluştuğundan antiplateletler kilit role sahiptir.",
                    "outcome": "Doğru karar: Arteriyel beyaz trombüsler trombosit zengin olduğundan aspirin ve P2Y12 blokerleri temel tedavidir.",
                    "isCorrect": True
                },
                {
                    "text": "Kırmızı staz trombüsü; eritrosit yığınlarından oluştuğu için sadece demir bağlayıcılar verilir.",
                    "outcome": "Hatalı: Arterde beyaz trombüs görülür, kırmızı trombüs venöz stazda oluşur.",
                    "isCorrect": False
                },
                {
                    "text": "Marantik trombüs; sadece kanserli dokularda oluşur.",
                    "outcome": "Hatalı: Koroner aterom plak rüptürü marantik endokardit değildir.",
                    "isCorrect": False
                }
            ]
        ),
        67: make_branching_logic(
            "Femoral vende lümeni tıkayan bir kitle saptanan hastada Doppler USG'de akım izlenmiyor. Patoloji örneğinde yoğun eritrosit ağları ve fibrin izlenirken Zahn çizgilerinin belirgin olmadığı görülüyor.",
            "Düşük basınçlı venöz sistemde staz zemininde gelişen bu pıhtı türünün patolojik adı nedir?",
            [
                {
                    "text": "Kırmızı trombüs (Staz pıhtısı / Flebotromboz)",
                    "outcome": "Doğru karar: Venöz sistemde yavaş akım eritrositlerin pıhtıya hapsolmasına yol açarak kırmızı trombüsü meydana getirir.",
                    "isCorrect": True
                },
                {
                    "text": "Beyaz arteriyel trombüs",
                    "outcome": "Hatalı: Venöz trombüsler eritrosit zengin kırmızı pıhtılardır.",
                    "isCorrect": False
                },
                {
                    "text": "Mural aortik trombüs",
                    "outcome": "Hatalı: Femoral ven tutulmuştur, aort değildir.",
                    "isCorrect": False
                }
            ]
        ),
        73: make_branching_logic(
            "Sol ventrikül apeksinde transmural MI sonrası akinetik keseleşme saptanan hastanın ekokardiyografisinde duvara yapışık 3 cm'lik düzensiz ekojen kitle izleniyor.",
            "Bu mural trombüsün serbestleşerek kopması durumunda embolusun en sık gitmesi beklenen organ hangisidir?",
            [
                {
                    "text": "Beyin (Serebral arterler - İskemik İnme)",
                    "outcome": "Doğru karar: Sol kalpten çıkan sistemik arteriyel embolusların en sık hedefi serebral dolaşımdır (%70'in üzerinde inme ile sonlanır).",
                    "isCorrect": True
                },
                {
                    "text": "Akciğer (Pulmoner arter yatağı)",
                    "outcome": "Hatalı: Sol kalpten çıkan pıhtı sistemik arteriyel dolaşıma gider, akciğere değil.",
                    "isCorrect": False
                },
                {
                    "text": "Karaciğer portal veni",
                    "outcome": "Hatalı: Aorttan portal vene doğrudan emboli geçişi anatomik olarak mümkün değildir.",
                    "isCorrect": False
                }
            ]
        ),
        77: make_branching_logic(
            "Adli tıp otopsisinde sağ femoral ven açıldığında lümenden kalıp şeklinde kolayca çıkan, jelatinimsi, duvara hiç yapışmamış ve üst kısmı sarı tavuk yağı renginde bir kitle elde ediliyor.",
            "Adli patoloğun bu kitleye ilişkin resmi rapor kararı ne olmalıdır?",
            [
                {
                    "text": "Ölüm sonrası (postmortem) durağan kanda sedimantasyonla oluşmuş pıhtıdır; antemortem tromboz değildir.",
                    "outcome": "Doğru karar: Duvara yapışmama, jelatinöz kıvam ve tavuk yağı görünümü postmortem pıhtının kesin kanıtıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Canlıyken oluşmuş ölümcül organize antemortem trombüstür.",
                    "outcome": "Hatalı: Antemortem trombüs duvara sıkıca yapışıktır ve Zahn çizgileri içerir.",
                    "isCorrect": False
                },
                {
                    "text": "Malign endotelyal anjiyosarkom tümör kitlesidir.",
                    "outcome": "Hatalı: Postmortem kan pıhtısıdır, neoplazm değildir.",
                    "isCorrect": False
                }
            ]
        ),
        83: make_branching_logic(
            "Ortopedi servisinde diz protezi ameliyatı sonrası 4. günde aniden fenalaşan, nefes darlığı, göğüs ağrısı ve hipotansiyon gelişen hastada BT pulmoner anjiyografide bilateral ana pulmoner arter bifurkasyonunda dev pıhtı saptanıyor.",
            "Ana pulmoner çatallanmayı tıkayarak ani ölüme yol açabilen bu özel venöz emboli tipi hangisidir?",
            [
                {
                    "text": "Semer Emboli (Saddle Embolus)",
                    "outcome": "Doğru karar: Pulmoner bifurkasyona oturan masif embolus semer emboli olarak adlandırılır ve sağ ventrikül yetmezliğiyle ani kardiyak arreste yol açar.",
                    "isCorrect": True
                },
                {
                    "text": "Paradoksal Emboli",
                    "outcome": "Hatalı: Paradoksal emboli sağdan sola intrakardiyak şantla sistemik dolaşıma geçen embolidir.",
                    "isCorrect": False
                },
                {
                    "text": "Hava Embolisi",
                    "outcome": "Hatalı: DVT kaynaklı tromboembolizmdir.",
                    "isCorrect": False
                }
            ]
        ),
        87: make_branching_logic(
            "Atriyal fibrilasyonu olan 68 yaşındaki hastada aniden sağ bacakta şiddetli ağrı, solukluk, soğukluk ve femoral nabız altında nabız alınamaması (akut ekstremite iskemisi) gelişiyor.",
            "Bu klinik tablonun en olası nedeni ve acil cerrahi yaklaşım nedir?",
            [
                {
                    "text": "Sol kalpten kaynaklanan arteriyel kardiyoembolizm; acil Fogarty kateter embolektomisi uygulanmalıdır.",
                    "outcome": "Doğru karar: Akut bacak iskemisinde kardiyoembolizm ilk akla gelmeli ve bacak nekrozunu önlemek için acil embolektomi yapılmalıdır.",
                    "isCorrect": True
                },
                {
                    "text": "Yüzeyel varis kanaması; sadece bacak yukarı kaldırılmalıdır.",
                    "outcome": "Hatalı: Nabızsızlık ve solukluk arteriyel tıkanmayı gösterir.",
                    "isCorrect": False
                },
                {
                    "text": "Bacakta venöz kapak yetmezliği; varis ameliyatı planlanmalıdır.",
                    "outcome": "Hatalı: Tablo akut arteriyel iskemidir, elektif venöz cerrahi yeri yoktur.",
                    "isCorrect": False
                }
            ]
        ),
        91: make_branching_logic(
            "Akut koroner sendrom geçiren ve koroner stent takılan hastaya dual antiplatelet tedavi (Aspirin + Klopidogrel) planlanıyor.",
            "Klopidogrelin trombositler üzerindeki moleküler etki mekanizması nedir?",
            [
                {
                    "text": "Trombosit yüzeyindeki P2Y12 ADP reseptörünü bloke ederek trombosit aktivasyonunu engeller.",
                    "outcome": "Doğru karar: Klopidogrel bir P2Y12 reseptör antagonistidir ve ADP aracılı agregasyonu durdurur.",
                    "isCorrect": True
                },
                {
                    "text": "COX-1 enzimini inhibe ederek TxA2 sentezini durdurur.",
                    "outcome": "Hatalı: Bu aspirinin mekanizmasıdır.",
                    "isCorrect": False
                },
                {
                    "text": "Faktör Xa'yı doğrudan parçalar.",
                    "outcome": "Hatalı: Klopidogrel antikoagülan değil antiplatelettir.",
                    "isCorrect": False
                }
            ]
        ),
        95: make_branching_logic(
            "Akut iskemik inme semptomları başlayan 62 yaşındaki hasta semptomların 2. saatinde acil servise ulaştırılıyor. Beyin BT'de kanama saptanmıyor.",
            "Bu hastada pıhtıyı çözerek nörolojik fonksiyonları kurtarmak amacıyla intravenöz yolla uygulanması gereken trombolitik ajan hangisidir?",
            [
                {
                    "text": "Rekombinant Doku Plazminojen Aktivatörü (Alteplaz / rt-PA)",
                    "outcome": "Doğru karar: İlk 4.5 saatlik altın pencere içinde intravenöz rt-PA iskemik inmede pıhtıyı eriterek reperfüzyon sağlayan kanıtlanmış tedavidir.",
                    "isCorrect": True
                },
                {
                    "text": "Oral Varfarin yüklemesi",
                    "outcome": "Hatalı: Varfarin pıhtıyı eritmez, etkisi günler sonra başlar ve akut inmede verilmez.",
                    "isCorrect": False
                },
                {
                    "text": "Subkutan Düşük Molekül Ağırlıklı Heparin",
                    "outcome": "Hatalı: DMAH akut inmede pıhtı eritici değildir.",
                    "isCorrect": False
                }
            ]
        ),
        99: make_branching_logic(
            "Hemostazı bozmadan ve majör kanama riski oluşturmadan patolojik trombozu önlemeyi hedefleyen yeni nesil antikoagülan klinik araştırmaları hangi faktörü hedeflemektedir?",
            "Geleceğin ideal antitrombotik adayı olan bu moleküler hedef hangisidir?",
            [
                {
                    "text": "Faktör XIa (ve Faktör XIIa)",
                    "outcome": "Doğru karar: Kontakt yolak faktörlerinin eksikliği ciddi kanama yapmazken tromboza karşı tam koruma sağlar; bu nedenle FXIa inhibitörleri en umut verici yeni sınıftır.",
                    "isCorrect": True
                },
                {
                    "text": "Fibrinojen (Faktör I)",
                    "outcome": "Hatalı: Fibrinojen bloke edilirse hasta fatal kontrolsüz kanamalardan kaybedilir.",
                    "isCorrect": False
                },
                {
                    "text": "Faktör II (Protrombin)",
                    "outcome": "Hatalı: Trombin hemostaz için vazgeçilmezdir, tam blokajı ağır kanama yapar.",
                    "isCorrect": False
                }
            ]
        ),
        31: make_branching_logic(
            "Hiperlipidemisi olan 52 yaşındaki hastada karotis bifurkasyonunda üfürüm duyuluyor. Doppler ultrasonda akım hızının arttığı ve lokal türbülans girdapları oluştuğu görülüyor.",
            "Bu hemodinamik türbülansın damar endoteli üzerindeki en tehlikeli patofizyolojik sonucu nedir?",
            [
                {
                    "text": "Endotel disfonksiyonu ve intimal erozyon yaratarak subendotelyal kolajenin açığa çıkması ve trombosit adhezyonunu tetiklemesi",
                    "outcome": "Doğru karar: Türbülans mekanik kayma gerilimini bozarak endotel hasarına ve trombüs oluşumuna zemin hazırlar.",
                    "isCorrect": True
                },
                {
                    "text": "Karaciğerde eritropoietin üretimini durdurması",
                    "outcome": "Hatalı: Karotis türbülansı böbrek veya karaciğer eritropoietinini etkilemez.",
                    "isCorrect": False
                },
                {
                    "text": "Endotelden aşırı miktarda heparin salınımına yol açarak kanama yapması",
                    "outcome": "Hatalı: Türbülans antikoagülasyon değil protrombotik hasar yaratır.",
                    "isCorrect": False
                }
            ]
        ),
        61: make_branching_logic(
            "Karın ağrısı ve asit gelişen siroz dışı 49 yaşındaki kadın hastada portal ven Doppler ultrasonda portal vende akut lümen tıkayıcı trombüs saptanıyor. Hastada JAK2 V617F mutasyonu pozitif bulunuyor.",
            "Bu hastada altta yatan primer patolojik zemin hangisidir?",
            [
                {
                    "text": "Polisitemia Vera veya Esansiyel Trombositemi gibi Miyeloproliferatif Neoplazm zemininde gelişen hiperviskozite ve trombofili",
                    "outcome": "Doğru karar: JAK2 mutasyonu miyeloproliferatif hastalıkların göstergesidir ve portal ven/Budd-Chiari trombozunun klasik nedenidir.",
                    "isCorrect": True
                },
                {
                    "text": "Viral hepatit B enfeksiyonu",
                    "outcome": "Hatalı: JAK2 V617F viral hepatit belirteci değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Wilson hastalığı",
                    "outcome": "Hatalı: Wilson bakır metabolizması bozukluğudur, JAK2 ile ilişkisizdir.",
                    "isCorrect": False
                }
            ]
        ),
        71: make_branching_logic(
            "Koroner arter bypass greft (KABG) cerrahisi geçiren hastada safen ven greftinde erken dönemde gelişen tromboz araştırılıyor.",
            "Venöz greftin arteriyel yüksek basınçlı ve hızlı akım ortamına maruz kalması sonucunda gelişen temel patolojik adaptasyon/hasar süreci nedir?",
            [
                {
                    "text": "Arteriyelleşme ve intimal hiperplazi zemininde endotel hasarı ve lümende trombosit aktivasyonu",
                    "outcome": "Doğru karar: Ven grefti arteriyel basınca uyum sağlamaya çalışırken intimal kalınlaşma ve endotel hasarına uğrar; erken dönemde tromboz gelişebilir.",
                    "isCorrect": True
                },
                {
                    "text": "Greft veninin kendiliğinden eriyerek ortadan kaybolması",
                    "outcome": "Hatalı: Ven grefti erimez, trombozla tıkanır.",
                    "isCorrect": False
                },
                {
                    "text": "Ven lümeninde kapakçıkların aşırı çoğalarak lümeni kapatması",
                    "outcome": "Hatalı: Kapakçık proliferasyonu görülmez.",
                    "isCorrect": False
                }
            ]
        ),
        81: make_branching_logic(
            "Acil servise nefes darlığı, taşikardi ve tansiyon 75/40 mmHg (kardiyojenik/obstrüktif şok) tablosunda getirilen masif pulmoner embolili hastada ekokardiyografide sağ ventrikül aşırı yüklenmesi saptanıyor.",
            "Bu hemodinamik instabilite tablosunda rehberlere göre en acil hayat kurtarıcı farmakolojik yaklaşım nedir?",
            [
                {
                    "text": "Sistemik intravenöz trombolitik tedavi (rekombinant t-PA / alteplaz infüzyonu)",
                    "outcome": "Doğru karar: Masif ve hipotansif pulmoner embolide sağ ventrikül yetmezliğini ve ölümü önlemek için acil trombolitik tedavi endikedir.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca oral varfarin tableti verilerek taburcu edilmesi",
                    "outcome": "Ölümcül hata: Şoktaki hastada oral varfarin etkisizdir ve mortalite kaçınılmazdır.",
                    "isCorrect": False
                },
                {
                    "text": "Bacaklara elastik bandaj sarılarak 24 saat izlenmesi",
                    "outcome": "Ölümcül ihmal: Obstrüktif şoktaki hastada acil revaskülarizasyon şarttır.",
                    "isCorrect": False
                }
            ]
        ),
        97: make_branching_logic(
            "Sol bacakta şişlik şikayetiyle başvuran düşük klinik olasılıklı (Wells skoru düşük) genç hastada D-Dimer testi normal (negatif) olarak raporlanıyor.",
            "Bu laboratuvar sonucu ışığında hekimin klinik kararı ne olmalıdır?",
            [
                {
                    "text": "D-Dimer testinin çok yüksek negatif prediktif değeri sayesinde DVT tanısı güvenle dışlanabilir ve ileri görüntülemeye gerek yoktur.",
                    "outcome": "Doğru karar: Wells düşük + D-Dimer negatif kombinasyonu DVT'yi %99'un üzerinde güvenilirlikle dışlar.",
                    "isCorrect": True
                },
                {
                    "text": "Testin hiçbir değeri yoktur, derhal invaziv konvansiyonel venografi çekilmelidir.",
                    "outcome": "Hatalı ve gereksiz invaziv yaklaşım: D-Dimer negatifken invaziv işleme gerek yoktur.",
                    "isCorrect": False
                },
                {
                    "text": "Hastaya derhal tam doz heparin infüzyonu başlanmalıdır.",
                    "outcome": "Hatalı: DVT dışlanmışken gereksiz antikoagülasyon kanama riski yaratır.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_recalls():
    """Active recall (aktif hatırlama) ögeleri."""
    return {
        4: make_active_recall(
            "Endotelyal disfonksiyonda l-arjinin aminoasidinden sentezlenen ve güçlü vazodilatatör ile trombosit inhibitörü olan temel gaz molekül hangisidir?",
            "Nitrik Oksittir (NO).",
            "Endotel kökenli gaz yapılı relaksasyon faktörü"
        ),
        8: make_active_recall(
            "Plazminojenin plazmine dönüşümünü fizyolojik olarak engelleyen endotel kökenli majör antifibrinolitik protein hangisidir?",
            "Plazminojen Aktivatör İnhibitörü-1'dir (PAI-1).",
            "Fibrin erimesini durduran endotel kaynaklı serpin"
        ),
        14: make_active_recall(
            "Aort koarktasyonu veya biküspit aort kapağında kanın yüksek hızla püskürmesi ve girdap yapması hangi Virchow bileşenini oluşturur?",
            "Türbülanslı kan akımını (anormal hemodinamik akım) oluşturur.",
            "Laminer akımın bozulduğu mekanik girdap hali"
        ),
        18: make_active_recall(
            "Miyokard enfarktüsü sonrasında nekroze olan ventrikül endokardında trombositlerin çökelmesini başlatan primer hücresel hasar tipi nedir?",
            "Endotel hasarı ve kaybıdır (endotel denudasyonu).",
            "Virchow triyadının 1 numaralı kardiyak başlatıcısı"
        ),
        24: make_active_recall(
            "Venöz kapakçıkların ceplerinde kan akımının duraksaması ve lokal hipoksiye girmesi hangi hemodinamik bozukluğun sonucudur?",
            "Venöz stazın (kan akımının yavaşlaması ve göllenmesi) sonucudur.",
            "Toplardamar içinde kanın durağanlaşması hali"
        ),
        28: make_active_recall(
            "Kronik kalp yetmezliğinde kalbin pompa gücünün düşmesi venöz sistemde hangi Virchow faktörünü şiddetlendirir?",
            "Sistemik venöz stazı şiddetlendirir.",
            "Kalp debisi düşüklüğünün venöz dolaşımdaki hemodinamik sonucu"
        ),
        34: make_active_recall(
            "Faktör V Leiden mutasyonunun kalıtım paterni nedir?",
            "Otozomal dominant kalıtım paterni gösterir.",
            "Mendeliyen tek gen geçiş modeli"
        ),
        38: make_active_recall(
            "Protrombin G20210A gen mutasyonunda tromboz riskini artıran temel patofizyolojik değişiklik nedir?",
            "Protrombin mRNA transkripsiyonunun artması ve plazma protrombin düzeyinin yükselmesidir.",
            "Pıhtılaşma faktörünün plazma konsantrasyonunda artış"
        ),
        44: make_active_recall(
            "Antifosfolipid antikor sendromunda en sık taranan üç temel serolojik antikor hangileridir?",
            "Lupus antikoagülanı, antikardiyolipin antikoru ve anti-beta2-glikoprotein I antikorudur.",
            "APS tanısında bakılan üç klasik laboratuvar belirteci"
        ),
        48: make_active_recall(
            "Heparin Kaynaklı Trombositopeni Tip 2'de (HIT-2) antikorların hedef aldığı antijenik kompleks hangisidir?",
            "Trombosit Faktör 4 (PF4) - Heparin kompleksidir.",
            "Trombositten salınan kemokin ve antikoagülan ilaç kompleksi"
        ),
        54: make_active_recall(
            "Trousseau sendromunun en sık ilişkili olduğu iç organ malignitesi hangisidir?",
            "Pankreas adenokarsinomudur (özellikle gövde ve kuyruk tümörleri).",
            "Müsin salgılayan retroperitoneal organ kanseri"
        ),
        58: make_active_recall(
            "Yaygın İntravasküler Koagülasyon (DIC) seyrinde periferik yaymada görülen parçalanmış eritrositlere ne ad verilir?",
            "Şistozit (kask hücreleri / parçalanmış eritrosit) adı verilir.",
            "Mikroanjiyopatik hemolitik anemiye özgü şekil bozukluğu"
        ),
        64: make_active_recall(
            "Arteriyel trombüslerin en sık görüldüğü vasküler yatak hangisidir?",
            "Koroner arterlerdir (bunu serebral ve femoral arterler izler).",
            "Kalp krizine yol açan miyokardı besleyen damarlar"
        ),
        68: make_active_recall(
            "Venöz trombüslerin en tehlikeli ve fatal olabilen doğrudan komplikasyonu nedir?",
            "Pulmoner Tromboembolizmdir (PE).",
            "Akciğer damar yatağını tıkayan ölümcül pıhtı tablosu"
        ),
        74: make_active_recall(
            "Aort anevrizması içinde oluşan mural trombüslerin doku iskemisi yapmadan önce oluşturabileceği diğer hayati tehlike nedir?",
            "Koparak alt ekstremitelere ve böbreğe embolize olmasıdır.",
            "Geniş damardan çevre dokulara pıhtı saçılması"
        ),
        84: make_active_recall(
            "Eski bir trombüsün t-PA tedavisine direnç kazanmasında fibrin liflerini birbirine kovalent bağlayan transglutaminaz enzimi hangisidir?",
            "Aktif Faktör XIII'tür (Faktör XIIIa).",
            "Fibrin stabilize edici koagülasyon faktörü"
        ),
        88: make_active_recall(
            "DVT sonrası venöz kapak yetmezliği ve staz dermatiti zemininde en sık ülser gelişen anatomik bölge neresidir?",
            "Mediyal malleol çevresidir (ayak bileği iç yüzü).",
            "Venöz staz ülserlerinin klasik yerleşim yeri"
        ),
        92: make_active_recall(
            "Standart heparinin aşırı dozunda gelişen hayatı tehdit edici kanamaların spesifik antidotu nedir?",
            "Protamin sülfattır.",
            "Pozitif yüklü heparin bağlayıcı antidot proteini"
        ),
        94: make_active_recall(
            "Direkt trombin inhibitörü dabigatranın kanamalarında kullanılan monoklonal antikor antidotu hangisidir?",
            "İdarusizumabdır (Praxbind).",
            "Dabigatranı bağlayan spesifik Fab fragmanı"
        )
    }

def get_extra_sliders():
    """Before/after slider (karşılaştırma) ögeleri."""
    return {
        5: make_before_after(
            "Endotelin Prokoagülan ve Antikoagülan Fonksiyonları",
            "Antitrombotik / Sağlıklı Endotel",
            [
                "PGI2 ve NO ile trombosit agregasyonunu durdurma",
                "Trombomodulin ile Protein C'yi aktive etme",
                "Heparin benzeri proteoglikanlarla Antitrombin III'ü çalıştırma"
            ],
            "Protrombotik / Hasarlı Endotel",
            [
                "vWF salgılayarak trombosit adezyonunu başlatma",
                "Doku Faktörü (TF) eksprese ederek ekstrinsik yolu tetikleme",
                "PAI-1 salgılayarak fibrinolizi durdurma"
            ]
        ),
        15: make_before_after(
            "Laminer Akım ile Türbülanslı Akım Farkları",
            "Laminer Fizyolojik Akım",
            [
                "Hücresel elemanlar damar merkezinde hızla akar",
                "Plazma çeperde endoteli koruyan kaygan bir kılıf oluşturur",
                "Trombositler endotel yüzeyine temas etmez"
            ],
            "Türbülanslı Patolojik Akım",
            [
                "Akım çizgileri bozulur ve kaotik girdaplar oluşur",
                "Trombositler endotel duvarına çarparak marjine olur",
                "Lokal endotel erozyonları ve nükleer hasar tetiklenir"
            ]
        ),
        25: make_before_after(
            "Normal Dolaşım ile Venöz Staz Karşılaştırması",
            "Normal Venöz Dolaşım",
            [
                "Baldır kas pompası venöz kanı yerçekimine karşı kalbe iter",
                "Kapakçıklar kanın geriye kaçmasını engeller",
                "Koagülasyon faktörleri karaciğerde hızla temizlenir"
            ],
            "Venöz Staz Tablosu",
            [
                "Hareketsizlik ve kapak yetmezliği kanı göllendirir",
                "Kapak ceplerinde lokal hipoksi ve endotel aktivasyonu gelişir",
                "Konsantre pıhtılaşma faktörleri lümende birikerek pıhtıyı başlatır"
            ]
        ),
        35: make_before_after(
            "Faktör V Normal ile Faktör V Leiden Farkı",
            "Normal Faktör V Proteini",
            [
                "506. pozisyonda Arjinin aminoasidi taşır",
                "Aktif Protein C (APC) tarafından kolayca parçalanır",
                "Pıhtılaşma fizyolojik sürede sonlandırılır"
            ],
            "Faktör V Leiden (Arg506Gln)",
            [
                "506. pozisyonda Glutamin aminoasidi yer alır",
                "APC molekülü enzimatik kesim yapamaz (APC direnci)",
                "FVa kanda uzun süre kalarak trombozu tetikler"
            ]
        ),
        45: make_before_after(
            "Primer APS ile Sekonder APS Karşılaştırması",
            "Primer Antifosfolipid Sendromu",
            [
                "Altta yatan tanımlanmış bir otoimmün hastalık bulunmaz",
                "Yalnızca tromboz ve tekrarlayan gebelik kayıpları ile seyreder",
                "İzole antifosfolipid antikor pozitifliği saptanır"
            ],
            "Sekonder Antifosfolipid Sendromu",
            [
                "Sistemik Lupus Eritematozus (SLE) zemininde gelişir",
                "Kelebek döküntü, nefrit ve artrit tabloya eşlik eder",
                "ANA ve Anti-dsDNA pozitifliği ile birliktedir"
            ]
        ),
        55: make_before_after(
            "Akut Dekompanse DIC ile Kronik Kompanse DIC Farkı",
            "Akut Dekompanse DIC (Sepsis/Travma)",
            [
                "Ani başlangıçlı yaygın mikrovasküler tromboz patlaması",
                "Faktörlerin hızla tükenmesiyle şiddetli kontrolsüz kanama",
                "Trombositopeni, PT/aPTT uzaması ve çok yüksek D-Dimer"
            ],
            "Kronik Kompanse DIC (Kanser/Tümör)",
            [
                "Yavaş ve sinsi ilerleyen subklinik pıhtılaşma aktivasyonu",
                "Karaciğer ve kemik iliği tüketilen faktörleri telafi eder",
                "Kanama nadirdir; derin ven trombozları ve vejetasyonlar ön plandadır"
            ]
        ),
        65: make_before_after(
            "Koroner Tromboz ile Serebral Tromboz Karşılaştırması",
            "Koroner Arter Trombozu",
            [
                "Aterom plağının rüptürü üzerine oturan trombosit pıhtısı",
                "Hedef doku: Miyokard kası",
                "Patolojik nekroz tipi: Koagülasyon nekrozu"
            ],
            "Serebral Arter Trombozu",
            [
                "Karotis veya intrakraniyal arterlerin trombotik oklüzyonu",
                "Hedef doku: Beyin parankimi",
                "Patolojik nekroz tipi: Likefaksiyon (sıvılaşma) nekrozu"
            ]
        ),
        75: make_before_after(
            "Enfektif Endokardit ile Libman-Sacks Endokarditi Farkı",
            "Enfektif Endokardit Vejetasyonu",
            [
                "Bakteriyel veya fungal kolonizasyon mevcuttur",
                "Büyük, düzensiz ve kapak dokusunu parçalayan destrüktif kitle",
                "Genellikle kapağın sadece akım yüzeyinde yerleşir"
            ],
            "Libman-Sacks Vejetasyonu (SLE)",
            [
                "Tamamen steril immün kompleks birikimidir",
                "Küçük, verrüköz ve kapak perforasyonu yapmayan lezyonlar",
                "Kapak yaprakçıklarının hem alt hem üst her iki yüzünde yerleşir"
            ]
        ),
        85: make_before_after(
            "Taze Trombüs ile Organize Trombüs Karşılaştırması",
            "Taze Trombüs (İlk Saatler)",
            [
                "Gevşek fibrin ağı ve taze hücresel elemanlar içerir",
                "t-PA ve endojen plazmin ile hızla eritilebilir",
                "Damar duvarına henüz zayıf tutunmuştur, embolizasyon riski yüksektir"
            ],
            "Organize Trombüs (Günler-Haftalar)",
            [
                "Fibroblastlar, endotel tomurcukları ve kollajen ile doludur",
                "Kovalent FXIIIa bağları nedeniyle trombolitiklere tam dirençlidir",
                "Damar duvarına kaynaşarak rekanalizasyon mikrokanalları barındırır"
            ]
        ),
        93: make_before_after(
            "Varfarin ile Direkt Oral Antikoagülanlar (DOAC) Farkı",
            "Varfarin (K Vitamini Antagonisti)",
            [
                "VKORC1 inhibisyonu ile dolaylı faktör sentez blokajı",
                "Dar terapötik aralık ve zorunlu rutin PT/INR takibi",
                "Çok sayıda besin (yeşil yapraklı sebzeler) ve ilaç etkileşimi"
            ],
            "DOAC'lar (Rivaroksaban, Dabigatran)",
            [
                "Faktör Xa veya Trombini doğrudan ve seçici olarak inhibe etme",
                "Sabit doz kullanımı ve rutin kan pıhtılaşma takibi gerektirmeme",
                "Düşük besin etkileşimi ve anlamlı derecede düşük beyin kanaması riski"
            ]
        )
    }

def get_extra_chains():
    """Causal chain (mekanizma zinciri) ögeleri."""
    return {
        7: make_causal_chain(
            "Endotelyal Antitrombotik Fren Mekanizması",
            [
                "1. Fizyolojik Laminer Akım: Normal akım endotelden PGI2 ve NO salınımını uyarır.",
                "2. Trombosit İnhibisyonu: cAMP ve cGMP artışı ile trombosit adezyonu engellenir.",
                "3. Trombomodulin Etkisi: Endotel yüzeyindeki trombomodulin serbest trombini yakalar.",
                "4. Protein C Aktivasyonu: Oluşan kompleks plazma Protein C'sini aktif APC'ye çevirir.",
                "5. Faktör Yıkımı: APC ve Protein S kofaktörü FVa ve FVIIIa'yı parçalayarak kaskadı durdurur."
            ]
        ),
        16: make_causal_chain(
            "Aterosklerotik Plak Rüptüründen Akut Tromboza Zincir",
            [
                "1. Fibröz Kılıf Zayıflaması: Makrofaj metalloproteinazları aterom kılıfını inceltir.",
                "2. Plak Yırtılması: Yüksek kayma gerilimi altında plak fissüre uğrar.",
                "3. Subendotelyal Temas: Kolajen ve doku faktörü kan dolaşımına açığa çıkar.",
                "4. Trombosit Adezyonu: vWF üzerinden GpIb reseptörleriyle trombositler yapışır.",
                "5. Oklüziv Trombüs: Trombin oluşumu ve GpIIb/IIIa ile lümeni tıkayan beyaz pıhtı tamamlanır."
            ]
        ),
        26: make_causal_chain(
            "Kardiyak Anevrizmada Mural Trombüs Oluşumu",
            [
                "1. Enfarktüs Sonrası Akinezi: Sol ventrikül miyokardı skarlaşarak dışa doğru bombeleşir.",
                "2. Türbülans ve Girdap: Ventriküler kan apeks anevrizması içinde döner ve duraksar.",
                "3. Endokard İskemisi: Gerilen endokard örtüsü endotel bütünlüğünü kaybeder.",
                "4. Trombosit Birikimi: Hasarlı duvara ardışık trombosit ve fibrin katmanları çöker.",
                "5. Mural Kitle: Geniş tabanlı mural trombüs oluşarak sistemik emboli tehdidi yaratır."
            ]
        ),
        36: make_causal_chain(
            "Protrombin G20210A Tromboz Kaskadı",
            [
                "1. Genetik Mutasyon: Protrombin geninin 3'-UTR bölgesinde G20210A değişimi gerçekleşir.",
                "2. mRNA Kararlılığı: Transkripsiyon sonrası mesajcı RNA yıkımı yavaşlar.",
                "3. Yüksek Plazma Düzeyi: Karaciğerde aşırı protrombin (Faktör II) sentezlenir.",
                "4. Trombin Patlaması: Pıhtılaşma uyaranı geldiğinde kontrolsüz miktarda trombin üretilir.",
                "5. Venöz Tromboz: Fibrin yapımı hızlanarak özellikle derin venlerde tromboz gelişir."
            ]
        ),
        46: make_causal_chain(
            "Heparin Kaynaklı Trombositopeni (HIT-2) Zinciri",
            [
                "1. Heparin Uygulaması: Plazmada heparin Trombosit Faktör 4'e (PF4) bağlanır.",
                "2. İmmünofarmakolojik Kompleks: Yabancı algılanan PF4-heparin kompleksine karşı IgG antikorları üretilir.",
                "3. Trombosit FcγRIIa Aktivasyonu: Antikorlar trombosit yüzeyindeki Fc reseptörlerine tutunur.",
                "4. İntravasküler Trombosit Tüketimi: Trombositler kontrolsüz kümelenerek kanda azalır (trombositopeni).",
                "5. Paradoksal Masif Tromboz: Salınan prokoagülan mikropartiküller yaygın arteriyel ve venöz tromboz yapar."
            ]
        ),
        56: make_causal_chain(
            "Malignite Zemininde Trousseau Sendromu Mekanizması",
            [
                "1. Tümör İlerlemesi: Pankreas veya mide adenokarsinomu kanda yayılır.",
                "2. Doku Faktörü ve Müsin Salınımı: Kanser hücreleri dolaşıma bol miktarda prokoagülan salgılar.",
                "3. Doğrudan Faktör X Aktivasyonu: Müsin kofaktörsüz şekilde Faktör X'i aktif FXa'ya dönüştürür.",
                "4. Gezici Tromboz: Vücudun farklı venöz yataklarında peş peşe tromboflebit atakları başlar.",
                "5. Trousseau Bulgusu: Bir kolda gerileyen tromboz diğer bacakta yeniden ortaya çıkar."
            ]
        ),
        66: make_causal_chain(
            "İskemik İnmede Sıvılaşma Nekrozu Zinciri",
            [
                "1. Karotis/Serebral Tromboz: Orta serebral arterde ani trombotik tıkanma gerçekleşir.",
                "2. Nöronal Anoksi: Dakikalar içinde ATP tükenir ve membran pompaları çöker.",
                "3. Kalsiyum İnvazyonu: Hücre içine giren kalsiyum lizozomal enzimleri ve proteazları aktive eder.",
                "4. Otolitik Sindirim: Beyin dokusu lipid ve sudan zengin olduğundan hidrolitik enzimlerle erir.",
                "5. Likefaksiyon Nekrozu: İskemik parankim sıvı dolu kistik bir kaviteye dönüşür."
            ]
        ),
        76: make_causal_chain(
            "Organize Trombüste Rekanalizasyon Zinciri",
            [
                "1. Trombüs Tutunması: Hasarlı intimaya bağlanan taze pıhtı damar lümenini doldurur.",
                "2. Endotel Tomurcuklanması: Duvar endotel hücreleri pıhtı kütlesinin içine urgan gibi ürer.",
                "3. Tüp Oluşumu: Prolifere olan endotel kordonları içinde tübüler mikrolümenler belirir.",
                "4. Anastomoz ve Kanal Açılımı: Küçük kanalcıklar birbirine bağlanarak pıhtı boyunca uzanır.",
                "5. Parsiyel Perfüzyon: Yeni kapiller kanallar üzerinden sınırlı kan akımı yeniden başlar."
            ]
        )
    }

def get_extra_tables():
    """Interactive table (gizli tablo) ögeleri."""
    return {
        11: make_table(
            ["Endotelyal Faktör", "Etki Mekanizması", "Fizyolojik Görevi"],
            [
                ["Prostasiklin (PGI2)", "cAMP artışı ile agregasyon blokajı", "Vazodilatasyon ve trombosit durdurma"],
                [
                    "Doku Faktörü Yolu İnhibitörü (TFPI)",
                    {"text": "TF-FVIIa kompleksini inaktive etme", "isMasked": True, "hint": "Ekstrinsik yolak başlama freni"},
                    "Pıhtılaşmanın kontrolsüz yayılmasını önleme"
                ],
                ["Trombomodulin", "Trombini bağlayıp Protein C'ye sunma", "Antikoagülan dönüşüm"]
            ]
        ),
        21: make_table(
            ["Hemodinamik Akım Tipi", "Vasküler Yatak", "Hücresel Etkisi"],
            [
                ["Fizyolojik Laminer Akım", "Düzgün elastik arter ve venler", "Endoteli koruyan koruyucu kayma stresi"],
                [
                    "Türbülanslı Akım",
                    {"text": "Aterom plakları ve bifurkasyonlar", "isMasked": True, "hint": "Damar dallanmalarındaki kaotik girdap"},
                    "Endotel erozyonu ve trombosit marjinasyonu"
                ],
                ["Venöz Staz", "Alt ekstremite venöz kapak cepleri", "Lokal hipoksi ve pıhtılaşma faktör birikimi"]
            ]
        ),
        31: make_table(
            ["Trombofili Nedeni", "Kalıtım ve Prevalans", "Göreceli Tromboz Riski"],
            [
                ["Faktör V Leiden", "Otozomal dominant / %5 beyaz ırk", "Heterozigotta 5-7 kat, homozigotta 50-80 kat"],
                [
                    "Protrombin G20210A",
                    {"text": "Otozomal dominant / %1-2 sıklık", "isMasked": True, "hint": "En sık 2. herediter trombofili"},
                    "Heterozigot bireylerde 2-3 kat venöz tromboz artışı"
                ],
                ["Antitrombin III Eksikliği", "Nadir (%0.02) ancak şiddetli", "Hayat boyu %70-80 oranında masif tromboz"]
            ]
        ),
        41: make_table(
            ["Kazanılmış Trombofili", "Tetikleyici Klinik Durum", "Karakteristik Komplikasyon"],
            [
                ["Antifosfolipid Sendromu", "Otoantikorlar (lupus antikoagülanı)", "Tekrarlayan düşükler ve arter/ven trombozu"],
                [
                    "Heparin Trombositopenisi (HIT)",
                    {"text": "PF4-heparin kompleksine antikor", "isMasked": True, "hint": "Trombosit sayısını düşürüp tromboz yapan durum"},
                    "Trombositopeni eşliğinde paradoksal tromboz"
                ],
                ["Kanser Hiperkoagülabilite", "Müsin ve tümör doku faktörü salınımı", "Trousseau gezici tromboflebiti"]
            ]
        ),
        51: make_table(
            ["Klinik Durum", "Primer Trombüs Tipi", "Hayati Tehlike Mekanizması"],
            [
                ["Akut Koroner Sendrom", "Arteriyel beyaz trombüs", "Transmural ventrikül miyokard enfarktüsü"],
                [
                    "Alt Ekstremite DVT",
                    {"text": "Venöz kırmızı trombüs", "isMasked": True, "hint": "Staz zemininde gelişen eritrosit zengin pıhtı"},
                    "Koparak masif semer pulmoner emboli oluşturma"
                ],
                ["Sol Ventrikül Apeks Anevrizması", "Kardiyak mural trombüs", "Serebral artere embolize olup inme yapma"]
            ]
        )
    }

def get_extra_quizzes():
    """Micro quiz (mini soru) ögeleri."""
    return {
        12: make_micro_quiz(
            "Endotel hasarı sonrasında subendotelyal matrikse bağlanan trombositlerin granül salınımı yapmasında kilit rol oynayan güçlü vazokonstriktör medyatör hangisidir?",
            {
                "A": "Tromboksan A2 (TxA2)",
                "B": "Prostasiklin (PGI2)",
                "C": "Nitrik Oksit (NO)",
                "D": "Bradikinin",
                "E": "Doku plazminojen aktivatörü (t-PA)"
            },
            "A",
            {
                "A": "A seçeneği doğrudur: TxA2 aktif trombositlerden salınarak vazokonstriksiyon yapar ve diğer trombositleri toplayarak agregasyonu artırır.",
                "B": "B seçeneği antikoagülandır, endotelden salınır.",
                "C": "C seçeneği vazodilatatördür.",
                "D": "D seçeneği inflamatuar ağrı ve vazodilatasyon yapar.",
                "E": "E seçeneği fibrinolitiktir."
            }
        ),
        22: make_micro_quiz(
            "Virchow triyadında tanımlanan 'anormal kan akımı' kapsamında aşağıdakilerden hangisi doğrudan staz (durgunluk) örneğidir?",
            {
                "A": "Aort kapak darlığında kapak orifisinden kanın fışkırması",
                "B": "Aterom plağının çatallanma noktasında oluşturduğu kaotik girdap",
                "C": "Uzun süre yatağa bağımlı hastanın bacak venlerinde kan göllenmesi",
                "D": "Hipertansif krizde arteriyel duvar kayma stresinin aşırı artması",
                "E": "Arteriyovenöz fistülde yüksek debili kan geçişi"
            },
            "C",
            {
                "A": "A seçeneği türbülans örneğidir.",
                "B": "B seçeneği türbülans örneğidir.",
                "C": "C seçeneği doğrudur: Yatağa bağımlılıkta kas pompası durur ve alt ekstremite venöz dolaşımında staz gelişir.",
                "D": "D seçeneği kayma stresidir, staz değildir.",
                "E": "E seçeneği yüksek akımlı şanttır."
            }
        ),
        32: make_micro_quiz(
            "Genç bir kadında tekrarlayan derin ven trombozları saptanmış ve plazma Protein C düzeyinin normalin %25'i olduğu ölçülmüştür. Bu hastada tromboz eğiliminin nedeni hangisidir?",
            {
                "A": "Faktör Va ve Faktör VIIIa'nın inaktive edilememesi",
                "B": "Trombinin doğrudan parçalanamaması",
                "C": "Fibrinojenin plazmine dönüşememesi",
                "D": "Antitrombin III sentezinin durması",
                "E": "Von Willebrand faktörün yokluğu"
            },
            "A",
            {
                "A": "A seçeneği doğrudur: Aktif Protein C normalde FVa ve FVIIIa'yı yıkar; Protein C eksikliğinde bu iki kritik kofaktör yıkılamaz ve kaskad frenlenemez.",
                "B": "B seçeneği yanlış; trombin ATIII tarafından inhibe edilir.",
                "C": "C seçeneği yanlış; fibrinojen plazmine dönüşmez, plazmin fibrini yıkar.",
                "D": "D seçeneği ATIII eksikliğiyle Protein C farklı sistemlerdir.",
                "E": "E seçeneği kanama yapar."
            }
        ),
        42: make_micro_quiz(
            "Heparin tedavisi alan bir hastada heparin kaynaklı trombositopeni (HIT) şüphesi doğduğunda neden doğrudan varfarin başlanması kontrendikedir?",
            {
                "A": "Varfarinin heparinin etkisini tamamen nötralize etmesi",
                "B": "Varfarinin erken Protein C düşüşüyle mikrovasküler deri nekrozu ve trombozu alevlendirme riski",
                "C": "Varfarinin trombosit sayısını bir milyonun üzerine çıkarması",
                "D": "Varfarinin böbreklerden hızla atılarak etkisiz kalması",
                "E": "Varfarinin aPTT süresini kontrolsüz şekilde 10 kat uzatması"
            },
            "B",
            {
                "A": "A seçeneği yanlıştır; mekanizmaları farklıdır.",
                "B": "B seçeneği doğrudur: HIT zemininde varfarin başlanırsa yarı ömrü kısa Protein C hızla tükenir ve masif venöz ekstremite gangreni/deri nekrozu gelişir.",
                "C": "C seçeneği yanlıştır; varfarin trombosit sayısını artırmaz.",
                "D": "D seçeneği yanlıştır; karaciğerde metabolize edilir.",
                "E": "E seçeneği yanlıştır; varfarin esasen PT/INR'yi etkiler."
            }
        )
    }

def get_extra_cloze():
    """Cloze masking (boşluk doldurma) ögeleri."""
    return {
        2: make_cloze(
            "Sağlıklı endotel hücreleri trombosit agregasyonunu engellemek amacıyla sürekli olarak prostasiklin ve nitrik oksit sentezler.",
            "prostasiklin",
            "Trombosit siklooksijenaz ürününün tam zıttı olan endotelyal vazodilatatör prostaglandin"
        ),
        29: make_cloze(
            "Uzun süreli yatak istirahatinde baldır kas pompasının devre dışı kalması alt ekstremite venlerinde staz oluşturarak tromboza zemin hazırlar.",
            "staz",
            "Kan akımının yavaşlaması ve göllenmesi hali"
        ),
        39: make_cloze(
            "Protrombin G20210A mutasyonu protrombin mRNA transkripsiyonunu artırarak kanda Faktör II seviyesini yükseltir.",
            "Faktör II",
            "Protrombinin koagülasyon kaskadındaki Romen rakamlı faktör numarası"
        ),
        49: make_cloze(
            "Heparin Kaynaklı Trombositopeni Tip 2 tablosunda IgG antikorları Trombosit Faktör 4 ile heparinin oluşturduğu kompleksi hedefler.",
            "Trombosit Faktör 4",
            "Alfa granüllerinden salınan heparin bağlayıcı kemokin molekülü"
        )
    }

def apply_enrichment(slides):
    """Slayt listesine tüm ek interaktif ögeleri entegre eder."""
    extra_branching = get_extra_branching()
    extra_recalls = get_extra_recalls()
    extra_sliders = get_extra_sliders()
    extra_chains = get_extra_chains()
    extra_tables = get_extra_tables()
    extra_quizzes = get_extra_quizzes()
    extra_cloze = get_extra_cloze()

    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        if "elements" in slide:
            elements = slide["elements"]
        else:
            elements = slide.setdefault("interactiveElements", [])

        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_recalls:
            elements.append(extra_recalls[slide_num])
        if slide_num in extra_sliders:
            elements.append(extra_sliders[slide_num])
        if slide_num in extra_chains:
            elements.append(extra_chains[slide_num])
        if slide_num in extra_tables:
            elements.append(extra_tables[slide_num])
        if slide_num in extra_quizzes:
            elements.append(extra_quizzes[slide_num])
        if slide_num in extra_cloze:
            elements.append(extra_cloze[slide_num])

    return slides
