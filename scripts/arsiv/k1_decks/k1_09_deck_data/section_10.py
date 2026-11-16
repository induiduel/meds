"""
Akut Enflamasyon (Ders 9) - Bölüm 10: Morfolojik Kalıplar, Sonlanma Yolları ve Büyük Sentez
Slayt 91 - 100 (Checkpoint 10: Slayt 100)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "slideNumber": 91,
        "title": "Akut Enflamasyonun Morfolojik Kalıplarına Giriş",
        "subtitle": "Doku hasarının şiddetine, damar kaçağının derecesine ve etkenin doğasına göre şekillenen kalıplar",
        "badge": "Morfolojiye Giriş",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Akut enflamasyonun vasküler ve hücresel mekanizmaları evrensel olsa da, çıplak gözle (makroskopi) "
            "veya mikroskop altında görülen lezyonlar büyük farklılıklar gösterir. Bu morfolojik kalıplar "
            "üç temel faktöre bağlı olarak şekillenir:\n\n"
            "1. **Enflamasyonun Şiddeti ve Vasküler Geçirgenliğin Derecesi:** Hafif sızıntılarda seröz sıvı çıkarken, "
            "büyük yarıklardan dev fibrinojen molekülleri dökülür (fibrinöz).\n"
            "2. **Etkenin Biyolojik Doğası:** Piyojenik bakteriler (Stafilokoklar) nötrofil yığılması ve irin (pürülan) yaparken, "
            "virüsler seröz veya lenfositik yanıt doğurur.\n"
            "3. **Etkilenen Organın Anatomik Yapısı:** Seröz zarlar (plevra, perikard) fibrinöz tabakalarla kaplanırken, "
            "epitel kaplı mukozalar (mide, bağırsak) dökülerek ülser oluşturur.\n\n"
            "> Dört klasik morfolojik kalıp: **Seröz**, **Fibrinöz**, **Pürülan (Süpüratif)** ve **Ülserdir**."
        ),
        "medicalTerms": [
            {"term": "Morfolojik Kalıp", "explanation": "Enflamasyonun dokuda oluşturduğu karakteristik makroskobik ve mikroskobik lezyon desenidir."},
            {"term": "Organ Anatomisi", "explanation": "Doku mimarisinin (seröz zar, kaviteli organ, mukoza) enflamatuvar lezyonun biçimini belirlemesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun 4 ana morfolojik kalıbı: Seröz, Fibrinöz, Pürülan (süpüratif) ve Ülserdir.",
            "📌 [SINAV SPOTU] Morfolojiyi belirleyen temel faktörler geçirgenliğin derecesi, mikrobun türü ve dokunun anatomisidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dört Ana Kalıp", "desc": "Seröz, Fibrinöz, Pürülan (abse) ve Ülser.", "isKey": True},
                {"title": "Belirleyici Faktörler", "desc": "Geçirgenlik derecesi, mikrop cinsi ve organ yapısı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Morfolojik Kalıp", "Baskın Sıvı ve Hücre İçeriği", "Karakteristik Klinik / Anatomik Örnek"],
                [
                    [("Seröz Enflamasyon", False, ""), ("Hücreden fakir berrak protein sıvısı", False, ""), ("Cilt su toplaması (bül), viral perikardiyal efüzyon", True, "Mezotel veya plazma kökenli hafif eksüda")],
                    [("Fibrinöz Enflamasyon", False, ""), ("Ağsı fibrin lifleri ve pıhtı katmanları", False, ""), ("Üremik perikardit, difteri psödomembranı", True, "Vasküler yarıklardan fibrinojen sızıntısı")],
                    [("Pürülan / Süpüratif", False, ""), ("Canlı/ölü nötrofiller ve nekrotik debris (pus)", False, ""), ("Akut apandisit, piyojenik bakteriyel abse odağı", True, "Stafilokok kaynaklı sıvılaşma nekrozu")],
                    [("Ülseröz Enflamasyon", False, ""), ("Epitelyal doku kaybı ve nekrotik taban", False, ""), ("Peptik mide ülseri, diyabetik ayak ülseri", True, "Organ yüzeyinden dökülen epitel defekti")]
                ]
            ),
            make_cloze(
                "Akut enflamasyonda doku hasarının şiddetine ve damar kaçağının derecesine göre ortaya çıkan karakteristik doku desenlerine morfolojik kalıplar adı verilir.",
                "morfolojik kalıplar",
                "Seröz, fibrinöz, pürülan ve ülser formlarını kapsayan genel patoloji terimi"
            )
        ]
    })

    # Slide 92
    slides.append({
        "slideNumber": 92,
        "title": "Seröz Enflamasyon: Hücreden Fakir Berrak Sıvı Efüzyonları",
        "subtitle": "Yanık bülleri, viral veziküller ve periton/plevra/perikard seröz efüzyonları",
        "badge": "Seröz Kalıp",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "**Seröz Enflamasyon**, vasküler geçirgenlik artışının en hafif düzeyde olduğu morfolojik kalıptır.\n\n"
            "- **Özellikleri:** Damar endotel aralıkları yalnızca küçük plazma proteinlerinin (albümin) ve suyun "
            "sızmasına izin verir; büyük fibrinojen molekülleri ve hücreler damar içinde kalır.\n"
            "- Sıvı nispeten proteinden zengin ancak **hücreden son derece fakir, açık sarı, berrak ve saydamdır**.\n"
            "- Sıvının kaynağı ya damar plazması ya da seröz boşlukları döşeyen **mezotel hücrelerinin aşırı salgısıdır**.\n\n"
            "> **Klasik Örnekler:**\n"
            "1. **Cilt Vezikülleri ve Bülleri:** İkinci derece güneş yanığında veya Herpes simplex/Varicella zoster "
            "viral enfeksiyonlarında epidermisin altında veya içinde toplanan berrak su kabarcıkları.\n"
            "2. **Seröz Boşluk Efüzyonları:** Viral plörit veya erken tüberkülozda plevra boşluğunda toplanan seröz sıvı."
        ),
        "medicalTerms": [
            {"term": "Seröz Enflamasyon", "explanation": "Hücreden fakir, berrak protein sıvısının doku aralığında veya vücut boşluklarında birikmesidir."},
            {"term": "Vezikül / Bül", "explanation": "Deri katmanları arasında toplanan berrak seröz sıvının oluşturduğu küçük (<0.5 cm) veya büyük kabarcıklardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Seröz enflamasyonun sıvısı hücreden fakir ve berraktır; tipik örneği yanık bülüdür.",
            "📌 [SINAV SPOTU] Seröz sıvıda fibrinojen bulunmadığı için bekletildiğinde spontan pıhtılaşmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hafif Geçirgenlik", "desc": "Sadece su ve küçük albümin sızar, hücre ve fibrin yoktur.", "isKey": True},
                {"title": "Tipik Lezyon", "desc": "Derideki su kabarcıkları (bül) ve seröz efüzyonlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Seröz Eksüda vs Pürülan Eksüda Görünümü",
                "Seröz Eksüda",
                "Berrak açık sarı, şeffaf sıvı; mikroskopta sadece tek tük lenfosit ve mezotel hücresi izlenir, pus yoktur.",
                "Pürülan Eksüda (Pus)",
                "Bulanık, sarı-yeşil, kıvamlı; mikroskopta milyonlarca dejenere nötrofil ve erimiş doku artıkları kaynar."
            ),
            make_cloze(
                "İkinci derece güneş yanığında deride oluşan ve içi berrak, hücreden fakir sıvı ile dolu su kabarcıkları seröz enflamasyon kalıbına örnektir.",
                "seröz",
                "Hücreden fakir hafif proteinli eksüda kalıbı"
            )
        ]
    })

    # Slide 93
    slides.append({
        "slideNumber": 93,
        "title": "Fibrinöz Enflamasyon: Damar Bariyerinin Ağır Yırtılması",
        "subtitle": "Kandan sızan dev fibrinojenin polimerizasyonu ve 'tereyağlı ekmek' perikarditi",
        "badge": "Fibrinöz Kalıp",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Vasküler geçirgenlik artışı çok daha ağır olduğunda veya ortamda yoğun pıhtılaştırıcı uyaranlar varsa "
            "**Fibrinöz Enflamasyon** gelişir:\n\n"
            "- Endotel yarıkları devasa boyutlara ulaşır; plazmanın en büyük proteinlerinden biri olan **Fibrinojen** "
            "damar dışına taşar.\n"
            "- Dokuya geçen fibrinojen, doku faktörü ve trombin etkisiyle çözünmeyen yapışkan **Fibrin ağlarına** "
            "polimerize olur.\n\n"
            "> **Klasik Sahne: Fibrinöz Perikardit ve Plörit:**\n"
            "- En sık **akut romatizmal ateş, üremi (böbrek yetmezliği) veya enfarktüs sonrası (Dressler sendromu)** görülür.\n"
            "- Kalbin perikard yaprakları normal kayganlığını kaybeder; üzeri sarı-kahverengi, pürüzlü, lifli fibrin "
            "katmanlarıyla örtülür.\n"
            "- İki perikard yaprağı birbirinden ayrıldığında ortaya çıkan manzara, tereyağı sürülmüş iki ekmeğin "
            "birbirine yapıştırılıp çekilmesine benzer (**Tereyağlı Ekmek / Bread and Butter Manzarası**).\n"
            "- Stetoskopla dinlendiğinde iki kaba yaprağın birbirine sürtünmesi **Perikardiyal Frotman** sesi olarak duyulur."
        ),
        "medicalTerms": [
            {"term": "Fibrinöz Enflamasyon", "explanation": "Ağır vasküler kaçak sonucu dokuya sızan fibrinojenin fibrin liflerine polimerize olmasıyla karakterize enflamasyondur."},
            {"term": "Perikardiyal Frotman", "explanation": "Fibrin kaplı viseral ve pariyetal perikardın kalp atımıyla birbirine sürtünmesiyle duyulan deri gıcırtısı benzeri sestir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Üremik perikardit tipik FİBRİNÖZ ENFLAMASYON örneğidir ('tereyağlı ekmek' görünümü).",
            "📌 [SINAV SPOTU] Fibrinöz eksüda temizlenemezse (rezolüsyona uğramazsa) organize olarak fibröz yapışıklık ve konstriktif perikardit yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Fibrinojen Sızıntısı", "desc": "Geniş endotel yarıklarından dev proteinler çıkar.", "isKey": True},
                {"title": "Tereyağlı Ekmek", "desc": "Kalp yüzeyinde pürüzlü fibrin katmanları ve frotman sesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Patolojik Özellik", "Fibrinöz Enflamasyon Evresi", "Klinik Yansıması ve Akıbeti"],
                [
                    [("Akut Sızıntı ve Polimerizasyon", False, ""), ("Fibrinojen dokuya kaçar ve ağsı fibrine dönüşür", False, ""), ("Stetoskopla duyulan kaba perikardiyal frotman sesi", True, "İki pürüzlü seröz zarın sürtünmesi")],
                    [("Başarılı Rezolüsyon (Eriyen)", False, ""), ("Plazmin ve makrofajlar fibrini eritip temizler", False, ""), ("Zarlar tamamen normal kaygan yapısına geri döner", True, "Fibrinolitik sistemin tam temizliği")],
                    [("Organizasyon (Skarlaşan)", False, ""), ("Fibroblastlar ve yeni damarlar fibrinin içine yürür", False, ""), ("Kalıcı fibröz yapışıklık ve konstriktif perikardit", True, "Kalbin gevşemesini mekanik engelleyen skar")]
                ]
            ),
            make_cloze(
                "Kronik böbrek yetmezliği olan bir hastada üremik perikardit zemininde gelişen ve kalbin yüzeyinde tereyağlı ekmek manzarası oluşturan reaksiyon fibrinöz enflamasyon kalıbıdır.",
                "fibrinöz",
                "Fibrinojen polimerizasyonuyla karakterize pürüzlü zarsı eksüda kalıbı"
            )
        ]
    })

    # Slide 94
    slides.append({
        "slideNumber": 94,
        "title": "Pürülan (Süpüratif) Enflamasyon ve Abse Anatomisi",
        "subtitle": "Piyojenik bakteriler, devasa nötrofil göçü, likefaksiyon (sıvılaşma) nekrozu ve pus",
        "badge": "Pürülan Kalıp",
        "badgeColor": "red",
        "synthesisNarrative": (
            "**Pürülan (Süpüratif) Enflamasyon**, piyojenik (irin yapıcı) bakterilerin (Staphylococcus aureus, "
            "Streptococcus pneumoniae vb.) dokuya yerleşmesiyle tetiklenir:\n\n"
            "- Ortama dökülen devasa kemotaktik faktörler milyonlarca nötrofili hasar odağına çeker.\n"
            "- Nötrofillerin saldığı güçlü proteazlar doku mimarisini tamamen eritir; **Likefaksiyon (Sıvılaşma) Nekrozu** gelişir.\n"
            "- Erimiş parankim artıkları, canlı-ölü nötrofiller ve eksüda bir araya gelerek **Pus (İrin)** sıvısını oluşturur.\n\n"
            "> **Bir Absenin Üç Katmanlı Anatomisi:**\n"
            "Abse, doku içinde kapalı kalmış fokal bir irin koleksiyonudur:\n"
            "1. **Santral Nekrotik Çekirdek:** Canlı/ölü nötrofil kütleleri ve sıvılaşmış nekrotik parankim gölü.\n"
            "2. **Piyojenik Membran:** Nekrozun çevresinde preserved nötrofillerden ve genişlemiş damarlardan oluşan zon.\n"
            "3. **Fibröz Kapsül:** En dışta fibroblastların ve granülasyon dokusunun enfeksiyonu hapsetmek için ördüğü duvar.\n\n"
            "> İlaçlar bu fibröz kapsülü aşamadığı için apselerin altın kuralı: **'Ubi pus, ibi evacua' (Nerede irin varsa, orayı boşalt!)**."
        ),
        "medicalTerms": [
            {"term": "Abse", "explanation": "Doku yıkımı ve likefaksiyon nekrozu sonucu bir parankim içinde kapalı kalmış fokal irin (pus) koleksiyonudur."},
            {"term": "Likefaksiyon Nekrozu", "explanation": "Lökosit proteazlarının doku matriksini tamamen eriterek sıvı birikintisine dönüştürdüğü nekroz tipidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Süpüratif enflamasyon ve abse oluşumundaki temel nekroz tipi LİKEFAKSİYON (SIVILAŞMA) NEKROZUDUR.",
            "📌 [SINAV SPOTU] En sık süpüratif abse etkeni koagülaz-pozitif Staphylococcus aureus'tur.",
            "📌 [SINAV SPOTU] Apseler avasküler bir fibrin/fibröz duvarla çevrili olduğu için antibiyotikler içeri giremez; mutlaka cerrahi drenaj gerekir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Pus Oluşumu", "desc": "Nötrofiller ve enzimler dokuyu eritip likefaksiyon yapar.", "isKey": True},
                {"title": "Abse Mimarisi", "desc": "Santral irin çekirdeği + piyojenik zon + fibröz kapsül.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Bakteriyel İstiladan Abse Oluşumuna Giden Yol",
                [
                    "1. Staphylococcus aureus dokuya yerleşerek koagülaz ve toksinler salgılar",
                    "2. Yoğun kemotaksiyle bölgeye masif nötrofil ordusu yığılır",
                    "3. Nötrofil proteazları çevre bağ dokusunu ve hücreleri sindirerek sıvılaşma nekrozu yapar",
                    "4. Çevreleyen granülasyon dokusu ve fibroblastlar irini hapsetmek için dış kılıf örer ve abse oturur"
                ]
            ),
            make_active_recall(
                "Akut apse odağında doku mimarisinin tamamen kaybolarak yerini sıvı bir irin havuzuna bırakmasına yol açan temel nekroz tipi hangisidir?",
                "Likefaksiyon (sıvılaşma) nekrozudur; nötrofillerden boşalan lizozomal enzimlerin ve elastazın dokuyu sindirmesiyle oluşur."
            )
        ]
    })

    # Slide 95
    slides.append({
        "slideNumber": 95,
        "title": "Ülseröz Enflamasyon: Epitelyal Örtünün Soyulması",
        "subtitle": "Organ yüzeyinden dökülen nekrotik epitel, akut eksüda tabanı ve granülasyon yatağı",
        "badge": "Ülser Kalıbı",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "**Ülser**, bir organın deri veya mukoza yüzeyini döşeyen epitel tabakasının nekroza uğrayarak "
            "dökülmesi ve geride oyuk şeklinde bir doku kaybı (defekt) bırakmasıdır.\n\n"
            "- Yalnızca yüzey epiteli barındıran organlarda görülür: **Mide ve duodenum (peptik ülser)**, "
            "kolon (ülseratif kolit), ağız mukozası (aftöz ülser) ve alt ekstremite cildi (diyabetik / variköz ülserler).\n\n"
            "> **Aktif Bir Peptik Ülserin Mikroskobik Katmanları (Yukarıdan Aşağıya):**\n"
            "1. **En Üst Katman:** Nekrotik debris ve nötrofillerden oluşan lüminosellüler pürülan eksüda.\n"
            "2. **İkinci Katman:** Yoğun asidofilik **Fibrinoid Nekroz** tabakası.\n"
            "3. **Üçüncü Katman:** Yeni tomurcuklanan pencereli kapillerler ve fibroblastlardan zengin **Granülasyon Dokusu**.\n"
            "4. **En Alt Katman:** Tabanı döşeyen sert, kollajenden zengin fibröz **Skar Dokusu**."
        ),
        "medicalTerms": [
            {"term": "Ülser", "explanation": "İnflamatuvar nekroz sonucu epitelize bir yüzeyin soyularak bazal membranı aşan lokal doku defekti oluşturmasıdır."},
            {"term": "Erozyon", "explanation": "Ülserden farklı olarak sadece yüzey epitelinde sınırlı kalan ve bazal membranı delmeyen yüzeysel defekttir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ülser epitelin dökülmesiyle oluşan doku defektidir (peptik ülser prototiptir).",
            "📌 [SINAV SPOTU] Kronik peptik ülser tabanında 4 katman vardır: Nekrotik eksüda -> Fibrinoid nekroz -> Granülasyon dokusu -> Fibröz skar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yüzey Defekti", "desc": "Epitel soyulur, derin katmanlar açığa çıkar.", "isKey": True},
                {"title": "Dört Katman", "desc": "Nekrozdan granülasyon dokusu ve skara uzanan histopatolojik yapı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Ülser Taban Katmanı", "Histopatolojik İçeriği", "Biyolojik Fonksiyonu"],
                [
                    [("1. Yüzeyel Eksüda Zonu", False, ""), ("Nötrofiller, nekrotik hücre artıkları ve fibrin", False, ""), ("Lümene bakan en üst iltihaplı yüzey örtüsü", True, "Lüminal asit ve mikroplarla temas eden katman")],
                    [("2. Fibrinoid Nekroz Zonu", False, ""), ("Asidofilik homojenize nekrotik bağ dokusu", False, ""), ("Şiddetli akut doku yıkımının gerçekleştiği ara bölge", True, "Proteinlerin çöktüğü amorf nekroz")],
                    [("3. Granülasyon Zonu", False, ""), ("Yeni kapiller damarlar, makrofajlar ve fibroblastlar", False, ""), ("Alttan yukarıya defekti kapatmaya çalışan onarım dokusu", True, "Yara tabanını dolduran canlı vasküler yatak")],
                    [("4. Fibröz Skar Zonu", False, ""), ("Yoğun asellüler kollajen lifleri ve olgun skar", False, ""), ("Ülser tabanını sağlamlaştıran ve duvarı çeken fibröz taban", True, "Kronikleşen lezyonun sert bağ dokusu")]
                ]
            ),
            make_cloze(
                "Organın deri veya mukoza yüzeyini döşeyen epitelin nekroza uğrayarak dökülmesiyle geride kalan lokal doku defektine ülser adı verilir.",
                "ülser",
                "Mide, duodenum ve deride sık görülen epitel kaybı lezyonu"
            )
        ]
    })

    # Slide 96
    slides.append({
        "slideNumber": 96,
        "title": "Akut Enflamasyonun Üç Nihai Akıbeti (Outcomes)",
        "subtitle": "1. Tam Rezolüsyon, 2. Skarlaşma/Fibrozis, 3. Kronik Enflamasyona İlerleme",
        "badge": "Akıbet Yolları",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Akut enflamasyon başladıktan sonra sonsuza kadar devam edemez; süreç zorunlu olarak **üç sonlanma "
            "yolundan (outcomes)** birine evrilir:\n\n"
            "1. **Tam İyileşme (Rezolüsyon):** İdeal sonuçtur. Zararlı etken tamamen yok edilir, vasküler geçirgenlik "
            "normale döner, eksüda ve ölü nötrofiller makrofajlarca temizlenir. Parankim hücreleri mitozla yenilenerek "
            "doku eski kusursuz anatomik mimarisine kavuşur (örneğin lobar pnömoni sonrası akciğerin tamamen temizlenmesi).\n\n"
            "2. **Skarlaşma ve Fibrozis (Bağ Dokusu ile İyileşme):** Eğer doku hasarı çok büyükse, parankim hücreleri "
            "bölünemeyen kalıcı hücrelerdense (kalp kası, nöron) veya doku iskeleti çökmüşse; defekt parankimle değil "
            "**kollajen bağ dokusu (skar)** ile doldurulur (örneğin miyokard enfarktüsü veya abse iyileşmesi).\n\n"
            "3. **Kronik Enflamasyona İlerleme:** Etken temizlenemezse (tüberküloz, yabancı cisim, otoimmünite); akut "
            "yanıt kronik enflamasyona dönüşür."
        ),
        "medicalTerms": [
            {"term": "Rezolüsyon", "explanation": "Doku hasarının tamamen gerileyerek organın fonksiyonel ve anatomik olarak eski orijinal haline dönmesidir."},
            {"term": "Skar (Sikatris)", "explanation": "Harabiyete uğrayan parankimin yerine fibroblastlar tarafından üretilen yoğun kollajenöz bağ dokusudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun 3 sonucu: 1) Tam rezolüsyon, 2) Skar/Fibrozis, 3) Kronik enflamasyondur.",
            "📌 [SINAV SPOTU] Dokunun mimari çatısı (stroma) sağlamsa rezolüsyon, çatı çökmüşse skar gelişir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. Rezolüsyon", "desc": "Etken yok edilir, doku sıfır hasarla orijinaline döner.", "isKey": True},
                {"title": "2. Skar/Fibrozis", "desc": "Ağır yıkım kollajen yamayla tamir edilir.", "isKey": True},
                {"title": "3. Kronikleşme", "desc": "Etken dirençliyse mononükleer yangıya dönüşür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Sonlanma Yolu", "Gelişmesi İçin Gerekli Doku Koşulu", "Tipik Klinik Senaryo"],
                [
                    [("1. Tam Rezolüsyon", False, ""), ("Hasar sınırlıdır, doku iskeleti korunmuştur, parankim rejenere olur", False, ""), ("Pnömokoksik lobar pnömoni sonrası akciğerin temizlenmesi", True, "Eksüdanın rezorbe olup alveollerin açılması")],
                    [("2. Skarlaşma / Fibrozis", False, ""), ("Geniş doku yıkımı, likefaksiyon veya bölünmeyen hücre nekrozu", False, ""), ("Doku apsesi veya miyokard enfarktüsü sonrası fibrozis", True, "Kollajen birikimiyle organın tamir edilmesi")],
                    [("3. Kronik Enflamasyon", False, ""), ("Zararlı etken temizlenemez, fagositoza dirençli mikrop kalır", False, ""), ("Akut viral hepatitin kronik aktif hepatite ilerlemesi", True, "Aylarca süren makrofaj/lenfosit yangısı")]
                ]
            ),
            make_cloze(
                "Akut enflamasyon odağında zararlı etkenin başarıyla temizlenmesi ve dokunun hiçbir iz kalmadan orijinal anatomik yapısına dönmesi sürecine rezolüsyon adı verilir.",
                "rezolüsyon",
                "Enflamasyonun tam ve kusursuz iyileşme ile sonlanmasını ifade eden kavram"
            )
        ]
    })

    # Slide 97
    slides.append({
        "slideNumber": 97,
        "title": "Rezolüsyonun Aktif Moleküler Frenleri: Yangıyı Söndürmek",
        "subtitle": "Lipoksinler, Rezolvinler, Protektinler, Nötrofil Apoptozu ve Eferositoz",
        "badge": "Yangı Frenleri",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Eski tıp kitaplarında enflamasyonun sönmesi 'pasif bir tükenme' sanılırdı. Bugün biliyoruz ki rezolüsyon, "
            "genetik olarak programlanmış son derece **aktif bir moleküler frenleme operasyonudur**:\n\n"
            "1. **Lipid Aracılı Sınıf Değişimi (Class Switch):**\n"
            "- Yangı ilerledikçe nötrofiller ve trombositler arakidonik asit yolağını pro-enflamatuvar lökotrienlerden "
            "anti-enflamatuvar **Lipoksinlere (LXA4, LXB4)** çevirir.\n"
            "- Omega-3 yağ asitlerinden (EPA, DHA) **Rezolvinler, Protektinler ve Maresinler** sentezlenir. "
            "Bu moleküller nötrofil göçünü bıçak gibi keser.\n\n"
            "2. **Nötrofil Apoptozu ve Eferositoz:**\n"
            "- Ömrü biten nötrofiller apoptoza gider; plazma zarlarında **Fosfatidilserin** dışa döner ('Beni ye!' sinyali).\n"
            "- Doku makrofajları apoptotik nötrofilleri sessizce yutar; bu temizliğe **Eferositoz** denir.\n"
            "- Apoptotik nötrofili yutan makrofaj, anında fenotip değiştirerek **IL-10 ve TGF-β** (anti-enflamatuvar) salgılar."
        ),
        "medicalTerms": [
            {"term": "Eferositoz", "explanation": "Makrofajların apoptotik hücreleri çevreye sitokin saçmadan sessizce fagosite edip temizlemesi olayıdır."},
            {"term": "Fosfatidilserin", "explanation": "Normalde hücre zarının iç yüzünde duran, apoptozda dışa dönerek makrofajlara 'beni ye' sinyali veren fosfolipittir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Rezolüsyon pasif değil, lipoksinler ve rezolvinlerle yürütülen AKTİF bir programdır.",
            "📌 [SINAV SPOTU] Apoptotik nötrofilleri temizleyen makrofajlar IL-10 ve TGF-beta salgılayarak yangıyı bitirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lipid Değişimi", "desc": "Lökotrienler durur, lipoksin ve rezolvinler yangıyı keser.", "isKey": True},
                {"title": "Eferositoz", "desc": "Apoptotik nötrofiller sessizce yutulup IL-10 salgılanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Akut Yangının Başlangıcı vs Rezolüsyon Evresi",
                "Yangının Başlangıcı (Akut Faz)",
                "Lökotrien B4 ve IL-8 nötrofilleri çağırır, TNF ve IL-1 endoteli açar, doku yıkımı ve eksüda tırmanır.",
                "Rezolüsyon Evresi (Sönümlenme)",
                "Lipoksinler ve rezolvinler nötrofil göçünü durdurur, nötrofiller apoptoza gider, makrofajlar IL-10 salar."
            ),
            make_cloze(
                "Akut enflamasyonun sönümlenme fazında makrofajların apoptotik nötrofilleri dokudan sessizce temizlemesi sürecine eferositoz adı verilir.",
                "eferositoz",
                "Apoptotik hücre kalıntılarının fagositozla ortadan kaldırılması olayı"
            )
        ]
    })

    # Slide 98
    slides.append({
        "slideNumber": 98,
        "title": "Organizasyon ve Skarlaşma: Granülasyon Dokusundan Fibröz Sikatrise",
        "subtitle": "Fibrin eksüdasının içine yürüyen yeni damarlar, fibroblastlar ve tip I kollajen çatısı",
        "badge": "Onarım Patolojisi",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "Eğer dokudaki eksüda (özellikle fibrin veya irin) makrofajlar ve lenfatiklerce hızla temizlenemezse, "
            "vücut bu ölü alanı boş bırakmaz; içerisine yeni doku yürütür: Bu olaya **Organizasyon** denir.\n\n"
            "Organizasyonun Evreleri:\n"
            "1. **Granülasyon Dokusu İstilası:** Hasardan 3-5 gün sonra, sağlam çevre dokudan VEGF etkisiyle "
            "yeni tomurcuklanan narin kapillerler (anjiyogenez) ve aktive fibroblastlar fibrin eksüdasının içine doğru göç eder.\n"
            "2. **Kollajen Depolanması:** Fibroblastlar ortama önce gevşek Tip III kollajen, ardından sağlam **Tip I kollajen** örer.\n"
            "3. **Skar Olgunlaşması (Sikatrizasyon):** Zamanla damarlar geriler, hücreler azalır; lezyon soluk, kansız, "
            "asellüler ve taş gibi sert bir **Kollajen Skara (Fibrozis)** dönüşür.\n\n"
            "> **Klinik Bedel:** Skar dokusu defekti kapatır ama orijinal organ fonksiyonunu göremez; kalpte ileti blokları "
            "veya pompa yetmezliğine, karında ise bağırsakları birbirine yapıştıran **fibröz adezyonlara (ileus)** yol açar."
        ),
        "medicalTerms": [
            {"term": "Organizasyon", "explanation": "Temizlenemeyen nekrotik alanın veya fibrin eksüdasının içine granülasyon dokusu ve fibroblastların girerek skara dönüştürmesidir."},
            {"term": "Granülasyon Dokusu", "explanation": "Yeni oluşan narin damarlar (anjiyogenez), fibroblastlar ve makrofajlardan oluşan pembe, granüllü geçici onarım dokusudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Organizasyon = Fibrin/nekroz alanının granülasyon dokusu ve ardından fibröz skarla yer değiştirmesidir.",
            "📌 [SINAV SPOTU] Granülasyon dokusunda önce Tip III kollajen üretilir, olgun skarda ise Tip I kollajen hakimdir.",
            "📌 [SINAV SPOTU] Karın cerrahisi sonrası gelişen mekanik ileusun en sık nedeni organize olan fibröz adezyonlardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Granülasyon İstilası", "desc": "Damarlar ve fibroblastlar fibrin içine yürür.", "isKey": True},
                {"title": "Kollajen Skar", "desc": "Tip I kollajen ile sert, asellüler kalıcı yama oluşur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Eksüdanın Skara Dönüşüm (Organizasyon) Zinciri",
                [
                    "1. Dokuda temizlenemeyen yoğun fibrinöz veya pürülan eksüda birikintisi kalır",
                    "2. VEGF ve bFGF etkisiyle çevre sağlam dokudan granülasyon damarları eksüdanın içine yürür",
                    "3. Fibroblastlar bölgeye göç ederek hücreler arasına bol miktarda Tip III ve Tip I kollajen örer",
                    "4. Kapiller damarlar geriler ve doku büzüşerek sert fibröz skar (organizasyon) dokusuna dönüşür"
                ]
            ),
            make_active_recall(
                "Akut perikardit veya apandisit sonrasında karın içinde veya perikard yaprakları arasında gelişen kalıcı yapışıklıkların (adezyon) patofizyolojik mekanizması nedir?",
                "Yüzeyde biriken zengin fibrinöz eksüdanın plazmin ile eritilip temizlenememesi (rezolüsyona uğrayamaması), içerisine granülasyon dokusu ve fibroblastların girerek fibröz skar dokusuna dönüştürmesidir (organizasyon)."
            )
        ]
    })

    # Slide 99
    slides.append({
        "slideNumber": 99,
        "title": "Akut Enflamasyonun Büyük Entegrasyon Matrisi",
        "subtitle": "Tüm vasküler, hücresel ve kimyasal mekanizmaların tek bir panoramik tabloda birleşimi",
        "badge": "Büyük Matris",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Akut enflamasyonun tüm aktörlerini tek bir panoramik sahnede birleştirdiğimizde kusursuz bir biyolojik "
            "senfoni görürüz:\n\n"
            "- **Vasküler Sahne:** Prekapiller arteriyol genişler (NO/Histamin), kapiller yatak kanla dolar (aktif hiperemi), "
            "venül endotelleri kasılır (histamin/lökotrien), eksüda dokuya boşalır, kan akımı duraklar (staz).\n\n"
            "- **Hücresel Sahne:** Staz nötrofili çepere iter (marginasyon), selektinler yuvarlar (rolling), kemokinler "
            "integrinleri açar, ICAM-1 kilitler (sıkı adezyon), PECAM-1 diapedez yaptırır, kollajenaz bazal membranı deler, "
            "C5a/IL-8 kemotaksisi ile nötrofil bakteriye koşar.\n\n"
            "- **İmha Sahnesi:** IgG ve C3b mikrobu opsonize eder, psödopodlar yutar (fagozom), NADPH oksidaz süperoksit "
            "patlatır, MPO çamaşır suyu (HOCl) sıkar; büyük mikroplara karşı NETosis ile DNA tuzakları fırlatılır.\n\n"
            "- **Sonlanma Sahnesi:** Lipoksinler yangıyı keser, nötrofiller ölür, makrofajlar eferositozla enkazı temizler "
            "ve doku ya tam rejenere olur (rezolüsyon) ya da fibrozisle kapatılır (skar)."
        ),
        "medicalTerms": [
            {"term": "Entegrasyon", "explanation": "Vasküler, hücresel ve moleküler süreçlerin birbiriyle olan zamansal ve mekansal uyumudur."},
            {"term": "Senfoni Modeli", "explanation": "Her mediyatörün ve hücrenin sırası geldiğinde devreye girip görevini yaptıktan sonra yerini bir sonrakine devretmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyon kronolojik akış: Vazodilatasyon -> Geçirgenlik -> Marginasyon -> Rolling -> Adezyon -> Diapedez -> Kemotaksi -> Fagositoz -> Rezolüsyondur.",
            "📌 [SINAV SPOTU] Sürecin hiçbir adımı rastgele değildir; moleküler kilit-anahtar sistemleriyle yönetilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Vasküler Akış", "desc": "Genişle -> Sızdır -> Yavaşla -> Lökositi yanaştır.", "isKey": True},
                {"title": "Hücresel Akış", "desc": "Yuvarlan -> Tutun -> Duvarı Del -> Hedefe Koş -> Parçala.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Enflamatuvar Faz", "Başroldeki Temel Moleküller", "Klinik / Morfolojik Yansıması"],
                [
                    [("Vasküler Faz", False, ""), ("Histamin, Nitrik Oksit, Lökotrienler", False, ""), ("Rubor (kızarıklık), Calor (sıcaklık) ve Tumor (ödem eksüdası)", True, "Damar genişlemesi ve geçirgenlik artışı")],
                    [("Hücresel Göç Fazı", False, ""), ("Selektinler, İntegrinler, ICAM-1, PECAM-1", False, ""), ("Kanda nötrofili ve dokuda masif lökosit infiltrasyonu", True, "Lökositlerin damardan dokuya geçişi")],
                    [("Kemotaksi ve İmha", False, ""), ("C5a, LTB4, IL-8, NADPH Oksidaz, MPO", False, ""), ("Fagositoz, süpüratif irin (pus) ve bakteri lizisi", True, "Mikrobisidal kaskadın çalışması")],
                    [("Rezolüsyon ve Onarım", False, ""), ("Lipoksinler, Rezolvinler, IL-10, TGF-β, VEGF", False, ""), ("Yangının sönmesi, nekroz temizliği ve fibröz skar", True, "Doku onarımının tamamlanması")]
                ]
            ),
            make_cloze(
                "Akut enflamasyonun vasküler, hücresel ve öldürme basamaklarının başarıyla tamamlanmasının ardından yangıyı aktif olarak sonlandıran koruyucu mediyatörlere lipoksinler ve rezolvinler adı verilir.",
                "rezolvinler",
                "Omega-3 yağ asitlerinden sentezlenen ve yangıyı söndüren özel molekül ailesi"
            )
        ]
    })

    # Slide 100 (CHECKPOINT 10 & MASTER SENTEZ)
    slides.append({
        "slideNumber": 100,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Akut Enflamasyonun Büyük Sentezi ve Master Özeti",
        "subtitle": "Bölüm 10 Morfolojik Kalıplar, Abse Mimarisi, Rezolüsyon ve Ders 9 Master Sentezi",
        "badge": "Master Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Tebrikler! Ders 9 Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar destesini başarıyla tamamladınız. "
            "Bu son checkpoint'te tüm dersin en kritik 10 sınav spotunu mühürlüyoruz:\n\n"
            "1. **Enflamasyon Tanımı:** Vaskülarize dokuların savunma yanıtıdır. Damarsız dokularda primer olarak başlayamaz.\n"
            "2. **5 Kardinal Belirti:** Rubor/Calor (vazodilatasyon), Tumor (geçirgenlik/eksüda), Dolor (bradikinin/PGE2), Functio Laesa (Virchow).\n"
            "3. **Tehlike Algısı:** PAMPs (LPS/TLR4) ve DAMPs (ürik asit/NLRP3). İnflamazom Kaspaz-1'i aktive eder, Gasdermin D ile piroptozis yapar.\n"
            "4. **Vasküler Olaylar:** Geçici vazokonstriksiyon -> Arteriyoler vazodilatasyon (NO/Histamin) -> Staz ve Marginasyon.\n"
            "5. **Geçirgenlik Mekanizmaları:** En sık Endotel Kasılması (venüller, histamin, 15-30 dk). Yanıkta Doğrudan Hasar (tüm yatak). ARDS'de Lökosit Hasarı.\n"
            "6. **Transüda vs Eksüda:** Transüda (dansite <1.012, protein <3 g/dL). Eksüda (dansite >1.020, protein >3 g/dL, lökosit ve fibrin zengini).\n"
            "7. **Lökosit Göçü:** Yuvarlanma = Selektinler (Sialyl-Lewis X). Sıkı Adezyon = İntegrinler (LFA-1/ICAM-1). Diapedez = PECAM-1 (CD31).\n"
            "8. **Genetik Bozukluklar:** LAD-1 = CD18 (sıkı adezyon bozuk, irinsiz yara). LAD-2 = Sialyl-Lewis X (yuvarlanma bozuk, Bombay). Chédiak-Higashi = LYST (kemotaksi bozuk, dev granüller, albinizm).\n"
            "9. **Fagositoz ve Öldürme:** Opsoninler = IgG ve C3b. Solunumsal patlama = NADPH Oksidaz ($O_2^{\\bullet -}$) -> MPO (HOCl). CGD = NADPH oksidaz mutasyonu (DHR/NBT negatif, katalaz pozitif mikroplarla apse).\n"
            "10. **Morfoloji ve Akıbet:** Seröz (bül), Fibrinöz (üremik perikardit), Pürülan (abse/likefaksiyon), Ülser (epitel kaybı). Akıbet: Rezolüsyon (lipoksin/IL-10), Skar (organizasyon) veya Kronikleşme."
        ),
        "medicalTerms": [
            {"term": "Akut Enflamasyon", "explanation": "Damarlı dokuların lökosit ve plazma proteinlerini dokuya geçirerek hasara karşı verdiği hızlı, kalıpsal savunma reaksiyonudur."},
            {"term": "Master Entegrasyon", "explanation": "Vasküler hemodinami, hücresel göç ve mikrobisidal biyokimyanın bir bütün halinde klinik hastalıklara uyarlanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun temel hücresi nötrofil, temel öldürücü ajanı HOCl'dir.",
            "📌 [SINAV SPOTU] Yuvarlanmayı selektinler, adezyonu integrinler, diapedezi PECAM-1 yönetir.",
            "📌 [SINAV SPOTU] LAD-1'de CD18, LAD-2'de Sialyl-Lewis X, Chédiak-Higashi'de LYST, CGD'de NADPH oksidaz defektiftir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemodinami ve Göç", "desc": "Vazodilatasyon -> Geçirgenlik -> Selektin -> İntegrin -> PECAM-1.", "isKey": True},
                {"title": "Öldürme ve Sonlanma", "desc": "Opsonizasyon -> Fagositoz -> HOCl -> Rezolüsyon veya Skar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Tıp fakültesi 3. sınıf patoloji stajında akut enflamasyon olgusunu değerlendiren bir hekim adayı olarak, hasarlı dokudaki sürecin kronikleşmeden tam bir doku onarımına (rezolüsyona) ulaşabilmesi için en kritik şartın ne olduğunu söylersiniz?",
                [
                    {"text": "Zararlı etkenin hızla nötralize edilmesi, doku mimari çatısının (stroma) korunmuş olması ve nötrofil apoptozunu takiben makrofajların devreye girmesi", "isCorrect": True, "feedback": "Kusursuz tıp vizyonu! Tam rezolüsyon etkenin yok edilmesine, doku iskeletinin sağlamlığına ve aktif anti-enflamatuvar sinyallere bağlıdır."},
                    {"text": "Nötrofillerin dokudan hiç ayrılmayarak haftalarca ortama elastaz salgılaması", "isCorrect": False, "feedback": "Bu durum doku nekrozuna ve kronik apselere yol açar."},
                    {"text": "Damarların kalıcı olarak vazokonstriksiyonda kalması ve dokunun kansız bırakılması", "isCorrect": False, "feedback": "İskemi infarkt ve gangrene neden olur."}
                ]
            ),
            make_active_recall(
                "Akut enflamasyon konusunda bir patoloğun asla unutmaması gereken üç kardinal moleküler kuralı belirtiniz?",
                "1) Vasküler geçirgenlik artışı olmaksızın eksüda ve lökosit göçü olamaz; 2) Lökosit ekstravazasyonu sırasıyla selektinler (yuvarlanma), integrinler (sıkı adezyon) ve PECAM-1 (diapedez) üzerinden yürütülür; 3) Oksijene bağımlı intrasellüler öldürmenin nihai ve en güçlü silahı MPO tarafından üretilen Hipokloröz Asittir (HOCl)."
            ),
            make_cloze(
                "Akut enflamasyonun tüm vasküler ve hücresel mekanizmalarının nihai hedefi zararlı etkeni ortadan kaldırarak dokunun tam fonksiyonel iyileşmesini yani rezolüsyon durumunu sağlamaktır.",
                "rezolüsyon",
                "Enflamasyonun doku hasarı bırakmadan tam iyileşmeyle sonlanması durumu"
            )
        ]
    })

    return slides
