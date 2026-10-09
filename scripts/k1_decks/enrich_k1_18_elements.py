# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 (hedef %10-20) oranına ulaşmasını sağlar.
"""

from scripts.k1_18_deck_data.helpers import (
    make_branching_logic, make_active_recall
)

def get_extra_branching():
    """Branching logic (tarihsel, epidemiyolojik ve halk sağlığı karar verme) ögeleri."""
    return {
        2: make_branching_logic(
            "Bir kentin belediye ve sağlık meclisi 1920 yılında halk sağlığı bütçesini planlamak üzere toplanıyor. Bazı üyeler yalnızca hastanedeki ameliyathanelere yatırım yapmayı öneriyor.",
            "C.E.A. Winslow'un halk sağlığı tanımı ve felsefesi dikkate alındığında meclis hekiminin sunması gereken en doğru stratejik karar nedir?",
            [
                {
                    "text": "Tüm bütçe özel kliniklere aktarılmalı, koruyucu çevre koşulları vatandaşın kendi sorununa bırakılmalıdır.",
                    "outcome": "Winslow tanımına tamamen zıt: Winslow organize toplum çabasıyla çevre sağlığının düzeltilmesini şart koşar.",
                    "isCorrect": False
                },
                {
                    "text": "Bütçe organize toplum çalışmalarıyla çevre sağlık koşullarını düzeltmeye, bulaşıcı hastalıkları önlemeye ve bireylere sağlık eğitimi vererek yaşamı uzatmaya tahsis edilmelidir.",
                    "outcome": "Kusursuz halk sağlığı kararı: Winslow'un 1920 tanımındaki üç temel hedef ve bilim/sanat niteliği tam olarak hayata geçirilir.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca salgın çıktığı günlerde ilaç satın alınmalı, salgın yokken hiçbir harcama yapılmamalıdır.",
                    "outcome": "Salgınlara hazırlıksız yakalanarak binlerce can kaybına yol açacak ihmal.",
                    "isCorrect": False
                }
            ]
        ),
        4: make_branching_logic(
            "Antik çağda bir köyde aniden yüksek ateş, titreme ve dalak büyümesiyle seyreden bir salgın patlak veriyor. Köy büyücüsü bunun 'ırmak tanrısının laneti' olduğunu söyleyerek kurban kesilmesini istiyor.",
            "Hipokratik rasyonel tıp okulundan yetişmiş bir antik hekimin bu duruma yaklaşımı ne olmalıdır?",
            [
                {
                    "text": "Büyücüyü desteklemeli ve tapınakta en büyük hayvanların kurban edilmesini emretmelidir.",
                    "outcome": "Rasyonel tıbbın reddi ve doğaüstü inançlara teslimiyet.",
                    "isCorrect": False
                },
                {
                    "text": "Hastalıkların tanrıların gazabı değil, bataklık havası, kirli sular ve çevresel dengesizlik gibi tamamen doğal nedenlerden kaynaklandığını belirterek bataklıktan uzaklaşmayı ve temiz su tüketmeyi önermelidir.",
                    "outcome": "Kusursuz Hipokratik yaklaşım: Doğaüstü inançlar yıkılır, hastalığın rasyonel ve çevresel nedenleri hedeflenir.",
                    "isCorrect": True
                },
                {
                    "text": "Köyü tamamen ateşe verip tüm halkı kılıçtan geçirmelidir.",
                    "outcome": "'Primum non nocere' ilkesine tamamen aykırı bir cinayet.",
                    "isCorrect": False
                }
            ]
        ),
        6: make_branching_logic(
            "Hipokrat'ın humoral patoloji kuramına göre muayene edilen bir hastada aşırı hüzün, içine kapanıklık, iştahsızlık ve zayıflama saptanıyor.",
            "Humoral teoriye göre bu hastada hangi vücut sıvısının aşırı arttığı (diskrazi) düşünülmeli ve tedavi dengesi nasıl kurulmalıdır?",
            [
                {
                    "text": "Kan (sanguis) aşırı artmıştır; hasta sangvinik mizaçtadır.",
                    "outcome": "Hatalı sıvı: Sangvinik mizaç neşeli ve hareketlidir, hüzünlü değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Dalak kaynaklı soğuk ve kuru nitelikteki kara safra (melanchole) aşırı birikmiştir; hastanın diyeti ve ortamı sıcak ve nemli unsurlarla dengelenmelidir.",
                    "outcome": "Kusursuz humoral patoloji analizi: Melankolinin kaynağı olan kara safra diskrazisi doğru yorumlanır.",
                    "isCorrect": True
                },
                {
                    "text": "Beyinden kaynaklanan balgam taşmıştır ve hasta flegmatiktir.",
                    "outcome": "Flegmatik mizaç uyuşuk ve duygusuzdur.",
                    "isCorrect": False
                }
            ]
        ),
        8: make_branching_logic(
            "Roma İmparatorluğu döneminde Bergamalı Galenos'a göğüs ağrısı ve nefes darlığı çeken bir gladyatör getiriliyor.",
            "Eczacılığın babası kabul edilen Galenos'un hastaya farmakolojik yaklaşımı nasıl şekillenmelidir?",
            [
                {
                    "text": "Hastaya yalnızca dua etmesini söyleyip hiçbir ilaç vermemelidir.",
                    "outcome": "Galenik farmakolojiyi yok sayan yaklaşım.",
                    "isCorrect": False
                },
                {
                    "text": "Şifalı bitki köklerini, mineralleri ve hayvansal özütleri belirli oranlarda karıştırarak elde ettiği galenik preparatlarla hastanın semptomlarını hafifletmelidir.",
                    "outcome": "Kusursuz antik farmakoloji uygulaması: Galenik ilaç hazırlama sanatının temel prensipleri uygulanır.",
                    "isCorrect": True
                },
                {
                    "text": "Gladyatörü derhal aslanların önüne atmalıdır.",
                    "outcome": "Tıbbi etik dışı vahşet.",
                    "isCorrect": False
                }
            ]
        ),
        12: make_branching_logic(
            "Abbasi Halifesi Bağdat'ta büyük bir bimaristan (hastane) inşa ettirmek istiyor ve yer seçimini hekim Ebubekir Razi'ye emanet ediyor.",
            "Razi'nin hastaların en hızlı iyileşeceği ve havanın en temiz olduğu noktayı bilimsel olarak belirleme kararı ne olmalıdır?",
            [
                {
                    "text": "Sarayın hemen yanındaki gürültülü çarşı meydanını seçmelidir.",
                    "outcome": "Gürültü ve pis koku hastaların iyileşmesini engeller.",
                    "isCorrect": False
                },
                {
                    "text": "Kentin dört bir tarafındaki direklere taze et parçaları astırmalı; etin en geç bozulduğu ve kokuşmanın en az olduğu yeri havanın en temiz bölgesi olarak seçmelidir.",
                    "outcome": "Kusursuz tarihi halk sağlığı deneyi: Razi'nin kokuşma kuramına dayalı meşhur hastane yeri seçimi uygulanır.",
                    "isCorrect": True
                },
                {
                    "text": "En bataklık ve sazlık alanı seçerek hastaneyi oraya kurmalıdır.",
                    "outcome": "Bataklık sıtma odağıdır, hastalar sıtmadan ölür.",
                    "isCorrect": False
                }
            ]
        ),
        14: make_branching_logic(
            "Orta Çağ'da Endülüs'te bir kasabada veba salgını baş gösteriyor. İbn-ül Habib hastaları tedavi ederken bulaş dinamiklerini inceliyor.",
            "İbn-ül Habib'in salgının yayılmasını durdurmak için yerel yöneticilere tavsiye edeceği en kritik halk sağlığı tedbiri nedir?",
            [
                {
                    "text": "Ölenlerin giysilerinin ve yatak çarşaflarının fakirlere dağıtılmasını emretmelidir.",
                    "outcome": "Ölümcül hata: Giysi ve kap-kacak teması (fomitler) vebayı tüm kente yayar.",
                    "isCorrect": False
                },
                {
                    "text": "Vebalı hastalarla temasın derhal kesilmesi, hastaların kullandığı giysi, yatak ve kap-kacakların imha edilmesi veya dezenfekte edilmesi gerektiğini bildirmelidir.",
                    "outcome": "Kusursuz enfeksiyon kontrol kararı: Fomit ve temas yoluyla bulaşın önlenmesi salgın zincirini kırar.",
                    "isCorrect": True
                },
                {
                    "text": "Hastalara yalnızca kokulu parfümler sıkılarak sokaklarda dolaşmalarına izin verilmelidir.",
                    "outcome": "Miazma yanılgısına teslim olup teması serbest bırakan tehlikeli yaklaşım.",
                    "isCorrect": False
                }
            ]
        ),
        16: make_branching_logic(
            "1403 yılında veba salgınının yaşandığı Levant bölgesinden Venedik limanına yanaşan bir ticaret gemisi görülüyor.",
            "Venedik Senatosu ve liman sağlık meclisinin kenti Kara Ölüm'den korumak için alması gereken resmi karar nedir?",
            [
                {
                    "text": "Tüm yolcuların ve malların hemen şehre girmesine izin verilmelidir.",
                    "outcome": "Tüm kentin vebadan kırılmasına yol açacak felaket.",
                    "isCorrect": False
                },
                {
                    "text": "Geminin karaya yanaşması yasaklanmalı; yolcular ve yükler açıkta tam 40 gün (quaranta giorni) boyunca tecrit edilmeli ve şüpheliler Lazaretto adasında gözetim altında tutulmalıdır.",
                    "outcome": "Kusursuz karantina kararı: Venedik'in tarihi 'quaranta giorni' kuralı ve lazaretto tecridi ile salgın önlenir.",
                    "isCorrect": True
                },
                {
                    "text": "Gemi içindeki herkesle birlikte yakılarak batırılmalıdır.",
                    "outcome": "İnsanlık dışı ve gereksiz aşırı şiddet.",
                    "isCorrect": False
                }
            ]
        ),
        22: make_branching_logic(
            "1675 yılında Delft'te Leeuwenhoek, kuyu suyundan aldığı bir damlayı kendi yaptığı tek mercekli mikroskobun odaklama iğnesine yerleştiriyor ve minik canlıların yüzdüğünü görüyor.",
            "Leeuwenhoek'un bu keşfi bilim dünyasına raporlarken yapması gereken doğru bilimsel çıkarım nedir?",
            [
                {
                    "text": "Gördüğü şeylerin sadece optik bir yanılsama veya göz kusuru olduğunu söyleyip merceğini kırmalıdır.",
                    "outcome": "Bilimsel keşfi inkar eden tutum.",
                    "isCorrect": False
                },
                {
                    "text": "Suda çıplak gözle görülemeyen bağımsız hareket eden canlı mikroorganizmalar ('animalcules') bulunduğunu titiz çizimlerle Londra Royal Society'ye bildirmelidir.",
                    "outcome": "Kusursuz mikrobiyolojik keşif: Mikroorganizmaların varlığı tarihte ilk kez tescillenir.",
                    "isCorrect": True
                },
                {
                    "text": "Bu küçük hayvancıkların doğrudan büyü yoluyla yok edilebileceğini iddia etmelidir.",
                    "outcome": "Orta Çağ hurafesine dönüş.",
                    "isCorrect": False
                }
            ]
        ),
        24: make_branching_logic(
            "Paris Bilimler Akademisi'nde abiyogenez (kendiliğinden oluş) savunucuları, mikropların et suyunda kendiliğinden türediğini iddia ediyor.",
            "Louis Pasteur'ün bu iddiayı kesin olarak çürütmek için kuğu boyunlu balon deneyinde sergilemesi gereken kanıt adımı nedir?",
            [
                {
                    "text": "Balonun ağzını tamamen mühürleyip 'havayı yok ettim' demelidir.",
                    "outcome": "Abiyogenezciler 'yaşam gücü olan havayı yok ettin' diyerek itiraz eder.",
                    "isCorrect": False
                },
                {
                    "text": "Balonun boynunu 'S' şeklinde kıvırarak havanın serbestçe girmesini sağlamalı; ancak toz ve mikropların kıvrımda çöktüğünü, sıvı steril kalırken boyun kırılınca mikropların ürediğini göstermelidir.",
                    "outcome": "Kusursuz deneysel darbe: Havanın yaşam gücü engellenmeden mikropların havadan geldiği ispatlanır ve abiyogenez çöker.",
                    "isCorrect": True
                },
                {
                    "text": "Tartışmadan çekilip kimya laboratuvarını kapatmalıdır.",
                    "outcome": "Bilimsel ilerlemeyi durduracak teslimiyet.",
                    "isCorrect": False
                }
            ]
        ),
        25: make_branching_logic(
            "19. yüzyıl sonunda bir kentte çocuklarda yaygın kemik ve barsak tüberkülozu (Mycobacterium bovis) ve dalgalı ateş (brusella) vakaları patlak veriyor. Vakaların tümünün çiğ süt içtiği saptanıyor.",
            "Halk sağlığı idaresinin bu salgınları durdurmak için zorunlu kılması gereken en etkili teknolojik yöntem nedir?",
            [
                {
                    "text": "Süt tüketimini tamamen yasaklayıp çocuklara sadece su içirmek.",
                    "outcome": "Ağır malnütrisyon ve raşitizme yol açar.",
                    "isCorrect": False
                },
                {
                    "text": "Sütlerin pastörizasyon işleminden geçirilerek belirli ısıda patojen bakterilerden arındırılmasını yasal zorunluluk haline getirmek.",
                    "outcome": "Kusursuz halk sağlığı müdahalesi: Çiğ süt kaynaklı tüberküloz ve bruselloz salgınları tamamen durdurulur.",
                    "isCorrect": True
                },
                {
                    "text": "Sütün içine cıva damlatılmasını önermek.",
                    "outcome": "Kitlesel cıva zehirlenmesine yol açacak ölümcül hata.",
                    "isCorrect": False
                }
            ]
        ),
        27: make_branching_logic(
            "Bir tıp araştırmacısı yeni bir salgın hastalığın etkenini bulduğunu iddia ediyor ancak bakteriyi yalnızca bir hastanın kanında gördüğünü, saf kültür yapamadığını ve deney hayvanında deneyemediğini belirtiyor.",
            "Robert Koch'un postülatları çerçevesinde bilim kurulunun bu iddiaya karşı vermesi gereken hakemlik kararı nedir?",
            [
                {
                    "text": "İddia hemen kabul edilmeli ve aşı üretimine başlanmalıdır.",
                    "outcome": "Kanıtsız ve aceleci karar büyük halk sağlığı fiyaskolarına yol açar.",
                    "isCorrect": False
                },
                {
                    "text": "İddia yetersizdir; bakteri hastadan saf kültür halinde üretilmeli, sağlıklı deney hayvanına verilip aynı hastalık oluşturulmalı ve hayvandan tekrar izole edilmelidir (Koch Postülatları).",
                    "outcome": "Kusursuz bilimsel metodoloji: Nedensellik ancak 4 Koch postülatının eksiksiz tamamlanmasıyla kanıtlanır.",
                    "isCorrect": True
                },
                {
                    "text": "Araştırmacı tıp mesleğinden tamamen ihraç edilmelidir.",
                    "outcome": "Aşırı ve orantısız ceza.",
                    "isCorrect": False
                }
            ]
        ),
        32: make_branching_logic(
            "18. yüzyıl başında İstanbul'da çiçek salgını yaklaşırken bir anne, çocuğunun ölümcül çiçekten korunmasını istiyor.",
            "Osmanlı 'aşıcı kadınlarının' variolasyon geleneğine göre uygulanması gereken geleneksel koruyucu karar nedir?",
            [
                {
                    "text": "Çocuğu ağır çiçekten ölmek üzere olan bir hastanın yanına kapatmak.",
                    "outcome": "Çocuğun ağır çiçek kapıp ölmesine yol açacak vahim hata.",
                    "isCorrect": False
                },
                {
                    "text": "Hastalığı hafif atlatan bir çocuğun olgun püstül cerahatini alıp sağlıklı çocuğun kol derisine çizik atarak kontrollü biçimde aşılamak (variolasyon).",
                    "outcome": "Kusursuz variolasyon uygulaması: Çocuk hastalığı hafifçe geçirerek ömür boyu kalıcı bağışıklık kazanır.",
                    "isCorrect": True
                },
                {
                    "text": "Çocuğa büyü yapılmış tılsımlı su içirmek.",
                    "outcome": "Hiçbir koruyuculuğu olmayan hurafe.",
                    "isCorrect": False
                }
            ]
        ),
        34: make_branching_logic(
            "Edward Jenner, süt sağan kadınların ellerindeki sığır çiçeği (cowpox) nedeniyle ölümcül insan çiçeğinden korunduğunu gözlemliyor.",
            "Jenner'ın bu koruyuculuğu tıp dünyasına ispatlamak için 1796'da tasarladığı tarihi aşı deneyi kararı nedir?",
            [
                {
                    "text": "İnekleri doğrudan ameliyatla insanlara nakletmek.",
                    "outcome": "Biyolojik olarak anlamsız ve imkansız.",
                    "isCorrect": False
                },
                {
                    "text": "Sütçü kız Sarah Nelmes'in sığır çiçeği kabarcığından aldığı sıvıyı James Phipps'in koluna aşılamak ve sonrasında çocuğun insan çiçeğine karşı bağışık olduğunu kanıtlamak.",
                    "outcome": "Kusursuz aşılama devrimi: Sığır çiçeği ile insan çiçeği arasında çapraz bağışıklık kanıtlanır ve 'vaccination' doğar.",
                    "isCorrect": True
                },
                {
                    "text": "Tüm inekleri itlaf etmek.",
                    "outcome": "Aşı kaynağını yok edecek yanlış karar.",
                    "isCorrect": False
                }
            ]
        ),
        35: make_branching_logic(
            "Temmuz 1885'te kuduz bir köpek tarafından 14 yerinden ağır şekilde ısırılan 9 yaşındaki Joseph Meister, annesi tarafından Pasteur'ün laboratuvarına getiriliyor. Kuduzun o güne kadar bilinen hiçbir tedavisi yok ve ölüm kesindir.",
            "Louis Pasteur'ün bu ölümcül vakada alması gereken hayat kurtarıcı karar nedir?",
            [
                {
                    "text": "Çocuğu eve gönderip ölümünü beklemek.",
                    "outcome": "Çocuğun birkaç hafta içinde kuduz ensefalitinden acı içinde ölmesine izin vermek.",
                    "isCorrect": False
                },
                {
                    "text": "Tavşan omuriliğinde zayıflattığı deneysel kuduz aşısını çocuğa artan dozlarda uygulayarak kuluçka süresi bitmeden bağışıklık oluşturmak.",
                    "outcome": "Kusursuz tıp zaferi: Joseph Meister kuduza yakalanmadan tamamen kurtulur ve ilk insan kuduz aşısı tarihe geçer.",
                    "isCorrect": True
                },
                {
                    "text": "Çocuğun ısırılan tüm uzuvlarını kesmek.",
                    "outcome": "Sakat bırakacak ve virüsün sinirsel göçünü durduramayacak gereksiz cerrahi.",
                    "isCorrect": False
                }
            ]
        ),
        36: make_branching_logic(
            "1890 yılında Berlin'de bir hastanede difteri sahte zarları (psödomembran) nedeniyle nefes alamayan ve ölmek üzere olan çocuklar bulunuyor.",
            "Emil von Behring'in at kanından elde ettiği antitoksin ile uygulaması gereken acil hayat kurtarıcı karar nedir?",
            [
                {
                    "text": "Çocuklara difteri basili aşısı yaparak antikor üretmelerini 1 ay beklemek.",
                    "outcome": "Çocuklar birkaç saat içinde nefessiz kalarak ölür; aktif aşı acil tabloda geç kalır.",
                    "isCorrect": False
                },
                {
                    "text": "Bağışık atlardan elde edilen hazır difteri antitoksin serumunu enjekte ederek toksinleri anında nötralize etmek (pasif bağışıklama).",
                    "outcome": "Kusursuz acil serum terapisi: Hazır antikorlar sahte zarları eritir, çocukların hayatı kurtulur ve ilk Nobel Tıp Ödülü kazanılır.",
                    "isCorrect": True
                },
                {
                    "text": "Çocukların boğazına buz basarak beklemek.",
                    "outcome": "Toksik boğulmayı engelleyemez.",
                    "isCorrect": False
                }
            ]
        ),
        44: make_branching_logic(
            "Ağustos 1854'te Londra Broad Street'te her gün onlarca insan koleradan ölüyor. Yerel meclis salgının bataklık kokusundan (miazma) çıktığına inanıyor.",
            "Nokta haritasıyla ölümlerin Broad Street su tulumbası çevresinde kümelendiğini kanıtlayan John Snow'un meclise aldırması gereken acil müdahale kararı nedir?",
            [
                {
                    "text": "Sokaklarda tütsü yakıp herkesin pencerelerini kapatmasını istemek.",
                    "outcome": "Miazma yanılgısına teslim olup su kaynaklı ölümlerin sürmesine yol açar.",
                    "isCorrect": False
                },
                {
                    "text": "Broad Street üzerindeki sokak su pompasının kolunu söktürerek halkın o kuyudan su içmesini derhal durdurmak.",
                    "outcome": "Kusursuz saha epidemiyolojisi müdahalesi: Tulumba kolu sökülür, su alımı durur ve kolera salgını anında bıçak gibi kesilir.",
                    "isCorrect": True
                },
                {
                    "text": "Tüm kentin su borularını dinamitle patlatmak.",
                    "outcome": "Tüm kenti susuz bırakacak orantısız yıkım.",
                    "isCorrect": False
                }
            ]
        ),
        46: make_branching_logic(
            "1842 yılında İngiltere'de Edwin Chadwick işçi sınıfı mahallelerinde ortalama yaşam süresinin pis su, açık lağımlar ve çöp dağları yüzünden 20 yaşın altında olduğunu belgeliyor.",
            "Chadwick'in hükümete sunduğu tarihi raporda önerdiği kamusal altyapı reform kararı ne olmalıdır?",
            [
                {
                    "text": "İşçilerin daha çok çalıştırılarak erken ölümlerine göz yumulması.",
                    "outcome": "İnsanlık dışı ve salgınları daha da azdıracak ihmal.",
                    "isCorrect": False
                },
                {
                    "text": "Kapalı kanalizasyon boruları döşenmesi, temiz basınçlı şehir şebeke suyu kurulması, çöplerin toplanması ve merkezi Halk Sağlığı Yasası çıkarılması.",
                    "outcome": "Kusursuz sanitasyon devrimi: 1848 Halk Sağlığı Yasası çıkar ve kentsel ölüm oranları hızla düşer.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca zengin mahallelerin sokaklarının yıkanması.",
                    "outcome": "Sosyal adaletsizliği artırır, salgını durduramaz.",
                    "isCorrect": False
                }
            ]
        ),
        48: make_branching_logic(
            "1897'de Ronald Ross sıtma parazitinin Anofel cinsi dişi sivrisineklerle bulaştığını kesin olarak kanıtlıyor.",
            "Bu keşiften sonra sıtmanın endemik olduğu bir bölgede halk sağlığı ekibinin uygulaması gereken en rasyonel mücadele kararı nedir?",
            [
                {
                    "text": "Tüm ağaçları kesip ormanları yok etmek.",
                    "outcome": "Ekolojik felaket yaratır, sivrisinekleri durdurmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Bataklıkları ve durgun suları kurutmak, su birikintilerini ilaçlamak (vektör mücadelesi) ve pencerelere tel takıp cibinlik kullanmak.",
                    "outcome": "Kusursuz vektör kontrolü: Sivrisinek üreme alanları yok edilerek sıtma bulaş zinciri kırılır.",
                    "isCorrect": True
                },
                {
                    "text": "Sıtmaya karşı halka yalnızca tuzlu su içirmek.",
                    "outcome": "Parazite hiçbir etkisi yoktur.",
                    "isCorrect": False
                }
            ]
        ),
        53: make_branching_logic(
            "1747 yılında HMS Salisbury gemisinde denizciler diş eti kanamaları ve kemik ağrılarıyla skorbütten kıvranıyor.",
            "İskoç cerrah James Lind'in tıp tarihinin ilk kontrollü klinik deneyini yürütürken vermesi gereken metodolojik karar nedir?",
            [
                {
                    "text": "Tüm hastalara rastgele büyü macunları vermek.",
                    "outcome": "Bilimsel kanıt değeri sıfırdır.",
                    "isCorrect": False
                },
                {
                    "text": "12 benzer hastayı ikişer kişilik 6 gruba ayırıp aynı diyeti vermek; gruplara elma şarabı, sirke, deniz suyu, vitriol ve narenciye (limon/portakal) vererek sonuçları karşılaştırmak.",
                    "outcome": "Kusursuz klinik araştırma tasarımı: Narenciye alan grubun hızla iyileşmesiyle skorbütün çaresi kanıtlanır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaları denize atarak geminin yükünü hafifletmek.",
                    "outcome": "Kabul edilemez cinayet.",
                    "isCorrect": False
                }
            ]
        ),
        56: make_branching_logic(
            "1700 yılında Modena'da Bernardino Ramazzini'ye sürekli nefes darlığı ve öksürükten yakınan 35 yaşında bir hasta başvuruyor.",
            "İş sağlığının babası kabul edilen Ramazzini'nin anamnez alırken sorması gereken kurucu soru nedir?",
            [
                {
                    "text": "'Dün gece hangi burç yıldızının altındaydınız?'",
                    "outcome": "Astrolojik safsata.",
                    "isCorrect": False
                },
                {
                    "text": "'Ne iş yaparsınız?' sorusunu sorarak hastanın taş kırma veya maden ocağında toz maruziyeti olup olmadığını öğrenmek.",
                    "outcome": "Kusursuz meslek hekimliği yaklaşımı: Hastalığın mesleki toz ve kimyasal maruziyetle ilişkisi aydınlatılır.",
                    "isCorrect": True
                },
                {
                    "text": "Hiçbir soru sormadan yalnızca kan alıp göndermek.",
                    "outcome": "Etiyolojiyi tamamen karanlıkta bırakan eksik hekimlik.",
                    "isCorrect": False
                }
            ]
        ),
        63: make_branching_logic(
            "Bir ülkenin Sağlık Bakanlığı sağlık bütçesini planlarken bütçenin %80'ini milyonda bir görülen nadir bir genetik sendromun ameliyatına mı, yoksa bebekleri öldüren ishal ve zatürreye mi ayırması gerektiğini tartışıyor.",
            "Alfred Grotjahn'ın sosyal hekimlik ilkeleri ışığında bakanlığın vermesi gereken en adil halk sağlığı kararı nedir?",
            [
                {
                    "text": "Tüm bütçe en nadir ve medyatik hastalığa ayrılmalı, yaygın bebek ölümleri görmezden gelinmelidir.",
                    "outcome": "Grotjahn kuralına tamamen aykırı: Kaynaklar israf edilir, binlerce bebek ölür.",
                    "isCorrect": False
                },
                {
                    "text": "Grotjahn'ın 'En önemli hastalıklar en çok öldüren, en sık görülen ve en çok sakat bırakanlardır' ilkesi uyarınca kaynaklar öncelikle bebek ishal ve zatürresine tahsis edilmelidir.",
                    "outcome": "Kusursuz halk sağlığı önceliklendirmesi: Toplumun en ağır yükünü oluşturan hastalıklar hedeflenerek devasa hayat kurtarılır.",
                    "isCorrect": True
                },
                {
                    "text": "Sağlık bütçesi tamamen sıfırlanıp lüks binalar yapılmalıdır.",
                    "outcome": "Halk sağlığı sistemini çökertecek vahim hata.",
                    "isCorrect": False
                }
            ]
        ),
        66: make_branching_logic(
            "İkinci Dünya Savaşı sonrası Yunanistan'da hastanede tedavi edilip kilo alan aç çocukların, köylerine döndükten sonra tekrar açlık ve hastalıkla hastaneye düşmesi tablosuyla karşılaşılıyor.",
            "Bu 'Yunanistan Deneyimi' karşısında uluslararası yardım kuruluşunun alması gereken kalıcı halk sağlığı kararı nedir?",
            [
                {
                    "text": "Çocukları ömür boyu hastane koğuşlarında kilitli tutmak.",
                    "outcome": "İnsan haklarına aykırı ve sürdürülemez bir hapislik.",
                    "isCorrect": False
                },
                {
                    "text": "Yalnızca hastanede bireysel tedaviyle yetinilmeyip; çocuğun ailesine iş, gıda güvencesi, temiz su ve sağlıklı barınma ortamı sağlayan toplumsal koruyucu programlar kurulmalıdır.",
                    "outcome": "Kusursuz halk sağlığı dersi: Hastalığın kök nedeni olan aile ve toplumsal çevre düzeltilerek kısır döngü kırılır.",
                    "isCorrect": True
                },
                {
                    "text": "Yardımları tamamen kesip çocukları kaderine terk etmek.",
                    "outcome": "Binlerce çocuğun ölümüne yol açacak vicdansızlık.",
                    "isCorrect": False
                }
            ]
        ),
        76: make_branching_logic(
            "1961 yılında Prof. Dr. Nusret Fişek 224 Sayılı Sosyalleştirme Kanunu'nu hazırlarken köylerde yaşayan yurttaşların hastanelere ulaşamadığı için öldüğünü görüyor.",
            "Fişek'in bu eşitsizliği ortadan kaldırmak için kurduğu Sağlık Ocakları teşkilatlanma kararı ne olmalıdır?",
            [
                {
                    "text": "Köylülerin şehre gelmesini zorunlu kılıp gelmeyenlere ceza yazmak.",
                    "outcome": "Ulaşım imkanı olmayan yoksul köylüyü ölüme terk etmektir.",
                    "isCorrect": False
                },
                {
                    "text": "Her köye sağlık evi açarak bir ebe yerleştirmek; kasabada hekim başkanlığında sağlık ocağı kurarak koruyucu ve tedavi edici hizmeti halkın ayağına ücretsiz götürmek.",
                    "outcome": "Kusursuz Türk sağlık devrimi: Sağlık Ocakları modeli ile anne-bebek ölümleri hızla düşer ve aşı kapsayıcılığı zirveye çıkar.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca başkente devasa bir hastane yapıp köyleri tamamen unutmak.",
                    "outcome": "Fırsat eşitliğini yok eden çarpık model.",
                    "isCorrect": False
                }
            ]
        ),
        92: make_branching_logic(
            "Bir ülkede kalp krizi ve akciğer kanseri vakaları hızla artıyor. Veriler hastaların çocukluk çağında sigaraya başladığını ve doymuş yağlı fast-food ile beslendiğini gösteriyor.",
            "Devletin bu risk faktörlerinin yeni nesillerde hiç ortaya çıkmamasını sağlamak amacıyla alması gereken primordial korunma kararı nedir?",
            [
                {
                    "text": "Hastalara yalnızca kalp krizi geçirdikten sonra stent takmak.",
                    "outcome": "Bu üçüncül korunmadır; primordial koruma ile ilgisi yoktur.",
                    "isCorrect": False
                },
                {
                    "text": "Okullarda tütün ve sağlıksız gıda reklamlarını yasaklamak, tütüne caydırıcı vergiler koymak ve çocuklara okulda sağlıklı beslenme ve spor ortamı sağlamak.",
                    "outcome": "Kusursuz primordial korunma: Risk faktörünün toplumda ve bireyde baştan oluşması engellenir.",
                    "isCorrect": True
                },
                {
                    "text": "Halkın sigara içmesini teşvik etmek.",
                    "outcome": "Halk sağlığı felaketi.",
                    "isCorrect": False
                }
            ]
        ),
        94: make_branching_logic(
            "35 yaşında hiçbir jinekolojik şikayeti ve kanaması olmayan sağlıklı bir kadın sağlık ocağına başvuruyor.",
            "Hekimin serviks kanserini henüz pre-semptomatik evrede yakalamak amacıyla uygulaması gereken ikincil korunma kararı nedir?",
            [
                {
                    "text": "'Hiçbir şikayetiniz yok, kanser olunca gelin' diyerek hastayı geri göndermek.",
                    "outcome": "Erken tanı fırsatını kaçıran ölümcül ihmal.",
                    "isCorrect": False
                },
                {
                    "text": "İkincil korunma kapsamında rutin servikal tarama (Pap-smear veya HPV-DNA testi) uygulayarak olası prekanseröz displaziyi belirti vermeden tespit etmek.",
                    "outcome": "Kusursuz ikincil korunma: Serviks kanseri pre-semptomatik evrede yakalanarak hayat kurtarılır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastanın rahmini acilen ameliyatla almak.",
                    "outcome": "Endikasyonsuz sakatlayıcı cerrahi.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_recalls():
    """Active recall soru sayısını 25'e çıkararak çeşitliliği dengeleyen ögeler."""
    return {
        10: make_active_recall(
            "Antik çağda hastalıkların kan, balgam, sarı safra ve kara safra sıvılarının dengesizliğinden kaynaklandığını savunan tıp teorisinin adı nedir?",
            "Humoral patoloji kuramı (Dört Sıvı Teorisi)",
            "Hipokrat'ın ortaya koyduğu antik vücut sıvıları teorisi"
        ),
        16: make_active_recall(
            "Venedik'te 14. yüzyılda salgın bölgelerinden gelen gemilerin limana girmeden açıkta 40 gün bekletilmesini ifade eden ve İtalyanca kökenden gelen halk sağlığı terimi nedir?",
            "Karantina (Quaranta giorni)",
            "Kırk gün anlamına gelen tecrit terimi"
        ),
        18: make_active_recall(
            "Osmanlı İmparatorluğu'nda Edirne II. Bayezid Külliyesi Şifahanesi'nde akıl hastalarını tedavi etmek için kullanılan iki temel doğal terapi unsuru nedir?",
            "Su sesi ve müzik (makamlarla musiki)",
            "Akustik kubbe altında uygulanan Osmanlı terapi unsurları"
        ),
        26: make_active_recall(
            "Robert Koch'un mikrobiyolojide tek bir bakteriden köken alan saf koloniler elde etmek için patatesten sonra geliştirdiği katı besiyeri maddesi nedir?",
            "Agar-agar (katı agar)",
            "Deniz yosunundan elde edilen jelleştirici madde"
        ),
        36: make_active_recall(
            "1890 yılında difteri toksinine karşı bağışık atların serumunu kullanarak pasif bağışıklamayı başlatan ve ilk Nobel Tıp Ödülü'nü alan bilim insanı kimdir?",
            "Emil von Behring",
            "Difteri antitoksinini geliştiren Alman hekim"
        ),
        44: make_active_recall(
            "1854 Londra kolera salgınında su tulumbasının kolunu söktürerek salgını durduran ve modern epidemiyolojinin babası sayılan hekim kimdir?",
            "John Snow",
            "Broad Street kolera araştırmacısı anestezi hekimi"
        ),
        48: make_active_recall(
            "1897 yılında sıtma paraziti Plasmodium'un insandan insana hangi dişi sivrisinek türü ile bulaştığını kanıtlayan hekim kimdir?",
            "Ronald Ross (Anofel sivrisineği)",
            "Sıtma vektörünü bularak Nobel alan İngiliz hekim"
        ),
        54: make_active_recall(
            "1747 yılında gemide skorbüt hastalarına limon ve portakal vererek ilk kontrollü klinik beslenme deneyini gerçekleştiren İskoç cerrah kimdir?",
            "James Lind",
            "Skorbütün narenciyeyle tedavisini kanıtlayan cerrah"
        ),
        58: make_active_recall(
            "1700 yılında yazdığı eserle iş sağlığı ve meslek hastalıklarının kurucusu kabul edilen ve hekimlere 'Ne iş yaparsınız?' diye sormalarını öğütleyen İtalyan hekim kimdir?",
            "Bernardino Ramazzini",
            "De Morbis Artificum Diatriba kitabının yazarı"
        ),
        64: make_active_recall(
            "Yukarı Silezya tifüs salgınını inceledikten sonra 'Tıp bir sosyal bilimdir ve politika geniş kapsamlı tıptan başka bir şey değildir' diyen ünlü patolog kimdir?",
            "Rudolf Virchow",
            "Hücresel patolojinin ve sosyal tıbbın Alman kurucusu"
        ),
        70: make_active_recall(
            "Dünya Sağlık Örgütü'nün (DSÖ) 1948 Anayasası'nda yer alan tanımına göre sağlık hangi üç yönden tam bir iyilik halidir?",
            "Bedenen, ruhen ve sosyal yönden tam bir iyilik hali",
            "Sağlığın fiziksel, mental ve toplumsal üç boyutu"
        ),
        78: make_active_recall(
            "1961 yılında çıkarılan ve Türkiye'de sağlık ocakları sistemini, entegre koruyucu hekimliği ve sevk zincirini kuran tarihi kanunun numarası nedir?",
            "224 sayılı kanun (Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun)",
            "Nusret Fişek'in mimarı olduğu tarihi Türk sağlık yasası"
        ),
        84: make_active_recall(
            "1978 yılında Kazakistan'da toplanan ve '2000 Yılında Herkese Sağlık' hedefini ilan eden tarihi küresel halk sağlığı konferansı nerede yapılmıştır?",
            "Alma-Ata (Alma-Ata Konferansı)",
            "Temel Sağlık Hizmetleri Bildirgesi'nin imzalandığı tarihi kent"
        ),
        94: make_active_recall(
            "Hastalık riskini artıran sosyal, ekonomik ve kültürel yaşam tarzı özelliklerinin toplumda ve çocuklarda hiç oluşmamasını sağlamayı amaçlayan en erken korunma düzeyi hangisidir?",
            "Primordial korunma",
            "Risk faktörünün oluşmasını baştan önleyen düzey"
        ),
        98: make_active_recall(
            "Asemptomatik bir kadında serviks kanserini henüz belirti vermeden yakalamak amacıyla yapılan rutin Pap-smear veya HPV-DNA taraması hangi korunma düzeyindedir?",
            "İkincil (sekonder) korunma",
            "Erken tanı ve taramaları kapsayan korunma düzeyi"
        ),
        100: make_active_recall(
            "Klinik diyabet tanısı almış bir hastada kangren ve bacak amputasyonunu önlemek amacıyla yapılan ayak bakımı eğitimi ve rehabilitasyon hangi korunma basamağına girer?",
            "Üçüncül (tersiyer) korunma",
            "Sakatlığı sınırlandırma ve rehabilitasyon basamağı"
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
