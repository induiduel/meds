# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 7: Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları (Slayt 61 - 70)
Checkpoint 7: Slayt 69
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # Slayt 61: Lohusalık (Puerperium) Dönemi Tanımı ve İnvolüsyon
    slides.append({
        "id": "k1-23-s61",
        "title": "Lohusalık (Puerperium) Dönemi Tanımı ve İnvolüsyon",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 61,
        "narrative": (
            "Lohusalık (Puerperium); plasentanın ayrılıp atılmasıyla başlayan ve kadının anatomik, fizyolojik ve "
            "psikolojik sistemlerinin gebelik öncesi durumuna döndüğü **doğumdan sonraki 42 günlük (6 haftalık)** süreci kapsar. "
            "Bu dönemin merkezinde **uterus involüsyonu** yer alır: "
            "Doğumdan hemen sonra yaklaşık 1000 gram ağırlığında ve göbek deliği hizasında olan uterus, "
            "düzenli miyometriyum kasılmalarıyla küçülerek 6. haftanın sonunda 60-80 gramlık normal ağırlığına ve "
            "küçük pelvisteki anatomik yerine geri döner. "
            "Bu süreçte plasenta yatağındaki yaranın iyileşmesiyle vajinadan **Loşi (Lochia)** adı verilen akıntı gelir: "
            "İlk 3-4 gün kanlı koyu kırmızı (lochia rubra), sonra pembe-kahverengi seröz (lochia serosa), "
            "10. günden sonra ise beyazımsı-sarı müköz (lochia alba) halini alır. "
            "Loşinin aniden kötü kokulu olması puerperal sepsis alarmıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Doğum sonrasında annenin üreme organlarının gebelik öncesi durumuna döndüğü altı haftalık döneme lohusalık adı verilir.",
                "lohusalık",
                "Kırk iki gün süren puerperium dönemi"
            ),
            make_table(
                "Lohusalıkta Uterus İnvolüsyonu ve Loşi Evreleri",
                ["Lohusalık Zamanı", "Uterus Fundus Seviyesi", "Uterus Ağırlığı", "Gelen Akıntı (Loşi) Tipi"],
                [
                    ["Doğumdan Hemen Sonra", "Göbek çukuru (Umblikus) hizasında", "~1000 gram", "Lochia Rubra (Koyu kırmızı kanlı)"],
                    [
                        "1. Haftanın Sonu",
                        {"text": "Simfizis pubis ile göbek ortasında", "isMasked": True, "hint": "Yarı yarıya küçülen fundus pozisyonu"},
                        "~500 gram",
                        "Lochia Serosa (Pembe-kahve seröz)"
                    ],
                    ["2. Haftanın Sonu", "Pelvis içine çekilir (karından palpe edilmez)", "~300 gram", "Lochia Alba (Beyazımsı sarı müköz)"],
                    ["6. Haftanın Sonu (Puerperium Sonu)", "Tamamen pelvis içinde normal boyutta", "~60 - 80 gram", "Akıntı tamamen kesilmiş veya normal"]
                ]
            ),
            make_active_recall(
                "Lohusalık döneminde vajinal akıntının (loşi) kötü kokulu, pürülan hale gelmesi ve ateş eşlik etmesi öncelikle hangi ciddi enfeksiyonu düşündürür?",
                "Puerperal Sepsis (Endometrit) tablosunu düşündürür.",
                "Lohusalık rahim içi enfeksiyonu"
            )
        ]
    })

    # Slayt 62: Lohusa İzleminin Amaçları: Kanama, Sepsis, Depresyon ve Emzirme
    slides.append({
        "id": "k1-23-s62",
        "title": "Lohusa İzleminin Amaçları: Kanama, Sepsis, Depresyon ve Emzirme",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 62,
        "narrative": (
            "Geleneksel toplumlarda doğum gerçekleştikten sonra annenin takibi ihmal edilir; oysa anne ölümlerinin %60'ından fazlası "
            "doğum sonrasındaki lohusalık evresinde meydana gelir. Lohusa izleminin temel halk sağlığı hedefleri şunlardır: "
            "1. **Maternal Komplikasyonların Erken Tespiti:** Postpartum kanama (atoni, plasenta retansiyonu), "
            "puerperal sepsis (endometrit), meme komplikasyonları (meme başı çatlağı, angorjman, mastit, abse), "
            "idrar yolu enfeksiyonu, derin ven trombozu ve preeklampsinin postpartum alevlenmesi. "
            "2. **Ruh Sağlığı Değerlendirmesi:** Annelerin %50-80'inde görülen hafif geçici hüzün (Baby Blues / Annelik Hüznü) ile "
            "ciddi tedavi gerektiren **Postpartum Depresyon ve Postpartum Psikozun** taranması (Edinburgh ölçeği). "
            "3. **Bebek Bakımı ve Emzirme Desteği:** Anne sütünün teşviki, tekniğin kontrolü. "
            "4. **Postpartum Aile Planlaması:** Emzirme dönemine uygun kontrasepsiyonun başlatılması."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Lohusa izleminin temel hedeflerinden biri erken dönemde ölümcül kanama ve puerperal sepsis komplikasyonlarını saptamaktır.",
                "puerperal sepsis",
                "Doğum sonrası lohusalık humması enfeksiyonu"
            ),
            make_before_after(
                "Lohusalık Ruh Sağlığı: Annelik Hüznü (Baby Blues) vs Postpartum Depresyon",
                "Annelik Hüznü (Baby Blues)",
                "Doğumdan sonraki ilk haftada başlar; hafif duygusallık ve ağlama nöbetleri vardır; 2 hafta içinde kendiliğinden geçer, tedavi gerekmez.",
                "Postpartum Depresyon",
                "2 haftadan uzun sürer; derin çökkünlük, bebeğe ilgisizlik, yetersizlik hissi ve intihar düşünceleri vardır; acil psikiyatrik tedavi şarttır.",
                "Lohusalık psikiyatrik tablolarının ayırıcı tanısı"
            ),
            make_active_recall(
                "Lohusalıkta doğumdan sonraki ilk 10 günde görülen, hormonal çekilmeye bağlı hafif ağlama ve duygusallıkla seyredip 2 haftada kendiliğinden düzelen fizyolojik tabloya ne ad verilir?",
                "Annelik Hüznü (Baby Blues / Postpartum Blues) adı verilir.",
                "Kendiliğinden geçen hafif lohusalık duygusal dalgalanması"
            )
        ]
    })

    # Slayt 63: Sağlık Bakanlığı Lohusa İzlem Takvimi: Toplam 3 İzlem
    slides.append({
        "id": "k1-23-s63",
        "title": "Sağlık Bakanlığı Lohusa İzlem Takvimi: Toplam 3 İzlem",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 63,
        "narrative": (
            "Sağlık Bakanlığı Doğum Sonu Bakım Yönetim Rehberi'ne göre, komplikasyonsuz doğum yapan her lohusa için "
            "asgari standart **TOPLAM 3 KEZ İZLEM YAPILMASIDIR**: "
            "1. **1. Lohusa İzlemi:** Doğumun yapıldığı sağlık kuruluşunda, **doğumun ertesi günü (taburcu olmadan hemen önce / ilk 24 saatte)** yapılır. "
            "Uterus sertliği, vital bulgular, vajinal kanama miktarı, idrar yapma ve emzirme kontrol edilir. "
            "2. **2. Lohusa İzlemi:** Doğumdan sonraki **2 - 5. günler arasında (ideal olarak 1. haftanın sonunda)** aile sağlığı merkezinde veya ev ziyaretinde yapılır. "
            "Erken enfeksiyonlar, dikiş yerleri, sarılık ve emzirme başarısı gözden geçirilir. "
            "3. **3. Lohusa İzlemi:** Doğumdan sonraki **6. haftanın sonunda (42. günde)** puerperium biterken yapılır. "
            "Uterusun tam involüsyonu teyit edilir, rutin jinekolojik değerlendirme yapılır ve etkili aile planlaması yöntemi uygulanır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlık Bakanlığı protokolüne göre lohusalık süresince her kadına doğumun ertesi günü dahil toplam 3 kez izlem yapılır.",
                "toplam 3 kez",
                "Lohusalık boyunca yapılması zorunlu olan resmi izlem sayısı"
            ),
            make_table(
                "Sağlık Bakanlığı Lohusa İzlem Takvimi ve İçeriği",
                ["İzlem Sırası", "Uygulama Zamanı", "Uygulama Yeri", "Kritik Odak Noktası"],
                [
                    ["1. Lohusa İzlemi", "Doğumun ertesi günü (İlk 24 saat)", "Doğumun yapıldığı hastane", "Erken postpartum kanama, uterus sertliği ve ilk emzirme"],
                    [
                        "2. Lohusa İzlemi",
                        {"text": "Doğum sonrası 2 - 5. günler (1. hafta)", "isMasked": True, "hint": "Erken lohusalık enfeksiyonlarının taranacağı ilk hafta viziti"},
                        "Aile Sağlığı Merkezi / Ev ziyareti",
                        "Epizyotomi yarası, loşi kokusu, mastit ve bebek sarılığı"
                    ],
                    ["3. Lohusa İzlemi", "6. haftanın sonu (42. gün)", "Aile Sağlığı Merkezi", "Tam involüsyon kontrolü ve aile planlaması yöntemi"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı Doğum Sonu Bakım protokollerine göre komplikasyonsuz bir lohusalık süreci boyunca bir kadına toplam kaç kez resmi izlem yapılması gereklidir?",
                {
                    "A": "Yalnızca 1 kez (doğum masasında)",
                    "B": "Toplam 3 kez",
                    "C": "Toplam 6 kez",
                    "D": "Her gün bir kez olmak üzere 42 kez",
                    "E": "Hiç izlem gerekmez"
                },
                "B",
                {
                    "A": "Yanlıştır; Yetersizdir, komplikasyonlar atlanır.",
                    "B": "Doğrudur; Doğumun ertesi günü (1) + lohusalık boyunca iki kez (2-5. gün ve 42. gün) olmak üzere toplam 3 kez izlem yapılır.",
                    "C": "Yanlıştır; Gebe izlemiyle karıştırılmamalıdır.",
                    "D": "Uygulanamaz derecede fazladır.",
                    "E": "Yanlıştır; Lohusa izlemi zorunlu performans kriteridir."
                }
            )
        ]
    })

    # Slayt 64: DSÖ İlk 24 Saat Kuralı ve Erken Postpartum Bakımın Önemi
    slides.append({
        "id": "k1-23-s64",
        "title": "DSÖ İlk 24 Saat Kuralı ve Erken Postpartum Bakımın Önemi",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 64,
        "narrative": (
            "Dünya Sağlık Örgütü (DSÖ) ve küresel maternal sağlık kılavuzları, doğum sonrası ilk saatleri **'Altın 24 Saat'** olarak adlandırır: "
            "1. **Mortalite Konsantrasyonu:** Anne ve yenidoğan ölümlerinin **%50'sinden fazlası doğumdan sonraki ilk 24 saat içinde gerçekleşir**. "
            "En ölümcül tablo olan primer postpartum atoni kanaması ilk 4 saatte; yenidoğan asfiksisi ve hipotermisi ilk saatlerde gelişir. "
            "2. **DSÖ Tavsiyesi:** Anne ve bebeğin doğumdan sonra sağlık kuruluşunda **en az 24 saat gözetim altında tutulması** "
            "ve eğitimli sağlık personelince vital bulgular, vajinal kanama ve idrar çıkışı açısından saatlik izlenmesi zorunludur. "
            "Türkiye'de TNSA-2018 verilerine göre ilk doğumlarda kadınların **%97'si**, sonraki doğumlarda **%90'ı** "
            "ilk 41 saat içinde doğum sonrası bakım almaktadır; bu oran uluslararası başarı standardıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Dünya Sağlık Örgütü anne ve yenidoğan ölümlerinin yarısından fazlasının ilk yirmi dört saatte olduğunu belirterek erken bakımı zorunlu kılar.",
                "ilk yirmi dört saatte",
                "Maternal ve neonatal ölümlerin en yoğunlaştığı ilk gün penceresi"
            ),
            make_causal_chain(
                "İlk 24 Saatte Erken Postpartum İzlem Basamakları",
                [
                    "1. İlk 2 Saat (Kurtarma Odası): Uterus sertliği, fundus masajı ve vajinal kanama 15 dakikada bir kontrol edilir.",
                    "2. İdrar Çıkışı Kontrolü: Dolu mesane uterusu yukarı itip atoni kanaması yapabileceğinden spontan idrar yapma izlenir.",
                    "3. Vital Bulgular: Nabız ve tansiyon takibiyle gizli iç kanama veya preeklampsi kontrol edilir.",
                    "4. Güvenli Taburculuk: Anne ve bebek 24 saati tamamlayıp emzirme rayına oturunca 2. izlem randevusuyla taburcu edilir."
                ]
            ),
            make_active_recall(
                "Doğum sonrası ilk 24 saat içinde lohusada dolu bir idrar torbasının (glob vezikale) hekim tarafından acilen boşaltılmasının obstetrik gerekçesi nedir?",
                "Dolu mesanenin uterusu yukarı ve yana iterek myometriumun kasılmasını engellemesi ve ölümcül atoni kanamasını tetiklemesidir.",
                "Mesane doluluğunun uterus kasılmasına mekanik engeli"
            )
        ]
    })

    # Slayt 65: Postpartum Kanama (Atonik Kanama): Tanım ve Yönetim
    slides.append({
        "id": "k1-23-s65",
        "title": "Postpartum Kanama (Atonik Kanama): Tanım ve Yönetim",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 65,
        "narrative": (
            "Postpartum Hemoraji (PPH); dünyada anne ölümlerinin en sık doğrudan obstetrik nedenidir: "
            "1. **Tanım:** Doğumdan sonraki ilk 24 saatte **vajinal doğumda >500 ml**, **sezaryen doğumda >1000 ml** kan kaybedilmesidir. "
            "2. **Etiyoloji (4T Kuralı):** "
            "- **Tonus (%80):** **Uterus Atonisi** (En sık neden! Myometrium gevşektir, tahta gibi sert olması gerekirken sünger kıvamındadır). "
            "- **Trauma (%20):** Serviks veya vajen yırtıkları, uterus rüptürü, hematomlar. "
            "- **Tissue (Doku):** Plasenta veya kotiledon retansiyonu (parça kalması). "
            "- **Thrombin:** Koagülopati (pıhtılaşma bozuklukları). "
            "3. **Acil Atoni Yönetimi:** Derhal fundusa iki elle **Bimanuel Uterus Masajı** yapılır, "
            "intravenöz geniş damar yolu açılarak **Oksitosin infüzyonu** (veya Metilergonovin/Misoprostol) yüklenir ve mesane boşaltılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Postpartum kanamaların yüzde sekseninden sorumlu olan en sık etken uterus kasının kasılamadığı uterus atonisidir.",
                "uterus atonisidir",
                "Doğum sonu miyometriyum gevşekliği ve masif kanama etkeni"
            ),
            make_table(
                "Postpartum Kanama Etiyolojisi (4T Formülü) ve Tedavisi",
                ["4T Sınıfı", "Klinik Patoloji", "Görülme Sıklığı", "İlk Yapılacak Tedavi"],
                [
                    [
                        "Tonus (Tone)",
                        {"text": "Uterus Atonisi (Miyometrium gevşekliği)", "isMasked": True, "hint": "En yaygın doğrudan postpartum kanama nedeni"},
                        "~%70 - 80 (En sık)",
                        "Bimanuel fundus masajı ve İV Oksitosin"
                    ],
                    ["Travma (Trauma)", "Vajinal ve servikal laserasyonlar", "~%15 - 20", "Spekulum muayenesi ve cerrahi sütür"],
                    ["Doku (Tissue)", "Plasenta veya zar parçası retansiyonu", "~%5 - 10", "Uterin kavitenin manuel/küretajla temizlenmesi"],
                    ["Trombin (Thrombin)", "Tüketim koagülopatisi / DİK", "< %1", "Taze donmuş plazma ve fibrinojen desteği"]
                ]
            ),
            make_micro_quiz(
                "Vajinal doğumdan 2 saat sonra pedlerinin hızla kanla dolduğu görülen ve muayenede uterusu göbek üzerinde yumuşak, gevşek sünger kıvamında palpe edilen bir lohusada ilk düşünülmesi gereken tanı hangisidir?",
                {
                    "A": "Uterus Atonisi",
                    "B": "Servikal kanser kanaması",
                    "C": "Hafif fizyolojik lochia rubra",
                    "D": "Puerperal mastit",
                    "E": "Akut apandisit perforasyonu"
                },
                "A",
                {
                    "A": "Doğrudur; Doğum sonrası yumuşak gevşek uterus ve masif kanama klasik Uterus Atonisidir.",
                    "B": "Yanlıştır; Nadirdir, akut doğum kanamasının ana nedeni değildir.",
                    "C": "Yanlıştır; Pedleri hızla dolduran kanama fizyolojik loşi olamaz.",
                    "D": "Yanlıştır; Meme enfeksiyonudur, kanama yapmaz.",
                    "E": "Yanlıştır; Akut karın tablosudur, vajinal kanama yapmaz."
                }
            )
        ]
    })

    # Slayt 66: Puerperal Enfeksiyonlar: Endometrit ve Yara Yeri Bakımı
    slides.append({
        "id": "k1-23-s66",
        "title": "Puerperal Enfeksiyonlar: Endometrit ve Yara Yeri Bakımı",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 66,
        "narrative": (
            "Lohusalık döneminde enfeksiyonlar (Puerperal Sepsis), asepsi kuralları öncesinde anne ölümlerinin bir numarasıydı: "
            "1. **Puerperal Endometrit:** Doğum sonrası uterus iç tabakasının bakteriyel enfeksiyonudur. "
            "Risk Faktörleri: Uzamış membran rüptürü (>18-24 saat), uzamış doğum eylemi, çok sayıda vajinal tuşe, "
            "sezaryen doğum (vajinal doğuma göre 10-20 kat yüksek risk) ve doğum sonu içeride plasenta parçası kalmasıdır. "
            "Klinik Triad: **Doğumdan sonraki ilk 24 saat hariç, 10 gün içinde en az 2 gün ölçülen $\\ge 38.0$ °C ateş**, "
            "uterusta palpasyonla aşırı hassasiyet ve **kötü kokulu, pürülan loşi**. "
            "Tedavi: İntravenöz geniş spektrumlu antibiyotik (Klindamisin + Gentamisin). "
            "2. **Cerrahi Yara Yeri Enfeksiyonları:** Sezaryen insizyonunda veya epizyotomi hattında kızarıklık, "
            "ödem, pürülan akıntı ve dikiş açılması (dehissens); lokal yara bakımı ve antibiyotik gerektirir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Lohusalıkta uterusta hassasiyet, kötü kokulu akıntı ve 38 derecenin üzerinde ateşle seyreden tablo puerperal endometrittir.",
                "puerperal endometrittir",
                "Lohusalık döneminde rahim iç zarı enfeksiyonu"
            ),
            make_table(
                "Puerperal Enfeksiyon Tipleri ve Klinik Belirtileri",
                ["Enfeksiyon Tipi", "Anatomik Lokalizasyon", "Karakteristik Klinik Bulgular", "Tedavi Yaklaşımı"],
                [
                    ["Puerperal Endometrit", "Uterus içi kavite", "Yüksek ateş, uterin hassasiyet ve kötü kokulu loşi", "İntravenöz geniş spektrumlu antibiyotik"],
                    [
                        "Yara Yeri Enfeksiyonu",
                        "Sezaryen veya epizyotomi hattı",
                        {"text": "İnsizyonda eritem, pürülan drenaj ve dikiş açılması", "isMasked": True, "hint": "Cerrahi kesi yerinde iltihap ve ayrılma"},
                        "Drenaj, lokal pansuman ve oral/İV antibiyotik"
                    ],
                    ["Puerperal Mastit", "Meme parankimi", "Meme kadranında ağrılı kızarık sıcak kitle", "Emzirmeye devam + anti-stafilokok antibiyotik"]
                ]
            ),
            make_active_recall(
                "Puerperal endometrit gelişimi açısından vajinal doğuma kıyasla riski 10-20 kat artıran en majör obstetrik risk faktörü nedir?",
                "Sezaryen doğum yapılmış olmasıdır.",
                "Endometrit riskini katlayan cerrahi doğum yöntemi"
            )
        ]
    })

    # Slayt 67: Gebe ve Lohusa Olmayan 15-49 Yaş Kadın İzlemi: Yılda 2 Kez
    slides.append({
        "id": "k1-23-s67",
        "title": "Gebe ve Lohusa Olmayan 15-49 Yaş Kadın İzlemi: Yılda 2 Kez",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 67,
        "narrative": (
            "Halk sağlığı anlayışında kadın yalnızca çocuk doğurduğu zaman hatırlanan bir birey değildir; "
            "doğurganlık çağındaki her kadın gebelikten bağımsız olarak korunmalıdır. "
            "Aile Hekimliği Uygulama Yönetmeliği gereğince, gebe veya lohusa olmayan **15-49 yaş arasındaki tüm kadınlar "
            "YILDA 2 KEZ periyodik sağlık izlemine tabi tutulur**: "
            "1. **Dönem Dağılımı:** "
            "- **1. İzlem Dönemi:** Her yılın **Ocak - Haziran** ayları arasında bir kez, "
            "- **2. İzlem Dönemi:** Her yılın **Temmuz - Aralık** ayları arasında bir kez yapılır. "
            "2. **Bu İzlemlerin 3 Temel Amacı Vardır:** "
            "- İstenmeyen gebelikleri önlemek için etkili aile planlaması danışmanlığı ve yöntemi sağlamak, "
            "- Gebelik planlayan kadınlara gebelik öncesi (prekonsepsiyonel) danışmanlık verip riskli gebelikleri önceden saptamak, "
            "- Başlamış gebelikleri ilk 4-6 haftada çok erken tespit ederek DÖB kapsamına erkenden sokmaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Aile hekimliğinde gebe ve lohusa olmayan 15-49 yaş kadınların periyodik izlemi yılda iki kez altı aylık dönemlerde yapılır.",
                "yılda iki kez",
                "Ocak-Haziran ve Temmuz-Aralık takvimindeki yıllık kadın kontrol frekansı"
            ),
            make_table(
                "15-49 Yaş Kadın İzleminin Dönemsel Takvimi ve Amaçları",
                ["İzlem Dönemi", "Takvim Ayları", "Temel Koruyucu Amaç"],
                [
                    ["1. İzlem", "Ocak - Haziran", "Üreme sağlığı kontrolü, erken gebelik tespiti ve aile planlaması"],
                    [
                        "2. İzlem",
                        {"text": "Temmuz - Aralık", "isMasked": True, "hint": "Yılın ikinci altı aylık kadın izlem dönemi"},
                        "Prekonsepsiyonel risk değerlendirmesi ve kanser taramaları"
                    ]
                ]
            ),
            make_micro_quiz(
                "Türkiye'de aile hekimliği mevzuatına göre gebe veya lohusa olmayan 15-49 yaş kadınların periyodik sağlık izlemleri hangi sıklıkta yapılmalıdır?",
                {
                    "A": "Ayda bir kez",
                    "B": "Yılda iki kez (Ocak-Haziran ve Temmuz-Aralık dönemlerinde birer kez)",
                    "C": "Yalnızca 5 yılda bir",
                    "D": "Yalnızca evlendikleri gün",
                    "E": "Hiç izlem yapılmaz, sadece şikayeti olunca gelinir"
                },
                "B",
                {
                    "A": "Yanlıştır; Gebe izlemi sıklığıdır.",
                    "B": "Doğrudur; Aile hekimliği yönetmeliğine göre yılda 2 kez (6 aylık periyotlarla) yapılır.",
                    "C": "Yanlıştır; Smear aralığıdır, genel izlem değildir.",
                    "D": "Yanlıştır; Evlilik öncesi taramadır.",
                    "E": "Yanlıştır; Birinci basamakta proaktif zorunlu koruyucu izlemdir."
                }
            )
        ]
    })

    # Slayt 68: 15-49 Yaş İzleminin Bileşenleri: Prekonsepsiyonel Bakım ve Kanser Taramaları
    slides.append({
        "id": "k1-23-s68",
        "title": "15-49 Yaş İzleminin Bileşenleri: Prekonsepsiyonel Bakım ve Kanser Taramaları",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 68,
        "narrative": (
            "15-49 yaş kadın izlemi çok yönlü bir koruyucu halk sağlığı paketidir: "
            "1. **Prekonsepsiyonel (Gebelik Öncesi) Bakım:** "
            "Diyabetik kadının kan şekerinin (HbA1c < %6.5) düzenlenmesi (konjenital kardiyak anomaliyi önler), "
            "hipertansif kadında teratojenik ilaçların (ACE inhibitörleri/ARB) kesilip güvenli ilaçlara geçilmesi, "
            "gebelikten en az 1 ay önce folik asit başlanması (NTD önleme) ve kızamıkçık/hepatit B bağışıklığının taranması. "
            "2. **Jinekolojik Kanser Taramaları (Ulusal KETEM Programı):** "
            "- **Serviks (Rahim Ağzı) Kanseri Taraması:** **30 - 65 yaş arasındaki tüm kadınlara her 5 yılda bir HPV-DNA ve Pap-smear** testi. "
            "- **Meme Kanseri Taraması:** 20 yaşından itibaren kendi kendine meme muayenesi eğitimi, "
            "**40 - 69 yaş arasındaki kadınlara her 2 yılda bir mamografi** çekimi. "
            "Bu taramalar aile sağlığı merkezlerinde tamamen ücretsiz yürütülür."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Ulusal kanser tarama programına göre 30-65 yaş arasındaki kadınlara her 5 yılda bir HPV-DNA ve Pap-smear testi yapılır.",
                "her 5 yılda bir",
                "Serviks kanseri taramasının ulusal periyodik aralığı"
            ),
            make_table(
                "15-49 Yaş Kadınlarda Ulusal Kanser Tarama Standartları",
                ["Kanser Tipi", "Hedef Yaş Grubu", "Tarama Yöntemi", "Tarama Sıklığı"],
                [
                    [
                        "Serviks (Rahim Ağzı) Kanseri",
                        "30 - 65 Yaş",
                        {"text": "HPV-DNA testi ve Pap-smear", "isMasked": True, "hint": "Onkojenik virüs ve servikal sitoloji ikilisi"},
                        "Her 5 yılda bir"
                    ],
                    ["Meme Kanseri", "40 - 69 Yaş", "İki yönlü Mamografi", "Her 2 yılda bir"]
                ]
            ),
            make_active_recall(
                "Diyabetik bir kadının gebe kalmadan önce prekonsepsiyonel dönemde kan şekerini regüle etmesinin doğacak bebekte önlediği en kritik majör konjenital anomali grubu nedir?",
                "Konjenital kalp anomalileri (Büyük arter transpozisyonu, VSD vb.) ve sakral agenezidir.",
                "Diyabetik embriyopati ve konjenital kalp defektleri"
            )
        ]
    })

    # Slayt 69: [TEKRAR SAYFASI - CHECKPOINT 7] Lohusa ve 15-49 Yaş Kadın İzlemleri
    slides.append({
        "id": "k1-23-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Lohusa ve 15-49 Yaş Kadın İzlemleri",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 69,
        "narrative": (
            "Bu yedinci checkpoint sayfasında, lohusa izlemi dinamiklerini ve 15-49 yaş kadın sağlığı protokollerini özetliyoruz: "
            "1. **Lohusalık (Puerperium):** Doğumdan sonraki 42 gündür (6 hafta); uterus 1000 gramdan 60 grama iner (involüsyon). "
            "2. **Loşi Sırası:** Lochia rubra (ilk 3 gün) $\\rightarrow$ lochia serosa $\\rightarrow$ lochia alba. Kötü koku endometrit alarmıdır. "
            "3. **Lohusa İzlem Sayısı:** Doğumun ertesi günü + 2 kez = TOPLAM 3 KEZ (ertesi gün, 1. hafta, 6. hafta). "
            "4. **DSÖ İlk 24 Saat Kuralı:** Maternal ölümlerin %50'den fazlası ilk 24 saatte gelişir (atoni kanaması). "
            "5. **Postpartum Kanama:** >500 ml vajinal, >1000 ml sezaryen; en sık neden Uterus Atonisidir (%80); bimanuel masaj ve oksitosin esastır. "
            "6. **15-49 Yaş Kadın İzlemi:** Gebe/lohusa olmayan kadınlar YILDA 2 KEZ (Ocak-Haziran, Temmuz-Aralık) taranır. "
            "7. **Serviks Taraması:** 30-65 yaşta her 5 yılda bir HPV-DNA/Smear; Meme taraması 40-69 yaşta 2 yılda bir mamografi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s69-1",
                "Sağlık Bakanlığı Doğum Sonu Bakım Rehberi'ne göre komplikasyonsuz bir kadına lohusalık dönemi boyunca toplam kaç kez izlem yapılır?",
                "Komplikasyonsuz lohusalık sürecinde tam 3 muayene planlanır.",
                "Hastaneden çıkış ertesi, ilk hafta bitimi ve altıncı hafta sonu",
                "Lohusa İzlem Takvimi"
            ),
            make_flashcard(
                "k1-23-fc-s69-2",
                "Lohusalıkta erken postpartum kanamanın (doğum sonu aşırı hemoraji) yüzde sekseninden sorumlu en yaygın etken nedir?",
                "Uterus atonisi tablosudur.",
                "Miyometriyumun gevşek kalarak spiral damarları kapatamaması",
                "Postpartum Patolojiler"
            ),
            make_flashcard(
                "k1-23-fc-s69-3",
                "Aile hekimliği sisteminde gebe veya lohusa olmayan 15-49 yaş kadınların periyodik sağlık izlemleri yılda kaç kez yapılır?",
                "Yılda iki kez (altı ayda bir) yapılır.",
                "Ocak-Haziran ve Temmuz-Aralık dönemlerinde birer kontrol",
                "Kadın Sağlığı İzlemi"
            )
        ],
        "interactiveElements": [
            make_table(
                "Lohusa ve Kadın İzlemleri Karşılaştırma Matrisi",
                ["Hedef Grup", "İzlem Sıklığı", "Birincil Tıbbi Amaç"],
                [
                    ["Lohusa Kadın (0 - 42 Gün)", "Toplam 3 izlem (Ertesi gün, 1. hafta, 42. gün)", "Atoni kanaması, sepsis, mastit ve depresyon tespiti"],
                    [
                        "15-49 Yaş Kadın (Gebe/Lohusa Dışı)",
                        {"text": "Yılda 2 kez (6 aylık periyotlarla)", "isMasked": True, "hint": "Ocak-Haziran ve Temmuz-Aralık dönem takvimi"},
                        "Prekonsepsiyonel hazırlık, aile planlaması ve HPV/mamografi taraması"
                    ]
                ]
            )
        ]
    })

    # Slayt 70: Bölüm Özeti: Kadın İzlemlerinden Bebek ve Çocuk İzlem Esaslarına Geçiş
    slides.append({
        "id": "k1-23-s70",
        "title": "Bölüm Özeti: Kadın İzlemlerinden Bebek ve Çocuk İzlem Esaslarına Geçiş",
        "section": "Lohusa İzlemi ve 15-49 Yaş Kadın İzlemi Standartları",
        "slideNumber": 70,
        "narrative": (
            "Lohusa izlemleri ve 15-49 yaş kadın sağlığı protokolleri, kadının gebelik öncesinden başlayıp doğum sonrasına uzanan "
            "tüm üreme döngüsünün koruyucu hekimlik zırhı altına alınmasını sağlar. "
            "Lohusalıkta ilk 24 saat takibi, atoni kanaması yönetimi, puerperal sepsis profilaksisi ve yılda 2 kez yapılan "
            "15-49 yaş izlemleri maternal mortaliteyi en aza indiren kurumsal sütunlardır. "
            "Ancak ana-çocuk sağlığı madalyonunun diğer vazgeçilmez yüzü **bebek ve çocuk izlemleridir**. "
            "Doğan her bebeğin konjenital anomalilerden taranması, ilk muayenesi, aşılama takvimi, "
            "büyüme-gelişme parametreleri (boy, kilo, baş çevresi, fontaneller) ve nöromotor basamakları periyodik takip edilmelidir. "
            "Sekizinci bölümümüzde, **'Bebek ve Çocuk İzleminin Amaçları, Yaş Dönemleri (Neonatal, Bebeklik, Okul Öncesi), "
            "İzlem Takvimi (7 Çocuk İzlemi), İlk Ziyaret Muayenesi ve GKD Taraması'** incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Birinci basamakta bebek ve çocuk izlemlerinin erişkin hasta muayenesinden en temel kavramsal ve metodolojik farkı nedir?",
                "Yalnızca hastalık anında değil, sağlıklı iken periyodik büyüme-gelişme takibi, konjenital anomali taraması ve aşılamanın yapılmasıdır.",
                "Sağlam çocuk izlemi ve büyüme takibi felsefesi"
            ),
            make_branching_logic(
                "Doğumdan 4 gün sonra evde ziyaret edilen bir lohusanın memesinde kızarıklık, gerginlik ve 38.4 °C ateş saptanıyor. Anne ağrıdan dolayı bebeği o memeden emzirmeyi kestiğini söylüyor.",
                "Aile hekiminin bu anneye vermesi gereken en doğru kanıta dayalı klinik talimat hangisidir?",
                [
                    {
                        "text": "Tanının Mastit olduğunu, kanal tıkanıklığını ve abseleşmeyi önlemek için o memeden emzirmeye sık aralıklarla ısrarla devam edilmesi gerektiğini anlatmak ve uygun antibiyotik başlamak",
                        "isCorrect": True,
                        "feedback": "Mükemmel Karar: Mastitte süt stazı çözülmelidir; emzirmeye devam etmek tedavinin en temel basamağıdır, antibiyotik bebeğe zarar vermez."
                    },
                    {
                        "text": "Memeyi bandajla sıkıca sarıp sütü tamamen kesmesini ve formül mamaya geçmesini söylemek",
                        "isCorrect": False,
                        "feedback": "Hatalı ve Tehlikeli: Süt stazı artar ve birkaç günde cerrahi drenaj gerektiren meme absesi patlar."
                    },
                    {
                        "text": "Sütü sağıp lavaboya dökmesini ve 1 ay boyunca o memeden bebeğe süt vermemesini tembihlemek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Bebek memeyi doğrudan emerek en güçlü boşalmayı sağlar; sütün atılmasına gerek yoktur."
                    }
                ]
            )
        ]
    })

    return slides
