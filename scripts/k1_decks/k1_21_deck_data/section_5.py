# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 5: Vektörler ve Artropodlar Aracılı Bulaş (Slayt 41 - 50)
Checkpoint 5: Slayt 49
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # Slayt 41: Vektör Kavramı: Biyolojik vs Mekanik Vektör
    slides.append({
        "id": "k1-21-s41",
        "title": "Vektör Kavramı ve İletim Mekanizmaları",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 41,
        "narrative": (
            "Enfeksiyon epidemiyolojisinde bir patojeni enfekte bir kaynaktan alarak duyarlı bir konağa "
            "aktaran canlı taşıyıcılara **vektör** adı verilir. Vektörlerin ezici çoğunluğunu eklem bacaklılar "
            "(artropodlar: böcekler ve keneler) oluşturur. "
            "Patojen ile vektör arasındaki biyolojik ilişkiye göre 2 temel iletim mekanizması tanımlanır: "
            "1. **Biyolojik Vektör:** Patojen mikroorganizma vektörün vücuduna girdikten sonra orada yaşamsal "
            "bir biyolojik evre geçirir; çoğalır (multiplikasyon), gelişimsel başkalaşım geçirir (morfolojik transformasyon) "
            "veya her ikisini birden yapar. Patojenin bulaşabilmesi için vektör içinde belirli bir kuluçka evresi "
            "(ekstrinsik inkübasyon süresi) geçmesi şarttır. "
            "Örnekler: Sıtma parazitinin Anopheles sivrisineğinde eşeyli çoğalması (sporogoni); "
            "KKKA virüsünün Hyalomma kenesinde çoğalması ve transovaryal olarak kenenin yumurtalarına aktarılmasıdır. "
            "2. **Mekanik Vektör:** Patojen eklem bacaklının vücut yüzeyine (bacaklarına, kanatlarına, hortumuna) "
            "pasif olarak yapışır ve hiçbir çoğalma veya gelişim göstermeden bir yerden başka bir yere taşınır. "
            "Klasik örnek: Karasineklerin (Musca domestica) dışkıdaki Shigella veya Salmonella bakterilerini "
            "ayaklarıyla açıkta duran gıdalara taşımasıdır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Patojenin eklem bacaklının vücudunda çoğalarak veya başkalaşım geçirerek nakledildiği iletim biçimine biyolojik vektörlük denir.",
                "biyolojik vektörlük",
                "Patojenin içinde geliştiği aktif vektörel iletim türü"
            ),
            make_before_after(
                "Biyolojik Vektör ile Mekanik Vektör Karşılaştırması",
                "Biyolojik Vektör (Örn. Anopheles sivrisineği)",
                [
                    "Patojen vektörün içinde çoğalır, evrimleşir veya döngüsünü tamamlar",
                    "Bulaşmadan önce vektör içinde zorunlu bir inkübasyon süresi gerekir",
                    "Patojen genellikle tükürük bezi veya dışkı yoluyla aktif inoküle edilir",
                    "Örnek: Sivrisinek-Sıtma, Kene-KKKA, Tatarcık-Leishmania"
                ],
                "Mekanik Vektör (Örn. Karasinek)",
                [
                    "Patojen vektörün dış yüzeyine veya hortumuna pasif olarak bulaşır",
                    "Vektör içinde hiçbir biyolojik çoğalma veya gelişim gerçekleşmez",
                    "Sadece kontamine alandan gıdaya pasif fiziksel taşıma yapar",
                    "Örnek: Karasineğin ayaklarıyla kolera veya amipleri gıdaya taşıması"
                ]
            ),
            make_micro_quiz(
                "Sıtma paraziti Plasmodium'un Anopheles cinsi dişi sivrisinekte eşeyli üreme (sporogoni) evresi geçirmesi hangi vektörel iletim tipinin en klasik örneğidir?",
                {
                    "A": "Mekanik vektörlük",
                    "B": "Biyolojik vektörlük",
                    "C": "Transplasental iletim",
                    "D": "Fomite aracılı bulaş",
                    "E": "Damlacık çekirdeği iletimi"
                },
                "B",
                {
                    "A": "A seçeneği pasif fiziksel taşımadır, organizma içinde üreme olmaz.",
                    "B": "B seçeneği doğrudur: Parazit sivrisineğin bağırsağında ve tükürük bezinde çoğalıp gelişimsel evre geçirdiğinden biyolojik vektörlüktür.",
                    "C": "C seçeneği anneden bebeğe geçiştir.",
                    "D": "D seçeneği cansız eşyalarla bulaştır.",
                    "E": "E seçeneği havadaki partiküllerdir."
                }
            )
        ]
    })

    # Slayt 42: Keneler ve Bulaştırdıkları Kritik Patojenler
    slides.append({
        "id": "k1-21-s42",
        "title": "Keneler (Ixodidae) ve Bulaşan Kritik Patojenler",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 42,
        "narrative": (
            "Keneler (Acarina alt takımı), kan emerek beslenen ve insanlarda en çok çeşitli patojen bulaştıran "
            "eklem bacaklılar arasındadır. Tıbbi açıdan öne çıkan kene türleri ve taşıdıkları tehlikeli hastalıklar şunlardır: "
            "1. **Hyalomma marginatum (Sert kene):** Ülkemizde özellikle İç Anadolu ve Orta Karadeniz havzasında (Kelkit vadisi) "
            "görülen **Kırım-Kongo Kanamalı Ateşi (KKKA)** virüsünün (Nairovirus) ana vektörü ve rezervuarıdır. "
            "Kenenin koparılmadan çıkarılması hayati kuraldır! "
            "2. **Ixodes ricinus / scapularis:** Ormanlık alanlarda yaşayan geyik kenesidir. "
            "Üç farklı mikroorganizmayı aynı anda bulaştırabilir: **Lyme hastalığı** (Borrelia burgdorferi spiroketi), "
            "**Kene Kaynaklı Ensefalit (TBE)** virüsü ve eritrosit içi protozoon olan **Babesiosis** (Babesia microti). "
            "3. **Rhipicephalus sanguineus (Kahverengi köpek kenesi):** Akdeniz havzasında **Rickettsia conorii**'yi "
            "bulaştırarak nekrotik siyah kabuklu (tache noire) **Akdeniz Benekli Ateşi** tablosuna yol açar. "
            "4. **Dermacentor türleri:** **Tularemi** (Francisella tularensis) ve Kayalık Dağlar benekli ateşi taşırlar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de Kırım-Kongo Kanamalı Ateşi virüsünün doğadaki ana vektörü ve rezervuarı Hyalomma marginatum cinsi sert kenelerdir.",
                "Hyalomma marginatum",
                "KKKA bulaştıran çizgili bacaklı sert kene türü"
            ),
            make_table(
                ["Kene Cinsi / Türü", "Primer Konak / Yaşam Alanı", "Bulaştırdığı Kritik Hastalık"],
                [
                    [
                        "Hyalomma marginatum",
                        "Mera, tarım arazisi, yabani kuşlar",
                        {"text": "Kırım-Kongo Kanamalı Ateşi (KKKA)", "isMasked": True, "hint": "Nairovirüs kaynaklı ölümcül hemorajik kene zoonozu"}
                    ],
                    ["Ixodes ricinus", "Geyikler, kemiriciler, ormanlık çalılık", "Lyme hastalığı, Babesiyoz, Kene ensefaliti (TBE)"],
                    ["Rhipicephalus sanguineus", "Evcil ve sokak köpekleri", "Akdeniz Benekli Ateşi (Tache Noire ile giden)"],
                    ["Dermacentor reticulatus", "Çayır ve orman kemiricileri", "Tularemi ve Omsk kanamalı ateşi"]
                ]
            ),
            make_micro_quiz(
                "Ixodes cinsi kenelerin ısırması sonrasında tek bir kene temasıyla eşzamanlı olarak hem Borrelia burgdorferi hem de eritrosit içi protozoon olan Babesia'nın bulaşmasına ne ad verilir?",
                {
                    "A": "Çapraz bağışıklık",
                    "B": "Ko-enfeksiyon (Birlikte enfeksiyon)",
                    "C": "Süperenfeksiyon",
                    "D": "Otoenfeksiyon",
                    "E": "Latent enfeksiyon"
                },
                "B",
                {
                    "A": "A seçeneği bağışıklık cevabıdır.",
                    "B": "B seçeneği doğrudur: Ixodes kenesi aynı anda birden fazla patojeni (Borrelia, Babesia, Anaplasma) bulaştırarak ko-enfeksiyon tablosu oluşturabilir.",
                    "C": "C seçeneği var olan bir enfeksiyon üzerine yeni bir enfeksiyon binmesidir.",
                    "D": "D seçeneği konağın kendi kendine bulaştırmasıdır.",
                    "E": "E seçeneği sessiz enfeksiyondur."
                }
            )
        ]
    })

    # Slayt 43: Sivrisinekler ve Küresel Salgınlar
    slides.append({
        "id": "k1-21-s43",
        "title": "Sivrisinekler (Culicidae) ve Küresel Vektörel Salgınlar",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 43,
        "narrative": (
            "Sivrisinekler, yeryüzünde insan ölümüne en çok yol açan bir numaralı biyolojik vektör ailesidir. "
            "Yalnızca dişi sivrisinekler yumurtalarını geliştirebilmek için memelilerden kan emerler. "
            "Üç ana sivrisinek cinsi küresel salgınları yönetir: "
            "1. **Anopheles Cinsi (Örn. Anopheles gambiae):** Sıtmanın (Plasmodium türleri) biyolojik vektörüdür. "
            "Durgun sularda ürer; tipik olarak gece ve alacakaranlıkta kan emer; konak yüzeyinde dururken gövdesi 45° açılı durur. "
            "2. **Aedes Cinsi (Aedes aegypti ve Aedes albopictus / Asya Kaplan Sivrisineği):** Gündüzleri kan emen, "
            "bacaklarında beyaz çizgili halkalar bulunan agresif sivrisineklerdir. Dört majör arbovirüsün vektörüdür: "
            "**Dengue (Kırık kemik humması)**, **Sarı Humma**, **Chikungunya** ve mikrosefaliye yol açan **Zika Virüsü**. "
            "3. **Culex Cinsi:** Durgun kirli sularda ürer; kuşlar ile insanlar arasında köprü kurarak "
            "**Batı Nil Virüsü (WNV)** ensefalitini ve lenfatik filaryazı (Wuchereria bancrofti / Fil hastalığı) bulaştırır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Gündüz saatlerinde kan emen Aedes cinsi sivrisinekler gebelerde fetal mikrosefali anomalisi yapan Zika virüsünü bulaştırır.",
                "Zika",
                "Aedes ile bulaşan ve konjenital mikrosefali yapan flavivirüs"
            ),
            make_table(
                ["Sivrisinek Cinsi", "Kan Emme Zamanı ve Alışkanlığı", "Bulaştırdığı Majör Patojenler"],
                [
                    ["Anopheles", "Gece ve alacakaranlık (açılı duruş)", "Plasmodium türleri (Sıtma)"],
                    [
                        "Aedes (A. aegypti/albopictus)",
                        {"text": "Gündüz saatleri, çizgili bacaklar", "isMasked": True, "hint": "Aydınlıkta sokan siyah-beyaz benekli sivrisinek"},
                        "Dengue, Sarı Humma, Zika Virüsü, Chikungunya"
                    ],
                    ["Culex", "Gece, kirli durgun sular", "Batı Nil Virüsü ensefaliti, Lenfatik Filaryaz"]
                ]
            ),
            make_micro_quiz(
                "Tropikal bölge seyahatinden dönen bir hastada ani başlayan çok şiddetli kas-eklem ağrıları ('kırık kemik humması'), retroorbital ağrı ve döküntü gelişiyor. Aedes sivrisineğiyle bulaşan bu etken hangisidir?",
                {
                    "A": "Dengue Virüsü",
                    "B": "Plasmodium falciparum",
                    "C": "Batı Nil Virüsü",
                    "D": "Kuduz virüsü",
                    "E": "Borrelia burgdorferi"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Dengue virüsü (Flaviviridae) Aedes sivrisinekleriyle bulaşır ve şiddetli eklem-kemik ağrıları nedeniyle 'kırık kemik humması' olarak bilinir.",
                    "B": "B seçeneği Anopheles ile bulaşır ve titremeli sıtma nöbeti yapar.",
                    "C": "C seçeneği Culex ile bulaşır.",
                    "D": "D seçeneği kuduz köpek ısırığıyla bulaşır.",
                    "E": "E seçeneği kene ile bulaşır."
                }
            )
        ]
    })

    # Slayt 44: Pireler ve Tarihi Salgınlar
    slides.append({
        "id": "k1-21-s44",
        "title": "Pireler (Siphonaptera): Kara Ölüm Veba ve Murin Tifüs",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 44,
        "narrative": (
            "Pireler, kanatsız, lateralden basık, güçlü arka bacaklarıyla zıplayabilen ve memelilerin kanıyla beslenen ektoparazitlerdir. "
            "İnsanlık tarihinin demografik yapısını değiştiren en yıkıcı salgınların taşıyıcısı olmuşlardır: "
            "1. **Xenopsylla cheopis (Oryantal Sıçan Piresi):** **Yersinia pestis** bakterisinin (Veba / Kara Ölüm) ana vektörüdür. "
            "Bakteri pirenin ön midesinde (proventrikülüs) biyofilm oluşturarak sindirim yolunu tıkar. "
            "Pire sürekli acıkır, kan emmeye çalıştığında tıkanıklık yüzünden kan geriye reflü olur ve bakteri ısırık yarasına kusulur! "
            "Hastalık kasık lenf bezlerinde devasa süpüratif apselere (**Bubonik Veba / Hıyarcıklı Veba**) "
            "veya kanda yayılarak ekstremitelerde siyah gangrenlere (septisemik veba) yol açar. "
            "Orta Çağ Avrupası'nda nüfusun üçte birini yok eden 'Kara Ölüm' bu mekanizmayla gerçekleşmiştir. "
            "2. **Endemik (Murin) Tifüs:** Yine sıçan pirelerinin dışkısıyla çıkarılan **Rickettsia typhi** bakterisinin kaşınma ile deriye inokülasyonu sonucu gelişir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Orta Çağ'da Kara Ölüm olarak adlandırılan veba salgınlarının vektörü sıçan piresi olan Xenopsylla cheopis türüdür.",
                "Xenopsylla cheopis",
                "Yersinia pestis taşıyan oryantal sıçan piresi türü"
            ),
            make_causal_chain(
                "Pire Aracılı Veba Bulaşma Mekanizması",
                [
                    "1. Enfekte Kemirici: Sıçan piresi kanda Yersinia pestis taşıyan kemiriciden kan emer.",
                    "2. Proventriküler Blokaj: Bakteri pirenin ön midesinde biyofilm yaparak sindirim kanalını tıkar.",
                    "3. Açlık ve Isırma Çılgınlığı: Aç kalan pire doyamaz ve hırsla insanları ısırmaya başlar.",
                    "4. Regürjitasyon: Pıhtılaşmış kan ve bakteri yığını insan dermal kapillerine geri kusulur.",
                    "5. Bubon Oluşumu: Bölgesel lenf bezine göç eden bakteri hemorajik nekrotik bubona yol açar."
                ]
            ),
            make_active_recall(
                "Yersinia pestis bakterisinin neden olduğu veba hastalığında regional lenf nodlarının dev boyutlara ulaşıp süpüre olmasına ne ad verilir?",
                "Bubon (Hıyarcık / Bubonik veba) adı verilir.",
                "Veba hastalığının ağrılı şişmiş lenf nodu lezyonu"
            )
        ]
    })

    # Slayt 45: Tatarcıklar ve Leishmaniasis
    slides.append({
        "id": "k1-21-s45",
        "title": "Tatarcıklar (Phlebotomus) ve Leishmaniasis Spektrumu",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 45,
        "narrative": (
            "Tatarcıklar (kum sinekleri / Phlebotomus türleri), sivrisineklerden çok daha küçük (2-3 mm), "
            "tüylü kanatlı, sessiz uçan ve geceleri alacakaranlıkta kan emen artropodlardır. "
            "Tıbbi açıdan hücre içi protozoon olan **Leishmania** türlerinin biyolojik vektörüdürler. "
            "Tatarcık kan emerken promastigot formundaki parazitleri deriye inoküle eder; dokuda makrofajlar içine giren parazit "
            "kamçısız **amastigot** formuna dönüşür. Klinikte iki zıt tablo yaratır: "
            "1. **Kutanöz Leishmaniasis (Şark Çıbanı):** Etkenleri Leishmania tropica ve L. major'dur. "
            "Türkiye'de özellikle Güneydoğu Anadolu (Şanlıurfa) ve Akdeniz bölgesinde endemiktir. "
            "Isırık yerinde aylar içinde ülsere olan, kenarları kabarık, volkan krateri benzeri nedbe bırakan granülomlar yapar. "
            "2. **Visseral Leishmaniasis (Kala-Azar / Kara Hastalık):** Etkenleri L. donovani ve L. infantum'dur. "
            "Parazit tüm retiküloendotelyal sisteme yayılır; **masif splenomegali**, hepatomegali, pansitopeni, kaşeksi ve tedavi edilmezse ölümle sonuçlanır. "
            "Tatarcıklar ayrıca Phlebovirüs kaynaklı kısa süreli yüksek ateş tablosu olan **Tatarcık Humması (Papatasi ateşi)** bulaştırırlar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de Şanlıurfa yöresinde şark çıbanı olarak bilinen kutanöz leishmaniasis tablosunun vektörü Phlebotomus cinsi tatarcıklardır.",
                "Phlebotomus",
                "Kum sineği olarak da bilinen küçük tüylü kan emici vektör cinsi"
            ),
            make_before_after(
                "Kutanöz Leishmaniasis ile Visseral Leishmaniasis Karşılaştırması",
                "Kutanöz Leishmaniasis (Şark Çıbanı)",
                [
                    "Etken: Leishmania tropica ve Leishmania major",
                    "Doku tutulumu: Yalnızca ısırık bölgesindeki deri ve subkutan doku",
                    "Klinik tablo: İyileşirken volkan krateri şeklinde skar bırakan kronik ülser",
                    "Sistemik yayılım: İç organ tutulumu ve hayati tehlike oluşturmaz"
                ],
                "Visseral Leishmaniasis (Kala-Azar)",
                [
                    "Etken: Leishmania donovani ve Leishmania infantum",
                    "Doku tutulumu: Kemik iliği, dalak, karaciğer ve lenf bezleri",
                    "Klinik tablo: Masif splenomegali, pansitopeni, hiperpigmentasyon ve kaşeksi",
                    "Sistemik yayılım: Tedavi edilmediğinde %90'ın üzerinde ölümcüldür"
                ]
            ),
            make_micro_quiz(
                "Güneydoğu Anadolu bölgesinde açıkta kalan yüz ve kol derisinde tatarcık ısırığı sonrası aylar içinde gelişen kenarları kalkık, ağrısız ve granülomatöz 'şark çıbanı' lezyonunun etkeni hangisidir?",
                {
                    "A": "Leishmania tropica",
                    "B": "Trypanosoma cruzi",
                    "C": "Plasmodium vivax",
                    "D": "Toxoplasma gondii",
                    "E": "Babesia microti"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Leishmania tropica Türkiye'de kutanöz leishmaniasis (şark çıbanı) tablosunun primer etkenidir.",
                    "B": "B seçeneği Chagas hastalığı etkenidir, Amerika'da görülür.",
                    "C": "C seçeneği sıtma etkenidir.",
                    "D": "D seçeneği toksoplazmoz etkenidir.",
                    "E": "E seçeneği kene kaynaklı intraeritrositer parazittir."
                }
            )
        ]
    })

    # Slayt 46: Bitler ve Bulaştırdıkları Hastalıklar
    slides.append({
        "id": "k1-21-s46",
        "title": "Bitler (Anoplura) ve Epidemik Tifüs, Siper Ateşi, Dönek Ateş",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 46,
        "narrative": (
            "Bitler (Pediculus humanus), insan vücudunda yaşayan, kanatsız, konak özgüllüğü çok yüksek ektoparazitlerdir. "
            "İki alt türü vardır: Saç biti (P. humanus capitis) ve **Vücut biti (P. humanus corporis)**. "
            "Saç biti vektörlük yapmazken, çamaşır dikişlerinde yaşayan vücut biti insanlık tarihinde 3 kritik enfeksiyonun vektörüdür: "
            "1. **Epidemik Tifüs (Rickettsia prowazekii):** Bit kan emerken dışkılar; dışkıda bol miktarda riketsiya bulunur. "
            "Kişi kaşındığında derideki mikro-çiziklerden bakteri kana girer (bitin ısırmasıyla değil, dışkısının kaşınmasıyla bulaşır!). "
            "2. **Siper Ateşi (Trench Fever - Bartonella quintana):** 1. Dünya Savaşı siperlerinde askerler arasında yayılmış, "
            "5 günde bir tekrarlayan ateş nöbetleri, kaval kemiği (tibia) ağrısı ve endokarditle seyreden enfeksiyondur. "
            "3. **Bit Kaynaklı Dönek Ateş (Louse-borne Relapsing Fever - Borrelia recurrentis):** Bit ezildiğinde hemolenfindeki "
            "spiroketlerin deriye temasıyla bulaşır; antijenik varyasyonlar nedeniyle tekrarlayan ateş atakları yapar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Epidemik tifüs etkeni olan Rickettsia prowazekii bitin ısırmasıyla değil dışkısının kaşınarak deriye inokülasyonu ile bulaşır.",
                "dışkısının kaşınarak",
                "Vücut bitinin riketsiyayı deriye geçirme mekanizması"
            ),
            make_table(
                ["Vücut Bitiyle Bulaşan Hastalık", "Mikrobiyolojik Patojen", "Karakteristik Klinik Tablo"],
                [
                    ["Epidemik Tifüs", "Rickettsia prowazekii", "Yüksek ateş, delirium, gövdeden yayılan döküntü, Brill-Zinsser nüksü"],
                    [
                        "Siper Ateşi (Trench fever)",
                        {"text": "Bartonella quintana", "isMasked": True, "hint": "Siperlerdeki askerlerde görülen bakteri"},
                        "5 günde bir tekrarlayan ateş, şiddetli pretibial bacak ağrısı"
                    ],
                    ["Bit Kaynaklı Dönek Ateş", "Borrelia recurrentis", "Antijenik varyasyonla tekrarlayan ateş ve hepatosplenomegali"]
                ]
            ),
            make_micro_quiz(
                "Birinci Dünya Savaşı sırasında askerlerin siperlerde uzun süre yıkanamaması sonucu vücut biti aracılığıyla yayılan ve pretibial (kaval kemiği) şiddetli ağrılarla seyreden Siper Ateşinin etkeni hangisidir?",
                {
                    "A": "Bartonella quintana",
                    "B": "Rickettsia prowazekii",
                    "C": "Borrelia burgdorferi",
                    "D": "Yersinia pestis",
                    "E": "Coxiella burnetii"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Bartonella quintana vücut bitiyle bulaşan siper ateşinin (trench fever) etkenidir.",
                    "B": "B seçeneği epidemik tifüs etkenidir.",
                    "C": "C seçeneği kene ile bulaşan Lyme etkenidir.",
                    "D": "D seçeneği veba etkenidir.",
                    "E": "E seçeneği Q ateşi etkenidir."
                }
            )
        ]
    })

    # Slayt 47: Doğrudan Ektoparaziter Artropodlar: Uyuz ve Saç Biti
    slides.append({
        "id": "k1-21-s47",
        "title": "Doğrudan Ektoparazitler: Uyuz (Scabies) ve Pedikuloz",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 47,
        "narrative": (
            "Bazı artropodlar başka bir mikroorganizmayı taşımak yerine, bizzat kendileri insan derisine yerleşerek "
            "doğrudan primer ektoparaziter hastalık oluştururlar: "
            "1. **Sarcoptes scabiei var. hominis (Uyuz Akarı):** Mikroskobik bir akardır. "
            "Dişi akar derinin en dış tabakası olan **stratum korneum içine tüneller (silion)** kazar ve buralara yumurtalarını ve dışkısını bırakır. "
            "Akarın proteinlerine ve dışkısına karşı gelişen tip IV gecikmiş aşırı duyarlılık yanıtı nedeniyle "
            "**geceleri yatakta ısıyla şiddetlenen**, parmak araları, el bileği fleksör yüzü, aksilla, bel ve genital bölgeyi tutan "
            "dayanılmaz kaşıntıya yol açar. "
            "Bağışıklığı çökmüş veya yaşlılarda milyonlarca akarın kabuklu lezyonlar yaptığı şekline **Norveç Uyuzu (Kabuklu Uyuz)** denir. "
            "Tedavide tüm aile bireyleri eşzamanlı olarak permetrin losyon veya oral ivermektin ile tedavi edilmeli, çamaşırlar 60°C'de yıkanmalıdır. "
            "2. **Pediculus humanus capitis (Saç Biti):** Saçlı deride yaşar, saç tellerine yapışık beyaz kapsüllü yumurtalar (**sirke**) bırakır; "
            "doğrudan temasla özellikle okul çağındaki çocuklarda salgınlar yapar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Sarcoptes scabiei dişi akarının derinin stratum korneum tabakasında açtığı tünellere silion adı verilir.",
                "silion",
                "Uyuz akarının cildin boynuzsu tabakasında kazdığı dalgalı tünel"
            ),
            make_table(
                ["Ektoparaziter Tablo", "Parazit Türü", "Tipik Tutulum Alanı ve Klinik"],
                [
                    ["Klasik Uyuz (Scabies)", "Sarcoptes scabiei", "El parmak araları, bilekler; gece artan kaşıntı ve tüneller"],
                    [
                        "Norveç Uyuzu (Kabuklu)",
                        {"text": "Aşırı akar yükü (milyonlarca akar)", "isMasked": True, "hint": "İmmünsüpresif konakta görülen formu"},
                        "Kalın kabuklu psöriyazis benzeri döküntü, kaşıntı hafif olabilir"
                    ],
                    ["Saç Biti (Pediküloz)", "Pediculus humanus capitis", "Oksipital ve kulak arkası saç köklerinde kaşıntı ve sirkeler"]
                ]
            ),
            make_micro_quiz(
                "Gece yatakta sıcakla şiddetlenen kaşıntı, parmak aralarında kıvrımlı tüneller (silion) ve ekskoriasyonlarla başvuran bir hastada uyuz tanısı konduğunda tedavi yönetimindeki en kritik epidemiyolojik kural nedir?",
                {
                    "A": "Yalnızca kaşınan hastanın tek bir doz antihistaminik alması yeterlidir.",
                    "B": "Semptomu olsun ya da olmasın aynı evde yaşayan tüm aile bireylerinin eşzamanlı olarak tedavi edilmesi gerekir.",
                    "C": "Hastanın derhal 1 ay süreyle karantinaya alınması şarttır.",
                    "D": "Hastaya yüksek doz damardan penisilin başlanmalıdır.",
                    "E": "Tedavide yalnızca saçların tamamen kazınması yeterlidir."
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; antihistaminik akarı öldürmez, tek kişi tedavi edilirse reenfeksiyon olur.",
                    "B": "B seçeneği doğrudur: Asemptomatik kuluçka dönemindeki bireylerden yeniden bulaşmayı önlemek için evdeki tüm temaslılar eşzamanlı tedavi edilmelidir.",
                    "C": "C seçeneği karantina gerektirmez, topikal tedavi yeterlidir.",
                    "D": "D seçeneği yanlıştır; parazittir, antibiyotik etkisizdir.",
                    "E": "E seçeneği saç biti ile karıştırılmıştır."
                }
            )
        ]
    })

    # Slayt 48: Vektör Kontrol Stratejileri
    slides.append({
        "id": "k1-21-s48",
        "title": "Vektör Kontrol Stratejileri ve Çevresel Yönetim",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 48,
        "narrative": (
            "Vektörlerle bulaşan hastalıkların kontrolünde en etkili ve kalıcı halk sağlığı yaklaşımı, "
            "enfeksiyon zincirinin vektör halkasını kırmaktır (**Vektör Mücadelesi**). "
            "Modern tıp ve halk sağlığı 4 entegre yöntem kullanır: "
            "1. **Çevresel Yönetim (Kaynak Yok Etme):** Vektörlerin üreme alanlarının kurutulmasıdır. "
            "Sivrisinekler için su birikintilerinin, bataklıkların, atık lastiklerin ve açık su tanklarının boşaltılması/ıslahı; "
            "kemiriciler için çöplüklerin kontrolü ve sanitasyonun sağlanması. "
            "2. **Kimyasal Kontrol:** İnsektisit (böcek öldürücü) ve akarisit uygulamaları. "
            "DDT tarihi bir örnektir; günümüzde çevreye daha az zararlı piretroidler ve organofosfatlar kullanılır. "
            "Ancak artropodların kimyasallara karşı geliştirdiği direnç büyük bir küresel sorundur. "
            "3. **Kişisel Korunma:** İnsektisit emdirilmiş cibinlikler (ITN - sıtmada mortaliteyi %50 azaltır), "
            "uzun kollu giysiler, DEET veya pikaridin içeren kovucu (repellent) losyonlar ve kene mevsiminde pantolon paçalarının çorap içine sokulması. "
            "4. **Biyolojik Kontrol:** Larvalarla beslenen Gambusia balıklarının göletlere salınması veya genetiği değiştirilmiş kısır erkek sivrisineklerin doğaya bırakılması."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Sıtmanın endemik olduğu tropikal bölgelerde çocuk ölümlerini yarı yarıya azaltan en ucuz ve etkili kişisel koruma aracı insektisit emdirilmiş cibinlik kullanımıdır.",
                "cibinlik",
                "Gece Anopheles ısırıklarını engelleyen koruyucu yatak tülü"
            ),
            make_before_after(
                "Çevresel Yönetim ile Kimyasal Vektör Kontrolü Karşılaştırması",
                "Çevresel Yönetim (Üreme Alanı Islahı)",
                [
                    "Durgun su birikintilerinin kurutulması, bataklık ıslahı",
                    "Uzun vadeli, kalıcı ve ekolojik dengeyi koruyan yaklaşım",
                    "Direnç gelişim riski kesinlikle yoktur",
                    "Toplum katılımı ve belediye altyapısı gerektirir"
                ],
                "Kimyasal Kontrol (İnsektisit / İlaçlama)",
                [
                    "Ergin ve larva öldürücü kimyasal ajanların püskürtülmesi",
                    "Akut salgın durumlarında hızla etki gösteren acil müdahale",
                    "Zamanla vektörlerde kimyasal direnç mutasyonları gelişir",
                    "Diğer faydalı canlılara ve su ekosistemine toksik yan etkileri olabilir"
                ]
            ),
            make_active_recall(
                "Durgun sulardaki sivrisinek larvalarını yiyerek biyolojik mücadele sağlayan tatlı su balığı türü hangisidir?",
                "Gambusia affinis (Sivrisinek balığı) türüdür.",
                "Biyolojik larva mücadelesinde kullanılan balık cinsi"
            )
        ]
    })

    # Slayt 49: [TEKRAR SAYFASI - CHECKPOINT 5]
    slides.append({
        "id": "k1-21-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Vektörler ve Artropodlar",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 49,
        "narrative": (
            "Bu beşinci checkpoint sayfasında vektörel bulaşın biyolojik ve mekanik temellerini, "
            "Türkiye için kritik kene kaynaklı KKKA virüsünü, sivrisineklerin ölümcül türlerini (Anopheles, Aedes) "
            "ve uyuz akarı patolojisini 3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp5-1",
                "Biyolojik vektör ile mekanik vektör arasındaki temel biyolojik etkileşim farkı nedir?",
                "Biyolojik vektörde patojen vektörün içinde çoğalır veya gelişimsel başkalaşım geçirir (örn. sivrisinekte sıtma). Mekanik vektörde ise patojen sadece vücut yüzeyine yapışarak fiziksel olarak taşınır, çoğalma olmaz (örn. karasinekte kolera).",
                "Eklembacaklı bünyesinde paraziter evrimleşme ile pasif dışsal nakil ayrımı",
                "Vektör Biyolojisi"
            ),
            make_flashcard(
                "fc-k1-21-cp5-2",
                "Aedes cinsi sivrisineklerin bulaştırdığı 4 majör arbovirüs hangileridir?",
                "Dengue (Kırık kemik humması), Sarı Humma virüsü, Chikungunya virüsü ve Zika virüsüdür.",
                "Gündüz sokan çizgili bacaklı sivrisineğin 4 viral hastalığı",
                "Sivrisinek Vektörleri"
            ),
            make_flashcard(
                "fc-k1-21-cp5-3",
                "Uyuz (Scabies) hastalığında derideki şiddetli gece kaşıntısının ve patolojik tünellerin (silion) sorumlusu nedir?",
                "Sarcoptes scabiei dişi akarının stratum korneum tabakasına tünel kazarak yumurta ve dışkı bırakması ve buna karşı gelişen tip 4 gecikmiş aşırı duyarlılık reaksiyonudur.",
                "Uyuz etkeninin deride açtığı kanallara verilen dördüncü küme hücresel hipersensitivite",
                "Ektoparazitoloji"
            )
        ]
    })

    # Slayt 50: Vektörel Tehditler Özeti ve Patojen-Konak Dengesine Geçiş
    slides.append({
        "id": "k1-21-s50",
        "title": "Vektörler Bölüm Özeti: Patojen-Konak Etkileşimine Doğru",
        "section": "Vektörler ve Artropodlar",
        "slideNumber": 50,
        "narrative": (
            "Özetle; artropod vektörler doğadaki hayvan rezervuarları ile insan toplulukları arasında "
            "ölümcül biyolojik köprüler kurarlar. Keneler KKKA, Lyme ve riketsiyozları taşırken; "
            "sivrisinekler sıtma, sarı humma, dengue ve Zika salgınlarını yönetir. "
            "Pireler vebanın, tatarcıklar şark çıbanı ve kala-azarın, bitler ise tifüsün taşıyıcısıdır. "
            "Uyuz akarı ise bizzat kendisi deride tünel açarak ektoparaziter hastalık oluşturur. "
            "Ancak bir patojenin vektörle veya başka bir yolla insan vücuduna girmesi, tek başına klinik hastalığın gelişeceği anlamına gelmez! "
            "Hastalığın ortaya çıkıp çıkmayacağını belirleyen asıl dinamik, mikroorganizmanın sahip olduğu "
            "**virülans faktörleri (toksinler, kapsül, enzimler)** ile konak bağışıklık sisteminin direnci arasındaki "
            "hassas biyolojik dengedir. Altıncı bölümümüzde bu **patojen-konak etkileşimini ve enfeksiyon gelişim faktörlerini** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Vektörlerle bulaşan hastalıkların önlenmesinde vektör üreme alanlarının kurutulması en kalıcı çevresel yönetim yöntemidir.",
                "çevresel yönetim",
                "Bataklık ve su birikintisi ıslahını içeren halk sağlığı mücadelesi"
            ),
            make_table(
                ["Vektör Artropod Grubu", "Temel Türü", "İnsanlığa Tehdidi"],
                [
                    ["Keneler", "Hyalomma marginatum", "Kırım-Kongo Kanamalı Ateşi ve yaygın mortalite"],
                    [
                        "Sivrisinekler",
                        {"text": "Anopheles ve Aedes türleri", "isMasked": True, "hint": "Sıtma ve sarı humma vektörleri"},
                        "Sıtma, Dang, Sarı Humma, Zika küresel salgınları"
                    ],
                    ["Pireler", "Xenopsylla cheopis", "Tarihi veba pandemileri ve hıyarcıklı veba"],
                    ["Tatarcıklar", "Phlebotomus cinsi", "Kutanöz şark çıbanı ve ölümcül visseral kala-azar"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki enfeksiyon hastalıklarından hangisinin bulaşmasında hiçbir eklem bacaklı (artropod) vektör rol oynamaz?",
                {
                    "A": "Sıtma",
                    "B": "Kırım-Kongo Kanamalı Ateşi",
                    "C": "Kolera (Vibrio cholerae)",
                    "D": "Lyme hastalığı",
                    "E": "Akdeniz Benekli Ateşi"
                },
                "C",
                {
                    "A": "A seçeneği Anopheles sivrisineği ile bulaşır.",
                    "B": "B seçeneği Hyalomma kenesi ile bulaşır.",
                    "C": "C seçeneği doğrudur: Kolera fekal-oral yolla kontamine suların ve gıdaların tüketilmesiyle bulaşır; biyolojik bir vektörü yoktur.",
                    "D": "D seçeneği Ixodes kenesi ile bulaşır.",
                    "E": "E seçeneği Rhipicephalus kenesi ile bulaşır."
                }
            )
        ]
    })

    return slides
