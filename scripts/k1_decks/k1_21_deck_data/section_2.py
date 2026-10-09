# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 2: Aselüler Etkenler: Prionlar ve Virüsler (Slayt 11 - 20)
Checkpoint 2: Slayt 19
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # Slayt 11: Aselüler Mikroorganizmaların Genel Yapısı
    slides.append({
        "id": "k1-21-s11",
        "title": "Aselüler Enfeksiyon Ajanları: Hücresiz Dünyanın Biyolojisi",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 11,
        "narrative": (
            "Biyolojik sınıflamada hücresel yapı göstermeyen, sitoplazması, hücre zarı veya organelleri "
            "bulunmayan enfeksiyon ajanlarına **aselüler etkenler** denir. "
            "Bu grubun tıbbi açıdan en önemli temsilcileri **virüsler** ve **prionlardır**. "
            "Aselüler ajanların en belirleyici ortak özelliği, kendi başlarına metabolik enerji (ATP) üretememeleri "
            "ve bağımsız bir protein sentez makinesine (ribozomlara) sahip olmamalarıdır. "
            "Bu nedenle hiçbir aselüler etken cansız yapay besiyerlerinde (agar, buyyon) çoğalamaz; "
            "yaşamlarını sürdürebilmek ve replike olabilmek için mutlaka duyarlı bir canlı konak hücresine "
            "bağımlıdırlar. Virüsler en azından bir nükleik asit genomu (DNA veya RNA) ve onu çevreleyen "
            "bir protein kılıf taşırken; prionlar biyolojinin bilinen tüm kurallarını yıkarak "
            "hiçbir nükleik asit içermeyen, sadece yanlış katlanmış enfeksiyöz protein moleküllerinden ibarettir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Aselüler enfeksiyon etkenleri bağımsız metabolizma ve ribozoma sahip olmadıkları için cansız besiyerinde çoğalamazlar.",
                "cansız besiyerinde",
                "Hücresiz etkenlerin üreyemediği yapay laboratuvar ortamı"
            ),
            make_before_after(
                "Aselüler Etkenler ile Prokaryotik Bakteriler Karşılaştırması",
                "Aselüler Etkenler (Prion ve Virüs)",
                [
                    "Hücresel yapı, sitoplazma ve ribozom kesinlikle yoktur",
                    "Yalnızca DNA veya RNA içerir (prionda nükleik asit dahi yoktur)",
                    "Metabolik enerji (ATP) üretemez; konak hücresine tam bağımlıdır",
                    "Yapay besiyerlerinde üremez; standart antibiyotiklere yanıtsızdır"
                ],
                "Prokaryotlar (Bakteriler)",
                [
                    "Hücresel organizasyon, sitoplazmik membran ve peptidoglikan duvar var",
                    "Aynı anda hem DNA hem RNA molekülleri içerir",
                    "Kendi enzimleriyle bağımsız metabolizma ve ATP üretimi yapabilir",
                    "Yapay cansız besiyerlerinde koloniler halinde çoğalabilir"
                ]
            ),
            make_active_recall(
                "Biyolojinin temel santral dogmasına aykırı olarak hiçbir nükleik asit (DNA veya RNA) taşımayan aselüler enfeksiyon ajanı hangisidir?",
                "Prion proteini (PrPSc) molekülüdür.",
                "Nükleik asitsiz enfeksiyöz protein parçacığı"
            )
        ]
    })

    # Slayt 12: Prionlar: Nükleik Asitsiz Enfeksiyöz Proteinler
    slides.append({
        "id": "k1-21-s12",
        "title": "Prionlar: Hatalı Katlanmış Enfeksiyöz Proteinler",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 12,
        "narrative": (
            "Prionlar (Proteinaceous infectious particles), bilinen en küçük virüslerden bile en az 100 kat daha küçük olan, "
            "yapısında **kesinlikle nükleik asit (DNA/RNA) bulunmayan** enfeksiyöz protein parçacıklarıdır. "
            "Normal memeli nöronlarının yüzeyinde fizyolojik olarak **PrPC (selüler prion proteini)** adı verilen "
            "alfa-heliks yapısından zengin, çözünür ve proteazlara duyarlı bir protein bulunur. "
            "Hastalık tablosunda ise PrPC molekülü konformasyonel bir değişim geçirerek **PrPSc (scrapie prion proteini)** "
            "formuna dönüşür. Bu patolojik formda alfa-heliksler çözülerek yerini aşırı miktarda **beta-tabakalı (beta-sheet)** "
            "yapılara bırakır. PrPSc molekülü ortamdaki normal PrPC proteinlerini de kendine benzemeye zorlayan "
            "otokatalitik bir kalıp gibi davranır. Beta-tabakalı bu patolojik proteinler hücre içinde çözünemez, "
            "proteazlar tarafından parçalanamaz ve nöronlarda birikerek vakuolizasyon, süngersi (spongiform) dejenerasyon "
            "ve amiloid plak birikimine yol açar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Normal selüler prion proteininin patolojik forma dönüşümünde alfa-heliks yapılar çözülerek zengin beta-tabakalı konformasyona dönüşür.",
                "beta-tabakalı",
                "Patolojik prion proteininin proteaz direnci sağlayan ikincil protein yapısı"
            ),
            make_causal_chain(
                "Prion Patogenezi ve Nörodejenerasyon Kaskadı",
                [
                    "1. PrPSc Girişi: Dışarıdan patolojik prion proteini alınır veya PrP geninde mutasyon olur.",
                    "2. Konformasyonel Kalıp: PrPSc normal PrPC moleküllerine bağlanarak onları beta-tabakalı forma büker.",
                    "3. Agregasyon: Proteazlara dirençli PrPSc molekülleri nöron sitoplazmasında birikir.",
                    "4. Spongiform Vakuolizasyon: Nöronlarda mikroskobik süngersi boşluklar ve nöron ölümü başlar.",
                    "5. Fatal Ensefalopati: İlerleyici demans, serebellar ataksi, miyoklonus ve ölüm gerçekleşir."
                ]
            ),
            make_micro_quiz(
                "Normal selüler prion proteini (PrPC) ile hastalık yapan patolojik prion proteini (PrPSc) arasındaki temel moleküler fark hangisidir?",
                {
                    "A": "PrPSc molekülünün devasa bir çift iplikli RNA halkası taşıması",
                    "B": "PrPSc'nin proteazlara dirençli, çözünmeyen ve yüksek oranda beta-tabakalı konformasyona sahip olması",
                    "C": "PrPSc'nin yalnızca gram-negatif bakteriler tarafından sentezlenmesi",
                    "D": "PrPC'nin hücre çekirdeğinde, PrPSc'nin ise mitokondri içinde bulunması",
                    "E": "PrPSc'nin standart otoklavlama ile saniyeler içinde tamamen denatüre olması"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; prionlarda hiçbir nükleik asit bulunmaz.",
                    "B": "B seçeneği doğrudur: PrPC alfa-heliks ağırlıklı ve çözünürken; PrPSc beta-tabaka ağırlıklı, çözünmez ve proteazlara aşırı dirençlidir.",
                    "C": "C seçeneği yanlıştır; bakteriyel bir ürün değildir.",
                    "D": "D seçeneği yanlıştır; membran glikoproteinidir.",
                    "E": "E seçeneği yanlıştır; otoklava ve ısıya son derece dirençlidir."
                }
            )
        ]
    })

    # Slayt 13: Prion Hastalıkları: Kuru ve Creutzfeldt-Jakob
    slides.append({
        "id": "k1-21-s13",
        "title": "Bulaşıcı Süngersi Ensefalopatiler: Kuru, CJD ve BSE",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 13,
        "narrative": (
            "Prionların insan ve hayvanlarda neden olduğu klinik tablolara topluca **Transmissible Spongiform Encephalopathies "
            "(Bulaşıcı Süngersi Ensefalopatiler - TSE)** adı verilir. "
            "Bu hastalıkların ortak özellikleri; aşırı uzun inkübasyon süreleri (aylar, yıllar, hatta on yıllar), "
            "sessiz başlangıç, santral sinir sistemine sınırlı kalma, hiçbir inflamatuar veya immün yanıt uyarmama "
            "ve klinik belirtiler başladıktan sonra kaçınılmaz olarak %100 fatal (ölümcül) seyretmeleridir. "
            "En önemli insan ve hayvan hastalıkları şunlardır: "
            "1. **Kuru:** Papua Yeni Gine yerlilerinde yamyamlık (ritüelistik ölü eti/beyni yeme) geleneğiyle bulaşan hastalık; "
            "inkübasyon süresi **30 yıla kadar** uzayabilir; serebellar ataksi ve kontrolsüz gülme krizleriyle seyreder. "
            "2. **Creutzfeldt-Jakob Hastalığı (CJD):** İnsanda en sık görülen TSE tablosudur. Hızlı ilerleyen demans, miyoklonus ve kortikal körlükle seyreder. "
            "3. **Varyant CJD (vCJD):** Sığırlardaki Bovine Spongiform Encephalopathy (BSE / 'Deli Dana') etkeninin kontamine sığır etiyle insanlara geçmesi sonucu gençlerde görülür. "
            "4. **Fatal Familiyal İnsomnia:** PRNP gen mutasyonu sonucu gelişen, uyuyamama ve otonomik fırtınayla giden genetik prion hastalığıdır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Papua Yeni Gine yerlilerinde ritüelistik kannibalizm ile bulaşan ve inkübasyon süresi otuz yıla kadar uzayabilen prion hastalığı Kuru hastalığıdır.",
                "Kuru",
                "Ritüelistik yamyamlık kökenli tarihi prion hastalığının adı"
            ),
            make_table(
                ["Prion Hastalığı", "Bulaş / Gelişim Yolu", "Temel Klinik Bulgular"],
                [
                    ["Kuru", "Kannibalizm (enfekte insan beyni tüketimi)", "Serebellar ataksi, titreme, kontrolsüz gülme (inkübasyon 30 yıl)"],
                    [
                        "Sporadik CJD",
                        {"text": "Spontan PrPC somatik mutasyonu", "isMasked": True, "hint": "En sık görülen insan prion formu"},
                        "Hızlı ilerleyen demans, miyoklonik sıçramalar, 1 yıl içinde ölüm"
                    ],
                    ["Varyant CJD (vCJD)", "Enfekte sığır dokusu tüketimi (Deli dana)", "Genç yaş başlangıcı, psikiyatrik semptomlar ve ataksi"],
                    ["Fatal Familiyal İnsomnia", "Otozomal dominant PRNP gen mutasyonu", "İnatçı uykusuzluk, halüsinasyonlar ve otonomik disfonksiyon"]
                ]
            ),
            make_active_recall(
                "İnsanda en sık görülen, yaşlılarda hızlı ilerleyen demans ve miyoklonik kasılmalarla seyreden prototipik prion hastalığı hangisidir?",
                "Creutzfeldt-Jakob Hastalığıdır (CJD).",
                "Hızlı demans ve miyoklonus ile seyreden süngersi ensefalopati"
            )
        ]
    })

    # Slayt 14: Prionların Olağanüstü Direnci ve İmmünojenite Yokluğu
    slides.append({
        "id": "k1-21-s14",
        "title": "Prionların Fiziksel Direnci ve İmmün Yanıt Yokluğu",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 14,
        "narrative": (
            "Prionlar enfeksiyon tıbbında sterilizasyon ve immünoloji kurallarını altüst eden iki benzersiz niteliğe sahiptir: "
            "1. **Olağanüstü Fizikokimyasal Direnç:** PrPSc molekülü kaynatmaya, standart otoklavlamaya (121°C), "
            "ultraviyole ve iyonize radyasyona, alkole, formalin fiksasyonuna ve proteaz enzimlerine (proteinaz K) karşı **tamamen dirençlidir**. "
            "Bu nedenle prion kontaminasyonu şüphesi olan cerrahi aletlerin sterilizasyonunda standart yöntemler yetersiz kalır; "
            "134°C'de en az 18 dakika basınçlı buhar otoklavı veya 1 Normal sodyum hidroksit (NaOH) solüsyonunda bekletme gibi agresif protokoller gerekir. "
            "2. **İmmün Yanıt ve İnflamasyon Yokluğu:** PrPSc proteini, konağın kendi endojen PrPC proteininin hatalı katlanmış bir izoformudur. "
            "Konak bağışıklık sistemi bu proteini yabancı (non-self) olarak algılamaz; bu nedenle prion hastalıklarında **hiçbir antikor yanıtı oluşmaz**, "
            "kanda veya BOS'ta lökosit artışı (pleositoz) izlenmez ve beyinde lenfositik inflamasyon görülmez. "
            "Görülen tek patolojik yanıt astrositoz ve nöronal vakuoler kayıptır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Prion proteini konağın kendi proteininin izoformu olduğundan prion hastalıklarında konakta hiçbir antikor yanıtı oluşmaz.",
                "antikor yanıtı",
                "Hümoral bağışıklığın prionlara karşı üretemediği savunma proteini"
            ),
            make_before_after(
                "Geleneksel Patojenler ile Prionların Direnç ve İmmünite Farkı",
                "Geleneksel Patojenler (Bakteri, Virüs)",
                [
                    "Standart otoklav (121°C), alkol veya UV ışınlarıyla inaktive edilir",
                    "Konak bağışıklığı güçlü antikor ve hücresel T yanıtı geliştirir",
                    "Enfeksiyon odağında belirgin lökositik inflamasyon (nötrofil/lenfosit) görülür",
                    "Nükleik asit hedeflenerek serolojik ve PCR yöntemleriyle saptanabilir"
                ],
                "Prionlar (PrPSc)",
                [
                    "121°C otoklav, formalin, UV ve proteazlara aşırı derecede dirençlidir",
                    "Konak 'self' algıladığı için hiçbir spesifik antikor yanıtı üretmez",
                    "Beyin dokusunda inflamatuar hücre infiltrasyonu hiç izlenmez (aseptik süngersi tablo)",
                    "Nükleik asit içermediği için PCR ile doğrudan genomik çoğaltma yapılamaz"
                ]
            ),
            make_micro_quiz(
                "Prion enfeksiyonlarında beyin omurilik sıvısında (BOS) ve serumda antikor saptanamamasının ve inflamasyon görülmemesinin temel nedeni nedir?",
                {
                    "A": "Prionların kemik iliğini tamamen tahrip ederek B lenfosit üretimini durdurması",
                    "B": "Prion proteininin konağın kendi PrPC proteininin hatalı katlanmış formu olması ve bağışıklık sistemi tarafından yabancı algılanmaması",
                    "C": "Prionların yalnızca nöron çekirdeği içinde hapsolup kana hiç geçmemesi",
                    "D": "Prionların kanda dolaşan tüm immünglobulinleri enzimatik olarak sindirmesi",
                    "E": "Prion enfeksiyonlarının yalnızca 24 saat süren akut tablolar olması"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; prionlar kemik iliğini felç etmez.",
                    "B": "B seçeneği doğrudur: PrPSc konak kökenli bir proteinin konformasyonel izoformudur; immün tolerans nedeniyle antikor veya hücresel yanıt tetiklenmez.",
                    "C": "C seçeneği yanlıştır; lenforetiküler sistemde de bulunabilirler.",
                    "D": "D seçeneği yanlıştır; prionların proteolitik sindirim yeteneği yoktur.",
                    "E": "E seçeneği yanlıştır; yıllarca süren kronik seyirli hastalıklardır."
                }
            )
        ]
    })

    # Slayt 15: Virüslerin Temel Mimarisi: Nükleokapsid ve Zarf
    slides.append({
        "id": "k1-21-s15",
        "title": "Virüslerin Temel Mimarisi: Nükleokapsid, Zarf ve Tropizm",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 15,
        "narrative": (
            "Virüsler, tek bir nükleik asit türü (ya DNA ya da RNA, asla ikisi birlikte değil) ve bu genomu "
            "çevreleyen bir protein kılıftan (**kapsid**) oluşan en küçük enfeksiyöz partiküllerdir. "
            "Genom ile kapsidin oluşturduğu komplekse **nükleokapsid** adı verilir. "
            "Yapısal mimarilerine göre virüsler iki büyük gruba ayrılır: "
            "1. **Çıplak (Zarfsız) Virüsler:** Yalnızca nükleokapsidden oluşurlar. Kapsid proteinleri çevresel etkenlere "
            "(kuruluk, asit, deterjanlar, mide asidi) son derece dirençlidir. Bu sayede fekal-oral yolla dış ortamda uzun süre canlı kalabilirler (örneğin Poliovirüs, Hepatit A, Rotavirüs). "
            "2. **Zarflı Virüsler:** Nükleokapsidin dışında konak hücre zarından türeyen lipid çift tabakalı bir **zarf (envelope)** taşırlar. "
            "Zarf üzerinde konak hücre reseptörlerine bağlanan viral glikoprotein çıkıntılar (peplomer/spike) yer alır. "
            "Zarf lipid içerdiğinden eter, alkol, deterjan ve kuruluğa karşı **son derece dayanıksızdır**; "
            "bu nedenle zarflı virüsler genellikle doğrudan temas, damlacık veya kan yoluyla bulaşır (örneğin İnfluenza, HIV, SARS-CoV-2, Herpesvirüsler)."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Virüsün genetik materyali olan nükleik asit ile onu saran protein kılıfın oluşturduğu yapısal komplekse nükleokapsid adı verilir.",
                "nükleokapsid",
                "Genom ve kapsidin oluşturduğu viral çekirdek ünitesi"
            ),
            make_table(
                ["Yapısal Özellik", "Çıplak (Zarfsız) Virüsler", "Zarflı Virüsler"],
                [
                    ["Dış Tabaka Yapısı", "Yalnızca protein kapsomerler", "Konak kaynaklı lipid çift tabaka ve glikoproteinler"],
                    [
                        "Çevresel Direnç",
                        {"text": "Mide asidine ve kuruluğa yüksek direnç", "isMasked": True, "hint": "Fekal-oral yolla bulaşabilme gücü"},
                        "Deterjan, alkol, ısı ve kuruluğa aşırı duyarlı"
                    ],
                    ["Bulaşma Yolları", "Fekal-oral yol, kontamine su ve gıdalar", "Damlacık, kan, cinsel temas, vücut sıvıları"],
                    ["Klinik Örnekler", "Poliovirüs, Rotavirüs, Norovirüs, HAV", "İnfluenza, HIV, SARS-CoV-2, HSV, HBV"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki virüs yapısal bileşenlerinden hangisinin varlığı, virüsü deterjanlara, etere ve kuruluğa karşı daha 'duyarlı' (kırılgan) hale getirir?",
                {
                    "A": "İkozahedral protein kapsid",
                    "B": "Lipid içerikli viral zarf",
                    "C": "Çift iplikli DNA genomu",
                    "D": "Ters transkriptaz enzimi",
                    "E": "Tegüment proteinleri"
                },
                "B",
                {
                    "A": "A seçeneği protein yapılıdır, deterjanlara dirençlidir.",
                    "B": "B seçeneği doğrudur: Lipid çift tabakalı zarf deterjan ve alkolle hızla çözünerek virüsün enfektivitesini yok eder.",
                    "C": "C seçeneği genetik materyaldir, zarf duyarlılığıyla doğrudan ilişkili değildir.",
                    "D": "D seçeneği polimeraz enzimidir.",
                    "E": "E seçeneği kapsid ile zarf arasındaki protein tabakasıdır."
                }
            )
        ]
    })

    # Slayt 16: Zorunlu Hücre İçi Replikasyon ve Laboratuvar Üretimi
    slides.append({
        "id": "k1-21-s16",
        "title": "Zorunlu Hücre İçi Yaşam ve Viral Replikasyon Döngüsü",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 16,
        "narrative": (
            "Virüsler **zorunlu hücre içi (obligat intrasellüler)** parazitlerdir. "
            "Bakteriler gibi ikiye bölünerek (ikili fizyon) çoğalmazlar; konak hücresinin metabolik biyosentez "
            "mekanizmalarını ele geçirerek kendi genom ve proteinlerini ayrı ayrı sentezletir ve sonra bunları "
            "bir montaj hattı gibi birleştirirler (replikasyon döngüsü). "
            "Viral yaşam döngüsü 6 temel basamaktan oluşur: "
            "1. **Tutunma (Adsorpsiyon):** Viral yüzey proteininin konak hücre yüzeyindeki spesifik reseptöre bağlanması (bu durum viral **doku tropizmini** belirler; örneğin HIV'in CD4 reseptörüne bağlanması). "
            "2. **Giriş (Penetrasyon):** Endositoz veya zarf füzyonu ile hücre içine girme. "
            "3. **Soyulma (Uncoating):** Kapsidin eriyerek nükleik asidin sitoplazmaya serbest kalması. "
            "4. **Biyosentez:** Viral mRNA transkripsiyonu, viral protein translasyonu ve genom replikasyonu. "
            "5. **Montaj (Assembly):** Yeni genomların kapsid içine paketlenmesi. "
            "6. **Salınım:** Tomurcuklanma (zarflı virüsler) veya hücre lizisi (çıplak virüsler) ile yeni virionların hücreden çıkması. "
            "Virüsler canlı hücre olmadan çoğalamadıkları için laboratuvarda ancak **hücre kültürleri**, embriyonlu tavuk yumurtası veya deney hayvanlarında üretilebilirler."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Virüsün yüzey proteinleri ile konak hücre reseptörlerinin spesifik eşleşmesi virüsün hangi dokuları enfekte edeceğini belirleyen doku tropizmini oluşturur.",
                "doku tropizmini",
                "Virüsün belirli hücre veya organlara özgüllüğünü ifade eden biyolojik terim"
            ),
            make_causal_chain(
                "Viral Replikasyon Döngüsü Basamakları",
                [
                    "1. Tutunma (Adsorpsiyon): Viral yüzey proteini konak hücre reseptörüne bağlanır.",
                    "2. Penetrasyon ve Soyulma: Virüs hücre içine girer ve protein kapsid eriyerek genom açığa çıkar.",
                    "3. Transkripsiyon ve Translasyon: Konak ribozomları viral yapısal ve enzimatik proteinleri üretir.",
                    "4. Genom Replikasyonu: Viral polimerazlar yüzlerce yeni viral DNA veya RNA kopyası çıkarır.",
                    "5. Montaj ve Salınım: Kapsit içine paketlenen yeni virionlar tomurcuklanarak veya lizisle dışarı çıkar."
                ]
            ),
            make_active_recall(
                "Virüslerin yapay cansız besiyerlerinde (kanlı agar, buyyon) üremeyip laboratuvarda çoğaltılabilmeleri için zorunlu olan biyolojik sistem nedir?",
                "Canlı hücre kültürleridir (veya embriyonlu tavuk yumurtası / deney hayvanları).",
                "Obligat intrasellüler etkenlerin üretildiği canlı laboratuvar ortamı"
            )
        ]
    })

    # Slayt 17: DNA Virüsleri
    slides.append({
        "id": "k1-21-s17",
        "title": "DNA Virüsleri Ailesi ve Temel Klinik Özellikleri",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 17,
        "narrative": (
            "Genomik materyali DNA olan virüsler, genellikle konak hücre çekirdeğinde replike olurlar "
            "(istisna: Poxvirüsler sitoplazmada replike olur). Parvovirüsler hariç tüm DNA virüsleri "
            "çift iplikli (dsDNA) genoma sahiptir. Başlıca DNA virüsü aileleri ve klinikleri şunlardır: "
            "1. **Herpesviridae (Zarflı dsDNA):** Primer enfeksiyon sonrası duyusal ganglionlarda veya lenfositlerde "
            "ömür boyu **latent (gizli)** kalabilme yeteneğindedirler. "
            "HSV-1 (oral uçuk, temporal ensefalit), HSV-2 (genital ülserler), VZV (suçiçeği ve zona), "
            "EBV (enfeksiyöz mononükleoz / öpücük hastalığı, Burkitt lenfoma), CMV (konjenital enfeksiyon, retinit) ve HHV-8 (Kaposi sarkomu). "
            "2. **Adenoviridae (Çıplak dsDNA):** Faringokonjonktival ateş, akut solunum yolu enfeksiyonları ve çocuklarda gastroenterit yapar. "
            "3. **Parvoviridae (Çıplak tek iplikli ssDNA):** İnsan patojeni olan Parvovirüs B19; çocuklarda beşinci hastalık (eritema infeksiyozum / tokatlanmış yüz), "
            "orak hücreli anemide aplastik kriz ve gebelikte hidrops fetalise yol açar. "
            "4. **Hepadnaviridae (Zarflı kısmi dsDNA):** Hepatit B virüsüdür (HBV); kronik hepatit, siroz ve hepatosellüler karsinom etkenidir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Çocuklarda tokatlanmış yüz görünümüyle seyreden beşinci hastalık tablosunun etkeni tek iplikli DNA virüsü olan Parvovirüs B19 virüsüdür.",
                "Parvovirüs B19",
                "Eritema infeksiyozum ve aplastik kriz yapan ssDNA virüsü"
            ),
            make_table(
                ["DNA Virüs Ailesi", "Zarf / Genom Yapısı", "Karakteristik Klinik Tablolar"],
                [
                    ["Herpes Simplex (HSV-1 / 2)", "Zarflı dsDNA", "Gingivostomatit, genital vezikül, temporal lob ensefaliti"],
                    [
                        "Varisella Zoster (VZV)",
                        {"text": "Zarflı dsDNA (Dorsal ganglion latensi)", "isMasked": True, "hint": "Dermatom boyunca ağrılı vezikül yapan virüs"},
                        "Primer suçiçeği ve reaktivasyonla gelişen zona"
                    ],
                    ["Parvovirüs B19", "Çıplak tek iplikli ssDNA", "Beşinci hastalık, fetal hidrops, eritroid aplastik kriz"],
                    ["Epstein-Barr Virüsü (EBV)", "Zarflı dsDNA (B lenfosit tropizmi)", "Enfeksiyöz mononükleoz, Burkitt lenfoma, nazofarenks Ca"]
                ]
            ),
            make_micro_quiz(
                "Tüm DNA virüsleri arasında istisnai olarak 'tek iplikli DNA (ssDNA)' genomu taşıyan ve çocuklarda eritema infeksiyozum yapan virüs hangisidir?",
                {
                    "A": "Sitomegalovirüs (CMV)",
                    "B": "Parvovirüs B19",
                    "C": "Hepatit B virüsü (HBV)",
                    "D": "Adenovirüs",
                    "E": "Varisella Zoster virüsü (VZV)"
                },
                "B",
                {
                    "A": "A seçeneği çift iplikli herpesvirüstür.",
                    "B": "B seçeneği doğrudur: Parvovirüs B19 insan patojeni tek iplikli DNA virüsüdür.",
                    "C": "C seçeneği kısmi çift iplikli hepadnavirüstür.",
                    "D": "D seçeneği çift iplikli zarfsız DNA virüsüdür.",
                    "E": "E seçeneği çift iplikli herpesvirüstür."
                }
            )
        ]
    })

    # Slayt 18: RNA Virüsleri
    slides.append({
        "id": "k1-21-s18",
        "title": "RNA Virüsleri Ailesi: Genetik Çeşitlilik ve Mutasyon Gücü",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 18,
        "narrative": (
            "Genetik materyali ribonükleik asit (RNA) olan virüsler, çoğunlukla konak hücresinin sitoplazmasında replike olurlar "
            "(istisnalar: İnfluenza ve Retrovirüsler nükleer evre içerir). "
            "Viral RNA polimerazların 'proofreading' (hata düzeltme) yeteneği bulunmadığından, RNA virüsleri "
            "DNA virüslerine kıyasla **çok daha yüksek mutasyon oranına ve antijenik değişkenliğe** sahiptir. "
            "Başlıca RNA virüsü grupları şunlardır: "
            "1. **Orthomyxoviridae (Zarflı, segmenter ssRNA):** İnfluenza A ve B virüsleridir; antijenik drift (küçük nokta mutasyonlar) ve "
            "antijenik shift (genomik segment değişimiyle pandemik suşlar) gösterirler. "
            "2. **Coronaviridae (Zarflı, pozitif polariteli ssRNA):** Soğuk algınlığı, SARS, MERS ve SARS-CoV-2 (COVID-19) etkenleridir. "
            "3. **Retroviridae (Zarflı diploit ssRNA):** Ters transkriptaz enzimi taşıyan HIV-1 ve HIV-2; CD4 T hücrelerini yıkarak AIDS tablosuna yol açar. "
            "4. **Rhabdoviridae (Zarflı, mermi şeklinde ssRNA):** Kuduz virüsü (Rabies); nöroinvaziv ve aşılanmazsa %100 fatal ensefalit yapar. "
            "5. **Picornaviridae (Çıplak ssRNA):** Poliovirüs (çocuk felci), Rinovirüs (nezle), Hepatit A virüsü (HAV) ve Koksakivirüsler."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "İnfluenza virüsünün segmenter genom yapısı sayesinde domuz veya kuş virüsleriyle genetik parça değişimi yapmasına antijenik shift denir.",
                "antijenik shift",
                "Pandemilere yol açan büyük genomik segment takası olayı"
            ),
            make_before_after(
                "DNA Virüsleri ile RNA Virüslerinin Karşılaştırması",
                "DNA Virüsleri",
                [
                    "Replikasyon genellikle konak hücre çekirdeğinde gerçekleşir",
                    "Hata düzeltme enzimleri nedeniyle mutasyon oranları düşüktür",
                    "Genetik materyal kimyasal olarak daha kararlıdır",
                    "Latent (gizli) kalma eğilimleri yüksektir (özellikle Herpesvirüsler)"
                ],
                "RNA Virüsleri",
                [
                    "Replikasyon kural olarak sitoplazmada yürütülür",
                    "RNA bağımlı RNA polimerazların hata düzeltmesi yoktur, mutasyon sıktır",
                    "Sürekli yeni varyant ve antijenik kaçış suşları üretirler",
                    "Mevsimsel salgınlar ve küresel pandemilere sıkça yol açarlar"
                ]
            ),
            make_active_recall(
                "Mermi şeklinde morfolojiye sahip, çizgili kastan periferik sinirler boyunca retrograd aksonal taşınmayla beyne ulaşan nörotropik RNA virüsü hangisidir?",
                "Kuduz virüsüdür (Rabies virüsü - Rhabdoviridae).",
                "Isırıkla bulaşan mermi şeklindeki ensefalit etkeni"
            )
        ]
    })

    # Slayt 19: [TEKRAR SAYFASI - CHECKPOINT 2]
    slides.append({
        "id": "k1-21-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Prionlar ve Virüsler",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 19,
        "narrative": (
            "Bu ikinci checkpoint sayfasında hücresiz enfeksiyon ajanları alemini, "
            "prionların benzersiz beta-tabakalı nükleik asitsiz yapısını ve fiziksel direncini, "
            "virüslerin nükleokapsid ve zarf mimarisi arasındaki çevresel dayanıklılık farklarını "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp2-1",
                "Prionların yapısı nasıldır ve normal PrPC ile patolojik PrPSc arasındaki temel konformasyonel fark nedir?",
                "Prionlar nükleik asit içermeyen enfeksiyöz proteinlerdir. Normal PrPC alfa-heliks zengini ve proteaza duyarlıyken; patolojik PrPSc beta-tabaka zengini, çözünmeyen ve proteazlara aşırı dirençli formdur.",
                "Genetik materyalsiz molekülün üç boyutlu kıvrım değişimi",
                "Prion Biyolojisi"
            ),
            make_flashcard(
                "fc-k1-21-cp2-2",
                "Zarflı virüsler ile çıplak (zarfsız) virüsler arasında çevresel direnç ve bulaş yolu farkı nedir?",
                "Çıplak virüsler mide asidine ve kuruluğa dirençlidir, fekal-oral yolla yayılabilir. Zarflı virüslerin lipid membranı deterjan, alkol ve kuruluğa aşırı duyarlıdır; yakın temas, damlacık veya kanla bulaşır.",
                "Çevreye dayanıklı kılıfsız yapı ile kimyasala hassas dış katmanın ayrımı",
                "Viral Mimari"
            ),
            make_flashcard(
                "fc-k1-21-cp2-3",
                "Virüslerin yapay cansız besiyerlerinde (agar, buyyon) üreyememesinin temel hücresel nedeni nedir?",
                "Kendi ribozomları ve metabolik ATP üretim enzimleri bulunmadığı için obligat hücre içi parazit olmaları ve konak hücresinin translasyon sistemine bağımlı olmalarıdır.",
                "Aminoasit dizici taneciklerin yokluğu ve serbestçe var olamama durumu",
                "Zorunlu Hücre İçi Yaşam"
            )
        ]
    })

    # Slayt 20: Onkojenik Virüsler ve Bölüm Özeti
    slides.append({
        "id": "k1-21-s20",
        "title": "Onkojenik Virüsler ve Aselüler Etkenler Özeti",
        "section": "Prionlar ve Virüsler",
        "slideNumber": 20,
        "narrative": (
            "Bazı virüsler hücreyi lizise uğratıp öldürmek yerine, konak genomuna entegre olarak veya "
            "tümör baskılayıcı genleri (p53, Rb) inaktive ederek hücresel proliferasyonu kontrolsüzleştirir ve kansere yol açar. "
            "Bu ajanlara **onkojenik (tümör) virüsleri** denir. İnsan kanserlerinin yaklaşık %15'i virüslerle ilişkilidir: "
            "1. **Human Papillomavirüs (HPV Tip 16 ve 18):** E6 proteini ile p53'ü, E7 proteini ile Rb'yi yıkarak serviks ve orofarenks kanserine neden olur. "
            "2. **Epstein-Barr Virüsü (EBV):** Burkitt lenfoma, nazofarenks karsinomu ve Hodgkin lenfoma yapar. "
            "3. **Hepatit B (HBV) ve Hepatit C (HCV):** Kronik karaciğer hasarı ve onkogenez ile hepatosellüler karsinoma (HCC) yol açar. "
            "4. **Human Herpesvirüs-8 (HHV-8):** AIDS hastalarında endotelyal vasküler tümör olan Kaposi sarkomunun etkenidir. "
            "Özetle; aselüler etkenler genetik ve protein düzeyinde konağı sömüren minik ajanlardır. "
            "Bir sonraki bölümümüzde gerçek hücresel yapıya ve hücre duvarına sahip prokaryotik dünyayı, yani **bakterileri** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Human Papillomavirüs tip 16 ve 18 virüslerinin E6 proteini p53'ü inaktive ederken E7 proteini retinoblastom proteinini baskılayarak serviks kanserine yol açar.",
                "retinoblastom",
                "HPV E7 onkoproteininin yıktığı kritik tümör süpresör protein"
            ),
            make_table(
                ["Onkojenik Virüs", "Genom Türü", "İlişkili İnsan Kanseri"],
                [
                    ["HPV (Tip 16, 18, 31, 33)", "Çıplak dsDNA", "Serviks kanseri, anogenital ve orofarengeal karsinomlar"],
                    ["Epstein-Barr Virüsü (EBV)", "Zarflı dsDNA", "Burkitt lenfoma, Nazofarenks karsinomu, Hodgkin lenfoma"],
                    [
                        "HHV-8 (KSHV)",
                        {"text": "Zarflı dsDNA (Vasküler endotel)", "isMasked": True, "hint": "Kazanılmış immün yetmezlikte beliren damarsal Kaposi lezyonu"},
                        "Kaposi Sarkomu ve Primer Efüzyon Lenfoması"
                    ],
                    ["Hepatit B (HBV) / Hepatit C (HCV)", "DNA (HBV) / RNA (HCV)", "Hepatosellüler Karsinom (HCC)"]
                ]
            ),
            make_micro_quiz(
                "Onkojenik virüsler ve yol açtıkları malign neoplazmlar ile ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?",
                {
                    "A": "HPV Tip 16 - Serviks invaziv skuamöz hücreli karsinomu",
                    "B": "EBV - Nazofarenks karsinomu ve Burkitt lenfoma",
                    "C": "HHV-8 - Kaposi sarkomu",
                    "D": "Hepatit B virüsü - Hepatosellüler karsinom",
                    "E": "Kuduz virüsü - Glioblastoma multiforme"
                },
                "E",
                {
                    "A": "A seçeneği doğrudur; serviks kanserinin en sık etkenidir.",
                    "B": "B seçeneği doğrudur; nazofarenks Ca ve lenfomalarla ilişkilidir.",
                    "C": "C seçeneği doğrudur; Kaposi sarkomu etkenidir.",
                    "D": "D seçeneği doğrudur; karaciğer kanserinin majör viral nedenidir.",
                    "E": "E seçeneği yanlıştır: Kuduz virüsü akut fatal ensefalit yapar; onkojenik bir virüs değildir ve beyin tümörüne yol açmaz."
                }
            )
        ]
    })

    return slides
