# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 5: Genomik İstikrarsızlık ve DNA Onarım Bozuklukları (Slayt 41 - 50)
Checkpoint: Slayt 49
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_5_slides():
    return [
        # Slayt 41
        {
            "slideNumber": 41,
            "title": "Genomik İstikrarsızlık ve Mutatör Fenotip",
            "content": (
                "Normal bir insan hücresi bölünürken DNA polimeraz enzimlerinin hata oranı son derece düşüktür "
                "(yaklaşık 10 milyar bazda 1 hata). Bu olağanüstü doğruluk, DNA tamir sistemlerinin koordineli "
                "çalışmasıyla güvenceye alınır. DNA onarım genlerinde meydana gelen kalıtsal veya edinsel bir bozukluk, "
                "hücrede yeni mutasyonların ortaya çıkma hızını yüzlerce kat artırır; bu hücresel duruma **mutatör "
                "fenotip** adı verilir. Mutatör fenotipe sahip hücreler kendiliğinden bölünmeye başlamaz; ancak "
                "onkogenler ve tümör baskılayıcı genler gibi kritik sürücü hedeflerin mutasyona uğrama olasılığı "
                "kaçınılmaz biçimde yükselir. Genomik kararsızlık karsinogenezin bağımsız bir 'hallmark' yeteneği "
                "olmaktan ziyade, tüm diğer hallmark özelliklerinin kazanılmasını sağlayan temel bir **itici zemin "
                "(enabling characteristic)** vazifesi görür."
            ),
            "elements": [
                make_cloze(
                    "DNA tamir genlerinin bozulması sonucu mutasyon birikim hızının fırlamasına mutatör fenotip adı verilir.",
                    "mutatör",
                    "Hata artıran hücresel zemin durumu"
                ),
                make_active_recall(
                    "Kanserin hallmarks (ayırt edici) sınıflamasında genomik istikrarsızlık hangi kategoride tanımlanır?",
                    "Kanserin ayırt edici özelliklerinin kazanılmasını kolaylaştıran 'etkinleştirici zemin (enabling characteristic)' olarak tanımlanır.",
                    "Habis kabiliyetlerin türemesine olanak sağlayan platform"
                )
            ]
        },

        # Slayt 42
        {
            "slideNumber": 42,
            "title": "DNA Uyuşmazlık Onarımı (MMR) Mekanizması",
            "content": (
                "**Uyuşmazlık Onarımı (Mismatch Repair - MMR)** sistemi, DNA replikasyonu sırasında DNA polimerazın "
                "proofreading aktivitesinden kaçan baz-baz uyumsuzluklarını (örneğin G karşısına T gelmesi) ve "
                "kayma hatalarını (insersiyon/delesyon ilmekleri) tanıyan ve düzelten moleküler bir denetim "
                "mekanizmasıdır. İnsan hücrelerinde bu süreç dört ana proteinin heterodimerler oluşturmasıyla "
                "yürütülür: **MSH2**, **MSH6** ile birleşerek 'MutS-alfa' kompleksini kurar ve yanlış eşleşmiş "
                "bazı yakalar; **MLH1** ise **PMS2** ile birleşerek 'MutL-alfa' kompleksini oluşturur ve hatalı "
                "yeni ipliği keserek ekzonükleazlar ve polimeraz delta aracılığıyla yeniden sentezlenmesini sağlar. "
                "Bu dört genden herhangi birinin bialelik kaybı MMR sistemini tamamen çökerterek karsinogenezi başlatır."
            ),
            "elements": [
                make_table(
                    "DNA Uyuşmazlık Onarım (MMR) Heterodimer Kompleksleri",
                    ["Kompleks Adı", "Bileşen Proteinler", "Moleküler Fonksiyon"],
                    [
                        {
                            "cells": ["MutS-alfa Kompleksi", "MSH2 ve MSH6", "Hatalı eşleşmiş nükleotid bazını tarayıp tanıma"],
                            "hiddenIndex": 1,
                            "hint": "Eşleşme hatasını ilk yakalayan ikili"
                        },
                        {
                            "cells": ["MutL-alfa Kompleksi", "MLH1 ve PMS2", "Endonükleaz kesisi yaparak tamir ekibini çağırma"],
                            "hiddenIndex": 1,
                            "hint": "Kesici ve koordine edici ikili"
                        }
                    ]
                ),
                make_active_recall(
                    "DNA uyuşmazlık onarımında (MMR) hatalı bazı ilk tanıyan MutS-alfa kompleksini oluşturan iki kilit protein hangisidir?",
                    "MSH2 ve MSH6 proteinleridir.",
                    "Hata tanıyan heterodimer bileşenleri"
                )
            ]
        },

        # Slayt 43
        {
            "slideNumber": 43,
            "title": "Mikrosatellit İnstabilitesi (MSI): Moleküler Kanıt",
            "content": (
                "İnsan genomunda 1 ila 6 baz çifti uzunluğunda, peş peşe yüzlerce kez tekrarlanan basit nükleotid "
                "dizilerine (örneğin AAAAA veya CACACA) **mikrosatellitler** denir. DNA polimeraz bu tekrarları "
                "kopyalarken sıklıkla kayar (slippage) ve tekrarlarda fazlalık veya eksiklik yaratır; sağlam bir MMR "
                "sistemi bu kaymaları anında onarır. Ancak MMR kompleksi felç olduğunda, mikrosatellit dizilerindeki "
                "uzunluk değişiklikleri düzeltilemez ve tüm genomda kaotik bir boyut değişkenliği ortaya çıkar; "
                "bu duruma **Mikrosatellit İnstabilitesi (MSI)** denir. PCR veya NGS ile standart 5 mikrosatellit "
                "belirtecinin (BAT25, BAT26, NR21, NR24, MONO27) 2 veya daha fazlasında kayma saptanması "
                "**MSI-High (MSI-H)** olarak kodlanır ve tümörün MMR yetmezliği taşıdığının kesin kanıtıdır."
            ),
            "elements": [
                make_before_after(
                    "Mikrosatellit Kararlı (MSS) vs İnstabil (MSI-H) Genom",
                    "Mikrosatellit Kararlı Genom (MSS)",
                    "MMR sistemi intaktır. Tekrarlayan mikrosatellit dizilerinin boyutu normal doku ile tümör dokusunda birebir aynı uzunluktadır.",
                    "Mikrosatellit İnstabil Genom (MSI-H)",
                    "MMR sistemi inaktiftir. Mikrosatellit bölgelerinde yaygın baz ekleme ve silinmeleri sonucu uzunluklar tamamen kaotik hale gelir.",
                    "MSI-H tümörler yüksek oranda neoantijen ürettikleri için immünoterapiye olağanüstü iyi yanıt verirler."
                ),
                make_cloze(
                    "MMR gen kusuru sonucu tekrarlayan kısa nükleotid dizilerinin boyutunun değişmesine mikrosatellit instabilitesi (MSI) adı verilir.",
                    "mikrosatellit",
                    "Kısa tandem tekrar dizileri terimi"
                )
            ]
        },

        # Slayt 44
        {
            "slideNumber": 44,
            "title": "Lynch Sendromu (HNPCC): Klinik ve Patolojik Spektrum",
            "content": (
                "**Lynch sendromu (Herediter Non-Polipozis Kolorektal Kanser - HNPCC)**, otozomal dominant geçişli "
                "en sık kalıtsal kolorektal karsinom nedenidir. Birey MSH2 (%50), MLH1 (%40), MSH6 (%7-10) veya PMS2 "
                "genlerinden birinde tek bir germline mutant alelle dünyaya gelir; hedef dokuda ikinci alel somatik "
                "olarak yitirildiğinde tümör gelişir. Lynch sendromunun klasik özellikleri şunlardır: Genç yaşta "
                "(genellikle <50 yaş) ortaya çıkış, kolonda binlerce polip olmaması (FAP'tan farkı), tümörlerin "
                "özellikle **sağ kolonda (çekum ve çıkan kolon)** yerleşmesi, histopatolojide bol müsin, taşlı yüzük "
                "hücresi ve yoğun **tümör infiltre eden lenfosit (TIL)** içermesi. Ayrıca kadınlarda birinci sırada "
                "**endometrium karsinomu**, ardından over, mide, ince bağırsak ve hepatobiliyer kanser riski fırlar."
            ),
            "elements": [
                make_table(
                    "Lynch Sendromu ile Familyal Adenomatöz Polipozis (FAP) Farkı",
                    ["Özellik", "Lynch Sendromu (HNPCC)", "Familyal Adenomatöz Polipozis (FAP)"],
                    [
                        {
                            "cells": ["Kusurlu Gen Grubu", "DNA Uyuşmazlık Onarımı (MSH2, MLH1)", "Tümör Baskılayıcı (APC geni)"],
                            "hiddenIndex": 1,
                            "hint": "Mismatch repair onarım genleri"
                        },
                        {
                            "cells": ["Kolonik Polip Sayısı", "Az sayıda (veya hiç polip yok)", "Yüzlerce ila binlerce adenomatöz polip"],
                            "hiddenIndex": 1,
                            "hint": "Non-polipozis teriminin kaynağı"
                        },
                        {
                            "cells": ["En Sık Ekstrakolonik Tümör", "Endometrium karsinomu", "Duodenum/ampulla kanseri, desmoid tümör"],
                            "hiddenIndex": 1,
                            "hint": "Kadın genital iç astarı kanseri"
                        }
                    ]
                ),
                make_active_recall(
                    "Lynch sendromu taşıyıcısı kadınlarda kolorektal kanserden sonra en sık görülen ekstrakolonik malignite hangisidir?",
                    "Endometrium adenokarsinomudur (uterus iç zarı kanseri).",
                    "Döl yatağı mukozal astar neoplazmı"
                )
            ]
        },

        # Slayt 45
        {
            "slideNumber": 45,
            "title": "Nükleotid Eksizyon Onarımı (NER) ve UV Dimerleri",
            "content": (
                "Güneş ışığından yayılan ultraviyole (özellikle UVB, 290-320 nm) ışınları, DNA çift sarmalında "
                "bitişik pirimidin bazları arasında anormal kovalent bağlar kurulmasına yol açar. Bu lezyonlar "
                "başlıca **siklobütan pirimidin dimerleri (timin-timin dimerleri)** ve 6-4 fotourunleridir. Bu hacimli "
                "fotokimyasal lezyonlar DNA heliksinin üç boyutlu konfigürasyonunu büker ve replikasyon çatalını "
                "bloke eder. Sağlıklı hücrelerde bu hacimli hasarlar yaklaşık 30 farklı proteinin koordine çalıştığı "
                "**Nükleotid Eksizyon Onarımı (NER)** mekanizması ile temizlenir. Hasarlı bölge helikazlar (XPB, XPD) "
                "ile açılır, endonükleazlar (XPF, XPG) hasarın her iki tarafından yaklaşık 24-32 nükleotidlik tek "
                "iplik parçasını kesip atar ve DNA polimeraz sağlam karşı ipliğe bakarak boşluğu hatasız doldurur."
            ),
            "elements": [
                make_causal_chain(
                    "Nükleotid Eksizyon Onarımı (NER) Moleküler Basamakları",
                    [
                        "1. Hasar Tanıma: XPC ve DDB kompleksleri DNA çift sarmalındaki hacimli pirimidin bükülmesini tespit eder.",
                        "2. Çift Sarmalın Açılması: TFIIH transkripsiyon faktörü kompleksi (XPB ve XPD helikazları) DNA'yı çözer.",
                        "3. Çift Taraflı İnsizyon: XPF (5' ucu) ve XPG (3' ucu) endonükleazları hasarlı oligonükleotid parçasını keser.",
                        "4. Eksizyon ve Boşluk: Yaklaşık 28 nükleotidlik hasarlı DNA ipliği zincirden sökülüp uzaklaştırılır.",
                        "5. Resentez ve Ligasyon: DNA Polimeraz delta/epsilon boşluğu tamamlar, DNA Ligaz I niki kapatır."
                    ]
                ),
                make_cloze(
                    "Ultraviyole ışınlarının DNA'da oluşturduğu en yaygın mutajenik fotokimyasal lezyon timin dimerleridir.",
                    "dimerleridir",
                    "Bitişik bazların kovalent eşleşmesi"
                )
            ]
        },

        # Slayt 46
        {
            "slideNumber": 46,
            "title": "Kseroderma Pigmentozum (XP)",
            "content": (
                "**Kseroderma Pigmentozum (XP)**, nükleotid eksizyon onarımı (NER) yolağında görevli yedi "
                "genden (XPA'dan XPG'ye kadar) birindeki mutasyona bağlı gelişen prototipik otozomal resesif bir "
                "DNA onarım bozukluğudur. XP hastalarında UV ışığının oluşturduğu pirimidin dimerleri onarılamaz "
                "ve genoma kalıcı olarak kazınır (özellikle karakteristik C>T ve CC>TT transisyon mutasyonları). "
                "Bu çocuklarda güneş ışığına aşırı duyarlılık, minimal güneşte dahi büllöz yanıklar, erken yaşta "
                "ciltte yaygın çillenme, atrofi ve telanjiektaziler gelişir. En trajik sonuç, 8 yaşından önce güneşe "
                "maruz kalan cilt bölgelerinde normal popülasyona kıyasla **1000 ila 2000 kat artmış** oranda "
                "**Malign Melanom**, **Skuamöz Hücreli Karsinom** ve **Bazal Hücreli Karsinom** patlak vermesidir. "
                "Hastalar ancak güneş ışığından tamamen izole edilerek korunabilir ('ay çocukları')."
            ),
            "elements": [
                make_table(
                    "Kseroderma Pigmentozum Klinik ve Genetik Özellikleri",
                    ["Parametre", "Biyolojik Gerçeklik", "Klinik Görünüm"],
                    [
                        {
                            "cells": ["Kalıtım Patern", "Otozomal Resesif", "Akraba evliliği olan ailelerde artmış sıklık"],
                            "hiddenIndex": 1,
                            "hint": "Çekinik genetik aktarım"
                        },
                        {
                            "cells": ["Kusurlu Sistem", "Nükleotid Eksizyon Onarımı (NER: XPA-XPG)", "Pirimidin fotourunlerinin temizlenememesi"],
                            "hiddenIndex": 1,
                            "hint": "Hacimli heliks hasarı tamir mekanizması"
                        },
                        {
                            "cells": ["Malignite Riski", "1000 kattan fazla cilt kanseri artışı", "Erken çocuklukta melanom, SCC ve BCC patlaması"],
                            "hiddenIndex": 1,
                            "hint": "Güneş gören deride ölümcül neoplazi"
                        }
                    ]
                ),
                make_active_recall(
                    "Kseroderma pigmentozum hastalarında nükleotid eksizyon onarımı yapılamadığı için ultraviyole maruziyetiyle oluşan karakteristik mutasyonel imza nedir?",
                    "Dipirimidin bölgelerinde C>T veya CC>TT transisyon mutasyonlarıdır.",
                    "UV etkisiyle sitozin timin dönüşümü"
                )
            ]
        },

        # Slayt 47
        {
            "slideNumber": 47,
            "title": "DNA Polimeraz Proofreading Kusurları: POLE ve POLD1",
            "content": (
                "Son yıllarda yeni nesil dizileme teknolojileri, DNA tamir mekanizmalarında yeni ve çarpıcı "
                "bir sınıfı aydınlatmıştır: **DNA Polimeraz Epsilon (POLE)** ve **Delta (POLD1)** enzimlerinin "
                "ekzonükleaz proofreading (hata okuma) kusurları. Bu polimerazlar DNA sentezi yaparken kendi "
                "ekledikleri yanlış bazı 3'→5' ekzonükleaz aktivitesiyle geriye dönüp kesip çıkartırlar. POLE geninin "
                "ekzonükleaz katalitik bölgesinde (özellikle ekzon 9-14) meydana gelen missense mutasyonlar, enzimin "
                "kendi hatalarını düzeltme yeteneğini felç eder. Bu durum hücrede eşi benzeri görülmemiş bir "
                "mutasyon patlamasına yol açar; bu tümörlerde mutasyon yükü megabaz başına 100-500 mutasyonun üzerine "
                "çıkar; bu fenotipe **ultra-hipermutasyonlu tümörler** adı verilir. Özellikle erken evre endometriyal "
                "karsinomlarda ve genç yaş kolorektal karsinomlarda saptanır."
            ),
            "elements": [
                make_table(
                    "DNA Replikasyon Hata Düzeltme Kusurları Kıyaslaması",
                    ["Kusurlu Sistem", "Mutasyon Yükü (TMB)", "Klasik Moleküler Tanı", "Klinik Örnek"],
                    [
                        {
                            "cells": ["Klasik CIN Yolu", "Düşük TMB (<10 mutasyon/Mb)", "MSS ve kromozomal anöploidi", "Sporadik sol kolon karsinomu"],
                            "hiddenIndex": 1,
                            "hint": "Standart sapma sıklığı aralığı"
                        },
                        {
                            "cells": ["MMR Kusuru (MSI-H)", "Yüksek TMB (10-100 mutasyon/Mb)", "Mikrosatellit instabilitesi", "Lynch sendromu ve sporadik MLH1 kaybı"],
                            "hiddenIndex": 1,
                            "hint": "On ile yüz arası genetik hasar derecesi"
                        },
                        {
                            "cells": ["POLE Proofreading Kusuru", "Ultra-Yüksek TMB (>100 mutasyon/Mb)", "POLE ekzonükleaz mutasyonu", "Ultra-mutant endometrium ve kolon Ca"],
                            "hiddenIndex": 1,
                            "hint": "Yüzün üzerinde devasa nükleotid fırtınası"
                        }
                    ]
                ),
                make_cloze(
                    "Replikasyon sırasında 3'-5' ekzonükleaz hata düzeltme aktivitesini kaybederek ultra-hipermutasyonlu tümörler oluşturan enzim DNA Polimeraz Epsilon (POLE) enzimidir.",
                    "POLE",
                    "Epsilon polimeraz gen kısaltması"
                )
            ]
        },

        # Slayt 48
        {
            "slideNumber": 48,
            "title": "Tümör Mutasyon Yükü (TMB) ve İmmünoterapi Yanıtı",
            "content": (
                "DNA onarım bozuklukları (MMR kusuru ve POLE mutasyonları), kanser hücresinin protein kodlayan "
                "genomunda binlerce anlamsız mutasyon oluşturur. Bu mutasyonlar hücre ribozomlarında anormal peptit "
                "dizilerinin sentezlenmesine yol açar; konak bağışıklık sistemi için tamamen yabancı olan bu mutant "
                "peptitlere **tümör neoantijenleri** adı verilir. Bir tümörün genomundaki toplam somatik mutasyon "
                "yoğunluğu **Tümör Mutasyon Yükü (TMB)** olarak tanımlanır. TMB ne kadar yüksekse, tümör hücreleri "
                "yüzeylerinde o kadar çok neoantijen sergiler ve konak sitotoksik T hücreleri tarafından 'yabancı "
                "istilacı' gibi algılanır. Tümör kendini korumak için PD-L1 ile T hücrelerini frenlese de, hastaya "
                "**İmmün Kontrol Noktası İnhibitörü (Anti-PD-1 / Anti-PD-L1 antikorları: Pembrolizumab, Nivolumab)** "
                "verildiğinde frenler çözülür ve lenfositler tümör dokusunu süratle imha eder."
            ),
            "elements": [
                make_causal_chain(
                    "Yüksek Mutasyon Yükünden İmmünoterapi Yanıtına İlerleme Zinciri",
                    [
                        "1. Onarım Kusuru: MMR veya POLE inaktivasyonu genom boyu yüzlerce ekzonik mutasyon biriktirir.",
                        "2. Neoantijen Üretimi: Mutant proteinlerden türeyen yabancı oligopeptitler MHC-I üzerinde sergilenir.",
                        "3. T Lenfosit Akını: Sitotoksik CD8+ T hücreleri tümör stromasını yoğun biçimde infiltre eder (TIL artışı).",
                        "4. Checkpoint Blokajı: Tümör hayatta kalmak için PD-L1 pompalar; T hücreleri anerjiye sürüklenir.",
                        "5. Anti-PD-1 Tedavisi ve Lizis: Pembrolizumab PD-1/PD-L1 bağını koparır; aktive T hücreleri tümörü hızla yok eder."
                    ]
                ),
                make_active_recall(
                    "DNA onarım bozukluğu taşıyan tümörlerde biriken mutant peptitlerin immün sistem tarafından yabancı antijen olarak algılanmasına ne ad verilir?",
                    "Tümör neoantijeni (neoantigen) adı verilir.",
                    "Kansere özgü yeni antijenik yapılar"
                )
            ]
        },

        # Slayt 49: CHECKPOINT 5
        {
            "slideNumber": 49,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Genomik İstikrarsızlık ve DNA Onarım Bozuklukları",
            "content": (
                "Beşinci bölümün bu tekrar sayfasında, genomik istikrarsızlığa yol açan DNA onarım kusurları ve "
                "klinik yansımaları sentezlenmektedir. DNA onarım genlerinin inaktivasyonu mutasyon hızını artırarak "
                "mutatör fenotip doğurur. DNA uyuşmazlık onarımı (MMR: MSH2, MLH1, MSH6, PMS2) replikasyon kaymalarını "
                "düzeltir; defektinde mikrosatellit instabilitesi (MSI-H) ve Lynch sendromu (sağ kolon ve endometrium "
                "karsinomu) gelişir. Nükleotid eksizyon onarımı (NER) ultraviyolenin timin dimerlerini kesip atar; "
                "kalıtsal kusuru kseroderma pigmentozumu (XP) ve çocuklukta bin kat artmış cilt kanserlerini doğurur. "
                "POLE proofreading kusurları ise ultra-hipermutasyonlu tümörler yaratır. Yüksek mutasyon yükü bol "
                "neoantijen ürettiği için bu tümörler Anti-PD-1 immünoterapisine olağanüstü yüksek yanıt verir."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp05-fc01",
                    "front": "DNA uyuşmazlık onarım (MMR) genlerindeki bozukluk sonucu tekrarlayan oligonükleotid dizilerinde boy değişkenliği oluşmasına ne ad verilir?",
                    "back": "Mikrosatellit instabilitesi (MSI) adı verilir.",
                    "hint": "Kısa tandem sekans kararsızlığı"
                },
                {
                    "id": "k1-29-cp05-fc02",
                    "front": "Güneşin ultraviyole ışınlarının oluşturduğu pirimidin dimerlerini onaramayan ve erken çocuklukta cilt kanseri patlamasıyla seyreden sendrom nedir?",
                    "back": "Kseroderma Pigmentozumdur (XP).",
                    "hint": "Işığa aşırı hassas pigmenter genetik antite"
                },
                {
                    "id": "k1-29-cp05-fc03",
                    "front": "Yüksek tümör mutasyon yükü (TMB) taşıyan MSI-H ve POLE mutant tümörlerin immün kontrole karşı tedavisinde hangi ilaç sınıfı kullanılır?",
                    "back": "İmmün kontrol noktası inhibitörleridir (Anti-PD-1 / Anti-PD-L1 antikorları).",
                    "hint": "T lenfosit frenini kaldıran monoklonal antikorlar"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 5 Özet Tablosu: DNA Onarım Kusurları",
                    ["Hastalık / Kusur", "Bozuk Onarım Yolu", "Karakteristik Klinik Tablo"],
                    [
                        {
                            "cells": ["Lynch Sendromu (HNPCC)", "Uyuşmazlık Onarımı (MMR: MSH2, MLH1)", "Sağ kolon ve endometrium karsinomu"],
                            "hiddenIndex": 1,
                            "hint": "Replikasyon kaçaklarını düzelten mekanizma"
                        },
                        {
                            "cells": ["Kseroderma Pigmentozum", "Nükleotid Eksizyon Onarımı (NER: XPA-G)", "UV duyarlılığı ve erken yaş cilt karsinomları"],
                            "hiddenIndex": 1,
                            "hint": "Güneş dimerlerini kesip çıkaran sistem"
                        }
                    ]
                )
            ]
        },

        # Slayt 50
        {
            "slideNumber": 50,
            "title": "Klinik Karar: Kolorektal ve Endometrial Kanserlerde MSI Taraması",
            "content": (
                "Güncel uluslararası onkoloji kılavuzları (NCCN, CAP), yeni tanı konmuş **tüm kolorektal ve "
                "endometrial adenokarsinom hastalarında** rutin evrensel MMR/MSI taramasını zorunlu kılmaktadır. "
                "Patolog rezeksiyon materyalinde dört MMR proteinine (MLH1, MSH2, MSH6, PMS2) immünohistokimya "
                "uygular. Herhangi bir proteinin nükleer boyanma kaybı MMR eksikliğini (dMMR) gösterir. dMMR/MSI-H "
                "saptanan olgularda üç kritik klinik karar verilir: 1) Hastaya Lynch sendromu genetik danışmanlığı "
                "verilir; 2) Evre 2 kolon kanserinde 5-FU kemoterapisinin etkisiz olduğu bilinir ve toksik tedaviden "
                "kaçınılır; 3) İleri evre olgularda FDA onaylı Anti-PD-1 immünoterapisi (Pembrolizumab) birinci "
                "basamak sistemik tedavi olarak seçilir."
            ),
            "elements": [
                make_branching_logic(
                    "52 yaşında erkek hastada rezeke edilen Evre 4 metastatik sigmoid kolon adenokarsinomu dokusunda immünohistokimya ile MSH2 ve MSH6 nükleer boyanma kaybı ve PCR ile MSI-High saptanıyor.",
                    "Bu hastada metastatik kitleyi geriletmek ve sağkalımı uzatmak için onkoloji konseyinde öncelikle tercih edilmesi gereken en rasyonel sistemik tedavi nedir?",
                    [
                        {
                            "text": "Anti-PD-1 immün kontrol noktası inhibitörü (Pembrolizumab); dMMR/MSI-H tümörler yüksek neoantijen yükü sayesinde immünoterapiye dramatik yanıt verir.",
                            "isCorrect": True,
                            "explanation": "FDA, MSI-H/dMMR taşıyan tüm metastatik solid tümörlerde tümör tipinden bağımsız (agnostik) olarak pembrolizumab kullanımını onaylamıştır."
                        },
                        {
                            "text": "Hastaya sadece tek ajan 5-Fluorourasil (5-FU) kemoterapisi verilmeli, başka hiçbir tedavi eklenmemelidir.",
                            "isCorrect": False,
                            "explanation": "dMMR tümörler 5-FU kemoterapisine dirençlidir ve tek başına verilmesi yararsızdır."
                        },
                        {
                            "text": "Tümör dokusunda tirozin kinaz mutasyonu olmadığından derhal kemik iliği nakline geçilmelidir.",
                            "isCorrect": False,
                            "explanation": "Kolon kanseri tedavisinde allojenik kemik iliği nakli endikasyonu yoktur."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Evrensel kılavuzlara göre yeni tanı konmuş kolorektal ve endometriyal karsinomlarda immünohistokimya ile taranması zorunlu olan dörtlü MMR proteini paneli hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "MLH1, MSH2, MSH6, PMS2",
                            "isCorrect": True,
                            "explanation": "Bu dört protein uyuşmazlık onarım heterodimerlerini kurar ve rutin patolojide evrensel olarak taranır."
                        },
                        {
                            "key": "B",
                            "text": "BRCA1, BRCA2, ATM, ATR",
                            "isCorrect": False,
                            "explanation": "Bunlar homolog rekombinasyon proteinleridir, MMR paneli değildir."
                        },
                        {
                            "key": "C",
                            "text": "XPA, XPB, XPC, XPD",
                            "isCorrect": False,
                            "explanation": "Bunlar nükleotid eksizyon onarımı (XP) genleridir."
                        },
                        {
                            "key": "D",
                            "text": "KRAS, NRAS, BRAF, EGFR",
                            "isCorrect": False,
                            "explanation": "Bunlar protoonkogenlerdir, DNA onarım proteini değildir."
                        }
                    ],
                    "MLH1, MSH2, MSH6 ve PMS2 standart MMR immünohistokimya panelidir."
                )
            ]
        }
    ]
