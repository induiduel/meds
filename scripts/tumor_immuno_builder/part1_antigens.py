# -*- coding: utf-8 -*-
"""
Part 1: Tümör İmmünolojisine Giriş ve Tümör Antijenleri (Slayt 1 - 6)
Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde.
"""

slides_part1 = [
    # SLIDE 1
    {
        "slideNumber": 1,
        "title": "Tümör İmmünolojisine Giriş ve İmmün Gözetim (Immune Surveillance)",
        "subtitle": "Burnet-Thomas hipotezi, immünosüpresyonda neoplazi insidansı ve TIL prognostik değeri",
        "badge": "İmmün Gözetim",
        "badgeColor": "emerald",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser gelişimi sadece genetik mutasyonların bir sonucu değildir; bağışıklık sisteminin gözetim ağından bir kaçış öyküsüdür. İmmün yetmezlikli bireylerde neoplazi patlaması bu dengenin en somut kanıtıdır.",
            "note": "Prof. Dr. Hikmet Keleş, amfide immün gözetim kavramının immünoonkolojinin temel taşı olduğunu ve komite sınavlarında klinik korelasyonlarla sıkça sorgulandığını vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### İmmün Gözetim Hipotezi ve Neoplazi Dengesi\n"
            "Tümör immünolojisinin temel dayanağı, Macfarlane Burnet ve Lewis Thomas tarafından ortaya atılan **İmmün Gözetim "
            "(Immune Surveillance)** hipotezidir. Organizmanın normal hücre döngüsü sırasında sürekli olarak DNA hasarına uğramış ve "
            "transformasyon gösteren atipik hücreler ortaya çıkar. Sağlıklı bir bağışıklık sistemi, bu neoplastik klonları klinik bir "
            "kitleye dönüşmeden önce saptar ve elimine eder. Dolayısıyla kanser gelişimi, proto-onkogen aktivasyonu ve tümör baskılayıcı gen "
            "inaktivasyonunun ötesinde, transformasyona uğramış hücrelerin konağın immün savunmasını aşmasıyla mümkündür.\n\n"
            "### İmmün Yetmezlik Zemininde Artan Malignite Riski\n"
            "İmmün gözetimin en güçlü klinik kanıtı immünsüpresif popülasyonlardır. Konjenital immün yetmezlikler (SCID, Wiskott-Aldrich), "
            "HIV/AIDS ve organ nakli sonrası ömür boyu kalsinörin inhibitörü (siklosporin, takrolimus) kullanan bireylerde kanser "
            "insidansı onlarca kat artar. Bu hastalarda özellikle onkojenik virüs ilişkili neoplaziler başı çeker: EBV ilişkili lenfoproliferatif "
            "hastalıklar (PTLD) ve lenfomalar, KSHV/HHV-8 ilişkili Kaposi sarkomu ve HPV ilişkili anogenital karsinomlar. Hücresel "
            "bağışıklığın çökmesi, viral onkoprotein taşıyan klonların kontrolsüzce çoğalmasına zemin hazırlar.\n\n"
            "### Tümör İnfiltre Eden Lenfositler (TIL) ve Prognostik İmmünoskor\n"
            "Malign tümörlerde tümör parankimi ve stromasındaki **Tümör İnfiltre Eden Lenfositler (TIL)** hayati prognostik öneme sahiptir. "
            "Kolorektal karsinom, malign melanom ve meme kanserinde yoğun CD8+ sitotoksik T lenfosit (CTL) infiltrasyonu saptanması, "
            "nüks riskinin azaldığını ve genel sağkalımın uzadığını gösteren bağımsız bir İYİ PROGNOZ kriteridir. Günümüzde TNM evrelemesini "
            "destekleyen 'İmmünoskor' (Immunoscore) sistemi, tümör merkezi ve invazyon cephesindeki CD3+/CD8+ lenfosit yoğunluğunu "
            "ölçerek hastaların tedavi yanıtını ve klinik gidişatını başarıyla öngörmektedir.\n\n"
            "🔴 **ÖNEMLİ:** İmmünosüpresif hastalarda ve organ nakli alıcılarında en sık ortaya çıkan maligniteler onkojenik virüslerle "
            "(EBV, HHV-8, HPV) ilişkilidir; hücresel bağışıklığın çökmesi viral onkoproteinlerin kontrolsüz proliferasyonuna yol açar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Malign bir solid tümörün histopatolojik incelemesinde yoğun CD8+ sitotoksik T lenfosit (TIL) "
            "infiltrasyonu saptanması, klinik gidişatta artmış genel sağkalım ve bağımsız İYİ PROGNOZ ile ilişkilidir."
        ),
        "content": (
            "### İmmün Gözetim Hipotezi ve Neoplazi Dengesi\n"
            "Tümör immünolojisinin temel dayanağı, Macfarlane Burnet ve Lewis Thomas tarafından ortaya atılan **İmmün Gözetim "
            "(Immune Surveillance)** hipotezidir. Organizmanın normal hücre döngüsü sırasında sürekli olarak DNA hasarına uğramış ve "
            "transformasyon gösteren atipik hücreler ortaya çıkar. Sağlıklı bir bağışıklık sistemi, bu neoplastik klonları klinik bir "
            "kitleye dönüşmeden önce saptar ve elimine eder. Dolayısıyla kanser gelişimi, proto-onkogen aktivasyonu ve tümör baskılayıcı gen "
            "inaktivasyonunun ötesinde, transformasyona uğramış hücrelerin konağın immün savunmasını aşmasıyla mümkündür.\n\n"
            "### İmmün Yetmezlik Zemininde Artan Malignite Riski\n"
            "İmmün gözetimin en güçlü klinik kanıtı immünsüpresif popülasyonlardır. Konjenital immün yetmezlikler (SCID, Wiskott-Aldrich), "
            "HIV/AIDS ve organ nakli sonrası ömür boyu kalsinörin inhibitörü (siklosporin, takrolimus) kullanan bireylerde kanser "
            "insidansı onlarca kat artar. Bu hastalarda özellikle onkojenik virüs ilişkili neoplaziler başı çeker: EBV ilişkili lenfoproliferatif "
            "hastalıklar (PTLD) ve lenfomalar, KSHV/HHV-8 ilişkili Kaposi sarkomu ve HPV ilişkili anogenital karsinomlar. Hücresel "
            "bağışıklığın çökmesi, viral onkoprotein taşıyan klonların kontrolsüzce çoğalmasına zemin hazırlar.\n\n"
            "### Tümör İnfiltre Eden Lenfositler (TIL) ve Prognostik İmmünoskor\n"
            "Malign tümörlerde tümör parankimi ve stromasındaki **Tümör İnfiltre Eden Lenfositler (TIL)** hayati prognostik öneme sahiptir. "
            "Kolorektal karsinom, malign melanom ve meme kanserinde yoğun CD8+ sitotoksik T lenfosit (CTL) infiltrasyonu saptanması, "
            "nüks riskinin azaldığını ve genel sağkalımın uzadığını gösteren bağımsız bir İYİ PROGNOZ kriteridir. Günümüzde TNM evrelemesini "
            "destekleyen 'İmmünoskor' (Immunoscore) sistemi, tümör merkezi ve invazyon cephesindeki CD3+/CD8+ lenfosit yoğunluğunu "
            "ölçerek hastaların tedavi yanıtını ve klinik gidişatını başarıyla öngörmektedir.\n\n"
            "🔴 **ÖNEMLİ:** İmmünosüpresif hastalarda ve organ nakli alıcılarında en sık ortaya çıkan maligniteler onkojenik virüslerle "
            "(EBV, HHV-8, HPV) ilişkilidir; hücresel bağışıklığın çökmesi viral onkoproteinlerin kontrolsüz proliferasyonuna yol açar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Malign bir solid tümörün histopatolojik incelemesinde yoğun CD8+ sitotoksik T lenfosit (TIL) "
            "infiltrasyonu saptanması, klinik gidişatta artmış genel sağkalım ve bağımsız İYİ PROGNOZ ile ilişkilidir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** İmmünosüpresif hastalarda kanser insidansı katlanarak artar; özellikle EBV, HHV-8 ve HPV gibi onkojenik virüs ilişkili maligniteler başı çeker.",
            "🔵 **ÇIKMIŞ SORU:** Tümör dokusunda yoğun CD8+ sitotoksik T lenfosit (TIL) infiltrasyonu varlığı, kolorektal kanser ve melanomda bağımsız bir İYİ PROGNOZ göstergesidir.",
            "⚡ **KLİNİK:** İmmünoskor sistemi, tümör merkezindeki ve periferik invazyon cephesindeki CD3/CD8 lenfosit yoğunluğuna göre TNM evrelemesine eşlik eden güçlü bir sağkalım belirtecidir."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** İmmün gözetim (Burnet-Thomas) hipotezi, neoplazilerin bağışıklık sisteminden kaçış yeteneği kazandığında klinik hastalık oluşturduğunu kanıtlar.",
            "🔵 **ÇIKMIŞ SORU:** Organ transplantasyonu sonrası immünsüpresif tedavi alan bireylerde gelişen en yaygın maligniteler EBV ilişkili lenfoproliferatif bozukluklardır.",
            "⚡ **KLİNİK:** Yüksek TIL varlığı, hastanın endojen bir antitümöral yanıt ürettiğini gösterir ve checkpoint inhibitör tedavilerine yüksek yanıtı öngörür."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "İmmün Gözetim Paradigması",
                    "desc": "Bağışıklık sisteminin transforme olmuş atipik hücreleri erken dönemde tanıyıp yok etme fizyolojik yeteneğidir.",
                    "isKey": True
                },
                {
                    "title": "İmmünsüpresyonda Onkojenik Virüs Patlaması",
                    "desc": "Transplant alıcılarında ve AIDS'te EBV, HHV-8 ve HPV kaynaklı maligniteler dramatik şekilde artar.",
                    "isKey": True
                },
                {
                    "title": "Tümör İnfiltre Eden Lenfositler (TIL)",
                    "desc": "Tümör dokusuna sızan CD8+ CTL yoğunluğu bağımsız iyi prognoz kriteri olup İmmünoskor hesabında kullanılır.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "İmmün Yeterlilik vs İmmün Yetmezlik Durumunda Neoplazi Dinamiği",
                "headers": ["İmmünolojik Durum", "Baskın Hücresel Yanıt", "Malignite Riski ve Karakteristiği", "Klinik Seyir ve Prognoz"],
                "rows": [
                    ["İmmün Yetkin Birey", "Aktif CD8+ CTL, Th1 ve NK gözetimi", "Düşük mutasyonlu transforme klonlar erkenden elimine edilir", "Tümör gelişirse yoğun TIL ile iyi prognoz"],
                    ["Organ Nakli / İmmünsüpresyon", "T hücresi baskılanmış (kalsinörin inh.)", "EBV lenfomaları (PTLD), HHV-8 Kaposi sarkomu riski yüksek", "Agresif seyir, immünsüpresyon azaltılınca gerileyebilir"],
                    ["İleri Evre HIV / AIDS", "CD4+ T hücre tükenmesi (<200/uL)", "Serviks karsinomu (HPV), MSS lenfoması (EBV), Kaposi sarkomu", "Yüksek mortalite, antiretroviral tedavi ile kısmi toparlanma"],
                    ["Genetik İmmün Yetmezlik", "T ve/veya B hücre defekti (SCID, Wiskott)", "Çocukluk çağında lösemi ve lenfoma insidansında belirgin artış", "Kök hücre nakli gerektiren ağır klinik tablo"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-01-01",
                "category": "İmmün Gözetim",
                "front": "Macfarlane Burnet ve Lewis Thomas tarafından ortaya atılan 'İmmün Gözetim' kavramının patofizyolojik özü nedir?",
                "hint": "Transforme olmuş neoplastik klonların henüz kitle yapmadan yok edilmesi.",
                "back": "Bağışıklık sisteminin vücutta sürekli beliren mutasyonlu ve atipik hücreleri tanıyarak klinik tümör oluşmadan elimine etmesi sürecidir.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu teorinin modern immünoonkolojinin temelini oluşturduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-01-02",
                "category": "Prognostik Belirteçler",
                "front": "Kolorektal kanser ve malign melanomda tümör dokusunda yoğun CD8+ TIL saptanmasının klinik önemi nedir?",
                "hint": "Hastalığın sağkalım süresi üzerindeki etkisi.",
                "back": "Bağımsız bir İYİ PROGNOZ kriteridir; nüks riskinin azaldığını ve genel sağkalımın belirgin olarak uzadığını gösterir.",
                "facultyNote": "TUS ve komite sınavlarında 'TIL varlığı prognozu nasıl etkiler?' kalıbı klasik bir sorudur."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-01",
            "question": "Böbrek transplantasyonu nedeniyle 6 yıldır siklosporin ve mikofenolat mofetil tedavisi almakta olan 48 yaşındaki bir erkek hastada servikal lenfadenopati gelişiyor. Biyopside EBV-pozitif Diffüz Büyük B Hücreli Lenfoma tanısı konuyor. Bu hastada malignite gelişiminin patogenetik mekanizması ve tümör immünolojisi prensipleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) İmmünsüpresif tedavi gören transplant hastalarında karsinogenez riski sadece kimyasal karsinojenlerin birikimine bağlıdır.",
                "B) İmmün yetmezlik zemininde gelişen malignitelerin ezici çoğunluğu onkojenik virüslerle (EBV, HHV-8, HPV) ilişkilidir.",
                "C) Tümör dokusunda yoğun CD8+ sitotoksik T lenfosit infiltrasyonu (TIL) bulunması daima kötü prognoz işaretidir.",
                "D) Kalsinörin inhibitörleri tümör antijenlerinin hücre yüzeyindeki neoantijen yükünü doğrudan artırarak mutasyon yapar.",
                "E) Sağlıklı bireylerde immün gözetim yalnızca hümoral B hücre antikorları aracılığıyla yürütülür, T hücrelerinin rolü yoktur."
            ],
            "answer": "B",
            "explanation": "İmmün yetmezlik durumlarında (organ nakli alıcıları, AIDS vb.) ortaya çıkan neoplazilerin en karakteristik özelliği, büyük çoğunluğunun onkojenik virüsler (özellikle EBV, HHV-8 ve HPV) tarafından indüklenmesidir. Sağlıklı bireylerde hücresel immünite (özellikle CD8+ T hücreleri) viral protein eksprese eden hücreleri sürekli denetim altında tutar; hücresel bağışıklık çöktüğünde bu viral onkogenler kontrolsüz proliferasyonu tetikler. Tümör dokusunda CD8+ TIL varlığı kötü değil, bağımsız İYİ PROGNOZ kriteridir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 2
    {
        "slideNumber": 2,
        "title": "Neoantijenler ve Tümör Mutasyon Yükü (TMB)",
        "subtitle": "Somatik mutasyonlar sonucu oluşan tümöre özgü antijenler (TSA) ve kontrol noktası yanıtı",
        "badge": "Tümör Antijenleri",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Neoantijenler immün sistemin daha önce hiç görmediği, öz-tolerans bariyerine takılmayan saf yabancı antijenlerdir. Mutasyon yükü ne kadar yüksekse, bağışıklık sisteminin hedef alabileceği neoantijen sayısı o kadar katlanır.",
            "note": "Prof. Dr. Hikmet Keleş, mikrosatellit instabilitesi (MSI-H) ve sigara/UV ilişkili kanserlerdeki yüksek mutasyon yükünün modern immünoterapiye yanıtın anahtarı olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Neoantijenlerin Biyolojik Doğası ve Tümöre Özgü Antijenler (TSA)\n"
            "Tümör antijenleri içerisinde immünolojik yanıtı en güçlü tetikleyen grup **Neoantijenler** (Tümöre Özgü Antijenler - TSA) "
            "olarak tanımlanır. Neoantijenler, normal insan genomunda bulunmayan; malign transformasyon sürecinde tümör hücresinde oluşan "
            "somatik missense mutasyonlar, çerçeve kayması (frameshift) insersiyon/delesyonları ve gen füzyonları sonucunda sentezlenen "
            "anormal peptit dizileridir. Normal konak hücrelerinde bu diziler asla bulunmadığı için, gelişmekte olan T lenfositleri timusta "
            "negatif seleksiyon sırasında bu antijenlerle karşılaşmamıştır. Bu durumun en kritik sonucu şudur: **Neoantijenlere karşı "
            "merkezi veya periferik öz-tolerans (self-tolerance) gelişmemiştir!** Bağışıklık sistemi neoantijenleri tıpkı viral veya "
            "bakteriyel bir protein gibi mutlak 'yabancı (non-self)' kabul ederek kuvvetli bir CD8+ CTL yanıtı üretir.\n\n"
            "### Tümör Mutasyon Yükü (TMB) ve DNA Onarım Kusurları\n"
            "Tümör Mutasyon Yükü (TMB), megabaz (Mb) başına düşen somatik mutasyon sayısını gösterir ve tümörler arasında belirgin "
            "farklılık sergiler:\n"
            "1. **Çevresel Karsinojen Kaynaklı Tümörler:** Tütün karsinojenlerine maruz kalan Akciğer Karsinomları ile ultraviyole (UV) "
            "hasarına bağlı Kutanöz Malign Melanom en yüksek mutasyon yüküne sahiptir. UV radyasyonunun oluşturduğu 'C>T dipirimidin' "
            "geçiş mutasyonları binlerce yeni neoantijen yaratır.\n"
            "2. **DNA Onarım Kusurları (MSI-H / dMMR):** DNA Uyumsuzluk Onarımı (Mismatch Repair - MMR; MLH1, MSH2, MSH6, PMS2) "
            "proteinlerini kaybeden kolorektal ve endometriyal karsinomlarda **Mikrosatellit İnstabilitesi (MSI-H)** gelişir. "
            "Oluşan yüzlerce çerçeve kayması mutasyonu, hücre zarında devasa bir neoantijen havuzu meydana getirir.\n\n"
            "### Kontrol Noktası Blokajına (Anti-PD-1) Yanıt Korelasyonu\n"
            "Yüksek neoantijen taşıyan (TMB-high veya MSI-H) tümörler, etraflarında hazır bekleyen ancak kontrol noktalarıyla "
            "frenlenmiş çok sayıda tümöre özgü T hücresine sahiptir. Bu hastalara Anti-PD-1 (Pembrolizumab, Nivolumab) verildiğinde "
            "T hücreleri hızla tümör hücrelerini lize ederek küratif remisyonlar sağlar. Buna karşın mutasyon yükü çok düşük pediatrik "
            "tümörler veya pankreas karsinomu immün kontrol noktası tedavilerine dirençlidir.\n\n"
            "🔴 **ÖNEMLİ:** Neoantijenler somatik mutasyonlarla oluştukları için öz-tolerans engeline takılmazlar; mutasyon yükü yüksek "
            "olan (MSI-H, melanom, tütün ilişkili akciğer Ca) tümörler immünoterapiye en iyi yanıtı verir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Mikrosatellit instabilitesi (MSI-H) ve MMR eksikliği olan kolorektal karsinomların Anti-PD-1 "
            "tedavisine dramatik yanıt vermesinin temel nedeni nedir? "
            "Cevap: Frameshift mutasyonları nedeniyle çok yüksek düzeyde immünojenik neoantijen üretmeleridir."
        ),
        "content": (
            "### Neoantijenlerin Biyolojik Doğası ve Tümöre Özgü Antijenler (TSA)\n"
            "Tümör antijenleri içerisinde immünolojik yanıtı en güçlü tetikleyen grup **Neoantijenler** (Tümöre Özgü Antijenler - TSA) "
            "olarak tanımlanır. Neoantijenler, normal insan genomunda bulunmayan; malign transformasyon sürecinde tümör hücresinde oluşan "
            "somatik missense mutasyonlar, çerçeve kayması (frameshift) insersiyon/delesyonları ve gen füzyonları sonucunda sentezlenen "
            "anormal peptit dizileridir. Normal konak hücrelerinde bu diziler asla bulunmadığı için, gelişmekte olan T lenfositleri timusta "
            "negatif seleksiyon sırasında bu antijenlerle karşılaşmamıştır. Bu durumun en kritik sonucu şudur: **Neoantijenlere karşı "
            "merkezi veya periferik öz-tolerans (self-tolerance) gelişmemiştir!** Bağışıklık sistemi neoantijenleri tıpkı viral veya "
            "bakteriyel bir protein gibi mutlak 'yabancı (non-self)' kabul ederek kuvvetli bir CD8+ CTL yanıtı üretir.\n\n"
            "### Tümör Mutasyon Yükü (TMB) ve DNA Onarım Kusurları\n"
            "Tümör Mutasyon Yükü (TMB), megabaz (Mb) başına düşen somatik mutasyon sayısını gösterir ve tümörler arasında belirgin "
            "farklılık sergiler:\n"
            "1. **Çevresel Karsinojen Kaynaklı Tümörler:** Tütün karsinojenlerine maruz kalan Akciğer Karsinomları ile ultraviyole (UV) "
            "hasarına bağlı Kutanöz Malign Melanom en yüksek mutasyon yüküne sahiptir. UV radyasyonunun oluşturduğu 'C>T dipirimidin' "
            "geçiş mutasyonları binlerce yeni neoantijen yaratır.\n"
            "2. **DNA Onarım Kusurları (MSI-H / dMMR):** DNA Uyumsuzluk Onarımı (Mismatch Repair - MMR; MLH1, MSH2, MSH6, PMS2) "
            "proteinlerini kaybeden kolorektal ve endometriyal karsinomlarda **Mikrosatellit İnstabilitesi (MSI-H)** gelişir. "
            "Oluşan yüzlerce çerçeve kayması mutasyonu, hücre zarında devasa bir neoantijen havuzu meydana getirir.\n\n"
            "### Kontrol Noktası Blokajına (Anti-PD-1) Yanıt Korelasyonu\n"
            "Yüksek neoantijen taşıyan (TMB-high veya MSI-H) tümörler, etraflarında hazır bekleyen ancak kontrol noktalarıyla "
            "frenlenmiş çok sayıda tümöre özgü T hücresine sahiptir. Bu hastalara Anti-PD-1 (Pembrolizumab, Nivolumab) verildiğinde "
            "T hücreleri hızla tümör hücrelerini lize ederek küratif remisyonlar sağlar. Buna karşın mutasyon yükü çok düşük pediatrik "
            "tümörler veya pankreas karsinomu immün kontrol noktası tedavilerine dirençlidir.\n\n"
            "🔴 **ÖNEMLİ:** Neoantijenler somatik mutasyonlarla oluştukları için öz-tolerans engeline takılmazlar; mutasyon yükü yüksek "
            "olan (MSI-H, melanom, tütün ilişkili akciğer Ca) tümörler immünoterapiye en iyi yanıtı verir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Mikrosatellit instabilitesi (MSI-H) ve MMR eksikliği olan kolorektal karsinomların Anti-PD-1 "
            "tedavisine dramatik yanıt vermesinin temel nedeni nedir? "
            "Cevap: Frameshift mutasyonları nedeniyle çok yüksek düzeyde immünojenik neoantijen üretmeleridir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Neoantijenler (TSA), somatik mutasyonlar sonucu üretilen ve konağın öz-tolerans geliştirmediği en güçlü antijenlerdir.",
            "🔵 **ÇIKMIŞ SORU:** MSI-H kolorektal karsinomlar ve UV ilişkili melanomlar, yüksek neoantijen yükleri sayesinde Pembrolizumab/Nivolumab gibi checkpoint inhibitörlerine en yüksek yanıtı verir.",
            "⚡ **KLİNİK:** TMB-high (≥10 mutasyon/Mb) durumu, tümör tipinden bağımsız olarak (agnostik) FDA tarafından Anti-PD-1 endikasyonu olarak onaylanmıştır."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Sürücü (driver) veya yolcu (passenger) mutasyonlar yeni peptit dizileri üreterek neoantijen havuzunu genişletir.",
            "🔵 **ÇIKMIŞ SORU:** DNA Mismatch Repair kusurunda gelişen mikrosatellit instabilitesi, frameshift mutasyonlarıyla bol miktarda yabancı peptit sentezletir.",
            "⚡ **KLİNİK:** Pediatrik lösemi ve retinoblastom gibi mutasyon yükü düşük tümörler immünoterapiye nadiren yanıt verir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Tümöre Özgü Neoantijenler (TSA)",
                    "desc": "Somatik DNA değişiklikleriyle kodlanan, timik toleransı olmayan tamamen yabancı peptit dizileridir.",
                    "isKey": True
                },
                {
                    "title": "TMB ve Çevresel Karsinojenler",
                    "desc": "Sigara (akciğer) ve UV (melanom) hasarı genomda binlerce mutasyon ve zengin neoantijen kaynağı oluşturur.",
                    "isKey": True
                },
                {
                    "title": "MSI-H ve Checkpoint İnhibisyonu",
                    "desc": "DNA tamir kusuru olan tümörlerde neoantijen sıklığı çok yüksektir ve Anti-PD-1 tedavisine mükemmel yanıt verirler.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Tümör Mutasyon Yükü (TMB), Neoantijen Sayısı ve İmmünoterapi Yanıtı",
                "headers": ["Tümör Tipi / Etiyoloji", "Mutasyon Mekanizması", "Neoantijen Düzeyi", "Anti-PD-1 / PD-L1 Yanıtı"],
                "rows": [
                    ["Malign Melanom", "UV radyasyonu (C>T dipirimidin)", "Çok Yüksek (>15 mut/Mb)", "Çok Yüksek (%40-60 objektif yanıt)"],
                    ["Akciğer Karsinomu (Sigara içen)", "Tütün karsinojenleri (benzopirenler)", "Yüksek (>10 mut/Mb)", "Yüksek (özellikle PD-L1 pozitifse)"],
                    ["MSI-H Kolorektal Karsinom", "Mismatch Repair (MMR) kusuru / Lynch", "Çok Yüksek (frameshift zengini)", "Dramatik yanıt (küratif remisyonlar)"],
                    ["Mikrosatellit Stabil (MSS) Kolon Ca", "Kromozomal instabilite (CIN yolağı)", "Düşük (1-3 mut/Mb)", "Dirençli / Etkisiz"],
                    ["Pediatrik Akut Lösemi (ALL)", "Tek tük translokasyonlar", "Çok Düşük (<1 mut/Mb)", "Checkpoint blokajına yanıtsız"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-02-01",
                "category": "Neoantijenler",
                "front": "Neoantijenlerin diğer tümör antijenlerine kıyasla en üstün immünolojik avantajı nedir?",
                "hint": "Timik negatif seleksiyon ve tolerans mekanizmaları.",
                "back": "Normal dokularda bulunmadıkları için konakta bunlara karşı merkezi veya periferik öz-tolerans (self-tolerance) GELİŞMEMİŞTİR; mutlak yabancı kabul edilirler.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide toleranssızlığın güçlü immünitenin anahtarı olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-02-02",
                "category": "Klinik Onkoloji",
                "front": "Mikrosatellit instabilitesi (MSI-H) gösteren karsinomların checkpoint inhibitörlerine dramatik yanıt vermesinin sebebi nedir?",
                "hint": "MMR kusuru ve frameshift mutasyonları.",
                "back": "MMR enzimlerinin kaybı sonucu oluşan çerçeve kayması (frameshift) mutasyonlarının devasa miktarda immünojenik neoantijen üretmesidir.",
                "facultyNote": "FDA'nın doku-agnostik ilk onayı MSI-H tümörlerde Pembrolizumab kullanımıdır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-02",
            "question": "Metastatik kolorektal karsinom tanısı alan 54 yaşındaki bir kadın hastanın tümör dokusu moleküler genetik analizinde MLH1 ekspresyon kaybı ve yüksek düzeyde mikrosatellit instabilitesi (MSI-H) saptanmıştır. Bu hastanın immünolojik profili ve immünoterapiye yanıtı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Tümör mutasyon yükü çok düşük olduğu için bağışıklık sistemi bu hücreleri tanıyamaz.",
                "B) Bu tümörde oluşan neoantijenlere karşı hastanın timusunda negatif seleksiyonla tam bir öz-tolerans gelişmiştir.",
                "C) Çok sayıda çerçeve kayması mutasyonu sonucu yüksek miktarda neoantijen eksprese eder ve Anti-PD-1 tedavisine mükemmel yanıt verir.",
                "D) Bu hastada immün kaçış yalnızca MHC Sınıf II moleküllerinin kaybıyla sınırlıdır, CD8+ CTL'ler aktive olamaz.",
                "E) Mikrosatellit instabilitesi olan tümörler yalnızca kutanöz skuamöz karsinomlarda checkpoint yanıtını artırır, viseral organlarda etkisizdir."
            ],
            "answer": "C",
            "explanation": "DNA mismatch repair (MMR; örn. MLH1 kaybı) defekti olan tümörlerde mikrosatellit instabilitesi (MSI-H) gelişir. Bu durum binlerce çerçeve kayması (frameshift) mutasyonuna yol açar ve hücre yüzeyinde MHC Sınıf I ile sunulan bol miktarda 'neoantijen' üretilir. Bu neoantijenlere karşı öz-tolerans bulunmadığı için güçlü bir immün tanıma mevcuttur; kontrol noktası inhibitörleri (Anti-PD-1) ile bu T hücreleri serbest bırakıldığında tümör dramatik şekilde geriler.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 3
    {
        "slideNumber": 3,
        "title": "Aşırı Eksprese Edilen veya Aberan Proteinler ve Diferansiyasyon Antijenleri",
        "subtitle": "HER2/neu, tirozinaz, Melan-A ve aberan glikozilasyonlu musinlerin patofizyolojisi",
        "badge": "Tümör Antijenleri",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Diferansiyasyon antijenleri normal dokuda da bulunur; melanomlu hastada tirozinaza karşı immün yanıt tetiklendiğinde normal melanositler de tahrip edilip vitiligo gelişebilir. Bu klinik bulgu, tümöre karşı etkili bir immün savaşın morfolojik kanıtıdır.",
            "note": "Prof. Dr. Hikmet Keleş, aşırı eksprese edilen hücresel onkoproteinlerin hem tanısal immünohistokimyada hem de hedefe yönelik monoklonal antikor tasarımında altın standart olduğunu vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Tümörle İlişkili Antijenler (TAA) ve Aşırı Ekspresyon\n"
            "Tümör antijenleri her zaman mutant peptitler olmak zorunda değildir. Normal hücrelerde düşük düzeyde sentezlenen ancak malign "
            "dönüşümde gen amplifikasyonuyla aşırı üretilen hücresel proteinler de immün yanıtı tetikleyebilir; bunlara **Tümörle İlişkili "
            "Antijenler (TAA)** denir. Bunun en klasik örneği **HER2/neu (ERBB2)** reseptör tirozin kinazıdır. Normal meme ve mide epitelinde "
            "hücre başına 20.000-50.000 reseptör bulunurken, HER2 amplifikasyonlu tümörlerde hücre zarında 1-2 milyon reseptör kopyası "
            "ifade edilir. Bu olağanüstü aşırı ekspresyon, periferik tolerans eşiğini aşarak hem hücresel hem hümoral yanıtları uyarır "
            "ve hedefe yönelik **Trastuzumab (Herceptin)** antikoru için ideal bir farmakolojik hedef oluşturur.\n\n"
            "### Doku Diferansiyasyon Antijenleri: Tirozinaz ve Melan-A\n"
            "Diferansiyasyon antijenleri, tümörün köken aldığı özgül hücre soyunda (lineage) fizyolojik olarak sentezlenen moleküllerdir. "
            "Kutanöz malign melanomda ifade edilen **Tirozinaz**, **Melan-A (MART-1)** ve **gp100** bu gruptadır. Tirozinaz, normal "
            "melanositlerde melanin biyosentezini yürüten temel enzimdir. Normal dokuda da bulunduğu için immün tolerans mevcuttur; ancak "
            "tümördeki yüksek antijen yükü bu toleransı kırabilir. Melanom hastalarında tirozinaza karşı sitotoksik T hücre yanıtı "
            "geliştiğinde, tümör hücrelerinin yanı sıra derideki normal melanositler de tahrip edilir ve ciltte yaygın edinsel depigmentasyon, "
            "yani **Vitiligo** ortaya çıkar. Melanomlu hastada vitiligo gelişmesi, bağışıklık sisteminin tümör antijenlerine karşı güçlü bir "
            "yanıt verdiğini gösteren bağımsız bir **İYİ PROGNOZ** işaretidir.\n\n"
            "### Aberan Post-Translasyonel Modifikasyonlar: MUC-1\n"
            "Bazı tümör antijenleri ise protein dizisindeki mutasyondan değil, translasyon sonrası glikozilasyon kusurlarından doğar. "
            "Glandüler epitelin apikal yüzeyinde koruyucu bariyer oluşturan **MUC-1 (Musin-1)**, normalde dallı karbonhidrat zincirleriyle "
            "kaplıdır. Meme, over ve pankreas karsinomlarında glikozilasyon eksik kalır; güdük zincirler normalde saklı duran peptit "
            "çekirdeğini (kriptik epitopları) bağışıklık sisteminin önüne sererek immünojenik hale getirir.\n\n"
            "🔴 **ÖNEMLİ:** Tirozinaz ve Melan-A diferansiyasyon antijenleridir; melanom immünoterapisinde bu antijenlere karşı gelişen "
            "çapraz yanıtın normal melanositleri tahrip etmesiyle 'vitiligo' gelişmesi iyi prognoz göstergesidir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Meme ve mide karsinomlarında gen amplifikasyonu sonucu hücre zarında aşırı eksprese edilen ve "
            "Trastuzumab monoklonal antikoru ile hedeflenen reseptör tirozin kinaz HER2/neu (ERBB2)'dur."
        ),
        "content": (
            "### Tümörle İlişkili Antijenler (TAA) ve Aşırı Ekspresyon\n"
            "Tümör antijenleri her zaman mutant peptitler olmak zorunda değildir. Normal hücrelerde düşük düzeyde sentezlenen ancak malign "
            "dönüşümde gen amplifikasyonuyla aşırı üretilen hücresel proteinler de immün yanıtı tetikleyebilir; bunlara **Tümörle İlişkili "
            "Antijenler (TAA)** denir. Bunun en klasik örneği **HER2/neu (ERBB2)** reseptör tirozin kinazıdır. Normal meme ve mide epitelinde "
            "hücre başına 20.000-50.000 reseptör bulunurken, HER2 amplifikasyonlu tümörlerde hücre zarında 1-2 milyon reseptör kopyası "
            "ifade edilir. Bu olağanüstü aşırı ekspresyon, periferik tolerans eşiğini aşarak hem hücresel hem hümoral yanıtları uyarır "
            "ve hedefe yönelik **Trastuzumab (Herceptin)** antikoru için ideal bir farmakolojik hedef oluşturur.\n\n"
            "### Doku Diferansiyasyon Antijenleri: Tirozinaz ve Melan-A\n"
            "Diferansiyasyon antijenleri, tümörün köken aldığı özgül hücre soyunda (lineage) fizyolojik olarak sentezlenen moleküllerdir. "
            "Kutanöz malign melanomda ifade edilen **Tirozinaz**, **Melan-A (MART-1)** ve **gp100** bu gruptadır. Tirozinaz, normal "
            "melanositlerde melanin biyosentezini yürüten temel enzimdir. Normal dokuda da bulunduğu için immün tolerans mevcuttur; ancak "
            "tümördeki yüksek antijen yükü bu toleransı kırabilir. Melanom hastalarında tirozinaza karşı sitotoksik T hücre yanıtı "
            "geliştiğinde, tümör hücrelerinin yanı sıra derideki normal melanositler de tahrip edilir ve ciltte yaygın edinsel depigmentasyon, "
            "yani **Vitiligo** ortaya çıkar. Melanomlu hastada vitiligo gelişmesi, bağışıklık sisteminin tümör antijenlerine karşı güçlü bir "
            "yanıt verdiğini gösteren bağımsız bir **İYİ PROGNOZ** işaretidir.\n\n"
            "### Aberan Post-Translasyonel Modifikasyonlar: MUC-1\n"
            "Bazı tümör antijenleri ise protein dizisindeki mutasyondan değil, translasyon sonrası glikozilasyon kusurlarından doğar. "
            "Glandüler epitelin apikal yüzeyinde koruyucu bariyer oluşturan **MUC-1 (Musin-1)**, normalde dallı karbonhidrat zincirleriyle "
            "kaplıdır. Meme, over ve pankreas karsinomlarında glikozilasyon eksik kalır; güdük zincirler normalde saklı duran peptit "
            "çekirdeğini (kriptik epitopları) bağışıklık sisteminin önüne sererek immünojenik hale getirir.\n\n"
            "🔴 **ÖNEMLİ:** Tirozinaz ve Melan-A diferansiyasyon antijenleridir; melanom immünoterapisinde bu antijenlere karşı gelişen "
            "çapraz yanıtın normal melanositleri tahrip etmesiyle 'vitiligo' gelişmesi iyi prognoz göstergesidir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Meme ve mide karsinomlarında gen amplifikasyonu sonucu hücre zarında aşırı eksprese edilen ve "
            "Trastuzumab monoklonal antikoru ile hedeflenen reseptör tirozin kinaz HER2/neu (ERBB2)'dur."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Tirozinaz ve Melan-A diferansiyasyon antijenleridir; melanomda bunlara karşı gelişen immün yanıt normal melanositleri de vurarak vitiligo oluşturur ve iyi prognozla birliktedir.",
            "🔵 **ÇIKMIŞ SORU:** HER2/neu (ERBB2), meme ve mide karsinomlarında aşırı eksprese edilen reseptör tirozin kinazdır; Trastuzumab ile hedeflenir.",
            "⚡ **PATOLOJİ:** MUC-1 gibi musinlerdeki aberan eksik glikozilasyon, gizli peptit epitoplarını açığa çıkararak antitümör immüniteyi tetikler."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Diferansiyasyon antijenleri tümöre özgü değildir, köken alınan doku soyuna özgüdür.",
            "🔵 **ÇIKMIŞ SORU:** Melanom hastasında gelişen depigmentasyon (vitiligo), antitümör immün yanıtın varlığını kanıtlayan pozitif prognostik faktördür.",
            "⚡ **PATOLOJİ:** HER2 pozitifliği immünohistokimyada 3+ membranöz boyanma veya FISH ile gen amplifikasyonu saptanarak doğrulanır."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Aşırı Eksprese Edilen Onkoproteinler",
                    "desc": "HER2/neu normal dokuda az miktardayken amplifikasyonla milyonlarca kopyaya ulaşarak hedef haline gelir.",
                    "isKey": True
                },
                {
                    "title": "Melanosit Diferansiyasyon Antijenleri",
                    "desc": "Tirozinaz, Melan-A ve gp100 melanomda eksprese edilir; çapraz otoimmünite vitiligoya yol açar.",
                    "isKey": True
                },
                {
                    "title": "Aberan Post-Translasyonel Değişiklikler",
                    "desc": "MUC-1 gibi musinlerin eksik glikozilasyonu kriptik immünojenik epitopların açığa çıkmasını sağlar.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Tümörle İlişkili Antijenler ve Diferansiyasyon Belirteçleri",
                "headers": ["Antijen Adı", "Normal Doku Dağılımı", "İlişkili Neoplazi", "Klinik ve Terapötik Önem"],
                "rows": [
                    ["HER2/neu (ERBB2)", "Normal meme ve mide epiteli (düşük)", "Meme ve mide adenokarsinomu", "Aşırı ekspresyon hedefe yönelik Trastuzumab hedefidir"],
                    ["Tirozinaz", "Epidermal melanositler", "Kutanöz malign melanom", "İmmün yıkım vitiligo yapar; iyi prognoz göstergesidir"],
                    ["Melan-A / MART-1", "Melanositler ve retina pigment epiteli", "Malign melanom", "Tanısal immünohistokimya ve aşı çalışmalarında hedef"],
                    ["Prostat Spesifik Antijen (PSA)", "Prostat duktal/asiner epiteli", "Prostat adenokarsinomu", "Doku diferansiyasyon belirteci, tarama ve nüks takibi"],
                    ["MUC-1 (Aberan Musin)", "Glandüler epitel apikal zarı", "Meme, over ve pankreas karsinomu", "Güdük glikozilasyon ile kriptik epitop açığa çıkışı"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-03-01",
                "category": "Diferansiyasyon Antijenleri",
                "front": "Melanom tedavisi gören bir hastada vücutta yaygın vitiligo (ciltte beyaz depigmente alanlar) gelişmesi ne anlama gelir?",
                "hint": "Tirozinaz ve Melan-A'ya karşı gelişen T hücre yanıtı.",
                "back": "Konağın tirozinaz gibi diferansiyasyon antijenlerine karşı güçlü bir CTL yanıtı ürettiğini ve normal melanositleri de tahrip ettiğini gösterir; İYİ PROGNOZ işaretidir.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu klinik bulguyu özellikle vurgulamıştır."
            },
            {
                "id": "imm-fc-03-02",
                "category": "Aşırı Eksprese Antijenler",
                "front": "Meme ve mide adenokarsinomlarında gen amplifikasyonuyla aşırı eksprese edilen ve Trastuzumab ile hedeflenen molekül nedir?",
                "hint": "Reseptör tirozin kinaz ailesi üyesi.",
                "back": "**HER2/neu (ERBB2)**. Hücre zarı başına milyonlarca kopyaya ulaşarak immün toleransı aşar ve monoklonal antikorlar için hedef oluşturur.",
                "facultyNote": "TUS Patoloji sınavlarında HER2 amplifikasyonu ve Trastuzumab ilişkisi en sık sorulan hedefler arasındadır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-03",
            "question": "Metastatik malign melanom tanısıyla immünoterapi başlanan 52 yaşındaki bir erkek hastanın 4. ay kontrolünde gövdesinde ve ekstremitelerinde yama tarzında belirgin depigmente cilt lezyonları (vitiligo) saptanıyor. Biyopside epidermisteki melanositlerin lenfositik infiltrasyonla tahrip edildiği izleniyor. Bu klinik tablonun patolojik ve immünolojik açıklaması aşağıdakilerden hangisidir?",
            "options": [
                "A) İmmünoterapi ilacının melanosit DNA'sında doğrudan sitotoksik mutasyon yapması sonucu oluşan bir komplikasyondur.",
                "B) Tümör hücrelerinin tirozinaz diferansiyasyon antijenini tamamen kaybederek immün sistemden kaçtığını gösterir.",
                "C) Aktive olan sitotoksik T lenfositlerin hem melanom hem de normal melanositlerdeki tirozinaz/Melan-A antijenlerine çapraz yanıt vermesidir ve iyi prognoz göstergesidir.",
                "D) Hastada eş zamanlı gelişen sistemik lupus eritematozus tablosudur ve immünoterapinin derhal kesilmesini gerektirir.",
                "E) Tümörün nöroendokrin diferansiasyona uğrayarak melanin üretimini durdurduğunu gösteren kötü prognoz bulgusudur."
            ],
            "answer": "C",
            "explanation": "Tirozinaz ve Melan-A (MART-1), melanosit diferansiyasyon antijenleridir. Hem melanom hücrelerinde hem de normal epidermal melanositlerde bulunurlar. İmmünoterapi ile bu antijenlere karşı güçlü bir CTL yanıtı uyarıldığında, tümör hücreleri yok edilirken normal melanositler de çapraz immüniteyle hasara uğrar ve vitiligo tablosu ortaya çıkar. Bu durum konakta etkili bir antitümöral yanıt oluştuğunu gösterir ve klinik olarak uzamış sağkalım ve iyi prognoz ile koreledir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 4
    {
        "slideNumber": 4,
        "title": "Kanser-Testis (Cancer-Testis / CTA) Antijenleri",
        "subtitle": "MAGE, BAGE, GAGE, NY-ESO-1 ve immünolojik ayrıcalık doku dinamiği",
        "badge": "Tümör Antijenleri",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser-Testis antijenleri doğanın muazzam bir paradoksudur: Normalde testis germ hücrelerinde eksprese edilirler ama testis MHC-I taşımaz! Bu yüzden timus bu antijenleri tanımaz. Tümörde yeniden ortaya çıktıklarında bağışıklık sistemi için kusursuz bir hedef haline gelirler.",
            "note": "Prof. Dr. Hikmet Keleş, MAGE ve NY-ESO-1 gibi Kanser-Testis antijenlerinin aşı ve TCR mühendisliği tedavilerinde neden ideal hedef olduğunu amfide ayrıntılı olarak açıklamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Kanser-Testis Antijenlerinin (CTA) Tanımı ve Doku Dağılımı\n"
            "Kanser-Testis Antijenleri (Cancer-Testis Antigens - CTA), tümör immünolojisinin en özgün antijen sınıflarındandır. "
            "Bu proteinler, fizyolojik koşullarda sadece erişkin testis dokusundaki germ hücrelerinde (spermatogonyumlar) ve plasentanın "
            "trofoblastik hücrelerinde eksprese edilir; diğer tüm normal erişkin somatik dokularda ise epigenetik hipermetilasyonla "
            "susturulurlar. Bu ailenin başlıca üyeleri **MAGE (MAGE-A1, MAGE-A3)**, **BAGE**, **GAGE**, **NY-ESO-1 (CTAG1B)** ve **SSX**'tir.\n\n"
            "### İmmünolojik Ayrıcalık (Immune Privilege) ve Tolerans Yokluğu\n"
            "Kanser-Testis antijenlerini immünolojik açıdan eşsiz kılan mekanizma testisin **'İmmünolojik Olarak Ayrıcalıklı "
            "(Immunologically Privileged)'** bir doku olmasıdır. Bu ayrıcalık iki temel faktöre dayanır:\n"
            "1. **Kan-Testis Bariyeri:** Sertoli hücreleri arasındaki sıkı bağlantılar antijenlerin sistemik lenfoid organlara geçişini engeller.\n"
            "2. **MHC Sınıf I Ekspresyonunun Yokluğu:** Testis germ hücreleri yüzeylerinde MHC Sınıf I molekülü taşımazlar. Bu nedenle gelişmekte "
            "olan T lenfositleri timusta veya periferde bu proteinlerle asla karşılaşmaz. Sonuç olarak **Kanser-Testis antijenlerine karşı "
            "bağışıklık sisteminde öz-tolerans gelişmemiştir!**\n\n"
            "### Solid Tümörlerde Yeniden Ekspresyon (De-represyon) ve Terapötik Önemi\n"
            "Malign melanom, küçük hücreli dışı akciğer karsinomu ve mesane karsinomlarında gelişen yaygın DNA hipometilasyonu, susturulmuş "
            "CTA genlerini yeniden aktif hale getirir (de-represyon). Somatik tümör hücreleri normal MHC Sınıf I moleküllerine sahip oldukları "
            "için, sentezlenen MAGE ve NY-ESO-1 peptitlerini yüzeylerinde CD8+ T lenfositlerine sunarlar. Bağışıklık sistemi için bu antijenler "
            "mutlak yabancıdır; sonuçta güçlü bir CTL infiltrasyonu tetiklenir. Normal somatik dokularda bulunmadıkları için CTA'lar, "
            "kişiselleştirilmiş kanser aşıları ve TCR mühendislikli T hücre tedavileri için otoimmün toksisite riski taşımayan ideal hedeflerdir.\n\n"
            "🔴 **ÖNEMLİ:** Testis germ hücrelerinde MHC Sınıf I bulunmadığı için kanser-testis antijenlerine (MAGE, NY-ESO-1) karşı tolerans "
            "gelişmez; tümörde de-represyonla eksprese edildiklerinde yabancı kabul edilerek güçlü immün yanıt doğururlar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Normalde sadece testis germ hücrelerinde eksprese edilen, diğer somatik dokularda susturulan ancak melanom "
            "ve akciğer kanserlerinde yeniden aktifleşerek T hücresi yanıtı başlatan antijen ailesi Kanser-Testis Antijenleridir (MAGE, NY-ESO-1)."
        ),
        "content": (
            "### Kanser-Testis Antijenlerinin (CTA) Tanımı ve Doku Dağılımı\n"
            "Kanser-Testis Antijenleri (Cancer-Testis Antigens - CTA), tümör immünolojisinin en özgün antijen sınıflarındandır. "
            "Bu proteinler, fizyolojik koşullarda sadece erişkin testis dokusundaki germ hücrelerinde (spermatogonyumlar) ve plasentanın "
            "trofoblastik hücrelerinde eksprese edilir; diğer tüm normal erişkin somatik dokularda ise epigenetik hipermetilasyonla "
            "susturulurlar. Bu ailenin başlıca üyeleri **MAGE (MAGE-A1, MAGE-A3)**, **BAGE**, **GAGE**, **NY-ESO-1 (CTAG1B)** ve **SSX**'tir.\n\n"
            "### İmmünolojik Ayrıcalık (Immune Privilege) ve Tolerans Yokluğu\n"
            "Kanser-Testis antijenlerini immünolojik açıdan eşsiz kılan mekanizma testisin **'İmmünolojik Olarak Ayrıcalıklı "
            "(Immunologically Privileged)'** bir doku olmasıdır. Bu ayrıcalık iki temel faktöre dayanır:\n"
            "1. **Kan-Testis Bariyeri:** Sertoli hücreleri arasındaki sıkı bağlantılar antijenlerin sistemik lenfoid organlara geçişini engeller.\n"
            "2. **MHC Sınıf I Ekspresyonunun Yokluğu:** Testis germ hücreleri yüzeylerinde MHC Sınıf I molekülü taşımazlar. Bu nedenle gelişmekte "
            "olan T lenfositleri timusta veya periferde bu proteinlerle asla karşılaşmaz. Sonuç olarak **Kanser-Testis antijenlerine karşı "
            "bağışıklık sisteminde öz-tolerans gelişmemiştir!**\n\n"
            "### Solid Tümörlerde Yeniden Ekspresyon (De-represyon) ve Terapötik Önemi\n"
            "Malign melanom, küçük hücreli dışı akciğer karsinomu ve mesane karsinomlarında gelişen yaygın DNA hipometilasyonu, susturulmuş "
            "CTA genlerini yeniden aktif hale getirir (de-represyon). Somatik tümör hücreleri normal MHC Sınıf I moleküllerine sahip oldukları "
            "için, sentezlenen MAGE ve NY-ESO-1 peptitlerini yüzeylerinde CD8+ T lenfositlerine sunarlar. Bağışıklık sistemi için bu antijenler "
            "mutlak yabancıdır; sonuçta güçlü bir CTL infiltrasyonu tetiklenir. Normal somatik dokularda bulunmadıkları için CTA'lar, "
            "kişiselleştirilmiş kanser aşıları ve TCR mühendislikli T hücre tedavileri için otoimmün toksisite riski taşımayan ideal hedeflerdir.\n\n"
            "🔴 **ÖNEMLİ:** Testis germ hücrelerinde MHC Sınıf I bulunmadığı için kanser-testis antijenlerine (MAGE, NY-ESO-1) karşı tolerans "
            "gelişmez; tümörde de-represyonla eksprese edildiklerinde yabancı kabul edilerek güçlü immün yanıt doğururlar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Normalde sadece testis germ hücrelerinde eksprese edilen, diğer somatik dokularda susturulan ancak melanom "
            "ve akciğer kanserlerinde yeniden aktifleşerek T hücresi yanıtı başlatan antijen ailesi Kanser-Testis Antijenleridir (MAGE, NY-ESO-1)."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Kanser-Testis antijenleri (MAGE, NY-ESO-1) normalde testiste eksprese edilir ancak testis hücrelerinde MHC-I bulunmadığı için immün tolerans gelişmemiştir.",
            "🔵 **ÇIKMIŞ SORU:** Solid tümörlerde DNA hipometilasyonu sonucu sessizliği bozularak (de-represyon) ifade edilen ve immünoterapi hedefi olan antijenler Kanser-Testis Antijenleridir.",
            "⚡ **TERAPÖTİK:** NY-ESO-1 ve MAGE-A3, TCR-transgenik T hücre tedavilerinde ve terapötik kanser aşılarında en sık hedeflenen moleküllerdir."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Testis germ hücreleri immünolojik ayrıcalığa sahiptir; kan-testis bariyeri ve MHC-I yokluğu lenfositik toleransı engeller.",
            "🔵 **ÇIKMIŞ SORU:** Melanom, mesane ve küçük hücreli dışı akciğer kanserlerinde yüksek oranda yeniden aktive olan antijen grubu MAGE ailesidir.",
            "⚡ **TERAPÖTİK:** CTA ekspresyonu normal dokuda sadece sperm üretiminde olduğu için hedeflenmeleri otoimmün doku hasarı (toksisite) oluşturmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "İmmünolojik Ayrıcalık ve Tolerans Yokluğu",
                    "desc": "Testiste MHC-I ekspresyonu olmadığı için T hücreleri MAGE/NY-ESO-1'e karşı tolerans geliştirmemiştir.",
                    "isKey": True
                },
                {
                    "title": "Epigenetik De-represyon",
                    "desc": "Tümör hücrelerindeki global DNA hipometilasyonu susturulmuş CTA genlerini yeniden aktif hale getirir.",
                    "isKey": True
                },
                {
                    "title": "Terapötik Güvenlik Profili",
                    "desc": "Normal somatik dokularda hiç bulunmadıkları için CTA hedeflendiğinde sağlıklı organlarda otoimmünite gelişmez.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Kanser-Testis Antijenleri vs Diferansiyasyon Antijenleri Karşılaştırması",
                "headers": ["Özellik", "Kanser-Testis Antijenleri (MAGE, NY-ESO-1)", "Diferansiyasyon Antijenleri (Tirozinaz, PSA)"],
                "rows": [
                    ["Normal Doku Varlığı", "Sadece testis germ hücresi ve plasenta", "İlgili hücre soyundaki tüm normal hücreler"],
                    ["Öz-Tolerans Durumu", "Tolerans YOK (Testiste MHC-I yoktur)", "Tolerans VAR (Ancak aşırı antijenle kırılabilir)"],
                    ["İmmünojenite Derecesi", "Çok yüksek (Yabancı antijen gibi algılanır)", "Orta / Düşük (Otoantijen karakterindedir)"],
                    ["Tedavi Sırasında Toksisite", "Toksisite beklenmez (Testis MHC-I taşımaz)", "Otoimmünite gelişir (örn. Vitiligo, tiroidit)"],
                    ["Tümör Tipleri", "Melanom, akciğer Ca, mesane ürotelyal Ca", "Melanom (Tirozinaz), Prostat Ca (PSA)"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-04-01",
                "category": "Kanser-Testis Antijenleri",
                "front": "Kanser-Testis antijenlerine (MAGE, NY-ESO-1) karşı normal konakta immün tolerans gelişmemesinin en temel sebebi nedir?",
                "hint": "Testis germ hücrelerinin yüzey molekülü profili.",
                "back": "Testis germ hücrelerinde Majör Histokompatibilite Kompleksi Sınıf I (MHC-I) ekspresyonunun bulunmamasıdır; lenfositler bu antijenlerle sunum ortamında tanışamaz.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu mekanizmanın sınavda mutlaka sorgulanacağını belirtmiştir."
            },
            {
                "id": "imm-fc-04-02",
                "category": "Epigenetik Mekanizma",
                "front": "Normal somatik dokularda susturulmuş olan Kanser-Testis antijenlerinin tümörde yeniden belirmesini sağlayan epigenetik olay nedir?",
                "hint": "DNA metilasyon durumu.",
                "back": "Genom çapında gelişen yaygın **DNA hipometilasyonudur** (CpG adalarının demetilasyonu ve gen de-represyonu).",
                "facultyNote": "Moleküler patoloji sorularında epigenetik hipometilasyon ve onkojenik reaktivasyon sıkça eşleştirilir."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-04",
            "question": "Malign melanom ve akciğer skuamöz hücreli karsinomunda yüksek düzeyde saptanan MAGE-A3 ve NY-ESO-1 gibi 'Kanser-Testis Antijenleri' (CTA) ile ilgili aşağıdaki ifadelerden hangisi BİYOLOJİK VE İMMÜNOLOJİK AÇIDAN DOĞRUDUR?",
            "options": [
                "A) Normal erişkin karaciğer ve böbrek tübül hücrelerinde yüksek düzeyde eksprese edilirler.",
                "B) Testis germ hücrelerinde MHC Sınıf I ekspresyonu bulunmadığı için T hücrelerinde bu antijenlere karşı öz-tolerans gelişmemiştir.",
                "C) Bu antijenleri hedefleyen immünoterapiler testis spermatogenezini geri dönüşümsüz olarak tahrip eder.",
                "D) Kanser-testis antijenleri daima kromozomal translokasyonlar sonucu oluşan mutant füzyon proteinleridir.",
                "E) Yalnızca benign adenomlarda bulunurlar, invaziv karsinomlara geçişte epigenetik olarak susturulurlar."
            ],
            "answer": "B",
            "explanation": "Kanser-Testis Antijenleri (CTA; MAGE, NY-ESO-1), fizyolojik olarak sadece testis germ hücrelerinde eksprese edilir. Testis germ hücreleri yüzeyinde MHC Sınıf I molekülü bulunmadığından ve kan-testis bariyeri mevcut olduğundan, gelişmekte olan T lenfositleri bu antijenlerle temas edemez ve tolerans gelişmez. Solid tümörlerde DNA hipometilasyonu ile yeniden eksprese edildiklerinde, tümör hücresindeki MHC-I ile sunularak güçlü bir immün tanıma sağlarlar. Testis germ hücreleri MHC-I taşımadığı için T hücre tedavileri testisi hedefleyip hasarlayamaz.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 5
    {
        "slideNumber": 5,
        "title": "Onkoviral Antijenler ve Virüs Aracılı Maligniteler",
        "subtitle": "HPV E6/E7, EBV LMP1/EBNA ve viral onkoproteinlerin immün hedefleri",
        "badge": "Viral Onkogenez",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Viral tümör antijenleri konak genomundan köken almaz; doğrudan viral genom tarafından kodlanan yabancı proteinlerdir. HPV'nin E6 ve E7'si, EBV'nin LMP1'i hem karsinogenezin sürücüsüdür hem de immün sistemin mutlak hedefidir.",
            "note": "Prof. Dr. Hikmet Keleş, HPV ve EBV onkoproteinlerinin moleküler hedeflerinin (p53, RB, NF-kB) patolojinin en yüksek verimli soru alanları olduğunu vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Viral Onkogenez İlkeleri ve Antijen Sunumu\n"
            "İnsan kanserlerinin yaklaşık %15-20'sinden onkojenik virüsler sorumludur. Onkoviral neoplazilerde tümör hücreleri, viral "
            "genomu kendi konak DNA'sına entegre etmiş veya epizomlar halinde taşımaktadır. Virüsler tarafından kodlanan onkoproteinler, "
            "konak proteomunda bulunmayan **mutlak yabancı proteinlerdir**. Bu proteinler tümör hücresinin proteazomunda parçalanıp TAP "
            "aracılığıyla **MHC Sınıf I** moleküllerine yüklenerek CD8+ CTL'lere sunulur; dolayısıyla kuvvetli bir immün yanıt tetiklerler.\n\n"
            "### İnsan Papilloma Virüsü (HPV) E6 ve E7 Onkoproteinleri\n"
            "Yüksek riskli HPV tipleri (Tip 16, 18), Servikal Skuamöz Karsinom ve Orofarenks (tonsil) kanserlerinin ana etkenidir. "
            "Viral genom konak DNA'sına entegre olduğunda viral regülatuar E2 geni parçalanır; bu durum iki majör onkoproteinin kontrolsüz "
            "salınımına yol açar:\n"
            "1. **HPV E6 Proteini:** Bir E3 ubikitin ligaz olan E6AP ile birleşerek ana tümör baskılayıcı **p53** proteinine bağlanır. p53'ü "
            "ubikitinleyerek 26S proteazomunda parçalatır. Hücre DNA hasarına karşı G1/S arresti yapamaz ve apoptoza gidemez; ayrıca telomerazı "
            "(TERT) aktive eder.\n"
            "2. **HPV E7 Proteini:** Hipofosforile (aktif) durumdaki **Retinoblastom (RB)** proteinine bağlanarak onu inaktive eder. RB'nin "
            "inaktivasyonu, baskı altındaki **E2F transkripsiyon faktörünün serbest kalmasına** yol açar. Serbest E2F hücreyi kontrolsüz "
            "şekilde S fazına sokar.\n\n"
            "### Epstein-Barr Virüsü (EBV): LMP1 ve B Hücre Ölümsüzlüğü\n"
            "EBV (HHV-4), Burkitt Lenfoma, Nazofarenks Karsinomu ve Hodgkin Lenfoma etkenidir:\n"
            "- **LMP1 (Latent Membran Proteini 1):** Tümör zarına yerleşerek **CD40 reseptörünü taklit eder**. Ligand uyarısı olmadan "
            "sürekli olarak **NF-kB ve JAK/STAT sinyal yolaklarını aktif tutar**. Bu sinyaller anti-apoptotik Bcl-2 ailesini artırarak "
            "B hücrelerine sınırsız proliferasyon ve ölümsüzlük sağlar.\n"
            "- Diğer onkovirüsler: HBV (HBx proteini ile transkripsiyonu bozar), HCV (kronik inflamasyonla HCC), KSHV/HHV-8 (Kaposi sarkomu).\n\n"
            "🔴 **ÖNEMLİ:** HPV E6 onkoproteini p53'ü proteazomda yıkar; HPV E7 ise RB proteinine bağlanarak E2F'yi serbest bırakır ve "
            "hücreyi S fazına geçirir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** EBV tarafından kodlanan, konak hücresindeki CD40 reseptörünü taklit ederek ligand bağımsız konstitütif "
            "NF-kB aktivasyonu sağlayan onkoprotein Latent Membran Proteini-1'dir (LMP1)."
        ),
        "content": (
            "### Viral Onkogenez İlkeleri ve Antijen Sunumu\n"
            "İnsan kanserlerinin yaklaşık %15-20'sinden onkojenik virüsler sorumludur. Onkoviral neoplazilerde tümör hücreleri, viral "
            "genomu kendi konak DNA'sına entegre etmiş veya epizomlar halinde taşımaktadır. Virüsler tarafından kodlanan onkoproteinler, "
            "konak proteomunda bulunmayan **mutlak yabancı proteinlerdir**. Bu proteinler tümör hücresinin proteazomunda parçalanıp TAP "
            "aracılığıyla **MHC Sınıf I** moleküllerine yüklenerek CD8+ CTL'lere sunulur; dolayısıyla kuvvetli bir immün yanıt tetiklerler.\n\n"
            "### İnsan Papilloma Virüsü (HPV) E6 ve E7 Onkoproteinleri\n"
            "Yüksek riskli HPV tipleri (Tip 16, 18), Servikal Skuamöz Karsinom ve Orofarenks (tonsil) kanserlerinin ana etkenidir. "
            "Viral genom konak DNA'sına entegre olduğunda viral regülatuar E2 geni parçalanır; bu durum iki majör onkoproteinin kontrolsüz "
            "salınımına yol açar:\n"
            "1. **HPV E6 Proteini:** Bir E3 ubikitin ligaz olan E6AP ile birleşerek ana tümör baskılayıcı **p53** proteinine bağlanır. p53'ü "
            "ubikitinleyerek 26S proteazomunda parçalatır. Hücre DNA hasarına karşı G1/S arresti yapamaz ve apoptoza gidemez; ayrıca telomerazı "
            "(TERT) aktive eder.\n"
            "2. **HPV E7 Proteini:** Hipofosforile (aktif) durumdaki **Retinoblastom (RB)** proteinine bağlanarak onu inaktive eder. RB'nin "
            "inaktivasyonu, baskı altındaki **E2F transkripsiyon faktörünün serbest kalmasına** yol açar. Serbest E2F hücreyi kontrolsüz "
            "şekilde S fazına sokar.\n\n"
            "### Epstein-Barr Virüsü (EBV): LMP1 ve B Hücre Ölümsüzlüğü\n"
            "EBV (HHV-4), Burkitt Lenfoma, Nazofarenks Karsinomu ve Hodgkin Lenfoma etkenidir:\n"
            "- **LMP1 (Latent Membran Proteini 1):** Tümör zarına yerleşerek **CD40 reseptörünü taklit eder**. Ligand uyarısı olmadan "
            "sürekli olarak **NF-kB ve JAK/STAT sinyal yolaklarını aktif tutar**. Bu sinyaller anti-apoptotik Bcl-2 ailesini artırarak "
            "B hücrelerine sınırsız proliferasyon ve ölümsüzlük sağlar.\n"
            "- Diğer onkovirüsler: HBV (HBx proteini ile transkripsiyonu bozar), HCV (kronik inflamasyonla HCC), KSHV/HHV-8 (Kaposi sarkomu).\n\n"
            "🔴 **ÖNEMLİ:** HPV E6 onkoproteini p53'ü proteazomda yıkar; HPV E7 ise RB proteinine bağlanarak E2F'yi serbest bırakır ve "
            "hücreyi S fazına geçirir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** EBV tarafından kodlanan, konak hücresindeki CD40 reseptörünü taklit ederek ligand bağımsız konstitütif "
            "NF-kB aktivasyonu sağlayan onkoprotein Latent Membran Proteini-1'dir (LMP1)."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** HPV E6 p53'ü proteazomal yıkıma uğratır; HPV E7 ise RB proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakır.",
            "🔵 **ÇIKMIŞ SORU:** EBV'nin LMP1 proteini, konak hücresindeki CD40 reseptörünü taklit ederek konstitütif NF-kB aktivasyonu ve B hücre ölümsüzlüğü sağlar.",
            "⚡ **VİRAL ANTİJEN:** Viral onkoproteinler konak hücresine yabancı oldukları için MHC Sınıf I ile sunulduklarında güçlü CTL yanıtı uyandırırlar."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** HPV Tip 16 ve 18 genomunun konak DNA'sına entegrasyonu, E2 genini yıkarak E6 ve E7 onkoproteinlerinin aşırı ekspresyonuna yol açar.",
            "🔵 **ÇIKMIŞ SORU:** Orofaringeal (tonsil) skuamöz hücreli karsinomlarda HPV-pozitif tümörler, tütün ilişkili tümörlere göre immünoterapiye ve radyoterapiye daha iyi yanıt verir.",
            "⚡ **VİRAL ANTİJEN:** HBV HBx proteini transkripsiyon faktörlerini modüle ederek hepatokarsinogenezi hızlandırır."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "HPV E6 ve p53 Yıkımı",
                    "desc": "E6AP ubikitin ligaz kompleksi ile p53 proteazomda parçalanır; apoptoz ve G1/S kontrolü çöker.",
                    "isKey": True
                },
                {
                    "title": "HPV E7 ve E2F Salınımı",
                    "desc": "E7 proteini hipofosforile RB'ye bağlanarak serbest kalan E2F aracılığıyla hücreyi S fazına sokar.",
                    "isKey": True
                },
                {
                    "title": "EBV LMP1 ve CD40 Taklidi",
                    "desc": "LMP1 onkoproteini CD40 sinyalini taklit edip NF-kB yolağını sürekli açık tutarak lenfoma gelişimini tetikler.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Başlıca Onkojenik Virüsler, Onkoproteinleri ve Moleküler Hedefleri",
                "headers": ["Onkojenik Virüs", "Majör Viral Onkoprotein", "Moleküler Hücresel Hedef", "İlişkili Maligniteler"],
                "rows": [
                    ["HPV (Tip 16, 18)", "E6", "p53 degradasyonu (ubikitin-proteazom), TERT aktivasyonu", "Serviks ve orofarenks karsinomu"],
                    ["HPV (Tip 16, 18)", "E7", "RB bağlanması ve inaktivasyonu, E2F serbestleşmesi", "Serviks, anogenital ve tonsil karsinomu"],
                    ["EBV (HHV-4)", "LMP1", "CD40 taklidi, sürekli NF-kB ve JAK/STAT aktivasyonu", "Nazofarenks Ca, Hodgkin ve Burkitt lenfoma"],
                    ["EBV (HHV-4)", "EBNA-2", "Notch reseptör taklidi, Siklin D ve c-Myc indüksiyonu", "B hücreli lenfoproliferatif hastalıklar"],
                    ["KSHV (HHV-8)", "v-Cyclin, v-FLIP, v-GPCR", "CDK6 aktivasyonu, Kaspaz-8 inhibisyonu, VEGF salınımı", "Kaposi sarkomu, Primer Efüzyon Lenfoması"],
                    ["HBV", "HBx proteini", "p53 bağlanması, sitoplazmik sinyal iletimi kaskadları", "Hepatosellüler karsinom (HCC)"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-05-01",
                "category": "HPV Onkogenezi",
                "front": "Yüksek riskli HPV'nin E6 ve E7 onkoproteinleri hangi temel tümör baskılayıcı gen ürünlerini inaktive eder?",
                "hint": "Genomun bekçisi ve hücre siklusunun ana freni.",
                "back": "**E6 proteini p53'ü** ubikitinleyerek proteazomda parçalatır; **E7 proteini ise Retinoblastom (RB)** proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakır.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu ikilinin komite ve TUS sınavlarının değişmez soru kalıbı olduğunu söylemiştir."
            },
            {
                "id": "imm-fc-05-02",
                "category": "EBV Onkogenezi",
                "front": "EBV tarafından kodlanan LMP1 onkoproteini konak hücresinde hangi reseptörü taklit ederek onkogenezi sürdürür?",
                "hint": "B hücresi kostimülatör reseptörü.",
                "back": "**CD40 reseptörünü** taklit eder; ligand bağımsız olarak NF-kB ve JAK/STAT yolaklarını sürekli aktif tutarak B hücre apoptozunu engeller.",
                "facultyNote": "LMP1 ve NF-kB ilişkisi hematopatoloji ve genel onkoloji sınavlarında yüksek frekanslıdır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-05",
            "question": "36 yaşındaki bir kadının rutin jinekolojik smear taramasında yüksek dereceli skuamöz intraepitelyal lezyon (HSIL) saptanıyor. Biyopside HPV Tip 16 DNA pozitifliği gösteriliyor. Bu hastanın servikal epitelinde viral transformasyonun gerçekleşmesinde rol oynayan HPV E6 ve E7 onkoproteinlerinin hücresel etkileri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) E6 proteini p53'ü doğrudan fosforilleyerek DNA tamir kapasitesini artırır.",
                "B) E7 proteini hipofosforile Retinoblastom (RB) proteinine bağlanıp inaktive ederek E2F transkripsiyon faktörünü serbest bırakır.",
                "C) E6 proteini B hücresindeki CD40 reseptörünü taklit ederek sitokin fırtınası başlatır.",
                "D) E7 proteini kaspaz-8 aktivasyonunu tetikleyerek servikal epitelde yaygın apoptoza yol açar.",
                "E) E6 ve E7 proteinleri hücre yüzeyinde MHC Sınıf II moleküllerini artırarak lenfositik lizisi hızlandırır."
            ],
            "answer": "B",
            "explanation": "Yüksek riskli HPV (Tip 16 ve 18) karsinogenezinde E7 onkoproteini, hipofosforile (aktif) Retinoblastom (RB) proteinine bağlanarak onu inaktive eder. RB inaktive olunca serbest kalan E2F transkripsiyon faktörü hücre siklusunu zorla G1'den S fazına geçirir. E6 ise p53 tümör baskılayıcı proteinini ubikitin-proteazom yolağıyla parçalar. Bu iki mekanizma apoptozu engelleyip kontrolsüz DNA sentezi sağlayarak malign transformasyona yol açar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 6
    {
        "slideNumber": 6,
        "title": "Onkofetal Antijenler: Karsinoembriyonik Antijen (CEA) ve Alfa-Fetoprotein (AFP)",
        "subtitle": "Fetal gelişimde eksprese edilen, neoplazide reaktive olan tümör belirteçleri",
        "badge": "Onkofetal Antijenler",
        "badgeColor": "cyan",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "CEA ve AFP gibi onkofetal proteinler mükemmel tümör belirteçleridir ancak zayıf immünojendirler! Fetal hayattan beri var oldukları için bağışıklık sistemi bunlara tamamen toleranslıdır. Bu yüzden taramada değil, cerrahi sonrası nüks takibinde değerlidirler.",
            "note": "Prof. Dr. Hikmet Keleş, CEA'nın kolorektal kanser cerrahisi sonrası karaciğer metastazının en erken habercisi olduğunu ve sınavda mutlaka ayırt edilmesi gerektiğini belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Onkofetal Antijenlerin Biyolojisi ve Epigenetik Reaktivasyon\n"
            "Onkofetal antijenler, fetal gelişim ve organogenez sırasında fetal dokular tarafından yüksek düzeyde üretilen; doğumdan sonra "
            "genlerinin epigenetik olarak susturulmasıyla erişkin dokularda iz miktara inen proteinlerdir. Malign transformasyon "
            "sırasında kanser hücrelerinde gelişen epigenetik düzensizlikler sonucu bu embriyonik genler yeniden transkribe edilmeye "
            "başlar. Başlıca iki temsilcisi **Karsinoembriyonik Antijen (CEA)** ve **Alfa-Fetoprotein (AFP)**'dir.\n\n"
            "### Karsinoembriyonik Antijen (CEA - CD66e)\n"
            "CEA, fetal yaşamın ilk iki trimesterinde bağırsak mukozası, karaciğer ve pankreasta yoğun üretilen karmaşık bir glikoproteindir:\n"
            "- **İlişkili Neoplaziler:** Başta **Kolorektal Adenokarsinomlar** olmak üzere (%60-80 olguda kanda yükselir), Pankreas, Mide, "
            "Meme ve Akciğer adenokarsinomlarında artış gösterir.\n"
            "- **Klinik Kullanım Kuralları:** CEA **asla primer kanser tarama (screening) testi DEĞİLDİR!** Erken evrede duyarlılığı düşüktür ve "
            "benign durumlarda da (siroz, pankreatit, ülseratif kolit, ağır sigara içimi) yükselebilir. CEA'nın onkolojideki temel amacı: "
            "Ameliyat öncesi bazal düzey tespiti, cerrahinin tam yapıldığının doğrulanması ve takipte serum düzeyinin yeniden yükselmesiyle "
            "**Karaciğer metastazı ve nüksün** erkenden saptanmasıdır.\n\n"
            "### Alfa-Fetoprotein (AFP) ve İmmünojenite Paradoksu\n"
            "AFP, fetal karaciğer ve vitellüs kesesi (yolk sac) tarafından üretilen fetal plazmanın ana proteinidir (fetal albümin eşdeğeri):\n"
            "- **İlişkili Maligniteler:** **Hepatosellüler Karsinom (HCC)** ve non-seminomatöz testis germ hücreli tümörlerinde (özellikle "
            "**Yolk Sac Tümörü**) kanda dramatik olarak yükselir. Saf seminomda AFP artışı görülmez.\n\n"
            "### Neden Zayıf İmmünojendirler?\n"
            "Onkofetal antijenler kanda çok yüksek düzeylere çıksalar da güçlü bir CTL yanıtı tetikleyemezler. Çünkü intrauterin dönemde "
            "T lenfositleri timusta eğitilirken bu antijenlerle karşılaşmış ve **tam bir santral immün tolerans** geliştirmiştir. "
            "Ayrıca bu proteinler hücre zarında sabit kalmayıp dolaşıma çözünür moleküller olarak dökülürler (antijenik shedding).\n\n"
            "🔴 **ÖNEMLİ:** CEA ve AFP zayıf immünojendir çünkü intrauterin dönemden beri mevcut oldukları için konakta tam öz-tolerans "
            "vardır; primer tarama testi olarak değil, cerrahi rezeksiyon sonrası nüks ve metastaz takibinde kullanılırlar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Kolorektal adenokarsinom cerrahisi sonrası takipleri sırasında serumda Karsinoembriyonik Antijen (CEA) "
            "düzeyinin ilerleyici artış göstermesi en çok karaciğer metastazı ve tümör nüksünü düşündürmelidir."
        ),
        "content": (
            "### Onkofetal Antijenlerin Biyolojisi ve Epigenetik Reaktivasyon\n"
            "Onkofetal antijenler, fetal gelişim ve organogenez sırasında fetal dokular tarafından yüksek düzeyde üretilen; doğumdan sonra "
            "genlerinin epigenetik olarak susturulmasıyla erişkin dokularda iz miktara inen proteinlerdir. Malign transformasyon "
            "sırasında kanser hücrelerinde gelişen epigenetik düzensizlikler sonucu bu embriyonik genler yeniden transkribe edilmeye "
            "başlar. Başlıca iki temsilcisi **Karsinoembriyonik Antijen (CEA)** ve **Alfa-Fetoprotein (AFP)**'dir.\n\n"
            "### Karsinoembriyonik Antijen (CEA - CD66e)\n"
            "CEA, fetal yaşamın ilk iki trimesterinde bağırsak mukozası, karaciğer ve pankreasta yoğun üretilen karmaşık bir glikoproteindir:\n"
            "- **İlişkili Neoplaziler:** Başta **Kolorektal Adenokarsinomlar** olmak üzere (%60-80 olguda kanda yükselir), Pankreas, Mide, "
            "Meme ve Akciğer adenokarsinomlarında artış gösterir.\n"
            "- **Klinik Kullanım Kuralları:** CEA **asla primer kanser tarama (screening) testi DEĞİLDİR!** Erken evrede duyarlılığı düşüktür ve "
            "benign durumlarda da (siroz, pankreatit, ülseratif kolit, ağır sigara içimi) yükselebilir. CEA'nın onkolojideki temel amacı: "
            "Ameliyat öncesi bazal düzey tespiti, cerrahinin tam yapıldığının doğrulanması ve takipte serum düzeyinin yeniden yükselmesiyle "
            "**Karaciğer metastazı ve nüksün** erkenden saptanmasıdır.\n\n"
            "### Alfa-Fetoprotein (AFP) ve İmmünojenite Paradoksu\n"
            "AFP, fetal karaciğer ve vitellüs kesesi (yolk sac) tarafından üretilen fetal plazmanın ana proteinidir (fetal albümin eşdeğeri):\n"
            "- **İlişkili Maligniteler:** **Hepatosellüler Karsinom (HCC)** ve non-seminomatöz testis germ hücreli tümörlerinde (özellikle "
            "**Yolk Sac Tümörü**) kanda dramatik olarak yükselir. Saf seminomda AFP artışı görülmez.\n\n"
            "### Neden Zayıf İmmünojendirler?\n"
            "Onkofetal antijenler kanda çok yüksek düzeylere çıksalar da güçlü bir CTL yanıtı tetikleyemezler. Çünkü intrauterin dönemde "
            "T lenfositleri timusta eğitilirken bu antijenlerle karşılaşmış ve **tam bir santral immün tolerans** geliştirmiştir. "
            "Ayrıca bu proteinler hücre zarında sabit kalmayıp dolaşıma çözünür moleküller olarak dökülürler (antijenik shedding).\n\n"
            "🔴 **ÖNEMLİ:** CEA ve AFP zayıf immünojendir çünkü intrauterin dönemden beri mevcut oldukları için konakta tam öz-tolerans "
            "vardır; primer tarama testi olarak değil, cerrahi rezeksiyon sonrası nüks ve metastaz takibinde kullanılırlar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Kolorektal adenokarsinom cerrahisi sonrası takipleri sırasında serumda Karsinoembriyonik Antijen (CEA) "
            "düzeyinin ilerleyici artış göstermesi en çok karaciğer metastazı ve tümör nüksünü düşündürmelidir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Onkofetal antijenler (CEA, AFP) zayıf immünojendir çünkü fetal hayatta maruziyet nedeniyle konakta tam öz-tolerans gelişmiştir.",
            "🔵 **ÇIKMIŞ SORU:** CEA genel popülasyonda kanser tarama testi olarak KULLANILMAZ; kolorektal karsinom cerrahisi sonrası nüks ve karaciğer metastazı takibinde altın standarttır.",
            "⚡ **TÜMÖR BELİRTECİ:** Serumda belirgin AFP artışı Hepatosellüler Karsinom (HCC) ve testisin Yolk Sac Tümörünün kardinal biyokimyasal bulgusudur."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** CEA benign durumlarda da (siroz, pankreatit, ülseratif kolit, ağır sigara içimi) yükselebilir.",
            "🔵 **ÇIKMIŞ SORU:** Testis tümörlü bir hastada serum AFP yüksekliği saptanması, lezyonun saf seminom olmadığını, non-seminomatöz (özellikle yolk sac) komponent içerdiğini kanıtlar.",
            "⚡ **TÜMÖR BELİRTECİ:** Tedavi sonrası sıfırlanan CEA'nın tekrar yükselmesi klinik nüksün 3-6 ay öncesinden habercisidir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Onkofetal Reaktivasyon",
                    "desc": "Fetal gelişimde üretilip erişkinde susturulan genlerin karsinogenezde epigenetik olarak yeniden açılmasıdır.",
                    "isKey": True
                },
                {
                    "title": "CEA'nın Klinik Kullanımı",
                    "desc": "Tarama testi değildir; kolorektal kanser cerrahisi sonrası rezidüel kitle ve metastaz monitörizasyonunda kullanılır.",
                    "isKey": True
                },
                {
                    "title": "AFP ve İlişkili Maligniteler",
                    "desc": "Fetal albümin eşdeğeri olup HCC ve testis yolk sac tümörlerinde tanı ve takip belirtecidir.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Majör Onkofetal Belirteçler, Fizyolojik Kökenleri ve Klinik Özellikleri",
                "headers": ["Belirteç Adı", "Fetal Kaynağı", "İlişkili Malign Neoplaziler", "Yükseldiği Benign Durumlar", "Klinik Rolü"],
                "rows": [
                    ["Karsinoembriyonik Antijen (CEA)", "Fetal bağırsak, karaciğer, pankreas", "Kolorektal Ca (%70), mide, pankreas, meme Ca", "Siroz, pankreatit, İBH, sigara içimi", "Cerrahi sonrası nüks/metastaz takibi"],
                    ["Alfa-Fetoprotein (AFP)", "Fetal karaciğer ve yolk sac", "Hepatosellüler Karsinom (HCC), Yolk Sac Tümörü", "Karaciğer sirozu, akut viral hepatit rejenerasyonu", "HCC taraması (sirotiklerde) ve germ hücreli tümör takibi"],
                    ["CA-125 (Onkofetal musin)", "Çölomik epitel türevleri", "Over seröz karsinomu, endometriyal karsinom", "Endometriozis, pelvik inflamatuar hastalık (PIH)", "Over kanseri tedavi yanıtı takibi"],
                    ["CA 19-9", "Fetal glandüler epitel", "Pankreas ve safra yolu adenokarsinomları", "Kolanjit, tıkanma sarılığı, kolesistit", "Pankreas kanseri kemoterapi yanıtı takibi"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-06-01",
                "category": "Onkofetal Antijenler",
                "front": "CEA ve AFP gibi onkofetal proteinler kanda yüksek seviyelere çıkmasına rağmen neden güçlü bir immün yanıt tetiklemez?",
                "hint": "Fetal dönemdeki immünolojik eğitim süreci.",
                "back": "Fetal yaşamda dolaşımda bulundukları için konağın T lenfositleri bunlara karşı **tam bir öz-tolerans (self-tolerance)** geliştirmiştir; yabancı olarak algılanmazlar.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide tolerans mekanizması ile tümör belirteçleri ilişkisini vurgulamıştır."
            },
            {
                "id": "imm-fc-06-02",
                "category": "Klinik Patoloji",
                "front": "Kolorektal adenokarsinom nedeniyle hemikolektomi yapılan hastada CEA neden rutin tarama testi değil de takip testi olarak kullanılır?",
                "hint": "Benign durumlarda yalancı pozitiflik ve erken evrede düşük duyarlılık.",
                "back": "Siroz, sigara, kolit gibi benign durumlarda da yükselebildiği ve erken evrede negatif olabildiği için taramada güvenilmezdir; ancak cerrahi sonrası nüksü erken saptamada mükemmeldir.",
                "facultyNote": "TUS Genel Cerrahi ve Patoloji ortak sorularında CEA endikasyonu klasik bir tuzaktır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-06",
            "question": "Kolon adenokarsinomu nedeniyle küratif cerrahi rezeksiyon uygulanan 62 yaşındaki bir erkeğin ameliyat öncesi serum CEA düzeyi 24 ng/mL (normal: <3 ng/mL) iken postoperatif 1. ayda 1.8 ng/mL'ye gerilemiştir. Ameliyattan 14 ay sonra yapılan rutin kontrolde asemptomatik olan hastanın serum CEA düzeyi 38 ng/mL olarak saptanıyor. Bu klinik tablonun en olası nedeni ve CEA'nın immünolojik özellikleri ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) CEA güçlü bir sitotoksik neoantijen olduğu için hastada immün sistemin tümörü tamamen temizlediğini gösterir.",
                "B) Kolorektal kanser nüksü ve olası karaciğer metastazı gelişmiştir; CEA tolerans nedeniyle zayıf immünojenik bir takip belirtecidir.",
                "C) Hastada yeni bir primer bazal hücreli karsinom geliştiğini gösteren spesifik bir belirteçtir.",
                "D) CEA düzeyindeki bu artış ameliyat bölgesinde cerrahi sütür reaksiyonuna bağlı gelişen fizyolojik bir inflamasyon yanıtıdır.",
                "E) CEA fetal dönemde hiç sentezlenmediği için ancak ileri evre kanserlerde mutasyonla ortaya çıkan bir tümöre özgü antijendir."
            ],
            "answer": "B",
            "explanation": "Karsinoembriyonik Antijen (CEA), onkofetal bir glikoproteindir. Fetal bağırsakta üretilir, erişkinde susturulur, kolorektal karsinomda yeniden sentezlenir. Fetal dönemde var olduğu için konakta tam tolerans mevcuttur; bu nedenle immünojenitesi zayıftır ve taramada değil takipte kullanılır. Başarılı cerrahi sonrası normale inen CEA'nın takiplerde belirgin ve ilerleyici artış göstermesi, en sık karaciğer metastazı olmak üzere tümör nüksünün en güvenilir ve erken biyokimyasal kanıtıdır.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    }
]
