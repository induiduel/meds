# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-16-s11",
        "title": "Hiperemi ve Konjesyona Giriş: Dokuda Kan Hacmi Artışı",
        "content": "Hem hiperemi hem de konjesyon, belirli bir doku veya organdaki kan hacminin yerel olarak artışını ifade eder:\n\n- **Ortak Payda:** Her iki durumda da damar yatağında anormal miktarda kan göllenmiştir ve etkilenen doku normalden daha fazla kan içerir.\n- **Temel Fizyopatolojik Ayrım:** İsim benzerliğine ve dokudaki kan artışına rağmen, bu iki sürecin gelişme mekanizması birbirine taban tabana zıttır.\n- **Aktif vs Pasif:** Hiperemi arteriyollerin genişlemesi sonucu dokuya giren kan akımının artmasıyla gerçekleşen **aktif** bir süreçtir; konjesyon ise venöz çıkışın engellenmesiyle kanın boşalamaması sonucu gelişen **pasif** bir süreçtir.\n- **Klinik ve Görsel Yansıma:** Hiperemik doku oksijenli kanla dolduğu için parlak kırmızı ve sıcaktır; konjesyone doku ise oksijeni tükenmiş kan biriktiği için koyu mavimsi-mor (siyanotik) ve soğuktur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Hiperemi vs Konjesyon Temel Mekanizma Ayrımı",
                "Hiperemi (Aktif Süreç)",
                "Arteriyollerin aktif genişlemesiyle dokuya giren oksijenli kan akımı artar; doku kırmızı ve sıcaktır.",
                "Konjesyon (Pasif Süreç)",
                "Venöz drenajın bozulmasıyla dokudan çıkan kan akımı engellenir; deoksihemoglobin birikir, doku siyanotiktir."
            ),
            make_cloze(
                "Dokudaki kan hacminin venöz çıkış yolunun tıkanması nedeniyle pasif olarak artmasına konjesyon denir.",
                "konjesyon",
                "Venöz göllenme ile karakterize pasif hemodinamik durum"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-16-s12",
        "title": "Hipereminin Fizyopatolojisi: Aktif Arteriyoler Dilatasyon",
        "content": "Hiperemi sürecinin temelinde arteriyel düz kasların gevşemesi ve mikrosirkülasyona girişin açılması yatar:\n\n- **Vazodilatasyon Mekanizması:** Sempatik tonusun azalması, vazodilatatör sinirlerin uyarılması veya lokal doku metabolitlerinin (nitrik oksit, adenozin, prostasiklin, laktat) etkisiyle prekapiller arterioller genişler.\n- **Açılan Kapiller Yataklar:** Normalde dinlenme halinde kapalı olan inaktif kapillerler perfüzyona katılır ve kılcal damar yatağındaki eritrosit akışı dramatik biçimde hızlanır.\n- **Oksijenasyon Düzeyi:** Dokuya gelen kan taze oksijenlenmiş eritrositlerle zengindir (oksihemoglobin bolluğu).\n- **Isı ve Renk Değişimi:** Hızlı ve bol arteriyel kan akımı deride veya organda 'rubor' (kızarıklık) ve 'calor' (sıcaklık artışı) meydana getirir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Aktif Hiperemi Gelişim Aşamaları",
                [
                    "1. Metabolik veya Enflamatuvar Uyarı: Nitrik oksit, histamin veya adenozin gibi mediyatörler salınır.",
                    "2. Arteriyoler Düz Kas Gevşemesi: Prekapiller sfinkterler gevşeyerek vasküler direnci hızla düşürür.",
                    "3. Kapiller Yatağın Açılması: Dinlenimdeki yedek kılcal damarlar yoğun taze kan akımıyla dolar.",
                    "4. Kızarıklık ve Isı Artışı: Dokuda parlak kırmızı renk ve bölgesel sıcaklık yükselmesi oluşur."
                ]
            ),
            make_quiz(
                "Hiperemi gelişen bir dokunun parlak kırmızı renkte ve sıcak olmasının biyokimyasal ve fizyolojik nedeni hangisidir?",
                [
                    {"key": "A", "text": "Dokuda deoksihemoglobin ve karbondioksit birikmesi", "isCorrect": False, "explanation": "Deoksihemoglobin mor-mavi renk ve soğukluk yapar (konjesyon)."},
                    {"key": "B", "text": "Arteriyollerin genişlemesiyle dokuya gelen oksijenli kan (oksihemoglobin) miktarının ve hızının artması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Arteriyel dilatasyonla dokuya bol miktarda parlak kırmızı oksihemoglobin taşınır ve sıcaklık yükselir."},
                    {"key": "C", "text": "Venöz kapakçıkların tamamen kapanarak kanı hapsetmesi", "isCorrect": False, "explanation": "Bu durum pasif konjesyona neden olur."},
                    {"key": "D", "text": "Lenf kanallarının aşırı protein üretmesi", "isCorrect": False, "explanation": "Lenfatikler protein üretmez, interstisyumu drene eder."}
                ]
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-16-s13",
        "title": "Hiperemi Örnekleri: Egzersiz Fizyolojisinden Akut Enflamasyona",
        "content": "Hiperemi fizyolojik durumlarda homeostazı desteklerken, patolojik durumlarda akut enflamasyonun kardinal bulgusudur:\n\n- **1. Fizyolojik Hiperemi (Fonksiyonel / Egzersiz):**\n  - Yoğun egzersiz yapan bir iskelet kasında veya yemek sonrası sindirim kanalında metabolik ihtiyaç katlanarak artar.\n  - Artan adenozin, CO2, H+ ve NO konsantrasyonu kas arteriyollerini genişletir; kan akımı dinlenme düzeyinin 20-30 katına çıkabilir.\n  - Yanakların utanma veya sıcak ortamda kızarması da sempatik inhibisyona bağlı fizyolojik hiperemidir.\n- **2. Patolojik Hiperemi (Enflamatuvar):**\n  - Akut enflamasyon odağında mast hücrelerinden salınan histamin ve endotelden salınan NO, lokal arteriolleri belirgin biçimde dilate eder.\n  - Celsus'un 4 kardinal bulgusundan **rubor** (kızarıklık) ve **calor** (sıcaklık) doğrudan bu aktif hipereminin sonucudur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Durum", "Tipi", "Tetikleyici Faktör", "Dokunun Görünümü"],
                [
                    ["Koşan bir atlette bacak kasları", "Fizyolojik hiperemi", "Kas metabolitleri (NO, laktat, adenozin)", "Kırmızı, sıcak, iyi oksijenlenmiş"],
                    ["Akut apandisitli apandiks duvarı", "Patolojik hiperemi", "Enflamatuvar mediyatörler (histamin, NO)", "Kızarık, şiş ve hiperemik damarlar"],
                    ["Güneş yanığı gelişen cilt", "Patolojik hiperemi", "UV hasarı ve vasküler histamin salınımı", "Eritematöz, parlak pembe-kırmızı"]
                ]
            ),
            make_cloze(
                "Akut enflamasyon alanında histamin ve nitrik oksit aracılığıyla gelişen aktif arteriyel genişlemeye patolojik hiperemi denir.",
                "patolojik hiperemi",
                "Enflamasyondaki kızarıklık ve sıcaklık sürecinin patolojik adı"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-16-s14",
        "title": "Konjesyonun Fizyopatolojisi: Pasif Venöz Drenaj Bozukluğu",
        "content": "Konjesyon (staz), kanın bir organdan veya dokudan venöz yolla boşaltılmasının engellenmesiyle meydana gelir:\n\n- **Mekanizma:** Dokuya arteriyel kan girişi normal olsa bile, venöz drenaj bozulduğu için venüller ve kapillerler aşırı miktarda kanla dolar ve genişler.\n- **Staz ve Akım Yavaşlaması:** Damar içinde kan akımı ileri derecede yavaşlar (staz); lümende eritrosit yığılması ve rulo formasyonu gelişir.\n- **Deoksihemoglobin Birikimi:** Yavaşlayan kan akımı nedeniyle doku hücreleri kandaki oksijenin neredeyse tamamını tüketir; kanda indirgenmiş hemoglobin (deoksihemoglobin) oranı fırlar.\n- **Siyanoz:** Bu oksijensizleşmiş koyu renkli kan birikimi nedeniyle konjesyonlu organ ve dokularda **mavi-kırmızı renk (siyanoz)** ve dokuda soğukluk gözlenir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Oksijenli Kan Akımı (Hiperemi) vs Deoksihemoglobin Göllenmesi (Konjesyon)",
                "Hiperemi Rengi",
                "Oksihemoglobin zenginliği sayesinde doku açık, parlak kırmızı ve sıcaktır.",
                "Konjesyon Rengi",
                "Deoksihemoglobin birikimi nedeniyle doku koyu mavi-kırmızı (siyanotik) ve soğuktur."
            ),
            make_quiz(
                "Konjesyon gelişen bir dokunun mavi-kırmızı renk (siyanoz) almasının temel patofizyolojik nedeni hangisidir?",
                [
                    {"key": "A", "text": "Dokuda melanin pigmentinin hızla sentezlenmesi", "isCorrect": False, "explanation": "Melanin deri rengi pigmentidir, konjesyonla ilişkisizdir."},
                    {"key": "B", "text": "Venöz dönüşün engellenmesi sonucu kanda deoksihemoglobin konsantrasyonunun belirgin artması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Venöz drenaj bozulunca kan durağanlaşır, doku oksijeni emer ve deoksihemoglobin birikerek siyanoza yol açar."},
                    {"key": "C", "text": "Arteriyollerin aşırı genişleyerek oksijen basıncını yükseltmesi", "isCorrect": False, "explanation": "Bu durum hiperemidir ve kırmızı renge neden olur."},
                    {"key": "D", "text": "Lenf kanallarının eritrosit fagosite etmesi", "isCorrect": False, "explanation": "Lenfatikler eritrosit fagosite etmez."},
                ]
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-16-s15",
        "title": "Sistemik Konjesyon vs Lokalize Konjesyon",
        "content": "Venöz dönüş engelinin yerleşim yerine göre konjesyon iki ana gruba ayrılır:\n\n- **1. Sistemik Konjesyon:**\n  - En sık ve en önemli nedeni **Konjestif Kalp Yetmezliği (KKY)**'dir.\n  - Sağ ventrikül yetmezliğinde: Kan tüm sistemik venöz dolaşımda (vena kava, karaciğer, alt ekstremite venleri) göllenir.\n  - Sol ventrikül yetmezliğinde: Kan pulmoner venlerde ve akciğer kapiller yatağında göllenir (akciğer konjesyonu).\n- **2. Lokalize (Bölgesel) Konjesyon:**\n  - Yalnızca belirli bir venin obstrüksiyonu veya dıştan basıya uğraması sonucu gelişir.\n  - Örnekler: Alt ekstremitede **derin ven trombozu (DVT)** sonucu bacağın şişmesi ve morarması; bağırsak volvulusu veya fıtık boğulmasında mezenterik ven basısı.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Konjesyon Tipi", "Etiyolojik Neden", "Etkilenen Vasküler Alan", "Klinik Görünüm"],
                [
                    ["Sistemik (Kardiyak)", "Konjestif Kalp Yetmezliği", "Tüm sistemik venler ve organlar", "Boyun ven dolgunluğu, hepatomegali, bacakta ödem"],
                    ["Sistemik (Pulmoner)", "Sol Ventrikül Yetmezliği", "Pulmoner kapillerler ve venler", "Akciğer konjesyonu, dispne, ortopne"],
                    ["Lokalize (Venöz Tromboz)", "Derin Ven Trombozu (DVT)", "Tek taraflı uyluk ve bacak venleri", "Tek bacakta ağrılı şişlik, morarma, sıcaklık farkı"],
                    ["Lokalize (Mekanik Boğulma)", "İnkarserasyon / Herniasyon", "Mezenter venöz pleksus", "Bağırsakta hemorajik enfarktüs riski"]
                ]
            ),
            make_cloze(
                "Sistemik venöz konjesyonun en yaygın ve klinik olarak en önemli kardiyovasküler nedeni konjestif kalp yetmezliği hastalığıdır.",
                "konjestif kalp yetmezliği",
                "Kalbin pompalama yetersizliği sonucu oluşan sistemik tablo"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-16-s16",
        "title": "Hiperemi ve Konjesyon Karşılaştırmalı Tablosu",
        "content": "Tıbbi patolojide ve kurul sınavlarında hiperemi ile konjesyon arasındaki zıtlıklar sıkça sorgulanır (Sınav Spotu):\n\n- **Süreç Dinamiği:** Hiperemi aktif bir fizyolojik/patolojik yanıttır; konjesyon pasif mekanik bir drenaj kusurudur.\n- **Etkilenen Vasküler Uç:** Hiperemi arteriyoler vazodilatasyonla başlar; konjesyon venöz obstrüksiyon veya yetmezlikle gelişir.\n- **Perfüzyon ve Oksijen:** Hiperemide doku perfüzyonu ve oksijenlenmesi artmıştır; konjesyonda ise perfüzyon yavaşlamış ve doku hipoksiktir.\n- **Renk:** Hiperemi parlak kırmızıdır; konjesyon mavi-mor (siyanotik) renktedir.\n- **Sıcaklık:** Hiperemik doku sıcak; konjesyone doku soğuktur.\n- **Uzun Dönem Akıbet:** Hiperemi doku hasarı yapmadan düzelir; kronik konjesyon ise parankim hücre ölümüne ve fibrozise yol açar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Hiperemi", "Konjesyon"],
                [
                    ["Süreç Karakteri", "Aktif süreç", "Pasif süreç"],
                    ["Mekanizma", "Arteriyoler dilatasyon, artmış giriş", "Venöz drenaj bozukluğu, engellenmiş çıkış"],
                    ["Görünüm ve Renk", "Parlak kırmızı (eritemli) ve sıcak", "Mavimsi-kırmızı (siyanotik) ve soğuk"],
                    ["Oksijenasyon", "Oksihemoglobin artışı, yüksek O2", "Deoksihemoglobin birikimi, hipoksi"],
                    ["Örnek Durum", "Egzersiz kası, akut inflamasyon", "Kalp yetmezliği, derin ven trombozu"]
                ]
            ),
            make_quiz(
                "Aşağıdaki özelliklerden hangisi konjesyonu hiperemiden kesin olarak ayıran bir bulgudur?",
                [
                    {"key": "A", "text": "Dokudaki toplam kan hacminin artmış olması", "isCorrect": False, "explanation": "Kan hacmi her ikisinde de artmıştır."},
                    {"key": "B", "text": "Arteriyollerin aktif genişlemesiyle tetiklenmesi", "isCorrect": False, "explanation": "Bu hipereminin özelliğidir."},
                    {"key": "C", "text": "Venöz dönüşün bozulması sonucu gelişen pasif bir süreç olması ve deoksihemoglobin birikmesi", "isCorrect": True, "explanation": "Doğru cevap C'dir: Konjesyon pasiftir, venöz kökenlidir ve siyanozla seyreder."},
                    {"key": "D", "text": "Dokunun parlak pembe renkte ve sıcak olması", "isCorrect": False, "explanation": "Bu hipereminin bulgusudur."}
                ]
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-16-s17",
        "title": "Kronik Konjesyonun Patolojik Sonuçları: Hipoksi ve Fibrozis",
        "content": "Konjesyon kısa sürede çözülmez ve kronikleşirse dokuda geri dönüşümsüz ağır morfolojik değişiklikler tetiklenir:\n\n- **1. Kronik Hipoksi:** Venöz kanın stazı nedeniyle dokuya yeni oksijen ve glukoz ulaşamaz. Oksijensiz kalan parankim hücreleri atrofiye uğrar veya nekroza gider.\n- **2. Parankimal Hücre Kaybı:** Özellikle oksijen hassasiyeti yüksek olan sentrilobüler hepatositler ve alveol epitel hücreleri iskemik hücre ölümüne yenik düşer.\n- **3. Sekonder Fibrozis:** Nekroze olan parankim hücrelerinin bıraktığı boşluk ve dokudaki kronik hasar fibroblastları uyarır; dokuda kollajen birikimi ve kalıcı sertleşme (endürasyon/fibrozis) gelişir.\n- **4. Organ Disfonksiyonu:** Zamanla karaciğer yetmezliği, pulmoner hipertansiyon ve solunum yetmezliği yerleşir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kronik Konjesyonda Doku Hasarı ve Skarlaşma Zinciri",
                [
                    "1. Venöz Drenaj Bozukluğu: Kan damar yatağında göllenir ve kapiller içi staz başlar.",
                    "2. Yetersiz Doku Perfüzyonu: Kılcal damarlardan dokuya oksijen ve besin iletimi durur.",
                    "3. Kronik Doku Hipoksisi: Oksijensiz kalan parankim hücrelerinde hücresel hasar ve nekroz gelişir.",
                    "4. Onarım ve Sekonder Fibrozis: Hasarlı parankimin yerini kollajen bağ dokusu alarak doku sertleşir."
                ]
            ),
            make_cloze(
                "Kronik konjesyonda yetersiz perfüzyon nedeniyle gelişen kronik hipoksi parankim hücresi kaybına ve sekonder fibrozis tablosuna yol açar.",
                "sekonder fibrozis",
                "Kronik hipoksi sonucu bağ dokusu artışı ve sertleşme"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-16-s18",
        "title": "Konjestif Odaksal Kanamalar ve Kapiller Rüptür",
        "content": "Kronik konjesyon yalnızca hipoksiye değil, mikrovasküler mekanik hasara da neden olur:\n\n- **Artmış İntravasküler Basınç:** Venöz çıkış tıkandığında geriye doğru kapiller hidrostatik basınç aşırı yükselir.\n- **Kapiller Duvar Gerilimi ve İskemik Zayıflama:** Hem kronik hipoksi endoteli zayıflatır hem de yüksek lümen içi basınç kapiller duvarı aşırı gerer.\n- **Kapiller Rüptürü:** Zayıflayan mikrodamarlar yırtılır (kapiller rüptürü) ve eritrositler interstisyuma ve doku boşluklarına sızar.\n- **Odaksal Kanamalar:** Doku içinde peteşi ve ekimoz benzeri küçük odaksal mikro-kanamalar (diapedez ve rüptür) oluşur.\n- **Hemosiderin Oluşumu:** Dokudaki eritrositler makrofajlar tarafından fagosite edilir; hemoglobin yıkılarak altın-kahverengi hemosiderin pigmentine dönüştürülür.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İntakt Konjesyone Kapiller vs Rüptüre Kapiller ve Kanama",
                "Genişlemiş İntakt Kapiller",
                "Damarlar eritrositle doludur, hidrostatik basınç yükselmiştir, henüz dokuya eritrosit kaçağı yoktur.",
                "Rüptüre Kapiller ve Kanama",
                "Basınç ve iskemiden yırtılan duvardan eritrositler dokuya dökülür; makrofajlar hemosiderin depolar."
            ),
            make_quiz(
                "Kronik konjesyona uğramış organlarda odaksal mikroskopik kanamaların meydana gelmesinin temel mekanizması hangisidir?",
                [
                    {"key": "A", "text": "Dokuda kalsiyum birikerek damarları delmesi", "isCorrect": False, "explanation": "Kalsifikasyon doğrudan kapiller yırtığı yapmaz."},
                    {"key": "B", "text": "Aşırı yükselen kapiller hidrostatik basıncın iskemik zayıflamış damar duvarını yırtması (rüptür)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Basınç artışı ve hipoksik endotel hasarı mikro-rüptürlere ve doku içi kanamalara yol açar."},
                    {"key": "C", "text": "Plazma albümininin eritrositleri parçalaması", "isCorrect": False, "explanation": "Albümin eritrositleri parçalamaz."},
                    {"key": "D", "text": "Histaminin arteriyolleri tamamen tıkaması", "isCorrect": False, "explanation": "Histamin vazodilatatördür, damarları tıkamaz."}
                ]
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-16-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Hiperemi ve Konjesyon Temelleri",
        "content": "Bu checkpointte hiperemi ve konjesyonun zıt fizyopatolojilerini ve kronik konjesyon komplikasyonlarını pekiştiriyoruz:\n\n- **Hiperemi:** Aktif arteriyoler dilatasyon; oksihemoglobin bolluğu; doku parlak kırmızı ve sıcak (egzersiz, akut enflamasyon).\n- **Konjesyon:** Pasif venöz drenaj bozukluğu; deoksihemoglobin birikimi; doku koyu mavi-kırmızı (siyanotik) ve soğuk (kalp yetmezliği, DVT).\n- **Sistemik vs Lokalize:** Kalp yetmezliği tüm vücutta sistemik konjesyon yaparken; bir venin pıhtıyla tıkanması lokal konjesyona neden olur.\n- **Kronik Konjesyon Triadı:**\n  1. Kronik hipoksi ve parankim hücre nekrozu.\n  2. Sekonder bağ dokusu artışı (fibrozis/endürasyon).\n  3. Yüksek hidrostatik basınca bağlı kapiller rüptürleri ve hemosiderin yüklü makrofaj birikimi.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Karşılaştırma Noktası", "Hiperemi", "Konjesyon"],
                [
                    ["Süreç Karakteri", "Aktif arteriyoler süreç", "Pasif venöz drenaj kusuru"],
                    ["Klinik Renk", "Parlak kırmızı (eritem)", "Mavimsi-mor (siyanoz)"],
                    ["Doku Sıcaklığı", "Belirgin sıcak (calor)", "Genellikle soğuk"],
                    ["Oksijen Durumu", "Yüksek oksihemoglobin", "Düşük O2, yüksek deoksihemoglobin"],
                    ["Kronik Hasar", "Doku hasarı bırakmaz", "Hipoksi, nekroz, fibrozis ve kanama"]
                ]
            ),
            make_chain(
                "Konjesyondan Kalıcı Parankimal Fibrozise Gidiş Basamakları",
                [
                    "1. Venöz Drenaj Engeli: Kan damar lümeninde staza uğrar.",
                    "2. İskemik Hücre Hasarı: Kronik oksijensizlik parankim hücrelerini öldürür.",
                    "3. Kapiller Mikro-Rüptür: Yüksek hidrostatik basınç eritrositleri dokuya saçar.",
                    "4. Fibrozis ve Hemosiderozis: Doku kollajen skarla dolar ve hemosiderin çöker."
                ]
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-16-s20",
        "title": "Bölüm Özeti: Vasküler Göllenmeden Organ Patolojilerine Geçiş",
        "content": "Bölüm 2 boyunca hiperemi ve konjesyonun temel mekanizmalarını karşılaştırdık:\n\n- **Klinik Önem:** Hiperemi akut iyileşme ve savunma yanıtının bir parçasıyken; konjesyon genellikle kardiyovasküler dekompansasyonun tehlikeli bir göstergesidir.\n- **Sonraki Adım:** Bir sonraki bölümde kronik konjesyonun organlardaki özgül morfolojik sonuçlarını — akciğerde **kalp yetmezliği hücrelerini** ve karaciğerde **muskat karaciğeri** manzarasını — inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Kronik venöz konjesyon zemininde yırtılan kapillerlerden sızan eritrositlerin makrofajlarca parçalanmasıyla oluşan altın-kahverengi pigment nedir?",
                "Hemosiderin pigmenti",
                "Demir içeren sarı-kahverengi mikroskopik doku pigmenti"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi kronik konjesyonun dokuda meydana getirdiği geri dönüşümsüz patolojik komplikasyonlardan biridir?",
                [
                    {"key": "A", "text": "Dokunun parlak pembe renge dönüp sıcaklığının sürekli artması", "isCorrect": False, "explanation": "Bu hiperemik bir bulgudur."},
                    {"key": "B", "text": "Kronik hipoksiye bağlı parankim hücresi ölümü ve sekonder doku fibrozisi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kronik staz iskemik parankim nekrozu ve sekonder fibrozise neden olur."},
                    {"key": "C", "text": "Dokudaki tüm venöz damarların tamamen yok olması", "isCorrect": False, "explanation": "Venler yok olmaz, tam aksine aşırı genişler."},
                    {"key": "D", "text": "Eritrositlerin tamamen lenfositlere dönüşmesi", "isCorrect": False, "explanation": "Eritrositler lenfosite dönüşemez."}
                ]
            )
        ]
    })

    return slides
