"""
Strictly Chronological, Forward-Leak-Free Enrichment Definitions for Decks 37, 38, 39, 40, 41.
Every interactive element references ONLY concepts that have already been taught up to that exact slide.
Zero forward leaks guaranteed.
"""

D37_ENRICHMENTS = {
    10: [
        {
            "type": "causal_chain",
            "title": "Nefrotik Sendromda Masif Ödem Oluşum Zinciri",
            "steps": [
                "1. Glomerüler filtrasyon bariyerinde podosit veya bazal membran negatif elektrik yükü hasara uğrar.",
                "2. Plazma proteinlerine karşı geçirgenlik artar ve idrarla masif albümin kaybı gelişir.",
                "3. Plazma albümin düzeyi düşer ve damar içi onkotik basınç dramatik biçimde azalır.",
                "4. Sıvı damar içinden interstisyel aralığa kaçarak intravasküler hipovolemiyi tetikler.",
                "5. RAAS sistemi ve ADH aktive olarak sekonder su-tuz retansiyonu ve yaygın ödem oluşturur."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Nefrotik Sendromun Dört Kardinal Bulgusu ve Mekanizması",
            "tableHeaders": ["Kardinal Bulgu", "Klinik Eşik / Değer", "Altta Yatan Patofizyolojik Mekanizma"],
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
                        {"text": "<3 g/dL", "isMasked": True, "hint": "Kandaki albümin düzeyi"},
                        {"text": "İdrarla aşırı albümin kaybının karaciğer sentez kapasitesini aşması"}
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
                        {"text": "Serum kolesterol ve trigliserid artışı", "isMasked": True, "hint": "Kan yağları parametresi"},
                        {"text": "Hipoalbüminemiye yanıt olarak hepatik lipoprotein sentezi artışı"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Nefrotik sendrom tanısında erişkinler için kardinal eşik değer 24 saatlik idrarla [≥3,5 g/gün] protein atılımıdır.",
            "maskedTerm": "≥3,5 g/gün",
            "hint": "Erişkinde nefrotik düzey proteinüri miktarı"
        }
    ],
    20: [
        {
            "type": "interactive_table",
            "title": "Minimal Değişiklik Hastalığı (MDH) Erken Dönem Özellikleri",
            "tableHeaders": ["İnceleme / Klinik Alan", "MDH Karakteristik Bulgusu", "Önemli Klinik Not"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Hasta Demografisi"},
                        {"text": "Çocukluk çağında nefrotik sendromun en sık nedeni", "isMasked": True, "hint": "Yaş grubu sıklığı"},
                        {"text": "Pediatrik olguların ezici çoğunluğundan sorumludur"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Rutin Işık Mikroskopisi"},
                        {"text": "Glomerüller tamamen normal yapıdadır", "isMasked": True, "hint": "Işık mikroskopisindeki görünüm"},
                        {"text": "Hücresel proliferasyon, nekroz veya skleroz izlenmez"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan Mikroskopisi"},
                        {"text": "Negatiftir; immün depozit izlenmez", "isMasked": True, "hint": "İmmünfloresan boyanma sonucu"},
                        {"text": "İmmün kompleks veya antikor birikimi saptanmaz"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Proteinüri Seçiciliği"},
                        {"text": "Yüksek oranda selektif proteinüri", "isMasked": True, "hint": "Protein kaçağı selektivitesi"},
                        {"text": "Temel olarak negatif elektrik yük kaybına bağlı albüminüri vardır"}
                    ]
                }
            ]
        },
        {
            "type": "causal_chain",
            "title": "Minimal Değişiklik Hastalığında Selektif Albüminüri Zinciri",
            "steps": [
                "1. T lenfosit kaynaklı dolaşan sitokinler podosit hücrelerinde biyokimyasal hasar oluşturur.",
                "2. Glomerüler bazal membranın polianyonik heparan sülfat negatif elektrik yükü kaybolur.",
                "3. Anyonik albümin moleküllerini geri iten elektrostatik yük bariyeri çöker.",
                "4. Küçük ve negatif yüklü albümin kolayca filtrasyon bariyerini aşarak idrara geçer.",
                "5. Yüksek molekül ağırlıklı immünglobulinler bariyeri geçemez ve selektif albüminüri tablosu ortaya çıkar."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Minimal Değişiklik Hastalığında rutin ışık mikroskobunda glomerüller [tamamen normal] olarak izlenir.",
            "maskedTerm": "tamamen normal",
            "hint": "MDH ışık mikroskobu görünüm durumu"
        }
    ],
    30: [
        {
            "type": "before_after_slider",
            "title": "MDH Seyri ile FSGS Başlangıç Özellikleri",
            "leftTitle": "MDH Klinik Seyri ve Tedavi",
            "rightTitle": "FSGS Başlangıcı ve Tanımı",
            "leftPoints": [
                "Elektron mikroskobunda podosit pedisellerinde yaygın silinme izlenir.",
                "Kortikosteroid tedavisine mükemmel yanıt verir; olguların çoğu hızla remisyona girer.",
                "Son dönem böbrek yetmezliğine ilerleme riski yok denecek kadar azdır."
            ],
            "rightPoints": [
                "Biyopside bazı glomerüllerin (fokal) bazı lobülleri (segmental) etkilenir.",
                "Kortikosteroid tedavisine zayıf veya dirençli yanıt verme eğilimindedir.",
                "Zamanla böbrek fonksiyonlarında bozulma ve progresyon riski taşır."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "MDH tanısında elektron mikroskobunda saptanan tek morfolojik bulgu podosit ayaksı çıkıntılarında [yaygın silinme] (effacement) izlenmesidir.",
            "maskedTerm": "yaygın silinme",
            "hint": "Pedisel morfolojik değişiklik terimi"
        },
        {
            "type": "active_recall",
            "question": "Fokal Segmental Glomerüloskleroz (FSGS) teriminde 'fokal' ve 'segmental' sözcükleri doku düzeyinde ne anlama gelir?",
            "answer": "Fokal: biyopsideki glomerüllerin yalnızca bir kısmının tutulması; Segmental: tutulan bir glomerülün yalnızca bazı lobüllerinin skleroza uğramasıdır."
        }
    ],
    40: [
        {
            "type": "causal_chain",
            "title": "FSGS'de Segmental Skleroz Oluşum Zinciri",
            "steps": [
                "1. Primer veya adaptif etkenler podosit hasarına, apoptozuna ve hücre kaybına yol açar.",
                "2. Bazal membranın üzerindeki podosit örtüsü soyulur ve denüde GBM alanları açığa çıkar.",
                "3. Çıplak bazal membran Bowman kapsülü parietal epiteliyle temas ederek sineşi oluşturur.",
                "4. Açığa çıkan segmentte plazma proteinleri ve kollajen birikerek hyalinozis ve skleroz meydana getirir.",
                "5. Glomerül kapiller lümenleri tıkanarak son dönem böbrek yetmezliğine doğru ilerleme başlar."
            ]
        },
        {
            "type": "interactive_table",
            "title": "FSGS Histopatolojik İnceleme Bulguları",
            "tableHeaders": ["Yöntem", "Histopatolojik Karakteristik", "Klinik Yorum"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Işık Mikroskopisi (LM)"},
                        {"text": "Segmental skleroz ve hyalinozis", "isMasked": True, "hint": "LM'deki tipik sklerotik lezyon"},
                        {"text": "Özellikle jukstamedüller glomerüllerde erken başlar"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan (IF)"},
                        {"text": "Sklerotik alanlarda non-spesifik IgM ve C3", "isMasked": True, "hint": "Tuzaklanmış immünglobulin depoziti"},
                        {"text": "Spesifik immün kompleks birikimi yoktur; tuzaklanmadır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Elektron Mikroskopisi (EM)"},
                        {"text": "Podosit kaybı ve soyulmuş bazal membran", "isMasked": True, "hint": "Ultra-yapısal podosit soyulması"},
                        {"text": "Sklerotik segmentlerde GBM çıplak kalmıştır"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "FSGS tanılı hastalara böbrek nakli yapıldığında hastalığın yeni böbrekte hızla nüks etmesinden dolaşımdaki [podosit geçirgenlik faktörleri] sorumludur.",
            "maskedTerm": "podosit geçirgenlik faktörleri",
            "hint": "Nakil sonrası erken nükse yol açan dolaşımdaki faktör"
        }
    ],
    50: [
        {
            "type": "causal_chain",
            "title": "Primer Membranöz Nefropatide Subepitelyal Hasar Mekanizması",
            "steps": [
                "1. Dolaşımdaki IgG4 yapısındaki otoantikorlar podosit yüzeyindeki PLA2R antijenine bağlanır.",
                "2. Podosit tabanı ile bazal membran arasında in situ subepitelyal immün kompleksler çöker.",
                "3. Kompleman sistemi aktive olarak C5b-9 membran atak kompleksini kurar.",
                "4. Podositler parçalanmadan hücresel aktivasyon ve sitokin uyarısına uğrar.",
                "5. Podosit hasarı sonucu filtrasyon bariyeri bozulur ve masif nefrotik proteinüri ortaya çıkar."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Membranöz Nefropatide Primer ve Sekonder Nedenler",
            "tableHeaders": ["Kategori", "Temel Etyolojik Ajan / Antijen", "Klinik Özellik"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Primer Membranöz Nefropati"},
                        {"text": "Anti-PLA2R otoantikorları", "isMasked": True, "hint": "Podosit yüzey antijeni"},
                        {"text": "Erişkinlerde primer nefrotik tablonun önde gelen nedenidir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sekonder İnfeksiyöz Nedenler"},
                        {"text": "Hepatit B ve Hepatit C virüsleri", "isMasked": True, "hint": "Sık ilişkili viral hepatitler"},
                        {"text": "Viral antijen-antikor kompleksleri ile tetiklenir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sekonder Malignite İlişkili"},
                        {"text": "Akciğer ve gastrointestinal karsinomlar", "isMasked": True, "hint": "İleri yaşta taranan neoplazmlar"},
                        {"text": "Yaşlı hastalarda karsinom taraması gerektirir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Sekonder Otoimmün / İlaç"},
                        {"text": "Lupus Sınıf V, NSAİİ, penisilamin ve altın", "isMasked": True, "hint": "Lupus ve sorumlu antiromatizmal ilaçlar"},
                        {"text": "Etken ilacın kesilmesiyle remisyona girebilir"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Erişkinlerde primer membranöz nefropati olgularının büyük kısmında podosit yüzeyindeki [PLA2R] antijenine karşı otoantikorlar saptanır.",
            "maskedTerm": "PLA2R",
            "hint": "Primer membranöz nefropatideki podosit hedef reseptörü kısaltması"
        }
    ],
    60: [
        {
            "type": "before_after_slider",
            "title": "Membranöz Nefropatide Gümüşleme ve İmmünfloresan",
            "leftTitle": "Gümüş Boyaması (LM)",
            "rightTitle": "İmmünfloresan Mikroskopisi",
            "leftPoints": [
                "GBM dış yüzeyinde subepitelyal depozitler arasında spikeler uzanır.",
                "Karakteristik 'Spike and dome' (diken ve kubbe) görünümü izlenir.",
                "Glomerül kapiller lümenlerinde hücresel proliferasyon görülmez."
            ],
            "rightPoints": [
                "GBM boyunca kesintisiz diffüz granüler boyanma saptanır.",
                "Birikim temel olarak IgG ve C3 depozitlerinden oluşur.",
                "Mezanjiyal veya subendotelyal birikim izlenmez."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Membranöz nefropatide gümüş boyamasında bazal membran materyalinin subepitelyal depozitler arasından çıkıntı yapmasıyla [spike and dome] görünümü oluşur.",
            "maskedTerm": "spike and dome",
            "hint": "Gümüş boyamasındaki meşhur morfolojik terim"
        },
        {
            "type": "branching_logic",
            "scenario": "56 yaşında erkek hasta nefrotik proteinüri ile geliyor; biyopsi membranöz nefropati ile uyumlu bulunuyor. Yaş ve klinik dikkate alındığında hastanın etiyolojik araştırmasında mutlaka yapılması gereken adım ne olmalıdır?",
            "options": [
                {
                    "text": "Hastada yaşa uygun malignite taraması (akciğer grafisi/BT, gastrointestinal endoskopi vb.) yapılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; ileri yaşta membranöz nefropati olgularında gizli karsinomlar mutlaka taranmalıdır."
                },
                {
                    "text": "Akut apandisit şüphesiyle acil cerrahiye sevk edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; membranöz nefropatinin akut apandisitle ilgisi yoktur."
                },
                {
                    "text": "Biyopsi alındığı için başka hiçbir sekonder araştırma yapılmamalıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlıştır; sekonder etiyolojiler (karsinom, hepatit, ilaç) dışlanmadan izlem yetersizdir."
                }
            ]
        }
    ],
    70: [
        {
            "type": "causal_chain",
            "title": "MPGN Tip 1'de Tramvay Rayı (Çift Kontur) Gelişimi",
            "steps": [
                "1. Dolaşımdaki immün kompleksler kapiller duvarın subendotelyal aralığında çöker.",
                "2. Kompleman aktivasyonu ile endotel ve mezanjiyal hücre proliferasyonu tetiklenir.",
                "3. Mezanjiyal hücre uzantıları bazal membran ile endotel arasına sokulur (mezanjiyal interpozisyon).",
                "4. İnterpoze mezanjiyal hücreler yeni bazal membran matriksi sentezler.",
                "5. Gümüş boyamasında GBM'de çift hatlı 'tramvay rayı' (tram-track) görünümü oluşur."
            ]
        },
        {
            "type": "interactive_table",
            "title": "MPGN Tip 1 Histopatolojik ve Laboratuvar Özellikleri",
            "tableHeaders": ["İnceleme Alanı", "MPGN Tip 1 Karakteristiği", "Klinik / Patolojik Anlam"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Depozit Lokalizasyonu"},
                        {"text": "Subendotelyal ve mezanjiyal birikim", "isMasked": True, "hint": "Endotel altı birikim alanı"},
                        {"text": "İmmün komplekslerin endotel altında depolanması"}
                    ]
                },
                {
                    "cells": [
                        {"text": "LM Görünümü"},
                        {"text": "Tramvay rayı (çift kontur) ve lobülasyon", "isMasked": True, "hint": "Gümüş boyamadaki çift hat"},
                        {"text": "Mezanjiyal interpozisyon sonucu yeni bazal membran sentezi"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Kompleman Profili"},
                        {"text": "Hem C3 hem C4 belirgin düşüktür", "isMasked": True, "hint": "Klasik kompleman tüketimi"},
                        {"text": "Klasik kompleman yolunun aktivasyonunu yansıtır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İlişkili Sistemik Enfeksiyon"},
                        {"text": "Hepatit C virüsü (HCV) enfeksiyonu", "isMasked": True, "hint": "En sık ilişkili hepatotrop virüs"},
                        {"text": "Tip II kriyoglobulinemi eşliğinde MPGN Tip 1 tablosu yapar"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "MPGN Tip 1'de mezanjiyal hücre uzantılarının kapiller duvar boyunca bazal membran altına sokulmasına [mezanjiyal interpozisyon] adı verilir.",
            "maskedTerm": "mezanjiyal interpozisyon",
            "hint": "Hücre uzantılarının araya girmesini tanımlayan patolojik terim"
        }
    ],
    80: [
        {
            "type": "interactive_table",
            "title": "MPGN Tip 1 ile Yoğun Birikim Hastalığı (DDD) Ayrımı",
            "tableHeaders": ["Özellik", "MPGN Tip 1 (İmmün Kompleks)", "Yoğun Birikim Hastalığı (C3 Glomerülopatisi)"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Depozit Lokalizasyonu"},
                        {"text": "Subendotelyal depozitler", "isMasked": True, "hint": "Endotel altı depozit sahası"},
                        {"text": "GBM lamina densasında intramembranöz yoğun kurdele bant"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan Patern"},
                        {"text": "Granüler IgG ve C3 pozitifliği", "isMasked": True, "hint": "Klasik immün depozit bileşimi"},
                        {"text": "Yalnızca yoğun C3 pozitif; IgG negatiftir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Temel Mekanizma"},
                        {"text": "İmmün kompleks birikimi (HCV vb.)", "isMasked": True, "hint": "Antijen-antikor süreci"},
                        {"text": "Alternatif kompleman yolu kontrolsüzlüğü (C3NeF otoantikoru)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Kompleman Profili"},
                        {"text": "C3 ve C4 sıklıkla birlikte düşük", "isMasked": True, "hint": "Klasik yol tüketimi"},
                        {"text": "C3 dramatik düşüktür; C4 genellikle normaldir"}
                    ]
                }
            ]
        },
        {
            "type": "active_recall",
            "question": "Yoğun Birikim Hastalığında (DDD) alternatif yol C3 konvertaz enzimini stabilize ederek C3'ün sürekli tükenmesine yol açan otoantikor hangisidir?",
            "answer": "C3 Nefritik Faktör (C3NeF)."
        },
        {
            "type": "cloze_masking",
            "sentence": "C3 Glomerulopatisinde immünfloresan mikroskobunda immünglobulinler negatifken yalnızca [C3 birikimi] saptanır.",
            "maskedTerm": "C3 birikimi",
            "hint": "İmmünfloresanda tek pozitif kompleman depoziti"
        }
    ],
    90: [
        {
            "type": "causal_chain",
            "title": "Nefrotik Sendromda Tromboemboli Mekanizması",
            "steps": [
                "1. Glomerül permeabilitesi artar ve antitrombin III idrarla masif olarak kaybedilir.",
                "2. Plazmada doğal antikoagülan düzeyleri düşerken karaciğerde fibrinojen sentezi uyarılır.",
                "3. Trombosit hiperagregabilitesi ve plazma vizkozitesi belirgin şekilde yükselir.",
                "4. İntravasküler alanda hiperkoagülabilite (tromboza yatkınlık) tablosu yerleşir.",
                "5. Özellikle membranöz nefropatide renal ven trombozu ve derin ven trombozu riski ortaya çıkar."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Diyabetik Glomerüloskleroz ile Renal Amiloidoz Ayrımı",
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
            "sentence": "Nefrotik sendromlu hastalarda hiperkoagülabilite gelişmesinde en kritik etken doğal bir antikoagülan olan [antitrombin III] düzeyinin idrarla kaybedilmesidir.",
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
            "scenario": "45 yaşında nefrotik sendrom tanısıyla izlenen bir hastada ani başlayan sol yan ağrısı, gross hematüri ve sol varikosel saptanıyor. Bu klinik tabloda öncelikle ne düşünülmeli ve ilk yaklaşım ne olmalıdır?",
            "options": [
                {
                    "text": "Renal ven trombozu düşünülmeli; acil Doppler ultrasonografi/BT anjiyografi ile tanı doğrulanıp derhal antikoagülan tedavi başlanmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğrudur; nefrotik sendromda antitrombin III kaybı nedeniyle renal ven trombozu riski yüksektir; ani yan ağrısı, hematüri ve sol varikosel renal ven trombozunun klasik triadıdır."
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
            "title": "APSGN İmmün Hasar Zinciri",
            "steps": [
                "1. A grubu beta-hemolitik streptokokların nefritojenik suşları farenjit veya cilt enfeksiyonu yapar.",
                "2. Bakteriyel antijenler (SpeB, NAPlr) dolaşıma karışarak glomerül bazal membranına ekilir.",
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
            "answer": "Streptokoksik pirojenik ekzotoksin B (SpeB) ve Nefritle ilişkili plazmin reseptörüdür (NAPlr)."
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
            "scenario": "7 yaşında çocuk, boğaz enfeksiyonundan 12 gün sonra çay rengi idrar, göz çevresi ödemi ve 140/90 mmHg tansiyon ile getiriliyor. ASO yüksek ve C3 kompleman düzeyi belirgin düşük bulunuyor. Bu çocukta klinik yönetim ve prognoz beklentisi ne olmalıdır?",
            "options": [
                {
                    "text": "Destekleyici tedavi (sıvı-tuz kısıtlaması, diüretik ve tansiyon kontrolü) verilmelidir; çocuklarda prognoz mükemmeldir (>%95 tam iyileşir).",
                    "isCorrect": True,
                    "feedback": "Doğrudur; tipik klinik ve laboratuvara sahip çocuklarda APSGN biyopsisiz destek tedavisiyle kendiliğinden mükemmel remisyona girer."
                },
                {
                    "text": "Acilen acil hemodiyaliz katateri takılarak yüksek doz sitotoksik kemoterapiye başlanmalıdır.",
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
                "1. Glomerül bazal membranında şiddetli nekroz ve mikro-yırtıklar oluşur.",
                "2. Plazma proteinleri, fibrinojen ve lökositler Bowman aralığına sızar.",
                "3. Bowman kapsülü parietal epitel hücreleri güçlü proliferasyon uyarısı alır.",
                "4. Bowman aralığına göç eden monosit ve makrofajlar fibrin ağlarıyla birleşerek hücre tabakaları kurar.",
                "5. Kapiller yumağı dıştan ezen hilal (kresent) yapısı oluşarak glomerülü skleroza götürür."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Tip I RPGN (Anti-GBM ve Goodpasture) Tanısal Özellikleri",
            "tableHeaders": ["Klinik / Patolojik Alan", "Karakteristik Tanı Özelliği", "Önemli Klinik Not"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Hedef Antijen"},
                        {"text": "Tip IV kollajen alfa-3 NC1 alanı", "isMasked": True, "hint": "Kollajen hedef alt birimi"},
                        {"text": "Bazal membrandaki spesifik non-kollajenöz bölgedir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan Paterni"},
                        {"text": "GBM boyunca kesintisiz lineer (çizgisel) IgG", "isMasked": True, "hint": "Çizgisel floresan boyanması"},
                        {"text": "Antikorların bazal membran boyunca pürüzsüz dizilimini yansıtır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Akciğer Tutulumu Varlığı"},
                        {"text": "Goodpasture Sendromu (alveolar kanama)", "isMasked": True, "hint": "Pulmoner-renal sendrom adı"},
                        {"text": "Alveol bazal membranı ile çapraz reaksiyon sonucu gelişir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Temel Acil Tedavi"},
                        {"text": "Plazmaferez ile antikorların uzaklaştırılması", "isMasked": True, "hint": "Otoantikorları temizleyen işlem"},
                        {"text": "Yüksek doz kortikosteroid ve siklofosfamid ile kombine edilir"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Goodpasture sendromunda otoantikorların hedefi Tip IV kollajenin [alfa-3 zinciri] non-kollajenöz bölgesidir.",
            "maskedTerm": "alfa-3 zinciri",
            "hint": "Goodpasture otoantikorunun bağlandığı kollajen alt birimi"
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
                "İmmünfloresan mikroskobunda immünglobulin ve kompleman birikimi saptanmaz (pauci-immün).",
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
            "type": "interactive_table",
            "title": "ISN/RPS Lupus Nefriti Sınıf I-IV Morfolojik Özellikleri",
            "tableHeaders": ["Lupus Sınıfı", "Histopatolojik İsimlendirme", "Baskın Klinik Özellik"],
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
                        {"text": "Nefritik sendrom başlangıcı ve orta derece proteinüri"}
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
        },
        {
            "type": "causal_chain",
            "title": "Lupus Nefriti Sınıf IV Diffüz Proliferatif GN Patogenezi",
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
            "sentence": "Lupus nefritinde immünfloresan incelemede IgG, IgA, IgM, C3 ve C1q moleküllerinin tümünün birden pozitif boyanmasına [full-house] paterni adı verilir.",
            "maskedTerm": "full-house",
            "hint": "Tüm immünglobulin ve komplemanların pozitifliği terimi"
        }
    ],
    70: [
        {
            "type": "before_after_slider",
            "title": "Lupus Nefriti Sınıf IV ile Sınıf V Karşılaştırması",
            "leftTitle": "Sınıf IV (Diffüz Proliferatif)",
            "rightTitle": "Sınıf V (Membranöz Lupus)",
            "leftPoints": [
                "Baskın klinik tablo nefritik sendromdur (hematüri, hipertansiyon, oligüri).",
                "İmmün kompleksler temel olarak subendotelyal aralıkta birikir.",
                "Işık mikroskobunda belirgin proliferasyon ve tel halka lezyonları izlenir.",
                "Prognozu en kötü sınıftır; agresif immünsüpresyon zorunludur."
            ],
            "rightPoints": [
                "Baskın klinik tablo nefrotik sendromdur (masif proteinüri, ağır ödem).",
                "İmmün kompleksler subepitelyal aralıkta podosit tabanında çöker.",
                "Işık mikroskobunda proliferasyon olmaksızın diffüz GBM kalınlaşması görülür.",
                "Prognoz membranöz hasarın derecesine ve tromboz riskine bağlıdır."
            ]
        },
        {
            "type": "causal_chain",
            "title": "IgA Nefropatisinde Mezanjiyal Hasar Zinciri",
            "steps": [
                "1. Mukozal enfeksiyon uyarısıyla galaktoz-eksik anormal IgA1 molekülleri sentezlenir.",
                "2. Bu anormal IgA1 moleküllerine karşı kanda spesifik IgG otoantikorları oluşur.",
                "3. Dolaşımda polimerik IgA1 immün kompleksleri meydana gelir.",
                "4. Kompleksler glomerül mezanjiyal hücrelerine bağlanarak mezanjiyumda depolanır.",
                "5. Mezanjiyal hücre proliferasyonu ve matriks artışı ile glomerüler hasar ve hematüri tetiklenir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Dünyada en sık görülen primer glomerülonefrit türü olan IgA nefropatisinde immün kompleksler özellikle [mezanjiyum] kompartmanında depolanır.",
            "maskedTerm": "mezanjiyum",
            "hint": "IgA depozitlerinin biriktiği anatomik glomerüler alan"
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
                        {"text": "Çok sıktır; her ÜSYE atağında yineler", "isMasked": True, "hint": "Rekürrens özelliği"},
                        {"text": "Nadir; tek bir atak halinde geçirilir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İmmünfloresan Bulgusu"},
                        {"text": "Mezanjiyumda granüler IgA birikimi", "isMasked": True, "hint": "Berger'deki tanısal antikor depoziti"},
                        {"text": "Kaba granüler IgG ve C3 birikimi (yıldızlı gökyüzü)"}
                    ]
                }
            ]
        },
        {
            "type": "causal_chain",
            "title": "Alport Sendromunda Glomerül Hasarı Zinciri",
            "steps": [
                "1. Tip IV kollajenin alfa-3, alfa-4 veya alfa-5 zincirini kodlayan genlerde mutasyon meydana gelir.",
                "2. Glomerüler bazal membranın normal üçlü sarmal kollajen ağ örgüsü kurulamaz.",
                "3. Çocuklukta GBM incelir; zamanla lamina densada tabakalanma ve düzensiz kalınlaşma başlar.",
                "4. Elektron mikroskobunda tipik 'sepet örgüsü' (basket-weave) yarılması ve fragmantasyonu gelişir.",
                "5. Persistan mikroskobik/makroskopik hematüri, sensorinöral işitme kaybı ve oküler bulgularla ilerleyici hasar oluşur."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Alport sendromunda elektron mikroskobunda glomerül bazal membranının lamina densasında karakteristik [sepet örgüsü] (basket-weave) yarılması izlenir.",
            "maskedTerm": "sepet örgüsü",
            "hint": "Alport EM lamina densa tipik deseni"
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
                "Faz kontrast mikroskopisinde dismorfik eritrositler ve akantositler izlenir.",
                "Eşlik eden subnefrotik veya nefrotik düzeyde proteinüri sıktır."
            ],
            "rightPoints": [
                "İdrar rengi parlak kırmızı veya pembe renktedir.",
                "İdrarda eritrosit silendirleri kesinlikle bulunmaz.",
                "Faz kontrast mikroskopisinde eritrositler normal bikonkav (izomorfik) yapıdadır.",
                "Kan pıhtıları görülebilir; taş veya tümör lehinedir."
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
                        {"text": "Klasik Asemptomatik Eşik (Kass Kriteri)"},
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
            "sentence": "Kass kriterine göre asemptomatik bireylerde orta akım idrar kültüründe anlamlı bakteriüri eşiği mililitrede [≥10⁵ CFU/ml] bakteri üremesidir.",
            "maskedTerm": "≥10⁵ CFU/ml",
            "hint": "Klasik Kass bakteriüri sınır değeri"
        },
        {
            "type": "active_recall",
            "question": "Asemptomatik bakteriürinin (ASB) mutlaka taranıp tedavi edilmesi gereken iki mutlak klinik durum nedir?",
            "answer": "Gebeliktir ve mukozal kanama riski taşıyan invaziv ürolojik cerrahi girişimler öncesidir."
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
                "Kısa süreli standart ampirik oral tedaviyle tamamen iyileşir."
            ],
            "rightPoints": [
                "Anatomik anomali, taş, obstrüksiyon, erkek cinsiyet veya gebelik eşlik eder.",
                "Dirençli patojenler ve böbrek parankim hasarı riski daha yüksektir.",
                "Daha uzun süreli tedavi ve anatomik faktörün düzeltilmesini gerektirir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Tedaviden sonraki ilk 2 hafta içinde aynı mikroorganizma suşu ile enfeksiyonun tekrarlamasına [nüks] (relaps) adı verilir.",
            "maskedTerm": "nüks",
            "hint": "Aynı patojenle erken dönemde tekrarlama terimi"
        },
        {
            "type": "active_recall",
            "question": "Genç erişkin erkeklerde üriner sistem enfeksiyonunun çok nadir görülmesinin temel anatomik nedenleri nelerdir?",
            "answer": "Üretra uzunluğunun fazla olması, kuru periüretral çevre ve prostat sıvısının antibakteriyel özellikleridir."
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
            "title": "Proteus mirabilis Enfeksiyonunda Struvit Taşı Oluşumu",
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
                "Tedavi edilmezse gebelerin önemli kısmında akut piyelonefrit ve erken doğum gelişir.",
                "Kültürde anlamlı üreme saptandığında mutlaka uygun antibiyotikle tedavi edilir."
            ],
            "rightPoints": [
                "Rutin tarama önerilmez ve klinik olarak endike değildir.",
                "Tedavi edilmemesi böbrek parankim hasarına veya fonksiyon kaybına yol açmaz.",
                "Gereksiz antibiyotik kullanımı dirençli suş gelişimine yol açacağı için tedavi edilmez."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Diyabetik hastalarda gaz oluşturan bakterilerin böbrek parankiminde gaz ve nekroz yapmasıyla gelişen tabloya [amfizematöz] enfeksiyon denir.",
            "maskedTerm": "amfizematöz",
            "hint": "Böbrekte gaz toplanan ağır enfeksiyon nitelemesi"
        },
        {
            "type": "active_recall",
            "question": "Yenidoğan ve erken süt çocukluğu döneminde (ilk 3 ay) ÜSE görülme sıklığında cinsiyet dağılımı nasıldır?",
            "answer": "Erkek bebeklerde kız bebeklerden daha sıktır; sünnet derisi altındaki kolonizasyon ve konjenital üriner anomalilerle ilişkilidir."
        }
    ],
    50: [
        {
            "type": "causal_chain",
            "title": "Katater İlişkili Üriner Sistem Enfeksiyonunda Biyofilm Oluşum Zinciri",
            "steps": [
                "1. Üretral sonda takılmasını takiben idrardaki proteinler katater yüzeyine çöker.",
                "2. Bakteriler kataterin iç ve dış yüzeyine adezinleri aracılığıyla tutunur.",
                "3. Bakteriler çoğalarak ekstrasellüler polisakkarit matriks sentezler.",
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
                        {"text": "S. aureus bakteriyemisi veya tüberkülozun böbrek parankimine ekilmesi"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Lenfatik Yol"},
                        {"text": "Çok nadir / tartışmalı", "isMasked": True, "hint": "Lenfatik yol sıklığı"},
                        {"text": "Ağır retroperitoneal enflamasyonda lenf kanalları yoluyla geçiş"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Katater ilişkili üriner sistem enfeksiyonlarında bakteri kolonizasyonu ve antibiyotik direncinin en temel nedeni katater yüzeyinde [biyofilm] tabakası oluşmasıdır.",
            "maskedTerm": "biyofilm",
            "hint": "Katater yüzeyini saran koruyucu bakteri tabakası"
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
                        {"text": "Mesane üroepitelindeki reseptörlere bağlanır", "isMasked": True, "hint": "Mesane epitelindeki bağlanma"},
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
                        {"text": "Konak hücre membranında porlar açarak lizis yapar", "isMasked": True, "hint": "Hücre zarı parçalayıcı por"},
                        {"text": "Doku invazyonu ve demir kazanımı sağlar"}
                    ]
                },
                {
                    "cells": [
                        {"text": "K Kapsül Antijeni"},
                        {"text": "Nötrofillerin fagositozunu engeller", "isMasked": True, "hint": "Bakteriyi yutulmaktan koruyan kılıf"},
                        {"text": "Bakterinin serum bakterisidal aktivitesine direnci"}
                    ]
                }
            ]
        },
        {
            "type": "before_after_slider",
            "title": "Miksiyon Zamanına Göre Hematüri Lokalizasyonu",
            "leftTitle": "Başlangıç (İnisiyal) Hematüri",
            "rightTitle": "Total Hematüri",
            "leftPoints": [
                "Kanama sadece işemenin ilk birkaç mililitresinde görülür, sonra idrar açılır.",
                "Patolojinin lokalizasyonu anterior üretradır.",
                "Üretrit, meatal darlık veya üretral travma düşünülür."
            ],
            "rightPoints": [
                "Total hematüri işeme boyunca homojen kırmızıdır.",
                "Patolojinin lokalizasyonu mesane gövdesi, üreter veya böbrek parankimidir.",
                "Ağır sistit, taş, neoplazm veya glomerülonefrit tablosunu gösterir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Erişkinde aksi kanıtlanana kadar aksi düşünülmemesi gereken altın kural, ağrısız gros hematürinin [malignite] habercisi olduğudur.",
            "maskedTerm": "malignite",
            "hint": "Ağrısız hematüride dışlanması zorunlu primer patoloji"
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
                        {"text": "Böbrek kapsülünün akut gerilmesi", "isMasked": True, "hint": "Böbrekte gerilen ağrıya duyarlı zar"},
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
            "type": "causal_chain",
            "title": "Renal Kolik Ağrısının Nöral İletim Zinciri",
            "steps": [
                "1. Üretere düşen taş idrar akımını tıkayarak proksimal hidrostatik basıncı artırır.",
                "2. Üreter duvarındaki mekanoreseptörler ve sempatik sinir uçları uyarılır.",
                "3. Ağrı duyusu T10-L2 spinal kord segmentlerine iletilir.",
                "4. İlgili dermatomlara yansıyan ağrı böbrek lojundan kasık bölgesine ve genital organlara yayılır.",
                "5. Parasempatik ve vagal uyarı ile bulantı, kusma ve taşikardi eşlik eder."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Üriner sistemde enflamasyona bağlı ağrılar sabit ve donuk seyrederken lümen obstrüksiyonuna bağlı ağrılar dalgalar halinde gelen [kolik] tarzda ağrılardır.",
            "maskedTerm": "kolik",
            "hint": "Obstrüksiyona bağlı dalgalı ağrı türü"
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
            "type": "before_after_slider",
            "title": "Depolama (İrritatif) ile İşeme (Obstrüktif) Semptomları",
            "leftTitle": "Depolama Semptomları",
            "rightTitle": "İşeme Semptomları",
            "leftPoints": [
                "Pollaküri (gündüz sık idrara çıkma) ve noktüri (gece uyanıp idrar yapma).",
                "Acil sıkışma hissi (urgency) ve sıkışma inkontinansı.",
                "Enflamasyon ve enfeksiyöz sistitte ön plandadır."
            ],
            "rightPoints": [
                "İdrara başlamada tereddüt (hesitancy) ve zayıf idrar akımı.",
                "Kesik kesik işeme ve işemek için karın kaslarını kullanarak ıkınma.",
                "Prostat hiperplazisi veya üretral darlık gibi mekanik engellerde görülür."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Mesanenin enflamatuar irritasyonu veya detrüsör aşırı duyarlılığı sonucu aniden gelişen şiddetli ve ertelenemez işeme hissine [urgency] (acil sıkışma) denir.",
            "maskedTerm": "urgency",
            "hint": "Acil sıkışma semptomunun tıbbi adı"
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
            "sentence": "Akut piyelonefritte böbrek kapsül gerilmesine bağlı olarak kostovertebral açıya hafif darbeyle şiddetli ağrı uyanması [Giordano belirtisi] olarak adlandırılır.",
            "maskedTerm": "Giordano belirtisi",
            "hint": "KVAH muayenesinin tıp tarihindeki meşhur özel adı"
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
                        {"text": "Böbrek tübülleri ve interstisyumu", "isMasked": True, "hint": "Piyelonefrit parankimal tutulumu"},
                        {"text": "Yüksek ateş, titreme, kostovertebral açı hassasiyeti, bulantı/kusma"},
                        {"text": "Klinik KVAH hassasiyeti ve kültürde üreme"}
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
            "question": "Akut bakteriyel prostatit düşünülen bir hastada bakteriyemiyi ve sepsisi tetikleme riski nedeniyle kesinlikle KONTRENDİKE olan tanısal manevra nedir?",
            "answer": "Prostat masajı ve sert rektal tuşedir."
        }
    ]
}

D40_ENRICHMENTS = {
    20: [
        {
            "type": "cloze_masking",
            "sentence": "Cinsel yolla bulaşan enfeksiyonların kontrolünde bulaş zincirini kırmak ve yeniden enfeksiyonu önlemek için cinsel eşin eş zamanlı tedavisi şarttır.",
            "maskedTerm": "cinsel eşin",
            "hint": "Bulaş zincirini kırmada partner yaklaşımı"
        }
    ],
    30: [
        {
            "type": "interactive_table",
            "title": "HPV Tipleri, Onkojenik Risk ve Aşı Kapsamı",
            "tableHeaders": ["HPV Tipi", "Onkojenik Risk", "İlişkili Klinik Tablo / Aşı"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "HPV Tip 6 ve 11"},
                        {"text": "Düşük Risk", "isMasked": False},
                        {"text": "Kondiloma aküminata (anogenital siğil)", "isMasked": True, "hint": "Benign genital siğil tablosu"}
                    ]
                },
                {
                    "cells": [
                        {"text": "HPV Tip 16 ve 18"},
                        {"text": "Yüksek Risk", "isMasked": False},
                        {"text": "Serviks kanseri ve premalign lezyonlar", "isMasked": True, "hint": "En sık servikal kanser etkeni"}
                    ]
                },
                {
                    "cells": [
                        {"text": "9'lu Aşı (Gardasil 9)"},
                        {"text": "Genişletilmiş Koruma", "isMasked": False},
                        {"text": "HPV 6, 11, 16, 18, 31, 33, 45, 52, 58", "isMasked": True, "hint": "Aşının kapsadığı dokuz tip"}
                    ]
                }
            ]
        }
    ],
    40: [
        {
            "type": "before_after_slider",
            "title": "Hepatit B Profilaksisinde Aktif vs Pasif Bağışıklama",
            "leftTitle": "Hepatit B Aşısı (Aktif)",
            "rightTitle": "Hepatit B İmmünglobulini (HBIG - Pasif)",
            "leftPoints": [
                "Rekombinant HBsAg antijeni içerir.",
                "Uzun süreli ve kalıcı koruyucu antikor yanıtı (anti-HBs) uyarır.",
                "Koruyucu titreye ulaşması haftalar/aylar alır."
            ],
            "rightPoints": [
                "Yüksek titrede hazır insan kaynaklı anti-HBs antikoru içerir.",
                "Hemen ve geçici (anlık) koruma sağlar.",
                "Yarı ömrü sınırlıdır, kalıcı immün bellek bırakmaz."
            ]
        }
    ],
    45: [
        {
            "type": "cloze_masking",
            "sentence": "Üç doz standart Hepatit B aşısı yapılmasına rağmen anti-HBs düzeyi 10 mIU/mL altında kalan bireyler aşıya yanıtsız olarak kabul edilir.",
            "maskedTerm": "yanıtsız",
            "hint": "Non-responder birey tanımı"
        }
    ],
    50: [
        {
            "type": "causal_chain",
            "title": "HBsAg Pozitif Kaynakla Temas Sonrası Yönetim Zinciri",
            "steps": [
                "1. Maruziyetin Değerlendirilmesi: Kaynağın HBsAg durumu ve temas türü hızla doğrulanır.",
                "2. Maruz Kalanın Bağışıklık Kontrolü: Aşılama öyküsü ve belgelenmiş anti-HBs titresi sorgulanır.",
                "3. HBIG Uygulaması: Aşısız veya yanıtsız kişiye ilk 24 saat içinde tek doz HBIG intramüsküler verilir.",
                "4. Aşı Serisinin Başlatılması: HBIG ile aynı anda fakat farklı ekstremiteden Hepatit B aşı serisi başlatılır."
            ]
        }
    ],
    60: [
        {
            "type": "cloze_masking",
            "sentence": "Hepatit C virüsüne karşı koruyucu bir aşı veya immünglobulin bulunmadığından temas sonrası aktif takip ve erken DAA tedavisi esastır.",
            "maskedTerm": "aşı veya immünglobulin",
            "hint": "Spesifik immünoprofilaksi ajanı eksikliği"
        }
    ],
    70: [
        {
            "type": "branching_logic",
            "scenario": "HIV-seronegatif bir birey, partnerinin HIV-pozitif olduğunu belirterek korunma talebiyle başvuruyor. Bu olguda temas öncesi profilaksi (PrEP) için en uygun yaklaşım hangisidir?",
            "options": [
                {
                    "text": "HIV serolojisi ve böbrek fonksiyonları değerlendirilerek günlük Tenofovir + Emtrisitabin (TDF/FTC) PrEP rejimi başlamak",
                    "isCorrect": True,
                    "feedback": "Doğru! HIV temas öncesi profilakside (PrEP) standart yaklaşım, negatif seroloji teyit edildikten sonra günlük oral TDF/FTC başlanmasıdır."
                },
                {
                    "text": "Sadece şüpheli cinsel temas geliştikten sonra ilk 72 saatte acil servise başvurmasını önermek",
                    "isCorrect": False,
                    "feedback": "Yanlış. Bu yaklaşım temas sonrası profilaksidir (PEP); düzenli yüksek risk altında yaşayan serodiskordan partnerlerde PrEP endikedir."
                },
                {
                    "text": "Tek başına haftalık intramüsküler penisilin profilaksisi vermek",
                    "isCorrect": False,
                    "feedback": "Yanlış. Penisilin sifiliz profilaksisinde kullanılır; HIV bulaşını önlemede hiçbir etkinliği yoktur."
                }
            ]
        }
    ],
    80: [
        {
            "type": "interactive_table",
            "title": "Maruziyette Sıvıların HIV Bulaş Riski Düzeyi",
            "tableHeaders": ["Sıvı Türü", "Bulaş Riski Düzeyi", "Klinik Açıklama ve Kural"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Kan ve Kanlı Sıvılar"},
                        {"text": "Yüksek bulaş riski taşır", "isMasked": True, "hint": "En riskli biyolojik sıvı"},
                        {"text": "İğne batması ve mukozal maruziyette en kritik bulaş kaynağıdır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Genital Sıvılar (Semen, Vajinal Salgı)"},
                        {"text": "Yüksek bulaş riski taşır", "isMasked": True, "hint": "Cinsel bulaş sıvıları"},
                        {"text": "Cinsel temas maruziyetlerinde temel bulaş kaynağıdır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Derin Vücut Sıvıları (BOS, Plevra, Periton)"},
                        {"text": "Potansiyel bulaş riski taşır", "isMasked": True, "hint": "Steril vücut boşluğu sıvıları"},
                        {"text": "Girişimsel işlemlerde maruziyette profilaksi değerlendirilir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Ter, Tükürük, Gözyaşı, İdrar, Feçes (Kansız)"},
                        {"text": "Bulaş riski taşımaz", "isMasked": True, "hint": "Kansız doğal salgılar"},
                        {"text": "Gözle görülür kan içermedikçe profilaksi endikasyonu doğurmaz"}
                    ]
                }
            ]
        },
        {
            "type": "causal_chain",
            "title": "Kesici-Delici Alet Maruziyetinde İlk Bakım Zinciri",
            "steps": [
                "1. Maruz kalan cilt bölgesi derhal bol su ve sabunla nazikçe yıkanır.",
                "2. Doku hasarını ve viral inokülasyonu artırmamak için yara yeri kesinlikle sıkılmaz veya kanatılmaz.",
                "3. Mukozal temas varsa göz ve ağız bol serum fizyolojik veya temiz suyla yıkanır.",
                "4. Olayın saati, kaynak hastanın bilinen durumları ve maruziyet şekli derhal kayıt altına alınır.",
                "5. Temas sonrası profilaksi değerlendirmesi için enfeksiyon kontrol birimine başvurulur."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Enfeksiyöz maruziyet sonrası yara bakımı yapılırken doku hasarını artırarak virüsün daha derin dokulara yayılmasını kolaylaştırdığı için yara yerini [sıkmak] kesinlikle yasaktır.",
            "maskedTerm": "sıkmak",
            "hint": "Yara bakımında kesinlikle yapılmaması gereken mekanik işlem"
        }
    ],
    90: [
        {
            "type": "before_after_slider",
            "title": "HIV PEP Zaman Penceresi ve Etkinlik",
            "leftTitle": "İlk 72 Saat İçinde Başlama",
            "rightTitle": "72 Saat Sonrası",
            "leftPoints": [
                "En yüksek koruyucu etkinlik ilk 2-4 saatte başlandığında elde edilir.",
                "Zamanında başlanan 28 günlük rejim HIV bulaş riskini en az %80 oranında azaltır.",
                "Profilaksi protokolü eksiksiz tamamlanır ve takip testleri yapılır."
            ],
            "rightPoints": [
                "72 saat aşıldığında virüs lenf nodlarına ve hedef dokulara yerleşir.",
                "72 saat sonrasında profilaksinin koruyucu etkisi gösterilememiştir.",
                "Rutin profilaksi önerilmez; izlem ve tanısal test protokolüne geçilir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "HIV temas sonrası profilaksisi (PEP) başlanabilmesi için temastan sonra geçmesi gereken azami kritik süre [72 saat]'tir.",
            "maskedTerm": "72 saat",
            "hint": "HIV PEP için kritik azami zaman eşiği"
        },
        {
            "type": "active_recall",
            "question": "Standart HIV temas sonrası profilaksisi (PEP) protokolü kaç gün uygulanır ve hangi ilaç sınıfı bileşenlerini içerir?",
            "answer": "28 gün boyunca aralıksız uygulanır; 2 adet NRTI (Tenofovir + Emtrisitabin) ile 1 adet İntegraz inhibitörü (Raltegravir veya Dolutegravir) kombinasyonunu içerir."
        }
    ]
}

D41_ENRICHMENTS = {
    14: [
        {
            "type": "cloze_masking",
            "sentence": "Diyabetik nefropatide mezanjiyal matriks artışı ve bazal membran kalınlaşması ile karakterize yaygın lezyona [difüz mezangiyal skleroz] denir.",
            "maskedTerm": "difüz mezangiyal skleroz",
            "hint": "Yaygın mezanjiyal matriks genişlemesi"
        }
    ],
    25: [
        {
            "type": "cloze_masking",
            "sentence": "Kongo kırmızısı ile boyanan amiloid birikintileri polarize ışık mikroskobunda karakteristik [elma yeşili çift kırınım] gösterir.",
            "maskedTerm": "elma yeşili çift kırınım",
            "hint": "Polarize mikroskopta patognomonik yansıma"
        }
    ],
    33: [
        {
            "type": "cloze_masking",
            "sentence": "Eozinofilik granülomatoz polianjiyitte (Churg-Strauss) astım ve doku eozinofilisinin yanı sıra olguların yaklaşık yarısında [p-ANCA] pozitifliği saptanır.",
            "maskedTerm": "p-ANCA",
            "hint": "Perinükleer antinötrofil sitoplazmik antikor"
        }
    ],
    40: [
        {
            "type": "interactive_table",
            "title": "ANCA İlişkili Vaskülitlerde Böbrek Tutulumu ve Ayırıcı Tanı",
            "tableHeaders": ["Vaskülit Tipi", "Hedef ANCA Tipi", "Böbrek Dışı Klinik Özellikler", "Böbrek Histopatolojisi"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Granülomatozisli Polianjiyit (GPA / Wegener)"},
                        {"text": "c-ANCA (PR3-ANCA)", "isMasked": True, "hint": "Wegener'deki ana serolojik belirteç"},
                        {"text": "Üst ve alt solunum yolu nekrotizan granülomları, sinüzit, kavitasyon"},
                        {"text": "Nekrotizan kresentik glomerülonefrit (pauci-immün)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Mikroskopik Polianjiyit (MPA)"},
                        {"text": "p-ANCA (MPO-ANCA)", "isMasked": True, "hint": "MPA'daki ana serolojik belirteç"},
                        {"text": "Granülom yoktur; akciğer kapillariti ve alveolar kanama"},
                        {"text": "Nekrotizan kresentik glomerülonefrit (pauci-immün)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Eozinofilik Granülomatozisli Polianjiyit (EGPA)"},
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
        },
        {
            "type": "active_recall",
            "question": "Granülomatozisli Polianjiyitiste (GPA / Wegener) hedef antijen ve serolojik belirteç nedir?",
            "answer": "Proteinaz 3 ve c-ANCA'dır (PR3-ANCA)."
        }
    ],
    54: [
        {
            "type": "cloze_masking",
            "sentence": "Atipik hemolitik üremik sendrom tedavisinde kontrolsüz kompleman aktivasyonunu durdurmak amacıyla monoklonal C5 inhibitörü [ekulizumab] kullanılır.",
            "maskedTerm": "ekulizumab",
            "hint": "Terminal kompleman bloker antikoru"
        }
    ],
    60: [
        {
            "type": "interactive_table",
            "title": "Trombotik Mikroanjiyopatiler (TMA): TTP ile HÜS Ayrımı",
            "tableHeaders": ["Klinik / Laboratuvar Parametre", "Trombotik Trombositopenik Purpura (TTP)", "Hemolitik Üremik Sendrom (HÜS)"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Primer Patofizyolojik Mekanizma"},
                        {"text": "ADAMTS13 metalloproteinaz enzim eksikliği", "isMasked": True, "hint": "vWF parçalayıcı enzim kusuru"},
                        {"text": "Şiga toksini (Tipik) veya kompleman regülasyon defekti (Atipik)"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Baskın Organ Tutulumu"},
                        {"text": "Nörolojik semptomlar ve konfüzyon ön planda", "isMasked": True, "hint": "Santral sinir sistemi bulguları"},
                        {"text": "Akut böbrek hasarı ve anüri belirgin ön planda"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Birincil Tedavi Yaklaşımı"},
                        {"text": "Acil plazma değişimi (plazmaferez)", "isMasked": True, "hint": "Antikorları temizleyen yöntem"},
                        {"text": "Destek tedavisi / Kompleman ilişkili formda Ekulizumab"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Trombotik trombositopenik purpura (TTP) patogenezinde von Willebrand faktör multimerlerini parçalayan [ADAMTS13] enzim aktivitesinin yetersizliği yatar.",
            "maskedTerm": "ADAMTS13",
            "hint": "vWF parçalayan metalloproteinaz"
        }
    ],
    70: [
        {
            "type": "causal_chain",
            "title": "Benign Hipertansiyonda Hiyalin Arteriyoloskleroz Zinciri",
            "steps": [
                "1. Kronik ve orta dereceli hemodinamik basınç artışı arteriyol endotelinde hasar oluşturur.",
                "2. Plazma proteinleri damar duvarına sızar ve damar düz kas hücreleri ekstrasellüler matriks üretir.",
                "3. Afferent arteriyol duvarında homojen pembe hiyalin kalınlaşma meydana gelir.",
                "4. Damar lümeni daralarak glomerül ve tübüllerde kronik iskemiye yol açar.",
                "5. Glomerüllerde iskemi ve tübüler atrofi ile simetrik ince granüler böbrek yüzeyi gelişir."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Benign nefrosklerozun histopatolojik damgası olan afferent arteriyol lezyonu [hiyalin arteriyoloskleroz] olarak adlandırılır.",
            "maskedTerm": "hiyalin arteriyoloskleroz",
            "hint": "Afferent arteriyoldeki tipik vasküler lezyon adı"
        },
        {
            "type": "active_recall",
            "question": "Benign nefrosklerozda böbreklerin makroskopik dış yüzey görünümü nasıldır?",
            "answer": "Simetrik, her iki böbrekte eşit derecede ince granüler (deri benzeri / leather-grain) bir yüzey izlenir."
        }
    ],
    80: [
        {
            "type": "before_after_slider",
            "title": "Benign Nefroskleroz ile Malign Nefroskleroz Ayrımı",
            "leftTitle": "Benign Nefroskleroz",
            "rightTitle": "Malign Nefroskleroz",
            "leftPoints": [
                "Hafif-orta kronik hipertansiyon zemininde yıllar içinde yavaş gelişir.",
                "Temel histopatolojik lezyon afferent arteriyolde hiyalin arteriyolosklerozdur.",
                "Makroskopide simetrik ince granüler yüzey izlenir; üremi ve böbrek yetmezliği nadirdir."
            ],
            "rightPoints": [
                "Akut dramatik tansiyon fırlaması (Diyastolik >120 mmHg) ve papilödemle acil seyreder.",
                "Damarlarda fibrinoid nekroz ve 'soğan zarı' (onion-skinning) hiperplastik lezyonları görülür.",
                "Makroskopide peteşiyal 'pire ısırığı' görünümü vardır; hızla böbrek yetmezliğine ilerler."
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "Malign nefrosklerozda interlobüler arterlerde proliferatif düz kas ve kollajen tabakalarının oluşturduğu konsantrik lüminal daralmaya [soğan zarı] (onion-skin) lezyonu denir.",
            "maskedTerm": "soğan zarı",
            "hint": "Malign hipertansiyondaki konsantrik lüminal tabakalanma nitelemesi"
        },
        {
            "type": "active_recall",
            "question": "Malign nefrosklerozda subkapsüler kortikal peteşiyal kanamaların oluşturduğu karakteristik makroskopik görünüm hangisidir?",
            "answer": "'Pire ısırığı' (flea-bitten) böbrek görünümüdür."
        }
    ],
    90: [
        {
            "type": "causal_chain",
            "title": "Kronik Böbrek Hastalığında Kendi Kendini Besleyen Kısır Döngü",
            "steps": [
                "1. Primer renal hasar ilerleyici nefron kitle kaybına yol açar.",
                "2. Kalan sağlam nefronlarda adaptif hipertrofi ve intrakapiller hiperfiltrasyon başlar.",
                "3. Yüksek intrakapiller hidrostatik basınç sağlam glomerüllerde endotel ve podosit hasarı yaratır.",
                "4. Sağlam nefronlar da sekonder fokal glomerüloskleroza ve tübüler atrofiye uğrar.",
                "5. Kısır döngü ilerleyerek nefron kitlesini tüketir ve son dönem böbrek yetmezliğini kurar."
            ]
        },
        {
            "type": "interactive_table",
            "title": "Son Dönem Kronik Böbrek Hastalığı Morfolojik Özellikleri",
            "tableHeaders": ["Doku Bölgesi", "Karakteristik Histopatolojik Değişiklik", "Klinik Açıklama"],
            "tableRows": [
                {
                    "cells": [
                        {"text": "Glomerüller"},
                        {"text": "Global glomerüloskleroz (tam hyalinizasyon)", "isMasked": True, "hint": "Glomerüllerin tamamen sertleşmesi"},
                        {"text": "Glomerül yumağı asellüler pembe skar dokusuna dönüşür"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Tübüller"},
                        {"text": "Tübüler atrofi ve 'tiroidizasyon'", "isMasked": True, "hint": "Tiroid folliküllerine benzeme"},
                        {"text": "Genişlemiş tübüller eozinofilik silendirlerle dolarak tiroid dokusunu andırır"}
                    ]
                },
                {
                    "cells": [
                        {"text": "İnterstisyum"},
                        {"text": "İleri derecede interstisyel fibrozis", "isMasked": True, "hint": "Kollajen ve bağ dokusu artışı"},
                        {"text": "Lenfosit infiltrasyonu ve diffüz skar dokusu yerleşir"}
                    ]
                },
                {
                    "cells": [
                        {"text": "Makroskopik Görünüm"},
                        {"text": "Simetrik küçülmüş, büzük ve diffüz granüler böbrek", "isMasked": True, "hint": "Son dönem böbrek makroskopisi"},
                        {"text": "Korteks incelmiş ve böbrek ağırlığı belirgin azalmıştır"}
                    ]
                }
            ]
        },
        {
            "type": "cloze_masking",
            "sentence": "İleri evre kronik böbrek hastalığında atrofik tübüllerin pembe eozinofilik kastlarla dolarak tiroid folliküllerini andırması manzarasına [tiroidizasyon] adı verilir.",
            "maskedTerm": "tiroidizasyon",
            "hint": "Tübüllerin tiroid dokusuna benzediği morfolojik terim"
        }
    ]
}
