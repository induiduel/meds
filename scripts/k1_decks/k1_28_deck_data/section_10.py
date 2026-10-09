# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 10: Moleküler Karsinogenez, Onkogenler, Tümör Baskılayıcılar ve Kalıtsal Kanser Sendromları (Slayt 91 - 100)
Checkpoint: Slayt 100
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_10_slides():
    return [
        # Slayt 91
        {
            "slideNumber": 91,
            "title": "Kanser Genleri: Onkogenler ve Tümör Baskılayıcılar",
            "content": (
                "Malign neoplazmların moleküler temelinde dört ana gen grubundaki genetik hasarlar yatar: "
                "büyümeyi teşvik eden protoonkogenler, büyümeyi inhibe eden tümör baskılayıcı genler (TSG), "
                "apoptozu düzenleyen genler ve DNA onarım genleri. **Protoonkogenler**, nokta mutasyonları, "
                "gen amplifikasyonu veya kromozomal translokasyonlar sonucu kontrolsüz aktifleşerek **onkogenlere** "
                "dönüşür. Onkogenler **işlev kazanımı (gain-of-function)** mutasyonları taşır ve tek bir alelin "
                "mutasyona uğraması (**dominant etki**) neoplastik proliferasyonu tetiklemek için yeterlidir "
                "(örneğin KRAS, MYC, HER2/ERBB2). Buna karşılık **tümör baskılayıcı genler** (RB1, TP53, APC), "
                "hücre döngüsünü durduran ve hasarlı hücreleri apoptoza sevk eden fren sistemleridir. Bu genler "
                "**işlev kaybı (loss-of-function)** mutasyonlarıyla inaktive olur ve resesif karakterlidir; "
                "tümör supresör etkisinin tamamen kalkması için kural olarak genin her iki alelinin de "
                "inaktive olması (Knudson'ın iki vuruş hipotezi) gerekir."
            ),
            "elements": [
                make_before_after(
                    "Onkogenler ile Tümör Baskılayıcı Genlerin Karşılaştırması",
                    "Onkogenler (Ör. KRAS, ERBB2, MYC)",
                    "İşlev kazanımı (gain-of-function) mutasyonları. Tek alelin mutasyonu neoplazi için yeterlidir (dominant genetik davranış).",
                    "Tümör Baskılayıcı Genler (Ör. TP53, RB1, APC)",
                    "İşlev kaybı (loss-of-function) mutasyonları. Hücresel fenotipte malignite için iki alelin de inaktivasyonu gerekir (resesif).",
                    "Moleküler tedaviler onkogenleri bloke etmeye, TSG fonksiyon kaybını ise telafi etmeye odaklanır."
                ),
                make_cloze(
                    "Protoonkogenlerin neoplastik dönüşümünde tek bir alelin mutasyonla aktifleşmesi yeterli olup bu durum dominant kalıtım özelliği gösterir.",
                    "dominant",
                    "Baskın fenotipik geçiş kalıbı"
                )
            ]
        },

        # Slayt 92
        {
            "slideNumber": 92,
            "title": "Sürücü ve Yolcu Mutasyonları ve Mutasyonel İmzalar",
            "content": (
                "Bir tümör genomu dizilendiğinde binlerce nükleotid değişikliği saptanır. Ancak bu mutasyonların "
                "tümü maligniteyi eşit derecede tetiklemez. **Sürücü (driver) mutasyonlar**, neoplastik "
                "klonun hayatta kalmasını, kontrolsüz çoğalmasını ve malign fenotip kazanmasını doğrudan sağlayan, "
                "onkogen veya tümör süpresör genlerde yerleşik kritik mutasyonlardır (örneğin adenokarsinomda EGFR "
                "veya melanomda BRAF V600E). Sürücü mutasyonlar hedefe yönelik moleküler tedavilerin (tirozin kinaz "
                "inhibitörleri) birincil hedefleridir. Buna karşılık **yolcu (passenger) mutasyonlar**, genomik "
                "kararsızlık ve hücresel bölünme esnasında tesadüfen biriken, malign transformasyona doğrudan katkı "
                "sağlamayan nötr değişikliklerdir. Ancak yolcu mutasyonların genomdaki sıklığı ve nükleotid değişim "
                "örüntüsü (**mutasyonel imzalar**), tümörün hangi karsinojene maruz kaldığını (ör. tütün dumanında "
                "C:G>A:T transversiyonları, UV ışığında C>T transisyonları) ele veren moleküler bir parmak izidir."
            ),
            "elements": [
                make_table(
                    "Driver (Sürücü) ve Passenger (Yolcu) Mutasyon Dinamikleri",
                    ["Mutasyon Tipi", "Biyolojik Fonksiyon", "Terapötik Hedeflenebilirlik", "Genomik Frekans"],
                    [
                        {
                            "cells": ["Sürücü (Driver)", "Kanser fenotipini ve proliferasyonu doğrudan yönetir", "Hedefe yönelik akıllı ilaç hedefidir", "Sayıca az fakat klonda sabittir"],
                            "hiddenIndex": 1,
                            "hint": "Neoplastik kinetiği belirleyen primer güç"
                        },
                        {
                            "cells": ["Yolcu (Passenger)", "Fenotipik avantaj sağlamayan rastlantısal mutasyon", "Doğrudan tedavi hedefi teşkil etmez", "Genomda sayıca çok daha fazladır"],
                            "hiddenIndex": 1,
                            "hint": "Fenotipe katkısız nötr genomik birikim"
                        }
                    ]
                ),
                make_active_recall(
                    "Tümör hücresinde malign proliferasyonu ve sağkalımı doğrudan tetikleyen, hedefe yönelik ilaçların bağlandığı mutasyonlara ne ad verilir?",
                    "Sürücü (driver) mutasyonlar adı verilir.",
                    "Hücresel gidişatı yönlendiren biyolojik faktör"
                )
            ]
        },

        # Slayt 93
        {
            "slideNumber": 93,
            "title": "Genomik İstikrarsızlık ve DNA Onarım Kusurları",
            "content": (
                "Normal insan hücrelerinde her gün on binlerce DNA lezyonu oluşur. Sağlıklı genom bütünlüğü, "
                "birbirini tamamlayan üç ana DNA onarım sistemi tarafından korunur. Replikasyon sırasında DNA polimerazın "
                "gözünden kaçan baz eşleşme hatalarını **Uyuşmazlık Onarımı (Mismatch Repair - MMR)** sistemi düzeltir. "
                "Ultraviyole ışığı ve kimyasal aduktların oluşturduğu hacimli heliks bozuklukları (pirimidin dimerleri) "
                "**Nükleotid Eksizyon Onarımı (NER)** mekanizması ile kesilip onarılır. İyonize radyasyon ve serbest "
                "radikallerin yol açtığı en tehlikeli lezyon olan çift iplik kırıkları ise **Homolog Rekombinasyon (HR)** "
                "veya Homolog Olmayan Uç Birleştirme (NHEJ) sistemleriyle restore edilir. Bu DNA tamir sistemlerini "
                "kodlayan genlerin kalıtsal veya edinsel inaktivasyonu, tümör hücrelerinde mutasyon hızını dramatik "
                "şekilde artıran bir **mutatör fenotip** doğurur; bu zemin karsinogenezin tüm aşamalarını hızlandırır."
            ),
            "elements": [
                make_causal_chain(
                    "DNA Onarım Kusurundan Mutatör Fenotipe ve Maligniteye İlerleme",
                    [
                        "1. Kalıtsal/Somatik İle Hasar: DNA onarım sistemini kodlayan gendeki çift alelik inaktivasyon tamir kapasitesini sıfırlar.",
                        "2. Hata Düzeltme Yetersizliği: Replikasyon kaçakları ve çevresel karsinojenik lezyonlar genoma kalıcı olarak yazılır.",
                        "3. Mutatör Fenotip Oluşumu: Genom boyu binlerce yeni mutasyonun hızla biriktiği kararsız bir nükleik asit ortamı doğar.",
                        "4. Kritik Onkogen/TSG Disfonksiyonu: TP53, APC veya KRAS genlerinde sürücü mutasyonlar rastlantısal olarak kaçınılmaz şekilde tetiklenir.",
                        "5. Agresif Klon Seçilimi: Tedaviye dirençli ve invaziv neoplastik hücre populasyonu hızla genişler."
                    ]
                ),
                make_cloze(
                    "DNA tamir genlerindeki mutasyonlar sonucu genomik instabilitenin fırlaması ve mutasyon oranının katlanması mutatör fenotip olarak tanımlanır.",
                    "mutatör",
                    "Hata biriktirici hücresel zemin"
                )
            ]
        },

        # Slayt 94
        {
            "slideNumber": 94,
            "title": "Lynch Sendromu ve Mikrosatellit İnstabilitesi (MSI)",
            "content": (
                "**Lynch sendromu (Herediter Non-Polipozis Kolorektal Kanser - HNPCC)**, otozomal dominant kalıtılan "
                "en sık kalıtsal kolorektal karsinom sendromudur. Patogenezinde DNA uyuşmazlık onarım (MMR) genleri "
                "olan **MSH2, MLH1, MSH6 ve PMS2** genlerindeki germline inaktivasyon yatar. İkinci alelin de "
                "tümör dokusunda inaktive olmasıyla MMR kompleksi felç olur. Bunun sonucunda, genomda tekrarlayan "
                "kısa nükleotid dizileri olan mikrosatellit bölgelerinde delesyon veya insersiyonlar birikir; bu "
                "durum **Mikrosatellit İnstabilitesi (MSI-High)** olarak adlandırılır. Lynch sendromlu hastalarda "
                "özellikle sağ kolon (çekum, çıkan kolon) yerleşimli, müsinöz histolojide, bol tümör infiltre eden "
                "lenfosit (TIL) içeren kolorektal karsinomlar gelişir. Ayrıca kadınlarda endometrial adenokarsinom "
                "başta olmak üzere over, mide, ince bağırsak ve hepatobiliyer kanser riski ileri derecede yükselmiştir."
            ),
            "elements": [
                make_table(
                    "Lynch Sendromu Klinik ve Patolojik Parametreleri",
                    ["Özellik", "Lynch Sendromu (HNPCC)", "Klasik Sporadik Kolorektal Ca", "Klinik Önem"],
                    [
                        {
                            "cells": ["Defektif Moleküler Yol", "DNA Uyuşmazlık Onarımı (MMR: MSH2, MLH1)", "APC/Wnt beta-katenin yolu (%80-85)", "Farklı patogenetik yolak"],
                            "hiddenIndex": 1,
                            "hint": "Eşleşmeyen bazları tamir eden sistem"
                        },
                        {
                            "cells": ["Karakteristik Kolon Odağı", "Sağ kolon (çekum, proksimal kolon)", "Sol kolon ve rektosigmoid bölge", "Endoskopik taramada sağa dikkat"],
                            "hiddenIndex": 1,
                            "hint": "İleuma komşu başlangıç segmenti"
                        },
                        {
                            "cells": ["En Sık Ekstrakolonik Tümör", "Endometrium karsinomu", "Nadir ekstrakolonik tümör", "Jinekolojik takip zorunludur"],
                            "hiddenIndex": 1,
                            "hint": "Uterus kavitesini döşeyen tabaka malignitesi"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Lynch sendromunda (HNPCC) mikrosatellit instabilitesine (MSI-H) yol açan primer moleküler defekt aşağıdakilerden hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "DNA uyuşmazlık onarım (Mismatch Repair - MMR) genlerinde (MSH2, MLH1) germline mutasyon",
                            "isCorrect": True,
                            "explanation": "Lynch sendromunun temelinde MSH2, MLH1, MSH6 veya PMS2 gen kusurları ve buna bağlı MMR yetersizliği yatar."
                        },
                        {
                            "key": "B",
                            "text": "Nükleotid eksizyon onarımında görevli XPA geninin homozigot kaybı",
                            "isCorrect": False,
                            "explanation": "XPA kusuru kseroderma pigmentozumda görülür."
                        },
                        {
                            "key": "C",
                            "text": "BRCA1 geninde çift iplik kırığı onarım kusuru",
                            "isCorrect": False,
                            "explanation": "BRCA1 homolog rekombinasyon kusuruyla kalıtsal meme/over kanserine yol açar."
                        },
                        {
                            "key": "D",
                            "text": "TP53 geninde dominant negatif mutasyon",
                            "isCorrect": False,
                            "explanation": "TP53 germline mutasyonu Li-Fraumeni sendromunu oluşturur."
                        }
                    ],
                    "Lynch sendromu uyuşmazlık onarım (MMR) kusuruna bağlı mikrosatellit instabilitesiyle karakterizedir."
                )
            ]
        },

        # Slayt 95
        {
            "slideNumber": 95,
            "title": "Kseroderma Pigmentozum: Nükleotid Eksizyon Onarım Kusuru",
            "content": (
                "**Kseroderma Pigmentozum (XP)**, otozomal resesif kalıtılan ve güneş ışığına aşırı duyarlılıkla "
                "seyreden prototipik bir DNA onarım hastalığıdır. Güneşten gelen ultraviyole (UV-B) ışınları, "
                "bitişik pirimidin bazları arasında kovalent bağlar kurarak **pirimidin dimerleri (siklobütan "
                "pirimidin dimeri ve 6-4 fotourunleri)** oluşturur. Bu dimerler DNA çift sarmalının yapısını "
                "bozar ve replikasyonu bloke eder. Normalde bu hacimli nükleotid lezyonları, yaklaşık 30 farklı "
                "proteinin koordine çalıştığı **Nükleotid Eksizyon Onarımı (NER)** mekanizmasıyla (XPA'dan XPG'ye "
                "kadar olan enzimler) kesilip çıkartılır. XP hastalarında bu genlerden birindeki kalıtsal defekt "
                "nedeniyle UV hasarlı DNA onarılamaz. Sonuç olarak bu çocuklarda güneşe maruz kalan cilt alanlarında "
                "erken yaşta (genellikle 8 yaşından önce) yaygın çillenme, atrofi ve multipl **skuamöz hücreli karsinom**, "
                "**bazal hücreli karsinom** ve ölümcül **malign melanomlar** patlak verir."
            ),
            "elements": [
                make_cloze(
                    "Ultraviyole ışınlarının oluşturduğu pirimidin dimerlerini tanıyan nükleotid eksizyon onarımındaki kalıtsal kusur kseroderma pigmentozum tablosuna yol açar.",
                    "kseroderma",
                    "Işığa aşırı duyarlı pigmenter cilt hastalığı"
                ),
                make_active_recall(
                    "Kseroderma pigmentozum hastalarında ultraviyole radyasyon etkisiyle DNA zincirinde biriken ve kesilip atılamayan karakteristik lezyon nedir?",
                    "Bitişik timin veya sitozin bazları arasında kurulan kovalent pirimidin dimerleridir.",
                    "Fotokimyasal baz ikilisi"
                )
            ]
        },

        # Slayt 96
        {
            "slideNumber": 96,
            "title": "Kalıtsal Kanser Sendromları: Li-Fraumeni ve FAP",
            "content": (
                "Kalıtsal kanser yatkınlık sendromlarının çoğu, tümör baskılayıcı genlerdeki germline mutasyonlara "
                "bağlıdır ve **Knudson'ın iki vuruş (two-hit) hipotezine** uyar. Birey birinci vuruşu (ilk mutant aleli) "
                "tüm vücut hücrelerinde kalıtsal olarak taşır; neoplastik dönüşüm için hedef dokuda ikinci alelin "
                "somatik mutasyon veya delesyonla yitirilmesi (**heterozigotluk kaybı - LOH**) yeterlidir. "
                "**Li-Fraumeni Sendromu**, 'genomun koruyucusu' olan **TP53** geninin otozomal dominant germline "
                "mutasyonudur. Bu hastalarda genç yaşta yumuşak doku ve kemik sarkomları, erken meme karsinomu, "
                "beyin tümörleri, lösemi ve adrenokortikal karsinom gibi son derece geniş ve agresif bir tümör yelpazesi "
                "gözlenir. **Familial Adenomatous Polyposis (FAP)** ise 5q21 kromozomundaki **APC** geninin germline "
                "mutasyonuyla gelişir. Ergenlikten itibaren kolonda binlerce (genellikle >100-1000) adenomatöz polip "
                "ortaya çıkar; profilaktik kolektomi yapılmazsa 40 yaşına kadar kolorektal adenokarsinom riski %100'dür."
            ),
            "elements": [
                make_table(
                    "Klasik Kalıtsal Kanser Sendromları Karşılaştırması",
                    ["Sendrom Adı", "Kalıtım ve İlgili Gen", "Karakteristik Neoplazm Yelpazesi", "Malignite Riski / Davranış"],
                    [
                        {
                            "cells": ["Li-Fraumeni Sendromu", "Otozomal Dominant / TP53", "Sarkomlar, meme ca, beyin tümörü, adrenokortikal ca", "Çoklu dokularda genç yaşta multipl malignite"],
                            "hiddenIndex": 1,
                            "hint": "Genom koruyucusu p53 faktörü"
                        },
                        {
                            "cells": ["FAP (Familyal Polipozis)", "Otozomal Dominant / APC", "Kolonda binlerce adenomatöz polip", "Profilaktik kolektomi yapılmazsa %100 kolon kanseri"],
                            "hiddenIndex": 1,
                            "hint": "Wnt yolu inhibitör supresör proteini"
                        },
                        {
                            "cells": ["Retinoblastom (Familyal)", "Otozomal Dominant / RB1", "Bilateral retinoblastom ve osteosarkom", "Göz küresi ve kemik malignite riski"],
                            "hiddenIndex": 1,
                            "hint": "E2F düzenleyici hücre döngüsü kontrolörü"
                        }
                    ]
                ),
                make_micro_quiz(
                    "28 yaşındaki bir kadın hastada erken evre meme kanseri, 5 yaşındaki çocuğunda rabdomyosarkom ve babasında osteosarkom öyküsü mevcuttur. Bu ailede en olası kalıtsal sendrom ve sorumlu gen hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Lynch sendromu - MSH2",
                            "isCorrect": False,
                            "explanation": "Lynch sendromunda kolon, endometrium ve over karsinomları baskındır; sarkom spektrumu Li-Fraumeni özelliğidir."
                        },
                        {
                            "key": "B",
                            "text": "Li-Fraumeni sendromu - TP53",
                            "isCorrect": True,
                            "explanation": "Genç yaşta meme karsinomu, çocukluk çağı sarkomları (rabdomyosarkom, osteosarkom) ve beyin tümörleri birlikteliği Li-Fraumeni sendromunun (TP53 germline mutasyonu) klasik tablosudur."
                        },
                        {
                            "key": "C",
                            "text": "Ailesel Adenomatöz Polipozis - APC",
                            "isCorrect": False,
                            "explanation": "FAP sendromunda kolonda binlerce polip ve kolorektal adenokarsinom gelişir."
                        },
                        {
                            "key": "D",
                            "text": "Multipl Endokrin Neoplazi Tip 1 - MEN1",
                            "isCorrect": False,
                            "explanation": "MEN-1 paratiroid, hipofiz ve pankreas adacık tümörleriyle karakterizedir."
                        }
                    ],
                    "Sarkomlar ve meme kanserinin genç yaşta aile boyu kümelenmesi Li-Fraumeni (TP53) sendromuna işaret eder."
                )
            ]
        },

        # Slayt 97
        {
            "slideNumber": 97,
            "title": "BRCA1 / BRCA2 ve Homolog Rekombinasyon Kusuru",
            "content": (
                "**BRCA1 ve BRCA2** genleri, DNA çift iplik kırıklarının hatasız şekilde onarılmasını sağlayan "
                "**Homolog Rekombinasyon (HR)** mekanizmasının vazgeçilmez bileşenleridir. Bu genlerdeki otozomal "
                "dominant geçişli germline mutasyonlar, kalıtsal meme ve over kanserlerinin yaklaşık %50-70'inden "
                "sorumludur. BRCA1 mutasyonu taşıyıcılarında yaşam boyu meme kanseri riski %60-85, over kanseri "
                "riski ise %40-50 düzeyindedir; ayrıca bu tümörler sıklıkla ER(-), PR(-) ve HER2(-) olan agresif "
                "**üçlü negatif (triple negative)** fenotiptedir. BRCA2 mutasyonları ise kadınlarda meme ve over "
                "kanseri riskinin yanı sıra erkek meme kanseri, prostat kanseri ve melanom riskini de yükseltir. "
                "Terapötik açıdan, homolog rekombinasyon kusuru taşıyan tümör hücreleri, tek iplik kırıklarını tamir "
                "eden PARP enziminin inhibitörleri (olaparib vb.) ile bloke edildiğinde hücresel letaliteye uğrar; "
                "bu hedefe yönelik tedavi stratejisine **sentetik letalite (synthetic lethality)** adı verilir."
            ),
            "elements": [
                make_before_after(
                    "BRCA Mutasyonlu Hücrelerde Sentetik Letalite Mekanizması",
                    "Tek Başına PARP İnhibisyonu (Normal Hücre)",
                    "Tek iplik kırıkları onarılamaz ve çift iplik kırığına döner; ancak sağlam BRCA/HR sistemi kırıkları tamir eder ve hücre yaşar.",
                    "BRCA Mutant Kanser Hücresinde PARP İnhibisyonu",
                    "Tek iplik onarımı PARP ile bloke edilir; çift iplik onarımı da mutant BRCA nedeniyle yapılamaz. Çifte kusur hücreyi doğrudan apoptoza sürükler.",
                    "Sentetik letalite, kanser hücresinin spesifik genetik açığını kullanarak seçici öldürme sağlar."
                ),
                make_cloze(
                    "BRCA1 ve BRCA2 gen defekti taşıyan tümör hücrelerinde tek iplik onarımını bloke ederek sentetik letalite oluşturan ilaç grubu PARP inhibitörleridir.",
                    "inhibitörleridir",
                    "Poli-ADP riboz polimeraz engelleyicileri"
                )
            ]
        },

        # Slayt 98
        {
            "slideNumber": 98,
            "title": "Çok Aşamalı Karsinogenez ve Klonal Heterojenite",
            "content": (
                "Karsinogenez tek bir genetik olayın sonucu değil; yıllar içinde gelişen **çok basamaklı (multi-step)** "
                "bir süreçtir. Klasik kimyasal karsinogenez üç evreye ayrılır: **İnisiyasyon** (mutajenik karsinojenin "
                "DNA'da geri dönüşümsüz kalıcı hasar oluşturması), **Promosyon** (mutajen olmayan ancak hücre "
                "bölünmesini tetikleyen ajanların -ör. forbol esterleri, hormonlar- inisiye hücreyi klonal çoğaltması) "
                "ve **Progresyon** (yeni mutasyonların eklenmesiyle klonun otonom, anaplastik ve metastatik malign "
                "karakter kazanması). Tümör başlangıçta tek bir transforme hücreden (monoklonal) köken alsa da, "
                "ilerleyen hücre bölünmeleri ve genomik instabilite sonucu zamanla farklı mutasyon profillerine "
                "sahip alt gruplara ayrılır; bu olguya **klonal heterojenite** denir. Kemoterapi veya radyoterapi "
                "uygulandığında duyarlı alt klonlar ölürken, dirençli mutant subklonlar seleksiyona uğrayarak "
                "hayatta kalır ve nüks eden agresif tümör kitlesini oluşturur."
            ),
            "elements": [
                make_causal_chain(
                    "Çok Aşamalı Karsinogenez ve Tedavi Direnci Gelişimi Zinciri",
                    [
                        "1. İnisiyasyon Evresi: Karsinojen maruziyeti hedef kök hücre genomunda geri dönüşsüz sürücü DNA mutasyonu oluşturur.",
                        "2. Promosyon Evresi: Büyüme uyarıcı faktörler inisiye hücrenin klonal proliferasyonunu tetikleyerek preneoplastik odak kurar.",
                        "3. Progresyon ve Subklonlaşma: Genomik dengesizlik yeni epigenetik ve genetik sapmalar doğurarak klonal heterojenite yaratır.",
                        "4. Terapötik Seleksiyon Baskısı: Kemoterapi sitotoksik etkiyle ilaca duyarlı baskın alt klonları elimine eder.",
                        "5. Dirençli Klon Nüksü: İlaca direnç mutasyonu taşıyan minör subklon boşalan alanda monoklonal olarak yeniden ürer."
                    ]
                ),
                make_active_recall(
                    "Kimyasal karsinogenezde mutajenik olmayan ancak inisiye olmuş hücrelerin klonal proliferasyonunu indükleyen geri dönüşlü evreye ne ad verilir?",
                    "Promosyon (promotion) evresi adı verilir.",
                    "Bölünmeyi tetikleyici hızlandırıcı süreç"
                )
            ]
        },

        # Slayt 99
        {
            "slideNumber": 99,
            "title": "İmmün Kaçış Mekanizmaları ve İmmün Kontrol Noktaları",
            "content": (
                "Kanser hücreleri neoantijenler eksprese ettiği için normalde sitotoksik CD8+ T lenfositleri ve "
                "doğal öldürücü (NK) hücreler tarafından **immün gözetim (immunosurveillance)** mekanizmalarıyla "
                "yok edilir. Ancak ilerlemiş maligniteler immün sistemin saldırısından kaçmak için sofistike "
                "karşı-stratejiler geliştirir (**immün kaçış**). Bu mekanizmaların başında tümör hücrelerinde "
                "**MHC Sınıf I moleküllerinin kaybı veya down-regülasyonu** gelir; antijen sunumu bozulunca T "
                "hücreleri tümörü tanıyamaz. İkinci majör mekanizma **immün kontrol noktası ligandlarının "
                "(checkpoint ligands)** aşırı ifadesidir. Kanser hücreleri yüzeylerinde **PD-L1** eksprese ederek "
                "sitotoksik T hücrelerindeki PD-1 reseptörüne bağlanır ve lenfositi anarjik (felçli) duruma sokar. "
                "Ayrıca tümör stroması; TGF-beta, IL-10, miyeloid kaynaklı baskılayıcı hücreler (MDSC) ve **FoxP3+ "
                "regülatuvar T hücrelerini (Treg)** toplayarak immünosüpresif bir mikroçevre kalkanı oluşturur. "
                "Anti-PD-1/PD-L1 ve anti-CTLA-4 monoklonal antikorları (immün kontrol noktası inhibitörleri), "
                "bu frenleri çözerek hastanın kendi T hücrelerini tümöre karşı yeniden harekete geçirir."
            ),
            "elements": [
                make_table(
                    "Tümör İmmün Kaçış Mekanizmaları ve Moleküler Karşılıkları",
                    ["Kaçış Stratejisi", "Hücresel / Moleküler Mekanizma", "İmmün Sistemin Yanıtı", "Terapötik Müdahale"],
                    [
                        {
                            "cells": ["Antijen Sunum Kaybı", "MHC Sınıf I veya beta-2 mikroglobulin kaybı", "CD8+ sitotoksik T hücreleri tümörü tanıyamaz", "Sitokin ve NK aktivatörleri"],
                            "hiddenIndex": 1,
                            "hint": "Doku uygunluk kompleksi birinci sınıfı"
                        },
                        {
                            "cells": ["Kontrol Noktası Aktivasyonu", "PD-L1 ekspresyonu ile PD-1 reseptör uyarımı", "T lenfositte anerji ve apoptoz indüklenir", "Anti-PD-1 ve anti-PD-L1 antikorları"],
                            "hiddenIndex": 1,
                            "hint": "Programlanmış ölüm ligandı birikimi"
                        },
                        {
                            "cells": ["İmmünosüpresif Mikroçevre", "TGF-beta, IL-10, Treg ve MDSC birikimi", "Efektör T hücre fonksiyonları lokal baskılanır", "Treg inhibitörleri ve sitokin blokajı"],
                            "hiddenIndex": 1,
                            "hint": "Regülatuvar lenfositler ve baskılayıcı faktörler"
                        }
                    ]
                ),
                make_cloze(
                    "Kanser hücrelerinin yüzeyinde eksprese ederek sitotoksik T hücrelerinin PD-1 reseptörünü bağlayıp anerjiye soktuğu immün kontrol noktası molekülü PD-L1'dir.",
                    "PD-L1'dir",
                    "Programlı ölüm yüzey ligandı"
                )
            ]
        },

        # Slayt 100: CHECKPOINT 10
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Moleküler Karsinogenez ve Kalıtsal Kanser Sendromları",
            "content": (
                "Tümör biyolojisi ve terminolojisi dersinin bu son bölümünde, neoplastik transformasyonun "
                "moleküler kural ve modelleri kapsamlı biçimde bir araya getirilmiştir. Protoonkogenler işlev "
                "kazanımı mutasyonlarıyla dominant davranış sergilerken; tümör baskılayıcı genler Knudson'ın "
                "iki vuruş kuralına uygun olarak çift alelik işlev kaybıyla inaktive olur. DNA uyuşmazlık "
                "onarımı kusuru Lynch sendromunu ve mikrosatellit instabilitesini doğururken; nükleotid "
                "eksizyon onarım kusuru UV aracılı kseroderma pigmentozumu tetikler. Li-Fraumeni sendromunda "
                "germline TP53 mutasyonu genç yaşta sarkom ve meme kanserlerine zemin hazırlar; FAP'ta APC "
                "mutasyonu binlerce polip üretir. BRCA1/2 gen kusurları homolog rekombinasyon yetmezliği ile "
                "sentetik letalite zemininde PARP inhibitörlerine duyarlılık yaratır. Tümörler immün kaçış "
                "amacıyla MHC-I kaybı ve PD-L1 ligasyonu kullanarak T hücrelerini felç eder."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp10-fc01",
                    "front": "DNA uyuşmazlık onarımı (MMR) genlerindeki kalıtsal mutasyon sonucu mikrosatellit instabilitesi ve sağ kolon kanseriyle seyreden sendrom hangisidir?",
                    "back": "Lynch sendromudur (HNPCC).",
                    "hint": "Polipozis dışı kalıtsal bağırsak neoplazi tablosu"
                },
                {
                    "id": "k1-28-cp10-fc02",
                    "front": "BRCA1 ve BRCA2 mutasyonlu homolog rekombinasyon kusuru taşıyan kanser hücrelerinde sentetik letalite oluşturan enzim inhibitör grubu nedir?",
                    "back": "PARP inhibitörleridir.",
                    "hint": "Nükleer tek iplik tamir blokeri"
                },
                {
                    "id": "k1-28-cp10-fc03",
                    "front": "Genom koruyucusu TP53 geninde germline mutasyonla seyreden, genç yaşta osteosarkom, meme kanseri ve beyin tümörlerine yol açan sendrom hangisidir?",
                    "back": "Li-Fraumeni sendromudur.",
                    "hint": "Ailesel çoklu sarkom yatkınlığı"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 10 Özet Tablosu: Kalıtsal Kanser Sendromları ve Genleri",
                    ["Kalıtsal Sendrom", "Bozuk Gen / Mekanizma", "Karakteristik Malignite Yelpazesi"],
                    [
                        {
                            "cells": ["Lynch Sendromu", "MMR (MSH2, MLH1)", "Kolorektal ve endometrial kanser"],
                            "hiddenIndex": 1,
                            "hint": "Uyuşmazlık onarımı gen grubu"
                        },
                        {
                            "cells": ["Li-Fraumeni Sendromu", "TP53 (Genom bekçisi)", "Sarkom, meme ca, beyin tümörü"],
                            "hiddenIndex": 1,
                            "hint": "Apoptoz ve arrest yönetici süpresörü"
                        }
                    ]
                )
            ]
        }
    ]
