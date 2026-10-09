# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-12-s31",
        "title": "Kortikosteroidlerin Güçlü Anti-İnflamatuar Mekanizması",
        "content": "Kortikosteroidler (prednizolon, deksametazon, hidrokortizon), tıptaki en geniş spektrumlu ve en güçlü anti-inflamatuar ilaç sınıfıdır. Bu muazzam güçlerini enflamasyon kaskadını birden fazla stratejik seviyede aynı anda felç ederek gösterirler:\n\n1. **Fosfolipaz A2 (PLA2) İnhibisyonu:** Sitoplazmik glukokortikoid reseptörüne bağlanan steroidler çekirdeğe geçerek **Anneksin-1 (Lipokortin-1)** proteininin sentezini artırır. Anneksin-1 doğrudan Fosfolipaz A2'yi bloke eder; bu sayede ne prostaglandinler ne de lökotrienler üretilebilir (en tepeden blokaj).\n2. **Genomik Transkripsiyonel Baskılama:** Pro-inflamatuar ana transkripsiyon faktörü olan **NF-κB** ve AP-1'i inhibe ederler. Bu sayede COX-2 enzimi, iNOS enzimi, adezyon molekülleri ve majör inflamatuar sitokinlerin (özellikle **TNF ve IL-1**) gen ekspresyonu kökten durdurulur.\n\nBu çift yönlü kilit mekanizma hem eikozanoid fırtınasını hem de sitokin yanıtını aynı anda söndürür.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kortikosteroidlerin Çift Yönlü İnhibisyon Zinciri",
                [
                    "1. Reseptör Bağlanması: Sitoplazmik glukokortikoid reseptörüne tutunma ve nükleusa göç",
                    "2. Anneksin-1 İndüksiyonu: Fosfolipaz A2'nin bloke edilerek tüm eikozanoidlerin kesilmesi",
                    "3. NF-κB İnhibisyonu: Enflamatuar gen transkripsiyonunun çekirdekte durdurulması",
                    "4. Sitokin/Enzim Çöküşü: TNF, IL-1, COX-2 ve iNOS sentezinin tamamen baskılanması"
                ]
            ),
            make_recall(
                "Kortikosteroidlerin uyarımıyla sentezlenerek Fosfolipaz A2 enzimini doğrudan inhibe eden endojen protein hangisidir?",
                "Anneksin-1'dir (Lipokortin-1).",
                "PLA2 inhibitörü glukokortikoid aracılı protein"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-12-s32",
        "title": "Sitokinlere Genel Bakış: İnflamatuar Haberleşme Ağı",
        "content": "Sitokinler, bağışıklık sistemi hücreleri ile diğer doku hücreleri arasındaki iletişimi sağlayan, hücresel büyüme, farklılaşma ve enflamatuar reaksiyonları yöneten düşük molekül ağırlıklı çözünebilir protein mediyatörlerdir. Sitokin biyolojisinin temel ilkeleri:\n\n- **Etki Mesafeleri:** Çoğunlukla salgılandıkları hücrenin hemen yanındaki komşu hücrelere etki ederler (**parakrin etki**) veya salgılayan hücrenin kendi reseptörlerine bağlanırlar (**otokrin etki**). Ağır enfeksiyonlarda kana karışarak uzak organlara ve beyne ulaşabilirler (**endokrin etki**).\n- **Pleiotropi ve Redundancy:** Tek bir sitokin birden fazla farklı hücre tipinde çok farklı etkiler oluşturabilir (pleiotropi); buna karşılık birden fazla farklı sitokin aynı biyolojik yanıtı üretebilir (redundancy / fazlalık).\n- **Temel Hücresel Kaynaklar:** Başlıca aktive doku makrofajları, dendritik hücreler ve T lenfositlerdir; endotel ve fibroblastlar da katkıda bulunur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sitokinlerin Etki Tarzları Karşılaştırması",
                "Otokrin ve Parakrin Etki (Fizyolojik)",
                "Lokal enflamasyon odağında salgılanan hücreye ve hemen komşu hücrelere yöneliktir.",
                "Endokrin Etki (Sistemik / Patolojik)",
                "Dolaşıma dökülerek hipotalamus, karaciğer, kemik iliği veya kalpte sistemik yanıt oluşturur."
            ),
            make_cloze(
                "Tek bir sitokinin birden fazla farklı hücre tipinde farklı biyolojik etkiler oluşturabilme yeteneğine pleiotropi adı verilir.",
                "pleiotropi",
                "Sitokinlerin çok yönlü farklı etkiler sergileme özelliği"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-12-s33",
        "title": "Akut Enflamasyonun Majör Sitokinleri: TNF ve İnterlökin-1",
        "content": "Akut enflamasyon yanıtını başlatan ve organize eden iki şef sitokin **Tümör Nekroz Faktörü (TNF)** ve **İnterlökin-1'dir (IL-1)**. Her iki sitokinin de en zengin ve ana hücresel kaynağı aktive olmuş **doku makrofajları ve dendritik hücrelerdir**; mast hücreleri ve endotel de üretime katılır. Üretimlerini tetikleyen temel uyaranlar:\n\n1. **Mikrobiyal Ürünler (PAMP'lar):** Gram-negatif bakteri endotoksini olan **Lipopolisakkarit (LPS)**, bakteriyel peptidoglikanlar ve viral nükleik asitler makrofaj Toll-benzeri reseptörlerini (TLR) uyararak masif TNF ve IL-1 transkripsiyonu başlatır.\n2. **Hasarlı Hücre Molekülleri (DAMP'lar):** Nekrotik hücrelerden ortama saçılan ürik asit kristalleri, ATP ve HMGB1 proteinleri hücre içi **NLRP3 inflamazomunu** aktive ederek prokaspaz-1 üzerinden pro-IL-1'i aktif **IL-1β** formuna dönüştürür.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Akut enflamasyonda endotel aktivasyonunu başlatan, karaciğerde akut faz yanıtını uyaran ve ateşe yol açan iki majör şef sitokin hangisidir?",
                [
                    {"key": "A", "text": "Tümör Nekroz Faktörü (TNF) ve İnterlökin-1 (IL-1)", "explanation": "A seçeneği DOĞRUDUR: TNF ve IL-1 akut enflamasyonun lokal ve sistemik organizasyonundan sorumlu iki ana sitokindir."},
                    {"key": "B", "text": "İnterlökin-4 (IL-4) ve İnterlökin-13 (IL-13)", "explanation": "B seçeneği yanlıştır: Bunlar Tip 2 Th2 alerji ve onarım sitokinleridir."},
                    {"key": "C", "text": "İnterferon-gama (IFN-γ) ve İnterlökin-12", "explanation": "C seçeneği yanlıştır: Kronik hücresel granülomatöz yanıt sitokinleridir."},
                    {"key": "D", "text": "İnterlökin-10 ve TGF-beta", "explanation": "D seçeneği yanlıştır: Anti-inflamatuar sitokinlerdir."},
                    {"key": "E", "text": "Eritropoietin ve Trombopoietin", "explanation": "E seçeneği yanlıştır: Hematopoietik büyüme faktörleridir."}
                ],
                "A"
            ),
            make_recall(
                "Makrofajlarda inaktif pro-IL-1β molekülünü keserek aktif sekrete edilen IL-1β formuna dönüştüren intraselüler multimerik protein kompleksi nedir?",
                "NLRP3 inflamazomudur (inflammasome).",
                "Kaspaz-1'i aktive eden sitozolik patojen sensör kompleksi"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-12-s34",
        "title": "TNF ve IL-1'in Lokal Endotelyal Etkileri ve Adezyon Molekülleri",
        "content": "Enflamasyon odağındaki lokal mikrodolaşımda TNF ve IL-1'in en kritik hedefi vasküler endotel hücreleridir. Bu iki sitokin 'endotel aktivasyonu' adı verilen köklü bir fenotipik dönüşüm başlatır:\n\n1. **Adezyon Moleküllerinin İndüksiyonu:** Endotel yüzeyinde lökosit yuvarlanmasını sağlayan **E-selektin** ekspresyonunu hızla artırırlar. Eş zamanlı olarak lökositlerin sıkı tutunmasını sağlayan integrin ligandları olan **ICAM-1 (İntraselüler Adezyon Molekülü-1)** ve **VCAM-1 (Vasküler Hücre Adezyon Molekülü-1)** sentezini transkripsiyonel olarak uyarırlar.\n2. **Kemokin Salgılanması:** Endotelden IL-8 (CXCL8) salınımını tetikleyerek lökositleri dokuya davet ederler.\n3. **Prokoagülan Duruma Geçiş:** Endotelin normal antitrombotik yüzeyini baskılarlar; doku faktörü ekspresyonunu artırıp trombomodülini azaltarak lokal damar içi fibrin pıhtılaşmasını teşvik ederler; bu sayede mikropların kan dolaşımına yayılması lokal bir fibrin barikatıyla hapsedilir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Endotelyal Değişiklik", "Moleküler Aracı", "Enflamatuar Fonksiyon"],
                [
                    [
                        {"text": "Yuvarlanma Reseptörü", "isMasked": False, "hint": ""},
                        {"text": "E-selektin ekspresyonu", "isMasked": True, "hint": "Lökositlerin endotelde yavaşlamasını sağlayan molekül"},
                        {"text": "Lökosit marjinasyonu ve yuvarlanması", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Sıkı Adezyon Ligandları", "isMasked": False, "hint": ""},
                        {"text": "ICAM-1 ve VCAM-1 artışı", "isMasked": True, "hint": "Lökosit integrinlerine kenetlenen ligandlar"},
                        {"text": "Lökositlerin durması ve yapışması", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Koagülasyon Dengesi", "isMasked": False, "hint": ""},
                        {"text": "Doku faktörü artışı, trombomodülin azalışı", "isMasked": True, "hint": "Trombotik yöne kayış"},
                        {"text": "Lokal mikrodamar trombozu ile bariyer oluşturma", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "TNF ve IL-1 endotel yüzeyinde integrin ligandları olan ICAM-1 ve VCAM-1 ekspresyonunu artırarak lökosit adezyonunu sağlar.",
                "ICAM-1 ve VCAM-1",
                "İki majör endotelyal integrin ligandı kısaltması"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-12-s35",
        "title": "Sistemik Koruyucu Akut Faz Yanıtı: Hipotalamik Ateş Mekanizması",
        "content": "Enflamasyon şiddetli olduğunda lokal dokudan kana sızan TNF, IL-1 ve IL-6, dolaşım yoluyla santral sinir sistemine ulaşarak sistemik bir savunma programı başlatır. Bu yanıtın en belirgin klinik yansıması **ateştir (febris)**:\n\n- **Hipotalamik Termostat Ayarı:** Sitokinler, kan-beyin bariyerinin geçirgen olduğu üçüncü ventrikül tabanındaki vasküler organum vazkulosum lamina terminalis (OVLT) endotelini uyarır.\n- **Lokal COX-2 ve PGE2 Patlaması:** Endotelde COX-2 enzimi indüklenir ve hızla **Prostaglandin E2 (PGE2)** sentezlenir.\n- **Set-Point Yükselmesi:** PGE2, anterior hipotalamusun preoptik alanındaki nöronal EP3 reseptörlerine bağlanır; termostat ayar noktasını örneğin 37°C'den 39°C'ye yükseltir.\n- **Isı Koruma Davranışı:** Vücut kendini üşüyor hisseder; vazomotor merkez periferik damarları büzer (solukluk), titreme (ürperme) ile ısı üretir ve vücut sıcaklığı yükselir. Yüksek vücut ısısı mikroorganizmaların replikasyonunu yavaşlatır ve lökosit aktivitesini optimize eder.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Enflamasyonda Ateş Oluşum Mekanizması",
                [
                    "1. Sitokin Salınımı: Makrofajlardan kana TNF ve IL-1 dökülmesi",
                    "2. Hipotalamik Endotel Uyarımı: OVLT bölgesinde COX-2 indüksiyonu",
                    "3. PGE2 Sentezi: Hipotalamik preoptik alanda lokal PGE2 üretimi",
                    "4. Termostat Yükselmesi ve Titreme: Set-point artışı ile periferik vazokonstriksiyon ve titreme"
                ]
            ),
            make_recall(
                "İnflamatuar sitokinlerin etkisiyle hipotalamusta sentezlenerek vücut ısı ayar noktasını yukarı çeken temel mediyatör hangisidir?",
                "Prostaglandin E2'dir (PGE2).",
                "Ateşin santral kimyasal yöneticisi"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-12-s36",
        "title": "Karaciğerde Akut Faz Proteinleri Sentezi: IL-6, CRP, SAA ve Fibrinojen",
        "content": "Sistemik akut faz yanıtının karaciğerdeki orkestra şefi **İnterlökin-6'dır (IL-6)** (üretimi bizzat TNF ve IL-1 tarafından uyarılır). Dolaşımdaki IL-6 hepatosit yüzeyindeki reseptörlerine bağlanarak STAT3 transkripsiyon yolağını aktive eder. Karaciğer normal albümin sentezini kısarak plazmaya yüksek miktarlarda **Akut Faz Proteinleri (APP)** pompalar:\n\n1. **C-Reaktif Protein (CRP):** Bakteri duvarındaki fosfokoline bağlanır; mikrobu opsonize eder ve klasik kompleman kaskadını (C1q) tetikler. Kandaki düzeyi inflamasyonun şiddetiyle yüzlerce kat artar.\n2. **Serum Amiloid A (SAA):** Bakteriyel lipidleri bağlar ve enflamatuar hücreleri temizler. Kronik enflamasyonda sürekli yüksek kalması amiloid fibrillerine (AA amiloidozu) dönüşerek böbrek yetmezliği yapabilir.\n3. **Fibrinojen:** Pıhtılaşma faktörüdür; eritrositlerin birbirine yapışıp para yığınları (rulo formasyonu) oluşturmasına yol açar. Bu durum klinik laboratuvarda **Eritrosit Sedimentasyon Hızının (ESR)** belirgin şekilde yükselmesinin fiziksel nedenidir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Akut Faz Proteini", "Primer İndükleyici Sitokin", "Klinik / Laboratuvar Önemi"],
                [
                    [
                        {"text": "C-Reaktif Protein (CRP)", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-6 (IL-6)", "isMasked": True, "hint": "Hepatositleri uyaran majör sitokin"},
                        {"text": "Opsonizasyon; akut inflamasyonun hassas göstergesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Fibrinojen", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-6 (IL-6)", "isMasked": True, "hint": "Karaciğer akut faz uyarımı"},
                        {"text": "Eritrosit rulo oluşumu ve Sedimentasyon (ESR) yüksekliği", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Serum Amiloid A (SAA)", "isMasked": False, "hint": ""},
                        {"text": "IL-1 ve TNF uyarımı", "isMasked": True, "hint": "Monosit kaynaklı diğer iki sitokin"},
                        {"text": "Kronikleştiğinde sekonder AA amiloidoz riski", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Karaciğerden CRP, SAA ve fibrinojen gibi akut faz proteinlerinin sentezini uyaran temel aracı sitokin interlökin altıdır.",
                "interlökin altıdır",
                "IL-6 sitokininin tam adı"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-12-s37",
        "title": "Lökositoz Mekanizması: Kemik İliği Uyarımı ve Sola Kayma",
        "content": "Akut enflamasyonun kardinal sistemik laboratuvar bulgularından biri kanda lökosit sayısının normal sınırların (4.000-10.000 /µL) çok üzerine çıkarak 15.000-20.000 /µL (bazen 40.000-100.000 /µL; lökomoid reaksiyon) seviyelerine ulaşmasıdır (**lökositoz**). Bu sürecin fizyopatolojisi iki aşamada yürür:\n\n1. **Hızlı Rezerv Boşalması:** Enflamasyonun erken saatlerinde salınan TNF ve IL-1, kemik iliğindeki post-mitotik depolama havuzunu uyararak olgun nötrofilleri derhal kana fırlatır.\n2. **Yeni Üretimin Patlaması:** Enflamatuar makrofajlar ve T lenfositler **Koloni Uyarıcı Faktörler (G-CSF ve GM-CSF)** salgılar. Kemik iliğindeki hematopoietik miyeloid öncül hücreler hızla bölünerek nötrofil üretimini katlar.\n\nKemik iliği yüksek nötrofil talebini karşılayabilmek için henüz tam olgunlaşmamış genç, çomak (band) formundaki nötrofilleri erken evrede dolaşıma döker. Periferik yaymada çomak nötrofil oranının artmasına klinik pratikte **'sola kayma (shift to the left)'** adı verilir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Akut bakteriyel enflamasyonda kemik iliğinden genç çomak nötrofillerin erken dolaşıma verilmesi tablosuna sola kayma denir.",
                "sola kayma",
                "İmmatür nötrofillerin kanda artışını simgeleyen klinik deyim"
            ),
            make_recall(
                "Kemik iliğinde hematopoietik kök hücreleri uyararak nötrofil üretimini günlerce artıran temel büyüme faktörü hangisidir?",
                "G-CSF'dir (Granulocyte colony-stimulating factor).",
                "Granülosit koloni uyarıcı faktör kısaltması"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-12-s38",
        "title": "Yüksek Düzey TNF ve IL-1'in Patolojik Etkileri: Septik Şok",
        "content": "Düşük ve orta konsantrasyonlarda koruyucu olan TNF ve IL-1, ağır sistemik enfeksiyonlarda (özellikle Gram-negatif bakteriyemi / sepsis) masif miktarlarda kana döküldüğünde ölümcül patolojik komplikasyonlara yol açar:\n\n1. **Sistemik Vazodilatasyon ve Hipotansiyon:** Aşırı TNF, endotel ve damar düz kasında indüklenebilir Nitrik Oksit Sentazı (iNOS) uyararak kontrolsüz NO üretimine neden olur; tüm periferik damarlar gevşer, sistemik vasküler direnç çöker ve derin hipotansiyon gelişir.\n2. **Miyokardiyal Depresyon:** Yüksek TNF ve IL-1 kardiyomiyositlerde kalsiyum döngüsünü bozarak kalbin kasılma gücünü (inotropiyi) baskılar; kardiyak debi düşer.\n3. **Yaygın Damar İçi Pıhtılaşma (DIC):** Endotelin tamamen prokoagülan hale gelmesiyle mikrodolaşımda yaygın mikrotrombüsler oluşur, doku perfüzyonu durur ve pıhtılaşma faktörleri tükendiği için ölümcül kanamalar başlar.\n\nBu üçlü çöküş tablosuna **Septik Şok** denir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Patolojik Etki", "Sorumlu Sitokin ve Mekanizma", "Klinik Tablo"],
                [
                    [
                        {"text": "Hipotansiyon / Vasküler Çöküş", "isMasked": False, "hint": ""},
                        {"text": "Aşırı TNF ile iNOS indüksiyonu ve masif NO", "isMasked": True, "hint": "Kontrolsüz vazodilatör gaz patlaması"},
                        {"text": "Dirençli septik hipotansiyon", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Miyokard Fonksiyon Kaybı", "isMasked": False, "hint": ""},
                        {"text": "TNF ve IL-1'in doğrudan kardiyomiyosit depresyonu", "isMasked": True, "hint": "Kalp kası kasılma gücünün baskılanması"},
                        {"text": "Kardiyak debide düşüş", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Mikrovasküler Tromboz", "isMasked": False, "hint": ""},
                        {"text": "Endotelde masif doku faktörü ve antikoagülan kaybı", "isMasked": True, "hint": "Pıhtılaşma sisteminin kontrolsüz aktivasyonu"},
                        {"text": "Dissemine intravasküler koagülasyon (DIC)", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_quiz(
                "Ağır sepsis tablosunda kanda aşırı yükselen TNF düzeylerinin yol açtığı sistemik patolojik etkilerle ilgili hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Sistemik vazodilatasyon, miyokardiyal kontraktilite depresyonu ve yaygın tromboz (DIC)", "explanation": "A seçeneği DOĞRUDUR: Aşırı TNF septik şokta hipotansiyon, kalp yetmezliği ve DIC tablosunu tetikler."},
                    {"key": "B", "text": "Kan basıncının kontrolsüz şekilde 250 mmHg üzerine fırlaması", "explanation": "B seçeneği yanlıştır: Şok tablosunda kan basıncı çöker (hipotansiyon)."},
                    {"key": "C", "text": "Kalp kasının normalden 5 kat daha kuvvetli kasılması", "explanation": "C seçeneği yanlıştır: Miyokard depresyonu gelişir."},
                    {"key": "D", "text": "Tüm periferik damarların aşırı büzüşerek kanamayı sıfırlaması", "explanation": "D seçeneği yanlıştır: Masif vazodilatasyon gelişir."},
                    {"key": "E", "text": "Kandaki tüm lökositlerin tamamen yok olarak kemik iliğinin erimesi", "explanation": "E seçeneği yanlıştır."}
                ],
                "A"
            )
        ]
    })

    # Slide 39 (CHECKPOINT 4)
    slides.append({
        "id": "k1-12-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Akut Enflamasyon Sitokinleri (TNF, IL-1, IL-6) ve Sistemik Yanıtlar",
        "content": "Akut enflamasyon sitokinlerinin temel ilkeleri:\n\n1. **Kortikosteroidler:** Anneksin-1 ile PLA2'yi bloke eder; NF-κB baskılamasıyla TNF, IL-1, COX-2 ve iNOS'u gen düzeyinde susturur.\n2. **Şef Sitokinler:** TNF ve IL-1'dir; makrofaj ve dendritik hücrelerce PAMP (LPS) ve DAMP uyarısıyla salgılanırlar.\n3. **Lokal Endotel Etkisi:** E-selektin, ICAM-1 ve VCAM-1'i artırarak lökosit yuvarlanma ve adezyonunu sağlarlar; prokoagülan fenotip oluştururlar.\n4. **Ateş:** Hipotalamus OVLT endotelinde COX-2 indüksiyonu ve PGE2 senteziyle termostat ayar noktasını yükseltirler.\n5. **Akut Faz Yanıtı:** IL-6 hepatositleri uyararak CRP, fibrinojen (ESR yüksekliği) ve SAA üretimini patlatır.\n6. **Lökositoz:** Kemik iliği rezervini boşaltır ve G-CSF ile yeni üretim yaparak kanda 'sola kayma' oluştururlar.\n7. **Aşırı TNF:** Septik şokta masif vazodilatasyon, miyokard depresyonu ve DIC'e yol açar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Akut faz proteinlerinin (CRP, fibrinojen) hepatositlerde sentezlenmesini doğrudan uyaran en kritik primer sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterlökin-6 (IL-6)", "explanation": "A seçeneği DOĞRUDUR: Karaciğerde akut faz protein sentezini doğrudan indükleyen ana sitokin IL-6'dır."},
                    {"key": "B", "text": "Histamin", "explanation": "B seçeneği yanlıştır: Vazoaktif amindir, hepatositleri uyarmaz."},
                    {"key": "C", "text": "Lökotrien B4", "explanation": "C seçeneği yanlıştır: Nötrofil kemoatraktanıdır."},
                    {"key": "D", "text": "Prostasiklin", "explanation": "D seçeneği yanlıştır: Endotelyal antitrombotiktir."},
                    {"key": "E", "text": "Serotonin", "explanation": "E seçeneği yanlıştır: Trombosit vazokonstriktörüdür."}
                ],
                "A"
            ),
            make_cloze(
                "Yüksek düzey TNF salınımı septik sok tablosunda miyokard kontraktilitesini baskılayarak kardiyak debiyi düsürür.",
                "miyokard kontraktilitesini",
                "Kalp kasının kasılma gücünü ifade eden terim"
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-12-s40",
        "title": "Kronik Enflamasyonda TNF ve IL-1: Kaşeksi ve Metabolik Yıkım",
        "content": "Akut fazın ötesine geçip aylarca veya yıllarca süren kronik enfeksiyonlarda (tüberküloz, osteomiyelit) ve ileri evre malignitelerde, sürekli salgılanan düşük-orta düzey TNF ve IL-1 vücutta ağır bir katabolik tükeniş tablosu yaratır:\n\n1. **Kaşeksi (Kaşektin Etkisi):** TNF tarihsel olarak ilk kez 'kaşektin' adıyla izole edilmiştir. Hipotalamusta iştah merkezini baskılayarak anoreksiya yapar; adipositlerde lipoprotein lipaz enzimini inhibe eder ve trigliserit yıkımını (lipoliz) hızlandırır. İskelet kaslarında protein parçalanmasını (ubikuitin-proteazom yolağı ile) tetikleyerek derin kas ve yağ dokusu erimesine (**kaşeksi**) yol açar.\n2. **İnsülin Direnci:** TNF, insülin reseptör substratı-1'i (IRS-1) serin amino asitlerinden fosforilleyerek insülin sinyalini bozar; kronik hastalarda hiperglisemi ve dokusal insülin direncine neden olur.\n3. **Kronik Hastalık Anemisi:** Hepatositlerden hepsidin salınımını artırarak demiri makrofajlarda hapsederler; eritropoez duraklar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Kronik tüberküloz ve akciğer karsinomu olan bir hastada 6 ay içinde 18 kilo kaybı, aşırı kas erimesi, iştahsızlık ve belirgin zayıflama (kaşeksi) tablosu gelişiyor.",
                "Bu derin katabolik tükeniş tablosundan (kaşeksi) sorumlu temel sitokin ve tarihsel adı nedir?",
                [
                    {
                        "text": "Tümör Nekroz Faktörüdür (TNF); tarihsel adıyla 'kaşektin' olarak bilinir ve lipoliz ile kas yıkımını tetikler.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. TNF hipotalamik anoreksi, adipoz lipoliz ve kas proteolizini uyararak kaşeksiye yol açar."
                    },
                    {
                        "text": "İnterlökin-10'dur; hastanın tüm yağ hücrelerini kemiğe dönüştürür.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. IL-10 anti-inflamatuardır, kaşeksi yapmaz."
                    },
                    {
                        "text": "Histamindir; mide asidini sıfırlayarak kilo kaybı yapar.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Kaşeksinin sorumlusu histamin değil TNF'dir."
                    }
                ]
            ),
            make_recall(
                "Kronik hastalıklarda iştahsızlık, lipoliz ve kas yıkımı yaparak kaşeksiye yol açtığı için tarihsel olarak 'kaşektin' adıyla bilinen sitokin nedir?",
                "Tümör Nekroz Faktörüdür (TNF).",
                "Kaşeksi sitokininin güncel adı"
            )
        ]
    })

    return slides
