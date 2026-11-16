# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını garanti eder.
"""

from scripts.k1_11_deck_data.helpers import (
    make_branching_logic, make_before_after, make_causal_chain
)

def get_extra_branching():
    """Branching logic (klinik karar verme) oranını artırmak için hedeflenen slaytlara eklenecek ögeler."""
    return {
        4: make_branching_logic(
            "45 yaşında kadın hasta, jinekolojik serviks kanseri cerrahisi ve radyoterapi sonrası her iki yan ağrısı ve oligüri ile başvuruyor. USG'de bilateral orta derecede hidronefroz ve retroperitoneal alanda üreterleri saran fibrotik doku saptanıyor.",
            "Bu hastadaki üreter obstrüksiyonunun temel anatomik ve etiyolojik sınıflandırması nedir?",
            [
                {
                    "text": "Bilateral, kronik, edinsel ve ekstrensek üreter obstrüksiyonudur.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Radyoterapiye bağlı retroperitoneal fibrozis ve tümör basısı üreteri dışarıdan sıkıştıran ekstrensek bir nedendir."
                },
                {
                    "text": "Unilateral, konjenital ve intralüminal üreter taşı tıkanıklığıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Tablo bilateraldir, edinseldir ve intralüminal değil ekstrensektir."
                },
                {
                    "text": "İnfravezikal prostat hiperplazisine bağlı mesane çıkım obstrüksiyonudur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Hasta kadındır ve sorun üreter seviyesindedir."
                }
            ]
        ),
        8: make_branching_logic(
            "60 yaşında erkek hasta, 24 saattir hiç idrar yapamama (akut retansiyon) ve suprapubik bölgede dayanılmaz şişkinlik ve ağrı ile acil servise geliyor. Muayenede göbek altına kadar uzanan hassas, fluktuan kitle (glob vezikale) palpe ediliyor.",
            "Bu hastada acil hekiminin yapması gereken en öncelikli tanısal ve terapötik girişim nedir?",
            [
                {
                    "text": "Derhal 16-18 F üretral Foley kateter takılarak mesane kademeli olarak boşaltılmalı ve rahatlatılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Akut glob vezikalede ilk ve en acil adım üretral kateterizasyonla mesanenin dekomprese edilmesidir."
                },
                {
                    "text": "Hastaya bol IV sıvı verilip idrarın kendiliğinden çıkması beklenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Mesane zaten tıkalıdır; ek sıvı vermek mesane rüptürü riskini artırır."
                },
                {
                    "text": "Ürodinami randevusu verilerek hasta 2 hafta sonraya polikliniğe yönlendirilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Glob vezikale acil dekompresyon gerektirir, ertelenemez."
                }
            ]
        ),
        14: make_branching_logic(
            "52 yaşında erkek hasta, her iki bacakta hafif ödem, kilo kaybı ve bel ağrısı ile başvuruyor. Laboratuvarda sedimentasyon yüksek, üre 80 mg/dL, kreatinin 2.8 mg/dL saptanıyor. BT'de L4-L5 düzeyinde aortu saran ve her iki üreteri medyale çekerek tıkayan retroperitoneal fibrotik plak izleniyor.",
            "Bu klinik tablonun (Ormond hastalığı) ayırıcı tanısında ve ilk yönetiminde ne hedeflenmelidir?",
            [
                {
                    "text": "IgG4 ilişkili retroperitoneal fibrozis düşünülmeli; önce üreteral stent veya nefrostomi ile böbrekler korunmalı, ardından kortikosteroid tedavisi planlanmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. RPF'de üremi varsa acil stentleme/drenaj şarttır; medikal olarak steroidlere yüksek yanıt verir."
                },
                {
                    "text": "Hemen her iki üreter rezeke edilip hastaya bilateral üreterostomi açılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Erken evrede medikal tedavi ve stentleme yeterlidir, kalıcı kutanöz stoma yapılmaz."
                },
                {
                    "text": "Hastaya yüksek doz kalsiyum verilerek taşın düşmesi beklenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Sorun taş değil retroperitoneal fibrozistir."
                }
            ]
        ),
        17: make_branching_logic(
            "25 yaşında erkek hasta, motosiklet kazası sonrası pelvik kemik fraktürü ile acile getiriliyor. Muayenede eksternal meatus ucunda kan damlası saptanıyor ve rektal muayenede prostat yukarı doğru yer değiştirmiş (yüksek yerleşimli) bulunuyor.",
            "Bu hastada üretral obstrüksiyon ve yaralanma şüphesinde yapılması gereken doğru yaklaşım nedir?",
            [
                {
                    "text": "Körlemesine Foley sonda ASLA takılmamalıdır; retrograd üretrografi çekilmeli veya acil suprapubik sistostomi açılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Meada kan ve yüksek yerleşimli prostat posterior üretra kopmasını düşündürür; kör sonda yırtığı tam kopmaya çevirir."
                },
                {
                    "text": "Geniş lümenli bir metal sonda ile üretraya kuvvetlice girilerek mesaneye ulaşılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bu işlem üretrayı tamamen parçalar ve sahte pasaj oluşturur."
                },
                {
                    "text": "Hastaya genel anestezi verilip doğrudan üretra rezeksiyonu yapılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Akut travmada ilk adım suprapubik drenajdır, rekonstrüksiyon aylar sonra yapılır."
                }
            ]
        ),
        22: make_branching_logic(
            "64 yaşında erkek hasta, BPH tanısıyla takip edilirken son haftalarda gündüz 12 kez, gece 5 kez idrara çıkma, ani sıkışma ve tuvalete yetişememe şikayetleriyle başvuruyor. Yapılan USG'de işeme sonrası mesanede 35 ml idrar saptanıyor.",
            "Hastanın hangi infravezikal evrede olduğu ve semptomların kaynağı nedir?",
            [
                {
                    "text": "İrritasyon / konjesyon evresindedir; mesane mukozal venöz konjesyonu ve ödemi aşırı duyarlılık ve pollaküri yapmaktadır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Rezidüel idrarın 50 ml altında olması ve irritatif LUTS semptomlarının baskınlığı bu evreyi kanıtlar."
                },
                {
                    "text": "Terminal dekompansasyon evresindedir; mesane kası tamamen felç olmuştur.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Dekompansasyonda rezidüel idrar >500 ml olur."
                },
                {
                    "text": "Kompansasyon evresindedir; hastada hiçbir semptom bulunmamaktadır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kompansasyonda irritatif LUTS semptomları ve rezidüel idrar görülmez."
                }
            ]
        ),
        33: make_branching_logic(
            "Akut üreter taş obstrüksiyonu olan hastanın yapılan IVP'sinde toplayıcı sistemde forniks açılarının küntleştiği ve papillaların düzleştiği görülüyor.",
            "Bu morfolojik değişimin böbrek içi basınç iletimi açısından anlamı nedir?",
            [
                {
                    "text": "Toplayıcı sistemde hidrostatik basıncın ilk olarak kaliksleri etkilediğini ve retrograd parankim basısının başladığını gösterir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Kaliks küntleşmesi (clubbing) erken hidrostatik basınç hasarının ilk anatomik kanıtıdır."
                },
                {
                    "text": "Böbreğin artık tamamen iyileştiğini ve taşın eridiğini gösterir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Küntleşme patolojik basınç hasarı bulgusudur."
                },
                {
                    "text": "Kalikslerin idrarı geriye emerek kalıcı koruma sağladığını gösterir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Forniks küntleşmesi koruma değil parankim ezilme başlangıcıdır."
                }
            ]
        ),
        43: make_branching_logic(
            "Deneysel akut tam üreter ligasyonu yapılan bir hayvanda ilk 90 dakikada renal kan akımı %30 artarken, 4. saatten itibaren hızla düşerek bazalin yarısına iniyor.",
            "Bu hemodinamik tablonun ikinci fazındaki (vazokonstriksiyon) baskın aracı moleküller hangileridir?",
            [
                {
                    "text": "Tromboksan A2 (TXA2) ve Anjiyotensin II",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Geç faz vazokonstriksiyonunu TXA2 ve lokal RAAS aktivasyonu (Ang II) yönetir."
                },
                {
                    "text": "Asetilkolin ve Bradikinin",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Bu moleküller geç vazokonstriksiyondan sorumlu primer mediyatörler değildir."
                },
                {
                    "text": "İnsülin ve Glukagon",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Glukoz metabolizma hormonlarıdır."
                }
            ]
        ),
        52: make_branching_logic(
            "Kronik obstrüktif nefropatili bir hastada serum sodyumu 142 mEq/L, plazma osmolaritesi 295 mOsm/kg iken; idrar dansitesi 1008 ve idrar osmolaritesi 240 mOsm/kg ölçülüyor.",
            "Toplayıcı tübüllerdeki bu konsantrasyon kusurunun hücresel temeli nedir?",
            [
                {
                    "text": "ADH'ya karşı toplayıcı kanal esas hücrelerinde reseptör ve cAMP duyarsızlığı ile Akuaporin-2 ekspresyon kaybıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Obstrüksiyonda gelişen edinsel nefrojenik DI tablosunun temeli AQP2 azalması ve medüller yıkanmadır."
                },
                {
                    "text": "Böbreğin fazla suyu tutmak için sodyumu tamamen idrara dökmesidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Hipostenüri suyun tutulamamasından kaynaklanır."
                },
                {
                    "text": "Glomerül podositlerinin tamamen yok olmasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Podosit hasarı nefrotik proteinüri yapar, hipostenüri yapmaz."
                }
            ]
        ),
        62: make_branching_logic(
            "34 yaşında erkek hasta, sağ böğründen başlayıp sağ testisine ve kasığına vuran, kıvrandırıcı, bulantı ve kusmanın eşlik ettiği şiddetli ağrıyla acil servise geliyor. İdrar tahlilinde mikroskobik hematüri saptanıyor.",
            "Bu ağrının yansıma paternine göre üreter taşının en olası anatomik lokalizasyonu neresidir?",
            [
                {
                    "text": "Distal üreter veya üreterovezikal bileşke (UVJ) seviyesindedir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. T11-L1 dermatomlarıyla testise ve labiuma yansıyan ağrı distal intramural üreter taşlarını gösterir."
                },
                {
                    "text": "Üst kaliks forniksi içindedir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kaliks içi taşlar testise yansımaz, sırtta kostavertebral ağrı yapar."
                },
                {
                    "text": "Eksternal üretral meatus ağzındadır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Meatus taşları penis ucunda lokal batma yapar, böğür koliği yapmaz."
                }
            ]
        ),
        66: make_branching_logic(
            "Tek taraflı üreter darlığı olan 40 yaşında bir hastada kan basıncı 160/100 mmHg ölçülüyor. Plazma renin aktivitesi belirgin yüksek bulunuyor. Başarılı bir endoürolojik ameliyatla üreter darlığı açılıyor.",
            "Ameliyattan 48 saat sonra hastanın kan basıncında beklenen fizyolojik değişim nedir?",
            [
                {
                    "text": "Renal kan akımının düzelmesiyle renin salgısı normale döner ve arteryel kan basıncı hızla normale geriler.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Tek taraflı tıkanıklıkta hipertansiyon renin bağımlıdır; perfüzyon düzelince tansiyon düşer."
                },
                {
                    "text": "Kan basıncı iki katına çıkarak malign hipertansif krize dönüşür.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Obstrüksiyon açıldığında vazokonstriktör uyarı biter, tansiyon yükselmez."
                },
                {
                    "text": "Hipertansiyon hiçbir şekilde değişmez, ömür boyu kalıcı seyreder.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Obstrüksiyona bağlı sekonder hipertansiyon dekompresyonla düzelir."
                }
            ]
        ),
        73: make_branching_logic(
            "Akut renal kolik tablosundaki 48 yaşında hastaya kontrassız helikal taş BT çekiliyor. Sağ distal üreterde 6 mm taş, proksimal üreterde dilatasyon ve sağ böbrek etrafında 'perirenal stranding' izleniyor.",
            "Tomografide görülen 'perirenal stranding' bulgusunun klinik ve patofizyolojik anlamı nedir?",
            [
                {
                    "text": "Yüksek intrapelvik basıncın pyelointerstisyel reflü ile perirenal yağ dokusuna ödem ve sıvı sızdırmasını gösteren obstrüksiyon kanıtıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Perirenal stranding intrapelvik basınç artışının ve interstisyel dekompresyonun objektif tomografik işaretidir."
                },
                {
                    "text": "Böbreğin tamamen kanser dokusuna dönüştüğünü gösterir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Perirenal yağ kirlenmesi akut inflamasyon ve ödem bulgusudur, malignite değildir."
                },
                {
                    "text": "Taşın vücut dışına kendiliğinden atıldığını gösterir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Taş hala distal üreterde lümeni tıkamaktadır."
                }
            ]
        ),
        83: make_branching_logic(
            "Sol böbreğinde 2 cm staghorn taş ve toplayıcı sistemde yoğun püy (piyonefroz) saptanan, septik şok tablosundaki bir hastada acil dekompresyon planlanıyor. Sistoskopide üreter orifisi ödemden dolayı bulunamıyor.",
            "Bu kritik aşamada hastanın hayatını kurtaracak girişimsel yaklaşım ne olmalıdır?",
            [
                {
                    "text": "Girişimsel radyoloji / üroloji tarafından acil USG eşliğinde Perkütan Nefrostomi (PNS) takılarak sistem dışarıya drene edilmelidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Retrograd yol tıkalı veya bulunamıyorsa perkütan nefrostomi en emniyetli hayat kurtarıcı drenajdır."
                },
                {
                    "text": "Sistoskopi sonlandırılıp hasta serviste yalnızca antibiyotikle takip edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Drenajsız piyonefroz ölümcüldür."
                },
                {
                    "text": "Hastaya yüksek doz idrar söktürücü verilerek taşın itilmesi beklenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Tıkalı sisteme diüretik vermek toplayıcı sistemi patlatır."
                }
            ]
        ),
        85: make_branching_logic(
            "Bilateral üreter taş obstrüksiyonu nedeniyle 10 gündür idrarı çok azalan ve kreatinini 8.2 mg/dL'ye çıkan hastaya bilateral JJ stent takılıyor. İşlemden sonraki ilk 4 saatte hasta 1800 ml idrar çıkarıyor.",
            "Bu postobstrüktif diürez tablosunun tetiklenmesindeki en güçlü ozmotik solüt hangisidir?",
            [
                {
                    "text": "Kanda aşırı birikmiş olan ve hızla filtre edilerek tübüllerde ozmotik su çeken üre molekülüdür.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Üre retansiyonu ve filtrasyonu POD tablosundaki temel ozmotik itici güçtür."
                },
                {
                    "text": "Kandaki kalsiyum iyonlarının glomerülde donmasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Kalsiyum ozmotik diürez başlatmaz."
                },
                {
                    "text": "Böbrek tübüllerinin tamamen kaybolarak idrarı tutamamasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Solüt yükünün atılımı fizyolojik bir süreçtir."
                }
            ]
        ),
        92: make_branching_logic(
            "22 yaşında genç erkek hasta, sol yan ağrısı ve sintigrafide sol UPJ darlığı (T1/2 > 28 dk) ve diferansiyel renal fonksiyon %38 saptanarak ameliyata alınıyor. İntraoperatif olarak pelvisi çaprazlayan aberran bir alt pol arteri izleniyor.",
            "Uygulanacak Anderson-Hynes piyeloplastide aberran damara yönelik en doğru cerrahi manevra nedir?",
            [
                {
                    "text": "Üreteropelvik bileşke rezeke edilir, renal parankim iskemisini önlemek için damar KESİLMEZ; üreter damarın arkasından öne taşınarak yeni anastomoz yapılır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Aberran alt pol renal damarı kesilirse alt pol infarktı gelişir; üreter transpoze edilir."
                },
                {
                    "text": "Aberran damar bağlanıp kesilir ve çöpe atılır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Alt pol renal arterinin kesilmesi renal parankim nekrozu ve hipertansiyon yapar."
                },
                {
                    "text": "Damara dokunulmaz, yalnızca mesaneye sonda takılıp operasyon kapatılır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Mekanik bası çözülmeden darlık düzelmez."
                }
            ]
        ),
        95: make_branching_logic(
            "Retroperitoneal fibrozis nedeniyle 6 aydır steroid tedavisi alan 56 yaşında hastada kontrol BT'de fibrotik plağın küçülmediği, üreterleri sıkıştırmaya devam ettiği ve bilateral hidronefrozun ilerlediği görülüyor.",
            "Medikal tedaviye dirençli bu olguda planlanması gereken definitif cerrahi yaklaşım nedir?",
            [
                {
                    "text": "Cerrahi üreterolizis (üreterlerin plaktan kurtarılması) ve nüksü önlemek için canlı omentumla sarılması (omentoplasti).",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Dirençli RPF'de altın standart cerrahi üreterolizis ve omental wrapping işlemidir."
                },
                {
                    "text": "Hastanın her iki böbreğinin çıkarılarak hemodiyalize başlatılması.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Nefronlar sağlamdır, üreterler kurtarılabilir."
                },
                {
                    "text": "Tüm karın içi organların rezeke edilmesi.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Agresif ve anlamsız bir yaklaşımdır."
                }
            ]
        ),
        99: make_branching_logic(
            "Bilateral ileri hidronefroz ve üremi ile başvuran bir hastada radyoloji, üroloji ve nefroloji konsültasyonu yapılıyor.",
            "Bu multidisipliner ekipte nefroloji uzmanının üstleneceği en kritik primer sorumluluk nedir?",
            [
                {
                    "text": "Dekompresyon sonrası gelişebilecek postobstrüktif diürezin sıvı-elektrolit resüsitasyonunu ve asit-baz dengesini yönetmek.",
                    "isCorrect": True,
                    "feedback": "Doğrudur. Nefroloji POD sürecinde ölümcül elektrolit dengesizliklerini ve metabolik asidozu izler."
                },
                {
                    "text": "Hastaya genel anestezi altında açık piyeloplasti ameliyatını bizzat yapmak.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Cerrahi ürolojinin görev alanıdır."
                },
                {
                    "text": "Bilgisayarlı tomografi cihazını bizzat kumanda etmek.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır. Görüntüleme radyolojinin sorumluluğundadır."
                }
            ]
        )
    }

def get_extra_sliders():
    """Before/after slider (karşılaştırma) oranını artırmak için hedeflenen slaytlara eklenecek ögeler."""
    return {
        3: make_before_after(
            "Renal Düzey Obstrüksiyon Etyolojileri",
            "Konjenital Lezyonlar",
            "UPJ darlığı, aberran damar basısı, polikistik böbrek ve peripelvik kistler.",
            "Neoplastik / İnflamatuar",
            "Wilms tümörü, RCC, renal pelvis TCC'si, tüberküloz kavitasyonu ve taşlar."
        ),
        5: make_before_after(
            "Mesane Çıkımı vs Üretra Obstrüksiyonu",
            "Mesane Çıkımı Düzeyi (BPH)",
            "Orta ve ileri yaş erkeklerde prostat hiperplazisi, detrüsör yorgunluğu ve rezidüel idrar.",
            "Üretra Düzeyi (Darlık / Valv)",
            "Erken yaşta posterior üretral valv, erişkinde travmatik/enfeksiyöz üretra darlıkları."
        ),
        7: make_before_after(
            "İnfravezikal Obstrüksiyonda Mesane vs Üst Sistem",
            "Erken Mesane Yanıtı",
            "Detrüsör hipertrofisi, intravezikal basınç yükselmesi ve trabekülasyon gelişimi.",
            "İleri Üst Sistem Etkilenimi",
            "Vezikoüreteral reflü, bilateral hidroüreteronefroz ve parankimal böbrek yetmezliği."
        ),
        31: make_before_after(
            "Supravezikal Obstrüksiyon Taraf Etkilenimi",
            "Unilateral Obstrüksiyon",
            "Tek böbreği ilgilendirir, sağlam karşı böbrek azotemiyi önler, renin yüksekliği görülebilir.",
            "Bilateral Obstrüksiyon",
            "Her iki böbreği vurur, hızla akut anüri, derin azotemi, hiperkalemi ve üremi tablosu üretir."
        ),
        35: make_before_after(
            "Toplayıcı Sistem Hasarının Zaman Çizelgesi",
            "İlk 6 Günlük Dönem",
            "Kollektör kanallarda hücresel bütünlük korunur; pasif gerilme ve dilatasyon hakimdir.",
            "7. Gün ve Sonrası",
            "Kollektör epitelinde nekroz ve atrofi başlar; interstisyuma idrar sızıntısı ve fibrozis gelişir."
        ),
        41: make_before_after(
            "Glomerüler Filtrasyon Kuvvetleri",
            "Filtrasyonu Destekleyen Kuvvet",
            "Glomerül içi hidrostatik basınç (yaklaşık 70 mmHg; sistemik arter basıncının %60'ı).",
            "Filtrasyona Karşı Koyan Kuvvetler",
            "Kapiller onkotik basınç (25-30 mmHg) ve Bowman kapsülü içi hidrostatik basınç (10-15 mmHg)."
        ),
        47: make_before_after(
            "Sitokin Kaynaklı Doku Dönüşümü",
            "TNF-Alfa Etkisi",
            "Ölüm reseptörlerini aktive ederek tübüler epitel hücrelerinde masif apoptozu tetikler.",
            "TGF-Beta Etkisi",
            "Fibroblastları miyofibroblasta dönüştürerek ekstraselüler matriks ve geri dönüşümsüz fibrozis üretir."
        ),
        63: make_before_after(
            "Oligüri vs Anüri Ayrımı",
            "Oligüri (< 400-500 ml/gün)",
            "Prerenal azotemi, akut tübüler nekroz veya parsiyel obstrüksiyonda izlenir.",
            "Ani Anüri (< 50-100 ml/gün)",
            "Bilateral tam mekanik tıkanıklık veya soliter böbrek obstrüksiyonunun kardinal acil bulgusudur."
        ),
        71: make_before_after(
            "Görüntüleme Yöntemleri Triyajı",
            "Ultrasonografi (İlk Basamak)",
            "Radyasyonsuz, hızlı, kontrast gerektirmez; hidronefroz ve mesane durumunu tarar.",
            "Kontrassız Taş BT (Altın Standart)",
            "Tüm taşları milimetrik gösterir, perirenal stranding ve tam anatomik lokalizasyonu verir."
        ),
        91: make_before_after(
            "BPH Girişimlerinde Doku Rezeksiyonu",
            "Klasik TUR-P",
            "Adenom dokusunu içeriden elektrik teliyle traşlayarak lümeni tünel gibi genişletir.",
            "Anatomik HoLEP",
            "Adenom loblarını cerrahi kapsül planından tamamen sıyırıp mesaneye atarak çıkarır."
        )
    }

def get_extra_causal_chains():
    """Causal chain (mekanizma zinciri) oranını artırmak için hedeflenen slaytlara eklenecek ögeler."""
    return {
        6: make_causal_chain(
            "Yaşa Göre Obstrüksiyon Epidemiyolojisi Zinciri",
            [
                "1. Neonatal / Çocukluk: Erkek çocuklarda posterior üretral valv ve UPJ darlığı hakimiyeti",
                "2. Genç Erişkinlik: Nefrolitiyazis, travmatik üretra darlıkları ve gebelik hidronefrozu",
                "3. İleri Yaş Erkek: BPH ve prostat kanseri insidansının tavan yapması",
                "4. İleri Yaş Kadın: Serviks/uterus kanserleri ve pelvik organ prolapsusuna bağlı bası"
            ]
        ),
        18: make_causal_chain(
            "İlaca Bağlı Üriner Retansiyon Kaskadı",
            [
                "1. Antikolinerjik / Antihistaminik Alımı: Detrüsör muskarinik M3 reseptörlerinin bloke edilmesi",
                "2. Detrüsör Felci: Mesane kasılma gücünün aniden sıfıra inmesi",
                "3. Alfa-Agonist Etki: Mesane boynu ve sfinkter düz kas tonusunun aşırı artması",
                "4. Akut Retansiyon: Hastanın idrarını hiç başlatamaması ve glob vezikale oluşması"
            ]
        ),
        54: make_causal_chain(
            "Obstrüktif Hipostenürik Poliüri Mekanizması",
            [
                "1. Kronik İskemi: Medüller piramitlerin yüksek basınçla ezilmesi",
                "2. Yıkanma Etkisi: Vaza rektaların medüller hipertonik sodyum gradyentini silmesi",
                "3. AQP2 Azalması: Toplayıcı kanalların suya geçirimsiz hale gelmesi",
                "4. Dilüe Poliüri: Plazmadan daha sulu, düşük dansiteli idrarın dışarı atılması"
            ]
        ),
        64: make_causal_chain(
            "Kronik Sinsi Obstrüksiyonda Üremi Zinciri",
            [
                "1. Ağrısız İlerleme: Kapsül gerilmeden hidronefrozun aylar içinde büyümesi",
                "2. Parankim Erimesi: Korteks kalınlığının 4-6 mm'ye kadar incelmesi",
                "3. Azotemi Gelişimi: Üre, kreatinin ve ürik asitin kanda birikmesi",
                "4. Klinik Toksisite: Asteriksis, konfüzyon ve üremik ensefalopati tablosu"
            ]
        ),
        84: make_causal_chain(
            "Postobstrüktif Diürezde Sıvı-Elektrolit Kayıp Zinciri",
            [
                "1. Barajın Açılması: Bilateral tıkanıklığın kateter ile hızla dekomprese edilmesi",
                "2. Üre Hücumu: Birikmiş yüksek konsantrasyonlu ürenin tübüllere dolması",
                "3. Ozmotik Kaçış: Ürenin lümende devasa su ve sodyum kütlesini peşinden sürüklemesi",
                "4. Hipovolemi Riski: Saatte 300-500 ml idrar çıkışıyla hastanın dehidrate olması"
            ]
        ),
        94: make_causal_chain(
            "Ürolitiyazis Cerrahi Karar Zinciri",
            [
                "1. Taş Boyut Tayini: Kontrassız BT ile taş milimetresi ve dansitesinin (HU) ölçülmesi",
                "2. Minimal İnvaziv Seçim: 20 mm altı için ESWL veya Fleksibl URS/RIRC planlanması",
                "3. Kompleks Staghorn Seçim: 20 mm üstü büyük kitleler için Perkütan Nefrolitotomi (PCNL)",
                "4. Tıkanıklığın Giderilmesi: Antegrad akımın sağlanıp renal fonksiyonun kurtarılması"
            ]
        )
    }
