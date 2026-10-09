# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 6: Sjögren Sendromu, Sistemik Skleroz ve İnflamatuvar Miyopatiler (Slayt 51 - 60)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_6_slides():
    slides = []

    # Slayt 51: Sjögren Sendromu: Etyopatogenez ve İmmünopatoloji
    slides.append({
        "id": "k1-25-s51",
        "title": "Sjögren Sendromu: Etyopatogenez ve İmmünopatoloji",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 51,
        "narrative": (
            "Sjögren sendromu, gözyaşı ve tükürük bezlerinin immün aracılı yıkımı sonucu gelişen kronik otoimmün ekzokrinopatidir: "
            "1. **Klinik Formlar:** "
            "- **Primer Sjögren (Sicca Sendromu):** Başka bir romatolojik hastalık olmaksızın izole ekzokrin bez tutulumudur. "
            "- **Sekonder Sjögren:** Romatoid artrit, SLE veya skleroderma gibi diğer otoimmün tabloların zemininde gelişir. "
            "2. **İmmünopatoloji:** T lenfositleri (CD4+ Th1/Th17) ve B lenfositleri lakrimal ve tükürük bezi kanalları etrafına toplanır. "
            "Salgı bezlerinin asinusları atrofiye uğrar; lümenler kollaps olur ve yerini duktal hiperplazi ile fibrozise bırakır. "
            "3. **Spesifik Otoantikorlar:** Hastaların %70-90'ında **Anti-Ro (SSA)** ve %50-70'inde **Anti-La (SSB)** antikorları saptanır. "
            "Bu ribonükleoprotein antikorları kutanöz lupus ve yenidoğanda konjenital kalp bloğu ile de yakından ilişkilidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sjögren Sendromu İmmünolojik Belirteçleri",
                ["Otoantikor / Hücresel Belirteç", "Görülme Sıklığı", "Hedef İntraselüler Yapı", "Klinik Patolojik Önemi"],
                [
                    ["Anti-Ro (SSA)", "%70 - 90 Pozitif", "Küçük sitoplazmik ribonükleoprotein", "Erken başlangıç, ekstraglandüler tutulum"],
                    [
                        "Anti-La (SSB)",
                        "%50 - 70 Pozitif",
                        {"text": "RNA polimeraz III ilişkili antijen", "isMasked": True, "hint": "Anti-Ro ile birlikte Sjögren tanısını destekleyen ikinci antikor"},
                        "Anti-Ro pozitifliğiyle birlikte varlığında tanı kesinleşir"
                    ],
                    ["Romatoid Faktör (RF)", "%75 Pozitif", "IgG Fc parçasına karşı IgM", "Poliklonal B hücresi hiperaktivitesinin kanıtı"],
                    ["ANA Pozitifliği", "%80 - 95 Pozitif", "Homojen veya benekli boyanma", "Yüksek otoimmün sensitivite"]
                ]
            ),
            make_active_recall(
                "Sjögren sendromu tanısında en sık pozitifleşen ve ribonükleoprotein komplekslerine karşı yönelen iki temel tanısal otoantikor hangileridir?",
                "Anti-Ro (SSA) ve Anti-La (SSB) antikorlarıdır.",
                "Kuru göz ve kuru ağız sendromunda kanda aranan anahtar antikor çifti"
            )
        ]
    })

    # Slayt 52: Sjögren Sendromunda Klinik Tanı ve MALT Lenfoma Riski
    slides.append({
        "id": "k1-25-s52",
        "title": "Sjögren Sendromunda Klinik Tanı ve MALT Lenfoma Riski",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 52,
        "narrative": (
            "Sjögren sendromunda klinik semptomlar bezlerin kurumasından kaynaklanır; ancak en ölümcül komplikasyon lenfomadır: "
            "1. **Klinik Tablo:** Gözyaşı eksikliği kornea epitelinde erozyonlara yol açar (**keratokonjonktivit sikka**). "
            "Tükürük salgısının durması (**kserostomi**) konuşma ve yutma güçlüğü, dilde çatlaklar ve masif diş çürükleri yapar. "
            "Tükürük bezleri (özellikle parotis) iki taraflı ağrısız olarak büyür. "
            "2. **Biyopsi Tanısı (Fokus Skoru):** Alt dudak minör tükürük bezi biyopsisi altın standarttır. 4 mm2 doku alanında "
            "**en az 50 lenfosit içeren agregatlara 'fokus'** denir; fokus skorunun >=1 olması tanısaldır. "
            "3. **Malignite Riski (B Hücreli MALT Lenfoma):** Yıllar boyu bez içinde süregiden poliklonal B lenfosit uyarımı, "
            "zamanla monoklonal mutasyona uğrar. Sjögren hastalarında marjinal zon **B hücreli lenfoma (MALT lenfoma) riski "
            "normal topluma göre yaklaşık 40 kat artmıştır**! Parotis bezinde ani asimetrik sertleşme lenfomayı düşündürmelidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Sjögren Sendromundan MALT Lenfomaya Progresyon",
                [
                    "1. Kronik Lenfositik Akın: Ekzokrin bez stromasına aralıksız T ve B hücresi toplanması",
                    "2. Poliklonal B Hiperaktivitesi: Sürekli antijenik uyarı ile hipergamaglobulinemi ve RF üretimi",
                    "3. Monoklonal Klon Çıkışı: Kronik inflamatuar zeminde B hücrelerinde genetik mutasyon birikimi",
                    "4. MALT Lenfoma: Tükürük bezinde marjinal zon B hücreli malign lenfoma kütlesinin belirmesi"
                ]
            ),
            make_cloze(
                "Sjögren sendromlu hastalarda kronik B hücresi uyarımı zemininde gelişme riski 40 kat artan malignite B hücreli MALT lenfomadır.",
                "MALT lenfoma",
                "Mukoza ilişkili lenfoid doku marjinal zon B hücreli neoplazisi"
            )
        ]
    })

    # Slayt 53: Sistemik Skleroz (Skleroderma): Üçlü Patofizyolojik Sacayağı
    slides.append({
        "id": "k1-25-s53",
        "title": "Sistemik Skleroz (Skleroderma): Üçlü Patofizyolojik Sacayağı",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 53,
        "narrative": (
            "Sistemik Skleroz (Skleroderma), yaygın mikrovasküler hasar ve tüm dokularda aşırı kollajen birikimi (fibrozis) ile "
            "karakterize multisistemik kronik hastalıktır. Patogenezi birbirini tetikleyen üçlü sacayağına dayanır: "
            "1. **Mikrovasküler Endotel Hasarı:** Hastalığın en erken olayıdır. Endotel aktivasyonu, lökosit adezyonu, intimal "
            "kalınlaşma ve yaygın kapiller kaybı gelişir. Damar lümenleri daralır; doku hipoksisi başlar. "
            "2. **Otoimmün İnflamasyon:** T lenfositleri (özellikle Th2) dokuya toplanarak masif sitokinler salgılar: "
            "**TGF-beta**, **IL-4** ve trombosit kaynaklı büyüme faktörü (**PDGF**). "
            "3. **Masif Fibroblast Aktivasyonu:** TGF-beta uyarımı altındaki fibroblastlar kapatılamayan bir kollajen fabrikasına "
            "dönüşür. Doku aralığı Tip I ve Tip III kollajen, fibronektin ve proteoglikanlarla tıkanır; organlar taş gibi sertleşir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sistemik Sklerozun Üçlü Patofizyolojik Döngüsü",
                ["Sacayağı Basamağı", "Tetikleyici Moleküller", "Hücresel Düzeyde Yanıt", "Patolojik Sonuç"],
                [
                    ["Vasküler Hasar", "Endotelin artışı, NO kaybı", "Mikrovasküler endotel ölümü ve intimal hiperplazi", "Raynaud fenomeni ve iskemik ülserler"],
                    [
                        "İmmün Aktivasyon",
                        "Th2 sitokinleri ve makrofajlar",
                        {"text": "Masif TGF-beta ve PDGF salınımı", "isMasked": True, "hint": "Fibroblastları kontrolsüz kollajen üretimine sevk eden ana sitokin"},
                        "Kronik interstisyel inflamasyon"
                    ],
                    ["Fibrozis", "Aşırı Tip I / III kollajen sentezi", "Miyofibroblast farklılaşması", "Deri sertleşmesi ve visseral organ iflası"]
                ]
            ),
            make_active_recall(
                "Sistemik sklerozda fibroblastları uyararak aşırı kollajen sentezine ve geri dönüşümsüz doku sertleşmesine yol açan temel profibrotik sitokin hangisidir?",
                "Transforme Edici Büyüme Faktörü-beta (TGF-beta) molekülüdür.",
                "Kronik fibrozis ve skar oluşumunun ana orkestra şefi sitokin"
            )
        ]
    })

    # Slayt 54: Diffüz Sistemik Skleroz vs Sınırlı Sistemik Skleroz (CREST)
    slides.append({
        "id": "k1-25-s54",
        "title": "Diffüz Sistemik Skleroz vs Sınırlı Sistemik Skleroz (CREST)",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 54,
        "narrative": (
            "Sistemik skleroz, klinik tutulumun yaygınlığına ve otoantikor profiline göre iki ana grupta incelenir: "
            "1. **Diffüz Sistemik Skleroz:** "
            "- **Deri:** Gövdeyi ve ekstremitelerin proksimalini (kol ve uyluk) tutan yaygın, hızlı ilerleyen cilt sertleşmesi. "
            "- **Visseral Organlar:** Çok erken dönemde interstisyel akciğer fibrozisi, skleroderma renal krizi ve miyokard fibrozisi gelişir. "
            "- **Otoantikor:** **Anti-DNA topoizomeraz I (Anti-Scl-70)** antikorları pozitiftir (%70). Prognozu kötüdür. "
            "2. **Sınırlı Sistemik Skleroz (CREST Sendromu):** "
            "- **Deri:** Fibrozis el, yüz ve ön kolla sınırlıdır; gövdeye yayılmaz. "
            "- **Klinik Tablo:** Yıllar boyu stabil kalan **CREST** sendromu ile seyreder. Geç dönemde pulmoner hipertansiyon riski vardır. "
            "- **Otoantikor:** **Anti-Sentromer antikorları (ACA)** pozitiftir (%80-90). Prognozu nispeten iyidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Diffüz vs Sınırlı Skleroderma Karşılaştırması",
                "Diffüz Sistemik Skleroz",
                "Gövdeyi tutan yaygın fibrozis, erken akciğer/böbrek yetmezliği, Anti-Scl-70 pozitifliği ve kötü prognoz",
                "Sınırlı Sistemik Skleroz (CREST)",
                "El ve yüzle sınırlı sertleşme, CREST bulguları, Anti-Sentromer (ACA) pozitifliği ve yavaş seyir"
            ),
            make_micro_quiz(
                "Parmaklarında ve yüzünde skleroz saptanan, gövdesinde cilt sertleşmesi bulunmayan ve laboratuvarında Anti-Sentromer antikoru (ACA) saptanan bir hastada en olası klinik tablo hangisidir?",
                {
                    "A": "Sınırlı Sistemik Skleroz (CREST Sendromu)",
                    "B": "Diffüz Sistemik Skleroz (Anti-Scl-70)",
                    "C": "Sistemik Lupus Eritematozus",
                    "D": "Dermatomiyozit",
                    "E": "Ankilozan Spondilit"
                },
                "A",
                {
                    "A": "Doğrudur; el-yüz sınırlı tutulum ve Anti-Sentromer antikoru klasik CREST sendromunun (sınırlı skleroderma) damgasıdır.",
                    "B": "Yanlış; diffüz form gövdeyi tutar ve Anti-Scl-70 ile ilişkilidir.",
                    "C": "Yanlış; SLE'de sentromer antikoru beklenmez.",
                    "D": "Yanlış; dermatomiyozitte anti-Jo-1 ve heliotrop raş vardır.",
                    "E": "Yanlış; bu aksiyel artrittir."
                }
            )
        ]
    })

    # Slayt 55: CREST Sendromu Bileşenleri ve Organ Morfolojisi
    slides.append({
        "id": "k1-25-s55",
        "title": "CREST Sendromu Bileşenleri ve Organ Morfolojisi",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 55,
        "narrative": (
            "Sınırlı sklerodermanın klinik tablosunu oluşturan beş temel özelliğin baş harfleri **CREST** akronimini oluşturur: "
            "1. **C (Calcinosis):** Subkutan dokularda ve periartiküler alanlarda sert kalsiyum fosfat birikintileri (kalsinozis kutis). "
            "2. **R (Raynaud Fenomeni):** Soğuk veya stresle el parmak arteriyollerinde ani spazm; parmaklar sırasıyla beyaz (iskemi), "
            "mor (siyanoz) ve kırmızı (reperfüzyon) renk alır. Sklerodermanın **en erken ve neredeyse %100 görülen** belirtisidir. "
            "3. **E (Esophageal Dismotility):** Özofagus alt üçte iki düz kas tabakasının atrofisi ve submukozal fibrozis. "
            "Özofagus sert bir lastik boruya döner; gastroözofageal reflü ve katı gıdalara karşı disfaji gelişir. "
            "4. **S (Sclerodactyly):** Parmak derisinin parlak, gergin, kıvrımsız hale gelmesi ve pençe eli (claw-hand) deformitesi. "
            "5. **T (Telangiectasia):** Yüzde, dudaklarda ve parmaklarda genişlemiş kapiller dilatasyon odakları."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "CREST Sendromu Patolojik Bileşenleri",
                ["Harf", "Klinik Özellik", "Histopatolojik Zemin", "Klinik Yansıması"],
                [
                    ["C", "Calcinosis kutis", "Deri altında distrofik kalsiyum nodülleri", "Ağrılı subkutan sert kitleler"],
                    [
                        "R",
                        "Raynaud fenomeni",
                        {"text": "İntimal fibrozis ve paroksismal vazospazm", "isMasked": True, "hint": "Parmak damarlarının soğukta büzüşerek renk değiştirmesi"},
                        "Beyaz-mor-kırmızı parmak atağı"
                    ],
                    ["E", "Esophageal dismotilite", "Muskularis eksterna atrofisi ve kollajenleşme", "Lastik boru özofagus, reflü, disfaji"],
                    ["S", "Sclerodactyly", "Dermal kollajen sıkılaşması, adneks kaybı", "Pençe eli deformitesi ve parmak ülserleri"],
                    ["T", "Telangiectasia", "Genişlemiş ve incelmiş kutanöz kapillerler", "Yüz ve dudakta kırmızı vasküler benekler"]
                ]
            ),
            make_active_recall(
                "Skleroderma hastalarında özofagus muskularis katmanının fibröz dokuyla yer değiştirmesi sonucu gelişen katı gıda yutma güçlüğü ve reflü tablosuna ne ad verilir?",
                "Özofagus dismotilitesi (Lastik boru özofagus) denir.",
                "CREST sendromunun E harfini oluşturan gastrointestinal tutulum"
            )
        ]
    })

    # Slayt 56: Sklerodermada İç Organ Tutulumları ve Ölüm Nedenleri
    slides.append({
        "id": "k1-25-s56",
        "title": "Sklerodermada İç Organ Tutulumları ve Ölüm Nedenleri",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 56,
        "narrative": (
            "Sistemik sklerozda hastaların yaşam beklentisini iç organlardaki mikrovasküler yıkım ve fibrozis belirler: "
            "1. **Akciğer Tutulumu (En Sık Ölüm Nedeni):** "
            "- **İnterstisyel Akciğer Fibrozisi:** Alveol duvarlarında masif kollajen birikimi, diffüz alveolar hasar ve son evrede **bal peteği akciğer** (honeycomb lung). "
            "- **Pulmoner Arteriyel Hipertansiyon:** Pulmoner arteriyollerin intimal fibrozisle tıkanması; sağ kalp yetmezliğine (kor pulmonale) yol açar. "
            "2. **Böbrek Tutulumu (Skleroderma Renal Krizi):** İnterlobüler arter lümeninde düz kas hiperplazisi ve intimal fibrozisle "
            "karakteristik **soğan zarı (onion-skin)** manzarası oluşur. Ani malign hipertansiyon, oligüri ve böbrek yetmezliği gelişir "
            "(ACE inhibitörleri mortaliteyi belirgin azaltmıştır). "
            "3. **Kalp:** Miyokardiyal küçük damar vazospazmlarına bağlı fokal iskemi ve diffüz fibröz skarlar (aritmi ve kalp yetmezliği)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sistemik Skleroz Organ Tutulumları ve Histopatolojik Özellikleri",
                ["Organ", "Histopatolojik Lezyon", "Klinik Sonuç", "Ölümcül Risk Düzeyi"],
                [
                    ["Akciğer", "İnterstisyel fibrozis ve pulmoner arter tıkanması", "Restriktif solunum yetmezliği ve kor pulmonale", "EN SIK ÖLÜM NEDENİ (%50)"],
                    [
                        "Böbrek",
                        "Arteriyollerde soğan zarı (onion-skin) intimal kalınlaşma",
                        {"text": "Skleroderma renal krizi ve malign hipertansiyon", "isMasked": True, "hint": "Ani tansiyon fırlaması ve akut oligürik böbrek yetmezliği tablosu"},
                        "Acil ACE inhibitörü gerektiren mortal kriz"
                    ],
                    ["GİS", "İnce bağırsakta submukozal fibrozis ve divertikül", "Bakteriyel aşırı çoğalma, malabsorpsiyon", "Kilo kaybı ve kaşeksi"],
                    ["Kalp", "Miyokardiyal dağınık fibrozis", "İleti blokları ve aritmiler", "Ani kardiyak ölüm"]
                ]
            ),
            make_active_recall(
                "Sistemik skleroz hastalarında günümüzde en sık ölüm nedeni olan primer visseral organ komplikasyonu hangisidir?",
                "Akciğer tutulumudur (İnterstisyel pulmoner fibrozis ve pulmoner hipertansiyon).",
                "Solunum yetmezliği ve sağ kalp yetmezliği yapan akciğer doku sertleşmesi"
            )
        ]
    })

    # Slayt 57: İnflamatuvar Miyopatiler: Polimiyozit, Dermatomiyozit ve İnklüzyon Cisimcikli Miyozit
    slides.append({
        "id": "k1-25-s57",
        "title": "İnflamatuvar Miyopatiler: Polimiyozit ve Dermatomiyozit",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 57,
        "narrative": (
            "İnflamatuvar miyopatiler, iskelet kaslarının immün aracılı yıkımı ve ilerleyici simetrik proksimal kas güçsüzlüğü ile seyreder: "
            "1. **Polimiyozit (CD8+ CTL Aracılı):** "
            "- **Mekanizma:** Doğrudan **CD8+ sitotoksik T hücreleri** kas liflerini sarar; endomizyuma sızarak kas hücresini deler. "
            "- **Histopatoloji:** İnfiltrat kas liflerinin hemen arasında (**endomizyal**) yerleşir; cilt lezyonu bulunmaz. "
            "2. **Dermatomiyozit (Antikor ve Kompleman Aracılı):** "
            "- **Mekanizma:** Küçük intramusküler kan damarlarına karşı antikor ve kompleman (C5b-9 MAC) çöker; vaskülit ve iskemi gelişir. "
            "- **Histopatoloji:** Kas fasikülü kenarındaki liflerde büzüşme ve atrofi izlenir (**perifasiküler / perimizyal atrofi**). "
            "- **Karakteristik Cilt Bulguları:** Üst göz kapaklarında leylak rengi ödemli **heliotrop raş** ve el parmak eklemleri üzerinde **Gottron papülleri**. "
            "Erişkin dermatomiyozit hastalarının yaklaşık %25'inde **iç organ kanserleri (malignite)** eşlik eder (Paraneoplastik sendrom)!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Polimiyozit vs Dermatomiyozit Histopatolojik Ayrımı",
                "Polimiyozit Patolojisi",
                "CD8+ sitotoksik T hücrelerinin kas liflerinin arasına girdiği ENDOMİZYAL infiltrat ve cilt lezyonunun olmaması",
                "Dermatomiyozit Patolojisi",
                "Kompleman ve antikor aracılı PERİFASİKÜLER atrofi, heliotrop raş, Gottron papülleri ve paraneoplastik kanser riski"
            ),
            make_micro_quiz(
                "Proksimal kas güçsüzlüğü olan bir kadın hastanın göz kapaklarında leylak rengi ödematöz döküntü (heliotrop raş) ve el eklemlerinde eritematöz Gottron papülleri saptanıyor. Bu hastada altta yatan malignite taraması gerektiren öncelikli tanı hangisidir?",
                {
                    "A": "Dermatomiyozit",
                    "B": "İzole Polimiyozit",
                    "C": "Miyastenia Gravis",
                    "D": "Duchenne Musküler Distrofi",
                    "E": "Amyotrofik Lateral Skleroz (ALS)"
                },
                "A",
                {
                    "A": "Doğrudur; heliotrop raş ve Gottron papülleri dermatomiyozite özgüdür ve erişkinde paraneoplastik malignite riski taşır.",
                    "B": "Yanlış; polimiyozitte cilt bulgusu olmaz.",
                    "C": "Yanlış; miyasteniada pitozis vardır fakat heliotrop raş ve Gottron papülü görülmez.",
                    "D": "Yanlış; distrofi genetik distrofin eksikliğidir.",
                    "E": "Yanlış; ALS motor nöron dejenerasyonudur."
                }
            )
        ]
    })

    # Slayt 58: İnflamatuvar Miyopati Otoantikorları: Anti-Jo-1 ve Antisentetaz Sendromu
    slides.append({
        "id": "k1-25-s58",
        "title": "İnflamatuvar Miyopati Otoantikorları ve Antisentetaz Sendromu",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 58,
        "narrative": (
            "İnflamatuvar miyopatilerin tanısında ve klinik alt tiplerinin belirlenmesinde spesifik miyozit otoantikorları kullanılır: "
            "1. **Anti-Jo-1 (Histidil-tRNA Sentetaz Antikoru):** En sık saptanan miyozit spesifik antikordur (%25). "
            "Varlığında klasik **Antisentetaz Sendromu** tablosu ortaya çıkar: "
            "- Şiddetli inflamatuvar miyozit, "
            "- Hızlı ilerleyen interstisyel akciğer hastalığı (akciğer fibrozisi), "
            "- Simetrik non-eroziv artrit, Raynaud fenomeni ve "
            "- Parmak uçlarında fissürler ve sertleşmelerle karakterize **'Tamirci Eli' (Mechanic's hands)** görünümü. "
            "2. **Anti-Mi-2:** Klasik dermatomiyozit ve heliotrop raş ile güçlü ilişkilidir; tedaviye yanıtı mükemmeldir. "
            "3. **Anti-SRP:** Şiddetli nekrotizan miyopati ve tedavi direnciyle ilişkilidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İnflamatuvar Miyopati Otoantikorları ve Klinik Korelasyonları",
                ["Otoantikor", "Hedef İntraselüler Enzim / Protein", "Klinik Sendrom", "Tedavi Yanıtı ve Prognoz"],
                [
                    [
                        "Anti-Jo-1",
                        "Histidil-tRNA sentetaz enzimi",
                        {"text": "Antisentetaz sendromu, tamirci eli, akciğer fibrozisi", "isMasked": True, "hint": "İnterstisyel akciğer tutulumu ve parmak fissürleriyle seyreden sendrom"},
                        "Akciğer tutulumu nedeniyle dikkatli takip gerektirir"
                    ],
                    ["Anti-Mi-2", "Nükleer helikaz proteini", "Klasik heliotrop raşlı dermatomiyozit", "Kortikosteroidlere mükemmel yanıt"],
                    ["Anti-SRP", "Sinyal tanıma partikülü (SRP)", "Akut masif nekrotizan miyopati", "Kortikosteroidlere dirençli, ağır seyir"]
                ]
            ),
            make_active_recall(
                "İnflamatuvar miyozitli bir hastada interstisyel akciğer fibrozisi, parmak uçlarında çatlaklar (tamirci eli) ve artritle seyreden antisentetaz sendromunun primer belirteç antikoru hangisidir?",
                "Anti-Jo-1 (Histidil-tRNA sentetaz) antikorudur.",
                "Miyozit spesifik transfer RNA sentetaz enzim antikoru"
            )
        ]
    })

    # Slayt 59: Checkpoint 6
    slides.append({
        "id": "k1-25-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Sjögren Sendromu, Sistemik Skleroz ve Miyopatiler",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 59,
        "narrative": (
            "Bu altıncı kontrol noktasında, bağ dokusu hastalıklarının kritik patoloji prensiplerini pekiştiriyoruz: "
            "1. **Sjögren Sendromu:** Göz ve ağız kuruluğu (kseroftalmi/kserostomi), Anti-Ro/SSA ve Anti-La/SSB antikorları; "
            "B hücreli MALT lenfoma riski 40 kat artmıştır (fokus skoru >=1). "
            "2. **Sistemik Skleroz:** Endotel hasarı, Th2/TGF-beta ve masif kollajen fibrozisi üçlüsüdür. "
            "3. **Diffüz vs CREST:** Diffüz formda Anti-Scl-70 pozitiftir ve erken akciğer fibrozisi/renal kriz yapar; "
            "CREST sınırlı formunda Anti-Sentromer (ACA) pozitiftir (Calcinosis, Raynaud, Esophagus, Sclerodactyly, Telangiectasia). "
            "4. **Skleroderma Ölüm Nedeni:** En sık akciğer fibrozisi ve pulmoner hipertansiyondur. "
            "5. **Miyopatiler:** Polimiyozit endomizyal CD8+ CTL sitotoksisitesidir; Dermatomiyozit perimizyal atrofi, "
            "heliotrop raş, Gottron papülleri ve paraneoplastik kanser riski ile seyreder (Anti-Jo-1)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s59-1",
                "Sjögren sendromunda ekzokrin bezlerdeki kronik poliklonal lenfosit aktivasyonu zemininde gelişme riski 40 kat artan neoplazi türü nedir?",
                "B hücreli MALT lenfomadır.",
                "Tükürük bezi marjinal sahasından köken alan neoplastik kitle",
                "Sjögren ve MALT Lenfoma"
            ),
            make_flashcard(
                "k1-25-fc-s59-2",
                "Sistemik sklerozda (skleroderma) fibroblast aktivasyonunu ve aşırı kollajen sentezini tetikleyen temel profibrotik sitokin hangisidir?",
                "Transforme edici büyüme faktörü-beta (TGF-beta) molekülüdür.",
                "Matriks birikimini ve miyofibroblast dönüşümünü yöneten sitokin",
                "TGF-beta ve Skleroderma"
            ),
            make_flashcard(
                "k1-25-fc-s59-3",
                "İnflamatuvar miyopatiler arasında iskelet kasında perifasiküler atrofi, yüzde heliotrop döküntü ve malignite birlikteliği gösteren patoloji hangisidir?",
                "Dermatomiyozit hastalığıdır.",
                "Cilt bulguları ve paraneoplastik risk taşıyan kompleman aracılı miyopati",
                "Dermatomiyozit"
            )
        ],
        "interactiveElements": [
            make_table(
                "Romatolojik Bağ Dokusu Hastalıkları Büyük Özet Matrisi",
                ["Hastalık", "Klasik Klinik Triad / Damga", "Tanısal Otoantikor", "En Korkulan Komplikasyon"],
                [
                    ["Sjögren Sendromu", "Kuru göz, kuru ağız, parotis şişmesi", "Anti-Ro (SSA) ve Anti-La (SSB)", "B hücreli MALT lenfoma (%40 kat)"],
                    ["Diffüz Skleroderma", "Gövde derisinde taşlaşma, Raynaud", "Anti-Scl-70 (DNA topoizomeraz I)", "Pulmoner fibrozis, soğan zarı renal kriz"],
                    ["CREST Sendromu", "Calcinosis, Raynaud, Esophagus dismotilitesi", "Anti-Sentromer antikorları (ACA)", "Geç pulmoner arteriyel hipertansiyon"],
                    [
                        "Dermatomiyozit",
                        "Proksimal güçsüzlük, heliotrop raş, Gottron",
                        {"text": "Anti-Jo-1 ve Anti-Mi-2", "isMasked": True, "hint": "Antisentetaz sendromu ve klasik miyozit antikorları"},
                        "Gizli visseral iç organ malignitesi"
                    ],
                    ["Polimiyozit", "İzole endomizyal kas güçsüzlüğü", "Anti-Jo-1 ve Anti-SRP", "Solunum kasları tutulumu ve aspirasyon"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki romatolojik hastalık ve karakteristik otoantikor eşleştirmelerinden hangisi YANLIŞTIR?",
                {
                    "A": "Diffüz Sistemik Skleroz - Anti-DNA topoizomeraz I (Anti-Scl-70)",
                    "B": "Sınırlı Sistemik Skleroz (CREST) - Anti-Sentromer antikoru (ACA)",
                    "C": "Sjögren Sendromu - Anti-Ro (SSA) ve Anti-La (SSB)",
                    "D": "Dermatomiyozit - Anti-Jo-1 (Histidil-tRNA sentetaz)",
                    "E": "Polimiyozit - Anti-dsDNA antikoru"
                },
                "E",
                {
                    "A": "Doğrudur; diffüz skleroderma Anti-Scl-70 ile karakterizedir.",
                    "B": "Doğrudur; CREST sendromunda anti-sentromer pozitiftir.",
                    "C": "Doğrudur; Sjögren Anti-Ro ve Anti-La taşır.",
                    "D": "Doğrudur; miyozitte Anti-Jo-1 pozitiftir.",
                    "E": "YANLIŞTIR; Anti-dsDNA antikoru polimiyozitte DEĞİL, Sistemik Lupus Eritematozustadır (SLE)."
                }
            )
        ]
    })

    # Slayt 60: Bölüm Özeti: Bağ Dokusu Hastalıklarından IgG4, Transplant Reddi ve GVHD'ye Geçiş
    slides.append({
        "id": "k1-25-s60",
        "title": "Bölüm Özeti: IgG4 İlişkili Hastalık, Transplant Reddi ve GVHD'ye Geçiş",
        "section": "Sjögren, Sistemik Skleroz ve Miyopatiler",
        "slideNumber": 60,
        "narrative": (
            "Bağ dokusu ve otoimmün hastalıklar vücudun kendi hücrelerine karşı tolerans kaybının sonuçlarıdır: "
            "1. **IgG4 İlişkili Hastalık:** Son yıllarda tanımlanan, kanda IgG4 artışı, dokuda storiform fibrozis ve "
            "obliteratif flebit ile seyreden, tüm organları tümör benzeri kitlelerle tutabilen yeni bir patolojik antitedir "
            "(Otoimmün pankreatit, Riedel tiroiditi vb.). "
            "2. **Alloimmünite (Transplant Reddi):** Bağışıklık sistemi kendi organları dışındaki allojenik greftleri de yabancı tanır. "
            "Donör organın reddedilmesi (hiperakut, akut hücresel, akut hümoral ve kronik ret) tıp tarihinin en dramatik immünolojik çatışmasıdır. "
            "3. **GVHD Paradoksu:** Kemik iliği naklinde ise tam tersine donör lenfositleri alıcının tüm vücuduna saldırır. "
            "Bölüm 7'de IgG4 ilişkili hastalığı, transplant rejeksiyon patolojisini ve GVHD'yi inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Otoimmüniteden Alloimmüniteye Geçiş",
                "Otoimmün Doku Hasarı (SLE, Skleroderma)",
                "Kendi öz antijenlerine karşı toleransın çökmesi ve otoreaktif T/B hücrelerinin iç organları tahrip etmesi",
                "Alloimmün Transplant Reddi (Rejeksiyon)",
                "Farklı bir bireye ait allojenik dokunun yabancı MHC moleküllerine karşı konak bağışıklık sisteminin saldırısı"
            ),
            make_active_recall(
                "Doku biyopsisinde IgG4 pozitif plazma hücreleri, storiform fibrozis ve obliteratif flebit triadı ile karakterize sistemik fibroinflamatuvar hastalık grubu hangisidir?",
                "IgG4 ilişkili hastalıktır (IgG4-RD).",
                "Otoimmün pankreatit ve Riedel tiroiditini içeren fibroinflamatuvar klinik antite"
            )
        ]
    })

    return slides
