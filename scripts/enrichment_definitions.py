"""
Enrichment definitions for Decks 37, 38, 39, 40, 41.
Contains high-yield interactive elements tailored to each checkpoint and milestone slide.
"""

D37_ENRICHMENTS = {
    10: [
        {
            "type": "causal_chain",
            "title": "Nefrotik Sendromda Masif Ödem Oluşum Zinciri",
            "steps": [
                "1. Podosit slit diyafram veya GBM negatif elektrik yükü hasara uğrar.",
                "2. Plazma proteinlerine karşı filtrasyon bariyeri geçirgenliği artar ve masif albüminüri gelişir.",
                "3. Serum albümin düzeyi düşer ve intravasküler onkotik basınç dramatik azalır.",
                "4. Sıvı damar içinden interstisyel aralığa geçerek hipovolemiyi tetikler.",
                "5. RAAS sistemi ve ADH aktive olarak sekonder su-tuz retansiyonu ve anazarka ödemi oluşturur."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Nefrotik sendrom tanısında erişkinler için kardinal eşik değer 24 saatlik idrarla [≥3,5 g/gün] protein atılımıdır.",
            "maskedTerm": "≥3,5 g/gün",
            "hint": "Erişkinde nefrotik düzey proteinüri miktarı"
        },
        {
            "type": "interactive_table",
            "title": "Nefrotik Sendromun Dört Kardinal Bulgusu ve Mekanizması",
            "tableHeaders": ["Kardinal Bulgu", "Klinik Eşik / Özellik", "Altta Yatan Patofizyolojik Mekanizma"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Masif Proteinüri"},
                        {"text": "≥3,5 g/gün/1,73 m²", "isMasked": True, "hint": "Kriter parametresi"},
                        {"text": "GBM ve podosit slit diyafram negatif yük ve por geçirgenlik artışı"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Hipoalbüminemi"},
                        {"text": "Serum albümini <3 g/dL", "isMasked": True, "hint": "Kandaki albümin sınırı"},
                        {"text": "İdrarla aşırı albümin kaybının hepatik sentez kapasitesini aşması"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Yaygın Ödem (Anazarka)"},
                        {"text": "Periorbital ve pretibial belirgin", "isMasked": True, "hint": "Karakteristik anatomik bölge"},
                        {"text": "Plazma onkotik basınç düşüşü ve sekonder RAAS su-tuz retansiyonu"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Hiperlipidemi / Lipidüri"},
                        {"text": "Serum kolesterol ve trigliserid artışı", "isMasked": True, "hint": "Kan yağları tablosu"},
                        {"text": "Hipoalbüminemiye yanıt olarak hepatik lipoprotein sentezi artışı ve katabolizma azalması"}
                    ]
                }
            ]
        }
    ],
    20: [
        {
            "type": "before_after_slider",
            "title": "Primer ve Sekonder Nefrotik Sendrom Karşılaştırması",
            "leftTitle": "Primer Glomerülopatiler",
            "rightTitle": "Sekonder Glomerülopatiler",
            "leftPoints": [
                "Hastalık doğrudan glomerülü hedef alır ve primer böbrek parankimiyle sınırlıdır.",
                "En sık nedenler Minimal Değişiklik Hastalığı, FSGS ve Membranöz Nefropatidir.",
                "Tanı anında sistemik otoimmün serolojiler ve metabolik belirteçler genellikle negatiftir."
            ],
            "rightPoints": [
                "Sistemik bir hastalığın böbrek glomerüllerinde oluşturduğu hasarlanmadır.",
                "En sık nedenler Diyabetes Mellitus, Renal Amiloidoz ve Sistemik Lupus Eritematozustur.",
                "Klinik tabloda ekstrarenal organ tutulumları ve spesifik serolojik antikorlar eşlik eder."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Minimal Değişiklik Hastalığı çocukluk çağı nefrotik sendromlarının [%90]'ından fazlasından sorumludur.",
            "maskedTerm": "%90",
            "hint": "Pediatrik nefrotik olguların ezici çoğunluk oranı"
        },
        {
            "type": "active_recall",
            "question": "Minimal Değişiklik Hastalığında ışık mikroskobunda glomerüller neden normal izlenir?",
            "answer": "Çünkü hasar ışık mikroskobu çözünürlüğü altındaki podosit ayaksı çıkıntılarının (pedisel) ultra-yapısal düzeyde silinmesiyle sınırlıdır; hücresel proliferasyon veya skleroz yoktur."
        }
    ],
    30: [
        {
            "type": "causal_chain",
            "title": "Minimal Değişiklik Hastalığında Selektif Proteinüri Mekanizması",
            "steps": [
                "1. T lenfosit kaynaklı sitokinler podosit hücre iskeletinde hasar meydana getirir.",
                "2. Glomerüler bazal membrandaki polianyonik heparan sülfat negatif elektrik yükü kaybolur.",
                "3. Negatif yüklü küçük plazma proteini albümin elektrostatik itilme kalktığı için idrara sızar.",
                "4. İmmünglobulinler gibi büyük moleküllü proteinler bariyeri geçemez ve selektif albüminüri oluşur.",
                "5. Kortikosteroid tedavisi sitokin üretimini keserek podosit pedisellerini normale döndürür."
            ]
        },
        {
            "type": "branching_logic",
            "scenario": "3 yaşında erkek çocuk, ani başlayan göz çevresi ve pretibial ödem tablosuyla getiriliyor. İdrarda masif selektif albüminüri (4 g/gün) ve mikroskopide normal ışık mikroskopisi bekleniyor. Bu hastada ilk basamak klinik yönetim ne olmalıdır?",
            "options": [
                {
                    "text": "Oral kortikosteroid tedavisi (Prednizolon) başlanarak klinik remisyon izlenmelidir.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; çocukluk çağı nefrotik sendromunda MDH %90 oranında sorumludur ve steroid tedavisine mükemmel yanıt (>%90 remisyon) verir; biyopsi ilk etapta endike değildir."
                },
                {
                    "text": "Derhal perkütan böbrek biyopsisi yapılmadan hiçbir ilaç verilmemelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; çocuklarda tipik MDH kliniğinde steroid yanıtı beklenir, böbrek biyopsisi steroide dirençli olgularda yapılır."
                },
                {
                    "text": "Hemen hemodiyaliz ve agresif plazmaferez uygulanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; MDH akut hemodiyaliz endikasyonu taşımaz, kortikosteroidle hızla geriler."
                }
            ]
        }
    ],
    40: [
        {
            "type": "before_after_slider",
            "title": "Minimal Değişiklik Hastalığı (MDH) ile FSGS Morfolojik Ayrımı",
            "leftTitle": "Minimal Değişiklik Hastalığı (MDH)",
            "rightTitle": "Fokal Segmental Glomerüloskleroz (FSGS)",
            "leftPoints": [
                "Işık mikroskobunda glomerüller tamamen normal morfolojide izlenir.",
                "Proteinüri son derece selektiftir (temelde sadece albümin kaçağı vardır).",
                "Kortikosteroid tedavisine mükemmel yanıt verir (>%90 tam yanıt).",
                "Son dönem böbrek yetmezliğine ilerleme riski yok denecek kadar azdır."
            ],
            "rightPoints": [
                "Işık mikroskobunda bazı glomerüllerin bazı lobüllerinde segmental skleroz izlenir.",
                "Proteinüri non-selektiftir (albümin ve büyük moleküllü globulinler birlikte kaçar).",
                "Kortikosteroid tedavisine zayıf veya dirençli yanıt verir (<%20-30).",
                "Hastaların önemli kısmı 10 yıl içinde son dönem böbrek yetmezliğine (SDBY) ilerler."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Fokal Segmental Glomerüloskleroz patolojisinde etkilenen glomerüller fokal yani [bazı glomerüller] ve segmental yani tek bir glomerülün bazı lobülleri tutulacak şekildedir.",
            "maskedTerm": "bazı glomerüller",
            "hint": "Fokal teriminin doku dağılımındaki karşılığı"
        },
        {
            "type": "active_recall",
            "question": "FSGS tanılı bir hastaya renal transplantasyon yapıldığında hastalığın yeni böbrekte nüks etme olasılığı nedir ve altta yatan etken nedir?",
            "answer": "Nüks oranı %25-50 arasındadır; altta yatan neden dolaşımdaki podosit geçirgenlik faktörleridir (örneğin suPAR)."
        }
    ],
    50: [
        {
            "type": "causal_chain",
            "title": "Primer Membranöz Nefropatide Subepitelyal İmmün Hasar Zinciri",
            "steps": [
                "1. Dolaşımdaki otoantikorlar podosit yüzeyindeki PLA2R antijenine in situ bağlanır.",
                "2. Podosit ile bazal membran arasında subepitelyal immün kompleksler çöker.",
                "3. Kompleman sistemi aktive olarak C5b-9 membran atak kompleksini (MAC) kurar.",
                "4. Podositler hasara uğrayarak ekstrasellüler matriks üretir ve depozitlerin etrafını sarar.",
                "5. Glomerüler filtrasyon bariyerinde diffüz kalınlaşma ve masif non-selektif proteinüri oluşur."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Membranöz Nefropati Etiyolojik Sınıflandırması",
            "tableHeaders": ["Kategori", "Temel Nedenler / Antijenler", "Önemli Klinik ve Biyolojik Özellik"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Primer (İdiyopatik) MN"},
                        {"text": "Anti-PLA2R otoantikorları (%70-80)", "isMasked": True, "hint": "Primer formdaki ana hedef podosit reseptörü"},
                        {"text": "Erişkinlerde en sık primer nefrotik nedenlerinden biri"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sekonder İnfeksiyöz MN"},
                        {"text": "Hepatit B ve Hepatit C virüsleri", "isMasked": True, "hint": "Sık ilişkili viral etkenler"},
                        {"text": "Viral antijen-antikor komplekslerinin glomerüler birikimi"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sekonder Malignite İlişkili"},
                        {"text": "Akciğer, GIS karsinomları ve melanom", "isMasked": True, "hint": "Yaşlı hastalarda taranması gereken neoplazmlar"},
                        {"text": "Tümör antijenlerine karşı oluşan immün kompleksler"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sekonder Otoimmün / İlaç"},
                        {"text": "SLE, NSAİİ, penisilamin ve altın tuzları", "isMasked": True, "hint": "Lupus ve nefrotoksik antiromatizmal ajanlar"},
                        {"text": "Etiyolojik ajanın kesilmesiyle remisyona girebilir"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Erişkinlerde primer membranöz nefropati vakalarının yaklaşık %70-80'inde podosit yüzeyindeki [fosfolipaz A2 reseptörü] (PLA2R) antijenine karşı otoantikorlar saptanır.",
            "maskedTerm": "fosfolipaz A2 reseptörü",
            "hint": "Primer membranöz nefropatideki podosit hedef reseptörü"
        }
    ],
    60: [
        {
            "type": "before_after_slider",
            "title": "Membranöz Nefropati Morfolojik Özellikleri",
            "leftTitle": "Işık Mikroskopisi ve Gümüş Boyası",
            "rightTitle": "İmmünfloresan (IF) ve Elektron Mikroskopisi (EM)",
            "leftPoints": [
                "Diffüz ve homojen GBM kalınlaşması izlenir; hiposellülerdir.",
                "Gümüş boyamasında subepitelyal birikimler arasında 'spike and dome' (diken ve kubbe) görünümü saptanır.",
                "Glomerül kapiller lümenleri açıktır ve hücresel proliferasyon görülmez."
            ],
            "rightPoints": [
                "IF mikroskobunda GBM boyunca diffüz granüler IgG ve C3 birikimi izlenir.",
                "EM'de podosit tabanında subepitelyal elektron-yoğun depozitler görülür.",
                "Podosit ayaksı çıkıntılarında immün depozitlerin üzerinde yaygın silinme izlenir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Membranöz nefropatide gümüşleme boyamasında bazal membran materyalinin immün depozitlerin arasından dışarı doğru uzanmasıyla [spike and dome] yani diken ve kubbe manzarası oluşur.",
            "maskedTerm": "spike and dome",
            "hint": "Gümüş boyamasındaki meşhur morfolojik terim"
        },
        {
            "type": "branching_logic",
            "scenario": "58 yaşında erkek hasta, bacaklarda şişlik ve 6 g/gün nefrotik proteinüri ile başvuruyor. Böbrek biyopsisinde gümüş boyasında subepitelyal spikeler ve diffüz granüler IgG birikimi saptanıyor. Yaş ve klinik dikkate alındığında hastanın etiyolojik araştırmasında mutlaka yapılması gereken adım ne olmalıdır?",
            "options": [
                {
                    "text": "Hastada yaşa uygun malignite taraması (akciğer grafisi/BT, kolonoskopi vb.) yapılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; ileri yaşta membranöz nefropati vakalarının önemli bir kısmı gizli karsinomlara (akciğer, kolon, mide) sekonder gelişir."
                },
                {
                    "text": "Sadece akut apandisit yönünden cerrahi muayene yapılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; membranöz nefropati yaşlılarda malignite ile ilişkili olabilir, akut batınla ilgili değildir."
                },
                {
                    "text": "Biyopsi sonucu kesinleştiği için hiçbir ek tetkik yapılmadan taburcu edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; sekonder etiyolojiler (kanser, hepatit, SLE) taranmadan takip yetersiz kalır."
                }
            ]
        }
    ],
    70: [
        {
            "type": "causal_chain",
            "title": "MPGN Tip 1'de Çift Kontur (Tramvay Rayı) Gelişimi",
            "steps": [
                "1. Dolaşımdaki immün kompleksler glomerül kapiller subendotelyal aralığında çöker.",
                "2. Kompleman aktivasyonu ile mezanjiyal ve endotelyal hücre proliferasyonu tetiklenir.",
                "3. Mezanjiyal hücre uzantıları kapiller duvar boyunca bazal membran altına sokulur (mezanjiyal interpozisyon).",
                "4. İnterpoze hücreler yeni bazal membran matriksi sentezleyerek lümeni daraltır.",
                "5. Gümüş boyamasında GBM'de çift hatlı tramvay rayı (tram-track) görünümü oluşur."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "MPGN Tip 1'de mezanjiyal hücrelerin GBM ile endotel arasına sokulması olayına [mezanjiyal interpozisyon] adı verilir.",
            "maskedTerm": "mezanjiyal interpozisyon",
            "hint": "Hücre uzantılarının araya girmesini tanımlayan patolojik terim"
        },
        {
            "type": "active_recall",
            "question": "MPGN Tip 1 etiyolojisinde en sık rol oynayan sistemik viral enfeksiyon ve immünolojik bozukluk hangisidir?",
            "answer": "Hepatit C virüsü (HCV) enfeksiyonu ve buna bağlı gelişen Tip II mikst kriyoglobulinemidir."
        }
    ],
    80: [
        {
            "type": "interactive_table",
            "title": "MPGN Tip 1 ile C3 Glomerülopatisi (Yoğun Birikim Hastalığı - DDD) Karşılaştırması",
            "tableHeaders": ["Özellik", "MPGN Tip 1 (İmmün Kompleks)", "Yoğun Birikim Hastalığı (C3 Glomerülopatisi)"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Depozit Lokalizasyonu"},
                        {"text": "Subendotelyal depozitler", "isMasked": True, "hint": "Endotel altı birikim yeri"},
                        {"text": "GBM laminası içinde intramembranöz yoğun bant"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan Patern"},
                        {"text": "Granüler IgG ve C3 pozitifliği", "isMasked": True, "hint": "Klasik immün depozit bileşimi"},
                        {"text": "Yalnızca yoğun C3 pozitif; IgG negatif"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Altta Yatan Mekanizma"},
                        {"text": "İmmün kompleks birikimi (HCV vb.)", "isMasked": True, "hint": "Kardinal antijen-antikor süreci"},
                        {"text": "Alternatif kompleman yolu düzensizliği (C3NeF otoantikoru)"}]
                },
                {
                    "cells": [
                        {"text": "Serum Kompleman Düzeyi"},
                        {"text": "C3 ve C4 sıklıkla birlikte düşük", "isMasked": True, "hint": "Klasik yol tüketimi"},
                        {"text": "C3 dramatik düşüktür; C4 genellikle normaldir"}
                    ]
                }
            ]
        },
        {
            "type": "active_recall",
            "question": "Yoğun Birikim Hastalığında (Dense Deposit Disease) alternatif yol C3 konvertaz enzimini stabilize ederek C3'ün sürekli tüketilmesine yol açan otoantikor hangisidir?",
            "answer": "C3 Nefritik Faktör (C3NeF)."
        },
        {
            "type": "cloze_masking",
            "sentence": "Yoğun Birikim Hastalığında elektron mikroskobunda GBM lamina densasında karakteristik olarak [intramembranöz kurdele benzeri] elektron-yoğun birikimler izlenir.",
            "maskedTerm": "intramembranöz kurdele benzeri",
            "hint": "Lamina densa içindeki tipik bant morfolojisi"
        }
    ],
    90: [
        {
            "type": "causal_chain",
            "title": "Nefrotik Sendromda Renal Ven Trombozu ve Tromboemboli Mekanizması",
            "steps": [
                "1. Glomerüler permeabilite artışı nedeniyle antitrombin III idrarla masif olarak kaybedilir.",
                "2. Plazmada protein C ve protein S düzeyleri düşerken karaciğerde fibrinojen sentezi artar.",
                "3. Trombosit agregabilitesi ve eritrosit viskozitesi belirgin şekilde yükselir.",
                "4. İntravasküler alanda hiperkoagülabilite (trombofili) tablosu yerleşir.",
                "5. Membranöz nefropati başta olmak üzere nefrotik hastalarda renal ven trombozu ve pulmoner emboli riski zirve yapar."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Diyabetik Glomerüloskleroz ve Renal Amiloidoz Ayırıcı Özellikleri",
            "tableHeaders": ["Patolojik Özellik", "Diyabetik Glomerüloskleroz", "Renal Amiloidoz"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Tipik Işık Mikroskopisi"},
                        {"text": "Kimmelstiel-Wilson nodülleri (nodüler glomerüloskleroz)", "isMasked": True, "hint": "Diyabete özgü mezanjiyal nodül ismi"},
                        {"text": "Mezanjiyum ve damar duvarlarında amorf asellüler hyalin birikim"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Özel Histokimyasal Boya"},
                        {"text": "PAS pozitif nodüller ve GBM kalınlaşması", "isMasked": True, "hint": "Karbohidrattan zengin bazal membran boyası"},
                        {"text": "Kongo kırmızısı ile polarize ışıkta elma yeşili çift kırınım"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Klinik Seyir"},
                        {"text": "Mikroalbüminüri -> Aşikar proteinüri -> SDBY", "isMasked": True, "hint": "Diyabetik renal progresyon sırası"},
                        {"text": "Masif nefrotik proteinüri ve böbrek boyutlarında büyüme"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Nefrotik sendromlu hastalarda hiperkoagülabilite gelişmesinde en kritik etken antikoagülan bir molekül olan [antitrombin III] düzeyinin idrarla kaybedilmesidir.",
            "maskedTerm": "antitrombin III",
            "hint": "İdrarla yitirilen ana doğal antikoagülan faktör"
        }
    ],
    100: [
        {
            "type": "interactive_table",
            "title": "Primer Glomerüler Nefrotik Hastalıklar Master Karşılaştırma Matrisi",
            "tableHeaders": ["Hastalık", "Işık Mikroskopisi (LM)", "İmmünfloresan (IF)", "Elektron Mikroskopisi (EM)", "Steroid Yanıtı"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Minimal Değişiklik Hastalığı (MDH)"},
                        {"text": "Tamamen normal glomerüller"},
                        {"text": "Negatif"},
                        {"text": "Podosit ayak çıkıntılarında yaygın silinme (effacement)", "isMasked": True, "hint": "MDH'deki tek ultra-yapısal hasar"},
                        {"text": "Mükemmel (>%90)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Fokal Segmental Glomerüloskleroz (FSGS)"},
                        {"text": "Bazı glomerüllerde segmental skleroz ve hyalinozis"},
                        {"text": "Non-spesifik IgM ve C3 birikimi"},
                        {"text": "Sklerotik segmentlerde podosit soyulması ve silinme", "isMasked": True, "hint": "Podosit kaybı ve çıplak bazal membran"},
                        {"text": "Kötü / Dirençli"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Membranöz Nefropati (MN)"},
                        {"text": "Diffüz GBM kalınlaşması, gümüşte spike and dome"},
                        {"text": "Diffüz granüler IgG ve C3 birikimi"},
                        {"text": "Subepitelyal elektron-yoğun depozitler", "isMasked": True, "hint": "Podosit altında biriken depozit sahası"},
                        {"text": "Değişken / Parsiyel"}
                    ]
                },
                {
                    "cells": [
                        {"text": "MPGN Tip 1"},
                        {"text": "Lobülasyon artışı, mezanjiyoproliferasyon, çift kontur"},
                        {"text": "Granüler IgG ve C3 birikimi"},
                        {"text": "Subendotelyal depozitler ve mezanjiyal interpozisyon", "isMasked": True, "hint": "Endotel altı birikim ve araya giren hücreler"},
                        {"text": "Genellikle zayıf"}
                    ]
                }
            ]
        },
        {
            "type": "branching_logic",
            "scenario": "45 yaşında nefrotik sendrom tanısıyla izlenen bir hastada ani başlayan sol yan ağrısı, gross hematüri ve sol varikosel saptanıyor. Proteinüri düzeyinde artış ve serum kreatinininde yükselme saptanıyor. Bu klinik tabloda öncelikle ne düşünülmeli ve ilk yaklaşım ne olmalıdır?",
            "options": [
                {
                    "text": "Renal ven trombozu düşünülmeli; Doppler ultrasonografi/BT anjiyografi ile tanı doğrulanıp derhal antikoagülan tedavi başlanmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; nefrotik sendromda antitrombin III kaybı nedeniyle renal ven trombozu riski yüksektir; ani yan ağrısı, hematüri ve sol varikosel renal ven oklüzyonunun klasik triadıdır."
                },
                {
                    "text": "Akut apandisit düşünülmeli ve acil cerrahi konsültasyon istenmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; sol yan ağrısı ve varikosel ile apandisitin hiçbir ilgisi yoktur, nefrotik tromboemboli akla gelmelidir."
                },
                {
                    "text": "Minimal değişiklik hastalığı alevlenmesi düşünülerek steroid dozu iki katına çıkarılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; akut hematüri ve yan ağrısı vasküler trombotik bir komplikasyondur, acil antikoagülasyon gerektirir."
                }
            ]
        }
    ]
}

D38_ENRICHMENTS = {
    10: [
        {
            "type": "causal_chain",
            "title": "Nefritik Sendromda Hipertansiyon ve Oligüri Mekanizması",
            "steps": [
                "1. Glomerül endotel ve mezanjiyumunda enflamasyon ve lökosit infiltrasyonu gelişir.",
                "2. Kapiller lümenler tıkanır ve glomerüler filtrasyon debisi (GFR) ani düşüşe geçer.",
                "3. Sıvı ve tuz atılımının bozulmasıyla oligüri ve intravasküler volüm genişlemesi oluşur.",
                "4. Hipervolemi ve renin baskılanmasıyla karakterize volüm bağımlı hipertansiyon ortaya çıkar.",
                "5. Hasarlı kapiller duvardan eritrositlerin idrara sızmasıyla dismorfik hematüri ve eritrosit silendirleri şekillenir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "İdrar mikroskopisinde saptanan [eritrosit silendirleri] hematürinin alt üriner sistemden değil, kesinlikle glomerülden kaynaklandığını kanıtlar.",
            "maskedTerm": "eritrosit silendirleri",
            "hint": "Glomerüler hematürinin idrar sedimentindeki patognomonik kanıtı"
        },
        {
            "type": "interactive_table",
            "title": "Nefrotik Sendrom ile Nefritik Sendrom Kardinal Farkları",
            "tableHeaders": ["Parametre", "Nefrotik Sendrom", "Nefritik Sendrom"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Proteinüri Düzeyi"},
                        {"text": "Masif (>3,5 g/gün)", "isMasked": True, "hint": "Nefrotik düzey protein kaçağı"},
                        {"text": "Subnefrotik (<3,5 g/gün, genelde 1-2 g/gün)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İdrar Sedimenti"},
                        {"text": "Lipid damlacıkları, oval yağ cisimcikleri", "isMasked": True, "hint": "Nefrotik idrardaki lipidik yapılar"},
                        {"text": "Dismorfik eritrositler ve eritrosit silendirleri"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Kan Basıncı"},
                        {"text": "Normal veya hafif değişken", "isMasked": True, "hint": "Nefrotik tansiyon durumu"},
                        {"text": "Sıklıkla belirgin hipertansiyon (sıvı yükü ilişkili)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "GFR ve Azotemi"},
                        {"text": "Genellikle korunmuştur (erken dönemde)", "isMasked": True, "hint": "Erken nefrotik süzme hızı"},
                        {"text": "GFR düşüktür; oligüri ve azotemi (üre/kreatinin artışı) belirgindir"}
                    ]
                }
            ]
        }
    ],
    20: [
        {
            "type": "causal_chain",
            "title": "Akut Poststreptokoksik Glomerulonefrit (APSGN) İmmün Hasar Zinciri",
            "steps": [
                "1. A grubu beta-hemolitik streptokokların nefritojenik suşları farenjit veya cilt enfeksiyonu yapar.",
                "2. Bakteriyel antijenler (SpeB, NAPIr) dolaşıma karışarak glomerül bazal membranına ekilir.",
                "3. 1-4 haftalık latent periyotta antijenlere karşı dolaşımda antikorlar sentezlenir.",
                "4. Glomerülde in situ immün kompleksler oluşur ve klasik kompleman yolu hızla aktive olur.",
                "5. Nötrofil ve monosit infiltrasyonu ile endokapiller proliferatif nefrit ve klinik hematüri başlar."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "APSGN'de streptokoksik farenjit enfeksiyonu ile nefritik sendrom başlangıcı arasındaki latent periyot ortalama [1-3 hafta] kadardır.",
            "maskedTerm": "1-3 hafta",
            "hint": "Farenjit sonrası nefrit çıkış süresi"
        },
        {
            "type": "active_recall",
            "question": "APSGN patogenezinde rol oynayan nefritojenik streptokok antijenleri nelerdir?",
            "answer": "Streptokoksik pirojenik ekzotoksin B (SpeB) ve Nefritle ilişkili plazmin reseptörüdür (NAPIr)."
        }
    ],
    30: [
        {
            "type": "before_after_slider",
            "title": "APSGN Işık Mikroskopisi ile Elektron Mikroskopisi Farkları",
            "leftTitle": "Işık Mikroskopisi (LM)",
            "rightTitle": "Elektron Mikroskopisi (EM)",
            "leftPoints": [
                "Diffüz endokapiller proliferatif ve eksüdatif glomerülonefrit tablosu izlenir.",
                "Glomerül yumakları büyümüş, aşırı sellüler ve kapiller lümenler tıkanmıştır.",
                "Lümenlerde bol miktarda nötrofil lökosit ve monosit infiltrasyonu saptanır."
            ],
            "rightPoints": [
                "Bazal membranın epitelyal tarafında (subepitelyal) devasa hörgüçler izlenir.",
                "Bu karakteristik elektron-yoğun depozitlere subepitelyal 'humps' (hörgüç) adı verilir.",
                "Podosit ayaksı çıkıntılarında bu depozitlerin üzerinde fokal silinmeler görülür."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "APSGN immünfloresan incelemesinde mezanjiyum ve kapiller duvarlar boyunca kaba granüler IgG ve C3 birikimi [yıldızlı gökyüzü] (starry sky) paterni oluşturur.",
            "maskedTerm": "yıldızlı gökyüzü",
            "hint": "İF'deki meşhur astronomik benzetme"
        },
        {
            "type": "branching_logic",
            "scenario": "7 yaşında erkek çocuk, boğaz enfeksiyonundan 12 gün sonra çay rengi idrar, göz kapaklarında şişlik ve 140/90 mmHg tansiyon ile getiriliyor. ASO yüksek, serum C3 düzeyi belirgin düşük bulunuyor. Bu çocukta klinik yönetim ve prognoz beklentisi ne olmalıdır?",
            "options": [
                {
                    "text": "Destekleyici tedavi (sıvı-tuz kısıtlaması, diüretik ve antihipertansif) verilmelidir; çocuklarda prognoz mükemmeldir (>%95 tam iyileşir).",
                    "isCorrect": True,
                    "feedback": "Doğrudur; tipik klinik ve laboratuvara sahip çocuklarda APSGN biyopsisiz destek tedavisiyle kendiliğinden mükemmel remisyona girer."
                },
                {
                    "text": "Acilen acil hemodiyaliz katateri takılarak yüksek doz immünsüpresif sitotoksik tedaviye başlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; çocukluk çağı APSGN olgularının ezici çoğunluğu spontan düzelir, sitotoksik tedavi endike değildir."
                },
                {
                    "text": "Solunum yetmezliği gelişeceği için hemen entübe edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; hastanın solunumu stabil olup nefritik destek tedavisi yeterlidir."
                }
            ]
        }
    ],
    40: [
        {
            "type": "causal_chain",
            "title": "Hızla İlerleyen Glomerülonefritte (RPGN) Hilal (Kresent) Oluşumu",
            "steps": [
                "1. Glomerül bazal membranında şiddetli enflamatuar nekroz ve mikro-yırtıklar oluşur.",
                "2. Plazma proteinleri, fibrinojen ve lökositler Bowman aralığına sızar.",
                "3. Bowman kapsülü parietal epitel hücreleri güçlü proliferasyon uyarısı alır.",
                "4. Bowman aralığına göç eden monosit ve makrofajlar fibrin ağlarıyla birleşerek hücre tabakaları kurar.",
                "5. Kapiller yumağı dıştan ezen hilal (kresent) yapısı oluşarak glomerülü skleroza götürür."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Goodpasture sendromunda otoantikorların hedefi Tip IV kollajenin [alfa-3 zinciri] non-kollajenöz (NC1) alanıdır.",
            "maskedTerm": "alfa-3 zinciri",
            "hint": "Goodpasture otoantikorunun bağlandığı kollajen alt birimi"
        },
        {
            "type": "interactive_table",
            "title": "RPGN'nin Üç İmmünolojik Alt Grubu",
            "tableHeaders": ["RPGN Tipi", "İmmün Mekanizma", "İmmünfloresan Mikroskopisi Patern"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Tip I RPGN (Anti-GBM)"},
                        {"text": "GBM kollajen Tip IV alfa-3 NC1 alanına karşı otoantikor", "isMasked": True, "hint": "Goodpasture hedef antijeni"},
                        {"text": "GBM boyunca kesintisiz lineer (çizgisel) IgG ve C3 birikimi"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Tip II RPGN (İmmün Kompleks)"},
                        {"text": "Dolaşan antijen-antikor komplekslerinin glomerüler birikimi", "isMasked": True, "hint": "Lupus ve APSGN mekanizması"},
                        {"text": "Mezanjiyum ve kapiller duvarlarda kaba granüler birikim"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Tip III RPGN (Pauci-İmmün)"},
                        {"text": "ANCA ilişkili vaskülitler (GPA, MPA) aracılı nötrofil degranülasyonu", "isMasked": True, "hint": "Vaskülit otoantikorları"},
                        {"text": "Floresan negatif veya yok denecek kadar az (pauci-immün)"}
                    ]
                }
            ]
        }
    ],
    50: [
        {
            "type": "before_after_slider",
            "title": "Tip I (Anti-GBM) ile Tip III (Pauci-İmmün) RPGN Karşılaştırması",
            "leftTitle": "Tip I RPGN (Anti-GBM)",
            "rightTitle": "Tip III RPGN (Pauci-İmmün)",
            "leftPoints": [
                "Kanda Anti-GBM otoantikorları pozitiftir.",
                "İmmünfloresan mikroskobunda GBM boyunca kusursuz lineer (çizgisel) boyanma vardır.",
                "Akciğer kanaması eşlik ederse Goodpasture Sendromu adını alır.",
                "Tedavide acil plazmaferez ile dolaşımdaki antikorların uzaklaştırılması esastır."
            ],
            "rightPoints": [
                "Kanda ANCA (p-ANCA / MPO veya c-ANCA / PR3) otoantikorları pozitiftir.",
                "İmmünfloresan mikroskobunda immünglobulin ve kompleman birikimi saptanmaz (pauci).",
                "Sistemik vaskülit bulguları (sinüzit, akciğer nodülleri, purpura vb.) eşlik edebilir.",
                "Tedavide yüksek doz kortikosteroid ve siklofosfamid veya rituksimab kullanılır."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Histopatolojik olarak kresentik glomerülonefrit (RPGN) tanısı koyabilmek için biyopsideki glomerüllerin en az [%50]'sinde hilal formasyonu izlenmelidir.",
            "maskedTerm": "%50",
            "hint": "Kresentik GN tanısı için gereken asgari glomerül tutulum yüzdesi"
        },
        {
            "type": "active_recall",
            "question": "Granülomatoz polianjiitiste (Wegener) en sık pozitifleşen ve Tip III RPGN'ye eşlik eden ANCA türü hangisidir?",
            "answer": "c-ANCA (PR3-ANCA / Proteinaz 3 antikorları)."
        }
    ],
    60: [
        {
            "type": "causal_chain",
            "title": "Lupus Nefriti Sınıf IV Diffüz Proliferatif Glomerülonefrit Patogenezi",
            "steps": [
                "1. SLE hastasında anti-dsDNA ve nükleer antijenlere karşı bol miktarda immün kompleks oluşur.",
                "2. İmmün kompleksler glomerül endoteli altında (subendotelyal) masif şekilde depolanır.",
                "3. Şiddetli kompleman aktivasyonu lökositleri çeker ve kapiller duvarları aşırı kalınlaştırır.",
                "4. Işık mikroskobunda lümenleri tıkayan kalın 'tel halka' (wire-loop) lezyonları gelişir.",
                "5. Glomerüllerin %50'sinden fazlası tutularak ağır nefritik sendrom ve böbrek yetmezliği tablosu oluşur."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Lupus nefriti Sınıf IV'te ışık mikroskobunda masif subendotelyal immün depozitlerin oluşturduğu sert halkasal kalınlaşmaya [tel halka] (wire-loop) lezyonu denir.",
            "maskedTerm": "tel halka",
            "hint": "Lupus nefritindeki meşhur İngilizce tel halka teriminin Türkçesi"
        },
        {
            "type": "interactive_table",
            "title": "ISN/RPS Lupus Nefriti Morfolojik Sınıflandırması",
            "tableHeaders": ["Sınıf", "Patolojik İsimlendirme", "Baskın Klinik Tablo ve Özellik"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Sınıf I"},
                        {"text": "Minimal mezanjiyal lupus nefriti", "isMasked": True, "hint": "En hafif mezanjiyal sınıf"},
                        {"text": "LM normaldir; IF'de mezanjiyal depozitler vardır; asemptomatiktir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sınıf II"},
                        {"text": "Mezanjiyal proliferatif lupus nefriti", "isMasked": True, "hint": "Mezanjiyumda hücre artışlı sınıf"},
                        {"text": "Mezanjiyal hipertrofi ve mikroskobik hematüri/hafif proteinüri"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sınıf III"},
                        {"text": "Fokal proliferatif lupus nefriti (<%50)", "isMasked": True, "hint": "Glomerüllerin yarısından azı tutulan sınıf"},
                        {"text": "Nefritik sendrom başlangıcı, orta derece proteinüri"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sınıf IV"},
                        {"text": "Diffüz proliferatif lupus nefriti (≥%50)", "isMasked": True, "hint": "En sık, en ağır ve en tehlikeli sınıf"},
                        {"text": "Ağır nefritik sendrom, tel halka lezyonları, böbrek yetmezliği riski"}
                    ]
                }
            ]
        }
    ],
    70: [
        {
            "type": "before_after_slider",
            "title": "Lupus Nefriti Sınıf IV ile Sınıf V Karşılaştırması",
            "leftTitle": "Sınıf IV (Diffüz Proliferatif)",
            "rightTitle": "Sınıf V (Membranöz Lupus Nefriti)",
            "leftPoints": [
                "Baskın klinik tablo nefritik sendromdur (hematüri, hipertansiyon, oligüri).",
                "İmmün kompleksler temel olarak subendotelyal aralıkta birikir.",
                "Işık mikroskobunda hiperplasitik proliferasyon ve wire-loop lezyonları izlenir.",
                "Prognozu en kötü sınıftır; agresif immünsüpresyon zorunludur."
            ],
            "rightPoints": [
                "Baskın klinik tablo nefrotik sendromdur (masif proteinüri, ağır ödem).",
                "İmmün kompleksler subepitelyal aralıkta podosit tabanında çöker.",
                "Işık mikroskobunda hücresel proliferasyon olmaksızın diffüz GBM kalınlaşması görülür.",
                "Prognoz membranöz lezyonun derecesine ve tromboz riskine bağlıdır."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Dünyada en sık görülen primer glomerülonefrit türü olan IgA nefropatisinde immün kompleksler özellikle [mezanjiyum] kompartmanında depolanır.",
            "maskedTerm": "mezanjiyum",
            "hint": "IgA depozitlerinin biriktiği anatomik glomerüler alan"
        },
        {
            "type": "active_recall",
            "question": "Lupus nefritinde immünfloresan incelemede IgG, IgA, IgM, C3 ve C1q'nun tümünün birden pozitif saptanması hangi isimle anılır?",
            "answer": "Full-house paterni."
        }
    ],
    80: [
        {
            "type": "interactive_table",
            "title": "IgA Nefropatisi (Berger) ile APSGN Ayırıcı Tanı Kriterleri",
            "tableHeaders": ["Klinik Özellik", "IgA Nefropatisi (Berger Hastalığı)", "Akut Poststreptokoksik GN (APSGN)"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Enfeksiyon ile Başlangıç Süresi"},
                        {"text": "1-2 gün sonra (senfarenjitik hematüri)", "isMasked": True, "hint": "ÜSYE ile eşzamanlı başlangıç süresi"},
                        {"text": "1-3 hafta sonra (postenfeksiyöz latent periyot)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Serum C3 Kompleman Düzeyi"},
                        {"text": "Normaldir (%90 olguda)", "isMasked": True, "hint": "IgA nefropatisinde C3 durumu"},
                        {"text": "Belirgin derecede düşüktür (erken dönemde)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Tekrarlayan Hematüri Atakları"},
                        {"text": "Çok sıktır; her ÜSYE atağında yineler", "isMasked": True, "hint": "Berger rekürrens özelliği"},
                        {"text": "Nadir; tek bir atak halinde geçirilir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan Bulgusu"},
                        {"text": "Mezanjiyumda diffüz granüler IgA birikimi", "isMasked": True, "hint": "Berger'deki tanısal antikor depoziti"},
                        {"text": "Kaba granüler IgG ve C3 birikimi (yıldızlı gökyüzü)"}
                    ]
                }
            ]
        },
        {
            "type": "causal_chain",
            "title": "Alport Sendromunda Glomerül Hasarı Zinciri",
            "steps": [
                "1. Tip IV kollajenin alfa-3, alfa-4 veya alfa-5 zincirini kodlayan genlerde (COL4A5) mutasyon meydana gelir.",
                "2. Glomerüler bazal membranın normal üçlü sarmal kollajen ağ örgüsü kurulamaz.",
                "3. Çocuklukta GBM incelir; zamanla lamina densada tabakalanma ve düzensiz kalınlaşma başlar.",
                "4. Elektron mikroskobunda tipik 'sepet örgüsü' (basket-weave) yarılması ve fragmantasyonu gelişir.",
                "5. Persistan mikroskobik/makroskopik hematüri, sensorinöral sağırlık ve görme bozuklukları eşliğinde böbrek yetmezliği gelişir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "IgA nefropatisinin deri purpurası, karın ağrısı ve artrit gibi sistemik vaskülit bulgularıyla seyreden formu [Henoch-Schönlein purpurası] (IgA vasküliti) olarak adlandırılır.",
            "maskedTerm": "Henoch-Schönlein purpurası",
            "hint": "IgA aracılı lökositoklastik sistemik vaskülit sendromu"
        }
    ],
    90: [
        {
            "type": "interactive_table",
            "title": "Nefritik Sendromda Serum C3 Kompleman Düzeyine Göre Ayırıcı Tanı",
            "tableHeaders": ["Kompleman Profili", "Hastalık Grupları", "Klinik ve Serolojik Doğrulama"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Düşük Serum C3 (Hipokomplemantemi)"},
                        {"text": "APSGN, Lupus Nefriti, MPGN ve Endokardit Nefriti", "isMasked": True, "hint": "Komplemanı tüketen nefritik hastalıklar"},
                        {"text": "Klasik veya alternatif kompleman yolunun aşırı tüketimi"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Normal Serum C3 (Normokomplemantemi)"},
                        {"text": "IgA Nefropatisi, Anti-GBM (Goodpasture) ve Pauci-İmmün RPGN", "isMasked": True, "hint": "C3'ü tüketmeyen nefritler"},
                        {"text": "Sistemik kompleman tüketimi yoktur; serolojide IgA, Anti-GBM veya ANCA aranır"}
                    ]
                }
            ]
        },
        {
            "type": "before_after_slider",
            "title": "Glomerüler Hematüri ile Ekstraglomerüler Hematüri Ayrımı",
            "leftTitle": "Glomerüler Hematüri",
            "rightTitle": "Ekstraglomerüler Hematüri",
            "leftPoints": [
                "İdrar rengi koyu kahverengi, kola veya çay rengindedir.",
                "İdrarda eritrosit silendirleri (RBC casts) mevcuttur.",
                "Faz kontrast mikroskopisinde dismorfik eritrositler (>%80) ve akantositler izlenir.",
                "Eşlik eden subnefrotik veya nefrotik düzeyde proteinüri sıktır."
            ],
            "rightPoints": [
                "İdrar rengi parlak kırmızı veya pembe renktedir.",
                "İdrarda eritrosit silendirleri kesinlikle bulunmaz.",
                "Faz kontrast mikroskopisinde eritrositler normal bikonkav (izomorfik) yapıdadır.",
                "Kan pıhtıları (koagülüm) görülebilir; taş veya tümör lehinedir."
            ]
        },
        {
            "type": "branching_logic",
            "scenario": "22 yaşında üniversite öğrencisi, şiddetli boğaz ağrısı ve ateş başladıktan tam 24 saat sonra parlak kırmızı/kola renkli idrar yaptığını fark ederek acil servise geliyor. Tansiyonu normal, serum kreatinini ve serum C3 kompleman düzeyi normal sınırlarda saptanıyor. Bu klinik tabloda en olası tanı ve yaklaşım ne olmalıdır?",
            "options": [
                {
                    "text": "IgA Nefropatisi (senfarenjitik hematüri); hastaya tanı anlatılmalı, renal fonksiyonlar ve proteinüri takibe alınmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; ÜSYE ile aynı anda veya 1-2 gün içinde ortaya çıkan makroskopik hematüri ve normal C3 düzeyi IgA nefropatisinin (Berger) en tipik klinik tablosudur."
                },
                {
                    "text": "Kesinlikle APSGN'dir; 10 gün önceki latent enfeksiyon hasta tarafından unutulmuştur ve acil steroid başlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; APSGN'de latent süre 1-3 haftadır ve serum C3 belirgin düşüktür; bu hastada süre 24 saattir ve C3 normaldir."
                },
                {
                    "text": "Goodpasture sendromu olduğu için acilen plazmaferez ünitesine sevk edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; izole senfarenjitik hematüride genç hastada Goodpasture değil IgA nefropatisi düşünülür."
                }
            ]
        }
    ],
    100: [
        {
            "type": "interactive_table",
            "title": "Nefritik Sendrom Nedenleri Master Karşılaştırma Matrisi",
            "tableHeaders": ["Hastalık", "Tipik Klinik Profil", "LM Bulgusu", "İmmünfloresan (IF)", "C3 Düzeyi"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "APSGN"},
                        {"text": "Çocuk, farenjitten 1-3 hafta sonra çay rengi idrar, ödem, HT"},
                        {"text": "Diffüz endokapiller proliferasyon ve nötrofiller"},
                        {"text": "Kaba granüler IgG ve C3 (yıldızlı gökyüzü)", "isMasked": True, "hint": "APSGN immünfloresan motifi"},
                        {"text": "Belirgin düşük"}
                    ]
                },
                {
                    "cells": [
                        {"text": "IgA Nefropatisi (Berger)"},
                        {"text": "Genç erkek, ÜSYE'den 1-2 gün sonra rekürren hematüri"},
                        {"text": "Fokal veya diffüz mezanjiyal proliferasyon"},
                        {"text": "Diffüz granüler mezanjiyal IgA birikimi", "isMasked": True, "hint": "Berger tanı koydurucu antikor birikimi"},
                        {"text": "Normal"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Anti-GBM (Goodpasture)"},
                        {"text": "Hızla ilerleyen böbrek yetmezliği ± hemoptizi"},
                        {"text": "Glomerüllerde nekroz ve yaygın kresent (%50)"},
                        {"text": "GBM boyunca kesintisiz lineer IgG", "isMasked": True, "hint": "Anti-GBM çizgisel florasanı"},
                        {"text": "Normal"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Lupus Nefriti (Sınıf IV)"},
                        {"text": "Genç kadın, SLE bulguları, ağır nefritik sendrom"},
                        {"text": "Diffüz proliferasyon, wire-loop lezyonları"},
                        {"text": "Full-house paterni (IgG, IgA, IgM, C3, C1q)", "isMasked": True, "hint": "Lupus floresanındaki tüm antikorlar"},
                        {"text": "Düşük"}
                    ]
                }
            ]
        },
        {
            "type": "active_recall",
            "question": "İnce Bazal Membran Hastalığında (Benign Familyal Hematüri) renal prognoz nasıldır ve böbrek yetmezliği gelişir mi?",
            "answer": "Prognoz mükemmeldir; mikroskobik hematüri kalıcı olsa da hipertansiyon, proteinüri veya böbrek yetmezliği gelişmez."
        }
    ]
}

D39_ENRICHMENTS = {
    10: [
        {
            "type": "interactive_table",
            "title": "Üriner Sistem Enfeksiyonlarında Tanısal Bakteriüri Eşik Değerleri",
            "tableHeaders": ["Klinik Durum / Örnek Türü", "Tanısal Bakteri Eşiği (CFU/mL)", "Klinik Anlam ve Önem"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Klasik Asemptomatik / Genel Eşik (Kass Kriteri)"},
                        {"text": "≥10⁵ CFU/mL (orta akım idrar)", "isMasked": True, "hint": "Geleneksel Kass bakteriüri sınırı"},
                        {"text": "İki ardışık örnekte aynı bakterinin üremesiyle anlamlıdır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Akut Komplike Olmayan Sistitli Kadın"},
                        {"text": "≥10² - 10³ CFU/mL", "isMasked": True, "hint": "Semptomatik kadında düşük eşik"},
                        {"text": "Tipik dizüri ve sıklık varlığında düşük konsantrasyon enfeksiyonu doğrular"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Akut Piyelonefrit veya Erkek Hasta"},
                        {"text": "≥10⁴ CFU/mL", "isMasked": True, "hint": "Piyelonefrit ve erkekte eşik"},
                        {"text": "Ateş ve yan ağrısı olan hastada tanı koydurucudur"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Suprapubik Aspirasyon (Steril Ponksiyon)"},
                        {"text": "Herhangi bir sayıda bakteri (≥1 CFU/mL)", "isMasked": True, "hint": "Steril mesane ponksiyonundaki eşik"},
                        {"text": "Mesane sterildir; tek bir koloni bile mutlak patolojiktir"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "İdrar çubuğu (dipstick) testinde gram-pozitif bakteriler ve enterokoklar nitrat redüktaz enzimine sahip olmadıkları için [nitrit testi] yalancı negatif sonuç verir.",
            "maskedTerm": "nitrit testi",
            "hint": "Bakteriyel redüktazın saptandığı tarama reaktifi"
        },
        {
            "type": "causal_chain",
            "title": "Üriner Dipstick Testinde Kimyasal Reaksiyon Zinciri",
            "steps": [
                "1. Üropatojen bakteriler idrardaki diyetsel nitratı nitrit bileşiğine indirger.",
                "2. İdrar çubuğundaki test pedi nitrit ile pembe renk reaksiyonu verir.",
                "3. Nötrofiller ortama lökosit esteraz enzimi salgılar.",
                "4. Test pedindeki ester substratının hidrolizi ile piyüri doğrulanır.",
                "5. Nitrit ve lökosit esteraz birlikte pozitif olduğunda ÜSE olasılığı %90'ın üzerine çıkar."
            ]
        }
    ],
    20: [
        {
            "type": "before_after_slider",
            "title": "Komplike Olmayan ÜSE ile Komplike ÜSE Karşılaştırması",
            "leftTitle": "Komplike Olmayan ÜSE",
            "rightTitle": "Komplike ÜSE",
            "leftPoints": [
                "Üriner sistemde yapısal veya fonksiyonel bozukluğu olmayan sağlıklı bireylerde gelişir.",
                "Tipik hasta grubu premenopozal, gebe olmayan, cinsel aktif genç kadınlardır.",
                "Ezici çoğunlukla etken antibiyotiğe duyarlı Escherichia coli suşlarıdır (%75-95).",
                "Kısa süreli standart ampirik oral antibiyotik tedavisiyle tamamen iyileşir."
            ],
            "rightPoints": [
                "Taş, sonda, obstrüksiyon, erkek cinsiyet, gebelik, diyabet veya immünsüpresyon eşlik eder.",
                "Dirençli bakteriler (Pseudomonas, Enterococcus, Proteus, Klebsiella, ESBL+) sıktır.",
                "Bakteriyel invazyon, böbrek parankim hasarı ve ürosepsis gelişme riski yüksektir.",
                "Geniş spektrumlu ve daha uzun süreli parenteral/oral tedavi ve anatomik düzeltme gerektirir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Tedaviden sonraki ilk 2 hafta içinde aynı bakteri türü ve suşuyla enfeksiyonun tekrarlamasına [nüks] (relaps) adı verilir.",
            "maskedTerm": "nüks",
            "hint": "Aynı patojenle erken dönemde tekrarlama terimi"
        },
        {
            "type": "active_recall",
            "question": "Yenidoğan ve erken süt çocukluğu döneminde (ilk 3 ay) ÜSE görülme sıklığında cinsiyet dağılımı nasıldır?",
            "answer": "Erkek bebeklerde kız bebeklerden daha sıktır; bu durum sünnetsiz erkeklerde sünnet derisi altındaki bakteriyel kolonizasyon ve konjenital anomalilerle ilişkilidir."
        }
    ],
    30: [
        {
            "type": "interactive_table",
            "title": "Üriner Sistem Enfeksiyonlarında Başlıca Mikroorganizmalar",
            "tableHeaders": ["Mikroorganizma", "Klinik Görülme Sıklığı", "Karakteristik Mikrobiyolojik ve Patolojik Özellik"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Escherichia coli (UPEC)"},
                        {"text": "Komplike olmayanda %75-95", "isMasked": True, "hint": "E. coli'nin ezici sıklık yüzdesi"},
                        {"text": "P fimbriyası ve Tip 1 pili ile üroepitele tutunarak asendan yayılır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Staphylococcus saprophyticus"},
                        {"text": "Genç cinsel aktif kadında %5-15", "isMasked": True, "hint": "S. saprophyticus'un genç kadındaki oranı"},
                        {"text": "Koagülaz-negatif, novobiyosine dirençli stafilokoktur"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Proteus mirabilis"},
                        {"text": "Taş ve katater ilişkili ÜSE'de sık", "isMasked": True, "hint": "Proteus'un tipik klinik ortamı"},
                        {"text": "Güçlü üreaz enzimi salgılar; idrarı alkalileştirerek struvit taşı yaptırır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Klebsiella pneumoniae"},
                        {"text": "Nozokomiyal ve komplike olgularda sık", "isMasked": True, "hint": "Klebsiella'nın hastane içi önemi"},
                        {"text": "Kalın polisakkarit kapsülü ile fagositoza dirençlidir"}
                    ]
                }
            ]
        },
        {
            "type": "causal_chain",
            "title": "Proteus mirabilis Enfeksiyonunda Struvit (Enfeksiyon) Taşı Oluşumu",
            "steps": [
                "1. Proteus mirabilis bakterisi üriner sisteme asendan yolla yerleşir.",
                "2. Bakteri bol miktarda üreaz enzimi salgılayarak idrardaki üreyi parçalar.",
                "3. Ürenin hidrolizi sonucu açığa çıkan amonyak idrar pH'sını alkalileştirir (pH > 7,2).",
                "4. Alkalen ortamda magnezyum, amonyum ve fosfat (MAP) iyonları hızla kristalleşir.",
                "5. Tüm böbrek toplayıcı sistemini dolduran geyik boynuzu (staghorn) struvit taşları şekillenir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Genç cinsel aktif kadınlarda komplike olmayan sistit tablosunda E. coli'den sonra ikinci en sık etken olan novobiyosine dirençli bakteri [Staphylococcus saprophyticus]'tur.",
            "maskedTerm": "Staphylococcus saprophyticus",
            "hint": "Koagülaz negatif novobiyosin dirençli patojen"
        }
    ],
    40: [
        {
            "type": "before_after_slider",
            "title": "Gebelikte Asemptomatik Bakteriüri ile Gebe Olmayan Kadının Yönetimi",
            "leftTitle": "Gebelikte Asemptomatik Bakteriüri",
            "rightTitle": "Gebe Olmayan Kadında Asemptomatik Bakteriüri",
            "leftPoints": [
                "Tüm gebeler ilk trimesterde asemptomatik bakteriüri yönünden taranmalıdır.",
                "Tedavi edilmezse gebelerin %20-40'ında akut piyelonefrit ve erken doğum gelişir.",
                "Kültürde anlamlı üreme saptandığında mutlaka uygun antibiyotikle tedavi edilir.",
                "Tedavi sonrasında kürün doğrulanması için kontrol idrar kültürü yapılır."
            ],
            "rightPoints": [
                "Rutin tarama önerilmez ve klinik olarak endike değildir.",
                "Tedavi edilmemesi böbrek yetmezliğine veya doku hasarına yol açmaz.",
                "Antibiyotik verilmesi dirençli suş gelişimine yol açtığı için tedavi önerilmez.",
                "Sadece invaziv ürolojik girişim öncesinde tedavi endikasyonu vardır."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Diyabetik hastalarda gaz oluşturan bakterilerin (E. coli, Klebsiella) böbrek parankiminde nekroz ve gaz birikimi yapmasıyla gelişen ölümcül tabloya [amfizemli piyelonefrit] adı verilir.",
            "maskedTerm": "amfizemli piyelonefrit",
            "hint": "Böbrekte gaz toplanan ağır nekrotizan enfeksiyon"
        },
        {
            "type": "active_recall",
            "question": "Çocukluk çağında tekrarlayan ateşli üriner sistem enfeksiyonu geçiren bir çocukta ilk araştırılması gereken konjenital anatomik bozukluk nedir?",
            "answer": "Vezikoüreteral reflüdür (VUR)."
        }
    ],
    50: [
        {
            "type": "causal_chain",
            "title": "Katater İlişkili Üriner Sistem Enfeksiyonunda Biyofilm Oluşum Zinciri",
            "steps": [
                "1. Üretral sonda takılmasını takiben idrardaki proteinler katater yüzeyine çöker.",
                "2. Bakteriler kataterin iç ve dış yüzeyine adezinleri aracılığıyla tutunur.",
                "3. Bakteriler çoğalarak ekstrasellüler polisakkarit matriks (glikokaliks) sentezler.",
                "4. Antibiyotiklerin ve immün savunmanın geçemediği korunaklı biyofilm tabakası kurulur.",
                "5. Biyofilmden periyodik olarak dökülen bakteriler inatçı bakteriüri ve ürosepsise yol açar."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Üriner Sistem Enfeksiyonlarında Bulaş Yolları",
            "tableHeaders": ["Bulaş Yolu", "Görülme Oranı", "Tipik Patojenler ve Mekanizma"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Asendan Yol (Çıkan Enfeksiyon)"},
                        {"text": "Ezici çoğunluk (>%95)", "isMasked": True, "hint": "Asendan yolun görülme sıklığı"},
                        {"text": "Gastrointestinal flora bakterilerinin periüretral bölgeden mesane ve böbreğe tırmanması"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Hematojen Yol (Kandan Yayılım)"},
                        {"text": "Nadir (<%3-5)", "isMasked": True, "hint": "Hematojen yayılım oranı"},
                        {"text": "S. aureus bakteriyemisi, tüberküloz veya mantar enfeksiyonlarının böbreğe ekilmesi"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Lenfatik Yol"},
                        {"text": "Çok nadir / tartışmalı", "isMasked": True, "hint": "Lenfatik yol sıklığı"},
                        {"text": "Ağır bağırsak enfeksiyonlarında veya retroperitoneal lenf kanalları yoluyla geçiş"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Tüm hastane kaynaklı (nozokomiyal) enfeksiyonların yaklaşık %40'ını [üriner sistem enfeksiyonları] oluşturur ve bunların %80'i katater ilişkili gelişir.",
            "maskedTerm": "üriner sistem enfeksiyonları",
            "hint": "Hastanede en sık gelişen nozokomiyal enfeksiyon türü"
        }
    ],
    60: [
        {
            "type": "interactive_table",
            "title": "Üropatojen E. coli (UPEC) Başlıca Virülans Faktörleri",
            "tableHeaders": ["Virülans Faktörü", "Biyolojik Fonksiyon", "Klinik Enfeksiyon Tipi"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Tip 1 Fimbriya (Mannoza Duyarlı)"},
                        {"text": "Mesane üroepitelindeki üroplakin reseptörlerine bağlanır", "isMasked": True, "hint": "Mesane epitelindeki hedef reseptör"},
                        {"text": "Akut sistit başlangıcında kolonizasyon sağlar"}
                    ]
                },
                {
                    "cells": [
                        {"text": "P Fimbriyası / Pap Pili (Mannoza Dirençli)"},
                        {"text": "Böbrek tübül ve parankim epitelindeki glikolipidlere bağlanır", "isMasked": True, "hint": "Üst üriner sistemdeki bağlanma hedefi"},
                        {"text": "Akut piyelonefrit patogenezinde kritik rol oynar"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Alfa-Hemolizin Toksini"},
                        {"text": "Konak hücre membranında porlar açarak hücre lizisi yapar", "isMasked": True, "hint": "Bakteriyel eritrosit/lökosit parçalayıcı por"},
                        {"text": "Doku invazyonu ve demir kazanımı sağlar"}
                    ]
                },
                {
                    "cells": [
                        {"text": "K Kapsül Antijeni"},
                        {"text": "Polisakkarit kılıf ile nötrofillerin fagositozunu engeller", "isMasked": True, "hint": "Bakteriyi yutulmaktan koruyan yapı"},
                        {"text": "Bakterinin serum bakterisidal aktivitesine direnci"}
                    ]
                }
            ]
        },
        {
            "type": "before_after_slider",
            "title": "Üç Bardak Testinde Hematürinin Anatomik Lokalizasyonu",
            "leftTitle": "Başlangıç (İnisiyal) Hematüri",
            "rightTitle": "Terminal veya Total Hematüri",
            "leftPoints": [
                "Kanama sadece işemenin ilk birkaç mililitresinde görülür, sonra idrar açılır.",
                "Patolojinin lokalizasyonu anterior üretradır.",
                "Üretrit, meatal darlık veya üretral travma düşünülür."
            ],
            "rightPoints": [
                "Terminal hematüri işemenin sonunda ortaya çıkar; mesane boynu veya prostat kaynaklıdır.",
                "Total hematüri işeme boyunca homojendir; mesane gövdesi, üreter veya böbrek kaynaklıdır.",
                "Taş, neoplazm veya ağır sistit/piyelonefrit tablosunu gösterir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "UPEC suşlarının böbrek tübül epitelindeki digalaktozid reseptörlerine yapışarak akut piyelonefrit yapmasını sağlayan mannoza dirençli fimbriya [P fimbriyası] (Pap pili) adını alır.",
            "maskedTerm": "P fimbriyası",
            "hint": "Piyelonefrit yapan bakteriyel adezyon uzantısı"
        }
    ],
    70: [
        {
            "type": "interactive_table",
            "title": "Üriner Sistem Ağrılarının Lokalizasyon ve Özellikleri",
            "tableHeaders": ["Ağrı Tipi / Bölge", "Altta Yatan Patofizyoloji", "Klinik Özellik ve Yayılım"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Böbrek Ağrısı (Kapsüler Ağrı)"},
                        {"text": "Böbrek kapsülünün akut gerilmesi (enflamasyon veya hidronefroz)", "isMasked": True, "hint": "Böbrekte gerilen ağrıya duyarlı zar"},
                        {"text": "Kostovertebral açıda (KVA) sürekli, donuk ağrı; pozisyonla değişmez"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Üreter Kolik Ağrısı"},
                        {"text": "Üreter düz kaslarının aşırı spazmı ve lümen obstrüksiyonu", "isMasked": True, "hint": "Kolik ağrıyı yapan kas spazmı"},
                        {"text": "Şiddetli, dalgalar halinde gelen kramp tarzında ağrı; kasığa ve testise/labiuma yayılır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Mesane Ağrısı (Suprapubik)"},
                        {"text": "Mesane mukozasının enflamasyonu ve detrüsör spazmı", "isMasked": True, "hint": "Mesane iç örtüsü enflamasyonu"},
                        {"text": "Suprapubik bölgede dolgunluk ve işeme ile hafifleyen rahatsızlık hissi"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Akut piyelonefritte elin ulnar kenarı ile kostovertebral açıya hafifçe vurulduğunda şiddetli hassasiyet uyanması [Giordano belirtisi] olarak adlandırılır.",
            "maskedTerm": "Giordano belirtisi",
            "hint": "KVAH muayenesinin tıp tarihindeki meşhur özel adı"
        },
        {
            "type": "causal_chain",
            "title": "Renal Kolik Ağrısının Nöral İletim Zinciri",
            "steps": [
                "1. Üretere düşen taş idrar akımını tıkayarak proksimal hidrostatik basıncı artırır.",
                "2. Üreter duvarındaki mekanoreseptörler ve sempatik sinir uçları uyarılır.",
                "3. Ağrı duyusu T10-L2 spinal kord segmentlerine iletilir.",
                "4. İlgili dermatomlara yansıyan ağrı böbrek lojundan kasık bölgesine ve genital organlara yayılır.",
                "5. Parasempatik ve vagal uyarı ile bulantı, kusma ve taşikardi eşlik eder."
            ]
        }
    ],
    80: [
        {
            "type": "interactive_table",
            "title": "Alt Üriner Sistem Semptomları (AÜSS) Sınıflandırması",
            "tableHeaders": ["Kategori", "Semptomlar", "Fizyopatolojik Mekanizma"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Depolama (İrritatif) Semptomları"},
                        {"text": "Pollaküri (sık işeme), noktüri, dizüri, sıkışma (urgency)", "isMasked": True, "hint": "Mesane depolama fazı bozuklukları"},
                        {"text": "Mesane mukozasında enflamatuar irritasyon ve detrüsör aşırı duyarlılığı"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İşeme (Obstrüktif) Semptomları"},
                        {"text": "Tereddüt (hesitancy), zayıf akım, kesik kesik işeme, ıkınma", "isMasked": True, "hint": "Mesane çıkım tıkanıklığı bulguları"},
                        {"text": "Prostat büyümesi, üretral darlık veya mesane boynu direnci"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İşeme Sonrası Semptomlar"},
                        {"text": "Tam boşalamama hissi, işeme sonrası damlama", "isMasked": True, "hint": "İdrar bittikten sonraki yakınmalar"},
                        {"text": "Rezidüel idrar varlığı veya üretra içi göllenme"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "İdrar yaparken hissedilen ağrı, yanma ve batma hissi [dizüri] olarak tanımlanır ve sistit ile üretritin en yaygın yakınmasıdır.",
            "maskedTerm": "dizüri",
            "hint": "Ağrılı işemenin tıbbi terminolojideki adı"
        },
        {
            "type": "before_after_slider",
            "title": "Akut Sistit ile Akut Üretrit Klinik Farkları",
            "leftTitle": "Akut Sistit",
            "rightTitle": "Akut Üretrit",
            "leftPoints": [
                "Baskın yakınmalar dizüri, sık idrara çıkma (pollaküri) ve suprapubik ağrıdır.",
                "Gözle görülür üretral pürülan akıntı genellikle bulunmaz.",
                "Etken çoğunlukla gastrointestinal kökenli E. coli ve diğer gram-negatif basillerdir.",
                "İdrar kültüründe klasik Kass kriterine göre anlamlı bakteriüri saptanır."
            ],
            "rightPoints": [
                "Baskın yakınma üretral akıntı (pürülan veya müköz) ve meatus çevresinde kaşıntıdır.",
                "Cinsel yolla bulaşan enfeksiyonlar (N. gonorrhoeae, C. trachomatis) önde gelir.",
                "İdrar analizinde piyüri olabilir fakat standart idrar kültüründe üreme olmaz (steril piyüri).",
                "Tanı üretral sürüntü veya ilk idrar örneğinde PCR testleri ile konur."
            ]
        }
    ],
    90: [
        {
            "type": "interactive_table",
            "title": "Akut Sistit ile Akut Piyelonefrit Ayırıcı Tanı Tablosu",
            "tableHeaders": ["Klinik Özellik", "Akut Sistit (Alt ÜSE)", "Akut Piyelonefrit (Üst ÜSE)"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Ateş ve Titreme"},
                        {"text": "Yoktur (vücut ısısı normaldir)", "isMasked": True, "hint": "Sistitteki ateş durumu"},
                        {"text": "Tipik olarak vardır; titremeyle yükselen yüksek ateş (≥38,5°C)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Yan Ağrısı / KVAH"},
                        {"text": "Yoktur; ağrı sadece suprapubiktir", "isMasked": True, "hint": "Sistitte yan ağrısı durumu"},
                        {"text": "Tek veya çift taraflı şiddetli yan ağrısı ve pozitif KVAH vardır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sistemik Toksisite"},
                        {"text": "Yoktur; genel durum iyidir", "isMasked": True, "hint": "Alt ÜSE'de genel durum"},
                        {"text": "Bulantı, kusma, halsizlik, hipotansiyon ve ürosepsis riski vardır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İdrar Sedimentinde Silendir"},
                        {"text": "Silendir bulunmaz (yalnızca lökosit ve bakteri)", "isMasked": True, "hint": "Sistitte silendir varlığı"},
                        {"text": "Lökosit silendirleri (WBC casts) patognomoniktir"}
                    ]
                }
            ]
        },
        {
            "type": "branching_logic",
            "scenario": "26 yaşında kadın hasta, 2 gündür devam eden dizüri ve sık idrara çıkma şikayetlerinin ardından aniden titreme ile yükselen 39°C ateş, sağ yan ağrısı ve bulantı ile başvuruyor. Fizik muayenede sağ kostovertebral açı hassasiyeti (KVAH) pozitif saptanıyor. Bu hastada ilk basamak tanı ve yönetim ne olmalıdır?",
            "options": [
                {
                    "text": "Akut piyelonefrit düşünülmeli; kan ve idrar kültürü alınarak derhal uygun sistemik antibiyotik tedavisi başlanmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; yüksek ateş, titreme, yan ağrısı ve KVAH enfeksiyonun mesaneden böbrek parankimine tırmandığını (akut piyelonefrit) gösterir ve acil sistemik tedavi gerektirir."
                },
                {
                    "text": "Basit sistit düşünülerek hastaya tek doz oral fosfomisin verip eve gönderilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; yüksek ateş ve KVAH pozitifliği üst üriner sistem parankimal enfeksiyonudur, tek doz oral sistit tedavisi yetersizdir."
                },
                {
                    "text": "Sadece kas spazmı kabul edilip kas gevşetici reçete edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; ateş, dizüri ve lökositoz eşliğinde yan ağrısı renal enfeksiyonu işaret eder."
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Menide kan görülmesi anlamına gelen [hematospermi] olgularının büyük kısmı prostat ve seminal veziküllerin benign enflamatuar veya enfeksiyöz süreçlerine bağlıdır.",
            "maskedTerm": "hematospermi",
            "hint": "Ejakülatta kan bulunması semptomunun tıbbi adı"
        }
    ],
    100: [
        {
            "type": "interactive_table",
            "title": "Üriner Sistem Enfeksiyonları Master Klinik Algoritması",
            "tableHeaders": ["Enfeksiyon Sendromu", "Birincil Tutulum Odağı", "Tipik Klinik Tablo", "Temel Tanı Kanıtı"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Akut Sistit"},
                        {"text": "Mesane mukozası", "isMasked": True, "hint": "Sistitin primer organı"},
                        {"text": "Dizüri, sık idrara çıkma, acil sıkışma, suprapubik ağrı; ateş yok"},
                        {"text": "Piyüri ve orta akım idrar kültüründe ≥10²-10³ CFU/mL bakteri"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Akut Piyelonefrit"},
                        {"text": "Böbrek tübülleri ve interstisyumu", "isMasked": True, "hint": "Piyelonefrit parankimal anatomik tutulumu"},
                        {"text": "Yüksek ateş, titreme, kostovertebral açı hassasiyeti, bulantı/kusma"},
                        {"text": "İdrarda lökosit silendirleri ve kültürde üreme"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Akut Prostatit"},
                        {"text": "Prostat bezi stroması ve asinusları", "isMasked": True, "hint": "Prostatitin tutulum odağı"},
                        {"text": "Perineal ağrı, dizüri, işeme güçlüğü, rektal muayenede aşırı hassas sıcak prostat"},
                        {"text": "İdrar kültürü ve piyüri (masaj KONTRENDİKEDİR)"}
                    ]
                }
            ]
        },
        {
            "type": "active_recall",
            "question": "İdrar sedimentinde saptandığında enfeksiyonun alt üriner sistemde (sistit) değil, böbrek parankiminde (piyelonefrit) olduğunu kesinleştiren silendir türü hangisidir?",
            "answer": "Lökosit silendirleridir (WBC casts)."
        },
        {
            "type": "before_after_slider",
            "title": "Ürosepsis Erken Uyarı Kriterleri (qSOFA) vs Standart Komplike ÜSE",
            "leftTitle": "Standart Piyelonefrit / Komplike ÜSE",
            "rightTitle": "Ürosepsis (Hayatı Tehdit Eden Organ Yetmezliği)",
            "leftPoints": [
                "Böbrek lojunda ağrı, ateş ve lökositoz mevcuttur ancak vital bulgular stabildir.",
                "Kan basıncı normal sınırlardadır ve doku perfüzyonu korunmuştur.",
                "Bilinç durumu tamamen açıktır ve oryantasyon tamdır.",
                "Standart servis yatışı veya ayaktan parenteral tedavi ile kontrol altına alınır."
            ],
            "rightPoints": [
                "qSOFA kriterlerinden en az ikisi pozitiftir (Solunum hızı ≥22/dk, Değişmiş mental durum, Sistolik KB ≤100 mmHg).",
                "Doku hipoperfüzyonuna bağlı serum laktat düzeyi belirgin şekilde yükselir (>2 mmol/L).",
                "Septik şok riski nedeniyle acil yoğun bakım izlemi, sıvı resüsitasyonu ve vazopressör gerekir.",
                "Mortalite riski yüksektir; ilk 1 saat içinde geniş spektrumlu antibiyotik şarttır."
            ]
        }
    ]
}

# Additions for Deck 40 (Checkpoints 80, 90) and Deck 41 (Checkpoints 70, 80, 90)
D40_ENRICHMENTS = {
    80: [
        {
            "type": "causal_chain",
            "title": "CYBH Tarama ve Partner Bildirimi Döngüsü",
            "steps": [
                "1. İndeks olguda cinsel yolla bulaşan enfeksiyon tanısı mikrobiyolojik olarak doğrulanır.",
                "2. İndeks olgunun son 60 gün içindeki tüm cinsel temaslıları belirlenir.",
                "3. Partnerlere asemptomatik olsalar dahi temas ve tarama bildirimi yapılır.",
                "4. Partnerler eşzamanlı olarak epidemiyolojik tedavi protokolüne alınır.",
                "5. Eşzamanlı tedavi tamamlanana kadar cinsel perhiz uygulanarak pinpon bulaşı engellenir."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Başlıca CYBH'lerde Temas Sonrası Profilaksi (PEP) Prensipleri",
            "tableHeaders": ["Patojen / Enfeksiyon", "Profilaktik Yaklaşım", "Kritik Başlama Zamanı"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "HIV Temas Sonrası Profilaksi (PEP)"},
                        {"text": "Üçlü antiretroviral kombinasyon (28 gün)", "isMasked": True, "hint": "HIV profilaksi rejim süresi"},
                        {"text": "İlk 72 saat içinde (mümkünse ilk 2-4 saatte)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Hepatit B Teması (Aşısız Kişi)"},
                        {"text": "Hepatit B İmmünglobulin (HBIG) + Aşı serisi", "isMasked": True, "hint": "Pasif ve aktif immünizasyon bileşeni"},
                        {"text": "İlk 24 saat içinde (en geç 7 gün içinde)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sifilis Teması"},
                        {"text": "Tek doz Benzatin Penisilin G (2,4 milyon ünite İM)", "isMasked": True, "hint": "Sifilis temasındaki standart antibiyotik dozu"},
                        {"text": "Temas sonrası ilk 90 gün içinde"}
                    ]
                }
            ]
        }
    ],
    90: [
        {
            "type": "before_after_slider",
            "title": "CYBH'lerde Birincil Korunma ile İkincil Korunma Ayrımı",
            "leftTitle": "Birincil Korunma (Primer)",
            "rightTitle": "İkincil Korunma (Sekonder)",
            "leftPoints": [
                "Hastalık henüz bulaşmadan önce sağlıklı bireyleri korumayı hedefler.",
                "Kondom kullanımı, sağlık eğitimi ve riskli cinsel davranışların azaltılması esastır.",
                "HPV ve HBV aşılamaları ile HIV PrEP (temas öncesi profilaksi) uygulanır."
            ],
            "rightPoints": [
                "Bulaşmış olan enfeksiyonun erken evrede taranıp saptanmasını hedefler.",
                "Asemptomatik risk gruplarında serolojik testler ve PCR taramaları yapılır.",
                "Erken tedavi ile bulaştırıcılık süresi kısaltılır ve komplikasyonlar önlenir."
            ]
        },
        {
            "type": "active_recall",
            "question": "HIV Temas Öncesi Profilaksisi (PrEP) kimlere önerilir ve hangi ilaç ikilisini içerir?",
            "answer": "Yüksek riskli cinsel davranışları olan HIV-negatif bireylere önerilir; Tenofovir disoproksil fumarat + Emtrisitabin (TDF/FTC) günlük oral kombinasyonunu içerir."
        }
    ]
}

D41_ENRICHMENTS = {
    70: [
        {
            "type": "interactive_table",
            "title": "ANCA İlişkili Vaskülitlerde Böbrek Tutulumu ve Ayırıcı Tanı",
            "tableHeaders": ["Vaskülit Tipi", "Hedef ANCA Tipi", "Böbrek Dışı Klinik Özellikler", "Böbrek Histopatolojisi"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Granülomatoz Polianjiitis (GPA - Wegener)"},
                        {"text": "c-ANCA (PR3-ANCA)", "isMasked": True, "hint": "Wegener'deki ana serolojik belirteç"},
                        {"text": "Üst ve alt solunum yolu nekrotizan granülomları, sinüzit, kavitasyon"},
                        {"text": "Nekrotizan kresentik glomerülonefrit (pauci-immün)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Mikroskopik Polianjiitis (MPA)"},
                        {"text": "p-ANCA (MPO-ANCA)", "isMasked": True, "hint": "MPA'daki ana serolojik belirteç"},
                        {"text": "Granülom yoktur; akciğer kapillariti ve alveolar kanama"},
                        {"text": "Nekrotizan kresentik glomerülonefrit (pauci-immün)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Eozinofilik Granülomatoz Polianjiitis (EGPA)"},
                        {"text": "p-ANCA (%40-50 olguda)", "isMasked": True, "hint": "Churg-Strauss antikor sıklığı"},
                        {"text": "Ağır astım, periferik eozinofili, alerjik rinit, kardiyak tutulum"},
                        {"text": "Fokal nekrotizan nefrit (nadir seyreder)"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "ANCA ilişkili vaskülitlerin böbrek biyopsisinde glomerüllerde nekroz ve hilaller görülürken immünfloresan mikroskopisinde immün birikimin olmamasına [pauci-immün] glomerülonefrit denir.",
            "maskedTerm": "pauci-immün",
            "hint": "İmmün depozitlerin yokluğunu belirten terim"
        }
    ],
    80: [
        {
            "type": "causal_chain",
            "title": "Multipl Miyelomda Kast Nefropatisi Mekanizması",
            "steps": [
                "1. Malign plazma hücreleri aşırı miktarda monoklonal immünglobulin hafif zinciri (kappa veya lambda) üretir.",
                "2. Serbest hafif zincirler glomerülden süzülerek distal tübül lümenine ulaşır.",
                "3. Distal tübülde hafif zincirler Henle kulpu epitelinden salgılanan Tamm-Horsfall proteini ile birleşir.",
                "4. Lümen içinde sert, amorf, eozinofilik protein tıkaçları (kastlar) çöker.",
                "5. Tıkaçların çevresinde dev hücreli yabancı cisim reaksiyonu gelişerek tübülleri tıkar ve akut böbrek hasarı yapar."
            ]
        },
        {
            "type": "before_after_slider",
            "title": "Multipl Miyelomda Kast Nefropatisi ile AL Tipi Amiloidoz Ayrımı",
            "leftTitle": "Miyelom Kast Nefropatisi",
            "rightTitle": "AL Tipi Renal Amiloidoz",
            "leftPoints": [
                "Hasar distal tübül lümenindeki protein tıkaçlarına ve direkt tübülotoksisiteye bağlıdır.",
                "Klinik tablo akut böbrek hasarı veya ilerleyici kronik tübüler yetmezliktir.",
                "Standart idrar dipstick testi hafifi zincirleri yakalayamaz (yalancı negatif proteinüri)."
            ],
            "rightPoints": [
                "Hafif zincirlerin fibriler formda glomerül mezanjiyumunda ve damarlarda birikimidir.",
                "Klinik tablo masif albüminüri ve ağır nefrotik sendromdur.",
                "Kongo kırmızısı boyasında polarize mikroskopta elma yeşili çift kırınım verir."
            ]
        }
    ],
    90: [
        {
            "type": "interactive_table",
            "title": "Trombotik Mikroanjiyopatiler (TMA): TTP ile HÜS Ayrımı",
            "tableHeaders": ["Özellik", "Trombotik Trombositopenik Purpura (TTP)", "Hemolitik Üremik Sendrom (HÜS)"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Temel Enzim / Toksin Defekti"},
                        {"text": "ADAMTS13 metaloproteaz eksikliği (<%10)", "isMasked": True, "hint": "TTP'deki von Willebrand faktör parçalayıcı enzim"},
                        {"text": "Shiga benzeri toksin (E. coli O157:H7) veya alternatif kompleman regülasyon defekti"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Baskın Organ Tutulumu"},
                        {"text": "Nörolojik semptomlar (konfüzyon, koma, nöbet)", "isMasked": True, "hint": "TTP'deki birincil klinik organ"},
                        {"text": "Akut böbrek yetmezliği (oligüri, azotemi) ön plandadır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Hasta Demografisi"},
                        {"text": "Daha çok genç erişkin kadınlar", "isMasked": True, "hint": "TTP tipik demografisi"},
                        {"text": "Tipik form çocuklarda kanlı ishal sonrası gelişir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İlk Basamak Tedavi"},
                        {"text": "Acil Terapötik Plazmaferez (TPE)", "isMasked": True, "hint": "TTP'deki hayat kurtaran plazma işlemi"},
                        {"text": "Destek tedavisi, hemodiyaliz; atipik HÜS'te Eculizumab (anti-C5)"}
                    ]
                }
            ]
        },
        {
            "type": "branching_logic",
            "scenario": "4 yaşında çocuk, kanlı ishal atağından 5 gün sonra solukluk, halsizlik, idrar çıkışında belirgin azalma (oligüri) ve peteşi döküntüleri ile acil servise getiriliyor. Laboratuvarda hemoglobin 7 g/dL, trombosit 28.000/mm³, kanda şistositler (parçalanmış eritrositler) ve serum kreatinininde belirgin yükseklik saptanıyor. Bu hastada tanı ve ilk yaklaşım ne olmalıdır?",
            "options": [
                {
                    "text": "Shiga toksin ilişkili tipik Hemolitik Üremik Sendrom (HÜS); destek tedavisi, sıvı-elektrolit dengesi ve gerekirse diyaliz uygulanmalıdır; antibiyotik ve trombosit transfüzyonundan kaçınılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; mikroanjiyopatik hemolitik anemi, trombositopeni ve akut böbrek hasarı HÜS triadıdır; çocuklarda kanlı ishal sonrası gelişir, gereksiz antibiyotik toksin salınımını artırabilir."
                },
                {
                    "text": "Akut viral gastroenterit kabul edilerek sadece oral rehidrasyon verilip taburcu edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; ağır anemi, derin trombositopeni ve akut böbrek hasarı tablosu mevcuttur, acil hastane yatışı şarttır."
                },
                {
                    "text": "İmmün trombositopenik purpura (ITP) düşünülerek acil splenektomi yapılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; ITP'de böbrek yetmezliği ve anemi eşlik etmez, cerrahi kontrendikedir."
                }
            ]
        }
    ]
}
